# Heap-use-after-free in WebCore::StyleResolver::collectMatchingRulesForList

| Field | Value |
|-------|-------|
| **Issue ID** | [40060927](https://issues.chromium.org/issues/40060927) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | ax...@gmail.com |
| **Assignee** | ds...@chromium.org |
| **Created** | 2012-07-07 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

Heap-use-after-free happens when trying to enumerate Rules after CSSStyleSheet Rule was deleted.

**VERSION**  

Stable 20.0.1132.47 m Win7 x64  

Version 20.0.1091.0 (130362) Ubuntu 11.10  

Version 22.0.1192.0 (145068) Ubuntu 10.10  

22.0.1199.0 canary Win7 x64

=================================================================  

==6506== ERROR: AddressSanitizer heap-use-after-free on address 0x7f2fcaaba488 at pc 0x7f2fde707617 bp 0x7fffc74fad80 sp 0x7fffc74fad78  

READ of size 8 at 0x7f2fcaaba488 thread T0  

#0 0x7f2fde707617 in WTF::RefPtr[WebCore::StylePropertySet](javascript:void(0);)::get() const ???:0  

#1 0x7f2fdf13519f in WebCore::StyleResolver::collectMatchingRulesForList(WTF::Vector<WebCore::RuleData, 0ul> const\*, int&, int&, WebCore::StyleResolver::MatchOptions const&) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/css/StyleResolver.cpp:1091  

#2 0x7f2fdf13669b in WebCore::StyleResolver::matchAuthorRules(WebCore::StyleResolver::MatchResult&, bool) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/css/StyleResolver.cpp:993  

#3 0x7f2fdf13768a in WebCore::StyleResolver::matchAllRules(WebCore::StyleResolver::MatchResult&, bool) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/css/StyleResolver.cpp:1165  

#4 0x7f2fdf1301b1 in WebCore::StyleResolver::styleForElement(WebCore::Element\*, WebCore::RenderStyle\*, WebCore::StyleSharingBehavior, WebCore::RuleMatchingBehavior, WebCore::RenderRegion\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/css/StyleResolver.cpp:1752  

#5 0x7f2fde6ff8c4 in WebCore::Element::styleForRenderer() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/Element.cpp:1033  

#6 0x7f2fde6ffbf2 in WebCore::Element::recalcStyle(WebCore::Node::StyleChange) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/Element.cpp:1057  

#7 0x7f2fde6ffe33 in WebCore::Element::recalcStyle(WebCore::Node::StyleChange) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/Element.cpp:1149  

#8 0x7f2fde6ffe33 in WebCore::Element::recalcStyle(WebCore::Node::StyleChange) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/Element.cpp:1149  

#9 0x7f2fde6ffe33 in WebCore::Element::recalcStyle(WebCore::Node::StyleChange) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/Element.cpp:1149  

#10 0x7f2fde6ffe33 in WebCore::Element::recalcStyle(WebCore::Node::StyleChange) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/Element.cpp:1149  

#11 0x7f2fde6a9845 in WebCore::Document::recalcStyle(WebCore::Node::StyleChange) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/Document.cpp:1812  

#12 0x7f2fde6aaa72 in WebCore::Document::updateStyleIfNeeded() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/Document.cpp:1861  

#13 0x7f2fdf44721d in WebCore::FrameView::updateLayoutAndStyleIfNeededRecursive() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/page/FrameView.cpp:3168  

#14 0x7f2fdf447287 in WebCore::FrameView::updateLayoutAndStyleIfNeededRecursive() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/page/FrameView.cpp:3178  

#15 0x7f2fde629408 in WebKit::PageWidgetDelegate::layout(WebCore::Page\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebKit/chromium/src/PageWidgetDelegate.cpp:83  

#16 0x7f2fde5c91a0 in WebKit::WebViewImpl::layout() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebKit/chromium/src/WebViewImpl.cpp:1581  

#17 0x7f2fe136ab8d in RenderWidget::DoDeferredUpdate() /media/Chromium/chromium/depot\_tools/src/content/renderer/render\_widget.cc:855  

#18 0x7f2fe13720a2 in RenderWidget::DoDeferredUpdateAndSendInputAck() /media/Chromium/chromium/depot\_tools/src/content/renderer/render\_widget.cc:807  

#19 0x7f2fe136e36a in RenderWidget::OnUpdateRectAck() /media/Chromium/chromium/depot\_tools/src/content/renderer/render\_widget.cc:452  

#20 0x7f2fe136d614 in bool IPC::Message::Dispatch<RenderWidget, RenderWidget>(IPC::Message const\*, RenderWidget\*, RenderWidget\*, void (RenderWidget::\*)()) /media/Chromium/chromium/depot\_tools/src/./ipc/ipc\_message.h:154  

#21 0x7f2fe136cba8 in RenderWidget::OnMessageReceived(IPC::Message const&) /media/Chromium/chromium/depot\_tools/src/content/renderer/render\_widget.cc:229  

#22 0x7f2fe132aceb in RenderViewImpl::OnMessageReceived(IPC::Message const&) /media/Chromium/chromium/depot\_tools/src/content/renderer/render\_view\_impl.cc:966  

#23 0x7f2fde10666d in MessageRouter::RouteMessage(IPC::Message const&) /media/Chromium/chromium/depot\_tools/src/content/common/message\_router.cc:47  

#24 0x7f2fde1065e6 in MessageRouter::OnMessageReceived(IPC::Message const&) /media/Chromium/chromium/depot\_tools/src/content/common/message\_router.cc:40  

#25 0x7f2fde016633 in ChildThread::OnMessageReceived(IPC::Message const&) /media/Chromium/chromium/depot\_tools/src/content/common/child\_thread.cc:208  

#26 0x7f2fdd307a77 in IPC::ChannelProxy::Context::OnDispatchMessage(IPC::Message const&) /media/Chromium/chromium/depot\_tools/src/ipc/ipc\_channel\_proxy.cc:250  

#27 0x7f2fdd30e568 in base::internal::InvokeHelper<false, void, base::internal::RunnableAdapter<void (IPC::ChannelProxy::Context::\*)(IPC::Message const&)>, void ()(IPC::ChannelProxy::Context\* const&, IPC::Message const&)>::MakeItSo(base::internal::RunnableAdapter<void (IPC::ChannelProxy::Context::\*)(IPC::Message const&)>, IPC::ChannelProxy::Context\* const&, IPC::Message const&) /media/Chromium/chromium/depot\_tools/src/./base/bind\_internal.h:897  

#28 0x7f2fdd20b263 in MessageLoop::RunTask(base::PendingTask const&) /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:456  

#29 0x7f2fdd20b9cd in MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:467  

#30 0x7f2fdd20bce2 in MessageLoop::DoWork() /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:643  

#31 0x7f2fdd217d58 in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) /media/Chromium/chromium/depot\_tools/src/base/message\_pump\_default.cc:28  

#32 0x7f2fdd20aa5c in MessageLoop::RunInternal() /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:415  

#33 0x7f2fdd244c53 in base::RunLoop::Run() /media/Chromium/chromium/depot\_tools/src/base/run\_loop.cc:46  

#34 0x7f2fdd209797 in MessageLoop::Run() /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:299  

#35 0x7f2fe138d628 in RendererMain(content::MainFunctionParams const&) /media/Chromium/chromium/depot\_tools/src/content/renderer/renderer\_main.cc:270  

#36 0x7f2fdd0ec66b in content::RunZygote(content::MainFunctionParams const&, content::ContentMainDelegate\*) /media/Chromium/chromium/depot\_tools/src/content/app/content\_main\_runner.cc:327  

#37 0x7f2fdd0ed113 in content::RunNamedProcessTypeMain(std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, content::MainFunctionParams const&, content::ContentMainDelegate\*) /media/Chromium/chromium/depot\_tools/src/content/app/content\_main\_runner.cc:380  

#38 0x7f2fdd0ede50 in content::ContentMainRunnerImpl::Run() /media/Chromium/chromium/depot\_tools/src/content/app/content\_main\_runner.cc:627  

#39 0x7f2fdd0ebddf in content::ContentMain(int, char const\*\*, content::ContentMainDelegate\*) /media/Chromium/chromium/depot\_tools/src/content/app/content\_main.cc:35  

#40 0x7f2fdbdaab47 in ChromeMain /media/Chromium/chromium/depot\_tools/src/chrome/app/chrome\_main.cc:32  

#41 0x7f2fdbdaaaab in main /media/Chromium/chromium/depot\_tools/src/chrome/app/chrome\_exe\_main\_gtk.cc:18  

#42 0x7f2fd4bb0d8e in \_\_libc\_start\_main /build/buildd/eglibc-2.12.1/csu/libc-start.c:258  

0x7f2fcaaba488 is located 8 bytes inside of 24-byte region [0x7f2fcaaba480,0x7f2fcaaba498)  

freed by thread T0 here:  

#0 0x7f2fe24aa642 in operator delete(void\*) ??:0  

#1 0x7f2fdf17fcd3 in WTF::Vector<WTF::RefPtr[WebCore::StyleRuleBase](javascript:void(0);), 0ul>::remove(unsigned long) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WTF/wtf/Vector.h:1129  

addr2line: '': No such file  

#2 0x7f2fdf0ef32a in WebCore::CSSStyleSheet::deleteRule(unsigned int, int&) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/css/CSSStyleSheet.cpp:271  

#3 0x7f2fdfd6a5fa in WebCore::CSSStyleSheetV8Internal::deleteRuleCallback(v8::Arguments const&) /media/Chromium/chromium/depot\_tools/src/out/Release/obj/gen/webcore/bindings/V8CSSStyleSheet.cpp:113  

#4 0x7f2fddabcdc1 in v8::internal::MaybeObject\* v8::internal::HandleApiCallHelper<false>(v8::internal::(anonymous namespace)::BuiltinArguments<(v8::internal::BuiltinExtraArguments)1>, v8::internal::Isolate\*) /media/Chromium/chromium/depot\_tools/src/v8/src/builtins.cc:1145  

#5 0xe5141d0618e in  

#6 0xe5141d468e6 in  

#7 0xe5141d23be7 in  

#8 0xe5141d11377 in  

#9 0x7f2fddb012bf in v8::internal::Invoke(bool, v8::internal::Handle[v8::internal::JSFunction](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*, bool\*) /media/Chromium/chromium/depot\_tools/src/v8/src/execution.cc:118  

#10 0x7f2fdda868cf in v8::Function::Call(v8::Handle[v8::Object](javascript:void(0);), int, v8::Handle[v8::Value](javascript:void(0);)\*) /media/Chromium/chromium/depot\_tools/src/v8/src/api.cc:3655  

#11 0x7f2fdefe5f60 in WebCore::V8Proxy::instrumentedCallFunction(WebCore::Frame\*, v8::Handle[v8::Function](javascript:void(0);), v8::Handle[v8::Object](javascript:void(0);), int, v8::Handle[v8::Value](javascript:void(0);)\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/bindings/v8/V8Proxy.cpp:441  

#12 0x7f2fdefe5af0 in WebCore::V8Proxy::callFunction(v8::Handle[v8::Function](javascript:void(0);), v8::Handle[v8::Object](javascript:void(0);), int, v8::Handle[v8::Value](javascript:void(0);)\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/bindings/v8/V8Proxy.cpp:390  

#13 0x7f2fdf5b197f in WebCore::ScheduledAction::execute(WebCore::V8Proxy\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/bindings/v8/ScheduledAction.cpp:133  

#14 0x7f2fdf3ea372 in WebCore::DOMTimer::fired() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/page/DOMTimer.cpp:149  

#15 0x7f2fdeca5be8 in WebCore::ThreadTimers::sharedTimerFiredInternal() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/platform/ThreadTimers.cpp:118  

#16 0x7f2fe048799d in base::internal::InvokeHelper<false, void, base::internal::RunnableAdapter<void (webkit\_glue::WebKitPlatformSupportImpl::\*)()>, void ()(webkit\_glue::WebKitPlatformSupportImpl\*)>::MakeItSo(base::internal::RunnableAdapter<void (webkit\_glue::WebKitPlatformSupportImpl::\*)()>, webkit\_glue::WebKitPlatformSupportImpl\*) /media/Chromium/chromium/depot\_tools/src/./base/bind\_internal.h:869  

#17 0x7f2fe04877cd in base::internal::Invoker<1, base::internal::BindState<base::internal::RunnableAdapter<void (webkit\_glue::WebKitPlatformSupportImpl::\*)()>, void ()(webkit\_glue::WebKitPlatformSupportImpl\*), void ()(base::internal::UnretainedWrapper<webkit\_glue::WebKitPlatformSupportImpl>)>, void ()(webkit\_glue::WebKitPlatformSupportImpl\*)>::Run(base::internal::BindStateBase\*) /media/Chromium/chromium/depot\_tools/src/./base/bind\_internal.h:1170  

#18 0x7f2fdd28af5d in base::Timer::RunScheduledTask() /media/Chromium/chromium/depot\_tools/src/base/timer.cc:184  

#19 0x7f2fdd28b54d in base::internal::InvokeHelper<false, void, base::internal::RunnableAdapter<void (base::BaseTimerTaskInternal::\*)()>, void ()(base::BaseTimerTaskInternal\*)>::MakeItSo(base::internal::RunnableAdapter<void (base::BaseTimerTaskInternal::\*)()>, base::BaseTimerTaskInternal\*) /media/Chromium/chromium/depot\_tools/src/./base/bind\_internal.h:869  

#20 0x7f2fdd28b408 in base::internal::Invoker<1, base::internal::BindState<base::internal::RunnableAdapter<void (base::BaseTimerTaskInternal::\*)()>, void ()(base::BaseTimerTaskInternal\*), void ()(base::internal::OwnedWrapper[base::BaseTimerTaskInternal](javascript:void(0);))>, void ()(base::BaseTimerTaskInternal\*)>::Run(base::internal::BindStateBase\*) /media/Chromium/chromium/depot\_tools/src/./base/bind\_internal.h:1170  

#21 0x7f2fdd20b263 in MessageLoop::RunTask(base::PendingTask const&) /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:456  

#22 0x7f2fdd20b9cd in MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:467  

#23 0x7f2fdd20bce2 in MessageLoop::DoWork() /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:643  

#24 0x7f2fdd217d58 in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) /media/Chromium/chromium/depot\_tools/src/base/message\_pump\_default.cc:28  

#25 0x7f2fdd20aa5c in MessageLoop::RunInternal() /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:415  

#26 0x7f2fdd244c53 in base::RunLoop::Run() /media/Chromium/chromium/depot\_tools/src/base/run\_loop.cc:46  

#27 0x7f2fdd209797 in MessageLoop::Run() /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:299  

#28 0x7f2fe138d628 in RendererMain(content::MainFunctionParams const&) /media/Chromium/chromium/depot\_tools/src/content/renderer/renderer\_main.cc:270  

previously allocated by thread T0 here:  

#0 0x7f2fe24aa4c2 in operator new(unsigned long) ??:0  

#1 0x7f2fdf0b53aa in WebCore::StyleRule::create(int) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/css/StyleRule.h:92  

#2 0x7f2fdf0b50b8 in WebCore::CSSParser::createStyleRule(WTF::Vector<WTF::OwnPtr[WebCore::CSSParserSelector](javascript:void(0);), 0ul>\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/css/CSSParser.cpp:9475  

#3 0x7f2fdff0fa32 in cssyyparse(void\*) /media/Chromium/chromium/src/third\_party/WebKit/Source/WebCore/css/CSSGrammar.y:919  

#4 0x7f2fdf071abc in WebCore::CSSParser::parseSheet(WebCore::StyleSheetContents\*, WTF::String const&, int, WTF::Vector<WTF::RefPtr[WebCore::CSSRuleSourceData](javascript:void(0);), 0ul>\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/css/CSSParser.cpp:330  

#5 0x7f2fdf1836b2 in WebCore::StyleSheetContents::parseStringAtLine(WTF::String const&, int) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/css/StyleSheetContents.cpp:311  

#6 0x7f2fdf18361b in WebCore::StyleSheetContents::parseString(WTF::String const&) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/css/StyleSheetContents.cpp:302  

#7 0x7f2fde7514e7 in WebCore::ProcessingInstruction::parseStyleSheet(WTF::String const&) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/ProcessingInstruction.cpp:244  

#8 0x7f2fde751144 in ~RefPtr /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WTF/wtf/RefPtr.h:56  

#9 0x7f2fdf3a6b3c in ~RefPtr /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WTF/wtf/RefPtr.h:56  

#10 0x7f2fdf3a68c4 in WebCore::CachedCSSStyleSheet::data(WTF::PassRefPtr[WebCore::SharedBuffer](javascript:void(0);), bool) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/loader/cache/CachedCSSStyleSheet.cpp:112  

#11 0x7f2fdf3932de in WebCore::SubresourceLoader::didFinishLoading(double) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/loader/SubresourceLoader.cpp:278  

#12 0x7f2fe0497e01 in webkit\_glue::WebURLLoaderImpl::Context::OnCompletedRequest(net::URLRequestStatus const&, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, base::TimeTicks const&) /media/Chromium/chromium/depot\_tools/src/webkit/glue/weburlloader\_impl.cc:665  

#13 0x7f2fde11af87 in ResourceDispatcher::OnRequestComplete(int, net::URLRequestStatus const&, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, base::TimeTicks const&) /media/Chromium/chromium/depot\_tools/src/content/common/resource\_dispatcher.cc:478  

#14 0x7f2fde11c282 in bool ResourceMsg\_RequestComplete::Dispatch<ResourceDispatcher, ResourceDispatcher, void (ResourceDispatcher::\*)(int, net::URLRequestStatus const&, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, base::TimeTicks const&)>(IPC::Message const\*, ResourceDispatcher\*, ResourceDispatcher\*, void (ResourceDispatcher::\*)(int, net::URLRequestStatus const&, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, base::TimeTicks const&)) /media/Chromium/chromium/depot\_tools/src/./content/common/resource\_messages.h:172  

#15 0x7f2fde118a08 in ResourceDispatcher::DispatchMessage(IPC::Message const&) /media/Chromium/chromium/depot\_tools/src/content/common/resource\_dispatcher.cc:548  

#16 0x7f2fde117e97 in ResourceDispatcher::OnMessageReceived(IPC::Message const&) /media/Chromium/chromium/depot\_tools/src/content/common/resource\_dispatcher.cc:315  

#17 0x7f2fde016322 in ChildThread::OnMessageReceived(IPC::Message const&) /media/Chromium/chromium/depot\_tools/src/content/common/child\_thread.cc:174  

#18 0x7f2fdd307a77 in IPC::ChannelProxy::Context::OnDispatchMessage(IPC::Message const&) /media/Chromium/chromium/depot\_tools/src/ipc/ipc\_channel\_proxy.cc:250  

#19 0x7f2fdd30e568 in base::internal::InvokeHelper<false, void, base::internal::RunnableAdapter<void (IPC::ChannelProxy::Context::\*)(IPC::Message const&)>, void ()(IPC::ChannelProxy::Context\* const&, IPC::Message const&)>::MakeItSo(base::internal::RunnableAdapter<void (IPC::ChannelProxy::Context::\*)(IPC::Message const&)>, IPC::ChannelProxy::Context\* const&, IPC::Message const&) /media/Chromium/chromium/depot\_tools/src/./base/bind\_internal.h:897  

#20 0x7f2fdd20b263 in MessageLoop::RunTask(base::PendingTask const&) /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:456  

#21 0x7f2fdd20b9cd in MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:467  

#22 0x7f2fdd20bce2 in MessageLoop::DoWork() /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:643  

#23 0x7f2fdd217d58 in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) /media/Chromium/chromium/depot\_tools/src/base/message\_pump\_default.cc:28  

#24 0x7f2fdd20aa5c in MessageLoop::RunInternal() /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:415  

==6506== ABORTING  

Stats: 9M malloced (11M for red zones) by 22122 calls  

Stats: 0M realloced by 111 calls  

Stats: 7M freed by 12713 calls  

Stats: 0M really freed by 0 calls  

Stats: 56M (14345 full pages) mmaped in 14 calls  

mmaps by size class: 8:32766; 9:8191; 10:4095; 11:2047; 12:1024; 13:512; 14:256; 15:128; 16:128; 17:32; 18:16; 19:8;  

mallocs by size class: 8:17359; 9:1545; 10:2461; 11:292; 12:92; 13:96; 14:116; 15:41; 16:110; 17:8; 18:1; 19:1;  

frees by size class: 8:8905; 9:1000; 10:2311; 11:130; 12:44; 13:75; 14:104; 15:33; 16:105; 17:4; 18:1; 19:1;  

rfrees by size class:  

Stats: malloc large: 10 small slow: 167  

Shadow byte and word:  

0x1fe5f9557491: fd  

0x1fe5f9557490: fd fd fd fd fd fd fd fd  

More shadow bytes:  

0x1fe5f9557470: fd fd fd fd fd fd fd fd  

0x1fe5f9557478: fd fd fd fd fd fd fd fd  

0x1fe5f9557480: fa fa fa fa fa fa fa fa  

0x1fe5f9557488: fa fa fa fa fa fa fa fa  

=>0x1fe5f9557490: fd fd fd fd fd fd fd fd  

0x1fe5f9557498: fd fd fd fd fd fd fd fd  

0x1fe5f95574a0: fa fa fa fa fa fa fa fa  

0x1fe5f95574a8: fa fa fa fa fa fa fa fa  

0x1fe5f95574b0: fd fd fd fd fd fd fd fd

## Attachments

- [07-07-uaf.zip](attachments/07-07-uaf.zip) (application/zip; charset=binary, 807 B)

## Timeline

### in...@chromium.org (2012-07-07)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=73517792

Uploader: inferno@chromium.org

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x7fe7fd593e88
Crash State:
  - crash stack -
  WebCore::StyleResolver::collectMatchingRulesForList
  WebCore::StyleResolver::collectMatchingRules
  - free stack -
  WebCore::StyleSheetContents::wrapperDeleteRule
  WebCore::CSSStyleSheet::deleteRule
  

Minimized Testcase (0.67 Kb): https://cluster-fuzz.appspot.com/download/AMIfv945XTPnhxOG6Hf0mwD5wAxg_1enLmE448cpBk1YwTHVgBnoL5sq3sHlj7oPB0Gzfh_HBtkvvDim3r8uYMYphBct7fb6GHTE39PoR7DRCoKUgj_HEEQYXDSbzkvI-m7VeNsAY2rDVUtfZiNXl0q4_iFpHbyrUYYIqgALSAEVXCbaHwuLSsY

### in...@chromium.org (2012-07-07)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-07-07)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-07-12)

Upstreamed - https://bugs.webkit.org/show_bug.cgi?id=90803

### in...@chromium.org (2012-07-16)

Mike, need help with an owner for css stuff.

### mi...@chromium.org (2012-07-17)

Doug - can you please take a look at this one?

### in...@chromium.org (2012-07-19)

http://trac.webkit.org/changeset/123128

### cl...@chromium.org (2012-07-21)

ClusterFuzz has detected this issue as fixed in range 147680:147690.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=73517792

Uploader: inferno@chromium.org

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x7fe7fd593e88
Crash State:
  - crash stack -
  WebCore::StyleResolver::collectMatchingRulesForList
  WebCore::StyleResolver::collectMatchingRules
  - free stack -
  WebCore::StyleSheetContents::wrapperDeleteRule
  WebCore::CSSStyleSheet::deleteRule
  
Fixed: https://cluster-fuzz.appspot.com/revisions?range=147680:147690

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv945XTPnhxOG6Hf0mwD5wAxg_1enLmE448cpBk1YwTHVgBnoL5sq3sHlj7oPB0Gzfh_HBtkvvDim3r8uYMYphBct7fb6GHTE39PoR7DRCoKUgj_HEEQYXDSbzkvI-m7VeNsAY2rDVUtfZiNXl0q4_iFpHbyrUYYIqgALSAEVXCbaHwuLSsY

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### sc...@gmail.com (2012-07-21)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-07-24)

merged to m21 in r123528

### sc...@gmail.com (2012-07-30)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-07-31)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-07-31)

Good catch, Arthur -- $1000 of course.

### sc...@gmail.com (2012-08-16)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-09-12)

Paid as part of $4133.70 batch.

### bu...@chromium.org (2012-10-14)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### js...@chromium.org (2012-12-20)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-01-18)

Restrict-View-EditIssue is preferred since it allows anyone who can edit an issue (committers and contributors) to view the bug.

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

This issue was migrated from crbug.com/chromium/136235?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060927)*
