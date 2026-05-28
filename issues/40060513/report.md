# Security: heap-use-after-free ui/events/event_processor.cc:77:26 in ui::EventProcessor::OnEventFromSource(ui::Event*)

| Field | Value |
|-------|-------|
| **Issue ID** | [40060513](https://issues.chromium.org/issues/40060513) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Aura, OS>Inputs |
| **Platforms** | ChromeOS |
| **Reporter** | rh...@gmail.com |
| **Assignee** | os...@chromium.org |
| **Created** | 2022-08-05 |
| **Bounty** | $4,000.00 |

## Description

**VERSION**  

Chrome Version: Chromium 106.0.5221.0  

Operating System: linux-chromeOS

**REPRODUCTION CASE**  

On the real devices with touchscreen, to reproduce this issue it requires alt+tab. In the emulator linux-chromeOS it requires --ash-dev-shortcuts --force-tablet-mode=clamshell --touch-devices=<id\_of\_virtual\_mouse> --show-taps

(1) Open two browsers  

(2) alt+tab, hold alt+tab then drag mouse left side or right side and repeat.

# **FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**

==601599==ERROR: AddressSanitizer: heap-use-after-free on address 0x6060008d2900 at pc 0x55f1ded9ac08 bp 0x7ffc632ef9d0 sp 0x7ffc632ef9c8  

READ of size 8 at 0x6060008d2900 thread T0 (chrome)  

SCARINESS: 51 (8-byte-read-heap-use-after-free)  

#0 0x55f1ded9ac07 in ui::EventProcessor::OnEventFromSource(ui::Event\*) ui/events/event\_processor.cc:77:26  

#1 0x55f1dbcf0630 in ui::EventSource::DeliverEventToSink(ui::Event\*) ui/events/event\_source.cc:118:16  

#2 0x55f1dbcf0b28 in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const\*) ui/events/event\_source.cc:66:14  

#3 0x55f1dbcef243 in ui::EventRewriter::SendEvent(base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);), ui::Event const\*) ui/events/event\_rewriter.cc:88:39  

#4 0x55f1cee0593c in ui::EventRewriterChromeOS::RewriteTouchEvent(ui::TouchEvent const&, base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);)) ui/chromeos/events/event\_rewriter\_chromeos.cc:1315:12  

#5 0x55f1cee02ed2 in ui::EventRewriterChromeOS::RewriteEvent(ui::Event const&, base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);)) ui/chromeos/events/event\_rewriter\_chromeos.cc:767:12  

#6 0x55f1dbcf0ad8 in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const\*) ui/events/event\_source.cc:67:32  

#7 0x55f1dbcef243 in ui::EventRewriter::SendEvent(base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);), ui::Event const\*) ui/events/event\_rewriter.cc:88:39  

#8 0x55f1df4aa900 in ash::KeyboardDrivenEventRewriter::RewriteEvent(ui::Event const&, base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);)) ash/events/keyboard\_driven\_event\_rewriter.cc:31:12  

#9 0x55f1dbcf0ad8 in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const\*) ui/events/event\_source.cc:67:32  

#10 0x55f1dbcef243 in ui::EventRewriter::SendEvent(base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);), ui::Event const\*) ui/events/event\_rewriter.cc:88:39  

#11 0x55f1df4a6af6 in ash::AccessibilityEventRewriter::RewriteEvent(ui::Event const&, base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);)) ash/events/accessibility\_event\_rewriter.cc  

#12 0x55f1dbcf0ad8 in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const\*) ui/events/event\_source.cc:67:32  

#13 0x55f1dbcef243 in ui::EventRewriter::SendEvent(base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);), ui::Event const\*) ui/events/event\_rewriter.cc:88:39  

#14 0x55f1df274a1e in ash::AutoclickDragEventRewriter::RewriteEvent(ui::Event const&, base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);)) ash/accessibility/autoclick/autoclick\_drag\_event\_rewriter.cc  

#15 0x55f1dbcf0ad8 in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const\*) ui/events/event\_source.cc:67:32  

#16 0x55f1dbcef243 in ui::EventRewriter::SendEvent(base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);), ui::Event const\*) ui/events/event\_rewriter.cc:88:39  

#17 0x55f1df2826ca in ash::FullscreenMagnifierController::RewriteEvent(ui::Event const&, base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);)) ash/accessibility/magnifier/fullscreen\_magnifier\_controller.cc  

#18 0x55f1dbcf02d5 in ui::EventSource::SendEventToSinkFromRewriter(ui::Event const\*, ui::EventRewriter const\*) ui/events/event\_source.cc:144:29  

#19 0x55f1df4e0be1 in aura::WindowTreeHostPlatform::DispatchEvent(ui::Event\*) ui/aura/window\_tree\_host\_platform.cc:229:38  

#20 0x55f1df4e81e8 in ash::AshWindowTreeHostPlatform::DispatchEvent(ui::Event\*) ash/host/ash\_window\_tree\_host\_platform.cc:207:40  

#21 0x55f1dbcfad9f in Run base/callback.h:145:12  

#22 0x55f1dbcfad9f in ui::DispatchEventFromNativeUiEvent(ui::Event\* const&, base::OnceCallback<void (ui::Event\*)>) ui/events/ozone/events\_ozone.cc:40:25  

#23 0x55f1cbc48c2f in ui::X11Window::DispatchUiEvent(ui::Event\*, x11::Event const&) ui/ozone/platform/x11/x11\_window.cc:1362:3  

#24 0x55f1cbc48481 in ui::X11Window::DispatchEvent(ui::Event\* const&) ui/ozone/platform/x11/x11\_window.cc:1315:3  

#25 0x55f1cbc48f6a in non-virtual thunk to ui::X11Window::DispatchEvent(ui::Event\* const&) ui/ozone/platform/x11/x11\_window.cc  

#26 0x55f1dbc94ff1 in ui::PlatformEventSource::DispatchEvent(ui::Event\*) ui/events/platform/platform\_event\_source.cc:99:29  

#27 0x55f1dc3e7db3 in ui::X11EventSource::OnEvent(x11::Event const&) ui/events/platform/x11/x11\_event\_source.cc:287:5  

#28 0x55f1cb8697ad in x11::Connection::DispatchEvent(x11::Event const&) ui/gfx/x/connection.cc:457:14  

#29 0x55f1cb8694bb in x11::Connection::ProcessNextEvent() ui/gfx/x/connection.cc:508:3  

#30 0x55f1cb868f8b in x11::Connection::Dispatch() ui/gfx/x/connection.cc  

#31 0x55f1dc3f0cdb in ui::X11EventWatcherFdWatch::OnFileCanReadWithoutBlocking(int) ui/events/platform/x11/x11\_event\_watcher\_fdwatch.cc:64:15  

#32 0x55f1d9a65ac7 in base::MessagePumpLibevent::OnLibeventNotification(int, short, void\*) base/message\_loop/message\_pump\_libevent.cc  

#33 0x55f1d9d9942b in event\_process\_active third\_party/libevent/event.c:381:4  

#34 0x55f1d9d9942b in event\_base\_loop third\_party/libevent/event.c:521:4  

#35 0x55f1d9a66483 in base::MessagePumpLibevent::Run(base::MessagePump::Delegate\*) base/message\_loop/message\_pump\_libevent.cc:316:5  

#36 0x55f1d99543a5 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:581:12  

#37 0x55f1d98a1dae in base::RunLoop::Run(base::Location const&) base/run\_loop.cc:141:14  

#38 0x55f1cfb6aa2c in content::BrowserMainLoop::RunMainMessageLoop() content/browser/browser\_main\_loop.cc:1042:18  

#39 0x55f1cfb6f7bb in content::BrowserMainRunnerImpl::Run() content/browser/browser\_main\_runner\_impl.cc:157:15  

#40 0x55f1cfb64f3a in content::BrowserMain(content::MainFunctionParams) content/browser/browser\_main.cc:30:28  

#41 0x55f1d9662c5e in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate\*) content/app/content\_main\_runner\_impl.cc:678:10  

#42 0x55f1d96652c1 in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) content/app/content\_main\_runner\_impl.cc:1197:10  

#43 0x55f1d9664ceb in content::ContentMainRunnerImpl::Run() content/app/content\_main\_runner\_impl.cc:1062:12  

#44 0x55f1d965f1ea in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner\*) content/app/content\_main.cc:433:36  

#45 0x55f1d965f891 in content::ContentMain(content::ContentMainParams) content/app/content\_main.cc:461:10  

#46 0x55f1ca7f3bb0 in ChromeMain chrome/app/chrome\_main.cc:182:12  

#47 0x7fd72ab2c082 in \_\_libc\_start\_main /build/glibc-SzIz7B/glibc-2.31/csu/../csu/libc-start.c:308:16

0x6060008d2900 is located 0 bytes inside of 56-byte region [0x6060008d2900,0x6060008d2938)  

freed by thread T0 (chrome) here:  

#0 0x55f1ca7f1c4d in operator delete(void\*) /b/s/w/ir/cache/builder/src/third\_party/llvm/compiler-rt/lib/asan/asan\_new\_delete.cpp:152:3  

#1 0x55f1df67e598 in operator() buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:48:5  

#2 0x55f1df67e598 in reset buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:305:7  

#3 0x55f1df67e598 in ~unique\_ptr buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:259:19  

#4 0x55f1df67e598 in aura::ScopedWindowTargeter::~ScopedWindowTargeter() ui/aura/scoped\_window\_targeter.cc:25:5  

#5 0x55f1df67e647 in aura::ScopedWindowTargeter::~ScopedWindowTargeter() ui/aura/scoped\_window\_targeter.cc:22:47  

#6 0x55f1dfd8ba8d in operator() buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:48:5  

#7 0x55f1dfd8ba8d in reset buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:305:7  

#8 0x55f1dfd8ba8d in ~unique\_ptr buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:259:19  

#9 0x55f1dfd8ba8d in ash::WindowCycleList::~WindowCycleList() ash/wm/window\_cycle/window\_cycle\_list.cc:151:1  

#10 0x55f1dfd8bc8d in ash::WindowCycleList::~WindowCycleList() ash/wm/window\_cycle/window\_cycle\_list.cc:116:37  

#11 0x55f1dfd878ac in operator() buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:48:5  

#12 0x55f1dfd878ac in reset buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:305:7  

#13 0x55f1dfd878ac in ash::WindowCycleController::StopCycling() ash/wm/window\_cycle/window\_cycle\_controller.cc:421:22  

#14 0x55f1dbceccb9 in ui::EventDispatcher::DispatchEvent(ui::EventHandler\*, ui::Event\*) ui/events/event\_dispatcher.cc:190:12  

#15 0x55f1dbcec9e9 in ui::EventDispatcher::DispatchEventToEventHandlers(std::Cr::vector<ui::EventHandler\*, std::Cr::allocator[ui::EventHandler\\*](javascript:void(0);)>\*, ui::Event\*) ui/events/event\_dispatcher.cc:177:7  

#16 0x55f1dbcec07f in ui::EventDispatcher::ProcessEvent(ui::EventTarget\*, ui::Event\*) ui/events/event\_dispatcher.cc:125:3  

#17 0x55f1dbcebd06 in ui::EventDispatcherDelegate::DispatchEventToTarget(ui::EventTarget\*, ui::Event\*) ui/events/event\_dispatcher.cc:83:14  

#18 0x55f1dbceba96 in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget\*, ui::Event\*) ui/events/event\_dispatcher.cc:55:15  

#19 0x55f1ded902bb in aura::WindowEventDispatcher::ProcessGestures(aura::Window\*, std::Cr::vector<std::Cr::unique\_ptr<ui::GestureEvent, std::Cr::default\_delete[ui::GestureEvent](javascript:void(0);)>, std::Cr::allocator<std::Cr::unique\_ptr<ui::GestureEvent, std::Cr::default\_delete[ui::GestureEvent](javascript:void(0);)>>>) ui/aura/window\_event\_dispatcher.cc:352:15  

#20 0x55f1ded9536f in aura::WindowEventDispatcher::PostDispatchEvent(ui::EventTarget\*, ui::Event const&) ui/aura/window\_event\_dispatcher.cc:606:16  

#21 0x55f1dbcebae9 in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget\*, ui::Event\*) ui/events/event\_dispatcher.cc:59:15  

#22 0x55f1ded9a8ec in ui::EventProcessor::OnEventFromSource(ui::Event\*) ui/events/event\_processor.cc:56:17  

#23 0x55f1dbcf0630 in ui::EventSource::DeliverEventToSink(ui::Event\*) ui/events/event\_source.cc:118:16  

#24 0x55f1dbcf0b28 in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const\*) ui/events/event\_source.cc:66:14  

#25 0x55f1dbcef243 in ui::EventRewriter::SendEvent(base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);), ui::Event const\*) ui/events/event\_rewriter.cc:88:39  

#26 0x55f1cee0593c in ui::EventRewriterChromeOS::RewriteTouchEvent(ui::TouchEvent const&, base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);)) ui/chromeos/events/event\_rewriter\_chromeos.cc:1315:12  

#27 0x55f1cee02ed2 in ui::EventRewriterChromeOS::RewriteEvent(ui::Event const&, base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);)) ui/chromeos/events/event\_rewriter\_chromeos.cc:767:12  

#28 0x55f1dbcf0ad8 in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const\*) ui/events/event\_source.cc:67:32  

#29 0x55f1dbcef243 in ui::EventRewriter::SendEvent(base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);), ui::Event const\*) ui/events/event\_rewriter.cc:88:39  

#30 0x55f1df4aa900 in ash::KeyboardDrivenEventRewriter::RewriteEvent(ui::Event const&, base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);)) ash/events/keyboard\_driven\_event\_rewriter.cc:31:12  

#31 0x55f1dbcf0ad8 in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const\*) ui/events/event\_source.cc:67:32  

#32 0x55f1dbcef243 in ui::EventRewriter::SendEvent(base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);), ui::Event const\*) ui/events/event\_rewriter.cc:88:39  

#33 0x55f1df4a6af6 in ash::AccessibilityEventRewriter::RewriteEvent(ui::Event const&, base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);)) ash/events/accessibility\_event\_rewriter.cc  

#34 0x55f1dbcf0ad8 in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const\*) ui/events/event\_source.cc:67:32  

#35 0x55f1dbcef243 in ui::EventRewriter::SendEvent(base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);), ui::Event const\*) ui/events/event\_rewriter.cc:88:39  

#36 0x55f1df274a1e in ash::AutoclickDragEventRewriter::RewriteEvent(ui::Event const&, base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);)) ash/accessibility/autoclick/autoclick\_drag\_event\_rewriter.cc  

#37 0x55f1dbcf0ad8 in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const\*) ui/events/event\_source.cc:67:32

previously allocated by thread T0 (chrome) here:  

#0 0x55f1ca7f13ed in operator new(unsigned long) /b/s/w/ir/cache/builder/src/third\_party/llvm/compiler-rt/lib/asan/asan\_new\_delete.cpp:95:3  

#1 0x55f1dfd8b1af in make\_unique<ash::(anonymous namespace)::CustomWindowTargeter, aura::Window \*> buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:714:28  

#2 0x55f1dfd8b1af in ash::WindowCycleList::InitWindowCycleView() ash/wm/window\_cycle/window\_cycle\_list.cc:389:9  

#3 0x55f1d99bbfe3 in Run base/callback.h:145:12  

#4 0x55f1d99bbfe3 in base::OneShotTimer::RunUserTask() base/timer/timer.cc:277:19  

#5 0x55f1d990e65c in Run base/callback.h:145:12  

#6 0x55f1d990e65c in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/task/common/task\_annotator.cc:135:32  

#7 0x55f1d995291d in RunTask<(lambda at ../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:430:29)> base/task/common/task\_annotator.h:74:5  

#8 0x55f1d995291d in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow\*) base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:428:21  

#9 0x55f1d9951bf2 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:298:41  

#10 0x55f1d99538f4 in non-virtual thunk to base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc  

#11 0x55f1d9a66428 in base::MessagePumpLibevent::Run(base::MessagePump::Delegate\*) base/message\_loop/message\_pump\_libevent.cc:294:55  

#12 0x55f1d99543a5 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:581:12  

#13 0x55f1d98a1dae in base::RunLoop::Run(base::Location const&) base/run\_loop.cc:141:14  

#14 0x55f1cfb6aa2c in content::BrowserMainLoop::RunMainMessageLoop() content/browser/browser\_main\_loop.cc:1042:18  

#15 0x55f1cfb6f7bb in content::BrowserMainRunnerImpl::Run() content/browser/browser\_main\_runner\_impl.cc:157:15  

#16 0x55f1cfb64f3a in content::BrowserMain(content::MainFunctionParams) content/browser/browser\_main.cc:30:28  

#17 0x55f1d9662c5e in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate\*) content/app/content\_main\_runner\_impl.cc:678:10  

#18 0x55f1d96652c1 in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) content/app/content\_main\_runner\_impl.cc:1197:10  

#19 0x55f1d9664ceb in content::ContentMainRunnerImpl::Run() content/app/content\_main\_runner\_impl.cc:1062:12  

#20 0x55f1d965f1ea in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner\*) content/app/content\_main.cc:433:36  

#21 0x55f1d965f891 in content::ContentMain(content::ContentMainParams) content/app/content\_main.cc:461:10  

#22 0x55f1ca7f3bb0 in ChromeMain chrome/app/chrome\_main.cc:182:12  

#23 0x7fd72ab2c082 in \_\_libc\_start\_main /build/glibc-SzIz7B/glibc-2.31/csu/../csu/libc-start.c:308:16

SUMMARY: AddressSanitizer: heap-use-after-free ui/events/event\_processor.cc:77:26 in ui::EventProcessor::OnEventFromSource(ui::Event\*)  

Shadow bytes around the buggy address:  

0x0c0c801124d0: fd fd fd fd fa fa fa fa fd fd fd fd fd fd fd fd  

0x0c0c801124e0: fa fa fa fa fd fd fd fd fd fd fd fa fa fa fa fa  

0x0c0c801124f0: fd fd fd fd fd fd fd fa fa fa fa fa fd fd fd fd  

0x0c0c80112500: fd fd fd fa fa fa fa fa fd fd fd fd fd fd fd fa  

0x0c0c80112510: fa fa fa fa fd fd fd fd fd fd fd fa fa fa fa fa  

=>0x0c0c80112520:[fd]fd fd fd fd fd fd fa fa fa fa fa fd fd fd fd  

0x0c0c80112530: fd fd fd fd fa fa fa fa fd fd fd fd fd fd fd fa  

0x0c0c80112540: fa fa fa fa fd fd fd fd fd fd fd fa fa fa fa fa  

0x0c0c80112550: fd fd fd fd fd fd fd fa fa fa fa fa fd fd fd fd  

0x0c0c80112560: fd fd fd fa fa fa fa fa 00 00 00 00 00 00 00 fa  

0x0c0c80112570: fa fa fa fa fd fd fd fd fd fd fd fd fa fa fa fa  

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

==601599==ABORTING

## Attachments

- [1350561.webm](attachments/1350561.webm) (video/webm, 6.6 MB)
- [tested-device.jpeg](attachments/tested-device.jpeg) (image/jpeg, 102.7 KB)
- [tested-on-dut.log](attachments/tested-on-dut.log) (text/plain, 10.7 KB)

## Timeline

### [Deleted User] (2022-08-05)

[Empty comment from Monorail migration]

### rh...@gmail.com (2022-08-05)

uploading screencast

### ma...@google.com (2022-08-05)

Sending to ChromeOS triage.

### th...@google.com (2022-08-08)

[Empty comment from Monorail migration]

[Monorail components: OS>Inputs]

### th...@google.com (2022-08-08)

[Empty comment from Monorail migration]

### th...@google.com (2022-08-08)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-09)

[Empty comment from Monorail migration]

### rh...@gmail.com (2022-08-19)

bisecting the crash:

r1019997 can reproduce
r1027376 can reproduce
r1020005 can reproduce
r1029999 can reproduce
r1030000 can reproduce
r1032752 can reproduce
r1037149 can reproduce

the chromeOS stable version is affected by this issue.

### rh...@gmail.com (2022-08-24)

Hello,

This issue is missing security_severity and can I have an update for this?


### rh...@gmail.com (2022-08-30)

friendly ping, anyone can help me answer https://crbug.com/chromium/1350561#c9?

### rh...@gmail.com (2022-09-07)

friendly ping: any chance to get an simple update? or next action reminder for this issue?

### am...@chromium.org (2022-09-28)

Assigning to current Chrome OS security sheriff (who also happens to be original Chrome OS security sheriff)
Hi thomascedeno@ can you please update this issue with a security severity and FoundIn- as well as help get this assigned to a developer that can look at this. 
It appears zentaro@ has not visited the tracker for some time. Thank you.

### th...@google.com (2022-09-28)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-28)

[Empty comment from Monorail migration]

### th...@google.com (2022-09-28)

I don't have much visibility on which developers are available for bug triage - jsboos is the only other developer listed to handle System Serivces > Input, feel free to re-triage if you don't have any response.

### [Deleted User] (2022-09-29)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rh...@gmail.com (2022-10-03)

Hello,

I think the current owner jsboos@chromium.org is not correct owner and has never visited chromium. Would you like to get an advice from following developer?

robliao@chromium.org
oshima@chromium.org

oshima@ and robliao@ might find/reroute to the correct owner for this issue.

Thanks

### rh...@gmail.com (2022-10-17)

hello,

is there anyone fixing this issue?
thanks

### rh...@gmail.com (2022-10-26)

[Comment Deleted]

### rh...@gmail.com (2022-11-30)

Any chance this issue get an update? also the potential owner for this code ui/events/event_processor.cc are yichenz@chromium.org and sky@chromium.org.

Thanks

### ha...@google.com (2022-12-14)

Re-assigning it to yichenz@ who last modified the file in question.  

Potential memory corruption so retriaging it as Severity medium 

CC'ing current sheriff: jorgelo@

### yi...@google.com (2022-12-14)

https://chromium-review.googlesource.com/c/chromium/src/+/3792819 is the last CL landed in 106.0.5221.0. Reassign it to oshima-san as he is the owner of this CL.

### [Deleted User] (2022-12-14)

oshima: Uh oh! This issue still open and hasn't been updated in the last 130 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-12-28)

oshima: Uh oh! This issue still open and hasn't been updated in the last 144 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rh...@gmail.com (2023-01-09)

Sorry for the ping. Any chance I can get the update for the bug?

### rh...@gmail.com (2023-01-19)

oshima-san@,

Sorry for the ping.
Do you have bandwidth to take a look this issue? I'm still able to repro this issue on 111.0.5548.0

thanks 

### rh...@gmail.com (2023-02-02)

Hi,

Tested on DUT(tablet mode) with connected external keyboard, I'm still able to repro the issue.

### rh...@gmail.com (2023-02-24)

Friendly ping: Have any updates for this issue?

Thanks

### ha...@google.com (2023-03-15)

I just reached out the owner internally,  I will update once I have response from them

### os...@chromium.org (2023-03-15)

This is most likely because targeter is deleted during dispatching phase[1]. We probably need to create weak ptr for the targeter to detect it.
fyi: sky@

[1]  https://source.chromium.org/chromium/chromium/src/+/main:ui/events/event_processor.cc;drc=0e9a0b6e9bb6ec59521977eec805f5d0bca833e0;l=77

[Monorail components: Internals>Aura]

### ha...@google.com (2023-03-16)

[Empty comment from Monorail migration]

### rh...@gmail.com (2023-03-16)

Oshima@, hardi..@
Thank you for helping this bug and the updates.

### yi...@google.com (2023-03-16)

[Empty comment from Monorail migration]

### xi...@chromium.org (2023-03-16)

I seems unable to repro on ToT (r1117838, or 958b6f4091ddafd736e0a7d7644d2b4552507929).

Here is my repro steps:
1. Build chromeos asan build
2. Run emulator with the command line as #06
3. Ctrl+N to create 5 browser windows
4. Use Alt-W (for alt-tab in eumlator) to bring up WindowCycleView in emulator
5. Use mouse simulate touch to draw window all the way to left (or right)
6. Release Alt-W to destory WindowCycleView

And no crash, or asan error observed at step 6.

### rh...@gmail.com (2023-03-17)

Hi,
Sorry if you had hard to repro this issue.

The most important step is:
...
5. Use mouse simulate touch to draw window all the way to left (or right)
6. Release Alt-W to destory WindowCycleView
7. Repeat step 5 or just click on the WindowCycleView and pres Alt+W (simultaneously)

I will provide new screencast tomorrow.

### xi...@chromium.org (2023-03-17)

Thanks. Could you also be more specific on the repro steps?

I looked at the screencast in #2 above but that looks like just tap on the WindowCycleView. What happened before the tap? After we bring up WindowCycleView in emulator via Alt-W, should we hold both keys and let the WindowCycleView keep moving the focus ring and then tap on it? Or we hold Alt but release W, then tap?

I still don't have the luck to see this UAF. (I only repro'd WmFlingHandler UaF in https://crbug.com/chromium/1350558 in M106.)

I will try a `111.0.5548.0`.

### rh...@gmail.com (2023-03-18)

xiy..@

Sorry for the delay and thanks for the patience. I'm still able to repro this issue on Chromium 113.0.5661.0  or latest ToT r1119039 but with another steps as follow:
1. Enable tablet mode and touch devices 
2. Open two NTP
3. Swipe up from bottom and still hold the keys(touch)
4. Fire alt+W, release the touch and while still hold alt and then pres W(double).  or
4a. Fire alt+W, release the touch and while still hold alt and then pres W(double) and then touch.

step #4 and #4a is really fast <0.5s but I'm sure you can repro this bug. I also uploaded the new screen cast on google drive[1] due the file is over 10mb.

FYI, repro steps in https://crbug.com/chromium/1350561#c0 is no longer triggers the bug(sometimes 1/10 can trigger the bug) due the first time reported this bug on 06 August 22 and sorry for screencast in https://crbug.com/chromium/1350561#c2 is mislead and pretty sure its was similar with https://crbug.com/chromium/1350558).


[1]https://drive.google.com/file/d/1Dzn-rvfw3wISydH0WVeXK2Ro12Juk8X2/view?usp=share_link


### gi...@appspot.gserviceaccount.com (2023-03-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/310887c96175af0e8fe3cabb7cb4ab286ddc6493

commit 310887c96175af0e8fe3cabb7cb4ab286ddc6493
Author: Mitsuru Oshima <oshima@chromium.org>
Date: Tue Mar 21 16:32:21 2023

Check if EventTargeter was destroyed during event dispatch.

New test cases are added that delete the targeter during dispatch and find target phase.

Bug: 1350561
Test: covered by unittests. passed asan.
Change-Id: I314b7b76d5cd34ad6feae62686e442d734ebd6ee
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4342920
Commit-Queue: Mitsuru Oshima <oshima@chromium.org>
Reviewed-by: Scott Violet <sky@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1119984}

[modify] https://crrev.com/310887c96175af0e8fe3cabb7cb4ab286ddc6493/ui/events/event_processor_unittest.cc
[modify] https://crrev.com/310887c96175af0e8fe3cabb7cb4ab286ddc6493/ui/events/BUILD.gn
[add] https://crrev.com/310887c96175af0e8fe3cabb7cb4ab286ddc6493/ui/events/event_targeter.cc
[modify] https://crrev.com/310887c96175af0e8fe3cabb7cb4ab286ddc6493/ui/events/event_processor.cc
[modify] https://crrev.com/310887c96175af0e8fe3cabb7cb4ab286ddc6493/ui/events/event_targeter.h


### os...@chromium.org (2023-03-24)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-24)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-25)

[Empty comment from Monorail migration]

### am...@google.com (2023-03-29)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-03-29)

Congratulations! The VRP Panel has decided to award you $3,000 for this report of a moderately mitigated security bug + $1,000 bisect bonus. Thank you for your efforts and reporting this issue to us! 

### rh...@gmail.com (2023-03-30)

Thank you developers and Google VRP

### am...@google.com (2023-04-01)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-04-28)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-05-01)

[Comment Deleted]

[Monorail components: UI>Input]

### am...@chromium.org (2023-05-01)

[Comment Deleted]

[Monorail components: -UI>Input]

### pg...@google.com (2023-05-02)

[Empty comment from Monorail migration]

### pg...@google.com (2023-05-02)

[Empty comment from Monorail migration]

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-30)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### yu...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-06)

This issue was migrated from crbug.com/chromium/1350561?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Internals>Aura, OS>Inputs]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060513)*
