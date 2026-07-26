# Dawn: heap-use-after-free in wire client ObjectStore via multithreaded WebGPU

| Field | Value |
|-------|-------|
| **Issue ID** | [501096128](https://issues.chromium.org/issues/501096128) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Dawn |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | no...@gmail.com |
| **Assignee** | lo...@google.com |
| **Created** | 2026-04-09 |
| **Bounty** | $1,000.00 |

## Description

---

### Report description

Dawn: heap-use-after-free in wire client ObjectStore via multithreaded WebGPU

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

#### Which URL (or repository) have you found the vulnerability in?

<https://dawn.googlesource.com/dawn>

---

### The problem

#### Please describe the technical details of the vulnerability

## Summary

`ObjectStore::Get()` and `ObjectStore::Insert()` race on the same `std::vector` from two threads. `Get()` runs on the renderer IO thread via `HandleCommands`; `Insert()` runs on the worker thread via Dawn proc stubs. The vector has no synchronization. When `emplace_back` reallocates, the IO thread's `Get()` reads freed memory.

Trigger: a WebGPU worker calling `requestDevice()` while uncaptured error callbacks from the GPU process are being dispatched on the IO thread.

## Affected code

- `third_party/dawn/src/dawn/wire/client/ObjectStore.cpp` — no locking on `Get()` or `Insert()`
- `gpu/command_buffer/client/webgpu_implementation.cc` — `OnGpuControlReturnData` calls `HandleCommands` inline on the IO thread (not posted to the worker)
- `gpu/ipc/client/command_buffer_proxy_impl.cc:168` — `OnReturnData` is a direct call, unlike `OnDestroyed`/`OnSignalAck` which post to `proxy_task_runner_`

The one-sided locking is the root cause: `DawnWireServices::lock_` serializes `HandleCommands` callers, but the worker's Dawn API calls (`wgpuAdapterRequestDevice` → `Client::Make<Device>` → `ObjectStore::Insert`) never acquire it.

## Feature Gate

The `WebGPUMultithreadDawnWireOnWorkers` required feature is experimental and not enabled by default. However, this is not a V8 experimental feature.`WebGPUMapSyncOnWorkers` (also experimental) will enable this too. Neither has an origin trial and the race is only reachable when the feature is active. The POC has --enable-unsafe-webgpu because it is needed for my specific reproduction case of allowing a navigator.gpu initialization on a headless Linux box with GPUs attached.

## Reproduction

Two instrumentation patches are included per [VRP guidelines for race condition reports](https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/vrp-faq.md):

1. **`objectstore_race_window.patch`** — Snapshots the vector's internal data pointer in `Get()`, sleeps 500µs, then dereferences the (now potentially stale) pointer. This simulates the compiler caching `mObjects.data()` in a register across a reallocation. Without this, the race window is ~1 instruction wide.
2. **`force_multithread.patch`** — Force-enables `IsWebGPUMultithreadedWorker()` for workers in content\_shell, where the experimental flag doesn't propagate correctly. This is just so the POC works on content\_shell, and does not affect actual Chrome, and therefore does not affect the validity of the exploit.

```
# Build (ASAN component build, Linux x86_64 with GPU)
patch -p1 < pocs/webgpu_wire_race/objectstore_race_window.patch
patch -p1 < pocs/webgpu_wire_race/force_multithread.patch
gn gen out/asan  # is_asan=true is_component_build=true symbol_level=1 devtools_bundle=false
autoninja -C out/asan content_shell

# Run
Xvfb :99 -screen 0 1280x800x24 &
cd pocs/webgpu_wire_race && python3 -m http.server 8090 &
DISPLAY=:99 LD_LIBRARY_PATH=out/asan \
ASAN_OPTIONS="detect_odr_violation=0:allocator_may_return_null=1:symbolize=1" \
VK_ICD_FILENAMES=/usr/share/vulkan/icd.d/nvidia_icd.json \
out/asan/content_shell --no-sandbox --disable-gpu-sandbox --disable-gpu-watchdog \
    --enable-features=WebGPUService --disable-vulkan-surface --enable-unsafe-webgpu \
    --enable-dawn-features=allow_unsafe_apis,disable_adapter_blocklist \
    --disable-dawn-features=disallow_unsafe_apis --ignore-gpu-blocklist \
    "http://127.0.0.1:8090/poc_delayed.html"

```

With both instrumentation patches applied, crashes within ~60s of workers starting. Real GPU hardware required (SwiftShader is too slow under ASAN to generate enough concurrent traffic).

## ASAN trace

```
==529834==ERROR: AddressSanitizer: heap-use-after-free on address 0x7a6f9be57e18
READ of size 8 at 0x7a6f9be57e18 thread T6 (Chrome_ChildIOT)
    #0 ObjectStore::Get(unsigned int) const             ObjectStore.cpp:106 [instrumented Get]
    #1 Client::Get<Device>(unsigned int)                Client.h:81
    #2 Client::HandleDeviceUncapturedErrorCallback      ClientHandlers_autogen.cpp:67
    #3 Client::HandleCommands(...)                      ClientHandlers_autogen.cpp:129
    #4 WireClient::HandleCommands(...)                  WireClient.cpp:47
    #5 DawnWireServices::HandleCommands(...)            webgpu_implementation.cc:89
    #6 WebGPUImplementation::OnGpuControlReturnData     webgpu_implementation.cc:338
    #7 CommandBufferProxyImpl::OnReturnData(...)         command_buffer_proxy_impl.cc:745
    #8 CommandBufferClientMessageFilter::OnReturnData   command_buffer_proxy_impl.cc:168

freed by thread T23 (DedicatedWorker):
    #0 operator delete(void*, unsigned long)
    ...
    #5 vector<raw_ptr<ObjectBase>>::__emplace_back_slow_path(...)
    #8 ObjectStore::Insert(...)                         ObjectStore.cpp:57
    #9 Client::Make<Device>(...)                        Client.h:72
    #10 Adapter::APIRequestDevice(...)                  Adapter.cpp:323
    #14 GPUAdapter::requestDevice(...)                  gpu_adapter.cc:316

```

Frame #0 line number is from the instrumented `Get()`. The original is `return mObjects[id]` at ~line 89. Full trace in `asan_trace_trimmed.log`.

## Bisect

Introduced by `128493b77655a` (Dec 22 2025) — "[webgpu][blink] Adds the capability to enable multithread GPU replies" (Cr-Commit-Position: refs/heads/main@{#1561916}). Before this commit, all wire replies went to `kMainThread`, so `Get` and `Insert` ran on the same thread.

## Suggested fix

`fix_objectstore_race.patch` — post `HandleCommands` to the worker thread instead of running it inline on the IO thread. Copies the IPC command bytes into an owned buffer and posts via `main_task_runner_`, ensuring all wire client `ObjectStore` access is single-threaded.

#### Impact analysis

Heap-use-after-free in the renderer process (sandboxed). The stale read returns a `raw_ptr<ObjectBase>` from the freed vector buffer, which is cast to `Device*` and dereferenced. The error callback path eventually reads a function pointer (`WGPUUncapturedErrorCallbackInfo::callback`) at a fixed offset from the `Device*`, so a successful heap spray of the freed region could redirect control flow.

MiraclePtr does not apply — BRP protects the `ObjectBase` allocations the `raw_ptr` elements point *to*, not the vector's backing store itself.

The feature is experimental and not currently reachable on Stable without flags.

---

### The cause

#### What version of Chrome have you found the security issue in?

146.0.7680.178 stable

#### Is the security issue related to a crash?

Yes, it is related to a crash.

#### Choose the type of vulnerability

Memory Corruption (in a non-sandboxed process)

#### How would you like to be publicly acknowledged for your report?

Noah Roskin-Frazee (ZeroClicks AI Lab)

## Attachments

- [poc.html](attachments/poc.html) (text/html, 3.4 KB)
- [objectstore_race_window.patch](attachments/objectstore_race_window.patch) (application/octet-stream, 1.5 KB)
- [force_multithread.patch](attachments/force_multithread.patch) (application/octet-stream, 497 B)
- [fix_objectstore_race.patch](attachments/fix_objectstore_race.patch) (application/octet-stream, 3.4 KB)
- [asan_trace.log](attachments/asan_trace.log) (application/octet-stream, 60.6 KB)
- [mmappeddata_asan.txt](attachments/mmappeddata_asan.txt) (text/plain, 16.8 KB)
- [mmappeddata_exploit_primitive_test.txt](attachments/mmappeddata_exploit_primitive_test.txt) (text/plain, 2.6 KB)
- [WireBufferMappedDataRacePOC.cpp](attachments/WireBufferMappedDataRacePOC.cpp) (text/x-c++src, 6.6 KB)

## Timeline

### aj...@google.com (2026-04-10)

Note 1: `--enable-dawn-features=allow_unsafe_apis`

Note 2: This crash is in the renderer and makes more patches than sleep.

Sending to gpu triage, setting S2 as this is racy if valid.

### ch...@google.com (2026-04-10)

Setting Priority to P2 to match Severity s2. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### pe...@google.com (2026-04-10)

If this has this '--enable-dawn-features=allow\_unsafe\_apis' flag as a requirement it might also be security impact none.

### no...@gmail.com (2026-04-10)

It does not require "--enable-dawn-features=allow_unsafe_apis" to replicate this vulnerability. content_shell needed both it and enable-unsafe-webgpu because I was running this on a no-display arm64 Linux box, and WebGPU on content_shell does not like initializing GPUs on headless machines.

The actual gate to the vulnerable path is WebGPUMultithreadDawnWireOnWorkers (or WebGPUMapSyncOnWorkers), which sets support_locking=true → creates main_task_runner_ → enables the multithreaded wire path where HandleCommands runs on the IO thread while Insert runs on the worker thread. No "unsafe" flag involved.

Apologies for any confusion.

### ch...@google.com (2026-04-11)

Setting milestone because of s2 severity.

### lo...@google.com (2026-04-13)

I can take a look at this @ka...@google.com since it seems related to async stuff. Not sure if you already started looking at it though, if not, just re-assign it to me.

### ka...@chromium.org (2026-04-13)

This doesn't have a security impact so I don't think it should be assigned right now. I have added the parent bugs that would require us to fix this so we hopefully don't lose it.

### lo...@google.com (2026-04-13)

FWIW, I read through this again, and I think [b/502037246](https://issues.chromium.org/issues/502037246) is a duplicate of this which I was already looking/working at so gonna assign myself this and dedup the other one since this once seems like it came first.

### no...@gmail.com (2026-04-14)

Curious how we can conclude this doesn't have any security impact given that it is a triggerable UAF with attacker-controlled addressing. If this is due to the flags, the unsafe flags are not actually needed to replicate this on customer hardware, unless that customer is using Linux with no display output but a GPU.

### ka...@chromium.org (2026-04-14)

It's because of `WebGPUMultithreadDawnWireOnWorkers`/`WebGPUMapSyncOnWorkers`, those are experimental flags for prototype features that AFAIK we don't have plans to ship very soon.

### no...@gmail.com (2026-04-15)

There are a couple other racy UAFs from the same bisect with the same experimental gate flags. I don't want to waste time, so submitting an ASAN stacktrace and POC for one that is RCE-y in Buffer::mMappedData / FreeMappedData (controlled write + heap slot reclaim of 256 bytes).

Buffer::GetMappedRange() reads mMappedData while Buffer::FreeMappedData() frees the backing memory and nulls the pointer. The dangling void* is returned to the caller, outside raw_ptr scope. MiraclePtr Status: NOT PROTECTED in BRP-enabled ASAN build. Demonstrated heap slot reclaim — writes through the dangling pointer corrupt subsequently allocated objects in the same bucket.

Let me know if you want this in a separate submission though.

### dx...@google.com (2026-04-16)

Project: dawn  

Branch:  main  

Author:  Lokbondo Kung [lokokung@google.com](mailto:lokokung@google.com)  

Link:    <https://dawn-review.googlesource.com/302499>

[wire][client] Make the object tables thread-safe.

---


Expand for full commit details
```
     
    - This is only necessary to handle the always spontaneous logging and 
      uncaptured error callbacks. The lookup table for the handles of 
      these objects on the client can race since callbacks can be called 
      from multiple threads, i.e. the main thread can be creating a new 
      object, while the callback thread could be trying to lookup another 
      existing one. 
     
    Bug: 501096128 
    Change-Id: I8d6da30d7cfb416507b458d8c39086a35532684f 
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/302499 
    Auto-Submit: Loko Kung <lokokung@google.com> 
    Commit-Queue: Loko Kung <lokokung@google.com> 
    Reviewed-by: Kai Ninomiya <kainino@chromium.org>

```

---

Files:

- M `src/dawn/wire/client/Client.cpp`
- M `src/dawn/wire/client/ObjectBase.h`
- M `src/dawn/wire/client/ObjectStore.cpp`
- M `src/dawn/wire/client/ObjectStore.h`

---

Hash: 865a3ec300872807864a27fb2b58fb3b29a72507  

Date: Thu Apr 16 08:56:31 2026


---

### dx...@google.com (2026-04-16)

Project: chromium/src  

Branch:  main  

Author:  [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com) [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com)  

Link:    <https://chromium-review.googlesource.com/7768584>

Roll Dawn from 936cc1681ce3 to 865a3ec30087 (3 revisions)

---


Expand for full commit details
```
     
    https://dawn.googlesource.com/dawn.git/+log/936cc1681ce3..865a3ec30087 
     
    2026-04-16 lokokung@google.com [wire][client] Make the object tables thread-safe. 
    2026-04-16 dawn-autoroll@skia-public.iam.gserviceaccount.com Roll DirectX Shader Compiler from 5f8d05f9b760 to 6dee5ce027b0 (10 revisions) 
    2026-04-16 dawn-autoroll@skia-public.iam.gserviceaccount.com Roll ANGLE from e45b5fbf2710 to 942c07d0c8a6 (6 revisions) 
     
    If this roll has caused a breakage, revert this CL and stop the roller 
    using the controls here: 
    https://autoroll.skia.org/r/dawn-chromium-autoroll 
    Please CC amaiorano@google.com,cwallez@google.com on the revert to ensure that a human 
    is aware of the problem. 
     
    To file a bug in Dawn: https://bugs.chromium.org/p/dawn/issues/entry 
    To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry 
     
    To report a problem with the AutoRoller itself, please file a bug: 
    https://issues.skia.org/issues/new?component=1389291&template=1850622 
     
    Documentation for the AutoRoller is here: 
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md 
     
    Cq-Include-Trybots: luci.chromium.try:dawn-android-arm-deps-rel;luci.chromium.try:dawn-android-arm64-deps-rel;luci.chromium.try:dawn-linux-x64-deps-rel;luci.chromium.try:dawn-mac-x64-deps-rel;luci.chromium.try:dawn-mac-arm64-deps-rel;luci.chromium.try:dawn-win10-x64-deps-rel;luci.chromium.try:dawn-win10-x86-deps-rel;luci.chromium.try:dawn-win11-arm64-deps-rel;luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:gpu-fyi-cq-mac-arm64;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:gpu-fyi-cq-android-arm64 
    Bug: chromium:501096128 
    Tbr: amaiorano@google.com 
    Change-Id: I1748c61eda184ff31e52b2c8de38223f6df8081e 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7768584 
    Bot-Commit: chromium-autoroll@skia-public.iam.gserviceaccount.com <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Commit-Queue: chromium-autoroll@skia-public.iam.gserviceaccount.com <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Cr-Commit-Position: refs/heads/main@{#1615841}

```

---

Files:

- M `DEPS`
- M `third_party/dawn`

---

Hash: [52b381ba3fd1fe6a0a71396a5f043d544ecd312f](https://chromiumdash.appspot.com/commit/52b381ba3fd1fe6a0a71396a5f043d544ecd312f)  

Date: Thu Apr 16 14:37:44 2026


---

### no...@gmail.com (2026-06-15)

Hi,

I know that the team has been extremely busy with AI-assisted reports. Since it has been a couple months, I wanted to check if there is any update on the reward for this report?

### cw...@google.com (2026-06-22)

I'm not sure what the escalation path is for the reward panel (and I'm not part of it), but given that this is for an experimental feature that was not close to launching, I think it wouldn't qualify.

### sp...@google.com (2026-06-22)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
Highly mitigated renderer.


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-07-24)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/501096128)*
