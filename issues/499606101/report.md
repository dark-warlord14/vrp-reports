# OOB Write in V8 TryMatchLoadStoreShift on Mac arm64 (OOB read on non-Mac arm64)

| Field | Value |
|-------|-------|
| **Issue ID** | [499606101](https://issues.chromium.org/issues/499606101) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Compiler>Turboshaft |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | he...@gmail.com |
| **Assignee** | ml...@chromium.org |
| **Created** | 2026-04-05 |
| **Bounty** | $11,000.00 |

## Description

### Summary

Arm64 Wasm memory accesses can miscompile 32-bit shifted indices in [`TryMatchLoadStoreShift`](https://source.chromium.org/chromium/chromium/src/+/main:v8/src/compiler/backend/arm64/instruction-selector-arm64.cc;l=578-606). When the index has the shape `ChangeUint32ToUint64(ShiftLeft(Word32))`, the selector folds it into `kMode_Operand2_R_UXTW_LSL_I`, and [`MemoryOperand`](https://source.chromium.org/chromium/chromium/src/+/main:v8/src/compiler/backend/arm64/code-generator-arm64.cc;l=207-226) lowers that mode as `MemOperand(base, Windex, UXTW, shift)`. That computes a zero-extend-before-shift address, but Wasm `i32.shl` semantics require the shift to happen in 32-bit arithmetic with wraparound before the value is widened for addressing. As a result, the Wasm loads and stores that should touch offset `0` instead dereference high addresses and crash with OOB writes.

### Details

The bug is in the arm64 address calculation, not in Wasm bounds checking itself. A minimal trigger uses a Wasm function shaped like `local.get 0; i32.wrap_i64; i32.const <scale>; i32.shl; <load/store>`. For an input such as `0x80000000n` and a 4-byte access, Wasm computes `(0x80000000 << 2) mod 2^32 == 0`, so the effective byte offset should be `0`.

Both [`EmitLoad`](https://source.chromium.org/chromium/chromium/src/+/main:v8/src/compiler/backend/arm64/instruction-selector-arm64.cc;l=1014-1093) and [`VisitStore`](https://source.chromium.org/chromium/chromium/src/+/main:v8/src/compiler/backend/arm64/instruction-selector-arm64.cc;l=1462-1512) call [`TryMatchLoadStoreShift`](https://source.chromium.org/chromium/chromium/src/+/main:v8/src/compiler/backend/arm64/instruction-selector-arm64.cc;l=578-606) and thus is reachable from Wasm reads and writes.

```
bool TryMatchLoadStoreShift(Arm64OperandGenerator* g,
                            InstructionSelector* selector,
                            MemoryRepresentation rep, OpIndex node,
                            OpIndex index, InstructionOperand* index_op,
                            InstructionOperand* shift_immediate_op,
                            AddressingMode* mode) {
  if (!selector->CanCover(node, index)) return false;
  if (const ChangeOp* change =
          selector->Get(index).TryCast<Opmask::kChangeUint32ToUint64>();
      change && selector->CanCover(index, change->input())) {
    const ShiftOp* shift =
        selector->Get(change->input()).TryCast<Opmask::kShiftLeft>();
    if (shift && shift->rep == RegisterRepresentation::Word32() &&
        g->CanBeLoadStoreShiftImmediate(shift->right(), rep)) {
      *index_op = g->UseRegister(shift->left());
      *shift_immediate_op = g->UseImmediate(shift->right());
      *mode = kMode_Operand2_R_UXTW_LSL_I;
      return true;
    }
  }
  ...
}

```

[`MemoryOperand`](https://source.chromium.org/chromium/chromium/src/+/main:v8/src/compiler/backend/arm64/code-generator-arm64.cc;l=207-226) then lowers that mode directly into an addressing form that zero-extends the 32-bit index register and applies the shift in the address calculation:

```
MemOperand MemoryOperand(size_t index = 0) {
  switch (AddressingModeField::decode(instr_->opcode())) {
    ...
    case kMode_Operand2_R_LSL_I:
      return MemOperand(InputRegister(index + 0), InputRegister(index + 1),
                        LSL, InputInt32(index + 2));
    case kMode_Operand2_R_UXTW_LSL_I:
      return MemOperand(InputRegister(index + 0), InputRegister32(index + 1),
                        UXTW, InputInt32(index + 2));
    ...
  }
}

```

That transformation is not semantics-preserving for Wasm `i32.shl`. The Wasm value should be:

```
zero_extend_64((index32 << shift) mod 2^32)

```

but the generated address mode implements:

```
(zero_extend_64(index32) << shift)

```

Those differ whenever the 32-bit left shift overflows. For example, with `index32 = 0x80000000` and `shift = 2`, the correct Wasm result is `0`, but the selected arm64 addressing mode computes `0x200000000` before the base is added. In practice that becomes a high invalid address and thus produce the OOB write for the `store` op.

This is reproducible across multiple load/store classes, which matches the shared selector/codegen path, we can achieve the OOB read/write for:

- `i32.load`
- `i64.load`
- `f32.load`
- `f64.load`
- `i32.store`
- `i64.store`
- `f32.store`
- `f64.store`
- `i64.load32_u`
- `i64.load32_s`
- `i64.store32`

The same root cause also reaches SIMD because [`kArm64LdrQ` / `kArm64StrQ`](https://source.chromium.org/chromium/chromium/src/+/main:v8/src/compiler/backend/arm64/code-generator-arm64.cc;l=2592-2598) use the same `i.MemoryOperand()` path with `s128.load` / `s128.store` using the index `0x20000000n`.

### Bisection

This issue is introduced by commit 3282ef156eff5e348fd7cade8a417d28367eaba1 (<https://chromium-review.googlesource.com/c/v8/v8/+/7705844>), landed on March 30, 2026 (exists for more than 2 days).

This change intended to re-enable an ARM64 load/store optimization by folding ChangeUint32ToUint64(ShiftLeft(Word32)) into kMode\_Operand2\_R\_UXTW\_LSL\_I. However, that lowering is not correct for Wasm: it computes zero-extend-before-shift, while Wasm requires 32-bit shift-with-wraparound before widening. As a result, overflowing indices are miscompiled into high out-of-bounds addresses.

### Reproduction

Build the ToT d8 (on commit f9659283a5f8d42b3c09228cf5df606fcaf47a3d) with the following args:

```
is_component_build = false
is_debug = false
v8_enable_sandbox = false
v8_enable_backtrace = true
dcheck_always_on = true
is_asan=true
v8_static_library=true

```

Run d8 on arm Mac:

```
./d8 --wasm-eager-tier-up-function=0 --wasm-sync-tier-up --no-wasm-lazy-compilation poc.js

```

You would observe the OOB write crash shown as `log.txt`

### Suggested Fix

Do not fold `ChangeUint32ToUint64(ShiftLeft(Word32))` into `kMode_Operand2_R_UXTW_LSL_I` in `TryMatchLoadStoreShift`.

## Attachments

- [log.txt](attachments/log.txt) (text/plain, 1.8 KB)
- [poc.js](attachments/poc.js) (text/javascript, 517 B)

## Timeline

### za...@google.com (2026-04-06)

[security shepherd]This appears to be a V8 issue. Routing to the current V8 security shepherd for investigation.

### ch...@google.com (2026-04-07)

This V8 bug has been marked as either a release blocker or a vulnerability bug. V8 bugs affect all OSs supported by Chrome, so the OS field has been updated to reflect this. Please update the bug with the correct OS field if it only affects a subset of OSes.

### is...@chromium.org (2026-04-07)

Thank you for the report. Assigning to the author of the code snippet.

### he...@gmail.com (2026-04-07)

Thanks. This is a very great primitive since the write address can be easily controlled, as well as the written value; and if it is not duplicated (7 days have already been past since the introduced commit date), I'm going to further working on the controlled arbitrary address write with arbitrary value POC.

Many thanks!

### ml...@chromium.org (2026-04-07)

From the arm64 documentation:

```
    // Note the extended width of the intermediate value and
    // that sign extension occurs from bit <len+shift-1>, not
    // from bit <len-1>. This is equivalent to the instruction
    //   [SU]BFIZ Rtmp, Rreg, #shift, #len
    // It may also be seen as a sign/zero extend followed by a shift:
    //   LSL(Extend(val<len-1:0>, N, unsigned), shift);

```

So we zero-extend from a 34, 35 bit value apparently (depending on the actual shift size), so the claim that this causes OOB-accesses seems to be correct.

However, this is not the behavior I'm observing with the arm64-simulator, it "just works" as if it was doing a 32 bit shift followed by a zero-extension on that value. Given that ClusterFuzz only supports the simulator, this sounds like a bug that would not be discoverable by most of our fuzzers and ClusterFuzz won't be able to verify that this issue reproduces.

### ml...@chromium.org (2026-04-07)

Actually, the simulator is correct, the problem is that with the store we do explicit bounds checks on stores unless the hardware is Mac: <https://source.chromium.org/chromium/chromium/src/+/main:v8/src/wasm/compilation-environment.h;l=38;drc=2f016e2364c0281c29e9dc0f8e9224f5278838f7>

```
#if V8_TARGET_ARCH_ARM64 && !V8_OS_MACOS
constexpr bool kPartialOOBWritesAreNoops = false;
#else
constexpr bool kPartialOOBWritesAreNoops = true;
#endif

```

With explicit bounds checks, this will not reproduce because the optimization doesn't apply as `CanCover()` fails. (A load reproduces the issue on non-Mac devices including in the simulator.)

I'd argue that we might want to reconsider what to do about this, given that this means that there might be all kinds of bugs that are only ever reproducible on Mac which might make it hard to impossible for fuzzers to find specific bugs.

Anyways, it seems that the correct solution is reverting the change.

### ml...@chromium.org (2026-04-07)

Note: If we just add the `0x80000000n` as an input to the `load-shift32.js` test case that I added in the change where I introduced this new addressing mode, we get the crash for the OOB read access...

I'll add that to the test case and not revert the test case, so we'll keep the (extended) test case but not the optimization.

### ml...@chromium.org (2026-04-07)

> Thanks. This is a very great primitive since the write address can be easily controlled, as well as the written value; and if it is not duplicated (7 days have already been past since the introduced commit date), I'm going to further working on the controlled arbitrary address write with arbitrary value POC.
> 
> Many thanks!

Note that the shift amount should be limited to 3 (for an `int64` store). You can start with `std::numeric_limits<uint32_t>::max()`, then do the shift by 3. 4GB are the memory cage and are inaccessible. Beyond that you have an arbitrary read-write primitive for anything that is allocated "behind" the memory. I don't exactly know how the memory is managed and fragmented inside the 1TB V8 sandbox cage and where the Wasm memories end up, so getting from this primitive to arbitrary (V8) in-sandbox or out-of-sandbox memory corruption would be very interesting to demonstrate the severity of this bug.

Due to the limited shift amount (`CanBeLoadStoreShiftImmediate()`), the V8 sandbox should still help here, so for process-wide memory corruption this should require a V8 sandbox bypass AFAICT.

### cl...@appspot.gserviceaccount.com (2026-04-07)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5434006816456704.

### dx...@google.com (2026-04-07)

Project: v8/v8  

Branch:  main  

Author:  Matthias Liedtke [mliedtke@chromium.org](mailto:mliedtke@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7735843>

Revert "[compiler][arm64] Use UXTW LSL addressing mode for zero-extended shifts"

---


Expand for full commit details
```
     
    This reverts commit 3282ef156eff5e348fd7cade8a417d28367eaba1. 
     
    Reason for revert: This optimization was incorrect. 
    In the end, it doesn't seem like we have an addressing mode that does 
    exactly what we'd need here. 
     
    Manual change: Keep the test case and add yet another case to it. 
    While the optimization will be disabled, we should keep the test cases 
    that would crash if the optimization was re-added. 
     
    Original change's description: 
    > [compiler][arm64] Use UXTW LSL addressing mode for zero-extended shifts 
    > 
    > The recent fix for a bug where 32-bit shifts were incorrectly replaced 
    > with 64-bit LSL addressing modes disabled the optimization entirely. 
    > This change re-enables it by using the UXTW LSL addressing mode, which 
    > correctly zero-extends the 32-bit register before performing the shift 
    > for the memory address calculation. 
    > 
    > Bug: 496776572, 497065732 
    > Change-Id: I4f859dc97ae3a8caedb6d2db766faaf15fee8879 
    > Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7705844 
    > Reviewed-by: Sam Parker-Haynes <sam.parker@arm.com> 
    > Reviewed-by: Darius Mercadier <dmercadier@chromium.org> 
    > Commit-Queue: Matthias Liedtke <mliedtke@chromium.org> 
    > Cr-Commit-Position: refs/heads/main@{#106142} 
     
    Bug: 496776572, 497065732 
    Fixed: 499606101 
    Change-Id: Ifb3e701940a90b49af8f328ff47f54dc9ca9727d 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7735843 
    Reviewed-by: Darius Mercadier <dmercadier@chromium.org> 
    Commit-Queue: Darius Mercadier <dmercadier@chromium.org> 
    Auto-Submit: Matthias Liedtke <mliedtke@chromium.org> 
    Commit-Queue: Matthias Liedtke <mliedtke@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#106286}

```

---

Files:

- M `src/compiler/backend/arm64/code-generator-arm64.cc`
- M `src/compiler/backend/arm64/instruction-codes-arm64.h`
- M `src/compiler/backend/arm64/instruction-selector-arm64.cc`
- M `test/mjsunit/wasm/load-shift32.js`
- M `test/unittests/compiler/arm64/turboshaft-instruction-selector-arm64-unittest.cc`

---

Hash: [c642c7279120c75952c90e8ba24268be347eacc3](https://chromiumdash.appspot.com/commit/c642c7279120c75952c90e8ba24268be347eacc3)  

Date: Tue Apr 7 13:17:15 2026


---

### cl...@appspot.gserviceaccount.com (2026-04-07)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5824343846191104.

### cl...@appspot.gserviceaccount.com (2026-04-07)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6551830171516928.

### cl...@appspot.gserviceaccount.com (2026-04-07)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6213484526206976.

### ml...@chromium.org (2026-04-07)

I guess, even on the most recent ClusterFuzz upload I missed something (in this case providing a commit ID).

1. Use the right job
2. Explicitly pass the needed non-default flags
3. Set the commit SHA that is known to have the crash
4. Don't use the `WasmModuleBuilder` because that one only works on very few ClusterFuzz jobs

Not sure if I missed anything else, the issue is in 148, so it shouldn't be that bad not to have the ClusterFuzz bisection / investigation for this.

### ch...@google.com (2026-04-08)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-04-08)

This is sufficiently serious that it should be merged to M148. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M148. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Security Merge Request:

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

### is...@chromium.org (2026-04-08)

Temporarily removing merge request to M148, because we've already got tons of merge request issues because of automation bug in buganizer.

### ch...@google.com (2026-04-08)

**M148** merge request created. **Please update [crbug/500600553](https://crbug.com/500600553) to have this merge reviewed.**

### ch...@google.com (2026-04-08)

**M148** merge request created. **Please update [crbug/500600706](https://crbug.com/500600706) to have this merge reviewed.**

### ch...@google.com (2026-04-08)

**M148** merge request created. **Please update [crbug/500601715](https://crbug.com/500601715) to have this merge reviewed.**

### ch...@google.com (2026-04-08)

**M148** merge request created. **Please update [crbug/500601069](https://crbug.com/500601069) to have this merge reviewed.**

### ch...@google.com (2026-04-08)

**M148** merge request created. **Please update [crbug/500601727](https://crbug.com/500601727) to have this merge reviewed.**

### ch...@google.com (2026-04-08)

**M148** merge request created. **Please update [crbug/500602381](https://crbug.com/500602381) to have this merge reviewed.**

### ch...@google.com (2026-04-08)

**M148** merge request created. **Please update [crbug/500602225](https://crbug.com/500602225) to have this merge reviewed.**

### ch...@google.com (2026-04-08)

**M148** merge request created. **Please update [crbug/500602565](https://crbug.com/500602565) to have this merge reviewed.**

### ch...@google.com (2026-04-08)

**M148** merge request created. **Please update [crbug/500602501](https://crbug.com/500602501) to have this merge reviewed.**

### ch...@google.com (2026-04-08)

**M148** merge request created. **Please update [crbug/500603365](https://crbug.com/500603365) to have this merge reviewed.**

### ch...@google.com (2026-04-08)

**M148** merge request created. **Please update [crbug/500604480](https://crbug.com/500604480) to have this merge reviewed.**

### ch...@google.com (2026-04-08)

**M148** merge request created. **Please update [crbug/500604387](https://crbug.com/500604387) to have this merge reviewed.**

### ch...@google.com (2026-04-08)

**M148** merge request created. **Please update [crbug/500604186](https://crbug.com/500604186) to have this merge reviewed.**

### ch...@google.com (2026-04-08)

**M148** merge request created. **Please update [crbug/500605494](https://crbug.com/500605494) to have this merge reviewed.**

### ch...@google.com (2026-04-08)

**M148** merge request created. **Please update [crbug/500604788](https://crbug.com/500604788) to have this merge reviewed.**

### dr...@chromium.org (2026-04-08)

Sorry for the noise folks - we believe this is a novel edge case in our automation (https://crbug.com/500636350). I'll clean up the excess merges now.

### he...@gmail.com (2026-04-09)

re [comment#9](https://issues.chromium.org/issues/499606101#comment9): yes, it's true. It is a OOB write (e.g., cross-WASM memory write) but with some target address limitations under the current V8 sandbox. Therefore, I failed to provide the arbitrary address r/w for this case due to the sandbox limitation (it needs to further combine with a sandbox bypass issue).

Thank you very much!

### ml...@chromium.org (2026-04-09)

> It is a OOB write (e.g., cross-WASM memory write) but with some target address limitations under the current V8 sandbox.

Writing into another Wasm-memory isn't a security issue from a V8 / Chrome perspective as both contain fully user-controlled arbitrary data.

However I suspect that besides the already user-controlled data bytes of a Wasm memory there can be also other objects allocated in the reachable address space, so it sounds reasonable to assume that this bug can be used to achieve arbitrary in-sandbox corruption.

### dx...@google.com (2026-04-09)

Project: v8/v8  

Branch:  refs/branch-heads/14.8  

Author:  Matthias Liedtke [mliedtke@chromium.org](mailto:mliedtke@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7740983>

[M148] Revert "[compiler][arm64] Use UXTW LSL addressing mode for zero-extended shifts"

---


Expand for full commit details
```
     
    Original change's description: 
    > Revert "[compiler][arm64] Use UXTW LSL addressing mode for zero-extended shifts" 
    > 
    > This reverts commit 3282ef156eff5e348fd7cade8a417d28367eaba1. 
    > 
    > Reason for revert: This optimization was incorrect. 
    > In the end, it doesn't seem like we have an addressing mode that does 
    > exactly what we'd need here. 
    > 
    > Manual change: Keep the test case and add yet another case to it. 
    > While the optimization will be disabled, we should keep the test cases 
    > that would crash if the optimization was re-added. 
    > 
    > Original change's description: 
    > > [compiler][arm64] Use UXTW LSL addressing mode for zero-extended shifts 
    > > 
    > > The recent fix for a bug where 32-bit shifts were incorrectly replaced 
    > > with 64-bit LSL addressing modes disabled the optimization entirely. 
    > > This change re-enables it by using the UXTW LSL addressing mode, which 
    > > correctly zero-extends the 32-bit register before performing the shift 
    > > for the memory address calculation. 
    > > 
    > > Bug: 496776572, 497065732 
    > > Change-Id: I4f859dc97ae3a8caedb6d2db766faaf15fee8879 
    > > Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7705844 
    > > Reviewed-by: Sam Parker-Haynes <sam.parker@arm.com> 
    > > Reviewed-by: Darius Mercadier <dmercadier@chromium.org> 
    > > Commit-Queue: Matthias Liedtke <mliedtke@chromium.org> 
    > > Cr-Commit-Position: refs/heads/main@{#106142} 
    > 
    > Bug: 496776572, 497065732 
    > Fixed: 499606101 
    > Change-Id: Ifb3e701940a90b49af8f328ff47f54dc9ca9727d 
    > Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7735843 
    > Reviewed-by: Darius Mercadier <dmercadier@chromium.org> 
    > Commit-Queue: Darius Mercadier <dmercadier@chromium.org> 
    > Auto-Submit: Matthias Liedtke <mliedtke@chromium.org> 
    > Commit-Queue: Matthias Liedtke <mliedtke@chromium.org> 
    > Cr-Commit-Position: refs/heads/main@{#106286} 
     
    (cherry picked from commit c642c7279120c75952c90e8ba24268be347eacc3) 
     
    Bug: 500604788,496776572,497065732,499606101 
    Change-Id: Ifb3e701940a90b49af8f328ff47f54dc9ca9727d 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7740983 
    Auto-Submit: Chrome Cherry Picker <chrome-cherry-picker@chops-service-accounts.iam.gserviceaccount.com> 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Cr-Commit-Position: refs/branch-heads/14.8@{#2} 
    Cr-Branched-From: f9659283a5f8d42b3c09228cf5df606fcaf47a3d-refs/heads/14.8.178@{#1} 
    Cr-Branched-From: 141232520dc4910401240c531db3af36910a0fd1-refs/heads/main@{#106240}

```

---

Files:

- M `src/compiler/backend/arm64/code-generator-arm64.cc`
- M `src/compiler/backend/arm64/instruction-codes-arm64.h`
- M `src/compiler/backend/arm64/instruction-selector-arm64.cc`
- M `test/mjsunit/wasm/load-shift32.js`
- M `test/unittests/compiler/arm64/turboshaft-instruction-selector-arm64-unittest.cc`

---

Hash: [2e1eaba99c579e0aa9b01db8c89cf1ef38ab493e](https://chromiumdash.appspot.com/commit/2e1eaba99c579e0aa9b01db8c89cf1ef38ab493e)  

Date: Tue Apr 7 13:17:15 2026


---

### pe...@google.com (2026-04-09)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### pe...@google.com (2026-04-09)

The NextAction date has arrived: 2026-04-09
To opt-out from this automation rule, please add Optout-Blintz-Nextaction-Alert to the "Chromium Labels" custom field.

### sp...@google.com (2026-04-22)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $11000.00 for this report.

Rationale for this decision:
Baseline with bisect. Renderer RCE / memory corruption in a sandboxed process


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### qk...@google.com (2026-05-20)

Labeled LTS-NotApplicable-144 because M144 doesnt's have the suspected CL.

### ch...@google.com (2026-07-15)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### cl...@google.com (2026-07-16)

Removing myself from issues where I was bulk CC-ed for no reason. Please add me back if my input is required.

---

*Comment created using gemini\_cli*

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/499606101)*
