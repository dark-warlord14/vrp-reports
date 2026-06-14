# Use after free due to style not updated for svg text runs.

| Field | Value |
|-------|-------|
| **Issue ID** | [40094538](https://issues.chromium.org/issues/40094538) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | in...@chromium.org |
| **Assignee** | in...@chromium.org |
| **Created** | 2011-09-01 |
| **Bounty** | $1,000.00 |

## Description

Branched off http://code.google.com/p/chromium/issues/detail?id=92651

## Attachments

- [svgfont.html](attachments/svgfont.html) (text/plain; charset=us-ascii, 239 B)
- [32_1208.html](attachments/32_1208.html) (text/html; charset=us-ascii, 11.0 KB)
- [8_inside_56.txt](attachments/8_inside_56.txt) (text/plain; charset=us-ascii, 12.6 KB)
- [8_inside_56.html](attachments/8_inside_56.html) (text/html; charset=us-ascii, 11.2 KB)
- [ruby_1165_inside_1208.txt](attachments/ruby_1165_inside_1208.txt) (text/plain; charset=us-ascii, 11.1 KB)
- [ruby_1165_inside_1208.html](attachments/ruby_1165_inside_1208.html) (text/html; charset=utf-8, 727 B)

## Timeline

### in...@chromium.org (2011-09-04)

Mitz is fixing this problem in a generic way in https://bugs.webkit.org/show_bug.cgi?id=67552

### in...@chromium.org (2011-09-05)

http://trac.webkit.org/changeset/94508

Miaubiz, can you please try your fuzzers to see this font bug and its variants are fixed. Thanks a lot for finding and helping us with this.

### mi...@gmail.com (2011-09-05)

@inferno: you mean svg or all of missing font stuff?

### mi...@gmail.com (2011-09-05)

something called gelf.h is messing with my build. :|

### in...@chromium.org (2011-09-05)

Miaubiz, i fixed ASAN compile in http://src.chromium.org/viewvc/chrome?view=rev&revision=99658. Can you please try again. LKGR build will take a little time to update, but trunk has the fix.

Regarding your c#3, i meant both svg and other font stuff. I think most or all of them will stop reproducing with this fix.

### gl...@chromium.org (2011-09-05)

BTW, I've updated ASan binaries in r99659, so it's better to sync to that revision instead of 99658.

### in...@chromium.org (2011-09-05)

Thanks a lot Alex.

### mi...@gmail.com (2011-09-05)

after a quick look asan crashes for metrics stuff with 16 inside 1208, 104 inside 1208, 1165 inside 1208 are still there. 

the new asan output is sweet:

ERROR: AddressSanitizer heap-use-after-free on address 0x00007fffe42c7090 at pc 0x7ffff

I have to update my scripts to handle it. 

### in...@chromium.org (2011-09-05)

Miaubiz, can you please attach the repros here. The table bugs will hopefully get 90% resolved (a few exception in tables) and ruby should get 100% resolved by my pending fix in https://crbug.com/chromium/92651. SVG bugs i am not sure if Mitz's patch fixes them. If your repors turn out different bugs, i will file them separately.

### mi...@gmail.com (2011-09-05)

give me a change to minify these if they're different.

8 inside 56..

==22572== ERROR: AddressSanitizer heap-use-after-free on address 0x00007fffde32da88 at pc 0x7ffff2c9f782 bp 0x7fffffff2130 sp 0x7fffffff1e00
READ of size 8 at 0x00007fffde32da88 thread T0
    #0 0x7ffff2c9f782 in WebCore::Font::glyphDataAndPageForCharacter(int, bool, WebCore::FontDataVariant) const ???:0
0x00007fffde32da88 is located 8 bytes inside of 56-byte region [0x00007fffde32da80,0x00007fffde32dab8)
freed by thread T0 here:
    #0 0x7ffff6239cd2 in operator delete(void*) _asan_rtl_
    #1 0x7ffff2cab59a in WebCore::GlyphPageTreeNode::pruneCustomFontData(WebCore::FontData const*) ???:0


### mi...@gmail.com (2011-09-05)

ruby 1165 inside 1208


==29156== ERROR: AddressSanitizer heap-use-after-free on address 0x00007fffe3c3cd0d at pc 0x7ffff39eb83b bp 0x7fffffff3a30 sp 0x7fffffff3940
READ of size 1 at 0x00007fffe3c3cd0d thread T0
    #0 0x7ffff39eb83b in WebCore::InlineFlowBox::requiresIdeographicBaseline(WTF::HashMap<WebCore::InlineTextBox const*, std::pair<WTF::Vector<WebCore::SimpleFontData const*, 0ul>, WebCore::GlyphOverflow>, WTF::PtrHash<WebCore::InlineTextBox const*>, WTF::HashTraits<WebCore::InlineTextBox const*>, WTF::HashTraits<std::pair<WTF::Vector<WebCore::SimpleFontData const*, 0ul>, WebCore::GlyphOverflow> > > const&) const ???:0

0x00007fffe3c3cd0d is located 1165 bytes inside of 1208-byte region [0x00007fffe3c3c880,0x00007fffe3c3cd38)
freed by thread T0 here:
    #0 0x7ffff623a6fa in free _asan_rtl_
    #1 0x7ffff285e46e in WTF::Vector<WTF::OwnPtr<WebCore::FontData>, 0ul>::shrinkCapacity(unsigned long) ???:0
    #2 0x7ffff282520b in WebCore::Document::recalcStyle(WebCore::Node::StyleChange) ???:0


### mi...@gmail.com (2011-09-05)

I'm on this version fwiw.  revision 100k approaching!

Chromium	15.0.873.0 (Developer Build 99671-dirty)
OS	Linux
WebKit	535.2 (trunk@94536)
JavaScript	V8 3.6.0

### mi...@gmail.com (2011-09-05)

zdi's test02.xhtml is still also crashing. so I won't post the 16inside1208 and 104inside1208

### in...@chromium.org (2011-09-05)

is the svg repro still reproducing ? looks like after mitz's fix, the original problem in 92651 (of tables and ruby) still reproduces, right ?

### in...@chromium.org (2011-09-06)

svg repro is definitely not fixed, easily hitting in CLUSTER_FUZZ

Testcase.svg::
<!DOCTYPE svg>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <d:SVGTestCase>
    <d:testDescription>
        </d:testDescription>
    <d:operatorScript>      
      </d:operatorScript>
    <d:passCriteria>
      </d:passCriteria>
  </d:SVGTestCase>
  <title></title>
  <font-face font-family="SVGFreeSansASCII">
      <font-face-src>
        <font-face-uri xlink:href="../custom/resources/SVGFreeSans.svg#ascii"/>
      </font-face-src>
    </font-face>
  <text font-family="SVGFreeSansASCII,sans-serif"><tref xlink:href="#hello"/>
    <text id="hello">>>


/mnt/scratch0/chrome/src/out/Release/chrome --allow-file-access-from-files --disable-click-to-play --disable-hang-monitor --disable-metrics --disable-popup-blocking --disable-prompt-on-repost --enable-desktop-notifications --enable-experimental-extension-apis --enable-extension-apps --enable-extension-timeline-api --enable-geolocation --enable-indexed-database --enable-nacl --enable-native-web-workers --enable-search-provider-api-v2 --force-internal-pdf --incognito --js-flags="--expose-gc" --new-window --no-default-browser-check --no-first-run --no-process-singleton-dialog --no-sandbox --single-process --disable-gpu-plugin --disable-gpu-rendering --disable-accelerated-compositing --disable-webgl --disable-accelerated-2d-canvas --user-data-dir=/mnt/scratch0/FuzzTmp/t250 

ASAN:SIGILL
=================================================================
HINT: if your stack trace looks short or garbled, use ASAN_OPTIONS=fast_unwind=0
==3032== ERROR: AddressSanitizer heap-use-after-free on address 0x00007f2c66bbe8e8 at pc 0x7f2c77c0b7f9 bp 0x7f2c5aa947b0 sp 0x7f2c5aa94660
READ of size 8 at 0x00007f2c66bbe8e8 thread T12
    #0 0x7f2c77c0b7f9 in WebCore::SVGTextMetrics::measureCharacterRange(WebCore::RenderSVGInlineText*, unsigned int, unsigned int) 
    #1 0x7f2c77bf9e4a in WebCore::SVGTextLayoutAttributesBuilder::propagateLayoutAttributes(WebCore::RenderObject*, WTF::Vector<WebCore::SVGTextLayoutAttributes, 0ul>&, unsigned int&, unsigned short&) const 
    #2 0x7f2c77bfb2d2 in WebCore::SVGTextLayoutAttributesBuilder::propagateLayoutAttributes(WebCore::RenderObject*, WTF::Vector<WebCore::SVGTextLayoutAttributes, 0ul>&, unsigned int&, unsigned short&) const 
    #3 0x7f2c77bf850b in WebCore::SVGTextLayoutAttributesBuilder::buildLayoutAttributesForTextSubtree(WebCore::RenderSVGText*) 
    #4 0x7f2c77bc446b in WebCore::RenderSVGText::layout() 
    #5 0x7f2c77bd20f5 in WebCore::SVGRenderSupport::layoutChildren(WebCore::RenderObject*, bool) 
    #6 0x7f2c77edf12a in WebCore::RenderSVGRoot::layout() 
    #7 0x7f2c771e908a in WebCore::RenderBlock::layoutInlineChildren(bool, int&, int&) 
    #8 0x7f2c7715fe21 in WebCore::RenderBlock::layoutBlock(bool, int, WebCore::RenderBlock::BlockLayoutPass) 
    #9 0x7f2c7715eab9 in WebCore::RenderBlock::layout() 
    #10 0x7f2c77179e9a in WebCore::RenderBlock::layoutBlockChild(WebCore::RenderBox*, WebCore::RenderBlock::MarginInfo&, int&, int&) 
    #11 0x7f2c77167c64 in WebCore::RenderBlock::layoutBlockChildren(bool, int&) 
    #12 0x7f2c7715fe45 in WebCore::RenderBlock::layoutBlock(bool, int, WebCore::RenderBlock::BlockLayoutPass) 
    #13 0x7f2c7715eab9 in WebCore::RenderBlock::layout() 
    #14 0x7f2c77179e9a in WebCore::RenderBlock::layoutBlockChild(WebCore::RenderBox*, WebCore::RenderBlock::MarginInfo&, int&, int&) 
    #15 0x7f2c77167c64 in WebCore::RenderBlock::layoutBlockChildren(bool, int&) 
    #16 0x7f2c7715fe45 in WebCore::RenderBlock::layoutBlock(bool, int, WebCore::RenderBlock::BlockLayoutPass) 
    #17 0x7f2c7715eab9 in WebCore::RenderBlock::layout() 
    #18 0x7f2c77179e9a in WebCore::RenderBlock::layoutBlockChild(WebCore::RenderBox*, WebCore::RenderBlock::MarginInfo&, int&, int&) 
    #19 0x7f2c77167c64 in WebCore::RenderBlock::layoutBlockChildren(bool, int&) 
    #20 0x7f2c7715fe45 in WebCore::RenderBlock::layoutBlock(bool, int, WebCore::RenderBlock::BlockLayoutPass) 
    #21 0x7f2c7715eab9 in WebCore::RenderBlock::layout() 
    #22 0x7f2c77411123 in WebCore::RenderView::layout() 
    #23 0x7f2c76c99a8b in WebCore::FrameView::layout(bool) 
    #24 0x7f2c75f6139e in WebCore::Document::implicitClose() 
    #25 0x7f2c76b3dabc in WebCore::FrameLoader::checkCompleted() 
    #26 0x7f2c76be0568 in WebCore::CachedResourceLoader::loadDone() 
    #27 0x7f2c76be7fbe in WebCore::CachedResourceRequest::didFinishLoading(WebCore::SubresourceLoader*, double) 
    #28 0x7f2c76bb0512 in WebCore::SubresourceLoader::didFinishLoading(double) 
    #29 0x7f2c78258695 in webkit_glue::WebURLLoaderImpl::Context::OnCompletedRequest(net::URLRequestStatus const&, std::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, base::Time const&) 
    #30 0x7f2c75a262fc in bool ResourceMsg_RequestComplete::Dispatch<ResourceDispatcher, ResourceDispatcher, void (ResourceDispatcher::*)(int, net::URLRequestStatus const&, std::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, base::Time const&)>(IPC::Message const*, ResourceDispatcher*, ResourceDispatcher*, void (ResourceDispatcher::*)(int, net::URLRequestStatus const&, std::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, base::Time const&)) 
    #31 0x7f2c75a23ec3 in ResourceDispatcher::DispatchMessage(IPC::Message const&) 
    #32 0x7f2c75a21d17 in ResourceDispatcher::OnMessageReceived(IPC::Message const&) 
    #33 0x7f2c75928090 in ChildThread::OnMessageReceived(IPC::Message const&) 
    #34 0x7f2c75a7ca51 in IPC::ChannelProxy::Context::OnDispatchMessage(IPC::Message const&) 
    #35 0x7f2c743be7b9 in base::subtle::TaskClosureAdapter::Run() 
    #36 0x7f2c7434ceae in MessageLoop::RunTask(MessageLoop::PendingTask const&) 
    #37 0x7f2c7434d4a2 in MessageLoop::DeferOrRunPendingTask(MessageLoop::PendingTask const&) 
    #38 0x7f2c7434e691 in MessageLoop::DoWork() 
    #39 0x7f2c7435776a in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) 
    #40 0x7f2c7434bd8a in MessageLoop::RunInternal() 
    #41 0x7f2c74349e89 in MessageLoop::Run() 
    #42 0x7f2c743c1ef8 in base::Thread::ThreadMain() 
    #43 0x7f2c743c0b6c in base::(anonymous namespace)::ThreadFunc(void*) base/threading/platform_thread_posix.cc:0
    #44 0x7f2c799574d1 in AsanThread::ThreadStart() /usr/local/google/asan/address-sanitizer/asan/asan_thread.cc:102
    #45 0x7f2c6e80d9ca in start_thread /build/buildd/eglibc-2.11.1/nptl/pthread_create.c:300
    #46 0x7f2c6c76b70d in ?? /build/buildd/eglibc-2.11.1/misc/../sysdeps/unix/sysv/linux/x86_64/clone.S:114
0x00007f2c66bbe8e8 is located 104 bytes inside of 1208-byte region [0x00007f2c66bbe880,0x00007f2c66bbed38)
freed by thread T12 here:
    #1 0x7f2c75f977ce in WTF::Vector<WTF::OwnPtr<WebCore::FontData>, 0ul>::shrinkCapacity(unsigned long) 
    #2 0x7f2c75f5e56b in WebCore::Document::recalcStyle(WebCore::Node::StyleChange) 
    #3 0x7f2c75f618df in WebCore::Document::updateStyleIfNeeded() 
    #4 0x7f2c75f61267 in WebCore::Document::implicitClose() 
    #5 0x7f2c76b3dabc in WebCore::FrameLoader::checkCompleted() 
    #6 0x7f2c76be0568 in WebCore::CachedResourceLoader::loadDone() 
    #7 0x7f2c76be7fbe in WebCore::CachedResourceRequest::didFinishLoading(WebCore::SubresourceLoader*, double) 
    #8 0x7f2c76bb0512 in WebCore::SubresourceLoader::didFinishLoading(double) 
    #9 0x7f2c78258695 in webkit_glue::WebURLLoaderImpl::Context::OnCompletedRequest(net::URLRequestStatus const&, std::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, base::Time const&) 
    #10 0x7f2c75a262fc in bool ResourceMsg_RequestComplete::Dispatch<ResourceDispatcher, ResourceDispatcher, void (ResourceDispatcher::*)(int, net::URLRequestStatus const&, std::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, base::Time const&)>(IPC::Message const*, ResourceDispatcher*, ResourceDispatcher*, void (ResourceDispatcher::*)(int, net::URLRequestStatus const&, std::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, base::Time const&)) 
    #11 0x7f2c75a23ec3 in ResourceDispatcher::DispatchMessage(IPC::Message const&) 
    #12 0x7f2c75a21d17 in ResourceDispatcher::OnMessageReceived(IPC::Message const&) 
    #13 0x7f2c75928090 in ChildThread::OnMessageReceived(IPC::Message const&) 
    #14 0x7f2c75a7ca51 in IPC::ChannelProxy::Context::OnDispatchMessage(IPC::Message const&) 
    #15 0x7f2c743be7b9 in base::subtle::TaskClosureAdapter::Run() 
    #16 0x7f2c7434ceae in MessageLoop::RunTask(MessageLoop::PendingTask const&) 
    #17 0x7f2c7434d4a2 in MessageLoop::DeferOrRunPendingTask(MessageLoop::PendingTask const&) 
    #18 0x7f2c7434e691 in MessageLoop::DoWork() 
    #19 0x7f2c7435776a in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) 
    #20 0x7f2c7434bd8a in MessageLoop::RunInternal() 
    #21 0x7f2c74349e89 in MessageLoop::Run() 
    #22 0x7f2c743c1ef8 in base::Thread::ThreadMain() 
    #23 0x7f2c743c0b6c in base::(anonymous namespace)::ThreadFunc(void*) base/threading/platform_thread_posix.cc:0
    #24 0x7f2c799574d1 in AsanThread::ThreadStart() /usr/local/google/asan/address-sanitizer/asan/asan_thread.cc:102
previously allocated by thread T12 here:
    #1 0x7f2c75c1845b in WTF::fastMalloc(unsigned long) 
    #2 0x7f2c770cdd18 in WebCore::CSSFontFaceSource::getFontData(WebCore::FontDescription const&, bool, bool, WebCore::CSSFontSelector*) 
    #3 0x7f2c770cabb9 in WebCore::CSSFontFace::getFontData(WebCore::FontDescription const&, bool, bool) 
    #4 0x7f2c76e5b26c in WebCore::CSSSegmentedFontFace::getFontData(WebCore::FontDescription const&) 
    #5 0x7f2c76e2d88e in WebCore::CSSFontSelector::getFontData(WebCore::FontDescription const&, WTF::AtomicString const&) 
    #6 0x7f2c763cd16e in WebCore::FontCache::getFontData(WebCore::Font const&, int&, WebCore::FontSelector*) 
    #7 0x7f2c763d6c36 in WebCore::FontFallbackList::fontDataAt(WebCore::Font const*, unsigned int) const 
    #8 0x7f2c77c0b2fc in WebCore::SVGTextMetrics::measureCharacterRange(WebCore::RenderSVGInlineText*, unsigned int, unsigned int) 
    #9 0x7f2c77bf9e4a in WebCore::SVGTextLayoutAttributesBuilder::propagateLayoutAttributes(WebCore::RenderObject*, WTF::Vector<WebCore::SVGTextLayoutAttributes, 0ul>&, unsigned int&, unsigned short&) const 
    #10 0x7f2c77bfb2d2 in WebCore::SVGTextLayoutAttributesBuilder::propagateLayoutAttributes(WebCore::RenderObject*, WTF::Vector<WebCore::SVGTextLayoutAttributes, 0ul>&, unsigned int&, unsigned short&) const 
    #11 0x7f2c77bf850b in WebCore::SVGTextLayoutAttributesBuilder::buildLayoutAttributesForTextSubtree(WebCore::RenderSVGText*) 
    #12 0x7f2c77bc446b in WebCore::RenderSVGText::layout() 
    #13 0x7f2c77bd20f5 in WebCore::SVGRenderSupport::layoutChildren(WebCore::RenderObject*, bool) 
    #14 0x7f2c77edf12a in WebCore::RenderSVGRoot::layout() 
    #15 0x7f2c771e908a in WebCore::RenderBlock::layoutInlineChildren(bool, int&, int&) 
    #16 0x7f2c7715fe21 in WebCore::RenderBlock::layoutBlock(bool, int, WebCore::RenderBlock::BlockLayoutPass) 
    #17 0x7f2c7715eab9 in WebCore::RenderBlock::layout() 
    #18 0x7f2c77179e9a in WebCore::RenderBlock::layoutBlockChild(WebCore::RenderBox*, WebCore::RenderBlock::MarginInfo&, int&, int&) 
    #19 0x7f2c77167c64 in WebCore::RenderBlock::layoutBlockChildren(bool, int&) 
    #20 0x7f2c7715fe45 in WebCore::RenderBlock::layoutBlock(bool, int, WebCore::RenderBlock::BlockLayoutPass) 
    #21 0x7f2c7715eab9 in WebCore::RenderBlock::layout() 
    #22 0x7f2c77179e9a in WebCore::RenderBlock::layoutBlockChild(WebCore::RenderBox*, WebCore::RenderBlock::MarginInfo&, int&, int&) 
Thread T12 created by T0 here:
    #1 0x7f2c743c0937 in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThread::Delegate*, unsigned long*) base/threading/platform_thread_posix.cc:0
    #2 0x7f2c743c083a in base::PlatformThread::Create(unsigned long, base::PlatformThread::Delegate*, unsigned long*) 
    #3 0x7f2c743c1613 in base::Thread::StartWithOptions(base::Thread::Options const&) 
    #4 0x7f2c7861d2ea in BrowserRenderProcessHost::Init(bool) 
    #5 0x7f2c786952fb in RenderViewHost::CreateRenderView(std::basic_string<unsigned short, base::string16_char_traits, std::allocator<unsigned short> > const&) 
    #6 0x7f2c78757cf7 in TabContents::CreateRenderViewForRenderManager(RenderViewHost*) 
    #7 0x7f2c7875812d in non-virtual thunk to TabContents::CreateRenderViewForRenderManager(RenderViewHost*) 
==3032== ABORTING
Shadow byte and word:
  0x00001fe58cd77d1d: fd
  0x00001fe58cd77d18: fd fd fd fd fd fd fd fd
More shadow bytes:
  0x00001fe58cd77cf8: fa fa fa fa fa fa fa fa
  0x00001fe58cd77d00: fa fa fa fa fa fa fa fa
  0x00001fe58cd77d08: fa fa fa fa fa fa fa fa
  0x00001fe58cd77d10: fd fd fd fd fd fd fd fd
=>0x00001fe58cd77d18: fd fd fd fd fd fd fd fd
  0x00001fe58cd77d20: fd fd fd fd fd fd fd fd
  0x00001fe58cd77d28: fd fd fd fd fd fd fd fd
  0x00001fe58cd77d30: fd fd fd fd fd fd fd fd
  0x00001fe58cd77d38: fd fd fd fd fd fd fd fd

### in...@chromium.org (2011-09-06)

This bug should handle c#0 and c#15 testcases.

### in...@chromium.org (2011-09-06)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-09-06)

[Empty comment from Monorail migration]

### ma...@google.com (2011-09-08)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-09-14)

Upstreamed https://bugs.webkit.org/show_bug.cgi?id=68060

### in...@chromium.org (2011-09-16)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-09-16)

http://trac.webkit.org/changeset/95301

### in...@chromium.org (2011-09-17)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-09-17)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-09-19)

merged to m15 in r95427

### in...@chromium.org (2011-09-23)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-09-26)

[Empty comment from Monorail migration]

### [Deleted User] (2011-09-26)

merged to m14 as r96027.

### sc...@gmail.com (2011-10-01)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-10-03)

@miaubiz: nice find, a slightly different variation on the "stale font" bug. $1000.

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

### js...@chromium.org (2011-10-05)

Batch update.

### in...@chromium.org (2011-10-06)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-10-07)

Payment in system.

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

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/95072?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/96958, crbug.com/chromium/99232]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094538)*
