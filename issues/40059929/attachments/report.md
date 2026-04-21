## Title
  - Google Chrome WebGL glCompressedTexImage3D Heap-Based Buffer Overflow Vulnerability

## Summary
  - A Heap-Based Buffer Overflow vulnerability exists in the WebGL glCompressedTexImage3D.
  - An attacker must open a arbitrary generated html file to exploit this vulnerability.

## Test environment
  - OS : macOS Monterey 12.4(21F79)
  - iMac GPU : AMD Radeon Pro Vega 48
  - asan-mac-release-1004761
  - Download link: https://alesandroortiz.com/articles/latest-chromium-asan-builds/
  ** The latest Chrome (not stable) version is uploaded from the link, and you can download the asan build for macOS. **

  ** As of my testing, this vulnerability only works on macOS. **

## Proof-of-Concept
  - Please check the attached file!

## Reproduce
  - /asan-mac-release-1004761/Chromium.app/Contents/MacOS/Chromium --no-sandbox poc.html

## Address Sanitizer (ASan)
  ```
=================================================================
==17802==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x6060001791c0 at pc 0x00010c19221d bp 0x7ff7b413eba0 sp 0x7ff7b413e368
READ of size 16 at 0x6060001791c0 thread T0
==17802==WARNING: failed to spawn external symbolizer (errno: 9)
==17802==WARNING: failed to spawn external symbolizer (errno: 9)
==17802==WARNING: failed to spawn external symbolizer (errno: 9)
==17802==WARNING: failed to spawn external symbolizer (errno: 9)
==17802==WARNING: failed to spawn external symbolizer (errno: 9)
==17802==WARNING: Failed to use and restart external symbolizer!
    #0 0x10c19221c in __sanitizer_weak_hook_memmem+0x179c (/Users/dnslab/Downloads/asan-mac-release-1004761/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/104.0.5071.0/Helpers/Chromium Helper (GPU).app/Contents/MacOS/libclang_rt.asan_osx_dynamic.dylib:x86_64+0x1f21c) (BuildId: 90dc47a9652a34e4841ca1b86bd256c0240000001000000000070a0000010b00)
    #1 0x7ffa1df34acc in glgCopyRowsWithMemCopy(GLGOperationRec const*, unsigned long, GLDPixelModeRec const*)+0x64 (/System/Library/Frameworks/OpenGL.framework/Versions/A/Libraries/libGLImage.dylib:x86_64+0x6acc) (BuildId: 56aed9f26e8235e9bd65a2c81c31dec232000000200000000100000000040c00)
    #2 0x7ffa1df33db9 in glgProcessPixelsWithProcessor+0x92a (/System/Library/Frameworks/OpenGL.framework/Versions/A/Libraries/libGLImage.dylib:x86_64+0x5db9) (BuildId: 56aed9f26e8235e9bd65a2c81c31dec232000000200000000100000000040c00)
    #3 0x112d607ad in glrATIModifyTexSubImageCPU+0x586 (/System/Library/Extensions/AMDRadeonX5000GLDriver.bundle/Contents/MacOS/AMDRadeonX5000GLDriver:x86_64+0x1f7ad) (BuildId: c30348bb999e396085f7000000fb775232000000200000000100000000040c00)
    #4 0x112d9a650 in glrWriteTextureData+0x23f (/System/Library/Extensions/AMDRadeonX5000GLDriver.bundle/Contents/MacOS/AMDRadeonX5000GLDriver:x86_64+0x59650) (BuildId: c30348bb999e396085f7000000fb775232000000200000000100000000040c00)
    #5 0x7ffa1e1bf6e1 in glCompressedTexImage3D_Exec+0x435 (/System/Library/Frameworks/OpenGL.framework/Versions/A/Resources/GLEngine.bundle/GLEngine:x86_64+0x866e1) (BuildId: a72561b77972305a8f850366b47b7a8f32000000200000000100000000040c00)
    #6 0x7ffa1e13209c in glCompressedTexImage3D+0x36 (/System/Library/Frameworks/OpenGL.framework/Versions/A/Libraries/libGL.dylib:x86_64+0x409c) (BuildId: 7a5491db1b1337bfa174112d53bf903132000000200000000100000000040c00)
    #7 0x1223b1242 in rx::TextureGL::setCompressedImage(gl::Context const*, gl::ImageIndex const&, unsigned int, gl::Extents const&, gl::PixelUnpackState const&, unsigned long, unsigned char const*)+0x2a2 (/Users/dnslab/Downloads/asan-mac-release-1004761/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/104.0.5071.0/Libraries/libGLESv2.dylib:x86_64+0x955242) (BuildId: 4c4c442155553144a1f8636ee586654e2400000010000000000d0a0000030c00)
    #8 0x121d0611c in gl::Texture::setCompressedImage(gl::Context*, gl::PixelUnpackState const&, gl::TextureTarget, int, unsigned int, gl::Extents const&, unsigned long, unsigned char const*)+0x1fc (/Users/dnslab/Downloads/asan-mac-release-1004761/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/104.0.5071.0/Libraries/libGLESv2.dylib:x86_64+0x2aa11c) (BuildId: 4c4c442155553144a1f8636ee586654e2400000010000000000d0a0000030c00)
    #9 0x121b3fecb in gl::Context::compressedTexImage3D(gl::TextureTarget, int, unsigned int, int, int, int, int, int, void const*)+0x3eb (/Users/dnslab/Downloads/asan-mac-release-1004761/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/104.0.5071.0/Libraries/libGLESv2.dylib:x86_64+0xe3ecb) (BuildId: 4c4c442155553144a1f8636ee586654e2400000010000000000d0a0000030c00)
    #10 0x121b40056 in gl::Context::compressedTexImage3DRobust(gl::TextureTarget, int, unsigned int, int, int, int, int, int, int, void const*)+0x26 (/Users/dnslab/Downloads/asan-mac-release-1004761/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/104.0.5071.0/Libraries/libGLESv2.dylib:x86_64+0xe4056) (BuildId: 4c4c442155553144a1f8636ee586654e2400000010000000000d0a0000030c00)
    #11 0x121aae57f in GL_CompressedTexImage3DRobustANGLE+0x13f (/Users/dnslab/Downloads/asan-mac-release-1004761/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/104.0.5071.0/Libraries/libGLESv2.dylib:x86_64+0x5257f) (BuildId: 4c4c442155553144a1f8636ee586654e2400000010000000000d0a0000030c00)
    #12 0x1629d4b02 in gl::GLApiBase::glCompressedTexImage3DRobustANGLEFn(unsigned int, int, unsigned int, int, int, int, int, int, int, void const*)+0x62 (/Users/dnslab/Downloads/asan-mac-release-1004761/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/104.0.5071.0/Chromium Framework:x86_64+0x125b2b02) (BuildId: 4c4c44d255553144a1adb7b706ed896b2400000010000000000d0a0000030c00)
    #13 0x1648bb84c in gpu::gles2::GLES2DecoderPassthroughImpl::DoCompressedTexImage3D(unsigned int, int, unsigned int, int, int, int, int, int, int, void const*)+0xac (/Users/dnslab/Downloads/asan-mac-release-1004761/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/104.0.5071.0/Chromium Framework:x86_64+0x1449984c) (BuildId: 4c4c44d255553144a1adb7b706ed896b2400000010000000000d0a0000030c00)
    #14 0x1649268c6 in gpu::gles2::GLES2DecoderPassthroughImpl::HandleCompressedTexImage3DBucket(unsigned int, void const volatile*)+0x176 (/Users/dnslab/Downloads/asan-mac-release-1004761/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/104.0.5071.0/Chromium Framework:x86_64+0x145048c6) (BuildId: 4c4c44d255553144a1adb7b706ed896b2400000010000000000d0a0000030c00)
    #15 0x16488e97c in gpu::error::Error gpu::gles2::GLES2DecoderPassthroughImpl::DoCommandsImpl<false>(unsigned int, void const volatile*, int, int*)+0x17c (/Users/dnslab/Downloads/asan-mac-release-1004761/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/104.0.5071.0/Chromium Framework:x86_64+0x1446c97c) (BuildId: 4c4c44d255553144a1adb7b706ed896b2400000010000000000d0a0000030c00)
    #16 0x164d5d74e in gpu::CommandBufferService::Flush(int, gpu::AsyncAPIInterface*)+0x48e (/Users/dnslab/Downloads/asan-mac-release-1004761/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/104.0.5071.0/Chromium Framework:x86_64+0x1493b74e) (BuildId: 4c4c44d255553144a1adb7b706ed896b2400000010000000000d0a0000030c00)
    #17 0x164d633f9 in gpu::CommandBufferStub::OnAsyncFlush(int, unsigned int, std::__1::vector<gpu::SyncToken, std::__1::allocator<gpu::SyncToken> > const&)+0x329 (/Users/dnslab/Downloads/asan-mac-release-1004761/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/104.0.5071.0/Chromium Framework:x86_64+0x149413f9) (BuildId: 4c4c44d255553144a1adb7b706ed896b2400000010000000000d0a0000030c00)
    #18 0x164d62801 in gpu::CommandBufferStub::ExecuteDeferredRequest(gpu::mojom::DeferredCommandBufferRequestParams&)+0x1f1 (/Users/dnslab/Downloads/asan-mac-release-1004761/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/104.0.5071.0/Chromium Framework:x86_64+0x14940801) (BuildId: 4c4c44d255553144a1adb7b706ed896b2400000010000000000d0a0000030c00)
    #19 0x164d8142b in gpu::GpuChannel::ExecuteDeferredRequest(mojo::StructPtr<gpu::mojom::DeferredRequestParams>)+0x36b (/Users/dnslab/Downloads/asan-mac-release-1004761/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/104.0.5071.0/Chromium Framework:x86_64+0x1495f42b) (BuildId: 4c4c44d255553144a1adb7b706ed896b2400000010000000000d0a0000030c00)
    #20 0x164d8e2eb in void base::internal::FunctorTraits<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>), void>::Invoke<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams> >(void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&)+0x18b (/Users/dnslab/Downloads/asan-mac-release-1004761/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/104.0.5071.0/Chromium Framework:x86_64+0x1496c2eb) (BuildId: 4c4c44d255553144a1adb7b706ed896b2400000010000000000d0a0000030c00)
    #21 0x1637bb9b4 in gpu::Scheduler::RunNextTask()+0xed4 (/Users/dnslab/Downloads/asan-mac-release-1004761/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/104.0.5071.0/Chromium Framework:x86_64+0x133999b4) (BuildId: 4c4c44d255553144a1adb7b706ed896b2400000010000000000d0a0000030c00)
    #22 0x15ebac40f in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x34f (/Users/dnslab/Downloads/asan-mac-release-1004761/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/104.0.5071.0/Chromium Framework:x86_64+0xe78a40f) (BuildId: 4c4c44d255553144a1adb7b706ed896b2400000010000000000d0a0000030c00)
    #23 0x15ebf3a85 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*)+0x595 (/Users/dnslab/Downloads/asan-mac-release-1004761/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/104.0.5071.0/Chromium Framework:x86_64+0xe7d1a85) (BuildId: 4c4c44d255553144a1adb7b706ed896b2400000010000000000d0a0000030c00)
    #24 0x15ebf307b in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x15b (/Users/dnslab/Downloads/asan-mac-release-1004761/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/104.0.5071.0/Chromium Framework:x86_64+0xe7d107b) (BuildId: 4c4c44d255553144a1adb7b706ed896b2400000010000000000d0a0000030c00)
    #25 0x15ebf4931 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x11 (/Users/dnslab/Downloads/asan-mac-release-1004761/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/104.0.5071.0/Chromium Framework:x86_64+0xe7d2931) (BuildId: 4c4c44d255553144a1adb7b706ed896b2400000010000000000d0a0000030c00)
    #26 0x15ece264c in base::MessagePumpCFRunLoopBase::RunWork()+0x19c (/Users/dnslab/Downloads/asan-mac-release-1004761/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/104.0.5071.0/Chromium Framework:x86_64+0xe8c064c) (BuildId: 4c4c44d255553144a1adb7b706ed896b2400000010000000000d0a0000030c00)
    #27 0x15ecd0239 in base::mac::CallWithEHFrame(void () block_pointer)+0x9 (/Users/dnslab/Downloads/asan-mac-release-1004761/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/104.0.5071.0/Chromium Framework:x86_64+0xe8ae239) (BuildId: 4c4c44d255553144a1adb7b706ed896b2400000010000000000d0a0000030c00)
    #28 0x15ece10e7 in base::MessagePumpCFRunLoopBase::RunWorkSource(void*)+0x157 (/Users/dnslab/Downloads/asan-mac-release-1004761/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/104.0.5071.0/Chromium Framework:x86_64+0xe8bf0e7) (BuildId: 4c4c44d255553144a1adb7b706ed896b2400000010000000000d0a0000030c00)
    #29 0x7ff80520919a in __CFRUNLOOP_IS_CALLING_OUT_TO_A_SOURCE0_PERFORM_FUNCTION__+0x10 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:x86_64h+0x8019a) (BuildId: f8e45ef99fd23331bb1b703d5dacdaf132000000200000000100000000040c00)
    #30 0x7ff805209102 in __CFRunLoopDoSource0+0xb3 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:x86_64h+0x80102) (BuildId: f8e45ef99fd23331bb1b703d5dacdaf132000000200000000100000000040c00)
    #31 0x7ff805208e7c in __CFRunLoopDoSources0+0xf1 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:x86_64h+0x7fe7c) (BuildId: f8e45ef99fd23331bb1b703d5dacdaf132000000200000000100000000040c00)
    #32 0x7ff805207897 in __CFRunLoopRun+0x37b (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:x86_64h+0x7e897) (BuildId: f8e45ef99fd23331bb1b703d5dacdaf132000000200000000100000000040c00)
    #33 0x7ff805206e5b in CFRunLoopRunSpecific+0x231 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:x86_64h+0x7de5b) (BuildId: f8e45ef99fd23331bb1b703d5dacdaf132000000200000000100000000040c00)
    #34 0x7ff80606ad69 in -[NSRunLoop(NSRunLoop) runMode:beforeDate:]+0xd7 (/System/Library/Frameworks/Foundation.framework/Versions/C/Foundation:x86_64+0x5fd69) (BuildId: ceb9e591a1ad3ebcab8d410f4ff9630732000000200000000100000000040c00)
    #35 0x15ece3b00 in base::MessagePumpNSRunLoop::DoRun(base::MessagePump::Delegate*)+0xf0 (/Users/dnslab/Downloads/asan-mac-release-1004761/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/104.0.5071.0/Chromium Framework:x86_64+0xe8c1b00) (BuildId: 4c4c44d255553144a1adb7b706ed896b2400000010000000000d0a0000030c00)
    #36 0x15ecdffd1 in base::MessagePumpCFRunLoopBase::Run(base::MessagePump::Delegate*)+0x2f1 (/Users/dnslab/Downloads/asan-mac-release-1004761/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/104.0.5071.0/Chromium Framework:x86_64+0xe8bdfd1) (BuildId: 4c4c44d255553144a1adb7b706ed896b2400000010000000000d0a0000030c00)
    #37 0x15ebf52c5 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta)+0x335 (/Users/dnslab/Downloads/asan-mac-release-1004761/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/104.0.5071.0/Chromium Framework:x86_64+0xe7d32c5) (BuildId: 4c4c44d255553144a1adb7b706ed896b2400000010000000000d0a0000030c00)
    #38 0x15eb0b8a6 in base::RunLoop::Run(base::Location const&)+0x4b6 (/Users/dnslab/Downloads/asan-mac-release-1004761/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/104.0.5071.0/Chromium Framework:x86_64+0xe6e98a6) (BuildId: 4c4c44d255553144a1adb7b706ed896b2400000010000000000d0a0000030c00)
    #39 0x16bcd16ea in content::GpuMain(content::MainFunctionParams)+0xa9a (/Users/dnslab/Downloads/asan-mac-release-1004761/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/104.0.5071.0/Chromium Framework:x86_64+0x1b8af6ea) (BuildId: 4c4c44d255553144a1adb7b706ed896b2400000010000000000d0a0000030c00)
    #40 0x15d7cd0dc in content::RunOtherNamedProcessTypeMain(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, content::MainFunctionParams, content::ContentMainDelegate*)+0x54c (/Users/dnslab/Downloads/asan-mac-release-1004761/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/104.0.5071.0/Chromium Framework:x86_64+0xd3ab0dc) (BuildId: 4c4c44d255553144a1adb7b706ed896b2400000010000000000d0a0000030c00)
    #41 0x15d7ceadd in content::ContentMainRunnerImpl::Run()+0x41d (/Users/dnslab/Downloads/asan-mac-release-1004761/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/104.0.5071.0/Chromium Framework:x86_64+0xd3acadd) (BuildId: 4c4c44d255553144a1adb7b706ed896b2400000010000000000d0a0000030c00)
    #42 0x15d7cb377 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*)+0x1717 (/Users/dnslab/Downloads/asan-mac-release-1004761/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/104.0.5071.0/Chromium Framework:x86_64+0xd3a9377) (BuildId: 4c4c44d255553144a1adb7b706ed896b2400000010000000000d0a0000030c00)
    #43 0x15d7cbaed in content::ContentMain(content::ContentMainParams)+0x12d (/Users/dnslab/Downloads/asan-mac-release-1004761/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/104.0.5071.0/Chromium Framework:x86_64+0xd3a9aed) (BuildId: 4c4c44d255553144a1adb7b706ed896b2400000010000000000d0a0000030c00)
    #44 0x150426b30 in ChromeMain+0x230 (/Users/dnslab/Downloads/asan-mac-release-1004761/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/104.0.5071.0/Chromium Framework:x86_64+0x4b30) (BuildId: 4c4c44d255553144a1adb7b706ed896b2400000010000000000d0a0000030c00)
    #45 0x10bdbdd00 in main+0x2c0 (/Users/dnslab/Downloads/asan-mac-release-1004761/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/104.0.5071.0/Helpers/Chromium Helper (GPU).app/Contents/MacOS/Chromium Helper (GPU):x86_64+0x100000d00) (BuildId: 4c4c444655553144a1d9c8ec979288e62400000010000000000d0a0000030c00)
    #46 0x112fa051d  (/usr/lib/dyld:x86_64+0x551d) (BuildId: b70ce1ecb9023852826805de00bfa8d532000000200000000100000000040c00)

0x6060001791c0 is located 960 bytes to the right of 64-byte region [0x606000178dc0,0x606000178e00)
allocated by thread T0 here:
    #0 0x10c1be390 in __asan_memmove+0x1bb0 (/Users/dnslab/Downloads/asan-mac-release-1004761/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/104.0.5071.0/Helpers/Chromium Helper (GPU).app/Contents/MacOS/libclang_rt.asan_osx_dynamic.dylib:x86_64+0x4b390) (BuildId: 90dc47a9652a34e4841ca1b86bd256c0240000001000000000070a0000010b00)
    #1 0x15d8fc167 in operator new(unsigned long)+0x27 (/Users/dnslab/Downloads/asan-mac-release-1004761/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/104.0.5071.0/Chromium Framework:x86_64+0xd4da167) (BuildId: 4c4c44d255553144a1adb7b706ed896b2400000010000000000d0a0000030c00)
    #2 0x16471dc3a in gpu::CommonDecoder::HandleSetBucketSize(unsigned int, void const volatile*)+0xaa (/Users/dnslab/Downloads/asan-mac-release-1004761/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/104.0.5071.0/Chromium Framework:x86_64+0x142fbc3a) (BuildId: 4c4c44d255553144a1adb7b706ed896b2400000010000000000d0a0000030c00)
    #3 0x16488e98b in gpu::error::Error gpu::gles2::GLES2DecoderPassthroughImpl::DoCommandsImpl<false>(unsigned int, void const volatile*, int, int*)+0x18b (/Users/dnslab/Downloads/asan-mac-release-1004761/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/104.0.5071.0/Chromium Framework:x86_64+0x1446c98b) (BuildId: 4c4c44d255553144a1adb7b706ed896b2400000010000000000d0a0000030c00)
    #4 0x164d5d74e in gpu::CommandBufferService::Flush(int, gpu::AsyncAPIInterface*)+0x48e (/Users/dnslab/Downloads/asan-mac-release-1004761/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/104.0.5071.0/Chromium Framework:x86_64+0x1493b74e) (BuildId: 4c4c44d255553144a1adb7b706ed896b2400000010000000000d0a0000030c00)
    #5 0x164d633f9 in gpu::CommandBufferStub::OnAsyncFlush(int, unsigned int, std::__1::vector<gpu::SyncToken, std::__1::allocator<gpu::SyncToken> > const&)+0x329 (/Users/dnslab/Downloads/asan-mac-release-1004761/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/104.0.5071.0/Chromium Framework:x86_64+0x149413f9) (BuildId: 4c4c44d255553144a1adb7b706ed896b2400000010000000000d0a0000030c00)
    #6 0x164d62801 in gpu::CommandBufferStub::ExecuteDeferredRequest(gpu::mojom::DeferredCommandBufferRequestParams&)+0x1f1 (/Users/dnslab/Downloads/asan-mac-release-1004761/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/104.0.5071.0/Chromium Framework:x86_64+0x14940801) (BuildId: 4c4c44d255553144a1adb7b706ed896b2400000010000000000d0a0000030c00)
    #7 0x164d8142b in gpu::GpuChannel::ExecuteDeferredRequest(mojo::StructPtr<gpu::mojom::DeferredRequestParams>)+0x36b (/Users/dnslab/Downloads/asan-mac-release-1004761/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/104.0.5071.0/Chromium Framework:x86_64+0x1495f42b) (BuildId: 4c4c44d255553144a1adb7b706ed896b2400000010000000000d0a0000030c00)
    #8 0x164d8e2eb in void base::internal::FunctorTraits<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>), void>::Invoke<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams> >(void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&)+0x18b (/Users/dnslab/Downloads/asan-mac-release-1004761/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/104.0.5071.0/Chromium Framework:x86_64+0x1496c2eb) (BuildId: 4c4c44d255553144a1adb7b706ed896b2400000010000000000d0a0000030c00)
    #9 0x1637bb9b4 in gpu::Scheduler::RunNextTask()+0xed4 (/Users/dnslab/Downloads/asan-mac-release-1004761/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/104.0.5071.0/Chromium Framework:x86_64+0x133999b4) (BuildId: 4c4c44d255553144a1adb7b706ed896b2400000010000000000d0a0000030c00)
    #10 0x15ebac40f in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x34f (/Users/dnslab/Downloads/asan-mac-release-1004761/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/104.0.5071.0/Chromium Framework:x86_64+0xe78a40f) (BuildId: 4c4c44d255553144a1adb7b706ed896b2400000010000000000d0a0000030c00)
    #11 0x15ebf3a85 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*)+0x595 (/Users/dnslab/Downloads/asan-mac-release-1004761/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/104.0.5071.0/Chromium Framework:x86_64+0xe7d1a85) (BuildId: 4c4c44d255553144a1adb7b706ed896b2400000010000000000d0a0000030c00)
    #12 0x15ebf307b in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x15b (/Users/dnslab/Downloads/asan-mac-release-1004761/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/104.0.5071.0/Chromium Framework:x86_64+0xe7d107b) (BuildId: 4c4c44d255553144a1adb7b706ed896b2400000010000000000d0a0000030c00)
    #13 0x15ebf4931 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x11 (/Users/dnslab/Downloads/asan-mac-release-1004761/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/104.0.5071.0/Chromium Framework:x86_64+0xe7d2931) (BuildId: 4c4c44d255553144a1adb7b706ed896b2400000010000000000d0a0000030c00)
    #14 0x15ece264c in base::MessagePumpCFRunLoopBase::RunWork()+0x19c (/Users/dnslab/Downloads/asan-mac-release-1004761/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/104.0.5071.0/Chromium Framework:x86_64+0xe8c064c) (BuildId: 4c4c44d255553144a1adb7b706ed896b2400000010000000000d0a0000030c00)
    #15 0x15ecd0239 in base::mac::CallWithEHFrame(void () block_pointer)+0x9 (/Users/dnslab/Downloads/asan-mac-release-1004761/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/104.0.5071.0/Chromium Framework:x86_64+0xe8ae239) (BuildId: 4c4c44d255553144a1adb7b706ed896b2400000010000000000d0a0000030c00)
    #16 0x15ece10e7 in base::MessagePumpCFRunLoopBase::RunWorkSource(void*)+0x157 (/Users/dnslab/Downloads/asan-mac-release-1004761/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/104.0.5071.0/Chromium Framework:x86_64+0xe8bf0e7) (BuildId: 4c4c44d255553144a1adb7b706ed896b2400000010000000000d0a0000030c00)
    #17 0x7ff80520919a in __CFRUNLOOP_IS_CALLING_OUT_TO_A_SOURCE0_PERFORM_FUNCTION__+0x10 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:x86_64h+0x8019a) (BuildId: f8e45ef99fd23331bb1b703d5dacdaf132000000200000000100000000040c00)
    #18 0x7ff805209102 in __CFRunLoopDoSource0+0xb3 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:x86_64h+0x80102) (BuildId: f8e45ef99fd23331bb1b703d5dacdaf132000000200000000100000000040c00)
    #19 0x7ff805208e7c in __CFRunLoopDoSources0+0xf1 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:x86_64h+0x7fe7c) (BuildId: f8e45ef99fd23331bb1b703d5dacdaf132000000200000000100000000040c00)
    #20 0x7ff805207897 in __CFRunLoopRun+0x37b (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:x86_64h+0x7e897) (BuildId: f8e45ef99fd23331bb1b703d5dacdaf132000000200000000100000000040c00)
    #21 0x7ff805206e5b in CFRunLoopRunSpecific+0x231 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:x86_64h+0x7de5b) (BuildId: f8e45ef99fd23331bb1b703d5dacdaf132000000200000000100000000040c00)
    #22 0x7ff80606ad69 in -[NSRunLoop(NSRunLoop) runMode:beforeDate:]+0xd7 (/System/Library/Frameworks/Foundation.framework/Versions/C/Foundation:x86_64+0x5fd69) (BuildId: ceb9e591a1ad3ebcab8d410f4ff9630732000000200000000100000000040c00)
    #23 0x15ece3b00 in base::MessagePumpNSRunLoop::DoRun(base::MessagePump::Delegate*)+0xf0 (/Users/dnslab/Downloads/asan-mac-release-1004761/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/104.0.5071.0/Chromium Framework:x86_64+0xe8c1b00) (BuildId: 4c4c44d255553144a1adb7b706ed896b2400000010000000000d0a0000030c00)
    #24 0x15ecdffd1 in base::MessagePumpCFRunLoopBase::Run(base::MessagePump::Delegate*)+0x2f1 (/Users/dnslab/Downloads/asan-mac-release-1004761/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/104.0.5071.0/Chromium Framework:x86_64+0xe8bdfd1) (BuildId: 4c4c44d255553144a1adb7b706ed896b2400000010000000000d0a0000030c00)
    #25 0x15ebf52c5 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta)+0x335 (/Users/dnslab/Downloads/asan-mac-release-1004761/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/104.0.5071.0/Chromium Framework:x86_64+0xe7d32c5) (BuildId: 4c4c44d255553144a1adb7b706ed896b2400000010000000000d0a0000030c00)
    #26 0x15eb0b8a6 in base::RunLoop::Run(base::Location const&)+0x4b6 (/Users/dnslab/Downloads/asan-mac-release-1004761/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/104.0.5071.0/Chromium Framework:x86_64+0xe6e98a6) (BuildId: 4c4c44d255553144a1adb7b706ed896b2400000010000000000d0a0000030c00)
    #27 0x16bcd16ea in content::GpuMain(content::MainFunctionParams)+0xa9a (/Users/dnslab/Downloads/asan-mac-release-1004761/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/104.0.5071.0/Chromium Framework:x86_64+0x1b8af6ea) (BuildId: 4c4c44d255553144a1adb7b706ed896b2400000010000000000d0a0000030c00)
    #28 0x15d7cd0dc in content::RunOtherNamedProcessTypeMain(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, content::MainFunctionParams, content::ContentMainDelegate*)+0x54c (/Users/dnslab/Downloads/asan-mac-release-1004761/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/104.0.5071.0/Chromium Framework:x86_64+0xd3ab0dc) (BuildId: 4c4c44d255553144a1adb7b706ed896b2400000010000000000d0a0000030c00)
    #29 0x15d7ceadd in content::ContentMainRunnerImpl::Run()+0x41d (/Users/dnslab/Downloads/asan-mac-release-1004761/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/104.0.5071.0/Chromium Framework:x86_64+0xd3acadd) (BuildId: 4c4c44d255553144a1adb7b706ed896b2400000010000000000d0a0000030c00)

SUMMARY: AddressSanitizer: heap-buffer-overflow (/Users/dnslab/Downloads/asan-mac-release-1004761/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/104.0.5071.0/Helpers/Chromium Helper (GPU).app/Contents/MacOS/libclang_rt.asan_osx_dynamic.dylib:x86_64+0x1f21c) (BuildId: 90dc47a9652a34e4841ca1b86bd256c0240000001000000000070a0000010b00) in __sanitizer_weak_hook_memmem+0x179c
Shadow bytes around the buggy address:
  0x1c0c0002f1e0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x1c0c0002f1f0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x1c0c0002f200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x1c0c0002f210: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x1c0c0002f220: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
=>0x1c0c0002f230: fa fa fa fa fa fa fa fa[fa]fa fa fa fa fa fa fa
  0x1c0c0002f240: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x1c0c0002f250: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x1c0c0002f260: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x1c0c0002f270: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x1c0c0002f280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
==17802==ABORTING
Received signal 6
 [0x00015ecaa4c9]
 [0x00015ea28eb3]
 [0x00015ecaa098]
 [0x7ff805157dfd]
 [0x00011301b3a0]
 [0x7ff80508dd24]
 [0x00010c1e3606]
 [0x00010c1e2d64]
 [0x00010c1c6827]
 [0x00010c1c5acc]
 [0x00010c19223c]
 [0x7ffa1df34acd]
 [0x7ffa1df33dba]
 [0x000112d607ae]
 [0x000112d9a651]
 [0x7ffa1e1bf6e2]
 [0x7ffa1e13209d]
 [0x0001223b1243]
 [0x000121d0611d]
 [0x000121b3fecc]
 [0x000121b40057]
 [0x000121aae580]
 [0x0001629d4b03]
 [0x0001648bb84d]
 [0x0001649268c7]
 [0x00016488e97d]
 [0x000164d5d74f]
 [0x000164d633fa]
 [0x000164d62802]
 [0x000164d8142c]
 [0x000164d8e2ec]
 [0x0001637bb9b5]
 [0x00015ebac410]
 [0x00015ebf3a86]
 [0x00015ebf307c]
 [0x00015ebf4932]
 [0x00015ece264d]
 [0x00015ecd023a]
 [0x00015ece10e8]
 [0x7ff80520919b]
 [0x7ff805209103]
 [0x7ff805208e7d]
 [0x7ff805207898]
 [0x7ff805206e5c]
 [0x7ff80606ad6a]
 [0x00015ece3b01]
 [0x00015ecdffd2]
 [0x00015ebf52c6]
 [0x00015eb0b8a7]
 [0x00016bcd16eb]
 [0x00015d7cd0dd]
 [0x00015d7ceade]
 [0x00015d7cb378]
 [0x00015d7cbaee]
 [0x000150426b31]
 [0x00010bdbdd01]
 [0x000112fa051e]
[end of stack trace]
  ```

## CREDIT Information
  - Dohyun Lee (@l33d0hyun) of SSD-Disclosure Labs & DNSLab, Korea Univ.