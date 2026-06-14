# Security: Canvas toDataURL security error: It is taking page information and not the canvas when making the image

| Field | Value |
|-------|-------|
| **Issue ID** | [40093249](https://issues.chromium.org/issues/40093249) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink |
| **Reporter** | si...@gmail.com |
| **Assignee** | bs...@google.com |
| **Created** | 2011-07-29 |
| **Bounty** | $500.00 |

## Description

**This template is ONLY for reporting security bugs. Please use a different**  

**template for other types of bug reports.**

**Please see the following link for instructions on filing security bugs:**  

**<http://www.chromium.org/Home/chromium-security/reporting-security-bugs>**

**VULNERABILITY DETAILS**  

Using toDataURL on Canvas in Canary is causing an image to be created with elements that are outside of the Canvas. This is a regression that is in violation of the Canvas spec and a security error.

**VERSION**  

Chrome Version: 14.0.835.9 canary  

Operating System: Windows 7

**REPRODUCTION CASE**  

<http://simonsarris.com/misc/textBaseline.html>

Press the button to make an image out of the Canvas.

Typically the image created would contain nothing but the canvas and NEVER other items on the page.

The image created instead includes other items on the page. This should never occur.

See the attachment for sample image created.

## Attachments

- [chrome-canary.png](attachments/chrome-canary.png) (image/png; charset=binary, 8.3 KB)

## Timeline

### js...@chromium.org (2011-07-30)

This seems like it should be fixed in WebKit. Neckar, you were looking at this yesterday, so assigning to you for the moment.

### sc...@gmail.com (2011-08-04)

We're getting a fair few reports on this; seems like an obvious regression. I'll mail Ken and James.

### sc...@gmail.com (2011-08-04)

[Empty comment from Monorail migration]

### kb...@chromium.org (2011-08-04)

This sounds like it's a bug related to the use of accelerated 2D canvas. CC'ing a few more people.


### ja...@chromium.org (2011-08-04)

I don't think our command buffer infrastructure should be allowing this sort of thing at all.  ReleaseBlock-Beta at _least_.

### [Deleted User] (2011-08-04)

Brian, any ideas? 

Here's a seemingly relevant stack trace:

0x65b15c7a	 [chrome.dll	 - gles2_implementation.cc:1671]	gpu::gles2::GLES2Implementation::ReadPixels(int,int,int,int,unsigned int,unsigned int,void *)
0x65b18386	 [chrome.dll	 - gles2_c_lib_autogen.h:332]	GLES2ReadPixels
0x65b0e848	 [chrome.dll	 - grgpugl.cpp:1345]	GrGpuGL::onReadPixels(GrRenderTarget *,int,int,int,int,GrPixelConfig,void *)
0x65af1e29	 [chrome.dll	 - grgpu.cpp:189]	GrGpu::readPixels(GrRenderTarget *,int,int,int,int,GrPixelConfig,void *)
0x65adf1ad	 [chrome.dll	 - grcontext.cpp:1456]	GrContext::readRenderTargetPixels(GrRenderTarget *,int,int,int,int,GrPixelConfig,void *)
0x6663d995	 [chrome.dll	 - skgrtexturepixelref.cpp:133]	SkGrRenderTargetPixelRef::onReadPixels(SkBitmap *,SkIRect const *)
0x6663d794	 [chrome.dll	 - skgrtexturepixelref.cpp:38]	SkROLockPixelsPixelRef::onLockPixels(SkColorTable * *)
0x65ad774f	 [chrome.dll	 - skbitmap.cpp:337]	SkBitmap::lockPixels()
0x65ae6179	 [chrome.dll	 - skdraw.cpp:1168]	SkDraw::drawBitmap(SkBitmap const &,SkMatrix const &,SkPaint const &)
0x65ad9163	 [chrome.dll	 - skdevice.cpp:169]	SkDevice::drawBitmap(SkDraw const &,SkBitmap const &,SkIRect const *,SkMatrix const &,SkPaint const &)
0x65adc644	 [chrome.dll	 - skcanvas.cpp:1339]	SkCanvas::commonDrawBitmap(SkBitmap const &,SkIRect const *,SkMatrix const &,SkPaint const &)
0x65adba17	 [chrome.dll	 - skcanvas.cpp:823]	SkCanvas::internalDrawBitmap(SkBitmap const &,SkIRect const *,SkMatrix const &,SkPaint const *)

http://crash/reportdetail?reportid=90e2352e39c5bfb3

and there's a lot of identical reports, all in 14.0.x releases . I don't see any in 15.x  . Maybe something recently fixed on trunk?

### bs...@google.com (2011-08-04)

Off the top of my head I'm not sure. I'm WFH this morning but will have a look as soon as I get in to the office.

### bs...@google.com (2011-08-04)

Stephen, does this look like the src/dst make current issue you fixed recently? It looks like we're doing a readback to draw a texture backed SkBitmap to a sw-raster SkDevice.

### bs...@google.com (2011-08-04)

My suspicion is we're reading from the compositors context rather than the canvas context.

### bs...@google.com (2011-08-04)

Upstack is BitmapImageSingleFrameSkia::draw which makes current the dst's context, but in this case it is the src that is gpu backed.

### se...@chromium.org (2011-08-04)

It's possible, but the only case I know of where accel->non-accel drawing happens currently is in printing.  Perhaps this is the accel->accel case, but the spurious readback is confusing skia.  That should be fixed as of http://trac.webkit.org/changeset/92297.  I'll try to repro with and without that patch.

### se...@chromium.org (2011-08-04)

I haven't been able to repro the problem as shown above yet, although I did get a version in which the canvas is drawn incorrectly (no large characters are drawn, only the outline box).  bisecting builds on that error led to chromium r92327:92335, which included the WebKit roll 90859:90895, which included the problematic change which removed the legacy canvas2D implementation (subsequently fixed, so that should not be showing up in the Canary anymore).

I'll try bisecting more recent builds to see if I can repro the problem as shown.

### se...@chromium.org (2011-08-04)

BTW I also could not repro in Canary 15.0.841.0 (chromium r95020).

### si...@gmail.com (2011-08-04)

I just noticed something in 15.0.844.0 canary

Hitting the save to PNG button on the page gives me a blank PNG.

But if I open Chrome developer tools and hit the save to PNG button, then suddenly I get the flawed image that is described.

I do not remember if developer tools was open when I first reported this bug, but give that a try.

### se...@chromium.org (2011-08-04)

I take it back -- the original canvas is fine in canary, but the resulting PNG is blank.

### bs...@google.com (2011-08-04)

Here is the callstack for the readback on the reported URL. It's different than the crash report stack (which looks like a dup of the bug Stephen fixed):



 1      skia.dll!GrContext::readRenderTargetPixels(GrRenderTarget * target=0x1c008868, int left=0x00000000, int top=0x00000000, int width=0x00000212, int height=0x000000b4, GrPixelConfig config=kRGBA_8888_GrPixelConfig, void * buffer=0x1c168438) 
 2      skia.dll!GrRenderTarget::readPixels(int left=0x00000000, int top=0x00000000, int width=0x00000212, int height=0x000000b4, GrPixelConfig config=kRGBA_8888_GrPixelConfig, void * buffer=0x1c168438) 
 3      skia.dll!SkGrRenderTargetPixelRef::onReadPixels(SkBitmap * dst=0x1bc6f8f8, const SkIRect * subset=0x00000000) 
 4      skia.dll!SkROLockPixelsPixelRef::onLockPixels(SkColorTable * * ctable=0x1bc6f8e0) 
 5      skia.dll!SkPixelRef::lockPixels() 
 6      skia.dll!SkBitmap::lockPixels() 
*7      webkit.dll!WebCore::ImageBuffer::toDataURL(const WTF::String & mimeType={...}, const double * quality=0x00000000) 
 8      webkit.dll!WebCore::HTMLCanvasElement::toDataURL(const WTF::String & mimeType={...}, const double * quality=0x00000000, int & ec=0x00000000) 
 9      webkit.dll!WebCore::V8HTMLCanvasElement::toDataURLCallback(const v8::Arguments & args={...}) 
 10     v8.dll!v8::internal::HandleApiCallHelper<0>(v8::internal::`anonymous-namespace'::BuiltinArguments<1> args={...}, v8::internal::Isolate * isolate=0x00a70068) 
 11     v8.dll!v8::internal::Builtin_Impl_HandleApiCall(v8::internal::`anonymous-namespace'::BuiltinArguments<1> args={...}, v8::internal::Isolate * isolate=0x00a70068) 
 12     v8.dll!v8::internal::Builtin_HandleApiCall(v8::internal::`anonymous-namespace'::BuiltinArguments<1> args={...}, v8::internal::Isolate * isolate=0x00a70068) 


### si...@gmail.com (2011-08-04)

senorblanco, can you corroborate whether or not having developer tools open causes the bug? That seems to be the consistent thing for me in both dev and canary - that the PNG will be blank unless developer tools is open, in which case it will be flawed.

### bs...@google.com (2011-08-04)

Putting a make current in WebCore::ImageBuffer::toDataURL fixes it.

### se...@chromium.org (2011-08-04)

Seems like it's just not setting the context current before toDataURL().  I have no idea how this ever worked (maybe luck?).

Bug and patch filed upstream at https://bugs.webkit.org/show_bug.cgi?id=65700

### sc...@gmail.com (2011-08-04)

Awesome, sounds like two different bugs, and two WebKit merges needed to the M14 branch. I can tackle those for you.

In terms of @senorblanco's recent bugfix https://bugs.webkit.org/show_bug.cgi?id=65560, was there a Chromium bug to track it? I don't immediately see one.

### se...@chromium.org (2011-08-04)

simon:  No, with dev tools up in canary I still get a blank PNG.  Regardless, I'm pretty sure the patch above will fix your symptoms too.

### se...@chromium.org (2011-08-04)

scarybeasts:  the chromium bug for wk65560 was http://code.google.com/p/chromium/issues/detail?id=55927 (still open due to WebGL printing problems).  Those fixes were already merged to the M14 WebKit branch as http://src.chromium.org/viewvc/chrome?view=rev&revision=92296 and http://src.chromium.org/viewvc/chrome?view=rev&revision=92297

### se...@chromium.org (2011-08-04)

(Er, those links should be http://trac.webkit.org/changeset/92296 and http://trac.webkit.org/changeset/92297 of course (I guess drover is a little URL-confused when uploading webkit patches to chromium rietveld!)).

### sc...@gmail.com (2011-08-04)

Thanks guys. I can merge to M14 if you like.

Committed r92388: <http://trac.webkit.org/changeset/92388>

### se...@chromium.org (2011-08-04)

scarybeasts:  I was gonna let it the WebKit merge go through first (and let it bake on trunk w/full bots for a bit).  But if you're ok with just canary coverage, it's looking ok so far.

### se...@chromium.org (2011-08-05)

OK, looks fine on trunk.  Merged to 835 at http://trac.webkit.org/changeset/92482.

### sc...@gmail.com (2011-08-05)

Thanks!

### si...@gmail.com (2011-08-09)

This looks right in Canary now for my example. Thanks guys!

### sc...@gmail.com (2011-08-24)

@simon.sarris: thanks for being the first to notice this regression! Since it's a security bug, and you were the first, this qualifies you for a provisional $500 Chromium Security Reward :D Congrats!

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

### si...@gmail.com (2011-08-24)

Wow, thanks!

### sc...@gmail.com (2011-09-16)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-10-05)

Batch update.

### sc...@gmail.com (2011-10-28)

@simon.sarris: please e-mail cevans@chromium.org for steps to collect your reward.

### sc...@gmail.com (2011-11-23)

Payment in system.

### [Deleted User] (2012-05-15)

Marking old security bugs Fixed..

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### la...@google.com (2013-01-18)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-10)

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

### bu...@chromium.org (2013-04-06)

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

This issue was migrated from crbug.com/chromium/91016?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/91541]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093249)*
