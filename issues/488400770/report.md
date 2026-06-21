# Security: Cross-tab GPU memory exfiltration via uint64 to uint32 truncation in Dawn's Metal vertex buffer length tracking

| Field | Value |
|-------|-------|
| **Issue ID** | [488400770](https://issues.chromium.org/issues/488400770) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Dawn>Native |
| **Platforms** | Mac |
| **Reporter** | sw...@gmail.com |
| **Assignee** | ka...@google.com |
| **Created** | 2026-02-27 |
| **Bounty** | $5,000.00 |

## Description

---

### Report description

Security: Cross-tab GPU memory exfiltration via uint64 to uint32 truncation in Dawn's Metal vertex buffer length tracking

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

---

### The problem

#### Please describe the technical details of the vulnerability

## Summary

A `uint64_t` to `uint32_t` truncation in Dawn's Metal backend (`CommandBufferMTL.mm:924`) causes vertex buffer sizes ≥ 4GB to be recorded as 0. This effectively disables the Tint robustness clamp for vertex buffer accesses (`arrayLength() = 0` → `min(idx, 0 - 1)` = no-op). Combined with `drawIndirect()` to bypass CPU-side firstVertex validation, this allows GPU out-of-bounds reads past the buffer boundary. Apple Silicon GPUs lack hardware buffer robustness, so OOB reads return actual adjacent GPU memory. Cross-tab data exfiltration confirmed on M4 Pro.

## Affected Version

- **Component**: Dawn / WebGPU (Metal backend)
- **Tested on**: Chrome stable, macOS (Apple M4 Pro)
- **Other affected**: Chrome Canary, Chromium (any version with Metal WebGPU backend)
- **Platform**: macOS with Apple Silicon (M1/M2/M3/M4)

## Root Cause

### The truncation

In `src/dawn/native/metal/CommandBufferMTL.mm`, vertex buffer binding sizes are stored as `uint32_t`. When `GetAllocatedSize() - offset ≥ 0x100000000`, the `static_cast<uint32_t>()` silently truncates the value:

```
// Line 923: DEBUG-ONLY assert — checks the WRONG VALUE
DAWN_ASSERT(buffer->GetSize() < std::numeric_limits<uint32_t>::max());
//           ^^^^^^^^^^^^^^^^ Checks GetSize() (user-requested), not GetAllocatedSize()!

// Line 924-925: Silent uint64→uint32 truncation
mVertexBufferBindingSizes[slot] =
    static_cast<uint32_t>(buffer->GetAllocatedSize() - offset);
//  ^^^^^^^^^^^^^^^^^^^^^^ GetAllocatedSize() = 0x100000000 → truncates to 0

```
### Optimal trigger: `size = 0xFFFFFFFC` (4GB - 4)

The size `0xFFFFFFFC` is optimal because it also **bypasses the debug-only DAWN\_ASSERT** on line 923:

1. `GetSize() = 0xFFFFFFFC` — user-requested buffer size
2. `extraBytes = 4` — Metal adds extra bytes for vertex buffers (`BufferMTL.mm:96`)
3. `currentSize = max(0xFFFFFFFC + 4, 4) = 0x100000000`
4. `Align(0x100000000, 4) = 0x100000000` (alignment=4 on macOS for fillBuffer)
5. `mAllocatedSize = 0x100000000` (exactly 4GB)
6. Line 923: `DAWN_ASSERT(0xFFFFFFFC < 0xFFFFFFFF)` → **TRUE** — assert passes even in debug!
7. Line 924: `static_cast<uint32_t>(0x100000000 - 0) = 0` — **truncated to zero**

### Robustness bypass chain

The truncated value of 0 propagates through:

```
mVertexBufferBindingSizes[slot] = 0
  → StorageBufferLengthTracker::data[Vertex][metalIndex] = 0    (line 946-947)
  → MSL shader: tint_storage_buffer_sizes[N].x = 0
  → arrayLength() = 0
  → Robustness clamp: min(idx, arrayLength() - 1)
                     = min(idx, 0 - 1)
                     = min(idx, 0xFFFFFFFF)      ← u32 underflow
                     = idx                        ← NO CLAMPING

```

The vertex pulling transform (`vertex_pulling.cc:222`) creates the buffer as `var<storage, read>`, and the robustness transform (`robustness.cc:310-312`) computes `arrayLength() - 1` without guarding against zero.

### Debug assert is doubly wrong

The DAWN\_ASSERT on line 923 has two independent bugs:

1. **Checks the wrong value**: It checks `GetSize()` (user-requested), but the truncation is on `GetAllocatedSize()` (which includes alignment + extra bytes)
2. **Uses wrong comparison**: `GetSize() = 0xFFFFFFFC < UINT32_MAX = 0xFFFFFFFF` is TRUE, so the assert passes even when `GetAllocatedSize() = 0x100000000` overflows uint32

The bug is invisible in debug builds.

## Proof of Concept

### Attack overview

The exploit uses two HTML files:

1. **`victim.html`** — Opened in a separate tab, sprays GPU memory with 512MB of identifiable marker patterns (`0xD1_XX_XX_XX`)
2. **`exploit_cross_tab_s4_imageSuccess.html`** — Creates a 4GB-4 vertex buffer (triggering the truncation), then uses `drawIndirect()` to read GPU memory beyond the buffer boundary

### bypass size validation using `drawIndirect()` instead of draw()

A direct `draw(N, 1, OOB_FIRST_VERTEX, 0)` call is rejected by Dawn's CPU-side validation (`CommandBufferStateTracker.cpp:399-437`), which checks `(firstVertex + vertexCount - 1) * arrayStride + lastStride` against the bound buffer size. However, `drawIndirect()` puts `firstVertex` in a GPU buffer — the CPU cannot inspect it:

```
// CPU validation CANNOT see firstVertex in an indirect buffer
const params = new Uint32Array([
    256,              // vertexCount
    1,                // instanceCount
    OOB_FIRST_VERTEX, // firstVertex — CPU can't validate this!
    0,                // firstInstance
]);
device.queue.writeBuffer(indirectBuffer, 0, params);
pass.drawIndirect(indirectBuffer, 0);

```

The GPU's indirect draw validation shader does not check vertex buffer bounds — it only validates draw parameter consistency. The vertex pulling shader reads from the buffer using `arrayLength=0` → no robustness clamping → OOB read.

### Data exfiltration chain

```
GPU OOB read (vertex buffer[firstVertex + vid])
  → vertex shader: v.data = OOB u32 value
  → fragment shader: encode as RGBA color
  → color attachment texture
  → copyTextureToBuffer
  → mapAsync(MAP_READ)
  → CPU JavaScript receives leaked data

```

Each `drawIndirect()` call reads 256 u32 values from GPU memory past the buffer boundary. The attacker controls the offset via `firstVertex`.

### Minimal reproduction

```
// 1. Create 4GB-4 vertex buffer (triggers truncation)
const victimBuffer = device.createBuffer({
    size: 0xFFFFFFFC,
    usage: GPUBufferUsage.VERTEX | GPUBufferUsage.COPY_DST,
});

// 2. Metal internally: allocatedSize = 0x100000000
//    mVertexBufferBindingSizes[0] = (uint32_t)(0x100000000) = 0
//    arrayLength() = 0 → robustness clamp = min(idx, 0xFFFFFFFF)

// 3. Vertex shader reads @location(0) data: u32 from vertex buffer
//    Vertex pulling loads buffer[firstVertex + vid] with NO clamping

// 4. drawIndirect bypasses CPU vertex range validation
const indirectParams = new Uint32Array([
    256,                      // vertexCount
    1,                        // instanceCount
    0x3FFFFFFF + 0x1000000,   // firstVertex: 16MB past buffer end
    0,                        // firstInstance
]);
device.queue.writeBuffer(indirectBuffer, 0, indirectParams);

pass.setVertexBuffer(0, victimBuffer);
pass.drawIndirect(indirectBuffer, 0);

```
## Suggested Fix

### Option 1: Widen the storage type (comprehensive fix)

Change `StorageBufferLengthTracker::data` and `mVertexBufferBindingSizes` from `uint32_t` to `uint64_t`. Update the Tint MSL writer to emit 64-bit buffer sizes. This prevents truncation for any buffer size.

### Option 2: Clamp to UINT32\_MAX (minimal fix)

```
// Replace line 924-925:
uint64_t size64 = buffer->GetAllocatedSize() - offset;
mVertexBufferBindingSizes[slot] = static_cast<uint32_t>(
    std::min(size64, static_cast<uint64_t>(std::numeric_limits<uint32_t>::max())));

```
### Option 3: Validation reject

Add explicit validation in `setVertexBuffer` to reject buffers where `allocatedSize - offset > UINT32_MAX`:

```
DAWN_INVALID_IF(buffer->GetAllocatedSize() - offset > std::numeric_limits<uint32_t>::max(),
    "Vertex buffer allocated size minus offset exceeds uint32 maximum.");

```
### Also fix the assert

Regardless of which fix is chosen, the DAWN\_ASSERT on line 923 should be corrected:

```
// Fix: check GetAllocatedSize(), not GetSize()
DAWN_ASSERT(buffer->GetAllocatedSize() - offset <= std::numeric_limits<uint32_t>::max());

```
## Reproduction Steps

1. **Environment**: macOS with Apple Silicon (M1/M2/M3/M4), Chrome stable (no flags)
2. Open `victim.html` in one Chrome tab → click "Spray 512MB" → wait for completion
3. Open `exploit_cross_tab_s4_imageSuccess.html` in another Chrome tab (same Chrome window = same GPU process)
4. Click "1. Self-Test" to verify the pipeline works (should show 256/256 matching in-bounds reads)
5. Click "2. Cross-Tab Exploit" to scan 512MB past the 4GB buffer boundary
6. Alternatively, click "5. Auto-Hunt" for automated retry with VA layout jittering

**Expected outcome**: The exploit detects victim buffer signatures (`0xD1_XX_XX_XX`) in the OOB scan. May require multiple attempts due to GPU VA layout variation.

## Version Information

- **Chrome**: Stable channel (145.0.7632.117)
- **OS**: macOS, Apple M4 Pro
- **Memory**: 24GB unified (4GB GPU allocation succeeds)

#### Impact analysis

# Cross-tab / cross-origin GPU memory disclosure

Chrome's GPU process is shared across all tabs. All WebGPU contexts on the same GPU device share the same GPU virtual address space. By reading past the 4GB buffer boundary, the attacker can access:

- **Other tabs' WebGPU buffer contents**
- **Compositor framebuffer pixels**
- **GPU virtual address metadata**

This is cross-origin information disclosure without any user interaction.

---

### The cause

#### What version of Chrome have you found the security issue in?

145.0.7632.117 stable

#### Is the security issue related to a crash?

No, it is not related to a crash.

#### Choose the type of vulnerability

Information Leak

#### How would you like to be publicly acknowledged for your report?

sweetchip

## Attachments

- [cross-tab-poc-result2.png](attachments/cross-tab-poc-result2.png) (image/png, 379.0 KB)
- [cross-tab-poc-result1.png](attachments/cross-tab-poc-result1.png) (image/png, 2.7 MB)
- [exploit_cross_tab_s4_imageSuccess.html](attachments/exploit_cross_tab_s4_imageSuccess.html) (text/html, 74.2 KB)
- [poc_minimized.html](attachments/poc_minimized.html) (text/html, 6.4 KB)
- [victim.html](attachments/victim.html) (text/html, 20.0 KB)

## Timeline

### li...@chromium.org (2026-02-27)

I was unable to reproduce. Did you mean to attach `victim.html`?

### sw...@gmail.com (2026-02-28)

Sorry, I forgot to attach the file. I've uploaded victim.html now.

### pe...@google.com (2026-02-28)

Thank you for providing more feedback. Adding the requester to the CC list.

### pe...@google.com (2026-03-02)

The NextAction date has arrived: 2026-03-02
To opt-out from this automation rule, please add Optout-Blintz-Nextaction-Alert to the "Chromium Labels" custom field.

### me...@google.com (2026-03-04)

Assigning provisional severity and foundin labels. kainino@, could you please double check? Thanks.

### ka...@chromium.org (2026-03-04)

I haven't been able to repro the data leak in `147.0.7717.0 (Official Build) canary (arm64)` on M1 Pro, though I don't see any reason it shouldn't repro.

### ka...@chromium.org (2026-03-04)

Guessing this is a non-regression and it's been in the wild since WebGPU shipped in Chromium 113.

### ka...@chromium.org (2026-03-05)

> I haven't been able to repro

Never mind, I was just holding it wrong. It does repro as expected.

### ka...@chromium.org (2026-03-05)

Severity looks correct based on <https://chromium.googlesource.com/chromium/src/+/lkgr/docs/security/severity-guidelines.md>. I consider this P0 for our team.

### ch...@google.com (2026-03-05)

Setting milestone because of s0/s1 severity.

### dx...@google.com (2026-03-09)

Project: dawn  

Branch:  main  

Author:  Kai Ninomiya [kainino@chromium.org](mailto:kainino@chromium.org)  

Link:    <https://dawn-review.googlesource.com/295255>

[dawn][metal] Fix robustness issues around buffer lengths being u32

---


Expand for full commit details
```
     
    On Metal, the sizes of storage buffers (and vertex buffers when 
    transformed into storage buffers for vertex pulling for robustness) are 
    passed to MSL in an array of u32 values. Thus, such bindings cannot be 
    larger than 4GiB-1. 
     
    There is no separate limit on vertex buffer binding size (as there is 
    for storage buffer bindings), so in order to make this safe - without 
    significantly changing how buffer sizes are passed - this also reduces 
    maxBufferSize by 4 bytes to 4GiB-4. This should have minimal impact on 
    apps, but in order to raise it back to 4GiB we can either: 
    - Pass buffer size minus one (i.e. the max byte index value) into the 
      shader so the minus-one step doesn't have to happen inside the shader 
    - Or just pass sizes as u64. 
     
    The tests are verified to fail without the fix, with the exception of 
    VertexBuffer_ZeroSizeRemaining which exists to help test later when we 
    raise the limit again. 
     
    Test: MetalBufferRobustnessTest.* 
    Fixed: 488400770 
    Change-Id: I3b4207b63ba641271b098a964734f70446595814 
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/295255 
    Reviewed-by: Loko Kung <lokokung@google.com> 
    Commit-Queue: Kai Ninomiya <kainino@chromium.org> 
    Reviewed-by: Corentin Wallez <cwallez@chromium.org>

```

---

Files:

- M `src/dawn/native/Limits.cpp`
- M `src/dawn/native/metal/BufferMTL.mm`
- M `src/dawn/native/metal/CommandBufferMTL.mm`
- M `src/dawn/native/metal/PhysicalDeviceMTL.mm`
- M `src/dawn/tests/BUILD.gn`
- M `src/dawn/tests/CMakeLists.txt`
- M `src/dawn/tests/end2end/ArchTierLimitsExhaustive.cpp`
- A `src/dawn/tests/end2end/BufferRobustnessTests.cpp`
- M `src/tint/lang/core/ir/transform/robustness.cc`

---

Hash: 12f4bc468e7a724285bfc9aac2e4fc3f2162c423  

Date: Mon Mar 9 21:53:56 2026


---

### ch...@google.com (2026-03-10)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M145. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M146. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [145, 146].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### ka...@chromium.org (2026-03-10)

1. <https://dawn-review.googlesource.com/295255>
2. Not yet released in Canary <https://chromiumdash.appspot.com/commit/12f4bc468e7a724285bfc9aac2e4fc3f2162c423>
3. Not a trivial change so yes, but I think low risk.
4. Risk of a very small number of websites no longer being able to use WebGPU on high-end devices, due to reduction of maxBufferSize from 4GiB to 4GiB-4. This would only happen if they're requiring exactly 4GiB, which already would have prevented them from running on a lot of systems.
5. No.
6. Done.

### ch...@google.com (2026-03-11)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M146. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to dev. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M147. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [146, 147].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### ka...@chromium.org (2026-03-11)

Oops, this is blocked on a Dawn->Chromium roll. Will check in with gardener about it.

### ka...@chromium.org (2026-03-11)

Roll should resume once this unrelated revert lands. <https://dawn-review.googlesource.com/c/dawn/+/296615>

### ka...@chromium.org (2026-03-12)

Patch now released in Canary 148.0.7731.0.

### dr...@chromium.org (2026-03-15)

No crashes in Canary. Merge approved to M146 and M147.

### dx...@google.com (2026-03-17)

Project: dawn  

Branch:  chromium/7727  

Author:  Kai Ninomiya [kainino@chromium.org](mailto:kainino@chromium.org)  

Link:    <https://dawn-review.googlesource.com/297515>

[M147] [dawn][metal] Fix robustness issues around buffer lengths being u32

---


Expand for full commit details
```
     
    On Metal, the sizes of storage buffers (and vertex buffers when 
    transformed into storage buffers for vertex pulling for robustness) are 
    passed to MSL in an array of u32 values. Thus, such bindings cannot be 
    larger than 4GiB-1. 
     
    There is no separate limit on vertex buffer binding size (as there is 
    for storage buffer bindings), so in order to make this safe - without 
    significantly changing how buffer sizes are passed - this also reduces 
    maxBufferSize by 4 bytes to 4GiB-4. This should have minimal impact on 
    apps, but in order to raise it back to 4GiB we can either: 
    - Pass buffer size minus one (i.e. the max byte index value) into the 
      shader so the minus-one step doesn't have to happen inside the shader 
    - Or just pass sizes as u64. 
     
    The tests are verified to fail without the fix, with the exception of 
    VertexBuffer_ZeroSizeRemaining which exists to help test later when we 
    raise the limit again. 
     
    No-Try: true 
    Test: MetalBufferRobustnessTest.* 
    Fixed: 488400770 
    Change-Id: I3b4207b63ba641271b098a964734f70446595814 
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/295255 
    Reviewed-by: Loko Kung <lokokung@google.com> 
    Commit-Queue: Kai Ninomiya <kainino@chromium.org> 
    Reviewed-by: Corentin Wallez <cwallez@chromium.org> 
    (cherry picked from commit 12f4bc468e7a724285bfc9aac2e4fc3f2162c423) 
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/297515 
    Bot-Commit: rubber-stamper@appspot.gserviceaccount.com <rubber-stamper@appspot.gserviceaccount.com>

```

---

Files:

- M `src/dawn/native/Limits.cpp`
- M `src/dawn/native/metal/BufferMTL.mm`
- M `src/dawn/native/metal/CommandBufferMTL.mm`
- M `src/dawn/native/metal/PhysicalDeviceMTL.mm`
- M `src/dawn/tests/BUILD.gn`
- M `src/dawn/tests/CMakeLists.txt`
- M `src/dawn/tests/end2end/ArchTierLimitsExhaustive.cpp`
- A `src/dawn/tests/end2end/BufferRobustnessTests.cpp`
- M `src/tint/lang/core/ir/transform/robustness.cc`

---

Hash: 34a55c2d3c5e423a6fe0ef28abffa7c7602e75ec  

Date: Tue Mar 17 03:14:48 2026


---

### dx...@google.com (2026-03-17)

Project: dawn  

Branch:  chromium/7680  

Author:  Kai Ninomiya [kainino@chromium.org](mailto:kainino@chromium.org)  

Link:    <https://dawn-review.googlesource.com/297495>

[M146] [dawn][metal] Fix robustness issues around buffer lengths being u32

---


Expand for full commit details
```
     
    On Metal, the sizes of storage buffers (and vertex buffers when 
    transformed into storage buffers for vertex pulling for robustness) are 
    passed to MSL in an array of u32 values. Thus, such bindings cannot be 
    larger than 4GiB-1. 
     
    There is no separate limit on vertex buffer binding size (as there is 
    for storage buffer bindings), so in order to make this safe - without 
    significantly changing how buffer sizes are passed - this also reduces 
    maxBufferSize by 4 bytes to 4GiB-4. This should have minimal impact on 
    apps, but in order to raise it back to 4GiB we can either: 
    - Pass buffer size minus one (i.e. the max byte index value) into the 
      shader so the minus-one step doesn't have to happen inside the shader 
    - Or just pass sizes as u64. 
     
    The tests are verified to fail without the fix, with the exception of 
    VertexBuffer_ZeroSizeRemaining which exists to help test later when we 
    raise the limit again. 
     
    No-Try: true 
    Test: MetalBufferRobustnessTest.* 
    Fixed: 488400770 
    Change-Id: I3b4207b63ba641271b098a964734f70446595814 
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/295255 
    Reviewed-by: Loko Kung <lokokung@google.com> 
    Commit-Queue: Kai Ninomiya <kainino@chromium.org> 
    Reviewed-by: Corentin Wallez <cwallez@chromium.org> 
    (cherry picked from commit 12f4bc468e7a724285bfc9aac2e4fc3f2162c423) 
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/297495 
    Commit-Queue: Srinivas Sista <srinivassista@google.com> 
    Auto-Submit: Kai Ninomiya <kainino@chromium.org>

```

---

Files:

- M `src/dawn/native/Limits.cpp`
- M `src/dawn/native/metal/BufferMTL.mm`
- M `src/dawn/native/metal/CommandBufferMTL.mm`
- M `src/dawn/native/metal/PhysicalDeviceMTL.mm`
- M `src/dawn/tests/BUILD.gn`
- M `src/dawn/tests/end2end/ArchTierLimitsExhaustive.cpp`
- A `src/dawn/tests/end2end/BufferRobustnessTests.cpp`
- M `src/tint/lang/core/ir/transform/robustness.cc`

---

Hash: 3d52cfc8dd0bc2cdbbecd9803cc08102de7e4597  

Date: Tue Mar 17 16:37:11 2026


---

### sp...@google.com (2026-03-31)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
Baseline. User information disclosure


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### sw...@gmail.com (2026-04-01)

Hello, Chrome VRP team!

Thank you for handling issue #488400770.

I’d like to understand the reward decision better.

The bug was classified as S1(High) severity, but the reward was set at the User Information Leak baseline.

Could you help clarify what factors led to the baseline rate being applied in this case?

For context, visiting a crafted page can leak pixel data from a cross-origin tab via GPU memory OOB read. The PoC (attached to the issue) demonstrates visually recognizable cross-origin image reconstruction.

I’d appreciate any clarification on the criteria used.

Thank you!

### ka...@chromium.org (2026-04-01)

> The PoC (attached to the issue) demonstrates visually recognizable cross-origin image reconstruction.

Just a note for VRP in case it's useful: this is accurate, I was able to reproduce and verify it.

### aj...@google.com (2026-04-21)

-> panel for reassessment, see comments 23 and 24

### sp...@google.com (2026-05-04)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $3000.00 for this report.

Rationale for this decision:
Moderate impact UAF. Sorry we missed this first time!


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-06-16)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/488400770)*
