# Heap-use-after-free in WebCore::RenderBlock::layoutBlockChildren

| Field | Value |
|-------|-------|
| **Issue ID** | [40059089](https://issues.chromium.org/issues/40059089) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | mi...@gmail.com |
| **Assignee** | in...@chromium.org |
| **Created** | 2012-05-31 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

use-after-free in WebCore::RenderBlock::layoutBlockChildren

**VERSION**  

Chrome Version: stable + dev

Chromium 21.0.1159.0 (Developer Build 139782)  

OS Linux  

WebKit 537.1 (@119013)

Operating System: 64bit precise

**REPRODUCTION CASE**

<html>
<head>
<style>
#el0 {
height: 1px;
-webkit-writing-mode: vertical-rl;
}
#el0:nth-child(3) {
height: auto;
}
</style>
<script>
onload = function() {
document.body.appendChild(document.createElement('select'))
document.body.appendChild(document.createElement('form'))
el0=document.createElement('input')
el0.setAttribute('id','el0')
el0.setAttribute('type', 'range')
document.body.appendChild(el0)
document.designMode='on'
document.execCommand('selectall')
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

==25800== ERROR: AddressSanitizer heap-use-after-free on address 0x7fffed5806b0 at pc 0x55555ae4a30b bp 0x7fffffff2330 sp 0x7fffffff2328  

READ of size 4 at 0x7fffed5806b0 thread T0  

#0 0x55555ae4a30b in WebCore::RenderBlock::layoutBlockChildren(bool, WebCore::FractionalLayoutUnit&) ???:0  

#1 0x55555ae4174c in WebCore::RenderBlock::layoutBlock(bool, WebCore::FractionalLayoutUnit) ???:0  

#2 0x55555ae3e36d in WebCore::RenderBlock::layout() ???:0

0x7fffed5806b0 is located 48 bytes inside of 184-byte region [0x7fffed580680,0x7fffed580738)  

freed by thread T0 here:  

#0 0x55555e658c72 in free ??:0  

#1 0x55555952eb1c in WebCore::Node::detach() ???:0  

#2 0x5555594f0f45 in WebCore::Element::detach() ???:0  

#3 0x555559459ab9 in WebCore::ContainerNode::detach() ???:0  

#4 0x5555595f77de in WebCore::ElementShadow::detach() ???:0

## Attachments

- [stable-48184.txt](attachments/stable-48184.txt) (text/plain; charset=us-ascii, 12.6 KB)
- [48184.html](attachments/48184.html) (text/html; charset=us-ascii, 720 B)
- [48184.txt](attachments/48184.txt) (text/plain; charset=us-ascii, 12.6 KB)

## Timeline

### in...@chromium.org (2012-05-31)

upstreamed - https://bugs.webkit.org/show_bug.cgi?id=88017

### in...@chromium.org (2012-05-31)

[Empty comment from Monorail migration]

### cl...@chromium.org (2012-06-12)

[Comment Deleted]

### cl...@chromium.org (2012-06-12)

[Comment Deleted]

### cl...@chromium.org (2012-06-12)

[Comment Deleted]

### in...@chromium.org (2012-06-12)

[Empty comment from Monorail migration]

### cl...@chromium.org (2012-06-12)

[Comment Deleted]

### cl...@chromium.org (2012-06-12)

[Comment Deleted]

### cl...@chromium.org (2012-06-12)

[Comment Deleted]

### cl...@chromium.org (2012-06-12)

[Comment Deleted]

### cl...@chromium.org (2012-06-12)

[Comment Deleted]

### in...@chromium.org (2012-06-20)

http://trac.webkit.org/changeset/120862

### in...@chromium.org (2012-06-21)

[Comment Deleted]

### in...@chromium.org (2012-06-21)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=65121273

Fuzzer: Inferno_layout_test_unmodified

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x7ff4ce7be4b0
Crash State:
  - crash stack -
  WebCore::RenderBlock::layoutBlockChildren
  WebCore::RenderBlock::layoutBlock
  - free stack -
  WebCore::Node::detach
  WebCore::Element::detach
  

Minimized Testcase (0.51 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv978WpDXPVYfJeUzvWA8C3XEOMkUSTl-aIouSRFGusOSpz1QsbmOEk8jdqomunlWI1cdzJJr_Zkf-OEPxd1xwZlIChcHQdief4AOEzPnBGtPN-Kw_88RtanyZdKBoEYpj8QGFGHZKPMDHwyEKbdxxl4dYDAl8Mjw5AazzOh2rrJJude092Y
<style>
#test1 { 
    height: 1px; 
    -webkit-writing-mode: vertical-rl;
}
#test1:nth-child(3) { 
    height: auto; 
</style>
<script>
onload = function() {
    document.body.appendChild(document.createElement('form'));
    test1 = document.createElement('input');
    test1.setAttribute('id', 'test1');
    test1.setAttribute('type', 'range');
    document.body.appendChild(test1);
    document.designMode = 'on';
    document.execCommand('selectall');
    document.execCommand('FormatBlock', false, '<'+'pre>');
}
</script>

### cl...@chromium.org (2012-06-22)

ClusterFuzz has detected this issue as fixed in range 143349:143352.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=65121273

Fuzzer: Inferno_layout_test_unmodified

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x7ff4ce7be4b0
Crash State:
  - crash stack -
  WebCore::RenderBlock::layoutBlockChildren
  WebCore::RenderBlock::layoutBlock
  - free stack -
  WebCore::Node::detach
  WebCore::Element::detach
  
Fixed: https://cluster-fuzz.appspot.com/revisions?range=143349:143352

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv978WpDXPVYfJeUzvWA8C3XEOMkUSTl-aIouSRFGusOSpz1QsbmOEk8jdqomunlWI1cdzJJr_Zkf-OEPxd1xwZlIChcHQdief4AOEzPnBGtPN-Kw_88RtanyZdKBoEYpj8QGFGHZKPMDHwyEKbdxxl4dYDAl8Mjw5AazzOh2rrJJude092Y

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### sc...@gmail.com (2012-07-09)

M20: http://trac.webkit.org/changeset/122128
M21: http://trac.webkit.org/changeset/122129

### sc...@gmail.com (2012-07-10)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-07-10)

Please accept another $1000 :)

### sc...@gmail.com (2012-09-12)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-10-14)

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

This issue was migrated from crbug.com/chromium/130595?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059089)*
