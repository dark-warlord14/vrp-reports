# <use> on <font-face> causes crashes, if SVGUseElement gets detached

| Field | Value |
|-------|-------|
| **Issue ID** | [40081971](https://issues.chromium.org/issues/40081971) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **CVE IDs** | CVE-2010-2902 |
| **Reporter** | ao...@gmail.com |
| **Assignee** | mo...@google.com |
| **Created** | 2010-07-04 |
| **Bounty** | $500.00 |

## Description

A renderer segmentation fault is triggered by an SVG document with the content: '<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"> <font-face id="foo"/> <use xlink:href="#foo"/> <crash>'. 

The error affects at least Chromium 6.0.453.0 (Developer Build 51332) in Ubuntu 10.04 (x64 and x86_64), and seems to cause an occasional segmentation fault when the browser is closed in current Google Chrome.

Backtrace begins:
Program received signal SIGSEGV, Segmentation fault.

WebCore::ContainerNode::removedFromDocument (this=0xa6ca4b0)
    at third_party/WebKit/WebCore/dom/ContainerNode.cpp:658
658     third_party/WebKit/WebCore/dom/ContainerNode.cpp: No such file or directory.
        in third_party/WebKit/WebCore/dom/ContainerNode.cpp
(gdb) bt
#0  WebCore::ContainerNode::removedFromDocument (this=0xa6ca4b0)
    at third_party/WebKit/WebCore/dom/ContainerNode.cpp:658
#1  0x08e3d221 in WebCore::Private::NodeRemovalDispatcher<WebCore::Node, true>::dispatch (head=@0xbfffd72c, tail=@0xbfffd728, container=0xa6613c0)
    at third_party/WebKit/WebCore/dom/ContainerNodeAlgorithms.h:99
#2  WebCore::Private::addChildNodesToDeletionQueue<WebCore::Node, WebCore::ContainerNode> (head=@0xbfffd72c, tail=@0xbfffd728, container=0xa6613c0)
    at third_party/WebKit/WebCore/dom/ContainerNodeAlgorithms.h:139
#3  0x08e3d260 in removeAllChildrenInContainer<WebCore::Node, WebCore::ContainerNode> (this=0xa6613c0)
    at third_party/WebKit/WebCore/dom/ContainerNodeAlgorithms.h:47
#4  WebCore::ContainerNode::removeAllChildren (this=0xa6613c0)
    at third_party/WebKit/WebCore/dom/ContainerNode.cpp:72
#5  0x08e3dfbf in ~ContainerNode (this=0xa6613c0, 
    __in_chrg=<value optimized out>)
    at third_party/WebKit/WebCore/dom/ContainerNode.cpp:77
#6  0x092f27d2 in ~SVGShadowTreeRootElement (this=0xa6613c0, 
    __in_chrg=<value optimized out>, __vtt_parm=<value optimized out>)
    at third_party/WebKit/WebCore/rendering/SVGShadowTreeElements.cpp:57
#7  0x092ea60e in derefIfNotNull<WebCore::SVGShadowTreeRootElement> (
    this=0xa6754e0, __in_chrg=<value optimized out>)
    at third_party/WebKit/JavaScriptCore/wtf/PassRefPtr.h:66
#8  ~RefPtr (this=0xa6754e0, __in_chrg=<value optimized out>)
[...]

The original non-minimized file triggered a segfault at WebCore::RenderObjectChildList::insertChildNode (this=0xa671620, owner=0xa671604, child=0xa67165c, beforeChild=0xa6716bc, fullInsert=true). It is probably just causing a different manifestation of the same bug, but I can be add it here if needed.

## Attachments

- [crash.svg](attachments/crash.svg) (text/plain; charset=us-ascii, 139 B)

## Timeline

### js...@chromium.org (2010-07-04)

Thanks Aki. This looks a lot like https://crbug.com/chromium/44500. The patch for that bug was just submitted and r+'d in the last two days, so it hasn't even landed upstream yet. I'll check your repro after it lands to see if it's the same bug.


### in...@chromium.org (2010-07-05)

The issue is very similar to 44500, but still crashes after applying the patch. I filed webkit bug - https://bugs.webkit.org/show_bug.cgi?id=41621. hopefully, nikolas will get to it soon.

### in...@chromium.org (2010-07-05)

[Empty comment from Monorail migration]

### js...@chromium.org (2010-07-05)

Before we left on Friday @cdn and I worked out the reentrancy issue that caused https://crbug.com/chromium/44500 (although Nikolas beat us to a patch). So, I may take a look at this one because I have a pretty idea of what will need to be fixed.


### in...@chromium.org (2010-07-07)

Fixed in http://trac.webkit.org/changeset/62662

### in...@chromium.org (2010-07-07)

[Empty comment from Monorail migration]

### sc...@gmail.com (2010-07-08)

Thanks again Aki! Another Chromium Security Reward for you.

### ao...@gmail.com (2010-07-09)

Most excellent :) Thank you.

### bu...@gmail.com (2010-07-14)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=52351 

------------------------------------------------------------------------
r52351 | inferno@chromium.org | 2010-07-14 11:17:44 -0700 (Wed, 14 Jul 2010) | 24 lines
Changed paths:
   A http://src.chromium.org/viewvc/chrome/branches/WebKit/375/LayoutTests/platform/mac/svg/custom/use-font-face-crash-expected.checksum
   A http://src.chromium.org/viewvc/chrome/branches/WebKit/375/LayoutTests/platform/mac/svg/custom/use-font-face-crash-expected.png
   A http://src.chromium.org/viewvc/chrome/branches/WebKit/375/LayoutTests/platform/mac/svg/custom/use-font-face-crash-expected.txt
   A http://src.chromium.org/viewvc/chrome/branches/WebKit/375/LayoutTests/svg/custom/use-font-face-crash.svg
   M http://src.chromium.org/viewvc/chrome/branches/WebKit/375/WebCore/svg/SVGFontFaceElement.cpp?r1=52351&r2=52350
   M http://src.chromium.org/viewvc/chrome/branches/WebKit/375/WebCore/svg/SVGUseElement.cpp?r1=52351&r2=52350

Merge 62662 - 2010-07-06  Nikolas Zimmermann  <nzimmermann@rim.com>

        Reviewed by Dirk Schulze.

        <use> on <font-face> causes crashes, if SVGUseElement gets detached
        https://bugs.webkit.org/show_bug.cgi?id=41621

        Do not call removeFromMappedElementSheet() from the SVGFontFaceElement destructor,
        as that can potentially cause the element to be reattached while destructing.

        In order to fix the crash in the testcase, the order of calling the base-class detach
        method in SVGUseElement and the instance/shadow tree destruction has to be reversed,
        matching the order in removedFromDocument().

        Test: svg/custom/use-font-face-crash.svg

        * svg/SVGFontFaceElement.cpp:
        (WebCore::SVGFontFaceElement::~SVGFontFaceElement): Remove removeFromMappedElementSheet() call.
        * svg/SVGUseElement.cpp:
        (WebCore::SVGUseElement::detach): Reverse order of calling base-class detach method and instance/shadow tree destruction.

BUG=48284

Review URL: http://codereview.chromium.org/2917014
------------------------------------------------------------------------


### in...@chromium.org (2010-07-14)

[Empty comment from Monorail migration]

### [Deleted User] (2010-07-20)

[Empty comment from Monorail migration]

### ro...@chromium.org (2010-07-21)

Verified on Mac 5.0.375.121 (Official Build 52864) beta

### sc...@gmail.com (2010-08-10)

Reward on it's way. Thanks Aki.

### sc...@gmail.com (2010-09-08)

Was fixed by Safai. Releasing.

### g....@gmail.com (2010-09-08)

@scarybeasts
duplicated as CVE-2010-2902

### js...@chromium.org (2010-11-30)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-03-21)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-10-05)

Batch update.

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-26)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-26)

This issue was migrated from crbug.com/chromium/48284?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081971)*
