# Security:  Type Confusion in LayoutBlockFlow::CreateLineBoxes

| Field | Value |
|-------|-------|
| **Issue ID** | [40093474](https://issues.chromium.org/issues/40093474) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Layout, Blink>SVG |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | or...@gmail.com |
| **Assignee** | fu...@chromium.org |
| **Created** | 2018-12-15 |
| **Bounty** | $3,000.00 |

## Description

Please credit this vulnerability to: Alexandru Pitis, Microsoft Browser Vulnerability Research

Affected version: 71.0.3357.0, I had it also crash 73.0.3635.0 Release but I didn't triage it on this version.

Vulnerability report:

CreateLineBoxes contains following code:
​
InlineFlowBox* LayoutBlockFlow::CreateLineBoxes(LineLayoutItem line_layout_item,​
                                                const LineInfo& line_info,​
                                                InlineBox* child_box) {​
[...]​
  do {​
    if (line_depth++ >= kCMaxLineDepth ||​
        (IsLayoutNGBlockFlow() && line_layout_item.IsLayoutBlockFlow())) {​
      line_layout_item = LineLayoutItem(this);​
    }​
​
    SECURITY_DCHECK(line_layout_item.IsLayoutInline() ||​
                    line_layout_item.IsEqual(this));​
​
    LineLayoutInline inline_flow(​
        !line_layout_item.IsEqual(this) ? line_layout_item : nullptr);​
​
[...]​
​
LineLayoutInline is a wrapper which contains a layout object within it. The idea of this wrapper is that it should be only fed classes descending from LayoutInline ( hence SECURITY_DCHECK above ).​
​
For some reason, POC seems to manage to fill in a LayoutSVGText object in, which is a descendant of LayoutObject. This means that this wrapper will exhibit undefined behavior once LineLayoutInline::ToLayoutInline is called ( which static_casts to LayoutInline type )​
​
Following command has been used to monitor line_layout_item incoming into the function:
​
bp chrome_child!blink::LayoutBlockFlow::CreateLineBoxes "?@rdx; dps @rdx; g;"​

Note how eventually a line_layout_item._layout_object contains a LayoutSVGText vtable reference indicating wrong object type.:
​
Evaluate expression: 20695399624512 = 000012d2`85f16f40​
000012d2`85f16f40  00007ff9`9aaa47c0 chrome_child!??_7LayoutSVGText@blink@@6BImageResourceObserver@1@@​
000012d2`85f16f48  00007ff9`9aaa5040 chrome_child!??_7LayoutSVGText@blink@@6BDisplayItemClient@1@@​
000012d2`85f16f50  bebebebe`bebebe16​
000012d2`85f16f58  bebebebe`bebebe09​
000012d2`85f16f60  000012bc`85f3e4a0​
000012d2`85f16f68  00007ebc`e11eff00​
000012d2`85f16f70  000012ce`86021200​
000012d2`85f16f78  000012ce`86021340​
000012d2`85f16f80  00000000`00000000​
000012d2`85f16f88  8023f026`800843a0​
000012d2`85f16f90  00000000`00000000​
000012d2`85f16f98  00000000`00000000​
000012d2`85f16fa0  00000000`00000000​
000012d2`85f16fa8  00000000`00000000​
000012d2`85f16fb0  00000000`00000000​
000012d2`85f16fb8  00000000`00000000​
​
HTML POC is attached. On Debug/ASAN builds, this POC should trigger the SECURITY_DCHECK in CreateLineBoxes. 

Thanks,
Alex, Microsoft Browser Vulnerability Research


## Attachments

- [poc_type_confusion.html](attachments/poc_type_confusion.html) (text/plain, 522.6 KB)
- [tc.html](attachments/tc.html) (text/plain, 310 B)

## Timeline

### cl...@chromium.org (2018-12-16)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4666700370542592.

### cl...@chromium.org (2018-12-16)

Detailed report: <https://clusterfuzz.com/testcase?key=4666700370542592>

Job Type: linux\_asan\_chrome\_mp  

Platform Id: linux

Crash Type: Security DCHECK failure  

Crash Address:  

Crash State:  

line\_layout\_item.IsLayoutInline() || line\_layout\_item.IsEqual(this) in layout\_bl  

blink::LayoutBlockFlow::CreateLineBoxes  

blink::LayoutBlockFlow::ConstructLine

Sanitizer: address (ASAN)

Reproducer Testcase: <https://clusterfuzz.com/download?testcase_id=4666700370542592>

See <https://github.com/google/clusterfuzz-tools> for instructions to reproduce this bug locally.

**Note: This crash might not be reproducible with the provided testcase. That said, for the past 14 days we've been seeing this crash frequently. If you are unable to reproduce this, please try a speculative fix based on the crash stacktrace in the report. The fix can be verified by looking at the crash statistics in the report, a day after the fix is deployed. We will auto-close the bug if the crash is not seen for 14 days.**

### ca...@chromium.org (2018-12-17)

[Empty comment from Monorail migration]

[Monorail components: Blink>Layout]

### ca...@chromium.org (2018-12-17)

wangxianzhu: Passing to you from recent activity and the owners file. Can you PTAL and help find a proper owner? Thanks.

### wa...@chromium.org (2018-12-17)

The DCHECK failure happens when we are trying to create a line box for a LayoutSVGText in a LayoutBlockFlow:

*  LayoutBlockFlow (anonymous) 0x360403e24d20
     LayoutSVGInlineText 0x360403ef4b10	#text "\n\n"
     LayoutSVGContainer 0x360403e98250	g id="svgvar00013" (editable)
       LayoutSVGResourceLinearGradient 0x360403e70388	linearGradient id="svgvar00014" (editable)
     LayoutSVGInlineText 0x360403ef4c70	#text "\n\n"
     LayoutSVGContainer 0x360403e98010	g id="svgvar00015" (editable)
       LayoutSVGResourcePattern 0x360403e70260	pattern id="svgvar00031" style="border-image-slice: 25 83 0 1 fill; border-right-color: white; snap-height: 0px; white: fuchsia; mso-width-source: userset" (editable)
+      LayoutSVGText 0x360403ee8010	text id="svgvar00032" (editable)
         LayoutSVGInlineText 0x360403ef4dd0	#text "Text"
     LayoutSVGInlineText 0x360403ef4f30	#text "\n\n"
     LayoutText 0x360403e609d0	#text "\n\n"

This seems wrong because a LayoutSVGText should not be a part of a block flow.

### cl...@chromium.org (2018-12-17)

Detailed report: <https://clusterfuzz.com/testcase?key=4666700370542592>

Job Type: linux\_asan\_chrome\_mp  

Platform Id: linux

Crash Type: Security DCHECK failure  

Crash Address:  

Crash State:  

line\_layout\_item.IsLayoutInline() || line\_layout\_item.IsEqual(this) in layout\_bl  

blink::LayoutBlockFlow::CreateLineBoxes  

blink::LayoutBlockFlow::ConstructLine

Sanitizer: address (ASAN)

Reproducer Testcase: <https://clusterfuzz.com/download?testcase_id=4666700370542592>

See <https://github.com/google/clusterfuzz-tools> for instructions to reproduce this bug locally.

**Note: This crash might not be reproducible with the provided testcase. That said, for the past 14 days we've been seeing this crash frequently. If you are unable to reproduce this, please try a speculative fix based on the crash stacktrace in the report. The fix can be verified by looking at the crash statistics in the report, a day after the fix is deployed. We will auto-close the bug if the crash is not seen for 14 days.**

### ms...@chromium.org (2018-12-18)

Looks like a Shadow DOM issue to me. An SVG 'g' element is placed right under an HTML 'div' element. That can't be good. See reduced test case in attachment.

LayoutView 0x2b1daa404010              	#document
  LayoutBlockFlow 0x2b1daa424010       	HTML
    LayoutBlockFlow 0x2b1daa424140     	BODY
      LayoutBlockFlow 0x2b1daa424270   	P
        LayoutText 0x2b1daa434010      	#text "PASS if no crash or DCHECK failure."
      LayoutBlockFlow (anonymous) 0x2b1daa4243a0
        LayoutSVGRoot 0x2b1daa444010   	svg id="svgvar00001"
          LayoutSVGForeignObject 0x2b1daa450010	foreignObject
*           LayoutBlockFlow 0x2b1daa4244d0	DIV
              LayoutSVGContainer 0x2b1daa458010	g
                LayoutSVGForeignObject 0x2b1daa450178	foreignObject
                  LayoutText 0x2b1daa4340e0	#text "Jeg er en and."
              LayoutSVGInlineText 0x2b1daa464010	#text "\n"
        LayoutText 0x2b1daa4341b0      	#text "\n"

### fu...@chromium.org (2018-12-18)

You can't attach a shadow root to <svg> in Shadow DOM v1, which is good.

The answer to the question here is yes (certainly necessary for shadow dom v0):

https://cs.chromium.org/chromium/src/third_party/blink/renderer/core/svg/svg_element.cc?type=cs&sq=package:chromium&g=0&l=1038-1039


[Monorail components: -Blink>Layout Blink>SVG]

### fu...@chromium.org (2018-12-18)

[Empty comment from Monorail migration]

### cl...@chromium.org (2018-12-18)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Blink>Layout]

### fu...@chromium.org (2018-12-18)

https://chromium-review.googlesource.com/c/chromium/src/+/1382494

### bu...@chromium.org (2018-12-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/032c3339bfb454c65ce38e7eafe49a54bac83073

commit 032c3339bfb454c65ce38e7eafe49a54bac83073
Author: Rune Lillesveen <futhark@chromium.org>
Date: Tue Dec 18 14:45:19 2018

Fix SVG crash for v0 distribution into foreignObject.

We require a parent element to be an SVG element for non-svg-root
elements in order to create a LayoutObject for them. However, we checked
the light tree parent element, not the flat tree one which is the parent
for the layout tree construction. Note that this is just an issue in
Shadow DOM v0 since v1 does not allow shadow roots on SVG elements.

Bug: 915469
Change-Id: Id81843abad08814fae747b5bc81c09666583f130
Reviewed-on: https://chromium-review.googlesource.com/c/1382494
Reviewed-by: Fredrik Söderquist <fs@opera.com>
Commit-Queue: Rune Lillesveen <futhark@chromium.org>
Cr-Commit-Position: refs/heads/master@{#617487}
[modify] https://crrev.com/032c3339bfb454c65ce38e7eafe49a54bac83073/third_party/blink/renderer/core/svg/svg_element.cc
[add] https://crrev.com/032c3339bfb454c65ce38e7eafe49a54bac83073/third_party/blink/web_tests/svg/foreignObject/shadow-dom-v0-crash.html


### fu...@chromium.org (2018-12-18)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-12-18)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-12-20)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-12-20)

This bug requires manual review: M72 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: govind@(Android), kariahda@(iOS), djmm@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ab...@google.com (2018-12-20)

[Empty comment from Monorail migration]

### ab...@google.com (2018-12-20)

branch:3626

### bu...@chromium.org (2018-12-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/38d67ec50027d2357bcbbbf194d1618137156bb3

commit 38d67ec50027d2357bcbbbf194d1618137156bb3
Author: Rune Lillesveen <futhark@chromium.org>
Date: Thu Dec 20 22:01:34 2018

Fix SVG crash for v0 distribution into foreignObject.

We require a parent element to be an SVG element for non-svg-root
elements in order to create a LayoutObject for them. However, we checked
the light tree parent element, not the flat tree one which is the parent
for the layout tree construction. Note that this is just an issue in
Shadow DOM v0 since v1 does not allow shadow roots on SVG elements.

Bug: 915469
Change-Id: Id81843abad08814fae747b5bc81c09666583f130
Reviewed-on: https://chromium-review.googlesource.com/c/1382494
Reviewed-by: Fredrik Söderquist <fs@opera.com>
Commit-Queue: Rune Lillesveen <futhark@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#617487}(cherry picked from commit 032c3339bfb454c65ce38e7eafe49a54bac83073)
Reviewed-on: https://chromium-review.googlesource.com/c/1387454
Reviewed-by: Rune Lillesveen <futhark@chromium.org>
Cr-Commit-Position: refs/branch-heads/3626@{#491}
Cr-Branched-From: d897fb137fbaaa9355c0c93124cc048824eb1e65-refs/heads/master@{#612437}
[modify] https://crrev.com/38d67ec50027d2357bcbbbf194d1618137156bb3/third_party/blink/renderer/core/svg/svg_element.cc
[add] https://crrev.com/38d67ec50027d2357bcbbbf194d1618137156bb3/third_party/blink/web_tests/svg/foreignObject/shadow-dom-v0-crash.html


### cr...@appspot.gserviceaccount.com (2018-12-20)

The following revision refers to this bug: 
https://chromium.googlesource.com/chromium/src.git/+/38d67ec50027d2357bcbbbf194d1618137156bb3

Commit: 38d67ec50027d2357bcbbbf194d1618137156bb3
Author: futhark@chromium.org
Commiter: futhark@chromium.org
Date: 2018-12-20 22:01:34 +0000 UTC

Fix SVG crash for v0 distribution into foreignObject.

We require a parent element to be an SVG element for non-svg-root
elements in order to create a LayoutObject for them. However, we checked
the light tree parent element, not the flat tree one which is the parent
for the layout tree construction. Note that this is just an issue in
Shadow DOM v0 since v1 does not allow shadow roots on SVG elements.

Bug: 915469
Change-Id: Id81843abad08814fae747b5bc81c09666583f130
Reviewed-on: https://chromium-review.googlesource.com/c/1382494
Reviewed-by: Fredrik Söderquist <fs@opera.com>
Commit-Queue: Rune Lillesveen <futhark@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#617487}(cherry picked from commit 032c3339bfb454c65ce38e7eafe49a54bac83073)
Reviewed-on: https://chromium-review.googlesource.com/c/1387454
Reviewed-by: Rune Lillesveen <futhark@chromium.org>
Cr-Commit-Position: refs/branch-heads/3626@{#491}
Cr-Branched-From: d897fb137fbaaa9355c0c93124cc048824eb1e65-refs/heads/master@{#612437}

### na...@google.com (2019-01-07)

[Empty comment from Monorail migration]

### na...@google.com (2019-01-10)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### pa...@chromium.org (2019-01-10)

Thanks for your report. The panel has decided to reward $3,000 :) 

Since you are a new reporter a member of our finance will be in touch. 

Additionally, how would you like to be credited in release notes?


### na...@google.com (2019-01-10)

[Empty comment from Monorail migration]

### or...@gmail.com (2019-01-11)

Hi,

We'll like to donate this bounty to charity. I understood from my team leader that there's already work underway with you to set this up.

Thanks,
Alex

### or...@gmail.com (2019-01-11)

Ah yes, please credit me as follows:
Alexandru Pitis, Microsoft Browser Vulnerability Research

### aw...@chromium.org (2019-01-28)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-01-28)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-02-19)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-03-27)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mm...@chromium.org (2019-05-13)

[Empty comment from Monorail migration]

### mm...@chromium.org (2019-05-17)

[Empty comment from Monorail migration]

### is...@google.com (2019-05-17)

This issue was migrated from crbug.com/chromium/915469?no_tracker_redirect=1

[Multiple monorail components: Blink>Layout, Blink>SVG]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093474)*
