# Security: UAF in Drag and Drop Download

| Field | Value |
|-------|-------|
| **Issue ID** | [40054619](https://issues.chromium.org/issues/40054619) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>DataTransfer, UI>Browser>Downloads |
| **Platforms** | Windows |
| **Reporter** | ra...@gmail.com |
| **Assignee** | qi...@chromium.org |
| **Created** | 2021-01-29 |
| **Bounty** | $20,000.00 |

## Description

**VULNERABILITY DETAILS**  

in Window, the chrome can "drag and drop download" [0]  

it is asynchronously executed on UI thread [1][2]. the DragDownloadFile object have raw DragDownloadFileUI pointer.  

it is safe because DragDownloadFileUI is deleted on UI thread using PostTask[3].  

but DragDownloadFileUI have raw WebContents pointer.[4]. it can be freed before executing "drag and drop download"[2].  

and WebContents pointer is used on it [5]. so can trigger UAF

[0] : <https://source.chromium.org/chromium/chromium/src/+/master:content/browser/web_contents/web_contents_view_aura.cc;drc=6cdb24a4ce9d4151035c1f133833137d2e2881d1;l=244>  

[1] : <https://source.chromium.org/chromium/chromium/src/+/master:ui/base/dragdrop/os_exchange_data_provider_win.cc;drc=6f2046bedac15dc31e1cdf9a5e4a5eadd46231ae;l=928>  

[2] : <https://source.chromium.org/chromium/chromium/src/+/master:content/browser/download/drag_download_file.cc;drc=6cdb24a4ce9d4151035c1f133833137d2e2881d1;l=216>  

[3] : <https://source.chromium.org/chromium/chromium/src/+/master:content/browser/download/drag_download_file.cc;drc=6cdb24a4ce9d4151035c1f133833137d2e2881d1;l=199>  

[4] : <https://source.chromium.org/chromium/chromium/src/+/master:content/browser/download/drag_download_file.cc;drc=6cdb24a4ce9d4151035c1f133833137d2e2881d1;l=168>  

[5] : <https://source.chromium.org/chromium/chromium/src/+/master:content/browser/download/drag_download_file.cc;drc=6cdb24a4ce9d4151035c1f133833137d2e2881d1;l=82>  

**VERSION**  

Chrome Version: latest chrome  

Operating System: only Window

**REPRODUCTION CASE**

apply patch.diff to simulate a compromised renderer  

navigate index.html and touch page

once touch the page, your cursor is changed to drag the cursor.  

and drop to the desktop using right-click.(slowly click to move/copy here) it will be crashed

plz see video

**CREDIT INFORMATION**

Reporter credit: Woojin Oh of STEALIEN(@pwn\_exploit)

## Attachments

- [patch.txt](attachments/patch.txt) (text/plain, 18.9 KB)
- [bandicam 2021-01-29 19-56-47-218.mp4](attachments/bandicam 2021-01-29 19-56-47-218.mp4) (video/mp4, 8.3 MB)
- [index.html](attachments/index.html) (text/plain, 91 B)

## Timeline

### [Deleted User] (2021-01-29)

[Empty comment from Monorail migration]

### rs...@chromium.org (2021-01-29)

Thanks for the report and detailed analysis! Adding some labels while I work to reproduce. CC'ing a few folks though, since you're right that a raw WebContents* does raise some eyebrows.

[Monorail components: Blink>DataTransfer UI>Browser>Downloads]

### qi...@chromium.org (2021-01-29)

Thanks for reporting this.  Looks like the easiest fix is to pass a RenderViewHost Id to DragDownloadFileUI, and use it to retrieve the WebContents if needed.


### rs...@chromium.org (2021-01-30)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-30)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rs...@chromium.org (2021-02-01)

qinmin: I'm having some trouble with the bisect, but on source inspection, as far as I can tell, this pattern goes to at least Stable. If I've misdiagnosed, feel free to shout at me (especially if/when sheriffbot gets shouty).

### [Deleted User] (2021-02-02)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-02-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/99dc876a13df19f3512bcfb97e794ab5d1b28905

commit 99dc876a13df19f3512bcfb97e794ab5d1b28905
Author: Min Qin <qinmin@chromium.org>
Date: Tue Feb 02 19:06:51 2021

Stop using raw WebContents ptr in DragDownloadFile

BUG=1172192

Change-Id: Ie029713553ff88c1e271db1c84396e1ddda19286
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2666189
Reviewed-by: Xing Liu <xingliu@chromium.org>
Commit-Queue: Min Qin <qinmin@chromium.org>
Cr-Commit-Position: refs/heads/master@{#849692}

[modify] https://crrev.com/99dc876a13df19f3512bcfb97e794ab5d1b28905/content/browser/download/drag_download_file_browsertest.cc
[modify] https://crrev.com/99dc876a13df19f3512bcfb97e794ab5d1b28905/content/browser/download/drag_download_file.cc


### qi...@chromium.org (2021-02-02)

[Empty comment from Monorail migration]

### [Deleted User] (2021-02-03)

[Empty comment from Monorail migration]

### [Deleted User] (2021-02-03)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-02-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/3eda2771096d422aa90adfe8297f470df797bd5e

commit 3eda2771096d422aa90adfe8297f470df797bd5e
Author: Min Qin <qinmin@chromium.org>
Date: Wed Feb 03 19:14:01 2021

Add a method to disable download from starting a foreground service if
activities are invisible

This CL adds a method in AppHooks to make us not start a new foreground
service if Chrome activities are not visible. If a foreground service is
already started, the new notification updates will still use the existing
foreground serviec to change notification Ids if necessary.

BUG=1172192

Change-Id: I9d9ee74ed3e84597850ccb935c01851968dbab10
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2667777
Reviewed-by: David Trainor <dtrainor@chromium.org>
Commit-Queue: Min Qin <qinmin@chromium.org>
Cr-Commit-Position: refs/heads/master@{#850218}

[modify] https://crrev.com/3eda2771096d422aa90adfe8297f470df797bd5e/chrome/android/java/src/org/chromium/chrome/browser/download/DownloadForegroundServiceManager.java
[modify] https://crrev.com/3eda2771096d422aa90adfe8297f470df797bd5e/chrome/android/java/src/org/chromium/chrome/browser/AppHooks.java
[modify] https://crrev.com/3eda2771096d422aa90adfe8297f470df797bd5e/chrome/android/java/src/org/chromium/chrome/browser/download/DownloadNotificationService.java


### [Deleted User] (2021-02-03)

Requesting merge to stable M88 because latest trunk commit (850218) appears to be after stable branch point (827102).

Requesting merge to beta M89 because latest trunk commit (850218) appears to be after beta branch point (843830).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### qi...@chromium.org (2021-02-03)

The 2nd CL has a wrong bug number,  should be only the first CL.

### [Deleted User] (2021-02-04)

This bug requires manual review: M89's targeted beta branch promotion date has already passed, so this requires manual review
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
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
Owners: benmason@(Android), bindusuvarna@(iOS), geohsu@(ChromeOS), pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pb...@google.com (2021-02-08)

qinmin@ request to provide answers to questions from https://crbug.com/chromium/1172192#c15

### qi...@chromium.org (2021-02-08)

1. yes
2. https://chromium-review.googlesource.com/c/chromium/src/+/2666189
3.yes
4. Yes for M89
5. Fix a UAF security issue
6. No

### ad...@google.com (2021-02-09)

Approving merge to M89, branch 4389.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-02-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/1ebd5af895d8231ff103b672f9c9e8d60ee62d68

commit 1ebd5af895d8231ff103b672f9c9e8d60ee62d68
Author: Min Qin <qinmin@chromium.org>
Date: Tue Feb 09 22:05:21 2021

Stop using raw WebContents ptr in DragDownloadFile

BUG=1172192

(cherry picked from commit 99dc876a13df19f3512bcfb97e794ab5d1b28905)

Change-Id: Ie029713553ff88c1e271db1c84396e1ddda19286
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2666189
Reviewed-by: Xing Liu <xingliu@chromium.org>
Commit-Queue: Min Qin <qinmin@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#849692}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2683515
Cr-Commit-Position: refs/branch-heads/4389@{#868}
Cr-Branched-From: 9251c5db2b6d5a59fe4eac7aafa5fed37c139bb7-refs/heads/master@{#843830}

[modify] https://crrev.com/1ebd5af895d8231ff103b672f9c9e8d60ee62d68/content/browser/download/drag_download_file_browsertest.cc
[modify] https://crrev.com/1ebd5af895d8231ff103b672f9c9e8d60ee62d68/content/browser/download/drag_download_file.cc


### am...@google.com (2021-02-10)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@chromium.org (2021-02-10)

Approving merge to M88, branch 4324. Please merge by the end of Thursday PST to get into next Tuesday's release.

### am...@google.com (2021-02-10)

Congratulations, Woojin Oh! The VRP Panel has decided to award you $20,000 for this report. Excellent work and thank you for your efforts! 

### am...@google.com (2021-02-11)

[Empty comment from Monorail migration]

### sr...@google.com (2021-02-11)

Please help complete the merge before friday (Feb 12) - 12pm PST, 

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-02-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/3a6f6fbfd8fa87c10a255c56501446bec1ccc3dc

commit 3a6f6fbfd8fa87c10a255c56501446bec1ccc3dc
Author: Min Qin <qinmin@chromium.org>
Date: Fri Feb 12 22:45:08 2021

Stop using raw WebContents ptr in DragDownloadFile

BUG=1172192

(cherry picked from commit 99dc876a13df19f3512bcfb97e794ab5d1b28905)

Change-Id: Ie029713553ff88c1e271db1c84396e1ddda19286
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2666189
Reviewed-by: Xing Liu <xingliu@chromium.org>
Commit-Queue: Min Qin <qinmin@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#849692}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2692927
Reviewed-by: Shakti Sahu <shaktisahu@chromium.org>
Cr-Commit-Position: refs/branch-heads/4324@{#2200}
Cr-Branched-From: c73b5a651d37a6c4d0b8e3262cc4015a5579c6c8-refs/heads/master@{#827102}

[modify] https://crrev.com/3a6f6fbfd8fa87c10a255c56501446bec1ccc3dc/content/browser/download/drag_download_file_browsertest.cc
[modify] https://crrev.com/3a6f6fbfd8fa87c10a255c56501446bec1ccc3dc/content/browser/download/drag_download_file.cc


### ad...@google.com (2021-02-13)

[Empty comment from Monorail migration]

### ac...@chromium.org (2021-02-19)

[Empty comment from Monorail migration]

### am...@google.com (2021-02-22)

[Empty comment from Monorail migration]

### am...@google.com (2021-02-22)

[Empty comment from Monorail migration]

### go...@chromium.org (2021-02-23)

[Empty comment from Monorail migration]

### as...@google.com (2021-04-22)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-12)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2021-05-12)

Hello! We consider attachments/pocs included with reports to be an integral part of the report, so I've un-deleted them. Thanks!

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1172192?no_tracker_redirect=1

[Multiple monorail components: Blink>DataTransfer, UI>Browser>Downloads]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40054619)*
