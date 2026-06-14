# Heap-use-after-free in blink::ScopedStyleResolver::collectFeaturesTo

| Field | Value |
|-------|-------|
| **Issue ID** | [40081029](https://issues.chromium.org/issues/40081029) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Reporter** | cl...@gmail.com |
| **Assignee** | ko...@chromium.org |
| **Created** | 2014-12-17 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

The contents of the attached archive will trigger a crash when crash.html is loaded from a web server. The testcase requires the --js-flags=--expose-gc flag. It crashes the latest asan chrome build as follows:

=================================================================  

==8583==ERROR: AddressSanitizer: heap-use-after-free on address 0x60c0000367d8 at pc 0x7fb8c3bb8e3d bp 0x7fff9843c250 sp 0x7fff9843c248  

READ of size 8 at 0x60c0000367d8 thread T0 (chrome)  

#0 0x7fb8c3bb8e3c in contents /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/wtf/RefPtr.h:57  

#1 0x7fb8c327f3c9 in collectScopedStyleFeaturesTo /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/StyleEngine.cpp:660  

#2 0x7fb8c3bde163 in collectFeatures /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/css/resolver/StyleResolver.cpp:303  

#3 0x7fb8c3bdda8a in finishAppendAuthorStyleSheets /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/css/resolver/StyleResolver.cpp:217  

#4 0x7fb8c30e8b7a in ensureResolver /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/StyleEngine.h:145  

#5 0x7fb8c30e787c in updateRenderTree /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/Document.cpp:1812  

#6 0x7fb8c30f1e9a in updateRenderTreeIfNeeded /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/Document.h:469  

#7 0x7fb8c40e6c4e in checkCompleted /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/loader/FrameLoader.cpp:501  

#8 0x7fb8c40e2221 in finishedParsing /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/loader/FrameLoader.cpp:431  

#9 0x7fb8c31191c1 in finishedParsing /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/Document.cpp:4644  

#10 0x7fb8c426f9b7 in end /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/xml/parser/XMLDocumentParser.cpp:436  

#11 0x7fb8c42704bf in finish /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/xml/parser/XMLDocumentParser.cpp:454  

#12 0x7fb8c40d6784 in end /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/loader/DocumentWriter.cpp:120  

#13 0x7fb8c40bd9cc in endWriting /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/loader/DocumentLoader.cpp:795  

#14 0x7fb8c40bd533 in notifyFinished /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/loader/DocumentLoader.cpp:246  

#15 0x7fb8c3e02f50 in checkNotify /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/fetch/Resource.cpp:213  

#16 0x7fb8c3e0427b in finish /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/fetch/Resource.cpp:272  

#17 0x7fb8c3e38de3 in didFinishLoading /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/fetch/ResourceLoader.cpp:450  

#18 0x7fb8c92cd434 in OnCompletedRequest /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../content/child/web\_url\_loader\_impl.cc:808  

#19 0x7fb8c92b1ac4 in OnRequestComplete /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../content/child/resource\_dispatcher.cc:580  

#20 0x7fb8c92accd3 in DispatchToMethodImpl<content::ResourceDispatcher, void (content::ResourceDispatcher::\*)(int, const ResourceMsg\_RequestCompleteData &), int, ResourceMsg\_RequestCompleteData, 0, 1> /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/tuple.h:265  

#21 0x7fb8c92ab458 in OnMessageReceived /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../content/child/resource\_dispatcher.cc:339  

#22 0x7fb8c926d6f2 in OnMessageReceived /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../content/child/child\_thread.cc:479  

#23 0x7fb8c0dbdd99 in OnDispatchMessage /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../ipc/ipc\_channel\_proxy.cc:274  

#24 0x7fb8bfbb15df in Run /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/callback.h:396  

#25 0x7fb8bfaeb84c in RunTask /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/message\_loop/message\_loop.cc:436  

#26 0x7fb8bfaec8c5 in DeferOrRunPendingTask /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/message\_loop/message\_loop.cc:446  

#27 0x7fb8bfaf2f7e in Run /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/message\_loop/message\_pump\_default.cc:32  

#28 0x7fb8bfb1f9a8 in Run /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/run\_loop.cc:55  

#29 0x7fb8bfae9fc6 in base::MessageLoop::Run() /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/message\_loop/message\_loop.cc:298  

#30 0x7fb8c9475423 in RendererMain /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../content/renderer/renderer\_main.cc:235  

#31 0x7fb8bfa59b43 in RunZygote /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../content/app/content\_main\_runner.cc:347  

#32 0x7fb8bfa5bec6 in Run /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../content/app/content\_main\_runner.cc:789  

#33 0x7fb8bfa59178 in ContentMain /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../content/app/content\_main.cc:19  

#34 0x7fb8bebb88d4 in ChromeMain /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../chrome/app/chrome\_main.cc:66  

#35 0x7fb8b4a69ec4 in \_\_libc\_start\_main /build/buildd/eglibc-2.19/csu/libc-start.c:287

0x60c0000367d8 is located 24 bytes inside of 120-byte region [0x60c0000367c0,0x60c000036838)  

freed by thread T0 (chrome) here:  

#0 0x7fb8beb9a2b9 in \_\_interceptor\_free ??:?  

#1 0x7fb8c3285a16 in deref /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/wtf/RefCounted.h:172 (discriminator 2)  

#2 0x7fb8c335a96e in ~TreeScopeStyleSheetCollection /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/TreeScopeStyleSheetCollection.h:48  

#3 0x7fb8c3276581 in deletePtr /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/wtf/OwnPtrCommon.h:52 (discriminator 2)  

#4 0x7fb8c30c6379 in ~Document /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/Document.cpp:609  

#5 0x7fb8c32b065e in ~XMLDocument /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/XMLDocument.h:34  

#6 0x7fb8c224b844 in PostGarbageCollectionProcessing /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/global-handles.cc:272  

#7 0x7fb8c224ad54 in PostGarbageCollectionProcessing /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/global-handles.cc:695  

#8 0x7fb8c229d188 in PerformGarbageCollection /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/heap/heap.cc:1121  

#9 0x7fb8c229beb4 in CollectGarbage /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/heap/heap.cc:844  

#10 0x7fb8c229b75f in CollectGarbage /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/heap/heap-inl.h:583  

#11 0x7fb8c1fc53da in RequestGarbageCollectionForTesting /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/api.cc:6489  

#12 0x7fb8c2b6239e in Call /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/arguments.cc:33  

#13 0x7fb8c204b3df in HandleApiCallHelper<false> /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/builtins.cc:1139  

#14 0x7fb8844071ba (<unknown module>)  

#15 0x7fb8844b6e74 (<unknown module>)  

#16 0x7fb8844b6cfd (<unknown module>)  

#17 0x7fb88443775f (<unknown module>)  

#18 0x7fb884432210 (<unknown module>)  

#14 0x7fb8c21980c4 in Invoke /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/execution.cc:103  

#15 0x7fb8c1f96d5a in Run /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/api.cc:1609  

#16 0x7fb8c4ef3972 in runCompiledScript /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/V8ScriptRunner.cpp:340  

#17 0x7fb8c4e7257a in executeScriptAndReturnValue /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/ScriptController.cpp:202 (discriminator 3)  

#18 0x7fb8c4e6c9ac in execute /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/ScheduledAction.cpp:118  

#19 0x7fb8c3e4865b in fired /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/frame/DOMTimer.cpp:164  

#20 0x7fb8cae0beeb in sharedTimerFiredInternal /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/platform/ThreadTimers.cpp:137  

#21 0x7fb8cae0b721 in sharedTimerFired /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/platform/ThreadTimers.cpp:107  

#22 0x7fb8bfb7d1ce in Run /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/callback.h:396  

#23 0x7fb8bfbb15df in Run /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/callback.h:396  

#24 0x7fb8bfaeb84c in RunTask /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/message\_loop/message\_loop.cc:436

previously allocated by thread T0 (chrome) here:  

#0 0x7fb8beb9a579 in \_\_interceptor\_malloc ??:?  

#1 0x7fb8c1e83344 in partitionAllocGenericFlags /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/wtf/PartitionAlloc.h:541  

#2 0x7fb8c39ce6f4 in operator new /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/wtf/RefCounted.h:166  

#3 0x7fb8c327e8d8 in parseSheet /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/StyleEngine.cpp:633  

#4 0x7fb8c327de8f in createSheet /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/StyleEngine.cpp:608  

#5 0x7fb8cb1dcc3f in createSheet /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/StyleElement.cpp:196  

#6 0x7fb8cb1db711 in process /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/StyleElement.cpp:144  

#7 0x7fb8c30a2ff1 in notifyNodeInserted /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/ContainerNode.cpp:782  

#8 0x7fb8c30a029f in updateTreeAfterInsertion /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/ContainerNode.cpp:1181  

#9 0x7fb8c309d957 in appendChild /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/ContainerNode.cpp:733  

#10 0x7fb8c31d8cd0 in appendChild /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/Node.cpp:492  

#11 0x7fb8c563a344 in appendChildMethodForMainWorld /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/gen/blink/bindings/core/v8/V8Node.cpp:651  

#12 0x7fb8c2b6239e in Call /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/arguments.cc:33  

#13 0x7fb8c204b3df in HandleApiCallHelper<false> /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/builtins.cc:1139  

#14 0x7fb8844071ba (<unknown module>)  

#15 0x7fb884487e9f (<unknown module>)  

#16 0x7fb884487cfc (<unknown module>)  

#17 0x7fb88443775f (<unknown module>)  

#18 0x7fb884432210 (<unknown module>)  

#14 0x7fb8c21980c4 in Invoke /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/execution.cc:103  

#15 0x7fb8c1fb6116 in Call /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/api.cc:4170  

#16 0x7fb8c4ef48cf in callFunction /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/V8ScriptRunner.cpp:387  

#17 0x7fb8c4e71983 in callFunction /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/ScriptController.cpp:170  

#18 0x7fb8c4e7112a in callFunction /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/ScriptController.cpp:154 (discriminator 3)  

#19 0x7fb8c4ed82a2 in callListenerFunction /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/V8LazyEventListener.cpp:99  

#20 0x7fb8c4eb250b in invokeEventHandler /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/V8AbstractEventListener.cpp:128  

#21 0x7fb8c4eb1ecc in handleEvent /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/V8AbstractEventListener.cpp:98  

#22 0x7fb8c4ed84f7 in handleEvent /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/V8LazyEventListener.cpp:117  

#23 0x7fb8c32fec87 in fireEventListeners /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/events/EventTarget.cpp:352  

#24 0x7fb8c32fd8ab in fireEventListeners /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/events/EventTarget.cpp:288

SUMMARY: AddressSanitizer: heap-use-after-free ??:0 ??  

Shadow bytes around the buggy address:  

0x0c187fffeca0: fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa fa  

0x0c187fffecb0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fa  

0x0c187fffecc0: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd  

0x0c187fffecd0: fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa fa  

0x0c187fffece0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fa  

=>0x0c187fffecf0: fa fa fa fa fa fa fa fa fd fd fd[fd]fd fd fd fd  

0x0c187fffed00: fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa fa  

0x0c187fffed10: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fa  

0x0c187fffed20: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd  

0x0c187fffed30: fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa fa  

0x0c187fffed40: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fa  

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

==8583==ABORTING

**VERSION**  

Chrome Version: asan-linux-release-308523

**REPRODUCTION CASE**  

Attached.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab

## Attachments

- [crash.zip](attachments/crash.zip) (application/zip, 903 B)

## Timeline

### cl...@chromium.org (2014-12-17)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5644891680931840

### in...@chromium.org (2014-12-17)

This looks like incorrectly closed https://code.google.com/p/chromium/issues/detail?id=434970. Kochi@, this repro looks reliable, can you please take a look.

### in...@chromium.org (2014-12-17)

Or might be similar to https://code.google.com/p/chromium/issues/detail?id=434970

### cl...@chromium.org (2014-12-17)

[Empty comment from Monorail migration]

### ta...@chromium.org (2014-12-17)

Looking.


### cl...@chromium.org (2014-12-17)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5644891680931840

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x61000006c798
Crash State:
  blink::ScopedStyleResolver::collectFeaturesTo
  blink::StyleEngine::collectScopedStyleFeaturesTo
  blink::StyleResolver::collectFeatures
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=305804:305808

Minimized Testcase (0.78 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94WWg0QYPDDzA5l3JWp-MWksbjULuqiO4jAqBzZZkHHvzRpkeoQ70BXbGEcLz1cEsXJ3DlMAl6Kc7T390kvf8JrIivM3ZxGs9WB9OuPTD_QS01Dz3e3j7Alf0tgwruu9UaCzVuyL-ITsEcofx1iJ5cvaOxsLQ

Additional requirements: Requires HTTP



### cl...@chromium.org (2014-12-17)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-12-17)

This medium+ severity security issue is a regression on trunk.

Please fix this asap. If you are unable to look into this soon, please revert your change.

- Your friendly ClusterFuzz

### ko...@chromium.org (2014-12-17)

Is this blocking Beta of M41 or Beta of M40?
(in either case tasak or I will look into this immediately)

### in...@chromium.org (2014-12-17)

As per CF, it regressed with this change below. So, only impacts M41 trunk, hence blocks M41 beta.

Author: tasak@google.com 
Component: blink
Changelist: https://chromium.googlesource.com/chromium/blink.git/+/26e77ca299af020de3a4a68bf3e2bfef41562140
Time: Wed Nov 26 10:37:16 2014
Lines 652-653 of file StyleEngine.cpp which potentially caused crash are changed in this cl (frame #5, "blink::StyleEngine::parseSheet").

Lines 106 of file StyleEngine.cpp which potentially caused crash are changed in this cl (frame #9, "blink::StyleEngine::detachFromDocument").
Minimum distance from crash line to modified line: 0. (file: StyleEngine.cpp, crashed on: 652, modified: 652).

### ko...@chromium.org (2014-12-18)

Hmm, the CL is merged to M40, so it also should block M40, then.

### in...@chromium.org (2014-12-18)

Ok thanks!, fixing flags.

### in...@chromium.org (2014-12-18)

might be correlated to https://code.google.com/p/chromium/issues/detail?id=443675. if that is a dupe, then please dupe that one out.

### ko...@chromium.org (2014-12-19)

tasak@'s CL https://codereview.chromium.org/809343002/ is under review.
It didn't fix https://crbug.com/chromium/443675 so 443675 is a different issue (unfortunately).


### bu...@chromium.org (2014-12-22)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=187602

------------------------------------------------------------------
r187602 | tasak@google.com | 2014-12-22T05:19:21.169684Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/html/resources/marquee-crash.svg?r1=187602&r2=187601&pathrev=187602
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/dom/shadow/ShadowRoot.cpp?r1=187602&r2=187601&pathrev=187602
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/html/marquee-clone-crash-expected.txt?r1=187602&r2=187601&pathrev=187602
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/html/marquee-clone-crash.html?r1=187602&r2=187601&pathrev=187602
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/css/resolver/StyleResolver.cpp?r1=187602&r2=187601&pathrev=187602

ScopedStyleResolver should be cleared when ShadowRoot is removed from document.

If a shadow root (=treescope), which has a style element, is moved from a document to another document, a new ShadowStyleSheetCollection is created for the shadow root.

The ShadowStyleSheetCollection has no active stylesheets, but the treescope's scopedStyleResolver has an active stylesheet.

The active stylesheet has been already cleared (i.e. clearOwnerNode is invoked) while moving.
However, StyleEngine cannot clear the treescope's resolver, because the ShadowStyleSheetCollection has no information. This causes heap-use-after-free.

BUG=443017
TEST=fast/html/marquee-clone-crash.html

Review URL: https://codereview.chromium.org/809343002
-----------------------------------------------------------------

### ko...@chromium.org (2014-12-22)

Requesting merge for M40 (will wait for some bake time).

### ko...@chromium.org (2014-12-22)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-12-22)

[Empty comment from Monorail migration]

### ma...@google.com (2014-12-23)

Approved for M40 (branch: 2214)

### cl...@chromium.org (2014-12-23)

ClusterFuzz has detected this issue as fixed in range 309395:309411.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5644891680931840

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x61000006c798
Crash State:
  blink::ScopedStyleResolver::collectFeaturesTo
  blink::StyleEngine::collectScopedStyleFeaturesTo
  blink::StyleResolver::collectFeatures
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=305804:305808
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=309395:309411

Minimized Testcase (0.78 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94WWg0QYPDDzA5l3JWp-MWksbjULuqiO4jAqBzZZkHHvzRpkeoQ70BXbGEcLz1cEsXJ3DlMAl6Kc7T390kvf8JrIivM3ZxGs9WB9OuPTD_QS01Dz3e3j7Alf0tgwruu9UaCzVuyL-ITsEcofx1iJ5cvaOxsLQ

Additional requirements: Requires HTTP

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### bu...@chromium.org (2014-12-24)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=187669

------------------------------------------------------------------
r187669 | kochi@chromium.org | 2014-12-24T02:02:46.172914Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/branches/chromium/2214/Source/core/css/resolver/StyleResolver.cpp?r1=187669&r2=187668&pathrev=187669
   A http://src.chromium.org/viewvc/blink/branches/chromium/2214/LayoutTests/fast/html/resources/marquee-crash.svg?r1=187669&r2=187668&pathrev=187669
   M http://src.chromium.org/viewvc/blink/branches/chromium/2214/Source/core/dom/shadow/ShadowRoot.cpp?r1=187669&r2=187668&pathrev=187669
   A http://src.chromium.org/viewvc/blink/branches/chromium/2214/LayoutTests/fast/html/marquee-clone-crash-expected.txt?r1=187669&r2=187668&pathrev=187669
   A http://src.chromium.org/viewvc/blink/branches/chromium/2214/LayoutTests/fast/html/marquee-clone-crash.html?r1=187669&r2=187668&pathrev=187669

Merge 187602 "ScopedStyleResolver should be cleared when ShadowR..."

> ScopedStyleResolver should be cleared when ShadowRoot is removed from document.
> 
> If a shadow root (=treescope), which has a style element, is moved from a document to another document, a new ShadowStyleSheetCollection is created for the shadow root.
> 
> The ShadowStyleSheetCollection has no active stylesheets, but the treescope's scopedStyleResolver has an active stylesheet.
> 
> The active stylesheet has been already cleared (i.e. clearOwnerNode is invoked) while moving.
> However, StyleEngine cannot clear the treescope's resolver, because the ShadowStyleSheetCollection has no information. This causes heap-use-after-free.
> 
> BUG=443017
> TEST=fast/html/marquee-clone-crash.html
> 
> Review URL: https://codereview.chromium.org/809343002

TBR=tasak@google.com

Review URL: https://codereview.chromium.org/821093008
-----------------------------------------------------------------

### in...@chromium.org (2014-12-24)

[Empty comment from Monorail migration]

### ti...@google.com (2015-01-22)

Congrats - $3000 for this report.

### ti...@google.com (2015-03-09)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-03-30)

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

This issue was migrated from crbug.com/chromium/443017?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081029)*
