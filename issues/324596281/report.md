# Debug check failed: !type.has_index(). in v8

| Field | Value |
|-------|-------|
| **Issue ID** | [324596281](https://issues.chromium.org/issues/324596281) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript, Blink>JavaScript>WebAssembly |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | je...@gmail.com |
| **Assignee** | ah...@chromium.org |
| **Created** | 2024-02-11 |
| **Bounty** | $7,000.00 |

## Description

VULNERABILITY DETAILS
## INTRODUCE
After bisect, it was determined that following commit caused this problem.

- Commit Info
    - Version: 92216
    - link: https://crrev.com/08170169a305fab1dca42bc11d86d7400f25421e 
- Commit Message

```
commit 08170169a305fab1dca42bc11d86d7400f25421e
Author: Jakob Kummerow <jkummerow@chromium.org>
Date:   Tue Feb 6 15:40:33 2024 +0100

    [wasm-imported-strings] Implement encodeStringToUtf8Array
    
    Contrary to the "Into" variant, this implicitly allocates an array
    of appropriate size.
    
    Bug: v8:14179
    Change-Id: I01974624683eef961f6c8b8c6cbe33aa65d2df6a
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5273182
    Reviewed-by: Matthias Liedtke <mliedtke@chromium.org>
    Commit-Queue: Jakob Kummerow <jkummerow@chromium.org>
    Auto-Submit: Jakob Kummerow <jkummerow@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#92216}

```

## CRASH LOG
- Debug output

```bash
# CMD: /tmp/d8-linux32-debug-v8-component-92260/d8 --allow-natives-syntax --experimental-wasm-imported-strings poc.js
# OUTPUT ==============================================================


#
# Fatal error in ../../src/wasm/canonical-types.cc, line 131
# Debug check failed: !type.has_index().
#
#
#
#FailureMessage Object: 0xffed0a00
==== C stack trace ===============================

    /tmp/d8-linux32-debug-v8-component-92260/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x1f) [0xf7f2d19f]
    /tmp/d8-linux32-debug-v8-component-92260/libv8_libplatform.so(+0x16274) [0xf7ed9274]
    /tmp/d8-linux32-debug-v8-component-92260/libv8_libbase.so(V8_Fatal(char const*, int, char const*, ...)+0xf7) [0xf7f0c5a7]
    /tmp/d8-linux32-debug-v8-component-92260/libv8_libbase.so(+0x26fa6) [0xf7f0bfa6]
    /tmp/d8-linux32-debug-v8-component-92260/libv8_libbase.so(V8_Dcheck(char const*, int, char const*)+0x31) [0xf7f0c5f1]
    /tmp/d8-linux32-debug-v8-component-92260/libv8.so(v8::internal::wasm::TypeCanonicalizer::AddRecursiveGroup(v8::internal::Signature<v8::internal::wasm::ValueType> const*)+0xda) [0xf68996ca]
    /tmp/d8-linux32-debug-v8-component-92260/libv8.so(+0x3153a0b) [0xf6753a0b]
    /tmp/d8-linux32-debug-v8-component-92260/libv8.so(v8::internal::Runtime_TierUpWasmToJSWrapper(int, unsigned int*, v8::internal::Isolate*)+0x7d) [0xf6752b4d]
    /tmp/d8-linux32-debug-v8-component-92260/libv8.so(+0x172590a) [0xf4d2590a]
    /tmp/d8-linux32-debug-v8-component-92260/libv8.so(+0x16f7a8a) [0xf4cf7a8a]
    [0x51d70442]
    [0x51d704dd]
    [0x51d704dd]
    [0x51d704dd]
    [0x51d704dd]
    [0x51d704dd]
    [0x51d704dd]
    [0x51d704dd]
    [0x51d704dd]
    [0x51d704dd]
    [0x51d704dd]
    [0x51d704dd]
    [0x51d704dd]
    [0x51d704dd]
    [0x51d704dd]
    [0x51d704dd]
    [0x51d704dd]
    [0x51d704dd]
    [0x51d704dd]
    [0x51d704dd]
    [0x51d704dd]
    [0x51d704dd]
    [0x51d704dd]
    [0x51d704dd]
    [0x51d704dd]
    [0x51d704dd]
    [0x51d704dd]
    [0x51d704dd]
    [0x51d704dd]
    [0x51d704dd]
    [0x51d704dd]
    [0x51d704dd]
    [0x51d704dd]
    [0x51d704dd]
    [0x51d704dd]
    [0x51d704dd]
    [0x51d704dd]
    [0x51d704dd]
    [0x51d704dd]
    [0x51d704dd]
    [0x51d704dd]
    [0x51d704dd]
    [0x51d704dd]
    [0x51d704dd]
    [0x51d704dd]
    [0x51d704dd]
    [0x51d704dd]
    [0x51d704dd]
    [0x51d704dd]
    [0x51d704dd]
    [0x51d704dd]
    [0x51d704dd]

```

## Other
Please note to include the flags `--allow-natives-syntax --experimental-wasm-imported-strings` for clusterfuzz classification.

VERSION
Tested on v8 version: 12.3.0 - 12.3.0

REPRODUCTION CASE
1. Download debug v8 from: gs://v8-asan/linux32-debug/d8-linux32-debug-v8-component-92260.zip
2. Run: `d8 --allow-natives-syntax --experimental-wasm-imported-strings poc.js`

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: tab

CREDIT INFORMATION
Reporter credit: Jerry

## Attachments

- [poc.js](attachments/poc.js) (text/javascript, 6.3 KB)
- [wasm.bin](attachments/wasm.bin) (application/octet-stream, 1.8 KB)

## Timeline

### je...@gmail.com (2024-02-12)

Due to recent changes in the functionality code of wasm, bisect may not necessarily be accurate. Please decide on the final entry point based on the actual situation.


### wf...@chromium.org (2024-02-12)

Thank you for your report

### cl...@appspot.gserviceaccount.com (2024-02-12)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4811466135240704.

### je...@gmail.com (2024-02-12)

Please use 32-bits debug d8 to run clusterfuzzer

### wf...@chromium.org (2024-02-13)

The severity and found in are provisional.

### cl...@appspot.gserviceaccount.com (2024-02-13)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5135378643615744.

### 24...@project.gserviceaccount.com (2024-02-13)

Detailed Report: https://clusterfuzz.com/testcase?key=5135378643615744

Fuzzer: None
Job Type: linux32_asan_d8_dbg
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  !type.has_index() in canonical-types.cc
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux32_asan_d8_dbg&range=92215:92216

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5135378643615744

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### jk...@chromium.org (2024-02-13)

The bisection result is bogus as suspected. 32-bit builds are not required, this reproduces everywhere. Simple repro:

```
d8.file.execute('../../test/mjsunit/wasm/wasm-module-builder.js');
let builder = new WasmModuleBuilder();
let struct = builder.addStruct([makeField(kWasmI32, true)]);
let sig = builder.addType(makeSig([wasmRefType(struct)], [wasmRefType(struct)]));
let imp = builder.addImport('m', 'f', sig);
builder.addFunction('main', kSig_i_i).exportFunc().addBody([
  kGCPrefix, kExprStructNewDefault, struct,
  kExprLoop, sig,
    kExprCallFunction, imp,
    kExprLocalGet, 0,
    kExprI32Const, 1,
    kExprI32Sub,
    kExprLocalTee, 0,
    kExprI32Eqz,
    kExprI32Eqz,
    kExprBrIf, 0,
  kExprEnd,
  kGCPrefix, kExprStructGet, struct, 0,
  ]);

let instance = builder.instantiate({m: {f: (x) => x}});
// The argument is the iteration count: enough to tier up the wasm-to-js wrapper.
instance.exports.main(2000);

```

`Runtime_TierUpWasmToJSWrapper` calls `wasm::GetTypeCanonicalizer()->AddRecursiveGroup(&sig);` which expects `sig` to only contain module-independent types, which is an incorrect limitation: the signature may very well contain module-specific types. I think we'll probably have to store the (canonical?) signature ID (or something from which it can be computed) in each `WasmApiFunctionRef` we create for module-specified signatures (as is the case for all imported functions), or something to that effect, and only call `AddRecursiveGroup` for truly new signatures (created in JavaScript via `new WebAssembly.Function`).

### pe...@google.com (2024-02-13)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2024-02-13)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ah...@chromium.org (2024-02-14)

Fixed in
5291374: [wasm] Use correct signature index for tier-up of wasm-to-js wrapper | https://chromium-review.googlesource.com/c/v8/v8/+/5291374

### pe...@google.com (2024-02-14)

This is sufficiently serious that it should be merged to extended stable. But I can't  see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M120. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
This is sufficiently serious that it should be merged to stable. But I can't  see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M121. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
This is sufficiently serious that it should be merged to beta. But I can't  see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M122. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.


Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.


Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.


Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [120, 121, 122].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


### pe...@google.com (2024-02-15)

This high+ V8 security issue with stable impact requires a lightweight post mortem. Please take some time to answer questions asked in this form [1] to help us improve V8 security. [1] https://docs.google.com/forms/d/e/1FAIpQLSdSMCiEpIFLLFkMbgtulK1sf1B-idQmkFaA4XP2Rz5mN1cqWg/viewform?usp=pp_url&entry.307501673=324596281&entry.364066060=jerrylulu7@gmail.com&entry.958145677=Android, Linux, Mac, Windows, Lacros, ChromeOS&entry.763880440=Extended&entry.1678852700=High&entry.763402679=Blink>JavaScript&entry.975983575=ahaas@chromium.org Please ensure to copy the full link, as otherwise some issue meta data might not be populated automatically. 

### ah...@chromium.org (2024-02-15)

1. Which CLs should be backmerged? (Please include Gerrit links.)
https://chromium-review.googlesource.com/c/v8/v8/+/5291374
2. Has this fix been verified on Canary to not pose any stability regressions?
Yes, in 123.0.6301.0
3. Does this fix pose any potential non-verifiable stability risks?
No
4. Does this fix pose any known compatibility risks?
No
5. Does it require manual verification by the test team? If so, please describe required testing.
No

### am...@chromium.org (2024-02-17)

<https://crrev.com/c/5291374> approved for merge to M122, please merge this fix to 12.2-lkgr at your earliest convenience (before EOD Thursday, 22 February) so this fix can be included in the first M122 Stable channel update.

There are no further planned releases of M121 Stable or M120 Extended.
M122 Stable is shipping on Tuesday.

### pe...@google.com (2024-02-19)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ap...@google.com (2024-02-19)

Project: v8/v8
Branch: refs/branch-heads/12.2

commit 27e21759257fe1b8f8e08dd8ea82062a56aa6453
Author: Andreas Haas <ahaas@chromium.org>
Date:   Tue Feb 13 14:14:59 2024

    Merged: [wasm] Use correct signature index for tier-up of wasm-to-js wrapper
    
    The wasm-to-js wrapper tierup used the canonicalized signature id lookup
    for module-independent signatures to look up the canonicalized signature
    id of module-specific signatures. With this CL the signature id is
    looked up with the function index of imported functions and from the
    dispatch table for indirect function calls instead.
    
    R=jkummerow@chromium.org
    
    Bug: 324596281
    (cherry picked from commit 2109613ad4622028778a38fb418956fab8b478b6)
    
    Change-Id: I3fb7e4f02596f62e13ffe60015f96bac5efbc598
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5300311
    Reviewed-by: Jakob Kummerow <jkummerow@chromium.org>
    Commit-Queue: Andreas Haas <ahaas@chromium.org>
    Cr-Commit-Position: refs/branch-heads/12.2@{#32}
    Cr-Branched-From: 6eb5a9616aa6f8c705217aeb7c7ab8c037a2f676-refs/heads/12.2.281@{#1}
    Cr-Branched-From: 44cf56d850167c6988522f8981730462abc04bcc-refs/heads/main@{#91934}

M       src/runtime/runtime-wasm.cc
A       test/mjsunit/regress/wasm/regress-324596281.js

https://chromium-review.googlesource.com/5300311


### ap...@google.com (2024-02-19)

Project: v8/v8
Branch: refs/branch-heads/12.2

commit 27e21759257fe1b8f8e08dd8ea82062a56aa6453
Author: Andreas Haas <ahaas@chromium.org>
Date:   Tue Feb 13 14:14:59 2024

    Merged: [wasm] Use correct signature index for tier-up of wasm-to-js wrapper
    
    The wasm-to-js wrapper tierup used the canonicalized signature id lookup
    for module-independent signatures to look up the canonicalized signature
    id of module-specific signatures. With this CL the signature id is
    looked up with the function index of imported functions and from the
    dispatch table for indirect function calls instead.
    
    R=jkummerow@chromium.org
    
    Bug: 324596281
    (cherry picked from commit 2109613ad4622028778a38fb418956fab8b478b6)
    
    Change-Id: I3fb7e4f02596f62e13ffe60015f96bac5efbc598
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5300311
    Reviewed-by: Jakob Kummerow <jkummerow@chromium.org>
    Commit-Queue: Andreas Haas <ahaas@chromium.org>
    Cr-Commit-Position: refs/branch-heads/12.2@{#32}
    Cr-Branched-From: 6eb5a9616aa6f8c705217aeb7c7ab8c037a2f676-refs/heads/12.2.281@{#1}
    Cr-Branched-From: 44cf56d850167c6988522f8981730462abc04bcc-refs/heads/main@{#91934}

M       src/runtime/runtime-wasm.cc
A       test/mjsunit/regress/wasm/regress-324596281.js

https://chromium-review.googlesource.com/5300311


### pe...@google.com (2024-02-19)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### ah...@chromium.org (2024-02-19)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
The issue happens in code that was shipped with finch starting with version 121.0.6143.0. Older versions would have the issue, but only in code that is disabled by default.
2. Is this issue related to a change or feature merged after the latest LTS Milestone?
Yes

### 24...@project.gserviceaccount.com (2024-02-22)

ClusterFuzz testcase 5135378643615744 is still reproducing on tip-of-tree build (trunk).

Please re-test your fix against this testcase and if the fix was incorrect or incomplete, please re-open the bug. Otherwise, ignore this notification and add the hotlistid:5432646.

### 24...@project.gserviceaccount.com (2024-02-22)

Detailed Report: https://clusterfuzz.com/testcase?key=5135378643615744

Fuzzer: None
Job Type: linux32_asan_d8_dbg
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  !type.has_index() in canonical-types.cc
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux32_asan_d8_dbg&range=92215:92216

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5135378643615744

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### am...@google.com (2024-02-22)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2024-02-22)

Congratulations Jerry! The VRP Panel has decided to award you $7,000 for this report of renderer process memory corruption. Thank you for your efforts and reporting this issue to us!

### pe...@google.com (2024-02-23)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### am...@chromium.org (2024-02-28)

Opening this issue to security-notify since the bots did not do that when the bug was closed as fixed.

### am...@chromium.org (2024-03-05)

resetting owner as I'm not sure why this changed ownership

### pe...@google.com (2024-06-11)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/324596281)*
