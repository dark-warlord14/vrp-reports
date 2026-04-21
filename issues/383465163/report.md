# Android Chrome: Heap overflow in GLES2DecoderPassthroughImpl::DoEndQueryEXT

| Field | Value |
|-------|-------|
| **Issue ID** | [383465163](https://issues.chromium.org/issues/383465163) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU |
| **Platforms** | Android |
| **Chrome Version** | 133.0.6887 (64bit SAMSUNG S-24) |
| **Reporter** | po...@gmail.com |
| **Assignee** | ge...@google.com |
| **Created** | 2024-12-11 |
| **Bounty** | $10,000.00 |

## Description

# Steps to reproduce the problem

1. Run Android Chrome
2. Open oob.html
3. check crash log using "adb logcat -b crash"

# Problem Description

In "gpu/command\_buffer/service/gles2\_cmd\_decoder\_passthrough\_doers.cc" `GLES2DecoderPassthroughImpl::DoEndQueryEXT` will try to erase an "active\_queries\_" without checking if the iterator was actually found or not by the "find" call [1]. This is will likely result in the flat\_map trying to call erase // [2] using something on heap chunk after it's end.

We don't actually check with Release Build because we check with DCHECK.

It's similar bug cases:

- <https://issues.chromium.org/issues/41482168>
- <https://issues.chromium.org/issues/40052594>

```
error::Error GLES2DecoderPassthroughImpl::DoEndQueryEXT(GLenum target,
                                                        uint32_t submit_count) {
  if (IsEmulatedQueryTarget(target)) {
    auto active_query_iter = active_queries_.find(target);
    if (active_query_iter == active_queries_.end()) {
      InsertError(GL_INVALID_OPERATION, "No active query on target.");
      return error::kNoError;
    }
    if (target == GL_ASYNC_PIXEL_PACK_COMPLETED_CHROMIUM &&
        !pending_read_pixels_.empty()) {
      GLuint query_service_id = active_query_iter->second.service_id;
      pending_read_pixels_.back().waiting_async_pack_queries.insert(
          query_service_id);
    }
  } else {
    // glEndQuery is not loaded unless GL_EXT_occlusion_query_boolean is present
    if (!feature_info_->feature_flags().occlusion_query_boolean) {
      InsertError(GL_INVALID_ENUM, "Invalid query target.");
      return error::kNoError;
    }

    // Flush all previous errors
    CheckErrorCallbackState();

    api()->glEndQueryFn(target);

    // Check if a new error was generated
    if (CheckErrorCallbackState()) {
      return error::kNoError;
    }
  }

  DCHECK(active_queries_.find(target) != active_queries_.end()); // [1]
  ActiveQuery active_query = std::move(active_queries_[target]);
  active_queries_.erase(target); // [2]

```
# Summary

Android Chrome: Heap overflow in GLES2DecoderPassthroughImpl::DoEndQueryEXT

# Custom Questions

#### Type of crash:

GPU process

#### Crash state:

```
12-11 18:40:48.203 19187 19220 F libc    : Fatal signal 6 (SIGABRT), code -1 (SI_QUEUE) in tid 19220 (CrGpuMain), pid 19187 (ileged_process1)
12-11 18:40:48.793 19360 19360 F DEBUG   : *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** ***
12-11 18:40:48.793 19360 19360 F DEBUG   : Build fingerprint: 'samsung/e1sksx/e1s:14/UP1A.231005.007/S921NKSU5AXK4:user/release-keys'
12-11 18:40:48.793 19360 19360 F DEBUG   : Revision: '17'
12-11 18:40:48.793 19360 19360 F DEBUG   : ABI: 'arm64'
12-11 18:40:48.793 19360 19360 F DEBUG   : Processor: '5'
12-11 18:40:48.793 19360 19360 F DEBUG   : Timestamp: 2024-12-11 18:40:48.375778788+0900
12-11 18:40:48.793 19360 19360 F DEBUG   : Process uptime: 19s
12-11 18:40:48.793 19360 19360 F DEBUG   : Cmdline: org.chromium.chrome:privileged_process1
12-11 18:40:48.793 19360 19360 F DEBUG   : pid: 19187, tid: 19220, name: CrGpuMain  >>> org.chromium.chrome:privileged_process1 <<<
12-11 18:40:48.793 19360 19360 F DEBUG   : uid: 10346
12-11 18:40:48.793 19360 19360 F DEBUG   : tagged_addr_ctrl: 0000000000000001 (PR_TAGGED_ADDR_ENABLE)
12-11 18:40:48.793 19360 19360 F DEBUG   : pac_enabled_keys: 000000000000000f (PR_PAC_APIAKEY, PR_PAC_APIBKEY, PR_PAC_APDAKEY, PR_PAC_APDBKEY)
12-11 18:40:48.793 19360 19360 F DEBUG   : signal 6 (SIGABRT), code -1 (SI_QUEUE), fault addr --------
12-11 18:40:48.793 19360 19360 F DEBUG   : Abort message: '[FATAL:gles2_cmd_decoder_passthrough_doers.cc(4014)] Check failed: active_queries_.find(target) != active_queries_.end(). '
12-11 18:40:48.793 19360 19360 F DEBUG   :     x0  0000000000000000  x1  0000000000004b14  x2  0000000000000006  x3  00000072e6b5cfb0
12-11 18:40:48.793 19360 19360 F DEBUG   :     x4  0000000000000008  x5  0000000000000008  x6  0000000000000008  x7  00000072e6b5cc63
12-11 18:40:48.793 19360 19360 F DEBUG   :     x8  00000000000000f0  x9  000000768fa621e8  x10 0000000000000001  x11 000000768fab5348
12-11 18:40:48.793 19360 19360 F DEBUG   :     x12 00000000000044aa  x13 0000000000004b8a  x14 0000000000000000  x15 000002952dfb2333
12-11 18:40:48.793 19360 19360 F DEBUG   :     x16 000000768fb22d08  x17 000000768faf7210  x18 00000072e5fa6000  x19 0000000000004af3
12-11 18:40:48.793 19360 19360 F DEBUG   :     x20 0000000000004b14  x21 00000000ffffffff  x22 00000072d2761c9b  x23 00000072d2def000
12-11 18:40:48.793 19360 19360 F DEBUG   :     x24 00000072e6b61000  x25 b4000075d9997988  x26 0000000000000018  x27 0000000000000005
12-11 18:40:48.793 19360 19360 F DEBUG   :     x28 0000000000000003  x29 00000072e6b5d030
12-11 18:40:48.793 19360 19360 F DEBUG   :     lr  000000768faa6b4c  sp  00000072e6b5cf90  pc  000000768faa6b78  pst 0000000000001000
12-11 18:40:48.793 19360 19360 F DEBUG   : 73 total frames
12-11 18:40:48.793 19360 19360 F DEBUG   : backtrace:
12-11 18:40:48.793 19360 19360 F DEBUG   :       #00 pc 0000000000066b78  /apex/com.android.runtime/lib64/bionic/libc.so (abort+164) (BuildId: 6fbd0d7c6e3abc50de22e2fa6d2d6513)
12-11 18:40:48.793 19360 19360 F DEBUG   :       #01 pc 00000000003280c8  /data/app/~~l-OxVV4YDTj6ZSe3W8_iAQ==/org.chromium.chrome-I_qSoW9qSe-upz3rkj29ng==/lib/arm64/libbase.cr.so (logging::LogMessage::HandleFatal(unsigned long, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> > const&) const+348) (BuildId: 036583c94eef5ae6)
12-11 18:40:48.793 19360 19360 F DEBUG   :       #02 pc 0000000000327b9c  /data/app/~~l-OxVV4YDTj6ZSe3W8_iAQ==/org.chromium.chrome-I_qSoW9qSe-upz3rkj29ng==/lib/arm64/libbase.cr.so (logging::LogMessage::Flush()+1052) (BuildId: 036583c94eef5ae6)
12-11 18:40:48.793 19360 19360 F DEBUG   :       #03 pc 0000000000327768  /data/app/~~l-OxVV4YDTj6ZSe3W8_iAQ==/org.chromium.chrome-I_qSoW9qSe-upz3rkj29ng==/lib/arm64/libbase.cr.so (logging::LogMessage::~LogMessage()+36) (BuildId: 036583c94eef5ae6)
12-11 18:40:48.793 19360 19360 F DEBUG   :       #04 pc 000000000030659c  /data/app/~~l-OxVV4YDTj6ZSe3W8_iAQ==/org.chromium.chrome-I_qSoW9qSe-upz3rkj29ng==/lib/arm64/libbase.cr.so (BuildId: 036583c94eef5ae6)
12-11 18:40:48.793 19360 19360 F DEBUG   :       #05 pc 0000000000305e3c  /data/app/~~l-OxVV4YDTj6ZSe3W8_iAQ==/org.chromium.chrome-I_qSoW9qSe-upz3rkj29ng==/lib/arm64/libbase.cr.so (logging::NotReachedError::~NotReachedError()+44) (BuildId: 036583c94eef5ae6)
12-11 18:40:48.793 19360 19360 F DEBUG   :       #06 pc 000000000039154c  /data/app/~~l-OxVV4YDTj6ZSe3W8_iAQ==/org.chromium.chrome-I_qSoW9qSe-upz3rkj29ng==/lib/arm64/libgpu_gles2.cr.so (gpu::gles2::GLES2DecoderPassthroughImpl::DoEndQueryEXT(unsigned int, unsigned int)+872) (BuildId: c6be1f52650ddbc9)
12-11 18:40:48.793 19360 19360 F DEBUG   :       #07 pc 0000000000378d40  /data/app/~~l-OxVV4YDTj6ZSe3W8_iAQ==/org.chromium.chrome-I_qSoW9qSe-upz3rkj29ng==/lib/arm64/libgpu_gles2.cr.so (gpu::error::Error gpu::gles2::GLES2DecoderPassthroughImpl::DoCommandsImpl<false>(unsigned int, void const volatile*, int, int*)+260) (BuildId: c6be1f52650ddbc9)
12-11 18:40:48.793 19360 19360 F DEBUG   :       #08 pc 00000000001763f4  /data/app/~~l-OxVV4YDTj6ZSe3W8_iAQ==/org.chromium.chrome-I_qSoW9qSe-upz3rkj29ng==/lib/arm64/libgpu.cr.so (gpu::CommandBufferService::Flush(int, gpu::AsyncAPIInterface*)+596) (BuildId: 28876a756dfa20d9)
12-11 18:40:48.793 19360 19360 F DEBUG   :       #09 pc 0000000000052ba8  /data/app/~~l-OxVV4YDTj6ZSe3W8_iAQ==/org.chromium.chrome-I_qSoW9qSe-upz3rkj29ng==/lib/arm64/libgpu_ipc_service.cr.so (gpu::CommandBufferStub::OnAsyncFlush(int, unsigned int, std::__Cr::vector<gpu::SyncToken, std::__Cr::allocator<gpu::SyncToken> > const&)+332) (BuildId: 352f7a3e3f647b44)
12-11 18:40:48.793 19360 19360 F DEBUG   :       #10 pc 00000000000527f4  /data/app/~~l-OxVV4YDTj6ZSe3W8_iAQ==/org.chromium.chrome-I_qSoW9qSe-upz3rkj29ng==/lib/arm64/libgpu_ipc_service.cr.so (gpu::CommandBufferStub::ExecuteDeferredRequest(gpu::mojom::DeferredCommandBufferRequestParams&, gpu::FenceSyncReleaseDelegate*)+180) (BuildId: 352f7a3e3f647b44)
12-11 18:40:48.793 19360 19360 F DEBUG   :       #11 pc 000000000005ea10  /data/app/~~l-OxVV4YDTj6ZSe3W8_iAQ==/org.chromium.chrome-I_qSoW9qSe-upz3rkj29ng==/lib/arm64/libgpu_ipc_service.cr.so (gpu::GpuChannel::ExecuteDeferredRequest(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*)+252) (BuildId: 352f7a3e3f647b44)
12-11 18:40:48.793 19360 19360 F DEBUG   :       #12 pc 0000000000062ae0  /data/app/~~l-OxVV4YDTj6ZSe3W8_iAQ==/org.chromium.chrome-I_qSoW9qSe-upz3rkj29ng==/lib/arm64/libgpu_ipc_service.cr.so (BuildId: 352f7a3e3f647b44)
12-11 18:40:48.793 19360 19360 F DEBUG   :       #13 pc 0000000000062988  /data/app/~~l-OxVV4YDTj6ZSe3W8_iAQ==/org.chromium.chrome-I_qSoW9qSe-upz3rkj29ng==/lib/arm64/libgpu_ipc_service.cr.so (BuildId: 352f7a3e3f647b44)
12-11 18:40:48.793 19360 19360 F DEBUG   :       #14 pc 000000000018c7b8  /data/app/~~l-OxVV4YDTj6ZSe3W8_iAQ==/org.chromium.chrome-I_qSoW9qSe-upz3rkj29ng==/lib/arm64/libgpu.cr.so (BuildId: 28876a756dfa20d9)
12-11 18:40:48.793 19360 19360 F DEBUG   :       #15 pc 000000000018c754  /data/app/~~l-OxVV4YDTj6ZSe3W8_iAQ==/org.chromium.chrome-I_qSoW9qSe-upz3rkj29ng==/lib/arm64/libgpu.cr.so (BuildId: 28876a756dfa20d9)
12-11 18:40:48.793 19360 19360 F DEBUG   :       #16 pc 000000000018c6dc  /data/app/~~l-OxVV4YDTj6ZSe3W8_iAQ==/org.chromium.chrome-I_qSoW9qSe-upz3rkj29ng==/lib/arm64/libgpu.cr.so (BuildId: 28876a756dfa20d9)
12-11 18:40:48.793 19360 19360 F DEBUG   :       #17 pc 0000000000175248  /data/app/~~l-OxVV4YDTj6ZSe3W8_iAQ==/org.chromium.chrome-I_qSoW9qSe-upz3rkj29ng==/lib/arm64/libgpu.cr.so (BuildId: 28876a756dfa20d9)
12-11 18:40:48.793 19360 19360 F DEBUG   :       #18 pc 000000000017d8e8  /data/app/~~l-OxVV4YDTj6ZSe3W8_iAQ==/org.chromium.chrome-I_qSoW9qSe-upz3rkj29ng==/lib/arm64/libgpu.cr.so (gpu::Scheduler::ExecuteSequence(base::IdType<gpu::SyncPointOrderData, unsigned int, 0u, 1u>)+936) (BuildId: 28876a756dfa20d9)
12-11 18:40:48.793 19360 19360 F DEBUG   :       #19 pc 000000000017ce88  /data/app/~~l-OxVV4YDTj6ZSe3W8_iAQ==/org.chromium.chrome-I_qSoW9qSe-upz3rkj29ng==/lib/arm64/libgpu.cr.so (gpu::Scheduler::RunNextTask()+480) (BuildId: 28876a756dfa20d9)
12-11 18:40:48.793 19360 19360 F DEBUG   :       #20 pc 0000000000301e24  /data/app/~~l-OxVV4YDTj6ZSe3W8_iAQ==/org.chromium.chrome-I_qSoW9qSe-upz3rkj29ng==/lib/arm64/libbase.cr.so (BuildId: 036583c94eef5ae6)
12-11 18:40:48.793 19360 19360 F DEBUG   :       #21 pc 00000000003b2250  /data/app/~~l-OxVV4YDTj6ZSe3W8_iAQ==/org.chromium.chrome-I_qSoW9qSe-upz3rkj29ng==/lib/arm64/libbase.cr.so (base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+232) (BuildId: 036583c94eef5ae6)
12-11 18:40:48.793 19360 19360 F DEBUG   :       #22 pc 00000000003dbf08  /data/app/~~l-OxVV4YDTj6ZSe3W8_iAQ==/org.chromium.chrome-I_qSoW9qSe-upz3rkj29ng==/lib/arm64/libbase.cr.so (base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)+876) (BuildId: 036583c94eef5ae6)
12-11 18:40:48.793 19360 19360 F DEBUG   :       #23 pc 00000000003dba24  /data/app/~~l-OxVV4YDTj6ZSe3W8_iAQ==/org.chromium.chrome-I_qSoW9qSe-upz3rkj29ng==/lib/arm64/libbase.cr.so (base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+100) (BuildId: 036583c94eef5ae6)
12-11 18:40:48.793 19360 19360 F DEBUG   :       #24 pc 0000000000336898  /data/app/~~l-OxVV4YDTj6ZSe3W8_iAQ==/org.chromium.chrome-I_qSoW9qSe-upz3rkj29ng==/lib/arm64/libbase.cr.so (base::MessagePumpDefault::Run(base::MessagePump::Delegate*)+96) (BuildId: 036583c94eef5ae6)
12-11 18:40:48.793 19360 19360 F DEBUG   :       #25 pc 00000000003dc51c  /data/app/~~l-OxVV4YDTj6ZSe3W8_iAQ==/org.chromium.chrome-I_qSoW9qSe-upz3rkj29ng==/lib/arm64/libbase.cr.so (base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta)+304) (BuildId: 036583c94eef5ae6)
12-11 18:40:48.793 19360 19360 F DEBUG   :       #26 pc 000000000037ede0  /data/app/~~l-OxVV4YDTj6ZSe3W8_iAQ==/org.chromium.chrome-I_qSoW9qSe-upz3rkj29ng==/lib/arm64/libbase.cr.so (base::RunLoop::Run(base::Location const&)+396) (BuildId: 036583c94eef5ae6)
12-11 18:40:48.793 19360 19360 F DEBUG   :       #27 pc 0000000002235628  /data/app/~~l-OxVV4YDTj6ZSe3W8_iAQ==/org.chromium.chrome-I_qSoW9qSe-upz3rkj29ng==/lib/arm64/libcontent.cr.so (BuildId: 6e145fa2d6f3986d)
12-11 18:40:48.793 19360 19360 F DEBUG   :       #28 pc 00000000043e48e0  /data/app/~~l-OxVV4YDTj6ZSe3W8_iAQ==/org.chromium.chrome-I_qSoW9qSe-upz3rkj29ng==/lib/arm64/libcontent.cr.so (BuildId: 6e145fa2d6f3986d)
12-11 18:40:48.793 19360 19360 F DEBUG   :       #29 pc 00000000043e5600  /data/app/~~l-OxVV4YDTj6ZSe3W8_iAQ==/org.chromium.chrome-I_qSoW9qSe-upz3rkj29ng==/lib/arm64/libcontent.cr.so (BuildId: 6e145fa2d6f3986d)
12-11 18:40:48.793 19360 19360 F DEBUG   :       #30 pc 00000000043e2cfc  /data/app/~~l-OxVV4YDTj6ZSe3W8_iAQ==/org.chromium.chrome-I_qSoW9qSe-upz3rkj29ng==/lib/arm64/libcontent.cr.so (content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*)+268) (BuildId: 6e145fa2d6f3986d)
12-11 18:40:48.793 19360 19360 F DEBUG   :       #31 pc 00000000043e3e58  /data/app/~~l-OxVV4YDTj6ZSe3W8_iAQ==/org.chromium.chrome-I_qSoW9qSe-upz3rkj29ng==/lib/arm64/libcontent.cr.so (Java_org_jni_1zero_GEN_1JNI_org_1chromium_1content_1app_1ContentMain_1start+136) (BuildId: 6e145fa2d6f3986d)
12-11 18:40:48.793 19360 19360 F DEBUG   :       #32 pc 0000000000384370  /apex/com.android.art/lib64/libart.so (art_quick_generic_jni_trampoline+144) (BuildId: 3f7d5a016e08d528f129bdd336d81168)
12-11 18:40:48.793 19360 19360 F DEBUG   :       #33 pc 000000000036de40  /apex/com.android.art/lib64/libart.so (art_quick_invoke_static_stub+640) (BuildId: 3f7d5a016e08d528f129bdd336d81168)
12-11 18:40:48.793 19360 19360 F DEBUG   :       #34 pc 000000000036725c  /apex/com.android.art/lib64/libart.so (bool art::interpreter::DoCall<false>(art::ArtMethod*, art::Thread*, art::ShadowFrame&, art::Instruction const*, unsigned short, bool, art::JValue*)+2048) (BuildId: 3f7d5a016e08d528f129bdd336d81168)
12-11 18:40:48.793 19360 19360 F DEBUG   :       #35 pc 000000000076e170  /apex/com.android.art/lib64/libart.so (void art::interpreter::ExecuteSwitchImplCpp<false>(art::interpreter::SwitchImplContext*)+12208) (BuildId: 3f7d5a016e08d528f129bdd336d81168)
12-11 18:40:48.793 19360 19360 F DEBUG   :       #36 pc 00000000003869d8  /apex/com.android.art/lib64/libart.so (ExecuteSwitchImplAsm+8) (BuildId: 3f7d5a016e08d528f129bdd336d81168)
12-11 18:40:48.793 19360 19360 F DEBUG   :       #37 pc 0000000002ecbd68  /data/app/~~l-OxVV4YDTj6ZSe3W8_iAQ==/org.chromium.chrome-I_qSoW9qSe-upz3rkj29ng==/oat/arm64/base.vdex (org.chromium.content.app.ContentMainJni.start+0)
12-11 18:40:48.793 19360 19360 F DEBUG   :       #38 pc 0000000000359650  /apex/com.android.art/lib64/libart.so (art::interpreter::Execute(art::Thread*, art::CodeItemDataAccessor const&, art::ShadowFrame&, art::JValue, bool, bool) (.__uniq.112435418011751916792819755956732575238.llvm.4560577758463694485)+428) (BuildId: 3f7d5a016e08d528f129bdd336d81168)
12-11 18:40:48.794 19360 19360 F DEBUG   :       #39 pc 0000000000367a78  /apex/com.android.art/lib64/libart.so (bool art::interpreter::DoCall<false>(art::ArtMethod*, art::Thread*, art::ShadowFrame&, art::Instruction const*, unsigned short, bool, art::JValue*)+4124) (BuildId: 3f7d5a016e08d528f129bdd336d81168)
12-11 18:40:48.794 19360 19360 F DEBUG   :       #40 pc 000000000076e170  /apex/com.android.art/lib64/libart.so (void art::interpreter::ExecuteSwitchImplCpp<false>(art::interpreter::SwitchImplContext*)+12208) (BuildId: 3f7d5a016e08d528f129bdd336d81168)
12-11 18:40:48.794 19360 19360 F DEBUG   :       #41 pc 00000000003869d8  /apex/com.android.art/lib64/libart.so (ExecuteSwitchImplAsm+8) (BuildId: 3f7d5a016e08d528f129bdd336d81168)
12-11 18:40:48.794 19360 19360 F DEBUG   :       #42 pc 0000000002ecbe20  /data/app/~~l-OxVV4YDTj6ZSe3W8_iAQ==/org.chromium.chrome-I_qSoW9qSe-upz3rkj29ng==/oat/arm64/base.vdex (org.chromium.content.app.ContentMain.start+0)
12-11 18:40:48.794 19360 19360 F DEBUG   :       #43 pc 0000000000359650  /apex/com.android.art/lib64/libart.so (art::interpreter::Execute(art::Thread*, art::CodeItemDataAccessor const&, art::ShadowFrame&, art::JValue, bool, bool) (.__uniq.112435418011751916792819755956732575238.llvm.4560577758463694485)+428) (BuildId: 3f7d5a016e08d528f129bdd336d81168)
12-11 18:40:48.794 19360 19360 F DEBUG   :       #44 pc 0000000000367a78  /apex/com.android.art/lib64/libart.so (bool art::interpreter::DoCall<false>(art::ArtMethod*, art::Thread*, art::ShadowFrame&, art::Instruction const*, unsigned short, bool, art::JValue*)+4124) (BuildId: 3f7d5a016e08d528f129bdd336d81168)
12-11 18:40:48.794 19360 19360 F DEBUG   :       #45 pc 000000000076e170  /apex/com.android.art/lib64/libart.so (void art::interpreter::ExecuteSwitchImplCpp<false>(art::interpreter::SwitchImplContext*)+12208) (BuildId: 3f7d5a016e08d528f129bdd336d81168)
12-11 18:40:48.794 19360 19360 F DEBUG   :       #46 pc 00000000003869d8  /apex/com.android.art/lib64/libart.so (ExecuteSwitchImplAsm+8) (BuildId: 3f7d5a016e08d528f129bdd336d81168)
12-11 18:40:48.794 19360 19360 F DEBUG   :       #47 pc 0000000002ecbc44  /data/app/~~l-OxVV4YDTj6ZSe3W8_iAQ==/org.chromium.chrome-I_qSoW9qSe-upz3rkj29ng==/oat/arm64/base.vdex (org.chromium.content.app.ContentChildProcessServiceDelegate.runMain+0)
12-11 18:40:48.794 19360 19360 F DEBUG   :       #48 pc 0000000000359650  /apex/com.android.art/lib64/libart.so (art::interpreter::Execute(art::Thread*, art::CodeItemDataAccessor const&, art::ShadowFrame&, art::JValue, bool, bool) (.__uniq.112435418011751916792819755956732575238.llvm.4560577758463694485)+428) (BuildId: 3f7d5a016e08d528f129bdd336d81168)
12-11 18:40:48.794 19360 19360 F DEBUG   :       #49 pc 0000000000367a78  /apex/com.android.art/lib64/libart.so (bool art::interpreter::DoCall<false>(art::ArtMethod*, art::Thread*, art::ShadowFrame&, art::Instruction const*, unsigned short, bool, art::JValue*)+4124) (BuildId: 3f7d5a016e08d528f129bdd336d81168)
12-11 18:40:48.794 19360 19360 F DEBUG   :       #50 pc 000000000076e170  /apex/com.android.art/lib64/libart.so (void art::interpreter::ExecuteSwitchImplCpp<false>(art::interpreter::SwitchImplContext*)+12208) (BuildId: 3f7d5a016e08d528f129bdd336d81168)
12-11 18:40:48.794 19360 19360 F DEBUG   :       #51 pc 00000000003869d8  /apex/com.android.art/lib64/libart.so (ExecuteSwitchImplAsm+8) (BuildId: 3f7d5a016e08d528f129bdd336d81168)
12-11 18:40:48.794 19360 19360 F DEBUG   :       #52 pc 00000000015d49ac  /data/app/~~l-OxVV4YDTj6ZSe3W8_iAQ==/org.chromium.chrome-I_qSoW9qSe-upz3rkj29ng==/oat/arm64/base.vdex (org.chromium.base.process_launcher.ChildProcessService.mainThreadMain+0)
12-11 18:40:48.794 19360 19360 F DEBUG   :       #53 pc 0000000000359650  /apex/com.android.art/lib64/libart.so (art::interpreter::Execute(art::Thread*, art::CodeItemDataAccessor const&, art::ShadowFrame&, art::JValue, bool, bool) (.__uniq.112435418011751916792819755956732575238.llvm.4560577758463694485)+428) (BuildId: 3f7d5a016e08d528f129bdd336d81168)
12-11 18:40:48.794 19360 19360 F DEBUG   :       #54 pc 0000000000367a78  /apex/com.android.art/lib64/libart.so (bool art::interpreter::DoCall<false>(art::ArtMethod*, art::Thread*, art::ShadowFrame&, art::Instruction const*, unsigned short, bool, art::JValue*)+4124) (BuildId: 3f7d5a016e08d528f129bdd336d81168)
12-11 18:40:48.794 19360 19360 F DEBUG   :       #55 pc 000000000076e170  /apex/com.android.art/lib64/libart.so (void art::interpreter::ExecuteSwitchImplCpp<false>(art::interpreter::SwitchImplContext*)+12208) (BuildId: 3f7d5a016e08d528f129bdd336d81168)
12-11 18:40:48.794 19360 19360 F DEBUG   :       #56 pc 00000000003869d8  /apex/com.android.art/lib64/libart.so (ExecuteSwitchImplAsm+8) (BuildId: 3f7d5a016e08d528f129bdd336d81168)
12-11 18:40:48.794 19360 19360 F DEBUG   :       #57 pc 00000000015d48b4  /data/app/~~l-OxVV4YDTj6ZSe3W8_iAQ==/org.chromium.chrome-I_qSoW9qSe-upz3rkj29ng==/oat/arm64/base.vdex (org.chromium.base.process_launcher.ChildProcessService.$r8$lambda$eZUxkj2POTXO6oIHcFpMMaOTgqA+0)
12-11 18:40:48.794 19360 19360 F DEBUG   :       #58 pc 0000000000359650  /apex/com.android.art/lib64/libart.so (art::interpreter::Execute(art::Thread*, art::CodeItemDataAccessor const&, art::ShadowFrame&, art::JValue, bool, bool) (.__uniq.112435418011751916792819755956732575238.llvm.4560577758463694485)+428) (BuildId: 3f7d5a016e08d528f129bdd336d81168)
12-11 18:40:48.794 19360 19360 F DEBUG   :       #59 pc 0000000000367a78  /apex/com.android.art/lib64/libart.so (bool art::interpreter::DoCall<false>(art::ArtMethod*, art::Thread*, art::ShadowFrame&, art::Instruction const*, unsigned short, bool, art::JValue*)+4124) (BuildId: 3f7d5a016e08d528f129bdd336d81168)
12-11 18:40:48.794 19360 19360 F DEBUG   :       #60 pc 000000000076e170  /apex/com.android.art/lib64/libart.so (void art::interpreter::ExecuteSwitchImplCpp<false>(art::interpreter::SwitchImplContext*)+12208) (BuildId: 3f7d5a016e08d528f129bdd336d81168)
12-11 18:40:48.794 19360 19360 F DEBUG   :       #61 pc 00000000003869d8  /apex/com.android.art/lib64/libart.so (ExecuteSwitchImplAsm+8) (BuildId: 3f7d5a016e08d528f129bdd336d81168)
12-11 18:40:48.794 19360 19360 F DEBUG   :       #62 pc 00000000015d419c  /data/app/~~l-OxVV4YDTj6ZSe3W8_iAQ==/org.chromium.chrome-I_qSoW9qSe-upz3rkj29ng==/oat/arm64/base.vdex (org.chromium.base.process_launcher.ChildProcessService$$ExternalSyntheticLambda1.run+0)
12-11 18:40:48.794 19360 19360 F DEBUG   :       #63 pc 00000000003589dc  /apex/com.android.art/lib64/libart.so (artQuickToInterpreterBridge+1932) (BuildId: 3f7d5a016e08d528f129bdd336d81168)
12-11 18:40:48.794 19360 19360 F DEBUG   :       #64 pc 0000000000384498  /apex/com.android.art/lib64/libart.so (art_quick_to_interpreter_bridge+88) (BuildId: 3f7d5a016e08d528f129bdd336d81168)
12-11 18:40:48.794 19360 19360 F DEBUG   :       #65 pc 0000000002004578  /memfd:jit-cache (deleted) (offset 0x2000000) (java.lang.Thread.run+136)
12-11 18:40:48.794 19360 19360 F DEBUG   :       #66 pc 000000000036db74  /apex/com.android.art/lib64/libart.so (art_quick_invoke_stub+612) (BuildId: 3f7d5a016e08d528f129bdd336d81168)
12-11 18:40:48.794 19360 19360 F DEBUG   :       #67 pc 0000000000359324  /apex/com.android.art/lib64/libart.so (art::ArtMethod::Invoke(art::Thread*, unsigned int*, unsigned int, art::JValue*, char const*)+132) (BuildId: 3f7d5a016e08d528f129bdd336d81168)
12-11 18:40:48.794 19360 19360 F DEBUG   :       #68 pc 0000000000944438  /apex/com.android.art/lib64/libart.so (_ZN3art9ArtMethod14InvokeInstanceILc86ETpTncJEEENS_6detail12ShortyTraitsIXT_EE4TypeEPNS_6ThreadENS_6ObjPtrINS_6mirror6ObjectEEEDpNS3_IXT0_EE4TypeE+60) (BuildId: 3f7d5a016e08d528f129bdd336d81168)
12-11 18:40:48.794 19360 19360 F DEBUG   :       #69 pc 00000000006209f4  /apex/com.android.art/lib64/libart.so (art::Thread::CreateCallback(void*)+1344) (BuildId: 3f7d5a016e08d528f129bdd336d81168)
12-11 18:40:48.794 19360 19360 F DEBUG   :       #70 pc 00000000006204a4  /apex/com.android.art/lib64/libart.so (art::Thread::CreateCallbackWithUffdGc(void*)+8) (BuildId: 3f7d5a016e08d528f129bdd336d81168)
12-11 18:40:48.794 19360 19360 F DEBUG   :       #71 pc 00000000000cba28  /apex/com.android.runtime/lib64/bionic/libc.so (__pthread_start(void*)+208) (BuildId: 6fbd0d7c6e3abc50de22e2fa6d2d6513)
12-11 18:40:48.794 19360 19360 F DEBUG   :       #72 pc 00000000000683b0  /apex/com.android.runtime/lib64/bionic/libc.so (__start_thread+64) (BuildId: 6fbd0d7c6e3abc50de22e2fa6d2d6513)

```
#### Reporter credit:

un3xploitable && GF

# Additional Data

Category: Security   

Chrome Channel: Stable   

Regression: N/A

## Attachments

- oob.html (text/html, 399.1 KB)

## Timeline

### kr...@google.com (2024-12-11)

[pore45214@gmail.com](mailto:pore45214@gmail.com): maybe attached the logcat as a file next time.

I can reproduce this on an Android device, and I see in the code that it is reasonable it happens so I think confirmed as a bug.

From my understanding this is a very old issue, looks like from 2016. It was maybe not reachable back at the time.

### kr...@google.com (2024-12-11)

dft@: I see geofflang@ is out for the next weeks, can you assign this as appropriate?

### pe...@google.com (2024-12-12)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2024-12-12)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### pe...@google.com (2024-12-30)

geofflang: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### pe...@google.com (2025-01-14)

geofflang: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ma...@google.com (2025-01-28)

[security shepherd] I pinged geofflang@ offline

### ap...@google.com (2025-02-05)

Project: chromium/src  

Branch: main  

Author: Geoff Lang <[geofflang@chromium.org](mailto:geofflang@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6226546>

Check query IDs before removing from active\_queries\_

---


Expand for full commit details
```
Check query IDs before removing from active_queries_ 
 
glDeleteQueries was removing queries from active_queries_ if they 
matched the type of query being deleted. It also needed to check that 
the ID matches. 
 
This would cause issues later when the real active query was ended and 
did not exist in the map. 
 
Bug: 383465163 
Change-Id: I1ea9d1b053324dbe86c8dceadd9e3b8aa2b41c64 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6226546 
Reviewed-by: Zhenyao Mo <zmo@chromium.org> 
Commit-Queue: Geoff Lang <geofflang@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#1416160}

```

---

Files:

- M `gpu/command_buffer/service/gles2_cmd_decoder_passthrough_doers.cc`
- M `gpu/command_buffer/tests/gl_query_unittest.cc`

---

Hash: d8747107c91751884bdc5a297b29e6ba1785e7e5  

Date:  Wed Feb 05 07:55:25 2025


---

### pe...@google.com (2025-02-10)

We commit ourselves to a 60 day deadline for fixing for s1 severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

### pe...@google.com (2025-02-11)

Security Merge Request Consideration: Requesting merge to extended stable (M132) because latest trunk commit (1416160) appears to be after extended stable branch point (1381561).
Security Merge Request Consideration: Requesting merge to stable (M133) because latest trunk commit (1416160) appears to be after stable branch point (1402768).
Security Merge Request Consideration: Requesting merge to beta (M134) because latest trunk commit (1416160) appears to be after beta branch point (1415337).
Security Merge Request - Manual Review: Merge review required: M132 is already shipping to stable.

Security Merge Request - Manual Review: Merge review required: M133 is already shipping to stable.

Security Merge Request - Manual Review: Merge review required: M134 is already shipping to beta.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [132, 133, 134].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### po...@gmail.com (2025-02-11)

Can I get CVE number?

### am...@chromium.org (2025-02-11)

<https://crrev.com/c/6226546> approved for merges, please merge to following channels and branches

- M134 Beta / branch 6998 (by 10am Pacific tomorrow, so this can be in the next beta)
- M133 Stable / branch 6943 (by EOD Thursday, 13 February so this fix can be included in the next Stable update)
- M132 Extended Stable / branch 6834

### ap...@google.com (2025-02-12)

Project: chromium/src  

Branch: refs/branch-heads/6834  

Author: Geoff Lang <[geofflang@chromium.org](mailto:geofflang@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6258068>

M132: Check query IDs before removing from active\_queries\_

---


Expand for full commit details
```
M132: Check query IDs before removing from active_queries_ 
 
glDeleteQueries was removing queries from active_queries_ if they 
matched the type of query being deleted. It also needed to check that 
the ID matches. 
 
This would cause issues later when the real active query was ended and 
did not exist in the map. 
 
(cherry picked from commit d8747107c91751884bdc5a297b29e6ba1785e7e5) 
 
Bug: 383465163 
Change-Id: I1ea9d1b053324dbe86c8dceadd9e3b8aa2b41c64 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6226546 
Reviewed-by: Zhenyao Mo <zmo@chromium.org> 
Commit-Queue: Geoff Lang <geofflang@chromium.org> 
Cr-Original-Commit-Position: refs/heads/main@{#1416160} 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6258068 
Cr-Commit-Position: refs/branch-heads/6834@{#5225} 
Cr-Branched-From: 47a3549fac11ee8cb7be6606001ede605b302b9f-refs/heads/main@{#1381561}

```

---

Files:

- M `gpu/command_buffer/service/gles2_cmd_decoder_passthrough_doers.cc`
- M `gpu/command_buffer/tests/gl_query_unittest.cc`

---

Hash: 408d9c5f391a719b18173d441f043ff35481edf8  

Date:  Wed Feb 12 10:48:28 2025


---

### ap...@google.com (2025-02-12)

Project: chromium/src  

Branch: refs/branch-heads/6998  

Author: Geoff Lang <[geofflang@chromium.org](mailto:geofflang@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6256659>

M134: Check query IDs before removing from active\_queries\_

---


Expand for full commit details
```
M134: Check query IDs before removing from active_queries_ 
 
glDeleteQueries was removing queries from active_queries_ if they 
matched the type of query being deleted. It also needed to check that 
the ID matches. 
 
This would cause issues later when the real active query was ended and 
did not exist in the map. 
 
(cherry picked from commit d8747107c91751884bdc5a297b29e6ba1785e7e5) 
 
Bug: 383465163 
Change-Id: I1ea9d1b053324dbe86c8dceadd9e3b8aa2b41c64 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6226546 
Reviewed-by: Zhenyao Mo <zmo@chromium.org> 
Commit-Queue: Geoff Lang <geofflang@chromium.org> 
Cr-Original-Commit-Position: refs/heads/main@{#1416160} 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6256659 
Cr-Commit-Position: refs/branch-heads/6998@{#578} 
Cr-Branched-From: de9c6fafd8ae5c6ea0438764076ca7d04a0b165d-refs/heads/main@{#1415337}

```

---

Files:

- M `gpu/command_buffer/service/gles2_cmd_decoder_passthrough_doers.cc`
- M `gpu/command_buffer/tests/gl_query_unittest.cc`

---

Hash: 5dd2b20deb7fb044181cd05bf0d7a10f508327c7  

Date:  Wed Feb 12 10:48:24 2025


---

### ap...@google.com (2025-02-12)

Project: chromium/src  

Branch: refs/branch-heads/6943  

Author: Geoff Lang <[geofflang@chromium.org](mailto:geofflang@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6258299>

M133: Check query IDs before removing from active\_queries\_

---


Expand for full commit details
```
M133: Check query IDs before removing from active_queries_ 
 
glDeleteQueries was removing queries from active_queries_ if they 
matched the type of query being deleted. It also needed to check that 
the ID matches. 
 
This would cause issues later when the real active query was ended and 
did not exist in the map. 
 
(cherry picked from commit d8747107c91751884bdc5a297b29e6ba1785e7e5) 
 
Bug: 383465163 
Change-Id: I1ea9d1b053324dbe86c8dceadd9e3b8aa2b41c64 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6226546 
Reviewed-by: Zhenyao Mo <zmo@chromium.org> 
Commit-Queue: Geoff Lang <geofflang@chromium.org> 
Cr-Original-Commit-Position: refs/heads/main@{#1416160} 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6258299 
Cr-Commit-Position: refs/branch-heads/6943@{#1521} 
Cr-Branched-From: 72dd0b377c099e1e0230cc7345d5a5125b46ae7d-refs/heads/main@{#1402768}

```

---

Files:

- M `gpu/command_buffer/service/gles2_cmd_decoder_passthrough_doers.cc`
- M `gpu/command_buffer/tests/gl_query_unittest.cc`

---

Hash: 74f85c0d6182f503178c9fb8ea74383c9b282c32  

Date:  Wed Feb 12 10:48:08 2025


---

### sp...@google.com (2025-02-20)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $10000.00 for this report.

Rationale for this decision:
report of memory corruption in a highly-privileged process (GPU) 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-02-20)

Congratulations! Thank you for your efforts and reporting this issue to us.

### ch...@google.com (2025-05-20)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### dx...@google.com (2025-05-29)

Project: chromium/src  

Branch: refs/branch-heads/6834\_160  

Author: Geoff Lang [geofflang@chromium.org](mailto:geofflang@chromium.org)  

Link:      <https://chromium-review.googlesource.com/6604415>

[CfM-R132] M132: Check query IDs before removing from active\_queries\_

---


Expand for full commit details
```
     
    glDeleteQueries was removing queries from active_queries_ if they 
    matched the type of query being deleted. It also needed to check that 
    the ID matches. 
     
    This would cause issues later when the real active query was ended and 
    did not exist in the map. 
     
    (cherry picked from commit d8747107c91751884bdc5a297b29e6ba1785e7e5) 
     
    (cherry picked from commit 408d9c5f391a719b18173d441f043ff35481edf8) 
     
    Bug: 383465163 
    Change-Id: I1ea9d1b053324dbe86c8dceadd9e3b8aa2b41c64 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6226546 
    Reviewed-by: Zhenyao Mo <zmo@chromium.org> 
    Commit-Queue: Geoff Lang <geofflang@chromium.org> 
    Cr-Original-Original-Commit-Position: refs/heads/main@{#1416160} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6258068 
    Cr-Original-Commit-Position: refs/branch-heads/6834@{#5225} 
    Cr-Original-Branched-From: 47a3549fac11ee8cb7be6606001ede605b302b9f-refs/heads/main@{#1381561} 
    Signed-off-by: Kyle Williams <kdgwill@google.com> 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6604415 
    Owners-Override: Kyle Williams <kdgwill@chromium.org> 
    Commit-Queue: Kyle Williams <kdgwill@chromium.org> 
    Auto-Submit: Kyle Williams <kdgwill@chromium.org> 
    Reviewed-by: Niko Tsirakis <ntsirakis@google.com> 
    Cr-Commit-Position: refs/branch-heads/6834_160@{#44} 
    Cr-Branched-From: cdae089eab830291f81deb011febbbdc520a019e-refs/branch-heads/6834@{#4409} 
    Cr-Branched-From: 47a3549fac11ee8cb7be6606001ede605b302b9f-refs/heads/main@{#1381561}

```

---

Files:

- M `gpu/command_buffer/service/gles2_cmd_decoder_passthrough_doers.cc`
- M `gpu/command_buffer/tests/gl_query_unittest.cc`

---

Hash: fd99415baec1852c703bffbe2a14cc3376cb941e  

Date:  Thu May 29 19:56:01 2025


---

## Bounty Award

> report of memory corruption in a highly-privileged process (GPU)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/383465163)*
