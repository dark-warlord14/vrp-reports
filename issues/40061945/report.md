# Security:  stack-use-after-scope in dawn::native::CommandEncoder::BeginRenderPass

| Field | Value |
|-------|-------|
| **Issue ID** | [40061945](https://issues.chromium.org/issues/40061945) |
| **Status** | Fixed |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU>Dawn, Internals>Skia |
| **Platforms** | Windows |
| **Reporter** | 0x...@gmail.com |
| **Assignee** | ar...@google.com |
| **Created** | 2022-11-29 |
| **Bounty** | $10,000.00 |

## Description

**VULNERABILITY DETAILS**  

stack-use-after-scope in dawn::native::CommandEncoder::BeginRenderPass

**VERSION**  

Chromium 110.0.5447.0 (Developer Build) (64-bit)  

Revision a3f4c77cb8416e743cb15d44aa75d30edf927c88-refs/heads/main@{#1076486}  

OS Windows 10 Version 22H2 (Build 19045.2251)

**REPRODUCTION CASE**  

Run the command:  

chrome.exe --user-data-dir=C:/tmp --no-sandbox --enable-features=SkiaDawn <http://localhost:8000/poc.html>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

**Type of crash: [tab, browser, etc.]**

=================================================================  

==31960==ERROR: AddressSanitizer: stack-use-after-scope on address 0x12096582e700 at pc 0x7ffc9425ebc4 bp 0x007c741fd4c0 sp 0x007c741fd508  

READ of size 8 at 0x12096582e700 thread T0  

==31960==WARNING: Failed to use and restart external symbolizer!  

==31960==\*\*\* WARNING: Failed to initialize DbgHelp! \*\*\*  

==31960==\*\*\* Most likely this means that the app is already \*\*\*  

==31960==\*\*\* using DbgHelp, possibly with incompatible flags. \*\*\*  

==31960==\*\*\* Due to technical reasons, symbolization might crash \*\*\*  

==31960==\*\*\* or produce wrong results. \*\*\*  

#0 0x7ffc9425ebc3 in dawn::native::CommandEncoder::BeginRenderPass::<lambda\_1>::operator() C:\b\s\w\ir\cache\builder\src\third\_party\dawn\src\dawn\native\CommandEncoder.cpp:853  

#1 0x7ffc94247b46 in dawn::native::CommandEncoder::BeginRenderPass C:\b\s\w\ir\cache\builder\src\third\_party\dawn\src\dawn\native\CommandEncoder.cpp:848  

#2 0x7ffc94247693 in dawn::native::CommandEncoder::APIBeginRenderPass C:\b\s\w\ir\cache\builder\src\third\_party\dawn\src\dawn\native\CommandEncoder.cpp:835  

#3 0x7ffc941d4eb9 in wgpu::CommandEncoder::BeginRenderPass C:\b\s\w\ir\cache\builder\src\out\Release\_x64\gen\third\_party\dawn\src\dawn\webgpu\_cpp.cpp:2058  

#4 0x7ffca6ad4f6a in GrDawnOpsRenderPass::beginRenderPass C:\b\s\w\ir\cache\builder\src\third\_party\skia\src\gpu\ganesh\dawn\GrDawnOpsRenderPass.cpp:89  

#5 0x7ffca6ad46cf in GrDawnOpsRenderPass::GrDawnOpsRenderPass C:\b\s\w\ir\cache\builder\src\third\_party\skia\src\gpu\ganesh\dawn\GrDawnOpsRenderPass.cpp:54  

#6 0x7ffca31f7796 in GrDawnGpu::onGetOpsRenderPass C:\b\s\w\ir\cache\builder\src\third\_party\skia\src\gpu\ganesh\dawn\GrDawnGpu.cpp:178  

#7 0x7ffca3224c0b in skgpu::v1::OpsTask::onExecute C:\b\s\w\ir\cache\builder\src\third\_party\skia\src\gpu\ganesh\ops\OpsTask.cpp:610  

#8 0x7ffca0355f5c in GrDrawingManager::executeRenderTasks C:\b\s\w\ir\cache\builder\src\third\_party\skia\src\gpu\ganesh\GrDrawingManager.cpp:273  

#9 0x7ffca0353db1 in GrDrawingManager::flush C:\b\s\w\ir\cache\builder\src\third\_party\skia\src\gpu\ganesh\GrDrawingManager.cpp:195  

#10 0x7ffca03566b7 in GrDrawingManager::flushSurfaces C:\b\s\w\ir\cache\builder\src\third\_party\skia\src\gpu\ganesh\GrDrawingManager.cpp:523  

#11 0x7ffca034e689 in GrDirectContextPriv::flushSurfaces C:\b\s\w\ir\cache\builder\src\third\_party\skia\src\gpu\ganesh\GrDirectContextPriv.cpp:63  

#12 0x7ffca0453034 in SkSurface\_Gpu::onFlush C:\b\s\w\ir\cache\builder\src\third\_party\skia\src\image\SkSurface\_Gpu.cpp:232  

#13 0x7ffcab5b540c in gpu::raster::RasterDecoderImpl::FlushSurface C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\raster\_decoder.cc:741  

#14 0x7ffcab5c24af in gpu::raster::RasterDecoderImpl::DoEndRasterCHROMIUM C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\raster\_decoder.cc:3353  

#15 0x7ffcab5a9c7c in gpu::raster::RasterDecoderImpl::HandleEndRasterCHROMIUM C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\raster\_decoder\_autogen.h:161  

#16 0x7ffcab5b0fc9 in gpu::raster::RasterDecoderImpl::DoCommandsImpl<0> C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\raster\_decoder.cc:1499  

#17 0x7ffcab5af7ea in gpu::raster::RasterDecoderImpl::DoCommands C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\raster\_decoder.cc:1559  

#18 0x7ffca3bf68f6 in gpu::CommandBufferService::Flush C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\command\_buffer\_service.cc:226  

#19 0x7ffca0f3766b in gpu::CommandBufferStub::OnAsyncFlush C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command\_buffer\_stub.cc:499  

#20 0x7ffca0f3653a in gpu::CommandBufferStub::ExecuteDeferredRequest C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command\_buffer\_stub.cc:154  

#21 0x7ffca3be168f in gpu::GpuChannel::ExecuteDeferredRequest C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\gpu\_channel.cc:694  

#22 0x7ffca3bee356 in base::internal::Invoker<base::internal::BindState<void (gpu::GpuChannel::\*)(mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);)),base::WeakPtr[gpu::GpuChannel](javascript:void(0);),mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);) >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind\_internal.h:894  

#23 0x7ffca09c8242 in gpu::Scheduler::RunNextTask C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\scheduler.cc:726  

#24 0x7ffca09d1d63 in base::internal::Invoker<base::internal::BindState<void (gpu::Scheduler::\*)(),base::internal::UnretainedWrapper[gpu::Scheduler,base::RawPtrBanDanglingIfSupported](javascript:void(0);) >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind\_internal.h:894  

#25 0x7ffc9f439419 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:156  

#26 0x7ffca2451741 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:449  

#27 0x7ffca2450232 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:300  

#28 0x7ffca2426333 in base::MessagePumpDefault::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_default.cc:48  

#29 0x7ffca2453b73 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:609  

#30 0x7ffc9f3c595e in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:141  

#31 0x7ffca1bc2480 in content::GpuMain C:\b\s\w\ir\cache\builder\src\content\gpu\gpu\_main.cc:399  

#32 0x7ffc9ef7ba23 in content::RunOtherNamedProcessTypeMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:734  

#33 0x7ffc9ef7e254 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1088  

#34 0x7ffc9ef793a2 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:344  

#35 0x7ffc9ef7a1fd in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:372  

#36 0x7ffc928314a5 in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc:174  

#37 0x7ff763bf6288 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main\_dll\_loader\_win.cc:166  

#38 0x7ff763bf2c0a in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_exe\_main\_win.cc:391  

#39 0x7ff76402166b in \_\_scrt\_common\_main\_seh d:\a01\_work\12\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#40 0x7ffd6f5474b3 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x1800174b3)  

#41 0x7ffd702026a0 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x1800526a0)

Address 0x12096582e700 is located in stack of thread T0 at offset 256 in frame  

#0 0x7ffca6ad490f in GrDawnOpsRenderPass::beginRenderPass C:\b\s\w\ir\cache\builder\src\third\_party\skia\src\gpu\ganesh\dawn\GrDawnOpsRenderPass.cpp:58

# This frame has 3 object(s): [32, 120) 'colorAttachment' (line 66) [160, 224) 'renderPassDescriptor' (line 73) [256, 304) 'depthStencilAttachment' (line 77) <== Memory access at offset 256 is inside this variable HINT: this may be a false positive if your program uses some custom stack unwind mechanism, swapcontext or vfork (longjmp, SEH and C++ exceptions \*are\* supported) SUMMARY: AddressSanitizer: stack-use-after-scope C:\b\s\w\ir\cache\builder\src\third\_party\dawn\src\dawn\native\CommandEncoder.cpp:853 in dawn::native::CommandEncoder::BeginRenderPass::<lambda\_1>::operator() Shadow bytes around the buggy address: 0x12096582e480: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 0x12096582e500: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 0x12096582e580: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 0x12096582e600: f1 f1 f1 f1 00 00 00 00 00 00 00 00 00 00 00 f2 0x12096582e680: f2 f2 f2 f2 00 00 00 00 00 00 00 00 f2 f2 f2 f2 =>0x12096582e700:[f8]f8 f8 f8 f8 f8 f3 f3 f3 f3 f3 f3 00 00 00 00 0x12096582e780: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 0x12096582e800: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 0x12096582e880: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 0x12096582e900: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 0x12096582e980: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 Shadow byte legend (one shadow byte represents 8 application bytes): Addressable: 00 Partially addressable: 01 02 03 04 05 06 07 Heap left redzone: fa Freed heap region: fd Stack left redzone: f1 Stack mid redzone: f2 Stack right redzone: f3 Stack after return: f5 Stack use after scope: f8 Global redzone: f9 Global init order: f6 Poisoned by user: f7 Container overflow: fc Array cookie: ac Intra object redzone: bb ASan internal: fe Left alloca redzone: ca Right alloca redzone: cb ==31960==ABORTING [23560:25416:1129/090403.610:ERROR:gpu\_process\_host.cc(992)] GPU process exited unexpectedly: exit\_code=1 Warning: windows\_read\_data\_files\_in\_registry: Registry lookup failed to get layer manifest files. [25780:30848:1129/090404.432:ERROR:gl\_display.cc(508)] EGL Driver message (Error) eglMakeCurrent: 'dpy' not a valid EGLDisplay handle Warning: DawnDeviceDescriptor is deprecated. Please use WGPUDeviceDescriptor instead.

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 2.3 KB)

## Timeline

### [Deleted User] (2022-11-29)

[Empty comment from Monorail migration]

### cl...@chromium.org (2022-11-30)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5119085710082048.

### cl...@chromium.org (2022-11-30)

ClusterFuzz testcase 5119085710082048 is closed as invalid, so closing issue.

### cl...@chromium.org (2022-11-30)

Testcase 5119085710082048 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=5119085710082048.

### 0x...@gmail.com (2022-11-30)

It is a GPU process issue in the Windows and it can be reproduced steadily.
To reproduce this issue needs the SkiaDawn feature.
Maybe the Status should not be WontFix (Closed).

### ad...@chromium.org (2022-11-30)

Reopening to look into other ways of figuring out if this is reproducible.

### aj...@chromium.org (2022-11-30)

shh robot. (I have not otherwise triaged this)

### 0x...@gmail.com (2022-12-01)

It seems than this issue is similar to https://crbug.com/chromium/1393728 .

### ad...@google.com (2022-12-07)

I am setting up a Windows VM to repro this. Apologies for the delay.

### ad...@google.com (2022-12-08)

I'm unable to reproduce this even with asan-win32-release_x64-1076486, but that's on a VM. I assume this is somehow GPU dependent.

So - Dan - unfortunately we're going to need to pass this over to you unreproduced. The stack trace suggests this is a real bug, possibly related to accessing depthStencilAttachment after it's no longer valid.

Could you take a look and assess if this is real?

IMPORTANT: I'm assuming this can only be reached with SkiaDawn so I'm labelling it Security_Impact-None, but if this is reachable in normal Chrome builds with default features (or origin trials) please let us know so we can label it appropriately.

[Monorail components: Internals>GPU>Dawn]

### 0x...@gmail.com (2022-12-08)

[Comment Deleted]

### ds...@google.com (2022-12-08)

It looks like the bug still exists even if it can't be triggered at the moment. The issue is in SkiaDawn.

In https://skia.googlesource.com/skia/+/refs/heads/main/src/gpu/ganesh/dawn/GrDawnOpsRenderPass.cpp#85 the `depthStencilAttachment` is assigned into the `renderPassDescriptor` but the lifetime of that item ends at the end of the `if()`, so it's out of scope.

Looks like the https://skia.googlesource.com/skia/+/refs/heads/main/src/gpu/ganesh/dawn/GrDawnOpsRenderPass.cpp#77 needs to move outside the `if()`

Sending to armansito@ who was last editing that file.

[Monorail components: Internals>Skia]

### ds...@chromium.org (2022-12-08)

[Empty comment from Monorail migration]

### ar...@google.com (2022-12-08)

Ah, this should be an easy fix. I'm taking a look now.

### se...@chromium.org (2022-12-08)

Thanks for the report. Yeah, this looks wrong. I'll put up the suggested fix.

### se...@chromium.org (2022-12-08)

Oops, looks like I hit a race condition with Arman. :) Anyway CL is here: https://skia-review.googlesource.com/c/skia/+/615876

### se...@chromium.org (2022-12-08)

Arman, you go ahead and land yours. Bouncing the bug back to you.

### gi...@appspot.gserviceaccount.com (2022-12-08)

The following revision refers to this bug:
  https://skia.googlesource.com/skia/+/77aa8623ef94dbd722671d5a96aa7112f8631d49

commit 77aa8623ef94dbd722671d5a96aa7112f8631d49
Author: Arman Uguray <armansito@google.com>
Date: Thu Dec 08 17:45:48 2022

[ganesh][dawn] Fix stack-use-after-scope bug in GrDawnOpsRenderPass

The DepthStencilAttachment instance always went out of scope after a
pointer to it got assigned to a RenderPassDescriptor.

Bug: 1394272
Change-Id: Icce9f385e524405fa8e4a072d858d9bd249093d1
Reviewed-on: https://skia-review.googlesource.com/c/skia/+/615856
Reviewed-by: Brian Osman <brianosman@google.com>
Commit-Queue: Arman Uguray <armansito@google.com>

[modify] https://crrev.com/77aa8623ef94dbd722671d5a96aa7112f8631d49/src/gpu/ganesh/dawn/GrDawnOpsRenderPass.cpp


### ar...@google.com (2022-12-08)

No worries! I just landed the fix to Skia, which should roll into chromium eventually.

### gi...@appspot.gserviceaccount.com (2022-12-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/506366e1a54a16856fc6c7c2c1f996df6926aa04

commit 506366e1a54a16856fc6c7c2c1f996df6926aa04
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Fri Dec 09 01:16:10 2022

Roll Skia from 4f94bfb18bba to 3e1741ebc581 (10 revisions)

https://skia.googlesource.com/skia.git/+log/4f94bfb18bba..3e1741ebc581

2022-12-08 cmumford@google.com [infra] make addr2line silent when checking existence
2022-12-08 cmumford@google.com [infra] Move Test-Debian10-*-DLL1 to new swarming job.
2022-12-08 johnstiles@google.com Add merge-loop-mask opcode.
2022-12-08 johnstiles@google.com Allow pushing and popping the loop- and return-masks.
2022-12-08 robertphillips@google.com [graphite] Fill in PrecompileRTEffect's addToKey method
2022-12-08 johnstiles@google.com Split combine_condition_mask op into two separate ops.
2022-12-08 johnstiles@google.com Fix nested ternary support.
2022-12-08 armansito@google.com [ganesh][dawn] Fix stack-use-after-scope bug in GrDawnOpsRenderPass
2022-12-08 herb@google.com Add serize slug, and remote slug configs to the Slug bot
2022-12-08 herb@google.com use SkStrikeServer to convert glyph run lists to slugs

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/skia-autoroll
Please CC djsollen@google.com on the revert to ensure that a human
is aware of the problem.

To file a bug in Skia: https://bugs.chromium.org/p/skia/issues/entry
To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux-blink-rel;luci.chromium.try:linux-chromeos-compile-dbg;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel
Cq-Do-Not-Cancel-Tryjobs: true
Bug: chromium:1394272
Tbr: djsollen@google.com
Change-Id: I196ab3e33e16bf48490f5fa0e778095c45711040
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4089816
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#1081270}

[modify] https://crrev.com/506366e1a54a16856fc6c7c2c1f996df6926aa04/DEPS


### an...@chromium.org (2022-12-19)

Hi armansito@, is this bug fixed now? 

### ar...@google.com (2023-02-01)

Sorry about the late reply. Yes, this has been fixed.

### [Deleted User] (2023-02-01)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-01)

[Empty comment from Monorail migration]

### am...@google.com (2023-02-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-02-09)

Congratulations asnine! The VRP Panel has decided to award you $10,000 for this report. Thank you for your efforts and reporting this issue to us -- nice work! 

### am...@google.com (2023-02-11)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-10)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-05-10)

This issue was migrated from crbug.com/chromium/1394272?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Internals>GPU>Dawn, Internals>Skia]
[Monorail components added to Component Tags custom field.]

### ti...@chromium.org (2024-06-27)

Adding `ClusterFuzz-Ignore` hotlist to all `ClusterFuzz-Wrong` issues per crbug.com/40285975.

### ti...@chromium.org (2024-06-27)

Adding `ClusterFuzz-Ignore` hotlist to all `ClusterFuzz-Wrong` issues per crbug.com/40285975.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061945)*
