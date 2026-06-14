# Check failed: !v8::internal::v8_flags.enable_slow_asserts.value() || (IsWasmExportedFunction(*this))

| Field | Value |
|-------|-------|
| **Issue ID** | [336399251](https://issues.chromium.org/issues/336399251) |
| **Status** | Accepted |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>WebAssembly |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ki...@gmail.com |
| **Assignee** | th...@chromium.org |
| **Created** | 2024-04-23 |
| **Bounty** | $8,000.00 |

## Description

# Steps to reproduce the problem

1. Download debug v8 from: gs://v8-asan/linux-debug/d8-linux-debug-v8-component-93481.zip
2. Run: `d8 --allow-natives-syntax --fuzzing poc.js`

# Problem Description

## INTRODUCE

After bisect, it was determined that following commit caused this problem.

- Commit Info
  - Version: 93460
  - link: <https://crrev.com/63a58875aea33190ef982d254d10f5700463f49a>
- Commit Message

```
commit 63a58875aea33190ef982d254d10f5700463f49a
Author: Thibaud Michaud <thibaudm@chromium.org>
Date:   Thu Apr 18 15:56:35 2024 +0200

    [wasm][jspi] Introduce WA.promising and WA.Suspending

    In the revised API, WebAssembly.promising and WebAssembly.Suspending
    replace WebAssembly.Function(..., {promising: 'first'}) and
    WebAssembly.Function(..., {suspending: 'first'}) respectively.

    WebAssembly.Suspending is a constructor. It returns a new object type
    which is not callable but can be imported into module.

    WebAssembly.promising returns a regular WasmExportedFunction.

    R=ahaas@chromium.org

    Bug: v8:14722
    Change-Id: I572b8d4bf0597a68dd31ac39241066156c6185ef
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5454695
    Reviewed-by: Andreas Haas <ahaas@chromium.org>
    Commit-Queue: Thibaud Michaud <thibaudm@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#93460}


```
## CRASH LOG

- Debug output

```
# CMD: /tmp/d8-linux-debug-v8-component-93481/d8 --allow-natives-syntax --fuzzing poc.js
# OUTPUT ==============================================================

#
# Fatal error in ../../src/wasm/wasm-objects-inl.h, line 356
# Check failed: !v8::internal::v8_flags.enable_slow_asserts.value() || (IsWasmExportedFunction(*this)).
#
#
#
#FailureMessage Object: 0x7ffd9193e960
==== C stack trace ===============================

    /tmp/d8-linux-debug-v8-component-93481/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x13) [0x7feb959f4d93]
    /tmp/d8-linux-debug-v8-component-93481/libv8_libplatform.so(+0x193cd) [0x7feb9599d3cd]
    /tmp/d8-linux-debug-v8-component-93481/libv8_libbase.so(V8_Fatal(char const*, int, char const*, ...)+0x17d) [0x7feb959d5f8d]
    /tmp/d8-linux-debug-v8-component-93481/libv8.so(+0x40e96b5) [0x7feb99ae96b5]
    /tmp/d8-linux-debug-v8-component-93481/libv8.so(+0x19a23de) [0x7feb973a23de]
Received signal 6


```
## Other

Please note to include the flags `--allow-natives-syntax --fuzzing` for clusterfuzz classification.

VERSION
Tested on v8 version: 12.6.0 - 12.6.0

# Summary

Check failed: !v8::internal::v8\_flags.enable\_slow\_asserts.value() || (IsWasmExportedFunction(\*this))

# Custom Questions

#### Type of crash:

tab

#### Reporter credit:

Zhenghang Xiao (@Kipreyyy)

# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: N/A

## Attachments

- [poc.js](attachments/poc.js) (text/javascript, 136 B)

## Timeline

### cl...@appspot.gserviceaccount.com (2024-04-23)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4910598069354496.

### 24...@project.gserviceaccount.com (2024-04-23)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the hotlistid:4801165.

### 24...@project.gserviceaccount.com (2024-04-23)

Automatically assigning owner based on suspected regression changelist https://chromium.googlesource.com/v8/v8/+/63a58875aea33190ef982d254d10f5700463f49a ([wasm][jspi] Introduce WA.promising and WA.Suspending).

If this is incorrect, please let us know why and apply the hotlistid:5433122. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### 24...@project.gserviceaccount.com (2024-04-23)

Detailed Report: https://clusterfuzz.com/testcase?key=4910598069354496

Fuzzer: None
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: CHECK failure
Crash Address: 
Crash State:
  !v8::internal::v8_flags.enable_slow_asserts.value() || (IsWasmExportedFunction(*
  v8::WebAssemblyPromising
  Builtins_CallApiCallbackGeneric
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=93459:93460

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=4910598069354496

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### th...@chromium.org (2024-04-24)

The poc uses

d8.test.enableJSPI();
d8.test.installConditionalFeatures();

which only exists in d8 and was added recently for the purposes of testing runtime-enabled OT features (in this case JSPI). This is not exploitable in V8 in the default configuration, so I don't think this classifies as a security issue (sroettger@ to confirm).

### th...@chromium.org (2024-04-24)

Discussed offline, this does classify as a security issue since it affects the JSPI OT. I am preparing the fix.

### ap...@google.com (2024-04-24)

Project: v8/v8
Branch: main

commit 9d4ca2a644156469f426f63c32cdd0c193de4691
Author: Thibaud Michaud <thibaudm@chromium.org>
Date:   Wed Apr 24 12:27:08 2024

    [wasm][jspi] Add missing return statement
    
    R=ahaas@chromium.org
    
    Bug: 336399251
    Change-Id: Iedfdc2c9355207b30d4b745e4b7cdfd899ec7341
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5481789
    Reviewed-by: Andreas Haas <ahaas@chromium.org>
    Commit-Queue: Thibaud Michaud <thibaudm@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#93552}

M       src/wasm/wasm-js.cc
M       test/mjsunit/wasm/stack-switching-new-api.js

https://chromium-review.googlesource.com/5481789


### pe...@google.com (2024-04-24)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2024-04-24)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security Impact hotlist or the Severity field, and remove the ReleaseBlock hotlist.

### 24...@project.gserviceaccount.com (2024-04-25)

ClusterFuzz testcase 4910598069354496 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=93551:93552

If this is incorrect, please add the hotlistid:5432646 and re-open the issue.

### sp...@google.com (2024-05-09)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $8000.00 for this report.

Rationale for this decision:
$7,000 for renderer / sandboxed process + $1,000 bisect bonus

Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. Two other things we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.
* If you are already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have already registered, there is no need to repeat the process and you’ll automatically be paid soon. If you have any payment related questions or issues, please reach out to p2p-vrp@google.com.

### pe...@google.com (2024-05-15)

This is sufficiently serious that it should be merged to dev. But I can't  see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M126. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Merge approved: your change passed merge requirements and is auto-approved for M126. Please go ahead and merge the CL to branch 6478 (refs/branch-heads/6478) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: harrysouders (Android), harrysouders (iOS), ceb (ChromeOS), srinivassista (Desktop)
Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [126].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


### th...@chromium.org (2024-05-16)

The fix (comment #8) already made it into 126, no merge is necessary.

### pe...@google.com (2024-05-20)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### pe...@google.com (2024-08-01)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/336399251)*
