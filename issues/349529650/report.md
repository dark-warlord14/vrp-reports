# V8 Sandbox Bypass: AAR/W via function import signature check race

| Field | Value |
|-------|-------|
| **Issue ID** | [349529650](https://issues.chromium.org/issues/349529650) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>JavaScript>Sandbox |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | se...@gmail.com |
| **Assignee** | jk...@chromium.org |
| **Created** | 2024-06-26 |
| **Bounty** | $5,000.00 |

## Description

### VULNERABILITY DETAILS

V8 sandbox bypass, arbitrary address read/write via function import signature check bypass through race condition using in-sandbox exploit primitives.

Imported functions are processed through `InstanceBuilder::ProcessImportedFunction()`, where various checks are performed in `WasmImportData::ComputeKind()`. Signature checks are performed in <https://source.chromium.org/chromium/chromium/src/+/main:v8/src/wasm/module-instantiate.cc;l=698>, where we access `WasmExportedFunction -> SharedFunctionInfo -> TrustedFunctionData`. However, we access this once again starting from the `WasmExportedFunction` at <https://source.chromium.org/chromium/chromium/src/+/main:v8/src/wasm/module-instantiate.cc;l=1874> when we actually add the function call target to the imported entry dispatch table.

This opens up a race window where we can race two `TrustedFunctionData` values: one malicious with differing signature, and one benign with matching signature. Once we pass the first check with the benign `TrustedFunctionData` and then add the malicious one to the dispatch table (benign -> malicious case), we can cause a signature mismatch at `call` (NOT `call_ref` which is signature hash checked) and obtain AAR/W. If the race condition is not satisfied, we either instantiate the WASM module with the benign function (benign -> benign case) or simply throw a `LinkError` (malicious -> ? case) which we can catch from JS, thus we obtain a 100% success rate.

### VERSION

Chrome Version: ~latest (tested on v8 commit a832ff96bd41b40b9cfee90a314fa816802cf9ae)  

Operating System: all

### REPRODUCTION CASE

Repro added as `function_import_race.js`.

### FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION

Type of crash: Sandbox violation

### CREDIT INFORMATION

Reporter credit: Seunghyun Lee (@0x10n)

## Attachments

- [function_import_race.js](attachments/function_import_race.js) (text/javascript, 72.5 KB)

## Timeline

### el...@chromium.org (2024-06-26)

Security shepherd: thanks for the report. Do you have a smaller repro case?

Either way, -> v8 shepherd, and setting Pri-2 Sev-2 since this is not a direct RCE.

### se...@gmail.com (2024-06-26)

Re [comment#2](https://issues.chromium.org/issues/349529650#comment2): The repro is large since I've embedded the whole `wasm-module-builder.js` (~2100 lines) - replace it with `d8.file.execute()` to reduce the redundancy, although for a easier repro I prefer to present it in the current form.

### pe...@google.com (2024-06-27)

Setting milestone because of s2 severity.

### jk...@chromium.org (2024-06-28)

Quick status update: I have a local fix that fixes the given repro. I haven't uploaded it yet because I want to spend a bit more time exploring whether it's sufficiently complete; it seems there's a good chance that there might be other places that are susceptible to similar race conditions with malicious worker threads.

(And re #3: yeah, this style of repro is totally fine.)

### jk...@chromium.org (2024-07-12)

Finally getting back to this. Fix in review: <https://chromium-review.googlesource.com/c/v8/v8/+/5701107>

### ap...@google.com (2024-07-15)

Project: v8/v8
Branch: main

commit 3caea615ab192c4211faaf4521b53c1c81ecb560
Author: Jakob Kummerow <jkummerow@chromium.org>
Date:   Mon Jul 15 20:08:10 2024

    [wasm][sandbox] Harden WasmImportData against concurrent modification
    
    While processing imports is specified to be an "atomic" operation
    in the sense that no user code runs in the same Isolate at the same
    time, a compromised worker could cause corruption anywhere in the
    same sandbox cage at any time. That means we must not read the same
    property repeatedly and trust that we get the same value; instead
    we must read security-relevant values only once, and cache them
    off-heap as long as they are needed.
    This patch applies that idea to ProcessImportedFunction().
    As a hardening measure, it also takes away a few helper functions
    that are easy to misuse.
    
    Fixed: 349529650
    Bug: 336507783
    Change-Id: Icba0d8159e1e5063c4c730120ebd6e397a4b67da
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5701107
    Commit-Queue: Jakob Kummerow <jkummerow@chromium.org>
    Reviewed-by: Clemens Backes <clemensb@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#95037}

M       src/diagnostics/objects-printer.cc
M       src/runtime/runtime-test-wasm.cc
M       src/wasm/c-api.cc
M       src/wasm/module-instantiate.cc
M       src/wasm/module-instantiate.h
M       src/wasm/wasm-js.cc
M       src/wasm/wasm-objects.cc
M       src/wasm/wasm-objects.h
M       test/fuzzer/wasm-deopt.cc
M       test/fuzzer/wasm-fuzzer-common.cc
A       test/mjsunit/sandbox/wasm-imports-concurrent-mutation.js

https://chromium-review.googlesource.com/5701107


### pe...@google.com (2024-07-16)

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M127. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
**Merge rejected:** M127 has already been cut for stable release and this issue is marked as a Priority:P2,P3 or Type:feature request.

Please contact the milestone owner if you have questions.

**Owners:** eakpobaro (Android), eakpobaro (iOS), alonbajayo (ChromeOS), danielyip (Desktop)
Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [127].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.

### jk...@chromium.org (2024-07-16)

#8: We don't backmerge sandbox escape fixes.

### sp...@google.com (2024-08-02)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $5000.00 for this report.

Rationale for this decision:
$5,000 V8 heap sandbox bypass reward


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-08-02)

Congratulations on another sandbox bypass, Seunghyun! Thanks for your efforts and reporting this bypass to us -- nice work!

### pe...@google.com (2024-10-22)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> $5,000 V8 heap sandbox bypass reward

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/349529650)*
