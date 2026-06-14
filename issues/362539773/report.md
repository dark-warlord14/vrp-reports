# Debug check failed: HasWasmExportedFunctionData(). in v8

| Field | Value |
|-------|-------|
| **Issue ID** | [362539773](https://issues.chromium.org/issues/362539773) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Runtime, Blink>JavaScript>WebAssembly |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ki...@gmail.com |
| **Assignee** | th...@chromium.org |
| **Created** | 2024-08-28 |
| **Bounty** | $7,000.00 |

## Description

VULNERABILITY DETAILS
## INTRODUCE
After bisect, it was determined that following commit caused this problem.

- Commit Info
    - Version: 92983
    - link: https://crrev.com/0c2b15100d997a8f1b74fcc448da319c75f2e045 
- Commit Message

```
commit 0c2b15100d997a8f1b74fcc448da319c75f2e045
Author: Adam Klein <adamk@chromium.org>
Date:   Thu Mar 21 13:36:59 2024 -0700

    [wasm][jspi][d8] Add ability to test runtime-enabling of JSPI
    
    This adds an `enableJSPI` function to the d8 test runner which
    allows simulating the way the JSPI Origin Trial in Chrome enables JSPI.
    
    Then it makes a copy of the JSPI mjsunit test to use this approach,
    rather than using a commandline flag.
    
    Bug: v8:14576
    Change-Id: I637972dcf7de288d42b1325355b08c6b1b86d9ef
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5385244
    Reviewed-by: Francis McCabe <fgm@chromium.org>
    Commit-Queue: Adam Klein <adamk@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#92983}

```

## CRASH LOG
- Debug output

```bash
# CMD: /tmp/d8-linux-debug-v8-component-95842/d8 --allow-natives-syntax --jit-fuzzing poc.js
# OUTPUT ==============================================================


#
# Fatal error in ../../src/objects/shared-function-info-inl.h, line 911
# Debug check failed: HasWasmExportedFunctionData().
#
#
#
#FailureMessage Object: 0x7ffd2b60ead0
==== C stack trace ===============================

    /tmp/d8-linux-debug-v8-component-95842/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x13) [0x7f831d74b153]
    /tmp/d8-linux-debug-v8-component-95842/libv8_libplatform.so(+0x199ed) [0x7f831d6f39ed]
    /tmp/d8-linux-debug-v8-component-95842/libv8_libbase.so(V8_Fatal(char const*, int, char const*, ...)+0x194) [0x7f831d72c854]
    /tmp/d8-linux-debug-v8-component-95842/libv8_libbase.so(+0x2c265) [0x7f831d72c265]
    /tmp/d8-linux-debug-v8-component-95842/libv8.so(v8::internal::SharedFunctionInfo::wasm_exported_function_data(v8::internal::PtrComprCageBase) const+0xa3) [0x7f831a87b143]
    /tmp/d8-linux-debug-v8-component-95842/libv8.so(+0x3ffb012) [0x7f831bdfb012]
    /tmp/d8-linux-debug-v8-component-95842/libv8.so(+0x3fda1fb) [0x7f831bdda1fb]
    /tmp/d8-linux-debug-v8-component-95842/libv8.so(v8::internal::Runtime_WasmCompileWrapper(int, unsigned long*, v8::internal::Isolate*)+0x90) [0x7f831bdd9a30]
    /tmp/d8-linux-debug-v8-component-95842/libv8.so(+0x1f65dd7) [0x7f8319d65dd7]

```

## Other
Please note to include the flags `--allow-natives-syntax --jit-fuzzing` for clusterfuzz classification.

VERSION
Tested on v8 version: 12.5.0 - 13.0.0

REPRODUCTION CASE
1. Download debug v8 from: gs://v8-asan/linux-debug/d8-linux-debug-v8-component-95842.zip
2. Run: `d8 --allow-natives-syntax --jit-fuzzing poc.js`

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: tab

CREDIT INFORMATION
Reporter credit: Zhenghang Xiao (@Kipreyyy)    

## Attachments

- [poc.js](attachments/poc.js) (text/javascript, 802 B)

## Timeline

### ti...@chromium.org (2024-08-28)

(security shepherd)

Was able to reproduce, assigning to cffsmith@ (current V8 security shepherd) sev=high / P1 because it looks like it would lead to a type confusion [1]

[1] <https://source.chromium.org/chromium/chromium/src/+/main:v8/src/objects/shared-function-info-inl.h;l=914;drc=82dff63dbf9db05e9274e11d9128af7b9f51ceaa>

### cl...@appspot.gserviceaccount.com (2024-08-28)

Detailed Report: https://clusterfuzz.com/testcase?key=5115795059179520

Fuzzer: None
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  HasWasmExportedFunctionData() in shared-function-info-inl.h
  v8::internal::SharedFunctionInfo::wasm_exported_function_data
  v8::internal::ReplaceWrapper
  
Sanitizer: address (ASAN)

Crash Revision: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&revision=95854

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5115795059179520

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### pe...@google.com (2024-08-28)

Setting milestone because of s0/s1 severity.

### ki...@gmail.com (2024-08-29)

please assign owner to fix this issue

### cf...@google.com (2024-08-29)

Assigning to thibaudm@ to take a look or find the right owner.

### th...@chromium.org (2024-08-29)

Re-exporting a WebAssembly.Function import creates a special case that is not correctly handled by the js-to-wasm wrapper tier-up logic. More specifically we try to set the new wrapper for all exports with the same signature, but WebAssembly.Function re-exported imports do not need the new wrapper (they are called directly via the js-to-js wrapper) and they don't have the expected function data type (which is what causes the crash).
We should just handle this special case and skip these exports in the tier-up runtime function.

### ap...@google.com (2024-08-29)

Project: v8/v8
Branch: main

commit 7860c9605e30623eb81129250790aa44757f0e4b
Author: Thibaud Michaud <thibaudm@chromium.org>
Date:   Thu Aug 29 14:56:57 2024

    [wasm] Skip WasmJSFunctions in js-to-wasm wrapper tier-up
    
    When a js-to-wasm wrapper tiers up, we also set the newly compiled
    wrapper as the target for other exports that have the same signature.
    This assumed that all exports have type WasmExportedFunction, but they
    can also have type WasmJSFunction in the case of a re-exported
    WebAssembly.Function import.
    
    R=clemensb@chromium.org
    
    Fixed: 362539773
    Change-Id: I190a680ac5726122e2124977668bba3a95df93b5
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5822928
    Reviewed-by: Clemens Backes <clemensb@chromium.org>
    Commit-Queue: Thibaud Michaud <thibaudm@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#95877}

M       src/runtime/runtime-wasm.cc

https://chromium-review.googlesource.com/5822928


### ap...@google.com (2024-08-29)

Project: v8/v8
Branch: main

commit 76b279609a9450c95e6315fe473980c63449f391
Author: Thibaud Michaud <thibaudm@chromium.org>
Date:   Thu Aug 29 16:24:50 2024

    [wasm] Remove flag implication between JSPI and type reflection
    
    The deprecated JSPI API based on the WebAssembly.Function constructor
    was removed from V8. The new API does not depend on the type reflection
    proposal, so remove the flag implication.
    
    R=clemensb@chromium.org
    
    Bug: 362539773,42202153
    Change-Id: I2f0ec66c542197a7e86ef1742abb74302ab1d05d
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5822930
    Commit-Queue: Thibaud Michaud <thibaudm@chromium.org>
    Reviewed-by: Clemens Backes <clemensb@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#95878}

M       src/flags/flag-definitions.h
M       src/wasm/wasm-features.cc
M       test/mjsunit/wasm/stack-switching.js
M       test/unittests/api/api-wasm-unittest.cc

https://chromium-review.googlesource.com/5822930


### pe...@google.com (2024-08-29)

Security Merge Request Consideration: Not requesting merge to stable (M128) because latest trunk commit (95878) appears to be prior to stable branch point (1331488). If this is incorrect please remove NA-128 from the 'Merge' field and add 128 to the 'Merge-Request' field If other changes are required to fix this bug completely please request a merge if necessary.
Security Merge Request Consideration: Not requesting merge to beta (M129) because latest trunk commit (95878) appears to be prior to beta branch point (1343869). If this is incorrect please remove NA-129 from the 'Merge' field and add 129 to the 'Merge-Request' field If other changes are required to fix this bug completely please request a merge if necessary.
Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### ap...@google.com (2024-08-29)

Project: v8/v8
Branch: main

commit 46dfd106f935c5afa1320ebdb0870be526f37ef0
Author: Matthias Liedtke <mliedtke@chromium.org>
Date:   Thu Aug 29 16:08:10 2024

    Revert "[wasm] Remove flag implication between JSPI and type reflection"
    
    This reverts commit 76b279609a9450c95e6315fe473980c63449f391.
    
    Reason for revert: Test failures on Blink:
    Chrome tests seem to expect that type reflection is available?
    https://ci.chromium.org/ui/p/v8/builders/ci/V8%20Blink%20Linux/32790/overview
    e.g. https://luci-milo.appspot.com/ui/inv/build-8738257798077045169/test-results?q=external%2Fwpt%2Fwasm%2Fjsapi%2Ftable%2Ftype.tentative.any.worker.html&sortby=&groupby=
    
    Original change's description:
    > [wasm] Remove flag implication between JSPI and type reflection
    >
    > The deprecated JSPI API based on the WebAssembly.Function constructor
    > was removed from V8. The new API does not depend on the type reflection
    > proposal, so remove the flag implication.
    >
    > R=clemensb@chromium.org
    >
    > Bug: 362539773,42202153
    > Change-Id: I2f0ec66c542197a7e86ef1742abb74302ab1d05d
    > Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5822930
    > Commit-Queue: Thibaud Michaud <thibaudm@chromium.org>
    > Reviewed-by: Clemens Backes <clemensb@chromium.org>
    > Cr-Commit-Position: refs/heads/main@{#95878}
    
    Bug: 362539773,42202153
    Change-Id: I445fd7e656faec214b99e36e13b3209e5813a132
    No-Presubmit: true
    No-Tree-Checks: true
    No-Try: true
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5824994
    Commit-Queue: Matthias Liedtke <mliedtke@chromium.org>
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Cr-Commit-Position: refs/heads/main@{#95880}

M       src/flags/flag-definitions.h
M       src/wasm/wasm-features.cc
M       test/mjsunit/wasm/stack-switching.js
M       test/unittests/api/api-wasm-unittest.cc

https://chromium-review.googlesource.com/5824994


### 24...@project.gserviceaccount.com (2024-08-30)

ClusterFuzz testcase 5115795059179520 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=95876:95877

If this is incorrect, please add the hotlistid:5433040 and re-open the issue.

### th...@google.com (2024-08-30)

1. https://chromium-review.googlesource.com/5822928
2. Reached canary today (130.0.6687.0)
3. No
4. No
5. No

### pe...@google.com (2024-08-30)

Merge review required: M129 is already shipping to beta.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), govind (iOS), matthewjoseph (ChromeOS), srinivassista (Desktop)

### pe...@google.com (2024-08-30)

Merge review required: M128 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: harrysouders (Android), harrysouders (iOS), obenedict (ChromeOS), pbommana (Desktop)

### th...@google.com (2024-08-30)

1. Fixes a security issue in a feature accessible via an OT
2. https://chromium-review.googlesource.com/c/v8/v8/+/5822928
3. < 1 day of canary coverage
4. Not a new feature
5. NA
6. NA

### pg...@google.com (2024-09-03)

This fix has been in Canary for a while, and I do not see any related stability regressions.

Merge approved for M128 - please merge to branch 12.8 by Thursday September 5th EOD MTV time to get this fix into the next M128 stable respin!  

Merge approved for M129 - please merge to branch 12.9 at your earliest convenience to get this fix into the next M129 beta release!

### ap...@google.com (2024-09-04)

Project: v8/v8
Branch: refs/branch-heads/12.9

commit 37d7d47c4e70001d3f345b3a2abc4a85f4e4b33b
Author: Thibaud Michaud <thibaudm@chromium.org>
Date:   Wed Sep 04 10:59:05 2024

    Merged: [wasm] Skip WasmJSFunctions in js-to-wasm wrapper tier-up
    
    When a js-to-wasm wrapper tiers up, we also set the newly compiled
    wrapper as the target for other exports that have the same signature.
    This assumed that all exports have type WasmExportedFunction, but they
    can also have type WasmJSFunction in the case of a re-exported
    WebAssembly.Function import.
    
    R=clemensb@chromium.org
    
    Fixed: 362539773
    (cherry picked from commit 7860c9605e30623eb81129250790aa44757f0e4b)
    
    Change-Id: Ie9b7c3edcefd40cad00e55d070f59edb35722698
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5835722
    Reviewed-by: Clemens Backes <clemensb@chromium.org>
    Commit-Queue: Thibaud Michaud <thibaudm@chromium.org>
    Cr-Commit-Position: refs/branch-heads/12.9@{#20}
    Cr-Branched-From: 64a21d7ad7fca1ddc73a9264132f703f35000b69-refs/heads/12.9.202@{#1}
    Cr-Branched-From: da4200b2cfe6eb1ad73c457ed27cf5b7ff32614f-refs/heads/main@{#95679}

M       src/runtime/runtime-wasm.cc

https://chromium-review.googlesource.com/5835722


### ap...@google.com (2024-09-04)

Project: v8/v8
Branch: refs/branch-heads/12.8

commit 309f157dd68a9af1490d5d820cc928f095ac9b93
Author: Thibaud Michaud <thibaudm@chromium.org>
Date:   Wed Sep 04 11:02:48 2024

    Merged: [wasm] Skip WasmJSFunctions in js-to-wasm wrapper tier-up
    
    When a js-to-wasm wrapper tiers up, we also set the newly compiled
    wrapper as the target for other exports that have the same signature.
    This assumed that all exports have type WasmExportedFunction, but they
    can also have type WasmJSFunction in the case of a re-exported
    WebAssembly.Function import.
    
    R=clemensb@chromium.org
    
    Fixed: 362539773
    (cherry picked from commit 7860c9605e30623eb81129250790aa44757f0e4b)
    
    Change-Id: Id685ae73a84121701729178a3a6f28dbc39648df
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5835724
    Reviewed-by: Clemens Backes <clemensb@chromium.org>
    Commit-Queue: Thibaud Michaud <thibaudm@chromium.org>
    Cr-Commit-Position: refs/branch-heads/12.8@{#54}
    Cr-Branched-From: 70cbb397b153166027e34c75adf8e7993858222e-refs/heads/12.8.374@{#1}
    Cr-Branched-From: 451b63ed4251c2b21c56144d8428f8be3331539b-refs/heads/main@{#95151}

M       src/runtime/runtime-wasm.cc

https://chromium-review.googlesource.com/5835724


### pe...@google.com (2024-09-04)

LTS Milestone M126

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### ap...@google.com (2024-09-05)

Project: v8/v8
Branch: main

commit d9b653416a870081c32fa8b7eeccec9264b56d88
Author: Thibaud Michaud <thibaudm@chromium.org>
Date:   Thu Aug 29 16:24:50 2024

    Reland "[wasm] Remove flag implication between JSPI and type reflection"
    
    This is a reland of commit 76b279609a9450c95e6315fe473980c63449f391
    
    Original change's description:
    > [wasm] Remove flag implication between JSPI and type reflection
    >
    > The deprecated JSPI API based on the WebAssembly.Function constructor
    > was removed from V8. The new API does not depend on the type reflection
    > proposal, so remove the flag implication.
    >
    > R=clemensb@chromium.org
    >
    > Bug: 362539773,42202153
    > Change-Id: I2f0ec66c542197a7e86ef1742abb74302ab1d05d
    > Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5822930
    > Commit-Queue: Thibaud Michaud <thibaudm@chromium.org>
    > Reviewed-by: Clemens Backes <clemensb@chromium.org>
    > Cr-Commit-Position: refs/heads/main@{#95878}
    
    Bug: 362539773,42202153
    Change-Id: Id1588d4514925e7d7b43c77bd868559efe1789ff
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5836662
    Commit-Queue: Thibaud Michaud <thibaudm@chromium.org>
    Reviewed-by: Clemens Backes <clemensb@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#95968}

M       src/flags/flag-definitions.h
M       src/wasm/wasm-features.cc
M       test/mjsunit/wasm/stack-switching.js
M       test/unittests/api/api-wasm-unittest.cc

https://chromium-review.googlesource.com/5836662


### pg...@google.com (2024-09-09)

FYI, confirmed that <https://chromium-review.googlesource.com/c/v8/v8/+/5836662> is not required to consider this fixed (and hence does not need to be backmerged).

<https://chromium-review.googlesource.com/c/v8/v8/+/5822928> is the only CL required.

### sp...@google.com (2024-09-11)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $7000.00 for this report.

Rationale for this decision:
baseline report of memory corruption in a non-sandboxed process


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-09-11)

Congratulations Zhenghang! Thank you for your efforts and reporting this issue to us.

### qk...@google.com (2024-09-12)

I mark `LTS-NotApplicable-120` label to this bug because this bug cannot be reproduced in M120. FYI, the fix required using the generic wrapper for re-exported imports, which was only added in M128. And it could not be exploited anyway because it requires the type reflection feature, which was only enabled as part of the JSPI OT in 123.

### qk...@google.com (2024-09-19)

Labeling as LTS-NotApplicable-126 because of the same reason for M120 above.

### ap...@google.com (2024-09-23)

Project: v8/v8
Branch: main

commit 50645cf964ba96cf44c75fed9790d981a5dd9010
Author: Thibaud Michaud <thibaudm@chromium.org>
Date:   Fri Sep 20 15:17:52 2024

    [wasm] Add some regression tests
    
    R=clemensb@chromium.org
    
    Bug: 361123483,361717714,362539773
    Change-Id: Ie212596f88d0dfa46269bfcdfc2ca24e9570fb76
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5876288
    Commit-Queue: Thibaud Michaud <thibaudm@chromium.org>
    Reviewed-by: Clemens Backes <clemensb@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#96227}

M       test/mjsunit/mjsunit.status
A       test/mjsunit/regress/wasm/regress-361123483.js
A       test/mjsunit/regress/wasm/regress-361717714.js
A       test/mjsunit/regress/wasm/regress-362539773.js

https://chromium-review.googlesource.com/5876288


### pe...@google.com (2024-12-06)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/362539773)*
