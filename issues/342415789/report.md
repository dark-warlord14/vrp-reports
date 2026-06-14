# A security issue when using the JSPI feature.

| Field | Value |
|-------|-------|
| **Issue ID** | [342415789](https://issues.chromium.org/issues/342415789) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>WebAssembly |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | jo...@gmail.com |
| **Assignee** | th...@google.com |
| **Created** | 2024-05-23 |
| **Bounty** | $11,000.00 |

## Description

## TITLE

A security issue when using the JSPI feature.

## VULNERABILITY DETAILS

I found that there is a type confusion when using the JSPI feature.

When using a re-exported imported JS function by `WebAssembly.promising`, the function `NewPromisingWasmExportedFunction` will construct the WasmExportedFunction object.

It uses the js-to-wasm wrapper here:

```
  i::Handle<i::Code> wrapper =
      with_suspender_param ? BUILTIN_CODE(i_isolate, WasmPromisingWithSuspender)
                           : BUILTIN_CODE(i_isolate, WasmPromising);

```

It refers to the `macro JSToWasmWrapperHelper` in file `js-to-wasm.tq`,

When the exported function is called, `JSToWasmWrapperHelper` runs and calls `WasmReturnPromiseOnSuspendAsm`:

```
  // Both `trustedInstanceData` and `resultArray` get passed separately as
  // parameters to make them GC-safe. They get passed over the stack so that
  // they get scanned by the GC as part of the outgoing parameters of this
  // Torque builtin.
  let result: JSAny;
  if constexpr (switchStack) {
    result = WasmReturnPromiseOnSuspendAsm(
        wrapperBuffer, trustedInstanceData, resultArray);
  } else {
    result =
        JSToWasmWrapperAsm(wrapperBuffer, trustedInstanceData, resultArray);
  }

```

`WasmReturnPromiseOnSuspendAsm` is finished in `JSToWasmWrapperHelper` in file `builtin-x64.c` for x64 system. And it will finally call the target.

```
    __ call(call_target);

```

For re-exported imported JS function, the target is the wasm-to-js wrapper.

A param `ref` with type `WasmApiFunctionRef` should be passed to the wasm-to-js wrapper at the register `rsi`:

```
@export
transitioning macro WasmToJSWrapper(ref: WasmApiFunctionRef): WasmToJSResult

```

However, I found that in `WasmReturnPromiseOnSuspendAsm`, the value of `rsi` never changes to a `WasmApiFunctionRef` before calling the target and keeps the value in `JSToWasmWrapperFrameConstants::kInstanceDataParamOffset` as a `kWasmInstanceRegister`.

Thus a type confusion will occur in the `WasmToJSWrapper`.

I construct a POC to prove it.

You can run it at the least version of v8 (commit `21af1bc9eec78ba8d1d17e6ffd5977b12b581c9e`)

You should use `python3 tools/dev/gm.py x64.debug` to build v8.

commond line:

```
out\x64.debug\d8 --experimental-wasm-jspi poc.js

```
## VERSION

Chrome Version: V8 12.7.0

Operating System: Ubuntu

## Timeline

### jo...@gmail.com (2024-05-23)

## Component:

Blink>JavaScript>WebAssembly

This issue should be passed to the V8 WebAssembly team.

## poc.js

```
// flags: --experimental-wasm-jspi
let module = new WebAssembly.Module(new Uint8Array([0,97,115,109,1,0,0,0,1,4,1,96,0,0,2,7,1,1,109,1,102,0,0,7,8,1,4,109,97,105,110,0,0]));
let instance = new WebAssembly.Instance(module, {m: {f: () => {}}});
WebAssembly.promising(instance.exports.main)();

```
## BISECT:

This type confusion will not trigger before this commit, because the `i::WasmTrustedInstanceData::cast` check will crash first.

```
commit 52d9e6db7f4664f0a0a11faaff4e7d28aa898bd8
Author: Thibaud Michaud <thibaudm@chromium.org>
Date:   Mon May 13 13:43:03 2024 +0200

    [wasm][jspi] Fix WA.promising of a re-exported JS import

```

The actual commit for this type confusion is:

```
commit 63a58875aea33190ef982d254d10f5700463f49a
Author: Thibaud Michaud <thibaudm@chromium.org>
Date:   Thu Apr 18 15:56:35 2024 +0200

    [wasm][jspi] Introduce WA.promising and WA.Suspending

```

### jo...@gmail.com (2024-05-23)

## Credit

Anonymous.

### ps...@google.com (2024-05-23)

Thank you for the report OP. Assigning to the V8 shepherd for assignment after setting provisional severity and priority 


### jo...@gmail.com (2024-05-24)

I think [thibaudm@chromium.org](mailto:thibaudm@chromium.org) or [irezvov@chromium.org](mailto:irezvov@chromium.org) may know how to fix it.

### cf...@google.com (2024-05-24)

Thanks for the report!  

thibaudm@, could you PTAL?

### th...@chromium.org (2024-05-24)

I see, so I was wondering why this is not a problem for regular exports, and I just learned by looking at the code that we normally fall back to the signature-specific wrappers, precisely because the generic wrapper does not support re-exported imports.
This is annoying because the promising behavior is not implemented in signature-specific wrappers (yet), so we cannot fallback to a specific wrapper for a promising export.
Technically there is no need to do any stack-switching if we are calling a re-exported import, the import could return the promise directly, and I believe that this would have the same observable behavior as capturing 0 frames. But the import would need to be aware of that, otherwise it will try to suspend the wasm stack.
Maybe the simplest solution is to add the necessary support for re-exported imports in the generic wrapper, then we can also use it for regular exports.

### pe...@google.com (2024-05-24)

Setting milestone because of s0/s1 severity.

### jo...@gmail.com (2024-05-29)

Are there any updates?

### th...@chromium.org (2024-05-29)

I'm working on the fix

### ap...@google.com (2024-05-29)

Project: v8/v8
Branch: main

commit d2d190fb1306449c022296cdec1bb16341996d4a
Author: Thibaud Michaud <thibaudm@chromium.org>
Date:   Wed May 29 17:10:01 2024

    [wasm] Support calling imports with the generic export wrapper
    
    So far the generic wrapper was only used for calling internal wasm
    functions, which allowed it to make the assumption that the implicit
    parameter was a WasmTrustedInstanceData object.
    Add support for passing a WasmApiFunctionRef, which enables using it for
    calling re-exported imports, and also fixes a correctness issue with the
    JSPI variant of the wrapper.
    
    R=ahaas@chromium.org
    
    Fixed: 342415789
    Change-Id: I6c49606ebb5d4406d6ed878b07fff3c8b5b2415c
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5575093
    Reviewed-by: Jakob Kummerow <jkummerow@chromium.org>
    Reviewed-by: Andreas Haas <ahaas@chromium.org>
    Commit-Queue: Thibaud Michaud <thibaudm@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#94161}

M       src/builtins/arm/builtins-arm.cc
M       src/builtins/arm64/builtins-arm64.cc
M       src/builtins/ia32/builtins-ia32.cc
M       src/builtins/js-to-wasm.tq
M       src/builtins/x64/builtins-x64.cc
M       src/execution/frame-constants.h
M       src/execution/frames.cc
M       src/runtime/runtime-wasm.cc
M       src/wasm/wasm-objects.cc

https://chromium-review.googlesource.com/5575093


### pe...@google.com (2024-05-30)

This high+ V8 security issue with stable impact requires a lightweight post mortem. Please take some time to answer questions asked in this form [1] to help us improve V8 security. [1] https://docs.google.com/forms/d/e/1FAIpQLSdSMCiEpIFLLFkMbgtulK1sf1B-idQmkFaA4XP2Rz5mN1cqWg/viewform?usp=pp_url&entry.307501673=342415789&entry.958145677=Linux&entry.763880440=Stable&entry.1678852700=High&entry.763402679=Blink>JavaScript>WebAssembly&entry.975983575=thibaudm@google.com Please ensure to copy the full link, as otherwise some issue meta data might not be populated automatically. 

### 24...@project.gserviceaccount.com (2024-05-30)

ClusterFuzz testcase 5134454535159808 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8&range=94160:94161

If this is incorrect, please add the hotlistid:5432646 and re-open the issue.

### pe...@google.com (2024-05-30)

This is sufficiently serious that it should be merged to stable. But I can't  see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M125. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
This is sufficiently serious that it should be merged to beta. But I can't  see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M126. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Merge review required: M125 is already shipping to stable.


Merge review required: M126 is already shipping to beta.


Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [125, 126].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


### pg...@google.com (2024-06-05)

Canary looks good - nothing relevant that I can see

Merge approved for M126! Please merge the fix to branch 12.6 by Thursday June 13th EOD MTV time to get this fix into the next stable respin

There are no more scheduled releases for M125 - removing label

### jo...@gmail.com (2024-06-07)

deleted

### am...@chromium.org (2024-06-08)

This issue missed the cutoff for this week's VRP panel. We'll review it at a future VRP panel session. Thanks for your patience in the meantime.

### pe...@google.com (2024-06-10)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### jo...@gmail.com (2024-06-10)

Re #17: Got it. Thanks. And credit: anonymous.

### ad...@chromium.org (2024-06-10)

I've been asked to merge this, but I don't think that's the correct action, given that the fix for another JSPI bug, <https://crbug.com/342522151>, is to disable the logic in the CL linked from #11.

thibaudm@, can you please sort out what the proper state of the M126 branch should be WRT these changes?

### ad...@chromium.org (2024-06-10)

Reading more closely I see that this CL includes some changes to the underlying torque implementation (<https://chromium-review.googlesource.com/c/v8/v8/+/5575093/7/src/builtins/js-to-wasm.tq>). And even after the followup fix (<https://crrev.com/c/5600348>) the POC for this issue fails to repro. Therefore I'm more confident that merging this + the followup will put the M126 into a better state (one matching the main branch).

### ap...@google.com (2024-06-10)

Project: v8/v8
Branch: refs/branch-heads/12.6

commit 7e03d1298c394f8a8763a5a88c83f9afc5c5d6bf
Author: Thibaud Michaud <thibaudm@chromium.org>
Date:   Wed May 29 17:10:01 2024

    Merged: [wasm] Support calling imports with the generic export wrapper
    
    So far the generic wrapper was only used for calling internal wasm
    functions, which allowed it to make the assumption that the implicit
    parameter was a WasmTrustedInstanceData object.
    Add support for passing a WasmApiFunctionRef, which enables using it for
    calling re-exported imports, and also fixes a correctness issue with the
    JSPI variant of the wrapper.
    
    (cherry picked from commit d2d190fb1306449c022296cdec1bb16341996d4a)
    
    Bug: 342415789
    Change-Id: I1c7545ac70585b3c2689956d64c816692b0c274c
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5617392
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Commit-Queue: Adam Klein <adamk@chromium.org>
    Cr-Commit-Position: refs/branch-heads/12.6@{#26}
    Cr-Branched-From: 3c9fa12db3183a6f4ea53d2675adb66ea1194529-refs/heads/12.6.228@{#2}
    Cr-Branched-From: 981bb15ba4dbf9e2381dfc94ec2c4af0b9c6a0b6-refs/heads/main@{#93835}

M       src/builtins/arm/builtins-arm.cc
M       src/builtins/arm64/builtins-arm64.cc
M       src/builtins/ia32/builtins-ia32.cc
M       src/builtins/js-to-wasm.tq
M       src/builtins/x64/builtins-x64.cc
M       src/execution/frame-constants.h
M       src/execution/frames.cc
M       src/runtime/runtime-wasm.cc
M       src/wasm/wasm-objects.cc

https://chromium-review.googlesource.com/5617392


### pe...@google.com (2024-06-10)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### rz...@google.com (2024-06-11)

Requesting merge to 125: <https://crrev.com/c/5621591>
Only had a few conflicts, described in the commit message.

### pe...@google.com (2024-06-11)

Merge review required: M125 is already shipping to stable.

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
Owners: govind (Android), govind (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

### rz...@google.com (2024-06-11)

1. It fixes a security issue that affects the milestone
2. <https://crrev.com/c/5621591>
3. Yes ([comment #15](https://issues.chromium.org/issues/342415789#comment15))

### dg...@google.com (2024-06-11)

Approved for M125 for ChromeOS

### ap...@google.com (2024-06-12)

Project: v8/v8
Branch: refs/branch-heads/12.5

commit 2f8100410c6e408c035e5640723f00c1eb791a84
Author: Thibaud Michaud <thibaudm@chromium.org>
Date:   Wed May 29 17:10:01 2024

    Merge to 125: [wasm] Support calling imports with the generic export wrapper
    
    Merge issues:
      builtins/js-to-wasm.tq:
        JSToWasmWrapperHelper():
          - conflicting declarations of "sig"
          - functionData.internal.ref is defined as
          functionData.func_ref.internal.ref in 125
    
    So far the generic wrapper was only used for calling internal wasm
    functions, which allowed it to make the assumption that the implicit
    parameter was a WasmTrustedInstanceData object.
    Add support for passing a WasmApiFunctionRef, which enables using it for
    calling re-exported imports, and also fixes a correctness issue with the
    JSPI variant of the wrapper.
    
    R=ahaas@chromium.org
    
    (cherry picked from commit d2d190fb1306449c022296cdec1bb16341996d4a)
    
    Fixed: 342415789
    Change-Id: I6c49606ebb5d4406d6ed878b07fff3c8b5b2415c
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5575093
    Commit-Queue: Thibaud Michaud <thibaudm@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#94161}
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5621591
    Reviewed-by: Jakob Kummerow <jkummerow@chromium.org>
    Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
    Cr-Commit-Position: refs/branch-heads/12.5@{#28}
    Cr-Branched-From: 15b9756484d5bda98ba273ae13f8db58200db4db-refs/heads/12.5.227@{#1}
    Cr-Branched-From: 497d8573dc80b1b69052a834bec894cf5d4238e7-refs/heads/main@{#93350}

M       src/builtins/arm/builtins-arm.cc
M       src/builtins/arm64/builtins-arm64.cc
M       src/builtins/ia32/builtins-ia32.cc
M       src/builtins/js-to-wasm.tq
M       src/builtins/x64/builtins-x64.cc
M       src/execution/frame-constants.h
M       src/execution/frames.cc
M       src/runtime/runtime-wasm.cc
M       src/wasm/wasm-objects.cc

https://chromium-review.googlesource.com/5621591


### rz...@google.com (2024-06-12)

The issue affects a feature that started an origin trial in 125, no need to backmerge to 120. Adding to the LTS-NotApplicable-120 hotlist.

### pe...@google.com (2024-06-12)

deleted

### sp...@google.com (2024-06-13)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $11000.00 for this report.

Rationale for this decision:
$10,000 for high quality report of memory corruption in the renderer / sandboxed process + $1,000 bisect bonus 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-06-13)

Congratulations! Thank you for your efforts in discovering this issue and your high quality reporting of it to us -- great work!

### ap...@google.com (2024-08-14)

Project: v8/v8
Branch: main

commit ab3bfaa628a5a1c5fb77bec8b7fecf6139d5ce74
Author: Thibaud Michaud <thibaudm@chromium.org>
Date:   Wed Aug 14 17:27:55 2024

    [wasm] Add missing regression tests
    
    R=jkummerow@chromium.org
    
    Bug: 342522151,342415789,346197738,346597059,
    Change-Id: Iace766d0032d0c3def5877ac86440442b2aea04d
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5788586
    Reviewed-by: Jakob Kummerow <jkummerow@chromium.org>
    Commit-Queue: Thibaud Michaud <thibaudm@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#95639}

A       test/mjsunit/regress/wasm/regress-342522151.js
A       test/mjsunit/regress/wasm/regress-346197738.js
A       test/mjsunit/regress/wasm/regress-346597059.js

https://chromium-review.googlesource.com/5788586


### ap...@google.com (2024-08-14)

Project: v8/v8
Branch: main

commit 6876e28371bccf8314d951187e8338ed9dbe19aa
Author: Deepti Gandluri <gdeepti@chromium.org>
Date:   Wed Aug 14 21:44:17 2024

    Revert "[wasm] Add missing regression tests"
    
    This reverts commit ab3bfaa628a5a1c5fb77bec8b7fecf6139d5ce74.
    
    Reason for revert: Regression test fails on the single generation bot - https://ci.chromium.org/ui/p/v8/builders/ci/V8%20Linux64%20-%20debug%20-%20single%20generation/16342/overview
    
    Original change's description:
    > [wasm] Add missing regression tests
    >
    > R=jkummerow@chromium.org
    >
    > Bug: 342522151,342415789,346197738,346597059,
    > Change-Id: Iace766d0032d0c3def5877ac86440442b2aea04d
    > Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5788586
    > Reviewed-by: Jakob Kummerow <jkummerow@chromium.org>
    > Commit-Queue: Thibaud Michaud <thibaudm@chromium.org>
    > Cr-Commit-Position: refs/heads/main@{#95639}
    
    Bug: 342522151,342415789,346197738,346597059,
    Change-Id: I8bb2b3032437519b4794a08f56314f8f9a3a4b7b
    No-Presubmit: true
    No-Tree-Checks: true
    No-Try: true
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5788832
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Auto-Submit: Deepti Gandluri <gdeepti@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#95645}

D       test/mjsunit/regress/wasm/regress-342522151.js
D       test/mjsunit/regress/wasm/regress-346197738.js
D       test/mjsunit/regress/wasm/regress-346597059.js

https://chromium-review.googlesource.com/5788832


### ap...@google.com (2024-08-19)

Project: v8/v8
Branch: main

commit c0d69082d25cfdd92557f8f922dc282934a89079
Author: Thibaud Michaud <thibaudm@chromium.org>
Date:   Mon Aug 19 14:58:10 2024

    Reland "[wasm] Add missing regression tests"
    
    This is a reland of commit ab3bfaa628a5a1c5fb77bec8b7fecf6139d5ce74
    
    Change: Skip test that uses %SimulateNewspaceFull in
    single_generation mode, and skip JSPI test on platforms that
    don't implement JSPI yet.
    
    Original change's description:
    > [wasm] Add missing regression tests
    >
    > R=jkummerow@chromium.org
    >
    > Bug: 342522151,342415789,346197738,346597059,
    > Change-Id: Iace766d0032d0c3def5877ac86440442b2aea04d
    > Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5788586
    > Reviewed-by: Jakob Kummerow <jkummerow@chromium.org>
    > Commit-Queue: Thibaud Michaud <thibaudm@chromium.org>
    > Cr-Commit-Position: refs/heads/main@{#95639}
    
    Bug: 342522151,342415789,346197738,346597059,
    Change-Id: Ib803b351b1a2b4eb45c549408b7cfc004063d9e7
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5797382
    Reviewed-by: Jakob Kummerow <jkummerow@chromium.org>
    Commit-Queue: Thibaud Michaud <thibaudm@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#95690}

M       test/mjsunit/mjsunit.status
A       test/mjsunit/regress/wasm/regress-342522151.js
A       test/mjsunit/regress/wasm/regress-346197738.js
A       test/mjsunit/regress/wasm/regress-346597059.js

https://chromium-review.googlesource.com/5797382


### pe...@google.com (2024-09-05)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### br...@gmail.com (2024-09-06)

Hi, I have no other meaning. I just confuse that ` --experimental-wasm-jspi` is in `experimental`, should not eligible for VRP at this report time. Why  does it eligible?

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/342415789)*
