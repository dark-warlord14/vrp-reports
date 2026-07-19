# heap-use-after-free in dawn::native::vulkan::BindGroupLayout::GetOrCreateSpecializedHandle

| Field | Value |
|-------|-------|
| **Issue ID** | [500609038](https://issues.chromium.org/issues/500609038) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | Dawn |
| **Platforms** | Android, Fuchsia, Linux, ChromeOS |
| **Reporter** | ki...@gmail.com |
| **Assignee** | lo...@google.com |
| **Created** | 2026-04-08 |
| **Bounty** | $11,000.00 |

## Description

# VULNERABILITY DETAILS

WebGPU supports compiling compute pipelines asynchronously via the `createComputePipelineAsync` API. This spawns background task worker threads in `ThreadPoolForeg` to initialize the pipeline in the backend. During backend layout construction, `BindGroupLayout` leverages an `absl::flat_hash_map` named `mSpecializations` to cache and specialize Vulkan descriptor sets and layouts based on `ExternalTexture` parameters.

In `BindGroupLayout::GetOrCreateSpecializedHandle`, the asynchronous background thread invokes `find` to look up an existing layout for the given `specialization` [0]. However, there is no synchronization or mutex protecting concurrent accesses to this `absl::flat_hash_map`.

Concurrently, the front-end JS can trigger operations on the main GPU thread, such as executing `queue.submit` with alternating `ExternalTexture` bindings to continuously incur cache misses on newly allocated combinations. Because of the intentional cache misses, `GetOrCreateSpecializedHandle` executes on the main GPU thread and frequently inserts new items into the same hash map [1].

```
ResultOrError<VkDescriptorSetLayout> BindGroupLayout::GetOrCreateSpecializedHandle(
    const Specialization& specialization) {
    if (auto it = mSpecializations.find(specialization); it != mSpecializations.end()) { // [0]
        return it->second; // [2]
    }

// ...

    VkDescriptorSetLayout specialized;
    DAWN_TRY(
        CheckVkSuccess(device->fn.CreateDescriptorSetLayout(device->GetVkDevice(), &createInfo,
                                                            nullptr, &*specialized),
                       "CreateDescriptorSetLayout"));

    mSpecializations.insert({specialization, specialized}); // [1]
    return specialized;
}

```

This unsynchronized `insert` operation can intermittently trigger an internal target container reallocation `rehash`, which drops the backing nodes. If the worker thread performs `mSpecializations.find()` at the same time and attempts to dereference the iterator `it->second` [2], a data race ensues, leading to heap-use-after-free.

[0] <https://source.chromium.org/chromium/chromium/src/+/main:third_party/dawn/src/dawn/native/vulkan/BindGroupLayoutVk.cpp;drc=35a1c65f9e2f12819540d824d414ae0109bb1b10;l=263>

[1] <https://source.chromium.org/chromium/chromium/src/+/main:third_party/dawn/src/dawn/native/vulkan/BindGroupLayoutVk.cpp;drc=35a1c65f9e2f12819540d824d414ae0109bb1b10;l=285>

[2] <https://source.chromium.org/chromium/chromium/src/+/main:third_party/dawn/src/dawn/native/vulkan/BindGroupLayoutVk.cpp;drc=35a1c65f9e2f12819540d824d414ae0109bb1b10;l=264>

# BISECTION

Introduced by Dawn upstream commit [0] which added runtime specialization of pipelines and the `absl::flat_hash_map` caching mechanism without mutex protection.

This regression was rolled into Chromium in commit [1].

[0] <https://dawn.googlesource.com/dawn/+/66c4d93dc91932933c4bd66ff6afba1562d51259> ([YUV AHB] Add runtime specialization of pipelines)

[1] <https://chromium.googlesource.com/chromium/src/+/5ba6a05e0af48d7b5a38703d0844fea105c5e1fc> (Roll Dawn from b263aff3bd77 to 7ae353ac9aa9 (5 revisions))

# VERSION

Chrome Version: HEAD

Operating System: Linux

# REPRODUCTION CASE

`poc.patch` is a simple patch that introduces a 50ms artificial sleep in the GPU process to widen the data race window, ensuring the race is won reliably.

1. Apply `poc.patch`, then build Chromium with ASan.
2. Host the `poc.html` on an HTTP server.
3. Run Chrome against the PoC.

```
$ python3 -m http.server
$ ./out/asan/chrome --enable-dawn-features=vulkan_force_static_samplers_for_external_textures "http://localhost:8000/poc.html"

```
# CRASH INFORMATION

Type of crash: GPU process

Crash log: see the attached `asan.txt` ASan trace.

# CREDIT INFORMATION

Reporter credit: Anonymous

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 29.4 KB)
- [poc.html](attachments/poc.html) (text/html, 4.1 KB)
- [poc.patch](attachments/poc.patch) (text/x-diff, 893 B)

## Timeline

### aj...@google.com (2026-04-09)

patch adds a small sleep - this might be reasonable but leaving for the gpu team to take a look

### pe...@google.com (2026-04-09)

Yes a small sleep of 50ms can happen for any thread at any time on over utilized machines.

### pe...@google.com (2026-04-09)

This looks to be quite serious. Use after free in gpu triggered from web content.

### ch...@google.com (2026-04-10)

Setting milestone because of s0/s1 severity.

### dx...@google.com (2026-04-10)

Project: dawn  

Branch:  main  

Author:  Lokbondo Kung [lokokung@google.com](mailto:lokokung@google.com)  

Link:    <https://dawn-review.googlesource.com/301935>

[native][vulkan] Wrap BindGroupLayout cache with a mutex.

---


Expand for full commit details
```
     
    - Because we dynamically create BGLs when initializing pipelines, 
      and because pipelines may be created asynchronously, we need to 
      make sure that access to the cache map doesn't mangle the data. 
     
    Bug: 500609038 
    Change-Id: I6ffc093773c1c8308bbc95f62da1f202622908db 
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/301935 
    Auto-Submit: Loko Kung <lokokung@google.com> 
    Reviewed-by: Kyle Charbonneau <kylechar@google.com> 
    Commit-Queue: Kyle Charbonneau <kylechar@google.com>

```

---

Files:

- M `src/dawn/native/vulkan/BindGroupLayoutVk.cpp`
- M `src/dawn/native/vulkan/BindGroupLayoutVk.h`

---

Hash: cea524cfcd4c24764cc2a2dce19290ecb1031b27  

Date: Fri Apr 10 13:52:26 2026


---

### ky...@chromium.org (2026-04-10)

Is `OpaqueYCbCrAndroidForExternalTexture` enabled anywhere yet? I think BindGroupLayout only creates a new specialized DescriptorSetLayouts when that feature is in use (or test only `VulkanForceStaticSamplersForExternalTextures` feature enabled in the POC). cwallez@ would have to confirm. If the feature isn't enabled I think this is going to be security impact none.

### dx...@google.com (2026-04-10)

Project: chromium/src  

Branch:  main  

Author:  [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com) [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com)  

Link:    <https://chromium-review.googlesource.com/7747031>

Roll Dawn from 086b2c1e5be7 to cea524cfcd4c (2 revisions)

---


Expand for full commit details
```
     
    https://dawn.googlesource.com/dawn.git/+log/086b2c1e5be7..cea524cfcd4c 
     
    2026-04-10 lokokung@google.com [native][vulkan] Wrap BindGroupLayout cache with a mutex. 
    2026-04-10 dawn-autoroll@skia-public.iam.gserviceaccount.com Roll OpenGL-Registry from 5bae8738b23d to 9cb90ca4902d (90 revisions) 
     
    If this roll has caused a breakage, revert this CL and stop the roller 
    using the controls here: 
    https://autoroll.skia.org/r/dawn-chromium-autoroll 
    Please CC chouinard@google.com,cwallez@google.com on the revert to ensure that a human 
    is aware of the problem. 
     
    To file a bug in Dawn: https://bugs.chromium.org/p/dawn/issues/entry 
    To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry 
     
    To report a problem with the AutoRoller itself, please file a bug: 
    https://issues.skia.org/issues/new?component=1389291&template=1850622 
     
    Documentation for the AutoRoller is here: 
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md 
     
    Cq-Include-Trybots: luci.chromium.try:dawn-android-arm-deps-rel;luci.chromium.try:dawn-android-arm64-deps-rel;luci.chromium.try:dawn-linux-x64-deps-rel;luci.chromium.try:dawn-mac-x64-deps-rel;luci.chromium.try:dawn-mac-arm64-deps-rel;luci.chromium.try:dawn-win10-x64-deps-rel;luci.chromium.try:dawn-win10-x86-deps-rel;luci.chromium.try:dawn-win11-arm64-deps-rel;luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:gpu-fyi-cq-mac-arm64;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:gpu-fyi-cq-android-arm64 
    Bug: chromium:500609038 
    Tbr: chouinard@google.com 
    Change-Id: If980f3d65cd63284a237799dd85bcf5d848e9285 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7747031 
    Bot-Commit: chromium-autoroll@skia-public.iam.gserviceaccount.com <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Commit-Queue: chromium-autoroll@skia-public.iam.gserviceaccount.com <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Cr-Commit-Position: refs/heads/main@{#1613035}

```

---

Files:

- M `DEPS`
- M `third_party/dawn`

---

Hash: [4f4a96155533595a2403c314c3ed0ed5846a394f](https://chromiumdash.appspot.com/commit/4f4a96155533595a2403c314c3ed0ed5846a394f)  

Date: Fri Apr 10 19:26:28 2026


---

### lo...@google.com (2026-04-10)

I also agree with @ky...@google.com that I don't think this UAF is reachable unless the explicit flag `--enable-dawn-features=vulkan_force_static_samplers_for_external_textures` is passed atm, so maybe this is security impact none.

### sp...@google.com (2026-04-22)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $11000.00 for this report.

Rationale for this decision:
Baseline with bisect. Memory corruption in a non-sandboxed process


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-05-20)

Requesting merge to M148 because latest trunk commit is in 149.

Security Merge Request:

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

### ch...@google.com (2026-05-20)

**M148** merge request created. **Please update [crbug/514925022](https://crbug.com/514925022) to have this merge reviewed.**

### dx...@google.com (2026-05-23)

Project: dawn  

Branch:  chromium/7778  

Author:  Lokbondo Kung [lokokung@google.com](mailto:lokokung@google.com)  

Link:    <https://dawn-review.googlesource.com/310635>

[M148] [native][vulkan] Wrap BindGroupLayout cache with a mutex.

---


Expand for full commit details
```
     
    Original change's description: 
    > [native][vulkan] Wrap BindGroupLayout cache with a mutex. 
    > 
    > - Because we dynamically create BGLs when initializing pipelines, 
    >   and because pipelines may be created asynchronously, we need to 
    >   make sure that access to the cache map doesn't mangle the data. 
    > 
    > Bug: 500609038 
    > Change-Id: I6ffc093773c1c8308bbc95f62da1f202622908db 
    > Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/301935 
    > Auto-Submit: Loko Kung <lokokung@google.com> 
    > Reviewed-by: Kyle Charbonneau <kylechar@google.com> 
    > Commit-Queue: Kyle Charbonneau <kylechar@google.com> 
     
    (cherry picked from commit cea524cfcd4c24764cc2a2dce19290ecb1031b27) 
     
    Bug: 514925022,500609038 
    Change-Id: I6ffc093773c1c8308bbc95f62da1f202622908db 
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/310635 
    Auto-Submit: Chrome Cherry Picker <chrome-cherry-picker@chops-service-accounts.iam.gserviceaccount.com> 
    Reviewed-by: Kai Ninomiya <kainino@chromium.org> 
    Commit-Queue: Kai Ninomiya <kainino@chromium.org> 
    Reviewed-by: Ken Russell <kbr@google.com>

```

---

Files:

- M `src/dawn/native/vulkan/BindGroupLayoutVk.cpp`
- M `src/dawn/native/vulkan/BindGroupLayoutVk.h`

---

Hash: 39662e337c4f9271543cb315a98cc8a7a1b617eb  

Date: Sat May 23 02:24:22 2026


---

### pe...@google.com (2026-05-23)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### qk...@google.com (2026-05-26)

Labeled LTS-NotApplicable-144 because M144 didn't have the suspected CL[1].

[1] <https://dawn-review.git.corp.google.com/c/dawn/+/298996>

### ch...@google.com (2026-07-18)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/500609038)*
