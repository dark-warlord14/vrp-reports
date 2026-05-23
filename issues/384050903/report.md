# Save As file dialog steal focus behind the PictureinPictureAPI save malicious file at arbitrary path

| Field | Value |
|-------|-------|
| **Issue ID** | [384050903](https://issues.chromium.org/issues/384050903) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Media>PictureInPicture |
| **Platforms** | Linux, Windows, ChromeOS |
| **Chrome Version** | 132.0.6834.46  |
| **Reporter** | pu...@gmail.com |
| **Assignee** | st...@chromium.org |
| **Created** | 2024-12-14 |
| **Bounty** | $1,000.00 |

## Description

# Steps to reproduce the problem

`Enable Ask where to save each file before downloading in Downloads`

1. Open the poc.html file in the browser
2. Click the button
3. Click on Start file writing button
4. Press the keys ctrl + v and keypress Enter key
   A file will be written

# Problem Description

Save as file dialog can steal focus behind the Picture-in-Picture API and can save malicious at arbitrary file path it is possible only if a user has enabled Ask where to save each file before downloading in Downloads

it is possible to saving malicious file at an arbitrary file path. the save as file dialog stays behind the PiP window, completely obscured. Since the dialog still receives focus, it's possible to trick the user into saving malicious file at any path

# Additional Comments

Google Chrome 132.0.6834.46 (Official Build) beta (64-bit) (cohort: Beta)
Revision c2f4d240db159da353deb230fea74b6a2f32533b-refs/branch-heads/6834@{#1946}
OS Windows 10 Version 22H2 (Build 19045.5131)

# Summary

Save As file dialog steal focus behind the PictureinPictureAPI save malicious file at arbitrary path

# Custom Questions

#### Reporter credit:

Puf

# Additional Data

Category: Security   

Chrome Channel: Beta   

Regression: N/A

## Attachments

- [repro.mp4](attachments/repro.mp4) (video/mp4, 296.3 KB)
- deleted (application/octet-stream, 0 B)

## Timeline

### pu...@gmail.com (2024-12-14)

if a User has *Enabled Ask where to save each file before downloading* in Downloads

The Attacker can take advantage of this feature with PIP Window can trick user into saving malicious file at arbitrary path

### pu...@gmail.com (2024-12-14)

`For Ref:` <https://issues.chromium.org/issues/40076120>

<https://chromium-review.googlesource.com/c/chromium/src/+/5981649>

### pu...@gmail.com (2024-12-14)

`POC File:`

### an...@chromium.org (2024-12-14)

[security shepherd]: Thanks for the report. Assigning this to [steimel@chromium.org](mailto:steimel@chromium.org) and assigning the main component to PictureInPicture. This is reproducible and it does look like PIP can hide the frame underneath.

Reference bug as mentioned in [comment #3](https://issues.chromium.org/issues/384050903#comment3) is <https://issues.chromium.org/issues/40076120>.

### pe...@google.com (2024-12-15)

Setting milestone because of s2 severity.

### pe...@google.com (2024-12-15)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security Impact hotlist or the Severity field, and remove the ReleaseBlock hotlist.

### pe...@google.com (2024-12-15)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### pe...@google.com (2024-12-29)

steimel: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### pe...@google.com (2025-01-01)

This issue appears to be blocking an upcoming release and is therefore an **Urgent Release Blocking Issue** as per <http://go/chrome-slo#release-blocking-issues>. Bumping the priority to P0 to better reflect the urgency.

If this is not a release blocking issue, please adjust the release block field. Adjusting the priority will have no affect, P0 will be re-applied whilever this is marked as a release blocking issue.

### am...@chromium.org (2025-01-06)

This is not a recently introduced regression and should not be considered a release blocker for 132; updating accordingly

### pe...@google.com (2025-01-13)

steimel: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### pu...@gmail.com (2025-03-18)

Friendly Ping :) Thanks

any update on this issue

### pu...@gmail.com (2025-05-14)

Hello, just a gentle reminder to keep this Issue on track!
Thank you

### st...@chromium.org (2025-05-29)

This should be fixed by a CL I have inflight. Hoping to land it next week once one of the reviewers is back from OOO

### st...@chromium.org (2025-06-09)

Update: The CL required some refactoring for an edge case I hadn't considered. That is done so now awaiting review again

### dx...@google.com (2025-06-10)

Project: chromium/src  

Branch: main  

Author: Tommy Steimel [steimel@chromium.org](mailto:steimel@chromium.org)  

Link:      <https://chromium-review.googlesource.com/6449682>

[pip] Tuck picture-in-picture windows when a file dialog is open

---


Expand for full commit details
```
     
    Picture-in-picture windows can occlude file dialogs, and initially we 
    tried to prevent this by closing all pip windows whenever a file 
    dialog was open. This created its own set of problems, so that feature 
    was disabled. 
     
    This is a replacement of that feature: instead of closing pip windows, 
    this moves them off to the side of the screen, preventing them from 
    obscuring the file dialog without having to actually close them. 
     
    go/picture-in-picture-tucking-design-doc 
     
    Bug: 403792431, 384050903, 415979072 
    Change-Id: I280333c32a02aee3c345c839e88848de6820ebe2 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6449682 
    Reviewed-by: Evan Liu <evliu@google.com> 
    Commit-Queue: Tommy Steimel <steimel@chromium.org> 
    Reviewed-by: Frank Liberato <liberato@chromium.org> 
    Reviewed-by: Fr <beaufort.francois@gmail.com> 
    Cr-Commit-Position: refs/heads/main@{#1471975}

```

---

Files:

- M `chrome/browser/file_select_helper.cc`
- M `chrome/browser/file_select_helper.h`
- M `chrome/browser/picture_in_picture/BUILD.gn`
- A `chrome/browser/picture_in_picture/picture_in_picture_window.h`
- M `chrome/browser/picture_in_picture/picture_in_picture_window_manager.cc`
- M `chrome/browser/picture_in_picture/picture_in_picture_window_manager.h`
- M `chrome/browser/picture_in_picture/picture_in_picture_window_manager_unittest.cc`
- A `chrome/browser/picture_in_picture/scoped_tuck_picture_in_picture.cc`
- A `chrome/browser/picture_in_picture/scoped_tuck_picture_in_picture.h`
- M `chrome/browser/ui/BUILD.gn`
- M `chrome/browser/ui/views/frame/picture_in_picture_browser_frame_view.cc`
- M `chrome/browser/ui/views/frame/picture_in_picture_browser_frame_view.h`
- M `chrome/browser/ui/views/overlay/video_overlay_window_views.cc`
- M `chrome/browser/ui/views/overlay/video_overlay_window_views.h`
- M `chrome/browser/ui/views/overlay/video_overlay_window_views_unittest.cc`
- A `chrome/browser/ui/views/picture_in_picture/OWNERS`
- A `chrome/browser/ui/views/picture_in_picture/README.md`
- A `chrome/browser/ui/views/picture_in_picture/picture_in_picture_tucker.cc`
- A `chrome/browser/ui/views/picture_in_picture/picture_in_picture_tucker.h`
- A `chrome/browser/ui/views/picture_in_picture/picture_in_picture_tucker_unittest.cc`
- M `chrome/test/BUILD.gn`
- M `media/base/media_switches.cc`
- M `media/base/media_switches.h`
- M `tools/metrics/histograms/metadata/media/enums.xml`
- M `tools/metrics/histograms/metadata/media/histograms.xml`

---

Hash: 923d0eca9ed86960af9e735f8a4b2271fa17fb37  

Date:  Tue Jun 10 18:52:42 2025


---

### st...@chromium.org (2025-06-16)

Fix landed in 139.0.7232.0

### am...@chromium.org (2025-06-18)

The reporter of the duplicate issue has reported this issue as not yet resolved.

### sp...@google.com (2025-07-02)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
report of lower impact web platform privilege escalation / UI spoof 


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-07-02)

Thank you for your efforts and reporting this issue to us.

### pu...@gmail.com (2025-07-03)

Thank you so much amy.

### pg...@google.com (2025-08-05)

(Updating OS as I do not believe this is a Windows specific issue)

### ch...@google.com (2025-10-02)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> report of lower impact web platform privilege escalation / UI spoof

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/384050903)*
