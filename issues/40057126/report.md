# Security: Security DCHECK failure at blink::LayoutInline

| Field | Value |
|-------|-------|
| **Issue ID** | [40057126](https://issues.chromium.org/issues/40057126) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>Internals>WTF, Blink>Layout |
| **Platforms** | Android, Linux, Windows |
| **Reporter** | ao...@gmail.com |
| **Assignee** | ik...@chromium.org |
| **Created** | 2021-09-01 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**  

The attached page triggers a security dcheck, which is there to help detect bad casts.

**VERSION**  

Chrome Version: Chromium 95.0.4624.0 beta (prebuilt asan)  

Operating System: Linux

**REPRODUCTION CASE**  

Open the attached file. Issue should reproduce every time.

# **FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION** Type of crash: tab Crash State: AddressSanitizer:DEADLYSIGNAL

==234251==ERROR: AddressSanitizer: ABRT on unknown address 0x03e80003930b (pc 0x7f3b8227e18b bp 0x7ffed3706c30 sp 0x7ffed37069e0 T0)  

SCARINESS: 10 (signal)  

#0 0x7f3b8227e18b in raise /build/glibc-eX1tMB/glibc-2.31/signal/../sysdeps/unix/sysv/linux/raise.c:51:1  

#1 0x55ff9000d54e in logging::LogMessage::~LogMessage() base/logging.cc:891:7  

#2 0x55ff9dc8cc6a in To<blink::LayoutInline, blink::LayoutObject> third\_party/blink/renderer/platform/wtf/casting.h:115:3  

#3 0x55ff9dc8cc6a in blink::LayoutInline const\* blink::To<blink::LayoutInline, blink::LayoutObject>(blink::LayoutObject const\*) third\_party/blink/renderer/platform/wtf/casting.h:121:18  

#4 0x55ff9dc75add in blink::NGOutOfFlowLayoutPart::Run(blink::LayoutBox const\*) third\_party/blink/renderer/core/layout/ng/ng\_out\_of\_flow\_layout\_part.cc:174:34  

#5 0x55ff9db78529 in blink::NGBlockLayoutAlgorithm::FinishLayout(blink::NGPreviousInflowPosition\*, blink::NGInlineChildLayoutContext\*) third\_party/blink/renderer/core/layout/ng/ng\_block\_layout\_algorithm.cc:962:73  

#6 0x55ff9db74b8e in blink::NGBlockLayoutAlgorithm::Layout(blink::NGInlineChildLayoutContext\*) third\_party/blink/renderer/core/layout/ng/ng\_block\_layout\_algorithm.cc:751:10  

#7 0x55ff9db71ea9 in blink::NGBlockLayoutAlgorithm::Layout() third\_party/blink/renderer/core/layout/ng/ng\_block\_layout\_algorithm.cc:439:14  

#8 0x55ff9db62c80 in operator() third\_party/blink/renderer/core/layout/ng/ng\_block\_node.cc:207:50  

#9 0x55ff9db62c80 in void blink::(anonymous namespace)::CreateAlgorithmAndRun<blink::NGBlockLayoutAlgorithm, blink::(anonymous namespace)::LayoutWithAlgorithm(blink::NGLayoutAlgorithmParams const&)::'lambda'(blink::NGLayoutAlgorithmOperations\*)>(blink::NGLayoutAlgorithmParams const&, blink::(anonymous namespace)::LayoutWithAlgorithm(blink::NGLayoutAlgorithmParams const&)::'lambda'(blink::NGLayoutAlgorithmOperations\*) const&) third\_party/blink/renderer/core/layout/ng/ng\_block\_node.cc:116:3  

#10 0x55ff9db46d5d in LayoutWithAlgorithm third\_party/blink/renderer/core/layout/ng/ng\_block\_node.cc:205:3  

#11 0x55ff9db46d5d in blink::NGBlockNode::Layout(blink::NGConstraintSpace const&, blink::NGBlockBreakToken const\*, blink::NGEarlyBreak const\*) const third\_party/blink/renderer/core/layout/ng/ng\_block\_node.cc:510:21  

#12 0x55ff9db8cef5 in LayoutBlockChild third\_party/blink/renderer/core/layout/ng/ng\_block\_layout\_algorithm.cc:105:16  

#13 0x55ff9db8cef5 in blink::(anonymous namespace)::LayoutInflow(blink::NGConstraintSpace const&, blink::NGBreakToken const\*, blink::NGEarlyBreak const\*, blink::NGLayoutInputNode\*, blink::NGInlineChildLayoutContext\*) third\_party/blink/renderer/core/layout/ng/ng\_block\_layout\_algorithm.cc:117:10  

#14 0x55ff9db8beac in blink::NGBlockLayoutAlgorithm::HandleInflow(blink::NGLayoutInputNode, blink::NGBreakToken const\*, blink::NGPreviousInflowPosition\*, blink::NGInlineChildLayoutContext\*, scoped\_refptr<blink::NGInlineBreakToken const>\*) third\_party/blink/renderer/core/layout/ng/ng\_block\_layout\_algorithm.cc:1653:7  

#15 0x55ff9db74308 in blink::NGBlockLayoutAlgorithm::Layout(blink::NGInlineChildLayoutContext\*) third\_party/blink/renderer/core/layout/ng/ng\_block\_layout\_algorithm.cc:692:18  

#16 0x55ff9db71ea9 in blink::NGBlockLayoutAlgorithm::Layout() third\_party/blink/renderer/core/layout/ng/ng\_block\_layout\_algorithm.cc:439:14  

#17 0x55ff9db62c80 in operator() third\_party/blink/renderer/core/layout/ng/ng\_block\_node.cc:207:50  

#18 0x55ff9db62c80 in void blink::(anonymous namespace)::CreateAlgorithmAndRun<blink::NGBlockLayoutAlgorithm, blink::(anonymous namespace)::LayoutWithAlgorithm(blink::NGLayoutAlgorithmParams const&)::'lambda'(blink::NGLayoutAlgorithmOperations\*)>(blink::NGLayoutAlgorithmParams const&, blink::(anonymous namespace)::LayoutWithAlgorithm(blink::NGLayoutAlgorithmParams const&)::'lambda'(blink::NGLayoutAlgorithmOperations\*) const&) third\_party/blink/renderer/core/layout/ng/ng\_block\_node.cc:116:3  

#19 0x55ff9db46d5d in LayoutWithAlgorithm third\_party/blink/renderer/core/layout/ng/ng\_block\_node.cc:205:3  

#20 0x55ff9db46d5d in blink::NGBlockNode::Layout(blink::NGConstraintSpace const&, blink::NGBlockBreakToken const\*, blink::NGEarlyBreak const\*) const third\_party/blink/renderer/core/layout/ng/ng\_block\_node.cc:510:21  

#21 0x55ff9dc899e3 in blink::NGOutOfFlowLayoutPart::GenerateFragment(blink::NGBlockNode, blink::LogicalSize const&, absl::optional[blink::LayoutUnit](javascript:void(0);) const&, blink::NGLogicalOutOfFlowDimensions const&, blink::LayoutUnit, blink::NGBlockBreakToken const\*, blink::NGConstraintSpace const\*, bool) third\_party/blink/renderer/core/layout/ng/ng\_out\_of\_flow\_layout\_part.cc:1342:15  

#22 0x55ff9dc88cd2 in blink::NGOutOfFlowLayoutPart::Layout(blink::NGOutOfFlowLayoutPart::NodeToLayout const&, blink::NGOutOfFlowLayoutPart::OffsetInfo const&, blink::NGConstraintSpace const\*) third\_party/blink/renderer/core/layout/ng/ng\_out\_of\_flow\_layout\_part.cc:1252:21  

#23 0x55ff9dc7d875 in blink::NGOutOfFlowLayoutPart::LayoutOOFNode(blink::NGOutOfFlowLayoutPart::NodeToLayout const&, blink::LayoutBox const\*, blink::NGConstraintSpace const\*) third\_party/blink/renderer/core/layout/ng/ng\_out\_of\_flow\_layout\_part.cc:1110:9  

#24 0x55ff9dc79117 in blink::NGOutOfFlowLayoutPart::LayoutCandidates(WTF::Vector<blink::NGLogicalOutOfFlowPositionedNode, 0u, WTF::PartitionAllocator>\*, blink::LayoutBox const\*, WTF::Hash  

Set<blink::LayoutObject const\*, WTF::PtrHash<blink::LayoutObject const>, WTF::HashTraits<blink::LayoutObject const\*>, WTF::PartitionAllocator>\*) third\_party/blink/renderer/core/layout/ng/ng\_o  

ut\_of\_flow\_layout\_part.cc:650:13  

#25 0x55ff9dc75587 in blink::NGOutOfFlowLayoutPart::Run(blink::LayoutBox const\*) third\_party/blink/renderer/core/layout/ng/ng\_out\_of\_flow\_layout\_part.cc:197:3  

#26 0x55ff9db01127 in blink::LayoutNGMixin[blink::LayoutBlockFlow](javascript:void(0);)::UpdateOutOfFlowBlockLayout() third\_party/blink/renderer/core/layout/ng/layout\_ng\_mixin.cc:381:8  

#27 0x55ff9dad830b in blink::LayoutNGBlockFlowMixin[blink::LayoutBlockFlow](javascript:void(0);)::UpdateNGBlockLayout() third\_party/blink/renderer/core/layout/ng/layout\_ng\_block\_flow\_mixin.cc:264:26  

#28 0x55ff9d4bc1bd in blink::LayoutBlock::UpdateLayout() third\_party/blink/renderer/core/layout/layout\_block.cc:431:3  

#29 0x55ff9d4c4483 in LayoutIfNeeded third\_party/blink/renderer/core/layout/layout\_object.h:2189:7  

#30 0x55ff9d4c4483 in blink::LayoutBlock::LayoutPositionedObject(blink::LayoutBox\*, bool, blink::LayoutBlock::PositionedLayoutBehavior) third\_party/blink/renderer/core/layout/layout\_block  

.cc:967:22  

#31 0x55ff9d4c338c in blink::LayoutBlock::LayoutPositionedObjects(bool, blink::LayoutBlock::PositionedLayoutBehavior) third\_party/blink/renderer/core/layout/layout\_block.cc:881:5  

#32 0x55ff9d4fa84d in blink::LayoutBlockFlow::UpdateBlockLayout(bool) third\_party/blink/renderer/core/layout/layout\_block\_flow.cc:523:3  

#33 0x55ff9d8c875d in blink::LayoutView::UpdateBlockLayout(bool) third\_party/blink/renderer/core/layout/layout\_view.cc:323:20  

#34 0x55ff9d4bc1bd in blink::LayoutBlock::UpdateLayout() third\_party/blink/renderer/core/layout/layout\_block.cc:431:3  

#35 0x55ff9d8c9436 in blink::LayoutView::UpdateLayout() third\_party/blink/renderer/core/layout/layout\_view.cc:364:20  

#36 0x55ff9c003670 in blink::LocalFrameView::PerformLayout() third\_party/blink/renderer/core/frame/local\_frame\_view.cc:837:24  

#37 0x55ff9c0058dc in blink::LocalFrameView::UpdateLayout() third\_party/blink/renderer/core/frame/local\_frame\_view.cc:895:3  

#38 0x55ff9c0282f3 in blink::LocalFrameView::UpdateStyleAndLayoutInternal() third\_party/blink/renderer/core/frame/local\_frame\_view.cc:3314:5  

#39 0x55ff9c00eaa5 in blink::LocalFrameView::UpdateStyleAndLayout() third\_party/blink/renderer/core/frame/local\_frame\_view.cc:3254:21  

#40 0x55ff9c01d4e8 in blink::LocalFrameView::UpdateStyleAndLayoutIfNeededRecursive() third\_party/blink/renderer/core/frame/local\_frame\_view.cc:3174:3  

#41 0x55ff9c0198ec in blink::LocalFrameView::RunStyleAndLayoutLifecyclePhases(blink::DocumentLifecycle::LifecycleState) third\_party/blink/renderer/core/frame/local\_frame\_view.cc:2557:3  

#42 0x55ff9c0186be in blink::LocalFrameView::UpdateLifecyclePhasesInternal(blink::DocumentLifecycle::LifecycleState) third\_party/blink/renderer/core/frame/local\_frame\_view.cc:2409:9  

#43 0x55ff9c01605f in blink::LocalFrameView::UpdateLifecyclePhases(blink::DocumentLifecycle::LifecycleState, blink::DocumentUpdateReason) third\_party/blink/renderer/core/frame/local\_frame\_view.cc:2350:3  

#44 0x55ff9c015abd in blink::LocalFrameView::UpdateAllLifecyclePhases(blink::DocumentUpdateReason) third\_party/blink/renderer/core/frame/local\_frame\_view.cc:2101:54  

#45 0x55ff9e042b59 in blink::PageAnimator::UpdateAllLifecyclePhases(blink::LocalFrame&, blink::DocumentUpdateReason) third\_party/blink/renderer/core/page/page\_animator.cc:149:9  

#46 0x55ff9cb88976 in blink::WebFrameWidgetImpl::UpdateLifecycle(blink::WebLifecycleUpdate, blink::DocumentUpdateReason) third\_party/blink/renderer/core/frame/web\_frame\_widget\_impl.cc:1280:3  

#47 0x55ff9f280fe3 in UpdateVisualState third\_party/blink/renderer/platform/widget/widget\_base.cc:786:12  

#48 0x55ff9f280fe3 in non-virtual thunk to blink::WidgetBase::UpdateVisualState() third\_party/blink/renderer/platform/widget/widget\_base.cc  

#49 0x55ff9411b6ac in cc::LayerTreeHost::RequestMainFrameUpdate(bool) cc/trees/layer\_tree\_host.cc:308:12  

#50 0x55ff94322ec6 in cc::ProxyMain::BeginMainFrame(std::\_\_1::unique\_ptr<cc::BeginMainFrameAndCommitState, std::\_\_1::default\_delete[cc::BeginMainFrameAndCommitState](javascript:void(0);) >) cc/trees/proxy\_main.cc:247:21  

#51 0x55ff94335b73 in Invoke<void (cc::ProxyMain::\*)(std::unique\_ptr[cc::BeginMainFrameAndCommitState](javascript:void(0);)), base::WeakPtr[cc::ProxyMain](javascript:void(0);), std::unique\_ptr[cc::BeginMainFrameAndCommitState](javascript:void(0);) > base/bind\_internal.h:509:12  

#52 0x55ff94335b73 in MakeItSo<void (cc::ProxyMain::\*)(std::unique\_ptr[cc::BeginMainFrameAndCommitState](javascript:void(0);)), base::WeakPtr[cc::ProxyMain](javascript:void(0);), std::unique\_ptr[cc::BeginMainFrameAndCommitState](javascript:void(0);) > base/bind\_internal.h:668:5  

#53 0x55ff94335b73 in RunImpl<void (cc::ProxyMain::\*)(std::unique\_ptr[cc::BeginMainFrameAndCommitState](javascript:void(0);)), std::tuple<base::WeakPtr[cc::ProxyMain](javascript:void(0);), std::unique\_ptr[cc::BeginMainFrameAndCommitState](javascript:void(0);) >, 0UL, 1UL> base/bind\_internal.h:721:12  

#54 0x55ff94335b73 in base::internal::Invoker<base::internal::BindState<void (cc::ProxyMain::\*)(std::\_\_1::unique\_ptr<cc::BeginMainFrameAndCommitState, std::\_\_1::default\_delete[cc::BeginMainFrameAndCommitState](javascript:void(0);) >), base::WeakPtr[cc::ProxyMain](javascript:void(0);), std::\_\_1::unique\_ptr<cc::BeginMainFrameAndCommitState, std::\_\_1::default\_delete[cc::BeginMainFrameAndCommitState](javascript:void(0);) > >, void ()>::RunOnce(base::internal::BindStateBase\*) base/bind\_internal.h:690:12  

#55 0x55ff9012c330 in Run base/callback.h:98:12  

#56 0x55ff9012c330 in base::TaskAnnotator::RunTask(char const\*, base::PendingTask\*) base/task/common/task\_annotator.cc:178:33  

#57 0x55ff901665e9 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence\_manager::LazyNow\*) base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:360:23  

#58 0x55ff90165d5a in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:260:36  

#59 0x55ff90166f91 in non-virtual thunk to base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc  

#60 0x55ff900249df in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) base/message\_loop/message\_pump\_default.cc:39:55  

#61 0x55ff90167654 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:467:12  

#62 0x55ff900a7a31 in base::RunLoop::Run(base::Location const&) base/run\_loop.cc:134:14  

#63 0x55ffa3786db1 in content::RendererMain(content::MainFunctionParams const&) content/renderer/renderer\_main.cc:261:16  

#64 0x55ff8ef60150 in content::RunZygote(content::ContentMainDelegate\*) content/app/content\_main\_runner\_impl.cc:569:14  

#65 0x55ff8ef63034 in content::ContentMainRunnerImpl::Run(bool) content/app/content\_main\_runner\_impl.cc:955:10  

#66 0x55ff8ef5d949 in content::RunContentProcess(content::ContentMainParams const&, content::ContentMainRunner\*) content/app/content\_main.cc:386:36  

#67 0x55ff8ef5de7c in content::ContentMain(content::ContentMainParams const&) content/app/content\_main.cc:412:10  

#68 0x55ff82ccae2d in ChromeMain chrome/app/chrome\_main.cc:151:12  

#69 0x7f3b8225f0b2 in \_\_libc\_start\_main /build/glibc-eX1tMB/glibc-2.31/csu/../csu/libc-start.c:308:16

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: Aki Helin

## Attachments

- crash-sdcheck-layoutline.html (text/plain, 1.7 KB)

## Timeline

### [Deleted User] (2021-09-01)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-09-02)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4984937508569088.

### cl...@chromium.org (2021-09-02)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-09-02)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-09-02)

[Empty comment from Monorail migration]

### do...@chromium.org (2021-09-02)

ClusterFuzz reproduces the security DCHECK. +LayoutNG folks, can you pease take a look?

[Monorail components: Blink>Layout]

### cl...@chromium.org (2021-09-02)

Detailed Report: https://clusterfuzz.com/testcase?key=4984937508569088

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Security DCHECK failure
Crash Address: 
Crash State:
  IsA<Derived>(from) in casting.h
  blink::LayoutInline* blink::To<blink::LayoutInline, blink::LayoutObject>
  blink::NGOutOfFlowLayoutPart::Run
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=825683:825689

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=4984937508569088

The reproduce tool requires a ClusterFuzz source checkout. To prepare one, run:

git clone https://github.com/google/clusterfuzz && cd clusterfuzz && git checkout tags/reproduce-tool-stable

To reproduce this issue, run:

./reproduce.sh -t https://clusterfuzz.com/testcase-detail/4984937508569088 -b /path/to/build

Please use the GN arguments provided in this report when building the binary. If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### cl...@chromium.org (2021-09-02)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Blink>Internals>WTF]

### ik...@chromium.org (2021-09-02)

cc/ kojii

This is:
https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/layout/layout_inline.cc;l=611;drc=7fc1bf7f07dacab1be87c6fde304750df5b7d4cd?q=splitinline&ss=chromium

Causing the fundamental issue.

We've currently got a project ("block-in-inline") inflight to remove inline-splitting for most cases (as its a constant source of issues / pain).

I did a quick test to relax that To<LayoutInline> to a DynamicTo<LayoutInline> however too many other CHECKs/DCHECKs trigger.

It looks like LayoutInline::SplitInlines has changed over the years. I think I'll just try to remove that 200 limit, and see if we get reports of hangs for the couple of releases which we won't have the new "block-in-inline" code.

@kojii - Thoughts?

Ian

### ik...@chromium.org (2021-09-02)

https://chromium-review.googlesource.com/c/chromium/src/+/3140144

### gi...@appspot.gserviceaccount.com (2021-09-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/bbd315efb49a4ae257509dd0f0d85c6b5906e0e4

commit bbd315efb49a4ae257509dd0f0d85c6b5906e0e4
Author: Ian Kilpatrick <ikilpatrick@chromium.org>
Date: Thu Sep 02 19:04:20 2021

[layout] Remove limit from LayoutInline::SplitInlines.

After 200 elements the code "gave up" causing the layout tree to be
"strange".

This caused a To<LayoutInline> to fail in the OOF code. Relaxing this
To<> to a DynamicTo<> caused additional CHECKs / DCHECKs all over the
place (not just in NG but in Legacy as well).

This patch removes the limit at which we "give up". This may cause
additional render hangs.

However we currently have a project "block-in-inline" which will (for
most cases) stop inline-splitting for occuring (except in legacy
fallback).

Bug: 1245786
Change-Id: I5f1c4d6a4b81a8345974de40c0c50a27a839b7b4
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3140144
Reviewed-by: Koji Ishii <kojii@chromium.org>
Commit-Queue: Ian Kilpatrick <ikilpatrick@chromium.org>
Cr-Commit-Position: refs/heads/main@{#917771}

[modify] https://crrev.com/bbd315efb49a4ae257509dd0f0d85c6b5906e0e4/third_party/blink/renderer/core/layout/layout_inline.cc
[add] https://crrev.com/bbd315efb49a4ae257509dd0f0d85c6b5906e0e4/third_party/blink/web_tests/external/wpt/css/css-inline/inline-crash.html


### at...@google.com (2021-09-02)

The code just "gave up"! Too funny.

### ik...@chromium.org (2021-09-02)

Now we'll see if we get any hang reports.

### [Deleted User] (2021-09-02)

Dear owner, thanks for fixing this bug. We’ve reopened it because security bugs need Security_Severity and FoundIn labels set, which will enable the bots to request merges to the correct branches ( as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact (security@chromium.org) to arrange to set these labels and then this bug can be marked closed again. Thank you! Severity guidelines: https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues FoundIn guidelines: https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security Thanks for your time! 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### do...@chromium.org (2021-09-02)

Hmm, I'm not 100% sure on the severity of this one. Owners, can you help shed some light? What is the implication of the layout tree being "strange" and the bad cast succeeding?

### ik...@chromium.org (2021-09-02)

Layout-tree being "strange" is "fine". As for the bad-cast unsure. We would typically be trying to cast a LayoutView (the root of the tree) to a LayoutInline.

Most of the calls on this confused type are on APIs on the base LayoutObject class, e.g.  CanContainOutOfFlowPositionedElement

We do lots of things with this afterwards:
https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/layout/ng/ng_out_of_flow_positioned_node.h;l=55;drc=7fc1bf7f07dacab1be87c6fde304750df5b7d4cd;bpv=1;bpt=1

But a lot of this might be "fine", e.g. calls to the base classes?

### ct...@chromium.org (2021-09-02)

Thanks! Conservatively assigning this Security_Severity-High as this could plausibly be used for memory corruption. If we can prove this isn't exploitable we can lower the severity.

### cl...@chromium.org (2021-09-03)

ClusterFuzz testcase 4984937508569088 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=917762:917771

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### [Deleted User] (2021-09-04)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-04)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-09-04)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-04)

Requesting merge to extended stable M92 because latest trunk commit (917771) appears to be after extended stable branch point (885287).

Requesting merge to stable M93 because latest trunk commit (917771) appears to be after stable branch point (902210).

Requesting merge to beta M94 because latest trunk commit (917771) appears to be after beta branch point (911515).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-09-04)

This bug requires manual review: M94's targeted beta branch promotion date has already passed, so this requires manual review
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/main/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on ToT?
4. Does this change need to be merged into other active release branches (M-1, M+1)?
5. Why are these changes required in this milestone after branch?
6. Is this a new feature?
7. If it is a new feature, is it behind a flag using finch?

Chrome OS Only:
8. Was the change reviewed and approved by the Eng Prod Representative? See Eng Prod ownership by component: http://go/cros-engprodcomponents

Please contact the milestone owner if you have questions.
Owners: govind@(Android), harrysouders@(iOS), matthewjoseph@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sr...@google.com (2021-09-07)

pls answer https://crbug.com/chromium/1245786#c23 for merge review.

### ik...@chromium.org (2021-09-08)


1. Does your merge fit within the Merge Decision Guidelines?

Yes. However is slightly risky as this may increase renderer hangs from removing the limit.

2. Links to the CLs you are requesting to merge.

https://chromium-review.googlesource.com/c/chromium/src/+/3140144

3. Has the change landed and been verified on ToT?

Yes

4. Does this change need to be merged into other active release branches (M-1, M+1)?

Up to security folks.

5. Why are these changes required in this milestone after branch?

Type confusion security issue.

6. Is this a new feature?

No

7. If it is a new feature, is it behind a flag using finch?

N/A

### sr...@google.com (2021-09-08)

amyressler@ to review the merge for M94 and approve if deemed appropriate.

### am...@chromium.org (2021-09-08)

merge approved to M94, please merge to branch 4606 at soonest. 

### am...@google.com (2021-09-08)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### gi...@appspot.gserviceaccount.com (2021-09-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/d760d2ae1d51c0b4fda87a0a3af4e7ed30d2ff4c

commit d760d2ae1d51c0b4fda87a0a3af4e7ed30d2ff4c
Author: Ian Kilpatrick <ikilpatrick@chromium.org>
Date: Wed Sep 08 23:02:44 2021

[layout] Remove limit from LayoutInline::SplitInlines.

After 200 elements the code "gave up" causing the layout tree to be
"strange".

This caused a To<LayoutInline> to fail in the OOF code. Relaxing this
To<> to a DynamicTo<> caused additional CHECKs / DCHECKs all over the
place (not just in NG but in Legacy as well).

This patch removes the limit at which we "give up". This may cause
additional render hangs.

However we currently have a project "block-in-inline" which will (for
most cases) stop inline-splitting for occuring (except in legacy
fallback).

(cherry picked from commit bbd315efb49a4ae257509dd0f0d85c6b5906e0e4)

Bug: 1245786
Change-Id: I5f1c4d6a4b81a8345974de40c0c50a27a839b7b4
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3140144
Reviewed-by: Koji Ishii <kojii@chromium.org>
Commit-Queue: Ian Kilpatrick <ikilpatrick@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#917771}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3149698
Cr-Commit-Position: refs/branch-heads/4606@{#876}
Cr-Branched-From: 35b0d5a9dc8362adfd44e2614f0d5b7402ef63d0-refs/heads/master@{#911515}

[modify] https://crrev.com/d760d2ae1d51c0b4fda87a0a3af4e7ed30d2ff4c/third_party/blink/renderer/core/layout/layout_inline.cc
[add] https://crrev.com/d760d2ae1d51c0b4fda87a0a3af4e7ed30d2ff4c/third_party/blink/web_tests/external/wpt/css/css-inline/inline-crash.html


### am...@chromium.org (2021-09-08)

Congratulations, Aki! The VRP Panel has decided to award you $5000 for this report. Nice work and thank you for this report! 

### am...@chromium.org (2021-09-09)

merge approved for M93; please merge to branch 4577 by EOD today, 9 September. 

### am...@google.com (2021-09-09)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-09-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/8623d711677dcda77a54e84955c96c71040573d6

commit 8623d711677dcda77a54e84955c96c71040573d6
Author: Ian Kilpatrick <ikilpatrick@chromium.org>
Date: Thu Sep 09 23:20:48 2021

[layout] Remove limit from LayoutInline::SplitInlines.

After 200 elements the code "gave up" causing the layout tree to be
"strange".

This caused a To<LayoutInline> to fail in the OOF code. Relaxing this
To<> to a DynamicTo<> caused additional CHECKs / DCHECKs all over the
place (not just in NG but in Legacy as well).

This patch removes the limit at which we "give up". This may cause
additional render hangs.

However we currently have a project "block-in-inline" which will (for
most cases) stop inline-splitting for occuring (except in legacy
fallback).

(cherry picked from commit bbd315efb49a4ae257509dd0f0d85c6b5906e0e4)

(cherry picked from commit d760d2ae1d51c0b4fda87a0a3af4e7ed30d2ff4c)

Bug: 1245786
Change-Id: I5f1c4d6a4b81a8345974de40c0c50a27a839b7b4
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3140144
Reviewed-by: Koji Ishii <kojii@chromium.org>
Commit-Queue: Ian Kilpatrick <ikilpatrick@chromium.org>
Cr-Original-Original-Commit-Position: refs/heads/main@{#917771}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3149698
Cr-Original-Commit-Position: refs/branch-heads/4606@{#876}
Cr-Original-Branched-From: 35b0d5a9dc8362adfd44e2614f0d5b7402ef63d0-refs/heads/master@{#911515}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3152301
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/4577@{#1224}
Cr-Branched-From: 761ddde228655e313424edec06497d0c56b0f3c4-refs/heads/master@{#902210}

[modify] https://crrev.com/8623d711677dcda77a54e84955c96c71040573d6/third_party/blink/renderer/core/layout/layout_inline.cc
[add] https://crrev.com/8623d711677dcda77a54e84955c96c71040573d6/third_party/blink/web_tests/external/wpt/css/css-inline/inline-crash.html


### am...@chromium.org (2021-09-13)

[Empty comment from Monorail migration]

### am...@google.com (2021-09-13)

[Empty comment from Monorail migration]

### vo...@google.com (2021-09-14)

[Empty comment from Monorail migration]

### vo...@google.com (2021-09-14)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-14)

[Empty comment from Monorail migration]

### vo...@google.com (2021-09-15)

[Empty comment from Monorail migration]

### gi...@google.com (2021-09-16)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-09-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/eaed84eec02939de6b18a7dedd224bee31ddde48

commit eaed84eec02939de6b18a7dedd224bee31ddde48
Author: Zakhar Voit <voit@google.com>
Date: Thu Sep 16 11:29:42 2021

[M90-LTS] [layout] Remove limit from LayoutInline::SplitInlines.

After 200 elements the code "gave up" causing the layout tree to be
"strange".

This caused a To<LayoutInline> to fail in the OOF code. Relaxing this
To<> to a DynamicTo<> caused additional CHECKs / DCHECKs all over the
place (not just in NG but in Legacy as well).

This patch removes the limit at which we "give up". This may cause
additional render hangs.

However we currently have a project "block-in-inline" which will (for
most cases) stop inline-splitting for occuring (except in legacy
fallback).

(cherry picked from commit bbd315efb49a4ae257509dd0f0d85c6b5906e0e4)

Bug: 1245786
Change-Id: I5f1c4d6a4b81a8345974de40c0c50a27a839b7b4
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3140144
Commit-Queue: Ian Kilpatrick <ikilpatrick@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#917771}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3160014
Reviewed-by: Jana Grill <janagrill@google.com>
Owners-Override: Jana Grill <janagrill@google.com>
Commit-Queue: Zakhar Voit <voit@google.com>
Cr-Commit-Position: refs/branch-heads/4430@{#1606}
Cr-Branched-From: e5ce7dc4f7518237b3d9bb93cccca35d25216cbe-refs/heads/master@{#857950}

[modify] https://crrev.com/eaed84eec02939de6b18a7dedd224bee31ddde48/third_party/blink/renderer/core/layout/layout_inline.cc
[add] https://crrev.com/eaed84eec02939de6b18a7dedd224bee31ddde48/third_party/blink/web_tests/external/wpt/css/css-inline/inline-crash.html


### vo...@google.com (2021-09-16)

[Empty comment from Monorail migration]

### am...@google.com (2021-10-08)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-11)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1245786?no_tracker_redirect=1

[Multiple monorail components: Blink>Internals>WTF, Blink>Layout]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057126)*
