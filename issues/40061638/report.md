# Crash in SkGlyphCache::findImage

| Field | Value |
|-------|-------|
| **Issue ID** | [40061638](https://issues.chromium.org/issues/40061638) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals, Internals>Skia |
| **Reporter** | at...@gmail.com |
| **Assignee** | re...@google.com |
| **Created** | 2012-07-20 |
| **Bounty** | $1,000.00 |

## Description


I tried to get control over the crash address but no luck so far.

Chrome Version: ASAN Chromium 22.0.1208.0 and Google Chrome 20.0.1132.57
OS: Ubuntu 11.04 x86_64

Repro-file:

<html>
	<body></body>
<script>
var canvas=document.body.appendChild(document.createElement("canvas"));
var ctx=canvas.getContext("2d")
canvas.setAttribute("width",869)
canvas.setAttribute("height",18)
ctx.shadowBlur="1000";
ctx.lineWidth="156";
ctx.lineJoin="round";
ctx.strokeStyle="";
ctx.shadowColor="#6E3535";
ctx.shadowOffsetY="-500";
ctx.setTransform(0.8369473826605827,0,0.23122202116064727,0.3953040260821581, 112,11 )
ctx.scale(416,611)
ctx.strokeText("]", 331,12 ,614);
</script>
</html>



ASAN-report:

==3754== ERROR: AddressSanitizer crashed on unknown address 0x7f0e1fe30000 (pc 0x7f0e2a79b38e sp 0x7fff9bc01f78 bp 0x7fff9bc02600 T0)
AddressSanitizer can not provide additional info. ABORTING
    #0 0x7f0e2a79b38e in ?? /build/buildd/eglibc-2.13/string/../sysdeps/x86_64/multiarch/../memset.S:1330
    #1 0x7f0e34222202 in SkGlyphCache::findImage(SkGlyph const&) ???:0
    #2 0x7f0e342161c7 in D1G_NoBounder_RectClip(SkDraw1Glyph const&, int, int, SkGlyph const&) third_party/skia/src/core/SkDraw.cpp:0
    #3 0x7f0e34219e83 in SkDraw::drawPosText(char const*, unsigned long, float const*, float, int, SkPaint const&) const ???:0
    #4 0x7f0e34202951 in SkCanvas::drawPosText(void const*, unsigned long, SkPoint const*, SkPaint const&) ???:0
    #5 0x7f0e350d9e18 in WebCore::Font::drawGlyphs(WebCore::GraphicsContext*, WebCore::SimpleFontData const*, WebCore::GlyphBuffer const&, int, int, WebCore::FloatPoint const&) const ???:0


## Attachments

- [crbug138208-cf-minimized.html](attachments/crbug138208-cf-minimized.html) (text/plain; charset=us-ascii, 363 B)
- [crbug138208-asan.txt](attachments/crbug138208-asan.txt) (text/x-c; charset=us-ascii, 9.5 KB)
- [chrome-heap-buffer-overflow-SkScalerContextgetImage-466.html](attachments/chrome-heap-buffer-overflow-SkScalerContextgetImage-466.html) (text/html; charset=us-ascii, 491 B)
- [chrome-heap-buffer-overflow-SkScalerContextFreeTypegenerateImage-b0e.html](attachments/chrome-heap-buffer-overflow-SkScalerContextFreeTypegenerateImage-b0e.html) (text/html; charset=utf-8, 938 B)

## Timeline

### gl...@chromium.org (2012-07-20)

I wonder why memset didn't get replaced by ASan.

### gl...@chromium.org (2012-07-20)

Perfectly reproducible: 

==8873== ERROR: AddressSanitizer crashed on unknown address 0x7f6c80cbc000 (pc 0x7f6c8cf435b8 sp 0x7fffb078fc98 bp 0x7fffb078fcd0 T0)
AddressSanitizer can not provide additional info. ABORTING
    #0 0x7f6c8cf435b8 in ?? /build/buildd/eglibc-2.11.1/string/../sysdeps/x86_64/memset.S:1056
    #1 0x7f6c9933009d in _ZL12generateMaskRK6SkMaskRK6SkPath /usr/local/google/chrome-commit/src/out/Release/../../third_party/skia/src/core/SkScalerContext.cpp:484
    #2 0x7f6c992d6109 in _ZN12SkGlyphCache9findImageERK7SkGlyph /usr/local/google/chrome-commit/src/out/Release/../../third_party/skia/src/core/SkGlyphCache.cpp:303
    #3 0x7f6c992ca636 in _ZL22D1G_NoBounder_RectClipRK12SkDraw1GlyphiiRK7SkGlyph /usr/local/google/chrome-commit/src/out/Release/../../third_party/skia/src/core/SkDraw.cpp:1375
    #4 0x7f6c992ce5c9 in _ZNK6SkDraw11drawPosTextEPKcmPKffiRK7SkPaint /usr/local/google/chrome-commit/src/out/Release/../../third_party/skia/src/core/SkDraw.cpp:1852
    #5 0x7f6c992b67ee in _ZNK7SkTLazyI7SkPaintE7isValidEv /usr/local/google/chrome-commit/src/out/Release/../../third_party/skia/include/core/SkTLazy.h:78



### gl...@chromium.org (2012-07-20)

From objdump of Chrome for frame #1 (    #1 0x7f6c9933009d (/usr/local/google/chrome-commit/src/out/Release/chrome+0x658d09d)):

 658d090:       4c 89 ef                mov    %r13,%rdi
 658d093:       31 f6                   xor    %esi,%esi
 658d095:       48 89 c2                mov    %rax,%rdx
 658d098:       e8 33 44 d3 02          callq  92c14d0 <__interceptor_memset>
 658d09d:       48 89 df                mov    %rbx,%rdi

So we actually intercept memset and check for the shadow value of 0x7f6c80cbc000, but this page isn't mapped, so the shadow check passes and the libc memset is called, which in turn crashes. Looks like a true positive then.

### in...@chromium.org (2012-07-20)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-07-20)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=80392301

Uploader: inferno@chromium.org

Crash Type: UNKNOWN
Crash Address: 0x7fde00a1d000
Crash State:
  - crash stack -
  /lib/libc-2.11.1.so+Unknown
  SkScalerContext::getImage
  SkGlyphCache::findImage
  

Minimized Testcase (0.35 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv94Ds4bt7lDBcOYeg_UtL-H1U5HJu77qte393RQFDUBWMhRZHdt4InC8utIPic929Jd2V8vTMumOwnYbOKxTNYqSyf72_UgZfeXXr_4bQJmP7Iw8XK_8bSjaPC8qxZ1yQlmLQ0GVq1Z9JR3tA628-lUh98Ukt0vc-_EjzR7iAKveayhyPOY
</body>
<script>
var canvas=document.body.appendChild(document.createElement("canvas"));
var ctx=canvas.getContext("2d")
ctx.shadowBlur="1000";
ctx.lineWidth="156";
ctx.lineJoin="round";
ctx.shadowColor="#6E3535";
ctx.setTransform(0.8369473826605827,0,0.23122202116064727,0.3953040260821581, 112,11 )
ctx.scale(416,611)
ctx.strokeText("]", 331,12 ,614);
</script>

### in...@chromium.org (2012-07-20)

you can check on clusterfuzz report again to see the regression range.

### [Deleted User] (2012-07-20)

[Empty comment from Monorail migration]

### ep...@google.com (2012-07-24)

I can reproduce the ASAN error by viewing the attached test case in this local release build on my Linux desktop via NX:
Chromium 22.0.1209.0 (Developer Build 146872) 

Full ASAN log is attached; here is the top:

ASAN:SIGSEGV
==24162== ERROR: AddressSanitizer crashed on unknown address 0x7f754a50a000 (pc 0x7f75752475b8 sp 0x7fff2a3196c8 bp 0x7fff2a319700 T0)
AddressSanitizer can not provide additional info. ABORTING
    #0 0x7f75752475b8 in ?? /build/buildd/eglibc-2.11.1/string/../sysdeps/x86_64/memset.S:1056
    #1 0x7f757e740a17 in sk_bzero(void*, unsigned long) third_party/skia/include/core/SkTypes.h:70
    #2 0x7f757e740d94 in generateMask(SkMask const&, SkPath const&) third_party/skia/src/core/SkScalerContext.cpp:482
    #3 0x7f757e74053d in SkScalerContext::getImage(SkGlyph const&) third_party/skia/src/core/SkScalerContext.cpp:545
    #4 0x7f757e702029 in SkGlyphCache::findImage(SkGlyph const&) third_party/skia/src/core/SkGlyphCache.cpp:303
    #5 0x7f757e6f794e in D1G_NoBounder_RectClip(SkDraw1Glyph const&, int, int, SkGlyph const&) third_party/skia/src/core/SkDraw.cpp:1375
    #6 0x7f757e6fa331 in SkDraw::drawPosText(char const*, unsigned long, float const*, float, int, SkPaint const&) const third_party/skia/src/core/SkDraw.cpp:1852
    #7 0x7f757e6e9036 in SkCanvas::drawPosText(void const*, unsigned long, SkPoint const*, SkPaint const&) third_party/skia/src/core/SkCanvas.cpp:1812
    #8 0x7f757f210722 in WebCore::Font::drawGlyphs(WebCore::GraphicsContext*, WebCore::SimpleFontData const*, WebCore::GlyphBuffer const&, int, int, WebCore::FloatPoint const&) const third_party/WebKit/Source/WebCore/platform/graphics/harfbuzz/FontHarfBuzz.cpp:151


### ep...@google.com (2012-07-24)

When I view the test case on this local debug build, in gdb, in single-process mode:
Chromium 22.0.1209.0 (Developer Build 146887) running on my Linux desktop via NX

I get this assert failure (unfortunately, gdb tells me that "x" has been optimized out)

[11461:11507:354135462260:FATAL:SkDebug.cpp(34)] third_party/skia/src/core/SkDebug.cpp:34: failed assertion "(uint16_t)x == x"

Backtrace:
	base::debug::StackTrace::StackTrace() [0x7fffc9773a04]
	logging::LogMessage::~LogMessage() [0x7fffc98df7ed]
	SkDebugf_FileLine() [0x7fffd0c69be4]
	SkToU16() [0x7fffd0768bf4]
	SkScalerContext::getMetrics() [0x7fffd09cbaf4]
	SkGlyphCache::lookupMetrics() [0x7fffd07db212]
	SkGlyphCache::getGlyphIDMetrics() [0x7fffd07de409]
	sk_getMetrics_glyph_00() [0x7fffd0868ec4]
	SkDraw::drawPosText() [0x7fffd07a8b1d]
	SkDevice::drawPosText() [0x7fffd0779eb4]
	SkCanvas::drawPosText() [0x7fffd073379f]
	WebCore::Font::drawGlyphs() [0x7fffd50dc19b]
	WebCore::Font::drawGlyphBuffer() [0x7fffd4e79c35]
	WebCore::Font::drawSimpleText() [0x7fffd4e78324]
	WebCore::Font::drawText() [0x7fffd4ddf7c0]
	WebCore::GraphicsContext::drawBidiText() [0x7fffd4f39168]
	WebCore::CanvasRenderingContext2D::drawTextInternal() [0x7fffd46a7e19]
	WebCore::CanvasRenderingContext2D::strokeText() [0x7fffd46a981e]
	WebCore::CanvasRenderingContext2DV8Internal::strokeTextCallback() [0x7fffdadd5655]
	v8::internal::HandleApiCallHelper<>() [0x7fffccc7f0df]
	v8::internal::Builtin_Impl_HandleApiCall() [0x7fffccc7de36]
	v8::internal::Builtin_HandleApiCall() [0x7fffccc54650]
	0x232a3f40618e

### in...@chromium.org (2012-08-01)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-08-01)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-08-01)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-08-02)

Please do read Mark's email titled "Code Yellow: Security Bug Backlog" on chrome-team mailing list.

### [Deleted User] (2012-08-02)

We are overflowing coordinates when I convert very-large floats to fixed in the font scaler. Don't know if this can lead to reading bad memory, unless we've ever seen an ASAN violation in the release build.

I will look for ways to catch this earlier in the process, to avoid the assert.

### in...@chromium.org (2012-08-06)

Mike, as per crash (release), we are crashing on memset(buffer, 0, size); which does not look good at all. Looks like we are passing a bad overflowed size ? 

### in...@chromium.org (2012-08-06)

[Empty comment from Monorail migration]

### at...@gmail.com (2012-08-07)

New repro-file with little bit different ASAN-report.

==18144== ERROR: AddressSanitizer heap-buffer-overflow on address 0x7f48b836a3da at pc 0x7f48cdfa9c5e bp 0x7fffc8d94e50 sp 0x7fffc8d94e48
WRITE of size 1 at 0x7f48b836a3da thread T0
    #0 0x7f48cdfa9c5d in SkScalerContext::getImage(SkGlyph const&) ???:0
    #1 0x7f48cdf4af98 in SkGlyphCache::findImage(SkGlyph const&) ???:0
    #2 0x7f48cdf3e827 in D1G_NoBounder_RectClip(SkDraw1Glyph const&, int, int, SkGlyph const&) ../../third_party/skia/src/core/SkDraw.cpp:0
    #3 0x7f48cdf42828 in SkDraw::drawPosText(char const*, unsigned long, float const*, float, int, SkPaint const&) const ???:0
    #4 0x7f48cdf274e0 in SkCanvas::drawPosText(void const*, unsigned long, SkPoint const*, SkPaint const&) ???:0
    #5 0x7f48ce2effdd in WebCore::Font::drawGlyphs(WebCore::GraphicsContext*, WebCore::SimpleFontData const*, WebCore::GlyphBuffer const&, int, int, WebCore::FloatPoint const&) const ???:0
    #6 0x7f48ce26ddcd in WebCore::Font::drawGlyphBuffer(WebCore::GraphicsContext*, WebCore::TextRun const&, WebCore::GlyphBuffer const&, WebCore::FloatPoint const&) const ???:0
    #7 0x7f48ce26d608 in WebCore::Font::drawSimpleText(WebCore::GraphicsContext*, WebCore::TextRun const&, WebCore::FloatPoint const&, int, int) const ???:0
    #8 0x7f48ce288ad0 in WebCore::GraphicsContext::drawBidiText(WebCore::Font const&, WebCore::TextRun const&, WebCore::FloatPoint const&) ???:0
    #9 0x7f48cfd68fc1 in WebCore::CanvasRenderingContext2D::drawTextInternal(WTF::String const&, float, float, bool, float, bool) ???:0
    #10 0x7f48cd5b5a0e in WebCore::CanvasRenderingContext2DV8Internal::strokeTextCallback(v8::Arguments const&) gen/webkit/bindings/V8DerivedSources17.cpp:0


### in...@chromium.org (2012-08-09)

Mike, just a fyi, this is our last high severity skia bug and has higher priority than other medium severity ones for code yellow.

### [Deleted User] (2012-08-10)

Ah, ok. I will pause working on http://code.google.com/p/chromium/issues/detail?id=141651 and switch back to this one.

### in...@chromium.org (2012-08-10)

Thank you very much Mike. You are our hero. Great job in knocking these Skia bugs so quick.

### to...@chromium.org (2012-08-10)

I've written a couple unit tests to attempt to recreate the reproduction cases in raw Skia, but they aren't triggering the same codepaths - neither the SkToU16() calls in SkScalerContext::getMetrics() nor SkScalerContext::getImage() are hit.

http://codereview.appspot.com/6446117/

I've forced bitmap filtering on the paint, but that didn't help; other suggestions would be appreciated!

### ep...@google.com (2012-08-13)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-08-15)

Is https://codereview.appspot.com/6446117/ fixed ? Sorry, but i don't have permission to see that codereview and can't determine the status.

### to...@chromium.org (2012-08-15)

Nope, we've made no progress on a standalone repro case. Per #14, Mike has a handle on the likely cause, and so we may be able to get a fix in even if we don't have a test case to add to the Skia suite.

Sorry about permissions, I figured that since this is SecSeverity-High we ought to keep spawned bugs private, too.

### at...@gmail.com (2012-08-19)

One more repro-file. I think that this is also from the same root-cause, but because of the multiple different stacks caused by the same repro-file, I think that after you have the patch ready this repro-file should be checked.

I have seen the following crashes caused by the same repro-file without any modifications. 

==9254== ERROR: AddressSanitizer heap-buffer-overflow on address 0x7f1e8e2a01a0 at pc 0x7f1ec4beb4a6 bp 0x7fff837a1e30 sp 0x7fff837a1e28
READ of size 1 at 0x7f1e8e2a01a0 thread T0
    #0 0x7f1ec4beb4a5 in build_sum_buffer(unsigned int*, int, int, unsigned char const*, int) ../../third_party/skia/src/effects/SkBlurMask.cpp:0
    #1 0x7f1ec4bea573 in SkBlurMask::Blur(SkMask*, SkMask const&, float, SkBlurMask::Style, SkBlurMask::Quality, SkIPoint*) ???:0
    #2 0x7f1ec4bda148 in SkBlurMaskFilterImpl::filterMask(SkMask*, SkMask const&, SkMatrix const&, SkIPoint*) ???:0
    #3 0x7f1ec4b2fff8 in SkScalerContext::getImage(SkGlyph const&) ???:0
    #4 0x7f1ec4ad37a8 in SkGlyphCache::findImage(SkGlyph const&) ???:0


==9247== ERROR: AddressSanitizer crashed on unknown address 0x7f1eac000000 (pc 0x7f1eb82f7fc8 sp 0x7fff837a1e38 bp 0x7fff837a1e70 T0)
AddressSanitizer can not provide additional info.
    #0 0x7f1eb82f7fc7 in ?? /build/buildd/eglibc-2.15/string/../sysdeps/x86_64/multiarch/../memset.S:879
    #1 0x7f1ec4a5f74c in SkScalerContext_FreeType::generateImage(SkGlyph const&, SkTMaskPreBlend<2, 2, 2>*) ???:0
    #2 0x7f1ec4b2e635 in SkScalerContext::getImage(SkGlyph const&) ???:0
    #3 0x7f1ec4ad37a8 in SkGlyphCache::findImage(SkGlyph const&) ???:0
    #4 0x7f1ec4ac1cc7 in D1G_NoBounder_RectClip(SkDraw1Glyph const&, int, int, SkGlyph const&) ../../third_party/skia/src/core/SkDraw.cpp:0

==9258== ERROR: AddressSanitizer heap-buffer-overflow on address 0x7f1eae4689b3 at pc 0x7f1ec4a5f78e bp 0x7fff837a1e70 sp 0x7fff837a1e68
WRITE of size 1 at 0x7f1eae4689b3 thread T0
    #0 0x7f1ec4a5f78d in SkScalerContext_FreeType::generateImage(SkGlyph const&, SkTMaskPreBlend<2, 2, 2>*) ???:0
    #1 0x7f1ec4b2e635 in SkScalerContext::getImage(SkGlyph const&) ???:0
    #2 0x7f1ec4ad37a8 in SkGlyphCache::findImage(SkGlyph const&) ???:0
    #3 0x7f1ec4ac1cc7 in D1G_NoBounder_RectClip(SkDraw1Glyph const&, int, int, SkGlyph const&) ../../third_party/skia/src/core/SkDraw.cpp:0
    #4 0x7f1ec4ac5c3e in SkDraw::drawPosText(char const*, unsigned long, float const*, float, int, SkPaint const&) const ???:0




### in...@chromium.org (2012-08-19)

c#25 bug is already covered by http://code.google.com/p/chromium/issues/detail?id=143409

### ep...@google.com (2012-08-23)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-08-23)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-09-05)

Skia guys, any updates on these. These high severity bugs we would definitely like to get knocked out before pwnium 2, your help is highly appreciated.

### sc...@gmail.com (2012-09-06)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-09-21)

Well this bug is stopping the entire skia fuzzing module of our external reporter Attekett since it is hitting pretty often. We have one last change for a fix for this since the last beta is next week before pwnium. Any chance to sneak a fix ?

### re...@google.com (2012-09-21)

I have yet to catch one of these in action, but I will start again today to try to repro this.

### at...@gmail.com (2012-09-21)

Let me know if you have problem with reproducing the issue with the files attached to this issue. I can fairly easily get a collection of unminimized repro-files.

### re...@google.com (2012-09-21)

fix in skia rev. 5640

should be very easy to cherry pick, as it is 3 lines in one file.

### in...@chromium.org (2012-09-21)

Thanks Mike for the fix, can you please merge to 1229 m22 branch.

### re...@google.com (2012-09-21)

the cherry has landed http://code.google.com/p/skia/source/detail?r=5643

### sc...@gmail.com (2012-09-21)

One less bug! Yeehaa. This won't make the M22 stable release, but will make the first M22 stable patch.

### in...@chromium.org (2012-09-25)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-09-25)

OOB write, $1000

### sc...@gmail.com (2012-10-02)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-10-02)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-10-12)

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

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/138208?no_tracker_redirect=1

[Multiple monorail components: Internals, Internals>Skia]
[Monorail blocking: crbug.com/chromium/143409]
[Monorail mergedwith: crbug.com/chromium/143995, crbug.com/chromium/144441]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061638)*
