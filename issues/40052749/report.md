# Heap-buffer-overflow in blink::NGFragmentItems::LayoutObjectWillBeMoved

| Field | Value |
|-------|-------|
| **Issue ID** | [40052749](https://issues.chromium.org/issues/40052749) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>Layout |
| **Platforms** | Linux, Windows |
| **Reporter** | cl...@chromium.org |
| **Assignee** | ko...@chromium.org |
| **Created** | 2020-07-02 |
| **Bounty** | $6,000.00 |

## Description

Detailed Report: https://clusterfuzz.com/testcase?key=6589180840312832

Fuzzer: puzzor
Job Type: linux_asan_chrome_v8_arm
Platform Id: linux

Crash Type: Heap-buffer-overflow READ 4
Crash Address: 0xf37736b0
Crash State:
  blink::NGFragmentItems::LayoutObjectWillBeMoved
  blink::InvalidateInlineItems
  blink::LayoutObjectChildList::RemoveChildNode
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_v8_arm&range=784296:784299

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6589180840312832

Issue filed automatically.

The reproduce tool requires a ClusterFuzz source checkout. To prepare one, run:

git clone https://github.com/google/clusterfuzz && cd clusterfuzz && git checkout tags/reproduce-tool-stable

To reproduce this issue, run:

./reproduce.sh -t https://clusterfuzz.com/testcase-detail/6589180840312832 -b /path/to/build

Please use the GN arguments provided in this report when building the binary. If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


## Attachments

- [tc.html](attachments/tc.html) (text/plain, 253 B)

## Timeline

### cl...@chromium.org (2020-07-02)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Blink>Layout]

### cl...@chromium.org (2020-07-02)

Automatically assigning owner based on suspected regression changelist https://chromium.googlesource.com/chromium/src/+/0ae74b0ca37141c9ced8fe4e48944f120d260d7b ([FragmentItem] Include floats in associated LayoutObject).

If this is incorrect, please let us know why and apply the Test-Predator-Wrong-CLs label. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### [Deleted User] (2020-07-02)

Setting milestone and target because of Security_Impact=Head and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-07-02)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-07-02)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ko...@chromium.org (2020-07-03)

Morten, can you help? The crash is within:
  if (UNLIKELY(layout_object.IsInsideFlowThread())) {
block. I though this code should not run without NGBlockFragmntation enabled, but it looks like it is running. Is this just adding "if" to check non-null, or is it something wrong to enter into this "if IsInsideFlowThread" block?

### ms...@chromium.org (2020-07-03)

Also only reproducible with LayoutNGFragmentItem. Does the fuzzer run with that one enabled these days? ReleaseBlock-Stable is probably wrong, though?

Investigating the problem now.

### ms...@chromium.org (2020-07-03)

DCHECK failure in NGFragmentItems::LayoutObjectWillBeMoved():

LayoutView 0x380808204010              	#document
  LayoutNGBlockFlow 0x380808218010     	HTML
    LayoutNGBlockFlow 0x3808082181b0   	BODY
      LayoutNGBlockFlow (positioned) 0x380808218350	DIV id="container" style="position: absolute; columns: auto 2;"
        LayoutMultiColumnFlowThread (anonymous) 0x380808228010
          LayoutNGBlockFlow (anonymous) 0x380808218690
*           LayoutNGBlockFlow (positioned) 0x380808218830	DIV id="child" style="float: right; position: absolute;"
          LayoutText 0x3808082102b0    	#text "\n  xxx\n  "
        LayoutMultiColumnSet (anonymous) 0x38080822c010

Looks like too many things (okay, maybe only two things, but that's enough) are happening almost at the same time here, but in the wrong order or something.

On one hand we're turning an object into a multicol container, which should make all descendants fall back to legacy layout. But at the same time we're cleaning up anonymous blocks (for reasons I don't quite understand yet). The layout tree is in a pretty bad state at this point.

### ms...@chromium.org (2020-07-03)

I've come to realize that the root cause of this bug is most likely https://crbug.com/chromium/1101986.

Admittedly, the tree is in a pretty strange state, given that we're supposed to fall back to legacy layout when entering multicol - i.e. we're about to reattach #container anyway (so we're wasting time populating a flow thread along with all the housekeeping that entails). But we need to deal with situations like these when LayoutNG block fragmentation is enabled anyway (then we're not going to reattach), so I really think we should just cope with a tree state like this.

I've created https://chromium-review.googlesource.com/c/chromium/src/+/2279820 , which fixes this bug, but underneath, https://crbug.com/chromium/1101986 is lurking, still causing DCHECK failures, but no heap-buffer-overflow, at least. I think it's better to fix https://crbug.com/chromium/1101986 instead.

### ko...@chromium.org (2020-07-04)

> Also only reproducible with LayoutNGFragmentItem. Does the fuzzer run with that one enabled these days?

Yes.

> ReleaseBlock-Stable is probably wrong, though?

Right.

### [Deleted User] (2020-07-04)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ko...@chromium.org (2020-07-05)

[Empty comment from Monorail migration]

### cl...@chromium.org (2020-07-05)

[Empty comment from Monorail migration]

### ms...@chromium.org (2020-07-06)

[Empty comment from Monorail migration]

### ko...@chromium.org (2020-07-06)

Morten, I confirmed this no longer crashes with the fix for https://crbug.com/chromium/1101986, but it still goes into this "if" block. Is this ok?

void NGFragmentItems::LayoutObjectWillBeDestroyed(
    const LayoutObject& layout_object) {
  if (UNLIKELY(layout_object.IsInsideFlowThread())) {


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-07-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/5ea1725538d36f8e768cf6cae7509fe6f7349395

commit 5ea1725538d36f8e768cf6cae7509fe6f7349395
Author: Koji Ishii <kojii@chromium.org>
Date: Mon Jul 06 17:53:24 2020

[FragmentItem] Clear inline fragment for positioned objects

This is a refix of r784685 <crrev.com/c/2275820>.

When floating objects become positioned, |NGFragmentItems|
can no longer track further changes or destructions. r784685
<crrev.com/c/1101277> fixed this in pre-layout, but it is
possible that changes can occur before next layout cycle.

This patch marks |NGFragmentItem| as moved and clears the
index in |LayoutBox::StyleWillChange| instead.

Logically speaking, this could happen to non-floating objects
such as inline-block. Our current code reattaches when non-
floating objects become positioned, so only floating objects
can cause this after r784297 <crrev.com/c/2275373>.

Bug: 1101818, 1101986, 1101277
Change-Id: I56e53aaf4e0b6b5b0ef78c3f75eaf3ffd3568596
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2279425
Reviewed-by: Morten Stenshorne <mstensho@chromium.org>
Reviewed-by: Ian Kilpatrick <ikilpatrick@chromium.org>
Commit-Queue: Koji Ishii <kojii@chromium.org>
Cr-Commit-Position: refs/heads/master@{#785453}

[modify] https://crrev.com/5ea1725538d36f8e768cf6cae7509fe6f7349395/third_party/blink/renderer/core/layout/layout_box.cc
[modify] https://crrev.com/5ea1725538d36f8e768cf6cae7509fe6f7349395/third_party/blink/renderer/core/layout/ng/inline/ng_inline_items_builder.cc
[add] https://crrev.com/5ea1725538d36f8e768cf6cae7509fe6f7349395/third_party/blink/web_tests/external/wpt/css/CSS2/positioning/detach-abspos-before-layout.html


### ms...@chromium.org (2020-07-06)

Yes, entering that code is possible and should be safe. 

### ko...@chromium.org (2020-07-06)

https://crbug.com/chromium/1101818#c17: Thank you for the info, then let's call this fixed.

### [Deleted User] (2020-07-06)

This release blocking issue appears to be targeted for M85, which has already branched. Because this issue was marked as fixed after branch point, a merge of any CLs which landed on or after June 25 may be required. Please review whether or not any CLs should be merged ASAP, and if a merge is necessary apply the label Merge-Request-85 to begin the merge review process. If no merge is required, please simply remove the Merge-TBD label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ko...@chromium.org (2020-07-06)

[Empty comment from Monorail migration]

### cl...@chromium.org (2020-07-06)

ClusterFuzz testcase 4695145024389120 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_msan_chrome&range=785449:785459

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### [Deleted User] (2020-07-07)

The older reward-topanel https://crbug.com/chromium/1101686 has been merged into this one. Please manually review this issue to see if the duplicate is potentially eligible for a reward.



### [Deleted User] (2020-07-07)

[Empty comment from Monorail migration]

### ko...@chromium.org (2020-07-10)

Requesting merge for https://crbug.com/chromium/1101277, and that not needed for this issue.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-07-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/31fd0a1a984f89aae83a47c3bc8b87299cef8afe

commit 31fd0a1a984f89aae83a47c3bc8b87299cef8afe
Author: Koji Ishii <kojii@chromium.org>
Date: Sat Jul 11 19:41:56 2020

Merge 4183: [FragmentItem] Clear inline fragment for positioned objects

This is a refix of r784685 <crrev.com/c/2275820>.

When floating objects become positioned, |NGFragmentItems|
can no longer track further changes or destructions. r784685
<crrev.com/c/1101277> fixed this in pre-layout, but it is
possible that changes can occur before next layout cycle.

This patch marks |NGFragmentItem| as moved and clears the
index in |LayoutBox::StyleWillChange| instead.

Logically speaking, this could happen to non-floating objects
such as inline-block. Our current code reattaches when non-
floating objects become positioned, so only floating objects
can cause this after r784297 <crrev.com/c/2275373>.

(cherry picked from commit 5ea1725538d36f8e768cf6cae7509fe6f7349395)

Bug: 1101818, 1101986, 1101277
Change-Id: I56e53aaf4e0b6b5b0ef78c3f75eaf3ffd3568596
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2279425
Reviewed-by: Morten Stenshorne <mstensho@chromium.org>
Reviewed-by: Ian Kilpatrick <ikilpatrick@chromium.org>
Commit-Queue: Koji Ishii <kojii@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#785453}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2291522
Reviewed-by: Koji Ishii <kojii@chromium.org>
Cr-Commit-Position: refs/branch-heads/4183@{#400}
Cr-Branched-From: 740e9e8a40505392ba5c8e022a8024b3d018ca65-refs/heads/master@{#782793}

[modify] https://crrev.com/31fd0a1a984f89aae83a47c3bc8b87299cef8afe/third_party/blink/renderer/core/layout/layout_box.cc
[add] https://crrev.com/31fd0a1a984f89aae83a47c3bc8b87299cef8afe/third_party/blink/web_tests/external/wpt/css/CSS2/positioning/detach-abspos-before-layout.html


### ad...@google.com (2020-07-29)

The VRP panel decided to upgrade this to High because one fuzzer case in a linked bug was a UaF.

### ad...@google.com (2020-07-29)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-07-30)

Congratulations! The VRP panel has decided to award $5000 for this report, plus the $1000 fuzzer bonus.

### ad...@google.com (2020-08-27)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-14)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1101818?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1101686, crbug.com/chromium/1102102]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40052749)*
