# Crash in vk::ImageView::clear

| Field | Value |
|-------|-------|
| **Issue ID** | [40062792](https://issues.chromium.org/issues/40062792) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU>SwiftShader |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ne...@nesk.kr |
| **Assignee** | ge...@chromium.org |
| **Created** | 2023-01-25 |
| **Bounty** | $15,000.00 |

## Description

**VULNERABILITY DETAILS**

=================================================================  

==11336==ERROR: AddressSanitizer: access-violation on unknown address 0x120fd6b63000 (pc 0x7ffe3749107f bp 0x001485fff500 sp 0x001485fff450 T27)  

==11336==The signal is caused by a WRITE memory access.  

==11336==WARNING: Failed to use and restart external symbolizer!  

#0 0x7ffe3749107e in sw::clear C:\b\s\w\ir\cache\builder\src\third\_party\swiftshader\src\System\Memory.cpp:144  

#1 0x7ffe37181008 in sw::Blitter::fastClear C:\b\s\w\ir\cache\builder\src\third\_party\swiftshader\src\Device\Blitter.cpp:293  

#2 0x7ffe3717f324 in sw::Blitter::clear C:\b\s\w\ir\cache\builder\src\third\_party\swiftshader\src\Device\Blitter.cpp:88  

#3 0x7ffe37106342 in vk::Image::clear C:\b\s\w\ir\cache\builder\src\third\_party\swiftshader\src\Vulkan\VkImage.cpp:1088  

#4 0x7ffe3710a245 in vk::ImageView::clear C:\b\s\w\ir\cache\builder\src\third\_party\swiftshader\src\Vulkan\VkImageView.cpp:216  

#5 0x7ffe370f18dd in vk::Framebuffer::executeLoadOp C:\b\s\w\ir\cache\builder\src\third\_party\swiftshader\src\Vulkan\VkFramebuffer.cpp:126  

#6 0x7ffe370cdac6 in `anonymous namespace'::CmdBeginRenderPass::execute C:\b\s\w\ir\cache\builder\src\third\_party\swiftshader\src\Vulkan\VkCommandBuffer.cpp:87  

#7 0x7ffe370cc8a0 in vk::CommandBuffer::submit C:\b\s\w\ir\cache\builder\src\third\_party\swiftshader\src\Vulkan\VkCommandBuffer.cpp:2330  

#8 0x7ffe37126bfd in vk::Queue::submitQueue C:\b\s\w\ir\cache\builder\src\third\_party\swiftshader\src\Vulkan\VkQueue.cpp:104  

#9 0x7ffe37125a75 in vk::Queue::taskLoop C:\b\s\w\ir\cache\builder\src\third\_party\swiftshader\src\Vulkan\VkQueue.cpp:156  

#10 0x7ffe3712871a in std::Cr::\_\_thread\_proxy<std::Cr::tuple<std::Cr::unique\_ptr<std::Cr::\_\_thread\_struct,std::Cr::default\_delete[std::Cr::\_\_thread\_struct](javascript:void(0);) >,void (vk::Queue::\*)(marl::Scheduler \*),vk::Queue \*,marl::Scheduler \*> > C:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\thread:293  

#11 0x7ffe37b15ab5 in thread\_start<unsigned int (\_\_cdecl\*)(void \*),1> C:\b\s\w\ir\cache\builder\src\out\Release\_x64\minkernel\crts\ucrt\src\appcrt\startup\thread.cpp:97  

#12 0x7ff6423dcb13 in \_\_asan::AsanThread::ThreadStart C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_thread.cpp:277  

#13 0x7ffe83747613 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x180017613)  

#14 0x7ffe849026a0 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x1800526a0)

AddressSanitizer can not provide additional info.  

SUMMARY: AddressSanitizer: access-violation C:\b\s\w\ir\cache\builder\src\third\_party\swiftshader\src\System\Memory.cpp:144 in sw::clear  

Thread T27 created by T20 here:  

#0 0x7ff6423dd6d2 in \_\_asan\_wrap\_CreateThread C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_win.cpp:146  

#1 0x7ffe37b15982 in \_beginthreadex C:\b\s\w\ir\cache\builder\src\out\Release\_x64\minkernel\crts\ucrt\src\appcrt\startup\thread.cpp:209  

#2 0x7ffe376e8781 in std::Cr::\_\_libcpp\_thread\_create C:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\src\support\win32\thread\_win32.cpp:203  

#3 0x7ffe37125d7e in std::Cr::thread::thread<void (vk::Queue::\*)(marl::Scheduler \*),vk::Queue \*,marl::Scheduler \*&,void> C:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\thread:309  

#4 0x7ffe371257b2 in vk::Queue::Queue C:\b\s\w\ir\cache\builder\src\third\_party\swiftshader\src\Vulkan\VkQueue.cpp:38  

#5 0x7ffe370ddaf1 in vk::Device::Device C:\b\s\w\ir\cache\builder\src\third\_party\swiftshader\src\Vulkan\VkDevice.cpp:139  

#6 0x7ffe3713df70 in vk::DispatchableObject<vk::Device,VkDevice\_T \*>::Create<VkDeviceCreateInfo,vk::PhysicalDevice \*,const VkPhysicalDeviceFeatures \*,std::Cr::shared\_ptr[marl::Scheduler](javascript:void(0);) > C:\b\s\w\ir\cache\builder\src\third\_party\swiftshader\src\Vulkan\VkObject.hpp:147  

#7 0x7ffe3713d8d1 in vkCreateDevice C:\b\s\w\ir\cache\builder\src\third\_party\swiftshader\src\Vulkan\libVulkan.cpp:1183  

#8 0x7ffe4bfd620d in terminator\_CreateDevice C:\b\s\w\ir\cache\builder\src\third\_party\vulkan-deps\vulkan-loader\src\loader\loader.c:5796  

#9 0x7ffe4bfd0025 in loader\_create\_device\_chain C:\b\s\w\ir\cache\builder\src\third\_party\vulkan-deps\vulkan-loader\src\loader\loader.c:4953  

#10 0x7ffe4bfce943 in loader\_layer\_create\_device C:\b\s\w\ir\cache\builder\src\third\_party\vulkan-deps\vulkan-loader\src\loader\loader.c:4370  

#11 0x7ffe4bfe4f1d in vkCreateDevice C:\b\s\w\ir\cache\builder\src\third\_party\vulkan-deps\vulkan-loader\src\loader\trampoline.c:842  

#12 0x7ffe4648139d in rx::RendererVk::initializeDevice C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\RendererVk.cpp:2985  

#13 0x7ffe46479ad4 in rx::RendererVk::initialize C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\RendererVk.cpp:1819  

#14 0x7ffe46401f5a in rx::DisplayVk::initialize C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\DisplayVk.cpp:130  

#15 0x7ffe46626200 in rx::DisplayVkWin32::initialize C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\renderer\vulkan\win32\DisplayVkWin32.cpp:62  

#16 0x7ffe467601af in egl::Display::initialize C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\Display.cpp:1010  

#17 0x7ffe46341968 in egl::Initialize C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libGLESv2\egl\_stubs.cpp:461  

#18 0x7ffe4634941c in EGL\_Initialize C:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libGLESv2\entry\_points\_egl\_autogen.cpp:373  

#19 0x7ffe08c6b86b in gl::GLDisplayEGL::InitializeDisplay C:\b\s\w\ir\cache\builder\src\ui\gl\gl\_display.cc:722  

#20 0x7ffe08c69c1f in gl::GLDisplayEGL::Initialize C:\b\s\w\ir\cache\builder\src\ui\gl\gl\_display.cc:627  

#21 0x7ffe0c9a5cd1 in gl::init::InitializeDisplay C:\b\s\w\ir\cache\builder\src\ui\gl\init\gl\_display\_initializer.cc:261  

#22 0x7ffe08c5eccd in gl::init::InitializeGLOneOffPlatform C:\b\s\w\ir\cache\builder\src\ui\gl\init\gl\_initializer\_win.cc:133  

#23 0x7ffe05b1f1c2 in gl::init::InitializeGLOneOffPlatformImplementation C:\b\s\w\ir\cache\builder\src\ui\gl\init\gl\_factory.cc:219  

#24 0x7ffe05b1e9a9 in gl::init::`anonymous namespace'::InitializeGLOneOffPlatformHelper C:\b\s\w\ir\cache\builder\src\ui\gl\init\gl_factory.cc:143 #25 0x7ffe05b1ed67 in gl::init::InitializeGLNoExtensionsOneOff C:\b\s\w\ir\cache\builder\src\ui\gl\init\gl_factory.cc:174 #26 0x7ffe0650d66e in gpu::GpuInit::InitializeInProcess C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\gpu_init.cc:867 #27 0x7ffe0727ac2c in content::InProcessGpuThread::Init C:\b\s\w\ir\cache\builder\src\content\gpu\in_process_gpu_thread.cc:63 #28 0x7ffe04805f3d in base::Thread::ThreadMain C:\b\s\w\ir\cache\builder\src\base\threading\thread.cc:403 #29 0x7ffe04885dc1 in base::`anonymous namespace'::ThreadFunc C:\b\s\w\ir\cache\builder\src\base\threading\platform\_thread\_win.cc:127  

#30 0x7ff6423dcb13 in \_\_asan::AsanThread::ThreadStart C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_thread.cpp:277  

#31 0x7ffe83747613 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x180017613)  

#32 0x7ffe849026a0 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x1800526a0)

Thread T20 created by T0 here:  

#0 0x7ff6423dd6d2 in \_\_asan\_wrap\_CreateThread C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_win.cpp:146  

#1 0x7ffe04884b2f in base::`anonymous namespace'::CreateThreadInternal C:\b\s\w\ir\cache\builder\src\base\threading\platform\_thread\_win.cc:192  

#2 0x7ffe04804cc2 in base::Thread::StartWithOptions C:\b\s\w\ir\cache\builder\src\base\threading\thread.cc:217  

#3 0x7ffdff10bf19 in content::GpuProcessHost::Init C:\b\s\w\ir\cache\builder\src\content\browser\gpu\gpu\_process\_host.cc:897  

#4 0x7ffdff10afb5 in content::GpuProcessHost::Get C:\b\s\w\ir\cache\builder\src\content\browser\gpu\gpu\_process\_host.cc:592  

#5 0x7ffdff0cb5ec in content::BrowserGpuChannelHostFactory::EstablishRequest::Establish C:\b\s\w\ir\cache\builder\src\content\browser\gpu\browser\_gpu\_channel\_host\_factory.cc:163  

#6 0x7ffdff0cafe1 in content::BrowserGpuChannelHostFactory::EstablishRequest::Create C:\b\s\w\ir\cache\builder\src\content\browser\gpu\browser\_gpu\_channel\_host\_factory.cc:133  

#7 0x7ffdff0cdbb8 in content::BrowserGpuChannelHostFactory::EstablishGpuChannel C:\b\s\w\ir\cache\builder\src\content\browser\gpu\browser\_gpu\_channel\_host\_factory.cc:377  

#8 0x7ffdff0cd4a3 in content::BrowserGpuChannelHostFactory::EstablishGpuChannel C:\b\s\w\ir\cache\builder\src\content\browser\gpu\browser\_gpu\_channel\_host\_factory.cc:317  

#9 0x7ffdff0cce7e in content::BrowserGpuChannelHostFactory::Initialize C:\b\s\w\ir\cache\builder\src\content\browser\gpu\browser\_gpu\_channel\_host\_factory.cc:266  

#10 0x7ffdfeb17f46 in content::BrowserMainLoop::PostCreateThreadsImpl C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_loop.cc:1307  

#11 0x7ffdfeb16f63 in content::BrowserMainLoop::PostCreateThreads C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_loop.cc:956  

#12 0x7ffdfeb1e244 in base::internal::Invoker<base::internal::BindState<int (content::BrowserMainLoop::\*)(),base::internal::UnretainedWrapper[content::BrowserMainLoop,base::unretained\_traits::MayNotDangle](javascript:void(0);) >,int ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind\_internal.h:970  

#13 0x7ffdffed6c60 in content::StartupTaskRunner::RunAllTasksNow C:\b\s\w\ir\cache\builder\src\content\browser\startup\_task\_runner.cc:44  

#14 0x7ffdfeb162ae in content::BrowserMainLoop::CreateStartupTasks C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_loop.cc:883  

#15 0x7ffdfeb206b0 in content::BrowserMainRunnerImpl::Initialize C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_runner\_impl.cc:141  

#16 0x7ffdfeb11d4f in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main.cc:28  

#17 0x7ffe02fa177d in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:715  

#18 0x7ffe02fa5505 in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1263  

#19 0x7ffe02fa4c16 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1117  

#20 0x7ffe02f9f6b8 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:324  

#21 0x7ffe02fa05a8 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:352  

#22 0x7ffdf744168c in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc:180  

#23 0x7ff642326378 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main\_dll\_loader\_win.cc:166  

#24 0x7ff642322bb1 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_exe\_main\_win.cc:391  

#25 0x7ff64278e42b in \_\_scrt\_common\_main\_seh d:\a01\_work\12\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#26 0x7ffe83747613 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x180017613)  

#27 0x7ffe849026a0 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x1800526a0)

==11336==ADDITIONAL INFO

==11336==Note: Please include this section with the ASan report.  

Task trace:

==11336==END OF ADDITIONAL INFO  

==11336==ABORTING

**VERSION**  

Chrome Version: [111.0.5560.0] + [DevBuild + ASan]  

Operating System: [Windows 10]

**REPRODUCTION CASE**  

I am trying to minimize testcase will upload it later.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: GPU Process  

Crash State: See asan.log

## Attachments

- [asan1.log](attachments/asan1.log) (text/plain, 11.1 KB)
- [asan2.log](attachments/asan2.log) (text/plain, 10.9 KB)
- [poc.html](attachments/poc.html) (text/plain, 1.9 KB)
- [windbg.log](attachments/windbg.log) (text/plain, 11.7 KB)
- [asan3.log](attachments/asan3.log) (text/plain, 11.1 KB)
- [asan4.log](attachments/asan4.log) (text/plain, 11.2 KB)

## Timeline

### [Deleted User] (2023-01-25)

[Empty comment from Monorail migration]

### rs...@chromium.org (2023-01-25)

Please provide the PoC / steps to reproduce in order for us to triage this.

[Monorail components: Internals>GPU>SwiftShader]

### ne...@nesk.kr (2023-01-26)

I've attached a minimized testcase.

when testing in chrome, the following parameters are required to use the swiftshader renderer.

```
asan-win32-release_x64-1096728\chrome.exe --no-sandbox --single-process --disable-gpu poc.html
```

### [Deleted User] (2023-01-26)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ne...@nesk.kr (2023-01-26)

It seems that the crash occurs because the size of the buffer "d" is smaller than the last parameter of sw::clear.

The area.extent.width is controllable, it is the width size of the canvas.

```
bool Blitter::fastClear(const void *clearValue, vk::Format clearFormat, vk::Image *dest, const vk::Format &viewFormat, const VkImageSubresourceRange &subresourceRange, const VkRect2D *renderArea)
{
...
			uint8_t *d = slice;

			switch(viewFormat.bytes())
			{
			case 4:
				for(uint32_t i = 0; i < area.extent.height; i++)
				{
					ASSERT(d < dest->end());
					sw::clear((uint32_t *)d, packed, area.extent.width);  // [1]
```

sw::clear works like memset, possible heap overflow (or oob write) caused by count exceeding buffer size.

```
void clear(uint32_t *memory, uint32_t element, size_t count)
{
#if defined(_MSC_VER) && defined(__x86__) && !defined(MEMORY_SANITIZER)
	__stosd((unsigned long *)memory, element, count);					  // [2]
#elif defined(__GNUC__) && defined(__x86__) && !defined(MEMORY_SANITIZER)
	__asm__ __volatile__("rep stosl"
	                     : "+D"(memory), "+c"(count)
	                     : "a"(element)
	                     : "memory");
#else
	for(size_t i = 0; i < count; i++)
	{
		memory[i] = element;
	}
#endif
}
```

[1] https://swiftshader.googlesource.com/SwiftShader/+/dd7bb92b9a7a813ebc2da9fe3f6484c34cc69363/src/Device/Blitter.cpp#293
[2] https://swiftshader.googlesource.com/SwiftShader/+/dd7bb92b9a7a813ebc2da9fe3f6484c34cc69363/src/System/Memory.cpp#144

### ne...@nesk.kr (2023-01-26)

also reproduced in stable. see the debugger log above.

109.0.5414.120 (Official Build) (64-bit)

### rs...@chromium.org (2023-01-26)

Thanks for the PoC and additional details in c#5.

### rs...@chromium.org (2023-01-26)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-01-26)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6237629350871040.

### [Deleted User] (2023-01-26)

[Empty comment from Monorail migration]

### su...@chromium.org (2023-01-26)

Hi rsesek@, I'm no longer in the SwiftShader team, delegating to geofflang@ for triaging.

### cl...@chromium.org (2023-01-27)

Detailed Report: https://clusterfuzz.com/testcase?key=6237629350871040

Fuzzer: None
Job Type: windows_asan_chrome
Platform Id: windows

Crash Type: UNKNOWN WRITE
Crash Address: 0x12bae3be2000
Crash State:
  sw::clear
  sw::Blitter::fastClear
  sw::Blitter::clear
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=windows_asan_chrome&range=1049421:1049459

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6237629350871040



### [Deleted User] (2023-01-27)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ne...@nesk.kr (2023-01-30)

I think the root cause of the bug is related to the following codes.

```c++
bool Blitter::fastClear(const void *clearValue, vk::Format clearFormat, vk::Image *dest, const vk::Format &viewFormat, const VkImageSubresourceRange &subresourceRange, const VkRect2D *renderArea)
{
...
		uint8_t *slice = (uint8_t *)dest->getTexelPointer(								// [3]
			{ area.offset.x, area.offset.y, static_cast<int32_t>(depth) }, subres);

		for(int j = 0; j < dest->getSampleCount(); j++)
		{
			uint8_t *d = slice;

			switch(viewFormat.bytes())
			{
			case 4:
				for(uint32_t i = 0; i < area.extent.height; i++)						// [1]
				{
					ASSERT(d < dest->end());
					sw::clear((uint32_t *)d, packed, area.extent.width);
					d += rowPitchBytes;													// [2]
				}
				break;
			}
		}
```

The reason the buffer bounds overflow is because of the area.extent.height of the for loop. [1]

```
gl.renderbufferStorage(gl.RENDERBUFFER, gl.RG8UI, 1304, 2041);
```

This value comes from the last parameter of the gl.renderbufferStorage in poc.

The rowPitchBytes is calculated through the Image::rowPitchBytes method, and this value was 0x4b0 when debugging. [2]

```
const VkMemoryRequirements Image::getMemoryRequirements() const
{
	VkMemoryRequirements memoryRequirements;
	memoryRequirements.alignment = vk::MEMORY_REQUIREMENTS_OFFSET_ALIGNMENT;
	memoryRequirements.memoryTypeBits = vk::MEMORY_TYPE_GENERIC_BIT;
	memoryRequirements.size = getStorageSize(format.getAspects()) +
	                          (decompressedImage ? decompressedImage->getStorageSize(decompressedImage->format.getAspects()) : 0);
	return memoryRequirements;
}
```

The size of buffer "d" is allocated by ImageHelper::initMemory during gl::Context::renderbufferStorageMultisample runs. [3]

In my debugging environment, the size of the buffer was 0xafc8f, but since the loop count is up to 2041, overflow occurs when i reaches over than buffer size.

```
1354 (i) * 0x4b0 (rowPitchBytes) == 0x18cae0 > 0xafc8f

0:003> p
Time Travel Position: 24279:1551
rax=0000000000000000 rbx=000000000002bf20 rcx=000002b1538f0be0
rdx=0000000000000000 rsi=0000000000000000 rdi=00000000000002af		<< rdi == i, 0x7f9 - 0x2af = 1354
rip=00007ffe4acb1849 rsp=000000e8271feb80 rbp=000002b1538f0be0
 r8=000000000000012c  r9=0000000000000000 r10=000000000000012c
r11=0000000000000001 r12=000002b153764100 r13=00000000000004b0
r14=0000000000000000 r15=000000000000012c
iopl=0         nv up ei pl nz ac po nc
cs=0033  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00000216
vk_swiftshader!sw::Blitter::fastClear+0x539:
00007ffe`4acb1849 e8e22a1300      call    vk_swiftshader!sw::clear (00007ffe`4ade4330)
```

[1] https://swiftshader.googlesource.com/SwiftShader/+/dd7bb92b9a7a813ebc2da9fe3f6484c34cc69363/src/Device/Blitter.cpp#290
[2] https://swiftshader.googlesource.com/SwiftShader/+/dd7bb92b9a7a813ebc2da9fe3f6484c34cc69363/src/Device/Blitter.cpp#263
[3] https://swiftshader.googlesource.com/SwiftShader/+/dd7bb92b9a7a813ebc2da9fe3f6484c34cc69363/src/Vulkan/VkImage.cpp#226

### ja...@chromium.org (2023-02-06)

[security marshal] Thanks for the additional information nesk@. I'll ping geofflang@ to take a look and add an update.

### [Deleted User] (2023-02-08)

geofflang: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cl...@chromium.org (2023-02-16)

ClusterFuzz testcase 6237629350871040 is verified as fixed in https://clusterfuzz.com/revisions?job=windows_asan_chrome&range=1105736:1105779

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### [Deleted User] (2023-02-16)

[Empty comment from Monorail migration]

### ne...@nesk.kr (2023-02-17)

That's weird. I'm still seeing crashes in r1105661 and r1106610.

### [Deleted User] (2023-02-17)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-17)

This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M110. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M111. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [110, 111].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-02-18)

This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M110. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M111. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [110, 111].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-02-20)

This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M110. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M111. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [110, 111].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-02-21)

Reopening for Swiftshader folks to PTAL based on https://crbug.com/chromium/1410191#c19 reports this issue can still be reproduced. 
Removing merge-111 label as no fix was landed here so removing for M111 merge approval queue. 

### [Deleted User] (2023-02-22)

geofflang: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cl...@chromium.org (2023-02-23)

Detailed Report: https://clusterfuzz.com/testcase?key=6551557591203840

Fuzzer: None
Job Type: windows_asan_chrome
Platform Id: windows

Crash Type: UNKNOWN WRITE
Crash Address: 0x123c22752000
Crash State:
  vk::ImageView::clear
  vk::Framebuffer::executeLoadOp
  CmdBeginRenderPass::execute
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Crash Revision: https://clusterfuzz.com/revisions?job=windows_asan_chrome&revision=1108675

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6551557591203840



### am...@chromium.org (2023-02-23)

reassigning to sugoi@ for attention (since capn@ is no longer working on swiftshader/vulkan), can you PTAL and help re-assign if needed? 
I'm able to still repro this issue and got CF to confirm. TY. 

### am...@chromium.org (2023-02-23)

[Empty comment from Monorail migration]

### su...@chromium.org (2023-02-23)

I'm also no longer working on SwiftShader. Re-assigning to geofflang@ for triage.

### am...@chromium.org (2023-02-23)

[Empty comment from Monorail migration]

### pg...@google.com (2023-02-23)

removing the other merge label that is not applicable since the issue still reproduces (see https://crbug.com/chromium/1410191#c24)

### [Deleted User] (2023-02-23)

[Empty comment from Monorail migration]

### ne...@nesk.kr (2023-03-17)

[Comment Deleted]

### ge...@chromium.org (2023-03-17)

I should have time to look next week.

### ti...@google.com (2023-03-20)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-03-20)

ClusterFuzz testcase 5625731783262208 appears to be flaky, updating reproducibility label.

### ne...@nesk.kr (2023-03-21)

the bug is still reproducible in r1119751 (113.0.5666.0)

### [Deleted User] (2023-03-26)

We commit ourselves to a 60 day deadline for fixing for high severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ge...@chromium.org (2023-03-27)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-03-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/c6ec59dcae7d56c93afddc764aa7979b23d53dac

commit c6ec59dcae7d56c93afddc764aa7979b23d53dac
Author: Geoff Lang <geofflang@chromium.org>
Date: Mon Mar 27 15:15:48 2023

Explicitly pass the extended dirty bits to syncState.

Add a the extended dirty bits and bit mask to syncState instead of
calling gl::State::getAndResetExtendedDirtyBits when encountering
DIRTY_BIT_EXTENDED. It disallowed us from masking the extended dirty
bits and feels like an anti-pattern to modify the extended dirty bits
in gl::State from the backend.

This is a refactor only.

Bug: chromium:1410191
Change-Id: I66fdec3eb57e3426cf0fda9ccb759700eafdda14
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/4374100
Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>
Reviewed-by: Yuxin Hu <yuxinhu@google.com>

[modify] https://crrev.com/c6ec59dcae7d56c93afddc764aa7979b23d53dac/src/libANGLE/renderer/d3d/d3d11/StateManager11.h
[modify] https://crrev.com/c6ec59dcae7d56c93afddc764aa7979b23d53dac/src/libANGLE/renderer/d3d/d3d9/StateManager9.h
[modify] https://crrev.com/c6ec59dcae7d56c93afddc764aa7979b23d53dac/src/libANGLE/renderer/d3d/d3d9/Context9.cpp
[modify] https://crrev.com/c6ec59dcae7d56c93afddc764aa7979b23d53dac/src/libANGLE/renderer/d3d/d3d11/StateManager11.cpp
[modify] https://crrev.com/c6ec59dcae7d56c93afddc764aa7979b23d53dac/src/libANGLE/Context.cpp
[modify] https://crrev.com/c6ec59dcae7d56c93afddc764aa7979b23d53dac/src/libANGLE/renderer/gl/StateManagerGL.cpp
[modify] https://crrev.com/c6ec59dcae7d56c93afddc764aa7979b23d53dac/src/libANGLE/State.cpp
[modify] https://crrev.com/c6ec59dcae7d56c93afddc764aa7979b23d53dac/src/libANGLE/renderer/metal/ContextMtl.h
[modify] https://crrev.com/c6ec59dcae7d56c93afddc764aa7979b23d53dac/src/libANGLE/Context.h
[modify] https://crrev.com/c6ec59dcae7d56c93afddc764aa7979b23d53dac/src/libANGLE/State.h
[modify] https://crrev.com/c6ec59dcae7d56c93afddc764aa7979b23d53dac/src/libANGLE/renderer/vulkan/ContextVk.h
[modify] https://crrev.com/c6ec59dcae7d56c93afddc764aa7979b23d53dac/src/libANGLE/renderer/d3d/d3d11/Context11.h
[modify] https://crrev.com/c6ec59dcae7d56c93afddc764aa7979b23d53dac/src/libANGLE/renderer/d3d/d3d9/StateManager9.cpp
[modify] https://crrev.com/c6ec59dcae7d56c93afddc764aa7979b23d53dac/src/libANGLE/Context.inl.h
[modify] https://crrev.com/c6ec59dcae7d56c93afddc764aa7979b23d53dac/src/libANGLE/renderer/d3d/d3d11/Context11.cpp
[modify] https://crrev.com/c6ec59dcae7d56c93afddc764aa7979b23d53dac/src/libANGLE/renderer/metal/ContextMtl.mm
[modify] https://crrev.com/c6ec59dcae7d56c93afddc764aa7979b23d53dac/src/libANGLE/renderer/gl/ContextGL.cpp
[modify] https://crrev.com/c6ec59dcae7d56c93afddc764aa7979b23d53dac/src/libANGLE/renderer/ContextImpl.h
[modify] https://crrev.com/c6ec59dcae7d56c93afddc764aa7979b23d53dac/src/libANGLE/renderer/null/ContextNULL.cpp
[modify] https://crrev.com/c6ec59dcae7d56c93afddc764aa7979b23d53dac/src/libANGLE/renderer/gl/StateManagerGL.h
[modify] https://crrev.com/c6ec59dcae7d56c93afddc764aa7979b23d53dac/src/libANGLE/renderer/null/ContextNULL.h
[modify] https://crrev.com/c6ec59dcae7d56c93afddc764aa7979b23d53dac/src/libANGLE/renderer/gl/ContextGL.h
[modify] https://crrev.com/c6ec59dcae7d56c93afddc764aa7979b23d53dac/src/libANGLE/renderer/vulkan/ContextVk.cpp
[modify] https://crrev.com/c6ec59dcae7d56c93afddc764aa7979b23d53dac/src/libANGLE/renderer/d3d/d3d9/Context9.h


### gi...@appspot.gserviceaccount.com (2023-03-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/642d7662be10c8cd7a1000c3a24c0acaf0dcdda9

commit 642d7662be10c8cd7a1000c3a24c0acaf0dcdda9
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Tue Mar 28 18:26:40 2023

Roll ANGLE from fc7cb00e9947 to c6ec59dcae7d (1 revision)

https://chromium.googlesource.com/angle/angle.git/+log/fc7cb00e9947..c6ec59dcae7d

2023-03-28 geofflang@chromium.org Explicitly pass the extended dirty bits to syncState.

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/angle-chromium-autoroll
Please CC angle-team@google.com,geofflang@google.com on the revert to ensure that a human
is aware of the problem.

To file a bug in ANGLE: https://bugs.chromium.org/p/angleproject/issues/entry
To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86
Bug: chromium:1410191
Tbr: geofflang@google.com
Change-Id: Ie784a9b505a2e577f3be7a08a6aa101d521dfe11
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4375915
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#1123167}

[modify] https://crrev.com/642d7662be10c8cd7a1000c3a24c0acaf0dcdda9/DEPS


### gi...@appspot.gserviceaccount.com (2023-03-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/da7dd31f27e1c547bb1fbb90cb2f10ccf4474f19

commit da7dd31f27e1c547bb1fbb90cb2f10ccf4474f19
Author: Geoff Lang <geofflang@chromium.org>
Date: Mon Mar 27 15:29:10 2023

GL: Disable extended dirty bit states for internal blits.

New GL states have been added to the GL backend and not updated in
ScopedGLState which is used to reset internal state for blits. This
caused test failures when tests were run in specific orders. Ex:

ClipDistanceTest.ThreeClipDistancesRedeclared/ES2_OpenGL:CopyTextureVariationsTest.CopySubTexture/ES2_OpenGL__AToBGRAFlipYUnmultiplyAlpha

Bug: angleproject:5160
Bug: chromium:1410191
Change-Id: I805e39bc8c4c7d7d843b43fdc7813dd668919e8a
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/4374101
Reviewed-by: Peng Huang <penghuang@chromium.org>

[modify] https://crrev.com/da7dd31f27e1c547bb1fbb90cb2f10ccf4474f19/src/libANGLE/renderer/gl/BlitGL.cpp


### gi...@appspot.gserviceaccount.com (2023-03-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/f575e23055dba7cba47a3ad138dd9c7afb1a1293

commit f575e23055dba7cba47a3ad138dd9c7afb1a1293
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Wed Mar 29 16:03:01 2023

Roll ANGLE from 21ffb23a58c8 to da7dd31f27e1 (1 revision)

https://chromium.googlesource.com/angle/angle.git/+log/21ffb23a58c8..da7dd31f27e1

2023-03-29 geofflang@chromium.org GL: Disable extended dirty bit states for internal blits.

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/angle-chromium-autoroll
Please CC angle-team@google.com,geofflang@google.com on the revert to ensure that a human
is aware of the problem.

To file a bug in ANGLE: https://bugs.chromium.org/p/angleproject/issues/entry
To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86
Bug: chromium:1410191
Tbr: geofflang@google.com
Change-Id: Ia5c74517c82d6f6794124d9b3a308f09ab948008
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4380823
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#1123624}

[modify] https://crrev.com/f575e23055dba7cba47a3ad138dd9c7afb1a1293/DEPS


### gi...@appspot.gserviceaccount.com (2023-03-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/bb15ceefd9ba0685723c20dedada6a74edc6d41f

commit bb15ceefd9ba0685723c20dedada6a74edc6d41f
Author: Geoff Lang <geofflang@chromium.org>
Date: Mon Mar 27 15:32:30 2023

Remove syncing of extended dirty bits for TexImage calls.

All extended dirty bits were synced for glTexImage calls but many of
them required valid GL state or a complete framebuffer. This caused
errors in the Vulkan backend when we would read and write out of
bounds of the framebuffer due to an incorrect render area.

Bug: chromium:1410191
Change-Id: I17f156f71ded72761b631ef9842b048a9173c9b7
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/4374102
Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>

[modify] https://crrev.com/bb15ceefd9ba0685723c20dedada6a74edc6d41f/src/tests/gl_tests/WebGLCompatibilityTest.cpp
[modify] https://crrev.com/bb15ceefd9ba0685723c20dedada6a74edc6d41f/src/libANGLE/Context.cpp


### gi...@appspot.gserviceaccount.com (2023-03-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/d12ce14e12301b8e30dde4251e42414e12efbfb6

commit d12ce14e12301b8e30dde4251e42414e12efbfb6
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Wed Mar 29 22:47:34 2023

Roll ANGLE from 4afbbe85d9eb to 31321cb3934a (5 revisions)

https://chromium.googlesource.com/angle/angle.git/+log/4afbbe85d9eb..31321cb3934a

2023-03-29 cnorthrop@google.com Tests: Add Minecraft Bedrock trace
2023-03-29 yuxinhu@google.com Explicitly Add Aliased Memory Decoration in SpirV
2023-03-29 angle-autoroll@skia-public.iam.gserviceaccount.com Roll Chromium from c83e966b4c7e to f7c2a70f23b1 (1902 revisions)
2023-03-29 geofflang@chromium.org Remove syncing of extended dirty bits for TexImage calls.
2023-03-29 mark@lunarg.com Tests: Add fishdom trace

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/angle-chromium-autoroll
Please CC angle-team@google.com,geofflang@google.com on the revert to ensure that a human
is aware of the problem.

To file a bug in ANGLE: https://bugs.chromium.org/p/angleproject/issues/entry
To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86
Bug: chromium:1292038,chromium:1410191
Tbr: geofflang@google.com
Test: Test: angle_trace_tests --gtest_filter="*fishdom*"
Test: Test: angle_trace_tests --gtest_filter="*minecraft_bedrock*"
Change-Id: Id9d29438c7fdb7ce413a094faca7f035275b82ce
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4383198
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#1123910}

[modify] https://crrev.com/d12ce14e12301b8e30dde4251e42414e12efbfb6/DEPS


### cl...@chromium.org (2023-03-30)

ClusterFuzz testcase 5625731783262208 is flaky and no longer crashes, so closing issue.

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### cl...@chromium.org (2023-03-30)

ClusterFuzz testcase 5625731783262208 is closed as invalid, so closing issue.

### am...@chromium.org (2023-03-30)

[Empty comment from Monorail migration]

### am...@google.com (2023-04-05)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-04-05)

Congratulations! The VRP Panel has decided to award you $15,000 for this report. Thank you for your efforts and reporting this issue to us -- great work! 

### am...@google.com (2023-04-08)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-05-25)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-05-26)

Hi n3sk, thanks again for this report.We consider attachments/POCs and analysis included with reports to be an integral part of the report (https://g.co/chrome/vrp), so I've undeleted comments #3 and #5 containing the POC and analysis / log file attachment. 

### am...@google.com (2023-05-30)

[Empty comment from Monorail migration]

### pg...@google.com (2023-05-30)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-06-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/fb0174fa6556af32da4ccb07965a8418dc9597b5

commit fb0174fa6556af32da4ccb07965a8418dc9597b5
Author: Shahbaz Youssefi <syoussefi@chromium.org>
Date: Fri Jun 16 16:08:51 2023

Fix clearing of extended dirty bits in draw calls

When syncing all dirty bits (i.e. in draw calls), the extended dirty
bits were not cleared.  This caused the extended dirty bits to be
resynced every time.

Credit Steven Noonan <steven@uplinklabs.net>

Bug: chromium:1410191
Change-Id: I7042462bbc4346880eb99128b3501cf130987505
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/4615239
Commit-Queue: Geoff Lang <geofflang@chromium.org>
Reviewed-by: Geoff Lang <geofflang@chromium.org>

[modify] https://crrev.com/fb0174fa6556af32da4ccb07965a8418dc9597b5/src/libANGLE/Context.inl.h
[modify] https://crrev.com/fb0174fa6556af32da4ccb07965a8418dc9597b5/src/libANGLE/Context.h


### gi...@appspot.gserviceaccount.com (2023-06-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/5474df133a413aefe789c6caf51e93a6c7fa2ff0

commit 5474df133a413aefe789c6caf51e93a6c7fa2ff0
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Mon Jun 19 21:28:39 2023

Roll ANGLE from b37df0c72923 to fb0174fa6556 (1 revision)

https://chromium.googlesource.com/angle/angle.git/+log/b37df0c72923..fb0174fa6556

2023-06-19 syoussefi@chromium.org Fix clearing of extended dirty bits in draw calls

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/angle-chromium-autoroll
Please CC angle-team@google.com,ynovikov@google.com on the revert to ensure that a human
is aware of the problem.

To file a bug in ANGLE: https://bugs.chromium.org/p/angleproject/issues/entry
To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86
Bug: chromium:1410191
Tbr: ynovikov@google.com
Change-Id: Ide2a669f3ea058944d2b3aeada80a198fe770964
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4626861
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#1159732}

[modify] https://crrev.com/5474df133a413aefe789c6caf51e93a6c7fa2ff0/DEPS


### [Deleted User] (2023-07-06)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1410191?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1420610, crbug.com/chromium/1426235]
[Monorail components added to Component Tags custom field.]

### ti...@chromium.org (2024-06-27)

Adding `ClusterFuzz-Ignore` hotlist to all `ClusterFuzz-Wrong` issues per crbug.com/40285975.

### ti...@chromium.org (2024-06-27)

Adding `ClusterFuzz-Ignore` hotlist to all `ClusterFuzz-Wrong` issues per crbug.com/40285975.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062792)*
