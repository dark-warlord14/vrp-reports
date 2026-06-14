# Chrome tab crashes when a pattern containing a Hebrew character followed by 2 horizontal tabs and then another character is clicked.

| Field | Value |
|-------|-------|
| **Issue ID** | [40093383](https://issues.chromium.org/issues/40093383) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Layout |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | [Deleted User] |
| **Assignee** | ea...@chromium.org |
| **Created** | 2018-12-11 |
| **Bounty** | $1,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36

Steps to reproduce the problem:
1. Go to a web page that displays a string with the specified pattern (or type such a string in a text box).
2. For example, "א		1"
3. Click on the tabs (area between the 2 characters).
4. Chrome tab will crash.

What is the expected behavior?
Chrome tab should not crash.

What went wrong?
Bug was encountered while using our web app. After some debugging it was reproduced outside of the app and thus deemed as a Chrome bug and not a bug in our app.

Crashed report ID: fd22ec05c6a72406 

How much crashed? Just one tab

Is it a problem with a plugin? No 

Did this work before? N/A 

Chrome version: 71.0.3578.80  Channel: stable
OS Version: 10.0
Flash Version: 

Clicking the example given here might be enough to reproduce. Otherwise, this pastebin can be used:
https://pastebin.com/raw/VzsCbrRQ

## Timeline

### dt...@chromium.org (2018-12-11)

[Empty comment from Monorail migration]

[Monorail components: Blink>Editing>Selection]

### [Deleted User] (2018-12-11)

Reproduced on Android as well (70.0.3538.110).

### cr...@chromium.org (2018-12-11)

[Empty comment from Monorail migration]

### cr...@chromium.org (2018-12-11)

I can repro on OSX and CrOS, adding labels.

- OSX (71.0.3578.80)
- CrOS (71.0.3578.85

### pb...@chromium.org (2018-12-11)

You are probably looking for a change made after 578698 (known good), but no later than 578699 (first known bad).
CHANGELOG URL:
The script might not always return single CL as suspect as some perf builds might get missing due to failure.
  https://chromium.googlesource.com/chromium/src/+log/cdcd8946ca73cc68e84e782f515b40531e57365f..ad2fcd6e0a36a7282b1b7140f258e7e071a5e753


Note : This is reproduciable on Chrome Stable, Beta and dev Channels, where in on canary I wasn't able to reproduce the issue. Since this been present on M70 and M71 not tagging with any blocker labels.

[Monorail components: -Blink>Editing>Selection Blink>Layout]

### ea...@chromium.org (2018-12-12)

Reproduces even in canary for me. Looking into it.

### ea...@chromium.org (2018-12-12)

[Empty comment from Monorail migration]

### ca...@chromium.org (2018-12-12)

Assigning medium severity as per https://chromium.googlesource.com/chromium/src/+/master/docs/security/severity-guidelines.md

### ea...@chromium.org (2018-12-12)

Thanks carlosil!

Fix in review, https://chromium-review.googlesource.com/c/chromium/src/+/1374630
Should be safe to down-integrate if needed.

### pb...@chromium.org (2018-12-12)

[Empty comment from Monorail migration]

### ab...@chromium.org (2018-12-12)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-12-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/8c7054864ea9b70015351b17376b8515296efb8f

commit 8c7054864ea9b70015351b17376b8515296efb8f
Author: Emil A Eklund <eae@chromium.org>
Date: Thu Dec 13 01:22:10 2018

Fix crash in RunInfo::NumGraphemes

Fix crash in NumGraphemes when called with an invalid end char position.

Bug: 913975
Test: fast/text/international/ar_tab_selection_crash.html
Change-Id: I93a94ba04e3e02b10ac8ef4186cf606b7df5c859
Reviewed-on: https://chromium-review.googlesource.com/c/1374630
Commit-Queue: Koji Ishii <kojii@chromium.org>
Reviewed-by: Koji Ishii <kojii@chromium.org>
Cr-Commit-Position: refs/heads/master@{#616145}
[modify] https://crrev.com/8c7054864ea9b70015351b17376b8515296efb8f/third_party/blink/renderer/platform/fonts/shaping/shape_result.cc
[add] https://crrev.com/8c7054864ea9b70015351b17376b8515296efb8f/third_party/blink/web_tests/fast/text/international/ar_tab_selection_crash-expected.txt
[add] https://crrev.com/8c7054864ea9b70015351b17376b8515296efb8f/third_party/blink/web_tests/fast/text/international/ar_tab_selection_crash.html


### [Deleted User] (2018-12-13)

Glad to see this is progressing quickly and that a fix is already on the way. 

As a side note, since I see this is now classified as a Medium Severity security bug, does this somehow qualify for the Chrome Reward Program?

### sh...@chromium.org (2018-12-13)

[Empty comment from Monorail migration]

### ea...@chromium.org (2018-12-13)

[Empty comment from Monorail migration]

### [Deleted User] (2018-12-13)

I'll take that as a "no"? :)

### ea...@chromium.org (2018-12-13)

It'll be considered. In the mean time, thank you for the detailed report and the minimal test case, it really helped isolating and fixing the issue!


### [Deleted User] (2018-12-13)

Glad to have helped, thanks for the reply!

### sh...@chromium.org (2018-12-14)

[Empty comment from Monorail migration]

### ea...@chromium.org (2018-12-14)

Requesting merge into M72.

### sh...@chromium.org (2018-12-14)

This bug requires manual review: M72 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: govind@(Android), kariahda@(iOS), djmm@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@google.com (2018-12-14)

Hi Guy - we consider bugs for reward once they've been marked as fixed, so it'll get picked up for a VRP panel meeting soon (modulo breaks over the holiday season).

@govind - good for 72

### go...@chromium.org (2018-12-14)

Approving merge to M72 branch 3626 based on https://crbug.com/chromium/913975#c22. Please merge ASAP. Thank you.

### ea...@chromium.org (2018-12-14)

Merged to refs/branch-heads/3626 as revision 369.

### bu...@chromium.org (2018-12-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/924e86aa0d2616a5464f285adffd0e9e588438e0

commit 924e86aa0d2616a5464f285adffd0e9e588438e0
Author: Emil A Eklund <eae@chromium.org>
Date: Fri Dec 14 22:08:32 2018

Fix crash in RunInfo::NumGraphemes

Fix crash in NumGraphemes when called with an invalid end char position.

Bug: 913975
Test: fast/text/international/ar_tab_selection_crash.html
Change-Id: I93a94ba04e3e02b10ac8ef4186cf606b7df5c859
Reviewed-on: https://chromium-review.googlesource.com/c/1374630
Commit-Queue: Koji Ishii <kojii@chromium.org>
Reviewed-by: Koji Ishii <kojii@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#616145}(cherry picked from commit 8c7054864ea9b70015351b17376b8515296efb8f)
Reviewed-on: https://chromium-review.googlesource.com/c/1379110
Reviewed-by: Emil A Eklund <eae@chromium.org>
Cr-Commit-Position: refs/branch-heads/3626@{#369}
Cr-Branched-From: d897fb137fbaaa9355c0c93124cc048824eb1e65-refs/heads/master@{#612437}
[modify] https://crrev.com/924e86aa0d2616a5464f285adffd0e9e588438e0/third_party/blink/renderer/platform/fonts/shaping/shape_result.cc
[add] https://crrev.com/924e86aa0d2616a5464f285adffd0e9e588438e0/third_party/blink/web_tests/fast/text/international/ar_tab_selection_crash-expected.txt
[add] https://crrev.com/924e86aa0d2616a5464f285adffd0e9e588438e0/third_party/blink/web_tests/fast/text/international/ar_tab_selection_crash.html


### na...@google.com (2018-12-17)

[Empty comment from Monorail migration]

### cr...@appspot.gserviceaccount.com (2018-12-19)

The following revision refers to this bug: 
https://chromium.googlesource.com/chromium/src.git/+/924e86aa0d2616a5464f285adffd0e9e588438e0

Commit: 924e86aa0d2616a5464f285adffd0e9e588438e0
Author: eae@chromium.org
Commiter: eae@chromium.org
Date: 2018-12-14 22:08:32 +0000 UTC

Fix crash in RunInfo::NumGraphemes

Fix crash in NumGraphemes when called with an invalid end char position.

Bug: 913975
Test: fast/text/international/ar_tab_selection_crash.html
Change-Id: I93a94ba04e3e02b10ac8ef4186cf606b7df5c859
Reviewed-on: https://chromium-review.googlesource.com/c/1374630
Commit-Queue: Koji Ishii <kojii@chromium.org>
Reviewed-by: Koji Ishii <kojii@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#616145}(cherry picked from commit 8c7054864ea9b70015351b17376b8515296efb8f)
Reviewed-on: https://chromium-review.googlesource.com/c/1379110
Reviewed-by: Emil A Eklund <eae@chromium.org>
Cr-Commit-Position: refs/branch-heads/3626@{#369}
Cr-Branched-From: d897fb137fbaaa9355c0c93124cc048824eb1e65-refs/heads/master@{#612437}

### cr...@appspot.gserviceaccount.com (2018-12-19)

The following revision refers to this bug: 
https://chromium.googlesource.com/chromium/src.git/+/924e86aa0d2616a5464f285adffd0e9e588438e0

Commit: 924e86aa0d2616a5464f285adffd0e9e588438e0
Author: eae@chromium.org
Commiter: eae@chromium.org
Date: 2018-12-14 22:08:32 +0000 UTC

Fix crash in RunInfo::NumGraphemes

Fix crash in NumGraphemes when called with an invalid end char position.

Bug: 913975
Test: fast/text/international/ar_tab_selection_crash.html
Change-Id: I93a94ba04e3e02b10ac8ef4186cf606b7df5c859
Reviewed-on: https://chromium-review.googlesource.com/c/1374630
Commit-Queue: Koji Ishii <kojii@chromium.org>
Reviewed-by: Koji Ishii <kojii@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#616145}(cherry picked from commit 8c7054864ea9b70015351b17376b8515296efb8f)
Reviewed-on: https://chromium-review.googlesource.com/c/1379110
Reviewed-by: Emil A Eklund <eae@chromium.org>
Cr-Commit-Position: refs/branch-heads/3626@{#369}
Cr-Branched-From: d897fb137fbaaa9355c0c93124cc048824eb1e65-refs/heads/master@{#612437}

### na...@google.com (2018-12-19)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### na...@google.com (2018-12-20)

Thanks for your report. The panel has decided to reward $1,000 :) 

Since you are a new reporter a member of our finance will be in touch. 

Additionally, how would you like to be credited in release notes?



### [Deleted User] (2018-12-20)

Oh wow, thank you very much!
As for the credit, "Guy Eshel" is fine :)

### na...@google.com (2018-12-20)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-01-28)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-01-28)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-02-19)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-03-22)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/913975?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093383)*
