# Heap buffer over-read in Mesa RadeonSI noop-blend analysis for scalar fragment outputs leads to GPU process memory disclosure

| Field | Value |
|-------|-------|
| **Issue ID** | [498828605](https://issues.chromium.org/issues/498828605) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>WebGL, Internals>GPU>ANGLE |
| **Platforms** | Linux, ChromeOS |
| **Reporter** | je...@gmail.com |
| **Assignee** | sy...@chromium.org |
| **Created** | 2026-04-02 |
| **Bounty** | $2,000.00 |

## Description

# Heap buffer over-read in Mesa RadeonSI noop-blend analysis for scalar fragment outputs leads to GPU process memory disclosure

## Summary

A heap buffer over-read exists in Mesa's RadeonSI driver during the noop-blend shader analysis, reachable from Chrome's GPU process via WebGL2 on Linux. When a fragment shader declares a scalar output (e.g. `out float`) and the blend state is `DST_COLOR * src + ZERO * dst`, the driver's `get_output_as_const_value` function unconditionally reads four `nir_const_value` elements from a `nir_load_const_instr` whose flexible array was allocated with only one element. This results in a 24-byte over-read on every first draw call with that shader and blend combination. The bug affects Linux systems running Mesa OpenGL drivers with RadeonSI (AMD GPUs).

Platform: Linux (Mesa OpenGL drivers, tested with radeonsi / AMD Radeon RX 6600 XT).

## Root Cause

RadeonSI implements a draw-time optimization for the blend mode `DST_COLOR * src + ZERO * dst`. When this blend state is active, the driver analyzes the fragment shader to determine whether it always outputs `vec4(1.0)` when fed an all-ones texture, which would make the blend a no-op. The analysis function `si_check_blend_dst_sampler_noop` clones the shader, replaces the sole texture fetch with a constant `vec4(1.0)`, runs constant folding, and then reads the resulting output value through `get_output_as_const_value`.

The problem is in `get_output_as_const_value`, which reads the constant output by hardcoding a 4-component access:

```
// src/gallium/drivers/radeonsi/si_nir_optim.c
nir_const_value *c = nir_src_as_const_value(intrin->src[0]);
if (!c)
   return false;

if (intrin->src[0].ssa->bit_size == 16) {
   uint16_t half_values[4];
   nir_const_value_to_array(half_values, c, 4, u16);
   for (unsigned i = 0; i < 4; i++)
      values[i] = _mesa_half_to_float(half_values[i]);
} else {
   nir_const_value_to_array(values, c, 4, f32);
}

```

The macro `nir_const_value_to_array` expands to a simple loop that accesses `c[0]` through `c[3]`:

```
// src/compiler/nir/nir.h
#define nir_const_value_to_array(arr, c, components, m) \
   do { for (unsigned i = 0; i < components; ++i) arr[i] = c[i].m; } while (false)

```

The pointer `c` comes from `nir_src_as_const_value`, which returns a pointer to the `value[]` flexible array member of `nir_load_const_instr`. This array is allocated with exactly `num_components` entries:

```
// src/compiler/nir/nir.c
nir_load_const_instr *
nir_load_const_instr_create(nir_shader *shader, unsigned num_components,
                            unsigned bit_size)
{
   nir_load_const_instr *instr =
      nir_instr_create(shader, nir_instr_type_load_const,
                       sizeof(nir_load_const_instr) + sizeof(nir_const_value) * num_components);

```

WebGL2 permits fragment shaders with scalar, vec2, or vec3 outputs such as `layout(location=0) out float o`. ANGLE's desktop GL backend preserves the declared type verbatim in the translated GLSL; it does not pad outputs to vec4. When such a shader's texture fetch is replaced with `vec4(1.0)` and constant-folded, the swizzle operation `.r` collapses the result to a single-component `nir_load_const_instr` with `num_components = 1`, meaning `value[]` has space for exactly one 8-byte `nir_const_value`. The subsequent call to `nir_const_value_to_array(values, c, 4, f32)` then reads three elements past the end of the allocation, a 24-byte over-read.

No ANGLE workaround covers this path; the existing Mesa-related workarounds (`recreateMipmapLevelsBeforeGenerate`, `disableRenderSnorm`, etc.) are unrelated.

## Reproduce

Tested at Chromium commit `ab3f3f8b586d6` on Linux x86\_64 with an AMD Radeon RX 6600 XT (radeonsi driver).

**The bug is confirmed present in Mesa 26.0.4 (latest stable as of 2026-04-02). The over-read object is a `nir_load_const_instr` allocated through Mesa's NIR GC slab allocator (`gc_alloc`). This allocator obtains 32 KB slabs from `malloc` and carves individual objects from within; ASAN only sees the outer slab boundary, not the boundaries between slab-internal objects, so the 24-byte over-read into adjacent slab data is invisible. To make it visible to ASAN, the slab is disabled by setting the compile-time constant `MAX_FREELIST_SIZE` to 0 in `src/util/ralloc.c`, which forces every `gc_alloc` to fall through to `ralloc_size` and thus to an individual `malloc` with its own ASAN redzone. This change affects only the allocation strategy; no application logic is modified, and the over-read occurs identically with or without the slab.**

### 0. Prerequisites

```
sudo apt-get build-dep mesa
pip install mako

```
### 1. Build libdrm (>= 2.4.121 required by Mesa 26.x)

```
git clone https://gitlab.freedesktop.org/mesa/drm.git /home/user/libdrm-new
cd /home/user/libdrm-new
git checkout libdrm-2.4.131

CC=~/chromium/src/third_party/llvm-build/Release+Asserts/bin/clang \
CXX=~/chromium/src/third_party/llvm-build/Release+Asserts/bin/clang++ \
meson setup build \
    --prefix=$PWD/install \
    -Dbuildtype=debug \
    -Db_sanitize=address \
    -Db_lundef=false

ninja -C build -j$(nproc) && ninja -C build install

```
### 2. Build Mesa with ASAN (slab allocator disabled)

Both Mesa and libdrm must be compiled with Chromium's Clang so the ASAN instrumentation resolves against the runtime statically linked into Chrome's ASAN binary. Using GCC's libasan.so will conflict at load time. The `-Db_lundef=false` flag is required because the shared libraries leave `__asan_*` symbols unresolved; they are provided by Chrome at runtime.

Mesa must be built as a release build (`-Dbuildtype=release -Db_ndebug=true`). Debug builds contain asserts in NIR that may abort before the overflow occurs.

Before building, apply the slab-disable patch to make the over-read visible to ASAN:

```
git clone https://gitlab.freedesktop.org/mesa/mesa.git /home/user/mesa-asan
cd /home/user/mesa-asan
git checkout mesa-26.0.4

# Disable the NIR GC slab allocator so each gc_alloc goes through malloc
sed -i 's/#define MAX_FREELIST_SIZE 512/#define MAX_FREELIST_SIZE 0/' src/util/ralloc.c

```

Then build:

```
PKG_CONFIG_PATH=/home/user/libdrm-new/install/lib/x86_64-linux-gnu/pkgconfig:$PKG_CONFIG_PATH \
CMAKE_PREFIX_PATH=/usr/lib/llvm-18 \
CC=~/chromium/src/third_party/llvm-build/Release+Asserts/bin/clang \
CXX=~/chromium/src/third_party/llvm-build/Release+Asserts/bin/clang++ \
meson setup build \
    --prefix=$PWD/install \
    -Dbuildtype=release \
    -Db_sanitize=address \
    -Db_lundef=false \
    -Db_ndebug=true \
    -Dglx=dri \
    -Degl=enabled \
    -Dplatforms=x11 \
    -Dllvm=enabled \
    -Dcpp_std=c++17 \
    -Dgallium-rusticl=false \
    -Dgallium-va=disabled \
    -Dcmake_prefix_path=/usr/lib/llvm-18

ninja -C build -j$(nproc) && ninja -C build install

```
### 3. Build Chrome with ASAN

```
cd ~/chromium/src
cat > out/asan-release/args.gn << 'EOF'
is_asan = true
is_debug = false
is_component_build = true
dcheck_always_on = false
EOF
gn gen out/asan-release
autoninja -C out/asan-release chrome

```
### 4. Run

```
MESA_SHADER_CACHE_DISABLE=true \
LD_LIBRARY_PATH=/home/user/mesa-asan/install/lib/x86_64-linux-gnu:/home/user/libdrm-new/install/lib/x86_64-linux-gnu:out/asan-release \
LIBGL_DRIVERS_PATH=/home/user/mesa-asan/install/lib/x86_64-linux-gnu/dri \
ASAN_OPTIONS="detect_leaks=0:halt_on_error=1:detect_odr_violation=0:redzone=128" \
out/asan-release/chrome \
    --no-sandbox \
    --disable-gpu-sandbox \
    --user-data-dir=/tmp/poc-$(date +%s) \
    "file:///path/to/poc.html"

```

The GPU process crashes within seconds of the page loading. ASAN reports:

```
==PID==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x7c4d3925a400
READ of size 4 at 0x7c4d3925a400 thread T44
SCARINESS: 24 (4-byte-read-heap-buffer-overflow)
    #0 in get_output_as_const_value si_nir_optim.c
    #1 in si_nir_is_output_const_if_tex_is_const si_nir_optim.c
    #2 in si_check_blend_dst_sampler_noop si_state.c
    #3 in si_draw_blend_dst_sampler_noop si_state.c
    #4 in tc_call_draw_single u_threaded_context.c
    ...

0x7c4d3925a400 is located 0 bytes after 128-byte region [0x7c4d3925a380,0x7c4d3925a400)
allocated by thread T44 here:
    #0 in malloc
    #1 in ralloc_size ralloc.c
    #2 in gc_alloc_size ralloc.c
    #3 in nir_load_const_instr_create nir.c
    #4 in nir_opt_constant_folding nir_opt_constant_folding.c
    #5 in si_nir_is_output_const_if_tex_is_const si_nir_optim.c
    #6 in si_check_blend_dst_sampler_noop si_state.c
    #7 in si_draw_blend_dst_sampler_noop si_state.c

```

The complete ASAN log is in `asan.log`.

### Standalone Mesa reproducer

The bug can also be reproduced without Chrome using the standalone C program `repro.c`. It uses GBM and EGL to create a headless OpenGL 3.2 core context on the hardware driver, compiles the same scalar-output fragment shader, sets the noop blend state, and issues a draw call. It requires the same ASAN-instrumented Mesa build with the slab allocator disabled (step 2 above).

```
cd /home/user/mesa-asan

# Compile the reproducer with the same Clang used for Mesa
~/chromium/src/third_party/llvm-build/Release+Asserts/bin/clang \
    -fsanitize=address -O1 -g \
    -o repro repro.c \
    -I install/include \
    -L install/lib/x86_64-linux-gnu \
    -L /home/user/libdrm-new/install/lib/x86_64-linux-gnu \
    -lEGL -lGL -lgbm \
    -Wl,-rpath,install/lib/x86_64-linux-gnu \
    -Wl,-rpath,/home/user/libdrm-new/install/lib/x86_64-linux-gnu

# Run
LD_LIBRARY_PATH=install/lib/x86_64-linux-gnu:/home/user/libdrm-new/install/lib/x86_64-linux-gnu \
LIBGL_DRIVERS_PATH=install/lib/x86_64-linux-gnu/dri \
MESA_SHADER_CACHE_DISABLE=true \
ASAN_OPTIONS="detect_leaks=0:detect_odr_violation=0" \
./repro /dev/dri/renderD128

```

ASAN reports the same `heap-buffer-overflow` in `get_output_as_const_value`.

## Suggested Fix

The fix is to read only `num_components` values from the flexible array instead of the hardcoded 4, and zero-initialize the remaining slots. The patch applies cleanly to Mesa 26.0.4:

```
--- a/src/gallium/drivers/radeonsi/si_nir_optim.c
+++ b/src/gallium/drivers/radeonsi/si_nir_optim.c
@@ -91,13 +91,15 @@ get_output_as_const_value(nir_shader *shader, float values[4])
                          !(nir_intrinsic_src_type(intrin) & nir_type_float))
                         return false;
 
+                     unsigned nc = intrin->src[0].ssa->num_components;
+                     memset(values, 0, 4 * sizeof(float));
                      if (intrin->src[0].ssa->bit_size == 16) {
-                        uint16_t half_values[4];
-                        nir_const_value_to_array(half_values, c, 4, u16);
-                        for (unsigned i = 0; i < 4; i++)
+                        uint16_t half_values[4] = {0};
+                        nir_const_value_to_array(half_values, c, nc, u16);
+                        for (unsigned i = 0; i < nc; i++)
                            values[i] = _mesa_half_to_float(half_values[i]);
                      } else {
-                        nir_const_value_to_array(values, c, 4, f32);
+                        nir_const_value_to_array(values, c, nc, f32);
                      }
                      return true;
                   }

```

With this patch applied, the reproducer completes without any ASAN report.

## Credit

Please use c6eed09fc8b174b0f3eebedcceb1e792 as the credit for this vulnerability. Thank you.

## Attachments

- [poc.html](attachments/poc.html) (text/html, 1.8 KB)
- [repro.c](attachments/repro.c) (text/x-csrc, 5.9 KB)
- [asan.log](attachments/asan.log) (text/plain, 9.3 KB)

## Timeline

### pe...@google.com (2026-04-02)

The issue's primary component must be in the Component Tags, so re-adding it. To change the primary component, use the edit button at the top of the issue, just above the title.

### ch...@google.com (2026-04-03)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-04-03)

Setting Priority to P0 to match Severity s0. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### je...@gmail.com (2026-04-03)

I don't think this should be s0; s1 is more appropriate.

### kb...@chromium.org (2026-04-03)

Thanks submitter for the detailed report and proposed Mesa patch. Have you reported this upstream against the Mesa project? Please do so if not, because the bug is ultimately in Mesa, even if it's reachable in WebGL 2 in Chrome.

Some things are unclear about your report. You claim that Mesa is optimizing the case where it's fed an all-ones texture, but the texture being fed in to the fragment shader in `poc.html` is an all-zeros texture - it's allocated without any contents, and is guaranteed by the WebGL implementation to be zeroed. It's not clear to me why the POC would reproduce the claimed bug. I don't have hardware on hand to reproduce it.

I wonder whether promoting all fragment shader outputs to a 4-vector of their type would work around the bug. I had a difficult time finding the OpenGL ES spec text defining compatibility between the fragment shader output and the format of the framebuffer attachment. The WebGL 2.0 spec covers this somewhat in <https://registry.khronos.org/webgl/specs/latest/2.0/#6.4> . The Stack Overflow discussion at <https://stackoverflow.com/questions/17943984/glsl-fragment-shader-output-type> discusses it as well. If more components are provided by the fragment shader than are present in the associated framebuffer attachment, the extra ones will be dropped on the floor. @sy...@chromium.org what do you think?

Regardless this bug seems to be medium severity per Chrome's security guidelines: <https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/severity-guidelines.md#TOC-Medium-severity> . "Medium severity (S2) bugs allow attackers to read or modify limited amounts of information." At most this is a 24-byte out-of-bounds read in the GPU process, not controllable in location.

@pr...@google.com does anyone on your team routinely commit to Mesa and if so do you think they could help with upstreaming this patch?

### je...@gmail.com (2026-04-04)

Thank you for the review.

Regarding the texture content question: the actual texture data is irrelevant to triggering the bug. The over-read occurs in the driver's *analysis* path, not during actual rendering. When `si_check_blend_dst_sampler_noop` detects the blend state `DST_COLOR * src + ZERO * dst`, it clones the fragment shader, unconditionally replaces all texture fetch instructions with a constant `vec4(1.0)` (regardless of what the real texture contains), runs constant folding, and then reads the folded output via `get_output_as_const_value`. The over-read happens in that last step — the scalar `.r` swizzle on `vec4(1.0)` folds to a 1-component `nir_load_const_instr`, but the function hardcodes a 4-component read. So the POC texture can be all-zeros, all-ones, or anything — only the blend state and the scalar output declaration matter.

Regarding upstream: I have not yet reported this to the Mesa project.

Regarding severity: I agree S2 (Medium) is reasonable. This is a 24-byte heap OOB read in the GPU process, not directly exploitable for code execution.

Regarding the vec4 promotion workaround: promoting fragment shader outputs to vec4 in ANGLE would indeed prevent this specific code path from over-reading, since the folded constant would then always have 4 components. That seems like a reasonable Chrome-side mitigation while the Mesa fix is upstreamed.

### kb...@chromium.org (2026-04-06)

@sy...@chromium.org would you please investigate adding a driver bug workaround to the shader translator, promoting ESSL 3.00 fragment outputs to 4-vectors on Mesa's RadeonSI driver?

### sy...@chromium.org (2026-04-08)

I couldn't find anything in the spec either. In particular, after expanding to vec4 I'm not sure if the alpha should be set to 0 or 1. It depends on how alpha-needing blend modes interpret alpha when that component doesn't exist. I'm asking Alexey to see if he has any insights. Writing the workaround should be trivial once I figure out what to output in the added channels.

### dx...@google.com (2026-05-01)

Project: angle/angle  

Branch:  main  

Author:  Shahbaz Youssefi [syoussefi@chromium.org](mailto:syoussefi@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7806928>

GL: Expand non-vec4 fragment outputs to vec4

---


Expand for full commit details
```
     
    As a workaround for driver bugs. 
     
    Bug: chromium:498828605 
    Change-Id: I88e2b33c807f92e8aa512bb99353f885b86d37c0 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7806928 
    Reviewed-by: Geoff Lang <geofflang@chromium.org> 
    Commit-Queue: Shahbaz Youssefi <syoussefi@chromium.org> 
    Reviewed-by: Kenneth Russell <kbr@chromium.org>

```

---

Files:

- M `include/GLSLANG/ShaderLang.h`
- M `include/platform/autogen/FeaturesGL_autogen.h`
- M `include/platform/gl_features.json`
- M `src/compiler.gni`
- M `src/compiler/translator/Compiler.cpp`
- M `src/compiler/translator/glsl/TranslatorESSL.cpp`
- M `src/compiler/translator/glsl/TranslatorGLSL.cpp`
- M `src/compiler/translator/tree_ops/MonomorphizeUnsupportedFunctions.cpp`
- A `src/compiler/translator/tree_ops/glsl/ExpandFragmentOutputsToVec4.cpp`
- A `src/compiler/translator/tree_ops/glsl/ExpandFragmentOutputsToVec4.h`
- M `src/compiler/translator/tree_util/IntermNode_util.cpp`
- M `src/compiler/translator/tree_util/IntermNode_util.h`
- M `src/libANGLE/renderer/gl/ShaderGL.cpp`
- M `src/libANGLE/renderer/gl/renderergl_utils.cpp`
- M `src/tests/gl_tests/GLSLTest.cpp`
- M `util/autogen/angle_features_autogen.cpp`
- M `util/autogen/angle_features_autogen.h`

---

Hash: [c1db297b2554ec7939f0234a3d53446f6a3c2ba7](https://chromiumdash.appspot.com/commit/c1db297b2554ec7939f0234a3d53446f6a3c2ba7)  

Date: Thu Apr 30 18:21:51 2026


---

### sy...@chromium.org (2026-05-01)

For future reference, the spec says that if the framebuffer is missing alpha, A\_d (alpha dst multiplier) is taken as 1. I noticed that the A\_s (alpha src multiplier) is correctly taken from the shader where declared. If the shader is not writing to a vec4 (i.e. alpha is not declared), I noticed some drivers use 0, some 1, and some replicate the value of an existing channel.

### dx...@google.com (2026-05-01)

Project: chromium/src  

Branch:  main  

Author:  [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com) [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com)  

Link:    <https://chromium-review.googlesource.com/7809140>

Roll ANGLE from 7b5b2509b037 to c1db297b2554 (5 revisions)

---


Expand for full commit details
```
     
    https://chromium.googlesource.com/angle/angle.git/+log/7b5b2509b037..c1db297b2554 
     
    2026-05-01 syoussefi@chromium.org GL: Expand non-vec4 fragment outputs to vec4 
    2026-05-01 geofflang@chromium.org GL: Use size_t for calculating lastRowOffset in TextureGL. 
    2026-05-01 lexa.knyazev@gmail.com Move writing ReadPixelsRobust output length to Context 
    2026-05-01 cclao@google.com Vulkan: Enable test coverage for ImagelessFramebuffer disabled 
    2026-05-01 alinakalyakina@google.com AHB: Allow R16UI and RG16UI formats 
     
    If this roll has caused a breakage, revert this CL and stop the roller 
    using the controls here: 
    https://autoroll.skia.org/r/angle-chromium-autoroll 
    Please CC angle-team@google.com,cnorthrop@google.com on the revert to ensure that a human 
    is aware of the problem. 
     
    To file a bug in ANGLE: https://bugs.chromium.org/p/angleproject/issues/entry 
    To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry 
     
    To report a problem with the AutoRoller itself, please file a bug: 
    https://issues.skia.org/issues/new?component=1389291&template=1850622 
     
    Documentation for the AutoRoller is here: 
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md 
     
    Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:gpu-fyi-cq-mac-arm64;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86 
    Bug: chromium:498828605 
    Tbr: cnorthrop@google.com 
    Test: Test: CtsNativeHardwareTestCases 
    Test: Test: angle_end2end_tests --gtest_filter=*BindExternalTextureAsImage*Vulkan 
    Change-Id: If5d17012be4849ccf5aeeeb5addf3aad45165151 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7809140 
    Commit-Queue: chromium-autoroll@skia-public.iam.gserviceaccount.com <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Bot-Commit: chromium-autoroll@skia-public.iam.gserviceaccount.com <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Cr-Commit-Position: refs/heads/main@{#1623993}

```

---

Files:

- M `DEPS`
- M `third_party/angle`

---

Hash: [361974ead51fefda03a493dd345c83011a9b4e8c](https://chromiumdash.appspot.com/commit/361974ead51fefda03a493dd345c83011a9b4e8c)  

Date: Fri May 1 19:28:17 2026


---

### sp...@google.com (2026-06-22)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
Baseline. User information disclosure.


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### eb...@google.com (2026-08-13)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/498828605)*
