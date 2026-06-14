# Security: INVALID_POINTER_READ/WRITE_EXPLOITABLE_chrome!SkRgnBuilder::blitH

| Field | Value |
|-------|-------|
| **Issue ID** | [40050935](https://issues.chromium.org/issues/40050935) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals, Internals>Skia |
| **Reporter** | at...@gmail.com |
| **Assignee** | re...@google.com |
| **Created** | 2011-11-07 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**

Invalid pointer read and write. During debuggin I was able to change the crash address but unable to identify why the address changed. Reproduce file caused both invalid write and read errors and cases that I couldn't track.

**VERSION**  

Chrome Version: 17.0.928.0 (Official Build 108431) dev-m  

Operating System: Windows 7 x64 SP1, Linux Debian 6.0.3 x86\_64

REPRODUCTION CASE:  

Attached html-file. You will also need one video file to reproduce. You need to add appropriate file name into html-file. Take note that there is one special-character in the html-file that may not be transferred if you use copy-paste.

Type of crash: tab-crash.  

Crash State:  

I got few different crashes with the same file.

Few INVALID\_POINTER\_READ and

APPLICATION\_FAULT\_INVALID\_POINTER\_READ\_INVALID\_POINTER\_WRITE\_PROBABLYEXPLOITABLE\_chrome!base::ConditionVariable::Event::Extract

APPLICATION\_FAULT\_INVALID\_POINTER\_READ\_INVALID\_POINTER\_WRITE\_EXPLOITABLE\_chrome!SkRgnBuilder::blitH

Analyze file for the later one is as attachment.

## Attachments

- [chrome_SkRgnBuilder.txt](attachments/chrome_SkRgnBuilder.txt) (text/plain; charset=us-ascii, 9.8 KB)
- [chrome_SkRgnBuilder.html](attachments/chrome_SkRgnBuilder.html) (text/html; charset=iso-8859-1, 824 B)
- [Check64x48bwrg16pal_25fps_noaudio.avi.026v10.ogv](attachments/Check64x48bwrg16pal_25fps_noaudio.avi.026v10.ogv) (application/ogg; charset=binary, 4.3 KB)

## Timeline

### at...@gmail.com (2011-11-07)

It seems that the sample html can be reduced even further by removing the while-loop and .À characters. After that I have been able to get only 0b dump-files but still tab-crash.

### js...@chromium.org (2011-11-07)

Haven't confirmed yet, just adding Skia label since that's where the log shows the crash.

### sc...@gmail.com (2011-11-07)

==2745== Invalid write of size 4
==2745==    at 0x105A0EF: SkRgnBuilder::blitH(int, int, int) (in /home/chris/chrome/src/out/Release/chrome)
==2745==    by 0x10603B3: walk_convex_edges(SkEdge*, SkPath::FillType, SkBlitter*, int, int, void (*)(SkBlitter*, int, bool)) (in /home/chris/chrome/src/out/Release/chrome)
==2745==    by 0x1060C0C: sk_fill_path(SkPath const&, SkIRect const*, SkBlitter*, int, int, int, SkRegion const&) (in /home/chris/chrome/src/out/Release/chrome)
==2745==    by 0x1060F6D: SkScan::FillPath(SkPath const&, SkRegion const&, SkBlitter*) (in /home/chris/chrome/src/out/Release/chrome)
==2745==    by 0x1059EF8: SkRegion::setPath(SkPath const&, SkRegion const&) (in /home/chris/chrome/src/out/Release/chrome)
==2745==    by 0x10574A7: SkRasterClip::setPath(SkPath const&, SkRasterClip const&, bool) (in /home/chris/chrome/src/out/Release/chrome)
==2745==    by 0x1038D1C: SkCanvas::clipPath(SkPath const&, SkRegion::Op, bool) (in /home/chris/chrome/src/out/Release/chrome)
==2745==    by 0x1038E24: SkCanvas::clipRect(SkRect const&, SkRegion::Op, bool) (in /home/chris/chrome/src/out/Release/chrome)
==2745==    by 0x1A5E6EF: WebCore::GraphicsContext::clip(WebCore::FloatRect const&) (in /home/chris/chrome/src/out/Release/chrome)
==2745==    by 0x1987E7E: WebCore::CanvasRenderingContext2D::drawImage(WebCore::HTMLVideoElement*, WebCore::FloatRect const&, WebCore::FloatRect const&, int&) (in /home/chris/chrome/src/out/Release/chrome)
==2745==    by 0x1988068: WebCore::CanvasRenderingContext2D::drawImage(WebCore::HTMLVideoElement*, float, float, float, float, int&) (in /home/chris/chrome/src/out/Release/chrome)
==2745==    by 0x20BD945: WebCore::CanvasRenderingContext2DInternal::drawImageCallback(v8::Arguments const&) (in /home/chris/chrome/src/out/Release/chrome)



==2745==  Address 0x18ac6dc8 is 4 bytes after a block of size 2,324 alloc'd
==2745==    at 0x4E6490F: malloc (vg_replace_malloc.c:1070)
==2745==    by 0x10865AA: sk_malloc_flags(unsigned long, unsigned int) (in /home/chris/chrome/src/out/Release/chrome)
==2745==    by 0x1059C71: SkRgnBuilder::init(int, int) (in /home/chris/chrome/src/out/Release/chrome)
==2745==    by 0x1059EE2: SkRegion::setPath(SkPath const&, SkRegion const&) (in /home/chris/chrome/src/out/Release/chrome)
==2745==    by 0x10574A7: SkRasterClip::setPath(SkPath const&, SkRasterClip const&, bool) (in /home/chris/chrome/src/out/Release/chrome)
==2745==    by 0x1038D1C: SkCanvas::clipPath(SkPath const&, SkRegion::Op, bool) (in /home/chris/chrome/src/out/Release/chrome)
==2745==    by 0x1038E24: SkCanvas::clipRect(SkRect const&, SkRegion::Op, bool) (in /home/chris/chrome/src/out/Release/chrome)
==2745==    by 0x1A5E6EF: WebCore::GraphicsContext::clip(WebCore::FloatRect const&) (in /home/chris/chrome/src/out/Release/chrome)
==2745==    by 0x1987E7E: WebCore::CanvasRenderingContext2D::drawImage(WebCore::HTMLVideoElement*, WebCore::FloatRect const&, WebCore::FloatRect const&, int&) (in /home/chris/chrome/src/out/Release/chrome)
==2745==    by 0x1988068: WebCore::CanvasRenderingContext2D::drawImage(WebCore::HTMLVideoElement*, float, float, float, float, int&) (in /home/chris/chrome/src/out/Release/chrome)
==2745==    by 0x20BD945: WebCore::CanvasRenderingContext2DInternal::drawImageCallback(v8::Arguments const&) (in /home/chris/chrome/src/out/Release/chrome)
==2745==    by 0x142F75C: v8::internal::Builtin_HandleApiCall(v8::internal::(anonymous namespace)::BuiltinArguments<(v8::internal::BuiltinExtraArguments)1>, v8::internal::Isolate*) (in /home/chris/chrome/src/out/Release/chrome)

### sc...@gmail.com (2011-11-07)

Attaching the .ogv for reference

### sc...@gmail.com (2011-11-07)

As per valgrind trace, it's a buffer overflow in Skia. Nasty.
Seems to be a Chrome 17 regression, so it needs to be fixed before we ship it to stable.


### [Deleted User] (2011-11-07)

[Empty comment from Monorail migration]

### at...@gmail.com (2011-11-08)

ASAN Build also reports this bug as heap-buffer-overflow.

17.0.933.0 (Developer Build 108839)

=================================================================
==1840== ERROR: AddressSanitizer heap-buffer-overflow on address 0x7fa9058cf400 at pc 0x7fa911ed071b bp 0x7fff38354ae0 sp 0x7fff38354ad8
WRITE of size 4 at 0x7fa9058cf400 thread T0
    #0 0x7fa911ed071b in SkRgnBuilder::blitH(int, int, int) /third_party/skia/src/core/SkRegion_path.cpp:147
    #1 0x7fa911ee72fe in walk_convex_edges(SkEdge*, SkPath::FillType, SkBlitter*, int, int, void (*)(SkBlitter*, int, bool)) /third_party/skia/src/core/SkScan_Path.cpp:273
    #2 0x7fa911ee63ec in sk_fill_path(SkPath const&, SkIRect const*, SkBlitter*, int, int, int, SkRegion const&) /third_party/skia/src/core/SkScan_Path.cpp:473
    #3 0x7fa911ee8a3d in SkScan::FillPath(SkPath const&, SkRegion const&, SkBlitter*) /third_party/skia/src/core/SkScan_Path.cpp:586
    #4 0x7fa911ed0ee8 in SkRgnBuilder::done() /third_party/skia/src/core/SkRegion_path.cpp:24
    #5 0x7fa911ec24e0 in SkRasterClip::setPath(SkPath const&, SkRegion const&, bool) /third_party/skia/src/core/SkRasterClip.cpp:71
    #6 0x7fa911e5e07d in clipPathHelper /third_party/skia/src/core/SkCanvas.cpp:955
    #7 0x7fa911e5dd78 in SkCanvas::clipRect(SkRect const&, SkRegion::Op, bool) /third_party/skia/src/core/SkCanvas.cpp:940
    #8 0x7fa913dc9b55 in WebCore::GraphicsContext::clip(WebCore::FloatRect const&) /third_party/WebKit/Source/WebCore/platform/graphics/skia/GraphicsContextSkia.cpp:354
    #9 0x7fa913b30652 in WebCore::FloatPoint::x() const /third_party/WebKit/Source/WebCore/platform/graphics/FloatPoint.h:75
    #10 0x7fa913b30012 in WebCore::CanvasRenderingContext2D::drawImage(WebCore::HTMLVideoElement*, float, float, float, float, int&) /third_party/WebKit/Source/WebCore/html/canvas/CanvasRenderingContext2D.cpp:1470
    #11 0x7fa91525f726 in drawImage8Callback /out/Release/obj/gen/webcore/bindings/V8CanvasRenderingContext2D.cpp:1005
    #12 0x7fa8df0476c7 in  
0x7fa9058cf400 is located 0 bytes to the right of 0-byte region [0x7fa9058cf400,0x7fa9058cf400)
freed by thread T0 here:
previously allocated by thread T0 here:
==1840== ABORTING
HINT: ASan doesn't collect stats. Set ASAN_OPTIONS=stats=1 or call __asan_enable_statistics(true)
Stats: 0M malloced (0M for red zones) by 0 calls
Stats: 0M realloced by 0 calls
Stats: 0M freed by 0 calls
Stats: 0M really freed by 0 calls
Stats: 0M (0 full pages) mmaped in 0 calls
  mmaps   by size class:
  mallocs by size class:
  frees   by size class:
  rfrees  by size class:
Stats: malloc large: 0 small slow: 0
Shadow byte and word:
  0x1ff520b19e80: fa
  0x1ff520b19e80: fa fa fa fa fa fa fa fa
More shadow bytes:
  0x1ff520b19e60: 00 00 00 00 00 00 00 00
  0x1ff520b19e68: 00 00 00 00 00 00 00 00
  0x1ff520b19e70: 00 00 00 00 00 00 00 00
  0x1ff520b19e78: 00 00 00 00 00 00 00 00
=>0x1ff520b19e80: fa fa fa fa fa fa fa fa
  0x1ff520b19e88: fa fa fa fa fa fa fa fa
  0x1ff520b19e90: fa fa fa fa fa fa fa fa
  0x1ff520b19e98: fa fa fa fa fa fa fa fa
  0x1ff520b19ea0: fa fa fa fa fa fa fa fa

### re...@google.com (2011-11-08)

BTW - when I build/run in debug on windows, I get an assert early on. It is triggered from a NaN given to us from V8.

static v8::Handle<v8::Value> drawImage8Callback(const v8::Arguments& args)
{
    ...
    EXCEPTION_BLOCK(float, width, static_cast<float>(MAYBE_MISSING_PARAMETER(args, 3, MissingIsUndefined)->NumberValue()));

width is NaN. I don't know if this is expected coming from V8 or not.

I will harden skia to handle this, but I wanted to also document whence the bad value came.


### re...@google.com (2011-11-08)

fixed in skia rev. 2632. working on a DEPS roll.

### ke...@google.com (2011-11-09)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-11-10)

@reed: thanks! I see trunk DEPS has been rolled to r2633 so we're good. Thanks for sorting this out before we branched in into M17 Beta :)

### sc...@gmail.com (2011-11-17)

@attekett: welcome to the Chromium Security Reward program :)
Thanks for catching this regression before we shipped it to Stable or Beta. The repro is nice and reliable and not too large, so we're delighted to offer you a $1000 Chromium Security Reward!

Since the bug doesn't affect stable and is resolved on the dev channel, we can pay you right away. Please e-mail cevans@chromium.org for details on how to collect your reward.

----
Boilerplate text:
Please do NOT publicly disclose details until a fix has been released to all our
users. Early public disclosure may cancel the provisional reward.
Also, please be considerate about disclosure when the bug affects a core library
that may be used by other products.
Please do NOT share this information with third parties who are not directly
involved in fixing the bug. Doing so may cancel the provisional reward.
Please be honest if you have already disclosed anything publicly or to third parties.
----

### at...@gmail.com (2011-11-18)

Thanks. :) I'm proud to be part of the program. I really appreciate your quick response to this issue. 

### sc...@gmail.com (2011-12-20)

Payment in system.

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-06-22)

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

This issue was migrated from crbug.com/chromium/103239?no_tracker_redirect=1

[Multiple monorail components: Internals, Internals>Skia]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40050935)*
