# Use-After-Free in ReadbackBufferShadowTracker via getBufferSubData with Non-Zero Offset

| Field | Value |
|-------|-------|
| **Issue ID** | [492228019](https://issues.chromium.org/issues/492228019) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebGL |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | je...@gmail.com |
| **Assignee** | gm...@chromium.org |
| **Created** | 2026-03-13 |
| **Bounty** | $11,000.00 |

## Description

# Use-After-Free in ReadbackBufferShadowTracker via getBufferSubData with Non-Zero Offset

## Summary

A use-after-free exists in the GPU command buffer client's `ReadbackBufferShadowTracker` on all desktop platforms. When a WebGL2 application calls `getBufferSubData` with a non-zero `srcByteOffset` on a `STREAM_READ` buffer, the internal `UnmapBuffer` path frees the wrong block in the `FencedAllocator`, releasing an adjacent buffer's shadow memory while it is still live. An attacker can reclaim the freed region to read or corrupt another buffer's data. By further manipulating the mapped memory lifecycle so the entire backing chunk is destroyed, the dangling shadow pointer dereferences unmapped memory, crashing the renderer. This is exploitable from any WebGL2-capable page with no special permissions.

## Bisect

Introducing Commit: `2ca03f3fc6fde691b46cba5744b31dff33c7725c`

- Date: 2018-06-12
- Author: Kai Ninomiya ([kainino@chromium.org](mailto:kainino@chromium.org))
- Review: <https://chromium-review.googlesource.com/c/chromium/src/+/1043024>

## Root Cause

The `ReadbackBufferShadowTracker` maintains shadow copies of `STREAM_READ`, `DYNAMIC_READ`, and `STATIC_READ` buffers in shared memory, enabling `getBufferSubData` to return data without a GPU round-trip. When `MapBufferRange` is called on such a buffer, it calls `MapReadbackShm(offset, size)`, which returns a subspan of the full allocation:

```
// readback_buffer_shadow_tracker.cc:47-66
base::span<uint8_t> ReadbackBufferShadowTracker::Buffer::MapReadbackShm(
    uint32_t offset,
    uint32_t map_size) {
  // ...
  is_mapped_ = true;
  return readback_buffer_.subspan(offset, map_size);
}

```

This subspan is stored in `mapped_buffer_range_map_` keyed by buffer ID. When `offset > 0`, the span's `data()` pointer points into the middle of the allocation, not at its base.

The corresponding `UnmapBuffer` correctly frees the allocation at its base address through `UnmapReadbackShm`, which internally calls `Free()`:

```
// readback_buffer_shadow_tracker.cc:39-45, 68-74
void ReadbackBufferShadowTracker::Buffer::Free() {
  if (!readback_buffer_.empty()) {
    mapped_memory_->FreePendingToken(readback_buffer_.data(),
                                     helper_->InsertToken());
  }
  readback_buffer_ = {};
}

bool ReadbackBufferShadowTracker::Buffer::UnmapReadbackShm() {
  Free();
  bool was_mapped = is_mapped_;
  is_mapped_ = false;
  return was_mapped;
}

```

However, after `UnmapReadbackShm` returns, `UnmapBuffer` unconditionally calls `RemoveMappedBufferRangeById`, which frees the subspan pointer a second time:

```
// gles2_implementation.cc:5608-5617
bool was_mapped_by_readback_tracker = false;
if (auto* buffer_object =
        readback_buffer_shadow_tracker_->GetBuffer(buffer)) {
  was_mapped_by_readback_tracker = buffer_object->UnmapReadbackShm();
}
if (!was_mapped_by_readback_tracker) {
  helper_->UnmapBuffer(target);
  InvalidateReadbackBufferShadowDataCHROMIUM(GetBoundBufferHelper(target));
}
RemoveMappedBufferRangeById(buffer);  // unconditional second free

```

`RemoveMappedBufferRangeById` passes the subspan's `data()` pointer to `FreePendingToken`:

```
// gles2_implementation.cc:5442-5452
void GLES2Implementation::RemoveMappedBufferRangeById(GLuint buffer) {
  if (buffer > 0) {
    auto iter = mapped_buffer_range_map_.find(buffer);
    if (iter != mapped_buffer_range_map_.end() &&
        !iter->second.shm_memory.empty()) {
      mapped_memory_->FreePendingToken(iter->second.shm_memory.data(),
                                       helper_->InsertToken());
      mapped_buffer_range_map_.erase(iter);
    }
  }
}

```

When `srcByteOffset > 0`, the subspan pointer does not correspond to the base of any allocation in the `FencedAllocator`. The allocator's `GetBlockByOffset` uses `lower_bound` binary search to resolve the offset to a block index, and the only guard against a mismatch is `DCHECK_EQ(block.offset, offset)`, which is stripped in release builds:

```
// fenced_allocator.cc:101-110
void FencedAllocator::FreePendingToken(FencedAllocator::Offset offset,
                                       int32_t token) {
  BlockIndex index = GetBlockByOffset(offset);
  Block &block = blocks_[index];
  DCHECK_EQ(block.offset, offset);  // stripped in release
  if (block.state == IN_USE)
    bytes_in_use_ -= block.size;
  block.state = FREE_PENDING_TOKEN;
  block.token = token;
}

```

The `lower_bound` search resolves to the next block after the intended allocation, since the subspan offset falls between two block boundaries. This erroneously marks the adjacent block as `FREE_PENDING_TOKEN`, freeing memory that belongs to a different, still-live buffer.

Once the adjacent block is freed, an attacker can allocate new buffers that reuse the same memory region, creating an overlapping allocation where two logical buffers share the same physical backing. Reading from the original (dangling) buffer returns the new buffer's contents, demonstrating information disclosure. Writing to one buffer corrupts the other.

## Reproduce

### Notes on the PoC Structure and Flags

The vulnerability itself is triggerable from any WebGL2 page without any special flags or user interaction; in a normal release build, the same bug produces exploitable heap corruption silently. All flags in the launch command, including `--disable-popup-blocking`, exist only for reproducing the ASAN crash log. Specifically, `--disable-popup-blocking` is required because Phase 2 of the PoC uses `window.open` to force a tab switch, triggering the page visibility transition that unmaps the shared memory chunk and produces the ASAN-detectable access-violation.

The PoC has two phases because the `FencedAllocator` is a sub-allocator within a single shared memory mapping, and its internal block-level mis-free is invisible to ASAN. Phase 1 proves the vulnerability is real by demonstrating overlapping allocation: after the mis-free, a newly allocated buffer E reuses the erroneously freed block, and reading through the original buffer C returns E's data (0xEE). The overlapping allocation from Phase 1 is already sufficient for exploitation, as an attacker can spray controlled data into the reclaimed region to corrupt adjacent buffer contents or hijack pointer-containing structures. Phase 2 exists purely to provide a minimal, deterministic ASAN crash as proof: it drains all other allocations from the chunk so `bytes_in_use` reaches zero, then triggers a page visibility transition that causes `MappedMemoryManager` to destroy the entire chunk via `UnmapViewOfFile`. The dangling `readback_buffer_` span now points into unmapped virtual address space, and `getBufferSubData` crashes in `memcpy`.

### Steps

Tested on commit `4e910e2277470c4576177b37937569fa4151abdc`, Windows 11. No source patches are required.

Build `out/asan-release` with `args.gn`:

```
is_debug = false
dcheck_always_on = false
is_asan = true
is_component_build = false

```

Build and launch:

```
autoninja -C out/asan-release chrome
python3 -m http.server 8080 -d issue_blink_mod_010
out\asan-release\chrome.exe --disable-gpu-sandbox --no-sandbox --disable-popup-blocking --enable-logging=stderr http://localhost:8080/poc.html

```

ASAN log:

```
==13076==ERROR: AddressSanitizer: access-violation on unknown address 0x132df6bb0c80 (pc 0x7ff92936dc7d bp 0x00ae447fcb30 sp 0x00ae447fcaa8 T0)
==13076==The signal is caused by a READ memory access.
    #0 0x7ff92936dc7c in memcpy+0x17c (C:\WINDOWS\System32\ucrtbase.dll+0x1800edc7c)
    #1 0x7ff8d343b532 in _asan_memcpy+0x422 (D:\chromium\src\out\asan-release\clang_rt.asan_dynamic-x86_64.dll+0x18004b532)
    #2 0x7ff8556ac923 in blink::WebGL2RenderingContextBase::getBufferSubData D:\chromium\src\third_party\blink\renderer\modules\webgl\webgl2_rendering_context_base.cc:456
    #3 0x7ff8556fe4cb in blink::`anonymous namespace'::v8_webgl2_rendering_context::GetBufferSubDataOperationCallback D:\chromium\src\out\asan-release\gen\third_party\blink\renderer\bindings\modules\v8\v8_webgl2_rendering_context.cc:4154
    #4 0x7ff85a7647e4 in Builtins_CallApiCallbackGeneric+0xa4 (D:\chromium\src\out\asan-release\chrome.dll+0x1ada747e4)
    #5 0x7ff85a76293b in Builtins_InterpreterEntryTrampoline+0x13b (D:\chromium\src\out\asan-release\chrome.dll+0x1ada7293b)
    #6 0x7ff85a75f6db in Builtins_JSEntryTrampoline+0x5b (D:\chromium\src\out\asan-release\chrome.dll+0x1ada6f6db)
    #7 0x7ff85a75f23e in Builtins_JSEntry+0xfe (D:\chromium\src\out\asan-release\chrome.dll+0x1ada6f23e)
    #8 0x7ff8322b2222 in v8::internal::`anonymous namespace'::Invoke D:\chromium\src\v8\src\execution\execution.cc:474
    #9 0x7ff8322b0493 in v8::internal::Execution::Call D:\chromium\src\v8\src\execution\execution.cc:564
    #10 0x7ff831db389c in v8::Function::Call D:\chromium\src\v8\src\api\api.cc:5584
    #11 0x7ff848d77fdd in blink::V8ScriptRunner::CallFunction D:\chromium\src\third_party\blink\renderer\bindings\core\v8\v8_script_runner.cc:851
    #12 0x7ff853c92406 in blink::bindings::CallbackInvokeHelper<blink::CallbackInterfaceBase,0,0>::Call D:\chromium\src\third_party\blink\renderer\bindings\core\v8\callback_invoke_helper.cc:148
    #13 0x7ff8538248df in blink::V8EventListener::InvokeWithoutRunnabilityCheck D:\chromium\src\out\asan-release\gen\third_party\blink\renderer\bindings\core\v8\v8_event_listener.cc:119
    #14 0x7ff84e982abb in blink::JSEventListener::InvokeInternal D:\chromium\src\third_party\blink\renderer\bindings\core\v8\js_event_listener.cc:58
    #15 0x7ff84e954feb in blink::JSBasedEventListener::Invoke D:\chromium\src\third_party\blink\renderer\bindings\core\v8\js_based_event_listener.cc:193
    #16 0x7ff848ee8c56 in blink::EventTarget::FireEventListeners D:\chromium\src\third_party\blink\renderer\core\dom\events\event_target.cc:1081
    #17 0x7ff848ee6a02 in blink::EventTarget::FireEventListeners D:\chromium\src\third_party\blink\renderer\core\dom\events\event_target.cc:982
    #18 0x7ff84e80209f in blink::EventDispatcher::DispatchEventAtBubbling D:\chromium\src\third_party\blink\renderer\core\dom\events\event_dispatcher.cc:368
    #19 0x7ff84e800a0e in blink::EventDispatcher::Dispatch D:\chromium\src\third_party\blink\renderer\core\dom\events\event_dispatcher.cc:278
    #20 0x7ff84e7fef51 in blink::EventDispatcher::DispatchEvent D:\chromium\src\third_party\blink\renderer\core\dom\events\event_dispatcher.cc:79
    #21 0x7ff848a48f5a in blink::Document::DidChangeVisibilityState D:\chromium\src\third_party\blink\renderer\core\dom\document.cc:2275
    #22 0x7ff8489bab61 in blink::LocalFrame::DidChangeVisibilityState D:\chromium\src\third_party\blink\renderer\core\frame\local_frame.cc:1175
    #23 0x7ff848c68d56 in blink::Page::SetVisibilityState D:\chromium\src\third_party\blink\renderer\core\page\page.cc:854
    #24 0x7ff8488e5e41 in blink::WebViewImpl::SetVisibilityState D:\chromium\src\third_party\blink\renderer\core\exported\web_view_impl.cc:4189
    #25 0x7ff848902757 in blink::WebViewImpl::SetPageLifecycleStateInternal D:\chromium\src\third_party\blink\renderer\core\exported\web_view_impl.cc:2551
    #26 0x7ff848903fd4 in blink::WebViewImpl::SetPageLifecycleState D:\chromium\src\third_party\blink\renderer\core\exported\web_view_impl.cc:2473
    #27 0x7ff83a218c88 in blink::mojom::blink::PageBroadcastStubDispatch::AcceptWithResponder D:\chromium\src\out\asan-release\gen\third_party\blink\public\mojom\page\page.mojom-blink.cc:1950
    #28 0x7ff84891d390 in blink::mojom::blink::PageBroadcastStub<mojo::RawPtrImplRefTraits<blink::mojom::blink::PageBroadcast> >::AcceptWithResponder D:\chromium\src\out\asan-release\gen\third_party\blink\public\mojom\page\page.mojom-blink.h:248
    #29 0x7ff8405deefd in mojo::InterfaceEndpointClient::HandleValidatedMessage D:\chromium\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:1036
    #30 0x7ff845e8488d in mojo::MessageDispatcher::Accept D:\chromium\src\mojo\public\cpp\bindings\lib\message_dispatcher.cc:44
    #31 0x7ff8405e563e in mojo::InterfaceEndpointClient::HandleIncomingMessage D:\chromium\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:747
    #32 0x7ff846ee4166 in IPC::ChannelAssociatedGroupController::AcceptOnEndpointThread D:\chromium\src\ipc\ipc_mojo_bootstrap.cc:1199
    #33 0x7ff846ee66a1 in base::internal::Invoker<...>::RunOnce D:\chromium\src\base\functional\bind_internal.h:982
    #34 0x7ff8407c3d48 in base::TaskAnnotator::RunTaskImpl D:\chromium\src\base\task\common\task_annotator.cc:229
    #35 0x7ff845f2c531 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl D:\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:475
    #36 0x7ff845f2b393 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork D:\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:346
    #37 0x7ff845f73c37 in base::MessagePumpDefault::Run D:\chromium\src\base\message_loop\message_pump_default.cc:42
    #38 0x7ff845f2e27f in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run D:\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:650
    #39 0x7ff840836dbc in base::RunLoop::Run D:\chromium\src\base\run_loop.cc:135
    #40 0x7ff843e2043f in content::RendererMain D:\chromium\src\content\renderer\renderer_main.cc:332
    #41 0x7ff83d18594f in content::RunOtherNamedProcessTypeMain D:\chromium\src\content\app\content_main_runner_impl.cc:762
    #42 0x7ff83d1880bb in content::ContentMainRunnerImpl::Run D:\chromium\src\content\app\content_main_runner_impl.cc:1152
    #43 0x7ff83d17beaf in content::RunContentProcess D:\chromium\src\content\app\content_main.cc:358
    #44 0x7ff83d17c652 in content::ContentMain D:\chromium\src\content\app\content_main.cc:371
    #45 0x7ff82ccf2b06 in ChromeMain D:\chromium\src\chrome\app\chrome_main.cc:191
    #46 0x7ff710b04807 in MainDllLoader::Launch D:\chromium\src\chrome\app\main_dll_loader_win.cc:204
    #47 0x7ff710b02074 in main D:\chromium\src\chrome\app\chrome_exe_main_win.cc:351

AddressSanitizer can not provide additional info.
SUMMARY: AddressSanitizer: access-violation (C:\WINDOWS\System32\ucrtbase.dll+0x1800edc7c) in memcpy+0x17c
==13076==ABORTING

```
## Credit

Please use c6eed09fc8b174b0f3eebedcceb1e792 as the credit for this vulnerability. Thank you.

## Attachments

- [poc.html](attachments/poc.html) (text/html, 7.1 KB)
- [asan.log](attachments/asan.log) (text/plain, 6.9 KB)

## Timeline

### th...@chromium.org (2026-03-13)

[security shepherd] I don't a device available to reproduce this, but this seems likely so I will triage this speculatively. Found In to current extended stable 146 based on bisect, high severity since this is the renderer process.

bajones@: Could you PTAL?

### th...@chromium.org (2026-03-13)

Correction: I can reproduce a renderer crash on Mac M146, though it manifests as "Received signal 11 SEGV\_ACCERR".

### ch...@google.com (2026-03-14)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-03-14)

Setting Priority to P1 to match Severity s1. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### dx...@google.com (2026-03-17)

Project: chromium/src  

Branch:  main  

Author:  Gregg Tavares [gman@chromium.org](mailto:gman@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7667030>

Fix Use-After-Free with GL MapBufferRange with shadow buf

---


Expand for full commit details
```
     
    When MapBufferRange is called on a readback-usage buffer, 
    it returns a subspan of the shadow buffer allocation. 
    This subspan pointer (base + offset) was being passed to 
    FreePendingToken during UnmapBuffer, causing the FencedAllocator 
    to misidentify and erroneously free the next adjacent memory block. 
     
    This change ensures that shadow-mapped buffers are correctly 
    unmapped via UnmapReadbackShm, which uses the correct base pointer. 
    Added null checks for shadow buffer lookups to handle cases where a 
    buffer mapping is tracked but the shadow buffer has been destroyed. 
     
    Added regression tests: 
    - UnmapBufferWithOffsetFreesCorrectBlock: Verifies that unmapping a 
      shadow buffer with an offset does not free adjacent blocks. 
      This was crashing before the fix. 
    - ReadbackShadowMixedCleanup: Verifies that multiple shadow mappings 
      with various offsets are correctly cleaned up. 
     
    Added coverage tests: 
    - ClearMappedBufferRangeMapShadow: Verifies ClearMappedBufferRangeMap 
      correctly unmaps shadow readback buffers. 
    - ClearMappedBufferMap: Verifies ClearMappedBufferMap correctly frees 
      transfer buffers mapped via MapBufferSubDataCHROMIUM. 
    - AllocateShadowCopiesForReadbackNullBuffer: Verifies that 
      AllocateShadowCopiesForReadback safely skips buffers that were 
      deleted before being fenced, preventing a null pointer dereference. 
    - AllocateShadowCopiesForReadbackAllocFail: Verifies that 
      AllocateShadowCopiesForReadback handles memory allocation failures 
      gracefully by skipping the shadow allocation instead of issuing a 
      command with an invalid shared memory ID. 
    - AllocateShadowCopiesForReadbackAlreadyAllocated: Verifies that 
      AllocateShadowCopiesForReadback issues a performance warning if a 
      READ-usage buffer is written to multiple times before being fenced. 
    - ReadbackBufferShadowTrackerTest.AllocFails: Verifies that the shadow 
      tracker correctly handles internal allocation failures from 
      MappedMemoryManager. 
     
    Bug: 492228019 
    Change-Id: I8e12ffd1ed4356609e7aeeef1552e81e250ae7bd 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7667030 
    Reviewed-by: Kenneth Russell <kbr@chromium.org> 
    Commit-Queue: Gregg Tavares <gman@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1600244}

```

---

Files:

- M `gpu/BUILD.gn`
- M `gpu/command_buffer/client/gles2_implementation.cc`
- M `gpu/command_buffer/client/gles2_implementation_unittest.cc`
- M `gpu/command_buffer/client/implementation_base.h`
- M `gpu/command_buffer/client/query_tracker.h`
- M `gpu/command_buffer/client/readback_buffer_shadow_tracker.cc`
- M `gpu/command_buffer/client/readback_buffer_shadow_tracker.h`
- A `gpu/command_buffer/client/readback_buffer_shadow_tracker_unittest.cc`

---

Hash: [7500f1d78b8c1e52dff6a3966e65c3eafa104d64](https://chromiumdash.appspot.com/commit/7500f1d78b8c1e52dff6a3966e65c3eafa104d64)  

Date: Tue Mar 17 01:04:27 2026


---

### ch...@google.com (2026-03-17)

Security Merge Request Consideration: Requesting merge to stable (M146) because latest trunk commit (1600244) appears to be after stable branch point (1582197).
Security Merge Request Consideration: Requesting merge to beta (M147) because latest trunk commit (1600244) appears to be after beta branch point (1596535).
Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### ch...@google.com (2026-03-18)

Merge review required: M147 is already shipping to beta.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: alonbajayo (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), harrysouders (Mobile US), eakpobaro (Mobile EMEA)

### ch...@google.com (2026-03-18)

Merge review required: M146 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: lmenezes (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), govind (Mobile US), eakpobaro (Mobile EMEA)

### dr...@chromium.org (2026-03-18)

No crashes in Canary. Approved to merge to M146 and M147.

### go...@google.com (2026-03-19)

Please merge your change to M147 by 2:00 PM PT today so we can take it in for tomorrow's M147 beta release. Thank you.

### ch...@google.com (2026-03-24)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2026-03-24)

Merge review required: M147 has already been cut for stable release.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: alonbajayo (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), harrysouders (Mobile US), eakpobaro (Mobile EMEA)

### ch...@google.com (2026-03-24)

Merge review required: M146 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: lmenezes (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), govind (Mobile US), eakpobaro (Mobile EMEA)

### dr...@chromium.org (2026-03-24)

gman@ - since this is a vulnerability, it won't get any child bugs (we're working on standardizing the process). Feel free to just create the merges and tag this bug.

### dx...@google.com (2026-03-25)

Project: chromium/src  

Branch:  refs/branch-heads/7727  

Author:  Gregg Tavares [gman@chromium.org](mailto:gman@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7701047>

[M147] Fix Use-After-Free with GL MapBufferRange with shadow buf

---


Expand for full commit details
```
     
    When MapBufferRange is called on a readback-usage buffer, 
    it returns a subspan of the shadow buffer allocation. 
    This subspan pointer (base + offset) was being passed to 
    FreePendingToken during UnmapBuffer, causing the FencedAllocator 
    to misidentify and erroneously free the next adjacent memory block. 
     
    This change ensures that shadow-mapped buffers are correctly 
    unmapped via UnmapReadbackShm, which uses the correct base pointer. 
    Added null checks for shadow buffer lookups to handle cases where a 
    buffer mapping is tracked but the shadow buffer has been destroyed. 
     
    Added regression tests: 
    - UnmapBufferWithOffsetFreesCorrectBlock: Verifies that unmapping a 
      shadow buffer with an offset does not free adjacent blocks. 
      This was crashing before the fix. 
    - ReadbackShadowMixedCleanup: Verifies that multiple shadow mappings 
      with various offsets are correctly cleaned up. 
     
    Added coverage tests: 
    - ClearMappedBufferRangeMapShadow: Verifies ClearMappedBufferRangeMap 
      correctly unmaps shadow readback buffers. 
    - ClearMappedBufferMap: Verifies ClearMappedBufferMap correctly frees 
      transfer buffers mapped via MapBufferSubDataCHROMIUM. 
    - AllocateShadowCopiesForReadbackNullBuffer: Verifies that 
      AllocateShadowCopiesForReadback safely skips buffers that were 
      deleted before being fenced, preventing a null pointer dereference. 
    - AllocateShadowCopiesForReadbackAllocFail: Verifies that 
      AllocateShadowCopiesForReadback handles memory allocation failures 
      gracefully by skipping the shadow allocation instead of issuing a 
      command with an invalid shared memory ID. 
    - AllocateShadowCopiesForReadbackAlreadyAllocated: Verifies that 
      AllocateShadowCopiesForReadback issues a performance warning if a 
      READ-usage buffer is written to multiple times before being fenced. 
    - ReadbackBufferShadowTrackerTest.AllocFails: Verifies that the shadow 
      tracker correctly handles internal allocation failures from 
      MappedMemoryManager. 
     
    (cherry picked from commit 7500f1d78b8c1e52dff6a3966e65c3eafa104d64) 
     
    Bug: 492228019 
    Change-Id: I8e12ffd1ed4356609e7aeeef1552e81e250ae7bd 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7667030 
    Reviewed-by: Kenneth Russell <kbr@chromium.org> 
    Commit-Queue: Gregg Tavares <gman@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1600244} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7701047 
    Auto-Submit: Gregg Tavares <gman@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7727@{#1499} 
    Cr-Branched-From: ce01102937348db7b88c8a4257ee4b3ac702eb1a-refs/heads/main@{#1596535}

```

---

Files:

- M `gpu/BUILD.gn`
- M `gpu/command_buffer/client/gles2_implementation.cc`
- M `gpu/command_buffer/client/gles2_implementation_unittest.cc`
- M `gpu/command_buffer/client/implementation_base.h`
- M `gpu/command_buffer/client/query_tracker.h`
- M `gpu/command_buffer/client/readback_buffer_shadow_tracker.cc`
- M `gpu/command_buffer/client/readback_buffer_shadow_tracker.h`
- A `gpu/command_buffer/client/readback_buffer_shadow_tracker_unittest.cc`

---

Hash: [1ac208a785ed1fbfdcf152db200eb4ee0761e4c5](https://chromiumdash.appspot.com/commit/1ac208a785ed1fbfdcf152db200eb4ee0761e4c5)  

Date: Wed Mar 25 19:30:37 2026


---

### dx...@google.com (2026-03-25)

Project: chromium/src  

Branch:  refs/branch-heads/7680  

Author:  Gregg Tavares [gman@chromium.org](mailto:gman@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7699638>

[M146] Fix Use-After-Free with GL MapBufferRange with shadow buf

---


Expand for full commit details
```
     
    When MapBufferRange is called on a readback-usage buffer, 
    it returns a subspan of the shadow buffer allocation. 
    This subspan pointer (base + offset) was being passed to 
    FreePendingToken during UnmapBuffer, causing the FencedAllocator 
    to misidentify and erroneously free the next adjacent memory block. 
     
    This change ensures that shadow-mapped buffers are correctly 
    unmapped via UnmapReadbackShm, which uses the correct base pointer. 
    Added null checks for shadow buffer lookups to handle cases where a 
    buffer mapping is tracked but the shadow buffer has been destroyed. 
     
    Added regression tests: 
    - UnmapBufferWithOffsetFreesCorrectBlock: Verifies that unmapping a 
      shadow buffer with an offset does not free adjacent blocks. 
      This was crashing before the fix. 
    - ReadbackShadowMixedCleanup: Verifies that multiple shadow mappings 
      with various offsets are correctly cleaned up. 
     
    Added coverage tests: 
    - ClearMappedBufferRangeMapShadow: Verifies ClearMappedBufferRangeMap 
      correctly unmaps shadow readback buffers. 
    - ClearMappedBufferMap: Verifies ClearMappedBufferMap correctly frees 
      transfer buffers mapped via MapBufferSubDataCHROMIUM. 
    - AllocateShadowCopiesForReadbackNullBuffer: Verifies that 
      AllocateShadowCopiesForReadback safely skips buffers that were 
      deleted before being fenced, preventing a null pointer dereference. 
    - AllocateShadowCopiesForReadbackAllocFail: Verifies that 
      AllocateShadowCopiesForReadback handles memory allocation failures 
      gracefully by skipping the shadow allocation instead of issuing a 
      command with an invalid shared memory ID. 
    - AllocateShadowCopiesForReadbackAlreadyAllocated: Verifies that 
      AllocateShadowCopiesForReadback issues a performance warning if a 
      READ-usage buffer is written to multiple times before being fenced. 
    - ReadbackBufferShadowTrackerTest.AllocFails: Verifies that the shadow 
      tracker correctly handles internal allocation failures from 
      MappedMemoryManager. 
     
    (cherry picked from commit 7500f1d78b8c1e52dff6a3966e65c3eafa104d64) 
     
    Bug: 492228019 
    Change-Id: I8e12ffd1ed4356609e7aeeef1552e81e250ae7bd 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7667030 
    Reviewed-by: Kenneth Russell <kbr@chromium.org> 
    Commit-Queue: Gregg Tavares <gman@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1600244} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7699638 
    Auto-Submit: Gregg Tavares <gman@chromium.org> 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Cr-Commit-Position: refs/branch-heads/7680@{#3220} 
    Cr-Branched-From: 76b7d80e5cda23fe6537eed26d68c92e995c7f39-refs/heads/main@{#1582197}

```

---

Files:

- M `gpu/BUILD.gn`
- M `gpu/command_buffer/client/gles2_implementation.cc`
- M `gpu/command_buffer/client/gles2_implementation_unittest.cc`
- M `gpu/command_buffer/client/implementation_base.h`
- M `gpu/command_buffer/client/query_tracker.h`
- M `gpu/command_buffer/client/readback_buffer_shadow_tracker.cc`
- M `gpu/command_buffer/client/readback_buffer_shadow_tracker.h`
- A `gpu/command_buffer/client/readback_buffer_shadow_tracker_unittest.cc`

---

Hash: [2d7a6bc13fd6509c62dd5ce8f4eec51dd2481acb](https://chromiumdash.appspot.com/commit/2d7a6bc13fd6509c62dd5ce8f4eec51dd2481acb)  

Date: Wed Mar 25 19:38:31 2026


---

### pe...@google.com (2026-03-25)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### vi...@google.com (2026-04-03)

For M138 LTS, the [CL containing the fix](https://chromium-review.googlesource.com/7667030) introduce conflicts that would require a large number of dependent CLs to resolve, including a few spanification works which is substantial. Given that this dependency chain is unsafe to merge into LTS, I’m labeling it as not applicable for the M138 LTS.

### vi...@google.com (2026-05-07)

Likewise to [#comment19](https://issues.chromium.org/issues/492228019#comment19), spanification work brings instability for M144 LTS.

### wf...@chromium.org (2026-05-21)

[vrp panel] the asan stack is just a read and not a uaf but we agree with your analysis here. We're not quite sure why asan didn't find this as a uaf - do you have an idea why?

### je...@gmail.com (2026-05-21)

I suspect it's due to issues with the allocator it uses.

### sp...@google.com (2026-05-21)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $11000.00 for this report.

Rationale for this decision:
High quality with bisect. User information disclosure


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-06-24)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/492228019)*
