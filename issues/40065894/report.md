# Security: Heap-use-after-free in ui::PropertyHandler::GetPropertyInternal

| Field | Value |
|-------|-------|
| **Issue ID** | [40065894](https://issues.chromium.org/issues/40065894) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Views, UI>Browser>Sharing |
| **Platforms** | ChromeOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | af...@chromium.org |
| **Created** | 2023-06-16 |
| **Bounty** | $2,000.00 |

## Description

Chrome Version: 116.0.5831.0  

Operating System: ChromeOS

**REPRODUCTION CASE**

1. Run ./chrome --force-tablet-mode=touch\_view --touch-devices=1
2. Open chromium and open another tab then split screen with chromium windows
3. Click on Sharesheet in any window and select Neaby Share
4. Close the other window

=================================================================  

==14294==ERROR: AddressSanitizer: heap-use-after-free on address 0x5150006bc230 at pc 0x555f2108a4ae bp 0x7fffa9555800 sp 0x7fffa95557f8  

READ of size 8 at 0x5150006bc230 thread T0 (chrome)  

==14294==WARNING: invalid path to external symbolizer!  

==14294==WARNING: Failed to use and restart external symbolizer!  

#0 0x555f2108a4ad in \_\_root ./../../buildtools/third\_party/libc++/trunk/include/\_\_tree:1102:59  

#1 0x555f2108a4ad in find<const void \*> ./../../buildtools/third\_party/libc++/trunk/include/\_\_tree:2487:45  

#2 0x555f2108a4ad in find ./../../buildtools/third\_party/libc++/trunk/include/map:1465:68  

#3 0x555f2108a4ad in ui::PropertyHandler::GetPropertyInternal(void const\*, long, bool) const ./../../ui/base/class\_property.cc:72:36  

#4 0x555f2664591c in GetTransientParent ./../../ui/wm/core/window\_util.cc:209:7  

#5 0x555f2664591c in wm::HasTransientAncestor(aura::Window const\*, aura::Window const\*) ./../../ui/wm/core/window\_util.cc:240:42  

#6 0x555f266391f6 in wm::TransientWindowManager::RestackTransientDescendants() ./../../ui/wm/core/transient\_window\_manager.cc:148:9  

#7 0x555f2606d1b7 in aura::Window::OnStackingChanged() ./../../ui/aura/window.cc:1119:14  

#8 0x555f26066d31 in aura::Window::StackChildRelativeTo(aura::Window\*, aura::Window\*, aura::Window::StackDirection) ./../../ui/aura/window.cc:1104:10  

#9 0x555f26632cfd in wm::FocusController::SetActiveWindow(wm::ActivationChangeObserver::ActivationReason, aura::Window\*, aura::Window\*, bool) ./../../ui/wm/core/focus\_controller.cc:373:5  

#10 0x555f26631e56 in wm::FocusController::WindowLostFocusFromDispositionChange(aura::Window\*, aura::Window\*) ./../../ui/wm/core/focus\_controller.cc:447:10  

#11 0x555f2606dd94 in aura::Window::NotifyWindowVisibilityChangedAtReceiver(aura::Window\*, bool) ./../../ui/aura/window.cc:1206:14  

#12 0x555f2606d952 in aura::Window::NotifyWindowVisibilityChangedDown(aura::Window\*, bool) ./../../ui/aura/window.cc:1212:8  

#13 0x555f2606c76f in aura::Window::NotifyWindowVisibilityChanged(aura::Window\*, bool) ./../../ui/aura/window.cc:1193:8  

#14 0x555f2606493f in aura::Window::SetVisibleInternal(bool) ./../../ui/aura/window.cc:1008:3  

#15 0x555f26492a88 in views::NativeWidgetAura::Close() ./../../ui/views/widget/native\_widget\_aura.cc:640:5  

#16 0x555f2642eb86 in views::Widget::CloseWithReason(views::Widget::ClosedReason) ./../../ui/views/widget/widget.cc:769:21  

#17 0x555f342d2c33 in Browser::TabStripEmpty() ./../../chrome/browser/ui/browser.cc:1312:12  

#18 0x555f3444c5ee in TabStripModel::SendDetachWebContentsNotifications(TabStripModel::DetachNotifications\*) ./../../chrome/browser/ui/tabs/tab\_strip\_model.cc:544:16  

#19 0x555f34452355 in TabStripModel::CloseTabs(base::span<content::WebContents\* const, 18446744073709551615ul>, unsigned int) ./../../chrome/browser/ui/tabs/tab\_strip\_model.cc:1883:5  

#20 0x555f34452e1e in TabStripModel::CloseWebContentsAt(int, unsigned int) ./../../chrome/browser/ui/tabs/tab\_strip\_model.cc:720:10  

#21 0x555f34329abc in chrome::CloseWebContents(Browser\*, content::WebContents\*, bool) ./../../chrome/browser/ui/browser\_tabstrip.cc:98:31  

#22 0x555f1176f5a3 in Run ./../../base/functional/callback.h:152:12  

#23 0x555f1176f5a3 in blink::mojom::LocalMainFrame\_ClosePage\_ForwardToCallback::Accept(mojo::Message\*) ./gen/third\_party/blink/public/mojom/frame/frame.mojom.cc:17194:26  

#24 0x555f2031142a in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/interface\_endpoint\_client.cc:1011:41  

#25 0x555f20329980 in mojo::MessageDispatcher::Accept(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/message\_dispatcher.cc:43:19  

#26 0x555f20315bae in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/interface\_endpoint\_client.cc:701:20  

#27 0x555f224006eb in IPC::(anonymous namespace)::ChannelAssociatedGroupController::AcceptOnEndpointThread(mojo::Message) ./../../ipc/ipc\_mojo\_bootstrap.cc:1069:24  

#28 0x555f223f90cd in Invoke<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message), scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message> ./../../base/functional/bind\_internal.h:746:12  

#29 0x555f223f90cd in MakeItSo<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message), std::\_\_Cr::tuple<scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message> > ./../../base/functional/bind\_internal.h:925:12  

#30 0x555f223f90cd in RunImpl<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message), std::\_\_Cr::tuple<scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, 0UL, 1UL> ./../../base/functional/bind\_internal.h:1025:12  

#31 0x555f223f90cd in base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message), scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, void ()>::RunOnce(base::internal::BindStateBase\*) ./../../base/functional/bind\_internal.h:976:12  

#32 0x555f1eb53efa in Run ./../../base/functional/callback.h:152:12  

#33 0x555f1eb53efa in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task\_annotator.cc:186:34  

#34 0x555f1eb9fe02 in RunTask<(lambda at ../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:488:11)> ./../../base/task/common/task\_annotator.h:89:5  

#35 0x555f1eb9fe02 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow\*) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:486:23  

#36 0x555f1eb9eef1 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:351:41  

#37 0x555f1eba11e4 in non-virtual thunk to base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:0:0  

#38 0x555f1eccd917 in base::MessagePumpLibevent::Run(base::MessagePump::Delegate\*) ./../../base/message\_loop/message\_pump\_libevent.cc:290:55  

#39 0x555f1eba1c78 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:651:12  

#40 0x555f1eade752 in base::RunLoop::Run(base::Location const&) ./../../base/run\_loop.cc:134:14  

#41 0x555f1604436a in content::BrowserMainLoop::RunMainMessageLoop() ./../../content/browser/browser\_main\_loop.cc:1067:18  

#42 0x555f16049a96 in content::BrowserMainRunnerImpl::Run() ./../../content/browser/browser\_main\_runner\_impl.cc:158:15  

#43 0x555f1603db87 in content::BrowserMain(content::MainFunctionParams) ./../../content/browser/browser\_main.cc:34:28  

#44 0x555f1d01d4da in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate\*) ./../../content/app/content\_main\_runner\_impl.cc:686:10  

#45 0x555f1d0209f3 in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) ./../../content/app/content\_main\_runner\_impl.cc:1263:10  

#46 0x555f1d0203e0 in content::ContentMainRunnerImpl::Run() ./../../content/app/content\_main\_runner\_impl.cc:1117:12  

#47 0x555f1d01ae58 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner\*) ./../../content/app/content\_main.cc:326:36  

#48 0x555f1d01b2eb in content::ContentMain(content::ContentMainParams) ./../../content/app/content\_main.cc:343:10  

#49 0x555f0d2fd843 in ChromeMain ./../../chrome/app/chrome\_main.cc:187:12  

#50 0x7f1d66f4d0b2 in \_\_libc\_start\_main /build/glibc-sMfBJT/glibc-2.31/csu/../csu/libc-start.c:308:16

0x5150006bc230 is located 176 bytes inside of 504-byte region [0x5150006bc180,0x5150006bc378)  

freed by thread T0 (chrome) here:  

#0 0x555f0d2fba2d in operator delete(void\*) *asan\_rtl*:3  

#1 0x555f264975f1 in views::NativeWidgetAura::~NativeWidgetAura() ./../../ui/views/widget/native\_widget\_aura.cc:0:0  

#2 0x555f26497951 in views::NativeWidgetAura::~NativeWidgetAura() ./../../ui/views/widget/native\_widget\_aura.cc:1226:39  

#3 0x555f264294d4 in operator() ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:65:5  

#4 0x555f264294d4 in reset ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:297:7  

#5 0x555f264294d4 in views::Widget::~Widget() ./../../ui/views/widget/widget.cc:196:26  

#6 0x555f2642a269 in views::Widget::~Widget() ./../../ui/views/widget/widget.cc:192:19  

#7 0x555f221b31ff in operator() ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:65:5  

#8 0x555f221b31ff in reset ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:297:7  

#9 0x555f221b31ff in ash::BackdropController::Hide(bool, bool) ./../../ash/wm/workspace/backdrop\_controller.cc:570:15  

#10 0x555f221b3f35 in ash::BackdropController::UpdateBackdropInternal() ./../../ash/wm/workspace/backdrop\_controller.cc:416:5  

#11 0x555f2606d1b7 in aura::Window::OnStackingChanged() ./../../ui/aura/window.cc:1119:14  

#12 0x555f26066d31 in aura::Window::StackChildRelativeTo(aura::Window\*, aura::Window\*, aura::Window::StackDirection) ./../../ui/aura/window.cc:1104:10  

#13 0x555f22119dda in ash::SplitViewDivider::RefreshStackingOrder() ./../../ash/wm/splitview/split\_view\_divider.cc:318:24  

#14 0x555f2211a89a in ash::SplitViewDivider::OnWindowStackingChanged(aura::Window\*) ./../../ash/wm/splitview/split\_view\_divider.cc:216:3  

#15 0x555f2606d1b7 in aura::Window::OnStackingChanged() ./../../ui/aura/window.cc:1119:14  

#16 0x555f26066d31 in aura::Window::StackChildRelativeTo(aura::Window\*, aura::Window\*, aura::Window::StackDirection) ./../../ui/aura/window.cc:1104:10  

#17 0x555f266392c0 in wm::TransientWindowManager::RestackTransientDescendants() ./../../ui/wm/core/transient\_window\_manager.cc:153:15  

#18 0x555f2606d1b7 in aura::Window::OnStackingChanged() ./../../ui/aura/window.cc:1119:14  

#19 0x555f26066d31 in aura::Window::StackChildRelativeTo(aura::Window\*, aura::Window\*, aura::Window::StackDirection) ./../../ui/aura/window.cc:1104:10  

#20 0x555f26632cfd in wm::FocusController::SetActiveWindow(wm::ActivationChangeObserver::ActivationReason, aura::Window\*, aura::Window\*, bool) ./../../ui/wm/core/focus\_controller.cc:373:5  

#21 0x555f26631e56 in wm::FocusController::WindowLostFocusFromDispositionChange(aura::Window\*, aura::Window\*) ./../../ui/wm/core/focus\_controller.cc:447:10  

#22 0x555f2606dd94 in aura::Window::NotifyWindowVisibilityChangedAtReceiver(aura::Window\*, bool) ./../../ui/aura/window.cc:1206:14  

#23 0x555f2606d952 in aura::Window::NotifyWindowVisibilityChangedDown(aura::Window\*, bool) ./../../ui/aura/window.cc:1212:8  

#24 0x555f2606c76f in aura::Window::NotifyWindowVisibilityChanged(aura::Window\*, bool) ./../../ui/aura/window.cc:1193:8  

#25 0x555f2606493f in aura::Window::SetVisibleInternal(bool) ./../../ui/aura/window.cc:1008:3  

#26 0x555f26492a88 in views::NativeWidgetAura::Close() ./../../ui/views/widget/native\_widget\_aura.cc:640:5  

#27 0x555f2642eb86 in views::Widget::CloseWithReason(views::Widget::ClosedReason) ./../../ui/views/widget/widget.cc:769:21  

#28 0x555f342d2c33 in Browser::TabStripEmpty() ./../../chrome/browser/ui/browser.cc:1312:12  

#29 0x555f3444c5ee in TabStripModel::SendDetachWebContentsNotifications(TabStripModel::DetachNotifications\*) ./../../chrome/browser/ui/tabs/tab\_strip\_model.cc:544:16  

#30 0x555f34452355 in TabStripModel::CloseTabs(base::span<content::WebContents\* const, 18446744073709551615ul>, unsigned int) ./../../chrome/browser/ui/tabs/tab\_strip\_model.cc:1883:5  

#31 0x555f34452e1e in TabStripModel::CloseWebContentsAt(int, unsigned int) ./../../chrome/browser/ui/tabs/tab\_strip\_model.cc:720:10  

#32 0x555f34329abc in chrome::CloseWebContents(Browser\*, content::WebContents\*, bool) ./../../chrome/browser/ui/browser\_tabstrip.cc:98:31  

#33 0x555f1176f5a3 in Run ./../../base/functional/callback.h:152:12  

#34 0x555f1176f5a3 in blink::mojom::LocalMainFrame\_ClosePage\_ForwardToCallback::Accept(mojo::Message\*) ./gen/third\_party/blink/public/mojom/frame/frame.mojom.cc:17194:26

previously allocated by thread T0 (chrome) here:  

#0 0x555f0d2fb1cd in operator new(unsigned long) *asan\_rtl*:3  

#1 0x555f2648dca2 in views::NativeWidgetAura::NativeWidgetAura(views::internal::NativeWidgetDelegate\*) ./../../ui/views/widget/native\_widget\_aura.cc:128:15  

#2 0x555f26497a85 in views::internal::NativeWidgetPrivate::CreateNativeWidget(views::internal::NativeWidgetDelegate\*) ./../../ui/views/widget/native\_widget\_aura.cc:1295:14  

#3 0x555f264282cd in CreateNativeWidget ./../../ui/views/widget/widget.cc:90:10  

#4 0x555f264282cd in views::Widget::Init(views::Widget::InitParams) ./../../ui/views/widget/widget.cc:428:7  

#5 0x555f221b5404 in ash::BackdropController::EnsureBackdropWidget() ./../../ash/wm/workspace/backdrop\_controller.cc:447:14  

#6 0x555f221b3f0d in ash::BackdropController::UpdateBackdropInternal() ./../../ash/wm/workspace/backdrop\_controller.cc:423:3  

#7 0x555f220808ab in ash::OverviewController::OnEndingAnimationComplete(bool) ./../../ash/wm/overview/overview\_controller.cc:537:14  

#8 0x555f220803f9 in ash::OverviewController::RemoveAndDestroyExitAnimationObserver(ash::DelayedAnimationObserver\*) ./../../ash/wm/overview/overview\_controller.cc:234:5  

#9 0x555f261188ec in ui::LayerAnimationObserver::DetachedFromSequence(ui::LayerAnimationSequence\*, bool) ./../../ui/compositor/layer\_animation\_observer.cc:55:5  

#10 0x555f26118e5c in ui::ImplicitAnimationObserver::OnLayerAnimationEnded(ui::LayerAnimationSequence\*) ./../../ui/compositor/layer\_animation\_observer.cc:89:13  

#11 0x555f2611c50e in ui::LayerAnimationSequence::NotifyEnded() ./../../ui/compositor/layer\_animation\_sequence.cc:290:14  

#12 0x555f26129111 in ProgressAnimationToEnd ./../../ui/compositor/layer\_animator.cc:486:13  

#13 0x555f26129111 in ui::LayerAnimator::FinishAnimation(ui::LayerAnimationSequence\*, bool) ./../../ui/compositor/layer\_animator.cc:638:5  

#14 0x555f2612b669 in ui::LayerAnimator::Step(base::TimeTicks) ./../../ui/compositor/layer\_animator.cc:517:7  

#15 0x555f2613456b in ui::LayerAnimatorCollection::OnAnimationStep(base::TimeTicks) ./../../ui/compositor/layer\_animator\_collection.cc:56:16  

#16 0x555f260c32bd in ui::Compositor::BeginMainFrame(viz::BeginFrameArgs const&) ./../../ui/compositor/compositor.cc:727:14  

#17 0x555f2500531d in cc::SingleThreadProxy::DoBeginMainFrame(viz::BeginFrameArgs const&) ./../../cc/trees/single\_thread\_proxy.cc:1107:21  

#18 0x555f25007015 in cc::SingleThreadProxy::BeginMainFrame(viz::BeginFrameArgs const&) ./../../cc/trees/single\_thread\_proxy.cc:1064:3  

#19 0x555f250097b7 in Invoke<void (cc::SingleThreadProxy::\*)(const viz::BeginFrameArgs &), const base::WeakPtr[cc::SingleThreadProxy](javascript:void(0);) &, viz::BeginFrameArgs> ./../../base/functional/bind\_internal.h:746:12  

#20 0x555f250097b7 in MakeItSo<void (cc::SingleThreadProxy::\*)(const viz::BeginFrameArgs &), std::\_\_Cr::tuple<base::WeakPtr[cc::SingleThreadProxy](javascript:void(0);), viz::BeginFrameArgs> > ./../../base/functional/bind\_internal.h:953:5  

#21 0x555f250097b7 in RunImpl<void (cc::SingleThreadProxy::\*)(const viz::BeginFrameArgs &), std::\_\_Cr::tuple<base::WeakPtr[cc::SingleThreadProxy](javascript:void(0);), viz::BeginFrameArgs>, 0UL, 1UL> ./../../base/functional/bind\_internal.h:1025:12  

#22 0x555f250097b7 in base::internal::Invoker<base::internal::BindState<void (cc::SingleThreadProxy::\*)(viz::BeginFrameArgs const&), base::WeakPtr[cc::SingleThreadProxy](javascript:void(0);), viz::BeginFrameArgs>, void ()>::RunOnce(base::internal::BindStateBase\*) ./../../base/functional/bind\_internal.h:976:12  

#23 0x555f1eb53efa in Run ./../../base/functional/callback.h:152:12  

#24 0x555f1eb53efa in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task\_annotator.cc:186:34  

#25 0x555f1eb9fe02 in RunTask<(lambda at ../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:488:11)> ./../../base/task/common/task\_annotator.h:89:5  

#26 0x555f1eb9fe02 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow\*) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:486:23  

#27 0x555f1eb9eef1 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:351:41  

#28 0x555f1eba11e4 in non-virtual thunk to base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:0:0  

#29 0x555f1eccd917 in base::MessagePumpLibevent::Run(base::MessagePump::Delegate\*) ./../../base/message\_loop/message\_pump\_libevent.cc:290:55  

#30 0x555f1eba1c78 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:651:12  

#31 0x555f1eade752 in base::RunLoop::Run(base::Location const&) ./../../base/run\_loop.cc:134:14  

#32 0x555f1604436a in content::BrowserMainLoop::RunMainMessageLoop() ./../../content/browser/browser\_main\_loop.cc:1067:18  

#33 0x555f16049a96 in content::BrowserMainRunnerImpl::Run() ./../../content/browser/browser\_main\_runner\_impl.cc:158:15  

#34 0x555f1603db87 in content::BrowserMain(content::MainFunctionParams) ./../../content/browser/browser\_main.cc:34:28  

#35 0x555f1d01d4da in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate\*) ./../../content/app/content\_main\_runner\_impl.cc:686:10  

#36 0x555f1d0209f3 in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) ./../../content/app/content\_main\_runner\_impl.cc:1263:10

SUMMARY: AddressSanitizer: heap-use-after-free (/home/lbstyle/Desktop/asan-linux-release-1157331/chrome+0x264f64ad) (BuildId: f4552bedf3531ef3)  

Shadow bytes around the buggy address:  

0x5150006bbf80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x5150006bc000: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x5150006bc080: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x5150006bc100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x5150006bc180: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

=>0x5150006bc200: fd fd fd fd fd fd[fd]fd fd fd fd fd fd fd fd fd  

0x5150006bc280: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x5150006bc300: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fa  

0x5150006bc380: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x5150006bc400: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x5150006bc480: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

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

==14294==ADDITIONAL INFO

## Attachments

- [screen.webm](attachments/screen.webm) (video/webm, 8.4 MB)

## Timeline

### [Deleted User] (2023-06-16)

[Empty comment from Monorail migration]

### dc...@chromium.org (2023-06-16)

I've confirmed this locally in M114. Medium despite being a use-after-free due to the user interactions required.

afakhry, I'm not sure if you're the best owner since I'm not sure if this is ultimately a problem in the ash wm or the nearby code; if this is more an issue with nearby sharing, please feel free to pass it off.

[Monorail components: Internals>Views UI>Browser>Sharing]

### [Deleted User] (2023-06-16)

[Empty comment from Monorail migration]

### af...@chromium.org (2023-06-16)

copybara-migrate-c-1252584

### ad...@google.com (2023-06-16)

(I am a bot: this is an auto-cc on a security bug)

### af...@chromium.org (2023-06-16)

copybara-migrate-c-1253075

### af...@chromium.org (2023-06-16)

[Empty comment from Monorail migration]

### af...@chromium.org (2023-06-16)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-17)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@google.com (2023-06-19)

Your report will be worked on in the Buganizer system (link: https://issuetracker.google.com/issues/287904584). You have been cc'ed on that report and should have access to it at this time to follow along while it is being worked on. We are setting Security_Severity-High as a default and the priority may either increase or decrease once their report is fully triaged and analyzed.

[Monorail blocking: b/287904584]

### ch...@gmail.com (2023-06-22)

Fixed on 117.0.5846.0.

### ch...@gmail.com (2023-06-27)

Should this be marked as fixed? 

### ch...@gmail.com (2023-07-05)

Friendly ping.

### ch...@google.com (2023-07-17)

Marked as fixed since fix got verified (https://crbug.com/chromium/1455270#c4 buganizer)

### [Deleted User] (2023-07-17)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-17)

[Empty comment from Monorail migration]

### am...@google.com (2023-07-27)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-07-27)

Congratulations Khalil! The VRP Panel has decided to award you $2,000 for this report of a heavily mitigated security bug. Thank you for your efforts and reporting this issue to us!

### am...@google.com (2023-07-28)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-23)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1455270?no_tracker_redirect=1

[Multiple monorail components: Internals>Views, UI>Browser>Sharing]
[Monorail blocking: b/287904584]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40065894)*
