# Heap-use-after-free in blink::ShapeOutsideInfo::isEnabledFor

| Field | Value |
|-------|-------|
| **Issue ID** | [40081071](https://issues.chromium.org/issues/40081071) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Reporter** | at...@gmail.com |
| **Assignee** | ro...@chromium.org |
| **Created** | 2014-12-28 |
| **Bounty** | $2,000.00 |

## Description



Tested on:

OS: Ubuntu 14.04

Chromium	41.0.2258.0 (Developer Build) 
Revision	e83f28ca816694be553baed069f784eb286d8170-refs/heads/master@{#309428}


ASAN-trace:

==19141==ERROR: AddressSanitizer: heap-use-after-free on address 0x61100006a1c8 at pc 0x7f17aefa0627 bp 0x7fffe5362090 sp 0x7fffe5362088
READ of size 8 at 0x61100006a1c8 thread T0 (chrome)
    #0 0x7f17aefa0626 in get /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/wtf/RefPtr.h:57:40
    #1 0x7f17aefa0626 in blink::RenderObject::style() const /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/rendering/RenderObject.h:799:0
    #2 0x7f17b02d2b1f in blink::ShapeOutsideInfo::isEnabledFor(blink::RenderBox const&) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/rendering/shapes/ShapeOutsideInfo.cpp:264:30
    #3 0x7f17afb1bcca in blink::RenderBox::shapeOutsideInfo() const /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/rendering/RenderBox.h:668:16
    #4 0x7f17b032e77a in blink::ComputeFloatOffsetForLineLayoutAdapter<(blink::FloatingObject::Type)2>::updateOffsetIfNeeded(blink::FloatingObject const&) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/rendering/FloatingObjects.cpp:506:42
    #5 0x7f17b032e27c in blink::ComputeFloatOffsetAdapter<(blink::FloatingObject::Type)2>::collectIfNeeded(blink::PODInterval<int, blink::FloatingObject*> const&) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/rendering/FloatingObjects.cpp:478:30
    #6 0x7f17b032df96 in void blink::PODIntervalTree<int, blink::FloatingObject*>::searchForOverlapsFrom<blink::ComputeFloatOffsetForLineLayoutAdapter<(blink::FloatingObject::Type)2> >(blink::PODRedBlackTree<blink::PODInterval<int, blink::FloatingObject*> >::Node*, blink::ComputeFloatOffsetForLineLayoutAdapter<(blink::FloatingObject::Type)2>&) const /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/platform/PODIntervalTree.h:175:9
    #7 0x7f17b032da34 in blink::FloatingObjects::logicalRightOffset(blink::LayoutUnit, blink::LayoutUnit, blink::LayoutUnit) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/rendering/FloatingObjects.cpp:407:5
    #8 0x7f17b0093637 in blink::RenderBlockFlow::logicalRightOffsetForLine(blink::LayoutUnit, blink::LayoutUnit, bool, blink::LayoutUnit) const /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/rendering/RenderBlockFlow.h:254:48
.
.
.
0x61100006a1c8 is located 8 bytes inside of 216-byte region [0x61100006a1c0,0x61100006a298)
freed by thread T0 (chrome) here:
    #0 0x7f17ab4e4b09 in __interceptor_free ??:0:0
    #1 0x7f17af1f4142 in blink::Node::detach(blink::Node::AttachContext const&) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/dom/Node.cpp:927:9
    #2 0x7f17af19bfdc in blink::Element::detach(blink::Node::AttachContext const&) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/dom/Element.cpp:1499:5
    #3 0x7f17af1f3f15 in blink::Node::reattach(blink::Node::AttachContext const&) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/dom/Node.cpp:891:9
    #4 0x7f17af19dc36 in blink::Element::recalcOwnStyle(blink::StyleRecalcChange) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/dom/Element.cpp:1656:9
    #5 0x7f17af19d6e0 in blink::Element::recalcStyle(blink::StyleRecalcChange, blink::Text*) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/dom/Element.cpp:1602:22
    #6 0x7f17af0efdf0 in blink::ContainerNode::recalcChildStyle(blink::StyleRecalcChange) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/dom/ContainerNode.cpp:1224:17
    #7 0x7f17af19d773 in blink::Element::recalcStyle(blink::StyleRecalcChange, blink::Text*) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/dom/Element.cpp:1617:13
    #8 0x7f17af0efdf0 in blink::ContainerNode::recalcChildStyle(blink::StyleRecalcChange) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/dom/ContainerNode.cpp:1224:17
.
.
.
previously allocated by thread T0 (chrome) here:
    #0 0x7f17ab4e4dc9 in __interceptor_malloc ??:0:0
    #1 0x7f17b01cff4a in partitionAlloc /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/wtf/PartitionAlloc.h:477:20
    #2 0x7f17b01cff4a in blink::RenderObject::operator new(unsigned long) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/rendering/RenderObject.cpp:148:0
    #3 0x7f17b01d01be in blink::RenderObject::createObject(blink::Element*, blink::RenderStyle*) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/rendering/RenderObject.cpp:188:9
    #4 0x7f17af2384b0 in blink::RenderTreeBuilderForElement::createRenderer() /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/dom/RenderTreeBuilder.cpp:120:33
    #5 0x7f17af19b4a3 in blink::Element::attach(blink::Node::AttachContext const&) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/dom/Element.cpp:1437:5
    #6 0x7f17af0eb911 in blink::ContainerNode::attachChildren(blink::Node::AttachContext const&) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/dom/ContainerNode.h:307:13
    #7 0x7f17af0eb7c1 in blink::ContainerNode::attach(blink::Node::AttachContext const&) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/dom/ContainerNode.cpp:825:5
    #8 0x7f17af19b4f1 in blink::Element::attach(blink::Node::AttachContext const&) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/dom/Element.cpp:1449:5
.
.
.

## Attachments

- [chrome-heap-use-after-free-blinkRenderObjectstyle.html](attachments/chrome-heap-use-after-free-blinkRenderObjectstyle.html) (text/html, 1.0 KB)

## Timeline

### cl...@chromium.org (2014-12-28)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=6613198835810304

### cl...@chromium.org (2014-12-29)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-12-29)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6613198835810304

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x612000057f88
Crash State:
  blink::ShapeOutsideInfo::isEnabledFor
  blink::ComputeFloatOffsetForLineLayoutAdapter<
  void blink::PODIntervalTree<int, blink::FloatingObject*>::searchForOverlaps
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=303684:303833

Minimized Testcase (0.86 Kb): https://cluster-fuzz.appspot.com/download/AMIfv97l7Vx-ktCZL7OvY8UZOEPlakpTlB8zy8fHHg-vXixTxQ9nZhLaBM8_5NmrnLEBx65kRkTEiX5goTCFJO-XaVw_RdlniTVK4gdXBjwJXvjixSf0n_-XbQCtpzJWLPkoKjbjoV6nPXV5CqQHS5evjaIjIPZmpQ



### rs...@chromium.org (2014-12-29)

Possible culprits:

https://chromium.googlesource.com/chromium/blink/+/bd11143b95729621b3041e301304e7939e64d7b8
https://chromium.googlesource.com/chromium/blink/+/fe3ae0fcf829b493207fb6f1ccbfa5e91d873bca

My guess is bd11143b95729621b3041e301304e7939e64d7b8.

### cl...@chromium.org (2014-12-29)

This medium+ severity security issue is a regression on trunk.

Please fix this asap. If you are unable to look into this soon, please revert your change.

- Your friendly ClusterFuzz

### ro...@chromium.org (2015-01-01)

[Empty comment from Monorail migration]

### bu...@chromium.org (2015-01-06)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=187935

------------------------------------------------------------------
r187935 | robhogan@gmail.com | 2015-01-06T21:33:30.556048Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/block/crash-when-element-becomes-positioned-and-doesnt-clear-floating-objects.html?r1=187935&r2=187934&pathrev=187935
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/block/crash-when-element-becomes-positioned-and-doesnt-clear-floating-objects-expected.txt?r1=187935&r2=187934&pathrev=187935
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/rendering/RenderHTMLCanvas.cpp?r1=187935&r2=187934&pathrev=187935

Don't check for layout in a canvas if it it's already needed

In this clusterfuzz test case a float is deleted but its entry in the floating
objects list of a sibling renderer is accessed before layout has had time to
remove reference to it. The read attempt pre-empts layout because the change in
zoom factor prompts the canvas renderer to recompute its width/height to check
if layout is required. If layout is already required this isn't necessary and,
what's more, if layout is already required it may be because renderer(s) in its
floating object list have been deleted and aren't safe to access while computing
offset as part of the width calculations.

So return early when the check for layout is unnecessary and may even crash.

BUG=445285

Review URL: https://codereview.chromium.org/828163002
-----------------------------------------------------------------

### aa...@google.com (2015-01-06)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-01-07)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

Your fix is very close to the branch point. After the branch happens, please make sure to check if your fix is in.

- Your friendly ClusterFuzz

### bu...@chromium.org (2015-01-07)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=187981

------------------------------------------------------------------
r187981 | junov@chromium.org | 2015-01-07T17:09:59.639276Z

Changed paths:
   D http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/block/crash-when-element-becomes-positioned-and-doesnt-clear-floating-objects.html?r1=187981&r2=187980&pathrev=187981
   D http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/block/crash-when-element-becomes-positioned-and-doesnt-clear-floating-objects-expected.txt?r1=187981&r2=187980&pathrev=187981
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/rendering/RenderHTMLCanvas.cpp?r1=187981&r2=187980&pathrev=187981

Revert of Don't check for layout in a canvas if it it's already needed (patchset #3 id:40001 of https://codereview.chromium.org/828163002/)

Reason for revert:
Speculative revert for crashes on WinXP bots. See crbug.com/446834
I will re-land if this does not fix the crashes.

Original issue's description:
> Don't check for layout in a canvas if it it's already needed
> 
> In this clusterfuzz test case a float is deleted but its entry in the floating
> objects list of a sibling renderer is accessed before layout has had time to
> remove reference to it. The read attempt pre-empts layout because the change in
> zoom factor prompts the canvas renderer to recompute its width/height to check
> if layout is required. If layout is already required this isn't necessary and,
> what's more, if layout is already required it may be because renderer(s) in its
> floating object list have been deleted and aren't safe to access while computing
> offset as part of the width calculations.
> 
> So return early when the check for layout is unnecessary and may even crash.
> 
> BUG=445285
> 
> Committed: https://src.chromium.org/viewvc/blink?view=rev&revision=187935

TBR=dsinclair@chromium.org,inferno@chromium.org,jchaffraix@chromium.org,jshin@chromium.org,pdr@chromium.org,robhogan@gmail.com
NOTREECHECKS=true
NOTRY=true
BUG=445285

Review URL: https://codereview.chromium.org/810943003
-----------------------------------------------------------------

### bu...@chromium.org (2015-01-07)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=187985

------------------------------------------------------------------
r187985 | junov@chromium.org | 2015-01-07T18:08:08.345253Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/block/crash-when-element-becomes-positioned-and-doesnt-clear-floating-objects-expected.txt?r1=187985&r2=187984&pathrev=187985
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/rendering/RenderHTMLCanvas.cpp?r1=187985&r2=187984&pathrev=187985
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/block/crash-when-element-becomes-positioned-and-doesnt-clear-floating-objects.html?r1=187985&r2=187984&pathrev=187985

Revert of Revert of Don't check for layout in a canvas if it it's already needed (patchset #1 id:1 of https://codereview.chromium.org/810943003/)

Reason for revert:
Speculative revert did not fix crbug.com/446834

Original issue's description:
> Revert of Don't check for layout in a canvas if it it's already needed (patchset #3 id:40001 of https://codereview.chromium.org/828163002/)
> 
> Reason for revert:
> Speculative revert for crashes on WinXP bots. See crbug.com/446834
> I will re-land if this does not fix the crashes.
> 
> Original issue's description:
> > Don't check for layout in a canvas if it it's already needed
> > 
> > In this clusterfuzz test case a float is deleted but its entry in the floating
> > objects list of a sibling renderer is accessed before layout has had time to
> > remove reference to it. The read attempt pre-empts layout because the change in
> > zoom factor prompts the canvas renderer to recompute its width/height to check
> > if layout is required. If layout is already required this isn't necessary and,
> > what's more, if layout is already required it may be because renderer(s) in its
> > floating object list have been deleted and aren't safe to access while computing
> > offset as part of the width calculations.
> > 
> > So return early when the check for layout is unnecessary and may even crash.
> > 
> > BUG=445285
> > 
> > Committed: https://src.chromium.org/viewvc/blink?view=rev&revision=187935
> 
> TBR=dsinclair@chromium.org,inferno@chromium.org,jchaffraix@chromium.org,jshin@chromium.org,pdr@chromium.org,robhogan@gmail.com
> NOTREECHECKS=true
> NOTRY=true
> BUG=445285
> 
> Committed: https://src.chromium.org/viewvc/blink?view=rev&revision=187981

TBR=dsinclair@chromium.org,inferno@chromium.org,jchaffraix@chromium.org,jshin@chromium.org,pdr@chromium.org,robhogan@gmail.com
NOTREECHECKS=true
NOTRY=true
BUG=445285

Review URL: https://codereview.chromium.org/837233002
-----------------------------------------------------------------

### cl...@chromium.org (2015-01-08)

ClusterFuzz has detected this issue as fixed in range 310098:310217.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6613198835810304

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x612000057f88
Crash State:
  blink::ShapeOutsideInfo::isEnabledFor
  blink::ComputeFloatOffsetForLineLayoutAdapter<
  void blink::PODIntervalTree<int, blink::FloatingObject*>::searchForOverlaps
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=303684:303833
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=310098:310217

Minimized Testcase (0.86 Kb): https://cluster-fuzz.appspot.com/download/AMIfv97l7Vx-ktCZL7OvY8UZOEPlakpTlB8zy8fHHg-vXixTxQ9nZhLaBM8_5NmrnLEBx65kRkTEiX5goTCFJO-XaVw_RdlniTVK4gdXBjwJXvjixSf0n_-XbQCtpzJWLPkoKjbjoV6nPXV5CqQHS5evjaIjIPZmpQ

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### ro...@chromium.org (2015-01-14)

Re-opening as I now believe the fix was incorrect, prompted by looking into 448067.

### cl...@chromium.org (2015-01-14)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-01-15)

[Empty comment from Monorail migration]

### in...@chromium.org (2015-01-25)

Robert, any update here ? Was your fix reverted ?

### bu...@chromium.org (2015-01-27)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=189049

------------------------------------------------------------------
r189049 | robhogan@gmail.com | 2015-01-27T19:13:04.115098Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/rendering/RenderHTMLCanvas.cpp?r1=189049&r2=189048&pathrev=189049
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/rendering/RenderBlockFlow.cpp?r1=189049&r2=189048&pathrev=189049

Ensure we remove floats from descendants even if they have become inline

This is a second go at https://codereview.chromium.org/828163002/. My solution
there was wrong. The real problem was that we were failing to remove the float
from the float-lists of all its parents descendants. The reason this has started
happening is because we can now make children inline while leaving their float
lists in place: this was introduced in https://codereview.chromium.org/253313005.

So if we are trying to remove a float from float-lists, inspect its children
even if they are inline.

BUG=448067, 445285

Review URL: https://codereview.chromium.org/850143002
-----------------------------------------------------------------

### in...@chromium.org (2015-01-27)

[Empty comment from Monorail migration]

### ti...@google.com (2015-02-17)

Merge Requested to M41 (Branch 2272)

### pe...@google.com (2015-02-17)

[Automated comment] Reverts referenced in bugdroid comments, needs manual review.

### pe...@chromium.org (2015-02-18)

Merge approved for M41 branch 2272.

### ti...@google.com (2015-02-23)

robhogan: please merge to M41 (branch 2272)

### ti...@google.com (2015-02-26)

inferno: can you land this change to the branch so that if an M41 patch comes along we can ship this?

### ti...@google.com (2015-02-26)

[Empty comment from Monorail migration]

### in...@chromium.org (2015-02-26)

This needs bake time, still pretty fresh.

### ti...@google.com (2015-03-16)

inferno@ - should we land the M41 merge now?

### ti...@google.com (2015-03-26)

Leaving for M42.

### ti...@google.com (2015-04-09)

Congratulations - $2000 for this report.

### cl...@chromium.org (2015-05-06)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2015-05-06)

[Empty comment from Monorail migration]

### ti...@google.com (2015-06-03)

Processing via our *new* e-payment system should only take a 7-10 days and the reward should be on its way to you. Thanks again for your help!

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/445285?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/448067]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081071)*
