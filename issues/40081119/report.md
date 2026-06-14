# Security: Integer Overflow in WebGL

| Field | Value |
|-------|-------|
| **Issue ID** | [40081119](https://issues.chromium.org/issues/40081119) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebGL |
| **Reporter** | de...@gmail.com |
| **Assignee** | re...@google.com |
| **Created** | 2015-01-05 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

When calling texImage2D in JavaScript, it will call WebGLRenderingContextBase::texImage2D.  

If the image type is svg it will drawImageIntoBuffer, during which a large image width (>= 0x40000000) will cause multiply integer overflow.

// JavaScript  

textureImage.width = 0x40000001;  

gl.texImage2D(0, 0, 0, 0, 0, textureImage);

// E:\depot\_tools\src\third\_party\WebKit\Source\core\html\canvas\WebGLRenderingContextBase.cpp  

void WebGLRenderingContextBase::texImage2D(GLenum target, GLint level, GLenum internalformat,  

GLenum format, GLenum type, HTMLImageElement\* image, ExceptionState& exceptionState) {  

...  

if (imageForRender->isSVGImage())  

imageForRender = drawImageIntoBuffer(imageForRender.get(), image->width(), image->height(), "texImage2D");  

...  

}

// E:\depot\_tools\src\third\_party\skia\src\core\SkMallocPixelRef.cpp  

SkMallocPixelRef\* SkMallocPixelRef::NewAllocate(const SkImageInfo& info, size\_t requestedRowBytes, SkColorTable\* ctable) {  

// info {fWidth=0x40000001 fHeight=0x00000096 ...}  

...  

int32\_t minRB = SkToS32(info.minRowBytes()); // Overflow: see minRowBytes(), minRB = 0x00000004  

...  

rowBytes = minRB;

```
int64_t bigSize = (int64_t)info.height() \* rowBytes;  
...  
size_t size = sk_64_asS32(bigSize);  
SkASSERT(size >= info.getSafeSize(rowBytes));  
void\* addr = sk_malloc_flags(size, 0); // Allocate memory with overflowed size = 0x00000258  
...  

```

}

size\_t minRowBytes() const {  

return (size\_t)this->minRowBytes64();  

// return 0x00000004  

}

uint64\_t minRowBytes64() const {  

return sk\_64\_mul(fWidth, this->bytesPerPixel()); // fWidth = 0x40000001, this->bytesPerPixel() = 0x4  

// return 0x0000000100000004  

}

Call Stack:  

skia.dll!SkMallocPixelRef::NewAllocate(const SkImageInfo & info={...}, unsigned int requestedRowBytes=0x00000000, SkColorTable \* ctable=0x00000000)  

skia.dll!SkSurface::NewRaster(const SkImageInfo & info={...}, const SkSurfaceProps \* props=0x0018e380)  

blink\_platform.dll!blink::UnacceleratedImageBufferSurface::UnacceleratedImageBufferSurface(const blink::IntSize & size={...}, blink::OpacityMode opacityMode=NonOpaque)  

blink\_platform.dll!blink::ImageBuffer::create(const blink::IntSize & size={...}, blink::OpacityMode opacityMode=NonOpaque)  

blink\_web.dll!blink::WebGLRenderingContextBase::LRUImageBufferCache::imageBuffer(const blink::IntSize & size={...})  

blink\_web.dll!blink::WebGLRenderingContextBase::drawImageIntoBuffer(blink::Image \* image=0x322748d0, int width=0x40000001, int height=0x00000096, const char \* functionName=0x1e15332c)  

blink\_web.dll!blink::WebGLRenderingContextBase::texImage2D(unsigned int target=0x00000000, int level=0x00000000, unsigned int internalformat=0x00000000, unsigned int format=0x00000000, unsigned int type=0x00000000, blink::HTMLImageElement \* image=0x5ee383d0, blink::ExceptionState & exceptionState={...})  

blink\_web.dll!blink::WebGLRenderingContextV8Internal::texImage2D3Method(const v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) & info={...})  

blink\_web.dll!blink::WebGLRenderingContextV8Internal::texImage2DMethod(const v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) & info={...})  

blink\_web.dll!blink::WebGLRenderingContextV8Internal::texImage2DMethodCallback(const v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) & info={...})  

v8.dll!v8::internal::FunctionCallbackArguments::Call(void (const v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) &)  

v8.dll!v8::internal::HandleApiCallHelper<0>(v8::internal::`anonymous-namespace'::BuiltinArguments<1> args={...}, v8::internal::Isolate \* isolate=0x2c108091)  

v8.dll!v8::internal::Builtin\_HandleApiCall(int args\_length=0x00000008, v8::internal::Object \* \* args\_object=0x0018e77c, v8::internal::Isolate \* isolate=0x2bc52100)  

...  

JavaScript JIT code

**VERSION**  

Chrome Version: 41.0.2246.0 + dev  

Operating System: Windows 7 ultimate 64-bit Service Pack 1

**REPRODUCTION CASE**  

attachment

## Attachments

- [2015-01-05@Integer Overflow in WebGL.html](attachments/2015-01-05@Integer Overflow in WebGL.html) (text/html, 708 B)
- [demiSvg.svg](attachments/demiSvg.svg) (image/svg+xml, 46 B)

## Timeline

### cl...@chromium.org (2015-01-06)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=6298003131334656

### in...@chromium.org (2015-01-06)

Ken, can you please help with an owner.

### zm...@chromium.org (2015-01-06)

[Empty comment from Monorail migration]

### in...@chromium.org (2015-01-07)

[Empty comment from Monorail migration]

### in...@chromium.org (2015-01-07)

[Empty comment from Monorail migration]

### zm...@chromium.org (2015-01-08)

I did some code reading.  It seems to me that there is nothing to be done in Chromium/Blink side, as it expects an invalid surface from SkSurface::NewRaster at overflow.

However, SkMallocPixelRef::NewAllocate needs to be more overflow-aware.

Assigning to @reed.

### de...@gmail.com (2015-01-23)

@zmo: Good analysis, thank you for helping reading the code!

### cl...@chromium.org (2015-01-23)

reed@: Uh oh! This issue is still open and hasn't been updated in the last 14 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### [Deleted User] (2015-01-23)

[Empty comment from Monorail migration]

### de...@gmail.com (2015-02-05)

Well, I hope I can help...

### de...@gmail.com (2015-02-06)

clusterfuzz@: I have tried to disable these nags, while I can't find how to add 'WIP' label and create an optional codereview link. Can you please help telling me how to do it?

### in...@chromium.org (2015-02-06)

demi6d: the nags are for the developer fixing bug and not you.

### cl...@chromium.org (2015-02-06)

reed@: Uh oh! This issue is still open and hasn't been updated in the last 28 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### de...@gmail.com (2015-02-07)

inferno: Thank you very much for your information! I just think when developer is focusing on developing one module, it really disrupt uncomfortably to change to another one, so I just want to help...
And according to @zmo's analysis "expects an invalid surface from SkSurface::NewRaster at overflow", I can do check in SkMallocPixelRef::NewAllocate and if overflowed then set surface to null, because invalid surface is null according to isValid():
bool UnacceleratedImageBufferSurface::isValid() const {
    return m_surface;
}
Although I'm not familiar with the code base, this logic seems not very complicate or maybe I miss something... I'm thinking about that maybe I can register a chromium account in the future when I am qualified :)

### in...@chromium.org (2015-02-07)

demi6d: thanks a lot for all your analysis. do you want to take a shot at uploading a chromium patch on codereview.chromium.org. and please mark zmo@, kbr@ as reviewiers. Uploading a patch will make this qualify for the higher rewards.

### de...@gmail.com (2015-02-08)

inferno: thank you for your help! I just learnt how to upload a cl, updated my chromium code and compile tools today and then plan to write a fix... While reading the related code, I find that reed@ has already fixed it with same idea but very nice code two weeks ago just when assigned...

https://codereview.chromium.org/871993003

@reed: quick and great fix, thank you!

### in...@chromium.org (2015-02-08)

Thanks, fixed in https://skia.googlesource.com/skia/+/2ff257bd95c732b9cebc3aac03fbed72d6e6082a

### cl...@chromium.org (2015-02-08)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### de...@gmail.com (2015-02-09)

inferno: thank you for always quick response to the report!


If there is a credit, I hope it the same as before: 

Chen Zhang (demi6od) of the NSFOCUS Security Team

### de...@gmail.com (2015-02-11)

[Comment Deleted]

### mb...@chromium.org (2015-02-11)

Sometimes we forget to add the reward-topanel label, but we're usually pretty good about going through the bugs to see if we missed any before voting on reward amounts for a release. Either way, this one definitely should have it.

### de...@gmail.com (2015-02-11)

Thank you for your information!

### ti...@google.com (2015-02-17)

Merge Requested to M41 (Branch 2272)

### pe...@google.com (2015-02-17)

[Automated comment] No bugdroid (commit) comments found, couldn't auto-approve, needs manual review.

### pe...@chromium.org (2015-02-18)

Merge approved for M41 branch 2272.

### pe...@chromium.org (2015-02-20)

Note: M41 stable cut happens in days, and you're approved for merge.  Get it in there!  (Let me know if you need any help, or aren't confident.)

### ti...@google.com (2015-02-23)

reed: Please merge your fix to M41 (branch 2272). Thanks.

### pe...@chromium.org (2015-02-24)

You have about 18 hours to get this into M41, or it'll be punted.  I can't do the merge for you in skia.  Adding Heather Miller in case she can help.

### hc...@chromium.org (2015-02-24)

Thanks for the CC. I can cherry pick into our Skia chrome/m41 branch, but want to confirm with Mike (and have him do it/test if possible).. will fup early AM.

### hc...@chromium.org (2015-02-24)

I cherry-picked and tested the change into the chrome/m41 branch of Skia.  It is on tip of branch now and should get picked up in the next build.

### ti...@google.com (2015-02-26)

[Empty comment from Monorail migration]

### ti...@google.com (2015-03-03)

Congratulations - $3000 for this report.

### de...@gmail.com (2015-03-04)

Thank you very much!

### ti...@google.com (2015-03-11)

[Empty comment from Monorail migration]

### ti...@google.com (2015-03-17)

Processing via our e-payment system can take up to six weeks, but the reward should be on its way to you. Thanks again for your help!

### de...@gmail.com (2015-03-18)

Thank you for your work and message!

### cl...@chromium.org (2015-05-17)

Bulk update: removing view restriction from closed bugs.

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

This issue was migrated from crbug.com/chromium/446164?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081119)*
