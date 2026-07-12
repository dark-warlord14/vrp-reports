# ANGLE Metal ProvokingVertexHelper uint32 Overflow causes GPU OOB Write

| Field | Value |
|-------|-------|
| **Issue ID** | [484986863](https://issues.chromium.org/issues/484986863) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>GPU>ANGLE |
| **Platforms** | Mac |
| **Reporter** | ci...@gmail.com |
| **Assignee** | ge...@chromium.org |
| **Created** | 2026-02-16 |
| **Bounty** | $4,000.00 |

## Description

---

### Report description

ANGLE Metal ProvokingVertexHelper uint32 Overflow causes GPU OOB Write

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

#### Which URL (or repository) have you found the vulnerability in?

<https://chromium.googlesource.com/angle/angle/+/refs/heads/main/src/libANGLE/renderer/metal/ProvokingVertexHelper.mm>

---

### The problem

#### Please describe the technical details of the vulnerability

A `uint32` integer overflow in ANGLE's Metal backend `ProvokingVertexHelper::generateIndexBuffer()` allows any WebGL 2 webpage to trigger a ~17GB GPU heap buffer overflow. The function `indexCountForPrimCount()` computes `primCount * 3` in 32-bit unsigned arithmetic. With `count=1431655768`, `primCount = count - 2 = 1431655766`, then `primCount * 3 = 0x100000002` wraps to 2, allocating 8 bytes while the GPU compute shader dispatches 1.4 billion primitives writing ~17GB past the allocation.

This produces a controlled write primitive: the attacker-chosen `firstVertex` value is written to every 3rd uint32 across ~17GB of GPU memory, corrupting other WebGL buffers. The corrupted data is readable from JavaScript via `getBufferSubData()`.

The shader must use a `flat` interpolation qualifier to trigger the `ProvokingVertexHelper` code path (ANGLE's provoking vertex convention rewrite). Without `flat`, ANGLE routes through the safe `TriangleFanBoundCheck` in `mtl_utils.mm` which correctly rejects the oversized draw. With `flat`, ANGLE routes through the vulnerable `indexCountForPrimCount` in `ProvokingVertexHelper.mm`. No user interaction, no permissions, no flags required. Runs in the GPU process and affects all macOS (Intel + Apple Silicon confirmed), Metal backend only.

### Affected Code

Primary overflow in `ProvokingVertexHelper.mm:51-75`:

```
static inline uint indexCountForPrimCount(const uint fixIndexBufferKey, const uint primCount)
{
    switch (fixIndexBufferMode) {
        case MtlFixIndexBufferKeyTriangleStrip:
            return primCount * 3;  // uint32 OVERFLOW when primCount > UINT32_MAX/3
        case MtlFixIndexBufferKeyTriangleFan:
            return primCount * 3;  // same overflow
    }
}

```

Undersized allocation in `ProvokingVertexHelper.mm:238-244`:

```
uint primCount     = primCountForIndexCount(indexBufferKey, (uint32_t)indexCount);
uint newIndexCount = indexCountForPrimCount(indexBufferKey, primCount);   // wraps to 2
ANGLE_TRY(mIndexBuffers.allocate(context, newIndexCount * indexSize, ...)); // 8 bytes!
// GPU dispatch: 22.4M thread groups writing ~17GB to the 8-byte buffer

```

Silent error handling in `ContextMtl.mm:2956-2961`: `checkCommandBufferError()` only checks `MTLCommandBufferErrorOutOfMemory`. All other errors (including GPU timeout/internal error from the 17GB write) are silently ignored. Corrupted buffers remain accessible.

### Steps to Reproduce

Prerequisites: Chrome on macOS (any version using ANGLE Metal backend, Chrome 96+).

#### Minimal overflow (`overflow_minimal.html`) - no flags required:

```
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  "file:///path/to/overflow_minimal.html"

```

1. Open `overflow_minimal.html` in Chrome on macOS
2. The overflow triggers automatically on page load
3. Expected: `drawArrays` accepted with GL error 0x0000, then after 30s: "Context survived. ANGLE silently handled the GPU timeout." Chrome's stderr will show: `mtl_command_buffer.mm:693 (onCommandBufferCompleted): Completed MTLCommandBuffer failed, and error is Caused GPU Timeout Error (00000002:kIOAccelCommandBufferCallbackErrorTimeout)`.

#### Write primitive (`write_primitive.html`) - requires `--in-process-gpu`:

```
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --in-process-gpu \
  "file:///path/to/write_primitive.html"

```

1. Open `write_primitive.html` in Chrome on macOS with `--in-process-gpu`
2. Click "Run Write Primitive Test"
3. Wait ~30 seconds (15s GPU write + readback)
4. Expected result: 200/600 victim buffers show corruption. Attacker-chosen `firstVertex` value `0x2AAAAAA0` appears every 3rd uint32 in victim buffers, readable via `getBufferSubData()`. The output will show `CONFIRMED: Attacker value 0x2AAAAAA0 in 200 victim buffers.`
5. If batch 0 shows 0 corrupted, click again without refreshing (race timing).

The `--in-process-gpu` flag runs the GPU process in-process, which changes GPU error recovery timing and allows readback of corrupted buffer data before the driver's error recovery cleans it up. On Chrome stable without this flag, the overflow fires and corrupts cross-buffer memory (visible as 0xDEADBEEF markers overwritten to zeros in 297/600 buffers), but the GPU error recovery zeros corrupted regions before JavaScript can read the overflow's index pattern. The `--in-process-gpu` flag is NOT required for the bug to trigger - the overflow is reachable from any renderer via normal IPC to the GPU process.

Tested on:

- Chrome 144.0.7559.133 (Official Build) (x86\_64), macOS 15.7.2
- Chrome 146.0.7676.0 (Developer Build) (x86\_64), macOS 15.7.2

Note on hardware variability: The write primitive PoC requires winning a race condition to place victim buffers in the GPU overflow write path. On my test hardware (Intel/AMD MacBook Pro 15,3), this succeeds on the first attempt with 200/600 buffers corrupted (batch 0: 200/200). On Apple Silicon (M1), the GPU error recovery mechanism (`kIOGPUCommandBufferCallbackErrorInnocentVictim`) kills in-flight command buffers as collateral damage, preventing readback of corrupted data in our testing - though the overflow itself still fires (visible as GPU reset in kernel logs). The `overflow_minimal.html` PoC is the simplest way to confirm the overflow triggers on any hardware.

#### System DoS (no flags required)

Opening any of the PoCs in default Chrome (no flags) may trigger kernel-level GPU resets or "visual snow". The macOS kernel GPU restart report directly names `genIndexBuffer` as the hung shader. This was followed by WindowServer watchdog timeout and full system freeze requiring forced reboot.

### Fix

Promote `primCount * 3` to 64-bit and validate before allocation:

```
static inline uint64_t indexCountForPrimCount(const uint fixIndexBufferKey, const uint primCount)
{
    switch (fixIndexBufferMode) {
        case MtlFixIndexBufferKeyTriangleStrip:
        case MtlFixIndexBufferKeyTriangleFan:
            return static_cast<uint64_t>(primCount) * 3;
    }
}

// In generateIndexBuffer():
uint64_t newIndexCount = indexCountForPrimCount(indexBufferKey, primCount);
ANGLE_CHECK(context, newIndexCount <= std::numeric_limits<uint32_t>::max(),
            "Index count overflow in provoking vertex rewrite", GL_OUT_OF_MEMORY);

```

Note: A safe pattern already exists in ANGLE at `mtl_utils.mm:1577-1598` (`TriangleFanBoundCheck` + `GetTriangleFanIndicesCount`) which uses `size_t` arithmetic with explicit overflow checks. The vulnerable `indexCountForPrimCount` deviates from this existing safe pattern.

Additionally, `checkCommandBufferError()` at `ContextMtl.mm:2956` should handle `MTLCommandBufferErrorTimeout` and other error codes instead of silently ignoring them.

### Bisect

Introducing commit: `da3db87ec4a491a650d86d3d2776466a48135972` ("Upstream latest changes to Metal backend from Apple to 7/1/2021"), committed October 1, 2021. Review: <https://chromium-review.googlesource.com/c/angle/angle/+/3167010>. Bug: angleproject:6395. The `primCount * 3` overflow has been present since this initial commit of `ProvokingVertexHelper.mm`. The `preconditionIndexBuffer` path (line 193-199) has the same overflow.

Earliest affected stable release: Chrome 96 (stable November 16, 2021). Chrome 95 branched September 9, 2021, before this commit landed. Chrome 96 branched October 7, 2021, after.

The `rewrite_indices.metal` compute shader lacks `ANGLE_KERNEL_GUARD` bounds checking. While it has a manual `if(prim < primCount)` guard, this checks against the correct (non-overflowed) primitive count, not the output buffer size. The safe `TriangleFanBoundCheck` pattern at `mtl_utils.mm:1577` predates this code (Copyright 2019).

#### Impact analysis

GPU process controlled write primitive from any webpage.

| Primitive | PoC | Evidence |
| --- | --- | --- |
| Write | `write_primitive.html` | 193/200 victim buffers contain attacker-chosen `firstVertex` value `0x2AAAAAA0` every 3rd uint32, readable via `getBufferSubData()`. |
| System DoS | Any PoC, no flags | 10 kernel GPU resets + 5 WindowServer crashes in one session. Kernel report names `genIndexBuffer` as hung shader. Full system freeze requiring forced reboot. |

Write characterization: the overflow writes ~17GB sequentially through GPU VA space. The TRIANGLE\_FAN index rewrite pattern `{firstVertex+prim+2, firstVertex, firstVertex+prim+1}` means every 3rd uint32 = the attacker-chosen `firstVertex` value exactly. The other 2/3 are sequential counters offset by `firstVertex`. Data is readable from JavaScript via `getBufferSubData()`. The write is sequential and the attacker controls 1/3 of the written values.

---

### The cause

#### What version of Chrome have you found the security issue in?

Chrome 144.0.7559.133 Stable

#### Is the security issue related to a crash?

Yes, it is related to a crash.

#### Choose the type of vulnerability

Memory Corruption (in a sandboxed process)

#### How would you like to be publicly acknowledged for your report?

cinzinga

## Attachments

- [write_primitive.html](attachments/write_primitive.html) (text/html, 5.8 KB)
- [overflow_minimal.html](attachments/overflow_minimal.html) (text/html, 2.5 KB)
- [lldb_out.txt](attachments/lldb_out.txt) (text/plain, 49.6 KB)

## Timeline

### an...@chromium.org (2026-02-18)

[security shepherd]: Thanks for the report. Triaging this to owner of directory. @ge...@chromium.org , would you be able to help investigate this report? Thanks!

### ch...@google.com (2026-02-19)

Setting milestone because of s2 severity.

### ch...@google.com (2026-02-19)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ci...@gmail.com (2026-03-04)

Attaching a fully symbolized stack trace with function names, source files, and line numbers, plus Metal Shader Validation OOB confirmation (lldb\_out.txt).

ASan can't catch this one - the uint32 overflow happens in CPU code but the resulting OOB write is dispatched to the GPU via a Metal compute shader. GPU buffer memory is invisible to ASan. Apple's Metal Shader Validation (GPU-side bounds checking) confirms the OOB:

[GPUDebug] Invalid device store at offset 72192, executing kernel function: "genIndexBuffer"
buffer: <unnamed>, length:65535, resident:Read Write

Key highlights from the attached lldb session (Chrome ASan 144.x, macOS, --in-process-gpu):

```
  #0  generateIndexBuffer                at ProvokingVertexHelper.mm:249
  #1  drawArraysProvokingVertexImpl      at ContextMtl.mm:675
  #2  drawArraysImpl                     at ContextMtl.mm:462
  #3  drawArrays                         at ContextMtl.mm:514
  #5  GL_DrawArrays                      at entry_points_gles_2_0_autogen.cpp:1794
  #7  DoDrawArrays                       at gles2_cmd_decoder_passthrough_doers.cc:1185
  #12 ExecuteDeferredRequest             at gpu_channel.cc:798

```

Registers confirm this is the overflow draw (not the warmup):

```
  rcx = 0x55555558  (indexCount = 1431655768, attacker-controlled)
  r8  = 0x00000006  (GL_TRIANGLE_FAN)

```

Disassembly shows the 32-bit truncation:

```
  +336: addl  $-0x2, %eax            ; primCount = 1431655766 (0x55555556)
  +369: leal  (%rcx,%rcx,2), %r14d   ; primCount*3 = 0x100000002 TRUNCATED to 0x2
  +562: callq allocate               ; allocates 4 bytes (should be ~8 GB)

```

Apologies for the delay on this information; hopefully, it will assist in place of ASan output.

### ch...@google.com (2026-03-05)

geofflang: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### dx...@google.com (2026-03-30)

Project: angle/angle  

Branch:  main  

Author:  Geoff Lang [geofflang@chromium.org](mailto:geofflang@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7695152>

Metal: Protect against overflow in provoking vertex index count

---


Expand for full commit details
```
     
    Update the ProvokingVertexHelper methods to pass in index counts as 
    GLsizei which matches what the API gives us and return index counts in 
    uint32_t which is what is passed to Metal. 
     
    Do internal math in 64 bits and then validate the results fit in 32 
    bits. 
     
    Bug: chromium:484986863 
    Change-Id: I56553a3deddc98834645c0fab4129dbc65a830d6 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7695152 
    Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org> 
    Reviewed-by: Kimmo Kinnunen <kkinnunen@apple.com> 
    Commit-Queue: Geoff Lang <geofflang@chromium.org>

```

---

Files:

- M `src/libANGLE/renderer/metal/ContextMtl.mm`
- M `src/libANGLE/renderer/metal/ProvokingVertexHelper.h`
- M `src/libANGLE/renderer/metal/ProvokingVertexHelper.mm`
- M `src/tests/gl_tests/ProvokingVertexTest.cpp`

---

Hash: [52ba614db7e9df373eb33f2c431e47e657b173a9](https://chromiumdash.appspot.com/commit/52ba614db7e9df373eb33f2c431e47e657b173a9)  

Date: Mon Mar 23 21:10:53 2026


---

### dx...@google.com (2026-03-30)

Project: chromium/src  

Branch:  main  

Author:  chromium-autoroll [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com)  

Link:    <https://chromium-review.googlesource.com/7712148>

Roll ANGLE from b149a5c62d76 to bd3dbd7fda5a (3 revisions)

---


Expand for full commit details
```
     
    https://chromium.googlesource.com/angle/angle.git/+log/b149a5c62d76..bd3dbd7fda5a 
     
    2026-03-30 willho@google.com Implement operator!= for YcbcrConversionDesc 
    2026-03-30 syoussefi@chromium.org IR: Port CollectVariables 
    2026-03-30 geofflang@chromium.org Metal: Protect against overflow in provoking vertex index count 
     
    If this roll has caused a breakage, revert this CL and stop the roller 
    using the controls here: 
    https://autoroll.skia.org/r/angle-chromium-autoroll 
    Please CC angle-team@google.com,syoussefi@google.com on the revert to ensure that a human 
    is aware of the problem. 
     
    To file a bug in ANGLE: https://bugs.chromium.org/p/angleproject/issues/entry 
    To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry 
     
    To report a problem with the AutoRoller itself, please file a bug: 
    https://issues.skia.org/issues/new?component=1389291&template=1850622 
     
    Documentation for the AutoRoller is here: 
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md 
     
    Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:gpu-fyi-cq-mac-arm64;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86 
    Bug: chromium:484986863 
    Tbr: syoussefi@google.com 
    Test: Test: Build udc-kiwi-dev 
    Change-Id: I0fc4b11ababcc72a5ffe7f3ab613fbd0063bc3a0 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7712148 
    Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Cr-Commit-Position: refs/heads/main@{#1607428}

```

---

Files:

- M `DEPS`
- M `third_party/angle`

---

Hash: [fd5882f6cf4463361b5a41c41ce8772ae43e1078](https://chromiumdash.appspot.com/commit/fd5882f6cf4463361b5a41c41ce8772ae43e1078)  

Date: Mon Mar 30 23:31:31 2026


---

### sp...@google.com (2026-06-15)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $4000.00 for this report.

Rationale for this decision:
Baseline. Mildly mitigated sandbox renderer with bisect.


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-07-07)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/484986863)*
