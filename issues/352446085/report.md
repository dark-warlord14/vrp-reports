# V8 Sandbox Bypass: AAR/W via WASM import race condition leading to broken runtime bounds check with memory64

| Field | Value |
|-------|-------|
| **Issue ID** | [352446085](https://issues.chromium.org/issues/352446085) |
| **Status** | Verified |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>JavaScript>WebAssembly |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows |
| **Reporter** | se...@gmail.com |
| **Assignee** | jk...@chromium.org |
| **Created** | 2024-07-11 |
| **Bounty** | $5,000.00 |

## Description

### VULNERABILITY DETAILS

This is a v8sbx bypass bug split out from [b/351327767#comment9](https://issues.chromium.org/issues/351327767#comment9).

V8 sandbox bypass, arbitrary address read/write via WASM memory64 import check race condition leading to broken invariants related with runtime memory index bounds check.

WASM memory access operations require runtime bounds check on dynamic indexes. This is done through [`LiftoffCompiler::BoundsCheckMem()`](https://source.chromium.org/chromium/chromium/src/+/main:v8/src/wasm/baseline/liftoff-compiler.cc;drc=cf999a774421e3e44e78902f63124173e038fed7;l=3434) for Liftoff and [`WasmGraphBuilder::BoundsCheckMem()`](https://source.chromium.org/chromium/chromium/src/+/main:v8/src/compiler/wasm-compiler.cc;drc=bdb1358afd8fc0dae2a3f8e0348d9841a2d30636;l=3687) for TurboFan. As explained in the coments for the TurboFan code, the runtime bounds check depend on the invariant `end_offset <= min_size <= mem_size` and computes `effective_size = mem_size - end_offset` to use as the upper bounds for the dynamic index. If the `end_offset` is statically known to be less than or equal to `min_size`, the subtraction should never overflow and thus the `end_offset < mem_size` bounds check is elided.

However, this invariant can be broken by a race condition between checking imported memory at [`InstanceBuilder::ProcessImportedMemories()`](https://source.chromium.org/chromium/chromium/src/+/main:v8/src/wasm/module-instantiate.cc;drc=e37b630102f0e757762d3f450f1646da97a7e4dd;l=2493) and adding the memory info to the trusted instance data at [`WasmMemoryObject::UseInInstance()`](https://source.chromium.org/chromium/chromium/src/+/main:v8/src/wasm/wasm-objects.cc;drc=e37b630102f0e757762d3f450f1646da97a7e4dd;l=807). Breaking this invariant results in `effective_size` computation to overflow, allowing the full 64bit address space to be indexable with memory64.

**Note that only memory64 is likely exploitable as indices on non-memory64 accesses are truncated to 32bit, landing any out-of-bounds accesses within the sandbox region.**

### VERSION

V8 Version: Tested on 2fdefb5683cd3e7f7734fb22c9a1cea3d06ece67, exists on latest (bc545b15a0ee5dd3bea9f2bfb991b380f5f3659c)

### REPRODUCTION CASE

Attached as `wasm-memory64-v8sbx.js`, run with `./d8 --experimental-wasm-memory64 --sandbox-testing ./wasm-memory64-v8sbx.js`.

### FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION

Type of crash: Sandbox violation

### CREDIT INFORMATION

Reporter credit: Seunghyun Lee (@0x10n)

## Attachments

- [wasm-memory64-v8sbx.js](attachments/wasm-memory64-v8sbx.js) (text/javascript, 75.0 KB)

## Timeline

### ap...@google.com (2024-07-11)

Project: v8/v8
Branch: main

commit b814386527b4ceedbc39c83abcd1b11e181bd482
Author: Jakob Kummerow <jkummerow@chromium.org>
Date:   Thu Jul 11 17:48:50 2024

    [wasm] Harden min mem size against concurrent corruption
    
    We check during instantiation that any imported memories are at
    least as big as their static minimum size, and later rely on this
    invariant. However, a worker thread with in-sandbox corruption
    capabilities could invalidate the invariant after we've checked it,
    so harden against that possibility.
    
    Fixed: 352446085
    Change-Id: Iec1449a6143e0e509e4d947d8a2eda172e995b2c
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5695668
    Reviewed-by: Matthias Liedtke <mliedtke@chromium.org>
    Commit-Queue: Matthias Liedtke <mliedtke@chromium.org>
    Commit-Queue: Jakob Kummerow <jkummerow@chromium.org>
    Auto-Submit: Jakob Kummerow <jkummerow@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#94986}

M       src/wasm/wasm-objects.cc

https://chromium-review.googlesource.com/5695668


### pe...@google.com (2024-07-11)

Dear owner, thanks for fixing this bug. We've reopened it because security bugs need the Severity (S0-S3) and the Found In set, which will enable the bots to request merges to the correct branches ( as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact ([security@chromium.org](mailto:security@chromium.org)) to arrange to set these labels and then this bug can be marked closed again. Thank you! Severity guidelines: <https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues> FoundIn guidelines: <https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security> Thanks for your time!

### jk...@chromium.org (2024-07-11)

#3: Severity is probably S1: it's a sandbox escape that requires having in-sandbox corruption already. (And, for a change, it's a sandbox escape that's not related to signature mixups at calls!)

Not sure how to set Found-In: it needs a feature ("memory64") that's not enabled by default yet, so I'd call that "Security-Impact\_None" in the old bug tracker.

Note that memory64 is marked as "staged", and staged features are (AFAIK) generally in scope for the VRP. I'm not sure how we handle the intersection of "staged feature" and "sandbox escape" though.

+CC Samuel for input on all these points.

### fl...@google.com (2024-07-11)

Current security shepherd here. re: [comment #4](https://issues.chromium.org/issues/352446085#comment4): We now set Security\_Impact-None via a Hotlist. I've updated that + the severity accordingly. Thank you very much!

### jk...@chromium.org (2024-07-12)

#5: Thanks, we can set this back to "Fixed" then.

### sa...@chromium.org (2024-07-15)

This is a V8 Sandbox bypass, so setting labels accordingly.

### sp...@google.com (2024-07-17)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $5000.00 for this report.

Rationale for this decision:
V8 heap sandbox bypass reward


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-07-17)

Congratulations on another sandbox bypass discovery and thank you for reporting it to us, Seunghyun!

### pe...@google.com (2024-10-19)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/352446085)*
