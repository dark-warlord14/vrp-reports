# Security: Heap-use-after-free in views::View::VisibilityChangedImpl 

| Field | Value |
|-------|-------|
| **Issue ID** | [40063861](https://issues.chromium.org/issues/40063861) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>Extensions |
| **Platforms** | Windows |
| **Reporter** | ch...@gmail.com |
| **Assignee** | em...@chromium.org |
| **Created** | 2023-04-01 |
| **Bounty** | $2,000.00 |

## Description

**VERSION**  

Chrome Version: 114.0.5687.0 (Official Build) canary (64-bit) (cohort: Clang-64)  

Operating System: Windows 10

**REPRODUCTION CASE**

1. Enable chrome://flags/#extensions-menu-access-control
2. Install an extension
3. Double click on Extensions icon

==6716==ERROR: AddressSanitizer: heap-use-after-free on address 0x1167af392c38 at pc 0x7ff97d88563b bp 0x002082bfd200 sp 0x002082bfd248  

READ of size 8 at 0x1167af392c38 thread T0  

==6716==WARNING: Failed to use and restart external symbolizer!  

#0 0x7ff97d88563a in views::View::VisibilityChangedImpl C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:3106  

#1 0x7ff97d86618d in views::View::PropagateVisibilityNotifications C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:3098  

#2 0x7ff97d86618d in views::View::PropagateVisibilityNotifications C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:3098  

#3 0x7ff97d86618d in views::View::PropagateVisibilityNotifications C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:3098  

#4 0x7ff97d86618d in views::View::PropagateVisibilityNotifications C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:3098  

#5 0x7ff97d86618d in views::View::PropagateVisibilityNotifications C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:3098  

#6 0x7ff97d84e2d8 in views::Widget::OnNativeWidgetVisibilityChanged C:\b\s\w\ir\cache\builder\src\ui\views\widget\widget.cc:1538  

#7 0x7ff9898eb48a in views::HWNDMessageHandler::OnWindowPosChanged C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd\_message\_handler.cc:3135  

#8 0x7ff9898d4bd0 in views::HWNDMessageHandler::\_ProcessWindowMessage C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd\_message\_handler.h:462  

#9 0x7ff9898d038e in views::HWNDMessageHandler::OnWndProc C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd\_message\_handler.cc:1219  

#10 0x7ff9822897d8 in gfx::WindowImpl::WndProc C:\b\s\w\ir\cache\builder\src\ui\gfx\win\window\_impl.cc:306  

#11 0x7ff982287f4d in base::win::WrappedWindowProc<&gfx::WindowImpl::WndProc> C:\b\s\w\ir\cache\builder\src\base\win\wrapped\_window\_proc.h:74  

#12 0x7ffa1a3fe857 in CallWindowProcW+0x3f7 (C:\Windows\System32\USER32.dll+0x18000e857)  

#13 0x7ffa1a3fe3db in DispatchMessageW+0x39b (C:\Windows\System32\USER32.dll+0x18000e3db)  

#14 0x7ffa1a415c2f in LookupIconIdFromDirectoryEx+0x2af (C:\Windows\System32\USER32.dll+0x180025c2f)  

#15 0x7ffa1be30ef3 in KiUserCallbackDispatcher+0x23 (C:\Windows\SYSTEM32\ntdll.dll+0x1800a0ef3)  

#16 0x7ffa199914c3 in NtUserSetWindowPos+0x13 (C:\Windows\System32\win32u.dll+0x1800014c3)  

#17 0x7ff9898c80c1 in views::HWNDMessageHandler::Hide C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd\_message\_handler.cc:846  

#18 0x7ff9898c7db3 in views::HWNDMessageHandler::Close C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd\_message\_handler.cc:540  

#19 0x7ff984697c3c in wm::`anonymous namespace'::HidingWindowAnimationObserverBase::OnAnimationCompleted C:\b\s\w\ir\cache\builder\src\ui\wm\core\window\_animations.cc:133  

#20 0x7ff97d946002 in ui::LayerAnimationObserver::DetachedFromSequence C:\b\s\w\ir\cache\builder\src\ui\compositor\layer\_animation\_observer.cc:55  

#21 0x7ff97d94648f in ui::ImplicitAnimationObserver::OnLayerAnimationEnded C:\b\s\w\ir\cache\builder\src\ui\compositor\layer\_animation\_observer.cc:89  

#22 0x7ff980ca7f8d in ui::LayerAnimationSequence::NotifyEnded C:\b\s\w\ir\cache\builder\src\ui\compositor\layer\_animation\_sequence.cc:290  

#23 0x7ff980c6de5f in ui::LayerAnimator::FinishAnimation C:\b\s\w\ir\cache\builder\src\ui\compositor\layer\_animator.cc:638  

#24 0x7ff980c7069c in ui::LayerAnimator::Step C:\b\s\w\ir\cache\builder\src\ui\compositor\layer\_animator.cc:517  

#25 0x7ff980cd207f in ui::LayerAnimatorCollection::OnAnimationStep C:\b\s\w\ir\cache\builder\src\ui\compositor\layer\_animator\_collection.cc:56  

#26 0x7ff97d96cdc2 in ui::Compositor::BeginMainFrame C:\b\s\w\ir\cache\builder\src\ui\compositor\compositor.cc:711  

#27 0x7ff9847b55aa in cc::SingleThreadProxy::DoBeginMainFrame C:\b\s\w\ir\cache\builder\src\cc\trees\single\_thread\_proxy.cc:1107  

#28 0x7ff9847b7dfd in cc::SingleThreadProxy::BeginMainFrame C:\b\s\w\ir\cache\builder\src\cc\trees\single\_thread\_proxy.cc:1064  

#29 0x7ff9847ba9ee in base::internal::Invoker<base::internal::BindState<void (cc::SingleThreadProxy::\*)(const viz::BeginFrameArgs &),base::WeakPtr[cc::SingleThreadProxy](javascript:void(0);),viz::BeginFrameArgs>,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind\_internal.h:976  

#30 0x7ff97dc279fd in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:178  

#31 0x7ff9811a919a in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:485  

#32 0x7ff9811a7cef in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:350  

#33 0x7ff97db65885 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:212  

#34 0x7ff97db6337d in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:78  

#35 0x7ff9811abab7 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:650  

#36 0x7ff97dc9cca8 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:134  

#37 0x7ff977e02055 in content::BrowserMainLoop::RunMainMessageLoop C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_loop.cc:1072  

#38 0x7ff977e090cb in content::BrowserMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_runner\_impl.cc:158  

#39 0x7ff977df9e53 in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main.cc:32  

#40 0x7ff97c3ef295 in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:702  

#41 0x7ff97c3f3009 in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1272  

#42 0x7ff97c3f2797 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1126  

#43 0x7ff97c3ed567 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:326  

#44 0x7ff97c3ee09e in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:343  

#45 0x7ff970701699 in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc:190  

#46 0x7ff7aa6a6324 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main\_dll\_loader\_win.cc:166  

#47 0x7ff7aa6a2bd8 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_exe\_main\_win.cc:390  

#48 0x7ff7aaad98fb in \_\_scrt\_common\_main\_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#49 0x7ffa1aa974b3 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x1800174b3)  

#50 0x7ffa1bde26a0 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x1800526a0)

0x1167af392c38 is located 56 bytes inside of 144-byte region [0x1167af392c00,0x1167af392c90)  

freed by thread T0 here:  

#0 0x7ff7aa75dcdd in free C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:82  

#1 0x7ff9909637c3 in ExtensionsMenuViewController::~ExtensionsMenuViewController C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\extensions\extensions\_menu\_view\_controller.cc:218  

#2 0x7ff98e77c6b3 in ExtensionsMenuCoordinator::CreateExtensionsMenuBubbleDialogDelegate C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\extensions\extensions\_menu\_coordinator.cc:86  

#3 0x7ff98e77c135 in ExtensionsMenuCoordinator::Show C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\extensions\extensions\_menu\_coordinator.cc:30  

#4 0x7ff98e77d9dd in ExtensionsToolbarButton::ToggleExtensionsMenu C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\extensions\extensions\_toolbar\_button.cc:132  

#5 0x7ff98e77f930 in base::internal::Invoker<base::internal::BindState<void (ExtensionsToolbarButton::\*)(),base::internal::UnretainedWrapper<ExtensionsToolbarButton,base::unretained\_traits::MayNotDangle,0> >,void ()>::Run C:\b\s\w\ir\cache\builder\src\base\functional\bind\_internal.h:989  

#6 0x7ff970b63c2d in base::RepeatingCallback<void ()>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:333  

#7 0x7ff97d90ce5a in base::internal::Invoker<base::internal::BindState<`lambda at ../../ui/views/controls/button/button.cc:111:31',base::RepeatingCallback<void ()> >,void (const ui::Event &)>::Run C:\b\s\w\ir\cache\builder\src\base\functional\bind\_internal.h:989  

#8 0x7ff97d90cbd5 in base::RepeatingCallback<void (const ui::Event &)>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:333  

#9 0x7ff98913e832 in views::MenuButtonController::Activate C:\b\s\w\ir\cache\builder\src\ui\views\controls\button\menu\_button\_controller.cc:258  

#10 0x7ff98913e223 in views::MenuButtonController::OnMousePressed C:\b\s\w\ir\cache\builder\src\ui\views\controls\button\menu\_button\_controller.cc:109  

#11 0x7ff98d465e30 in ToolbarButton::OnMousePressed C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\toolbar\toolbar\_button.cc:488  

#12 0x7ff97d872272 in views::View::ProcessMousePressed C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:3387  

#13 0x7ff97d871dda in views::View::OnMouseEvent C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:1518  

#14 0x7ff9846d9588 in ui::ScopedTargetHandler::OnEvent C:\b\s\w\ir\cache\builder\src\ui\events\scoped\_target\_handler.cc:28  

#15 0x7ff97f09996e in ui::EventDispatcher::DispatchEvent C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:187  

#16 0x7ff97f0989ea in ui::EventDispatcher::ProcessEvent C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:136  

#17 0x7ff97f0980c7 in ui::EventDispatcherDelegate::DispatchEventToTarget C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:82  

#18 0x7ff97f097c75 in ui::EventDispatcherDelegate::DispatchEvent C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:54  

#19 0x7ff980be5b1f in views::internal::RootView::OnMousePressed C:\b\s\w\ir\cache\builder\src\ui\views\widget\root\_view.cc:464  

#20 0x7ff97d850c5d in views::Widget::OnMouseEvent C:\b\s\w\ir\cache\builder\src\ui\views\widget\widget.cc:1712  

#21 0x7ff97f09996e in ui::EventDispatcher::DispatchEvent C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:187  

#22 0x7ff97f0989ea in ui::EventDispatcher::ProcessEvent C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:136  

#23 0x7ff97f0980c7 in ui::EventDispatcherDelegate::DispatchEventToTarget C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:82  

#24 0x7ff97f097c75 in ui::EventDispatcherDelegate::DispatchEvent C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:54  

#25 0x7ff9846a97b4 in ui::EventProcessor::OnEventFromSource C:\b\s\w\ir\cache\builder\src\ui\events\event\_processor.cc:72  

#26 0x7ff980bd214b in ui::EventSource::DeliverEventToSink C:\b\s\w\ir\cache\builder\src\ui\events\event\_source.cc:118  

#27 0x7ff980bd1d90 in ui::EventSource::SendEventToSinkFromRewriter C:\b\s\w\ir\cache\builder\src\ui\events\event\_source.cc:143

previously allocated by thread T0 here:  

#0 0x7ff7aa75dddd in malloc C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:98  

#1 0x7ff993681c1e in operator new D:\a\_work\1\s\src\vctools\crt\vcstartup\src\heap\new\_scalar.cpp:35  

#2 0x7ff98e77c5f1 in ExtensionsMenuCoordinator::CreateExtensionsMenuBubbleDialogDelegate C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\extensions\extensions\_menu\_coordinator.cc:86  

#3 0x7ff98e77c135 in ExtensionsMenuCoordinator::Show C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\extensions\extensions\_menu\_coordinator.cc:30  

#4 0x7ff98e77d9dd in ExtensionsToolbarButton::ToggleExtensionsMenu C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\extensions\extensions\_toolbar\_button.cc:132  

#5 0x7ff98e77f930 in base::internal::Invoker<base::internal::BindState<void (ExtensionsToolbarButton::\*)(),base::internal::UnretainedWrapper<ExtensionsToolbarButton,base::unretained\_traits::MayNotDangle,0> >,void ()>::Run C:\b\s\w\ir\cache\builder\src\base\functional\bind\_internal.h:989  

#6 0x7ff970b63c2d in base::RepeatingCallback<void ()>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:333  

#7 0x7ff97d90ce5a in base::internal::Invoker<base::internal::BindState<`lambda at ../../ui/views/controls/button/button.cc:111:31',base::RepeatingCallback<void ()> >,void (const ui::Event &)>::Run C:\b\s\w\ir\cache\builder\src\base\functional\bind\_internal.h:989  

#8 0x7ff97d90cbd5 in base::RepeatingCallback<void (const ui::Event &)>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:333  

#9 0x7ff98913e832 in views::MenuButtonController::Activate C:\b\s\w\ir\cache\builder\src\ui\views\controls\button\menu\_button\_controller.cc:258  

#10 0x7ff98913e223 in views::MenuButtonController::OnMousePressed C:\b\s\w\ir\cache\builder\src\ui\views\controls\button\menu\_button\_controller.cc:109  

#11 0x7ff98d465e30 in ToolbarButton::OnMousePressed C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\toolbar\toolbar\_button.cc:488  

#12 0x7ff97d872272 in views::View::ProcessMousePressed C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:3387  

#13 0x7ff97d871dda in views::View::OnMouseEvent C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:1518  

#14 0x7ff9846d9588 in ui::ScopedTargetHandler::OnEvent C:\b\s\w\ir\cache\builder\src\ui\events\scoped\_target\_handler.cc:28  

#15 0x7ff97f09996e in ui::EventDispatcher::DispatchEvent C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:187  

#16 0x7ff97f0989ea in ui::EventDispatcher::ProcessEvent C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:136  

#17 0x7ff97f0980c7 in ui::EventDispatcherDelegate::DispatchEventToTarget C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:82  

#18 0x7ff97f097c75 in ui::EventDispatcherDelegate::DispatchEvent C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:54  

#19 0x7ff980be5b1f in views::internal::RootView::OnMousePressed C:\b\s\w\ir\cache\builder\src\ui\views\widget\root\_view.cc:464  

#20 0x7ff97d850c5d in views::Widget::OnMouseEvent C:\b\s\w\ir\cache\builder\src\ui\views\widget\widget.cc:1712  

#21 0x7ff97f09996e in ui::EventDispatcher::DispatchEvent C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:187  

#22 0x7ff97f0989ea in ui::EventDispatcher::ProcessEvent C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:136  

#23 0x7ff97f0980c7 in ui::EventDispatcherDelegate::DispatchEventToTarget C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:82  

#24 0x7ff97f097c75 in ui::EventDispatcherDelegate::DispatchEvent C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:54  

#25 0x7ff9846a97b4 in ui::EventProcessor::OnEventFromSource C:\b\s\w\ir\cache\builder\src\ui\events\event\_processor.cc:72  

#26 0x7ff980bd214b in ui::EventSource::DeliverEventToSink C:\b\s\w\ir\cache\builder\src\ui\events\event\_source.cc:118  

#27 0x7ff980bd1d90 in ui::EventSource::SendEventToSinkFromRewriter C:\b\s\w\ir\cache\builder\src\ui\events\event\_source.cc:143

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:3106 in views::View::VisibilityChangedImpl  

Shadow bytes around the buggy address:  

0x1167af392980: f7 fa 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x1167af392a00: 00 00 00 00 fa fa fa fa fa fa f7 fa 00 00 00 00  

0x1167af392a80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 fa fa  

0x1167af392b00: fa fa fa fa f7 fa 00 00 00 00 00 00 00 00 00 00  

0x1167af392b80: 00 00 00 00 00 00 00 00 fa fa fa fa fa fa f7 fa  

=>0x1167af392c00: fd fd fd fd fd fd fd[fd]fd fd fd fd fd fd fd fd  

0x1167af392c80: fd fd fa fa fa fa fa fa f7 fa 00 00 00 00 00 00  

0x1167af392d00: 00 00 00 00 00 00 00 00 00 00 00 fa fa fa fa fa  

0x1167af392d80: fa fa f7 fa 00 00 00 00 00 00 00 00 00 00 00 00  

0x1167af392e00: 00 00 00 00 00 fa fa fa fa fa fa fa f7 fa fd fd  

0x1167af392e80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

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

## Attachments

- [Screen Recording (4-1-2023 5-11-02 AM).mp4](attachments/Screen Recording (4-1-2023 5-11-02 AM).mp4) (video/mp4, 2.5 MB)
- [screen.mp4](attachments/screen.mp4) (video/mp4, 2.0 MB)
- [screen_1.mp4](attachments/screen_1.mp4) (video/mp4, 354.4 KB)

## Timeline

### [Deleted User] (2023-04-01)

[Empty comment from Monorail migration]

### ch...@gmail.com (2023-04-01)

[Empty comment from Monorail migration]

### mp...@chromium.org (2023-04-01)

I can't seem to reproduce this on Linux, can you confirm it still reproduces?

### mp...@chromium.org (2023-04-01)

r1125011 at least, and also 1084002.

### ch...@gmail.com (2023-04-01)

I am still able to repro this on Windows.

### ch...@gmail.com (2023-04-01)

I couldn't repro this on Linux.

### mp...@chromium.org (2023-04-04)

[Empty comment from Monorail migration]

[Monorail components: Platform>Extensions]

### em...@chromium.org (2023-04-11)

Chrome: 111.0.5563.147 (Official Build) (64-bit) (cohort: Stable) 
OS: Windows 10 (Version 20H2 OS Build 19042.2728) - remote desktop
OS: Linux - local machine

I wasn't able to reproduce in Linux or Windows. See video: https://drive.google.com/file/d/11uTXN4SKfQfILfBAFPLseEKQrkCn0gvr/view?usp=sharing
Could it be that I am not running the executable properly? (using start chrome)

OS: Linux



### ch...@gmail.com (2023-04-12)

Please double click quickly. 

### ch...@gmail.com (2023-04-12)

Screen: https://drive.google.com/file/d/1NOZGq3MgrkFnqb5uAO3OI3V9OJbnJ7kY/view?usp=sharing

### ch...@gmail.com (2023-04-12)

Note: This does not repro on M111 (repro'd on canary).

### el...@chromium.org (2023-04-12)

Hm from the stacktrace this looks like an animation issue. Potentially related to the quick closing and opening of the extensions menu and the fact that layer animations are async. I will take a look into trying to repro this. 

### el...@chromium.org (2023-04-12)

I was unable to repro this on 114.0.5710.1 Canary.

Stacktrace looks the memory for the ExtensionsMenuViewController is freed and then accessed. This shouldn't destroy any views though so I'm not sure what object is being accessed after free. 

### ch...@gmail.com (2023-04-18)

You may need to click more than 2 times consistently.

### ch...@gmail.com (2023-05-03)

I tried to repro this bug on another windows machine and was able to repro the crash.

### ch...@gmail.com (2023-05-03)

[Empty comment from Monorail migration]

### ch...@gmail.com (2023-05-16)

Friendly ping.

### ch...@gmail.com (2023-06-26)

Emiliapaz@, Any update on this bug? thanks!

### ch...@gmail.com (2023-08-11)

Friendly ping.

### ch...@gmail.com (2023-10-31)

Friendly ping.

### so...@chromium.org (2023-11-02)

Is this reproducible? It seems like several comments say that it's not on Windows or Linux. Then there was a comment about double clicking, but it's unclear if that's confirmed or consistent.

### el...@chromium.org (2023-11-02)

I believe this is the same issue as in https://bugs.chromium.org/p/chromium/issues/detail?id=1493353&q=cc%3Ame&can=2 which had an explanation and similar repro instructions 

### ch...@gmail.com (2023-11-02)

I'm still able to repro this by double clicking.

### em...@chromium.org (2023-11-03)

Marking as duplicate, and working on crbug.com/1493353

### ch...@gmail.com (2023-11-03)

Note that this bug was filed before https://crbug.com/chromium/1493353.

### ch...@gmail.com (2023-11-03)

Does this report worth to be marked as a duplicate bug of https://crbug.com/chromium/1493353?

### am...@chromium.org (2023-11-03)

Hi Khalil, thank you for reaching out with your question. If faced with other similar issues in the future on bugs closed (such as Duplicate or Wontfix) please reach out to security-vrp@chromium.org and we're happy to take a look.

Hi emiliapaz@ since this is an externally reported issue reported prior to 1493353, it should not be merged into a newer report as a duplicate. This impacts the VRP process and negates the report from making it to the VRP reward decision process once the issue is fixed. 

Because 1493353 has more information and is sourced from crash reporting, that you may use in resolving this issue, I'll refrain from merging that report into this one. Please close this report as fixed once you've landed the fixes for https://crbug.com/chromium/1493353. I've updated this issue as blocked on https://crbug.com/chromium/1493353. 

Please reach out with any questions. Thank you! 

### ch...@gmail.com (2023-12-04)

I think this bug is fixed in https://crbug.com/chromium/1493353 (https://chromium-review.googlesource.com/c/chromium/src/+/5057224).

### aj...@chromium.org (2023-12-06)

[Empty comment from Monorail migration]

### aj...@chromium.org (2023-12-06)

Marking fixed as later dupe (from crash) is Fixed.

### [Deleted User] (2023-12-06)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-07)

[Empty comment from Monorail migration]

### am...@google.com (2023-12-14)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-12-14)

Congratulations Khalil! The Chrome VRP Panel has decided to award you $2,000 for this report of a highly mitigated security bug. Thank you for your efforts and reporting this issue to us.

### am...@google.com (2023-12-15)

[Empty comment from Monorail migration]

### is...@google.com (2023-12-15)

This issue was migrated from crbug.com/chromium/1429801?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail blocked-on: crbug.com/chromium/1493353]
[Monorail mergedwith: crbug.com/chromium/1493353]
[Monorail mergedinto: crbug.com/chromium/1493353]
[Monorail components added to Component Tags custom field.]

### em...@chromium.org (2025-07-21)

Not sure why this was reopened. Marking as fixed

### ch...@google.com (2025-10-28)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40063861)*
