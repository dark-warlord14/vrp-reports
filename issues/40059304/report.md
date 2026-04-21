# Security: [ANGLE] Heap use-after-free in ContextVk::onBeginTransformFeedback

| Field | Value |
|-------|-------|
| **Issue ID** | [40059304](https://issues.chromium.org/issues/40059304) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU>Vulkan |
| **Platforms** | Linux, Mac, Windows |
| **Reporter** | gg...@gmail.com |
| **Assignee** | jm...@chromium.org |
| **Created** | 2022-04-06 |
| **Bounty** | $10,000.00 |

## Description

**VULNERABILITY DETAILS**  

There is a heap uss-after-free vulnerability that is caused by the ContextVk::onBeginTransformFeedback function.  

This vulnerability exists in the Vulkan backend.

When glBeginTransformFeedback() is called, the TransformFeedbackVk::begin function calls initializeXFBBuffersDesc.  

**-------------------------** --------------------------------------------------------------  

void TransformFeedbackVk::initializeXFBBuffersDesc(ContextVk \*contextVk, size\_t xfbBufferCount)  

{  

mXFBBuffersDesc.reset();  

for (size\_t bufferIndex = 0; bufferIndex < xfbBufferCount; ++bufferIndex)  

{  

const gl::OffsetBindingPointer[gl::Buffer](javascript:void(0);) &binding = mState.getIndexedBuffer(bufferIndex);  

ASSERT(binding.get());

```
    BufferVk \*bufferVk = vk::GetImpl(binding.get());  

    if (bufferVk->isBufferValid())  
    {  
        mBufferHelpers[bufferIndex] = &bufferVk->getBuffer();  
        mBufferOffsets[bufferIndex] =  
            binding.getOffset() + mBufferHelpers[bufferIndex]->getOffset();  
        mBufferSizes[bufferIndex] = gl::GetBoundBufferAvailableSize(binding);  
        mBufferObserverBindings[bufferIndex].bind(bufferVk);  
    }  

```

**-------------------------** --------------------------------------------------------------

|mBufferHelpers| has a buffer bound to GL\_TRANSFORM\_FEEDBACK\_BUFFER. This buffer can be freed by glDeleteBuffer().  

And in the glResumeTransformFeedback() function, the ContextVk::onBeginTransformFeedback function is called with the |mBufferHelpers| argument.  

**-------------------------** --------------------------------------------------------------  

angle::Result TransformFeedbackVk::resume(const gl::Context \*context)  

{  

....

```
return contextVk->onBeginTransformFeedback(xfbBufferCount, mBufferHelpers,  
                                           mCounterBufferHelpers);  

```

}  

**-------------------------** --------------------------------------------------------------

And in onBeginTransformFeedback, it uses the already freed buffer without any validation.  

**-------------------------** --------------------------------------------------------------  

angle::Result ContextVk::onBeginTransformFeedback(  

size\_t bufferCount,  

const gl::TransformFeedbackBuffersArray<vk::BufferHelper \*> &buffers,  

const gl::TransformFeedbackBuffersArray[vk::BufferHelper](javascript:void(0);) &counterBuffers)  

{  

onTransformFeedbackStateChanged();

```
bool shouldEndRenderPass = false;  

// If any of the buffers were previously used in the render pass, break the render pass as a  
// barrier is needed.  
for (size_t bufferIndex = 0; bufferIndex < bufferCount; ++bufferIndex)  
{  
    const vk::BufferHelper \*buffer = buffers[bufferIndex];                  <--- can be freed  
    if (mRenderPassCommands->usesBuffer(\*buffer))  
    {  
        shouldEndRenderPass = true;  
        break;  
    }  
}  

```

**-------------------------** --------------------------------------------------------------

This vulnerability causes a simple crash in Swiftshader.  

**-------------------------** --------------------------------------------------------------  

angle::Result TransformFeedbackVk::resume(const gl::Context \*context)  

{  

ContextVk \*contextVk = vk::GetImpl(context);  

const gl::ProgramExecutable \*executable = contextVk->getState().getProgramExecutable();  

ASSERT(executable);  

size\_t xfbBufferCount = executable->getTransformFeedbackBufferCount();

```
if (contextVk->getFeatures().emulateTransformFeedback.enabled)  
{  
    initializeXFBBuffersDesc(contextVk, xfbBufferCount);  
}  

return contextVk->onBeginTransformFeedback(xfbBufferCount, mBufferHelpers,  
                                           mCounterBufferHelpers);  

```

}  

**-------------------------** --------------------------------------------------------------

On platforms without VK\_EXT\_transform\_feedback(including Swiftshader), emulateTransformFeedback.enabled is true.  

Therefore, the initializeXFBBuffersDesc function is called.  

**-------------------------** --------------------------------------------------------------  

void TransformFeedbackVk::initializeXFBBuffersDesc(ContextVk \*contextVk, size\_t xfbBufferCount)  

{  

mXFBBuffersDesc.reset();  

for (size\_t bufferIndex = 0; bufferIndex < xfbBufferCount; ++bufferIndex)  

{  

const gl::OffsetBindingPointer[gl::Buffer](javascript:void(0);) &binding = mState.getIndexedBuffer(bufferIndex);  

ASSERT(binding.get());

```
    BufferVk \*bufferVk = vk::GetImpl(binding.get());  

```

**-------------------------** --------------------------------------------------------------

However, buffer has already been detached. So the GetImpl function crashes.  

If ASSERT is enabled(is\_debug = true), Chrome will output an Assert failed error message.

**VERSION**  

Chrome Version: master (and tested on 100.0.4896.75 (Official Build) (64-bit) Stable)  

Operating System: Linux (vulkan)

**REPRODUCTION CASE**  

Run the attached poc.html on Vulkan backend (--use-angle=vulkan) (not swiftshader)

# **FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION** Type of crash: GPU Process Crash State:

==6788==ERROR: AddressSanitizer: heap-use-after-free on address 0x1205380bf774 at pc 0x7ffa987bc62f bp 0x00ac4fdfe340 sp 0x00ac4fdfe388  

READ of size 4 at 0x1205380bf774 thread T0  

==6788==WARNING: Failed to use and restart external symbolizer!  

==6788==\*\*\* WARNING: Failed to initialize DbgHelp! \*\*\*  

==6788==\*\*\* Most likely this means that the app is already \*\*\*  

==6788==\*\*\* using DbgHelp, possibly with incompatible flags. \*\*\*  

==6788==\*\*\* Due to technical reasons, symbolization might crash \*\*\*  

==6788==\*\*\* or produce wrong results. \*\*\*  

#0 0x7ffa987bc62e in rx::vk::CommandBufferHelperCommon::usesBuffer C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\vk\_helpers.cpp:1330  

#1 0x7ffa9866fc24 in rx::ContextVk::onBeginTransformFeedback C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\ContextVk.cpp:5096  

#2 0x7ffa980d2239 in gl::TransformFeedback::resume C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\TransformFeedback.cpp:197  

#3 0x7ffa97f8bfb1 in gl::Context::resumeTransformFeedback C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\Context.cpp:7839  

#4 0x7ffa97ef42d8 in GL\_ResumeTransformFeedback C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libGLESv2\entry\_points\_gles\_3\_0\_autogen.cpp:2127  

#5 0x7ffaafbc3f96 in gpu::gles2::GLES2DecoderPassthroughImpl::DoResumeTransformFeedback C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\gles2\_cmd\_decoder\_passthrough\_doers.cc:2581  

#6 0x7ffaabf697fb in gpu::gles2::GLES2DecoderPassthroughImpl::DoCommandsImpl<0> C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\gles2\_cmd\_decoder\_passthrough.cc:870  

#7 0x7ffaabf68c50 in gpu::gles2::GLES2DecoderPassthroughImpl::DoCommands C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\gles2\_cmd\_decoder\_passthrough.cc:808  

#8 0x7ffaa8d6804b in gpu::CommandBufferService::Flush C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\command\_buffer\_service.cc:70  

#9 0x7ffaa609af6c in gpu::CommandBufferStub::OnAsyncFlush C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command\_buffer\_stub.cc:500  

#10 0x7ffaa609a146 in gpu::CommandBufferStub::ExecuteDeferredRequest C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command\_buffer\_stub.cc:152  

#11 0x7ffaa60a6b37 in gpu::GpuChannel::ExecuteDeferredRequest C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\gpu\_channel.cc:670  

#12 0x7ffaa60b199f in base::internal::Invoker<base::internal::BindState<void (gpu::GpuChannel::\*)(mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);)),base::WeakPtr[gpu::GpuChannel](javascript:void(0);),mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);) >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind\_internal.h:748  

#13 0x7ffaa5cdfc6c in gpu::Scheduler::RunNextTask C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\scheduler.cc:691  

#14 0x7ffaa4820714 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:135  

#15 0x7ffaa76c3215 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:386  

#16 0x7ffaa76c2809 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:291  

#17 0x7ffaa769f8aa in base::MessagePumpDefault::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_default.cc:39  

#18 0x7ffaa76c4980 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:498  

#19 0x7ffaa479b2b3 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:141  

#20 0x7ffaa6fce29e in content::GpuMain C:\b\s\w\ir\cache\builder\src\content\gpu\gpu\_main.cc:405  

#21 0x7ffaa43ca48b in content::RunOtherNamedProcessTypeMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:682  

#22 0x7ffaa43cc0c7 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1021  

#23 0x7ffaa43c8abb in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:407  

#24 0x7ffaa43c9244 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:435  

#25 0x7ffa992514ca in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc:176  

#26 0x7ff7b0595b16 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main\_dll\_loader\_win.cc:167  

#27 0x7ff7b0592b5f in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_exe\_main\_win.cc:382  

#28 0x7ff7b098f87b in \_\_scrt\_common\_main\_seh d:\a01\_work\12\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#29 0x7ffb54ed7033 in BaseThreadInitThunk+0x13 (C:\WINDOWS\System32\KERNEL32.DLL+0x180017033)  

#30 0x7ffb55c22650 in RtlUserThreadStart+0x20 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x180052650)

0x1205380bf774 is located 180 bytes inside of 312-byte region [0x1205380bf6c0,0x1205380bf7f8)  

freed by thread T0 here:  

#0 0x7ff7b063e8cb in free C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:82  

#1 0x7ffa98628c89 in rx::BufferVk::~BufferVk C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\BufferVk.cpp:238  

#2 0x7ffa97f304e2 in gl::Buffer::~Buffer C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\Buffer.cpp:55  

#3 0x7ffa97f31ec3 in gl::Buffer::~Buffer C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\Buffer.cpp:54  

#4 0x7ffa98089833 in gl::TypedResourceManager[gl::Sampler,gl::SamplerManager,gl::SamplerID](javascript:void(0);)::deleteObject C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\ResourceManager.cpp:96  

#5 0x7ffa97f844bd in gl::Context::deleteBuffers C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\Context.cpp:6786  

#6 0x7ffa97ee0897 in GL\_DeleteBuffers C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libGLESv2\entry\_points\_gles\_2\_0\_autogen.cpp:819  

#7 0x7ffaafbb2d85 in gpu::gles2::GLES2DecoderPassthroughImpl::DoDeleteBuffers C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\gles2\_cmd\_decoder\_passthrough\_doers.cc:1012  

#8 0x7ffaabf697fb in gpu::gles2::GLES2DecoderPassthroughImpl::DoCommandsImpl<0> C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\gles2\_cmd\_decoder\_passthrough.cc:870  

#9 0x7ffaabf68c50 in gpu::gles2::GLES2DecoderPassthroughImpl::DoCommands C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\gles2\_cmd\_decoder\_passthrough.cc:808  

#10 0x7ffaa8d6804b in gpu::CommandBufferService::Flush C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\command\_buffer\_service.cc:70  

#11 0x7ffaa609af6c in gpu::CommandBufferStub::OnAsyncFlush C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command\_buffer\_stub.cc:500  

#12 0x7ffaa609a146 in gpu::CommandBufferStub::ExecuteDeferredRequest C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command\_buffer\_stub.cc:152  

#13 0x7ffaa60a6b37 in gpu::GpuChannel::ExecuteDeferredRequest C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\gpu\_channel.cc:670  

#14 0x7ffaa60b199f in base::internal::Invoker<base::internal::BindState<void (gpu::GpuChannel::\*)(mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);)),base::WeakPtr[gpu::GpuChannel](javascript:void(0);),mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);) >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind\_internal.h:748  

#15 0x7ffaa5cdfc6c in gpu::Scheduler::RunNextTask C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\scheduler.cc:691  

#16 0x7ffaa4820714 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:135  

#17 0x7ffaa76c3215 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:386  

#18 0x7ffaa76c2809 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:291  

#19 0x7ffaa769f8aa in base::MessagePumpDefault::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_default.cc:39  

#20 0x7ffaa76c4980 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:498  

#21 0x7ffaa479b2b3 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:141  

#22 0x7ffaa6fce29e in content::GpuMain C:\b\s\w\ir\cache\builder\src\content\gpu\gpu\_main.cc:405  

#23 0x7ffaa43ca48b in content::RunOtherNamedProcessTypeMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:682  

#24 0x7ffaa43cc0c7 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1021  

#25 0x7ffaa43c8abb in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:407  

#26 0x7ffaa43c9244 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:435  

#27 0x7ffa992514ca in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc:176

previously allocated by thread T0 here:  

#0 0x7ff7b063e9cb in malloc C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:98  

#1 0x7ffa98beefc6 in operator new d:\a01\_work\12\s\src\vctools\crt\vcstartup\src\heap\new\_scalar.cpp:35  

#2 0x7ffa9866d8c9 in rx::ContextVk::createBuffer C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\ContextVk.cpp:4814  

#3 0x7ffa97f3024a in gl::Buffer::Buffer C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\Buffer.cpp:47  

#4 0x7ffa9808b1a3 in gl::BufferManager::AllocateNewObject C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\ResourceManager.cpp:114  

#5 0x7ffa97eebc17 in gl::TypedResourceManager[gl::Buffer,gl::BufferManager,gl::BufferID](javascript:void(0);)::checkObjectAllocationImpl<> C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\ResourceManager.h:117  

#6 0x7ffa97edda65 in GL\_BindBuffer C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libGLESv2\entry\_points\_gles\_2\_0\_autogen.cpp:118  

#7 0x7ffaafbadac7 in gpu::gles2::GLES2DecoderPassthroughImpl::DoBindBuffer C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\gles2\_cmd\_decoder\_passthrough\_doers.cc:390  

#8 0x7ffaabf697fb in gpu::gles2::GLES2DecoderPassthroughImpl::DoCommandsImpl<0> C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\gles2\_cmd\_decoder\_passthrough.cc:870  

#9 0x7ffaabf68c50 in gpu::gles2::GLES2DecoderPassthroughImpl::DoCommands C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\gles2\_cmd\_decoder\_passthrough.cc:808  

#10 0x7ffaa8d6804b in gpu::CommandBufferService::Flush C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\command\_buffer\_service.cc:70  

#11 0x7ffaa609af6c in gpu::CommandBufferStub::OnAsyncFlush C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command\_buffer\_stub.cc:500  

#12 0x7ffaa609a146 in gpu::CommandBufferStub::ExecuteDeferredRequest C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command\_buffer\_stub.cc:152  

#13 0x7ffaa60a6b37 in gpu::GpuChannel::ExecuteDeferredRequest C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\gpu\_channel.cc:670  

#14 0x7ffaa60b199f in base::internal::Invoker<base::internal::BindState<void (gpu::GpuChannel::\*)(mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);)),base::WeakPtr[gpu::GpuChannel](javascript:void(0);),mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);) >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind\_internal.h:748  

#15 0x7ffaa5cdfc6c in gpu::Scheduler::RunNextTask C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\scheduler.cc:691  

#16 0x7ffaa4820714 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:135  

#17 0x7ffaa76c3215 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:386  

#18 0x7ffaa76c2809 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:291  

#19 0x7ffaa769f8aa in base::MessagePumpDefault::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_default.cc:39  

#20 0x7ffaa76c4980 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:498  

#21 0x7ffaa479b2b3 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:141  

#22 0x7ffaa6fce29e in content::GpuMain C:\b\s\w\ir\cache\builder\src\content\gpu\gpu\_main.cc:405  

#23 0x7ffaa43ca48b in content::RunOtherNamedProcessTypeMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:682  

#24 0x7ffaa43cc0c7 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1021  

#25 0x7ffaa43c8abb in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:407  

#26 0x7ffaa43c9244 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:435  

#27 0x7ffa992514ca in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc:176

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\vk\_helpers.cpp:1330 in rx::vk::CommandBufferHelperCommon::usesBuffer  

Shadow bytes around the buggy address:  

0x0421def17e90: fd fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa  

0x0421def17ea0: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd  

0x0421def17eb0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0421def17ec0: fd fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa  

0x0421def17ed0: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd  

=>0x0421def17ee0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd[fd]fd  

0x0421def17ef0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fa  

0x0421def17f00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0421def17f10: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0421def17f20: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0421def17f30: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

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

==6788==ABORTING  

[20576:20036:0406/204207.698:ERROR:gpu\_process\_host.cc(973)] GPU process exited unexpectedly: exit\_code=1

**CREDIT INFORMATION**  

Reporter credit: SeongHwan Park (SeHwa)

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 1.7 KB)

## Timeline

### [Deleted User] (2022-04-06)

[Empty comment from Monorail migration]

### cl...@chromium.org (2022-04-06)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6205249010073600.

### rs...@chromium.org (2022-04-06)

Thanks, I can reproduce this on Linux.

[Monorail components: Internals>GPU>Vulkan]

### [Deleted User] (2022-04-06)

[Empty comment from Monorail migration]

### cl...@chromium.org (2022-04-07)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-07)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jm...@chromium.org (2022-04-07)

Won't affect Android, may affect Mac.

### jm...@chromium.org (2022-04-11)

Believe this is a duplicate of an earlier report, fixed in 101.

### jm...@chromium.org (2022-04-11)

Seems to still repro in ToT, looking again.

### gg...@gmail.com (2022-04-12)

I just looked at https://crrev.com/c/3578378/
May I know why is this commit's bug number 1305190?
The test code included in the patch seems to be the PoC I uploaded.

I don't know exactly because I can't see the 1305190 report,
but 1305190 seems to have been patched in commit 708ce9cfd63.
My PoC is still valid with this patch applied.

Thanks.

### jm...@chromium.org (2022-04-12)

Ah, I used the wrong bug ID. This bug was fixed by

commit 5c85fd4e11a3835a0719223a7cedb978d309da21
Author: Jamie Madill <jmadill@chromium.org>
Date: Mon Apr 11 16:29:00 2022

Add error check on resuming XFB with deleted buffer.

Bug: chromium:1305190
Change-Id: I22c6f6400b05ca32c922fba9a3b9d4b5841ca8b8
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3578378
Auto-Submit: Jamie Madill <jmadill@chromium.org>
Reviewed-by: Geoff Lang <geofflang@chromium.org>
Commit-Queue: Jamie Madill <jmadill@chromium.org>


### [Deleted User] (2022-04-12)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-12)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-12)

This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M100. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M101. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-04-12)

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

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

### [Deleted User] (2022-04-12)

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

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

### am...@chromium.org (2022-04-16)

M101 and M100 merges approved; please merge this fix to branches 4951 and 4896 respectively and before 10am PDT Tuesday, 19 April so this fix can be included in the M101 Stable cut and M100 Extended -- thanks! 

### gi...@appspot.gserviceaccount.com (2022-04-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/e37380e62a427cbb7172b6c17f8752ab96abf356

commit e37380e62a427cbb7172b6c17f8752ab96abf356
Author: Jamie Madill <jmadill@chromium.org>
Date: Mon Apr 11 16:29:00 2022

[M101] Add error check on resuming XFB with deleted buffer.

Bug: chromium:1313905
Change-Id: I22c6f6400b05ca32c922fba9a3b9d4b5841ca8b8
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3578378
Auto-Submit: Jamie Madill <jmadill@chromium.org>
Reviewed-by: Geoff Lang <geofflang@chromium.org>
Commit-Queue: Jamie Madill <jmadill@chromium.org>
(cherry picked from commit 5c85fd4e11a3835a0719223a7cedb978d309da21)
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3594102
Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>

[modify] https://crrev.com/e37380e62a427cbb7172b6c17f8752ab96abf356/src/libANGLE/validationES3.cpp


### gi...@appspot.gserviceaccount.com (2022-04-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/d49484c21e3c43b06dbe1274e94908559dc444a1

commit d49484c21e3c43b06dbe1274e94908559dc444a1
Author: Jamie Madill <jmadill@chromium.org>
Date: Mon Apr 11 16:29:00 2022

[M100] Add error check on resuming XFB with deleted buffer.

Bug: chromium:1313905
Change-Id: I22c6f6400b05ca32c922fba9a3b9d4b5841ca8b8
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3578378
Auto-Submit: Jamie Madill <jmadill@chromium.org>
Reviewed-by: Geoff Lang <geofflang@chromium.org>
Commit-Queue: Jamie Madill <jmadill@chromium.org>
(cherry picked from commit 5c85fd4e11a3835a0719223a7cedb978d309da21)
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3594103
Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>

[modify] https://crrev.com/d49484c21e3c43b06dbe1274e94908559dc444a1/src/libANGLE/validationES3.cpp


### gi...@appspot.gserviceaccount.com (2022-04-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/e37380e62a427cbb7172b6c17f8752ab96abf356

commit e37380e62a427cbb7172b6c17f8752ab96abf356
Author: Jamie Madill <jmadill@chromium.org>
Date: Mon Apr 11 16:29:00 2022

[M101] Add error check on resuming XFB with deleted buffer.

Bug: chromium:1313905
Change-Id: I22c6f6400b05ca32c922fba9a3b9d4b5841ca8b8
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3578378
Auto-Submit: Jamie Madill <jmadill@chromium.org>
Reviewed-by: Geoff Lang <geofflang@chromium.org>
Commit-Queue: Jamie Madill <jmadill@chromium.org>
(cherry picked from commit 5c85fd4e11a3835a0719223a7cedb978d309da21)
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3594102
Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>

[modify] https://crrev.com/e37380e62a427cbb7172b6c17f8752ab96abf356/src/libANGLE/validationES3.cpp


### am...@google.com (2022-04-22)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-04-22)

Congratulations, SeongHwan! The VRP Panel has decided to award you $10,000 for this report. Thank you for your efforts and excellent work in reporting GPU process memory corruption bugs! 

### am...@chromium.org (2022-04-25)

[Empty comment from Monorail migration]

### am...@google.com (2022-04-25)

[Empty comment from Monorail migration]

### am...@google.com (2022-04-26)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-20)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2022-07-26)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-29)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1313905?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedinto: crbug.com/chromium/1305190]
[Monorail components added to Component Tags custom field.]

### dt...@google.com (2025-02-13)

Bulk update of issues accidentally marked as duplicate in issue tracker migration (b/325072672)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059304)*
