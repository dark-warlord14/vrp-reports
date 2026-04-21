# Security: use-after-poison in blink::InlineLayoutAlgorithm::CreateLine

| Field | Value |
|-------|-------|
| **Issue ID** | [40945761](https://issues.chromium.org/issues/40945761) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>CSS, Blink>Layout |
| **Platforms** | Linux |
| **Reporter** | wh...@gmail.com |
| **Assignee** | sa...@chromium.org |
| **Created** | 2023-11-25 |
| **Bounty** | Confirmed (amount unknown) |

## Description

deleted

## Attachments

- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- [1.png](attachments/1.png) (image/png, 70.6 KB)

## Timeline

### [Deleted User] (2023-11-25)

[Empty comment from Monorail migration]

### dc...@chromium.org (2023-11-25)

Sorry, without a test case, this is inactionable. Please provide a test case :)

### wh...@gmail.com (2023-11-26)

deleted

### wh...@gmail.com (2023-11-26)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-26)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cl...@chromium.org (2023-11-26)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4751138184691712.

### dc...@chromium.org (2023-11-26)

I'll run it through Clusterfuzz, but if you can just attach a file next time, that would be easier and guarantee that there's no accidental diffs introduced by copying and pasting something.

### cl...@chromium.org (2023-11-27)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-11-27)

Detailed Report: https://clusterfuzz.com/testcase?key=4751138184691712

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Use-after-poison READ 4
Crash Address: 0x7ee50015d2fc
Crash State:
  blink::InlineLayoutAlgorithm::CreateLine
  blink::InlineLayoutAlgorithm::Layout
  blink::InlineNode::Layout
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1197657:1197659

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=4751138184691712

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


A recommended severity was added to this bug. Please change the severity if it is inaccurate.

### wh...@gmail.com (2023-11-27)

bisect 
[text-wrap-pretty] Use `NGLineInfoList`

This patch adds either `NGLineInfo` or `NGLineInfoList` to
`NGInlineChildLayoutContext`, depending on the line breaker
type of the inline formatting context.

Currently, `NGLineInfoList` is used only when `text-wrap:
pretty`, which is a runtime flag not enabled yet.

`NGLineInfo` is a rather large object, ~4k, and
`NGLineInfoList` has 4 instances. As the inline layout may be
nested when it has inline blocks for instance, adding
`NGLineInfoList` only when necessary is important to avoid
stack overflow.

Before this patch, `NGInlineLayoutAlgorithm` allocated one
`NGLineInfo` on the stack, so the stack amount shouldn't
change unless `text-wrap: pretty` is enabled.

This patch should have no behavior changes.

Bug: 1432798
Change-Id: Ib2f4fc2afdf853674ff869171b28f9e35cc7802e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4354810
Reviewed-by: Kent Tamura <tkent@chromium.org>
Commit-Queue: Koji Ishii <kojii@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1141937}

active channel: 119/stable 120/beta 121/dev

### wh...@gmail.com (2023-11-27)

deleted

### [Deleted User] (2023-11-27)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### el...@chromium.org (2023-11-27)

Shepherd: We can consider the clusterfuzz reproduction in #9 to be a confirmation; thanks for the bisect in #10. It looks quite likely to me as well. Marking this as Pri-1 since it's a high-severity bug affecting stable, and sending to 

-> kojii@ cc tkent@ from https://chromium-review.googlesource.com/c/chromium/src/+/4354810

[Monorail components: Blink>Layout]

### ko...@chromium.org (2023-11-28)

CQ experts, can you help?

The inline layout has an assumption that the tree within an IFC doesn't change while laying it out.

CQ calls `UpdateStyleAndLayoutTreeForContainer`:
https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/layout/ng/ng_block_node.cc;l=404-405?q=BlockNode::Layout&ss=chromium%2Fchromium%2Fsrc

This reattaches `LayoutQuote`. Then `LayoutQuote::UpdateText()` sets the text. which dirties the IFC we're currently laying out.

Where did we go wrong?
1. Inline layout should assume that IFC can change while laying it out. When that happens, it should re-start from the beginning of the IFC? Is doing so compatbile with CQ?
2. CQ shouldn't reattach `LayoutQuote`.
3. `LayoutQuote` shouldn't dirty the IFC in this specific case.

### an...@chromium.org (2023-11-28)

I *think* this needs to be something along the lines of (3). A CQ (size) container has style containment applied, so any any quotes-related changes that happen within the container should not have any effect on the quotes situation outside the container.


### ko...@chromium.org (2023-11-28)

Thank you for the comment. I looked at the `container` argument of `UpdateStyleAndLayoutTreeForContainer`, and which `LayoutQuote` are dirtied.

1. We're laying out [1].
2. LineBreaker lays out the atomic inline[2].
3. `UpdateStyleAndLayoutTreeForContainer` with `container`=[2]
4. It then reattaches/UpdateText [3], which is outside of [2] but part of the IFC[1].

LayoutView 4C5C2168                    	#document
  LayoutNGBlockFlow 4C5C22B4           	HTML
    LayoutNGBlockFlow 4C5C2394         	BODY
      LayoutInline 4C5C25B8            	Q id="htmlvar00008" style="~bv%{BC+}ZH@F$c\\b}`3"
        LayoutInline 4C5C2604          	::before
          LayoutQuote (anonymous) 4C5C2650
            LayoutTextFragment (anonymous) 4C5C26B0 "?" 
        LayoutText 4C5C2728            	#text "Z69Kn]UZ2 *"
        LayoutInline 4C5C278C          	::after
          LayoutQuote (anonymous) 4C5C27D8
            LayoutTextFragment (anonymous) 4C5C2838 "?" 
      LayoutText 4C5C28B0              	#text "\n\n\n\n\n  "
      [1]LayoutNGBlockFlow 4C5C2474       	INS id="htmlvar00018" class="class5"
        [2]LayoutNGBlockFlow 4C5C2C0C     	Q id="htmlvar00019" class="class7" style="scroll-margin-top: 9px; link-parameters: none; -webkit-writing-mode: vertical-lr; stroke-break: clone; column-rule-width: medium"
          LayoutInline 4C5C2ED8        	::before
            LayoutQuote (anonymous) 4C5C2F24
              LayoutTextFragment (anonymous) 4C5C2F84 "?" 
          LayoutText 4C5C2E74          	#text ">Tc"
          LayoutInline 4C5C2D50        	::after
            LayoutQuote (anonymous) 4C5C2D9C
              LayoutTextFragment (anonymous) 4C5C2DFC "" 
        LayoutText 4C5C2CEC            	#text "\n\n    "
        LayoutInline 4C5C2914          	Q id="htmlvar00020" class="class7"
          LayoutInline 4C5C2960        	::before
            LayoutQuote (anonymous) 4C5C29AC
              LayoutTextFragment (anonymous) 4C5C2A0C "?" 
          LayoutText 4C5C2A84          	#text "\n  "
          LayoutInline 4C5C2AE8        	::after
            [3]LayoutQuote (anonymous) 4C5C2B34
              LayoutTextFragment (anonymous) 4C5C2B94 "?" 
      LayoutText 4C5C2554              	#text "\n\n\n"

### ko...@chromium.org (2023-11-28)

Is it correct that this CHECK shouldn't hit?
https://chromium-review.googlesource.com/c/chromium/src/+/5065251

This hits with this test case.

### ko...@chromium.org (2023-11-28)

crrev.com/c/4487892 implemented `StyleContainmentScope::UpdateQuotes()`, which updates quote text (and probably counter text too?) across IFCs, including ones in the parent IFC of atomic inline.

Daniil, can you confirm if this is a desired behavior of CQ?

If yes, I think we need to modify `InlineLayoutAlgorithm` and `LineBreaker` to be aware of possible IFC changes after laying out block child nodes.

That chagne is likely not safe to merge, so I wonder if we should just crash to avoid use-after-fgree when this happens for now?

### ik...@chromium.org (2023-11-28)

Style containment should mean that we shouldn't be re-attaching quotes outside the element with style containment (I think).

### fu...@chromium.org (2023-11-29)

Yes, re-attaching outside the container with style containment sounds wrong.

### ko...@chromium.org (2023-11-29)

Thanks Ian and Rune. Updated Components.

If we prefer crashing in layout to downgrade this to a non-security issue, please assign back to me.

[Monorail components: -Blink>Layout Blink>CSS]

### cl...@chromium.org (2023-11-29)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Blink>Layout]

### gi...@appspot.gserviceaccount.com (2023-12-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/690ccf3b8dff0fcd4c8424075e92f8c61e31d227

commit 690ccf3b8dff0fcd4c8424075e92f8c61e31d227
Author: Daniil Sakhapov <sakhapov@chromium.org>
Date: Fri Dec 01 11:49:25 2023

Mark the outmost dirty style containment scope only if it has changed

During the creation of the style containment scope the ancestors are
created on the fly and are marked as outmost dirty in such cases.
But that's not correct as if nothing is changed in the new
ancestor, we don't need to update the outmost dirty scope.
Dirtying parent style containment scopes outside a size query container
during layout leads to modifying the layout box tree outside the query
container which is not allowed.

Bug: 1505164
Change-Id: Ic267a863201223d1b3c669ae5216c1eef7dddff7
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5075697
Reviewed-by: Rune Lillesveen <futhark@chromium.org>
Commit-Queue: Daniil Sakhapov <sakhapov@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1231862}

[add] https://crrev.com/690ccf3b8dff0fcd4c8424075e92f8c61e31d227/third_party/blink/web_tests/external/wpt/css/css-lists/counters-container-crash.html
[modify] https://crrev.com/690ccf3b8dff0fcd4c8424075e92f8c61e31d227/third_party/blink/renderer/core/css/style_containment_scope.cc
[modify] https://crrev.com/690ccf3b8dff0fcd4c8424075e92f8c61e31d227/third_party/blink/renderer/core/css/style_containment_scope_tree.cc


### cl...@chromium.org (2023-12-02)

ClusterFuzz testcase 4751138184691712 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1231859:1231867

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### [Deleted User] (2023-12-02)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-02)

Requesting merge to other stable M119 because latest trunk commit (1231862) appears to be after other stable branch point (1204232).

Requesting merge to stable M120 because latest trunk commit (1231862) appears to be after stable branch point (1217362).

Merge review required: M119 is already shipping to stable.

Merge review required: M120 has already been cut for stable release.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [119, 120].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-12-03)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-03)

Requesting merge to other stable M119 because latest trunk commit (1231862) appears to be after other stable branch point (1204232).

Requesting merge to stable M120 because latest trunk commit (1231862) appears to be after stable branch point (1217362).

Merge review required: M119 is already shipping to stable.

Merge review required: M120 has already been cut for stable release.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [119, 120].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sa...@chromium.org (2023-12-04)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-12-04)

This issue appears to be a duplicate of an earlier report of this https://crbug.com/chromium/1504036. Since this fix was landed here and requires security merge review, I'm unable to reverse the duplicate merge of these reports. This is a not to refer to https://crbug.com/chromium/1504036 for VRP consideration and CVE/release notes acknowledgement. 

### [Deleted User] (2023-12-04)

The older reward-topanel https://crbug.com/chromium/1504036 has been merged into this one. Please manually review this issue to see if the duplicate is potentially eligible for a reward.



### wh...@gmail.com (2023-12-04)

deleted

### am...@chromium.org (2023-12-04)

Hello, thanks for reaching out. Generally the first report of a given issue is only considered for a VRP reward. In this cases, as well as others prior, both reports will be considered based on actionable information provided. I cannot guarantee that this report will be eligible for a VRP reward, but it will be considered. This is why the reward-topanel label was not removed from this report. Both reports will be reviewed. A note was needing to be made here since sheriffbot tends to remove any attempt of reward-topanel labeling from the report marked as duplicate. 

### wh...@gmail.com (2023-12-04)

Thanks for your reply.


### [Deleted User] (2023-12-04)

Requesting merge to other stable M119 because latest trunk commit (1231862) appears to be after other stable branch point (1204232).

Requesting merge to stable M120 because latest trunk commit (1231862) appears to be after stable branch point (1217362).

Merge review required: M119 is already shipping to stable.

Merge review required: M120 has already been cut for stable release.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [119, 120].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-12-04)

There are no further planned releases of M119. 
https://crrev.com/c/5075697 approved for M120 merge. Please merge this fix to branch 6099 at your earliest convenience and before EOD Thursday, 7 December so this fix can be included in the first M120 security update.

### gi...@appspot.gserviceaccount.com (2023-12-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/27dc36f4224b646c6bed8c80e7ebaf06682a109e

commit 27dc36f4224b646c6bed8c80e7ebaf06682a109e
Author: Daniil Sakhapov <sakhapov@chromium.org>
Date: Tue Dec 05 10:47:15 2023

Mark the outmost dirty style containment scope only if it has changed

During the creation of the style containment scope the ancestors are
created on the fly and are marked as outmost dirty in such cases.
But that's not correct as if nothing is changed in the new
ancestor, we don't need to update the outmost dirty scope.
Dirtying parent style containment scopes outside a size query container
during layout leads to modifying the layout box tree outside the query
container which is not allowed.

(cherry picked from commit 690ccf3b8dff0fcd4c8424075e92f8c61e31d227)

Bug: 1505164
Change-Id: Ic267a863201223d1b3c669ae5216c1eef7dddff7
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5075697
Reviewed-by: Rune Lillesveen <futhark@chromium.org>
Commit-Queue: Daniil Sakhapov <sakhapov@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1231862}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5087689
Cr-Commit-Position: refs/branch-heads/6099@{#1382}
Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}

[add] https://crrev.com/27dc36f4224b646c6bed8c80e7ebaf06682a109e/third_party/blink/web_tests/external/wpt/css/css-lists/counters-container-crash.html
[modify] https://crrev.com/27dc36f4224b646c6bed8c80e7ebaf06682a109e/third_party/blink/renderer/core/css/style_containment_scope.cc
[modify] https://crrev.com/27dc36f4224b646c6bed8c80e7ebaf06682a109e/third_party/blink/renderer/core/css/style_containment_scope_tree.cc


### wh...@gmail.com (2023-12-07)

deleted

### am...@chromium.org (2023-12-07)

Hello, this fix was merged to 120 after 120 Stable release on Tuesday. A CVE will be issued when this fix is shipped in the next M120 Stable channel update. 

### wh...@gmail.com (2023-12-07)

Thanks.

### am...@chromium.org (2023-12-07)

Hello, thank you for the report. As mentioned in comments #30 and c#31, as such the Chrome VRP Panel has decided this report is unfortunately not eligible for a VRP reward. This issue is a duplicate of a previously report and we have pretty straight forward guidelines about duplicates [1]. Clusterfuzz did not find duplicates at the time because the valid, reproducible POC later provided by the other reporter in their report - but before this one - got overlooked since the issue was already triaged, but was assigned to a different owner than this issue.  

[1] https://g.co/chrome/vrp/#qualifying-vulnerabilities 

### wh...@gmail.com (2023-12-07)

All right.

### wh...@gmail.com (2023-12-07)

deleted

### am...@chromium.org (2023-12-07)

Release notes / CVE acknowledgement will need to go to the other reporter as per the policy

### wh...@gmail.com (2023-12-07)

Ok, thanks for your reply.

### am...@chromium.org (2023-12-11)

[for records-keeping] the fix for this issue is being released in tomorrow's respin; the associated release label (release-1-M120) has been added to https://crbug.com/chromium/1504036

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1505164?no_tracker_redirect=1

[Multiple monorail components: Blink>CSS, Blink>Layout]
[Monorail mergedwith: crbug.com/chromium/1504036]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-03-10)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40945761)*
