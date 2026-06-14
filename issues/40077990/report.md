# Heap-use-after-free in WebCore::RenderBlock::determineStartPosition

| Field | Value |
|-------|-------|
| **Issue ID** | [40077990](https://issues.chromium.org/issues/40077990) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Reporter** | at...@gmail.com |
| **Assignee** | jw...@chromium.org |
| **Created** | 2013-08-26 |
| **Bounty** | $2,000.00 |

## Description


Tested on:

OS: Ubuntu 12.04
Chromium: ASAN 31.0.1612.0 (Developer Build 219526)

I think this issue is related to https://crbug.com/chromium/265838, at least the stack trace looks similar.

Repro-file as attachment

ASAN-report:

==5017==ERROR: AddressSanitizer: heap-use-after-free on address 0x608000015da0 at pc 0x7fe2dc9dfb97 bp 0x7fff82c21410 sp 0x7fff82c21408
READ of size 8 at 0x608000015da0 thread T0 (chrome)
    #0 0x7fe2dc9dfb96 in WebCore::isIsolatedInline(WebCore::RenderObject*) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/rendering/InlineIterator.h:414:0
    #1 0x7fe2dc9cb1c7 in WebCore::numberOfIsolateAncestors(WebCore::InlineIterator const&) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/rendering/InlineIterator.h:440:13
    #2 0x7fe2dc9c2adc in WebCore::RenderBlock::determineStartPosition(WebCore::LineLayoutState&, WebCore::BidiResolver<WebCore::InlineIterator, WebCore::BidiRun>&) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/rendering/RenderBlockLineLayout.cpp:2338:36
    #3 0x7fe2dc9c1d68 in WebCore::RenderBlock::layoutRunsAndFloats(WebCore::LineLayoutState&, bool) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/rendering/RenderBlockLineLayout.cpp:1549:0
    #4 0x7fe2dc9cbf2e in WebCore::RenderBlock::layoutInlineChildren(bool, WebCore::LayoutUnit&, WebCore::LayoutUnit&) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/rendering/RenderBlockLineLayout.cpp:2173:0
    #5 0x7fe2dc9501dd in WebCore::RenderBlock::layoutBlock(bool, WebCore::LayoutUnit) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/rendering/RenderBlock.cpp:1596:0
.
.
.
0x608000015da0 is located 0 bytes inside of 96-byte region [0x608000015da0,0x608000015e00)
freed by thread T0 (chrome) here:
    #0 0x7fe2d59672c5 in __interceptor_free _asan_rtl_
    #1 0x7fe2dc04a6ee in detach /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/dom/Node.cpp:1127
    #2 0x7fe2dbf6235c in removeBetween /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/dom/ContainerNode.cpp:508
    #3 0x7fe2dbf61d32 in removeChild /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/dom/ContainerNode.cpp:492
    #4 0x7fe2dc047087 in removeChild /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/dom/Node.cpp:537
    #5 0x7fe2dc6da179 in removeChildMethodCustom /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/bindings/v8/custom/V8NodeCustom.cpp:104
    #6 0x7fe2dc5b3e4c in removeChildMethodCallbackForMainWorld /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/gen/blink/bindings/V8Node.cpp:684
.
.
.


## Attachments

- [chrome-heap-use-after-free-WebCoreisIsolatedInline10.html](attachments/chrome-heap-use-after-free-WebCoreisIsolatedInline10.html) (text/html; charset=us-ascii, 767 B)

## Timeline

### in...@chromium.org (2013-08-26)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-08-26)

ClusterFuzz is now working on this testcase. See https://cluster-fuzz.appspot.com/testcase?key=4773916883025920

### ts...@chromium.org (2013-08-26)

Assigning to @jww on the basis of similarity to https://code.google.com/p/chromium/issues/detail?id=265838.  I think CF just kicked out the same (similar?) testcase to what we believe fixed in the refernced bug :(.

### jw...@chromium.org (2013-08-26)

This looks like a variant of 265838. It's not exactly the same thing, but it definitely is crashing, and is almost certainly related. I'll get to work on it.

### jw...@chromium.org (2013-08-26)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-08-26)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4773916883025920

Uploader: tsepez@chromium.org
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x60e0000252a0
Crash State:
  - crash stack -
  WebCore::RenderBlock::determineStartPosition
  WebCore::RenderBlock::layoutRunsAndFloats
  - free stack -
  WebCore::Node::detach
  WebCore::ContainerNode::removeChild
  

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv97C0YrrbQxULz73h7bBXELA_mhOaexop0fEILuDFXuuid-P12czcDlJn4PWrRTkC0bNXBFfdESFgyCMY97Swzzxj4iDrDDWSX3kUMMZn9O3h5RMNXAr9KagbWNMbR2VaHk_h1jzTeDUYdy4l3bVkv9JaNpKkw



### cl...@chromium.org (2013-08-27)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4773916883025920

Uploader: tsepez@chromium.org
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x60e0000252a0
Crash State:
  - crash stack -
  WebCore::RenderBlock::determineStartPosition
  WebCore::RenderBlock::layoutRunsAndFloats
  - free stack -
  WebCore::Node::detach
  WebCore::ContainerNode::removeChild
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=114622:114634

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv97C0YrrbQxULz73h7bBXELA_mhOaexop0fEILuDFXuuid-P12czcDlJn4PWrRTkC0bNXBFfdESFgyCMY97Swzzxj4iDrDDWSX3kUMMZn9O3h5RMNXAr9KagbWNMbR2VaHk_h1jzTeDUYdy4l3bVkv9JaNpKkw



### jw...@chromium.org (2013-08-27)

Here is a minimized testcase:

<script>
  function remove(node)
  {
      console.log('removing');
      node.parentNode.removeChild(node);
  }

  window.onload = function() {
      document.body.offsetTop;
      remove(b.lastChild);
      document.body.offsetTop;
      remove(a.nextSibling);
      document.body.offsetTop;
  }
</script>

<body>
  <output>
    <span>
      <div id="a">a</div>b<div></div>
      <output>c</output>
      <span id="b">
        <span>
          <div style="display:inline-block"></div>
          <br><br>
        </span>
      </span>
    </span>
  </output>
</body>

### jw...@chromium.org (2013-08-27)

Ah, just to clarify, that console.log in the minimized testcase is completely unnecessary (that was just from my debugging). So here's the real minimized testcase:

<script>
  function remove(node)
  {
      node.parentNode.removeChild(node);
  }

  window.onload = function() {
      document.body.offsetTop;
      remove(b.lastChild);
      document.body.offsetTop;
      remove(a.nextSibling);
      document.body.offsetTop;
  }
</script>

<body>
  <output>
    <span>
      <div id="a">a</div>b<div></div>
      <output>c</output>
      <span id="b">
        <span>
          <div style="display:inline-block"></div>
          <br><br>
        </span>
      </span>
    </span>
  </output>
</body>

### jw...@chromium.org (2013-08-28)

One more time. Here's a minified repro that eliminates all anonymous render blocks:

<script>
  function remove(node)
  {
      node.parentNode.removeChild(node);
  }

  window.onload = function() {
      document.body.offsetTop;
      remove(b.lastChild);
      document.body.offsetTop;
      remove(a.nextSibling);
      document.body.offsetTop;
  }
</script>

<body>
  <div id="a">a</div><div>b</div><div></div>
  <div>
    <output>
      <span>
        <output>c</output>
        <span id="b">
          <span>
            <div style="display:inline-block"></div>
            <br><br>
          </span>
        </span>
      </span>
    </output>
  </div>
</body>

### in...@chromium.org (2013-09-03)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-09-03)

Fix labels.

### in...@chromium.org (2013-09-03)

[Empty comment from Monorail migration]

### jw...@chromium.org (2013-09-04)

So I just confirmed what the problem was. Basically, igor's previous fix for nested isolates fails in the case that there is RenderObject between the two isolates (in the repro above, we have a span between the two outputs).

In particular, in igor's containingIsolate implementation, it would go up the tree until it found the first isolate that didn't have an isolate immediately following it. This is a problem in this repro because we have to get up the top isolate from the "c" text, which requires getting by the <span>.

Thus, the solution seems to be to just go to the last isolate we can find before getting to the current root. I have a CL uploaded now to make this change.

### bu...@chromium.org (2013-09-05)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=157268

------------------------------------------------------------------------
r157268 | jww@chromium.org | 2013-09-05T03:54:10.778047Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/text/international/unicode-bidi-isolate-nested-with-removes-not-adjacent-expected.txt?r1=157268&r2=157267&pathrev=157268
   M http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/text/international/unicode-bidi-isolate-nested-with-removes.html?r1=157268&r2=157267&pathrev=157268
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/text/international/unicode-bidi-isolate-nested-with-removes-not-adjacent.html?r1=157268&r2=157267&pathrev=157268
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/rendering/InlineIterator.h?r1=157268&r2=157267&pathrev=157268
   M http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/text/international/unicode-bidi-isolate-nested-with-removes-expected.txt?r1=157268&r2=157267&pathrev=157268
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/rendering/RenderBlockLineLayout.cpp?r1=157268&r2=157267&pathrev=157268

Update containtingIsolate to go back all the way to top isolate from current root, rather than stopping at the first isolate it finds. This works because the current root is always updated with each isolate run.

BUG=279277

Review URL: https://chromiumcodereview.appspot.com/23972003
------------------------------------------------------------------------

### le...@chromium.org (2013-09-06)

This is fixed, right?

### in...@chromium.org (2013-09-06)

yes Sir!

### cl...@chromium.org (2013-09-06)

ClusterFuzz has detected this issue as fixed in range 221446:221565.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4773916883025920

Uploader: tsepez@chromium.org
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x60e0000252a0
Crash State:
  - crash stack -
  WebCore::RenderBlock::determineStartPosition
  WebCore::RenderBlock::layoutRunsAndFloats
  - free stack -
  WebCore::Node::detach
  WebCore::ContainerNode::removeChild
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=114622:114634
Fixed: https://cluster-fuzz.appspot.com/revisions?range=221446:221565

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv97C0YrrbQxULz73h7bBXELA_mhOaexop0fEILuDFXuuid-P12czcDlJn4PWrRTkC0bNXBFfdESFgyCMY97Swzzxj4iDrDDWSX3kUMMZn9O3h5RMNXAr9KagbWNMbR2VaHk_h1jzTeDUYdy4l3bVkv9JaNpKkw

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### in...@chromium.org (2013-09-12)

Please merge your change to the m30 branch (1599) by early next week [using drover]. We have m30 beta coming next week and we want all the security changes in by that time. 

### in...@chromium.org (2013-09-13)

merged to 1599 in r157785.

### bu...@chromium.org (2013-09-13)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=157785

------------------------------------------------------------------------
r157785 | inferno@chromium.org | 2013-09-13T20:58:05.509554Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/branches/chromium/1599/Source/core/rendering/InlineIterator.h?r1=157785&r2=157784&pathrev=157785
   M http://src.chromium.org/viewvc/blink/branches/chromium/1599/Source/core/rendering/RenderBlockLineLayout.cpp?r1=157785&r2=157784&pathrev=157785

Merge 157268 "Update containtingIsolate to go back all the way t..."

> Update containtingIsolate to go back all the way to top isolate from current root, rather than stopping at the first isolate it finds. This works because the current root is always updated with each isolate run.
> 
> BUG=279277
> 
> Review URL: https://chromiumcodereview.appspot.com/23972003

TBR=jww@chromium.org

Review URL: https://codereview.chromium.org/23995017
------------------------------------------------------------------------

### in...@chromium.org (2013-09-16)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-09-25)

Did you saw our new criteria for possibly issuing higher rewards? See http://www.chromium.org/Home/chromium-security/vulnerability-rewards-program/reward-nomination-process
E.g. If you are able to provide a repro that faulted at an address of 0x41414141, it will qualify for the new higher rewards. Or, if you can show that you have control between free and crash points, etc.

### mb...@chromium.org (2013-09-26)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-09-28)

$2000! Looks like JS runs between free and use. Possibly mitigated by partitioning.

### pa...@chromium.org (2013-10-18)

Ok, payment initiated, so expect something in a few weeks. Thanks again for your help Attekett!

### cl...@chromium.org (2014-02-06)

Bulk update: removing view restriction from closed bugs.

### ti...@chromium.org (2014-02-28)

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

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/279277?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40077990)*
