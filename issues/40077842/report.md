# Heap-use-after-free in WebCore::RenderObjectChildList::destroyLeftoverChildren

| Field | Value |
|-------|-------|
| **Issue ID** | [40077842](https://issues.chromium.org/issues/40077842) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Reporter** | cl...@chromium.org |
| **Assignee** | jc...@chromium.org |
| **Created** | 2013-07-26 |
| **Bounty** | $2,000.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5107399685832704

Fuzzer: Miaubiz_css_fuzzer

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x6120000d22a0
Crash State:
  - crash stack -
  WebCore::RenderBox::computeBlockDirectionMargins
  WebCore::RenderBox::computeAndSetBlockDirectionMargins
  - free stack -
  WebCore::ElementRareData::setPseudoElement
  WebCore::Element::updatePseudoElement
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=213598:213606

Minimized Testcase (1.35 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94BPtE04XDqEdAIU4BDZRsG-M1M6z9bI-a75_ZvuK9v_NDfIkJu3s2jxufcPG93xVtK-MfR23pL3yWuHsUEpsTNz2EJkGqzjP4usgNgbsXSaRvYJK39E5tVt1o0FMaFTCKYr_gvFAdeZR9VS5biOthXebRUCQ

## Attachments

- [fuzz-87.html](attachments/fuzz-87.html) (text/plain; charset=us-ascii, 1.4 KB)
- [fuzz-35 (1).html](attachments/fuzz-35 (1).html) (text/plain; charset=us-ascii, 1.4 KB)

## Timeline

### in...@chromium.org (2013-07-26)

Elliot, i am at a offsite and can't find out who caused this pseudoelement regression. Since you know this code well, can you take a quick peek at this narrow regression range - http://build.chromium.org/f/chromium/perf/dashboard/ui/changelog_blink.html?url=/trunk&range=154842:154902&mode=html and assign it to regresse. Thanks a lot.

### es...@chromium.org (2013-07-26)

I suspect http://src.chromium.org/viewvc/blink?revision=154884&view=revision since there's run-ins in that test case. Not sure how to assign to igor.o though.

### in...@chromium.org (2013-07-26)

Attaching report and repro since Igor won't be able to access clusterfuzz

==7==ERROR: AddressSanitizer: heap-use-after-free on address 0x615001294620 at pc 0x7f1e06f2c982 bp 0x7fff6c232e80 sp 0x7fff6c232e78
READ of size 8 at 0x615001294620 thread T0 (chrome)
    #0 0x7f1e06f2c981 in WebCore::Node::treeScope() const src/third_party/WebKit/Source/core/dom/Node.h:498
    #1 0x7f1e06f2c948 in WebCore::Node::documentInternal() const src/third_party/WebKit/Source/core/dom/Node.h:816
    #2 0x7f1e08214dc8 in WebCore::RenderObject::view() const src/third_party/WebKit/Source/core/rendering/RenderObject.h:604
    #3 0x7f1e0831ad0d in WebCore::RenderBox::computeBlockDirectionMargins(WebCore::RenderBlock const*, WebCore::LayoutUnit&, WebCore::LayoutUnit&) const src/third_party/WebKit/Source/core/rendering/RenderBox.cpp:2927
    #4 0x7f1e08320d10 in WebCore::RenderBox::computeAndSetBlockDirectionMargins(WebCore::RenderBlock const*) src/third_party/WebKit/Source/core/rendering/RenderBox.cpp:2937
    #5 0x7f1e0826a929 in WebCore::RenderBlock::marginBeforeEstimateForChild(WebCore::RenderBox*, WebCore::LayoutUnit&, WebCore::LayoutUnit&, bool&) const src/third_party/WebKit/Source/core/rendering/RenderBlock.cpp:2320
    #6 0x7f1e0826a9cf in WebCore::RenderBlock::marginBeforeEstimateForChild(WebCore::RenderBox*, WebCore::LayoutUnit&, WebCore::LayoutUnit&, bool&) const src/third_party/WebKit/Source/core/rendering/RenderBlock.cpp:2329
    #7 0x7f1e0826a9cf in WebCore::RenderBlock::marginBeforeEstimateForChild(WebCore::RenderBox*, WebCore::LayoutUnit&, WebCore::LayoutUnit&, bool&) const src/third_party/WebKit/Source/core/rendering/RenderBlock.cpp:2329
    #8 0x7f1e0826ad40 in WebCore::RenderBlock::estimateLogicalTopPosition(WebCore::RenderBox*, WebCore::RenderBlock::MarginInfo const&, WebCore::LayoutUnit&) src/third_party/WebKit/Source/core/rendering/RenderBlock.cpp:2343
    #9 0x7f1e0826f405 in WebCore::RenderBlock::layoutBlockChild(WebCore::RenderBox*, WebCore::RenderBlock::MarginInfo&, WebCore::LayoutUnit&, WebCore::LayoutUnit&) src/third_party/WebKit/Source/core/rendering/RenderBlock.cpp:2593
    #10 0x7f1e0825d0f3 in WebCore::RenderBlock::layoutBlockChildren(bool, WebCore::LayoutUnit&) src/third_party/WebKit/Source/core/rendering/RenderBlock.cpp:2573
    #11 0x7f1e082593d0 in WebCore::RenderBlock::layoutBlock(bool, WebCore::LayoutUnit) src/third_party/WebKit/Source/core/rendering/RenderBlock.cpp:1648
    #12 0x7f1e08256d93 in WebCore::RenderBlock::layout() src/third_party/WebKit/Source/core/rendering/RenderBlock.cpp:1455
    #13 0x7f1e0826f84a in WebCore::RenderBlock::layoutBlockChild(WebCore::RenderBox*, WebCore::RenderBlock::MarginInfo&, WebCore::LayoutUnit&, WebCore::LayoutUnit&) src/third_party/WebKit/Source/core/rendering/RenderBlock.cpp:2636
    #14 0x7f1e0825d0f3 in WebCore::RenderBlock::layoutBlockChildren(bool, WebCore::LayoutUnit&) src/third_party/WebKit/Source/core/rendering/RenderBlock.cpp:2573
    #15 0x7f1e082593d0 in WebCore::RenderBlock::layoutBlock(bool, WebCore::LayoutUnit) src/third_party/WebKit/Source/core/rendering/RenderBlock.cpp:1648
    #16 0x7f1e08256d93 in WebCore::RenderBlock::layout() src/third_party/WebKit/Source/core/rendering/RenderBlock.cpp:1455
    #17 0x7f1e084f03ed in WebCore::RenderView::layoutContent(WebCore::LayoutState const&) src/third_party/WebKit/Source/core/rendering/RenderView.cpp:130
    #18 0x7f1e084f163b in WebCore::RenderView::layout() src/third_party/WebKit/Source/core/rendering/RenderView.cpp:290
    #19 0x7f1e08a6e705 in WebCore::FrameView::layout(bool) src/third_party/WebKit/Source/core/page/FrameView.cpp:1014
    #20 0x7f1e078620e5 in WebCore::Document::updateLayout() src/third_party/WebKit/Source/core/dom/Document.cpp:1722
    #21 0x7f1e07862402 in WebCore::Document::updateLayoutIgnorePendingStylesheets() src/third_party/WebKit/Source/core/dom/Document.cpp:1760
    #22 0x7f1e078ad277 in WebCore::Element::offsetTop() src/third_party/WebKit/Source/core/dom/Element.cpp:571
    #23 0x7f1e07b00eac in WebCore::ElementV8Internal::offsetTopAttrGetterForMainWorld(v8::Local<v8::String>, v8::PropertyCallbackInfo<v8::Value> const&) src/out/Release/gen/webkit/bindings/V8Element.cpp:214
    #24 0x7f1e07ae4f3c in WebCore::ElementV8Internal::offsetTopAttrGetterCallbackForMainWorld(v8::Local<v8::String>, v8::PropertyCallbackInfo<v8::Value> const&) src/out/Release/gen/webkit/bindings/V8Element.cpp:221
    #25 0x7f1dd03597d7
    #26 0x7f1dd0357e90
    #27 0x7f1dd032b663
    #28 0x7f1dd0317d96
    #25 0x7f1e0a9381c2 in v8::internal::Invoke(bool, v8::internal::Handle<v8::internal::JSFunction>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*, bool*) src/v8/src/execution.cc:119
    #26 0x7f1e0a88e4f8 in v8::Function::Call(v8::Handle<v8::Object>, int, v8::Handle<v8::Value>*) src/v8/src/api.cc:4328
    #27 0x7f1e07fad2b2 in WebCore::V8ScriptRunner::callFunction(v8::Handle<v8::Function>, WebCore::ScriptExecutionContext*, v8::Handle<v8::Object>, int, v8::Handle<v8::Value>*) src/third_party/WebKit/Source/bindings/v8/V8ScriptRunner.cpp:130
    #28 0x7f1e07f5cd6a in WebCore::ScriptController::callFunctionWithInstrumentation(WebCore::ScriptExecutionContext*, v8::Handle<v8::Function>, v8::Handle<v8::Object>, int, v8::Handle<v8::Value>*) src/third_party/WebKit/Source/bindings/v8/ScriptController.cpp:203
    #29 0x7f1e07f5cb9c in WebCore::ScriptController::callFunction(v8::Handle<v8::Function>, v8::Handle<v8::Object>, int, v8::Handle<v8::Value>*) src/third_party/WebKit/Source/bindings/v8/ScriptController.cpp:159
    #30 0x7f1e07f58ef0 in WebCore::ScheduledAction::execute(WebCore::Frame*) src/third_party/WebKit/Source/bindings/v8/ScheduledAction.cpp:100
    #31 0x7f1e08a17826 in WebCore::DOMTimer::fired() src/third_party/WebKit/Source/core/page/DOMTimer.cpp:156
    #32 0x7f1e074210c1 in WebCore::ThreadTimers::sharedTimerFiredInternal() src/third_party/WebKit/Source/core/platform/ThreadTimers.cpp:134
    #33 0x7f1e07420af4 in WebCore::ThreadTimers::sharedTimerFired() src/third_party/WebKit/Source/core/platform/ThreadTimers.cpp:108
    #34 0x7f1e0d01928a in base::internal::InvokeHelper<false, void, base::internal::RunnableAdapter<void (webkit_glue::WebKitPlatformSupportImpl::*)()>, void (webkit_glue::WebKitPlatformSupportImpl*)>::MakeItSo(base::internal::RunnableAdapter<void (webkit_glue::WebKitPlatformSupportImpl::*)()>, webkit_glue::WebKitPlatformSupportImpl*) src/base/bind_internal.h:871
    #35 0x7f1e0d019063 in base::internal::Invoker<1, base::internal::BindState<base::internal::RunnableAdapter<void (webkit_glue::WebKitPlatformSupportImpl::*)()>, void (webkit_glue::WebKitPlatformSupportImpl*), void (base::internal::UnretainedWrapper<webkit_glue::WebKitPlatformSupportImpl>)>, void (webkit_glue::WebKitPlatformSupportImpl*)>::Run(base::internal::BindStateBase*) src/base/bind_internal.h:1169
    #36 0x7f1e0b1647e2 in base::Timer::RunScheduledTask() src/base/timer/timer.cc:181
    #37 0x7f1e0b164e1a in base::internal::InvokeHelper<false, void, base::internal::RunnableAdapter<void (base::BaseTimerTaskInternal::*)()>, void (base::BaseTimerTaskInternal*)>::MakeItSo(base::internal::RunnableAdapter<void (base::BaseTimerTaskInternal::*)()>, base::BaseTimerTaskInternal*) src/base/bind_internal.h:871
    #38 0x7f1e0b164cc3 in base::internal::Invoker<1, base::internal::BindState<base::internal::RunnableAdapter<void (base::BaseTimerTaskInternal::*)()>, void (base::BaseTimerTaskInternal*), void (base::internal::OwnedWrapper<base::BaseTimerTaskInternal>)>, void (base::BaseTimerTaskInternal*)>::Run(base::internal::BindStateBase*) src/base/bind_internal.h:1169
    #39 0x7f1e0b0c0bc4 in base::MessageLoop::RunTask(base::PendingTask const&) src/base/message_loop/message_loop.cc:478
    #40 0x7f1e0b0c152b in base::MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) src/base/message_loop/message_loop.cc:490
    #41 0x7f1e0b0c1791 in base::MessageLoop::DoWork() src/base/message_loop/message_loop.cc:604
    #42 0x7f1e0b0ce65e in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) src/base/message_loop/message_pump_default.cc:32
    #43 0x7f1e0b0c01fb in base::MessageLoop::RunInternal() src/base/message_loop/message_loop.cc:432
    #44 0x7f1e0b10c569 in base::RunLoop::Run() src/base/run_loop.cc:45
    #45 0x7f1e0b0bef5d in base::MessageLoop::Run() src/base/message_loop/message_loop.cc:303
    #46 0x7f1e0d708cf6 in content::RendererMain(content::MainFunctionParams const&) src/content/renderer/renderer_main.cc:254
    #47 0x7f1e0b5c5076 in content::RunZygote(content::MainFunctionParams const&, content::ContentMainDelegate*) src/content/app/content_main_runner.cc:393
    #48 0x7f1e0b5c59d8 in content::RunNamedProcessTypeMain(std::string const&, content::MainFunctionParams const&, content::ContentMainDelegate*) src/content/app/content_main_runner.cc:453
    #49 0x7f1e0b5c68a0 in content::ContentMainRunnerImpl::Run() src/content/app/content_main_runner.cc:765
    #50 0x7f1e0b5c4732 in content::ContentMain(int, char const**, content::ContentMainDelegate*) src/content/app/content_main.cc:35
    #51 0x7f1e056c68d6 in ChromeMain src/chrome/app/chrome_main.cc:32
    #52 0x7f1e056c681a in main src/chrome/app/chrome_exe_main_gtk.cc:43
    #53 0x7f1dfbecd76c in ?? ??
0x615001294620 is located 32 bytes inside of 104-byte region [0x615001294600,0x615001294668)
freed by thread T0 (chrome) here:
    #0 0x7f1e056b3695 in free _asan_rtl_
    #1 0x7f1e078ca4b4 in derefIfNotNull<WebCore::PseudoElement> src/third_party/WebKit/Source/wtf/PassRefPtr.h:44
    #2 0x7f1e078ca4b4 in WTF::RefPtr<WebCore::PseudoElement>::operator=(WTF::PassRefPtr<WebCore::PseudoElement> const&) src/third_party/WebKit/Source/wtf/RefPtr.h:128
    #3 0x7f1e078b4621 in WebCore::Element::updatePseudoElement(WebCore::PseudoId, WebCore::Node::StyleChange) src/third_party/WebKit/Source/core/dom/Element.cpp:2396
    #4 0x7f1e078b4037 in WebCore::Element::recalcStyle(WebCore::Node::StyleChange) src/third_party/WebKit/Source/core/dom/Element.cpp:1509
    #5 0x7f1e078b4179 in WebCore::Element::recalcStyle(WebCore::Node::StyleChange) src/third_party/WebKit/Source/core/dom/Element.cpp:1540
    #6 0x7f1e078b4179 in WebCore::Element::recalcStyle(WebCore::Node::StyleChange) src/third_party/WebKit/Source/core/dom/Element.cpp:1540
    #7 0x7f1e0786134a in WebCore::Document::recalcStyle(WebCore::Node::StyleChange) src/third_party/WebKit/Source/core/dom/Document.cpp:1632
    #8 0x7f1e078627b2 in WebCore::Document::styleResolverChanged(WebCore::StyleResolverUpdateType, WebCore::StyleResolverUpdateMode) src/third_party/WebKit/Source/core/dom/Document.cpp:3017
    #9 0x7f1e07867bff in WebCore::Document::didRemoveAllPendingStylesheet() src/third_party/WebKit/Source/core/dom/Document.cpp:2592
    #10 0x7f1e0d391907 in WebCore::StyleElement::sheetLoaded(WebCore::Document*) src/third_party/WebKit/Source/core/dom/StyleElement.cpp:172
    #11 0x7f1e0ce093bc in WebCore::HTMLStyleElement::sheetLoaded() src/third_party/WebKit/Source/core/html/HTMLStyleElement.h:82
    #12 0x7f1e0873fb62 in WebCore::StyleSheetContents::checkLoaded() src/third_party/WebKit/Source/core/css/StyleSheetContents.cpp:346
    #13 0x7f1e0d391616 in WebCore::StyleElement::createSheet(WebCore::Element*, WTF::String const&) src/third_party/WebKit/Source/core/dom/StyleElement.cpp:156
    #14 0x7f1e0d390c4e in WebCore::StyleElement::process(WebCore::Element*) src/third_party/WebKit/Source/core/dom/StyleElement.cpp:114
    #15 0x7f1e07844a5b in WebCore::updateTreeAfterInsertion(WebCore::ContainerNode*, WebCore::Node*, WebCore::AttachBehavior) src/third_party/WebKit/Source/core/dom/ContainerNode.cpp:1028
    #16 0x7f1e07844443 in WebCore::ContainerNode::appendChild(WTF::PassRefPtr<WebCore::Node>, int&, WebCore::AttachBehavior) src/third_party/WebKit/Source/core/dom/ContainerNode.cpp:642
    #17 0x7f1e07900a9a in WebCore::Node::appendChild(WTF::PassRefPtr<WebCore::Node>, int&, WebCore::AttachBehavior) src/third_party/WebKit/Source/core/dom/Node.cpp:540
    #18 0x7f1e07feb260 in WebCore::V8Node::appendChildMethodCustom(v8::FunctionCallbackInfo<v8::Value> const&) src/third_party/WebKit/Source/bindings/v8/custom/V8NodeCustom.cpp:120
    #19 0x7f1e07ec3abc in WebCore::NodeV8Internal::appendChildMethodCallbackForMainWorld(v8::FunctionCallbackInfo<v8::Value> const&) src/out/Release/gen/webkit/bindings/V8Node.cpp:690
    #20 0x7f1e0a8aa207 in v8::internal::FunctionCallbackArguments::Call(v8::Handle<v8::Value> (*)(v8::Arguments const&)) src/v8/src/arguments.cc:103
    #21 0x7f1e0a8cf085 in v8::internal::MaybeObject* v8::internal::HandleApiCallHelper<false>(v8::internal::(anonymous namespace)::BuiltinArguments<(v8::internal::BuiltinExtraArguments)1>, v8::internal::Isolate*) src/v8/src/builtins.cc:1272
    #22 0x7f1e0a8c28d4 in v8::internal::Builtin_HandleApiCall(int, v8::internal::Object**, v8::internal::Isolate*) src/v8/src/builtins.cc:1288
    #22 0x7f1dd0307eed
    #23 0x7f1dd035aad9
    #24 0x7f1dd030e853
    #25 0x7f1dd0357e22
    #26 0x7f1dd032b663
    #27 0x7f1dd0317d96
    #23 0x7f1e0a9381c2 in v8::internal::Invoke(bool, v8::internal::Handle<v8::internal::JSFunction>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*, bool*) src/v8/src/execution.cc:119
    #24 0x7f1e0a88e4f8 in v8::Function::Call(v8::Handle<v8::Object>, int, v8::Handle<v8::Value>*) src/v8/src/api.cc:4328
    #25 0x7f1e07fad2b2 in WebCore::V8ScriptRunner::callFunction(v8::Handle<v8::Function>, WebCore::ScriptExecutionContext*, v8::Handle<v8::Object>, int, v8::Handle<v8::Value>*) src/third_party/WebKit/Source/bindings/v8/V8ScriptRunner.cpp:130
    #26 0x7f1e07f5cd6a in WebCore::ScriptController::callFunctionWithInstrumentation(WebCore::ScriptExecutionContext*, v8::Handle<v8::Function>, v8::Handle<v8::Object>, int, v8::Handle<v8::Value>*) src/third_party/WebKit/Source/bindings/v8/ScriptController.cpp:203
    #27 0x7f1e07f5cb9c in WebCore::ScriptController::callFunction(v8::Handle<v8::Function>, v8::Handle<v8::Object>, int, v8::Handle<v8::Value>*) src/third_party/WebKit/Source/bindings/v8/ScriptController.cpp:159
    #28 0x7f1e07f58ef0 in WebCore::ScheduledAction::execute(WebCore::Frame*) src/third_party/WebKit/Source/bindings/v8/ScheduledAction.cpp:100
    #29 0x7f1e08a17826 in WebCore::DOMTimer::fired() src/third_party/WebKit/Source/core/page/DOMTimer.cpp:156
    #30 0x7f1e074210c1 in WebCore::ThreadTimers::sharedTimerFiredInternal() src/third_party/WebKit/Source/core/platform/ThreadTimers.cpp:134
    #31 0x7f1e07420af4 in WebCore::ThreadTimers::sharedTimerFired() src/third_party/WebKit/Source/core/platform/ThreadTimers.cpp:108
    #32 0x7f1e0d01928a in base::internal::InvokeHelper<false, void, base::internal::RunnableAdapter<void (webkit_glue::WebKitPlatformSupportImpl::*)()>, void (webkit_glue::WebKitPlatformSupportImpl*)>::MakeItSo(base::internal::RunnableAdapter<void (webkit_glue::WebKitPlatformSupportImpl::*)()>, webkit_glue::WebKitPlatformSupportImpl*) src/base/bind_internal.h:871
    #33 0x7f1e0d019063 in base::internal::Invoker<1, base::internal::BindState<base::internal::RunnableAdapter<void (webkit_glue::WebKitPlatformSupportImpl::*)()>, void (webkit_glue::WebKitPlatformSupportImpl*), void (base::internal::UnretainedWrapper<webkit_glue::WebKitPlatformSupportImpl>)>, void (webkit_glue::WebKitPlatformSupportImpl*)>::Run(base::internal::BindStateBase*) src/base/bind_internal.h:1169
    #34 0x7f1e0b1647e2 in base::Timer::RunScheduledTask() src/base/timer/timer.cc:181
    #35 0x7f1e0b164e1a in base::internal::InvokeHelper<false, void, base::internal::RunnableAdapter<void (base::BaseTimerTaskInternal::*)()>, void (base::BaseTimerTaskInternal*)>::MakeItSo(base::internal::RunnableAdapter<void (base::BaseTimerTaskInternal::*)()>, base::BaseTimerTaskInternal*) src/base/bind_internal.h:871
    #36 0x7f1e0b164cc3 in base::internal::Invoker<1, base::internal::BindState<base::internal::RunnableAdapter<void (base::BaseTimerTaskInternal::*)()>, void (base::BaseTimerTaskInternal*), void (base::internal::OwnedWrapper<base::BaseTimerTaskInternal>)>, void (base::BaseTimerTaskInternal*)>::Run(base::internal::BindStateBase*) src/base/bind_internal.h:1169
    #37 0x7f1e0b0c0bc4 in base::MessageLoop::RunTask(base::PendingTask const&) src/base/message_loop/message_loop.cc:478
    #38 0x7f1e0b0c152b in base::MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) src/base/message_loop/message_loop.cc:490
    #39 0x7f1e0b0c1791 in base::MessageLoop::DoWork() src/base/message_loop/message_loop.cc:604
    #40 0x7f1e0b0ce65e in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) src/base/message_loop/message_pump_default.cc:32
    #41 0x7f1e0b0c01fb in base::MessageLoop::RunInternal() src/base/message_loop/message_loop.cc:432
    #42 0x7f1e0b10c569 in base::RunLoop::Run() src/base/run_loop.cc:45
    #43 0x7f1e0b0bef5d in base::MessageLoop::Run() src/base/message_loop/message_loop.cc:303
    #44 0x7f1e0d708cf6 in content::RendererMain(content::MainFunctionParams const&) src/content/renderer/renderer_main.cc:254
    #45 0x7f1e0b5c5076 in content::RunZygote(content::MainFunctionParams const&, content::ContentMainDelegate*) src/content/app/content_main_runner.cc:393
    #46 0x7f1e0b5c59d8 in content::RunNamedProcessTypeMain(std::string const&, content::MainFunctionParams const&, content::ContentMainDelegate*) src/content/app/content_main_runner.cc:453
    #47 0x7f1e0b5c68a0 in content::ContentMainRunnerImpl::Run() src/content/app/content_main_runner.cc:765
    #48 0x7f1e0b5c4732 in content::ContentMain(int, char const**, content::ContentMainDelegate*) src/content/app/content_main.cc:35
    #49 0x7f1e056c68d6 in ChromeMain src/chrome/app/chrome_main.cc:32
    #50 0x7f1e056c681a in main src/chrome/app/chrome_exe_main_gtk.cc:43
    #51 0x7f1dfbecd76c in ?? ??
previously allocated by thread T0 (chrome) here:
    #0 0x7f1e056b37d5 in malloc _asan_rtl_
    #1 0x7f1e078b911d in WebCore::PseudoElement::create(WebCore::Element*, WebCore::PseudoId) src/third_party/WebKit/Source/core/dom/PseudoElement.h:40
    #2 0x7f1e078b29f5 in WebCore::Element::createPseudoElementIfNeeded(WebCore::PseudoId) src/third_party/WebKit/Source/core/dom/Element.cpp:2416
    #3 0x7f1e078b4663 in WebCore::Element::updatePseudoElement(WebCore::PseudoId, WebCore::Node::StyleChange) src/third_party/WebKit/Source/core/dom/Element.cpp:2398
    #4 0x7f1e078b4037 in WebCore::Element::recalcStyle(WebCore::Node::StyleChange) src/third_party/WebKit/Source/core/dom/Element.cpp:1509
    #5 0x7f1e078b4179 in WebCore::Element::recalcStyle(WebCore::Node::StyleChange) src/third_party/WebKit/Source/core/dom/Element.cpp:1540
    #6 0x7f1e078b4179 in WebCore::Element::recalcStyle(WebCore::Node::StyleChange) src/third_party/WebKit/Source/core/dom/Element.cpp:1540
    #7 0x7f1e0786134a in WebCore::Document::recalcStyle(WebCore::Node::StyleChange) src/third_party/WebKit/Source/core/dom/Document.cpp:1632
    #8 0x7f1e0785c88f in WebCore::Document::updateStyleIfNeeded() src/third_party/WebKit/Source/core/dom/Document.cpp:1687
    #9 0x7f1e078620a6 in WebCore::Document::updateLayout() src/third_party/WebKit/Source/core/dom/Document.cpp:1716
    #10 0x7f1e07862402 in WebCore::Document::updateLayoutIgnorePendingStylesheets() src/third_party/WebKit/Source/core/dom/Document.cpp:1760
    #11 0x7f1e078ad277 in WebCore::Element::offsetTop() src/third_party/WebKit/Source/core/dom/Element.cpp:571
    #12 0x7f1e07b00eac in WebCore::ElementV8Internal::offsetTopAttrGetterForMainWorld(v8::Local<v8::String>, v8::PropertyCallbackInfo<v8::Value> const&) src/out/Release/gen/webkit/bindings/V8Element.cpp:214
    #13 0x7f1e07ae4f3c in WebCore::ElementV8Internal::offsetTopAttrGetterCallbackForMainWorld(v8::Local<v8::String>, v8::PropertyCallbackInfo<v8::Value> const&) src/out/Release/gen/webkit/bindings/V8Element.cpp:221


### in...@chromium.org (2013-07-26)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-07-26)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6152576756088832

Fuzzer: Miaubiz_css_fuzzer

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x60f000003334
Crash State:
  - crash stack -
  WebCore::RenderObjectChildList::destroyLeftoverChildren
  WebCore::RenderBlock::willBeDestroyed
  - free stack -
  WebCore::Element::detach
  WebCore::ContainerNode::detach
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=213598:213606

Minimized Testcase (1.41 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95ok6kdLpeGRCSoc0NnHfJfqpyfNf-FacQNSjEheTngN8EpThxAqRVOtzA95EMoL908P91q0miabTtQ8ycXEcJwLngu-tg_yh6T0gsLBYurQgdEd8H_-qNtD6BSZBcnKL4x_7KxPsEifmafXiFldCgcMe_XYA



### in...@chromium.org (2013-07-26)

Elliot, i think you are right, this second testcase with different stack, is also pointing towards run-in.

Attaching second repro for Igor.

### ig...@sisa.samsung.com (2013-07-26)

Looking.

### ig...@sisa.samsung.com (2013-07-26)

Inferno,

Could you paste the test case.

### es...@chromium.org (2013-07-27)

@igor.o the test case is attached to https://crbug.com/chromium/264504#c6, the fuzz-87.html file.

### in...@chromium.org (2013-07-27)

This testcase attached is for c#3 stack and testcase in c#6 is for testcase in c#5 stack. Sorry for this confusion.

### in...@chromium.org (2013-07-30)

Verified locally that that changeset caused multiple regressions. So, reverted in r155173. When you checkin your changeset again, please make sure to verify testcases in c#6 and c#10 with an asan build.

### cl...@chromium.org (2013-07-31)

ClusterFuzz has detected this issue as fixed in range 214658:214671.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5107399685832704

Fuzzer: Miaubiz_css_fuzzer

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x6120000d22a0
Crash State:
  - crash stack -
  WebCore::RenderBox::computeBlockDirectionMargins
  WebCore::RenderBox::computeAndSetBlockDirectionMargins
  - free stack -
  WebCore::ElementRareData::setPseudoElement
  WebCore::Element::updatePseudoElement
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=213598:213606
Fixed: https://cluster-fuzz.appspot.com/revisions?range=214658:214671

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv94BPtE04XDqEdAIU4BDZRsG-M1M6z9bI-a75_ZvuK9v_NDfIkJu3s2jxufcPG93xVtK-MfR23pL3yWuHsUEpsTNz2EJkGqzjP4usgNgbsXSaRvYJK39E5tVt1o0FMaFTCKYr_gvFAdeZR9VS5biOthXebRUCQ

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### cl...@chromium.org (2013-07-31)

ClusterFuzz has detected this issue as fixed in range 214658:214671.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6152576756088832

Fuzzer: Miaubiz_css_fuzzer

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x60f000003334
Crash State:
  - crash stack -
  WebCore::RenderObjectChildList::destroyLeftoverChildren
  WebCore::RenderBlock::willBeDestroyed
  - free stack -
  WebCore::Element::detach
  WebCore::ContainerNode::detach
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=213598:213606
Fixed: https://cluster-fuzz.appspot.com/revisions?range=214658:214671

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv95ok6kdLpeGRCSoc0NnHfJfqpyfNf-FacQNSjEheTngN8EpThxAqRVOtzA95EMoL908P91q0miabTtQ8ycXEcJwLngu-tg_yh6T0gsLBYurQgdEd8H_-qNtD6BSZBcnKL4x_7KxPsEifmafXiFldCgcMe_XYA

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### cl...@chromium.org (2013-09-19)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-09-25)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-09-25)

Did you saw our new criteria for possibly issuing higher rewards? See http://www.chromium.org/Home/chromium-security/vulnerability-rewards-program/reward-nomination-process
E.g. If you are able to provide a repro that faulted at an address of 0x41414141, it will qualify for the new higher rewards. Or, if you can show that you have control between free and crash points, etc.

### in...@chromium.org (2013-09-26)

Removing incorrect Release-0 which is reserved for bugs impacting stable.

### sc...@gmail.com (2013-09-28)

$2000 for this one because the ASAN shows JS control between the free and use.
But down from $3000 because the used object is inside one of our partitions.

### pa...@chromium.org (2013-10-18)

[Empty comment from Monorail migration]

### js...@chromium.org (2013-11-18)

Bulk release of old security bug reports.


### js...@chromium.org (2013-11-18)

Bulk release of old security bug reports.


### ti...@chromium.org (2014-02-28)

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

This issue was migrated from crbug.com/chromium/264504?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40077842)*
