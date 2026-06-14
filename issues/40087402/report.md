# Security: Field validation bubbles can appear over the wrong tab

| Field | Value |
|-------|-------|
| **Issue ID** | [40087402](https://issues.chromium.org/issues/40087402) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Forms>Validation |
| **Reporter** | ch...@gmail.com |
| **Assignee** | tk...@chromium.org |
| **Created** | 2017-04-20 |
| **Bounty** | $500.00 |

## Description

**VERSION**  

Chrome Version: Canary 60.0.3076.0  

Operating System: Windows 7

**REPRODUCTION CASE**

1. Open testcase.html.
2. Click on the button and observe.

From <https://crbug.com/chromium/673163> and <https://crbug.com/chromium/704560>.

## Attachments

- [screenshot.png](attachments/screenshot.png) (image/png, 154.7 KB)
- [testcase.html](attachments/testcase.html) (text/plain, 3.4 KB)

## Timeline

### el...@chromium.org (2017-04-20)

Confirmed.

[Monorail components: Blink>Forms>Validation]

### el...@chromium.org (2017-04-20)

[Empty comment from Monorail migration]

### me...@chromium.org (2017-04-20)

tkent: Can you please take a look?

### tk...@chromium.org (2017-04-21)

Oh, print()! interesting.



### bu...@chromium.org (2017-04-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/9dbd356b0cc52911caef089b09de63572cd9e39f

commit 9dbd356b0cc52911caef089b09de63572cd9e39f
Author: tkent <tkent@chromium.org>
Date: Fri Apr 21 06:38:15 2017

window.print() should close form validation bubble.

Usually, window.open() deactivates the origin window and validation bubble on the
origin window is closed. However, if window.print() is executed, it suspends message
loop of the window, and deactivation isn't noticed until print dialog is closed.
So, we need to close validation popup explicitly for window.print().

BUG=713686

Review-Url: https://codereview.chromium.org/2834783002
Cr-Commit-Position: refs/heads/master@{#466273}

[modify] https://crrev.com/9dbd356b0cc52911caef089b09de63572cd9e39f/third_party/WebKit/Source/web/ChromeClientImpl.cpp
[modify] https://crrev.com/9dbd356b0cc52911caef089b09de63572cd9e39f/third_party/WebKit/Source/web/ChromeClientImpl.h
[modify] https://crrev.com/9dbd356b0cc52911caef089b09de63572cd9e39f/third_party/WebKit/Source/web/ValidationMessageClientImpl.cpp
[modify] https://crrev.com/9dbd356b0cc52911caef089b09de63572cd9e39f/third_party/WebKit/Source/web/ValidationMessageClientImpl.h


### sh...@chromium.org (2017-04-21)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-04-21)

This issue is a security regression. If you are not able to fix this quickly, please revert the change that introduced it.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2017-04-21)

[Empty comment from Monorail migration]

### ch...@gmail.com (2017-04-21)

Verified on 60.0.3078.0. Thanks for the quick fix!

### sh...@chromium.org (2017-04-22)

[Empty comment from Monorail migration]

### tk...@chromium.org (2017-04-23)

This affects 58 stable.


### sh...@chromium.org (2017-04-23)

Your change meets the bar and is auto-approved for M59. Please go ahead and merge the CL to branch 3071 manually. Please contact milestone owner if you have questions.
Owners: amineer@(Android), cmasso@(iOS), gkihumba@(ChromeOS), Abdul Syed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2017-04-23)

This bug requires manual review: We are only 1 days from stable.
Please contact the milestone owner if you have questions.
Owners: amineer@(Android), cmasso@(iOS), bhthompson@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2017-04-23)

Your change meets the bar and is auto-approved for M59. Please go ahead and merge the CL to branch 3071 manually. Please contact milestone owner if you have questions.
Owners: amineer@(Android), cmasso@(iOS), gkihumba@(ChromeOS), Abdul Syed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2017-04-23)

[Comment Deleted]

### go...@chromium.org (2017-04-23)

+awhalley@ for M58 merge review. Please note M58 is already in Stable and bar is VERY high to take any merges in for future stable refresh if any.

### go...@chromium.org (2017-04-23)

Please merge your change to M59 branch #3071 latest before 4:00 PM PT, Monday (04/24) so we can take it for next week last M59 dev release. Thank you.

### bu...@chromium.org (2017-04-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/31455b249cf2737bf96ab751252b84e8c85b3804

commit 31455b249cf2737bf96ab751252b84e8c85b3804
Author: Kent Tamura <tkent@chromium.org>
Date: Mon Apr 24 00:59:15 2017

Merge "window.print() should close form validation bubble." to M59

Usually, window.open() deactivates the origin window and validation bubble on the
origin window is closed. However, if window.print() is executed, it suspends message
loop of the window, and deactivation isn't noticed until print dialog is closed.
So, we need to close validation popup explicitly for window.print().

BUG=713686

Review-Url: https://codereview.chromium.org/2834783002
Cr-Commit-Position: refs/heads/master@{#466273}
(cherry picked from commit 9dbd356b0cc52911caef089b09de63572cd9e39f)

Review-Url: https://codereview.chromium.org/2833303002 .
Cr-Commit-Position: refs/branch-heads/3071@{#151}
Cr-Branched-From: a106f0abbf69dad349d4aaf4bcc4f5d376dd2377-refs/heads/master@{#464641}

[modify] https://crrev.com/31455b249cf2737bf96ab751252b84e8c85b3804/third_party/WebKit/Source/web/ChromeClientImpl.cpp
[modify] https://crrev.com/31455b249cf2737bf96ab751252b84e8c85b3804/third_party/WebKit/Source/web/ChromeClientImpl.h
[modify] https://crrev.com/31455b249cf2737bf96ab751252b84e8c85b3804/third_party/WebKit/Source/web/ValidationMessageClientImpl.cpp
[modify] https://crrev.com/31455b249cf2737bf96ab751252b84e8c85b3804/third_party/WebKit/Source/web/ValidationMessageClientImpl.h


### sh...@chromium.org (2017-04-24)

[Empty comment from Monorail migration]

### aw...@google.com (2017-04-24)

No need to rush this into a 58 stable update.

### go...@chromium.org (2017-04-24)

Applying "Merge-Rejected-58" label per https://crbug.com/chromium/713686#c20.

### aw...@google.com (2017-04-24)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-04-28)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-04-28)

The panel decided to award $500 for this bug.  Thanks as ever!

### aw...@chromium.org (2017-04-28)

[Empty comment from Monorail migration]

### aw...@google.com (2017-05-03)

[Empty comment from Monorail migration]

### aw...@google.com (2017-05-03)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-05-25)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-05-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-07-31)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/713686?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/713477]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40087402)*
