# SUMMARY: AddressSanitizer: stack-use-after-scope renderer11_utils.cpp:2299 in rx::d3d11::SetDebugName

| Field | Value |
|-------|-------|
| **Issue ID** | [40057460](https://issues.chromium.org/issues/40057460) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>GPU>ANGLE |
| **Platforms** | Windows |
| **Reporter** | m....@gmail.com |
| **Assignee** | ra...@microsoft.com |
| **Created** | 2021-09-30 |
| **Bounty** | $5,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4646.0 Safari/537.36

Steps to reproduce the problem:
chrome --no-sandbox --enable-blink-test-features --disable-extensions --user-data-dir=test poc.html

What is the expected behavior?

What went wrong?
note:
only reproduce on some machine,my local test is remotedesk to a windows system 

Type of crash
gpu process

#Analysis
Not Yet

#Patch
Not Yet

Did this work before? N/A 

Chrome version: 96.0.4646.0  Channel: n/a
OS Version: 10.0

#ASAN

=================================================================
==7568==ERROR: AddressSanitizer: stack-use-after-scope on address 0x126698dc6d37 at pc 0x7ff9f9c82762 bp 0x000a3edfd660 sp 0x000a3edfd6a8
READ of size 1 at 0x126698dc6d37 thread T0
==7568==WARNING: Failed to use and restart external symbolizer!
    #0 0x7ff9f9c82761 in rx::d3d11::SetDebugName C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\d3d\d3d11\renderer11_utils.cpp:2299
    #1 0x7ff9f9c69285 in rx::TextureStorage11_2DMultisample::ensureTextureExists C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\d3d\d3d11\TextureStorage11.cpp:3743
    #2 0x7ff9f9c4c37f in rx::TextureStorage11_2DMultisample::getRenderTarget C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\d3d\d3d11\TextureStorage11.cpp:3782
    #3 0x7ff9f9c4bc34 in rx::TextureStorage11::getMultisampledRenderTarget C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\d3d\d3d11\TextureStorage11.cpp:953
    #4 0x7ff9f9c4fe7a in rx::TextureStorage11_2D::getRenderTarget C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\d3d\d3d11\TextureStorage11.cpp:1347
    #5 0x7ff9f9cf89d8 in rx::TextureD3D::getAttachmentRenderTarget C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\d3d\TextureD3D.cpp:647
    #6 0x7ff9f9bc4445 in rx::RenderTargetCache<rx::RenderTarget11>::updateCachedRenderTarget C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\RenderTargetCache.h:163
    #7 0x7ff9f9bc4299 in rx::RenderTargetCache<rx::RenderTarget11>::updateColorRenderTarget C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\RenderTargetCache.h:137
    #8 0x7ff9f9bc4048 in rx::RenderTargetCache<rx::RenderTarget11>::update C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\RenderTargetCache.h:97
    #9 0x7ff9f9bc3e78 in rx::Framebuffer11::syncState C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\d3d\d3d11\Framebuffer11.cpp:398
    #10 0x7ff9f96f5723 in gl::Framebuffer::syncState C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\Framebuffer.cpp:2051
    #11 0x7ff9f960d745 in GL_DrawArrays C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libGLESv2\entry_points_gles_2_0_autogen.cpp:1063
    #12 0x7ffa091cd020 in `anonymous namespace'::FillRectOpImpl::onExecute C:\b\s\w\ir\cache\builder\src\third_party\skia\src\gpu\ops\FillRectOp.cpp:320
    #13 0x7ffa091db507 in GrOp::execute C:\b\s\w\ir\cache\builder\src\third_party\skia\src\gpu\ops\GrOp.h:193
    #14 0x7ffa091da7d0 in skgpu::v1::OpsTask::onExecute C:\b\s\w\ir\cache\builder\src\third_party\skia\src\gpu\ops\OpsTask.cpp:657
    #15 0x7ffa136fd92b in skgpu::v1::AtlasRenderTask::onExecute C:\b\s\w\ir\cache\builder\src\third_party\skia\src\gpu\ops\AtlasRenderTask.cpp:177
    #16 0x7ffa0909ab7a in GrDrawingManager::executeRenderTasks C:\b\s\w\ir\cache\builder\src\third_party\skia\src\gpu\GrDrawingManager.cpp:328
    #17 0x7ffa09098cfa in GrDrawingManager::flush C:\b\s\w\ir\cache\builder\src\third_party\skia\src\gpu\GrDrawingManager.cpp:234
    #18 0x7ffa0909b4c2 in GrDrawingManager::flushSurfaces C:\b\s\w\ir\cache\builder\src\third_party\skia\src\gpu\GrDrawingManager.cpp:533
    #19 0x7ffa06847ee6 in GrDirectContextPriv::flushSurfaces C:\b\s\w\ir\cache\builder\src\third_party\skia\src\gpu\GrDirectContextPriv.cpp:60
    #20 0x7ffa06927bf8 in SkSurface_Gpu::onFlush C:\b\s\w\ir\cache\builder\src\third_party\skia\src\image\SkSurface_Gpu.cpp:217
    #21 0x7ffa0d157ee5 in gpu::raster::RasterDecoderImpl::FlushAndSubmitIfNecessary C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\raster_decoder.cc:824
    #22 0x7ffa0d164759 in gpu::raster::RasterDecoderImpl::DoEndRasterCHROMIUM C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\raster_decoder.cc:3820
    #23 0x7ffa0d14800e in gpu::raster::RasterDecoderImpl::HandleEndRasterCHROMIUM C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\raster_decoder_autogen.h:161
    #24 0x7ffa0d14f353 in gpu::raster::RasterDecoderImpl::DoCommandsImpl<0> C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\raster_decoder.cc:1593
    #25 0x7ffa0d14dbce in gpu::raster::RasterDecoderImpl::DoCommands C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\raster_decoder.cc:1653
    #26 0x7ffa09fcc53a in gpu::CommandBufferService::Flush C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\command_buffer_service.cc:70
    #27 0x7ffa075b2dd4 in gpu::CommandBufferStub::OnAsyncFlush C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command_buffer_stub.cc:501
    #28 0x7ffa075b1f88 in gpu::CommandBufferStub::ExecuteDeferredRequest C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command_buffer_stub.cc:152
    #29 0x7ffa075bec66 in gpu::GpuChannel::ExecuteDeferredRequest C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\gpu_channel.cc:666
    #30 0x7ffa075c9d8f in base::internal::Invoker<base::internal::BindState<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>),base::WeakPtr<gpu::GpuChannel>,mojo::StructPtr<gpu::mojom::DeferredRequestParams> >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind_internal.h:690
    #31 0x7ffa071eda0e in gpu::Scheduler::RunNextTask C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler.cc:688
    #32 0x7ffa05f70eba in base::TaskAnnotator::RunTask C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:178
    #33 0x7ffa08a3fd0f in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:357
    #34 0x7ffa08a3f428 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:260
    #35 0x7ffa08a19397 in base::MessagePumpDefault::Run C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_default.cc:38
    #36 0x7ffa08a41125 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:462
    #37 0x7ffa05ef3f23 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:134
    #38 0x7ffa0844f2c9 in content::GpuMain C:\b\s\w\ir\cache\builder\src\content\gpu\gpu_main.cc:430
    #39 0x7ffa01c57071 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:985
    #40 0x7ffa01c53a56 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:390
    #41 0x7ffa01c54a98 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:418
    #42 0x7ff9fb67147f in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:172
    #43 0x7ff65bd55bc4 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:169
    #44 0x7ff65bd52c31 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:382
    #45 0x7ff65c143fcf in __scrt_common_main_seh d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #46 0x7ffa518e7973 in BaseThreadInitThunk+0x13 (C:\WINDOWS\System32\KERNEL32.DLL+0x180017973)
    #47 0x7ffa522ea2f0 in RtlUserThreadStart+0x20 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x18005a2f0)

Address 0x126698dc6d37 is located in stack of thread T0 at offset 55 in frame
    #0 0x7ff9f9c4b711 in rx::TextureStorage11::getMultisampledRenderTarget C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\d3d\d3d11\TextureStorage11.cpp:929

  This frame has 6 object(s):
    [32, 56) 'ref.tmp' (line 942) <== Memory access at offset 55 is inside this variable
    [96, 112) 'area' (line 947)
    [128, 136) 'readRenderTarget' (line 948)
    [160, 176) 'indexMS' (line 951)
    [192, 200) 'drawRenderTarget' (line 952)
    [224, 232) 'rt' (line 963)
HINT: this may be a false positive if your program uses some custom stack unwind mechanism, swapcontext or vfork
      (longjmp, SEH and C++ exceptions *are* supported)
SUMMARY: AddressSanitizer: stack-use-after-scope C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\d3d\d3d11\renderer11_utils.cpp:2299 in rx::d3d11::SetDebugName
Shadow bytes around the buggy address:
  0x04336b4b8d50: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5
  0x04336b4b8d60: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5
  0x04336b4b8d70: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5
  0x04336b4b8d80: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5
  0x04336b4b8d90: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5
=>0x04336b4b8da0: f1 f1 f1 f1 f8 f8[f8]f2 f2 f2 f2 f2 00 00 f2 f2
  0x04336b4b8db0: 00 f2 f2 f2 00 00 f2 f2 00 f2 f2 f2 f8 f3 f3 f3
  0x04336b4b8dc0: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5
  0x04336b4b8dd0: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5
  0x04336b4b8de0: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5
  0x04336b4b8df0: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07 
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
==7568==ABORTING
[7664:10756:0930/213059.896:ERROR:gpu_process_host.cc(967)] GPU process exited unexpectedly: exit_code=1

------------------
System Information
------------------
      Time of this report: 9/30/2021, 22:22:30
             Machine name: WIN-1H0N3JFSDPF
               Machine Id: {17FDCF55-7A28-4203-80B2-7F02400E1CE1}
         Operating System: Windows Server 2019 Standard 64-bit (10.0, Build 17763) (17763.rs5_release.180914-1434)
                 Language: English (Regional Setting: English)
      System Manufacturer: System manufacturer
             System Model: System Product Name
                     BIOS: BIOS Date: 07/08/19 14:04:20 Ver: 05.0000E (type: BIOS)
                Processor: AMD Ryzen 9 3950X 16-Core Processor             (16 CPUs), ~3.5GHz
                   Memory: 65446MB RAM
      Available OS Memory: 65446MB RAM
                Page File: 3025MB used, 72147MB available
              Windows Dir: C:\WINDOWS
          DirectX Version: DirectX 12
      DX Setup Parameters: Not found
         User DPI Setting: 120 DPI (125 percent)
       System DPI Setting: 96 DPI (100 percent)
          DWM DPI Scaling: Disabled
                 Miracast: Available, no HDCP
Microsoft Graphics Hybrid: Not Supported
           DxDiag Version: 10.00.17763.0001 64bit Unicode

--------------------
DirectX Debug Levels
--------------------
Direct3D:    0/4 (retail)
DirectDraw:  0/4 (retail)
DirectInput: 0/5 (retail)
DirectMusic: 0/5 (retail)
DirectPlay:  0/9 (retail)
DirectSound: 0/5 (retail)
DirectShow:  0/6 (retail)

---------------
Display Devices
---------------
           Card name: NVIDIA GeForce GTX 650 Ti
        Manufacturer: NVIDIA
           Chip type: GeForce GTX 650 Ti
            DAC type: Integrated RAMDAC
         Device Type: Full Device (POST)
          Device Key: Enum\PCI\VEN_10DE&DEV_11C6&SUBSYS_28071462&REV_A1
       Device Status: 0180200A [DN_DRIVER_LOADED|DN_STARTED|DN_DISABLEABLE|DN_NT_ENUMERATOR|DN_NT_DRIVER] 
 Device Problem Code: No Problem
 Driver Problem Code: Unknown
      Display Memory: 33707 MB
    Dedicated Memory: 984 MB
       Shared Memory: 32722 MB
        Current Mode: 2560 x 1440 (32 bit) (32Hz)
         HDR Support: Unknown
    Display Topology: Unknown
 Display Color Space: DXGI_COLOR_SPACE_RGB_FULL_G22_NONE_P709
     Color Primaries: Red(0.000000,0.000000), Green(0.000000,0.000000), Blue(0.000000,0.000000), White Point(0.000000,0.000000)
   Display Luminance: Min Luminance = 0.000000, Max Luminance = 0.000000, MaxFullFrameLuminance = 0.000000
         Driver Name: C:\WINDOWS\System32\DriverStore\FileRepository\nv_dispi.inf_amd64_324f172f3e662ec5\nvldumdx.dll,C:\WINDOWS\System32\DriverStore\FileRepository\nv_dispi.inf_amd64_324f172f3e662ec5\nvldumdx.dll,C:\WINDOWS\System32\DriverStore\FileRepository\nv_dispi.inf_amd64_324f172f3e662ec5\nvldumdx.dll,C:\WINDOWS\System32\DriverStore\FileRepository\nv_dispi.inf_amd64_324f172f3e662ec5\nvldumdx.dll
 Driver File Version: 27.21.0014.5638 (English)
      Driver Version: 27.21.14.5638
         DDI Version: 12
      Feature Levels: 11_0,10_1,10_0,9_3,9_2,9_1
        Driver Model: WDDM 2.5
 Graphics Preemption: DMA
  Compute Preemption: DMA
            Miracast: Not Supported
 Hybrid Graphics GPU: Not Supported
      Power P-states: Not Supported
      Virtualization: Paravirtualization 
          Block List: No Blocks
  Catalog Attributes: Universal:False Declarative:False 
   Driver Attributes: Final Retail
    Driver Date/Size: 14/09/2020 08:00:00, 1037840 bytes
         WHQL Logo'd: n/a
     WHQL Date Stamp: n/a
   Device Identifier: {D7B71E3E-5286-11CF-D461-09081BC2D635}
           Vendor ID: 0x10DE
           Device ID: 0x11C6
           SubSys ID: 0x28071462
         Revision ID: 0x00A1
  Driver Strong Name: oem20.inf:0f066de3500239da:Section004:27.21.14.5638:pci\ven_10de&dev_11c6
      Rank Of Driver: 00D12001
         Video Accel: Unknown
         DXVA2 Modes: DXVA2_ModeMPEG2_VLD  DXVA2_ModeVC1_D2010  DXVA2_ModeVC1_VLD  DXVA2_ModeH264_VLD_Stereo_Progressive_NoFGT  DXVA2_ModeH264_VLD_Stereo_NoFGT  DXVA2_ModeH264_VLD_NoFGT  DXVA2_ModeHEVC_VLD_Main  DXVA2_ModeMPEG4pt2_VLD_Simple  DXVA2_ModeMPEG4pt2_VLD_AdvSimple_NoGMC  
      Deinterlace Caps: n/a
        D3D9 Overlay: Supported
             DXVA-HD: Supported
        DDraw Status: Not Available
          D3D Status: Enabled
          AGP Status: Not Available
       MPO MaxPlanes: 1
            MPO Caps: Not Supported
         MPO Stretch: Not Supported
     MPO Media Hints: Not Supported
         MPO Formats: Not Supported
    PanelFitter Caps: Not Supported
 PanelFitter Stretch: Not Supported

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 19.1 KB)

## Timeline

### [Deleted User] (2021-09-30)

[Empty comment from Monorail migration]

### m....@gmail.com (2021-09-30)

asan-win32-release_x64-922637 NOT REPRODUCE
asan-win32-release_x64-926627  REPRODUCE


### rs...@chromium.org (2021-09-30)

It's not immediately obvious from your repro if "--no-sandbox --enable-blink-test-features" are necessary. Does this reproduce for you without these?

### m....@gmail.com (2021-09-30)

re https://crbug.com/chromium/1254746#c3
--no-sandbox is for get the asan log.
--enable-blink-test-features is not necessary.

### cl...@chromium.org (2021-09-30)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5406500401774592.

### rs...@chromium.org (2021-09-30)

jmadill: I kicked off a ClusterFuzz run here; at least based on the stack trace reported, I had a question: I can't find any documentation confirming that WKPDID_D3DDebugObjectName actually makes a copy of the input parameter. The examples provided (e.g. by Microsoft) seem to use constant strings that will not be deallocated. Given that Microsoft contributed the most recent change (in https://source.chromium.org/chromium/_/chromium/angle/angle.git/+/5e02940105dbfda6f057f6cca12b46e008136632 ), would it be possible to confirm that it is indeed safe to use?

I'm just curious whether this is "safe" (to use the stack-local storage here)

[Monorail components: Internals>GPU>ANGLE]

### jm...@chromium.org (2021-09-30)

Adding MS to this issue, as it's likely caused by one of the recent changes. Rafael can you help diagnose the issue here?

### ra...@microsoft.com (2021-09-30)

@rsleevi, SetPrivateDebugLabel used with the WKPDID_D3DDebugObjectName GUID will make a copy of the passed in string and frees the copy when the D3D object is released. 

Is ClusterFuzz finding that the passed in string points to invalid/freed memory?  If so, we should revert the change and reland when the bug is fixed.

### rs...@chromium.org (2021-09-30)

re: https://crbug.com/chromium/1254746#c8 - I'm still working through to try and reproduce this :) Right now all we have is the report, and ClusterFuzz for Windows is a bit backed up at the moment. So right now, this is just trying to good faith debug and try to see if I can narrow down and find a repro.

### ra...@microsoft.com (2021-09-30)

[Empty comment from Monorail migration]

### ra...@microsoft.com (2021-09-30)

SetPrivateDebugLabel is always passed member variables from instances of Resource11Base.  

All strings that end up in Resource11Base::mInternalDebugName come from hardcoded strings in the ANGLE DLL and not from the heap.  We should good here from a reliability perspective.

Resource11Base::mKhrDebugName comes from the TextureStorage::mTextureLabel const reference. TextureStorage::mTextureLabel is assigned from TextureImpl::mState's getLabel method. getLabel always returns a const reference to its mLabel member variable. 

If it is the case that Resource11Base instances ever outlive their TextureStorage and TextureImpl outer classes, we have bug we need to fix. From talking with Geoff at the onset of the work, I do not believe this is the case.  

@Geoff and @Jamie, please correct me if I am wrong in the above.

### rs...@chromium.org (2021-10-01)

adetaylor pointed out a likely candidate:

On line https://source.chromium.org/chromium/_/chromium/angle/angle/+/5090cb22e9ce716623524dbf5098534c1a45642e:src/libANGLE/renderer/d3d/d3d11/TextureStorage11.cpp;l=942-944;drc=c9dcc5535edadfeb722202e1cc7da6ebb77152a1 , the last parameter passed is ""

However, the signature here is "const std::string &label", so a temporary string is created (converting the const char* into an std::string implicitly)

This goes through https://source.chromium.org/chromium/_/chromium/angle/angle.git/+/0b4508e5d9177b3c3919ad73b4fc74e8d1184380:src/libANGLE/renderer/d3d/d3d11/Renderer11.cpp;l=3376-3386;drc=20be5bed84f184175a273042a4d1f49d20bfe3f0 and into https://source.chromium.org/chromium/_/chromium/angle/angle.git/+/0b4508e5d9177b3c3919ad73b4fc74e8d1184380:src/libANGLE/renderer/d3d/d3d11/TextureStorage11.cpp;l=3659-3672;drc=5e02940105dbfda6f057f6cca12b46e008136632 , which passes this "const std::string&" further into the TextSture11ImmutableBase ( https://source.chromium.org/chromium/_/chromium/angle/angle.git/+/0b4508e5d9177b3c3919ad73b4fc74e8d1184380:src/libANGLE/renderer/d3d/d3d11/TextureStorage11.cpp;l=1817-1823;drc=5e02940105dbfda6f057f6cca12b46e008136632 ) and the TextureStorage11 ( https://source.chromium.org/chromium/_/chromium/angle/angle.git/+/0b4508e5d9177b3c3919ad73b4fc74e8d1184380:src/libANGLE/renderer/d3d/d3d11/TextureStorage11.cpp;l=78-83;drc=5e02940105dbfda6f057f6cca12b46e008136632 ), which ultimately passes it into TextureStorage ( https://source.chromium.org/chromium/_/chromium/angle/angle.git/+/8d1e74abd5d65d39b7b1249af3bf83cfe30855d0:src/libANGLE/renderer/d3d/TextureStorage.h;l=43;drc=2e2aee0550b8ff482c0329bad62f71c49407d40a )

TextureStorage stores this const-ref into mTextureLabel, https://source.chromium.org/chromium/_/chromium/angle/angle.git/+/8d1e74abd5d65d39b7b1249af3bf83cfe30855d0:src/libANGLE/renderer/d3d/TextureStorage.h;l=92;drc=2e2aee0550b8ff482c0329bad62f71c49407d40a

However, after this statement is completed, the reference mTextureLabel is now to a temporary which no longer exists. This does appear to have regressed in July, in https://source.chromium.org/chromium/_/chromium/angle/angle.git/+/c9dcc5535edadfeb722202e1cc7da6ebb77152a1 . Prior to this, the label was stored as a full copy ("std::string mLabel") on the Texture, but it was made const-ref on the TextureStorage.

A simple fix would be making a copy ("std::string") again.

This was a latent bug, until https://source.chromium.org/chromium/_/chromium/angle/angle.git/+/5e02940105dbfda6f057f6cca12b46e008136632 , which began access mTextureLabel, and revealing it. However, if there were other users of mTextureLabel before then, they would also have been unsafe.

### [Deleted User] (2021-10-01)

[Empty comment from Monorail migration]

### ra...@microsoft.com (2021-10-01)

@rsleevi, thank you for your in-depth analysis!

Actually, I think the following change was the one that cause the freed pointer to be read but it got relatively limited use.  
    3067921: Implement onLabelUpdate method. | https://chromium-review.googlesource.com/c/angle/angle/+/3067921

The recent change you linked to was the one which spread the reading to more places.  

I agree making a copy of the string would be one fix. Another, somewhat more risky one, is to pass mTextureLabel as the last parameter to createTextureStorage2DMultisample instead of "". 

### rs...@chromium.org (2021-10-02)

It was all adetaylor's doing :) I'm just the messenger.

I'd like to try to confirm that this is only M96 - the original problem seems to have been introduced in July, but as you point out, different CLs may have surfaced it. In this case, it's not necessarily a freed pointer (which, OK, is definitely not good :D) - it's the binding a reference to a temporary, which is equally subtle. Having the copy there definitely seems safer, because the risks of creating a temporary and not realizing it seem significantly greater and more subtle.

### ra...@microsoft.com (2021-10-02)

The original code was trying to avoid having a copy for every abstraction layer in ANGLE. There is another, similar pointer in Resource11Base.

Taking a step back ... one potential solution that gives us both safety and avoid copies is to have all of the abstraction layers have a std::string instance but only the deepest level std::string instance has the string allocation. As the deeper abstractions objects are created (they're not present at the beginning), the string is std::moved "further in". getLabel would ask the deepest abstraction object for the label.  

The above is an involved change so for the purposes of fixing the immediate regression (and CP it to other branches) we should make a copy.    

### [Deleted User] (2021-10-02)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-10-02)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@microsoft.com (2021-10-02)

Working on the fix and will create a fix soon.

### ad...@microsoft.com (2021-10-02)

CL created for the fix
3201030: Fix ASAN bug caused by passing empty label string. | https://chromium-review.googlesource.com/c/angle/angle/+/3201030

### rs...@chromium.org (2021-10-03)

[Empty comment from Monorail migration]

### xi...@chromium.org (2021-10-11)

[Empty comment from Monorail migration]

### xi...@chromium.org (2021-10-11)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-10-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/d8471b290ccb5084ab93881250624cc15808cef8

commit d8471b290ccb5084ab93881250624cc15808cef8
Author: Aditya Kushwah <adkushwa@microsoft.com>
Date: Sat Oct 02 17:36:33 2021

Fix ASAN bug caused by passing empty label string.

This CL will fix the ASAN bug that was caused by passing empty label
string to getMultisampledRenderTarget, function of TextureStorage11.
Instead, pass mTextureLabel so we can get WebGL labels now. Also to
avoid this in future, convert ref mTextureLabel to now store copy.

The change in the test reflects the steps to first set the label
string and later the label being used to initialize mTextureLabel via
texture storage creation.

Bug: chromium:1254746
Change-Id: I007bdf1c7a421a2b4b9288aa71fa4368c14cf333
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3201030
Reviewed-by: Rafael Cintron <rafael.cintron@microsoft.com>
Reviewed-by: Jamie Madill <jmadill@chromium.org>
Commit-Queue: Rafael Cintron <rafael.cintron@microsoft.com>

[modify] https://crrev.com/d8471b290ccb5084ab93881250624cc15808cef8/src/libANGLE/renderer/d3d/d3d11/TextureStorage11.cpp
[modify] https://crrev.com/d8471b290ccb5084ab93881250624cc15808cef8/src/tests/gl_tests/TextureTest.cpp
[modify] https://crrev.com/d8471b290ccb5084ab93881250624cc15808cef8/src/libANGLE/renderer/d3d/TextureStorage.h


### gi...@appspot.gserviceaccount.com (2021-10-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/85650c29ebb3371d5e96123a321c5aec69ba37ea

commit 85650c29ebb3371d5e96123a321c5aec69ba37ea
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Thu Oct 14 03:48:39 2021

Roll ANGLE from ea5804842bfe to d8471b290ccb (3 revisions)

https://chromium.googlesource.com/angle/angle.git/+log/ea5804842bfe..d8471b290ccb

2021-10-14 adkushwa@microsoft.com Fix ASAN bug caused by passing empty label string.
2021-10-13 yuxinhu@google.com README.md maintenance
2021-10-13 yuxinhu@google.com Add fixes on the doc based on Jamie's Suggestions

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/angle-chromium-autoroll
Please CC jonahr@google.com on the revert to ensure that a human
is aware of the problem.

To file a bug in ANGLE: https://bugs.chromium.org/p/angleproject/issues/entry
To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86
Bug: chromium:1254746
Tbr: jonahr@google.com
Change-Id: I9aec9dcd845f04790873dc3bcd22a8e229dbb1d3
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3222201
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#931366}

[modify] https://crrev.com/85650c29ebb3371d5e96123a321c5aec69ba37ea/DEPS


### [Deleted User] (2021-10-16)

rafael.cintron: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@microsoft.com (2021-10-17)

The CL to resolve this bug is now merged:
3201030: Fix ASAN bug caused by passing empty label string. | https://chromium-review.googlesource.com/c/angle/angle/+/3201030

### ra...@microsoft.com (2021-10-18)

[Empty comment from Monorail migration]

### ad...@microsoft.com (2021-10-19)

The bug due to empty string being passed to const reference was surfaced when the following changes were checked in:

3192180: Add a new variant to the labeling API. | https://chromium-review.googlesource.com/c/angle/angle/+/3192180

and more specifically this line was called when making webpages with WebGL:

TextureStorage11.cpp - Chromium Code Search

While putting a breakpoint here, &mTextureLabel was getting "" string. What would have happened was:

createTextureStorage2DMultisample would have initialized the const ref mTextureLabel with empty string and when TextureStorage11_2DMultisample::ensureTextureExists was called, the &mTextureLabel would have accessed null const ref.

The changes are currently in Dev 96:
https://chromiumdash.appspot.com/commit/5e02940105dbfda6f057f6cca12b46e008136632

@rsleevi Should this fix be cherry picked in Dev 96? How should we proceed from here?

### rs...@chromium.org (2021-10-19)

Amy/Ade: Checking with you, I thought Sheriffbot would automatically set the merge labels?

https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/sheriff.md#wrap-up-the-fixed-issue has the old labels (Security_Impact_{Beta,Stable}),  and I wasn't sure whether it's appropriate to manually request a merge here. It looks like M96 is still Dev, but wasn't sure based on https://www.chromium.org/Home/chromium-security/security-release-management which suggests we only merge Mediums if they're particularly worrisome (and I'm not sure if this counts, re: GPU sandbox).

### [Deleted User] (2021-10-19)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-19)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-19)

Requesting merge to dev M96 because latest trunk commit (931366) appears to be after dev branch point (929512).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-10-19)

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

### rs...@chromium.org (2021-10-19)

Ah, there we go :) It just took its time to run :)

### sr...@google.com (2021-10-19)

Merge approved for M96 branch:4664 please merge before 3pm PST to make it to tomorrow dev RC build

### ad...@microsoft.com (2021-10-19)

Thank you for the quick response and merge. :)

### gi...@appspot.gserviceaccount.com (2021-10-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/f4d94efbc335db33e007818fdc5bbc648596b716

commit f4d94efbc335db33e007818fdc5bbc648596b716
Author: Aditya Kushwah <adkushwa@microsoft.com>
Date: Sat Oct 02 17:36:33 2021

Fix ASAN bug caused by passing empty label string.

This CL will fix the ASAN bug that was caused by passing empty label
string to getMultisampledRenderTarget, function of TextureStorage11.
Instead, pass mTextureLabel so we can get WebGL labels now. Also to
avoid this in future, convert ref mTextureLabel to now store copy.

The change in the test reflects the steps to first set the label
string and later the label being used to initialize mTextureLabel via
texture storage creation.

Bug: chromium:1254746
Change-Id: I007bdf1c7a421a2b4b9288aa71fa4368c14cf333
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3201030
Reviewed-by: Rafael Cintron <rafael.cintron@microsoft.com>
Reviewed-by: Jamie Madill <jmadill@chromium.org>
Commit-Queue: Rafael Cintron <rafael.cintron@microsoft.com>
(cherry picked from commit d8471b290ccb5084ab93881250624cc15808cef8)
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3233839

[modify] https://crrev.com/f4d94efbc335db33e007818fdc5bbc648596b716/src/libANGLE/renderer/d3d/d3d11/TextureStorage11.cpp
[modify] https://crrev.com/f4d94efbc335db33e007818fdc5bbc648596b716/src/tests/gl_tests/TextureTest.cpp
[modify] https://crrev.com/f4d94efbc335db33e007818fdc5bbc648596b716/src/libANGLE/renderer/d3d/TextureStorage.h


### am...@google.com (2021-10-28)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-10-28)

Congratulations - the VRP Panel has decided to award you $5000 for this report. Nice work and thanks for your efforts! 

### am...@google.com (2021-10-29)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-26)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1254746?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1255396, crbug.com/chromium/1258296, crbug.com/chromium/1258375]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-03-12)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057460)*
