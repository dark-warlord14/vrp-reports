# Security: heap-use-after-free in blink::TransitionInterpolation on CSS custom properties

| Field | Value |
|-------|-------|
| **Issue ID** | [407328533](https://issues.chromium.org/issues/407328533) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Animation, Blink>CSS |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | re...@gmail.com |
| **Assignee** | fl...@google.com |
| **Created** | 2025-03-30 |
| **Bounty** | $4,000.00 |

## Description

VULNERABILITY DETAILS
When transitioning a custom property with @starting-style, heap-use-after-free tab crashes in blink::TransitionInterpolation seem to be likely. I am not exactly sure what triggers the heap-uaf and how/whether it could be used, but I have found a reliable repro for this.

I am not sure whether this is an exploitable security bug, but since it is an uaf read I figured I'd report it anyways.

VERSION
Chrome Version: 136.0.7091.2 Dev
Operating System: Windows, Android

REPRODUCTION CASE
Condensed down:
```
@property --crash {
  syntax: '<integer>';
  initial-value: 0;
  inherits: false;
}
* {
  transition: --crash 1000s;
  @starting-style {
    --crash: 1000000;
  }
}
```
I have also added a viewport in the included crash.html just in case.

This bug is reliably reproducible through DevTools:
1. Open crash.html.
2. Open devtools.
3. Turn on the device toolbar.
4. Wait a few seconds, turn the device toolbar off.
5. Resize the devtools panel.
Note that only the steps 1-3 are necessary for a crash, but steps 4-5 make the repro reliable.

On Android it can be reproduced as such:
1. Open crash.html.
2. Resize Chrome[1].
3. Wait for a while
Repro on Android is not reliable and takes a while, but doesn't require DevTools or unrealistic user actions.

[1] I am not sure what types of resizes trigger the crash and which do not. Closing my folding phone does trigger the crash, as does resizing a window in my phone's multi-window mode. I am not sure of whether simply rotating the screen is enough though.

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: tab
Crash State: see asan.log
The asan report was captured with --single-process, I'm not sure how I'd get asan logs for the tab otherwise. The tab crash happens without the flag too, of course.

CREDIT INFORMATION
Externally reported security bugs may appear in Chrome release notes. If this bug is included, how would you like to be credited?
Reporter credit: Lyra Rebane (rebane2001)


## Attachments

- deleted (application/octet-stream, 0 B)
- [chrome_2025-03-30_19-51-07.mp4](attachments/chrome_2025-03-30_19-51-07.mp4) (video/mp4, 324.5 KB)
- [crash.html](attachments/crash.html) (text/html, 318 B)
- [asan2.log](attachments/asan2.log) (text/plain, 35.9 KB)
- [crash2.html](attachments/crash2.html) (text/html, 372 B)
- [crash2.html](attachments/crash2.html) (text/html, 372 B)
- [crash3.html](attachments/crash3.html) (text/html, 846 B)
- [demo.webm](attachments/demo.webm) (video/webm, 2.9 MB)
- [crash.html](attachments/crash.html) (text/html, 590 B)

## Timeline

### re...@gmail.com (2025-03-30)

Oh nevermind, `--no-sandbox` also gives the asan trace, no need for `--single-process`:

```
=================================================================
==60948==ERROR: AddressSanitizer: heap-use-after-free on address 0x120150a365c0 at pc 0x7ffcb1e268b4 bp 0x006ab5fed5a0 sp 0x006ab5fed5e8
READ of size 8 at 0x120150a365c0 thread T0
    #0 0x7ffcb1e268b3 in blink::TransitionInterpolation::Apply(class blink::InterpolationEnvironment &) const C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\animation\transition_interpolation.cc:45:9
    #1 0x7ffcb1872979 in blink::StyleCascade::ApplyInterpolation(class blink::CSSProperty const &, class blink::CascadePriority, class blink::HeapVector<class cppgc::internal::BasicMember<class blink::Interpolation, class cppgc::internal::StrongMemberTag, struct cppgc::internal::DijkstraWriteBarrierPolicy, class cppgc::internal::DisabledCheckingPolicy, class cppgc::internal::CompressedPointer>, 1> const &, class blink::CascadeResolver &) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\css\resolver\style_cascade.cc:828:48
    #2 0x7ffcb1872119 in blink::StyleCascade::ApplyInterpolationMap(class blink::BasicHeapHashMap<1, class blink::PropertyHandle, class cppgc::internal::BasicMember<class blink::HeapVector<class cppgc::internal::BasicMember<class blink::Interpolation, class cppgc::internal::StrongMemberTag, struct cppgc::internal::DijkstraWriteBarrierPolicy, class cppgc::internal::DisabledCheckingPolicy, class cppgc::internal::CompressedPointer>, 1>, class cppgc::internal::StrongMemberTag, struct cppgc::internal::DijkstraWriteBarrierPolicy, class cppgc::internal::DisabledCheckingPolicy, class cppgc::internal::CompressedPointer>, struct WTF::HashTraits<class blink::PropertyHandle>, struct WTF::HashTraits<class cppgc::internal::BasicMember<class blink::HeapVector<class cppgc::internal::BasicMember<class blink::Interpolation, class cppgc::internal::StrongMemberTag, struct cppgc::internal::DijkstraWriteBarrierPolicy, class cppgc::internal::DisabledCheckingPolicy, class cppgc::internal::CompressedPointer>, 1>, class cppgc::internal::StrongMemberTag, struct cppgc::internal::DijkstraWriteBarrierPolicy, class cppgc::internal::DisabledCheckingPolicy, class cppgc::internal::CompressedPointer>>> const &, enum blink::CascadeOrigin, unsigned __int64, class blink::CascadeResolver &) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\css\resolver\style_cascade.cc:809:5
    #3 0x7ffcb1865ab3 in blink::StyleCascade::ApplyInterpolations C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\css\resolver\style_cascade.cc:775
    #4 0x7ffcb1865ab3 in blink::StyleCascade::Apply(class blink::CascadeFilter) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\css\resolver\style_cascade.cc:281:3
    #5 0x7ffcb18a7f2b in blink::StyleResolver::ApplyAnimatedStyle(class blink::StyleResolverState &, class blink::StyleCascade &, class blink::StyleRecalcContext const &) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\css\resolver\style_resolver.cc:2469:13
    #6 0x7ffcb18a455e in blink::StyleResolver::ResolveStyle(class blink::Element *, class blink::StyleRecalcContext const &, class blink::StyleRequest const &) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\css\resolver\style_resolver.cc:1314:7
    #7 0x7ffcb1be9500 in blink::Element::OriginalStyleForLayoutObject(class blink::StyleRecalcContext const &) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\element.cc:3983:43
    #8 0x7ffcb1be8cc0 in blink::Element::StyleForLayoutObject(class blink::StyleRecalcContext const &) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\element.cc:3938:13
    #9 0x7ffcb1becced in blink::Element::RecalcOwnStyle(class blink::StyleRecalcChange, class blink::StyleRecalcContext const &) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\element.cc:4500:17
    #10 0x7ffcb1bea89c in blink::Element::RecalcStyle(class blink::StyleRecalcChange, class blink::StyleRecalcContext const &) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\element.cc:4136:20
    #11 0x7ffcb019fe28 in blink::StyleEngine::RecalcStyle(class blink::StyleRecalcChange, class blink::StyleRecalcContext const &) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\css\style_engine.cc:3816:16
    #12 0x7ffcb01a4592 in blink::StyleEngine::RecalcStyle C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\css\style_engine.cc:3869
    #13 0x7ffcb01a4592 in blink::StyleEngine::UpdateStyleAndLayoutTree(void) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\css\style_engine.cc:3987:7
    #14 0x7ffcb1d518f3 in blink::Document::UpdateStyle(void) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\document.cc:2522:16
    #15 0x7ffcb1d4ea5e in blink::Document::UpdateStyleAndLayoutTreeForThisDocument(void) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\document.cc:2460:3
    #16 0x7ffcaf5f99c5 in blink::LocalFrameView::UpdateStyleAndLayoutInternal(void) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\frame\local_frame_view.cc:3192:30
    #17 0x7ffcaf5e5850 in blink::LocalFrameView::UpdateStyleAndLayout(void) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\frame\local_frame_view.cc:3136:18
    #18 0x7ffcb1d4ff5d in blink::Document::UpdateStyleAndLayout(enum blink::DocumentUpdateReason) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\document.cc:2834:17
    #19 0x7ffcafc35598 in blink::FrameSelection::ComputeAbsoluteBounds(class gfx::Rect &, class gfx::Rect &) const C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\editing\frame_selection.cc:738:26
    #20 0x7ffcaf4c1df1 in blink::WebFrameWidgetImpl::CalculateSelectionBounds(class gfx::Rect &, class gfx::Rect &, class gfx::Rect *) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\frame\web_frame_widget_impl.cc:4708:18
    #21 0x7ffcaf4c12b2 in blink::WebFrameWidgetImpl::GetSelectionBoundsInWindow(class gfx::Rect *, class gfx::Rect *, class gfx::Rect *, enum base::i18n::TextDirection *, enum base::i18n::TextDirection *, bool *) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\frame\web_frame_widget_impl.cc:3865:3
    #22 0x7ffcb0f6357d in blink::WidgetBase::UpdateSelectionBounds(void) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\widget\widget_base.cc:1470:23
    #23 0x7ffcb0f630db in blink::WidgetBase::WillBeginMainFrame(void) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\widget\widget_base.cc:997:3
    #24 0x7ffca7fa1a15 in cc::LayerTreeHost::WillBeginMainFrame(void) C:\b\s\w\ir\cache\builder\src\cc\trees\layer_tree_host.cc:372:12
    #25 0x7ffca7f731cd in cc::ProxyMain::BeginMainFrame(class std::__Cr::unique_ptr<struct cc::BeginMainFrameAndCommitState, struct std::__Cr::default_delete<struct cc::BeginMainFrameAndCommitState>>) C:\b\s\w\ir\cache\builder\src\cc\trees\proxy_main.cc:274:21
    #26 0x7ffca7f694de in base::internal::DecayedFunctorTraits<void (cc::ProxyMain::*)(std::__Cr::unique_ptr<cc::BeginMainFrameAndCommitState,std::__Cr::default_delete<cc::BeginMainFrameAndCommitState> >),base::WeakPtr<cc::ProxyMain> &&,std::__Cr::unique_ptr<cc::BeginMainFrameAndCommitState,std::__Cr::default_delete<cc::BeginMainFrameAndCommitState> > &&>::Invoke C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:731
    #27 0x7ffca7f694de in base::internal::InvokeHelper<1,base::internal::FunctorTraits<void (cc::ProxyMain::*&&)(std::__Cr::unique_ptr<cc::BeginMainFrameAndCommitState,std::__Cr::default_delete<cc::BeginMainFrameAndCommitState> >),base::WeakPtr<cc::ProxyMain> &&,std::__Cr::unique_ptr<cc::BeginMainFrameAndCommitState,std::__Cr::default_delete<cc::BeginMainFrameAndCommitState> > &&>,void,0,1>::MakeItSo C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:947
    #28 0x7ffca7f694de in base::internal::Invoker<base::internal::FunctorTraits<void (cc::ProxyMain::*&&)(std::__Cr::unique_ptr<cc::BeginMainFrameAndCommitState,std::__Cr::default_delete<cc::BeginMainFrameAndCommitState> >),base::WeakPtr<cc::ProxyMain> &&,std::__Cr::unique_ptr<cc::BeginMainFrameAndCommitState,std::__Cr::default_delete<cc::BeginMainFrameAndCommitState> > &&>,base::internal::BindState<1,1,0,void (cc::ProxyMain::*)(std::__Cr::unique_ptr<cc::BeginMainFrameAndCommitState,std::__Cr::default_delete<cc::BeginMainFrameAndCommitState> >),base::WeakPtr<cc::ProxyMain>,std::__Cr::unique_ptr<cc::BeginMainFrameAndCommitState,std::__Cr::default_delete<cc::BeginMainFrameAndCommitState> > >,void ()>::RunImpl C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:1060
    #29 0x7ffca7f694de in base::internal::Invoker<struct base::internal::FunctorTraits<void (__cdecl cc::ProxyMain::*&&)(class std::__Cr::unique_ptr<struct cc::BeginMainFrameAndCommitState, struct std::__Cr::default_delete<struct cc::BeginMainFrameAndCommitState>>), class base::WeakPtr<class cc::ProxyMain> &&, class std::__Cr::unique_ptr<struct cc::BeginMainFrameAndCommitState, struct std::__Cr::default_delete<struct cc::BeginMainFrameAndCommitState>> &&>, struct base::internal::BindState<1, 1, 0, void (__cdecl cc::ProxyMain::*)(class std::__Cr::unique_ptr<struct cc::BeginMainFrameAndCommitState, struct std::__Cr::default_delete<struct cc::BeginMainFrameAndCommitState>>), class base::WeakPtr<class cc::ProxyMain>, class std::__Cr::unique_ptr<struct cc::BeginMainFrameAndCommitState, struct std::__Cr::default_delete<struct cc::BeginMainFrameAndCommitState>>>, (void)>::RunOnce(class base::internal::BindStateBase *) C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:973:12
    #30 0x7ffca2cf9343 in base::OnceCallback<void ()>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:156
    #31 0x7ffca2cf9343 in base::TaskAnnotator::RunTaskImpl(struct base::PendingTask &) C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:209:34
    #32 0x7ffca2ccc1c4 in base::TaskAnnotator::RunTask C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.h:106
    #33 0x7ffca2ccc1c4 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(class base::LazyNow *) C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:456:23
    #34 0x7ffca2ccb03f in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork(void) C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:330:40
    #35 0x7ffca2e21d37 in base::MessagePumpDefault::Run(class base::MessagePump::Delegate *) C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_default.cc:42:55
    #36 0x7ffca2ccdeb1 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, class base::TimeDelta) C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:629:12
    #37 0x7ffca2d63c8e in base::RunLoop::Run(class base::Location const &) C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:134:14
    #38 0x7ffcb8302269 in content::RendererMain(struct content::MainFunctionParams) C:\b\s\w\ir\cache\builder\src\content\renderer\renderer_main.cc:369:16
    #39 0x7ffc9f8ae236 in content::RunOtherNamedProcessTypeMain(class std::__Cr::basic_string<char, struct std::__Cr::char_traits<char>, class std::__Cr::allocator<char>> const &, struct content::MainFunctionParams, class content::ContentMainDelegate *) C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:780:14
    #40 0x7ffc9f8b0561 in content::ContentMainRunnerImpl::Run(void) C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1154:10
    #41 0x7ffc9f8a4695 in content::RunContentProcess(struct content::ContentMainParams, class content::ContentMainRunner *) C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:359:36
    #42 0x7ffc9f8a523d in content::ContentMain(struct content::ContentMainParams) C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:372:10
    #43 0x7ffc903216c7 in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:222:12
    #44 0x7ff7e79f47ae in MainDllLoader::Launch(struct HINSTANCE__*, class base::TimeTicks) C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:201:12
    #45 0x7ff7e79f2015 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:352:20
    #46 0x7ff7e807307b in invoke_main D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:78
    #47 0x7ff7e807307b in __scrt_common_main_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #48 0x7ffe20607373  (C:\WINDOWS\System32\KERNEL32.DLL+0x180017373)
    #49 0x7ffe20e7cc90  (C:\WINDOWS\SYSTEM32\ntdll.dll+0x18004cc90)

0x120150a365c0 is located 0 bytes inside of 64-byte region [0x120150a365c0,0x120150a36600)
freed by thread T0 here:
    #0 0x7ffd765c932d  (G:\chromium-136.0.7091.2-win64-asan\clang_rt.asan_dynamic-x86_64.dll+0x18004932d)
    #1 0x7ffcb8fe8a23 in free C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win_thunk.cpp:55
    #2 0x7ffcb1f26401 in blink::InterpolationType::operator delete C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\animation\interpolation_type.h:31
    #3 0x7ffcb1f26401 in blink::CSSVisibilityInterpolationType::`scalar deleting dtor'(unsigned int) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\animation\css_length_interpolation_type.h:16:19
    #4 0x7ffcb03054d9 in std::__Cr::default_delete<const blink::InterpolationType>::operator() C:\b\s\w\ir\cache\builder\src\third_party\libc++\src\include\__memory\unique_ptr.h:76
    #5 0x7ffcb03054d9 in std::__Cr::unique_ptr<const blink::InterpolationType,std::__Cr::default_delete<const blink::InterpolationType> >::reset C:\b\s\w\ir\cache\builder\src\third_party\libc++\src\include\__memory\unique_ptr.h:287
    #6 0x7ffcb03054d9 in std::__Cr::unique_ptr<const blink::InterpolationType,std::__Cr::default_delete<const blink::InterpolationType> >::~unique_ptr C:\b\s\w\ir\cache\builder\src\third_party\libc++\src\include\__memory\unique_ptr.h:256
    #7 0x7ffcb03054d9 in WTF::VectorTypeOperations<std::__Cr::unique_ptr<const blink::InterpolationType,std::__Cr::default_delete<const blink::InterpolationType> >,WTF::PartitionAllocator>::Destruct C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\wtf\vector.h:177
    #8 0x7ffcb03054d9 in WTF::Vector<std::__Cr::unique_ptr<const blink::InterpolationType,std::__Cr::default_delete<const blink::InterpolationType> >,0,WTF::PartitionAllocator>::~Vector C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\wtf\vector.h:1620
    #9 0x7ffcb03054d9 in blink::PropertyRegistration::~PropertyRegistration(void) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\css\property_registration.cc:58:45
    #10 0x7ffc9776328a in cppgc::internal::`anonymous namespace'::SweepFinalizer::FinalizePage::<lambda_1>::operator() C:\b\s\w\ir\cache\builder\src\v8\src\heap\cppgc\sweeper.cc:505
    #11 0x7ffc9776328a in cppgc::internal::`anonymous namespace'::SweepFinalizer::FinalizePage C:\b\s\w\ir\cache\builder\src\v8\src\heap\cppgc\sweeper.cc:519:7
    #12 0x7ffc977683b9 in cppgc::internal::`anonymous namespace'::SweepFinalizer::FinalizeWithDeadline C:\b\s\w\ir\cache\builder\src\v8\src\heap\cppgc\sweeper.cc:488
    #13 0x7ffc977683b9 in cppgc::internal::`anonymous namespace'::MutatorThreadSweeper::FinalizeAndSweepWithDeadline C:\b\s\w\ir\cache\builder\src\v8\src\heap\cppgc\sweeper.cc:658:20
    #14 0x7ffc9775693d in cppgc::internal::Sweeper::SweeperImpl::PerformSweepOnMutatorThread C:\b\s\w\ir\cache\builder\src\v8\src\heap\cppgc\sweeper.cc:1367:24
    #15 0x7ffc9775daeb in cppgc::internal::Sweeper::SweeperImpl::SweepInForegroundTaskImpl(class v8::base::TimeDelta, enum cppgc::internal::StatsCollector::ScopeId) C:\b\s\w\ir\cache\builder\src\v8\src\heap\cppgc\sweeper.cc:1508:39
    #16 0x7ffc9775d6d3 in cppgc::internal::Sweeper::SweeperImpl::SweepForLowPriorityTask C:\b\s\w\ir\cache\builder\src\v8\src\heap\cppgc\sweeper.cc:1051
    #17 0x7ffc9775d6d3 in cppgc::internal::Sweeper::SweeperImpl::IncrementalSweepTask::Run(void) C:\b\s\w\ir\cache\builder\src\v8\src\heap\cppgc\sweeper.cc:1466:20
    #18 0x7ffca9d1f4e6 in base::internal::DecayedFunctorTraits<void (v8::Task::*)(),std::__Cr::unique_ptr<v8::Task,std::__Cr::default_delete<v8::Task> > &&>::Invoke C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:731
    #19 0x7ffca9d1f4e6 in base::internal::InvokeHelper<0,base::internal::FunctorTraits<void (v8::Task::*&&)(),std::__Cr::unique_ptr<v8::Task,std::__Cr::default_delete<v8::Task> > &&>,void,0>::MakeItSo C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:923
    #20 0x7ffca9d1f4e6 in base::internal::Invoker<base::internal::FunctorTraits<void (v8::Task::*&&)(),std::__Cr::unique_ptr<v8::Task,std::__Cr::default_delete<v8::Task> > &&>,base::internal::BindState<1,1,0,void (v8::Task::*)(),std::__Cr::unique_ptr<v8::Task,std::__Cr::default_delete<v8::Task> > >,void ()>::RunImpl C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:1060
    #21 0x7ffca9d1f4e6 in base::internal::Invoker<struct base::internal::FunctorTraits<void (__cdecl v8::Task::*&&)(void), class std::__Cr::unique_ptr<class v8::Task, struct std::__Cr::default_delete<class v8::Task>> &&>, struct base::internal::BindState<1, 1, 0, void (__cdecl v8::Task::*)(void), class std::__Cr::unique_ptr<class v8::Task, struct std::__Cr::default_delete<class v8::Task>>>, (void)>::RunOnce(class base::internal::BindStateBase *) C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:973:12
    #22 0x7ffca2cf9343 in base::OnceCallback<void ()>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:156
    #23 0x7ffca2cf9343 in base::TaskAnnotator::RunTaskImpl(struct base::PendingTask &) C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:209:34
    #24 0x7ffca2ccc1c4 in base::TaskAnnotator::RunTask C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.h:106
    #25 0x7ffca2ccc1c4 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(class base::LazyNow *) C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:456:23
    #26 0x7ffca2ccb03f in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork(void) C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:330:40
    #27 0x7ffca2e21d37 in base::MessagePumpDefault::Run(class base::MessagePump::Delegate *) C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_default.cc:42:55
    #28 0x7ffca2ccdeb1 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, class base::TimeDelta) C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:629:12
    #29 0x7ffca2d63c8e in base::RunLoop::Run(class base::Location const &) C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:134:14
    #30 0x7ffcb8302269 in content::RendererMain(struct content::MainFunctionParams) C:\b\s\w\ir\cache\builder\src\content\renderer\renderer_main.cc:369:16
    #31 0x7ffc9f8ae236 in content::RunOtherNamedProcessTypeMain(class std::__Cr::basic_string<char, struct std::__Cr::char_traits<char>, class std::__Cr::allocator<char>> const &, struct content::MainFunctionParams, class content::ContentMainDelegate *) C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:780:14
    #32 0x7ffc9f8b0561 in content::ContentMainRunnerImpl::Run(void) C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1154:10
    #33 0x7ffc9f8a4695 in content::RunContentProcess(struct content::ContentMainParams, class content::ContentMainRunner *) C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:359:36
    #34 0x7ffc9f8a523d in content::ContentMain(struct content::ContentMainParams) C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:372:10
    #35 0x7ffc903216c7 in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:222:12
    #36 0x7ff7e79f47ae in MainDllLoader::Launch(struct HINSTANCE__*, class base::TimeTicks) C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:201:12
    #37 0x7ff7e79f2015 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:352:20
    #38 0x7ff7e807307b in invoke_main D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:78
    #39 0x7ff7e807307b in __scrt_common_main_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #40 0x7ffe20607373  (C:\WINDOWS\System32\KERNEL32.DLL+0x180017373)
    #41 0x7ffe20e7cc90  (C:\WINDOWS\SYSTEM32\ntdll.dll+0x18004cc90)

previously allocated by thread T0 here:
    #0 0x7ffd765c943d  (G:\chromium-136.0.7091.2-win64-asan\clang_rt.asan_dynamic-x86_64.dll+0x18004943d)
    #1 0x7ffcb8fe8a43 in malloc C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win_thunk.cpp:64
    #2 0x7ffca2ea8e89 in partition_alloc::PartitionRoot::AllocInternal C:\b\s\w\ir\cache\builder\src\base\allocator\partition_allocator\src\partition_alloc\partition_root.h:2144
    #3 0x7ffca2ea8e89 in partition_alloc::PartitionRoot::AllocInline C:\b\s\w\ir\cache\builder\src\base\allocator\partition_allocator\src\partition_alloc\partition_root.h:543
    #4 0x7ffca2ea8e89 in partition_alloc::PartitionRoot::Alloc<0>(unsigned __int64, char const *) C:\b\s\w\ir\cache\builder\src\base\allocator\partition_allocator\src\partition_alloc\partition_root.h:537:12
    #5 0x7ffcb1fbf499 in blink::InterpolationType::operator new C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\animation\interpolation_type.h:31
    #6 0x7ffcb1fbf499 in std::__Cr::make_unique<class blink::CSSNumberInterpolationType, class blink::PropertyHandle &, class blink::PropertyRegistration const *, bool, 0>(class blink::PropertyHandle &, class blink::PropertyRegistration const *&&, bool &&) C:\b\s\w\ir\cache\builder\src\third_party\libc++\src\include\__memory\unique_ptr.h:754:26
    #7 0x7ffcb1fbc7d8 in blink::CreateInterpolationTypeForCSSSyntax C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\animation\css_interpolation_types_map.cc:495
    #8 0x7ffcb1fbc7d8 in blink::CSSInterpolationTypesMap::CreateInterpolationTypesForCSSSyntax(class WTF::AtomicString const &, class blink::CSSSyntaxDefinition const &, class blink::PropertyRegistration const &) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\animation\css_interpolation_types_map.cc:538:9
    #9 0x7ffcb0307ecc in blink::PropertyRegistration::PropertyRegistration C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\css\property_registration.cc:52
    #10 0x7ffcb0307ecc in cppgc::MakeGarbageCollectedTrait<class blink::PropertyRegistration>::Call<class WTF::AtomicString const &, class blink::CSSSyntaxDefinition &, bool &, class blink::CSSValue const *&, class blink::StyleRuleProperty *>(class cppgc::AllocationHandle &, class WTF::AtomicString const &, class blink::CSSSyntaxDefinition &, bool &, class blink::CSSValue const *&, class blink::StyleRuleProperty *&&) C:\b\s\w\ir\cache\builder\src\v8\include\cppgc\allocation.h:240:32
    #11 0x7ffcb0306c29 in cppgc::MakeGarbageCollected C:\b\s\w\ir\cache\builder\src\v8\include\cppgc\allocation.h:278
    #12 0x7ffcb0306c29 in blink::MakeGarbageCollected C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\heap\garbage_collected.h:37
    #13 0x7ffcb0306c29 in blink::PropertyRegistration::MaybeCreateForDeclaredProperty(class blink::Document &, class WTF::AtomicString const &, class blink::StyleRuleProperty &) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\css\property_registration.cc:184:10
    #14 0x7ffcb019b871 in blink::StyleEngine::AddPropertyRules(class blink::StyleEngine::AtRuleCascadeMap &, class blink::RuleSet const &, bool) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\css\style_engine.cc:3437:9
    #15 0x7ffcb01961a0 in blink::StyleEngine::AddPropertyRulesFromSheets C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\css\style_engine.cc:3325
    #16 0x7ffcb01961a0 in blink::StyleEngine::ApplyRuleSetChanges(class blink::TreeScope &, class blink::HeapVector<struct std::__Cr::pair<class cppgc::internal::BasicMember<class blink::CSSStyleSheet, class cppgc::internal::StrongMemberTag, struct cppgc::internal::DijkstraWriteBarrierPolicy, class cppgc::internal::DisabledCheckingPolicy, class cppgc::internal::CompressedPointer>, class cppgc::internal::BasicMember<class blink::RuleSet, class cppgc::internal::StrongMemberTag, struct cppgc::internal::DijkstraWriteBarrierPolicy, class cppgc::internal::DisabledCheckingPolicy, class cppgc::internal::CompressedPointer>>, 0> const &, class blink::HeapVector<struct std::__Cr::pair<class cppgc::internal::BasicMember<class blink::CSSStyleSheet, class cppgc::internal::StrongMemberTag, struct cppgc::internal::DijkstraWriteBarrierPolicy, class cppgc::internal::DisabledCheckingPolicy, class cppgc::internal::CompressedPointer>, class cppgc::internal::BasicMember<class blink::RuleSet, class cppgc::internal::StrongMemberTag, struct cppgc::internal::DijkstraWriteBarrierPolicy, class cppgc::internal::DisabledCheckingPolicy, class cppgc::internal::CompressedPointer>>, 0> const &, class blink::HeapVector<class cppgc::internal::BasicMember<class blink::RuleSetDiff, class cppgc::internal::StrongMemberTag, struct cppgc::internal::DijkstraWriteBarrierPolicy, class cppgc::internal::DisabledCheckingPolicy, class cppgc::internal::CompressedPointer>, 0> const &) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\css\style_engine.cc:3042:7
    #17 0x7ffcb014eb9b in blink::TreeScopeStyleSheetCollection::ApplyActiveStyleSheetChanges(class blink::StyleSheetCollection &) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\css\tree_scope_style_sheet_collection.cc:56:34
    #18 0x7ffcb0692681 in blink::DocumentStyleSheetCollection::UpdateActiveStyleSheets(class blink::StyleEngine &) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\css\document_style_sheet_collection.cc:127:3
    #19 0x7ffcb017b71e in blink::StyleEngine::UpdateActiveStyleSheets(void) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\css\style_engine.cc:685:39
    #20 0x7ffcb0172b03 in blink::StyleEngine::UpdateActiveStyle(void) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\css\style_engine.cc:763:3
    #21 0x7ffcb1d4e9ee in blink::Document::UpdateStyleAndLayoutTreeForThisDocument(void) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\document.cc:2453:16
    #22 0x7ffcb1d4d8e3 in blink::Document::UpdateStyleAndLayoutTree(class blink::LayoutUpgrade &) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\document.cc:2320:5
    #23 0x7ffcb1d4310f in blink::Document::UpdateStyleAndLayoutTree(void) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\document.cc:2295:3
    #24 0x7ffcafc37705 in blink::FrameSelection::FocusedOrActiveStateChanged(void) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\editing\frame_selection.cc:1038:17
    #25 0x7ffcaf4aafd4 in blink::WebFrameWidgetImpl::FocusChanged(enum blink::mojom::FocusState) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\frame\web_frame_widget_impl.cc:1843:11
    #26 0x7ffcb0f9429e in base::internal::DecayedFunctorTraits<void (blink::WidgetBase::*)(blink::mojom::FocusState),base::WeakPtr<blink::WidgetBase> &&,blink::mojom::FocusState &&>::Invoke C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:731
    #27 0x7ffcb0f9429e in base::internal::InvokeHelper<1,base::internal::FunctorTraits<void (blink::WidgetBase::*&&)(blink::mojom::FocusState),base::WeakPtr<blink::WidgetBase> &&,blink::mojom::FocusState &&>,void,0,1>::MakeItSo C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:947
    #28 0x7ffcb0f9429e in base::internal::Invoker<base::internal::FunctorTraits<void (blink::WidgetBase::*&&)(blink::mojom::FocusState),base::WeakPtr<blink::WidgetBase> &&,blink::mojom::FocusState &&>,base::internal::BindState<1,1,0,void (blink::WidgetBase::*)(blink::mojom::FocusState),base::WeakPtr<blink::WidgetBase>,blink::mojom::FocusState>,void ()>::RunImpl C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:1060
    #29 0x7ffcb0f9429e in base::internal::Invoker<struct base::internal::FunctorTraits<void (__cdecl blink::WidgetBase::*&&)(enum blink::mojom::FocusState), class base::WeakPtr<class blink::WidgetBase> &&, enum blink::mojom::FocusState &&>, struct base::internal::BindState<1, 1, 0, void (__cdecl blink::WidgetBase::*)(enum blink::mojom::FocusState), class base::WeakPtr<class blink::WidgetBase>, enum blink::mojom::FocusState>, (void)>::RunOnce(class base::internal::BindStateBase *) C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:973:12
    #30 0x7ffcb0f93a45 in base::OnceCallback<void ()>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:156
    #31 0x7ffcb0f93a45 in blink::`anonymous namespace'::RunClosureIfNotSwappedOut C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\widget\input\widget_input_handler_impl.cc:37:22
    #32 0x7ffcb0f97258 in base::internal::DecayedFunctorTraits<void (*)(base::WeakPtr<blink::WidgetBase>, base::OnceCallback<void ()>),base::WeakPtr<blink::WidgetBase> &&,base::OnceCallback<void ()> &&>::Invoke C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:664
    #33 0x7ffcb0f97258 in base::internal::InvokeHelper<0,base::internal::FunctorTraits<void (*&&)(base::WeakPtr<blink::WidgetBase>, base::OnceCallback<void ()>),base::WeakPtr<blink::WidgetBase> &&,base::OnceCallback<void ()> &&>,void,0,1>::MakeItSo C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:923
    #34 0x7ffcb0f97258 in base::internal::Invoker<base::internal::FunctorTraits<void (*&&)(base::WeakPtr<blink::WidgetBase>, base::OnceCallback<void ()>),base::WeakPtr<blink::WidgetBase> &&,base::OnceCallback<void ()> &&>,base::internal::BindState<0,1,0,void (*)(base::WeakPtr<blink::WidgetBase>, base::OnceCallback<void ()>),base::WeakPtr<blink::WidgetBase>,base::OnceCallback<void ()> >,void ()>::RunImpl C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:1060
    #35 0x7ffcb0f97258 in base::internal::Invoker<struct base::internal::FunctorTraits<void (__cdecl *&&)(class base::WeakPtr<class blink::WidgetBase>, class base::OnceCallback<(void)>), class base::WeakPtr<class blink::WidgetBase> &&, class base::OnceCallback<void __cdecl(void)> &&>, struct base::internal::BindState<0, 1, 0, void (__cdecl *)(class base::WeakPtr<class blink::WidgetBase>, class base::OnceCallback<(void)>), class base::WeakPtr<class blink::WidgetBase>, class base::OnceCallback<void __cdecl(void)>>, (void)>::RunOnce(class base::internal::BindStateBase *) C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:973:12
    #36 0x7ffcb0fb7dc1 in base::OnceCallback<void ()>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:156
    #37 0x7ffcb0fb7dc1 in blink::`anonymous namespace'::QueuedClosure::Dispatch C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\widget\input\main_thread_event_queue.cc:44:71
    #38 0x7ffcb0fac163 in blink::MainThreadEventQueue::DispatchEvents(void) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\widget\input\main_thread_event_queue.cc:570:11
    #39 0x7ffcb0fb8b4b in base::internal::DecayedFunctorTraits<void (blink::MainThreadEventQueue::*)(),blink::MainThreadEventQueue *&&>::Invoke C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:731
    #40 0x7ffcb0fb8b4b in base::internal::InvokeHelper<0,base::internal::FunctorTraits<void (blink::MainThreadEventQueue::*&&)(),blink::MainThreadEventQueue *&&>,void,0>::MakeItSo C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:923
    #41 0x7ffcb0fb8b4b in base::internal::Invoker<base::internal::FunctorTraits<void (blink::MainThreadEventQueue::*&&)(),blink::MainThreadEventQueue *&&>,base::internal::BindState<1,1,0,void (blink::MainThreadEventQueue::*)(),scoped_refptr<blink::MainThreadEventQueue> >,void ()>::RunImpl C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:1060
    #42 0x7ffcb0fb8b4b in base::internal::Invoker<struct base::internal::FunctorTraits<void (__cdecl blink::MainThreadEventQueue::*&&)(void), class blink::MainThreadEventQueue *&&>, struct base::internal::BindState<1, 1, 0, void (__cdecl blink::MainThreadEventQueue::*)(void), class scoped_refptr<class blink::MainThreadEventQueue>>, (void)>::RunOnce(class base::internal::BindStateBase *) C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:973:12
    #43 0x7ffca2cf9343 in base::OnceCallback<void ()>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:156
    #44 0x7ffca2cf9343 in base::TaskAnnotator::RunTaskImpl(struct base::PendingTask &) C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:209:34
    #45 0x7ffca2ccc1c4 in base::TaskAnnotator::RunTask C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.h:106
    #46 0x7ffca2ccc1c4 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(class base::LazyNow *) C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:456:23
    #47 0x7ffca2ccb03f in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork(void) C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:330:40
    #48 0x7ffca2e21d37 in base::MessagePumpDefault::Run(class base::MessagePump::Delegate *) C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_default.cc:42:55

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\animation\transition_interpolation.cc:45:9 in blink::TransitionInterpolation::Apply(class blink::InterpolationEnvironment &) const
Shadow bytes around the buggy address:
  0x120150a36300: fa fa f7 fa 00 00 00 00 00 00 00 fa fa fa f7 fa
  0x120150a36380: 00 00 00 00 00 00 00 fa fa fa f7 fa fa fa fa fa
  0x120150a36400: fa fa fa fa fa fa f7 fa 00 00 00 00 00 00 00 00
  0x120150a36480: fa fa f7 fa fa fa fa fa fa fa fa fa fa fa f7 fa
  0x120150a36500: fa fa fa fa fa fa fa fa fa fa f7 fa fd fd fd fd
=>0x120150a36580: fd fd fd fa fa fa f7 fa[fd]fd fd fd fd fd fd fd
  0x120150a36600: fa fa f7 fa fa fa fa fa fa fa fa fa fa fa f7 fa
  0x120150a36680: fa fa fa fa fa fa fa fa fa fa f7 fa fa fa fa fa
  0x120150a36700: fa fa fa fa fa fa f7 fa 00 00 00 00 00 00 00 fa
  0x120150a36780: fa fa f7 fa 00 00 00 00 00 00 00 fa fa fa f7 fa
  0x120150a36800: 00 00 00 00 00 00 00 fa fa fa f7 fa 00 00 00 00
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

==60948==ADDITIONAL INFO

==60948==Note: Please include this section with the ASan report.
Task trace:
    #0 0x7ffca7f61211 in cc::ProxyImpl::ScheduledActionSendBeginMainFrame(struct viz::BeginFrameArgs const &) C:\b\s\w\ir\cache\builder\src\cc\trees\proxy_impl.cc:767:7


Command line: `"G:\chromium-136.0.7091.2-win64-asan\chrome.exe" --type=renderer --no-pre-read-main-dll --no-sandbox --file-url-path-alias="/gen=G:\chromium-136.0.7091.2-win64-asan\gen" --video-capture-use-gpu-memory-buffer --lang=en-US --device-scale-factor=1 --num-raster-threads=4 --enable-main-frame-before-activation --renderer-client-id=10 --time-ticks-at-unix-epoch=-1742570653892378 --launch-time-ticks=785770462192 --metrics-shmem-handle=4348,i,15483222888000177775,14057892565839972040,2097152 --field-trial-handle=2084,i,18049945435554230983,6143566284878194330,262144 --variations-seed-version --mojo-platform-channel-handle=4344 /prefetch:1`


MiraclePtr Status: NOT PROTECTED
No raw_ptr<T> access to this region was detected prior to this crash.
This crash is still exploitable with MiraclePtr.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.

==60948==END OF ADDITIONAL INFO
==60948==ABORTING

```

### re...@gmail.com (2025-03-30)

I've made a slightly modified repro so that it works on older browser versions (repro steps are the same, except you must hover your mouse over the page first).

Bisected the bug down to between branch positions 871163 (doesn't repro) and 871167 (repros).

### re...@gmail.com (2025-03-30)

Those asan branch positions are builds at d94c7226d7bfc1d6a47e446164b382f22e8645de and f53b342ecd8083d7c74d9fb792736fc2ae1d8dc9 respectively. Looking at all the commits between the two, it appears the bad commit is most likely [f53b342ecd8083d7c74d9fb792736fc2ae1d8dc9](https://source.chromium.org/chromium/chromium/src/+/f53b342ecd8083d7c74d9fb792736fc2ae1d8dc9).

I read through the entire diff and couldn't find anything concrete though. The only suspicious change that stood out to me was:

```
diff --git a/third_party/blink/renderer/core/css/style_engine.cc b/third_party/blink/renderer/core/css/style_engine.cc
index 22df6e5369f38..8d768d5e49394 100644
--- a/third_party/blink/renderer/core/css/style_engine.cc
+++ b/third_party/blink/renderer/core/css/style_engine.cc
@@ -114,23 +113,19 @@ CSSFontSelector* CreateCSSFontSelectorFor(Document& document) {
 
 StyleEngine::StyleEngine(Document& document)
     : document_(&document),
-      is_html_import_(document.IsHTMLImport()),
       document_style_sheet_collection_(
           MakeGarbageCollected<DocumentStyleSheetCollection>(document)),
       resolver_(MakeGarbageCollected<StyleResolver>(document)),
       owner_color_scheme_(mojom::blink::ColorScheme::kLight) {
   if (document.GetFrame()) {
-    // We don't need to create CSSFontSelector for imported document or
-    // HTMLTemplateElement's document, because those documents have no frame.
     font_selector_ = CreateCSSFontSelectorFor(document);
     font_selector_->RegisterForInvalidationCallbacks(this);
+    global_rule_set_ = MakeGarbageCollected<CSSGlobalRuleSet>();
     if (const auto* owner = document.GetFrame()->Owner())
       owner_color_scheme_ = owner->GetColorScheme();
   }
   if (document.IsInMainFrame())
     viewport_resolver_ = MakeGarbageCollected<ViewportStyleResolver>(document);
-  if (!IsHTMLImport())
-    global_rule_set_ = MakeGarbageCollected<CSSGlobalRuleSet>();
   if (auto* settings = GetDocument().GetSettings()) {
     if (!settings->GetForceDarkModeEnabled())
       preferred_color_scheme_ = settings->GetPreferredColorScheme();

```

Which is moving the `global_rule_set_ = MakeGarbageCollected<CSSGlobalRuleSet>()` assignment into an `if(document.GetFrame())` block, while previously it would've been assigned regardless of what `document.GetFrame()` returns. But that's just something I've noticed, not sure if that's the breaking change.

I am also not sure whether this bisect reveals the true root cause of the issue or just marks the point where my specific repro was regressed.

### re...@gmail.com (2025-03-30)

Hmm, the bug does in fact seem to be related to a garbage collector. I suspect the going out of device mode and moving DevTools just forces a GC to happen.
Here's a new repro that crashes faster and more often, so it requires less user interaction.

New repro for desktop:

1. Open crash3.html.
2. Wait for the red square to disappear.
3. Open devtools (enable device toolbar if it isn't already).
4. Wait a few seconds for the tab to crash.

On Android it can be reproduced as such:

1. Open crash3.html while Chrome is in tabbed/tablet mode (eg when folding phone is open).
2. Wait for the red square to disappear.
3. Resize Chrome to the mobile mode (eg unfold a folding phone).
4. Wait a few seconds for the tab to crash.

I attached a video of the Android repro.

### re...@gmail.com (2025-03-30)

Moving the `global_rule_set_ = MakeGarbageCollected<CSSGlobalRuleSet>()` out of the if block did not fix the issue, so I don't think it is that.

### za...@google.com (2025-03-31)

Assigning this bug to v8 sheriff to take a look.

Hi cffsmith@ can you please take a look at this bug. I set the severity to S1 since it's a UaF bug. And it seems to related to renderer.
It seems like this CL (<https://chromium-review.googlesource.com/c/chromium/src/+/2798954>) caused this issue. Can you please take a look? Thanks.

### cf...@google.com (2025-04-01)

Hi zackhan@, this is not a V8 issue.

### ch...@google.com (2025-04-01)

Setting milestone because of s0/s1 severity.

### za...@google.com (2025-04-01)

Thanks, I am taking another look!

### za...@google.com (2025-04-01)

Hi masonf@ can you please take a look at this bug, it seems the CL in #7 might caused it, thank you!

### pe...@google.com (2025-04-02)

The issue's primary component must be in the Component Tags, so re-adding it. To change the primary component, use the edit button at the top of the issue, just above the title.

### pe...@google.com (2025-04-02)

The issue's primary component must be in the Component Tags, so re-adding it. To change the primary component, use the edit button at the top of the issue, just above the title.

### ma...@chromium.org (2025-04-02)

I can repro, with the crash.html from [comment #1](https://issues.chromium.org/issues/407328533#comment1). Open the file, open devtools, go to device emulation mode, tap on the page.

Crash stack is:

```
[59467:75080594:0402/093855.827818:ERROR:google_apis/gcm/engine/registration_request.cc:291] Registration response error message: DEPRECATED_ENDPOINT
Received signal 11 SEGV_ACCERR 2030310000000038
0   libbase.dylib                       0x0000000103a65e5c base::debug::CollectStackTrace(base::span<void const*, 18446744073709551615ul, void const**>) + 28
1   libbase.dylib                       0x0000000103a4cda8 base::debug::StackTrace::StackTrace(unsigned long) + 224
2   libbase.dylib                       0x0000000103a65d44 base::debug::(anonymous namespace)::StackDumpSignalHandler(int, __siginfo*, void*) + 940
3   libsystem_platform.dylib            0x0000000185f02584 _sigtramp + 56
4   libblink_core.dylib                 0x0000000122b5ec4c blink::TransitionInterpolation::Apply(blink::InterpolationEnvironment&) const + 44
5   libblink_core.dylib                 0x0000000120a731c8 blink::StyleCascade::ApplyInterpolation(blink::CSSProperty const&, blink::CascadePriority, blink::HeapVector<cppgc::internal::BasicMember<blink::Interpolation, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy, cppgc::internal::CompressedPointer>, 1u> const&, blink::CascadeResolver&) + 372
6   libblink_core.dylib                 0x0000000120a72e64 blink::StyleCascade::ApplyInterpolationMap(blink::BasicHeapHashMap<(blink::internal::HeapCollectionType)1, blink::PropertyHandle, cppgc::internal::BasicMember<blink::HeapVector<cppgc::internal::BasicMember<blink::Interpolation, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy, cppgc::internal::CompressedPointer>, 1u>, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy, cppgc::internal::CompressedPointer>, WTF::HashTraits<blink::PropertyHandle>, WTF::HashTraits<cppgc::internal::BasicMember<blink::HeapVector<cppgc::internal::BasicMember<blink::Interpolation, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy, cppgc::internal::CompressedPointer>, 1u>, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy, cppgc::internal::CompressedPointer>>> const&, blink::CascadeOrigin, unsigned long, blink::CascadeResolver&) + 684
7   libblink_core.dylib                 0x0000000120a6f4a0 blink::StyleCascade::Apply(blink::CascadeFilter) + 508
8   libblink_core.dylib                 0x0000000122662ff0 blink::StyleResolver::ApplyAnimatedStyle(blink::StyleResolverState&, blink::StyleCascade&, blink::StyleRecalcContext const&) + 892
9   libblink_core.dylib                 0x0000000122661f50 blink::StyleResolver::ResolveStyle(blink::Element*, blink::StyleRecalcContext const&, blink::StyleRequest const&) + 624
10  libblink_core.dylib                 0x0000000122503a8c blink::Element::OriginalStyleForLayoutObject(blink::StyleRecalcContext const&) + 88
11  libblink_core.dylib                 0x0000000122503880 blink::Element::StyleForLayoutObject(blink::StyleRecalcContext const&) + 312
12  libblink_core.dylib                 0x0000000122505404 blink::Element::RecalcOwnStyle(blink::StyleRecalcChange, blink::StyleRecalcContext const&) + 572
13  libblink_core.dylib                 0x000000012250469c blink::Element::RecalcStyle(blink::StyleRecalcChange, blink::StyleRecalcContext const&) + 692
14  libblink_core.dylib                 0x0000000120ad1840 blink::StyleEngine::RecalcStyle(blink::StyleRecalcChange, blink::StyleRecalcContext const&) + 384
15  libblink_core.dylib                 0x0000000120ad32cc blink::StyleEngine::UpdateStyleAndLayoutTree() + 472
16  libblink_core.dylib                 0x00000001224811b4 blink::Document::UpdateStyle() + 292
17  libblink_core.dylib                 0x000000012247f5ac blink::Document::UpdateStyleAndLayoutTreeForThisDocument() + 1308
18  libblink_core.dylib                 0x00000001210cd59c blink::LocalFrameView::UpdateStyleAndLayoutInternal() + 284
19  libblink_core.dylib                 0x00000001210b8f58 blink::LocalFrameView::UpdateStyleAndLayout() + 528
20  libblink_core.dylib                 0x00000001224800ac blink::Document::UpdateStyleAndLayout(blink::DocumentUpdateReason) + 560
21  libblink_core.dylib                 0x0000000120ddaf4c blink::FrameSelection::ComputeAbsoluteBounds(gfx::Rect&, gfx::Rect&) const + 160
22  libblink_core.dylib                 0x0000000121188e98 blink::WebFrameWidgetImpl::CalculateSelectionBounds(gfx::Rect&, gfx::Rect&, gfx::Rect*) + 80
23  libblink_core.dylib                 0x0000000121188cc4 blink::WebFrameWidgetImpl::GetSelectionBoundsInWindow(gfx::Rect*, gfx::Rect*, gfx::Rect*, base::i18n::TextDirection*, base::i18n::TextDirection*, bool*) + 208
24  libblink_platform.dylib             0x000000011dbd9658 blink::WidgetBase::UpdateSelectionBounds() + 136
25  libblink_platform.dylib             0x000000011dbd9574 blink::WidgetBase::WillBeginMainFrame() + 92

```

The CL in [comment #7](https://issues.chromium.org/issues/407328533#comment7) was the removal of HTML imports, which likely (possibly?) just changed the timing of things?

The crash happens here:

<https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/css/resolver/style_cascade.cc;l=828;drc=d5af351cc29e7258499bad863b8e70298de981d2>

That was most recently touched by andruud@, so I'm going to move this over to him (now that I have access again).

### an...@chromium.org (2025-04-03)

Just from looking at the stack traces, it looks like we're holding a raw pointer (reference) to an InterpolationType (PartitionAlloc) that's owned by a PropertyRegistration (GC) that gets garbage collected---possibly because opening devtools / device emulator causes the custom property to re-register.

Interpolations holding on to raw pointers to InterpolationTypes *was* reasonable in a world without a custom properties, since CSSInterpolationTypesMap would allocate them in DEFINE\_STATIC\_LOCAL maps. For custom props, however, the ownership is left to the caller. Even if thorough analysis determines that this should *theoretically* be OK, it seems very fragile to me: the lifetime of various involved objects is too complicated to *easily* reason about. So, I think we should move InterpolationType to either Oilpan or RefCounted to make this more solid.

But this will be a largeish refactor (especially in the Oilpan case, which I recommend trying first), so Blink>Animations should decide what to do here.

### pe...@google.com (2025-04-03)

The issue's primary component must be in the Component Tags, so re-adding it. To change the primary component, use the edit button at the top of the issue, just above the title.

### nh...@chromium.org (2025-04-03)

flackr: based on [comment #15](https://issues.chromium.org/issues/407328533#comment15), this sounds like a Blink>Animation issue. Since this is a security bug, it should have an assignee. Can you find an appropriate owner for this bug?

### ch...@google.com (2025-04-18)

flackr: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-04-19)

flackr: Uh oh! This issue still open and hasn't been updated in the last 15 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-04-20)

flackr: Uh oh! This issue still open and hasn't been updated in the last 16 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-04-21)

flackr: Uh oh! This issue still open and hasn't been updated in the last 17 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-04-22)

flackr: Uh oh! This issue still open and hasn't been updated in the last 18 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-04-23)

flackr: Uh oh! This issue still open and hasn't been updated in the last 19 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-04-24)

flackr: Uh oh! This issue still open and hasn't been updated in the last 20 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-04-25)

flackr: Uh oh! This issue still open and hasn't been updated in the last 21 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### th...@chromium.org (2025-04-25)

[secondary shepherd] Hi flackr@, do you have any suggestions on a good owner for this bug? (will ping over chat as well)

### ch...@google.com (2025-04-26)

flackr: Uh oh! This issue still open and hasn't been updated in the last 22 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-04-27)

flackr: Uh oh! This issue still open and hasn't been updated in the last 23 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-04-28)

flackr: Uh oh! This issue still open and hasn't been updated in the last 24 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-04-29)

flackr: Uh oh! This issue still open and hasn't been updated in the last 25 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-04-30)

flackr: Uh oh! This issue still open and hasn't been updated in the last 26 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-05-01)

flackr: Uh oh! This issue still open and hasn't been updated in the last 27 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-05-02)

flackr: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### fl...@google.com (2025-05-02)

I've had a look at this and modified the test case to be a bit easier to reproduce. With this attached the crash pretty quickly reproduces after opening dev tools and turning on mobile emulation. The crash in blink::TransitionInterpolation::Apply is because the InterpolationType& type\_ has been deleted. Normally I think interpolation types are not erased during the lifetime of a document so we expect the reference saved by a running animation to remain valid, however, enabling device emulation results in a call to StyleEngine::ClearPropertyRules with the following stack:

```
#0  blink::PropertyRegistry::RemoveDeclaredProperties (this=0x17cc0042ecb0) at ../../third_party/blink/renderer/core/css/property_registry.cc:28
#1  0x00007f9ed6999f2e in blink::PropertyRegistration::RemoveDeclaredProperties (document=...)
    at ../../third_party/blink/renderer/core/css/property_registration.cc:266
#2  0x00007f9ed6b6086d in blink::StyleEngine::ClearPropertyRules (this=0x17cc00459ff8) at ../../third_party/blink/renderer/core/css/style_engine.cc:3319
#3  0x00007f9ed6b61a81 in blink::StyleEngine::ApplyRuleSetChanges
    (this=0x17cc00459ff8, tree_scope=..., old_style_sheets=..., new_style_sheets=..., diffs=...)
    at ../../third_party/blink/renderer/core/css/style_engine.cc:3038
#4  0x00007f9ed6c66371 in blink::TreeScopeStyleSheetCollection::ApplyActiveStyleSheetChanges (this=0x17cc0042df58, new_collection=...)
    at ../../third_party/blink/renderer/core/css/tree_scope_style_sheet_collection.cc:56
#5  0x00007f9ed666bae2 in blink::DocumentStyleSheetCollection::UpdateActiveStyleSheets (this=0x17cc0042df58, engine=...)
    at ../../third_party/blink/renderer/core/css/document_style_sheet_collection.cc:127
#6  0x00007f9ed6b4ab80 in blink::StyleEngine::UpdateActiveStyleSheets (this=0x17cc00459ff8)
    at ../../third_party/blink/renderer/core/css/style_engine.cc:685
#7  0x00007f9ed6b3fed3 in blink::StyleEngine::UpdateActiveStyle (this=0x17cc00459ff8) at ../../third_party/blink/renderer/core/css/style_engine.cc:763
#8  0x00007f9eda4a3bf4 in blink::Document::UpdateStyleAndLayoutTreeForThisDocument (this=0x17cc005015e8)
    at ../../third_party/blink/renderer/core/dom/document.cc:2473
#9  0x00007f9ed797ece9 in blink::LocalFrameView::UpdateStyleAndLayoutInternal (this=0x17cc00458780)
    at ../../third_party/blink/renderer/core/frame/local_frame_view.cc:3186
#10 0x00007f9ed795dc2f in blink::LocalFrameView::UpdateStyleAndLayout (this=0x17cc00458780)
    at ../../third_party/blink/renderer/core/frame/local_frame_view.cc:3130
#11 0x00007f9ed7973b3b in blink::LocalFrameView::UpdateStyleAndLayoutIfNeededRecursive (this=0x17cc00458780)
    at ../../third_party/blink/renderer/core/frame/local_frame_view.cc:3053
#12 0x00007f9ed796f66a in blink::LocalFrameView::RunStyleAndLayoutLifecyclePhases
    (this=0x17cc00458780, target_state=blink::DocumentLifecycle::kLayoutClean) at ../../third_party/blink/renderer/core/frame/local_frame_view.cc:2494
#13 0x00007f9ed796ec32 in blink::LocalFrameView::UpdateLifecyclePhasesInternal (this=0x17cc00458780, target_state=blink::DocumentLifecycle::kLayoutClean)
    at ../../third_party/blink/renderer/core/frame/local_frame_view.cc:2231
#14 0x00007f9ed796b52a in blink::LocalFrameView::UpdateLifecyclePhases
    (this=0x17cc00458780, target_state=blink::DocumentLifecycle::kLayoutClean, reason=blink::DocumentUpdateReason::kInspector)
    at ../../third_party/blink/renderer/core/frame/local_frame_view.cc:2163
#15 0x00007f9ed796d908 in blink::LocalFrameView::UpdateLifecycleToLayoutClean (this=0x17cc00458780, reason=blink::DocumentUpdateReason::kInspector)
    at ../../third_party/blink/renderer/core/frame/local_frame_view.cc:1967
#16 0x00007f9ed8362f38 in blink::DevToolsEmulator::EnableMobileEmulation (this=0x17cc0044d950)
    at ../../third_party/blink/renderer/core/inspector/dev_tools_emulator.cc:421
#17 0x00007f9ed8362aa0 in blink::DevToolsEmulator::EnableDeviceEmulation (this=0x17cc0044d950, params=...)
    at ../../third_party/blink/renderer/core/inspector/dev_tools_emulator.cc:346
#18 0x00007f9edb6e67ec in blink::WebViewImpl::ActivateDevToolsTransform (this=0xab4004f9000, params=...)
    at ../../third_party/blink/renderer/core/exported/web_view_impl.cc:3287
#19 0x00007f9ed7b80b1b in blink::WebFrameWidgetImpl::SetScreenMetricsEmulationParameters (this=0x17cc00455210, enabled=true, params=...)
    at ../../third_party/blink/renderer/core/frame/web_frame_widget_impl.cc:4759
#20 0x00007f9ed7afe654 in blink::ScreenMetricsEmulator::Apply (this=0x17cc00f5bdb8)
    at ../../third_party/blink/renderer/core/frame/screen_metrics_emulator.cc:140
#21 0x00007f9ed7afdf0e in blink::ScreenMetricsEmulator::ChangeEmulationParams (this=0x17cc00f5bdb8, params=...)
    at ../../third_party/blink/renderer/core/frame/screen_metrics_emulator.cc:52
#22 0x00007f9ed7b73df7 in blink::WebFrameWidgetImpl::EnableDeviceEmulation (this=0x17cc00455210, parameters=...)
    at ../../third_party/blink/renderer/core/frame/web_frame_widget_impl.cc:2356

```

Then it's just a matter of time before the erased interpolation type is collected and this crash is triggered.

It seems like this bug will fundamentally repro any time we call this function unless we find some way to correctly track and apply this update to running animations. Perhaps the simplest way to avoid this until a better mitigation can be worked out, though incorrect, would be to cancel any ongoing custom property animations?

### an...@chromium.org (2025-05-05)

> unless we find some way to correctly track and apply this update to running animations

I proposed a better way in <https://issues.chromium.org/issues/407328533#comment15>: moving interpolation types to Oilpan. What do you think about this?

The benefits of attempting to track this "ourselves" seem small vs. the risk of getting it wrong.

### fl...@google.com (2025-05-05)

> I proposed a better way in <https://issues.chromium.org/issues/407328533#comment15>: moving interpolation types to Oilpan. What do you think about this?

I'm worried this may change it from a use-after-free to an unexpected behavior issue. I.e. if the custom property is registered with a different type and running animations continue interpolating with the old type and new animations pick up the new type. Not that canceling animations is necessarily better, I think the only correct thing to do is recreate the interpolations using the new interpolation type.

### fl...@google.com (2025-05-05)

It seems like we do currently pick up if a property is registered on an already running animation, e.g. on <https://jsbin.com/nupuzur/edit?html,css,js,output> if you start the animation and then register the custom property it correctly updates the in progress animation to interpolate smoothly.

### fl...@google.com (2025-05-05)

Ah I see we call `document->GetStyleEngine().PropertyRegistryChanged();` when the property registry changes (in most cases - though notably it seems not in the AutoRegistration that dev tools performs). I guess when adding properties though this is fine because we just have a lag between no interpolation and the new interpolation however when removing properties we would have a potentially leaked pointer - so even if we do want the interpolation to update, it seems like the architecture we currently have only updates it "soon" rather than immediately so we should still make it all memory safe.

### fl...@google.com (2025-05-06)

I have this mostly coded up in <https://chromium-review.googlesource.com/c/chromium/src/+/6511917> but I'm still working on a crash in InvalidatableInterpolation::MaybeConvertUnderlyingValue in some of the tests.

### dx...@google.com (2025-05-07)

Project: chromium/src  

Branch: main  

Author: Robert Flack [flackr@chromium.org](mailto:flackr@chromium.org)  

Link:      <https://chromium-review.googlesource.com/6511917>

Make InterpolationType GarbageCollected.

---


Expand for full commit details
```
     
    Active interpolations keep pointers to the InterpolationType 
    however the referenced type can be deleted by calls to 
    blink::PropertyRegistry::RemoveDeclaredProperties. 
    Instead, we make InterpolationType garbage collected 
    so that active interpolations can safely use the old 
    interpolation type until it is updated. 
     
    Bug: 407328533 
    Change-Id: Ifb7661a4c663cbefadb9216221e679ad0e9eab97 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6511917 
    Reviewed-by: Kevin Ellis <kevers@chromium.org> 
    Reviewed-by: Anders Hartvoll Ruud <andruud@chromium.org> 
    Commit-Queue: Robert Flack <flackr@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1456895}

```

---

Files:

- M `third_party/blink/renderer/core/animation/BUILD.gn`
- M `third_party/blink/renderer/core/animation/animation_test.cc`
- M `third_party/blink/renderer/core/animation/css/css_animations.cc`
- M `third_party/blink/renderer/core/animation/css_aspect_ratio_interpolation_type.cc`
- M `third_party/blink/renderer/core/animation/css_basic_shape_interpolation_type.cc`
- M `third_party/blink/renderer/core/animation/css_border_image_length_box_interpolation_type.cc`
- M `third_party/blink/renderer/core/animation/css_clip_interpolation_type.cc`
- M `third_party/blink/renderer/core/animation/css_color_interpolation_type.cc`
- M `third_party/blink/renderer/core/animation/css_content_visibility_interpolation_type.cc`
- M `third_party/blink/renderer/core/animation/css_custom_list_interpolation_type.cc`
- M `third_party/blink/renderer/core/animation/css_custom_list_interpolation_type.h`
- M `third_party/blink/renderer/core/animation/css_default_interpolation_type.cc`
- M `third_party/blink/renderer/core/animation/css_default_interpolation_type.h`
- M `third_party/blink/renderer/core/animation/css_display_interpolation_type.cc`
- M `third_party/blink/renderer/core/animation/css_dynamic_range_limit_interpolation_type_test.cc`
- M `third_party/blink/renderer/core/animation/css_filter_list_interpolation_type.cc`
- M `third_party/blink/renderer/core/animation/css_font_palette_interpolation_type_test.cc`
- M `third_party/blink/renderer/core/animation/css_font_size_adjust_interpolation_type.cc`
- M `third_party/blink/renderer/core/animation/css_font_variation_settings_interpolation_type.cc`
- M `third_party/blink/renderer/core/animation/css_grid_template_property_interpolation_type.cc`
- M `third_party/blink/renderer/core/animation/css_image_interpolation_type.cc`
- M `third_party/blink/renderer/core/animation/css_image_list_interpolation_type.cc`
- M `third_party/blink/renderer/core/animation/css_image_slice_interpolation_type.cc`
- M `third_party/blink/renderer/core/animation/css_interpolation_type.cc`
- M `third_party/blink/renderer/core/animation/css_interpolation_type.h`
- M `third_party/blink/renderer/core/animation/css_intrinsic_length_interpolation_type.cc`
- M `third_party/blink/renderer/core/animation/css_length_interpolation_type.cc`
- M `third_party/blink/renderer/core/animation/css_length_list_interpolation_type.cc`
- M `third_party/blink/renderer/core/animation/css_offset_rotate_interpolation_type.cc`
- M `third_party/blink/renderer/core/animation/css_overlay_interpolation_type.cc`
- M `third_party/blink/renderer/core/animation/css_path_interpolation_type.cc`
- M `third_party/blink/renderer/core/animation/css_ray_interpolation_type.cc`
- M `third_party/blink/renderer/core/animation/css_rotate_interpolation_type.cc`
- M `third_party/blink/renderer/core/animation/css_scale_interpolation_type.cc`
- M `third_party/blink/renderer/core/animation/css_scrollbar_color_interpolation_type.cc`
- M `third_party/blink/renderer/core/animation/css_shadow_list_interpolation_type.cc`
- M `third_party/blink/renderer/core/animation/css_shape_interpolation_type.cc`
- M `third_party/blink/renderer/core/animation/css_size_list_interpolation_type.cc`
- M `third_party/blink/renderer/core/animation/css_text_indent_interpolation_type.cc`
- M `third_party/blink/renderer/core/animation/css_transform_interpolation_type.cc`
- M `third_party/blink/renderer/core/animation/css_translate_interpolation_type.cc`
- M `third_party/blink/renderer/core/animation/css_var_cycle_interpolation_type.cc`
- M `third_party/blink/renderer/core/animation/css_var_cycle_interpolation_type.h`
- M `third_party/blink/renderer/core/animation/css_visibility_interpolation_type.cc`
- M `third_party/blink/renderer/core/animation/interpolable_value_test.cc`
- M `third_party/blink/renderer/core/animation/interpolation_effect_test.cc`
- A `third_party/blink/renderer/core/animation/interpolation_type.cc`
- M `third_party/blink/renderer/core/animation/interpolation_type.h`
- M `third_party/blink/renderer/core/animation/interpolation_types_map.cc`
- M `third_party/blink/renderer/core/animation/interpolation_types_map.h`
- M `third_party/blink/renderer/core/animation/interpolation_types_map_test.cc`
- M `third_party/blink/renderer/core/animation/invalidatable_interpolation.cc`
- M `third_party/blink/renderer/core/animation/invalidatable_interpolation.h`
- M `third_party/blink/renderer/core/animation/list_interpolation_functions.cc`
- M `third_party/blink/renderer/core/animation/list_interpolation_functions.h`
- M `third_party/blink/renderer/core/animation/list_interpolation_functions_test.cc`
- M `third_party/blink/renderer/core/animation/path_interpolation_functions.cc`
- M `third_party/blink/renderer/core/animation/path_interpolation_functions.h`
- M `third_party/blink/renderer/core/animation/primitive_interpolation.h`
- M `third_party/blink/renderer/core/animation/transition_interpolation.cc`
- M `third_party/blink/renderer/core/animation/transition_interpolation.h`
- M `third_party/blink/renderer/core/animation/transition_keyframe.cc`
- M `third_party/blink/renderer/core/animation/typed_interpolation_value.h`
- M `third_party/blink/renderer/core/animation/underlying_value_owner.cc`
- M `third_party/blink/renderer/core/animation/underlying_value_owner.h`
- M `third_party/blink/renderer/core/css/property_registration.cc`
- M `third_party/blink/renderer/core/css/property_registration.h`

---

Hash: 3dc8b5b36eaa1d68f5caa5e36444fcb3e204d460  

Date:  Wed May 7 12:39:51 2025


---

### ch...@google.com (2025-05-08)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M136. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M137. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [136, 137].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### fl...@google.com (2025-05-08)

1. <https://chromium-review.googlesource.com/c/chromium/src/+/6511917> is the CL that fixed the issue.
2. I've verified the fix in Canary 138.0.7168.0 (Official Build) canary (arm64)
3. It's a non-trivial refactor across a lot of animations code - which is used in many different ways across the web. While it is pretty well tested, it would be hard to say with confidence that there isn't some risk of a stability regression. Additionally, being a large patch there is a big chance that it will not merge back cleanly.
4. There's no compatibility risks, no behavior has been changed.
5. The crash was not easy to automatically test, the repro steps in the OP or the alternate repro file in [#comment34](https://issues.chromium.org/issues/407328533#comment34) can be used to verify.

### am...@chromium.org (2025-05-09)

Since this is renderer memory corruption and has some preconditions to exploitation such as user interaction / direct engagement with devtools, I've lowered the severity.
Based on S2 severity, this fix would ordinarily be backmerge eligible for M137 Beta, however, in reviewing the fix, it's not only textually large this looks fairly risky due to the degree of changes in animation code.
Greatly appreciate the work here that went into this change, however, I'm going to decline backmerge for this fix given the risk to backmerge compatability and potential for stability issues.

### sp...@google.com (2025-05-16)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $4000.00 for this report.

Rationale for this decision:
$3,000 for report of mildly mitigated memory corruption in a sandboxed process / the renderer + $1,000 bisect bonus 


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-05-16)

Thank you for your efforts and reporting this issue to us!

### re...@gmail.com (2025-05-16)

thank you so much <3

### am...@chromium.org (2025-05-16)

💜

### ch...@google.com (2025-08-14)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> $3,000 for report of mildly mitigated memory corruption in a sandboxed process / the renderer + $1,000 bisect bonus

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/407328533)*
