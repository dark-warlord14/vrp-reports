# Security: Use-after-free in IndexedDB Transactions

| Field | Value |
|-------|-------|
| **Issue ID** | [40087795](https://issues.chromium.org/issues/40087795) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Storage>IndexedDB |
| **Reporter** | ne...@gmail.com |
| **Assignee** | dm...@chromium.org |
| **Created** | 2017-05-22 |
| **Bounty** | $10,500.00 |

## Description

**VULNERABILITY DETAILS**  

When an IndexedDB transaction is created, indexed\_db\_connection.cc stores a map from transaction id to a unique\_ptr containing the IndexedDBTransaction, and schedules some actions with the raw pointer. A compromised renderer can create a new transaction with the same id, leading to UaF when one of the raw pointers is accessed.

To fix this, we can check that the id is not already present in the map.

I'm pretty sure this affects stable as the bug was introduced in 9d00e05d1070176eb8a13f7b83d73f067946f958, but feel free to repro there if you have that version checked out (building stable isn't really available to the public).

**VERSION**  

Chrome Version: 58.0 Stable  

Operating System: All

**REPRODUCTION CASE**  

Apply crash.diff and launch the browser. The UaF is triggered on boot for me (builtin IDB usage I think).

Type of crash: browser  

Crash State: See asan.log

## Attachments

- [crash.diff](attachments/crash.diff) (application/octet-stream, 620 B)
- [asan.log](attachments/asan.log) (text/plain, 9.2 KB)
- [fix.diff](attachments/fix.diff) (application/octet-stream, 1.4 KB)
- [register_control.patch](attachments/register_control.patch) (application/octet-stream, 2.5 KB)
- [gdb.log](attachments/gdb.log) (text/plain, 3.3 KB)
- [register_control.patch](attachments/register_control_52920268.patch) (application/octet-stream, 2.5 KB)

## Timeline

### wf...@chromium.org (2017-05-23)

=================================================================
==29572==ERROR: AddressSanitizer: heap-use-after-free on address 0x615000260028 at pc 0x556d90f82d20 bp 0x7ff91f65b350 sp 0x7ff91f65b348
READ of size 4 at 0x615000260028 thread T24 (IndexedDB)
    #0 0x556d90f82d1f in mode content/browser/indexed_db/indexed_db_transaction.h:63:54
    #1 0x556d90f82d1f in content::IndexedDBTransactionCoordinator::ProcessQueuedTransactions() content/browser/indexed_db/indexed_db_transaction_coordinator.cc:117
    #2 0x556d90f823e0 in content::IndexedDBTransactionCoordinator::DidCreateTransaction(content::IndexedDBTransaction*) content/browser/indexed_db/indexed_db_transaction_coordinator.cc:37:3
    #3 0x556d90f1d668 in TransactionCreated content/browser/indexed_db/indexed_db_database.cc:1850:28
    #4 0x556d90f1d668 in content::IndexedDBDatabase::CreateTransaction(long, content::IndexedDBConnection*, std::__1::vector<long, std::__1::allocator<long> > const&, blink::WebIDBTransactionMode) content/browser/indexed_db/indexed_db_database.cc:1844
    #5 0x556d95b62ad1 in Run base/callback.h:91:12
    #6 0x556d95b62ad1 in base::debug::TaskAnnotator::RunTask(char const*, base::PendingTask*) base/debug/task_annotator.cc:59
    #7 0x556d959916c2 in base::MessageLoop::RunTask(base::PendingTask*) base/message_loop/message_loop.cc:409:19
    #8 0x556d95992600 in base::MessageLoop::DeferOrRunPendingTask(base::PendingTask) base/message_loop/message_loop.cc:420:5
    #9 0x556d959930be in base::MessageLoop::DoWork() base/message_loop/message_loop.cc:508:13
    #10 0x556d9599b50f in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_default.cc:33:31
    #11 0x556d95a1a68a in base::RunLoop::Run() base/run_loop.cc:111:14
    #12 0x556d95aa63b5 in base::Thread::ThreadMain() base/threading/thread.cc:338:3
    #13 0x556d95a940ba in base::(anonymous namespace)::ThreadFunc(void*) base/threading/platform_thread_posix.cc:71:13
    #14 0x7ff949e4c6b9 in start_thread (/lib/x86_64-linux-gnu/libpthread.so.0+0x76b9)

0x615000260028 is located 40 bytes inside of 480-byte region [0x615000260000,0x6150002601e0)
freed by thread T24 (IndexedDB) here:
    #0 0x556d8f42ae82 in operator delete(void*) (/home/ned/dev/chromium/src/out/Default/chrome+0x3126e82)
    #1 0x556d90eddd9d in operator() buildtools/third_party/libc++/trunk/include/memory:2529:13
    #2 0x556d90eddd9d in reset buildtools/third_party/libc++/trunk/include/memory:2735
    #3 0x556d90eddd9d in operator= buildtools/third_party/libc++/trunk/include/memory:2644
    #4 0x556d90eddd9d in content::IndexedDBConnection::CreateTransaction(long, std::__1::set<long, std::__1::less<long>, std::__1::allocator<long> > const&, blink::WebIDBTransactionMode, content::IndexedDBBackingStore::Transaction*) content/browser/indexed_db/indexed_db_connection.cc:115
    #5 0x556d90f1d605 in content::IndexedDBDatabase::CreateTransaction(long, content::IndexedDBConnection*, std::__1::vector<long, std::__1::allocator<long> > const&, blink::WebIDBTransactionMode) content/browser/indexed_db/indexed_db_database.cc:1840:51
    #6 0x556d95b62ad1 in Run base/callback.h:91:12
    #7 0x556d95b62ad1 in base::debug::TaskAnnotator::RunTask(char const*, base::PendingTask*) base/debug/task_annotator.cc:59
    #8 0x556d959916c2 in base::MessageLoop::RunTask(base::PendingTask*) base/message_loop/message_loop.cc:409:19
    #9 0x556d95992600 in base::MessageLoop::DeferOrRunPendingTask(base::PendingTask) base/message_loop/message_loop.cc:420:5
    #10 0x556d959930be in base::MessageLoop::DoWork() base/message_loop/message_loop.cc:508:13
    #11 0x556d9599b50f in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_default.cc:33:31
    #12 0x556d95a1a68a in base::RunLoop::Run() base/run_loop.cc:111:14
    #13 0x556d95aa63b5 in base::Thread::ThreadMain() base/threading/thread.cc:338:3
    #14 0x556d95a940ba in base::(anonymous namespace)::ThreadFunc(void*) base/threading/platform_thread_posix.cc:71:13
    #15 0x7ff949e4c6b9 in start_thread (/lib/x86_64-linux-gnu/libpthread.so.0+0x76b9)

previously allocated by thread T24 (IndexedDB) here:
    #0 0x556d8f42a282 in operator new(unsigned long) (/home/ned/dev/chromium/src/out/Default/chrome+0x3126282)
    #1 0x556d90edb193 in content::IndexedDBClassFactory::CreateIndexedDBTransaction(long, content::IndexedDBConnection*, std::__1::set<long, std::__1::less<long>, std::__1::allocator<long> > const&, blink::WebIDBTransactionMode, content::IndexedDBBackingStore::Transaction*) content/browser/indexed_db/indexed_db_class_factory.cc:47:48
    #2 0x556d90eddabc in content::IndexedDBConnection::CreateTransaction(long, std::__1::set<long, std::__1::less<long>, std::__1::allocator<long> > const&, blink::WebIDBTransactionMode, content::IndexedDBBackingStore::Transaction*) content/browser/indexed_db/indexed_db_connection.cc:112:37
    #3 0x556d90f1d605 in content::IndexedDBDatabase::CreateTransaction(long, content::IndexedDBConnection*, std::__1::vector<long, std::__1::allocator<long> > const&, blink::WebIDBTransactionMode) content/browser/indexed_db/indexed_db_database.cc:1840:51
    #4 0x556d95b62ad1 in Run base/callback.h:91:12
    #5 0x556d95b62ad1 in base::debug::TaskAnnotator::RunTask(char const*, base::PendingTask*) base/debug/task_annotator.cc:59
    #6 0x556d959916c2 in base::MessageLoop::RunTask(base::PendingTask*) base/message_loop/message_loop.cc:409:19
    #7 0x556d95992600 in base::MessageLoop::DeferOrRunPendingTask(base::PendingTask) base/message_loop/message_loop.cc:420:5
    #8 0x556d959930be in base::MessageLoop::DoWork() base/message_loop/message_loop.cc:508:13
    #9 0x556d9599b50f in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_default.cc:33:31
    #10 0x556d95a1a68a in base::RunLoop::Run() base/run_loop.cc:111:14
    #11 0x556d95aa63b5 in base::Thread::ThreadMain() base/threading/thread.cc:338:3
    #12 0x556d95a940ba in base::(anonymous namespace)::ThreadFunc(void*) base/threading/platform_thread_posix.cc:71:13
    #13 0x7ff949e4c6b9 in start_thread (/lib/x86_64-linux-gnu/libpthread.so.0+0x76b9)

Thread T24 (IndexedDB) created by T0 (chrome) here:
    #0 0x556d8f3e8f1d in __interceptor_pthread_create (/home/ned/dev/chromium/src/out/Default/chrome+0x30e4f1d)
    #1 0x556d95a9323b in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThread::Delegate*, base::PlatformThreadHandle*, base::ThreadPriority) base/threading/platform_thread_posix.cc:110:13
    #2 0x556d95aa55c7 in base::Thread::StartWithOptions(base::Thread::Options const&) base/threading/thread.cc:112:15
    #3 0x556d95aa5246 in base::Thread::Start() base/threading/thread.cc:75:10
    #4 0x556d90936926 in content::BrowserMainLoop::BrowserThreadsStarted() content/browser/browser_main_loop.cc:1415:23
    #5 0x556d915f97a1 in Run base/callback.h:80:12
    #6 0x556d915f97a1 in content::StartupTaskRunner::RunAllTasksNow() content/browser/startup_task_runner.cc:45
    #7 0x556d9093402d in content::BrowserMainLoop::CreateStartupTasks() content/browser/browser_main_loop.cc:957:25
    #8 0x556d90944481 in content::BrowserMainRunnerImpl::Initialize(content::MainFunctionParams const&) content/browser/browser_main_runner.cc:127:17
    #9 0x556d9092b327 in content::BrowserMain(content::MainFunctionParams const&) content/browser/browser_main.cc:42:32
    #10 0x556d94bf5267 in content::ContentMainRunnerImpl::Run() content/app/content_main_runner.cc:705:12
    #11 0x556d94c0ff1d in service_manager::Main(service_manager::MainParams const&) services/service_manager/embedder/main.cc:469:29
    #12 0x556d94bf113f in content::ContentMain(content::ContentMainParams const&) content/app/content_main.cc:19:10
    #13 0x556d8f42d29a in ChromeMain chrome/app/chrome_main.cc:109:12
    #14 0x7ff94988682f in __libc_start_main /build/glibc-9tT8Do/glibc-2.23/csu/../csu/libc-start.c:291

SUMMARY: AddressSanitizer: heap-use-after-free content/browser/indexed_db/indexed_db_transaction.h:63:54 in mode
Shadow bytes around the buggy address:
  0x0c2a80043fb0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c2a80043fc0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c2a80043fd0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c2a80043fe0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c2a80043ff0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
=>0x0c2a80044000: fd fd fd fd fd[fd]fd fd fd fd fd fd fd fd fd fd
  0x0c2a80044010: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c2a80044020: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c2a80044030: fd fd fd fd fd fd fd fd fd fd fd fd fa fa fa fa
  0x0c2a80044040: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c2a80044050: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
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
==29572==ABORTING


### wf...@chromium.org (2017-05-23)

dmurph -> can you take a look at this external report?

[Monorail components: Blink>Storage>IndexedDB]

### sh...@chromium.org (2017-05-23)

[Empty comment from Monorail migration]

### ne...@gmail.com (2017-05-28)

The attached renderer patch reliably crashes the browser with a
controlled register. I built this on Ubuntu 16.04.2 LTS; the size
required to reclaim the object and the offset of mode may differ
on other builds.

### ne...@gmail.com (2017-05-31)

I apologize for the noise, but I realized my last patch was on a build with one of the sanitizers compiled in. This one gets two registers without any special build options; the size of the sprayed object had to be increased slightly. Without a leak, this is tricky to exploit alone since interesting things (e.g. sending a leak back to renderer over IPC) requires having a valid pointer in the now-null weak_ptr factory, but it's possible I missed something. Cheers!

(gdb) info reg
rax            0xfc12a9ebe70	17322318151280
rbx            0x4141414141414141	4702111234474983745
rcx            0x7	7
rdx            0x0	0
rsi            0x3	3
rdi            0x28	40
rbp            0x7fffda91a440	0x7fffda91a440
rsp            0x7fffda91a3e0	0x7fffda91a3e0
r8             0x0	0
r9             0x0	0
r10            0x0	0
r11            0x206	518
r12            0x7fffda91a440	140736860365888
r13            0x4141414141414161	4702111234474983777
r14            0xfc12a9f3b01	17322318183169
r15            0x7fffda91a438	140736860365880
rip            0x5555566ee607	0x5555566ee607 <std::_Rb_tree<long, long, std::_Identity<long>, std::less<long>, std::allocator<long> >::_M_insert_unique<std::_Rb_tree_const_iterator<long> >(std::_Rb_tree_const_iterator<long>, std::_Rb_tree_const_iterator<long>)+103>
eflags         0x10202	[ IF RF ]
cs             0x33	51
ss             0x2b	43
ds             0x0	0
es             0x0	0
fs             0x0	0
gs             0x0	0


### bu...@chromium.org (2017-05-31)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/11601c08e92732d2883af2057c41c17cba890844

commit 11601c08e92732d2883af2057c41c17cba890844
Author: Daniel Murphy <dmurph@chromium.org>
Date: Wed May 31 17:12:06 2017

[IndexedDB] Fixed transaction use-after-free vuln

Bug: 725032
Change-Id: I689ded6c74d5563403587b149c3f3e02e807e4aa
Reviewed-on: https://chromium-review.googlesource.com/518483
Reviewed-by: Joshua Bell <jsbell@chromium.org>
Commit-Queue: Daniel Murphy <dmurph@chromium.org>
Cr-Commit-Position: refs/heads/master@{#475952}
[modify] https://crrev.com/11601c08e92732d2883af2057c41c17cba890844/content/browser/indexed_db/database_impl.cc
[modify] https://crrev.com/11601c08e92732d2883af2057c41c17cba890844/content/browser/indexed_db/indexed_db_connection.cc


### dm...@chromium.org (2017-05-31)

requesting merges for all versions

### sh...@chromium.org (2017-05-31)

This bug requires manual review: We are only 5 days from stable.
Please contact the milestone owner if you have questions.
Owners: amineer@(Android), cmasso@(iOS), gkihumba@(ChromeOS), Abdul Syed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ab...@chromium.org (2017-05-31)

+ awhalley@ for security review. 

### sh...@chromium.org (2017-06-01)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2017-06-01)

Your change meets the bar and is auto-approved for M60. Please go ahead and merge the CL to branch 3112 manually. Please contact milestone owner if you have questions.
Owners: amineer@(Android), cmasso@(iOS), josafat@(ChromeOS), bustamante@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2017-06-01)

We are not planning any further M58 stable releases. Hence, rejecting merge to M58.

### bu...@chromium.org (2017-06-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/8fa06d4080e85f301966dec124bcab380f65bc83

commit 8fa06d4080e85f301966dec124bcab380f65bc83
Author: Daniel Murphy <dmurph@chromium.org>
Date: Thu Jun 01 18:05:17 2017

[IndexedDB] Fixed transaction use-after-free vuln

TBR=dmurph@chromium.org

(cherry picked from commit 11601c08e92732d2883af2057c41c17cba890844)

Bug: 725032
Change-Id: I689ded6c74d5563403587b149c3f3e02e807e4aa
Reviewed-on: https://chromium-review.googlesource.com/518483
Reviewed-by: Joshua Bell <jsbell@chromium.org>
Commit-Queue: Daniel Murphy <dmurph@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#475952}
Reviewed-on: https://chromium-review.googlesource.com/521762
Reviewed-by: Daniel Murphy <dmurph@chromium.org>
Cr-Commit-Position: refs/branch-heads/3112@{#97}
Cr-Branched-From: b6460e24cf59f429d69de255538d0fc7a425ccf9-refs/heads/master@{#474897}
[modify] https://crrev.com/8fa06d4080e85f301966dec124bcab380f65bc83/content/browser/indexed_db/database_impl.cc
[modify] https://crrev.com/8fa06d4080e85f301966dec124bcab380f65bc83/content/browser/indexed_db/indexed_db_connection.cc


### sh...@chromium.org (2017-06-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-06-02)

Let's not rush this into the 58 stable release on Monday, but we should consider it for any 58 stable updates.

### aw...@google.com (2017-06-02)

s/58/59/ 

### ab...@chromium.org (2017-06-02)

thanks - let's hold off on taking this merge now as Andrew suggested.

### aw...@chromium.org (2017-06-05)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-06-05)

[Empty comment from Monorail migration]

### ab...@chromium.org (2017-06-07)

We're planning an M59 respin for next week. Can you please confirm if this fix has been well tested/verified in canary? Is it a safe merge overall?

### dm...@chromium.org (2017-06-08)

Yes it has been in Canary for a while, I believe it is safe

### dm...@chromium.org (2017-06-08)

I think it is safe to merge.

### aw...@chromium.org (2017-06-08)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-06-08)

Great news! The VRP Panel decided to award $10,00 for this bug, and a $500 bonus for supplying the suggested fix.  Nice one!

### aw...@chromium.org (2017-06-08)

[Empty comment from Monorail migration]

### ab...@chromium.org (2017-06-08)

Per discussion with awhalley@, merges should be baked in beta first, before coming to stable. Since this was merged in M60 7 days ago, can someone please confirm and verify the fix in M60 Beta?

### dm...@chromium.org (2017-06-09)

It's in 60.0.3112.20
https://chromiumdash.appspot.com/commit/8fa06d4080e85f301966dec124bcab380f65bc83

### ab...@chromium.org (2017-06-10)

Approving merge to M59. 

### ne...@gmail.com (2017-06-11)

Thanks for the generous reward!

### bu...@chromium.org (2017-06-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/fdb26c79ea82251077cfebd14e4f8da036f059a5

commit fdb26c79ea82251077cfebd14e4f8da036f059a5
Author: Daniel Murphy <dmurph@chromium.org>
Date: Mon Jun 12 18:43:06 2017

[IndexedDB] Fixed transaction use-after-free vuln

TBR=dmurph@chromium.org

(cherry picked from commit 11601c08e92732d2883af2057c41c17cba890844)

(cherry picked from commit 8fa06d4080e85f301966dec124bcab380f65bc83)

Bug: 725032
Change-Id: I689ded6c74d5563403587b149c3f3e02e807e4aa
Reviewed-on: https://chromium-review.googlesource.com/518483
Reviewed-by: Joshua Bell <jsbell@chromium.org>
Commit-Queue: Daniel Murphy <dmurph@chromium.org>
Cr-Original-Original-Commit-Position: refs/heads/master@{#475952}
Reviewed-on: https://chromium-review.googlesource.com/521762
Reviewed-by: Daniel Murphy <dmurph@chromium.org>
Cr-Original-Commit-Position: refs/branch-heads/3112@{#97}
Cr-Original-Branched-From: b6460e24cf59f429d69de255538d0fc7a425ccf9-refs/heads/master@{#474897}
Reviewed-on: https://chromium-review.googlesource.com/531775
Cr-Commit-Position: refs/branch-heads/3071@{#777}
Cr-Branched-From: a106f0abbf69dad349d4aaf4bcc4f5d376dd2377-refs/heads/master@{#464641}
[modify] https://crrev.com/fdb26c79ea82251077cfebd14e4f8da036f059a5/content/browser/indexed_db/database_impl.cc
[modify] https://crrev.com/fdb26c79ea82251077cfebd14e4f8da036f059a5/content/browser/indexed_db/indexed_db_connection.cc


### aw...@chromium.org (2017-06-12)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-06-12)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-09-08)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/725032?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40087795)*
