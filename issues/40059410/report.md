# Security: [ANGLE] Heap use-after-free caused by State::detachBuffer

| Field | Value |
|-------|-------|
| **Issue ID** | [40059410](https://issues.chromium.org/issues/40059410) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU>ANGLE |
| **Platforms** | Fuchsia, Linux, Mac, Windows |
| **Reporter** | gg...@gmail.com |
| **Assignee** | jm...@chromium.org |
| **Created** | 2022-04-19 |
| **Bounty** | $10,000.00 |

## Description

**VULNERABILITY DETAILS**  

There is a heap uss-after-free vulnerability that is caused by State::detachBuffer.  

This vulnerability exists in the Vulkan backend.

In commit 708ce9cfd63bc8eab7c48987612a2dedce78c69a, the patch added validation to the ValidateDrawStates function called by drawArrays.  

However, the problem is that the deleteBuffer function does not initialize |mCachedBasicDrawStatesError|.  

**-------------------------** --------------------------------------------------------------  

// Places that can trigger updateBasicDrawStatesError:  

// 1. onVertexArrayBindingChange.  

// 2. onProgramExecutableChange.  

// 3. onVertexArrayBufferContentsChange.  

// 4. onVertexArrayStateChange.  

// 5. onVertexArrayBufferStateChange.  

// 6. onDrawFramebufferChange.  

// 7. onContextCapChange.  

// 8. onStencilStateChange.  

// 9. onDefaultVertexAttributeChange.  

// 10. onActiveTextureChange.  

// 11. onQueryChange.  

// 12. onActiveTransformFeedbackChange.  

// 13. onUniformBufferStateChange.  

// 14. onColorMaskChange.  

// 15. onBufferBindingChange.  

// 16. onBlendFuncIndexedChange.  

**-------------------------** --------------------------------------------------------------

If deleteBuffer function remove transform\_feedback\_buffer, onActiveTransformFeedbackChange(12th above) should be called.  

**-------------------------** --------------------------------------------------------------  

angle::Result State::detachBuffer(Context \*context, const Buffer \*buffer)  

{  

BufferID bufferID = buffer->id();  

for (gl::BufferBinding target : angle::AllEnums<BufferBinding>())  

{  

if (mBoundBuffers[target].id() == bufferID)  

{  

UpdateBufferBinding(context, &mBoundBuffers[target], nullptr, target);  

}  

}

```
TransformFeedback \*curTransformFeedback = getCurrentTransformFeedback();  
if (curTransformFeedback)  
{  
    ANGLE_TRY(curTransformFeedback->detachBuffer(context, bufferID));  
    if (isTransformFeedbackActiveUnpaused())                                     <-- false  
    {  
        context->getStateCache().onActiveTransformFeedbackChange(context);  
    }  
}  

```

**-------------------------** --------------------------------------------------------------

However, if the current TransformFeedback was paused, the conditional statement in the above code becomes false and the onActiveTransformFeedbackChange function is not called.  

So getBasicDrawStatesErrorImpl is not called in getBasicDrawStatesError. As a result, the ValidateDrawStates function is never called.  

**-------------------------** --------------------------------------------------------------  

intptr\_t getBasicDrawStatesError(const Context \*context) const  

{  

if (mCachedBasicDrawStatesError != kInvalidPointer)  

{  

return mCachedBasicDrawStatesError;  

}

```
    return getBasicDrawStatesErrorImpl(context);  
}  

```

**-------------------------** --------------------------------------------------------------

**VERSION**  

Chrome Version: master (and tested on 100.0.4896.127 (Official Build) (64-bit) Stable)  

Operating System: Windows/Linux (vulkan)

**REPRODUCTION CASE**  

Run the attached poc.html on Vulkan backend (--use-angle=vulkan) (not swiftshader)

# **FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION** Type of crash: GPU Process Crash State:

==22584==ERROR: AddressSanitizer: heap-use-after-free on address 0x11af643c3bb0 at pc 0x7ffaeb39f345 bp 0x0010a6dfe200 sp 0x0010a6dfe248  

READ of size 8 at 0x11af643c3bb0 thread T0  

==22584==WARNING: Failed to use and restart external symbolizer!  

==22584==\*\*\* WARNING: Failed to initialize DbgHelp! \*\*\*  

==22584==\*\*\* Most likely this means that the app is already \*\*\*  

==22584==\*\*\* using DbgHelp, possibly with incompatible flags. \*\*\*  

==22584==\*\*\* Due to technical reasons, symbolization might crash \*\*\*  

==22584==\*\*\* or produce wrong results. \*\*\*  

#0 0x7ffaeb39f344 in rx::vk::CommandBufferHelperCommon::bufferWrite C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\vk\_helpers.cpp:1305  

#1 0x7ffaeb22a2c7 in rx::ContextVk::handleDirtyGraphicsTransformFeedbackBuffersExtension C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\ContextVk.cpp:2314  

#2 0x7ffaeb232442 in rx::ContextVk::setupDraw C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\ContextVk.cpp:1253  

#3 0x7ffaeb23e4b1 in rx::ContextVk::drawArrays C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\ContextVk.cpp:3065  

#4 0x7ffaeaac1b52 in GL\_DrawArrays C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libGLESv2\entry\_points\_gles\_2\_0\_autogen.cpp:1109  

#5 0x7ffab95c8bc2 in gpu::gles2::GLES2DecoderPassthroughImpl::DoDrawArrays C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\gles2\_cmd\_decoder\_passthrough\_doers.cc:1217  

#6 0x7ffab5831aab in gpu::gles2::GLES2DecoderPassthroughImpl::DoCommandsImpl<0> C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\gles2\_cmd\_decoder\_passthrough.cc:870  

#7 0x7ffab5830f00 in gpu::gles2::GLES2DecoderPassthroughImpl::DoCommands C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\gles2\_cmd\_decoder\_passthrough.cc:808  

#8 0x7ffab25d3c63 in gpu::CommandBufferService::Flush C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\command\_buffer\_service.cc:70  

#9 0x7ffaaf8e2bbc in gpu::CommandBufferStub::OnAsyncFlush C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command\_buffer\_stub.cc:500  

#10 0x7ffaaf8e1d96 in gpu::CommandBufferStub::ExecuteDeferredRequest C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command\_buffer\_stub.cc:152  

#11 0x7ffaaf8ee787 in gpu::GpuChannel::ExecuteDeferredRequest C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\gpu\_channel.cc:670  

#12 0x7ffaaf8f96cf in base::internal::Invoker<base::internal::BindState<void (gpu::GpuChannel::\*)(mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);)),base::WeakPtr[gpu::GpuChannel](javascript:void(0);),mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);) >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind\_internal.h:748  

#13 0x7ffaaf525f5c in gpu::Scheduler::RunNextTask C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\scheduler.cc:691  

#14 0x7ffaae06a364 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:135  

#15 0x7ffab0f33205 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:386  

#16 0x7ffab0f327d9 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:291  

#17 0x7ffab0f0f7fa in base::MessagePumpDefault::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_default.cc:39  

#18 0x7ffab0f349c0 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:498  

#19 0x7ffaadfe65d7 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:141  

#20 0x7ffab081a45e in content::GpuMain C:\b\s\w\ir\cache\builder\src\content\gpu\gpu\_main.cc:405  

#21 0x7ffaadc12cab in content::RunOtherNamedProcessTypeMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:682  

#22 0x7ffaadc148e7 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1021  

#23 0x7ffaadc112db in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:407  

#24 0x7ffaadc11a64 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:435  

#25 0x7ffaa29614ca in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc:176  

#26 0x7ff635b35b16 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main\_dll\_loader\_win.cc:167  

#27 0x7ff635b32b5f in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_exe\_main\_win.cc:382  

#28 0x7ff635f2fafb in \_\_scrt\_common\_main\_seh d:\a01\_work\12\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#29 0x7ffb54ed7033 in BaseThreadInitThunk+0x13 (C:\WINDOWS\System32\KERNEL32.DLL+0x180017033)  

#30 0x7ffb55c22650 in RtlUserThreadStart+0x20 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x180052650)

0x11af643c3bb0 is located 112 bytes inside of 312-byte region [0x11af643c3b40,0x11af643c3c78)  

freed by thread T0 here:  

#0 0x7ff635bde82b in free C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:82  

#1 0x7ffaeb20ae5f in rx::BufferVk::~BufferVk C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\BufferVk.cpp:238  

#2 0x7ffaeab104ce in gl::Buffer::~Buffer C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\Buffer.cpp:55  

#3 0x7ffaeab11eaf in gl::Buffer::~Buffer C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\Buffer.cpp:54  

#4 0x7ffaeac69973 in gl::TypedResourceManager[gl::Sampler,gl::SamplerManager,gl::SamplerID](javascript:void(0);)::deleteObject C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\ResourceManager.cpp:96  

#5 0x7ffaeab644a9 in gl::Context::deleteBuffers C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\Context.cpp:6786  

#6 0x7ffaeaac0897 in GL\_DeleteBuffers C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libGLESv2\entry\_points\_gles\_2\_0\_autogen.cpp:819  

#7 0x7ffab95c5dd5 in gpu::gles2::GLES2DecoderPassthroughImpl::DoDeleteBuffers C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\gles2\_cmd\_decoder\_passthrough\_doers.cc:1012  

#8 0x7ffab5831aab in gpu::gles2::GLES2DecoderPassthroughImpl::DoCommandsImpl<0> C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\gles2\_cmd\_decoder\_passthrough.cc:870  

#9 0x7ffab5830f00 in gpu::gles2::GLES2DecoderPassthroughImpl::DoCommands C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\gles2\_cmd\_decoder\_passthrough.cc:808  

#10 0x7ffab25d3c63 in gpu::CommandBufferService::Flush C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\command\_buffer\_service.cc:70  

#11 0x7ffaaf8e2bbc in gpu::CommandBufferStub::OnAsyncFlush C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command\_buffer\_stub.cc:500  

#12 0x7ffaaf8e1d96 in gpu::CommandBufferStub::ExecuteDeferredRequest C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command\_buffer\_stub.cc:152  

#13 0x7ffaaf8ee787 in gpu::GpuChannel::ExecuteDeferredRequest C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\gpu\_channel.cc:670  

#14 0x7ffaaf8f96cf in base::internal::Invoker<base::internal::BindState<void (gpu::GpuChannel::\*)(mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);)),base::WeakPtr[gpu::GpuChannel](javascript:void(0);),mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);) >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind\_internal.h:748  

#15 0x7ffaaf525f5c in gpu::Scheduler::RunNextTask C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\scheduler.cc:691  

#16 0x7ffaae06a364 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:135  

#17 0x7ffab0f33205 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:386  

#18 0x7ffab0f327d9 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:291  

#19 0x7ffab0f0f7fa in base::MessagePumpDefault::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_default.cc:39  

#20 0x7ffab0f349c0 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:498  

#21 0x7ffaadfe65d7 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:141  

#22 0x7ffab081a45e in content::GpuMain C:\b\s\w\ir\cache\builder\src\content\gpu\gpu\_main.cc:405  

#23 0x7ffaadc12cab in content::RunOtherNamedProcessTypeMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:682  

#24 0x7ffaadc148e7 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1021  

#25 0x7ffaadc112db in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:407  

#26 0x7ffaadc11a64 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:435  

#27 0x7ffaa29614ca in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc:176

previously allocated by thread T0 here:  

#0 0x7ff635bde92b in malloc C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:98  

#1 0x7ffaeb7e24e6 in operator new d:\a01\_work\12\s\src\vctools\crt\vcstartup\src\heap\new\_scalar.cpp:35  

#2 0x7ffaeb24fded in rx::ContextVk::createBuffer C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\ContextVk.cpp:4868  

#3 0x7ffaeab10236 in gl::Buffer::Buffer C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\Buffer.cpp:47  

#4 0x7ffaeac6b2e3 in gl::BufferManager::AllocateNewObject C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\ResourceManager.cpp:114  

#5 0x7ffaeaacbc17 in gl::TypedResourceManager[gl::Buffer,gl::BufferManager,gl::BufferID](javascript:void(0);)::checkObjectAllocationImpl<> C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\ResourceManager.h:117  

#6 0x7ffaeab3393c in gl::Context::bindBufferRange C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\Context.cpp:6283  

#7 0x7ffaeab5f57e in gl::Context::bindBufferBase C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\Context.cpp:6274  

#8 0x7ffaeaace053 in GL\_BindBufferBase C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libGLESv2\entry\_points\_gles\_3\_0\_autogen.cpp:93  

#9 0x7ffab95c1320 in gpu::gles2::GLES2DecoderPassthroughImpl::DoBindBufferBase C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\gles2\_cmd\_decoder\_passthrough\_doers.cc:409  

#10 0x7ffab5831aab in gpu::gles2::GLES2DecoderPassthroughImpl::DoCommandsImpl<0> C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\gles2\_cmd\_decoder\_passthrough.cc:870  

#11 0x7ffab5830f00 in gpu::gles2::GLES2DecoderPassthroughImpl::DoCommands C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\gles2\_cmd\_decoder\_passthrough.cc:808  

#12 0x7ffab25d3c63 in gpu::CommandBufferService::Flush C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\command\_buffer\_service.cc:70  

#13 0x7ffaaf8e2bbc in gpu::CommandBufferStub::OnAsyncFlush C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command\_buffer\_stub.cc:500  

#14 0x7ffaaf8e1d96 in gpu::CommandBufferStub::ExecuteDeferredRequest C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command\_buffer\_stub.cc:152  

#15 0x7ffaaf8ee787 in gpu::GpuChannel::ExecuteDeferredRequest C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\gpu\_channel.cc:670  

#16 0x7ffaaf8f96cf in base::internal::Invoker<base::internal::BindState<void (gpu::GpuChannel::\*)(mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);)),base::WeakPtr[gpu::GpuChannel](javascript:void(0);),mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);) >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind\_internal.h:748  

#17 0x7ffaaf525f5c in gpu::Scheduler::RunNextTask C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\scheduler.cc:691  

#18 0x7ffaae06a364 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:135  

#19 0x7ffab0f33205 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:386  

#20 0x7ffab0f327d9 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:291  

#21 0x7ffab0f0f7fa in base::MessagePumpDefault::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_default.cc:39  

#22 0x7ffab0f349c0 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:498  

#23 0x7ffaadfe65d7 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:141  

#24 0x7ffab081a45e in content::GpuMain C:\b\s\w\ir\cache\builder\src\content\gpu\gpu\_main.cc:405  

#25 0x7ffaadc12cab in content::RunOtherNamedProcessTypeMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:682  

#26 0x7ffaadc148e7 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1021  

#27 0x7ffaadc112db in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:407

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\vk\_helpers.cpp:1305 in rx::vk::CommandBufferHelperCommon::bufferWrite  

Shadow bytes around the buggy address:  

0x03c1509f8720: fd fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa  

0x03c1509f8730: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd  

0x03c1509f8740: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x03c1509f8750: fd fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa  

0x03c1509f8760: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd  

=>0x03c1509f8770: fd fd fd fd fd fd[fd]fd fd fd fd fd fd fd fd fd  

0x03c1509f8780: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fa  

0x03c1509f8790: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd  

0x03c1509f87a0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x03c1509f87b0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x03c1509f87c0: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd  

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

==22584==ABORTING  

[30536:18252:0419/171849.710:ERROR:gpu\_process\_host.cc(973)] GPU process exited unexpectedly: exit\_code=1

**CREDIT INFORMATION**  

Reporter credit: SeongHwan Park (SeHwa)

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 1.6 KB)

## Timeline

### [Deleted User] (2022-04-19)

[Empty comment from Monorail migration]

### ts...@chromium.org (2022-04-19)

Assigning per author of referenced CL.
Impact stable per reported version 100.0.4896.127

[Monorail components: Internals>GPU>ANGLE]

### ad...@google.com (2022-04-19)

(auto-cc on security bug)

### [Deleted User] (2022-04-20)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-04-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/4efc4ee6830a8a53a0daf9daa3c7aa835db4220f

commit 4efc4ee6830a8a53a0daf9daa3c7aa835db4220f
Author: Jamie Madill <jmadill@chromium.org>
Date: Tue Apr 19 21:01:20 2022

Fix validate state cache after XFB buffer deleted.

Bug: chromium:1317650
Change-Id: Iec9f1167c3b2957091dd0f4ef3efcfcd7c4bf3c0
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3594250
Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>
Auto-Submit: Jamie Madill <jmadill@chromium.org>
Commit-Queue: Jamie Madill <jmadill@chromium.org>

[modify] https://crrev.com/4efc4ee6830a8a53a0daf9daa3c7aa835db4220f/src/tests/gl_tests/TransformFeedbackTest.cpp
[modify] https://crrev.com/4efc4ee6830a8a53a0daf9daa3c7aa835db4220f/src/libANGLE/State.cpp
[modify] https://crrev.com/4efc4ee6830a8a53a0daf9daa3c7aa835db4220f/src/tests/angle_end2end_tests_expectations.txt


### ts...@chromium.org (2022-04-21)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-21)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-22)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-04-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/c82d1e276ce17ad9c258e4dad0da07c21c623b70

commit c82d1e276ce17ad9c258e4dad0da07c21c623b70
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Fri Apr 22 22:00:20 2022

Roll ANGLE from 5610ab64237a to e6fc5e62c52d (32 revisions)

https://chromium.googlesource.com/angle/angle.git/+log/5610ab64237a..e6fc5e62c52d

2022-04-22 romanl@google.com Use _FindAdb (cached) directly instead of Adb wrapper.
2022-04-22 romanl@google.com Switch py_utils import to pathlib.
2022-04-22 ianelliott@google.com Suppress VVL UNASSIGNED-BestPractices-SemaphoreCount
2022-04-22 jmadill@chromium.org Revert "Vulkan: Cache ImageView serials on texture changes."
2022-04-22 cclao@google.com Vulkan: Add feature avoid HOST_VISIBLE and DEVICE_LOCAL combination
2022-04-22 romanl@google.com Fall back to adb on PATH if platform-tools not present.
2022-04-22 jmadill@chromium.org Track Surface color & depth/stencil init separately.
2022-04-22 angle-autoroll@skia-public.iam.gserviceaccount.com Roll Chromium from 408793418c48 to 192db13f8509 (548 revisions)
2022-04-21 ianelliott@google.com Revert "CGL, MTL: pbuffer for IOSurface fails for some formats"
2022-04-21 jmadill@chromium.org Vulkan: Update glslang wrapper TODO.
2022-04-21 jmadill@chromium.org Revert "Re-land: "Vulkan: Support Wayland""
2022-04-21 jmadill@chromium.org Expand Vulkan end2end_test skip.
2022-04-21 sugoi@google.com Disable MSAN in the Vulkan loader
2022-04-21 jmadill@chromium.org Android: Add //build to blueprint.
2022-04-21 Guoxing.Wu@arm.com Vulkan: use "undefined" for layerProvokingVertex
2022-04-21 angle-autoroll@skia-public.iam.gserviceaccount.com Roll SwiftShader from ea5f37f39193 to 71f3089b729c (5 revisions)
2022-04-21 angle-autoroll@skia-public.iam.gserviceaccount.com Roll Chromium from a434f1de2483 to 408793418c48 (456 revisions)
2022-04-21 lexa.knyazev@gmail.com Avoid IOError in capture_replay_tests.py
2022-04-21 steven@valvesoftware.com EGL: allow eglQueryString(EGL_NO_DISPLAY, EGL_VERSION)
2022-04-21 syoussefi@chromium.org Add a test for backwards mip generation with draw
2022-04-20 cclao@google.com Vulkan: Remove BufferVk::mHasBeenReferencedByGPU
2022-04-20 senorblanco@chromium.org D3D: unsuppress some now-passing tests.
2022-04-20 abdolrashidi@google.com Vulkan: Add perf test for MSAA swapchain resolve
2022-04-20 syoussefi@chromium.org Vulkan: Fix surface invalidate w.r.t shared present mode
2022-04-20 cnorthrop@google.com Tests: Add Free Fire Max trace
2022-04-20 jmadill@chromium.org Vulkan: Cache ImageView serials on texture changes.
2022-04-20 romanl@google.com Use adb directly (instead of catapult) in gold tests.
2022-04-20 jmadill@chromium.org Fix validate state cache after XFB buffer deleted.
2022-04-20 gman@chromium.org Metal:Clear Backbuffer when Robust Resource Init enabled
2022-04-20 kkinnunen@apple.com CGL, MTL: pbuffer for IOSurface fails for some formats
2022-04-20 jmadill@chromium.org Vulkan: Renaming "ShaderBuffers" to "ShaderResources".
2022-04-20 antonio.caggiano@collabora.com Re-land: "Vulkan: Support Wayland"

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/angle-chromium-autoroll
Please CC ianelliott@google.com on the revert to ensure that a human
is aware of the problem.

To file a bug in ANGLE: https://bugs.chromium.org/p/angleproject/issues/entry
To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86
Bug: chromium:1313907,chromium:1317650
Tbr: ianelliott@google.com
Test: Test: angle_perftests --gtest_filter="*free_fire_max*"
Change-Id: I01977fc48309dfb2bf59ffe3102e537495c01254
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3603281
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#995378}

[modify] https://crrev.com/c82d1e276ce17ad9c258e4dad0da07c21c623b70/DEPS


### jm...@chromium.org (2022-04-25)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-25)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-25)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-25)

Requesting merge to stable M100 because latest trunk commit (995378) appears to be after stable branch point (972766).

Requesting merge to beta M101 because latest trunk commit (995378) appears to be after beta branch point (982481).

Requesting merge to dev M102 because latest trunk commit (995378) appears to be after dev branch point (992738).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-04-25)

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

### [Deleted User] (2022-04-25)

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

### [Deleted User] (2022-04-25)

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

### jm...@chromium.org (2022-04-25)

1. use-after-free
2. https://chromium-review.googlesource.com/c/angle/angle/+/3594250
3. yes
4. no

### jm...@chromium.org (2022-04-25)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-04-27)

Thanks for this landing this fix so quickly, Jamie; merges approved, please merge this fix to the following branches at your earliest convenience 
m102 merge approved - please merge to branch 5005
m101 merge approved - please merge to branch 4951
m100 merge approved - please merge to branch 4896 

### [Deleted User] (2022-05-02)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-05-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/f2280c0c5f935dccbaf528343d474c8fcdebe63a

commit f2280c0c5f935dccbaf528343d474c8fcdebe63a
Author: Jamie Madill <jmadill@chromium.org>
Date: Tue Apr 19 21:01:20 2022

[M102] Fix validate state cache after XFB buffer deleted.

Bug: chromium:1317650
Change-Id: Iec9f1167c3b2957091dd0f4ef3efcfcd7c4bf3c0
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3594250
Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>
Auto-Submit: Jamie Madill <jmadill@chromium.org>
Commit-Queue: Jamie Madill <jmadill@chromium.org>
(cherry picked from commit 4efc4ee6830a8a53a0daf9daa3c7aa835db4220f)
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3621777
Reviewed-by: Amirali Abdolrashidi <abdolrashidi@google.com>

[modify] https://crrev.com/f2280c0c5f935dccbaf528343d474c8fcdebe63a/src/libANGLE/State.cpp


### gi...@appspot.gserviceaccount.com (2022-05-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/4718e8197a83458d5948a7c2984972da114f1d28

commit 4718e8197a83458d5948a7c2984972da114f1d28
Author: Jamie Madill <jmadill@chromium.org>
Date: Tue Apr 19 21:01:20 2022

[M101] Fix validate state cache after XFB buffer deleted.

Bug: chromium:1317650
Change-Id: Iec9f1167c3b2957091dd0f4ef3efcfcd7c4bf3c0
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3594250
Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>
Auto-Submit: Jamie Madill <jmadill@chromium.org>
Commit-Queue: Jamie Madill <jmadill@chromium.org>
(cherry picked from commit 4efc4ee6830a8a53a0daf9daa3c7aa835db4220f)
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3621778
Reviewed-by: Amirali Abdolrashidi <abdolrashidi@google.com>

[modify] https://crrev.com/4718e8197a83458d5948a7c2984972da114f1d28/src/libANGLE/State.cpp


### gi...@appspot.gserviceaccount.com (2022-05-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/a602a068e022149691d8642b095b8e68d05feb77

commit a602a068e022149691d8642b095b8e68d05feb77
Author: Jamie Madill <jmadill@chromium.org>
Date: Tue Apr 19 21:01:20 2022

[M100] Fix validate state cache after XFB buffer deleted.

Bug: chromium:1317650
Change-Id: Iec9f1167c3b2957091dd0f4ef3efcfcd7c4bf3c0
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3594250
Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>
Auto-Submit: Jamie Madill <jmadill@chromium.org>
Commit-Queue: Jamie Madill <jmadill@chromium.org>
(cherry picked from commit 4efc4ee6830a8a53a0daf9daa3c7aa835db4220f)
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3621779
Reviewed-by: Amirali Abdolrashidi <abdolrashidi@google.com>

[modify] https://crrev.com/a602a068e022149691d8642b095b8e68d05feb77/src/libANGLE/State.cpp


### gi...@appspot.gserviceaccount.com (2022-05-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/4718e8197a83458d5948a7c2984972da114f1d28

commit 4718e8197a83458d5948a7c2984972da114f1d28
Author: Jamie Madill <jmadill@chromium.org>
Date: Tue Apr 19 21:01:20 2022

[M101] Fix validate state cache after XFB buffer deleted.

Bug: chromium:1317650
Change-Id: Iec9f1167c3b2957091dd0f4ef3efcfcd7c4bf3c0
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3594250
Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>
Auto-Submit: Jamie Madill <jmadill@chromium.org>
Commit-Queue: Jamie Madill <jmadill@chromium.org>
(cherry picked from commit 4efc4ee6830a8a53a0daf9daa3c7aa835db4220f)
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3621778
Reviewed-by: Amirali Abdolrashidi <abdolrashidi@google.com>

[modify] https://crrev.com/4718e8197a83458d5948a7c2984972da114f1d28/src/libANGLE/State.cpp


### am...@chromium.org (2022-05-09)

[Empty comment from Monorail migration]

### am...@google.com (2022-05-09)

[Empty comment from Monorail migration]

### am...@google.com (2022-05-16)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-05-16)

Congratulations, SeongHwan! The VRP Panel has decided to award you $10,000 for this report. Thank you for your efforts in discovering GPU bugs and in providing this high quality report to us! 

### am...@google.com (2022-05-24)

[Empty comment from Monorail migration]

### am...@google.com (2022-07-26)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-29)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1317650?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059410)*
