# Incorrect security UI at screen share API

| Field | Value |
|-------|-------|
| **Issue ID** | [40053536](https://issues.chromium.org/issues/40053536) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Unknown |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | zy...@gmail.com |
| **Assignee** | ag...@chromium.org |
| **Created** | 2020-10-09 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36

Steps to reproduce the problem:
1.open the attchment poc2.html at 'http://127.0.0.1/poc2.html'
2.click button `Start capture`
3.`www.google.com` will ask to share your screen!

What is the expected behavior?
blob:http://127.0.0.1/ ask to share screen not www.google.com

What went wrong?
Wrong behaviour for overlong domains

Did this work before? N/A 

Chrome version: Version 87.0.4277.0 (Official Build) canary (x86_64)  Channel: canary
OS Version: OS X 10.15.1
Flash Version:

## Attachments

- [poc2.html](attachments/poc2.html) (text/plain, 2.6 KB)
- [截屏2020-10-09上午11.00.39.png](attachments/截屏2020-10-09上午11.00.39.png) (image/png, 450.6 KB)
- [poc.html](attachments/poc.html) (text/plain, 2.4 KB)
- [record.gif](attachments/record.gif) (image/gif, 4.3 MB)

## Timeline

### me...@chromium.org (2020-10-09)

Thanks for the report.

tommi: Could you PTAL and reassign if necessary?

[Monorail components: Blink>GetUserMedia>Desktop]

### [Deleted User] (2020-10-09)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-10-09)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### to...@chromium.org (2020-10-11)

Stefan - can someone on your team take a look?

### ho...@chromium.org (2020-10-12)

[Empty comment from Monorail migration]

### ag...@chromium.org (2020-10-12)

[Empty comment from Monorail migration]

### ag...@chromium.org (2020-10-12)

[Empty comment from Monorail migration]

### zy...@gmail.com (2020-10-19)

hello,any update here?

### ag...@chromium.org (2020-10-19)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-10-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/1bb44f9919224d826a4fb594342389d35160d28f

commit 1bb44f9919224d826a4fb594342389d35160d28f
Author: Palak Agarwal <agpalak@chromium.org>
Date: Thu Oct 22 13:49:58 2020

Passing Origin instead of URL as the app_name for the picker params

Change-Id: I5b7ee18f7f497d787998bde8408d46987a45a6eb
Bug: 1136714
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2463833
Commit-Queue: Palak Agarwal <agpalak@chromium.org>
Reviewed-by: Guido Urdaneta <guidou@chromium.org>
Cr-Commit-Position: refs/heads/master@{#819813}

[modify] https://crrev.com/1bb44f9919224d826a4fb594342389d35160d28f/chrome/browser/media/webrtc/display_media_access_handler.cc
[modify] https://crrev.com/1bb44f9919224d826a4fb594342389d35160d28f/chrome/browser/media/webrtc/display_media_access_handler_unittest.cc
[modify] https://crrev.com/1bb44f9919224d826a4fb594342389d35160d28f/chrome/browser/media/webrtc/fake_desktop_media_picker_factory.cc
[modify] https://crrev.com/1bb44f9919224d826a4fb594342389d35160d28f/chrome/browser/media/webrtc/fake_desktop_media_picker_factory.h


### ag...@chromium.org (2020-10-23)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-23)

[Empty comment from Monorail migration]

### gu...@chromium.org (2020-10-26)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-26)

This bug requires manual review: M87's targeted beta branch promotion date has already passed, so this requires manual review
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
Owners: benmason@(Android), bindusuvarna @(iOS), cindyb@(ChromeOS), lakpamarthy@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gu...@chromium.org (2020-10-26)

1. Does your merge fit within the Merge Decision Guidelines?
Yes. Security issue.

2. Links to the CLs you are requesting to merge.
r 819813

3. Has the change landed and been verified on ToT?
Yes.

4. Does this change need to be merged into other active release branches (M-1, M+1)?
We should consider merging to 86.

5. Why are these changes required in this milestone after branch?
The change fixes a security issue where a malicious site can mislead users making them believe that a trustworthy site is the one requesting to share the screen.

6. Is this a new feature?
No.

7. If it is a new feature, is it behind a flag using finch?
N/A

### zy...@gmail.com (2020-10-26)

I think this UI spoofing has a high credibility, if the described web page inner dialog has the function of remote assistance, such as teamviewer.com, victims have a high possibility of agreeing to share the screen, once you get the user screen, you may disclose the user's privacy password and other information, so I think the severity of this vulnerability can be improved.

### gu...@chromium.org (2020-10-26)

zyzengstorm@: We have verified the fix locally using Canary. Can you verify it on your end as well?

### ad...@google.com (2020-10-26)

[Empty comment from Monorail migration]

### la...@google.com (2020-10-26)

merge approved for M87 branch 4280

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-10-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/8cc873e0390c8782128c904e064de3fa50998b5f

commit 8cc873e0390c8782128c904e064de3fa50998b5f
Author: Palak Agarwal <agpalak@chromium.org>
Date: Mon Oct 26 22:09:36 2020

Passing Origin instead of URL as the app_name for the picker params

(cherry picked from commit 1bb44f9919224d826a4fb594342389d35160d28f)

Change-Id: I5b7ee18f7f497d787998bde8408d46987a45a6eb
Bug: 1136714
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2463833
Commit-Queue: Palak Agarwal <agpalak@chromium.org>
Reviewed-by: Guido Urdaneta <guidou@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#819813}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2499542
Commit-Queue: Guido Urdaneta <guidou@chromium.org>
Cr-Commit-Position: refs/branch-heads/4280@{#785}
Cr-Branched-From: ea420fb963f9658c9969b6513c56b8f47efa1a2a-refs/heads/master@{#812852}

[modify] https://crrev.com/8cc873e0390c8782128c904e064de3fa50998b5f/chrome/browser/media/webrtc/display_media_access_handler.cc
[modify] https://crrev.com/8cc873e0390c8782128c904e064de3fa50998b5f/chrome/browser/media/webrtc/display_media_access_handler_unittest.cc
[modify] https://crrev.com/8cc873e0390c8782128c904e064de3fa50998b5f/chrome/browser/media/webrtc/fake_desktop_media_picker_factory.cc
[modify] https://crrev.com/8cc873e0390c8782128c904e064de3fa50998b5f/chrome/browser/media/webrtc/fake_desktop_media_picker_factory.h


### zy...@gmail.com (2020-10-27)

Re #17:

Yeah, I can confirm it has been fixed.

### ad...@google.com (2020-10-28)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-10-28)

Congratulations, the VRP panel has decided to award $500 for this report.

### gu...@chromium.org (2020-10-29)

[Empty comment from Monorail migration]

### zy...@gmail.com (2020-10-29)

Re #23:
Hi, I think this case is much more easier than 1080934 and 754304 to exploit, it also has an ultra-high credibility, why only reward this case only $500?

### ad...@google.com (2020-10-29)

Thanks for the links to related bugs. We'll discuss it again at the panel next week.

### zy...@gmail.com (2020-10-30)

Thanks! Please see this exploit video, I think this bug's severity is higher than a lot of other $1000/2000... spoof cases, so I think the reward is lower than expected.

### ad...@google.com (2020-10-30)

I'm going to reject merge to M86. It's right on the cusp. It's medium severity; the fix is simple but not trivial. It's very important that the next M86 release goes out without a hitch, and M87 is coming along very soon, so this fix can wait for M87.

### [Deleted User] (2020-10-30)

[Empty comment from Monorail migration]

### ad...@google.com (2020-11-04)

zyzengstorm@ thank you for bringing the other bugs to our attention. The VRP panel again discussed this bug and considered the bugs in https://crbug.com/chromium/1136714#c25 and and the extra information in https://crbug.com/chromium/1136714#c27, and they have chosen not to alter the reward amount.

### zy...@gmail.com (2020-11-05)

Alright, I just think this is a very deceptive vulnerability.


### ad...@google.com (2020-11-05)

[Empty comment from Monorail migration]

### zy...@gmail.com (2020-11-09)

Hi @adetaylor, please just credit to wester0x01(https://twitter.com/wester0x01) for this bug, thanks!


### ad...@google.com (2020-11-16)

[Empty comment from Monorail migration]

### ad...@google.com (2020-11-16)

[Empty comment from Monorail migration]

### vs...@google.com (2020-12-10)

[Empty comment from Monorail migration]

### vs...@google.com (2020-12-10)

[Empty comment from Monorail migration]

### [Deleted User] (2020-12-10)

[Empty comment from Monorail migration]

### ke...@google.com (2020-12-11)

[Empty comment from Monorail migration]

### [Deleted User] (2020-12-14)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gu...@chromium.org (2020-12-14)

How does one merge to 86-LTS?

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-12-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/e23e35d9a89918509f7eb3c577173f20c8e539ed

commit e23e35d9a89918509f7eb3c577173f20c8e539ed
Author: Palak Agarwal <agpalak@chromium.org>
Date: Wed Dec 16 18:39:29 2020

Passing Origin instead of URL as the app_name for the picker params

(cherry picked from commit 1bb44f9919224d826a4fb594342389d35160d28f)

(cherry picked from commit 8cc873e0390c8782128c904e064de3fa50998b5f)

Change-Id: I5b7ee18f7f497d787998bde8408d46987a45a6eb
Bug: 1136714
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2463833
Commit-Queue: Palak Agarwal <agpalak@chromium.org>
Reviewed-by: Guido Urdaneta <guidou@chromium.org>
Cr-Original-Original-Commit-Position: refs/heads/master@{#819813}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2499542
Commit-Queue: Guido Urdaneta <guidou@chromium.org>
Cr-Original-Commit-Position: refs/branch-heads/4280@{#785}
Cr-Original-Branched-From: ea420fb963f9658c9969b6513c56b8f47efa1a2a-refs/heads/master@{#812852}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2585093
Reviewed-by: Achuith Bhandarkar <achuith@chromium.org>
Commit-Queue: Victor-Gabriel Savu <vsavu@google.com>
Cr-Commit-Position: refs/branch-heads/4240@{#1486}
Cr-Branched-From: f297677702651916bbf65e59c0d4bbd4ce57d1ee-refs/heads/master@{#800218}

[modify] https://crrev.com/e23e35d9a89918509f7eb3c577173f20c8e539ed/chrome/browser/media/webrtc/fake_desktop_media_picker_factory.cc
[modify] https://crrev.com/e23e35d9a89918509f7eb3c577173f20c8e539ed/chrome/browser/media/webrtc/display_media_access_handler_unittest.cc
[modify] https://crrev.com/e23e35d9a89918509f7eb3c577173f20c8e539ed/chrome/browser/media/webrtc/fake_desktop_media_picker_factory.h
[modify] https://crrev.com/e23e35d9a89918509f7eb3c577173f20c8e539ed/chrome/browser/media/webrtc/display_media_access_handler.cc


### [Deleted User] (2020-12-18)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2021-01-07)

[Empty comment from Monorail migration]

### ja...@google.com (2021-01-19)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-29)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1136714?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40053536)*
