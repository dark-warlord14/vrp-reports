# Security: Heap-use-after-free in TypedArray.join

| Field | Value |
|-------|-------|
| **Issue ID** | [40093588](https://issues.chromium.org/issues/40093588) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | se...@gmail.com |
| **Assignee** | jg...@chromium.org |
| **Created** | 2018-12-27 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**  

While verifying the fix for <https://crbug.com/chromium/915783>, I noticed another issue in |TypedArray.join|. Converting the |separator| argument to a string has side effects, and then the method doesn't ensure that the array buffer hasn't been detached. That might lead to a similar use-after-free condition.

**VERSION**  

Google Chrome 73.0.3653.0 (Official Build) canary (64-bit) (cohort: Clang-64)  

Google Chrome 73.0.3642.0 (Official Build) dev (64-bit) (cohort: Dev)

**REPRODUCTION CASE**

<script>
array = new Int8Array(1024 \\* 1024);
array.join({toString() {
try {
postMessage("", "", [array.buffer]);
} catch { }
} });
</script>

## Attachments

- [join_image.html](attachments/join_image.html) (text/plain, 1.4 KB)
- [join.log](attachments/join.log) (text/plain, 1.0 KB)

## Timeline

### cl...@chromium.org (2018-12-27)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4865808936992768.

### cl...@chromium.org (2018-12-27)

Testcase 4865808936992768 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=4865808936992768.

### mp...@google.com (2018-12-27)

Thanks for the report. CF probably didn't reproduce because it's too recent--assigning to current v8 sheriff.

[Monorail components: Blink>JavaScript]

### cl...@chromium.org (2018-12-28)

Bisects to v8 roll 7.3.106 in ba46085641fdcec0a2bbc9d1d77f1fe965ef1768.
This roll contains d1c15973d32287e3cb54afbab57a1cc334ab81f2 ([builtins] Port TypedArray join, toString, and toLocaleString to Torque.).
Assigning to Jakob, cc Peter (author) and Peter (second reviewer).

### cl...@chromium.org (2018-12-28)

[Empty comment from Monorail migration]

### pe...@gmail.com (2018-12-28)

Taking a look a now. At a glance, I think this is an issue, but should be a small fix.
Thanks.

### sh...@chromium.org (2018-12-28)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-12-28)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pe...@gmail.com (2018-12-28)

Fix in-flight: https://chromium-review.googlesource.com/c/v8/v8/+/1392070

### bu...@chromium.org (2018-12-31)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/75ca843c5c545cf8f14ff1d5438777023ae7978e

commit 75ca843c5c545cf8f14ff1d5438777023ae7978e
Author: peterwmwong <peter.wm.wong@gmail.com>
Date: Mon Dec 31 18:27:51 2018

[typedarray] Check for a detached buffer before each iteration of TypedArray.p.join.

Bug: chromium:917980
Change-Id: Ia9b68f492bb9f0769dc6ee1706baf8b09de49968
Reviewed-on: https://chromium-review.googlesource.com/c/1392070
Commit-Queue: Peter Wong <peter.wm.wong@gmail.com>
Reviewed-by: Jakob Gruber <jgruber@chromium.org>
Cr-Commit-Position: refs/heads/master@{#58490}
[modify] https://crrev.com/75ca843c5c545cf8f14ff1d5438777023ae7978e/src/builtins/array-join.tq
[add] https://crrev.com/75ca843c5c545cf8f14ff1d5438777023ae7978e/test/mjsunit/regress/regress-crbug-917980.js


### ke...@chromium.org (2019-01-03)

This doesn't appear to need anything else, so marking as fixed. Please re-open if I am wrong.

### ke...@chromium.org (2019-01-03)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-01-04)

[Empty comment from Monorail migration]

### na...@google.com (2019-01-10)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### pa...@chromium.org (2019-01-10)

Thanks for your report. The panel has decided to reward $5,000 :) 



### na...@google.com (2019-01-10)

[Empty comment from Monorail migration]

### aw...@google.com (2019-02-15)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-04-12)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/917980?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093588)*
