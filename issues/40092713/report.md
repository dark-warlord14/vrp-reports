# Use after free in SVGUseElement::buildShadowTree

| Field | Value |
|-------|-------|
| **Issue ID** | [40092713](https://issues.chromium.org/issues/40092713) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | mi...@gmail.com |
| **Assignee** | si...@chromium.org |
| **Created** | 2011-07-17 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

use-after-free

**VERSION**  

Chrome Version: trunk, chromium-nightly  

Operating System: linux 64bit

**REPRODUCTION CASE**  

attached

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: renderer

## Attachments

- [6110cd5b86ac0bd6d1cd5ce03d8399eff41a3f44.html](attachments/6110cd5b86ac0bd6d1cd5ce03d8399eff41a3f44.html) (text/html; charset=us-ascii, 338 B)
- [vg-89558.txt](attachments/vg-89558.txt) (text/plain; charset=us-ascii, 15.2 KB)
- [asan-89558.txt](attachments/asan-89558.txt) (text/plain; charset=us-ascii, 8.4 KB)
- [svg.html](attachments/svg.html) (text/plain; charset=us-ascii, 102 B)

## Timeline

### mi...@gmail.com (2011-07-17)

valgrind log

Invalid read of size 1
   at 0x169EA2B: WebCore::ContainerNode::appendChild(WTF::PassRefPtr<WebCore::Node>, int&, bool) (ContainerNode.cpp:653)

 Address 0x364ff7c9 is 73 bytes inside a block of size 384 free'd
   at 0x4C2901A: operator delete(void*) (vg_replace_malloc.c:915)
   by 0x1E45321: WebCore::RenderSVGShadowTreeRootContainer::~RenderSVGShadowTreeRootContainer() (TreeShared.h:79)
 
Invalid read of size 8
   at 0x16E3BC2: WebCore::Node::dispatchSubtreeModifiedEvent() (Node.cpp:2848)
   by 0x169EC3D: WebCore::ContainerNode::appendChild(WTF::PassRefPtr<WebCore::Node>, int&, bool) (ContainerNode.cpp:666)


### mi...@gmail.com (2011-07-17)

Chromium	14.0.823.0 (Developer Build 92642) Ubuntu 11.04
OS	Linux
WebKit	535.1 (trunk@91024)
JavaScript	V8 3.4.12.1

is the chromium-browser version

### in...@chromium.org (2011-07-17)

Miaubiz confirmed me this crashes in ASAN over chat.

James, this same bug svg execute script bug came back. I remember you removed the hack we added in http://trac.webkit.org/changeset/90970. Mind taking a look?

### in...@chromium.org (2011-07-17)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-07-17)

[Empty comment from Monorail migration]

### mi...@gmail.com (2011-07-17)

asan log here with symbols

### in...@chromium.org (2011-07-17)

[Empty comment from Monorail migration]

### mi...@gmail.com (2011-07-17)

here is minimized:

<svg>

<g>

<use xlink:href="#test"/>

<rect id="test">

<script>

document.body.innerHTML = "PASS";


the unclosed script tag seems to be the thing.

### si...@chromium.org (2011-07-18)

Abhishek, we need to bring back your fix from:

https://bugs.webkit.org/show_bug.cgi?id=62225

In that bug, we had a problem where the <use> element was coming into play after the <script> should've executed. Fixing SVG script execution fixed that particular test case, but there's still an underlying issue with the <use> tag, which you had fixed in your patch. I locally applied your patch from the WebKit bug and it seems to fix this crash, or at least Valgrind no longer warns about it.

Just to be sure, I put my hack back in and stepped through the code. My hack does not execute here. My hack only prevented scripts from running within the shadow DOM. In the example from https://crbug.com/chromium/89558#c8, the script is running directly in the main DOM.

As an aside, the closing </script> is probably just flakiness. I see Valgrind complain with and without it.

### si...@chromium.org (2011-07-19)

I've done more digging. There are now two bugs that need to be fixed.

The thing that makes svg.html different than our existing layout test (use-style-recalc-script-execute-crash.html) is that it's missing the closing tags. The script itself is inserted in foreign content mode. When we encounter the EOF in foreign content mode, we reach undefined behavior in the HTML spec. WebKit just treats this as a parse error and doesn't run the script. Now we're back to the same situation that started webkit https://crbug.com/chromium/62225, where the original script didn't run, so we run the cloned script inside the shadow DOM.

So, that's a bug in the spec. I can file that and implement whatever fix is needed in the parser.

However, this is still broken even with a proper </script>.

The problem is that when we reach </script>, we don't execute it right away. We decide we want to get our first paint in instead. So, the parser yields instead of executing the script and recalcStyle() is called. It builds the shadow DOM for <use>, which clones our un-run <script>. The clone copies m_alreadyStarted, but the original hasn't been run, so m_alreadyStarted is false. Seeing that the clone's m_alreadyStarted is false, the script gets executed when it's inserted into the shadow DOM.

This is also the cause of https://crbug.com/chromium/89455.

With both of these bugs, my hack is enough to prevent them. So, despite it being ugly and non-conformant, I will put it back in for the time being.

### in...@chromium.org (2011-07-19)

Thanks James for the analysis. If we get one more svg bug on the same stack, we will use my fix next time. Deal :) For now, i now like your fix since that is what the reviewer will ask too :) which is why the script didn't execute.

### in...@chromium.org (2011-07-20)

part 1 went in http://trac.webkit.org/changeset/91382

### in...@chromium.org (2011-07-21)

Just a fyi,,

Testcase::
<!DOCTYPE html>
<html>
Test passes if it does not crash and "script" inside "rect" executes.
<script>
if (window.layoutTestController)
    layoutTestController.dumpAsText();
</script>
<svg>
<g>
<use xlink:href="#test"/>
<rect id="test">
<script>
document.body.innerHTML = "PASS";
</script>
</rect>
</g>
</svg>
</html>

crashed with ASAN + DumpRenderTree 

Bot CLUSTER_FUZZ_5 on platform LINUX
Chromium Revision : 93211
Webkit Revision : 91310

So, looks like this unmodified layouttest would crash under any memory debugging tool. Glad you brought back the hack in http://trac.webkit.org/changeset/91382. Weird, i dont understand why it didnt reproduce on all the bots.

==================================================================
HINT: if your stack trace looks short or garbled, use ASAN_OPTIONS=fast_unwind=0
==19072== ERROR: AddressSanitizer crashed on address 0x00007effa6e4dd48 at pc 0x16574ca bp 0x7fff5379d8d0 sp 0x7fff5379d6e0
READ of size 4 at 0x00007effa6e4dd48 thread T0
    #0 0x16574ca in WebCore::ContainerNode::appendChild(WTF::PassRefPtr<WebCore::Node>, int&, bool) 
    #1 0x2d6ed90 in WebCore::SVGUseElement::buildShadowTree(WebCore::SVGShadowTreeRootElement*, WebCore::SVGElement*, WebCore::SVGElementInstance*) 
    #2 0x2d6d6b4 in WebCore::SVGUseElement::buildShadowAndInstanceTree(WebCore::SVGShadowTreeRootElement*) 
    #3 0x2de1059 in WebCore::RenderSVGShadowTreeRootContainer::updateFromElement() 
    #4 0x16e65a6 in WebCore::Element::recalcStyle(WebCore::Node::StyleChange) 
    #5 0x16e65a6 in WebCore::Element::recalcStyle(WebCore::Node::StyleChange) 
    #6 0x16e65a6 in WebCore::Element::recalcStyle(WebCore::Node::StyleChange) 
    #7 0x16e65a6 in WebCore::Element::recalcStyle(WebCore::Node::StyleChange) 
    #8 0x168b4de in WebCore::Document::recalcStyle(WebCore::Node::StyleChange) 
    #9 0x168eb18 in WebCore::Document::updateStyleIfNeeded() 
    #10 0x23f2ab1 in WebCore::FrameView::layout(bool) 
    #11 0x1a8dabf in WebCore::ThreadTimers::sharedTimerFiredInternal() 
    #12 0xdcf089 in (anonymous namespace)::TaskClosureAdapter::Run() base/message_loop.cc:0
    #13 0xdd2afc in MessageLoop::RunTask(MessageLoop::PendingTask const&) 
    #14 0xdd3112 in MessageLoop::DeferOrRunPendingTask(MessageLoop::PendingTask const&) 
    #15 0xdd4362 in MessageLoop::DoWork() 
    #16 0xe14334 in base::MessagePumpGlib::RunWithDispatcher(base::MessagePump::Delegate*, base::MessagePumpDispatcher*) 
    #17 0xdd1a66 in MessageLoop::RunInternal() 
    #18 0xdd0a5a in MessageLoop::Run() 
    #19 0x47e665 in TestShell::waitTestFinished() 
    #20 0x476148 in TestShell::runFileTest(TestParams const&) 
    #21 0x42e20d in runTest(TestShell&, TestParams&, std::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, bool) third_party/WebKit/Tools/DumpRenderTree/chromium/DumpRenderTree.cpp:0
    #22 0x42d072 in main 
    #23 0x7effd607dc4d in __libc_start_main /build/buildd/eglibc-2.11.1/csu/libc-start.c:258
    #24 0x4193d9 in _start 
0x00007effa6e4dd48 is located 72 bytes inside of 384-byte region [0x00007effa6e4dd00,0x00007effa6e4de80)
freed by thread T0 here:
    #1 0x2de0949 in WebCore::RenderSVGShadowTreeRootContainer::~RenderSVGShadowTreeRootContainer() 
    #2 0x2a49c85 in WebCore::RenderObject::arenaDelete(WebCore::RenderArena*, void*) 
    #3 0x172b4fc in WebCore::Node::detach() 
    #4 0x16e45b9 in WebCore::Element::detach() 
    #5 0x2d71a42 in WebCore::SVGUseElement::detach() 
    #6 0x165f689 in WebCore::ContainerNode::detach() 
    #7 0x16e45b9 in WebCore::Element::detach() 
    #8 0x165f689 in WebCore::ContainerNode::detach() 
    #9 0x16e45b9 in WebCore::Element::detach() 
    #10 0x165e269 in WebCore::ContainerNode::removeChildren() 
    #11 0x18156ff in WebCore::replaceChildrenWithFragment(WebCore::HTMLElement*, WTF::PassRefPtr<WebCore::DocumentFragment>, int&) third_party/WebKit/Source/WebCore/html/HTMLElement.cpp:0
    #12 0x1814df0 in WebCore::HTMLElement::setInnerHTML(WTF::String const&, int&) 
    #13 0xadcf03 in WebCore::HTMLElementInternal::innerHTMLAttrSetter(v8::Local<v8::String>, v8::Local<v8::Value>, v8::AccessorInfo const&) out/Release/obj/gen/webkit/bindings/V8DerivedSources15.cpp:0
    #14 0x1255108 in v8::internal::JSObject::SetPropertyWithCallback(v8::internal::Object*, v8::internal::String*, v8::internal::Object*, v8::internal::JSObject*, v8::internal::StrictModeFlag) 
    #15 0x125b3f2 in v8::internal::JSObject::SetPropertyForResult(v8::internal::LookupResult*, v8::internal::String*, v8::internal::Object*, PropertyAttributes, v8::internal::StrictModeFlag) 
previously allocated by thread T0 here:
    #1 0x2de7dd6 in WebCore::SVGShadowTreeRootElement::create(WebCore::Document*, WebCore::SVGUseElement*) 
    #2 0x2de0d38 in WebCore::RenderSVGShadowTreeRootContainer::updateFromElement() 
    #3 0x2d71971 in WebCore::SVGUseElement::attach() 
    #4 0x1a367e9 in WTF::PassRefPtr<WebCore::Element> WebCore::HTMLConstructionSite::attach<WebCore::Element>(WebCore::ContainerNode*, WTF::PassRefPtr<WebCore::Element>) 
    #5 0x1a3bc70 in WebCore::HTMLConstructionSite::insertForeignElement(WebCore::AtomicHTMLToken&, WTF::AtomicString const&) 
    #6 0x19c3b11 in WebCore::HTMLTreeBuilder::processStartTag(WebCore::AtomicHTMLToken&) 
    #7 0x19bdcd4 in WebCore::HTMLTreeBuilder::processToken(WebCore::AtomicHTMLToken&) 
    #8 0x19bd875 in WebCore::HTMLTreeBuilder::constructTreeFromAtomicToken(WebCore::AtomicHTMLToken&) 
    #9 0x19bd710 in WebCore::HTMLTreeBuilder::constructTreeFromToken(WebCore::HTMLToken&) 
    #10 0x19753be in WebCore::HTMLDocumentParser::pumpTokenizer(WebCore::HTMLDocumentParser::SynchronousMode) 
    #11 0x1976f82 in WebCore::HTMLDocumentParser::append(WebCore::SegmentedString const&) 
    #12 0x3bb83e6 in WebCore::DecodedDataDocumentParser::flush(WebCore::DocumentWriter*) 
    #13 0x2273b95 in WebCore::DocumentWriter::endIfNotLoadingMainResource() 
    #14 0x22b2a59 in WebCore::FrameLoader::finishedLoading() 
    #15 0x22d6b60 in WebCore::MainResourceLoader::didFinishLoading(double) 
==19072== ABORTING
Stats: 0M malloced (0M for red zones) by 0 calls
Stats: 1M realloced by 1414 calls
Stats: 0M freed by 0 calls
Stats: 0M really freed by 0 calls
Stats: 0M (0 pages) mmaped in 0 calls
Stats: 26M of shadow memory allocated in 26 clusters
             (1M each, 3 low and 23 high)
Shadow byte and word:
  0x00001fdff4dc9ba9: fb
  0x00001fdff4dc9ba8: fb fb fb fb fb fb fb fb
More shadow bytes:
  0x00001fdff4dc9b88: ff ff ff ff ff ff ff ff
  0x00001fdff4dc9b90: ff ff ff ff ff ff ff ff
  0x00001fdff4dc9b98: ff ff ff ff ff ff ff ff
  0x00001fdff4dc9ba0: fb fb fb fb fb fb fb fb
=>0x00001fdff4dc9ba8: fb fb fb fb fb fb fb fb
  0x00001fdff4dc9bb0: fb fb fb fb fb fb fb fb
  0x00001fdff4dc9bb8: fb fb fb fb fb fb fb fb
  0x00001fdff4dc9bc0: fb fb fb fb fb fb fb fb
  0x00001fdff4dc9bc8: fb fb fb fb fb fb fb fb



### js...@chromium.org (2011-07-27)

Am I misreading, or has this been fixed (the security aspect at least)?

### si...@chromium.org (2011-07-27)

Yeah, and bugs have been filed in WebKit to fix the root cause.

### in...@chromium.org (2011-07-27)

Was this merged to m13, my memory is not sharp ? i think it made the branch point for m14 though.

### si...@chromium.org (2011-07-27)

No, but it shouldn't be in there. I removed the hack on 7/12, which is well after the m13 branch point.

### sc...@gmail.com (2011-07-27)

So M13 is okay? Sounds great :D

### si...@chromium.org (2011-07-27)

Correct.

### sc...@gmail.com (2011-09-02)

I'm kind of confused as to what was fixed when, but @inferno, perhaps it sounds like a rewardable condition for @miaubiz ?

Adding reward-topanel

### in...@chromium.org (2011-09-05)

Chris, this was a brief regression on trunk. It also reproduced on ClusterFuzz, but miaubiz had another interesting modified version of original testcase which helped to fix the underlying parser issue. I think yeah we can consider this one for reward, although this one is just on the border.

### sc...@gmail.com (2011-09-08)

@miaubiz: sounds like you weren't first on this one, but definitely provided a useful testcase different to the one we already had, and this helped get the right fix.
Accordingly, a $500 Chromium Security Reward for general helpfulness.

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

### sc...@gmail.com (2011-09-23)

Payment in system.

### js...@chromium.org (2011-10-05)

Batch update.

### in...@chromium.org (2012-01-11)

[Empty comment from Monorail migration]

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

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/89558?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/89455]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092713)*
