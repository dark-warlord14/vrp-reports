# Memory corruption in blink::StyleColor

| Field | Value |
|-------|-------|
| **Issue ID** | [41495060](https://issues.chromium.org/issues/41495060) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Color |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | he...@gmail.com |
| **Assignee** | ke...@chromium.org |
| **Created** | 2024-01-26 |
| **Bounty** | $7,000.00 |

## Description

**Steps to reproduce the problem:**  

I'm still investigating the root cause and will attach more analysis soon.

Reproduction step:

./chrome --no-sandbox <http://localhost/poc.html>

**Problem Description:**  

renderer memory corruption

**Additional Comments:**

\*\*Chrome version: \*\* 123.0.6265.0 \*\*Channel: \*\* Canary

**OS:** Linux

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 13.5 KB)
- [harness.js](attachments/harness.js) (text/plain, 187.6 KB)
- [poc.html](attachments/poc.html) (text/plain, 408 B)
- [poc2.html](attachments/poc2.html) (text/plain, 373 B)

## Timeline

### he...@gmail.com (2024-01-26)

Note that this is reproduced on the 123.0.6265.0 Linux chromium without any additional flag.

### [Deleted User] (2024-01-26)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-26)

I'm able to repro with the POC as is and no interaction. For chromium devs working on this fix, please repro using the attached POC, but it appears some amount of interaction is needed to trigger it (opening devtools seems to work for that).

Repros in M121 and M123 but not M120. Repros on Linux and Mac, setting OS to all blink platforms assuming this isn't platform specific.

Symbolized stack trace from chromium-123.0.6262.5-linux-asan:

    #0 0x559b7fa00576 in ___interceptor_backtrace /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/../sanitizer_common/sanitizer_common_interceptors.inc:4358:13
    #1 0x559b93cb0228 in base::debug::CollectStackTrace(void const**, unsigned long) ./../../base/debug/stack_trace_posix.cc:1040:7
    #2 0x559b93c71f69 in StackTrace ./../../base/debug/stack_trace.cc:221:12
    #3 0x559b93c71f69 in base::debug::StackTrace::StackTrace() ./../../base/debug/stack_trace.cc:218:28
    #4 0x559b93cae9f2 in base::debug::(anonymous namespace)::StackDumpSignalHandler(int, siginfo_t*, void*) ./../../base/debug/stack_trace_posix.cc:458:3
    #5 0x7f22a1a42520 in __sigaction ??:?
    #6 0x559ba14e7190 in operator== ./../../third_party/blink/renderer/core/css/style_color.h:98:47
    #7 0x559ba14e7190 in blink::StyleColor::UnresolvedColorMix::Equals(blink::StyleColor::ColorOrUnresolvedColorMix const&, blink::StyleColor::ColorOrUnresolvedColorMix const&, blink::StyleColor::UnresolvedColorMix::UnderlyingColorType) ./../../third_party/blink/renderer/core/css/style_color.h:93:46
    #8 0x559ba3a4c401 in operator()<const blink::ComputedStyleBase::StyleBackgroundData &, const blink::ComputedStyleBase::StyleBackgroundData &> ./../../third_party/libc++/src/include/__functional/operations.h:309:35
    #9 0x559ba3a4c401 in ValuesEquivalent<blink::ComputedStyleBase::StyleBackgroundData, std::__Cr::equal_to<void> > ./../../base/memory/values_equivalent.h:33:10
    #10 0x559ba3a4c401 in ValuesEquivalent<cppgc::internal::BasicMember<blink::ComputedStyleBase::StyleBackgroundData, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy, cppgc::internal::CompressedPointer>, std::__Cr::equal_to<void> > ./../../base/memory/values_equivalent.h:70:10
    #11 0x559ba3a4c401 in blink::ComputedStyleBase::NonInheritedEqual(blink::ComputedStyleBase const&) const ./gen/third_party/blink/renderer/core/style/computed_style_base.h:428:12
    #12 0x559ba3a468a1 in NonInheritedEqual ./../../third_party/blink/renderer/core/style/computed_style.cc:785:29
    #13 0x559ba3a468a1 in blink::ComputedStyle::ComputeDifferenceIgnoringInheritedFirstLineStyle(blink::ComputedStyle const&, blink::ComputedStyle const&) ./../../third_party/blink/renderer/core/style/computed_style.cc:434:40
    #14 0x559ba3a4499d in blink::ComputedStyle::ComputeDifference(blink::ComputedStyle const*, blink::ComputedStyle const*) ./../../third_party/blink/renderer/core/style/computed_style.cc:404:7
    #15 0x559ba4e18014 in blink::Element::RecalcOwnStyle(blink::StyleRecalcChange, blink::StyleRecalcContext const&) ./../../third_party/blink/renderer/core/dom/element.cc:3914:7
    #16 0x559ba4e13b6d in blink::Element::RecalcStyle(blink::StyleRecalcChange, blink::StyleRecalcContext const&) ./../../third_party/blink/renderer/core/dom/element.cc:3585:20
    #17 0x559ba4bc6070 in blink::ContainerNode::RecalcDescendantStyles(blink::StyleRecalcChange, blink::StyleRecalcContext const&) ./../../third_party/blink/renderer/core/dom/container_node.cc:1378:22
    #18 0x559ba4e14846 in blink::Element::RecalcStyle(blink::StyleRecalcChange, blink::StyleRecalcContext const&) ./../../third_party/blink/renderer/core/dom/element.cc:3687:7
    #19 0x559ba4bc6070 in blink::ContainerNode::RecalcDescendantStyles(blink::StyleRecalcChange, blink::StyleRecalcContext const&) ./../../third_party/blink/renderer/core/dom/container_node.cc:1378:22
    #20 0x559ba4e14846 in blink::Element::RecalcStyle(blink::StyleRecalcChange, blink::StyleRecalcContext const&) ./../../third_party/blink/renderer/core/dom/element.cc:3687:7
    #21 0x559ba4bc6070 in blink::ContainerNode::RecalcDescendantStyles(blink::StyleRecalcChange, blink::StyleRecalcContext const&) ./../../third_party/blink/renderer/core/dom/container_node.cc:1378:22
    #22 0x559ba4e14846 in blink::Element::RecalcStyle(blink::StyleRecalcChange, blink::StyleRecalcContext const&) ./../../third_party/blink/renderer/core/dom/element.cc:3687:7
    #23 0x559ba0dfa6bd in blink::StyleEngine::RecalcStyle(blink::StyleRecalcChange, blink::StyleRecalcContext const&) ./../../third_party/blink/renderer/core/css/style_engine.cc:3500:16
    #24 0x559ba0dfed53 in blink::StyleEngine::RecalcStyle() ./../../third_party/blink/renderer/core/css/style_engine.cc:3537:3
    #25 0x559ba0dff9d3 in blink::StyleEngine::UpdateStyleAndLayoutTree() ./../../third_party/blink/renderer/core/css/style_engine.cc:3654:7
    #26 0x559ba4bffe3c in blink::Document::UpdateStyle() ./../../third_party/blink/renderer/core/dom/document.cc:2386:16
    #27 0x559ba4bfdc92 in blink::Document::UpdateStyleAndLayoutTreeForThisDocument() ./../../third_party/blink/renderer/core/dom/document.cc:2330:3
    #28 0x559ba1a6645c in blink::LocalFrameView::UpdateStyleAndLayoutInternal() ./../../third_party/blink/renderer/core/frame/local_frame_view.cc:3139:30
    #29 0x559ba1a5061b in blink::LocalFrameView::UpdateStyleAndLayout() ./../../third_party/blink/renderer/core/frame/local_frame_view.cc:3087:18
    #30 0x559ba1a5ef7c in blink::LocalFrameView::UpdateStyleAndLayoutIfNeededRecursive() ./../../third_party/blink/renderer/core/frame/local_frame_view.cc:3011:3
    #31 0x559ba1a5c05f in blink::LocalFrameView::RunStyleAndLayoutLifecyclePhases(blink::DocumentLifecycle::LifecycleState) ./../../third_party/blink/renderer/core/frame/local_frame_view.cc:2456:3
    #32 0x559ba1a5ae24 in blink::LocalFrameView::UpdateLifecyclePhasesInternal(blink::DocumentLifecycle::LifecycleState) ./../../third_party/blink/renderer/core/frame/local_frame_view.cc:2221:9
    #33 0x559ba1a58b29 in blink::LocalFrameView::UpdateLifecyclePhases(blink::DocumentLifecycle::LifecycleState, blink::DocumentUpdateReason) ./../../third_party/blink/renderer/core/frame/local_frame_view.cc:2153:3
    #34 0x559ba1a5818e in blink::LocalFrameView::UpdateAllLifecyclePhases(blink::DocumentUpdateReason) ./../../third_party/blink/renderer/core/frame/local_frame_view.cc:1903:54
    #35 0x559ba34a421e in blink::PageAnimator::UpdateAllLifecyclePhases(blink::LocalFrame&, blink::DocumentUpdateReason) ./../../third_party/blink/renderer/core/page/page_animator.cc:394:9
    #36 0x559ba1bdf87e in blink::WebFrameWidgetImpl::UpdateLifecycle(blink::WebLifecycleUpdate, blink::DocumentUpdateReason) ./../../third_party/blink/renderer/core/frame/web_frame_widget_impl.cc:1547:14
    #37 0x559ba4811326 in UpdateVisualState ./../../third_party/blink/renderer/platform/widget/widget_base.cc:991:12
    #38 0x559ba4811326 in non-virtual thunk to blink::WidgetBase::UpdateVisualState() ./../../third_party/blink/renderer/platform/widget/widget_base.cc:0:0
    #39 0x559b9907121d in cc::LayerTreeHost::RequestMainFrameUpdate(bool) ./../../cc/trees/layer_tree_host.cc:376:12
    #40 0x559b993944cf in cc::ProxyMain::BeginMainFrame(std::__Cr::unique_ptr<cc::BeginMainFrameAndCommitState, std::__Cr::default_delete<cc::BeginMainFrameAndCommitState> >) ./../../cc/trees/proxy_main.cc:283:21
    #41 0x559b993be0ea in Invoke<void (cc::ProxyMain::*)(std::__Cr::unique_ptr<cc::BeginMainFrameAndCommitState, std::__Cr::default_delete<cc::BeginMainFrameAndCommitState> >), const base::WeakPtr<cc::ProxyMain> &, std::__Cr::unique_ptr<cc::BeginMainFrameAndCommitState, std::__Cr::default_delete<cc::BeginMainFrameAndCommitState> > > ./../../base/functional/bind_internal.h:710:12
    #42 0x559b993be0ea in MakeItSo<void (cc::ProxyMain::*)(std::__Cr::unique_ptr<cc::BeginMainFrameAndCommitState, std::__Cr::default_delete<cc::BeginMainFrameAndCommitState> >), std::__Cr::tuple<base::WeakPtr<cc::ProxyMain>, std::__Cr::unique_ptr<cc::BeginMainFrameAndCommitState, std::__Cr::default_delete<cc::BeginMainFrameAndCommitState> >
> > ./../../base/functional/bind_internal.h:881:5
    #43 0x559b993be0ea in void base::internal::Invoker<base::internal::BindState<void (cc::ProxyMain::*)(std::__Cr::unique_ptr<cc::BeginMainFrameAndCommitState, std::__Cr::default_delete<cc::BeginMainFrameAndCommitState> >), base::WeakPtr<cc::ProxyMain>, std::__Cr::unique_ptr<cc::BeginMainFrameAndCommitState, std::__Cr::default_delete<cc::BeginMainFrameAndCommitState> > >, void ()>::RunImpl<void (cc::ProxyMain::*)(std::__Cr::unique_ptr<cc::BeginMainFrameAndCommitState, std::__Cr::default_delete<cc::BeginMainFrameAndCommitState> >), std::__Cr::tuple<base::WeakPtr<cc::ProxyMain>, std::__Cr::unique_ptr<cc::BeginMainFrameAndCommitState, std::__Cr::default_delete<cc::BeginMainFrameAndCommitState> > >, 0ul, 1ul>(void (cc::ProxyMain::*&&)(std::__Cr::unique_ptr<cc::BeginMainFrameAndCommitState, std::__Cr::default_delete<cc::BeginMainFrameAndCommitState> >), std::__Cr::tuple<base::WeakPtr<cc::ProxyMain>, std::__Cr::unique_ptr<cc::BeginMainFrameAndCommitState, std::__Cr::default_delete<cc::BeginMainFrameAndCommitState> > >&&, std::__Cr::integer_sequence<unsigned long, 0ul, 1ul>) ./../../base/functional/bind_internal.h:991:14
    #44 0x559b93b08c40 in Run ./../../base/functional/callback.h:156:12
    #45 0x559b93b08c40 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task_annotator.cc:201:34
    #46 0x559b93b720e5 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:480:11)> ./../../base/task/common/task_annotator.h:89:5
    #47 0x559b93b720e5 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:478:23
    #48 0x559b93b70dde in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:343:41
    #49 0x559b93b7315b in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0:0
    #50 0x559b939e62b0 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_default.cc:40:55
    #51 0x559b93b740d0 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:646:12
    #52 0x559b93a91603 in base::RunLoop::Run(base::Location const&) ./../../base/run_loop.cc:134:14
    #53 0x559bad1c72d9 in content::RendererMain(content::MainFunctionParams) ./../../content/renderer/renderer_main.cc:367:16
    #54 0x559b90ab2120 in content::RunZygote(content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:676:14
    #55 0x559b90ab38b5 in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> > const&, content::MainFunctionParams, content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:780:12
    #56 0x559b90ab688a in content::ContentMainRunnerImpl::Run() ./../../content/app/content_main_runner_impl.cc:1142:10
    #57 0x559b90aaffa6 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) ./../../content/app/content_main.cc:335:36
    #58 0x559b90ab0663 in content::ContentMain(content::ContentMainParams) ./../../content/app/content_main.cc:348:10
    #59 0x559b7fa8ae8e in ChromeMain ./../../chrome/app/chrome_main.cc:194:12
    #60 0x7f22a1a29d90 in __libc_init_first ??:?
    #61 0x7f22a1a29e40 in __libc_start_main ??:0:0
    #62 0x559b7f9be02a in _start ??:0:0



[Monorail components: Blink>Color]

### [Deleted User] (2024-01-26)

[Empty comment from Monorail migration]

### he...@gmail.com (2024-01-27)

Note that the original Poc.html doesn’t require interaction. I agree with that the modified poc2.html probably needs some interaction. Thanks.

### [Deleted User] (2024-01-27)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2024-01-27)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-28)

[Empty comment from Monorail migration]

### ke...@chromium.org (2024-01-29)

Found the problem.  Fix in review.

### gi...@appspot.gserviceaccount.com (2024-01-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/ed24de7484625cf4f68a1bee69c76f82c14507c2

commit ed24de7484625cf4f68a1bee69c76f82c14507c2
Author: Kevin Ellis <kevers@google.com>
Date: Tue Jan 30 14:22:25 2024

Fix StyleColor::UnresolvedColorMix::operator==

Bug: 1522095
Change-Id: Ib9b41c8b865aeb72ac1881503639231faaf68c40
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5245748
Commit-Queue: Kevin Ellis <kevers@chromium.org>
Reviewed-by: Aaron Krajeski <aaronhk@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1253884}

[modify] https://crrev.com/ed24de7484625cf4f68a1bee69c76f82c14507c2/third_party/blink/renderer/core/css/style_color.h
[add] https://crrev.com/ed24de7484625cf4f68a1bee69c76f82c14507c2/third_party/blink/web_tests/external/wpt/css/css-backgrounds/animations/background-color-transition-colormix.html
[modify] https://crrev.com/ed24de7484625cf4f68a1bee69c76f82c14507c2/third_party/blink/renderer/core/css/style_color.cc


### ke...@chromium.org (2024-01-30)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-30)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-30)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-30)

This issue was migrated from crbug.com/chromium/1522095?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-02-04)

Requesting merge to beta (M122) because latest trunk commit (1253884) appears to be after beta branch point (1250580).
Merge approved: your change passed merge requirements and is auto-approved for M122. Please go ahead and merge the CL to branch 6261 (refs/branch-heads/6261) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: eakpobaro (Android), eakpobaro (iOS), ceb (ChromeOS), pbommana (Desktop)
Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [122].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


### ke...@google.com (2024-02-05)

1. https://chromium-review.googlesource.com/c/chromium/src/+/5245748
2. Yes. The fix has been verified in Canary via an automated test.
3. No. The fix is very isolated to the source of the memory corruption.
4. No compatibility risks.
5. No manual testing required. Covered by an automated test in the same CL.

### ap...@google.com (2024-02-06)

Project: chromium/src
Branch: refs/branch-heads/6261

commit d3590f7793ea97e475a1162fa30976d86fae8458
Author: Kevin Ellis <kevers@google.com>
Date:   Tue Feb 06 13:12:31 2024

    Fix StyleColor::UnresolvedColorMix::operator==
    
    (cherry picked from commit ed24de7484625cf4f68a1bee69c76f82c14507c2)
    
    Bug: 1522095
    Change-Id: Ib9b41c8b865aeb72ac1881503639231faaf68c40
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5245748
    Commit-Queue: Kevin Ellis <kevers@chromium.org>
    Reviewed-by: Aaron Krajeski <aaronhk@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1253884}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5269965
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Cr-Commit-Position: refs/branch-heads/6261@{#517}
    Cr-Branched-From: 9755d9d81e4a8cb5b4f76b23b761457479dbb06b-refs/heads/main@{#1250580}

M       third_party/blink/renderer/core/css/style_color.cc
M       third_party/blink/renderer/core/css/style_color.h
A       third_party/blink/web_tests/external/wpt/css/css-backgrounds/animations/background-color-transition-colormix.html

https://chromium-review.googlesource.com/5269965


### pe...@google.com (2024-02-06)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-02-06)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-02-06)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-02-06)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-02-06)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-02-06)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-02-06)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-02-06)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-02-06)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-02-06)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-02-06)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-02-06)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-02-06)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-02-06)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-02-06)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-02-06)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-02-06)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-02-06)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-02-06)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-02-06)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-02-06)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-02-06)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-02-06)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-02-06)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-02-06)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-02-06)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-02-06)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-02-06)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-02-06)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-02-06)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-02-06)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-02-06)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-02-06)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-02-06)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-02-06)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-02-06)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### ke...@google.com (2024-02-06)

This does not need a merge into M120.  The issue was a regression in the version in which it was found, and related to a change in a later version.




### pe...@google.com (2024-02-06)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-02-06)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-02-06)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-02-06)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-02-06)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-02-06)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-02-06)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-02-07)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-02-07)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-02-07)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-02-07)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-02-07)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-02-07)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-02-07)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-02-07)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-02-07)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-02-07)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-02-07)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-02-07)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-02-07)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-02-07)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-02-07)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-02-07)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-02-07)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-02-07)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-02-07)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-02-07)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-02-07)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-02-07)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-02-07)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-02-07)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-02-07)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-02-07)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-02-07)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-02-07)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-02-07)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-02-07)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-02-07)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-02-07)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-02-07)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-02-07)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-02-07)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-02-07)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-02-07)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-02-07)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-02-07)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-02-07)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-02-07)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-02-07)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-02-07)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-02-07)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-02-07)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-02-07)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-02-07)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-02-07)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-02-07)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-02-07)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-02-07)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-02-07)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-02-07)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### ke...@google.com (2024-02-07)

Can someone from the blintz team please look into why this issue is getting spammed with updates. Thanks.

Replied to the request that it does NOT need a merge in comment #55.

### pe...@google.com (2024-02-07)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-02-07)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-02-07)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-02-07)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-02-07)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-02-07)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-02-07)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-02-07)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-02-07)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pg...@google.com (2024-02-07)

Not a Chrome OS Blintz rule owner, but looking at [this code](https://source.corp.google.com/piper///depot/google3/buzz/test/blintz/runners/peeps/chromeos_blintz.py;l=282?q=%22This%20issue%20has%20been%20flagged%20as%20a%20merge%20candidate%20for%20Chrome%20O%22) assuming this label might do the trick

### am...@google.com (2024-02-14)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2024-02-14)

Congratulations! The Chrome VRP Panel has decided to award you $7,000 for this report of renderer / sandboxed process memory corruption. Thank you for your efforts and reporting this issue to us -- nice work!

### he...@gmail.com (2024-02-15)

Thanks Amy! Cheers for the first bounty on the new issue tracker🍻 

### na...@google.com (2024-02-18)

Based on comment#4 & #16, this issue does not impact LTS-114.

### pe...@google.com (2024-05-08)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/41495060)*
