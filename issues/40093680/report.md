# Security: http authentication spoof on chrome iOS (repro issue 884179)

| Field | Value |
|-------|-------|
| **Issue ID** | [40093680](https://issues.chromium.org/issues/40093680) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Mobile>iOSWeb>Security |
| **Platforms** | iOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | eu...@chromium.org |
| **Created** | 2019-01-09 |
| **Bounty** | $500.00 |

## Description

**VERSION**  

Chrome Version: 72.0.3626.28 beta  

Operating System: iOS 12.1.2

**REPRODUCTION CASE**

1. Lunch the PoC.html
2. Click on the red button, then click on the green button quickly.

The authentication dialog should be gone after navigation (see <https://crbug.com/chromium/884179>).

## Attachments

- [screenshot.jpeg](attachments/screenshot.jpeg) (image/jpeg, 78.4 KB)
- [poc.html](attachments/poc.html) (text/plain, 1.2 KB)
- [AA29DEDB-D2E2-47E9-8335-2C78DAC5AB65.MOV](attachments/AA29DEDB-D2E2-47E9-8335-2C78DAC5AB65.MOV) (video/quicktime, 1.4 MB)

## Timeline

### ch...@gmail.com (2019-01-09)

[Empty comment from Monorail migration]

### rs...@chromium.org (2019-01-09)

eugenebut: Can you take a look or help route?

[Monorail components: Mobile>iOSWeb>Security]

### eu...@chromium.org (2019-01-09)

Dialogs are dismissed after Navigation was started. The fix would be to dismiss the dialogs when the navigation is committed: crrev.com/c/1403655

Kurt, I intentionally omitting detailed CL description to have codereview conversation here. I can't think how crrev.com/c/1403655 can break other things, because after navigation is committed we no longer need dialogs from the previous page.

### eu...@chromium.org (2019-01-09)

[Empty comment from Monorail migration]

### kk...@chromium.org (2019-01-10)

Yep, your CL looks good. I sent it to the CQ.

### bu...@chromium.org (2019-01-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/25ea09c09d46906ce3f971205815bb0c26bde84a

commit 25ea09c09d46906ce3f971205815bb0c26bde84a
Author: Eugene But <eugenebut@google.com>
Date: Thu Jan 10 22:03:03 2019

Dismiss dialogs after navigation is committed.

Bug: 920048
Change-Id: Iab26503ec0c48124659765831ae0621243c1e02d
Reviewed-on: https://chromium-review.googlesource.com/c/1403655
Commit-Queue: Kurt Horimoto <kkhorimoto@chromium.org>
Reviewed-by: Kurt Horimoto <kkhorimoto@chromium.org>
Cr-Commit-Position: refs/heads/master@{#621768}
[modify] https://crrev.com/25ea09c09d46906ce3f971205815bb0c26bde84a/ios/chrome/browser/tabs/tab.mm


### eu...@chromium.org (2019-01-10)

Srikanth, could you please verify with the next Canary build. Thanks!

### eu...@chromium.org (2019-01-10)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-01-10)

This bug requires manual review: Less than 15 days to go before AppStore submit on M72
Please contact the milestone owner if you have questions.
Owners: govind@(Android), kariahda@(iOS), djmm@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-01-11)

[Empty comment from Monorail migration]

### ka...@chromium.org (2019-01-11)

[Empty comment from Monorail migration]

### sr...@chromium.org (2019-01-11)

Looks good. Verified on M73.0.3668.0 canary
Device: iPhoneX, iPhone7plus
iOS: 12.1.2, 12.1.3 beta

HTTPAuth dialog is dismissed as soon as the page redirects to amazon.com

### ka...@chromium.org (2019-01-11)

Approved, please merge asap.

### bu...@chromium.org (2019-01-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/43438edc9ba74fb2950f4ea3dd0fd00e89b6a1e5

commit 43438edc9ba74fb2950f4ea3dd0fd00e89b6a1e5
Author: Eugene But <eugenebut@google.com>
Date: Fri Jan 11 21:14:03 2019

Dismiss dialogs after navigation is committed.

TBR=eugenebut@google.com

(cherry picked from commit 25ea09c09d46906ce3f971205815bb0c26bde84a)

Bug: 920048
Change-Id: Iab26503ec0c48124659765831ae0621243c1e02d
Reviewed-on: https://chromium-review.googlesource.com/c/1403655
Commit-Queue: Kurt Horimoto <kkhorimoto@chromium.org>
Reviewed-by: Kurt Horimoto <kkhorimoto@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#621768}
Reviewed-on: https://chromium-review.googlesource.com/c/1407649
Reviewed-by: Eugene But <eugenebut@chromium.org>
Cr-Commit-Position: refs/branch-heads/3626@{#651}
Cr-Branched-From: d897fb137fbaaa9355c0c93124cc048824eb1e65-refs/heads/master@{#612437}
[modify] https://crrev.com/43438edc9ba74fb2950f4ea3dd0fd00e89b6a1e5/ios/chrome/browser/tabs/tab.mm


### cr...@appspot.gserviceaccount.com (2019-01-11)

The following revision refers to this bug: 
https://chromium.googlesource.com/chromium/src.git/+/43438edc9ba74fb2950f4ea3dd0fd00e89b6a1e5

Commit: 43438edc9ba74fb2950f4ea3dd0fd00e89b6a1e5
Author: eugenebut@google.com
Commiter: eugenebut@chromium.org
Date: 2019-01-11 21:14:03 +0000 UTC

Dismiss dialogs after navigation is committed.

TBR=eugenebut@google.com

(cherry picked from commit 25ea09c09d46906ce3f971205815bb0c26bde84a)

Bug: 920048
Change-Id: Iab26503ec0c48124659765831ae0621243c1e02d
Reviewed-on: https://chromium-review.googlesource.com/c/1403655
Commit-Queue: Kurt Horimoto <kkhorimoto@chromium.org>
Reviewed-by: Kurt Horimoto <kkhorimoto@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#621768}
Reviewed-on: https://chromium-review.googlesource.com/c/1407649
Reviewed-by: Eugene But <eugenebut@chromium.org>
Cr-Commit-Position: refs/branch-heads/3626@{#651}
Cr-Branched-From: d897fb137fbaaa9355c0c93124cc048824eb1e65-refs/heads/master@{#612437}

### na...@google.com (2019-01-14)

[Empty comment from Monorail migration]

### na...@google.com (2019-01-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### pa...@chromium.org (2019-01-17)

Congrats! The Panel decided to reward $500 for this report. 

### aw...@google.com (2019-01-21)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-04-19)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2019-04-19)

This issue was migrated from crbug.com/chromium/920048?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-03-19)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093680)*
