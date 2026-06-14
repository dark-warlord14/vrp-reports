# Sig11 in wasm

| Field | Value |
|-------|-------|
| **Issue ID** | [40095591](https://issues.chromium.org/issues/40095591) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>JavaScript>WebAssembly |
| **Platforms** | Linux |
| **Reporter** | cd...@gmail.com |
| **Assignee** | cl...@chromium.org |
| **Created** | 2019-07-03 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36

Steps to reproduce the problem:
Steps to reproduce the problem:
1. Build asan 77.0.3835.0 version of chrome.
2. Put  js into the same dir with poc.html and setup a webserver.
3. Run chrome --js-flags="--wasm-code-gc"  poc.html

What is the expected behavior?

What went wrong?
Can get sig11 crash stably.

Seems like that multi-thread compiling wasm code could let the RegisterHandlerData(v8/src/trap-handler/handler-outside.cc:133) for protected code to be later than handling a segment fault signal(v8/src/trap-handler/handler-inside-posix.cc:74).

So the gCodeObjects could not contain the error RIP and when error RIP execution raised the sig11 the check(v8/src/trap-handler/handler-inside.cc:37) for the RIP won't return true.
Then crash happened. The log:

Received signal 11 SEGV_ACCERR 101f8ce03ffe
#0 0x7efc7ee18929 base::debug::CollectStackTrace()
#1 0x7efc7ed51393 base::debug::StackTrace::StackTrace()
#2 0x7efc7ee18431 base::debug::(anonymous namespace)::StackDumpSignalHandler()
#3 0x7efc61447390 <unknown>
#4 0x3d6f07f892d0 <unknown>
  r8: 0000000000000029  r9: 000015b3a4e804d1 r10: 000035c569251369 r11: 0000343def9de489
 r12: 0000000000000101 r13: 000035c569319080 r14: 0000343def9de489 r15: 000035c569362410
  di: 000019c134514301  si: 000019c134514149  bp: 00007ffc5d727718  bx: 0000101e8ce00000
  dx: 00000000ffffffff  ax: 0000000000000000  cx: 00003d6f07f89000  sp: 00007ffc5d727708
  ip: 00003d6f07f892d0 efl: 0000000000010206 cgf: 002b000000000033 erf: 0000000000000004
 trp: 000000000000000e msk: 0000000000000000 cr2: 0000101f8ce03ffe
[end of stack trace]
Calling _exit(1). Core file will not be generated.

Did this work before? N/A 

Chrome version: 77.0.3838.0  Channel: n/a
OS Version: 16.04
Flash Version:

## Attachments

- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)

## Timeline

### li...@chromium.org (2019-07-03)

Tentatively setting labels and punting to v8 sheriff to help triage. clemensh, would you be able to help take a look? Thanks!

[Monorail components: Blink>JavaScript>WebAssembly]

### sh...@chromium.org (2019-07-04)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cl...@chromium.org (2019-07-05)

Cannot reproduce, but probably the same root cause as https://crbug.com/v8/9375. I have a fix which will land soon.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-07-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/e9d93babca1b9b8c88b09724757b84378bbd3500

commit e9d93babca1b9b8c88b09724757b84378bbd3500
Author: Clemens Hammacher <clemensh@chromium.org>
Date: Fri Jul 05 12:44:41 2019

[wasm] Register trap handler data early enough

Registration of trap handler data has to happen *before* updating the
jump table, otherwise other threads might start using the code right
away, and if they hit a memory OOB, they just segfault if the trap
handlers have not been registered yet.

R=ahaas@chromium.org

Bug: v8:9375, chromium:980843
Change-Id: Ifac5c0681ce133b7af730a87beaede9d3c223f50
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/1687414
Reviewed-by: Andreas Haas <ahaas@chromium.org>
Commit-Queue: Clemens Hammacher <clemensh@chromium.org>
Cr-Commit-Position: refs/heads/master@{#62535}

[modify] https://crrev.com/e9d93babca1b9b8c88b09724757b84378bbd3500/src/wasm/wasm-code-manager.cc


### cl...@chromium.org (2019-07-05)

Probably fixed, please confirm.

### sh...@chromium.org (2019-07-05)

[Empty comment from Monorail migration]

### na...@google.com (2019-07-15)

[Empty comment from Monorail migration]

### aw...@google.com (2019-07-31)

Hi clemensh@ - the VRP panel wondered if this report was useful in the fix, or if Bug: v8:9375 was sufficient to ensure we'd fix it?

### cl...@chromium.org (2019-08-01)

Hi Andrew,

this report contained a nice description of what is actually happening, which reduced the time for me to debug the issue.
v8:9375 would probably have resulted in the same fix, so this report was not crucial.

Hope this helps!

### na...@google.com (2019-08-21)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### pa...@chromium.org (2019-08-21)

Congrats! The Panel decided to reward $500 as a thank you for helping debug this issue. 

### na...@google.com (2019-08-21)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-10-12)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cl...@chromium.org (2020-02-17)

[Empty comment from Monorail migration]

### is...@google.com (2020-02-17)

This issue was migrated from crbug.com/chromium/980843?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095591)*
