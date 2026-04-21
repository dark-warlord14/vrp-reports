# Security: Heap-use-after-free in ash::DeskMiniView::UpdateDeskButtonVisibility

| Field | Value |
|-------|-------|
| **Issue ID** | [40063713](https://issues.chromium.org/issues/40063713) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Shell |
| **Platforms** | ChromeOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | ch...@google.com |
| **Created** | 2023-03-21 |
| **Bounty** | $1,000.00 |

## Description

Chrome Version: 113.0.5667.0  

Operating System: ChromeOS

**REPRODUCTION CASE**

- Run chrome with --enable-features=DesksTemplates

1. Go to <https://lbstyle.github.io/back.html> and click event in textarea
2. F5 >> Save desk as a template >> Use template
3. Repeat again step-2

==43659==ERROR: AddressSanitizer: heap-use-after-free on address 0x61900055b7b0 at pc 0x55c39e21d73a bp 0x7ffe558bd5f0 sp 0x7ffe558bd5e8  

READ of size 1 at 0x61900055b7b0 thread T0 (chrome)  

==43659==WARNING: invalid path to external symbolizer!  

==43659==WARNING: Failed to use and restart external symbolizer!  

#0 0x55c39e21d739 in dragged\_item\_over\_bar ./../../ash/wm/desks/desks\_bar\_view.h:117:47  

#1 0x55c39e21d739 in ash::DeskMiniView::UpdateDeskButtonVisibility() ./../../ash/wm/desks/desk\_mini\_view.cc:198:52  

#2 0x55c39e21cf6a in ash::DeskMiniView::DeskMiniView(ash::DesksBarView\*, aura::Window\*, ash::Desk\*) ./../../ash/wm/desks/desk\_mini\_view.cc:165:3  

#3 0x55c39e2040b9 in make\_unique<ash::DeskMiniView, ash::DesksBarView \*, aura::Window \*&, ash::Desk \*> ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:686:30  

#4 0x55c39e2040b9 in ash::DesksBarView::UpdateNewMiniViews(bool, bool) ./../../ash/wm/desks/desks\_bar\_view.cc:1151:11  

#5 0x55c39e203c68 in ash::DesksBarView::Init() ./../../ash/wm/desks/desks\_bar\_view.cc:695:3  

#6 0x55c39e2c0ff8 in ash::OverviewGrid::MaybeInitDesksWidget() ./../../ash/wm/overview/overview\_grid.cc:2187:20  

#7 0x55c39e2cb870 in ash::OverviewGrid::OnStartingAnimationComplete(bool) ./../../ash/wm/overview/overview\_grid.cc:1073:3  

#8 0x55c39e2fdf26 in ash::OverviewSession::OnStartingAnimationComplete(bool, bool) ./../../ash/wm/overview/overview\_session.cc:776:11  

#9 0x55c39e2baccf in ash::OverviewController::OnStartingAnimationComplete(bool) ./../../ash/wm/overview/overview\_controller.cc:531:22  

#10 0x55c39e2ba9c7 in ash::OverviewController::RemoveAndDestroyEnterAnimationObserver(ash::DelayedAnimationObserver\*) ./../../ash/wm/overview/overview\_controller.cc:251:5  

#11 0x55c3a217a09c in ui::LayerAnimationObserver::DetachedFromSequence(ui::LayerAnimationSequence\*, bool) ./../../ui/compositor/layer\_animation\_observer.cc:55:5  

#12 0x55c3a217a60c in ui::ImplicitAnimationObserver::OnLayerAnimationEnded(ui::LayerAnimationSequence\*) ./../../ui/compositor/layer\_animation\_observer.cc:89:13  

#13 0x55c3a217dc88 in ui::LayerAnimationSequence::NotifyEnded() ./../../ui/compositor/layer\_animation\_sequence.cc:290:14  

#14 0x55c3a218a7d5 in ProgressAnimationToEnd ./../../ui/compositor/layer\_animator.cc:486:13  

#15 0x55c3a218a7d5 in ui::LayerAnimator::FinishAnimation(ui::LayerAnimationSequence\*, bool) ./../../ui/compositor/layer\_animator.cc:638:5  

#16 0x55c3a218cd2d in ui::LayerAnimator::Step(base::TimeTicks) ./../../ui/compositor/layer\_animator.cc:517:7  

#17 0x55c3a2195c9b in ui::LayerAnimatorCollection::OnAnimationStep(base::TimeTicks) ./../../ui/compositor/layer\_animator\_collection.cc:56:16  

#18 0x55c3a21256dd in ui::Compositor::BeginMainFrame(viz::BeginFrameArgs const&) ./../../ui/compositor/compositor.cc:711:14  

#19 0x55c3a118660d in cc::SingleThreadProxy::DoBeginMainFrame(viz::BeginFrameArgs const&) ./../../cc/trees/single\_thread\_proxy.cc:1109:21  

#20 0x55c3a11882d5 in cc::SingleThreadProxy::BeginMainFrame(viz::BeginFrameArgs const&) ./../../cc/trees/single\_thread\_proxy.cc:1066:3  

#21 0x55c3a118a895 in Invoke<void (cc::SingleThreadProxy::\*)(const viz::BeginFrameArgs &), base::WeakPtr[cc::SingleThreadProxy](javascript:void(0);), viz::BeginFrameArgs> ./../../base/functional/bind\_internal.h:744:12  

#22 0x55c3a118a895 in MakeItSo<void (cc::SingleThreadProxy::\*)(const viz::BeginFrameArgs &), std::Cr::tuple<base::WeakPtr[cc::SingleThreadProxy](javascript:void(0);), viz::BeginFrameArgs> > ./../../base/functional/bind\_internal.h:946:5  

#23 0x55c3a118a895 in RunImpl<void (cc::SingleThreadProxy::\*)(const viz::BeginFrameArgs &), std::Cr::tuple<base::WeakPtr[cc::SingleThreadProxy](javascript:void(0);), viz::BeginFrameArgs>, 0UL, 1UL> ./../../base/functional/bind\_internal.h:1018:12  

#24 0x55c3a118a895 in base::internal::Invoker<base::internal::BindState<void (cc::SingleThreadProxy::\*)(viz::BeginFrameArgs const&), base::WeakPtr[cc::SingleThreadProxy](javascript:void(0);), viz::BeginFrameArgs>, void ()>::RunOnce(base::internal::BindStateBase\*) ./../../base/functional/bind\_internal.h:969:12  

#25 0x55c39af7fbe5 in Run ./../../base/functional/callback.h:152:12  

#26 0x55c39af7fbe5 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task\_annotator.cc:178:34  

#27 0x55c39afce482 in RunTask<(lambda at ../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:478:11)> ./../../base/task/common/task\_annotator.h:89:5  

#28 0x55c39afce482 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow\*) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:476:23  

#29 0x55c39afcd551 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:341:41  

#30 0x55c39afcf754 in non-virtual thunk to base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:0:0  

#31 0x55c39b1039cb in base::MessagePumpLibevent::Run(base::MessagePump::Delegate\*) ./../../base/message\_loop/message\_pump\_libevent.cc:290:55  

#32 0x55c39afd01f9 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:636:12  

#33 0x55c39af04643 in base::RunLoop::Run(base::Location const&) ./../../base/run\_loop.cc:134:14  

#34 0x55c392b5b430 in content::BrowserMainLoop::RunMainMessageLoop() ./../../content/browser/browser\_main\_loop.cc:1071:18  

#35 0x55c392b60a26 in content::BrowserMainRunnerImpl::Run() ./../../content/browser/browser\_main\_runner\_impl.cc:158:15  

#36 0x55c392b54cc3 in content::BrowserMain(content::MainFunctionParams) ./../../content/browser/browser\_main.cc:32:28  

#37 0x55c3996881c4 in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate\*) ./../../content/app/content\_main\_runner\_impl.cc:702:10  

#38 0x55c39968b6b5 in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) ./../../content/app/content\_main\_runner\_impl.cc:1273:10  

#39 0x55c39968b07c in content::ContentMainRunnerImpl::Run() ./../../content/app/content\_main\_runner\_impl.cc:1127:12  

#40 0x55c399685930 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner\*) ./../../content/app/content\_main.cc:326:36  

#41 0x55c399685e42 in content::ContentMain(content::ContentMainParams) ./../../content/app/content\_main.cc:343:10  

#42 0x55c38a1f4d17 in ChromeMain ./../../chrome/app/chrome\_main.cc:190:12  

#43 0x7f13599fe0b2 in \_\_libc\_start\_main /build/glibc-sMfBJT/glibc-2.31/csu/../csu/libc-start.c:308:16

0x61900055b7b0 is located 816 bytes inside of 992-byte region [0x61900055b480,0x61900055b860)  

freed by thread T0 (chrome) here:  

#0 0x55c38a1f2c1d in operator delete(void\*) *asan\_rtl*:3  

#1 0x55c3a243ec5c in operator() ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:65:5  

#2 0x55c3a243ec5c in reset ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:297:7  

#3 0x55c3a243ec5c in ~unique\_ptr ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:263:75  

#4 0x55c3a243ec5c in views::View::DoRemoveChildView(views::View\*, bool, bool, views::View\*) ./../../ui/views/view.cc:2993:1  

#5 0x55c3a243ee94 in views::View::RemoveAllChildViews() ./../../ui/views/view.cc:345:5  

#6 0x55c3a2477c3c in views::Widget::DestroyRootView() ./../../ui/views/widget/widget.cc:1989:15  

#7 0x55c3a24774c6 in views::Widget::~Widget() ./../../ui/views/widget/widget.cc:215:3  

#8 0x55c3a2478069 in views::Widget::~Widget() ./../../ui/views/widget/widget.cc:192:19  

#9 0x55c39e2bf2fb in operator() ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:65:5  

#10 0x55c39e2bf2fb in reset ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:297:7  

#11 0x55c39e2bf2fb in ~unique\_ptr ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:263:75  

#12 0x55c39e2bf2fb in ash::OverviewGrid::~OverviewGrid() ./../../ash/wm/overview/overview\_grid.cc:480:29  

#13 0x55c39e2bf4d3 in ash::OverviewGrid::~OverviewGrid() ./../../ash/wm/overview/overview\_grid.cc:480:29  

#14 0x55c39e2fa268 in destroy\_at<std::Cr::unique\_ptr<ash::OverviewGrid, std::Cr::default\_delete[ash::OverviewGrid](javascript:void(0);) >, 0> ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/construct\_at.h:101:5  

#15 0x55c39e2fa268 in destroy<std::Cr::unique\_ptr<ash::OverviewGrid, std::Cr::default\_delete[ash::OverviewGrid](javascript:void(0);) >, void, void> ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/allocator\_traits.h:323:9  

#16 0x55c39e2fa268 in \_\_base\_destruct\_at\_end ./../../buildtools/third\_party/libc++/trunk/include/vector:839:9  

#17 0x55c39e2fa268 in \_\_clear ./../../buildtools/third\_party/libc++/trunk/include/vector:833:29  

#18 0x55c39e2fa268 in std::Cr::vector<std::Cr::unique\_ptr<ash::OverviewGrid, std::Cr::default\_delete[ash::OverviewGrid](javascript:void(0);) >, std::Cr::allocator<std::Cr::unique\_ptr<ash::OverviewGrid, std::Cr::default\_delete[ash::OverviewGrid](javascript:void(0);) > > >::clearabi:v170000 ./../../buildtools/third\_party/libc++/trunk/include/vector:646:9  

#19 0x55c39e2f9a72 in ash::OverviewSession::Shutdown() ./../../ash/wm/overview/overview\_session.cc:364:14  

#20 0x55c39e2b82b2 in ash::OverviewController::ToggleOverview(ash::OverviewEnterExitType) ./../../ash/wm/overview/overview\_controller.cc:352:24  

#21 0x55c39e2b8a94 in ash::OverviewController::EndOverview(ash::OverviewEndAction, ash::OverviewEnterExitType) ./../../ash/wm/overview/overview\_controller.cc:150:3  

#22 0x55c39e2fe751 in ash::OverviewSession::OnWindowActivating(wm::ActivationChangeObserver::ActivationReason, aura::Window\*, aura::Window\*) ./../../ash/wm/overview/overview\_session.cc:0:0  

#23 0x55c3a26a15a9 in wm::FocusController::SetActiveWindow(wm::ActivationChangeObserver::ActivationReason, aura::Window\*, aura::Window\*, bool) ./../../ui/wm/core/focus\_controller.cc:354:14  

#24 0x55c3a269f75e in wm::FocusController::FocusAndActivateWindow(wm::ActivationChangeObserver::ActivationReason, aura::Window\*, bool) ./../../ui/wm/core/focus\_controller.cc:235:10  

#25 0x55c3a24de728 in views::NativeWidgetAura::Activate() ./../../ui/views/widget/native\_widget\_aura.cc:705:56  

#26 0x55c3a24de400 in views::NativeWidgetAura::Show(ui::WindowShowState, gfx::Rect const&) ./../../ui/views/widget/native\_widget\_aura.cc:673:7  

#27 0x55c3a247d45c in views::Widget::Show() ./../../ui/views/widget/widget.cc:811:23  

#28 0x55c3b1946718 in FedCmAccountSelectionView::OnVisibilityChanged(content::Visibility) ./../../chrome/browser/ui/views/webid/fedcm\_account\_selection\_view\_desktop.cc:176:21  

#29 0x55c393f4aebf in void content::WebContentsImpl::WebContentsObserverList::NotifyObservers<void (content::WebContentsObserver::\*)(content::Visibility), content::Visibility&>(void (content::WebContentsObserver::\*)(content::Visibility), content::Visibility&) ./../../content/browser/web\_contents/web\_contents\_impl.h:1552:9  

#30 0x55c393f38cdd in content::WebContentsImpl::SetVisibilityAndNotifyObservers(content::Visibility) ./../../content/browser/web\_contents/web\_contents\_impl.cc:5377:16  

#31 0x55c393f2629a in content::WebContentsImpl::UpdateVisibilityAndNotifyPageAndView(content::Visibility, bool) ./../../content/browser/web\_contents/web\_contents\_impl.cc:3781:5  

#32 0x55c3a20ce608 in aura::Window::SetOcclusionInfo(aura::Window::OcclusionState, SkRegion const&) ./../../ui/aura/window.cc:1020:16  

#33 0x55c3a20f694d in aura::DefaultWindowOcclusionChangeBuilder::~DefaultWindowOcclusionChangeBuilder() ./../../ui/aura/window\_occlusion\_change\_builder.cc:35:15  

#34 0x55c3a20f6abb in aura::DefaultWindowOcclusionChangeBuilder::~DefaultWindowOcclusionChangeBuilder() ./../../ui/aura/window\_occlusion\_change\_builder.cc:26:51  

#35 0x55c3a20ec3c8 in operator() ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:65:5  

#36 0x55c3a20ec3c8 in reset ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:297:7  

#37 0x55c3a20ec3c8 in ~unique\_ptr ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:263:75  

#38 0x55c3a20ec3c8 in aura::WindowOcclusionTracker::MaybeComputeOcclusion() ./../../ui/aura/window\_occlusion\_tracker.cc:345:3  

#39 0x55c3a20e9aa7 in aura::WindowOcclusionTracker::ForceWindowVisible(aura::Window\*) ./../../ui/aura/window\_occlusion\_tracker.cc:788:7  

#40 0x55c39e212490 in make\_unique<aura::WindowOcclusionTracker::ScopedForceVisible, aura::Window \*> ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:686:30  

#41 0x55c39e212490 in ash::DeskPreviewView::DeskPreviewView(views::Button::PressedCallback, ash::DeskMiniView\*) ./../../ash/wm/desks/desk\_preview\_view.cc:344:11  

#42 0x55c39e21c2b5 in make\_unique<ash::DeskPreviewView, base::RepeatingCallback<void ()>, ash::DeskMiniView \*> ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:686:30  

#43 0x55c39e21c2b5 in ash::DeskMiniView::DeskMiniView(ash::DesksBarView\*, aura::Window\*, ash::Desk\*) ./../../ash/wm/desks/desk\_mini\_view.cc:121:32  

#44 0x55c39e2040b9 in make\_unique<ash::DeskMiniView, ash::DesksBarView \*, aura::Window \*&, ash::Desk \*> ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:686:30  

#45 0x55c39e2040b9 in ash::DesksBarView::UpdateNewMiniViews(bool, bool) ./../../ash/wm/desks/desks\_bar\_view.cc:1151:11

previously allocated by thread T0 (chrome) here:  

#0 0x55c38a1f23bd in operator new(unsigned long) *asan\_rtl*:3  

#1 0x55c39e2c0fb5 in make\_unique<ash::DesksBarView, ash::OverviewGrid \*> ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:686:26  

#2 0x55c39e2c0fb5 in ash::OverviewGrid::MaybeInitDesksWidget() ./../../ash/wm/overview/overview\_grid.cc:2186:38  

#3 0x55c39e2cb870 in ash::OverviewGrid::OnStartingAnimationComplete(bool) ./../../ash/wm/overview/overview\_grid.cc:1073:3  

#4 0x55c39e2fdf26 in ash::OverviewSession::OnStartingAnimationComplete(bool, bool) ./../../ash/wm/overview/overview\_session.cc:776:11  

#5 0x55c39e2baccf in ash::OverviewController::OnStartingAnimationComplete(bool) ./../../ash/wm/overview/overview\_controller.cc:531:22  

#6 0x55c39e2ba9c7 in ash::OverviewController::RemoveAndDestroyEnterAnimationObserver(ash::DelayedAnimationObserver\*) ./../../ash/wm/overview/overview\_controller.cc:251:5  

#7 0x55c3a217a09c in ui::LayerAnimationObserver::DetachedFromSequence(ui::LayerAnimationSequence\*, bool) ./../../ui/compositor/layer\_animation\_observer.cc:55:5  

#8 0x55c3a217a60c in ui::ImplicitAnimationObserver::OnLayerAnimationEnded(ui::LayerAnimationSequence\*) ./../../ui/compositor/layer\_animation\_observer.cc:89:13  

#9 0x55c3a217dc88 in ui::LayerAnimationSequence::NotifyEnded() ./../../ui/compositor/layer\_animation\_sequence.cc:290:14  

#10 0x55c3a218a7d5 in ProgressAnimationToEnd ./../../ui/compositor/layer\_animator.cc:486:13  

#11 0x55c3a218a7d5 in ui::LayerAnimator::FinishAnimation(ui::LayerAnimationSequence\*, bool) ./../../ui/compositor/layer\_animator.cc:638:5  

#12 0x55c3a218cd2d in ui::LayerAnimator::Step(base::TimeTicks) ./../../ui/compositor/layer\_animator.cc:517:7  

#13 0x55c3a2195c9b in ui::LayerAnimatorCollection::OnAnimationStep(base::TimeTicks) ./../../ui/compositor/layer\_animator\_collection.cc:56:16  

#14 0x55c3a21256dd in ui::Compositor::BeginMainFrame(viz::BeginFrameArgs const&) ./../../ui/compositor/compositor.cc:711:14  

#15 0x55c3a118660d in cc::SingleThreadProxy::DoBeginMainFrame(viz::BeginFrameArgs const&) ./../../cc/trees/single\_thread\_proxy.cc:1109:21  

#16 0x55c3a11882d5 in cc::SingleThreadProxy::BeginMainFrame(viz::BeginFrameArgs const&) ./../../cc/trees/single\_thread\_proxy.cc:1066:3  

#17 0x55c3a118a895 in Invoke<void (cc::SingleThreadProxy::\*)(const viz::BeginFrameArgs &), base::WeakPtr[cc::SingleThreadProxy](javascript:void(0);), viz::BeginFrameArgs> ./../../base/functional/bind\_internal.h:744:12  

#18 0x55c3a118a895 in MakeItSo<void (cc::SingleThreadProxy::\*)(const viz::BeginFrameArgs &), std::Cr::tuple<base::WeakPtr[cc::SingleThreadProxy](javascript:void(0);), viz::BeginFrameArgs> > ./../../base/functional/bind\_internal.h:946:5  

#19 0x55c3a118a895 in RunImpl<void (cc::SingleThreadProxy::\*)(const viz::BeginFrameArgs &), std::Cr::tuple<base::WeakPtr[cc::SingleThreadProxy](javascript:void(0);), viz::BeginFrameArgs>, 0UL, 1UL> ./../../base/functional/bind\_internal.h:1018:12  

#20 0x55c3a118a895 in base::internal::Invoker<base::internal::BindState<void (cc::SingleThreadProxy::\*)(viz::BeginFrameArgs const&), base::WeakPtr[cc::SingleThreadProxy](javascript:void(0);), viz::BeginFrameArgs>, void ()>::RunOnce(base::internal::BindStateBase\*) ./../../base/functional/bind\_internal.h:969:12  

#21 0x55c39af7fbe5 in Run ./../../base/functional/callback.h:152:12  

#22 0x55c39af7fbe5 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task\_annotator.cc:178:34  

#23 0x55c39afce482 in RunTask<(lambda at ../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:478:11)> ./../../base/task/common/task\_annotator.h:89:5  

#24 0x55c39afce482 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow\*) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:476:23  

#25 0x55c39afcd551 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:341:41  

#26 0x55c39afcf754 in non-virtual thunk to base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:0:0  

#27 0x55c39b1039cb in base::MessagePumpLibevent::Run(base::MessagePump::Delegate\*) ./../../base/message\_loop/message\_pump\_libevent.cc:290:55  

#28 0x55c39afd01f9 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:636:12  

#29 0x55c39af04643 in base::RunLoop::Run(base::Location const&) ./../../base/run\_loop.cc:134:14  

#30 0x55c392b5b430 in content::BrowserMainLoop::RunMainMessageLoop() ./../../content/browser/browser\_main\_loop.cc:1071:18  

#31 0x55c392b60a26 in content::BrowserMainRunnerImpl::Run() ./../../content/browser/browser\_main\_runner\_impl.cc:158:15  

#32 0x55c392b54cc3 in content::BrowserMain(content::MainFunctionParams) ./../../content/browser/browser\_main.cc:32:28  

#33 0x55c3996881c4 in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate\*) ./../../content/app/content\_main\_runner\_impl.cc:702:10  

#34 0x55c39968b6b5 in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) ./../../content/app/content\_main\_runner\_impl.cc:1273:10  

#35 0x55c39968b07c in content::ContentMainRunnerImpl::Run() ./../../content/app/content\_main\_runner\_impl.cc:1127:12  

#36 0x55c399685930 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner\*) ./../../content/app/content\_main.cc:326:36

SUMMARY: AddressSanitizer: heap-use-after-free (/home/lbstyle/Desktop/asan-linux-release-1119925/chrome+0x25956739) (BuildId: dbfbbcbf7ad4a950)  

Shadow bytes around the buggy address:  

0x61900055b500: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x61900055b580: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x61900055b600: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x61900055b680: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x61900055b700: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

=>0x61900055b780: fd fd fd fd fd fd[fd]fd fd fd fd fd fd fd fd fd  

0x61900055b800: fd fd fd fd fd fd fd fd fd fd fd fd fa fa fa fa  

0x61900055b880: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x61900055b900: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x61900055b980: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x61900055ba00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

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

- [Screencast from 21 مارس, 2023 +00 16:38:34.webm](attachments/Screencast from 21 مارس, 2023 +00 16_38_34.webm) (video/webm, 3.6 MB)
- [PoC.html](attachments/PoC.html) (text/plain, 3.4 KB)

## Timeline

### [Deleted User] (2023-03-21)

[Empty comment from Monorail migration]

### hc...@google.com (2023-03-22)

Can you please attach https://lbstyle.github.io/back.html to this bug? its kinda dangerous for us to click on random links w/o seeing the contents of the html page.

### ch...@gmail.com (2023-03-22)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-22)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### hc...@google.com (2023-03-23)

this PoC.html includes references to all sorts of different external resources and makes it harder to verify its safe and isolate it down to a specific cause. Can you work on minimizing this PoC to a smaller file?

(I tried cutting things out but I couldn't replicate the issue)

@dandersson: I'm adding you here as well as I'm not actually sure how to use the DeskTemplate feature, so I might be missing something. Note that I have not been able to repro this. (I'm also not sure what bug component to use)

[Monorail components: Internals>Media>ScreenCapture]

### hc...@google.com (2023-03-23)

[Empty comment from Monorail migration]

### mf...@chromium.org (2023-03-23)

Not related to screen capture as far as I can tell but how ChromeOS implements desktop animations.

[Monorail components: -Internals>Media>ScreenCapture UI>Shell]

### da...@chromium.org (2023-03-23)

[Empty comment from Monorail migration]

### da...@chromium.org (2023-03-23)

We're investigating this. At this point we don't need any more feedback from the reporter.

### am...@chromium.org (2023-03-24)

OS=Chrome so this can also receive appropriate triage (including severity + foundin) by ChromeOS security team

### [Deleted User] (2023-03-24)

[Empty comment from Monorail migration]

### ch...@gmail.com (2023-04-15)

Friendly ping.

### ch...@google.com (2023-05-22)

Your report will be worked on in the Buganizer system (link: https://issuetracker.google.com/issues/283720524). You have been cc'ed on that report and should have access to it at this time to follow along while it is being worked on. We are setting  Security_Severity-High as a default and the priority may either increase or decrease once their report is fully triaged and analyzed



[Monorail blocking: b/283720524]

### [Deleted User] (2023-05-22)

[Empty comment from Monorail migration]

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### ch...@gmail.com (2023-05-25)

This seems fixed in https://chromium-review.googlesource.com/c/chromium/src/+/4395222 as mentioned in the Buganizer report. 

### ch...@google.com (2023-05-25)

Thanks for the heads-up...will close this bug (also closed linked buganizer ticket)



### ch...@google.com (2023-05-25)

[Empty comment from Monorail migration]

### ch...@gmail.com (2023-05-25)

Note that this bug was filed 3 days before https://crbug.com/chromium/1427417, so this should be marked as Fixed not WontFix. right?

### ch...@google.com (2023-05-25)

So sorry...my bad! 

### [Deleted User] (2023-05-26)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-26)

[Empty comment from Monorail migration]

### ch...@gmail.com (2023-06-16)

What is the severity that should be specified here?

### ch...@google.com (2023-06-27)

[Empty comment from Monorail migration]

### st...@google.com (2023-07-18)

[Empty comment from Monorail migration]

### am...@google.com (2023-07-21)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-07-21)

Congratulations Khalil! The VRP Panel has decided to award you $1,000 for this report given that this issue isn't remote exploitable and there are a significant amount of user gestures required to trigger this issue. As always, we appreciate your efforts in reporting this issue to us. 

### am...@google.com (2023-07-22)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-31)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-08-31)

This issue was migrated from crbug.com/chromium/1426517?no_tracker_redirect=1

[Monorail blocking: b/283720524]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40063713)*
