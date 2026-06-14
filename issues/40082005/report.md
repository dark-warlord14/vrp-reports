# Heap-use-after-free in blink::CSSAnimations::maybeApplyPendingUpdate

| Field | Value |
|-------|-------|
| **Issue ID** | [40082005](https://issues.chromium.org/issues/40082005) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Animation |
| **Reporter** | at...@gmail.com |
| **Assignee** | al...@chromium.org |
| **Created** | 2015-05-05 |
| **Bounty** | $3,000.00 |

## Description



Tested on:

OS: Ubuntu 14.04

Chromium: ASAN 44.0.2375.0 (Developer Build) (64-bit) 

2bd42fdbfab81b645ac926bd115e2a0762426b64-refs/heads/master@{#325771}


Repro-file as an attachment.

ASAN-trace:

==23174==ERROR: AddressSanitizer: heap-use-after-free on address 0x607000061800 at pc 0x7f9bd49bac8b bp 0x7ffdcf3c3070 sp 0x7ffdcf3c3068
READ of size 8 at 0x607000061800 thread T0 (chrome)
    #0 0x7f9bd49bac8a in operator-> /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/wtf/RefPtr.h:63
    #1 0x7f9bd49b5d52 in maybeApplyPendingUpdate /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/animation/css/CSSAnimations.cpp:362
    #2 0x7f9bd425f845 in styleForLayoutObject /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/dom/Element.cpp:1632
    #3 0x7f9bd42612a1 in recalcOwnStyle /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/dom/Element.cpp:1719
    #4 0x7f9bd4260a62 in blink::Element::recalcStyle(blink::StyleRecalcChange, blink::Text*) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/dom/Element.cpp:1674
    #5 0x7f9bd414d06d in blink::ContainerNode::recalcChildStyle(blink::StyleRecalcChange) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/dom/ContainerNode.cpp:1285
    #6 0x7f9bd4260cce in blink::Element::recalcStyle(blink::StyleRecalcChange, blink::Text*) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/dom/Element.cpp:1689
    #7 0x7f9bd414d06d in blink::ContainerNode::recalcChildStyle(blink::StyleRecalcChange) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/dom/ContainerNode.cpp:1285
    #8 0x7f9bd4260cce in blink::Element::recalcStyle(blink::StyleRecalcChange, blink::Text*) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/dom/Element.cpp:1689
    #9 0x7f9bd41ad841 in updateStyle /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/dom/Document.cpp:1825
    #10 0x7f9bd41ac5b4 in updateRenderTree /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/dom/Document.cpp:1766
.
.
.
0x607000061800 is located 48 bytes inside of 72-byte region [0x6070000617d0,0x607000061818)
freed by thread T0 (chrome) here:
    #0 0x7f9bce4f646b in __interceptor_free ??:?
    #1 0x7f9bd49d9218 in WTF::RefCounted<blink::AnimationEffect>::deref() /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/wtf/RefCounted.h:172 (discriminator 23)
    #2 0x7f9bd49dafdc in derefIfNotNull<blink::AnimationEffect> /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/wtf/PassRefPtr.h:57
    #3 0x7f9bd49b5ad7 in maybeApplyPendingUpdate /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/animation/css/CSSAnimations.cpp:355
    #4 0x7f9bd425f845 in styleForLayoutObject /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/dom/Element.cpp:1632
    #5 0x7f9bd42612a1 in recalcOwnStyle /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/dom/Element.cpp:1719
    #6 0x7f9bd4260a62 in blink::Element::recalcStyle(blink::StyleRecalcChange, blink::Text*) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/dom/Element.cpp:1674
    #7 0x7f9bd414d06d in blink::ContainerNode::recalcChildStyle(blink::StyleRecalcChange) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/dom/ContainerNode.cpp:1285
    #8 0x7f9bd4260cce in blink::Element::recalcStyle(blink::StyleRecalcChange, blink::Text*) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/dom/Element.cpp:1689
    #9 0x7f9bd414d06d in blink::ContainerNode::recalcChildStyle(blink::StyleRecalcChange) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/dom/ContainerNode.cpp:1285
    #10 0x7f9bd4260cce in blink::Element::recalcStyle(blink::StyleRecalcChange, blink::Text*) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/dom/Element.cpp:1689
.
.
.



## Attachments

- [chrome-heap-use-after-free-operator10-min.html](attachments/chrome-heap-use-after-free-operator10-min.html) (text/html, 4.3 KB)
- [hand-minimized.html](attachments/hand-minimized.html) (text/html, 592 B)

## Timeline

### cl...@chromium.org (2015-05-05)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=6444156143009792

### cl...@chromium.org (2015-05-06)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=6409302214967296

### ri...@chromium.org (2015-05-06)

Hand-minimized it a bit - clusterfuzz wasn't able to reproduce on trunk - going to try again with the hand-minimized one.

Here's the trace I got on the latest debug asan build:

=================================================================
==1==ERROR: AddressSanitizer: heap-use-after-free on address 0x60800060eae0 at pc 0x7f88fbad867c bp 0x7fff7a444700 sp 0x7fff7a4446f8
READ of size 8 at 0x60800060eae0 thread T0 (chrome)
    #0 0x7f88fbad867b in WTF::RefPtr<blink::InterpolationEffect>::operator->() const /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../third_party/WebKit/Source/wtf/RefPtr.h:64:54
    #1 0x7f8902f68292 in void blink::KeyframeEffectModelBase::forEachInterpolation<blink::CSSAnimations::maybeApplyPendingUpdate(blink::Element*)::$_0>(blink::CSSAnimations::maybeApplyPendingUpdate(blink::Element*)::$_0 const&) /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../third_party/WebKit/Source/core/animation/KeyframeEffectModel.h:112:59
    #2 0x7f8902f65803 in blink::CSSAnimations::maybeApplyPendingUpdate(blink::Element*) /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../third_party/WebKit/Source/core/animation/css/CSSAnimations.cpp:341:9
    #3 0x7f8901e91415 in blink::Element::styleForLayoutObject() /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../third_party/WebKit/Source/core/dom/Element.cpp:1632:9
    #4 0x7f8901e930c0 in blink::Element::recalcOwnStyle(blink::StyleRecalcChange) /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../third_party/WebKit/Source/core/dom/Element.cpp:1719:38
    #5 0x7f8901e9214d in blink::Element::recalcStyle(blink::StyleRecalcChange, blink::Text*) /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../third_party/WebKit/Source/core/dom/Element.cpp:1674:22
    #6 0x7f8901c6c2f3 in blink::ContainerNode::recalcChildStyle(blink::StyleRecalcChange) /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../third_party/WebKit/Source/core/dom/ContainerNode.cpp:1299:17
    #7 0x7f8901e9257d in blink::Element::recalcStyle(blink::StyleRecalcChange, blink::Text*) /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../third_party/WebKit/Source/core/dom/Element.cpp:1689:13
    #8 0x7f8901c6c2f3 in blink::ContainerNode::recalcChildStyle(blink::StyleRecalcChange) /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../third_party/WebKit/Source/core/dom/ContainerNode.cpp:1299:17
    #9 0x7f8901e9257d in blink::Element::recalcStyle(blink::StyleRecalcChange, blink::Text*) /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../third_party/WebKit/Source/core/dom/Element.cpp:1689:13
    #10 0x7f8901d266c4 in blink::Document::updateStyle(blink::StyleRecalcChange) /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../third_party/WebKit/Source/core/dom/Document.cpp:1813:13
    #11 0x7f8901d24e3e in blink::Document::updateLayoutTree(blink::StyleRecalcChange) /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../third_party/WebKit/Source/core/dom/Document.cpp:1752:5
    #12 0x7f88fb272e71 in blink::Document::updateLayoutTreeIfNeeded() /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../third_party/WebKit/Source/core/dom/Document.h:472:39
    #13 0x7f8901d556d7 in blink::Document::finishedParsing() /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../third_party/WebKit/Source/core/dom/Document.cpp:4538:13
    #14 0x7f8902b3b30e in blink::HTMLConstructionSite::finishedParsing() /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../third_party/WebKit/Source/core/html/parser/HTMLConstructionSite.cpp:546:5
    #15 0x7f8902c7f702 in blink::HTMLTreeBuilder::finished() /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../third_party/WebKit/Source/core/html/parser/HTMLTreeBuilder.cpp:2806:5
    #16 0x7f8902b63209 in blink::HTMLDocumentParser::end() /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../third_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:853:5
    #17 0x7f8902b563fb in blink::HTMLDocumentParser::attemptToRunDeferredScriptsAndEnd() /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../third_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:866:5
    #18 0x7f8902b55baa in blink::HTMLDocumentParser::prepareToStopParsing() /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../third_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:272:5
    #19 0x7f8902b5e64a in blink::HTMLDocumentParser::processParsedChunkFromBackgroundParser(WTF::PassOwnPtr<blink::HTMLDocumentParser::ParsedChunk>) /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../third_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:485:17
    #20 0x7f8902b59a86 in blink::HTMLDocumentParser::pumpPendingSpeculations() /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../third_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:563:36
    #21 0x7f8902b58a35 in blink::HTMLDocumentParser::resumeParsingAfterYield() /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../third_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:307:5
    #22 0x7f8902bc06a5 in blink::HTMLParserScheduler::continueParsing() /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../third_party/WebKit/Source/core/html/parser/HTMLParserScheduler.cpp:163:5
    #23 0x7f8902bc2ffe in WTF::FunctionWrapper<void (blink::HTMLParserScheduler::*)()>::operator()(blink::HTMLParserScheduler*) /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../third_party/WebKit/Source/wtf/Functional.h:83:16
    #24 0x7f8902bc2e6d in WTF::PartBoundFunctionImpl<1, WTF::FunctionWrapper<void (blink::HTMLParserScheduler::*)()>, void (blink::HTMLParserScheduler*)>::operator()() /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../third_party/WebKit/Source/wtf/Functional.h:181:16
    #25 0x7f88eda2fc67 in WTF::Function<void ()>::operator()() const /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../third_party/WebKit/Source/wtf/Functional.h:338:16
    #26 0x7f88ee3fb27d in blink::CancellableTaskFactory::CancellableTask::run() /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../third_party/WebKit/Source/platform/scheduler/CancellableTaskFactory.cpp:29:9
    #27 0x7f88e16d4ff5 in scheduler::WebSchedulerImpl::runTask(scoped_ptr<blink::WebThread::Task, base::DefaultDeleter<blink::WebThread::Task> >) /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../components/scheduler/child/web_scheduler_impl.cc:46:3
    #28 0x7f88e16db7f2 in base::internal::RunnableAdapter<void (*)(scoped_ptr<blink::WebThread::Task, base::DefaultDeleter<blink::WebThread::Task> >)>::Run(scoped_ptr<blink::WebThread::Task, base::DefaultDeleter<blink::WebThread::Task> >) /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../base/bind_internal.h:157:12
    #29 0x7f88e16db41e in base::internal::InvokeHelper<false, void, base::internal::RunnableAdapter<void (*)(scoped_ptr<blink::WebThread::Task, base::DefaultDeleter<blink::WebThread::Task> >)>, base::internal::TypeList<scoped_ptr<blink::WebThread::Task, base::DefaultDeleter<blink::WebThread::Task> > > >::MakeItSo(base::internal::RunnableAdapter<void (*)(scoped_ptr<blink::WebThread::Task, base::DefaultDeleter<blink::WebThread::Task> >)>, scoped_ptr<blink::WebThread::Task, base::DefaultDeleter<blink::WebThread::Task> >) /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../base/bind_internal.h:293:5
    #30 0x7f88e16db228 in base::internal::Invoker<IndexSequence<0ul>, base::internal::BindState<base::internal::RunnableAdapter<void (*)(scoped_ptr<blink::WebThread::Task, base::DefaultDeleter<blink::WebThread::Task> >)>, void (scoped_ptr<blink::WebThread::Task, base::DefaultDeleter<blink::WebThread::Task> >), base::internal::TypeList<base::internal::PassedWrapper<scoped_ptr<blink::WebThread::Task, base::DefaultDeleter<blink::WebThread::Task> > > > >, base::internal::TypeList<base::internal::UnwrapTraits<base::internal::PassedWrapper<scoped_ptr<blink::WebThread::Task, base::DefaultDeleter<blink::WebThread::Task> > > > >, base::internal::InvokeHelper<false, void, base::internal::RunnableAdapter<void (*)(scoped_ptr<blink::WebThread::Task, base::DefaultDeleter<blink::WebThread::Task> >)>, base::internal::TypeList<scoped_ptr<blink::WebThread::Task, base::DefaultDeleter<blink::WebThread::Task> > > >, void ()>::Run(base::internal::BindStateBase*) /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../base/bind_internal.h:343:12
    #31 0x7f88f492280e in base::Callback<void ()>::Run() const /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../base/callback.h:396:12
    #32 0x7f88f49dd82c in base::debug::TaskAnnotator::RunTask(char const*, char const*, base::PendingTask const&) /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../base/debug/task_annotator.cc:62:3
    #33 0x7f88e1653bb0 in scheduler::TaskQueueManager::ProcessTaskFromWorkQueue(unsigned long, bool, base::PendingTask*) /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../components/scheduler/child/task_queue_manager.cc:653:5
    #34 0x7f88e164e24e in scheduler::TaskQueueManager::DoWork(bool) /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../components/scheduler/child/task_queue_manager.cc:608:9
    #35 0x7f88e16c642d in base::internal::RunnableAdapter<void (scheduler::TaskQueueManager::*)(bool)>::Run(scheduler::TaskQueueManager*, bool const&) /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../base/bind_internal.h:176:12
    #36 0x7f88e16c5f5f in base::internal::InvokeHelper<true, void, base::internal::RunnableAdapter<void (scheduler::TaskQueueManager::*)(bool)>, base::internal::TypeList<base::WeakPtr<scheduler::TaskQueueManager> const&, bool const&> >::MakeItSo(base::internal::RunnableAdapter<void (scheduler::TaskQueueManager::*)(bool)>, base::WeakPtr<scheduler::TaskQueueManager> const&, bool const&) /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../base/bind_internal.h:303:5
    #37 0x7f88e16c5cd4 in base::internal::Invoker<IndexSequence<0ul, 1ul>, base::internal::BindState<base::internal::RunnableAdapter<void (scheduler::TaskQueueManager::*)(bool)>, void (scheduler::TaskQueueManager*, bool), base::internal::TypeList<base::WeakPtr<scheduler::TaskQueueManager>, bool> >, base::internal::TypeList<base::internal::UnwrapTraits<base::WeakPtr<scheduler::TaskQueueManager> >, base::internal::UnwrapTraits<bool> >, base::internal::InvokeHelper<true, void, base::internal::RunnableAdapter<void (scheduler::TaskQueueManager::*)(bool)>, base::internal::TypeList<base::WeakPtr<scheduler::TaskQueueManager> const&, bool const&> >, void ()>::Run(base::internal::BindStateBase*) /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../base/bind_internal.h:343:12
    #38 0x7f88f492280e in base::Callback<void ()>::Run() const /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../base/callback.h:396:12
    #39 0x7f88f49dd82c in base::debug::TaskAnnotator::RunTask(char const*, char const*, base::PendingTask const&) /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../base/debug/task_annotator.cc:62:3
    #40 0x7f88f4c413ed in base::MessageLoop::RunTask(base::PendingTask const&) /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../base/message_loop/message_loop.cc:458:3
    #41 0x7f88f4c41a67 in base::MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../base/message_loop/message_loop.cc:468:5
    #42 0x7f88f4c43044 in base::MessageLoop::DoWork() /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../base/message_loop/message_loop.cc:580:13
    #43 0x7f88f4c8bb4e in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../base/message_loop/message_pump_default.cc:32:21
    #44 0x7f88f4c3fe43 in base::MessageLoop::RunHandler() /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../base/message_loop/message_loop.cc:424:3
    #45 0x7f88f4e7a854 in base::RunLoop::Run() /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../base/run_loop.cc:55:3
    #46 0x7f88f4c3db26 in base::MessageLoop::Run() /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../base/message_loop/message_loop.cc:286:3
    #47 0x7f891983b2e0 in content::RendererMain(content::MainFunctionParams const&) /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../content/renderer/renderer_main.cc:220:7
    #48 0x7f89132bd0dc in content::RunZygote(content::MainFunctionParams const&, content::ContentMainDelegate*) /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../content/app/content_main_runner.cc:308:14
    #49 0x7f89132bd981 in content::RunNamedProcessTypeMain(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, content::MainFunctionParams const&, content::ContentMainDelegate*) /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../content/app/content_main_runner.cc:392:12
    #50 0x7f89132c6aab in content::ContentMainRunnerImpl::Run() /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../content/app/content_main_runner.cc:783:12
    #51 0x7f89132bb534 in content::ContentMain(content::ContentMainParams const&) /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../content/app/content_main.cc:19:15
    #52 0x7f892b3dad5b in ChromeMain /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../chrome/app/chrome_main.cc:66:12
    #53 0x7f892b3daa40 in main /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../chrome/app/chrome_exe_main_aura.cc:17:10
    #54 0x7f88e284eec4 in __libc_start_main /build/buildd/eglibc-2.19/csu/libc-start.c:287:0

0x60800060eae0 is located 64 bytes inside of 88-byte region [0x60800060eaa0,0x60800060eaf8)
freed by thread T0 (chrome) here:
    #0 0x7f892b3b80db in __interceptor_free ??:0:0
    #1 0x7f88e1bae2eb in WTF::partitionFreeGeneric(WTF::PartitionRootGeneric*, void*) /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../third_party/WebKit/Source/wtf/PartitionAlloc.h:591:5
    #2 0x7f88e1bc5325 in WTF::fastFree(void*) /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../third_party/WebKit/Source/wtf/FastMalloc.cpp:61:5
    #3 0x7f88fb84924f in WTF::RefCounted<blink::EffectModel>::operator delete(void*) /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../third_party/WebKit/Source/wtf/RefCounted.h:166:5
    #4 0x7f8902e77ed2 in blink::KeyframeEffectModel<blink::StringKeyframe>::~KeyframeEffectModel() /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../third_party/WebKit/Source/core/animation/KeyframeEffectModel.h:150:7
    #5 0x7f88fb82e178 in WTF::RefCounted<blink::EffectModel>::deref() /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../third_party/WebKit/Source/wtf/RefCounted.h:172:13
    #6 0x7f88fb82dfec in void WTF::derefIfNotNull<blink::EffectModel>(blink::EffectModel*) /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../third_party/WebKit/Source/wtf/PassRefPtr.h:57:13
    #7 0x7f88fb9adfd7 in WTF::RefPtr<blink::EffectModel>::~RefPtr() /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../third_party/WebKit/Source/wtf/RefPtr.h:56:35
    #8 0x7f8900809c00 in WTF::RefPtr<blink::EffectModel>::operator=(WTF::PassRefPtr<blink::EffectModel> const&) /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../third_party/WebKit/Source/wtf/RefPtr.h:136:5
    #9 0x7f8902f71a41 in blink::KeyframeEffect::setEffect(WTF::PassRefPtr<blink::EffectModel>) /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../third_party/WebKit/Source/core/animation/KeyframeEffect.h:69:75
    #10 0x7f8902f65611 in blink::CSSAnimations::maybeApplyPendingUpdate(blink::Element*) /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../third_party/WebKit/Source/core/animation/css/CSSAnimations.cpp:334:9
    #11 0x7f8901e91415 in blink::Element::styleForLayoutObject() /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../third_party/WebKit/Source/core/dom/Element.cpp:1632:9
    #12 0x7f8901e930c0 in blink::Element::recalcOwnStyle(blink::StyleRecalcChange) /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../third_party/WebKit/Source/core/dom/Element.cpp:1719:38
    #13 0x7f8901e9214d in blink::Element::recalcStyle(blink::StyleRecalcChange, blink::Text*) /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../third_party/WebKit/Source/core/dom/Element.cpp:1674:22
    #14 0x7f8901c6c2f3 in blink::ContainerNode::recalcChildStyle(blink::StyleRecalcChange) /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../third_party/WebKit/Source/core/dom/ContainerNode.cpp:1299:17
    #15 0x7f8901e9257d in blink::Element::recalcStyle(blink::StyleRecalcChange, blink::Text*) /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../third_party/WebKit/Source/core/dom/Element.cpp:1689:13
    #16 0x7f8901c6c2f3 in blink::ContainerNode::recalcChildStyle(blink::StyleRecalcChange) /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../third_party/WebKit/Source/core/dom/ContainerNode.cpp:1299:17
    #17 0x7f8901e9257d in blink::Element::recalcStyle(blink::StyleRecalcChange, blink::Text*) /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../third_party/WebKit/Source/core/dom/Element.cpp:1689:13
    #18 0x7f8901d266c4 in blink::Document::updateStyle(blink::StyleRecalcChange) /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../third_party/WebKit/Source/core/dom/Document.cpp:1813:13
    #19 0x7f8901d24e3e in blink::Document::updateLayoutTree(blink::StyleRecalcChange) /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../third_party/WebKit/Source/core/dom/Document.cpp:1752:5
    #20 0x7f88fb272e71 in blink::Document::updateLayoutTreeIfNeeded() /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../third_party/WebKit/Source/core/dom/Document.h:472:39
    #21 0x7f8901d556d7 in blink::Document::finishedParsing() /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../third_party/WebKit/Source/core/dom/Document.cpp:4538:13
    #22 0x7f8902b3b30e in blink::HTMLConstructionSite::finishedParsing() /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../third_party/WebKit/Source/core/html/parser/HTMLConstructionSite.cpp:546:5
    #23 0x7f8902c7f702 in blink::HTMLTreeBuilder::finished() /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../third_party/WebKit/Source/core/html/parser/HTMLTreeBuilder.cpp:2806:5
    #24 0x7f8902b63209 in blink::HTMLDocumentParser::end() /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../third_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:853:5
    #25 0x7f8902b563fb in blink::HTMLDocumentParser::attemptToRunDeferredScriptsAndEnd() /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../third_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:866:5
    #26 0x7f8902b55baa in blink::HTMLDocumentParser::prepareToStopParsing() /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../third_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:272:5
    #27 0x7f8902b5e64a in blink::HTMLDocumentParser::processParsedChunkFromBackgroundParser(WTF::PassOwnPtr<blink::HTMLDocumentParser::ParsedChunk>) /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../third_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:485:17
    #28 0x7f8902b59a86 in blink::HTMLDocumentParser::pumpPendingSpeculations() /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../third_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:563:36
    #29 0x7f8902b58a35 in blink::HTMLDocumentParser::resumeParsingAfterYield() /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../third_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:307:5

previously allocated by thread T0 (chrome) here:
    #0 0x7f892b3b83bb in __interceptor_malloc ??:0:0
    #1 0x7f88e1bae094 in WTF::partitionAllocGenericFlags(WTF::PartitionRootGeneric*, int, unsigned long) /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../third_party/WebKit/Source/wtf/PartitionAlloc.h:569:20
    #2 0x7f88e1bb44e1 in WTF::partitionAllocGeneric(WTF::PartitionRootGeneric*, unsigned long) /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../third_party/WebKit/Source/wtf/PartitionAlloc.h:585:12
    #3 0x7f88e1bc5255 in WTF::fastMalloc(unsigned long) /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../third_party/WebKit/Source/wtf/FastMalloc.cpp:56:12
    #4 0x7f88fb847eef in WTF::RefCounted<blink::EffectModel>::operator new(unsigned long) /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../third_party/WebKit/Source/wtf/RefCounted.h:166:5
    #5 0x7f8902e6d827 in blink::KeyframeEffectModel<blink::StringKeyframe>::create(WTF::Vector<WTF::RefPtr<blink::StringKeyframe>, 0ul, WTF::DefaultAllocator> const&, WTF::PassRefPtr<blink::TimingFunction>) /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../third_party/WebKit/Source/core/animation/KeyframeEffectModel.h:155:35
    #6 0x7f8902f64149 in blink::(anonymous namespace)::createKeyframeEffect(blink::StyleResolver*, blink::Element const*, blink::Element&, blink::ComputedStyle const*, blink::ComputedStyle const*, WTF::AtomicString const&, blink::TimingFunction*) /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../third_party/WebKit/Source/core/animation/css/CSSAnimations.cpp:175:60
    #7 0x7f8902f5c568 in blink::CSSAnimations::calculateAnimationUpdate(blink::CSSAnimationUpdate*, blink::Element const*, blink::Element&, blink::ComputedStyle const&, blink::ComputedStyle*, blink::StyleResolver*) /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../third_party/WebKit/Source/core/animation/css/CSSAnimations.cpp:287:17
    #8 0x7f8902f5a890 in blink::CSSAnimations::calculateUpdate(blink::Element const*, blink::Element&, blink::ComputedStyle const&, blink::ComputedStyle*, blink::StyleResolver*) /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../third_party/WebKit/Source/core/animation/css/CSSAnimations.cpp:207:5
    #9 0x7f8903619749 in blink::StyleResolver::applyAnimatedProperties(blink::StyleResolverState&, blink::Element const*) /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../third_party/WebKit/Source/core/css/resolver/StyleResolver.cpp:972:30
    #10 0x7f8903616754 in blink::StyleResolver::styleForElement(blink::Element*, blink::ComputedStyle const*, blink::StyleSharingBehavior, blink::RuleMatchingBehavior) /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../third_party/WebKit/Source/core/css/resolver/StyleResolver.cpp:644:9
    #11 0x7f8901e91907 in blink::Element::originalStyleForLayoutObject() /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../third_party/WebKit/Source/core/dom/Element.cpp:1651:12
    #12 0x7f8901e91262 in blink::Element::styleForLayoutObject() /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../third_party/WebKit/Source/core/dom/Element.cpp:1627:17
    #13 0x7f8901f3bcb5 in blink::LayoutTreeBuilderForElement::style() const /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../third_party/WebKit/Source/core/dom/LayoutTreeBuilder.cpp:114:19
    #14 0x7f8901f3bade in blink::LayoutTreeBuilderForElement::shouldCreateLayoutObject() const /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../third_party/WebKit/Source/core/dom/LayoutTreeBuilder.cpp:108:41
    #15 0x7f8901eb6616 in blink::LayoutTreeBuilderForElement::createLayoutObjectIfNeeded() /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../third_party/WebKit/Source/core/dom/LayoutTreeBuilder.h:84:13
    #16 0x7f8901e8f4d5 in blink::Element::attach(blink::Node::AttachContext const&) /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../third_party/WebKit/Source/core/dom/Element.cpp:1506:9
    #17 0x7f8901c742ad in blink::ContainerNode::attachChildren(blink::Node::AttachContext const&) /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../third_party/WebKit/Source/core/dom/ContainerNode.h:310:13
    #18 0x7f8901c63736 in blink::ContainerNode::attach(blink::Node::AttachContext const&) /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../third_party/WebKit/Source/core/dom/ContainerNode.cpp:842:5
    #19 0x7f8901e8f5de in blink::Element::attach(blink::Node::AttachContext const&) /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../third_party/WebKit/Source/core/dom/Element.cpp:1518:5
    #20 0x7f8901c742ad in blink::ContainerNode::attachChildren(blink::Node::AttachContext const&) /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../third_party/WebKit/Source/core/dom/ContainerNode.h:310:13
    #21 0x7f8901c63736 in blink::ContainerNode::attach(blink::Node::AttachContext const&) /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../third_party/WebKit/Source/core/dom/ContainerNode.cpp:842:5
    #22 0x7f8901e8f5de in blink::Element::attach(blink::Node::AttachContext const&) /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../third_party/WebKit/Source/core/dom/Element.cpp:1518:5
    #23 0x7f8901fba24b in blink::Node::reattach(blink::Node::AttachContext const&) /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../third_party/WebKit/Source/core/dom/Node.cpp:927:5
    #24 0x7f8901e9340c in blink::Element::recalcOwnStyle(blink::StyleRecalcChange) /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../third_party/WebKit/Source/core/dom/Element.cpp:1728:9
    #25 0x7f8901e9214d in blink::Element::recalcStyle(blink::StyleRecalcChange, blink::Text*) /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../third_party/WebKit/Source/core/dom/Element.cpp:1674:22
    #26 0x7f8901d266c4 in blink::Document::updateStyle(blink::StyleRecalcChange) /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../third_party/WebKit/Source/core/dom/Document.cpp:1813:13
    #27 0x7f8901d24e3e in blink::Document::updateLayoutTree(blink::StyleRecalcChange) /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../third_party/WebKit/Source/core/dom/Document.cpp:1752:5
    #28 0x7f88fb272e71 in blink::Document::updateLayoutTreeIfNeeded() /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../third_party/WebKit/Source/core/dom/Document.h:472:39
    #29 0x7f8903ae6a6f in blink::FrameView::updateLayoutAndStyleIfNeededRecursive() /mnt/data/b/build/slave/ASAN_Debug/build/src/out/Debug/../../third_party/WebKit/Source/core/frame/FrameView.cpp:2559:5

SUMMARY: AddressSanitizer: heap-use-after-free (/usr/local/google/home/rickyz/fa/asan-linux-debug-328577/lib/libblink_web.so+0x25fa67b)
Shadow bytes around the buggy address:
  0x0c10800b9d00: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fa
  0x0c10800b9d10: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fa
  0x0c10800b9d20: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fa
  0x0c10800b9d30: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fa
  0x0c10800b9d40: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fa
=>0x0c10800b9d50: fa fa fa fa fd fd fd fd fd fd fd fd[fd]fd fd fa
  0x0c10800b9d60: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fa
  0x0c10800b9d70: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fa
  0x0c10800b9d80: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fa
  0x0c10800b9d90: fa fa fa fa 00 00 00 00 00 00 00 00 00 00 00 fa
  0x0c10800b9da0: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fa
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07
  Heap left redzone:       fa
  Heap right redzone:      fb
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack partial redzone:   f4
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
==1==ABORTING

It looks like UpdatedAnimationStyle has a raw pointer to an effect model, but the model is destroyed and the pointer becomes invalid. shend@, it looks like you added UpdatedAnimationStyle - mind taking a look at this (and also the trace/repro from the reporter as well - it'd be good to confirm that these crashes have the same root cause).

### ri...@chromium.org (2015-05-06)

Oops, forgot to upload the hand-minimized version.

### in...@chromium.org (2015-05-06)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-05-06)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-05-06)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6409302214967296

Uploader: rickyz@chromium.org
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x60d000079830
Crash State:
  blink::CSSAnimations::maybeApplyPendingUpdate
  blink::Element::styleForLayoutObject
  blink::Element::recalcOwnStyle
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=328345:328348

Minimized Testcase (0.46 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95ikKM54wQawXbMSdOuW8_WI_UqQ0O_H32o-cjY8--IEbXtoYLvqaN3T4DQ0prYP0Py1PyuA8umtHlwQx0d6cUx69UvtE--5SqWCuAEeiNaG2z7O6ckzHzQMbimTFir7IOTNkdTJhkQfgIEJGmnp76vbHs3jg



### cl...@chromium.org (2015-05-07)

[Empty comment from Monorail migration]

### ti...@chromium.org (2015-05-07)

Darren no longer works on Blink, assigning to alancutter :-)

### cl...@chromium.org (2015-05-10)

ClusterFuzz has detected this issue as potentially fixed, but it appears to be flaky.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6409302214967296

Uploader: rickyz@chromium.org
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x60d000079830
Crash State:
  blink::CSSAnimations::maybeApplyPendingUpdate
  blink::Element::styleForLayoutObject
  blink::Element::recalcOwnStyle
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=328345:328348

Minimized Testcase (0.46 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95ikKM54wQawXbMSdOuW8_WI_UqQ0O_H32o-cjY8--IEbXtoYLvqaN3T4DQ0prYP0Py1PyuA8umtHlwQx0d6cUx69UvtE--5SqWCuAEeiNaG2z7O6ckzHzQMbimTFir7IOTNkdTJhkQfgIEJGmnp76vbHs3jg

If you suspect that the result above is incorrect,try re-doing that job on the test case report page.

### bu...@chromium.org (2015-05-12)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=195229

------------------------------------------------------------------
r195229 | alancutter@chromium.org | 2015-05-12T07:47:30.781822Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/animation/css/CSSAnimations.cpp?r1=195229&r2=195228&pathrev=195229
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/animations/multiple-same-animations-asan-crash.html?r1=195229&r2=195228&pathrev=195229

Fix use-after-free on multiple same name CSS Animations with different timings

This change fixes an ASAN use-after-free crash when running two animations
that share the same @keyframes name on the same element with different
timings during a style update.
This scenario rides on an existing bug where we only store the last
animation for a given @keyframes name per element but process updates
for each specified animation on the same animation. This caused a scenario
where updates that replaced the KeyframeEffectModel were also triggering
synthetic keyframe updates on the same animation. The ordering of these
updates left a dangling RawPtr that was then used in appropriately
when updating expired synthetic keyframes.

BUG=484614

Review URL: https://codereview.chromium.org/1136203002
-----------------------------------------------------------------

### al...@chromium.org (2015-05-12)

[Empty comment from Monorail migration]

### in...@chromium.org (2015-05-12)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-05-12)

[Empty comment from Monorail migration]

### la...@google.com (2015-05-13)

[Automated comment] Less than 2 weeks to go before stable on M43, manual review required.

### la...@google.com (2015-05-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2015-05-15)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=195389

------------------------------------------------------------------
r195389 | alancutter@chromium.org | 2015-05-15T03:03:49.196038Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/branches/chromium/2357/LayoutTests/animations/multiple-same-animations-asan-crash.html?r1=195389&r2=195388&pathrev=195389
   M http://src.chromium.org/viewvc/blink/branches/chromium/2357/Source/core/animation/css/CSSAnimations.cpp?r1=195389&r2=195388&pathrev=195389

Merge 195229 "Fix use-after-free on multiple same name CSS Anima..."

> Fix use-after-free on multiple same name CSS Animations with different timings
> 
> This change fixes an ASAN use-after-free crash when running two animations
> that share the same @keyframes name on the same element with different
> timings during a style update.
> This scenario rides on an existing bug where we only store the last
> animation for a given @keyframes name per element but process updates
> for each specified animation on the same animation. This caused a scenario
> where updates that replaced the KeyframeEffectModel were also triggering
> synthetic keyframe updates on the same animation. The ordering of these
> updates left a dangling RawPtr that was then used in appropriately
> when updating expired synthetic keyframes.
> 
> BUG=484614
> 
> Review URL: https://codereview.chromium.org/1136203002

TBR=alancutter@chromium.org

Review URL: https://codereview.chromium.org/1139913008
-----------------------------------------------------------------

### in...@chromium.org (2015-05-21)

[Empty comment from Monorail migration]

### mb...@chromium.org (2015-07-16)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-08-18)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2016-06-24)

As mentioned over email, $3,000 for this report.

### aw...@chromium.org (2016-07-01)

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

This issue was migrated from crbug.com/chromium/484614?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/490504]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40082005)*
