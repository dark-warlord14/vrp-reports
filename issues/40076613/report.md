# Access violation write in _VEC_memcpy

| Field | Value |
|-------|-------|
| **Issue ID** | [40076613](https://issues.chromium.org/issues/40076613) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals, Internals>Skia |
| **Reporter** | at...@gmail.com |
| **Assignee** | bs...@google.com |
| **Created** | 2012-11-25 |
| **Bounty** | $1,000.00 |

## Description


Tested on:

OS: Windows 7 x64
Chrome: 25.0.1334.0 (169347) canary ( didn't reproduce on current Stable Chrome )

You need to have page-heap enabled gflags.exe /p /enable chrome.exe /full and enviromental variable CHROME_ALLOCATOR set to "winheap". This issue did not reproduce without those set.

This issue reproduced easilly on two laptops. First one is with i5-3210M processor with Intel HD 4000 graphics and the second one is with AMD E450 processor and it's integrated graphics.

windbg analysis from dump-file:

FAULTING_IP: 
chrome_66ac0000!_VEC_memcpy+33
66ac8443 660f7f07        movdqa  xmmword ptr [edi],xmm0

EXCEPTION_RECORD:  ffffffff -- (.exr 0xffffffffffffffff)
ExceptionAddress: 66ac8443 (chrome_66ac0000!_VEC_memcpy+0x00000033)
   ExceptionCode: c0000005 (Access violation)
  ExceptionFlags: 00000000
NumberParameters: 2
   Parameter[0]: 00000001
   Parameter[1]: 02286110
Attempt to write to address 02286110

EXCEPTION_PARAMETER1:  00000001

EXCEPTION_PARAMETER2:  02286110

WRITE_ADDRESS:  02286110 

FOLLOWUP_IP: 
chrome_66ac0000!_VEC_memcpy+33
66ac8443 660f7f07        movdqa  xmmword ptr [edi],xmm0

MOD_LIST: <ANALYSIS/>

NTGLOBALFLAG:  2000000

FAULTING_THREAD:  00001134

BUGCHECK_STR:  APPLICATION_FAULT_INVALID_POINTER_WRITE

PRIMARY_PROBLEM_CLASS:  INVALID_POINTER_WRITE

DEFAULT_BUCKET_ID:  INVALID_POINTER_WRITE

LAST_CONTROL_TRANSFER:  from 67e5fe50 to 66ac8443

STACK_TEXT:  
0035e430 67e5fe50 00000000 00000000 00000f64 chrome_66ac0000!_VEC_memcpy+0x33
0035e454 670ebaa8 00000000 00000000 00000f64 chrome_66ac0000!GLES2ReadPixels+0x27 [c:\b\build\slave\win\build\src\gpu\command_buffer\client\gles2_c_lib_autogen.h @ 336]
0035e54c 670cd129 135aff90 00000000 00000000 chrome_66ac0000!GrGpuGL::onReadPixels+0x2ea [c:\b\build\slave\win\build\src\third_party\skia\src\gpu\gl\grgpugl.cpp @ 1490]
0035e778 670e449d 1154ffb0 00000000 00000000 chrome_66ac0000!GrContext::readRenderTargetPixels+0x449 [c:\b\build\slave\win\build\src\third_party\skia\src\gpu\grcontext.cpp @ 1356]
0035e7a8 676738aa 00000000 00000000 00000f64 chrome_66ac0000!GrTexture::readPixels+0x48 [c:\b\build\slave\win\build\src\third_party\skia\src\gpu\grtexture.cpp @ 53]
0035e7f8 67673472 135c9fcc 00000000 68daf8b0 chrome_66ac0000!SkGrPixelRef::onReadPixels+0x11f [c:\b\build\slave\win\build\src\third_party\skia\src\gpu\skgrpixelref.cpp @ 163]
0035e810 66b0882b 135c9fb8 0035e894 1124afb0 chrome_66ac0000!SkROLockPixelsPixelRef::onLockPixels+0x47 [c:\b\build\slave\win\build\src\third_party\skia\src\gpu\skgrpixelref.cpp @ 33]
0035e820 6733daae 00000000 116ccfe0 0035e848 chrome_66ac0000!SkPixelRef::lockPixels+0x2b [c:\b\build\slave\win\build\src\third_party\skia\src\core\skpixelref.cpp @ 114]
0035e830 67311a67 1124afb0 00000050 13785fc0 chrome_66ac0000!WebCore::WEBPImageEncoder::encode+0x1d [c:\b\build\slave\win\build\src\third_party\webkit\source\webcore\platform\image-encoders\skia\webpimageencoder.cpp @ 123]
0035e848 673111b7 1124afb0 0035e8d4 00000000 chrome_66ac0000!WebCore::encodeImage<SkBitmap const >+0xb9 [c:\b\build\slave\win\build\src\third_party\webkit\source\webcore\platform\graphics\skia\imagebufferskia.cpp @ 351]
0035e8ac 67282e54 0035e8ec 0035e8d4 00000000 chrome_66ac0000!WebCore::ImageBuffer::toDataURL+0x69 [c:\b\build\slave\win\build\src\third_party\webkit\source\webcore\platform\graphics\skia\imagebufferskia.cpp @ 368]
0035e8cc 678d1907 116ccfe0 00000000 00000000 chrome_66ac0000!WebCore::HTMLCanvasElement::toDataURL+0x107 [c:\b\build\slave\win\build\src\third_party\webkit\source\webcore\html\htmlcanvaselement.cpp @ 430]
0035e918 66d64c04 0035e938 0035e954 00000003 chrome_66ac0000!WebCore::V8HTMLCanvasElement::toDataURLCallback+0x136 [c:\b\build\slave\win\build\src\third_party\webkit\source\webcore\bindings\v8\custom\v8htmlcanvaselementcustom.cpp @ 137]
0035e980 66d64a1b 00000003 0035e9c0 0035e9b0 chrome_66ac0000!v8::internal::HandleApiCallHelper<0>+0x1e2 [c:\b\build\slave\win\build\src\v8\src\builtins.cc @ 1376]
0035ea3c 66cf0bd8 0f03f200 2d886765 2d828591 chrome_66ac0000!v8::internal::Builtin_HandleApiCall+0x16 [c:\b\build\slave\win\build\src\v8\src\builtins.cc @ 1394]
0035ea8c 66cf05c1 0035eb00 00000000 100fc030 chrome_66ac0000!v8::internal::Invoke+0x140 [c:\b\build\slave\win\build\src\v8\src\execution.cc @ 118]
0035eacc 66da5231 0035eb00 100fc030 100fc034 chrome_66ac0000!v8::internal::Execution::Call+0x17b [c:\b\build\slave\win\build\src\v8\src\execution.cc @ 179]
0035eb34 66da4e9f 0035eb4c 00000000 0c461828 chrome_66ac0000!v8::Script::Run+0x1ef [c:\b\build\slave\win\build\src\v8\src\api.cc @ 1704]
0035eb50 66da33db 0035eb74 100fc024 0c461c7c chrome_66ac0000!WebCore::ScriptRunner::runCompiledScript+0x87 [c:\b\build\slave\win\build\src\third_party\webkit\source\webcore\bindings\v8\scriptrunner.cpp @ 52]
.
.
.

FAILURE_BUCKET_ID:  INVALID_POINTER_WRITE_c0000005_chrome.dll!_VEC_memcpy

BUCKET_ID:  APPLICATION_FAULT_INVALID_POINTER_WRITE_chrome!_VEC_memcpy+33

## Attachments

- [_VEC_memcpy033.zip](attachments/_VEC_memcpy033.zip) (application/zip; charset=binary, 1.4 KB)

## Timeline

### at...@gmail.com (2012-11-25)

This issue has similar crash stack than https://crbug.com/chromium/161051 except that this issue has WebCore::WEBPImageEncoder::encode and the https://crbug.com/chromium/161051 has WebCore::PNGImageEncoder::encode.

### ke...@chromium.org (2012-12-04)

As an update, this isn't being ignored, but we've been having trouble reproducing these bugs.

### at...@gmail.com (2012-12-04)

I tried this on Windows machine without any previous programming/debugging tools installed. 

I installed Chrome Canary and Windows Debugging Tools x86 like said in instructions from http://www.chromium.org/developers/testing/page-heap-for-chrome

From Control Panel -> System -> Advanced system settings -> Environment Variables added new env variable CHROME_ALLOCATOR with value winheap

Then in Powershell ISE run commands (if you run powershell ISE before applying the env variable it won't work so you must restart powershell)
& 'c:\Program Files (x86)\Debugging Tools for Windows (x86)\gflags.exe' /p /enable chrome.exe /full

path/to/chrome SxS/chrome.exe --no-sandbox run.html


### at...@gmail.com (2012-12-04)

[Comment Deleted]

### at...@gmail.com (2012-12-04)

I'm not still 100% sure but this issue might depend on resolution/window size, all my own local computers are laptops with 1366x768 resolution and had chrome in full-screen mode when I tried to reproduce this.

### [Deleted User] (2012-12-05)

CCing people to get the ball rolling again on this. Can anyone reproduce this?

### [Deleted User] (2012-12-05)

[Empty comment from Monorail migration]

### [Deleted User] (2012-12-10)

Darin, any ideas for an owner to get this sorted out?

### [Deleted User] (2012-12-10)

brian, have you looked at this yet?

### [Deleted User] (2012-12-10)

[Empty comment from Monorail migration]

### bs...@google.com (2012-12-10)

I tried unsuccessfully to reproduce this using gflags.

### er...@chromium.org (2012-12-11)

Reproduces as described for me. Here is a full memory dump: http://www/~ericroman/chrome/162551.dmp

Be sure to use the 32-bit version of gflags to enable full page heap on chrome.exe.

### pa...@chromium.org (2012-12-18)

Calling it Assigned since eroman can confirm it. Friendly ping. :)

FWIW, I cannot reproduce it on Linux ToT ASAN. But perhaps that is no surprise; do we think this bug is Windows-only? (Nothing in attekett's stack looks Windows-specific to me, but perhaps build_gles2_cmd_buffer.py generates something very different on Windows than on Linux.)

This would seem to be a 128-bit write primitive in a renderer, which I'd call Pri-1, SecSeverity-High. Do other people agree? Similarly, SecImpacts-None since Canary only so far. (I hesitate to update the severity flags since I haven't observed the bug myself.)

### bs...@google.com (2012-12-18)

I don't know what I did differently this time, but I am able to reproduce it now.

### bs...@google.com (2012-12-18)

The crash initially occurs because Skia fails to allocate memory for a temporary bitmap to hold a readback of the 2D canvas. I suppose pageheap is causing us to OOM when we otherwise wouldn't. If I add a failure check there is a crash sometime later in WK. Looking into that...

### bs...@google.com (2012-12-18)

The WK SkBitmap encoders are not checking if SkBitmap has NULL pixels or not. I'll prepare a WK patch for that.

The Skia-side fix landed here: https://codereview.appspot.com/6936068/

With both fixes we still eventually crash but it is a deliberate SK_CRASH() due to SkCanvas pixel allocation failure.

### bs...@google.com (2012-12-19)

https://bugs.webkit.org/show_bug.cgi?id=105349

### bs...@google.com (2012-12-19)

Fixed in WK rev 138170. It should hit Chromium in the next WK roll.

### sc...@gmail.com (2012-12-19)

http://trac.webkit.org/changeset/138170



### sc...@gmail.com (2012-12-19)

@bsalomon: thanks for the fix!!
Now that you have a solid handle on the problem and the fix, does it match with the original report of a memcpy() into a bad pointer?

### sc...@gmail.com (2012-12-19)

[Empty comment from Monorail migration]

### bs...@google.com (2012-12-20)

Yes, the Skia issue was writing memcpy()ing into a NULL pointer.

### js...@chromium.org (2012-12-20)

[Empty comment from Monorail migration]

### js...@chromium.org (2013-01-03)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-01-11)

@attekett: is this issue fixed to your satisfaction? The fix seems to talk a lot about NULL pointers, but your original report looks like a bad read from a non-NULL pointer.

### at...@gmail.com (2013-01-11)

@scarybeasts: Looks like my fuzzer is unable to find any test cases that would reproduce this issue, so I'm happy. 

### sc...@gmail.com (2013-01-14)

M25: http://trac.webkit.org/changeset/139670

### sc...@gmail.com (2013-01-22)

@attekett: thanks! $1000

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

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-29)

[Empty comment from Monorail migration]

### is...@google.com (2018-07-29)

This issue was migrated from crbug.com/chromium/162551?no_tracker_redirect=1

[Multiple monorail components: Internals, Internals>Skia]
[Monorail blocking: crbug.com/chromium/161051]
[Monorail mergedwith: crbug.com/chromium/161051]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40076613)*
