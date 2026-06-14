# Security: ANGLE TextureStorage11::setData Memory Corruption

| Field | Value |
|-------|-------|
| **Issue ID** | [40092368](https://issues.chromium.org/issues/40092368) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU>ANGLE |
| **Platforms** | Windows |
| **Reporter** | [Deleted User] |
| **Assignee** | jm...@chromium.org |
| **Created** | 2018-09-05 |
| **Bounty** | $1,000.00 |

## Description

I have tested this on Chrome Stable version 69.0.3497.81.
There is a crash which occurs on an invalid reference to pixelData in TextureStorage11::setData.

This is reproducible on any GPU driver, I have attached a testcase with Nvidia.

3:034> r
rax=0000022684109300 rbx=000082239303ed50 rcx=00007ffd2d04e96b
rdx=000082239303ed50 rsi=0000000000000004 rdi=0000022684109300
rip=00007ffd2d04e96b rsp=0000004c9edfd458 rbp=0000000000000000
 r8=0000000000000004  r9=00007ffd2bdb0000 r10=000082239303ed50
r11=0000022684109300 r12=0000000000000080 r13=0000000000000001
r14=0000000000000001 r15=0000000000000004
iopl=0         nv up ei pl nz na pe nc
cs=0033  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00010202
nvwgf2umx_cfg!NVAPI_Thunk+0x80d8db:
00007ffd`2d04e96b 8b0a            mov     ecx,dword ptr [rdx] ds:00008223`9303ed50=????????
3:034> k
 # Child-SP          RetAddr           Call Site
00 0000004c`9edfd458 00007ffd`2cbaabc5 nvwgf2umx_cfg!NVAPI_Thunk+0x80d8db
01 0000004c`9edfd460 00007ffd`2c135896 nvwgf2umx_cfg!NVAPI_Thunk+0x369b35
*** ERROR: Symbol file could not be found.  Defaulted to export symbols for C:\WINDOWS\SYSTEM32\d3d11.dll - 
02 0000004c`9edfd560 00007ffd`33442988 nvwgf2umx_cfg!OpenAdapter12+0x21d666
03 0000004c`9edfd600 00007ffc`fbfe4cc4 d3d11!CreateDirect3D11SurfaceFromDXGISurface+0x4ecb8
04 0000004c`9edfd710 00007ffc`fbfeea30 libglesv2!rx::TextureStorage11::setData+0x4da [C:\b\c\b\win64_clang\src\third_party\angle\src\libANGLE\renderer\d3d\d3d11\TextureStorage11.cpp @ 791] 
05 0000004c`9edfdaf0 00007ffc`fbff5326 libglesv2!rx::TextureD3D::subImage+0xf8 [C:\b\c\b\win64_clang\src\third_party\angle\src\libANGLE\renderer\d3d\TextureD3D.cpp @ 277] 
06 0000004c`9edfdb90 00007ffc`fbeca026 libglesv2!rx::TextureD3D_2DArray::setSubImage+0x164 [C:\b\c\b\win64_clang\src\third_party\angle\src\libANGLE\renderer\d3d\TextureD3D.cpp @ 2955] 
07 0000004c`9edfdd60 00007ffc`fbfc4c3c libglesv2!gl::Texture::setSubImage+0xbe [C:\b\c\b\win64_clang\src\third_party\angle\src\libANGLE\Texture.cpp @ 986] 
08 0000004c`9edfde10 00007ffc`fbffbdc4 libglesv2!rx::IncompleteTextureSet::getIncompleteTexture+0x278 [C:\b\c\b\win64_clang\src\third_party\angle\src\libANGLE\renderer\renderer_utils.cpp @ 613] 
09 0000004c`9edfdf00 00007ffc`fbf8e94e libglesv2!rx::Context11::getIncompleteTexture+0x2a [C:\b\c\b\win64_clang\src\third_party\angle\src\libANGLE\renderer\d3d\d3d11\Context11.cpp @ 584] 
0a 0000004c`9edfdf40 00007ffc`fbfbb2f1 libglesv2!rx::Renderer11::getIncompleteTexture+0x1e [C:\b\c\b\win64_clang\src\third_party\angle\src\libANGLE\renderer\d3d\d3d11\Renderer11.cpp @ 3888] 
0b 0000004c`9edfdf80 00007ffc`fbfba1be libglesv2!rx::StateManager11::applyTextures+0xe9 [C:\b\c\b\win64_clang\src\third_party\angle\src\libANGLE\renderer\d3d\d3d11\StateManager11.cpp @ 2386] 
0c 0000004c`9edfe030 00007ffc`fbfb9e13 libglesv2!rx::StateManager11::syncTextures+0x3c [C:\b\c\b\win64_clang\src\third_party\angle\src\libANGLE\renderer\d3d\d3d11\StateManager11.cpp @ 2403] 
0d 0000004c`9edfe080 00007ffc`fbffb113 libglesv2!rx::StateManager11::updateState+0x2df [C:\b\c\b\win64_clang\src\third_party\angle\src\libANGLE\renderer\d3d\d3d11\StateManager11.cpp @ 2049] 
0e 0000004c`9edfe110 00007ffc`fbffb151 libglesv2!rx::Context11::prepareForDrawCall+0x19 [C:\b\c\b\win64_clang\src\third_party\angle\src\libANGLE\renderer\d3d\d3d11\Context11.cpp @ 566] 
0f 0000004c`9edfe140 00007ffc`fbeb1783 libglesv2!rx::Context11::drawElementsInstanced+0x21 [C:\b\c\b\win64_clang\src\third_party\angle\src\libANGLE\renderer\d3d\d3d11\Context11.cpp @ 273] 
10 0000004c`9edfe190 00007ffc`fbe8cc2a libglesv2!gl::Context::drawElements+0xa5 [C:\b\c\b\win64_clang\src\third_party\angle\src\libANGLE\Context.cpp @ 2175] 
11 0000004c`9edfe220 00007ffc`ebbfae54 libglesv2!gl::DrawElements+0x95 [C:\b\c\b\win64_clang\src\third_party\angle\src\libGLESv2\entry_points_gles_2_0_autogen.cpp @ 790] 
12 0000004c`9edfe290 00007ffc`eb7c76b9 chrome_child!gpu::gles2::GLES2DecoderPassthroughImpl::DoDrawElements+0x4c [C:\b\c\b\win64_clang\src\gpu\command_buffer\service\gles2_cmd_decoder_passthrough_doers.cc @ 1056] 
13 0000004c`9edfe2f0 00007ffc`eb05acd9 chrome_child!gpu::gles2::GLES2DecoderPassthroughImpl::HandleDrawElements+0x21 [C:\b\c\b\win64_clang\src\gpu\command_buffer\service\gles2_cmd_decoder_passthrough_handlers.cc @ 137] 
14 0000004c`9edfe320 00007ffc`eb05a869 chrome_child!gpu::gles2::GLES2DecoderPassthroughImpl::DoCommandsImpl<0>+0xdd [C:\b\c\b\win64_clang\src\gpu\command_buffer\service\gles2_cmd_decoder_passthrough.cc @ 576] 
15 0000004c`9edfe390 00007ffc`ea8930ed chrome_child!gpu::gles2::GLES2DecoderPassthroughImpl::DoCommands+0x25 [C:\b\c\b\win64_clang\src\gpu\command_buffer\service\gles2_cmd_decoder_passthrough.cc @ 517] 
16 0000004c`9edfe3c0 00007ffc`eb0fff97 chrome_child!gpu::CommandBufferService::Flush+0xef [C:\b\c\b\win64_clang\src\gpu\command_buffer\service\command_buffer_service.cc @ 90] 
17 0000004c`9edfe510 00007ffc`eb0ffdfa chrome_child!gpu::CommandBufferStub::OnAsyncFlush+0xb9 [C:\b\c\b\win64_clang\src\gpu\ipc\service\command_buffer_stub.cc @ 614] 
18 0000004c`9edfe660 00007ffc`eb0feb3f chrome_child!IPC::MessageT<GpuCommandBufferMsg_AsyncFlush_Meta,std::tuple<int,unsigned int>,void>::Dispatch<gpu::CommandBufferStub,gpu::CommandBufferStub,void,void (gpu::CommandBufferStub::*)(int, unsigned int)>+0x92 [C:\b\c\b\win64_clang\src\ipc\ipc_message_templates.h @ 146] 
19 0000004c`9edfe760 00007ffc`eaa09cd6 chrome_child!gpu::CommandBufferStub::OnMessageReceived+0x219 [C:\b\c\b\win64_clang\src\gpu\ipc\service\command_buffer_stub.cc @ 280] 
1a 0000004c`9edfe990 00007ffc`eaa08802 chrome_child!gpu::GpuChannel::HandleMessageHelper+0x32 [C:\b\c\b\win64_clang\src\gpu\ipc\service\gpu_channel.cc @ 541] 
1b 0000004c`9edfe9d0 00007ffc`eaa00469 chrome_child!gpu::GpuChannel::HandleMessage+0x5e [C:\b\c\b\win64_clang\src\gpu\ipc\service\gpu_channel.cc @ 517] 
1c 0000004c`9edfea70 00007ffc`e8b8d2cc chrome_child!gpu::Scheduler::RunNextTask+0x2dd [C:\b\c\b\win64_clang\src\gpu\command_buffer\service\scheduler.cc @ 526] 
1d 0000004c`9edfebe0 00007ffc`e8b8cb37 chrome_child!base::debug::TaskAnnotator::RunTask+0x12c [C:\b\c\b\win64_clang\src\base\debug\task_annotator.cc @ 101] 
1e 0000004c`9edfed00 00007ffc`e8b87ac8 chrome_child!base::MessageLoop::RunTask+0x247 [C:\b\c\b\win64_clang\src\base\message_loop\message_loop.cc @ 423] 
1f 0000004c`9edfee60 00007ffc`e8b87909 chrome_child!base::MessageLoop::DoWork+0x198 [C:\b\c\b\win64_clang\src\base\message_loop\message_loop.cc @ 480] 
20 0000004c`9edff050 00007ffc`e8b87621 chrome_child!base::MessagePumpDefault::Run+0x99 [C:\b\c\b\win64_clang\src\base\message_loop\message_pump_default.cc @ 37] 
21 0000004c`9edff0b0 00007ffc`ea5e93bb chrome_child!base::RunLoop::Run+0x31 [C:\b\c\b\win64_clang\src\base\run_loop.cc @ 108] 
22 0000004c`9edff0e0 00007ffc`ea24fbea chrome_child!content::GpuMain+0x397 [C:\b\c\b\win64_clang\src\content\gpu\gpu_main.cc @ 348] 
23 0000004c`9edff3e0 00007ffc`e8b44bdb chrome_child!content::ContentMainRunnerImpl::Run+0x1ee [C:\b\c\b\win64_clang\src\content\app\content_main_runner_impl.cc @ 951] 
24 0000004c`9edff590 00007ffc`e8b447d8 chrome_child!service_manager::Main+0x336 [C:\b\c\b\win64_clang\src\services\service_manager\embedder\main.cc @ 472] 
25 0000004c`9edff8a0 00007ffc`e8b41c3d chrome_child!content::ContentMain+0x41 [C:\b\c\b\win64_clang\src\content\app\content_main.cc @ 19] 
26 0000004c`9edff930 00007ff6`8851372c chrome_child!ChromeMain+0x118 [C:\b\c\b\win64_clang\src\chrome\app\chrome_main.cc @ 104] 
27 0000004c`9edffa10 00007ff6`88511699 chrome!MainDllLoader::Launch+0x26c [C:\b\c\b\win64_clang\src\chrome\app\main_dll_loader_win.cc @ 201] 
28 0000004c`9edffb00 00007ff6`885d4a72 chrome!wWinMain+0x699 [C:\b\c\b\win64_clang\src\chrome\app\chrome_exe_main_win.cc @ 230] 
29 0000004c`9edffee0 00007ffd`39dd3034 chrome!__scrt_common_main_seh+0x106 [f:\dd\vctools\crt\vcstartup\src\startup\exe_common.inl @ 283] 
2a 0000004c`9edfff20 00007ffd`3a4d1551 KERNEL32!BaseThreadInitThunk+0x14
2b 0000004c`9edfff50 00000000`00000000 ntdll!RtlUserThreadStart+0x21
3:034> lmv m chrome
Browse full module list
start             end                 module name
00007ff6`88510000 00007ff6`88682000   chrome     (private pdb symbols)  c:\symcache\chrome\chrome.exe.pdb\87C912AE57111EE90B876C7F2D30397F1\chrome.exe.pdb
    Loaded symbol image file: C:\Program Files (x86)\Google\Chrome\Application\chrome.exe
    Image path: chrome.exe
    Image name: chrome.exe
    Browse all global symbols  functions  data
    Timestamp:        Mon Sep  3 13:30:31 2018 (5B8D99E7)
    CheckSum:         0017457D
    ImageSize:        00172000
    File version:     69.0.3497.81
    Product version:  69.0.3497.81
    File flags:       0 (Mask 17)
    File OS:          4 Unknown Win32
    File type:        1.0 App
    File date:        00000000.00000000
    Translations:     0409.04b0
    Information from resource tables:
        CompanyName:      Google Inc.
        ProductName:      Google Chrome
        InternalName:     chrome_exe
        OriginalFilename: chrome.exe
        ProductVersion:   69.0.3497.81
        FileVersion:      69.0.3497.81
        FileDescription:  Google Chrome
        LegalCopyright:   Copyright 2017 Google Inc. All rights reserved.


## Attachments

- [texstor11.html](attachments/texstor11.html) (text/plain, 2.1 KB)

## Timeline

### cl...@chromium.org (2018-09-05)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5165834497163264.

### cl...@chromium.org (2018-09-05)

Testcase 5165834497163264 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=5165834497163264.

### cl...@chromium.org (2018-09-05)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5674188034277376.

### mp...@google.com (2018-09-05)

Thanks for the bug report!

@jmadill and @cwallez, can you please investigate and assign a good owner?

[Monorail components: Internals>GPU>ANGLE]

### jm...@chromium.org (2018-09-05)

Thanks for the report. I'll take a look at this first thing tomorrow.

### sh...@chromium.org (2018-09-06)

[Empty comment from Monorail migration]

### jm...@chromium.org (2018-09-07)

This is a regression where the unpack buffer is used when initializing an incomplete texture. It only happens when rendering with an incomplete texture when an unpack buffer is bound. I'll look at making a fix.

### bu...@chromium.org (2018-09-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/0d0fb43f34eeea20bf78089ca2a4e1f2831cffe5

commit 0d0fb43f34eeea20bf78089ca2a4e1f2831cffe5
Author: Jamie Madill <jmadill@chromium.org>
Date: Tue Sep 11 01:43:38 2018

Pass unpack buffer as explicit parameter to texSubImage.

This allows us to override it in the incomplete texture init. Any
back-end that used incomplete textures was vulnerable to a bug where
the unpack buffer would be used to initialize the incomplete texture.

Bug: chromium:880906
Change-Id: Ica558e4a4d81de9212f0bc6619ccd812a048ad45
Reviewed-on: https://chromium-review.googlesource.com/1214207
Reviewed-by: Yuly Novikov <ynovikov@chromium.org>
Reviewed-by: Frank Henigman <fjhenigman@chromium.org>
Commit-Queue: Jamie Madill <jmadill@chromium.org>

[modify] https://crrev.com/0d0fb43f34eeea20bf78089ca2a4e1f2831cffe5/src/libANGLE/renderer/renderer_utils.cpp
[modify] https://crrev.com/0d0fb43f34eeea20bf78089ca2a4e1f2831cffe5/src/libANGLE/Texture.cpp
[modify] https://crrev.com/0d0fb43f34eeea20bf78089ca2a4e1f2831cffe5/src/libANGLE/renderer/null/TextureNULL.h
[modify] https://crrev.com/0d0fb43f34eeea20bf78089ca2a4e1f2831cffe5/src/libANGLE/renderer/vulkan/TextureVk.cpp
[modify] https://crrev.com/0d0fb43f34eeea20bf78089ca2a4e1f2831cffe5/src/libANGLE/renderer/d3d/TextureD3D.cpp
[modify] https://crrev.com/0d0fb43f34eeea20bf78089ca2a4e1f2831cffe5/src/libANGLE/Context.cpp
[modify] https://crrev.com/0d0fb43f34eeea20bf78089ca2a4e1f2831cffe5/src/libANGLE/renderer/gl/TextureGL.h
[modify] https://crrev.com/0d0fb43f34eeea20bf78089ca2a4e1f2831cffe5/src/tests/gl_tests/IncompleteTextureTest.cpp
[modify] https://crrev.com/0d0fb43f34eeea20bf78089ca2a4e1f2831cffe5/src/libANGLE/renderer/TextureImpl.h
[modify] https://crrev.com/0d0fb43f34eeea20bf78089ca2a4e1f2831cffe5/src/libANGLE/renderer/d3d/TextureD3D.h
[modify] https://crrev.com/0d0fb43f34eeea20bf78089ca2a4e1f2831cffe5/src/libANGLE/renderer/null/TextureNULL.cpp
[modify] https://crrev.com/0d0fb43f34eeea20bf78089ca2a4e1f2831cffe5/src/libANGLE/Texture.h
[modify] https://crrev.com/0d0fb43f34eeea20bf78089ca2a4e1f2831cffe5/src/libANGLE/renderer/TextureImpl_mock.h
[modify] https://crrev.com/0d0fb43f34eeea20bf78089ca2a4e1f2831cffe5/src/libANGLE/renderer/vulkan/TextureVk.h
[modify] https://crrev.com/0d0fb43f34eeea20bf78089ca2a4e1f2831cffe5/src/libANGLE/renderer/gl/TextureGL.cpp


### bu...@chromium.org (2018-09-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/db0c0fa2872a51e9795e926b46f20d8eec21b032

commit db0c0fa2872a51e9795e926b46f20d8eec21b032
Author: angle-chromium-autoroll <angle-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com>
Date: Tue Sep 11 05:08:41 2018

Roll src/third_party/angle 63aa0e5b7001..0d0fb43f34ee (1 commits)

https://chromium.googlesource.com/angle/angle.git/+log/63aa0e5b7001..0d0fb43f34ee


git log 63aa0e5b7001..0d0fb43f34ee --date=short --no-merges --format='%ad %ae %s'
2018-09-11 jmadill@chromium.org Pass unpack buffer as explicit parameter to texSubImage.


Created with:
  gclient setdep -r src/third_party/angle@0d0fb43f34ee

The AutoRoll server is located here: https://autoroll.skia.org/r/angle-chromium-autoroll

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, please contact the current sheriff, who should
be CC'd on the roll, and stop the roller if necessary.

CQ_INCLUDE_TRYBOTS=luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel

BUG=chromium:880906
TBR=ynovikov@chromium.org

Change-Id: I83ce6ccf2c62c770845912f19ef043d6cd3c374e
Reviewed-on: https://chromium-review.googlesource.com/1217815
Reviewed-by: angle-chromium-autoroll <angle-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com>
Commit-Queue: angle-chromium-autoroll <angle-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#590205}
[modify] https://crrev.com/db0c0fa2872a51e9795e926b46f20d8eec21b032/DEPS


### jm...@chromium.org (2018-09-14)

This is fixed in Canary. I believe the fix made it into 70. Marking merge request to 69. It's been baking in Canary for a few days. Patch logic is fairly simple:

https://chromium-review.googlesource.com/1214207

Fixes a potential out of bounds reads that leads to a crash.

### sh...@chromium.org (2018-09-14)

[Empty comment from Monorail migration]

### go...@chromium.org (2018-09-14)

Pls apply appropriate OSs label. 
M70 is already branched at 3538 on August 30th. This also need a merge to M70, pls request a merge to M70.

+awhalley@ for M69 merge review.

### jm...@chromium.org (2018-09-14)

Added Windows Label and M70 tag. You're right it does need a merge to 70.

### sh...@chromium.org (2018-09-14)

This bug requires manual review: DEPS changes referenced in bugdroid comments.
Please contact the milestone owner if you have questions.
Owners: benmason@(Android), kariahda@(iOS), geohsu@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ab...@chromium.org (2018-09-14)

Approved for M70 - branch:3538

### aw...@chromium.org (2018-09-14)

This'll need some time in 70 beta before being considered for 69 at this point.  Cheers!

### bu...@chromium.org (2018-09-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/05c729f336efb544e224444c2485a412bd3a66b3

commit 05c729f336efb544e224444c2485a412bd3a66b3
Author: Jamie Madill <jmadill@chromium.org>
Date: Fri Sep 14 19:14:22 2018

Pass unpack buffer as explicit parameter to texSubImage.

This allows us to override it in the incomplete texture init. Any
back-end that used incomplete textures was vulnerable to a bug where
the unpack buffer would be used to initialize the incomplete texture.

Cherry-picked to the chromium/3538 branch cleanly.

Bug: chromium:880906
Change-Id: Iead2a8c57674e8962915902d6d5896f44fe8ca88
Reviewed-on: https://chromium-review.googlesource.com/1227033
Reviewed-by: Jamie Madill <jmadill@chromium.org>

[modify] https://crrev.com/05c729f336efb544e224444c2485a412bd3a66b3/src/libANGLE/renderer/renderer_utils.cpp
[modify] https://crrev.com/05c729f336efb544e224444c2485a412bd3a66b3/src/libANGLE/Texture.cpp
[modify] https://crrev.com/05c729f336efb544e224444c2485a412bd3a66b3/src/libANGLE/renderer/null/TextureNULL.h
[modify] https://crrev.com/05c729f336efb544e224444c2485a412bd3a66b3/src/libANGLE/renderer/vulkan/TextureVk.cpp
[modify] https://crrev.com/05c729f336efb544e224444c2485a412bd3a66b3/src/libANGLE/renderer/d3d/TextureD3D.cpp
[modify] https://crrev.com/05c729f336efb544e224444c2485a412bd3a66b3/src/libANGLE/Context.cpp
[modify] https://crrev.com/05c729f336efb544e224444c2485a412bd3a66b3/src/libANGLE/renderer/gl/TextureGL.h
[modify] https://crrev.com/05c729f336efb544e224444c2485a412bd3a66b3/src/tests/gl_tests/IncompleteTextureTest.cpp
[modify] https://crrev.com/05c729f336efb544e224444c2485a412bd3a66b3/src/libANGLE/renderer/TextureImpl.h
[modify] https://crrev.com/05c729f336efb544e224444c2485a412bd3a66b3/src/libANGLE/renderer/d3d/TextureD3D.h
[modify] https://crrev.com/05c729f336efb544e224444c2485a412bd3a66b3/src/libANGLE/renderer/null/TextureNULL.cpp
[modify] https://crrev.com/05c729f336efb544e224444c2485a412bd3a66b3/src/libANGLE/Texture.h
[modify] https://crrev.com/05c729f336efb544e224444c2485a412bd3a66b3/src/libANGLE/renderer/TextureImpl_mock.h
[modify] https://crrev.com/05c729f336efb544e224444c2485a412bd3a66b3/src/libANGLE/renderer/vulkan/TextureVk.h
[modify] https://crrev.com/05c729f336efb544e224444c2485a412bd3a66b3/src/libANGLE/renderer/gl/TextureGL.cpp


### aw...@chromium.org (2018-09-17)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-09-27)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-09-28)

Thanks omair@! The VRP panel decided to award $1,000 for this report. Cheers!

### aw...@chromium.org (2018-09-28)

[Empty comment from Monorail migration]

### go...@chromium.org (2018-10-08)

We're not planning any further M69 releases, Rejecting merge to M69.

### aw...@google.com (2018-10-15)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-10-16)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-11-12)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-12-21)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-06)

This issue was migrated from crbug.com/chromium/880906?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-03-12)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092368)*
