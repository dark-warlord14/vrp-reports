# Heap-use-after-free in WebCore::PopStateEvent::~PopStateEvent

| Field | Value |
|-------|-------|
| **Issue ID** | [40076611](https://issues.chromium.org/issues/40076611) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink, Blink>SVG |
| **Reporter** | at...@gmail.com |
| **Assignee** | sc...@chromium.org |
| **Created** | 2012-11-23 |
| **Bounty** | $1,000.00 |

## Description


Tested on:

OS: Ubuntu 12.04 x86_64
Chromium: ASAN 25.0.1332.0 (Developer Build 169130)

repro-file as attachment.

You need to load the attached SVG-file into a img-tag with html-file

html-file:

<html>
<img src='chrome-use-after-free-25d45.svg'></img>
</html>



ASAN-report:

==9498== ERROR: AddressSanitizer: heap-use-after-free on address 0x7f17355b99e0 at pc 0x7f1768a34d16 bp 0x7fffb1bee1f0 sp 0x7fffb1bee1e8
READ of size 4 at 0x7f17355b99e0 thread T0
    #0 0x7f1768a34d15 in WebCore::PopStateEvent::~PopStateEvent() ???:0
    #1 0x7f176860c572 in WebCore::SVGRenderSupport::layoutChildren(WebCore::RenderObject*, bool) ???:0
    #2 0x7f17687f48a9 in WebCore::RenderSVGContainer::layout() ???:0
    #3 0x7f176860c776 in WebCore::SVGRenderSupport::layoutChildren(WebCore::RenderObject*, bool) ???:0
    #4 0x7f17687f48a9 in WebCore::RenderSVGContainer::layout() ???:0
    #5 0x7f176860c776 in WebCore::SVGRenderSupport::layoutChildren(WebCore::RenderObject*, bool) ???:0
    #6 0x7f17687f48a9 in WebCore::RenderSVGContainer::layout() ???:0
    #7 0x7f176860c776 in WebCore::SVGRenderSupport::layoutChildren(WebCore::RenderObject*, bool) ???:0
    #8 0x7f17686037d7 in WebCore::RenderSVGRoot::layout() ???:0
    #9 0x7f176bca34fc in WebCore::RenderBlock::layoutBlockChild(WebCore::RenderBox*, WebCore::RenderBlock::MarginInfo&, WebCore::LayoutUnit&, WebCore::LayoutUnit&) ???:0
.
.
.
freed by thread T0 here:
    #0 0x7f176de88860 in __interceptor_free ??:0
    #1 0x7f17687731ca in WebCore::SVGTextContentElement::~SVGTextContentElement() ???:0
    #2 0x7f176cdea6ed in WebCore::SVGTextElement::~SVGTextElement() ???:0
    #3 0x7f1768648b7a in WebCore::SVGElementInstance::detach() ???:0
    #4 0x7f1768704304 in WebCore::SVGUseElement::clearResourceReferences() ???:0
    #5 0x7f176870654c in WebCore::SVGUseElement::buildPendingResource() ???:0
    #6 0x7f1768706053 in WebCore::SVGUseElement::svgAttributeChanged(WebCore::QualifiedName const&) ???:0
    #7 0x7f1768899c76 in WebCore::notifyTargetAndInstancesAboutAnimValChange(WebCore::SVGElement*, WebCore::QualifiedName const&) ../../third_party/WebKit/Source/WebCore/svg/SVGAnimateElement.cpp:0
.
.
.


## Attachments

- [chrome-use-after-free-25d45.svg](attachments/chrome-use-after-free-25d45.svg) (image/svg+xml; charset=us-ascii, 755 B)
- [Global-buffer-overflow.svg](attachments/Global-buffer-overflow.svg) (image/svg+xml; charset=us-ascii, 647 B)

## Timeline

### at...@gmail.com (2012-11-23)

Altered version of the same repro-file causes a global-buffer-overflow. repro-file as attachment. This file also causes a crash only when loaded into a img-tag.

ASAN-report:

==9679== ERROR: AddressSanitizer: global-buffer-overflow on address 0x7fd42e4a59f0 at pc 0x7fd42542facd bp 0x7fffbf9caf70 sp 0x7fffbf9caf68
READ of size 8 at 0x7fd42e4a59f0 thread T0
    #0 0x7fd42542facc in WebCore::SVGRenderSupport::layoutChildren(WebCore::RenderObject*, bool) ???:0
    #1 0x7fd4256178a9 in WebCore::RenderSVGContainer::layout() ???:0
    #2 0x7fd42542f776 in WebCore::SVGRenderSupport::layoutChildren(WebCore::RenderObject*, bool) ???:0
    #3 0x7fd4256178a9 in WebCore::RenderSVGContainer::layout() ???:0
    #4 0x7fd42542f776 in WebCore::SVGRenderSupport::layoutChildren(WebCore::RenderObject*, bool) ???:0
    #5 0x7fd4256178a9 in WebCore::RenderSVGContainer::layout() ???:0
    #6 0x7fd42542f776 in WebCore::SVGRenderSupport::layoutChildren(WebCore::RenderObject*, bool) ???:0
    #7 0x7fd4254267d7 in WebCore::RenderSVGRoot::layout() ???:0
    #8 0x7fd428ac64fc in WebCore::RenderBlock::layoutBlockChild(WebCore::RenderBox*, WebCore::RenderBlock::MarginInfo&, WebCore::LayoutUnit&, WebCore::LayoutUnit&) ???:0
.
.
.


### sc...@gmail.com (2012-11-24)

I confirm similar stack traces on a trunk ASAN build.

For some reason, ASAN isn't seeing a UAF for me in a Debug build; it's hitting a wild address:

==24799== ERROR: AddressSanitizer: SEGV on unknown address 0x000700000034 (pc 0x7ff6b04019dc sp 0x7fff78ae1280 bp 0x7fff78ae13d0 T0)
AddressSanitizer can not provide additional info.
    #0 0x7ff6b04019db in WTF::ThreadRestrictionVerifier::isSafeToUse() const out/Debug/../../third_party/WebKit/Source/WTF/wtf/ThreadRestrictionVerifier.h:123
    #1 0x7ff6b0400f70 in WTF::RefCountedBase::derefBase() out/Debug/../../third_party/WebKit/Source/WTF/wtf/RefCounted.h:142
    #2 0x7ff6ba63f9c2 in WTF::RefCounted<WebCore::History>::deref() out/Debug/../../third_party/WebKit/Source/WTF/wtf/RefCounted.h:201
    #3 0x7ff6ba63f88b in void WTF::derefIfNotNull<WebCore::History>(WebCore::History*) out/Debug/../../third_party/WebKit/Source/WTF/wtf/PassRefPtr.h:53
    #4 0x7ff6ba656c3b in ~RefPtr out/Debug/../../third_party/WebKit/Source/WTF/wtf/RefPtr.h:56
    #5 0x7ff6ba6298b6 in ~RefPtr out/Debug/../../third_party/WebKit/Source/WTF/wtf/RefPtr.h:56
    #6 0x7ff6bcf294c6 in ~PopStateEvent out/Debug/../../third_party/WebKit/Source/WebCore/dom/PopStateEvent.cpp:64
    #7 0x7ff6bcf2933f in ~PopStateEvent out/Debug/../../third_party/WebKit/Source/WebCore/dom/PopStateEvent.cpp:63
    #8 0x7ff6bbe2f309 in WebCore::SVGRenderSupport::layoutChildren(WebCore::RenderObject*, bool) out/Debug/../../third_party/WebKit/Source/WebCore/rendering/svg/SVGRenderSupport.cpp:250
    #9 0x7ff6bc4e6362 in WebCore::RenderSVGContainer::layout() out/Debug/../../third_party/WebKit/Source/WebCore/rendering/svg/RenderSVGContainer.cpp:71
...

### sc...@gmail.com (2012-11-24)

@attekett: ClusterFuzz doesn't seem to reproduce this for me (I think I uploaded a .zip of the two files correctly....) and I'm not near my desktop, so I'll be lazy and ask you: does this affect M23 stable / M24 beta?

### sc...@gmail.com (2012-11-24)

@schenney: would you or one of the other SVG experts mind taking this on?

### at...@gmail.com (2012-11-24)

@scarybeasts: The SVG-files didn't have any effect on asan-linux-stable-23.0.1271.64, but on asan-linux-beta-24.0.1312.5 file chrome-use-after-free-25d45.svg loaded via the html-file caused a tab crash. I donwnloaded the builds from https://commondatastorage.googleapis.com/chromium-browser-asan/index.html

ASAN-report:

ASAN:SIGSEGV
=================================================================
==3125== ERROR: AddressSanitizer crashed on unknown address 0x000000000000 (pc 0x000000000000 sp 0x7fff78fcd218 bp 0x7fff78fcd390 T0)
AddressSanitizer can not provide additional info.
Stats: 36M malloced (19M for red zones) by 23940 calls
Stats: 0M realloced by 63 calls
Stats: 24M freed by 13957 calls
Stats: 0M really freed by 0 calls
Stats: 58M (15006 full pages) mmaped in 43 calls
  mmaps   by size class: 7:20475; 8:4094; 9:1023; 10:2044; 11:255; 12:128; 13:128; 14:128; 15:48; 16:80; 17:8; 18:2; 19:1; 22:2; 23:4; 
  mallocs by size class: 7:17946; 8:2968; 9:541; 10:1932; 11:157; 12:79; 13:84; 14:105; 15:35; 16:80; 17:5; 18:1; 19:1; 22:2; 23:4; 
  frees   by size class: 7:9616; 8:1839; 9:299; 10:1822; 11:69; 12:36; 13:69; 14:95; 15:29; 16:74; 17:3; 18:1; 19:1; 22:2; 23:2; 
  rfrees  by size class: 
Stats: malloc large: 128 small slow: 267
==3125== ABORTING

### sc...@gmail.com (2012-11-24)

Marking as release blocker since it seems to be a M24 security regression.

### sc...@chromium.org (2012-11-26)

I'm on it.

### sc...@chromium.org (2012-11-26)

[Empty comment from Monorail migration]

### sc...@chromium.org (2012-11-26)

The global-buffer-override version will crash but not assert in a regular build. Something is using a <text> element while it is being deleted.


### sc...@chromium.org (2012-12-01)

Stopped crashing between Tuesday and today (Friday). No idea why but I'll have to try Asan before deciding the problem has gone away.

The issue is that layout is occurring during destruction of the use element's shadow tree, which is calling layout on the shadow tree when the element that it refers to has already been destroyed. Very odd, really, and I need to track down the cause of the layout as it seems silly to lay out something that is being removed.

### sc...@chromium.org (2012-12-03)

Still crashes an Asan build. So I'm still on it.

### sc...@chromium.org (2012-12-04)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-12-05)

This code SVGImageCache::imageContentChanged hasnt changed for a while, so m23 should be affected.

### in...@chromium.org (2012-12-05)

This code SVGImageCache::imageContentChanged hasnt changed for a while, so m23 should be affected.

### in...@chromium.org (2012-12-05)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-12-06)

http://trac.webkit.org/changeset/136845

SVG team rocks big time!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

### sc...@gmail.com (2012-12-12)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-12-13)

M24: http://trac.webkit.org/changeset/137675

### sc...@gmail.com (2012-12-18)

[Empty comment from Monorail migration]

### js...@chromium.org (2012-12-20)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-12-26)

@attekett: Enjoy your New Year with a $1000 Chromium Security Reward! Thanks!

### at...@gmail.com (2012-12-26)

@scarybeasts: Thanks! I will enjoy this even more because I had sorted this bug into Duplicates section and didn't even remember it was reward-topanel. :D

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

This issue was migrated from crbug.com/chromium/162494?no_tracker_redirect=1

[Multiple monorail components: Blink, Blink>SVG]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40076611)*
