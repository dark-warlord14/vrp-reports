# Heap-buffer-overflow in SkAlphaRuns::add

| Field | Value |
|-------|-------|
| **Issue ID** | [40063405](https://issues.chromium.org/issues/40063405) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals, Internals>Skia |
| **Reporter** | at...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2012-08-11 |
| **Bounty** | $500.00 |

## Description

All files needed for reproducing are as attachments.

This issue can be hard to reproduce, I created the runner.html to help in reproducing. Place all the attached files in a same folder and open the runner.html with Chrome. I had a success rate of about one of ten tries to reproduce the issue. (If you can't reproduce using the runner.html you can try to adjust the iframe onload timeout and the number of file1 opens before file2 is opened.)

The issue can also reproduce as heap-buffer-overflow READ of size 2.

ASAN-report:
==17173== ERROR: AddressSanitizer heap-use-after-free on address 0x7fd122a5c1c6 at pc 0x7fd13c769b18 bp 0x7fff116f5020 sp 0x7fff116f5018
READ of size 2 at 0x7fd122a5c1c6 thread T0
    #0 0x7fd13c769b17 in SkAlphaRuns::add(int, unsigned int, int, unsigned int, unsigned int, int) ???:0
    #1 0x7fd13c6427d4 in SuperBlitter::blitH(int, int, int) ???:0
    #2 0x7fd13c64e9c5 in sk_fill_path(SkPath const&, SkIRect const*, SkBlitter*, int, int, int, SkRegion const&) ???:0
    #3 0x7fd13c644a90 in SkScan::AntiFillPath(SkPath const&, SkRegion const&, SkBlitter*, bool) ???:0
    #4 0x7fd13c645287 in SkScan::AntiFillPath(SkPath const&, SkRasterClip const&, SkBlitter*) ???:0
    #5 0x7fd13c5d1a2c in SkDraw::drawPath(SkPath const&, SkPaint const&, SkMatrix const*, bool) const ???:0
.
.
.

## Attachments

- [runner.html](attachments/runner.html) (text/html; charset=us-ascii, 547 B)
- [chrome-heap-buffer-overflow-SkAlphaRunsadd-c5610.html](attachments/chrome-heap-buffer-overflow-SkAlphaRunsadd-c5610.html) (text/html; charset=utf-8, 22.4 KB)
- [chrome-heap-buffer-overflow-SkAlphaRunsadd-c569.html](attachments/chrome-heap-buffer-overflow-SkAlphaRunsadd-c569.html) (text/html; charset=utf-8, 25.0 KB)
- [chrome-heap-buffer-overflow-SkAlphaRunsadd-c569.html](attachments/chrome-heap-buffer-overflow-SkAlphaRunsadd-c569_53180796.html) (text/html; charset=utf-8, 13.1 KB)
- [chrome-heap-buffer-overflow-SkAlphaRunsadd-c5610.html](attachments/chrome-heap-buffer-overflow-SkAlphaRunsadd-c5610_53180797.html) (text/html; charset=us-ascii, 1.5 KB)
- [chrome-heap-buffer-overflow-SkAlphaRunsadd-c5610.html](attachments/chrome-heap-buffer-overflow-SkAlphaRunsadd-c5610_53180804.html) (text/html; charset=us-ascii, 1.5 KB)
- [repro.zip](attachments/repro.zip) (application/zip; charset=binary, 6.7 KB)
- [Repro-8-from-10.zip](attachments/Repro-8-from-10.zip) (application/zip; charset=binary, 6.5 KB)
- [Repro-10-from-10.zip](attachments/Repro-10-from-10.zip) (application/zip; charset=binary, 1.6 KB)

## Timeline

### [Deleted User] (2012-08-13)

https://cluster-fuzz.appspot.com/testcase?key=93515723

### in...@chromium.org (2012-08-13)

[Empty comment from Monorail migration]

### [Deleted User] (2012-08-13)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-08-14)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=93515723

Uploader: cdn@chromium.org

Crash Type: Heap-use-after-free READ 2
Crash Address: 0x7f08a25df39c
Crash State:
  - crash stack -
  SkAlphaRuns::add
  SuperBlitter::blitH
  - free stack -
  IA__g_realloc
  IA__g_realloc
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=137791:137812

Minimized Testcase (12.27 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95DigASG6XJWJp9QHDB4tWbhYYANBspZcnAammmok4i1kMFeJv4Gy4kjneEexbPpuYqz7VyGycjVftROQCJn0dtRyMt7Nt1X7LBPTFLnK8GTCXeSuoEDWYKlGDKSf0vNRtHLuhW7jJbv7b4xZMuArdyEbBUHD-fpQwSUPQXhr_N7lTRQAk

### in...@chromium.org (2012-08-14)

This just looks like a read.

### cl...@chromium.org (2012-08-16)

ClusterFuzz has detected this issue as fixed in range 151665:151672.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=93515723

Uploader: cdn@chromium.org

Crash Type: Heap-use-after-free READ 2
Crash Address: 0x7f08a25df39c
Crash State:
  - crash stack -
  SkAlphaRuns::add
  SuperBlitter::blitH
  - free stack -
  IA__g_realloc
  IA__g_realloc
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=137791:137812
Fixed: https://cluster-fuzz.appspot.com/revisions?range=151665:151672

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv95DigASG6XJWJp9QHDB4tWbhYYANBspZcnAammmok4i1kMFeJv4Gy4kjneEexbPpuYqz7VyGycjVftROQCJn0dtRyMt7Nt1X7LBPTFLnK8GTCXeSuoEDWYKlGDKSf0vNRtHLuhW7jJbv7b4xZMuArdyEbBUHD-fpQwSUPQXhr_N7lTRQAk

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### in...@chromium.org (2012-08-16)

ignore the last CF fixed message, since the test was flaky.

This looks like the last medium severity bug open for Skia. Elliot, can you please help us here.

### to...@chromium.org (2012-08-16)

Elliot is WebKit gardener through Tuesday, so likely won't get to look at it before midweek.

Interestingly, the minimized testcase seems to hang forever on my Linux desktop with ToT.

### in...@chromium.org (2012-08-20)

[Empty comment from Monorail migration]

### ep...@google.com (2012-08-22)

https://cluster-fuzz.appspot.com/testcase?key=93515723 says that this affects Beta (21.0.1180.79), so I downloaded asan-linux-beta-21.0.1180.79 from https://commondatastorage.googleapis.com/chromium-browser-asan/index.html and launched it on my Linux desktop (running via NX).

I downloaded the minimized test case from clusterfuzz (attached here), unzipped it, and opened run.html.  I did not get any ASAN errors, but the browser seems to hang forever (as Tom reported on Aug 16).  Eventually, if I click on the browser window, I get a "Page(s) Unresponsive" dialog.

I tried it 5 times and got the same result every time.

I will look into this some more tomorrow... but it looks like this is gonna be difficult to reproduce.

### in...@chromium.org (2012-08-23)

So, i tried this locally and also retried on ClusterFuzz. it is extremely flaky repro that is causing not to reproduce locally at all and once-twice on CF.

Attekett, can you please try to provide a more reliable repro. This will increase the chances of a higher reward.

### cl...@chromium.org (2012-08-23)

ClusterFuzz has detected this issue as fixed in range 151255:151257.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=93515723

Uploader: cdn@chromium.org

Crash Type: Heap-use-after-free READ 2
Crash Address: 0x7f08a25df39c
Crash State:
  - crash stack -
  SkAlphaRuns::add
  SuperBlitter::blitH
  - free stack -
  IA__g_realloc
  IA__g_realloc
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=137791:137812
Fixed: https://cluster-fuzz.appspot.com/revisions?range=151255:151257

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv95DigASG6XJWJp9QHDB4tWbhYYANBspZcnAammmok4i1kMFeJv4Gy4kjneEexbPpuYqz7VyGycjVftROQCJn0dtRyMt7Nt1X7LBPTFLnK8GTCXeSuoEDWYKlGDKSf0vNRtHLuhW7jJbv7b4xZMuArdyEbBUHD-fpQwSUPQXhr_N7lTRQAk

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### in...@chromium.org (2012-08-23)

ignore the CF fixed range, this is because repro was flaky.

Attekett, can you please also check if it still reproduces for you. Something might have magically fixed it, although i doubt it :) 

### at...@gmail.com (2012-08-23)

I can still reproduce this. Took about 10 tries on my laptop. I'll try to minimize the files and then combine them into one file. That could make it easier to reproduce.


### at...@gmail.com (2012-08-23)

I reduced the second file but I failed to make it more stable. 

I found one interesting line.
ctx.arcTo( 83,730 , 107,252 ,-0.2222905217204243e-2045)

Removing it or changing the e-2045 part into something with higher value than -45 will stop the hanging but also seems to stop the crashing.

I'm not sure that all the lines in the reduced repro-file are needed because in some situations I didn't get a crash in a 50 or so re-runs. :(

### at...@gmail.com (2012-08-23)

Inferno: Try with this new file. No need to test with the old one. 

### at...@gmail.com (2012-08-23)

Here are all the needed files enclosed into a single zip-file.

### in...@chromium.org (2012-08-23)

Elliot - Attekett's repro in c#17 reproduces reliably for me locally, i can reproduce a crash in less than 30 sec. ClusterFuzz report coming in https://cluster-fuzz.appspot.com/testcase?key=98309443

### ep...@google.com (2012-08-29)

OK, I can finally reproduce this reliably on my Linux desktop machine (running remotely via NX).

I downloaded asan-linux-release-152058 from https://commondatastorage.googleapis.com/chromium-browser-asan/index.html
when I view the repro case from https://crbug.com/chromium/142169#c17, I get this ASAN error:


=================================================================
==9282== ERROR: AddressSanitizer heap-buffer-overflow on address 0x7f80f92aed28 at pc 0x7f8108e960e6 bp 0x7fffb8b60400 sp 0x7fffb8b603f8
READ of size 2 at 0x7f80f92aed28 thread T0
    #0 0x7f8108e960e5 in SkAlphaRuns::add(int, unsigned int, int, unsigned int, unsigned int, int) ???:0
    #1 0x7f8108e25b14 in SuperBlitter::blitH(int, int, int) ???:0
    #2 0x7f8108e31d05 in sk_fill_path(SkPath const&, SkIRect const*, SkBlitter*, int, int, int, SkRegion const&) ???:0
    #3 0x7f8108e27dd0 in SkScan::AntiFillPath(SkPath const&, SkRegion const&, SkBlitter*, bool) ???:0
    #4 0x7f8108e285c7 in SkScan::AntiFillPath(SkPath const&, SkRasterClip const&, SkBlitter*) ???:0
    #5 0x7f8108dae0dc in SkDraw::drawPath(SkPath const&, SkPaint const&, SkMatrix const*, bool) const ???:0
    #6 0x7f8108d94926 in SkCanvas::drawPath(SkPath const&, SkPaint const&) ???:0
    #7 0x7f8109df12ed in WebCore::GraphicsContext::fillPath(WebCore::Path const&) ???:0
    #8 0x7f8109a9d232 in WebCore::CanvasRenderingContext2D::fill() ???:0
    #9 0x7f810b891760 in WebCore::CanvasRenderingContext2DV8Internal::fillCallback(v8::Arguments const&) out/Release/obj/gen/webkit/bindings/V8DerivedSources17.cpp:0
    #10 0x7f8107f95d55 in v8::internal::Builtin_HandleApiCall(v8::internal::(anonymous namespace)::BuiltinArguments<(v8::internal::BuiltinExtraArguments)1>, v8::internal::Isolate*) v8/src/builtins.cc:0
    #11 0x2faf43f0618d in  
    #12 0x2faf43f717ef in  
    #13 0x2faf43f240e6 in  
    #14 0x2faf43f11416 in  
    #15 0x7f8108012012 in v8::internal::Invoke(bool, v8::internal::Handle<v8::internal::JSFunction>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*, bool*) v8/src/execution.cc:0
    #16 0x7f8107f2857a in v8::Script::Run() ???:0
    #17 0x7f810a0364b3 in WebCore::V8Proxy::runScript(v8::Handle<v8::Script>) ???:0
    #18 0x7f810a035ef2 in WebCore::V8Proxy::evaluate(WebCore::ScriptSourceCode const&, WebCore::Node*) ???:0
    #19 0x7f8109fd4eda in WebCore::ScriptController::evaluate(WebCore::ScriptSourceCode const&) ???:0
    #20 0x7f81094651b9 in WebCore::ScriptElement::executeScript(WebCore::ScriptSourceCode const&) ???:0
    #21 0x7f8109460861 in WebCore::ScriptElement::prepareScript(WTF::TextPosition const&, WebCore::ScriptElement::LegacyTypeSupport) ???:0
    #22 0x7f8109b0c6b2 in WebCore::HTMLScriptRunner::runScript(WebCore::Element*, WTF::TextPosition const&) ???:0
    #23 0x7f8109b0c3cf in WebCore::HTMLScriptRunner::execute(WTF::PassRefPtr<WebCore::Element>, WTF::TextPosition const&) ???:0
    #24 0x7f8109b0132a in WebCore::HTMLDocumentParser::runScriptsForPausedTreeBuilder() ???:0
    #25 0x7f8109b015c1 in WebCore::HTMLDocumentParser::canTakeNextToken(WebCore::HTMLDocumentParser::SynchronousMode, WebCore::PumpSession&) ???:0
    #26 0x7f8109b009ad in WebCore::HTMLDocumentParser::pumpTokenizer(WebCore::HTMLDocumentParser::SynchronousMode) ???:0
    #27 0x7f8109b02614 in WebCore::HTMLDocumentParser::append(WebCore::SegmentedString const&) ???:0
    #28 0x7f810dfe9a1a in WebCore::DecodedDataDocumentParser::appendBytes(WebCore::DocumentWriter*, char const*, unsigned long) ???:0
    #29 0x7f810a5c1fc0 in WebCore::DocumentLoader::commitData(char const*, unsigned long) ???:0
    #30 0x7f8109216a69 in WebKit::FrameLoaderClientImpl::committedLoad(WebCore::DocumentLoader*, char const*, int) ???:0
    #31 0x7f810a5c227d in WebCore::DocumentLoader::commitLoad(char const*, int) ???:0
    #32 0x7f810a65f282 in WebCore::ResourceLoader::didReceiveData(char const*, int, long long, bool) ???:0
    #33 0x7f810a63addb in WebCore::MainResourceLoader::didReceiveData(char const*, int, long long, bool) ???:0
    #34 0x7f810a6608ad in WebCore::ResourceLoader::didReceiveData(WebCore::ResourceHandle*, char const*, int, int) ???:0
    #35 0x7f8108b80047 in content::ResourceDispatcher::OnReceivedData(IPC::Message const&, int, base::FileDescriptor, int, int) ???:0
    #36 0x7f8108b7e310 in content::ResourceDispatcher::DispatchMessage(IPC::Message const&) ???:0
    #37 0x7f8108b7c629 in content::ResourceDispatcher::OnMessageReceived(IPC::Message const&) ???:0
    #38 0x7f8108a674ea in ChildThread::OnMessageReceived(IPC::Message const&) ???:0
    #39 0x7f81075adb60 in IPC::ChannelProxy::Context::OnDispatchMessage(IPC::Message const&) ???:0
    #40 0x7f810745e9fc in MessageLoop::RunTask(base::PendingTask const&) ???:0
    #41 0x7f810745ef9f in MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) ???:0
    #42 0x7f810745fdaa in MessageLoop::DoWork() ???:0
    #43 0x7f810746a7b6 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ???:0
    #44 0x7f810745d745 in MessageLoop::RunInternal() ???:0
    #45 0x7f81074a3c81 in base::RunLoop::Run() ???:0
    #46 0x7f810745bb76 in MessageLoop::Run() ???:0
    #47 0x7f810d440b6e in RendererMain(content::MainFunctionParams const&) ???:0
    #48 0x7f810730300a in content::RunZygote(content::MainFunctionParams const&, content::ContentMainDelegate*) ???:0
    #49 0x7f81073044f6 in content::RunNamedProcessTypeMain(std::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, content::MainFunctionParams const&, content::ContentMainDelegate*) ???:0
    #50 0x7f8107305bf3 in content::ContentMainRunnerImpl::Run() ???:0
    #51 0x7f81073026e4 in content::ContentMain(int, char const**, content::ContentMainDelegate*) ???:0
    #52 0x7f8105be06e6 in ChromeMain ??:0
    #53 0x7f8105be064a in main ???:0
    #54 0x7f80ff0d1c4d in __libc_start_main /build/buildd/eglibc-2.11.1/csu/libc-start.c:258
0x7f80f92aed28 is located 168 bytes to the right of 1024-byte region [0x7f80f92ae880,0x7f80f92aec80)
freed by thread T0 here:
    #0 0x7f810e9e8710 in __interceptor_free ??:0
    #1 0x7f8109121b87 in WebCore::ResourceRequestBase::~ResourceRequestBase() ???:0
    #2 0x7f8109188ef6 in WebCore::FrameLoadRequest::~FrameLoadRequest() ???:0
    #3 0x7f810a5ec93b in WebCore::FrameLoader::changeLocation(WebCore::SecurityOrigin*, WebCore::KURL const&, WTF::String const&, bool, bool, bool) ???:0
    #4 0x7f810a64354c in WebCore::ScheduledURLNavigation::fire(WebCore::Frame*) ???:0
    #5 0x7f810a63f8ce in WebCore::NavigationScheduler::timerFired(WebCore::Timer<WebCore::NavigationScheduler>*) ???:0
    #6 0x7f8109d0edd7 in WebCore::ThreadTimers::sharedTimerFiredInternal() ???:0
    #7 0x7f81074f2c45 in base::Timer::RunScheduledTask() ???:0
    #8 0x7f810745e9fc in MessageLoop::RunTask(base::PendingTask const&) ???:0
    #9 0x7f810745ef9f in MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) ???:0
    #10 0x7f810745fdaa in MessageLoop::DoWork() ???:0
    #11 0x7f810746a7b6 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ???:0
    #12 0x7f810745d745 in MessageLoop::RunInternal() ???:0
    #13 0x7f81074a3c81 in base::RunLoop::Run() ???:0
    #14 0x7f810745bb76 in MessageLoop::Run() ???:0
    #15 0x7f810d440b6e in RendererMain(content::MainFunctionParams const&) ???:0
    #16 0x7f810730300a in content::RunZygote(content::MainFunctionParams const&, content::ContentMainDelegate*) ???:0
    #17 0x7f81073044f6 in content::RunNamedProcessTypeMain(std::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, content::MainFunctionParams const&, content::ContentMainDelegate*) ???:0
    #18 0x7f8107305bf3 in content::ContentMainRunnerImpl::Run() ???:0
    #19 0x7f81073026e4 in content::ContentMain(int, char const**, content::ContentMainDelegate*) ???:0
    #20 0x7f8105be06e6 in ChromeMain ??:0
    #21 0x7f8105be064a in main ???:0
    #22 0x7f80ff0d1c4d in __libc_start_main /build/buildd/eglibc-2.11.1/csu/libc-start.c:258
previously allocated by thread T0 here:
    #0 0x7f810e9e87d0 in __interceptor_malloc ??:0
    #1 0x7f810946b2ae in WTF::fastZeroedMalloc(unsigned long) ???:0
    #2 0x7f8109120bf4 in WTF::HashTable<WTF::AtomicString, WTF::KeyValuePair<WTF::AtomicString, WTF::String>, WTF::KeyValuePairKeyExtractor<WTF::KeyValuePair<WTF::AtomicString, WTF::String> >, WTF::CaseFoldingHash, WTF::HashMapValueTraits<WTF::HashTraits<WTF::AtomicString>, WTF::HashTraits<WTF::String> >, WTF::HashTraits<WTF::AtomicString> >::rehash(int) ???:0
    #3 0x7f810912275f in WTF::HashTableAddResult<WTF::HashTableIterator<WTF::AtomicString, WTF::KeyValuePair<WTF::AtomicString, WTF::String>, WTF::KeyValuePairKeyExtractor<WTF::KeyValuePair<WTF::AtomicString, WTF::String> >, WTF::CaseFoldingHash, WTF::HashMapValueTraits<WTF::HashTraits<WTF::AtomicString>, WTF::HashTraits<WTF::String> >, WTF::HashTraits<WTF::AtomicString> > > WTF::HashTable<WTF::AtomicString, WTF::KeyValuePair<WTF::AtomicString, WTF::String>, WTF::KeyValuePairKeyExtractor<WTF::KeyValuePair<WTF::AtomicString, WTF::String> >, WTF::CaseFoldingHash, WTF::HashMapValueTraits<WTF::HashTraits<WTF::AtomicString>, WTF::HashTraits<WTF::String> >, WTF::HashTraits<WTF::AtomicString> >::add<WTF::IdentityHashTranslator<WTF::CaseFoldingHash>, WTF::AtomicString, WTF::KeyValuePair<WTF::AtomicString, WTF::String> >(WTF::AtomicString const&, WTF::KeyValuePair<WTF::AtomicString, WTF::String> const&) ???:0
    #4 0x7f8109122150 in WebCore::ResourceRequestBase::ResourceRequestBase(WebCore::ResourceRequestBase const&) ???:0
    #5 0x7f810a5ec53b in WebCore::FrameLoader::changeLocation(WebCore::SecurityOrigin*, WebCore::KURL const&, WTF::String const&, bool, bool, bool) ???:0
    #6 0x7f810a64354c in WebCore::ScheduledURLNavigation::fire(WebCore::Frame*) ???:0
    #7 0x7f810a63f8ce in WebCore::NavigationScheduler::timerFired(WebCore::Timer<WebCore::NavigationScheduler>*) ???:0
    #8 0x7f8109d0edd7 in WebCore::ThreadTimers::sharedTimerFiredInternal() ???:0
    #9 0x7f81074f2c45 in base::Timer::RunScheduledTask() ???:0
    #10 0x7f810745e9fc in MessageLoop::RunTask(base::PendingTask const&) ???:0
    #11 0x7f810745ef9f in MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) ???:0
    #12 0x7f810745fdaa in MessageLoop::DoWork() ???:0
    #13 0x7f810746a7b6 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ???:0
    #14 0x7f810745d745 in MessageLoop::RunInternal() ???:0
    #15 0x7f81074a3c81 in base::RunLoop::Run() ???:0
    #16 0x7f810745bb76 in MessageLoop::Run() ???:0
    #17 0x7f810d440b6e in RendererMain(content::MainFunctionParams const&) ???:0
    #18 0x7f810730300a in content::RunZygote(content::MainFunctionParams const&, content::ContentMainDelegate*) ???:0
    #19 0x7f81073044f6 in content::RunNamedProcessTypeMain(std::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, content::MainFunctionParams const&, content::ContentMainDelegate*) ???:0
    #20 0x7f8107305bf3 in content::ContentMainRunnerImpl::Run() ???:0
    #21 0x7f81073026e4 in content::ContentMain(int, char const**, content::ContentMainDelegate*) ???:0
    #22 0x7f8105be06e6 in ChromeMain ??:0
    #23 0x7f8105be064a in main ???:0
    #24 0x7f80ff0d1c4d in __libc_start_main /build/buildd/eglibc-2.11.1/csu/libc-start.c:258
==9282== ABORTING
Stats: 235M malloced (126M for red zones) by 137533 calls
Stats: 2M realloced by 3129 calls
Stats: 230M freed by 119671 calls
Stats: 59M really freed by 56784 calls
Stats: 332M (85063 full pages) mmaped in 83 calls
  mmaps   by size class: 8:98298; 9:16382; 10:12285; 11:2047; 12:1024; 13:2048; 14:768; 15:512; 16:128; 17:64; 18:80; 19:8; 21:2; 22:48;
  mallocs by size class: 8:102652; 9:13265; 10:14633; 11:1912; 12:1134; 13:2415; 14:746; 15:487; 16:91; 17:46; 18:89; 19:6; 21:1; 22:56;
  frees   by size class: 8:86333; 9:12402; 10:14380; 11:1669; 12:1045; 13:2374; 14:727; 15:473; 16:85; 17:34; 18:87; 19:6; 22:56;
  rfrees  by size class: 8:42310; 9:6176; 10:5350; 11:781; 12:486; 13:1053; 14:361; 15:157; 16:55; 17:22; 18:16; 19:6; 22:11;
Stats: malloc large: 198 small slow: 855
Shadow byte and word:
  0x1ff01f255da5: fa
  0x1ff01f255da0: fa fa fa fa fa fa fa fa
More shadow bytes:
  0x1ff01f255d80: fd fd fd fd fd fd fd fd
  0x1ff01f255d88: fd fd fd fd fd fd fd fd
  0x1ff01f255d90: fa fa fa fa fa fa fa fa
  0x1ff01f255d98: fa fa fa fa fa fa fa fa
=>0x1ff01f255da0: fa fa fa fa fa fa fa fa
  0x1ff01f255da8: fa fa fa fa fa fa fa fa
  0x1ff01f255db0: fa fa fa fa fa fa fa fa
  0x1ff01f255db8: fa fa fa fa fa fa fa fa
  0x1ff01f255dc0: fa fa fa fa fa fa fa fa


### ep...@google.com (2012-08-29)

The reproducible case (from https://crbug.com/chromium/142169#c17) affects trunk but not M21 or M22, at least on my Linux desktop.

But https://cluster-fuzz.appspot.com/testcase?key=93515723 says that it affects Beta (21.0.1180.79).  Maybe the repro case in https://crbug.com/chromium/142169#c17 is not exercising exactly the same problem?

Is anyone able to reproduce this in M21 or M22?

I downloaded the following precompiled binaries from https://commondatastorage.googleapis.com/chromium-browser-asan/index.html

asan-linux-beta-21.0.1180.79
reports 21.0.1180.79 (Developer Build 151411)
does NOT exhibit the ASAN error

asan-linux-beta-22.0.1229.14
reports 22.0.1229.14 (Developer Build 152690)
does NOT exhibit the ASAN error

asan-linux-release-152058
reports 23.0.1238.0 (Developer Build 152058)
DOES exhibit the ASAN error



### in...@chromium.org (2012-08-29)

https://cluster-fuzz.appspot.com/testcase?key=93515723 i was not able to reproduce locally because of flakiness.if the m21 bug turns out to be different, attekett will file a new bug, since it will hit easily in his fuzzing.

### ep...@google.com (2012-08-29)

So, should we remove the Mstone-21 label and handle M21 bugs before this one?

### in...@chromium.org (2012-08-29)

So, i dont think there should another m21 patch, and pwnium is targeted for m22, so both m21 and m22 buckets are same in terms of importance.

### in...@chromium.org (2012-09-05)

Skia guys, any updates on these. These high severity bugs we would definitely like to get knocked out before pwnium 2, your help is highly appreciated.

### in...@chromium.org (2012-10-14)

Mass move from m21 to m22.

### in...@chromium.org (2012-10-14)

friendly ping!

### in...@chromium.org (2012-10-22)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-11-12)

Attekett, is this still reproducing for you ?

### at...@gmail.com (2012-11-12)

Repro-file from https://crbug.com/chromium/142169#c17 still reproduces on my laptop. I don't remember how flaky that repro-file was, but now it caused crash twice in ten tries. The ASAN-report looks little different now.

Tested with:
Chromium 25.0.1324.0 (Developer Build 167149)
Ubuntu 12.04 x86_64

ASAN-report:

==3428== ERROR: AddressSanitizer: heap-use-after-free on address 0x7ffc1acee556 at pc 0x7ffc3286f0d0 bp 0x7fff2ae65870 sp 0x7fff2ae65868
READ of size 2 at 0x7ffc1acee556 thread T0
    #0 0x7ffc3286f0cf in SkRectClipBlitter::blitAntiH(int, int, unsigned char const*, short const*) ???:0
    #1 0x7ffc32786fed in SuperBlitter::blitH(int, int, int) ???:0
    #2 0x7ffc32794190 in sk_fill_path(SkPath const&, SkIRect const*, SkBlitter*, int, int, int, SkRegion const&) ???:0
    #3 0x7ffc32789445 in SkScan::AntiFillPath(SkPath const&, SkRegion const&, SkBlitter*, bool) ???:0
    #4 0x7ffc32789c43 in SkScan::AntiFillPath(SkPath const&, SkRasterClip const&, SkBlitter*) ???:0
    #5 0x7ffc32700c89 in SkDraw::drawPath(SkPath const&, SkPaint const&, SkMatrix const*, bool) const ???:0
    #6 0x7ffc326e741b in SkCanvas::drawPath(SkPath const&, SkPaint const&) ???:0
    #7 0x7ffc32cebab5 in WebCore::GraphicsContext::fillPath(WebCore::Path const&) ???:0
    #8 0x7ffc34b1f3d4 in WebCore::CanvasRenderingContext2D::fill() ???:0
    #9 0x7ffc31cc643b in WebCore::CanvasRenderingContext2DV8Internal::fillCallback(v8::Arguments const&) gen/webkit/bindings/V8DerivedSources17.cpp:0
    #10 0x7ffc32f4f9ef in v8::internal::Builtin_HandleApiCall(v8::internal::(anonymous namespace)::BuiltinArguments<(v8::internal::BuiltinExtraArguments)1>, v8::internal::Isolate*) ../../v8/src/builtins.cc:0
.
.
.



### at...@gmail.com (2012-11-12)

ASAN-free stack:
freed by thread T0 here:
    #0 0x7ffc35ee9650 in __interceptor_free ??:0
    #1 0x7ffc30614281 in WebCore::RuleSet::shrinkToFit() ???:0
    #2 0x7ffc2fd5676e in WebCore::makeRuleSet(WTF::Vector<WebCore::RuleFeature, 0ul> const&) ../../third_party/WebKit/Source/WebCore/css/StyleResolver.cpp:0
    #3 0x7ffc2fd563ce in WebCore::StyleResolver::collectFeatures() ???:0
    #4 0x7ffc2fd55f75 in WebCore::StyleResolver::appendAuthorStyleSheets(unsigned int, WTF::Vector<WTF::RefPtr<WebCore::CSSStyleSheet>, 0ul> const&) ???:0
    #5 0x7ffc2fd4fe29 in WebCore::StyleResolver::StyleResolver(WebCore::Document*, bool) ???:0
    #6 0x7ffc30bf9733 in WebCore::Document::createStyleResolver() ???:0
    #7 0x7ffc30c74633 in WebCore::Element::styleForRenderer() ???:0
    #8 0x7ffc30cf22c4 in WebCore::NodeRendererFactory::createRendererIfNeeded() ???:0
    #9 0x7ffc30cc9a5c in WebCore::Node::createRendererIfNeeded() ???:0
    #10 0x7ffc30c73277 in WebCore::Element::attach() ???:0
    #11 0x7ffc2e8e7589 in WebCore::executeTask(WebCore::HTMLConstructionSiteTask&) ../../third_party/WebKit/Source/WebCore/html/parser/HTMLConstructionSite.cpp:0
.
.
.

Sorry forget to paste the free stack.

### at...@gmail.com (2012-11-12)

I got the success-rate pretty high on my laptop. Not 100% sure still. I'll try more later, but not sure if I can create more reliable version.

New repro-files as attachment.

### at...@gmail.com (2012-11-12)

Here is the best I can manually do. This repro looked like 100% sure. I also minimized the second-file needed to reproduce.

### in...@chromium.org (2012-11-12)

Thanks a lot Attekett. This new repro is coming out as fully reproducible on ClusterFuzz. Report coming.

Mike, Elliot, can you please take a look. This is a really old bug now :(

### in...@chromium.org (2012-11-26)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=139373635

Uploader: aarya@google.com

Crash Type: Heap-buffer-overflow READ 2
Crash Address: 0x7f1266ece8f0
Crash State:
  - crash stack -
  SkAlphaRuns::add
  SuperBlitter::blitH
  sk_fill_path
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=162815:162921

Minimized Testcase (1.22 Kb): https://cluster-fuzz.appspot.com/download/AMIfv97jDJIYYqHbvYI8kXIT04275liALLpmeZ3v-e1kdY06pm6skOFQGH0lcuVEt3Er2BGtdyO7Swohh98t8NgfvzomivZ3nFBbNNJcPPUJVnSKQwmMhqRmEcl0sfs5EJQAUYgvJxPaCYX7yt86uIpyB4Vdn6kBbj_HJEHfrF5wMI_ypHE7Ids

### in...@chromium.org (2012-11-29)

Moving all milestone 22 bugs to milestone 23

### in...@chromium.org (2012-12-05)

Mike, Elliot, friendly ping!

### [Deleted User] (2012-12-05)

I am traveling this week, and won't be able to sit down to try to repro, but I will work on this when I'm back in the office.

### in...@chromium.org (2013-01-02)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=154022740

Fuzzer: Inferno_canvas_wrecker

Crash Type: Heap-buffer-overflow READ 2
Crash Address: 0x7f879c6d21d8
Crash State:
  - crash stack -
  SkAlphaRuns::add
  SuperBlitter::blitH
  - free stack -
  SkPathRef::~SkPathRef
  SkScalerContext::getImage
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=162815:162921

Minimized Testcase (3006.14 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94gBkDmYruiZ57cMwIB0V3xdqxd8PwwntWypzezajyMZrgi06YdRB42mnFGGnypTUd0KcIjRucKViuRoh-7km0Vs2fJ4DQXmwpi5ZqlE3zW692kc1NyBvQOV8FvqYNAx1NHUNFvs44YWO2rtapp4fuAN6ua3Q

### in...@chromium.org (2013-01-02)

friendly ping Mike, this bug is getting very old and needs some love. Also found both internally and externally.

### in...@chromium.org (2013-01-09)

Please note that this is 2nd last bug skia security bug and also discovered externally. We would like to have the fix in m24 first patch, can you please help to take a look.

### in...@chromium.org (2013-01-10)

[Empty comment from Monorail migration]

### [Deleted User] (2013-01-10)

note to self: this path triggers an assert in the edgelist code. It appears that even after we chop it to fit in the clip (0, 0, 640, 480) I still generate a cubic with negative Y values (I think).

    path.quadTo(577330, 1971.72f, 577341, 1972.11f);
    path.cubicTo(10.7082f, -116.596f, 262.057f, 45.6468f, 294.694f, 1.96237f);


### [Deleted User] (2013-01-15)

Speculative fix in skia rev. 7184
Should land in chrome tomorrow (w/ DEPS roll)

### in...@chromium.org (2013-01-15)

We should know by tmrw from ClusterFuzz whether this is fixed or not after the roll. We can reopen if the fix didn't work.

### cl...@chromium.org (2013-01-16)

ClusterFuzz has detected this issue as fixed in range 177136:177151.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=154022740

Fuzzer: Inferno_canvas_wrecker

Crash Type: Heap-buffer-overflow READ 2
Crash Address: 0x7f879c6d21d8
Crash State:
  - crash stack -
  SkAlphaRuns::add
  SuperBlitter::blitH
  - free stack -
  SkPathRef::~SkPathRef
  SkScalerContext::getImage
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=162815:162921
Fixed: https://cluster-fuzz.appspot.com/revisions?range=177136:177151

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv94gBkDmYruiZ57cMwIB0V3xdqxd8PwwntWypzezajyMZrgi06YdRB42mnFGGnypTUd0KcIjRucKViuRoh-7km0Vs2fJ4DQXmwpi5ZqlE3zW692kc1NyBvQOV8FvqYNAx1NHUNFvs44YWO2rtapp4fuAN6ua3Q

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### cl...@chromium.org (2013-01-17)

ClusterFuzz has detected this issue as fixed in range 177136:177151.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=139373635

Uploader: aarya@google.com

Crash Type: Heap-buffer-overflow READ 2
Crash Address: 0x7f1266ece8f0
Crash State:
  - crash stack -
  SkAlphaRuns::add
  SuperBlitter::blitH
  sk_fill_path
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=162815:162921
Fixed: https://cluster-fuzz.appspot.com/revisions?range=177136:177151

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv97jDJIYYqHbvYI8kXIT04275liALLpmeZ3v-e1kdY06pm6skOFQGH0lcuVEt3Er2BGtdyO7Swohh98t8NgfvzomivZ3nFBbNNJcPPUJVnSKQwmMhqRmEcl0sfs5EJQAUYgvJxPaCYX7yt86uIpyB4Vdn6kBbj_HJEHfrF5wMI_ypHE7Ids

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### cl...@chromium.org (2013-01-17)

ClusterFuzz has detected this issue as fixed in range 177136:177151.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=139373635

Uploader: aarya@google.com

Crash Type: Heap-buffer-overflow READ 2
Crash Address: 0x7f1266ece8f0
Crash State:
  - crash stack -
  SkAlphaRuns::add
  SuperBlitter::blitH
  sk_fill_path
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=162815:162921
Fixed: https://cluster-fuzz.appspot.com/revisions?range=177136:177151

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv97jDJIYYqHbvYI8kXIT04275liALLpmeZ3v-e1kdY06pm6skOFQGH0lcuVEt3Er2BGtdyO7Swohh98t8NgfvzomivZ3nFBbNNJcPPUJVnSKQwmMhqRmEcl0sfs5EJQAUYgvJxPaCYX7yt86uIpyB4Vdn6kBbj_HJEHfrF5wMI_ypHE7Ids

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### in...@chromium.org (2013-01-17)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-01-24)

[Empty comment from Monorail migration]

### [Deleted User] (2013-01-29)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-01-29)

M25: Skia r7456

### sc...@gmail.com (2013-02-11)

Another OOB read!
$500 and our thanks :)

### sc...@gmail.com (2013-02-19)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-02-19)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-02-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### js...@chromium.org (2013-11-18)

Bulk release of old security bug reports.


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

### gi...@appspot.gserviceaccount.com (2024-01-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/8b86b97f3a70b2b0e8bcf5a2907c670c07e24967

commit 8b86b97f3a70b2b0e8bcf5a2907c670c07e24967
Author: Andrés Olivares <andoli@chromium.org>
Date: Wed Jan 03 12:50:41 2024

Actually disable extensions test to allow for devtools roll

Bug: 142169
Change-Id: Iaaca44b73beef6e151d94e53d43389568bddcc39
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5164107
Reviewed-by: Wolfgang Beyer <wolfi@chromium.org>
Reviewed-by: Alex Rudenko <alexrudenko@chromium.org>
Commit-Queue: Andres Olivares <andoli@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1242375}

[modify] https://crrev.com/8b86b97f3a70b2b0e8bcf5a2907c670c07e24967/third_party/blink/web_tests/TestExpectations


### is...@google.com (2024-01-03)

This issue was migrated from crbug.com/chromium/142169?no_tracker_redirect=1

[Multiple monorail components: Internals, Internals>Skia]
[Monorail mergedwith: crbug.com/chromium/168735]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40063405)*
