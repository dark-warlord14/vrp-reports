# V8 Sandbox Bypass: AAR/W via table import signature check bypass

| Field | Value |
|-------|-------|
| **Issue ID** | [348793147](https://issues.chromium.org/issues/348793147) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>JavaScript>Sandbox |
| **Platforms** | Android, Linux, Mac, Windows, iOS, ChromeOS |
| **Reporter** | se...@gmail.com |
| **Assignee** | jk...@chromium.org |
| **Created** | 2024-06-23 |
| **Bounty** | $5,000.00 |

## Description

### VULNERABILITY DETAILS

V8 sandbox bypass, arbitrary address read/write via table import signature check bypass using in-sandbox exploit primitives.

This is a direct variant of [b/336507783](https://issues.chromium.org/issues/336507783), where we now modify the table signature and then pass it as an imported table. The signature is checked via `wasm::InstanceBuilder::ProcessImportedTable()`, where the corrupted in-sandbox signature allows the `EquivalentTypes()` check in <https://source.chromium.org/chromium/chromium/src/+/main:v8/src/wasm/module-instantiate.cc;l=2086> to succeed. This results in the same signature confusion in `call_indirect` as seen in [b/336507783](https://issues.chromium.org/issues/336507783).

### VERSION

Chrome Version: ~latest (current latest v8 commit: 8b52e5f026dc859cab827ec584f3eedbc0510459)
Operating System: all

### REPRODUCTION CASE

Repro added as exp.js.

### FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION

Type of crash: Sandbox violation

### CREDIT INFORMATION

Reporter credit: Seunghyun Lee (@0x10n)

## Attachments

- [exp.js](attachments/exp.js) (text/javascript, 71.6 KB)
- [exp2.js](attachments/exp2.js) (text/javascript, 71.9 KB)

## Timeline

### se...@gmail.com (2024-06-23)

Forgot to mention that I found this while looking at GoogleCTF 2024 "heat" challenge, so kudos to the chal authors and ctf admins :)

### se...@gmail.com (2024-06-24)

Just recognized that [b/336507783](https://issues.chromium.org/issues/336507783) looks like a large tracking bug for various wasm signature confusion v8sbx bypasses, so to be more specific this is a variant of <https://chromium-review.googlesource.com/c/v8/v8/+/5626414>.

### sa...@chromium.org (2024-06-25)

Thanks, great work! :)

[b/336507783](https://issues.chromium.org/issues/336507783) is indeed just the tracking bug for making Wasm "sandbox compatible", and I don't think it should be view-restricted, so fixed that now.

### se...@gmail.com (2024-06-26)

Hi, attached is another variant. Instead of modifying the `raw_type` of the `WasmTypeObject`, we can replace each `entries` in the `WasmTypeObject` with another function having different signature and achieve the same effect.

As both of these approaches would be fixed by adding `SBXCHECK(FunctionSigMatchesTable(...))` for each entries processed in `InstanceBuilder::InitializeImportedIndirectFunctionTable()`, I'm just adding this as a comment here. Feel free to split this out if it's considered another bypass.

Note that I've tested this one on commit a832ff96bd41b40b9cfee90a314fa816802cf9ae so offset is changed (`kWasmTableObjectTypeOffset = 28`).

### jk...@chromium.org (2024-06-27)

I think [comment #5](https://issues.chromium.org/issues/348793147#comment5) is spot on: since tables are writable, it makes sense to continue treating the `WasmTableObject` itself as untrusted and possibly-corrupted, whereas we should signature-check the individual functions in it before writing their entry points into the `WasmDispatchTable`.

Patch: <https://chromium-review.googlesource.com/c/v8/v8/+/5659606>

### jk...@chromium.org (2024-06-27)

Btw, Seunghyun, your repro cases are great to work with, thanks for that! In the patch linked in #6 I've included the module builder fix so you don't need to avoid type index 0 any more :)

---

I think there's another variant of this issue that needs `new WebAssembly.Function(...)` (enabled by `--experimental-wasm-type-reflection`). I'll try to build a repro for that, and then fix that too.

### se...@gmail.com (2024-06-27)

Re [comment#7](https://issues.chromium.org/issues/348793147#comment7): Thanks! I'm also somewhat concerned in how wasm type reflection and JSPI would work together with the v8 sandbox, but to be honest I haven't looked deeply into these as they are either experimental or gated behind origin trials. I'll take a look when time permits :)

P.S. Please excuse the unnamed constants and unused codes in the repro testcase, I'll remember to clean them up for future submissions.

### ap...@google.com (2024-06-27)

Project: v8/v8
Branch: main

commit 2b620f7de169ee3374ca1cb11098cc38ec2b0b8d
Author: Jakob Kummerow <jkummerow@chromium.org>
Date:   Thu Jun 27 16:21:06 2024

    [wasm][sandbox] Check signatures when importing tables
    
    Importing function tables must perform the same checks we already
    do during table.set.
    
    Bug: 336507783
    Change-Id: I720365f0f2606251b9e083cc7e421030d37d46c7
    Fixed: 348793147
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5659606
    Auto-Submit: Jakob Kummerow <jkummerow@chromium.org>
    Commit-Queue: Clemens Backes <clemensb@chromium.org>
    Commit-Queue: Jakob Kummerow <jkummerow@chromium.org>
    Reviewed-by: Clemens Backes <clemensb@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#94692}

M       src/wasm/module-instantiate.cc
M       src/wasm/wasm-objects.cc
M       src/wasm/wasm-objects.h
M       test/mjsunit/mjsunit.status
A       test/mjsunit/sandbox/wasm-table-import.js
M       test/mjsunit/sandbox/wasm-table-sigcheck.js
M       test/mjsunit/wasm/wasm-module-builder.js

https://chromium-review.googlesource.com/5659606


### jk...@chromium.org (2024-06-28)

Following up on #7: That other variant does indeed exist, and is slightly more involved to fix, but also less urgent because Type Reflection is still behind a flag. Patch coming up.

### am...@chromium.org (2024-07-03)

re-opening since it look the change to address the variant is still WIP, so this isn't fully resolved as of yet 

### se...@gmail.com (2024-07-04)

Regarding <https://chromium-review.googlesource.com/c/v8/v8/+/5675271>, are we sure that we don't need to acquire `mutex_` in `TypeCanonicalizer::LookupSignature()`? I think this might race with concurrent writers.

### ap...@google.com (2024-07-10)

Project: v8/v8
Branch: main

commit 420911ec384016858d9412664c93f52f0ff794cc
Author: Jakob Kummerow <jkummerow@chromium.org>
Date:   Wed Jul 10 17:41:47 2024

    [wasm][sandbox] Check WasmJSFunctions in imported tables
    
    Functions created via `new WebAssembly.Function` take a different
    code path, so they need their own copy of a sandbox-proof type
    check when they are passed to module instantiation as elements in
    a function table.
    This is accomplished by having WasmJSFunctionData store its
    `canonical_sig_index` instead of an on-heap serialized signature.
    
    Bug: 336507783, 348793147
    Change-Id: I19e8bbf847050239cf4cf5152aa9dc3c0fa323ba
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5675271
    Commit-Queue: Jakob Kummerow <jkummerow@chromium.org>
    Reviewed-by: Clemens Backes <clemensb@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#94946}

M       src/diagnostics/objects-printer.cc
M       src/heap/factory.cc
M       src/heap/factory.h
M       src/wasm/canonical-types.cc
M       src/wasm/canonical-types.h
M       src/wasm/module-instantiate.cc
M       src/wasm/wasm-engine.cc
M       src/wasm/wasm-js.cc
M       src/wasm/wasm-objects.cc
M       src/wasm/wasm-objects.h
M       src/wasm/wasm-objects.tq
M       test/mjsunit/sandbox/wasm-table-import.js
A       test/mjsunit/sandbox/wasm-table-wasmjsfunction.js

https://chromium-review.googlesource.com/5675271


### ap...@google.com (2024-07-10)

Project: v8/v8
Branch: main

commit e37b630102f0e757762d3f450f1646da97a7e4dd
Author: Ilya Rezvov <irezvov@chromium.org>
Date:   Wed Jul 10 19:57:25 2024

    Revert "[wasm][sandbox] Check WasmJSFunctions in imported tables"
    
    This reverts commit 420911ec384016858d9412664c93f52f0ff794cc.
    
    Reason for revert: LookupSignature accesses canonical_sigs_ without acquiring mutex. It causes a TSAN failure https://ci.chromium.org/ui/p/v8/builders/ci/V8%20Linux64%20TSAN%20-%20isolates/31337/overview
    
    Original change's description:
    > [wasm][sandbox] Check WasmJSFunctions in imported tables
    >
    > Functions created via `new WebAssembly.Function` take a different
    > code path, so they need their own copy of a sandbox-proof type
    > check when they are passed to module instantiation as elements in
    > a function table.
    > This is accomplished by having WasmJSFunctionData store its
    > `canonical_sig_index` instead of an on-heap serialized signature.
    >
    > Bug: 336507783, 348793147
    > Change-Id: I19e8bbf847050239cf4cf5152aa9dc3c0fa323ba
    > Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5675271
    > Commit-Queue: Jakob Kummerow <jkummerow@chromium.org>
    > Reviewed-by: Clemens Backes <clemensb@chromium.org>
    > Cr-Commit-Position: refs/heads/main@{#94946}
    
    Bug: 336507783, 348793147
    Change-Id: I08f8a712af38907182018b626a962d5415ca3aff
    No-Presubmit: true
    No-Tree-Checks: true
    No-Try: true
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5691711
    Auto-Submit: Ilya Rezvov <irezvov@chromium.org>
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Commit-Queue: Ilya Rezvov <irezvov@chromium.org>
    Reviewed-by: Ilya Rezvov <irezvov@chromium.org>
    Owners-Override: Ilya Rezvov <irezvov@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#94949}

M       src/diagnostics/objects-printer.cc
M       src/heap/factory.cc
M       src/heap/factory.h
M       src/wasm/canonical-types.cc
M       src/wasm/canonical-types.h
M       src/wasm/module-instantiate.cc
M       src/wasm/wasm-engine.cc
M       src/wasm/wasm-js.cc
M       src/wasm/wasm-objects.cc
M       src/wasm/wasm-objects.h
M       src/wasm/wasm-objects.tq
M       test/mjsunit/sandbox/wasm-table-import.js
D       test/mjsunit/sandbox/wasm-table-wasmjsfunction.js

https://chromium-review.googlesource.com/5691711


### jk...@chromium.org (2024-07-11)

#12: Good catch, TSan agrees. Reland in flight: <https://chromium-review.googlesource.com/c/v8/v8/+/5691757>.

### ap...@google.com (2024-07-11)

Project: v8/v8
Branch: main

commit 5de108340f21afe181e5b6dc636a07e58721d5ff
Author: Jakob Kummerow <jkummerow@chromium.org>
Date:   Thu Jul 11 14:53:30 2024

    Reland "[wasm][sandbox] Check WasmJSFunctions in imported tables"
    
    This is a reland of commit 420911ec384016858d9412664c93f52f0ff794cc
    Changed in reland: added MutexGuard
    
    Original change's description:
    > [wasm][sandbox] Check WasmJSFunctions in imported tables
    >
    > Functions created via `new WebAssembly.Function` take a different
    > code path, so they need their own copy of a sandbox-proof type
    > check when they are passed to module instantiation as elements in
    > a function table.
    > This is accomplished by having WasmJSFunctionData store its
    > `canonical_sig_index` instead of an on-heap serialized signature.
    >
    > Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5675271
    
    Bug: 336507783, 348793147
    Change-Id: I25a6e24a95b302feb4c835308bbdf4f4f0a40e08
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5691757
    Reviewed-by: Matthias Liedtke <mliedtke@chromium.org>
    Auto-Submit: Jakob Kummerow <jkummerow@chromium.org>
    Commit-Queue: Jakob Kummerow <jkummerow@chromium.org>
    Commit-Queue: Matthias Liedtke <mliedtke@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#94979}

M       src/diagnostics/objects-printer.cc
M       src/heap/factory.cc
M       src/heap/factory.h
M       src/wasm/canonical-types.cc
M       src/wasm/canonical-types.h
M       src/wasm/module-instantiate.cc
M       src/wasm/wasm-engine.cc
M       src/wasm/wasm-js.cc
M       src/wasm/wasm-objects.cc
M       src/wasm/wasm-objects.h
M       src/wasm/wasm-objects.tq
M       test/mjsunit/sandbox/wasm-table-import.js
A       test/mjsunit/sandbox/wasm-table-wasmjsfunction.js

https://chromium-review.googlesource.com/5691757


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

Congratulations Seunghyun! Thank you for your efforts digging into the V8 sandbox -- nice work!

### pe...@google.com (2024-10-18)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/348793147)*
