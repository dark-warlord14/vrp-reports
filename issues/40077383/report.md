# Heap-use-after-free in webkit_media::WebMediaPlayerImpl::paint

| Field | Value |
|-------|-------|
| **Issue ID** | [40077383](https://issues.chromium.org/issues/40077383) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Media |
| **Reporter** | [Deleted User] |
| **Assignee** | ac...@chromium.org |
| **Created** | 2013-04-10 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

The attached testcase (crash.html) crashes when loaded in the current ASAN chromium build. Unfortunately I wasn't able to get rid of the dependencies, svg1.svg and skeleton.ogv have to be placed in the same directory.

The ASAN output looks as follows:

==7500== ERROR: AddressSanitizer: heap-use-after-free on address 0x603400063400 at pc 0x7faace41d4c3 bp 0x7fffbc5580f0 sp 0x7fffbc5580e8  

READ of size 8 at 0x603400063400 thread T0 (chrome)  

#0 0x7faace41d4c2 in paint /b/build/slave/ASAN\_Release\_\_symbolized\_/build/webkit/media/webmediaplayer\_impl.cc:629  

#1 0x7faacbf5f5ac in paintCurrentFrameInContext /b/build/slave/ASAN\_Release\_\_symbolized\_/build/third\_party/WebKit/Source/WebKit/chromium/src/WebMediaPlayerClientImpl.cpp:628  

#2 0x7faacda4f230 in paintReplaced /b/build/slave/ASAN\_Release\_\_symbolized\_/build/third\_party/WebKit/Source/WebCore/rendering/RenderVideo.cpp:217  

#3 0x7faacd9d3bc7 in paint /b/build/slave/ASAN\_Release\_\_symbolized\_/build/third\_party/WebKit/Source/WebCore/rendering/RenderReplaced.cpp:158  

#4 0x7faacd8f8611 in paint /b/build/slave/ASAN\_Release\_\_symbolized\_/build/third\_party/WebKit/Source/WebCore/rendering/RenderImage.cpp:405  

#5 0x7faacd92e711 in paintForegroundForFragmentsWithPhase /b/build/slave/ASAN\_Release\_\_symbolized\_/build/third\_party/WebKit/Source/WebCore/rendering/RenderLayer.cpp:4032  

#6 0x7faacd92b912 in paintForegroundForFragments /b/build/slave/ASAN\_Release\_\_symbolized\_/build/third\_party/WebKit/Source/WebCore/rendering/RenderLayer.cpp:4008  

#7 0x7faacd9294d9 in paintLayerContents /b/build/slave/ASAN\_Release\_\_symbolized\_/build/third\_party/WebKit/Source/WebCore/rendering/RenderLayer.cpp:3736  

#8 0x7faacd926679 in paintLayer /b/build/slave/ASAN\_Release\_\_symbolized\_/build/third\_party/WebKit/Source/WebCore/rendering/RenderLayer.cpp:3538  

#9 0x7faacd92b690 in paintList /b/build/slave/ASAN\_Release\_\_symbolized\_/build/third\_party/WebKit/Source/WebCore/rendering/RenderLayer.cpp:3825  

#10 0x7faacd929539 in paintLayerContents /b/build/slave/ASAN\_Release\_\_symbolized\_/build/third\_party/WebKit/Source/WebCore/rendering/RenderLayer.cpp:3745  

#11 0x7faacd926679 in paintLayer /b/build/slave/ASAN\_Release\_\_symbolized\_/build/third\_party/WebKit/Source/WebCore/rendering/RenderLayer.cpp:3538  

#12 0x7faacd92b690 in paintList /b/build/slave/ASAN\_Release\_\_symbolized\_/build/third\_party/WebKit/Source/WebCore/rendering/RenderLayer.cpp:3825  

#13 0x7faacd929558 in paintLayerContents /b/build/slave/ASAN\_Release\_\_symbolized\_/build/third\_party/WebKit/Source/WebCore/rendering/RenderLayer.cpp:3748  

#14 0x7faacd926679 in paintLayer /b/build/slave/ASAN\_Release\_\_symbolized\_/build/third\_party/WebKit/Source/WebCore/rendering/RenderLayer.cpp:3538  

#15 0x7faacd926210 in paint /b/build/slave/ASAN\_Release\_\_symbolized\_/build/third\_party/WebKit/Source/WebCore/rendering/RenderLayer.cpp:3362  

#16 0x7faacd3f49ca in paintContents /b/build/slave/ASAN\_Release\_\_symbolized\_/build/third\_party/WebKit/Source/WebCore/page/FrameView.cpp:3165  

#17 0x7faaccc6a656 in paint /b/build/slave/ASAN\_Release\_\_symbolized\_/build/third\_party/WebKit/Source/WebCore/platform/ScrollView.cpp:962  

#18 0x7faacbff3573 in paint /b/build/slave/ASAN\_Release\_\_symbolized\_/build/third\_party/WebKit/Source/WebKit/chromium/src/PageWidgetDelegate.cpp:97  

#19 0x7faacbf894c8 in paint /b/build/slave/ASAN\_Release\_\_symbolized\_/build/third\_party/WebKit/Source/WebKit/chromium/src/WebViewImpl.cpp:1888  

#20 0x7faacf54a2d7 in PaintRect /b/build/slave/ASAN\_Release\_\_symbolized\_/build/content/renderer/render\_widget.cc:904  

#21 0x7faacf5415ca in DoDeferredUpdate /b/build/slave/ASAN\_Release\_\_symbolized\_/build/content/renderer/render\_widget.cc:1228  

#22 0x7faacf547f81 in DoDeferredUpdateAndSendInputAck /b/build/slave/ASAN\_Release\_\_symbolized\_/build/content/renderer/render\_widget.cc:1036  

#23 0x7faacf54b6ed in InvalidationCallback /b/build/slave/ASAN\_Release\_\_symbolized\_/build/content/renderer/render\_widget.cc:1032  

#24 0x7faacf55844f in MakeItSo /b/build/slave/ASAN\_Release\_\_symbolized\_/build/./base/bind\_internal.h:871  

#25 0x7faacad5c664 in RunTask /b/build/slave/ASAN\_Release\_\_symbolized\_/build/base/message\_loop.cc:474  

#26 0x7faacad5ce7b in DeferOrRunPendingTask /b/build/slave/ASAN\_Release\_\_symbolized\_/build/base/message\_loop.cc:486  

#27 0x7faacad5d101 in DoWork /b/build/slave/ASAN\_Release\_\_symbolized\_/build/base/message\_loop.cc:669  

#28 0x7faacad68c1c in Run /b/build/slave/ASAN\_Release\_\_symbolized\_/build/base/message\_pump\_default.cc:29  

#29 0x7faacad5bdb7 in RunInternal /b/build/slave/ASAN\_Release\_\_symbolized\_/build/base/message\_loop.cc:431  

#30 0x7faacad9a989 in Run /b/build/slave/ASAN\_Release\_\_symbolized\_/build/base/run\_loop.cc:45  

#31 0x7faacad5ab21 in Run /b/build/slave/ASAN\_Release\_\_symbolized\_/build/base/message\_loop.cc:311  

#32 0x7faacf55dbb8 in RendererMain /b/build/slave/ASAN\_Release\_\_symbolized\_/build/content/renderer/renderer\_main.cc:226  

#33 0x7faacaaf14d3 in RunZygote /b/build/slave/ASAN\_Release\_\_symbolized\_/build/content/app/content\_main\_runner.cc:411  

#34 0x7faacaaf1dd3 in RunNamedProcessTypeMain /b/build/slave/ASAN\_Release\_\_symbolized\_/build/content/app/content\_main\_runner.cc:467  

#35 0x7faacaaf2aca in Run /b/build/slave/ASAN\_Release\_\_symbolized\_/build/content/app/content\_main\_runner.cc:764  

#36 0x7faacaaf0bfb in ContentMain /b/build/slave/ASAN\_Release\_\_symbolized\_/build/content/app/content\_main.cc:35  

#37 0x7faac9d2d82a in ChromeMain /b/build/slave/ASAN\_Release\_\_symbolized\_/build/chrome/app/chrome\_main.cc:32  

#38 0x7faac9d2d77a in main /b/build/slave/ASAN\_Release\_\_symbolized\_/build/chrome/app/chrome\_exe\_main\_gtk.cc:34  

#39 0x7faac29ed76c in **libc\_start\_main /build/buildd/eglibc-2.15/csu/libc-start.c:226  

#40 0x7faac9d2d6a4 in *start ??:0  

0x603400063400 is located 0 bytes inside of 456-byte region [0x603400063400,0x6034000635c8)  

freed by thread T0 (chrome) here:  

#0 0x7faac9d21892 in free ??:0  

#1 0x7faacd2dd3cb in ~FrameLoader /b/build/slave/ASAN\_Release\_\_symbolized*/build/third\_party/WebKit/Source/WebCore/loader/FrameLoader.cpp:245  

#2 0x7faacd3d75d8 in ~Frame /b/build/slave/ASAN\_Release\_\_symbolized*/build/third\_party/WebKit/Source/WebCore/page/Frame.cpp:210  

#3 0x7faacbf430b5 in deref /b/build/slave/ASAN\_Release\_\_symbolized*/build/third\_party/WebKit/Source/WTF/wtf/RefCounted.h:202  

#4 0x7faacd3e31ec in derefIfNotNull[WebCore::Frame](javascript:void(0);) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/third\_party/WebKit/Source/WTF/wtf/PassRefPtr.h:45  

#5 0x7faacd3e2ecd in ~FrameView /b/build/slave/ASAN\_Release\_\_symbolized\_/build/third\_party/WebKit/Source/WebCore/page/FrameView.cpp:225  

#6 0x7faacda68553 in deallocateTable /b/build/slave/ASAN\_Release\_\_symbolized\_/build/third\_party/WebKit/Source/WTF/wtf/HashTable.h:1089  

#7 0x7faacda626bb in moveWidgets /b/build/slave/ASAN\_Release\_\_symbolized\_/build/third\_party/WebKit/Source/WebCore/rendering/RenderWidget.cpp:72  

#8 0x7faacc0a9c46 in ~WidgetHierarchyUpdatesSuspensionScope /b/build/slave/ASAN\_Release\_\_symbolized\_/build/third\_party/WebKit/Source/WebCore/rendering/RenderWidget.h:41  

#9 0x7faacc0a46ef in removeChild /b/build/slave/ASAN\_Release\_\_symbolized\_/build/third\_party/WebKit/Source/WebCore/dom/ContainerNode.cpp:518  

#10 0x7faacc0a32c7 in collectChildrenAndRemoveFromOldParent /b/build/slave/ASAN\_Release\_\_symbolized\_/build/third\_party/WebKit/Source/WebCore/dom/ContainerNode.cpp:81  

#11 0x7faacc0a2ef8 in appendChild /b/build/slave/ASAN\_Release\_\_symbolized\_/build/third\_party/WebKit/Source/WebCore/dom/ContainerNode.cpp:653  

#12 0x7faacc185c88 in appendChild /b/build/slave/ASAN\_Release\_\_symbolized\_/build/third\_party/WebKit/Source/WebCore/dom/Node.cpp:574  

#13 0x7faacdfeeff5 in appendChildMethodCustom /b/build/slave/ASAN\_Release\_\_symbolized\_/build/third\_party/WebKit/Source/bindings/v8/custom/V8NodeCustom.cpp:116  

#14 0x7faacc5583b3 in HandleApiCallHelper<false> /b/build/slave/ASAN\_Release\_\_symbolized\_/build/v8/src/builtins.cc:1327  

#15 0x2df640d0654d in  

#16 0x2df640d87516 in  

#17 0x2df640d873f7 in  

#18 0x2df640d26003 in  

#19 0x2df640d0c336 in  

#20 0x7faacc5a5811 in Invoke /b/build/slave/ASAN\_Release\_\_symbolized\_/build/v8/src/execution.cc:118  

#21 0x7faacc513e6e in Run /b/build/slave/ASAN\_Release\_\_symbolized\_/build/v8/src/api.cc:1815  

#22 0x7faacdf785f8 in runCompiledScript /b/build/slave/ASAN\_Release\_\_symbolized\_/build/third\_party/WebKit/Source/bindings/v8/ScriptRunner.cpp:52  

#23 0x7faacdf5fd70 in compileAndRunScript /b/build/slave/ASAN\_Release\_\_symbolized\_/build/third\_party/WebKit/Source/bindings/v8/ScriptController.cpp:288  

#24 0x7faacdf5bfc5 in execute /b/build/slave/ASAN\_Release\_\_symbolized\_/build/third\_party/WebKit/Source/bindings/v8/ScheduledAction.cpp:109  

#25 0x7faacd391b18 in fired /b/build/slave/ASAN\_Release\_\_symbolized\_/build/third\_party/WebKit/Source/WebCore/page/DOMTimer.cpp:141  

#26 0x7faaccc82ef5 in sharedTimerFiredInternal /b/build/slave/ASAN\_Release\_\_symbolized\_/build/third\_party/WebKit/Source/WebCore/platform/ThreadTimers.cpp:129  

#27 0x7faace356f9e in MakeItSo /b/build/slave/ASAN\_Release\_\_symbolized\_/build/./base/bind\_internal.h:871  

#28 0x7faace356d97 in Run /b/build/slave/ASAN\_Release\_\_symbolized\_/build/./base/bind\_internal.h:1173  

#29 0x7faacadde582 in RunScheduledTask /b/build/slave/ASAN\_Release\_\_symbolized\_/build/base/timer.cc:181  

previously allocated by thread T0 (chrome) here:  

#0 0x7faac9d21972 in malloc ??:0  

#1 0x7faacc05d4f8 in fastMalloc /b/build/slave/ASAN\_Release\_\_symbolized\_/build/third\_party/WebKit/Source/WTF/wtf/FastMalloc.cpp:280  

#2 0x7faacbf4112b in createChildFrame /b/build/slave/ASAN\_Release\_\_symbolized\_/build/third\_party/WebKit/Source/WebKit/chromium/src/WebFrameImpl.cpp:2167  

#3 0x7faacbfe0ab4 in createFrame /b/build/slave/ASAN\_Release\_\_symbolized\_/build/third\_party/WebKit/Source/WebKit/chromium/src/FrameLoaderClientImpl.cpp:1464  

#4 0x7faacd31c370 in loadSubframe /b/build/slave/ASAN\_Release\_\_symbolized\_/build/third\_party/WebKit/Source/WebCore/loader/SubframeLoader.cpp:260  

#5 0x7faacd31a75f in loadOrRedirectSubframe /b/build/slave/ASAN\_Release\_\_symbolized\_/build/third\_party/WebKit/Source/WebCore/loader/SubframeLoader.cpp:234  

#6 0x7faacd31a48e in requestFrame /b/build/slave/ASAN\_Release\_\_symbolized\_/build/third\_party/WebKit/Source/WebCore/loader/SubframeLoader.cpp:83  

#7 0x7faad0de815f in openURL /b/build/slave/ASAN\_Release\_\_symbolized\_/build/third\_party/WebKit/Source/WebCore/html/HTMLFrameElementBase.cpp:88  

#8 0x7faacc0a3d43 in notify /b/build/slave/ASAN\_Release\_\_symbolized\_/build/third\_party/WebKit/Source/WebCore/dom/ContainerNodeAlgorithms.h:229  

#9 0x7faacc0a3614 in updateTreeAfterInsertion /b/build/slave/ASAN\_Release\_\_symbolized\_/build/third\_party/WebKit/Source/WebCore/dom/ContainerNode.cpp:948  

#10 0x7faacc0a2fb9 in appendChild /b/build/slave/ASAN\_Release\_\_symbolized\_/build/third\_party/WebKit/Source/WebCore/dom/ContainerNode.cpp:685  

#11 0x7faacc185c88 in appendChild /b/build/slave/ASAN\_Release\_\_symbolized\_/build/third\_party/WebKit/Source/WebCore/dom/Node.cpp:574  

#12 0x7faacdfeeff5 in appendChildMethodCustom /b/build/slave/ASAN\_Release\_\_symbolized\_/build/third\_party/WebKit/Source/bindings/v8/custom/V8NodeCustom.cpp:116  

#13 0x7faacc5583b3 in HandleApiCallHelper<false> /b/build/slave/ASAN\_Release\_\_symbolized\_/build/v8/src/builtins.cc:1327  

#14 0x2df640d0654d in  

#15 0x2df640d45849 in  

#16 0x2df640d45687 in  

#17 0x2df640d26003 in  

#18 0x2df640d0c336 in  

#19 0x7faacc5a5811 in Invoke /b/build/slave/ASAN\_Release\_\_symbolized\_/build/v8/src/execution.cc:118  

#20 0x7faacc5202e2 in Call /b/build/slave/ASAN\_Release\_\_symbolized\_/build/v8/src/api.cc:3891  

#21 0x7faacdf5f367 in callFunctionWithInstrumentation /b/build/slave/ASAN\_Release\_\_symbolized\_/build/third\_party/WebKit/Source/bindings/v8/ScriptController.cpp:240  

#22 0x7faacdf5f082 in callFunction /b/build/slave/ASAN\_Release\_\_symbolized\_/build/third\_party/WebKit/Source/bindings/v8/ScriptController.cpp:193  

#23 0x7faacdf9b97e in callListenerFunction /b/build/slave/ASAN\_Release\_\_symbolized\_/build/third\_party/WebKit/Source/bindings/v8/V8LazyEventListener.cpp:103  

#24 0x7faace111da6 in invokeEventHandler /b/build/slave/ASAN\_Release\_\_symbolized\_/build/third\_party/WebKit/Source/bindings/v8/V8AbstractEventListener.cpp:138  

#25 0x7faace111b6a in handleEvent /b/build/slave/ASAN\_Release\_\_symbolized\_/build/third\_party/WebKit/Source/bindings/v8/V8AbstractEventListener.cpp:98  

#26 0x7faacc166ad3 in fireEventListeners /b/build/slave/ASAN\_Release\_\_symbolized\_/build/third\_party/WebKit/Source/WebCore/dom/EventTarget.cpp:257  

#27 0x7faacc16648d in fireEventListeners /b/build/slave/ASAN\_Release\_\_symbolized\_/build/third\_party/WebKit/Source/WebCore/dom/EventTarget.cpp:203  

#28 0x7faacd394818 in dispatchEvent /b/build/slave/ASAN\_Release\_\_symbolized\_/build/third\_party/WebKit/Source/WebCore/page/DOMWindow.cpp:1695  

#29 0x7faacd39f980 in dispatchLoadEvent /b/build/slave/ASAN\_Release\_\_symbolized\_/build/third\_party/WebKit/Source/WebCore/page/DOMWindow.cpp:1669  

Shadow bytes around the buggy address:  

0x0c0700004630: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c0700004640: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c0700004650: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c0700004660: fd fd fd fd fd fd fd fd fd fd fd fd fa fa fa fa  

0x0c0700004670: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

=>0x0c0700004680:[fd]fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c0700004690: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c07000046a0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c07000046b0: fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa  

0x0c07000046c0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c07000046d0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

Shadow byte legend (one shadow byte represents 8 application bytes):  

Addressable: 00  

Partially addressable: 01 02 03 04 05 06 07  

Heap left redzone: fa  

Heap righ redzone: fb  

Freed Heap region: fd  

Stack left redzone: f1  

Stack mid redzone: f2  

Stack right redzone: f3  

Stack partial redzone: f4  

Stack after return: f5  

Stack use after scope: f8  

Global redzone: f9  

Global init order: f6  

Poisoned by user: f7  

ASan internal: fe  

==7500== ABORTING

**VERSION**  

Tested with ASAN build of chromium (193330) under Linux

**REPRODUCTION CASE**  

All required files attached.

## Attachments

- [crash.html](attachments/crash.html) (text/html; charset=us-ascii, 881 B)
- [svg1.svg](attachments/svg1.svg) (text/plain; charset=us-ascii, 44 B)
- [skeleton.ogv](attachments/skeleton.ogv) (application/ogg; charset=binary, 32.7 KB)
- [skeleton.html](attachments/skeleton.html) (text/plain; charset=us-ascii, 35 B)
- [crash2.html](attachments/crash2.html) (text/html; charset=us-ascii, 915 B)

## Timeline

### me...@google.com (2013-04-11)

I wasn't able to reproduce this on my local ASAN build or on ClusterFuzz. 

@scherkus: Could you or someone else on the media side take a look at this and confirm?

### me...@google.com (2013-04-11)

[Empty comment from Monorail migration]

### js...@chromium.org (2013-04-11)

This was a very recent revision, so it looks like it's just trunk churn. I'm closing it out, but please pull a new revision and I'll reopen if you're still hitting it.

### [Deleted User] (2013-04-11)

Yes, can't repro in the latest version. Which is the best version to do fuzzing on?

### sc...@gmail.com (2013-04-12)

@nils: hard to say. If you're looking to validate a new fuzzer, you might consider pulling the M26 (stable) branch, which shouldn't have any transient regressions.

Other than that, the version corresponding to a latest dev channel is a good choice.

### [Deleted User] (2013-04-13)

Cool, have moved to fuzzing stable for now and have hit a very similar issue, it wraps the video in a html file (skeleton.html, attached).

I don't seem to be able to re-open this issue.

Crashes the stable asan build, asan output below:

READ of size 8 at 0x7f0be5640440 thread T0 (chrome)
    #0 0x7f0bf64106ac in paint /mnt/scratch0/tmpbuild/src/out/Release/../../webkit/media/webmediaplayer_impl.cc:579
    #1 0x7f0bf5fcb55a in paintCurrentFrameInContext /mnt/scratch0/tmpbuild/src/out/Release/../../third_party/WebKit/Source/WebKit/chromium/src/WebMediaPlayerClientImpl.cpp:690
    #2 0x7f0bfcaf97f2 in paintReplaced /mnt/scratch0/tmpbuild/src/out/Release/../../third_party/WebKit/Source/WebCore/rendering/RenderVideo.cpp:220
    #3 0x7f0bfca199db in paint /mnt/scratch0/tmpbuild/src/out/Release/../../third_party/WebKit/Source/WebCore/rendering/RenderReplaced.cpp:157
    #4 0x7f0bfc864ce1 in paint /mnt/scratch0/tmpbuild/src/out/Release/../../third_party/WebKit/Source/WebCore/rendering/RenderImage.cpp:406
    #5 0x7f0bfc8c4fe4 in paintLayerContents /mnt/scratch0/tmpbuild/src/out/Release/../../third_party/WebKit/Source/WebCore/rendering/RenderLayer.cpp:3792
    #6 0x7f0bfc8bf1b6 in paintLayerContentsAndReflection /mnt/scratch0/tmpbuild/src/out/Release/../../third_party/WebKit/Source/WebCore/rendering/RenderLayer.cpp:3588
    #7 0x7f0bfc8c9f3d in paintList /mnt/scratch0/tmpbuild/src/out/Release/../../third_party/WebKit/Source/WebCore/rendering/RenderLayer.cpp:3880
    #8 0x7f0bfc8c5807 in paintLayerContents /mnt/scratch0/tmpbuild/src/out/Release/../../third_party/WebKit/Source/WebCore/rendering/RenderLayer.cpp:3812
    #9 0x7f0bfc8bf1b6 in paintLayerContentsAndReflection /mnt/scratch0/tmpbuild/src/out/Release/../../third_party/WebKit/Source/WebCore/rendering/RenderLayer.cpp:3588
    #10 0x7f0bfc8c9f3d in paintList /mnt/scratch0/tmpbuild/src/out/Release/../../third_party/WebKit/Source/WebCore/rendering/RenderLayer.cpp:3880
    #11 0x7f0bfc8c583c in paintLayerContents /mnt/scratch0/tmpbuild/src/out/Release/../../third_party/WebKit/Source/WebCore/rendering/RenderLayer.cpp:3815
    #12 0x7f0bfc8bf1b6 in paintLayerContentsAndReflection /mnt/scratch0/tmpbuild/src/out/Release/../../third_party/WebKit/Source/WebCore/rendering/RenderLayer.cpp:3588
    #13 0x7f0bfc8be669 in paint /mnt/scratch0/tmpbuild/src/out/Release/../../third_party/WebKit/Source/WebCore/rendering/RenderLayer.cpp:3371
    #14 0x7f0bf887d754 in paintContents /mnt/scratch0/tmpbuild/src/out/Release/../../third_party/WebKit/Source/WebCore/page/FrameView.cpp:3335
    #15 0x7f0bfb295d16 in paint /mnt/scratch0/tmpbuild/src/out/Release/../../third_party/WebKit/Source/WebCore/platform/ScrollView.cpp:1087
    #16 0x7f0bf608f72d in paint /mnt/scratch0/tmpbuild/src/out/Release/../../third_party/WebKit/Source/WebKit/chromium/src/PageWidgetDelegate.cpp:101
    #17 0x7f0bf5ffa176 in paint /mnt/scratch0/tmpbuild/src/out/Release/../../third_party/WebKit/Source/WebKit/chromium/src/WebViewImpl.cpp:1953
    #18 0x7f0bfa734beb in PaintRect /mnt/scratch0/tmpbuild/src/out/Release/../../content/renderer/render_widget.cc:833
    #19 0x7f0bfa72943c in DoDeferredUpdate /mnt/scratch0/tmpbuild/src/out/Release/../../content/renderer/render_widget.cc:1156
    #20 0x7f0bfa736fc2 in DoDeferredUpdateAndSendInputAck /mnt/scratch0/tmpbuild/src/out/Release/../../content/renderer/render_widget.cc:964
    #21 0x7f0bf672c610 in Run /mnt/scratch0/tmpbuild/src/out/Release/../../base/callback.h:396
    #22 0x7f0bf672cc7f in DeferOrRunPendingTask /mnt/scratch0/tmpbuild/src/out/Release/../../base/message_loop.cc:488
    #23 0x7f0bf672d9c1 in DoWork /mnt/scratch0/tmpbuild/src/out/Release/../../base/message_loop.cc:671
    #24 0x7f0bf6738316 in Run /mnt/scratch0/tmpbuild/src/out/Release/../../base/message_pump_default.cc:29
    #25 0x7f0bf672b473 in RunInternal /mnt/scratch0/tmpbuild/src/out/Release/../../base/message_loop.cc:433
    #26 0x7f0bf6770171 in Run /mnt/scratch0/tmpbuild/src/out/Release/../../base/run_loop.cc:45
    #27 0x7f0bf6729827 in Run /mnt/scratch0/tmpbuild/src/out/Release/../../base/message_loop.cc:313
    #28 0x7f0bfa74e735 in RendererMain /mnt/scratch0/tmpbuild/src/out/Release/../../content/renderer/renderer_main.cc:226
    #29 0x7f0bfa68665e in RunZygote /mnt/scratch0/tmpbuild/src/out/Release/../../content/app/content_main_runner.cc:402
    #30 0x7f0bfa6879fa in RunNamedProcessTypeMain /mnt/scratch0/tmpbuild/src/out/Release/../../content/app/content_main_runner.cc:458
    #31 0x7f0bfa688f89 in Run /mnt/scratch0/tmpbuild/src/out/Release/../../content/app/content_main_runner.cc:754
    #32 0x7f0bfa685dd7 in ContentMain /mnt/scratch0/tmpbuild/src/out/Release/../../content/app/content_main.cc:35
    #33 0x7f0bf47744c0 in ChromeMain /mnt/scratch0/tmpbuild/src/out/Release/../../chrome/app/chrome_main.cc:32
    #34 0x7f0bf477441a in main /mnt/scratch0/tmpbuild/src/out/Release/../../chrome/app/chrome_exe_main_gtk.cc:31
    #35 0x7f0bed47b76c in __libc_start_main /build/buildd/eglibc-2.15/csu/libc-start.c:226
0x7f0be5640440 is located 0 bytes inside of 472-byte region [0x7f0be5640440,0x7f0be5640618)
freed by thread T0 (chrome) here:
    #0 0x7f0bf476b5b2 in free ??:0
    #1 0x7f0bf86baab2 in ~FrameLoader /mnt/scratch0/tmpbuild/src/out/Release/../../third_party/WebKit/Source/WebCore/loader/FrameLoader.cpp:250
    #2 0x7f0bf884f259 in ~Frame /mnt/scratch0/tmpbuild/src/out/Release/../../third_party/WebKit/Source/WebCore/page/Frame.cpp:229
    #3 0x7f0bf885e62b in deref /mnt/scratch0/tmpbuild/src/out/Release/../../third_party/WebKit/Source/WTF/wtf/RefCounted.h:202
    #4 0x7f0bf885dd1d in ~FrameView /mnt/scratch0/tmpbuild/src/out/Release/../../third_party/WebKit/Source/WebCore/page/FrameView.cpp:234
    #5 0x7f0bfcb0fc98 in deref /mnt/scratch0/tmpbuild/src/out/Release/../../third_party/WebKit/Source/WTF/wtf/RefCounted.h:202
    #6 0x7f0bf9193f35 in ~WidgetHierarchyUpdatesSuspensionScope /mnt/scratch0/tmpbuild/src/out/Release/../../third_party/WebKit/Source/WebCore/rendering/RenderWidget.h:41
    #7 0x7f0bf918f226 in collectChildrenAndRemoveFromOldParent /mnt/scratch0/tmpbuild/src/out/Release/../../third_party/WebKit/Source/WebCore/dom/ContainerNode.cpp:87
    #8 0x7f0bf918e4ef in appendChild /mnt/scratch0/tmpbuild/src/out/Release/../../third_party/WebKit/Source/WebCore/dom/ContainerNode.cpp:671
    #9 0x7f0bf92a3337 in appendChild /mnt/scratch0/tmpbuild/src/out/Release/../../third_party/WebKit/Source/WebCore/dom/Node.cpp:571
    #10 0x7f0bf815cf50 in appendChildCallback /mnt/scratch0/tmpbuild/src/out/Release/../../third_party/WebKit/Source/WebCore/bindings/v8/custom/V8NodeCustom.cpp:116
    #11 0x7f0bfb68cec0 in HandleApiCallHelper<false> /mnt/scratch0/tmpbuild/src/out/Release/../../v8/src/builtins.cc:1350
addr2line: '': No such file
    #12 0xc81e72062ed in  
    #13 0xc81e7250aa6 in  
previously allocated by thread T0 (chrome) here:
    #0 0x7f0bf476b692 in malloc ??:0
    #1 0x7f0bfc58a288 in fastMalloc /mnt/scratch0/tmpbuild/src/out/Release/../../third_party/WebKit/Source/WTF/wtf/FastMalloc.cpp:283
    #2 0x7f0bf5fb5179 in operator new /mnt/scratch0/tmpbuild/src/out/Release/../../third_party/WebKit/Source/WTF/wtf/RefCounted.h:197
    #3 0x7f0bf607a70d in createFrame /mnt/scratch0/tmpbuild/src/out/Release/../../third_party/WebKit/Source/WebKit/chromium/src/FrameLoaderClientImpl.cpp:1477
    #4 0x7f0bf8737726 in loadSubframe /mnt/scratch0/tmpbuild/src/out/Release/../../third_party/WebKit/Source/WebCore/loader/SubframeLoader.cpp:367
    #5 0x7f0bf8732103 in loadOrRedirectSubframe /mnt/scratch0/tmpbuild/src/out/Release/../../third_party/WebKit/Source/WebCore/loader/SubframeLoader.cpp:341
    #6 0x7f0bf8731ade in requestFrame /mnt/scratch0/tmpbuild/src/out/Release/../../third_party/WebKit/Source/WebCore/loader/SubframeLoader.cpp:87
    #7 0x7f0bfd35caf5 in openURL /mnt/scratch0/tmpbuild/src/out/Release/../../third_party/WebKit/Source/WebCore/html/HTMLFrameElementBase.cpp:88
    #8 0x7f0bfd35efdb in didNotifySubtreeInsertions /mnt/scratch0/tmpbuild/src/out/Release/../../third_party/WebKit/Source/WebCore/html/HTMLFrameElementBase.cpp:172
Shadow byte and word:
  0x1fe17cac8088: fd
  0x1fe17cac8088: fd fd fd fd fd fd fd fd
More shadow bytes:
  0x1fe17cac8068: fa fa fa fa fa fa fa fa
  0x1fe17cac8070: fa fa fa fa fa fa fa fa
  0x1fe17cac8078: fa fa fa fa fa fa fa fa
  0x1fe17cac8080: fa fa fa fa fa fa fa fa
=>0x1fe17cac8088: fd fd fd fd fd fd fd fd
  0x1fe17cac8090: fd fd fd fd fd fd fd fd
  0x1fe17cac8098: fd fd fd fd fd fd fd fd
  0x1fe17cac80a0: fd fd fd fd fd fd fd fd
  0x1fe17cac80a8: fd fd fd fd fd fd fd fd
Stats: 31M malloced (28M for red zones) by 41737 calls
Stats: 7M realloced by 1012 calls
Stats: 23M freed by 28939 calls
Stats: 21M really freed by 24206 calls
Stats: 27M (6952 full pages) mmaped in 53 calls
  mmaps   by size class: 7:20475; 8:4094; 9:2046; 10:1022; 11:510; 12:256; 13:128; 14:192; 15:304; 16:48; 17:8; 18:2; 19:1; 20:1;
  mallocs by size class: 7:28037; 8:5673; 9:1655; 10:3572; 11:728; 12:389; 13:268; 14:668; 15:580; 16:137; 17:15; 18:7; 19:7; 20:1;
  frees   by size class: 7:18190; 8:4077; 9:1223; 10:3358; 11:530; 12:265; 13:225; 14:624; 15:314; 16:105; 17:13; 18:7; 19:7; 20:1;
  rfrees  by size class: 7:15034; 8:3304; 9:1053; 10:3010; 11:439; 12:202; 13:179; 14:575; 15:283; 16:99; 17:13; 18:7; 19:7; 20:1;
Stats: malloc large: 747 small slow: 847
==3786== ABORTING


### sc...@gmail.com (2013-04-14)

Re-opening, thank you.

### me...@google.com (2013-04-15)

@nils: The new repro doesn't reproduce for me either. What exact revision are you testing on?

### sc...@chromium.org (2013-04-16)

acolwell/japhet: I can't tell .. does this look similar to https://crbug.com/chromium/177620 where we have loader code involved?

### [Deleted User] (2013-04-16)

I was testing with an ASAN Linux build of Version 26.0.1410.63 (192696).

The testcase was loaded from a file:// URL and I used the flag: --allow-file-access-from-files maybe that will affect it, especially if it is a timing issue.

### ac...@chromium.org (2013-04-16)

@scherkus on the surface this does not look the same as https://crbug.com/chromium/177620. The best way to be sure though is to put print statements at the beginning and end of ~HTMLMediaElement. A common situation for https://crbug.com/chromium/177620 was the destructor would not complete executing before V8 transfered control to other code via dispatchEvent(). If you see the clearMediaPlayer(-1) call start, but not complete before you see the offending use-after-free then this may be a related bug.

### in...@chromium.org (2013-04-16)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=178588083

Uploader: cdn@chromium.org

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x603200029840
Crash State:
  - crash stack -
  webkit_media::WebMediaPlayerImpl::paint
  WebKit::WebMediaPlayerClientImpl::paintCurrentFrameInContext
  - free stack -
  WebCore::FrameLoader::~FrameLoader
  WebCore::Frame::~Frame
  

Minimized Testcase (31.25 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94JT6t5XTfsz3xsVBYKvKQPIFFXv5ov7vPCndQv294uAugX2uK7ORFtmiEv8fRT1s70ZPkCDI6nyQFmNUgJDZmaS7qDrVUg7zvWsklws6sKOPua55L9vnF3LGRtVFTQFWnXtRZTSeGgA9g9OniLuZM_0k_kPKSU6ZRxp3DybkPYgmWUqHM

### in...@chromium.org (2013-04-16)

regression range will come soon.

### in...@chromium.org (2013-04-18)

Dale, this is a high severity external report. Can you please help with an owner for this one.

### da...@chromium.org (2013-04-18)

[Empty comment from Monorail migration]

### ac...@chromium.org (2013-04-20)

inferno@ : I just posted the fix for this bug (https://codereview.chromium.org/14127004/). The WebMediaPlayerImpl instance was accessing the WebFrameImpl after it was destroyed. 

The fix is simply to force the player to get cleaned up when the pending destruction of WebFrameImpl tries to stop all the ActiveDOMObjects. I'm not really sure why clearMediaPlayer() wasn't always being called in this case.

### cl...@chromium.org (2013-04-20)

ClusterFuzz has detected this issue as fixed in range 195296:195394.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=178588083

Uploader: cdn@chromium.org

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x603200029840
Crash State:
  - crash stack -
  webkit_media::WebMediaPlayerImpl::paint
  WebKit::WebMediaPlayerClientImpl::paintCurrentFrameInContext
  - free stack -
  WebCore::FrameLoader::~FrameLoader
  WebCore::Frame::~Frame
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=159577:159613
Fixed: https://cluster-fuzz.appspot.com/revisions?range=195296:195394

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv94JT6t5XTfsz3xsVBYKvKQPIFFXv5ov7vPCndQv294uAugX2uK7ORFtmiEv8fRT1s70ZPkCDI6nyQFmNUgJDZmaS7qDrVUg7zvWsklws6sKOPua55L9vnF3LGRtVFTQFWnXtRZTSeGgA9g9OniLuZM_0k_kPKSU6ZRxp3DybkPYgmWUqHM

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### [Deleted User] (2013-04-21)

Should this be fixed in the this build: "asan-symbolized-linux-release-195402" ?

I am still getting crashes with the same signature.

### in...@chromium.org (2013-04-21)

Ignore the last ClusterFuzz which says fixed in range "195296:195394". Looks like a bad build sneeked in [clang roll] and ASAN stopped working. Things look fine on trunk, so i clicked redo on ClusterFuzz reports.

### cl...@chromium.org (2013-04-21)

[Comment Deleted]

### sc...@gmail.com (2013-04-21)

@nils: ClusterFuzz has gone crazy! The fix hasn't landed yet.

### cl...@chromium.org (2013-04-21)

[Comment Deleted]

### ac...@chromium.org (2013-05-01)

So here is the latest news. I'm still not able to get DumpRenderTree to reproduce the paint calls that trigger the crash, but I am able to reliably reproduce the crash in Chrome. https://codereview.chromium.org/14127004/ is a viable short term fix that will avoid several possible use-after-free situations that can occur when elements in an iframe are pulled out of the iframe and placed in the parent document. 

In the long term though several fixes will need to be made. I've discovered that elements that derive from ActiveDOMObject, like <video> and <marquee>, are not properly handling being removed from one document and added to another. In the case of <marquee> it just causes the element not to display. In the case of <video> the WebMediaPlayer and ActiveURLLoader are holding on to references to objects from the iframe they were originally created in which is what causes the use-after-free when the iframe is removed from the document. It is going to take some time to figure out a proper solution for reinitializing WebMediaPlayer and ActiveURLLoader with the proper objects from the element's new document so I suggest we just land the quick fix now, and I'll continue working on the proper fix.

### bu...@chromium.org (2013-05-01)

------------------------------------------------------------------------
r149537 | acolwell@chromium.org | 2013-05-01T20:21:20.394687Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/html/HTMLMediaElement.cpp?r1=149537&r2=149536&pathrev=149537
   A http://src.chromium.org/viewvc/blink/trunk/ManualTests/media-elements/video-iframe.html?r1=149537&r2=149536&pathrev=149537
   A http://src.chromium.org/viewvc/blink/trunk/ManualTests/media-elements/video-moved-from-iframe-to-main-page.html?r1=149537&r2=149536&pathrev=149537

Change HTMLMediaElement::userCancelledLoad() to always call clearMediaPlayer()

HTMLMediaElement::userCancelledLoad() is only called when Blink is trying to stop
all the ActiveDOMObjects. In all cases where that happens we want to make sure that
m_player is cleared so that nothing from MediaPlayer and below will access WebCore
objects.

BUG=230117

Review URL: https://chromiumcodereview.appspot.com/14127004
------------------------------------------------------------------------

### in...@chromium.org (2013-05-01)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-05-02)

Nice work @acolwell

### sc...@gmail.com (2013-05-03)

@nils: welcome to the Chromium VRP ;-)
This qualifies for a $1000 reward! Thanks for making the repro nice and small (bad repros lead to $500 rewards ;-)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties.


### cl...@chromium.org (2013-05-03)

ClusterFuzz has detected this issue as fixed in range 197479:197876.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=178588083

Uploader: cdn@chromium.org

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x603200029840
Crash State:
  - crash stack -
  webkit_media::WebMediaPlayerImpl::paint
  WebKit::WebMediaPlayerClientImpl::paintCurrentFrameInContext
  - free stack -
  WebCore::FrameLoader::~FrameLoader
  WebCore::Frame::~Frame
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=159577:159613
Fixed: https://cluster-fuzz.appspot.com/revisions?range=197479:197876

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv94JT6t5XTfsz3xsVBYKvKQPIFFXv5ov7vPCndQv294uAugX2uK7ORFtmiEv8fRT1s70ZPkCDI6nyQFmNUgJDZmaS7qDrVUg7zvWsklws6sKOPua55L9vnF3LGRtVFTQFWnXtRZTSeGgA9g9OniLuZM_0k_kPKSU6ZRxp3DybkPYgmWUqHM

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### sc...@gmail.com (2013-05-06)

M27 is https://src.chromium.org/viewvc/blink?view=rev&revision=149767

### bu...@chromium.org (2013-05-06)

------------------------------------------------------------------------
r149767 | cevans@chromium.org | 2013-05-06T18:43:23.836885Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/branches/chromium/1453/Source/WebCore/html/HTMLMediaElement.cpp?r1=149767&r2=149766&pathrev=149767

Merge Blink r149537 to M27

BUG=230117
TBR=acolwell@chromium.org

Review URL: https://codereview.chromium.org/14695006
------------------------------------------------------------------------

### sc...@gmail.com (2013-05-17)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-05-28)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-06-24)

[Empty comment from Monorail migration]

### js...@chromium.org (2013-11-18)

Bulk release of old security bug reports.


### cl...@chromium.org (2016-02-02)

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

### sh...@chromium.org (2018-07-29)

[Empty comment from Monorail migration]

### is...@google.com (2018-07-29)

This issue was migrated from crbug.com/chromium/230117?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/170146, crbug.com/chromium/234636]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40077383)*
