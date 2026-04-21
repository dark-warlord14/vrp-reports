# Security: readanything render frame UAF fix of crbug.com/1488268 is not robust.

| Field | Value |
|-------|-------|
| **Issue ID** | [40936128](https://issues.chromium.org/issues/40936128) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | UI>Accessibility>ReadingMode |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | zh...@gmail.com |
| **Assignee** | jo...@google.com |
| **Created** | 2023-10-13 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**

<https://chromium-review.googlesource.com/c/chromium/src/+/4908587>

While reviewing the aforementioned modification, I discovered that  

it did not work as the owner's expectations.

The primary modification made in this fix is the inclusion of a  

check for the raw pointer |render\_frame\_| before its usage.

```
void ReadAnythingAppController::ExecuteJavaScript(std::string script) {  
  if (!render_frame_) {     
    return;  // <-- render_frame_ is not null ptr even though it is gone.  
  }  
  
  // <-- UAF here if render_frame_ is freed.  
  render_frame_->ExecuteJavaScript(base::ASCIIToUTF16(script));    
}  

```

However, the raw\_ptr did not support this type of verification. The  

condition "if (!render\_frame\_)" will only evaluate to true if  

render\_frame\_ is explicitly set to nullptr beforehand.

For instance, executing the |test| function below will lead to a UAF.

```
void test() {  
  int \*pa = new int(42);  
  raw_ptr<int> raw_a(pa);  
  delete pa;  
  
  if (!raw_a) {  
    LOG(INFO) << "ok...";  
  } else {  
    LOG(ERROR) << \*raw_a;  
  }  
}  

```

**VERSION**  

Chrome Version: This is the fix bypass of <https://crbug.com/1488268>. I also reproduced the same UAF in stable channel, version: 118.0.5993.70  

Operating System: ALL

**REPRODUCTION CASE**

1. Run ./out/Default/chrome --enable-features=ReadAnything 2>&1 | tools/valgrind/asan/asan\_symbolize.py
2. Open a new tab with url: chrome-untrusted://read-anything-side-panel.top-chrome/
3. Go to "<https://google.com>"

Demo video also attached.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State: see attached readanything-render-uaf.asan

**CREDIT INFORMATION**  

Reporter credit: Chaobin Zhang

SUGGESTION FIX  

Please review the attached file readanything-reander-uaf-fix.patch  

for more details.

## Attachments

- [readanything-render-uaf.asan](attachments/readanything-render-uaf.asan) (text/plain, 23.9 KB)
- [readanything-render-uaf.demo.mp4](attachments/readanything-render-uaf.demo.mp4) (video/mp4, 4.7 MB)
- [readanything-reander-uaf-fix.patch](attachments/readanything-reander-uaf-fix.patch) (text/plain, 3.4 KB)

## Timeline

### [Deleted User] (2023-10-13)

[Empty comment from Monorail migration]

### ct...@chromium.org (2023-10-14)

Thanks for the report. Adding folks from https://crbug.com/chromium/1488268.

It looks like the M118 cherry-pick for the fix in https://crbug.com/chromium/1488268 has not yet been released https://chromiumdash.appspot.com/commit/86f0cf0295bc1dc3d9877afb7949e1ecbda8a85d. However, I'm able to reproduce this using the reporter's steps on M120 Dev (Linux), so this does continue to be an issue after crrev.com/c/4908587.

Setting the same security severity as https://crbug.com/chromium/1488268, although this is heavily mitigated by not being remotely exploitable and requiring user interaction to trigger.

[Monorail components: UI>Accessibility>ReadingMode]

### [Deleted User] (2023-10-14)

[Empty comment from Monorail migration]

### zh...@gmail.com (2023-10-14)

> It looks like the M118 cherry-pick for the fix in https://crbug.com/chromium/1488268 has not yet been released https://chromiumdash.appspot.com/commit/86f0cf0295bc1dc3d9877afb7949e1ecbda8a85d. 

The fix in issue #1488268 didn't change the code logic actually, since  |if (!render_frame_)| will always evaluate to false. I reproduce the UAF both in stable M118 (before the fix) and also in my local build of M120 (after the fix).

### [Deleted User] (2023-10-14)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jo...@google.com (2023-10-19)

[Empty comment from Monorail migration]

### jo...@google.com (2023-10-23)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-10-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/8726246686fb97b2b52445ed9ff8ebc2d1740b64

commit 8726246686fb97b2b52445ed9ff8ebc2d1740b64
Author: Jocelyn Tran <jocelyntran@google.com>
Date: Mon Oct 23 21:35:14 2023

[Read Anything] Use render frame id instead of pointer

Fixed: 1492396
Change-Id: Id721aea793e4877b193c9d71fb1ff41020f054b0
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4955256
Reviewed-by: Mark Schillaci <mschillaci@google.com>
Commit-Queue: Jocelyn Tran <jocelyntran@google.com>
Cr-Commit-Position: refs/heads/main@{#1213759}

[modify] https://crrev.com/8726246686fb97b2b52445ed9ff8ebc2d1740b64/chrome/renderer/accessibility/read_anything_app_controller.h
[modify] https://crrev.com/8726246686fb97b2b52445ed9ff8ebc2d1740b64/chrome/renderer/accessibility/read_anything_app_controller.cc


### [Deleted User] (2023-10-24)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-24)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-24)

Requesting merge to beta M119 because latest trunk commit (1213759) appears to be after beta branch point (1204232).

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jo...@google.com (2023-10-24)

1. https://chromium-review.googlesource.com/c/chromium/src/+/4955256
2. yes
3. no known stability regressions or risks
4. no known compatibility ricks
5. no manual verification required

### [Deleted User] (2023-10-24)

Merge review required: M119 has already been cut for stable release.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: eakpobaro (Android), eakpobaro (iOS), dgagnon (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jo...@google.com (2023-10-25)

1. medium severity security issue
2. https://chromium-review.googlesource.com/c/chromium/src/+/4955256
3. yes
4. yes, this is for a new feature. it's not behind a finch flag and experiments are active.

### am...@chromium.org (2023-10-26)

119 merge approved for https://crrev.com/c/4955256
please merge this fix to branch 6045 at your convenience -- thank you 

### gi...@appspot.gserviceaccount.com (2023-10-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/2fa4bc5c800e90a7145189dce6dc97fc048e7ad2

commit 2fa4bc5c800e90a7145189dce6dc97fc048e7ad2
Author: Jocelyn Tran <jocelyntran@google.com>
Date: Fri Oct 27 01:09:16 2023

[Merge M119][Read Anything] Use render frame id instead of pointer

(cherry picked from commit 8726246686fb97b2b52445ed9ff8ebc2d1740b64)

Fixed: 1492396
Change-Id: Id721aea793e4877b193c9d71fb1ff41020f054b0
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4955256
Reviewed-by: Mark Schillaci <mschillaci@google.com>
Commit-Queue: Jocelyn Tran <jocelyntran@google.com>
Cr-Original-Commit-Position: refs/heads/main@{#1213759}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4978748
Cr-Commit-Position: refs/branch-heads/6045@{#1003}
Cr-Branched-From: 905e8bdd32d891451d94d1ec71682e989da2b0a1-refs/heads/main@{#1204232}

[modify] https://crrev.com/2fa4bc5c800e90a7145189dce6dc97fc048e7ad2/chrome/renderer/accessibility/read_anything_app_controller.h
[modify] https://crrev.com/2fa4bc5c800e90a7145189dce6dc97fc048e7ad2/chrome/renderer/accessibility/read_anything_app_controller.cc


### [Deleted User] (2023-10-27)

LTS Milestone M114

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2023-10-27)

[Empty comment from Monorail migration]

### pg...@google.com (2023-10-30)

[Empty comment from Monorail migration]

### pg...@google.com (2023-11-01)

[Empty comment from Monorail migration]

### pg...@google.com (2023-11-01)

[Empty comment from Monorail migration]

### am...@google.com (2023-11-02)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-11-02)

Congratulations Chaobin! The Chrome VRP Panel has decided to award you $2,000 for this report of a highly mitigated security bug, mitigated by UI interaction and BRP protection. Thank you for your efforts and reporting this issue to us! 

### zh...@gmail.com (2023-11-02)

Thank you very much! 

### rz...@google.com (2023-11-03)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-03)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2023-11-03)

[Empty comment from Monorail migration]

### gm...@google.com (2023-11-06)

[Empty comment from Monorail migration]

### gm...@google.com (2023-11-06)

@rzanoni reminder to answer the questionnaire

### rz...@google.com (2023-11-13)

1. https://crrev.com/c/4981980
2. Medium, the author helped with the conflict resolution. I tested the CL and couldn't reproduce the crash.
3. 119
4. Yes

### na...@google.com (2023-12-11)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-12-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/8bbecbaea5f9f74c1b28ea049fd1d5550a52620f

commit 8bbecbaea5f9f74c1b28ea049fd1d5550a52620f
Author: Jocelyn Tran <jocelyntran@google.com>
Date: Wed Dec 13 21:14:47 2023

[M114-LTS][Read Anything] Use render frame id instead of pointer

M114 merge issues:
  chrome/renderer/accessibility/read_anything_app_controller.h:
    Conflicting types for render_frame_

  chrome/renderer/accessibility/read_anything_app_controller.cc:
    - ExecuteJavaScript() isn't present in 114
    - OnConnected()/SetContentForTesting(): render_frame check isn't present in 114

(cherry picked from commit 8726246686fb97b2b52445ed9ff8ebc2d1740b64)

Fixed: 1492396
Change-Id: Id721aea793e4877b193c9d71fb1ff41020f054b0
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4955256
Commit-Queue: Jocelyn Tran <jocelyntran@google.com>
Cr-Original-Commit-Position: refs/heads/main@{#1213759}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4981980
Owners-Override: Achuith Bhandarkar <achuith@chromium.org>
Reviewed-by: Achuith Bhandarkar <achuith@chromium.org>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Cr-Commit-Position: refs/branch-heads/5735@{#1649}
Cr-Branched-From: 2f562e4ddbaf79a3f3cb338b4d1bd4398d49eb67-refs/heads/main@{#1135570}

[modify] https://crrev.com/8bbecbaea5f9f74c1b28ea049fd1d5550a52620f/chrome/renderer/accessibility/read_anything_app_controller.h
[modify] https://crrev.com/8bbecbaea5f9f74c1b28ea049fd1d5550a52620f/chrome/renderer/accessibility/read_anything_app_controller.cc


### rz...@google.com (2023-12-13)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-30)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2024-01-30)

This issue was migrated from crbug.com/chromium/1492396?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

### ni...@google.com (2024-05-28)

marking verrified per comment 24

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40936128)*
