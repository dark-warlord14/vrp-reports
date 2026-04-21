# Security: Debug check failed: HasBytecodeArray()

| Field | Value |
|-------|-------|
| **Issue ID** | [40068825](https://issues.chromium.org/issues/40068825) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>JavaScript>Runtime, Blink>JavaScript>WebAssembly |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | dd...@gmail.com |
| **Assignee** | ah...@chromium.org |
| **Created** | 2023-08-05 |
| **Bounty** | $2,000.00 |

## Description

**This template is ONLY for reporting security bugs. If you are reporting a**  

**Download Protection Bypass bug, please use the "Security - Download**  

**Protection" template. For all other reports, please use a different**  

**template.**

**Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com>**  

**/chromium/src/+/HEAD/docs/security/faq.md**

**Please see the following link for instructions on filing security bugs:**  

**<https://www.chromium.org/Home/chromium-security/reporting-security-bugs>**

**Reports may be eligible for reward payments under the Chrome VRP:**  

**<http://g.co/ChromeBugRewards>**

**NOTE: Security bugs are normally made public once a fix has been widely**  

**deployed.**

**-------------------------**

**VULNERABILITY DETAILS**

# 

# Fatal error in ../../src/objects/shared-function-info-inl.h, line 606

# Debug check failed: HasBytecodeArray().

# 

# 

# 

#FailureMessage Object: 0x7f06e16acb40  

==== C stack trace ===============================

```
./out/fuzzbuild/d8(+0x7f9702) [0x56538868c702]  
./out/fuzzbuild/d8(+0x7f7e97) [0x56538868ae97]  
./out/fuzzbuild/d8(+0x7ea40f) [0x56538867d40f]  
./out/fuzzbuild/d8(+0x7e9d95) [0x56538867cd95]  
./out/fuzzbuild/d8(+0x72bb0b) [0x5653885beb0b]  
./out/fuzzbuild/d8(+0xd40a66) [0x565388bd3a66]  
./out/fuzzbuild/d8(+0xd6c178) [0x565388bff178]  
./out/fuzzbuild/d8(+0xd6990e) [0x565388bfc90e]  
./out/fuzzbuild/d8(+0xd6a715) [0x565388bfd715]  
./out/fuzzbuild/d8(+0xdd407c) [0x565388c6707c]  
./out/fuzzbuild/d8(+0x1b7ac91) [0x565389a0dc91]  
./out/fuzzbuild/d8(+0x1b7a582) [0x565389a0d582]  
./out/fuzzbuild/d8(+0x365c876) [0x56538b4ef876]  

```

Received signal 6  

Aborted (core dumped)

**VERSION**

commit 02729eeabf97bb1ec6238c6a460b57f893f464e4 (grafted, HEAD, origin/main)  

Author: v8-ci-autoroll-builder [v8-ci-autoroll-builder@chops-service-accounts.iam.gserviceaccount.com](mailto:v8-ci-autoroll-builder@chops-service-accounts.iam.gserviceaccount.com)  

Date: Fri Jul 28 21:02:42 2023 -0700

**REPRODUCTION CASE**  

build with debug and run the poc with

```
--expose-gc --allow-natives-syntax --future --turboshaft --maglev --shared-string-table  

```

## Attachments

- [poc.js](attachments/poc.js) (text/plain, 1.2 KB)
- [poc.js](attachments/poc.js) (text/plain, 1.3 KB)
- [poc.js](attachments/poc.js) (text/plain, 1.5 KB)

## Timeline

### [Deleted User] (2023-08-05)

[Empty comment from Monorail migration]

### dd...@gmail.com (2023-08-05)

and this one without %EnableCodeLoggingForTesting, but this poc not stable, need run multi time

### cl...@chromium.org (2023-08-05)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5074172449062912.

### cl...@chromium.org (2023-08-05)

ClusterFuzz testcase 5074172449062912 appears to be flaky, updating reproducibility label.

### cl...@chromium.org (2023-08-05)

Detailed Report: https://clusterfuzz.com/testcase?key=5074172449062912

Fuzzer: None
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  HasBytecodeArray() in shared-function-info-inl.h
  v8::internal::BytecodeArray v8::internal::SharedFunctionInfo::GetBytecodeArray<v
  v8::internal::FrameSummary::JavaScriptFrameSummary::AreSourcePositionsAvailable
  
Sanitizer: address (ASAN)

Crash Revision: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&revision=89386

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5074172449062912

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


************************* UNREPRODUCIBLE *************************
Note: This crash might not be reproducible with the provided testcase. That said, for the past 14 days, we've been seeing this crash frequently.

It may be possible to reproduce by trying the following options:
- Run testcase multiple times for a longer duration.
- Run fuzzing without testcase argument to hit the same crash signature.

If it still does not reproduce, try a speculative fix based on the crash stacktrace and verify if it works by looking at the crash statistics in the report. We will auto-close the bug if the crash is not seen for 14 days.
******************************************************************

### cl...@chromium.org (2023-08-05)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Blink>JavaScript>Runtime]

### dd...@gmail.com (2023-08-05)

Hi, the Regression of CF seems wrong because my local version not in that range. And which the flag is experimental? in my local version none of them is experimental
```
out/fuzzbuild/d8 --expose-gc --omit-quit --allow-natives-syntax --fuzzing --jit-fuzzing --future --turboshaft --maglev --shared-string-table
[COV] no shared memory bitmap available, skipping
[COV] edge counters initialized. Shared memory: (null) with 1162152 edges
V8 version 11.7.0 (candidate)
d8> 
```
And I have not try to reproduce it without --turboshaft --maglev, if need, I can try without experimental flag. Thank you : )


### dd...@gmail.com (2023-08-05)

Hi all, I have try to reproduce it and I succeed. it don't need any flag, just run it multi time and it can be reproduce.

REPRODUCE STEP

build with
```
is_debug = false
dcheck_always_on = true
v8_static_library = true
v8_enable_verify_heap = true
v8_fuzzilli = true
sanitizer_coverage_flags = "trace-pc-guard"
target_cpu = "x64"
```
and run the following poc.js for multi time and see the output



### cl...@chromium.org (2023-08-06)

Detailed Report: https://clusterfuzz.com/testcase?key=5074172449062912

Fuzzer: None
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  HasBytecodeArray() in shared-function-info-inl.h
  v8::internal::BytecodeArray v8::internal::SharedFunctionInfo::GetBytecodeArray<v
  v8::internal::FrameSummary::JavaScriptFrameSummary::AreSourcePositionsAvailable
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=89385:89386

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5074172449062912

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


************************* UNREPRODUCIBLE *************************
Note: This crash might not be reproducible with the provided testcase. That said, for the past 14 days, we've been seeing this crash frequently.

It may be possible to reproduce by trying the following options:
- Run testcase multiple times for a longer duration.
- Run fuzzing without testcase argument to hit the same crash signature.

If it still does not reproduce, try a speculative fix based on the crash stacktrace and verify if it works by looking at the crash statistics in the report. We will auto-close the bug if the crash is not seen for 14 days.
******************************************************************

### sr...@google.com (2023-08-07)

I bisected this to 00245a401bba15d76857385bb2787dc9057c4c79

### sr...@google.com (2023-08-07)

ahaas@ I was able to reproduce this with the args from https://crbug.com/chromium/1470434#c8. Sometimes it needs more than 100 tries though.

[Monorail components: Blink>JavaScript>WebAssembly]

### [Deleted User] (2023-08-07)

[Empty comment from Monorail migration]

### dd...@gmail.com (2023-08-07)

Thank you for bisect!

### ah...@chromium.org (2023-08-07)

[Empty comment from Monorail migration]

### ah...@chromium.org (2023-08-07)

The DCHECK was tricky to reproduce because it required an interrupt to be handled by the stack check of the js-to-wasm wrapper. This interrupt then terminated the execution of the worker, which then tried to generate a stack trace for the termination exception. The stack trace creation tried to access source positions of the js-to-wasm wrapper, which don't exist.
The fix is to mark the JSFunction of the js-to-wasm wrapper as not subject to debugging. CL is incoming.

### [Deleted User] (2023-08-07)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2023-08-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/8f99f563ecf03769c47d42de554664d2205d1bd8

commit 8f99f563ecf03769c47d42de554664d2205d1bd8
Author: Andreas Haas <ahaas@chromium.org>
Date: Mon Aug 07 16:46:45 2023

[wasm] JSToWasm wrapper is not subject to debugging

The JSToWasm was recently rewritten in Torque. Thereby the frame type
changed from JSToWasmFrame to TurbofanFrame. As a side effect, this
change made the JSToWasm wrapper subject to debugging. This side effect gets prevented by this CL by marking WasmExportedFunctions,
which contain the the JSToWasm wrapper, explicitly as not subject to
debugging.

R=clemensb@chromium.org

Bug: chromium:1470434
Change-Id: If47b908013004869a63d1bf1fbcceafc94a999a5
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4756856
Reviewed-by: Clemens Backes <clemensb@chromium.org>
Commit-Queue: Andreas Haas <ahaas@chromium.org>
Cr-Commit-Position: refs/heads/main@{#89424}

[modify] https://crrev.com/8f99f563ecf03769c47d42de554664d2205d1bd8/src/objects/shared-function-info-inl.h


### ah...@chromium.org (2023-08-08)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-08)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-08)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-08)

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M116. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ah...@chromium.org (2023-08-09)

1) https://chromium-review.googlesource.com/c/v8/v8/+/4756856
2) Yes
3) Yes
4) No
5) No

### [Deleted User] (2023-08-09)

Merge review required: M116 has already been cut for stable release.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: eakpobaro (Android), eakpobaro (iOS), obenedict (ChromeOS), danielyip (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sr...@google.com (2023-08-09)

Updating the severity since we believe this just turns into an info leak, i.e. reading a wrong source position.

### ah...@chromium.org (2023-08-09)

1) The severity is only low, so this change may not meet the merge criteria.
2) https://chromium-review.googlesource.com/c/v8/v8/+/4756856
3) Yes
4) No
5) No
6) No

### [Deleted User] (2023-08-09)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-08-11)

Generally info leaks are medium severity, but given that this is exceptionally not reliable to trigger, I think low is a accurate severity. 
In keeping with low severity fixes, I'm going to decline backmerging this. 

### dd...@gmail.com (2023-08-11)

Hi Amy@, in my local version the success rate more than 60% (I try first poc for four times and all success). And in https://crbug.com/chromium/1470434#c11, "sometimes it need more than 100 tries though " is not mean alway need 100 tries right?

### am...@chromium.org (2023-08-11)

Hello, your original POC and reprowas based on flags specific to experimental V8 features, which would not be considered security relevant nor meet our backmerge criteria. 
I'm going to take sroettger@ at their work in c#11 when he says it takes 100 times to reproduce, and while I'm not presuming that 100 is the exact number, this does not appear to reliably reproduce in a way that is not reliant on experimental features or non-default flags. 

### dd...@gmail.com (2023-08-11)

got it, thank you

### dd...@gmail.com (2023-08-19)

[Comment Deleted]

### dd...@gmail.com (2023-08-21)

[Comment Deleted]

### am...@google.com (2023-09-21)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-09-21)

Congratulations! The Chrome VRP Panel has decided to award you $2,000 for this report of a info leak. A member of our finance team will be in touch with you soon to arrange payment. In the meantime, please let us know what name or other identifier you would like us to use in acknowledging you for this finding. Thank you for your effort and reporting this issue to us! 

### dd...@gmail.com (2023-09-22)

thank you Amy. "ddme" for my id is ok : )

### am...@google.com (2023-09-22)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-14)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1470434?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>JavaScript>Runtime, Blink>JavaScript>WebAssembly]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40068825)*
