# Security: Heap use-after-free when bind/unbind TransformFeedback after deleting buffer

| Field | Value |
|-------|-------|
| **Issue ID** | [40059796](https://issues.chromium.org/issues/40059796) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU>ANGLE |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | gg...@gmail.com |
| **Assignee** | jm...@chromium.org |
| **Created** | 2022-05-30 |
| **Bounty** | $12,000.00 |

## Description

**VULNERABILITY DETAILS**  

There is a heap use-after-free vulnerability that exists in the Vulkan backend.

This vulnerability has a root cause similar to 1320024.  

1320024 is a vuln caused by not invalidate StateCache when transform feedback was removed.

This vulnerability occurs when binding and unbinding transform feedback after deleting the buffer.  

Because bindTransformFeedback does not call onActiveTransformFeedbackChange.

To fix this vulnerability, I think that the Context::bindTransformFeedback function should call  

onActiveTransformFeedbackChange of mStateCache to invalidate the drawStates cache.

**-------------------------** --------------------------------------------------------------  

void Context::bindTransformFeedback(GLenum target, TransformFeedbackID transformFeedbackHandle)  

{  

ASSERT(target == GL\_TRANSFORM\_FEEDBACK);  

TransformFeedback \*transformFeedback =  

checkTransformFeedbackAllocation(transformFeedbackHandle);  

mState.setTransformFeedbackBinding(this, transformFeedback);  

// call onActiveTransformFeedbackChange  

}  

**-------------------------** --------------------------------------------------------------

**VERSION**  

Chrome Version: master (and tested on 102.0.5005.63 (Official Build) (64-bit) Stable)  

Operating System: Windows/Linux (vulkan)

**REPRODUCTION CASE**  

Run the attached poc.html on Vulkan backend (--use-angle=vulkan)

# **FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION** Type of crash: GPU Process Crash State:

==24084==ERROR: AddressSanitizer: heap-use-after-free on address 0x1281fed38ef0 at pc 0x7fff1aa35e6d bp 0x006bac7fe200 sp 0x006bac7fe248  

READ of size 8 at 0x1281fed38ef0 thread T0  

==24084==WARNING: Failed to use and restart external symbolizer!  

==24084==\*\*\* WARNING: Failed to initialize DbgHelp! \*\*\*  

==24084==\*\*\* Most likely this means that the app is already \*\*\*  

==24084==\*\*\* using DbgHelp, possibly with incompatible flags. \*\*\*  

==24084==\*\*\* Due to technical reasons, symbolization might crash \*\*\*  

==24084==\*\*\* or produce wrong results. \*\*\*  

#0 0x7fff1aa35e6c in rx::vk::CommandBufferHelperCommon::bufferWrite C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\vk\_helpers.cpp:1372  

#1 0x7fff1a8afc13 in rx::ContextVk::handleDirtyGraphicsTransformFeedbackBuffersExtension C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\ContextVk.cpp:2431  

#2 0x7fff1a8bfcc6 in rx::ContextVk::setupDraw C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\ContextVk.cpp:1327  

#3 0x7fff1a8cafe3 in rx::ContextVk::drawArrays C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\ContextVk.cpp:3454  

#4 0x7fff1a151ba2 in GL\_DrawArrays C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libGLESv2\entry\_points\_gles\_2\_0\_autogen.cpp:1109  

#5 0x7fff00e2f17a in gpu::gles2::GLES2DecoderPassthroughImpl::DoDrawArrays C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\gles2\_cmd\_decoder\_passthrough\_doers.cc:1218  

#6 0x7ffefcee4e04 in gpu::gles2::GLES2DecoderPassthroughImpl::DoCommandsImpl<0> C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\gles2\_cmd\_decoder\_passthrough.cc:869  

#7 0x7ffefcee4262 in gpu::gles2::GLES2DecoderPassthroughImpl::DoCommands C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\gles2\_cmd\_decoder\_passthrough.cc:807  

#8 0x7ffef9c27a15 in gpu::CommandBufferService::Flush C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\command\_buffer\_service.cc:193  

#9 0x7ffef6e961f7 in gpu::CommandBufferStub::OnAsyncFlush C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command\_buffer\_stub.cc:505  

#10 0x7ffef6e953d2 in gpu::CommandBufferStub::ExecuteDeferredRequest C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command\_buffer\_stub.cc:152  

#11 0x7ffef6ea23fb in gpu::GpuChannel::ExecuteDeferredRequest C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\gpu\_channel.cc:708  

#12 0x7ffef6ead3d1 in base::internal::Invoker<base::internal::BindState<void (gpu::GpuChannel::\*)(mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);)),base::WeakPtr[gpu::GpuChannel](javascript:void(0);),mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);) >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind\_internal.h:747  

#13 0x7ffef6b011ba in gpu::Scheduler::RunNextTask C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\scheduler.cc:698  

#14 0x7ffef564f974 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:135  

#15 0x7ffef85728fd in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:422  

#16 0x7ffef8571afa in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:300  

#17 0x7ffef854e869 in base::MessagePumpDefault::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_default.cc:39  

#18 0x7ffef857441a in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:542  

#19 0x7ffef55b3717 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:141  

#20 0x7ffef7e2a447 in content::GpuMain C:\b\s\w\ir\cache\builder\src\content\gpu\gpu\_main.cc:400  

#21 0x7ffef516cab3 in content::RunOtherNamedProcessTypeMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:702  

#22 0x7ffef516e6ef in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1041  

#23 0x7ffef516b0e3 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:407  

#24 0x7ffef516b86c in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:435  

#25 0x7ffee9d014be in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc:177  

#26 0x7ff6c9855d52 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main\_dll\_loader\_win.cc:167  

#27 0x7ff6c9852b74 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_exe\_main\_win.cc:385  

#28 0x7ff6c9c5bc1f in \_\_scrt\_common\_main\_seh d:\a01\_work\12\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#29 0x7fff98677033 in BaseThreadInitThunk+0x13 (C:\WINDOWS\System32\KERNEL32.DLL+0x180017033)  

#30 0x7fff9a3a2650 in RtlUserThreadStart+0x20 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x180052650)

0x1281fed38ef0 is located 112 bytes inside of 328-byte region [0x1281fed38e80,0x1281fed38fc8)  

freed by thread T0 here:  

#0 0x7ff6c98fe9bb in free C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:82  

#1 0x7fff1a88f701 in rx::BufferVk::~BufferVk C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\BufferVk.cpp:245  

#2 0x7fff1a1a02e8 in gl::Buffer::~Buffer C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\Buffer.cpp:55  

#3 0x7fff1a1a1c17 in gl::Buffer::~Buffer C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\Buffer.cpp:54  

#4 0x7fff1a2f79e1 in gl::TypedResourceManager[gl::Sampler,gl::SamplerManager,gl::SamplerID](javascript:void(0);)::deleteObject C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\ResourceManager.cpp:96  

#5 0x7fff1a1f4865 in gl::Context::deleteBuffers C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\Context.cpp:6849  

#6 0x7fff1a1508e7 in GL\_DeleteBuffers C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libGLESv2\entry\_points\_gles\_2\_0\_autogen.cpp:819  

#7 0x7fff00e2c30b in gpu::gles2::GLES2DecoderPassthroughImpl::DoDeleteBuffers C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\gles2\_cmd\_decoder\_passthrough\_doers.cc:1013  

#8 0x7ffefcee4e04 in gpu::gles2::GLES2DecoderPassthroughImpl::DoCommandsImpl<0> C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\gles2\_cmd\_decoder\_passthrough.cc:869  

#9 0x7ffefcee4262 in gpu::gles2::GLES2DecoderPassthroughImpl::DoCommands C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\gles2\_cmd\_decoder\_passthrough.cc:807  

#10 0x7ffef9c27a15 in gpu::CommandBufferService::Flush C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\command\_buffer\_service.cc:193  

#11 0x7ffef6e961f7 in gpu::CommandBufferStub::OnAsyncFlush C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command\_buffer\_stub.cc:505  

#12 0x7ffef6e953d2 in gpu::CommandBufferStub::ExecuteDeferredRequest C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command\_buffer\_stub.cc:152  

#13 0x7ffef6ea23fb in gpu::GpuChannel::ExecuteDeferredRequest C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\gpu\_channel.cc:708  

#14 0x7ffef6ead3d1 in base::internal::Invoker<base::internal::BindState<void (gpu::GpuChannel::\*)(mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);)),base::WeakPtr[gpu::GpuChannel](javascript:void(0);),mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);) >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind\_internal.h:747  

#15 0x7ffef6b011ba in gpu::Scheduler::RunNextTask C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\scheduler.cc:698  

#16 0x7ffef564f974 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:135  

#17 0x7ffef85728fd in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:422  

#18 0x7ffef8571afa in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:300  

#19 0x7ffef854e869 in base::MessagePumpDefault::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_default.cc:39  

#20 0x7ffef857441a in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:542  

#21 0x7ffef55b3717 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:141  

#22 0x7ffef7e2a447 in content::GpuMain C:\b\s\w\ir\cache\builder\src\content\gpu\gpu\_main.cc:400  

#23 0x7ffef516cab3 in content::RunOtherNamedProcessTypeMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:702  

#24 0x7ffef516e6ef in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1041  

#25 0x7ffef516b0e3 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:407  

#26 0x7ffef516b86c in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:435  

#27 0x7ffee9d014be in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc:177

previously allocated by thread T0 here:  

#0 0x7ff6c98feabb in malloc C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:98  

#1 0x7fff1ae7a9b6 in operator new d:\a01\_work\12\s\src\vctools\crt\vcstartup\src\heap\new\_scalar.cpp:35  

#2 0x7fff1a8dcfc3 in rx::ContextVk::createBuffer C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\ContextVk.cpp:5358  

#3 0x7fff1a1a0076 in gl::Buffer::Buffer C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\Buffer.cpp:47  

#4 0x7fff1a2f936b in gl::BufferManager::AllocateNewObject C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\ResourceManager.cpp:114  

#5 0x7fff1a15bc60 in gl::TypedResourceManager[gl::Buffer,gl::BufferManager,gl::BufferID](javascript:void(0);)::checkObjectAllocationImpl<> C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\ResourceManager.h:117  

#6 0x7fff1a1c38f6 in gl::Context::bindBufferRange C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\Context.cpp:6346  

#7 0x7fff1a1ef8fa in gl::Context::bindBufferBase C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\Context.cpp:6337  

#8 0x7fff1a15e0b7 in GL\_BindBufferBase C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libGLESv2\entry\_points\_gles\_3\_0\_autogen.cpp:93  

#9 0x7fff00e27700 in gpu::gles2::GLES2DecoderPassthroughImpl::DoBindBufferBase C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\gles2\_cmd\_decoder\_passthrough\_doers.cc:410  

#10 0x7ffefcee4e04 in gpu::gles2::GLES2DecoderPassthroughImpl::DoCommandsImpl<0> C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\gles2\_cmd\_decoder\_passthrough.cc:869  

#11 0x7ffefcee4262 in gpu::gles2::GLES2DecoderPassthroughImpl::DoCommands C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\gles2\_cmd\_decoder\_passthrough.cc:807  

#12 0x7ffef9c27a15 in gpu::CommandBufferService::Flush C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\command\_buffer\_service.cc:193  

#13 0x7ffef6e961f7 in gpu::CommandBufferStub::OnAsyncFlush C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command\_buffer\_stub.cc:505  

#14 0x7ffef6e953d2 in gpu::CommandBufferStub::ExecuteDeferredRequest C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command\_buffer\_stub.cc:152  

#15 0x7ffef6ea23fb in gpu::GpuChannel::ExecuteDeferredRequest C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\gpu\_channel.cc:708  

#16 0x7ffef6ead3d1 in base::internal::Invoker<base::internal::BindState<void (gpu::GpuChannel::\*)(mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);)),base::WeakPtr[gpu::GpuChannel](javascript:void(0);),mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);) >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind\_internal.h:747  

#17 0x7ffef6b011ba in gpu::Scheduler::RunNextTask C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\scheduler.cc:698  

#18 0x7ffef564f974 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:135  

#19 0x7ffef85728fd in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:422  

#20 0x7ffef8571afa in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:300  

#21 0x7ffef854e869 in base::MessagePumpDefault::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_default.cc:39  

#22 0x7ffef857441a in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:542  

#23 0x7ffef55b3717 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:141  

#24 0x7ffef7e2a447 in content::GpuMain C:\b\s\w\ir\cache\builder\src\content\gpu\gpu\_main.cc:400  

#25 0x7ffef516cab3 in content::RunOtherNamedProcessTypeMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:702  

#26 0x7ffef516e6ef in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1041  

#27 0x7ffef516b0e3 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:407

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\vk\_helpers.cpp:1372 in rx::vk::CommandBufferHelperCommon::bufferWrite  

Shadow bytes around the buggy address:  

0x04ac3e827180: 00 00 00 00 00 00 00 00 00 00 fa fa fa fa fa fa  

0x04ac3e827190: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd  

0x04ac3e8271a0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x04ac3e8271b0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x04ac3e8271c0: fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa  

=>0x04ac3e8271d0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd[fd]fd  

0x04ac3e8271e0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x04ac3e8271f0: fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa  

0x04ac3e827200: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd  

0x04ac3e827210: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x04ac3e827220: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

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

==24084==ABORTING  

[14612:17076:0531/015128.803:ERROR:gpu\_process\_host.cc(966)] GPU process exited unexpectedly: exit\_code=1

**CREDIT INFORMATION**  

Reporter credit: SeongHwan Park (SeHwa)

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 1.8 KB)

## Timeline

### [Deleted User] (2022-05-30)

[Empty comment from Monorail migration]

### gg...@gmail.com (2022-05-30)

Here is the patch: https://crrev.com/c/3677115

### dr...@chromium.org (2022-05-30)

Unfortunately I get an error trying to reproduce this:
[420825:420825:0530/214439.142767:ERROR:gl_utils.cc(319)] [.WebGL-0x61b000059480]GL Driver Message (OpenGL, Performance, GL_CLOSE_PATH_NV, High): GPU stall due to ReadPixels

But I suspect that might be my machine/GPU, which isn't always the most reliable. Triaging assuming it can be reproduced, since owners of relevant code will be more able to test their GPU. jmadill@ - can you take a look?

[Monorail components: Internals>GPU>ANGLE]

### [Deleted User] (2022-05-30)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-05-31)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/d96cee6685099f6bcc392a4d20d28c8ec484673a

commit d96cee6685099f6bcc392a4d20d28c8ec484673a
Author: SeongHwan Park <ggabu423@gmail.com>
Date: Mon May 30 17:41:32 2022

Fix to invalidate cache when binding Transform Feedback.

Bug: chromium:1330379
Change-Id: I091116286ac511c50f9abcffa4d3cf350be920b4
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3677115
Commit-Queue: Jamie Madill <jmadill@chromium.org>
Reviewed-by: Jamie Madill <jmadill@chromium.org>

[modify] https://crrev.com/d96cee6685099f6bcc392a4d20d28c8ec484673a/src/tests/gl_tests/TransformFeedbackTest.cpp
[modify] https://crrev.com/d96cee6685099f6bcc392a4d20d28c8ec484673a/src/libANGLE/Context.cpp


### [Deleted User] (2022-05-31)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-05-31)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-05-31)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/152d0efcdba6b9c7fac9aa456cce4068494bfdd8

commit 152d0efcdba6b9c7fac9aa456cce4068494bfdd8
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Tue May 31 19:47:15 2022

Roll ANGLE from 86fce7a77eb2 to d96cee668509 (1 revision)

https://chromium.googlesource.com/angle/angle.git/+log/86fce7a77eb2..d96cee668509

2022-05-31 ggabu423@gmail.com Fix to invalidate cache when binding Transform Feedback.

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/angle-chromium-autoroll
Please CC geofflang@google.com on the revert to ensure that a human
is aware of the problem.

To file a bug in ANGLE: https://bugs.chromium.org/p/angleproject/issues/entry
To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86
Bug: chromium:1330379
Tbr: geofflang@google.com
Change-Id: Icdad3d61efcb436fccd9b71cc903b6a22bc43994
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3680139
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#1009229}

[modify] https://crrev.com/152d0efcdba6b9c7fac9aa456cce4068494bfdd8/DEPS


### jm...@chromium.org (2022-05-31)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-01)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-01)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-01)

Requesting merge to stable M102 because latest trunk commit (1009229) appears to be after stable branch point (992738).

Requesting merge to beta M103 because latest trunk commit (1009229) appears to be after beta branch point (1002911).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-06-01)

Merge review required: a commit with DEPS changes was detected.

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
Owners: govind (Android), harrysouders (iOS), dgagnon (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-06-01)

Merge review required: a commit with DEPS changes was detected.

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
Owners: eakpobaro (Android), harrysouders (iOS), ceb (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2022-06-06)

Approving merge to M103 and M102. Please merge to branches 5005 and 5060 (or ANGLE equivalents of course).

### gi...@appspot.gserviceaccount.com (2022-06-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/4eff86fbc7bb337bc2a30c3c2d69f36229c39ae6

commit 4eff86fbc7bb337bc2a30c3c2d69f36229c39ae6
Author: SeongHwan Park <ggabu423@gmail.com>
Date: Mon May 30 17:41:32 2022

[M103] Fix to invalidate cache when binding Transform Feedback.

Bug: chromium:1330379
Change-Id: I091116286ac511c50f9abcffa4d3cf350be920b4
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3677115
Commit-Queue: Jamie Madill <jmadill@chromium.org>
Reviewed-by: Jamie Madill <jmadill@chromium.org>
(cherry picked from commit d96cee6685099f6bcc392a4d20d28c8ec484673a)
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3691051
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>

[modify] https://crrev.com/4eff86fbc7bb337bc2a30c3c2d69f36229c39ae6/src/tests/gl_tests/TransformFeedbackTest.cpp
[modify] https://crrev.com/4eff86fbc7bb337bc2a30c3c2d69f36229c39ae6/src/libANGLE/Context.cpp


### [Deleted User] (2022-06-06)

LTS Milestone M102

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-06-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/9768648fffc94a434a7d400a2542ce3706224417

commit 9768648fffc94a434a7d400a2542ce3706224417
Author: SeongHwan Park <ggabu423@gmail.com>
Date: Mon May 30 17:41:32 2022

[M102] Fix to invalidate cache when binding Transform Feedback.

Bug: chromium:1330379
Change-Id: I091116286ac511c50f9abcffa4d3cf350be920b4
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3677115
Commit-Queue: Jamie Madill <jmadill@chromium.org>
Reviewed-by: Jamie Madill <jmadill@chromium.org>
(cherry picked from commit d96cee6685099f6bcc392a4d20d28c8ec484673a)
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3691799
Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>

[modify] https://crrev.com/9768648fffc94a434a7d400a2542ce3706224417/src/libANGLE/Context.cpp


### ad...@google.com (2022-06-06)

[Empty comment from Monorail migration]

### ad...@google.com (2022-06-06)

[Empty comment from Monorail migration]

### rz...@google.com (2022-06-07)

[Empty comment from Monorail migration]

### am...@google.com (2022-06-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-06-13)

Congratulations, SeongHwan! The VRP Panel had decided to award you $10,000 for this report + $2,000 patch bonus for your patch that you committed directly to Chromium. Thank you for your continued GPU bug discoveries and excellent work! 

### am...@google.com (2022-06-16)

[Empty comment from Monorail migration]

### rz...@google.com (2022-06-21)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-21)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2022-06-23)

1. Just https://crrev.com/c/3687713
2. Low, conflicts around the introduced test case
3. 102, 103
4. No

Test cases unrelated to the added test case are failing after the changes.  


### gm...@google.com (2022-06-23)

Evaluating recommendation.

### gm...@google.com (2022-06-27)

[Empty comment from Monorail migration]

### gm...@google.com (2022-07-01)

[Empty comment from Monorail migration]

### gm...@google.com (2022-07-01)

Not yet ready for approval. Still trying to resolve test failures.


### rz...@google.com (2022-07-06)

gmpritchard@ I checked the conflict resolution done when cherry-picking it to 102, and the test that was causing the issues was skipped. I did the same for 96 and it didn't cause issues on other tests, we can proceed with the merge.

### gm...@google.com (2022-07-06)

@rzanoni, OK, I will approve.

### gi...@appspot.gserviceaccount.com (2022-07-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/6753e54ecaa78d2583c8e25ec97d4ecef3045a16

commit 6753e54ecaa78d2583c8e25ec97d4ecef3045a16
Author: SeongHwan Park <ggabu423@gmail.com>
Date: Mon May 30 17:41:32 2022

[M96-LTS] Fix to invalidate cache when binding Transform Feedback.

Bug: chromium:1330379
No-Try: true
No-Presubmit: true
No-Tree-Checks: true
Change-Id: I091116286ac511c50f9abcffa4d3cf350be920b4
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3677115
Commit-Queue: Jamie Madill <jmadill@chromium.org>
(cherry picked from commit d96cee6685099f6bcc392a4d20d28c8ec484673a)
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3691799
(cherry picked from commit 9768648fffc94a434a7d400a2542ce3706224417)
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3687713
Reviewed-by: Jamie Madill <jmadill@chromium.org>
Auto-Submit: Roger Felipe Zanoni da Silva <rzanoni@google.com>

[modify] https://crrev.com/6753e54ecaa78d2583c8e25ec97d4ecef3045a16/src/libANGLE/Context.cpp


### rz...@google.com (2022-07-08)

[Empty comment from Monorail migration]

### am...@google.com (2022-07-28)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-28)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-07)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1330379?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-03-12)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059796)*
