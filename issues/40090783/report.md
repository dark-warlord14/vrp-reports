# Referrer Policy bypass using srcdoc

| Field | Value |
|-------|-------|
| **Issue ID** | [40090783](https://issues.chromium.org/issues/40090783) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>SecurityFeature>Referrer |
| **Platforms** | iOS |
| **Reporter** | s....@gmail.com |
| **Assignee** | aj...@google.com |
| **Created** | 2018-03-14 |
| **Bounty** | $1,000.00 |

## Description

Steps to reproduce the problem:
1. Go to https://test.shhnjk.com/refpola.php

What is the expected behavior?
No referrer is leaked to any resource.

What went wrong?
Referrer Policy doesn't get inherited to iframe srcdoc. To prove this, there are 2 frames. Frame 1 won't send referrer, but Frame 2 (the one with srcdoc) sends referrer.

Did this work before? N/A 

Chrome version: 65.0.3325.152  Channel: stable
OS Version: iOS 11.2.6
Flash Version:

## Timeline

### do...@chromium.org (2018-03-14)

I don't know if we have control over Referrer Policy on iOS. estark/droger, do you know?

[Monorail components: Blink>SecurityFeature>Referrer]

### es...@chromium.org (2018-03-14)

Nope, it's implemented in Blink and the net stack. We should do with this the same thing that we do with the CSP iOS bugs.

### pa...@chromium.org (2018-03-14)

[Empty comment from Monorail migration]

### es...@chromium.org (2018-03-16)

[Empty comment from Monorail migration]

### s....@gmail.com (2018-08-13)

This bug seems fixed in latest version of Chrome for iOS. Could anyone verify? Thanks!

### [Deleted User] (2020-10-30)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-31)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### jo...@chromium.org (2023-12-06)

Can you help me triage this? Not sure if this should go to Blink folks. 

### aj...@chromium.org (2023-12-06)

This is a really old bug, but I verified it's fixed. 

### [Deleted User] (2023-12-07)

[Empty comment from Monorail migration]

### am...@google.com (2024-02-02)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2024-02-02)

Congratulations, Jun! The Chrome VRP Panel has decided to award you $1,000 for this report of an exploitation mitigation bypass. While $500 may be an acceptable reward amount for this issue ;), please consider any overage as interest for this very old bug report. Cheers!  

### s....@gmail.com (2024-02-02)

Thanks Amy! Appreciate it!

### am...@google.com (2024-02-02)

[Empty comment from Monorail migration]

### is...@google.com (2024-02-02)

This issue was migrated from crbug.com/chromium/821626?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-03-14)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40090783)*
