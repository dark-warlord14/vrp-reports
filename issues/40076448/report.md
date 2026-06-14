# UNKNOWN in _wordcopy_fwd_aligned

| Field | Value |
|-------|-------|
| **Issue ID** | [40076448](https://issues.chromium.org/issues/40076448) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals, Internals>Skia |
| **Reporter** | at...@gmail.com |
| **Assignee** | re...@google.com |
| **Created** | 2012-10-16 |
| **Bounty** | $1,000.00 |

## Description

Repro-file as attachment.

Tested on:

OS: Ubuntu 12.04 x86_64
Chromium: ASAN 24.0.1299.0 (Developer Build 162260)

Repro-file had no effect on Google Chrome: 22.0.1229.94 (Official Build 161065)

ASAN-report:

==31613== ERROR: AddressSanitizer crashed on unknown address 0x7fc645287080 (pc 0x7fc84b2e0ee4 sp 0x7fff880c1948 bp 0x7fff880c21a0 T0)
AddressSanitizer can not provide additional info.
    #0 0x7fc84b2e0ee3 in ?? /build/buildd/eglibc-2.15/string/../sysdeps/x86_64/multiarch/memcpy-ssse3-back.S:1474
    #1 0x7fc857ca7e49 in Clamp_S32_D32_nofilter_trans_shaderproc(SkBitmapProcState const&, int, int, unsigned int*, int) ../../third_party/skia/src/core/SkBitmapProcState.cpp:0
    #2 0x7fc857c9752c in SkBitmapProcShader::shadeSpan(int, int, unsigned int*, int) ???:0
    #3 0x7fc857ccb132 in SkFilterShader::shadeSpan(int, int, unsigned int*, int) ???:0
    #4 0x7fc857cc23f1 in SkARGB32_Shader_Blitter::blitMask(SkMask const&, SkIRect const&) ???:0
    #5 0x7fc857b6056c in SkMaskFilter::filterPath(SkPath const&, SkMatrix const&, SkRasterClip const&, SkBounder*, SkBlitter*, SkPaint::Style) ???:0
    #6 0x7fc857b45559 in SkDraw::drawPath(SkPath const&, SkPaint const&, SkMatrix const*, bool) const ???:0
    #7 0x7fc857b2d1b8 in SkCanvas::drawPath(SkPath const&, SkPaint const&) ???:0
    #8 0x7fc858065801 in WebCore::GraphicsContext::strokePath(WebCore::Path const&) ???:0
    #9 0x7fc859f3ea0b in WebCore::CanvasRenderingContext2D::stroke() ???:0
    #10 0x7fc8570efbbd in WebCore::CanvasRenderingContext2DV8Internal::strokeCallback(v8::Arguments const&) gen/webkit/bindings/V8DerivedSources17.cpp:0
.
.
.


## Attachments

- [chrome-crashed-wordcopyfwdaligned-de49.html](attachments/chrome-crashed-wordcopyfwdaligned-de49.html) (text/html; charset=us-ascii, 703 B)

## Timeline

### in...@chromium.org (2012-10-17)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=127576594

Uploader: inferno@chromium.org

Crash Type: UNKNOWN
Crash Address: 0x7fb04cae4880
Crash State:
  - crash stack -
  _wordcopy_fwd_aligned
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=161867:161923

Minimized Testcase (0.64 Kb): https://cluster-fuzz.appspot.com/download/AMIfv977zkOBQD2Gl1Xbx_9AbtmM2r5hHpgjiaRzbCTfkjzmfws8fbWUC6GYUmJDldMB_JmW3qMrypy7euZNt_QKT4dJ3iljDVdfRHQ5d5-39JU_KLVdpiTUnvp16M2mHNEQVrGdUx2Y10b2lTVwBsBbmbIXBgmzaWsZXrctR2P-XQuCkGM1voM

### in...@chromium.org (2012-10-17)

Looks to have regressed in Skia roll Skia: r5907:r5950

### in...@chromium.org (2012-10-18)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-10-22)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-10-22)

[Empty comment from Monorail migration]

### js...@chromium.org (2012-11-09)

[Empty comment from Monorail migration]

### [Deleted User] (2012-11-16)

Confirmed locally (on my Ubiquity instance)...

I downloaded the following binaries from https://commondatastorage.googleapis.com/chromium-browser-asan/index.html :
asan-linux-release-161867.zip (last one BEFORE clusterfuzz reported crash)
asan-linux-release-161923.zip (first one AFTER clusterfuzz reported crash)
asan-linux-release-168203.zip (newest one available)

And ran each one against the minimized test case from clusterfuzz.


# asan-linux-release-161867 succeeds
$ ./asan-linux-release-161867/chrome http://www.corp.google.com/~epoger/bugs/crbug156231-cf127576594/minimized.html
[31594:31594:1116/123552:ERROR:object_proxy.cc(495)] Failed to call method: org.chromium.Mtpd.EnumerateStorage: object_path= /org/chromium/Mtpd: org.freedesktop.DBus.Error.ServiceUnknown: The name org.chromium.Mtpd was not provided by any .service files
[31643:31643:1116/123552:ERROR:gl_surface_glx.cc(62)] GLX 1.3 or later is required.
[31643:31643:1116/123552:ERROR:gl_surface_linux.cc(58)] GLSurfaceGLX::InitializeOneOff failed.


# asan-linux-release-161923 fails
$ ./asan-linux-release-161923/chrome http://www.corp.google.com/~epoger/bugs/crbug156231-cf127576594/minimized.html
[24515:24515:1116/122934:ERROR:object_proxy.cc(495)] Failed to call method: org.chromium.Mtpd.EnumerateStorage: object_path= /org/chromium/Mtpd: org.freedesktop.DBus.Error.ServiceUnknown: The name org.chromium.Mtpd was not provided by any .service files
[24806:24806:1116/122934:ERROR:gl_surface_glx.cc(62)] GLX 1.3 or later is required.
[24806:24806:1116/122934:ERROR:gl_surface_linux.cc(58)] GLSurfaceGLX::InitializeOneOff failed.
ASAN:SIGSEGV
=================================================================
==24799== ERROR: AddressSanitizer crashed on unknown address 0x7fbb54741080 (pc 0x7fbd5a22033b sp 0x7fff157b5ac8 bp 0x7fff157b6320 T0)
AddressSanitizer can not provide additional info.
    #0 0x7fbd5a22033a (/lib/libc-2.11.1.so+0x8833a)
    #1 0x7fbd632d53a9 (/home/epoger/chrome-old-binaries/asan/asan-linux-release-161923/chrome+0x32623a9)
    #2 0x7fbd632c487c (/home/epoger/chrome-old-binaries/asan/asan-linux-release-161923/chrome+0x325187c)
    #3 0x7fbd632f9542 (/home/epoger/chrome-old-binaries/asan/asan-linux-release-161923/chrome+0x3286542)
    #4 0x7fbd632f0801 (/home/epoger/chrome-old-binaries/asan/asan-linux-release-161923/chrome+0x327d801)
    #5 0x7fbd63185eac (/home/epoger/chrome-old-binaries/asan/asan-linux-release-161923/chrome+0x3112eac)
    #6 0x7fbd6316aee9 (/home/epoger/chrome-old-binaries/asan/asan-linux-release-161923/chrome+0x30f7ee9)
    #7 0x7fbd63152b48 (/home/epoger/chrome-old-binaries/asan/asan-linux-release-161923/chrome+0x30dfb48)
    #8 0x7fbd64bba2a1 (/home/epoger/chrome-old-binaries/asan/asan-linux-release-161923/chrome+0x4b472a1)
    #9 0x7fbd648354eb (/home/epoger/chrome-old-binaries/asan/asan-linux-release-161923/chrome+0x47c24eb)
    #10 0x7fbd6681787d (/home/epoger/chrome-old-binaries/asan/asan-linux-release-161923/chrome+0x67a487d)
    #11 0x7fbd2e043096 (+0x3d096)
    #12 0x7fbd2e04240e (+0x3c40e)
    #13 0x7fbd2e024646 (+0x1e646)
    #14 0x7fbd2e0118b6 (+0xb8b6)
    #15 0x7fbd63e3319e (/home/epoger/chrome-old-binaries/asan/asan-linux-release-161923/chrome+0x3dc019e)
    #16 0x7fbd63d5ca6c (/home/epoger/chrome-old-binaries/asan/asan-linux-release-161923/chrome+0x3ce9a6c)
    #17 0x7fbd64e12255 (/home/epoger/chrome-old-binaries/asan/asan-linux-release-161923/chrome+0x4d9f255)
    #18 0x7fbd64e112fa (/home/epoger/chrome-old-binaries/asan/asan-linux-release-161923/chrome+0x4d9e2fa)
    #19 0x7fbd658350b1 (/home/epoger/chrome-old-binaries/asan/asan-linux-release-161923/chrome+0x57c20b1)
    #20 0x7fbd655ab9bf (/home/epoger/chrome-old-binaries/asan/asan-linux-release-161923/chrome+0x55389bf)
    #21 0x7fbd64ac11b9 (/home/epoger/chrome-old-binaries/asan/asan-linux-release-161923/chrome+0x4a4e1b9)
    #22 0x7fbd62164612 (/home/epoger/chrome-old-binaries/asan/asan-linux-release-161923/chrome+0x20f1612)
    #23 0x7fbd620cedec (/home/epoger/chrome-old-binaries/asan/asan-linux-release-161923/chrome+0x205bdec)
    #24 0x7fbd620cf3df (/home/epoger/chrome-old-binaries/asan/asan-linux-release-161923/chrome+0x205c3df)
    #25 0x7fbd620d018b (/home/epoger/chrome-old-binaries/asan/asan-linux-release-161923/chrome+0x205d18b)
    #26 0x7fbd620daa16 (/home/epoger/chrome-old-binaries/asan/asan-linux-release-161923/chrome+0x2067a16)
    #27 0x7fbd620cdb8c (/home/epoger/chrome-old-binaries/asan/asan-linux-release-161923/chrome+0x205ab8c)
    #28 0x7fbd62113bb1 (/home/epoger/chrome-old-binaries/asan/asan-linux-release-161923/chrome+0x20a0bb1)
    #29 0x7fbd620cbfc6 (/home/epoger/chrome-old-binaries/asan/asan-linux-release-161923/chrome+0x2058fc6)
    #30 0x7fbd689d5e63 (/home/epoger/chrome-old-binaries/asan/asan-linux-release-161923/chrome+0x8962e63)
    #31 0x7fbd61f6b10a (/home/epoger/chrome-old-binaries/asan/asan-linux-release-161923/chrome+0x1ef810a)
    #32 0x7fbd61f6c569 (/home/epoger/chrome-old-binaries/asan/asan-linux-release-161923/chrome+0x1ef9569)
    #33 0x7fbd61f6dc31 (/home/epoger/chrome-old-binaries/asan/asan-linux-release-161923/chrome+0x1efac31)
    #34 0x7fbd61f6a837 (/home/epoger/chrome-old-binaries/asan/asan-linux-release-161923/chrome+0x1ef7837)
    #35 0x7fbd60f8ea86 (/home/epoger/chrome-old-binaries/asan/asan-linux-release-161923/chrome+0xf1ba86)
    #36 0x7fbd60f8e9ea (/home/epoger/chrome-old-binaries/asan/asan-linux-release-161923/chrome+0xf1b9ea)
    #37 0x7fbd5a1b6c4c (/lib/libc-2.11.1.so+0x1ec4c)
Stats: 8M malloced (10M for red zones) by 23479 calls
Stats: 0M realloced by 51 calls
Stats: 6M freed by 13753 calls
Stats: 0M really freed by 0 calls
Stats: 56M (14345 full pages) mmaped in 14 calls
  mmaps   by size class: 8:32766; 9:8191; 10:4095; 11:2047; 12:1024; 13:512; 14:256; 15:128; 16:128; 17:32; 18:16; 19:8; 
  mallocs by size class: 8:19394; 9:1767; 10:1783; 11:163; 12:69; 13:66; 14:114; 15:30; 16:81; 17:7; 18:3; 19:2; 
  frees   by size class: 8:10520; 9:1188; 10:1681; 11:69; 12:34; 13:52; 14:101; 15:24; 16:75; 17:5; 18:2; 19:2; 
  rfrees  by size class: 
Stats: malloc large: 12 small slow: 144
==24799== ABORTING


# asan-linux-release-168203 fails
$ ./asan-linux-release-168203/chrome http://www.corp.google.com/~epoger/bugs/crbug156231-cf127576594/minimized.html
[30144:30157:1116/123441:ERROR:object_proxy.cc(624)] Failed to get name owner. Got org.freedesktop.DBus.Error.NameHasNoOwner: Could not get owner of name 'org.chromium.Mtpd': no such name
[30144:30157:1116/123441:ERROR:object_proxy.cc(624)] Failed to get name owner. Got org.freedesktop.DBus.Error.NameHasNoOwner: Could not get owner of name 'org.chromium.Mtpd': no such name
[30144:30144:1116/123441:ERROR:object_proxy.cc(529)] Failed to call method: org.chromium.Mtpd.EnumerateStorage: object_path= /org/chromium/Mtpd: org.freedesktop.DBus.Error.ServiceUnknown: The name org.chromium.Mtpd was not provided by any .service files
[30176:30176:1116/123441:ERROR:gl_surface_glx.cc(383)] GLX 1.3 or later is required.
[30176:30176:1116/123441:ERROR:gl_surface_linux.cc(58)] GLSurfaceGLX::InitializeOneOff failed.
ASAN:SIGSEGV
=================================================================
==30169== ERROR: AddressSanitizer: SEGV on unknown address 0x7fc1f28ad840 (pc 0x7fc3f776533b sp 0x7fffc93b2678 bp 0x7fffc93b2ed0 T0)
AddressSanitizer can not provide additional info.
    #0 0x7fc3f776533a (/lib/libc-2.11.1.so+0x8833a)
    #1 0x7fc40074a579 (/home/epoger/chrome-old-binaries/asan/asan-linux-release-168203/chrome+0x2f8f579)
    #2 0x7fc400739e33 (/home/epoger/chrome-old-binaries/asan/asan-linux-release-168203/chrome+0x2f7ee33)
    #3 0x7fc40076d8e2 (/home/epoger/chrome-old-binaries/asan/asan-linux-release-168203/chrome+0x2fb28e2)
    #4 0x7fc400764c4e (/home/epoger/chrome-old-binaries/asan/asan-linux-release-168203/chrome+0x2fa9c4e)
    #5 0x7fc40068283d (/home/epoger/chrome-old-binaries/asan/asan-linux-release-168203/chrome+0x2ec783d)
    #6 0x7fc400665333 (/home/epoger/chrome-old-binaries/asan/asan-linux-release-168203/chrome+0x2eaa333)
    #7 0x7fc40064bf4b (/home/epoger/chrome-old-binaries/asan/asan-linux-release-168203/chrome+0x2e90f4b)
    #8 0x7fc402087551 (/home/epoger/chrome-old-binaries/asan/asan-linux-release-168203/chrome+0x48cc551)
    #9 0x7fc401cea721 (/home/epoger/chrome-old-binaries/asan/asan-linux-release-168203/chrome+0x452f721)
    #10 0x7fc403c826b4 (/home/epoger/chrome-old-binaries/asan/asan-linux-release-168203/chrome+0x64c76b4)
    #11 0x278b79544096 (+0x3e096)
    #12 0x278b7954340e (+0x3d40e)
    #13 0x278b79524f86 (+0x1ef86)
    #14 0x278b79511b76 (+0xbb76)
    #15 0x7fc40132e84a (/home/epoger/chrome-old-binaries/asan/asan-linux-release-168203/chrome+0x3b7384a)
    #16 0x7fc401258d44 (/home/epoger/chrome-old-binaries/asan/asan-linux-release-168203/chrome+0x3a9dd44)
    #17 0x7fc4023093a8 (/home/epoger/chrome-old-binaries/asan/asan-linux-release-168203/chrome+0x4b4e3a8)
    #18 0x7fc402308510 (/home/epoger/chrome-old-binaries/asan/asan-linux-release-168203/chrome+0x4b4d510)
    #19 0x7fc402d75de6 (/home/epoger/chrome-old-binaries/asan/asan-linux-release-168203/chrome+0x55bade6)
    #20 0x7fc402aa6d57 (/home/epoger/chrome-old-binaries/asan/asan-linux-release-168203/chrome+0x52ebd57)
    #21 0x7fc401f7d999 (/home/epoger/chrome-old-binaries/asan/asan-linux-release-168203/chrome+0x47c2999)
    #22 0x7fc3ff935ad8 (/home/epoger/chrome-old-binaries/asan/asan-linux-release-168203/chrome+0x217aad8)
    #23 0x7fc3ff89fe23 (/home/epoger/chrome-old-binaries/asan/asan-linux-release-168203/chrome+0x20e4e23)
    #24 0x7fc3ff8a03bf (/home/epoger/chrome-old-binaries/asan/asan-linux-release-168203/chrome+0x20e53bf)
    #25 0x7fc3ff8a116e (/home/epoger/chrome-old-binaries/asan/asan-linux-release-168203/chrome+0x20e616e)
    #26 0x7fc3ff8ab996 (/home/epoger/chrome-old-binaries/asan/asan-linux-release-168203/chrome+0x20f0996)
    #27 0x7fc3ff89ecfa (/home/epoger/chrome-old-binaries/asan/asan-linux-release-168203/chrome+0x20e3cfa)
    #28 0x7fc3ff8e5211 (/home/epoger/chrome-old-binaries/asan/asan-linux-release-168203/chrome+0x212a211)
    #29 0x7fc3ff89d1b6 (/home/epoger/chrome-old-binaries/asan/asan-linux-release-168203/chrome+0x20e21b6)
    #30 0x7fc4061088ab (/home/epoger/chrome-old-binaries/asan/asan-linux-release-168203/chrome+0x894d8ab)
    #31 0x7fc3ff53ee3e (/home/epoger/chrome-old-binaries/asan/asan-linux-release-168203/chrome+0x1d83e3e)
    #32 0x7fc3ff54026a (/home/epoger/chrome-old-binaries/asan/asan-linux-release-168203/chrome+0x1d8526a)
    #33 0x7fc3ff54191a (/home/epoger/chrome-old-binaries/asan/asan-linux-release-168203/chrome+0x1d8691a)
    #34 0x7fc3ff53e587 (/home/epoger/chrome-old-binaries/asan/asan-linux-release-168203/chrome+0x1d83587)
    #35 0x7fc3fe6ec6ef (/home/epoger/chrome-old-binaries/asan/asan-linux-release-168203/chrome+0xf316ef)
    #36 0x7fc3fe6ec65a (/home/epoger/chrome-old-binaries/asan/asan-linux-release-168203/chrome+0xf3165a)
    #37 0x7fc3f76fbc4c (/lib/libc-2.11.1.so+0x1ec4c)
Stats: 7M malloced (7M for red zones) by 23609 calls
Stats: 0M realloced by 56 calls
Stats: 6M freed by 13814 calls
Stats: 0M really freed by 0 calls
Stats: 17M (4502 full pages) mmaped in 35 calls
  mmaps   by size class: 7:20475; 8:4094; 9:1023; 10:2044; 11:255; 12:128; 13:64; 14:128; 15:32; 16:80; 17:8; 18:2; 19:1; 
  mallocs by size class: 7:18257; 8:2658; 9:417; 10:1759; 11:156; 12:65; 13:64; 14:114; 15:30; 16:80; 17:6; 18:2; 19:1; 
  frees   by size class: 7:10018; 8:1555; 9:224; 10:1665; 11:65; 12:30; 13:51; 14:102; 15:24; 16:74; 17:4; 18:1; 19:1; 
  rfrees  by size class: 
Stats: malloc large: 119 small slow: 256
==30169== ABORTING


### [Deleted User] (2012-11-16)

I'll update my chrome source tree and make a debug build so I can run this in gdb... I will update this issue on Monday.

### [Deleted User] (2012-11-19)

When I view the test page in my local tip-of-tree build (crrev 168230, running on my Linux desktop via NX), I get this failed assertion in the Skia code:

$ out/Debug/chrome --single-process http://www.corp.google.com/~epoger/bugs/crbug156231-cf127576594/minimized.html
[9707:9742:1119/120048:FATAL:SkUtils_opts_SSE2.cpp(44)] ../../third_party/skia/src/opts/SkUtils_opts_SSE2.cpp:44: failed assertion "dst != __null && count >= 0"

	base::debug::StackTrace::StackTrace() [0x7f71a4c1945a]
	logging::LogMessage::~LogMessage() [0x7f71a4c4483b]
	SkDebugf_FileLine() [0x7f71a56fa413]
	sk_memset32_SSE2() [0x7f71a62d10e1]
	Clamp_S32_D32_nofilter_trans_shaderproc() [0x7f71a580ef75]
	SkBitmapProcShader::shadeSpan() [0x7f71a5801e17]
	SkFilterShader::shadeSpan() [0x7f71a5827969]
	SkARGB32_Shader_Blitter::blitMask() [0x7f71a5820dff]
	SkMaskFilter::filterPath() [0x7f71a572ddf6]
	SkDraw::drawPath() [0x7f71a571d1fa]
	SkDevice::drawPath() [0x7f71a5719d3d]
	SkCanvas::drawPath() [0x7f71a570ce08]
	WebCore::GraphicsContext::strokePath() [0x7f71a5affa08]
	WebCore::CanvasRenderingContext2D::stroke() [0x7f71a6b15b50]
	WebCore::CanvasRenderingContext2DV8Internal::strokeCallback() [0x7f71a51c24d6]
	<unknown> [0x18339ac44a37]

According to ClusterFuzz, the regression window was:
Chromium: r161867:r161923
Webkit: r131273:r131301
Skia: r5907:r5950

Mike, I see that you updated src/core/SkBitmapProcShader.cpp in https://code.google.com/p/skia/source/detail?r=5930 , so I am assigning this over to you.  In the meanwhile, though, I will revert that revision in my local checkout and see if that fixes the problem for me...

### re...@google.com (2012-11-19)

Possibly the bug is in rev. 5939. If your first revert doesn't fix it, try that revision.

### [Deleted User] (2012-11-19)

Yeah, reverting 5930 alone doesn't seem to fix it.  Trying 5939 now.

### [Deleted User] (2012-11-19)

I tried reverting just 5930 in both my release and debug trees, and it didn't seem to help in either one.

I tried reverting just 5939 in my debug tree, and it didn't seem to help.  (Still working on a test of that in my release tree.)

I'm going to see if I can revert all Skia changes in the regression window without too much trouble, and see what that does...

### [Deleted User] (2012-11-19)

In my release tree, I made just the following change (SIMILAR to rolling out just 5939, but simplified), and the ASAN failure went away.

Mike, what does this mean to you?


Index: third_party/skia/src/core/SkBitmapProcState.cpp
===================================================================
--- third_party/skia/src/core/SkBitmapProcState.cpp	(revision 6446)
+++ third_party/skia/src/core/SkBitmapProcState.cpp	(working copy)
@@ -432,11 +432,11 @@
     SkShader::TileMode ty = (SkShader::TileMode)fTileModeY;
 
     if (SkShader::kClamp_TileMode == tx && SkShader::kClamp_TileMode == ty) {
-        this->setupForTranslate();
+        //this->setupForTranslate();
         return Clamp_S32_D32_nofilter_trans_shaderproc;
     }
     if (SkShader::kRepeat_TileMode == tx && SkShader::kRepeat_TileMode == ty) {
-        this->setupForTranslate();
+        //this->setupForTranslate();
         return Repeat_S32_D32_nofilter_trans_shaderproc;
     }
     return NULL;


### re...@google.com (2012-11-19)

That change seems wacky, as now those fields (fFilterOneX,Y) do not have anything meaningful in them, but I believe you. The gist of 5939 was to add this function (setupForTranslate). Have you run gm locally, to see if you still get "correct" results with your change?

### [Deleted User] (2012-11-19)

No, I haven't run gm locally against this change.  It may well be that commenting out the calls to setupForTranslate() just hides the problem because the draw operation is just using radically different parameters... I dunno.

For now, I'm focusing on reverting all Skia changes in the regression window (it's tricky because of the number of subsequent changes in these same files), to see what happens.  I'll update this bug when I have more data on that.

### [Deleted User] (2012-11-19)

Unfortunately, my attempt to revert all the Skia changes in the regression window failed.  Too many conflicts from the many revisions since then... I tried to fix them manually, but it got too unwieldy.

Maybe a more fruitful approach would be to:

1. sync a Chrome tree to r162220 (just after this started happening)
2. build in debug mode
3. confirm that you can reproduce the assert failure using this test case
4. try reverting individual changes within the regression window (this will be easier when the tree is synced to 162220 instead of 168230)

Mike, can you please do that (or whatever approach you see fit)?  I think it would be better for me to triage *more* Chrome bugs (and do my other work!) rather than drilling down even more into this one.  But if you think otherwise, let me know and I can take the next step.

### re...@google.com (2012-11-20)

fixed in skia 6513

### in...@chromium.org (2012-11-20)

[Empty comment from Monorail migration]

### cl...@chromium.org (2012-11-22)

ClusterFuzz has detected this issue as fixed in range 169035:169047.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=127576594

Uploader: inferno@chromium.org

Crash Type: UNKNOWN
Crash Address: 0x7fb04cae4880
Crash State:
  - crash stack -
  _wordcopy_fwd_aligned
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=161867:161923
Fixed: https://cluster-fuzz.appspot.com/revisions?range=169035:169047

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv977zkOBQD2Gl1Xbx_9AbtmM2r5hHpgjiaRzbCTfkjzmfws8fbWUC6GYUmJDldMB_JmW3qMrypy7euZNt_QKT4dJ3iljDVdfRHQ5d5-39JU_KLVdpiTUnvp16M2mHNEQVrGdUx2Y10b2lTVwBsBbmbIXBgmzaWsZXrctR2P-XQuCkGM1voM

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### sc...@gmail.com (2012-11-30)

Mike or Elliot, do you mind merging Skia r6513 to the M24 branch? My reading of this bug is that this regression is currently on the M24 branch so we should merge the fix.

### sc...@gmail.com (2012-12-04)

[Empty comment from Monorail migration]

### ep...@google.com (2012-12-12)

Sorry for the wait, cherrypicking https://code.google.com/p/skia/source/detail?r=6513 into https://code.google.com/p/skia/source/browse/#svn%2Fbranches%2Fchrome%2Fm24_1312 now.

### [Deleted User] (2012-12-12)

Merged http://code.google.com/p/skia/source/detail?r=6513 into Skia's chrome/m24_1312 branch as http://code.google.com/p/skia/source/detail?r=6761.

### js...@chromium.org (2012-12-20)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-01-22)

@attekett: aaaand another $1000 etc.

### pa...@chromium.org (2013-02-19)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-02-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/156231?no_tracker_redirect=1

[Multiple monorail components: Internals, Internals>Skia]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40076448)*
