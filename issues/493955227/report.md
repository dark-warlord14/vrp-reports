# Reentrant vector mutation during FrameSink invalidation causes heap use-after-free in Viz process

| Field | Value |
|-------|-------|
| **Issue ID** | [493955227](https://issues.chromium.org/issues/493955227) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Services>Viz |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | je...@gmail.com |
| **Assignee** | ky...@chromium.org |
| **Created** | 2026-03-19 |
| **Bounty** | $16,000.00 |

## Description

# Reentrant vector mutation during FrameSink invalidation causes heap use-after-free in Viz process

## Summary

A heap use-after-free vulnerability exists in the Viz compositor process on all desktop platforms (Linux, macOS, Windows, ChromeOS). `SurfaceManager::InvalidateFrameSinkId()` iterates a vector of `SurfaceAllocationGroup` pointers using a range-for loop. During iteration, the synchronous callback chain through `WillNotRegisterNewSurfaces` can activate a pending surface whose `referenced_surfaces` metadata triggers creation of new allocation groups via `push_back` into the same vector. When the vector reallocates its internal buffer, the range-for loop's captured iterators become dangling, and subsequent iterations read freed heap memory. A compromised renderer can construct the necessary state entirely through the `EmbeddedFrameSinkProvider` and `CompositorFrameSink` Mojo interfaces and trigger the invalidation by closing a connection. The crash occurs on the VizCompositorThread, which runs outside the renderer sandbox. ASAN confirms the region is not protected by MiraclePtr.

## Bisect

Introducing Commit: `9ef8b6ebe397e7a492210006d949423ba27f5acd`

- Date: 2019-04-05
- Author: Saman Sami <[samans@chromium.org](mailto:samans@chromium.org)>
- Review: <https://chromium-review.googlesource.com/c/chromium/src/+/1539860>

## Root Cause

`SurfaceManager::InvalidateFrameSinkId` looks up all `SurfaceAllocationGroup` entries associated with a given `FrameSinkId` and notifies each that no further surfaces will be registered:

```
// components/viz/service/surfaces/surface_manager.cc:166-174
void SurfaceManager::InvalidateFrameSinkId(const FrameSinkId& frame_sink_id) {
  auto it = frame_sink_id_to_allocation_groups_.find(frame_sink_id);
  if (it != frame_sink_id_to_allocation_groups_.end()) {
    for (SurfaceAllocationGroup* group : it->second) {
      group->WillNotRegisterNewSurfaces();
    }
  }
  GarbageCollectSurfaces();
}

```

The range-for loop captures `begin()` and `end()` iterators of `it->second`, a `std::vector<raw_ptr<SurfaceAllocationGroup, VectorExperimental>>`. These iterators point into the vector's internal heap buffer.

`WillNotRegisterNewSurfaces` moves out all blocked embedders and synchronously resolves their activation dependencies:

```
// components/viz/service/surfaces/surface_allocation_group.cc:176-182
void SurfaceAllocationGroup::WillNotRegisterNewSurfaces() {
  base::flat_map<Surface*, SurfaceId> embedders = std::move(blocked_embedders_);
  blocked_embedders_.clear();
  for (const auto& entry : embedders) {
    entry.first->OnActivationDependencyResolved(entry.second, this);
  }
}

```

If the resolved dependency was the last outstanding one for a surface, `OnActivationDependencyResolved` calls `ActivatePendingFrame`, which calls `ActivateFrame`, which calls `RecomputeActiveReferencedSurfaces`. That function iterates the activated frame's `referenced_surfaces` metadata and calls `GetOrCreateAllocationGroupForSurfaceId` for each entry:

```
// components/viz/service/surfaces/surface_manager.cc:656-661
if (!allocation_group) {
    allocation_group = std::make_unique<SurfaceAllocationGroup>(
        this, surface_id.frame_sink_id(),
        surface_id.local_surface_id().embed_token());
    frame_sink_id_to_allocation_groups_[surface_id.frame_sink_id()].push_back(
        allocation_group.get());
}

```

When `surface_id.frame_sink_id()` matches the FrameSinkId currently being invalidated, `push_back` appends to the same vector that `InvalidateFrameSinkId` is iterating. If the vector's capacity is exceeded, it reallocates its internal buffer, freeing the old one. The range-for loop then advances its stale iterator into the freed buffer, reading a dangling `SurfaceAllocationGroup*` pointer.

A compromised renderer can construct this state through normal Mojo interfaces. It creates a target FrameSink X and three attacker FrameSinks via `blink.mojom.EmbeddedFrameSinkProvider.CreateSimpleCompositorFrameSink`. Each attacker submits a `CompositorFrame` with one `activation_dependency` referencing X (using distinct embed tokens E1, E2, E3), which creates three allocation groups in the vector for X. The first attacker's frame additionally carries 200 `referenced_surfaces` entries, each referencing X with a unique embed token. These entries are inert while the frame is pending. When the renderer closes X's `EmbeddedFrameSinkClient` connection, the browser forwards an `InvalidateFrameSinkId(X)` call to the Viz process. The loop processes E1's group first, resolving the first attacker surface's sole dependency, activating its pending frame, and processing 200 `referenced_surfaces` entries. Each entry calls `GetOrCreateAllocationGroupForSurfaceId`, which `push_back`s a new group into the vector for X. The vector grows from 3 elements to over 200, reallocating its buffer. The next loop iteration dereferences the stale iterator into the freed 3-element buffer.

No mitigations block this path. There are no `CHECK` guards on the iteration, no reentrancy protection, and no copy of the vector before iteration. The `raw_ptr<VectorExperimental>` wrapper on the vector elements protects the pointed-to `SurfaceAllocationGroup` objects but does not protect the vector's own internal buffer from iterator invalidation. The mojom deserialization in `compositor_frame_metadata_mojom_traits.cc` imposes no restrictions on the number or content of `referenced_surfaces` or `activation_dependencies`. ASAN confirms "MiraclePtr Status: NOT PROTECTED" for this access.

## Reproduce

Tested at commit `7c89d33808e551aed6122c1f324864784011c158`.

Apply the attached `patch.diff` to the renderer source, then build:

```
git apply issue_framesink_invalidation_uaf/patch.diff
autoninja -C ~/chromium/src/out/asan-release chrome

```

Launch and open `poc.html`:

```
ASAN_OPTIONS=detect_odr_violation=0 xvfb-run -a \
  ~/chromium/src/out/asan-release/chrome \
  --user-data-dir=/tmp/poc-$(date +%s) \
  issue_framesink_invalidation_uaf/poc.html

```

The GPU/Viz process crashes with a heap-use-after-free within approximately one second. The crash occurs on the VizCompositorThread inside `SurfaceManager::InvalidateFrameSinkId`.

```
==2458553==ERROR: AddressSanitizer: heap-use-after-free on address 0x7b2e9da4f4c8 at pc 0x7efea76d1825 bp 0x7afe82a9eb30 sp 0x7afe82a9eb28
READ of size 8 at 0x7b2e9da4f4c8 thread T15 (VizCompositorTh)
    #0 0x7efea76d1824 in viz::SurfaceManager::InvalidateFrameSinkId(viz::FrameSinkId const&) base/allocator/partition_allocator/src/partition_alloc/pointers/raw_ptr.h:1018:47
    #1 0x7efea75774b5 in viz::FrameSinkManagerImpl::InvalidateFrameSinkId(viz::FrameSinkId const&, base::OnceCallback<void ()>) components/viz/service/frame_sinks/frame_sink_manager_impl.cc:223:20
    #2 0x7efea77696ae in viz::mojom::FrameSinkManagerStubDispatch::AcceptWithResponder(viz::mojom::FrameSinkManager*, mojo::Message*, std::__Cr::unique_ptr<mojo::MessageReceiverWithStatus, std::__Cr::default_delete<mojo::MessageReceiverWithStatus>>) gen/services/viz/privileged/mojom/compositing/frame_sink_manager.mojom.cc:3271:13

0x7b2e9da4f4c8 is located 8 bytes inside of 32-byte region [0x7b2e9da4f4c0,0x7b2e9da4f4e0)
freed by thread T15 (VizCompositorTh) here:
    #0 0x5596ce120b02 in operator delete(void*, unsigned long)
    #1 0x7efea76db70d in std::__Cr::vector<...>::__emplace_back_slow_path gen/third_party/libc++/src/include/__new/allocate.h:63:10
    #2 0x7efea76cfed8 in viz::SurfaceManager::GetOrCreateAllocationGroupForSurfaceId(viz::SurfaceId const&) gen/third_party/libc++/src/include/__vector/vector.h:1148:21
    #3 0x7efea76a888f in viz::Surface::RecomputeActiveReferencedSurfaces() components/viz/service/surfaces/surface.cc:634:27
    #4 0x7efea76ad04e in viz::Surface::ActivateFrame(viz::Surface::FrameData) components/viz/service/surfaces/surface.cc:697:3
    #5 0x7efea76a7df9 in viz::Surface::ActivatePendingFrame() components/viz/service/surfaces/surface.cc:520:3
    #6 0x7efea76af659 in viz::Surface::OnActivationDependencyResolved(viz::SurfaceId const&, viz::SurfaceAllocationGroup*) components/viz/service/surfaces/surface.cc:459:3
    #7 0x7efea76cb544 in viz::SurfaceAllocationGroup::WillNotRegisterNewSurfaces() components/viz/service/surfaces/surface_allocation_group.cc:180:18
    #8 0x7efea76d1781 in viz::SurfaceManager::InvalidateFrameSinkId(viz::FrameSinkId const&) components/viz/service/surfaces/surface_manager.cc:170:14

previously allocated by thread T15 (VizCompositorTh) here:
    #0 0x5596ce11fefd in operator new(unsigned long)
    #1 0x7efea76db5e4 in std::__Cr::vector<...>::__emplace_back_slow_path gen/third_party/libc++/src/include/__new/allocate.h:43:28
    #2 0x7efea76cfed8 in viz::SurfaceManager::GetOrCreateAllocationGroupForSurfaceId(viz::SurfaceId const&) gen/third_party/libc++/src/include/__vector/vector.h:1148:21
    #3 0x7efea76ac1d6 in viz::Surface::UpdateActivationDependencies(viz::CompositorFrame const&) components/viz/service/surfaces/surface.cc:802:27
    #4 0x7efea76aab53 in viz::Surface::CommitFrame(viz::Surface::FrameData) components/viz/service/surfaces/surface.cc:343:3
    #5 0x7efea76a9e4a in viz::Surface::QueueFrame(viz::CompositorFrame, unsigned int, base::ScopedClosureRunner) components/viz/service/surfaces/surface.cc:270:14
    #6 0x7efea7541176 in viz::CompositorFrameSinkSupport::MaybeSubmitCompositorFrame components/viz/service/frame_sinks/compositor_frame_sink_support.cc:1014:55

MiraclePtr Status: NOT PROTECTED
No raw_ptr<T> access to this region was detected prior to this crash.
This crash is still exploitable with MiraclePtr.

```

The complete ASAN log is in `asan.log`.

## Credit

Please use c6eed09fc8b174b0f3eebedcceb1e792 as the credit for this vulnerability. Thank you.

## Attachments

- [asan-mac.log](attachments/asan-mac.log) (text/plain, 26.5 KB)
- [asan.log](attachments/asan.log) (text/plain, 22.0 KB)
- [patch.diff](attachments/patch.diff) (text/x-diff, 5.5 KB)
- [poc.html](attachments/poc.html) (text/html, 500 B)
- [asan_3.txt](attachments/asan_3.txt) (text/plain, 21.3 KB)

## Timeline

### ts...@google.com (2026-03-19)

Reproduced on Chromium 146.0.7680.159 / Linux, ASAN trace attached.


### ts...@google.com (2026-03-19)

Kyle, do you think you could suggest an owner for this?  Thanks!

### ch...@google.com (2026-03-20)

Setting milestone because of s0/s1 severity.

### jo...@chromium.org (2026-03-20)

The current POC requires more than just a regular page, containing a chromium patch. Decreasing priority

### je...@gmail.com (2026-03-20)

Yes, as background, this vulnerability requires a compromised render, then triggers a UAF in the GPU process, which is a sandbox escape.

### ch...@google.com (2026-03-21)

Setting Priority to P1 to match Severity s1. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### dx...@google.com (2026-04-10)

Project: chromium/src  

Branch:  main  

Author:  kylechar [kylechar@chromium.org](mailto:kylechar@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7707244>

Guard against reentrant vector modification

---


Expand for full commit details
```
     
    Copy active surface group vector during before iterating as 
    WillNotRegisterNewSurfaces() can cause new surface groups to be added to 
    vector, invalidating existing iterators. 
     
    Fixed: 493955227 
    Change-Id: Ia58a539523d7b5d700cbfd232f4d8bab597d20d4 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7707244 
    Reviewed-by: Jonathan Ross <jonross@chromium.org> 
    Commit-Queue: Kyle Charbonneau <kylechar@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1612925}

```

---

Files:

- M `components/viz/service/surfaces/surface_manager.cc`
- M `components/viz/service/surfaces/surface_unittest.cc`

---

Hash: [2332137922bb5abd4ffe7ea8ae125c5f0b1d400b](https://chromiumdash.appspot.com/commit/2332137922bb5abd4ffe7ea8ae125c5f0b1d400b)  

Date: Fri Apr 10 16:33:51 2026


---

### ch...@google.com (2026-04-11)

Requesting merge to M146 because latest trunk commit (1612925) appears to be after M146 branch point (1582197).

Security Merge Request:

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Requesting merge to M147 because latest trunk commit (1612925) appears to be after M147 branch point (1596535).

Requesting merge to M148 because latest trunk commit (1612925) appears to be after M148 branch point (1610480).

### ch...@google.com (2026-04-11)

**M146** merge request created. **Please update [crbug/501627367](https://crbug.com/501627367) to have this merge reviewed.**

### ch...@google.com (2026-04-11)

**M147** merge request created. **Please update [crbug/501628362](https://crbug.com/501628362) to have this merge reviewed.**

### ch...@google.com (2026-04-11)

**M148** merge request created. **Please update [crbug/501627390](https://crbug.com/501627390) to have this merge reviewed.**

### dx...@google.com (2026-04-22)

Project: chromium/src  

Branch:  refs/branch-heads/7680  

Author:  kylechar [kylechar@chromium.org](mailto:kylechar@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7782791>

[M146] Guard against reentrant vector modification

---


Expand for full commit details
```
     
    Original change's description: 
    > Guard against reentrant vector modification 
    > 
    > Copy active surface group vector during before iterating as 
    > WillNotRegisterNewSurfaces() can cause new surface groups to be added to 
    > vector, invalidating existing iterators. 
    > 
    > Fixed: 493955227 
    > Change-Id: Ia58a539523d7b5d700cbfd232f4d8bab597d20d4 
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7707244 
    > Reviewed-by: Jonathan Ross <jonross@chromium.org> 
    > Commit-Queue: Kyle Charbonneau <kylechar@chromium.org> 
    > Cr-Commit-Position: refs/heads/main@{#1612925} 
     
    (cherry picked from commit 2332137922bb5abd4ffe7ea8ae125c5f0b1d400b) 
     
    Bug: 501627367,493955227 
    Change-Id: Ia58a539523d7b5d700cbfd232f4d8bab597d20d4 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7782791 
    Auto-Submit: chrome-cherry-picker@chops-service-accounts.iam.gserviceaccount.com <chrome-cherry-picker@chops-service-accounts.iam.gserviceaccount.com> 
    Bot-Commit: rubber-stamper@appspot.gserviceaccount.com <rubber-stamper@appspot.gserviceaccount.com> 
    Commit-Queue: rubber-stamper@appspot.gserviceaccount.com <rubber-stamper@appspot.gserviceaccount.com> 
    Cr-Commit-Position: refs/branch-heads/7680@{#3988} 
    Cr-Branched-From: 76b7d80e5cda23fe6537eed26d68c92e995c7f39-refs/heads/main@{#1582197}

```

---

Files:

- M `components/viz/service/surfaces/surface_manager.cc`
- M `components/viz/service/surfaces/surface_unittest.cc`

---

Hash: [8846d4ef0e730f0c712da3a334e0b50bc01895b1](https://chromiumdash.appspot.com/commit/8846d4ef0e730f0c712da3a334e0b50bc01895b1)  

Date: Wed Apr 22 02:02:19 2026


---

### dx...@google.com (2026-04-22)

Project: chromium/src  

Branch:  refs/branch-heads/7727  

Author:  kylechar [kylechar@chromium.org](mailto:kylechar@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7784451>

[M147] Guard against reentrant vector modification

---


Expand for full commit details
```
     
    Original change's description: 
    > Guard against reentrant vector modification 
    > 
    > Copy active surface group vector during before iterating as 
    > WillNotRegisterNewSurfaces() can cause new surface groups to be added to 
    > vector, invalidating existing iterators. 
    > 
    > Fixed: 493955227 
    > Change-Id: Ia58a539523d7b5d700cbfd232f4d8bab597d20d4 
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7707244 
    > Reviewed-by: Jonathan Ross <jonross@chromium.org> 
    > Commit-Queue: Kyle Charbonneau <kylechar@chromium.org> 
    > Cr-Commit-Position: refs/heads/main@{#1612925} 
     
    (cherry picked from commit 2332137922bb5abd4ffe7ea8ae125c5f0b1d400b) 
     
    Bug: 501628362,493955227 
    Change-Id: Ia58a539523d7b5d700cbfd232f4d8bab597d20d4 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7784451 
    Auto-Submit: chrome-cherry-picker@chops-service-accounts.iam.gserviceaccount.com <chrome-cherry-picker@chops-service-accounts.iam.gserviceaccount.com> 
    Commit-Queue: rubber-stamper@appspot.gserviceaccount.com <rubber-stamper@appspot.gserviceaccount.com> 
    Bot-Commit: rubber-stamper@appspot.gserviceaccount.com <rubber-stamper@appspot.gserviceaccount.com> 
    Cr-Commit-Position: refs/branch-heads/7727@{#3437} 
    Cr-Branched-From: ce01102937348db7b88c8a4257ee4b3ac702eb1a-refs/heads/main@{#1596535}

```

---

Files:

- M `components/viz/service/surfaces/surface_manager.cc`
- M `components/viz/service/surfaces/surface_unittest.cc`

---

Hash: [73527f1549dbb76a9652f7096fe07de32d1b8e25](https://chromiumdash.appspot.com/commit/73527f1549dbb76a9652f7096fe07de32d1b8e25)  

Date: Wed Apr 22 02:03:34 2026


---

### pe...@google.com (2026-04-22)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### dx...@google.com (2026-04-22)

Project: chromium/src  

Branch:  refs/branch-heads/7778  

Author:  kylechar [kylechar@chromium.org](mailto:kylechar@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7784453>

[M148] Guard against reentrant vector modification

---


Expand for full commit details
```
     
    Original change's description: 
    > Guard against reentrant vector modification 
    > 
    > Copy active surface group vector during before iterating as 
    > WillNotRegisterNewSurfaces() can cause new surface groups to be added to 
    > vector, invalidating existing iterators. 
    > 
    > Fixed: 493955227 
    > Change-Id: Ia58a539523d7b5d700cbfd232f4d8bab597d20d4 
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7707244 
    > Reviewed-by: Jonathan Ross <jonross@chromium.org> 
    > Commit-Queue: Kyle Charbonneau <kylechar@chromium.org> 
    > Cr-Commit-Position: refs/heads/main@{#1612925} 
     
    (cherry picked from commit 2332137922bb5abd4ffe7ea8ae125c5f0b1d400b) 
     
    Bug: 501627390,493955227 
    Change-Id: Ia58a539523d7b5d700cbfd232f4d8bab597d20d4 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7784453 
    Commit-Queue: rubber-stamper@appspot.gserviceaccount.com <rubber-stamper@appspot.gserviceaccount.com> 
    Auto-Submit: chrome-cherry-picker@chops-service-accounts.iam.gserviceaccount.com <chrome-cherry-picker@chops-service-accounts.iam.gserviceaccount.com> 
    Bot-Commit: rubber-stamper@appspot.gserviceaccount.com <rubber-stamper@appspot.gserviceaccount.com> 
    Cr-Commit-Position: refs/branch-heads/7778@{#1329} 
    Cr-Branched-From: 77f495ee216d4c3cc784d33658bad4778c0680ee-refs/heads/main@{#1610480}

```

---

Files:

- M `components/viz/service/surfaces/surface_manager.cc`
- M `components/viz/service/surfaces/surface_unittest.cc`

---

Hash: [560c1726c21b86575b1a6a6e7f92162873b1f919](https://chromiumdash.appspot.com/commit/560c1726c21b86575b1a6a6e7f92162873b1f919)  

Date: Wed Apr 22 02:30:39 2026


---

### sp...@google.com (2026-04-24)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $16000.00 for this report.

Rationale for this decision:
High quality with bisect. Memory corruption in a highly privileged process (e.g. GPU, network processes) 


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### pe...@google.com (2026-06-02)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2026-06-02)

1. https://chromium-review.git.corp.google.com/c/chromium/src/+/7882927/1..2
2. Low - There was a small conflict.
3. 146, 147, and 148
4. Yes, the bug has existed for a long years.

### dx...@google.com (2026-06-09)

Project: chromium/src  

Branch:  refs/branch-heads/7559  

Author:  kylechar [kylechar@chromium.org](mailto:kylechar@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7882927>

[M144-LTS] Guard against reentrant vector modification

---


Expand for full commit details
```
     
    Copy active surface group vector during before iterating as 
    WillNotRegisterNewSurfaces() can cause new surface groups to be added to 
    vector, invalidating existing iterators. 
     
    (cherry picked from commit 2332137922bb5abd4ffe7ea8ae125c5f0b1d400b) 
     
    Fixed: 493955227 
    Change-Id: Ia58a539523d7b5d700cbfd232f4d8bab597d20d4 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7707244 
    Reviewed-by: Jonathan Ross <jonross@chromium.org> 
    Commit-Queue: Kyle Charbonneau <kylechar@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1612925} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7882927 
    Reviewed-by: Mohamed Omar <mohamedaomar@google.com> 
    Commit-Queue: Gyuyoung Kim (xWF) <qkim@google.com> 
    Reviewed-by: Artem Sumaneev <asumaneev@google.com> 
    Owners-Override: Artem Sumaneev <asumaneev@google.com> 
    Reviewed-by: Kyle Charbonneau <kylechar@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7559@{#4976} 
    Cr-Branched-From: 223dfbac1c7542a06b422390d954afe5b560b607-refs/heads/main@{#1552494}

```

---

Files:

- M `components/viz/service/surfaces/surface_manager.cc`
- M `components/viz/service/surfaces/surface_unittest.cc`

---

Hash: [4b2db12fa71ed4aec1a75d6bea00ec1bf208d1a7](https://chromiumdash.appspot.com/commit/4b2db12fa71ed4aec1a75d6bea00ec1bf208d1a7)  

Date: Tue Jun 9 05:17:17 2026


---

### ch...@google.com (2026-07-18)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/493955227)*
