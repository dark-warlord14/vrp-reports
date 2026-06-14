# Security: download protection bypass on macOS with .inetloc

| Field | Value |
|-------|-------|
| **Issue ID** | [40057339](https://issues.chromium.org/issues/40057339) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>Downloads |
| **Platforms** | Mac |
| **CVE IDs** | CVE-2021-38510 |
| **Reporter** | ho...@gmail.com |
| **Assignee** | dr...@chromium.org |
| **Created** | 2021-09-21 |
| **Bounty** | $500.00 |

## Description

**VERSION**  

Chrome Version: Version 93.0.4577.82 (Official Build) (arm64)  

Operating System: macOS Big Sur, 11.5.2

**REPRODUCTION CASE**  

Vladimir Metnew reported that .fileloc files on macOS can bypass download protection in 2019:<https://bugs.chromium.org/p/chromium/issues/detail?id=1029375>  

However, .inetloc files are similar to .fileloc files and .inetloc is not in blacklist.  

When download a .fileloc file in chrome, chrome will warn:"This type of file can harm your computer.Do you want to keep test.fileloc anyway?"  

But when download a .inetloc file in chrome there is no warning and if victim double click the .inetloc file they download then attacker may execute arbitrary commands.  

I provided a test.inetloc which can open calc for test.

## Attachments

- [test.inetloc](attachments/test.inetloc) (application/octet-stream, 295 B)

## Timeline

### [Deleted User] (2021-09-21)

[Empty comment from Monorail migration]

### aj...@google.com (2021-09-21)

drubery - it feels like this should be added to the list of dangerous file types for Mac.

[Monorail components: Services>Safebrowsing UI>Browser>Downloads]

### aj...@google.com (2021-09-21)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-21)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-21)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-22)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### va...@chromium.org (2021-09-24)

[Empty comment from Monorail migration]

### dr...@chromium.org (2021-09-24)

I agree that this is just a matter of changing the file type policy. We're currently running an experiment with that policy, so I'd prefer not to fix this until that experiment wraps up with M95 Stable. 

The risk here is pretty low, as we do contact Safe Browsing for these downloads. We just don't show a warning every time.

### dr...@chromium.org (2021-10-05)

[Empty comment from Monorail migration]

### dr...@chromium.org (2021-10-28)

The experiment is still ongoing, so continuing to push this.

### ho...@gmail.com (2021-11-26)

Same problem exists in firefox and the mozilla security advisory is here:
https://www.mozilla.org/en-US/security/advisories/mfsa2021-48/#CVE-2021-38510

### ho...@gmail.com (2021-12-29)

Hello, anyone here???

### gi...@appspot.gserviceaccount.com (2022-03-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/784abfd18c9b7e733ec6031ab02912f2ebd27aeb

commit 784abfd18c9b7e733ec6031ab02912f2ebd27aeb
Author: Daniel Rubery <drubery@chromium.org>
Date: Thu Mar 24 22:42:54 2022

Add inetloc to download_file_types.asciipb

This file type is comparable to webloc, so treat it the same way.

Fixed: 1251588
Change-Id: I311fa69bcf155eb2882ebb5706404a134f9fd857
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3549458
Auto-Submit: Daniel Rubery <drubery@chromium.org>
Reviewed-by: Xinghui Lu <xinghuilu@chromium.org>
Commit-Queue: Xinghui Lu <xinghuilu@chromium.org>
Cr-Commit-Position: refs/heads/main@{#985052}

[modify] https://crrev.com/784abfd18c9b7e733ec6031ab02912f2ebd27aeb/components/safe_browsing/content/resources/download_file_types.asciipb
[modify] https://crrev.com/784abfd18c9b7e733ec6031ab02912f2ebd27aeb/components/safe_browsing/content/resources/download_file_types_experiment.asciipb
[modify] https://crrev.com/784abfd18c9b7e733ec6031ab02912f2ebd27aeb/tools/metrics/histograms/enums.xml


### [Deleted User] (2022-03-27)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-27)

[Empty comment from Monorail migration]

### am...@google.com (2022-03-31)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-03-31)

Hello, thank you for reporting this issue to us. The Chrome VRP would like to extend a $500 thank you for this report. A member of our finance team will be in touch to arrange payment. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2022-04-01)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-05-24)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-05-24)

Hello OP, what is the name/handle/tag you would like us to use in acknowledging you for this issue? 

### ho...@gmail.com (2022-05-24)

Please use "hjy79425575". Thank you!

### am...@google.com (2022-05-24)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-07-21)

[Empty comment from Monorail migration]

### am...@google.com (2022-07-27)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-29)

[Empty comment from Monorail migration]

### is...@google.com (2022-07-29)

This issue was migrated from crbug.com/chromium/1251588?no_tracker_redirect=1

[Multiple monorail components: Services>Safebrowsing, UI>Browser>Downloads]
[Monorail blocked-on: crbug.com/chromium/1241961]
[Monorail mergedwith: crbug.com/chromium/1255337]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057339)*
