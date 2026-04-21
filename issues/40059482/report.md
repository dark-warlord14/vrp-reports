# Security: [ANGLE] Heap use-after-free when deleting TransformFeedback

| Field | Value |
|-------|-------|
| **Issue ID** | [40059482](https://issues.chromium.org/issues/40059482) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU>ANGLE |
| **Platforms** | Windows |
| **Reporter** | gg...@gmail.com |
| **Assignee** | jm...@chromium.org |
| **Created** | 2022-04-26 |
| **Bounty** | $10,000.00 |

## Description

**VULNERABILITY DETAILS**  

There is a heap use-after-free vulnerability that exists in the Vulkan backend.

I think that this vulnerability is caused by not invalidate the drawStates cache for TransformFeedback binding changes.  

last drawArrays in the attached PoC should cause an error in the following validation.  

**-------------------------** --------------------------------------------------------------  

const char \*ValidateDrawStates(const Context \*context)  

{  

....  

if (state.isTransformFeedbackActive())  

{  

if (!ValidateProgramExecutableXFBBuffersPresent(context, executable))  

{  

return kTransformFeedbackBufferMissing;  

}  

}  

**-------------------------** --------------------------------------------------------------

|mCachedBasicDrawStatesError| is cached when binding a new TransformFeedback and calling drawArrays.  

However cache is not invalidated when deleting the transformfeedback and rebinding it with the previous TransformFeedback.  

As a result, the ValidateDrawStates function is never called.  

**-------------------------** --------------------------------------------------------------  

intptr\_t getBasicDrawStatesError(const Context \*context) const  

{  

if (mCachedBasicDrawStatesError != kInvalidPointer) <-- true  

{  

return mCachedBasicDrawStatesError;  

}

```
    return getBasicDrawStatesErrorImpl(context);  
}  

```

**-------------------------** --------------------------------------------------------------

**VERSION**  

Chrome Version: master (and tested on 101.0.4951.41 (Official Build) (64-bit) Stable)  

Operating System: Windows/Linux (vulkan)

**REPRODUCTION CASE**  

Run the attached poc.html on Vulkan backend (--use-angle=vulkan)

# **FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION** Type of crash: GPU Process Crash State:

==11296==ERROR: AddressSanitizer: heap-use-after-free on address 0x118411575df0 at pc 0x7ffc35f1350f bp 0x0038045fe2c0 sp 0x0038045fe308  

READ of size 8 at 0x118411575df0 thread T0  

==11296==WARNING: Failed to use and restart external symbolizer!  

==11296==\*\*\* WARNING: Failed to initialize DbgHelp! \*\*\*  

==11296==\*\*\* Most likely this means that the app is already \*\*\*  

==11296==\*\*\* using DbgHelp, possibly with incompatible flags. \*\*\*  

==11296==\*\*\* Due to technical reasons, symbolization might crash \*\*\*  

==11296==\*\*\* or produce wrong results. \*\*\*  

#0 0x7ffc35f1350e in rx::vk::CommandBufferHelperCommon::bufferWrite C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\vk\_helpers.cpp:1305  

#1 0x7ffc35d990a3 in rx::ContextVk::handleDirtyGraphicsTransformFeedbackBuffersExtension C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\ContextVk.cpp:2318  

#2 0x7ffc35da1eb8 in rx::ContextVk::setupDraw C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\ContextVk.cpp:1254  

#3 0x7ffc35dad2c3 in rx::ContextVk::drawArrays C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\ContextVk.cpp:3070  

#4 0x7ffc35631b36 in GL\_DrawArrays C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libGLESv2\entry\_points\_gles\_2\_0\_autogen.cpp:1109  

#5 0x7ffc4d4c59d2 in gpu::gles2::GLES2DecoderPassthroughImpl::DoDrawArrays C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\gles2\_cmd\_decoder\_passthrough\_doers.cc:1217  

#6 0x7ffc4965148b in gpu::gles2::GLES2DecoderPassthroughImpl::DoCommandsImpl<0> C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\gles2\_cmd\_decoder\_passthrough.cc:870  

#7 0x7ffc496508e0 in gpu::gles2::GLES2DecoderPassthroughImpl::DoCommands C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\gles2\_cmd\_decoder\_passthrough.cc:808  

#8 0x7ffc463cbb5f in gpu::CommandBufferService::Flush C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\command\_buffer\_service.cc:70  

#9 0x7ffc436b61d8 in gpu::CommandBufferStub::OnAsyncFlush C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command\_buffer\_stub.cc:500  

#10 0x7ffc436b53b2 in gpu::CommandBufferStub::ExecuteDeferredRequest C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command\_buffer\_stub.cc:152  

#11 0x7ffc436c1da3 in gpu::GpuChannel::ExecuteDeferredRequest C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\gpu\_channel.cc:705  

#12 0x7ffc436cd399 in base::internal::Invoker<base::internal::BindState<void (gpu::GpuChannel::\*)(mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);)),base::WeakPtr[gpu::GpuChannel](javascript:void(0);),mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);) >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind\_internal.h:748  

#13 0x7ffc432f1824 in gpu::Scheduler::RunNextTask C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\scheduler.cc:691  

#14 0x7ffc41e83d94 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:135  

#15 0x7ffc44d2a055 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:386  

#16 0x7ffc44d29629 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:291  

#17 0x7ffc44d0664a in base::MessagePumpDefault::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_default.cc:39  

#18 0x7ffc44d2b810 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:498  

#19 0x7ffc41df6377 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:141  

#20 0x7ffc446007ae in content::GpuMain C:\b\s\w\ir\cache\builder\src\content\gpu\gpu\_main.cc:405  

#21 0x7ffc41a21aeb in content::RunOtherNamedProcessTypeMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:701  

#22 0x7ffc41a23727 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1040  

#23 0x7ffc41a2011b in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:407  

#24 0x7ffc41a208a4 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:435  

#25 0x7ffc369b14cb in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc:177  

#26 0x7ff6874a5b16 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main\_dll\_loader\_win.cc:167  

#27 0x7ff6874a2b5f in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_exe\_main\_win.cc:382  

#28 0x7ff6878a0e1b in \_\_scrt\_common\_main\_seh d:\a01\_work\12\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#29 0x7ffce92f7033 in BaseThreadInitThunk+0x13 (C:\WINDOWS\System32\KERNEL32.DLL+0x180017033)  

#30 0x7ffceadc2650 in RtlUserThreadStart+0x20 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x180052650)

0x118411575df0 is located 112 bytes inside of 328-byte region [0x118411575d80,0x118411575ec8)  

freed by thread T0 here:  

#0 0x7ff68754e37b in free C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:82  

#1 0x7ffc35d7993d in rx::BufferVk::~BufferVk C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\BufferVk.cpp:254  

#2 0x7ffc3568047e in gl::Buffer::~Buffer C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\Buffer.cpp:55  

#3 0x7ffc35681e57 in gl::Buffer::~Buffer C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\Buffer.cpp:54  

#4 0x7ffc357d79f3 in gl::TypedResourceManager[gl::Sampler,gl::SamplerManager,gl::SamplerID](javascript:void(0);)::deleteObject C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\ResourceManager.cpp:96  

#5 0x7ffc356d47b9 in gl::Context::deleteBuffers C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\Context.cpp:6826  

#6 0x7ffc3563087b in GL\_DeleteBuffers C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libGLESv2\entry\_points\_gles\_2\_0\_autogen.cpp:819  

#7 0x7ffc4d4c2be5 in gpu::gles2::GLES2DecoderPassthroughImpl::DoDeleteBuffers C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\gles2\_cmd\_decoder\_passthrough\_doers.cc:1012  

#8 0x7ffc4965148b in gpu::gles2::GLES2DecoderPassthroughImpl::DoCommandsImpl<0> C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\gles2\_cmd\_decoder\_passthrough.cc:870  

#9 0x7ffc496508e0 in gpu::gles2::GLES2DecoderPassthroughImpl::DoCommands C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\gles2\_cmd\_decoder\_passthrough.cc:808  

#10 0x7ffc463cbb5f in gpu::CommandBufferService::Flush C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\command\_buffer\_service.cc:70  

#11 0x7ffc436b61d8 in gpu::CommandBufferStub::OnAsyncFlush C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command\_buffer\_stub.cc:500  

#12 0x7ffc436b53b2 in gpu::CommandBufferStub::ExecuteDeferredRequest C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command\_buffer\_stub.cc:152  

#13 0x7ffc436c1da3 in gpu::GpuChannel::ExecuteDeferredRequest C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\gpu\_channel.cc:705  

#14 0x7ffc436cd399 in base::internal::Invoker<base::internal::BindState<void (gpu::GpuChannel::\*)(mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);)),base::WeakPtr[gpu::GpuChannel](javascript:void(0);),mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);) >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind\_internal.h:748  

#15 0x7ffc432f1824 in gpu::Scheduler::RunNextTask C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\scheduler.cc:691  

#16 0x7ffc41e83d94 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:135  

#17 0x7ffc44d2a055 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:386  

#18 0x7ffc44d29629 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:291  

#19 0x7ffc44d0664a in base::MessagePumpDefault::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_default.cc:39  

#20 0x7ffc44d2b810 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:498  

#21 0x7ffc41df6377 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:141  

#22 0x7ffc446007ae in content::GpuMain C:\b\s\w\ir\cache\builder\src\content\gpu\gpu\_main.cc:405  

#23 0x7ffc41a21aeb in content::RunOtherNamedProcessTypeMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:701  

#24 0x7ffc41a23727 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1040  

#25 0x7ffc41a2011b in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:407  

#26 0x7ffc41a208a4 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:435  

#27 0x7ffc369b14cb in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc:177

previously allocated by thread T0 here:  

#0 0x7ff68754e47b in malloc C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:98  

#1 0x7ffc36355ee2 in operator new d:\a01\_work\12\s\src\vctools\crt\vcstartup\src\heap\new\_scalar.cpp:35  

#2 0x7ffc35dbebd1 in rx::ContextVk::createBuffer C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\ContextVk.cpp:4879  

#3 0x7ffc356801e6 in gl::Buffer::Buffer C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\Buffer.cpp:47  

#4 0x7ffc357d9363 in gl::BufferManager::AllocateNewObject C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\ResourceManager.cpp:114  

#5 0x7ffc3563bbfb in gl::TypedResourceManager[gl::Buffer,gl::BufferManager,gl::BufferID](javascript:void(0);)::checkObjectAllocationImpl<> C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\ResourceManager.h:117  

#6 0x7ffc356a38a0 in gl::Context::bindBufferRange C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\Context.cpp:6323  

#7 0x7ffc356cf88e in gl::Context::bindBufferBase C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\Context.cpp:6314  

#8 0x7ffc3563e037 in GL\_BindBufferBase C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libGLESv2\entry\_points\_gles\_3\_0\_autogen.cpp:93  

#9 0x7ffc4d4be130 in gpu::gles2::GLES2DecoderPassthroughImpl::DoBindBufferBase C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\gles2\_cmd\_decoder\_passthrough\_doers.cc:409  

#10 0x7ffc4965148b in gpu::gles2::GLES2DecoderPassthroughImpl::DoCommandsImpl<0> C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\gles2\_cmd\_decoder\_passthrough.cc:870  

#11 0x7ffc496508e0 in gpu::gles2::GLES2DecoderPassthroughImpl::DoCommands C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\gles2\_cmd\_decoder\_passthrough.cc:808  

#12 0x7ffc463cbb5f in gpu::CommandBufferService::Flush C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\command\_buffer\_service.cc:70  

#13 0x7ffc436b61d8 in gpu::CommandBufferStub::OnAsyncFlush C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command\_buffer\_stub.cc:500  

#14 0x7ffc436b53b2 in gpu::CommandBufferStub::ExecuteDeferredRequest C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command\_buffer\_stub.cc:152  

#15 0x7ffc436c1da3 in gpu::GpuChannel::ExecuteDeferredRequest C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\gpu\_channel.cc:705  

#16 0x7ffc436cd399 in base::internal::Invoker<base::internal::BindState<void (gpu::GpuChannel::\*)(mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);)),base::WeakPtr[gpu::GpuChannel](javascript:void(0);),mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);) >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind\_internal.h:748  

#17 0x7ffc432f1824 in gpu::Scheduler::RunNextTask C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\scheduler.cc:691  

#18 0x7ffc41e83d94 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:135  

#19 0x7ffc44d2a055 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:386  

#20 0x7ffc44d29629 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:291  

#21 0x7ffc44d0664a in base::MessagePumpDefault::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_default.cc:39  

#22 0x7ffc44d2b810 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:498  

#23 0x7ffc41df6377 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:141  

#24 0x7ffc446007ae in content::GpuMain C:\b\s\w\ir\cache\builder\src\content\gpu\gpu\_main.cc:405  

#25 0x7ffc41a21aeb in content::RunOtherNamedProcessTypeMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:701  

#26 0x7ffc41a23727 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1040  

#27 0x7ffc41a2011b in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:407

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\vk\_helpers.cpp:1305 in rx::vk::CommandBufferHelperCommon::bufferWrite  

Shadow bytes around the buggy address:  

0x038e9372eb60: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x038e9372eb70: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd  

0x038e9372eb80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x038e9372eb90: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x038e9372eba0: fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa  

=>0x038e9372ebb0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd[fd]fd  

0x038e9372ebc0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x038e9372ebd0: fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa  

0x038e9372ebe0: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd  

0x038e9372ebf0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x038e9372ec00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

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

==11296==ABORTING  

[28224:15020:0426/204102.797:ERROR:gpu\_process\_host.cc(973)] GPU process exited unexpectedly: exit\_code=1

**CREDIT INFORMATION**  

Reporter credit: SeongHwan Park (SeHwa)

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 1.8 KB)

## Timeline

### [Deleted User] (2022-04-26)

[Empty comment from Monorail migration]

### do...@chromium.org (2022-04-27)

+vulkan OWNERs. Do you mind helping me figure out if this is on by default or off by default, and when this UaF might have been first introduced?

[Monorail components: Internals>GPU>ANGLE Internals>GPU>Vulkan]

### jm...@chromium.org (2022-04-27)

[Empty comment from Monorail migration]

[Monorail components: -Internals>GPU>Vulkan]

### jm...@chromium.org (2022-04-27)

[Empty comment from Monorail migration]

### jm...@chromium.org (2022-04-27)

pretty sure this is a duplicate of https://crbug.com/chromium/1317650

### gg...@gmail.com (2022-04-27)

jmadill@ If you don't mind, could you kindly tell me why you think that this is duplicate?

### ad...@google.com (2022-04-27)

(auto-cc on security bug)

### jm...@chromium.org (2022-05-02)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-05-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/84e42c3b04da9e2c9d93d35bb6f2b1830fef22f4

commit 84e42c3b04da9e2c9d93d35bb6f2b1830fef22f4
Author: Jamie Madill <jmadill@chromium.org>
Date: Mon May 02 19:42:23 2022

Fix validation cache when deleting a Transform Feedback.

Bug: chromium:1320024
Change-Id: I76ef85a3c65c663c138d8caebd4ef2c0da53cd4f
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3621780
Commit-Queue: Jamie Madill <jmadill@chromium.org>
Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>
Commit-Queue: Shahbaz Youssefi <syoussefi@chromium.org>

[modify] https://crrev.com/84e42c3b04da9e2c9d93d35bb6f2b1830fef22f4/src/tests/gl_tests/TransformFeedbackTest.cpp
[modify] https://crrev.com/84e42c3b04da9e2c9d93d35bb6f2b1830fef22f4/src/libANGLE/Context.cpp


### gi...@appspot.gserviceaccount.com (2022-05-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/46a7889ae2811f0cbb9c61dbb3abbfdc12368bd4

commit 46a7889ae2811f0cbb9c61dbb3abbfdc12368bd4
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Tue May 03 15:44:58 2022

Roll ANGLE from b5f0fd1bd2a6 to 84e42c3b04da (1 revision)

https://chromium.googlesource.com/angle/angle.git/+log/b5f0fd1bd2a6..84e42c3b04da

2022-05-03 jmadill@chromium.org Fix validation cache when deleting a Transform Feedback.

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/angle-chromium-autoroll
Please CC abdolrashidi@google.com on the revert to ensure that a human
is aware of the problem.

To file a bug in ANGLE: https://bugs.chromium.org/p/angleproject/issues/entry
To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86
Bug: chromium:1320024
Tbr: abdolrashidi@google.com
Change-Id: I43293a75918fc7647d174f233559224fd005d776
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3623397
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#998880}

[modify] https://crrev.com/46a7889ae2811f0cbb9c61dbb3abbfdc12368bd4/DEPS


### me...@google.com (2022-05-04)

jmadill: I tentatively added M100 as the found-in milestone. Could you confirm if this is the case? Thanks.

### [Deleted User] (2022-05-04)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-05)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jm...@chromium.org (2022-05-09)

[Empty comment from Monorail migration]

### jm...@chromium.org (2022-05-09)

meacer: I think this problem goes back to m100 at least.

### [Deleted User] (2022-05-09)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-09)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-09)

Requesting merge to extended stable M100 because latest trunk commit (998880) appears to be after extended stable branch point (972766).

Requesting merge to stable M101 because latest trunk commit (998880) appears to be after stable branch point (982481).

Requesting merge to beta M102 because latest trunk commit (998880) appears to be after beta branch point (992738).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-05-09)

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

### [Deleted User] (2022-05-09)

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
Owners: benmason (Android), harrysouders (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-05-09)

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
Owners: govind (Android), harrysouders (iOS), dgagnon (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-05-14)

M102 merge approved; please merge this fix to branch 5005 NLT EOD Monday, 16 May so this fix can be included in M102 stable cut on Tuesday -- thank you! 

M101/M100 merge n/a as there are no further planned releases of M100 Extended and M101 Stable 

### gi...@appspot.gserviceaccount.com (2022-05-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/6661eb4900dae62cbe9af5023f9c1e7105798b50

commit 6661eb4900dae62cbe9af5023f9c1e7105798b50
Author: Jamie Madill <jmadill@chromium.org>
Date: Mon May 02 19:42:23 2022

[M102] Fix validation cache when deleting a Transform Feedback.

Bug: chromium:1320024
Change-Id: I76ef85a3c65c663c138d8caebd4ef2c0da53cd4f
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3621780
Commit-Queue: Jamie Madill <jmadill@chromium.org>
Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>
Commit-Queue: Shahbaz Youssefi <syoussefi@chromium.org>
(cherry picked from commit 84e42c3b04da9e2c9d93d35bb6f2b1830fef22f4)
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3650697
Reviewed-by: Geoff Lang <geofflang@chromium.org>

[modify] https://crrev.com/6661eb4900dae62cbe9af5023f9c1e7105798b50/src/libANGLE/Context.cpp


### am...@google.com (2022-05-16)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-05-16)

Congratulations on another one, SeongHwan! The VRP Panel has decided to reward you $10,000 for this bug as well. Thank you for your efforts and reporting this issue to us! 

### am...@chromium.org (2022-05-24)

[Empty comment from Monorail migration]

### am...@google.com (2022-05-24)

[Empty comment from Monorail migration]

### am...@google.com (2022-05-24)

[Empty comment from Monorail migration]

### gm...@google.com (2022-06-23)

[Empty comment from Monorail migration]

### rz...@google.com (2022-06-27)

[Empty comment from Monorail migration]

### rz...@google.com (2022-07-07)

[Empty comment from Monorail migration]

### rz...@google.com (2022-07-07)

1. https://crrev.com/c/3749918
2. Low,  no conflicts
3. 102
4. Yes

### gm...@google.com (2022-07-07)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-07-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/42c0cd98edc356dab50f95a7e2e6d1f5635c85f1

commit 42c0cd98edc356dab50f95a7e2e6d1f5635c85f1
Author: Jamie Madill <jmadill@chromium.org>
Date: Mon May 02 19:42:23 2022

[M96-LTS] Fix validation cache when deleting a Transform Feedback.

Bug: chromium:1320024
Change-Id: I76ef85a3c65c663c138d8caebd4ef2c0da53cd4f
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3621780
Commit-Queue: Jamie Madill <jmadill@chromium.org>
Commit-Queue: Shahbaz Youssefi <syoussefi@chromium.org>
(cherry picked from commit 84e42c3b04da9e2c9d93d35bb6f2b1830fef22f4)
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3650697
Reviewed-by: Geoff Lang <geofflang@chromium.org>
(cherry picked from commit 6661eb4900dae62cbe9af5023f9c1e7105798b50)
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3749918
Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>

[modify] https://crrev.com/42c0cd98edc356dab50f95a7e2e6d1f5635c85f1/src/libANGLE/Context.cpp


### rz...@google.com (2022-07-18)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-21)

[Empty comment from Monorail migration]

### am...@google.com (2022-07-27)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-29)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-15)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1320024?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059482)*
