# V8 Sandbox Bypass:TypedArray.prototype.set ElementsKind TOCTOU

| Field | Value |
|-------|-------|
| **Issue ID** | [499717570](https://issues.chromium.org/issues/499717570) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>JavaScript |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Chrome Version** | V8 version 14.9.0 (candidate) |
| **Reporter** | gr...@gmail.com |
| **Assignee** | ar...@google.com |
| **Created** | 2026-04-05 |
| **Bounty** | $5,000.00 |

## Description

# Steps to reproduce the problem

1. Build d8 for android (arm64)

```
//The test commit is 56e2ad9bc14b082cf40252f99d1217bd477a0398 (Fri Apr 3 00:19:11 2026)
target_os = "android"
target_cpu = "arm64"
v8_enable_sandbox = true
v8_enable_memory_corruption_api = true
is_debug = false
is_component_build = false
v8_static_library = true
symbol_level = 1

```

2. Push to an Android ARM64 device and run: ./d8 --sandbox-testing ./poc.js
3. You will then see a crash

# Problem Description

## Summary

`TypedArray.prototype.set(arrayLike, offset)` has a TOCTOU between Torque's offset validation and C++ element copy dispatch. A Proxy source object provides deterministic JS callbacks to flip the target's Map between Uint8Array (large element count for bounds check) and Float64Array (8-byte element size for pointer arithmetic), achieving an OOB write of up to 256 GB past `DataPtr`. On Android (128 GB sandbox + 64 GB guard = 192 GB), this escapes the V8 sandbox.

## Root Cause

`TypedArrayPrototypeSetArray` in `typed-array-set.tq` reads the target's `elements_kind` multiple times from the heap, with JS-observable side effects between reads.

```
| Step | Code Location | What Happens |
|------|--------------|--------------|
| 1 | `EnsureValidAndReadLength` (tq:72) | READ 1: `elements_kind` → Uint8 → `targetLength ≈ 34.4B` |
| 2 | `GetLengthProperty(proxy)` (tq:122) | **JS callback** → attacker flips Map to Float64Array |
| 3 | `CheckIntegerIndexAdditionOverflow` (tq:131) | Uses **stale** `targetLength` from step 1 → offset 32B passes |
| 4 | `target.elements_kind` (tq:141) | READ 2: Float64 → not BigInt → continues |
| 5 | `Cast<FastJSArray>(proxy)` (tq:143) | Proxy fails cast → **IfSlow** |
| 6 | `Runtime_TypedArraySet` (tq:168) | `target->GetElementsAccessor()` → **Float64ElementsAccessor** |
| 7 | `GetProperty(proxy, 0)` (elements.cc:4394) | **JS callback** → attacker flips Map back to Uint8Array |
| 8 | `GetLengthOrOutOfBounds` (elements.cc) | Reads Uint8 → `length ≈ 34.4B` → `32B + 0 < 34.4B` → **passes** |
| 9 | `Float64ElementsAccessor::SetImpl` (elements.cc:3533) | `(double*)DataPtr + 32B = DataPtr + 256 GB` → **OOB write** |     

```
## BISECT

<https://chromium-review.googlesource.com/c/v8/v8/+/6968758>  

This is a bypass of the 435630461 fix: the SBXCHECK was added to `CopyElementsFromTypedArray` (TypedArray→TypedArray path), but `CopyElementsHandleSlow` (Proxy→TypedArray path) remains vulnerable. The `GetLengthOrOutOfBounds` check in the slow path is defeated by flipping the Map back to Uint8 before the check.

## FIX

A fix patch is provided in the attachment, which has been tested and confirmed to resolve the vulnerability on commit 56e2ad9bc14b082cf40252f99d1217bd477a0398.

# Summary

V8 Sandbox Bypass:TypedArray.prototype.set ElementsKind TOCTOU

# Custom Questions

#### Type of crash:

tab

#### Crash state:

Details can be found in the attached crash.txt file.

```
emu64a:/data/local/tmp/v8 # ./d8 --sandbox-testing ./poc.js                                                                                         
Sandbox testing mode is enabled. Only sandbox violations will be reported, all other crashes will be ignored.     
Sandbox bounds: [0x2e00000000,0x4e00000000)      

## V8 sandbox violation detected!     

Segmentation fault       

```
#### Reporter credit:

GraVity0

# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: N/A \

## Attachments

- [poc.js](attachments/poc.js) (text/javascript, 1.4 KB)
- [crash.txt](attachments/crash.txt) (text/plain, 3.0 KB)
- [fix.diff](attachments/fix.diff) (text/x-diff, 1.5 KB)
- [oob-controlled-addr.js](attachments/oob-controlled-addr.js) (text/javascript, 1.7 KB)
- [test.sh](attachments/test.sh) (text/x-sh, 3.1 KB)
- [shellcode.sh](attachments/shellcode.sh) (text/x-sh, 6.7 KB)
- [poc.js](attachments/poc_78827974.js) (text/javascript, 6.0 KB)

## Timeline

### gr...@gmail.com (2026-04-05)

A new PoC is provided, which allows selecting the write target outside the sandbox by controlling the offset through an argument.  

Write address = `DataPtr + offset * 8`. Both variables are attacker-controlled,Tested on Android emulator:

```
./d8 --sandbox-testing ./oob-controlled-addr.js -- 25000000000                                                                           
Sandbox testing mode is enabled. Only sandbox violations will be reported, all other crashes will be ignored.
Sandbox bounds: [0x2800000000,0x4800000000)
sandbox: 0x2800000000 - 0x4800000000
offset=25000000000  write=sandbox_base+0x2e90edd000 (186.3 GB)

## V8 sandbox violation detected!

Segmentation fault 


04-06 02:26:27.811  2934  2934 F DEBUG   : *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** ***
04-06 02:26:27.811  2934  2934 F DEBUG   : Build fingerprint: 'Android/sdk_phone64_arm64/emu64a:16/BE2A.250530.026.D1/13818094:userdebug/test-keys'
04-06 02:26:27.811  2934  2934 F DEBUG   : Revision: '0'
04-06 02:26:27.811  2934  2934 F DEBUG   : ABI: 'arm64'
04-06 02:26:27.811  2934  2934 F DEBUG   : Timestamp: 2026-04-06 02:26:27.799272607+0800
04-06 02:26:27.811  2934  2934 F DEBUG   : Process uptime: 1s
04-06 02:26:27.811  2934  2934 F DEBUG   : Cmdline: ./d8 --sandbox-testing ./oob-controlled-addr.js -- 25000000000
04-06 02:26:27.811  2934  2934 F DEBUG   : pid: 2922, tid: 2922, name: d8  >>> ./d8 <<<
04-06 02:26:27.811  2934  2934 F DEBUG   : uid: 0
04-06 02:26:27.811  2934  2934 F DEBUG   : tagged_addr_ctrl: 0000000000000001 (PR_TAGGED_ADDR_ENABLE)
04-06 02:26:27.811  2934  2934 F DEBUG   : pac_enabled_keys: 000000000000000f (PR_PAC_APIAKEY, PR_PAC_APIBKEY, PR_PAC_APDAKEY, PR_PAC_APDBKEY)
04-06 02:26:27.811  2934  2934 F DEBUG   : signal 11 (SIGSEGV), code 1 (SEGV_MAPERR), fault addr 0x0000005890ee1000
04-06 02:26:27.811  2934  2934 F DEBUG   :     x0  00000007ffffffff  x1  0000007fc6e4d9f0  x2  000000280104d0e9  x3  00000028000007e5
04-06 02:26:27.811  2934  2934 F DEBUG   :     x4  0000000000000000  x5  0000007200d20838  x6  0000000000000001  x7  0000000000000001
04-06 02:26:27.811  2934  2934 F DEBUG   :     x8  0000002a00004000  x9  41ebd5b7dde00000  x10 0000000000000000  x11 1000020000000000
04-06 02:26:27.811  2934  2934 F DEBUG   :     x12 000000280101f3c1  x13 0000000000000000  x14 0000000000000000  x15 0000000000000030
04-06 02:26:27.811  2934  2934 F DEBUG   :     x16 0000000000000004  x17 00000058f7f98680  x18 00000079728d4000  x19 00000005d21dba00
04-06 02:26:27.812  2934  2934 F DEBUG   :     x20 0000000000000001  x21 0000007fc6e4dca8  x22 0000007fc6e4dca0  x23 00000072001a4000
04-06 02:26:27.812  2934  2934 F DEBUG   :     x24 0000000000000000  x25 0000007200d20858  x26 00000058b02589b8  x27 0000002e90edd000
04-06 02:26:27.812  2934  2934 F DEBUG   :     x28 00000007ffffffff  x29 0000007fc6e4dbd0
04-06 02:26:27.812  2934  2934 F DEBUG   :     lr  00000058aeecfa44  sp  0000007fc6e4db60  pc  00000058aeecfacc  pst 0000000040001000
04-06 02:26:27.812  2934  2934 F DEBUG   : 3 total frames
04-06 02:26:27.812  2934  2934 F DEBUG   : backtrace:
04-06 02:26:27.812  2934  2934 F DEBUG   :       #00 pc 000000000099bacc  /data/local/tmp/v8/d8 (BuildId: 3f8347c6c580ccf8)
04-06 02:26:27.812  2934  2934 F DEBUG   :       #01 pc 0000000000be0720  /data/local/tmp/v8/d8 (BuildId: 3f8347c6c580ccf8)
04-06 02:26:27.812  2934  2934 F DEBUG   :       #02 pc 0000000001a7c518  /data/local/tmp/v8/d8 (BuildId: 3f8347c6c580ccf8)

```

- DataPtr = 0x2A00004000 (SAB backing store, inside sandbox)
- offset = 0x5D21DBA00 (25,000,000,000)
- offset \* 8 = 0x2E90EDd000
- DataPtr + offset \* 8 = 0x2A00004000 + 0x2E90EDD000 = 0x5890EE1000
- fault addr = 0x5890EE1000
- sandbox reservation end = 0x5800000000 (sandbox 0x4800000000 + guard 0x1000000000)
- fault - reservation end = 0x5890EE1000 - 0x5800000000 = 0x90EE1000 (~2.3 GB outside)

Changing `offset` directly shifts the fault address by `delta * 8`.

### ch...@google.com (2026-04-06)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-04-06)

Setting Priority to P1 to match Severity s1. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### cl...@chromium.org (2026-04-07)

More ElementsKinds switcheroo? Potentially duplicates of <https://crbug.com/499489156> or <https://crbug.com/499473996>, please check.

### ar...@google.com (2026-04-07)

Thanks for the report. I can reproduce this on a Pixel 9 Pro:

```
Sandbox testing mode is enabled. Only sandbox violations will be reported, all other crashes will be ignored.
Sandbox bounds: [0x2200000000,0x4200000000)

## V8 sandbox violation detected!

Segmentation fault

```

Regarding the controlled write PoC, I believe this doesn't provide an arbitrary write but it is bounded by the max element size for typed arrays (8 \* 32GB). I don't see a way to turn this into an arbitrary write primitive so its impact is limited.

Note for VRP panel: <https://crbug.com/499489156> was technically filed before this issue but provided an invalid PoC. I have closed that as not reproducible, their PoC also seemed not deterministic compared to this report.

### gr...@gmail.com (2026-04-08)

Thanks for the quick reproduction,Below is my understanding. Feel free to discuss with me if there are any errors.  

The 256GB bound is correct, but on Android it covers the RWX JIT code region — this is a full arbitrary write primitive within that range.

Address control is fully precise. The attacker chooses the `offset` parameter to `.set()`, giving 8-byte-granular targeting anywhere in `[DataPtr, DataPtr + 256GB)`.
Value control is fully arbitrary.The Proxy `get` trap returns attacker-controlled doubles. The write path uses `WriteUnalignedValue` (memcpy) with no NaN canonicalization, so all 2^64 bit patterns are writable — including ARM64 instruction encodings. Multiple consecutive 8-byte values can be written in a single `.set()` call.

On Android, this 256GB range covers the RWX JIT code region. The sandbox reservation is 256GB total (64GB front guard + 128GB sandbox + 64GB back guard), but DataPtr starts inside the sandbox, so `DataPtr + 256GB` extends well past the reservation end. On desktop, `kTotalTrailingGuardRegionSize = 288GB` covers the 256GB worst case. On Android, `kAdditionalTrailingGuardRegionSize = 0` (`sandbox.cc:213`) — only the base 64GB back guard remains.

Here is proof from the same d8 process on a Pixel 9 Pro (Android 16). The script reads `/proc/PID/maps` to locate the RWX JIT region, then triggers the TOCTOU and captures the fault address from logcat — all from one process, so ASLR is consistent:

```
reservation_end:  0x5500000000  (+192 GB)
rwx_start:        0x55f0000000  (+195.75 GB)   ← 256 MB rwxp
rwx_end:          0x5600000000  (+196.00 GB)
toctou_fault:     0x6554772000  (+257.32 GB)   ← TOCTOU writes past here

reservation_end < rwx_start < rwx_end < toctou_fault
TRUE — RWX JIT is fully within TOCTOU OOB range

```

V8 has no W^X on Android ARM64 — `RwxMemoryWriteScope::SetWritable()` and `SetExecutable()` are both no-ops (`code-memory-access-inl.h:390-393`), so writes to the JIT region are immediately executable.

To reproduce, push `test.sh` to the device and run:

```
adb push test.sh /data/local/tmp/
adb shell "chmod +x /data/local/tmp/test.sh && /data/local/tmp/test.sh /path/to/d8"

```

The script launches a single d8 process, dumps its `/proc/PID/maps` to find the RWX region, lets the TOCTOU trigger a sandbox violation, then reads the fault address from logcat. It prints the address ordering to confirm the RWX JIT region is fully within the TOCTOU write range. Due to ASLR, ~90% of runs show `TRUE`; if the first run doesn't, re-run.

### ar...@google.com (2026-04-08)

Good point, I wouldn't have expected the RWX region to be that close or at least the randomization to not make this very reliable. On a Pixel 9 Pro it seems very reliably within ~200GB of the sandbox end, for example:

```
2c00000000-2c00010000 r--p 00000000 00:00 0 // Sandbox.start
...
2c01080000-5c00000000 ---p 00000000 00:00 0 // Sandbox.end + guard region
...
63f0000000-63f7400000 rwxp 00000000 00:00 0
...
63f7fc7000-6400000000 rwxp 00000000 00:00 0

```

In this case we should be able to write up to `0x9400000000` so also in the RWX region. I have a work in progress CL that should address this type of issue by masking the write to always end within the sandbox: <https://crrev.com/c/7705535>.

### gr...@gmail.com (2026-04-08)

This Demo demonstrates a **full sandbox escape on Android ARM64**(Some shortcuts were used in the implementation, but I believe they are entirely achievable in a real-world attack scenario.): starting from sandbox-internal corruption, the TOCTOU bug in `TypedArray.prototype.set()` is used to write attacker-controlled ARM64 machine code into the V8 JIT RWX code region, which is then executed by calling a JIT-compiled JS function. The shellcode performs `openat` + `write` + `close` syscalls to create a file `/data/local/tmp/pwned` with content "PWNED".

### How to reproduce

```
adb push shellcode.sh /data/local/tmp/
adb shell "chmod +x /data/local/tmp/shellcode.sh"
adb shell "/data/local/tmp/shellcode.sh /path/to/d8"

```

Expected output:

```
[+] /data/local/tmp/pwned EXISTS!
[+] Content: PWNED

```

The script retries up to 5 times to handle ASLR (succeeds ~80% per attempt).

### ar...@google.com (2026-04-08)

Nice! I can reproduce this:

```
$ 
=== Real Shellcode v2: NOP sled + file write ===

--- Attempt 1 ---
[*] PID: 10597
[*] RWX: 5af0000000-5af7400000 rwxp 00000000 00:00 0
[*] Offset: 25199376384

=== d8 OUTPUT ===
Sandbox testing mode is enabled. Only sandbox violations will be reported, all other crashes will be ignored.
Sandbox bounds: [0x2a00000000,0x4a00000000)
[*] shellcode_target(10) before = 73
[*] DataPtr = 0x2c00004000
DATAPTR=188978577408
PAUSE
[*] TOCTOU offset = 25199376384
[*] Block size: 40 doubles, spraying 4096 doubles
[+] TOCTOU write completed! Sprayed 4096 doubles
[*] Calling shellcode_target(10)...
[*] result = 4919
[+] Shellcode returned Smi(0x1337)!

=== PROOF ===
[+] /data/local/tmp/pwned EXISTS!
[+] Content: PWNED
-rw-r--r-- 1 shell shell 6 2025-05-17 21:42 /data/local/tmp/pwned

$ cat /data/local/tmp/pwned
PWNED

```

The PoC looks up the actual offsets in the process map but I think it should be possible to use a similar read primitive to find the proper locations.

### dx...@google.com (2026-04-15)

Project: v8/v8  

Branch:  main  

Author:  Arash Kazemi [arashk@chromium.org](mailto:arashk@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7705535>

[sandbox] Mask TypedArray stores to be within bounded size on Android

---


Expand for full commit details
```
     
    This CL adds masking to all TypedArray stores to prevent out-of-sandbox 
    writes caused by double fetching of the elements kind, aka ElementsKind 
    switcheroo. This bypass is currently prevented by having additional 
    guard regions, except for Android where address space is limited. 
    Masking all stores mitigates this issue on Android without requiring 
    large address reservations. 
     
    Fixed: 475479180, 499717570, 500413224 
    Change-Id: I55e6faea2351c854707fb1c01454723ea323d419 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7705535 
    Reviewed-by: Michael Lippautz <mlippautz@chromium.org> 
    Commit-Queue: Arash Kazemi <arashk@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#106485}

```

---

Files:

- M `include/v8-internal.h`
- M `src/builtins/builtins-sharedarraybuffer-gen.cc`
- M `src/codegen/code-stub-assembler.cc`
- M `src/objects/elements.cc`
- M `src/sandbox/sandbox.cc`
- A `test/mjsunit/sandbox/regress-499717570.js`

---

Hash: [f1917d3b041b114c9a613e98208e9d33e69e7bf3](https://chromiumdash.appspot.com/commit/f1917d3b041b114c9a613e98208e9d33e69e7bf3)  

Date: Tue Apr 14 11:14:22 2026


---

### dx...@google.com (2026-04-15)

Project: v8/v8  

Branch:  main  

Author:  Nico Hartmann [nicohartmann@chromium.org](mailto:nicohartmann@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7762053>

Revert "[sandbox] Mask TypedArray stores to be within bounded size on Android"

---


Expand for full commit details
```
     
    This reverts commit f1917d3b041b114c9a613e98208e9d33e69e7bf3. 
     
    Reason for revert: I suspect this to cause pgo issues on an android bot blocking the roll https://ci.chromium.org/ui/p/chromium/builders/try/android-binary-size/2690807/overview 
     
    Original change's description: 
    > [sandbox] Mask TypedArray stores to be within bounded size on Android 
    > 
    > This CL adds masking to all TypedArray stores to prevent out-of-sandbox 
    > writes caused by double fetching of the elements kind, aka ElementsKind 
    > switcheroo. This bypass is currently prevented by having additional 
    > guard regions, except for Android where address space is limited. 
    > Masking all stores mitigates this issue on Android without requiring 
    > large address reservations. 
    > 
    > Fixed: 475479180, 499717570, 500413224 
    > Change-Id: I55e6faea2351c854707fb1c01454723ea323d419 
    > Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7705535 
    > Reviewed-by: Michael Lippautz <mlippautz@chromium.org> 
    > Commit-Queue: Arash Kazemi <arashk@chromium.org> 
    > Cr-Commit-Position: refs/heads/main@{#106485} 
     
    Bug: 475479180, 499717570, 500413224 
    No-Presubmit: true 
    No-Tree-Checks: true 
    No-Try: true 
    Change-Id: I3dd7495bbd3ed003001ad908ce2471a4d55f4c16 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7762053 
    Owners-Override: Nico Hartmann <nicohartmann@chromium.org> 
    Bot-Commit: rubber-stamper@appspot.gserviceaccount.com <rubber-stamper@appspot.gserviceaccount.com> 
    Commit-Queue: Nico Hartmann <nicohartmann@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#106502}

```

---

Files:

- M `include/v8-internal.h`
- M `src/builtins/builtins-sharedarraybuffer-gen.cc`
- M `src/codegen/code-stub-assembler.cc`
- M `src/objects/elements.cc`
- M `src/sandbox/sandbox.cc`
- D `test/mjsunit/sandbox/regress-499717570.js`

---

Hash: [00d5009540ed0a2f19fd267db418cacc51385728](https://chromiumdash.appspot.com/commit/00d5009540ed0a2f19fd267db418cacc51385728)  

Date: Wed Apr 15 12:47:17 2026


---

### gr...@gmail.com (2026-05-17)

Hey team, just wondering — is this vulnerability fixed now?

### ar...@google.com (2026-05-18)

Yes the sandbox bypass should be fixed with [crrev.com/c/7761897](https://crrev.com/c/7761897), I had to reland the CL but didn't realize the automation didn't pick up the associated bug numbers so there is no comment for the reland. Did you find that it still reproduces on ToT?

### sp...@google.com (2026-06-15)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $5000.00 for this report.

Rationale for this decision:
v8 Sandbox


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### gr...@gmail.com (2026-06-16)

Appeal reward reason:  

As demonstrated in [comment #9](https://issues.chromium.org/issues/499717570#comment9), the submitted PoC achieves a fully working V8 sandbox escape with arbitrary native code execution on Android ARM64. Specifically, it exploits a TOCTOU vulnerability in TypedArray.prototype.set() to write attacker-controlled shellcode into the V8 JIT RWX code region, and then triggers execution by invoking the corresponding JIT-compiled JavaScript function. The shellcode performs openat, write, and close syscalls, creating the file /data/local/tmp/pwned with the contents "PWNED" as a verifiable side effect.  

Regarding the use of process maps: in the submitted PoC, the RWX region offset was obtained by reading process maps purely for testing convenience, in order to make the PoC reliable and reproducible during evaluation. This is not a fundamental requirement of the exploit. In a realistic exploitation scenario, the same primitive can be achieved entirely through sandbox-internal corruption, without relying on any external information source such as /proc/self/maps.  

Based on the above, I believe this report meets the criteria for "Controlled V8 sandbox escape", and I would like to kindly ask the panel to reassess the reward tier accordingly.  

Thank you for your time and consideration.

### gr...@gmail.com (2026-07-01)

Hi team,  

As a follow-up to [comment #16](https://issues.chromium.org/issues/499717570#comment16), I would like to provide an updated PoC that no longer relies on /proc/self/maps to obtain the RWX address.  

In this new PoC, instead of using --sandbox-testing, I leveraged a previously-fixed in-sandbox issue (<https://chromium-review.googlesource.com/c/v8/v8/+/7604253>) as the demonstration primitive. The RWX address is obtained through the same in-sandbox issue as well, so the entire exploit chain now operates without any external information source.

#### Build & environment

V8 commit: c0a41078e69f23668c8d34c61f286a1b5b211f19  

args.gn:

```
target_os = "android"
target_cpu = "arm64"
v8_enable_sandbox = true
is_debug = false
is_component_build = false
v8_static_library = true
symbol_level = 1

```
#### Reproduction

```
emu64a:/data/local/tmp/v8_new # rm -rf /data/local/tmp/pwned
emu64a:/data/local/tmp/v8_new # ./d8 --allow-natives-syntax --expose-externalize-string poc.js
Trap
133|emu64a:/data/local/tmp/v8_new # cat /data/local/tmp/pwned
PWNED 

```
#### Notes

- The PoC succeeds with roughly ~60% probability per run; if a single attempt fails, simply re-running a few times reliably reproduces the result.
- --expose-externalize-string is used for PoC convenience only. ExternalStrings are abundant in real Chrome (DOM strings, network data, etc.), so this flag does not represent an additional exploitation prerequisite in a real-world scenario.

### sp...@google.com (2026-07-10)

*NOTE: This is an automatically generated email*

Hello,

Chrome Vulnerability Rewards Program (VRP) Panel has decided to issue a reward of
**$15000.00** for your report. Congratulations!

Rationale for this decision:

In the future, please try and use the test harnesses provided as this allows the team to triage your reports more easily and also do not submit reports as zip files.

Important payment guidance:

- **Legacy**: If you aren't already registered with Google as a supplier,
  [p2p-vrp@google.com](mailto:p2p-vrp@google.com) will reach out to you. If you have registered in the
  past, no need to repeat the process – you can sit back and relax, and we
  will process the payment soon.
  
  If you have any payment related requests, please direct them to
  [p2p-vrp@google.com](mailto:p2p-vrp@google.com). Please remember to include the subject of this email and
  the email address that the report was sent from.

Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot

P.S. One other thing we'd like to mention:

- Please do NOT publicly disclose details until a fix has been released to all
  our users. Early public disclosure may cancel the provisional reward. Also,
  please be considerate about disclosure when the bug affects a core library
  that may be used by other products. Please do NOT share this information
  with third parties who are not directly involved in fixing the bug. Doing so
  may cancel the provisional reward. Please be honest if you have already
  disclosed anything publicly or to third parties. Lastly, we understand that
  some of you are not interested in money. We offer the option to donate your
  reward to an eligible charity. Any rewards that are unclaimed after 12
  months will be donated to a charity of our choosing.

Please contact [security-vrp@chromium.org](mailto:security-vrp@chromium.org) with any questions.

### ch...@google.com (2026-07-23)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/499717570)*
