# Heap-use-after-free in blink::V8PerContextData::constructorForTypeSlowCase

| Field | Value |
|-------|-------|
| **Issue ID** | [40081176](https://issues.chromium.org/issues/40081176) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Bindings |
| **Reporter** | cl...@gmail.com |
| **Assignee** | dc...@chromium.org |
| **Created** | 2015-01-13 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

The attached testcase crashes the latest asan build and the stable release build of Chrome. The freed buffer is not protected by PartitionAlloc and Javascript code execution is possible between the free and the use.

ASAN output:

=================================================================  

==28305==ERROR: AddressSanitizer: heap-use-after-free on address 0x61000001ce68 at pc 0x7fa53275dbe2 bp 0x7fffab4fdc90 sp 0x7fffab4fdc88  

READ of size 8 at 0x61000001ce68 thread T0 (chrome)  

#0 0x7fa53275dbe1 in Get /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/include/v8-util.h:141  

#1 0x7fa53275d5a7 in constructorForType /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/V8PerContextData.h:84 (discriminator 1)  

#2 0x7fa53273a73c in createWrapperFromCache /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/V8PerContextData.h:78 (discriminator 1)  

#3 0x7fa5309588f3 in wrap /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/Document.cpp:5680  

#4 0x7fa53277bc55 in toV8 /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/ToV8.h:43  

#5 0x7fa53277a6a2 in updateDocument /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/WindowProxy.cpp:435  

#6 0x7fa5316d86a8 in installNewDocument /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/frame/LocalDOMWindow.cpp:451  

#7 0x7fa53191b994 in createWriterFor /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/loader/DocumentLoader.cpp:809  

#8 0x7fa53191b3b5 in ensureWriter /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/loader/DocumentLoader.cpp:525  

#9 0x7fa53191c23d in commitData /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/loader/DocumentLoader.cpp:539  

#10 0x7fa531d60318 in appendData /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/fetch/RawResource.cpp:48  

#11 0x7fa531678459 in didReceiveData /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/fetch/ResourceLoader.cpp:431  

#12 0x7fa536d69f63 in OnReceivedData /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../content/child/web\_url\_loader\_impl.cc:706  

#13 0x7fa536d4f14f in OnReceivedData /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../content/child/resource\_dispatcher.cc:489  

#14 0x7fa536d4bb3c in DispatchToMethodImpl<content::ResourceDispatcher, void (content::ResourceDispatcher::\*)(int, int, int, int), int, int, int, int, 0, 1, 2, 3> /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/tuple.h:200  

#15 0x7fa536d4a368 in OnMessageReceived /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../content/child/resource\_dispatcher.cc:343  

#16 0x7fa52d3b6564 in Run /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/callback.h:396  

#17 0x7fa536f2c976 in ProcessTaskFromWorkQueue /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../content/renderer/scheduler/task\_queue\_manager.cc:368  

#18 0x7fa52d3b6564 in Run /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/callback.h:396  

#19 0x7fa52d2f084c in RunTask /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/message\_loop/message\_loop.cc:436  

#20 0x7fa52d2f18c5 in DeferOrRunPendingTask /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/message\_loop/message\_loop.cc:446  

#21 0x7fa52d2f7d0e in Run /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/message\_loop/message\_pump\_default.cc:32  

#22 0x7fa52d324508 in Run /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/run\_loop.cc:55  

#23 0x7fa52d2eefc6 in base::MessageLoop::Run() /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/message\_loop/message\_loop.cc:298  

#24 0x7fa536f1a743 in RendererMain /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../content/renderer/renderer\_main.cc:235  

#25 0x7fa52d25f093 in RunZygote /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../content/app/content\_main\_runner.cc:347  

#26 0x7fa52d261416 in Run /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../content/app/content\_main\_runner.cc:800  

#27 0x7fa52d25e6c8 in ContentMain /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../content/app/content\_main.cc:19  

#28 0x7fa52c389ea4 in ChromeMain /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../chrome/app/chrome\_main.cc:66  

#29 0x7fa5221cbec4 in \_\_libc\_start\_main /build/buildd/eglibc-2.19/csu/libc-start.c:287

0x61000001ce68 is located 40 bytes inside of 184-byte region [0x61000001ce40,0x61000001cef8)  

freed by thread T0 (chrome) here:  

#0 0x7fa52c3894d9 in operator delete(void\*) ??:?  

#1 0x7fa5327123d7 in deletePtr /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/wtf/OwnPtrCommon.h:52 (discriminator 1)  

#2 0x7fa53277749a in disposeContext /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/WindowProxy.cpp:117  

#3 0x7fa53277de68 in clearForClose /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/WindowProxyManager.cpp:52  

#4 0x7fa5326e6e71 in clearForClose /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/ScriptController.cpp:135  

#5 0x7fa531704f05 in detach /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/frame/LocalFrame.cpp:279  

#6 0x7fa530c05489 in disconnectContentFrame /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/html/HTMLFrameOwnerElement.cpp:153  

#7 0x7fa530b5379b in disconnectCollectedFrameOwners /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/ChildFrameDisconnector.cpp:65  

#8 0x7fa5308d3d77 in willRemoveChild /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/ContainerNode.cpp:423  

#9 0x7fa5308d30fc in removeChild /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/ContainerNode.cpp:552  

#10 0x7fa530a05eb0 in removeChild /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/Node.cpp:483  

#11 0x7fa532ebd7a0 in removeChildMethod /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/gen/blink/bindings/core/v8/V8Node.cpp:583  

#12 0x7fa53037f42e in Call /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/arguments.cc:33  

#13 0x7fa52f85e88f in HandleApiCallHelper<false> /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/builtins.cc:1139  

#14 0x7fa4f04071ba (<unknown module>)  

#15 0x7fa4f0476533 (<unknown module>)  

#16 0x7fa4f046b604 (<unknown module>)  

#17 0x7fa4f0451d87 (<unknown module>)  

#18 0x7fa4f04536d5 (<unknown module>)  

#19 0x7fa4f046132a (<unknown module>)  

#20 0x7fa4f04760a0 (<unknown module>)  

#21 0x7fa4f04068f4 (<unknown module>)  

#22 0x7fa4f0461577 (<unknown module>)  

#23 0x7fa4f04760a0 (<unknown module>)  

#24 0x7fa4f04068f4 (<unknown module>)  

#25 0x7fa4f04377bb (<unknown module>)  

#26 0x7fa4f0432270 (<unknown module>)  

#14 0x7fa52f9ac337 in Invoke /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/execution.cc:103  

#15 0x7fa52f9b1631 in Call /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/execution.cc:153  

#16 0x7fa52f7c9bc2 in GetFunction /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/api.cc:5215

previously allocated by thread T0 (chrome) here:  

#0 0x7fa52c388f59 in operator new(unsigned long) ??:?  

#1 0x7fa53275d373 in create /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/V8PerContextData.cpp:69  

#2 0x7fa532711d9d in ScriptState /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/ScriptState.cpp:35  

#3 0x7fa532711861 in create /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/ScriptState.cpp:17  

#4 0x7fa53277983b in createContext /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/WindowProxy.cpp:287  

#5 0x7fa532778214 in initialize /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/WindowProxy.cpp:209  

#6 0x7fa532777f0f in initializeIfNeeded /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/WindowProxy.cpp:195  

#7 0x7fa5326e94ba in windowProxy /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/ScriptController.cpp:221 (discriminator 1)  

#8 0x7fa53273105d in toV8Context /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/V8Binding.cpp:863  

#9 0x7fa5326afbc1 in toV8 /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/custom/V8WindowCustom.cpp:455  

#10 0x7fa532b6a22f in v8SetReturnValueFast<v8::PropertyCallbackInfo[v8::Value](javascript:void(0);) > /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/gen/blink/bindings/core/v8/V8Window.h:78  

#11 0x7fa530380038 in Call /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/arguments.cc:87  

#12 0x7fa52ff49f59 in GetPropertyWithAccessor /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/objects.cc:291  

#13 0x7fa52fe39c8e in Load /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/ic/ic.cc:737  

#14 0x7fa52fe52d64 in \_\_RT\_impl\_LoadIC\_Miss /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/ic/ic.cc:2302 (discriminator 1)  

#15 0x7fa4f04071ba (<unknown module>)  

#16 0x7fa4f046e9b2 (<unknown module>)  

#17 0x7fa4f046e45c (<unknown module>)  

#18 0x7fa4f04377bf (<unknown module>)  

#19 0x7fa4f0432270 (<unknown module>)  

#15 0x7fa52f9ac337 in Invoke /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/execution.cc:103  

#16 0x7fa52f7ca7d6 in Call /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/api.cc:4030  

#17 0x7fa53276abdf in callFunction /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/V8ScriptRunner.cpp:405  

#18 0x7fa5326e7a53 in callFunction /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/ScriptController.cpp:164  

#19 0x7fa5326e7128 in callFunction /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/ScriptController.cpp:148  

#20 0x7fa53274e579 in callListenerFunction /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/V8LazyEventListener.cpp:99  

#21 0x7fa53272841a in invokeEventHandler /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/V8AbstractEventListener.cpp:125  

#22 0x7fa532727e56 in handleEvent /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/V8AbstractEventListener.cpp:100  

#23 0x7fa532727b02 in handleEvent /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/V8AbstractEventListener.cpp:85  

#24 0x7fa530b2bb67 in fireEventListeners /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/events/EventTarget.cpp:376

SUMMARY: AddressSanitizer: heap-use-after-free ??:0 ??  

Shadow bytes around the buggy address:  

0x0c207fffb970: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0c207fffb980: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd  

0x0c207fffb990: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c207fffb9a0: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd  

0x0c207fffb9b0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

=>0x0c207fffb9c0: fa fa fa fa fa fa fa fa fd fd fd fd fd[fd]fd fd  

0x0c207fffb9d0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fa  

0x0c207fffb9e0: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd  

0x0c207fffb9f0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c207fffba00: fa fa fa fa fa fa fa fa 00 00 00 00 00 00 00 00  

0x0c207fffba10: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

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

==28305==ABORTING  

[28317:28320:0113/091049:WARNING:channel.cc(553)] Failed to send message to ack remove remote endpoint (local ID 1, remote ID 1)

**VERSION**  

Chrome Version: asan-linux-release-311005

**REPRODUCTION CASE**  

Attached in crash.zip

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab

## Attachments

- [crash.zip](attachments/crash.zip) (application/zip, 3.4 KB)
- [a.html](attachments/a.html) (text/html, 401 B)
- [a.svg](attachments/a.svg) (image/svg+xml, 12 B)
- [crash.html](attachments/crash.html) (text/html, 360 B)

## Timeline

### cl...@chromium.org (2015-01-13)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5633179296727040

### cl...@chromium.org (2015-01-13)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5665941307260928

### cl...@chromium.org (2015-01-13)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-01-13)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5665941307260928

Uploader: mbarbella@google.com
Job Type: Linux_asan_content_shell_drt

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x6110003440e8
Crash State:
  blink::V8PerContextData::constructorForTypeSlowCase
  blink::V8PerContextData::createWrapperFromCacheSlowCase
  blink::V8DOMWrapper::createWrapper
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_content_shell_drt&range=268656:269696

Minimized Testcase (0.79 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94Q912S_fasbH4ZfSM45bEHKLl_Lx_cMUpvUj8msVTBQvT9roL0M7rXzCcF6CprdIU2rMm-t12nBBV9gVkU6Zo8UsXk4bHmuiywECFUSx2_YC92GoGIl0hcy7DjeYOAlzDkJhS69UJDb-nfn5KX2chLT_eV4A



### mb...@chromium.org (2015-01-13)

Author: tkent@chromium.org
Component: blink
Changelist: https://chromium.googlesource.com/chromium/blink.git/+/0c67285682954a4ac6ad555ac55619eec56102e3
Time: Fri May 09 03:37:44 2014
Lines 5707 of file Document.cpp which potentially caused crash are changed in this cl (frame #3, "blink::Document::wrap").
Minimum distance from crash line to modified line: 0. (file: Document.cpp, crashed on: 5707, modified: 5707).

tkent, could you take a look at this or help to find another owner if it isn't related to that change?

### cl...@chromium.org (2015-01-13)

[Empty comment from Monorail migration]

### tk...@chromium.org (2015-01-14)

Shiino-san, can you handle this?  I'm OOO.


### yu...@chromium.org (2015-01-15)

[Empty comment from Monorail migration]

### yu...@chromium.org (2015-01-15)

+dcheng, do you have any ideas on this issue, or do you know someone who is good in this area?

It seems that Node::removeChild() causes a detach of LocalFrame, and it destroys a V8PerContextData, while we're doing LocalDOMWindow::installNewDocument.

LocalDOMWindow::installNewDocument (indirectly) creates a new wrapper for Document (via Document::wrap) and then we need the v8::Context and the corresponding V8PerContextData.  However, while V8PerContextData::constructorForTypeSlowCase is running, V8 runs and calls Node::removeChild().

See the stacktrace of "freed by thread T0" at https://cluster-fuzz.appspot.com/testcase?key=5665941307260928

Any clues or suggestions are welcome.

### ha...@chromium.org (2015-01-15)

+dcarney, +jochen (who would know what happens around updateDocumentProperty)


### jo...@chromium.org (2015-01-15)

my guess is that this is because of the blink scheduler.

### yu...@chromium.org (2015-01-16)

rmcilroy@, could you take a look?

### ha...@chromium.org (2015-01-16)

I don't think this is an issue of the blink scheduler. The problem is that there is a call path in which V8DOMWrapper::createWrapper() invokes an arbitrary JavaScript and the JavaScript can destroy the context that the V8DOMWrapper::createWrapper() is using.

I think that it's valid to allow an arbitrary JavaScript during V8DOMWrapper::createWrapper() (see the minimized test case), so a right fix would be to protect the context (or something) during V8DOMWrapper::createWrapper().


### ha...@chromium.org (2015-01-16)

[Empty comment from Monorail migration]

### rm...@chromium.org (2015-01-16)

I agree with haraken@, I doubt this would be caused by the scheduler. We currently don't reorder any tasks posted by Blink, only tasks posted by the Compositor and any posted directly to the message_loop in Chrome (which is a very small proportion of tasks).

#13 sounds more likely to me.

### yu...@chromium.org (2015-01-23)

My findings for this issue are:

1. It's very hard to protect frame and document against arbitrary JS operations while frame and document are being loaded.  JS can destroy frame and document while we're loading them, and we'll easily get into unexpected invalid states.  Most of the code don't expect such a situation.

2. Firefox and IE don't have this issue, because:
2-1) In Firefox, iframe.contentWindow returns null before iframe gets loaded, so there is no chance for JS code to run while frame and document are being loaded.
2-2) In IE, iframe.contentWindow.document returns null, so there is no chance, too.

3. http://crrev.com/872693002 fixes the issue by making iframe.contentWindow return null until iframe is loaded, however, when the patch is applied, Developer Tools does NOT work because DevToolsApp.js, etc. expect iframe.contentWindow is available before iframe is loaded.

My proposal is 1) make DevTools work with the patch applied, and then 2) commit the patch.
What do you guys think?

Attached files are a simplified version of the test case.


### pf...@chromium.org (2015-01-23)

[Empty comment from Monorail migration]

### dg...@chromium.org (2015-01-23)

re #16: don't you think that web sites may depend on iframe.contentWindow similarly to DevTools? Perhaps, this decision requires an Intent to ship?

### yu...@chromium.org (2015-01-23)

Yes, probably.  It would be a tough decision and we may need an Intent to ship if you guys agree with this approach.  I'd like to hear you guys' opinions and thoughts on this issue before I send an Intent to ship.

Since other browsers (FF and IE) don't support iframe.contentWindow or iframe.contentWindow.document, I hope that many web sites don't depend on iframe.contentWindow.

### dg...@chromium.org (2015-01-26)

I've created a patch for DevTools (http://crrev.com/867833003) which avoids using iframe.contentWindow while loading, so DevTools are ready for this change.

### yu...@chromium.org (2015-01-27)

Thanks for the fix.  I've posted an Intent-to-ship:
https://groups.google.com/a/chromium.org/forum/#!topic/blink-dev/CADkW9ZrSBs

### dc...@chromium.org (2015-01-27)

[Empty comment from Monorail migration]

### yu...@chromium.org (2015-01-28)

From the discussion in the thread of the Intent-to-ship, I figured out that iframe.contentWindow must return a valid WindowProxy object.  Now we're back to the original question, how do we handle this issue?

dgozman@, I'm sorry for having you work on that CL.

To all, any help or advises are welcome.  It's great if someone who is an expert of this area can take this issue.  I feel I'm not the right person to handle this issue.

### yu...@chromium.org (2015-01-28)

[Empty comment from Monorail migration]

### dc...@chromium.org (2015-01-28)

[Empty comment from Monorail migration]

### dc...@chromium.org (2015-01-28)

Completely minimized and self-contained example.

### dc...@chromium.org (2015-01-30)

OK, so there are a few oddities that this test case reveals:

1) What should document.removeChild(document.documentElement) followed by document.appendChild(document.createElement('iframe')) do?

IE: iframe is attached and renders normally, window.length is 1
FF: iframe is not attached and renders strangely (the iframe drawn is 4 pixels high and the width of the entire viewport), window.length is 0
Chrome: iframe is attached and renders normally, window.length is 1

The spec (https://html.spec.whatwg.org/multipage/embedded-content.html#the-iframe-element) says:
When an iframe element is inserted into a document that has a browsing context, the user agent must create a nested browsing context, and then process the iframe attributes for the "first time".
A strict reading suggests that the current IE/Chrome behavior is correct.

2) The test case changes Object.prototype.valueOf to detach the iframe. This ends up running at a very awkward time:
2:024> k
ChildEBP RetAddr  
0018defc 02260951 content_shell!blink::ContainerNode::removeChild [d:\src\chrome\src\third_party\webkit\source\core\dom\containernode.cpp @ 523]
0018df24 03049e65 content_shell!blink::Node::removeChild+0x51 [d:\src\chrome\src\third_party\webkit\source\core\dom\node.cpp @ 483]
0018dfc0 0303a0d9 content_shell!blink::NodeV8Internal::removeChildMethod+0x125 [d:\src\chrome\src\out\debug\gen\blink\bindings\core\v8\v8node.cpp @ 583]
0018dfcc 01e3ad98 content_shell!blink::NodeV8Internal::removeChildMethodCallback+0x19 [d:\src\chrome\src\out\debug\gen\blink\bindings\core\v8\v8node.cpp @ 594]
0018e000 01df1042 content_shell!v8::internal::FunctionCallbackArguments::Call+0x58 [d:\src\chrome\src\v8\src\arguments.cc @ 34]
0018e074 01df3893 content_shell!v8::internal::HandleApiCallHelper<0>+0x4d2 [d:\src\chrome\src\v8\src\builtins.cc @ 1078]
0018e094 01df0495 content_shell!v8::internal::Builtin_Impl_HandleApiCall+0x53 [d:\src\chrome\src\v8\src\builtins.cc @ 1100]
0018e0a8 2650a93c content_shell!v8::internal::Builtin_HandleApiCall+0x55 [d:\src\chrome\src\v8\src\builtins.cc @ 1095]
WARNING: Frame IP not in any known module. Following frames may be wrong.
0018e0c8 26556afd 0x2650a93c
0018e0e8 26552c16 0x26556afd
0018e10c 265450ba 0x26552c16
0018e128 2654666a 0x265450ba
0018e14c 2654ffa2 0x2654666a
0018e274 01ccdf67 0x2654ffa2
0018e2d0 01ccccfa content_shell!v8::internal::Invoke+0x3c7 [d:\src\chrome\src\v8\src\execution.cc @ 128]
0018e300 01ccdb47 content_shell!v8::internal::Execution::Call+0x1ba [d:\src\chrome\src\v8\src\execution.cc @ 180]
0018e33c 01c4e4da content_shell!v8::internal::Execution::InstantiateObject+0x1d7 [d:\src\chrome\src\v8\src\execution.cc @ 681]
0018e35c 03323f8b content_shell!v8::ObjectTemplate::NewInstance+0x11a [d:\src\chrome\src\v8\src\api.cc @ 5248]
0018e524 00660ff3 content_shell!gin::WrappableBase::GetWrapperImpl+0x1cb [d:\src\chrome\src\gin\wrappable.cc @ 46]
0018e53c 0065e607 content_shell!gin::Wrappable<content::AccessibilityControllerBindings>::GetWrapper+0x23 [d:\src\chrome\src\gin\wrappable.h @ 87]
0018e55c 006611c3 content_shell!gin::CreateHandle<content::AccessibilityControllerBindings>+0x27 [d:\src\chrome\src\gin\handle.h @ 64]
0018e5ec 006610e6 content_shell!content::AccessibilityControllerBindings::Install+0xc3 [d:\src\chrome\src\content\shell\renderer\test_runner\accessibility_controller.cc @ 64]
0018e61c 0065a7a1 content_shell!content::AccessibilityController::Install+0xd6 [d:\src\chrome\src\content\shell\renderer\test_runner\accessibility_controller.cc @ 153]
0018e62c 0061fca1 content_shell!content::TestInterfaces::BindTo+0x21 [d:\src\chrome\src\content\shell\renderer\test_runner\test_interfaces.cc @ 78]
0018e63c 0061a361 content_shell!content::WebTestInterfaces::BindTo+0x21 [d:\src\chrome\src\content\shell\renderer\test_runner\web_test_interfaces.cc @ 34]
0018e64c 046fa3a4 content_shell!content::WebKitTestRunner::DidClearWindowObject+0x31 [d:\src\chrome\src\content\shell\renderer\layout_test\webkit_test_runner.cc @ 600]
0018e6e0 0472b518 content_shell!content::RenderViewImpl::didClearWindowObject+0x74 [d:\src\chrome\src\content\renderer\render_view_impl.cc @ 2319]
0018e7d8 02211959 content_shell!content::RenderFrameImpl::didClearWindowObject+0xf8 [d:\src\chrome\src\content\renderer\render_frame_impl.cc @ 2598]
0018e7f4 026ba95e content_shell!blink::FrameLoaderClientImpl::dispatchDidClearWindowObjectInMainWorld+0x59 [d:\src\chrome\src\third_party\webkit\source\web\frameloaderclientimpl.cpp @ 122]
0018e80c 026bc684 content_shell!blink::FrameLoader::dispatchDidClearDocumentOfWindowObject+0x9e [d:\src\chrome\src\third_party\webkit\source\core\loader\frameloader.cpp @ 1371]
0018e85c 02746e9d content_shell!blink::FrameLoader::receivedFirstData+0x2c4 [d:\src\chrome\src\third_party\webkit\source\core\loader\frameloader.cpp @ 359]
0018e8fc 0274612b content_shell!blink::DocumentLoader::ensureWriter+0x1cd [d:\src\chrome\src\third_party\webkit\source\core\loader\documentloader.cpp @ 497]
0018e97c 027472e3 content_shell!blink::DocumentLoader::commitData+0x3b [d:\src\chrome\src\third_party\webkit\source\core\loader\documentloader.cpp @ 502]
0018e9a4 02747f2e content_shell!blink::DocumentLoader::finishedLoading+0x133 [d:\src\chrome\src\third_party\webkit\source\core\loader\documentloader.cpp @ 243]
0018e9c4 026a8f1e content_shell!blink::DocumentLoader::notifyFinished+0xde [d:\src\chrome\src\third_party\webkit\source\core\loader\documentloader.cpp @ 213]
0018e9f8 026ab538 content_shell!blink::Resource::checkNotify+0x6e [d:\src\chrome\src\third_party\webkit\source\core\fetch\resource.cpp @ 213]
0018ea08 026ab4cc content_shell!blink::Resource::finishOnePart+0x28 [d:\src\chrome\src\third_party\webkit\source\core\fetch\resource.cpp @ 265]
0018ea18 028e086d content_shell!blink::Resource::finish+0x7c [d:\src\chrome\src\third_party\webkit\source\core\fetch\resource.cpp @ 272]
0018ea40 068587a8 content_shell!blink::ResourceLoader::didFinishLoading+0x18d [d:\src\chrome\src\third_party\webkit\source\core\fetch\resourceloader.cpp @ 455]
0018ec00 068583f4 content_shell!content::WebURLLoaderImpl::Context::OnCompletedRequest+0x2d8 [d:\src\chrome\src\content\child\web_url_loader_impl.cc @ 764]
0018f040 0685ac41 content_shell!content::WebURLLoaderImpl::Context::HandleDataURL+0x1b4 [d:\src\chrome\src\content\child\web_url_loader_impl.cc @ 826]
0018f050 068584ba content_shell!base::internal::RunnableAdapter<void (__thiscall content::WebURLLoaderImpl::Context::*)(void)>::Run+0x21 [d:\src\chrome\src\base\bind_internal.h @ 185]
0018f05c 0685abb9 content_shell!base::internal::InvokeHelper<0,void,base::internal::RunnableAdapter<void (__thiscall content::WebURLLoaderImpl::Context::*)(void)>,void __cdecl(content::WebURLLoaderImpl::Context * const &)>::MakeItSo+0x1a [d:\src\chrome\src\base\bind_internal.h @ 382]
0018f078 005f28af content_shell!base::internal::Invoker<1,base::internal::BindState<base::internal::RunnableAdapter<void (__thiscall content::WebURLLoaderImpl::Context::*)(void)>,void __cdecl(content::WebURLLoaderImpl::Context *),void __cdecl(content::WebURLLoaderImpl::Context *)>,void __cdecl(content::WebURLLoaderImpl::Context *)>::Run+0x49 [d:\src\chrome\src\base\bind_internal.h @ 478]
0018f090 009e659b content_shell!base::Callback<void __cdecl(void)>::Run+0x2f [d:\src\chrome\src\base\callback.h @ 396]
0018f158 04ae1eae content_shell!base::debug::TaskAnnotator::RunTask+0x22b [d:\src\chrome\src\base\debug\task_annotator.cc @ 65]
0018f1b0 04ae14c0 content_shell!content::TaskQueueManager::ProcessTaskFromWorkQueue+0x7e [d:\src\chrome\src\content\renderer\scheduler\task_queue_manager.cc @ 410]
0018f2a8 04ae237d content_shell!content::TaskQueueManager::DoWork+0x170 [d:\src\chrome\src\content\renderer\scheduler\task_queue_manager.cc @ 381]
0018f2bc 04ae18bf content_shell!base::internal::RunnableAdapter<void (__thiscall content::TaskQueueManager::*)(bool)>::Run+0x2d [d:\src\chrome\src\base\bind_internal.h @ 185]
0018f2cc 04ae22eb content_shell!base::internal::InvokeHelper<1,void,base::internal::RunnableAdapter<void (__thiscall content::TaskQueueManager::*)(bool)>,void __cdecl(base::WeakPtr<content::TaskQueueManager> const &,bool const &)>::MakeItSo+0x2f [d:\src\chrome\src\base\bind_internal.h @ 392]
0018f2ec 005f28af content_shell!base::internal::Invoker<2,base::internal::BindState<base::internal::RunnableAdapter<void (__thiscall content::TaskQueueManager::*)(bool)>,void __cdecl(content::TaskQueueManager *,bool),void __cdecl(base::WeakPtr<content::TaskQueueManager>,bool)>,void __cdecl(content::TaskQueueManager *,bool)>::Run+0x6b [d:\src\chrome\src\base\bind_internal.h @ 562]
0018f304 009e659b content_shell!base::Callback<void __cdecl(void)>::Run+0x2f [d:\src\chrome\src\base\callback.h @ 396]
0018f3cc 00923278 content_shell!base::debug::TaskAnnotator::RunTask+0x22b [d:\src\chrome\src\base\debug\task_annotator.cc @ 65]
0018f598 00920db4 content_shell!base::MessageLoop::RunTask+0x1c8 [d:\src\chrome\src\base\message_loop\message_loop.cc @ 461]
0018f5a8 0092139d content_shell!base::MessageLoop::DeferOrRunPendingTask+0x34 [d:\src\chrome\src\base\message_loop\message_loop.cc @ 471]
0018f600 009ee4c4 content_shell!base::MessageLoop::DoWork+0xdd [d:\src\chrome\src\base\message_loop\message_loop.cc @ 580]
0018f710 00923087 content_shell!base::MessagePumpDefault::Run+0xf4 [d:\src\chrome\src\base\message_loop\message_pump_default.cc @ 32]
0018f7e8 00a07556 content_shell!base::MessageLoop::RunHandler+0xf7 [d:\src\chrome\src\base\message_loop\message_loop.cc @ 424]
0018f81c 00922f3b content_shell!base::RunLoop::Run+0x46 [d:\src\chrome\src\base\run_loop.cc @ 56]
0018f850 047076fa content_shell!base::MessageLoop::Run+0x2b [d:\src\chrome\src\base\message_loop\message_loop.cc @ 318]
0018fbdc 006e2569 content_shell!content::RendererMain+0x42a [d:\src\chrome\src\content\renderer\renderer_main.cc @ 229]
0018fcb0 006e2431 content_shell!content::RunNamedProcessTypeMain+0xa9 [d:\src\chrome\src\content\app\content_main_runner.cc @ 423]
0018fea8 006d9bf0 content_shell!content::ContentMainRunnerImpl::Run+0x1f1 [d:\src\chrome\src\content\app\content_main_runner.cc @ 800]
0018fed8 005b1ca7 content_shell!content::ContentMain+0x90 [d:\src\chrome\src\content\app\content_main.cc @ 19]
0018ff3c 05362aa1 content_shell!wWinMain+0x57 [d:\src\chrome\src\content\shell\app\shell_main.cc @ 34]
0018ff88 772c338a content_shell!__tmainCRTStartup+0xfd [f:\dd\vctools\crt\crtw32\startup\crt0.c @ 251]
0018ff94 779b9f72 kernel32!BaseThreadInitThunk+0x12
0018ffd4 779b9f45 ntdll!RtlInitializeExceptionChain+0x63
0018ffec 00000000 ntdll!RtlInitializeExceptionChain+0x36

We do not expect to run Javascript at this time--the Frame reference is unprotected, and we blow away Frame from underneath ourselves.

3) I did some experiments to see what, if anything, persists from the initial about:blank Window object (since this is reused on first navigation away from the page). It seems we wipe the Window object clean at some point (I tried setting window.Object.prototype.valueOf and window.foo, navigating, and seeing if the set values persisted)--but not before we call dispatchDidClearDocumentOfWindowObject(). It seems like this is a bad ordering, because it might be possible for 

4) Finally, FrameLoader calls dispatchDidClearDocumentOfWindowObject() in two places (didBeginDocument and receivedFirstData). The coordination is quite awkward and should be improved.

This being said, I'm not sure how reachable this is from a normal build of Chrome. I took a quick audit of the code reached by RenderViewImpl::DidClearWindowObject(). In general, installed JS bindings fall into two camps:
- Bindings installed for WebUI. Since we should be forcing renderer swaps for this, I /think/ that 
- Bindings installed for testing/debugging/logging purposes. These are guarded by various flags which should not be present on "normal" Chrome.

A quick test in an ASAN Chrome reveals that we don't get killed by ASAN (though we do hit a NOTREACHED in child_thread.cc:480 in ChildThread::AllocateSharedMemory, since it expects the IPC send to never fail).

### dc...@chromium.org (2015-01-30)

OK, so there are a few oddities that this test case reveals:

1) What should document.removeChild(document.documentElement) followed by document.appendChild(document.createElement('iframe')) do?

IE: iframe is attached and renders normally, window.length is 1
FF: iframe is not attached and renders strangely (the iframe drawn is 4 pixels high and the width of the entire viewport), window.length is 0
Chrome: iframe is attached and renders normally, window.length is 1

The spec (https://html.spec.whatwg.org/multipage/embedded-content.html#the-iframe-element) says:
When an iframe element is inserted into a document that has a browsing context, the user agent must create a nested browsing context, and then process the iframe attributes for the "first time".
A strict reading suggests that the current IE/Chrome behavior is correct.

2) The test case changes Object.prototype.valueOf to detach the iframe. This ends up running at a very awkward time:
2:024> k
ChildEBP RetAddr  
0018defc 02260951 content_shell!blink::ContainerNode::removeChild [d:\src\chrome\src\third_party\webkit\source\core\dom\containernode.cpp @ 523]
0018df24 03049e65 content_shell!blink::Node::removeChild+0x51 [d:\src\chrome\src\third_party\webkit\source\core\dom\node.cpp @ 483]
0018dfc0 0303a0d9 content_shell!blink::NodeV8Internal::removeChildMethod+0x125 [d:\src\chrome\src\out\debug\gen\blink\bindings\core\v8\v8node.cpp @ 583]
0018dfcc 01e3ad98 content_shell!blink::NodeV8Internal::removeChildMethodCallback+0x19 [d:\src\chrome\src\out\debug\gen\blink\bindings\core\v8\v8node.cpp @ 594]
0018e000 01df1042 content_shell!v8::internal::FunctionCallbackArguments::Call+0x58 [d:\src\chrome\src\v8\src\arguments.cc @ 34]
0018e074 01df3893 content_shell!v8::internal::HandleApiCallHelper<0>+0x4d2 [d:\src\chrome\src\v8\src\builtins.cc @ 1078]
0018e094 01df0495 content_shell!v8::internal::Builtin_Impl_HandleApiCall+0x53 [d:\src\chrome\src\v8\src\builtins.cc @ 1100]
0018e0a8 2650a93c content_shell!v8::internal::Builtin_HandleApiCall+0x55 [d:\src\chrome\src\v8\src\builtins.cc @ 1095]
WARNING: Frame IP not in any known module. Following frames may be wrong.
0018e0c8 26556afd 0x2650a93c
0018e0e8 26552c16 0x26556afd
0018e10c 265450ba 0x26552c16
0018e128 2654666a 0x265450ba
0018e14c 2654ffa2 0x2654666a
0018e274 01ccdf67 0x2654ffa2
0018e2d0 01ccccfa content_shell!v8::internal::Invoke+0x3c7 [d:\src\chrome\src\v8\src\execution.cc @ 128]
0018e300 01ccdb47 content_shell!v8::internal::Execution::Call+0x1ba [d:\src\chrome\src\v8\src\execution.cc @ 180]
0018e33c 01c4e4da content_shell!v8::internal::Execution::InstantiateObject+0x1d7 [d:\src\chrome\src\v8\src\execution.cc @ 681]
0018e35c 03323f8b content_shell!v8::ObjectTemplate::NewInstance+0x11a [d:\src\chrome\src\v8\src\api.cc @ 5248]
0018e524 00660ff3 content_shell!gin::WrappableBase::GetWrapperImpl+0x1cb [d:\src\chrome\src\gin\wrappable.cc @ 46]
0018e53c 0065e607 content_shell!gin::Wrappable<content::AccessibilityControllerBindings>::GetWrapper+0x23 [d:\src\chrome\src\gin\wrappable.h @ 87]
0018e55c 006611c3 content_shell!gin::CreateHandle<content::AccessibilityControllerBindings>+0x27 [d:\src\chrome\src\gin\handle.h @ 64]
0018e5ec 006610e6 content_shell!content::AccessibilityControllerBindings::Install+0xc3 [d:\src\chrome\src\content\shell\renderer\test_runner\accessibility_controller.cc @ 64]
0018e61c 0065a7a1 content_shell!content::AccessibilityController::Install+0xd6 [d:\src\chrome\src\content\shell\renderer\test_runner\accessibility_controller.cc @ 153]
0018e62c 0061fca1 content_shell!content::TestInterfaces::BindTo+0x21 [d:\src\chrome\src\content\shell\renderer\test_runner\test_interfaces.cc @ 78]
0018e63c 0061a361 content_shell!content::WebTestInterfaces::BindTo+0x21 [d:\src\chrome\src\content\shell\renderer\test_runner\web_test_interfaces.cc @ 34]
0018e64c 046fa3a4 content_shell!content::WebKitTestRunner::DidClearWindowObject+0x31 [d:\src\chrome\src\content\shell\renderer\layout_test\webkit_test_runner.cc @ 600]
0018e6e0 0472b518 content_shell!content::RenderViewImpl::didClearWindowObject+0x74 [d:\src\chrome\src\content\renderer\render_view_impl.cc @ 2319]
0018e7d8 02211959 content_shell!content::RenderFrameImpl::didClearWindowObject+0xf8 [d:\src\chrome\src\content\renderer\render_frame_impl.cc @ 2598]
0018e7f4 026ba95e content_shell!blink::FrameLoaderClientImpl::dispatchDidClearWindowObjectInMainWorld+0x59 [d:\src\chrome\src\third_party\webkit\source\web\frameloaderclientimpl.cpp @ 122]
0018e80c 026bc684 content_shell!blink::FrameLoader::dispatchDidClearDocumentOfWindowObject+0x9e [d:\src\chrome\src\third_party\webkit\source\core\loader\frameloader.cpp @ 1371]
0018e85c 02746e9d content_shell!blink::FrameLoader::receivedFirstData+0x2c4 [d:\src\chrome\src\third_party\webkit\source\core\loader\frameloader.cpp @ 359]
0018e8fc 0274612b content_shell!blink::DocumentLoader::ensureWriter+0x1cd [d:\src\chrome\src\third_party\webkit\source\core\loader\documentloader.cpp @ 497]
0018e97c 027472e3 content_shell!blink::DocumentLoader::commitData+0x3b [d:\src\chrome\src\third_party\webkit\source\core\loader\documentloader.cpp @ 502]
0018e9a4 02747f2e content_shell!blink::DocumentLoader::finishedLoading+0x133 [d:\src\chrome\src\third_party\webkit\source\core\loader\documentloader.cpp @ 243]
0018e9c4 026a8f1e content_shell!blink::DocumentLoader::notifyFinished+0xde [d:\src\chrome\src\third_party\webkit\source\core\loader\documentloader.cpp @ 213]
0018e9f8 026ab538 content_shell!blink::Resource::checkNotify+0x6e [d:\src\chrome\src\third_party\webkit\source\core\fetch\resource.cpp @ 213]
0018ea08 026ab4cc content_shell!blink::Resource::finishOnePart+0x28 [d:\src\chrome\src\third_party\webkit\source\core\fetch\resource.cpp @ 265]
0018ea18 028e086d content_shell!blink::Resource::finish+0x7c [d:\src\chrome\src\third_party\webkit\source\core\fetch\resource.cpp @ 272]
0018ea40 068587a8 content_shell!blink::ResourceLoader::didFinishLoading+0x18d [d:\src\chrome\src\third_party\webkit\source\core\fetch\resourceloader.cpp @ 455]
0018ec00 068583f4 content_shell!content::WebURLLoaderImpl::Context::OnCompletedRequest+0x2d8 [d:\src\chrome\src\content\child\web_url_loader_impl.cc @ 764]
0018f040 0685ac41 content_shell!content::WebURLLoaderImpl::Context::HandleDataURL+0x1b4 [d:\src\chrome\src\content\child\web_url_loader_impl.cc @ 826]
0018f050 068584ba content_shell!base::internal::RunnableAdapter<void (__thiscall content::WebURLLoaderImpl::Context::*)(void)>::Run+0x21 [d:\src\chrome\src\base\bind_internal.h @ 185]
0018f05c 0685abb9 content_shell!base::internal::InvokeHelper<0,void,base::internal::RunnableAdapter<void (__thiscall content::WebURLLoaderImpl::Context::*)(void)>,void __cdecl(content::WebURLLoaderImpl::Context * const &)>::MakeItSo+0x1a [d:\src\chrome\src\base\bind_internal.h @ 382]
0018f078 005f28af content_shell!base::internal::Invoker<1,base::internal::BindState<base::internal::RunnableAdapter<void (__thiscall content::WebURLLoaderImpl::Context::*)(void)>,void __cdecl(content::WebURLLoaderImpl::Context *),void __cdecl(content::WebURLLoaderImpl::Context *)>,void __cdecl(content::WebURLLoaderImpl::Context *)>::Run+0x49 [d:\src\chrome\src\base\bind_internal.h @ 478]
0018f090 009e659b content_shell!base::Callback<void __cdecl(void)>::Run+0x2f [d:\src\chrome\src\base\callback.h @ 396]
0018f158 04ae1eae content_shell!base::debug::TaskAnnotator::RunTask+0x22b [d:\src\chrome\src\base\debug\task_annotator.cc @ 65]
0018f1b0 04ae14c0 content_shell!content::TaskQueueManager::ProcessTaskFromWorkQueue+0x7e [d:\src\chrome\src\content\renderer\scheduler\task_queue_manager.cc @ 410]
0018f2a8 04ae237d content_shell!content::TaskQueueManager::DoWork+0x170 [d:\src\chrome\src\content\renderer\scheduler\task_queue_manager.cc @ 381]
0018f2bc 04ae18bf content_shell!base::internal::RunnableAdapter<void (__thiscall content::TaskQueueManager::*)(bool)>::Run+0x2d [d:\src\chrome\src\base\bind_internal.h @ 185]
0018f2cc 04ae22eb content_shell!base::internal::InvokeHelper<1,void,base::internal::RunnableAdapter<void (__thiscall content::TaskQueueManager::*)(bool)>,void __cdecl(base::WeakPtr<content::TaskQueueManager> const &,bool const &)>::MakeItSo+0x2f [d:\src\chrome\src\base\bind_internal.h @ 392]
0018f2ec 005f28af content_shell!base::internal::Invoker<2,base::internal::BindState<base::internal::RunnableAdapter<void (__thiscall content::TaskQueueManager::*)(bool)>,void __cdecl(content::TaskQueueManager *,bool),void __cdecl(base::WeakPtr<content::TaskQueueManager>,bool)>,void __cdecl(content::TaskQueueManager *,bool)>::Run+0x6b [d:\src\chrome\src\base\bind_internal.h @ 562]
0018f304 009e659b content_shell!base::Callback<void __cdecl(void)>::Run+0x2f [d:\src\chrome\src\base\callback.h @ 396]
0018f3cc 00923278 content_shell!base::debug::TaskAnnotator::RunTask+0x22b [d:\src\chrome\src\base\debug\task_annotator.cc @ 65]
0018f598 00920db4 content_shell!base::MessageLoop::RunTask+0x1c8 [d:\src\chrome\src\base\message_loop\message_loop.cc @ 461]
0018f5a8 0092139d content_shell!base::MessageLoop::DeferOrRunPendingTask+0x34 [d:\src\chrome\src\base\message_loop\message_loop.cc @ 471]
0018f600 009ee4c4 content_shell!base::MessageLoop::DoWork+0xdd [d:\src\chrome\src\base\message_loop\message_loop.cc @ 580]
0018f710 00923087 content_shell!base::MessagePumpDefault::Run+0xf4 [d:\src\chrome\src\base\message_loop\message_pump_default.cc @ 32]
0018f7e8 00a07556 content_shell!base::MessageLoop::RunHandler+0xf7 [d:\src\chrome\src\base\message_loop\message_loop.cc @ 424]
0018f81c 00922f3b content_shell!base::RunLoop::Run+0x46 [d:\src\chrome\src\base\run_loop.cc @ 56]
0018f850 047076fa content_shell!base::MessageLoop::Run+0x2b [d:\src\chrome\src\base\message_loop\message_loop.cc @ 318]
0018fbdc 006e2569 content_shell!content::RendererMain+0x42a [d:\src\chrome\src\content\renderer\renderer_main.cc @ 229]
0018fcb0 006e2431 content_shell!content::RunNamedProcessTypeMain+0xa9 [d:\src\chrome\src\content\app\content_main_runner.cc @ 423]
0018fea8 006d9bf0 content_shell!content::ContentMainRunnerImpl::Run+0x1f1 [d:\src\chrome\src\content\app\content_main_runner.cc @ 800]
0018fed8 005b1ca7 content_shell!content::ContentMain+0x90 [d:\src\chrome\src\content\app\content_main.cc @ 19]
0018ff3c 05362aa1 content_shell!wWinMain+0x57 [d:\src\chrome\src\content\shell\app\shell_main.cc @ 34]
0018ff88 772c338a content_shell!__tmainCRTStartup+0xfd [f:\dd\vctools\crt\crtw32\startup\crt0.c @ 251]
0018ff94 779b9f72 kernel32!BaseThreadInitThunk+0x12
0018ffd4 779b9f45 ntdll!RtlInitializeExceptionChain+0x63
0018ffec 00000000 ntdll!RtlInitializeExceptionChain+0x36

We do not expect to run Javascript at this time--the Frame reference is unprotected, and we blow away Frame from underneath ourselves.

3) I did some experiments to see what, if anything, persists from the initial about:blank Window object (since this is reused on first navigation away from the page). It seems we wipe the Window object clean at some point (I tried setting window.Object.prototype.valueOf and window.foo, navigating, and seeing if the set values persisted)--but not before we call dispatchDidClearDocumentOfWindowObject(). It seems like this is a bad ordering, because it might be possible for 

4) Finally, FrameLoader calls dispatchDidClearDocumentOfWindowObject() in two places (didBeginDocument and receivedFirstData). The coordination is quite awkward and should be improved.

This being said, I'm not sure how reachable this is from a normal build of Chrome. I took a quick audit of the code reached by RenderViewImpl::DidClearWindowObject(). In general, installed JS bindings fall into two camps:
- Bindings installed for WebUI. Since we should be forcing renderer swaps for this, I /think/ that 
- Bindings installed for testing/debugging/logging purposes. These are guarded by various flags which should not be present on "normal" Chrome.

A quick test in an ASAN Chrome reveals that we don't get killed by ASAN (though we do hit a NOTREACHED in child_thread.cc:480 in ChildThread::AllocateSharedMemory, since it expects the IPC send to never fail).

### dc...@chromium.org (2015-01-30)

Oops, point #3 got cut off. But it seems bad to allow a previous page to influence the loading of the current page.

### cl...@chromium.org (2015-02-08)

ClusterFuzz has detected this issue as fixed in range 314621:315214.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5665941307260928

Uploader: mbarbella@google.com
Job Type: Linux_asan_content_shell_drt

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x6110003440e8
Crash State:
  blink::V8PerContextData::constructorForTypeSlowCase
  blink::V8PerContextData::createWrapperFromCacheSlowCase
  blink::V8DOMWrapper::createWrapper
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_content_shell_drt&range=268656:269696
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_content_shell_drt&range=314621:315214

Minimized Testcase (0.79 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94Q912S_fasbH4ZfSM45bEHKLl_Lx_cMUpvUj8msVTBQvT9roL0M7rXzCcF6CprdIU2rMm-t12nBBV9gVkU6Zo8UsXk4bHmuiywECFUSx2_YC92GoGIl0hcy7DjeYOAlzDkJhS69UJDb-nfn5KX2chLT_eV4A

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### dc...@chromium.org (2015-02-10)

Hmm... so apparently the v8 roll fixed this: https://chromium.googlesource.com/chromium/src/+/28da0fc5c88d3ee7e9c5e49dcbffbc7c2240e378

(Aside: I don't understand how I'm supposed to parse the v8 commit logs, since all the entries look like "Version x (squashed - based on 897457e2394872983472394872398472785)". Is there any documentation on how I'm supposed to parse these entries? I've also created https://crbug.com/chromium/457022 so the v8 autoroll bot can include a summary of changes like the blink bot.)

Bisecting seems to indicate https://chromium.googlesource.com/v8/v8/+/570983f30ccfd47c2a2ba22a830d2ed14d79b95c is the revision that fixed this.

Adding yurys@ who I think wrote the patch in question... I'm not sure how a patch that adds NativeWeakMap would have fixed this. However, I can confirm that the the overridden Object.valueOf prototype doesn't seem to be getting run anymore (a breakpoint on blink::ContainerNode::removeChild is only hit once).

### yu...@chromium.org (2015-02-10)

I don't think adding NativeWeakMap has anything to do with fixing mentioned crash. The V8 roll contains many other changes apart from mine (which is just https://crrev.com/a559367956d870de38375a51e919a2c06c004e26) you can notice that looking at the number of affected files. 

I think V8 log message is comprised of those commit message headers that had LOG=Y entry in their description and it seems that in that roll there happened to be only one such commit.

### dc...@chromium.org (2015-02-10)

Thanks for the pointers.

It turns out https://codereview.chromium.org/895053002 is the actual patch responsible (Move the contents of api-natives.js to c++). This makes a lot more sense.

dcarney@, how hard would it be to merge this into M40?

### dc...@chromium.org (2015-02-11)

dcheng@ nontrivial as there are a lot of constants involved that will have changed since m40 - how important is a backmerge?

### yu...@chromium.org (2015-02-11)

[Empty comment from Monorail migration]

### in...@chromium.org (2015-02-12)

We can just let this roll into m41. is m41 merge needed ?

### cl...@chromium.org (2015-02-12)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### ti...@google.com (2015-02-17)

dcheng: can you confirm if this fix is already in M41 or do we need to request a merge to M41 here?

### ti...@google.com (2015-02-23)

dcheng / yurys: Can one of you please let me know if there's a merge required for this fix in M41? Thanks.

### ti...@google.com (2015-02-26)

[Empty comment from Monorail migration]

### ti...@google.com (2015-02-26)

spoke to dcheng - this change is not entirely in M41, but merging this would be difficult. Let's let this roll into M42.

If there's any objection to that approach, let's discuss and we can reconsider.

### ti...@google.com (2015-04-09)

$3000 for this one also.

### ti...@google.com (2015-05-06)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-05-21)

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

This issue was migrated from crbug.com/chromium/448314?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081176)*
