# Destroying nextblock in RenderBlock::removeChild can cause oldChild and nextblock's next sibling to be merged.

| Field | Value |
|-------|-------|
| **Issue ID** | [40086618](https://issues.chromium.org/issues/40086618) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | ma...@gmail.com |
| **Assignee** | in...@chromium.org |
| **Created** | 2011-01-03 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

Two separate HTML files have been attached which each trigger a jump to null in the 8.0.552.224 Ubuntu 10.10 release of Chromium. In each case, a small number of DOM nodes are created, appended to a document, and removed. When removing certain nodes, a jump to null is triggered in each of the two cases. Common among the two proof of concept files are a span with a display property of run-in and a different span with a display property of list-item.

**VERSION**  

Chrome Version: 8.0.552.224 Ubuntu 10.10 stable  

Operating System: Ubuntu 10.10

**REPRODUCTION CASE**  

I have attached two files, 0.html and 1.html, which trigger crashes in slightly different portions of the code, though I suspect that they have the same root cause. In both cases I was unable to reproduce the crash if additional elements were removed, but common in both cases were an element with a display type of run-in, and a separate element with display type of list-item. This may not be the root cause of the issue, since in each case more is going on, but it seemed to be a strange coincidence.

I have also tired to narrow the proof of concept files down further. When pruning additional moves and elements the crash either did not occur or was significantly less reliable.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab

Below are slightly truncated versions of the traces through the programs with gdb and valgrind (using the development branch of Chromium 10.0.626.0). The full traces have been included as attachments.

For the file 0.html:

$ chromium-browser --debug --single-process 0.html

# Env:

# LD\_LIBRARY\_PATH=/usr/lib/chromium-browser

# PATH=/usr/lib/chromium-browser:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games

# GTK\_PATH=

# CHROMIUM\_USER\_FLAGS=

# CHROMIUM\_FLAGS=

/usr/bin/gdb /usr/lib/chromium-browser/chromium-browser -x /tmp/chromiumargs.DlQ3kQ  

GNU gdb (GDB) 7.2-ubuntu  

...

Program received signal SIGSEGV, Segmentation fault.  

[Switching to Thread 0xb09fdb70 (LWP 2039)]  

0x00000000 in ?? ()  

(gdb) bt  

#0 0x00000000 in ?? ()  

#1 0x0194b82b in markContainingBlocksForLayout (this=0x2e29944, owner=  

0x2e298e4, oldChild=0x0, fullRemove=true)  

at third\_party/WebKit/WebCore/rendering/RenderObject.h:946  

#2 setNeedsLayout (this=0x2e29944, owner=0x2e298e4, oldChild=0x0,  

fullRemove=true) at third\_party/WebKit/WebCore/rendering/RenderObject.h:884  

#3 setNeedsLayoutAndPrefWidthsRecalc (this=0x2e29944, owner=0x2e298e4,  

oldChild=0x0, fullRemove=true)  

at third\_party/WebKit/WebCore/rendering/RenderObject.h:466  

#4 WebCore::RenderObjectChildList::removeChildNode (this=0x2e29944,  

owner=0x2e298e4, oldChild=0x0, fullRemove=true)  

at third\_party/WebKit/WebCore/rendering/RenderObjectChildList.cpp:70  

#5 0x01943ca0 in WebCore::RenderObject::removeChild (this=0x2e298e4,  

oldChild=0x2e2959c)  

at third\_party/WebKit/WebCore/rendering/RenderObject.cpp:340  

#6 0x018dc77f in WebCore::RenderBlock::removeChild (this=0x2e298e4,  

oldChild=0x2e2959c)  

at third\_party/WebKit/WebCore/rendering/RenderBlock.cpp:996  

#7 0x019438f5 in remove (this=0x2e2959c)  

at third\_party/WebKit/WebCore/rendering/RenderObject.h:727  

#8 WebCore::RenderObject::destroy (this=0x2e2959c)  

at third\_party/WebKit/WebCore/rendering/RenderObject.cpp:2178  

#9 0x018f8d11 in WebCore::RenderBoxModelObject::destroy (this=0x2e2959c)  

---Type <return> to continue, or q <return> to quit---

(gdb) frame 1  

#1 0x0194b82b in markContainingBlocksForLayout (this=0x2e29944,  

owner=0x2e298e4, oldChild=0x0, fullRemove=true)  

at third\_party/WebKit/WebCore/rendering/RenderObject.h:946  

946 third\_party/WebKit/WebCore/rendering/RenderObject.h: No such file or directory.  

in third\_party/WebKit/WebCore/rendering/RenderObject.h  

(gdb) disassemble $pc-16,$pc+16  

Dump of assembler code from 0x194b81b to 0x194b83b:  

0x0194b81b <WebCore::RenderObjectChildList::removeChildNode(WebCore::RenderObject\*, WebCore::RenderObject\*, bool)+1083>: decl -0x74ffd98c(%ebp)  

0x0194b821 <WebCore::RenderObjectChildList::removeChildNode(WebCore::RenderObject\*, WebCore::RenderObject\*, bool)+1089>: push %es  

0x0194b822 <WebCore::RenderObjectChildList::removeChildNode(WebCore::RenderObject\*, WebCore::RenderObject\*, bool)+1090>: mov %esi,(%esp)  

0x0194b825 <WebCore::RenderObjectChildList::removeChildNode(WebCore::RenderObject\*, WebCore::RenderObject\*, bool)+1093>: call \*0xb0(%eax)  

=> 0x0194b82b <WebCore::RenderObjectChildList::removeChildNode(WebCore::RenderObject\*, WebCore::RenderObject\*, bool)+1099>: test %al,%al  

0x0194b82d <WebCore::RenderObjectChildList::removeChildNode(WebCore::RenderObject\*, WebCore::RenderObject\*, bool)+1101>: jne 0x194b67d <WebCore::RenderObjectChildList::removeChildNode(WebCore::RenderObject\*, WebCore::RenderObject\*, bool)+669>  

0x0194b833 <WebCore::RenderObjectChildList::removeChildNode(WebCore::RenderObject\*, WebCore::RenderObject\*, bool)+1107>: mov -0x24(%ebp),%edi  

0x0194b836 <WebCore::RenderObjectChildList::removeChildNode(WebCore::RenderObject\*, WebCore::RenderObject\*, bool)+1110>: mov -0x28(%ebp),%esi  

0x0194b839 <WebCore::RenderObjectChildList::removeChildNode(WebCore::RenderObject\*, WebCore::RenderObject\*, bool)+1113>: jmp 0x194b728 <WebCore::RenderObjectChildList::removeChildNode(WebCore::RenderObject\*, WebCore::RenderObject\*, bool)+840>  

---Type <return> to continue, or q <return> to quit---  

End of assembler dump.  

(gdb) i r  

eax 0x2e29448 48403528  

ecx 0x2e29110 48402704  

edx 0x328fdc0 53018048  

ebx 0x2d20d14 47320340  

esp 0xb09fc5e0 0xb09fc5e0  

ebp 0xb09fc618 0xb09fc618  

esi 0x2e2964c 48404044  

edi 0x0 0  

eip 0x194b82b 0x194b82b <WebCore::RenderObjectChildList::removeChildNode(WebCore::RenderObject\*, WebCore::RenderObject\*, bool)+1099>  

eflags 0x210246 [ PF ZF IF RF ID ]  

cs 0x73 115  

ss 0x7b 123  

ds 0x7b 123  

es 0x7b 123  

fs 0x0 0  

gs 0x33 51

==4810== Thread 13:  

==4810== Conditional jump or move depends on uninitialised value(s)  

==4810== at 0x91D0866: v8::internal::StackTracer::Trace(v8::internal::TickSample\*) (log.cc:167)  

==4810== by 0x91D50D2: v8::internal::Ticker::DoSampleStack(v8::internal::TickSample\*) (log.cc:237)  

==4810== by 0x93A2FBA: v8::internal::Sampler::SampleStack(v8::internal::TickSample\*) (platform.h:575)  

==4810== by 0x93A27C7: v8::internal::ProfilerSignalHandler(int, siginfo\*, void\*) (platform-linux.cc:809)  

==4810== by 0x4BCCACF: ??? (in /lib/libpthread-2.12.1.so)  

==4810== by 0x8BDE3FF: tcmalloc::PageHeap::DecommitSpan(tcmalloc::Span\*) (page\_heap.cc:160)  

==4810== by 0x8BDED8D: tcmalloc::PageHeap::MergeIntoFreeList(tcmalloc::Span\*) (page\_heap.cc:286)  

==4810== by 0x8BDE9E2: tcmalloc::PageHeap::Delete(tcmalloc::Span\*) (page\_heap.cc:216)  

==4810== by 0x8BD04F1: (anonymous namespace)::do\_free\_with\_callback(void\*, void (\*)(void\*)) (tcmalloc.cc:1056)  

==4810== by 0x8BD051E: (anonymous namespace)::do\_free(void\*) (tcmalloc.cc:1062)  

==4810== by 0xA7F52AE: free (in /home/marty/Documents/security\_research/tests/chromium/home/chrome-svn/tarball/chromium/src/out/Debug/chrome)  

==4810== by 0x93A62C6: v8::internal::Malloced::Delete(void\*) (allocation.cc:50)  

==4810==  

==4810== Invalid read of size 4  

==4810== at 0x9A9BA23: WebCore::RenderObject::markContainingBlocksForLayout(bool, WebCore::RenderObject\*) (RenderObject.h:959)  

==4810== by 0x9A9B74C: WebCore::RenderObject::setNeedsLayout(bool, bool) (RenderObject.h:897)  

==4810== by 0x9A9B67C: WebCore::RenderObject::setNeedsLayoutAndPrefWidthsRecalc() (RenderObject.h:470)  

==4810== by 0xA1DB1F3: WebCore::RenderObjectChildList::removeChildNode(WebCore::RenderObject\*, WebCore::RenderObject\*, bool) (RenderObjectChildList.cpp:70)  

==4810== by 0xA1D12E9: WebCore::RenderObject::removeChild(WebCore::RenderObject\*) (RenderObject.cpp:339)  

==4810== by 0xA1375A9: WebCore::RenderBlock::removeChild(WebCore::RenderObject\*) (RenderBlock.cpp:999)  

==4810== by 0xA1C2475: WebCore::RenderObject::remove() (RenderObject.h:727)  

==4810== by 0xA1D8FA3: WebCore::RenderObject::destroy() (RenderObject.cpp:2185)  

==4810== by 0xA17B812: WebCore::RenderBoxModelObject::destroy() (RenderBoxModelObject.cpp:246)  

==4810== by 0xA1963C7: WebCore::RenderInline::destroy() (RenderInline.cpp:93)  

==4810== by 0x9F08270: WebCore::Node::detach() (Node.cpp:1256)  

==4810== by 0x9EAD6CD: WebCore::ContainerNode::detach() (ContainerNode.cpp:724)  

==4810== Address 0x12c is not stack'd, malloc'd or (recently) free'd  

==4810==  

==4810==  

==4810== Process terminating with default action of signal 11 (SIGSEGV)  

==4810== Access not within mapped region at address 0x12C  

==4810== at 0x9A9BA23: WebCore::RenderObject::markContainingBlocksForLayout(bool, WebCore::RenderObject\*) (RenderObject.h:959)  

==4810== by 0x9A9B74C: WebCore::RenderObject::setNeedsLayout(bool, bool) (RenderObject.h:897)  

==4810== by 0x9A9B67C: WebCore::RenderObject::setNeedsLayoutAndPrefWidthsRecalc() (RenderObject.h:470)  

==4810== by 0xA1DB1F3: WebCore::RenderObjectChildList::removeChildNode(WebCore::RenderObject\*, WebCore::RenderObject\*, bool) (RenderObjectChildList.cpp:70)  

==4810== by 0xA1D12E9: WebCore::RenderObject::removeChild(WebCore::RenderObject\*) (RenderObject.cpp:339)  

==4810== by 0xA1375A9: WebCore::RenderBlock::removeChild(WebCore::RenderObject\*) (RenderBlock.cpp:999)  

==4810== by 0xA1C2475: WebCore::RenderObject::remove() (RenderObject.h:727)  

==4810== by 0xA1D8FA3: WebCore::RenderObject::destroy() (RenderObject.cpp:2185)  

==4810== by 0xA17B812: WebCore::RenderBoxModelObject::destroy() (RenderBoxModelObject.cpp:246)  

==4810== by 0xA1963C7: WebCore::RenderInline::destroy() (RenderInline.cpp:93)  

==4810== by 0x9F08270: WebCore::Node::detach() (Node.cpp:1256)  

==4810== by 0x9EAD6CD: WebCore::ContainerNode::detach() (ContainerNode.cpp:724)  

==4810== If you believe this happened as a result of a stack  

==4810== overflow in your program's main thread (unlikely but  

==4810== possible), you can try to increase the size of the  

==4810== main thread stack using the --main-stacksize= flag.  

==4810== The main thread stack size used in this run was 8388608.

For the file 1.html:

$ chromium-browser --debug --single-process 1.html

# Env:

# LD\_LIBRARY\_PATH=/usr/lib/chromium-browser

# PATH=/usr/lib/chromium-browser:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games

# GTK\_PATH=

# CHROMIUM\_USER\_FLAGS=

# CHROMIUM\_FLAGS=

/usr/bin/gdb /usr/lib/chromium-browser/chromium-browser -x /tmp/chromiumargs.nXCKsz  

GNU gdb (GDB) 7.2-ubuntu  

...

Program received signal SIGSEGV, Segmentation fault.  

[Switching to Thread 0xb1646b70 (LWP 2100)]  

0x00000000 in ?? ()  

(gdb) bt  

#0 0x00000000 in ?? ()  

#1 0x0194387f in WebCore::RenderObject::destroy (this=0x2e29cc4)  

at third\_party/WebKit/WebCore/rendering/RenderObject.cpp:2152  

#2 0x018f8d11 in WebCore::RenderBoxModelObject::destroy (this=0x2e29cc4)  

at third\_party/WebKit/WebCore/rendering/RenderBoxModelObject.cpp:220  

#3 0x018f1c6c in WebCore::RenderBox::destroy (this=0x2e29cc4)  

at third\_party/WebKit/WebCore/rendering/RenderBox.cpp:209  

#4 0x018cef4c in WebCore::RenderBlock::destroy (this=0x2e29cc4)  

at third\_party/WebKit/WebCore/rendering/RenderBlock.cpp:190  

#5 0x0194a711 in WebCore::RenderObjectChildList::destroyLeftoverChildren (  

this=0x2e296f8)  

at third\_party/WebKit/WebCore/rendering/RenderObjectChildList.cpp:57  

#6 0x018ceee2 in WebCore::RenderBlock::destroy (this=0x2e29698)  

at third\_party/WebKit/WebCore/rendering/RenderBlock.cpp:156  

#7 0x0194a711 in WebCore::RenderObjectChildList::destroyLeftoverChildren (  

this=0x2e297a8)  

at third\_party/WebKit/WebCore/rendering/RenderObjectChildList.cpp:57  

#8 0x018ceee2 in WebCore::RenderBlock::destroy (this=0x2e29748)  

at third\_party/WebKit/WebCore/rendering/RenderBlock.cpp:156  

#9 0x019140f4 in WebCore::RenderInline::destroy (this=0x2e29830)  

at third\_party/WebKit/WebCore/rendering/RenderInline.cpp:65  

#10 0x0194a755 in WebCore::RenderObjectChildList::destroyLeftoverChildren (  

this=0x2e294a8)  

---Type <return> to continue, or q <return> to quit---

(gdb) frame 1  

#1 0x0194387f in WebCore::RenderObject::destroy (this=0x2e29cc4)  

at third\_party/WebKit/WebCore/rendering/RenderObject.cpp:2152  

2152 third\_party/WebKit/WebCore/rendering/RenderObject.cpp: No such file or directory.  

in third\_party/WebKit/WebCore/rendering/RenderObject.cpp  

(gdb) disassemble $pc-16,$pc+16  

Dump of assembler code from 0x194386f to 0x194388f:  

0x0194386f [WebCore::RenderObject::destroy()+15](javascript:void(0);): xchg %eax,%ebx  

0x01943870 [WebCore::RenderObject::destroy()+16](javascript:void(0);): incb 0x3dd4a3c3(%ecx)  

0x01943876 [WebCore::RenderObject::destroy()+22](javascript:void(0);): add %ecx,0x24348906(%ebx)  

0x0194387c [WebCore::RenderObject::destroy()+28](javascript:void(0);): call \*0x24(%eax)  

=> 0x0194387f [WebCore::RenderObject::destroy()+31](javascript:void(0);): test %eax,%eax  

0x01943881 [WebCore::RenderObject::destroy()+33](javascript:void(0);): je 0x194388b [WebCore::RenderObject::destroy()+43](javascript:void(0);)  

0x01943883 [WebCore::RenderObject::destroy()+35](javascript:void(0);): mov %eax,(%esp)  

0x01943886 [WebCore::RenderObject::destroy()+38](javascript:void(0);): call 0x194a680 [WebCore::RenderObjectChildList::destroyLeftoverChildren()](javascript:void(0);)  

0x0194388b [WebCore::RenderObject::destroy()+43](javascript:void(0);): mov 0x8(%esi),%eax  

0x0194388e [WebCore::RenderObject::destroy()+46](javascript:void(0);): mov 0x14(%eax),%eax  

End of assembler dump.  

(gdb) i r  

eax 0x2e29d38 48405816  

ecx 0x31528c0 51718336  

edx 0x31a19f0 52042224  

ebx 0x2d20d14 47320340  

esp 0xb1644d80 0xb1644d80  

ebp 0xb1644da8 0xb1644da8  

esi 0x2e29cc4 48405700  

edi 0x0 0  

eip 0x194387f 0x194387f [WebCore::RenderObject::destroy()+31](javascript:void(0);)  

eflags 0x210206 [ PF IF RF ID ]  

cs 0x73 115  

ss 0x7b 123  

ds 0x7b 123  

es 0x7b 123  

fs 0x0 0  

gs 0x33 51

==4858== Thread 13:  

==4858== Conditional jump or move depends on uninitialised value(s)  

==4858== at 0x91D0866: v8::internal::StackTracer::Trace(v8::internal::TickSample\*) (log.cc:167)  

==4858== by 0x91D50D2: v8::internal::Ticker::DoSampleStack(v8::internal::TickSample\*) (log.cc:237)  

==4858== by 0x93A2FBA: v8::internal::Sampler::SampleStack(v8::internal::TickSample\*) (platform.h:575)  

==4858== by 0x93A27C7: v8::internal::ProfilerSignalHandler(int, siginfo\*, void\*) (platform-linux.cc:809)  

==4858== by 0x4BCCACF: ??? (in /lib/libpthread-2.12.1.so)  

==4858== by 0x910BB62: v8::internal::Object::IsDescriptorArray() (objects-inl.h:458)  

==4858== by 0x910C546: v8::internal::DescriptorArray::cast(v8::internal::Object\*) (objects-inl.h:1711)  

==4858== by 0x910A6C0: v8::internal::Heap::empty\_descriptor\_array() (heap.h:771)  

==4858== by 0x910C0A8: v8::internal::DescriptorArray::IsEmpty() (objects-inl.h:1540)  

==4858== by 0x910A4E6: v8::internal::DescriptorArray::number\_of\_descriptors() (objects.h:1938)  

==4858== by 0x910C10A: v8::internal::DescriptorArray::GetKey(int) (objects-inl.h:1581)  

==4858== by 0x91F33E6: v8::internal::DescriptorArray::LinearSearch(v8::internal::String\*, int) (objects.cc:4144)  

==4858==  

==4858== Conditional jump or move depends on uninitialised value(s)  

==4858== at 0x90E20EC: CheckHelper(char const\*, int, char const\*, bool) (checks.h:59)  

==4858== by 0x90F8C47: v8::internal::HeapObject::cast(v8::internal::Object\*) (objects-inl.h:1730)  

==4858== by 0x91D0872: v8::internal::StackTracer::Trace(v8::internal::TickSample\*) (log.cc:168)  

==4858== by 0x91D50D2: v8::internal::Ticker::DoSampleStack(v8::internal::TickSample\*) (log.cc:237)  

==4858== by 0x93A2FBA: v8::internal::Sampler::SampleStack(v8::internal::TickSample\*) (platform.h:575)  

==4858== by 0x93A27C7: v8::internal::ProfilerSignalHandler(int, siginfo\*, void\*) (platform-linux.cc:809)  

==4858== by 0x4BCCACF: ??? (in /lib/libpthread-2.12.1.so)  

==4858== by 0x910C07F: v8::internal::FixedArray::fast\_set(v8::internal::FixedArray\*, int, v8::internal::Object\*) (objects-inl.h:1480)  

==4858== by 0x92026C7: v8::internal::DescriptorArray::fast\_swap(v8::internal::FixedArray\*, int, int) (objects-inl.h:1548)  

==4858== by 0x9202922: v8::internal::DescriptorArray::Swap(int, int) (objects-inl.h:1681)  

==4858== by 0x91F3057: v8::internal::DescriptorArray::SortUnchecked() (objects.cc:4072)  

==4858== by 0x91F31B0: v8::internal::DescriptorArray::Sort() (objects.cc:4105)  

==4858==  

==4858== Invalid read of size 4  

==4858== at 0xA1D8E43: WebCore::RenderObject::destroy() (RenderObject.cpp:2159)  

==4858== by 0xA17B812: WebCore::RenderBoxModelObject::destroy() (RenderBoxModelObject.cpp:246)  

==4858== by 0xA16C20D: WebCore::RenderBox::destroy() (RenderBox.cpp:209)  

==4858== by 0xA1346D6: WebCore::RenderBlock::destroy() (RenderBlock.cpp:186)  

==4858== by 0xA1DB13E: WebCore::RenderObjectChildList::destroyLeftoverChildren() (RenderObjectChildList.cpp:57)  

==4858== by 0xA134574: WebCore::RenderBlock::destroy() (RenderBlock.cpp:151)  

==4858== by 0xA1DB13E: WebCore::RenderObjectChildList::destroyLeftoverChildren() (RenderObjectChildList.cpp:57)  

==4858== by 0xA134574: WebCore::RenderBlock::destroy() (RenderBlock.cpp:151)  

==4858== by 0xA19629C: WebCore::RenderInline::destroy() (RenderInline.cpp:65)  

==4858== by 0xA1DB0E3: WebCore::RenderObjectChildList::destroyLeftoverChildren() (RenderObjectChildList.cpp:52)  

==4858== by 0xA134574: WebCore::RenderBlock::destroy() (RenderBlock.cpp:151)  

==4858== by 0xA1DB13E: WebCore::RenderObjectChildList::destroyLeftoverChildren() (RenderObjectChildList.cpp:57)  

==4858== Address 0x98 is not stack'd, malloc'd or (recently) free'd  

==4858==  

==4858==  

==4858== Process terminating with default action of signal 11 (SIGSEGV)  

==4858== Access not within mapped region at address 0x98  

==4858== at 0xA1D8E43: WebCore::RenderObject::destroy() (RenderObject.cpp:2159)  

==4858== by 0xA17B812: WebCore::RenderBoxModelObject::destroy() (RenderBoxModelObject.cpp:246)  

==4858== by 0xA16C20D: WebCore::RenderBox::destroy() (RenderBox.cpp:209)  

==4858== by 0xA1346D6: WebCore::RenderBlock::destroy() (RenderBlock.cpp:186)  

==4858== by 0xA1DB13E: WebCore::RenderObjectChildList::destroyLeftoverChildren() (RenderObjectChildList.cpp:57)  

==4858== by 0xA134574: WebCore::RenderBlock::destroy() (RenderBlock.cpp:151)  

==4858== by 0xA1DB13E: WebCore::RenderObjectChildList::destroyLeftoverChildren() (RenderObjectChildList.cpp:57)  

==4858== by 0xA134574: WebCore::RenderBlock::destroy() (RenderBlock.cpp:151)  

==4858== by 0xA19629C: WebCore::RenderInline::destroy() (RenderInline.cpp:65)  

==4858== by 0xA1DB0E3: WebCore::RenderObjectChildList::destroyLeftoverChildren() (RenderObjectChildList.cpp:52)  

==4858== by 0xA134574: WebCore::RenderBlock::destroy() (RenderBlock.cpp:151)  

==4858== by 0xA1DB13E: WebCore::RenderObjectChildList::destroyLeftoverChildren() (RenderObjectChildList.cpp:57)  

==4858== If you believe this happened as a result of a stack  

==4858== overflow in your program's main thread (unlikely but  

==4858== possible), you can try to increase the size of the  

==4858== main thread stack using the --main-stacksize= flag.  

==4858== The main thread stack size used in this run was 8388608.

## Attachments

- [0.html](attachments/0.html) (text/html; charset=us-ascii, 1.1 KB)
- [1.html](attachments/1.html) (text/html; charset=us-ascii, 1.1 KB)
- [0_gdb.txt](attachments/0_gdb.txt) (text/plain; charset=us-ascii, 10.3 KB)
- [1_valgrind.txt](attachments/1_valgrind.txt) (text/x-c; charset=us-ascii, 7.4 KB)
- [0_valgrind.txt](attachments/0_valgrind.txt) (text/plain; charset=us-ascii, 6.4 KB)
- [1_gdb.txt](attachments/1_gdb.txt) (text/plain; charset=us-ascii, 14.5 KB)
- [repro_server.py](attachments/repro_server.py) (text/x-pascal; charset=us-ascii, 16.9 KB)
- [chrome.dll!WebCore..RenderObject..markContainingBlocksForLayout ExecAV@Arbitrary (973d3e84ba8b317bb30c1e0dd47e9948).repro.pickle.zip](attachments/chrome.dll!WebCore..RenderObject..markContainingBlocksForLayout ExecAV@Arbitrary (973d3e84ba8b317bb30c1e0dd47e9948).repro.pickle.zip) (application/zip; charset=binary, 8.5 KB)

## Timeline

### in...@chromium.org (2011-01-03)

Both testcases trigger stale pointers. Need to reduce these before proceeding further and might be dupes. Will try to minimize these soon.

### in...@chromium.org (2011-01-03)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-01-03)

assigning to me for now.

### sk...@chromium.org (2011-01-03)

One of my execCommand fuzzers found a ExecAV@NULL (and @Arbitrary) in markContaingingBlocksForLayout on 31-12 as well. This suggests that the problem may have been recently introduced. Repro+server attached (run .py, point browser to http://localhost:28876/). I can manually reduce it to one file if it turns out not to be a dup, but I'd rather not bother if you can confirm it triggers the same issue.

### in...@chromium.org (2011-01-03)

This exists in v8 stable and reduced version looks like this. Still dont know if the root cause is in listItem styling or runIn styling (higher probability). Also this reduction is from first testcase (second testcase i see is almost similar).

<body onload="runTest();">
<span style="display: run-in" id="runIn">
</span>
<span style="display: list-item" id="listItem">
</span>
<script>
function runTest()
{
    document.body.offsetTop;
    var runIn = document.getElementById('runIn');
    var listItem = document.getElementById('listItem');

    runIn.appendChild(document.createElement('menu'));
    
    ol = document.createElement('ol');
    listItem.appendChild(ol);
    listItem.appendChild(document.createElement('span'));
    
    document.body.offsetTop;
    listItem.removeChild(ol);
    document.body.removeChild(runIn);
    document.body.removeChild(listItem);
}
</script>
</body>

### in...@chromium.org (2011-01-05)

I understand the problem atleast, testing out a fix.

### in...@chromium.org (2011-01-05)

filed webkit bug - https://bugs.webkit.org/show_bug.cgi?id=51919.

### in...@chromium.org (2011-01-05)

http://trac.webkit.org/changeset/75082

### in...@chromium.org (2011-01-05)

build fix in http://trac.webkit.org/changeset/75084.

### in...@chromium.org (2011-01-05)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-01-05)

merged to m8 in r75090 (both changesets), still needs m9 merge.

### sc...@gmail.com (2011-01-05)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-01-05)

@MartyBarbella: congratulations! This report has qualified for a provisional $1000 Chromium Security Reward.
The panel was impressed by the level of detail (stack traces, register details, good repros).

It turns out this seems to be a duplicate of the older internal https://crbug.com/chromium/66051 (by SkyLined), however it is your report that enabled us to very rapidly fix the issue (as you can see :), hence the reward.

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

### ma...@gmail.com (2011-01-05)

Nice job fixing the issue, that was really quick.

To address the boilerplate text, I have not disclosed any information about this issue to any third parties, and have no plans on disclosing any details about the issue until after fixes have been released in the affected products.

### sc...@gmail.com (2011-01-05)

@MartyBarbella: thanks! What name would you like us to use for credit purposes in our release notes and Hall of Fame?

### ma...@gmail.com (2011-01-06)

Martin Barbella

### in...@chromium.org (2011-01-10)

merged to m9 in r75419.

### sc...@gmail.com (2011-01-13)

Released to as 8.0.552.237: http://googlechromereleases.blogspot.com/2011/01/chrome-stable-release.html

Just realized this is a 10-day fix from filed -> diagnosed -> fixed -> merged -> autoupdated to users. Cool!

@MartyBarbella: thanks again for your help! Here's the bit where we pay you $1000 for being awesome! Please e-mail cevans@chromium.org to get that going.

### ma...@gmail.com (2011-01-13)

After updating to Google Chrome 8.0.552.237 on my laptop (running Windows Vista) I just tried out both of the test cases again. 0.html is no longer crashing, as expected, but the 1.html test case is still crashing fairly consistently. It may have been caused by an unrelated issue. When I have time later in the day I'll look in to this a bit more, but this issue should probably be kept private in the meantime.

### in...@chromium.org (2011-01-13)

Marty, you are right. I am filing a new bug to investigate the crash in the 2nd testcase - http://code.google.com/p/chromium/issues/detail?id=69556.

### sc...@gmail.com (2011-02-10)

Invoice finalized; payment is in e-payment system.

Was fixed in 8.0.552.237

### js...@chromium.org (2011-03-21)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-10-05)

Batch update.

### sc...@gmail.com (2012-02-24)

[Empty comment from Monorail migration]

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

This issue was migrated from crbug.com/chromium/68439?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/66051]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40086618)*
