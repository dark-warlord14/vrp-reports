# Heap-use-after-free in WebCore::RenderBlock::determineStartPosition

| Field | Value |
|-------|-------|
| **Issue ID** | [40077857](https://issues.chromium.org/issues/40077857) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Layout |
| **Reporter** | at...@gmail.com |
| **Assignee** | jw...@chromium.org |
| **Created** | 2013-07-30 |
| **Bounty** | $2,000.00 |

## Description


Tested on:

OS: Windows 7 x64

Chrome:   30.0.1569.1 (Official build 212521) canary SyzyASan
Chromium: 30.0.1582.0 (Developer Build 214332) 

I only managed to get SyzyASAN-trace from Chrome Canary which is little outdated. In Chromium I get sad tab but I'm unable to analyse the crash any further atm.

I haven't tried this on ASAN-build yet.

SyzyASAN-trace:

SyzyASAN error: heap-use-after-free on address 0x057CC4AB (stack_id=0x11151836)
READ of size 4 at 0x057CC498
    #0 0x000064ded9c3 in (unknown)
    #1 0x000064e813e7 in (unknown)
    #2 0x000064e7c912 in (unknown)
    #3 0x000064e7fdd4 in (unknown)
    #4 0x000064df483e in (unknown)
    #5 0x000064df3a75 in (unknown)
.
.
.


Analysis from minidump:

Bad access information:
   +0x000 alloc_stack      : [62] 0x0fd24ca8
   +0x0f8 alloc_stack_size : 0x1c ''
   +0x0fc alloc_tid        : 0xfd29b21
   +0x100 free_stack       : [62] 0x0fd24d52
   +0x1f8 free_stack_size  : 0x1c ''
   +0x1fc free_tid         : 2
   +0x200 error_type       : 0 ( UNKNOWN_BAD_ACCESS )
   +0x204 access_mode      : 4 (No matching name)
   +0x208 access_size      : 0x34393430
   +0x20c shadow_info      : [128]  "B21B is 3 bytes inside 60-byte block [0494B218,0494B254)."
   +0x290 microseconds_since_free : 0x10003`00000000

Crash stack:
chrome_dll!WebCore::numberOfIsolateAncestors+0x1c (FPO: [Non-Fpo]) (CONV: cdecl)
chrome_dll!WebCore::RenderBlock::determineStartPosition+0x443 (FPO: [Non-Fpo]) (CONV: thiscall)
chrome_dll!WebCore::RenderBlock::layoutRunsAndFloats+0x3b (FPO: [Non-Fpo]) (CONV: thiscall)
0x23e898

Allocation stack:
chrome_dll!malloc+0x17
chrome_dll!WebCore::Text::createTextRenderer+0xc5
chrome_dll!WebCore::NodeRenderingContext::createRendererForTextIfNeeded+0x15b
chrome_dll!WebCore::Text::attach+0x43
chrome_dll!WebCore::insert+0x125
chrome_dll!WebCore::HTMLConstructionSite::insertTextNode+0x3b3
chrome_dll!WebCore::HTMLTreeBuilder::processCharacterBufferForInBody+0x71
chrome_dll!WebCore::HTMLTreeBuilder::processCharacterBuffer+0x357
chrome_dll!WebCore::HTMLTreeBuilder::processCharacter+0x36
chrome_dll!WebCore::HTMLTreeBuilder::processToken+0x73
chrome_dll!WebCore::HTMLTreeBuilder::constructTree+0x23
chrome_dll!WebCore::HTMLDocumentParser::pumpPendingSpeculations+0x228
chrome_dll!WebCore::HTMLDocumentParser::didReceiveParsedChunkFromBackgroundParser+0x50
chrome_dll!WTF::FunctionWrapper<void (__thiscall WebCore::HTMLDocumentParser::*)(WTF::PassOwnPtr<WebCore::HTMLDocumentParser::ParsedChunk>)>::operator()+0x52
chrome_dll!WTF::BoundFunctionImpl<WTF::FunctionWrapper<void (__thiscall WebCore::HTMLDocumentParser::*)(WTF::PassOwnPtr<WebCore::HTMLDocumentParser::ParsedChunk>)>,void __cdecl(WTF::W
eakPtr<WebCore::HTMLDocumentParser>,WTF::PassOwnPtr<WebCore::HTMLDocumentParser::ParsedChunk>)>::operator()+0x1a
chrome_dll!base::internal::Invoker<1,base::internal::BindState<base::internal::RunnableAdapter<bool (__cdecl*)(void *)>,bool __cdecl(void *),void __cdecl(void *)>,bool __cdecl(void *)
>::Run+0xf
chrome_dll!base::MessageLoop::RunTask+0x1eb
chrome_dll!base::MessageLoop::DoWork+0x2ec
chrome_dll!base::MessagePumpDefault::Run+0xc1
chrome_dll!base::MessageLoop::RunInternal+0x72
chrome_dll!base::RunLoop::Run+0x59
chrome_dll!base::MessageLoop::Run+0x34
chrome_dll!content::RendererMain+0x40e
chrome_dll!content::RunNamedProcessTypeMain+0x58
chrome_dll!content::ContentMainRunnerImpl::Run+0x85
chrome_dll!content::ContentMain+0x29
chrome_dll!ChromeMain+0x1e

Free stack:
chrome_dll!malloc+0x17
chrome_dll!WebCore::Text::createTextRenderer+0xc5
chrome_dll!WebCore::NodeRenderingContext::createRendererForTextIfNeeded+0x15b
chrome_dll!WebCore::Text::attach+0x43
chrome_dll!WebCore::insert+0x125
chrome_dll!WebCore::HTMLConstructionSite::insertTextNode+0x3b3
chrome_dll!WebCore::HTMLTreeBuilder::processCharacterBufferForInBody+0x71
chrome_dll!WebCore::HTMLTreeBuilder::processCharacterBuffer+0x357
chrome_dll!WebCore::HTMLTreeBuilder::processCharacter+0x36
chrome_dll!WebCore::HTMLTreeBuilder::processToken+0x73
chrome_dll!WebCore::HTMLTreeBuilder::constructTree+0x23
chrome_dll!WebCore::HTMLDocumentParser::pumpPendingSpeculations+0x228
chrome_dll!WebCore::HTMLDocumentParser::didReceiveParsedChunkFromBackgroundParser+0x50
chrome_dll!WTF::FunctionWrapper<void (__thiscall WebCore::HTMLDocumentParser::*)(WTF::PassOwnPtr<WebCore::HTMLDocumentParser::ParsedChunk>)>::operator()+0x52
chrome_dll!WTF::BoundFunctionImpl<WTF::FunctionWrapper<void (__thiscall WebCore::HTMLDocumentParser::*)(WTF::PassOwnPtr<WebCore::HTMLDocumentParser::ParsedChunk>)>,void __cdecl(WTF::W
eakPtr<WebCore::HTMLDocumentParser>,WTF::PassOwnPtr<WebCore::HTMLDocumentParser::ParsedChunk>)>::operator()+0x1a
chrome_dll!base::internal::Invoker<1,base::internal::BindState<base::internal::RunnableAdapter<bool (__cdecl*)(void *)>,bool __cdecl(void *),void __cdecl(void *)>,bool __cdecl(void *)
>::Run+0xf
chrome_dll!base::MessageLoop::RunTask+0x1eb
chrome_dll!base::MessageLoop::DoWork+0x2ec
chrome_dll!base::MessagePumpDefault::Run+0xc1
chrome_dll!base::MessageLoop::RunInternal+0x72
chrome_dll!base::RunLoop::Run+0x59
chrome_dll!base::MessageLoop::Run+0x34
chrome_dll!content::RendererMain+0x40e
chrome_dll!content::RunNamedProcessTypeMain+0x58
chrome_dll!content::ContentMainRunnerImpl::Run+0x85
chrome_dll!content::ContentMain+0x29
chrome_dll!ChromeMain+0x1e


## Attachments

- [chrome-heap-use-after-free-9c3.html](attachments/chrome-heap-use-after-free-9c3.html) (text/html; charset=us-ascii, 808 B)
- [minified-repo.html](attachments/minified-repo.html) (text/html; charset=us-ascii, 716 B)

## Timeline

### at...@gmail.com (2013-07-30)

This issue reproduces also with newest pre-built ASAN binary.
Tested on:

OS: Ubuntu 12.04

Chromium: 30.0.1581.0 (Developer Build 214246)

ASAN-trace:

==22439==ERROR: AddressSanitizer: heap-use-after-free on address 0x6080000136a0 at pc 0x7f5fc8a974c7 bp 0x7fffbe73b770 sp 0x7fffbe73b768
READ of size 8 at 0x6080000136a0 thread T0 (chrome)
    #0 0x7f5fc8a974c6 in WebCore::isIsolatedInline(WebCore::RenderObject*) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/rendering/InlineIterator.h:414:0
    #1 0x7f5fc8a819c7 in WebCore::numberOfIsolateAncestors(WebCore::InlineIterator const&) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/rendering/InlineIterator.h:435:13
    #2 0x7f5fc8a7b32a in WebCore::RenderBlock::determineStartPosition(WebCore::LineLayoutState&, WebCore::BidiResolver<WebCore::InlineIterator, WebCore::BidiRun>&) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/rendering/RenderBlockLineLayout.cpp:2163:36
    #3 0x7f5fc8a7a588 in WebCore::RenderBlock::layoutRunsAndFloats(WebCore::LineLayoutState&, bool) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/rendering/RenderBlockLineLayout.cpp:1491:0
    #4 0x7f5fc8a8275e in WebCore::RenderBlock::layoutInlineChildren(bool, WebCore::LayoutUnit&, WebCore::LayoutUnit&) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/rendering/RenderBlockLineLayout.cpp:1997:0
    #5 0x7f5fc89fd1f3 in WebCore::RenderBlock::layoutBlock(bool, WebCore::LayoutUnit) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/rendering/RenderBlock.cpp:1646:0
.
.
.
freed by thread T0 (chrome) here:
    #0 0x7f5fc5e5c295 in __interceptor_free _asan_rtl_
    #1 0x7f5fc80b3c7e in detach /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/dom/Node.cpp:1069
    #2 0x7f5fc7fe62bc in removeBetween /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/dom/ContainerNode.cpp:510
    #3 0x7f5fc7fe5cee in removeChild /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/dom/ContainerNode.cpp:494
    #4 0x7f5fc878d37f in removeChildMethodCustom /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/bindings/v8/custom/V8NodeCustom.cpp:104
    #5 0x7f5fc8665d9c in removeChildMethodCallbackForMainWorld /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/gen/webkit/bindings/V8Node.cpp:671
.
.
.


### cl...@chromium.org (2013-08-01)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6188154117685248

Uploader: jln@chromium.org

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x6080000169a0
Crash State:
  - crash stack -
  WebCore::RenderBlock::determineStartPosition
  WebCore::RenderBlock::layoutRunsAndFloats
  - free stack -
  WebCore::Node::detach
  WebCore::ContainerNode::removeChild
  

Unminimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv95vgsQFOXWVd3yayPhOOjMs9kwcyPvDekWmKpKP3lmWw-4E14U-n9xExRzQMfGIheEWhsvaznYOJtsYKb1amM5o_hIuhMW9Xcvi195FxiKXitNyvOdchxXkg2V_vtYYXkeJGUsnm83Wmvewcc4DnJWYi82YyA



### jl...@chromium.org (2013-08-01)

[Empty comment from Monorail migration]

### jl...@chromium.org (2013-08-01)

[Empty comment from Monorail migration]

### jl...@chromium.org (2013-08-01)

Levi, would you want to give this bug some love ?

### cl...@chromium.org (2013-08-01)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6188154117685248

Uploader: jln@chromium.org

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x60e000027a00
Crash State:
  - crash stack -
  WebCore::RenderBlock::determineStartPosition
  WebCore::RenderBlock::layoutRunsAndFloats
  - free stack -
  WebCore::Node::detach
  WebCore::ContainerNode::removeChild
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=114622:114634

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv97bRRgCEF5isCNZOt3fliAQmRp_nP3sWaoVxroEqrqE8vdYHRVyakscdPp2m7GtEvs1qitCJVGrp1X1v3QE4f9CBLk-BjH-uElav6CWQPIKfO25egPPp0E1_oSr6rkTYypuaO_dXLKfh_qXTWb8qluOlQHevQ



### jl...@chromium.org (2013-08-01)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-08-01)

ClusterFuzz is now working on this testcase. See https://cluster-fuzz.appspot.com/testcase?key=265838

### jl...@chromium.org (2013-08-02)

[Empty comment from Monorail migration]

### ad...@chromium.org (2013-08-02)

[Empty comment from Monorail migration]

### jw...@chromium.org (2013-08-03)

[Empty comment from Monorail migration]

### jw...@chromium.org (2013-08-06)

Slightly more reduced test case attached.

### jw...@chromium.org (2013-08-06)

We believe that the lastBreakObj is stale in the line box tree. Something to do with bidi-isolate.

Much more minified:

<script>
function remove(node)
{
    node.parentNode.removeChild(node);
}

window.onload = function()
{
    document.body.offsetTop;
    remove(e.lastChild);
    document.body.offsetTop;
    remove(z.firstChild);
    document.body.offsetTop;
}
</script>
<body>
  <div><output id="z">f</output></div>
  <div> </div>
  <div>
  <output>
      <output>o</output>
      <span id="e">
          <span><div style="display:inline-block"></div><br><br><br></span>
      </span>
  </output>
  </div>
</body>

### cl...@chromium.org (2013-08-07)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5030331061108736

Uploader: inferno@chromium.org
windows_syzyasan_chrome

Crash Type: Use-after-free READ 4
Crash Address: 0x04c7c1b3
Crash State:
  - crash stack -
  WebCore::numberOfIsolateAncestors
  WebCore::RenderBlock::determineStartPosition
  - free stack -
  WebCore::Text::createTextRenderer
  WebCore::NodeRenderingContext::createRendererForTextIfNeeded
  




### cl...@chromium.org (2013-08-08)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5030331061108736

Uploader: inferno@chromium.org
Job Type: Windows_syzyasan_chrome

Crash Type: Use-after-free READ 4
Crash Address: 0x03dd056b
Crash State:
  - crash stack -
  WebCore::numberOfIsolateAncestors
  WebCore::RenderBlock::determineStartPosition
  - free stack -
  WebCore::Text::createTextRenderer
  WebCore::NodeRenderingContext::createRendererForTextIfNeeded
  

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv97uYqyleWUxES8wfdOoT6FeZf3Fr-jEhKg6C7StGHTZ6rXoOEXCkPIukHzbaTHQ9bEDdGm6COFhUQS_G1NDvy_S8zkB_kuU0jqRjshkw1zrnAnEpP8jtFrZxT4Md_6rmAD_tzRVuoHcRrFDYq9hjlx8te8M0g



### jw...@chromium.org (2013-08-09)

Confirmed that the last->lineBreakObj() is stale in RenderBlock::determineStartPosition. Member access to lineBreakObj in determineStartPosition also cause use-after-free error.

Also, *slightly* more minified:

<script>
function remove(node)
{
    node.parentNode.removeChild(node);
}

window.onload = function()
{
    document.body.offsetTop;
    remove(b.lastChild);
    document.body.offsetTop;
    remove(a.firstChild);
    document.body.offsetTop;
}
</script>

<body>
  <div id="a">a</div>
  <div></div>
  <div>
    <output>
        <output>b</output>
        <span id="b">
            <span><div style="display:inline-block"></div><br><br><br></span>
        </span>
    </output>
  </div>
</body>

### jw...@chromium.org (2013-08-09)

In RenderBlock::determineStartPosition, forced layoutStateisFullLayout() path for full tree re-render, which eliminated the use-after-free. Suggests that determineStartPosition is returning incorrect position on previous layout recalc? I'm going to explore that possibility.

### cl...@chromium.org (2013-08-09)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5030331061108736

Uploader: inferno@chromium.org
Job Type: Windows_syzyasan_chrome

Crash Type: Use-after-free READ 4
Crash Address: 0x0520b64b
Crash State:
  - crash stack -
  WebCore::numberOfIsolateAncestors
  WebCore::RenderBlock::determineStartPosition
  - free stack -
  WebCore::RenderWordBreak::`scalar deleting destructor'
  WebCore::RenderObject::postDestroy
  

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv94GE2crL9EeI6-4kBCyPEEt5-anwOzT3IkiqwFtwBX3SZGlsHghe8GPlmey4suk3dLltqvEo0I3yKJQx-etvcDsCgxTcW1rI4k5nnWeVX2PanbgN4F1cbQsmf0e_cSSA6x30FETPsA2srvdob6fuPZHYqXJkQ



### cl...@chromium.org (2013-08-09)

ClusterFuzz has detected this issue as fixed in latest custom build.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5030331061108736

Uploader: inferno@chromium.org
Job Type: Windows_syzyasan_chrome

Crash Type: Use-after-free READ 4
Crash Address: 0x0520b64b
Crash State:
  - crash stack -
  WebCore::numberOfIsolateAncestors
  WebCore::RenderBlock::determineStartPosition
  - free stack -
  WebCore::RenderWordBreak::`scalar deleting destructor'
  WebCore::RenderObject::postDestroy
  

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv94GE2crL9EeI6-4kBCyPEEt5-anwOzT3IkiqwFtwBX3SZGlsHghe8GPlmey4suk3dLltqvEo0I3yKJQx-etvcDsCgxTcW1rI4k5nnWeVX2PanbgN4F1cbQsmf0e_cSSA6x30FETPsA2srvdob6fuPZHYqXJkQ

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### in...@chromium.org (2013-08-09)

ignore last comment, i was testing something with syzyasan and broke logic.

### cl...@chromium.org (2013-08-13)

ClusterFuzz has detected this issue as fixed in latest custom build.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5030331061108736

Uploader: inferno@chromium.org
Job Type: Windows_syzyasan_chrome

Crash Type: Use-after-free READ 4
Crash Address: 0x0520b64b
Crash State:
  - crash stack -
  WebCore::numberOfIsolateAncestors
  WebCore::RenderBlock::determineStartPosition
  - free stack -
  WebCore::RenderWordBreak::`scalar deleting destructor'
  WebCore::RenderObject::postDestroy
  

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv94GE2crL9EeI6-4kBCyPEEt5-anwOzT3IkiqwFtwBX3SZGlsHghe8GPlmey4suk3dLltqvEo0I3yKJQx-etvcDsCgxTcW1rI4k5nnWeVX2PanbgN4F1cbQsmf0e_cSSA6x30FETPsA2srvdob6fuPZHYqXJkQ

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### cl...@chromium.org (2013-08-13)

ClusterFuzz has detected this issue as fixed in latest custom build.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5030331061108736

Uploader: inferno@chromium.org
Job Type: Windows_syzyasan_chrome

Crash Type: Use-after-free READ 4
Crash Address: 0x0520b64b
Crash State:
  - crash stack -
  WebCore::numberOfIsolateAncestors
  WebCore::RenderBlock::determineStartPosition
  - free stack -
  WebCore::RenderWordBreak::`scalar deleting destructor'
  WebCore::RenderObject::postDestroy
  

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv94GE2crL9EeI6-4kBCyPEEt5-anwOzT3IkiqwFtwBX3SZGlsHghe8GPlmey4suk3dLltqvEo0I3yKJQx-etvcDsCgxTcW1rI4k5nnWeVX2PanbgN4F1cbQsmf0e_cSSA6x30FETPsA2srvdob6fuPZHYqXJkQ

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### jw...@chromium.org (2013-08-15)

Some updates on what we've seen so far. Here is a test case that *does not* fail, but should have virtually the same internal Render Tree and basic behavior as the failing case:
<script>
function remove(node)
{
    node.parentNode.removeChild(node);
}

window.onload = function()
{
    document.body.offsetTop;
    remove(b.lastChild);
    document.body.offsetTop;
    remove(a.firstChild);
    document.body.offsetTop;
}
</script>

<body>
  <div id="a">a</div>
  <div></div>
  <div>
    <span>
        <output>b</output>
        <span id="b">
            <span><div style="display:inline-block"></div><br><br><br></span>
        </span>
    </span>
  </div>
</body>

In debugging this, we've noted that at a certain point, the failing has an inline without an inlineBoxWrapper while the good case has an inlineBoxWrapper. Looking back further, this seems to diverge during a call to createLineBoxesFromBidiRuns where they're at the same place in the Render Tree, but the good case has a firstRun of its bidi runs pointing at a RenderText (first child of the OUTPUT RenderInline), while the bad case points to the third RenderBR of the last SPAN.

At this point, I'm trying to find out how that BidiRun divergence occurs.

### jw...@chromium.org (2013-08-15)

Just as a clarification, at the point that the firstRun() for the two versions point to different RenderObjects, I have confirmed that, indeed, the lineBox points to the same line in the Render Tree, namely the DIV surrounding the SPAN/OUTPUT (respectively for the two cases).

### cl...@chromium.org (2013-08-21)

ClusterFuzz has detected this issue as fixed in latest custom build.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5030331061108736

Uploader: inferno@chromium.org
Job Type: Windows_syzyasan_chrome

Crash Type: Use-after-free READ 4
Crash Address: 0x0520b64b
Crash State:
  - crash stack -
  WebCore::numberOfIsolateAncestors
  WebCore::RenderBlock::determineStartPosition
  - free stack -
  WebCore::RenderWordBreak::`scalar deleting destructor'
  WebCore::RenderObject::postDestroy
  

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv94GE2crL9EeI6-4kBCyPEEt5-anwOzT3IkiqwFtwBX3SZGlsHghe8GPlmey4suk3dLltqvEo0I3yKJQx-etvcDsCgxTcW1rI4k5nnWeVX2PanbgN4F1cbQsmf0e_cSSA6x30FETPsA2srvdob6fuPZHYqXJkQ

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### le...@chromium.org (2013-08-21)

Fixed!? Say it's so!

### jw...@chromium.org (2013-08-21)

I just ran our test locally and it seems like the use-after-free is, indeed, gone. I still need to verify that the actual bug is gone and not just the symptom.

### [Deleted User] (2013-08-21)

Was this from the samsung guy making isolate changes recently?  Or did we fix this directly?

### in...@chromium.org (2013-08-21)

We don't have fixed/regression ranges for windows bots yet. So, i clicked redo on the linux report - https://cluster-fuzz.appspot.com/testcase?key=6188154117685248. let see what CF says.


### cl...@chromium.org (2013-08-21)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6188154117685248

Uploader: jln@chromium.org
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x60e000027a00
Crash State:
  - crash stack -
  WebCore::RenderBlock::determineStartPosition
  WebCore::RenderBlock::layoutRunsAndFloats
  - free stack -
  WebCore::Node::detach
  WebCore::ContainerNode::removeChild
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=114622:114634

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv97bRRgCEF5isCNZOt3fliAQmRp_nP3sWaoVxroEqrqE8vdYHRVyakscdPp2m7GtEvs1qitCJVGrp1X1v3QE4f9CBLk-BjH-uElav6CWQPIKfO25egPPp0E1_oSr6rkTYypuaO_dXLKfh_qXTWb8qluOlQHevQ

Fully reproducible crash found using linux_tsan_chrome_mp job type (history_size=6).


### cl...@chromium.org (2013-08-21)

ClusterFuzz has detected this issue as fixed in range 218200:218201.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6188154117685248

Uploader: jln@chromium.org
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x60e000027a00
Crash State:
  - crash stack -
  WebCore::RenderBlock::determineStartPosition
  WebCore::RenderBlock::layoutRunsAndFloats
  - free stack -
  WebCore::Node::detach
  WebCore::ContainerNode::removeChild
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=114622:114634
Fixed: https://cluster-fuzz.appspot.com/revisions?range=218200:218201

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv97bRRgCEF5isCNZOt3fliAQmRp_nP3sWaoVxroEqrqE8vdYHRVyakscdPp2m7GtEvs1qitCJVGrp1X1v3QE4f9CBLk-BjH-uElav6CWQPIKfO25egPPp0E1_oSr6rkTYypuaO_dXLKfh_qXTWb8qluOlQHevQ

Fully reproducible crash found using linux_tsan_chrome_mp job type (history_size=6).

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### in...@chromium.org (2013-08-21)

Fixed by http://src.chromium.org/viewvc/blink?view=rev&revision=156261

### jw...@chromium.org (2013-08-21)

eseidel@, yes, igor's fix was the solution. leviw and I realized that this morning. oh, well, there goes my last week and a half :-P

### jw...@chromium.org (2013-08-21)

[Empty comment from Monorail migration]

### [Deleted User] (2013-08-21)

Seems like we should still land the test case.  Feel free to TBR=me.

### jw...@chromium.org (2013-08-21)

Yup, that's the plan. Will do in a bit.

### in...@chromium.org (2013-08-22)

It has to duplicated the way around, also makes it easier to handle rewards.

### in...@chromium.org (2013-08-22)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-08-22)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=156580

------------------------------------------------------------------------
r156580 | jww@chromium.org | 2013-08-22T21:25:59.416473Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/text/international/unicode-bidi-isolate-nested-with-removes-expected.txt?r1=156580&r2=156579&pathrev=156580
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/text/international/unicode-bidi-isolate-nested-with-removes.html?r1=156580&r2=156579&pathrev=156580

Added LayoutTest for use-after-free regression with bidi isolates.

BUG=265838

Review URL: https://chromiumcodereview.appspot.com/23137012
------------------------------------------------------------------------

### in...@chromium.org (2013-09-12)

Please merge your change to the m30 branch (1599) by early next week [using drover]. We have m30 beta coming next week and we want all the security changes in by that time. 

### in...@chromium.org (2013-09-13)

merged to 1599 in r157784.

### la...@google.com (2013-09-13)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-09-16)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-09-25)

Did you saw our new criteria for possibly issuing higher rewards? See http://www.chromium.org/Home/chromium-security/vulnerability-rewards-program/reward-nomination-process
E.g. If you are able to provide a repro that faulted at an address of 0x41414141, it will qualify for the new higher rewards. Or, if you can show that you have control between free and crash points, etc.

### mb...@chromium.org (2013-09-26)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-09-28)

$2000 under the new reward rules! Bumped up because it looks like JS runs between the free and the use. (Could have been $3000 but the use is inside one of our heap partitions).

### pa...@chromium.org (2013-10-18)

Payment sent out on this one too.

### cl...@chromium.org (2014-02-06)

Bulk update: removing view restriction from closed bugs.

### ti...@chromium.org (2014-02-28)

[Empty comment from Monorail migration]

### la...@google.com (2015-01-09)

Migrate from Cr-Blink-Rendering to Cr-Blink-Layout

### gl...@chromium.org (2015-06-29)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-02-02)

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

### sh...@chromium.org (2018-07-29)

[Empty comment from Monorail migration]

### is...@google.com (2018-07-29)

This issue was migrated from crbug.com/chromium/265838?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/274717]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40077857)*
