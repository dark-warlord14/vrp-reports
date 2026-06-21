# Wasm Liftoff stack corruption on eager compilation + JS interop prototype setup optimization

| Field | Value |
|-------|-------|
| **Issue ID** | [489109716](https://issues.chromium.org/issues/489109716) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>WebAssembly |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | se...@gmail.com |
| **Assignee** | jk...@chromium.org |
| **Created** | 2026-03-03 |
| **Bounty** | $50,000.00 |

## Description

### VULNERABILITY DETAILS

> Disclaimer: This bug is introduced from a feature/optimization work for Wasm Custom Descriptors, specifically the JS interop part `configureAll()`. However, **triggering the bug does not require JS interop to be enabled; instead, it requires Wasm eager compilation**. Reporting this as a vulnerability, but AFAICT such configs are not standard.

#### Summary

`PrototypeSetupSequenceDetector::DetectSequence()` unconditionally matches if the target import function is not yet instantiated (`WellKnownImport::kUninstantiated`). This results in inconsistent stack merge states, leading to arbitrary uncaged read/write.

#### Details

Wasm Custom Descriptors, more specifically its JS interop part, introduces a well-known import `configureAll` in the `wasm:js-prototypes` module namespace for performant initialization of the idiomatic use of custom descriptors with JS prototypes and vtables.

Lfitoff further implements a lookahead pattern-matcher `PrototypeSetupSequenceDetector::DetectSequence()` that runs on `array.new_segment` to parse a specific sequence of Wasm opcodes that is known to be a `configureAll()` call. This embeds a conditional branch to directly call `Builtin::kWasmConfigureAllPrototypesOpt` and avoid `array.new_segment` if at runtime we know that the import is indeed `WellKnownImport::kConfigureAllPrototypes`. This runtime check is implemented because Liftoff is shared across different instantiations of the module, and one instantiation may have the expected WKI whereas another could be a different function.

> Note that there was also an indexing bug in this runtime check (underlying WKI array was assumed to be `FixedAddressArray` instead of `FixedArray`), which has been fixed at <https://crrev.com/c/7614269>.

The pattern matcher uses `PrototypeSetupSequenceDetector::ExpectCallWellKnownImport()` which returns true when:

- WKI is known to be the expected one (`WellKnownImport::kConfigureAllPrototypes` for our case)
- WKI is not yet known (`WellKnownImport::kUninstantiated`)

The second case is interesting - it is not `kGeneric` which indicates polymorphic import. Instead, it is `kUninstantiated` which seems to be reachable only when we have not instantiated the underlying Wasm module, as the first instantiation will set WKI status to whatever value that is not `kUninstantiated`. This means that **we can reach this condition when we can eagerly compile the target Wasm function, regardless of whether or not we can use `WellKnownImport::kConfigureAllPrototypes` via JS interop**.

Also, the target function signature is not checked anywhere for `kUninstantiated` case. However, we're injecting an if-else split and merge assuming that its function signature is compatible with the actual function signature of `configureAll()`. This leads to inconsistent Liftoff stack state even when the runtime WKI check fails and we take the else case, leading to invalid codegen that allows manipulating the stack state to trigger arbitrary read/writes by e.g. swapping i64 with ref.

Now back to the question: how can we trigger eager Wasm function compilation? Some conditions are:

- `--no-wasm-lazy-compilation` and similar variants that disable Wasm lazy compilation
- `--experimental-wasm-compilation-hints` + compilation priority set to eagerly compile to Liftoff

AFAICT these configurations does not seem to be the default for any of the builds and environments Chrome considers standard, but pedantically speaking `--no-wasm-lazy-compilation` is not an experimental config & enabling Wasm compilation hints proposal may inadvertently make this seemingly unrelated bug exploitable.

---

A recommended fix would be to:

- Do a function signature check at `PrototypeSetupSequenceDetector::ExpectCallWellKnownImport()`
- Guard the whole sequence matcher logic behind `v8_flags.experimental_wasm_js_interop`, as this is a JS interop feature that is being exposed even without JS interops being enabled

### VERSION

V8: Tested on latest V8 component revision 105538:

- d8-asan-linux-debug-v8-component-105538 (dcheck)
- d8-linux-release-v8-component-105538 (crash, uncaged write)
- d8-asan-no-inline-linux-release-v8-component-105538 (crash, uncaged write)

Introduced on <https://crrev.com/c/6779123>.

### REPRODUCTION CASE

Attached as `poc-js-interop-eager-compile.js` which crashes on a fully arbitrary write of value 0x434343434343 to raw pointer 0x424242424242 on release builds, or crashes on a DCHECK() on debug builds. Helper scripts are inlined, so jump to around L2800 for the actual PoC. Run with either `--no-wasm-lazy-compilation` or `--experimental-wasm-compilation-hints` enabled.

### FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION

Type of crash: Renderer

### CREDIT INFORMATION

Reporter credit: Seunghyun Lee (@0x10n) of CMU CSD / CyLab

## Attachments

- [poc-js-interop-eager-compile.js](attachments/poc-js-interop-eager-compile.js) (text/javascript, 86.0 KB)
- [poc2.js](attachments/poc2.js) (text/javascript, 4.9 KB)
- [poc3.js](attachments/poc3.js) (text/javascript, 5.0 KB)

## Timeline

### me...@google.com (2026-03-06)

Thanks for the report. Would you mind splitting the files? I moved the actual exploit code into a separate file and reused the other files from Chromium repo, but it seems your PoC doesn't have start() defined?

### se...@gmail.com (2026-03-06)

AFAIK ClusterFuzz needs a single file or the relevant files bundled together, so I just inline them all. In the original PoC I modified the inlined `prototype-setup-builder.js` to create a custom `start()` function with appropriate code/signature, but I'll just reattach a PoC with the mjsunit-like `d8.file.execute()` format and do the appropriate modifications separately in the PoC.

### pe...@google.com (2026-03-06)

Thank you for providing more feedback. Adding the requester to the CC list.

### cl...@appspot.gserviceaccount.com (2026-03-06)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5607048599240704.

### me...@google.com (2026-03-06)

Thanks. Yes, indeed, CF requires a bundle, but we are being extra cautious to keep the uploads smaller and auditable.

### cl...@appspot.gserviceaccount.com (2026-03-07)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4844115103514624.

### cl...@appspot.gserviceaccount.com (2026-03-07)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6408599890755584.

### ch...@google.com (2026-03-07)

Setting milestone because of s0/s1 severity.

### 24...@project.gserviceaccount.com (2026-03-08)

Detailed Report: https://clusterfuzz.com/testcase?key=6408599890755584

Fuzzer: None
Job Type: linux_asan_d8
Platform Id: linux

Crash Type: UNKNOWN WRITE
Crash Address: 0x424242424242
Crash State:
  Builtins_JSToWasmWrapperAsm
  Builtins_JSToWasmWrapper
  Builtins_InterpreterEntryTrampoline
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8&range=101616:101617

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6408599890755584

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary.

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


A recommended severity was added to this bug. Please change the severity if it is inaccurate.

### cl...@chromium.org (2026-03-09)

Thanks for this report!

Yes, this should have no impact right now, but since we were not aware of this issue we could easily have shipped e.g. compilation hints and thereby exposing this issue.

So thanks for filing this now and not only when it was reachable in production! IMO this should be rewarded like a stable-impacting issue.

In a DCHECK-enabled build, we actually run into this DCHECK at Liftoff compile time:

```
#
# Fatal error in ../../src/wasm/baseline/liftoff-compiler.cc, line 8080
# Debug check failed: decoder->stack_size() == stack_depth + 1 (7 vs. 9).
#

```

### jk...@chromium.org (2026-03-09)

Fun bug! I think part of the analysis is incorrect though: this doesn't have anything to do with the signature of the imported function. The bug is in this snippet:

```
          uint32_t stack_depth = __ cache_state() -> stack_height();
          // The decoder has already dropped start/length and pushed the array.
          DCHECK_EQ(decoder->stack_size(), stack_depth + 1);
          prototype_setup_end_->state =
              __ MergeIntoNewState(__ num_locals(), 0, stack_depth);

```

`__ cache_state()->stack_height()` returns the size of the value stack including locals, whereas `__ MergeIntoNewState(..., stack_depth)` expects the stack depth *without* locals. That discrepancy is what causes the bad stack merge.
Adding `- __ num_locals()` to the first line (i.e. to the computation of `stack_depth`) fixes the `DCHECK`. (Which does then make the repro run into a different DCHECK, but that one's harmless I believe.)

That said, I agree that the suggested fixes are useful in their own right, even though they're not fixes for this bug:

- Including the signature of the expected import in the pattern matcher makes it more selective at little cost, which is not important but an improvement.
- Guarding the whole machinery behind its corresponding flag is also generally good practice. (The critical thing, which is the fast path, can't be triggered without the right feature flags anyway; but as this issue demonstrates, that doesn't necessarily imply that the fallback is bug free...)

Patch coming up.

### se...@gmail.com (2026-03-09)

Re #12: That makes more sense, thanks for the correction. But something tells me that the signature check should also be present, we're merging & stealing the merge state assuming that the stack state is equivalent to calling a function signature compatible with `configureAll()`. What happens if the function call returns something, will we not have a discrepancy with decoder stack vs. liftoff stack?

### se...@gmail.com (2026-03-09)

Re #12, #13: Yup, the issue still persists after the proposed patch in #12 (see `poc3.js`), confirmed on a build with `- __ num_locals()` patch. My naive guess is that both #12 (local count) and #13 (signature match) needs to be fixed?

---

Note: `poc3.js` is just shifts and paddings modified from the previous PoCs so that overlap the returned structrefs with stack spilled `0x1111...` constants

### jk...@chromium.org (2026-03-09)

#13, #14: Yes, I just figured that out too. I was going to add the signature check anyway (as I said in #12, it's just the right thing to do); turns out it's actually more important than I first realized. Thanks, as always, for your diligence!

### jk...@chromium.org (2026-03-09)

Fix in flight: <https://chromium-review.googlesource.com/c/v8/v8/+/7650014>

### dx...@google.com (2026-03-10)

Project: v8/v8  

Branch:  main  

Author:  Jakob Kummerow [jkummerow@chromium.org](mailto:jkummerow@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7650014>

[wasm-custom-desc] Fix configureAll fast path

---


Expand for full commit details
```
     
    For incorrect signatures of the imported function, Liftoff could 
    get confused about its stack state. 
     
    Fixed: 489109716 
    Change-Id: I1909b158dc5a693f0a06065aeca5fe0f0fbd6de3 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7650014 
    Reviewed-by: Clemens Backes <clemensb@chromium.org> 
    Commit-Queue: Jakob Kummerow <jkummerow@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#105700}

```

---

Files:

- M `src/wasm/baseline/liftoff-assembler.cc`
- M `src/wasm/baseline/liftoff-compiler.cc`
- A `test/mjsunit/regress/wasm/regress-489109716.js`

---

Hash: [a58753bac7b1f80d53cdf86c8a61842c8e05b386](https://chromiumdash.appspot.com/commit/a58753bac7b1f80d53cdf86c8a61842c8e05b386)  

Date: Mon Mar 9 21:04:30 2026


---

### sp...@google.com (2026-04-08)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $50000.00 for this report.

Rationale for this decision:
High quality. Renderer RCE / memory corruption in a sandboxed process


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### se...@gmail.com (2026-04-08)

Re [comment#18](https://issues.chromium.org/issues/489109716#comment18): Please donate the bounty to a charity of Chrome VRP / Google's choice, thanks!

### ch...@google.com (2026-06-17)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### dj...@gmail.com (2026-06-18)

deleted

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/489109716)*
