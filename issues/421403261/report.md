# V8 Sandbox Bypass: AAW via clobbered i32 high word on return value in Liftoff

| Field | Value |
|-------|-------|
| **Issue ID** | [421403261](https://issues.chromium.org/issues/421403261) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Blink>JavaScript>WebAssembly |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | se...@gmail.com |
| **Assignee** | cl...@chromium.org |
| **Created** | 2025-05-31 |
| **Bounty** | $20,000.00 |

## Description

### VULNERABILITY DETAILS

#### Summary

V8 sandbox bypass, arbitrary address read/write due to Liftoff emitting WasmArray indexing code using full 64bit registers in x86-64.

#### Details

Liftoff holds an invariant that all registers storing an i32 value is valid, i.e. that the upper 32bits are zeroed out properly in x86-64. Thus, WasmArray bound checks uses the 32bit wide comparison in `BoundsCheckArray()`:

```
// https://source.chromium.org/chromium/chromium/src/+/main:v8/src/wasm/baseline/liftoff-compiler.cc;drc=0dc30698370bcde67dda4f48b7ca19bf4c1dbc17;l=9781
  void BoundsCheckArray(FullDecoder* decoder, bool implicit_null_check,
                        LiftoffRegister array, LiftoffRegister index,
                        LiftoffRegList pinned) {
    // ...
    __ emit_cond_jump(kUnsignedGreaterThanEqual, trap.label(), kI32, index.gp(),  // [!] 32bit comparison
                      length.gp(), trap.frozen());
  }

```

...but uses the full 64bit register when actually using it to index into the array. Below is an example in `array.set`:

```
// https://source.chromium.org/chromium/chromium/src/+/main:v8/src/wasm/baseline/liftoff-compiler.cc;drc=27dd841b0c86ab73f4318764bda78bdc467e5a47;l=7316
  void ArraySet(FullDecoder* decoder, const Value& array_obj,
                const ArrayIndexImmediate& imm, const Value& index_val,
                const Value& value_val) {
    // ...
    BoundsCheckArray(decoder, implicit_null_check, array, index, pinned);
    ValueKind elem_kind = imm.array_type->element_type().kind();
    int elem_size_shift = value_kind_size_log2(elem_kind);
    if (elem_size_shift != 0) {
      __ emit_i32_shli(index.gp(), index.gp(), elem_size_shift);                  // [!] avoid this using i8 array
    }
    StoreObjectField(decoder, array.gp(), index.gp(),
                     wasm::ObjectAccess::ToTagged(WasmArray::kHeaderSize),
                     value, false, pinned, elem_kind);
  }

// https://source.chromium.org/chromium/chromium/src/+/main:v8/src/wasm/baseline/liftoff-compiler.cc;drc=0dc30698370bcde67dda4f48b7ca19bf4c1dbc17;l=9854
  void StoreObjectField(FullDecoder* decoder, Register obj, Register offset_reg,
                        int offset, LiftoffRegister value, bool trapping,
                        LiftoffRegList pinned, ValueKind kind,
                        LiftoffAssembler::SkipWriteBarrier skip_write_barrier =
                            LiftoffAssembler::kNoSkipWriteBarrier) {
    uint32_t protected_load_pc = 0;
    if (is_reference(kind)) {
      // ...
    } else {
      // Primitive kind.
      StoreType store_type = StoreType::ForValueKind(kind);
      __ Store(obj, offset_reg, offset, value, store_type, pinned,
               trapping ? &protected_load_pc : nullptr);
    }
    // ...
  }

// https://source.chromium.org/chromium/chromium/src/+/main:v8/src/wasm/baseline/x64/liftoff-assembler-x64-inl.h;l=643;drc=0dc30698370bcde67dda4f48b7ca19bf4c1dbc17;bpv=1;bpt=1
void LiftoffAssembler::Store(Register dst_addr, Register offset_reg,
                             uintptr_t offset_imm, LiftoffRegister src,
                             StoreType type, LiftoffRegList /* pinned */,
                             uint32_t* protected_store_pc,
                             bool /* is_store_mem */, bool i64_offset) {
  if (offset_reg != no_reg && !i64_offset) AssertZeroExtended(offset_reg);
  Operand dst_op = liftoff::GetMemOp(this, dst_addr, offset_reg, offset_imm);     // [!] 64bit offset register
  // ...store to dst_op
}

// https://source.chromium.org/chromium/chromium/src/+/main:v8/src/codegen/x64/macro-assembler-x64.h;drc=0dc30698370bcde67dda4f48b7ca19bf4c1dbc17;l=592
  // Abort execution if a 64 bit register containing a 32 bit payload does not
  // have zeros in the top 32 bits, enabled via --debug-code.
  void AssertZeroExtended(Register reg) NOOP_UNLESS_DEBUG_CODE;

```

We see that unless `--debug-code` is enabled `AssertZeroExtended()` is a no-op and thus the full 64bit register is used as index without truncation if `elem_size_shift == 0`, that is, we index an i8 array.

Under memory corruption, it is indeed possible to create a state where the upper 32bits of a register holding a i32-typed value is clobbered to an attacker-controlled value. One way is to exploit Wasm signature confusion within the same [signature hash](https://source.chromium.org/chromium/chromium/src/+/main:v8/src/wasm/signature-hashing.h) equivalence class, e.g. call a `i64->i64` function with its type confused into a `i64->i32` and use the return value as a clobbered i32 value. This does not violate WasmCPT signature checks introduced against [b/350292240](https://issues.chromium.org/issues/350292240), but is still sufficient to violate the i32 invariant and bypass the sandbox.

Attached repro demonstrates this to achieve arbitrary address read/write. Liftoff-generated code for `array.set` on an i8 array is shown as below. After calling an indirect function, the first return value stored inside `rax` is used to index into the given i8 array - array bounds check are done with the lower 32bit register `eax`, but the actual indexing is done with the full 64bit register `rax`.

```
 ► 0x7ffff7700ad1    call   qword ptr [rcx]
 
   0x7ffff7700ad3    mov    ecx, dword ptr [rbp - 0x34]
   0x7ffff7700ad6    mov    rdx, qword ptr [rbp - 0x40]
   0x7ffff7700ada    mov    ebx, dword ptr [rdx + 7]
   0x7ffff7700add    cmp    eax, ebx
   0x7ffff7700adf    jae    0x7ffff7700b22              <0x7ffff7700b22>
 
   0x7ffff7700ae5    mov    byte ptr [rdx + rax + 0xb], cl     <Cannot dereference [0x424242424242]>

```
### VERSION

V8: Tested on latest CF asan / no-asan sandbox-testing d8 build @ revision 100600 (commit [56f541d](https://crrev.com/c/6604643))

### REPRODUCTION CASE

Attached as `liftoff-wasmarray-i64-indexing.js`, run `d8` with `--sandbox-testing`.

The repro attempts to write a single byte `0x43` to address `0x424242424242`.

### FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION

Type of crash: Sandbox violation

### CREDIT INFORMATION

Reporter credit: Seunghyun Lee (@0x10n)

## Attachments

- [liftoff-wasmarray-i64-indexing.js](attachments/liftoff-wasmarray-i64-indexing.js) (text/javascript, 75.3 KB)

## Timeline

### th...@chromium.org (2025-06-02)

[security shepherd]
Triaging as v8 sandbox bypass bug: provisional severity of S2, provisional priority of P1, assigning to current V8 shepherd, setting Security_Impact-None and V8 Sandbox hotlists.

### cl...@chromium.org (2025-06-02)

We fixed this for parameters by explicitly zero-extending them on function entry in Liftoff: https://crrev.com/c/5494364

I guess we need the same after function calls for return values...

### is...@chromium.org (2025-06-02)

Thank you for the report!

Assigning to Wasm folks for further triaging.

### cl...@appspot.gserviceaccount.com (2025-06-02)

Detailed Report: https://clusterfuzz.com/testcase?key=5414746165542912

Fuzzer: None
Job Type: linux_asan_d8_sandbox_testing
Platform Id: linux

Crash Type: V8 sandbox violation
Crash Address: 0x424242424242
Crash State:
  Builtins_JSToWasmWrapperAsm
  Builtins_JSToWasmWrapper
  Builtins_InterpreterEntryTrampoline
  
Sanitizer: address (ASAN)

Crash Revision: https://clusterfuzz.com/revisions?job=linux_asan_d8_sandbox_testing&revision=100621

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5414746165542912

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### cl...@chromium.org (2025-06-02)

After talking to Jakob, I'll take this one.

Samuel, is `Security-Impact-None` still the right categorization of sandbox escapes? And P1/S2?

### sa...@google.com (2025-06-02)

Yes that's all correct! Thanks!

### cl...@chromium.org (2025-06-02)

Stupid bot.
Any idea how to stop it from re-adding the `Untriaged` label?

### th...@chromium.org (2025-06-02)

It may have been from the missing OS labels (though I am not sure).

### cl...@chromium.org (2025-06-02)

Anyway, I'll better spend my time on fixing this then preventing bots from messing with labels.

### se...@gmail.com (2025-06-02)

FYI: Should be obvious, but works with plain old memory load/stores too - choice of `array.set` was just carried on from other code. Title should rather be "AAW via Liftoff i32 high word clobbered returns" (similar to <https://crrev.com/c/5494364>) or something in the lines of that.

### cl...@chromium.org (2025-06-02)

Fix is in review: https://crrev.com/c/6611066

### dx...@google.com (2025-06-02)

Project: v8/v8  

Branch: main  

Author: Clemens Backes [clemensb@chromium.org](mailto:clemensb@chromium.org)  

Link:      <https://chromium-review.googlesource.com/6611066>

[liftoff] Ensure zero-extension of returned i32 values

---


Expand for full commit details
```
     
    The signature hash allows for i64/i32 collisions. To compensate for that 
    we already did zero-extend all parameters in the Liftoff prologue. 
    This does the same for returned values, which have the same problem. 
     
    R=jkummerow@chromium.org 
     
    Bug: 421403261 
    Change-Id: Iff76f6f8bdcb78fe399bdd81c9194794cb6e0d5c 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6611066 
    Commit-Queue: Jakob Kummerow <jkummerow@chromium.org> 
    Auto-Submit: Clemens Backes <clemensb@chromium.org> 
    Reviewed-by: Jakob Kummerow <jkummerow@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#100630}

```

---

Files:

- M `src/wasm/baseline/liftoff-assembler.cc`
- M `src/wasm/baseline/liftoff-compiler.cc`
- A `test/mjsunit/sandbox/liftoff-wasmarray-i64-indexing.js`

---

Hash: df3874776c396ba7ddc6ca7894a1e09937bc3d04  

Date:  Mon Jun 2 15:42:22 2025


---

### 24...@project.gserviceaccount.com (2025-06-03)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the hotlistid:4801165.

### 24...@project.gserviceaccount.com (2025-06-03)

ClusterFuzz testcase 5414746165542912 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8_sandbox_testing&range=100629:100630

If this is incorrect, please add the hotlistid:5433040 and re-open the issue.

### sa...@google.com (2025-06-03)

Fantastic work with the quick fix! It looks like this fix should be backmergeable, and I think that would make sense here (we want to start backmerging sandboxes fixes where possible). If you're ok with that, I can request merge approvals once the fix has gotten some canary coverage.

### cl...@chromium.org (2025-06-03)

Yes, the fix is super simple and could/should be backmerged.

### cl...@chromium.org (2025-06-03)

The fix is released in Canary 139.0.7217.0.

### am...@chromium.org (2025-06-03)

I talked to Samuel about starting to consider backmerges for some of the v8 sb bypasses, so I've updated this particular one with the merge review labels so it is in the queue.
I feel like we can merge this to current Stable but backmerging to M136 Extended would is probably taking it too far back, so I've added tags for review for M138 Beta and M137 Stable.

### sp...@google.com (2025-06-04)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $20000.00 for this report.

Rationale for this decision:
report of V8 sandbox bypass demonstrating controlled write outside the V8 heap sandbox


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-06-04)

Congratulations! Thank you for continuing to hunt against the V8 sandbox!

### am...@chromium.org (2025-06-06)

merges for <https://crrev.com/c/6611066> approved for M138 Beta and M138 Stable; please merge to 13.8 and 13.7 at your earliest convenience; there is not rush needed here however and can wait until after Monday's MUC holiday

### dx...@google.com (2025-06-10)

Project: v8/v8  

Branch: refs/branch-heads/13.8  

Author: Clemens Backes [clemensb@chromium.org](mailto:clemensb@chromium.org)  

Link:      <https://chromium-review.googlesource.com/6632488>

Merged: [liftoff] Ensure zero-extension of returned i32 values

---


Expand for full commit details
```
     
    The signature hash allows for i64/i32 collisions. To compensate for that 
    we already did zero-extend all parameters in the Liftoff prologue. 
    This does the same for returned values, which have the same problem. 
     
    R=jkummerow@chromium.org 
     
    Bug: 421403261 
    (cherry picked from commit df3874776c396ba7ddc6ca7894a1e09937bc3d04) 
     
    Change-Id: Ic0463a7f107331a86ca67fca75e75d4a9f8a8ce2 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6632488 
    Auto-Submit: Clemens Backes <clemensb@chromium.org> 
    Reviewed-by: Jakob Kummerow <jkummerow@chromium.org> 
    Commit-Queue: Jakob Kummerow <jkummerow@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/13.8@{#24} 
    Cr-Branched-From: 61ddd471ece346840bbebbb308dceb4b4ce31b28-refs/heads/13.8.258@{#1} 
    Cr-Branched-From: fdb5de2c741658e94944f2ec1218530e98601c23-refs/heads/main@{#100480}

```

---

Files:

- M `src/wasm/baseline/liftoff-assembler.cc`
- M `src/wasm/baseline/liftoff-compiler.cc`
- A `test/mjsunit/sandbox/liftoff-wasmarray-i64-indexing.js`

---

Hash: ee425ad53cdb15d4b462d0ac24206f09c188842a  

Date:  Mon Jun 2 15:42:22 2025


---

### dx...@google.com (2025-06-10)

Project: v8/v8  

Branch: refs/branch-heads/13.7  

Author: Clemens Backes [clemensb@chromium.org](mailto:clemensb@chromium.org)  

Link:      <https://chromium-review.googlesource.com/6632487>

Merged: [liftoff] Ensure zero-extension of returned i32 values

---


Expand for full commit details
```
     
    The signature hash allows for i64/i32 collisions. To compensate for that 
    we already did zero-extend all parameters in the Liftoff prologue. 
    This does the same for returned values, which have the same problem. 
     
    R=jkummerow@chromium.org 
     
    Bug: 421403261 
    (cherry picked from commit df3874776c396ba7ddc6ca7894a1e09937bc3d04) 
     
    Change-Id: Idd8573fddc9c9e1f57455b4e5ec6bfe3424e11b2 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6632487 
    Commit-Queue: Jakob Kummerow <jkummerow@chromium.org> 
    Auto-Submit: Clemens Backes <clemensb@chromium.org> 
    Reviewed-by: Jakob Kummerow <jkummerow@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/13.7@{#28} 
    Cr-Branched-From: dd5370d3d251320f6a5bed609ff8e1b71c767d97-refs/heads/13.7.152@{#1} 
    Cr-Branched-From: fa9b75303b0b5d2940a67096dca3babd14aa1fd2-refs/heads/main@{#99927}

```

---

Files:

- M `src/wasm/baseline/liftoff-assembler.cc`
- M `src/wasm/baseline/liftoff-compiler.cc`
- A `test/mjsunit/sandbox/liftoff-wasmarray-i64-indexing.js`

---

Hash: 3efc4f0f8135c612b5b8d5ae708f716951bde5cc  

Date:  Mon Jun 2 15:42:22 2025


---

### ch...@google.com (2025-06-10)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-06-10)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-09-10)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/421403261)*
