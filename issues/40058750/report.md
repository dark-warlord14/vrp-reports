# Security: [ANGLE] Heap use-after-free in BufferHelper::recordReadBarrier

| Field | Value |
|-------|-------|
| **Issue ID** | [40058750](https://issues.chromium.org/issues/40058750) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU>Vulkan |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | gg...@gmail.com |
| **Assignee** | cc...@google.com |
| **Created** | 2022-02-11 |
| **Bounty** | $7,000.00 |

## Description

**VULNERABILITY DETAILS**  

There is a heap use-after-free vulnerability that could be triggered in Swiftshader.  

I think that this vulnerability started in commit 1608a9567b66c92cb346682a6e9e2aece070b181.

The attached PoC has already been minimized as far as I can.

**VERSION**  

Chrome Version: master (and tested on 100.0.4878.0 (Official Build) (64-bit) dev)  

Operating System: Windows 10 x64

**REPRODUCTION CASE**  

Run the attached poc.html (with --disable-gpu)

# **FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION** Type of crash: GPU Process Crash State:

==4072==ERROR: AddressSanitizer: heap-use-after-free on address 0x1209725ab9c4 at pc 0x7ffc11c4a1e7 bp 0x00a595dfe4a0 sp 0x00a595dfe4e8  

READ of size 4 at 0x1209725ab9c4 thread T0  

==4072==WARNING: Failed to use and restart external symbolizer!  

==4072==\*\*\* WARNING: Failed to initialize DbgHelp! \*\*\*  

==4072==\*\*\* Most likely this means that the app is already \*\*\*  

==4072==\*\*\* using DbgHelp, possibly with incompatible flags. \*\*\*  

==4072==\*\*\* Due to technical reasons, symbolization might crash \*\*\*  

==4072==\*\*\* or produce wrong results. \*\*\*  

#0 0x7ffc11c4a1e6 in rx::vk::BufferHelper::recordReadBarrier C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\vk\_helpers.cpp:4262  

#1 0x7ffc11c49d63 in rx::vk::CommandBufferHelperCommon::bufferRead C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\vk\_helpers.cpp:1057  

#2 0x7ffc11ae52dc in rx::ContextVk::handleDirtyGraphicsVertexBuffers C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\ContextVk.cpp:1871  

#3 0x7ffc11aef372 in rx::ContextVk::setupDraw C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\ContextVk.cpp:1190  

#4 0x7ffc11af98bb in rx::ContextVk::drawArrays C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\ContextVk.cpp:2739  

#5 0x7ffc11391f69 in GL\_DrawArrays C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libGLESv2\entry\_points\_gles\_2\_0\_autogen.cpp:1109  

#6 0x7ffbd0ba6fb2 in gpu::gles2::GLES2DecoderPassthroughImpl::DoDrawArrays C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\gles2\_cmd\_decoder\_passthrough\_doers.cc:1217  

#7 0x7ffbcd0a64ad in gpu::gles2::GLES2DecoderPassthroughImpl::DoCommandsImpl<0> C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\gles2\_cmd\_decoder\_passthrough.cc:871  

#8 0x7ffbcd0a58f4 in gpu::gles2::GLES2DecoderPassthroughImpl::DoCommands C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\gles2\_cmd\_decoder\_passthrough.cc:809  

#9 0x7ffbc9f681b6 in gpu::CommandBufferService::Flush C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\command\_buffer\_service.cc:70  

#10 0x7ffbc73a7c5c in gpu::CommandBufferStub::OnAsyncFlush C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command\_buffer\_stub.cc:499  

#11 0x7ffbc73a6e36 in gpu::CommandBufferStub::ExecuteDeferredRequest C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command\_buffer\_stub.cc:151  

#12 0x7ffbc73b372f in gpu::GpuChannel::ExecuteDeferredRequest C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\gpu\_channel.cc:669  

#13 0x7ffbc73be595 in base::internal::Invoker<base::internal::BindState<void (gpu::GpuChannel::\*)(mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);)),base::WeakPtr[gpu::GpuChannel](javascript:void(0);),mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);) >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind\_internal.h:748  

#14 0x7ffbc6fd780c in gpu::Scheduler::RunNextTask C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\scheduler.cc:691  

#15 0x7ffbc5b40534 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:135  

#16 0x7ffbc88ce335 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:387  

#17 0x7ffbc88cd909 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:292  

#18 0x7ffbc88a6067 in base::MessagePumpDefault::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_default.cc:38  

#19 0x7ffbc88cfa61 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:499  

#20 0x7ffbc5abfc83 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:141  

#21 0x7ffbc82f0184 in content::GpuMain C:\b\s\w\ir\cache\builder\src\content\gpu\gpu\_main.cc:404  

#22 0x7ffbc15c0243 in content::RunOtherNamedProcessTypeMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:683  

#23 0x7ffbc15c1f67 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1043  

#24 0x7ffbc15be876 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:399  

#25 0x7ffbc15beffa in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:427  

#26 0x7ffbbabe14ca in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc:176  

#27 0x7ff634cf5b16 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main\_dll\_loader\_win.cc:167  

#28 0x7ff634cf2b5f in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_exe\_main\_win.cc:382  

#29 0x7ff6350f4e7f in \_\_scrt\_common\_main\_seh d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#30 0x7ffc47ce7033 in BaseThreadInitThunk+0x13 (C:\WINDOWS\System32\KERNEL32.DLL+0x180017033)  

#31 0x7ffc48622650 in RtlUserThreadStart+0x20 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x180052650)

0x1209725ab9c4 is located 36 bytes inside of 56-byte region [0x1209725ab9a0,0x1209725ab9d8)  

freed by thread T0 here:  

#0 0x7ff634da22cb in free C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:82  

#1 0x7ffc11c96d1f in rx::vk::BufferHelper::~BufferHelper C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\vk\_helpers.cpp:3807  

#2 0x7ffc1180e03d in std::\_\_1::vector<std::\_\_1::unique\_ptr<rx::StaticVertexBufferInterface,std::\_\_1::default\_delete[rx::StaticVertexBufferInterface](javascript:void(0);) >,std::\_\_1::allocator<std::\_\_1::unique\_ptr<rx::StaticVertexBufferInterface,std::\_\_1::default\_delete[rx::StaticVertexBufferInterface](javascript:void(0);) > > >::clear C:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\vector:775  

#3 0x7ffc11c5717d in rx::vk::DynamicBuffer::releaseInFlightBuffersToResourceUseList C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\vk\_helpers.cpp:2522  

#4 0x7ffc11b11ce2 in rx::ContextVk::flushAndGetSerial C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\ContextVk.cpp:5720  

#5 0x7ffc11b1351b in rx::ContextVk::flushCommandsAndEndRenderPassImpl C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\ContextVk.cpp:6142  

#6 0x7ffc11af316c in rx::ContextVk::flushDirtyGraphicsRenderPass C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\ContextVk.cpp:6165  

#7 0x7ffc11ae3fe8 in rx::ContextVk::handleDirtyGraphicsRenderPass C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\ContextVk.cpp:1728  

#8 0x7ffc11aef372 in rx::ContextVk::setupDraw C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\ContextVk.cpp:1190  

#9 0x7ffc11af98bb in rx::ContextVk::drawArrays C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\ContextVk.cpp:2739  

#10 0x7ffc11391f69 in GL\_DrawArrays C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libGLESv2\entry\_points\_gles\_2\_0\_autogen.cpp:1109  

#11 0x7ffbd0ba6fb2 in gpu::gles2::GLES2DecoderPassthroughImpl::DoDrawArrays C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\gles2\_cmd\_decoder\_passthrough\_doers.cc:1217  

#12 0x7ffbcd0a64ad in gpu::gles2::GLES2DecoderPassthroughImpl::DoCommandsImpl<0> C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\gles2\_cmd\_decoder\_passthrough.cc:871  

#13 0x7ffbcd0a58f4 in gpu::gles2::GLES2DecoderPassthroughImpl::DoCommands C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\gles2\_cmd\_decoder\_passthrough.cc:809  

#14 0x7ffbc9f681b6 in gpu::CommandBufferService::Flush C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\command\_buffer\_service.cc:70  

#15 0x7ffbc73a7c5c in gpu::CommandBufferStub::OnAsyncFlush C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command\_buffer\_stub.cc:499  

#16 0x7ffbc73a6e36 in gpu::CommandBufferStub::ExecuteDeferredRequest C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command\_buffer\_stub.cc:151  

#17 0x7ffbc73b372f in gpu::GpuChannel::ExecuteDeferredRequest C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\gpu\_channel.cc:669  

#18 0x7ffbc73be595 in base::internal::Invoker<base::internal::BindState<void (gpu::GpuChannel::\*)(mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);)),base::WeakPtr[gpu::GpuChannel](javascript:void(0);),mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);) >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind\_internal.h:748  

#19 0x7ffbc6fd780c in gpu::Scheduler::RunNextTask C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\scheduler.cc:691  

#20 0x7ffbc5b40534 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:135  

#21 0x7ffbc88ce335 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:387  

#22 0x7ffbc88cd909 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:292  

#23 0x7ffbc88a6067 in base::MessagePumpDefault::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_default.cc:38  

#24 0x7ffbc88cfa61 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:499  

#25 0x7ffbc5abfc83 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:141  

#26 0x7ffbc82f0184 in content::GpuMain C:\b\s\w\ir\cache\builder\src\content\gpu\gpu\_main.cc:404  

#27 0x7ffbc15c0243 in content::RunOtherNamedProcessTypeMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:683

previously allocated by thread T0 here:  

#0 0x7ff634da23cb in malloc C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:98  

#1 0x7ffc120789fe in operator new d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\heap\new\_scalar.cpp:35  

#2 0x7ffc11c54b46 in rx::vk::DynamicBuffer::allocateNewBuffer C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\vk\_helpers.cpp:2388  

#3 0x7ffc11c5603a in rx::vk::DynamicBuffer::allocate C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\vk\_helpers.cpp:2459  

#4 0x7ffc11b126d2 in rx::ContextVk::allocateStreamedVertexBuffer C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\ContextVk.h:684  

#5 0x7ffc11af556e in rx::ContextVk::updateDefaultAttribute C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\ContextVk.cpp:5914  

#6 0x7ffc11ae34c8 in rx::ContextVk::handleDirtyGraphicsDefaultAttribs C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\ContextVk.cpp:1639  

#7 0x7ffc11aef372 in rx::ContextVk::setupDraw C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\ContextVk.cpp:1190  

#8 0x7ffc11af98bb in rx::ContextVk::drawArrays C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\ContextVk.cpp:2739  

#9 0x7ffc11391f69 in GL\_DrawArrays C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libGLESv2\entry\_points\_gles\_2\_0\_autogen.cpp:1109  

#10 0x7ffbd0ba6fb2 in gpu::gles2::GLES2DecoderPassthroughImpl::DoDrawArrays C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\gles2\_cmd\_decoder\_passthrough\_doers.cc:1217  

#11 0x7ffbcd0a64ad in gpu::gles2::GLES2DecoderPassthroughImpl::DoCommandsImpl<0> C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\gles2\_cmd\_decoder\_passthrough.cc:871  

#12 0x7ffbcd0a58f4 in gpu::gles2::GLES2DecoderPassthroughImpl::DoCommands C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\gles2\_cmd\_decoder\_passthrough.cc:809  

#13 0x7ffbc9f681b6 in gpu::CommandBufferService::Flush C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\command\_buffer\_service.cc:70  

#14 0x7ffbc73a7c5c in gpu::CommandBufferStub::OnAsyncFlush C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command\_buffer\_stub.cc:499  

#15 0x7ffbc73a6e36 in gpu::CommandBufferStub::ExecuteDeferredRequest C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command\_buffer\_stub.cc:151  

#16 0x7ffbc73b372f in gpu::GpuChannel::ExecuteDeferredRequest C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\gpu\_channel.cc:669  

#17 0x7ffbc73be595 in base::internal::Invoker<base::internal::BindState<void (gpu::GpuChannel::\*)(mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);)),base::WeakPtr[gpu::GpuChannel](javascript:void(0);),mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);) >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind\_internal.h:748  

#18 0x7ffbc6fd780c in gpu::Scheduler::RunNextTask C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\scheduler.cc:691  

#19 0x7ffbc5b40534 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:135  

#20 0x7ffbc88ce335 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:387  

#21 0x7ffbc88cd909 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:292  

#22 0x7ffbc88a6067 in base::MessagePumpDefault::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_default.cc:38  

#23 0x7ffbc88cfa61 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:499  

#24 0x7ffbc5abfc83 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:141  

#25 0x7ffbc82f0184 in content::GpuMain C:\b\s\w\ir\cache\builder\src\content\gpu\gpu\_main.cc:404  

#26 0x7ffbc15c0243 in content::RunOtherNamedProcessTypeMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:683  

#27 0x7ffbc15c1f67 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1043

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\vk\_helpers.cpp:4262 in rx::vk::BufferHelper::recordReadBarrier  

Shadow bytes around the buggy address:  

0x043ea09b56e0: 00 00 00 00 00 00 00 00 fa fa fa fa 00 00 00 00  

0x043ea09b56f0: 00 00 00 00 fa fa fa fa 00 00 00 00 00 00 00 00  

0x043ea09b5700: fa fa fa fa 00 00 00 00 00 00 00 00 fa fa fa fa  

0x043ea09b5710: 00 00 00 00 00 00 00 00 fa fa fa fa 00 00 00 00  

0x043ea09b5720: 00 00 00 00 fa fa fa fa fd fd fd fd fd fd fd fd  

=>0x043ea09b5730: fa fa fa fa fd fd fd fd[fd]fd fd fa fa fa fa fa  

0x043ea09b5740: 00 00 00 00 00 00 00 fa fa fa fa fa 00 00 00 00  

0x043ea09b5750: 00 00 00 fa fa fa fa fa 00 00 00 00 00 00 00 fa  

0x043ea09b5760: fa fa fa fa 00 00 00 00 00 00 00 fa fa fa fa fa  

0x043ea09b5770: 00 00 00 00 00 00 00 fa fa fa fa fa 00 00 00 00  

0x043ea09b5780: 00 00 00 fa fa fa fa fa 00 00 00 00 00 00 00 fa  

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

==4072==ABORTING  

[6284:6312:0211/143457.152:ERROR:gpu\_process\_host.cc(974)] GPU process exited unexpectedly: exit\_code=1

**CREDIT INFORMATION**  

Reporter credit: SeongHwan Park (SeHwa)

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 6.4 KB)

## Timeline

### [Deleted User] (2022-02-11)

[Empty comment from Monorail migration]

### cl...@chromium.org (2022-02-11)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5040857652461568.

### cl...@chromium.org (2022-02-11)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5827705727418368.

### cl...@chromium.org (2022-02-12)

[Empty comment from Monorail migration]

### cl...@chromium.org (2022-02-13)

[Empty comment from Monorail migration]

### ad...@google.com (2022-02-14)

ggabu423@ thanks for the report.

ClusterFuzz has found that this currently results in a null pointer deref, which of course we don't consider to be a security vulnerability. That was with Chrome head revision 970472. I don't know why that's different from the use-after-free you're seeing.

ClusterFuzz has also decided that this is a duplicate of https://crbug.com/chromium/1295411, which in turn it thought was a duplicate of https://crbug.com/chromium/1252274. I don't think it's making duplicate assessments correctly.

I'll try to run this on a Windows bot just in case that somehow changes timings and reveals a UaF here.

### cl...@chromium.org (2022-02-14)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6079425103593472.

### gg...@gmail.com (2022-02-14)

@adetaylor

I think that minimize task of 5827705727418368 is incorrect.
Before minimize task was performed, I saw the use-after-free log(the same I attached) in the crash stacktrace of 5827705727418368.
However, after the minimize task, the asan log was changed to null-deref.
(And I don't know why ClusterFuzz decided it was a duplicate, but this also seems to be wrong.)

### cl...@chromium.org (2022-02-14)

[Empty comment from Monorail migration]

### ad...@google.com (2022-02-14)

https://crbug.com/chromium/1296467#c8 - yeah that actually makes perfect sense. I already reported https://crbug.com/chromium/1297000 regarding ClusterFuzz's mistake here, but I hadn't realized that this was causing minimization errors.

### ad...@google.com (2022-02-14)

GPU process UaF reproduced manually on asan-linux-release-970659.

Not reproducible on asan-linux-release-950353 (M98 equivalent). Will test on a M99 build.

### [Deleted User] (2022-02-14)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-14)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2022-02-14)

Doesn't immediately reproduce on asan-linux-release-961656 so I think FoundIn-100 is correct. I'll assume the reporter's suspicion of the offending change is correct and send this to cclao@.

Assuming this affects all platforms other than iOS.

[Monorail components: Internals>GPU>Vulkan]

### ad...@google.com (2022-02-14)

[Empty comment from Monorail migration]

### gg...@gmail.com (2022-02-14)

https://crbug.com/chromium/1296467#c14 - Thanks :)  by the way, may I know why you removed the Type-Bug-Security label?

### ad...@google.com (2022-02-15)

Ha, due to finger trouble :)

ClusterFuzz has reproduced this on win_asan.

### [Deleted User] (2022-02-15)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cc...@google.com (2022-02-16)

I think what happened is that ContextVk::updateDefaultAttribute(size_t attribIndex) will always allocate space for the default attributes, regardless if the attribute index is enabled or not. Then it calls vertexArrayVk->updateDefaultAttrib(), which only updates mCurrentArrayBuffers[attribIndex] if it is enabled:    

if (!mState.getEnabledAttributesMask().test(attribIndex))
    {
        mCurrentArrayBufferHandles[attribIndex] = bufferHandle;
        mCurrentArrayBufferOffsets[attribIndex] = offset;
        mCurrentArrayBuffers[attribIndex]       = buffer;

        ANGLE_TRY(setDefaultPackedInput(contextVk, attribIndex));
    }

This means if mState.getEnabledAttributesMask().test(attribIndex)) is true, mCurrentArrayBuffers[attribIndex]  will still point to the previous buffer, which may have been pushed to mInflightBuffers by this call:

angle::Result ContextVk::updateDefaultAttribute(size_t attribIndex)
{
    vk::BufferHelper *defaultBuffer;
    ANGLE_TRY(allocateStreamedVertexBuffer(attribIndex, kDefaultValueSize, &defaultBuffer));
...
}

And then at submission time, we decided to release the mInflightBuffers, the BufferHelper object gets deleted (note, the underline VkBuffer will be garbage collected instead of immediately destroyed, but the helper object gets destructed), while mCurrentArrayBuffers still pointing to it, thus the use-after-free.

The easy fix is to add  `if (!mState.getEnabledAttributesMask().test(attribIndex))` check before calling allocateStreamedVertexBuffer() so that we do not waste time to allocate and not use it, and mean time fix this bug as well.




### gi...@appspot.gserviceaccount.com (2022-02-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/38723c28c0a5eb61ad70c5ac3dec12de438d8e11

commit 38723c28c0a5eb61ad70c5ac3dec12de438d8e11
Author: Charlie Lao <cclao@google.com>
Date: Wed Feb 16 00:29:36 2022

Vulkan: Allocate space for default attrib only if it is enabled

When context's default attributes is dirty, we allocate space for the
default attribute, regardless it is enabled or not. Then we call into
VertexArrayVk::updateDefaultAttrib() which only update its state if the
attribute is enabled. This causes a use-after-free scenario that if it
is disabled, the vertex array may have a pointer to the buffer that is
now becomes inflight which may gets deleted when DynamicBuffer code
think the size no longer matches etc.

Bug: chromium:1296467
Change-Id: Ib9ec8e60ebdb326f9bbfb215b3711c37631fce4b
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3466776
Reviewed-by: Jamie Madill <jmadill@chromium.org>
Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>
Commit-Queue: Charlie Lao <cclao@google.com>

[modify] https://crrev.com/38723c28c0a5eb61ad70c5ac3dec12de438d8e11/src/libANGLE/renderer/vulkan/VertexArrayVk.h
[modify] https://crrev.com/38723c28c0a5eb61ad70c5ac3dec12de438d8e11/src/libANGLE/renderer/vulkan/VertexArrayVk.cpp
[modify] https://crrev.com/38723c28c0a5eb61ad70c5ac3dec12de438d8e11/src/libANGLE/renderer/vulkan/ContextVk.h
[modify] https://crrev.com/38723c28c0a5eb61ad70c5ac3dec12de438d8e11/src/libANGLE/renderer/vulkan/ContextVk.cpp


### gi...@appspot.gserviceaccount.com (2022-02-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/75045d60794be3228325e49d5408db3518f31352

commit 75045d60794be3228325e49d5408db3518f31352
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Thu Feb 17 02:17:40 2022

Roll ANGLE from bfbe86613787 to 38723c28c0a5 (3 revisions)

https://chromium.googlesource.com/angle/angle.git/+log/bfbe86613787..38723c28c0a5

2022-02-16 cclao@google.com Vulkan: Allocate space for default attrib only if it is enabled
2022-02-16 kbr@chromium.org Refine suppression for GLSLTest.SwizzledChainedAssignIncrement.
2022-02-16 jmadill@chromium.org Vulkan: Add uniform descriptor set caching test.

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/angle-chromium-autoroll
Please CC cnorthrop@google.com on the revert to ensure that a human
is aware of the problem.

To file a bug in ANGLE: https://bugs.chromium.org/p/angleproject/issues/entry
To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86
Bug: chromium:1296467
Tbr: cnorthrop@google.com
Change-Id: I0a3cda20e397971337df4d266519d4e3df0ae8ed
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3470146
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#972228}

[modify] https://crrev.com/75045d60794be3228325e49d5408db3518f31352/DEPS


### gi...@appspot.gserviceaccount.com (2022-02-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/e7a5a1f72d4b254fc46ff4f05231f5f8249103e5

commit e7a5a1f72d4b254fc46ff4f05231f5f8249103e5
Author: Rushan Suleymanov <rushans@google.com>
Date: Thu Feb 17 13:29:00 2022

Revert "Roll ANGLE from bfbe86613787 to 38723c28c0a5 (3 revisions)"

This reverts commit 75045d60794be3228325e49d5408db3518f31352.

Reason for revert: it might cause test failures on Mac11 Tests (dbg)
This CL also reverts the following one: https://crrev.com/c/3471035.
> 2022-02-17 yuxinhu@google.com Add instructions to build RenderDoc for Android on Windows

Original change's description:
> Roll ANGLE from bfbe86613787 to 38723c28c0a5 (3 revisions)
>
> https://chromium.googlesource.com/angle/angle.git/+log/bfbe86613787..38723c28c0a5
>
> 2022-02-16 cclao@google.com Vulkan: Allocate space for default attrib only if it is enabled
> 2022-02-16 kbr@chromium.org Refine suppression for GLSLTest.SwizzledChainedAssignIncrement.
> 2022-02-16 jmadill@chromium.org Vulkan: Add uniform descriptor set caching test.
>
> If this roll has caused a breakage, revert this CL and stop the roller
> using the controls here:
> https://autoroll.skia.org/r/angle-chromium-autoroll
> Please CC cnorthrop@google.com on the revert to ensure that a human
> is aware of the problem.
>
> To file a bug in ANGLE: https://bugs.chromium.org/p/angleproject/issues/entry
> To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry
>
> To report a problem with the AutoRoller itself, please file a bug:
> https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug
>
> Documentation for the AutoRoller is here:
> https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md
>
> Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86
> Bug: chromium:1296467
> Tbr: cnorthrop@google.com
> Change-Id: I0a3cda20e397971337df4d266519d4e3df0ae8ed
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3470146
> Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
> Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
> Cr-Commit-Position: refs/heads/main@{#972228}

Bug: chromium:1296467,1298434
Change-Id: I1cfb88dffd7555990c622c225edf25c31720202a
Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3470401
Reviewed-by: Marc Treib <treib@chromium.org>
Reviewed-by: Victor Vianna <victorvianna@google.com>
Commit-Queue: Rushan Suleymanov <rushans@google.com>
Owners-Override: Rushan Suleymanov <rushans@google.com>
Cr-Commit-Position: refs/heads/main@{#972410}

[modify] https://crrev.com/e7a5a1f72d4b254fc46ff4f05231f5f8249103e5/DEPS


### gi...@appspot.gserviceaccount.com (2022-02-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/2017f88a67750c4d76f1c744d7a9f623071d7e22

commit 2017f88a67750c4d76f1c744d7a9f623071d7e22
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Thu Feb 17 21:01:33 2022

Roll ANGLE from bfbe86613787 to 8ade4c2f7ffd (9 revisions)

https://chromium.googlesource.com/angle/angle.git/+log/bfbe86613787..8ade4c2f7ffd

2022-02-17 jmadill@chromium.org Vulkan: Add overlay and stats for descriptor set caches.
2022-02-17 m.maiya@samsung.com Vulkan: Add a feature to retain SPIR-V debug info
2022-02-17 jmadill@chromium.org Vulkan: Refactor DynamicBuffer::allocate.
2022-02-17 jmadill@chromium.org Vulkan: Simplify SubAllocation data types.
2022-02-17 angle-autoroll@skia-public.iam.gserviceaccount.com Roll vulkan-deps from 9fb91023eb58 to 4d9fe6bf1f0c (8 revisions)
2022-02-17 yuxinhu@google.com Add instructions to build RenderDoc for Android on Windows
2022-02-16 cclao@google.com Vulkan: Allocate space for default attrib only if it is enabled
2022-02-16 kbr@chromium.org Refine suppression for GLSLTest.SwizzledChainedAssignIncrement.
2022-02-16 jmadill@chromium.org Vulkan: Add uniform descriptor set caching test.

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/angle-chromium-autoroll
Please CC cnorthrop@google.com on the revert to ensure that a human
is aware of the problem.

To file a bug in ANGLE: https://bugs.chromium.org/p/angleproject/issues/entry
To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86
Bug: chromium:1296467
Tbr: cnorthrop@google.com
Change-Id: I63b365c73bffbc99961820bbe38f4b0bd87caabd
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3472166
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#972618}

[modify] https://crrev.com/2017f88a67750c4d76f1c744d7a9f623071d7e22/DEPS


### go...@chromium.org (2022-03-01)

Reminder M100 is already branched and Stable promotion is coming soon. Please review this bug and assess if this is indeed a RBS. If not, please remove the RBS label. If so, please make sure to land the fix and request a merge into the release branch ASAP. Thank you.

### [Deleted User] (2022-03-02)

cclao: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cc...@google.com (2022-03-02)

This should already have been fixed. See https://crbug.com/chromium/1296467#c23, it appears already rolled into chromium. Let me know if my understanding is incorrect, or still seeing the bug.

### cc...@google.com (2022-03-02)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-02)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-02)

Not requesting merge to dev (M100) because latest trunk commit (972618) appears to be prior to dev branch point (972766). If this is incorrect, please replace the Merge-NA-100 label with Merge-Request-100. If other changes are required to fix this bug completely, please request a merge if necessary.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-03-03)

[Empty comment from Monorail migration]

### cl...@chromium.org (2022-03-09)

ClusterFuzz testcase 5827705727418368 is still reproducing on tip-of-tree build (trunk).

Please re-test your fix against this testcase and if the fix was incorrect or incomplete, please re-open the bug. Otherwise, ignore this notification and add the ClusterFuzz-Wrong label.

### cc...@google.com (2022-03-11)

This new testcase 5827705727418368 is completely different failure though. 


### am...@google.com (2022-03-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-03-11)

Congratulations on another one, SeongHwan! The VRP Panel has decided to award you $7,000 for this report. Thank you for your efforts and great work! 

### am...@google.com (2022-03-11)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-03-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/d4ddd0c1990d9ff0a20feeed36c6a7cf75f2745a

commit d4ddd0c1990d9ff0a20feeed36c6a7cf75f2745a
Author: Charlie Lao <cclao@google.com>
Date: Fri Mar 11 00:31:00 2022

Vulkan: Handle the case where the bound buffer is empty

If vertex attribute is enabled and buffer is bound, but buffer size is
0, we should not crash. This CL skips mapImpl and data copy all together
if size is 0 to avoid crash when calling mapImpl while buffer is
invalid.

This CL also added a test for this.

Bug: chromium:1296467
Change-Id: I79af348f133e1d3b4427f044e370652d0875dc91
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3516700
Reviewed-by: Amirali Abdolrashidi <abdolrashidi@google.com>
Reviewed-by: Jamie Madill <jmadill@chromium.org>
Commit-Queue: Charlie Lao <cclao@google.com>

[modify] https://crrev.com/d4ddd0c1990d9ff0a20feeed36c6a7cf75f2745a/src/libANGLE/renderer/vulkan/VertexArrayVk.cpp
[modify] https://crrev.com/d4ddd0c1990d9ff0a20feeed36c6a7cf75f2745a/src/tests/gl_tests/VertexAttributeTest.cpp
[modify] https://crrev.com/d4ddd0c1990d9ff0a20feeed36c6a7cf75f2745a/src/tests/angle_end2end_tests_expectations.txt


### gi...@appspot.gserviceaccount.com (2022-03-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/9b1219a869bd9b469bac758bc9f8463b1361b52e

commit 9b1219a869bd9b469bac758bc9f8463b1361b52e
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Thu Mar 17 00:45:04 2022

Roll ANGLE from 3739a195c2df to d867ddbbb1b8 (26 revisions)

https://chromium.googlesource.com/angle/angle.git/+log/3739a195c2df..d867ddbbb1b8

2022-03-16 m.maiya@samsung.com Doc: Update supported EGL minor version
2022-03-16 yuxinhu@google.com Revert "Flush the texture staged updates when destroying context share group"
2022-03-16 lubosz.sarnecki@collabora.com FrameCapture: Add override for Glsizei* types.
2022-03-16 antonio.caggiano@collabora.com Vulkan: VkFormat/DrmFourCC
2022-03-16 romanl@google.com angle_system_info_test also exports androidSdkLevel
2022-03-16 romanl@google.com angle_system_info_test passes json via file
2022-03-16 angle-autoroll@skia-public.iam.gserviceaccount.com Roll vulkan-deps from a11411926c31 to 51988dcdccbf (9 revisions)
2022-03-16 yahan@google.com Do not copy parent layer frame position
2022-03-15 cclao@google.com Vulkan: Update mCurrentElementArrayBuffersync based on dirty bit
2022-03-15 yuxinhu@google.com Flush the texture staged updates when destroying context share group
2022-03-15 b.schade@samsung.com Remove invalid validation check on compressed texture formats
2022-03-15 cclao@google.com Vulkan: Handle the case where the bound buffer is empty
2022-03-15 lubosz.sarnecki@collabora.com FrameCapture: Skip invalid VertexAttribPointer calls in MEC.
2022-03-15 antonio.caggiano@collabora.com Vulkan: VkFormat/DrmFourCC
2022-03-15 jmadill@chromium.org Vulkan: Temporarily suppress 3 perf counter tests on P6.
2022-03-15 jmadill@chromium.org Revert "Vulkan: VkFormat/DrmFourCC"
2022-03-15 lexa.knyazev@gmail.com Skip no-op base instance draw calls
2022-03-15 lexa.knyazev@gmail.com Fix typo in DrawElementsInstancedBaseVertexBaseInstanceANGLE
2022-03-15 angle-autoroll@skia-public.iam.gserviceaccount.com Roll Chromium from ffa866a5ae9e to 45902868a797 (562 revisions)
2022-03-15 b.schade@samsung.com Add usage of Spirv through glslang build flag
2022-03-14 kkinnunen@apple.com Add device id as a part of the key in EGLDisplay cache
2022-03-14 antonio.caggiano@collabora.com Vulkan: VkFormat/DrmFourCC
2022-03-14 angle-autoroll@skia-public.iam.gserviceaccount.com Roll vulkan-deps from 2d9abfbddc1b to a11411926c31 (18 revisions)
2022-03-14 jmadill@chromium.org Fix crash when pausing XFB then deleting a buffer.
2022-03-14 cclao@google.com Vulkan: Fix another corner case of mCurrentElementArrayBuffer
2022-03-14 angle-autoroll@skia-public.iam.gserviceaccount.com Roll VK-GL-CTS from f7e842466e0a to 8252a3d3cdd3 (8 revisions)

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/angle-chromium-autoroll
Please CC jmadill@google.com on the revert to ensure that a human
is aware of the problem.

To file a bug in ANGLE: https://bugs.chromium.org/p/angleproject/issues/entry
To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86
Bug: chromium:1296467,chromium:1299211,chromium:1299261,chromium:1305190
Tbr: jmadill@google.com
Test: Test: angle_end2end_tests --gtest_filter="VertexAttributeTestES3.InvalidAttribPointer/*"
Test: Test: capture_replay_tests.py --gtest_filter=FenceSyncTest.NullLength/*
Test: Test: gtest_filter=*DXT1CompressedTextureTest.NonBlockSizesMipLevels*
Test: Test: when using ANGLE (with metal or swiftshader backend) with
Change-Id: I52ffe787d20dd083af8efe1bdef05616ac611f55
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3530116
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#981945}

[modify] https://crrev.com/9b1219a869bd9b469bac758bc9f8463b1361b52e/DEPS


### [Deleted User] (2022-06-09)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-06-10)

Hello, SeongHwan- we consider attachments/pocs included with reports to be an integral part of the report, so I've un-deleted the deleted POC. Thank you! 

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1296467?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058750)*
