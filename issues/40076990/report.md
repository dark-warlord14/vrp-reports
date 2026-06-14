# postTaskForModeToWorkerContext/dispatchTaskToWorkerThread invalid pointer crash with Workers/FileSystem API

| Field | Value |
|-------|-------|
| **Issue ID** | [40076990](https://issues.chromium.org/issues/40076990) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals |
| **Reporter** | th...@gmail.com |
| **Assignee** | me...@chromium.org |
| **Created** | 2013-02-16 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

A reproducible (freed pointer) postTaskForModeToWorkerContext/dispatchTaskToWorkerThread crash occurs when a (FileSystem) file is continuously read/written (or at least opened) from a worker while the script is reloaded from an onmessage event triggered by Postmessage from within the file entry's onloadend event.

I've hit all sorts of invalid pointers. Sometimes they are caught by a "PureCall" breakdebugger crash. Sometimes the stack is damaged and !analyze shows things like "Bad Instruction Pointer". However, there is always an invalid pointer on the stack.

I have collected full stack traces from three operating systems (WinXP, Win7, Linux, all 32-bit) with clear information on what is going on. This probably reproduces on all OS's, but (most likely) depends on the speed of thread creation/destruction, so (repro) results may vary.

Also, with Chrome stable, the crash occurs with WebWorkerClientImpl::postTaskForModeToWorkerContext, while later versions (code changes) have WorkerFileWriterCallbacksBridge::dispatchTaskToWorkerThread on the stack.

**VERSION**  

Chrome Version: All (24.0.1312.57 stable up to ToT 178923)  

Operating System: Windows XP SP3, Windows 7 and Ubuntu 12.10

**REPRODUCTION CASE**  

Launch the added repro script

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Check the added stack traces from the three operating systems mentioned above. I could not get a trace from Linux (Ubuntu 12.10) with the stable version of Chrome, because I do not have access to the (stable) symbol files.

Type of crash: the crash happens in the "CrRendererMain" thread of the child process.

## Attachments

- [filesystem_postTaskForModeToWorkerContext_crash_Win7_Stable_trace.txt](attachments/filesystem_postTaskForModeToWorkerContext_crash_Win7_Stable_trace.txt) (text/x-c++; charset=us-ascii, 78.0 KB)
- [filesystem_postTaskForModeToWorkerContext_crash_WinXP_Stable_trace.txt](attachments/filesystem_postTaskForModeToWorkerContext_crash_WinXP_Stable_trace.txt) (text/x-c++; charset=us-ascii, 69.3 KB)
- [filesystem_dispatchTaskToWorkerThread_crash_Linux_ToT_trace.txt](attachments/filesystem_dispatchTaskToWorkerThread_crash_Linux_ToT_trace.txt) (text/x-c; charset=us-ascii, 9.7 KB)
- [filesystem_dispatchTaskToWorkerThread_crash_WinXP_ToT_trace.txt](attachments/filesystem_dispatchTaskToWorkerThread_crash_WinXP_ToT_trace.txt) (text/x-c++; charset=us-ascii, 85.2 KB)
- [filesystem_crash_repro.html](attachments/filesystem_crash_repro.html) (text/plain; charset=us-ascii, 1.6 KB)
- [filesystem_dispatchTaskToWorkerThread_crash_Win7_ToT_trace.txt](attachments/filesystem_dispatchTaskToWorkerThread_crash_Win7_ToT_trace.txt) (text/x-c++; charset=us-ascii, 82.6 KB)
- [176692_noworkers_trace1.txt](attachments/176692_noworkers_trace1.txt) (text/x-c++; charset=us-ascii, 63.8 KB)
- [176692_vp8_six_tap_mmx_trace.txt](attachments/176692_vp8_six_tap_mmx_trace.txt) (text/x-c++; charset=us-ascii, 85.2 KB)
- [176692_noworkers_trace2.txt](attachments/176692_noworkers_trace2.txt) (text/x-c++; charset=us-ascii, 68.1 KB)
- [176692_crash_addresses.txt](attachments/176692_crash_addresses.txt) (text/plain; charset=us-ascii, 5.6 KB)

## Timeline

### th...@gmail.com (2013-02-16)

Better version info:

VERSION
Chrome Version: All (24.0.1312.57 stable up to ToT 182757)
Operating System: Windows XP SP3, Windows 7 and Ubuntu 12.10

### ts...@chromium.org (2013-02-19)

@kbr - could you take a look or assign an appropriate owner.

I was not able to reproduce this under ASAN linux 64 either in trunk or m25. We'll treat this as severity high for now, though I expect it may be much lower due to the apparent lack of control over the crash address.

### kb...@chromium.org (2013-02-19)

Proactively assigning to @michaeln and CC'ing a couple of other people.

I vaguely recall a similar bug being reported within the past week or so. Possibly a duplicate?


### js...@chromium.org (2013-02-19)

Vaguely related to 172240 in that having Worker scripts pound on available Async APIs during worker thread and/or renderer shutdown is turning up issues. But in this case it looks like it's the main renderer thread that's crashed, rather than a Worker crashing after the renderer thread has started cleanup.

(kbr@ may be thinking of something else, though.)

### ts...@chromium.org (2013-02-19)

[Empty comment from Monorail migration]

### js...@chromium.org (2013-02-20)

@michaeln, @jsbell - Any progress here?

### mi...@chromium.org (2013-02-20)

Looks like WorkerFileWriterCallbacksBridge::m_proxy (a raw pointer) is no longer valid.

### th...@gmail.com (2013-02-24)

It seems that this issue is the exact opposite of 172240. 172240 describes a worker crash happening when the renderer thread has started cleanup (or has been cleaned up completely, I've seen stacks without a renderer thread on 172240) and this issue is about the renderer thread crashing when/after the worker thread has started cleanup? At least that is what it looks like to me.

Since I can reproduce the issue reliably (on all OS's), I've collected a few crash stacks to look for more clues. I've added two of those to this comment, with a dispatchTaskToWorkerThread call while there are no workers on the stack at all. This results in all sorts of bad pointer trouble.

Also, even if there are workers on the crash stack, the worker(s) needed by the renderer thread may have already been (partially) freed at that time.

While I was testing, I also got vp8_six_tap_mmx crashes (added). Although they are (most likely) caused by the same issue, I can't seem to understand why vp8 would even be on the crash stack.

### mi...@chromium.org (2013-02-25)

Geeez... tough spelunking thru the worker code given all the layers of indirection. There be dragons in these dark places.

The WorkerFileWriterCallbacksBridge::m_proxy, that raw pointer that seems to have gone bad and resulting in PureCall crashes, is a pointer to an instance of WebWorkerClientImpl. Its created in Worker::Worker.


inline Worker::Worker(ScriptExecutionContext* context)
    : AbstractWorker(context)
    , m_contextProxy(WorkerContextProxy::create(this))  // m_contextProxy is raw pointer too
{
}

WorkerContextProxy* WorkerContextProxy::create(Worker* worker)
{
    ASSERT(s_workerContextProxyCreateFunction);
    return s_workerContextProxyCreateFunction(worker);
}

// s_workerContextProxyCreateFunction is setup to be this function
WorkerContextProxy* WebWorkerClientImpl::createWorkerContextProxy(Worker* worker)
{
    if (worker->scriptExecutionContext()->isDocument()) {
        Document* document = static_cast<Document*>(worker->scriptExecutionContext());
        WebFrameImpl* webFrame = WebFrameImpl::fromFrame(document->frame());
        WebWorkerClientImpl* proxy = new WebWorkerClientImpl(worker, webFrame);
        return proxy;
    }
    ASSERT_NOT_REACHED();
    return 0;
}


Locating the balancing delete in this maze is really something. Worker::~Worker invokes m_contextProxy->workerObjectDestroyed.

void WorkerMessagingProxy::workerObjectDestroyed()
{
    m_workerObject = 0;
    m_scriptExecutionContext->postTask(createCallbackTask(&workerObjectDestroyedInternal, AllowCrossThreadAccess(this)));
}

void WorkerMessagingProxy::workerObjectDestroyedInternal(ScriptExecutionContext*, WorkerMessagingProxy* proxy)
{
    proxy->m_mayBeDestroyed = true;
    if (proxy->m_workerThread)
        proxy->terminateWorkerContext();
    else
        proxy->workerContextDestroyedInternal();
}

void WorkerMessagingProxy::workerContextDestroyedInternal()
{
    // WorkerContextDestroyedTask is always the last to be performed, so the proxy is not needed for communication
    // in either side any more. However, the Worker object may still exist, and it assumes that the proxy exists, too.
    m_askedToTerminate = true;
    m_workerThread = 0;

    InspectorInstrumentation::workerContextTerminated(m_scriptExecutionContext.get(), this);

    if (m_mayBeDestroyed)
        delete this;   // HERE
}

Who's the primary care taker of this worker stuff? Is there anybody with that role?

### mi...@chromium.org (2013-02-25)

So WebCore::Worker has a raw pointer to the WebWorkerClientImpl  and so does WorkerFileWriterCallbacksBridge. WebCore::Worker looks all setup to ensure it's raw pointer remains valid so long as it is still around. But looks like WorkerFileWriterCallbacksBridge can outlive the WebCore::Worker and the WebWorkerClientImp.

### th...@gmail.com (2013-03-08)

There seems to be a pattern here. The crash addresses I have do not seem to be completely random (c#2). Also, I do seem to be having some (???) control over them by varying the array size of the HTML file name.


### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-03-19)

[Empty comment from Monorail migration]

### [Deleted User] (2013-03-21)

Bulk Edit

### [Deleted User] (2013-03-21)

Bulk edit

### [Deleted User] (2013-03-21)

Bulk edit

### in...@chromium.org (2013-04-03)

M26 has sailed. Moving all m25 bugs to m26.

### me...@google.com (2013-04-16)

Friendly ping :) Do we have any progress on this bug?

### mi...@chromium.org (2013-04-16)

No progress / no update.

I'm not actively looking into this atm, nobody is. @meacer, since you asked, do you have any interest in poking at it?

### [Deleted User] (2013-04-16)

bulk edit

### js...@chromium.org (2013-04-16)

Hm... that's very bad. As a project we have a hard deadline of under 60 days to fix high-severity bugs. Given that we've already exceeded that deadline, could you prioritize this higher, or find someone else familiar with the code to do so?

### sc...@gmail.com (2013-04-17)

If the feature does not have an active Chrome / Blink maintainer, perhaps it's not ready to be turned on?

### mi...@chromium.org (2013-04-17)

This is a worker/filesytem integration issue, filesystem does have active maintainers workers really don't afaict. Individuals maintaining other things trip thru the worker logic from time to time to resolve bugs... but there are no 'worker guys' afaict to collaborate with on resolving these things in an orderly way.

I'm under the impression that worker'isms are the source of a lot of 'security restricted' bugs. Would it make sense for the security team to cultivate some expertise about the worker infrastructure/impl to fill in that gap of "no worker guys to be found"?

### me...@google.com (2013-04-17)

FWIW, I'm looking at this but I'm not familiar with this code at all, so I wouldn't expect a quick resolution anytime soon.

### me...@chromium.org (2013-04-18)

This is a use after free. @michaeln, your analysis is mostly correct, but WorkerMessagingProxy::workerContextDestroyedInternal is called from 

WorkerContextDestroyedTask::performTask

rather than

WorkerMessagingProxy::workerObjectDestroyedInternal as you suggested. Here is the stack trace from ASAN:

=================================================================
==27650== ERROR: AddressSanitizer: heap-use-after-free on address 0x6018001b3d10 at pc 0x7f3c9c2e96c8 bp 0x7fff1ac75130 sp 0x7fff1ac75128
READ of size 8 at 0x6018001b3d10 thread T0 (chrome)
    #0 0x7f3c9c2e96c7 in WebKit::WorkerFileWriterCallbacksBridge::dispatchTaskToWorkerThread(WTF::PassOwnPtr<WebCore::ScriptExecutionContext::Task>) src/out/Debug/../../third_party/WebKit/Source/WebKit/chromium/src/WorkerFileWriterCallbacksBridge.cpp:208
    #1 0x7f3c9c2ea2d9 in WebKit::WorkerFileWriterCallbacksBridge::didFail(WebKit::WebFileError) src/out/Debug/../../third_party/WebKit/Source/WebKit/chromium/src/WorkerFileWriterCallbacksBridge.cpp:120
    #2 0x7f3c9c2eaa2f in non-virtual thunk to WebKit::WorkerFileWriterCallbacksBridge::didFail(WebKit::WebFileError) src/out/Debug/../../third_party/WebKit/Source/WebKit/chromium/src/WorkerFileWriterCallbacksBridge.cpp:121
    #3 0x7f3cb508dae4 in fileapi::WebFileWriterBase::FinishCancel() src/out/Debug/../../webkit/fileapi/webfilewriter_base.cc:154
    #4 0x7f3cb508d29b in fileapi::WebFileWriterBase::DidSucceed() src/out/Debug/../../webkit/fileapi/webfilewriter_base.cc:89
    #5 0x7f3cac4690f9 in content::WebFileWriterImpl::CallbackDispatcher::DidSucceed() src/out/Debug/../../content/common/fileapi/webfilewriter_impl.cc:47
    #6 0x7f3cac42f487 in content::FileSystemDispatcher::OnDidSucceed(int) src/out/Debug/../../content/common/fileapi/file_system_dispatcher.cc:297
    #7 0x7f3cac44c6d9 in void DispatchToMethod<content::FileSystemDispatcher, void (content::FileSystemDispatcher::*)(int), int>(content::FileSystemDispatcher*, void (content::FileSystemDispatcher::*)(int), Tuple1<int> const&) src/out/Debug/../../base/tuple.h:546
    #8 0x7f3cac43b3d0 in bool FileSystemMsg_DidSucceed::Dispatch<content::FileSystemDispatcher, content::FileSystemDispatcher, void (content::FileSystemDispatcher::*)(int)>(IPC::Message const*, content::FileSystemDispatcher*, content::FileSystemDispatcher*, void (content::FileSystemDispatcher::*)(int)) src/out/Debug/../../content/common/fileapi/file_system_messages.h:34
    #9 0x7f3cac42d8dc in content::FileSystemDispatcher::OnMessageReceived(IPC::Message const&) src/out/Debug/../../content/common/fileapi/file_system_dispatcher.cc:33
    #10 0x7f3cabd0f2cb in content::ChildThread::OnMessageReceived(IPC::Message const&) src/out/Debug/../../content/common/child_thread.cc:245
    #11 0x7f3c9a0c7bb2 in IPC::ChannelProxy::Context::OnDispatchMessage(IPC::Message const&) src/out/Debug/../../ipc/ipc_channel_proxy.cc:261
    #12 0x7f3c9a0ef0bd in base::internal::RunnableAdapter<void (IPC::ChannelProxy::Context::*)(IPC::Message const&)>::Run(IPC::ChannelProxy::Context*, IPC::Message const&) src/out/Debug/../../base/bind_internal.h:190
    #13 0x7f3c9a0eec5f in base::internal::InvokeHelper<false, void, base::internal::RunnableAdapter<void (IPC::ChannelProxy::Context::*)(IPC::Message const&)>, void (IPC::ChannelProxy::Context* const&, IPC::Message const&)>::MakeItSo(base::internal::RunnableAdapter<void (IPC::ChannelProxy::Context::*)(IPC::Message const&)>, IPC::ChannelProxy::Context* const&, IPC::Message const&) src/out/Debug/../../base/bind_internal.h:899
    #14 0x7f3c9a0ee889 in base::internal::Invoker<2, base::internal::BindState<base::internal::RunnableAdapter<void (IPC::ChannelProxy::Context::*)(IPC::Message const&)>, void (IPC::ChannelProxy::Context*, IPC::Message const&), void (IPC::ChannelProxy::Context*, IPC::Message)>, void (IPC::ChannelProxy::Context*, IPC::Message const&)>::Run(base::internal::BindStateBase*) src/out/Debug/../../base/bind_internal.h:1257
    #15 0x7f3c94a577db in base::Callback<void ()>::Run() const src/out/Debug/../../base/callback.h:396
    #16 0x7f3c9e3997d3 in base::MessageLoop::RunTask(base::PendingTask const&) src/out/Debug/../../base/message_loop.cc:474
    #17 0x7f3c9e39b193 in base::MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) src/out/Debug/../../base/message_loop.cc:486
    #18 0x7f3c9e39b83c in base::MessageLoop::DoWork() src/out/Debug/../../base/message_loop.cc:669
    #19 0x7f3c9e3e854e in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) src/out/Debug/../../base/message_pump_default.cc:29
    #20 0x7f3c9e397ed9 in base::MessageLoop::RunInternal() src/out/Debug/../../base/message_loop.cc:431
    #21 0x7f3c9e39799f in base::MessageLoop::RunHandler() src/out/Debug/../../base/message_loop.cc:404
    #22 0x7f3c9e4f2122 in base::RunLoop::Run() src/out/Debug/../../base/run_loop.cc:45
    #23 0x7f3c9e39562a in base::MessageLoop::Run() src/out/Debug/../../base/message_loop.cc:311
    #24 0x7f3cbea5e717 in content::RendererMain(content::MainFunctionParams const&) src/out/Debug/../../content/renderer/renderer_main.cc:226
    #25 0x7f3cb315a56b in content::RunZygote(content::MainFunctionParams const&, content::ContentMainDelegate*) src/out/Debug/../../content/app/content_main_runner.cc:383
    #26 0x7f3cb315b58c in content::RunNamedProcessTypeMain(std::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, content::MainFunctionParams const&, content::ContentMainDelegate*) src/out/Debug/../../content/app/content_main_runner.cc:439
    #27 0x7f3cb31609bf in content::ContentMainRunnerImpl::Run() src/out/Debug/../../content/app/content_main_runner.cc:736
    #28 0x7f3cb3157323 in content::ContentMain(int, char const**, content::ContentMainDelegate*) src/out/Debug/../../content/app/content_main.cc:35
    #29 0x7f3c9464e7bb in ChromeMain src/out/Debug/../../chrome/app/chrome_main.cc:32
    #30 0x7f3c9464e496 in main src/out/Debug/../../chrome/app/chrome_exe_main_gtk.cc:34
    #31 0x7f3c8a82e76c in __libc_start_main /build/buildd/eglibc-2.15/csu/libc-start.c:226
    #32 0x7f3c9464e184 in _start ??:0
0x6018001b3d10 is located 16 bytes inside of 120-byte region [0x6018001b3d00,0x6018001b3d78)
freed by thread T0 (chrome) here:
    #0 0x7f3c94642362 in free ??:0
    #1 0x7f3cbc341d66 in WTF::fastFree(void*) src/out/Debug/../../third_party/WebKit/Source/WTF/wtf/FastMalloc.cpp:340
    #2 0x7f3c9bf27521 in WebCore::WorkerMessagingProxy::operator delete(void*) src/out/Debug/../../third_party/WebKit/Source/WebCore/workers/WorkerMessagingProxy.h:48
    #3 0x7f3c9bf26602 in ~WebWorkerClientImpl src/out/Debug/../../third_party/WebKit/Source/WebKit/chromium/src/WebWorkerClientImpl.cpp:159
    #4 0x7f3ca7b14a3d in WebCore::WorkerMessagingProxy::workerContextDestroyedInternal() src/out/Debug/../../third_party/WebKit/Source/WebCore/workers/WorkerMessagingProxy.cpp:428
    #5 0x7f3ca7b3220c in WebCore::WorkerContextDestroyedTask::performTask(WebCore::ScriptExecutionContext*) src/out/Debug/../../third_party/WebKit/Source/WebCore/workers/WorkerMessagingProxy.cpp:163
    #6 0x7f3ca9a1256c in WebCore::Document::didReceiveTask(void*) src/out/Debug/../../third_party/WebKit/Source/WebCore/dom/Document.cpp:4730
    #7 0x7f3c9a554234 in base::internal::RunnableAdapter<void (*)(void*)>::Run(void* const&) src/out/Debug/../../base/bind_internal.h:171
    #8 0x7f3c9e1d9122 in base::internal::InvokeHelper<false, void, base::internal::RunnableAdapter<void (*)(void*)>, void (void* const&)>::MakeItSo(base::internal::RunnableAdapter<void (*)(void*)>, void* const&) src/out/Debug/../../base/bind_internal.h:871
    #9 0x7f3c9e1d8f93 in base::internal::Invoker<1, base::internal::BindState<base::internal::RunnableAdapter<void (*)(void*)>, void (void*), void (void*)>, void (void*)>::Run(base::internal::BindStateBase*) src/out/Debug/../../base/bind_internal.h:1173
    #10 0x7f3c94a577db in base::Callback<void ()>::Run() const src/out/Debug/../../base/callback.h:396
    #11 0x7f3c9e3997d3 in base::MessageLoop::RunTask(base::PendingTask const&) src/out/Debug/../../base/message_loop.cc:474
    #12 0x7f3c9e39b193 in base::MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) src/out/Debug/../../base/message_loop.cc:486
    #13 0x7f3c9e39b83c in base::MessageLoop::DoWork() src/out/Debug/../../base/message_loop.cc:669
    #14 0x7f3c9e3e854e in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) src/out/Debug/../../base/message_pump_default.cc:29
    #15 0x7f3c9e397ed9 in base::MessageLoop::RunInternal() src/out/Debug/../../base/message_loop.cc:431
    #16 0x7f3c9e39799f in base::MessageLoop::RunHandler() src/out/Debug/../../base/message_loop.cc:404
    #17 0x7f3c9e4f2122 in base::RunLoop::Run() src/out/Debug/../../base/run_loop.cc:45
    #18 0x7f3c9e39562a in base::MessageLoop::Run() src/out/Debug/../../base/message_loop.cc:311
    #19 0x7f3cbea5e717 in content::RendererMain(content::MainFunctionParams const&) src/out/Debug/../../content/renderer/renderer_main.cc:226
    #20 0x7f3cb315a56b in content::RunZygote(content::MainFunctionParams const&, content::ContentMainDelegate*) src/out/Debug/../../content/app/content_main_runner.cc:383
    #21 0x7f3cb315b58c in content::RunNamedProcessTypeMain(std::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, content::MainFunctionParams const&, content::ContentMainDelegate*) src/out/Debug/../../content/app/content_main_runner.cc:439
    #22 0x7f3cb31609bf in content::ContentMainRunnerImpl::Run() src/out/Debug/../../content/app/content_main_runner.cc:736
    #23 0x7f3cb3157323 in content::ContentMain(int, char const**, content::ContentMainDelegate*) src/out/Debug/../../content/app/content_main.cc:35
    #24 0x7f3c9464e7bb in ChromeMain src/out/Debug/../../chrome/app/chrome_main.cc:32
    #25 0x7f3c9464e496 in main src/out/Debug/../../chrome/app/chrome_exe_main_gtk.cc:34
    #26 0x7f3c8a82e76c in __libc_start_main /build/buildd/eglibc-2.15/csu/libc-start.c:226
previously allocated by thread T0 (chrome) here:
    #0 0x7f3c94642442 in malloc ??:0
    #1 0x7f3cbc340a69 in WTF::fastMalloc(unsigned long) src/out/Debug/../../third_party/WebKit/Source/WTF/wtf/FastMalloc.cpp:280
    #2 0x7f3c9bf26db3 in WebCore::WorkerMessagingProxy::operator new(unsigned long) src/out/Debug/../../third_party/WebKit/Source/WebCore/workers/WorkerMessagingProxy.h:48
    #3 0x7f3c9bf22b27 in WebKit::WebWorkerClientImpl::createWorkerContextProxy(WebCore::Worker*) src/out/Debug/../../third_party/WebKit/Source/WebKit/chromium/src/WebWorkerClientImpl.cpp:78
    #4 0x7f3ca7b74063 in WebCore::WorkerContextProxy::create(WebCore::Worker*) src/out/Debug/../../third_party/WebKit/Source/WebCore/workers/chromium/WorkerContextProxyChromium.cpp:46
    #5 0x7f3cc03c0010 in Worker src/out/Debug/../../third_party/WebKit/Source/WebCore/workers/Worker.cpp:54
    #6 0x7f3cc03be5cc in Worker src/out/Debug/../../third_party/WebKit/Source/WebCore/workers/Worker.cpp:56
    #7 0x7f3cc03bb5a4 in WebCore::Worker::create(WebCore::ScriptExecutionContext*, WTF::String const&, int&) src/out/Debug/../../third_party/WebKit/Source/WebCore/workers/Worker.cpp:63
    #8 0x7f3cadfe8a5c in WebCore::WorkerV8Internal::constructor(v8::Arguments const&) src/out/Debug/gen/webcore/bindings/V8Worker.cpp:128
    #9 0x7f3cadfe6d34 in WebCore::V8Worker::constructorCallback(v8::Arguments const&) src/out/Debug/gen/webcore/bindings/V8Worker.cpp:159
    #10 0x7f3cb7aec806 in v8::internal::MaybeObject* v8::internal::HandleApiCallHelper<true>(v8::internal::(anonymous namespace)::BuiltinArguments<(v8::internal::BuiltinExtraArguments)1>, v8::internal::Isolate*) src/out/Debug/../../v8/src/builtins.cc:1327
    #11 0x7f3cb7aeae1a in v8::internal::Builtin_Impl_HandleApiCallConstruct(v8::internal::(anonymous namespace)::BuiltinArguments<(v8::internal::BuiltinExtraArguments)1>, v8::internal::Isolate*) src/out/Debug/../../v8/src/builtins.cc:1350
    #12 0x7f3cb7ac5094 in v8::internal::Builtin_HandleApiCallConstruct(v8::internal::(anonymous namespace)::BuiltinArguments<(v8::internal::BuiltinExtraArguments)1>, v8::internal::Isolate*) src/out/Debug/../../v8/src/builtins.cc:1349
    #13 0x3eee99e0654d
    #14 0x3eee99e26050
    #15 0x3eee99e460a1
    #16 0x3eee99e26163
    #17 0x3eee99e0c336
    #13 0x7f3cb7d9b0db in v8::internal::Invoke(bool, v8::internal::Handle<v8::internal::JSFunction>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*, bool*) src/out/Debug/../../v8/src/execution.cc:118
    #14 0x7f3cb7d98b90 in v8::internal::Execution::Call(v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*, bool*, bool) src/out/Debug/../../v8/src/execution.cc:181
    #15 0x7f3cb78a601b in v8::Script::Run() src/out/Debug/../../v8/src/api.cc:1815
    #16 0x7f3cb0dfcf1f in WebCore::ScriptRunner::runCompiledScript(v8::Handle<v8::Script>, WebCore::ScriptExecutionContext*) src/out/Debug/../../third_party/WebKit/Source/bindings/v8/ScriptRunner.cpp:52
    #17 0x7f3cb0cfa22f in WebCore::ScriptController::compileAndRunScript(WebCore::ScriptSourceCode const&) src/out/Debug/../../third_party/WebKit/Source/bindings/v8/ScriptController.cpp:278
    #18 0x7f3cb0cfbada in WebCore::ScriptController::evaluate(WebCore::ScriptSourceCode const&) src/out/Debug/../../third_party/WebKit/Source/bindings/v8/ScriptController.cpp:302
    #19 0x7f3caa011b60 in WebCore::ScriptElement::executeScript(WebCore::ScriptSourceCode const&) src/out/Debug/../../third_party/WebKit/Source/WebCore/dom/ScriptElement.cpp:310
    #20 0x7f3caa00d21e in WebCore::ScriptElement::prepareScript(WTF::TextPosition const&, WebCore::ScriptElement::LegacyTypeSupport) src/out/Debug/../../third_party/WebKit/Source/WebCore/dom/ScriptElement.cpp:243
    #21 0x7f3c9f409aa0 in WebCore::HTMLScriptRunner::runScript(WebCore::Element*, WTF::TextPosition const&) src/out/Debug/../../third_party/WebKit/Source/WebCore/html/parser/HTMLScriptRunner.cpp:310
    #22 0x7f3c9f409174 in WebCore::HTMLScriptRunner::execute(WTF::PassRefPtr<WebCore::Element>, WTF::TextPosition const&) src/out/Debug/../../third_party/WebKit/Source/WebCore/html/parser/HTMLScriptRunner.cpp:179
    #23 0x7f3c9f358235 in WebCore::HTMLDocumentParser::runScriptsForPausedTreeBuilder() src/out/Debug/../../third_party/WebKit/Source/WebCore/html/parser/HTMLDocumentParser.cpp:273
    #24 0x7f3c9f35b9ba in WebCore::HTMLDocumentParser::processParsedChunkFromBackgroundParser(WTF::PassOwnPtr<WebCore::HTMLDocumentParser::ParsedChunk>) src/out/Debug/../../third_party/WebKit/Source/WebCore/html/parser/HTMLDocumentParser.cpp:445
Shadow bytes around the buggy address:
  0x0c038002e750: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd
  0x0c038002e760: fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa
  0x0c038002e770: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c038002e780: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd
  0x0c038002e790: fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa
=>0x0c038002e7a0: fd fd[fd]fd fd fd fd fd fd fd fd fd fd fd fd fa
  0x0c038002e7b0: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd
  0x0c038002e7c0: fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa
  0x0c038002e7d0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fa
  0x0c038002e7e0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c038002e7f0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07
  Heap left redzone:     fa
  Heap righ redzone:     fb
  Freed Heap region:     fd
  Stack left redzone:    f1
  Stack mid redzone:     f2
  Stack right redzone:   f3
  Stack partial redzone: f4
  Stack after return:    f5
  Stack use after scope: f8
  Global redzone:        f9
  Global init order:     f6
  Poisoned by user:      f7
  ASan internal:         fe
==27650== ABORTING


### me...@chromium.org (2013-04-23)

Patch: https://codereview.chromium.org/14271015

### me...@chromium.org (2013-04-23)

[Empty comment from Monorail migration]

### me...@google.com (2013-04-26)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-05-01)

------------------------------------------------------------------------
r149494 | meacer@chromium.org | 2013-05-01T00:29:49.842249Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/WebKit/chromium/src/WorkerFileWriterCallbacksBridge.cpp?r1=149494&r2=149493&pathrev=149494
   M http://src.chromium.org/viewvc/blink/trunk/Source/WebKit/chromium/src/WorkerFileWriterCallbacksBridge.h?r1=149494&r2=149493&pathrev=149494

Fix crash in WorkerFileWriterCallbacksBridge.

The bridge outlives the proxy. This fix clears the proxy when the
bridge is notified to stop.

BUG=176692

Review URL: https://chromiumcodereview.appspot.com/14271015
------------------------------------------------------------------------

### me...@chromium.org (2013-05-01)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-05-01)

Mustafa, just a fyi, security bugs have blanket merge approval. Please use Merge-Approved directly.

### sc...@gmail.com (2013-05-03)

@therealholden: thanks for your help getting to the bottom of this crash!
$1000 Chromium Security Reward.

### th...@gmail.com (2013-05-03)

Thanks!

### sc...@gmail.com (2013-05-06)

M27 is https://src.chromium.org/viewvc/blink?view=rev&revision=149742

### sc...@gmail.com (2013-05-17)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-05-28)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-06-24)

[Empty comment from Monorail migration]

### js...@chromium.org (2013-11-18)

Bulk release of old security bug reports.


### sh...@chromium.org (2016-06-14)

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

This issue was migrated from crbug.com/chromium/176692?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40076990)*
