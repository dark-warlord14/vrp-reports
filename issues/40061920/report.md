# Security: stack-use-after-scope in dawn::native::d3d12::ShaderModule::Compile

| Field | Value |
|-------|-------|
| **Issue ID** | [40061920](https://issues.chromium.org/issues/40061920) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Dawn |
| **Platforms** | Windows |
| **Reporter** | 0x...@gmail.com |
| **Assignee** | sh...@google.com |
| **Created** | 2022-11-26 |
| **Bounty** | $10,000.00 |

## Description

**VULNERABILITY DETAILS**

stack-use-after-scope in dawn::native::d3d12::ShaderModule::Compile

**VERSION**

Chromium 110.0.5441.0 (Developer Build) (64-bit)  

Revision 04b0c316b8fa3d1017142592f171473f1eba9069-refs/heads/main@{#1075846}  

OS Windows 10 Version 22H2 (Build 19045.2251)

**REPRODUCTION CASE**  

Run the command:

chrome.exe --user-data-dir=C:/any --no-sandbox --enable-features=SkiaDawn,WebXRImageTracking

# **FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION** **Type of crash: [tab, browser, etc.]**

==13984==ERROR: AddressSanitizer: stack-use-after-scope on address 0x128bc78825f0 at pc 0x7ffb90302380 bp 0x003939bfd6a0 sp 0x003939bfd6e8  

READ of size 8 at 0x128bc78825f0 thread T0  

==13984==WARNING: Failed to use and restart external symbolizer!  

==13984==\*\*\* WARNING: Failed to initialize DbgHelp! \*\*\*  

==13984==\*\*\* Most likely this means that the app is already \*\*\*  

==13984==\*\*\* using DbgHelp, possibly with incompatible flags. \*\*\*  

==13984==\*\*\* Due to technical reasons, symbolization might crash \*\*\*  

==13984==\*\*\* or produce wrong results. \*\*\*  

#0 0x7ffb9030237f in dawn::native::d3d12::ShaderModule::Compile C:\b\s\w\ir\cache\builder\src\third\_party\dawn\src\dawn\native\d3d12\ShaderModuleD3D12.cpp:490  

#1 0x7ffb902e3ef9 in dawn::native::d3d12::RenderPipeline::Initialize C:\b\s\w\ir\cache\builder\src\third\_party\dawn\src\dawn\native\d3d12\RenderPipelineD3D12.cpp:370  

#2 0x7ffb9019978e in dawn::native::DeviceBase::CreateRenderPipeline C:\b\s\w\ir\cache\builder\src\third\_party\dawn\src\dawn\native\Device.cpp:1615  

#3 0x7ffb901989d7 in dawn::native::DeviceBase::APICreateRenderPipeline C:\b\s\w\ir\cache\builder\src\third\_party\dawn\src\dawn\native\Device.cpp:1151  

#4 0x7ffb900c16ef in wgpu::Device::CreateRenderPipeline C:\b\s\w\ir\cache\builder\src\out\Release\_x64\gen\third\_party\dawn\src\dawn\webgpu\_cpp.cpp:2253  

#5 0x7ffba29abff1 in GrDawnProgramBuilder::Build C:\b\s\w\ir\cache\builder\src\third\_party\skia\src\gpu\ganesh\dawn\GrDawnProgramBuilder.cpp:407  

#6 0x7ffb9f0cf48e in GrDawnGpu::getOrCreateRenderPipeline C:\b\s\w\ir\cache\builder\src\third\_party\skia\src\gpu\ganesh\dawn\GrDawnGpu.cpp:943  

#7 0x7ffba29a26cf in GrDawnOpsRenderPass::onBindPipeline C:\b\s\w\ir\cache\builder\src\third\_party\skia\src\gpu\ganesh\dawn\GrDawnOpsRenderPass.cpp:160  

#8 0x7ffba29b46ec in GrOpsRenderPass::bindPipeline C:\b\s\w\ir\cache\builder\src\third\_party\skia\src\gpu\ganesh\GrOpsRenderPass.cpp:96  

#9 0x7ffb9f161e65 in `anonymous namespace'::FillRectOpImpl::onExecute C:\b\s\w\ir\cache\builder\src\third_party\skia\src\gpu\ganesh\ops\FillRectOp.cpp:317 #10 0x7ffb9f0f2bde in GrOp::execute C:\b\s\w\ir\cache\builder\src\third_party\skia\src\gpu\ganesh\ops\GrOp.h:193 #11 0x7ffb9f0f1b54 in skgpu::v1::OpsTask::onExecute C:\b\s\w\ir\cache\builder\src\third_party\skia\src\gpu\ganesh\ops\OpsTask.cpp:646 #12 0x7ffb9f0f87b3 in GrDDLTask::onExecute C:\b\s\w\ir\cache\builder\src\third_party\skia\src\gpu\ganesh\GrDDLTask.cpp:93 #13 0x7ffb9c217a5c in GrDrawingManager::executeRenderTasks C:\b\s\w\ir\cache\builder\src\third_party\skia\src\gpu\ganesh\GrDrawingManager.cpp:273 #14 0x7ffb9c2158b1 in GrDrawingManager::flush C:\b\s\w\ir\cache\builder\src\third_party\skia\src\gpu\ganesh\GrDrawingManager.cpp:195 #15 0x7ffb9c2181b7 in GrDrawingManager::flushSurfaces C:\b\s\w\ir\cache\builder\src\third_party\skia\src\gpu\ganesh\GrDrawingManager.cpp:523 #16 0x7ffb9c210189 in GrDirectContextPriv::flushSurfaces C:\b\s\w\ir\cache\builder\src\third_party\skia\src\gpu\ganesh\GrDirectContextPriv.cpp:63 #17 0x7ffb9c314c84 in SkSurface_Gpu::onFlush C:\b\s\w\ir\cache\builder\src\third_party\skia\src\image\SkSurface_Gpu.cpp:232 #18 0x7ffba542ccf0 in viz::SkiaOutputSurfaceImplOnGpu::FinishPaintRenderPass C:\b\s\w\ir\cache\builder\src\components\viz\service\display_embedder\skia_output_surface_impl_on_gpu.cc:696 #19 0x7ffba0da471d in base::internal::Invoker<base::internal::BindState<void (viz::SkiaOutputSurfaceImplOnGpu::\*)(const gpu::Mailbox &, sk_sp<SkDeferredDisplayList>, sk_sp<SkDeferredDisplayList>, std::Cr::vector<viz::ImageContextImpl \*,std::Cr::allocator<viz::ImageContextImpl \*> >, std::Cr::vector<gpu::SyncToken,std::Cr::allocator<gpu::SyncToken> >, base::OnceCallback<void ()>, base::OnceCallback<void (gfx::GpuFenceHandle)>, bool),base::internal::UnretainedWrapper<viz::SkiaOutputSurfaceImplOnGpu,base::RawPtrBanDanglingIfSupported>,gpu::Mailbox,sk_sp<SkDeferredDisplayList>,sk_sp<SkDeferredDisplayList>,std::Cr::vector<viz::ImageContextImpl \*,std::Cr::allocator<viz::ImageContextImpl \*> >,std::Cr::vector<gpu::SyncToken,std::Cr::allocator<gpu::SyncToken> >,base::OnceCallback<void ()>,base::OnceCallback<void (gfx::GpuFenceHandle)>,bool>,void ()>::RunImpl<void (viz::SkiaOutputSurfaceImplOnGpu::\*)(const gpu::Mailbox &, sk_sp<SkDeferredDisplayList>, sk_sp<SkDeferredDisplayList>, std::Cr::vector<viz::ImageContextImpl \*,std::Cr::allocator<viz::ImageContextImpl \*> >, std::Cr::vector<gpu::SyncToken,std::Cr::allocator<gpu::SyncToken> >, base::OnceCallback<void ()>, base::OnceCallback<void (gfx::GpuFenceHandle)>, bool),std::Cr::tuple<base::internal::UnretainedWrapper<viz::SkiaOutputSurfaceImplOnGpu,base::RawPtrBanDanglingIfSupported>,gpu::Mailbox,sk_sp<SkDeferredDisplayList>,sk_sp<SkDeferredDisplayList>,std::Cr::vector<viz::ImageContextImpl \*,std::Cr::allocator<viz::ImageContextImpl \*> >,std::Cr::vector<gpu::SyncToken,std::Cr::allocator<gpu::SyncToken> >,base::OnceCallback<void ()>,base::OnceCallback<void (gfx::GpuFenceHandle)>,bool>,0,1,2,3,4,5,6,7,8> C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:943 #20 0x7ffba0da8992 in base::internal::Invoker<base::internal::BindState<`lambda at ../../components/viz/service/display\_embedder/skia\_output\_surface\_impl.cc:1107:7',std::Cr::vector<base::OnceCallback<void ()>,std::Cr::allocator<base::OnceCallback<void ()> > >,viz::SkiaOutputSurfaceImpl::SyncMode,base::internal::UnretainedWrapper[base::WaitableEvent,base::RawPtrBanDanglingIfSupported](javascript:void(0);),base::internal::UnretainedWrapper[viz::SkiaOutputSurfaceImplOnGpu,base::RawPtrBanDanglingIfSupported](javascript:void(0);),bool,bool,base::TimeTicks>,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind\_internal.h:894  

#21 0x7ffb9c889e82 in gpu::Scheduler::RunNextTask C:\b\s\w\ir\cache\builder\src\gpu\command\_buffer\service\scheduler.cc:726  

#22 0x7ffb9c8939a3 in base::internal::Invoker<base::internal::BindState<void (gpu::Scheduler::\*)(),base::internal::UnretainedWrapper[gpu::Scheduler,base::RawPtrBanDanglingIfSupported](javascript:void(0);) >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind\_internal.h:894  

#23 0x7ffb9b2fe899 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:156  

#24 0x7ffb9e31af71 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:449  

#25 0x7ffb9e319a62 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:300  

#26 0x7ffb9e2efb63 in base::MessagePumpDefault::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_default.cc:48  

#27 0x7ffb9e31d3a3 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:609  

#28 0x7ffb9b28adde in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:141  

#29 0x7ffb9da866d4 in content::GpuMain C:\b\s\w\ir\cache\builder\src\content\gpu\gpu\_main.cc:399  

#30 0x7ffb9ae40837 in content::RunOtherNamedProcessTypeMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:734  

#31 0x7ffb9ae43068 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1088  

#32 0x7ffb9ae3e1b6 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:344  

#33 0x7ffb9ae3f011 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:372  

#34 0x7ffb8e7214a5 in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc:174  

#35 0x7ff64d7a6288 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main\_dll\_loader\_win.cc:166  

#36 0x7ff64d7a2c0a in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_exe\_main\_win.cc:391  

#37 0x7ff64dbd166b in \_\_scrt\_common\_main\_seh d:\a01\_work\12\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#38 0x7ffc67e774b3 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x1800174b3)  

#39 0x7ffc69a626a0 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x1800526a0)

Address 0x128bc78825f0 is located in stack of thread T0 at offset 1520 in frame  

#0 0x7ffb902e3047 in dawn::native::d3d12::RenderPipeline::Initialize C:\b\s\w\ir\cache\builder\src\third\_party\dawn\src\dawn\native\d3d12\RenderPipelineD3D12.cpp:332

This frame has 22 object(s):  

[32, 688) 'descriptorD3D12' (line 352)  

[816, 840) 'shaders' (line 354)  

[880, 1168) 'compiledShader' (line 358)  

[1232, 1920) 'entryPoint' (line 364) <== Memory access at offset 1520 is inside this variable  

[2048, 2056) 'ref.tmp24' (line 368)  

[2080, 2096) '\_\_begin2' (line 368)  

[2112, 2128) '\_\_end2' (line 368)  

[2144, 2256) '\_localVar373' (line 370)  

[2288, 2304) 'ref.tmp48' (line 374)  

[2320, 2832) 'inputElementDescriptors' (line 385)  

[2896, 2912) 'ref.tmp73' (line 387)  

[2928, 2936) 'ref.tmp115' (line 416)  

[2960, 2968) 'ref.tmp119' (line 417)  

[2992, 3008) '\_\_begin2120' (line 417)  

[3024, 3040) '\_\_end2121' (line 417)  

[3056, 3108) 'ref.tmp151' (line 429)  

[3152, 3208) 'blob' (line 441)  

[3248, 3256) '\_localVar451' (line 449)  

[3280, 3288) 'd3dBlob' (line 455)  

[3312, 3320) '\_localVar457' (line 456)  

[3344, 3400) 'ref.tmp228' (line 458)  

[3440, 3448) 'agg.tmp229'  

HINT: this may be a false positive if your program uses some custom stack unwind mechanism, swapcontext or vfork  

(longjmp, SEH and C++ exceptions \*are\* supported)  

SUMMARY: AddressSanitizer: stack-use-after-scope C:\b\s\w\ir\cache\builder\src\third\_party\dawn\src\dawn\native\d3d12\ShaderModuleD3D12.cpp:490 in dawn::native::d3d12::ShaderModule::Compile  

Shadow bytes around the buggy address:  

0x128bc7882300: f2 f2 f2 f2 f2 f2 00 00 00 f2 f2 f2 f2 f2 00 00  

0x128bc7882380: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x128bc7882400: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x128bc7882480: 00 00 f2 f2 f2 f2 f2 f2 f2 f2 f8 f8 f8 f8 f8 f8  

0x128bc7882500: f8 f8 f8 f8 f8 f8 f8 f8 f8 f8 f8 f8 f8 f8 f8 f8  

=>0x128bc7882580: f8 f8 f8 f8 f8 f8 f8 f8 f8 f8 f8 f8 f8 f8[f8]f8  

0x128bc7882600: f8 f8 f8 f8 f8 f8 f8 f8 f8 f8 f8 f8 f8 f8 f8 f8  

0x128bc7882680: f8 f8 f8 f8 f8 f8 f8 f8 f8 f8 f8 f8 f8 f8 f8 f8  

0x128bc7882700: f8 f8 f8 f8 f8 f8 f8 f8 f8 f8 f8 f8 f8 f8 f8 f8  

0x128bc7882780: f2 f2 f2 f2 f2 f2 f2 f2 f2 f2 f2 f2 f2 f2 f2 f2  

0x128bc7882800: 00 f2 f2 f2 00 00 f2 f2 00 00 f2 f2 00 00 00 00  

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

==13984==ABORTING  

[11404:6636:1126/093940.254:ERROR:gpu\_process\_host.cc(992)] GPU process exited unexpectedly: exit\_code=1  

Warning: windows\_read\_data\_files\_in\_registry: Registry lookup failed to get layer manifest files.  

Warning: Layer VK\_LAYER\_TENCENT\_wegame\_cross\_overlay uses API version 1.1 which is older than the application specified API version of 1.3. May cause issues.  

[1176:1080:1126/093940.955:ERROR:gl\_display.cc(508)] EGL Driver message (Error) eglMakeCurrent: 'dpy' not a valid EGLDisplay handle  

Warning: DawnDeviceDescriptor is deprecated. Please use WGPUDeviceDescriptor instead.

## Timeline

### [Deleted User] (2022-11-26)

[Empty comment from Monorail migration]

### ct...@chromium.org (2022-11-29)

Passing to GPU folks as I don't have a Windows device with GPUs (only virtual machines). Based on blame... shrekshao@ could you please take a look? Also cc'ing dsinclair@ and cwallez@. It looks like SkiaDawn may be active on the correct system configuration, and possibly WebXRImageTracking may be in Origin Trial. If the latter is not true yet, then this may be Security_Impact-None.

Reporter: Are there any other steps to reproduce this or does this trigger on loading the new tab page? This seems plausibly like it code allow an attacker controlled UAF in the GPU process, but it isn't immediately clear how exploitable this would be. Any further analysis would be very helpful for treating this as a security bug.

[Monorail components: Internals>GPU>Dawn]

### 0x...@gmail.com (2022-11-29)

It seems that `chrome.exe --user-data-dir=C:/any --no-sandbox --enable-features=SkiaDawn http://localhost/anypage`  
will trigger this issue.


### sh...@google.com (2022-11-29)

Thanks for the report. It's pretty obvious that https://source.chromium.org/chromium/chromium/src/+/main:third_party/dawn/src/dawn/native/d3d12/RenderPipelineD3D12.cpp;l=364;drc=2899fd9a2767ef605edff106d1e00ff45af08a2e
the pointer is pointing to a local variable that's getting freed. Let me put up a fix

### [Deleted User] (2022-11-29)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-11-29)

The following revision refers to this bug:
  https://dawn.googlesource.com/dawn/+/67d52eb4f27b2056e181a77cbd8afa34c62d0d16

commit 67d52eb4f27b2056e181a77cbd8afa34c62d0d16
Author: shrekshao <shrekshao@google.com>
Date: Tue Nov 29 22:00:13 2022

Fix stack-use-after-scope for usedInterstageVariables pointer

Bug: chromium:1393728
Change-Id: I078f898b9a6a237c81c15bb86736eb790cf6a261
Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/112260
Reviewed-by: Austin Eng <enga@chromium.org>
Commit-Queue: Shrek Shao <shrekshao@google.com>
Kokoro: Kokoro <noreply+kokoro@google.com>

[modify] https://dawn.googlesource.com/dawn/+/67d52eb4f27b2056e181a77cbd8afa34c62d0d16/src/dawn/native/d3d12/RenderPipelineD3D12.cpp


### sh...@google.com (2022-11-29)

[Comment Deleted]

### sh...@google.com (2022-11-29)

I wasn't lucky enough to reproduce with `chrome.exe --user-data-dir=C:/tmp --no-sandbox --enable-features=SkiaDawn`

I got some other backtrace log like:
```
skia_output_device.cc(378) Check failed: characterization.isTextureable() == surface_characterization.isTextureable() (1 vs. 0)
```

But I'm pretty sure the issue you are reporting should be fixed by the fix in https://crbug.com/chromium/1393728#c6. Can you help to verify that 0xasnine@gmail.com? Thanks!

### gi...@appspot.gserviceaccount.com (2022-11-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/15eaa81dc06e96727b9d63395243a8a1083b98b5

commit 15eaa81dc06e96727b9d63395243a8a1083b98b5
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Wed Nov 30 00:20:23 2022

Roll Dawn from 75759ac27378 to 106eaa2710a1 (10 revisions)

https://dawn.googlesource.com/dawn.git/+log/75759ac27378..106eaa2710a1

2022-11-29 dawn-autoroll@skia-public.iam.gserviceaccount.com Roll vulkan-deps from 4b2c47fa5f32 to f42d9335d0ae (3 revisions)
2022-11-29 bclayton@google.com tint/resolver: Clean up variable validation
2022-11-29 shrekshao@google.com Fix stack-use-after-scope for usedInterstageVariables pointer
2022-11-29 dawn-autoroll@skia-public.iam.gserviceaccount.com Roll ANGLE from 000b3bfa32ca to 2de99d47e5e7 (3 revisions)
2022-11-29 bclayton@google.com tint: Add Symbol inequality operator
2022-11-29 bclayton@google.com tint/utils: Add Hashmap equality and hashing
2022-11-29 dsinclair@chromium.org [ir] Make Value a pointer stored in the module.
2022-11-29 bclayton@google.com tint/utils: Add Hashmap::Keys(), Hashmap::Values()
2022-11-29 bclayton@google.com tint/utils: Make Hashmap iterator values mutable
2022-11-29 amaiorano@google.com tint: simplify const eval binary op unit tests

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/dawn-chromium-autoroll
Please CC dsinclair@google.com on the revert to ensure that a human
is aware of the problem.

To file a bug in Dawn: https://bugs.chromium.org/p/dawn/issues/entry
To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Cq-Include-Trybots: luci.chromium.try:dawn-linux-x64-deps-rel;luci.chromium.try:dawn-mac-x64-deps-rel;luci.chromium.try:dawn-win10-x64-deps-rel;luci.chromium.try:dawn-win10-x86-deps-rel
Bug: chromium:1393728
Tbr: dsinclair@google.com
Change-Id: I9facd735bafae43333244eaf60e719e8e9e6cb02
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4063991
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#1077174}

[modify] https://crrev.com/15eaa81dc06e96727b9d63395243a8a1083b98b5/DEPS


### 0x...@gmail.com (2022-11-30)

This issue cannot be reproduced in the latest asan build.

My another https://crbug.com/chromium/1394272 similar to this is marked as WontFix.
However it can be reproduced in  the latest asan build.

### sh...@google.com (2022-11-30)

Do you mean you can still reproduce the bug using ASAN build with the commit roll into chromium at https://crbug.com/chromium/1393728#c9?

### sh...@google.com (2022-11-30)

Maybe you can share the args.gn you use?

This is what I used and didn't reproduce without the CL

use_goma = true
is_asan = true
is_debug = false
is_component_build = true
symbol_level = 2
print_unsymbolized_stack_traces = true
dcheck_always_on = true
enable_nacl = false
dawn_enable_vulkan = true
dawn_enable_wgsl = true # this one might be default by now


### 0x...@gmail.com (2022-11-30)

Fixed in the latest asan build.

### sh...@google.com (2022-11-30)

Oh great. Thanks for the reply!

### [Deleted User] (2022-11-30)

Dear owner, thanks for fixing this bug. We’ve reopened it because security bugs need Security_Severity and FoundIn labels set, which will enable the bots to request merges to the correct branches ( as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact (security@chromium.org) to arrange to set these labels and then this bug can be marked closed again. Thank you! Severity guidelines: https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues FoundIn guidelines: https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security Thanks for your time! 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@google.com (2022-11-30)

This bug is a use-after-free bug and is behind a flag or origin trial token that is not by default available to users. Set labels according to the severity guidelines. Feel free to modify if necessary.

### sh...@google.com (2022-11-30)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-30)

Dear owner, thanks for fixing this bug. We’ve reopened it because security bugs need Security_Severity and FoundIn labels set, which will enable the bots to request merges to the correct branches ( as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact (security@chromium.org) to arrange to set these labels and then this bug can be marked closed again. Thank you! Severity guidelines: https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues FoundIn guidelines: https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security Thanks for your time! 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-11-30)

[Empty comment from Monorail migration]

### ct...@chromium.org (2022-11-30)

Thanks. Setting Severity-High as this was a UAF in the GPU process. That should appease the robots.

Could you clarify if this feature is in Origin Trial? If so, then this would not be Impact-None as it is shipping to users (origin trials are not a security boundary).

### ct...@chromium.org (2022-11-30)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-01)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-01)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-12-01)

[Empty comment from Monorail migration]

### ct...@chromium.org (2022-12-02)

Out of an abundance of caution, removing Security-Impact_None so the appropriate bot machinery kicks in, as https://crbug.com/chromium/1393728#c16 seems to indicate that this feature is in Origin Trial and thus exposed to real users on the open web.

### am...@google.com (2022-12-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-12-09)

Congratulations on another one, asnine! The VRP Panel has decided to award you $10,000 for this report. Thank you for your efforts in discovering and reporting this issue to us -- nice work! 

### am...@google.com (2022-12-10)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-17)

Not requesting merge to dev (M110) because latest trunk commit (1077174) appears to be prior to dev branch point (1084008). If this is incorrect, please replace the Merge-NA-110 label with Merge-Request-110. If other changes are required to fix this bug completely, please request a merge if necessary.

Merge review required: a commit with DEPS changes was detected.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [110].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-12-19)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-12-19)

the dawn roll with this fix landed on 110; the bot is simultaneous adding merge review and merge-NA labels, we'll look into why this is happening 

### [Deleted User] (2023-03-09)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1393728?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061920)*
