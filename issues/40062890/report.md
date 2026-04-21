# type mismatch with turboshaft,1 vs NaN

| Field | Value |
|-------|-------|
| **Issue ID** | [40062890](https://issues.chromium.org/issues/40062890) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Compiler>Turbofan |
| **Platforms** | Windows |
| **Reporter** | 5n...@gmail.com |
| **Assignee** | ni...@chromium.org |
| **Created** | 2023-02-03 |
| **Bounty** | $7,000.00 |

## Description

**Steps to reproduce the problem:**  

v8 version:head  

build flag:  

gn gen out/x64\_release --args="target\_cpu="x64" symbol\_level=2 is\_debug=false is\_component\_build=false v8\_enable\_backtrace = true v8\_enable\_disassembler=true v8\_enable\_object\_print=true"

run arg:  

--allow-natives-syntax --turboshaft

**Problem Description:**  

Running with "--allow-natives-syntax --jitless --turboshaft",before\_jit is the same with after\_jit.However running with "--allow-natives-syntax --turboshaft",before\_jit is not same with after\_jit,before\_jit=1 vs after\_jit=NaN.

**Additional Comments:**

\*\*Chrome version: \*\* 109.0.0.0 \*\*Channel: \*\* Not sure

**OS:** Windows

## Attachments

- [11.js](attachments/11.js) (text/plain, 524 B)
- [minimized.js](attachments/minimized.js) (text/plain, 369 B)

## Timeline

### [Deleted User] (2023-02-03)

[Empty comment from Monorail migration]

### 5n...@gmail.com (2023-02-03)

[Comment Deleted]

### 5n...@gmail.com (2023-02-03)

Add minimized poc

### fl...@google.com (2023-02-03)

Setting Security_Impact-None because Turboshaft is still experimental.

Passing to the Turboshaft folks for further analysis.

[Monorail components: Blink>JavaScript>Compiler>Turbofan]

### fl...@google.com (2023-02-03)

[Empty comment from Monorail migration]

### ec...@chromium.org (2023-02-05)

@mslekova, @nicohartmann: Could one of you look into this? Thanks!

### ni...@chromium.org (2023-02-06)

I'll take a look.

### gi...@appspot.gserviceaccount.com (2023-02-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/6d2bd5afdc2e4dc0bbf8cf20c851ddce30e0702d

commit 6d2bd5afdc2e4dc0bbf8cf20c851ddce30e0702d
Author: Nico Hartmann <nicohartmann@chromium.org>
Date: Mon Feb 06 13:26:39 2023

[turboshaft] Fix typing of NaN ** 0

Bug: v8:12783, chromium:1412629
Change-Id: If00a7467443df50cd2c79b3bb09f9dd92dd0548b
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4221773
Auto-Submit: Nico Hartmann <nicohartmann@chromium.org>
Commit-Queue: Jakob Kummerow <jkummerow@chromium.org>
Reviewed-by: Jakob Kummerow <jkummerow@chromium.org>
Cr-Commit-Position: refs/heads/main@{#85687}

[add] https://crrev.com/6d2bd5afdc2e4dc0bbf8cf20c851ddce30e0702d/test/mjsunit/regress/regress-1412629.js
[modify] https://crrev.com/6d2bd5afdc2e4dc0bbf8cf20c851ddce30e0702d/src/compiler/turboshaft/types.h
[modify] https://crrev.com/6d2bd5afdc2e4dc0bbf8cf20c851ddce30e0702d/src/compiler/turboshaft/type-inference-reducer.h


### fl...@google.com (2023-02-07)

[Empty comment from Monorail migration]

### ni...@chromium.org (2023-02-08)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-08)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-08)

[Empty comment from Monorail migration]

### am...@google.com (2023-02-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-02-17)

Congratulations! The VRP Panel has decided to award you $7,000 for this report. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2023-02-18)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-17)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-05-17)

This issue was migrated from crbug.com/chromium/1412629?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062890)*
