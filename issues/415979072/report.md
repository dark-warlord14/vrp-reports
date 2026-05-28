# Save As file dialog steal focus behind the PictureinPictureAPI save malicious file at arbitrary path

| Field | Value |
|-------|-------|
| **Issue ID** | [415979072](https://issues.chromium.org/issues/415979072) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Media>PictureInPicture |
| **Platforms** | Linux, Windows, ChromeOS |
| **Chrome Version** | 132.0.6834.46  |
| **Reporter** | pu...@gmail.com |
| **Assignee** | st...@chromium.org |
| **Created** | 2025-05-06 |
| **Bounty** | $1,000.00 |

## Description

# Steps to reproduce the problem

1. Host the provided HTML file.
2. Open the link in Chrome Browser.
3. Click the "Treasure Box" button and move the box to the center of the screen.
4. Click the "Choose a folder to save the reward" button and select a folder.
5. After selecting the folder, press the Tab key, then press the Enter key repeatedly to claim the reward. However, unbeknownst to the victim, all files in the selected folder will be deleted.

# Problem Description

In Chrome Browser, the Picture-in-Picture (PiP) layer can be exploited by an attacker to cover permission prompts that are required when a user selects a folder to save a file. In this scenario, the victim is asked to move the treasure chest (PiP video) over the screen, then select a folder to save the file (the prize). After selecting the folder, the victim is instructed to press the Tab key and then the Enter key repeatedly to claim the prize. However, unbeknownst to the victim, all files in the selected folder will be deleted.

**Recommendations**:

- Ensure that Picture-in-Picture cannot cover important permissions that need to be seen by the user, or if a permission is covered by PiP, that permission should not be executable because it is covered.

# Summary

Mass File Deletion Without User Awareness in chrome

# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: N/A

## Attachments

- [2025-05-07 04-12-58.mp4](attachments/2025-05-07 04-12-58.mp4) (video/mp4, 1.2 MB)
- [Poc.html](attachments/Poc.html) (text/html, 5.3 KB)

## Timeline

### xi...@chromium.org (2025-05-06)

Thanks for the report. It seems that the issue was reported in https://crbug.com/40076120 and fixed in https://crrev.com/c/5753110. However, it was reverted recently due to breakage https://crrev.com/c/6318768. Adding the original owner while the team is exploring a different approach.

### ch...@google.com (2025-05-07)

Setting milestone because of s2 severity.

### ch...@google.com (2025-05-07)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ki...@gmail.com (2025-05-13)

any update?

### ch...@google.com (2025-05-21)

steimel: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ki...@gmail.com (2025-05-24)

any update?

### st...@chromium.org (2025-05-29)

There's a CL I'm working on for another bug that should also fix this if I'm understanding the poc correctly. Note that I can't seem to get the poc to work locally (tried both as a file and hosting it on an https server)

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

### ki...@gmail.com (2025-06-16)

Hi team, thank you for accepting the issue. Just wanted to kindly ask if there’s any update regarding the reward eligibility or expected timeline. Much appreciated!


### st...@chromium.org (2025-06-16)

The CL that fixed it (in comment 10) is in 139.0.7232.0

### pg...@google.com (2025-06-16)

handling merges in issue 384050903 - removing merge labels from here

... there were no merge labels but i got way ahead. consider this a note to my future self lol

### am...@chromium.org (2025-06-18)

This issue was resolved as part of a fix for the general root cause of PiP window placement when file dialogs are engaged. The other reports are slightly different outcomes, but all issues have a single root cause.
In reviewing this issue in relation to those, there is a lot of UI engagement, with the start of it requiring the user to place the PIP window in a specific place that would allow for themselves to be owned. There are also a lot of subsequent UI interaction to the degree that this seems to be a scenario that would be unlikely to result in exploitation in real world conditions. The preconditions for this issue do not align with what we would consider "reasonable and prudent" interactions for a user. Please see our FAQ on this topic for more information. [1]
I've, therefore, converted this to a functional bug. Now that it is resolved, we will still review it at a forthcoming VRP panel session, but I do want to level set expectations that bugs of this kind are not generally eligible for VRP rewards.

[1] <https://chromium.googlesource.com/chromium/src/+/main/docs/security/faq.md#What-makes-a-UI-spoof-interesting-to-report>

### ki...@gmail.com (2025-06-25)

any update?

### am...@chromium.org (2025-06-25)

Thank you for the report. As conveyed in c#14, given the significant and specific preconditions for user interaction required for the outcome of this bug, this does not meet the conditions to be considered a security issue and concurred with in VRP Panel review today. Therefore, this report is unfortunately not eligible for a Chrome VRP reward.

### ki...@gmail.com (2025-06-25)

:(

### ch...@google.com (2025-09-23)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/415979072)*
