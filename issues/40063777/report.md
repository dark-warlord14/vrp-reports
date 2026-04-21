# Security:UAF in content::SyntheticPointerAction::ForwardTouchOrMouseInputEvents(browser process)

| Field | Value |
|-------|-------|
| **Issue ID** | [40063777](https://issues.chromium.org/issues/40063777) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | Blink>Input |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | 0x...@gmail.com |
| **Assignee** | bo...@chromium.org |
| **Created** | 2023-03-27 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

UAF in content::SyntheticPointerAction::ForwardTouchOrMouseInputEvents in the browser process

**VERSION**  

Chromium 114.0.5677.0 (Developer Build) (64-bit)  

Revision 2c16a353a63f5c3e31612dc255e00ba58537bca8-refs/heads/main@{#1122213}  

OS Windows 10 Version 22H2 (Build 19045.2728)

**REPRODUCTION CASE**

1. download the latest asan build(asan-win32-release\_x64-1122213.zip)
2. put the files into the webserver dir and run python3 -m http.server 8000
3. run the command:  
   
   chrome --user-data-dir=C:/tmp/any--enable-gpu-benchmarking about:blank <http://localhost:8000/poc.html>

# **FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION** Type of crash: [browser]

==15792==ERROR: AddressSanitizer: heap-use-after-free on address 0x12c279aa3930 at pc 0x7ff84b6dd1b4 bp 0x00afdf5fe580 sp 0x00afdf5fe5c8  

READ of size 8 at 0x12c279aa3930 thread T0  

==15792==WARNING: Failed to use and restart external symbolizer!  

#0 0x7ff84b6dd1b3 in content::SyntheticPointerAction::ForwardTouchOrMouseInputEvents C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\input\synthetic\_pointer\_action.cc:127  

#1 0x7ff84b6dbd4c in content::SyntheticPointerAction::ForwardInputEvents C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\input\synthetic\_pointer\_action.cc:42  

#2 0x7ff84b6d1818 in content::SyntheticGestureController::DispatchNextEvent C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\input\synthetic\_gesture\_controller.cc:116  

#3 0x7ff84b6d4f13 in base::internal::Invoker<base::internal::BindState<`lambda at ../../content/browser/renderer\_host/input/synthetic\_gesture\_controller.cc:101:11',base::WeakPtr[content::SyntheticGestureController](javascript:void(0);) >,void ()>::Run C:\b\s\w\ir\cache\builder\src\base\functional\bind\_internal.h:984  

#4 0x7ff85075355d in base::MetronomeTimer::OnScheduledTaskInvoked C:\b\s\w\ir\cache\builder\src\base\timer\timer.cc:374  

#5 0x7ff850753b5e in base::internal::Invoker<base::internal::BindState<void (base::MetronomeTimer::\*)(),base::internal::UnretainedWrapper[base::MetronomeTimer,base::unretained\_traits::MayNotDangle,0](javascript:void(0);) >,void ()>::Run C:\b\s\w\ir\cache\builder\src\base\functional\bind\_internal.h:984  

#6 0x7ff85079e2cd in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:178  

#7 0x7ff853d1f490 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:485  

#8 0x7ff853d1dfbf in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:350  

#9 0x7ff8506db2f5 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:212  

#10 0x7ff8506d8ded in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:78  

#11 0x7ff853d21d07 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:645  

#12 0x7ff850813588 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:134  

#13 0x7ff84a9bfea9 in content::BrowserMainLoop::RunMainMessageLoop C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_loop.cc:1071  

#14 0x7ff84a9c6f1f in content::BrowserMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_runner\_impl.cc:158  

#15 0x7ff84a9b7ca7 in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main.cc:32  

#16 0x7ff84ef74511 in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:702  

#17 0x7ff84ef78285 in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1272  

#18 0x7ff84ef77a13 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1126  

#19 0x7ff84ef727e3 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:326  

#20 0x7ff84ef7331a in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:343  

#21 0x7ff8432a1699 in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc:190  

#22 0x7ff704c16324 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main\_dll\_loader\_win.cc:166  

#23 0x7ff704c12bd8 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_exe\_main\_win.cc:390  

#24 0x7ff7050410fb in \_\_scrt\_common\_main\_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#25 0x7ff91f9d7613 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x180017613)  

#26 0x7ff9208626a0 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x1800526a0)

0x12c279aa3930 is located 96 bytes inside of 104-byte region [0x12c279aa38d0,0x12c279aa3938)  

freed by thread T0 here:  

#0 0x7ff704ccdcdd in free C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:82  

#1 0x7ff84b6dd403 in content::SyntheticPointerAction::~SyntheticPointerAction C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\input\synthetic\_pointer\_action.cc:16  

#2 0x7ff843370d6a in std::Cr::vector<std::Cr::unique\_ptr<perfetto::internal::TracingMuxerImpl::ConsumerImpl,std::Cr::default\_delete[perfetto::internal::TracingMuxerImpl::ConsumerImpl](javascript:void(0);) >,std::Cr::allocator<std::Cr::unique\_ptr<perfetto::internal::TracingMuxerImpl::ConsumerImpl,std::Cr::default\_delete[perfetto::internal::TracingMuxerImpl::ConsumerImpl](javascript:void(0);) > > >::\_\_destruct\_at\_end C:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\vector:727  

#3 0x7ff84b6cf9dc in content::SyntheticGestureController::GestureAndCallbackQueue::Pop C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\input\synthetic\_gesture\_controller.h:111  

#4 0x7ff84b6cf38e in content::SyntheticGestureController::~SyntheticGestureController C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\input\synthetic\_gesture\_controller.cc:31  

#5 0x7ff84b6d20b5 in content::SyntheticGestureController::~SyntheticGestureController C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\input\synthetic\_gesture\_controller.cc:27  

#6 0x7ff84babac11 in content::RenderWidgetHostImpl::SetView C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\render\_widget\_host\_impl.cc:573  

#7 0x7ff84bb1d4cd in content::RenderWidgetHostViewAura::~RenderWidgetHostViewAura C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\render\_widget\_host\_view\_aura.cc:2186  

#8 0x7ff84bb21319 in content::RenderWidgetHostViewAura::~RenderWidgetHostViewAura C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\render\_widget\_host\_view\_aura.cc:2182  

#9 0x7ff8523b515e in aura::Window::~Window C:\b\s\w\ir\cache\builder\src\ui\aura\window.cc:229  

#10 0x7ff8523ca463 in aura::Window::~Window C:\b\s\w\ir\cache\builder\src\ui\aura\window.cc:184  

#11 0x7ff84bad3573 in content::RenderWidgetHostImpl::RendererExited C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\render\_widget\_host\_impl.cc:2209  

#12 0x7ff84baacbe6 in content::RenderViewHostImpl::RenderProcessExited C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\render\_view\_host\_impl.cc:745  

#13 0x7ff84ba74763 in content::RenderProcessHostImpl::ProcessDied C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\render\_process\_host\_impl.cc:4824  

#14 0x7ff84ba73d23 in content::RenderProcessHostImpl::FastShutdownIfPossible C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\render\_process\_host\_impl.cc:3671  

#15 0x7ff8505c1a14 in browser\_shutdown::OnShutdownStarting C:\b\s\w\ir\cache\builder\src\chrome\browser\lifetime\browser\_shutdown.cc:169  

#16 0x7ff853495cb1 in Browser::OnWindowClosing C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\browser.cc:938  

#17 0x7ff856d8ceb9 in BrowserView::OnWindowCloseRequested C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\frame\browser\_view.cc:3685  

#18 0x7ff8503bfb15 in views::Widget::CloseWithReason C:\b\s\w\ir\cache\builder\src\ui\views\widget\widget.cc:735  

#19 0x7ff862f5bedf in base::internal::Invoker<base::internal::BindState<void (views::Widget::\*)(views::Widget::ClosedReason),base::internal::UnretainedWrapper<BrowserFrame,base::unretained\_traits::MayNotDangle,0>,views::Widget::ClosedReason>,void ()>::Run C:\b\s\w\ir\cache\builder\src\base\functional\bind\_internal.h:984  

#20 0x7ff843713fcd in base::RepeatingCallback<void ()>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:333  

#21 0x7ff850483648 in base::internal::Invoker<base::internal::BindState<`lambda at ../../ui/views/controls/button/button.cc:111:31',base::RepeatingCallback<void ()> >,void (const ui::Event &)>::Run C:\b\s\w\ir\cache\builder\src\base\functional\bind\_internal.h:984  

#22 0x7ff8504833c3 in base::RepeatingCallback<void (const ui::Event &)>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:333  

#23 0x7ff85048123e in views::Button::NotifyClick C:\b\s\w\ir\cache\builder\src\ui\views\controls\button\button.cc:631  

#24 0x7ff85047cd9b in views::Button::DefaultButtonControllerDelegate::NotifyClick C:\b\s\w\ir\cache\builder\src\ui\views\controls\button\button.cc:67  

#25 0x7ff8537cda04 in views::ButtonController::OnMouseReleased C:\b\s\w\ir\cache\builder\src\ui\views\controls\button\button\_controller.cc  

#26 0x7ff8503eb1e7 in views::View::ProcessMouseReleased C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:3451  

#27 0x7ff8572c8478 in ui::ScopedTargetHandler::OnEvent C:\b\s\w\ir\cache\builder\src\ui\events\scoped\_target\_handler.cc:28

previously allocated by thread T0 here:  

#0 0x7ff704ccdddd in malloc C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:98  

#1 0x7ff866480e1e in operator new D:\a\_work\1\s\src\vctools\crt\vcstartup\src\heap\new\_scalar.cpp:35  

#2 0x7ff84b6ceb73 in content::SyntheticGesture::Create C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\input\synthetic\_gesture.cc:47  

#3 0x7ff84b6ae4e2 in content::InputInjectorImpl::QueueSyntheticPointerAction C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\input\input\_injector\_impl.cc:46  

#4 0x7ff84706c15e in content::mojom::InputInjectorStubDispatch::AcceptWithResponder C:\b\s\w\ir\cache\builder\src\out\Release\_x64\gen\content\common\input\input\_injector.mojom.cc:1735  

#5 0x7ff84b6b0366 in content::mojom::InputInjectorStub<mojo::RawPtrImplRefTraits[content::mojom::InputInjector](javascript:void(0);) >::AcceptWithResponder C:\b\s\w\ir\cache\builder\src\out\Release\_x64\gen\content\common\input\input\_injector.mojom.h:201  

#6 0x7ff8513b3b8b in mojo::InterfaceEndpointClient::HandleValidatedMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface\_endpoint\_client.cc:968  

#7 0x7ff8546cddbc in mojo::MessageDispatcher::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\message\_dispatcher.cc:43  

#8 0x7ff8513b95c9 in mojo::InterfaceEndpointClient::HandleIncomingMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface\_endpoint\_client.cc:695  

#9 0x7ff8513a5838 in mojo::internal::MultiplexRouter::ProcessIncomingMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\multiplex\_router.cc:1096  

#10 0x7ff8513a4620 in mojo::internal::MultiplexRouter::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\multiplex\_router.cc:710  

#11 0x7ff8546cddbc in mojo::MessageDispatcher::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\message\_dispatcher.cc:43  

#12 0x7ff8513c9ff4 in mojo::Connector::DispatchMessageW C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\connector.cc:550  

#13 0x7ff8513cb980 in mojo::Connector::ReadAllAvailableMessages C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\connector.cc:607  

#14 0x7ff8513cd938 in base::internal::Invoker<base::internal::BindState<void (mojo::Connector::\*)(unsigned int),base::internal::UnretainedWrapper[mojo::Connector,base::unretained\_traits::MayNotDangle,0](javascript:void(0);) >,void (unsigned int)>::Run C:\b\s\w\ir\cache\builder\src\base\functional\bind\_internal.h:984  

#15 0x7ff846bd104d in base::RepeatingCallback<void (unsigned int)>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:333  

#16 0x7ff846bd0e54 in base::internal::Invoker<base::internal::BindState<void (\*)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &),base::RepeatingCallback<void (unsigned int)> >,void (unsigned int, const mojo::HandleSignalsState &)>::Run C:\b\s\w\ir\cache\builder\src\base\functional\bind\_internal.h:984  

#17 0x7ff85123b6a4 in base::RepeatingCallback<void (unsigned int, const mojo::HandleSignalsState &)>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:333  

#18 0x7ff85123b1c0 in mojo::SimpleWatcher::OnHandleReady C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\system\simple\_watcher.cc:278  

#19 0x7ff85123c4e8 in base::internal::Invoker<base::internal::BindState<void (mojo::SimpleWatcher::\*)(int, unsigned int, const mojo::HandleSignalsState &),base::WeakPtr[mojo::SimpleWatcher](javascript:void(0);),int,unsigned int,mojo::HandleSignalsState>,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind\_internal.h:971  

#20 0x7ff85079e2cd in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:178  

#21 0x7ff853d1f490 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:485  

#22 0x7ff853d1dfbf in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:350  

#23 0x7ff8506db2f5 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:212  

#24 0x7ff8506d8ded in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:78  

#25 0x7ff853d21d07 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:645  

#26 0x7ff850813588 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:134  

#27 0x7ff84a9bfea9 in content::BrowserMainLoop::RunMainMessageLoop C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_loop.cc:1071

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\input\synthetic\_pointer\_action.cc:127 in content::SyntheticPointerAction::ForwardTouchOrMouseInputEvents  

Shadow bytes around the buggy address:  

0x12c279aa3680: fa fa fa fa fa fa f7 fa fd fd fd fd fd fd fd fd  

0x12c279aa3700: fd fd fd fd fd fd fa fa fa fa fa fa f7 fa fd fd  

0x12c279aa3780: fd fd fd fd fd fd fd fd fd fd fd fd fa fa fa fa  

0x12c279aa3800: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fd  

0x12c279aa3880: fd fa fa fa fa fa fa fa f7 fa fd fd fd fd fd fd  

=>0x12c279aa3900: fd fd fd fd fd fd[fd]fa fa fa fa fa fa fa f7 fa  

0x12c279aa3980: fd fd fd fd fd fd fd fd fd fd fd fd fd fa fa fa  

0x12c279aa3a00: fa fa fa fa f7 fa fd fd fd fd fd fd fd fd fd fd  

0x12c279aa3a80: fd fd fd fd fa fa fa fa fa fa f7 fa fd fd fd fd  

0x12c279aa3b00: fd fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa  

0x12c279aa3b80: f7 fa fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

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

==15792==ADDITIONAL INFO

==15792==Note: Please include this section with the ASan report.  

Task trace:  

#0 0x7ff84b6d1319 in content::SyntheticGestureController::StartTimer C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\input\synthetic\_gesture\_controller.cc:99  

#1 0x7ff84b6d1319 in content::SyntheticGestureController::StartTimer C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\input\synthetic\_gesture\_controller.cc:99  

#2 0x7ff84b6d1319 in content::SyntheticGestureController::StartTimer C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\input\synthetic\_gesture\_controller.cc:99  

#3 0x7ff85123bfdb in mojo::SimpleWatcher::Context::Notify C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\system\simple\_watcher.cc:102

MiraclePtr Status: NOT PROTECTED  

No raw\_ptr<T> access to this region was detected prior to this crash.  

This crash is still exploitable with MiraclePtr.  

Refer to <https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md> for details.

==15792==END OF ADDITIONAL INFO  

==15792==ABORTING

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 1.7 KB)
- [gesture-util.js](attachments/gesture-util.js) (text/plain, 27.9 KB)
- [run-after-layout-and-paint.js](attachments/run-after-layout-and-paint.js) (text/plain, 2.6 KB)
- [testharness.js](attachments/testharness.js) (text/plain, 180.4 KB)

## Timeline

### [Deleted User] (2023-03-27)

[Empty comment from Monorail migration]

### hc...@google.com (2023-03-27)

bokan@, you've got the last change to synthetic_gesture_controller.cc (from https://crbug.com/chromium/1394736), could you take a quick look? I'm not able to replicate this (tried reproing both on linux and windows with no success), so please feel free to close if this isn't actionable.

[Monorail components: Blink>Input]

### [Deleted User] (2023-03-27)

[Empty comment from Monorail migration]

### bo...@chromium.org (2023-03-27)

I haven't reproduced but luckily I can see the problem from the stack trace - this is the same issue as 1394736 but I missed a case in my prior fix. I have an updated CL up for review.

Setting Impact-None and Severity-Low since this affects Chrome only in a non-default configuration (requires adding command line flag).

### gi...@appspot.gserviceaccount.com (2023-03-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/47138b0cb0581eb54dbdf2baf648eb86a82bd8a4

commit 47138b0cb0581eb54dbdf2baf648eb86a82bd8a4
Author: David Bokan <bokan@chromium.org>
Date: Wed Mar 29 19:11:25 2023

Fix UAF in SyntheticPointerAction

https://crrev.com/c/4241725 fixed a UAF where a gesture action causes
the browser window to be closed and the gesture controller to be
destroyed. It did so by checking for the controller's destruction after
any click-type event dispatch and early returning to ensure we're not
touching any of the gesture's members after destroying it.

That CL missed one case in SyntheticPointerAction. While
ForwardInputEvents does check for destruction and return GESTURE_ABORT,
the call to ForwardTouchOrMouseInputEvents has some code after dispatch
that will read memory belonging to |this|. This CL adds an early return
in this case as well.

Bug: 1427918,1394736
Change-Id: I08bf3a42f0bcaa44b2a795021fb5f8e32b35a67a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4375537
Reviewed-by: Mustaq Ahmed <mustaq@chromium.org>
Commit-Queue: David Bokan <bokan@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1123742}

[modify] https://crrev.com/47138b0cb0581eb54dbdf2baf648eb86a82bd8a4/content/browser/renderer_host/input/synthetic_pointer_action.cc


### bo...@chromium.org (2023-03-29)

Reporter, can you please try the repro on a build that includes #1123742 and see if the above fixed works?

### bo...@chromium.org (2023-03-29)

Fixed -> Assigned, will wait for confirmation since I never reproduced this one.

### 0x...@gmail.com (2023-03-31)

Sorry , the command line is missing a space.
the right one:
`chrome --user-data-dir=C:/tmp/any --enable-gpu-benchmarking about:blank http://localhost:8000/poc.html`



### 0x...@gmail.com (2023-03-31)

Get a new slightly different log with a different poc:
=================================================================
==5984==ERROR: AddressSanitizer: heap-use-after-free on address 0x127117993958 at pc 0x7ffd15609a2e bp 0x00acdd3fdfb0 sp 0x00acdd3fdff8
READ of size 8 at 0x127117993958 thread T0
==5984==WARNING: Failed to use and restart external symbolizer!
    #0 0x7ffd15609a2d in base::internal::WeakReference::MaybeValid C:\b\s\w\ir\cache\builder\src\base\memory\weak_ptr.cc:70
    #1 0x7ffd10437a13 in content::SyntheticPointerAction::ForwardTouchOrMouseInputEvents C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\input\synthetic_pointer_action.cc:127
    #2 0x7ffd10436cec in content::SyntheticPointerAction::ForwardInputEvents C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\input\synthetic_pointer_action.cc:42
    #3 0x7ffd1042c7b8 in content::SyntheticGestureController::DispatchNextEvent C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\input\synthetic_gesture_controller.cc:116
    #4 0x7ffd1042feb3 in base::internal::Invoker<base::internal::BindState<`lambda at ../../content/browser/renderer_host/input/synthetic_gesture_controller.cc:101:11',base::WeakPtr<content::SyntheticGestureController> >,void ()>::Run C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:984
    #5 0x7ffd154b9f0d in base::MetronomeTimer::OnScheduledTaskInvoked C:\b\s\w\ir\cache\builder\src\base\timer\timer.cc:374
    #6 0x7ffd154ba50e in base::internal::Invoker<base::internal::BindState<void (base::MetronomeTimer::*)(),base::internal::UnretainedWrapper<base::MetronomeTimer,base::unretained_traits::MayNotDangle,0> >,void ()>::Run C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:984
    #7 0x7ffd155048dd in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:178
    #8 0x7ffd18a7f47a in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:485
    #9 0x7ffd18a7dfcf in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:350
    #10 0x7ffd15442d35 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:212
    #11 0x7ffd1544082d in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:78
    #12 0x7ffd18a81d97 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:650
    #13 0x7ffd15579b88 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:134
    #14 0x7ffd0f70ad65 in content::BrowserMainLoop::RunMainMessageLoop C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_loop.cc:1072
    #15 0x7ffd0f711ddb in content::BrowserMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_runner_impl.cc:158
    #16 0x7ffd0f702b63 in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser_main.cc:32
    #17 0x7ffd13cd6ee9 in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:702
    #18 0x7ffd13cdac5d in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1272
    #19 0x7ffd13cda3eb in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1126
    #20 0x7ffd13cd51bb in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:326
    #21 0x7ffd13cd5cf2 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:343
    #22 0x7ffd08041699 in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:190
    #23 0x7ff636646324 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:166
    #24 0x7ff636642bd8 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:390
    #25 0x7ff636a717fb in __scrt_common_main_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #26 0x7ffda18e7613 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x180017613)
    #27 0x7ffda35c26a0 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x1800526a0)

### bo...@chromium.org (2023-03-31)

*facepalm* I added a WeakPtr that I use to check for deletion but that WeakPtr is a member of the deleted object.

https://crrev.com/c/4241725 made the same mistake in a few places (but correctly put the WeakPtr on the stack first in others).

Thanks for the confirmation - at least I know I'm in the right place.

Will put up another fix tomorrow.

### ke...@chromium.org (2023-04-13)

Why does this require the --enable-gpu-benchmarking flag to trigger the bug?

This is not Severity-Low, by the way. Bugs that require a non-default flag to be set implies Security_Impact-None, but severity does not take that into account. For example, we don't make assumptions about shipping configurations for other Chromium embedders.

Is this actually a regression in 114, or can it happen earlier than that?

### bo...@chromium.org (2023-04-13)

> Why does this require the --enable-gpu-benchmarking flag to trigger the bug?

There are two paths into creating/using SyntheticGestureController:

  * [1] InputInjector which is only instantiated if --enable-gpu-benchmarking flag is set
  * [2] DevTools protocol which isn't a flag but also isn't available on the drive by web

In general, SyntheticGestureController shouldn't be available/invokable outside of testing scenarios since being able to inject input would itself be a sever security issue.

[1] https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:content/browser/browser_interface_binders.cc;l=1026;drc=837cc12de25a288edf3ac222f7265c9936e69552
[2] https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:content/browser/devtools/protocol/input_handler.cc;l=1425-1427;drc=837cc12de25a288edf3ac222f7265c9936e69552

> This is not Severity-Low, by the way...

Ah, thanks for explaining.

> Is this actually a regression in 114, or can it happen earlier than that?

Not a regression, presumably this has been the case since the class was introduced ~2013

### gi...@appspot.gserviceaccount.com (2023-04-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/865adbfec6b41286880068cd28d8efee482bd565

commit 865adbfec6b41286880068cd28d8efee482bd565
Author: David Bokan <bokan@chromium.org>
Date: Thu Apr 13 20:12:19 2023

Synthetic Gestures: Checks of weak ptr happen on stack

https://crrev.com/c/4241725 added a WeakPtr to the
SyntheticGestureController so gestures could tell when they caused
deletion of the controller and return without touching deleted memory.

Unfortunately, that CL (and a followup in https://crrev.com/c/4375537)
made the silly mistake (in some callsites) of checking the WeakPtr
member directly. If the object was deleted, this is itself a UAF.

This CL changes those call sites to place the WeakPtr into a stack
variable before dispatching an event. When event dispatch returns,
check this stack variable rather than the (possibly deleted) member.

Also change related DCHECKs to CHECK as per [1]

[1] https://chromium.googlesource.com/chromium/src/+/HEAD/styleguide/c++/checks.md

Bug: 1427918,1394736
Change-Id: I1835eaeeafb2c75fca4034556d9bced342d9d5f7
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4387914
Reviewed-by: Ken Buchanan <kenrb@chromium.org>
Code-Coverage: Findit <findit-for-me@appspot.gserviceaccount.com>
Commit-Queue: David Bokan <bokan@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1130058}

[modify] https://crrev.com/865adbfec6b41286880068cd28d8efee482bd565/content/browser/renderer_host/input/synthetic_touchpad_pinch_gesture.cc
[modify] https://crrev.com/865adbfec6b41286880068cd28d8efee482bd565/content/browser/renderer_host/input/synthetic_touchscreen_pinch_gesture.cc
[modify] https://crrev.com/865adbfec6b41286880068cd28d8efee482bd565/content/browser/renderer_host/input/synthetic_gesture.cc
[modify] https://crrev.com/865adbfec6b41286880068cd28d8efee482bd565/content/browser/renderer_host/input/synthetic_tap_gesture.cc
[modify] https://crrev.com/865adbfec6b41286880068cd28d8efee482bd565/content/browser/renderer_host/input/synthetic_pointer_action.cc
[modify] https://crrev.com/865adbfec6b41286880068cd28d8efee482bd565/content/browser/renderer_host/input/synthetic_smooth_move_gesture.cc
[modify] https://crrev.com/865adbfec6b41286880068cd28d8efee482bd565/content/browser/renderer_host/render_widget_host_impl.h


### ke...@chromium.org (2023-04-13)

Thanks for the extra context.

### bo...@chromium.org (2023-04-19)

Reporter, can you try the repro in a build after r1130058? Included in 114.0.5714.0 and newer. 

### 0x...@gmail.com (2023-04-20)

I test this issue in the latest asan build and the chromium will close automatically without any crash log.

### bo...@chromium.org (2023-04-24)

Thanks, I believe that's expected

### [Deleted User] (2023-04-25)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-25)

[Empty comment from Monorail migration]

### am...@google.com (2023-05-05)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-05-05)

Congratulations, asnine! The VRP Panel has decided to award you $3,000 for this report of a mitigated security bug, given the reliance on --enable-gpu-benchmarking, which is only used for testing. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2023-05-05)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-08-01)

This issue was migrated from crbug.com/chromium/1427918?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40063777)*
