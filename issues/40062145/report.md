# stack use after return in gpu::raster::(anonymous namespace)::OnReadYUVImagePixelsDone

| Field | Value |
|-------|-------|
| **Issue ID** | [40062145](https://issues.chromium.org/issues/40062145) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU>Vulkan |
| **Platforms** | Linux |
| **Reporter** | em...@gmail.com |
| **Assignee** | va...@chromium.org |
| **Created** | 2022-12-09 |
| **Bounty** | $10,000.00 |

## Description

**Steps to reproduce the problem:**  

glxinfo -B  

name of display: :0  

display: :0 screen: 0  

direct rendering: Yes  

Memory info (GL\_NVX\_gpu\_memory\_info):  

Dedicated video memory: 8192 MB  

Total available memory: 8192 MB  

Currently available dedicated video memory: 7951 MB  

OpenGL vendor string: NVIDIA Corporation  

OpenGL renderer string: NVIDIA GeForce GTX 1070/PCIe/SSE2  

OpenGL core profile version string: 4.6.0 NVIDIA 525.60.11  

OpenGL core profile shading language version string: 4.60 NVIDIA  

OpenGL core profile context flags: (none)  

OpenGL core profile profile mask: core profile

OpenGL version string: 4.6.0 NVIDIA 525.60.11  

OpenGL shading language version string: 4.60 NVIDIA  

OpenGL context flags: (none)  

OpenGL profile mask: (none)

OpenGL ES profile version string: OpenGL ES 3.2 NVIDIA 525.60.11  

OpenGL ES profile shading language version string: OpenGL ES GLSL ES 3.20

repro steps:  

./chrome --enable-features=Vulkan --user-data-dir=/tmp/xx1 ./crash.html

In my test,it looks like the memory corruption is only reproducible on NVIDIA.

**Problem Description:**  

==1865475==ERROR: AddressSanitizer: stack-use-after-return on address 0x7f1333b87100 at pc 0x55de076cdc5c bp 0x7ffdb7cc5cd0 sp 0x7ffdb7cc5cc8  

READ of size 8 at 0x7f1333b87100 thread T0 (chrome)  

#0 0x55de076cdc5b in reset ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:278:28  

#1 0x55de076cdc5b in operator= ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:215:5  

#2 0x55de076cdc5b in gpu::raster::(anonymous namespace)::OnReadYUVImagePixelsDone(void\*, std::Cr::unique\_ptr<SkImage::AsyncReadResult const, std::Cr::default\_delete<SkImage::AsyncReadResult const>>) ./../../gpu/command\_buffer/service/raster\_decoder.cc:2493:25  

#3 0x55de0353ffc3 in operator() ./../../third\_party/skia/src/gpu/ganesh/SurfaceContext.cpp:926:13  

#4 0x55de0353ffc3 in skgpu::v1::SurfaceContext::asyncRescaleAndReadPixelsYUV420(GrDirectContext\*, SkYUVColorSpace, sk\_sp<SkColorSpace>, SkIRect const&, SkISize, SkImage::RescaleGamma, SkImage::RescaleMode, void (\*)(void\*, std::Cr::unique\_ptr<SkImage::AsyncReadResult const, std::Cr::default\_delete<SkImage::AsyncReadResult const>>), void\*)::$\_0::\_\_invoke(void\*) ./../../third\_party/skia/src/gpu/ganesh/SurfaceContext.cpp:919:27  

#5 0x55de039e2cc4 in ~RefCntedCallback ./../../third\_party/skia/src/gpu/RefCntedCallback.h:41:13  

#6 0x55de039e2cc4 in unref ./../../third\_party/skia/include/core/SkRefCnt.h:180:13  

#7 0x55de039e2cc4 in SkSafeUnref[skgpu::RefCntedCallback](javascript:void(0);) ./../../third\_party/skia/include/core/SkRefCnt.h:150:14  

#8 0x55de039e2cc4 in ~sk\_sp ./../../third\_party/skia/include/core/SkRefCnt.h:260:9  

#9 0x55de039e2cc4 in pop\_back\_n ./../../third\_party/skia/include/private/SkTArray.h:308:19  

#10 0x55de039e2cc4 in reset ./../../third\_party/skia/include/private/SkTArray.h:139:15  

#11 0x55de039e2cc4 in callFinishedProcs ./../../third\_party/skia/src/gpu/ganesh/vk/GrVkCommandBuffer.h:324:24  

#12 0x55de039e2cc4 in GrVkPrimaryCommandBuffer::onReleaseResources() ./../../third\_party/skia/src/gpu/ganesh/vk/GrVkCommandBuffer.cpp:678:11  

#13 0x55de039daac5 in GrVkCommandBuffer::releaseResources() ./../../third\_party/skia/src/gpu/ganesh/vk/GrVkCommandBuffer.cpp:69:11  

#14 0x55de039eb192 in GrVkCommandPool::releaseResources() ./../../third\_party/skia/src/gpu/ganesh/vk/GrVkCommandPool.cpp:104:28  

#15 0x55de039eb416 in GrVkCommandPool::freeGPUData() const ./../../third\_party/skia/src/gpu/ganesh/vk/GrVkCommandPool.cpp:114:19  

#16 0x55de03a20f80 in internal\_dispose ./../../third\_party/skia/src/gpu/ganesh/GrManagedResource.h:172:15  

#17 0x55de03a20f80 in unref ./../../third\_party/skia/src/gpu/ganesh/GrManagedResource.h:132:19  

#18 0x55de03a20f80 in GrVkResourceProvider::destroyResources() ./../../third\_party/skia/src/gpu/ganesh/vk/GrVkResourceProvider.cpp:511:15  

#19 0x55de039b4a1f in GrVkGpu::disconnect(GrGpu::DisconnectType) ./../../third\_party/skia/src/gpu/ganesh/vk/GrVkGpu.cpp:293:15  

#20 0x55de0346dea9 in GrDirectContext::abandonContext() ./../../third\_party/skia/src/gpu/ganesh/GrDirectContext.cpp:141:11  

#21 0x55de0346e0aa in GrDirectContext::abandoned() ./../../third\_party/skia/src/gpu/ganesh/GrDirectContext.cpp:157:15  

#22 0x55de0731df00 in gpu::ExternalVkImageSkiaImageRepresentation::BeginWriteAccess(int, SkSurfaceProps const&, gfx::Rect const&, std::Cr::vector<GrBackendSemaphore, std::Cr::allocator<GrBackendSemaphore>>\*, std::Cr::vector<GrBackendSemaphore, std::Cr::allocator<GrBackendSemaphore>>\*, std::Cr::unique\_ptr<GrBackendSurfaceMutableState, std::Cr::default\_delete<GrBackendSurfaceMutableState>>\*) ./../../gpu/command\_buffer/service/shared\_image/external\_vk\_image\_skia\_representation.cc:43:19  

#23 0x55de06f4e8c6 in gpu::SkiaImageRepresentation::BeginScopedWriteAccess(int, SkSurfaceProps const&, gfx::Rect const&, std::Cr::vector<GrBackendSemaphore, std::Cr::allocator<GrBackendSemaphore>>\*, std::Cr::vector<GrBackendSemaphore, std::Cr::allocator<GrBackendSemaphore>>\*, gpu::SharedImageRepresentation::AllowUnclearedAccess, bool) ./../../gpu/command\_buffer/service/shared\_image/shared\_image\_representation.cc:192:9  

#24 0x55de06f4f8f1 in BeginScopedWriteAccess ./../../gpu/command\_buffer/service/shared\_image/shared\_image\_representation.cc:227:10  

#25 0x55de06f4f8f1 in gpu::SkiaImageRepresentation::BeginScopedWriteAccess(std::Cr::vector<GrBackendSemaphore, std::Cr::allocator<GrBackendSemaphore>>\*, std::Cr::vector<GrBackendSemaphore, std::Cr::allocator<GrBackendSemaphore>>\*, gpu::SharedImageRepresentation::AllowUnclearedAccess, bool) ./../../gpu/command\_buffer/service/shared\_image/shared\_image\_representation.cc:238:10  

#26 0x55de076c5df4 in gpu::raster::RasterDecoderImpl::DoCopySubTextureINTERNAL(int, int, int, int, int, int, unsigned char, signed char const volatile\*) ./../../gpu/command\_buffer/service/raster\_decoder.cc:1962:47  

#27 0x55de076bb502 in gpu::raster::RasterDecoderImpl::HandleCopySubTextureINTERNALImmediate(unsigned int, void const volatile\*) ./../../gpu/command\_buffer/s

**Additional Comments:**

\*\*Chrome version: \*\* 110.0.5449.0 \*\*Channel: \*\* Not sure

**OS:** Linux

## Attachments

- [asan.log](attachments/asan.log) (text/plain, 25.9 KB)
- [crash.html](attachments/crash.html) (text/plain, 837 B)
- [common.js](attachments/common.js) (text/plain, 11.1 KB)
- [about_gpu.txt](attachments/about_gpu.txt) (text/plain, 54.3 KB)

## Timeline

### [Deleted User] (2022-12-09)

[Empty comment from Monorail migration]

### cl...@chromium.org (2022-12-09)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6543741897867264.

### em...@gmail.com (2022-12-09)

I'm not sure cf can repro this kind issue,because It's hardware related bug.

### ad...@google.com (2022-12-09)

Yes, you're almost certainly right, but it's worth a try. If ClusterFuzz can reproduce it, it saves us many hours.

### ad...@google.com (2022-12-09)

I don't have a physical Linux box nearby with an Nvidia card, so I'm not going to attempt to reproduce this.

However the ASAN trace strongly suggests that https://crrev.com/f5f270e is related. In raster_decoder.cc there's this comment:

  // While this function indicates it's asynchronous, the flushAndSubmit()
  // call below ensures it completes synchronously. We do this because
  // RasterImplementation/Decoder does not currently have a query
  // that can handle asynchronous calls.

which presumably isn't true on some nvidia machines.

This might, of course, be a bug in the way some nvidia drivers handle flushing of commands... or something. But for now I'm going to assume that this is a bug in our code. Vasily, can you work out what to do here?

Setting security labels: FoundIn-108 on the assumption that this bug has been around for a while. Security_Severity-High due to UaR in GPU process.

[Monorail components: Internals>GPU>Vulkan]

### [Deleted User] (2022-12-09)

[Empty comment from Monorail migration]

### va...@chromium.org (2022-12-09)

Interesting. I suspect the device lost handling involved here, flushAndSubmit(true) supposed to be synchronous, but if we got device lost in the middle driver might not report completion or something like that. 

In stack trace from https://crbug.com/chromium/1399742#c0 the problem happens when we actually detected device lost.

I'll look into more details, but one thing we should do regardless of trying to handle this more gracefully is to CHECK that callback was actually run during that function call as we rely on it.

### [Deleted User] (2022-12-09)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-12-09)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### an...@chromium.org (2022-12-19)

[security marshal] Hi vasilyt@! Any update on this issue?

### [Deleted User] (2022-12-23)

vasilyt: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-01-06)

vasilyt: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2023-01-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/081df1e7d3712131bcaa575bda2e37ec7f6aa83d

commit 081df1e7d3712131bcaa575bda2e37ec7f6aa83d
Author: Vasiliy Telezhnikov <vasilyt@chromium.org>
Date: Mon Jan 16 15:41:34 2023

CHECK that YUV readback finished synchronously

DoReadbackYUVImagePixelsINTERNAL is implemented using skia asynchronous
readback and to make it synchronous we use sync cpu and gpu. In some
edge cases on linux we saw that doesn't happen if readback triggered
vulkan device lost.

To avoid use after free, CHECK that callback was actually called. In
case of device-lost gpu process will restart anyway, so while this is
not proper fix of the problem, it doesn't result in worse user visible
behaviour.

Bug: 1399742
Change-Id: Ie2172539bb907b9696ef62c70d398aca3967177c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4143606
Reviewed-by: Peng Huang <penghuang@chromium.org>
Commit-Queue: Vasiliy Telezhnikov <vasilyt@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1093064}

[modify] https://crrev.com/081df1e7d3712131bcaa575bda2e37ec7f6aa83d/gpu/command_buffer/service/raster_decoder.cc


### ja...@chromium.org (2023-02-02)

[security marshal]

Hi vasilyt@ thanks for the fix. Can you confirm if there are any other changes needed to address the issue?


### va...@chromium.org (2023-02-02)

The fix turns security issue in a clean crash issue. 

Ideally we shouldn't hit that check and reach vulkan device lost handling code that will restart gpu process cleanly, but it seems to be driver dependent (I'm guessing driver doesn't report error when we ask if gpu has finished workload). From user perspective there is not much difference between gpu process crash via CHECK or base::TerminateCurrentProcessImmediately [1], so investigating and working around gpu issue is lower priority.

Maybe we should mark this as fixed and file follow-up issue for gpu, if this is easier for security fixes workflow.

[1] https://source.chromium.org/chromium/chromium/src/+/main:components/viz/service/main/viz_main_impl.cc;drc=2a7fa9b6065bba9cbe273ddc4f5e5a4a51bb450d;l=298

### ja...@chromium.org (2023-02-02)

Sounds good, vasilyt. Go ahead and file the ticket for followup work, linking it here, and then mark this issue as fixed.

Thanks!

### va...@chromium.org (2023-02-02)

[Empty comment from Monorail migration]

### va...@chromium.org (2023-02-02)

Files https://crbug.com/chromium/1412504, marking this as fixed.

### [Deleted User] (2023-02-02)

Requesting merge to extended stable M108 because latest trunk commit (1093064) appears to be after extended stable branch point (1058933).

Requesting merge to other stable M109 because latest trunk commit (1093064) appears to be after other stable branch point (1070088).

Requesting merge to stable M110 because latest trunk commit (1093064) appears to be after stable branch point (1084008).

Not requesting merge to dev (M111) because latest trunk commit (1093064) appears to be prior to dev branch point (1097615). If this is incorrect, please replace the Merge-NA-111 label with Merge-Request-111. If other changes are required to fix this bug completely, please request a merge if necessary.

Merge approved: your change passed merge requirements and is auto-approved for M111. Please go ahead and merge the CL to branch 5563 (refs/branch-heads/5563) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: harrysouders (Android), harrysouders (iOS), dgagnon (ChromeOS), pbommana (Desktop)

Merge review required: M108 is already shipping to stable.

Merge review required: M109 is already shipping to stable.

Merge review required: M110 has already been cut for stable release.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [108, 109, 110].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### va...@chromium.org (2023-02-02)

1. https://chromium-review.googlesource.com/c/chromium/src/+/4143606
2. Change was released in Canary and Dev, I don't see crashes related to it
3. Change replaces security issue (which likely to cause crash) with guaranteed clean crash.
4. No
5. No. 

### [Deleted User] (2023-02-03)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-03)

[Empty comment from Monorail migration]

### pb...@google.com (2023-02-06)

[Bulk Edit] This merge has been approved for M111, please help complete your merges asap (before 3pm PST) today, so the change can be included in this week's RC build for dev/beta releases.`

We would like to get the changes as much Dev/beta time as possible, so please complete your merges asap to M111 branch(go/chrome-branches).

### va...@chromium.org (2023-02-06)

I think bot is a bit confused, CL in question was landed in 111.0.5561.2 and so doesn't need to be merged to M111.

### am...@google.com (2023-02-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-02-09)

Congratulations, Cassidy Kim! The VRP Panel has decided to award you $10,000 for this report. Thank you for your efforts and reporting this issue to us -- great work! 

### am...@chromium.org (2023-02-10)

M110 merge approved, please merge to branch 5481 so this fix can be included in the next 110/Stable refresh -- ty! 

### am...@chromium.org (2023-02-10)

forgot to remove the merge labels for 108 and 109 as there are no further planned releases for either 

### gi...@appspot.gserviceaccount.com (2023-02-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/e79b89b47dacd0efe12cd0a8328a53f62d1a3a9c

commit e79b89b47dacd0efe12cd0a8328a53f62d1a3a9c
Author: Vasiliy Telezhnikov <vasilyt@chromium.org>
Date: Fri Feb 10 17:36:57 2023

CHECK that YUV readback finished synchronously

DoReadbackYUVImagePixelsINTERNAL is implemented using skia asynchronous
readback and to make it synchronous we use sync cpu and gpu. In some
edge cases on linux we saw that doesn't happen if readback triggered
vulkan device lost.

To avoid use after free, CHECK that callback was actually called. In
case of device-lost gpu process will restart anyway, so while this is
not proper fix of the problem, it doesn't result in worse user visible
behaviour.

(cherry picked from commit 081df1e7d3712131bcaa575bda2e37ec7f6aa83d)

Bug: 1399742
Change-Id: Ie2172539bb907b9696ef62c70d398aca3967177c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4143606
Reviewed-by: Peng Huang <penghuang@chromium.org>
Commit-Queue: Vasiliy Telezhnikov <vasilyt@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1093064}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4239960
Cr-Commit-Position: refs/branch-heads/5481@{#1084}
Cr-Branched-From: 130f3e4d850f4bc7387cfb8d08aa993d288a67a9-refs/heads/main@{#1084008}

[modify] https://crrev.com/e79b89b47dacd0efe12cd0a8328a53f62d1a3a9c/gpu/command_buffer/service/raster_decoder.cc


### am...@google.com (2023-02-10)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-02-20)

[Empty comment from Monorail migration]

### am...@google.com (2023-02-21)

[Empty comment from Monorail migration]

### pg...@google.com (2023-02-22)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-13)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1399742?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail blocking: crbug.com/chromium/1412504]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062145)*
