# Security: SEGV_ACCERR in Maglev

| Field | Value |
|-------|-------|
| **Issue ID** | [40062816](https://issues.chromium.org/issues/40062816) |
| **Status** | Fixed |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Compiler>Maglev |
| **Platforms** | Linux, Mac, Windows |
| **Reporter** | p4...@gmail.com |
| **Assignee** | vi...@chromium.org |
| **Created** | 2023-01-28 |
| **Bounty** | $7,000.00 |

## Description

see details at https://crbug.com/chromium/1410970#c1

## Attachments

- [test.js](attachments/test.js) (text/plain, 1.1 KB)

## Timeline

### p4...@gmail.com (2023-01-28)

This template is ONLY for reporting security bugs. If you are reporting a
Download Protection Bypass bug, please use the "Security - Download
Protection" template. For all other reports, please use a different
template.

Please READ THIS FAQ before filing a bug: https://chromium.googlesource.com
/chromium/src/+/HEAD/docs/security/faq.md

Please see the following link for instructions on filing security bugs:
https://www.chromium.org/Home/chromium-security/reporting-security-bugs

Reports may be eligible for reward payments under the Chrome VRP:
http://g.co/ChromeBugRewards

NOTE: Security bugs are normally made public once a fix has been widely
deployed.

-------------------------

VULNERABILITY DETAILS
Please provide a brief explanation of the security issue.

The bug seems to be an issue in maglev arm64. 

The performance is writing to unmapped area in jit code.


VERSION
v8 Version: de36f16642a889cd054108fd696ac814e0a18e58
Operating System: all OS

REPRODUCTION CASE
Please include a demonstration of the security bug, such as an attached
HTML or binary file that reproduces the bug when loaded in Chrome. PLEASE
make the file as small as possible and remove any content not required to
demonstrate the bug, or any personal or confidential information.

Please attach files directly, not in zip or other archive formats, and if
you've created a demonstration site please also attach the files needed to
reproduce the demonstration locally.

run the attached file in arm64 d8 with commond line args "--interrupt-budget=1024 --maglev", it will crash at the Segmentation fault.


FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: tab
Crash State: 
 Received signal 11 SEGV_ACCERR 09b000000017
 ==== C stack trace ===============================
  [0x5580b6ac21f2]
  [0x7f6aabea93c0]
  [0x5580b8a94abf]
  [0x5580b8a8d74d]
  [0x5580b8a8d3c8]
  [0x5580b8a8c26f]
  [0x5580b8a8be92]
  [0x5580b70eeeb7]
  [0x5580b70f1c5d]
  [0x5580b6af2f70]
  [0x5580b69b0b91]
  [0x5580b69cfbe9]
  [0x5580b69d47c2]
  [0x5580b69d75a9]
  [0x7f6aabb350b3]
  [0x5580b697d02a]
 [end of stack trace]

### [Deleted User] (2023-01-28)

[Empty comment from Monorail migration]

### jg...@chromium.org (2023-01-30)

[Empty comment from Monorail migration]

### vi...@chromium.org (2023-01-30)

That seems to be an issue with OSRing Maglev->TF

### rs...@chromium.org (2023-01-31)

I cannot reproduce this on v8 head at 8131315998add278941cc23d12f2547d19c3d022 on an M1/arm64 Mac.

### p4...@gmail.com (2023-01-31)

[Comment Deleted]

### jg...@chromium.org (2023-01-31)

FYI crbug.com/1404279 (not yet fixed) is also related to ML-TF OSR.

### vi...@chromium.org (2023-01-31)

I can also repro, if one runs with `--no-turbo-inlining --interrupt-budget=1024 --maglev`, a DCHECK is thrown in a bytecode handler expecting a context, but it finds a Smi 2.

### vi...@chromium.org (2023-01-31)

Btw, the repro is a bit flaky.

### fl...@google.com (2023-01-31)

Setting Security_Impact-None because the bug occurs in a non-production configuration (maglev).

Setting Security_Impact-High because of arbitrary write in the JIT.

Assigning to jgruber@ because of maglev ownership.

### fl...@google.com (2023-01-31)

[Empty comment from Monorail migration]

### fl...@google.com (2023-01-31)

[Empty comment from Monorail migration]

### jg...@chromium.org (2023-02-01)

I think Victor was looking at this, reassigning.

### gi...@appspot.gserviceaccount.com (2023-02-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/12ecfa78cd57978caebda77ef40309ce89b97d8b

commit 12ecfa78cd57978caebda77ef40309ce89b97d8b
Author: Victor Gomes <victorgomes@chromium.org>
Date: Wed Feb 01 12:03:09 2023

[maglev] Remove BaselineAssembler dep from Maglev

We should not mix Baseline vs Maglev ScratchScope. x14 is considered
an extra-scratch register in arm64 for Baseline, but not for Maglev,
which has a more comprehensive way to allocate extra scratches.

Bug: v8:7700, chromium:1410970
Change-Id: Ia7eb77ff7fffc3c91d572931aa2ea001c90c1ffc
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4212388
Reviewed-by: Leszek Swirski <leszeks@chromium.org>
Auto-Submit: Victor Gomes <victorgomes@chromium.org>
Commit-Queue: Victor Gomes <victorgomes@chromium.org>
Cr-Commit-Position: refs/heads/main@{#85590}

[modify] https://crrev.com/12ecfa78cd57978caebda77ef40309ce89b97d8b/src/codegen/x64/macro-assembler-x64.h
[modify] https://crrev.com/12ecfa78cd57978caebda77ef40309ce89b97d8b/src/maglev/maglev-assembler.h
[modify] https://crrev.com/12ecfa78cd57978caebda77ef40309ce89b97d8b/src/codegen/arm64/macro-assembler-arm64.h
[modify] https://crrev.com/12ecfa78cd57978caebda77ef40309ce89b97d8b/src/maglev/arm64/maglev-assembler-arm64-inl.h
[modify] https://crrev.com/12ecfa78cd57978caebda77ef40309ce89b97d8b/src/maglev/x64/maglev-assembler-x64-inl.h
[modify] https://crrev.com/12ecfa78cd57978caebda77ef40309ce89b97d8b/src/baseline/arm64/baseline-assembler-arm64-inl.h
[modify] https://crrev.com/12ecfa78cd57978caebda77ef40309ce89b97d8b/src/baseline/x64/baseline-assembler-x64-inl.h
[modify] https://crrev.com/12ecfa78cd57978caebda77ef40309ce89b97d8b/src/codegen/arm64/macro-assembler-arm64.cc
[modify] https://crrev.com/12ecfa78cd57978caebda77ef40309ce89b97d8b/src/codegen/x64/macro-assembler-x64.cc
[modify] https://crrev.com/12ecfa78cd57978caebda77ef40309ce89b97d8b/src/maglev/DEPS
[modify] https://crrev.com/12ecfa78cd57978caebda77ef40309ce89b97d8b/src/maglev/maglev-ir.cc


### vi...@chromium.org (2023-02-01)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-01)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-01)

[Empty comment from Monorail migration]

### am...@google.com (2023-02-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-02-09)

Congratulations! The VRP Panel has decided to award you $7,000 for this report. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2023-02-10)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-10)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-05-10)

This issue was migrated from crbug.com/chromium/1410970?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062816)*
