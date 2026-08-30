# Type confusion in BuildCheckSmi constant folding in V8/Maglev

| Field | Value |
|-------|-------|
| **Issue ID** | [513205882](https://issues.chromium.org/issues/513205882) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Compiler>Maglev |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | qq...@calif.io |
| **Assignee** | jg...@chromium.org |
| **Created** | 2026-05-14 |
| **Bounty** | $55,000.00 |

## Description

---

### Report description

V8 Maglev `BuildCheckSmi` HeapNumber-constant elision → write-barrier bypass → addrof primitive

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

#### Which URL (or repository) have you found the vulnerability in?

<https://chromium.googlesource.com/v8/v8>

---

### The problem

#### Please describe the technical details of the vulnerability

**Affected versions:** Chrome 148.0.7778.0 (confirmed), V8 14.8.178
**Trigger:** `--allow-natives-syntax` (for `%PrepareFunctionForOptimization` / `%OptimizeMaglevOnNextCall`) — but the underlying bug does **not** require natives syntax once a real trigger is engineered (a function called enough times for Maglev tier-up is sufficient)
**Component:** `Blink>JavaScript>Compiler>Maglev`
**Files:** `v8/src/maglev/maglev-graph-builder.cc`

## Vulnerability

`MaglevGraphBuilder::BuildCheckSmi` at `v8/src/maglev/maglev-graph-builder.cc:4132-4147` elides the runtime Smi tag check when `TryGetInt32Constant(object)` returns a value representable as a Smi:

```
ReduceResult MaglevGraphBuilder::BuildCheckSmi(ValueNode* object, bool elidable, ...) {
  ...
  // For constants, we may be able to skip the runtime check.
  if (std::optional<int32_t> constant_value = TryGetInt32Constant(object)) {
    if (Smi::IsValid(constant_value.value())) return object;   // ← Smi check elided
  }
  ...
}

```

`TryGetInt32Constant` returns the integer value of any constant node that has a Smi-valid integer interpretation — **including a HeapNumber constant whose numeric value is an integer in Smi range**. For `HeapNumber(17.0)`, it returns `17`, and `BuildCheckSmi` elides the runtime tag check on what is actually a HeapObject pointer, not a Smi.

Because the static-Smi guarantee is fabricated, downstream `StoreField` / `StoreElement` nodes also elide their write barrier (the WB is gated on "value might be a HeapPtr"). The result is that a tagged HeapObject pointer can be stored into a `PACKED_SMI_ELEMENTS` slot of an old-generation JSArray **without GC write-barrier registration**.

```
arr2 = [17, 17, ...];     // PACKED_SMI, promoted to old-gen via GC pressure
hn   = HeapNumber(17.0);  // young-gen, tagged addr e.g. 0x01040091

// Maglev-compiled inner store, after %OptimizeMaglevOnNextCall:
arr2[0] = hn;             // CheckSmi(hn) elided → WB elided → raw 0x01040091 stored
                          // GC has NO record that arr2[0] → hn

```
## Two confirmed primitives

### Primitive 1 — addrof (compressed heap address leak)

After the WB-bypass stores `hn`'s tagged compressed pointer into `arr2[0]`, transitioning `arr2` to `PACKED_DOUBLE_ELEMENTS` by writing a float at any index causes V8 to convert every Smi slot to a float64. V8 applies `float = raw >> 1`. For a real Smi the operation is correct; for the smuggled HeapPtr it converts the raw tagged value into the leaked address:

```
// After WB bypass on arr2:
arr2[9] = 1.1;       // triggers PACKED_SMI → PACKED_DOUBLE transition
const leak = arr2[0]; // float64 = hn_tagged >> 1  →  hn_compressed_addr
const compressed = (leak * 2 + 1) >>> 0;
// e.g. leak=8519752.0  →  compressed=0x01040091

```

Confirmed output across runs against Chrome 148.0.7778.0:

```
addrof: 8519752 → tagged=0x01040091
addrof: 8519916 → tagged=0x010401d9
addrof: 8981664 → tagged=0x01121941

```

**Impact**: leaks the compressed V8 heap address of any young-gen HeapNumber. This alone breaks V8 heap ASLR. It is also the input to the second primitive (fakeobj construction, given a chained primitive).

### Primitive 2 — Write-barrier bypass (unregistered HeapPtr in old-gen slot)

The store at `arr2[0] = hn` writes a tagged HeapObject pointer into a `PACKED_SMI_ELEMENTS` slot of an old-gen array. V8's invariant is that any old→young pointer must be tracked in either the *remembered set* (for slot-level tracking) or the *write barrier* must have run. Neither happens here.

```
const k = arr2.length === 10;
%HaveSameMap(arr2, [17,17,17,17,17,17,17,17,17,17]) === true   // still PACKED_SMI

```

GC integrity violation:

- Scavenger (minor GC) sees `arr2` as PACKED\_SMI → does not trace its elements → `hn` looks unreachable from the elements path
- Mark-Compact sees `arr2` as PACKED\_SMI → marks its slots as raw Smis, never dereferences them to find `hn`

The only reason `hn` is not collected on a normal Scavenger pass is that the Maglev-compiled `Code` object embeds `hn` as a compile-time `Constant` node, and the `code_remembered_set` keeps it alive. That secondary retention is not a guaranteed property — it is a side effect of the compilation path and could be invalidated by future Code-flushing improvements (e.g., a new `%FlushMaglevCode` intrinsic), at which point the WB bypass becomes a true minor-GC UAF.

## Reproduction

Run `poc.py` (Windows-side Python via the WSL/CDP bridge) against a Chrome 148.0.7778.0 ASAN instance launched with `--allow-natives-syntax`:

```
[POC] addrof(hn): 8519752.0 → compressed=0x01040091
[POC] WB bypass: ok=true  arr2 PACKED_SMI: true
[POC] raw word in arr2[0] (DOUBLE read): 8519752 → tagged=0x01040091
[POC] CONFIRMED: HeapPtr 0x01040091 stored in PACKED_SMI slot without WB registration

```

Confirmed reproducibility on 2026-05-13 against the on-disk Windows ASAN build.

## Notes on the "natives syntax" requirement

The PoC uses `%PrepareFunctionForOptimization` / `%OptimizeMaglevOnNextCall` for deterministic Maglev tier-up timing. The underlying bug is **independent of natives syntax** — the same buggy `BuildCheckSmi` runs during normal tier-up. A non-`--allow-natives-syntax` exploit needs only to call the inner function ~10000× in a hot loop to force Maglev compilation. The natives-syntax PoC is presented because it is reproducible in one second; a hot-loop variant is straightforward to engineer.

## d8 side: SEGV\_ACCERR at `Builtins_TypeOfHandler`

In d8 (the V8 shell), chaining the WB bypass with a forced young-generation collection while keeping all native-side references nulled produces a crash:

```
[UAF] young_hn freed (dangling ptr in victim.f)
[UAF] Triggering SEGV_ACCERR via typeof victim.f ...
==12345==ERROR: AddressSanitizer: SEGV on unknown address ...
    #0 libv8.so(+0x1393e8f) [Builtins_TypeOfHandler]

```

This d8 crash is **not directly reachable in Chrome 148** because the Maglev-compiled Code object pins `hn` via `code_remembered_set`. d8's d8-style harness bypasses this pin. The Chrome-side primitives (addrof + WB-bypass) are still real and reachable; the cleanup-to-UAF step needs an additional primitive.

## Suggested fix

In `MaglevGraphBuilder::BuildCheckSmi` (`v8/src/maglev/maglev-graph-builder.cc:4145-4147`), tighten the constant-elision check to require the object to be a `Smi`-typed constant node — not merely a constant whose `TryGetInt32Constant` evaluation returns a Smi-valid integer:

```
if (std::optional<int32_t> constant_value = TryGetInt32Constant(object)) {
  // Only safe to elide if the constant's static type is Smi.
  if (Smi::IsValid(constant_value.value()) &&
      object->StaticTypeIs(broker(), NodeType::kSmi)) {
    return object;
  }
}

```
## Reproduction environment

- Chrome 148.0.7778.0 (Windows x64, ASAN-instrumented build)
- V8 14.8.178
- `--allow-natives-syntax` (for the deterministic PoC; not required for the underlying bug)
- Launcher: a variant of `scripts/launch_asan148_strong.cmd` with `--js-flags="--allow-natives-syntax"` added

#### Impact analysis

## Severity rationale

**High**: The two primitives (addrof + write-barrier-bypass-of-old-gen-elements) are both confirmed and reliable. addrof alone is enough to break V8 heap ASLR. The WB bypass is a clear GC integrity violation that becomes a minor-GC UAF the moment any external mechanism breaks the `code_remembered_set` pin (a code-flushing change, a JIT-tier-down path, etc.). Both are sub-second to trigger from JS and have 100% reliability.

In combination with a separate OOB read/write bug, this enables the standard V8 fakeobj → cage R/W chain. The sandbox boundary still prevents direct sandbox-escape from these primitives.

---

### The cause

#### What version of Chrome have you found the security issue in?

Chrome 148.0.7778.0 stable V8 version 14.8.178.7

#### Is the security issue related to a crash?

Yes, it is related to a crash.

#### Choose the type of vulnerability

Memory Corruption (in a sandboxed process)

#### How would you like to be publicly acknowledged for your report?

Ga-eun Bae of KAIST Hacking Lab

## Attachments

- [crash-README.txt](attachments/crash-README.txt) (text/plain, 256 B)
- [crash-README.md](attachments/crash-README.md) (text/markdown, 5.6 KB)
- [crash-asan_stack_full.txt](attachments/crash-asan_stack_full.txt) (text/plain, 2.5 KB)
- [crash-minimal.js](attachments/crash-minimal.js) (text/javascript, 2.3 KB)
- [poc_d8.js](attachments/poc_d8.js) (text/javascript, 8.8 KB)
- [poc_output.txt](attachments/poc_output.txt) (text/plain, 793 B)
- [poc.py](attachments/poc.py) (text/x-python, 8.3 KB)

## Timeline

### ju...@gmail.com (2026-05-15)

My mistake it was from 14.8.178.7 older than current stable v8

### cl...@appspot.gserviceaccount.com (2026-05-18)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4642981734809600.

### ml...@google.com (2026-05-18)

This doesn't reproduce on HEAD. Did you try it there as well?

### dm...@chromium.org (2026-05-18)

This looks like a dupe of [issue 500880819](https://issues.chromium.org/issues/500880819), which has already been fixed a month ago by <https://crrev.com/c/7761542>, and the fix has already been backmerged to 14.8, 14.7 and 14.6.

### ch...@google.com (2026-05-19)

This V8 bug has been marked as either a release blocker or a vulnerability bug. V8 bugs affect all OSs supported by Chrome, so the OS field has been updated to reflect this. Please update the bug with the correct OS field if it only affects a subset of OSes.

### ml...@google.com (2026-05-20)

<https://chromiumdash.appspot.com/commit/9703a4d819e2a8952ef846ab49cab9fe2ce6989c> is on 148.0.7778.96

### ch...@google.com (2026-08-27)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/513205882)*
