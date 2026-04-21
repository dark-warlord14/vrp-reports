# Security: File picker dialog can be shown over a different tab

| Field | Value |
|-------|-------|
| **Issue ID** | [40944847](https://issues.chromium.org/issues/40944847) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>Forms>File, UI>Browser>Navigation |
| **Platforms** | Windows |
| **Reporter** | ch...@gmail.com |
| **Assignee** | bo...@chromium.org |
| **Created** | 2023-11-21 |
| **Bounty** | $1,000.00 |

## Description

**VERSION**  

Chrome Version: 121.0.6139.0 (Official Build) canary (64-bit) (cohort: Clang-64)  

Operating System: Windows 10

I think the fix for <https://crbug.com/chromium/1414936> was incomplete. I am still able to repro it.

**REPRODUCTION CASE**

1. Open poc.html
2. Click in the page

This bug takes several attempts to repro, and is not reproduced consistently.

## Attachments

- [Recording #3.mp4](attachments/Recording #3.mp4) (video/mp4, 665.7 KB)
- [poc.html](attachments/poc.html) (text/plain, 826 B)
- [testcase (2).html](attachments/testcase (2).html) (text/plain, 838 B)
- [screen-capture.webm](attachments/screen-capture.webm) (video/webm, 2.4 MB)

## Timeline

### [Deleted User] (2023-11-21)

[Empty comment from Monorail migration]

### pm...@chromium.org (2023-11-22)

A single click would lead to the popup being blocked by: window.open blocked due to active file chooser.
However clicking rapidly after closing the file chooser allows both the file chooser and the popup to be opened.
This worked on windows stable but not on linux.
The severity seems fairly low given the sequence of event the user has to do.

[Monorail components: Blink>Forms>File UI>Browser>Navigation]

### [Deleted User] (2023-11-22)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-22)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pm...@google.com (2023-11-23)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-05)

[Empty comment from Monorail migration]

### ch...@gmail.com (2023-12-09)

I can easily reproduce this bug using the alert() dialog and consistently which can increase the severity.

### ch...@gmail.com (2023-12-09)

[Empty comment from Monorail migration]

### ch...@gmail.com (2023-12-13)

Shouldn't be higher than low severity as in https://crbug.com/chromium/1414936?

### ch...@gmail.com (2024-01-10)

Any update on this bug?

### na...@chromium.org (2024-01-10)

Assigning to boliu@, who owned the original bug pointed to in this report. Bo, please triage and reassign if appropriate.

### bo...@chromium.org (2024-01-10)

Sequence of IPCs on renderer side is:
1) OpenFileChooser: https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/html/forms/file_chooser.cc;drc=67d90538f11c6b232dbfd716075db52aeb34fd15;l=84
2) CreateWindow: https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/page/create_window.cc;drc=67d90538f11c6b232dbfd716075db52aeb34fd15;l=355
3) Show: https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/page/create_window.cc;drc=67d90538f11c6b232dbfd716075db52aeb34fd15;l=377

Through the magic of mojo (probably affected by something with the synchronous alert call), the order the calls arrive on browser UI side is 2, 1, 3. And 3 doesn't check for active file chooser, only 2 does.

### bo...@chromium.org (2024-01-10)

cc jam for review

### bo...@chromium.org (2024-01-10)

Fix merged: https://chromium-review.googlesource.com/c/chromium/src/+/5185860

### [Deleted User] (2024-01-11)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-11)

[Empty comment from Monorail migration]

### am...@google.com (2024-02-02)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2024-02-02)

Congratulations Khalil! The Chrome VRP Panel has decided to award you $1,000 for this report. The reward amount was decided due to the significant amount of specific and fast-timed UI interaction that would be required of a user to be exploitable by this issue. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2024-02-02)

[Empty comment from Monorail migration]

### is...@google.com (2024-02-02)

This issue was migrated from crbug.com/chromium/1504324?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>Forms>File, UI>Browser>Navigation]
[Monorail mergedwith: crbug.com/chromium/1504806]
[Monorail components added to Component Tags custom field.]

### ch...@gmail.com (2024-02-14)

deleted

### pe...@google.com (2024-04-18)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ap...@google.com (2024-11-22)

Project: chromium/src  

Branch: main  

Author: David Bienvenu <[davidbienvenu@chromium.org](mailto:davidbienvenu@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6043104>

codehealth: Remove stale WindowOpenSelectFix feature

---


Expand for full commit details
```
codehealth: Remove stale WindowOpenSelectFix feature 
 
Bug: 40944847, 356624363 
Change-Id: I2dbd9c25b138aab9074868e8e5a81dbb66094fdb 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6043104 
Reviewed-by: Bo Liu <boliu@chromium.org> 
Reviewed-by: Avi Drissman <avi@chromium.org> 
Code-Coverage: findit-for-me@appspot.gserviceaccount.com <findit-for-me@appspot.gserviceaccount.com> 
Commit-Queue: David Bienvenu <davidbienvenu@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#1386891}

```

---

Files:

- M `content/browser/web_contents/web_contents_impl.cc`
- M `content/common/features.cc`
- M `content/common/features.h`

---

Hash: 1a92f91888917e80073889cec31bccafc78201ab  

Date:  Fri Nov 22 17:16:23 2024


---

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40944847)*
