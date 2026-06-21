# V8 Sandbox Bypass: AAW/PC Control via code marked for deopt (ARM64 only)

| Field | Value |
|-------|-------|
| **Issue ID** | [481295170](https://issues.chromium.org/issues/481295170) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>JavaScript>Sandbox |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | kr...@gmail.com |
| **Assignee** | ol...@google.com |
| **Created** | 2026-02-03 |
| **Bounty** | $20,000.00 |

## Description

### VULNERABILITY DETAILS

#### Summary

ARM64 [does not zap code](https://source.chromium.org/chromium/chromium/src/+/main:v8/src/deoptimizer/arm64/deoptimizer-arm64.cc;l=25;drc=1d1fcea6ebbc1c2c3d04ab5538c74f742c66444f) when it gets [marked for deopt](https://source.chromium.org/chromium/chromium/src/+/main:v8/src/objects/code.cc;l=241;drc=1d1fcea6ebbc1c2c3d04ab5538c74f742c66444f) unlike x64 which means we can still call such code using in-sandbox corruption without it resulting in an immediate crash. This can lead to AAW/PC control and one such way is shown by resurrecting [crbug/443772809](https://crbug.com/443772809).

**Suggested Fix:** Implement `Deoptimizer::ZapCode` for ARM64 too.

#### Details

To explain the specifics of this PoC, notice [crbug/443772809](https://crbug.com/443772809) exploited the fact that the contents of a dispatch entry can be modified while there are stale references to it. This allowed the stack to become imbalanced as the dispatch entry could be modified to use an entrypoint with a higher parameter count leading to underapplication when called via the stale references. [crbug/443772809](https://crbug.com/443772809) was fixed by deoptimizing functions that used the dispatch entry when it gets freed.

However, in ARM64 the Code is still lying around. Moreover, while [embedded objects and dispatch handles are cleared](https://source.chromium.org/chromium/chromium/src/+/main:v8/src/heap/mark-compact.cc;l=3504;drc=1850704180fcfdc9614b7045306fabefed43ef0a) in the code being marked for deoptimization, the instructions to actually load from the table and call are still intact. Thus, an attacker can simply just call the stale code to use the stale reference and imbalance the stack like before. For the PoC, to call the stale code `DebugBreakTrampoline` was used[1], but it might simply be possible to reinstall the Code on some function (never tried).

[1] `Sandbox.setFunctionCodeToBuiltin` was used for convenience, in practice something like [crbug/435630464](https://crbug.com/435630464) or the wasm export cache could be used to install `DebugBreakTrampoline`.

### VERSION

V8 commit: 91a0f4eefb2c0d70b0d8dc699bac822a3aa5f5aa

#### REPRODUCTION CASE

I don't have an ARM64 environment, so I used the simulator.

**Build args:**

```
is_debug=false
is_asan=true
v8_enable_sandbox=true
v8_enable_memory_corruption_api=true
dcheck_always_on=false
target_cpu="x64"
v8_target_cpu="arm64"
v8_control_flow_integrity=false # Mac doesn't have it and i'm lazy to walk around PAC :D

```

**Shell args:** `--sandbox-testing --expose-gc --allow-natives-syntax`

**Sample output (since the simulator is used it says it's harmless):**

```
Sandbox testing mode is enabled. Only sandbox violations will be reported, all other crashes will be ignored.
Sandbox bounds: [0x7a8c00000000,0x7b8c00000000)
ACCESS BELOW STACK POINTER:
  sp is here:          0x00007bcd7e8c6af0
  access was here:     0x00007bcd7e8c6a18
  stack limit is here: 0x00007bcd7e6c6c00



#
# Safely terminating process due to error in , line 0
# The following harmless error was encountered: ACCESS BELOW STACK POINTER
#
#
#
#FailureMessage Object: 0x7bcdc97e0060
==== C stack trace ===============================

    ./v8/out/playground_arm64/d8(___interceptor_backtrace+0x46) [0x55f7c2157b36]
    ./v8/out/playground_arm64/d8(+0x62bc5e4) [0x55f7c705c5e4]
    ./v8/out/playground_arm64/d8(+0x62baaab) [0x55f7c705aaab]
    ./v8/out/playground_arm64/d8(+0x629a0de) [0x55f7c703a0de]
    ./v8/out/playground_arm64/d8(+0x3dba363) [0x55f7c4b5a363]
    ./v8/out/playground_arm64/d8(+0x3da8cef) [0x55f7c4b48cef]
    ./v8/out/playground_arm64/d8(+0x3da89a9) [0x55f7c4b489a9]
    ./v8/out/playground_arm64/d8(+0x3da5dcc) [0x55f7c4b45dcc]
    ./v8/out/playground_arm64/d8(+0x1b2acf3) [0x55f7c28cacf3]
    ./v8/out/playground_arm64/d8(+0x1b2c239) [0x55f7c28cc239]
    ./v8/out/playground_arm64/d8(+0x173a11c) [0x55f7c24da11c]
    ./v8/out/playground_arm64/d8(+0x147b528) [0x55f7c221b528]
    ./v8/out/playground_arm64/d8(+0x14b382a) [0x55f7c225382a]
    ./v8/out/playground_arm64/d8(+0x14bfb2e) [0x55f7c225fb2e]
    ./v8/out/playground_arm64/d8(+0x14bef66) [0x55f7c225ef66]
    ./v8/out/playground_arm64/d8(+0x14c2608) [0x55f7c2262608]
    /usr/lib/libc.so.6(+0x27635) [0x7fcdcb510635]
    /usr/lib/libc.so.6(__libc_start_main+0x89) [0x7fcdcb5106e9]
    ./v8/out/playground_arm64/d8(_start+0x2a) [0x55f7c211002a]

```

If you comment out the body of `Simulator::CheckMemoryAccess` to more closely mimic hardware and add `--trace-sim` it can be seen trying to return to 0x424242424242:

```
0x00005563f0000230  8b306fff            add sp, sp, x16, lsl #3
#    sp: 0x00007b89c7270a40
0x00005563f0000234  d65f03c0            ret

## V8 sandbox violation detected!

The sandbox violation was a *read* access which is technically not a sandbox violation. This requires manual investigation.
Received signal 11 SEGV_MAPERR 424242424242

==== C stack trace ===============================

./v8/out/playground_arm64/d8(___interceptor_backtrace+0x46) [0x55630d307b36]
./v8/out/playground_arm64/d8(+0x62bc3d0) [0x55631220c3d0]
./v8/out/playground_arm64/d8(+0x2d79caa) [0x55630ecc9caa]
/usr/lib/libc.so.6(+0x3e4d0) [0x7f8a13e644d0]
./v8/out/playground_arm64/d8(+0x3da1697) [0x55630fcf1697]
./v8/out/playground_arm64/d8(+0x3da8cef) [0x55630fcf8cef]
./v8/out/playground_arm64/d8(+0x3da89a9) [0x55630fcf89a9]
./v8/out/playground_arm64/d8(+0x3da5dcc) [0x55630fcf5dcc]
./v8/out/playground_arm64/d8(+0x1b2acf3) [0x55630da7acf3]
./v8/out/playground_arm64/d8(+0x1b2c239) [0x55630da7c239]
./v8/out/playground_arm64/d8(+0x173a11c) [0x55630d68a11c]
./v8/out/playground_arm64/d8(+0x147b528) [0x55630d3cb528]
./v8/out/playground_arm64/d8(+0x14b382a) [0x55630d40382a]
./v8/out/playground_arm64/d8(+0x14bfb2e) [0x55630d40fb2e]
./v8/out/playground_arm64/d8(+0x14bef66) [0x55630d40ef66]
./v8/out/playground_arm64/d8(+0x14c2608) [0x55630d412608]
/usr/lib/libc.so.6(+0x27635) [0x7f8a13e4d635]
/usr/lib/libc.so.6(__libc_start_main+0x89) [0x7f8a13e4d6e9]
./v8/out/playground_arm64/d8(_start+0x2a) [0x55630d2c002a]
[end of stack trace]
[1]    43333 segmentation fault  ./v8/out/playground_arm64/d8 --sandbox-testing --expose-gc  --trace-sim

```
### FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION

Type of crash: Sandbox violation

### CREDIT INFORMATION

Reporter credit: Krishna Ravishankar (@krsh732)

## Attachments

- [arm64-sim-zap-poc.js](attachments/arm64-sim-zap-poc.js) (text/javascript, 2.8 KB)

## Timeline

### ch...@google.com (2026-02-03)

This V8 bug has been marked as either a release blocker or a vulnerability bug. V8 bugs affect all OSs supported by Chrome, so the OS field has been updated to reflect this. Please update the bug with the correct OS field if it only affects a subset of OSes.

### xi...@chromium.org (2026-02-03)

Thanks for the report. Following the V8 Sandbox Bypass guidance to triage this bug.

### ta...@google.com (2026-02-04)

Hi Andreas, CYPTAL?

### ol...@chromium.org (2026-02-05)

That is a neat escape that actually exposes two separate flaws.

1. The main problem here is that we confuse the optimized code for baseline code. The SFI should only contain baseline code and we must check that. Clever idea to revive deopted code via SFI!
2. The next problem is indeed we are still calling cleared dispatch handles :/
3. We might also port code zapping as a defense in depth to arm64...

### ol...@chromium.org (2026-02-05)

Thanks for reporting it!

### kr...@gmail.com (2026-02-05)

Thank you for the kind words!

### dx...@google.com (2026-02-06)

Project: v8/v8  

Branch:  main  

Author:  Olivier Flückiger [olivf@chromium.org](mailto:olivf@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7548783>

[sandbox] Remove hard-coded CallJSDispatchEntry

---


Expand for full commit details
```
     
    Always call through the proper relocated dispatch handle. Ensures 
    cleared handles cannot be called. 
     
    Bug: 481295170 
    Change-Id: I53f5c2d303edadea62019dacf34634d6809b6534 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7548783 
    Reviewed-by: Leszek Swirski <leszeks@chromium.org> 
    Commit-Queue: Olivier Flückiger <olivf@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#105108}

```

---

Files:

- M `src/codegen/arm64/macro-assembler-arm64.cc`
- M `src/codegen/arm64/macro-assembler-arm64.h`
- M `src/codegen/riscv/macro-assembler-riscv.cc`
- M `src/codegen/riscv/macro-assembler-riscv.h`
- M `src/codegen/x64/macro-assembler-x64.cc`
- M `src/codegen/x64/macro-assembler-x64.h`

---

Hash: [1973b12d6241a7e7a82965447dc40fb6a8fb7bd5](https://chromiumdash.appspot.com/commit/1973b12d6241a7e7a82965447dc40fb6a8fb7bd5)  

Date: Thu Feb 5 16:25:25 2026


---

### dx...@google.com (2026-02-06)

Project: v8/v8  

Branch:  main  

Author:  Olivier Flückiger [olivf@chromium.org](mailto:olivf@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7544874>

[sandbox] Ensure sfi contains baseline code

---


Expand for full commit details
```
     
    We should not load any other kind of code from the SFI. 
     
    Bug: 481295170 
    Change-Id: Id2b2ed7f402bd1ede5ac8735d208942454131dea 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7544874 
    Auto-Submit: Olivier Flückiger <olivf@chromium.org> 
    Reviewed-by: Leszek Swirski <leszeks@chromium.org> 
    Commit-Queue: Olivier Flückiger <olivf@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#105115}

```

---

Files:

- M `src/builtins/arm64/builtins-arm64.cc`
- M `src/builtins/riscv/builtins-riscv.cc`
- M `src/builtins/x64/builtins-x64.cc`
- M `src/codegen/code-stub-assembler.cc`
- M `src/codegen/code-stub-assembler.h`
- M `src/objects/shared-function-info-inl.h`
- M `src/objects/shared-function-info.cc`

---

Hash: [86120e12cf11f9920379dc10e473cfd9c12e5478](https://chromiumdash.appspot.com/commit/86120e12cf11f9920379dc10e473cfd9c12e5478)  

Date: Thu Feb 5 15:07:26 2026


---

### dx...@google.com (2026-02-09)

Project: v8/v8  

Branch:  main  

Author:  Liu Yu [liuyu@loongson.cn](mailto:liuyu@loongson.cn)  

Link:    <https://chromium-review.googlesource.com/7553890>

[loong64][sandbox] Ensure sfi contains baseline code

---


Expand for full commit details
```
     
    Port commit 86120e12cf11f9920379dc10e473cfd9c12e5478 
     
    Bug: 481295170 
    Change-Id: I8e9cacaeb270b99a7548bf18b1740ac2d32e9f2a 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7553890 
    Commit-Queue: Zhao Jiazhong <zhaojiazhong-hf@loongson.cn> 
    Auto-Submit: Liu Yu <liuyu@loongson.cn> 
    Reviewed-by: Zhao Jiazhong <zhaojiazhong-hf@loongson.cn> 
    Cr-Commit-Position: refs/heads/main@{#105128}

```

---

Files:

- M `src/builtins/loong64/builtins-loong64.cc`

---

Hash: [3a2e25fe861344c4e8c5bfc4c25e14faa209ea23](https://chromiumdash.appspot.com/commit/3a2e25fe861344c4e8c5bfc4c25e14faa209ea23)  

Date: Sat Feb 7 09:14:59 2026


---

### dx...@google.com (2026-02-09)

Project: v8/v8  

Branch:  main  

Author:  Liu Yu [liuyu@loongson.cn](mailto:liuyu@loongson.cn)  

Link:    <https://chromium-review.googlesource.com/7553870>

[loong64][sandbox] Remove hard-coded CallJSDispatchEntry

---


Expand for full commit details
```
     
    Port commit 1973b12d6241a7e7a82965447dc40fb6a8fb7bd5 
     
    Bug: 481295170 
    Change-Id: Ib6ba55387d0c93be006036aa54c8b9ce49961bb4 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7553870 
    Auto-Submit: Liu Yu <liuyu@loongson.cn> 
    Reviewed-by: Zhao Jiazhong <zhaojiazhong-hf@loongson.cn> 
    Commit-Queue: Zhao Jiazhong <zhaojiazhong-hf@loongson.cn> 
    Cr-Commit-Position: refs/heads/main@{#105129}

```

---

Files:

- M `src/codegen/loong64/macro-assembler-loong64.cc`
- M `src/codegen/loong64/macro-assembler-loong64.h`

---

Hash: [3e4a34843f5c499b92acbcd9a05bd6f4bef8048a](https://chromiumdash.appspot.com/commit/3e4a34843f5c499b92acbcd9a05bd6f4bef8048a)  

Date: Sat Feb 7 08:57:23 2026


---

### dx...@google.com (2026-02-11)

Project: v8/v8  

Branch:  main  

Author:  Gyuyoung Kim [gyuyoung@igalia.com](mailto:gyuyoung@igalia.com)  

Link:    <https://chromium-review.googlesource.com/7556277>

Fix mksnapshot failure

---


Expand for full commit details
```
     
    Resolve a !is_linked() assertion failure in v8/src/codegen/label.h by 
    wrapping it with a !V8_JITLESS_BOOL guard. 
     
    This issue was introduced by https://crrev.com/c/7544874. 
     
    Bug: 481295170 
    Change-Id: Ia7c2828aa454a3b24fcc80a72756943ba1057436 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7556277 
    Reviewed-by: Olivier Flückiger <olivf@chromium.org> 
    Commit-Queue: Gyuyoung Kim <gyuyoung@igalia.com> 
    Reviewed-by: Leszek Swirski <leszeks@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#105193}

```

---

Files:

- M `src/builtins/arm64/builtins-arm64.cc`
- M `src/builtins/riscv/builtins-riscv.cc`
- M `src/builtins/x64/builtins-x64.cc`
- M `src/codegen/code-stub-assembler.cc`

---

Hash: [ef44b4d99435dfecd3c78065c39a4217a179fd1d](https://chromiumdash.appspot.com/commit/ef44b4d99435dfecd3c78065c39a4217a179fd1d)  

Date: Tue Feb 10 02:24:45 2026


---

### ch...@google.com (2026-06-15)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### sp...@google.com (2026-06-15)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $20000.00 for this report.

Rationale for this decision:
Baseline. v8 sandbox escape.


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/481295170)*
