# Support SPIR-V 1.4

| Field | Value |
|-------|-------|
| **Issue ID** | [498659375](https://issues.chromium.org/issues/498659375) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Dawn>Tint |
| **Reporter** | al...@google.com |
| **Assignee** | al...@google.com |
| **Created** | 2026-04-01 |
| **Bounty** | $32,000.00 |

## Description

**VULNERABILITY DETAILS**

Chrome on Android compiles WebGPU shaders by first translating them to SPIR-V using tint, and then passing them for further compilation to libGLES\_mali.so. The shader included in this bug report causes a SIGSEGV crash in libGLES\_mali.so if the shader is compiled to SPIR-V 1.4.

Type of crash: GPU process

Stack trace:

```
 ./adb logcat -d | grep -A 50 "DEBUG"
04-01 20:33:59.446 29121 29121 F DEBUG   : *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** ***
04-01 20:33:59.446 29121 29121 F DEBUG   : Build fingerprint: 'google/oriole/oriole:16/CP1A.260305.018/14887507:user/release-keys'
04-01 20:33:59.446 29121 29121 F DEBUG   : Kernel Release: '6.1.145-android14-11-gfa1d6308d1fe-ab14691759'
04-01 20:33:59.446 29121 29121 F DEBUG   : Revision: 'MP1.0'
04-01 20:33:59.446 29121 29121 F DEBUG   : ABI: 'arm64'
04-01 20:33:59.446 29121 29121 F DEBUG   : Timestamp: 2026-04-01 20:33:59.144639214+0100
04-01 20:33:59.446 29121 29121 F DEBUG   : Process uptime: 9s
04-01 20:33:59.446 29121 29121 F DEBUG   : Executable: /system/bin/app_process64
04-01 20:33:59.446 29121 29121 F DEBUG   : Cmdline: com.android.chrome:privileged_process0
04-01 20:33:59.446 29121 29121 F DEBUG   : pid: 28775, tid: 28810, name: CrGpuMain  >>> com.android.chrome:privileged_process0 <<<
04-01 20:33:59.446 29121 29121 F DEBUG   : uid: 10186
04-01 20:33:59.446 29121 29121 F DEBUG   : tagged_addr_ctrl: 0000000000000001 (PR_TAGGED_ADDR_ENABLE)
04-01 20:33:59.446 29121 29121 F DEBUG   : esr: 0000000092000005 (Data Abort Exception 0x24)
04-01 20:33:59.446 29121 29121 F DEBUG   : signal 11 (SIGSEGV), code 1 (SEGV_MAPERR), fault addr 0x0000002100430240 (read)
04-01 20:33:59.446 29121 29121 F DEBUG   :     x0  b400007cb5495e60  x1  0000007adced2860  x2  0000007adced28c8  x3  0000000000000008
04-01 20:33:59.446 29121 29121 F DEBUG   :     x4  0000000000000000  x5  0000007adced24c0  x6  b400007bd5464ad0  x7  b400007bd5464ad0
04-01 20:33:59.446 29121 29121 F DEBUG   :     x8  0000002100430240  x9  0000000000343462  x10 b400007d254502f0  x11 0000002100000040
04-01 20:33:59.446 29121 29121 F DEBUG   :     x12 0000000000343461  x13 0000000000043020  x14 fffffffffffff000  x15 0000000000000002
04-01 20:33:59.446 29121 29121 F DEBUG   :     x16 fffffffffffff000  x17 0000000000000001  x18 0000007adc12c000  x19 0000007adced28d0
04-01 20:33:59.446 29121 29121 F DEBUG   :     x20 b400007cb5495e60  x21 0000007adced8240  x22 b400007cb5495440  x23 0000002100000040
04-01 20:33:59.446 29121 29121 F DEBUG   :     x24 b400007bd5464738  x25 b400007bd54b19e0  x26 0000000000000030  x27 0000000000000002
04-01 20:33:59.446 29121 29121 F DEBUG   :     x28 0000000000000001  x29 0000007b33426a60
04-01 20:33:59.446 29121 29121 F DEBUG   :     lr  0000007b3325c240  sp  0000007adced2830  pc  0000007b30f82bec  pst 0000000080001000
04-01 20:33:59.446 29121 29121 F DEBUG   :     esr 0000000092000005  vg  0000000000000000
04-01 20:33:59.446 29121 29121 F DEBUG   : 51 total frames
04-01 20:33:59.446 29121 29121 F DEBUG   : backtrace:
04-01 20:33:59.446 29121 29121 F DEBUG   :       #00 pc 0000000000b23bec  /vendor/lib64/egl/libGLES_mali.so (llvm::DenseMapBase<llvm::DenseMap<clang::Stmt const*, unsigned long, llvm::DenseMapInfo<clang::Stmt const*, void>, llvm::detail::DenseMapPair<clang::Stmt const*, unsigned long>>, clang::Stmt const*, unsigned long, llvm::DenseMapInfo<clang::Stmt const*, void>, llvm::detail::DenseMapPair<clang::Stmt const*, unsigned long>>::FindAndConstruct(clang::Stmt const*&&)+60) (BuildId: feb9f26605cd09ae111d43748527cd1fcf5013d2)
04-01 20:33:59.446 29121 29121 F DEBUG   :       #01 pc 0000000002dfd23c  /vendor/lib64/egl/libGLES_mali.so (llvm::ValueHandleBase::AddToUseList()+76) (BuildId: feb9f26605cd09ae111d43748527cd1fcf5013d2)
04-01 20:33:59.446 29121 29121 F DEBUG   :       #02 pc 000000000248fc90  /vendor/lib64/egl/libGLES_mali.so (llvm::Mali::analyzeFunctionImpl(llvm::Mali::IsPilotableCache*, llvm::Function const&, llvm::SmallVectorImpl<llvm::Instruction*>*)+480) (BuildId: feb9f26605cd09ae111d43748527cd1fcf5013d2)
04-01 20:33:59.446 29121 29121 F DEBUG   :       #03 pc 000000000248fa60  /vendor/lib64/egl/libGLES_mali.so (llvm::Mali::MaliIsPilotableAnalysis::analyzeFunction(bool, llvm::SmallVectorImpl<llvm::Instruction*>*)+256) (BuildId: feb9f26605cd09ae111d43748527cd1fcf5013d2)
04-01 20:33:59.446 29121 29121 F DEBUG   :       #04 pc 000000000229701c  /vendor/lib64/egl/libGLES_mali.so (combineInstructionsOverFunction(llvm::Function&, llvm::InstructionWorklist&, llvm::AAResults*, llvm::AssumptionCache&, llvm::TargetLibraryInfo&, llvm::TargetTransformInfo&, llvm::DominatorTree&, llvm::OptimizationRemarkEmitter&, llvm::BlockFrequencyInfo*, llvm::ProfileSummaryInfo*, unsigned int, llvm::LoopInfo*, llvm::MaliICParams)+556) (BuildId: feb9f26605cd09ae111d43748527cd1fcf5013d2)
04-01 20:33:59.446 29121 29121 F DEBUG   :       #05 pc 0000000002299158  /vendor/lib64/egl/libGLES_mali.so (llvm::InstructionCombiningPass::runOnFunction(llvm::Function&)+808) (BuildId: feb9f26605cd09ae111d43748527cd1fcf5013d2)
04-01 20:33:59.446 29121 29121 F DEBUG   :       #06 pc 00000000023509b4  /vendor/lib64/egl/libGLES_mali.so ((anonymous namespace)::MaliIC::runOnFunction(llvm::Function&)+116) (BuildId: feb9f26605cd09ae111d43748527cd1fcf5013d2)
04-01 20:33:59.446 29121 29121 F DEBUG   :       #07 pc 0000000002446ab0  /vendor/lib64/egl/libGLES_mali.so ((anonymous namespace)::MaliFunctionPassManager::runOnModule(llvm::Module&)+560) (BuildId: feb9f26605cd09ae111d43748527cd1fcf5013d2)
04-01 20:33:59.446 29121 29121 F DEBUG   :       #08 pc 0000000002445e48  /vendor/lib64/egl/libGLES_mali.so ((anonymous namespace)::MaliModulePassManager::runOnModule(llvm::Module&)+408) (BuildId: feb9f26605cd09ae111d43748527cd1fcf5013d2)
04-01 20:33:59.446 29121 29121 F DEBUG   :       #09 pc 000000000244181c  /vendor/lib64/egl/libGLES_mali.so (llvm::Mali::StaticPassManager::TLPassManagerImpl::run(llvm::Module&)+268) (BuildId: feb9f26605cd09ae111d43748527cd1fcf5013d2)
04-01 20:33:59.446 29121 29121 F DEBUG   :       #10 pc 0000000001d63444  /vendor/lib64/egl/libGLES_mali.so (cmpbep_bfr_run_llvm_backend+2052) (BuildId: feb9f26605cd09ae111d43748527cd1fcf5013d2)
04-01 20:33:59.446 29121 29121 F DEBUG   :       #11 pc 0000000001d67e34  /vendor/lib64/egl/libGLES_mali.so (cmpbe_compile_gles_shader+660) (BuildId: feb9f26605cd09ae111d43748527cd1fcf5013d2)
04-01 20:33:59.446 29121 29121 F DEBUG   :       #12 pc 0000000001d8a6ec  /vendor/lib64/egl/libGLES_mali.so (do_single_part2_compilation+220) (BuildId: feb9f26605cd09ae111d43748527cd1fcf5013d2)
04-01 20:33:59.446 29121 29121 F DEBUG   :       #13 pc 0000000001d89fb0  /vendor/lib64/egl/libGLES_mali.so (cmpbe_v2_compile_multiple_shaders+8912) (BuildId: feb9f26605cd09ae111d43748527cd1fcf5013d2)
04-01 20:33:59.446 29121 29121 F DEBUG   :       #14 pc 0000000001bef2d8  /vendor/lib64/egl/libGLES_mali.so (gfx::compiler::compile_shaders(gfx::shader_set const&, gfx::shader_set&, gfx::shader_state const&, gfx::mem_allocator&, gfx::compilation_dynamic_args&, cutils_cmpbe_dump_ctx**, unsigned long*, gfx::mem_blob*, gfx::pipeline_exec_info*)+952) (BuildId: feb9f26605cd09ae111d43748527cd1fcf5013d2)
04-01 20:33:59.446 29121 29121 F DEBUG   :       #15 pc 0000000001bf008c  /vendor/lib64/egl/libGLES_mali.so (gfx::compiler::compile_shaders_with_cache(gfx::shader_set const&, gfx::shader_set&, gfx::shader_state const&, compiler_cache*, gfx::mem_allocator&, cutils_cmpbe_dump_ctx**, bool*, unsigned long*, gfx::pipeline_exec_info*)+396) (BuildId: feb9f26605cd09ae111d43748527cd1fcf5013d2)
04-01 20:33:59.446 29121 29121 F DEBUG   :       #16 pc 00000000009165d0  /vendor/lib64/egl/libGLES_mali.so (vkCreateComputePipelines+2496) (BuildId: feb9f26605cd09ae111d43748527cd1fcf5013d2)
04-01 20:33:59.446 29121 29121 F DEBUG   :       #17 pc 0000000002aa177c  /data/app/~~eEshiOZy94RO5C-OOXFQwA==/com.google.android.trichromelibrary_768017733-Ntbecq5LomTHIa0-BxSllQ==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: 36894d7d02ba6dd926ce935e4753618f784b9bf4)
04-01 20:33:59.446 29121 29121 F DEBUG   :       #18 pc 00000000073ed988  /data/app/~~eEshiOZy94RO5C-OOXFQwA==/com.google.android.trichromelibrary_768017733-Ntbecq5LomTHIa0-BxSllQ==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: 36894d7d02ba6dd926ce935e4753618f784b9bf4)
04-01 20:33:59.446 29121 29121 F DEBUG   :       #19 pc 0000000002a2f6a8  /data/app/~~eEshiOZy94RO5C-OOXFQwA==/com.google.android.trichromelibrary_768017733-Ntbecq5LomTHIa0-BxSllQ==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: 36894d7d02ba6dd926ce935e4753618f784b9bf4)
04-01 20:33:59.446 29121 29121 F DEBUG   :       #20 pc 0000000002a2f498  /data/app/~~eEshiOZy94RO5C-OOXFQwA==/com.google.android.trichromelibrary_768017733-Ntbecq5LomTHIa0-BxSllQ==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: 36894d7d02ba6dd926ce935e4753618f784b9bf4)
04-01 20:33:59.446 29121 29121 F DEBUG   :       #21 pc 000000000284d700  /data/app/~~eEshiOZy94RO5C-OOXFQwA==/com.google.android.trichromelibrary_768017733-Ntbecq5LomTHIa0-BxSllQ==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: 36894d7d02ba6dd926ce935e4753618f784b9bf4)
04-01 20:33:59.446 29121 29121 F DEBUG   :       #22 pc 0000000002854014  /data/app/~~eEshiOZy94RO5C-OOXFQwA==/com.google.android.trichromelibrary_768017733-Ntbecq5LomTHIa0-BxSllQ==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: 36894d7d02ba6dd926ce935e4753618f784b9bf4)
04-01 20:33:59.446 29121 29121 F DEBUG   :       #23 pc 0000000008f1f4d0  /data/app/~~eEshiOZy94RO5C-OOXFQwA==/com.google.android.trichromelibrary_768017733-Ntbecq5LomTHIa0-BxSllQ==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: 36894d7d02ba6dd926ce935e4753618f784b9bf4)
04-01 20:33:59.446 29121 29121 F DEBUG   :       #24 pc 0000000008f1f5e0  /data/app/~~eEshiOZy94RO5C-OOXFQwA==/com.google.android.trichromelibrary_768017733-Ntbecq5LomTHIa0-BxSllQ==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: 36894d7d02ba6dd926ce935e4753618f784b9bf4)
04-01 20:33:59.446 29121 29121 F DEBUG   :       #25 pc 0000000008f1d0b0  /data/app/~~eEshiOZy94RO5C-OOXFQwA==/com.google.android.trichromelibrary_768017733-Ntbecq5LomTHIa0-BxSllQ==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: 36894d7d02ba6dd926ce935e4753618f784b9bf4)
04-01 20:33:59.446 29121 29121 F DEBUG   :       #26 pc 00000000072bcca0  /data/app/~~eEshiOZy94RO5C-OOXFQwA==/com.google.android.trichromelibrary_768017733-Ntbecq5LomTHIa0-BxSllQ==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: 36894d7d02ba6dd926ce935e4753618f784b9bf4)
04-01 20:33:59.446 29121 29121 F DEBUG   :       #27 pc 00000000072bc1b8  /data/app/~~eEshiOZy94RO5C-OOXFQwA==/com.google.android.trichromelibrary_768017733-Ntbecq5LomTHIa0-BxSllQ==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: 36894d7d02ba6dd926ce935e4753618f784b9bf4)
04-01 20:33:59.446 29121 29121 F DEBUG   :       #28 pc 00000000072bbee4  /data/app/~~eEshiOZy94RO5C-OOXFQwA==/com.google.android.trichromelibrary_768017733-Ntbecq5LomTHIa0-BxSllQ==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: 36894d7d02ba6dd926ce935e4753618f784b9bf4)
04-01 20:33:59.446 29121 29121 F DEBUG   :       #29 pc 00000000072bbd8c  /data/app/~~eEshiOZy94RO5C-OOXFQwA==/com.google.android.trichromelibrary_768017733-Ntbecq5LomTHIa0-BxSllQ==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: 36894d7d02ba6dd926ce935e4753618f784b9bf4)
04-01 20:33:59.446 29121 29121 F DEBUG   :       #30 pc 00000000072bbcfc  /data/app/~~eEshiOZy94RO5C-OOXFQwA==/com.google.android.trichromelibrary_768017733-Ntbecq5LomTHIa0-BxSllQ==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: 36894d7d02ba6dd926ce935e4753618f784b9bf4)
04-01 20:33:59.447 29121 29121 F DEBUG   :       #31 pc 00000000072c717c  /data/app/~~eEshiOZy94RO5C-OOXFQwA==/com.google.android.trichromelibrary_768017733-Ntbecq5LomTHIa0-BxSllQ==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: 36894d7d02ba6dd926ce935e4753618f784b9bf4)
04-01 20:33:59.447 29121 29121 F DEBUG   :       #32 pc 000000000776c6ec  /data/app/~~eEshiOZy94RO5C-OOXFQwA==/com.google.android.trichromelibrary_768017733-Ntbecq5LomTHIa0-BxSllQ==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: 36894d7d02ba6dd926ce935e4753618f784b9bf4)
04-01 20:33:59.447 29121 29121 F DEBUG   :       #33 pc 00000000059b5f68  /data/app/~~eEshiOZy94RO5C-OOXFQwA==/com.google.android.trichromelibrary_768017733-Ntbecq5LomTHIa0-BxSllQ==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: 36894d7d02ba6dd926ce935e4753618f784b9bf4)
04-01 20:33:59.447 29121 29121 F DEBUG   :       #34 pc 00000000059777e8  /data/app/~~eEshiOZy94RO5C-OOXFQwA==/com.google.android.trichromelibrary_768017733-Ntbecq5LomTHIa0-BxSllQ==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: 36894d7d02ba6dd926ce935e4753618f784b9bf4)
04-01 20:33:59.447 29121 29121 F DEBUG   :       #35 pc 0000000005977350  /data/app/~~eEshiOZy94RO5C-OOXFQwA==/com.google.android.trichromelibrary_768017733-Ntbecq5LomTHIa0-BxSllQ==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: 36894d7d02ba6dd926ce935e4753618f784b9bf4)
04-01 20:33:59.447 29121 29121 F DEBUG   :       #36 pc 0000000007248c98  /data/app/~~eEshiOZy94RO5C-OOXFQwA==/com.google.android.trichromelibrary_768017733-Ntbecq5LomTHIa0-BxSllQ==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: 36894d7d02ba6dd926ce935e4753618f784b9bf4)
04-01 20:33:59.447 29121 29121 F DEBUG   :       #37 pc 0000000005896268  /data/app/~~eEshiOZy94RO5C-OOXFQwA==/com.google.android.trichromelibrary_768017733-Ntbecq5LomTHIa0-BxSllQ==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: 36894d7d02ba6dd926ce935e4753618f784b9bf4)
04-01 20:33:59.447 29121 29121 F DEBUG   :       #38 pc 00000000059507f8  /data/app/~~eEshiOZy94RO5C-OOXFQwA==/com.google.android.trichromelibrary_768017733-Ntbecq5LomTHIa0-BxSllQ==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: 36894d7d02ba6dd926ce935e4753618f784b9bf4)
04-01 20:33:59.447 29121 29121 F DEBUG   :       #39 pc 000000000595d6c0  /data/app/~~eEshiOZy94RO5C-OOXFQwA==/com.google.android.trichromelibrary_768017733-Ntbecq5LomTHIa0-BxSllQ==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: 36894d7d02ba6dd926ce935e4753618f784b9bf4)
04-01 20:33:59.447 29121 29121 F DEBUG   :       #40 pc 000000000595d42c  /data/app/~~eEshiOZy94RO5C-OOXFQwA==/com.google.android.trichromelibrary_768017733-Ntbecq5LomTHIa0-BxSllQ==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: 36894d7d02ba6dd926ce935e4753618f784b9bf4)
04-01 20:33:59.447 29121 29121 F DEBUG   :       #41 pc 00000000002e4560  /system/framework/arm64/boot.oat (art_jni_trampoline+112) (BuildId: 9db2d70aebf85f91b896447dda201b4e01075fdc)
04-01 20:33:59.447 29121 29121 F DEBUG   :       #42 pc 00000000006687e8  /apex/com.android.art/lib64/libart.so (nterp_helper+152) (BuildId: be34fbe63ff357beb403f9cb39923ea7)
04-01 20:33:59.447 29121 29121 F DEBUG   :       #43 pc 00000000000df14c  /data/app/~~RqfjifOUkL-V6XZP1F_yjA==/com.android.chrome-3A34KG3dm46dt9l3vPaOwQ==/base.apk (offset 0x1fc000) (no3.run+564)
04-01 20:33:59.447 29121 29121 F DEBUG   :       #44 pc 00000000000a95e0  /system/framework/arm64/boot.oat (java.lang.Thread.run+64) (BuildId: 9db2d70aebf85f91b896447dda201b4e01075fdc)
04-01 20:33:59.447 29121 29121 F DEBUG   :       #45 pc 00000000002cdd94  /apex/com.android.art/lib64/libart.so (art_quick_invoke_stub+612) (BuildId: be34fbe63ff357beb403f9cb39923ea7)
04-01 20:33:59.447 29121 29121 F DEBUG   :       #46 pc 000000000026e624  /apex/com.android.art/lib64/libart.so (art::ArtMethod::Invoke(art::Thread*, unsigned int*, unsigned int, art::JValue*, char const*)+220) (BuildId: be34fbe63ff357beb403f9cb39923ea7)
04-01 20:33:59.447 29121 29121 F DEBUG   :       #47 pc 00000000004c3f30  /apex/com.android.art/lib64/libart.so (art::Thread::CreateCallback(void*)+1184) (BuildId: be34fbe63ff357beb403f9cb39923ea7)
04-01 20:33:59.447 29121 29121 F DEBUG   :       #48 pc 00000000004c3a80  /apex/com.android.art/lib64/libart.so (art::Thread::CreateCallbackWithUffdGc(void*)+8) (BuildId: be34fbe63ff357beb403f9cb39923ea7)
04-01 20:33:59.447 29121 29121 F DEBUG   :       #49 pc 0000000000087d9c  /apex/com.android.runtime/lib64/bionic/libc.so (__pthread_start(void*) (.__uniq.67847048707805468364044055584648682506)+236) (BuildId: 55eea1626770ab1b58504f8f9f205d43)
04-01 20:33:59.447 29121 29121 F DEBUG   :       #50 pc 0000000000078950  /apex/com.android.runtime/lib64/bionic/libc.so (__start_thread+64) (BuildId: 55eea1626770ab1b58504f8f9f205d43)
04-01 20:33:59.469  1556 29131 I DropBoxManagerService: add tag=system_app_native_crash isTagEnabled=true flags=0x2
04-01 20:33:59.471   645   645 E tombstoned: Tombstone written to: tombstone_22
04-01 20:33:59.478  1556  1873 I BootReceiver: Filtering tombstone file: tombstone_22.pb
04-01 20:33:59.483  1556  1873 I BootReceiver: Generated tombstone file: tombstone_22.pb5755149712307559275.pb.tmp
04-01 20:33:59.483  1556  1873 I BootReceiver: Adding tombstone tombstone_22.pb5755149712307559275.pb.tmp to dropbox
04-01 20:33:59.486  7309  7309 I cr_A11yState: Enabled accessibility services: [to.freedom.android2/.android.service.FreedomAccessibilityService]
04-01 20:33:59.486  7309  7309 I cr_A11yState: Running accessibility services: []
04-01 20:33:59.486  7309  7309 I cr_A11yState: Will check again after 250 milliseconds.
04-01 20:33:59.486  1556  1873 I DropBoxManagerService: add tag=SYSTEM_TOMBSTONE_PROTO_WITH_HEADERS isTagEnabled=true flags=0x4
04-01 20:33:59.510  1556  1873 I BootReceiver: Adding text tombstone version of tombstone_22.pb5755149712307559275.pb.tmp to dropbox
04-01 20:33:59.542 29077 29101 E ashmem  : readlink(/proc/self/fd/108) failed: Operation not permitted
04-01 20:33:59.542 29077 29101 E chromium: [ERROR:gpu/ipc/client/command_buffer_proxy_impl.cc:285] ContextResult::kTransientFailure: Failed to send GpuControl.CreateCommandBuffer.
04-01 20:33:59.566  7309  7309 E chromium: [ERROR:gpu/ipc/client/command_buffer_proxy_impl.cc:488] GPU state invalid after WaitForGetOffsetInRange.
04-01 20:33:59.568  1556 13268 I ActivityManager: Process com.android.chrome:privileged_process0 (pid 28775) has died: fg  BTOP
04-01 20:33:59.568  7309  7309 E chromium: [ERROR:content/browser/gpu/gpu_process_host.cc:996] GPU process exited unexpectedly: exit_code=0

```

Crash ID: 41c11825d469a24b

**VERSION**

Device: Pixel 6

Chrome Version: 146.0.7680.177 stable

OS: Android 16 (Build CP1A.260305.018)

**REPRODUCTION CASE**

Open the attached html in Chrome.
Please note that SPIR-V 1.4 is currently in a Finch trial; according to <https://issuetracker.google.com/issues/422421915> it seems that for around 50% of users the shaders are compiled to SPIR-V 1.4.
There are two ways to ensure the shader is compiled to SPIR-V 1.4:

1. Find Chrome in settings; do a "Force stop" and clean storage. It seems that this resets your Finch variations. You might need to do this a few times until you get the right Finch variation.
2. Run `adb shell` and then `echo "_ --enable-dawn-features=dump_shaders,use_spirv_1_4" > /data/local/tmp/chrome-command-line`. In Chrome, go to chrome://flags and enable command line on non-rooted devices, and restart Chrome.

After the site loads, the GPU process should crash. Use `./adb logcat -d | grep -A 50 "DEBUG"` to observe the stack trace.

The attached bug.spv is the SPIR-V 1.4 dump from Chrome's developer console with dawn's `--dump-shaders` flag on. vulkan\_reproducer.cpp is a standalone Vulkan reproducer. Compile it with `~/bin/android-ndk-r27/toolchains/llvm/prebuilt/linux-x86_64/bin/aarch64-linux-android35-clang++ vulkan_reproducer.cpp -o reproducer -lvulkan`. Run it with: `./reproducer bug.spv`.

I have also prepared a standalone Dawn reproducer <https://github.com/mandryskowski/dawn-mre-android/tree/master>

## Attachments

- [bug.html](attachments/bug.html) (text/html, 3.4 KB)
- [bug.spv](attachments/bug.spv) (application/octet-stream, 2.7 KB)
- [bug.wgsl](attachments/bug.wgsl) (application/octet-stream, 443 B)
- [vulkan_reproducer.cpp](attachments/vulkan_reproducer.cpp) (text/x-c++src, 7.4 KB)

## Timeline

### an...@gmail.com (2026-04-01)

Reported to ARM PSIRT.

### ch...@google.com (2026-04-03)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-04-03)

Setting Priority to P1 to match Severity s1. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### ds...@google.com (2026-04-08)

This is a crash in the Mali driver. According to [comment #2](https://issues.chromium.org/issues/498659375#comment2) it's been reported to ARM already. I believe we just need to loop the correct ARM folks into this issue and mark it as external dependency.

### ds...@google.com (2026-04-08)

There isn't anything surprising in the WGSL:

```
@group(0) @binding(0)
var<uniform> u_input: i32;

var<workgroup> global2: i32;

fn foo() -> vec2<bool> {
  var i = 1i;
  loop {
    if (i >= 1i) {
      break;
    }
    i++;
  }
  return !select(vec2<bool>(), !vec2<bool>(), 1i > u_input);
}

@compute @workgroup_size(1)
fn main() {
  let var_0 = foo();
  var i = 1i;
  for (; var_0.x; global2 = 1i) {
    if (i >= 1i) {
      break;
    }
    i++;
  }
}

```

### pe...@google.com (2026-04-08)

Adding some pixel folks. This is certainly a candidate for status external dependency.

### ds...@google.com (2026-04-08)

Not seeing it crash with this WGSL when trying internally. Will need to hear from ARM as to what the specific cause was in order to determine if there is a workaround we can put in place.

### ds...@google.com (2026-04-08)

Jeremy, sending your way as it's a Pixel 6 Mali issue, if you get the problem resolved with the ARM team, please feel free to pass back our way with an idea of what the root cause is so we can workaround if possible.

### an...@gmail.com (2026-04-13)

Still no update from ARM. I pinged them just now. The Intigriti issue code for the ARM report is ARM-PQ8JNRBC.

### an...@gmail.com (2026-05-13)

Still waiting for a response from the ARM GPU security team (ticket ARMSEC-462).

I ran the standalone Vulkan reproducer on a Pixel 8 with MTE enabled in sync mode. This produced the following stack trace (sent to ARM):

```
05-13 21:37:23.085  8832  8832 F DEBUG   : *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** ***
05-13 21:37:23.085  8832  8832 F DEBUG   : Build fingerprint: 'google/shiba/shiba:16/CP1A.260305.018/14887507:user/release-keys'
05-13 21:37:23.085  8832  8832 F DEBUG   : Kernel Release: '6.1.145-android14-11-gfa1d6308d1fe-ab14691759'
05-13 21:37:23.085  8832  8832 F DEBUG   : Revision: 'MP1.0'
05-13 21:37:23.085  8832  8832 F DEBUG   : ABI: 'arm64'
05-13 21:37:23.085  8832  8832 F DEBUG   : Timestamp: 2026-05-13 21:37:22.878243223+0100
05-13 21:37:23.085  8832  8832 F DEBUG   : Process uptime: 2s
05-13 21:37:23.085  8832  8832 F DEBUG   : Executable: /data/local/tmp/reproducer
05-13 21:37:23.085  8832  8832 F DEBUG   : Cmdline: ./reproducer bug.spv
05-13 21:37:23.085  8832  8832 F DEBUG   : pid: 8824, tid: 8824, name: reproducer  >>> ./reproducer <<<
05-13 21:37:23.085  8832  8832 F DEBUG   : uid: 2000
05-13 21:37:23.085  8832  8832 F DEBUG   : tagged_addr_ctrl: 000000000007fff3 (PR_TAGGED_ADDR_ENABLE, PR_MTE_TCF_SYNC, mask 0xfffe)
05-13 21:37:23.085  8832  8832 F DEBUG   : pac_enabled_keys: 000000000000000f (PR_PAC_APIAKEY, PR_PAC_APIBKEY, PR_PAC_APDAKEY, PR_PAC_APDBKEY)
05-13 21:37:23.085  8832  8832 F DEBUG   : esr: 0000000092000011 (Data Abort Exception 0x24)
05-13 21:37:23.085  8832  8832 F DEBUG   : signal 11 (SIGSEGV), code 9 (SEGV_MTESERR), fault addr 0x0e000076a1d70090 (read)
05-13 21:37:23.085  8832  8832 F DEBUG   :     x0  0300007561d61cc0  x1  0000007fea48aad8  x2  0000000000000001  x3  0300007561d61c80
05-13 21:37:23.085  8832  8832 F DEBUG   :     x4  0000000000000002  x5  0000000000000000  x6  0000000000000080  x7  0000000000000001
05-13 21:37:23.085  8832  8832 F DEBUG   :     x8  0e000076a1d6f580  x9  0000000000000058  x10 0300007561d61ca8  x11 0300007561d61cc0
05-13 21:37:23.085  8832  8832 F DEBUG   :     x12 0300007561d61ca0  x13 0000000061e4fa0b  x14 0500007571d5dc78  x15 0a00007571d5d5d8
05-13 21:37:23.085  8832  8832 F DEBUG   :     x16 0000007795582198  x17 000000779550adc0  x18 0000007796238000  x19 0300007561d61cc0
05-13 21:37:23.085  8832  8832 F DEBUG   :     x20 0000000000000001  x21 0000007fea48abb0  x22 0b00007611da0e90  x23 0400007561d621d0
05-13 21:37:23.085  8832  8832 F DEBUG   :     x24 0000000000000001  x25 0000000000000040  x26 0f00007551d99450  x27 0000000100000002
05-13 21:37:23.085  8832  8832 F DEBUG   :     x28 0900007621d6b8c8  x29 0000000000000001
05-13 21:37:23.085  8832  8832 F DEBUG   :     lr  004af9f4fb3c5d18  sp  0000007fea48a950  pc  00000074fb3c5868  pst 0000000080001000
05-13 21:37:23.085  8832  8832 F DEBUG   :     esr 0000000092000011  vg  0000000000000002
05-13 21:37:23.085  8832  8832 F DEBUG   : 18 total frames
05-13 21:37:23.085  8832  8832 F DEBUG   : backtrace:
05-13 21:37:23.085  8832  8832 F DEBUG   :   NOTE: Function names and BuildId information is missing for some frames due
05-13 21:37:23.085  8832  8832 F DEBUG   :   NOTE: to unreadable libraries. For unwinds of apps, only shared libraries
05-13 21:37:23.085  8832  8832 F DEBUG   :   NOTE: found under the lib/ directory are readable.
05-13 21:37:23.085  8832  8832 F DEBUG   :   NOTE: On this device, run setenforce 0 to make the libraries readable.
05-13 21:37:23.085  8832  8832 F DEBUG   :   NOTE: Unreadable libraries:
05-13 21:37:23.085  8832  8832 F DEBUG   :   NOTE:   /data/local/tmp/reproducer
05-13 21:37:23.085  8832  8832 F DEBUG   :       #00 pc 0000000002d9c868  /vendor/lib64/egl/libGLES_mali.so (llvm::Value::setNameImpl(llvm::Twine const&)+40) (BuildId: 186c1907d236658548fc5b497ff0570ca6ea6c23)
05-13 21:37:23.086  8832  8832 F DEBUG   :       #01 pc 0000000002d9cd14  /vendor/lib64/egl/libGLES_mali.so (llvm::Value::setName(llvm::Twine const&, bool)+20) (BuildId: 186c1907d236658548fc5b497ff0570ca6ea6c23)
05-13 21:37:23.086  8832  8832 F DEBUG   :       #02 pc 0000000000afa438  /vendor/lib64/egl/libGLES_mali.so (llvm::IRBuilderBase::CreateExtractElement(llvm::Value*, llvm::Value*, llvm::Twine const&)+232) (BuildId: 186c1907d236658548fc5b497ff0570ca6ea6c23)
05-13 21:37:23.086  8832  8832 F DEBUG   :       #03 pc 0000000001c7af94  /vendor/lib64/egl/libGLES_mali.so (LIR2LLVMConverter::convert_swizzle(cmpbe_node const*)+132) (BuildId: 186c1907d236658548fc5b497ff0570ca6ea6c23)
05-13 21:37:23.086  8832  8832 F DEBUG   :       #04 pc 0000000001c73078  /vendor/lib64/egl/libGLES_mali.so (LIR2LLVMConverter::TraverseBBs(_tag_mempool*, cmpbe_bb*)+424) (BuildId: 186c1907d236658548fc5b497ff0570ca6ea6c23)
05-13 21:37:23.086  8832  8832 F DEBUG   :       #05 pc 0000000001c73168  /vendor/lib64/egl/libGLES_mali.so (LIR2LLVMConverter::TraverseBBs(_tag_mempool*, cmpbe_bb*)+664) (BuildId: 186c1907d236658548fc5b497ff0570ca6ea6c23)
05-13 21:37:23.086  8832  8832 F DEBUG   :       #06 pc 0000000001c73168  /vendor/lib64/egl/libGLES_mali.so (LIR2LLVMConverter::TraverseBBs(_tag_mempool*, cmpbe_bb*)+664) (BuildId: 186c1907d236658548fc5b497ff0570ca6ea6c23)
05-13 21:37:23.086  8832  8832 F DEBUG   :       #07 pc 0000000001c74204  /vendor/lib64/egl/libGLES_mali.so (lir2llvm(cmpbep_pass_manager_context*) (.llvm.13794120129703341920)+3524) (BuildId: 186c1907d236658548fc5b497ff0570ca6ea6c23)
05-13 21:37:23.086  8832  8832 F DEBUG   :       #08 pc 0000000001d6f2c8  /vendor/lib64/egl/libGLES_mali.so (cmpbep_run_pass+392) (BuildId: 186c1907d236658548fc5b497ff0570ca6ea6c23)
05-13 21:37:23.086  8832  8832 F DEBUG   :       #09 pc 0000000001c6f528  /vendor/lib64/egl/libGLES_mali.so (cmpbe_compile_gles_shader+568) (BuildId: 186c1907d236658548fc5b497ff0570ca6ea6c23)
05-13 21:37:23.086  8832  8832 F DEBUG   :       #10 pc 0000000001c90960  /vendor/lib64/egl/libGLES_mali.so (do_single_part2_compilation+208) (BuildId: 186c1907d236658548fc5b497ff0570ca6ea6c23)
05-13 21:37:23.086  8832  8832 F DEBUG   :       #11 pc 0000000001c90218  /vendor/lib64/egl/libGLES_mali.so (cmpbe_v2_compile_multiple_shaders+9032) (BuildId: 186c1907d236658548fc5b497ff0570ca6ea6c23)
05-13 21:37:23.086  8832  8832 F DEBUG   :       #12 pc 0000000001acd860  /vendor/lib64/egl/libGLES_mali.so (gfx::compiler::compile_shaders(gfx::shader_set const&, gfx::shader_set&, gfx::shader_state const&, gfx::mem_allocator&, gfx::compilation_dynamic_args&, cutils_cmpbe_dump_ctx**, unsigned long*, gfx::mem_blob*, gfx::pipeline_exec_info*)+1152) (BuildId: 186c1907d236658548fc5b497ff0570ca6ea6c23)
05-13 21:37:23.086  8832  8832 F DEBUG   :       #13 pc 0000000001ace378  /vendor/lib64/egl/libGLES_mali.so (gfx::compiler::compile_shaders_with_cache(gfx::shader_set const&, gfx::shader_set&, gfx::shader_state const&, compiler_cache*, gfx::mem_allocator&, cutils_cmpbe_dump_ctx**, bool*, unsigned long*, gfx::pipeline_exec_info*)+408) (BuildId: 186c1907d236658548fc5b497ff0570ca6ea6c23)
05-13 21:37:23.086  8832  8832 F DEBUG   :       #14 pc 0000000000948478  /vendor/lib64/egl/libGLES_mali.so (vkCreateComputePipelines+2696) (BuildId: 186c1907d236658548fc5b497ff0570ca6ea6c23)
05-13 21:37:23.086  8832  8832 F DEBUG   :       #15 pc 0000000000005f88  /data/local/tmp/reproducer
05-13 21:37:23.086  8832  8832 F DEBUG   :       #16 pc 000000000000631c  /data/local/tmp/reproducer
05-13 21:37:23.086  8832  8832 F DEBUG   :       #17 pc 000000000006b25c  /apex/com.android.runtime/lib64/bionic/libc.so (__libc_init+124) (BuildId: 91811ea70d610cb58de95ac6d0978282)
05-13 21:37:23.086  8832  8832 F DEBUG   : Note: multiple potential causes for this crash were detected, listing them in decreasing order of likelihood.
05-13 21:37:23.086  8832  8832 F DEBUG   : Cause: [MTE]: Buffer Overflow, 8 bytes right of a 2856-byte allocation at 0x76a1d6f560
05-13 21:37:23.086  8832  8832 F DEBUG   : allocated by thread 8824:
05-13 21:37:23.086  8832  8832 F DEBUG   :       #00 pc 000000000005f964  /apex/com.android.runtime/lib64/bionic/libc.so (_ZN5scudo9AllocatorINS_19AndroidNormalConfigEXadL_Z21scudo_malloc_postinitEEE8allocateEmNS_5Chunk6OriginEmb+852) (BuildId: 91811ea70d610cb58de95ac6d0978282)
05-13 21:37:23.086  8832  8832 F DEBUG   :       #01 pc 000000000005fcd8  /apex/com.android.runtime/lib64/bionic/libc.so (scudo_malloc+40) (BuildId: 91811ea70d610cb58de95ac6d0978282)
05-13 21:37:23.086  8832  8832 F DEBUG   :       #02 pc 000000000005975c  /apex/com.android.runtime/lib64/bionic/libc.so (malloc+44) (BuildId: 91811ea70d610cb58de95ac6d0978282)
05-13 21:37:23.086  8832  8832 F DEBUG   :       #03 pc 0000000000111204  /vendor/lib64/libc++.so (_Znwm+28) (BuildId: c1178e02479441e4d5f533f88cd8ff05d8ef10a8)
05-13 21:37:23.086  8832  8832 F DEBUG   :       #04 pc 0000000002d6a774  /vendor/lib64/egl/libGLES_mali.so (_ZN4llvm11LLVMContextC1EPNS_4Mali7MemPoolE+36) (BuildId: 186c1907d236658548fc5b497ff0570ca6ea6c23)
05-13 21:37:23.086  8832  8832 F DEBUG   : Cause: [MTE]: Buffer Overflow, 6016 bytes right of a 3088-byte allocation at 0x76a1d6dd00
05-13 21:37:23.086  8832  8832 F DEBUG   : allocated by thread 8824:
05-13 21:37:23.086  8832  8832 F DEBUG   :       #00 pc 000000000005f964  /apex/com.android.runtime/lib64/bionic/libc.so (_ZN5scudo9AllocatorINS_19AndroidNormalConfigEXadL_Z21scudo_malloc_postinitEEE8allocateEmNS_5Chunk6OriginEmb+852) (BuildId: 91811ea70d610cb58de95ac6d0978282)
05-13 21:37:23.086  8832  8832 F DEBUG   :       #01 pc 000000000005fcd8  /apex/com.android.runtime/lib64/bionic/libc.so (scudo_malloc+40) (BuildId: 91811ea70d610cb58de95ac6d0978282)
05-13 21:37:23.086  8832  8832 F DEBUG   :       #02 pc 000000000005975c  /apex/com.android.runtime/lib64/bionic/libc.so (malloc+44) (BuildId: 91811ea70d610cb58de95ac6d0978282)
05-13 21:37:23.086  8832  8832 F DEBUG   :       #03 pc 0000000000949310  /vendor/lib64/egl/libGLES_mali.so (_ZN3gfx18host_mem_allocator23allocate_cutils_wrapperEPvm+32) (BuildId: 186c1907d236658548fc5b497ff0570ca6ea6c23)

```

### ds...@google.com (2026-05-20)

@mj...@google.com has there been any update from ARM on this issue? Is there a workaround we can do to mitigate?

### mj...@google.com (2026-05-20)

> @mjstokes has there been any update from ARM on this issue? Is there a workaround we can do to mitigate?

Arm say it is still under investigation -- I have sent them a question about potential mitigations.

### mj...@google.com (2026-05-21)

Hi @ds...@google.com,

**Mitigation suggestion from Arm:**

For ternary expressions where the operands are vectors and evaluate to all-true/all-false respectively, please ensure the selector is converted into a vector boolean selector.

For example:

```
bool selector = ...;
bvec4 foo = selector ? bvec4(true) : bvec4(false);

```

can be rewritten as:

```
bool selector = ...;
bvec4 foo = bvec4(selector) ? bvec4(true) : bvec4(false);

```

Note the `selector` -> `bvec4(selector)`

### ds...@google.com (2026-05-21)

Ah, nice. In this case we should be good already as we denylist'd SPIR-V 1.4 on Arm. On pre-1.4 we already do that transform.

### ds...@google.com (2026-05-21)

Marking this as security-impact-none because we disabled the 1.4 support on ARM before going to full launch.

### ds...@google.com (2026-05-25)

Going to remove the security-impact-none because this *was* impacting before we disabled ARM. We're going to close this as fixed as we denylisted SPIR-V 1.4 ARM, we'll open a new bug to investigating allowing ARM SPIRV-1.4 in the future.

### ch...@google.com (2026-05-25)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### ch...@google.com (2026-05-26)

This is sufficiently serious that it should be merged to M148. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M148. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Security Merge Request:

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

This is sufficiently serious that it should be merged to M149. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M149. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

### ch...@google.com (2026-05-26)

**M148** merge request created. **Please update [crbug/516657428](https://crbug.com/516657428) to have this merge reviewed.**

### ch...@google.com (2026-05-26)

**M149** merge request created. **Please update [crbug/516658471](https://crbug.com/516658471) to have this merge reviewed.**

### sp...@google.com (2026-06-04)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $32000.00 for this report.

Rationale for this decision:
Baseline. Memory Corruption / RCE in a highly privileged process (e.g. GPU or network)


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-09-01)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> Baseline. Memory Corruption / RCE in a highly privileged process (e.g. GPU or network)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/498659375)*
