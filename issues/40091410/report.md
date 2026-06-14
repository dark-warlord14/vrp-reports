# Security: SpeechSynthesisEvent exposes high-resolution timestamps

| Field | Value |
|-------|-------|
| **Issue ID** | [40091410](https://issues.chromium.org/issues/40091410) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Privacy |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | md...@gmail.com |
| **Assignee** | ka...@chromium.org |
| **Created** | 2018-05-17 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**

SpeechSynthesisEvent#elapsedTime is specified to return the elapsed time in  

seconds since the associated SpeechSynthesisUtterance began playing to the user.  

Chrome instead returns the elapsed time in milliseconds.

Moreover, SpeechSynthesis::StartSpeakingImmediately and  

SpeechSynthesis::FireEvent (blink/renderer/modules/speech/speech\_synthesis.cc)  

draw the timestamps used to calculate the elapsed time value from  

CurrentTimeInSeconds, which returns a raw OS timestamp that bypasses the  

degradation of resolution applied to performance.now() post-Meltdown/Spectre. We  

have been able to observe timing precision of 5-7 microseconds via this route  

(vs the 20 microseconds exposed via performance.now).

Ideally, Chrome would have one designated API for obtaining a user-safe  

timestamp value, instead of applying the necessary filtering ad-hoc at the  

performance.now() API boundary.

**VERSION**

Chrome Version: 66.0.3359.181 stable  

Operating System: Windows 10 Pro Version 1709 (OS Build 16299.371)

**REPRODUCTION CASE**

`demo.html` compares time intervals extracted from the Web Speech API with ones  

obtained via performance.now()

## Attachments

- [demo.html](attachments/demo.html) (text/plain, 3.6 KB)

## Timeline

### el...@chromium.org (2018-05-17)

[Empty comment from Monorail migration]

### me...@chromium.org (2018-05-17)

Labeling low-severity as high-resolution timers aren't something that is exploitable on their own but are useful as part of timing-based attacks.

katie@ could you please take a look at this or suggest someone more suitable?

[Monorail components: Privacy]

### ka...@chromium.org (2018-05-18)

[Empty comment from Monorail migration]

### ka...@chromium.org (2018-05-18)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-05-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/cd32918faafeb42a02f6d47c41741cc11f43226d

commit cd32918faafeb42a02f6d47c41741cc11f43226d
Author: Katie D <katie@chromium.org>
Date: Fri May 25 19:52:44 2018

Use web-safe timestamps in window.speechSynthesis.

Tested to ensure that the values are the same magnitude as before the change.

Bug: 844195
Change-Id: I8f884e1535037741bc34186edcfb80ac3f96a2bd
Reviewed-on: https://chromium-review.googlesource.com/1066225
Reviewed-by: Dominic Mazzoni <dmazzoni@chromium.org>
Reviewed-by: Jonathan Metzman <metzman@chromium.org>
Commit-Queue: Katie Dektar <katie@chromium.org>
Cr-Commit-Position: refs/heads/master@{#561982}
[modify] https://crrev.com/cd32918faafeb42a02f6d47c41741cc11f43226d/third_party/blink/renderer/modules/speech/speech_synthesis.cc
[modify] https://crrev.com/cd32918faafeb42a02f6d47c41741cc11f43226d/third_party/blink/renderer/modules/speech/speech_synthesis.h


### ka...@chromium.org (2018-05-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-05-26)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-05-29)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-06-29)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@chromium.org (2018-06-29)

Thanks for the report, mdsmtp@. The VRP panel decided to award $500 for this. Cheers!

### aw...@chromium.org (2018-06-29)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-09-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2018-09-01)

This issue was migrated from crbug.com/chromium/844195?no_tracker_redirect=1

[Monorail blocking: crbug.com/chromium/798795]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091410)*
