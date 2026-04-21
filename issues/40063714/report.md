# Security: Heap-use-after-free in ExclusiveAccessBubbleViews::UpdateBounds

| Field | Value |
|-------|-------|
| **Issue ID** | [40063714](https://issues.chromium.org/issues/40063714) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser |
| **Platforms** | Android, Fuchsia, Linux, Windows, ChromeOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | tl...@chromium.org |
| **Created** | 2023-03-21 |
| **Bounty** | $10,000.00 |

## Description

**VERSION**  

Chrome Version: 113.0.5667.0  

Operating System: ChromeOS

**REPRODUCTION CASE**

1. Go to <https://permission.site/> and click on "Pointer Lock"
2. Press F5

=================================================================  

==44950==ERROR: AddressSanitizer: heap-use-after-free on address 0x6170004286a8 at pc 0x55dee7766971 bp 0x7ffe3973dc90 sp 0x7ffe3973dc88  

READ of size 8 at 0x6170004286a8 thread T0 (chrome)  

==44950==WARNING: invalid path to external symbolizer!  

==44950==WARNING: Failed to use and restart external symbolizer!  

#0 0x55dee7766970 in GetForDereference ./../../base/allocator/partition\_allocator/pointers/raw\_ptr.h:975:48  

#1 0x55dee7766970 in operator-> ./../../base/allocator/partition\_allocator/pointers/raw\_ptr.h:737:12  

#2 0x55dee7766970 in ExclusiveAccessBubbleViews::UpdateBounds() ./../../chrome/browser/ui/views/exclusive\_access\_bubble\_views.cc:214:5  

#3 0x55dee78f4f98 in BrowserViewLayout::Layout(views::View\*) ./../../chrome/browser/ui/views/frame/browser\_view\_layout.cc:433:30  

#4 0x55ded8939d1e in views::View::Layout() ./../../ui/views/view.cc:858:25  

#5 0x55dee78019bf in BrowserView::Layout() ./../../chrome/browser/ui/views/frame/browser\_view.cc:3732:16  

#6 0x55ded89316bd in views::View::SetBoundsRect(gfx::Rect const&) ./../../ui/views/view.cc:386:7  

#7 0x55ded899b96c in views::NonClientFrameView::Layout() ./../../ui/views/window/non\_client\_view.cc:125:16  

#8 0x55dee77d8a36 in BrowserNonClientFrameViewChromeOS::Layout() ./../../chrome/browser/ui/views/frame/browser\_non\_client\_frame\_view\_chromeos.cc:471:30  

#9 0x55ded89316bd in views::View::SetBoundsRect(gfx::Rect const&) ./../../ui/views/view.cc:386:7  

#10 0x55ded899d2bb in views::NonClientView::Layout() ./../../ui/views/window/non\_client\_view.cc:271:16  

#11 0x55ded89316bd in views::View::SetBoundsRect(gfx::Rect const&) ./../../ui/views/view.cc:386:7  

#12 0x55ded894f382 in views::View::DefaultFillLayout::Layout(views::View\*) ./../../ui/views/view.cc:3604:14  

#13 0x55ded8939d1e in views::View::Layout() ./../../ui/views/view.cc:858:25  

#14 0x55ded8634509 in ui::Layer::SendDamagedRects() ./../../ui/compositor/layer.cc:1238:16  

#15 0x55ded8617ad1 in ui::Compositor::SendDamagedRectsRecursive(ui::Layer\*) ./../../ui/compositor/compositor.cc:729:10  

#16 0x55ded8617bc5 in ui::Compositor::SendDamagedRectsRecursive(ui::Layer\*) ./../../ui/compositor/compositor.cc:735:5  

#17 0x55ded8617bc5 in ui::Compositor::SendDamagedRectsRecursive(ui::Layer\*) ./../../ui/compositor/compositor.cc:735:5  

#18 0x55ded8617bc5 in ui::Compositor::SendDamagedRectsRecursive(ui::Layer\*) ./../../ui/compositor/compositor.cc:735:5  

#19 0x55ded8617bc5 in ui::Compositor::SendDamagedRectsRecursive(ui::Layer\*) ./../../ui/compositor/compositor.cc:735:5  

#20 0x55ded8617bc5 in ui::Compositor::SendDamagedRectsRecursive(ui::Layer\*) ./../../ui/compositor/compositor.cc:735:5  

#21 0x55ded741482e in cc::LayerTreeHost::RequestMainFrameUpdate(bool) ./../../cc/trees/layer\_tree\_host.cc:376:12  

#22 0x55ded7678681 in cc::SingleThreadProxy::DoBeginMainFrame(viz::BeginFrameArgs const&) ./../../cc/trees/single\_thread\_proxy.cc:1118:21  

#23 0x55ded767a2d5 in cc::SingleThreadProxy::BeginMainFrame(viz::BeginFrameArgs const&) ./../../cc/trees/single\_thread\_proxy.cc:1066:3  

#24 0x55ded767c895 in Invoke<void (cc::SingleThreadProxy::\*)(const viz::BeginFrameArgs &), base::WeakPtr[cc::SingleThreadProxy](javascript:void(0);), viz::BeginFrameArgs> ./../../base/functional/bind\_internal.h:744:12  

#25 0x55ded767c895 in MakeItSo<void (cc::SingleThreadProxy::\*)(const viz::BeginFrameArgs &), std::Cr::tuple<base::WeakPtr[cc::SingleThreadProxy](javascript:void(0);), viz::BeginFrameArgs> > ./../../base/functional/bind\_internal.h:946:5  

#26 0x55ded767c895 in RunImpl<void (cc::SingleThreadProxy::\*)(const viz::BeginFrameArgs &), std::Cr::tuple<base::WeakPtr[cc::SingleThreadProxy](javascript:void(0);), viz::BeginFrameArgs>, 0UL, 1UL> ./../../base/functional/bind\_internal.h:1018:12  

#27 0x55ded767c895 in base::internal::Invoker<base::internal::BindState<void (cc::SingleThreadProxy::\*)(viz::BeginFrameArgs const&), base::WeakPtr[cc::SingleThreadProxy](javascript:void(0);), viz::BeginFrameArgs>, void ()>::RunOnce(base::internal::BindStateBase\*) ./../../base/functional/bind\_internal.h:969:12  

#28 0x55ded1471be5 in Run ./../../base/functional/callback.h:152:12  

#29 0x55ded1471be5 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task\_annotator.cc:178:34  

#30 0x55ded14c0482 in RunTask<(lambda at ../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:478:11)> ./../../base/task/common/task\_annotator.h:89:5  

#31 0x55ded14c0482 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow\*) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:476:23  

#32 0x55ded14bf551 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:341:41  

#33 0x55ded14c1754 in non-virtual thunk to base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:0:0  

#34 0x55ded15f59cb in base::MessagePumpLibevent::Run(base::MessagePump::Delegate\*) ./../../base/message\_loop/message\_pump\_libevent.cc:290:55  

#35 0x55ded14c21f9 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:636:12  

#36 0x55ded13f6643 in base::RunLoop::Run(base::Location const&) ./../../base/run\_loop.cc:134:14  

#37 0x55dec904d430 in content::BrowserMainLoop::RunMainMessageLoop() ./../../content/browser/browser\_main\_loop.cc:1071:18  

#38 0x55dec9052a26 in content::BrowserMainRunnerImpl::Run() ./../../content/browser/browser\_main\_runner\_impl.cc:158:15  

#39 0x55dec9046cc3 in content::BrowserMain(content::MainFunctionParams) ./../../content/browser/browser\_main.cc:32:28  

#40 0x55decfb7a1c4 in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate\*) ./../../content/app/content\_main\_runner\_impl.cc:702:10  

#41 0x55decfb7d6b5 in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) ./../../content/app/content\_main\_runner\_impl.cc:1273:10  

#42 0x55decfb7d07c in content::ContentMainRunnerImpl::Run() ./../../content/app/content\_main\_runner\_impl.cc:1127:12  

#43 0x55decfb77930 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner\*) ./../../content/app/content\_main.cc:326:36  

#44 0x55decfb77e42 in content::ContentMain(content::ContentMainParams) ./../../content/app/content\_main.cc:343:10  

#45 0x55dec06e6d17 in ChromeMain ./../../chrome/app/chrome\_main.cc:190:12  

#46 0x7fca35d340b2 in \_\_libc\_start\_main /build/glibc-sMfBJT/glibc-2.31/csu/../csu/libc-start.c:308:16

0x6170004286a8 is located 680 bytes inside of 728-byte region [0x617000428400,0x6170004286d8)  

freed by thread T0 (chrome) here:  

#0 0x55dec06e4c1d in operator delete(void\*) *asan\_rtl*:3  

#1 0x55dee77f4124 in operator() ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:65:5  

#2 0x55dee77f4124 in reset ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:297:7  

#3 0x55dee77f4124 in BrowserView::UpdateExclusiveAccessExitBubbleContent(GURL const&, ExclusiveAccessBubbleType, base::OnceCallback<void (ExclusiveAccessBubbleHideReason)>, bool, bool) ./../../chrome/browser/ui/views/frame/browser\_view.cc:1756:30  

#4 0x55dee6977f1c in ExclusiveAccessManager::UpdateExclusiveAccessExitBubbleContent(base::OnceCallback<void (ExclusiveAccessBubbleHideReason)>, bool) ./../../chrome/browser/ui/exclusive\_access/exclusive\_access\_manager.cc:80:30  

#5 0x55dee6982e53 in MouseLockController::LostMouseLock() ./../../chrome/browser/ui/exclusive\_access/mouse\_lock\_controller.cc:152:33  

#6 0x55deca42b9a0 in content::WebContentsImpl::LostMouseLock(content::RenderWidgetHostImpl\*) ./../../content/browser/web\_contents/web\_contents\_impl.cc:3900:16  

#7 0x55deca7616c2 in content::RenderWidgetHostViewEventHandler::UnlockMouse() ./../../content/browser/renderer\_host/render\_widget\_host\_view\_event\_handler.cc:216:10  

#8 0x55deca0315d5 in content::RenderWidgetHostImpl::SetPageFocus(bool) ./../../content/browser/renderer\_host/render\_widget\_host\_impl.cc:1335:14  

#9 0x55deca0313e0 in content::RenderWidgetHostImpl::LostFocus() ./../../content/browser/renderer\_host/render\_widget\_host\_impl.cc:1284:3  

#10 0x55deca07f921 in content::RenderWidgetHostViewAura::OnWindowFocused(aura::Window\*, aura::Window\*) ./../../content/browser/renderer\_host/render\_widget\_host\_view\_aura.cc:2119:11  

#11 0x55ded8b91fe3 in wm::FocusController::SetFocusedWindow(aura::Window\*) ./../../ui/wm/core/focus\_controller.cc:298:17  

#12 0x55ded8b91895 in wm::FocusController::FocusAndActivateWindow(wm::ActivationChangeObserver::ActivationReason, aura::Window\*, bool) ./../../ui/wm/core/focus\_controller.cc:257:7  

#13 0x55ded89d0728 in views::NativeWidgetAura::Activate() ./../../ui/views/widget/native\_widget\_aura.cc:705:56  

#14 0x55ded89d0400 in views::NativeWidgetAura::Show(ui::WindowShowState, gfx::Rect const&) ./../../ui/views/widget/native\_widget\_aura.cc:673:7  

#15 0x55ded896f4f1 in views::Widget::Show() ./../../ui/views/widget/widget.cc:820:21  

#16 0x55ded47b301a in ash::OverviewGrid::MaybeInitDesksWidget() ./../../ash/wm/overview/overview\_grid.cc:2189:18  

#17 0x55ded47bd870 in ash::OverviewGrid::OnStartingAnimationComplete(bool) ./../../ash/wm/overview/overview\_grid.cc:1073:3  

#18 0x55ded47eff26 in ash::OverviewSession::OnStartingAnimationComplete(bool, bool) ./../../ash/wm/overview/overview\_session.cc:776:11  

#19 0x55ded47acccf in ash::OverviewController::OnStartingAnimationComplete(bool) ./../../ash/wm/overview/overview\_controller.cc:531:22  

#20 0x55ded47ac9c7 in ash::OverviewController::RemoveAndDestroyEnterAnimationObserver(ash::DelayedAnimationObserver\*) ./../../ash/wm/overview/overview\_controller.cc:251:5  

#21 0x55ded866c09c in ui::LayerAnimationObserver::DetachedFromSequence(ui::LayerAnimationSequence\*, bool) ./../../ui/compositor/layer\_animation\_observer.cc:55:5  

#22 0x55ded866c60c in ui::ImplicitAnimationObserver::OnLayerAnimationEnded(ui::LayerAnimationSequence\*) ./../../ui/compositor/layer\_animation\_observer.cc:89:13  

#23 0x55ded866fc88 in ui::LayerAnimationSequence::NotifyEnded() ./../../ui/compositor/layer\_animation\_sequence.cc:290:14  

#24 0x55ded867c7d5 in ProgressAnimationToEnd ./../../ui/compositor/layer\_animator.cc:486:13  

#25 0x55ded867c7d5 in ui::LayerAnimator::FinishAnimation(ui::LayerAnimationSequence\*, bool) ./../../ui/compositor/layer\_animator.cc:638:5  

#26 0x55ded8674634 in ui::LayerAnimator::StopAnimatingProperty(ui::LayerAnimationElement::AnimatableProperty) ./../../ui/compositor/layer\_animator.cc:374:5  

#27 0x55ded86741e0 in ui::LayerAnimator::SetTransform(gfx::Transform const&) ./../../ui/compositor/layer\_animator.cc:108:1  

#28 0x55ded85b9a6a in aura::Window::SetTransform(gfx::Transform const&) ./../../ui/aura/window.cc:439:12  

#29 0x55ded47fac1e in ash::SetTransform(aura::Window\*, gfx::Transform const&) ./../../ash/wm/overview/overview\_utils.cc:175:18  

#30 0x55ded47dc9cf in ash::OverviewItem::SetItemBounds(gfx::RectF const&, ash::OverviewAnimationType, bool) ./../../ash/wm/overview/overview\_item.cc:1283:3  

#31 0x55ded47db64e in ash::OverviewItem::SetBounds(gfx::RectF const&, ash::OverviewAnimationType) ./../../ash/wm/overview/overview\_item.cc:404:5  

#32 0x55ded85c3b76 in aura::Window::OnLayerBoundsChanged(gfx::Rect const&, ui::PropertyChangeReason) ./../../ui/aura/window.cc:1430:14

previously allocated by thread T0 (chrome) here:  

#0 0x55dec06e43bd in operator new(unsigned long) *asan\_rtl*:3  

#1 0x55dee77f41f6 in make\_unique<ExclusiveAccessBubbleViews, BrowserView \*, const GURL &, ExclusiveAccessBubbleType &, base::OnceCallback<void (ExclusiveAccessBubbleHideReason)> > ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:686:26  

#2 0x55dee77f41f6 in BrowserView::UpdateExclusiveAccessExitBubbleContent(GURL const&, ExclusiveAccessBubbleType, base::OnceCallback<void (ExclusiveAccessBubbleHideReason)>, bool, bool) ./../../chrome/browser/ui/views/frame/browser\_view.cc:1773:30  

#3 0x55dee6977f1c in ExclusiveAccessManager::UpdateExclusiveAccessExitBubbleContent(base::OnceCallback<void (ExclusiveAccessBubbleHideReason)>, bool) ./../../chrome/browser/ui/exclusive\_access/exclusive\_access\_manager.cc:80:30  

#4 0x55dee6982297 in MouseLockController::RequestToLockMouse(content::WebContents\*, bool, bool) ./../../chrome/browser/ui/exclusive\_access/mouse\_lock\_controller.cc:99:33  

#5 0x55deca42b6b9 in content::WebContentsImpl::RequestToLockMouse(content::RenderWidgetHostImpl\*, bool, bool, bool) ./../../content/browser/web\_contents/web\_contents\_impl.cc:3878:16  

#6 0x55deca0436d9 in content::RenderWidgetHostImpl::RequestMouseLock(bool, bool, base::OnceCallback<void (blink::mojom::PointerLockResult, mojo::PendingRemote[blink::mojom::PointerLockContext](javascript:void(0);))>) ./../../content/browser/renderer\_host/render\_widget\_host\_impl.cc:2951:14  

#7 0x55dec9c64b6c in RequestMouseLock ./../../content/browser/renderer\_host/input/input\_router\_impl.cc:404:12  

#8 0x55dec9c64b6c in non-virtual thunk to content::InputRouterImpl::RequestMouseLock(bool, bool, base::OnceCallback<void (blink::mojom::PointerLockResult, mojo::PendingRemote[blink::mojom::PointerLockContext](javascript:void(0);))>) ./../../content/browser/renderer\_host/input/input\_router\_impl.cc:0:0  

#9 0x55dec4aea296 in blink::mojom::WidgetInputHandlerHostStubDispatch::AcceptWithResponder(blink::mojom::WidgetInputHandlerHost\*, mojo::Message\*, std::Cr::unique\_ptr<mojo::MessageReceiverWithStatus, std::Cr::default\_delete[mojo::MessageReceiverWithStatus](javascript:void(0);) >) ./gen/third\_party/blink/public/mojom/input/input\_handler.mojom.cc:2597:13  

#10 0x55ded389857a in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/interface\_endpoint\_client.cc:968:56  

#11 0x55ded38b0640 in mojo::MessageDispatcher::Accept(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/message\_dispatcher.cc:43:19  

#12 0x55ded389ce99 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/interface\_endpoint\_client.cc:695:20  

#13 0x55ded38ba1dc in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper\*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner\*) ./../../mojo/public/cpp/bindings/lib/multiplex\_router.cc:1096:42  

#14 0x55ded38b9083 in mojo::internal::MultiplexRouter::Accept(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/multiplex\_router.cc:710:7  

#15 0x55ded38b0640 in mojo::MessageDispatcher::Accept(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/message\_dispatcher.cc:43:19  

#16 0x55ded3890474 in mojo::Connector::DispatchMessage(mojo::ScopedHandleBase[mojo::MessageHandle](javascript:void(0);)) ./../../mojo/public/cpp/bindings/lib/connector.cc:550:49  

#17 0x55ded38919bc in mojo::Connector::ReadAllAvailableMessages() ./../../mojo/public/cpp/bindings/lib/connector.cc:607:14  

#18 0x55dec4eb62f7 in base::RepeatingCallback<void (unsigned int)>::Run(unsigned int) const & ./../../base/functional/callback.h:333:12  

#19 0x55ded391013b in base::RepeatingCallback<void (unsigned int, mojo::HandleSignalsState const&)>::Run(unsigned int, mojo::HandleSignalsState const&) const & ./../../base/functional/callback.h:333:12  

#20 0x55ded390fcc1 in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, mojo::HandleSignalsState const&) ./../../mojo/public/cpp/system/simple\_watcher.cc:278:14  

#21 0x55ded1471be5 in Run ./../../base/functional/callback.h:152:12  

#22 0x55ded1471be5 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task\_annotator.cc:178:34  

#23 0x55ded14c0482 in RunTask<(lambda at ../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:478:11)> ./../../base/task/common/task\_annotator.h:89:5  

#24 0x55ded14c0482 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow\*) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:476:23  

#25 0x55ded14bf551 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:341:41  

#26 0x55ded14c1754 in non-virtual thunk to base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:0:0  

#27 0x55ded15f59cb in base::MessagePumpLibevent::Run(base::MessagePump::Delegate\*) ./../../base/message\_loop/message\_pump\_libevent.cc:290:55  

#28 0x55ded14c21f9 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:636:12  

#29 0x55ded13f6643 in base::RunLoop::Run(base::Location const&) ./../../base/run\_loop.cc:134:14  

#30 0x55dec904d430 in content::BrowserMainLoop::RunMainMessageLoop() ./../../content/browser/browser\_main\_loop.cc:1071:18  

#31 0x55dec9052a26 in content::BrowserMainRunnerImpl::Run() ./../../content/browser/browser\_main\_runner\_impl.cc:158:15  

#32 0x55dec9046cc3 in content::BrowserMain(content::MainFunctionParams) ./../../content/browser/browser\_main.cc:32:28  

#33 0x55decfb7a1c4 in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate\*) ./../../content/app/content\_main\_runner\_impl.cc:702:10

SUMMARY: AddressSanitizer: heap-use-after-free (/home/lbstyle/Desktop/asan-linux-release-1119925/chrome+0x389ad970) (BuildId: dbfbbcbf7ad4a950)  

Shadow bytes around the buggy address:  

0x617000428400: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x617000428480: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x617000428500: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x617000428580: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x617000428600: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

=>0x617000428680: fd fd fd fd fd[fd]fd fd fd fd fd fa fa fa fa fa  

0x617000428700: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x617000428780: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x617000428800: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x617000428880: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x617000428900: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

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

- [Screencast from 21 مارس, 2023 +00 16:48:29.webm](attachments/Screencast from 21 مارس, 2023 +00 16_48_29.webm) (video/webm, 2.9 MB)
- [PoC.html](attachments/PoC.html) (text/plain, 89 B)

## Timeline

### [Deleted User] (2023-03-21)

[Empty comment from Monorail migration]

### hc...@google.com (2023-03-22)

Can you please attach an html test case to this bug? Its kinda dangerous for us to be clicking on possible security issues w/o knowing the contents of the page

### ch...@gmail.com (2023-03-22)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-22)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### hc...@google.com (2023-03-23)

[Empty comment from Monorail migration]

### ch...@gmail.com (2023-03-24)

(Note: Please keep minimized chrome browser to repro the bug)

### ch...@google.com (2023-03-24)

[Empty comment from Monorail migration]

[Monorail blocking: b/275017043]

### ch...@google.com (2023-03-24)

Your report will be worked on in the Buganizer system (link: https://issuetracker.google.com/issues/275017043). You have been cc'ed on that report and should have access to it at this time to follow along while it is being worked on.

### [Deleted User] (2023-03-24)

[Empty comment from Monorail migration]

### ch...@gmail.com (2023-04-12)

Friendly ping.

### ch...@google.com (2023-04-12)

Dear chromium.khalil@gmail.com please check https://crbug.com/chromium/1426521#c8: 

Your report will be worked on in the Buganizer system (link: https://issuetracker.google.com/issues/275017043). You have been cc'ed on that report and should have access to it at this time to follow along while it is being worked on.



### ch...@google.com (2023-04-14)

Marked as fixed in order to reflect linked buganizer ticket

### ch...@google.com (2023-04-14)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-14)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-14)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-04-14)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-14)

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M113. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [113].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-04-15)

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M113. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [113].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-04-16)

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M113. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [113].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ma...@google.com (2023-04-17)

Is this needed in M113?  If so, please answer the merge questionnaire.

### [Deleted User] (2023-04-17)

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M113. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [113].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-04-18)

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M113. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [113].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-04-20)

This issue does not appear to be specific to Chrome OS and is in the Browser UI, updating impacted OSes accordingly 

[Monorail components: UI>Browser]

### am...@chromium.org (2023-04-20)

This issue was fixed by 11069c56f3f4ebd7b8b66969ef365cb508392cb3 // https://chromium-review.googlesource.com/c/chromium/src/+/4420047
Reassigning this issue to tluk@ patch author and owner of the buganizer issue this bug was moved to 

### am...@chromium.org (2023-04-20)

This fix does not look specific to Chrome OS however in b/275017043 https://crbug.com/chromium/1426521#c7: 
"The issue is we're holding an unowned reference to ExclusiveAccessBubbleViews::view_ but passing ownership of this view (the content view) to the popup widget here.

This Widget is then deleted by the OS (ChromeOS) but the ExclusiveAccessBubbleViews remains owned by the BrowserView and remains around enough to participate in a layout pass, causing the UAF. Will have a fix up shortly."

tluk@ is this possible only in Chrome OS? If so, please lmk and I'll readjust impacted OSes. 
If not, this should be considered for backmerge to M113 and possibly M112 which will soon be Extended Stable support. 


### am...@google.com (2023-04-20)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-04-20)

Congratulations, Khalil! The VRP Panel has decided to award you $10,000 for this report of a mildly mitigated security bug. Thank you for you efforts and reporting this issue to us -- nice work! 

### [Deleted User] (2023-04-20)

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M113. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [113].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-04-21)

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M113. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [113].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-04-22)

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M113. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [113].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-04-23)

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M113. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [113].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-04-24)

as per comments #23 and #24, in the case that this issue affects all platform and not just ChromeOS, since this is a browser UI fix, tentatively approving merge to M113 and M112
please merge this fix to M113 / branch 5672 asap, by 10am Pacific tomorrow/Tuesday 25 April so this fix can be included in the M113/Stable RC being cut tomorrow.

Also approving merge to M112/branch 5615, please merge this fix to branch 5672 so this fix can be included in the M112/Extended Stable release. 

### am...@google.com (2023-04-24)

[Empty comment from Monorail migration]

### sr...@google.com (2023-04-25)

M113 merge done here - https://chromium-review.googlesource.com/c/chromium/src/+/4476024?tab=checks

### sr...@google.com (2023-04-25)

[Empty comment from Monorail migration]

### sr...@google.com (2023-04-25)

M112 - merge done her e- https://chromium-review.googlesource.com/c/chromium/src/+/4473668


### [Deleted User] (2023-07-21)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1426521?no_tracker_redirect=1

[Monorail blocking: b/275017043]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40063714)*
