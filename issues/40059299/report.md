# Security: heap-buffer-overflow on components/ui_devtools/views/devtools_server_util.cc

| Field | Value |
|-------|-------|
| **Issue ID** | [40059299](https://issues.chromium.org/issues/40059299) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Platform>DevTools |
| **Platforms** | Linux, Mac, Windows |
| **Reporter** | rh...@gmail.com |
| **Assignee** | lg...@chromium.org |
| **Created** | 2022-04-05 |
| **Bounty** | $2,000.00 |

## Description

**-------------------------**

**VULNERABILITY DETAILS**  

Similar with issue #1313574

**VERSION**  

Chrome Version: 102.0.4987.0 + dev  

Operating System: linux-chromeOS and Linux

**REPRODUCTION CASE**  

Option 1

1. Open browser and navigate to devtools://devtools/bundled/devtools\_app.html?uiDevTools=true&ws=localhost:9222/1 while issue # devtools://devtools/bundled/devtools\_app.html?uiDevTools=true&ws=localhost:9222/0

Option 2

1. Install plugin

# **FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**

==87795==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x60900171c448 at pc 0x561f90c3db40 bp 0x7fff53251ed0 sp 0x7fff53251ec8  

READ of size 8 at 0x60900171c448 thread T0 (chrome)  

SCARINESS: 23 (8-byte-read-heap-buffer-overflow)  

#0 0x561f90c3db3f in get buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:288:19  

#1 0x561f90c3db3f in ui\_devtools::UiDevToolsServer::OnWebSocketRequest(int, network::server::HttpServerRequestInfo const&) components/ui\_devtools/devtools\_server.cc:218:50  

#2 0x561f90c42f40 in network::server::HttpServer::HandleReadResult(network::server::HttpConnection\*, unsigned int) services/network/public/cpp/server/http\_server.cc:309:18  

#3 0x561f90c41ed0 in network::server::HttpServer::OnReadable(int, unsigned int, mojo::HandleSignalsState const&) services/network/public/cpp/server/http\_server.cc:257:3  

#4 0x561f90c464c3 in Invoke<void (network::server::HttpServer::\*)(int, unsigned int, const mojo::HandleSignalsState &), const base::WeakPtr[network::server::HttpServer](javascript:void(0);) &, const int &, unsigned int, const mojo::HandleSignalsState &> base/bind\_internal.h:542:12  

#5 0x561f90c464c3 in MakeItSo<void (network::server::HttpServer::\*const &)(int, unsigned int, const mojo::HandleSignalsState &), const base::WeakPtr[network::server::HttpServer](javascript:void(0);) &, const int &, unsigned int, const mojo::HandleSignalsState &> base/bind\_internal.h:726:5  

#6 0x561f90c464c3 in RunImpl<void (network::server::HttpServer::\*const &)(int, unsigned int, const mojo::HandleSignalsState &), const std::\_\_1::tuple<base::WeakPtr[network::server::HttpServer](javascript:void(0);), int> &, 0UL, 1UL> base/bind\_internal.h:779:12  

#7 0x561f90c464c3 in base::internal::Invoker<base::internal::BindState<void (network::server::HttpServer::\*)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr[network::server::HttpServer](javascript:void(0);), int>, void (unsigned int, mojo::HandleSignalsState const&)>::Run(base::internal::BindStateBase\*, unsigned int, mojo::HandleSignalsState const&) base/bind\_internal.h:761:12  

#8 0x561f894066d7 in Run base/callback.h:241:12  

#9 0x561f894066d7 in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, mojo::HandleSignalsState const&) mojo/public/cpp/system/simple\_watcher.cc:278:14  

#10 0x561f8940769f in Invoke<void (mojo::SimpleWatcher::\*)(int, unsigned int, const mojo::HandleSignalsState &), base::WeakPtr[mojo::SimpleWatcher](javascript:void(0);), int, unsigned int, mojo::HandleSignalsState> base/bind\_internal.h:542:12  

#11 0x561f8940769f in MakeItSo<void (mojo::SimpleWatcher::\*)(int, unsigned int, const mojo::HandleSignalsState &), base::WeakPtr[mojo::SimpleWatcher](javascript:void(0);), int, unsigned int, mojo::HandleSignalsState> base/bind\_internal.h:726:5  

#12 0x561f8940769f in RunImpl<void (mojo::SimpleWatcher::\*)(int, unsigned int, const mojo::HandleSignalsState &), std::\_\_1::tuple<base::WeakPtr[mojo::SimpleWatcher](javascript:void(0);), int, unsigned int, mojo::HandleSignalsState>, 0UL, 1UL, 2UL, 3UL> base/bind\_internal.h:779:12  

#13 0x561f8940769f in base::internal::Invoker<base::internal::BindState<void (mojo::SimpleWatcher::\*)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr[mojo::SimpleWatcher](javascript:void(0);), int, unsigned int, mojo::HandleSignalsState>, void ()>::RunOnce(base::internal::BindStateBase\*) base/bind\_internal.h:748:12  

#14 0x561f888adb93 in Run base/callback.h:142:12  

#15 0x561f888adb93 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/task/common/task\_annotator.cc:135:32  

#16 0x561f888efecd in RunTask<(lambda at ../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:388:29)> base/task/common/task\_annotator.h:74:5  

#17 0x561f888efecd in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence\_manager::LazyNow\*) base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:386:21  

#18 0x561f888ef5c4 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:291:41  

#19 0x561f888f0bb1 in non-virtual thunk to base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc  

#20 0x561f887a60c9 in HandleDispatch base/message\_loop/message\_pump\_glib.cc:375:46  

#21 0x561f887a60c9 in base::(anonymous namespace)::WorkSourceDispatch(\_GSource\*, int (\*)(void\*), void\*) base/message\_loop/message\_pump\_glib.cc:126:43  

#0 0x7f2e3cde517c in g\_main\_context\_dispatch ??:0:0

0x60900171c448 is located 0 bytes to the right of 8-byte region [0x60900171c440,0x60900171c448)  

allocated by thread T0 (chrome) here:  

#0 0x561f7990e91d in operator new(unsigned long) /b/s/w/ir/cache/builder/src/third\_party/llvm/compiler-rt/lib/asan/asan\_new\_delete.cpp:95:3  

#1 0x561f90c3e7c5 in \_\_libcpp\_operator\_new<unsigned long> buildtools/third\_party/libc++/trunk/include/new:235:10  

#2 0x561f90c3e7c5 in \_\_libcpp\_allocate buildtools/third\_party/libc++/trunk/include/new:261:10  

#3 0x561f90c3e7c5 in allocate buildtools/third\_party/libc++/trunk/include/\_\_memory/allocator.h:82:38  

#4 0x561f90c3e7c5 in allocate buildtools/third\_party/libc++/trunk/include/\_\_memory/allocator\_traits.h:261:20  

#5 0x561f90c3e7c5 in \_\_split\_buffer buildtools/third\_party/libc++/trunk/include/\_\_split\_buffer:314:29  

#6 0x561f90c3e7c5 in void std::\_\_1::vector<std::\_\_1::unique\_ptr<ui\_devtools::UiDevToolsClient, std::\_\_1::default\_delete<ui\_devtools::UiDevToolsClient> >, std::\_\_1::allocator<std::\_\_1::unique\_ptr<ui\_devtools::UiDevToolsClient, std::\_\_1::default\_delete<ui\_devtools::UiDevToolsClient> > > >::\_\_push\_back\_slow\_path<std::\_\_1::unique\_ptr<ui\_devtools::UiDevToolsClient, std::\_\_1::default\_delete<ui\_devtools::UiDevToolsClient> > >(std::\_\_1::unique\_ptr<ui\_devtools::UiDevToolsClient, std::\_\_1::default\_delete<ui\_devtools::UiDevToolsClient> >&&) buildtools/third\_party/libc++/trunk/include/vector:1625:49  

#7 0x561f90c3ce44 in push\_back buildtools/third\_party/libc++/trunk/include/vector:1657:9  

#8 0x561f90c3ce44 in ui\_devtools::UiDevToolsServer::AttachClient(std::\_\_1::unique\_ptr<ui\_devtools::UiDevToolsClient, std::\_\_1::default\_delete<ui\_devtools::UiDevToolsClient> >) components/ui\_devtools/devtools\_server.cc:161:12  

#9 0x561f826289b4 in ui\_devtools::CreateUiDevToolsServerForViews(network::mojom::NetworkContext\*, std::\_\_1::unique\_ptr<ui\_devtools::ConnectorDelegate, std::\_\_1::default\_delete<ui\_devtools::ConnectorDelegate> >, base::FilePath const&) components/ui\_devtools/views/devtools\_server\_util.cc:42:11  

#10 0x561f93b0d050 in ChromeBrowserMainExtraPartsViews::CreateUiDevTools() chrome/browser/ui/views/chrome\_browser\_main\_extra\_parts\_views.cc:197:22  

#11 0x561f93b0cc6d in ChromeBrowserMainExtraPartsViews::PreProfileInit() chrome/browser/ui/views/chrome\_browser\_main\_extra\_parts\_views.cc:121:5  

#12 0x561f8783534e in ChromeBrowserMainParts::PreProfileInit() chrome/browser/chrome\_browser\_main.cc:1168:24  

#13 0x561f883afe13 in ChromeBrowserMainPartsLinux::PreProfileInit() chrome/browser/chrome\_browser\_main\_linux.cc:103:32  

#14 0x561f878338f7 in ChromeBrowserMainParts::PreMainMessageLoopRunImpl() chrome/browser/chrome\_browser\_main.cc:1544:3  

#15 0x561f87832f04 in ChromeBrowserMainParts::PreMainMessageLoopRun() chrome/browser/chrome\_browser\_main.cc:1142:18  

#16 0x561f7ee959aa in content::BrowserMainLoop::PreMainMessageLoopRun() content/browser/browser\_main\_loop.cc:983:28  

#17 0x561f8005f008 in Run base/callback.h:142:12  

#18 0x561f8005f008 in content::StartupTaskRunner::RunAllTasksNow() content/browser/startup\_task\_runner.cc:43:29  

#19 0x561f7ee94f2d in content::BrowserMainLoop::CreateStartupTasks() content/browser/browser\_main\_loop.cc:894:25  

#20 0x561f7ee9bbb1 in content::BrowserMainRunnerImpl::Initialize(content::MainFunctionParams) content/browser/browser\_main\_runner\_impl.cc:134:15  

#21 0x561f7ee917ce in content::BrowserMain(content::MainFunctionParams) content/browser/browser\_main.cc:26:32  

#22 0x561f8764acc0 in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate\*) content/app/content\_main\_runner\_impl.cc:640:10  

#23 0x561f8764e1ec in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) content/app/content\_main\_runner\_impl.cc:1147:10  

#24 0x561f8764d517 in content::ContentMainRunnerImpl::Run() content/app/content\_main\_runner\_impl.cc:1019:12  

#25 0x561f87646d31 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner\*) content/app/content\_main.cc:407:36  

#26 0x561f8764745c in content::ContentMain(content::ContentMainParams) content/app/content\_main.cc:435:10  

#27 0x561f79911126 in ChromeMain chrome/app/chrome\_main.cc:176:12  

#28 0x7f2e3b89a0b2 in \_\_libc\_start\_main /build/glibc-sMfBJT/glibc-2.31/csu/../csu/libc-start.c:308:16

SUMMARY: AddressSanitizer: heap-buffer-overflow buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:288:19 in get  

Shadow bytes around the buggy address:  

0x0c12802db830: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c12802db840: 00 fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c12802db850: fa fa 00 fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c12802db860: fa fa fa fa 00 fa fa fa fa fa fa fa fa fa fa fa  

0x0c12802db870: fa fa fa fa fa fa 00 fa fa fa fa fa fa fa fa fa  

=>0x0c12802db880: fa fa fa fa fa fa fa fa 00[fa]fa fa fa fa fa fa  

0x0c12802db890: fa fa fa fa fa fa fa fa fa fa 00 00 fa fa fa fa  

0x0c12802db8a0: fa fa fa fa fa fa fa fa fa fa fa fa 04 fa fa fa  

0x0c12802db8b0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa 00 fa  

0x0c12802db8c0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c12802db8d0: 00 fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

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

==87795==ABORTING

## Attachments

- [background.js](attachments/background.js) (text/plain, 129 B)
- [manifest.json](attachments/manifest.json) (text/plain, 339 B)
- deleted (application/octet-stream, 0 B)
- [screencast_1313600.webm](attachments/screencast_1313600.webm) (video/webm, 2.3 MB)
- [bug-1313600.txt](attachments/bug-1313600.txt) (text/plain, 10.6 KB)

## Timeline

### [Deleted User] (2022-04-05)

[Empty comment from Monorail migration]

### rh...@gmail.com (2022-04-05)

Sorry missing arguments:
Needing --enable-ui-devtools=9222 enable.



### rh...@gmail.com (2022-04-05)

oops clarify the repro:

Option 1
1. Open browser and navigate to devtools://devtools/bundled/devtools_app.html?uiDevTools=true&ws=localhost:9222/1
while issue #1313574 "devtools://devtools/bundled/devtools_app.html?uiDevTools=true&ws=localhost:9222/0"

Option 2
1. Install plugin

### rs...@chromium.org (2022-04-06)

Thanks, I can confirm this. Steps that reproed for me are:

1. Launch with  --enable-ui-devtools=9222 
2. Navigate to devtools://devtools/bundled/devtools_app.html?uiDevTools=true&ws=localhost:9222/1

`connection_id` is not validated here before indexing the array: https://source.chromium.org/chromium/chromium/src/+/main:components/ui_devtools/devtools_server.cc;l=218;drc=729f2502700cbb51589fd7a2bff221663035293e

Because this requires the developer option --enable-ui-devtools, this is Low.

[Monorail components: Platform>DevTools]

### [Deleted User] (2022-04-06)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-04-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/2039b7264b8d1c653d4ef876aa1aa221fb98ad7e

commit 2039b7264b8d1c653d4ef876aa1aa221fb98ad7e
Author: Leonard Grey <lgrey@chromium.org>
Date: Mon Apr 11 22:52:50 2022

UIDevTools: Fix server test on Mac

(Though TBH I couldn't get it to pass locally on Linux either!)

Not *directly* related to https://crbug.com/1313600 but I want the
tests in good shape so that fix can have a test. This is in a separate
change for better revertability/granularity.

Bug: 1313600
Change-Id: I8d9e22312c9911b5470619f18603022f3b4c6a2d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3577365
Reviewed-by: Robert Sesek <rsesek@chromium.org>
Commit-Queue: Leonard Grey <lgrey@chromium.org>
Cr-Commit-Position: refs/heads/main@{#991248}

[modify] https://crrev.com/2039b7264b8d1c653d4ef876aa1aa221fb98ad7e/components/ui_devtools/devtools_server.cc
[modify] https://crrev.com/2039b7264b8d1c653d4ef876aa1aa221fb98ad7e/components/ui_devtools/devtools_server_unittest.cc
[modify] https://crrev.com/2039b7264b8d1c653d4ef876aa1aa221fb98ad7e/components/ui_devtools/devtools_server.h


### gi...@appspot.gserviceaccount.com (2022-04-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/6bbbdbf771fc7ff458724de4720154123b2dd019

commit 6bbbdbf771fc7ff458724de4720154123b2dd019
Author: Leonard Grey <lgrey@chromium.org>
Date: Tue Apr 12 23:14:06 2022

UIDevTools: fix bounds check for websocket connections

Bug: 1313600
Change-Id: Ic97da6e5cf5595d530a100bc8bbbee12467cef05
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3584284
Reviewed-by: Robert Sesek <rsesek@chromium.org>
Commit-Queue: Leonard Grey <lgrey@chromium.org>
Cr-Commit-Position: refs/heads/main@{#991786}

[modify] https://crrev.com/6bbbdbf771fc7ff458724de4720154123b2dd019/components/ui_devtools/devtools_server.cc
[modify] https://crrev.com/6bbbdbf771fc7ff458724de4720154123b2dd019/components/ui_devtools/devtools_server_unittest.cc


### lg...@chromium.org (2022-04-18)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-18)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-18)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-05-24)

[Empty comment from Monorail migration]

### am...@google.com (2022-05-24)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-21)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-25)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2022-07-27)

[Empty comment from Monorail migration]

### am...@google.com (2022-07-28)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-07-29)

Congratulations, Rheza! The VRP Panel has decided to award you $2,000 for this report. The reward amount decided up was based on this issue being significantly mitigated by not being remote exploitable, requiring developers option/ high amount of user interaction required, and requiring an extension to be installed. Thank you for your efforts and reporting this issue to us. 

### am...@chromium.org (2022-07-29)

[Empty comment from Monorail migration]

### am...@google.com (2022-07-29)

[Empty comment from Monorail migration]

### is...@google.com (2022-07-29)

This issue was migrated from crbug.com/chromium/1313600?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059299)*
