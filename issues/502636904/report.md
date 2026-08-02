# Renderer-to-GPU sandbox escape via Skia SPIR-V injection

| Field | Value |
|-------|-------|
| **Issue ID** | [502636904](https://issues.chromium.org/issues/502636904) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | Internals>Skia |
| **Platforms** | Android, Fuchsia, Linux, ChromeOS |
| **Reporter** | qq...@calif.io |
| **Assignee** | mi...@google.com |
| **Created** | 2026-04-14 |
| **Bounty** | $25,000.00 |

## Description

## Summary

A compromised renderer sends a crafted glyph drawable through the
strike-cache IPC. The GPU process deserialises it into SkSL (finding 1:
missing `allowSkSL` check on `SkRuntimeImageFilter`), compiles it to
SPIR-V with a truncated instruction word-count (finding 2: 16-bit
overflow in `SPIRVCodeGenerator::writeOpCode`), and feeds the malformed module to
`vkCreateGraphicsPipelines`. The Vulkan driver (Mesa RADV) hits a
stack-buffer-overflow parsing the truncated `OpTypeStruct`. This is a
renderer-to-GPU sandbox escape on Vulkan-raster configurations
(Linux, Android, ChromeOS, and potentially Windows). ASAN-confirmed.

## Repro

This technically affects other GPUs as well but we only tested on AMDGPU. This should also affect Chrome Stable and older versions.

Requirements: Linux, AMD GPU (RDNA or later), Wayland session, clang,
meson, ninja, llvm. Tested on Arch with Mesa 26.0.4 source and
Chromium 148.0.7778.24 (rev 0f0efd8976ddaa54b04d945a440a5a9da3d8ccb9).

```
# Create build dir
mkdir -p out/asan
cat > out/asan/args.gn <<'EOF'
is_asan = true
is_debug = false
is_component_build = true
symbol_level = 1
dcheck_always_on = false
EOF
gn gen out/asan

# Apply the PoC patch to Skia and build
cd third_party/skia
git apply /tmp/renderer.patch # Change this to correct path
cd ../..
autoninja -C out/asan chrome

# Clone Mesa (if needed)
git clone https://gitlab.freedesktop.org/mesa/mesa.git
cd mesa
git checkout mesa-26.0.4   # or any recent release

# Configure - AMD Vulkan driver only, no Gallium
CC=clang CXX=clang++ meson setup build-asan \
  -Dvulkan-drivers=amd \
  -Dgallium-drivers= \
  -Dplatforms=wayland \
  -Db_sanitize=address \
  -Dbuildtype=debugoptimized \
  -Db_ndebug=true \
  -Db_lundef=false \
  -Dllvm=enabled

# Build only RADV
ninja -C build-asan \
  src/amd/vulkan/libvulkan_radeon.so \
  src/amd/vulkan/radeon_devenv_icd.x86_64.json


```
### Run

You may need to point VK\_ICD\_FILENAMES to the correct path

```
POC_GLYPH_SKSL=1 \
VK_ICD_FILENAMES=mesa/build-asan/src/amd/vulkan/radeon_devenv_icd.x86_64.json \
ASAN_OPTIONS="detect_leaks=0:detect_odr_violation=0" \
ASAN_SYMBOLIZER_PATH=/usr/bin/llvm-symbolizer \
RADV_DEBUG=nocache \
out/asan/chrome \
  --no-sandbox --disable-gpu-sandbox \
  --use-vulkan --enable-features=Vulkan \
  --enable-gpu-rasterization --enable-oop-rasterization \
  --allow-file-access-from-files --enable-logging=stderr \
  --user-data-dir=/tmp/poc --ozone-platform=wayland \
  --disable-in-process-stack-traces --disable-breakpad --disable-crash-reporter \
  --disable-gpu-watchdog \
  "file://$PWD/poc.html" 2>&1 | tee poc.log

```

---

See more root cause analysis in: [crbug/501471710](https://crbug.com/501471710) (reported by me). I reopened this bug with more concise information and patch with clearer IsRenderer guard. **If you fail to reproduce this, please let me know:**

- At what step your command failed? Please give me the command and diagnostic information
- Are you on AMDGPU?

## Attachments

- [asan.log](attachments/asan.log) (text/plain, 52.8 KB)
- [renderer.patch](attachments/renderer.patch) (text/x-diff, 5.4 KB)
- [poc.html](attachments/poc.html) (text/html, 29.9 KB)

## Timeline

### pe...@google.com (2026-04-20)

@qq...@calif.io Not all stack overflows are security issues.
They have to provably go past the guard pages on these OS.
If this cannot be proven then this will be simply converted to a bug.

Specific to AMD - mesa which is sandboxed on all platforms. s1 at most.

### qq...@calif.io (2026-04-20)

Hello, the stack buffer overflow is only symptom, confirming chrome allow malformed instruction to Mesa (or GPU driver in general, including Mali on Android potentially). Give me a few days, I think I can find better exploitable primitives there (I already found some but need to confirm them dynamically + build the demo)

### mi...@google.com (2026-04-20)

Raising severity to S0; the fact that this is able to inject arbitrary sksl via SkRuntimeImageFilter from the renderer process is significant in and of itself.

### qq...@calif.io (2026-04-20)

Moreover, to be clear, this is [stack-based buffer overflow](https://en.wikipedia.org/wiki/Stack_buffer_overflow) where stack smashing attack could happen not stack exhaustion (stack overflows). I am not claim RCE yet but I think this is clear memory corruption in GPU process.

---

EDIT: Thanks Michael for the clarification.

### mi...@google.com (2026-04-20)

Fix is <https://skia-review.git.corp.google.com/c/skia/+/1214636>

### jr...@google.com (2026-04-20)

[GPU security triage]

OS -> Android, Fuchsia, Linux, ChromeOS (feature owners please update if this is inaccurate).

### ch...@google.com (2026-04-21)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-04-21)

Setting Priority to P0 to match Severity s0. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### dx...@google.com (2026-04-21)

Project: skia  

Branch:  main  

Author:  Michael Ludwig [michaelludwig@google.com](mailto:michaelludwig@google.com)  

Link:    <https://skia-review.googlesource.com/1214636>

[sksl] Check allowSkSL for SkRuntimeImageFilter::CreateProc

---


Expand for full commit details
```
     
    Since SkRuntimeImageFilter doesn't create its runtime shaders until 
    actually evaluating the image filter, SkRuntimeShader's CreateProc 
    was not being reached; it must be responsible for validating allowSkSL. 
     
    Updates the unit test to confirm that all sources of runtime effects 
    in drawables are detected when allowSkSl is false. 
     
    Bug: b/502636904 
    Change-Id: I391ba2608010431429ac3e3c03e106f380304edb 
    Reviewed-on: https://skia-review.googlesource.com/c/skia/+/1214636 
    Reviewed-by: Kaylee Lubick <kjlubick@google.com> 
    Reviewed-by: Jorge Betancourt <jmbetancourt@google.com> 
    Commit-Queue: Michael Ludwig <michaelludwig@google.com>

```

---

Files:

- M `src/effects/imagefilters/SkRuntimeImageFilter.cpp`
- M `tests/SkGlyphTest.cpp`

---

Hash: 3150bddf3edd9ff7e9c3171a196cea2fb4d53a1f  

Date: Tue Apr 21 17:49:08 2026


---

### dx...@google.com (2026-04-22)

Project: skia  

Branch:  main  

Author:  Michael Ludwig [michaelludwig@google.com](mailto:michaelludwig@google.com)  

Link:    <https://skia-review.googlesource.com/1215396>

[sksl] Limit field count for structs

---


Expand for full commit details
```
     
    Limits structs to 1024 fields (should be sufficient) and adds a 
    check for overflowing the op code length packing in spirv generation. 
     
    Bug: b/502636904 
    Change-Id: Ia22f3ee1651d7bec9fe625efdc2ea7263e31f084 
    Reviewed-on: https://skia-review.googlesource.com/c/skia/+/1215396 
    Reviewed-by: Thomas Smith <thomsmit@google.com> 
    Commit-Queue: Thomas Smith <thomsmit@google.com> 
    Auto-Submit: Michael Ludwig <michaelludwig@google.com>

```

---

Files:

- M `src/sksl/codegen/SkSLSPIRVCodeGenerator.cpp`
- M `src/sksl/ir/SkSLType.cpp`
- M `tests/RasterPipelineCodeGeneratorTest.cpp`

---

Hash: 684457bb5dbadc1b8df3c9aa6ade714f5cf00d04  

Date: Tue Apr 21 18:26:33 2026


---

### dx...@google.com (2026-04-22)

Project: skia  

Branch:  main  

Author:  Michael Ludwig [michaelludwig@google.com](mailto:michaelludwig@google.com)  

Link:    <https://skia-review.googlesource.com/1216576>

Revert "[sksl] Limit field count for structs"

---


Expand for full commit details
```
     
    This reverts commit 684457bb5dbadc1b8df3c9aa6ade714f5cf00d04. 
     
    Reason for revert: breaking windows 11 in SkSLRasterPipelineSlotOverflow_355465305 
     
    Original change's description: 
    > [sksl] Limit field count for structs 
    > 
    > Limits structs to 1024 fields (should be sufficient) and adds a 
    > check for overflowing the op code length packing in spirv generation. 
    > 
    > Bug: b/502636904 
    > Change-Id: Ia22f3ee1651d7bec9fe625efdc2ea7263e31f084 
    > Reviewed-on: https://skia-review.googlesource.com/c/skia/+/1215396 
    > Reviewed-by: Thomas Smith <thomsmit@google.com> 
    > Commit-Queue: Thomas Smith <thomsmit@google.com> 
    > Auto-Submit: Michael Ludwig <michaelludwig@google.com> 
     
    Bug: b/502636904 
    No-Presubmit: true 
    No-Tree-Checks: true 
    No-Try: true 
    Change-Id: Icfeb65a749b09054fae3ad0909ccbfe1828541d5 
    Reviewed-on: https://skia-review.googlesource.com/c/skia/+/1216576 
    Commit-Queue: Michael Ludwig <michaelludwig@google.com> 
    Bot-Commit: rubber-stamper@appspot.gserviceaccount.com <rubber-stamper@appspot.gserviceaccount.com>

```

---

Files:

- M `src/sksl/codegen/SkSLSPIRVCodeGenerator.cpp`
- M `src/sksl/ir/SkSLType.cpp`
- M `tests/RasterPipelineCodeGeneratorTest.cpp`

---

Hash: a1b67bcdd645e85eee51a68f217c708cad78a853  

Date: Wed Apr 22 18:36:36 2026


---

### mi...@google.com (2026-04-22)

Note the above revert does not re-open this issue; the CL in #10 was the primary fix.

### sp...@google.com (2026-05-04)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $25000.00 for this report.

Rationale for this decision:
baseline memory corruption in gpu (android)


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### mi...@google.com (2026-05-08)

Added merge request to 148, not sure why it didn't auto create when fixed, sorry for the delay.

### ch...@google.com (2026-05-08)

**M148** merge request created. **Please update [crbug/511231535](https://crbug.com/511231535) to have this merge reviewed.**

### dx...@google.com (2026-05-08)

Project: skia  

Branch:  chrome/m148  

Author:  Michael Ludwig [michaelludwig@google.com](mailto:michaelludwig@google.com)  

Link:    <https://skia-review.googlesource.com/1230739>

[sksl] Check allowSkSL for SkRuntimeImageFilter::CreateProc

---


Expand for full commit details
```
     
    Since SkRuntimeImageFilter doesn't create its runtime shaders until 
    actually evaluating the image filter, SkRuntimeShader's CreateProc 
    was not being reached; it must be responsible for validating allowSkSL. 
     
    Updates the unit test to confirm that all sources of runtime effects 
    in drawables are detected when allowSkSl is false. 
     
    Bug: 502636904 
    Fixed: 511231535 
    Change-Id: I391ba2608010431429ac3e3c03e106f380304edb 
    Reviewed-on: https://skia-review.googlesource.com/c/skia/+/1214636 
    Reviewed-by: Kaylee Lubick <kjlubick@google.com> 
    Reviewed-by: Jorge Betancourt <jmbetancourt@google.com> 
    Commit-Queue: Michael Ludwig <michaelludwig@google.com> 
    (cherry picked from commit 3150bddf3edd9ff7e9c3171a196cea2fb4d53a1f) 
    Reviewed-on: https://skia-review.googlesource.com/c/skia/+/1230739 
    Auto-Submit: Michael Ludwig <michaelludwig@google.com> 
    Commit-Queue: Thomas Smith <thomsmit@google.com> 
    Reviewed-by: Thomas Smith <thomsmit@google.com>

```

---

Files:

- M `src/effects/imagefilters/SkRuntimeImageFilter.cpp`
- M `tests/SkGlyphTest.cpp`

---

Hash: a2888b27a98e4ff30085d4d2dba8a1a99baf6dfb  

Date: Tue Apr 21 17:49:08 2026


---

### pe...@google.com (2026-05-08)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### pe...@google.com (2026-05-11)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2026-05-11)

1. <https://skia-review.git.corp.google.com/c/skia/+/1231136>
2. Low - There was no conflict.
3. 148
4. Yes.

### dx...@google.com (2026-05-20)

Project: skia  

Branch:  chrome/m144  

Author:  Michael Ludwig [michaelludwig@google.com](mailto:michaelludwig@google.com)  

Link:    <https://skia-review.googlesource.com/1231136>

[M144-LTS][sksl] Check allowSkSL for SkRuntimeImageFilter::CreateProc

---


Expand for full commit details
```
     
    Since SkRuntimeImageFilter doesn't create its runtime shaders until 
    actually evaluating the image filter, SkRuntimeShader's CreateProc 
    was not being reached; it must be responsible for validating allowSkSL. 
     
    Updates the unit test to confirm that all sources of runtime effects 
    in drawables are detected when allowSkSl is false. 
     
    Bug: b/502636904 
    Change-Id: I391ba2608010431429ac3e3c03e106f380304edb 
    Reviewed-on: https://skia-review.googlesource.com/c/skia/+/1214636 
    Reviewed-by: Kaylee Lubick <kjlubick@google.com> 
    Reviewed-by: Jorge Betancourt <jmbetancourt@google.com> 
    Commit-Queue: Michael Ludwig <michaelludwig@google.com> 
    (cherry picked from commit 3150bddf3edd9ff7e9c3171a196cea2fb4d53a1f) 
    Reviewed-on: https://skia-review.googlesource.com/c/skia/+/1231136 
    Reviewed-by: Michael Ludwig <michaelludwig@google.com>

```

---

Files:

- M `src/effects/imagefilters/SkRuntimeImageFilter.cpp`
- M `tests/SkGlyphTest.cpp`

---

Hash: 7c565113f37b25491d97c6f19e7fa8cfef8b260e  

Date: Tue Apr 21 17:49:08 2026


---

### ch...@google.com (2026-07-30)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/502636904)*
