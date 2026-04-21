# Security: container-overflow in ui::Compositor::StopThroughtputTracker

| Field | Value |
|-------|-------|
| **Issue ID** | [40059416](https://issues.chromium.org/issues/40059416) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Compositing |
| **Platforms** | ChromeOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | xi...@chromium.org |
| **Created** | 2022-04-19 |
| **Bounty** | $3,000.00 |

## Description

Chromium 103.0.5010.0 Ozone build 


I reproduced this crash When I closed two chromium windows from two desks. I'm still trying to get specific steps.

=================================================================
==104810==ERROR: AddressSanitizer: container-overflow on address 0x61300012cb69 at pc 0x555fb103dbd6 bp 0x7ffc4fb8b7b0 sp 0x7ffc4fb8b7a8
READ of size 1 at 0x61300012cb69 thread T0 (chrome)
==104810==WARNING: invalid path to external symbolizer!
==104810==WARNING: Failed to use and restart external symbolizer!
    #0 0x555fb103dbd5 in ui::Compositor::StopThroughtputTracker(unsigned long) ./../../ui/compositor/compositor.cc:825:18
    #1 0x555fb8955b27 in TabHoverCardController::OnFadeAnimationEnded(views::WidgetFadeAnimator*, views::WidgetFadeAnimator::FadeType) ./../../chrome/browser/ui/views/tabs/tab_hover_card_controller.cc:695:13
    #2 0x555fb89620fa in Run ./../../base/callback.h:241:12
    #3 0x555fb89620fa in RunCallback<views::WidgetFadeAnimator *&, const views::WidgetFadeAnimator::FadeType &> ./../../base/callback_list.h:329:9
    #4 0x555fb89620fa in void base::internal::CallbackListBase<base::RepeatingCallbackList<void (views::WidgetFadeAnimator*, views::WidgetFadeAnimator::FadeType)> >::Notify<views::WidgetFadeAnimator*, views::WidgetFadeAnimator::FadeType const&>(views::WidgetFadeAnimator*&&, views::WidgetFadeAnimator::FadeType const&) ./../../base/callback_list.h:219:47
    #5 0x555fb8961e8d in views::WidgetFadeAnimator::AnimationEnded(gfx::Animation const*) ./../../ui/views/animation/widget_fade_animator.cc:92:28
    #6 0x555fb896235f in views::WidgetFadeAnimator::OnWidgetDestroying(views::Widget*) ./../../ui/views/animation/widget_fade_animator.cc:97:19
    #7 0x555fb1431c25 in views::Widget::OnNativeWidgetDestroying() ./../../ui/views/widget/widget.cc:1415:14
    #8 0x555fb1476f8d in views::NativeWidgetAura::OnWindowDestroying(aura::Window*) ./../../ui/views/widget/native_widget_aura.cc:956:14
    #9 0x555fb0fe1d04 in aura::Window::~Window() ./../../ui/aura/window.cc:193:16
    #10 0x555fb0fe322f in aura::Window::~Window() ./../../ui/aura/window.cc:184:19
    #11 0x555fab752466 in Run ./../../base/callback.h:142:12
    #12 0x555fab752466 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task_annotator.cc:135:32
    #13 0x555fab793bad in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:388:29)> ./../../base/task/common/task_annotator.h:74:5
    #14 0x555fab793bad in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:386:21
    #15 0x555fab7932c7 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:291:41
    #16 0x555fab794881 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0:0
    #17 0x555fab89b93c in base::MessagePumpLibevent::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_libevent.cc:195:55
    #18 0x555fab794f39 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:498:12
    #19 0x555fab6cc02c in base::RunLoop::Run(base::Location const&) ./../../base/run_loop.cc:141:14
    #20 0x555fa1cc268a in content::BrowserMainLoop::RunMainMessageLoop() ./../../content/browser/browser_main_loop.cc:1067:18
    #21 0x555fa1cc6b71 in content::BrowserMainRunnerImpl::Run() ./../../content/browser/browser_main_runner_impl.cc:155:15
    #22 0x555fa1cbc86a in content::BrowserMain(content::MainFunctionParams) ./../../content/browser/browser_main.cc:30:28
    #23 0x555fab4a891f in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:640:10
    #24 0x555fab4ab47f in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) ./../../content/app/content_main_runner_impl.cc:1147:10
    #25 0x555fab4aa8b8 in content::ContentMainRunnerImpl::Run() ./../../content/app/content_main_runner_impl.cc:1019:12
    #26 0x555fab4a5081 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) ./../../content/app/content_main.cc:407:36
    #27 0x555fab4a5708 in content::ContentMain(content::ContentMainParams) ./../../content/app/content_main.cc:435:10
    #28 0x555f9cfd786a in ChromeMain ./../../chrome/app/chrome_main.cc:176:12
    #29 0x7f4e6b2f50b2 in __libc_start_main /build/glibc-sMfBJT/glibc-2.31/csu/../csu/libc-start.c:308:16

0x61300012cb69 is located 105 bytes inside of 384-byte region [0x61300012cb00,0x61300012cc80)
allocated by thread T0 (chrome) here:
    #0 0x555f9cfd508d in operator new(unsigned long) _asan_rtl_:3
    #1 0x555fb1041a8b in __libcpp_operator_new<unsigned long> ./../../buildtools/third_party/libc++/trunk/include/new:235:10
    #2 0x555fb1041a8b in __libcpp_allocate ./../../buildtools/third_party/libc++/trunk/include/new:261:10
    #3 0x555fb1041a8b in allocate ./../../buildtools/third_party/libc++/trunk/include/__memory/allocator.h:82:38
    #4 0x555fb1041a8b in allocate ./../../buildtools/third_party/libc++/trunk/include/__memory/allocator_traits.h:261:20
    #5 0x555fb1041a8b in std::__1::__split_buffer<std::__1::pair<unsigned long, ui::Compositor::TrackerState>, std::__1::allocator<std::__1::pair<unsigned long, ui::Compositor::TrackerState> >&>::__split_buffer(unsigned long, unsigned long, std::__1::allocator<std::__1::pair<unsigned long, ui::Compositor::TrackerState> >&) ./../../buildtools/third_party/libc++/trunk/include/__split_buffer:314:29
    #6 0x555fb104140a in std::__1::__wrap_iter<std::__1::pair<unsigned long, ui::Compositor::TrackerState>*> std::__1::vector<std::__1::pair<unsigned long, ui::Compositor::TrackerState>, std::__1::allocator<std::__1::pair<unsigned long, ui::Compositor::TrackerState> > >::emplace<unsigned long const&, ui::Compositor::TrackerState>(std::__1::__wrap_iter<std::__1::pair<unsigned long, ui::Compositor::TrackerState> const*>, unsigned long const&, ui::Compositor::TrackerState&&) ./../../buildtools/third_party/libc++/trunk/include/vector:1862:53
    #7 0x555fb103d916 in unsafe_emplace<const unsigned long &, ui::Compositor::TrackerState> ./../../base/containers/flat_tree.h:1048:16
    #8 0x555fb103d916 in base::flat_map<unsigned long, ui::Compositor::TrackerState, std::__1::less<void>, std::__1::vector<std::__1::pair<unsigned long, ui::Compositor::TrackerState>, std::__1::allocator<std::__1::pair<unsigned long, ui::Compositor::TrackerState> > > >::operator[](unsigned long const&) ./../../base/containers/flat_map.h:284:19
    #9 0x555fb103d70f in ui::Compositor::StartThroughputTracker(unsigned long, base::OnceCallback<void (cc::FrameSequenceMetrics::CustomReportData const&)>) ./../../ui/compositor/compositor.cc:813:25
    #10 0x555fb10a649c in ui::ThroughputTracker::Start(base::OnceCallback<void (cc::FrameSequenceMetrics::CustomReportData const&)>) ./../../ui/compositor/throughput_tracker.cc:46:10
    #11 0x555fb1031caf in ui::AnimationThroughputReporter::AnimationTracker::MaybeStartTracking() ./../../ui/compositor/animation_throughput_reporter.cc:116:26
    #12 0x555fb10316e0 in ui::AnimationThroughputReporter::AnimationTracker::OnLayerAnimationStarted(ui::LayerAnimationSequence*) ./../../ui/compositor/animation_throughput_reporter.cc:81:7
    #13 0x555fb108890b in ui::LayerAnimationSequence::NotifyStarted() ./../../ui/compositor/layer_animation_sequence.cc:285:14
    #14 0x555fb1092190 in ui::LayerAnimator::StartSequenceImmediately(ui::LayerAnimationSequence*) ./../../ui/compositor/layer_animator.cc:902:15
    #15 0x555fb108e41e in ui::LayerAnimator::StartAnimation(ui::LayerAnimationSequence*) ./../../ui/compositor/layer_animator.cc:220:8
    #16 0x555fb108ee04 in ui::LayerAnimator::SetOpacity(float) ./../../ui/compositor/layer_animator.cc:114:1
    #17 0x555fb1941d6b in ash::ShelfView::FadeIn(views::View*) ./../../ash/shelf/shelf_view.cc:1482:18
    #18 0x555fb127ba01 in views::BoundsAnimator::AnimationEndedOrCanceled(gfx::Animation const*, views::BoundsAnimator::AnimationEndType) ./../../ui/views/animation/bounds_animator.cc:0:0
    #19 0x555face2a359 in gfx::LinearAnimation::Step(base::TimeTicks) ./../../ui/gfx/animation/linear_animation.cc:88:5
    #20 0x555face279ab in gfx::AnimationContainer::Run(base::TimeTicks) ./../../ui/gfx/animation/animation_container.cc:99:13
    #21 0x555face290df in Run ./../../base/callback.h:241:12
    #22 0x555face290df in gfx::AnimationRunner::Step(base::TimeTicks) ./../../ui/gfx/animation/animation_runner.cc:78:9
    #23 0x555fb103af83 in ui::Compositor::BeginMainFrame(viz::BeginFrameArgs const&) ./../../ui/compositor/compositor.cc:691:14
    #24 0x555fade7d3a9 in cc::SingleThreadProxy::DoBeginMainFrame(viz::BeginFrameArgs const&) ./../../cc/trees/single_thread_proxy.cc:1048:21
    #25 0x555fade7edec in cc::SingleThreadProxy::BeginMainFrame(viz::BeginFrameArgs const&) ./../../cc/trees/single_thread_proxy.cc:1010:3
    #26 0x555fade809cb in Invoke<void (cc::SingleThreadProxy::*)(const viz::BeginFrameArgs &), base::WeakPtr<cc::SingleThreadProxy>, viz::BeginFrameArgs> ./../../base/bind_internal.h:542:12
    #27 0x555fade809cb in MakeItSo<void (cc::SingleThreadProxy::*)(const viz::BeginFrameArgs &), base::WeakPtr<cc::SingleThreadProxy>, viz::BeginFrameArgs> ./../../base/bind_internal.h:726:5
    #28 0x555fade809cb in RunImpl<void (cc::SingleThreadProxy::*)(const viz::BeginFrameArgs &), std::__1::tuple<base::WeakPtr<cc::SingleThreadProxy>, viz::BeginFrameArgs>, 0UL, 1UL> ./../../base/bind_internal.h:779:12
    #29 0x555fade809cb in base::internal::Invoker<base::internal::BindState<void (cc::SingleThreadProxy::*)(viz::BeginFrameArgs const&), base::WeakPtr<cc::SingleThreadProxy>, viz::BeginFrameArgs>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/bind_internal.h:748:12
    #30 0x555fab752466 in Run ./../../base/callback.h:142:12
    #31 0x555fab752466 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task_annotator.cc:135:32
    #32 0x555fab793bad in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:388:29)> ./../../base/task/common/task_annotator.h:74:5
    #33 0x555fab793bad in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:386:21
    #34 0x555fab7932c7 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:291:41
    #35 0x555fab794881 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0:0
    #36 0x555fab89b93c in base::MessagePumpLibevent::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_libevent.cc:195:55
    #37 0x555fab794f39 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:498:12
    #38 0x555fab6cc02c in base::RunLoop::Run(base::Location const&) ./../../base/run_loop.cc:141:14
    #39 0x555fa1cc268a in content::BrowserMainLoop::RunMainMessageLoop() ./../../content/browser/browser_main_loop.cc:1067:18
    #40 0x555fa1cc6b71 in content::BrowserMainRunnerImpl::Run() ./../../content/browser/browser_main_runner_impl.cc:155:15

HINT: if you don't care about these errors you may set ASAN_OPTIONS=detect_container_overflow=0.
If you suspect a false positive see also: https://github.com/google/sanitizers/wiki/AddressSanitizerContainerOverflow.
SUMMARY: AddressSanitizer: container-overflow (/home/lbstyle/asan-linux-release-991831/chrome+0x22349bd5) (BuildId: cb3cce5833f729b9)
Shadow bytes around the buggy address:
  0x0c268001d910: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c268001d920: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd
  0x0c268001d930: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c268001d940: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c268001d950: fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa
=>0x0c268001d960: 00 00 00 00 00 00 00 00 00 00 00 00 fc[fc]fc fc
  0x0c268001d970: fc fc fc fc fc fc fc fc fc fc fc fc fc fc fc fc
  0x0c268001d980: fc fc fc fc fc fc fc fc fc fc fc fc fc fc fc fc
  0x0c268001d990: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd
  0x0c268001d9a0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c268001d9b0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb



## Attachments

- [screen.webm](attachments/screen.webm) (video/webm, 3.2 MB)
- [chrome log](attachments/chrome log) (text/plain, 30.9 KB)

## Timeline

### [Deleted User] (2022-04-19)

[Empty comment from Monorail migration]

### ts...@chromium.org (2022-04-19)

Assigning to author of StopThroughtputTracker (note the stray T in Throuhtput) on the chance that there is enough information in the ASAN trace to deduce what is happening. Otherwise, Khalil, we'd need a poc.

[Monorail components: Internals>Compositing]

### ch...@gmail.com (2022-04-20)

I can repro it again.

1. Open https://lbstyle.github.io/back.html in Desk_1
2. Open https://lbstyle.github.io/back.html in Desk_2 
3. "https://lbstyle.github.io/back.html" page will open https://lbstyle.github.io/alert.html after a few seconds
4. Keep moving mouse pointer into the tab strip of https://lbstyle.github.io/back.html triggering the hovercard as shown in the video.

### ts...@chromium.org (2022-04-21)

Note that I wasn't able to repro due to the dual desk setup required, so it is hard to say which versions are affected.

### xi...@chromium.org (2022-04-26)

On it. It is likely that we are trying to stop an already canceled tracker.

### xi...@chromium.org (2022-04-26)

I could not repro the issue. The problem is that the entry in `throughput_tracker_map_` is removed when `StopThroughtputTracker` is called. Currently, this is protected by a DCHECK and I could not get it to happen and I could not repro with an asan build either.

Khalil, I wonder whether you could try the following debug CL and pass me the log. Thanks.
  https://chromium-review.googlesource.com/c/chromium/src/+/3609053

### xi...@chromium.org (2022-04-26)

[Empty comment from Monorail migration]

### ch...@gmail.com (2022-04-27)

Sorry for the delay.

I'm on vacation this week. I don't have a machine that can support chromium build right now.

### xi...@chromium.org (2022-04-27)

No worries. I'll keep trying on my end. I would like to understand more about the problem as it should not be happening.

### ch...@gmail.com (2022-04-28)

#0 0x7f2dd6c7a9cf base::debug::CollectStackTrace()
#1 0x7f2dd69f68ca base::debug::StackTrace::StackTrace()
#2 0x7f2dd69f6885 base::debug::StackTrace::StackTrace()
#3 0x7f2dd6a40617 logging::LogMessage::~LogMessage()
#4 0x7f2dd6a40df9 logging::LogMessage::~LogMessage()
#5 0x7f2dd69b2deb logging::CheckError::~CheckError()
#6 0x7f2dc5a743e3 views::WidgetFadeAnimator::FadeOut()
#7 0x55878ecbdc7e TabHoverCardController::HideHoverCard()
#8 0x55878ecbd53e TabHoverCardController::UpdateHoverCard()
#9 0x55878ecd3801 TabContainer::UpdateHoverCard()
#10 0x55878ecac09a TabStrip::UpdateHoverCard()
#11 0x55878eca9c40 TabStrip::SetSelection()
#12 0x55878ec70e8d BrowserTabStripController::OnTabStripModelChanged()
#13 0x55878de66024 TabStripModel::InsertWebContentsAtImpl()
#14 0x55878de6c6a2 TabStripModel::AddWebContents()
#15 0x55878dda2d62 Navigate()
#16 0x55878ddaa3e6 chrome::AddWebContents()
#17 0x55878dd5e468 Browser::AddNewContents()
#18 0x55878dd5e4e7 Browser::AddNewContents()
#19 0x7f2db5f45f50 content::WebContentsImpl::ShowCreatedWindow()
#20 0x7f2db5a5677a content::RenderFrameHostImpl::ShowCreatedWindow()
#21 0x7f2dca26f398 blink::mojom::LocalMainFrameHostStubDispatch::AcceptWithResponder()
#22 0x7f2db5a9f2a9 blink::mojom::LocalMainFrameHostStub<>::AcceptWithResponder()
#23 0x7f2dd45b63ef mojo::InterfaceEndpointClient::HandleValidatedMessage()
#24 0x7f2dd45b6029 mojo::InterfaceEndpointClient::HandleIncomingMessageThunk::Accept()
#25 0x7f2dd45cc467 mojo::MessageDispatcher::Accept()
#26 0x7f2dd45b8171 mojo::InterfaceEndpointClient::HandleIncomingMessage()
#27 0x7f2dd20ec00a IPC::(anonymous namespace)::ChannelAssociatedGroupController::AcceptOnEndpointThread()
#28 0x7f2dd20e1e96 base::internal::FunctorTraits<>::Invoke<>()
#29 0x7f2dd20e1d5c base::internal::InvokeHelper<>::MakeItSo<>()
#30 0x7f2dd20e1d0e _ZN4base8internal7InvokerINS0_9BindStateIMN3IPC12_GLOBAL__N_132ChannelAssociatedGroupControllerEFvN4mojo7MessageEEJ13scoped_refptrIS5_ES7_EEEFvvEE7RunImplIS9_NSt4__Cr5tupleIJSB_S7_EEEJLm0ELm1EEEEvOT_OT0_NSG_16integer_sequenceImJXspT1_EEEE
#31 0x7f2dd20e1c57 base::internal::Invoker<>::RunOnce()
#32 0x7f2dd69a7e49 _ZNO4base12OnceCallbackIFvvEE3RunEv
#33 0x7f2dd6b75dae base::TaskAnnotator::RunTaskImpl()
#34 0x7f2dd6bc8030 base::TaskAnnotator::RunTask<>()
#35 0x7f2dd6bc7df5 base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl()
#36 0x7f2dd6bc751e base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()
#37 0x7f2dd6bc7fb0 base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()
#38 0x7f2dd6ce12e7 base::MessagePumpLibevent::Run()
#39 0x7f2dd6bc8532 base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run()
#40 0x7f2dd6b0a739 base::RunLoop::Run()
#41 0x7f2db4d29acc content::BrowserMainLoop::RunMainMessageLoop()
#42 0x7f2db4d35b0f content::BrowserMainRunnerImpl::Run()
#43 0x7f2db4d2581e content::BrowserMain()
#44 0x7f2db7383e89 content::RunBrowserProcessMain()
#45 0x7f2db73859bc content::ContentMainRunnerImpl::RunBrowser()
#46 0x7f2db7385263 content::ContentMainRunnerImpl::Run()
#47 0x7f2db7381d7d content::RunContentProcess()
#48 0x7f2db73826e2 content::ContentMain()
#49 0x558781917fa1 ChromeMain
#50 0x558781917e12 main
#51 0x7f2d73f580b3 __libc_start_main
#52 0x558781917d2a _start
Task trace:
#0 0x7f2dd20e132c IPC::(anonymous namespace)::ChannelAssociatedGroupController::Accept()
#1 0x7f2dd44e8f5d mojo::SimpleWatcher::Context::Notify()
Crash keys:
  "ui_scheduler_async_stack" = "0x7F2DD20E132C 0x7F2DD44E8F5D"
  "io_scheduler_async_stack" = "0x7F2DD44E8F5D 0x0"

Trace/breakpoint trap (core dumped)


### ch...@gmail.com (2022-04-28)

It was worth going back to get it done. Hope that helps :).

### xi...@chromium.org (2022-04-28)

Sorry for not being clear. I have seen that DCHECK in #10 but that is probably not cause of the ASAN problem. I am more interested to see the chrome logs with my CL (https://chromium-review.googlesource.com/c/chromium/src/+/3609053 in https://crbug.com/chromium/1317746#c6). The CL adds debugging logs to help me understand why we stop an already removed tracker.

Is it possible for you to help with that? You can cherry pick my CL to your check out. Press "D" on gerrit would show you the command line to do that.

Thanks.

### ch...@gmail.com (2022-04-29)

[Empty comment from Monorail migration]

### ch...@gmail.com (2022-04-29)

Is that what you need?

### xi...@chromium.org (2022-04-29)

Yes. Looks great. Thank you.

2022-04-29T06:59:54.030335Z ERROR chrome[681426:681426]: [compositor.cc(823)] #### Compositor::StopThroughtputTracker, tracker_id=85
2022-04-29T06:59:54.083245Z ERROR chrome[681426:681426]: [compositor.cc(902)] #### Compositor::ReportMetricsForTracker, tracker_id=85
2022-04-29T06:59:54.083988Z ERROR chrome[681426:681426]: [compositor.cc(823)] #### Compositor::StopThroughtputTracker, tracker_id=85

So the problem is that we are somehow stopped tracker "85" twice. 

### ch...@gmail.com (2022-04-29)

Sounds good. Thank you for the clarification and your patience with my late replies. 

### xi...@chromium.org (2022-04-29)

Pending CL: https://chromium-review.googlesource.com/c/chromium/src/+/3614045

### xi...@chromium.org (2022-04-29)

+flackr

### xi...@chromium.org (2022-05-03)

+dfried

### gi...@appspot.gserviceaccount.com (2022-05-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/43af2894f3f6408d9e960563a51e2a5c1b3e2bf3

commit 43af2894f3f6408d9e960563a51e2a5c1b3e2bf3
Author: Xiyuan Xia <xiyuan@google.com>
Date: Wed May 04 15:55:37 2022

Fix tab hover card overlapping animation edge case

There is one edge case that "TabHoverCardController::HideHoverCard
-> WidgetFadeAnimator::FadeOut" could be called with an active
fade in animation. WidgetFadeAnimator::Hide would directly close
the card widget in such case. However, there is an active
ui::ThroughputTracker because of the unfinished fade-in animation.
Stop() would be triggered twice in WidgetFadeAnimator::FadeOut
for the edge case. Once from `fade_complete_callbacks_.Notify`
and the other one from WidgetFadeAnimator::OnWidgetDestroying. The
2nd Stop() would cause a crash because the tracker is no longer
valid in ui::Compositor.

This CL fixes the crash by canceling the pending fade-in animation
and resets the tracker for the edge case.

Bug: 1317746
Change-Id: I4b726bc704e1d048949d21644c125129732d07c6
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3624098
Commit-Queue: Xiyuan Xia <xiyuan@chromium.org>
Reviewed-by: Peter Kasting <pkasting@chromium.org>
Reviewed-by: Dana Fried <dfried@chromium.org>
Cr-Commit-Position: refs/heads/main@{#999429}

[modify] https://crrev.com/43af2894f3f6408d9e960563a51e2a5c1b3e2bf3/ui/views/animation/widget_fade_animator.cc
[modify] https://crrev.com/43af2894f3f6408d9e960563a51e2a5c1b3e2bf3/chrome/browser/ui/views/tabs/tab_hover_card_metrics.cc
[modify] https://crrev.com/43af2894f3f6408d9e960563a51e2a5c1b3e2bf3/chrome/browser/ui/views/tabs/tab_hover_card_controller.cc
[modify] https://crrev.com/43af2894f3f6408d9e960563a51e2a5c1b3e2bf3/ui/views/animation/widget_fade_animator.h


### xi...@chromium.org (2022-05-04)

I was wrong about the DCHECK in #10. It is actually the cause of double Stop().

Check out code around the DCHECK:
https://source.chromium.org/chromium/chromium/src/+/main:ui/views/animation/widget_fade_animator.cc;drc=287fa204b78ccaa8da5c1a155c5fbfacafef31c8;l=42-45

When the DCHECK is triggered, FadeOut() is called with a running fade-in animation. The code would trigger Stop() twice. Once from `fade_complete_callbacks_.Notify` and the other from `widget_->Close()` -> `WidgetFadeAnimator::OnWidgetDestroying`. The 2nd Stop is the crash in #0.

Think the CL in #20 should fix the issue.

### [Deleted User] (2022-05-05)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-05)

[Empty comment from Monorail migration]

### am...@google.com (2022-05-16)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-05-16)

Thank you for this report, Khalil! Because the amount of user interaction required to trigger this issue, the VRP Panel has decided to award you $3,000 for this report. Thank you for your efforts in discovering and reporting this issue to us!  

### am...@chromium.org (2022-05-16)

Noticing a foundin was never set; going against my own general guidance and process and not reproducing or looking for when this issue was introduced or how long back it goes and adding foundin based solely on what version this was discovered and reported in 

### am...@chromium.org (2022-05-16)

This fix landed on 103 so need to manually request backmerge based on foundin above 

### [Deleted User] (2022-05-17)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-05-17)

Not requesting merge to dev (M103) because latest trunk commit (999429) appears to be prior to dev branch point (1002911). If this is incorrect, please replace the Merge-NA-103 label with Merge-Request-103. If other changes are required to fix this bug completely, please request a merge if necessary.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2022-05-24)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-10)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1317746?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059416)*
