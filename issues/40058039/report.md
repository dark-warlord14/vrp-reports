# Heap-use-after-free in WebCore::SVGTextLayoutEngine::layoutTextOnLineOrPath

| Field | Value |
|-------|-------|
| **Issue ID** | [40058039](https://issues.chromium.org/issues/40058039) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink, Blink>SVG |
| **Reporter** | ax...@gmail.com |
| **Assignee** | fm...@chromium.org |
| **Created** | 2012-05-09 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

Use-after-free can be triggered when trying to get attributes from freed SVG node.

**VERSION**  

Version 20.0.1132.0 (136016) (Ubuntu 10.10).  

Does not repro on 18.0.1025.168 m and 20.0.1131.0 canary (Windows7 x64).

**REPRODUCTION CASE**  

In attach.

# **FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**

==3315== ERROR: AddressSanitizer heap-use-after-free on address 0x7fe9c47a3928 at pc 0x7fe9d478a7a7 bp 0x7fff96340020 sp 0x7fff96340018  

READ of size 8 at 0x7fe9c47a3928 thread T0  

#0 0x7fe9d478a7a7 in WebCore::SVGTextLayoutAttributes::context() const ???:0  

#1 0x7fe9d47b5169 in WebCore::SVGTextLayoutEngine::currentLogicalCharacterAttributes(WebCore::SVGTextLayoutAttributes\*&) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/rendering/svg/SVGTextLayoutEngine.cpp:341  

#2 0x7fe9d47b30c1 in WebCore::SVGTextLayoutEngine::layoutTextOnLineOrPath(WebCore::SVGInlineTextBox\*, WebCore::RenderSVGInlineText\*, WebCore::RenderStyle const\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/rendering/svg/SVGTextLayoutEngine.cpp:466  

#3 0x7fe9d47b29d5 in WebCore::SVGTextLayoutEngine::layoutInlineTextBox(WebCore::SVGInlineTextBox\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/rendering/svg/SVGTextLayoutEngine.cpp:249  

#4 0x7fe9d47aa931 in WebCore::SVGRootInlineBox::layoutCharactersInTextBoxes(WebCore::InlineFlowBox\*, WebCore::SVGTextLayoutEngine&) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/rendering/svg/SVGRootInlineBox.cpp:105  

#5 0x7fe9d47aa6dd in WebCore::SVGRootInlineBox::computePerCharacterLayoutInformation() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/rendering/svg/SVGRootInlineBox.cpp:88  

#6 0x7fe9d4030932 in WebCore::RenderBlock::createLineBoxesFromBidiRuns(WebCore::BidiRunList[WebCore::BidiRun](javascript:void(0);)&, WebCore::InlineIterator const&, WebCore::LineInfo&, WebCore::VerticalPositionCache&, WebCore::BidiRun\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/rendering/RenderBlockLineLayout.cpp:1053  

#7 0x7fe9d4032d3d in WebCore::RenderBlock::layoutRunsAndFloatsInRange(WebCore::LineLayoutState&, WebCore::BidiResolver<WebCore::InlineIterator, WebCore::BidiRun>&, WebCore::InlineIterator const&, WebCore::BidiStatus const&, unsigned int) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/rendering/RenderBlockLineLayout.cpp:1294  

#8 0x7fe9d4030ef0 in WebCore::RenderBlock::layoutRunsAndFloats(WebCore::LineLayoutState&, bool) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/rendering/RenderBlockLineLayout.cpp:1218  

#9 0x7fe9d403b9ce in WebCore::RenderBlock::layoutInlineChildren(bool, WebCore::FractionalLayoutUnit&, WebCore::FractionalLayoutUnit&) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/rendering/RenderBlockLineLayout.cpp:1518  

#10 0x7fe9d478b220 in WebCore::RenderBlock::forceLayoutInlineChildren() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/rendering/RenderBlock.h:458  

#11 0x7fe9d478aeb1 in WebCore::RenderSVGText::layout() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/rendering/svg/RenderSVGText.cpp:322  

#12 0x7fe9d4793c96 in WebCore::SVGRenderSupport::layoutChildren(WebCore::RenderObject\*, bool) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/rendering/svg/SVGRenderSupport.cpp:213  

#13 0x7fe9d4784d8d in WebCore::RenderSVGRoot::layout() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/rendering/svg/RenderSVGRoot.cpp:234  

#14 0x7fe9d3c9753d in WebCore::FrameView::layout(bool) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/page/FrameView.cpp:1111  

#15 0x7fe9d3ca49f6 in WebCore::FrameView::updateLayoutAndStyleIfNeededRecursive() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/page/FrameView.cpp:3172  

#16 0x7fe9d3ca4a47 in WebCore::FrameView::updateLayoutAndStyleIfNeededRecursive() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/page/FrameView.cpp:3176  

#17 0x7fe9d2ed9a58 in WebKit::PageWidgetDelegate::layout(WebCore::Page\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebKit/chromium/src/PageWidgetDelegate.cpp:83  

#18 0x7fe9d2e7a170 in WebKit::WebViewImpl::layout() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebKit/chromium/src/WebViewImpl.cpp:1458  

#19 0x7fe9d59cade8 in RenderWidget::DoDeferredUpdate() /media/Chromium/chromium/depot\_tools/src/content/renderer/render\_widget.cc:872  

#20 0x7fe9d59d1a02 in RenderWidget::DoDeferredUpdateAndSendInputAck() /media/Chromium/chromium/depot\_tools/src/content/renderer/render\_widget.cc:824  

#21 0x7fe9d59ce206 in RenderWidget::OnUpdateRectAck() /media/Chromium/chromium/depot\_tools/src/content/renderer/render\_widget.cc:457  

#22 0x7fe9d59cd4e4 in bool IPC::Message::Dispatch<RenderWidget, RenderWidget>(IPC::Message const\*, RenderWidget\*, RenderWidget\*, void (RenderWidget::\*)()) /media/Chromium/chromium/depot\_tools/src/./ipc/ipc\_message.h:158  

#23 0x7fe9d59cccb8 in RenderWidget::OnMessageReceived(IPC::Message const&) /media/Chromium/chromium/depot\_tools/src/content/renderer/render\_widget.cc:238  

#24 0x7fe9d598efac in RenderViewImpl::OnMessageReceived(IPC::Message const&) /media/Chromium/chromium/depot\_tools/src/content/renderer/render\_view\_impl.cc:878  

#25 0x7fe9d29f7bed in MessageRouter::RouteMessage(IPC::Message const&) /media/Chromium/chromium/depot\_tools/src/content/common/message\_router.cc:46  

#26 0x7fe9d29f7b66 in MessageRouter::OnMessageReceived(IPC::Message const&) /media/Chromium/chromium/depot\_tools/src/content/common/message\_router.cc:39  

#27 0x7fe9d290fb43 in ChildThread::OnMessageReceived(IPC::Message const&) /media/Chromium/chromium/depot\_tools/src/content/common/child\_thread.cc:208  

#28 0x7fe9d1c78ef4 in IPC::ChannelProxy::Context::OnDispatchMessage(IPC::Message const&) /media/Chromium/chromium/depot\_tools/src/ipc/ipc\_channel\_proxy.cc:247  

#29 0x7fe9d1c7f9d8 in base::internal::InvokeHelper<false, void, base::internal::RunnableAdapter<void (IPC::ChannelProxy::Context::\*)(IPC::Message const&)>, void ()(IPC::ChannelProxy::Context\* const&, IPC::Message const&)>::MakeItSo(base::internal::RunnableAdapter<void (IPC::ChannelProxy::Context::\*)(IPC::Message const&)>, IPC::ChannelProxy::Context\* const&, IPC::Message const&) /media/Chromium/chromium/depot\_tools/src/./base/bind\_internal.h:897  

#30 0x7fe9d1b85493 in MessageLoop::RunTask(base::PendingTask const&) /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:459  

#31 0x7fe9d1b85bf9 in MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:470  

#32 0x7fe9d1b85f12 in MessageLoop::DoWork() /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:647  

#33 0x7fe9d1b92388 in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) /media/Chromium/chromium/depot\_tools/src/base/message\_pump\_default.cc:28  

#34 0x7fe9d1b84c8c in MessageLoop::RunInternal() /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:418  

#35 0x7fe9d1b83988 in MessageLoop::Run() /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:301  

#36 0x7fe9d59ebc91 in RendererMain(content::MainFunctionParams const&) /media/Chromium/chromium/depot\_tools/src/content/renderer/renderer\_main.cc:271  

#37 0x7fe9d1a6fe80 in (anonymous namespace)::RunZygote(content::MainFunctionParams const&, content::ContentMainDelegate\*) /media/Chromium/chromium/depot\_tools/src/content/app/content\_main\_runner.cc:255  

addr2line: '': No such file  

#38 0x7fe9d1a6f9d3 in (anonymous namespace)::RunNamedProcessTypeMain(std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, content::MainFunctionParams const&, content::ContentMainDelegate\*) /media/Chromium/chromium/depot\_tools/src/content/app/content\_main\_runner.cc:300  

#39 0x7fe9d1a6f3b0 in (anonymous namespace)::ContentMainRunnerImpl::Run() /media/Chromium/chromium/depot\_tools/src/content/app/content\_main\_runner.cc:550  

#40 0x7fe9d1a6e63f in content::ContentMain(int, char const\*\*, content::ContentMainDelegate\*) /media/Chromium/chromium/depot\_tools/src/content/app/content\_main.cc:35  

#41 0x7fe9d0807077 in ChromeMain /media/Chromium/chromium/depot\_tools/src/chrome/app/chrome\_main.cc:32  

#42 0x7fe9d0806fdb in main /media/Chromium/chromium/depot\_tools/src/chrome/app/chrome\_exe\_main\_gtk.cc:18  

#43 0x7fe9c96a6d8e in \_\_libc\_start\_main /build/buildd/eglibc-2.12.1/csu/libc-start.c:258  

0x7fe9c47a3928 is located 168 bytes inside of 224-byte region [0x7fe9c47a3880,0x7fe9c47a3960)  

freed by thread T0 here:  

#0 0x7fe9d6a8f4a2 in free ??:0  

#1 0x7fe9d2ff3ef9 in WebCore::Node::detach() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/Node.cpp:1355  

#2 0x7fe9d2f4d8f9 in WebCore::ContainerNode::detachChildren() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/ContainerNode.h:190  

#3 0x7fe9d2f4d87e in WebCore::ContainerNode::detach() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/ContainerNode.cpp:685  

#4 0x7fe9d307f5a5 in WebCore::ElementShadow::detach() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/ElementShadow.cpp:154  

#5 0x7fe9d307fb2d in WebCore::ElementShadow::detachHost(WebCore::Element\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/ElementShadow.cpp:164  

#6 0x7fe9d2fc6752 in WebCore::Element::detach() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/Element.cpp:1006  

#7 0x7fe9d2f4c330 in WebCore::ContainerNode::removeBetween(WebCore::Node\*, WebCore::Node\*, WebCore::Node\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/ContainerNode.cpp:430  

#8 0x7fe9d2f4be55 in WebCore::ContainerNode::removeChild(WebCore::Node\*, int&) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/ContainerNode.cpp:411  

#9 0x7fe9d2f4ab6b in WebCore::collectChildrenAndRemoveFromOldParent(WebCore::Node\*, WTF::Vector<WTF::RefPtr[WebCore::Node](javascript:void(0);), 11ul>&, int&) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/ContainerNode.cpp:82  

#10 0x7fe9d2f4a7f0 in WebCore::ContainerNode::appendChild(WTF::PassRefPtr[WebCore::Node](javascript:void(0);), int&, bool) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/ContainerNode.cpp:546  

#11 0x7fe9d2ff0a03 in WebCore::Node::appendChild(WTF::PassRefPtr[WebCore::Node](javascript:void(0);), int&, bool) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/Node.cpp:621  

#12 0x7fe9d38a3671 in WebCore::V8Node::appendChildCallback(v8::Arguments const&) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/bindings/v8/custom/V8NodeCustom.cpp:129  

#13 0x7fe9d23efd13 in v8::internal::MaybeObject\* v8::internal::HandleApiCallHelper<false>(v8::internal::(anonymous namespace)::BuiltinArguments<(v8::internal::BuiltinExtraArguments)1>, v8::internal::Isolate\*) /media/Chromium/chromium/depot\_tools/src/v8/src/builtins.cc:1115  

#14 0xe0b9c30618e in  

#15 0xe0b9c3472ba in  

#16 0xe0b9c324907 in  

#17 0xe0b9c311417 in  

#18 0x7fe9d242aebf in v8::internal::Invoke(bool, v8::internal::Handle[v8::internal::JSFunction](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*, bool\*) /media/Chromium/chromium/depot\_tools/src/v8/src/execution.cc:118  

#19 0x7fe9d23ba1ef in v8::Function::Call(v8::Handle[v8::Object](javascript:void(0);), int, v8::Handle[v8::Value](javascript:void(0);)\*) /media/Chromium/chromium/depot\_tools/src/v8/src/api.cc:3630  

#20 0x7fe9d3874761 in WebCore::V8Proxy::instrumentedCallFunction(WebCore::Frame\*, v8::Handle[v8::Function](javascript:void(0);), v8::Handle[v8::Object](javascript:void(0);), int, v8::Handle[v8::Value](javascript:void(0);)\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/bindings/v8/V8Proxy.cpp:417  

#21 0x7fe9d3874300 in WebCore::V8Proxy::callFunction(v8::Handle[v8::Function](javascript:void(0);), v8::Handle[v8::Object](javascript:void(0);), int, v8::Handle[v8::Value](javascript:void(0);)\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/bindings/v8/V8Proxy.cpp:387  

#22 0x7fe9d3dee8df in WebCore::ScheduledAction::execute(WebCore::V8Proxy\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/bindings/v8/ScheduledAction.cpp:133  

#23 0x7fe9d3c48d72 in WebCore::DOMTimer::fired() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/page/DOMTimer.cpp:149  

#24 0x7fe9d354c8a8 in WebCore::ThreadTimers::sharedTimerFiredInternal() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/platform/ThreadTimers.cpp:118  

#25 0x7fe9d4c3082d in base::internal::InvokeHelper<false, void, base::internal::RunnableAdapter<void (webkit\_glue::WebKitPlatformSupportImpl::\*)()>, void ()(webkit\_glue::WebKitPlatformSupportImpl\*)>::MakeItSo(base::internal::RunnableAdapter<void (webkit\_glue::WebKitPlatformSupportImpl::\*)()>, webkit\_glue::WebKitPlatformSupportImpl\*) /media/Chromium/chromium/depot\_tools/src/./base/bind\_internal.h:869  

#26 0x7fe9d4c3065d in base::internal::Invoker<1, base::internal::BindState<base::internal::RunnableAdapter<void (webkit\_glue::WebKitPlatformSupportImpl::\*)()>, void ()(webkit\_glue::WebKitPlatformSupportImpl\*), void ()(base::internal::UnretainedWrapper<webkit\_glue::WebKitPlatformSupportImpl>)>, void ()(webkit\_glue::WebKitPlatformSupportImpl\*)>::Run(base::internal::BindStateBase\*) /media/Chromium/chromium/depot\_tools/src/./base/bind\_internal.h:1170  

#27 0x7fe9d1c00bcd in base::Timer::RunScheduledTask() /media/Chromium/chromium/depot\_tools/src/base/timer.cc:182  

#28 0x7fe9d1c011bd in base::internal::InvokeHelper<false, void, base::internal::RunnableAdapter<void (base::BaseTimerTaskInternal::\*)()>, void ()(base::BaseTimerTaskInternal\*)>::MakeItSo(base::internal::RunnableAdapter<void (base::BaseTimerTaskInternal::\*)()>, base::BaseTimerTaskInternal\*) /media/Chromium/chromium/depot\_tools/src/./base/bind\_internal.h:869  

previously allocated by thread T0 here:  

#0 0x7fe9d6a8f562 in malloc ??:0  

#1 0x7fe9d488e3c2 in WebCore::SVGShadowText::createRenderer(WebCore::RenderArena\*, WebCore::RenderStyle\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/svg/SVGTRefElement.cpp:140  

#2 0x7fe9d30176df in WebCore::NodeRendererFactory::createRenderer() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/NodeRenderingContext.cpp:351  

#3 0x7fe9d3017a8c in WebCore::NodeRendererFactory::createRendererIfNeeded() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/NodeRenderingContext.cpp:397  

#4 0x7fe9d2ff3e86 in WebCore::Node::createRendererIfNeeded() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/Node.cpp:1431  

#5 0x7fe9d305315e in WebCore::Text::attach() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/Text.cpp:250  

#6 0x7fe9d2f4d839 in WebCore::ContainerNode::attachChildren() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/ContainerNode.h:156  

#7 0x7fe9d2f4d7ce in WebCore::ContainerNode::attach() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/ContainerNode.cpp:679  

#8 0x7fe9d304d3ad in WebCore::ShadowRoot::attach() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/ShadowRoot.cpp:206  

#9 0x7fe9d307f9f5 in WebCore::ElementShadow::attach() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/ElementShadow.cpp:138  

#10 0x7fe9d307fa4e in WebCore::ElementShadow::attachHost(WebCore::Element\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/ElementShadow.cpp:148  

#11 0x7fe9d2fc6401 in WebCore::Element::attach() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/Element.cpp:969  

#12 0x7fe9d4886a5e in WebCore::SVGStyledElement::attach() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/svg/SVGStyledElement.cpp:356  

#13 0x7fe9d3d422d0 in WebCore::XMLDocumentParser::startElementNs(unsigned char const\*, unsigned char const\*, unsigned char const\*, int, unsigned char const\*\*, int, int, unsigned char const\*\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/xml/parser/XMLDocumentParserLibxml2.cpp:814  

#14 0x7fe9d30ff077 in xmlParseStartTag2 /media/Chromium/chromium/depot\_tools/src/third\_party/libxml/src/parser.c:9126  

#15 0x7fe9d31094e3 in xmlParseTryOrFinish /media/Chromium/chromium/depot\_tools/src/third\_party/libxml/src/parser.c:10850  

#16 0x7fe9d3104d6c in xmlParseChunk /media/Chromium/chromium/depot\_tools/src/third\_party/libxml/src/parser.c:11625  

#17 0x7fe9d3d4120b in WebCore::XMLDocumentParser::doWrite(WTF::String const&) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/xml/parser/XMLDocumentParserLibxml2.cpp:661  

#18 0x7fe9d3d3e00f in ~RefPtr /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WTF/wtf/RefPtr.h:56  

#19 0x7fe9d627422e in WebCore::DecodedDataDocumentParser::appendBytes(WebCore::DocumentWriter\*, char const\*, unsigned long) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/DecodedDataDocumentParser.cpp:50  

#20 0x7fe9d3b95b53 in WebCore::DocumentLoader::commitData(char const\*, unsigned long) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/loader/DocumentLoader.cpp:350  

#21 0x7fe9d2ec2c7c in WebKit::FrameLoaderClientImpl::committedLoad(WebCore::DocumentLoader\*, char const\*, int) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebKit/chromium/src/FrameLoaderClientImpl.cpp:1118  

#22 0x7fe9d3b95c9b in void WTF::derefIfNotNull[WebCore::DocumentLoader](javascript:void(0);)(WebCore::DocumentLoader\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WTF/wtf/PassRefPtr.h:52  

==3315== ABORTING  

Stats: 33M malloced (28M for red zones) by 65814 calls  

Stats: 1M realloced by 1777 calls  

Stats: 29M freed by 53650 calls  

Stats: 0M really freed by 0 calls  

Stats: 92M (23566 full pages) mmaped in 23 calls  

mmaps by size class: 8:65532; 9:16382; 10:8190; 11:2047; 12:1024; 13:1024; 14:256; 15:128; 16:128; 17:64; 18:16; 19:8; 21:6;  

mallocs by size class: 8:50154; 9:7474; 10:5632; 11:1020; 12:284; 13:898; 14:72; 15:115; 16:114; 17:36; 18:3; 19:7; 21:5;  

frees by size class: 8:39610; 9:6736; 10:5261; 11:690; 12:183; 13:866; 14:56; 15:107; 16:107; 17:19; 18:3; 19:7; 21:5;  

rfrees by size class:  

Stats: malloc large: 51 small slow: 363  

Shadow byte and word:  

0x1ffd388f4725: fd  

0x1ffd388f4720: fd fd fd fd fd fd fd fd  

More shadow bytes:  

0x1ffd388f4700: fa fa fa fa fa fa fa fa  

0x1ffd388f4708: fa fa fa fa fa fa fa fa  

0x1ffd388f4710: fd fd fd fd fd fd fd fd  

0x1ffd388f4718: fd fd fd fd fd fd fd fd  

=>0x1ffd388f4720: fd fd fd fd fd fd fd fd  

0x1ffd388f4728: fd fd fd fd fd fd fd fd  

0x1ffd388f4730: fa fa fa fa fa fa fa fa  

0x1ffd388f4738: fa fa fa fa fa fa fa fa  

0x1ffd388f4740: fa fa fa fa fa fa fa fa

## Attachments

- [09-05-2012-uaf.zip](attachments/09-05-2012-uaf.zip) (application/zip; charset=binary, 618 B)

## Timeline

### in...@chromium.org (2012-05-09)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=44908125

Uploader: inferno@chromium.org

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x7f9c6c2dc128
Crash State:
  - crash stack -
  WebCore::SVGTextLayoutEngine::layoutTextOnLineOrPath
  WebCore::SVGTextLayoutEngine::layoutInlineTextBox
  - free stack -
  WebCore::Node::detach
  WebCore::ContainerNode::detach
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=136004:136013

Minimized Testcase (0.50 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96WonT13R0t4BCfS_bMattEntVyJbv4tyn020KMH33e_z0eHfbQEabhthkaHpYbybF3Z3gLpi5I59Cx_SBlGaVSPT32Fm_3MEnnE5KndimZrtB1-qa-a5FapfPK8jDFriRqb60NsjqWg4VLvIAWL8H4TOC3Tw

### in...@chromium.org (2012-05-09)

What the heck is happening in svg land these days, regressions all over the place.

### pd...@chromium.org (2012-05-09)

Sigh...

@fmalita, do you have room on your plate for this one?

### fm...@chromium.org (2012-05-09)

Sure (for some loose definition of "plate"... and "room" :)

### in...@chromium.org (2012-05-09)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-05-11)

Thanks for all your efforts. We should definitely try to prevent these regressions from touching stable.

### in...@chromium.org (2012-05-11)

upstream - https://bugs.webkit.org/show_bug.cgi?id=86166. Stephen has a patch.

### fm...@chromium.org (2012-05-11)

Cool - I assume we'll get a confirmation from ClusterFuzz if that fixes it.

It's definitely in the same space, but since I haven't been able to trigger this (timing/ASAN/--single-process?), I've been investigating based solely on the stack traces so I can't be 100 certain.

### fm...@chromium.org (2012-05-11)

I was able to repro this with an ASAN build, and unfortunately https://bugs.webkit.org/show_bug.cgi?id=86166 doesn't seem to fix it.

One observation is that this appears to be a race condition: initially I had some debug messages instrumented in the code and the problem was not triggering even with ASAN. After removing my instrumentation, it popped right up. The proverbial heisenbug :)

### in...@chromium.org (2012-05-11)

Fixed by rollout - http://trac.webkit.org/changeset/116801.

Keeping in merge approved so that we can see what went in m20 and also remember to uptake upstream fix if needed instead of the rollout fix.

Two security bugs introduced by Niko are
https://bugs.webkit.org/show_bug.cgi?id=86166
https://bugs.webkit.org/show_bug.cgi?id=86253


### cl...@chromium.org (2012-05-12)

ClusterFuzz has detected this issue as fixed in range 136724:136736.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=44908125

Uploader: inferno@chromium.org

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x7f9c6c2dc128
Crash State:
  - crash stack -
  WebCore::SVGTextLayoutEngine::layoutTextOnLineOrPath
  WebCore::SVGTextLayoutEngine::layoutInlineTextBox
  - free stack -
  WebCore::Node::detach
  WebCore::ContainerNode::detach
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=136004:136013
Fixed: https://cluster-fuzz.appspot.com/revisions?range=136724:136736

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv96WonT13R0t4BCfS_bMattEntVyJbv4tyn020KMH33e_z0eHfbQEabhthkaHpYbybF3Z3gLpi5I59Cx_SBlGaVSPT32Fm_3MEnnE5KndimZrtB1-qa-a5FapfPK8jDFriRqb60NsjqWg4VLvIAWL8H4TOC3Tw

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### sc...@chromium.org (2012-05-15)

Current patch up here fixes this: https://bugs.webkit.org/show_bug.cgi?id=83405

I just going through and looking at all of the bugs that are affected by the aforementioned patch.

### in...@chromium.org (2012-05-16)

looks like new fix http://trac.webkit.org/changeset/117225 is in place. when the webkit rolls in chromium, Florin, can you please verify the fix using an asanified build from https://commondatastorage.googleapis.com/chromium-browser-asan/index.html. i think there was this one security bug and some other sites that Philip pointed.

### fm...@chromium.org (2012-05-16)

Verified: the ASAN build @137414 (WK fix rolled in @137405) no longer triggers a use-after-free.

### in...@chromium.org (2012-05-16)

Thanks a lot.

### sc...@chromium.org (2012-05-16)

Note there's a comment on WebKit b83405 that has the 3 Chromium security fixes that I verified were fixed using an Asan Release Chrome build. So no need for anyone to go back and verify again.

### in...@chromium.org (2012-05-16)

Sorry Stephen, missed to see that one.

### sc...@gmail.com (2012-05-18)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-05-23)

Thanks Arthur, your testcase was helpful independently of other efforts to stomp this regression. So $1000.

### sc...@gmail.com (2012-05-30)

Merged webkit 117225 to M20: http://trac.webkit.org/changeset/118875

### sc...@gmail.com (2012-07-09)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### js...@chromium.org (2012-12-20)

[Empty comment from Monorail migration]

### la...@google.com (2013-01-18)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-14)

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

### sh...@chromium.org (2016-06-22)

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

This issue was migrated from crbug.com/chromium/127418?no_tracker_redirect=1

[Multiple monorail components: Blink, Blink>SVG]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058039)*
