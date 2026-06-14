# Use after free in WebCore::Text::recalcStyle due to before after content issue in table parts

| Field | Value |
|-------|-------|
| **Issue ID** | [40094145](https://issues.chromium.org/issues/40094145) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | in...@chromium.org |
| **Assignee** | in...@chromium.org |
| **Created** | 2011-08-20 |
| **Bounty** | $1,000.00 |

## Description

found in my fuzzing + ASAN + ClusterFuzz

Bot CLUSTER_FUZZ_58 on platform LINUX
Chromium Revision : 96444
Webkit Revision : 92846

Testcase::
<style>

    #target::after { content: "AFTER"; display: table-row;</style>

<summary><div id="not-target"
style="color-interpolation: element; display: table; "<tt><tt> CONTENT
<script>
    document.getElementById("not-target").id = "target";
    document.body.offsetTop;
    document.body.style.color = "red";
</script>

/mnt/scratch0/chrome/src/out/Release/DumpRenderTree 

ASAN:SIGILL
==================================================================
HINT: if your stack trace looks short or garbled, use ASAN_OPTIONS=fast_unwind=0
==25981== ERROR: AddressSanitizer crashed on address 0x00007f676b2f4280 at pc 0x1832259 bp 0x7fff5f47e0f0 sp 0x7fff5f47dfe0
READ of size 8 at 0x00007f676b2f4280 thread T0
    #0 0x1832259 in WebCore::Text::recalcStyle(WebCore::Node::StyleChange) 
    #1 0x17637a6 in WebCore::Element::recalcStyle(WebCore::Node::StyleChange) 
    #2 0x17637a6 in WebCore::Element::recalcStyle(WebCore::Node::StyleChange) 
    #3 0x17637a6 in WebCore::Element::recalcStyle(WebCore::Node::StyleChange) 
    #4 0x17637a6 in WebCore::Element::recalcStyle(WebCore::Node::StyleChange) 
    #5 0x17637a6 in WebCore::Element::recalcStyle(WebCore::Node::StyleChange) 
    #6 0x170802e in WebCore::Document::recalcStyle(WebCore::Node::StyleChange) 
    #7 0x170b5d8 in WebCore::Document::updateStyleIfNeeded() 
    #8 0x170b8df in WebCore::Document::updateStyleForAllDocuments() 
    #9 0x1812b33 in WebCore::ScriptElement::executeScript(WebCore::ScriptSourceCode const&) 
    #10 0x180e85d in WebCore::ScriptElement::prepareScript(WTF::TextPosition<WTF::OneBasedNumber> const&, WebCore::ScriptElement::LegacyTypeSupport) 
    #11 0x1a0166c in WebCore::HTMLScriptRunner::runScript(WebCore::Element*, WTF::TextPosition<WTF::OneBasedNumber> const&) 
    #12 0x1a00fe2 in WebCore::HTMLScriptRunner::execute(WTF::PassRefPtr<WebCore::Element>, WTF::TextPosition<WTF::OneBasedNumber> const&) 
    #13 0x19f5319 in WebCore::HTMLDocumentParser::runScriptsForPausedTreeBuilder() 
    #14 0x19f56b0 in WebCore::HTMLDocumentParser::canTakeNextToken(WebCore::HTMLDocumentParser::SynchronousMode, WebCore::PumpSession&) 
    #15 0x19f4882 in WebCore::HTMLDocumentParser::pumpTokenizer(WebCore::HTMLDocumentParser::SynchronousMode) 
    #16 0x19f6414 in WebCore::HTMLDocumentParser::append(WebCore::SegmentedString const&) 
    #17 0x3da7a26 in WebCore::DecodedDataDocumentParser::flush(WebCore::DocumentWriter*) 
    #18 0x234aa39 in WebCore::DocumentWriter::endIfNotLoadingMainResource() 
    #19 0x2389d49 in WebCore::FrameLoader::finishedLoading() 
    #20 0x23ae920 in WebCore::MainResourceLoader::didFinishLoading(double) 
    #21 0x3049699 in webkit_glue::WebURLLoaderImpl::Context::OnCompletedRequest(net::URLRequestStatus const&, std::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, base::Time const&) 
    #22 0x316cf89 in (anonymous namespace)::RequestProxy::NotifyCompletedRequest(net::URLRequestStatus const&, std::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, base::Time const&) webkit/tools/test_shell/simple_resource_loader_bridge.cc:0
    #23 0xe38a19 in base::subtle::TaskClosureAdapter::Run() 
    #24 0xdfe6ac in MessageLoop::RunTask(MessageLoop::PendingTask const&) 
    #25 0xdfecb2 in MessageLoop::DeferOrRunPendingTask(MessageLoop::PendingTask const&) 
    #26 0xdffefe in MessageLoop::DoWork() 
    #27 0xe3eb0f in (anonymous namespace)::WorkSourceDispatch(_GSource*, int (*)(void*), void*) base/message_pump_glib.cc:0
    #28 0x7f67768778c2 in g_main_dispatch /build/buildd/glib2.0-2.24.1/glib/gmain.c:1960
    #29 0x7f677687b748 in g_main_context_iterate /build/buildd/glib2.0-2.24.1/glib/gmain.c:2591
    #30 0x7f677687b8fc in IA__g_main_context_iteration /build/buildd/glib2.0-2.24.1/glib/gmain.c:2654
    #31 0xe40da1 in base::MessagePumpGtk::RunOnce(_GMainContext*, bool) 
    #32 0xe3f6ad in base::MessagePumpGlib::RunWithDispatcher(base::MessagePump::Delegate*, base::MessagePumpDispatcher*) 
    #33 0xdfd5d7 in MessageLoop::RunInternal() 
    #34 0xdfc59e in MessageLoop::Run() 
    #35 0x480b65 in TestShell::waitTestFinished() 
    #36 0x47863d in TestShell::runFileTest(TestParams const&) 
    #37 0x42dbeb in runTest(TestShell&, TestParams&, std::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, bool) third_party/WebKit/Tools/DumpRenderTree/chromium/DumpRenderTree.cpp:0
    #38 0x42ca92 in main 
    #39 0x7f6774518c4d in __libc_start_main /build/buildd/eglibc-2.11.1/csu/libc-start.c:258
    #40 0x418d09 in _start 
0x00007f676b2f4280 is located 0 bytes inside of 96-byte region [0x00007f676b2f4280,0x00007f676b2f42e0)
freed by thread T0 here:
    #1 0x2b60937 in WebCore::RenderObjectChildList::updateBeforeAfterContent(WebCore::RenderObject*, WebCore::PseudoId, WebCore::RenderObject const*) 
    #2 0x2a8acbd in WebCore::RenderInline::styleDidChange(WebCore::StyleDifference, WebCore::RenderStyle const*) 
    #3 0x2b5340e in WebCore::RenderObject::setStyle(WTF::PassRefPtr<WebCore::RenderStyle>) 
    #4 0x2b52709 in WebCore::RenderObject::setAnimatableStyle(WTF::PassRefPtr<WebCore::RenderStyle>) 
    #5 0x17abe12 in WebCore::Node::setRenderStyle(WTF::PassRefPtr<WebCore::RenderStyle>) 
    #6 0x1763003 in WebCore::Element::recalcStyle(WebCore::Node::StyleChange) 
    #7 0x17637a6 in WebCore::Element::recalcStyle(WebCore::Node::StyleChange) 
    #8 0x17637a6 in WebCore::Element::recalcStyle(WebCore::Node::StyleChange) 
    #9 0x17637a6 in WebCore::Element::recalcStyle(WebCore::Node::StyleChange) 
    #10 0x17637a6 in WebCore::Element::recalcStyle(WebCore::Node::StyleChange) 
    #11 0x170802e in WebCore::Document::recalcStyle(WebCore::Node::StyleChange) 
    #12 0x170b5d8 in WebCore::Document::updateStyleIfNeeded() 
    #13 0x170b8df in WebCore::Document::updateStyleForAllDocuments() 
    #14 0x1812b33 in WebCore::ScriptElement::executeScript(WebCore::ScriptSourceCode const&) 
    #15 0x180e85d in WebCore::ScriptElement::prepareScript(WTF::TextPosition<WTF::OneBasedNumber> const&, WebCore::ScriptElement::LegacyTypeSupport) 
    #16 0x1a0166c in WebCore::HTMLScriptRunner::runScript(WebCore::Element*, WTF::TextPosition<WTF::OneBasedNumber> const&) 
    #17 0x1a00fe2 in WebCore::HTMLScriptRunner::execute(WTF::PassRefPtr<WebCore::Element>, WTF::TextPosition<WTF::OneBasedNumber> const&) 
    #18 0x19f5319 in WebCore::HTMLDocumentParser::runScriptsForPausedTreeBuilder() 
    #19 0x19f56b0 in WebCore::HTMLDocumentParser::canTakeNextToken(WebCore::HTMLDocumentParser::SynchronousMode, WebCore::PumpSession&) 
    #20 0x19f4882 in WebCore::HTMLDocumentParser::pumpTokenizer(WebCore::HTMLDocumentParser::SynchronousMode) 
    #21 0x19f6414 in WebCore::HTMLDocumentParser::append(WebCore::SegmentedString const&) 
    #22 0x3da7a26 in WebCore::DecodedDataDocumentParser::flush(WebCore::DocumentWriter*) 
    #23 0x234aa39 in WebCore::DocumentWriter::endIfNotLoadingMainResource() 
    #24 0x2389d49 in WebCore::FrameLoader::finishedLoading() 
    #25 0x23ae920 in WebCore::MainResourceLoader::didFinishLoading(double) 
    #26 0x3049699 in webkit_glue::WebURLLoaderImpl::Context::OnCompletedRequest(net::URLRequestStatus const&, std::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, base::Time const&) 
    #27 0x316cf89 in (anonymous namespace)::RequestProxy::NotifyCompletedRequest(net::URLRequestStatus const&, std::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, base::Time const&) webkit/tools/test_shell/simple_resource_loader_bridge.cc:0
    #28 0xe38a19 in base::subtle::TaskClosureAdapter::Run() 
    #29 0xdfe6ac in MessageLoop::RunTask(MessageLoop::PendingTask const&) 
previously allocated by thread T0 here:
    #1 0x18318ec in WebCore::Text::createRenderer(WebCore::RenderArena*, WebCore::RenderStyle*) 
    #2 0x17cad55 in WebCore::NodeRendererFactory::createRendererAndStyle() 
    #3 0x17cb385 in WebCore::NodeRendererFactory::createRendererIfNeeded() 
    #4 0x17ab112 in WebCore::Node::createRendererIfNeeded() 
    #5 0x1831bb1 in WebCore::Text::attach() 
    #6 0x16d9ac9 in WebCore::ContainerNode::attach() 
    #7 0x1760f19 in WebCore::Element::attach() 
    #8 0x16d9ac9 in WebCore::ContainerNode::attach() 
    #9 0x1760f19 in WebCore::Element::attach() 
    #10 0x182241c in WebCore::ShadowContentElement::attach() 
    #11 0x16d9ac9 in WebCore::ContainerNode::attach() 
    #12 0x1825ad1 in WebCore::ShadowRoot::attach() 
    #13 0x18257f7 in WebCore::ShadowRoot::recalcStyle(WebCore::Node::StyleChange) 
    #14 0x1763b19 in WebCore::Element::recalcStyle(WebCore::Node::StyleChange) 
    #15 0x17637a6 in WebCore::Element::recalcStyle(WebCore::Node::StyleChange) 
    #16 0x17637a6 in WebCore::Element::recalcStyle(WebCore::Node::StyleChange) 
    #17 0x170802e in WebCore::Document::recalcStyle(WebCore::Node::StyleChange) 
    #18 0x170b5d8 in WebCore::Document::updateStyleIfNeeded() 
    #19 0x170bb3d in WebCore::Document::updateLayout() 
    #20 0x170be87 in WebCore::Document::updateLayoutIgnorePendingStylesheets() 
    #21 0x175607c in WebCore::Element::offsetTop() 
    #22 0x7e3e80 in WebCore::ElementInternal::offsetTopAttrGetter(v8::Local<v8::String>, v8::AccessorInfo const&) out/Release/obj/gen/webkit/bindings/V8DerivedSources03.cpp:0
    #23 0x1279812 in v8::internal::Object::GetPropertyWithCallback(v8::internal::Object*, v8::internal::Object*, v8::internal::String*, v8::internal::Object*) 
==25981== ABORTING
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
  0x00001feced65e850: fb
  0x00001feced65e850: fb fb fb fb fb fb fb fb
More shadow bytes:
  0x00001feced65e830: 00 00 00 00 00 00 00 00
  0x00001feced65e838: 00 00 00 00 00 fa fa fa
  0x00001feced65e840: ff ff ff ff ff ff ff ff
  0x00001feced65e848: ff ff ff ff ff ff ff ff
=>0x00001feced65e850: fb fb fb fb fb fb fb fb
  0x00001feced65e858: fb fb fb fb fb fb fb fb
  0x00001feced65e860: ff ff ff ff ff ff ff ff
  0x00001feced65e868: ff ff ff ff ff ff ff ff
  0x00001feced65e870: fb fb fb fb fb fb fb fb
	base::debug::StackTrace::StackTrace() [0xe4b986]
	base::(anonymous namespace)::StackDumpSignalHandler() [0xe2692b]
	0x7f677452daf0
	0x7f677452da75
	0x7f67745315c0
	asan_report_error() [0x43d2958]
	0x7f677541f8f0
	WebCore::Text::recalcStyle() [0x1832259]
	WebCore::Element::recalcStyle() [0x17637a6]



## Timeline

### pa...@google.com (2011-08-20)

Verified on 15 on OS X; verified not present on 13 on OS X.

### in...@chromium.org (2011-08-22)

Bug became evident after http://trac.webkit.org/changeset/92744, but real bug might be somewhere else. Keeping m14 for now.
Upstreamed - https://bugs.webkit.org/show_bug.cgi?id=66699

### in...@chromium.org (2011-08-23)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-08-25)

http://trac.webkit.org/changeset/93794

### in...@chromium.org (2011-08-25)

This patch touches some sensitive areas, so we should either merge quick to m14 and get some data (if any breakage) or let it roll into m15.

### in...@chromium.org (2011-08-25)

Chromium rebaselines - http://trac.webkit.org/changeset/93803

### sc...@gmail.com (2011-08-26)

Merged to M14: http://trac.webkit.org/changeset/93794

Joyously, this also fixes https://code.google.com/p/chromium/issues/detail?id=93132 from miaubiz. Since miaubiz's bug came in first, it is eligible for the reward.

### sc...@gmail.com (2011-08-26)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-09-08)

@miaubiz: seems like you found a variant first, therefore thanks! And a $1000 Chromium Security Reward.

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

### js...@chromium.org (2011-10-05)

Batch update.

### sc...@gmail.com (2011-10-28)

Looks like we failed to pay out this one. I'll do it now :)

### sc...@gmail.com (2011-11-03)

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

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/93587?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/93132]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094145)*
