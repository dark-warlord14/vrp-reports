# libGLES_mali memory safety violation via WebGPU shaders at llvm::Value::setNameImpl

| Field | Value |
|-------|-------|
| **Issue ID** | [379551588](https://issues.chromium.org/issues/379551588) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | Dawn>Tint |
| **Platforms** | Android |
| **Reporter** | a7...@gmail.com |
| **Assignee** | ds...@chromium.org |
| **Created** | 2024-11-18 |
| **Bounty** | $35,000.00 |

## Description

##### VULNERABILITY DETAILS

Chrome on Android translates WebGPU shaders to SPIR-V. These SPIR-V shaders are eventually passed to libGLES\_mali.so for optimization and native code generation. This bug report is about a WebGPU shader that crashes com.android.chrome (and sometimes com.android.systemui, not really sure how those are related). When running a standalone reproducer with ARM MTE enabled, the issue can be attributed to libGLES\_mali.so. MTE terminates the standalone reproducer as it detects an OOB access in `llvm::Value::setNameImpl`.

##### VERSION

Device: Pixel 9 Pro XL  

Android build number: AP3A.241105.008  

Chrome: 130.0.6723.102

##### REPRODUCTION CASE

Attached a html file that triggers the crash. Below the adb log of com.android.chrome (running without MTE) and afterwards of the standalone reproducer (running with MTE). It took me a couple of attempts to provoke a chrome crash (standalone reproduction with MTE is deterministic); if caching is a concern: there is a `256u` in the shader, I successfully tested smaller values such as 247.

com.android.chrome:

```
11-18 17:13:19.058 22895 22895 F DEBUG   : Build fingerprint: 'google/komodo/komodo:15/AP3A.241105.008/12485168:user/release-keys'
11-18 17:13:19.058 22895 22895 F DEBUG   : Revision: 'MP1.0'
11-18 17:13:19.058 22895 22895 F DEBUG   : ABI: 'arm64'
11-18 17:13:19.058 22895 22895 F DEBUG   : Timestamp: 2024-11-18 17:13:18.535765682+0100
11-18 17:13:19.058 22895 22895 F DEBUG   : Process uptime: 715029s
11-18 17:13:19.058 22895 22895 F DEBUG   : Cmdline: com.android.systemui
11-18 17:13:19.058 22895 22895 F DEBUG   : pid: 2068, tid: 2128, name: RenderThread  >>> com.android.systemui <<<
11-18 17:13:19.058 22895 22895 F DEBUG   : uid: 10244
11-18 17:13:19.058 22895 22895 F DEBUG   : tagged_addr_ctrl: 000000000007fff1 (PR_TAGGED_ADDR_ENABLE, mask 0xfffe)
11-18 17:13:19.058 22895 22895 F DEBUG   : pac_enabled_keys: 000000000000000f (PR_PAC_APIAKEY, PR_PAC_APIBKEY, PR_PAC_APDAKEY, PR_PAC_APDBKEY)
11-18 17:13:19.058 22895 22895 F DEBUG   : signal 6 (SIGABRT), code -1 (SI_QUEUE), fault addr --------
11-18 17:13:19.058 22895 22895 F DEBUG   : Abort message: 'VK_ERROR_DEVICE_LOST (RenderThread, 1 vendor info (65537:0)): Exception type 0x10001: GPU fault.'
11-18 17:13:19.058 22895 22895 F DEBUG   :     x0  0000000000000000  x1  0000000000000850  x2  0000000000000006  x3  0000007163d4e910
11-18 17:13:19.058 22895 22895 F DEBUG   :     x4  000000000000000a  x5  000000000000000a  x6  000000000000000a  x7  00000074b6cdeffc
11-18 17:13:19.058 22895 22895 F DEBUG   :     x8  00000000000000f0  x9  00000074d645c3a8  x10 0000000000000001  x11 00000074d64ad6f0
11-18 17:13:19.058 22895 22895 F DEBUG   :     x12 00000000153d6ea0  x13 00000000153d6ea0  x14 0000007163d4d700  x15 00000ffb7b7fdecb
11-18 17:13:19.058 22895 22895 F DEBUG   :     x16 00000074d6517fd0  x17 00000074d6501040  x18 00000071634fc000  x19 0000000000000814
11-18 17:13:19.058 22895 22895 F DEBUG   :     x20 0000000000000850  x21 00000000ffffffff  x22 00000072077a0180  x23 00000073bb561c60
11-18 17:13:19.058 22895 22895 F DEBUG   :     x24 00000074c2068087  x25 00000074c2099ed2  x26 00000074c2065ef8  x27 00000074c208164e
11-18 17:13:19.058 22895 22895 F DEBUG   :     x28 00000074c206bc7a  x29 0000007163d4e990
11-18 17:13:19.058 22895 22895 F DEBUG   :     lr  00000074d6496a58  sp  0000007163d4e8f0  pc  00000074d6496a84  pst 0000000000001000
11-18 17:13:19.058 22895 22895 F DEBUG   : 13 total frames
11-18 17:13:19.058 22895 22895 F DEBUG   : backtrace:
11-18 17:13:19.058 22895 22895 F DEBUG   :       #00 pc 000000000005da84  /apex/com.android.runtime/lib64/bionic/libc.so (abort+164) (BuildId: 32a42812c629603f9b8fb44bd931166b)
11-18 17:13:19.058 22895 22895 F DEBUG   :       #01 pc 000000000092f3fc  /apex/com.android.art/lib64/libart.so (art::Runtime::Abort(char const*)+344) (BuildId: dcb9fe2b5c99aa3f1a682a6008427d08)
11-18 17:13:19.058 22895 22895 F DEBUG   :       #02 pc 00000000000160fc  /apex/com.android.art/lib64/libbase.so (android::base::SetAborter(std::__1::function<void (char const*)>&&)::$_0::__invoke(char
 const*)+80) (BuildId: 42d41ca7c77853791d096606e7186547)
11-18 17:13:19.058 22895 22895 F DEBUG   :       #03 pc 000000000000c2d0  /system/lib64/liblog.so (__android_log_assert+288) (BuildId: 6c6c7184c32b8026f55145c840d2d1d3)
11-18 17:13:19.058 22895 22895 F DEBUG   :       #04 pc 00000000005daed8  /system/lib64/libhwui.so (android::uirenderer::renderthread::(anonymous namespace)::onVkDeviceFault(std::__1::basic_string<char
, std::__1::char_traits<char>, std::__1::allocator<char>> const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, std::__1::vector<VkDeviceFaultAddressInfoE
XT, std::__1::allocator<VkDeviceFaultAddressInfoEXT>> const&, std::__1::vector<VkDeviceFaultVendorInfoEXT, std::__1::allocator<VkDeviceFaultVendorInfoEXT>> const&, std::__1::vector<std::byte, std::__1:
:allocator<std::byte>> const&) (.__uniq.192405051647925496281077346275335259674)+1464) (BuildId: d0fbbf82fac0387511250862f416d83f)
11-18 17:13:19.058 22895 22895 F DEBUG   :       #05 pc 00000000005da8c8  /system/lib64/libhwui.so (android::uirenderer::renderthread::(anonymous namespace)::deviceLostProcRenderThread(void*, std::__1:
:basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, std::__1::vector<VkDeviceFaultAddressInfoEXT, std::__1::allocator<VkDeviceFaultAddressInfoEXT>> const&, std::__1::vec
tor<VkDeviceFaultVendorInfoEXT, std::__1::allocator<VkDeviceFaultVendorInfoEXT>> const&, std::__1::vector<std::byte, std::__1::allocator<std::byte>> const&) (.__uniq.192405051647925496281077346275335259674)+56) (BuildId: d0fbbf82fac0387511250862f416d83f)
11-18 17:13:19.058 22895 22895 F DEBUG   :       #06 pc 0000000000211194  /system/lib64/libhwui.so (skgpu::InvokeDeviceLostCallback(skgpu::VulkanInterface const*, VkDevice_T*, void*, void (*)(void*, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, std::__1::vector<VkDeviceFaultAddressInfoEXT, std::__1::allocator<VkDeviceFaultAddressInfoEXT>> const&, std::__1::vector<VkDeviceFaultVendorInfoEXT, std::__1::allocator<VkDeviceFaultVendorInfoEXT>> const&, std::__1::vector<std::byte, std::__1::allocator<std::byte>> const&), bool)+708) (BuildId: d0fbbf82fac0387511250862f416d83f)
11-18 17:13:19.058 22895 22895 F DEBUG   :       #07 pc 0000000000211368  /system/lib64/libhwui.so (GrVkResourceProvider::checkCommandBuffers()+232) (BuildId: d0fbbf82fac0387511250862f416d83f)
11-18 17:13:19.058 22895 22895 F DEBUG   :       #08 pc 000000000033d7b8  /system/lib64/libhwui.so (GrDirectContext::performDeferredCleanup(std::__1::chrono::duration<long long, std::__1::ratio<1l, 1000l>>, GrPurgeResourceOptions)+104) (BuildId: d0fbbf82fac0387511250862f416d83f)
11-18 17:13:19.058 22895 22895 F DEBUG   :       #09 pc 00000000003420b4  /system/lib64/libhwui.so (android::uirenderer::renderthread::RenderThread::threadLoop()+756) (BuildId: d0fbbf82fac0387511250862f416d83f)
11-18 17:13:19.058 22895 22895 F DEBUG   :       #10 pc 0000000000016c90  /system/lib64/libutils.so (android::Thread::_threadLoop(void*)+368) (BuildId: fa639e42761c9f4d00a390a8b06ed417)
11-18 17:13:19.058 22895 22895 F DEBUG   :       #11 pc 000000000006f718  /apex/com.android.runtime/lib64/bionic/libc.so (__pthread_start(void*)+200) (BuildId: 32a42812c629603f9b8fb44bd931166b)
11-18 17:13:19.058 22895 22895 F DEBUG   :       #12 pc 0000000000060e00  /apex/com.android.runtime/lib64/bionic/libc.so (__start_thread+64) (BuildId: 32a42812c629603f9b8fb44bd931166b)
11-18 17:13:19.085 32310   804 F libc    : Fatal signal 6 (SIGABRT), code -1 (SI_QUEUE) in tid 804 (RenderThread), pid 32310 (.android.chrome)
11-18 17:13:19.137   556   556 E tombstoned: Tombstone written to: tombstone_15

```

standalone reproducer:

```
11-18 17:07:49.612 21887 21887 F DEBUG   : Build fingerprint: 'google/komodo/komodo:15/AP3A.241105.008/12485168:user/release-keys'
11-18 17:07:49.612 21887 21887 F DEBUG   : Revision: 'MP1.0'
11-18 17:07:49.612 21887 21887 F DEBUG   : ABI: 'arm64'
11-18 17:07:49.612 21887 21887 F DEBUG   : Timestamp: 2024-11-18 17:07:49.514248188+0100
11-18 17:07:49.612 21887 21887 F DEBUG   : Process uptime: 2s
11-18 17:07:49.612 21887 21887 F DEBUG   : Cmdline: ./tint_no_afl min.wgsl --mesafuzz
11-18 17:07:49.612 21887 21887 F DEBUG   : pid: 21873, tid: 21873, name: tint_no_afl  >>> ./tint_no_afl <<<
11-18 17:07:49.612 21887 21887 F DEBUG   : uid: 2000
11-18 17:07:49.612 21887 21887 F DEBUG   : tagged_addr_ctrl: 000000000007fff3 (PR_TAGGED_ADDR_ENABLE, PR_MTE_TCF_SYNC, mask 0xfffe)
11-18 17:07:49.612 21887 21887 F DEBUG   : pac_enabled_keys: 000000000000000f (PR_PAC_APIAKEY, PR_PAC_APIBKEY, PR_PAC_APDAKEY, PR_PAC_APDBKEY)
11-18 17:07:49.612 21887 21887 F DEBUG   : signal 11 (SIGSEGV), code 9 (SEGV_MTESERR), fault addr 0x0500007da0af0c00
11-18 17:07:49.612 21887 21887 F DEBUG   :     x0  0300007e70aeea00  x1  0000007fc0dcefc0  x2  0000000000000001  x3  0300007e70aee9c0
11-18 17:07:49.612 21887 21887 F DEBUG   :     x4  0000000000000002  x5  0000000000000000  x6  0000000000000080  x7  0000000000000001
11-18 17:07:49.612 21887 21887 F DEBUG   :     x8  0500007da0af00f0  x9  0000000000000058  x10 0300007e70aee9e8  x11 0300007e70aeea00
11-18 17:07:49.612 21887 21887 F DEBUG   :     x12 0300007e70aee9e0  x13 0000000000000048  x14 0000000000000001  x15 fffffffffffff000
11-18 17:07:49.612 21887 21887 F DEBUG   :     x16 0000007f826fa038  x17 0000007f82680380  x18 0000007f8545c000  x19 0000000000000001
11-18 17:07:49.612 21887 21887 F DEBUG   :     x20 0300007e70aeea00  x21 0000007fc0dcf0b8  x22 0900007d40b28ad0  x23 0100007d70aea878
11-18 17:07:49.612 21887 21887 F DEBUG   :     x24 0000007f852cdf80  x25 0000000000000001  x26 0000007f852cdf80  x27 0e00007df0b1fa40
11-18 17:07:49.612 21887 21887 F DEBUG   :     x28 0000000000000000  x29 0000000000000000
11-18 17:07:49.612 21887 21887 F DEBUG   :     lr  0000007ce8d0ade4  sp  0000007fc0dcee30  pc  0000007ce8d0aa04  pst 0000000080001000
11-18 17:07:49.612 21887 21887 F DEBUG   : 18 total frames
11-18 17:07:49.612 21887 21887 F DEBUG   : backtrace:
11-18 17:07:49.612 21887 21887 F DEBUG   :   NOTE: Function names and BuildId information is missing for some frames due
11-18 17:07:49.612 21887 21887 F DEBUG   :   NOTE: to unreadable libraries. For unwinds of apps, only shared libraries
11-18 17:07:49.612 21887 21887 F DEBUG   :   NOTE: found under the lib/ directory are readable.
11-18 17:07:49.612 21887 21887 F DEBUG   :   NOTE: On this device, run setenforce 0 to make the libraries readable.
11-18 17:07:49.612 21887 21887 F DEBUG   :   NOTE: Unreadable libraries:
11-18 17:07:49.612 21887 21887 F DEBUG   :   NOTE:   /data/local/tmp/tint_no_afl
11-18 17:07:49.612 21887 21887 F DEBUG   :       #00 pc 0000000002d03a04  /vendor/lib64/egl/libGLES_mali.so (llvm::Value::setNameImpl(llvm::Twine const&)+52) (BuildId: 33542643f7d7aab2)
11-18 17:07:49.613 21887 21887 F DEBUG   :       #01 pc 0000000002d03de0  /vendor/lib64/egl/libGLES_mali.so (llvm::Value::setName(llvm::Twine const&, bool)+16) (BuildId: 33542643f7d7aab2)
11-18 17:07:49.613 21887 21887 F DEBUG   :       #02 pc 0000000000aee1bc  /vendor/lib64/egl/libGLES_mali.so (llvm::IRBuilderBase::CreateExtractElement(llvm::Value*, llvm::Value*, llvm::Twine const&)+252) (BuildId: 33542643f7d7aab2)
11-18 17:07:49.613 21887 21887 F DEBUG   :       #03 pc 0000000001c71360  /vendor/lib64/egl/libGLES_mali.so (LIR2LLVMConverter::convert_swizzle(cmpbe_node const*)+144) (BuildId: 33542643f7d7aab2)
11-18 17:07:49.613 21887 21887 F DEBUG   :       #04 pc 0000000001c67cd0  /vendor/lib64/egl/libGLES_mali.so (LIR2LLVMConverter::TraverseBBs(_tag_mempool*, cmpbe_bb*, bool)+304) (BuildId: 33542643f7d7aab2)
11-18 17:07:49.613 21887 21887 F DEBUG   :       #05 pc 0000000001c67d3c  /vendor/lib64/egl/libGLES_mali.so (LIR2LLVMConverter::TraverseBBs(_tag_mempool*, cmpbe_bb*, bool)+412) (BuildId: 33542643f7d7aab2)
11-18 17:07:49.613 21887 21887 F DEBUG   :       #06 pc 0000000001c68f64  /vendor/lib64/egl/libGLES_mali.so (lir2llvm(cmpbep_pass_manager_context*) (.llvm.5730081084462460087)+3764) (BuildId: 33542643f7d7aab2)
11-18 17:07:49.613 21887 21887 F DEBUG   :       #07 pc 0000000001d69d68  /vendor/lib64/egl/libGLES_mali.so (cmpbep_run_pass+360) (BuildId: 33542643f7d7aab2)
11-18 17:07:49.613 21887 21887 F DEBUG   :       #08 pc 0000000001c63784  /vendor/lib64/egl/libGLES_mali.so (cmpbe_compile_gles_shader+580) (BuildId: 33542643f7d7aab2)
11-18 17:07:49.613 21887 21887 F DEBUG   :       #09 pc 0000000001c8781c  /vendor/lib64/egl/libGLES_mali.so (do_single_part2_compilation+204) (BuildId: 33542643f7d7aab2)
11-18 17:07:49.613 21887 21887 F DEBUG   :       #10 pc 0000000001c872f0  /vendor/lib64/egl/libGLES_mali.so (cmpbe_v2_compile_multiple_shaders+9536) (BuildId: 33542643f7d7aab2)
11-18 17:07:49.613 21887 21887 F DEBUG   :       #11 pc 0000000001b87790  /vendor/lib64/egl/libGLES_mali.so (gfx::compiler::compile_shaders(gfx::shader_set const&, gfx::shader_set&, hal::shader_language, gfx::shader_state const&, compiler_cache*, gfx::mem_allocator&, cutils_cmpbe_dump_ctx**, bool*, unsigned long*)+7152) (BuildId: 33542643f7d7aab2)
11-18 17:07:49.613 21887 21887 F DEBUG   :       #12 pc 0000000000923070  /vendor/lib64/egl/libGLES_mali.so (vkCreateComputePipelines+1984) (BuildId: 33542643f7d7aab2)
11-18 17:07:49.613 21887 21887 F DEBUG   :       #13 pc 00000000000af6c0  /data/local/tmp/tint_no_afl
11-18 17:07:49.613 21887 21887 F DEBUG   :       #14 pc 00000000000b0430  /data/local/tmp/tint_no_afl
11-18 17:07:49.613 21887 21887 F DEBUG   :       #15 pc 00000000000b0bbc  /data/local/tmp/tint_no_afl
11-18 17:07:49.613 21887 21887 F DEBUG   :       #16 pc 00000000000b2668  /data/local/tmp/tint_no_afl
11-18 17:07:49.613 21887 21887 F DEBUG   : Note: multiple potential causes for this crash were detected, listing them in decreasing order of likelihood.
11-18 17:07:49.613 21887 21887 F DEBUG   : Cause: [MTE]: Buffer Overflow, 8 bytes right of a 2856-byte allocation at 0x7da0af00d0
11-18 17:07:49.613 21887 21887 F DEBUG   : allocated by thread 21873:
11-18 17:07:49.613 21887 21887 F DEBUG   :       #00 pc 000000000004b594  /apex/com.android.runtime/lib64/bionic/libc.so (scudo::Allocator<scudo::AndroidNormalConfig, &scudo_malloc_postinit>::allocate(unsigned long, scudo::Chunk::Origin, unsigned long, bool)+852) (BuildId: 32a42812c629603f9b8fb44bd931166b)
11-18 17:07:49.613 21887 21887 F DEBUG   :       #01 pc 000000000004b904  /apex/com.android.runtime/lib64/bionic/libc.so (scudo_malloc+36) (BuildId: 32a42812c629603f9b8fb44bd931166b)
11-18 17:07:49.613 21887 21887 F DEBUG   :       #02 pc 00000000000456cc  /apex/com.android.runtime/lib64/bionic/libc.so (malloc+44) (BuildId: 32a42812c629603f9b8fb44bd931166b)
11-18 17:07:49.613 21887 21887 F DEBUG   :       #03 pc 000000000008bff0  /vendor/lib64/libc++.so (operator new(unsigned long)+28) (BuildId: 53e0091d25a788802d2d3a5324f79b527df4913f)
11-18 17:07:49.613 21887 21887 F DEBUG   :       #04 pc 0000000002ccffdc  /vendor/lib64/egl/libGLES_mali.so (llvm::LLVMContext::LLVMContext(llvm::Mali::MemPool*)+44) (BuildId: 33542643f7d7aab2)
11-18 17:07:49.613 21887 21887 F DEBUG   : Cause: [MTE]: Use After Free, 2864 bytes into a 3088-byte allocation at 0x7da0af00d0
11-18 17:07:49.613 21887 21887 F DEBUG   : deallocated by thread 21873:
11-18 17:07:49.613 21887 21887 F DEBUG   :       #00 pc 00000000000514b8  /apex/com.android.runtime/lib64/bionic/libc.so (scudo::Allocator<scudo::AndroidNormalConfig, &scudo_malloc_postinit>::quarantineOrDeallocateChunk(scudo::Options const&, void*, scudo::Chunk::UnpackedHeader*, unsigned long)+968) (BuildId: 32a42812c629603f9b8fb44bd931166b)
11-18 17:07:49.613 21887 21887 F DEBUG   :       #01 pc 000000000004b740  /apex/com.android.runtime/lib64/bionic/libc.so (scudo::Allocator<scudo::AndroidNormalConfig, &scudo_malloc_postinit>::deallocate(void*, scudo::Chunk::Origin, unsigned long, unsigned long)+192) (BuildId: 32a42812c629603f9b8fb44bd931166b)
11-18 17:07:49.613 21887 21887 F DEBUG   :       #02 pc 0000000001e12c94  /vendor/lib64/egl/libGLES_mali.so (cutils_strdict_insert+1044) (BuildId: 33542643f7d7aab2)
11-18 17:07:49.613 21887 21887 F DEBUG   : allocated by thread 21873:
11-18 17:07:49.613 21887 21887 F DEBUG   :       #00 pc 000000000004b594  /apex/com.android.runtime/lib64/bionic/libc.so (scudo::Allocator<scudo::AndroidNormalConfig, &scudo_malloc_postinit>::allocate(unsigned long, scudo::Chunk::Origin, unsigned long, bool)+852) (BuildId: 32a42812c629603f9b8fb44bd931166b)
11-18 17:07:49.613 21887 21887 F DEBUG   :       #01 pc 000000000004b904  /apex/com.android.runtime/lib64/bionic/libc.so (scudo_malloc+36) (BuildId: 32a42812c629603f9b8fb44bd931166b)
11-18 17:07:49.613 21887 21887 F DEBUG   :       #02 pc 00000000000456cc  /apex/com.android.runtime/lib64/bionic/libc.so (malloc+44) (BuildId: 32a42812c629603f9b8fb44bd931166b)
11-18 17:07:49.613 21887 21887 F DEBUG   :       #03 pc 0000000000923c6c  /vendor/lib64/egl/libGLES_mali.so (gfx::host_mem_allocator::allocate_cutils_wrapper(void*, unsigned long)+28) (BuildId: 33542643f7d7aab2)
11-18 17:07:49.613 21887 21887 F DEBUG   : Learn more about MTE reports: https://source.android.com/docs/security/test/memory-safety/mte-reports

```

## Attachments

- [androidoob.html](attachments/androidoob.html) (text/html, 4.1 KB)
- [comp.spv](attachments/comp.spv) (application/octet-stream, 2.4 KB)
- [standalone.cpp](attachments/standalone.cpp) (text/x-c++src, 7.6 KB)
- [androidoob.html](attachments/androidoob.html) (text/html, 4.1 KB)
- [androidoob2.html](attachments/androidoob2.html) (text/html, 4.2 KB)
- [comp(2).spv](attachments/comp(2).spv) (application/octet-stream, 3.7 KB)

## Timeline

### a7...@gmail.com (2024-11-18)

This issue has also been reported to ARM PSIRT

### am...@chromium.org (2024-11-18)

Thank you for the report and also confirming you have already reported this issue upstream to Arm.

Generally I would not pass over a report without an attempt to reproduce, but given the nature of this report and the low likelihood I will be able to successfully reproduce without hardware, I'm going to go ahead and pass this along to the WebGPU team. This issue in in the Mali driver, but WebGPU team can make the determination if a workaround in WebGPU is appropriate.

S0/P1 for OOB memory access in the GPU, which is not sandboxed on Android.

### am...@chromium.org (2024-11-18)

Since this is a Mali driver bug, as discussed on bug (in process that will be including into our shepherding guidelines soon -- this is a draft CL up in gerrit), providing visibility to appropriate Pixel, Android, and ChromeOS points of contact.

### cw...@chromium.org (2024-11-18)

Dan PTAL for triage, note that the Ganesh stack is likely unrelated to the issue itself, and it just happens that they are the one catching the issue first. Maybe with `VkDeviceFaultAddressInfoEXT`.

### a7...@gmail.com (2024-11-18)

I forgot to add, if you would like to use the standalone reproducer let me know.

### dn...@google.com (2024-11-18)

Staring at the stack trace, the bug is probably in Arm's private code: LIR2LLVMConverter::convert\_swizzle
It is calling llvm::IRBuilderBase::CreateExtractElement(llvm::Value\*, llvm::Value\*, llvm::Twine const&) likely with a bad last argument.

The "Twine" type is essentially a pointer to a C-string, but it doesn't take ownership of the memory. The LLVM call has supplies an optional empty string if the caller doesn't supply it.

There's not much going on in this shader.  

An LLVM ExtractElement instruction corresponds to SPIR-V OpCompositeExtract.
There are 5 uses of the latter in the generated SPIR-V disassembly.
The first is a very ordinary extraction of a scalar from a vec4f:

```
         %32 = OpCompositeExtract %float %30 1

```

The other 4 are in this code sequence:

```
        %_e5 = OpLoad %v3uint %g None
        %_e6 = OpVectorShuffle %v2uint %_e5 %_e5 2 2
         %69 = OpFunctionCall %void %f
         %70 = OpCompositeExtract %uint %_e6 0
         %71 = OpCompositeExtract %uint %_e6 0
         %72 = OpIMul %uint %70 %71
         %73 = OpCompositeExtract %uint %_e6 1
         %74 = OpCompositeExtract %uint %_e6 1
         %75 = OpIMul %uint %73 %74
         %76 = OpIAdd %uint %72 %75 

```

That corresponds to this part of the WGSL:

```
                  let _e6 =_e5.zz;
                  f();
                  switch dot(_e6, _e6) {

```

Instructions %70 through %76 implement the `dot(_e6, _e6)`. The `OpVectorShuffle` is the swizzle expression `_e5.zz`. It's all perfectly legal and looks ordinary?

### pe...@google.com (2024-11-19)

Setting milestone because of s0/s1 severity.

### ds...@chromium.org (2024-11-19)

Having the standalone reproducer that we can compile and run would be useful. Thanks.

### ds...@google.com (2024-11-19)

And, just to confirm, this is running on Vulkan, not Compat and OpenGL, correct?

### a7...@gmail.com (2024-11-19)

Attached a standalone reproducer and the tint-generated shader. Build the reproducer with:

`~/bin/android-ndk-r27/toolchains/llvm/prebuilt/linux-x86_64/bin/x86_64-linux-android35-clang++ --target=aarch64-linux-android35 -lvulkan standalone.cpp -o reproducer`

`adb push` the reproducer and the shader to /data/local/tmp and enable MTE with `adb shell setprop arm64.memtag.process.reproducer sync`.
Note that MTE must be enabled in the Developer Settings and requires a reboot. The reproducer will check if MTE is enabled and early-exists if found to be disabled.
Also note that `libc++_shared.so` must be in `/data/local/tmp`, I copied it from `~/bin/android-ndk-r27/toolchains/llvm/prebuilt/linux-x86_64/sysroot/usr/lib/aarch64-linux-android/libc++_shared.so` onto the device.

On the device, cd into /data/local/tmp and run `LD_LIBRARY_PATH=/data/local/tmp ./reproducer comp.spv`.
If all works as intended, the reproducer should crash with a segfault; `adb logcat` should log the MTE violation and the backtrace from the original report.

### a7...@gmail.com (2024-11-19)

Regarding the Vulkan/Compat/OpenGL question: about://gpu says "<Integrated GPU> Vulkan backend - Mali-G715".
If this is not what you wanted to know I'm a bit lost

### ds...@chromium.org (2024-11-20)

I've been trying to reproduce the crash in Chrome without success so far. I've tried on a Pixel 6, and a Pixel 9, with both Chrome 128 and Chrome 131. I have not seen a crash from chrome.

We also tried taking the provided `spv` file and running that on the device (both the Pixel 6 and Pixel 9) through the test runner `amber` and did not see any crashes (the runner times out due to a fence triggering because the input WGSL (and thus SPIR-V) has an illegal infinite loop in it).

### a7...@gmail.com (2024-11-21)

I haven't heard anything from ARM so far (except that they'll look into this). In the meantime, I tried a few things on two other devices.

##### Pixel 8a

Device: Pixel 8a   

Build: AP3A.241105.007   

Chrome: 130.0.6723.102   

libGLES\_mali.so: sha256sum 876d47ef8fdc65d2e5db07f324ad23f30f44499debaa4a52a9211240f36861fd \

The standalone reproducer works and crashes with an MTE violation, same backtrace as the initial report.
Attempting to run the html reproducer in chrome results in the backtrace at the end of this comment.

##### Pixel 8

Device: Pixel 8   

Build: AP3A.241105.007   

Chrome: 131.0.6778.39   

libGLES\_mali.so: sha256sum bdac41f4cd2dcdb4391c94d7308a67c77a5a79b09794b58085575da758b46ccd \

The standalone reproducer works and crashes with an MTE violation, same backtrace as the initial report.
I tried the html a couple of times, replacing the `256u` with smaller values (just in case there is caching). After like 10 attempts the device initiated a reboot without logging anything striking. I gave the html a few more tries and observed a crash due to a null-deref. The backtrace is at the end of the report.

##### Pixel 9 Pro XL

Device: Pixel 9 Pro XL   

Android build number: AP3A.241105.008   

Chrome: 130.0.6723.102   

libGLES\_mali.so: sha256sum b9bcb08777f8cb276f595dfa12052a59ebc1dd00ffc3ef1d7f79448725c63aba

Just for reference, the initial device with sha256sum of the crashing lib. Standalone reproducer and chrome backtrace as in the initial report.

##### Pixel 8a html in chrome:

```
11-21 07:04:56.237 19478 19478 F DEBUG   : Build fingerprint: 'google/akita/akita:15/AP3A.241105.007/12470370:user/release-keys'
11-21 07:04:56.237 19478 19478 F DEBUG   : Revision: 'MP1.0'
11-21 07:04:56.237 19478 19478 F DEBUG   : ABI: 'arm64'
11-21 07:04:56.237 19478 19478 F DEBUG   : Timestamp: 2024-11-21 07:04:56.062578902+0100
11-21 07:04:56.237 19478 19478 F DEBUG   : Process uptime: 10s
11-21 07:04:56.237 19478 19478 F DEBUG   : Cmdline: com.android.chrome:privileged_process2
11-21 07:04:56.237 19478 19478 F DEBUG   : pid: 19378, tid: 19393, name: CrGpuMain  >>> com.android.chrome:privileged_process2 <<<
11-21 07:04:56.237 19478 19478 F DEBUG   : uid: 10176
11-21 07:04:56.237 19478 19478 F DEBUG   : tagged_addr_ctrl: 000000000007fff1 (PR_TAGGED_ADDR_ENABLE, mask 0xfffe)
11-21 07:04:56.237 19478 19478 F DEBUG   : pac_enabled_keys: 000000000000000f (PR_PAC_APIAKEY, PR_PAC_APIBKEY, PR_PAC_APDAKEY, PR_PAC_APDBKEY)
11-21 07:04:56.237 19478 19478 F DEBUG   : signal 11 (SIGSEGV), code 1 (SEGV_MAPERR), fault addr 0x0000000000000008
11-21 07:04:56.237 19478 19478 F DEBUG   : Cause: null pointer dereference
11-21 07:04:56.237 19478 19478 F DEBUG   :     x0  0000000000000000  x1  0000000000000000  x2  000000712729c6f0  x3  0000000000000000
11-21 07:04:56.237 19478 19478 F DEBUG   :     x4  0000006f97be6c5c  x5  00000070272b5540  x6  0000000000000002  x7  0000006f97be65b8
11-21 07:04:56.237 19478 19478 F DEBUG   :     x8  0000000000000001  x9  000000000000ac7f  x10 000000713729ef68  x11 0000006fdf6fedf8
11-21 07:04:56.237 19478 19478 F DEBUG   :     x12 0000000000000020  x13 fffffffffffff000  x14 0000000000000001  x15 000000000000000b
11-21 07:04:56.237 19478 19478 F DEBUG   :     x16 0000006fe1cb6730  x17 00000072e66dab00  x18 0000006f97134000  x19 0000006f97be6c20
11-21 07:04:56.237 19478 19478 F DEBUG   :     x20 0000000000000000  x21 000000712729c6f0  x22 0000000000000000  x23 000000713729ef50
11-21 07:04:56.237 19478 19478 F DEBUG   :     x24 000000713729ef50  x25 0000006f97beaa80  x26 0000000000000047  x27 0000000000000000
11-21 07:04:56.237 19478 19478 F DEBUG   :     x28 00000071772bd670  x29 00000070272b5448
11-21 07:04:56.237 19478 19478 F DEBUG   :     lr  0000006fe1024408  sp  0000006f97be6a10  pc  0000006fe1957944  pst 0000000060001000
11-21 07:04:56.237 19478 19478 F DEBUG   : 49 total frames
11-21 07:04:56.237 19478 19478 F DEBUG   : backtrace:
11-21 07:04:56.237 19478 19478 F DEBUG   :       #00 pc 0000000002cfe944  /vendor/lib64/egl/libGLES_mali.so (llvm::Type::isSizedDerivedType(llvm::SmallPtrSetImpl<llvm::Type*>*) const+52) (BuildId: 7f26
8bb2ad047524)
11-21 07:04:56.237 19478 19478 F DEBUG   :       #01 pc 00000000023cb404  /vendor/lib64/egl/libGLES_mali.so ((anonymous namespace)::InstrScalarInfo::generateOperandsCommon(unsigned int, llvm::Value*, i
nt)+1012) (BuildId: 7f268bb2ad047524)
11-21 07:04:56.237 19478 19478 F DEBUG   :       #02 pc 00000000023c6f1c  /vendor/lib64/egl/libGLES_mali.so ((anonymous namespace)::InstrScalarInfo::generateOperands(llvm::ArrayRef<int>)+60) (BuildId: 7f268bb2ad047524)
11-21 07:04:56.237 19478 19478 F DEBUG   :       #03 pc 00000000023c44e8  /vendor/lib64/egl/libGLES_mali.so ((anonymous namespace)::MaliScalarizer::scalarize(llvm::Instruction*)+5176) (BuildId: 7f268bb2ad047524)
11-21 07:04:56.237 19478 19478 F DEBUG   :       #04 pc 00000000023c2654  /vendor/lib64/egl/libGLES_mali.so ((anonymous namespace)::MaliScalarizer::runOnFunction(llvm::Function&) (.03a141ad775a5f40f0ad2389a308d930)+1540) (BuildId: 7f268bb2ad047524)
11-21 07:04:56.237 19478 19478 F DEBUG   :       #05 pc 000000000234b56c  /vendor/lib64/egl/libGLES_mali.so ((anonymous namespace)::MaliFunctionPassManager::runOnModule(llvm::Module&) (.aeafa394eef5d85b5c8fdc1ceb23a163)+492) (BuildId: 7f268bb2ad047524)
11-21 07:04:56.237 19478 19478 F DEBUG   :       #06 pc 000000000234aa3c  /vendor/lib64/egl/libGLES_mali.so ((anonymous namespace)::MaliModulePassManager::runOnModule(llvm::Module&) (.aeafa394eef5d85b5c8fdc1ceb23a163)+412) (BuildId: 7f268bb2ad047524)
11-21 07:04:56.237 19478 19478 F DEBUG   :       #07 pc 000000000234677c  /vendor/lib64/egl/libGLES_mali.so (llvm::Mali::StaticPassManager::TLPassManagerImpl::run(llvm::Module&)+252) (BuildId: 7f268bb2ad047524)
11-21 07:04:56.237 19478 19478 F DEBUG   :       #08 pc 0000000001c5e1f4  /vendor/lib64/egl/libGLES_mali.so (cmpbep_bfr_run_llvm_backend+2100) (BuildId: 7f268bb2ad047524)
11-21 07:04:56.237 19478 19478 F DEBUG   :       #09 pc 0000000001c637fc  /vendor/lib64/egl/libGLES_mali.so (cmpbe_compile_gles_shader+700) (BuildId: 7f268bb2ad047524)
11-21 07:04:56.237 19478 19478 F DEBUG   :       #10 pc 0000000001c8781c  /vendor/lib64/egl/libGLES_mali.so (do_single_part2_compilation+204) (BuildId: 7f268bb2ad047524)
11-21 07:04:56.237 19478 19478 F DEBUG   :       #11 pc 0000000001c872f0  /vendor/lib64/egl/libGLES_mali.so (cmpbe_v2_compile_multiple_shaders+9536) (BuildId: 7f268bb2ad047524)
11-21 07:04:56.237 19478 19478 F DEBUG   :       #12 pc 0000000001b87790  /vendor/lib64/egl/libGLES_mali.so (gfx::compiler::compile_shaders(gfx::shader_set const&, gfx::shader_set&, hal::shader_language, gfx::shader_state const&, compiler_cache*, gfx::mem_allocator&, cutils_cmpbe_dump_ctx**, bool*, unsigned long*)+7152) (BuildId: 7f268bb2ad047524)
11-21 07:04:56.237 19478 19478 F DEBUG   :       #13 pc 0000000000923070  /vendor/lib64/egl/libGLES_mali.so (vkCreateComputePipelines+1984) (BuildId: 7f268bb2ad047524)
11-21 07:04:56.237 19478 19478 F DEBUG   :       #14 pc 0000000004f68e48  /data/app/~~CH_doHGMNfGupBc071OkgA==/com.google.android.trichromelibrary_672310233-Hab8_7zfbH-gWeJicHdvCw==/base.apk!libmonochrome_64.so (offset 0x8dc000) (BuildId: 77f8ff4f62cc8adf53e228d740ed66d6bdc3e250)
11-21 07:04:56.237 19478 19478 F DEBUG   :       #15 pc 0000000004f09eac  /data/app/~~CH_doHGMNfGupBc071OkgA==/com.google.android.trichromelibrary_672310233-Hab8_7zfbH-gWeJicHdvCw==/base.apk!libmonochrome_64.so (offset 0x8dc000) (BuildId: 77f8ff4f62cc8adf53e228d740ed66d6bdc3e250)
11-21 07:04:56.237 19478 19478 F DEBUG   :       #16 pc 0000000004ee2c34  /data/app/~~CH_doHGMNfGupBc071OkgA==/com.google.android.trichromelibrary_672310233-Hab8_7zfbH-gWeJicHdvCw==/base.apk!libmonochrome_64.so (offset 0x8dc000) (BuildId: 77f8ff4f62cc8adf53e228d740ed66d6bdc3e250)
11-21 07:04:56.237 19478 19478 F DEBUG   :       #17 pc 0000000004ee2a24  /data/app/~~CH_doHGMNfGupBc071OkgA==/com.google.android.trichromelibrary_672310233-Hab8_7zfbH-gWeJicHdvCw==/base.apk!libmonochrome_64.so (offset 0x8dc000) (BuildId: 77f8ff4f62cc8adf53e228d740ed66d6bdc3e250)
11-21 07:04:56.237 19478 19478 F DEBUG   :       #18 pc 0000000007c43518  /data/app/~~CH_doHGMNfGupBc071OkgA==/com.google.android.trichromelibrary_672310233-Hab8_7zfbH-gWeJicHdvCw==/base.apk!libmonochrome_64.so (offset 0x8dc000) (BuildId: 77f8ff4f62cc8adf53e228d740ed66d6bdc3e250)
11-21 07:04:56.237 19478 19478 F DEBUG   :       #19 pc 0000000007c4964c  /data/app/~~CH_doHGMNfGupBc071OkgA==/com.google.android.trichromelibrary_672310233-Hab8_7zfbH-gWeJicHdvCw==/base.apk!libmonochrome_64.so (offset 0x8dc000) (BuildId: 77f8ff4f62cc8adf53e228d740ed66d6bdc3e250)
11-21 07:04:56.237 19478 19478 F DEBUG   :       #20 pc 0000000007c0ab88  /data/app/~~CH_doHGMNfGupBc071OkgA==/com.google.android.trichromelibrary_672310233-Hab8_7zfbH-gWeJicHdvCw==/base.apk!libmonochrome_64.so (offset 0x8dc000) (BuildId: 77f8ff4f62cc8adf53e228d740ed66d6bdc3e250)
11-21 07:04:56.237 19478 19478 F DEBUG   :       #21 pc 0000000007c0ac2c  /data/app/~~CH_doHGMNfGupBc071OkgA==/com.google.android.trichromelibrary_672310233-Hab8_7zfbH-gWeJicHdvCw==/base.apk!libmonochrome_64.so (offset 0x8dc000) (BuildId: 77f8ff4f62cc8adf53e228d740ed66d6bdc3e250)
11-21 07:04:56.237 19478 19478 F DEBUG   :       #22 pc 0000000007c084d4  /data/app/~~CH_doHGMNfGupBc071OkgA==/com.google.android.trichromelibrary_672310233-Hab8_7zfbH-gWeJicHdvCw==/base.apk!libmonochrome_64.so (offset 0x8dc000) (BuildId: 77f8ff4f62cc8adf53e228d740ed66d6bdc3e250)
11-21 07:04:56.237 19478 19478 F DEBUG   :       #23 pc 000000000444ef8c  /data/app/~~CH_doHGMNfGupBc071OkgA==/com.google.android.trichromelibrary_672310233-Hab8_7zfbH-gWeJicHdvCw==/base.apk!libmonochrome_64.so (offset 0x8dc000) (BuildId: 77f8ff4f62cc8adf53e228d740ed66d6bdc3e250)
11-21 07:04:56.237 19478 19478 F DEBUG   :       #24 pc 000000000427ea34  /data/app/~~CH_doHGMNfGupBc071OkgA==/com.google.android.trichromelibrary_672310233-Hab8_7zfbH-gWeJicHdvCw==/base.apk!libmonochrome_64.so (offset 0x8dc000) (BuildId: 77f8ff4f62cc8adf53e228d740ed66d6bdc3e250)
11-21 07:04:56.237 19478 19478 F DEBUG   :       #25 pc 000000000427e798  /data/app/~~CH_doHGMNfGupBc071OkgA==/com.google.android.trichromelibrary_672310233-Hab8_7zfbH-gWeJicHdvCw==/base.apk!libmonochrome_64.so (offset 0x8dc000) (BuildId: 77f8ff4f62cc8adf53e228d740ed66d6bdc3e250)
11-21 07:04:56.237 19478 19478 F DEBUG   :       #26 pc 000000000427e684  /data/app/~~CH_doHGMNfGupBc071OkgA==/com.google.android.trichromelibrary_672310233-Hab8_7zfbH-gWeJicHdvCw==/base.apk!libmonochrome_64.so (offset 0x8dc000) (BuildId: 77f8ff4f62cc8adf53e228d740ed66d6bdc3e250)
11-21 07:04:56.237 19478 19478 F DEBUG   :       #27 pc 000000000427e5d0  /data/app/~~CH_doHGMNfGupBc071OkgA==/com.google.android.trichromelibrary_672310233-Hab8_7zfbH-gWeJicHdvCw==/base.apk!libmonochrome_64.so (offset 0x8dc000) (BuildId: 77f8ff4f62cc8adf53e228d740ed66d6bdc3e250)
11-21 07:04:56.237 19478 19478 F DEBUG   :       #28 pc 000000000444b50c  /data/app/~~CH_doHGMNfGupBc071OkgA==/com.google.android.trichromelibrary_672310233-Hab8_7zfbH-gWeJicHdvCw==/base.apk!libmonochrome_64.so (offset 0x8dc000) (BuildId: 77f8ff4f62cc8adf53e228d740ed66d6bdc3e250)
11-21 07:04:56.237 19478 19478 F DEBUG   :       #29 pc 000000000690d588  /data/app/~~CH_doHGMNfGupBc071OkgA==/com.google.android.trichromelibrary_672310233-Hab8_7zfbH-gWeJicHdvCw==/base.apk!libmonochrome_64.so (offset 0x8dc000) (BuildId: 77f8ff4f62cc8adf53e228d740ed66d6bdc3e250)
11-21 07:04:56.237 19478 19478 F DEBUG   :       #30 pc 0000000002b8c65c  /data/app/~~CH_doHGMNfGupBc071OkgA==/com.google.android.trichromelibrary_672310233-Hab8_7zfbH-gWeJicHdvCw==/base.apk!libmonochrome_64.so (offset 0x8dc000) (BuildId: 77f8ff4f62cc8adf53e228d740ed66d6bdc3e250)
11-21 07:04:56.237 19478 19478 F DEBUG   :       #31 pc 0000000002b7d548  /data/app/~~CH_doHGMNfGupBc071OkgA==/com.google.android.trichromelibrary_672310233-Hab8_7zfbH-gWeJicHdvCw==/base.apk!libmonochrome_64.so (offset 0x8dc000) (BuildId: 77f8ff4f62cc8adf53e228d740ed66d6bdc3e250)
11-21 07:04:56.237 19478 19478 F DEBUG   :       #32 pc 0000000002b7d060  /data/app/~~CH_doHGMNfGupBc071OkgA==/com.google.android.trichromelibrary_672310233-Hab8_7zfbH-gWeJicHdvCw==/base.apk!libmonochrome_64.so (offset 0x8dc000) (BuildId: 77f8ff4f62cc8adf53e228d740ed66d6bdc3e250)
11-21 07:04:56.237 19478 19478 F DEBUG   :       #33 pc 000000000426af28  /data/app/~~CH_doHGMNfGupBc071OkgA==/com.google.android.trichromelibrary_672310233-Hab8_7zfbH-gWeJicHdvCw==/base.apk!libmonochrome_64.so (offset 0x8dc000) (BuildId: 77f8ff4f62cc8adf53e228d740ed66d6bdc3e250)
11-21 07:04:56.237 19478 19478 F DEBUG   :       #34 pc 0000000002b55560  /data/app/~~CH_doHGMNfGupBc071OkgA==/com.google.android.trichromelibrary_672310233-Hab8_7zfbH-gWeJicHdvCw==/base.apk!libmonochrome_64.so (offset 0x8dc000) (BuildId: 77f8ff4f62cc8adf53e228d740ed66d6bdc3e250)
11-21 07:04:56.237 19478 19478 F DEBUG   :       #35 pc 0000000002be0a10  /data/app/~~CH_doHGMNfGupBc071OkgA==/com.google.android.trichromelibrary_672310233-Hab8_7zfbH-gWeJicHdvCw==/base.apk!libmonochrome_64.so (offset 0x8dc000) (BuildId: 77f8ff4f62cc8adf53e228d740ed66d6bdc3e250)
11-21 07:04:56.237 19478 19478 F DEBUG   :       #36 pc 0000000002b6f20c  /data/app/~~CH_doHGMNfGupBc071OkgA==/com.google.android.trichromelibrary_672310233-Hab8_7zfbH-gWeJicHdvCw==/base.apk!libmonochrome_64.so (offset 0x8dc000) (BuildId: 77f8ff4f62cc8adf53e228d740ed66d6bdc3e250)
11-21 07:04:56.237 19478 19478 F DEBUG   :       #37 pc 0000000002b51368  /data/app/~~CH_doHGMNfGupBc071OkgA==/com.google.android.trichromelibrary_672310233-Hab8_7zfbH-gWeJicHdvCw==/base.apk!libmonochrome_64.so (offset 0x8dc000) (Java_J_N__1I_1Z+296) (BuildId: 77f8ff4f62cc8adf53e228d740ed66d6bdc3e250)
11-21 07:04:56.237 19478 19478 F DEBUG   :       #38 pc 00000000000a0110  /system/framework/arm64/boot.oat (art_jni_trampoline+112) (BuildId: 59f4d29f747a3d5e404718071bba0cc8abfd77fa)
11-21 07:04:56.237 19478 19478 F DEBUG   :       #39 pc 000000000077e408  /apex/com.android.art/lib64/libart.so (nterp_helper+152) (BuildId: dcb9fe2b5c99aa3f1a682a6008427d08)
11-21 07:04:56.237 19478 19478 F DEBUG   :       #40 pc 00000000000d1590  /data/app/~~FleaNZCT9ggEcltKh_FUpg==/com.android.chrome-IaELQ-2xG6XPUsP2YWSxLw==/base.apk (BV.run+456)
11-21 07:04:56.237 19478 19478 F DEBUG   :       #41 pc 0000000000155120  /system/framework/arm64/boot.oat (java.lang.Thread.run+64) (BuildId: 59f4d29f747a3d5e404718071bba0cc8abfd77fa)
11-21 07:04:56.237 19478 19478 F DEBUG   :       #42 pc 0000000000362774  /apex/com.android.art/lib64/libart.so (art_quick_invoke_stub+612) (BuildId: dcb9fe2b5c99aa3f1a682a6008427d08)
11-21 07:04:56.237 19478 19478 F DEBUG   :       #43 pc 000000000034def0  /apex/com.android.art/lib64/libart.so (art::ArtMethod::Invoke(art::Thread*, unsigned int*, unsigned int, art::JValue*, char const*)+132) (BuildId: dcb9fe2b5c99aa3f1a682a6008427d08)
11-21 07:04:56.237 19478 19478 F DEBUG   :       #44 pc 00000000009430d8  /apex/com.android.art/lib64/libart.so (art::detail::ShortyTraits<(char)86>::Type art::ArtMethod::InvokeInstance<(char)86>(art::Thread*, art::ObjPtr<art::mirror::Object>, art::detail::ShortyTraits<>::Type...)+60) (BuildId: dcb9fe2b5c99aa3f1a682a6008427d08)
11-21 07:04:56.237 19478 19478 F DEBUG   :       #45 pc 000000000063e694  /apex/com.android.art/lib64/libart.so (art::Thread::CreateCallback(void*)+1344) (BuildId: dcb9fe2b5c99aa3f1a682a6008427d08)
11-21 07:04:56.237 19478 19478 F DEBUG   :       #46 pc 000000000063e144  /apex/com.android.art/lib64/libart.so (art::Thread::CreateCallbackWithUffdGc(void*)+8) (BuildId: dcb9fe2b5c99aa3f1a682a6008427d08)
11-21 07:04:56.237 19478 19478 F DEBUG   :       #47 pc 000000000006f718  /apex/com.android.runtime/lib64/bionic/libc.so (__pthread_start(void*)+200) (BuildId: 32a42812c629603f9b8fb44bd931166b)
11-21 07:04:56.237 19478 19478 F DEBUG   :       #48 pc 0000000000060e00  /apex/com.android.runtime/lib64/bionic/libc.so (__start_thread+64) (BuildId: 32a42812c629603f9b8fb44bd931166b)
11-21 07:04:56.257  1650 19482 I DropBoxManagerService: add tag=system_app_native_crash isTagEnabled=true flags=0x2
11-21 07:04:56.260  1650  1898 I DropBoxManagerService: add tag=SYSTEM_TOMBSTONE_PROTO_WITH_HEADERS isTagEnabled=true flags=0x4
11-21 07:04:56.261   709   709 E tombstoned: Tombstone written to: tombstone_09

```
##### Pixel 8 html in chrome

```
11-21 07:39:05.395 23733 23733 F DEBUG   : Build fingerprint: 'google/shiba/shiba:15/AP3A.241105.007/12470370:user/release-keys'
11-21 07:39:05.395 23733 23733 F DEBUG   : Revision: 'MP1.0'
11-21 07:39:05.395 23733 23733 F DEBUG   : ABI: 'arm64'
11-21 07:39:05.395 23733 23733 F DEBUG   : Timestamp: 2024-11-21 07:39:04.839679558+0100
11-21 07:39:05.395 23733 23733 F DEBUG   : Process uptime: 166s
11-21 07:39:05.395 23733 23733 F DEBUG   : Cmdline: com.android.chrome:privileged_process0
11-21 07:39:05.395 23733 23733 F DEBUG   : pid: 23287, tid: 23305, name: CrGpuMain  >>> com.android.chrome:privileged_process0 <<<
11-21 07:39:05.395 23733 23733 F DEBUG   : uid: 10189
11-21 07:39:05.395 23733 23733 F DEBUG   : tagged_addr_ctrl: 000000000007fff1 (PR_TAGGED_ADDR_ENABLE, mask 0xfffe)
11-21 07:39:05.395 23733 23733 F DEBUG   : pac_enabled_keys: 000000000000000f (PR_PAC_APIAKEY, PR_PAC_APIBKEY, PR_PAC_APDAKEY, PR_PAC_APDBKEY)
11-21 07:39:05.395 23733 23733 F DEBUG   : signal 11 (SIGSEGV), code 1 (SEGV_MAPERR), fault addr 0x0000000000000008
11-21 07:39:05.395 23733 23733 F DEBUG   : Cause: null pointer dereference
11-21 07:39:05.395 23733 23733 F DEBUG   :     x0  0000000000000000  x1  0000000000000000  x2  0000007106a79510  x3  0000000000000000
11-21 07:39:05.395 23733 23733 F DEBUG   :     x4  000000704ba2dd0c  x5  0000007226a858a0  x6  706f6f6c2e6d766c  x7  0000007092b23896
11-21 07:39:05.395 23733 23733 F DEBUG   :     x8  0000000000000001  x9  000000000000ac7f  x10 00000072a6a69e68  x11 00000070934def18
11-21 07:39:05.395 23733 23733 F DEBUG   :     x12 0000000000000020  x13 fffffffffffff000  x14 0000000000000001  x15 0000000000000033
11-21 07:39:05.395 23733 23733 F DEBUG   :     x16 0000007095a96738  x17 0000007383adba40  x18 000000704a314000  x19 000000704ba2dcd0
11-21 07:39:05.395 23733 23733 F DEBUG   :     x20 0000000000000000  x21 0000007106a79510  x22 00000
00000000000  x23 00000072a6a69e50
11-21 07:39:05.395 23733 23733 F DEBUG   :     x24 00000072a6a69e50  x25 000000704ba31a80  x26 0000000000000047  x27 0000000000000000
11-21 07:39:05.395 23733 23733 F DEBUG   :     x28 0000007216a7f440  x29 0000007226a857a8
11-21 07:39:05.395 23733 23733 F DEBUG   :     lr  0000007094e04d98  sp  000000704ba2dac0  pc  00000070957382d4  pst 0000000060001000
11-21 07:39:05.395 23733 23733 F DEBUG   : 49 total frames
11-21 07:39:05.395 23733 23733 F DEBUG   : backtrace:
11-21 07:39:05.396 23733 23733 F DEBUG   :       #00 pc 0000000002cff2d4  /vendor/lib64/egl/libGLES_mali.so (llvm::Type::isSizedDerivedType(llvm::SmallPtrSetImpl<llvm::Type*>*) const+52) (BuildId: f4d514cc662b18fe)
11-21 07:39:05.396 23733 23733 F DEBUG   :       #01 pc 00000000023cbd94  /vendor/lib64/egl/libGLES_mali.so ((anonymous namespace)::InstrScalarInfo::generateOperandsCommon(unsigned int, llvm::Value*, int)+1012) (BuildId: f4d514cc662b18fe)
11-21 07:39:05.396 23733 23733 F DEBUG   :       #02 pc 00000000023c78ac  /vendor/lib64/egl/libGLES_mali.so ((anonymous namespace)::InstrScalarInfo::generateOperands(llvm::ArrayRef<int>)+60) (BuildId: f4d514cc662b18fe)
11-21 07:39:05.396 23733 23733 F DEBUG   :       #03 pc 00000000023c4e78  /vendor/lib64/egl/libGLES_mali.so ((anonymous namespace)::MaliScalarizer::scalarize(llvm::Instruction*)+5176) (BuildId: f4d514cc662b18fe)
11-21 07:39:05.396 23733 23733 F DEBUG   :       #04 pc 00000000023c2fe4  /vendor/lib64/egl/libGLES_mali.so ((anonymous namespace)::MaliScalarizer::runOnFunction(llvm::Function&)+1540) (BuildId: f4d514cc662b18fe)
11-21 07:39:05.396 23733 23733 F DEBUG   :       #05 pc 000000000234befc  /vendor/lib64/egl/libGLES_mali.so ((anonymous namespace)::MaliFunctionPassManager::runOnModule(llvm::Module&)+492) (BuildId: f4d514cc662b18fe)
11-21 07:39:05.396 23733 23733 F DEBUG   :       #06 pc 000000000234b3cc  /vendor/lib64/egl/libGLES_mali.so ((anonymous namespace)::MaliModulePassManager::runOnModule(llvm::Module&)+412) (BuildId: f4d514cc662b18fe)
11-21 07:39:05.396 23733 23733 F DEBUG   :       #07 pc 000000000234710c  /vendor/lib64/egl/libGLES_mali.so (llvm::Mali::StaticPassManager::TLPassManagerImpl::run(llvm::Module&)+252) (BuildId: f4d514cc662b18fe)
11-21 07:39:05.396 23733 23733 F DEBUG   :       #08 pc 0000000001c5eb64  /vendor/lib64/egl/libGLES_mali.so (cmpbep_bfr_run_llvm_backend+2100) (BuildId: f4d514cc662b18fe)
11-21 07:39:05.396 23733 23733 F DEBUG   :       #09 pc 0000000001c6416c  /vendor/lib64/egl/libGLES_mali.so (cmpbe_compile_gles_shader+700) (BuildId: f4d514cc662b18fe)
11-21 07:39:05.396 23733 23733 F DEBUG   :       #10 pc 0000000001c8818c  /vendor/lib64/egl/libGLES_mali.so (do_single_part2_compilation+204) (BuildId: f4d514cc662b18fe)
11-21 07:39:05.396 23733 23733 F DEBUG   :       #11 pc 0000000001c87c60  /vendor/lib64/egl/libGLES_mali.so (cmpbe_v2_compile_multiple_shaders+9536) (BuildId: f4d514cc662b18fe)
11-21 07:39:05.396 23733 23733 F DEBUG   :       #12 pc 0000000001b878b0  /vendor/lib64/egl/libGLES_mali.so (gfx::compiler::compile_shaders(gfx::shader_set const&, gfx::shader_set&, hal::shader_language, gfx::shader_state const&, compiler_cache*, gfx::mem_allocator&, cutils_cmpbe_dump_ctx**, bool*, unsigned long*)+7152) (BuildId: f4d514cc662b18fe)
11-21 07:39:05.396 23733 23733 F DEBUG   :       #13 pc 0000000000923070  /vendor/lib64/egl/libGLES_mali.so (vkCreateComputePipelines+1984) (BuildId: f4d514cc662b18fe)
11-21 07:39:05.396 23733 23733 F DEBUG   :       #14 pc 0000000004e91d60  /data/app/~~63LjocmR8aMxeGbZC8Y7lQ==/com.google.android.trichromelibrary_677803933-7mI16VWrYKKUoPG96sSnyA==/base.apk!libmonochrome_64.so (offset 0x8dc000) (BuildId: b447567fc3d6e547a5afd08a2514ae9f30ef57a8)
11-21 07:39:05.396 23733 23733 F DEBUG   :       #15 pc 0000000004e34bb4  /data/app/~~63LjocmR8aMxeGbZC8Y7lQ==/com.google.android.trichromelibrary_677803933-7mI16VWrYKKUoPG96sSnyA==/base.apk!libmonochrome_64.so (offset 0x8dc000) (BuildId: b447567fc3d6e547a5afd08a2514ae9f30ef57a8)
11-21 07:39:05.396 23733 23733 F DEBUG   :       #16 pc 0000000004e0eea4  /data/app/~~63LjocmR8aMxeGbZC8Y7lQ==/com.google.android.trichromelibrary_677803933-7mI16VWrYKKUoPG96sSnyA==/base.apk!libmonochrome_64.so (offset 0x8dc000) (BuildId: b447567fc3d6e547a5afd08a2514ae9f30ef57a8)
11-21 07:39:05.396 23733 23733 F DEBUG   :       #17 pc 0000000004e0ec88  /data/app/~~63LjocmR8aMxeGbZC8Y7lQ==/com.google.android.trichromelibrary_677803933-7mI16VWrYKKUoPG96sSnyA==/base.apk!libmonochrome_64.so (offset 0x8dc000) (BuildId: b447567fc3d6e547a5afd08a2514ae9f30ef57a8)
11-21 07:39:05.396 23733 23733 F DEBUG   :       #18 pc 0000000007b5af58  /data/app/~~63LjocmR8aMxeGbZC8Y7lQ==/com.google.android.trichromelibrary_677803933-7mI16VWrYKKUoPG96sSnyA==/base.apk!libmonochrome_64.so (offset 0x8dc000) (BuildId: b447567fc3d6e547a5afd08a2514ae9f30ef57a8)
11-21 07:39:05.396 23733 23733 F DEBUG   :       #19 pc 0000000007b60c34  /data/app/~~63LjocmR8aMxeGbZC8Y7lQ==/com.google.android.trichromelibrary_677803933-7mI16VWrYKKUoPG96sSnyA==/base.apk!libmonochrome_64.so (offset 0x8dc000) (BuildId: b447567fc3d6e547a5afd08a2514ae9f30ef57a8)
11-21 07:39:05.396 23733 23733 F DEBUG   :       #20 pc 0000000007b23654  /data/app/~~63LjocmR8aMxeGbZC8Y7lQ==/com.google.android.trichromelibrary_677803933-7mI16VWrYKKUoPG96sSnyA==/base.apk!libmonochrome_64.so (offset 0x8dc000) (BuildId: b447567fc3d6e547a5afd08a2514ae9f30ef57a8)
11-21 07:39:05.396 23733 23733 F DEBUG   :       #21 pc 0000000007b236f8  /data/app/~~63LjocmR8aMxeGbZC8Y7lQ==/com.google.android.trichromelibrary_677803933-7mI16VWrYKKUoPG96sSnyA==/base.apk!libmonochrome_64.so (offset 0x8dc000) (BuildId: b447567fc3d6e547a5afd08a2514ae9f30ef57a8)
11-21 07:39:05.396 23733 23733 F DEBUG   :       #22 pc 0000000007b212d0  /data/app/~~63LjocmR8aMxeGbZC8Y7lQ==/com.google.android.trichromelibrary_677803933-7mI16VWrYKKUoPG96sSnyA==/base.apk!libmonochrome_64.so (offset 0x8dc000) (BuildId: b447567fc3d6e547a5afd08a2514ae9f30ef57a8)
11-21 07:39:05.396 23733 23733 F DEBUG   :       #23 pc 00000000043c5884  /data/app/~~63LjocmR8aMxeGbZC8Y7lQ==/com.google.android.trichromelibrary_677803933-7mI16VWrYKKUoPG96sSnyA==/base.apk!libmonochrome_64.so (offset 0x8dc000) (BuildId: b447567fc3d6e547a5afd08a2514ae9f30ef57a8)
11-21 07:39:05.396 23733 23733 F DEBUG   :       #24 pc 00000000043c4fd8  /data/app/~~63LjocmR8aMxeGbZC8Y7lQ==/com.google.android.trichromelibrary_677803933-7mI16VWrYKKUoPG96sSnyA==/base.apk!libmonochrome_64.so (offset 0x8dc000) (BuildId: b447567fc3d6e547a5afd08a2514ae9f30ef57a8)
11-21 07:39:05.396 23733 23733 F DEBUG   :       #25 pc 00000000043c4cf4  /data/app/~~63LjocmR8aMxeGbZC8Y7lQ==/com.google.android.trichromelibrary_677803933-7mI16VWrYKKUoPG96sSnyA==/base.apk!libmonochrome_64.so (offset 0x8dc000) (BuildId: b447567fc3d6e547a5afd08a2514ae9f30ef57a8)
11-21 07:39:05.396 23733 23733 F DEBUG   :       #26 pc 00000000043c4be0  /data/app/~~63LjocmR8aMxeGbZC8Y7lQ==/com.google.android.trichromelibrary_677803933-7mI16VWrYKKUoPG96sSnyA==/base.apk!libmonochrome_64.so (offset 0x8dc000) (BuildId: b447567fc3d6e547a5afd08a2514ae9f30ef57a8)
11-21 07:39:05.396 23733 23733 F DEBUG   :       #27 pc 00000000043c4b2c  /data/app/~~63LjocmR8aMxeGbZC8Y7lQ==/com.google.android.trichromelibrary_677803933-7mI16VWrYKKUoPG96sSnyA==/base.apk!libmonochrome_64.so (offset 0x8dc000) (BuildId: b447567fc3d6e547a5afd08a2514ae9f30ef57a8)
11-21 07:39:05.396 23733 23733 F DEBUG   :       #28 pc 00000000043b530c  /data/app/~~63LjocmR8aMxeGbZC8Y7lQ==/com.google.android.trichromelibrary_677803933-7mI16VWrYKKUoPG96sSnyA==/base.apk!libmonochrome_64.so (offset 0x8dc000) (BuildId: b447567fc3d6e547a5afd08a2514ae9f30ef57a8)
11-21 07:39:05.396 23733 23733 F DEBUG   :       #29 pc 0000000006838610  /data/app/~~63LjocmR8aMxeGbZC8Y7lQ==/com.google.android.trichromelibrary_677803933-7mI16VWrYKKUoPG96sSnyA==/base.apk!libmonochrome_64.so (offset 0x8dc000) (BuildId: b447567fc3d6e547a5afd08a2514ae9f30ef57a8)
11-21 07:39:05.396 23733 23733 F DEBUG   :       #30 pc 0000000003282b14  /data/app/~~63LjocmR8aMxeGbZC8Y7lQ==/com.google.android.trichromelibrary_677803933-7mI16VWrYKKUoPG96sSnyA==/base.apk!libmonochrome_64.so (offset 0x8dc000) (BuildId: b447567fc3d6e547a5afd08a2514ae9f30ef57a8)
11-21 07:39:05.396 23733 23733 F DEBUG   :       #31 pc 000000000317124c  /data/app/~~63LjocmR8aMxeGbZC8Y7lQ==/com.google.android.trichromelibrary_677803933-7mI16VWrYKKUoPG96sSnyA==/base.apk!libmonochrome_64.so (offset 0x8dc000) (BuildId: b447567fc3d6e547a5afd08a2514ae9f30ef57a8)
11-21 07:39:05.396 23733 23733 F DEBUG   :       #32 pc 0000000003170d48  /data/app/~~63LjocmR8aMxeGbZC8Y7lQ==/com.google.android.trichromelibrary_677803933-7mI16VWrYKKUoPG96sSnyA==/base.apk!libmonochrome_64.so (offset 0x8dc000) (BuildId: b447567fc3d6e547a5afd08a2514ae9f30ef57a8)
11-21 07:39:05.396 23733 23733 F DEBUG   :       #33 pc 0000000004203d34  /data/app/~~63LjocmR8aMxeGbZC8Y7lQ==/com.google.android.trichromelibrary_677803933-7mI16VWrYKKUoPG96sSnyA==/base.apk!libmonochrome_64.so (offset 0x8dc000) (BuildId: b447567fc3d6e547a5afd08a2514ae9f30ef57a8)
11-21 07:39:05.396 23733 23733 F DEBUG   :       #34 pc 00000000031a1608  /data/app/~~63LjocmR8aMxeGbZC8Y7lQ==/com.google.android.trichromelibrary_677803933-7mI16VWrYKKUoPG96sSnyA==/base.apk!libmonochrome_64.so (offset 0x8dc000) (BuildId: b447567fc3d6e547a5afd08a2514ae9f30ef57a8)
11-21 07:39:05.396 23733 23733 F DEBUG   :       #35 pc 000000000312c454  /data/app/~~63LjocmR8aMxeGbZC8Y7lQ==/com.google.android.trichromelibrary_677803933-7mI16VWrYKKUoPG96sSnyA==/base.apk!libmonochrome_64.so (offset 0x8dc000) (BuildId: b447567fc3d6e547a5afd08a2514ae9f30ef57a8)
11-21 07:39:05.396 23733 23733 F DEBUG   :       #36 pc 000000000313b254  /data/app/~~63LjocmR8aMxeGbZC8Y7lQ==/com.google.android.trichromelibrary_677803933-7mI16VWrYKKUoPG96sSnyA==/base.apk!libmonochrome_64.so (offset 0x8dc000) (BuildId: b447567fc3d6e547a5afd08a2514ae9f30ef57a8)
11-21 07:39:05.396 23733 23733 F DEBUG   :       #37 pc 0000000003128814  /data/app/~~63LjocmR8aMxeGbZC8Y7lQ==/com.google.android.trichromelibrary_677803933-7mI16VWrYKKUoPG96sSnyA==/base.apk!libmonochrome_64.so (offset 0x8dc000) (Java_J_N__1I_1Z+296) (BuildId: b447567fc3d6e547a5afd08a2514ae9f30ef57a8)
11-21 07:39:05.396 23733 23733 F DEBUG   :       #38 pc 00000000003181a0  /data/misc/apexdata/com.android.art/dalvik-cache/arm64/boot.oat (art_jni_trampoline+112)
11-21 07:39:05.396 23733 23733 F DEBUG   :       #39 pc 000000000077eb08  /apex/com.android.art/lib64/libart.so (nterp_helper+152) (BuildId: 3f7d5a016e08d528f129bdd336d81168)
11-21 07:39:05.396 23733 23733 F DEBUG   :       #40 pc 00000000000d2678  /data/app/~~rsDfZSJ0axDWLacI7sDu7Q==/com.android.chrome-s8j26bmHT2kPzGkFN67oIg==/base.apk (YV.run+456)
11-21 07:39:05.396 23733 23733 F DEBUG   :       #41 pc 00000000003edf30  /data/misc/apexdata/com.android.art/dalvik-cache/arm64/boot.oat (java.lang.Thread.run+64)
11-21 07:39:05.396 23733 23733 F DEBUG   :       #42 pc 000000000036db74  /apex/com.android.art/lib64/libart.so (art_quick_invoke_stub+612) (BuildId: 3f7d5a016e08d528f129bdd336d81168)
11-21 07:39:05.396 23733 23733 F DEBUG   :       #43 pc 0000000000359324  /apex/com.android.art/lib64/libart.so (art::ArtMethod::Invoke(art::Thread*, unsigned int*, unsigned int, art::JValue*, char const*)+132) (BuildId: 3f7d5a016e08d528f129bdd336d81168)
11-21 07:39:05.396 23733 23733 F DEBUG   :       #44 pc 0000000000944438  /apex/com.android.art/lib64/libart.so (art::detail::ShortyTraits<(char)86>::Type art::ArtMethod::InvokeInstance<(char)86>(art::Thread*, art::ObjPtr<art::mirror::Object>, art::detail::ShortyTraits<>::Type...)+60) (BuildId: 3f7d5a016e08d528f129bdd336d81168)
11-21 07:39:05.396 23733 23733 F DEBUG   :       #45 pc 00000000006209f4  /apex/com.android.art/lib64/libart.so (art::Thread::CreateCallback(void*)+1344) (BuildId: 3f7d5a016e08d528f129bdd336d81168)
11-21 07:39:05.396 23733 23733 F DEBUG   :       #46 pc 00000000006204a4  /apex/com.android.art/lib64/libart.so (art::Thread::CreateCallbackWithUffdGc(void*)+8) (BuildId: 3f7d5a016e08d528f129bdd336d81168)
11-21 07:39:05.396 23733 23733 F DEBUG   :       #47 pc 0000000000070098  /apex/com.android.runtime/lib64/bionic/libc.so (__pthread_start(void*)+200) (BuildId: 119138cdca21ff059fa688b61b44fa46)
11-21 07:39:05.396 23733 23733 F DEBUG   :       #48 pc 0000000000061410  /apex/com.android.runtime/lib64/bionic/libc.so (__start_thread+64) (BuildId: 119138cdca21ff059fa688b61b44fa46)
11-21 07:39:05.422   665   665 E tombstoned: Tombstone written to: tombstone_16
11-21 07:39:05.427 14472 23737 I DropBoxManagerService: add tag=system_app_native_crash isTagEnabled=true flags=0x2
11-21 07:39:05.429 14472 14532 D CompatChangeReporter: Compat change id reported: 296060945; UID 10165; state: ENABLED
11-21 07:39:05.440 14472 14660 I DropBoxManagerService: add tag=SYSTEM_TOMBSTONE_PROTO_WITH_HEADERS isTagEnabled=true flags=0x4
11-21 07:39:05.524 14472 14660 I BootReceiver: Copying /data/tombstones/tombstone_16 to DropBox (SYSTEM_TOMBSTONE)
11-21 07:39:05.525 14472 14660 I DropBoxManagerService: add tag=SYSTEM_TOMBSTONE isTagEnabled=true flags=0x6
11-21 07:39:05.548 23198 23198 E chromium: [ERROR:gpu_process_host.cc(982)] GPU process exited unexpectedly: exit_code=0
11-21 07:39:05.548 23198 23198 W chromium: [WARNING:gpu_process_host.cc(1416)] The GPU process has crashed 1 time(s)
11-21 07:39:05.548 14472 16291 I ActivityManager: Process com.android.chrome:privileged_process0 (pid 23287) has died: fg  BTOP
11-21 07:39:05.548   622   622 W powerhal-libperfmgr: sched_setattr failed for thread 23305, err=3
11-21 07:39:05.548 23198 23237 W cr_ChildProcessConn: onServiceDisconnected (crash or killed by oom): pid=23287 bindings:W  S
11-21 07:39:05.549   622   622 W powerhal-libperfmgr: sched_setattr failed for thread 23349, err=3
11-21 07:39:05.549 23198 23198 W chromium: [WARNING:compositor_view.cc(344)] Child process died (type=9) pid=23287)
11-21 07:39:05.549   622   622 W powerhal-libperfmgr: sched_setattr failed for thread 23351, err=3
11-21 07:39:05.549 14472 16291 W ActivityManager: Scheduling restart of crashed service com.android.chrome/org.chromium.content.app.PrivilegedProcessService0 in 1000ms for connection
11-21 07:39:05.550 14359 14359 I Zygote  : Process 23287 exited due to signal 11 (Segmentation fault)
11-21 07:39:05.552 23198 23198 E chromium: [ERROR:command_buffer_proxy_impl.cc(331)] GPU state invalid after WaitForGetOffsetInRange.
11-21 07:39:05.552 14472 14557 I libprocessgroup: Removed cgroup /sys/fs/cgroup/uid_10189/pid_23287
11-21 07:39:05.553 23279 23318 E chromium: [ERROR:command_buffer_proxy_impl.cc(131)] ContextResult::kTransientFailure: Failed to send GpuControl.CreateCommandBuffer.
11-21 07:39:05.556 23198 23258 E chromium: [ERROR:directory_reader_posix.cc(43)] opendir /data/user/0/com.android.chrome/cache/Crashpad/attachments/c5e864d7-ec7a-4d87-a8a6-0d07af686047: No such file or directory (2)
11-21 07:39:05.565 14472 15055 V GrammaticalInflectionUtils: AttributionSource: android.content.AttributionSource@53f78f6b does not have READ_SYSTEM_GRAMMATICAL_GENDER permission.
11-21 07:39:05.589 23198 23258 I cr_LogcatCrashExtractor: Trying to extract logcat for minidump c5e864d7-ec7a-4d87-a8a6-0d07af686047.dmp23287.
11-21 07:39:05.600 14359 14359 D Zygote  : Forked child process 23740
11-21 07:39:05.602 14472 14556 I ActivityManager: Start proc 23740:com.android.chrome:privileged_process1/u0a189 for service {com.android.chrome/org.chromium.content.app.PrivilegedProcessService1}
11-21 07:39:05.618 23740 23740 I ileged_process1: Using CollectorTypeCMC GC.
11-21 07:39:05.621 23740 23740 E ileged_process1: Not starting debugger since process cannot load the jdwp agent.
11-21 07:39:05.625 23740 23740 D nativeloader: Load libframework-connectivity-tiramisu-jni.so using APEX ns com_android_tethering for caller /apex/com.android.tethering/javalib/framework-connectivity-t.jar: ok
11-21 07:39:05.636 14472 15055 D OomAdjuster: Not killing cached processes

```

### ds...@google.com (2024-11-21)

Hm, the two stacks in the last comment appear to be a different code path in LLVM then the one in the original report. They look like a different part of the system crashed.

### ds...@google.com (2024-11-21)

In the attached HTML file, the compute shader is an infinite loop which isn't permitted in WGSL. Can you modify the loop in the compute shader so it terminates and see if the issue persists?

### a7...@gmail.com (2024-11-21)

ARM just stated that their investigation is ongoing.

If I correctly understand the WGSL, function `f()` does contain 2 loops, none of them infinite. The single loop in `main()` is infinite, I patched it s.t. it iterates a finite amount of times. The attached html should now be free of infinite loops. In the standalone reproducer, the MTE violation persists deterministically. In Chrome, the crash is flaky; I successively incremented the exit condition in `break if iter > 20041;` from 20000 all the way to 20041 until I observed the first crash.

### a7...@gmail.com (2024-11-26)

Update from ARM:

> Hi XXX,
> 
> We've reproduced a problem in the Mali shader compiler triggered by the SPIR-V shader on our latest development compiler, and are investigating the impact and fix. We're not sure why it doesn't reproduce on Pixel 6 / Pixel 9, as the bug has been present for some time now.
> 
> We hope to come back to you again in about a week's time on the result of our security assessment.
> 
> In the meantime, has Google come back to you about whether it reproduces on all of their Mali devices, including Pixel 6 and Pixel 9?
> Many thanks,
> 
> XXX
> 
> Arm PSIRT

The question regarding Pixel 6 + 9 is directed at [comment #13](https://issues.chromium.org/issues/379551588#comment13) which I provided to Arm PSIRT.

### ds...@google.com (2024-11-26)

I spent some more time this morning in Chrome trying to re-produce the crash to no success. I tried flipping on various GPU related flags to see if they did anything, but even after reloading the new file probably a hundred times every load completed successfully.

### a7...@gmail.com (2024-11-26)

It shouldn't take that many attempts. When looking for a crash, did you observe the output of `adb logcat` or have you been looking for Aw, Snap? The latter is not expected to happen (as the GPU process should crash, not a renderer).

### ds...@chromium.org (2024-11-26)

I was watching `adb logcat` and didn't see anything crash related when reloading.

### a7...@gmail.com (2024-11-26)

Arm is working on the underlying issue, so the vital part is progressing. How important is the reproduction of the crash to you? I'm pretty much out of ideas on what else to do, considering that I tried it on three devices.

And one more question: Is there a way to detect that Pixel devices have been updated to a fixed shader compiler version (once Arm makes a patch available)? I would like to re-run the remaining fuzz findings with a patched version.

### ds...@chromium.org (2024-11-26)

We tried on a pixel 8 pro here as well and were unable to get chrome to crash. We checked the build number on your pixel 9 pro matches my pixel 9, so should be the same build setup. Are the devices you're running on rooted or am I missing a setting to get the crash to show up in `adb logcat`?

### ds...@chromium.org (2024-11-26)

As to the importance, I was trying to determine if we needed to workaround something in the Tint compiler, but given I can't repro, we resorted to reading the SPIR-V and the WGSL output and it all seems to be correct from our standpoint. Unless there is something the ARM folks can point us too that we could change in the generated SPIR-V, I'm not sure what we can do on the Chrome side.

### a7...@gmail.com (2024-11-26)

The Pixel 8a is rooted, the Pixel 8 and the Pixel 9 Pro XL are not rooted. The only difference from a vanilla installation I can come up with is that I (1) enabled Developer Settings and (2) enabled MTE. AFAIK this shouldn't impact Chrome. Is it possible to run Chrome with MTE? If yes, the crash should reproduce deterministically.

### ds...@chromium.org (2024-11-26)

I enabled MTE on the Pixel 9 through the Developer Options, and tried refreshing about 20 times, and didn't observe a crash in logcat.

### a7...@gmail.com (2024-11-26)

This is so strange, I successfully tested it on Pixel 8 Chrome 131.0.6778.81 just now. I'll let Arm know you didn't manage to reproduce in Chrome and will relay further updates from them to you (unless you already have a direct communication channel).

### a7...@gmail.com (2024-11-28)

Okay, one more attempt: I used the fuzzer to explore variants of the shader which crash in a harness without MTE. When inserting the found variants in an HTML and testing them in Chrome I observe deterministic crashes (Chrome 131.0.6778.81 on Pixel 8). Could you please try the attached HTML file?
I tested with and without MTE enabled on the device, not that it should make much of a difference.

### ds...@google.com (2024-12-04)

I was able to reproduce the crash with that latest test file.

```
12-04 14:55:23.401 21551 21551 I crash_dump64: performing dump of process 21483 (target tid = 21496)
12-04 14:55:23.569 21551 21551 F DEBUG   : *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** ***
12-04 14:55:23.569 21551 21551 F DEBUG   : Build fingerprint: 'google/tokay/tokay:15/AP3A.241105.008/12485168:user/release-keys'
12-04 14:55:23.569 21551 21551 F DEBUG   : Revision: 'MP1.0'
12-04 14:55:23.569 21551 21551 F DEBUG   : ABI: 'arm64'
12-04 14:55:23.569 21551 21551 F DEBUG   : Timestamp: 2024-12-04 14:55:23.409612556-0500
12-04 14:55:23.569 21551 21551 F DEBUG   : Process uptime: 2s
12-04 14:55:23.569 21551 21551 F DEBUG   : Cmdline: com.android.chrome:privileged_process2
12-04 14:55:23.569 21551 21551 F DEBUG   : pid: 21483, tid: 21496, name: CrGpuMain  >>> com.android.chrome:privileged_process2 <<<
12-04 14:55:23.569 21551 21551 F DEBUG   : uid: 10203
12-04 14:55:23.569 21551 21551 F DEBUG   : tagged_addr_ctrl: 000000000007fff1 (PR_TAGGED_ADDR_ENABLE, mask 0xfffe)
12-04 14:55:23.569 21551 21551 F DEBUG   : pac_enabled_keys: 000000000000000f (PR_PAC_APIAKEY, PR_PAC_APIBKEY, PR_PAC_APDAKEY, PR_PAC_APDBKEY)
12-04 14:55:23.569 21551 21551 F DEBUG   : signal 11 (SIGSEGV), code 1 (SEGV_MAPERR), fault addr 0x0000000000000000
12-04 14:55:23.569 21551 21551 F DEBUG   : Cause: null pointer dereference
12-04 14:55:23.569 21551 21551 F DEBUG   :     x0  0000006efe070810  x1  0000006c8d8a36d8  x2  0000006c8d8a3690  x3  0000006c8d8a3978
12-04 14:55:23.569 21551 21551 F DEBUG   :     x4  0000006c8d8a39d0  x5  0000006dde037420  x6  0000006dee0199e0  x7  0000000000000001
12-04 14:55:23.569 21551 21551 F DEBUG   :     x8  0000000000000008  x9  0000000000000002  x10 0000006e9e10a070  x11 0000000000000008
12-04 14:55:23.569 21551 21551 F DEBUG   :     x12 0000000000000001  x13 0000006ece0504b0  x14 0000000000000002  x15 0000000000000001
12-04 14:55:23.569 21551 21551 F DEBUG   :     x16 0000006cd7aad730  x17 0000006fbe4a8b00  x18 0000006c8cbf4000  x19 0000006d2e0592b0
12-04 14:55:23.569 21551 21551 F DEBUG   :     x20 0000006e0e04d870  x21 000000000000100d  x22 0000000000000003  x23 0000000000000003
12-04 14:55:23.569 21551 21551 F DEBUG   :     x24 0000000000000004  x25 0000006c8d8a3a00  x26 0000000000000000  x27 0000000000000000
12-04 14:55:23.569 21551 21551 F DEBUG   :     x28 0000000000000004  x29 0000006e9e10a060
12-04 14:55:23.569 21551 21551 F DEBUG   :     lr  0000006cd6e18c20  sp  0000006c8d8a38f0  pc  0000006cd6e18c78  pst 0000000080001000
12-04 14:55:23.569 21551 21551 F DEBUG   : 47 total frames
12-04 14:55:23.569 21551 21551 F DEBUG   : backtrace:
12-04 14:55:23.569 21551 21551 F DEBUG   :       #00 pc 00000000023c8c78  /vendor/lib64/egl/libGLES_mali.so ((anonymous namespace)::MaliScalarizer::scalarizeShuffleVector(llvm::Instruction*, (anonymous namespace)::InstrScalarInfo const&)+1256) (BuildId: 5196daba9a83c6fb)
12-04 14:55:23.569 21551 21551 F DEBUG   :       #01 pc 00000000023c42c0  /vendor/lib64/egl/libGLES_mali.so ((anonymous namespace)::MaliScalarizer::scalarize(llvm::Instruction*)+4624) (BuildId: 5196daba9a83c6fb)
12-04 14:55:23.569 21551 21551 F DEBUG   :       #02 pc 00000000023c2654  /vendor/lib64/egl/libGLES_mali.so ((anonymous namespace)::MaliScalarizer::runOnFunction(llvm::Function&) (.03a141ad775a5f40f0ad2389a308d930)+1540) (BuildId: 5196daba9a83c6fb)
12-04 14:55:23.569 21551 21551 F DEBUG   :       #03 pc 000000000234b56c  /vendor/lib64/egl/libGLES_mali.so ((anonymous namespace)::MaliFunctionPassManager::runOnModule(llvm::Module&) (.aeafa394eef5d85b5c8fdc1ceb23a163)+492) (BuildId: 5196daba9a83c6fb)
12-04 14:55:23.569 21551 21551 F DEBUG   :       #04 pc 000000000234aa3c  /vendor/lib64/egl/libGLES_mali.so ((anonymous namespace)::MaliModulePassManager::runOnModule(llvm::Module&) (.aeafa394eef5d85b5c8fdc1ceb23a163)+412) (BuildId: 5196daba9a83c6fb)
12-04 14:55:23.569 21551 21551 F DEBUG   :       #05 pc 000000000234677c  /vendor/lib64/egl/libGLES_mali.so (llvm::Mali::StaticPassManager::TLPassManagerImpl::run(llvm::Module&)+252) (BuildId: 5196daba9a83c6fb)

```

Given the reference to the `scalarizeShuffleVector` in that stack, we're guessing it's related to the emitted `OpVectorSuffle` which is emitted for the swizzle. The specific line in the shader is `let _e6_ = _e5_.zz;` which would map to the shuffle.

Interestingly, changing that to `yy`, `yz`, `zy` all crash. Put anything with an `x` in it seems fine (at least in my testing).

We can try re-writing the `OpVectorShuffle` as 2 extracts and a composite construct. We'll end up emitting 3-5 SPIR-V instructions instead of a single `OpVectorShuffle` but may work around the crash issue.

### ds...@google.com (2024-12-10)

We've discussed the possibilities of what to do here and have decided it's better to wait to hear from Arm as to the root cause of this bug. We can start adding pessimizations into the SPIR-V generation, but there have been 4 different stack traces in this bug alone, so we don't know if the one I'm seeing would fix the others or we need to make more changes.

So, we're going to hold off changes at the moment until we can understand from Arm what exactly is causing the issue.

a72827312@ would it be possible to add me ([dsinclair@google.com](mailto:dsinclair@google.com)) to the ticket that was filed with Arm, or if not ask them to contact us when they know the root cause (either through email or commenting here).

### pe...@google.com (2024-12-11)

dsinclair: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ds...@chromium.org (2024-12-11)

ARM is currently investigating on their end, we're waiting for ARM to respond at this point to determine what the underlying issue is and if we can/should work around it at a higher level.

### am...@chromium.org (2024-12-11)

Adding the external dependency hotlist which will hopefully quell the bot pings to some extent.

@aygupta can you assist with getting Arm engagement here? We're happy to cc them directly to this issue to facilitate more direct comms on this issue.

### pe...@google.com (2024-12-19)

We commit ourselves to a 30 day deadline for fixing for s0 severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

### pe...@google.com (2024-12-26)

dsinclair: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ds...@google.com (2025-01-08)

@amyressler could/should we lower the severity of this from S0? I'm not sure what to do here until we hear back from ARM and am getting various pings about the SLO.

### am...@chromium.org (2025-01-09)

Severity should remain S0 to reflect that actual security risk rather than to quite SLOs.
But I do hear you about the SLO pings.
Since we don't ship the Mali driver in Chrome, I think it's fair that we can add SI-None to this issue, which should quell SLO pings from the automation but also from any other dashboards and processes.

### am...@chromium.org (2025-01-09)

If there other SLO-related pings / issues I can help address on this please let me know and feel free to reach out to me directly off-bug even.

### ds...@google.com (2025-01-14)

I have heard back from ARM and they've given me a workaround. I'm going to try it out locally and see if it resolves the issue for us or not.

### a7...@gmail.com (2025-01-20)

During the discussion with ARM a variant of the shader surfaced that triggers the following error/abort on a Pixel 8 device:

```
DEBUG   : Abort message: 'Pointer tag for 0x2100000040 was truncated, see 'https://source.android.com/devices/tech/debug/tagged-pointers'.'
DEBUG   :     x0  0000000000000000  x1  0000000000007d39  x2 0000000000000006  x3  0000007fcc7e3230
DEBUG   :     x4  3030303031327830  x5  3030303031327830  x6 3030303031327830  x7  3034303030303030
DEBUG   :     x8  00000000000000f0  x9  d214386733441c4f  x10 0000000000000001  x11 000000775e2eda80
DEBUG   :     x12 00000000678a19e4  x13 000000007fffffff  x14 0000000000730fe4  x15 0000010dc11aaa14
DEBUG   :     x16 000000775e357058  x17 000000775e341590  x18 0000007760f3c000  x19 0000000000007d39
DEBUG   :     x20 0000000000007d39  x21 00000000ffffffff  x22 b400007549be99e0  x23 0000002100000040
DEBUG   :     x24 0000007fcc7e33d8  x25 b400007569af27f0  x26 0000000000000030  x27 0000000000000002
DEBUG   :     x28 b400007699b1fde8  x29 0000007fcc7e32b0 
DEBUG   :     lr  000000775e2d6098  sp  0000007fcc7e3230  pc 000000775e2d60bc  pst 0000000000001000
DEBUG   : 24 total frames
DEBUG   : backtrace:
DEBUG   :   NOTE: Function names and BuildId information is missing for some frames due
DEBUG   :   NOTE: to unreadable libraries. For unwinds of apps, only shared libraries
DEBUG   :   NOTE: found under the lib/ directory are readable.
DEBUG   :   NOTE: On this device, run setenforce 0 to make the libraries readable.
DEBUG   :   NOTE: Unreadable libraries:
DEBUG   :   NOTE:   /data/local/tmp/reproducer
DEBUG   :       #00 pc 000000000005e0bc /apex/com.android.runtime/lib64/bionic/libc.so (abort+156) (BuildId: d607b2dd86e0ffc603529ce13afab7fa)
DEBUG   :       #01 pc 0000000000045508 /apex/com.android.runtime/lib64/bionic/libc.so (free+104) (BuildId: d607b2dd86e0ffc603529ce13afab7fa)
DEBUG   :       #02 pc 0000000000ade920 /vendor/lib64/egl/libGLES_mali.so (llvm::DenseMapBase<llvm::DenseMap<clang::Stmt const*, unsigned long, llvm::DenseMapInfo<clang::Stmt const*, void>, llvm::detail::DenseMapPair<clang::Stmt const*, unsigned long>>, clang::Stmt const*, unsigned long, llvm::DenseMapInfo<clang::Stmt const*, void>, llvm::detail::DenseMapPair<clang::Stmt const*, unsigned long>>::FindAndConstruct(clang::Stmt const*&&)+304) BuildId:
ae0dd7744c46583c)

```

I was asked to update this issue with the respective shader (and the above log message) s.t. the Chrome team can reach an informed decision regarding the security impact of the issue (in the context of Chrome).

### ap...@google.com (2025-01-21)

Project: dawn  

Branch: main  

Author: dan sinclair <[dsinclair@chromium.org](mailto:dsinclair@chromium.org)>  

Link:      <https://dawn-review.googlesource.com/222215>

Add polyfill for pack/unpack 4x8 snorm/unorm

---


Expand for full commit details
```
Add polyfill for pack/unpack 4x8 snorm/unorm 
 
This CL adds a polyfill for the 4x8 pack and unpack normalized methods. 
 
Bug: 379551588 
Change-Id: I5f3823c3fd63fb09f828f8af7fd0d7293ac6a727 
Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/222215 
Reviewed-by: Corentin Wallez <cwallez@chromium.org> 
Reviewed-by: James Price <jrprice@google.com> 
Commit-Queue: dan sinclair <dsinclair@chromium.org>

```

---

Files:

- M `src/dawn/native/Toggles.cpp`
- M `src/dawn/native/Toggles.h`
- M `src/dawn/native/vulkan/PhysicalDeviceVk.cpp`
- M `src/dawn/native/vulkan/ShaderModuleVk.cpp`
- M `src/dawn/tests/BUILD.gn`
- A `src/dawn/tests/end2end/PackUnpack4x8NormTests.cpp`
- M `src/tint/lang/core/ir/transform/builtin_polyfill.cc`
- M `src/tint/lang/core/ir/transform/builtin_polyfill.h`
- M `src/tint/lang/core/ir/transform/builtin_polyfill_test.cc`
- M `src/tint/lang/spirv/writer/common/options.h`
- M `src/tint/lang/spirv/writer/raise/raise.cc`

---

Hash: 5bf02b8dee218f82783da522212dc184b6118ac0  

Date:  Tue Jan 21 10:29:22 2025


---

### ds...@google.com (2025-01-21)

Ok, I've landed what should work as a polyfill for this issue. Can you please test it out with our various pocs? For some reason, even without my patch, the POC I got working with Chrome 131 doesn't work with my built Chromium. But, I also know that it was pretty touchy with respect to the spirv and there were possibly other changes which stopped it working for me.

The change should hopefully roll into Chrome today and we get into the next Android canary or the one after that.

### ap...@google.com (2025-01-21)

Project: chromium/src  

Branch: main  

Author: chromium-autoroll <[chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com)>  

Link:      <https://chromium-review.googlesource.com/6188046>

Roll Dawn from 30a6aadfd7d3 to 1d982f1d0d73 (6 revisions)

---


Expand for full commit details
```
Roll Dawn from 30a6aadfd7d3 to 1d982f1d0d73 (6 revisions) 
 
https://dawn.googlesource.com/dawn.git/+log/30a6aadfd7d3..1d982f1d0d73 
 
2025-01-21 kainino@chromium.org [emscripten] More fixes for passing pointers and i64s 
2025-01-21 ynovikov@chromium.org Suppress CTS failures on Pixel 6 
2025-01-21 dsinclair@chromium.org Suppress unsafe-buffer-usage in ir fuzzing. 
2025-01-21 ynovikov@chromium.org Suppress CTS flaky failures on Mac AMD 
2025-01-21 dsinclair@chromium.org Add polyfill for pack/unpack 4x8 snorm/unorm 
2025-01-21 yiwzhang@google.com remove dawn_analysis builder 
 
If this roll has caused a breakage, revert this CL and stop the roller 
using the controls here: 
https://autoroll.skia.org/r/dawn-chromium-autoroll 
Please CC cwallez@google.com,gman@google.com on the revert to ensure that a human 
is aware of the problem. 
 
To file a bug in Dawn: https://bugs.chromium.org/p/dawn/issues/entry 
To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry 
 
To report a problem with the AutoRoller itself, please file a bug: 
https://issues.skia.org/issues/new?component=1389291&template=1850622 
 
Documentation for the AutoRoller is here: 
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md 
 
Cq-Include-Trybots: luci.chromium.try:dawn-android-arm-deps-rel;luci.chromium.try:dawn-android-arm64-deps-rel;luci.chromium.try:dawn-linux-x64-deps-rel;luci.chromium.try:dawn-mac-x64-deps-rel;luci.chromium.try:dawn-mac-arm64-deps-rel;luci.chromium.try:dawn-win10-x64-deps-rel;luci.chromium.try:dawn-win10-x86-deps-rel;luci.chromium.try:dawn-win11-arm64-deps-rel;luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:gpu-fyi-cq-android-arm64 
Bug: chromium:371963563,chromium:379551588,chromium:382140966,chromium:389977397,chromium:391283121 
Tbr: gman@google.com 
Change-Id: Ib190038560918f54d31522a4db71a0086454ee9c 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6188046 
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
Cr-Commit-Position: refs/heads/main@{#1409343}

```

---

Files:

- M `DEPS`
- M `third_party/dawn`

---

Hash: e2b18a445d192ddda76fa8112641ee9e785cea9d  

Date:  Tue Jan 21 15:44:54 2025


---

### a7...@gmail.com (2025-01-22)

I just tested samples that previously triggered an MTE violation and can confirm that those now pass without issues. I cherry-picked the patch onto an older version of dawn to ensure the problem hasn't been masked by some unrelated change in the tint SPIR-V code generation.

### am...@chromium.org (2025-01-22)

Since a fix for this was landed in Dawn and rolled into Chromium, I'm removing external dependency my merge review tags won't get removed by the bot.

### am...@chromium.org (2025-01-29)

this non-trivial change has been on Chromium since 21 January; not seeing any issues on Canary or Dev data in that time; merges approved for <https://dawn-review.googlesource.com/c/dawn/+/222215>; please merge this change to M133 (branch 6943) and M132 (branch 6834) at your earliest convenience, before EOD tomorrow / Thursday 30 January so this fix can be included in the next respective updates

### ap...@google.com (2025-01-29)

Project: dawn  

Branch: chromium/6943  

Author: dan sinclair <[dsinclair@chromium.org](mailto:dsinclair@chromium.org)>  

Link:      <https://dawn-review.googlesource.com/223816>

Add polyfill for pack/unpack 4x8 snorm/unorm

---


Expand for full commit details
```
Add polyfill for pack/unpack 4x8 snorm/unorm 
 
This CL adds a polyfill for the 4x8 pack and unpack normalized methods. 
 
Bug: 379551588 
Change-Id: I5f3823c3fd63fb09f828f8af7fd0d7293ac6a727 
Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/222215 
Reviewed-by: Corentin Wallez <cwallez@chromium.org> 
Reviewed-by: James Price <jrprice@google.com> 
Commit-Queue: dan sinclair <dsinclair@chromium.org> 
(cherry picked from commit 5bf02b8dee218f82783da522212dc184b6118ac0) 
Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/223816 
Auto-Submit: dan sinclair <dsinclair@chromium.org>

```

---

Files:

- M `src/dawn/native/Toggles.cpp`
- M `src/dawn/native/Toggles.h`
- M `src/dawn/native/vulkan/PhysicalDeviceVk.cpp`
- M `src/dawn/native/vulkan/ShaderModuleVk.cpp`
- M `src/dawn/tests/BUILD.gn`
- A `src/dawn/tests/end2end/PackUnpack4x8NormTests.cpp`
- M `src/tint/lang/core/ir/transform/builtin_polyfill.cc`
- M `src/tint/lang/core/ir/transform/builtin_polyfill.h`
- M `src/tint/lang/core/ir/transform/builtin_polyfill_test.cc`
- M `src/tint/lang/spirv/writer/common/options.h`
- M `src/tint/lang/spirv/writer/raise/raise.cc`

---

Hash: d4321eef8c5c94107783d903355c1cbbbb8a3776  

Date:  Wed Jan 29 14:10:59 2025


---

### sp...@google.com (2025-01-29)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $35000.00 for this report.

Rationale for this decision:
high-quality report of memory corruption in a non-sandboxed process


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-01-29)

Congratulations! Thank you for your all your efforts throughout and reporting this issue to us -- great work!

### ap...@google.com (2025-01-29)

Project: dawn  

Branch: chromium/6834  

Author: dan sinclair <[dsinclair@chromium.org](mailto:dsinclair@chromium.org)>  

Link:      <https://dawn-review.googlesource.com/223817>

Add polyfill for pack/unpack 4x8 snorm/unorm

---


Expand for full commit details
```
Add polyfill for pack/unpack 4x8 snorm/unorm 
 
This CL adds a polyfill for the 4x8 pack and unpack normalized methods. 
 
Bug: 379551588 
Change-Id: I5f3823c3fd63fb09f828f8af7fd0d7293ac6a727 
Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/222215 
Reviewed-by: Corentin Wallez <cwallez@chromium.org> 
Reviewed-by: James Price <jrprice@google.com> 
Commit-Queue: dan sinclair <dsinclair@chromium.org> 
(cherry picked from commit 5bf02b8dee218f82783da522212dc184b6118ac0) 
Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/223817 
Commit-Queue: James Price <jrprice@google.com> 
Auto-Submit: dan sinclair <dsinclair@chromium.org>

```

---

Files:

- M `src/dawn/native/Toggles.cpp`
- M `src/dawn/native/Toggles.h`
- M `src/dawn/native/vulkan/PhysicalDeviceVk.cpp`
- M `src/dawn/native/vulkan/ShaderModuleVk.cpp`
- M `src/dawn/tests/BUILD.gn`
- A `src/dawn/tests/end2end/PackUnpack4x8NormTests.cpp`
- M `src/tint/lang/core/ir/transform/builtin_polyfill.cc`
- M `src/tint/lang/core/ir/transform/builtin_polyfill.h`
- M `src/tint/lang/core/ir/transform/builtin_polyfill_test.cc`
- M `src/tint/lang/spirv/writer/common/options.h`
- M `src/tint/lang/spirv/writer/raise/raise.cc`

---

Hash: c3530f2883610bb6606a5f55935c189e732e67d0  

Date:  Wed Jan 29 15:16:22 2025


---

### ch...@google.com (2025-04-30)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/379551588)*
