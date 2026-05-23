# [bugSWAT] GPU process crash via WebGPU shader - wild-deref in Mesa aco::combine_instruction

| Field | Value |
|-------|-------|
| **Issue ID** | [448294721](https://issues.chromium.org/issues/448294721) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebGPU |
| **Platforms** | Fuchsia, Linux, Windows, ChromeOS |
| **Reporter** | a7...@gmail.com |
| **Assignee** | pe...@google.com |
| **Created** | 2025-09-30 |
| **Bounty** | $10,000.00 |

## Description

#### VULNERABILITY DETAILS

This report is about a heap-use-after-free in the Mesa shader compiler, reachable via WebGPU shaders emitted by dawn/tint. The offending shader looks as follows:

```
enable subgroups;

@group(0) @binding(0) 
var<storage, read_write> g: f32;

@fragment
fn frag_main() -> @location(0) vec4<f32> {
    g = tanh(subgroupMin(-g));
    return vec4<f32>();
}

```

The standalone reproducer crashs in the vendor-specific file amd/compiler/aco\_optimizer.cpp + I never found a similar-looking crash on Intel devices so its probably only affecting AMD.

#### VERSION

Chrome Version: Version 141.0.7353.0 (Developer Build) (64-bit) (ASAN build)   

Operating System: Ubuntu 25.04   

Mesa: mesa-25.2.3 commit 62f9be9

#### REPRODUCTION

There are two means of reproduction, standalone and via Chrome. The instructions below use an ASAN build of Chrome and an ASAN build of Mesa. Precise build instructions for Mesa depend on the distro, a complete example for Ubuntu is part of the Dockerfile file of the standalone reproducer.

##### Standalone

1. Place the Dockerfile and the .gfxr in a new directory
2. Inside this directory: `docker build -t mesarepo .`
3. Once built, switch into the container: `docker run -it mesarepo /bin/bash`
4. Inside the container, run: `LD_PRELOAD="/usr/lib/llvm-20/lib/clang/20/lib/linux/libclang_rt.asan-x86_64.so /mesa/buildASAN/src/amd/drm-shim/libamdgpu_noop_drm_shim.so" VK_DRIVER_FILES=/mesa/buildASAN/src/amd/vulkan/radeon_icd.x86_64.json /gfxreconstruct/build/tools/replay/gfxrecon-replay /gfxrecon.gfxr`

This should produce the following ASAN report:

```
AddressSanitizer:DEADLYSIGNAL
=================================================================
==18==ERROR: AddressSanitizer: SEGV on unknown address 0x6f731bde2ba0 (pc 0x6ef31762a73b bp 0x7ffc932e4a90 sp 0x7ffc932e4940 T0)
==18==The signal is caused by a READ memory access.
    #0 0x6ef31762a73b in aco::(anonymous namespace)::combine_instruction(aco::(anonymous namespace)::opt_ctx&, std::unique_ptr<aco::Instruction, aco::instr_deleter_functor>&) /mesa/buildASAN/../src/amd/compiler/aco_optimizer.cpp:3800:46
    #1 0x6ef3176091ca in aco::optimize(aco::Program*) /mesa/buildASAN/../src/amd/compiler/aco_optimizer.cpp:5086:10
    #2 0x6ef3174cc63c in (anonymous namespace)::aco_postprocess_shader[abi:cxx11](aco_compiler_options const*, std::unique_ptr<aco::Program, std::default_delete<aco::Program>>&) /mesa/buildASAN/../src/amd/compiler/aco_interface.cpp:89:10
    #3 0x6ef3174cbc32 in aco_compile_shader /mesa/buildASAN/../src/amd/compiler/aco_interface.cpp:245:26
    #4 0x6ef316a88131 in shader_compile /mesa/buildASAN/../src/amd/vulkan/radv_shader.c:3120:7
    #5 0x6ef316a88131 in radv_shader_nir_to_asm /mesa/buildASAN/../src/amd/vulkan/radv_shader.c:3151:7
    #6 0x6ef316a2df53 in radv_graphics_shaders_nir_to_asm /mesa/buildASAN/../src/amd/vulkan/radv_pipeline_graphics.c:2380:21
    #7 0x6ef316a2df53 in radv_graphics_shaders_compile /mesa/buildASAN/../src/amd/vulkan/radv_pipeline_graphics.c:2808:4
    #8 0x6ef316a3f8a9 in radv_graphics_pipeline_compile /mesa/buildASAN/../src/amd/vulkan/radv_pipeline_graphics.c:3057:4
    #9 0x6ef316a35f03 in radv_graphics_pipeline_init /mesa/buildASAN/../src/amd/vulkan/radv_pipeline_graphics.c:3453:13
    #10 0x6ef316a35f03 in radv_graphics_pipeline_create /mesa/buildASAN/../src/amd/vulkan/radv_pipeline_graphics.c:3514:13
    #11 0x6ef316a35f03 in radv_CreateGraphicsPipelines /mesa/buildASAN/../src/amd/vulkan/radv_pipeline_graphics.c:3669:14
    #12 0x56db1d817769 in gfxrecon::decode::VulkanReplayConsumerBase::OverrideCreateGraphicsPipelines(VkResult (*)(VkDevice_T*, VkPipelineCache_T*, unsigned int, VkGraphicsPipelineCreateInfo const*, VkAllocationCallbacks const*, VkPipeline_T**), VkResult, gfxrecon::decode::VulkanDeviceInfo const*, gfxrecon::decode::VulkanPipelineCacheInfo const*, unsigned int, gfxrecon::decode::StructPointerDecoder<gfxrecon::decode::Decoded_VkGraphicsPipelineCreateInfo> const*, gfxrecon::decode::StructPointerDecoder<gfxrecon::decode::Decoded_VkAllocationCallbacks> const*, gfxrecon::decode::HandlePointerDecoder<VkPipeline_T*>*) /gfxreconstruct/framework/decode/vulkan_replay_consumer_base.cpp:11229:34
    #13 0x56db1de1d702 in gfxrecon::decode::VulkanReplayConsumer::Process_vkCreateGraphicsPipelines(gfxrecon::decode::ApiCallInfo const&, VkResult, unsigned long, unsigned long, unsigned int, gfxrecon::decode::StructPointerDecoder<gfxrecon::decode::Decoded_VkGraphicsPipelineCreateInfo>*, gfxrecon::decode::StructPointerDecoder<gfxrecon::decode::Decoded_VkAllocationCallbacks>*, gfxrecon::decode::HandlePointerDecoder<VkPipeline_T*>*) /gfxreconstruct/framework/generated/generated_vulkan_replay_consumer.cpp:995:61
    #14 0x56db1dceb1df in gfxrecon::decode::VulkanDecoder::Decode_vkCreateGraphicsPipelines(gfxrecon::decode::ApiCallInfo const&, unsigned char const*, unsigned long) /gfxreconstruct/framework/generated/generated_vulkan_decoder.cpp:1375:52
    #15 0x56db1dd3f6e6 in gfxrecon::decode::VulkanDecoder::DecodeFunctionCall(gfxrecon::format::ApiCallId, gfxrecon::decode::ApiCallInfo const&, unsigned char const*, unsigned long) /gfxreconstruct/framework/generated/generated_vulkan_decoder.cpp:14766:41
    #16 0x56db1d6709d4 in gfxrecon::decode::FileProcessor::ProcessFunctionCall(gfxrecon::format::BlockHeader const&, gfxrecon::format::ApiCallId, bool&) /gfxreconstruct/framework/decode/file_processor.cpp:689:48
    #17 0x56db1d66f6b7 in gfxrecon::decode::FileProcessor::ProcessBlocks() /gfxreconstruct/framework/decode/file_processor.cpp:307:64
    #18 0x56db1d66ef2a in gfxrecon::decode::FileProcessor::ProcessBlocksOneFrame() /gfxreconstruct/framework/decode/file_processor.cpp:122:25
    #19 0x56db1d66edc6 in gfxrecon::decode::FileProcessor::ProcessNextFrame()::'lambda'()::operator()() const /gfxreconstruct/framework/decode/file_processor.cpp:112:73
    #20 0x56db1d67923d in bool std::__invoke_impl<bool, gfxrecon::decode::FileProcessor::ProcessNextFrame()::'lambda'()&>(std::__invoke_other, gfxrecon::decode::FileProcessor::ProcessNextFrame()::'lambda'()&) /usr/include/c++/14/bits/invoke.h:61:36
    #21 0x56db1d679133 in std::enable_if<is_invocable_r_v<bool, gfxrecon::decode::FileProcessor::ProcessNextFrame()::'lambda'()&>, bool>::type std::__invoke_r<bool, gfxrecon::decode::FileProcessor::ProcessNextFrame()::'lambda'()&>(gfxrecon::decode::FileProcessor::ProcessNextFrame()::'lambda'()&) /usr/include/c++/14/bits/invoke.h:114:35
    #22 0x56db1d679006 in std::_Function_handler<bool (), gfxrecon::decode::FileProcessor::ProcessNextFrame()::'lambda'()>::_M_invoke(std::_Any_data const&) /usr/include/c++/14/bits/std_function.h:290:30
    #23 0x56db1d67a8db in std::function<bool ()>::operator()() const /usr/include/c++/14/bits/std_function.h:591:9
    #24 0x56db1d66ef76 in gfxrecon::decode::FileProcessor::DoProcessNextFrame(std::function<bool ()> const&) /gfxreconstruct/framework/decode/file_processor.cpp:132:34
    #25 0x56db1d66ee17 in gfxrecon::decode::FileProcessor::ProcessNextFrame() /gfxreconstruct/framework/decode/file_processor.cpp:113:30
    #26 0x56db1d59ae82 in gfxrecon::application::Application::PlaySingleFrame() /gfxreconstruct/framework/application/application.cpp:207:52
    #27 0x56db1d59acee in gfxrecon::application::Application::Run() /gfxreconstruct/framework/application/application.cpp:168:28
    #28 0x56db1d4ee8fd in main /gfxreconstruct/tools/replay/desktop_main.cpp:324:29
    #29 0x72f31bcfa337  (/lib/x86_64-linux-gnu/libc.so.6+0x2a337) (BuildId: 467f544f15035abef911999cbc14489edd0555ab)
    #30 0x72f31bcfa3fa in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a3fa) (BuildId: 467f544f15035abef911999cbc14489edd0555ab)
    #31 0x56db1d4d6aa4 in _start (/gfxreconstruct/build/tools/replay/gfxrecon-replay+0xccaa4) (BuildId: 46d2949d464fa1eacdc6c00f89eb8e9661551eba)

==18==Register values:
rax = 0x000070831ae1d6a8  rbx = 0x00007ffc932e4940  rcx = 0x00006f731bde2ba0  rdx = 0x0000000000000000  
rdi = 0x000072031ae30d50  rsi = 0x000070131ade1d50  rbp = 0x00007ffc932e4a90  rsp = 0x00007ffc932e4940  
 r8 = 0x00007ffc932e4ce0   r9 = 0x00000e02635bc3aa  r10 = 0x000070831ae1d480  r11 = 0x00006f731ade2ba0  
r12 = 0x00000e40635c61a7  r13 = 0x0000000021000017  r14 = 0x000072031ae30d38  r15 = 0x000072031ae30d2c  
AddressSanitizer can not provide additional info.
SUMMARY: AddressSanitizer: SEGV /mesa/buildASAN/../src/amd/compiler/aco_optimizer.cpp:3800:46 in aco::(anonymous namespace)::combine_instruction(aco::(anonymous namespace)::opt_ctx&, std::unique_ptr<aco::Instruction, aco::instr_deleter_functor>&)
==18==ABORTING

```
##### Chrome

Reproducing the issue requires an AMD GPU with the subgroups feature, I've been using a RX 7600. Opening the attached html file should trigger a crash in the Chrome GPU process. Start chrome and run it with the ASAN version of mesa (adapt paths as needed): `ASAN_OPTIONS=external_symbolizer_path=/usr/lib/llvm-20/bin/llvm-symbolizer VK_DRIVER_FILES=/path/to/src/amd/vulkan/radeon_icd.x86_64.json ./chrome --user-data-dir=/tmp/deleteme --use-angle=vulkan --enable-features=Vulkan --disable-gpu-watchdog --no-sandbox --enable-unsafe-webgpu` and open the attached html:

```
ASAN_OPTIONS=external_symbolizer_path=/usr/lib/llvm-20/bin/llvm-symbolizer VK_DRIVER_FILES=/home/user/mesa/radeon_icd.x86_64.json ./chrome --user-data-dir=/tmp/deleteme --use-angle=vulkan --enable-features=Vulkan --disable-gpu-watchdog --no-sandbox --enable-unsafe-webgpu
[10519:10519:0929/172016.461885:ERROR:ui/ozone/platform/wayland/gpu/wayland_surface_factory.cc:250] '--ozone-platform=wayland' is not compatible with Vulkan. Consider switching to '--ozone-platform=x11' or disabling Vulkan
Received signal 11 SEGV_ACCERR 78baa6b691a0
#0 0x5d12bd92b8a6 (/home/user/Downloads/linux-1499953/chrome+0xff578a5)
#1 0x5d12d3920e48 (/home/user/Downloads/linux-1499953/chrome+0x25f4ce47)
#2 0x5d12d38e1317 (/home/user/Downloads/linux-1499953/chrome+0x25f0d316)
#3 0x5d12d3920272 (/home/user/Downloads/linux-1499953/chrome+0x25f4c271)
#4 0x7c3aa74458d0 (/usr/lib/x86_64-linux-gnu/libc.so.6+0x458cf)
#5 0x783a86467b72 <unknown>
#6 0x783a8645e2fb <unknown>
#7 0x783a863f5987 <unknown>
#8 0x783a863f5499 <unknown>
#9 0x783a8614be78 <unknown>
#10 0x783a8613079f <unknown>
#11 0x783a861355c5 <unknown>
#12 0x783a86132e23 <unknown>
#13 0x5d12c07a4027 (/home/user/Downloads/linux-1499953/chrome+0x12dd0026)
#14 0x5d12c05093a8 (/home/user/Downloads/linux-1499953/chrome+0x12b353a7)
#15 0x5d12c03d8fea (/home/user/Downloads/linux-1499953/chrome+0x12a04fe9)
#16 0x5d12c03d8a55 (/home/user/Downloads/linux-1499953/chrome+0x12a04a54)
#17 0x5d12dd0b76f0 (/home/user/Downloads/linux-1499953/chrome+0x2f6e36ef)
#18 0x5d12dd0aa26d (/home/user/Downloads/linux-1499953/chrome+0x2f6d626c)
#19 0x5d12dd0b1304 (/home/user/Downloads/linux-1499953/chrome+0x2f6dd303)
#20 0x5d12dd06bd11 (/home/user/Downloads/linux-1499953/chrome+0x2f697d10)
#21 0x5d12dd06c1a4 (/home/user/Downloads/linux-1499953/chrome+0x2f6981a3)
#22 0x5d12dd060202 (/home/user/Downloads/linux-1499953/chrome+0x2f68c201)
#23 0x5d12c786d868 (/home/user/Downloads/linux-1499953/chrome+0x19e99867)
#24 0x5d12dc89d7f8 (/home/user/Downloads/linux-1499953/chrome+0x2eec97f7)
#25 0x5d12dc89ca44 (/home/user/Downloads/linux-1499953/chrome+0x2eec8a43)
#26 0x5d12dc8bed3e (/home/user/Downloads/linux-1499953/chrome+0x2eeead3d)
#27 0x5d12dc8cc8f8 (/home/user/Downloads/linux-1499953/chrome+0x2eef88f7)
#28 0x5d12dc8cc6e0 (/home/user/Downloads/linux-1499953/chrome+0x2eef86df)
#29 0x5d12c78af736 (/home/user/Downloads/linux-1499953/chrome+0x19edb735)
#30 0x5d12c78829cd (/home/user/Downloads/linux-1499953/chrome+0x19eae9cc)
#31 0x5d12c788062d (/home/user/Downloads/linux-1499953/chrome+0x19eac62c)
#32 0x5d12c7886d04 (/home/user/Downloads/linux-1499953/chrome+0x19eb2d03)
#33 0x5d12d37700a7 (/home/user/Downloads/linux-1499953/chrome+0x25d9c0a6)
#34 0x5d12d37e2d68 (/home/user/Downloads/linux-1499953/chrome+0x25e0ed67)
#35 0x5d12d37e1c4d (/home/user/Downloads/linux-1499953/chrome+0x25e0dc4c)
#36 0x5d12d37e385b (/home/user/Downloads/linux-1499953/chrome+0x25e0f85a)
#37 0x5d12d3635cd7 (/home/user/Downloads/linux-1499953/chrome+0x25c61cd6)
#38 0x5d12d37e4425 (/home/user/Downloads/linux-1499953/chrome+0x25e10424)
#39 0x5d12d36eeea0 (/home/user/Downloads/linux-1499953/chrome+0x25d1ae9f)
#40 0x5d12de76d57b (/home/user/Downloads/linux-1499953/chrome+0x30d9957a)
#41 0x5d12cfca75c1 (/home/user/Downloads/linux-1499953/chrome+0x222d35c0)
#42 0x5d12cfca864e (/home/user/Downloads/linux-1499953/chrome+0x222d464d)
#43 0x5d12cfcaafb4 (/home/user/Downloads/linux-1499953/chrome+0x222d6fb3)
#44 0x5d12cfca52df (/home/user/Downloads/linux-1499953/chrome+0x222d12de)
#45 0x5d12cfca580c (/home/user/Downloads/linux-1499953/chrome+0x222d180b)
#46 0x5d12bd9c0278 (/home/user/Downloads/linux-1499953/chrome+0xffec277)
#47 0x7c3aa742a578 (/usr/lib/x86_64-linux-gnu/libc.so.6+0x2a577)
#48 0x7c3aa742a63b (/usr/lib/x86_64-linux-gnu/libc.so.6+0x2a63a)
#49 0x5d12bd8e402a (/home/user/Downloads/linux-1499953/chrome+0xff10029)
  r8: 0000795aa5c3f2c8  r9: 00007ffe4fd509d0 r10: 0000000000000000 r11: 000000000000020f
 r12: 00007b4aae298cf0 r13: 0000000021000017 r14: 000078baa5b691a0 r15: 0000000000000045
  di: 00007ffe4fd509d0  si: 0000000000800000  bp: 000079caa5eaef80  bx: 000079caa5eaef80
  dx: 00007ffe4fd50a30  ax: 0000000000000018  cx: 0000000000000045  sp: 00007ffe4fd508a0
  ip: 0000783a86467b72 efl: 0000000000010206 cgf: 002b000000000033 erf: 0000000000000004
 trp: 000000000000000e msk: 0000000000000000 cr2: 000078baa6b691a0
[end of stack trace]

```

## Attachments

- [combine.gfxr](attachments/combine.gfxr) (application/octet-stream, 11.3 KB)
- [combine.wgsl](attachments/combine.wgsl) (application/octet-stream, 186 B)
- [combine.html](attachments/combine.html) (text/html, 2.7 KB)
- [Dockerfile](attachments/Dockerfile) (application/octet-stream, 1.9 KB)

## Timeline

### a7...@gmail.com (2025-09-30)

Upstream issue: <https://gitlab.freedesktop.org/mesa/mesa/-/issues/14013>

### ca...@chromium.org (2025-09-30)

I don't have an AMD GPU so I couldn't reproduce this, but triaging as a tentatively valid high severity bug, affecting all desktop OSs and FoundIn as current stable

### ca...@chromium.org (2025-09-30)

amaiorano: Can you help further triage this and reassign as appropriate? Thanks

### ds...@chromium.org (2025-10-01)

Reassiging to Peter as this crash was originally a Linux Chrome issue and he's probably better setup to repro. Looks like it's in Mesa, so we probably need to loop in someone from Mesa to take a look and see if there is a workaround we can put into our SPIR-V.

### pe...@google.com (2025-10-01)

Very simple wgls.

### a7...@gmail.com (2025-10-01)

Upsteam fix <https://gitlab.freedesktop.org/mesa/mesa/-/merge_requests/37643>

### ch...@google.com (2025-10-01)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2025-10-01)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ds...@chromium.org (2025-10-01)

Looks like this is due to a bug in an optimization pass for a `neg(multiply)`. I'm not sure where this is coming from, if I just run the shader through Tint I get:

```
               OpCapability Shader
               OpCapability GroupNonUniformArithmetic
         %20 = OpExtInstImport "GLSL.std.450"
               OpMemoryModel Logical GLSL450
               OpEntryPoint Fragment %frag_main "frag_main" %frag_main_loc0_Output
               OpExecutionMode %frag_main OriginUpperLeft
               OpMemberName %g_block 0 "inner"
               OpName %g_block "g_block"
               OpName %frag_main_loc0_Output "frag_main_loc0_Output"
               OpName %frag_main_inner "frag_main_inner"
               OpName %frag_main "frag_main"
               OpMemberDecorate %g_block 0 Offset 0
               OpDecorate %g_block Block
               OpDecorate %1 DescriptorSet 0
               OpDecorate %1 Binding 0
               OpDecorate %1 Coherent
               OpDecorate %frag_main_loc0_Output Location 0
      %float = OpTypeFloat 32
    %g_block = OpTypeStruct %float
%_ptr_StorageBuffer_g_block = OpTypePointer StorageBuffer %g_block
          %1 = OpVariable %_ptr_StorageBuffer_g_block StorageBuffer
    %v4float = OpTypeVector %float 4
%_ptr_Output_v4float = OpTypePointer Output %v4float
%frag_main_loc0_Output = OpVariable %_ptr_Output_v4float Output
          %9 = OpTypeFunction %v4float
%_ptr_StorageBuffer_float = OpTypePointer StorageBuffer %float
       %uint = OpTypeInt 32 0
     %uint_0 = OpConstant %uint 0
     %uint_3 = OpConstant %uint 3
         %22 = OpConstantNull %v4float
       %void = OpTypeVoid
         %25 = OpTypeFunction %void
%frag_main_inner = OpFunction %v4float None %9
         %10 = OpLabel
         %11 = OpAccessChain %_ptr_StorageBuffer_float %1 %uint_0
         %15 = OpLoad %float %11 None
         %16 = OpFNegate %float %15
         %17 = OpGroupNonUniformFMin %float %uint_3 Reduce %16
         %19 = OpExtInst %float %20 Tanh %17
         %21 = OpAccessChain %_ptr_StorageBuffer_float %1 %uint_0
               OpStore %21 %19 None
               OpReturnValue %22
               OpFunctionEnd
  %frag_main = OpFunction %void None %25
         %26 = OpLabel
         %27 = OpFunctionCall %v4float %frag_main_inner
               OpStore %frag_main_loc0_Output %27 None
               OpReturn
               OpFunctionEnd

```

Which has an `OpFNegate` but I don't see a multiply. I'm guessing there are more transforms we apply when this is Mesa, so could be useful to see the SPIR-V from a device where this is crashing to determine where the `negate(multiply)` comes from. Maybe we can change the operands around to do the `multiply(negate(a), b)` ourselves.

### pe...@google.com (2025-10-01)

running the combined.html on my zork (chromeos AMD) instantly crashed the GPU. This is a live issue on chromeos. (m142)

### pe...@google.com (2025-10-01)

I have not been able to reproduce this original failure. Not sure why yet.

### pe...@google.com (2025-10-02)

Definitely got it to reproduce on my Skyrim device (AMD chromebook)

### pe...@google.com (2025-10-03)

This can be polyfilled fixed by replacing unary negation of g with "sign(g) \*abs(g)"
and also we need to change unary abs(g) to "sign(g) \* g"

### ch...@google.com (2025-10-18)

petermcneeley: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### an...@chromium.org (2025-10-28)

[security shepherd] Hi petermcneeley@, any update on your proposed fix in c#14? Thanks!

### ch...@google.com (2025-10-28)

This V8 bug has been marked as either a release blocker or a vulnerability bug. V8 bugs affect all OSs supported by Chrome, so the OS field has been updated to reflect this. Please update the bug with the correct OS field if it only affects a subset of OSes.

### ch...@google.com (2025-11-02)

petermcneeley: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-11-17)

petermcneeley: Uh oh! This issue still open and hasn't been updated in the last 44 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ri...@google.com (2025-11-24)

[security shepherd] Hi petermcneeley@, are you still able to implement the fix in c#14? If not, would you mind finding another owner? This vulnerability is already past our 60-day SLO.

### pe...@google.com (2025-11-26)

I flashed to the latest m144 on skyrim (chromeOS device) and this is still happening
I think this is worth a polyfill even if we get a fix landed soon.

### ch...@google.com (2025-11-30)

We commit ourselves to a 60 day deadline for fixing for s1 severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

### pe...@google.com (2025-11-30)

WebGPU fix incoming <https://dawn-review.googlesource.com/c/dawn/+/276774>

### dx...@google.com (2025-12-01)

Project: dawn  

Branch:  main  

Author:  Peter McNeeley [petermcneeley@google.com](mailto:petermcneeley@google.com)  

Link:    <https://dawn-review.googlesource.com/276774>

[tint] Polyfill unary negation and abs for amd mesa frontend

---


Expand for full commit details
```
     
    Bug: 448294721 
    Change-Id: Ibca22bac11a7289538cefcd70169640d323b297c 
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/276774 
    Reviewed-by: James Price <jrprice@google.com> 
    Commit-Queue: Peter McNeeley <petermcneeley@google.com>

```

---

Files:

- M `src/dawn/native/Toggles.cpp`
- M `src/dawn/native/Toggles.h`
- M `src/dawn/native/vulkan/PhysicalDeviceVk.cpp`
- M `src/dawn/native/vulkan/PhysicalDeviceVk.h`
- M `src/dawn/native/vulkan/ShaderModuleVk.cpp`
- M `src/tint/lang/spirv/writer/common/options.h`
- M `src/tint/lang/spirv/writer/raise/BUILD.bazel`
- M `src/tint/lang/spirv/writer/raise/BUILD.cmake`
- M `src/tint/lang/spirv/writer/raise/BUILD.gn`
- M `src/tint/lang/spirv/writer/raise/raise.cc`
- A `src/tint/lang/spirv/writer/raise/unary_polyfill.cc`
- A `src/tint/lang/spirv/writer/raise/unary_polyfill.h`
- A `src/tint/lang/spirv/writer/raise/unary_polyfill_test.cc`

---

Hash: 7369bddb2b510ffd4feb52b8d32e853bfa6695e0  

Date: Mon Dec 1 17:10:36 2025


---

### pe...@google.com (2025-12-01)

My cl above ([comment #24](https://issues.chromium.org/issues/448294721#comment24)) should fix this specific issue.

### pe...@google.com (2025-12-01)

I tested these fixes locally before writing the polyfill. I am confident that this is fixed.

### dx...@google.com (2025-12-02)

Project: chromium/src  

Branch:  main  

Author:  chromium-autoroll [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com)  

Link:    <https://chromium-review.googlesource.com/7213910>

Roll Dawn from 0223916e3a57 to f25649879904 (15 revisions)

---


Expand for full commit details
```
     
    https://dawn.googlesource.com/dawn.git/+log/0223916e3a57..f25649879904 
     
    2025-12-01 petermcneeley@google.com [tint] Remove tanh expectation, known fixed 
    2025-12-01 bsheedy@google.com Add Symlink implementation to FSTestOSWrapper 
    2025-12-01 kainino@chromium.org [emscripten] Implement ExternalTexture 
    2025-12-01 dsinclair@chromium.org [msl] Split options into extensions and workarounds 
    2025-12-01 dsinclair@chromium.org [vk] Validate subgroup matrix configuration 
    2025-12-01 dsinclair@chromium.org [hlsl] Split options into extensions and workarounds 
    2025-12-01 cwallez@chromium.org [dawn][utils] Add ScopedIgnoreValidationErrors 
    2025-12-01 gman@chromium.org Capture: DrawIndexedIndirect 
    2025-12-01 gman@chromium.org Capture: DrawIndirect 
    2025-12-01 gman@chromium.org Capture: DrawIndexed 
    2025-12-01 gman@chromium.org Capture: Fix Texture Expectations 
    2025-12-01 petermcneeley@google.com [tint] Polyfill unary negation and abs for amd mesa frontend 
    2025-12-01 203005141+jacksonrl@users.noreply.github.com set ios to 14 in github action ci 
    2025-12-01 jrprice@google.com [tint] Remove workgroup size and storage reflection 
    2025-12-01 amaiorano@google.com [dawn][native] Add limits for resource tables 
     
    If this roll has caused a breakage, revert this CL and stop the roller 
    using the controls here: 
    https://autoroll.skia.org/r/dawn-chromium-autoroll 
    Please CC cwallez@google.com,dsinclair@google.com on the revert to ensure that a human 
    is aware of the problem. 
     
    To file a bug in Dawn: https://bugs.chromium.org/p/dawn/issues/entry 
    To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry 
     
    To report a problem with the AutoRoller itself, please file a bug: 
    https://issues.skia.org/issues/new?component=1389291&template=1850622 
     
    Documentation for the AutoRoller is here: 
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md 
     
    Cq-Include-Trybots: luci.chromium.try:dawn-android-arm-deps-rel;luci.chromium.try:dawn-android-arm64-deps-rel;luci.chromium.try:dawn-linux-x64-deps-rel;luci.chromium.try:dawn-mac-x64-deps-rel;luci.chromium.try:dawn-mac-arm64-deps-rel;luci.chromium.try:dawn-win10-x64-deps-rel;luci.chromium.try:dawn-win10-x86-deps-rel;luci.chromium.try:dawn-win11-arm64-deps-rel;luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:gpu-fyi-cq-android-arm64 
    Bug: chromium:435317394,chromium:436025865,chromium:448294721,chromium:451338754,chromium:463425874,chromium:463925499 
    Tbr: dsinclair@google.com 
    Change-Id: Ib2c4a21f1eee3a94eca7056467c6880e20e9354a 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7213910 
    Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Cr-Commit-Position: refs/heads/main@{#1552499}

```

---

Files:

- M `DEPS`
- M `third_party/dawn`

---

Hash: [83eb99306e606337c1187f0c5f0757f44301b5b9](https://chromiumdash.appspot.com/commit/83eb99306e606337c1187f0c5f0757f44301b5b9)  

Date: Tue Dec 2 02:09:05 2025


---

### ch...@google.com (2025-12-02)

Security Merge Request Consideration: Requesting merge to stable (M142) because latest trunk commit (1552499) appears to be after stable branch point (1522585).
Security Merge Request Consideration: Requesting merge to beta (M143) because latest trunk commit (1552499) appears to be after beta branch point (1536371).
Security Merge Request - Manual Review: Merge review required: a commit with DEPS changes was detected.

Security Merge Request - Manual Review: Merge review required: a commit with DEPS changes was detected.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [142, 143].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### ch...@google.com (2025-12-03)

Security Merge Request Consideration: Requesting merge to stable (M142) because latest trunk commit (1552499) appears to be after stable branch point (1522585).
Security Merge Request Consideration: Requesting merge to beta (M143) because latest trunk commit (1552499) appears to be after beta branch point (1536371).
Security Merge Request Consideration: Requesting merge to dev (M144) because latest trunk commit (1552499) appears to be after dev branch point (1552494).
Security Merge Request - Manual Review: Merge review required: a commit with DEPS changes was detected.

Security Merge Request - Manual Review: Merge review required: a commit with DEPS changes was detected.

Security Merge Request - Manual Review: Merge review required: a commit with DEPS changes was detected.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [142, 143, 144].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### pe...@google.com (2025-12-03)

Which CLs should be backmerged? (Please include Gerrit links.)
<https://dawn-review.googlesource.com/276774>

Has this fix been verified on Canary to not pose any stability regressions?
Not yet. We can wait a few days.

Does this fix pose any potential non-verifiable stability risks?
Potentially yes as this is a compiler transform that operates on all shaders. We should as a minimum backport to m144.

Does this fix pose any known compatibility risks?
No

Does it require manual verification by the test team? If so, please describe required testing.
No

(no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### ya...@chromium.org (2025-12-05)

It's been a couple of days. Have you seen any issues on Canary?

### pe...@google.com (2025-12-05)

No. I did add a next action on the 8th.
I definitely think we should backport this to at least m144.

### pe...@google.com (2025-12-05)

<https://chromiumdash.appspot.com/commit/7369bddb2b510ffd4feb52b8d32e853bfa6695e0>

### pe...@google.com (2025-12-08)

The NextAction date has arrived: 2025-12-08
To opt-out from this automation rule, please add Optout-Blintz-Nextaction-Alert to the "Chromium Labels" custom field.

### sp...@google.com (2025-12-08)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $10000.00 for this report.

Rationale for this decision:
Memory corruption in a highly privileged process (e.g. GPU, network processes) 


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### dx...@google.com (2025-12-11)

Project: dawn  

Branch:  chromium/7559  

Author:  Peter McNeeley [petermcneeley@google.com](mailto:petermcneeley@google.com)  

Link:    <https://dawn-review.googlesource.com/279435>

[tint] Polyfill unary negation and abs for amd mesa frontend

---


Expand for full commit details
```
     
    Bug: 448294721 
    Change-Id: Ibca22bac11a7289538cefcd70169640d323b297c 
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/276774 
    Reviewed-by: James Price <jrprice@google.com> 
    Commit-Queue: Peter McNeeley <petermcneeley@google.com> 
    (cherry picked from commit 7369bddb2b510ffd4feb52b8d32e853bfa6695e0) 
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/279435

```

---

Files:

- M `src/dawn/native/Toggles.cpp`
- M `src/dawn/native/Toggles.h`
- M `src/dawn/native/vulkan/PhysicalDeviceVk.cpp`
- M `src/dawn/native/vulkan/PhysicalDeviceVk.h`
- M `src/dawn/native/vulkan/ShaderModuleVk.cpp`
- M `src/tint/lang/spirv/writer/common/options.h`
- M `src/tint/lang/spirv/writer/raise/BUILD.bazel`
- M `src/tint/lang/spirv/writer/raise/BUILD.cmake`
- M `src/tint/lang/spirv/writer/raise/BUILD.gn`
- M `src/tint/lang/spirv/writer/raise/raise.cc`
- A `src/tint/lang/spirv/writer/raise/unary_polyfill.cc`
- A `src/tint/lang/spirv/writer/raise/unary_polyfill.h`
- A `src/tint/lang/spirv/writer/raise/unary_polyfill_test.cc`

---

Hash: e482afa257f44ed4cbef940d3f763ae246eae02c  

Date: Thu Dec 11 04:40:14 2025


---

### ch...@google.com (2025-12-12)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ya...@chromium.org (2025-12-12)

Provided there remain no issues on Canary, please proceed with the merge

### pe...@google.com (2025-12-12)

[Comment #36](https://issues.chromium.org/issues/448294721#comment36) is the merge to m144
<https://chromiumdash.appspot.com/commit/e482afa257f44ed4cbef940d3f763ae246eae02c>

### sr...@chromium.org (2025-12-12)

pls complete the merge to 143 asap as well thanks

### pe...@google.com (2025-12-15)

LTS Milestone M138

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### dx...@google.com (2025-12-15)

Project: dawn  

Branch:  chromium/7499  

Author:  Peter McNeeley [petermcneeley@google.com](mailto:petermcneeley@google.com)  

Link:    <https://dawn-review.googlesource.com/280515>

[tint] Polyfill unary negation and abs for amd mesa frontend

---


Expand for full commit details
```
     
    Bug: 448294721 
    Change-Id: Ibca22bac11a7289538cefcd70169640d323b297c 
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/276774 
    Reviewed-by: James Price <jrprice@google.com> 
    Commit-Queue: Peter McNeeley <petermcneeley@google.com> 
    (cherry picked from commit 7369bddb2b510ffd4feb52b8d32e853bfa6695e0) 
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/280515 
    Reviewed-by: dan sinclair <dsinclair@chromium.org>

```

---

Files:

- M `src/dawn/native/Toggles.cpp`
- M `src/dawn/native/Toggles.h`
- M `src/dawn/native/vulkan/PhysicalDeviceVk.cpp`
- M `src/dawn/native/vulkan/PhysicalDeviceVk.h`
- M `src/dawn/native/vulkan/ShaderModuleVk.cpp`
- M `src/tint/lang/spirv/writer/common/options.h`
- M `src/tint/lang/spirv/writer/raise/BUILD.bazel`
- M `src/tint/lang/spirv/writer/raise/BUILD.cmake`
- M `src/tint/lang/spirv/writer/raise/BUILD.gn`
- M `src/tint/lang/spirv/writer/raise/raise.cc`
- A `src/tint/lang/spirv/writer/raise/unary_polyfill.cc`
- A `src/tint/lang/spirv/writer/raise/unary_polyfill.h`
- A `src/tint/lang/spirv/writer/raise/unary_polyfill_test.cc`

---

Hash: 479f62d2194fd6e44c37d07654ca6e41c42bd332  

Date: Mon Dec 15 22:17:54 2025


---

### sr...@chromium.org (2025-12-15)

as per offline chat , 142 merge for win/mac is not needed as this issue doesnt impact desktop and impacts CrOS so dropping 142 merge approved label 

### qk...@google.com (2025-12-16)

Labeling this issue as not applicable for LTS M138 because the fix[1] causes conflicts in 6 files, and the conflicts require dependency CLs to be fixed. I think it's not safe to merge more patches together for LTS.

[1] <https://dawn-review.googlesource.com/c/dawn/+/276774>

### ch...@google.com (2026-03-10)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> Memory corruption in a highly privileged process (e.g. GPU, network processes)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/448294721)*
