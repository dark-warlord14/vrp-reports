# Heap-use-after-free in blink::ScopedStyleResolver::collectMatchingAuthorRules

| Field | Value |
|-------|-------|
| **Issue ID** | [40081158](https://issues.chromium.org/issues/40081158) |
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

The testcase consists of two files which are attached in crash.zip. Use --js-flags=--expose-gc for reliable repro.

Crashes the latest chromium asan build as follows:

=================================================================  

==14650==ERROR: AddressSanitizer: heap-use-after-free on address 0x60c000037e58 at pc 0x7f967e0cb37b bp 0x7fff98fcee70 sp 0x7fff98fcee68  

READ of size 8 at 0x60c000037e58 thread T0 (chrome)  

#0 0x7f967e0cb37a in contents /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/wtf/RefPtr.h:57  

#1 0x7f967e0f2893 in matchAuthorRules /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/css/resolver/StyleResolver.cpp:443 (discriminator 6)  

#2 0x7f967e0f3780 in matchAllRules /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/css/resolver/StyleResolver.cpp:505  

#3 0x7f967e0f55d1 in styleForElement /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/css/resolver/StyleResolver.cpp:632  

#4 0x7f967d67609a in originalStyleForRenderer /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/Element.cpp:1586  

#5 0x7f967d6773f0 in recalcOwnStyle /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/Element.cpp:1654  

#6 0x7f967d6769c3 in recalcStyle /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/Element.cpp:1609  

#7 0x7f967d5b1c1c in recalcChildStyle /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/ContainerNode.cpp:1229  

#8 0x7f967d7dd478 in recalcStyle /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/shadow/ShadowRoot.cpp:145  

#9 0x7f967d676c13 in recalcStyle /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/Element.cpp:1622  

#10 0x7f967d5b1c1c in recalcChildStyle /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/ContainerNode.cpp:1229  

#11 0x7f967d676c4e in recalcStyle /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/Element.cpp:1624  

#12 0x7f967d5b1c1c in recalcChildStyle /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/ContainerNode.cpp:1229  

#13 0x7f967d676c4e in recalcStyle /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/Element.cpp:1624  

#14 0x7f967d5b1c1c in recalcChildStyle /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/ContainerNode.cpp:1229  

#15 0x7f967d676c4e in recalcStyle /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/Element.cpp:1624  

#16 0x7f967d5e8cf1 in updateStyle /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/Document.cpp:1831  

#17 0x7f967d5e767c in updateRenderTree /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/Document.cpp:1772  

#18 0x7f967de1079d in getPropertyCSSValue /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/css/CSSComputedStyleDeclaration.cpp:542  

#19 0x7f967de149ef in blink::CSSComputedStyleDeclaration::getPropertyCSSValueInternal(blink::CSSPropertyID) /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/css/CSSComputedStyleDeclaration.cpp:676  

#20 0x7f967feed617 in namedPropertyGetterCustom /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/custom/V8CSSStyleDeclarationCustom.cpp:214  

#21 0x7f967f87ae9a in namedPropertyGetterCallback /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/gen/blink/bindings/core/v8/V8CSSStyleDeclaration.cpp:247  

#22 0x7f967d052038 in Call /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/arguments.cc:87  

#23 0x7f967cc1b066 in GetPropertyWithInterceptor /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/objects.cc:13515  

#24 0x7f967cc1a433 in GetProperty /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/objects.cc:121  

#25 0x7f967cb0bc8e in Load /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/ic/ic.cc:737  

#26 0x7f967cb24d64 in \_\_RT\_impl\_LoadIC\_Miss /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/ic/ic.cc:2302 (discriminator 1)  

#27 0x7f963e4071ba (<unknown module>)  

#28 0x7f963e49b913 (<unknown module>)  

#29 0x7f963e49a96a (<unknown module>)  

#30 0x7f963e497c7f (<unknown module>)  

#31 0x7f963e497a1c (<unknown module>)  

#32 0x7f963e4068f4 (<unknown module>)  

#33 0x7f963e4377bb (<unknown module>)  

#34 0x7f963e432270 (<unknown module>)  

#27 0x7f967c67e337 in Invoke /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/execution.cc:103  

#28 0x7f967d1fe97e in \_\_RT\_impl\_Runtime\_Apply /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/runtime/runtime-function.cc:578 (discriminator 1)  

#37 0x7f963e4071ba (<unknown module>)  

#38 0x7f963e476b3c (<unknown module>)  

#39 0x7f963e4068f4 (<unknown module>)  

#40 0x7f963e4377bb (<unknown module>)  

#41 0x7f963e432270 (<unknown module>)  

#29 0x7f967c67e337 in Invoke /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/execution.cc:103  

#30 0x7f967c49c7d6 in Call /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/api.cc:4030  

#31 0x7f967f43cbdf in callFunction /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/V8ScriptRunner.cpp:405  

#32 0x7f967f3b9a53 in callFunction /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/ScriptController.cpp:164  

#33 0x7f967fa30071 in handleEvent /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/gen/blink/bindings/core/v8/V8RequestAnimationFrameCallback.cpp:53  

#34 0x7f967d75b70f in executeCallbacks /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/ScriptedAnimationController.cpp:183  

#35 0x7f967d75c27e in serviceScriptedAnimations /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/ScriptedAnimationController.cpp:215  

#36 0x7f967e6d1b94 in serviceScriptedAnimations /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/page/PageAnimator.cpp:70  

#37 0x7f967d4eb747 in animate /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/web/PageWidgetDelegate.cpp:56  

#38 0x7f967d476617 in beginFrame /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/web/WebViewImpl.cpp:1841  

#39 0x7f9683de3364 in BeginMainFrame /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../content/renderer/gpu/render\_widget\_compositor.cc:767  

#40 0x7f967bb6b89f in cc::LayerTreeHost::BeginMainFrame(cc::BeginFrameArgs const&) /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../cc/trees/layer\_tree\_host.cc:232  

#41 0x7f967bc0f720 in BeginMainFrame /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../cc/trees/thread\_proxy.cc:750  

#42 0x7f967bc1c694 in Run /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/bind\_internal.h:185  

#43 0x7f967bc1c3ba in Run /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/bind\_internal.h:557  

#44 0x7f967a088564 in Run /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/callback.h:396  

#45 0x7f9683bfe976 in ProcessTaskFromWorkQueue /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../content/renderer/scheduler/task\_queue\_manager.cc:368  

#46 0x7f967a088564 in Run /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/callback.h:396  

#47 0x7f9679fc284c in RunTask /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/message\_loop/message\_loop.cc:436  

#48 0x7f9679fc38c5 in DeferOrRunPendingTask /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/message\_loop/message\_loop.cc:446  

#49 0x7f9679fc9d0e in Run /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/message\_loop/message\_pump\_default.cc:32  

#50 0x7f9679ff6508 in Run /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/run\_loop.cc:55  

#51 0x7f9679fc0fc6 in base::MessageLoop::Run() /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/message\_loop/message\_loop.cc:298  

#52 0x7f9683bec743 in RendererMain /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../content/renderer/renderer\_main.cc:235  

#53 0x7f9679f31093 in RunZygote /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../content/app/content\_main\_runner.cc:347  

#54 0x7f9679f33416 in Run /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../content/app/content\_main\_runner.cc:800  

#55 0x7f9679f306c8 in ContentMain /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../content/app/content\_main.cc:19  

#56 0x7f967905bea4 in ChromeMain /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../chrome/app/chrome\_main.cc:66  

#57 0x7f966ee9dec4 in \_\_libc\_start\_main /build/buildd/eglibc-2.19/csu/libc-start.c:287

0x60c000037e58 is located 24 bytes inside of 120-byte region [0x60c000037e40,0x60c000037eb8)  

freed by thread T0 (chrome) here:  

#0 0x7f967903d889 in \_\_interceptor\_free ??:?  

#1 0x7f967d784e36 in deref /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/wtf/RefCounted.h:172 (discriminator 2)  

#2 0x7f967d85a84e in ~TreeScopeStyleSheetCollection /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/TreeScopeStyleSheetCollection.h:48  

#3 0x7f967d776c52 in deletePtr /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/wtf/OwnPtrCommon.h:52 (discriminator 2)  

#4 0x7f967d5c6209 in ~Document /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/Document.cpp:569  

#5 0x7f967d7b005e in ~XMLDocument /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/XMLDocument.h:34  

#6 0x7f967c7321f8 in PostGarbageCollectionProcessing /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/global-handles.cc:368  

#7 0x7f967c732801 in PostMarkSweepProcessing /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/global-handles.cc:849  

#8 0x7f967c784251 in PerformGarbageCollection /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/heap/heap.cc:1140  

#9 0x7f967c782e34 in CollectGarbage /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/heap/heap.cc:848  

#10 0x7f967c7826df in CollectGarbage /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/heap/heap-inl.h:583  

#11 0x7f967c4aba00 in RequestGarbageCollectionForTesting /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/api.cc:6343  

#12 0x7f967d05142e in Call /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/arguments.cc:33  

#13 0x7f967c53088f in HandleApiCallHelper<false> /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/builtins.cc:1139  

#14 0x7f963e4071ba (<unknown module>)  

#15 0x7f963e4b533d (<unknown module>)  

#16 0x7f963e4377bf (<unknown module>)  

#17 0x7f963e432270 (<unknown module>)  

#14 0x7f967c67e337 in Invoke /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/execution.cc:103  

#15 0x7f967c47d18a in Run /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/api.cc:1476  

#16 0x7f967f43bc82 in runCompiledScript /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/V8ScriptRunner.cpp:358  

#17 0x7f967f3ba834 in executeScriptAndReturnValue /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/ScriptController.cpp:196 (discriminator 3)  

#18 0x7f967f3b4ccc in execute /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/ScheduledAction.cpp:118  

#19 0x7f967e35a2fe in fired /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/frame/DOMTimer.cpp:163  

#20 0x7f96856912eb in sharedTimerFiredInternal /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/platform/ThreadTimers.cpp:137  

#21 0x7f9685690b21 in sharedTimerFired /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/platform/ThreadTimers.cpp:107  

#22 0x7f967a0534ee in Run /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/callback.h:396  

#23 0x7f967a088564 in Run /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/callback.h:396  

#24 0x7f9683bfe976 in ProcessTaskFromWorkQueue /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../content/renderer/scheduler/task\_queue\_manager.cc:368  

#25 0x7f967a088564 in Run /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/callback.h:396

previously allocated by thread T0 (chrome) here:  

#0 0x7f967903db49 in \_\_interceptor\_malloc ??:?  

#1 0x7f967bdf8344 in partitionAllocGenericFlags /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/wtf/PartitionAlloc.h:541  

#2 0x7f967de50994 in operator new /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/wtf/RefCounted.h:166  

#3 0x7f967d77ebd8 in parseSheet /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/StyleEngine.cpp:680  

#4 0x7f967d77e18f in createSheet /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/StyleEngine.cpp:655  

#5 0x7f9685a63b7f in createSheet /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/StyleElement.cpp:196  

#6 0x7f9685a62651 in process /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/StyleElement.cpp:144  

#7 0x7f967d5a2791 in notifyNodeInserted /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/ContainerNode.cpp:783  

#8 0x7f967d59fa3f in updateTreeAfterInsertion /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/ContainerNode.cpp:1186  

#9 0x7f967d59d0f7 in appendChild /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/ContainerNode.cpp:734  

#10 0x7f967d6d8200 in appendChild /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/Node.cpp:492  

#11 0x7f967fb91afc in appendChildMethodForMainWorld /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/gen/blink/bindings/core/v8/V8Node.cpp:651  

#12 0x7f967d05142e in Call /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/arguments.cc:33  

#13 0x7f967c53088f in HandleApiCallHelper<false> /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/builtins.cc:1139  

#14 0x7f963e4071ba (<unknown module>)  

#15 0x7f963e487d7f (<unknown module>)  

#16 0x7f963e487bdc (<unknown module>)  

#17 0x7f963e4377bf (<unknown module>)  

#18 0x7f963e432270 (<unknown module>)  

#14 0x7f967c67e337 in Invoke /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/execution.cc:103  

#15 0x7f967c49c7d6 in Call /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/api.cc:4030  

#16 0x7f967f43cbdf in callFunction /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/V8ScriptRunner.cpp:405  

#17 0x7f967f3b9a53 in callFunction /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/ScriptController.cpp:164  

#18 0x7f967f3b9128 in callFunction /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/ScriptController.cpp:148  

#19 0x7f967f420579 in callListenerFunction /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/V8LazyEventListener.cpp:99  

#20 0x7f967f3fa41a in invokeEventHandler /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/V8AbstractEventListener.cpp:125  

#21 0x7f967f3f9e56 in handleEvent /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/V8AbstractEventListener.cpp:100  

#22 0x7f967f3f9b02 in handleEvent /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/V8AbstractEventListener.cpp:85  

#23 0x7f967d7fdb67 in fireEventListeners /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/events/EventTarget.cpp:376  

#24 0x7f967d7fc78b in fireEventListeners /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/events/EventTarget.cpp:312

SUMMARY: AddressSanitizer: heap-use-after-free ??:0 ??  

Shadow bytes around the buggy address:  

0x0c187fffef70: fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa  

0x0c187fffef80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c187fffef90: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd  

0x0c187fffefa0: fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa  

0x0c187fffefb0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

=>0x0c187fffefc0: fa fa fa fa fa fa fa fa fd fd fd[fd]fd fd fd fd  

0x0c187fffefd0: fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa fa  

0x0c187fffefe0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fa  

0x0c187fffeff0: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd  

0x0c187ffff000: fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa fa  

0x0c187ffff010: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fa  

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

==14650==ABORTING

**VERSION**  

Chrome Version: asan-linux-release-311005

**REPRODUCTION CASE**  

Attached in crash.zip

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab

## Attachments

- [crash.zip](attachments/crash.zip) (application/zip, 845 B)

## Timeline

### cl...@chromium.org (2015-01-12)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5970374201180160

### cl...@chromium.org (2015-01-12)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-01-12)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5970374201180160

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x61000009af98
Crash State:
  blink::ScopedStyleResolver::collectMatchingAuthorRules
  blink::StyleResolver::matchAuthorRules
  blink::StyleResolver::matchAllRules
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=305804:305808

Minimized Testcase (0.72 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94iUOvg8uf-kPYmwsJTTO0l5w5fBm7910rJLz8dBOSQTgBBNA7C9Gybb_F7kaIgPA81PzPAiltYi-9BWL4Wcuhsg61uDAZYZVLgxlfRtvIoEbNiVjM4Zq0XV1UEGmOk73luFHyRaUhJDPOrEMRC5jd1SnJAGg



### in...@chromium.org (2015-01-12)

The result is a list of CLs that change the crashed files.

Author: tasak@google.com 
Component: blink
Changelist: https://chromium.googlesource.com/chromium/blink.git/+/26e77ca299af020de3a4a68bf3e2bfef41562140
Time: Wed Nov 26 10:37:16 2014
Lines 652-657 of file StyleEngine.cpp which potentially caused crash are changed in this cl (frame #6, "blink::StyleEngine::createSheet").

Lines 106 of file StyleEngine.cpp which potentially caused crash are changed in this cl (frame #9, "blink::StyleEngine::detachFromDocument").
Minimum distance from crash line to modified line: 0. (file: StyleEngine.cpp, crashed on: 652, modified: 652).

Suspected component: blink

### cl...@chromium.org (2015-01-12)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-01-12)

This medium+ severity security issue is a regression on trunk.

Please fix this asap. If you are unable to look into this soon, please revert your change.

- Your friendly ClusterFuzz

### ta...@chromium.org (2015-01-13)

Looking.


### ta...@chromium.org (2015-01-13)

I've finished investigating this issue.
I'm now creating a patch.


### ta...@chromium.org (2015-01-13)

I created a patch: https://codereview.chromium.org/845333003/
Now I'm trying to add a layout test.


### cl...@chromium.org (2015-01-27)

tasak@: Uh oh! This issue is still open and hasn't been updated in the last 14 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### bu...@chromium.org (2015-02-04)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=189480

------------------------------------------------------------------
r189480 | tasak@google.com | 2015-02-04T10:56:11.882779Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/html/marquee-destroyed-without-removed-from-crash-expected.txt?r1=189480&r2=189479&pathrev=189480
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/dom/StyleEngine.cpp?r1=189480&r2=189479&pathrev=189480
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/html/marquee-destroyed-without-removed-from-crash.html?r1=189480&r2=189479&pathrev=189480
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/css/resolver/ScopedStyleResolver.cpp?r1=189480&r2=189479&pathrev=189480
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/html/resources/marquee-destroyed-without-removed-from-crash.svg?r1=189480&r2=189479&pathrev=189480

StyleEngine should clear all scoped style resolvers in clearResolver.

Elements could be destroyed without removedFrom. So when document is detached, we should consider that style elements (and their own stylesheets) are not available. So we should clear all scoped style resolvers which are owned by all treescopes which are being destroyed.

Since document invokes StyleEngine::didDetach during its detach and
didDetach invokes clearResolver, clearResolver should clear all scoped
style resolvers.

BUG=447976
TEST=fast/html/marquee-destroyed-without-removed-from-crash.html

Review URL: https://codereview.chromium.org/845333003
-----------------------------------------------------------------

### cl...@chromium.org (2015-02-08)

ClusterFuzz has detected this issue as fixed in range 314621:315214.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5970374201180160

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x61000009af98
Crash State:
  blink::ScopedStyleResolver::collectMatchingAuthorRules
  blink::StyleResolver::matchAuthorRules
  blink::StyleResolver::matchAllRules
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=305804:305808
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=314621:315214

Minimized Testcase (0.72 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94iUOvg8uf-kPYmwsJTTO0l5w5fBm7910rJLz8dBOSQTgBBNA7C9Gybb_F7kaIgPA81PzPAiltYi-9BWL4Wcuhsg61uDAZYZVLgxlfRtvIoEbNiVjM4Zq0XV1UEGmOk73luFHyRaUhJDPOrEMRC5jd1SnJAGg

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### cl...@chromium.org (2015-02-11)

tasak@: Uh oh! This issue is still open and hasn't been updated in the last 28 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### ti...@google.com (2015-02-17)

Marking as fixed based on CF. 

tasak: Please reopen if there is more work to do here.

### cl...@chromium.org (2015-02-17)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

Your fix is very close to the branch point. After the branch happens, please make sure to check if your fix is in.

- Your friendly ClusterFuzz

### in...@chromium.org (2015-02-19)

[Empty comment from Monorail migration]

### ti...@google.com (2015-02-26)

Requesting merge to M41 (in case there's a patch before M42 lands - this is already in M42).

### am...@chromium.org (2015-02-26)

[Empty comment from Monorail migration]

### am...@google.com (2015-03-03)

[Automated comment] There appears to be on-going work (i.e. bugroid changes), needs manual review.

### pe...@chromium.org (2015-03-05)

Removing M41 merge request for the moment.  Tim Willis will handle security merge requests to stable, if they are important enough, and at specific times.  Hold steady on this one.


### in...@chromium.org (2015-03-05)

Penny, if you remove Merge tracking labels, Tim and me would have no way of tracking when to put it later back. Please don't remove these or use something like Merge-Triage label (which we use in security team).

### am...@google.com (2015-03-05)

[Automated comment] Request affecting a post-stable build (M41), manual review required.

### pe...@chromium.org (2015-03-05)

Inferno, I spoke to Tim about removing the Merge-Review label, and we agreed I should reject the merges for now.  This is not a security-specific tracking label like "Merge-Triage".  Merge-Review is added specifically by the TPM bot when someone adds a Merge-Requested.

We definitely needs some clarity and comms about this, and Tim is planning some procedure docs about security ticket merge processes.

I'll go ahead and add the Rejected label if that helps you.

### ti...@chromium.org (2015-03-05)

From my perspective, just adding Merge-Rejected is fine. We can figure out
a better process as part of the larger label / release management
discussion.

### ti...@google.com (2015-04-09)

Congrats - $3000 for this report.

(updating labels - this will roll out with M42)

### ti...@google.com (2015-05-06)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-05-26)

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

This issue was migrated from crbug.com/chromium/447976?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/447996, crbug.com/chromium/454281]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081158)*
