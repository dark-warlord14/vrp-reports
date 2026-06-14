# Security: Chrome webm rendering on OS X includes image artifacts from video memory

| Field | Value |
|-------|-------|
| **Issue ID** | [40086337](https://issues.chromium.org/issues/40086337) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Media>Video, Internals>GPU>Internals |
| **Platforms** | Mac |
| **Reporter** | da...@gmail.com |
| **Assignee** | kb...@chromium.org |
| **Created** | 2016-12-25 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

When displaying embedded webm videos, the most recent version of Chrome (and not other browsers) appears to be pulling image data either directly from the OS or from VRAM.

I can pick out fragments of other websites viewed in Chrome, as well as fragments of jpgs on my hard drive that were rendered in icon view within Finder.

If this is just a local video rendering issue, I'm not quite as concerned - though it's still very unnerving. But I don't know whether the image data from outside Chrome is interacting with / vulnerable to upload or exploitation by sites or code running within Chrome.

**VERSION**  

Chrome Version: 55.0.2883.95 [stable]  

Operating System: OS X 10.9.5

**REPRODUCTION CASE**  

Not sure how to reproduce. See attached screen capture of a video from the following url, as it renders in Chrome on my computer:  

<https://gfycat.com/ShamefulNaiveAmberpenshell>

## Attachments

- [Screen Shot 2016-12-25 at 2.48.12 PM.png](attachments/Screen Shot 2016-12-25 at 2.48.12 PM.png) (image/png, 180.3 KB)
- [Screen Shot 2017-01-09 at 8.20.14 AM.png](attachments/Screen Shot 2017-01-09 at 8.20.14 AM.png) (image/png, 748.5 KB)
- [Screen Shot 2017-01-10 at 5.40.43 PM.png](attachments/Screen Shot 2017-01-10 at 5.40.43 PM.png) (image/png, 467.5 KB)
- [about GPU.rtf](attachments/about GPU.rtf) (application/octet-stream, 56.8 KB)

## Timeline

### el...@chromium.org (2016-12-28)

Typically, these turn out to be bugs in video drivers and they aren't exploitable. Having said that, we'll definitely want more information-- can you provide exact details of which OS X hardware you're using (machine type, GPU info) as well as confirming that you have all updates from Apple installed? 

See https://crbug.com/chromium/477328, https://crbug.com/chromium/120949, etc.

### da...@gmail.com (2016-12-28)

Sure, it's a 15" MacBook Pro (Early 2008) with the NVIDIA GeForce 8600M GT 256MB. CPU is 2.4 GHz Intel Core 2 Duo.

The OS is 10.9.5 (Mavericks), and yes, all updates from Apple have been installed. Chrome is on the latest stable build: 55.0.2883.95 (64-bit)

In addition to webm videos, I noticed today that the same glitch happens with the extension Awesome Screenshot (https://chrome.google.com/webstore/detail/awesome-screenshot-screen/nlipoenfbbikpbjkfpfillcgkoblgpmj?hl=en). Instead of taking a screenshot, it will display a collage of artifacts from video memory. Though I should say, I've tried running Chrome with all extensions disabled - to make sure that none of them was causing the issue - and the glitch still happened on sites like gfycat.

### pa...@chromium.org (2016-12-29)

It would be a vulnerability if you could exfiltrate the video contents across origins, such as by painting them into a <canvas> and shipping them off to a web site (see e.g. https://html2canvas.hertzen.com/).

(You might think of using getUserMedia for screensharing, but I think the requirement that the person explicitly agree to screensharing stymies most realistic attack scenarios — a malicious web origin won't be able to invisibly spy on content from other origins. Unless I'm wrong! :) )

Passing to kbr for triage.

[Monorail components: Blink>Media>Video Internals>GPU]

### sh...@chromium.org (2016-12-29)

[Empty comment from Monorail migration]

### ke...@chromium.org (2016-12-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-12-31)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-01-09)

kbr: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### da...@gmail.com (2017-01-09)

Issue is still occurring. I've also noticed it on sites that don't appear to be related to webm rendering. For example, tumblr blogs that require the user to log in before browsing are affected, as you can see in the screenshot attached.

### da...@gmail.com (2017-01-11)

Also, yelp. There's strange artifacting at the bottom of the screen when I scroll on this page:
https://www.yelp.com/biz/izakaya-roku-san-francisco?osq=Restaurants&search_key=13561

### kb...@chromium.org (2017-01-11)

Reporter: could you please provide the contents of about:gpu from your system? A plaintext copy/paste is fine, and preferred. Thanks.

This is an ancient laptop not even running the current OS. We don't have any of these in house to test with. The response to fix this in the wild will be to disable GPU acceleration on it.


[Monorail components: -Internals>GPU Internals>GPU>Internals]

### da...@gmail.com (2017-01-11)

Sure, plain text below, RTF attached. I'd get a new MBP if Apple reintroduced a matte screen and a keyboard with actual travel :)

Graphics Feature Status
Canvas: Hardware accelerated
Flash: Hardware accelerated
Flash Stage3D: Hardware accelerated
Flash Stage3D Baseline profile: Hardware accelerated
Compositing: Hardware accelerated
Multiple Raster Threads: Disabled
Native GpuMemoryBuffers: Hardware accelerated
Rasterization: Software only, hardware acceleration unavailable
Video Decode: Hardware accelerated
Video Encode: Hardware accelerated
VPx Video Decode: Hardware accelerated
WebGL: Hardware accelerated
Driver Bug Workarounds
disable_av_sample_buffer_display_layer
disable_framebuffer_cmaa
disable_multimonitor_multisampling
get_frag_data_info_bug
needs_offscreen_buffer_workaround
pack_parameters_workaround_with_pack_buffer
regenerate_struct_names
rewrite_do_while_loops
scalarize_vec_and_mat_constructor_args
set_zero_level_before_generating_mipmap
unfold_short_circuit_as_ternary_operation
unpack_alignment_workaround_with_unpack_buffer
unpack_overlapping_rows_separately_unpack_buffer
use_intermediary_for_copy_texture_image
use_shadowed_tex_level_params
validate_multisample_buffer_allocation
Problems Detected
Some GPUs on Mac can perform poorly with GPU rasterization. Disable all known NVidia GPUs other than the Geforce 6xx and 7xx series, which have been tested.: 613272, 614468
Disabled Features: gpu_rasterization
There are display issues with GPU Raster on OSX 10.9: 611310
Disabled Features: gpu_rasterization
Work around a bug in offscreen buffers on NVIDIA GPUs on Macs: 89557
Applied Workarounds: needs_offscreen_buffer_workaround
Multisampling is buggy on OSX when multiple monitors are connected: 237931
Applied Workarounds: disable_multimonitor_multisampling
Multisampled renderbuffer allocation must be validated on some Macs: 290391
Applied Workarounds: validate_multisample_buffer_allocation
Unfold short circuit on Mac OS X: 307751
Applied Workarounds: unfold_short_circuit_as_ternary_operation
Always rewrite vec/mat constructors to be consistent: 398694
Applied Workarounds: scalarize_vec_and_mat_constructor_args
Mac drivers handle struct scopes incorrectly: 403957
Applied Workarounds: regenerate_struct_names
glGenerateMipmap fails if the zero texture level is not set on some Mac drivers: 560499
Applied Workarounds: set_zero_level_before_generating_mipmap
Pack parameters work incorrectly with pack buffer bound: 563714
Applied Workarounds: pack_parameters_workaround_with_pack_buffer
Alignment works incorrectly with unpack buffer bound: 563714
Applied Workarounds: unpack_alignment_workaround_with_unpack_buffer
copyTexImage2D fails when reading from IOSurface on multiple GPU types.: 581777
Applied Workarounds: use_intermediary_for_copy_texture_image
Unpacking overlapping rows from unpack buffers is unstable on NVIDIA GL driver: 596774
Applied Workarounds: unpack_overlapping_rows_separately_unpack_buffer
Mac Drivers store texture level parameters on int16_t that overflow: 610153
Applied Workarounds: use_shadowed_tex_level_params
Limited enabling of Chromium GL_INTEL_framebuffer_CMAA: 535198
Applied Workarounds: disable_framebuffer_cmaa
glGetFragData{Location|Index} works incorrectly on Max: 638340
Applied Workarounds: get_frag_data_info_bug
Rewrite do-while loops to simpler constructs on Mac: 644669
Applied Workarounds: rewrite_do_while_loops
AVSampleBufferDisplayLayer leaks IOSurfaces on 10.9.: 632178
Applied Workarounds: disable_av_sample_buffer_display_layer
Raster is using a single thread.
Disabled Features: multiple_raster_threads
Version Information
Data exported	1/10/2017, 5:49:13 PM
Chrome version	Chrome/55.0.2883.95
Operating system	Mac OS X 10.9.5
Software rendering list version	11.17
Driver bug list version	9.15
ANGLE commit id	4d208abb1926
2D graphics backend	Skia/55 d1740f81c843c65acd58d1b571ce94b90fee99d0
Command Line Args	Chrome.app/Contents/MacOS/Google Chrome --flag-switches-begin --disable-new-profile-management --top-chrome-md=material --flag-switches-end
Driver Information
Initialization time	79
In-process GPU	false
Sandboxed	true
GPU0	VENDOR = 0x10de, DEVICE= 0x0407 *ACTIVE*
Optimus	false
AMD switchable	false
Driver vendor	
Driver version	8.24.17 310.90.9.05f01
Driver date	
Pixel shader version	3.30
Vertex shader version	3.30
Max. MSAA samples	8
Machine model name	MacBookPro
Machine model version	4.1
GL_VENDOR	NVIDIA Corporation
GL_RENDERER	NVIDIA GeForce 8600M GT OpenGL Engine
GL_VERSION	3.3 NVIDIA-8.24.17 310.90.9.05f01
GL_EXTENSIONS	GL_ARB_blend_func_extended GL_ARB_ES2_compatibility GL_ARB_explicit_attrib_location GL_ARB_instanced_arrays GL_ARB_internalformat_query GL_ARB_occlusion_query2 GL_ARB_sampler_objects GL_ARB_separate_shader_objects GL_ARB_shader_bit_encoding GL_ARB_shading_language_include GL_ARB_texture_rgb10_a2ui GL_ARB_texture_storage GL_ARB_texture_swizzle GL_ARB_timer_query GL_ARB_vertex_type_2_10_10_10_rev GL_ARB_viewport_array GL_EXT_debug_label GL_EXT_debug_marker GL_EXT_depth_bounds_test GL_EXT_framebuffer_multisample_blit_scaled GL_EXT_texture_compression_s3tc GL_EXT_texture_filter_anisotropic GL_EXT_texture_mirror_clamp GL_EXT_texture_sRGB_decode GL_APPLE_client_storage GL_APPLE_container_object_shareable GL_APPLE_flush_render GL_APPLE_object_purgeable GL_APPLE_rgb_422 GL_APPLE_row_bytes GL_APPLE_texture_range GL_ATI_texture_mirror_once GL_NV_texture_barrier
Disabled Extensions	
Window system binding vendor	
Window system binding version	
Window system binding extensions	
Direct rendering	Yes
Reset notification strategy	0x0000
GPU process crash count	0
Compositor Information
Tile Update Mode	Zero-copy
Partial Raster	Enabled
GpuMemoryBuffers Status
ATC	Software only
ATCIA	Software only
DXT1	Software only
DXT5	Software only
ETC1	Software only
R_8	GPU_READ_CPU_READ_WRITE, GPU_READ_CPU_READ_WRITE_PERSISTENT
RG_88	Software only
BGR_565	Software only
RGBA_4444	Software only
RGBX_8888	Software only
RGBA_8888	GPU_READ, SCANOUT
BGRX_8888	GPU_READ, SCANOUT
BGRA_8888	GPU_READ, SCANOUT, GPU_READ_CPU_READ_WRITE, GPU_READ_CPU_READ_WRITE_PERSISTENT
YVU_420	Software only
YUV_420_BIPLANAR	GPU_READ_CPU_READ_WRITE, GPU_READ_CPU_READ_WRITE_PERSISTENT
UYVY_422	GPU_READ_CPU_READ_WRITE, GPU_READ_CPU_READ_WRITE_PERSISTENT
Log Messages
[330:1287:0109/122430:ERROR:gpu_video_decode_accelerator.cc(365)] : HW video decode not available for profile 0
[330:1287:0109/122508:ERROR:gpu_video_decode_accelerator.cc(365)] : HW video decode not available for profile 0
[330:1287:0109/123949:ERROR:gpu_video_decode_accelerator.cc(365)] : HW video decode not available for profile 0
[330:1287:0109/143821:ERROR:gles2_cmd_decoder.cc(16349)] : [.DisplayCompositor-0x7f9e434ee000]GL ERROR :GL_INVALID_OPERATION : glCreateAndConsumeTextureCHROMIUM: invalid mailbox name
[330:1287:0109/143821:ERROR:gles2_cmd_decoder.cc(9063)] : [.DisplayCompositor-0x7f9e434ee000]RENDER WARNING: texture bound to texture unit 0 is not renderable. It maybe non-power-of-2 and have incompatible texture filtering.
[330:1287:0109/143821:ERROR:gles2_cmd_decoder.cc(16349)] : [.DisplayCompositor-0x7f9e434ee000]GL ERROR :GL_INVALID_OPERATION : glCreateAndConsumeTextureCHROMIUM: invalid mailbox name
[330:1287:0109/143821:ERROR:gles2_cmd_decoder.cc(11318)] : [.DisplayCompositor-0x7f9e434ee000]GL ERROR :GL_INVALID_VALUE : glScheduleCALayerCHROMIUM: unsupported texture format
[330:1287:0109/143821:ERROR:gles2_cmd_decoder.cc(16349)] : [.DisplayCompositor-0x7f9e434ee000]GL ERROR :GL_INVALID_OPERATION : glCreateAndConsumeTextureCHROMIUM: invalid mailbox name
[330:1287:0109/143821:ERROR:gles2_cmd_decoder.cc(11318)] : [.DisplayCompositor-0x7f9e434ee000]GL ERROR :GL_INVALID_VALUE : glScheduleCALayerCHROMIUM: unsupported texture format
[330:1287:0109/143821:ERROR:gles2_cmd_decoder.cc(16349)] : [.DisplayCompositor-0x7f9e434ee000]GL ERROR :GL_INVALID_OPERATION : glCreateAndConsumeTextureCHROMIUM: invalid mailbox name
[330:1287:0109/143821:ERROR:gles2_cmd_decoder.cc(9063)] : [.DisplayCompositor-0x7f9e434ee000]RENDER WARNING: texture bound to texture unit 1 is not renderable. It maybe non-power-of-2 and have incompatible texture filtering.
[330:1287:0109/150310:ERROR:gles2_cmd_decoder.cc(16349)] : [.DisplayCompositor-0x7f9e434ee000]GL ERROR :GL_INVALID_OPERATION : glCreateAndConsumeTextureCHROMIUM: invalid mailbox name
[330:1287:0109/150310:ERROR:gles2_cmd_decoder.cc(9063)] : [.DisplayCompositor-0x7f9e434ee000]RENDER WARNING: texture bound to texture unit 0 is not renderable. It maybe non-power-of-2 and have incompatible texture filtering.
[330:1287:0109/150310:ERROR:gles2_cmd_decoder.cc(16349)] : [.DisplayCompositor-0x7f9e434ee000]GL ERROR :GL_INVALID_OPERATION : glCreateAndConsumeTextureCHROMIUM: invalid mailbox name
[330:1287:0109/150310:ERROR:gles2_cmd_decoder.cc(11318)] : [.DisplayCompositor-0x7f9e434ee000]GL ERROR :GL_INVALID_VALUE : glScheduleCALayerCHROMIUM: unsupported texture format
[330:1287:0109/150310:ERROR:gles2_cmd_decoder.cc(16349)] : [.DisplayCompositor-0x7f9e434ee000]GL ERROR :GL_INVALID_OPERATION : glCreateAndConsumeTextureCHROMIUM: invalid mailbox name
[330:1287:0109/150310:ERROR:gles2_cmd_decoder.cc(11318)] : [.DisplayCompositor-0x7f9e434ee000]GL ERROR :GL_INVALID_VALUE : glScheduleCALayerCHROMIUM: unsupported texture format
[330:1287:0109/150310:ERROR:gles2_cmd_decoder.cc(16349)] : [.DisplayCompositor-0x7f9e434ee000]GL ERROR :GL_INVALID_OPERATION : glCreateAndConsumeTextureCHROMIUM: invalid mailbox name
[330:1287:0109/150310:ERROR:gles2_cmd_decoder.cc(11318)] : [.DisplayCompositor-0x7f9e434ee000]GL ERROR :GL_INVALID_VALUE : glScheduleCALayerCHROMIUM: unsupported texture format
[330:1287:0109/150310:ERROR:gles2_cmd_decoder.cc(16349)] : [.DisplayCompositor-0x7f9e434ee000]GL ERROR :GL_INVALID_OPERATION : glCreateAndConsumeTextureCHROMIUM: invalid mailbox name
[330:1287:0109/150310:ERROR:gles2_cmd_decoder.cc(11318)] : [.DisplayCompositor-0x7f9e434ee000]GL ERROR :GL_INVALID_VALUE : glScheduleCALayerCHROMIUM: unsupported texture format
[330:1287:0109/150310:ERROR:gles2_cmd_decoder.cc(16349)] : [.DisplayCompositor-0x7f9e434ee000]GL ERROR :GL_INVALID_OPERATION : glCreateAndConsumeTextureCHROMIUM: invalid mailbox name
[330:1287:0109/150310:ERROR:gles2_cmd_decoder.cc(11318)] : [.DisplayCompositor-0x7f9e434ee000]GL ERROR :GL_INVALID_VALUE : glScheduleCALayerCHROMIUM: unsupported texture format
[330:1287:0109/150310:ERROR:gles2_cmd_decoder.cc(16349)] : [.DisplayCompositor-0x7f9e434ee000]GL ERROR :GL_INVALID_OPERATION : glCreateAndConsumeTextureCHROMIUM: invalid mailbox name
[330:1287:0109/150310:ERROR:gles2_cmd_decoder.cc(11318)] : [.DisplayCompositor-0x7f9e434ee000]GL ERROR :GL_INVALID_VALUE : glScheduleCALayerCHROMIUM: unsupported texture format
[330:1287:0109/150310:ERROR:gles2_cmd_decoder.cc(16349)] : [.DisplayCompositor-0x7f9e434ee000]GL ERROR :GL_INVALID_OPERATION : glCreateAndConsumeTextureCHROMIUM: invalid mailbox name
[330:1287:0109/150310:ERROR:gles2_cmd_decoder.cc(11318)] : [.DisplayCompositor-0x7f9e434ee000]GL ERROR :GL_INVALID_VALUE : glScheduleCALayerCHROMIUM: unsupported texture format
[330:1287:0109/150310:ERROR:gles2_cmd_decoder.cc(16349)] : [.DisplayCompositor-0x7f9e434ee000]GL ERROR :GL_INVALID_OPERATION : glCreateAndConsumeTextureCHROMIUM: invalid mailbox name
[330:1287:0109/150310:ERROR:gles2_cmd_decoder.cc(11318)] : [.DisplayCompositor-0x7f9e434ee000]GL ERROR :GL_INVALID_VALUE : glScheduleCALayerCHROMIUM: unsupported texture format
[330:1287:0109/150310:ERROR:gles2_cmd_decoder.cc(16349)] : [.DisplayCompositor-0x7f9e434ee000]GL ERROR :GL_INVALID_OPERATION : glCreateAndConsumeTextureCHROMIUM: invalid mailbox name
[330:1287:0109/150310:ERROR:gles2_cmd_decoder.cc(11318)] : [.DisplayCompositor-0x7f9e434ee000]GL ERROR :GL_INVALID_VALUE : glScheduleCALayerCHROMIUM: unsupported texture format
[330:1287:0109/150310:ERROR:gles2_cmd_decoder.cc(16349)] : [.DisplayCompositor-0x7f9e434ee000]GL ERROR :GL_INVALID_OPERATION : glCreateAndConsumeTextureCHROMIUM: invalid mailbox name
[330:1287:0109/150310:ERROR:gles2_cmd_decoder.cc(11318)] : [.DisplayCompositor-0x7f9e434ee000]GL ERROR :GL_INVALID_VALUE : glScheduleCALayerCHROMIUM: unsupported texture format
[330:1287:0109/150310:ERROR:gles2_cmd_decoder.cc(16349)] : [.DisplayCompositor-0x7f9e434ee000]GL ERROR :GL_INVALID_OPERATION : glCreateAndConsumeTextureCHROMIUM: invalid mailbox name
[330:1287:0109/150310:ERROR:gles2_cmd_decoder.cc(11318)] : [.DisplayCompositor-0x7f9e434ee000]GL ERROR :GL_INVALID_VALUE : glScheduleCALayerCHROMIUM: unsupported texture format
[330:1287:0109/150310:ERROR:gles2_cmd_decoder.cc(16349)] : [.DisplayCompositor-0x7f9e434ee000]GL ERROR :GL_INVALID_OPERATION : glCreateAndConsumeTextureCHROMIUM: invalid mailbox name
[330:1287:0109/150310:ERROR:gles2_cmd_decoder.cc(11318)] : [.DisplayCompositor-0x7f9e434ee000]GL ERROR :GL_INVALID_VALUE : glScheduleCALayerCHROMIUM: unsupported texture format
[330:1287:0109/150310:ERROR:gles2_cmd_decoder.cc(16349)] : [.DisplayCompositor-0x7f9e434ee000]GL ERROR :GL_INVALID_OPERATION : glCreateAndConsumeTextureCHROMIUM: invalid mailbox name
[330:1287:0109/150310:ERROR:gles2_cmd_decoder.cc(11318)] : [.DisplayCompositor-0x7f9e434ee000]GL ERROR :GL_INVALID_VALUE : glScheduleCALayerCHROMIUM: unsupported texture format
[330:1287:0109/150310:ERROR:gles2_cmd_decoder.cc(16349)] : [.DisplayCompositor-0x7f9e434ee000]GL ERROR :GL_INVALID_OPERATION : glCreateAndConsumeTextureCHROMIUM: invalid mailbox name
[330:1287:0109/150310:ERROR:gles2_cmd_decoder.cc(11318)] : [.DisplayCompositor-0x7f9e434ee000]GL ERROR :GL_INVALID_VALUE : glScheduleCALayerCHROMIUM: unsupported texture format
[330:1287:0109/150310:ERROR:gles2_cmd_decoder.cc(16349)] : [.DisplayCompositor-0x7f9e434ee000]GL ERROR :GL_INVALID_OPERATION : glCreateAndConsumeTextureCHROMIUM: invalid mailbox name
[330:1287:0109/150310:ERROR:gles2_cmd_decoder.cc(11318)] : [.DisplayCompositor-0x7f9e434ee000]GL ERROR :GL_INVALID_VALUE : glScheduleCALayerCHROMIUM: unsupported texture format
[330:1287:0109/150310:ERROR:gles2_cmd_decoder.cc(16349)] : [.DisplayCompositor-0x7f9e434ee000]GL ERROR :GL_INVALID_OPERATION : glCreateAndConsumeTextureCHROMIUM: invalid mailbox name
[330:1287:0109/150310:ERROR:gles2_cmd_decoder.cc(11318)] : [.DisplayCompositor-0x7f9e434ee000]GL ERROR :GL_INVALID_VALUE : glScheduleCALayerCHROMIUM: unsupported texture format
[330:1287:0109/150310:ERROR:gles2_cmd_decoder.cc(16349)] : [.DisplayCompositor-0x7f9e434ee000]GL ERROR :GL_INVALID_OPERATION : glCreateAndConsumeTextureCHROMIUM: invalid mailbox name
[330:1287:0109/150310:ERROR:gles2_cmd_decoder.cc(9063)] : [.DisplayCompositor-0x7f9e434ee000]RENDER WARNING: texture bound to texture unit 1 is not renderable. It maybe non-power-of-2 and have incompatible texture filtering.
[330:1287:0109/213234:ERROR:gpu_video_decode_accelerator.cc(365)] : HW video decode not available for profile 0
[330:1287:0109/213250:ERROR:gpu_video_decode_accelerator.cc(365)] : HW video decode not available for profile 0
[330:1287:0110/093043:ERROR:gpu_video_decode_accelerator.cc(365)] : HW video decode not available for profile 0
[330:1287:0110/094043:ERROR:gpu_video_decode_accelerator.cc(365)] : HW video decode not available for profile 1
[330:1287:0110/100135:ERROR:gpu_video_decode_accelerator.cc(365)] : HW video decode not available for profile 0
[330:1287:0110/150954:ERROR:gles2_cmd_decoder.cc(16349)] : [.DisplayCompositor-0x7f9e4762b000]GL ERROR :GL_INVALID_OPERATION : glCreateAndConsumeTextureCHROMIUM: invalid mailbox name
[330:1287:0110/150954:ERROR:gles2_cmd_decoder.cc(11318)] : [.DisplayCompositor-0x7f9e4762b000]GL ERROR :GL_INVALID_VALUE : glScheduleCALayerCHROMIUM: unsupported texture format
[330:1287:0110/151210:ERROR:latency_info.cc(159)] : GpuCommandBufferStub::OnAsyncFlush, LatencyInfo vector size 927 is too big.
[330:1287:0110/172215:ERROR:gles2_cmd_decoder.cc(16349)] : [.DisplayCompositor-0x7f9e481eec00]GL ERROR :GL_INVALID_OPERATION : glCreateAndConsumeTextureCHROMIUM: invalid mailbox name
[330:1287:0110/172215:ERROR:gles2_cmd_decoder.cc(11318)] : [.DisplayCompositor-0x7f9e481eec00]GL ERROR :GL_INVALID_VALUE : glScheduleCALayerCHROMIUM: unsupported texture format
[330:1287:0110/172215:ERROR:gles2_cmd_decoder.cc(16349)] : [.DisplayCompositor-0x7f9e481eec00]GL ERROR :GL_INVALID_OPERATION : glCreateAndConsumeTextureCHROMIUM: invalid mailbox name
[330:1287:0110/172215:ERROR:gles2_cmd_decoder.cc(11318)] : [.DisplayCompositor-0x7f9e481eec00]GL ERROR :GL_INVALID_VALUE : glScheduleCALayerCHROMIUM: unsupported texture format
[330:1287:0110/172836:ERROR:latency_info.cc(159)] : GpuCommandBufferStub::OnAsyncFlush, LatencyInfo vector size 297 is too big.

### kb...@chromium.org (2017-01-11)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-01-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/4ef48a4037ea44d220fbe9f468d3ac659a38f9cb

commit 4ef48a4037ea44d220fbe9f468d3ac659a38f9cb
Author: kbr <kbr@chromium.org>
Date: Wed Jan 11 20:46:13 2017

Disable all GPU features on GeForce 8600M on macOS.

Rendering corruption is seen on this GPU, which is nearly 10 years
old. Fall back to software rendering.

BUG=676975
CQ_INCLUDE_TRYBOTS=master.tryserver.chromium.linux:linux_optional_gpu_tests_rel;master.tryserver.chromium.mac:mac_optional_gpu_tests_rel;master.tryserver.chromium.win:win_optional_gpu_tests_rel

Review-Url: https://codereview.chromium.org/2626973002
Cr-Commit-Position: refs/heads/master@{#442990}

[modify] https://crrev.com/4ef48a4037ea44d220fbe9f468d3ac659a38f9cb/gpu/config/software_rendering_list_json.cc


### kb...@chromium.org (2017-01-11)

Fixed. Not sure whether this warrants a backport. The affected machines are ancient and I doubt there are many out there.


### sh...@chromium.org (2017-01-12)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-13)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-23)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-23)

Congratulations, the panel decided to award $500 for this bug.  A member of our finance team will be in touch.

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an established charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@chromium.org (2017-01-23)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-24)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-02-03)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-02-03)

Your change meets the bar and is auto-approved for M57. Please go ahead and merge the CL to branch 2987 manually. Please contact milestone owner if you have questions.
Owners: amineer@(clank), cmasso@(bling), ketakid@(cros), govind@(desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2017-02-03)

Please merge your change to M57 branch 2987 before 5:00 PM Pt, Monday (02/06/) so we can pick it up for next week Beta release. Thank you.

### sh...@chromium.org (2017-02-06)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2017-02-06)

Please merge your change to M57 branch 2987 before 5:00 PM PT, Tuesday (02/07/17) so we can pick it up for next Beta release. Thank you.

### kb...@chromium.org (2017-02-08)

Note: per a recent update to http://crbug.com/397484 , vendor ID 0x10de and device ID 0x0640 should be subject to the same workaround.


### go...@chromium.org (2017-02-09)

Please merge your change to M57 branch 2987 before 5:00 PM PT, Friday 02/10 (sooner the better please) so we can take it in for next week beta release. Thank you.

### go...@chromium.org (2017-02-09)

[Empty comment from Monorail migration]

### go...@chromium.org (2017-02-09)

Cl listed #13 by kbr@ is landed on Jan 11th and M57 branched on Jan 19th. So I don't think M57 merge is needed. kbr@, could you please confirm? 

### go...@chromium.org (2017-02-09)

M57 was branched at 444943.

### aw...@chromium.org (2017-02-14)

Yep, #13 made it in to 57.

### kb...@chromium.org (2017-02-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-04-20)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/676975?no_tracker_redirect=1

[Multiple monorail components: Blink>Media>Video, Internals>GPU>Internals]
[Monorail blocking: crbug.com/chromium/676829, crbug.com/chromium/692189]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40086337)*
