# Use after free in ListIterms and RunIns rendering (from bug 88680)

| Field | Value |
|-------|-------|
| **Issue ID** | [40094745](https://issues.chromium.org/issues/40094745) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | in...@chromium.org |
| **Assignee** | in...@chromium.org |
| **Created** | 2011-09-07 |
| **Bounty** | $1,000.00 |

## Description

credit miaubiz

Testcase.xhtml::
<html xmlns="http://www.w3.org/1999/xhtml" >

  <head>
<style>
li:before {
    display: table-row-group;
    content: "hello";
}


</style>   </head>  <body>   
   
         
                            
                   <body>
<style type="text/css">
@font-face { font-family: "Ahhhem"; src: url(../fonts/Ahem.ttf); }
html { background: white; }
body { font-family: Ahhhem; font-size: 50px; height: 2ex; width: 2ex; background: blue;  }
</style>                          
                  </body>
          
   
      <ul> 
        <li>test
        
        </li> 
      </ul>
   
  </body>

</html>

ASAN:SIGILL
=================================================================
==6283== ERROR: AddressSanitizer heap-use-after-free on address 0x00007f5809d55890 at pc 0x7f5851cd1c74 bp 0x7f582e0ed7f0 sp 0x7f582e0ed7e0
READ of size 4 at 0x00007f5809d55890 thread T12
    #0 0x7f5851cd1c74 in WebCore::FontMetrics::ascent(WebCore::FontBaseline) const third_party/WebKit/Source/WebCore/platform/graphics/FontMetrics.h:80
    #1 0x7f5852be4682 in WebCore::RenderBlock::firstLineBoxBaseline() const third_party/WebKit/Source/WebCore/rendering/RenderBlock.cpp:5337
    #2 0x7f5852d450cd in WebCore::RenderTableCell::cellBaselinePosition() const third_party/WebKit/Source/WebCore/rendering/RenderTableCell.cpp:300
    #3 0x7f5852d50ac0 in WebCore::RenderTableSection::calcRowLogicalHeight() third_party/WebKit/Source/WebCore/rendering/RenderTableSection.cpp:377
    #4 0x7f5852d3a286 in WebCore::RenderTable::layout() third_party/WebKit/Source/WebCore/rendering/RenderTable.cpp:310
    #5 0x7f5852bcae76 in WebCore::RenderBlock::layoutBlockChild(WebCore::RenderBox*, WebCore::RenderBlock::MarginInfo&, int&, int&) third_party/WebKit/Source/WebCore/rendering/RenderBlock.cpp:2038
    #6 0x7f5852bbfe4c in WebCore::RenderBlock::layoutBlockChildren(bool, int&) third_party/WebKit/Source/WebCore/rendering/RenderBlock.cpp:1973
    #7 0x7f5852bbbdd0 in WebCore::RenderBlock::layoutBlock(bool, int, WebCore::RenderBlock::BlockLayoutPass) third_party/WebKit/Source/WebCore/rendering/RenderBlock.cpp:1290
    #8 0x7f5852bbb531 in WebCore::RenderBlock::layout() third_party/WebKit/Source/WebCore/rendering/RenderBlock.cpp:1177
    #9 0x7f5852bcae76 in WebCore::RenderBlock::layoutBlockChild(WebCore::RenderBox*, WebCore::RenderBlock::MarginInfo&, int&, int&) third_party/WebKit/Source/WebCore/rendering/RenderBlock.cpp:2038
    #10 0x7f5852bbfe4c in WebCore::RenderBlock::layoutBlockChildren(bool, int&) third_party/WebKit/Source/WebCore/rendering/RenderBlock.cpp:1973
    #11 0x7f5852bbbdd0 in WebCore::RenderBlock::layoutBlock(bool, int, WebCore::RenderBlock::BlockLayoutPass) third_party/WebKit/Source/WebCore/rendering/RenderBlock.cpp:1290
    #12 0x7f5852bbb531 in WebCore::RenderBlock::layout() third_party/WebKit/Source/WebCore/rendering/RenderBlock.cpp:1177
    #13 0x7f5852bcae76 in WebCore::RenderBlock::layoutBlockChild(WebCore::RenderBox*, WebCore::RenderBlock::MarginInfo&, int&, int&) third_party/WebKit/Source/WebCore/rendering/RenderBlock.cpp:2038
    #14 0x7f5852bbfe4c in WebCore::RenderBlock::layoutBlockChildren(bool, int&) third_party/WebKit/Source/WebCore/rendering/RenderBlock.cpp:1973
    #15 0x7f5852bbbdd0 in WebCore::RenderBlock::layoutBlock(bool, int, WebCore::RenderBlock::BlockLayoutPass) third_party/WebKit/Source/WebCore/rendering/RenderBlock.cpp:1290
    #16 0x7f5852bbb531 in WebCore::RenderBlock::layout() third_party/WebKit/Source/WebCore/rendering/RenderBlock.cpp:1177
    #17 0x7f5852bcae76 in WebCore::RenderBlock::layoutBlockChild(WebCore::RenderBox*, WebCore::RenderBlock::MarginInfo&, int&, int&) third_party/WebKit/Source/WebCore/rendering/RenderBlock.cpp:2038
    #18 0x7f5852bbfe4c in WebCore::RenderBlock::layoutBlockChildren(bool, int&) third_party/WebKit/Source/WebCore/rendering/RenderBlock.cpp:1973
    #19 0x7f5852bbbdd0 in WebCore::RenderBlock::layoutBlock(bool, int, WebCore::RenderBlock::BlockLayoutPass) third_party/WebKit/Source/WebCore/rendering/RenderBlock.cpp:1290
    #20 0x7f5852bbb531 in WebCore::RenderBlock::layout() third_party/WebKit/Source/WebCore/rendering/RenderBlock.cpp:1177
    #21 0x7f5852bcae76 in WebCore::RenderBlock::layoutBlockChild(WebCore::RenderBox*, WebCore::RenderBlock::MarginInfo&, int&, int&) third_party/WebKit/Source/WebCore/rendering/RenderBlock.cpp:2038
    #22 0x7f5852bbfe4c in WebCore::RenderBlock::layoutBlockChildren(bool, int&) third_party/WebKit/Source/WebCore/rendering/RenderBlock.cpp:1973
    #23 0x7f5852bbbdd0 in WebCore::RenderBlock::layoutBlock(bool, int, WebCore::RenderBlock::BlockLayoutPass) third_party/WebKit/Source/WebCore/rendering/RenderBlock.cpp:1290
    #24 0x7f5852bbb531 in WebCore::RenderBlock::layout() third_party/WebKit/Source/WebCore/rendering/RenderBlock.cpp:1177
    #25 0x7f5852d911e9 in WebCore::RenderView::layout() third_party/WebKit/Source/WebCore/rendering/RenderView.cpp:134
    #26 0x7f5852855370 in WebCore::FrameView::layout(bool) third_party/WebKit/Source/WebCore/page/FrameView.cpp:1078
    #27 0x7f5852209360 in WebCore::ThreadTimers::sharedTimerFiredInternal() third_party/WebKit/Source/WebCore/platform/ThreadTimers.cpp:115
    #28 0x7f5850856409 in base::subtle::TaskClosureAdapter::Run() base/task.cc:56
    #29 0x7f58507f6922 in MessageLoop::RunTask(MessageLoop::PendingTask const&) base/message_loop.cc:477
    #30 0x7f58507f6d64 in MessageLoop::DeferOrRunPendingTask(MessageLoop::PendingTask const&) base/message_loop.cc:492
    #31 0x7f58507f70f3 in MessageLoop::DoWork() base/message_loop.cc:682
    #32 0x7f5850802c05 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) base/message_pump_default.cc:23
    #33 0x7f58507f62c8 in MessageLoop::RunInternal() base/message_loop.cc:443
    #34 0x7f58507f5244 in MessageLoop::Run() base/message_loop.cc:341
    #35 0x7f5850859ebe in base::Thread::ThreadMain() base/threading/thread.cc:163
    #36 0x7f58508590ec in base::(anonymous namespace)::ThreadFunc(void*) base/threading/platform_thread_posix.cc:58
    #37 0x7f5854940971 in AsanThread::ThreadStart() /usr/local/google/asan/address-sanitizer/asan/asan_thread.cc:102
    #38 0x7f584b1b59ca in start_thread ??:0
    #39 0x7f584911370d in __clone ??:0
0x00007f5809d55890 is located 16 bytes inside of 1208-byte region [0x00007f5809d55880,0x00007f5809d55d38)
freed by thread T12 here:
    #0 0x7f5854937c23 in free _asan_rtl_
    #1 0x7f5851f90598 in WTF::VectorDestructor<true, WTF::OwnPtr<WebCore::FontData> >::destruct(WTF::OwnPtr<WebCore::FontData>*, WTF::OwnPtr<WebCore::FontData>*) third_party/WebKit/Source/JavaScriptCore/wtf/Vector.h:79
    #2 0x7f5851f9032f in WTF::Vector<WTF::OwnPtr<WebCore::FontData>, 0ul>::shrink(unsigned long) third_party/WebKit/Source/JavaScriptCore/wtf/Vector.h:862
    #3 0x7f5851f90286 in WTF::Vector<WTF::OwnPtr<WebCore::FontData>, 0ul>::shrinkCapacity(unsigned long) third_party/WebKit/Source/JavaScriptCore/wtf/Vector.h:923
    #4 0x7f5851f5ca5d in WebCore::Document::recalcStyle(WebCore::Node::StyleChange) third_party/WebKit/Source/WebCore/dom/Document.cpp:1571
    #5 0x7f5851f5e39e in WebCore::Document::updateStyleIfNeeded() third_party/WebKit/Source/WebCore/dom/Document.cpp:1621
    #6 0x7f5852209360 in WebCore::ThreadTimers::sharedTimerFiredInternal() third_party/WebKit/Source/WebCore/platform/ThreadTimers.cpp:115
    #7 0x7f5850856409 in base::subtle::TaskClosureAdapter::Run() base/task.cc:56
    #8 0x7f58507f6922 in MessageLoop::RunTask(MessageLoop::PendingTask const&) base/message_loop.cc:477
    #9 0x7f58507f6d64 in MessageLoop::DeferOrRunPendingTask(MessageLoop::PendingTask const&) base/message_loop.cc:492
    #10 0x7f58507f70f3 in MessageLoop::DoWork() base/message_loop.cc:682
    #11 0x7f5850802c05 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) base/message_pump_default.cc:23
    #12 0x7f58507f62c8 in MessageLoop::RunInternal() base/message_loop.cc:443
    #13 0x7f58507f5244 in MessageLoop::Run() base/message_loop.cc:341
    #14 0x7f5850859ebe in base::Thread::ThreadMain() base/threading/thread.cc:163
    #15 0x7f58508590ec in base::(anonymous namespace)::ThreadFunc(void*) base/threading/platform_thread_posix.cc:58
    #16 0x7f5854940971 in AsanThread::ThreadStart() /usr/local/google/asan/address-sanitizer/asan/asan_thread.cc:102
    #17 0x7f584b1b59ca in start_thread ??:0
    #18 0x7f584911370d in __clone ??:0
previously allocated by thread T12 here:
    #0 0x7f5854937b13 in malloc _asan_rtl_
    #1 0x7f5851d4fc0b in WTF::fastMalloc(unsigned long) third_party/WebKit/Source/JavaScriptCore/wtf/FastMalloc.cpp:285
    #2 0x7f5852b507dc in WebCore::CSSFontFaceSource::getFontData(WebCore::FontDescription const&, bool, bool, WebCore::CSSFontSelector*) third_party/WebKit/Source/WebCore/css/CSSFontFaceSource.cpp:192
    #3 0x7f5852b4c7a3 in WebCore::CSSFontFace::getFontData(WebCore::FontDescription const&, bool, bool) third_party/WebKit/Source/WebCore/css/CSSFontFace.cpp:112
    #4 0x7f58529dd490 in WebCore::CSSSegmentedFontFace::getFontData(WebCore::FontDescription const&) third_party/WebKit/Source/WebCore/css/CSSSegmentedFontFace.cpp:107
    #5 0x7f58529b178a in WebCore::CSSFontSelector::getFontData(WebCore::FontDescription const&, WTF::AtomicString const&) third_party/WebKit/Source/WebCore/css/CSSFontSelector.cpp:585
    #6 0x7f585223fcc6 in WebCore::FontCache::getFontData(WebCore::Font const&, int&, WebCore::FontSelector*) third_party/WebKit/Source/WebCore/platform/graphics/FontCache.cpp:414
    #7 0x7f585224eb74 in WebCore::FontFallbackList::fontDataAt(WebCore::Font const*, unsigned int) const third_party/WebKit/Source/WebCore/platform/graphics/FontFallbackList.cpp:105
    #8 0x7f5851cd1d5f in WebCore::FontFallbackList::primarySimpleFontData(WebCore::Font const*) third_party/WebKit/Source/WebCore/platform/graphics/FontFallbackList.h:71
    #9 0x7f5851cd1b89 in WebCore::Font::fontMetrics() const third_party/WebKit/Source/WebCore/platform/graphics/Font.h:132
    #10 0x7f5852528c8d in WebCore::CSSPrimitiveValue::computeLengthDouble(WebCore::RenderStyle*, WebCore::RenderStyle*, double, bool) third_party/WebKit/Source/WebCore/css/CSSPrimitiveValue.cpp:366
    #11 0x7f5852528ecc in WebCore::Length WebCore::CSSPrimitiveValue::computeLength<WebCore::Length>(WebCore::RenderStyle*, WebCore::RenderStyle*, double, bool) third_party/WebKit/Source/WebCore/css/CSSPrimitiveValue.cpp:322
    #12 0x7f58529fdd00 in WebCore::ApplyPropertyLength<(WebCore::LengthAuto)1, (WebCore::LengthIntrinsic)1, (WebCore::LengthMinIntrinsic)1, (WebCore::LengthNone)0, (WebCore::LengthUndefined)0, (WebCore::LengthFlexDirection)2>::applyValue(WebCore::CSSStyleSelector*, WebCore::CSSValue*) const third_party/WebKit/Source/WebCore/css/CSSStyleApplyProperty.cpp:326
    #13 0x7f5852561ba3 in WebCore::CSSStyleSelector::applyProperty(int, WebCore::CSSValue*) third_party/WebKit/Source/WebCore/css/CSSStyleSelector.cpp:3600
    #14 0x7f585256e9c2 in void WebCore::CSSStyleSelector::applyDeclarations<false>(bool, int, int) third_party/WebKit/Source/WebCore/css/CSSStyleSelector.cpp:3369
    #15 0x7f585255710d in WebCore::CSSStyleSelector::styleForElement(WebCore::Element*, WebCore::RenderStyle*, bool, bool, bool) third_party/WebKit/Source/WebCore/css/CSSStyleSelector.cpp:1454
    #16 0x7f5851fddbef in WebCore::Node::styleForRenderer(WebCore::NodeRenderingContext const&) third_party/WebKit/Source/WebCore/dom/Node.cpp:1475
    #17 0x7f5851fb3041 in WebCore::Element::recalcStyle(WebCore::Node::StyleChange) third_party/WebKit/Source/WebCore/dom/Element.cpp:1070
    #18 0x7f5851fb387e in WebCore::Element::recalcStyle(WebCore::Node::StyleChange) third_party/WebKit/Source/WebCore/dom/Element.cpp:1150
    #19 0x7f5851f5ca45 in WebCore::Document::recalcStyle(WebCore::Node::StyleChange) third_party/WebKit/Source/WebCore/dom/Document.cpp:1559
    #20 0x7f5851f5ed7f in WebCore::Document::styleSelectorChanged(WebCore::StyleSelectorUpdateFlag) third_party/WebKit/Source/WebCore/dom/Document.cpp:2900
    #21 0x7f58529450fd in WebCore::XMLDocumentParser::end() third_party/WebKit/Source/WebCore/xml/parser/XMLDocumentParser.cpp:214
    #22 0x7f5852759c4c in WebCore::DocumentWriter::endIfNotLoadingMainResource() third_party/WebKit/Source/WebCore/loader/DocumentWriter.cpp:236
Thread T12 created by T0 here:
    #0 0x7f5854936dc7 in pthread_create _asan_rtl_
    #1 0x7f5850858e92 in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThread::Delegate*, unsigned long*) base/threading/platform_thread_posix.cc:119
    #2 0x7f5850858daa in base::PlatformThread::Create(unsigned long, base::PlatformThread::Delegate*, unsigned long*) base/threading/platform_thread_posix.cc:230
    #3 0x7f5850859721 in base::Thread::StartWithOptions(base::Thread::Options const&) base/threading/thread.cc:74
    #4 0x7f5853a64cfb in BrowserRenderProcessHost::Init(bool) content/browser/renderer_host/browser_render_process_host.cc:316
    #5 0x7f5853ad174b in RenderViewHost::CreateRenderView(std::basic_string<unsigned short, base::string16_char_traits, std::allocator<unsigned short> > const&) content/browser/renderer_host/render_view_host.cc:161
    #6 0x7f5853b7b7a4 in TabContents::CreateRenderViewForRenderManager(RenderViewHost*) content/browser/tab_contents/tab_contents.cc:1962
    #7 0x7f5853b7b8bd in non-virtual thunk to TabContents::CreateRenderViewForRenderManager(RenderViewHost*) ???:0
    #8 0x7f5853b676cb in RenderViewHostManager::InitRenderView(RenderViewHost*, NavigationEntry const&) content/browser/tab_contents/render_view_host_manager.cc:563
    #9 0x7f5853b668ba in RenderViewHostManager::Navigate(NavigationEntry const&) content/browser/tab_contents/render_view_host_manager.cc:101
    #10 0x7f5853b74088 in TabContents::NavigateToEntry(NavigationEntry const&, NavigationController::ReloadType) content/browser/tab_contents/tab_contents.cc:575
    #11 0x7f5853b73ff5 in TabContents::NavigateToPendingEntry(NavigationController::ReloadType) content/browser/tab_contents/tab_contents.cc:569
    #12 0x7f5853b5b62f in NavigationController::NavigateToPendingEntry(NavigationController::ReloadType) content/browser/tab_contents/navigation_controller.cc:1068
    #13 0x7f5853b5bf8c in NavigationController::LoadEntry(NavigationEntry*) content/browser/tab_contents/navigation_controller.cc:279
    #14 0x7f584f79f884 in browser::Navigate(browser::NavigateParams*) chrome/browser/ui/browser_navigator.cc:482
    #15 0x7f584fff2870 in BrowserInit::LaunchWithProfile::OpenTabsInBrowser(Browser*, bool, std::vector<BrowserInit::LaunchWithProfile::Tab, std::allocator<BrowserInit::LaunchWithProfile::Tab> > const&) chrome/browser/ui/browser_init.cc:1080
    #16 0x7f584fff11e4 in BrowserInit::LaunchWithProfile::ProcessSpecifiedURLs(std::vector<GURL, std::allocator<GURL> > const&) chrome/browser/ui/browser_init.cc:990
    #17 0x7f584fff0eb3 in BrowserInit::LaunchWithProfile::ProcessStartupURLs(std::vector<GURL, std::allocator<GURL> > const&) chrome/browser/ui/browser_init.cc:957
    #18 0x7f584ffefefa in BrowserInit::LaunchWithProfile::ProcessLaunchURLs(bool, std::vector<GURL, std::allocator<GURL> > const&) chrome/browser/ui/browser_init.cc:878
    #19 0x7f584ffeefda in BrowserInit::LaunchWithProfile::Launch(Profile*, std::vector<GURL, std::allocator<GURL> > const&, bool) chrome/browser/ui/browser_init.cc:721
    #20 0x7f584ffedeec in BrowserInit::LaunchBrowser(CommandLine const&, Profile*, FilePath const&, bool, int*) chrome/browser/ui/browser_init.cc:575
    #21 0x7f584fff4299 in BrowserInit::ProcessCmdLineImpl(CommandLine const&, FilePath const&, bool, Profile*, int*, BrowserInit*) chrome/browser/ui/browser_init.cc:1487
    #22 0x7f5850231e6a in BrowserInit::Start(CommandLine const&, FilePath const&, Profile*, int*) ./chrome/browser/ui/browser_init.h:38
    #23 0x7f585022fcda in ChromeBrowserMainParts::TemporaryContinue() chrome/browser/browser_main.cc:1801
    #24 0x7f5853939021 in BrowserMain(MainFunctionParams const&) content/browser/browser_main.cc:311
    #25 0x7f58506de8d4 in (anonymous namespace)::RunNamedProcessTypeMain(std::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, MainFunctionParams const&, content::ContentMainDelegate*) content/app/content_main.cc:292
    #26 0x7f58506de057 in content::ContentMain(int, char**, content::ContentMainDelegate*) content/app/content_main.cc:482
    #27 0x7f584f4f1207 in ChromeMain chrome/app/chrome_main.cc:764
    #28 0x7f584f4f394b in main chrome/app/chrome_exe_main_gtk.cc:18
    #29 0x7f584904bc4d in __libc_start_main ??:0
    #30 0x7f584f4f10b9 in _start ??:0
==6283== ABORTING
Shadow byte and word:
  0x00001feb013aab12: fd
  0x00001feb013aab10: fd fd fd fd fd fd fd fd
More shadow bytes:
  0x00001feb013aaaf0: fa fa fa fa fa fa fa fa
  0x00001feb013aaaf8: fa fa fa fa fa fa fa fa
  0x00001feb013aab00: fa fa fa fa fa fa fa fa
  0x00001feb013aab08: fa fa fa fa fa fa fa fa
=>0x00001feb013aab10: fd fd fd fd fd fd fd fd
  0x00001feb013aab18: fd fd fd fd fd fd fd fd
  0x00001feb013aab20: fd fd fd fd fd fd fd fd
  0x00001feb013aab28: fd fd fd fd fd fd fd fd
  0x00001feb013aab30: fd fd fd fd fd fd fd fd

## Attachments

- [table.html](attachments/table.html) (text/plain; charset=us-ascii, 241 B)

## Timeline

### mi...@gmail.com (2011-09-07)

here's a crashing repro also

### mi...@gmail.com (2011-09-07)

oh right, the original also crashes if you just select all manually.

### in...@chromium.org (2011-09-07)

https://bugs.webkit.org/show_bug.cgi?id=67735

### in...@chromium.org (2011-09-08)

Another testcase I wrote that shows the problem with runins as well [see the two ABCds]. The problem is in RenderObjectChildList::beforePseudoElementRenderer(const RenderObject* owner)

<style>
#test::before {
    content: "ABCD";
}
</style>                          
<div style="display: run-in">EFGH</div><div id="test">IJKL</div>
<script>
    document.body.offsetTop;
    document.body.style.fontSize = "800%";
</script>


Content-Type: text/plain
layer at (0,0) size 1004x585
  RenderView at (0,0) size 800x585
layer at (0,0) size 800x585
  RenderBlock {HTML} at (0,0) size 800x585
    RenderBody {BODY} at (8,8) size 784x569
      RenderBlock {DIV} at (0,0) size 784x147
        RenderInline (generated) at (0,0) size 354x147
          RenderText at (0,0) size 354x147
            text run at (0,0) width 354: "ABCD"
        RenderInline (run-in) {DIV} at (0,0) size 333x147
          RenderText {#text} at (354,0) size 333x147
            text run at (354,0) width 333: "EFGH"
        RenderInline (generated) at (0,0) size 46x18
          RenderText at (687,101) size 46x18
            text run at (687,101) width 46: "ABCD"
        RenderText {#text} at (733,0) size 263x147
          text run at (733,0) width 263: "IJKL"
#EOF

### in...@chromium.org (2011-09-08)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-09-09)

http://trac.webkit.org/changeset/94857

### in...@chromium.org (2011-09-19)

merged to m15 in r95426.

### in...@chromium.org (2011-09-23)

Merge-Merged-874

### js...@chromium.org (2011-09-26)

Covered in m14 by WebKit r95959.

### sc...@gmail.com (2011-10-03)

@miaubiz: thanks for your continuing help in this area :D $1000 for this one.

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

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/95672?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094745)*
