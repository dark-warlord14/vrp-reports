# libGLES_mali UAF via WebGPU shaders at llvm::PatternMatch::undef_match::check

| Field | Value |
|-------|-------|
| **Issue ID** | [391284742](https://issues.chromium.org/issues/391284742) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | Dawn>Tint |
| **Platforms** | Android |
| **CVE IDs** | CVE-2025-0932 |
| **Reporter** | a7...@gmail.com |
| **Assignee** | am...@chromium.org |
| **Created** | 2025-01-21 |
| **Bounty** | $5,000.00 |

## Description

##### VULNERABILITY DETAILS

Chrome on Android translates WebGPU shaders to SPIR-V. These SPIR-V shaders are eventually passed to libGLES\_mali.so for optimization and native code generation. This bug report is about a WebGPU shader that crashes org.chromium.chrome on an MTE-enable device. Chromium uses async MTE, hence the backtrace is imprecise. When running a standalone reproducer with MTE in sync mode, MTE detects a UAF in `llvm::PatternMatch::undef_match::check`. I will provide a copy of this report to ARM and keep you posted.

##### VERSION

Device: Pixel 8a   

Android build number: AP4A.241205.013   

Chromium: 134.0.6971.0 (commit 70c0998f9a2abf76f4083f80fbae94220f7e6e06)

##### REPRODUCTION CASE (Chromium)

I compiled Chromium from source and enabled MTE on the device; this seem to enable MTE for Chromium as well (in async mode). Opening the attached a.html file should trigger a crash with the following backtrace:

```
01-21 15:42:31.244 19084 19084 F DEBUG   : *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** ***
01-21 15:42:31.244 19084 19084 F DEBUG   : Build fingerprint: 'google/akita/akita:15/AP4A.241205.013/12621605:user/release-keys'
01-21 15:42:31.244 19084 19084 F DEBUG   : Revision: 'MP1.0'
01-21 15:42:31.244 19084 19084 F DEBUG   : ABI: 'arm64'
01-21 15:42:31.244 19084 19084 F DEBUG   : Timestamp: 2025-01-21 15:42:30.190512096+0100
01-21 15:42:31.244 19084 19084 F DEBUG   : Process uptime: 90s
01-21 15:42:31.245 19084 19084 F DEBUG   : Cmdline: org.chromium.chrome:privileged_process0
01-21 15:42:31.245 19084 19084 F DEBUG   : pid: 18739, tid: 18752, name: CrGpuMain  >>> org.chromium.chrome:privileged_process0 <<<
01-21 15:42:31.245 19084 19084 F DEBUG   : uid: 10280
01-21 15:42:31.245 19084 19084 F DEBUG   : tagged_addr_ctrl: 000000000007fff7 (PR_TAGGED_ADDR_ENABLE, PR_MTE_TCF_SYNC, PR_MTE_TCF_ASYNC, mask 0xfffe)
01-21 15:42:31.245 19084 19084 F DEBUG   : pac_enabled_keys: 000000000000000f (PR_PAC_APIAKEY, PR_PAC_APIBKEY, PR_PAC_APDAKEY, PR_PAC_APDBKEY)
01-21 15:42:31.245 19084 19084 F DEBUG   : signal 11 (SIGSEGV), code 8 (SEGV_MTEAERR), fault addr --------
01-21 15:42:31.245 19084 19084 F DEBUG   :     x0  080000748ce08e90  x1  0000000000000000  x2  0e0000747ce4d878  x3  0000000000000000
01-21 15:42:31.245 19084 19084 F DEBUG   :     x4  0000000000000000  x5  0000000000000000  x6  0000000000000000  x7  0000000000000000
01-21 15:42:31.245 19084 19084 F DEBUG   :     x8  0a0000751ce056d0  x9  0c0000760d70f278  x10 0000000000000010  x11 080000748ce08e90
01-21 15:42:31.245 19084 19084 F DEBUG   :     x12 010000748ce97aa0  x13 0c0000760d70f288  x14 080000748ce08e90  x15 0000000000000000
01-21 15:42:31.245 19084 19084 F DEBUG   :     x16 0000007436ac6e58  x17 0000007719498a40  x18 00000073e3dfc000  x19 0e0000747ce4d878
01-21 15:42:31.245 19084 19084 F DEBUG   :     x20 0e0000766ce33898  x21 00000073e4d1dbc8  x22 0a0000751ce056e0  x23 00000073e4d1dae8
01-21 15:42:31.245 19084 19084 F DEBUG   :     x24 0000000000000000  x25 00000073e4d1dae8  x26 0000000000000000  x27 0000000000000000
01-21 15:42:31.245 19084 19084 F DEBUG   :     x28 00000073e4d1db20  x29 0c0000760d70f220
01-21 15:42:31.245 19084 19084 F DEBUG   :     lr  00000074363c76b4  sp  00000073e4d1d9d0  pc  00000074363c8298  pst 0000000060001000
01-21 15:42:31.245 19084 19084 F DEBUG   : Note: This crash is a delayed async MTE crash. Memory corruption has occurred
01-21 15:42:31.245 19084 19084 F DEBUG   :       in this process. The stack trace below is the first system call or context
01-21 15:42:31.245 19084 19084 F DEBUG   :       switch that was executed after the memory corruption happened.
01-21 15:42:31.245 19084 19084 F DEBUG   : 87 total frames
01-21 15:42:31.245 19084 19084 F DEBUG   : backtrace:
01-21 15:42:31.245 19084 19084 F DEBUG   :       #00 pc 00000000027bf298  /vendor/lib64/egl/libGLES_mali.so (llvm::simplifyLoop(llvm::Loop*, llvm::DominatorTree*, llvm::LoopInfo*, llvm::ScalarEvolution*, llvm::AssumptionCache*, llvm::MemorySSAUpdater*, bool)+4808) (BuildId: ba412f8560df6af8)
01-21 15:42:31.245 19084 19084 F DEBUG   :       #01 pc 00000000027c19fc  /vendor/lib64/egl/libGLES_mali.so ((anonymous namespace)::LoopSimplify::runOnFunction(llvm::Function&)+492) (BuildId: ba412f8560df6af8)
01-21 15:42:31.245 19084 19084 F DEBUG   :       #02 pc 00000000021cd050  /vendor/lib64/egl/libGLES_mali.so ((anonymous namespace)::MaliFunctionPassManager::runOnModule(llvm::Module&)+544) (BuildId: ba412f8560df6af8)
01-21 15:42:31.245 19084 19084 F DEBUG   :       #03 pc 00000000021cc420  /vendor/lib64/egl/libGLES_mali.so ((anonymous namespace)::MaliModulePassManager::runOnModule(llvm::Module&)+400) (BuildId: ba412f8560df6af8)
01-21 15:42:31.245 19084 19084 F DEBUG   :       #04 pc 00000000021c80ac  /vendor/lib64/egl/libGLES_mali.so (llvm::Mali::StaticPassManager::TLPassManagerImpl::run(llvm::Module&)+252) (BuildId: ba412f8560df6af8)
01-21 15:42:31.245 19084 19084 F DEBUG   :       #05 pc 0000000001aed77c  /vendor/lib64/egl/libGLES_mali.so (cmpbep_bfr_run_llvm_backend+2044) (BuildId: ba412f8560df6af8)
01-21 15:42:31.245 19084 19084 F DEBUG   :       #06 pc 0000000001af29d4  /vendor/lib64/egl/libGLES_mali.so (cmpbe_compile_gles_shader+660) (BuildId: ba412f8560df6af8)
01-21 15:42:31.245 19084 19084 F DEBUG   :       #07 pc 0000000001b1769c  /vendor/lib64/egl/libGLES_mali.so (do_single_part2_compilation+188) (BuildId: ba412f8560df6af8)
01-21 15:42:31.245 19084 19084 F DEBUG   :       #08 pc 0000000001b173d8  /vendor/lib64/egl/libGLES_mali.so (cmpbe_v2_compile_multiple_shaders+9944) (BuildId: ba412f8560df6af8)
01-21 15:42:31.245 19084 19084 F DEBUG   :       #09 pc 0000000001a0cf4c  /vendor/lib64/egl/libGLES_mali.so (gfx::compiler::compile_shaders(gfx::shader_set const&, gfx::shader_set&, hal::shader_language, gfx::shader_state const&, compiler_cache*, gfx::mem_allocator&, cutils_cmpbe_dump_ctx**, bool*, unsigned long*)+6956) (BuildId: ba412f8560df6af8)
01-21 15:42:31.245 19084 19084 F DEBUG   :       #10 pc 00000000009330e4  /vendor/lib64/egl/libGLES_mali.so (vkCreateGraphicsPipelines+12164) (BuildId: ba412f8560df6af8)
01-21 15:42:31.245 19084 19084 F DEBUG   :       #11 pc 00000000004e915c  /data/app/~~3TLx5oqswNbd9-q6R5wzWg==/org.chromium.chrome-Pgd-CbytKw65rQOCYhqomw==/lib/arm64/libdawn_native.so (BuildId: ee4a2029e250beb1)
01-21 15:42:31.245 19084 19084 F DEBUG   :       #12 pc 000000000040d49c  /data/app/~~3TLx5oqswNbd9-q6R5wzWg==/org.chromium.chrome-Pgd-CbytKw65rQOCYhqomw==/lib/arm64/libdawn_native.so (BuildId: ee4a2029e250beb1)
01-21 15:42:31.245 19084 19084 F DEBUG   :       #13 pc 00000000003bea2c  /data/app/~~3TLx5oqswNbd9-q6R5wzWg==/org.chromium.chrome-Pgd-CbytKw65rQOCYhqomw==/lib/arm64/libdawn_native.so (BuildId: ee4a2029e250beb1)
01-21 15:42:31.246 19084 19084 F DEBUG   :       #14 pc 00000000003be820  /data/app/~~3TLx5oqswNbd9-q6R5wzWg==/org.chromium.chrome-Pgd-CbytKw65rQOCYhqomw==/lib/arm64/libdawn_native.so (BuildId: ee4a2029e250beb1)
01-21 15:42:31.246 19084 19084 F DEBUG   :       #15 pc 0000000000083248  /data/app/~~3TLx5oqswNbd9-q6R5wzWg==/org.chromium.chrome-Pgd-CbytKw65rQOCYhqomw==/lib/arm64/libdawn_wire.so (BuildId: 65f6453b2b5dde89)
01-21 15:42:31.246 19084 19084 F DEBUG   :       #16 pc 000000000008aeac  /data/app/~~3TLx5oqswNbd9-q6R5wzWg==/org.chromium.chrome-Pgd-CbytKw65rQOCYhqomw==/lib/arm64/libdawn_wire.so (BuildId: 65f6453b2b5dde89)
01-21 15:42:31.246 19084 19084 F DEBUG   :       #17 pc 000000000008d96c  /data/app/~~3TLx5oqswNbd9-q6R5wzWg==/org.chromium.chrome-Pgd-CbytKw65rQOCYhqomw==/lib/arm64/libdawn_wire.so (BuildId: 65f6453b2b5dde89)
01-21 15:42:31.246 19084 19084 F DEBUG   :       #18 pc 0000000000093394  /data/app/~~3TLx5oqswNbd9-q6R5wzWg==/org.chromium.chrome-Pgd-CbytKw65rQOCYhqomw==/lib/arm64/libdawn_wire.so (BuildId: 65f6453b2b5dde89)
01-21 15:42:31.246 19084 19084 F DEBUG   :       #19 pc 0000000000444a60  /data/app/~~3TLx5oqswNbd9-q6R5wzWg==/org.chromium.chrome-Pgd-CbytKw65rQOCYhqomw==/lib/arm64/libgpu_gles2.cr.so (BuildId: 4a68ca206e95dafa)
01-21 15:42:31.246 19084 19084 F DEBUG   :       #20 pc 0000000000444ec8  /data/app/~~3TLx5oqswNbd9-q6R5wzWg==/org.chromium.chrome-Pgd-CbytKw65rQOCYhqomw==/lib/arm64/libgpu_gles2.cr.so (BuildId: 4a68ca206e95dafa)
01-21 15:42:31.246 19084 19084 F DEBUG   :       #21 pc 000000000043fa9c  /data/app/~~3TLx5oqswNbd9-q6R5wzWg==/org.chromium.chrome-Pgd-CbytKw65rQOCYhqomw==/lib/arm64/libgpu_gles2.cr.so (BuildId: 4a68ca206e95dafa)
01-21 15:42:31.246 19084 19084 F DEBUG   :       #22 pc 00000000001745c4  /data/app/~~3TLx5oqswNbd9-q6R5wzWg==/org.chromium.chrome-Pgd-CbytKw65rQOCYhqomw==/lib/arm64/libgpu.cr.so (gpu::CommandBufferService::Flush(int, gpu::AsyncAPIInterface*)+572) (BuildId: 2d448ededacc953d)
01-21 15:42:31.246 19084 19084 F DEBUG   :       #23 pc 0000000000050f04  /data/app/~~3TLx5oqswNbd9-q6R5wzWg==/org.chromium.chrome-Pgd-CbytKw65rQOCYhqomw==/lib/arm64/libgpu_ipc_service.cr.so (gpu::CommandBufferStub::OnAsyncFlush(int, unsigned int, std::__Cr::vector<gpu::SyncToken, std::__Cr::allocator<gpu::SyncToken>> const&)+324) (BuildId: a9a1ef976fc9dea3)
01-21 15:42:31.246 19084 19084 F DEBUG   :       #24 pc 0000000000050b70  /data/app/~~3TLx5oqswNbd9-q6R5wzWg==/org.chromium.chrome-Pgd-CbytKw65rQOCYhqomw==/lib/arm64/libgpu_ipc_service.cr.so (gpu::CommandBufferStub::ExecuteDeferredRequest(gpu::mojom::DeferredCommandBufferRequestParams&, gpu::FenceSyncReleaseDelegate*)+180) (BuildId: a9a1ef976fc9dea3)
01-21 15:42:31.246 19084 19084 F DEBUG   :       #25 pc 000000000005cc20  /data/app/~~3TLx5oqswNbd9-q6R5wzWg==/org.chromium.chrome-Pgd-CbytKw65rQOCYhqomw==/lib/arm64/libgpu_ipc_service.cr.so (gpu::GpuChannel::ExecuteDeferredRequest(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*)+252) (BuildId: a9a1ef976fc9dea3)
01-21 15:42:31.246 19084 19084 F DEBUG   :       #26 pc 0000000000060bec  /data/app/~~3TLx5oqswNbd9-q6R5wzWg==/org.chromium.chrome-Pgd-CbytKw65rQOCYhqomw==/lib/arm64/libgpu_ipc_service.cr.so (BuildId: a9a1ef976fc9dea3)
01-21 15:42:31.246 19084 19084 F DEBUG   :       #27 pc 0000000000060a94  /data/app/~~3TLx5oqswNbd9-q6R5wzWg==/org.chromium.chrome-Pgd-CbytKw65rQOCYhqomw==/lib/arm64/libgpu_ipc_service.cr.so (BuildId: a9a1ef976fc9dea3)
01-21 15:42:31.246 19084 19084 F DEBUG   :       #28 pc 000000000018a510  /data/app/~~3TLx5oqswNbd9-q6R5wzWg==/org.chromium.chrome-Pgd-CbytKw65rQOCYhqomw==/lib/arm64/libgpu.cr.so (BuildId: 2d448ededacc953d)
01-21 15:42:31.246 19084 19084 F DEBUG   :       #29 pc 000000000018a4ac  /data/app/~~3TLx5oqswNbd9-q6R5wzWg==/org.chromium.chrome-Pgd-CbytKw65rQOCYhqomw==/lib/arm64/libgpu.cr.so (BuildId: 2d448ededacc953d)
01-21 15:42:31.246 19084 19084 F DEBUG   :       #30 pc 000000000018a43c  /data/app/~~3TLx5oqswNbd9-q6R5wzWg==/org.chromium.chrome-Pgd-CbytKw65rQOCYhqomw==/lib/arm64/libgpu.cr.so (BuildId: 2d448ededacc953d)
01-21 15:42:31.246 19084 19084 F DEBUG   :       #31 pc 0000000000173488  /data/app/~~3TLx5oqswNbd9-q6R5wzWg==/org.chromium.chrome-Pgd-CbytKw65rQOCYhqomw==/lib/arm64/libgpu.cr.so (BuildId: 2d448ededacc953d)
01-21 15:42:31.246 19084 19084 F DEBUG   :       #32 pc 000000000017b944  /data/app/~~3TLx5oqswNbd9-q6R5wzWg==/org.chromium.chrome-Pgd-CbytKw65rQOCYhqomw==/lib/arm64/libgpu.cr.so (gpu::Scheduler::ExecuteSequence(base::IdType<gpu::SyncPointOrderData, unsigned int, 0u, 1u>)+912) (BuildId: 2d448ededacc953d)
01-21 15:42:31.246 19084 19084 F DEBUG   :       #33 pc 000000000017aefc  /data/app/~~3TLx5oqswNbd9-q6R5wzWg==/org.chromium.chrome-Pgd-CbytKw65rQOCYhqomw==/lib/arm64/libgpu.cr.so (gpu::Scheduler::RunNextTask()+464) (BuildId: 2d448ededacc953d)
01-21 15:42:31.246 19084 19084 F DEBUG   :       #34 pc 00000000002f4e14  /data/app/~~3TLx5oqswNbd9-q6R5wzWg==/org.chromium.chrome-Pgd-CbytKw65rQOCYhqomw==/lib/arm64/libbase.cr.so (BuildId: bb92b0f43ac6f384)
01-21 15:42:31.246 19084 19084 F DEBUG   :       #35 pc 00000000003a9094  /data/app/~~3TLx5oqswNbd9-q6R5wzWg==/org.chromium.chrome-Pgd-CbytKw65rQOCYhqomw==/lib/arm64/libbase.cr.so (base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+232) (BuildId: bb92b0f43ac6f384)
01-21 15:42:31.246 19084 19084 F DEBUG   :       #36 pc 00000000003d1bb8  /data/app/~~3TLx5oqswNbd9-q6R5wzWg==/org.chromium.chrome-Pgd-CbytKw65rQOCYhqomw==/lib/arm64/libbase.cr.so (base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)+868) (BuildId: bb92b0f43ac6f384)
01-21 15:42:31.246 19084 19084 F DEBUG   :       #37 pc 00000000003d16dc  /data/app/~~3TLx5oqswNbd9-q6R5wzWg==/org.chromium.chrome-Pgd-CbytKw65rQOCYhqomw==/lib/arm64/libbase.cr.so (base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+100) (BuildId: bb92b0f43ac6f384)
01-21 15:42:31.246 19084 19084 F DEBUG   :       #38 pc 000000000032933c  /data/app/~~3TLx5oqswNbd9-q6R5wzWg==/org.chromium.chrome-Pgd-CbytKw65rQOCYhqomw==/lib/arm64/libbase.cr.so (base::MessagePumpDefault::Run(base::MessagePump::Delegate*)+116) (BuildId: bb92b0f43ac6f384)
01-21 15:42:31.246 19084 19084 F DEBUG   :       #39 pc 00000000003d21c4  /data/app/~~3TLx5oqswNbd9-q6R5wzWg==/org.chromium.chrome-Pgd-CbytKw65rQOCYhqomw==/lib/arm64/libbase.cr.so (base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta)+296) (BuildId: bb92b0f43ac6f384)
01-21 15:42:31.246 19084 19084 F DEBUG   :       #40 pc 0000000000376320  /data/app/~~3TLx5oqswNbd9-q6R5wzWg==/org.chromium.chrome-Pgd-CbytKw65rQOCYhqomw==/lib/arm64/libbase.cr.so (base::RunLoop::Run(base::Location const&)+388) (BuildId: bb92b0f43ac6f384)
01-21 15:42:31.246 19084 19084 F DEBUG   :       #41 pc 00000000021d01fc  /data/app/~~3TLx5oqswNbd9-q6R5wzWg==/org.chromium.chrome-Pgd-CbytKw65rQOCYhqomw==/lib/arm64/libcontent.cr.so (BuildId: 5f02796b7bfabdd5)
01-21 15:42:31.247 19084 19084 F DEBUG   :       #42 pc 0000000004368dcc  /data/app/~~3TLx5oqswNbd9-q6R5wzWg==/org.chromium.chrome-Pgd-CbytKw65rQOCYhqomw==/lib/arm64/libcontent.cr.so (BuildId: 5f02796b7bfabdd5)
01-21 15:42:31.247 19084 19084 F DEBUG   :       #43 pc 0000000004369a00  /data/app/~~3TLx5oqswNbd9-q6R5wzWg==/org.chromium.chrome-Pgd-CbytKw65rQOCYhqomw==/lib/arm64/libcontent.cr.so (BuildId: 5f02796b7bfabdd5)
01-21 15:42:31.247 19084 19084 F DEBUG   :       #44 pc 000000000436717c  /data/app/~~3TLx5oqswNbd9-q6R5wzWg==/org.chromium.chrome-Pgd-CbytKw65rQOCYhqomw==/lib/arm64/libcontent.cr.so (content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*)+268) (BuildId: 5f02796b7bfabdd5)
01-21 15:42:31.247 19084 19084 F DEBUG   :       #45 pc 00000000043682bc  /data/app/~~3TLx5oqswNbd9-q6R5wzWg==/org.chromium.chrome-Pgd-CbytKw65rQOCYhqomw==/lib/arm64/libcontent.cr.so (Java_org_jni_1zero_GEN_1JNI_org_1chromium_1content_1app_1ContentMain_1start+136) (BuildId: 5f02796b7bfabdd5)
01-21 15:42:31.247 19084 19084 F DEBUG   :       #46 pc 0000000000383d70  /apex/com.android.art/lib64/libart.so (art_quick_generic_jni_trampoline+144) (BuildId: c35c9ebf7bb06435e4b31977d87bd5d5)
01-21 15:42:31.247 19084 19084 F DEBUG   :       #47 pc 000000000036d840  /apex/com.android.art/lib64/libart.so (art_quick_invoke_static_stub+640) (BuildId: c35c9ebf7bb06435e4b31977d87bd5d5)
01-21 15:42:31.247 19084 19084 F DEBUG   :       #48 pc 0000000000366af8  /apex/com.android.art/lib64/libart.so (bool art::interpreter::DoCall<false>(art::ArtMethod*, art::Thread*, art::ShadowFrame&, art::Instruction const*, unsigned short, bool, art::JValue*)+2048) (BuildId: c35c9ebf7bb06435e4b31977d87bd5d5)
01-21 15:42:31.247 19084 19084 F DEBUG   :       #49 pc 000000000076e870  /apex/com.android.art/lib64/libart.so (void art::interpreter::ExecuteSwitchImplCpp<false>(art::interpreter::SwitchImplContext*)+12208) (BuildId: c35c9ebf7bb06435e4b31977d87bd5d5)
01-21 15:42:31.247 19084 19084 F DEBUG   :       #50 pc 00000000003863d8  /apex/com.android.art/lib64/libart.so (ExecuteSwitchImplAsm+8) (BuildId: c35c9ebf7bb06435e4b31977d87bd5d5)
01-21 15:42:31.247 19084 19084 F DEBUG   :       #51 pc 0000000000269300  [anon:dalvik-classes6.dex extracted in memory from /data/app/~~3TLx5oqswNbd9-q6R5wzWg==/org.chromium.chrome-Pgd-CbytKw65rQOCYhqomw==/base.apk] (org.chromium.content.app.ContentMainJni.start+0)
01-21 15:42:31.247 19084 19084 F DEBUG   :       #52 pc 0000000000358eec  /apex/com.android.art/lib64/libart.so (art::interpreter::Execute(art::Thread*, art::CodeItemDataAccessor const&, art::ShadowFrame&, art::JValue, bool, bool) (.__uniq.112435418011751916792819755956732575238.llvm.17771861963221910393)+428) (BuildId: c35c9ebf7bb06435e4b31977d87bd5d5)
01-21 15:42:31.247 19084 19084 F DEBUG   :       #53 pc 0000000000367314  /apex/com.android.art/lib64/libart.so (bool art::interpreter::DoCall<false>(art::ArtMethod*, art::Thread*, art::ShadowFrame&, art::Instruction const*, unsigned short, bool, art::JValue*)+4124) (BuildId: c35c9ebf7bb06435e4b31977d87bd5d5)
01-21 15:42:31.247 19084 19084 F DEBUG   :       #54 pc 000000000076e870  /apex/com.android.art/lib64/libart.so (void art::interpreter::ExecuteSwitchImplCpp<false>(art::interpreter::SwitchImplContext*)+12208) (BuildId: c35c9ebf7bb06435e4b31977d87bd5d5)
01-21 15:42:31.247 19084 19084 F DEBUG   :       #55 pc 00000000003863d8  /apex/com.android.art/lib64/libart.so (ExecuteSwitchImplAsm+8) (BuildId: c35c9ebf7bb06435e4b31977d87bd5d5)
01-21 15:42:31.247 19084 19084 F DEBUG   :       #56 pc 00000000002693b8  [anon:dalvik-classes6.dex extracted in memory from /data/app/~~3TLx5oqswNbd9-q6R5wzWg==/org.chromium.chrome-Pgd-CbytKw65rQOCYhqomw==/base.apk] (org.chromium.content.app.ContentMain.start+0)
01-21 15:42:31.247 19084 19084 F DEBUG   :       #57 pc 0000000000358eec  /apex/com.android.art/lib64/libart.so (art::interpreter::Execute(art::Thread*, art::CodeItemDataAccessor const&, art::ShadowFrame&, art::JValue, bool, bool) (.__uniq.112435418011751916792819755956732575238.llvm.17771861963221910393)+428) (BuildId: c35c9ebf7bb06435e4b31977d87bd5d5)
01-21 15:42:31.247 19084 19084 F DEBUG   :       #58 pc 0000000000367314  /apex/com.android.art/lib64/libart.so (bool art::interpreter::DoCall<false>(art::ArtMethod*, art::Thread*, art::ShadowFrame&, art::Instruction const*, unsigned short, bool, art::JValue*)+4124) (BuildId: c35c9ebf7bb06435e4b31977d87bd5d5)
01-21 15:42:31.247 19084 19084 F DEBUG   :       #59 pc 000000000076e870  /apex/com.android.art/lib64/libart.so (void art::interpreter::ExecuteSwitchImplCpp<false>(art::interpreter::SwitchImplContext*)+12208) (BuildId: c35c9ebf7bb06435e4b31977d87bd5d5)
01-21 15:42:31.247 19084 19084 F DEBUG   :       #60 pc 00000000003863d8  /apex/com.android.art/lib64/libart.so (ExecuteSwitchImplAsm+8) (BuildId: c35c9ebf7bb06435e4b31977d87bd5d5)
01-21 15:42:31.247 19084 19084 F DEBUG   :       #61 pc 00000000002691c8  [anon:dalvik-classes6.dex extracted in memory from /data/app/~~3TLx5oqswNbd9-q6R5wzWg==/org.chromium.chrome-Pgd-CbytKw65rQOCYhqomw==/base.apk] (org.chromium.content.app.ContentChildProcessServiceDelegate.runMain+0)
01-21 15:42:31.247 19084 19084 F DEBUG   :       #62 pc 0000000000358eec  /apex/com.android.art/lib64/libart.so (art::interpreter::Execute(art::Thread*, art::CodeItemDataAccessor const&, art::ShadowFrame&, art::JValue, bool, bool) (.__uniq.112435418011751916792819755956732575238.llvm.17771861963221910393)+428) (BuildId: c35c9ebf7bb06435e4b31977d87bd5d5)
:
01-21 15:42:31.247 19084 19084 F DEBUG   :       #63 pc 0000000000367314  /apex/com.android.art/lib64/libart.so (bool art::interpreter::DoCall<false>(art::ArtMethod*, art::Thread*, art::ShadowFrame&, art::Instruction const*, unsigned short, bool, art::JValue*)+4124) (BuildId: c35c9ebf7bb06435e4b31977d87bd5d5)
01-21 15:42:31.247 19084 19084 F DEBUG   :       #64 pc 000000000076e870  /apex/com.android.art/lib64/libart.so (void art::interpreter::ExecuteSwitchImplCpp<false>(art::interpreter::SwitchImplContext*)+12208) (BuildId: c35c9ebf7bb06435e4b31977d87bd5d5)
01-21 15:42:31.247 19084 19084 F DEBUG   :       #65 pc 00000000003863d8  /apex/com.android.art/lib64/libart.so (ExecuteSwitchImplAsm+8) (BuildId: c35c9ebf7bb06435e4b31977d87bd5d5)
01-21 15:42:31.247 19084 19084 F DEBUG   :       #66 pc 00000000002893d4  [anon:dalvik-classes3.dex extracted in memory from /data/app/~~3TLx5oqswNbd9-q6R5wzWg==/org.chromium.chrome-Pgd-CbytKw65rQOCYhqomw==/base.apk] (org.chromium.base.process_launcher.ChildProcessService.mainThreadMain+0)
01-21 15:42:31.247 19084 19084 F DEBUG   :       #67 pc 0000000000358eec  /apex/com.android.art/lib64/libart.so (art::interpreter::Execute(art::Thread*, art::CodeItemDataAccessor const&, art::ShadowFrame&, art::JValue, bool, bool) (.__uniq.112435418011751916792819755956732575238.llvm.17771861963221910393)+428) (BuildId: c35c9ebf7bb06435e4b31977d87bd5d5)
01-21 15:42:31.247 19084 19084 F DEBUG   :       #68 pc 0000000000367314  /apex/com.android.art/lib64/libart.so (bool art::interpreter::DoCall<false>(art::ArtMethod*, art::Thread*, art::ShadowFrame&, art::Instruction const*, unsigned short, bool, art::JValue*)+4124) (BuildId: c35c9ebf7bb06435e4b31977d87bd5d5)
01-21 15:42:31.247 19084 19084 F DEBUG   :       #69 pc 000000000076e870  /apex/com.android.art/lib64/libart.so (void art::interpreter::ExecuteSwitchImplCpp<false>(art::interpreter::SwitchImplContext*)+12208) (BuildId: c35c9ebf7bb06435e4b31977d87bd5d5)
01-21 15:42:31.247 19084 19084 F DEBUG   :       #70 pc 00000000003863d8  /apex/com.android.art/lib64/libart.so (ExecuteSwitchImplAsm+8) (BuildId: c35c9ebf7bb06435e4b31977d87bd5d5)
01-21 15:42:31.248 19084 19084 F DEBUG   :       #71 pc 00000000002892dc  [anon:dalvik-classes3.dex extracted in memory from /data/app/~~3TLx5oqswNbd9-q6R5wzWg==/org.chromium.chrome-Pgd-CbytKw65rQOCYhqomw==/base.apk] (org.chromium.base.process_launcher.ChildProcessService.$r8$lambda$eZUxkj2POTXO6oIHcFpMMaOTgqA+0)
01-21 15:42:31.248 19084 19084 F DEBUG   :       #72 pc 0000000000358eec  /apex/com.android.art/lib64/libart.so (art::interpreter::Execute(art::Thread*, art::CodeItemDataAccessor const&, art::ShadowFrame&, art::JValue, bool, bool) (.__uniq.112435418011751916792819755956732575238.llvm.17771861963221910393)+428) (BuildId: c35c9ebf7bb06435e4b31977d87bd5d5)
01-21 15:42:31.248 19084 19084 F DEBUG   :       #73 pc 0000000000367314  /apex/com.android.art/lib64/libart.so (bool art::interpreter::DoCall<false>(art::ArtMethod*, art::Thread*, art::ShadowFrame&, art::Instruction const*, unsigned short, bool, art::JValue*)+4124) (BuildId: c35c9ebf7bb06435e4b31977d87bd5d5)
01-21 15:42:31.248 19084 19084 F DEBUG   :       #74 pc 000000000076e870  /apex/com.android.art/lib64/libart.so (void art::interpreter::ExecuteSwitchImplCpp<false>(art::interpreter::SwitchImplContext*)+12208) (BuildId: c35c9ebf7bb06435e4b31977d87bd5d5)
01-21 15:42:31.248 19084 19084 F DEBUG   :       #75 pc 00000000003863d8  /apex/com.android.art/lib64/libart.so (ExecuteSwitchImplAsm+8) (BuildId: c35c9ebf7bb06435e4b31977d87bd5d5)
01-21 15:42:31.248 19084 19084 F DEBUG   :       #76 pc 0000000000288b18  [anon:dalvik-classes3.dex extracted in memory from /data/app/~~3TLx5oqswNbd9-q6R5wzWg==/org.chromium.chrome-Pgd-CbytKw65rQOCYhqomw==/base.apk] (org.chromium.base.process_launcher.ChildProcessService$$ExternalSyntheticLambda1.run+0)
01-21 15:42:31.248 19084 19084 F DEBUG   :       #77 pc 0000000000358278  /apex/com.android.art/lib64/libart.so (artQuickToInterpreterBridge+1932) (BuildId: c35c9ebf7bb06435e4b31977d87bd5d5)
01-21 15:42:31.248 19084 19084 F DEBUG   :       #78 pc 0000000000383e98  /apex/com.android.art/lib64/libart.so (art_quick_to_interpreter_bridge+88) (BuildId: c35c9ebf7bb06435e4b31977d87bd5d5)
01-21 15:42:31.248 19084 19084 F DEBUG   :       #79 pc 0000000002004568  /memfd:jit-cache (deleted) (offset 0x2000000) (java.lang.Thread.run+136)
01-21 15:42:31.248 19084 19084 F DEBUG   :       #80 pc 000000000036d574  /apex/com.android.art/lib64/libart.so (art_quick_invoke_stub+612) (BuildId: c35c9ebf7bb06435e4b31977d87bd5d5)
01-21 15:42:31.248 19084 19084 F DEBUG   :       #81 pc 0000000000358bc0  /apex/com.android.art/lib64/libart.so (art::ArtMethod::Invoke(art::Thread*, unsigned int*, unsigned int, art::JValue*, char const*)+132) (BuildId: c35c9ebf7bb06435e4b31977d87bd5d5)
01-21 15:42:31.248 19084 19084 F DEBUG   :       #82 pc 0000000000944608  /apex/com.android.art/lib64/libart.so (art::detail::ShortyTraits<(char)86>::Type art::ArtMethod::InvokeInstance<(char)86>(art::Thread*, art::ObjPtr<art::mirror::Object>, art::detail::ShortyTraits<>::Type...)+60) (BuildId: c35c9ebf7bb06435e4b31977d87bd5d5)
01-21 15:42:31.248 19084 19084 F DEBUG   :       #83 pc 0000000000625d24  /apex/com.android.art/lib64/libart.so (art::Thread::CreateCallback(void*)+1344) (BuildId: c35c9ebf7bb06435e4b31977d87bd5d5)
01-21 15:42:31.248 19084 19084 F DEBUG   :       #84 pc 00000000006257d4  /apex/com.android.art/lib64/libart.so (art::Thread::CreateCallbackWithUffdGc(void*)+8) (BuildId: c35c9ebf7bb06435e4b31977d87bd5d5)
01-21 15:42:31.248 19084 19084 F DEBUG   :       #85 pc 00000000000705f4  /apex/com.android.runtime/lib64/bionic/libc.so (__pthread_start(void*)+132) (BuildId: d607b2dd86e0ffc603529ce13afab7fa)
01-21 15:42:31.248 19084 19084 F DEBUG   :       #86 pc 0000000000061870  /apex/com.android.runtime/lib64/bionic/libc.so (__start_thread+64) (BuildId: d607b2dd86e0ffc603529ce13afab7fa)
01-21 15:42:31.248 19084 19084 F DEBUG   : Learn more about MTE reports: https://source.android.com/docs/security/test/memory-safety/mte-reports
01-21 15:42:31.368   696   696 E tombstoned: Tombstone written to: tombstone_21
01-21 15:42:31.374  1675 19093 I DropBoxManagerService: add tag=data_app_native_crash isTagEnabled=true flags=0x6

```
##### REPRODUCTION CASE (Standalone)

- Compile the attached standalone.cpp via: `~/android-ndk-r27/toolchains/llvm/prebuilt/linux-x86_64/bin/x86_64-linux-android35-clang++ --target=aarch64-linux-android35 -lvulkan standalone.cpp -o reproducer`
- Push the resulting binary, vert.spv, and frag.spv onto the device.
- Enable MTE sync for the reproducer: `adb shell setprop arm64.memtag.process.reproducer sync`
- Run the reproducer via `./reproducer vert.spv frag.spv`

This should result in the following backtrace:

```
01-21 16:49:20.875 24062 24062 F DEBUG   : *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** ***
01-21 16:49:20.875 24062 24062 F DEBUG   : Build fingerprint: 'google/akita/akita:15/AP4A.241205.013/12621605:user/release-keys'
01-21 16:49:20.875 24062 24062 F DEBUG   : Revision: 'MP1.0'
01-21 16:49:20.875 24062 24062 F DEBUG   : ABI: 'arm64'
01-21 16:49:20.875 24062 24062 F DEBUG   : Timestamp: 2025-01-21 16:49:20.731788224+0100
01-21 16:49:20.875 24062 24062 F DEBUG   : Process uptime: 1s
01-21 16:49:20.875 24062 24062 F DEBUG   : Cmdline: ./reproducer vert.spv frag.spv
01-21 16:49:20.875 24062 24062 F DEBUG   : pid: 24053, tid: 24053, name: reproducer  >>> ./reproducer <<<
01-21 16:49:20.875 24062 24062 F DEBUG   : uid: 2000
01-21 16:49:20.875 24062 24062 F DEBUG   : tagged_addr_ctrl: 000000000007fff3 (PR_TAGGED_ADDR_ENABLE, PR_MTE_TCF_SYNC, mask 0xfffe)
01-21 16:49:20.875 24062 24062 F DEBUG   : pac_enabled_keys: 000000000000000f (PR_PAC_APIAKEY, PR_PAC_APIBKEY, PR_PAC_APDAKEY, PR_PAC_APDBKEY)
01-21 16:49:20.875 24062 24062 F DEBUG   : signal 11 (SIGSEGV), code 9 (SEGV_MTESERR), fault addr 0x0e00007d0e4e2830
01-21 16:49:20.875 24062 24062 F DEBUG   : Cause: [MTE]: Use After Free, 112 bytes into a 160-byte allocation at 0x7d0e4e27c0
01-21 16:49:20.875 24062 24062 F DEBUG   :     x0  0e00007d0e4e2820  x1  0000007fcccd6cd0  x2  0000000000000002  x3  0000007fcccd7b40
01-21 16:49:20.875 24062 24062 F DEBUG   :     x4  0a00007b5e4d8660  x5  0c00007bfe4e3de4  x6  0000000000000001  x7  0000000000000001
01-21 16:49:20.875 24062 24062 F DEBUG   :     x8  4a732c7b76ed2730  x9  4a732c7b76ed2730  x10 0000007b58d40bd4  x11 0000007b5b119808
01-21 16:49:20.875 24062 24062 F DEBUG   :     x12 000000000000007e  x13 0000000000000000  x14 00000000fffffffe  x15 00000000ffffffff
01-21 16:49:20.875 24062 24062 F DEBUG   :     x16 0000000000000014  x17 0000000000000001  x18 0000007df5a24000  x19 0500007c8e4da238
01-21 16:49:20.875 24062 24062 F DEBUG   :     x20 0000007df541af80  x21 0000000000000000  x22 0000000000000008  x23 0000007fcccd6cd0
01-21 16:49:20.876 24062 24062 F DEBUG   :     x24 0000007df541af80  x25 0700007d3e4dad00  x26 0500007c8e4da238  x27 0000007fcccd7b40
01-21 16:49:20.876 24062 24062 F DEBUG   :     x28 0000000000000000  x29 0000000000000000
01-21 16:49:20.876 24062 24062 F DEBUG   :     lr  0000007b5b119858  sp  0000007fcccd6ad0  pc  0000007b5a833d38  pst 0000000020001000
01-21 16:49:20.876 24062 24062 F DEBUG   : 17 total frames
01-21 16:49:20.876 24062 24062 F DEBUG   : backtrace:
01-21 16:49:20.876 24062 24062 F DEBUG   :   NOTE: Function names and BuildId information is missing for some frames due
01-21 16:49:20.876 24062 24062 F DEBUG   :   NOTE: to unreadable libraries. For unwinds of apps, only shared libraries
01-21 16:49:20.876 24062 24062 F DEBUG   :   NOTE: found under the lib/ directory are readable.
01-21 16:49:20.876 24062 24062 F DEBUG   :   NOTE: On this device, run setenforce 0 to make the libraries readable.
01-21 16:49:20.876 24062 24062 F DEBUG   :   NOTE: Unreadable libraries:
01-21 16:49:20.876 24062 24062 F DEBUG   :   NOTE:   /data/local/tmp/reproducer
01-21 16:49:20.876 24062 24062 F DEBUG   :       #00 pc 0000000002014d38  /vendor/lib64/egl/libGLES_mali.so (llvm::PatternMatch::undef_match::check(llvm::Value const*)+24) (BuildId: ba412f8560df6af8)
01-21 16:49:20.876 24062 24062 F DEBUG   :       #01 pc 00000000028fa854  /vendor/lib64/egl/libGLES_mali.so (simplifyInstructionWithOperands(llvm::Instruction*, llvm::ArrayRef<llvm::Value*>, llvm::Simp
lifyQuery const&, llvm::OptimizationRemarkEmitter*) (.llvm.13836456976102157447)+692) (BuildId: ba412f8560df6af8)
01-21 16:49:20.876 24062 24062 F DEBUG   :       #02 pc 00000000028fb188  /vendor/lib64/egl/libGLES_mali.so (llvm::SimplifyInstruction(llvm::Instruction*, llvm::SimplifyQuery const&, llvm::Optimization
RemarkEmitter*)+344) (BuildId: ba412f8560df6af8)
01-21 16:49:20.876 24062 24062 F DEBUG   :       #03 pc 0000000002663bcc  /vendor/lib64/egl/libGLES_mali.so (llvm::GVNPass::runImpl(llvm::Function&, llvm::AssumptionCache&, llvm::DominatorTree&, llvm::
TargetLibraryInfo const&, llvm::AAResults&, llvm::MemoryDependenceResults*, llvm::LoopInfo*, llvm::OptimizationRemarkEmitter*, llvm::MemorySSA*)+1820) (BuildId: ba412f8560df6af8)
01-21 16:49:20.876 24062 24062 F DEBUG   :       #04 pc 000000000266ca74  /vendor/lib64/egl/libGLES_mali.so (llvm::gvn::GVNLegacyPass::runOnFunction(llvm::Function&)+580) (BuildId: ba412f8560df6af8)
01-21 16:49:20.876 24062 24062 F DEBUG   :       #05 pc 00000000021cd050  /vendor/lib64/egl/libGLES_mali.so ((anonymous namespace)::MaliFunctionPassManager::runOnModule(llvm::Module&)+544) (BuildId: ba
412f8560df6af8)
01-21 16:49:20.876 24062 24062 F DEBUG   :       #06 pc 00000000021cc420  /vendor/lib64/egl/libGLES_mali.so ((anonymous namespace)::MaliModulePassManager::runOnModule(llvm::Module&)+400) (BuildId: ba41
2f8560df6af8)
01-21 16:49:20.876 24062 24062 F DEBUG   :       #07 pc 00000000021c80ac  /vendor/lib64/egl/libGLES_mali.so (llvm::Mali::StaticPassManager::TLPassManagerImpl::run(llvm::Module&)+252) (BuildId: ba412f85
60df6af8)
01-21 16:49:20.876 24062 24062 F DEBUG   :       #08 pc 0000000001aed77c  /vendor/lib64/egl/libGLES_mali.so (cmpbep_bfr_run_llvm_backend+2044) (BuildId: ba412f8560df6af8)
01-21 16:49:20.876 24062 24062 F DEBUG   :       #09 pc 0000000001af29d4  /vendor/lib64/egl/libGLES_mali.so (cmpbe_compile_gles_shader+660) (BuildId: ba412f8560df6af8)
01-21 16:49:20.876 24062 24062 F DEBUG   :       #10 pc 0000000001b1769c  /vendor/lib64/egl/libGLES_mali.so (do_single_part2_compilation+188) (BuildId: ba412f8560df6af8)
01-21 16:49:20.876 24062 24062 F DEBUG   :       #11 pc 0000000001b173d8  /vendor/lib64/egl/libGLES_mali.so (cmpbe_v2_compile_multiple_shaders+9944) (BuildId: ba412f8560df6af8)
01-21 16:49:20.876 24062 24062 F DEBUG   :       #12 pc 0000000001a0cf4c  /vendor/lib64/egl/libGLES_mali.so (gfx::compiler::compile_shaders(gfx::shader_set const&, gfx::shader_set&, hal::shader_language, gfx::shader_state const&, compiler_cache*, gfx::mem_allocator&, cutils_cmpbe_dump_ctx**, bool*, unsigned long*)+6956) (BuildId: ba412f8560df6af8)
01-21 16:49:20.876 24062 24062 F DEBUG   :       #13 pc 00000000009330e4  /vendor/lib64/egl/libGLES_mali.so (vkCreateGraphicsPipelines+12164) (BuildId: ba412f8560df6af8)
01-21 16:49:20.876 24062 24062 F DEBUG   :       #14 pc 00000000000063dc  /data/local/tmp/reproducer
01-21 16:49:20.876 24062 24062 F DEBUG   :       #15 pc 000000000000690c  /data/local/tmp/reproducer
01-21 16:49:20.876 24062 24062 F DEBUG   :       #16 pc 0000000000057854  /apex/com.android.runtime/lib64/bionic/libc.so (__libc_init+116) (BuildId: d607b2dd86e0ffc603529ce13afab7fa)
01-21 16:49:20.876 24062 24062 F DEBUG   : deallocated by thread 24053:
01-21 16:49:20.876 24062 24062 F DEBUG   :       #00 pc 00000000000518b8  /apex/com.android.runtime/lib64/bionic/libc.so (scudo::Allocator<scudo::AndroidNormalConfig, &scudo_malloc_postinit>::quarantineOrDeallocateChunk(scudo::Options const&, void*, scudo::Chunk::UnpackedHeader*, unsigned long)+968) (BuildId: d607b2dd86e0ffc603529ce13afab7fa)
01-21 16:49:20.877 24062 24062 F DEBUG   :       #01 pc 000000000004b8f0  /apex/com.android.runtime/lib64/bionic/libc.so (scudo::Allocator<scudo::AndroidNormalConfig, &scudo_malloc_postinit>::deallocate(void*, scudo::Chunk::Origin, unsigned long, unsigned long)+192) (BuildId: d607b2dd86e0ffc603529ce13afab7fa)
01-21 16:49:20.877 24062 24062 F DEBUG   :       #02 pc 0000000002b13990  /vendor/lib64/egl/libGLES_mali.so (llvm::Instruction::eraseFromParent()+48) (BuildId: ba412f8560df6af8)
01-21 16:49:20.877 24062 24062 F DEBUG   : allocated by thread 24053:
01-21 16:49:20.877 24062 24062 F DEBUG   :       #00 pc 000000000004b744  /apex/com.android.runtime/lib64/bionic/libc.so (scudo::Allocator<scudo::AndroidNormalConfig, &scudo_malloc_postinit>::allocate(unsigned long, scudo::Chunk::Origin, unsigned long, bool)+852) (BuildId: d607b2dd86e0ffc603529ce13afab7fa)
01-21 16:49:20.877 24062 24062 F DEBUG   :       #01 pc 000000000004bab4  /apex/com.android.runtime/lib64/bionic/libc.so (scudo_malloc+36) (BuildId: d607b2dd86e0ffc603529ce13afab7fa)
01-21 16:49:20.877 24062 24062 F DEBUG   :       #02 pc 00000000000456dc  /apex/com.android.runtime/lib64/bionic/libc.so (malloc+44) (BuildId: d607b2dd86e0ffc603529ce13afab7fa)
01-21 16:49:20.877 24062 24062 F DEBUG   :       #03 pc 00000000000eb97c  /vendor/lib64/libc++.so (operator new(unsigned long)+28) (BuildId: 94744eed32fba2eb636a9d2e5365a00614c1b4ae)
01-21 16:49:20.877 24062 24062 F DEBUG   :       #04 pc 0000000002b5a844  /vendor/lib64/egl/libGLES_mali.so (llvm::User::operator new(unsigned long, unsigned int)+20) (BuildId: ba412f8560df6af8)
01-21 16:49:20.877 24062 24062 F DEBUG   : Learn more about MTE reports: https://source.android.com/docs/security/test/memory-safety/mte-reports

```

## Attachments

- frag.spv (application/octet-stream, 3.1 KB)
- vert.spv (application/octet-stream, 512 B)
- a.html (text/html, 4.7 KB)
- standalone.cpp (text/x-c++src, 12.0 KB)

## Timeline

### a7...@gmail.com (2025-01-21)

Upstream issue: ARMSEC-325

### ct...@chromium.org (2025-01-22)

Thank you for the report. I don't currently have an MTE-enabled device to repro this on, but the report and stack traces appear valid to me, so doing initial triage to get quick visibility on this -- I'll separately work on verifying the repro. Setting this to Sev-Crit (P0/S0) as this impacts GPU on Android (unsandboxed) per <https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/severity-guidelines.md#toc-critical-severity>.

jrprice@ could you PTAL at this SPIR-V related vulnerability or help re-assign to someone on the GPU side of things who can help take a look?

My understanding is that we apply SPIR-V validation on ChromeOS and Linux, so marking this as affecting only Chrome on Android, but looping in other folks per our GPU bug triage guidelines [1](https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/shepherd.md#:~:text=GPU%20driver%20bugs,from%20ChromeOS%20GPU.). As this is in Mali drivers, +aygupta@, bcreasey@, asdl-kfc@ for Android, +mjstokes@ and layog@ for Pixel, and +robdclark@ and msturner@ for ChromeOS for visibility.

### ct...@chromium.org (2025-01-22)

@reporter: Have you also been able to repro against Chrome 132 (Stable) or 133 (Beta) on Android? My guess is that this may be equally reachable there if it is tickling an issue in the same underlying driver.

### a7...@gmail.com (2025-01-22)

I tested Chromium 132.0.6834.79, the version did not trigger an MTE violation. Bisecting Chromium identifies the first bad commit as:

```
6f35744d771cd7a3587a8d20691869f0927eaa1a
Manual roll Dawn from 12a3b24c456c to e0d7445de8cd

```

Fixing the last good version of Chromium, I bisected Dawn on the commit range 12a3b24c456c to e0d7445de8cd. This identifies the following commit as the first bad one:

```
2fce40705f903a3b28973c0764d610aea5bcf54c
[spirv] Use PreventInfiniteLoops transform

```

### ar...@google.com (2025-01-22)

+CC [keishi@chromium.org](mailto:keishi@chromium.org) who work on MTE FYI

### ms...@google.com (2025-01-22)

deleted

### ct...@chromium.org (2025-01-22)

Thank you for checking other channels and for doing the bisect, that is very helpful! Based on those results I'm going to tentatively set this as FoundIn-133 (based on when the Dawn roll happened in Chromium [1](https://chromiumdash.appspot.com/commit/6f35744d771cd7a3587a8d20691869f0927eaa1a)). The Dawn bisect points to <https://dawn-review.googlesource.com/c/dawn/+/217374>.

### pe...@google.com (2025-01-23)

Setting milestone because of s0/s1 severity.

### ds...@chromium.org (2025-01-23)

Have we heard back from Arm as to what the code pattern is that is generating the crash? We need to know what's triggering the issue in order to determine if we can work around this issue.

### a7...@gmail.com (2025-01-27)

I haven't received an update so far but will forward you any news.

### a7...@gmail.com (2025-02-05)

Update from ARM:

```
Hi XXX,

A quick update for this report - we have assessed the problem as a High Severity security issue affecting our Mali GPU Drivers. We have allocated CVE-2025-0932 for it.

We are working on a fix now and are working toward setting a date for Coordinated Vulnerability Disclosure once we know the timelines; we’ll let you know once we’ve set the date(s) for those steps.

Don’t hesitate to reach out if you have any questions in the mean time, of course.

Thanks!

XXX

Arm PSIRT

```

### pe...@google.com (2025-02-11)

jrprice: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### jr...@google.com (2025-02-18)

I've tried to reproduce this on a Pixel 9 with the standalone reproducer with no luck. I've run it 1000 times with `MEMTAG_OPTIONS=sync` but no crashes appeared in `adb logcat`. I can try and reproduce via Chrome hopefully tomorrow when I have physical access to the device.

a72827312@ are you able to add me ([jrprice@google.com](mailto:jrprice@google.com)) to the ticket that was filed with Arm?

### jr...@google.com (2025-02-18)

@amyressler should we add SI-None to this issue as we are waiting for more details from Arm, similar to [crbug.com/379551588#comment37](https://crbug.com/379551588#comment37)?

### a7...@gmail.com (2025-02-19)

I don't have access to the ticket either but contact via mail only. I suppose your best chance is inquiring regarding ARMSEC-325 at [psirt@arm.com](mailto:psirt@arm.com). FWIW: I asked ARM to provide you/Google a workaround on Feb 10 so they should be working on this.

I don't have a Pixel 9 at hand, but I did try to run it on a Pixel 8 (in contrast to the original report, which was a Pixel 8a). On the Pixel 8, this results in a deterministic crash (same as on the Pixel 8a); running the reproducer multiple times should not be necessary.

Pixel 8 adb logcat:

```
02-19 08:49:56.242  7733  7733 F DEBUG   : Build fingerprint: 'google/shiba/shiba:15/AP4A.250205.002/12821496:user/release-keys'
02-19 08:49:56.242  7733  7733 F DEBUG   : Revision: 'MP1.0'
02-19 08:49:56.242  7733  7733 F DEBUG   : ABI: 'arm64'
02-19 08:49:56.242  7733  7733 F DEBUG   : Timestamp: 2025-02-19 08:49:56.196442510+0100
02-19 08:49:56.242  7733  7733 F DEBUG   : Process uptime: 1s
02-19 08:49:56.242  7733  7733 F DEBUG   : Cmdline: ./reproducer vert.spv frag.spv
02-19 08:49:56.242  7733  7733 F DEBUG   : pid: 7723, tid: 7723, name: reproducer  >>> ./reproducer <<<
02-19 08:49:56.242  7733  7733 F DEBUG   : uid: 2000
02-19 08:49:56.242  7733  7733 F DEBUG   : tagged_addr_ctrl: 000000000007fff3 (PR_TAGGED_ADDR_ENABLE, PR_MTE_TCF_SYNC, mask 0xfffe)
02-19 08:49:56.242  7733  7733 F DEBUG   : pac_enabled_keys: 000000000000000f (PR_PAC_APIAKEY, PR_PAC_APIBKEY, PR_PAC_APDAKEY, PR_PAC_APDBKEY)
02-19 08:49:56.242  7733  7733 F DEBUG   : signal 11 (SIGSEGV), code 9 (SEGV_MTESERR), fault addr 0x0a000075e1af3780
02-19 08:49:56.242  7733  7733 F DEBUG   : Cause: [MTE]: Use After Free, 112 bytes into a 160-byte allocation at 0x75e1af3710
02-19 08:49:56.242  7733  7733 F DEBUG   :     x0  0a000075e1af3770  x1  0000007ff5207710  x2  0000000000000002  x3  0000007ff5208580
02-19 08:49:56.242  7733  7733 F DEBUG   :     x4  0b000074d1aeec20  x5  03000074e1ae9644  x6  0000000000000001  x7  0000000000000001
02-19 08:49:56.242  7733  7733 F DEBUG   :     x8  ff473b86ad71c165  x9  ff473b86ad71c165  x10 000000740d725bd4  x11 000000740fafe808
02-19 08:49:56.242  7733  7733 F DEBUG   :     x12 000000000000007e  x13 0000000000000000  x14 00000000fffffffe  x15 00000000ffffffff
02-19 08:49:56.242  7733  7733 F DEBUG   :     x16 0000000000000014  x17 0000000000000001  x18 00000076a8d30000  x19 07000075c1af16b8
02-19 08:49:56.242  7733  7733 F DEBUG   :     x20 00000076a8628f80  x21 0000000000000000  x22 0000000000000008  x23 0000007ff5207710
02-19 08:49:56.242  7733  7733 F DEBUG   :     x24 00000076a8628f80  x25 03000074f1af40f0  x26 07000075c1af16b8  x27 0000007ff5208580
02-19 08:49:56.242  7733  7733 F DEBUG   :     x28 0000000000000000  x29 0000000000000000
02-19 08:49:56.242  7733  7733 F DEBUG   :     lr  000000740fafe858  sp  0000007ff5207510  pc  000000740f218d38  pst 0000000020001000
02-19 08:49:56.242  7733  7733 F DEBUG   : 17 total frames
02-19 08:49:56.242  7733  7733 F DEBUG   : backtrace:
02-19 08:49:56.242  7733  7733 F DEBUG   :   NOTE: Function names and BuildId information is missing for some frames due
02-19 08:49:56.242  7733  7733 F DEBUG   :   NOTE: to unreadable libraries. For unwinds of apps, only shared libraries
02-19 08:49:56.242  7733  7733 F DEBUG   :   NOTE: found under the lib/ directory are readable.
02-19 08:49:56.242  7733  7733 F DEBUG   :   NOTE: On this device, run setenforce 0 to make the libraries readable.
02-19 08:49:56.242  7733  7733 F DEBUG   :   NOTE: Unreadable libraries:
02-19 08:49:56.242  7733  7733 F DEBUG   :   NOTE:   /data/local/tmp/reproducer
02-19 08:49:56.242  7733  7733 F DEBUG   :       #00 pc 0000000002014d38  /vendor/lib64/egl/libGLES_mali.so (llvm::PatternMatch::undef_match::check(llvm::Value const*)+24) (BuildId: ae0dd7744c46583c)
02-19 08:49:56.242  7733  7733 F DEBUG   :       #01 pc 00000000028fa854  /vendor/lib64/egl/libGLES_mali.so (simplifyInstructionWithOperands(llvm::Instruction*, llvm::ArrayRef<llvm::Value*>, llvm::SimplifyQuery const&, llvm::OptimizationRemarkEmitter*) (.llvm.13836456976102157447)+692) (BuildId: ae0dd7744c46583c)
02-19 08:49:56.242  7733  7733 F DEBUG   :       #02 pc 00000000028fb188  /vendor/lib64/egl/libGLES_mali.so (llvm::SimplifyInstruction(llvm::Instruction*, llvm::SimplifyQuery const&, llvm::OptimizationRemarkEmitter*)+344) (BuildId: ae0dd7744c46583c)
02-19 08:49:56.242  7733  7733 F DEBUG   :       #03 pc 0000000002663bcc  /vendor/lib64/egl/libGLES_mali.so (llvm::GVNPass::runImpl(llvm::Function&, llvm::AssumptionCache&, llvm::DominatorTree&, llvm::TargetLibraryInfo const&, llvm::AAResults&, llvm::MemoryDependenceResults*, llvm::LoopInfo*, llvm::OptimizationRemarkEmitter*, llvm::MemorySSA*)+1820) (BuildId: ae0dd7744c46583c)
02-19 08:49:56.242  7733  7733 F DEBUG   :       #04 pc 000000000266ca74  /vendor/lib64/egl/libGLES_mali.so (llvm::gvn::GVNLegacyPass::runOnFunction(llvm::Function&)+580) (BuildId: ae0dd7744c46583c)
02-19 08:49:56.242  7733  7733 F DEBUG   :       #05 pc 00000000021cd050  /vendor/lib64/egl/libGLES_mali.so ((anonymous namespace)::MaliFunctionPassManager::runOnModule(llvm::Module&)+544) (BuildId: ae0dd7744c46583c)
02-19 08:49:56.242  7733  7733 F DEBUG   :       #06 pc 00000000021cc420  /vendor/lib64/egl/libGLES_mali.so ((anonymous namespace)::MaliModulePassManager::runOnModule(llvm::Module&)+400) (BuildId: ae0dd7744c46583c)
02-19 08:49:56.242  7733  7733 F DEBUG   :       #07 pc 00000000021c80ac  /vendor/lib64/egl/libGLES_mali.so (llvm::Mali::StaticPassManager::TLPassManagerImpl::run(llvm::Module&)+252) (BuildId: ae0dd7744c46583c)
02-19 08:49:56.242  7733  7733 F DEBUG   :       #08 pc 0000000001aed77c  /vendor/lib64/egl/libGLES_mali.so (cmpbep_bfr_run_llvm_backend+2044) (BuildId: ae0dd7744c46583c)
02-19 08:49:56.242  7733  7733 F DEBUG   :       #09 pc 0000000001af29d4  /vendor/lib64/egl/libGLES_mali.so (cmpbe_compile_gles_shader+660) (BuildId: ae0dd7744c46583c)
02-19 08:49:56.242  7733  7733 F DEBUG   :       #10 pc 0000000001b1769c  /vendor/lib64/egl/libGLES_mali.so (do_single_part2_compilation+188) (BuildId: ae0dd7744c46583c)
02-19 08:49:56.242  7733  7733 F DEBUG   :       #11 pc 0000000001b173d8  /vendor/lib64/egl/libGLES_mali.so (cmpbe_v2_compile_multiple_shaders+9944) (BuildId: ae0dd7744c46583c)
02-19 08:49:56.242  7733  7733 F DEBUG   :       #12 pc 0000000001a0cf4c  /vendor/lib64/egl/libGLES_mali.so (gfx::compiler::compile_shaders(gfx::shader_set const&, gfx::shader_set&, hal::shader_language, gfx::shader_state const&, compiler_cache*, gfx::mem_allocator&, cutils_cmpbe_dump_ctx**, bool*, unsigned long*)+6956) (BuildId: ae0dd7744c46583c)
02-19 08:49:56.242  7733  7733 F DEBUG   :       #13 pc 00000000009330e4  /vendor/lib64/egl/libGLES_mali.so (vkCreateGraphicsPipelines+12164) (BuildId: ae0dd7744c46583c)
02-19 08:49:56.242  7733  7733 F DEBUG   :       #14 pc 00000000000063dc  /data/local/tmp/reproducer
02-19 08:49:56.242  7733  7733 F DEBUG   :       #15 pc 000000000000690c  /data/local/tmp/reproducer
02-19 08:49:56.242  7733  7733 F DEBUG   :       #16 pc 0000000000057854  /apex/com.android.runtime/lib64/bionic/libc.so (__libc_init+116) (BuildId: d607b2dd86e0ffc603529ce13afab7fa)
02-19 08:49:56.242  7733  7733 F DEBUG   : deallocated by thread 7723:
02-19 08:49:56.242  7733  7733 F DEBUG   :       #00 pc 00000000000518b8  /apex/com.android.runtime/lib64/bionic/libc.so (scudo::Allocator<scudo::AndroidNormalConfig, &scudo_malloc_postinit>::quarantineOrDeallocateChunk(scudo::Options const&, void*, scudo::Chunk::UnpackedHeader*, unsigned long)+968) (BuildId: d607b2dd86e0ffc603529ce13afab7fa)
02-19 08:49:56.242  7733  7733 F DEBUG   :       #01 pc 000000000004b8f0  /apex/com.android.runtime/lib64/bionic/libc.so (scudo::Allocator<scudo::AndroidNormalConfig, &scudo_malloc_postinit>::deallocate(void*, scudo::Chunk::Origin, unsigned long, unsigned long)+192) (BuildId: d607b2dd86e0ffc603529ce13afab7fa)
02-19 08:49:56.242  7733  7733 F DEBUG   :       #02 pc 0000000002b13990  /vendor/lib64/egl/libGLES_mali.so (llvm::Instruction::eraseFromParent()+48) (BuildId: ae0dd7744c46583c)
02-19 08:49:56.242  7733  7733 F DEBUG   : allocated by thread 7723:
02-19 08:49:56.242  7733  7733 F DEBUG   :       #00 pc 000000000004b744  /apex/com.android.runtime/lib64/bionic/libc.so (scudo::Allocator<scudo::AndroidNormalConfig, &scudo_malloc_postinit>::allocate(unsigned long, scudo::Chunk::Origin, unsigned long, bool)+852) (BuildId: d607b2dd86e0ffc603529ce13afab7fa)
02-19 08:49:56.242  7733  7733 F DEBUG   :       #01 pc 000000000004bab4  /apex/com.android.runtime/lib64/bionic/libc.so (scudo_malloc+36) (BuildId: d607b2dd86e0ffc603529ce13afab7fa)
02-19 08:49:56.242  7733  7733 F DEBUG   :       #02 pc 00000000000456dc  /apex/com.android.runtime/lib64/bionic/libc.so (malloc+44) (BuildId: d607b2dd86e0ffc603529ce13afab7fa)
02-19 08:49:56.242  7733  7733 F DEBUG   :       #03 pc 00000000000eb97c  /vendor/lib64/libc++.so (operator new(unsigned long)+28) (BuildId: 94744eed32fba2eb636a9d2e5365a00614c1b4ae)
02-19 08:49:56.242  7733  7733 F DEBUG   :       #04 pc 0000000002b5a844  /vendor/lib64/egl/libGLES_mali.so (llvm::User::operator new(unsigned long, unsigned int)+20) (BuildId: ae0dd7744c46583c)
02-19 08:49:56.242  7733  7733 F DEBUG   : Learn more about MTE reports: https://source.android.com/docs/security/test/memory-safety/mte-reports

```

### jr...@google.com (2025-02-19)

Thanks, I've reached out to Arm PSIRT, we'll see what they say.

I tried the HTML reproducer today on a Pixel 9 but was still unable to reproduce the crash.

### ch...@google.com (2025-02-21)

We commit ourselves to a 30 day deadline for fixing for s0 severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

### jr...@google.com (2025-02-21)

Update from Arm today is that they are still working on a fix, and are not yet able to provide details of a potential workaround.

Can somebody from the security team add `SI-None` as we did with other issue, since we are waiting on external feedback?

### am...@chromium.org (2025-03-04)

This was labeled as an External Dependency, so I that should disable the nags, however it doesn't look like the blintz rule is configured that way.
I've updated as SI-None since Chromium won't be the one shipping the change provided by Arm.

### jr...@google.com (2025-04-09)

Update from Arm: the bug was fixed in upstream LLVM last June and they will be sending notifications out to partners soon. Given the nature of the bug they don't have a reliable pattern of SPIR-V that triggers the issue, and therefore it would be difficult for us to workaround this inside Tint.

Question for security folks: If we are unable to workaround the issue and are instead relying on the patched driver to reach user devices, is there anything else we need to do here?

### am...@chromium.org (2025-04-15)

Thank you for the update from Arm, James.
Ordinarily we would close this as fixed with the note that this was patched in the driver based on this report.
However, based on the feedback fro Arm, this appears to have been known and patched in upstream LLVM well before this report and it being reported to them in January.
Based on this and also given we are unable to pursue a workaround here, closing this as `infeasible` seems like the most accurate approach.

### sp...@google.com (2025-05-02)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $5000.00 for this report.

Rationale for this decision:
Since while this issue was known and patched upstream in LLVM before this report, it seems that it was only based on this report that ARM knew of this issue and was able to backport that change into Mali as a result of this report. 
Therefore, while we can't issue a full reward for this report, we wanted to show our appreciation for this this issue being reported to us and Arm ensuring full resolution.


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2025-07-23)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> Since while this issue was known and patched upstream in LLVM before this report, it seems that it was only based on this report that ARM knew of this issue and was able to backport that change into Mali as a result of this report. 
> Therefore, while we can't issue a full reward for this report, we wanted to show our appreciation for this this issue being reported to us and Arm ensuring full resolution.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/391284742)*
