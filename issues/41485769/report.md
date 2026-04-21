# Security: Spoof to allow permission

| Field | Value |
|-------|-------|
| **Issue ID** | [41485769](https://issues.chromium.org/issues/41485769) |
| **Status** | Fixed |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Internals>Preload |
| **Platforms** | Windows |
| **Reporter** | sa...@gmail.com |
| **Assignee** | to...@chromium.org |
| **Created** | 2023-12-19 |
| **Bounty** | $1,000.00 |

## Description

deleted

## Attachments

- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)

## Timeline

### [Deleted User] (2023-12-19)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-12-21)

Hello Hafiizh, thanks for the report. I just attempted to reproduce this on Windows Canary 122.0.6198.0. This is not reproducing for me as depicted. 
I downloaded both files
1) I opened spoofpermission.html as the intended website
2) right-clicked Read Instructions
3) Selected Preview Link
4)The spoofpermission1 link was not displayed behind the preview link window, but on top of it

I attempted to reproduce this multiple times with the same result of the spoofpermission1 page being very visible. 

Is there a step I am missing here? 

### am...@chromium.org (2023-12-21)

Information pending from reporter in terms of completion of security triage, adding kenoss@ and toyoshim@ for visibility 
Windows and Mac, since Preview Link is available in both those OSes, and FoundIn-122 since Preview Link is only available starting in 122. 
Severity is based on more information from researcher since this does not reproduce for me as depicted. 
cc'ing kenoss@ and toyoshim@ as conveyed in https://crbug.com/chromium/1513185

### [Deleted User] (2023-12-21)

[Empty comment from Monorail migration]

### sa...@gmail.com (2023-12-21)

deleted

### [Deleted User] (2023-12-21)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bb...@google.com (2023-12-21)

Attempting this does not work on the mac, permissions dialogue pops up in another window and the preview pane does not occlude it or interfere with it no matter what I could do with it. I tried a number of different window sizes and locations and was unsucessful in any way. So I don't believe if this can be made to work on windows, it can be made to work on the mac. 

### am...@chromium.org (2023-12-21)

Note: the link in step #2 is actually Read Instruction not Google for this POC 
Removing Mac as an affected OS, since Mac provides a separate prompt to request perform from Chrome for the microphone. Also, the spoofpermission1 window displays completely overlaid in front of the spoofpermission window on Mac and is wholly visible to the user. 

On Windows, this also doesn't work if the browser window isn't open to full size / covering the entire desktop. In various attempts to repro, depending on the size or position of the browser window, I could view the spoofpermission1 window. When the browser window is full size I can see the small window briefly appear before it is hidden behind the main browser window. Then you still have to convince the user to tab tab enter. 
Based on the preconditions and workflow, assessing as low severity.

[Monorail components: Internals>Preload]

### [Deleted User] (2023-12-22)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-12-22)

[Empty comment from Monorail migration]

### to...@chromium.org (2024-01-10)

This is not a launched feature, but a WIP canary/dev experimental. The behavior is not in the final shape.
Preview window are running in a feature sandbox that allows only chosen features, and will be disallowed to open a new window.

### to...@chromium.org (2024-01-10)

[Empty comment from Monorail migration]

### to...@chromium.org (2024-01-10)

[Empty comment from Monorail migration]

### sa...@gmail.com (2024-01-10)

hi toyoshim@chromium.org shouldn't the large report ID be a duplicate of the small report ID?  1513196 duplicate to (1513185)

### to...@chromium.org (2024-01-10)

I just prefer to merge one to the other that already had more context, in order to keep as many information as available after the merge.

### to...@chromium.org (2024-01-12)

[Empty comment from Monorail migration]

### to...@chromium.org (2024-01-16)

[Empty comment from Monorail migration]

### ke...@chromium.org (2024-01-16)

https://b.corp.google.com/issues/320386573
We are planning to fix it by cancelling preview when focus is lost.


### [Deleted User] (2024-01-24)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-24)

This issue was migrated from crbug.com/chromium/1513196?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail blocked-on: crbug.com/chromium/1517208]
[Monorail mergedwith: crbug.com/chromium/1513185]
[Monorail components added to Component Tags custom field.]

### to...@chromium.org (2024-02-06)

https://issues.chromium.org/u/1/issues/41485769
https://issues.chromium.org/u/1/issues/41485752
These two are closed as duplications of this.

### to...@chromium.org (2024-02-06)

https://b.corp.google.com/issues/320386573 is also merged.

The original description follows (as currently b/ doesn't do expected information merge among Chromium and Chrome)
----

Currently, preview is cancelled if mouse release received outside preview window [1]. (Note that it's just a tentative one.)

Opening and holding another type of window (rather than normal window containing normal tab) can be problematic and expose security risk. E.g. [2] and [3]. Note that

Autofill had a similar bug [4] with multiple noraml window. It's fixed by enabling autofill only on active tab.
Non-floating windows, such as JS alert and omnibox completion are obsecured by other windows. It would be not a problem because of they contains low-security-risk contents.
Floating windows, such as context menu, overlays other windows. It would be not a problem because they vanishes if focus is lost.
Possible solutions:

Disable autofill if preview window is closed. Jan's prototype [5].
It fixes [3] (autofill with preview).

Don't use z-order for preview window and let other floating windows overlays.
Negative. It will expose the same attack surface as [4].

Cancel preview if focus is lost.
It follows floating windows convention the above and will fix all related bugs.

We are planning to fix it with 3.

[1] https://source.chromium.org/chromium/chromium/src/+/refs/tags/122.0.6251.1:chrome/browser/preloading/preview/preview_tab.cc;l=71-76

[2] https://bugs.chromium.org/p/chromium/issues/detail?id=1513196

[3] https://bugs.chromium.org/p/chromium/issues/detail?id=1513179

[4] https://bugs.chromium.org/p/chromium/issues/detail?id=1239760

[5] https://chromium-review.googlesource.com/c/chromium/src/+/5177188

### sa...@gmail.com (2024-03-06)

Hello any updates?

### am...@chromium.org (2024-03-06)

It looks like there has been some progress in terms of the team making a determination about how they will resolve this issue. Since this is a low-severity issue, there is no SLO for this issue to be resolved. Thank you for your patience in the meantime while the team works on this issue.

### ap...@google.com (2024-03-19)

Project: chromium/src
Branch: main

commit ba9d4db90c06bf0085c4a0490caf5a757029e0c7
Author: Takashi Toyoshima <toyoshim@chromium.org>
Date:   Tue Mar 19 02:41:42 2024

    LinkPreview: Stop specifying floating window and capturing
    
    This patch changes to override OnNativeBlur() to close the
    preview tab, and also changes to use AuditWebInputEvent()
    to hook up mouse events to trigger a tab promotion.
    
    OnNativeBlur() is also called before the mouse down event
    unfortunately. So, the closing tab is executed asynchronously
    so that if a mouse down event follows synchronously, we
    do the tab promotion before executing the asynchronous tab closure.
    
    Change-Id: I642b5a03b7d1e7f164ba24af8491d3ad99aa49ca
    Bug: b/305007647, b/41485769
    Fixed: b/41485769
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5364174
    Commit-Queue: Takashi Toyoshima <toyoshim@chromium.org>
    Reviewed-by: Scott Violet <sky@chromium.org>
    Reviewed-by: Kouhei Ueno <kouhei@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1274660}

M       chrome/browser/preloading/preview/preview_tab.cc

https://chromium-review.googlesource.com/5364174


### sa...@gmail.com (2024-04-03)

hello any updates?

### am...@chromium.org (2024-04-04)

This is in the VRP Panel queue and will be assessed at a forthcoming VRP panel session. Sorry, we are a bit behind on reward decisions for some low severity bugs, and appreciate your patience!

### am...@google.com (2024-04-25)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2024-04-26)

Congratulations Hafiizh! The Chrome VRP Panel has decided to award you $1,000 for this report of a lower impact UI spoof. Thank you for your efforts and reporting this issue to us!

### sa...@gmail.com (2024-04-26)

Thank you amy

### pe...@google.com (2024-06-26)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/41485769)*
