# Security DCHECK failed: !NeedsLayout() || ChildLayoutBlockedByDisplayLock()

| Field | Value |
|-------|-------|
| **Issue ID** | [40060446](https://issues.chromium.org/issues/40060446) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Layout>MultiCol |
| **Platforms** | Windows |
| **Reporter** | m....@gmail.com |
| **Assignee** | ms...@chromium.org |
| **Created** | 2022-07-30 |
| **Bounty** | $7,000.00 |

## Description

**Steps to reproduce the problem:**  

#TestOn  

asan-win32-release\_x64-1028254

#Reproduce

1. chrome --no-sandbox --user-data-dir=test poc.html

NOTE!  

The problem was found by my fuzzer running on CF(CC Security team for access permission <https://clusterfuzz.com/testcase-detail/6253560717312000>),  

CF incorrectly thought that the issue could not be stably reproduced, so the report would not be automatically generated, so I manually made a MINIPOC and submitted the report.

**Problem Description:**  

#Type of crash  

render tab

#asan  

[20112:24256:0730/111631.665:FATAL:ng\_offset\_mapping.cc(275)] Security DCHECK failed: unit.TextContentEnd() <= text.length(). 2<=1  

Backtrace:  

base::debug::CollectStackTrace [0x00007FFA29BC1C82+18] (C:\b\s\w\ir\cache\builder\src\base\debug\stack\_trace\_win.cc:329)  

base::debug::StackTrace::StackTrace [0x00007FFA2C48323A+26] (C:\b\s\w\ir\cache\builder\src\base\debug\stack\_trace.cc:218)  

logging::LogMessage::~LogMessage [0x00007FFA29A32F68+664] (C:\b\s\w\ir\cache\builder\src\base\logging.cc:671)  

blink::NGOffsetMapping::NGOffsetMapping [0x00007FFA32B1849F+703] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\ng\inline\ng\_offset\_mapping.cc:275)  

blink::NGOffsetMappingBuilder::Build [0x00007FFA36BB529E+1374] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\ng\inline\ng\_offset\_mapping\_builder.cc:244)  

blink::NGInlineNode::ComputeOffsetMapping [0x00007FFA33187EB5+1541] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\ng\inline\ng\_inline\_node.cc:1068)  

blink::NGInlineNode::ComputeOffsetMappingIfNeeded [0x00007FFA331877B0+944] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\ng\inline\ng\_inline\_node.cc:1024)  

blink::NGInlineNode::GetOffsetMapping [0x00007FFA33189207+951] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\ng\inline\ng\_inline\_node.cc:1088)  

blink::`anonymous namespace'::ElementInnerTextCollector::ProcessLayoutText [0x00007FFA2F0ED5FD+429] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\editing\element_inner_text.cc:243) blink::`anonymous namespace'::ElementInnerTextCollector::ProcessChildren [0x00007FFA2F0EB845+3061] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\editing\element\_inner\_text.cc:220)  

blink::`anonymous namespace'::ElementInnerTextCollector::ProcessChildren [0x00007FFA2F0EB2B7+1639] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\editing\element_inner_text.cc:220) blink::`anonymous namespace'::ElementInnerTextCollector::ProcessChildrenWithRequiredLineBreaks [0x00007FFA2F0ED1C2+114] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\editing\element\_inner\_text.cc:230)  

blink::`anonymous namespace'::ElementInnerTextCollector::ProcessChildren [0x00007FFA2F0EBC36+4070] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\editing\element_inner_text.cc:220) blink::Element::GetInnerTextWithoutUpdate [0x00007FFA2F0E948A+906] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\editing\element_inner_text.cc:471) blink::Element::innerText [0x00007FFA2F0E90E4+84] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\editing\element_inner_text.cc:457) blink::FrameContentAsText [0x00007FFA36E4D8C8+536] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\frame\frame_content_as_text.cc:32) blink::WebFrameContentDumper::DumpFrameTreeAsText [0x00007FFA336BA5EA+762] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\exported\web_frame_content_dumper.cc:19) ChromeRenderFrameObserver::CapturePageText [0x00007FFA2F34BEA4+720] (C:\b\s\w\ir\cache\builder\src\chrome\renderer\chrome_render_frame_observer.cc:591) content::RenderFrameImpl::DidMeaningfulLayout [0x00007FFA2C2D3B1C+542] (C:\b\s\w\ir\cache\builder\src\content\renderer\render_frame_impl.cc:2207) blink::`anonymous namespace'::ForEachLocalFrameControlledByWidget [0x00007FFA2EA737A1+305] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\frame\web\_frame\_widget\_impl.cc:171)  

blink::WebFrameWidgetImpl::UpdateLifecycle [0x00007FFA2EA74211+1617] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\frame\web\_frame\_widget\_impl.cc:1406)  

blink::WidgetBase::UpdateVisualState [0x00007FFA31ED19DA+314] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\platform\widget\widget\_base.cc:886)  

cc::LayerTreeHost::RequestMainFrameUpdate [0x00007FFA2C4BF447+279] (C:\b\s\w\ir\cache\builder\src\cc\trees\layer\_tree\_host.cc:376)  

cc::ProxyMain::BeginMainFrame [0x00007FFA2F6427DD+3949] (C:\b\s\w\ir\cache\builder\src\cc\trees\proxy\_main.cc:277)  

base::internal::Invoker<base::internal::BindState<void (cc::ProxyMain::\*)(std::Cr::unique\_ptr<cc::BeginMainFrameAndCommitState,std::Cr::default\_delete[cc::BeginMainFrameAndCommitState](javascript:void(0);) >),base::WeakPtr[cc::ProxyMain](javascript:void(0);),std::Cr::unique\_ptr<cc::BeginMainFrame [0x00007FFA33A12A06+454] (C:\b\s\w\ir\cache\builder\src\base\bind\_internal.h:791)  

base::TaskAnnotator::RunTaskImpl [0x00007FFA29B2652B+923] (C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:135)  

base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl [0x00007FFA2C86E39A+2666] (C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:428)

**Additional Comments:**

\*\*Chrome version: \*\* asan-win32-release\_x64-1028254 \*\*Channel: \*\* Not sure

**OS:** Windows

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 7.0 KB)
- [h1.js](attachments/h1.js) (text/plain, 452 B)
- [poc.html](attachments/poc.html) (text/plain, 8.2 KB)
- [tc.html](attachments/tc.html) (text/plain, 264 B)

## Timeline

### [Deleted User] (2022-07-30)

[Empty comment from Monorail migration]

### bh...@google.com (2022-08-01)

Able to replicate in M105. Setting to Medium severity.

CCing owners for Blink. Please let us know if someone else should be the right owner.

[Monorail components: Blink]

### [Deleted User] (2022-08-01)

[Empty comment from Monorail migration]

### cb...@chromium.org (2022-08-02)

[Empty comment from Monorail migration]

### ko...@chromium.org (2022-08-02)

[Empty comment from Monorail migration]

[Monorail components: -Blink Blink>Editing>Serialization]

### [Deleted User] (2022-08-02)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-08-02)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-08-02)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### me...@chromium.org (2022-08-02)

yosin, could you PTAL? Thanks.

### yo...@chromium.org (2022-08-03)

<input> isn't laid out in LocalFrameView::UpdateStyleAndLayout().

# Stack trace from content_shell -run-web-tests
    LayoutObject::AssertLaidOut()
    LayoutObject::AssertSubtreeIsLaidOut()
    LocalFrameView::UpdateStyleAndLayout()
    Document::UpdateStyleAndLayout()
    Document::ImplicitClose()
    Document::CheckCompletedInternal()
    Document::CheckCompleted()
    FrameLoader::FinishedParsing()
    Document::FinishedParsing()
    HTMLConstructionSite::FinishedParsing()
    HTMLTreeBuilder::Finished()
    HTMLDocumentParser::end()
    HTMLDocumentParser::AttemptToRunDeferredScriptsAndEnd()
    HTMLDocumentParser::PrepareToStopParsing()
    HTMLDocumentParser::EndIfDelayed()
    HTMLDocumentParser::DeferredPumpTokenizerIfPossible()


# HTML
<media id="id124" cs="cs30" style="writing-mode: vertical-lr; column-count: 10;">
<x-menu id="id123" cs="cs7"><object test-description="<object> in <video>"></object></x-menu>
<input vspace="4"></media>

# Layout Tree
LayoutView 000041B200C21F60             #document
  LayoutNGBlockFlow 000041B200C22180    HTML
    LayoutNGBlockFlow 000041B200C22330  BODY
      LayoutNGBlockFlow 000041B200C22720        MEDIA id="id124" style="writing-mode: vertical-lr; column-count: 10; container-type: size;"
        LayoutMultiColumnFlowThread (anonymous) 000041B200C22BB8
          LayoutNGBlockFlow (anonymous) 000041B200C22D60
            LayoutInline 000041B200C22850       X-MENU id="id123"
              LayoutEmbeddedObject 000041B200C228E8     OBJECT
            LayoutText 000041B200C22A70 #text "\n\n\n"
*           LayoutNGTextControlSingleLine 000041B200C23008      INPUT
              LayoutNGTextControlInnerEditor 000041B200C23138   DIV (editable)
        LayoutMultiColumnSet (anonymous) 000041B200C22E90


[Monorail components: -Blink>Editing>Serialization Blink>Layout>MultiCol]

### ms...@chromium.org (2022-08-03)

[Empty comment from Monorail migration]

### ms...@chromium.org (2022-08-03)

[Empty comment from Monorail migration]

### ms...@chromium.org (2022-08-04)

<!DOCTYPE html>
<div id="container" style="width:fit-content; container-type:size;">
  <span></span>
  <span id="boo" style="display:none;"></span>
</div>
<script>
  document.body.offsetTop;
  container.style.columnCount = "2";
  boo.style.display = "inline";
</script>

What's happening here is that since #container is a container for container queries (due to container-type:size), we'll delay layout tree updates of its children until we get to NGBlockNode::Layout() for #container.

When we make the following style changes:
  container.style.columnCount = "2";
  boo.style.display = "inline";

#container becomes a multicol container during regular style recalc, while #boo isn't inserted yet, since that's a child of the container query container. When we get to NGBlockNode::Layout() for #container after the style changes, we have this layout tree:

*     LayoutNGBlockFlow 0x202300c26928 	DIV id="container" style="width: fit-content; container-type: size; column-count: 2;"
        LayoutMultiColumnFlowThread (anonymous) 0x202300c26c10
          LayoutNGBlockFlow (anonymous) 0x202300c26db0
            LayoutInline 0x202300c26ac8	SPAN
            LayoutText 0x202300c26b58  	#text "\n  "
        LayoutMultiColumnSet (anonymous) 0x202300c26ed8

(i.e. no #boo yet)

We have inserted an anonymous block (0x202300c26db0) to hold direct inline children of the multicol container [1] (and a LayoutMultiColumnFlowThread and a LayoutMultiColumnSet, but LayoutNG ignores those).

With the above layout tree we calculate min/max sizes (because of width:fit-content). This happens via CalculateInitialFragmentGeometry(). THEN we insert #boo, via UpdateStyleAndLayoutTreeForContainer(), and we end up with the final layout tree:

*     LayoutNGBlockFlow 0x202300c26928 	DIV id="container" style="width: fit-content; container-type: size; column-count: 2;"
        LayoutMultiColumnFlowThread (anonymous) 0x202300c26c10
          LayoutNGBlockFlow (anonymous) 0x202300c26db0
            LayoutInline 0x202300c26ac8	SPAN
            LayoutText 0x202300c26b58  	#text "\n  "
            LayoutInline 0x202300c27048	SPAN id="boo" style="display: inline;"
            LayoutText 0x202300c270d8  	#text "\n"
        LayoutMultiColumnSet (anonymous) 0x202300c26ed8

However, when we invoke NGInlineNode::PrepareLayoutIfNeeded() (on 0x202300c26db0) during actual layout, we'll return early, because IsPrepareLayoutFinished() returns true, even though we have modified the layout tree. This is bad, and the reason is the owner->EverHadLayout() condition in https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/layout/layout_object_child_list.cc;l=224-227;drc=5e38e1aa0f83e2f03493f0399210821be4731440

|owner| is the anonymous block 0x202300c26db0, which was just inserted, so it has never had layout. We therefore fail to call owner->SetChildNeedsCollectInlines() from LayoutObjectChildList::InsertChildNode(), and we therefore end up with stale LayoutNGBlockFlowMixin::ng_inline_node_data_ when performing layout, so that we miss layout of #boo.

[1] This is multicol-specific behavior, introduced here: https://chromium-review.googlesource.com/c/chromium/src/+/2823033

### ms...@chromium.org (2022-08-04)

Fixing the DHECK failure for this particular multicol-specific test case is easy, though, because what's causing trouble is that we examine children during min/max calculation for a size-contained object, which is something we shouldn't be doing. Fix here: https://chromium-review.googlesource.com/c/chromium/src/+/3807462

However, I'm still concerned about this. I'm not convinced that we can always be sure that we update LayoutNGBlockFlowMixin::ng_inline_node_data_ when we should.

### gi...@appspot.gserviceaccount.com (2022-08-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/69875852d8cb7445cc4b2c07ba5b9366d40ff4c1

commit 69875852d8cb7445cc4b2c07ba5b9366d40ff4c1
Author: Morten Stenshorne <mstensho@chromium.org>
Date: Thu Aug 04 12:23:02 2022

Correct multicol min/max with inline-size containment.

Without this fix, we used to make room for column spanners, which is
wrong if inline-size containment should apply.

Make an existing test more evil, so that it would fail without this fix.

This also fixes a crash, which is what crbug.com/1348714 really was
about. We used to lay out with stale NGInlineNodeData. NGInlineNodeData
used to get updated during min/max calculation (because we didn't honor
size containment), and that takes place (via
CalculateInitialFragmentGeometry() in NGBlockNode::Layout()) before
container query evaluation (which will update the layout object tree
structure). Apparently we don't update NGInlineNodeData again once we
get to actual layout. It could be that there's an underlying cause that
still needs to be addressed here. If someone is unlucky enough to do an
NGInlineNode::PrepareLayoutIfNeeded() before container query evaluation,
it seems that we might end up with stale NGInlineNodeData.

Bug: 1348714
Change-Id: I1996f95138050778ea05d7b20b5301b57c94695a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3807462
Reviewed-by: Koji Ishii <kojii@chromium.org>
Commit-Queue: Morten Stenshorne <mstensho@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1031461}

[modify] https://crrev.com/69875852d8cb7445cc4b2c07ba5b9366d40ff4c1/third_party/blink/web_tests/external/wpt/css/css-contain/contain-inline-size-multicol.html
[modify] https://crrev.com/69875852d8cb7445cc4b2c07ba5b9366d40ff4c1/third_party/blink/renderer/core/layout/ng/ng_column_layout_algorithm.cc
[add] https://crrev.com/69875852d8cb7445cc4b2c07ba5b9366d40ff4c1/third_party/blink/web_tests/external/wpt/css/css-multicol/crashtests/size-containment-become-multicol-add-inline-child.html


### ms...@chromium.org (2022-08-04)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-04)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-04)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-04)

Requesting merge to dev M105 because latest trunk commit (1031461) appears to be after dev branch point (1027018).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-08-05)

Merge review required: M105 is already shipping to beta.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), harrysouders (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ms...@chromium.org (2022-08-05)

1. any security issues
2. https://chromium-review.googlesource.com/c/chromium/src/+/3807462
3. Yes
4. No
5. N/A
6. N/A

### pb...@google.com (2022-08-08)

Merge approved for M105 Branch:Refer to go/chrome-branches for branch info, Please goahead and get the changes cherrypick asap.


### gi...@appspot.gserviceaccount.com (2022-08-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/38b2cdab61d7b7f44535d7f1fd44ef67ee301b20

commit 38b2cdab61d7b7f44535d7f1fd44ef67ee301b20
Author: Morten Stenshorne <mstensho@chromium.org>
Date: Mon Aug 08 21:59:10 2022

Correct multicol min/max with inline-size containment.

Without this fix, we used to make room for column spanners, which is
wrong if inline-size containment should apply.

Make an existing test more evil, so that it would fail without this fix.

This also fixes a crash, which is what crbug.com/1348714 really was
about. We used to lay out with stale NGInlineNodeData. NGInlineNodeData
used to get updated during min/max calculation (because we didn't honor
size containment), and that takes place (via
CalculateInitialFragmentGeometry() in NGBlockNode::Layout()) before
container query evaluation (which will update the layout object tree
structure). Apparently we don't update NGInlineNodeData again once we
get to actual layout. It could be that there's an underlying cause that
still needs to be addressed here. If someone is unlucky enough to do an
NGInlineNode::PrepareLayoutIfNeeded() before container query evaluation,
it seems that we might end up with stale NGInlineNodeData.

(cherry picked from commit 69875852d8cb7445cc4b2c07ba5b9366d40ff4c1)

Bug: 1348714
Change-Id: I1996f95138050778ea05d7b20b5301b57c94695a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3807462
Reviewed-by: Koji Ishii <kojii@chromium.org>
Commit-Queue: Morten Stenshorne <mstensho@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1031461}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3817985
Auto-Submit: Morten Stenshorne <mstensho@chromium.org>
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/5195@{#345}
Cr-Branched-From: 7aa3f074a7907975b001346cc0288d0214af8451-refs/heads/main@{#1027018}

[modify] https://crrev.com/38b2cdab61d7b7f44535d7f1fd44ef67ee301b20/third_party/blink/web_tests/external/wpt/css/css-contain/contain-inline-size-multicol.html
[modify] https://crrev.com/38b2cdab61d7b7f44535d7f1fd44ef67ee301b20/third_party/blink/renderer/core/layout/ng/ng_column_layout_algorithm.cc
[add] https://crrev.com/38b2cdab61d7b7f44535d7f1fd44ef67ee301b20/third_party/blink/web_tests/external/wpt/css/css-multicol/crashtests/size-containment-become-multicol-add-inline-child.html


### am...@google.com (2022-08-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-08-17)

Congratulations on another one! The VRP Panel has decided to award you $7,000 for this report (based on updated VRP reward amounts). Thank you for your efforts in reporting this issue to us! Nice work! 

### am...@google.com (2022-08-19)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-10)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1348714?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060446)*
