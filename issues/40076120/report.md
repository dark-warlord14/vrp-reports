# Security: Document Picture-in-Picture API can be used to spoof file reads and writes

| Field | Value |
|-------|-------|
| **Issue ID** | [40076120](https://issues.chromium.org/issues/40076120) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Media>PictureInPicture |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | re...@gmail.com |
| **Assignee** | st...@chromium.org |
| **Created** | 2023-11-02 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**  

The Document Picture-in-Picture API can be used to spawn an always on-top window that covers up anything behind it. When a file save/open dialog is opened from a PiP window, the dialog gets correctly displayed on top of it, but when a different browser window opens the file dialog it'll appear behind the PiP window.

By cleverly positioning a pop-up it is possible to force the file dialog to spawn behind the PiP window, completely obscured. Since the dialog still receives focus, it's possible to trick the user into saving or opening a file at an arbitrary file path.

In addition, the file write will appear to not open the downloads bubble since the bubble that does open is a part of the pop-up window that's completely obscured.

**VERSION**  

Chrome Version: 119.0.6045.106 Stable + Dev  

Operating System: Windows 10

**REPRODUCTION CASE**  

The repro currently assumes that you've set your downloads to ask the path every time - this could be worked around by using the File System API.  

The paths used are defined by the `fileWritePath` and `fileReadPath` variables respectively.

1. Open the poc.html file in the browser
2. Click the button
3. Choose whether you want to see a file read or write and press the corresponding button
4. Press the keys as instructed
5. A file will be read or written

I've also included a demo video showing both the read and the write repros.

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: Lyra Rebane (rebane2001)

## Attachments

- [demo.webm](attachments/demo.webm) (video/webm, 1.7 MB)
- [poc.html](attachments/poc.html) (text/plain, 2.2 KB)

## Timeline

### [Deleted User] (2023-11-02)

[Empty comment from Monorail migration]

### xi...@chromium.org (2023-11-02)

Thanks for the report. I think this is similar to https://crbug.com/1498673. Maybe we should bring the file picker prompt to the front when it is focused.

[Monorail components: Blink>Media>PictureInPicture]

### [Deleted User] (2023-11-02)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-03)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-11-03)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-11-17)

steimel: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### st...@chromium.org (2023-11-17)

I'm working on a general solution for this and other bugs that use a picture-in-picture window to hide important dialogs

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1498997?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-02-21)

steimel: Uh oh! This issue still open and hasn't been updated in the last 95 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### pg...@google.com (2024-05-24)

[secondary security shepherd]

hi [steimel@chromium.org](mailto:steimel@chromium.org)! you have many issues filed related to PIP so i wasnt sure which one was the right one - if there is a tracking bug for the general solution you mentioned in [comment #8](https://issues.chromium.org/issues/40076120#comment8) can you link it to this bug as a blocker? It would be good for folks to follow along (:

### st...@chromium.org (2024-05-24)

Sorry for the delay. Enough of the general solution is there to fix this issue, so I will do that now

### st...@chromium.org (2024-05-24)

WIP CL here: crrev.com/c/5570091. I need to discuss with file selection owners first though

### st...@chromium.org (2024-06-14)

+sky@chromium.org who is reviewing the CL

### ap...@google.com (2024-07-09)

Project: chromium/src
Branch: main

commit d03e39ce030958ca00fa1a6f06f4cf98c7fbd6b5
Author: Tommy Steimel <steimel@chromium.org>
Date:   Tue Jul 09 12:34:54 2024

    Add metrics to see when file dialogs and pip windows are both open
    
    This CL adds a new histogram that is recorded each time either a file
    dialog or picture-in-picture window opens. It records an enum to
    indicate whether file dialogs exist when a picture-in-picture window is
    opened and whether picture-in-picture windows exist when a file dialog
    is opened.
    
    Bug: 40076120
    Change-Id: Ic2039086c6e255f58a9c51efce0970865f59d1d2
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5671171
    Reviewed-by: Scott Violet <sky@chromium.org>
    Reviewed-by: Takashi Toyoshima <toyoshim@chromium.org>
    Commit-Queue: Tommy Steimel <steimel@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1324803}

M       chrome/browser/file_select_helper.cc
M       chrome/browser/file_select_helper.h
M       chrome/browser/picture_in_picture/picture_in_picture_window_manager.cc
M       chrome/browser/picture_in_picture/picture_in_picture_window_manager.h
M       tools/metrics/histograms/metadata/media/enums.xml
M       tools/metrics/histograms/metadata/media/histograms.xml

https://chromium-review.googlesource.com/5671171


### ap...@google.com (2024-09-05)

Project: chromium/src
Branch: main

commit 47617c1e9e6217aa03b889a8a3f1af44b4baa1ef
Author: Tommy Steimel <steimel@chromium.org>
Date:   Thu Sep 05 21:56:15 2024

    Close picture-in-picture windows when a file dialog is present
    
    This CL adds `ScopedDisallowPictureInPicture`, which can be used to
    close any existing picture-in-picture windows and prevent new ones from
    opening. This is used in the `FileSelectHelper` to prevent
    picture-in-picture windows from occluding file dialogs.
    
    Bug: 40076120
    Change-Id: I5b8eb02003370cf14d5968a39f62a13e925b112a
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5753110
    Commit-Queue: Tommy Steimel <steimel@chromium.org>
    Reviewed-by: Frank Liberato <liberato@chromium.org>
    Reviewed-by: Evan Liu <evliu@google.com>
    Reviewed-by: Scott Violet <sky@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1351716}

M       chrome/browser/BUILD.gn
M       chrome/browser/file_select_helper.cc
M       chrome/browser/file_select_helper.h
M       chrome/browser/picture_in_picture/auto_picture_in_picture_tab_helper.cc
M       chrome/browser/picture_in_picture/picture_in_picture_window_manager.cc
M       chrome/browser/picture_in_picture/picture_in_picture_window_manager.h
M       chrome/browser/picture_in_picture/picture_in_picture_window_manager_unittest.cc
A       chrome/browser/picture_in_picture/scoped_disallow_picture_in_picture.cc
A       chrome/browser/picture_in_picture/scoped_disallow_picture_in_picture.h
M       media/base/media_switches.cc
M       media/base/media_switches.h
M       tools/metrics/histograms/metadata/media/enums.xml
M       tools/metrics/histograms/metadata/media/histograms.xml

https://chromium-review.googlesource.com/5753110


### st...@chromium.org (2024-09-05)

After looking at some metrics to determine how often file pickers and pip windows were both open, we decided to just close pip windows whenever a file dialog is open. This avoids the issue entirely.

Ideally we would have only done this when the pip window actually occludes the file dialog, but due to the nature of file dialogs (they're not Chrome widgets but often owned/opened by the OS) it was fairly complex and platform-dependent. We decided the simpler route of always closing was the better alternative

### ap...@google.com (2024-09-11)

Project: chromium/src
Branch: main

commit 377ccf6b184e982d278f999253e2bf839732d9db
Author: Tommy Steimel <steimel@chromium.org>
Date:   Wed Sep 11 18:15:53 2024

    Remove metrics for when file dialogs and pip windows are both open
    
    This CL removes the metrics we added to understand how often file
    dialogs and picture-in-picture windows are both open. These are no
    longer needed as we've settled on a solution based on the data
    already collected.
    
    Bug: 40076120
    Change-Id: I323211d46c8399a7911592027c985d084057a70e
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5852356
    Commit-Queue: Tommy Steimel <steimel@chromium.org>
    Reviewed-by: Evan Liu <evliu@google.com>
    Reviewed-by: Scott Violet <sky@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1354082}

M       chrome/browser/file_select_helper.cc
M       chrome/browser/file_select_helper.h
M       chrome/browser/picture_in_picture/picture_in_picture_window_manager.cc
M       chrome/browser/picture_in_picture/picture_in_picture_window_manager.h
M       tools/metrics/histograms/metadata/media/enums.xml
M       tools/metrics/histograms/metadata/media/histograms.xml

https://chromium-review.googlesource.com/5852356


### sp...@google.com (2024-09-11)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $5000.00 for this report.

Rationale for this decision:
$5,000 for high quality report of moderate impact security UI spoof / web platform privilege escalation 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-09-11)

Congratulations Lyra! Thank you for your efforts and reporting this issue to us -- nice work!

### re...@gmail.com (2024-09-11)

Thank you so much for the reward :)

### pe...@google.com (2024-11-01)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2024-11-01)

1. https://chromium-review.googlesource.com/c/chromium/src/+/5981649
2. Medium - I think we need to merge 3 CLs to fix this bug. But, the last CL was just to remove the first CL. So it's likely we only need to merge the second CL to M126 LTS. However, there were some conflicts when merging the second CL to M126.
3. No.
4. Yes, as mentioned in the description, the issue was reproduced on 119.0.6045.106 Stable + Dev.

### gm...@google.com (2024-11-04)

Answer to 3 is yes, it's on 130. Approving for LTS-126

### ap...@google.com (2024-11-06)

Project: chromium/src  

Branch: refs/branch-heads/6478  

Author: Gyuyoung Kim <[qkim@google.com](mailto:qkim@google.com)>  

Link:      <https://chromium-review.googlesource.com/5981649>

[M126-LTS] Close picture-in-picture windows when a file dialog is present

---


Expand for full commit details
```
[M126-LTS] Close picture-in-picture windows when a file dialog is present 
 
This CL adds `ScopedDisallowPictureInPicture`, which can be used to 
close any existing picture-in-picture windows and prevent new ones from 
opening. This is used in the `FileSelectHelper` to prevent 
picture-in-picture windows from occluding file dialogs. 
 
(cherry picked from commit 47617c1e9e6217aa03b889a8a3f1af44b4baa1ef) 
 
Bug: 40076120 
Change-Id: I5b8eb02003370cf14d5968a39f62a13e925b112a 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5753110 
Commit-Queue: Tommy Steimel <steimel@chromium.org> 
Reviewed-by: Frank Liberato <liberato@chromium.org> 
Reviewed-by: Evan Liu <evliu@google.com> 
Reviewed-by: Scott Violet <sky@chromium.org> 
Cr-Original-Commit-Position: refs/heads/main@{#1351716} 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5981649 
Commit-Queue: Mohamed Omar <mohamedaomar@google.com> 
Owners-Override: Mohamed Omar <mohamedaomar@google.com> 
Reviewed-by: Mohamed Omar <mohamedaomar@google.com> 
Cr-Commit-Position: refs/branch-heads/6478@{#1990} 
Cr-Branched-From: e6143acc03189c5e52959545b110d6d17ecd5286-refs/heads/main@{#1300313}

```

---

Files:

- M `chrome/browser/BUILD.gn`
- M `chrome/browser/file_select_helper.cc`
- M `chrome/browser/file_select_helper.h`
- M `chrome/browser/picture_in_picture/auto_picture_in_picture_tab_helper.cc`
- M `chrome/browser/picture_in_picture/picture_in_picture_window_manager.cc`
- M `chrome/browser/picture_in_picture/picture_in_picture_window_manager.h`
- M `chrome/browser/picture_in_picture/picture_in_picture_window_manager_unittest.cc`
- A `chrome/browser/picture_in_picture/scoped_disallow_picture_in_picture.cc`
- A `chrome/browser/picture_in_picture/scoped_disallow_picture_in_picture.h`
- M `media/base/media_switches.cc`
- M `media/base/media_switches.h`
- M `tools/metrics/histograms/metadata/media/enums.xml`
- M `tools/metrics/histograms/metadata/media/histograms.xml`

---

Hash: b5206c953a402ca234c16d923759200c06321038  

Date:  Wed Nov 06 21:31:23 2024


---

### ap...@google.com (2024-11-11)

Project: chromium/src  

Branch: refs/branch-heads/6478\_182  

Author: Gyuyoung Kim <[qkim@google.com](mailto:qkim@google.com)>  

Link:      <https://chromium-review.googlesource.com/6011312>

[CfM-R126] Close picture-in-picture windows when a file dialog is present

---


Expand for full commit details
```
[CfM-R126] Close picture-in-picture windows when a file dialog is present 
 
This CL adds `ScopedDisallowPictureInPicture`, which can be used to 
close any existing picture-in-picture windows and prevent new ones from 
opening. This is used in the `FileSelectHelper` to prevent 
picture-in-picture windows from occluding file dialogs. 
 
(cherry picked from commit 47617c1e9e6217aa03b889a8a3f1af44b4baa1ef) 
 
(cherry picked from commit b5206c953a402ca234c16d923759200c06321038) 
 
Bug: 40076120 
Change-Id: I5b8eb02003370cf14d5968a39f62a13e925b112a 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5753110 
Commit-Queue: Tommy Steimel <steimel@chromium.org> 
Reviewed-by: Frank Liberato <liberato@chromium.org> 
Reviewed-by: Evan Liu <evliu@google.com> 
Reviewed-by: Scott Violet <sky@chromium.org> 
Cr-Original-Original-Commit-Position: refs/heads/main@{#1351716} 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5981649 
Commit-Queue: Mohamed Omar <mohamedaomar@google.com> 
Owners-Override: Mohamed Omar <mohamedaomar@google.com> 
Reviewed-by: Mohamed Omar <mohamedaomar@google.com> 
Cr-Original-Commit-Position: refs/branch-heads/6478@{#1990} 
Cr-Original-Branched-From: e6143acc03189c5e52959545b110d6d17ecd5286-refs/heads/main@{#1300313} 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6011312 
Owners-Override: Kyle Williams <kdgwill@chromium.org> 
Commit-Queue: Kyle Williams <kdgwill@chromium.org> 
Reviewed-by: Niko Tsirakis <ntsirakis@google.com> 
Auto-Submit: Kyle Williams <kdgwill@chromium.org> 
Cr-Commit-Position: refs/branch-heads/6478_182@{#100} 
Cr-Branched-From: 5b5d8292ddf182f8b2096fa665b473b6317906d5-refs/branch-heads/6478@{#1776} 
Cr-Branched-From: e6143acc03189c5e52959545b110d6d17ecd5286-refs/heads/main@{#1300313}

```

---

Files:

- M `chrome/browser/BUILD.gn`
- M `chrome/browser/file_select_helper.cc`
- M `chrome/browser/file_select_helper.h`
- M `chrome/browser/picture_in_picture/auto_picture_in_picture_tab_helper.cc`
- M `chrome/browser/picture_in_picture/picture_in_picture_window_manager.cc`
- M `chrome/browser/picture_in_picture/picture_in_picture_window_manager.h`
- M `chrome/browser/picture_in_picture/picture_in_picture_window_manager_unittest.cc`
- A `chrome/browser/picture_in_picture/scoped_disallow_picture_in_picture.cc`
- A `chrome/browser/picture_in_picture/scoped_disallow_picture_in_picture.h`
- M `media/base/media_switches.cc`
- M `media/base/media_switches.h`
- M `tools/metrics/histograms/metadata/media/enums.xml`
- M `tools/metrics/histograms/metadata/media/histograms.xml`

---

Hash: 80ea54235f8cd7a154d90f76da8b6eb169b365d3  

Date:  Mon Nov 11 18:56:56 2024


---

### pe...@google.com (2024-12-13)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40076120)*
