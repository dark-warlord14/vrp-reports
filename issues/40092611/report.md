# Use after free due to document destruction within unload event

| Field | Value |
|-------|-------|
| **Issue ID** | [40092611](https://issues.chromium.org/issues/40092611) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | ax...@gmail.com |
| **Assignee** | ja...@chromium.org |
| **Created** | 2011-07-13 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

Chrome tab is crashing when loading specifically crafted page.

SVG file is loaded from object, then event "onunload" is attached to any object in SVG file.  

Then page is reloaded.  

Event calls functions like write()/writeln()/open() for document that is already unloaded and crash happens.

Crash place depends on how many objects were before last object and how data (data="") was loaded in object.  

Generally, crash happens all a time with code provided in test cases (see attachments) functions body\_start() and event\_code() with producing in most cases following common stack trace:  

0012f53c 01cba6f7 00000000 01cbac5e 018d8200 chrome\_1c30000!WebCore::FrameLoader::detachChildren+0x1d [d:\b\build\slave\chrome-official\build\src\third\_party\webkit\source\webcore\loader\frameloader.cpp @ 2552]  

0012f544 01cbac5e 018d8200 018d8200 00f14c80 chrome\_1c30000!WebCore::FrameLoader::setDocumentLoader+0x25 [d:\b\build\slave\chrome-official\build\src\third\_party\webkit\source\webcore\loader\frameloader.cpp @ 1824]  

0012f560 01cba8cb 018d8200 00000000 00f07000 chrome\_1c30000!WebCore::FrameLoader::transitionToCommitted+0xb9 [d:\b\build\slave\chrome-official\build\src\third\_party\webkit\source\webcore\loader\frameloader.cpp @ 2015]  

0012f6f8 01d2703b 00f07040 01d27094 01868b04 chrome\_1c30000!WebCore::FrameLoader::commitProvisionalLoad+0xd8 [d:\b\build\slave\chrome-official\build\src\third\_party\webkit\source\webcore\loader\frameloader.cpp @ 1912]  

0012f700 01d27094 01868b04 01dc633f 01670000 chrome\_1c30000!WebCore::DocumentLoader::commitIfReady+0x22 [d:\b\build\slave\chrome-official\build\src\third\_party\webkit\source\webcore\loader\documentloader.cpp @ 280]  

0012f708 01dc633f 01670000 00000769 01868b00 chrome\_1c30000!WebCore::DocumentLoader::commitLoad+0x14 [d:\b\build\slave\chrome-official\build\src\third\_party\webkit\source\webcore\loader\documentloader.cpp @ 300]  

0012f71c 01dc5b46 01670000 00000769 00000000 chrome\_1c30000!WebCore::MainResourceLoader::addData+0x3b [d:\b\build\slave\chrome-official\build\src\third\_party\webkit\source\webcore\loader\mainresourceloader.cpp @ 163]  

0012f734 01dc6ba3 01670000 00000769 ffffffff chrome\_1c30000!WebCore::ResourceLoader::didReceiveData+0x1b [d:\b\build\slave\chrome-official\build\src\third\_party\webkit\source\webcore\loader\resourceloader.cpp @ 283]  

0012f75c 01dc5e56 01670000 00000769 ffffffff chrome\_1c30000!WebCore::MainResourceLoader::didReceiveData+0x50 [d:\b\build\slave\chrome-official\build\src\third\_party\webkit\source\webcore\loader\mainresourceloader.cpp @ 455]  

0012f790 01fd9856 00ebd470 01670000 00000769 chrome\_1c30000!WebCore::ResourceLoader::didReceiveData+0x62 [d:\b\build\slave\chrome-official\build\src\third\_party\webkit\source\webcore\loader\resourceloader.cpp @ 431]  

0012f7a4 02565820 0137f698 01670000 00000769 chrome\_1c30000!WebCore::ResourceHandleInternal::didReceiveData+0x38 [d:\b\build\slave\chrome-official\build\src\third\_party\webkit\source\webkit\chromium\src\resourcehandle.cpp @ 171]  

0012f7c4 02014fb4 01670000 00000769 ffffffff chrome\_1c30000!webkit\_glue::WebURLLoaderImpl::Context::OnReceivedData+0x54 [d:\b\build\slave\chrome-official\build\src\webkit\glue\weburlloader\_impl.cc @ 620]  

0012f824 0201553a 019cf6d0 00000049 000000e4 chrome\_1c30000!ResourceDispatcher::OnReceivedData+0x9f [d:\b\build\slave\chrome-official\build\src\content\common\resource\_dispatcher.cc @ 358]  

0012f860 02014dc7 019cf6d0 00f19004 0012fb48 chrome\_1c30000!ResourceDispatcher::DispatchMessageW+0xa0 [d:\b\build\slave\chrome-official\build\src\content\common\resource\_dispatcher.cc @ 504]  

0012f87c 0200b6c4 019cf6d0 0012f8b4 01ff49de chrome\_1c30000!ResourceDispatcher::OnMessageReceived+0xbb [d:\b\build\slave\chrome-official\build\src\content\common\resource\_dispatcher.cc @ 282]  

0012f894 022abf40 019cf6d0 0012fc50 021bc998 chrome\_1c30000!ChildThread::OnMessageReceived+0x1b [d:\b\build\slave\chrome-official\build\src\content\common\child\_thread.cc @ 149]  

0012f8a0 021bc998 0012f900 00f26518 0012fb48 chrome\_1c30000!RunnableMethod<MemoryDetails,void (\_\_thiscall MemoryDetails::\*)(std::vector<ProcessMemoryInformation,std::allocator<ProcessMemoryInformation> > const &),Tuple1<std::vector<ProcessMemoryInformation,std::allocator<ProcessMemoryInformation> > > >::Run+0x17 [d:\b\build\slave\chrome-official\build\src\base\task.h @ 332]  

0012f8c0 021bca1f 00000000 019cf6c0 0012fb48 chrome\_1c30000!MessageLoop::RunTask+0x7d [d:\b\build\slave\chrome-official\build\src\base\message\_loop.cc @ 372]  

0012f8d0 021bcdba 0012fb48 00f0ec20 00f0ec30 chrome\_1c30000!MessageLoop::DeferOrRunPendingTask+0x28 [d:\b\build\slave\chrome-official\build\src\base\message\_loop.cc @ 383]  

0012f900 021d3525 00f19004 0012fb48 00000000 chrome\_1c30000!MessageLoop::DoWork+0x71 [d:\b\build\slave\chrome-official\build\src\base\message\_loop.cc @ 573]  

0012f92c 021bc919 0012fb48 02e638f0 021bc89e chrome\_1c30000!base::MessagePumpDefault::Run+0xc2 [d:\b\build\slave\chrome-official\build\src\base\message\_pump\_default.cc @ 50]  

0012f938 021bc89e 00000000 021bc792 00000000 chrome\_1c30000!MessageLoop::RunInternal+0x31 [d:\b\build\slave\chrome-official\build\src\base\message\_loop.cc @ 347]  

0012f940 021bc792 00000000 00000001 00f19000 chrome\_1c30000!MessageLoop::RunHandler+0x17 [d:\b\build\slave\chrome-official\build\src\base\message\_loop.cc @ 319]  

0012f960 01c3f644 0012fde0 00000001 02e631a8 chrome\_1c30000!MessageLoop::Run+0x15 [d:\b\build\slave\chrome-official\build\src\base\message\_loop.cc @ 244]  

0012fc7c 01c341e7 0012fcc8 00765088 00765518 chrome\_1c30000!RendererMain+0x309 [d:\b\build\slave\chrome-official\build\src\content\renderer\renderer\_main.cc @ 234]  

0012fe3c 004020f9 00400000 0012ff1c 00020998 chrome\_1c30000!ChromeMain+0x653 [d:\b\build\slave\chrome-official\build\src\chrome\app\chrome\_main.cc @ 821]  

0012fec4 0040423d 00400000 0012ff1c fffffffe chrome!MainDllLoader::Launch+0xf0 [d:\b\build\slave\chrome-official\build\src\chrome\app\client\_util.cc @ 250]  

0012ff30 00453a1b 00400000 00000000 00020a62 chrome!wWinMain+0xef [d:\b\build\slave\chrome-official\build\src\chrome\app\chrome\_exe\_main\_win.cc @ 46]  

0012ffc0 7c817077 05382e08 0364f258 7ffdb000 chrome!\_\_tmainCRTStartup+0x112 [f:\dd\vctools\crt\_bld\self\_x86\crt\src\crt0.c @ 263]  

0012fff0 00000000 00453a86 00000000 78746341 kernel32!BaseProcessStart+0x23  

After which for every test case stack continuation may vary (0012f87c is last common for all crashes).

Several notes about test cases:

1. Looks like it does not matters which svg files are loaded and what they contain.
2. In test case event\_code() function, document.write(), document.open() and document.writeln() produce equal results (crash).
3. For test case nr.3 two times appeared error 416 "Requested Range Not Satisfiable" and then disappeared without any code modifications (maybe even another bug at all).
4. Can't detect when, but sometimes instead of "Aw, Snap" appeared tab "It's Dead, Jim" - only on Windows. On Linux it is "Aw, Snap" all a time.
5. When placing into tag "body" onload event for any function (event empty), it affected note 4.
6. Notes 3, 4 and 5 may be the cause of caching issue in Chrome - when data is not able to be loaded in object, it takes from cache old files.
7. Sometimes test case page needs to be reloded after it has been already reloaded after location.reload().
8. For some test cases may be produced two diffrent crash places.

For test case named "not-working-tc1" there is debugging information included, but unfortunately, later I was unable to reproduce it with equal results.  

Later it resulted in the same stack trace as in test case nr.2.

PS: Probably there are only null pointer dereferences and not dangerous invalid memory reads, but I have marked this bug as "Security" just for sure - it could require more investigation for more correct conclusions.

**VERSION**  

Windows XP SP3: 12.0.742.112 stable, 12.0.742.122 stable, 14.0.814.0 canary, 14.0.814.0 dev-m  

Ubuntu 10.04: 12.0.742.112 stable

**REPRODUCTION CASE**  

See below attached test cases with debugging information (only for Windows).

## Attachments

- [working-tc2.tar.gz](attachments/working-tc2.tar.gz) (application/x-gzip; charset=binary, 11.1 KB)
- [not-working-tc1.tar.gz](attachments/not-working-tc1.tar.gz) (application/x-gzip; charset=binary, 3.5 KB)
- [working-tc1.tar.gz](attachments/working-tc1.tar.gz) (application/x-gzip; charset=binary, 11.1 KB)
- [working-tc3.tar.gz](attachments/working-tc3.tar.gz) (application/x-gzip; charset=binary, 10.6 KB)

## Timeline

### sc...@gmail.com (2011-07-14)

I will have a look at this now and see if I can get anything worse than a NULL out of any of the repros.

### sc...@gmail.com (2011-07-14)

Valgrind tells all :)

not-working-tc1.tar.gz
(debug)
ASSERTION FAILED: !needsLayout()
third_party/WebKit/Source/WebCore/page/FrameView.cpp(2473) : virtual void WebCore::FrameView::paintContents(WebCore::GraphicsContext*, const WebCore::IntRect&)

(release)
==19356== Invalid read of size 8
==19356==    at 0x1CA78D0: WebCore::FrameLoader::detachChildren() (in /home/chris/chrome/src/out/Release/chrome)
==19356==    by 0x1CA791D: WebCore::FrameLoader::setDocumentLoader(WebCore::DocumentLoader*) (in /home/chris/chrome/src/out/Release/chrome)
==19356==    by 0x1CA8D43: WebCore::FrameLoader::transitionToCommitted(WTF::PassRefPtr<WebCore::CachedPage>) (in /home/chris/chrome/src/out/Release/chrome)
==19356==    by 0x1CACE67: WebCore::FrameLoader::commitProvisionalLoad() (in /home/chris/chrome/src/out/Release/chrome)
==19356==    by 0x1C9106E: WebCore::DocumentLoader::commitLoad(char const*, int) (in /home/chris/chrome/src/out/Release/chrome)
==19356==    by 0x1CCFB52: WebCore::ResourceLoader::didReceiveData(char const*, int, long long, bool) (in /home/chris/chrome/src/out/Release/chrome)
==19356==    by 0x1CBA5F4: WebCore::MainResourceLoader::didReceiveData(char const*, int, long long, bool) (in /home/chris/chrome/src/out/Release/chrome)
==19356==    by 0x1CCF724: WebCore::ResourceLoader::didReceiveData(WebCore::ResourceHandle*, char const*, int, int) (in /home/chris/chrome/src/out/Release/chrome)
==19356==    by 0x1615256: ResourceDispatcher::OnReceivedData(IPC::Message const&, int, base::FileDescriptor, int, int) (in /home/chris/chrome/src/out/Release/chrome)
==19356==    by 0x1613771: bool IPC::MessageWithTuple<Tuple4<int, base::FileDescriptor, int, int> >::Dispatch<ResourceDispatcher, ResourceDispatcher, int, base::FileDescriptor, int, int>(IPC::Message const*, ResourceDispatcher*, ResourceDispatcher*, void (ResourceDispatcher::*)(IPC::Message const&, int, base::FileDescriptor, int, int)) (in /home/chris/chrome/src/out/Release/chrome)
==19356==    by 0x16156FE: ResourceDispatcher::DispatchMessage(IPC::Message const&) (in /home/chris/chrome/src/out/Release/chrome)
==19356==    by 0x1616455: ResourceDispatcher::OnMessageReceived(IPC::Message const&) (in /home/chris/chrome/src/out/Release/chrome)
==19356==    by 0x15B4850: ChildThread::OnMessageReceived(IPC::Message const&) (in /home/chris/chrome/src/out/Release/chrome)
==19356==    by 0xEF3CDD: (anonymous namespace)::TaskClosureAdapter::Run() (in /home/chris/chrome/src/out/Release/chrome)
==19356==    by 0xEF8B16: MessageLoop::RunTask(MessageLoop::PendingTask const&) (in /home/chris/chrome/src/out/Release/chrome)
==19356==    by 0xEF90E7: MessageLoop::DeferOrRunPendingTask(MessageLoop::PendingTask const&) (in /home/chris/chrome/src/out/Release/chrome)
==19356==    by 0xEF941F: MessageLoop::DoWork() (in /home/chris/chrome/src/out/Release/chrome)
==19356==    by 0xEFB0C8: base::MessagePumpDefault::Run(base::MessagePump::Delegate*) (in /home/chris/chrome/src/out/Release/chrome)
==19356==    by 0xEF7195: MessageLoop::RunInternal() (in /home/chris/chrome/src/out/Release/chrome)
==19356==    by 0xEF734B: MessageLoop::Run() (in /home/chris/chrome/src/out/Release/chrome)
==19356==    by 0x24ED5EE: RendererMain(MainFunctionParams const&) (in /home/chris/chrome/src/out/Release/chrome)
==19356==    by 0x62A160: ChromeMain (in /home/chris/chrome/src/out/Release/chrome)
==19356==    by 0x62ACA0: main (in /home/chris/chrome/src/out/Release/chrome)
==19356==  Address 0x128a5360 is 80 bytes inside a block of size 2,344 free'd
==19356==    at 0x4C28146: free (vg_replace_malloc.c:913)
==19356==    by 0x1D2CACF: WebCore::FrameView::~FrameView() (in /home/chris/chrome/src/out/Release/chrome)
==19356==    by 0x1F34625: WTF::HashTable<WTF::RefPtr<WebCore::Widget>, std::pair<WTF::RefPtr<WebCore::Widget>, WebCore::FrameView*>, WTF::PairFirstExtractor<std::pair<WTF::RefPtr<WebCore::Widget>, WebCore::FrameView*> >, WTF::PtrHash<WTF::RefPtr<WebCore::Widget> >, WTF::PairHashTraits<WTF::HashTraits<WTF::RefPtr<WebCore::Widget> >, WTF::HashTraits<WebCore::FrameView*> >, WTF::HashTraits<WTF::RefPtr<WebCore::Widget> > >::deallocateTable(std::pair<WTF::RefPtr<WebCore::Widget>, WebCore::FrameView*>*, int) (in /home/chris/chrome/src/out/Release/chrome)
==19356==    by 0x1F353CC: WebCore::RenderWidget::resumeWidgetHierarchyUpdates() (in /home/chris/chrome/src/out/Release/chrome)
==19356==    by 0x18E8244: WebCore::ContainerNode::removeChildren() (in /home/chris/chrome/src/out/Release/chrome)
==19356==    by 0x18FE844: WebCore::Document::implicitOpen() (in /home/chris/chrome/src/out/Release/chrome)
==19356==    by 0x190785D: WebCore::Document::open(WebCore::Document*) (in /home/chris/chrome/src/out/Release/chrome)
==19356==    by 0x1907A04: WebCore::Document::write(WebCore::SegmentedString const&, WebCore::Document*) (in /home/chris/chrome/src/out/Release/chrome)
==19356==    by 0x1907AB9: WebCore::Document::write(WTF::String const&, WebCore::Document*) (in /home/chris/chrome/src/out/Release/chrome)
==19356==    by 0x1B16EDD: WebCore::V8HTMLDocument::writeCallback(v8::Arguments const&) (in /home/chris/chrome/src/out/Release/chrome)
==19356==    by 0x1306C2C: v8::internal::Builtin_HandleApiCall(v8::internal::(anonymous namespace)::BuiltinArguments<(v8::internal::BuiltinExtraArguments)1>, v8::internal::Isolate*) (in /home/chris/chrome/src/out/Release/chrome)


So it's a use-after-free; thanks for filing as security.
Adam, any initial thoughts? Looks like a document / frame loading interaction.

### sc...@gmail.com (2011-07-14)

working-tc1.tar.gz is similar

working-tc2.tar.gz gives a largely similar but ever so slightly different-looking use-after-free:
==19526== Invalid read of size 8
==19526==    at 0x1CA78D0: WebCore::FrameLoader::detachChildren() (in /home/chris/chrome/src/out/Release/chrome)
==19526==    by 0x1CA791D: WebCore::FrameLoader::setDocumentLoader(WebCore::DocumentLoader*) (in /home/chris/chrome/src/out/Release/chrome)
==19526==    by 0x1CA8D43: WebCore::FrameLoader::transitionToCommitted(WTF::PassRefPtr<WebCore::CachedPage>) (in /home/chris/chrome/src/out/Release/chrome)
==19526==    by 0x1CACE67: WebCore::FrameLoader::commitProvisionalLoad() (in /home/chris/chrome/src/out/Release/chrome)
==19526==    by 0x1C9106E: WebCore::DocumentLoader::commitLoad(char const*, int) (in /home/chris/chrome/src/out/Release/chrome)
==19526==    by 0x1CCFB52: WebCore::ResourceLoader::didReceiveData(char const*, int, long long, bool) (in /home/chris/chrome/src/out/Release/chrome)
==19526==    by 0x1CBA5F4: WebCore::MainResourceLoader::didReceiveData(char const*, int, long long, bool) (in /home/chris/chrome/src/out/Release/chrome)
==19526==    by 0x1CCF724: WebCore::ResourceLoader::didReceiveData(WebCore::ResourceHandle*, char const*, int, int) (in /home/chris/chrome/src/out/Release/chrome)
==19526==    by 0x1615256: ResourceDispatcher::OnReceivedData(IPC::Message const&, int, base::FileDescriptor, int, int) (in /home/chris/chrome/src/out/Release/chrome)
==19526==    by 0x1613771: bool IPC::MessageWithTuple<Tuple4<int, base::FileDescriptor, int, int> >::Dispatch<ResourceDispatcher, ResourceDispatcher, int, base::FileDescriptor, int, int>(IPC::Message const*, ResourceDispatcher*, ResourceDispatcher*, void (ResourceDispatcher::*)(IPC::Message const&, int, base::FileDescriptor, int, int)) (in /home/chris/chrome/src/out/Release/chrome)
==19526==    by 0x16156FE: ResourceDispatcher::DispatchMessage(IPC::Message const&) (in /home/chris/chrome/src/out/Release/chrome)
==19526==    by 0x1616455: ResourceDispatcher::OnMessageReceived(IPC::Message const&) (in /home/chris/chrome/src/out/Release/chrome)
==19526==    by 0x15B4850: ChildThread::OnMessageReceived(IPC::Message const&) (in /home/chris/chrome/src/out/Release/chrome)
==19526==    by 0xEF3CDD: (anonymous namespace)::TaskClosureAdapter::Run() (in /home/chris/chrome/src/out/Release/chrome)
==19526==    by 0xEF8B16: MessageLoop::RunTask(MessageLoop::PendingTask const&) (in /home/chris/chrome/src/out/Release/chrome)
==19526==    by 0xEF90E7: MessageLoop::DeferOrRunPendingTask(MessageLoop::PendingTask const&) (in /home/chris/chrome/src/out/Release/chrome)
==19526==    by 0xEF941F: MessageLoop::DoWork() (in /home/chris/chrome/src/out/Release/chrome)
==19526==    by 0xEFB0C8: base::MessagePumpDefault::Run(base::MessagePump::Delegate*) (in /home/chris/chrome/src/out/Release/chrome)
==19526==    by 0xEF7195: MessageLoop::RunInternal() (in /home/chris/chrome/src/out/Release/chrome)
==19526==    by 0xEF734B: MessageLoop::Run() (in /home/chris/chrome/src/out/Release/chrome)
==19526==    by 0x24ED5EE: RendererMain(MainFunctionParams const&) (in /home/chris/chrome/src/out/Release/chrome)
==19526==    by 0x62A160: ChromeMain (in /home/chris/chrome/src/out/Release/chrome)
==19526==    by 0x62ACA0: main (in /home/chris/chrome/src/out/Release/chrome)
==19526==  Address 0x12743760 is 80 bytes inside a block of size 2,344 free'd
==19526==    at 0x4C28146: free (vg_replace_malloc.c:913)
==19526==    by 0x197C8BF: WebCore::HTMLFrameOwnerElement::willRemove() (in /home/chris/chrome/src/out/Release/chrome)
==19526==    by 0x18E7474: WebCore::ContainerNode::willRemove() (in /home/chris/chrome/src/out/Release/chrome)
==19526==    by 0x18E7474: WebCore::ContainerNode::willRemove() (in /home/chris/chrome/src/out/Release/chrome)
==19526==    by 0x18E7474: WebCore::ContainerNode::willRemove() (in /home/chris/chrome/src/out/Release/chrome)
==19526==    by 0x18E80F3: WebCore::ContainerNode::removeChildren() (in /home/chris/chrome/src/out/Release/chrome)
==19526==    by 0x18FE844: WebCore::Document::implicitOpen() (in /home/chris/chrome/src/out/Release/chrome)
==19526==    by 0x190785D: WebCore::Document::open(WebCore::Document*) (in /home/chris/chrome/src/out/Release/chrome)
==19526==    by 0x1907A04: WebCore::Document::write(WebCore::SegmentedString const&, WebCore::Document*) (in /home/chris/chrome/src/out/Release/chrome)
==19526==    by 0x1907AB9: WebCore::Document::write(WTF::String const&, WebCore::Document*) (in /home/chris/chrome/src/out/Release/chrome)
==19526==    by 0x1B16EDD: WebCore::V8HTMLDocument::writeCallback(v8::Arguments const&) (in /home/chris/chrome/src/out/Release/chrome)
==19526==    by 0x1306C2C: v8::internal::Builtin_HandleApiCall(v8::internal::(anonymous namespace)::BuiltinArguments<(v8::internal::BuiltinExtraArguments)1>, v8::internal::Isolate*) (in /home/chris/chrome/src/out/Release/chrome)

And working-tc3.tar.gz crashes with maybe just a NULL (after clicking 'ok' and then hitting refresh)

==19579== Invalid read of size 4
==19579==    at 0x1C9087A: WebCore::DocumentLoader::isLoadingInAPISense() const (in /home/chris/chrome/src/out/Release/chrome)
==19579==    by 0x164EB27: WebKit::WebFrameImpl::currentHistoryItem() const (in /home/chris/chrome/src/out/Release/chrome)
==19579==    by 0x24D0ECE: RenderView::OnNavigate(ViewMsg_Navigate_Params const&) (in /home/chris/chrome/src/out/Release/chrome)
==19579==    by 0x24DFFDA: RenderView::OnMessageReceived(IPC::Message const&) (in /home/chris/chrome/src/out/Release/chrome)
==19579==    by 0x1608F89: MessageRouter::RouteMessage(IPC::Message const&) (in /home/chris/chrome/src/out/Release/chrome)
==19579==    by 0xEF3CDD: (anonymous namespace)::TaskClosureAdapter::Run() (in /home/chris/chrome/src/out/Release/chrome)
==19579==    by 0xEF8B16: MessageLoop::RunTask(MessageLoop::PendingTask const&) (in /home/chris/chrome/src/out/Release/chrome)
==19579==    by 0xEF90E7: MessageLoop::DeferOrRunPendingTask(MessageLoop::PendingTask const&) (in /home/chris/chrome/src/out/Release/chrome)
==19579==    by 0xEF941F: MessageLoop::DoWork() (in /home/chris/chrome/src/out/Release/chrome)
==19579==    by 0xEFB0C8: base::MessagePumpDefault::Run(base::MessagePump::Delegate*) (in /home/chris/chrome/src/out/Release/chrome)
==19579==    by 0xEF7195: MessageLoop::RunInternal() (in /home/chris/chrome/src/out/Release/chrome)
==19579==    by 0xEF734B: MessageLoop::Run() (in /home/chris/chrome/src/out/Release/chrome)
==19579==    by 0x24ED5EE: RendererMain(MainFunctionParams const&) (in /home/chris/chrome/src/out/Release/chrome)
==19579==    by 0x62A160: ChromeMain (in /home/chris/chrome/src/out/Release/chrome)
==19579==    by 0x62ACA0: main (in /home/chris/chrome/src/out/Release/chrome)
==19579==  Address 0x268 is not stack'd, malloc'd or (recently) free'd


### in...@chromium.org (2011-07-15)

Reduced testcase
test.html
<html>
    <body>
        <script>
            function runTest() {
                var test = document.getElementById('root').contentDocument;
                test.firstChild.setAttribute('onunload', "parent.clearUs();");
                location.reload();
            }
            function clearUs() {
                document.write();
            }
        </script>
        <object data="does_not_exist"></object>
        <object data="1.svg" id="root" onload="runTest();"></object>
    </body>
</html>

1.svg
<svg xmlns="http://www.w3.org/2000/svg">
</svg>

ASAN Stacktrace:


==27424== ERROR: AddressSanitizer crashed on address 0x00007f0b12949150 at pc 0x7f0b5f3ff600 bp 0x7f0b4155af00 sp 0x7f0b4155aee8
READ of size 8 at 0x00007f0b12949150 thread T12
    #0 0x7f0b5f3ff600 in WebCore::FrameTree::previousSibling() const third_party/WebKit/Source/WebCore/page/FrameTree.h:50
    #1 0x7f0b602cf980 in WebCore::FrameLoader::detachChildren() third_party/WebKit/Source/WebCore/loader/FrameLoader.cpp:2325
    #2 0x7f0b602d4b1c in WebCore::FrameLoader::setDocumentLoader(WebCore::DocumentLoader*) third_party/WebKit/Source/WebCore/loader/FrameLoader.cpp:1648
    #3 0x7f0b602d5e1e in WebCore::FrameLoader::transitionToCommitted(WTF::PassRefPtr<WebCore::CachedPage>) third_party/WebKit/Source/WebCore/loader/FrameLoader.cpp:1825
    #4 0x7f0b602d5174 in WebCore::FrameLoader::commitProvisionalLoad() third_party/WebKit/Source/WebCore/loader/FrameLoader.cpp:1729
    #5 0x7f0b6029f93c in WebCore::DocumentLoader::commitLoad(char const*, int) third_party/WebKit/Source/WebCore/loader/DocumentLoader.cpp:300
    #6 0x7f0b60303a72 in WebCore::ResourceLoader::didReceiveData(char const*, int, long long, bool) third_party/WebKit/Source/WebCore/loader/ResourceLoader.cpp:284
    #7 0x7f0b602ed6b0 in WebCore::MainResourceLoader::didReceiveData(char const*, int, long long, bool) third_party/WebKit/Source/WebCore/loader/MainResourceLoader.cpp:464
    #8 0x7f0b603048f9 in WebCore::ResourceLoader::didReceiveData(WebCore::ResourceHandle*, char const*, int, int) third_party/WebKit/Source/WebCore/loader/ResourceLoader.cpp:439
    #9 0x7f0b5f375704 in ResourceDispatcher::OnReceivedData(IPC::Message const&, int, base::FileDescriptor, int, int) content/common/resource_dispatcher.cc:354
    #10 0x7f0b5f376b40 in bool IPC::MessageWithTuple<Tuple4<int, base::FileDescriptor, int, int> >::Dispatch<ResourceDispatcher, ResourceDispatcher, int, base::FileDescriptor, int, int>(IPC::Message const*, ResourceDispatcher*, ResourceDispatcher*, void (ResourceDispatcher::*)(IPC::Message const&, int, base::FileDescriptor, int, int)) ./ipc/ipc_message_utils.h:1012
    #11 0x7f0b5f374f6b in ResourceDispatcher::DispatchMessage(IPC::Message const&) content/common/resource_dispatcher.cc:500
    #12 0x7f0b5f3743bd in ResourceDispatcher::OnMessageReceived(IPC::Message const&) content/common/resource_dispatcher.cc:277
    #13 0x7f0b5f2a2a98 in ChildThread::OnMessageReceived(IPC::Message const&) content/common/child_thread.cc:149
    #14 0x7f0b5f3c72fe in IPC::ChannelProxy::Context::OnDispatchMessage(IPC::Message const&) ipc/ipc_channel_proxy.cc:262
    #15 0x7f0b5e1568d9 in (anonymous namespace)::TaskClosureAdapter::Run() base/message_loop.cc:104
    #16 0x7f0b5e158e02 in MessageLoop::RunTask(MessageLoop::PendingTask const&) base/message_loop.cc:485
    #17 0x7f0b5e159244 in MessageLoop::DeferOrRunPendingTask(MessageLoop::PendingTask const&) base/message_loop.cc:502
    #18 0x7f0b5e1595d3 in MessageLoop::DoWork() base/message_loop.cc:693
    #19 0x7f0b5e1652fb in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) base/message_pump_default.cc:23
    #20 0x7f0b5e1587f8 in MessageLoop::RunInternal() base/message_loop.cc:451
    #21 0x7f0b5e157774 in MessageLoop::Run() base/message_loop.cc:349
    #22 0x7f0b5e1bb011 in base::Thread::ThreadMain() base/threading/thread.cc:164
    #23 0x7f0b5e1ba21c in base::(anonymous namespace)::ThreadFunc(void*) base/threading/platform_thread_posix.cc:51
    #24 0x7f0b61c7dcd3 in AsanThread::ThreadStart() /home/kcc/asan/asan/asan_thread.cc:77
    #25 0x7f0b58d609ca in start_thread ??:0
    #26 0x7f0b56cbe70d in __clone ??:0
0x00007f0b12949150 is located 80 bytes inside of 2344-byte region [0x00007f0b12949100,0x00007f0b12949a28)
freed by thread T12 here:
    #0 0x7f0b61c79776 in free _asan_rtl_
    #1 0x7f0b5fbe1b32 in WebCore::HTMLFrameOwnerElement::willRemove() third_party/WebKit/Source/WebCore/html/HTMLFrameOwnerElement.cpp:62
    #2 0x7f0b5faa36d7 in WebCore::ContainerNode::willRemove() third_party/WebKit/Source/WebCore/dom/ContainerNode.cpp:379
    #3 0x7f0b5faa36d7 in WebCore::ContainerNode::willRemove() third_party/WebKit/Source/WebCore/dom/ContainerNode.cpp:379
    #4 0x7f0b5faa421c in WebCore::willRemoveChildren(WebCore::ContainerNode*) third_party/WebKit/Source/WebCore/dom/ContainerNode.cpp:403
    #5 0x7f0b5faa3c4d in WebCore::ContainerNode::removeChildren() third_party/WebKit/Source/WebCore/dom/ContainerNode.cpp:536
    #6 0x7f0b5fac23eb in WebCore::Document::implicitOpen() third_party/WebKit/Source/WebCore/dom/Document.cpp:1992
    #7 0x7f0b5faba2c8 in WebCore::Document::open(WebCore::Document*) third_party/WebKit/Source/WebCore/dom/Document.cpp:1955
    #8 0x7f0b5fac395b in WebCore::Document::write(WebCore::SegmentedString const&, WebCore::Document*) third_party/WebKit/Source/WebCore/dom/Document.cpp:2259
    #9 0x7f0b5fac3b43 in WebCore::Document::write(WTF::String const&, WebCore::Document*) third_party/WebKit/Source/WebCore/dom/Document.cpp:2272
    #10 0x7f0b5ff88da3 in WebCore::V8HTMLDocument::writeCallback(v8::Arguments const&) third_party/WebKit/Source/WebCore/bindings/v8/custom/V8HTMLDocumentCustom.cpp:116
    #11 0x7f0b5ea1f5f8 in HandleApiCallHelper v8/src/builtins.cc:1105
    #12 0x7f0b1b50214e in  
previously allocated by thread T12 here:
    #0 0x7f0b61c79866 in malloc _asan_rtl_
    #1 0x7f0b5f8fad89 in WTF::fastMalloc(unsigned long) third_party/WebKit/Source/JavaScriptCore/wtf/FastMalloc.cpp:248
    #2 0x7f0b603989d7 in WebCore::Frame::create(WebCore::Page*, WebCore::HTMLFrameOwnerElement*, WebCore::FrameLoaderClient*) third_party/WebKit/Source/WebCore/page/Frame.cpp:205
    #3 0x7f0b5f40e324 in WebKit::WebFrameImpl::createChildFrame(WebCore::FrameLoadRequest const&, WebCore::HTMLFrameOwnerElement*) third_party/WebKit/Source/WebKit/chromium/src/WebFrameImpl.cpp:1897
    #4 0x7f0b5f4a6d8a in WebKit::FrameLoaderClientImpl::createFrame(WebCore::KURL const&, WTF::String const&, WebCore::HTMLFrameOwnerElement*, WTF::String const&, bool, int, int) third_party/WebKit/Source/WebKit/chromium/src/FrameLoaderClientImpl.cpp:1439
    #5 0x7f0b603079c0 in WebCore::SubframeLoader::loadSubframe(WebCore::HTMLFrameOwnerElement*, WebCore::KURL const&, WTF::String const&, WTF::String const&) third_party/WebKit/Source/WebCore/loader/SubframeLoader.cpp:265
    #6 0x7f0b60305b18 in WebCore::SubframeLoader::loadOrRedirectSubframe(WebCore::HTMLFrameOwnerElement*, WebCore::KURL const&, WTF::AtomicString const&, bool, bool) third_party/WebKit/Source/WebCore/loader/SubframeLoader.cpp:240
    #7 0x7f0b60306c1b in WebCore::SubframeLoader::requestObject(WebCore::HTMLPlugInImageElement*, WTF::String const&, WTF::AtomicString const&, WTF::String const&, WTF::Vector<WTF::String, 0ul> const&, WTF::Vector<WTF::String, 0ul> const&) third_party/WebKit/Source/WebCore/loader/SubframeLoader.cpp:147
    #8 0x7f0b5fc091ae in WebCore::HTMLObjectElement::updateWidget(WebCore::PluginCreationOption) third_party/WebKit/Source/WebCore/html/HTMLObjectElement.cpp:333
    #9 0x7f0b5faa46af in WebCore::ContainerNode::dispatchPostAttachCallbacks() third_party/WebKit/Source/WebCore/dom/ContainerNode.cpp:747
    #10 0x7f0b5faa4582 in WebCore::ContainerNode::resumePostAttachCallbacks() third_party/WebKit/Source/WebCore/dom/ContainerNode.cpp:713
    #11 0x7f0b5fb09781 in WebCore::Element::attach() third_party/WebKit/Source/WebCore/dom/Element.cpp:1039
    #12 0x7f0b5fc11fed in WebCore::HTMLPlugInImageElement::attach() third_party/WebKit/Source/WebCore/html/HTMLPlugInImageElement.cpp:139
    #13 0x7f0b5fd03e75 in WTF::PassRefPtr<WebCore::Element> WebCore::HTMLConstructionSite::attach<WebCore::Element>(WebCore::ContainerNode*, WTF::PassRefPtr<WebCore::Element>) third_party/WebKit/Source/WebCore/html/parser/HTMLConstructionSite.cpp:112
    #14 0x7f0b5fd052a4 in WebCore::HTMLConstructionSite::attachToCurrent(WTF::PassRefPtr<WebCore::Element>) third_party/WebKit/Source/WebCore/html/parser/HTMLConstructionSite.cpp:265
    #15 0x7f0b5fd05e2e in WebCore::HTMLConstructionSite::insertHTMLElement(WebCore::AtomicHTMLToken&) third_party/WebKit/Source/WebCore/html/parser/HTMLConstructionSite.cpp:295
Thread T12 created by T0 here:
    #0 0x7f0b61c78a07 in pthread_create _asan_rtl_
    #1 0x7f0b5e1ba001 in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThread::Delegate*, unsigned long*) base/threading/platform_thread_posix.cc:109
    #2 0x7f0b5e1b9eca in base::PlatformThread::Create(unsigned long, base::PlatformThread::Delegate*, unsigned long*) base/threading/platform_thread_posix.cc:203
    #3 0x7f0b5e1ba833 in base::Thread::StartWithOptions(base::Thread::Options const&) base/threading/thread.cc:74
    #4 0x7f0b61006318 in BrowserRenderProcessHost::Init(bool) content/browser/renderer_host/browser_render_process_host.cc:305
    #5 0x7f0b6104e28a in RenderViewHost::CreateRenderView(std::basic_string<unsigned short, base::string16_char_traits, std::allocator<unsigned short> > const&) content/browser/renderer_host/render_view_host.cc:147
    #6 0x7f0b610de46e in TabContents::CreateRenderViewForRenderManager(RenderViewHost*) content/browser/tab_contents/tab_contents.cc:1771
    #7 0x7f0b610de58d in non-virtual thunk to TabContents::CreateRenderViewForRenderManager(RenderViewHost*) ??:0
    #8 0x7f0b610ccc5b in RenderViewHostManager::InitRenderView(RenderViewHost*, NavigationEntry const&) content/browser/tab_contents/render_view_host_manager.cc:560
    #9 0x7f0b610cbe24 in RenderViewHostManager::Navigate(NavigationEntry const&) content/browser/tab_contents/render_view_host_manager.cc:101
    #10 0x7f0b610d786c in TabContents::NavigateToEntry(NavigationEntry const&, NavigationController::ReloadType) content/browser/tab_contents/tab_contents.cc:523
    #11 0x7f0b610d77d5 in TabContents::NavigateToPendingEntry(NavigationController::ReloadType) content/browser/tab_contents/tab_contents.cc:517
    #12 0x7f0b610c17be in NavigationController::NavigateToPendingEntry(NavigationController::ReloadType) content/browser/tab_contents/navigation_controller.cc:1043
    #13 0x7f0b610c201a in NavigationController::LoadEntry(NavigationEntry*) content/browser/tab_contents/navigation_controller.cc:276
    #14 0x7f0b5d478809 in browser::Navigate(browser::NavigateParams*) chrome/browser/ui/browser_navigator.cc:451
    #15 0x7f0b5d46ac7f in BrowserInit::LaunchWithProfile::OpenTabsInBrowser(Browser*, bool, std::vector<BrowserInit::LaunchWithProfile::Tab, std::allocator<BrowserInit::LaunchWithProfile::Tab> > const&) chrome/browser/ui/browser_init.cc:1023
    #16 0x7f0b5d4695cc in BrowserInit::LaunchWithProfile::ProcessStartupURLs(std::vector<GURL, std::allocator<GURL> > const&) chrome/browser/ui/browser_init.cc:933
    #17 0x7f0b5d4685fe in BrowserInit::LaunchWithProfile::ProcessLaunchURLs(bool, std::vector<GURL, std::allocator<GURL> > const&) chrome/browser/ui/browser_init.cc:850
    #18 0x7f0b5d46778b in BrowserInit::LaunchWithProfile::Launch(Profile*, std::vector<GURL, std::allocator<GURL> > const&, bool) chrome/browser/ui/browser_init.cc:693
    #19 0x7f0b5d4668da in BrowserInit::LaunchBrowser(CommandLine const&, Profile*, FilePath const&, bool, int*) chrome/browser/ui/browser_init.cc:549
    #20 0x7f0b5d46c57c in BrowserInit::ProcessCmdLineImpl(CommandLine const&, FilePath const&, bool, Profile*, int*, BrowserInit*) chrome/browser/ui/browser_init.cc:1424
    #21 0x7f0b5d0072da in BrowserInit::Start(CommandLine const&, FilePath const&, Profile*, int*) ./chrome/browser/ui/browser_init.h:38
    #22 0x7f0b5d0052a4 in BrowserMain(MainFunctionParams const&) chrome/browser/browser_main.cc:1974
    #23 0x7f0b5cff34c4 in (anonymous namespace)::RunNamedProcessTypeMain(std::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, MainFunctionParams const&) chrome/app/chrome_main.cc:532
    #24 0x7f0b5cff2546 in ChromeMain chrome/app/chrome_main.cc:858
    #25 0x7f0b5cff4582 in main chrome/app/chrome_exe_main_gtk.cc:46
    #26 0x7f0b56bf6c4d in __libc_start_main ??:0
    #27 0x7f0b5cff1ca9 in _start ??:0
==27424== ABORTING
Stats: 0M malloced (0M for red zones) by 0 calls
Stats: 1M realloced by 13366 calls
Stats: 0M freed by 0 calls
Stats: 0M really freed by 0 calls
Stats: 0M (0 pages) mmaped in 0 calls
Stats: 68M of shadow memory allocated in 68 clusters
             (1M each, 0 low and 68 high)
Shadow byte and word:
  0x00001fe16252922a: fb
  0x00001fe162529228: fb fb fb fb fb fb fb fb
More shadow bytes:
  0x00001fe162529208: ff ff ff ff ff ff ff ff
  0x00001fe162529210: ff ff ff ff ff ff ff ff
  0x00001fe162529218: ff ff ff ff ff ff ff ff
  0x00001fe162529220: fb fb fb fb fb fb fb fb
=>0x00001fe162529228: fb fb fb fb fb fb fb fb
  0x00001fe162529230: fb fb fb fb fb fb fb fb
  0x00001fe162529238: fb fb fb fb fb fb fb fb
  0x00001fe162529240: fb fb fb fb fb fb fb fb
  0x00001fe162529248: fb fb fb fb fb fb fb fb

I have verified that it affects m13(782) branch too.

### in...@chromium.org (2011-07-18)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-07-18)

filed tracking webkit bug - https://bugs.webkit.org/show_bug.cgi?id=64741

### kc...@chromium.org (2011-07-21)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-07-27)

@scottmg - Here's some potential bugs to start with. I can CC you upstream if there's one you pan on taking.

### sc...@gmail.com (2011-08-04)

I'm gonna take a look to see how involved this one is, unless anyone objects.

### sc...@chromium.org (2011-08-04)

I've got a patch just about ready for this one. I'll upload tomorrow once I figure out a good way to get a test for it (the reloading business in the repro nukes the test code).

I'd be grateful if you could review it?

### sc...@gmail.com (2011-08-04)

Pleased to meet you Scott, sorry for almost stealing your bug :D
I've assigned it to you and marked it "Started"

Awesome that you're looking at this bug. Not sure I'm the best reviewer, but I can introduce you to one after a quick look at the patch.


### sc...@chromium.org (2011-08-04)

Ah, thanks, I should have marked it. I looked at the WebKit one and saw that it had a magic group assignment that I figured I shouldn't change, but I didn't check back here.

Anyhow, I've upload the patch to the associated webkit bug now, if anyone's up for having a look.

### sc...@gmail.com (2011-08-05)

Thanks Scott for the fix! Let me know if you're up for more :)

Committed r92439: <http://trac.webkit.org/changeset/92439>

### sc...@gmail.com (2011-08-05)

Rolled out upstream, unfortunately.

### in...@chromium.org (2011-08-16)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-08-17)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-08-20)

Nate has a new patch upstream. Nate, think it's related to https://code.google.com/p/chromium/issues/detail?id=89330 ?

### in...@chromium.org (2011-08-22)

http://trac.webkit.org/changeset/93521

### sc...@gmail.com (2011-08-22)

[Empty comment from Monorail migration]

### ke...@google.com (2011-08-22)

Moving back to started until merged.

### sc...@gmail.com (2011-08-22)

Do we have to do that? :P

### sc...@gmail.com (2011-08-24)

@Ax330d: this turns out to be a nice bug in the end -- all sorts of interesting document lifetime issues :)
It looks like you're testing on Windows. Have you considered testing on Linux? Chrome / Linux has some nice tools and integrations, such as the command-line flag "--renderer-cmd-prefix=valgrind" (or there's a better valgrind checked into the Chromium SVN repository). Even on a production build, this will give you very quick differentiation between a NULL ptr and a use-after-free.

Anyway, we're still going to reward at the higher $1000 level because the repros uncovered a nest of related issues in the code.

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

### ax...@gmail.com (2011-08-24)

Great, thanks! 

I will definitely try Linux with tools, but later - currently I don't have such opportunity.

### sc...@gmail.com (2011-08-24)

Merged to M14: http://trac.webkit.org/changeset/93736

### sc...@gmail.com (2011-09-09)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-09-30)

Payment is in system.

### js...@chromium.org (2011-10-05)

Batch update.

### [Deleted User] (2012-05-15)

Marking old security bugs Fixed..

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-01)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-26)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-26)

This issue was migrated from crbug.com/chromium/89219?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/93119]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092611)*
