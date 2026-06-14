# Heap-use-after-free in WebCore::CanvasRenderingContext2D::setFont

| Field | Value |
|-------|-------|
| **Issue ID** | [40076322](https://issues.chromium.org/issues/40076322) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | at...@gmail.com |
| **Assignee** | ju...@chromium.org |
| **Created** | 2012-09-20 |
| **Bounty** | $1,000.00 |

## Description


Tested on ASAN Chromium 24.0.1273.0

Repro-file:

<html><body>
<canvas id="test"></canvas>
</body>
<script>
var canvas=document.getElementById("test");
var ctx=canvas.getContext("2d")
for(x=0;x<100;x++){
	ctx.restore()
	ctx.save()
	ctx.save()
	ctx.measureText("a",0,0,0);
}
</script></html>

ASAN-report:

==7897== ERROR: AddressSanitizer heap-use-after-free on address 0x7fab33b6bec0 at pc 0x7fab4789f3da bp 0x7fff696d9ef0 sp 0x7fff696d9ee8
READ of size 8 at 0x7fab33b6bec0 thread T0
    #0 0x7fab4789f3d9 in WebCore::CanvasRenderingContext2D::setFont(WTF::String const&) ???:0
    #1 0x7fab478a193a in WebCore::CanvasRenderingContext2D::measureText(WTF::String const&) ???:0
    #2 0x7fab44b25a34 in WebCore::CanvasRenderingContext2DV8Internal::measureTextCallback(v8::Arguments const&) gen/webkit/bindings/V8DerivedSources17.cpp:0
    #3 0xed3f3c3deb6 in  
    #4 0xed3f3c3d387 in  
    #5 0xed3f3c24006 in  
.
.
.
freed by thread T0 here:
    #0 0x7fab48b0ad80 in __interceptor_free ??:0
    #1 0x7fab478a3a80 in void WTF::Vector<WebCore::CanvasRenderingContext2D::State, 1ul>::appendSlowCase<WebCore::CanvasRenderingContext2D::State>(WebCore::CanvasRenderingContext2D::State const&) ???:0
    #2 0x7fab4787fbf0 in WebCore::CanvasRenderingContext2D::realizeSavesLoop() ???:0
    #3 0x7fab4789e05c in WebCore::CanvasRenderingContext2D::setFont(WTF::String const&) ???:0
    #4 0x7fab478a193a in WebCore::CanvasRenderingContext2D::measureText(WTF::String const&) ???:0
    #5 0x7fab44b25a34 in WebCore::CanvasRenderingContext2DV8Internal::measureTextCallback(v8::Arguments const&) gen/webkit/bindings/V8DerivedSources17.cpp:0
.
.
.



## Timeline

### sc...@gmail.com (2012-09-21)

I suspect this might be a duplicate of 148637, but it's hard to tell without knowing what revision of Chromium you built at.

There was a significant Skia object lifetime regression and we had all sorts of valgrind / crash bugs etc. Root https://crbug.com/chromium/148637

Feel free to re-open if you think you have something different.

### at...@gmail.com (2012-09-21)

@scarybeasts: I used Chromium 24.0.1273.0 (Developer Build 157742), I can check on this when the https://crbug.com/chromium/148637 is fixed.

### in...@chromium.org (2012-09-21)

This still reproduces on trunk, so might not be a duplicate. CF report coming - https://cluster-fuzz.appspot.com/testcase?key=113231645

### in...@chromium.org (2012-09-21)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=113231645

Uploader: inferno@chromium.org

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x7f05936d6ec0
Crash State:
  - crash stack -
  WebCore::CanvasRenderingContext2D::setFont
  WebCore::CanvasRenderingContext2D::measureText
  - free stack -
  void WTF::Vector<WebCore::CanvasRenderingContext2D::State, 1ul>::appendSlowCase<WebCore::CanvasRende
  WebCore::CanvasRenderingContext2D::realizeSavesLoop
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=150627:150709

Minimized Testcase (0.20 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv96b-UuA_4L7W3bEIdZLtKsZ8CQqOWAUZQfM8Ei0glZKuk4a1XVO0NI5EY5QX2-0a7Vr--1iFPXUzYram6TMoIQd8-kbXOH337Tsoc_0UNRMUm4aEMMwQkpXBGon_dbyPixZCXgZTrSMNDX1CcsA83vDkNYYSuH9rdnhmX1F1NqsniBOezE
<canvas id="test"><script>
var canvas=document.getElementById("test");
var ctx=canvas.getContext("2d")
for(x=0;x<100;x++){
	ctx.restore()
	ctx.save()
	ctx.save()
	ctx.measureText("a",0,0,0);
}
</script>

### in...@chromium.org (2012-09-21)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-09-24)

@inferno: I'm confused as to why the ClusterFuzz report says this impacts stable/beta, yet the regression ranges are after M22 branched.

Is it possible we merged a faulty patch?

### in...@chromium.org (2012-09-24)

verified that beta m22 build crashes with same stack, now looking why regression range was wrong.

### in...@chromium.org (2012-09-24)

OK Security Team, here is the reason for wrong regression range, we had clang problems around r145022-149286 and r149313-r150647 [r149286 we reverte. at these points ASAN was completely broken on gprecise. I don't see a way to fix this problem. If ignore those builds (like delete them which is a too many), the regression range will be too big to tell anything useful. If we keep those builds as it is, we will still get the wrong regression range. This kind of problem shouldn't happen in future. Primary reason was we were on 10.04 for a long time and we recently migrated for ubuntu 12 for several reasons. Otherwise, we would have caught this issue much earlier and just had kept the clang roll reverted. Sorry for the triage problem, however we should still rely on the impacts label as it should still be correct (i got the beta builds fixed in https://src.chromium.org/viewvc/chrome?view=rev&revision=157718)

### [Deleted User] (2012-09-26)

Filed upstream as https://bugs.webkit.org/show_bug.cgi?id=97714

### in...@chromium.org (2012-10-16)

Mike, can you please help to triage.

### in...@chromium.org (2012-10-22)

[Empty comment from Monorail migration]

### [Deleted User] (2012-10-22)

I will take a look, but this crash is in webkit code, and not in skia at all. There may be others that understand this code more than I.

### in...@chromium.org (2012-10-22)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-10-23)

Upstreamed - https://bugs.webkit.org/show_bug.cgi?id=100148

### [Deleted User] (2012-10-25)

juno and blanco, this seems to crash in webkit and not skia. Do you know who is familiar with this code?

### in...@chromium.org (2012-11-29)

Moving all milestone 22 bugs to milestone 23

### in...@chromium.org (2012-11-30)

Juno, Blanco, friendly ping! This is a sec-high severity bug and hasn't got any update in the last month. Can you please help with an owner.

### in...@chromium.org (2012-12-05)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-12-12)

The bug is here 

    // The parse succeeded.
    realizeSaves();
    modifiableState().m_unparsedFont = newFont;

realizeSaves deletes the newFont, which is passed as a reference in the function argument. I tried to change to a pass by value, but i get a weird test failure in canvas-test.html layouttest which i have no clue about. Any idea why all these strings are passed as references in this code.

freed by thread T0 here:
    #0 0x7f49666f8350 in __interceptor_free 
    #1 0x7f4927c930fc in WTF::fastFree(void*) third_party/WebKit/Source/WTF/wtf/FastMalloc.cpp:330
    #2 0x7f4929c71722 in WTF::VectorBufferBase<WebCore::CanvasRenderingContext2D::State>::deallocateBuffer(WebCore::CanvasRenderingContext2D::State*) third_party/WebKit/Source/WTF/wtf/Vector.h:314
    #3 0x7f4929c7133c in WTF::VectorBuffer<WebCore::CanvasRenderingContext2D::State, 1ul>::deallocateBuffer(WebCore::CanvasRenderingContext2D::State*) third_party/WebKit/Source/WTF/wtf/Vector.h:448
    #4 0x7f4929c70c28 in WTF::Vector<WebCore::CanvasRenderingContext2D::State, 1ul>::reserveCapacity(unsigned long) third_party/WebKit/Source/WTF/wtf/Vector.h:966
    #5 0x7f4929c70849 in WTF::Vector<WebCore::CanvasRenderingContext2D::State, 1ul>::expandCapacity(unsigned long) third_party/WebKit/Source/WTF/wtf/Vector.h:880
    #6 0x7f4929c704be in WTF::Vector<WebCore::CanvasRenderingContext2D::State, 1ul>::expandCapacity(unsigned long, WebCore::CanvasRenderingContext2D::State const*) third_party/WebKit/Source/WTF/wtf/Vector.h:891
    #7 0x7f4929c6ff85 in void WTF::Vector<WebCore::CanvasRenderingContext2D::State, 1ul>::appendSlowCase<WebCore::CanvasRenderingContext2D::State>(WebCore::CanvasRenderingContext2D::State const&) third_party/WebKit/Source/WTF/wtf/Vector.h:1077
    #8 0x7f4929c5b4b5 in void WTF::Vector<WebCore::CanvasRenderingContext2D::State, 1ul>::append<WebCore::CanvasRenderingContext2D::State>(WebCore::CanvasRenderingContext2D::State const&) third_party/WebKit/Source/WTF/wtf/Vector.h:1068
    #9 0x7f4929c1a785 in WebCore::CanvasRenderingContext2D::realizeSavesLoop() third_party/WebKit/Source/WebCore/html/canvas/CanvasRenderingContext2D.cpp:280

Juno, can you please help to take a look.

### in...@chromium.org (2013-01-05)

Junov@, please note that this is a high severity security bug. If you can't take it, please help with an owner or respond here.

### ju...@chromium.org (2013-01-07)

Taking a look now...

### ju...@chromium.org (2013-01-07)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-01-07)

[Empty comment from Monorail migration]

### ju...@chromium.org (2013-01-08)

Merged.

M25: http://trac.webkit.org/changeset/139059
M24: http://trac.webkit.org/changeset/139058
M23: http://trac.webkit.org/changeset/139057

### in...@chromium.org (2013-01-08)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-01-09)

ClusterFuzz has detected this issue as fixed in range 175484:175517.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=113231645

Uploader: inferno@chromium.org

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x7f05936d6ec0
Crash State:
  - crash stack -
  WebCore::CanvasRenderingContext2D::setFont
  WebCore::CanvasRenderingContext2D::measureText
  - free stack -
  void WTF::Vector<WebCore::CanvasRenderingContext2D::State, 1ul>::appendSlowCase<WebCore::CanvasRende
  WebCore::CanvasRenderingContext2D::realizeSavesLoop
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=150627:150709
Fixed: https://cluster-fuzz.appspot.com/revisions?range=175484:175517

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv96b-UuA_4L7W3bEIdZLtKsZ8CQqOWAUZQfM8Ei0glZKuk4a1XVO0NI5EY5QX2-0a7Vr--1iFPXUzYram6TMoIQd8-kbXOH337Tsoc_0UNRMUm4aEMMwQkpXBGon_dbyPixZCXgZTrSMNDX1CcsA83vDkNYYSuH9rdnhmX1F1NqsniBOezE

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### sc...@gmail.com (2013-01-17)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-01-21)

@attekett: $1000, never stop rocking!

### sc...@gmail.com (2013-01-21)

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

### bu...@chromium.org (2013-04-01)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-05)

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

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/151008?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40076322)*
