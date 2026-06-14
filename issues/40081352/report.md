# Heap-use-after-free in blink::PendingScript::stopWatchingForLoad

| Field | Value |
|-------|-------|
| **Issue ID** | [40081352](https://issues.chromium.org/issues/40081352) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Reporter** | cl...@gmail.com |
| **Assignee** | ma...@chromium.org |
| **Created** | 2015-02-06 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

The following testcase crashes the latest chrome ASAN build. It crashes reliably with --js-flags=--expose-gc :

=================================================================  

==6026==ERROR: AddressSanitizer: heap-use-after-free on address 0x60b000011a60 at pc 0x7f7559b54c72 bp 0x7fff801a4f60 sp 0x7fff801a4f58  

READ of size 1 at 0x60b000011a60 thread T0 (chrome)  

#0 0x7f7559b54c71 in stopWatchingForLoad /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/PendingScript.cpp:94  

#1 0x7f7559b585fe in detach /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/ScriptLoader.cpp:116  

#2 0x7f7559a5b200 in ~ScriptRunner /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/ScriptRunner.cpp:52  

#3 0x7f75598cd638 in deletePtr /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/wtf/OwnPtrCommon.h:52 (discriminator 21)  

#4 0x7f7559e3828e in ~HTMLDocument /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/html/HTMLDocument.cpp:82  

#5 0x7f7558ab8399 in PostGarbageCollectionProcessing /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/global-handles.cc:330  

#6 0x7f7558ab896c in PostMarkSweepProcessing /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/global-handles.cc:806  

#7 0x7f7558afe081 in PerformGarbageCollection /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/heap/heap.cc:1143  

#8 0x7f7558afcc47 in CollectGarbage /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/heap/heap.cc:853  

#9 0x7f7558afc49f in CollectGarbage /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/heap/heap-inl.h:583  

#10 0x7f75588888b0 in RequestGarbageCollectionForTesting /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/api.cc:6404  

#11 0x7f75593804a4 in Call /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/arguments.cc:33  

#12 0x7f75588f4ded in HandleApiCallHelper<false> /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/builtins.cc:1076  

#13 0x7f75588fdea5 in Builtin\_implHandleApiCall /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/builtins.cc:1099 (discriminator 1)  

#14 0x7f751a40615a (<unknown module>)  

#15 0x7f751a477bf9 (<unknown module>)  

#16 0x7f751a477adc (<unknown module>)  

#17 0x7f751a435dff (<unknown module>)  

#18 0x7f751a417d10 (<unknown module>)  

#14 0x7f7558a38eb2 in Invoke /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/execution.cc:128  

#15 0x7f7558879cb4 in Call /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/api.cc:4088  

#16 0x7f755b9fe45f in callFunction /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/V8ScriptRunner.cpp:463  

#17 0x7f755b97af73 in callFunction /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/ScriptController.cpp:164  

#18 0x7f755b97a648 in callFunction /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/ScriptController.cpp:148  

#19 0x7f755b9e2469 in callListenerFunction /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/V8LazyEventListener.cpp:99  

#20 0x7f755b9bb9fa in invokeEventHandler /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/V8AbstractEventListener.cpp:125  

#21 0x7f755b9bb436 in handleEvent /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/V8AbstractEventListener.cpp:100  

#22 0x7f755b9bb0e2 in handleEvent /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/V8AbstractEventListener.cpp:85  

#23 0x7f7559b03f17 in fireEventListeners /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/events/EventTarget.cpp:376  

#24 0x7f7559b02b3b in fireEventListeners /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/events/EventTarget.cpp:312  

#25 0x7f755a95e83f in dispatchEvent /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/frame/LocalDOMWindow.cpp:1589  

#26 0x7f755a95c6ff in dispatchLoadEvent /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/frame/LocalDOMWindow.cpp:1557  

#27 0x7f755a95d3d4 in dispatchWindowLoadEvent /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/frame/LocalDOMWindow.cpp:498  

#28 0x7f75598fa58a in implicitClose /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/Document.cpp:2515  

#29 0x7f755abbf47d in checkCompleted /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/loader/FrameLoader.cpp:494  

#30 0x7f755abbeff1 in finishedParsing /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/loader/FrameLoader.cpp:410  

#31 0x7f7559920b87 in finishedParsing /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/Document.cpp:4569  

#32 0x7f755a0c0a97 in end /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:852  

#33 0x7f755a0c6d28 in processParsedChunkFromBackgroundParser /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:506  

#34 0x7f755a0c2d0b in pumpPendingSpeculations /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:561  

#35 0x7f755a0c2360 in resumeParsingAfterYield /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:303  

#36 0x7f7561f4056b in sharedTimerFiredInternal /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/platform/ThreadTimers.cpp:137  

#37 0x7f7561f3fda1 in sharedTimerFired /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/platform/ThreadTimers.cpp:107  

#38 0x7f755684cc8e in Run /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/callback.h:396  

#39 0x7f75568aa0e4 in Run /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/callback.h:396  

#40 0x7f755ea7c6f8 in ProcessTaskFromWorkQueue /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../content/renderer/scheduler/task\_queue\_manager.cc:416  

#41 0x7f75568aa0e4 in Run /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/callback.h:396  

#42 0x7f75567bb65c in RunTask /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/message\_loop/message\_loop.cc:443  

#43 0x7f75567bc617 in DeferOrRunPendingTask /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/message\_loop/message\_loop.cc:453  

#44 0x7f75567c2afe in Run /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/message\_loop/message\_pump\_default.cc:32  

#45 0x7f75567efe18 in Run /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/run\_loop.cc:55  

#46 0x7f75567b9e76 in base::MessageLoop::Run() /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/message\_loop/message\_loop.cc:302  

#47 0x7f755ea69632 in RendererMain /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../content/renderer/renderer\_main.cc:228  

#48 0x7f75567515e3 in RunZygote /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../content/app/content\_main\_runner.cc:347  

#49 0x7f75567539a6 in Run /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../content/app/content\_main\_runner.cc:803  

#50 0x7f7556750c18 in ContentMain /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../content/app/content\_main.cc:19  

#51 0x7f75558bae14 in ChromeMain /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../chrome/app/chrome\_main.cc:66  

#52 0x7f754b6dfec4 in \_\_libc\_start\_main /build/buildd/eglibc-2.19/csu/libc-start.c:287

0x60b000011a60 is located 64 bytes inside of 104-byte region [0x60b000011a20,0x60b000011a88)  

freed by thread T0 (chrome) here:  

#0 0x7f75558ba449 in operator delete(void\*) ??:?  

#1 0x7f755a30aa71 in deletePtr /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/wtf/OwnPtrCommon.h:52 (discriminator 1)  

#2 0x7f75598a1043 in removeDetachedChildrenInContainer /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/ContainerNode.cpp:468 (discriminator 1)  

#3 0x7f75598d1bc7 in dispose /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/Document.cpp:627  

#4 0x7f75599f63e7 in removedLastRefToScope /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/Node.cpp:2205  

#5 0x7f7559aa1327 in destruct /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/wtf/Vector.h:64  

#6 0x7f7559ae87a6 in deletePtr /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/wtf/OwnPtrCommon.h:52 (discriminator 1)  

#7 0x7f7559ae8bda in ~Event /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/events/Event.cpp:72  

#8 0x7f7558ab8399 in PostGarbageCollectionProcessing /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/global-handles.cc:330  

#9 0x7f7558ab896c in PostMarkSweepProcessing /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/global-handles.cc:806  

#10 0x7f7558afe081 in PerformGarbageCollection /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/heap/heap.cc:1143  

#11 0x7f7558afcc47 in CollectGarbage /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/heap/heap.cc:853  

#12 0x7f7558afc49f in CollectGarbage /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/heap/heap-inl.h:583  

#13 0x7f75588888b0 in RequestGarbageCollectionForTesting /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/api.cc:6404  

#14 0x7f75593804a4 in Call /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/arguments.cc:33  

#15 0x7f75588f4ded in HandleApiCallHelper<false> /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/builtins.cc:1076  

#16 0x7f75588fdea5 in Builtin\_implHandleApiCall /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/builtins.cc:1099 (discriminator 1)  

#17 0x7f751a40615a (<unknown module>)  

#18 0x7f751a477bf9 (<unknown module>)  

#19 0x7f751a477adc (<unknown module>)  

#20 0x7f751a435dff (<unknown module>)  

#21 0x7f751a417d10 (<unknown module>)  

#17 0x7f7558a38eb2 in Invoke /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/execution.cc:128  

#18 0x7f7558879cb4 in Call /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/api.cc:4088  

#19 0x7f755b9fe45f in callFunction /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/V8ScriptRunner.cpp:463  

#20 0x7f755b97af73 in callFunction /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/ScriptController.cpp:164  

#21 0x7f755b97a648 in callFunction /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/ScriptController.cpp:148  

#22 0x7f755b9e2469 in callListenerFunction /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/V8LazyEventListener.cpp:99  

#23 0x7f755b9bb9fa in invokeEventHandler /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/V8AbstractEventListener.cpp:125  

#24 0x7f755b9bb436 in handleEvent /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/V8AbstractEventListener.cpp:100

previously allocated by thread T0 (chrome) here:  

#0 0x7f75558b9ec9 in operator new(unsigned long) ??:?  

#1 0x7f755a305bdd in create /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/ScriptLoader.h:43  

#2 0x7f755c25919f in scriptConstructor /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/gen/blink/core/HTMLElementFactory.cpp:1006  

#3 0x7f755c24fc51 in createHTMLElement /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/gen/blink/core/HTMLElementFactory.cpp:1250  

#4 0x7f75598d41b4 in createElement /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/Document.cpp:741  

#5 0x7f755c052671 in createElement1MethodForMainWorld /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/gen/blink/bindings/core/v8/V8Document.cpp:3634  

#6 0x7f75593804a4 in Call /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/arguments.cc:33  

#7 0x7f75588f4ded in HandleApiCallHelper<false> /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/builtins.cc:1076  

#8 0x7f75588fdea5 in Builtin\_implHandleApiCall /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/builtins.cc:1099 (discriminator 1)  

#9 0x7f751a40615a (<unknown module>)  

#10 0x7f751a46cb04 (<unknown module>)  

#11 0x7f751a46c95c (<unknown module>)  

#12 0x7f751a435dff (<unknown module>)  

#13 0x7f751a417d10 (<unknown module>)  

#9 0x7f7558a38eb2 in Invoke /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/execution.cc:128  

#10 0x7f7558879cb4 in Call /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/api.cc:4088  

#11 0x7f755b9fe45f in callFunction /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/V8ScriptRunner.cpp:463  

#12 0x7f755b97af73 in callFunction /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/ScriptController.cpp:164  

#13 0x7f755b97a648 in callFunction /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/ScriptController.cpp:148  

#14 0x7f755b9e2469 in callListenerFunction /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/V8LazyEventListener.cpp:99  

#15 0x7f755b9bb9fa in invokeEventHandler /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/V8AbstractEventListener.cpp:125  

#16 0x7f755b9bb436 in handleEvent /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/V8AbstractEventListener.cpp:100  

#17 0x7f755b9bb0e2 in handleEvent /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/V8AbstractEventListener.cpp:85  

#18 0x7f7559b03f17 in fireEventListeners /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/events/EventTarget.cpp:376  

#19 0x7f7559b02b3b in fireEventListeners /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/events/EventTarget.cpp:312  

#20 0x7f755a95e83f in dispatchEvent /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/frame/LocalDOMWindow.cpp:1589  

#21 0x7f755a95c6ff in dispatchLoadEvent /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/frame/LocalDOMWindow.cpp:1557  

#22 0x7f755a95d3d4 in dispatchWindowLoadEvent /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/frame/LocalDOMWindow.cpp:498  

#23 0x7f75598fa58a in implicitClose /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/Document.cpp:2515  

#24 0x7f755abbf47d in checkCompleted /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/loader/FrameLoader.cpp:494

SUMMARY: AddressSanitizer: heap-use-after-free ??:0 ??  

Shadow bytes around the buggy address:  

0x0c167fffa2f0: fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa  

0x0c167fffa300: fa fa fd fd fd fd fd fd fd fd fd fd fd fd fd fa  

0x0c167fffa310: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd  

0x0c167fffa320: fd fd fd fd fd fd fa fa fa fa fa fa fa fa fd fd  

0x0c167fffa330: fd fd fd fd fd fd fd fd fd fd fd fa fa fa fa fa  

=>0x0c167fffa340: fa fa fa fa fd fd fd fd fd fd fd fd[fd]fd fd fd  

0x0c167fffa350: fd fa fa fa fa fa fa fa fa fa 00 00 00 00 00 00  

0x0c167fffa360: 00 00 00 00 00 00 00 00 fa fa fa fa fa fa fa fa  

0x0c167fffa370: fd fd fd fd fd fd fd fd fd fd fd fd fd fa fa fa  

0x0c167fffa380: fa fa fa fa fa fa fd fd fd fd fd fd fd fd fd fd  

0x0c167fffa390: fd fd fd fa fa fa fa fa fa fa fa fa fd fd fd fd  

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

==6026==ABORTING

**VERSION**  

Chrome Version: asan-linux-release-314508  

Operating System: Linux 64bit

**REPRODUCTION CASE**

<script>
function start() {
if(gc)gc();
o94=document.body;
o2510=document.createElement('script');
o2510.src=null;
o2518=document.createElement('b');
o2518.appendChild(o94);
o2672=document.documentElement;
o2775=document.createElement('iframe');
o2775.onload=cb\_nodeiframes\_1523\_1;
o2672.appendChild(o2775)
}
function cb\_nodeiframes\_1523\_1() {
o2777=this.contentDocument;
o2810=document.documentElement;
o2814=document.createElement('iframe');
o2814.onload=cb\_nodeiframes\_1645\_1;
o2810.appendChild(o2814)
}
function cb\_nodeiframes\_1645\_1() {
o2845=document.createElement('li');
o94.appendChild(o2845)
o2864=o2777.implementation.createDocument('','b',null);
o2867=o2864.implementation.createDocument('','a',null);
o2884=o2867.createElement('div');
o94.appendChild(o2510);
o2884.appendChild(o94.parentNode);
o3028=o2845.cloneNode(true);
o2814.appendChild(o94);
o3028.appendChild(o94);
o2814.appendChild(o2510);
gc();
location.reload(true);
}
</script>
<body onload="start()"></body>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab

## Timeline

### cl...@chromium.org (2015-02-06)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=4859876961419264

### cl...@chromium.org (2015-02-06)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-02-06)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4859876961419264

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 1
Crash Address: 0x60f000010b00
Crash State:
  blink::PendingScript::stopWatchingForLoad
  blink::ScriptLoader::detach
  blink::ScriptRunner::~ScriptRunner
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=300226:300272

Minimized Testcase (0.95 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96yfyScirf58nxuaklQhEBHn4XeMSy9VUIC0VJmUUuRDWBjNgkuA7bbjq-Fnq04IdKU3n3IMeI3OO0ZEVfOttrSiNLFsxiEOkqlsZXWEtUDIRWWSqSicJGfIpDYUs8MfY4MUsXNAkGheRIYmdtSfoI5kvOW0A



### js...@chromium.org (2015-02-06)

Assigning to marja based on blamelist.

### cl...@chromium.org (2015-02-07)

[Empty comment from Monorail migration]

### ma...@chromium.org (2015-02-09)

sigbjornf@, this seems to be script moving stuff again. :/

I think we should make these ASSERTS

ASSERT(m_pendingAsyncScripts.contains(scriptLoader));

RELEASE_ASSERTs instead...

### ma...@chromium.org (2015-02-09)

More information: The script handling seems to be pretty confused here o.O

Heres' a log of what happens:

ScriptRunner ctor RUNNER1
ScriptRunner ctor RUNNER2
ScriptRunner ctor RUNNER3
movePendingAsyncScript RUNNER1 LOADER RUNNER2 << huh??
not found
movePendingAsyncScript RUNNER3 LOADER RUNNER1 << huh??
not found
addPendingAsyncScript RUNNER1 LOADER << ok
movePendingAsyncScript RUNNER1 LOADER RUNNER2 << ok
found
addPendingAsyncScript RUNNER2 LOADER << huh?? it's already moved there!
movePendingAsyncScript RUNNER3 LOADER RUNNER1 << huh??
not found
notifyScriptLoadError RUNNER1 LOADER << huh?? it's already moved away
-> ASSERT fails


### ma...@chromium.org (2015-02-09)

Oops, this line is actually sane:

addPendingAsyncScript RUNNER2 LOADER << huh?? it's already moved there!

because that's called from movePendingAsyncScript. So it's only the moving which is confused... trying to move scripts which are not there.

### ma...@chromium.org (2015-02-09)

Afaics, this is the minimal repro case:

<script>
function start() {
if(gc)gc();
document_body=document.body;
teh_script_element=document.createElement('script');
teh_script_element.src=null;
document_body.appendChild(teh_script_element);
new_iframe=document.createElement('iframe');
document.documentElement.appendChild(new_iframe)
newdoc=document.implementation.createDocument('','a',null);
div_element=newdoc.createElement('div');
div_element.appendChild(document_body);
new_iframe.appendChild(teh_script_element);
location.reload(true);
}
</script>
<body onload="start()"></body>

### ma...@chromium.org (2015-02-09)

More information:

1) the repro case in https://crbug.com/chromium/456059#c9 is not exactly same than the original bug, but I think it's a minimal case where we're confused b/c of script moving.

2) what seems to happen is that when we move the script to newdoc, the contextDocument is still the same as the old document, and we end up not moving the script at all (instead, we remove it... oops.)

3) However, the confusion in the original fuzz case is more complicated, and the trivial fix ("don't try to move from scriptrunner to itself") doesn't help.

### bu...@chromium.org (2015-02-10)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=189886

------------------------------------------------------------------
r189886 | marja@chromium.org | 2015-02-10T11:36:10.507717Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/dom/ScriptRunner.h?r1=189886&r2=189885&pathrev=189886
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/dom/HTMLScriptElement/resources/move-back-from-non-contextdoc.svg?r1=189886&r2=189885&pathrev=189886
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/dom/HTMLScriptElement/script-moving-from-non-contextdoc-expected.txt?r1=189886&r2=189885&pathrev=189886
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/html/HTMLScriptElement.cpp?r1=189886&r2=189885&pathrev=189886
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/dom/HTMLScriptElement/resources/move-back-from-non-contextdoc.html?r1=189886&r2=189885&pathrev=189886
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/dom/HTMLScriptElement/resources/move-from-non-contextdoc-to-iframe.html?r1=189886&r2=189885&pathrev=189886
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/dom/HTMLScriptElement/script-moving-from-non-contextdoc.html?r1=189886&r2=189885&pathrev=189886
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/dom/ScriptRunner.cpp?r1=189886&r2=189885&pathrev=189886
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/svg/SVGScriptElement.cpp?r1=189886&r2=189885&pathrev=189886

Script moving fixes related to context documents.

There were 2 bugs:

1) Moving script element to a new document whose context document is the same as
the current document: we ended up doing ScriptRunner::movePendingAsyncScript to
itself and that does the wrong thing (just removes the script).

2) Moving script element to a new document which is not its own context
document, and then moving it somewhere else. The script was not where we
expected it to be (it was in the context document, we expected it to be in the
non-context document).

BUG=456059

Review URL: https://codereview.chromium.org/913473002
-----------------------------------------------------------------

### ma...@chromium.org (2015-02-10)

Will need to request a merge once this has been on Canary for some days.

### cl...@chromium.org (2015-02-10)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### cl...@chromium.org (2015-02-11)

ClusterFuzz has detected this issue as fixed in range 315522:315577.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4859876961419264

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 1
Crash Address: 0x60f000010b00
Crash State:
  blink::PendingScript::stopWatchingForLoad
  blink::ScriptLoader::detach
  blink::ScriptRunner::~ScriptRunner
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=300226:300272
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=315522:315577

Minimized Testcase (0.95 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96yfyScirf58nxuaklQhEBHn4XeMSy9VUIC0VJmUUuRDWBjNgkuA7bbjq-Fnq04IdKU3n3IMeI3OO0ZEVfOttrSiNLFsxiEOkqlsZXWEtUDIRWWSqSicJGfIpDYUs8MfY4MUsXNAkGheRIYmdtSfoI5kvOW0A

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### ma...@chromium.org (2015-02-12)

Merge to M40 and M41?

(Hmm, I guess I should set this as not-fixed for the merge, right?)

### pe...@google.com (2015-02-12)

[Automated comment] Request affecting a post-stable build (M40), manual review required.

### pe...@google.com (2015-02-12)

Approved for M41 (branch: 2272)

### bu...@chromium.org (2015-02-12)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=190043

------------------------------------------------------------------
r190043 | marja@chromium.org | 2015-02-12T11:46:55.818462Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/branches/chromium/2272/Source/core/dom/ScriptRunner.h?r1=190043&r2=190042&pathrev=190043
   A http://src.chromium.org/viewvc/blink/branches/chromium/2272/LayoutTests/fast/dom/HTMLScriptElement/resources/move-back-from-non-contextdoc.svg?r1=190043&r2=190042&pathrev=190043
   A http://src.chromium.org/viewvc/blink/branches/chromium/2272/LayoutTests/fast/dom/HTMLScriptElement/script-moving-from-non-contextdoc-expected.txt?r1=190043&r2=190042&pathrev=190043
   M http://src.chromium.org/viewvc/blink/branches/chromium/2272/Source/core/html/HTMLScriptElement.cpp?r1=190043&r2=190042&pathrev=190043
   A http://src.chromium.org/viewvc/blink/branches/chromium/2272/LayoutTests/fast/dom/HTMLScriptElement/resources/move-back-from-non-contextdoc.html?r1=190043&r2=190042&pathrev=190043
   A http://src.chromium.org/viewvc/blink/branches/chromium/2272/LayoutTests/fast/dom/HTMLScriptElement/resources/move-from-non-contextdoc-to-iframe.html?r1=190043&r2=190042&pathrev=190043
   A http://src.chromium.org/viewvc/blink/branches/chromium/2272/LayoutTests/fast/dom/HTMLScriptElement/script-moving-from-non-contextdoc.html?r1=190043&r2=190042&pathrev=190043
   M http://src.chromium.org/viewvc/blink/branches/chromium/2272/Source/core/dom/ScriptRunner.cpp?r1=190043&r2=190042&pathrev=190043
   M http://src.chromium.org/viewvc/blink/branches/chromium/2272/Source/core/svg/SVGScriptElement.cpp?r1=190043&r2=190042&pathrev=190043

Merge 189886 "Script moving fixes related to context documents."

> Script moving fixes related to context documents.
> 
> There were 2 bugs:
> 
> 1) Moving script element to a new document whose context document is the same as
> the current document: we ended up doing ScriptRunner::movePendingAsyncScript to
> itself and that does the wrong thing (just removes the script).
> 
> 2) Moving script element to a new document which is not its own context
> document, and then moving it somewhere else. The script was not where we
> expected it to be (it was in the context document, we expected it to be in the
> non-context document).
> 
> BUG=456059
> 
> Review URL: https://codereview.chromium.org/913473002

TBR=marja@chromium.org

Review URL: https://codereview.chromium.org/915413002
-----------------------------------------------------------------

### in...@chromium.org (2015-02-12)

[Empty comment from Monorail migration]

### pe...@chromium.org (2015-02-12)

[Empty comment from Monorail migration]

### in...@chromium.org (2015-02-12)

[Empty comment from Monorail migration]

### ti...@google.com (2015-02-17)

inferno: is there a reason why the merge triage label is still on this bug? #18 has a merge to M41 (2272) so I think we can remove the "merge-triage" label, though I see you explicitly added it in #21 so want to double check.

### in...@chromium.org (2015-02-17)

[Empty comment from Monorail migration]

### ma...@chromium.org (2015-02-18)

This is not yet merged to M40 - should it be? I thought the Merge-Triage label was here because of that...

### in...@chromium.org (2015-02-18)

We are only taking security merges for upcoming M-41.

### ti...@google.com (2015-02-26)

[Empty comment from Monorail migration]

### ti...@google.com (2015-03-03)

Congratulations - $3000 for this report.

Notes from panel: Not convinced that there is control between use and free.

### ti...@google.com (2015-03-09)

[Empty comment from Monorail migration]

### ti...@google.com (2015-04-07)

Processing via our e-payment system can take up to six weeks, but the reward should be on its way to you. Thanks again for your help!

### cl...@chromium.org (2015-05-21)

Bulk update: removing view restriction from closed bugs.

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

This issue was migrated from crbug.com/chromium/456059?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081352)*
