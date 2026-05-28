# libGLES_mali UAF via WebGPU shaders at llvm::BasicBlock::getTerminator

| Field | Value |
|-------|-------|
| **Issue ID** | [442273697](https://issues.chromium.org/issues/442273697) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Dawn>Tint |
| **Platforms** | Android |
| **Reporter** | a7...@gmail.com |
| **Assignee** | pe...@google.com |
| **Created** | 2025-09-01 |
| **Bounty** | $25,000.00 |

## Description

#### VULNERABILITY DETAILS

Chrome on Android translates WebGPU shaders to SPIR-V. These SPIR-V shaders are eventually passed to libGLES\_mali.so for optimization and native code generation. This bug report is about a WebGPU shader that crashes the GPU process of com.android.chrome with an MTE violation. I will provide a copy of this report to ARM and keep you posted.

#### VERSION

Device: Pixel 8a   

Android build number: BP2A.250805.005   

Chromium: 139.0.7258.158

#### REPRODUCER

There are 2 ways to reproduce the issue, within Chrome and a standalone reproducer. In both cases you need to enable MTE on your device.

##### REPRODUCTION CASE (Chromium)

Enable MTE on the device and for Chrome (as described here: <https://googleprojectzero.blogspot.com/2023/11/first-handset-with-mte-on-market.html#h.48b4e8cq1xxw>). Then open the attached HTML, you should get the following message in your adb logs:

```
09-01 12:48:28.220 28459 28459 F DEBUG   : *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** ***
09-01 12:48:28.220 28459 28459 F DEBUG   : Build fingerprint: 'google/akita/akita:16/BP2A.250805.005/13691446:user/release-keys'
09-01 12:48:28.220 28459 28459 F DEBUG   : Revision: 'MP1.0'
09-01 12:48:28.220 28459 28459 F DEBUG   : ABI: 'arm64'
09-01 12:48:28.220 28459 28459 F DEBUG   : Timestamp: 2025-09-01 12:48:27.334395337+0200
09-01 12:48:28.220 28459 28459 F DEBUG   : Process uptime: 61s
09-01 12:48:28.220 28459 28459 F DEBUG   : Cmdline: com.android.chrome:privileged_process0
09-01 12:48:28.220 28459 28459 F DEBUG   : pid: 28124, tid: 28151, name: CrGpuMain  >>> com.android.chrome:privileged_process0 <<<
09-01 12:48:28.220 28459 28459 F DEBUG   : uid: 10176
09-01 12:48:28.220 28459 28459 F DEBUG   : tagged_addr_ctrl: 000000000007fff3 (PR_TAGGED_ADDR_ENABLE, PR_MTE_TCF_SYNC, mask 0xfffe)
09-01 12:48:28.220 28459 28459 F DEBUG   : pac_enabled_keys: 000000000000000f (PR_PAC_APIAKEY, PR_PAC_APIBKEY, PR_PAC_APDAKEY, PR_PAC_APDBKEY)
09-01 12:48:28.220 28459 28459 F DEBUG   : signal 11 (SIGSEGV), code 9 (SEGV_MTESERR), fault addr 0x0000007a4cd6cc78
09-01 12:48:28.220 28459 28459 F DEBUG   :     x0  0900007a4cd6cc50  x1  0000000000000001  x2  070000793cda42b0  x3  090000791cce72f8
09-01 12:48:28.220 28459 28459 F DEBUG   :     x4  0000000000000000  x5  00000078069456a0  x6  0000000000000001  x7  0000000000000000
09-01 12:48:28.220 28459 28459 F DEBUG   :     x8  04000079cd560de0  x9  04000079cd560de8  x10 0000000000000005  x11 04000079cd560dc0
09-01 12:48:28.220 28459 28459 F DEBUG   :     x12 0000000000000008  x13 0000000000000020  x14 0100007a4cd6d830  x15 03000079cd566d30
09-01 12:48:28.220 28459 28459 F DEBUG   :     x16 0000007857e27258  x17 0000007b5ab37e00  x18 00000078051fc000  x19 0000007806945278
09-01 12:48:28.220 28459 28459 F DEBUG   :     x20 04000079cd560d68  x21 0f0000798ccbbe00  x22 0000000000000002  x23 0000000000000002
09-01 12:48:28.220 28459 28459 F DEBUG   :     x24 0800007a4cd6d560  x25 0000007806949880  x26 0600007a4cd6d6f8  x27 0600007a4cd6d718
09-01 12:48:28.220 28459 28459 F DEBUG   :     x28 0000007806949880  x29 040000792cca6e50
09-01 12:48:28.220 28459 28459 F DEBUG   :     lr  000000785792a2f8  sp  00000078069450e0  pc  0000007857ab89e0  pst 0000000080001000
09-01 12:48:28.220 28459 28459 F DEBUG   : 50 total frames
09-01 12:48:28.220 28459 28459 F DEBUG   : backtrace:
09-01 12:48:28.221 28459 28459 F DEBUG   :       #00 pc 0000000002db79e0  /vendor/lib64/egl/libGLES_mali.so (llvm::BasicBlock::getTerminator() const+0) (BuildId: a046e33cd959c87438f7bf9d7cfeb10bf9809fa9)
09-01 12:48:28.221 28459 28459 F DEBUG   :       #01 pc 0000000002c292f4  /vendor/lib64/egl/libGLES_mali.so (void llvm::getUniqueExitBlocksHelper<llvm::BasicBlock, llvm::LoopBase<llvm::BasicBlock, llvm::Loop>, llvm::LoopBase<llvm::BasicBlock, llvm::Loop>::getUniqueExitBlocks(llvm::SmallVectorImpl<llvm::BasicBlock*>&) const::'lambda'(llvm::BasicBlock const*)>(llvm::LoopBase<llvm::BasicBlock, llvm::Loop> const*, llvm::SmallVectorImpl<llvm::BasicBlock*>&, llvm::LoopBase<llvm::BasicBlock, llvm::Loop>::getUniqueExitBlocks(llvm::SmallVectorImpl<llvm::BasicBlock*>&) const::'lambda'(llvm::BasicBlock const*))+148) (BuildId: a046e33cd959c87438f7bf9d7cfeb10bf9809fa9)
09-01 12:48:28.221 28459 28459 F DEBUG   :       #02 pc 0000000002c290fc  /vendor/lib64/egl/libGLES_mali.so (llvm::LoopBase<llvm::BasicBlock, llvm::Loop>::hasDedicatedExits() const+76) (BuildId: a046e33cd959c87438f7bf9d7cfeb10bf9809fa9)
09-01 12:48:28.221 28459 28459 F DEBUG   :       #03 pc 000000000298c1e0  /vendor/lib64/egl/libGLES_mali.so (deleteLoopIfDead(llvm::Loop*, llvm::DominatorTree&, llvm::ScalarEvolution&, llvm::LoopInfo&, llvm::MemorySSA*, llvm::OptimizationRemarkEmitter&)+80) (BuildId: a046e33cd959c87438f7bf9d7cfeb10bf9809fa9)
09-01 12:48:28.221 28459 28459 F DEBUG   :       #04 pc 000000000298e8c8  /vendor/lib64/egl/libGLES_mali.so ((anonymous namespace)::LoopDeletionLegacyPass::runOnLoop(llvm::Loop*, llvm::LPPassManager&)+328) (BuildId: a046e33cd959c87438f7bf9d7cfeb10bf9809fa9)
09-01 12:48:28.221 28459 28459 F DEBUG   :       #05 pc 00000000024c4e08  /vendor/lib64/egl/libGLES_mali.so ((anonymous namespace)::MaliLoopPassManager::runOnFunction(llvm::Function&)+968) (BuildId: a046e33cd959c87438f7bf9d7cfeb10bf9809fa9)
09-01 12:48:28.221 28459 28459 F DEBUG   :       #06 pc 00000000024c45e0  /vendor/lib64/egl/libGLES_mali.so ((anonymous namespace)::MaliFunctionPassManager::runOnModule(llvm::Module&)+544) (BuildId: a046e33cd959c87438f7bf9d7cfeb10bf9809fa9)
09-01 12:48:28.221 28459 28459 F DEBUG   :       #07 pc 00000000024c399c  /vendor/lib64/egl/libGLES_mali.so ((anonymous namespace)::MaliModulePassManager::runOnModule(llvm::Module&)+412) (BuildId: a046e33cd959c87438f7bf9d7cfeb10bf9809fa9)
09-01 12:48:28.221 28459 28459 F DEBUG   :       #08 pc 00000000024bf24c  /vendor/lib64/egl/libGLES_mali.so (llvm::Mali::StaticPassManager::TLPassManagerImpl::run(llvm::Module&)+268) (BuildId: a046e33cd959c87438f7bf9d7cfeb10bf9809fa9)
09-01 12:48:28.221 28459 28459 F DEBUG   :       #09 pc 0000000001dc7be8  /vendor/lib64/egl/libGLES_mali.so (cmpbep_bfr_run_llvm_backend+2056) (BuildId: a046e33cd959c87438f7bf9d7cfeb10bf9809fa9)
09-01 12:48:28.221 28459 28459 F DEBUG   :       #10 pc 0000000001dcc710  /vendor/lib64/egl/libGLES_mali.so (cmpbe_compile_gles_shader+640) (BuildId: a046e33cd959c87438f7bf9d7cfeb10bf9809fa9)
09-01 12:48:28.221 28459 28459 F DEBUG   :       #11 pc 0000000001defb98  /vendor/lib64/egl/libGLES_mali.so (do_single_part2_compilation+216) (BuildId: a046e33cd959c87438f7bf9d7cfeb10bf9809fa9)
09-01 12:48:28.221 28459 28459 F DEBUG   :       #12 pc 0000000001def5fc  /vendor/lib64/egl/libGLES_mali.so (cmpbe_v2_compile_multiple_shaders+9452) (BuildId: a046e33cd959c87438f7bf9d7cfeb10bf9809fa9)
09-01 12:48:28.221 28459 28459 F DEBUG   :       #13 pc 0000000001c2315c  /vendor/lib64/egl/libGLES_mali.so (gfx::compiler::compile_shaders(gfx::shader_set const&, gfx::shader_set&, gfx::shader_state const&, gfx::mem_allocator&, gfx::compilation_dynamic_args&, cutils_cmpbe_dump_ctx**, unsigned long*, compiler_cache*, char const*, gfx::pipeline_exec_info*)+1036) (BuildId: a046e33cd959c87438f7bf9d7cfeb10bf9809fa9)
09-01 12:48:28.221 28459 28459 F DEBUG   :       #14 pc 0000000001c253ec  /vendor/lib64/egl/libGLES_mali.so (gfx::compiler::compile_shaders_with_cache(gfx::shader_set const&, gfx::shader_set&, gfx::shader_state const&, compiler_cache*, gfx::mem_allocator&, cutils_cmpbe_dump_ctx**, bool*, unsigned long*, gfx::pipeline_exec_info*)+6316) (BuildId: a046e33cd959c87438f7bf9d7cfeb10bf9809fa9)
09-01 12:48:28.221 28459 28459 F DEBUG   :       #15 pc 0000000000989e30  /vendor/lib64/egl/libGLES_mali.so (vkCreateComputePipelines+2000) (BuildId: a046e33cd959c87438f7bf9d7cfeb10bf9809fa9)
09-01 12:48:28.221 28459 28459 F DEBUG   :       #16 pc 00000000027ecebc  /data/app/~~bX2XDeyfSvebNgUfSEsuzQ==/com.google.android.trichromelibrary_725815833-84epr_6-TgvCU3aYKFOR3A==/base.apk!libmonochrome_64.so (offset 0x8dc000) (BuildId: 1486a57a4ba7b56144721fcd544c8b14f165e53b)
09-01 12:48:28.221 28459 28459 F DEBUG   :       #17 pc 000000000700b918  /data/app/~~bX2XDeyfSvebNgUfSEsuzQ==/com.google.android.trichromelibrary_725815833-84epr_6-TgvCU3aYKFOR3A==/base.apk!libmonochrome_64.so (offset 0x8dc000) (BuildId: 1486a57a4ba7b56144721fcd544c8b14f165e53b)
09-01 12:48:28.221 28459 28459 F DEBUG   :       #18 pc 0000000002786c60  /data/app/~~bX2XDeyfSvebNgUfSEsuzQ==/com.google.android.trichromelibrary_725815833-84epr_6-TgvCU3aYKFOR3A==/base.apk!libmonochrome_64.so (offset 0x8dc000) (BuildId: 1486a57a4ba7b56144721fcd544c8b14f165e53b)
09-01 12:48:28.221 28459 28459 F DEBUG   :       #19 pc 0000000002786a48  /data/app/~~bX2XDeyfSvebNgUfSEsuzQ==/com.google.android.trichromelibrary_725815833-84epr_6-TgvCU3aYKFOR3A==/base.apk!libmonochrome_64.so (offset 0x8dc000) (BuildId: 1486a57a4ba7b56144721fcd544c8b14f165e53b)
09-01 12:48:28.221 28459 28459 F DEBUG   :       #20 pc 0000000008487a24  /data/app/~~bX2XDeyfSvebNgUfSEsuzQ==/com.google.android.trichromelibrary_725815833-84epr_6-TgvCU3aYKFOR3A==/base.apk!libmonochrome_64.so (offset 0x8dc000) (BuildId: 1486a57a4ba7b56144721fcd544c8b14f165e53b)
09-01 12:48:28.221 28459 28459 F DEBUG   :       #21 pc 000000000848d2cc  /data/app/~~bX2XDeyfSvebNgUfSEsuzQ==/com.google.android.trichromelibrary_725815833-84epr_6-TgvCU3aYKFOR3A==/base.apk!libmonochrome_64.so (offset 0x8dc000) (BuildId: 1486a57a4ba7b56144721fcd544c8b14f165e53b)
09-01 12:48:28.221 28459 28459 F DEBUG   :       #22 pc 0000000008556644  /data/app/~~bX2XDeyfSvebNgUfSEsuzQ==/com.google.android.trichromelibrary_725815833-84epr_6-TgvCU3aYKFOR3A==/base.apk!libmonochrome_64.so (offset 0x8dc000) (BuildId: 1486a57a4ba7b56144721fcd544c8b14f165e53b)
09-01 12:48:28.221 28459 28459 F DEBUG   :       #23 pc 0000000008556750  /data/app/~~bX2XDeyfSvebNgUfSEsuzQ==/com.google.android.trichromelibrary_725815833-84epr_6-TgvCU3aYKFOR3A==/base.apk!libmonochrome_64.so (offset 0x8dc000) (BuildId: 1486a57a4ba7b56144721fcd544c8b14f165e53b)
09-01 12:48:28.221 28459 28459 F DEBUG   :       #24 pc 00000000085541cc  /data/app/~~bX2XDeyfSvebNgUfSEsuzQ==/com.google.android.trichromelibrary_725815833-84epr_6-TgvCU3aYKFOR3A==/base.apk!libmonochrome_64.so (offset 0x8dc000) (BuildId: 1486a57a4ba7b56144721fcd544c8b14f165e53b)
09-01 12:48:28.221 28459 28459 F DEBUG   :       #25 pc 0000000006a77778  /data/app/~~bX2XDeyfSvebNgUfSEsuzQ==/com.google.android.trichromelibrary_725815833-84epr_6-TgvCU3aYKFOR3A==/base.apk!libmonochrome_64.so (offset 0x8dc000) (BuildId: 1486a57a4ba7b56144721fcd544c8b14f165e53b)
09-01 12:48:28.221 28459 28459 F DEBUG   :       #26 pc 0000000006a7694c  /data/app/~~bX2XDeyfSvebNgUfSEsuzQ==/com.google.android.trichromelibrary_725815833-84epr_6-TgvCU3aYKFOR3A==/base.apk!libmonochrome_64.so (offset 0x8dc000) (BuildId: 1486a57a4ba7b56144721fcd544c8b14f165e53b)
09-01 12:48:28.222 28459 28459 F DEBUG   :       #27 pc 0000000006a76630  /data/app/~~bX2XDeyfSvebNgUfSEsuzQ==/com.google.android.trichromelibrary_725815833-84epr_6-TgvCU3aYKFOR3A==/base.apk!libmonochrome_64.so (offset 0x8dc000) (BuildId: 1486a57a4ba7b56144721fcd544c8b14f165e53b)
09-01 12:48:28.222 28459 28459 F DEBUG   :       #28 pc 0000000006a76520  /data/app/~~bX2XDeyfSvebNgUfSEsuzQ==/com.google.android.trichromelibrary_725815833-84epr_6-TgvCU3aYKFOR3A==/base.apk!libmonochrome_64.so (offset 0x8dc000) (BuildId: 1486a57a4ba7b56144721fcd544c8b14f165e53b)
09-01 12:48:28.222 28459 28459 F DEBUG   :       #29 pc 0000000006a7646c  /data/app/~~bX2XDeyfSvebNgUfSEsuzQ==/com.google.android.trichromelibrary_725815833-84epr_6-TgvCU3aYKFOR3A==/base.apk!libmonochrome_64.so (offset 0x8dc000) (BuildId: 1486a57a4ba7b56144721fcd544c8b14f165e53b)
09-01 12:48:28.222 28459 28459 F DEBUG   :       #30 pc 0000000006aa9fbc  /data/app/~~bX2XDeyfSvebNgUfSEsuzQ==/com.google.android.trichromelibrary_725815833-84epr_6-TgvCU3aYKFOR3A==/base.apk!libmonochrome_64.so (offset 0x8dc000) (BuildId: 1486a57a4ba7b56144721fcd544c8b14f165e53b)
09-01 12:48:28.222 28459 28459 F DEBUG   :       #31 pc 0000000006db7e78  /data/app/~~bX2XDeyfSvebNgUfSEsuzQ==/com.google.android.trichromelibrary_725815833-84epr_6-TgvCU3aYKFOR3A==/base.apk!libmonochrome_64.so (offset 0x8dc000) (BuildId: 1486a57a4ba7b56144721fcd544c8b14f165e53b)
09-01 12:48:28.222 28459 28459 F DEBUG   :       #32 pc 000000000550a46c  /data/app/~~bX2XDeyfSvebNgUfSEsuzQ==/com.google.android.trichromelibrary_725815833-84epr_6-TgvCU3aYKFOR3A==/base.apk!libmonochrome_64.so (offset 0x8dc000) (BuildId: 1486a57a4ba7b56144721fcd544c8b14f165e53b)
09-01 12:48:28.222 28459 28459 F DEBUG   :       #33 pc 00000000054d6e14  /data/app/~~bX2XDeyfSvebNgUfSEsuzQ==/com.google.android.trichromelibrary_725815833-84epr_6-TgvCU3aYKFOR3A==/base.apk!libmonochrome_64.so (offset 0x8dc000) (BuildId: 1486a57a4ba7b56144721fcd544c8b14f165e53b)
09-01 12:48:28.222 28459 28459 F DEBUG   :       #34 pc 00000000054d6890  /data/app/~~bX2XDeyfSvebNgUfSEsuzQ==/com.google.android.trichromelibrary_725815833-84epr_6-TgvCU3aYKFOR3A==/base.apk!libmonochrome_64.so (offset 0x8dc000) (BuildId: 1486a57a4ba7b56144721fcd544c8b14f165e53b)
09-01 12:48:28.222 28459 28459 F DEBUG   :       #35 pc 0000000006d167e4  /data/app/~~bX2XDeyfSvebNgUfSEsuzQ==/com.google.android.trichromelibrary_725815833-84epr_6-TgvCU3aYKFOR3A==/base.apk!libmonochrome_64.so (offset 0x8dc000) (BuildId: 1486a57a4ba7b56144721fcd544c8b14f165e53b)
09-01 12:48:28.222 28459 28459 F DEBUG   :       #36 pc 000000000551a734  /data/app/~~bX2XDeyfSvebNgUfSEsuzQ==/com.google.android.trichromelibrary_725815833-84epr_6-TgvCU3aYKFOR3A==/base.apk!libmonochrome_64.so (offset 0x8dc000) (BuildId: 1486a57a4ba7b56144721fcd544c8b14f165e53b)
09-01 12:48:28.222 28459 28459 F DEBUG   :       #37 pc 0000000005491fc0  /data/app/~~bX2XDeyfSvebNgUfSEsuzQ==/com.google.android.trichromelibrary_725815833-84epr_6-TgvCU3aYKFOR3A==/base.apk!libmonochrome_64.so (offset 0x8dc000) (BuildId: 1486a57a4ba7b56144721fcd544c8b14f165e53b)
09-01 12:48:28.222 28459 28459 F DEBUG   :       #38 pc 00000000054c7a8c  /data/app/~~bX2XDeyfSvebNgUfSEsuzQ==/com.google.android.trichromelibrary_725815833-84epr_6-TgvCU3aYKFOR3A==/base.apk!libmonochrome_64.so (offset 0x8dc000) (BuildId: 1486a57a4ba7b56144721fcd544c8b14f165e53b)
09-01 12:48:28.222 28459 28459 F DEBUG   :       #39 pc 0000000005530720  /data/app/~~bX2XDeyfSvebNgUfSEsuzQ==/com.google.android.trichromelibrary_725815833-84epr_6-TgvCU3aYKFOR3A==/base.apk!libmonochrome_64.so (offset 0x8dc000) (Java_J_N_IZ+296) (BuildId: 1486a57a4ba7b56144721fcd544c8b14f165e53b)
09-01 12:48:28.222 28459 28459 F DEBUG   :       #40 pc 00000000002d7ae0  /system/framework/arm64/boot.oat (art_jni_trampoline+112) (BuildId: f7dcc0c41d7298598dd50b6df5fbdd67cef62829)
09-01 12:48:28.222 28459 28459 F DEBUG   :       #41 pc 0000000000689588  /apex/com.android.art/lib64/libart.so (nterp_helper+152) (BuildId: b229f9d1b6196afaae086f29f029f907)
09-01 12:48:28.222 28459 28459 F DEBUG   :       #42 pc 00000000000e2906  /data/app/~~ly-jBVXyV5D9c0Dl4AnlHw==/com.android.chrome-Tdsf-XuDj7ItyiSUQ6spHg==/base.apk (offset 0x145000) (If0.run+646)
09-01 12:48:28.222 28459 28459 F DEBUG   :       #43 pc 00000000000a94f0  /system/framework/arm64/boot.oat (java.lang.Thread.run+64) (BuildId: f7dcc0c41d7298598dd50b6df5fbdd67cef62829)
09-01 12:48:28.222 28459 28459 F DEBUG   :       #44 pc 0000000000328194  /apex/com.android.art/lib64/libart.so (art_quick_invoke_stub+612) (BuildId: b229f9d1b6196afaae086f29f029f907)
09-01 12:48:28.222 28459 28459 F DEBUG   :       #45 pc 00000000002d9348  /apex/com.android.art/lib64/libart.so (art::ArtMethod::Invoke(art::Thread*, unsigned int*, unsigned int, art::JValue*, char const*)+216) (BuildId: b229f9d1b6196afaae086f29f029f907)
09-01 12:48:28.222 28459 28459 F DEBUG   :       #46 pc 0000000000421028  /apex/com.android.art/lib64/libart.so (art::Thread::CreateCallback(void*)+932) (BuildId: b229f9d1b6196afaae086f29f029f907)
09-01 12:48:28.222 28459 28459 F DEBUG   :       #47 pc 0000000000420c74  /apex/com.android.art/lib64/libart.so (art::Thread::CreateCallbackWithUffdGc(void*)+8) (BuildId: b229f9d1b6196afaae086f29f029f907)
09-01 12:48:28.222 28459 28459 F DEBUG   :       #48 pc 0000000000083c9c  /apex/com.android.runtime/lib64/bionic/libc.so (__pthread_start(void*)+236) (BuildId: ee75586813c8ea694071e432799eab05)
09-01 12:48:28.222 28459 28459 F DEBUG   :       #49 pc 00000000000761a0  /apex/com.android.runtime/lib64/bionic/libc.so (__start_thread+64) (BuildId: ee75586813c8ea694071e432799eab05)
09-01 12:48:28.223 28459 28459 F DEBUG   : Learn more about MTE reports: https://source.android.com/docs/security/test/memory-safety/mte-reports

```
##### REPRODUCTION CASE (Standalone)

- Compile the attached standalone.cpp via: `~/android-ndk-r27/toolchains/llvm/prebuilt/linux-x86_64/bin/x86_64-linux-android35-clang++ --target=aarch64-linux-android35 -lvulkan standalone.cpp -o reproducer`
- Push the resulting binary and comp.spv onto the device.
- Enable MTE sync for the reproducer: `adb shell setprop arm64.memtag.process.reproducer sync`
- Run the reproducer via `./reproducer comp.spv`

## Attachments

- [standalone.cpp](attachments/standalone.cpp) (text/x-c++src, 7.9 KB)
- [comp.spv](attachments/comp.spv) (application/octet-stream, 3.9 KB)
- [a.html](attachments/a.html) (text/html, 4.2 KB)

## Timeline

### a7...@gmail.com (2025-09-02)

Upstream issue is ARMSEC-379

### el...@chromium.org (2025-09-02)

Thank you for reporting this upstream!

There may still be steps we can take on the Chromium side to mitigate this vulnerability even though the real fix should happen in Mali. I am going to kick this into the Dawn component for some assessment of whether we can mitigate it ourselves. I have not tried to repro this myself since I don't have an appropriate Android test device.

### el...@chromium.org (2025-09-02)

Setting FoundIn to 139 to match the report, but if this is a Mali bug it's probably FoundIn everything.

### pe...@google.com (2025-09-02)

Could not reproduce on pixel 6

### pe...@google.com (2025-09-03)

Was able to reproduce on pixel 8a using Amber test script

### ch...@google.com (2025-09-03)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2025-09-10)

Internal pixel team bug <https://buganizer.corp.google.com/issues/442621902>

### ch...@google.com (2025-09-25)

petermcneeley: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### a7...@gmail.com (2025-09-25)

The issue has been confirmed by upstream, the vendor should reach out to you.

### ch...@google.com (2025-10-10)

petermcneeley: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### pe...@google.com (2025-10-10)

Linked bug on the pixel side
<https://buganizer.corp.google.com/issues/442621902#comment8>
"Pending patch"

### ch...@google.com (2025-10-25)

petermcneeley: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-11-01)

We commit ourselves to a 60 day deadline for fixing for s1 severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

### ch...@google.com (2025-11-11)

petermcneeley: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### dn...@google.com (2025-11-11)

Latest status on the Pixel side is still from Oct2, pending patch.

### ch...@google.com (2025-11-26)

petermcneeley: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### pe...@google.com (2025-11-26)

[Comment #12](https://issues.chromium.org/issues/442273697#comment12) pixel side is pending patch. At this stage there is no action for webgpu.

### pe...@google.com (2025-12-12)

The NextAction date has arrived: 2025-12-12
To opt-out from this automation rule, please add Optout-Blintz-Nextaction-Alert to the "Chromium Labels" custom field.

### pe...@google.com (2025-12-16)

Patch will roll out to all affected devices. Nothing left to do on our end.

### ch...@google.com (2025-12-16)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### aj...@google.com (2025-12-16)

Fixed in the driver so no Chrome changes.

### aj...@google.com (2025-12-16)

reporter: did ARM issue a CVE for this?

### ch...@google.com (2025-12-31)

petermcneeley: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2026-01-09)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to extended stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M142. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M143. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M144. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [142, 143, 144].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### dr...@chromium.org (2026-01-09)

No Chrome changes means nothing to merge.

### sp...@google.com (2026-01-26)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $25000.00 for this report.

Rationale for this decision:
Baseline Memory corruption in a non-sandboxed process (GPU on Android)


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-04-17)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/442273697)*
