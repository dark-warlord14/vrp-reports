# Heap-use-after-free in blink::PendingScript::stopWatchingForLoad

| Field | Value |
|-------|-------|
| **Issue ID** | [40081032](https://issues.chromium.org/issues/40081032) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Reporter** | cl...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2014-12-17 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**

The testcase consists of multiple files attached as crash.zip. It requires to be loaded from a webserver. It will crash the latest asan build as follows:

=================================================================  

==22594==ERROR: AddressSanitizer: heap-use-after-free on address 0x60b000035a80 at pc 0x7f53fce4e572 bp 0x7fff31916f40 sp 0x7fff31916f38  

READ of size 1 at 0x60b000035a80 thread T0 (chrome)  

#0 0x7f53fce4e571 in stopWatchingForLoad /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/PendingScript.cpp:94  

#1 0x7f53fce5215e in detach /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/ScriptLoader.cpp:114  

#2 0x7f53fcd54660 in ~ScriptRunner /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/ScriptRunner.cpp:52  

#3 0x7f53fcbc5ffb in deletePtr /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/wtf/OwnPtrCommon.h:52 (discriminator 20)  

#4 0x7f53fce98aae in ~HTMLDocument /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/html/HTMLDocument.cpp:82  

#5 0x7f53fbd4b844 in PostGarbageCollectionProcessing /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/global-handles.cc:272  

#6 0x7f53fbd4ad54 in PostGarbageCollectionProcessing /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/global-handles.cc:695  

#7 0x7f53fbd9d188 in PerformGarbageCollection /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/heap/heap.cc:1121  

#8 0x7f53fbd9beb4 in CollectGarbage /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/heap/heap.cc:844  

#9 0x7f53fbdbf7f3 in CollectGarbage /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/heap/heap-inl.h:583  

#10 0x7f53fbac63d4 in IdleNotification /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/api.cc:6716  

#11 0x7f54031607dc in DidCommit /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../content/renderer/gpu/render\_widget\_compositor.cc:898  

#12 0x7f53fb22c9e3 in BeginMainFrame /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../cc/trees/thread\_proxy.cc:830  

#13 0x7f53fb239154 in Run /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/bind\_internal.h:185  

#14 0x7f53fb238e7a in Run /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/bind\_internal.h:557  

#15 0x7f53f96b15df in Run /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/callback.h:396  

#16 0x7f53f95eb84c in RunTask /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/message\_loop/message\_loop.cc:436  

#17 0x7f53f95ec8c5 in DeferOrRunPendingTask /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/message\_loop/message\_loop.cc:446  

#18 0x7f53f95f2f7e in Run /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/message\_loop/message\_pump\_default.cc:32  

#19 0x7f53f961f9a8 in Run /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/run\_loop.cc:55  

#20 0x7f53f95e9fc6 in base::MessageLoop::Run() /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/message\_loop/message\_loop.cc:298  

#21 0x7f5402f75423 in RendererMain /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../content/renderer/renderer\_main.cc:235  

#22 0x7f53f9559b43 in RunZygote /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../content/app/content\_main\_runner.cc:347  

#23 0x7f53f955bec6 in Run /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../content/app/content\_main\_runner.cc:789  

#24 0x7f53f9559178 in ContentMain /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../content/app/content\_main.cc:19  

#25 0x7f53f86b88d4 in ChromeMain /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../chrome/app/chrome\_main.cc:66  

#26 0x7f53ee569ec4 in \_\_libc\_start\_main /build/buildd/eglibc-2.19/csu/libc-start.c:287

0x60b000035a80 is located 64 bytes inside of 104-byte region [0x60b000035a40,0x60b000035aa8)  

freed by thread T0 (chrome) here:  

#0 0x7f53f86b7f09 in operator delete(void\*) ??:?  

#1 0x7f53fd36b591 in deletePtr /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/wtf/OwnPtrCommon.h:52 (discriminator 1)  

#2 0x7f53fcb9a2c3 in removeDetachedChildrenInContainer /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/ContainerNode.cpp:467 (discriminator 1)  

#3 0x7f53fcb9ba8f in removeDetachedChildren /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/ContainerNode.cpp:84  

#4 0x7f53fd294dca in blink::HTMLHtmlElement::~HTMLHtmlElement() /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/html/HTMLHtmlElement.h:31  

#5 0x7f53fbd4b844 in PostGarbageCollectionProcessing /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/global-handles.cc:272  

#6 0x7f53fbd4ad54 in PostGarbageCollectionProcessing /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/global-handles.cc:695  

#7 0x7f53fbd9d188 in PerformGarbageCollection /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/heap/heap.cc:1121  

#8 0x7f53fbd9beb4 in CollectGarbage /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/heap/heap.cc:844  

#9 0x7f53fbdbf7f3 in CollectGarbage /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/heap/heap-inl.h:583  

#10 0x7f53fbac63d4 in IdleNotification /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/api.cc:6716  

#11 0x7f54031607dc in DidCommit /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../content/renderer/gpu/render\_widget\_compositor.cc:898  

#12 0x7f53fb22c9e3 in BeginMainFrame /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../cc/trees/thread\_proxy.cc:830  

#13 0x7f53fb239154 in Run /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/bind\_internal.h:185  

#14 0x7f53fb238e7a in Run /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/bind\_internal.h:557  

#15 0x7f53f96b15df in Run /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/callback.h:396  

#16 0x7f53f95eb84c in RunTask /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/message\_loop/message\_loop.cc:436  

#17 0x7f53f95ec8c5 in DeferOrRunPendingTask /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/message\_loop/message\_loop.cc:446  

#18 0x7f53f95f2f7e in Run /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/message\_loop/message\_pump\_default.cc:32  

#19 0x7f53f961f9a8 in Run /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/run\_loop.cc:55  

#20 0x7f53f95e9fc6 in base::MessageLoop::Run() /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/message\_loop/message\_loop.cc:298  

#21 0x7f5402f75423 in RendererMain /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../content/renderer/renderer\_main.cc:235  

#22 0x7f53f9559b43 in RunZygote /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../content/app/content\_main\_runner.cc:347  

#23 0x7f53f955bec6 in Run /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../content/app/content\_main\_runner.cc:789  

#24 0x7f53f9559178 in ContentMain /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../content/app/content\_main.cc:19  

#25 0x7f53f86b88d4 in ChromeMain /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../chrome/app/chrome\_main.cc:66  

#26 0x7f53ee569ec4 in \_\_libc\_start\_main /build/buildd/eglibc-2.19/csu/libc-start.c:287

previously allocated by thread T0 (chrome) here:  

#0 0x7f53f86b7989 in operator new(unsigned long) ??:?  

#1 0x7f53fd36682d in create /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/ScriptLoader.h:43  

#2 0x7f53ff236e7f in scriptConstructor /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/gen/blink/core/HTMLElementFactory.cpp:1006  

#3 0x7f53ff22d931 in createHTMLElement /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/gen/blink/core/HTMLElementFactory.cpp:1250  

#4 0x7f53fcbcc7c4 in createElement /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/Document.cpp:779  

#5 0x7f53ff030e11 in createElement1MethodForMainWorld /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/gen/blink/bindings/core/v8/V8Document.cpp:3634  

#6 0x7f53fc66239e in Call /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/arguments.cc:33  

#7 0x7f53fbb4b3df in HandleApiCallHelper<false> /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/builtins.cc:1139  

#8 0x7f53bc4071ba (<unknown module>)  

#9 0x7f53bc48365c (<unknown module>)  

#10 0x7f53bc4832bd (<unknown module>)  

#11 0x7f53bc43775f (<unknown module>)  

#12 0x7f53bc432210 (<unknown module>)  

#8 0x7f53fbc980c4 in Invoke /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/execution.cc:103  

#9 0x7f53fba96d5a in Run /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/api.cc:1609  

#10 0x7f53fe9f3972 in runCompiledScript /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/V8ScriptRunner.cpp:340  

#11 0x7f53fe97257a in executeScriptAndReturnValue /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/ScriptController.cpp:202 (discriminator 3)  

#12 0x7f53fe96c9ac in execute /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/ScheduledAction.cpp:118  

#13 0x7f53fd94865b in fired /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/frame/DOMTimer.cpp:164  

#14 0x7f540490beeb in sharedTimerFiredInternal /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/platform/ThreadTimers.cpp:137  

#15 0x7f540490b721 in sharedTimerFired /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/platform/ThreadTimers.cpp:107  

#16 0x7f53f967d1ce in Run /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/callback.h:396  

#17 0x7f53f96b15df in Run /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/callback.h:396  

#18 0x7f53f95eb84c in RunTask /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/message\_loop/message\_loop.cc:436  

#19 0x7f53f95ed140 in DeferOrRunPendingTask /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/message\_loop/message\_loop.cc:446  

#20 0x7f53f95f2e33 in Run /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/message\_loop/message\_pump\_default.cc:36  

#21 0x7f53f961f9a8 in Run /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/run\_loop.cc:55  

#22 0x7f53f95e9fc6 in base::MessageLoop::Run() /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/message\_loop/message\_loop.cc:298  

#23 0x7f5402f75423 in RendererMain /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../content/renderer/renderer\_main.cc:235  

#24 0x7f53f9559b43 in RunZygote /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../content/app/content\_main\_runner.cc:347

SUMMARY: AddressSanitizer: heap-use-after-free ??:0 ??  

Shadow bytes around the buggy address:  

0x0c167fffeb00: fa fa fa fa fa fa fd fd fd fd fd fd fd fd fd fd  

0x0c167fffeb10: fd fd fd fd fa fa fa fa fa fa fa fa fd fd fd fd  

0x0c167fffeb20: fd fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa  

0x0c167fffeb30: fa fa fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c167fffeb40: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd  

=>0x0c167fffeb50:[fd]fd fd fd fd fa fa fa fa fa fa fa fa fa fd fd  

0x0c167fffeb60: fd fd fd fd fd fd fd fd fd fd fd fd fa fa fa fa  

0x0c167fffeb70: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c167fffeb80: fd fa fa fa fa fa fa fa fa fa fd fd fd fd fd fd  

0x0c167fffeb90: fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa  

0x0c167fffeba0: fd fd fd fd fd fd fd fd fd fd fd fd fd fa fa fa  

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

==22594==ABORTING

**VERSION**  

Chrome Version: asan-symbolized-linux-release-307759

**REPRODUCTION CASE**  

Attached as crash.zip

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab

## Attachments

- [crash.zip](attachments/crash.zip) (application/zip, 756 B)

## Timeline

### cl...@chromium.org (2014-12-17)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5764418204860416

### cl...@chromium.org (2014-12-17)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5688002683600896

### in...@chromium.org (2014-12-17)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-12-17)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5764418204860416

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 1
Crash Address: 0x60f0000467a0
Crash State:
  blink::PendingScript::stopWatchingForLoad
  blink::ScriptLoader::detach
  blink::ScriptRunner::~ScriptRunner
  

Unminimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv97HTZLdza4KA_hWwJaTMlfPLro_pm0BzpsM865e6O7WO7v8vv44kNP6Cex9lQPfBF-UUiRjyII53lwS764K7JfIzpghiv2aQ0QUP7jI3jSa2or4EAKG2-Gj9XvCBEIQs8llXdC98oTOESx0ZsCbkRMApYpElg




### in...@chromium.org (2014-12-17)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-12-17)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5688002683600896

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 1
Crash Address: 0x60f0000481e0
Crash State:
  blink::PendingScript::stopWatchingForLoad
  blink::ScriptLoader::detach
  blink::ScriptRunner::~ScriptRunner
  

Unminimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv94kXFpHWJW8CFjfJN-eJaceOFink-1Nv0ys5cpymwCzBwzPbRxUiYoTLqasx1z1xYpHwbEbfdoOesx-lLwVGVe2xhzI1JE0VsCmkHrO5ZB7rTnjlhoy6Z8ElvrH7QFw9B7Nc5uQWnPoSGr5rTQFVxeslctS3w


Additional requirements: Requires HTTP



### cl...@chromium.org (2014-12-17)

[Empty comment from Monorail migration]

### ma...@chromium.org (2014-12-17)

This is most probably related to the ScriptLoader - ScriptRunner - PendingScript dance. There was a similar issue some time ago: https://crbug.com/chromium/427108, and this too seems to be related to moving nodes across documents.

Analysis based on the stack traces:

1) ContainerNode::removeDetachedChildrenInContainer calls delete on the child nodes

2) One of the deleted children is probably a HTMLScriptElement and it deletes its ScriptLoader (but doesn't notify ScriptRunner)

3) Then, the HTMLDocument is deleted and it deletes its ScriptRunner, which tries to detach the ScriptLoader which was already deleted.

### ma...@chromium.org (2014-12-17)

Here's what happens in more detail:

ScriptRunner::queueScriptForExecution <runner-1> <loader> (ASYNC_EXECUTION)

ScriptRunner::movePendingAsyncScript <runner-1> <runner-2> <loader>
(the script is in pendingAsyncScripts, so this does the right thing)

<< Something weird happens here >>

ScriptRunner::movePendingAsyncScript <runner-3> <runner-4> <loader>
(The script is not known to runner-3, so it doesn't do anything)


ScriptRunner::notifyScriptLoadError <runner-4> <loader>
(The script is not known for runner-4; an ASSERT fires here, but not in Release mode)

ScriptRunner::~ScriptRunner <runner-2>
(This detaches, and now the memory is already freed.)

IOW, we should get 

ScriptRunner::movePendingAsyncScript <runner-2> <runner-3>

but that never happens :(

### ma...@chromium.org (2014-12-17)

And the final piece of the puzzle:

in the << weird >> stage,

HTMLScriptElement::didMoveToNewDocument is called, old ScriptRunner is <runner-2>, ScriptLoader is <loader>, *but* there's no context document, so, this doesn't actually call ScriptRunner::movePendingAsyncScript.

I have no idea why that happens.

sigbjornf@, moving scripts around is your stuff, I think, e.g., here: https://codereview.chromium.org/532643002

I think the moving is not working correctly in this case... we're missing one movePendingAsyncScript and then trying to tell the wrong ScriptRunner about the loading error.

### ma...@chromium.org (2014-12-17)

[Empty comment from Monorail migration]

### ma...@chromium.org (2014-12-17)

And to clarify, this is most probably a problem w/ script moving which has always been there, but exposed by my ScriptRunner / ScriptLoader refactoring, because now we actually *do* care that ScriptLoaders are associated to the right ScriptRunners. The state before the refactoring was more relaxed, so, stuff wouldn't crash even if the associations were incorrect (though ASSERTS would fire).

### js...@chromium.org (2014-12-17)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-12-17)

[Empty comment from Monorail migration]

### [Deleted User] (2014-12-17)

Thanks for analyzing and narrowing down the problem quite closely. Will fix tomorrow morning (CET). A script element is moved to a frame-detached document only to be moved to another document just after, afaict. This confuses the moving of async ScriptLoaders between the document ScriptRunners.

### bu...@chromium.org (2014-12-18)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=187458

------------------------------------------------------------------
r187458 | sigbjornf@opera.com | 2014-12-18T13:11:21.692888Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/dom/HTMLScriptElement/script-element-moved-to-detached-document-crash.html?r1=187458&r2=187457&pathrev=187458
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/html/HTMLScriptElement.cpp?r1=187458&r2=187457&pathrev=187458
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/dom/HTMLScriptElement/resources/script-element-moved-to-detached-document-crash-frames.html?r1=187458&r2=187457&pathrev=187458
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/dom/HTMLScriptElement/script-element-moved-to-detached-document-crash-expected.txt?r1=187458&r2=187457&pathrev=187458

Correctly move script element to a detached document.

If a script element ends up being moved over to a new document's tree,
its script loader is re-associated with that document's script runner
if the load is still pending. That association of script runner and
loader needs to reflect document association of the element itself,
otherwise completion of script loading and any later movement of the
element to another document will go wrong.

R=marja,jochen
BUG=443115

Review URL: https://codereview.chromium.org/809323002
-----------------------------------------------------------------

### [Deleted User] (2014-12-18)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-12-18)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### in...@chromium.org (2014-12-22)

[Empty comment from Monorail migration]

### ma...@google.com (2014-12-22)

Approved for M40 (branch: 2214)

### bu...@chromium.org (2014-12-30)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=187772

------------------------------------------------------------------
r187772 | sigbjornf@opera.com | 2014-12-30T09:58:39.265494Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/branches/chromium/2214/LayoutTests/fast/dom/HTMLScriptElement/script-element-moved-to-detached-document-crash-expected.txt?r1=187772&r2=187771&pathrev=187772
   A http://src.chromium.org/viewvc/blink/branches/chromium/2214/LayoutTests/fast/dom/HTMLScriptElement/script-element-moved-to-detached-document-crash.html?r1=187772&r2=187771&pathrev=187772
   M http://src.chromium.org/viewvc/blink/branches/chromium/2214/Source/core/html/HTMLScriptElement.cpp?r1=187772&r2=187771&pathrev=187772
   A http://src.chromium.org/viewvc/blink/branches/chromium/2214/LayoutTests/fast/dom/HTMLScriptElement/resources/script-element-moved-to-detached-document-crash-frames.html?r1=187772&r2=187771&pathrev=187772

Merge 187458 "Correctly move script element to a detached document."

> Correctly move script element to a detached document.
> 
> If a script element ends up being moved over to a new document's tree,
> its script loader is re-associated with that document's script runner
> if the load is still pending. That association of script runner and
> loader needs to reflect document association of the element itself,
> otherwise completion of script loading and any later movement of the
> element to another document will go wrong.
> 
> R=marja,jochen
> BUG=443115
> 
> Review URL: https://codereview.chromium.org/809323002

TBR=sigbjornf@opera.com

Review URL: https://codereview.chromium.org/798493005
-----------------------------------------------------------------

### bu...@chromium.org (2014-12-30)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=187777

------------------------------------------------------------------
r187777 | sigbjornf@opera.com | 2014-12-30T11:27:34.667217Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/html/HTMLScriptElement.cpp?r1=187777&r2=187776&pathrev=187777

Improve HTMLScriptElement::didMoveToNewDocument() comment.

Clarify when contextDocument() will return no Document; comment-only
change.

R=haraken
BUG=443115
NOTRY=true

Review URL: https://codereview.chromium.org/827233002
-----------------------------------------------------------------

### aa...@google.com (2014-12-30)

[Empty comment from Monorail migration]

### ti...@google.com (2015-01-22)

Congrats - $2000 for this report.

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

This issue was migrated from crbug.com/chromium/443115?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081032)*
