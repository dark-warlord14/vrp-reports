# UNKNOWN in SkARGB32_Blitter::blitV

| Field | Value |
|-------|-------|
| **Issue ID** | [40055770](https://issues.chromium.org/issues/40055770) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals |
| **Reporter** | ao...@gmail.com |
| **Assignee** | sc...@gmail.com |
| **Created** | 2012-03-28 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

A renderer crash happens at an unknown address when the attached page is opened. The address moves with ASLR, at least one of the arguments seems to affect it, and there is a large numeric argument in one call suggesting an integer error.

**VERSION**  

Chrome Version: 17.0.963.83 stable, 19.0.1083.0 dev  

Operating System: Linux (Debian 6.0.4, x86\_64)

**REPRODUCTION CASE**  

$ google-chrome blit.html

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State:

==28626== ERROR: AddressSanitizer crashed on unknown address 0x7f61a55f2a10 (pc 0x7f60b8363e62 sp 0x7fffcf18d900 bp 0x7fffcf18d910 T0)  

AddressSanitizer can not provide additional info. ABORTING  

#0 0x7f60b8363e62 in SkARGB32\_Blitter::blitV(int, int, int, unsigned char) ???:0  

#1 0x7f60b82aac67 in vline(int, int, int, int, SkBlitter\*, int) third\_party/skia/src/core/SkScan\_Antihair.cpp:0  

#2 0x7f60b82a6c0f in do\_anti\_hairline(int, int, int, int, SkIRect const\*, SkBlitter\*) third\_party/skia/src/core/SkScan\_Antihair.cpp:0  

#3 0x7f60b82a66dd in do\_anti\_hairline(int, int, int, int, SkIRect const\*, SkBlitter\*) third\_party/skia/src/core/SkScan\_Antihair.cpp:0  

#4 0x7f60b82a66c5 in do\_anti\_hairline(int, int, int, int, SkIRect const\*, SkBlitter\*) third\_party/skia/src/core/SkScan\_Antihair.cpp:0  

#5 0x7f60b82a66c5 in do\_anti\_hairline(int, int, int, int, SkIRect const\*, SkBlitter\*) third\_party/skia/src/core/SkScan\_Antihair.cpp:0  

#6 0x7f60b82a66c5 in do\_anti\_hairline(int, int, int, int, SkIRect const\*, SkBlitter\*) third\_party/skia/src/core/SkScan\_Antihair.cpp:0  

#7 0x7f60b82a66c5 in do\_anti\_hairline(int, int, int, int, SkIRect const\*, SkBlitter\*) third\_party/skia/src/core/SkScan\_Antihair.cpp:0  

#8 0x7f60b82a66c5 in do\_anti\_hairline(int, int, int, int, SkIRect const\*, SkBlitter\*) third\_party/skia/src/core/SkScan\_Antihair.cpp:0  

#9 0x7f60b82a66c5 in do\_anti\_hairline(int, int, int, int, SkIRect const\*, SkBlitter\*) third\_party/skia/src/core/SkScan\_Antihair.cpp:0  

#10 0x7f60b82a66c5 in do\_anti\_hairline(int, int, int, int, SkIRect const\*, SkBlitter\*) third\_party/skia/src/core/SkScan\_Antihair.cpp:0  

#11 0x7f60b82a66c5 in do\_anti\_hairline(int, int, int, int, SkIRect const\*, SkBlitter\*) third\_party/skia/src/core/SkScan\_Antihair.cpp:0  

#12 0x7f60b82a66c5 in do\_anti\_hairline(int, int, int, int, SkIRect const\*, SkBlitter\*) third\_party/skia/src/core/SkScan\_Antihair.cpp:0  

#13 0x7f60b82a66c5 in do\_anti\_hairline(int, int, int, int, SkIRect const\*, SkBlitter\*) third\_party/skia/src/core/SkScan\_Antihair.cpp:0  

#14 0x7f60b82a66c5 in do\_anti\_hairline(int, int, int, int, SkIRect const\*, SkBlitter\*) third\_party/skia/src/core/SkScan\_Antihair.cpp:0  

#15 0x7f60b82a66c5 in do\_anti\_hairline(int, int, int, int, SkIRect const\*, SkBlitter\*) third\_party/skia/src/core/SkScan\_Antihair.cpp:0  

#16 0x7f60b82a66c5 in do\_anti\_hairline(int, int, int, int, SkIRect const\*, SkBlitter\*) third\_party/skia/src/core/SkScan\_Antihair.cpp:0  

#17 0x7f60b82a66c5 in do\_anti\_hairline(int, int, int, int, SkIRect const\*, SkBlitter\*) third\_party/skia/src/core/SkScan\_Antihair.cpp:0  

#18 0x7f60b82a66c5 in do\_anti\_hairline(int, int, int, int, SkIRect const\*, SkBlitter\*) third\_party/skia/src/core/SkScan\_Antihair.cpp:0  

#19 0x7f60b82a66c5 in do\_anti\_hairline(int, int, int, int, SkIRect const\*, SkBlitter\*) third\_party/skia/src/core/SkScan\_Antihair.cpp:0  

#20 0x7f60b82a6394 in SkScan::AntiHairLineRgn(SkPoint const&, SkPoint const&, SkRegion const\*, SkBlitter\*) ???:0  

#21 0x7f60b82ae21f in hairquad(SkPoint const\*, SkRegion const\*, SkBlitter\*, int, void (\*)(SkPoint const&, SkPoint const&, SkRegion const\*, SkBlitter\*)) third\_party/skia/src/core/SkScan\_Hairline.cpp:0  

#22 0x7f60b82ae1fc in hairquad(SkPoint const\*, SkRegion const\*, SkBlitter\*, int, void (\*)(SkPoint const&, SkPoint const&, SkRegion const\*, SkBlitter\*)) third\_party/skia/src/core/SkScan\_Hairline.cpp:0  

#23 0x7f60b82ae1fc in hairquad(SkPoint const\*, SkRegion const\*, SkBlitter\*, int, void (\*)(SkPoint const&, SkPoint const&, SkRegion const\*, SkBlitter\*)) third\_party/skia/src/core/SkScan\_Hairline.cpp:0  

#24 0x7f60b82ae1fc in hairquad(SkPoint const\*, SkRegion const\*, SkBlitter\*, int, void (\*)(SkPoint const&, SkPoint const&, SkRegion const\*, SkBlitter\*)) third\_party/skia/src/core/SkScan\_Hairline.cpp:0  

#25 0x7f60b82ae1fc in hairquad(SkPoint const\*, SkRegion const\*, SkBlitter\*, int, void (\*)(SkPoint const&, SkPoint const&, SkRegion const\*, SkBlitter\*)) third\_party/skia/src/core/SkScan\_Hairline.cpp:0  

#26 0x7f60b82ae1fc in hairquad(SkPoint const\*, SkRegion const\*, SkBlitter\*, int, void (\*)(SkPoint const&, SkPoint const&, SkRegion const\*, SkBlitter\*)) third\_party/skia/src/core/SkScan\_Hairline.cpp:0  

#27 0x7f60b82acaeb in hair\_path(SkPath const&, SkRasterClip const&, SkBlitter\*, void (\*)(SkPoint const&, SkPoint const&, SkRegion const\*, SkBlitter\*)) third\_party/skia/src/core/SkScan\_Hairline.cpp:0  

#28 0x7f60b8236bba in SkDraw::drawPath(SkPath const&, SkPaint const&, SkMatrix const\*, bool) const ???:0  

#29 0x7f60b8225dc5 in SkCanvas::drawPath(SkPath const&, SkPaint const&) ???:0  

#30 0x7f60b9105dc2 in WebCore::GraphicsContext::strokePath(WebCore::Path const&) ???:0  

#31 0x7f60b8dcd91c in WebCore::CanvasRenderingContext2D::stroke() ???:0  

#32 0x7f60ba80a2ba in WebCore::CanvasRenderingContext2DInternal::strokeCallback(v8::Arguments const&) out/Release/obj/gen/webkit/bindings/V8DerivedSources17.cpp:0  

#33 0x7f60b7682946 in v8::internal::Builtin\_HandleApiCall(v8::internal::(anonymous namespace)::BuiltinArguments<(v8::internal::BuiltinExtraArguments)1>, v8::internal::Isolate\*) v8/src/builtins.cc:0  

#34 0x7f608200618e  

#35 0x7f60820344a4  

#36 0x7f6082023dc7  

#37 0x7f6082011357  

#38 0x7f60b76ee654 in v8::internal::Invoke(bool, v8::internal::Handle[v8::internal::JSFunction](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*, bool\*) v8/src/execution.cc:0  

#39 0x7f60b7618a73 in v8::Script::Run() ???:0  

#40 0x7f60b9347804 in WebCore::V8Proxy::runScript(v8::Handle[v8::Script](javascript:void(0);)) ???:0  

#41 0x7f60b9346995 in WebCore::V8Proxy::evaluate(WebCore::ScriptSourceCode const&, WebCore::Node\*) ???:0  

#42 0x7f60b92f3576 in WebCore::ScriptController::evaluate(WebCore::ScriptSourceCode const&) ???:0  

#43 0x7f60b88638ec in WebCore::ScriptElement::executeScript(WebCore::ScriptSourceCode const&) ???:0  

#44 0x7f60b885f0f5 in WebCore::ScriptElement::prepareScript(WTF::TextPosition const&, WebCore::ScriptElement::LegacyTypeSupport) ???:0  

#45 0x7f60b8e354e4 in WebCore::HTMLScriptRunner::runScript(WebCore::Element\*, WTF::TextPosition const&) ???:0  

#46 0x7f60b8e34f71 in WebCore::HTMLScriptRunner::execute(WTF::PassRefPtr[WebCore::Element](javascript:void(0);), WTF::TextPosition const&) ???:0  

#47 0x7f60b8e2952d in WebCore::HTMLDocumentParser::runScriptsForPausedTreeBuilder() ???:0  

#48 0x7f60b8e298a0 in WebCore::HTMLDocumentParser::canTakeNextToken(WebCore::HTMLDocumentParser::SynchronousMode, WebCore::PumpSession&) ???:0  

#49 0x7f60b8e28b26 in WebCore::HTMLDocumentParser::pumpTokenizer(WebCore::HTMLDocumentParser::SynchronousMode) ???:0  

#50 0x7f60b8e2a654 in WebCore::HTMLDocumentParser::append(WebCore::SegmentedString const&) ???:0  

#51 0x7f60bc909c2c in WebCore::DecodedDataDocumentParser::flush(WebCore::DocumentWriter\*) ???:0  

#52 0x7f60b98a18d1 in WebCore::DocumentWriter::endIfNotLoadingMainResource() ???:0  

#53 0x7f60b98d7d99 in WebCore::FrameLoader::finishedLoading() ???:0  

#54 0x7f60b9900611 in WebCore::MainResourceLoader::didFinishLoading(double) ???:0  

#55 0x7f60bb0d94e2 in webkit\_glue::WebURLLoaderImpl::Context::OnCompletedRequest(net::URLRequestStatus const&, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, base::TimeTicks const&) ???:0  

#56 0x7f60b80fe00b in ResourceDispatcher::OnRequestComplete(int, net::URLRequestStatus const&, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, base::TimeTicks const&) ???:0  

#57 0x7f60b80fee8b in bool ResourceMsg\_RequestComplete::Dispatch<ResourceDispatcher, ResourceDispatcher, void (ResourceDispatcher::\*)(int, net::URLRequestStatus const&, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, base::TimeTicks const&)>(IPC::Message const\*, ResourceDispatcher\*, ResourceDispatcher\*, void (ResourceDispatcher::\*)(int, net::URLRequestStatus const&, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, base::TimeTicks const&)) ???:0  

#58 0x7f60b80fb7ed in ResourceDispatcher::DispatchMessage(IPC::Message const&) ???:0  

#59 0x7f60b80f9ac1 in ResourceDispatcher::OnMessageReceived(IPC::Message const&) ???:0  

#60 0x7f60b7ff494f in ChildThread::OnMessageReceived(IPC::Message const&) ???:0  

#61 0x7f60b6d1b7e3 in IPC::ChannelProxy::Context::OnDispatchMessage(IPC::Message const&) ???:0  

#62 0x7f60b6c09a26 in MessageLoop::RunTask(base::PendingTask const&) ???:0  

#63 0x7f60b6c0a286 in MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) ???:0  

Stats: 3M malloced (5M for red zones) by 15209 calls  

Stats: 0M realloced by 44 calls  

Stats: 2M freed by 7323 calls  

Stats: 0M really freed by 0 calls  

Stats: 48M (12296 full pages) mmaped in 12 calls  

mmaps by size class: 8:16383; 9:8191; 10:4095; 11:2047; 12:1024; 13:512; 14:256; 15:128; 16:64; 17:32; 18:16; 19:8;  

mallocs by size class: 8:13793; 9:653; 10:398; 11:203; 12:38; 13:41; 14:57; 15:8; 16:9; 17:5; 18:2; 19:2;  

frees by size class: 8:6472; 9:334; 10:310; 11:103; 12:16; 13:30; 14:45; 15:4; 16:2; 17:4; 18:2; 19:1;  

rfrees by size class:  

Stats: malloc large: 9 small slow: 68

## Attachments

- [blit.html](attachments/blit.html) (text/x-fortran; charset=us-ascii, 222 B)
- [bigarc.html](attachments/bigarc.html) (text/x-fortran; charset=us-ascii, 218 B)
- [repros-in-130133.txt](attachments/repros-in-130133.txt) (text/plain; charset=utf-8, 7.8 KB)

## Timeline

### kc...@chromium.org (2012-03-28)

first guess: stack overflow. asan uses way more stack that regular run. 
may simply need to increase the thread's stack size. 

### kc...@chromium.org (2012-03-28)

Nope. No relation to stack. Looks more like a completely wild dereference. 

### in...@chromium.org (2012-03-29)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=31757765

Uploader: inferno@chromium.org

Crash Type: UNKNOWN
Crash Address: 0x7f38734e5a10
Crash State:
  - crash stack -
  SkARGB32_Blitter::blitV
  vline
  do_anti_hairline
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=109205:109251

Minimized Testcase (0.20 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv96RhzG9Ernh-XJ6dJ-6rGHooMrbanFarllYzD_0pDJtJ3xqtH0dJ4eQjxgnewxgpITBNhpPGnRWPN0GC9s7fXXV93xhgYjqgUjg_XyGn3NSeJEYmBnh5FE9RQvtZuRAq60JAZrXkUHzL8eHxMyNQe1R9b8cfg
<script>
C = document.createElement("canvas");
A = C.getContext("2d");
C.height = 400;
P = 3.14159265;
A.translate(100,300);
A.arc(0,0,170141183460469231731687303715884105724,P*2,0,0);
A.stroke();
</script>

### in...@chromium.org (2012-03-29)

Elliot, this seems to have regressed in Skia: r2620:r2633. Can you please help to triage this.

### [Deleted User] (2012-03-29)

skia rev. 2632 looks to be done explicitly to handle NaN values in paths, which the arc code in #3 might create. I will test that case now in tip-of-tree, to see its current behavior.

### ka...@google.com (2012-03-30)

[Empty comment from Monorail migration]

### ka...@google.com (2012-03-30)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-03-30)

Reverting wrong marking of security bugs by release management.

### in...@chromium.org (2012-03-30)

[Empty comment from Monorail migration]

### [Deleted User] (2012-03-30)

Assigning over to Mike.  He is going to download some prebuilt ASAN binaries from https://commondatastorage.googleapis.com/chromium-browser-asan/index.html and see if he can reproduce the bug.

### [Deleted User] (2012-03-30)

Speculative fix in Skia-rev. 3558

### [Deleted User] (2012-03-30)

[Empty comment from Monorail migration]

### [Deleted User] (2012-03-30)

repro case from #3 as a file, attached...

### [Deleted User] (2012-03-30)

I was able to repro using tip-of-tree (debug build) by loading bigarc.html, and disabling gpu canvas (which is now on by default, and which doesn't have this bug).

--disable-accelerated-2d-canvas


### ep...@google.com (2012-03-30)

Thanks for the fix in http://code.google.com/p/skia/source/detail?r=3558 , Mike!

Mike is going to be out of town next week, so I am taking ownership... on Monday, I will confirm that this has indeed been fixed in the latest canary build, and then request permission to merge the fix into M18.


### ep...@google.com (2012-04-02)

The fix was just now rolled into Chrome within this Skia DEPS roll: http://crrev.com/130175

### ep...@google.com (2012-04-02)

Baseline for comparison once the above fix goes into a test build...

I downloaded asan-linux-release-130133 from https://commondatastorage.googleapis.com/chromium-browser-asan/index.html
and ran it on my remote Linux instance (no GPU).  When I opened blit.html from https://crbug.com/chromium/120648#c1, I saw an ASAN stack trace similar to that pasted in https://crbug.com/chromium/120648#c1.

more details in the attachment...

### sc...@gmail.com (2012-04-02)

Thanks for being so on top of all these Skia issues, Elliot. You're awesome.
We can look to merge this to Chrome 19 once the change survives a canary (or perhaps M20 dev channel)

### ao...@gmail.com (2012-04-02)

Fix looks good here. 130186 had no issues with the files which triggered this earlier.

### cl...@chromium.org (2012-04-03)

ClusterFuzz has detected this issue as fixed in range 130154:130180.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=31757765

Uploader: inferno@chromium.org

Crash Type: UNKNOWN
Crash Address: 0x7f38734e5a10
Crash State:
  - crash stack -
  SkARGB32_Blitter::blitV
  vline
  do_anti_hairline
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=109205:109251
Fixed: https://cluster-fuzz.appspot.com/revisions?range=130154:130180

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv96RhzG9Ernh-XJ6dJ-6rGHooMrbanFarllYzD_0pDJtJ3xqtH0dJ4eQjxgnewxgpITBNhpPGnRWPN0GC9s7fXXV93xhgYjqgUjg_XyGn3NSeJEYmBnh5FE9RQvtZuRAq60JAZrXkUHzL8eHxMyNQe1R9b8cfg

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### ep...@google.com (2012-04-03)

Works for me too... I downloaded asan-linux-release-130180 from https://commondatastorage.googleapis.com/chromium-browser-asan/index.html
and ran it on my remote Linux instance (no GPU).  When I opened blit.html from https://crbug.com/chromium/120648#c1, I did not get any errors at all.

This bug is now marked as M19/Merge-Approved, so I will go ahead and prepare an M19 patch...

But don't we also want an M18 patch?

### pa...@chromium.org (2012-04-03)

I'd think we do want an M18 patch. Will the diff be as small as it was for M19? Thanks!

### sc...@gmail.com (2012-04-03)

@epoger: the usual "safe" way forward is:
- Let the Skia change roll into a canary to make sure nothing terrible is broken.
- Merge it to a dev channel for wider baking / testing.
- Merge back to stable finally if all is well.

### ep...@google.com (2012-04-04)

Fix merged into Skia's chrome/1084 branch as http://code.google.com/p/skia/source/detail?r=3604

Using a local M19-branch ASAN build on Mac, I have confirmed that I DID see the failure before the above merge, and I DO NOT see the failure after the above merge.

[Be sure to use the --disable-accelerated-2d-canvas command-line argument , or else the bug will not reproduce on most systems.]

Do we have precompiled M19-branch ASAN build binaries somewhere so that we can confirm that the next official release build contains the fix?  I don't see any M19 builds at https://commondatastorage.googleapis.com/chromium-browser-asan/index.html ...

[Reminder: We still need to attempt a patch into M18, once we are happy with the M19 patch.]

### sc...@gmail.com (2012-04-04)

Adding flags to make sure we revisit this for M18.

### ep...@google.com (2012-04-05)

Somebody let me know if/when it's time to merge it into M18... (once it's marked as Merge-Approved, I will do so)

### ep...@google.com (2012-04-13)

Assigning to scarybeasts for now... please assign back to me when it's time for me to merge the fix ( http://code.google.com/p/skia/source/detail?r=3558 ) into M18.

### sc...@gmail.com (2012-04-13)

(We'll leave it Merge-Approved because all security fixes are approved and we search on the label when it's merge time.... I will let you know when it is merge time, thanks so much!)

### sc...@gmail.com (2012-04-30)

There are no more M18 merge opportunities so this goes into M19 (already merged, yay). There's only a couple of weeks to wait until M19 hits stable.

### sc...@gmail.com (2012-05-04)

Thanks Aki. This involves canvas so the OOB content is plausibly recoverable.
$500

### sc...@gmail.com (2012-05-06)

Reward to be upped to $1337 and donated to http://www.betterplace.org/en/projects/2001-school-project-welkite-i-in-ethiopia-east-africa

### sc...@gmail.com (2012-05-14)

[Empty comment from Monorail migration]

### [Deleted User] (2012-05-15)

Updating status to Fixed on security bugs which were fixed when m19 went to stable.

### sc...@gmail.com (2012-06-28)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-14)

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

This issue was migrated from crbug.com/chromium/120648?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40055770)*
