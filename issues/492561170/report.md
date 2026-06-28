# V8 Sandbox Bypass: Atomics TypedArray TOCTOU (Map/Length Mismatch)

| Field | Value |
|-------|-------|
| **Issue ID** | [492561170](https://issues.chromium.org/issues/492561170) |
| **Status** | Verified |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Blink>JavaScript |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ki...@gmail.com |
| **Assignee** | ma...@chromium.org |
| **Created** | 2026-03-14 |
| **Bounty** | $5,000.00 |

## Description

# Steps to reproduce the problem

1. Build d8 for desktop (x86-64):

```
cat > out/args.gn << 'EOF'
v8_enable_sandbox = true
v8_enable_memory_corruption_api = true
is_debug = false
target_cpu = "x64"
EOF
autoninja -C out d8

```

2. Run the attached poc.js on desktop:

```
./out/d8 --sandbox-testing poc.js

```

On desktop this produces "Caught harmless memory access violation" because the 260 GB guard contains the 48 GB OOB write. The bug fires but the write is contained by the desktop guard.

3. Build d8 for Android ARM64:

```
cat > out/android_arm64/args.gn << 'EOF'
target_os = "android"
target_cpu = "arm64"
v8_enable_sandbox = true
v8_enable_memory_corruption_api = true
is_debug = false
is_component_build = false
v8_static_library = true
EOF
autoninja -C out/android_arm64 d8

```

4. Push to an Android ARM64 device and run:

```
./d8 --sandbox-testing poc.js

```

On Android this produces "V8 sandbox violation detected!" because the 36 GB trailing guard is exceeded by the 48 GB OOB write.
5. Tested on OnePlus 11 (CPH2449), Android 14. Relevant logcat output:

```
13:32:56.814 d8> Sandbox bounds: [0x2f00000000,0x4f00000000)
13:32:56.837 libc: Fatal signal 11 (SIGSEGV), code 1 (SEGV_MAPERR), fault addr 0x5a2d05dfff
13:32:56.838 d8> ## V8 sandbox violation detected!
13:32:56.877 DEBUG: signal 11 (SIGSEGV), code 1 (SEGV_MAPERR), fault addr 0x0000005a2d05dfff
13:32:56.890 d8 exit code: 139

```

Fault address 0x5a2d05dfff is 44.7 GB past sandbox end 0x4f00000000, exceeding the 36 GB Android guard. The full logcat is attached.

# Problem Description

EmitElementStoreTypedArray in src/codegen/code-stub-assembler.cc has a TOCTOU between two reads of elements\_kind from the receiver's map. PrepareValueForWriteToTypedArray calls ToBigInt which invokes valueOf() between the two reads. The valueOf callback runs synchronously (no race condition needed) and can corrupt the receiver's map via the sandbox memory corruption API.

The attacker flips the map from BigUint64Array to Uint8Array between LOAD 1 (dispatch) and LOAD 2 (length computation). LOAD 1 dispatches to the BigUint64 handler (8 bytes per element). LOAD 2 re-reads the map, sees Uint8, and computes length as byte\_length >> 0 instead of >> 3, inflating it from 0 to ~34 billion. The bounds check passes for any index up to 34 billion. The store then writes 8 bytes at data\_ptr + index \* 8, reaching up to ~253 GB past the sandbox end.

On Android, the trailing sandbox guard is only 36 GB (kAdditionalTrailingGuardRegionSize = 0 in sandbox.cc:213). The OOB write exceeds this, escaping the sandbox. On desktop, a 260 GB workaround guard ([crbug.com/40070746](https://crbug.com/40070746)) contains the write, but the code bug is still present and unfixed.

This is a different code path from [bug 488927521](https://issues.chromium.org/issues/488927521) (Atomics TOCTOU). The fix for that bug (CL 149c19dcbdb) added an optional elements\_kind parameter to LoadJSTypedArrayLengthAndValidate, but the IC store callers in EmitElementStoreTypedArray were not updated. Unfixed on all branches as of V8 14.7.

The IC store path is strictly more powerful than the Atomics path: it is fully deterministic (synchronous valueOf, no SharedArrayBuffer race), supports 64-bit indices via TryToIntptr/TruncateFloat64ToInt64, and gives value control (the BigInt return from valueOf becomes the written value).

The affected code path:

```
EmitElementStoreTypedArray:
  elements_kind = LoadElementsKind(receiver)              <- LOAD 1
  PrepareValueForWriteToTypedArray(value, elements_kind)
    -> ToBigInt -> valueOf() -> JS runs -> attacker flips map
  length = LoadJSTypedArrayLengthAndValidate(typed_array)
    -> LoadElementsKind(typed_array)                      <- LOAD 2
    -> Uint8 shift=0 -> length = byte_length (~34 billion)
  StoreElement(data_ptr, elements_kind, key, value)
    -> Uses LOAD 1's BigUint64 element size with LOAD 2's inflated length

```

Entry point: Generate\_StoreFastElementIC (builtins-handler-gen.cc:284).

Primitive properties:

- Write size: 8 bytes
- Address: data\_ptr + index \* 8, index up to 2^53
- Max OOB reach: ~253 GB past sandbox end
- Reliability: 100% deterministic

Android vs Desktop:

- Android: 36 GB trailing guard, 253 GB OOB -> escapes sandbox
- Desktop: 260 GB trailing guard, 253 GB OOB -> contained

Proposed fix: thread elements\_kind from LOAD 1 through to the length computation so LOAD 2 is eliminated. Also fix LoadJSTypedArrayLength (line 17942) and the IC load path in accessor-assembler.cc:2903.

Attachments:

- poc.js: standalone PoC (no dependencies beyond --sandbox-testing)
- logcat.txt: full device logcat from OnePlus 11 run
- logcat\_relevant.txt

# Summary

IC Store ElementsKind TOCTOU: OOB Write Outside V8 Sandbox

# Custom Questions

#### Type of crash:

Tab crash (renderer process). The V8 sandbox runs inside the renderer. The OOB write escapes the sandbox but stays within the renderer process address space.

#### Crash state:

signal 11 (SIGSEGV), code 1 (SEGV\_MAPERR), fault addr 0x0000005a2d05dfff

```
  x0  0000002f0104d46d  x1  0000002f0104d331  x2  0000000000000000  x3  0000004effffffff
  x4  0000000165a0bc00  x5  0000000000000000  x6  0000004effffffff  x7  0000000000000000
  x8  0000007000213538  x9  ffffffffffff0ac8  x10 0000000000000000  x11 0000000000000001
  x12 0000000000000004  x13 0000000000000000  x14 0000002f0101ac61  x15 0000000000000153
  x16 0000000000000002  x17 00000060f7f1d4a0  x18 00000076a3a28000  x19 0000000000000029
  x20 0000000a0100027d  x21 00000070002c0010  x22 0000000000000001  x23 000000000000b
  x24 000000000000002d  x25 0000002f00000011  x26 0000007000204100  x27 0000002f0102bd59
  x28 0000002f00000000  x29 0000007fdc75b530
  lr  00000060f79bde9c  sp  0000007fdc75b4e0  pc  00000060f79bdf44  pst 0000000080001000

```

backtrace:
#00 pc 0000000002a61f44 libd8.so (BuildId: 839303c7b04a8396)

Sandbox bounds: [0x2f00000000, 0x4f00000000)
Fault addr 0x5a2d05dfff = sandbox\_end + 44.7 GB (exceeds 36 GB Android guard)

Device: OnePlus 11 (CPH2449), Android 14, ARM64. Binary is stripped (no symbols) — #00 pc 0x2a61f44 is inside the V8 sandbox violation signal handler in libd8.so.

#### Reporter credit:

Peter Malone

# Additional Data

Category: Security   

Chrome Channel: Stable   

Regression: N/A \

## Attachments

- [logcat_relevant.txt](attachments/logcat_relevant.txt) (text/plain, 1.2 KB)
- [logcat.txt](attachments/logcat.txt) (text/plain, 8.1 MB)
- [poc.js](attachments/poc.js) (text/javascript, 1.4 KB)

## Timeline

### cl...@appspot.gserviceaccount.com (2026-03-16)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5093768130756608.

### dr...@chromium.org (2026-03-16)

Does not reproduce on Clusterfuzz, but that's to be expected if the report is accurate. Triaging to V8 folks.

### ch...@google.com (2026-03-17)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-03-17)

Setting Priority to P1 to match Severity s1. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### ar...@google.com (2026-03-17)

I was able to reproduce it on a Pixel 9 Pro, Marja since you worked on the related bug CYPTAL?

### ma...@chromium.org (2026-03-18)

Thanks for the bug report!

I can't repro this but just based on reading the code, I believe this is a legit bug. I'm wondering how the previous repros, which were variants of the ElementsKind switcheroo, managed to also repro reliably on x64. They seem pretty similar to this one, I'm not sure what's the significant difference there. (Except they were using a Worker to modify the memory on a BG thread, and also iterated N times to win the race - but somehow they managed to not trip on the "harmless memory access violation".)

### dx...@google.com (2026-03-18)

Project: v8/v8  

Branch:  main  

Author:  Marja Hölttä [marja@chromium.org](mailto:marja@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7678850>

[sandbox] Fix another ElementsKind switcheroo bug

---


Expand for full commit details
```
     
    Because of previous fixes, LoadJSTypedArrayLengthAndValidate can 
    already take an ElementsKind. Now we just need to make sure that 
    we pass it, in case we have an ElementsKind we're going to use for 
    figuring out a location where we'll write into. 
     
    Fixed: 492561170 
    Change-Id: Ifa376efb3a21bcca06f13ac80582b34ab800c01e 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7678850 
    Commit-Queue: Marja Hölttä <marja@chromium.org> 
    Reviewed-by: Leszek Swirski <leszeks@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#105878}

```

---

Files:

- M `src/builtins/builtins-typed-array-gen.cc`
- M `src/codegen/code-stub-assembler.cc`

---

Hash: [fb58169194571777782af0ff9256968bc2fc795b](https://chromiumdash.appspot.com/commit/fb58169194571777782af0ff9256968bc2fc795b)  

Date: Wed Mar 18 09:41:59 2026


---

### pe...@gmail.com (2026-05-30)

Just checking in here. Need anything from my end?

### ar...@google.com (2026-06-01)

No the bug should be fixed already, if you are inquiring about the VRP we are not responsible for handling that. You can email them directly at [security-vrp@chromium.org](mailto:security-vrp@chromium.org) or [security@chromium.org](mailto:security@chromium.org), although I assume they will get to this issue as well.

### sp...@google.com (2026-06-15)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $5000.00 for this report.

Rationale for this decision:
Baseline. v8 Sandbox.


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-06-25)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/492561170)*
