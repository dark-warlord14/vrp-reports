# Security: type mismatch with jit,0 vs 65536

| Field | Value |
|-------|-------|
| **Issue ID** | [40064983](https://issues.chromium.org/issues/40064983) |
| **Status** | Fixed |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Compiler |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | be...@gmail.com |
| **Assignee** | ni...@chromium.org |
| **Created** | 2023-05-29 |
| **Bounty** | $7,000.00 |

## Description

Steps to reproduce the problem:
build flag:
gn gen out/fuzzbuild_new --args='is_debug=false dcheck_always_on=true v8_static_library=true v8_enable_slow_dchecks=true v8_enable_v8_checks=true v8_enable_verify_heap=true v8_enable_verify_csa=true v8_fuzzilli=true sanitizer_coverage_flags="trace-pc-guard" target_cpu="x64"'

environment:
Ubuntu 22.04.2 LTS 5.19.0-42-generic
v8 Version: commit c5677ca37541eb0d4672fe963cd237a0aec4f1fc 11.6.0

run with:
d8 --future --allow-natives-syntax poc.js

result will be:
[COV] no shared memory bitmap available, skipping
[COV] edge counters initialized. Shared memory: (null) with 1228626 edges
0
65536

and run with:
d8 --future --allow-natives-syntax -jitless poc.js
result will be:
[COV] no shared memory bitmap available, skipping
[COV] edge counters initialized. Shared memory: (null) with 1228626 edges
Warning: disabling flag --expose_wasm due to conflicting flags
0
0

## Attachments

- [poc.js](attachments/poc.js) (text/plain, 511 B)
- [mini.js](attachments/mini.js) (text/plain, 389 B)

## Timeline

### [Deleted User] (2023-05-29)

[Empty comment from Monorail migration]

### be...@gmail.com (2023-05-30)

[Empty comment from Monorail migration]

### ct...@chromium.org (2023-05-31)

I'm able to reproduce the different output with and without --jitless, but I'm not sure what the security consequences would be here. Notably, this appears to be similar to https://crbug.com/chromium/1448536 -- saelo@ could you take a look and check if there is any security risk to this difference between JIT and non-JIT execution?

[Monorail components: Blink>JavaScript>Compiler]

### sr...@google.com (2023-05-31)

[Empty comment from Monorail migration]

### sr...@google.com (2023-05-31)

This repros with `d8 --turboshaft --allow-natives-syntax poc.js` (thanks to cffsmith@ for pointing that out).

Marking as high for now since it looks like it might be the interesting kind of mismatch. But I haven't looked in detail to confirm.

### te...@chromium.org (2023-06-15)

[Empty comment from Monorail migration]

### ni...@chromium.org (2023-06-15)

Fixed by https://chromium-review.googlesource.com/c/v8/v8/+/4610200.

### [Deleted User] (2023-06-15)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-15)

[Empty comment from Monorail migration]

### am...@google.com (2023-06-24)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### wf...@chromium.org (2023-06-24)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-06-24)

Congratulations! The VRP Panel has decided to award you $7,000 for this report. A member of our finance team will be in touch with you soon to arrange payment. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2023-06-26)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-21)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### wh...@gmail.com (2023-09-22)

[Comment Deleted]

### is...@google.com (2023-09-22)

This issue was migrated from crbug.com/chromium/1449799?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/1451704]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40064983)*
