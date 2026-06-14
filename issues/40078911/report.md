# Security: UAF while deleting IndexedDB databases from (shared) workers

| Field | Value |
|-------|-------|
| **Issue ID** | [40078911](https://issues.chromium.org/issues/40078911) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Workers |
| **Reporter** | th...@gmail.com |
| **Assignee** | ho...@chromium.org |
| **Created** | 2014-02-13 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

Deleting a database from a worker while the same database is in use by another worker (and the worker triggers a reload) causes a UAF.

**VERSION**  

Chrome Version: 248869(+) ToT/Continuous(/Asan)  

Operating System: Ubuntu 13.10 x64

**REPRODUCTION CASE**  

Launch the added script

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: worker  

Crash State: See the trace below (Asan did not return detailed info)

==18840==ERROR: AddressSanitizer: heap-use-after-free on address 0x611000007368 at pc 0x7f997899e3b9 bp 0x7fffde509040 sp 0x7fffde509038  

READ of size 8 at 0x611000007368 thread T0 (chrome)

==20597==ERROR: AddressSanitizer: heap-use-after-free on address 0x6110000074a8 at pc 0x7fb8786dc3b9 bp 0x7fff3e9eae20 sp 0x7fff3e9eae18  

READ of size 8 at 0x6110000074a8 thread T0 (chrome)

## Attachments

- [delete_IDB_workers_repro.html](attachments/delete_IDB_workers_repro.html) (text/html, 407 B)
- [delete_IDB_workers_repro.html](attachments/delete_IDB_workers_repro_53218842.html) (text/html, 289 B)
- [0x611_base_WeakPtrFactory_UAF.txt](attachments/0x611_base_WeakPtrFactory_UAF.txt) (text/plain, 18.4 KB)
- [0x626_std_basic_UAF_251481.txt](attachments/0x626_std_basic_UAF_251481.txt) (text/plain, 19.8 KB)
- [ThreadState_visitStack_SEGV_trace.txt](attachments/ThreadState_visitStack_SEGV_trace.txt) (text/plain, 21.6 KB)
- [0x626_Pickle_FindNext_UAF.txt](attachments/0x626_Pickle_FindNext_UAF.txt) (text/plain, 19.0 KB)

## Timeline

### cl...@chromium.org (2014-02-13)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-02-13)

ClusterFuzz is analyzing your testcase. See https://cluster-fuzz.appspot.com/testcase?key=5640261803704320

### jl...@chromium.org (2014-02-13)

inferno: any idea why CF doesn't see the UAF here? I can reproduce locally.

==15568==ERROR: AddressSanitizer: heap-use-after-free on address 0x62600001f110 at pc 0x7ffe7c1df408 bp 0x7ffe0b669850 sp 0x7ffe0b669848
READ of size 8 at 0x62600001f110 thread T16 (Chrome_IOThread)
    #0 0x7ffe7c1df407 in std::string::_M_data() const /usr/lib/gcc/x86_64-linux-gnu/4.6/../../../../include/c++/4.6/bits/basic_string.h:288
    #1 0x7ffe7c1e0239 in std::string::_M_rep() const /usr/lib/gcc/x86_64-linux-gnu/4.6/../../../../include/c++/4.6/bits/basic_string.h:296
    #2 0x7ffe7c1df5a9 in std::string::size() const /usr/lib/gcc/x86_64-linux-gnu/4.6/../../../../include/c++/4.6/bits/basic_string.h:711
    #3 0x7ffe7c1dcf07 in std::string::assign(char const*, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/4.6/../../../../include/c++/4.6/bits/basic_string.tcc:264
    #4 0x7ffe62b8233a in IPC::internal::ChannelReader::DispatchInputData(char const*, int) /home/julien/sources/chrome/src/out/Debug/../../ipc/ipc_channel_reader.cc:106
    #5 0x7ffe62b80b04 in IPC::internal::ChannelReader::ProcessIncomingMessages() /home/julien/sources/chrome/src/out/Debug/../../ipc/ipc_channel_reader.cc:32
    #6 0x7ffe62ad9d17 in IPC::Channel::ChannelImpl::OnFileCanReadWithoutBlocking(int) /home/julien/sources/chrome/src/out/Debug/../../ipc/ipc_channel_posix.cc:679
    #7 0x7ffe62ada1ae in non-virtual thunk to IPC::Channel::ChannelImpl::OnFileCanReadWithoutBlocking(int) /home/julien/sources/chrome/src/out/Debug/../../ipc/ipc_channel_posix.cc:698
    #8 0x7ffe6e936566 in base::MessagePumpLibevent::FileDescriptorWatcher::OnFileCanReadWithoutBlocking(int, base::MessagePumpLibevent*) /home/julien/sources/chrome/src/out/Debug/../../base/message_loop/message_pump_libevent.cc:99
    #9 0x7ffe6e93c178 in base::MessagePumpLibevent::OnLibeventNotification(int, short, void*) /home/julien/sources/chrome/src/out/Debug/../../base/message_loop/message_pump_libevent.cc:356
    #10 0x7ffe6f9d3e34 in event_process_active /home/julien/sources/chrome/src/out/Debug/../../third_party/libevent/event.c:385
    #11 0x7ffe6f9ce60f in event_base_loop /home/julien/sources/chrome/src/out/Debug/../../third_party/libevent/event.c:525
    #12 0x7ffe6e93d765 in base::MessagePumpLibevent::Run(base::MessagePump::Delegate*) /home/julien/sources/chrome/src/out/Debug/../../base/message_loop/message_pump_libevent.cc:269
    #13 0x7ffe6f0a6e99 in base::MessageLoop::RunHandler() /home/julien/sources/chrome/src/out/Debug/../../base/message_loop/message_loop.cc:397
    #14 0x7ffe6f41cf6b in base::RunLoop::Run() /home/julien/sources/chrome/src/out/Debug/../../base/run_loop.cc:49
    #15 0x7ffe6f0a42ca in base::MessageLoop::Run() /home/julien/sources/chrome/src/out/Debug/../../base/message_loop/message_loop.cc:290
    #16 0x7ffe6f748d52 in base::Thread::Run(base::MessageLoop*) /home/julien/sources/chrome/src/out/Debug/../../base/threading/thread.cc:172
    #17 0x7ffe2f1f9e65 in content::BrowserThreadImpl::IOThreadRun(base::MessageLoop*) /home/julien/sources/chrome/src/out/Debug/../../content/browser/browser_thread_impl.cc:162

0x62600001f110 is located 4112 bytes inside of 10248-byte region [0x62600001e100,0x626000020908)
freed by thread T16 (Chrome_IOThread) here:
    #0 0x7ffe7c1a7881 in operator delete(void*) /usr/local/google/work/chromium/src/third_party/llvm/projects/compiler-rt/lib/asan/asan_new_delete.cc:85
    #1 0x7ffe62acc4fe in IPC::Channel::ChannelImpl::~ChannelImpl() /home/julien/sources/chrome/src/out/Debug/../../ipc/ipc_channel_posix.cc:195
    #2 0x7ffe62ae135f in IPC::Channel::~Channel() /home/julien/sources/chrome/src/out/Debug/../../ipc/ipc_channel_posix.cc:1054
    #3 0x7ffe62ae1501 in IPC::Channel::~Channel() /home/julien/sources/chrome/src/out/Debug/../../ipc/ipc_channel_posix.cc:1053
    #4 0x7ffe313a5fcc in base::DefaultDeleter<IPC::Channel>::operator()(IPC::Channel*) const /home/julien/sources/chrome/src/out/Debug/../../base/memory/scoped_ptr.h:137
    #5 0x7ffe313a64f3 in base::internal::scoped_ptr_impl<IPC::Channel, base::DefaultDeleter<IPC::Channel> >::~scoped_ptr_impl() /home/julien/sources/chrome/src/out/Debug/../../base/memory/scoped_ptr.h:220
    #6 0x7ffe313a6169 in scoped_ptr<IPC::Channel, base::DefaultDeleter<IPC::Channel> >::~scoped_ptr() /home/julien/sources/chrome/src/out/Debug/../../base/memory/scoped_ptr.h:432
    #7 0x7ffe3392df38 in content::ChildProcessHostImpl::~ChildProcessHostImpl() /home/julien/sources/chrome/src/out/Debug/../../content/common/child_process_host_impl.cc:151
    #8 0x7ffe3392e2a1 in content::ChildProcessHostImpl::~ChildProcessHostImpl() /home/julien/sources/chrome/src/out/Debug/../../content/common/child_process_host_impl.cc:144
    #9 0x7ffe2efad46c in base::DefaultDeleter<content::ChildProcessHost>::operator()(content::ChildProcessHost*) const /home/julien/sources/chrome/src/out/Debug/../../base/memory/scoped_ptr.h:137

previously allocated by thread T16 (Chrome_IOThread) here:
    #0 0x7ffe7c1a7441 in operator new(unsigned long) /usr/local/google/work/chromium/src/third_party/llvm/projects/compiler-rt/lib/asan/asan_new_delete.cc:54
    #1 0x7ffe62ae0fe2 in IPC::Channel::Channel(IPC::ChannelHandle const&, IPC::Channel::Mode, IPC::Listener*) /home/julien/sources/chrome/src/out/Debug/../../ipc/ipc_channel_posix.cc:1050
    #2 0x7ffe3392ecb2 in content::ChildProcessHostImpl::CreateChannel() /home/julien/sources/chrome/src/out/Debug/../../content/common/child_process_host_impl.cc:166
    #3 0x7ffe32f0bfb2 in content::WorkerProcessHost::Init(int, int) /home/julien/sources/chrome/src/out/Debug/../../content/browser/worker_host/worker_process_host.cc:157
    #4 0x7ffe32f68dc9 in content::WorkerServiceImpl::CreateWorkerFromInstance(content::WorkerProcessHost::WorkerInstance) /home/julien/sources/chrome/src/out/Debug/../../content/browser/worker_host/worker_service_impl.cc:396
    #5 0x7ffe32f677c6 in content::WorkerServiceImpl::CreateWorker(ViewHostMsg_CreateWorker_Params const&, int, content::WorkerMessageFilter*, content::ResourceContext*, content::WorkerStoragePartition const&, bool*) /home/julien/sources/chrome/src/out/Debug/../../content/browser/worker_host/worker_service_impl.cc:333
    #6 0x7ffe32f03eb5 in content::WorkerMessageFilter::OnCreateWorker(ViewHostMsg_CreateWorker_Params const&, int*) /home/julien/sources/chrome/src/out/Debug/../../content/browser/worker_host/worker_message_filter.cc:61
    #7 0x7ffe32f095a3 in void DispatchToMethod<content::WorkerMessageFilter, void (content::WorkerMessageFilter::*)(ViewHostMsg_CreateWorker_Params const&, int*), ViewHostMsg_CreateWorker_Params, int>(content::WorkerMessageFilter*, void (content::WorkerMessageFilter::*)(ViewHostMsg_CreateWorker_Params const&, int*), Tuple1<ViewHostMsg_CreateWorker_Params> const&, Tuple1<int>*) /home/julien/sources/chrome/src/out/Debug/../../base/tuple.h:803
    #8 0x7ffe32f08be9 in bool IPC::SyncMessageSchema<Tuple1<ViewHostMsg_CreateWorker_Params>, Tuple1<int&> >::DispatchWithSendParams<content::WorkerMessageFilter, content::WorkerMessageFilter, void (content::WorkerMessageFilter::*)(ViewHostMsg_CreateWorker_Params const&, int*)>(bool, Tuple1<ViewHostMsg_CreateWorker_Params> const&, IPC::Message const*, content::WorkerMessageFilter*, content::WorkerMessageFilter*, void (content::WorkerMessageFilter::*)(ViewHostMsg_CreateWorker_Params const&, int*)) /home/julien/sources/chrome/src/out/Debug/../../ipc/ipc_message_utils.h:825
    #9 0x7ffe32f06769 in bool ViewHostMsg_CreateWorker::Dispatch<content::WorkerMessageFilter, content::WorkerMessageFilter, void (content::WorkerMessageFilter::*)(ViewHostMsg_CreateWorker_Params const&, int*)>(IPC::Message const*, content::WorkerMessageFilter*, content::WorkerMessageFilter*, void (content::WorkerMessageFilter::*)(ViewHostMsg_CreateWorker_Params const&, int*)) /home/julien/sources/chrome/src/out/Debug/../../content/common/view_messages.h:1564
    #10 0x7ffe32f0344b in content::WorkerMessageFilter::OnMessageReceived(IPC::Message const&, bool*) /home/julien/sources/chrome/src/out/Debug/../../content/browser/worker_host/worker_message_filter.cc:42

### js...@chromium.org (2014-02-13)

[Empty comment from Monorail migration]

### jl...@chromium.org (2014-02-13)

[Empty comment from Monorail migration]

### jl...@chromium.org (2014-02-14)

The failure looks pretty spectacular. This fires a large number of workers, at some point one of them fails [why?] and the ChildProcessHost is destroyed, which takes down the IPC channel.

For some reason, there is still a (now invalid) reference to the IPC channel from the IO thread message loop.

I'm marking as "Severity High" to be conservative. It could be "Critical" since it's in the browser process, but it looks like it could be very difficult to exploit.

cmumford@chromium.org or ericu@chromium.org, could one of you jump on this?

### cl...@chromium.org (2014-02-14)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-02-14)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5640261803704320

Uploader: jln@chromium.org
Job Type: Linux_asan_chrome_mp

Crash Type: UNKNOWN
Crash Address: 0x000000000000
Crash State:
  - crash stack -
  v8::internal::FullCodeGenerator::VisitNativeFunctionLiteral
  v8::internal::FullCodeGenerator::VisitAssignment
  v8::internal::FullCodeGenerator::VisitAssignment
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=244526:244571

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv94cur2gtgzw71Ax8ijXQYFvFGAkTo7SyeewCxdXNfva0nnTJLLVu2pjw_iy8imGneJfkh3uQBtgQYbiQR76h8YUFTyhd4B9SPS8iQi_Xk_myX_-DI0ND-04Ju5Xg0P9kdFG-fGfMzm0ewQ8aAczRqYkz43AAw



### jl...@chromium.org (2014-02-14)

It looks like we're having two issues here.

This is triggering a V8 crash and that sudden "worker process" crash is triggering a UAF in the browser.

I'm restoring the original bug title and I'll create another bug for the V8 issue.

### jl...@chromium.org (2014-02-14)

We can track the V8 issue in https://crbug.com/chromium/343774.

### jl...@chromium.org (2014-02-14)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-02-14)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-02-14)

This medium+ severity security issue is a regression on trunk.

Please fix this asap. If you are unable to look into this soon, please revert your change.

- Your friendly ClusterFuzz

### js...@chromium.org (2014-02-14)

I'm seeing the same crash if I remove all of the IDB code from the repro.


### jl...@chromium.org (2014-02-14)

[Empty comment from Monorail migration]

### jl...@chromium.org (2014-02-14)

Good point jsbell@, thanks!

I still haven't had time to take a real look myself. I'm now hitting two different UAFs in the browser process.

Adding jam@ in case the first trace immediately makes sense for him.

### js...@chromium.org (2014-02-15)

And just confirming now that i have an ASan build - I see the same UAF stacks from https://crbug.com/chromium/343661#c3 with the more minimal (non-IDB) repro in https://crbug.com/chromium/343661#c14.

The UAF seems to go away if I remove the use of either SharedWorker or postMessage, but I haven't done any further digging. I <3 Workers so much...


### cl...@chromium.org (2014-02-16)

[Empty comment from Monorail migration]

### th...@gmail.com (2014-02-16)

I'm also hitting 2 different (browser process?) UAFs (original post/c#3 repro) with the debug version. Two starting with 0x626 (std::basic_string/Pickle::FindNext) and one starting with 0x611 (base::WeakPtrFactory). I assumed they were the same because I couldn't get a detailed stack out of the release version of Chrome. 

Sometimes a (trivial?) WebCore::ThreadState::visitStack crash occurs as well.

Also, The crashes/UAFs seem to start precisely @ version 248869. I can't repro any of this with 248867 (or asan debug version 248857).

### cl...@chromium.org (2014-02-17)

jsbell@: Can you please take a look or find someone else to own it.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-02-17)

[Empty comment from Monorail migration]

### jk...@chromium.org (2014-02-18)

[Empty comment from Monorail migration]

### js...@chromium.org (2014-02-18)

Thanks for the bisect, therealholden@ - I notice that r248869 is a Worker related refactor by horo@ touching worker related IPC, which looks plausible as a cause.

Since this doesn't seem to be related to IDB (unless I'm missing something - were there any IDB-specific repros remaining?) I'm going to pass it off to horo@



### th...@gmail.com (2014-02-18)

re: #23

You're welcome. There are no IDB-specific repros with a different result than the c#14 repro remaining indeed (as far as I can tell).

### js...@chromium.org (2014-02-18)

[Empty comment from Monorail migration]

### ho...@chromium.org (2014-02-19)

The heap-use-after-free bug in SharedWorker is caused by my refactoring and will be fixed by https://codereview.chromium.org/171943002.

I think heap-use-after-free bug in IPC::Channel::ChannelImpl::OnFileCanReadWithoutBlocking() is caused by https://codereview.chromium.org/150893002 and fixed by https://codereview.chromium.org/170863002.


### bu...@chromium.org (2014-02-19)

------------------------------------------------------------------------
r252010 | horo@chromium.org | 2014-02-19T08:41:01.929610Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/content/worker/websharedworker_stub.cc?r1=252010&r2=252009&pathrev=252010

Don't terminate SharedWorker while loading the script.

This path will fix the heap-use-after-free bug.

BUG=343661,344750

Review URL: https://codereview.chromium.org/171943002
------------------------------------------------------------------------

### ho...@chromium.org (2014-02-20)

[Empty comment from Monorail migration]

### th...@gmail.com (2014-02-20)

I don't understand the merge into 344750 since that report is newer than this one (343661). Shouldn't that issue have been merged into this one, or am I missing something?

### ho...@chromium.org (2014-02-20)

[Empty comment from Monorail migration]

### ho...@chromium.org (2014-02-20)

Sorry, I fixed.

### in...@chromium.org (2014-02-20)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-02-20)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-02-20)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### ho...@chromium.org (2014-02-21)

[Comment Deleted]

### ho...@chromium.org (2014-02-21)

This crash is introduced by r248869 and fixed by r252010.
Chrome 33 was branched at r241107.
Chrome 34 was branched at r251904.

So I have to merge r252010 to Chrome 34 (Branch No:1750).

### dx...@chromium.org (2014-02-21)

chrome 34 branch is 1847.  Please merge to 1847.

### ho...@chromium.org (2014-02-24)

Oh,yes.
I will merge it to 1847.

### bu...@chromium.org (2014-02-24)

------------------------------------------------------------------------
r252868 | horo@chromium.org | 2014-02-24T01:34:37.804282Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/1847/src/content/worker/websharedworker_stub.cc?r1=252868&r2=252867&pathrev=252868

Merge 252010 "Don't terminate SharedWorker while loading the scr..."

> Don't terminate SharedWorker while loading the script.
> 
> This path will fix the heap-use-after-free bug.
> 
> BUG=343661,344750
> 
> Review URL: https://codereview.chromium.org/171943002

TBR=horo@chromium.org

Review URL: https://codereview.chromium.org/175093005
------------------------------------------------------------------------

### in...@chromium.org (2014-02-25)

[Empty comment from Monorail migration]

### mb...@chromium.org (2014-03-01)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-04-04)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-04-05)

[Comment Deleted]

### ti...@chromium.org (2014-04-05)

[Comment Deleted]

### ti...@chromium.org (2014-04-05)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-04-14)

Thanks for the report - $3000 for this one. I'll start the payment process today.

### ti...@chromium.org (2014-04-15)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-04-18)

Processing via our e-payment system can take a few weeks, but reward should be on its way to you (Ref #233620). Thanks again for your help!

### ti...@chromium.org (2014-05-01)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-05-16)

This bug is a regression and does not impact stable. Removing incorrectly added Release-0-M34 label.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-05-29)

Bulk update: removing view restriction from closed bugs.

### in...@chromium.org (2014-12-16)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/343661?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/344750]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40078911)*
