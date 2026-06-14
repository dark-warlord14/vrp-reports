# Stale iterator in SVGDocumentExtensions::startAnimations()

| Field | Value |
|-------|-------|
| **Issue ID** | [40087375](https://issues.chromium.org/issues/40087375) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | mi...@gmail.com |
| **Assignee** | js...@chromium.org |
| **Created** | 2011-01-29 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

sad tab in bad html

**VERSION**  

Chrome Version:  

Chromium 11.0.653.0 (Developer Build 73068) Ubuntu 10.10  

on Ubuntu Maverick 2.6.35-25-generic

Chrome 8.0.552.236 Official Build 70801 on OSX Snow Leopard 10.6

**REPRODUCTION CASE**  

data:text/html;base64,PHN2Zz4KPGcgaWQ9IlIiPgo8bGluZWFyR3JhZGllbnQgaWQ9ImciPjxhbmltYXRlVHJhbnNmb3JtIGF0dHJpYnV0ZU5hbWU9ImEiLz48L2xpbmVhckdyYWRpZW50Pgo8Zm9udD48Zm9udC1mYWNlIGZvbnQtZmFtaWx5PSJ4Ii8+PGZvbnQ+Cjx4bWxuczp4bGluaz0iOi94LzAwLyIgYj0idj0iMiIJZTwvc2NyaXB0Pgo8c3ZnPjxsaW5lYXJHcmFkaWVudCBpZD0iZyI+PGFuaW1hdGVUcmFuc2Zvcm0gYXR0cmlidXRlTmFtZT0iYSIvPjwvbGluZWFyR3JhZGllbnQ+Cjxzdmc+PGxpbmVhckdyYWRpZW50IGlkPSJnIj48YW5pbWF0ZVRyYW5zZm9ybSBhdHRyaWJ1dGVOYW1lPSJhIi8+PC9saW5lYXJHcmFkaWVudD4KPHhtbG5zOnhsaW5rPSI6L3gvMDAvIiBiPSIidj0iMiIJZTwvc2NyaXB0Pgo8c3ZnPgo8ZyBpZD0iUiI+CjxsaW5lYXJHcmFkaWVudCBpZD0iZyI+PGFuaW1hdGVUcmFuc2Zvcm0gYXR0cmlidXRlTmFtZT0iYSIvPjwvbGluZWFyR3JhZGllbnQ+CjwvZz4KPHN2Zz4KPHN2Zz4KPGcgaWQ9IlIiPgo8bGluZWFyR3JhZGllbnQgaWQ9ImciPjxhbmltYXRlVHJhbnNmb3JtIGF0dHJpYnV0ZU5hbWU9ImEiLz48L2xpbmVhckdyYWRpZW50Pgo8L2c+Cjx1CjwvZz4KPHN2Zz4KPGcgaWQ9IlIiPjwvZz4KPHVzZSB4bGluazpocmVmPSIjUiI+Cgo8L2c+Cjx1CjwvZz4KPHN2Zz4KPGcgaWQ9IlIiPjwvZz4KPHVzZSB4bGluazpocmVmPSIjUiI+Cg==

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: sad tab  

Crash State:  

(gdb) r  

Starting program: /usr/lib/chromium-browser/chromium-browser --single-process small.html

Program received signal SIGSEGV, Segmentation fault.  

[Switching to Thread 0x7fffdf110700 (LWP 728)]  

0x0000000000000004 in ?? ()  

(gdb)  

(gdb) bt  

#0 0x0000000000000004 in ?? ()  

#1 0x00007ffff65f5335 in WebCore::Element::getAttribute (this=0x7ffff91a1a00, name="href") at third\_party/WebKit/Source/WebCore/dom/Element.cpp:231  

#2 0x00007ffff69af4f3 in WebCore::SVGSMILElement::xlinkHref (this=0x7ffff91a1a00) at third\_party/WebKit/Source/WebCore/svg/animation/SVGSMILElement.cpp:512  

#3 0x00007ffff69af52b in WebCore::SVGSMILElement::targetElement (this=0x7ffff91a1a00) at third\_party/WebKit/Source/WebCore/svg/animation/SVGSMILElement.cpp:464  

#4 0x00007ffff6a74315 in WebCore::SMILTimeContainer::updateAnimations (this=<value optimized out>, elapsed=DWARF-2 expression error: DW\_OP\_reg operations must be used either alone or in conjuction with DW\_OP\_piece or DW\_OP\_bit\_piece.  

) at third\_party/WebKit/Source/WebCore/svg/animation/SMILTimeContainer.cpp:238  

#5 0x00007ffff6a751b5 in WebCore::SMILTimeContainer::begin (this=0x7ffff9198140) at third\_party/WebKit/Source/WebCore/svg/animation/SMILTimeContainer.cpp:103  

#6 0x00007ffff69cd2ca in WebCore::SVGDocumentExtensions::startAnimations (this=<value optimized out>) at third\_party/WebKit/Source/WebCore/svg/SVGDocumentExtensions.cpp:98  

#7 0x00007ffff65dfe22 in WebCore::Document::implicitClose (this=0x7ffff972f400) at third\_party/WebKit/Source/WebCore/dom/Document.cpp:2209  

#8 0x00007ffff672e463 in WebCore::FrameLoader::checkCompleted (this=0x7ffff90aa070) at third\_party/WebKit/Source/WebCore/loader/FrameLoader.cpp:842  

#9 0x00007ffff672d207 in WebCore::FrameLoader::finishedParsing (this=0x7ffff90aa070) at third\_party/WebKit/Source/WebCore/loader/FrameLoader.cpp:776  

#10 0x00007ffff65e0490 in WebCore::Document::finishedParsing (this=0x7ffff972f400) at third\_party/WebKit/Source/WebCore/dom/Document.cpp:4282  

#11 0x00007ffff629d5c8 in WebCore::HTMLDocumentParser::prepareToStopParsing (this=0x7ffff9101000) at third\_party/WebKit/Source/WebCore/html/parser/HTMLDocumentParser.cpp:150  

#12 0x00007ffff629d614 in WebCore::HTMLDocumentParser::finish (this=0x7ffff9101000) at third\_party/WebKit/Source/WebCore/html/parser/HTMLDocumentParser.cpp:384  

#13 0x00007ffff6721cbf in WebCore::DocumentWriter::endIfNotLoadingMainResource (this=0x7ffff90aa290) at third\_party/WebKit/Source/WebCore/loader/DocumentWriter.cpp:221  

#14 0x00007ffff672e258 in WebCore::FrameLoader::finishedLoading (this=0x7ffff90aa070) at third\_party/WebKit/Source/WebCore/loader/FrameLoader.cpp:2184  

#15 0x00007ffff673bf22 in WebCore::MainResourceLoader::didFinishLoading (this=0x7ffff909f000, finishTime=<value optimized out>) at third\_party/WebKit/Source/WebCore/loader/MainResourceLoader.cpp:463  

#16 0x00007ffff5fc29c9 in webkit\_glue::WebURLLoaderImpl::Context::OnCompletedRequest (this=0x7ffff92a4960, status=<value optimized out>, security\_info=<value optimized out>, completion\_time=...)  

at webkit/glue/weburlloader\_impl.cc:655  

#17 0x00007ffff6b48bee in ResourceDispatcher::OnRequestComplete (this=<value optimized out>, request\_id=<value optimized out>, status=..., security\_info=..., completion\_time=...)  

at chrome/common/resource\_dispatcher.cc:457  

#18 0x00007ffff6b4a4c6 in DispatchToMethod<ResourceDispatcher, void (ResourceDispatcher::\*)(int, net::URLRequestStatus const&, std::string const&, base::Time const&), int, net::URLRequestStatus, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> >, base::Time> (this=0x7ffff9031b90, message=...) at ./base/tuple.h:570  

#19 Dispatch<ResourceDispatcher, ResourceDispatcher, void (ResourceDispatcher::\*)(int, net::URLRequestStatus const&, std::string const&, base::Time const&)> (this=0x7ffff9031b90, message=...)  

at ./ipc/ipc\_message\_utils.h:933  

#20 ResourceDispatcher::DispatchMessage (this=0x7ffff9031b90, message=...) at chrome/common/resource\_dispatcher.cc:530  

#21 0x00007ffff6b4aaeb in ResourceDispatcher::OnMessageReceived (this=0x7ffff9031b90, message=...) at chrome/common/resource\_dispatcher.cc:297  

#22 0x00007ffff6b64941 in ChildThread::OnMessageReceived (this=0x7ffff8de9d88, msg=...) at chrome/common/child\_thread.cc:144  

#23 0x00007ffff594e3b1 in MessageLoop::RunTask (this=0x7fffdf10fa90, task=0x7ffff9e3f0c0) at base/message\_loop.cc:362  

#24 0x00007ffff594fa4b in MessageLoop::DeferOrRunPendingTask (this=0x7fffdf10fa90, pending\_task=<value optimized out>) at base/message\_loop.cc:371  

#25 0x00007ffff594fd3d in MessageLoop::DoWork (this=0x7fffdf10fa90) at base/message\_loop.cc:564  

#26 0x00007ffff5951bb9 in base::MessagePumpDefault::Run (this=0x7ffff9035620, delegate=0x7fffdf10fa90) at base/message\_pump\_default.cc:23  

#27 0x00007ffff594f00c in RunHandler (this=0x7ffff91a1a00) at base/message\_loop.cc:310  

#28 MessageLoop::Run (this=0x7ffff91a1a00) at base/message\_loop.cc:234  

#29 0x00007ffff59713d5 in base::Thread::ThreadMain (this=0x7ffff9031870) at base/threading/thread.cc:164  

#30 0x00007ffff5970932 in base::(anonymous namespace)::ThreadFunc (params=<value optimized out>) at base/threading/platform\_thread\_posix.cc:51  

#31 0x00007ffff0fb7971 in start\_thread (arg=<value optimized out>) at pthread\_create.c:304  

#32 0x00007fffee89492d in clone () at ../sysdeps/unix/sysv/linux/x86\_64/clone.S:112  

#33 0x0000000000000000 in ?? ()

(gdb) i r  

rax 0x7ffff91b5400 140737372705792  

rbx 0x7ffff91a1a00 140737372625408  

rcx 0x7ffff9198140 140737372586304  

rdx 0x7ffff90e8fc0 140737371869120  

rsi 0x7ffff848ee00 140737358917120  

rdi 0x7ffff91a1a00 140737372625408  

rbp 0x7ffff848ee00 0x7ffff848ee00  

rsp 0x7fffdf10f108 0x7fffdf10f108  

r8 0x40 64  

r9 0x7fffdf10f220 140736935817760  

r10 0x7ffff90ac4e0 140737371620576  

r11 0x7fffee833c53 140737194966099  

r12 0x7fffdf10f3c0 140736935818176  

r13 0x0 0  

r14 0x0 0  

r15 0x7fffdf10fc30 140736935820336  

rip 0x4 0x4  

eflags 0x10246 [ PF ZF IF RF ]  

cs 0x33 51  

ss 0x2b 43  

ds 0x0 0  

es 0x0 0  

fs 0x0 0  

gs 0x0 0

(gdb) disas  

No function contains program counter for selected frame.  

(gdb) up  

#1 0x00007ffff65f5335 in WebCore::Element::getAttribute (this=0x7ffff91a1a00, name="href") at third\_party/WebKit/Source/WebCore/dom/Element.cpp:231  

231 third\_party/WebKit/Source/WebCore/dom/Element.cpp: No such file or directory.  

in third\_party/WebKit/Source/WebCore/dom/Element.cpp  

(gdb) disas  

Dump of assembler code for function WebCore::Element::getAttribute(WebCore::QualifiedName const&) const:  

0x00007ffff65f5270 <+0>: push %rbp  

0x00007ffff65f5271 <+1>: mov %rsi,%rbp  

0x00007ffff65f5274 <+4>: push %rbx  

0x00007ffff65f5275 <+5>: mov %rdi,%rbx  

0x00007ffff65f5278 <+8>: sub $0x8,%rsp  

0x00007ffff65f527c <+12>: mov 0x1e09b9d(%rip),%rax # 0x7ffff83fee20  

0x00007ffff65f5283 <+19>: mov (%rax),%rdx  

0x00007ffff65f5286 <+22>: cmp %rdx,(%rsi)  

0x00007ffff65f5289 <+25>: je 0x7ffff65f533a <WebCore::Element::getAttribute(WebCore::QualifiedName const&) const+202>  

0x00007ffff65f528f <+31>: mov 0x48(%rbx),%eax  

0x00007ffff65f5292 <+34>: test $0x400000,%eax  

0x00007ffff65f5297 <+39>: je 0x7ffff65f5326 <WebCore::Element::getAttribute(WebCore::QualifiedName const&) const+182>  

0x00007ffff65f529d <+45>: mov 0x68(%rbx),%rax  

0x00007ffff65f52a1 <+49>: test %rax,%rax  

0x00007ffff65f52a4 <+52>: je 0x7ffff65f5318 <WebCore::Element::getAttribute(WebCore::QualifiedName const&) const+168>  

0x00007ffff65f52a6 <+54>: mov 0x18(%rax),%r8d  

0x00007ffff65f52aa <+58>: test %r8d,%r8d  

0x00007ffff65f52ad <+61>: je 0x7ffff65f5318 <WebCore::Element::getAttribute(WebCore::QualifiedName const&) const+168>  

0x00007ffff65f52af <+63>: mov 0x20(%rax),%rdi  

0x00007ffff65f52b3 <+67>: mov 0x0(%rbp),%rsi  

0x00007ffff65f52b7 <+71>: mov (%rdi),%rax  

0x00007ffff65f52ba <+74>: mov 0x8(%rax),%rdx  

0x00007ffff65f52be <+78>: cmp %rsi,%rdx  

0x00007ffff65f52c1 <+81>: je 0x7ffff65f52ef <WebCore::Element::getAttribute(WebCore::QualifiedName const&) const+127>  

0x00007ffff65f52c3 <+83>: mov 0x10(%rsi),%rbp  

0x00007ffff65f52c7 <+87>: mov $0x8,%ecx  

0x00007ffff65f52cc <+92>: xor %ebx,%ebx  

0x00007ffff65f52ce <+94>: xchg %ax,%ax  

0x00007ffff65f52d0 <+96>: cmp %rbp,0x10(%rdx)  

0x00007ffff65f52d4 <+100>: je 0x7ffff65f5300 <WebCore::Element::getAttribute(WebCore::QualifiedName const&) const+144>  

0x00007ffff65f52d6 <+102>: add $0x1,%ebx  

0x00007ffff65f52d9 <+105>: cmp %ebx,%r8d  

0x00007ffff65f52dc <+108>: jbe 0x7ffff65f5318 <WebCore::Element::getAttribute(WebCore::QualifiedName const&) const+168>  

0x00007ffff65f52de <+110>: mov (%rdi,%rcx,1),%rax  

0x00007ffff65f52e2 <+114>: add $0x8,%rcx  

0x00007ffff65f52e6 <+118>: mov 0x8(%rax),%rdx  

0x00007ffff65f52ea <+122>: cmp %rsi,%rdx  

0x00007ffff65f52ed <+125>: jne 0x7ffff65f52d0 <WebCore::Element::getAttribute(WebCore::QualifiedName const&) const+96>  

0x00007ffff65f52ef <+127>: add $0x8,%rsp  

0x00007ffff65f52f3 <+131>: add $0x10,%rax  

0x00007ffff65f52f7 <+135>: pop %rbx  

0x00007ffff65f52f8 <+136>: pop %rbp  

0x00007ffff65f52f9 <+137>: retq  

0x00007ffff65f52fa <+138>: jmp 0x7ffff65f5300 <WebCore::Element::getAttribute(WebCore::QualifiedName const&) const+144>  

0x00007ffff65f52fc <+140>: nop  

0x00007ffff65f52fd <+141>: nop  

0x00007ffff65f52fe <+142>: nop  

0x00007ffff65f52ff <+143>: nop  

0x00007ffff65f5300 <+144>: mov 0x18(%rsi),%r9  

0x00007ffff65f5304 <+148>: cmp %r9,0x18(%rdx)  

0x00007ffff65f5308 <+152>: je 0x7ffff65f52ef <WebCore::Element::getAttribute(WebCore::QualifiedName const&) const+127>  

0x00007ffff65f530a <+154>: add $0x1,%ebx  

0x00007ffff65f530d <+157>: cmp %ebx,%r8d  

0x00007ffff65f5310 <+160>: ja 0x7ffff65f52de <WebCore::Element::getAttribute(WebCore::QualifiedName const&) const+110>  

0x00007ffff65f5312 <+162>: jmp 0x7ffff65f5318 <WebCore::Element::getAttribute(WebCore::QualifiedName const&) const+168>  

0x00007ffff65f5314 <+164>: nop  

0x00007ffff65f5315 <+165>: nop  

0x00007ffff65f5316 <+166>: nop  

0x00007ffff65f5317 <+167>: nop  

0x00007ffff65f5318 <+168>: mov 0x1e046c1(%rip),%rax # 0x7ffff83f99e0  

0x00007ffff65f531f <+175>: add $0x8,%rsp  

0x00007ffff65f5323 <+179>: pop %rbx  

0x00007ffff65f5324 <+180>: pop %rbp  

0x00007ffff65f5325 <+181>: retq  

0x00007ffff65f5326 <+182>: mov (%rbx),%rax  

0x00007ffff65f5329 <+185>: mov %rbp,%rsi  

0x00007ffff65f532c <+188>: mov %rbx,%rdi  

0x00007ffff65f532f <+191>: callq \*0x4a8(%rax)  

=> 0x00007ffff65f5335 <+197>: jmpq 0x7ffff65f529d <WebCore::Element::getAttribute(WebCore::QualifiedName const&) const+45>  

0x00007ffff65f533a <+202>: mov 0x48(%rdi),%eax  

0x00007ffff65f533d <+205>: test $0x100000,%eax  

0x00007ffff65f5342 <+210>: jne 0x7ffff65f5292 <WebCore::Element::getAttribute(WebCore::QualifiedName const&) const+34>  

0x00007ffff65f5348 <+216>: mov (%rdi),%rax  

0x00007ffff65f534b <+219>: jmp 0x7ffff65f5350 <WebCore::Element::getAttribute(WebCore::QualifiedName const&) const+224>  

0x00007ffff65f534d <+221>: nop  

0x00007ffff65f534e <+222>: nop  

0x00007ffff65f534f <+223>: nop  

0x00007ffff65f5350 <+224>: callq \*0x4a0(%rax)  

0x00007ffff65f5356 <+230>: jmpq 0x7ffff65f528f <WebCore::Element::getAttribute(WebCore::QualifiedName const&) const+31>  

End of assembler dump.  

(gdb)

## Attachments

- [small.html](attachments/small.html) (text/plain; charset=us-ascii, 703 B)
- [crbug71296.html](attachments/crbug71296.html) (text/plain; charset=us-ascii, 704 B)

## Timeline

### js...@chromium.org (2011-01-30)

The intersection of SVG use elements and animation--not a pretty place. This looks like another stale pointer with disallowed shadow tree elements. I'll take care of it Monday or Tuesday.

@miaubiz - Thanks for the bug and the detail, but I have one small request. I'd appreciate if you attached a file for the test case rather than paste a base64 data URL as a comment. And, as a general rule, it's usually preferable to attach files for any content longer than 10 lines or so (whether it's a repro file or a gdb listing). So, for example, it's nice to have the top ten lines of the gdb stack trace in the comment, and have the detailed listing as an attachment. It's not a big deal, but it makes our jobs a bit easier.

@inferno - Would you mind running this through the minimizer to see if it can be further reduced?


### in...@chromium.org (2011-01-30)

Reduced testcase::
<svg>
<g id="R">
<svg>
<linearGradient><animateTransform attributeName="a">
</g>
<use xlink:href="#R">

Iterators looks jacked up here, so that is why we hit an assert ASSERT(m_table) in debug.
void SVGDocumentExtensions::startAnimations()
{
    // FIXME: Eventually every "Time Container" will need a way to latch on to some global timer
    // starting animations for a document will do this "latching"
#if ENABLE(SVG_ANIMATION)    
    HashSet<SVGSVGElement*>::iterator end = m_timeContainers.end();
    for (HashSet<SVGSVGElement*>::iterator itr = m_timeContainers.begin(); itr != end; ++itr)
        (*itr)->timeContainer()->begin();
#endif
}

### sc...@gmail.com (2011-01-30)

@jschuh - I think you missed the "small.html" attachment in miaubiz's initial report?

### js...@chromium.org (2011-01-30)

So I did; though I guess that underscores the point. Codesite makes it easy to miss important details when dealing with really long comments. That, and the wrapping falls apart on long lines.


### js...@chromium.org (2011-01-30)

@inferno - Just got a debug build to test against running on my laptop. You're right; the stale pointer is obviously due to startAnimation having an open iterator on the stack. A recalcStyle causes the shadow tree to get pruned and that ends up calling removeTimeContainer, which removes an item from the HashSet we're currently iterating through. 

It's a really trivial fix. However, I need to trace the code and see if pauseAnimations and unpauseAnimations have a similar issue (although they don't appear to at first glance).


### js...@chromium.org (2011-01-30)

The pauseAnimations and unpauseAnimations methods use timers, so the iterations are safe. And the SVG root element is guaranteed to clear itself from m_timeContainers before deletion. So, we just need our own RefCounted vector as we're iterating.

I've pasted the fix below as a reminder to myself. I don't have my Mac build set up, so I'll just file the upstream bug, write the test, and submit the patch from work tomorrow.


Index: Source/WebCore/svg/SVGDocumentExtensions.cpp
===================================================================
--- Source/WebCore/svg/SVGDocumentExtensions.cpp	(revision 77069)
+++ Source/WebCore/svg/SVGDocumentExtensions.cpp	(working copy)
@@ -93,8 +93,10 @@
     // FIXME: Eventually every "Time Container" will need a way to latch on to some global timer
     // starting animations for a document will do this "latching"
 #if ENABLE(SVG_ANIMATION)    
-    HashSet<SVGSVGElement*>::iterator end = m_timeContainers.end();
-    for (HashSet<SVGSVGElement*>::iterator itr = m_timeContainers.begin(); itr != end; ++itr)
+    Vector<RefPtr<SVGSVGElement>> timeContainers;
+    timeContainers.appendRange(m_timeContainers.begin(), m_timeContainers.end());
+    Vector<RefPtr<SVGSVGElement> >::iterator end = timeContainers.end();
+    for (Vector<RefPtr<SVGSVGElement> >::iterator itr = timeContainers.begin(); itr != end; ++itr)
         (*itr)->timeContainer()->begin();
 #endif
 }





### mi...@gmail.com (2011-01-30)

@jschuh: point taken.  if I find anymore bugs I'll stick to that advice

is the minimizer in the repo?  I couldn't find it with git-gs or find.

### js...@chromium.org (2011-01-30)

@miaubiz - Thanks. I'd rather our bug tracker were less quirky, but until it is we certainly appreciate a little extra effort to make bugs as easy to follow as possible. As for the minimizer, it's something @inferno is working on, and not in the repo. Although, we'd like to eventually release it after it's a bit more polished and not so tied to our infrastructure. Your testcase was pretty minimal on its own, however, and would have been easy to work with regardless.

### js...@chromium.org (2011-01-31)

Filed upstream: https://bugs.webkit.org/show_bug.cgi?id=53458

Patch up for review.

### mi...@gmail.com (2011-02-03)

patch still not gone through :(

but I applied the one you posted in https://crbug.com/chromium/71296#c6 and recompiled and it stopped crashing for me.

### js...@chromium.org (2011-02-03)

@miaubiz - Yeah, the upstream owner of the code is reluctant to approve and I'm engaged in a bit of a debate to convince him that it's the right thing to do. If you have a bugs.webkit.org account I can CC you on it.

### js...@chromium.org (2011-02-04)

Landed upstream: http://trac.webkit.org/changeset/77548


### in...@chromium.org (2011-02-09)

merged to m10 in r78134.

merged to m9 in r78136.


### sc...@gmail.com (2011-02-13)

@miaubiz: nice report! And it provisionally qualifies for a $1000 Chromium Security Reward.

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

This issue was migrated from crbug.com/chromium/71296?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40087375)*
