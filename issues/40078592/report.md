# ASSERTION FAILED: m_stateStack.size() == 1, Heap-use-after-free in WebCore::ScrollView::paint

| Field | Value |
|-------|-------|
| **Issue ID** | [40078592](https://issues.chromium.org/issues/40078592) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Layout, Blink>SVG |
| **Reporter** | at...@gmail.com |
| **Assignee** | sc...@chromium.org |
| **Created** | 2013-12-21 |
| **Bounty** | $1,000.00 |

## Description



Tested on:

OS: Ubuntu 12.04

Chromium: ASAN 33.0.1738.0 (Developer Build 240534)


Repro-file as attachment. 

Note: The file content is actually a SVG-file, but you have to have file-extension .html to reproduce the issue. If you rename the file with .svg extension Chrome only reports syntax-error when the file is opened.

ASAN-report:

==8060==ERROR: AddressSanitizer: heap-use-after-free on address 0x616000067280 at pc 0x7fc6fabe5872 bp 0x7fffa6cdeb40 sp 0x7fffa6cdeb38
READ of size 8 at 0x616000067280 thread T0 (chrome)
    #0 0x7fc6fabe5871 in WebCore::GraphicsContext::paintingDisabled() const /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/platform/graphics/GraphicsContext.h:88:0
    #1 0x7fc6fb055ea2 in WebCore::ScrollView::paint(WebCore::GraphicsContext*, WebCore::IntRect const&) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/platform/scroll/ScrollView.cpp:878:0
    #2 0x7fc6fca198b6 in WebCore::SVGImage::draw(WebCore::GraphicsContext*, WebCore::FloatRect const&, WebCore::FloatRect const&, WebCore::CompositeOperator, blink::WebBlendMode) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/svg/graphics/SVGImage.cpp:264:0
    #3 0x7fc6fafa68d1 in WebCore::GraphicsContext::drawImage(WebCore::Image*, WebCore::FloatRect const&, WebCore::FloatRect const&, WebCore::CompositeOperator, blink::WebBlendMode, WebCore::RespectImageOrientationEnum, bool) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/platform/graphics/GraphicsContext.cpp:1107:0
    #4 0x7fc6fafa658b in WebCore::GraphicsContext::drawImage(WebCore::Image*, WebCore::FloatRect const&, WebCore::FloatRect const&, WebCore::CompositeOperator, WebCore::RespectImageOrientationEnum, bool) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/platform/graphics/GraphicsContext.cpp:1086:0
    #5 0x7fc6fca337d1 in WebCore::RenderSVGImage::paintForeground(WebCore::PaintInfo&) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/rendering/svg/RenderSVGImage.cpp:171:0
.
.
.
0x616000067280 is located 0 bytes inside of 592-byte region [0x616000067280,0x6160000674d0)
freed by thread T0 (chrome) here:
    #0 0x7fc6f7a3bbe9 in __interceptor_free _asan_rtl_:0
    #1 0x7fc6fafdd9a1 in WTF::OwnPtr<WebCore::GraphicsContext>::~OwnPtr() /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/wtf/OwnPtr.h:62:0
    #2 0x7fc6fafd9411 in WebCore::ImageBuffer::~ImageBuffer() /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/platform/graphics/ImageBuffer.cpp:87:0
    #3 0x7fc6fafabd65 in WTF::OwnedPtrDeleter<WebCore::ImageBuffer>::deletePtr(WebCore::ImageBuffer*) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/wtf/OwnPtrCommon.h:52:0
    #4 0x7fc6fca33e26 in WebCore::RenderSVGImage::imageChanged(void*, WebCore::IntRect const*) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/rendering/svg/RenderSVGImage.cpp:219:0
    #5 0x7fc6fbebe90a in WebCore::ImageResource::notifyObservers(WebCore::IntRect const*) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/fetch/ImageResource.cpp:270:0
.
.
.


## Attachments

- [chrome-heap-use-after-free-WebCoreGraphicsContextpaintingDisabled10-min.html](attachments/chrome-heap-use-after-free-WebCoreGraphicsContextpaintingDisabled10-min.html) (text/html, 501 B)

## Timeline

### cl...@chromium.org (2013-12-21)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-12-23)

ClusterFuzz is analyzing your testcase. See https://cluster-fuzz.appspot.com/testcase?key=6483245877166080

### cl...@chromium.org (2013-12-23)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6483245877166080

Uploader: meacer@chromium.org
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x616000008480
Crash State:
  - crash stack -
  WebCore::ScrollView::paint
  WebCore::SVGImage::draw
  - free stack -
  WebCore::ImageBuffer::~ImageBuffer
  WebCore::RenderSVGImage::imageChanged
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=238209:238239

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv95y_euLk8Iszqv05cgfH9hKSc3vHXh-8ukMck0YFQFBQB2dPgMQVo78EZNM0424q3AVU-uddkN-Tr_rxPLoEQypORohfwhm0kpsDPqHI03aQfqJng8ev93E8aeNNWDqDKGCNTdnnK3cp3r9881t6c3X8TCWiQ



### cl...@chromium.org (2013-12-23)

[Empty comment from Monorail migration]

### me...@chromium.org (2013-12-24)

[Empty comment from Monorail migration]

### me...@chromium.org (2013-12-24)

@schenney: Could you take a look or find an owner? Thanks.

### me...@chromium.org (2013-12-24)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-12-24)

This medium+ severity security issue is a regression on trunk.

Please fix this asap. If you are unable to look into this soon, please revert your change.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-01-01)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6483245877166080

Uploader: meacer@chromium.org
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x616000008480
Crash State:
  - crash stack -
  WebCore::ScrollView::paint
  WebCore::SVGImage::draw
  - free stack -
  WebCore::ImageBuffer::~ImageBuffer
  WebCore::RenderSVGImage::imageChanged
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=238209:238239

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv95y_euLk8Iszqv05cgfH9hKSc3vHXh-8ukMck0YFQFBQB2dPgMQVo78EZNM0424q3AVU-uddkN-Tr_rxPLoEQypORohfwhm0kpsDPqHI03aQfqJng8ev93E8aeNNWDqDKGCNTdnnK3cp3r9881t6c3X8TCWiQ



### cl...@chromium.org (2014-01-01)

schenney@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-01-06)

ClusterFuzz is analyzing your testcase. See https://cluster-fuzz.appspot.com/testcase?key=4527480241127424

### in...@chromium.org (2014-01-06)

The last report was upload on windows jobs to see if we can get any better regression range.

### in...@chromium.org (2014-01-06)

As per https://cluster-fuzz.appspot.com/testcase?key=4527480241127424, this bug is old.

### sc...@chromium.org (2014-01-06)

Patch is up. It's probably due to pdr's patch to enable buffered rendering of SVG images. It's a simple fix but I need his review. https://codereview.chromium.org/109753004/

### in...@chromium.org (2014-01-06)

Thanks Stephen. Adding WIP, so that you don't get any more nags.

### cl...@chromium.org (2014-01-06)

[Empty comment from Monorail migration]

### bu...@chromium.org (2014-01-07)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=164536

------------------------------------------------------------------------
r164536 | schenney@chromium.org | 2014-01-07T00:39:12.598162Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/svg/as-image/zero-size-buffered-image-nopaint-expected.html?r1=164536&r2=164535&pathrev=164536
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/svg/as-image/zero-size-buffered-image-nopaint.html?r1=164536&r2=164535&pathrev=164536
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/rendering/svg/RenderSVGImage.cpp?r1=164536&r2=164535&pathrev=164536

Avoid drawing SVG image content when the image is of zero size.

R=pdr
BUG=330420

Review URL: https://codereview.chromium.org/109753004
------------------------------------------------------------------------

### be...@chromium.org (2014-01-07)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-01-07)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-01-08)

[Empty comment from Monorail migration]

### bu...@chromium.org (2014-01-08)

Is there a merge required here?

### sc...@chromium.org (2014-01-08)

Yes

### in...@chromium.org (2014-01-08)

In future, for security bugs, you can wait for CF sheriffbot to update bug. It will automatically put all the milestone labels and Merge-Triage. Basically we want to make sure all milestone labels exist, and also fix gets some bake time. 

### la...@google.com (2014-01-08)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-01-08)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-01-09)

ClusterFuzz has detected this issue as fixed in range 243511:243516.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6483245877166080

Uploader: meacer@chromium.org
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x616000008480
Crash State:
  - crash stack -
  WebCore::ScrollView::paint
  WebCore::SVGImage::draw
  - free stack -
  WebCore::ImageBuffer::~ImageBuffer
  WebCore::RenderSVGImage::imageChanged
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=238209:238239
Fixed: https://cluster-fuzz.appspot.com/revisions?range=243511:243516

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv95y_euLk8Iszqv05cgfH9hKSc3vHXh-8ukMck0YFQFBQB2dPgMQVo78EZNM0424q3AVU-uddkN-Tr_rxPLoEQypORohfwhm0kpsDPqHI03aQfqJng8ev93E8aeNNWDqDKGCNTdnnK3cp3r9881t6c3X8TCWiQ

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### bu...@chromium.org (2014-01-09)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=164792

------------------------------------------------------------------------
r164792 | schenney@chromium.org | 2014-01-09T18:23:27.050921Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/branches/chromium/1750/LayoutTests/svg/as-image/zero-size-buffered-image-nopaint-expected.html?r1=164792&r2=164791&pathrev=164792
   A http://src.chromium.org/viewvc/blink/branches/chromium/1750/LayoutTests/svg/as-image/zero-size-buffered-image-nopaint.html?r1=164792&r2=164791&pathrev=164792
   M http://src.chromium.org/viewvc/blink/branches/chromium/1750/Source/core/rendering/svg/RenderSVGImage.cpp?r1=164792&r2=164791&pathrev=164792

Merge 164536 "Avoid drawing SVG image content when the image is ..."

> Avoid drawing SVG image content when the image is of zero size.
> 
> R=pdr
> BUG=330420
> 
> Review URL: https://codereview.chromium.org/109753004

TBR=schenney@chromium.org

Review URL: https://codereview.chromium.org/131973005
------------------------------------------------------------------------

### dh...@google.com (2014-01-16)

Requesting merge for M32.

### in...@chromium.org (2014-01-16)

[Empty comment from Monorail migration]

### ka...@google.com (2014-01-17)

[Empty comment from Monorail migration]

### bu...@chromium.org (2014-01-17)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=165329

------------------------------------------------------------------------
r165329 | schenney@chromium.org | 2014-01-17T19:52:26.401086Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/branches/chromium/1700/Source/core/rendering/svg/RenderSVGImage.cpp?r1=165329&r2=165328&pathrev=165329
   A http://src.chromium.org/viewvc/blink/branches/chromium/1700/LayoutTests/svg/as-image/zero-size-buffered-image-nopaint-expected.html?r1=165329&r2=165328&pathrev=165329
   A http://src.chromium.org/viewvc/blink/branches/chromium/1700/LayoutTests/svg/as-image/zero-size-buffered-image-nopaint.html?r1=165329&r2=165328&pathrev=165329

Merge 164536 "Avoid drawing SVG image content when the image is ..."

> Avoid drawing SVG image content when the image is of zero size.
> 
> R=pdr
> BUG=330420
> 
> Review URL: https://codereview.chromium.org/109753004

TBR=schenney@chromium.org

Review URL: https://codereview.chromium.org/140783011
------------------------------------------------------------------------

### dh...@google.com (2014-01-22)

[Empty comment from Monorail migration]

### dh...@google.com (2014-01-22)

[Empty comment from Monorail migration]

### dh...@google.com (2014-01-23)

[Empty comment from Monorail migration]

### mb...@chromium.org (2014-01-27)

Thanks for the report! This one qualifies for a $1000 reward. It does not seem like there is control between the free and use in this case.

### ti...@chromium.org (2014-02-28)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-03-17)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-04-14)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-04-16)

Bulk update: removing view restriction from closed bugs.

### la...@google.com (2015-01-09)

Migrate from Cr-Blink-Rendering to Cr-Blink-Layout

### cl...@chromium.org (2016-02-02)

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

This issue was migrated from crbug.com/chromium/330420?no_tracker_redirect=1

[Multiple monorail components: Blink>Layout, Blink>SVG]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40078592)*
