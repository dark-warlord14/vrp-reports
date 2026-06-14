# Heap-use-after-free in blink::Node::setNeedsStyleRecalc

| Field | Value |
|-------|-------|
| **Issue ID** | [40080776](https://issues.chromium.org/issues/40080776) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Reporter** | at...@gmail.com |
| **Assignee** | pd...@chromium.org |
| **Created** | 2014-11-03 |
| **Bounty** | $2,000.00 |

## Description


Tested on:

OS: Ubuntu 14.04

Chromium: 40.0.2209.0 (Developer Build) 
Revision: 09df15868941e7489acff767e00864769ca6338b-refs/heads/master@{#302420}




ASAN-trace:

==21900==ERROR: AddressSanitizer: heap-use-after-free on address 0x60b000013ea8 at pc 0x7fb419393770 bp 0x7ffff565d270 sp 0x7ffff565d268
READ of size 4 at 0x60b000013ea8 thread T0 (chrome)
    #0 0x7fb41939376f in getFlag /home/attekett/chrome/src/out/Release/../../third_party/WebKit/Source/core/dom/Node.h:722:42
    #1 0x7fb41939376f in inDocument /home/attekett/chrome/src/out/Release/../../third_party/WebKit/Source/core/dom/Node.h:466:0
    #2 0x7fb41939376f in inActiveDocument /home/attekett/chrome/src/out/Release/../../third_party/WebKit/Source/core/dom/Node.cpp:742:0
    #3 0x7fb41939376f in blink::Node::setNeedsStyleRecalc(blink::StyleChangeType, blink::StyleChangeReasonForTracing const&) /home/attekett/chrome/src/out/Release/../../third_party/WebKit/Source/core/dom/Node.cpp:710:0
    #4 0x7fb4192b1731 in blink::Document::dirtyElementsForLayerUpdate() /home/attekett/chrome/src/out/Release/../../third_party/WebKit/Source/core/dom/Document.cpp:2062:9
    #5 0x7fb4192b0d65 in blink::Document::updateStyle(blink::StyleRecalcChange) /home/attekett/chrome/src/out/Release/../../third_party/WebKit/Source/core/dom/Document.cpp:1869:9
    #6 0x7fb4192af9b8 in blink::Document::updateRenderTree(blink::StyleRecalcChange) /home/attekett/chrome/src/out/Release/../../third_party/WebKit/Source/core/dom/Document.cpp:1814:5
.
.
.
0x60b000013ea8 is located 24 bytes inside of 104-byte region [0x60b000013e90,0x60b000013ef8)
freed by thread T0 (chrome) here:
    #0 0x7fb41520874b in __interceptor_free ??:0:0
    #1 0x7fb419869571 in deref /home/attekett/chrome/src/out/Release/../../third_party/WebKit/Source/core/dom/TreeShared.h:82:13
    #2 0x7fb419869571 in derefIfNotNull<blink::ContainerNode> /home/attekett/chrome/src/out/Release/../../third_party/WebKit/Source/wtf/PassRefPtr.h:57:0
    #3 0x7fb419869571 in ~RefPtr /home/attekett/chrome/src/out/Release/../../third_party/WebKit/Source/wtf/RefPtr.h:57:0
    #4 0x7fb419869571 in blink::HTMLStackItem::~HTMLStackItem() /home/attekett/chrome/src/out/Release/../../third_party/WebKit/Source/core/html/parser/HTMLStackItem.h:43:0
    #5 0x7fb41998ed00 in deref /home/attekett/chrome/src/out/Release/../../third_party/WebKit/Source/wtf/RefCounted.h:172:13
.
.
.


## Attachments

- [chrome-heap-use-after-free-blinkNodegetFlag.html](attachments/chrome-heap-use-after-free-blinkNodegetFlag.html) (text/html, 626 B)

## Timeline

### cl...@chromium.org (2014-11-03)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5746675279724544

### cl...@chromium.org (2014-11-03)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-11-03)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5746675279724544

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x60f000013d78
Crash State:
  blink::Node::setNeedsStyleRecalc
  blink::Document::dirtyElementsForLayerUpdate
  blink::Document::updateStyle
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=259056:259494

Minimized Testcase (0.28 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv965yEVghIqky8O5ZajH4AhsEpvRbzm3NYu4S3685_62tKGiPhHTRw6lF-Q1J-HP4mKG7lg_l0bzGkV7z6GFTG-QHyFUfAxdfTGDl9V4tO5tYWo1zdVDXHsoKLL6uLHXGXIwzzsyW3YeGtHwRX_E2ydG4-HiSQ
<body" id="I0">
 <div style="-webkit-filter: url('#filter');">
 
 <div style="-webkit-filter: url('#filter');">
 </div>
 
 <svg>
 <filter id="filter">
 
 <feFlood>
 
<script> 
var test2=document.getElementById("I0")
document.execCommand("JustifyRight", false)
test2.innerHTML=''
</script>




### in...@chromium.org (2014-11-03)

Author: esprehn@chromium.org 
Component: blink
Changelist: https://chromium.googlesource.com/chromium/blink.git/+/896a93c12fb190aaeee1304a0eed7f56c43e7a9b
Time: Mon Mar 24 23:59:28 2014
Files Node.cpp, Document.cpp are changed in this cl (and is part of stack frame #2, "blink::Node::setNeedsStyleRecalc")
Minimum distance from crash line to modified line: 8. (file: Document.cpp, crashed on: 1811, modified: 1803).

Author: esprehn@chromium.org 
Component: blink
Changelist: https://chromium.googlesource.com/chromium/blink.git/+/d1cfe6fda95077a0c5c6565c05b9c407eb5059c2
Time: Tue Mar 25 05:34:24 2014
File Document.cpp is changed in this cl (and is part of stack frame #4, "blink::Document::updateStyle"; frame #5, "blink::Document::updateRenderTree"; frame #6, "blink::Document::finishedParsing")
Minimum distance from crash line to modified line: 1103. (file: Document.cpp, crashed on: 1811, modified: 708).

### in...@chromium.org (2014-11-03)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-11-03)

[Empty comment from Monorail migration]

### oj...@chromium.org (2014-11-03)

[Empty comment from Monorail migration]

### es...@chromium.org (2014-11-04)

We should unschedule the layer update hack when we get ::detach()'ed, maybe some SVG code is not doing that properly?

https://code.google.com/p/chromium/codesearch#chromium/src/third_party/WebKit/Source/core/dom/Element.cpp&q=unscheduleSVGFilterLayerUpdateHack&sq=package:chromium&l=1371&type=cs

Or maybe someone is scheduling an update when already detached, and then we get removed from the DOM and it never happens?

I'm not currently fixing bugs in Blink though, pdr@ want to take a look? Short term you could just make these things RefPtr on Document.

### cl...@chromium.org (2014-11-08)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-11-11)

pdr@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-11-18)

pdr@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### bu...@chromium.org (2014-11-20)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=185670

------------------------------------------------------------------
r185670 | pdr@chromium.org | 2014-11-20T15:26:53.065056Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/svg/filters/filter-detach-crash-expected.txt?r1=185670&r2=185669&pathrev=185670
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/dom/Element.cpp?r1=185670&r2=185669&pathrev=185670
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/svg/filters/filter-detach-crash.html?r1=185670&r2=185669&pathrev=185670

Unschedule the SVG filter layer update hack after detaching children

This patch fixes a crash where an element is scheduled for an update
while being detached.

When an element is being detached it would clear the update flag then
detach its children. This is problematic because children can set the
update flag on elements during detach (which is expected). If a child
sets an element as needing an update while that element is being
detached, we'll end up with a detached element that needs a filter update
which can make Document::dirtyElementsForLayerUpdate angry.

When scheduling, we check that an element does not need an attach
(which would handle the filter layer update) before actually scheduling.
This patch moves unscheduling after the element is in a needsAttach state.

Looking forward to removing this hack entirely..

R=esprehn
BUG=429666

Review URL: https://codereview.chromium.org/742693002
-----------------------------------------------------------------

### in...@chromium.org (2014-11-21)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-11-21)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-11-21)

ClusterFuzz has detected this issue as fixed in range 304972:305118.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5746675279724544

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x60f000013d78
Crash State:
  blink::Node::setNeedsStyleRecalc
  blink::Document::dirtyElementsForLayerUpdate
  blink::Document::updateStyle
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=259056:259494
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=304972:305118

Minimized Testcase (0.28 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv965yEVghIqky8O5ZajH4AhsEpvRbzm3NYu4S3685_62tKGiPhHTRw6lF-Q1J-HP4mKG7lg_l0bzGkV7z6GFTG-QHyFUfAxdfTGDl9V4tO5tYWo1zdVDXHsoKLL6uLHXGXIwzzsyW3YeGtHwRX_E2ydG4-HiSQ
<body" id="I0">
 <div style="-webkit-filter: url('#filter');">
 
 <div style="-webkit-filter: url('#filter');">
 </div>
 
 <svg>
 <filter id="filter">
 
 <feFlood>
 
<script> 
var test2=document.getElementById("I0")
document.execCommand("JustifyRight", false)
test2.innerHTML=''
</script>

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### in...@chromium.org (2014-12-15)

[Empty comment from Monorail migration]

### ma...@google.com (2014-12-15)

Approved for M40 (branch: 2214)

### at...@gmail.com (2014-12-15)

Should this issue have reward-topanel?

### in...@chromium.org (2014-12-15)

Yes Sir! I was just triaging bugs today, would have added it anyway :)

### pd...@chromium.org (2014-12-15)

Merged in r187178! Thanks for flying pdr airlines.

### bu...@chromium.org (2014-12-15)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=187178

------------------------------------------------------------------
r187178 | pdr@chromium.org | 2014-12-15T21:14:00.271786Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/branches/chromium/2214/Source/core/dom/Element.cpp?r1=187178&r2=187177&pathrev=187178
   A http://src.chromium.org/viewvc/blink/branches/chromium/2214/LayoutTests/svg/filters/filter-detach-crash.html?r1=187178&r2=187177&pathrev=187178
   A http://src.chromium.org/viewvc/blink/branches/chromium/2214/LayoutTests/svg/filters/filter-detach-crash-expected.txt?r1=187178&r2=187177&pathrev=187178

Merge 185670 "Unschedule the SVG filter layer update hack after ..."

> Unschedule the SVG filter layer update hack after detaching children
> 
> This patch fixes a crash where an element is scheduled for an update
> while being detached.
> 
> When an element is being detached it would clear the update flag then
> detach its children. This is problematic because children can set the
> update flag on elements during detach (which is expected). If a child
> sets an element as needing an update while that element is being
> detached, we'll end up with a detached element that needs a filter update
> which can make Document::dirtyElementsForLayerUpdate angry.
> 
> When scheduling, we check that an element does not need an attach
> (which would handle the filter layer update) before actually scheduling.
> This patch moves unscheduling after the element is in a needsAttach state.
> 
> Looking forward to removing this hack entirely..
> 
> R=esprehn
> BUG=429666
> 
> Review URL: https://codereview.chromium.org/742693002

TBR=pdr@chromium.org

Review URL: https://codereview.chromium.org/806793003
-----------------------------------------------------------------

### in...@chromium.org (2014-12-15)

It was a very pleasant experience flying with pdr airlines. will fly again :)

### ti...@google.com (2015-01-22)

Congrats - $2000 for this report. Notes from reward panel: "In partition, no control between use and free".

### cl...@chromium.org (2015-02-27)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2015-03-09)

[Empty comment from Monorail migration]

### ti...@google.com (2015-04-15)

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

This issue was migrated from crbug.com/chromium/429666?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080776)*
