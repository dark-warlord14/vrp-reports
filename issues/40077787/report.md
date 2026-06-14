# Heap-buffer-overflow in WebCore::Element::recalcStyle

| Field | Value |
|-------|-------|
| **Issue ID** | [40077787](https://issues.chromium.org/issues/40077787) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | cl...@gmail.com |
| **Assignee** | ad...@chromium.org |
| **Created** | 2013-07-15 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

The attached test case crashes the chrome ASAN build in recalcStyle

**VERSION**  

Chrome Version: asan-symbolized-linux-release-211418  

Operating System: Linux 64bit

**REPRODUCTION CASE**  

Attached as a zip file as it requires multiple files. Loading crash.html will trigger the crash.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State: see attached crash.log

## Attachments

- [crash.log](attachments/crash.log) (text/plain; charset=us-ascii, 10.4 KB)
- [crash.zip](attachments/crash.zip) (application/zip; charset=binary, 1003 B)

## Timeline

### in...@chromium.org (2013-07-15)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-07-15)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6569399171416064

Uploader: inferno@chromium.org

Crash Type: Heap-buffer-overflow READ 4
Crash Address: 0x60e00001053f
Crash State:
  - crash stack -
  WebCore::Element::recalcStyle
  WebCore::Document::recalcStyle
  WebCore::Document::updateStyleIfNeeded
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=193329:193330

Minimized Testcase (0.79 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96HQ-0qj6LhFSKlEXh96x3MuPgrd75FeFQ3AlkJ9lAtK72dGcgxIszWSm_U9NbpcwgjLuxQuzmw1M7KA22BPTy7dvP5I4khM5oQ3KmOqnJBUBW6Rwj9ey3n383RJeZZOMeD5_Hk0oO1YDFI2Ap-vjEEKu96UA



### ae...@chromium.org (2013-07-24)

Reproduces on linux 30.0.1574.0.

### ae...@chromium.org (2013-07-24)

RenderStyle* Node::renderStyle() returns an unaligned pointer, ending with 0xf. Pretty interesting.

### jl...@chromium.org (2013-08-01)

Robert, would you mind taking a look at this (or help find a good owner) ?

It looks like you touch this code in b3eb70b7664ef89278c49f050467858cb0658457.

### jl...@chromium.org (2013-08-01)

[Empty comment from Monorail migration]

### jl...@chromium.org (2013-08-02)

[Empty comment from Monorail migration]

### ad...@chromium.org (2013-08-02)

Debug stack trace:

#0  0x00007ffff1992584 in WebCore::Node::rareData (this=0x2ece8b0a8298) at ../../third_party/WebKit/Source/core/dom/Node.cpp:380
#1  0x00007ffff199c0d8 in WebCore::Node::decrementConnectedSubframeCount (this=0x2ece8b0a8298, amount=1)
    at ../../third_party/WebKit/Source/core/dom/Node.cpp:2586
#2  0x00007ffff3310616 in WebCore::HTMLFrameOwnerElement::clearContentFrame (this=0x2ece8b0b40d0)
    at ../../third_party/WebKit/Source/core/html/HTMLFrameOwnerElement.cpp:73
#3  0x00007ffff277bad1 in WebCore::Frame::disconnectOwnerElement (this=0x26661c6773a0)
    at ../../third_party/WebKit/Source/core/page/Frame.cpp:383
#4  0x00007ffff331068e in WebCore::HTMLFrameOwnerElement::disconnectContentFrame (this=0x2ece8b0b40d0)
    at ../../third_party/WebKit/Source/core/html/HTMLFrameOwnerElement.cpp:85
#5  0x00007ffff1892d9b in WebCore::ChildFrameDisconnector::disconnectCollectedFrameOwners (this=0x7fffc96018a0)
    at ../../third_party/WebKit/Source/core/dom/ContainerNodeAlgorithms.h:313
#6  0x00007ffff188cdd1 in WebCore::ChildFrameDisconnector::disconnect (this=0x7fffc96018a0, 
    policy=WebCore::ChildFrameDisconnector::RootAndDescendants)
    at ../../third_party/WebKit/Source/core/dom/ContainerNodeAlgorithms.h:333
#7  0x00007ffff1889bfa in WebCore::willRemoveChild (child=0x2ece8b0b40d0)
    at ../../third_party/WebKit/Source/core/dom/ContainerNode.cpp:423
#8  0x00007ffff1889931 in WebCore::ContainerNode::removeChild (this=0x2ece8b0a8298, oldChild=0x2ece8b0b40d0, ec=@0x7fffc9601aa8: 0)
    at ../../third_party/WebKit/Source/core/dom/ContainerNode.cpp:481
#9  0x00007ffff1992d7a in WebCore::Node::removeChild (this=0x2ece8b0a8298, oldChild=0x2ece8b0b40d0, ec=@0x7fffc9601aa8: 0)
    at ../../third_party/WebKit/Source/core/dom/Node.cpp:531
#10 0x00007ffff315354a in WebCore::V8Node::removeChildMethodCustom (args=...)
    at ../../third_party/WebKit/Source/bindings/v8/custom/V8NodeCustom.cpp:104
#11 0x00007ffff2f9d874 in WebCore::NodeV8Internal::removeChildMethodCallbackForMainWorld (args=...) at gen/blink/bindings/V8Node.cpp:671
#12 0x00007ffff515afcb in v8::internal::FunctionCallbackArguments::Call (this=<optimized out>, f=<optimized out>)


### bu...@chromium.org (2013-08-15)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=156174

------------------------------------------------------------------------
r156174 | adamk@chromium.org | 2013-08-15T22:20:53.580101Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/frames/reattach-in-unload-expected.txt?r1=156174&r2=156173&pathrev=156174
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/html/HTMLFrameOwnerElement.h?r1=156174&r2=156173&pathrev=156174
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/frames/reattach-in-unload.html?r1=156174&r2=156173&pathrev=156174

Ensure that removing an iframe from the DOM tree disconnects its Frame

SubframeLoadingDisabler wasn't catching the case when an <iframe> was, in its unload
handler, removed and re-added to the same parent. Fix this by using a count of
SubframeLoadingDisablers that are on the stack for a given root, rather than a simple
boolean (using a HashCountedSet instead of a HashSet).

BUG=260375

Review URL: https://chromiumcodereview.appspot.com/21887005
------------------------------------------------------------------------

### in...@chromium.org (2013-08-15)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-08-17)

ClusterFuzz has detected this issue as fixed in range 217925:217943.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6569399171416064

Uploader: inferno@chromium.org
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-buffer-overflow READ 4
Crash Address: 0x60e00001053f
Crash State:
  - crash stack -
  WebCore::Element::recalcStyle
  WebCore::Document::recalcStyle
  WebCore::Document::updateStyleIfNeeded
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=193329:193330
Fixed: https://cluster-fuzz.appspot.com/revisions?range=217925:217943

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv96HQ-0qj6LhFSKlEXh96x3MuPgrd75FeFQ3AlkJ9lAtK72dGcgxIszWSm_U9NbpcwgjLuxQuzmw1M7KA22BPTy7dvP5I4khM5oQ3KmOqnJBUBW6Rwj9ey3n383RJeZZOMeD5_Hk0oO1YDFI2Ap-vjEEKu96UA

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### in...@chromium.org (2013-09-12)

Please merge your change to the m30 branch (1599) by early next week [using drover]. We have m30 beta coming next week and we want all the security changes in by that time. 

### in...@chromium.org (2013-09-13)

merged in r157783

### bu...@chromium.org (2013-09-13)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=157783

------------------------------------------------------------------------
r157783 | inferno@chromium.org | 2013-09-13T20:53:30.367005Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/branches/chromium/1599/LayoutTests/fast/frames/reattach-in-unload-expected.txt?r1=157783&r2=157782&pathrev=157783
   M http://src.chromium.org/viewvc/blink/branches/chromium/1599/Source/core/html/HTMLFrameOwnerElement.h?r1=157783&r2=157782&pathrev=157783
   A http://src.chromium.org/viewvc/blink/branches/chromium/1599/LayoutTests/fast/frames/reattach-in-unload.html?r1=157783&r2=157782&pathrev=157783

Merge 156174 "Ensure that removing an iframe from the DOM tree d..."

> Ensure that removing an iframe from the DOM tree disconnects its Frame
> 
> SubframeLoadingDisabler wasn't catching the case when an <iframe> was, in its unload
> handler, removed and re-added to the same parent. Fix this by using a count of
> SubframeLoadingDisablers that are on the stack for a given root, rather than a simple
> boolean (using a HashCountedSet instead of a HashSet).
> 
> BUG=260375
> 
> Review URL: https://chromiumcodereview.appspot.com/21887005

TBR=adamk@chromium.org

Review URL: https://codereview.chromium.org/23600050
------------------------------------------------------------------------

### in...@chromium.org (2013-09-16)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-09-25)

Did you saw our new criteria for possibly issuing higher rewards? See http://www.chromium.org/Home/chromium-security/vulnerability-rewards-program/reward-nomination-process
E.g. If you are able to provide a repro that faulted at an address of 0x41414141, it will qualify for the new higher rewards. Or, if you can show that you have control between free and crash points, etc.

### in...@chromium.org (2013-09-26)

Removing incorrect Release-0 which is reserved for bugs impacting stable.

### sc...@gmail.com (2013-09-28)

@cloudfuzzer: we're rewarding at $1000. As a reminder, we might be able to go higher (up to $5000+) if the analysis or repro has more detail and impact. Hard to tell what is going on in this particular ASAN trace.

### pa...@chromium.org (2013-10-18)

OK, kicked off payment for this one (and the rest). Expect something in a few weeks. Thanks again cloudfuzzer :)

### js...@chromium.org (2013-11-18)

Bulk release of old security bug reports.


### js...@chromium.org (2013-11-18)

Bulk release of old security bug reports.


### ti...@chromium.org (2014-02-28)

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

This issue was migrated from crbug.com/chromium/260375?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40077787)*
