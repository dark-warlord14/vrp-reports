# Security: use-after-poison rtp_contributing_source_cache.cc:215 in blink::RtpContributingSourceCache::ClearCache

| Field | Value |
|-------|-------|
| **Issue ID** | [40062944](https://issues.chromium.org/issues/40062944) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebRTC>PeerConnection |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | m....@gmail.com |
| **Assignee** | hb...@chromium.org |
| **Created** | 2023-02-07 |
| **Bounty** | $2,000.00 |

## Description

**VERSION**  

WIN10 X64  

asan-win32-release\_x64-1100289

**REPRODUCTION CASE**  

The test case cannot be reproduced stably, so provide the root cause analysis first, and I will provide the test sample later if needed

Type of crash: [render]

#RCA

1. RTCPeerConnection is on-heap object and has a member rtp\_contributing\_source\_cache\_[1]
2. RtpContributingSourceCache is off-heap object
3. MaybeUpdateRtpSources invoke EnqueueMicrotask to run ClearCache with RtpContributingSourceCache's weakptr[2]
4. When RTCPeerConnection Dispose get call by gc, RtpContributingSourceCache's weakptr may not invaild cause UAP

```
class MODULES_EXPORT RTCPeerConnection final  
    : public EventTargetWithInlineData,  
      public RTCPeerConnectionHandlerClient,  
      public ActiveScriptWrappable<RTCPeerConnection>,  
      public ExecutionContextLifecycleObserver,  
      public MediaStreamObserver {  
  DEFINE_WRAPPERTYPEINFO();  
  USING_PRE_FINALIZER(RTCPeerConnection, Dispose);  
  
 public:  
  static RTCPeerConnection\* Create(ExecutionContext\*,  
...CUT...  
  // Always has a value if initialization was successful (the constructor did  
  // not throw an exception).  
  absl::optional<RtpContributingSourceCache> rtp_contributing_source_cache_;	<<[1]  

```
```
void RtpContributingSourceCache::MaybeUpdateRtpSources(  
    ScriptState\* script_state,  
    RTCRtpReceiver\* requesting_receiver) {  
  if (!pc_) {  
    return;  
  }  
...CUT...  
  
  ExecutionContext::From(script_state)  
      ->GetAgent()  
      ->event_loop()  
      ->EnqueueMicrotask(WTF::BindOnce(&RtpContributingSourceCache::ClearCache,  
                                       weak_factory_.GetWeakPtr()));			<<[2]  
}  

```

ASAN

=================================================================  

==25060==ERROR: AddressSanitizer: use-after-poison on address 0x7edd005bc2d8 at pc 0x7ffe696ccf4e bp 0x0092541fde00 sp 0x0092541fde48  

READ of size 8 at 0x7edd005bc2d8 thread T0  

==25060==WARNING: Failed to use and restart external symbolizer!  

#0 0x7ffe696ccf4d in blink::RtpContributingSourceCache::ClearCache C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\modules\peerconnection\rtp\_contributing\_source\_cache.cc:215  

#1 0x7ffe696cfc3b in base::internal::Invoker<base::internal::BindState<void (blink::RtpContributingSourceCache::\*)(),base::WeakPtr[blink::RtpContributingSourceCache](javascript:void(0);) >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind\_internal.h:970  

#2 0x7ffe521bec6d in blink::scheduler::EventLoop::RunPendingMicrotask C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\platform\scheduler\common\event\_loop.cc:151  

#3 0x7ffe4c608f79 in v8::internal::Runtime\_RunMicrotaskCallback C:\b\s\w\ir\cache\builder\src\v8\src\runtime\runtime-promise.cc:89  

#4 0x7ffdffe9a97b (<unknown module>)

Address 0x7edd005bc2d8 is a wild pointer inside of access range of size 0x000000000008.  

SUMMARY: AddressSanitizer: use-after-poison C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\modules\peerconnection\rtp\_contributing\_source\_cache.cc:215 in blink::RtpContributingSourceCache::ClearCache  

Shadow bytes around the buggy address:  

0x7edd005bc000: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x7edd005bc080: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7  

0x7edd005bc100: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7  

0x7edd005bc180: f7 f7 f7 f7 f7 f7 f7 f7 00 f7 f7 f7 f7 f7 f7 f7  

0x7edd005bc200: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7  

=>0x7edd005bc280: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7[f7]f7 f7 f7 f7  

0x7edd005bc300: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7  

0x7edd005bc380: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7  

0x7edd005bc400: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7  

0x7edd005bc480: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7  

0x7edd005bc500: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7  

Shadow byte legend (one shadow byte represents 8 application bytes):  

Addressable: 00  

Partially addressable: 01 02 03 04 05 06 07  

Heap left redzone: fa  

Freed heap region: fd  

Stack left redzone: f1  

Stack mid redzone: f2  

Stack right redzone: f3  

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

==25060==ADDITIONAL INFO

## Attachments

- [rca.diff](attachments/rca.diff) (text/plain, 3.0 KB)
- [rca_log.txt](attachments/rca_log.txt) (text/plain, 3.7 KB)
- [fix.diff](attachments/fix.diff) (text/plain, 2.0 KB)

## Timeline

### [Deleted User] (2023-02-07)

[Empty comment from Monorail migration]

### m....@gmail.com (2023-02-07)

I added some debugging code to locate the problem. Through the log, you can see that RTCPeerConnection::Dispose is called first and then RtpContributingSourceCache::ClearCache is called, resulting in UAP
```
[9380:18188:0207/154727.016:ERROR:rtc_peer_connection.cc(679)] [11000]RTCPeerConnection::Dispose -> this 00007E9900755568 tname-> Chrome_InProcRendererThread
Backtrace:
        base::debug::CollectStackTrace [0x00007FFAE7D00742+18] (D:\chromium\src\base\debug\stack_trace_win.cc:329)
        base::debug::StackTrace::StackTrace [0x00007FFAE799A9DA+26] (D:\chromium\src\base\debug\stack_trace.cc:218)
        blink::RTCPeerConnection::Dispose [0x00007FFA82E62212+636] (D:\chromium\src\third_party\blink\renderer\modules\peerconnection\rtc_peer_connection.cc:684)
        blink::RTCPeerConnection::InvokePreFinalizer [0x00007FFA82E61919+43] (D:\chromium\src\third_party\blink\renderer\modules\peerconnection\rtc_peer_connection.h:101)
        cppgc::internal::PreFinalizerHandler::InvokePreFinalizers [0x00007FFA96CDD167+2263] (D:\chromium\src\v8\src\heap\cppgc\prefinalizer-handler.cc:69)
        cppgc::internal::HeapBase::ExecutePreFinalizers [0x00007FFA96CA4081+241] (D:\chromium\src\v8\src\heap\cppgc\heap-base.cc:208)
        v8::internal::CppHeap::TraceEpilogue [0x00007FFA94CD4DD4+964] (D:\chromium\src\v8\src\heap\cppgc-js\cpp-heap.cc:849)
        v8::internal::Heap::PerformGarbageCollection [0x00007FFA94DD435C+7964] (D:\chromium\src\v8\src\heap\heap.cc:2309)
        v8::internal::Heap::CollectGarbage [0x00007FFA94DCB518+3560] (D:\chromium\src\v8\src\heap\heap.cc:1741)
        v8::internal::Heap::HandleGCRequest [0x00007FFA94DC8B39+585] (D:\chromium\src\v8\src\heap\heap.cc:1405)
        v8::internal::StackGuard::HandleInterrupts [0x00007FFA94C3D6F8+1992] (D:\chromium\src\v8\src\execution\stack-guard.cc:293)
        v8::internal::Runtime_StackGuard [0x00007FFA95EFFCA8+1000] (D:\chromium\src\v8\src\runtime\runtime-internal.cc:324)

[9380:18188:0207/154732.024:ERROR:rtp_contributing_source_cache.cc(217)] [11000]RtpContributingSourceCache::ClearCache1 -> this 00007E9900755658 tname-> Chrome_InProcRendererThread
Backtrace:
        base::debug::CollectStackTrace [0x00007FFAE7D00742+18] (D:\chromium\src\base\debug\stack_trace_win.cc:329)
        base::debug::StackTrace::StackTrace [0x00007FFAE799A9DA+26] (D:\chromium\src\base\debug\stack_trace.cc:218)
        blink::RtpContributingSourceCache::ClearCache [0x00007FFA82F56F8F+699] (D:\chromium\src\third_party\blink\renderer\modules\peerconnection\rtp_contributing_source_cache.cc:222)
        blink::scheduler::EventLoop::RunPendingMicrotask [0x00007FFA881817E6+688] (D:\chromium\src\third_party\blink\renderer\platform\scheduler\common\event_loop.cc:151)
        v8::internal::Runtime_RunMicrotaskCallback [0x00007FFA95FAB2E8+696] (D:\chromium\src\v8\src\runtime\runtime-promise.cc:89)
        (No symbol) [0x00007FFA1FE9A97C]
        
=================================================================
==9380==ERROR: AddressSanitizer: use-after-poison on address 0x7e9900755658 at pc 0x7ffa82f573bf bp 0x008adbdfacc0 sp 0x008adbdfad08
READ of size 8 at 0x7e9900755658 thread T43
==9380==*** WARNING: Failed to initialize DbgHelp!              ***
==9380==*** Most likely this means that the app is already      ***
==9380==*** using DbgHelp, possibly with incompatible flags.    ***
==9380==*** Due to technical reasons, symbolization might crash ***
==9380==*** or produce wrong results.                           ***
    #0 0x7ffa82f573be in blink::RtpContributingSourceCache::ClearCache D:\chromium\src\third_party\blink\renderer\modules\peerconnection\rtp_contributing_source_cache.cc:224
    #1 0x7ffa881817e5 in blink::scheduler::EventLoop::RunPendingMicrotask D:\chromium\src\third_party\blink\renderer\platform\scheduler\common\event_loop.cc:151
    #2 0x7ffa95fab2e7 in v8::internal::Runtime_RunMicrotaskCallback D:\chromium\src\v8\src\runtime\runtime-promise.cc:89
    #3 0x7ffa1fe9a97b  (<unknown module>)

```

### m....@gmail.com (2023-02-07)

BISECT:

Introduce CL
https://chromium-review.googlesource.com/c/chromium/src/+/3571922

Affect
Canary 102 102.0.4989.0
Dev 102 102.0.4997.0
Beta 102 102.0.5005.27
Stable 102 102.0.5005.61

### m....@gmail.com (2023-02-07)

my fix patch

Force clean up before destruction of RTCPeerConnection
```
diff --git a/third_party/blink/renderer/modules/peerconnection/rtc_peer_connection.cc b/third_party/blink/renderer/modules/peerconnection/rtc_peer_connection.cc
index cecf75544298..f71efec322f8 100644
--- a/third_party/blink/renderer/modules/peerconnection/rtc_peer_connection.cc
+++ b/third_party/blink/renderer/modules/peerconnection/rtc_peer_connection.cc
@@ -672,6 +672,8 @@ void RTCPeerConnection::Dispose() {
   if (peer_handler_) {
     peer_handler_.reset();
   }
+
+  GetRtpContributingSourceCache().Shutdown();
 }
 
 ScriptPromise RTCPeerConnection::createOffer(ScriptState* script_state,
diff --git a/third_party/blink/renderer/modules/peerconnection/rtp_contributing_source_cache.cc b/third_party/blink/renderer/modules/peerconnection/rtp_contributing_source_cache.cc
index 1707280e448b..3cf5160afeae 100644
--- a/third_party/blink/renderer/modules/peerconnection/rtp_contributing_source_cache.cc
+++ b/third_party/blink/renderer/modules/peerconnection/rtp_contributing_source_cache.cc
@@ -133,6 +133,10 @@ RtpContributingSourceCache::getContributingSources(
                                                     GetRtpSources(receiver));
 }
 
+void RtpContributingSourceCache::Shutdown(){
+  weak_factory_.InvalidateWeakPtrs();
+}
+
 void RtpContributingSourceCache::MaybeUpdateRtpSources(
     ScriptState* script_state,
     RTCRtpReceiver* requesting_receiver) {
diff --git a/third_party/blink/renderer/modules/peerconnection/rtp_contributing_source_cache.h b/third_party/blink/renderer/modules/peerconnection/rtp_contributing_source_cache.h
index 0d0ef9d1c593..dd9ef790555e 100644
--- a/third_party/blink/renderer/modules/peerconnection/rtp_contributing_source_cache.h
+++ b/third_party/blink/renderer/modules/peerconnection/rtp_contributing_source_cache.h
@@ -52,6 +52,7 @@ class RtpContributingSourceCache {
       ExceptionState& exception_state,
       RTCRtpReceiver* receiver);
 
+    void Shutdown();
  private:
   // Ensures the cache for `requesting_receiver` is up-to-date. Based on a
   // heuristic, this method may update the cache for all other receivers while
```

### ma...@google.com (2023-02-08)

Thanks for the report. Can you actually trigger this UAP (even if unreliably), in an unmodified build?

hbos@, are you a good person to own this issue?

(Not setting FoundIn-* for now, until we determine potential reachability/exploitability.)

[Monorail components: Blink>WebRTC]

### m....@gmail.com (2023-02-09)

Can be triggered in the unmodified build

### [Deleted User] (2023-02-09)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### hb...@chromium.org (2023-02-10)

Thank you for the report and proposed fix! I'll take a look shortly (today or monday)

### hb...@chromium.org (2023-02-10)

[Empty comment from Monorail migration]

[Monorail components: -Blink>WebRTC Blink>WebRTC>PeerConnection]

### ma...@google.com (2023-02-14)

[Empty comment from Monorail migration]

### hb...@chromium.org (2023-02-14)

[Empty comment from Monorail migration]

### ma...@google.com (2023-02-14)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-14)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-02-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/4d450ecd6ec7776c7505dcf7d2f04157ff3ba0eb

commit 4d450ecd6ec7776c7505dcf7d2f04157ff3ba0eb
Author: Henrik Boström <hbos@chromium.org>
Date: Wed Feb 15 15:21:56 2023

Shutdown RtpContributingSourceCache in Dispose().

The cache is an off-heap object, but it is owned by an on-heap object
(RTCPeerConnection). Dispoing the owning object poisons memory owned by
it, but the cache may have in-flight tasks (cache doing ClearCache in a
delayed microtask). This CL adds a Shutdown() method to ensure the
cache isn't doing anything in the next microtask after disposal.

No reliable way to repro this has been found but the change should be
safe so hoping we can land without tests.

Bug: 1413628
Change-Id: I479aace9859f4c10cd75d4aa5a34808b4726299d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4247023
Reviewed-by: Evan Shrubsole <eshr@google.com>
Commit-Queue: Henrik Boström <hbos@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1105653}

[modify] https://crrev.com/4d450ecd6ec7776c7505dcf7d2f04157ff3ba0eb/third_party/blink/renderer/modules/peerconnection/rtp_contributing_source_cache.h
[modify] https://crrev.com/4d450ecd6ec7776c7505dcf7d2f04157ff3ba0eb/third_party/blink/renderer/modules/peerconnection/rtp_contributing_source_cache.cc
[modify] https://crrev.com/4d450ecd6ec7776c7505dcf7d2f04157ff3ba0eb/third_party/blink/renderer/modules/peerconnection/rtc_peer_connection.cc


### hb...@chromium.org (2023-02-15)

Fixed in M112. Security folks might want to have an opinion about whether or not this warrants backmerging.

### [Deleted User] (2023-02-15)

[Empty comment from Monorail migration]

### ma...@google.com (2023-02-15)

Thank you for addressing this! With the bug fixed, sheriffbot should take care of the merges automatically for you, based on the Severity and FoundIn labels. Could you double check that the OS labels on this bug are accurate?


### [Deleted User] (2023-02-15)

[Empty comment from Monorail migration]

### hb...@chromium.org (2023-02-16)

Ack. The OS labels are accurate.

### am...@chromium.org (2023-02-23)

The M-112 label seems to have confused the bot and impacted it's logic to request merges. I've adjusted accordingly but going ahead and reviewing this for merge now given the time since this fix was landed and impending RC cuts. 

M111 merge approved, please merge this fix to branch 5563 before EOD Monday, 27 February so this fix can be included in the M111 Stable RC for release the following week. 
M110 merge approved, please merge this fix to branch 5481 so this fix can be included in the first M110/Extended release. 
Thank you! 

### gi...@appspot.gserviceaccount.com (2023-02-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b80ec9ba7207fa6b85911f5604f1957e91275919

commit b80ec9ba7207fa6b85911f5604f1957e91275919
Author: Henrik Boström <hbos@chromium.org>
Date: Fri Feb 24 08:44:54 2023

[Merge-111] Shutdown RtpContributingSourceCache in Dispose().

The cache is an off-heap object, but it is owned by an on-heap object
(RTCPeerConnection). Dispoing the owning object poisons memory owned by
it, but the cache may have in-flight tasks (cache doing ClearCache in a
delayed microtask). This CL adds a Shutdown() method to ensure the
cache isn't doing anything in the next microtask after disposal.

No reliable way to repro this has been found but the change should be
safe so hoping we can land without tests.

(cherry picked from commit 4d450ecd6ec7776c7505dcf7d2f04157ff3ba0eb)

Bug: 1413628
Change-Id: I479aace9859f4c10cd75d4aa5a34808b4726299d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4247023
Reviewed-by: Evan Shrubsole <eshr@google.com>
Commit-Queue: Henrik Boström <hbos@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1105653}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4290469
Cr-Commit-Position: refs/branch-heads/5563@{#775}
Cr-Branched-From: 3ac59a6729cdb287a7ee629a0004c907ec1b06dc-refs/heads/main@{#1097615}

[modify] https://crrev.com/b80ec9ba7207fa6b85911f5604f1957e91275919/third_party/blink/renderer/modules/peerconnection/rtp_contributing_source_cache.h
[modify] https://crrev.com/b80ec9ba7207fa6b85911f5604f1957e91275919/third_party/blink/renderer/modules/peerconnection/rtp_contributing_source_cache.cc
[modify] https://crrev.com/b80ec9ba7207fa6b85911f5604f1957e91275919/third_party/blink/renderer/modules/peerconnection/rtc_peer_connection.cc


### [Deleted User] (2023-02-24)

LTS Milestone M108

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2023-02-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/63bbeb73f6f0f53ba740532ce032cd7fea70cc86

commit 63bbeb73f6f0f53ba740532ce032cd7fea70cc86
Author: Henrik Boström <hbos@chromium.org>
Date: Fri Feb 24 08:50:29 2023

[Merge-110] Shutdown RtpContributingSourceCache in Dispose().

The cache is an off-heap object, but it is owned by an on-heap object
(RTCPeerConnection). Dispoing the owning object poisons memory owned by
it, but the cache may have in-flight tasks (cache doing ClearCache in a
delayed microtask). This CL adds a Shutdown() method to ensure the
cache isn't doing anything in the next microtask after disposal.

No reliable way to repro this has been found but the change should be
safe so hoping we can land without tests.

(cherry picked from commit 4d450ecd6ec7776c7505dcf7d2f04157ff3ba0eb)

Bug: 1413628
Change-Id: I479aace9859f4c10cd75d4aa5a34808b4726299d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4247023
Reviewed-by: Evan Shrubsole <eshr@google.com>
Commit-Queue: Henrik Boström <hbos@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1105653}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4290429
Cr-Commit-Position: refs/branch-heads/5481@{#1275}
Cr-Branched-From: 130f3e4d850f4bc7387cfb8d08aa993d288a67a9-refs/heads/main@{#1084008}

[modify] https://crrev.com/63bbeb73f6f0f53ba740532ce032cd7fea70cc86/third_party/blink/renderer/modules/peerconnection/rtp_contributing_source_cache.h
[modify] https://crrev.com/63bbeb73f6f0f53ba740532ce032cd7fea70cc86/third_party/blink/renderer/modules/peerconnection/rtp_contributing_source_cache.cc
[modify] https://crrev.com/63bbeb73f6f0f53ba740532ce032cd7fea70cc86/third_party/blink/renderer/modules/peerconnection/rtc_peer_connection.cc


### hb...@chromium.org (2023-02-24)

1. This bug was introduced in M102 and only detected now (backmerging to M111 and M110 respin). So its an old regression but if "found in" refers to M102 then yes.
2. No its an old feature. I don't know what the latest LTS Milestone is but I assume it is much later than M102.

### rz...@google.com (2023-02-27)

[Empty comment from Monorail migration]

### rz...@google.com (2023-02-27)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-27)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-02-27)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2023-02-28)

1: https://crrev.com/c/4291515 for 102 and https://crrev.com/c/4291513 for 108
2: Low, no conflicts for 108 and only conflicts with comments for 102
3. 110, 111
4. Yes

### gm...@google.com (2023-03-01)

[Empty comment from Monorail migration]

### am...@google.com (2023-03-02)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-03-02)

Congratulations! The VRP Panel has decided to award you $2,000 for this report of this highly mitigated (by race condition and shutdown) bug + $1,000 bisect bonus. Thank you for your efforts in discovering and reporting this issue to us! 

### am...@google.com (2023-03-03)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-03-06)

[Empty comment from Monorail migration]

### am...@google.com (2023-03-07)

[Empty comment from Monorail migration]

### pg...@google.com (2023-03-07)

[Empty comment from Monorail migration]

### m....@gmail.com (2023-03-09)

re https://crbug.com/chromium/1413628#c32 Looks like the patch I provided at https://crbug.com/chromium/1413628#c04 are used, should be able to get a patch bounty?

### am...@chromium.org (2023-03-10)

Thanks for calling our attention to that. We'll discuss at the next VRP Panel session. 

### gm...@google.com (2023-03-13)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-03-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/9aa4c45f21b1fbb6666090fabf3d03297ad982e3

commit 9aa4c45f21b1fbb6666090fabf3d03297ad982e3
Author: Henrik Boström <hbos@chromium.org>
Date: Tue Mar 14 13:07:19 2023

[M108-LTS] Shutdown RtpContributingSourceCache in Dispose().

The cache is an off-heap object, but it is owned by an on-heap object
(RTCPeerConnection). Dispoing the owning object poisons memory owned by
it, but the cache may have in-flight tasks (cache doing ClearCache in a
delayed microtask). This CL adds a Shutdown() method to ensure the
cache isn't doing anything in the next microtask after disposal.

No reliable way to repro this has been found but the change should be
safe so hoping we can land without tests.

(cherry picked from commit 4d450ecd6ec7776c7505dcf7d2f04157ff3ba0eb)

Bug: 1413628
Change-Id: I479aace9859f4c10cd75d4aa5a34808b4726299d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4247023
Commit-Queue: Henrik Boström <hbos@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1105653}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4291513
Reviewed-by: Achuith Bhandarkar <achuith@chromium.org>
Owners-Override: Achuith Bhandarkar <achuith@chromium.org>
Reviewed-by: Henrik Boström <hbos@chromium.org>
Commit-Queue: Zakhar Voit <voit@google.com>
Cr-Commit-Position: refs/branch-heads/5359@{#1404}
Cr-Branched-From: 27d3765d341b09369006d030f83f582a29eb57ae-refs/heads/main@{#1058933}

[modify] https://crrev.com/9aa4c45f21b1fbb6666090fabf3d03297ad982e3/third_party/blink/renderer/modules/peerconnection/rtp_contributing_source_cache.h
[modify] https://crrev.com/9aa4c45f21b1fbb6666090fabf3d03297ad982e3/third_party/blink/renderer/modules/peerconnection/rtp_contributing_source_cache.cc
[modify] https://crrev.com/9aa4c45f21b1fbb6666090fabf3d03297ad982e3/third_party/blink/renderer/modules/peerconnection/rtc_peer_connection.cc


### vo...@google.com (2023-03-14)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-03-17)

We have updated the reward amount to include a patch bonus. Thank you for your efforts on this! 

### am...@google.com (2023-03-17)

[Empty comment from Monorail migration]

### gm...@google.com (2023-04-28)

Rejecting Merge for LTS-102 as there is no plans for another respin.

### [Deleted User] (2023-05-26)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-05-26)

This issue was migrated from crbug.com/chromium/1413628?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062944)*
