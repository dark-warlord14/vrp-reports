# Security: Navigating to "chrome://" URLs via 'about:' protocol

| Field | Value |
|-------|-------|
| **Issue ID** | [40085160](https://issues.chromium.org/issues/40085160) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>Navigation |
| **Platforms** | iOS |
| **Reporter** | ma...@gmail.com |
| **Assignee** | eu...@chromium.org |
| **Created** | 2016-08-21 |
| **Bounty** | $500.00 |

## Description

Steps to reproduce the problem:
1. Open the PoC.html
<a href="about:history-frame" target="x" onclick="setTimeout('d()', 2000);">Click Me</a>

Or you could visit the online PoC page:
http://115.159.58.203/chrome/poc.html

2. You will find the Chrome iOS version opened a new window and navigated to "chrome://". But according to the Chrome desktop version, I could not find the same behavior. 

What is the expected behavior?

What went wrong?
There have been similar issues in the Chrome 44.0.2403.157 stable and Chrome 49.0.2623.87. 
https://bugs.chromium.org/p/chromium/issues/detail?id=528505
https://bugs.chromium.org/p/chromium/issues/detail?id=595514

But the PoC I offered above bypassed the patch imposed on the Chrome iOS version.

Did this work before? N/A 

Chrome version: 52.0.2743.84  Channel: stable
OS Version: iOS 9.3.3
Flash Version: Shockwave Flash 22.0 r0

## Attachments

- [PoC.html](attachments/PoC.html) (text/plain, 88 B)

## Timeline

### ji...@chromium.org (2016-08-22)

+eugenebut@, since you are the owner of https://bugs.chromium.org/p/chromium/issues/detail?id=595514.
Could you help triage this issue? Please feel free to suggest other owner. 

[Monorail components: UI>Browser>Navigation]

### cr...@chromium.org (2016-08-22)

This should probably be higher severity, as it's similar to https://crbug.com/chromium/604086.  That one was rated Security_Severity-Medium.

### eu...@chromium.org (2016-08-22)

creis@, just FYI: 604086 allowed to load WebUI url in the same window (and same web process). This bug allows a WebUI child window which is run in a separate process. 

### eu...@chromium.org (2016-08-22)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-08-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/5bdbf8b4a257e3264644900234c1d31126394c5f

commit 5bdbf8b4a257e3264644900234c1d31126394c5f
Author: eugenebut <eugenebut@chromium.org>
Date: Tue Aug 23 21:11:29 2016

[ios] Do not allow WebUI URLs for windows open by DOM.

BUG=639658

Review-Url: https://codereview.chromium.org/2268053002
Cr-Commit-Position: refs/heads/master@{#413834}

[modify] https://crrev.com/5bdbf8b4a257e3264644900234c1d31126394c5f/ios/web/web_state/ui/crw_web_controller.mm


### eu...@chromium.org (2016-08-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-08-24)

[Empty comment from Monorail migration]

### ma...@gmail.com (2016-08-26)

Reward-topanel?

### mb...@chromium.org (2016-08-26)

Sure, we can take this to the reward panel to review. Ultimately it's up to them to determine if this qualifies for a reward. Low severity issues are usually case-by-case, and don't necessarily qualify.

### aw...@chromium.org (2016-10-10)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-11)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-15)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-15)

Congratulations, the panel awarded $500 for this bug.  A member of our finance team will be in touch shortly.

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an established charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@chromium.org (2016-10-16)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-16)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-11-30)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/639658?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40085160)*
