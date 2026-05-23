# Heap-use-after-free in color input on switching screens (MacOS)

| Field | Value |
|-------|-------|
| **Issue ID** | [40057634](https://issues.chromium.org/issues/40057634) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Forms>Color |
| **Platforms** | Mac |
| **Reporter** | dm...@gmail.com |
| **Assignee** | io...@microsoft.com |
| **Created** | 2021-10-18 |
| **Bounty** | $10,000.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0

Steps to reproduce the problem:
0. Prepare MacOS (my version: 11.6 (20G165)) with two spaces (https://support.apple.com/en-bh/guide/mac-help/mh14112/mac).
1. Download file "poc.html"
2. Open this file via command: `./Chromium poc.html`
3. Click color input.
4. Click on the custom color icon and switch to another space.
5. Back to space with Chromium.
6. Click anywhere.
7. Heap-use-after-free will be triggered.

What is the expected behavior?

What went wrong?
Check attached ASAN log.

Did this work before? N/A 

Chrome version: 97.0.4673.0 (Developer Build) (x86_64)  Channel: n/a
OS Version: OS X 10.15

I attach video with reproduce.

## Attachments

- [ASANReportHeapUaFInColorInput.txt](attachments/ASANReportHeapUaFInColorInput.txt) (text/plain, 12.9 KB)
- [ChromiumHeapUseAfterFreeInColorInput.mp4](attachments/ChromiumHeapUseAfterFreeInColorInput.mp4) (video/mp4, 8.5 MB)
- [poc.html](attachments/poc.html) (text/plain, 46 B)

## Timeline

### [Deleted User] (2021-10-18)

[Empty comment from Monorail migration]

### bd...@chromium.org (2021-10-18)

Assigning to iopopesc@ who has directly worked with EyeDropperView

[Monorail components: Blink>Forms>Color]

### ad...@google.com (2021-10-28)

Fixing spelling of "FoundIn-97" label. Also, as a browser process UaF this is high severity even if it involves substantial UI interaction (it would be Critical otherwise).

bdea: by adding FoundIn-97 you are stating that you could reproduce this on M97, but not on 94, 95 or 96, so this will be regarded as a regression and will block release of Chrome 97. If that's not correct please adjust the label to the earliest of those branches on which this is reproducible.

(In general it is really helpful if you can add a comment explaining the extent to which you have successfully reproduced bugs, before passing them onto developers.)

### [Deleted User] (2021-10-28)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-29)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-10-29)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### io...@microsoft.com (2021-10-29)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-10-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/5237981a0e2e1268788dfdb8ff2abadc2732686f

commit 5237981a0e2e1268788dfdb8ff2abadc2732686f
Author: Ionel Popescu <iopopesc@microsoft.com>
Date: Sat Oct 30 00:09:22 2021

Check if EyeDropperViewMac object is alive when NSColorSampler handler is called.

Since currently there is no way to dismiss NSColorSampler, we need
to check if the EyeDropperViewMac object is still alive when
its handler is called.

Bug: 1260858
Change-Id: Idc575cd2147e6af2f181fd1df7bc3374d9d6f1aa
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3253456
Commit-Queue: Ionel Popescu <iopopesc@microsoft.com>
Reviewed-by: Mason Freed <masonf@chromium.org>
Cr-Commit-Position: refs/heads/main@{#936619}

[modify] https://crrev.com/5237981a0e2e1268788dfdb8ff2abadc2732686f/chrome/browser/ui/views/eye_dropper/eye_dropper_view_mac.mm
[modify] https://crrev.com/5237981a0e2e1268788dfdb8ff2abadc2732686f/chrome/browser/ui/views/eye_dropper/eye_dropper_view_mac.h


### io...@microsoft.com (2021-10-30)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-30)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-30)

[Empty comment from Monorail migration]

### am...@google.com (2021-11-03)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-11-03)

Congratulations! The VRP Panel has decided to award you $10,000 for this report. Thank you for your report and nice work! 

### am...@google.com (2021-11-04)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-07)

Not requesting merge to dev (M97) because latest trunk commit (936619) appears to be prior to dev branch point (938553). If this is incorrect, please replace the Merge-NA-97 label with Merge-Request-97. If other changes are required to fix this bug completely, please request a merge if necessary.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-02-05)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1260858?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1264427]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057634)*
