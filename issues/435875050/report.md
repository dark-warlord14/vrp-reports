# WebGPU dawn::native::d3d12::ResourceAllocatorManager::Tick Heap-Use-After-Free

| Field | Value |
|-------|-------|
| **Issue ID** | [435875050](https://issues.chromium.org/issues/435875050) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Dawn |
| **Platforms** | Windows |
| **Chrome Version** | 140.0.7317.0 |
| **Reporter** | wl...@gmail.com |
| **Assignee** | lo...@google.com |
| **Created** | 2025-08-03 |
| **Bounty** | $15,000.00 |

## Description

# Steps to reproduce the problem

## Steps to reproduce

1. Run open\_PoC.bat (launches a local HTTP server and opens chromium)
2. Navigates to PoC.html, The flag —no-sandbox is used for ASAN output. ⇒ `./chrome.exe --no-sandbox http://localhost:8000/PoC.html`
3. After a few reload cycles, the GPU process crashes. On ASan builds, you will see a **heap-use-after-free**

**open\_PoC.bat**

```
@echo off
cd /d %~dp0

start "" python -m http.server 8000

timeout /t 2 >nul

start "" http://localhost:8000/PoC.html


```
# Problem Description

### Description

This issue is a heap-use-after-free bug in the Dawn D3D12 backend of Chromium/WebGPU, **observed only on Windows systems without a discrete GPU (e.g., integrated GPU or GPU-less notebook environments)**, triggered by resource lifetime mismanagement during asynchronous GPU command execution.

### Impact

When specific WebGPU operations are performed (creating large depth/stencil textures, creating incompatible texture views, and issuing `copyTextureToBuffer` with intentionally misaligned parameters), the GPU process consistently crashes.

### Root Cause

The root cause lies in `third_party/dawn/src/dawn/native/d3d12/ResourceAllocatorManagerD3D12.cpp`:

```
void ResourceAllocatorManager::Tick(ExecutionSerial completedSerial) {
    for (ResourceHeapAllocation& allocation :
         mAllocationsToDelete.IterateUpTo(completedSerial)) {
        if (allocation.GetInfo().mMethod == AllocationMethod::kSubAllocated) {
            FreeSubAllocatedMemory(allocation);
        }
    }
    mAllocationsToDelete.ClearUpTo(completedSerial);
    mHeapsToDelete.ClearUpTo(completedSerial);
}


```

`Tick()` is called with a `completedSerial` that Dawn believes corresponds to all finished GPU work. However, in certain timing conditions, commands that still reference these `Heap` objects may not yet be fully retired on the GPU. This allows the manager to clear and free heap resources prematurely.

Later, when `ResidencyManager::EnsureHeapsAreResident()` iterates over those heap pointers to lock residency before executing a new command list, it dereferences stale pointers to already-freed memory. This results in a reproducible **use-after-free read** (and potentially write) condition.

### mitigation suggestion

Use-after-free can be mitigated by introducing a reference counting mechanism for D3D12 Heaps:

retain the Heap while any command list or resource still references it, and only free when the ref-count drops to zero after GPU work completion.

### How to Fix

The root cause is that `ResourceAllocatorManager::Tick()` may free `ResourceHeapAllocation` objects that are still referenced by in-flight GPU commands.

To fix this, **introdue reference counting (or strong ownership tracking) for heap allocations** instead of relying solely on `completedSerial`.

**Key steps:**

1. **Add a ref-count to ResourceHeapAllocation / Heap objects**
   - Increment the ref-count when a command list or texture/buffer references a heap.
   - Decrement the ref-count only after the GPU has signaled completion of the work using that heap.
2. **Modify Tick() to defer freeing**
   - In `Tick()`, instead of calling `FreeSubAllocatedMemory()` and `ClearUpTo()` immediately,
     
     check whether the ref-count for each `allocation` has reached 0.
   - Only free and clear entries when no active references remain.
3. **Validation**
   - Optionally add debug assertions (in ASan/Debug builds) to ensure that no heap is accessed after free.
   - This prevents use-after-free bugs when commands complete later than `completedSerial` suggests.

**Pseudo-code adjustment:**

```
void ResourceAllocatorManager::Tick(ExecutionSerial completedSerial) {
    for (ResourceHeapAllocation& allocation :
         mAllocationsToDelete.IterateUpTo(completedSerial)) {

        if (allocation.refCount == 0 &&
            allocation.GetInfo().mMethod == AllocationMethod::kSubAllocated) {
            FreeSubAllocatedMemory(allocation);
        } else {
            // Still in use: defer deletion
            DeferAllocation(allocation);
        }
    }

    // Clear only those heaps that are confirmed unused
    mAllocationsToDelete.RemoveIf([](auto& alloc) { return alloc.refCount == 0; });
    mHeapsToDelete.RemoveIf([](auto& heap) { return heap.refCount == 0; });
}

```

This ensures that heap objects will not be freed prematurely, eliminating the race that leads to the use-after-free.

# Summary

WebGPU dawn::native::d3d12::ResourceAllocatorManager::Tick Heap-Use-After-Free

# Custom Questions

#### Type of crash:

see ASan

#### Crash state:

ASan stack trace

Heap-use-after-free (read) detected by ASan.

```
READ of size 4 at 0x12a6a8aec854 thread T0
    #0 0x7ff8e93af829 in dawn::native::d3d12::Pageable::IsResidencyLocked(void) const C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d12\PageableD3D12.cpp:86:12
    #1 0x7ff8e93c8159 in dawn::native::d3d12::ResidencyManager::EnsureHeapsAreResident(class dawn::native::d3d12::Heap **, unsigned __int64) C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d12\ResidencyManagerD3D12.cpp:263:19
    #2 0x7ff8e9398acf in dawn::native::d3d12::CommandRecordingContext::ExecuteCommandList(class dawn::native::d3d12::Device *, struct ID3D12CommandQueue *) C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d12\CommandRecordingContext.cpp:77:5
    #3 0x7ff8e93bee55 in dawn::native::d3d12::Queue::SubmitPendingCommandsImpl(void) C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d12\QueueD3D12.cpp:133:5
    #4 0x7ff8e9163d98 in dawn::native::ExecutionQueueBase::SubmitPendingCommands(void) C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\ExecutionQueue.cpp:112:19
    #5 0x7ff8e93a4938 in dawn::native::d3d12::Device::TickImpl(void) C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d12\DeviceD3D12.cpp:366:5
    #6 0x7ff8e90c37d9 in dawn::native::DeviceBase::Destroy(void) C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Device.cpp:665:22
    #7 0x7ff8e8fa2258 in dawn::native::NativeDeviceDestroy(struct WGPUDeviceImpl *) C:\b\s\w\ir\cache\builder\src\out\069a-Win_ASan_Releas\gen\third_party\dawn\src\dawn\native\ProcTable.cpp:921:15
...
freed by thread T0 here:
    #0 0x7ff96150c584  (C:\Users\wlsrb\Desktop\bugs\chromium-140.0.7317.0-win64-asan\clang_rt.asan_dynamic-x86_64.dll+0x18005c584)
    #1 0x7ff8e93af1ce in dawn::native::d3d12::Heap::`scalar deleting dtor'(unsigned int) C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d12\HeapD3D12.h:42:7
    #2 0x7ff8e6f83124 in std::__Cr::default_delete<perfetto::internal::TracingMuxerImpl::ConsumerImpl>::operator() C:\b\s\w\ir\cache\builder\src\third_party\libc++\src\include\__memory\unique_ptr.h:77
    #3 0x7ff8e6f83124 in std::__Cr::unique_ptr<perfetto::internal::TracingMuxerImpl::ConsumerImpl,std::__Cr::default_delete<perfetto::internal::TracingMuxerImpl::ConsumerImpl> >::reset C:\b\s\w\ir\cache\builder\src\third_party\libc++\src\include\__memory\unique_ptr.h:290


```
#### Reporter credit:

Giunash (Gyujeong Jin) of BoB 14th

# Additional Data

Category: Security   

Chrome Channel: Dev   

Regression: N/A \

## Attachments

- [Asan_logs.txt](attachments/Asan_logs.txt) (text/plain, 38.3 KB)
- [PoC.html](attachments/PoC.html) (text/html, 1.6 KB)

## Timeline

### wl...@gmail.com (2025-08-03)

A credit is omitted.

- 이동하 ( Lee Dong Ha of BoB 14th )

### ja...@chromium.org (2025-08-04)

[security shepherd]
Thanks for the report! I'm working on reproducing this.

I'll treat this as speculatively valid and add some other team members to take a look.

### ja...@chromium.org (2025-08-04)

Adding a few others based on a similar stack trace in [issue 380013515](https://issues.chromium.org/issues/380013515)

### ja...@chromium.org (2025-08-04)

All security bugs need an owner. Setting the owner to lokokung.

### ja...@chromium.org (2025-08-04)

This is memory corruption in WebGPU on a sandboxed OS, so assigning S2 (medium).

### ch...@google.com (2025-08-05)

Setting milestone because of s2 severity.

### ch...@google.com (2025-08-05)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### cw...@chromium.org (2025-08-05)

Looking at the ASAN logs, everything seems to be during a single Device::Destroy call. When destroying the following happens:

```
READ of size 4 at 0x12a6a8aec854 thread T0
    #0 0x7ff8e93af829 in dawn::native::d3d12::Pageable::IsResidencyLocked(void) const C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d12\PageableD3D12.cpp:86:12
    #1 0x7ff8e93c8159 in dawn::native::d3d12::ResidencyManager::EnsureHeapsAreResident(class dawn::native::d3d12::Heap **, unsigned __int64) C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d12\ResidencyManagerD3D12.cpp:263:19
    #2 0x7ff8e9398acf in dawn::native::d3d12::CommandRecordingContext::ExecuteCommandList(class dawn::native::d3d12::Device *, struct ID3D12CommandQueue *) C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d12\CommandRecordingContext.cpp:77:5
    #3 0x7ff8e93bee55 in dawn::native::d3d12::Queue::SubmitPendingCommandsImpl(void) C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d12\QueueD3D12.cpp:133:5
    #4 0x7ff8e9163d98 in dawn::native::ExecutionQueueBase::SubmitPendingCommands(void) C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\ExecutionQueue.cpp:112:19
    #5 0x7ff8e93a4938 in dawn::native::d3d12::Device::TickImpl(void) C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d12\DeviceD3D12.cpp:366:5
    #6 0x7ff8e90c37d9 in dawn::native::DeviceBase::Destroy(void) C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Device.cpp:665:22
    #7 0x7ff8e8fa2258 in dawn::native::NativeDeviceDestroy(struct WGPUDeviceImpl *) C:\b\s\w\ir\cache\builder\src\out\069a-Win_ASan_Releas\gen\third_party\dawn\src\dawn\native\ProcTable.cpp:921:15
    #8 0x7ff8fe9c77c1 in wgpu::Device::Destroy C:\b\s\w\ir\cache\builder\src\out\069a-Win_ASan_Releas\gen\third_party\dawn\include\dawn\webgpu_cpp.h:8726
```

Which doesn't really make sense because we are in a destruction and shouldn't submit pending commands. This Tick call happens after we "assume the commands completed" on the queue, causing the ExecutionSerial to be larger than all previously seen ones. So any pending deletion of heaps is performed, even if the pending commands (that we wrongly submit) are using them.

Loko you seem to be a good owner for this issue given that you are looking at queues and execution serials these days.

### wl...@gmail.com (2025-08-13)

Hi!
I was able to look into the code and get a clearer picture of the root cause. I'm sharing my understanding below in case it's helpful.

Based on my reading of the code, the issue seems to originate from the sequence of operations in `DeviceBase::Destroy()`. Specifically, this block:

```
// at DeviceBase::Destroy() in third_party/dawn/src/dawn/native/Device.cp
if (mState != State::BeingCreated) {
    // ...
    mQueue->AssumeCommandsComplete();
    DAWN_ASSERT(mQueue->GetCompletedCommandSerial() == mQueue->GetLastSubmittedCommandSerial());
    mQueue->Tick(mQueue->GetCompletedCommandSerial());

    // Call TickImpl once last time to clean up resources
    // Ignore errors so that we can continue with destruction
    IgnoreErrors(TickImpl());
}

```

The logic first calls `mQueue->AssumeCommandsComplete()`, which marks all pending work as finished and makes associated resources ready for their final deletion. However, it then immediately calls `TickImpl()` under the assumption that it's only for cleanup, as the comment suggests.

The problem is that the D3D12 backend's `Device::TickImpl()` does more than just clean up. it actively tries to submit new commands:

```
// at d3d12::Device::TickImpl() third_party/dawn/src/dawn/native/d3d12/DeviceD3D12.cpp
MaybeError Device::TickImpl() {
    // ... (cleanup operations based on completedSerial) ...

    DAWN_TRY(ToBackend(GetQueue())->SubmitPendingCommands());

    // ...
    return {};
}

```

This sequence seems to create the race condition. `TickImpl()` can submit a new command that uses a resource right as the destruction process, accelerated by `AssumeCommandsComplete()`, is freeing that exact same resource. In my thought, it can explain the use-after-free crash reported by ASAN.

Please correct me if my understanding is off.
Thanks!

### ch...@google.com (2025-08-19)

lokokung: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### lo...@google.com (2025-08-19)

Took a look at this, and will look a bit more into it tomorrow since I don't have a Windows machine with an integrated GPU on me atm, but the issue is interesting because `AssumeCommandsComplete` is always called after `WaitForIdleForDestruction` which immediately empties pending commands. So somehow, in between those calls, somewhere we are calling `Queue::ForceEventualFlushOfCommands()` or `Queue::GetPendingCommandContext()` to result in what would appear as new commands. I should be able to get my hands on a machine to repro and see where those calls are happening tomorrow and hopefully send a fix out for this soon.

### lo...@google.com (2025-08-19)

FWIW, I did notice that in the places we call `WaitForIdleForDestruction`, `TickImpl`, and `AssumeCommandsComplete`, we actually call those three in different orders.

1. In `DeviceBase::HandleError` for injected device lost errors:
   
   - `WaitForIdleForDestruction`
   - `AssumeCommandsComplete`
2. In `DeviceBase::HandleError` for disallowed and non-device lost errors:
   
   - `WaitForIdleForDestruction`
   - `TickImpl`
   - `AssumeCommandsComplete`
3. In `DeviceBase::Destroy`:
   
   - `WaitForIdleForDestruction`
   - `AssumeCommandsComplete`
   - `TickImpl`

I suspect, that the correct thing to do is actually 2 in all cases, since all three code-paths are effectively trying to gracefully teardown the GPU. Semantically, it would therefore make sense to wait for idle, then tick one last time which is currently necessary to clean up potentially remaining resources that aren't cleaned up by waiting for idle, and finally, assume that all commands are complete. In theory, I think that we shouldn't even need to explicitly assume commands complete because wait for idle should do that. The `AssumeCommandsComplete` helper should only be used in the case of a real GPU device loss when we cannot gracefully teardown.

I will speculatively implement a fix that makes all three of those paths equivalent to 2, and then further confirm whether it fixes the repro case tomorrow. I'm also tagging [cwallez@chromium.org](mailto:cwallez@chromium.org) here to double check my understanding above.

### dx...@google.com (2025-08-20)

Project: dawn  

Branch:  main  

Author:  Lokbondo Kung [lokokung@google.com](mailto:lokokung@google.com)  

Link:    <https://dawn-review.googlesource.com/258175>

[dawn][native] Standardize calling order for graceful device teardown.

---


Expand for full commit details
```
     
    - Updates all the code-paths to call the graceful device teardown 
      helpers in the same order. 
    - See https://g-issues.chromium.org/issues/435875050#comment13 for 
      breakdown of the logic for ordering it in this manner. 
     
    Bug: 435875050 
    Change-Id: Ife7dfcb2c333f9b9bbc2895b683974e96119e73f 
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/258175 
    Auto-Submit: Loko Kung <lokokung@google.com> 
    Commit-Queue: Corentin Wallez <cwallez@chromium.org> 
    Reviewed-by: Corentin Wallez <cwallez@chromium.org>

```

---

Files:

- M `src/dawn/native/Device.cpp`

---

Hash: 1237c6eccd8822df3fcd76a10be27234d4ba9918  

Date: Wed Aug 20 12:01:25 2025


---

### dx...@google.com (2025-08-20)

Project: chromium/src  

Branch:  main  

Author:  chromium-autoroll [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com)  

Link:    <https://chromium-review.googlesource.com/6866978>

Roll Dawn from fc20981a1a59 to 8ed25cea7c18 (9 revisions)

---


Expand for full commit details
```
     
    https://dawn.googlesource.com/dawn.git/+log/fc20981a1a59..8ed25cea7c18 
     
    2025-08-20 cwallez@chromium.org [dawn][native] Add BindGroupBase::GetBindingAsBuffer 
    2025-08-20 diejorarr@gmail.com [dawn] Add `TexelBuffer` buffer usage bit 
    2025-08-20 cwallez@chromium.org [dawn][native] Use BGL index iterators for PassResourceUsageTracker 
    2025-08-20 lokokung@google.com [dawn][native] Standardize calling order for graceful device teardown. 
    2025-08-20 jimblackler@google.com Kotlin: replace 'callback' with a custom on... method name 
    2025-08-20 jimblackler@google.com Kotlin: specify @JvmField on enum-type constants 
    2025-08-20 cwallez@chromium.org [dawn][native] Use BGL index iterators for BindGroupVk init. 
    2025-08-20 jimblackler@google.com Kotlin: supply a hashCode on objects, matching the existing toEquals 
    2025-08-20 bsheedy@google.com Move SurfaceTests skip 
     
    If this roll has caused a breakage, revert this CL and stop the roller 
    using the controls here: 
    https://autoroll.skia.org/r/dawn-chromium-autoroll 
    Please CC bajones@google.com,cwallez@google.com on the revert to ensure that a human 
    is aware of the problem. 
     
    To file a bug in Dawn: https://bugs.chromium.org/p/dawn/issues/entry 
    To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry 
     
    To report a problem with the AutoRoller itself, please file a bug: 
    https://issues.skia.org/issues/new?component=1389291&template=1850622 
     
    Documentation for the AutoRoller is here: 
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md 
     
    Cq-Include-Trybots: luci.chromium.try:dawn-android-arm-deps-rel;luci.chromium.try:dawn-android-arm64-deps-rel;luci.chromium.try:dawn-linux-x64-deps-rel;luci.chromium.try:dawn-mac-x64-deps-rel;luci.chromium.try:dawn-mac-arm64-deps-rel;luci.chromium.try:dawn-win10-x64-deps-rel;luci.chromium.try:dawn-win10-x86-deps-rel;luci.chromium.try:dawn-win11-arm64-deps-rel;luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:gpu-fyi-cq-android-arm64 
    Bug: chromium:382544164,chromium:385317083,chromium:41488897,chromium:42242088,chromium:435875050,chromium:438554018,chromium:438698368,chromium:439565641,chromium:439760125,chromium:439765594 
    Tbr: bajones@google.com 
    Test: Test: ./gradlew connectedAndroidTest 
    Test: Test: ./gradlew connectedAndroidTests 
    Change-Id: I20b257c05763680aa18eea15ac1b3215c30950f9 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6866978 
    Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Cr-Commit-Position: refs/heads/main@{#1503973}

```

---

Files:

- M `DEPS`
- M `third_party/dawn`

---

Hash: [29aed41d0ba5dfd2dd441d8154873ccf115a0e7c](https://chromiumdash.appspot.com/commit/29aed41d0ba5dfd2dd441d8154873ccf115a0e7c)  

Date: Wed Aug 20 15:40:55 2025


---

### lo...@google.com (2025-08-20)

Note that the speculative fix has landed and rolled into Chromium. I will try to verify later once I have a Windows machine without a discrete GPU available to try the repro case.

### lo...@google.com (2025-08-28)

I have not been able to repro the issue with or without my change anymore. I suspect that the issue was fixed, but would encourage the original reporter to try again to see if they can still repro. Otherwise, I am leaning towards closing the issue.

### lo...@google.com (2025-09-03)

Closing this for now. If there's any indication that the crash is still happening, feel free to reopen or file another bug.

### ch...@google.com (2025-09-03)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### ch...@google.com (2025-09-11)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M140. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M141. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [140, 141].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### lo...@google.com (2025-09-11)

This is the only CL that needs to be backmerged to Dawn branches for 140 and 141: <https://dawn-review.googlesource.com/c/dawn/+/258175>

There are current no known risks, and the fix has been in for ~3 weeks without issues.

### ts...@google.com (2025-09-11)

Please merge to M140 (7339) by EOD Friday, and M141 (7390).

### lo...@google.com (2025-09-11)

Merge for 140 is here: <https://dawn-review.googlesource.com/c/dawn/+/261574>

I don't think this needs to be merged into 141 since 141's branch already includes the change.

### sp...@google.com (2025-09-11)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $15000.00 for this report.

Rationale for this decision:
high quality report of memory corruption in the GPU


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### dx...@google.com (2025-09-12)

Project: dawn  

Branch:  chromium/7339  

Author:  Lokbondo Kung [lokokung@google.com](mailto:lokokung@google.com)  

Link:    <https://dawn-review.googlesource.com/261574>

[dawn][native] Standardize calling order for graceful device teardown.

---


Expand for full commit details
```
     
    - Updates all the code-paths to call the graceful device teardown 
      helpers in the same order. 
    - See https://g-issues.chromium.org/issues/435875050#comment13 for 
      breakdown of the logic for ordering it in this manner. 
     
    Bug: 435875050 
    Change-Id: Ife7dfcb2c333f9b9bbc2895b683974e96119e73f 
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/258175 
    Auto-Submit: Loko Kung <lokokung@google.com> 
    Commit-Queue: Corentin Wallez <cwallez@chromium.org> 
    Reviewed-by: Corentin Wallez <cwallez@chromium.org> 
    (cherry picked from commit 1237c6eccd8822df3fcd76a10be27234d4ba9918) 
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/261574 
    Reviewed-by: Kai Ninomiya <kainino@chromium.org> 
    Commit-Queue: Kai Ninomiya <kainino@chromium.org>

```

---

Files:

- M `src/dawn/native/Device.cpp`

---

Hash: 67be7fddacc4f4bcb21d0cf7bf8bb18752d8fb08  

Date: Fri Sep 12 05:28:37 2025


---

### ch...@google.com (2025-09-15)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-09-15)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### wl...@gmail.com (2025-09-20)

Thank you for your Fixing.

I gracefully checked release note.
But, there is ommited credit of this issue.
Can you check the credit again please?

DongHa Lee(@gap\_dev)

### wl...@gmail.com (2025-09-29)

How are things coming along?

### cw...@chromium.org (2025-09-29)

tsepez@ do you know who could answer #28?

### ch...@google.com (2025-12-11)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> high quality report of memory corruption in the GPU

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/435875050)*
