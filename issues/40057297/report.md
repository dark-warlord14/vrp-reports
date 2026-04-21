# #Summary SUMMARY: AddressSanitizer: heap-use-after-free in gpu::CommandBufferProxyImpl::OnDisconnect

| Field | Value |
|-------|-------|
| **Issue ID** | [40057297](https://issues.chromium.org/issues/40057297) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU |
| **Platforms** | Windows |
| **Reporter** | m....@gmail.com |
| **Assignee** | ro...@google.com |
| **Created** | 2021-09-17 |
| **Bounty** | $7,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4628.3 Safari/537.36

Steps to reproduce the problem:
#TestOn
Windows NT 10.0; Win64; x64
git status
HEAD detached from 77ffd97a139

#Reproduce
This issue is not stable to reproduce, but it is easy to find through a code audit, so I did not provide a POC but provided an analysis

What is the expected behavior?

What went wrong?
Type of crash
gpu process

Did this work before? N/A 

Chrome version: 95.0.4628.3  Channel: n/a
OS Version: 10.0

#Analysis
CommandBufferProxyImpl is member of ContextProviderCommandBuffer obj,This issue occurs in a special situation, when CommandBufferProxyImpl::OnDisconnect is called, it will cause ContextProviderCommandBuffer obj to be released, resulting in UAF.

1. CommandBufferProxyImpl obj created when ContextProviderCommandBuffer::BindToCurrentThread() call and save as a unique_ptr member of ContextProviderCommandBuffer
2. CommandBufferProxyImpl::Initialize was call form ContextProviderCommandBuffer::BindToCurrentThread(),in CommandBufferProxyImpl::Initialize it will set CommandBufferProxyImpl::OnDisconnect as set_disconnect_handler callback
3. When set_disconnect_handler called OnDisconnect call OnGpuAsyncMessageError,which Will eventually call ContextProviderCommandBuffer::OnLostContext() because[4]
4. ContextProviderCommandBuffer::OnLostContext() will take ref of this[5],and relese this out of scope.
5. Then the function returns to CommandBufferProxyImpl::OnDisconnect and operates on lock_&last_state_lock_, because ContextProviderCommandBuffer released cause CommandBufferProxyImpl released too, resulting in UAF. 

```
//
services/viz/public/cpp/gpu/context_provider_command_buffer.cc：141
gpu::ContextResult ContextProviderCommandBuffer::BindToCurrentThread() {
  // This is called on the thread the context will be used.
  DCHECK(context_thread_checker_.CalledOnValidThread());

<<<-CUT->>>
  // This command buffer is a client-side proxy to the command buffer in the
  // GPU process.
  command_buffer_ = std::make_unique<gpu::CommandBufferProxyImpl>(			<<[1]
      channel_, gpu_memory_buffer_manager_, stream_id_, task_runner);
  bind_result_ = command_buffer_->Initialize(
      surface_handle_, /*shared_command_buffer=*/nullptr, stream_priority_,
      attributes_, active_url_);

//
gpu/ipc/client/command_buffer_proxy_impl.cc:136  
ContextResult CommandBufferProxyImpl::Initialize(
    gpu::SurfaceHandle surface_handle,
    CommandBufferProxyImpl* share_group,
    gpu::SchedulingPriority stream_priority,
    const gpu::ContextCreationAttribs& attribs,
    const GURL& active_url) {
  DCHECK(!share_group || (stream_id_ == share_group->stream_id_));
  TRACE_EVENT0("gpu", "GpuChannelHost::CreateViewCommandBuffer");

<<<-CUT->>>

  client_receiver_.set_disconnect_handler(base::BindOnce(
      &CommandBufferProxyImpl::OnDisconnect, base::Unretained(this)));		<<[2]

  channel_ = std::move(channel);
  return result;
}

//
gpu/ipc/client/command_buffer_proxy_impl.cc:156
void CommandBufferProxyImpl::OnDisconnect() {
  base::AutoLockMaybe lock(lock_);
  base::AutoLock last_state_lock(last_state_lock_);

  gpu::error::ContextLostReason context_lost_reason =
      gpu::error::kGpuChannelLost;
  if (shared_state_mapping_.IsValid()) {
    // The GPU process might have intentionally been crashed
    // (exit_on_context_lost), so try to find out the original reason.
    TryUpdateStateDontReportError();
    if (last_state_.error == gpu::error::kLostContext)
      context_lost_reason = last_state_.context_lost_reason;
  }
  OnGpuAsyncMessageError(context_lost_reason, gpu::error::kLostContext);		<<[3]
}

//
services/viz/public/cpp/gpu/context_provider_command_buffer.cc:295
gpu::ContextResult ContextProviderCommandBuffer::BindToCurrentThread() {
  // This is called on the thread the context will be used.
  DCHECK(context_thread_checker_.CalledOnValidThread());

<<<-CUT->>>
  // TODO(crbug.com/868192): SetLostContextCallback should probably work on
  // WebGPU contexts too.
  if (impl_) {
    impl_->SetLostContextCallback(
        base::BindOnce(&ContextProviderCommandBuffer::OnLostContext,			<<[4]
                       // |this| owns the impl_, which holds the callback.
                       base::Unretained(this)));
  }

//  
services/viz/public/cpp/gpu/context_provider_command_buffer.cc:483
void ContextProviderCommandBuffer::OnLostContext() {
  CheckValidThreadOrLockAcquired();

  // Ensure |this| isn't destroyed in the middle of OnLostContext() if observers
  // drop all references to it.
  scoped_refptr<ContextProviderCommandBuffer> ref(this);			  <<[5]
```

#Patch
I think there are many fix options, and I will provide them after thinking about them later.

#ASAN
[0915/191842.411:ERROR:command_buffer_proxy_impl.cc(328)] GPU state invalid after WaitForGetOffsetInRange.
[0915/191842.412:ERROR:gpu_process_host.cc(957)] GPU process exited unexpectedly: exit_code=1
[0915/191842.412:WARNING:gpu_process_host.cc(1270)] The GPU process has crashed 3 time(s)
=================================================================
==11692==ERROR: AddressSanitizer: heap-use-after-free on address 0x125548e6a110 at pc 0x7ffacd83c1aa bp 0x009824ff94a0 sp 0x009824ff94e8
READ of size 4 at 0x125548e6a110 thread T0
    #0 0x7ffacd83c1a9 in base::Lock::CheckUnheldAndMark+0x1d9 (E:\v8\chromium\src\out\0311\base.dll+0x18025c1a9)
    #1 0x7ffa9f77101d in gpu::CommandBufferProxyImpl::OnDisconnect+0x1e1 (E:\v8\chromium\src\out\0311\gpu.dll+0x18010101d)
    #2 0x7ffac99c1b20 in base::OnceCallback<void __cdecl(void)>::Run+0x126 (E:\v8\chromium\src\out\0311\bindings.dll+0x180011b20)
    #3 0x7ffac99d96fc in mojo::InterfaceEndpointClient::NotifyError+0x396 (E:\v8\chromium\src\out\0311\bindings.dll+0x1800296fc)
    #4 0x7ffabcae8260 in std::__1::unique_ptr<mojo::SequenceLocalSyncEventWatcher,std::__1::default_delete<mojo::SequenceLocalSyncEventWatcher> >::reset+0x2900 (E:\v8\chromium\src\out\0311\ipc.dll+0x180048260)
    #5 0x7ffabcae8a39 in scoped_refptr<base::SequencedTaskRunner>::operator=+0x30d (E:\v8\chromium\src\out\0311\ipc.dll+0x180048a39)
    #6 0x7ffacd852aae in base::TaskAnnotator::RunTask+0x4be (E:\v8\chromium\src\out\0311\base.dll+0x180272aae)
    #7 0x7ffacd8c8622 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl+0x962 (E:\v8\chromium\src\out\0311\base.dll+0x1802e8622)
    #8 0x7ffacd8c701d in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork+0x1bd (E:\v8\chromium\src\out\0311\base.dll+0x1802e701d)
    #9 0x7ffacd6bd0a7 in base::MessagePumpDefault::Run+0x297 (E:\v8\chromium\src\out\0311\base.dll+0x1800dd0a7)
    #10 0x7ffacd8ca9ef in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run+0x5ff (E:\v8\chromium\src\out\0311\base.dll+0x1802ea9ef)
    #11 0x7ffacd791b15 in base::RunLoop::Run+0x755 (E:\v8\chromium\src\out\0311\base.dll+0x1801b1b15)
    #12 0x7ffaa3870f83 in content::RendererMain+0x76f (E:\v8\chromium\src\out\0311\content.dll+0x183d10f83)
    #13 0x7ffaa3da880c in content::ContentMainRunnerImpl::Run+0x3f2 (E:\v8\chromium\src\out\0311\content.dll+0x18424880c)
    #14 0x7ffaa3da4bea in content::RunContentProcess+0x55e (E:\v8\chromium\src\out\0311\content.dll+0x184244bea)
    #15 0x7ffaa3da5c29 in content::ContentMain+0xc6 (E:\v8\chromium\src\out\0311\content.dll+0x184245c29)
    #16 0x7ffaab9aadca in headless::HeadlessShellMain+0x445 (E:\v8\chromium\src\out\0311\chrome.dll+0x1841aadca)
    #17 0x7ffaab9aa5f3 in headless::RunChildProcessIfNeeded+0x40f (E:\v8\chromium\src\out\0311\chrome.dll+0x1841aa5f3)
    #18 0x7ffaab9a735e in headless::HeadlessShellMain+0x515 (E:\v8\chromium\src\out\0311\chrome.dll+0x1841a735e)
    #19 0x7ffaa78014ae in ChromeMain+0x3aa (E:\v8\chromium\src\out\0311\chrome.dll+0x1800014ae)
    #20 0x7ff792ba5b15 in MainDllLoader::Launch+0x467 (E:\v8\chromium\src\out\0311\chrome.exe+0x140005b15)
    #21 0x7ff792ba2d8d in main+0x1d1f (E:\v8\chromium\src\out\0311\chrome.exe+0x140002d8d)
    #22 0x7ff792dc509b in __scrt_common_main_seh D:\a01\_work\9\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #23 0x7ffaf3887033 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x180017033)
    #24 0x7ffaf57a2650 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x180052650)

0x125548e6a110 is located 144 bytes inside of 1008-byte region [0x125548e6a080,0x125548e6a470)
freed by thread T0 here:
    #0 0x7ffacccbdfab in operator delete+0x8b (E:\v8\chromium\src\out\0311\clang_rt.asan_dynamic-x86_64.dll+0x18003dfab)
    #1 0x7ffa9f77be71 in gpu::CommandBufferProxyImpl::`scalar deleting destructor'+0x1b (E:\v8\chromium\src\out\0311\gpu.dll+0x18010be71)
    #2 0x7ffaa36870a4 in viz::ContextProviderCommandBuffer::~ContextProviderCommandBuffer+0x612 (E:\v8\chromium\src\out\0311\content.dll+0x183b270a4)
    #3 0x7ffaa368f2b7 in viz::ContextProviderCommandBuffer::`scalar deleting destructor'+0xf (E:\v8\chromium\src\out\0311\content.dll+0x183b2f2b7)
    #4 0x7ffaa368b921 in viz::ContextProviderCommandBuffer::OnLostContext+0x34b (E:\v8\chromium\src\out\0311\content.dll+0x183b2b921)
    #5 0x7ffa5801d8f0 in base::OnceCallback<void __cdecl(void)>::Run+0x126 (E:\v8\chromium\src\out\0311\gles2_implementation.dll+0x18000d8f0)
    #6 0x7ffa5801d73f in gpu::gles2::GLES2Implementation::OnGpuControlLostContext+0x173 (E:\v8\chromium\src\out\0311\gles2_implementation.dll+0x18000d73f)
    #7 0x7ffa9f76e89a in gpu::CommandBufferProxyImpl::DisconnectChannel+0x230 (E:\v8\chromium\src\out\0311\gpu.dll+0x1800fe89a)
    #8 0x7ffa9f77120f in gpu::CommandBufferProxyImpl::OnGpuAsyncMessageError+0x7f (E:\v8\chromium\src\out\0311\gpu.dll+0x18010120f)
    #9 0x7ffa9f77101d in gpu::CommandBufferProxyImpl::OnDisconnect+0x1e1 (E:\v8\chromium\src\out\0311\gpu.dll+0x18010101d)
    #10 0x7ffac99c1b20 in base::OnceCallback<void __cdecl(void)>::Run+0x126 (E:\v8\chromium\src\out\0311\bindings.dll+0x180011b20)
    #11 0x7ffac99d96fc in mojo::InterfaceEndpointClient::NotifyError+0x396 (E:\v8\chromium\src\out\0311\bindings.dll+0x1800296fc)
    #12 0x7ffabcae8260 in std::__1::unique_ptr<mojo::SequenceLocalSyncEventWatcher,std::__1::default_delete<mojo::SequenceLocalSyncEventWatcher> >::reset+0x2900 (E:\v8\chromium\src\out\0311\ipc.dll+0x180048260)
    #13 0x7ffabcae8a39 in scoped_refptr<base::SequencedTaskRunner>::operator=+0x30d (E:\v8\chromium\src\out\0311\ipc.dll+0x180048a39)
    #14 0x7ffacd852aae in base::TaskAnnotator::RunTask+0x4be (E:\v8\chromium\src\out\0311\base.dll+0x180272aae)
    #15 0x7ffacd8c8622 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl+0x962 (E:\v8\chromium\src\out\0311\base.dll+0x1802e8622)
    #16 0x7ffacd8c701d in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork+0x1bd (E:\v8\chromium\src\out\0311\base.dll+0x1802e701d)
    #17 0x7ffacd6bd0a7 in base::MessagePumpDefault::Run+0x297 (E:\v8\chromium\src\out\0311\base.dll+0x1800dd0a7)
    #18 0x7ffacd8ca9ef in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run+0x5ff (E:\v8\chromium\src\out\0311\base.dll+0x1802ea9ef)
    #19 0x7ffacd791b15 in base::RunLoop::Run+0x755 (E:\v8\chromium\src\out\0311\base.dll+0x1801b1b15)
    #20 0x7ffaa3870f83 in content::RendererMain+0x76f (E:\v8\chromium\src\out\0311\content.dll+0x183d10f83)
    #21 0x7ffaa3da880c in content::ContentMainRunnerImpl::Run+0x3f2 (E:\v8\chromium\src\out\0311\content.dll+0x18424880c)
    #22 0x7ffaa3da4bea in content::RunContentProcess+0x55e (E:\v8\chromium\src\out\0311\content.dll+0x184244bea)
    #23 0x7ffaa3da5c29 in content::ContentMain+0xc6 (E:\v8\chromium\src\out\0311\content.dll+0x184245c29)
    #24 0x7ffaab9aadca in headless::HeadlessShellMain+0x445 (E:\v8\chromium\src\out\0311\chrome.dll+0x1841aadca)
    #25 0x7ffaab9aa5f3 in headless::RunChildProcessIfNeeded+0x40f (E:\v8\chromium\src\out\0311\chrome.dll+0x1841aa5f3)
    #26 0x7ffaab9a735e in headless::HeadlessShellMain+0x515 (E:\v8\chromium\src\out\0311\chrome.dll+0x1841a735e)
    #27 0x7ffaa78014ae in ChromeMain+0x3aa (E:\v8\chromium\src\out\0311\chrome.dll+0x1800014ae)

previously allocated by thread T0 here:
    #0 0x7ffacccbdcbb in operator new+0x8b (E:\v8\chromium\src\out\0311\clang_rt.asan_dynamic-x86_64.dll+0x18003dcbb)
    #1 0x7ffaa36880c8 in viz::ContextProviderCommandBuffer::BindToCurrentThread+0x52c (E:\v8\chromium\src\out\0311\content.dll+0x183b280c8)
    #2 0x7ffaa38d8535 in content::WebGraphicsContext3DProviderImpl::BindToCurrentThread+0x79 (E:\v8\chromium\src\out\0311\content.dll+0x183d78535)
    #3 0x7ffa6e85daea in blink::WebGLRenderingContextBase::CreateContextProviderInternal+0x552 (E:\v8\chromium\src\out\0311\blink_modules.dll+0x18265daea)
    #4 0x7ffa6e85f050 in blink::WebGLRenderingContextBase::CreateWebGraphicsContext3DProvider+0x170 (E:\v8\chromium\src\out\0311\blink_modules.dll+0x18265f050)
    #5 0x7ffa6e84532c in blink::WebGLRenderingContext::Factory::Create+0x278 (E:\v8\chromium\src\out\0311\blink_modules.dll+0x18264532c)
    #6 0x7ffa7a557d29 in blink::OffscreenCanvas::GetCanvasRenderingContext+0xd09 (E:\v8\chromium\src\out\0311\blink_core.dll+0x183577d29)
    #7 0x7ffa6d5656e5 in blink::OffscreenCanvasModule::getContext+0x161 (E:\v8\chromium\src\out\0311\blink_modules.dll+0x1813656e5)
    #8 0x7ffa6cb32175 in blink::V8OffscreenCanvas::Impl::InstallUnconditionalProperties+0x2485 (E:\v8\chromium\src\out\0311\blink_modules.dll+0x180932175)
    #9 0x7ffa80322976 in v8::internal::FunctionCallbackArguments::Call+0x766 (E:\v8\chromium\src\out\0311\v8.dll+0x180352976)
    #10 0x7ffa8031d849 in v8::internal::Builtins::InvokeApiFunction+0x4909 (E:\v8\chromium\src\out\0311\v8.dll+0x18034d849)
    #11 0x7ffa803181f7 in v8::internal::BuiltinArguments::BuiltinArguments+0x7c7 (E:\v8\chromium\src\out\0311\v8.dll+0x1803481f7)
    #12 0x7ffa80317101 in v8::internal::Builtin_HandleApiCall+0x1d1 (E:\v8\chromium\src\out\0311\v8.dll+0x180347101)
    #13 0x7e9c000d363b  (<unknown module>)

SUMMARY: AddressSanitizer: heap-use-after-free (E:\v8\chromium\src\out\0311\base.dll+0x18025c1a9) in base::Lock::CheckUnheldAndMark+0x1d9
Shadow bytes around the buggy address:
  0x046df1ecd3d0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x046df1ecd3e0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x046df1ecd3f0: fd fd fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x046df1ecd400: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x046df1ecd410: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
=>0x046df1ecd420: fd fd[fd]fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x046df1ecd430: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x046df1ecd440: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x046df1ecd450: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x046df1ecd460: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x046df1ecd470: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
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
==11692==ABORTING

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 10.6 KB)

## Timeline

### [Deleted User] (2021-09-17)

[Empty comment from Monorail migration]

### ca...@chromium.org (2021-09-17)

Tentatively triageing as valid since the steps seem feasible, though there is no reproduction case.

rockot: I see you've worked on the affected file recently, can you PTAL? Feel free to reassign to a better owner if appropriate. Thanks.

[Monorail components: Internals>GPU]

### [Deleted User] (2021-09-17)

[Empty comment from Monorail migration]

### ro...@google.com (2021-09-17)

Looks valid, and also looks like this bug may have existed for quite a while.

AFAICT ContextProviderCommandBuffer has ~always synchronously invoked OnContextLost on its observers in response to context loss, and CommandBufferProxyImpl has never been safe to delete within GpuControlClient::OnGpuControlLostContext due to CBPI's lock management around that invocation.

So as long as it's been possible for an observer's OnContextLost to result in CPCB deletion, this bug has been possible. I see a local stack ref was added some time later to prevent the CPCB from being destroyed within OnLostContext itself, but of course it (and its CBPI) can still then be destroyed upon OnLostContext return in that case.

### [Deleted User] (2021-09-18)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-09-18)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-09-18)

[Empty comment from Monorail migration]

### ky...@chromium.org (2021-09-20)

ContextProviderCommandBuffer owns a pretty complicated hierarchy of classes and context loss handling code is messy. I'm sure the context loss code could be reworked to be a bit more straight forward and hopefully avoid this UAF but..

I wonder if ContextProviderCommandBuffer::OnLostContext() could just post a task to delete the scoped_ref<ContextProviderCommandBuffer> it holds to ensure it's impossible to destroy the ContextProviderCommandBuffer object in the same call stack as the context loss event?

### [Deleted User] (2021-09-22)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-02)

rockot: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-10-16)

rockot: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### m....@gmail.com (2021-11-10)

re#c4 rockot@ Do you have time to look at this issue, or assign it to someone else, thanks.

### [Deleted User] (2021-11-15)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-16)

We commit ourselves to a 60 day deadline for fixing for high severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### do...@chromium.org (2022-01-24)

Security marshall ping: this issue has exceeded the 60 day deadline we set for fixing high severity security issues.

rockot/sunnyps/kylechar: can you urgently follow up on this issue and identify what the next steps are to fix it? Specifically, will the suggestion in #8 work?

### ro...@google.com (2022-01-25)

Fix is up at https://chromium-review.googlesource.com/c/chromium/src/+/3414063

### gi...@appspot.gserviceaccount.com (2022-01-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/98d246cabe677e1d8287e4d42ce02825417be9e2

commit 98d246cabe677e1d8287e4d42ce02825417be9e2
Author: Ken Rockot <rockot@google.com>
Date: Tue Jan 25 16:18:37 2022

Viz: Fix UAF on context loss

Fixed: 1250655
Change-Id: I2898316635d370fa36b94e0ae2564ed357745b2c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3413372
Auto-Submit: Ken Rockot <rockot@google.com>
Reviewed-by: Kyle Charbonneau <kylechar@chromium.org>
Commit-Queue: Kyle Charbonneau <kylechar@chromium.org>
Cr-Commit-Position: refs/heads/main@{#963012}

[modify] https://crrev.com/98d246cabe677e1d8287e4d42ce02825417be9e2/services/viz/public/cpp/gpu/context_provider_command_buffer.cc


### [Deleted User] (2022-01-26)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-26)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-26)

Requesting merge to extended stable M96 because latest trunk commit (963012) appears to be after extended stable branch point (929512).

Requesting merge to stable M97 because latest trunk commit (963012) appears to be after stable branch point (938553).

Requesting merge to beta M98 because latest trunk commit (963012) appears to be after beta branch point (950365).

Requesting merge to dev M99 because latest trunk commit (963012) appears to be after dev branch point (961656).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-26)

Merge approved: your change passed merge requirements and is auto-approved for M99. Please go ahead and merge the CL to branch 4844 (refs/branch-heads/4844) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: benmason (Android), harrysouders (iOS), cindyb (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-26)

Merge review required: M98 has already been cut for stable release.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), harrysouders (iOS), matthewjoseph (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-26)

Merge review required: M97 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: benmason (Android), harrysouders (iOS), ceb (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-26)

Merge review required: M96 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), harrysouders (iOS), dgagnon (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pb...@google.com (2022-01-27)

Your change has been approved for M99 branch 4844,please go ahead and merge the CL's manually asap so that they would be part of tomorrow's M99 Dev release.

### gi...@appspot.gserviceaccount.com (2022-01-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/1f67cc8f7fc671b3cfc571f2b52bf8fbf09cfa97

commit 1f67cc8f7fc671b3cfc571f2b52bf8fbf09cfa97
Author: Ken Rockot <rockot@google.com>
Date: Thu Jan 27 21:37:53 2022

Viz: Fix UAF on context loss

(cherry picked from commit 98d246cabe677e1d8287e4d42ce02825417be9e2)

Fixed: 1250655
Change-Id: I2898316635d370fa36b94e0ae2564ed357745b2c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3413372
Auto-Submit: Ken Rockot <rockot@google.com>
Reviewed-by: Kyle Charbonneau <kylechar@chromium.org>
Commit-Queue: Kyle Charbonneau <kylechar@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#963012}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3421375
Commit-Queue: Ken Rockot <rockot@google.com>
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/4844@{#88}
Cr-Branched-From: 007241ce2e6c8e5a7b306cc36c730cd07cd38825-refs/heads/main@{#961656}

[modify] https://crrev.com/1f67cc8f7fc671b3cfc571f2b52bf8fbf09cfa97/services/viz/public/cpp/gpu/context_provider_command_buffer.cc


### am...@chromium.org (2022-02-02)

merge approved for M98, please merge this fix to branch 4758 at your earliest convenience so this fix can be included in the next security refresh 

### gi...@appspot.gserviceaccount.com (2022-02-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/be50c60b422563e672ed59324b79b8863e336739

commit be50c60b422563e672ed59324b79b8863e336739
Author: Ken Rockot <rockot@google.com>
Date: Wed Feb 02 05:45:44 2022

Viz: Fix UAF on context loss

(cherry picked from commit 98d246cabe677e1d8287e4d42ce02825417be9e2)

Fixed: 1250655
Change-Id: I2898316635d370fa36b94e0ae2564ed357745b2c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3413372
Auto-Submit: Ken Rockot <rockot@google.com>
Reviewed-by: Kyle Charbonneau <kylechar@chromium.org>
Commit-Queue: Kyle Charbonneau <kylechar@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#963012}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3430523
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Commit-Queue: Ken Rockot <rockot@google.com>
Cr-Commit-Position: refs/branch-heads/4758@{#1050}
Cr-Branched-From: 4a2cf4baf90326df19c3ee70ff987960d59a386e-refs/heads/main@{#950365}

[modify] https://crrev.com/be50c60b422563e672ed59324b79b8863e336739/services/viz/public/cpp/gpu/context_provider_command_buffer.cc


### am...@chromium.org (2022-02-12)

[Empty comment from Monorail migration]

### am...@google.com (2022-02-14)

[Empty comment from Monorail migration]

### am...@google.com (2022-02-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-02-17)

Congratulations on another one! The VRP Panel has decided to award you $7000 for this report of a GPU security bug. Thank you for your efforts and nice work! 

### am...@google.com (2022-02-18)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-03)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-07-21)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-29)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1250655?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057297)*
