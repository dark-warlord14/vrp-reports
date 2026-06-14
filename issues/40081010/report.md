# ASSERTION FAILED: !value || (value->isValueList())

| Field | Value |
|-------|-------|
| **Issue ID** | [40081010](https://issues.chromium.org/issues/40081010) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Reporter** | cl...@gmail.com |
| **Assignee** | ti...@chromium.org |
| **Created** | 2014-12-14 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

The following testcase crashes the latest chrome asan build as follows:

# ASAN:SIGSEGV

==19462==ERROR: AddressSanitizer: SEGV on unknown address 0x00009f7537dd (pc 0x7fe9ffe2655a bp 0x7fff758fe810 sp 0x7fff758fe800 T0)  

#0 0x7fe9ffe26559 in blink::toCSSValueList(blink::CSSValue\*) /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/WebKit/Source/core/css/CSSValueList.h:74 (discriminator 4)  

#1 0x7fe9ffe0799c in resolveKeyframes /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/WebKit/Source/core/animation/css/CSSAnimations.cpp:121  

#2 0x7fe9ffe04e43 in calculateAnimationUpdate /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/WebKit/Source/core/animation/css/CSSAnimations.cpp:294  

#3 0x7fe9ffe04596 in blink::CSSAnimations::calculateUpdate(blink::Element const\*, blink::Element&, blink::RenderStyle const&, blink::RenderStyle\*, blink::StyleResolver\*) /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/WebKit/Source/core/animation/css/CSSAnimations.cpp:239  

#4 0x7fea00006007 in blink::StyleResolver::applyAnimatedProperties(blink::StyleResolverState&, blink::Element const\*) /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/WebKit/Source/core/css/resolver/StyleResolver.cpp:999  

#5 0x7fea00004219 in styleForElement /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/WebKit/Source/core/css/resolver/StyleResolver.cpp:647  

#6 0x7fe9ff8716be in inheritHtmlAndBodyElementStyles /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/Document.cpp:1682  

#7 0x7fe9ff873b21 in updateStyle /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/Document.cpp:1869  

#8 0x7fe9ff873165 in updateRenderTree /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/Document.cpp:1815  

#9 0x7fe9ff87a193 in implicitClose /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/Document.cpp:2563  

#10 0x7fea0033b763 in checkCompleted /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/WebKit/Source/core/loader/FrameLoader.cpp:501  

#11 0x7fea00338f56 in finishedParsing /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/WebKit/Source/core/loader/FrameLoader.cpp:431  

#12 0x7fe9ff890d15 in finishedParsing /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/Document.cpp:4647  

#13 0x7fe9ffc71beb in blink::HTMLDocumentParser::end() /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:822  

#14 0x7fe9ffc692bd in prepareToStopParsing /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:251  

#15 0x7fe9ffc6cbec in blink::HTMLDocumentParser::processParsedChunkFromBackgroundParser(WTF::PassOwnPtr[blink::HTMLDocumentParser::ParsedChunk](javascript:void(0);)) /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:479  

#16 0x7fe9ffc6a315 in pumpPendingSpeculations /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:525  

#17 0x7fe9ffc6acc5 in didReceiveParsedChunkFromBackgroundParser /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:349  

#18 0x7fe9ffd7e465 in WTF::FunctionWrapper<void (blink::HTMLDocumentParser::\*)(WTF::PassOwnPtr[blink::HTMLDocumentParser::ParsedChunk](javascript:void(0);))>::operator()(WTF::WeakPtr[blink::HTMLDocumentParser](javascript:void(0);) const&, WTF::PassOwnPtr[blink::HTMLDocumentParser::ParsedChunk](javascript:void(0);)) /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/WebKit/Source/wtf/Functional.h:88 (discriminator 4)  

#19 0x7fe9ffd7e2cf in WTF::BoundFunctionImpl<WTF::FunctionWrapper<void (blink::HTMLDocumentParser::\*)(WTF::PassOwnPtr[blink::HTMLDocumentParser::ParsedChunk](javascript:void(0);))>, void (WTF::WeakPtr[blink::HTMLDocumentParser](javascript:void(0);), WTF::PassOwnPtr[blink::HTMLDocumentParser::ParsedChunk](javascript:void(0);))>::operator()() /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/WebKit/Source/wtf/Functional.h:355  

#20 0x7fe9feca89fa in WTF::callFunctionObject(void\*) /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/WebKit/Source/wtf/MainThread.cpp:65  

#21 0x7fe9fcd0a61c in base::internal::InvokeHelper<false, void, base::internal::RunnableAdapter<void (\*)(void\*)>, void (void\* const&)>::MakeItSo(base::internal::RunnableAdapter<void (\*)(void\*)>, void\* const&) /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../base/bind\_internal.h:381  

#22 0x7fe9fce48ef6 in base::debug::TaskAnnotator::RunTask(char const\*, char const\*, base::PendingTask const&) /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../base/debug/task\_annotator.cc:63  

#23 0x7fe9fcd89360 in base::MessageLoop::RunTask(base::PendingTask const&) /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../base/message\_loop/message\_loop.cc:448  

#24 0x7fe9fcd89a7f in DeferOrRunPendingTask /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../base/message\_loop/message\_loop.cc:458  

#25 0x7fe9fcd89f7c in DoWork /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../base/message\_loop/message\_loop.cc:567  

#26 0x7fe9fcd9232c in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../base/message\_loop/message\_pump\_default.cc:32  

#27 0x7fe9fcdbd823 in base::RunLoop::Run() /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../base/run\_loop.cc:55  

#28 0x7fe9fcd880c2 in base::MessageLoop::Run() /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../base/message\_loop/message\_loop.cc:310  

#29 0x7fea0491c5cc in RendererMain /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../content/renderer/renderer\_main.cc:235  

#30 0x7fe9fccf1fde in RunZygote /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../content/app/content\_main\_runner.cc:347  

#31 0x7fe9fccf43eb in Run /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../content/app/content\_main\_runner.cc:789  

#32 0x7fe9fccf1534 in content::ContentMain(content::ContentMainParams const&) /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../content/app/content\_main.cc:19  

#33 0x7fe9fbcdce62 in ChromeMain /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../chrome/app/chrome\_main.cc:66  

#34 0x7fe9f1b9aec4 in \_\_libc\_start\_main /build/buildd/eglibc-2.19/csu/libc-start.c:287

The crash occurs on a ASSERT\_WITH\_SECURITY\_IMPLICATIONS

**VERSION**  

Chrome Version: asan-symbolized-linux-release-307759  

Operating System: linux 64 bit

**REPRODUCTION CASE**

<script>
function start() {
o0=document.documentElement;
o15=document.createElement('style');
o15.innerHTML = '@-webkit-keyframes key0 { from { -webkit-animation-timing-function: unset; } }';
document.head.appendChild(o15);
o0.style.webkitAnimationName = 'key0';
}
</script>
<body onload="start()"></body>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab

## Timeline

### cl...@chromium.org (2014-12-15)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5750184314142720

### in...@chromium.org (2014-12-15)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-12-15)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-12-15)

Cannot reproduce this on CF. Can you please check using latest trunk build ? Are you using any other command line flags ?

### cl...@gmail.com (2014-12-15)

Hi,

307759 is the latest build available from https://commondatastorage.googleapis.com/chromium-browser-asan/index.html?prefix=linux-release/

It reproduces 100% reliably for me without any flags :-/ 

The testcase prints an assertion on ASSERT_WITH_SECURITY_IMPLICATIONS before crashing:

ASSERTION FAILED: !value || (value->isValueList())
../../third_party/WebKit/Source/core/css/CSSValueList.h(74) : blink::CSSValueList *blink::toCSSValueList(blink::CSSValue *)

Is CF maybe ignoring ASSERTIONS?

### ts...@chromium.org (2014-12-15)

Repro'd locally against 41.0.2247.0 / linux / asan.

### cl...@chromium.org (2014-12-15)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-12-15)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-12-16)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5766199810981888

Uploader: mbarbella@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: ASSERT
Crash Address: 
Crash State:
  ASSERTION FAILED: !value || (value->isValueList())
  blink::CSSAnimations::calculateAnimationUpdate
  blink::CSSAnimations::calculateUpdate
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=307131:307349

Minimized Testcase (0.30 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv96MT7VEwCjbVFifV9klu2kyfy9YVdRtcMOiDOWPS7VBK2RqL5CrhIaae_dA4sArvznNe_7RmaVfF-ylR5cz7WwemTGNumZaQx0BvA0mkFnjxUv_F4iWrI1W-Qsu3jWaAD1bTM3hRj4Oj9-Xcq3yzO0ChZDKfQ
<script>
function start() {
o0=document.documentElement;
o15=document.createElement('style');
o15.innerHTML = '@-webkit-keyframes key0 { from { -webkit-animation-timing-function: unset; } }';
document.head.appendChild(o15);
o0.style.webkitAnimationName = 'key0';
}
</script>
<body onload="start()"></body>



Filer: inferno

### in...@chromium.org (2014-12-16)

Author: philipj@opera.com 
Component: blink
Changelist: https://chromium.googlesource.com/chromium/blink.git/+/04ff98e66ab4d4a7c77225dc86e30ceb78d7785c
Time: Mon Dec 08 11:33:11 2014
File Document.cpp is changed in this cl (and is part of stack frame #6, "blink::Document::inheritHtmlAndBodyElementStyles"; frame #7, "blink::Document::updateStyle"; frame #8, "blink::Document::updateRenderTree"; frame #9, "blink::Document::implicitClose")
Minimum distance from crash line to modified line: 488. (file: Document.cpp, crashed on: 1679, modified: 1191).

Suspected component: blink

### cl...@chromium.org (2014-12-16)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-12-16)

[Empty comment from Monorail migration]

### [Deleted User] (2014-12-17)

Reverting Blink r186637 fixes the problem, assigning to Rob Buis as the original author of the doubly reverted CL: https://codereview.chromium.org/775153002

### in...@chromium.org (2014-12-17)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-12-18)

[Empty comment from Monorail migration]

### rw...@gmail.com (2014-12-18)

Sorry, I did not see this bug.
Looks like resolveKeyframes not knowing unset is the problem.
I did a quick speculative fix there:

-                else if (value->isInheritedValue() || value->isInitialValue())
+                else if (value->isInheritedValue() || value->isInitialValue() || value->isUnsetValue())
                     timingFunction = CSSTimingData::initialTimingFunction();

That seems to fix the crash. However, I don't know if that is a correct fix, and since the sydney group has all the animation knowledge, I think it is best if Tim
does the fix (he already started) but let me knowif I can help further.

### bu...@chromium.org (2014-12-19)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=187512

------------------------------------------------------------------
r187512 | timloh@chromium.org | 2014-12-19T05:52:57.841148Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/animations/keyframe-timing-function-unset-crash-expected.txt?r1=187512&r2=187511&pathrev=187512
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/animation/DeferredLegacyStyleInterpolation.cpp?r1=187512&r2=187511&pathrev=187512
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/animations/keyframe-timing-function-unset-crash.html?r1=187512&r2=187511&pathrev=187512
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/animation/AnimationInputHelpers.cpp?r1=187512&r2=187511&pathrev=187512
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/animation/AnimationInputHelpersTest.cpp?r1=187512&r2=187511&pathrev=187512
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/animation/css/CSSAnimations.cpp?r1=187512&r2=187511&pathrev=187512

Handle 'unset' timing functions better

This patch fixes a crash when using 'animation-timing-function: unset'.
We previously expected to either get initial, inherit, or a value list,
but 'unset' is now also a valid global css value.

BUG=442121

Review URL: https://codereview.chromium.org/811623009
-----------------------------------------------------------------

### in...@chromium.org (2014-12-19)

[Empty comment from Monorail migration]

### am...@google.com (2014-12-19)

Is there a merge required here?

### cl...@chromium.org (2014-12-19)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-12-20)

ClusterFuzz has detected this issue as fixed in range 309126:309171.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5766199810981888

Uploader: mbarbella@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: ASSERT
Crash Address: 
Crash State:
  ASSERTION FAILED: !value || (value->isValueList())
  blink::CSSAnimations::calculateAnimationUpdate
  blink::CSSAnimations::calculateUpdate
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=307131:307349
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=309126:309171

Minimized Testcase (0.30 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv96MT7VEwCjbVFifV9klu2kyfy9YVdRtcMOiDOWPS7VBK2RqL5CrhIaae_dA4sArvznNe_7RmaVfF-ylR5cz7WwemTGNumZaQx0BvA0mkFnjxUv_F4iWrI1W-Qsu3jWaAD1bTM3hRj4Oj9-Xcq3yzO0ChZDKfQ
<script>
function start() {
o0=document.documentElement;
o15=document.createElement('style');
o15.innerHTML = '@-webkit-keyframes key0 { from { -webkit-animation-timing-function: unset; } }';
document.head.appendChild(o15);
o0.style.webkitAnimationName = 'key0';
}
</script>
<body onload="start()"></body>

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### in...@chromium.org (2014-12-20)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-12-23)

[Empty comment from Monorail migration]

### ma...@google.com (2014-12-23)

Approved for M40 (branch: 2214)

### in...@chromium.org (2015-01-02)

Please merges these fixes to M40 (branch: 2214) asap. The branch will be cut soon for M40 release.

### ti...@chromium.org (2015-01-05)

Doesn't look like the offending changes made it to M40; https://codereview.chromium.org/775153002 landed at 186604 (relanded at 186637), OmahaProxy says M40's base revision is 184994.

### in...@chromium.org (2015-01-05)

Thanks!

### ti...@google.com (2015-01-22)

$2000 for this one. Please enjoy.

### ti...@google.com (2015-03-09)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-03-27)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2015-04-07)

Processing via our e-payment system can take up to six weeks, but the reward should be on its way to you. Thanks again for your help!

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/442121?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/444341]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081010)*
