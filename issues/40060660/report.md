# Security: UAF in content::CrOSSystemTracingSession::StartTracingCallbackProxy (browser process)

| Field | Value |
|-------|-------|
| **Issue ID** | [40060660](https://issues.chromium.org/issues/40060660) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Speed>Tracing |
| **Platforms** | ChromeOS |
| **Reporter** | 0x...@gmail.com |
| **Assignee** | kh...@google.com |
| **Created** | 2022-08-23 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**  

heap-use-after-free in content::CrOSSystemTracingSession::StartTracingCallbackProxy

**VERSION**  

Chrome Version: 107.0.5257.0 (Developer Build) (64-bit)  

Operating System: ChromiumOS

**REPRODUCTION CASE**

Download the latest chromiumOS build:  

gs://chromium-browser-asan/linux-release-chromeos/asan-linux-release-1038230.zip

Run the extension:  

./chrome --no-sandbox --use-system-clipboard --ash-host-window-bounds="3840x2160\*1.5" --load-extension="extension\_path" --user-data-dir=/tmp/any

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: [browser]

# Asan log:

==2882352==ERROR: AddressSanitizer: heap-use-after-free on address 0x6020007aa990 at pc 0x55cd967cc970 bp 0x7ffd28f54010 sp 0x7ffd28f54008  

WRITE of size 1 at 0x6020007aa990 thread T0 (chrome)  

==2882352==WARNING: invalid path to external symbolizer!  

==2882352==WARNING: Failed to use and restart external symbolizer!  

#0 0x55cd967cc96f in content::CrOSSystemTracingSession::StartTracingCallbackProxy(base::OnceCallback<void (bool)>, std::Cr::basic\_string<char, std::Cr::char\_traits<char>, std::Cr::allocator<char> > const&, bool) ./../../content/browser/tracing/cros\_tracing\_agent.cc:80:17  

#1 0x55cd967ccc98 in void base::internal::FunctorTraits<void (content::CrOSSystemTracingSession::\*)(base::OnceCallback<void (bool)>, std::Cr::basic\_string<char, std::Cr::char\_traits<char>, std::Cr::allocator<char> > const&, bool), void>::Invoke<void (content::CrOSSystemTracingSession::\*)(base::OnceCallback<void (bool)>, std::Cr::basic\_string<char, std::Cr::char\_traits<char>, std::Cr::allocator<char> > const&, bool), content::CrOSSystemTracingSession\*, base::OnceCallback<void (bool)>, std::Cr::basic\_string<char, std::Cr::char\_traits<char>, std::Cr::allocator<char> > const&, bool>(void (content::CrOSSystemTracingSession::\*)(base::OnceCallback<void (bool)>, std::Cr::basic\_string<char, std::Cr::char\_traits<char>, std::Cr::allocator<char> > const&, bool), content::CrOSSystemTracingSession\*&&, base::OnceCallback<void (bool)>&&, std::Cr::basic\_string<char, std::Cr::char\_traits<char>, std::Cr::allocator<char> > const&, bool&&) ./../../base/bind\_internal.h:608:12  

#2 0x55cd967ccad4 in MakeItSo<void (content::CrOSSystemTracingSession::\*)(base::OnceCallback<void (bool)>, const std::Cr::basic\_string<char, std::Cr::char\_traits<char>, std::Cr::allocator<char> > &, bool), content::CrOSSystemTracingSession \*, base::OnceCallback<void (bool)>, const std::Cr::basic\_string<char, std::Cr::char\_traits<char>, std::Cr::allocator<char> > &, bool> ./../../base/bind\_internal.h:777:12  

#3 0x55cd967ccad4 in RunImpl<void (content::CrOSSystemTracingSession::\*)(base::OnceCallback<void (bool)>, const std::Cr::basic\_string<char, std::Cr::char\_traits<char>, std::Cr::allocator<char> > &, bool), std::Cr::tuple<base::internal::UnretainedWrapper[content::CrOSSystemTracingSession](javascript:void(0);), base::OnceCallback<void (bool)> >, 0UL, 1UL> ./../../base/bind\_internal.h:850:12  

#4 0x55cd967ccad4 in base::internal::Invoker<base::internal::BindState<void (content::CrOSSystemTracingSession::\*)(base::OnceCallback<void (bool)>, std::Cr::basic\_string<char, std::Cr::char\_traits<char>, std::Cr::allocator<char> > const&, bool), base::internal::UnretainedWrapper[content::CrOSSystemTracingSession](javascript:void(0);), base::OnceCallback<void (bool)> >, void (std::Cr::basic\_string<char, std::Cr::char\_traits<char>, std::Cr::allocator<char> > const&, bool)>::RunOnce(base::internal::BindStateBase\*, std::Cr::basic\_string<char, std::Cr::char\_traits<char>, std::Cr::allocator<char> > const&, bool) ./../../base/bind\_internal.h:819:12  

#5 0x55cda422d4e1 in Run ./../../base/callback.h:145:12  

#6 0x55cda422d4e1 in Invoke<base::OnceCallback<void (const std::Cr::basic\_string<char, std::Cr::char\_traits<char>, std::Cr::allocator<char> > &, bool)>, std::Cr::basic\_string<char, std::Cr::char\_traits<char>, std::Cr::allocator<char> >, bool> ./../../base/bind\_internal.h:711:49  

#7 0x55cda422d4e1 in MakeItSo<base::OnceCallback<void (const std::Cr::basic\_string<char, std::Cr::char\_traits<char>, std::Cr::allocator<char> > &, bool)>, std::Cr::basic\_string<char, std::Cr::char\_traits<char>, std::Cr::allocator<char> >, bool> ./../../base/bind\_internal.h:777:12  

#8 0x55cda422d4e1 in RunImpl<base::OnceCallback<void (const std::Cr::basic\_string<char, std::Cr::char\_traits<char>, std::Cr::allocator<char> > &, bool)>, std::Cr::tuple<std::Cr::basic\_string<char, std::Cr::char\_traits<char>, std::Cr::allocator<char> >, bool>, 0UL, 1UL> ./../../base/bind\_internal.h:850:12  

#9 0x55cda422d4e1 in base::internal::Invoker<base::internal::BindState<base::OnceCallback<void (std::Cr::basic\_string<char, std::Cr::char\_traits<char>, std::Cr::allocator<char> > const&, bool)>, std::Cr::basic\_string<char, std::Cr::char\_traits<char>, std::Cr::allocator<char> >, bool>, void ()>::RunOnce(base::internal::BindStateBase\*) ./../../base/bind\_internal.h:819:12  

#10 0x55cd9f5a1dac in Run ./../../base/callback.h:145:12  

#11 0x55cd9f5a1dac in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task\_annotator.cc:135:32  

#12 0x55cd9f5e560a in RunTask<(lambda at ../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:426:29)> ./../../base/task/common/task\_annotator.h:74:5  

#13 0x55cd9f5e560a in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow\*) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:424:21  

#14 0x55cd9f5e48a2 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:294:41  

#15 0x55cd9f5e6634 in non-virtual thunk to base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:0:0  

#16 0x55cd9f6fb9e8 in base::MessagePumpLibevent::Run(base::MessagePump::Delegate\*) ./../../base/message\_loop/message\_pump\_libevent.cc:293:55  

#17 0x55cd9f5e70e5 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:577:12  

#18 0x55cd9f5353b3 in base::RunLoop::Run(base::Location const&) ./../../base/run\_loop.cc:141:14  

#19 0x55cd955b2f7c in content::BrowserMainLoop::RunMainMessageLoop() ./../../content/browser/browser\_main\_loop.cc:1042:18  

#20 0x55cd955b7d0b in content::BrowserMainRunnerImpl::Run() ./../../content/browser/browser\_main\_runner\_impl.cc:157:15  

#21 0x55cd955ad48a in content::BrowserMain(content::MainFunctionParams) ./../../content/browser/browser\_main.cc:30:28  

#22 0x55cd9f2f5f4e in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate\*) ./../../content/app/content\_main\_runner\_impl.cc:680:10  

#23 0x55cd9f2f85b1 in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) ./../../content/app/content\_main\_runner\_impl.cc:1207:10  

#24 0x55cd9f2f7fdb in content::ContentMainRunnerImpl::Run() ./../../content/app/content\_main\_runner\_impl.cc:1069:12  

#25 0x55cd9f2f24da in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner\*) ./../../content/app/content\_main.cc:433:36  

#26 0x55cd9f2f2b81 in content::ContentMain(content::ContentMainParams) ./../../content/app/content\_main.cc:461:10  

#27 0x55cd901ccb90 in ChromeMain ./../../chrome/app/chrome\_main.cc:182:12  

#28 0x7fe10c13b0b2 in \_\_libc\_start\_main /build/glibc-sMfBJT/glibc-2.31/csu/../csu/libc-start.c:308:16

0x6020007aa990 is located 0 bytes inside of 16-byte region [0x6020007aa990,0x6020007aa9a0)  

freed by thread T0 (chrome) here:  

#0 0x55cd901cac2d in operator delete(void\*) *asan\_rtl*:3  

#1 0x55cd967cea62 in operator() ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:51:5  

#2 0x55cd967cea62 in reset ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:308:7  

#3 0x55cd967cea62 in content::(anonymous namespace)::CrOSDataSource::OnTraceDataOnUI(base::OnceCallback<void ()>) ./../../content/browser/tracing/cros\_tracing\_agent.cc:223:14  

#4 0x55cd967cd2d4 in Invoke<void (content::(anonymous namespace)::CrOSDataSource::\*)(base::OnceCallback<void ()>), content::(anonymous namespace)::CrOSDataSource \*, base::OnceCallback<void ()> > ./../../base/bind\_internal.h:608:12  

#5 0x55cd967cd2d4 in MakeItSo<void (content::(anonymous namespace)::CrOSDataSource::\*)(base::OnceCallback<void ()>), content::(anonymous namespace)::CrOSDataSource \*, base::OnceCallback<void ()> > ./../../base/bind\_internal.h:777:12  

#6 0x55cd967cd2d4 in RunImpl<void (content::(anonymous namespace)::CrOSDataSource::\*)(base::OnceCallback<void ()>), std::Cr::tuple<base::internal::UnretainedWrapper<content::(anonymous namespace)::CrOSDataSource>, base::OnceCallback<void ()> >, 0UL, 1UL> ./../../base/bind\_internal.h:850:12  

#7 0x55cd967cd2d4 in base::internal::Invoker<base::internal::BindState<void (content::(anonymous namespace)::CrOSDataSource::\*)(base::OnceCallback<void ()>), base::internal::UnretainedWrapper<content::(anonymous namespace)::CrOSDataSource>, base::OnceCallback<void ()> >, void ()>::RunOnce(base::internal::BindStateBase\*) ./../../base/bind\_internal.h:819:12  

#8 0x55cd9f5a1dac in Run ./../../base/callback.h:145:12  

#9 0x55cd9f5a1dac in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task\_annotator.cc:135:32  

#10 0x55cd9f5e560a in RunTask<(lambda at ../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:426:29)> ./../../base/task/common/task\_annotator.h:74:5  

#11 0x55cd9f5e560a in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow\*) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:424:21  

#12 0x55cd9f5e48a2 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:294:41  

#13 0x55cd9f5e6634 in non-virtual thunk to base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:0:0  

#14 0x55cd9f6fb9e8 in base::MessagePumpLibevent::Run(base::MessagePump::Delegate\*) ./../../base/message\_loop/message\_pump\_libevent.cc:293:55  

#15 0x55cd9f5e70e5 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:577:12  

#16 0x55cd9f5353b3 in base::RunLoop::Run(base::Location const&) ./../../base/run\_loop.cc:141:14  

#17 0x55cd955b2f7c in content::BrowserMainLoop::RunMainMessageLoop() ./../../content/browser/browser\_main\_loop.cc:1042:18  

#18 0x55cd955b7d0b in content::BrowserMainRunnerImpl::Run() ./../../content/browser/browser\_main\_runner\_impl.cc:157:15  

#19 0x55cd955ad48a in content::BrowserMain(content::MainFunctionParams) ./../../content/browser/browser\_main.cc:30:28  

#20 0x55cd9f2f5f4e in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate\*) ./../../content/app/content\_main\_runner\_impl.cc:680:10  

#21 0x55cd9f2f85b1 in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) ./../../content/app/content\_main\_runner\_impl.cc:1207:10  

#22 0x55cd9f2f7fdb in content::ContentMainRunnerImpl::Run() ./../../content/app/content\_main\_runner\_impl.cc:1069:12  

#23 0x55cd9f2f24da in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner\*) ./../../content/app/content\_main.cc:433:36  

#24 0x55cd9f2f2b81 in content::ContentMain(content::ContentMainParams) ./../../content/app/content\_main.cc:461:10  

#25 0x55cd901ccb90 in ChromeMain ./../../chrome/app/chrome\_main.cc:182:12  

#26 0x7fe10c13b0b2 in \_\_libc\_start\_main /build/glibc-sMfBJT/glibc-2.31/csu/../csu/libc-start.c:308:16

previously allocated by thread T0 (chrome) here:  

#0 0x55cd901ca3cd in operator new(unsigned long) *asan\_rtl*:3  

#1 0x55cd967cbdad in make\_unique[content::CrOSSystemTracingSession](javascript:void(0);) ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:744:28  

#2 0x55cd967cbdad in content::(anonymous namespace)::CrOSDataSource::StartTracingOnUI(tracing::PerfettoProducer\*, perfetto::protos::gen::DataSourceConfig const&) ./../../content/browser/tracing/cros\_tracing\_agent.cc:162:16  

#3 0x55cd9f5a1dac in Run ./../../base/callback.h:145:12  

#4 0x55cd9f5a1dac in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task\_annotator.cc:135:32  

#5 0x55cd9f5e560a in RunTask<(lambda at ../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:426:29)> ./../../base/task/common/task\_annotator.h:74:5  

#6 0x55cd9f5e560a in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow\*) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:424:21  

#7 0x55cd9f5e48a2 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:294:41  

#8 0x55cd9f5e6634 in non-virtual thunk to base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:0:0  

#9 0x55cd9f6fb9e8 in base::MessagePumpLibevent::Run(base::MessagePump::Delegate\*) ./../../base/message\_loop/message\_pump\_libevent.cc:293:55  

#10 0x55cd9f5e70e5 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:577:12  

#11 0x55cd9f5353b3 in base::RunLoop::Run(base::Location const&) ./../../base/run\_loop.cc:141:14  

#12 0x55cd955b2f7c in content::BrowserMainLoop::RunMainMessageLoop() ./../../content/browser/browser\_main\_loop.cc:1042:18  

#13 0x55cd955b7d0b in content::BrowserMainRunnerImpl::Run() ./../../content/browser/browser\_main\_runner\_impl.cc:157:15  

#14 0x55cd955ad48a in content::BrowserMain(content::MainFunctionParams) ./../../content/browser/browser\_main.cc:30:28  

#15 0x55cd9f2f5f4e in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate\*) ./../../content/app/content\_main\_runner\_impl.cc:680:10  

#16 0x55cd9f2f85b1 in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) ./../../content/app/content\_main\_runner\_impl.cc:1207:10  

#17 0x55cd9f2f7fdb in content::ContentMainRunnerImpl::Run() ./../../content/app/content\_main\_runner\_impl.cc:1069:12  

#18 0x55cd9f2f24da in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner\*) ./../../content/app/content\_main.cc:433:36  

#19 0x55cd9f2f2b81 in content::ContentMain(content::ContentMainParams) ./../../content/app/content\_main.cc:461:10  

#20 0x55cd901ccb90 in ChromeMain ./../../chrome/app/chrome\_main.cc:182:12  

#21 0x7fe10c13b0b2 in \_\_libc\_start\_main /build/glibc-sMfBJT/glibc-2.31/csu/../csu/libc-start.c:308:16

SUMMARY: AddressSanitizer: heap-use-after-free (/home/cat/chromium\_version/asan-linux-release-1038230/chrome+0x138fc96f) (BuildId: 1c51846e2eed1d78)  

Shadow bytes around the buggy address:  

0x0c04800ed4e0: fa fa fd fa fa fa fd fa fa fa fd fa fa fa fd fa  

0x0c04800ed4f0: fa fa fd fd fa fa fd fd fa fa fd fa fa fa fd fa  

0x0c04800ed500: fa fa fd fa fa fa fd fa fa fa fd fa fa fa fd fa  

0x0c04800ed510: fa fa fd fa fa fa fd fa fa fa fd fa fa fa fd fd  

0x0c04800ed520: fa fa fd fd fa fa fd fa fa fa fd fa fa fa fd fa  

=>0x0c04800ed530: fa fa[fd]fd fa fa fd fa fa fa fd fa fa fa fd fa  

0x0c04800ed540: fa fa fd fa fa fa fd fa fa fa fd fa fa fa fd fa  

0x0c04800ed550: fa fa fd fa fa fa fd fd fa fa fd fa fa fa fd fa  

0x0c04800ed560: fa fa fd fa fa fa fd fa fa fa fd fa fa fa fd fa  

0x0c04800ed570: fa fa fd fa fa fa fd fd fa fa fd fa fa fa fd fa  

0x0c04800ed580: fa fa fd fa fa fa fd fa fa fa fd fa fa fa fd fd  

Shadow byte legend (one shadow byte represents 8 application bytes):  

Addressable: 00  

Partially addressable: 01 02 03 04 05 06 07  

Heap left redzone: fa  

Freed heap region: fd  

Stack left redzone: f1  

Stack mid redzone: f2  

Stack right redzone: f3  

Stack after return: f5  

Stack use after scope: f8  

Global redzone: f9  

Global init order: f6  

Poisoned by user: f7  

Container overflow: fc  

Array cookie: ac  

Intra object redzone: bb  

ASan internal: fe  

Left alloca redzone: ca  

Right alloca redzone: cb  

==2882352==ABORTING

## Attachments

- [extension.zip](attachments/extension.zip) (application/octet-stream, 1.9 KB)
- [asan.log](attachments/asan.log) (text/plain, 15.9 KB)
- [background.js](attachments/background.js) (text/plain, 1.7 KB)
- [manifest.json](attachments/manifest.json) (text/plain, 1.4 KB)

## Timeline

### [Deleted User] (2022-08-23)

[Empty comment from Monorail migration]

### es...@chromium.org (2022-08-23)

[Empty comment from Monorail migration]

### al...@google.com (2022-08-23)

[Empty comment from Monorail migration]

### al...@google.com (2022-08-23)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-23)

[Empty comment from Monorail migration]

### hi...@chromium.org (2022-08-24)

Looks like StartTracing is called twice in seqneuce?


### [Deleted User] (2022-08-24)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-08-24)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-08-24)

This ReleaseBlock issue's priority is being increased in accordance with go/cros-bug-slo-guidelines#release-blockers.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### es...@chromium.org (2022-08-24)

I'm not sure that's really what's happening. AFAICT, each time CrOSDataSource::StartTracingOnUI is called, a new |session_| object is created and StartTracing() called for it: https://source.chromium.org/chromium/chromium/src/+/main:content/browser/tracing/cros_tracing_agent.cc;drc=a0ee56858ce61af771b771c44874f992245d259b;l=163

This |session_| object is cleared in CrOSDataSource::OnTraceDataOnUI: https://source.chromium.org/chromium/chromium/src/+/main:content/browser/tracing/cros_tracing_agent.cc;drc=a0ee56858ce61af771b771c44874f992245d259b;l=223

So it seems that we've somehow gotten the callback for StartAgentTracing() after the callback for debug_daemon_->StopAgentTracing().

I wonder if that may be because we don't wait for the stop to fully complete, before starting the next session. The extension seems to call "Tracing.end, Tracing.start, Tracing.end, Tracing.start, ..." without waiting for the results of these calls. It's possible that Tracing.end() will not wait for tracing to be fully stopped before allowing new sessions.

AFAICT, Tracing.end resets the state here: https://source.chromium.org/chromium/chromium/src/+/main:content/browser/devtools/protocol/tracing_handler.cc;drc=a0ee56858ce61af771b771c44874f992245d259b;l=1079 without waiting for session_->DisableTracing() to complete. That means, Tracing.start can start a new session before the old one is teared down.

In theory, we also guard against starting a new session before tearing down the old one in the tracing service: https://source.chromium.org/chromium/chromium/src/+/main:services/tracing/perfetto/perfetto_service.cc;drc=a0ee56858ce61af771b771c44874f992245d259b;l=180

But when the tracing consumer disappears (TracingHandler resets its session_ when handling the next "Tracing.start" => consumer is gone), the tracing service skips waiting for producers to tear down their data source instances before acknowledging the session stop: https://source.chromium.org/chromium/chromium/src/+/main:third_party/perfetto/src/tracing/core/tracing_service_impl.cc;drc=a0ee56858ce61af771b771c44874f992245d259b;l=2398 ... which means we are able to start the next session, without waiting for the old session's data sources to stop.

We have a few ways to solve this -- the simplest one may be to modify TracingHandler not to start a new session before the old one has completed fully. Maybe we can simply move the reset of g_any_agent_tracing (g_any_agent_tracing = false) to happen only after |session_.reset()|.

Mika, do you have cycles to look into the latter?

[Monorail components: Speed>Tracing]

### kh...@google.com (2022-08-25)

[Empty comment from Monorail migration]

### kh...@google.com (2022-08-25)

I couldn't reproduce the original crash unfortunately, but I can confirm that it's possible to create a new session before the previous one is completely destroyed. The simple fix that Eric suggested solves this issue: crrev.com/c/3855415

### gi...@appspot.gserviceaccount.com (2022-08-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/a08980c4b696c46e151bf5426a08b583b597f2ad

commit a08980c4b696c46e151bf5426a08b583b597f2ad
Author: Mikhail Khokhlov <khokhlov@google.com>
Date: Tue Aug 30 17:49:23 2022

[Tracing] Fix concurrent session guard

Calling "Tracing.start" immediately after "Tracing.end" could sometimes
start a new session before the old one is destroyed. This CL makes sure
we never allow concurrent sessions.

Bug: 1355902
Change-Id: I7ee7d095213db1c7c5cc76b02129fb98c0124394
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3855415
Commit-Queue: Mikhail Khokhlov <khokhlov@google.com>
Reviewed-by: Eric Seckler <eseckler@chromium.org>
Reviewed-by: Andrey Kosyakov <caseq@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1041064}

[modify] https://crrev.com/a08980c4b696c46e151bf5426a08b583b597f2ad/content/browser/devtools/protocol/tracing_handler.cc


### kh...@google.com (2022-08-31)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-31)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-31)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-17)

Not requesting merge to dev (M107) because latest trunk commit (1041064) appears to be prior to dev branch point (1047731). If this is incorrect, please replace the Merge-NA-107 label with Merge-Request-107. If other changes are required to fix this bug completely, please request a merge if necessary.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aj...@google.com (2022-09-29)

Adding files for posterity.

### am...@google.com (2022-10-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-10-14)

Congratulations on another one, asnine! The VRP Panel has decided to award you $5,000 for this moderately mitigated security issue. Thank you for your efforts in finding and reporting this issue to us! 

### am...@google.com (2022-10-14)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-07)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-12-20)

Hello, we consider attachments/POCs included with reports to be an integral part of the report (https://g.co/chrome/vrp), so I've undeleted them.

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1355902?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060660)*
