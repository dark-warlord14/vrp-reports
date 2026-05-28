# Security: [ANGLE] Heap-buffer-overflow caused by writing exceeding the querypool size

| Field | Value |
|-------|-------|
| **Issue ID** | [40060610](https://issues.chromium.org/issues/40060610) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU>Vulkan |
| **Platforms** | Android, Linux, Windows, ChromeOS |
| **Reporter** | gg...@gmail.com |
| **Assignee** | jm...@chromium.org |
| **Created** | 2022-08-18 |
| **Bounty** | $17,000.00 |

## Description

**VULNERABILITY DETAILS**  

There is a heap buffer overflow vulnerability that exists in the Vulkan backend.

In the QueryVk::allocateQuery, call getCurrentViewCount() to get the current viewCount value.  

And in the allocatePoolEntries function, there is a conditional statement as below.  

**-------------------------** --------------------------------------------------------------  

angle::Result DynamicallyGrowingPool<Pool>::allocatePoolEntries(ContextVk \*contextVk,  

uint32\_t entryCount,  

uint32\_t \*poolIndex,  

uint32\_t \*currentEntryOut)  

{  

if (mCurrentFreeEntry + entryCount > mPoolSize)  

{  

if (!findFreeEntryPool(contextVk))  

{  

Pool newPool;  

ANGLE\_TRY(allocatePoolImpl(contextVk, newPool, mPoolSize));  

ANGLE\_TRY(allocateNewEntryPool(contextVk, std::move(newPool)));  

}  

}  

....  

}  

**-------------------------** --------------------------------------------------------------

Above mPoolSize is set to the values below.  

**-------------------------** --------------------------------------------------------------  

constexpr uint32\_t kDefaultOcclusionQueryPoolSize = 64;  

constexpr uint32\_t kDefaultTimestampQueryPoolSize = 64;  

constexpr uint32\_t kDefaultTransformFeedbackQueryPoolSize = 128;  

constexpr uint32\_t kDefaultPrimitivesGeneratedQueryPoolSize = 128;  

**-------------------------** --------------------------------------------------------------

If the new queryCount value(mCurrentFreeEntry+entryCount) is greater than mPoolSize, the pool is reallocated.  

And the getCurrentViewCount function gets the viewCount value from the mRenderPassDesc of mDrawFramebuffer.  

**-------------------------** --------------------------------------------------------------  

uint32\_t ContextVk::getCurrentViewCount() const  

{  

FramebufferVk \*drawFBO = vk::GetImpl(mState.getDrawFramebuffer());  

return drawFBO->getRenderPassDesc().viewCount();  

}  

**-------------------------** --------------------------------------------------------------

The mRenderPassDesc used above is a member of drawFramebuffer, so this can be changed it to bindFramebuffer.  

When the current mCurrentFreeEntry value is mPoolSize - 1, the pool will not be reallocated in the allocatePoolEntries function if binding a new drawFramebuffer.

However, mRenderPassDesc also exists as a member of RenderPassCommandBufferHelper class.  

In the attached PoC, when the gl.clear function is called, The RenderPassCommandBufferHelper::beginRenderPass function is also called.  

mRenderPassDesc of RenderPassCommandBufferHelper is set in this function.  

This is not changed by calling bindFramebuffer. And the CmdBeginRenderPass use this mRenderPassDesc.

In SwiftShader, the code below is called.  

**-------------------------** --------------------------------------------------------------  

class CmdBeginQuery : public vk::CommandBuffer::Command  

{  

public:  

CmdBeginQuery(vk::QueryPool \*queryPool, uint32\_t query, VkQueryControlFlags flags)  

: queryPool(queryPool)  

, query(query)  

, flags(flags)  

{  

}

```
void execute(vk::CommandBuffer::ExecutionState &executionState) override  
{  
	// "If queries are used while executing a render pass instance that has multiview enabled, the query uses  
	//  N consecutive query indices in the query pool (starting at `query`)"  
	for(uint32_t i = 0; i < executionState.viewCount(); i++)  
	{  
		queryPool->begin(query + i, flags);  
	}  
        .....  

```

}  

**-------------------------** --------------------------------------------------------------

As a result, the executionState.viewCount() above gets its value from mRenderPassDesc in RenderPassCommandBufferHelper.  

However, even if this value is greater than 1, the queryPool may not have been reallocated. (as seen above)  

This can cause a heap buffer overflow.

Before commit ca5e6f685c5d73b32bd729d5ed81115eaccbc9b3, the getCurrentViewCount function used mRenderPassDesc from ContextVk::mDrawFramebuffer.  

This didn't changed immediately after binding a new drawFramebuffer unlike mState.mDrawFramebuffer. (before syncState DIRTY\_BIT\_DRAW\_FRAMEBUFFER\_BINDING)  

So before this commit, allocatePoolEntries function reallocated the pool. (In the same situation as above)  

(ContextVk::mDrawFramebuffer has been removed for now.)

This vulnerability is first valid in asan-win32-release\_x64-935597 and in stable version 96.0.4664.45.  

In older versions(included 935597 / 96.0.4664.45), the PRE\_QUERY\_CNT value of the attached PoC must be 63 to work. (mPoolSize - 1)  

However, due to internal behavior changes at some point, now the PRE\_QUERY\_CNT value should be 62 for it to work. (mPoolSize - 2)

**VERSION**  

Chrome Version: master (and tested on 104.0.5112.102 (Official Build) (64-bit) Stable)  

Operating System: Windows, Linux, ...

**REPRODUCTION CASE**  

Run the attached poc.html (with --disable-gpu)

# **FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION** Type of crash: GPU Process Crash State:

==17592==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x1281a1fa78b0 at pc 0x7fff4d37f3d7 bp 0x00caffbff530 sp 0x00caffbff578  

WRITE of size 4 at 0x1281a1fa78b0 thread T4  

==17592==WARNING: Failed to use and restart external symbolizer!  

==17592==\*\*\* WARNING: Failed to initialize DbgHelp! \*\*\*  

==17592==\*\*\* Most likely this means that the app is already \*\*\*  

==17592==\*\*\* using DbgHelp, possibly with incompatible flags. \*\*\*  

==17592==\*\*\* Due to technical reasons, symbolization might crash \*\*\*  

==17592==\*\*\* or produce wrong results. \*\*\*  

#0 0x7fff4d37f3d6 in vk::QueryPool::begin C:\b\s\w\ir\cache\builder\src\third\_party\swiftshader\src\Vulkan\VkQueryPool.cpp:194  

#1 0x7fff4d32e9c7 in `anonymous namespace'::CmdBeginQuery::execute C:\b\s\w\ir\cache\builder\src\third\_party\swiftshader\src\Vulkan\VkCommandBuffer.cpp:1540  

#2 0x7fff4d32c6e5 in vk::CommandBuffer::submit C:\b\s\w\ir\cache\builder\src\third\_party\swiftshader\src\Vulkan\VkCommandBuffer.cpp:2344  

#3 0x7fff4d380ef0 in vk::Queue::submitQueue C:\b\s\w\ir\cache\builder\src\third\_party\swiftshader\src\Vulkan\VkQueue.cpp:104  

#4 0x7fff4d37fd5d in vk::Queue::taskLoop C:\b\s\w\ir\cache\builder\src\third\_party\swiftshader\src\Vulkan\VkQueue.cpp:156  

#5 0x7fff4d382987 in std::Cr::\_\_thread\_proxy<std::Cr::tuple<std::Cr::unique\_ptr<std::Cr::\_\_thread\_struct,std::Cr::default\_delete[std::Cr::\_\_thread\_struct](javascript:void(0);) >,void (vk::Queue::\*)(marl::Scheduler \*),vk::Queue \*,marl::Scheduler \*> > C:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\thread:296  

#6 0x7fff4dd573c5 in thread\_start<unsigned int (\_\_cdecl\*)(void \*),1> C:\b\s\w\ir\cache\builder\src\out\Release\_x64\minkernel\crts\ucrt\src\appcrt\startup\thread.cpp:97  

#7 0x7ff7d95029d3 in \_\_asan::AsanThread::ThreadStart C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_thread.cpp:277  

#8 0x7ff82e0d7033 in BaseThreadInitThunk+0x13 (C:\WINDOWS\System32\KERNEL32.DLL+0x180017033)  

#9 0x7ff8300a2650 in RtlUserThreadStart+0x20 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x180052650)

0x1281a1fa78b0 is located 24 bytes to the right of 3096-byte region [0x1281a1fa6c80,0x1281a1fa7898)  

allocated by thread T0 here:  

#0 0x7ff7d94f81cc in malloc C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:98  

#1 0x7fff4d6f127a in sw::allocateZeroOrPoison C:\b\s\w\ir\cache\builder\src\third\_party\swiftshader\src\System\Memory.cpp:110  

#2 0x7fff4d39cc43 in vk::ObjectBase<vk::QueryPool,VkNonDispatchableHandle<VkQueryPool\_T \*> >::Create<VkQueryPoolCreateInfo> C:\b\s\w\ir\cache\builder\src\third\_party\swiftshader\src\Vulkan\VkObject.hpp:92  

#3 0x7fff4d39cb17 in vkCreateQueryPool C:\b\s\w\ir\cache\builder\src\third\_party\swiftshader\src\Vulkan\libVulkan.cpp:1745  

#4 0x7fff4eebef9c in rx::vk::DynamicQueryPool::allocatePoolImpl C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\vk\_helpers.cpp:3707  

#5 0x7fff4eebeaf7 in rx::vk::DynamicallyGrowingPool[rx::vk::QueryPool](javascript:void(0);)::allocatePoolEntries C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\vk\_helpers.cpp:3631  

#6 0x7fff4eebe783 in rx::vk::DynamicQueryPool::allocateQuery C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\vk\_helpers.cpp:3684  

#7 0x7fff4ed88898 in rx::QueryVk::onRenderPassStart C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\QueryVk.cpp:211  

#8 0x7fff4ed40521 in rx::ContextVk::resumeRenderPassQueriesIfActive C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\ContextVk.cpp:7180  

#9 0x7fff4ed1f691 in rx::ContextVk::startRenderPass C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\ContextVk.cpp:6743  

#10 0x7fff4ecfe337 in rx::ContextVk::handleDirtyGraphicsRenderPass C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\ContextVk.cpp:1895  

#11 0x7fff4ed17268 in rx::ContextVk::setupDraw C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\ContextVk.cpp:1274  

#12 0x7fff4ed24fe1 in rx::ContextVk::drawArrays C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\ContextVk.cpp:3438  

#13 0x7fff4e54cfc6 in GL\_DrawArrays C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libGLESv2\entry\_points\_gles\_2\_0\_autogen.cpp:1109  

#14 0x7fff5f8e4024 in gl::RealGLApi::glDrawArraysFn C:\b\s\w\ir\cache\builder\src\ui\gl\gl\_gl\_api\_implementation.cc:451  

#15 0x7fff6b53d357 in gpu::gles2::GLES2DecoderPassthroughImpl::DoDrawArrays C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\gles2\_cmd\_decoder\_passthrough\_doers.cc:1223  

#16 0x7fff68ffb9c3 in gpu::gles2::GLES2DecoderPassthroughImpl::DoCommandsImpl<0> C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\gles2\_cmd\_decoder\_passthrough.cc:894  

#17 0x7fff68ffadc8 in gpu::gles2::GLES2DecoderPassthroughImpl::DoCommands C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\gles2\_cmd\_decoder\_passthrough.cc:832  

#18 0x7fff5ffdecaf in gpu::CommandBufferService::Flush C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\command\_buffer\_service.cc:229  

#19 0x7fff5d3b2e74 in gpu::CommandBufferStub::OnAsyncFlush C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command\_buffer\_stub.cc:498  

#20 0x7fff5d3b1f86 in gpu::CommandBufferStub::ExecuteDeferredRequest C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command\_buffer\_stub.cc:154  

#21 0x7fff5ffcd049 in gpu::GpuChannel::ExecuteDeferredRequest C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\gpu\_channel.cc:706  

#22 0x7fff5ffd824d in base::internal::Invoker<base::internal::BindState<void (gpu::GpuChannel::\*)(mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);)),base::WeakPtr[gpu::GpuChannel](javascript:void(0);),mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);) >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind\_internal.h:819  

#23 0x7fff5d07f831 in gpu::Scheduler::RunNextTask C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\scheduler.cc:698  

#24 0x7fff5bc06eca in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:135  

#25 0x7fff5e9a8719 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:424  

#26 0x7fff5e9a7736 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:294  

#27 0x7fff5e9857ca in base::MessagePumpDefault::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_default.cc:39

Thread T4 created by T0 here:  

#0 0x7ff7d9503462 in \_\_asan\_wrap\_CreateThread C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_win.cpp:146  

#1 0x7fff4dd57292 in \_beginthreadex C:\b\s\w\ir\cache\builder\src\out\Release\_x64\minkernel\crts\ucrt\src\appcrt\startup\thread.cpp:209  

#2 0x7fff4d9331f7 in std::Cr::\_\_libcpp\_thread\_create C:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\src\support\win32\thread\_win32.cpp:203  

#3 0x7fff4d380066 in std::Cr::thread::thread<void (vk::Queue::\*)(marl::Scheduler \*),vk::Queue \*,marl::Scheduler \*&,void> C:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\thread:312  

#4 0x7fff4d37fa9f in vk::Queue::Queue C:\b\s\w\ir\cache\builder\src\third\_party\swiftshader\src\Vulkan\VkQueue.cpp:38  

#5 0x7fff4d33cdc9 in vk::Device::Device C:\b\s\w\ir\cache\builder\src\third\_party\swiftshader\src\Vulkan\VkDevice.cpp:138  

#6 0x7fff4d398225 in vk::DispatchableObject<vk::Device,VkDevice\_T \*>::Create<VkDeviceCreateInfo,vk::PhysicalDevice \*,const VkPhysicalDeviceFeatures \*,std::Cr::shared\_ptr[marl::Scheduler](javascript:void(0);) > C:\b\s\w\ir\cache\builder\src\third\_party\swiftshader\src\Vulkan\VkObject.hpp:147  

#7 0x7fff4d397b14 in vkCreateDevice C:\b\s\w\ir\cache\builder\src\third\_party\swiftshader\src\Vulkan\libVulkan.cpp:1093  

#8 0x7fff4e22f143 in terminator\_CreateDevice C:\b\s\w\ir\cache\builder\src\third\_party\vulkan-deps\vulkan-loader\src\loader\loader.c:5730  

#9 0x7fff4e229309 in loader\_create\_device\_chain C:\b\s\w\ir\cache\builder\src\third\_party\vulkan-deps\vulkan-loader\src\loader\loader.c:4932  

#10 0x7fff4e227c0c in loader\_layer\_create\_device C:\b\s\w\ir\cache\builder\src\third\_party\vulkan-deps\vulkan-loader\src\loader\loader.c:4365  

#11 0x7fff4e23e680 in vkCreateDevice C:\b\s\w\ir\cache\builder\src\third\_party\vulkan-deps\vulkan-loader\src\loader\trampoline.c:848  

#12 0x7fff4edb5fef in rx::RendererVk::initializeDevice C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\RendererVk.cpp:2738  

#13 0x7fff4edae8d0 in rx::RendererVk::initialize C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\RendererVk.cpp:1744  

#14 0x7fff4ed5081f in rx::DisplayVk::initialize C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\DisplayVk.cpp:50  

#15 0x7fff4ef14e22 in rx::DisplayVkWin32::initialize C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\win32\DisplayVkWin32.cpp:62  

#16 0x7fff4e60ac83 in egl::Display::initialize C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\Display.cpp:993  

#17 0x7fff4e530609 in egl::Initialize C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libGLESv2\egl\_stubs.cpp:468  

#18 0x7fff4e537d83 in EGL\_Initialize C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libGLESv2\entry\_points\_egl\_autogen.cpp:330  

#19 0x7fff5f9ee130 in gl::GLDisplayEGL::InitializeDisplay C:\b\s\w\ir\cache\builder\src\ui\gl\gl\_display.cc:917  

#20 0x7fff5f9e899b in gl::GLDisplayEGL::Initialize C:\b\s\w\ir\cache\builder\src\ui\gl\gl\_display.cc:791  

#21 0x7fff5f9d42ce in gl::init::InitializeGLOneOffPlatform C:\b\s\w\ir\cache\builder\src\ui\gl\init\gl\_initializer\_win.cc:132  

#22 0x7fff5ce7ac35 in gl::init::InitializeGLOneOffPlatformImplementation C:\b\s\w\ir\cache\builder\src\ui\gl\init\gl\_factory.cc:219  

#23 0x7fff5ce7a481 in gl::init::`anonymous namespace'::InitializeGLOneOffPlatformHelper C:\b\s\w\ir\cache\builder\src\ui\gl\init\gl\_factory.cc:143  

#24 0x7fff5ce7a7c1 in gl::init::InitializeGLNoExtensionsOneOff C:\b\s\w\ir\cache\builder\src\ui\gl\init\gl\_factory.cc:174  

#25 0x7fff5d3be86f in gpu::GpuInit::InitializeAndStartSandbox C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\gpu\_init.cc:478  

#26 0x7fff5e1e2819 in content::GpuMain C:\b\s\w\ir\cache\builder\src\content\gpu\gpu\_main.cc:322  

#27 0x7fff5b755c07 in content::RunOtherNamedProcessTypeMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:722  

#28 0x7fff5b757e02 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1071  

#29 0x7fff5b7541c5 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:433  

#30 0x7fff5b754998 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:461  

#31 0x7fff4fe614ac in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc:182  

#32 0x7ff7d9455a0e in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main\_dll\_loader\_win.cc:162  

#33 0x7ff7d9452bd0 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_exe\_main\_win.cc:395  

#34 0x7ff7d986febf in \_\_scrt\_common\_main\_seh d:\a01\_work\12\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#35 0x7ff82e0d7033 in BaseThreadInitThunk+0x13 (C:\WINDOWS\System32\KERNEL32.DLL+0x180017033)  

#36 0x7ff8300a2650 in RtlUserThreadStart+0x20 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x180052650)

SUMMARY: AddressSanitizer: heap-buffer-overflow C:\b\s\w\ir\cache\builder\src\third\_party\swiftshader\src\Vulkan\VkQueryPool.cpp:194 in vk::QueryPool::begin  

Shadow bytes around the buggy address:  

0x0493d62f4ec0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0493d62f4ed0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0493d62f4ee0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0493d62f4ef0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0493d62f4f00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

=>0x0493d62f4f10: 00 00 00 fa fa fa[fa]fa fa fa fa fa fa fa fa fa  

0x0493d62f4f20: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0493d62f4f30: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0493d62f4f40: fa fa fa fa fa fa fa fa fa fa fa fa fa fa f7 fa  

0x0493d62f4f50: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0493d62f4f60: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

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

==17592==ABORTING  

[25780:31724:0817/035531.329:ERROR:gpu\_process\_host.cc(973)] GPU process exited unexpectedly: exit\_code=1

**CREDIT INFORMATION**  

Reporter credit: SeongHwan Park (SeHwa)

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 2.1 KB)

## Timeline

### [Deleted User] (2022-08-18)

[Empty comment from Monorail migration]

### sr...@google.com (2022-08-19)

[Empty comment from Monorail migration]

[Monorail components: Internals>GPU>Vulkan]

### [Deleted User] (2022-08-19)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-19)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-08-19)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ti...@chromium.org (2022-08-24)

[Empty comment from Monorail migration]

### jm...@chromium.org (2022-08-24)

Sorry for the slow response, was OOO. Will take a look at this in the next couple of days.

### ti...@chromium.org (2022-08-24)

[Comment Deleted]

### ti...@chromium.org (2022-08-24)

geofflang@, jmadill@, penghuang@, I believe the validating command buffer is still used on Android. What's the impact/reach of these types of ANGLE bugs on Android OS?

### ge...@chromium.org (2022-08-24)

This is a security issue in ANGLE's Vulkan backend. From the original report we can see it reproducing with the --disable-gpu flag which forces ANGLE to use its Vulkan backend and SwiftShader as the Vulkan driver.

SwiftShader is not required to trigger this but is the easiest way to trigger the use of ANGLE's Vulkan backend.

Shabi, you may be the most familiar with the query pools. Can you take/assign this?

### jm...@chromium.org (2022-08-24)

As I said in https://crbug.com/chromium/1354271#c7 I'll take a look in the next few days. Shabi has a bunch on his plate already.

### ge...@chromium.org (2022-08-24)

Also to clarify how ANGLE and the command decoders are is used for the Chrome security folks:

 - Validating command decoder can run on any GLES driver but in practice never runs on ANGLE (can be forced with flags).
 - Passthrough command decoder always runs on ANGLE. It cannot function without some extra validation that ANGLE provides.

The passthrough command decoder shipped/default on: Windows, Linux, Mac
The passthrough command decoder is currently in finch for: Android (1% stable, 50% beta/dev/canary), and ChromeOS (50% canary/dev)

ANGLE has multiple backends targeting different graphics APIs:
 - D3D11 and D3D9 are used on Windows
 - OpenGL and Metal (finching) on Mac
 - OpenGL and Vulkan (finching) on Linux and Android
 - OpenGL ES on ChromeOS

ANGLE also supports a software rendering mode "SwANGLE" which ANGLE's Vulkan backend + SwiftShader as the Vulkan driver as a fallback when the system's gpu/driver is blocklisted.

### [Deleted User] (2022-09-08)

jmadill: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jm...@chromium.org (2022-09-08)

I have a WIP solution that causes some test failures, still investigating.

### [Deleted User] (2022-09-23)

jmadill: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-09-28)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-10-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/4ebdac790c76b65abf5703bcef9482c638076195

commit 4ebdac790c76b65abf5703bcef9482c638076195
Author: Jamie Madill <jmadill@chromium.org>
Date: Mon Aug 29 20:25:46 2022

Vulkan: Ensure we sync the draw FB before beingQuery.

Bug: chromium:1354271
Change-Id: I5fe3649d9d39de37d0a59c80a4f31a17d1a72838
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3863145
Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>
Commit-Queue: Jamie Madill <jmadill@chromium.org>

[modify] https://crrev.com/4ebdac790c76b65abf5703bcef9482c638076195/src/libANGLE/renderer/vulkan/QueryVk.cpp
[modify] https://crrev.com/4ebdac790c76b65abf5703bcef9482c638076195/src/tests/gl_tests/StateChangeTest.cpp
[modify] https://crrev.com/4ebdac790c76b65abf5703bcef9482c638076195/src/libANGLE/State.h


### gi...@appspot.gserviceaccount.com (2022-10-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/a326d089b704a91c3463bd0d56576860bd884461

commit a326d089b704a91c3463bd0d56576860bd884461
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Thu Oct 06 21:33:05 2022

Roll ANGLE from 04f3ed80f471 to c19ec9481a70 (3 revisions)

https://chromium.googlesource.com/angle/angle.git/+log/04f3ed80f471..c19ec9481a70

2022-10-06 abdolrashidi@google.com Vulkan: Implement imageless framebuffers
2022-10-06 jmadill@chromium.org Vulkan: Ensure we sync the draw FB before beingQuery.
2022-10-06 chris@rive.app Implement PLS on Apple Silicon

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
Bug: chromium:1354271
Tbr: ianelliott@google.com
Change-Id: Ibd1d9249536ca4fdf23f83bc1c7220ad377ddec0
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3938216
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#1056023}

[modify] https://crrev.com/a326d089b704a91c3463bd0d56576860bd884461/DEPS


### fl...@google.com (2022-10-07)

Thanks for the patch!  Is there anything else to be done here, or is it OK to mark this fixed?

### jm...@chromium.org (2022-10-07)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-08)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-08)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-08)

Requesting merge to stable M106 because latest trunk commit (1056023) appears to be after stable branch point (1036826).

Requesting merge to beta M107 because latest trunk commit (1056023) appears to be after beta branch point (1047731).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-10-08)

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
Owners: govind (Android), eakpobaro (iOS), dgagnon (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-10-08)

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

### am...@chromium.org (2022-10-13)

Hi Geoff -- thanks for this fix and the info in comments #10 and #12, very helpful indeed! 
107 merge approved, please merge to branch 5304 as soon as possible so this fix can be included in m107/beta update
106 merge approved, please merge to branch 5249, so this fix can be included in the next Extended Stable updated when m107 is promoted to stable -- thank you

### am...@google.com (2022-10-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-10-14)

Congratulations, SeHwa! Nice finding! The VRP Panel has decided to award you $15,000 for this report + $1,000 bisect bonus for a $16,000 reward total. Thank you for your efforts in discovering and reporting this issue to us -- great work! 

### am...@chromium.org (2022-10-14)

Apologies, the bisect bonus here should have been $2,000 - as full bisect was provided in addition to providing providing full information and verification of this issue reproducing in and affecting the other active release branches/versions! Updating reward total to $17,000 accordingly. 

### gi...@appspot.gserviceaccount.com (2022-10-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/b8636b57b8f231994ecb3fb14f181c593c83a3fb

commit b8636b57b8f231994ecb3fb14f181c593c83a3fb
Author: Jamie Madill <jmadill@chromium.org>
Date: Mon Aug 29 20:25:46 2022

[M106] Vulkan: Ensure we sync the draw FB before beingQuery.

Bug: chromium:1354271
(cherry picked from commit 4ebdac790c76b65abf5703bcef9482c638076195)
Change-Id: I7b715a9c28badfe58a0ae1a478d2b4e8bbd23c47
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3956939
Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>

[modify] https://crrev.com/b8636b57b8f231994ecb3fb14f181c593c83a3fb/src/libANGLE/renderer/vulkan/QueryVk.cpp
[modify] https://crrev.com/b8636b57b8f231994ecb3fb14f181c593c83a3fb/src/libANGLE/State.h


### gi...@appspot.gserviceaccount.com (2022-10-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/bbf57e6db2fab3ee4c4336d6c73786b73aff28b2

commit bbf57e6db2fab3ee4c4336d6c73786b73aff28b2
Author: Jamie Madill <jmadill@chromium.org>
Date: Mon Aug 29 20:25:46 2022

[M107] Vulkan: Ensure we sync the draw FB before beingQuery.

Bug: chromium:1354271
Change-Id: I5fe3649d9d39de37d0a59c80a4f31a17d1a72838
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3863145
Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>
Commit-Queue: Jamie Madill <jmadill@chromium.org>
(cherry picked from commit 4ebdac790c76b65abf5703bcef9482c638076195)
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3956938

[modify] https://crrev.com/bbf57e6db2fab3ee4c4336d6c73786b73aff28b2/src/libANGLE/renderer/vulkan/QueryVk.cpp
[modify] https://crrev.com/bbf57e6db2fab3ee4c4336d6c73786b73aff28b2/src/libANGLE/State.h


### am...@google.com (2022-10-14)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-10-21)

[Empty comment from Monorail migration]

### am...@google.com (2022-10-27)

[Empty comment from Monorail migration]

### pg...@google.com (2022-11-01)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-14)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1354271?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060610)*
