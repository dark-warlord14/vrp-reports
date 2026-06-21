# OOB Write in dawn::SlabAllocatorImpl

| Field | Value |
|-------|-------|
| **Issue ID** | [489482634](https://issues.chromium.org/issues/489482634) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Dawn |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | he...@gmail.com |
| **Assignee** | cw...@google.com |
| **Created** | 2026-03-04 |
| **Bounty** | $16,000.00 |

## Description

### Summary

On Metal, [`dawn::native::metal::BindGroupLayout`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/dawn/src/dawn/native/metal/BindGroupLayoutMTL.mm;l=47) constructs a fixed-size 4KiB slab allocator for `BindGroup` objects via `MakeFrontendBindGroupAllocator<BindGroup>(4096)`. When a WebGPU page creates a bind group layout with enough bindings that the computed `BindGroup` object size exceeds 4096 bytes, [`dawn::SlabAllocator`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/dawn/src/dawn/common/SlabAllocator.h;l=191) computes `blocksPerSlab = totalObjectBytes / objectSize` as zero and `SlabAllocatorImpl` proceeds with `mBlocksPerSlab == 0`, leading to an OOB heap write during allocation in GPU process.

### Details

The Metal backend creates a frontend bind group allocator with a constant byte budget (4KiB) that is independent of the bind group layout’s binding count. In [`BindGroupLayout::BindGroupLayout`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/dawn/src/dawn/native/metal/BindGroupLayoutMTL.mm;l=47), `mBindGroupAllocator` is constructed like:

```
BindGroupLayout::BindGroupLayout(DeviceBase* device,
                                 const UnpackedPtr<BindGroupLayoutDescriptor>& descriptor)
    : BindGroupLayoutInternalBase(device, descriptor),
      mBindGroupAllocator(MakeFrontendBindGroupAllocator<BindGroup>(4096)) {

```

[`BindGroupLayoutInternalBase::MakeFrontendBindGroupAllocator`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/dawn/src/dawn/native/BindGroupLayoutInternal.h;l=208) derives the per `BindGroup` object size from the layout’s binding counts (variable-sized tail storage) and passes that into a `SlabAllocator`:

```
template <typename BindGroup>
SlabAllocator<BindGroup> MakeFrontendBindGroupAllocator(size_t size) {
    return SlabAllocator<BindGroup>(
        size,                                                                        // bytes
        Align(sizeof(BindGroup), GetBindingDataAlignment()) + GetBindingDataSize(),  // size
        std::max(alignof(BindGroup), GetBindingDataAlignment())  // alignment
    );
}

```

The binding-data tail size grows with both the number of buffer bindings and the total binding count (object pointers). [`BindGroupLayoutInternalBase::GetBindingDataSize`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/dawn/src/dawn/native/BindGroupLayoutInternal.cpp;l=966) is linear in `bufferCount` and `bindingCount`:

```
const size_t bufferCount = size_t(GetBindingTypeEnd(BindingTypeOrder_RegularBuffer));
const size_t bindingCount = size_t(mBindingInfo.size());

size_t objectPointerStart = bufferCount * sizeof(BufferBindingData);
size_t bufferSizeArrayStart =
    Align(objectPointerStart + bindingCount * sizeof(Ref<ObjectBase>), sizeof(uint64_t));
return bufferSizeArrayStart + mUnverifiedBufferCount * sizeof(uint64_t);

```

This makes the issue reachable from WebGPU even on devices with low per-shader-stage resource limits: `BindGroupLayoutEntry.visibility` can be set to `0` (no shader stage), which avoids per-stage counting while still contributing to `mBindingInfo.size()` and the computed bind-group object size.

Once the computed `objectSize` exceeds the fixed 4096-byte slab budget, [`dawn::SlabAllocator`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/dawn/src/dawn/common/SlabAllocator.h;l=191) computes `blocksPerSlab` with integer division and passes it to `SlabAllocatorImpl`:

```
SlabAllocator(size_t totalObjectBytes,
              uint32_t objectSize = u32_sizeof<T>,
              uint32_t objectAlignment = u32_alignof<T>)
    : SlabAllocatorImpl(totalObjectBytes / objectSize, objectSize, objectAlignment) {}

```

With `totalObjectBytes / objectSize == 0`, [`SlabAllocatorImpl::GetNewSlab`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/dawn/src/dawn/common/SlabAllocator.cpp;l=250) allocates only `mTotalAllocationSize = mSlabBlocksOffset + mBlocksPerSlab * mBlockStride` bytes (i.e., no space for any blocks) and still derives a free-list node pointer from `dataStart`, then installs it into the slab:

```
char* alignedPtr = static_cast<char*>(AlignedAlloc(mTotalAllocationSize, mAllocationAlignment));
char* dataStart = alignedPtr + mSlabBlocksOffset;

IndexLinkNode* node = NodeFromObject(dataStart);
for (uint32_t i = 0; i < mBlocksPerSlab; ++i) {
    new (OffsetFrom(node, i)) IndexLinkNode(i, i + 1);
}

IndexLinkNode* lastNode = OffsetFrom(node, mBlocksPerSlab - 1);
lastNode->nextIndex = kInvalidIndex;

mAvailableSlabs.Prepend(new (alignedPtr) Slab(alignedPtr, node));

```

On the subsequent allocation, [`SlabAllocatorImpl::Allocate`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/dawn/src/dawn/common/SlabAllocator.cpp;l=212) pops the head of the free list and dereferences the out-of-bounds `IndexLinkNode` in the GPU process.

### Bisection

This issue is introduced by the commit `https://dawn-review.googlesource.com/c/dawn/+/15862`. The original storage size uses `sizeof(T)` as the minimum size/unit, while this commits changes to the `totalObjectBytes / objectSize`, making it possible to 0 due to the division truncation, and further the heap OOB.

### Reproduction

Download the chrome from `https://storage.googleapis.com/chromium-browser-asan/mac-release-arm64/asan-mac-release-1592006.zip`.

I can also reproduce it on the ToT arm Mac asan build with the commit 94452bdd15ffe772fde8b066e4fc017a6bc0b28d.

Run the following on the arm Mac.

```
./Chromium.app/Contents/MacOS/Chromium --enable-unsafe-webgpu --disable-in-process-stack-traces --enable-experimental-web-platform-features poc.html

```

You would observe the OOB shown in the `asan.txt`.

### Suggested Fix

In [`dawn::SlabAllocator`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/dawn/src/dawn/common/SlabAllocator.h;l=191), clamp `totalObjectBytes / objectSize` to at least 1 (and to at most `std::numeric_limits<Index>::max()`), so `mTotalAllocationSize` always includes space for at least one block.

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 25.7 KB)
- [poc.html](attachments/poc.html) (text/html, 832 B)

## Timeline

### he...@gmail.com (2026-03-06)

deleted

### cl...@appspot.gserviceaccount.com (2026-03-07)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5533671163363328.

### me...@google.com (2026-03-07)

Reproed locally on stable.

cwallez@: PTAL?

### 24...@project.gserviceaccount.com (2026-03-07)

Detailed Report: https://clusterfuzz.com/testcase?key=5533671163363328

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-buffer-overflow READ 2
Crash Address: 0x7c2a154a289a
Crash State:
  dawn::SlabAllocatorImpl::Allocate
  dawn::native::vulkan::BindGroupLayout::AllocateBindGroup
  dawn::native::vulkan::BindGroup::Create
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1577010:1577013

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5533671163363328

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary.

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


A recommended severity was added to this bug. Please change the severity if it is inaccurate.

### dx...@google.com (2026-03-12)

Project: dawn  

Branch:  main  

Author:  Corentin Wallez [cwallez@chromium.org](mailto:cwallez@chromium.org)  

Link:    <https://dawn-review.googlesource.com/295955>

[dawn] Fix SlabAllocator of objects larger than totalObjectBytes

---


Expand for full commit details
```
     
    It would previously compute that it can only fit 0 objects and cause a 
    bunch of failures. 
     
     - Fix SlabAllocator to always have space to allocate at least one 
       object. 
     - Add a SlabAllocatorTest for that case. 
     - Add an end2end test for bindgroup with maxBindingsPerGroup. 
     - Fix incorrect assumption in BindGroup.cpp that the bindingsSet could 
       be maxBindingsPerPipelineLayout. 
     - Fix the same assumption in an ASSERT in BindGroupLayout.cpp 
     - Fix a similar problem to SlabAllocator in 
       vulkan::DescriptorSetAllocator. 
     - Make D3D12 skip over visibility `None` bind group entries to avoid 
       running against assumption done in that backend. 
     
    Bug: 491082532, 489482634 
    Change-Id: I66b1567be051af141b8c48e99388d48617171978 
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/295955 
    Commit-Queue: Corentin Wallez <cwallez@chromium.org> 
    Reviewed-by: Loko Kung <lokokung@google.com> 
    Reviewed-by: Antonio Maiorano <amaiorano@google.com>

```

---

Files:

- M `src/dawn/common/SlabAllocator.cpp`
- M `src/dawn/common/SlabAllocator.h`
- M `src/dawn/native/BindGroup.cpp`
- M `src/dawn/native/BindGroupLayoutInternal.cpp`
- M `src/dawn/native/Limits.cpp`
- M `src/dawn/native/d3d12/BindGroupD3D12.cpp`
- M `src/dawn/native/d3d12/BindGroupLayoutD3D12.cpp`
- M `src/dawn/native/vulkan/DescriptorSetAllocator.cpp`
- M `src/dawn/tests/end2end/BindGroupTests.cpp`
- M `src/dawn/tests/unittests/SlabAllocatorTests.cpp`

---

Hash: c4a63a567b25170a7c373a0a833b711bea746f56  

Date: Thu Mar 12 11:03:11 2026


---

### cw...@chromium.org (2026-03-12)

Asking for a merge in Beta but also Stable because this is an OOB write.

### ch...@google.com (2026-03-12)

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

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

### ch...@google.com (2026-03-12)

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

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

### dx...@google.com (2026-03-12)

Project: chromium/src  

Branch:  main  

Author:  chromium-autoroll [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com)  

Link:    <https://chromium-review.googlesource.com/7659377>

Roll Dawn from 5dd4bab0d750 to c4a63a567b25 (6 revisions)

---


Expand for full commit details
```
     
    https://dawn.googlesource.com/dawn.git/+log/5dd4bab0d750..c4a63a567b25 
     
    2026-03-12 cwallez@chromium.org [dawn] Fix SlabAllocator of objects larger than totalObjectBytes 
    2026-03-12 beaufort.francois@gmail.com [dawn.json] Remove deprecated texture binding view dimension descriptor 
    2026-03-12 jiawei.shao@intel.com Remove mapping usages when creating buffer from shared buffer memory with default descriptor 
    2026-03-12 arthursonzogni@chromium.org Enable MiraclePtr clang plugin. 
    2026-03-12 arthursonzogni@chromium.org Refresh MiraclePtr (mac specific code) 
    2026-03-12 dawn-autoroll@skia-public.iam.gserviceaccount.com Roll Chromium from 8d43dd57d980 to 6be1399c83ba (703 revisions) 
     
    If this roll has caused a breakage, revert this CL and stop the roller 
    using the controls here: 
    https://autoroll.skia.org/r/dawn-chromium-autoroll 
    Please CC cwallez@google.com,gman@google.com on the revert to ensure that a human 
    is aware of the problem. 
     
    To file a bug in Dawn: https://bugs.chromium.org/p/dawn/issues/entry 
    To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry 
     
    To report a problem with the AutoRoller itself, please file a bug: 
    https://issues.skia.org/issues/new?component=1389291&template=1850622 
     
    Documentation for the AutoRoller is here: 
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md 
     
    Cq-Include-Trybots: luci.chromium.try:dawn-android-arm-deps-rel;luci.chromium.try:dawn-android-arm64-deps-rel;luci.chromium.try:dawn-linux-x64-deps-rel;luci.chromium.try:dawn-mac-x64-deps-rel;luci.chromium.try:dawn-mac-arm64-deps-rel;luci.chromium.try:dawn-win10-x64-deps-rel;luci.chromium.try:dawn-win10-x86-deps-rel;luci.chromium.try:dawn-win11-arm64-deps-rel;luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:gpu-fyi-cq-mac-arm64;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:gpu-fyi-cq-android-arm64 
    Bug: chromium:386255678,chromium:479233871,chromium:479743213,chromium:489482634,chromium:491082532 
    Tbr: gman@google.com 
    Change-Id: Idf029de45a53ecf4a8827dc77383164258fa4e7c 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7659377 
    Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Cr-Commit-Position: refs/heads/main@{#1598434}

```

---

Files:

- M `DEPS`
- M `third_party/dawn`

---

Hash: [cee8bfa2119ff043d70c4ccfa4d7bd9f75af1e80](https://chromiumdash.appspot.com/commit/cee8bfa2119ff043d70c4ccfa4d7bd9f75af1e80)  

Date: Thu Mar 12 15:03:30 2026


---

### dx...@google.com (2026-03-13)

Project: dawn  

Branch:  main  

Author:  Corentin Wallez [cwallez@chromium.org](mailto:cwallez@chromium.org)  

Link:    <https://dawn-review.googlesource.com/297035>

[dawn][native] Check for duplicate bindings after checking they exist.

---


Expand for full commit details
```
     
    Otherwise we could go past the bitset<>'s size, triggering an ASSERT or 
    libc++ hardening exception. 
     
    Bug: 492390076, 489482634 
    Change-Id: I0d824013ff223b7375c8b319864d44208cf25873 
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/297035 
    Reviewed-by: Antonio Maiorano <amaiorano@google.com> 
    Commit-Queue: Antonio Maiorano <amaiorano@google.com> 
    Auto-Submit: Corentin Wallez <cwallez@chromium.org>

```

---

Files:

- M `src/dawn/native/BindGroup.cpp`
- M `src/dawn/tests/unittests/validation/BindGroupValidationTests.cpp`

---

Hash: ea757bf42d98bba037f098865d394ce219842a04  

Date: Fri Mar 13 14:33:52 2026


---

### 24...@project.gserviceaccount.com (2026-03-13)

ClusterFuzz testcase 5533671163363328 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1598432:1598437

If this is incorrect, please add the hotlistid:5433040 and re-open the issue.

### dx...@google.com (2026-03-13)

Project: chromium/src  

Branch:  main  

Author:  chromium-autoroll [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com)  

Link:    <https://chromium-review.googlesource.com/7662297>

Roll Dawn from f5d3ecd87ced to 2319a695c238 (3 revisions)

---


Expand for full commit details
```
     
    https://dawn.googlesource.com/dawn.git/+log/f5d3ecd87ced..2319a695c238 
     
    2026-03-13 jrprice@google.com Revert "[tint] Add IR validation for @color on f16" 
    2026-03-13 cwallez@chromium.org [dawn][native] Check for duplicate bindings after checking they exist. 
    2026-03-13 dawn-autoroll@skia-public.iam.gserviceaccount.com Roll vulkan-deps from 3ad5a6d56b25 to ff6eb204a9bc (10 revisions) 
     
    If this roll has caused a breakage, revert this CL and stop the roller 
    using the controls here: 
    https://autoroll.skia.org/r/dawn-chromium-autoroll 
    Please CC cwallez@google.com,gman@google.com on the revert to ensure that a human 
    is aware of the problem. 
     
    To file a bug in Dawn: https://bugs.chromium.org/p/dawn/issues/entry 
    To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry 
     
    To report a problem with the AutoRoller itself, please file a bug: 
    https://issues.skia.org/issues/new?component=1389291&template=1850622 
     
    Documentation for the AutoRoller is here: 
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md 
     
    Cq-Include-Trybots: luci.chromium.try:dawn-android-arm-deps-rel;luci.chromium.try:dawn-android-arm64-deps-rel;luci.chromium.try:dawn-linux-x64-deps-rel;luci.chromium.try:dawn-mac-x64-deps-rel;luci.chromium.try:dawn-mac-arm64-deps-rel;luci.chromium.try:dawn-win10-x64-deps-rel;luci.chromium.try:dawn-win10-x86-deps-rel;luci.chromium.try:dawn-win11-arm64-deps-rel;luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:gpu-fyi-cq-mac-arm64;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:gpu-fyi-cq-android-arm64 
    Bug: chromium:489482634,chromium:492390076 
    Tbr: gman@google.com 
    Change-Id: I402b7ee1fbb5a86193d4d26e654a40e6ee9d8a72 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7662297 
    Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Cr-Commit-Position: refs/heads/main@{#1599135}

```

---

Files:

- M `DEPS`
- M `third_party/dawn`

---

Hash: [a1cc6e0996921de486abd6bac8a03cd3b9ec2809](https://chromiumdash.appspot.com/commit/a1cc6e0996921de486abd6bac8a03cd3b9ec2809)  

Date: Fri Mar 13 17:00:14 2026


---

### cw...@chromium.org (2026-03-16)

Re both #8 and #9

1. It is an OOB write potentially, so at least a Medium or High severity issue.
2. <https://dawn-review.googlesource.com/295955> and follow-up bugfix <https://dawn-review.googlesource.com/297035>
3. Yes
4. No
5. N/A
6. No

### dr...@chromium.org (2026-03-18)

No crashes in Canary. Approved to merge both CLs to M146 and M147.

### go...@google.com (2026-03-19)

Please merge your change to M147 by 2:00 PM PT today so we can take it in for tomorrow's M147 beta release. Thank you.

### ds...@chromium.org (2026-03-19)

I've created a CL which cherry picks the two CLs and sent it to cwallez for review (<https://dawn-review.googlesource.com/c/dawn/+/298317>)

### dx...@google.com (2026-03-19)

Project: dawn  

Branch:  chromium/7727  

Author:  dan sinclair [dsinclair@chromium.org](mailto:dsinclair@chromium.org)  

Link:    <https://dawn-review.googlesource.com/298317>

[dawn][native] Check for duplicate bindings after checking they exist.

---


Expand for full commit details
```
     
    Otherwise we could go past the bitset<>'s size, triggering an ASSERT or 
    libc++ hardening exception. 
     
    Bug: 492390076, 489482634 
    Change-Id: I0d824013ff223b7375c8b319864d44208cf25873 
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/297035 
    Reviewed-by: Antonio Maiorano <amaiorano@google.com> 
    Commit-Queue: Antonio Maiorano <amaiorano@google.com> 
    Auto-Submit: Corentin Wallez <cwallez@chromium.org> 
     
     
    [dawn] Fix SlabAllocator of objects larger than totalObjectBytes 
     
    It would previously compute that it can only fit 0 objects and cause a 
    bunch of failures. 
     
     - Fix SlabAllocator to always have space to allocate at least one 
       object. 
     - Add a SlabAllocatorTest for that case. 
     - Add an end2end test for bindgroup with maxBindingsPerGroup. 
     - Fix incorrect assumption in BindGroup.cpp that the bindingsSet could 
       be maxBindingsPerPipelineLayout. 
     - Fix the same assumption in an ASSERT in BindGroupLayout.cpp 
     - Fix a similar problem to SlabAllocator in 
       vulkan::DescriptorSetAllocator. 
     - Make D3D12 skip over visibility `None` bind group entries to avoid 
       running against assumption done in that backend. 
     
    Bug: 491082532, 489482634 
    Change-Id: I66b1567be051af141b8c48e99388d48617171978 
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/295955 
    Commit-Queue: Corentin Wallez <cwallez@chromium.org> 
    Reviewed-by: Loko Kung <lokokung@google.com> 
    Reviewed-by: Antonio Maiorano <amaiorano@google.com> 
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/298317 
    Commit-Queue: Loko Kung <lokokung@google.com> 
    Auto-Submit: dan sinclair <dsinclair@chromium.org>

```

---

Files:

- M `src/dawn/common/SlabAllocator.cpp`
- M `src/dawn/common/SlabAllocator.h`
- M `src/dawn/native/BindGroup.cpp`
- M `src/dawn/native/BindGroupLayoutInternal.cpp`
- M `src/dawn/native/Limits.cpp`
- M `src/dawn/native/d3d12/BindGroupD3D12.cpp`
- M `src/dawn/native/d3d12/BindGroupLayoutD3D12.cpp`
- M `src/dawn/native/vulkan/DescriptorSetAllocator.cpp`
- M `src/dawn/tests/end2end/BindGroupTests.cpp`
- M `src/dawn/tests/unittests/SlabAllocatorTests.cpp`
- M `src/dawn/tests/unittests/validation/BindGroupValidationTests.cpp`

---

Hash: 6ba7e1dbf3ed6b971e6bf4960376eabd7f871be5  

Date: Thu Mar 19 20:43:48 2026


---

### dr...@chromium.org (2026-03-23)

dsinclair@ - I only see a merge to M147 here. Is there a merge to M146 coming too?

### ds...@chromium.org (2026-03-23)

Sorry, I only saw the message in #16 saying to merge to M147. Missed the earlier one for M146. I'll put up a merge for 146 now. Sorry about that.

### ds...@chromium.org (2026-03-23)

Merge is up for review, bots are running. <https://dawn-review.git.corp.google.com/c/dawn/+/298975>

### dx...@google.com (2026-03-23)

Project: dawn  

Branch:  chromium/7680  

Author:  dan sinclair [dsinclair@chromium.org](mailto:dsinclair@chromium.org)  

Link:    <https://dawn-review.googlesource.com/298975>

[dawn][native] Check for duplicate bindings after checking they exist.

---


Expand for full commit details
```
     
    Otherwise we could go past the bitset<>'s size, triggering an ASSERT or 
    libc++ hardening exception. 
     
    Bug: 492390076, 489482634 
    Change-Id: I0d824013ff223b7375c8b319864d44208cf25873 
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/297035 
    Reviewed-by: Antonio Maiorano <amaiorano@google.com> 
    Commit-Queue: Antonio Maiorano <amaiorano@google.com> 
    Auto-Submit: Corentin Wallez <cwallez@chromium.org> 
     
     
    [dawn] Fix SlabAllocator of objects larger than totalObjectBytes 
     
    It would previously compute that it can only fit 0 objects and cause a 
    bunch of failures. 
     
     - Fix SlabAllocator to always have space to allocate at least one 
       object. 
     - Add a SlabAllocatorTest for that case. 
     - Add an end2end test for bindgroup with maxBindingsPerGroup. 
     - Fix incorrect assumption in BindGroup.cpp that the bindingsSet could 
       be maxBindingsPerPipelineLayout. 
     - Fix the same assumption in an ASSERT in BindGroupLayout.cpp 
     - Fix a similar problem to SlabAllocator in 
       vulkan::DescriptorSetAllocator. 
     - Make D3D12 skip over visibility `None` bind group entries to avoid 
       running against assumption done in that backend. 
     
    Bug: 491082532, 489482634 
    Change-Id: I66b1567be051af141b8c48e99388d48617171978 
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/295955 
    Commit-Queue: Corentin Wallez <cwallez@chromium.org> 
    Reviewed-by: Loko Kung <lokokung@google.com> 
    Reviewed-by: Antonio Maiorano <amaiorano@google.com> 
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/298975 
    Commit-Queue: dan sinclair <dsinclair@chromium.org> 
    Reviewed-by: Corentin Wallez <cwallez@chromium.org> 
    Auto-Submit: dan sinclair <dsinclair@chromium.org>

```

---

Files:

- M `src/dawn/common/SlabAllocator.cpp`
- M `src/dawn/common/SlabAllocator.h`
- M `src/dawn/native/BindGroup.cpp`
- M `src/dawn/native/BindGroupLayoutInternal.cpp`
- M `src/dawn/native/Limits.cpp`
- M `src/dawn/native/d3d12/BindGroupD3D12.cpp`
- M `src/dawn/native/d3d12/BindGroupLayoutD3D12.cpp`
- M `src/dawn/native/vulkan/DescriptorSetAllocator.cpp`
- M `src/dawn/tests/end2end/BindGroupTests.cpp`
- M `src/dawn/tests/unittests/SlabAllocatorTests.cpp`
- M `src/dawn/tests/unittests/validation/BindGroupValidationTests.cpp`

---

Hash: fcaf11f6e545d20940b00268da26ccac2344e151  

Date: Mon Mar 23 21:15:43 2026


---

### sp...@google.com (2026-04-10)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $16000.00 for this report.

Rationale for this decision:
High quality with bisect. Renderer RCE / memory corruption in a sandboxed process


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-06-20)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/489482634)*
