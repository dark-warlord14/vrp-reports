# Security: Drag and Drop XSS

| Field | Value |
|-------|-------|
| **Issue ID** | [40059347](https://issues.chromium.org/issues/40059347) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>DataTransfer, Blink>Editing, Blink>SVG |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | mi...@bentkowski.info |
| **Assignee** | xi...@chromium.org |
| **Created** | 2022-04-10 |
| **Bounty** | $2,000.00 |

## Description

This bug is similar to many Copy&Paste bugs I reported for Chromium (examples: https://crbug.com/chromium/1011950, https://crbug.com/chromium/1040755, https://crbug.com/chromium/1065761, https://crbug.com/chromium/1141350). The difference is that now I'm focusing on drag and drop.

Essentially, when you drag&drop an HTML data into an element that is content-editable, the HTML is automatically sanitized. I used to assume it is the same sanitization process that also works for copy&paste. It turns out that's not the case. I've found a way to execute arbitrary JavaScript on drag&drop by using SVG <use> tag.

Chromium blocks drag&drop for iframes if the target origin is different than the source origin. However, it doesn't block if the drag starts in another window. So the attack scenario is possible, although much less likely than in the case of copy&paste. It is still a bug, though, from a technical stand-point hence I'm reporting it.

Below is a short proof of concept that proves the exploit on the same origin but it also works cross-origin if you drag and drop between two windows (check the attached video; the target is: https://developers-dot-devsite-v2-prod.appspot.com/transliterate/v1/richedittransliteration). Just drag the "drag me" box onto the contenteditable field below to see an alert


<!DOCTYPE html>
<meta charset="UTF-8">
<title>Drag And Drop Proof of Concept</title>
<script>const payload = `
  <svg><use href="data:image/svg+xml,&lt;svg id='x' xmlns='http://www.w3.org/2000/svg'&gt;&lt;image href='' onerror='alert(1337)' /&gt;&lt;script&gt;alert(2)&lt;/script&gt;&lt;/svg&gt;#x" />
`;</script>
<div
  style="background:lightblue; padding: 2em; width:100px" 
  draggable=true
  ondragstart="event.dataTransfer.setData('text/html', payload)"
>Drag me!</div>
<div contenteditable style="border: 1px solid black; padding:2em; margin-top: 2em; height:200px">Drop here!</div>



## Attachments

- [recording.mov](attachments/recording.mov) (video/quicktime, 1.4 MB)

## Timeline

### [Deleted User] (2022-04-10)

[Empty comment from Monorail migration]

### rs...@chromium.org (2022-04-11)

Thanks for the report. I can confirm this on M100 - M102.

[Monorail components: Blink>DataTransfer Blink>Editing Blink>SVG]

### [Deleted User] (2022-04-11)

[Empty comment from Monorail migration]

### sc...@chromium.org (2022-04-11)

This is related to another bug where it is argued that we should not execute script in SVG from data urls, which would fix this I believe because we would not run the script in the <use> tag.

### gi...@appspot.gserviceaccount.com (2022-04-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/5164a0fe3391283663e1196cf4576ec233985e89

commit 5164a0fe3391283663e1196cf4576ec233985e89
Author: Xiaocheng Hu <xiaochengh@chromium.org>
Date: Tue Apr 12 02:03:00 2022

Sanitize DragData markup before inserting it into document

Fixed: 1315040
Change-Id: I8a0ddfb983d12c185f7e943d3d5277788199b011
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3579670
Quick-Run: Xiaocheng Hu <xiaochengh@chromium.org>
Auto-Submit: Xiaocheng Hu <xiaochengh@chromium.org>
Reviewed-by: Kent Tamura <tkent@chromium.org>
Commit-Queue: Kent Tamura <tkent@chromium.org>
Cr-Commit-Position: refs/heads/main@{#991324}

[add] https://crrev.com/5164a0fe3391283663e1196cf4576ec233985e89/third_party/blink/web_tests/editing/pasteboard/drag-and-drop-svg-use-sanitize.html
[modify] https://crrev.com/5164a0fe3391283663e1196cf4576ec233985e89/third_party/blink/renderer/core/page/drag_data.cc


### mi...@bentkowski.info (2022-04-12)

Wow, that was quick! I checked the fix and it looks fine. Thanks!

### [Deleted User] (2022-04-12)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-12)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-04-12)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-12)

Requesting merge to beta M101 because latest trunk commit (991324) appears to be after beta branch point (982481).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-04-13)

Merge review required: M101 is already shipping to beta.

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
Owners: benmason (Android), harrysouders (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### xi...@chromium.org (2022-04-13)

1. Why does your merge fit within the merge criteria for these milestones?

It's a security fix.

2. What changes specifically would you like to merge? Please link to Gerrit.

https://chromium-review.googlesource.com/c/chromium/src/+/3579670

3. Have the changes been released and tested on canary?

Yes

4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?

No

5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents

No, and maybe N/A? This change doesn't have anything specific to ChromeOS

6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Maybe N/A? Because we are not merging to the stable channel

### am...@chromium.org (2022-04-15)

M101 merge approved, please merge this fix to branch 4951 at your earliest convenience and NLT noon PDT, Tuesday, 19 April 

### gi...@appspot.gserviceaccount.com (2022-04-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/e2b8856012e068e16a9a343525961972bc45b480

commit e2b8856012e068e16a9a343525961972bc45b480
Author: Xiaocheng Hu <xiaochengh@chromium.org>
Date: Mon Apr 18 01:14:45 2022

[M101] Sanitize DragData markup before inserting it into document

(cherry picked from commit 5164a0fe3391283663e1196cf4576ec233985e89)

Fixed: 1315040
Change-Id: I8a0ddfb983d12c185f7e943d3d5277788199b011
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3579670
Quick-Run: Xiaocheng Hu <xiaochengh@chromium.org>
Auto-Submit: Xiaocheng Hu <xiaochengh@chromium.org>
Reviewed-by: Kent Tamura <tkent@chromium.org>
Commit-Queue: Kent Tamura <tkent@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#991324}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3588887
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/4951@{#831}
Cr-Branched-From: 27de6227ca357da0d57ae2c7b18da170c4651438-refs/heads/main@{#982481}

[add] https://crrev.com/e2b8856012e068e16a9a343525961972bc45b480/third_party/blink/web_tests/editing/pasteboard/drag-and-drop-svg-use-sanitize.html
[modify] https://crrev.com/e2b8856012e068e16a9a343525961972bc45b480/third_party/blink/renderer/core/page/drag_data.cc


### [Deleted User] (2022-04-18)

LTS Milestone M96

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2022-04-18)

[Empty comment from Monorail migration]

### rz...@google.com (2022-04-18)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-18)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2022-04-18)

1. Just https://crrev.com/c/3589799
2. Low, no conflicts
3. 101
4. Yes

### gm...@google.com (2022-04-19)

[Empty comment from Monorail migration]

### am...@google.com (2022-04-22)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-04-22)

Thank you for this report! The VRP Panel has decided to award you $2,000 for your report of this issue. Thank you for your efforts and taking the time to report this to us. 

### mi...@bentkowski.info (2022-04-22)

Thanks!

### gm...@google.com (2022-04-22)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-04-25)

[Empty comment from Monorail migration]

### am...@google.com (2022-04-25)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-04-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/12ba78f3fa7a42c9a6a15f7a8248453ffef91a08

commit 12ba78f3fa7a42c9a6a15f7a8248453ffef91a08
Author: Xiaocheng Hu <xiaochengh@chromium.org>
Date: Mon Apr 25 20:57:43 2022

[M96-LTS] Sanitize DragData markup before inserting it into document

(cherry picked from commit 5164a0fe3391283663e1196cf4576ec233985e89)

Fixed: 1315040
Change-Id: I8a0ddfb983d12c185f7e943d3d5277788199b011
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3579670
Quick-Run: Xiaocheng Hu <xiaochengh@chromium.org>
Auto-Submit: Xiaocheng Hu <xiaochengh@chromium.org>
Commit-Queue: Kent Tamura <tkent@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#991324}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3589799
Reviewed-by: Achuith Bhandarkar <achuith@chromium.org>
Owners-Override: Achuith Bhandarkar <achuith@chromium.org>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Cr-Commit-Position: refs/branch-heads/4664@{#1602}
Cr-Branched-From: 24dc4ee75e01a29d390d43c9c264372a169273a7-refs/heads/main@{#929512}

[add] https://crrev.com/12ba78f3fa7a42c9a6a15f7a8248453ffef91a08/third_party/blink/web_tests/editing/pasteboard/drag-and-drop-svg-use-sanitize.html
[modify] https://crrev.com/12ba78f3fa7a42c9a6a15f7a8248453ffef91a08/third_party/blink/renderer/core/page/drag_data.cc


### rz...@google.com (2022-04-26)

[Empty comment from Monorail migration]

### am...@google.com (2022-04-26)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-20)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2022-07-26)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-29)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1315040?no_tracker_redirect=1

[Multiple monorail components: Blink>DataTransfer, Blink>Editing, Blink>SVG]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059347)*
