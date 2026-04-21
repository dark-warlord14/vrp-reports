# Security: UAF in DesktopCapture

| Field | Value |
|-------|-------|
| **Issue ID** | [40054952](https://issues.chromium.org/issues/40054952) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>GetUserMedia |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | le...@gmail.com |
| **Assignee** | ag...@chromium.org |
| **Created** | 2021-02-23 |
| **Bounty** | $20,000.00 |

## Description

**VULNERABILITY DETAILS**  

When the browser processes the ScreenCaptureAccess request, it will show a QuestionMessageBox[1]. The MessageBox will run a nested message loop[2] to continue running the UI thread. If the web content or other related instances are destroyed, the UAF will be triggered after the nested message loops exit.

[1]. <https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/media/webrtc/desktop_capture_access_handler.cc;l=222;drc=6bd941b67ab326925457b4e8ff05d79f8b9a7489>  

[2]. <https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/ui/views/message_box_dialog.cc;l=85;drc=28a5ac480de97fe18bcd55d11bfa06e68d6e808e>

**VERSION**  

Chrome Version: stable  

Operating System: Linux, Windows, ChromeOS

**REPRODUCTION CASE**

$ python ./copy\_mojo\_js\_bindings.py /path/to/chrome/.../out/asan/gen  

$ python -m SimpleHTTPServer  

$ out/asan/chrome --user-data-dir=/tmp/xxxx --enable-blink-features=MojoJS --enable-usermedia-screen-capturing "<http://localhost:8000/poc.html>" "about:blank"  

Click the trigger button, and click yes after the page "poc.html" is closed.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: browser  

Crash State: see asan file

**CREDIT INFORMATION**  

Reporter credit: Leecraso and Guang Gong of 360 Alpha Lab

## Attachments

- [asan](attachments/asan) (text/plain, 21.0 KB)
- [poc.html](attachments/poc.html) (text/plain, 1.5 KB)
- [copy_mojo_js_bindings.py](attachments/copy_mojo_js_bindings.py) (text/plain, 514 B)

## Timeline

### [Deleted User] (2021-02-23)

[Empty comment from Monorail migration]

### me...@chromium.org (2021-02-24)

Thanks for this report. I was able to reproduce this.
guidou@ Could you please take a look?

### [Deleted User] (2021-02-24)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### do...@chromium.org (2021-03-02)

Friendly security sheriff ping here.

[Monorail components: Blink>GetUserMedia]

### gu...@chromium.org (2021-03-03)

[Empty comment from Monorail migration]

### gu...@chromium.org (2021-03-03)

This requires the --enable-usermedia-screen-capturing flag, so maybe we can adjust the Security_Impact-Stable.

### [Deleted User] (2021-03-03)

[Empty comment from Monorail migration]

### le...@gmail.com (2021-03-08)

Hi guidou@: Yes, so do you have any plans to fix it recently?

### gu...@chromium.org (2021-03-08)

[Empty comment from Monorail migration]

### ag...@chromium.org (2021-03-09)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-11)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-03-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/a462be0883486431086c5f07cdafbd3607005a59

commit a462be0883486431086c5f07cdafbd3607005a59
Author: Palak Agarwal <agpalak@chromium.org>
Date: Wed Mar 17 17:22:38 2021

WebContents bug fix: Device capture only if web contents is valid

Bug: 1181228
Change-Id: I0a4c9718a3c0ccb52cefa4565b9787e6912554c9
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2752235
Reviewed-by: Guido Urdaneta <guidou@chromium.org>
Commit-Queue: Palak Agarwal <agpalak@chromium.org>
Cr-Commit-Position: refs/heads/master@{#863828}

[modify] https://crrev.com/a462be0883486431086c5f07cdafbd3607005a59/chrome/browser/media/webrtc/desktop_capture_access_handler.cc


### zh...@google.com (2021-03-17)

[Empty comment from Monorail migration]

### ag...@chromium.org (2021-03-18)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-18)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-18)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-18)

Requesting merge to stable M89 because latest trunk commit (863828) appears to be after stable branch point (843830).

Requesting merge to beta M90 because latest trunk commit (863828) appears to be after beta branch point (857950).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-03-18)

This bug requires manual review: M90's targeted beta branch promotion date has already passed, so this requires manual review
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
Owners: govind@(Android), bindusuvarna@(iOS), cindyb@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sr...@google.com (2021-03-18)

pls answer https://crbug.com/chromium/1181228#c18 for review 

### sr...@google.com (2021-03-22)

Friendly ping ^

### gu...@chromium.org (2021-03-22)

agpalak@ is OOO for a few days, so answering in her place.

1. Does your merge fit within the Merge Decision Guidelines?
Yes. Security fix.

2. Links to the CLs you are requesting to merge.
r 863828

3. Has the change landed and been verified on ToT?
Yes

4. Does this change need to be merged into other active release branches (M-1, M+1)?
Yes, preferably to M89 too. 

5. Why are these changes required in this milestone after branch?
Fix a UAF bug.

6. Is this a new feature?
No.

7. If it is a new feature, is it behind a flag using finch?
N/A

### ad...@google.com (2021-03-22)

Approving merge to M90. Please merge to branch 4430. I am likely to approve merge to M89 a few days before we make the next M89 refresh, to give maximum bake time.

### gi...@appspot.gserviceaccount.com (2021-03-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/75844cd2a26d288633646dddf1af988b63a49468

commit 75844cd2a26d288633646dddf1af988b63a49468
Author: Palak Agarwal <agpalak@chromium.org>
Date: Mon Mar 22 22:38:28 2021

WebContents bug fix: Device capture only if web contents is valid

(cherry picked from commit a462be0883486431086c5f07cdafbd3607005a59)

Bug: 1181228
Change-Id: I0a4c9718a3c0ccb52cefa4565b9787e6912554c9
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2752235
Reviewed-by: Guido Urdaneta <guidou@chromium.org>
Commit-Queue: Palak Agarwal <agpalak@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#863828}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2780252
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Commit-Queue: Guido Urdaneta <guidou@chromium.org>
Cr-Commit-Position: refs/branch-heads/4430@{#649}
Cr-Branched-From: e5ce7dc4f7518237b3d9bb93cccca35d25216cbe-refs/heads/master@{#857950}

[modify] https://crrev.com/75844cd2a26d288633646dddf1af988b63a49468/chrome/browser/media/webrtc/desktop_capture_access_handler.cc


### ad...@google.com (2021-03-23)

Approving merge to M89, branch 4389, as it looks like we're cutting the M89 refresh biuld a little sooner than I expected.

### gi...@appspot.gserviceaccount.com (2021-03-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/e6f11cafde08981e47ba77e71abf99a271f7a042

commit e6f11cafde08981e47ba77e71abf99a271f7a042
Author: Palak Agarwal <agpalak@chromium.org>
Date: Tue Mar 23 19:08:03 2021

WebContents bug fix: Device capture only if web contents is valid

(cherry picked from commit a462be0883486431086c5f07cdafbd3607005a59)

Bug: 1181228
Change-Id: I0a4c9718a3c0ccb52cefa4565b9787e6912554c9
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2752235
Reviewed-by: Guido Urdaneta <guidou@chromium.org>
Commit-Queue: Palak Agarwal <agpalak@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#863828}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2782122
Auto-Submit: Guido Urdaneta <guidou@chromium.org>
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/4389@{#1586}
Cr-Branched-From: 9251c5db2b6d5a59fe4eac7aafa5fed37c139bb7-refs/heads/master@{#843830}

[modify] https://crrev.com/e6f11cafde08981e47ba77e71abf99a271f7a042/chrome/browser/media/webrtc/desktop_capture_access_handler.cc


### am...@google.com (2021-03-24)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-03-24)

Congratulations, Leecraso and Guang Gong! The VRP Panel has decided to award you $20,000 for this report. Excellent work! 

### am...@google.com (2021-03-29)

[Empty comment from Monorail migration]

### ad...@google.com (2021-03-29)

[Empty comment from Monorail migration]

### am...@google.com (2021-03-29)

[Empty comment from Monorail migration]

### as...@google.com (2021-03-30)

[Empty comment from Monorail migration]

### su...@chromium.org (2021-03-30)

Merge approved for LTS-86

### gi...@appspot.gserviceaccount.com (2021-03-31)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/6a6361c9f31c11880bdd26cc0ea232da81c7b7d9

commit 6a6361c9f31c11880bdd26cc0ea232da81c7b7d9
Author: Palak Agarwal <agpalak@chromium.org>
Date: Wed Mar 31 16:10:26 2021

WebContents bug fix: Device capture only if web contents is valid

(cherry picked from commit a462be0883486431086c5f07cdafbd3607005a59)

(cherry picked from commit e6f11cafde08981e47ba77e71abf99a271f7a042)

Bug: 1181228
Change-Id: I0a4c9718a3c0ccb52cefa4565b9787e6912554c9
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2752235
Reviewed-by: Guido Urdaneta <guidou@chromium.org>
Commit-Queue: Palak Agarwal <agpalak@chromium.org>
Cr-Original-Original-Commit-Position: refs/heads/master@{#863828}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2782122
Auto-Submit: Guido Urdaneta <guidou@chromium.org>
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Original-Commit-Position: refs/branch-heads/4389@{#1586}
Cr-Original-Branched-From: 9251c5db2b6d5a59fe4eac7aafa5fed37c139bb7-refs/heads/master@{#843830}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2795101
Reviewed-by: Victor-Gabriel Savu <vsavu@google.com>
Reviewed-by: Artem Sumaneev <asumaneev@google.com>
Auto-Submit: Artem Sumaneev <asumaneev@google.com>
Commit-Queue: Guido Urdaneta <guidou@chromium.org>
Cr-Commit-Position: refs/branch-heads/4240@{#1585}
Cr-Branched-From: f297677702651916bbf65e59c0d4bbd4ce57d1ee-refs/heads/master@{#800218}

[modify] https://crrev.com/6a6361c9f31c11880bdd26cc0ea232da81c7b7d9/chrome/browser/media/webrtc/desktop_capture_access_handler.cc


### as...@google.com (2021-03-31)

[Empty comment from Monorail migration]

### am...@google.com (2021-04-09)

[Empty comment from Monorail migration]

### [Deleted User] (2021-07-07)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1181228?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40054952)*
