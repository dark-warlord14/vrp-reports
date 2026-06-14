# Dangerous file extension: BGI

| Field | Value |
|-------|-------|
| **Issue ID** | [40738834](https://issues.chromium.org/issues/40738834) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P4 |
| **Component** | UI>Browser>Downloads |
| **Platforms** | Windows |
| **Reporter** | do...@gmail.com |
| **Assignee** | dr...@chromium.org |
| **Created** | 2020-12-23 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36

Steps to reproduce the problem:
POC BGI: https://drive.google.com/file/d/1CJoROZv2lIKCWluWz8gqYQNlomT5_y_O/view
you can download it with chrome with no warning. 
It will open calc.exe on computer with BGINFO installed. 

What is the expected behavior?

What went wrong?
The file extension: BGI could lead to RCE on machine with BGINFO installed. 
This file type is dangerous and should alert the user before downloading (same as script files like: ps1, bat, etc..)

for more details you can read the blog I wrote:

https://www.varonis.com/blog/exploiting-bginfo-to-infiltrate-a-corporate-network/

Did this work before? No 

Chrome version: 87.0.4280.88  Channel: stable
OS Version: 10.0
Flash Version:

## Timeline

### [Deleted User] (2020-12-23)

[Empty comment from Monorail migration]

### aj...@google.com (2020-12-23)

Thanks. To be clear the user will still need to double-click the downloaded bginfo file and have bginfo in their path? If so this is the same as a user double-clicking an executable and is something we'd leave to the operating system or Defender to deal with.

### pa...@chromium.org (2020-12-23)

#2: Yes, that is the case with all our Dangerous Download types. We still want to warn people that the file type poses such risk.

[Monorail components: UI>Browser>Downloads]

### do...@gmail.com (2020-12-24)

yes, this one need to be double clicked in order to run. (but no need BGINFO in the path, just one time run and it automatically associate BGI extension with its executable.)
And I am agree that this file type need to be warning as other dangerous file types. 

### [Deleted User] (2020-12-24)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aj...@google.com (2020-12-24)

Thanks. This should probably be treated the same as other dangerous file types.

Assigning Low as this requires user to click & particular software to be installed.

### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### bd...@chromium.org (2021-02-03)

[Empty comment from Monorail migration]

[Monorail components: Services>Safebrowsing]

### [Deleted User] (2021-02-04)

[Empty comment from Monorail migration]

### xi...@chromium.org (2021-02-12)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-11)

[Empty comment from Monorail migration]

### zh...@google.com (2021-03-17)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-01-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/54783fe5e971fed4bed695b46025682521d5df65

commit 54783fe5e971fed4bed695b46025682521d5df65
Author: Daniel Rubery <drubery@chromium.org>
Date: Wed Jan 18 00:17:33 2023

Add BGI to file type policy

This file type can lead to code execution on machines with BGINFO
installed. BGINFO is part of Sysinternals, so it's likely common
enough to justify an entry in the file type policy config.

This CL adds BGI at danger level ALLOW_ON_USER_GESTURE, since it does
not meet the requirements for DANGEROUS.

Fixed: 1161456
Change-Id: Ifb08fc5c6c7c8c8c6f7ec969b45ae652acdcf562
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4166265
Reviewed-by: Xinghui Lu <xinghuilu@chromium.org>
Commit-Queue: Daniel Rubery <drubery@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1093627}

[modify] https://crrev.com/54783fe5e971fed4bed695b46025682521d5df65/components/safe_browsing/content/resources/download_file_types.asciipb
[modify] https://crrev.com/54783fe5e971fed4bed695b46025682521d5df65/components/safe_browsing/content/resources/download_file_types_experiment.asciipb
[modify] https://crrev.com/54783fe5e971fed4bed695b46025682521d5df65/tools/metrics/histograms/enums.xml


### [Deleted User] (2023-01-18)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-18)

[Empty comment from Monorail migration]

### va...@chromium.org (2023-01-26)

[Empty comment from Monorail migration]

### am...@google.com (2023-01-26)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-01-27)

Thank you for this report. While we don't consider this to be a security bug in Chrome's threat model, but more of a change to a security feature, we did want to thank you for this report. As such, we would like to extend to you a $500 VRP reward. A member of our finance team will be in touch with you soon to arrange payment. Thank you for your efforts! 

### am...@google.com (2023-01-28)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-03-06)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-26)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-04-26)

This issue was migrated from crbug.com/chromium/1161456?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Services>Safebrowsing, UI>Browser>Downloads]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40738834)*
