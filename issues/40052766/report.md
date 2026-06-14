# Security DCHECK failure: unit.TextContentEnd() <= text.length() in ng_offset_mapping.cc

| Field | Value |
|-------|-------|
| **Issue ID** | [40052766](https://issues.chromium.org/issues/40052766) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>Layout |
| **Platforms** | Linux |
| **Reporter** | cl...@chromium.org |
| **Assignee** | ko...@chromium.org |
| **Created** | 2020-07-04 |
| **Bounty** | $6,000.00 |

## Description

Detailed Report: https://clusterfuzz.com/testcase?key=5686589092593664

Fuzzer: attekett_dom_fuzzer
Job Type: linux_asan_chrome_v8_arm
Platform Id: linux

Crash Type: Security DCHECK failure
Crash Address: 
Crash State:
  unit.TextContentEnd() <= text.length() in ng_offset_mapping.cc
  blink::NGInlineNode::ComputeOffsetMapping
  blink::NGInlineNode::ComputeOffsetMappingIfNeeded
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_v8_arm&range=785094:785095

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5686589092593664

Issue filed automatically.

The reproduce tool requires a ClusterFuzz source checkout. To prepare one, run:

git clone https://github.com/google/clusterfuzz && cd clusterfuzz && git checkout tags/reproduce-tool-stable

To reproduce this issue, run:

./reproduce.sh -t https://clusterfuzz.com/testcase-detail/5686589092593664 -b /path/to/build

Please use the GN arguments provided in this report when building the binary. If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


## Timeline

### cl...@chromium.org (2020-07-04)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Blink>Layout]

### cl...@chromium.org (2020-07-04)

Automatically assigning owner based on suspected regression changelist https://chromium.googlesource.com/chromium/src/+/1990adcaddb542be27a80d04555cac343711d869 (ExternalVkImageBacking: only do synchronization when GL texture is created).

If this is incorrect, please let us know why and apply the Test-Predator-Wrong-CLs label. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### pe...@chromium.org (2020-07-04)

It is so weird. The CL is for gpu process, and it is behind flag --enable-features=Vulkan. I don't see how the blink crash is related.

Hi yosin@, could you please take a look?

### [Deleted User] (2020-07-04)

Setting milestone and target because of Security_Impact=Head and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-07-04)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-07-04)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### yo...@chromium.org (2020-07-06)

Hit  LayoutObjectAssertSubtreeIsLaidOut() for LayoutView from "usecss" command
Note: requires --enable-blink-features=LayoutNGFragmentItem


Stack trace:
LayoutObject::AssertLaidOut()
LayoutObject::AssertSubtreeIsLaidOut()
LocalFrameView::UpdateLayout()
Document::UpdateStyleAndLayout()
EditorCommand::Execute()
Document::execCommand()
document_v8_internal::ExecCommandMethod()
V8Document::ExecCommandMethodCallback()


### yo...@chromium.org (2020-07-06)

It seems |normal\_child\_needs\_layout\_| isn't propagated from <a> to <body> and ancestors.

Minimized test script to reproduce:

<!doctype html>  

<a><object id="target">\*\*\*\* </object><br></a>

<script>
const target = document.getElementById('target');
target.style.setProperty('transition-delay', '9999s');
document.body.offsetWidth;
target.style.transform = 'scale(1)';
document.body.offsetHeight;
</script>

### yo...@chromium.org (2020-07-06)

Layout Tree:

LayoutView 000065441F204010             #document
  LayoutNGBlockFlow 000065441F218010    HTML
    LayoutNGBlockFlow 000065441F2181B0  BODY
*     LayoutInline 000065441F228010     A
        LayoutInline 000065441F2280D0   OBJECT id="target" style="transition-delay: 9999s; transform: scale(1);"
          LayoutInline 000065441F228190 B
        LayoutBR 000065441F2102B0       BR
      LayoutText 000065441F240010       #text "\n"

[32964:5304:0706/135715.380:FATAL:layout_object.h(441)] Security DCHECK failed: !NeedsLayout() || LayoutBlockedByDisplay for <a>

### yo...@chromium.org (2020-07-06)

kojji@, could you take look? This is yet another condition to set dirty for |NGFragmentItems::DirtyLinesFromNeedsLayout()|.
When <object> is marked SetChildNeedsLayout() but <b> (child of <object>) isn't marked SelfNeedsLayout.

Even if your CL http://crrev.com/c/2281781, this issue isn't fixed.
It seems for LayoutInline, we should call DirtyLinesFromNeedsForChild() for LayoutInline if we don't call DirtyLinesFromNeedsForChild() for descendants.
We may need to use recursive call for LayoutInline?



### ko...@chromium.org (2020-07-06)

Thank you for minimized test, it is helpful.

The code does DFS traversal, so recursive call is already done, but this looks like complicated. Now I'm thinking to make it simpler by giving up some cases to reuse lines...

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-07-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/3818ee97578a630573bc5af8dce0e303bc26c1dd

commit 3818ee97578a630573bc5af8dce0e303bc26c1dd
Author: Koji Ishii <kojii@chromium.org>
Date: Mon Jul 06 13:18:29 2020

[FragmentItem] Limit reusing cached lines only when top-level child is clean

This patch simplifies |DirtyLinesFromNeedsLayout| to check
|NeedsLayout| of top-level children only.

The previous code tried to reuse more lines, e.g.:
  <div><span>many lines of text</span></div>
Most lines are reusable when appending to the end of "text".
But supporting this case complicates the logic, especially
when culled inline is involved.

The new logic can't reuse lines in the above case, but still
can reuse liens if the `<span>` does not exist, and should
cover most common cases.

Bug: 1102083
Change-Id: I4f76e154b834c8c00e5ce04ab251c4f1fcdabab0
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2282821
Reviewed-by: Yoshifumi Inoue <yosin@chromium.org>
Commit-Queue: Yoshifumi Inoue <yosin@chromium.org>
Commit-Queue: Koji Ishii <kojii@chromium.org>
Cr-Commit-Position: refs/heads/master@{#785345}

[modify] https://crrev.com/3818ee97578a630573bc5af8dce0e303bc26c1dd/third_party/blink/renderer/core/layout/ng/inline/ng_fragment_items.cc
[add] https://crrev.com/3818ee97578a630573bc5af8dce0e303bc26c1dd/third_party/blink/web_tests/external/wpt/css/CSS2/linebox/needs-layout-transform.html


### cl...@chromium.org (2020-07-06)

ClusterFuzz testcase 5686589092593664 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_v8_arm&range=785344:785345

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### [Deleted User] (2020-07-06)

This release blocking issue appears to be targeted for M85, which has already branched. Because this issue was marked as fixed after branch point, a merge of any CLs which landed on or after June 25 may be required. Please review whether or not any CLs should be merged ASAP, and if a merge is necessary apply the label Merge-Request-85 to begin the merge review process. If no merge is required, please simply remove the Merge-TBD label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-07-07)

[Empty comment from Monorail migration]

### ko...@chromium.org (2020-07-10)

Requesting merge. This merge requires manual merge as it supersedes https://crbug.com/chromium/1101883, but it is safer than the fix for https://crbug.com/chromium/1101883.

### [Deleted User] (2020-07-11)

Your change meets the bar and is auto-approved for M85. Please go ahead and merge the CL to branch 4183 (refs/branch-heads/4183) manually. Please contact milestone owner if you have questions.
Merge instructions: https://www.chromium.org/developers/how-tos/drover
Owners: benmason@(Android), bindusuvarna@(iOS), dgagnon@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-07-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/c1cced896b7143bfd45466df3f9a4b5557e157c3

commit c1cced896b7143bfd45466df3f9a4b5557e157c3
Author: Koji Ishii <kojii@chromium.org>
Date: Sat Jul 11 18:38:47 2020

Merge 4183: [FragmentItem] Limit reusing cached lines only when top-level child is clean

This patch simplifies |DirtyLinesFromNeedsLayout| to check
|NeedsLayout| of top-level children only.

The previous code tried to reuse more lines, e.g.:
  <div><span>many lines of text</span></div>
Most lines are reusable when appending to the end of "text".
But supporting this case complicates the logic, especially
when culled inline is involved.

The new logic can't reuse lines in the above case, but still
can reuse liens if the `<span>` does not exist, and should
cover most common cases.

(cherry picked from commit 3818ee97578a630573bc5af8dce0e303bc26c1dd)

Bug: 1102083
Change-Id: I4f76e154b834c8c00e5ce04ab251c4f1fcdabab0
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2282821
Reviewed-by: Yoshifumi Inoue <yosin@chromium.org>
Commit-Queue: Yoshifumi Inoue <yosin@chromium.org>
Commit-Queue: Koji Ishii <kojii@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#785345}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2290489
Reviewed-by: Koji Ishii <kojii@chromium.org>
Cr-Commit-Position: refs/branch-heads/4183@{#397}
Cr-Branched-From: 740e9e8a40505392ba5c8e022a8024b3d018ca65-refs/heads/master@{#782793}

[modify] https://crrev.com/c1cced896b7143bfd45466df3f9a4b5557e157c3/third_party/blink/renderer/core/layout/ng/inline/ng_fragment_items.cc
[add] https://crrev.com/c1cced896b7143bfd45466df3f9a4b5557e157c3/third_party/blink/web_tests/external/wpt/css/CSS2/linebox/needs-layout-transform.html


### na...@google.com (2020-07-16)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-07-16)

Congrats! The Panel decided to award $5,000 for this report plus an additional $1,000 fuzzing bonus!

### na...@google.com (2020-07-16)

[Empty comment from Monorail migration]

### wa...@chromium.org (2020-09-09)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-14)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1102083?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/762966]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40052766)*
