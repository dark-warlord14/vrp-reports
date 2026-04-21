# UAF in vk::Format::getAspectFormat(unsigned int)

| Field | Value |
|-------|-------|
| **Issue ID** | [40937251](https://issues.chromium.org/issues/40937251) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU>SwiftShader |
| **Platforms** | Linux, Mac, Windows |
| **Reporter** | em...@gmail.com |
| **Assignee** | sy...@chromium.org |
| **Created** | 2023-10-22 |
| **Bounty** | $10,000.00 |

## Description

**Steps to reproduce the problem:**  

tested os version:

- ubuntu 22.04  
  
  tested chrome version:  
  
  Chromium 120.0.6073.0  
  
  Chromium 120.0.6080.0(gs://chromium-browser-asan/linux-release/asan-linux-release-1213059.zip)  
  
  repro steps:  
  
  1 python3 -m http.server 8000 --dir=|PATH|  
  
  2 ./chrome --user-data-dir=/tmp/xx4 --disable-gpu <http://localhost:8000/crash.html>  
  
  Need to wait for 30~60 seconds to repro.

**Problem Description:**  

==18570==ERROR: AddressSanitizer: heap-use-after-free on address 0x5110001943e8 at pc 0x7fe01a0c96d9 bp 0x7fdfee163c10 sp 0x7fdfee163c08  

READ of size 4 at 0x5110001943e8 thread T18  

#0 0x7fe01a0c96d8 in vk::Format::getAspectFormat(unsigned int) const ./../../third\_party/swiftshader/src/Vulkan/VkFormat.cpp:182:10  

#1 0x7fe01a0dece6 in getFormat ./../../third\_party/swiftshader/src/Vulkan/VkImage.cpp:872:16  

#2 0x7fe01a0dece6 in vk::Image::copy(void const\*, void\*, unsigned int, unsigned int, VkImageSubresourceLayers const&, VkOffset3D const&, VkExtent3D const&) ./../../third\_party/swiftshader/src/Vulkan/VkImage.cpp:616:22  

#3 0x7fe01a0df7ca in vk::Image::copyFrom(vk::Buffer\*, VkBufferImageCopy2 const&) ./../../third\_party/swiftshader/src/Vulkan/VkImage.cpp:684:2  

#4 0x7fe01a0a7fbb in vk::CommandBuffer::submit(vk::CommandBuffer::ExecutionState&) ./../../third\_party/swiftshader/src/Vulkan/VkCommandBuffer.cpp:2330:12  

#5 0x7fe01a1021a8 in vk::Queue::submitQueue(vk::Queue::Task const&) ./../../third\_party/swiftshader/src/Vulkan/VkQueue.cpp:104:42  

#6 0x7fe01a101170 in vk::Queue::taskLoop(marl::Scheduler\*) ./../../third\_party/swiftshader/src/Vulkan/VkQueue.cpp:156:4  

#7 0x7fe01a104a81 in \_\_invoke<void (vk::Queue::\*)(marl::Scheduler \*), vk::Queue \*, marl::Scheduler \*, void> ./../../third\_party/libc++/src/include/\_\_type\_traits/invoke.h:312:25  

#8 0x7fe01a104a81 in \_\_thread\_execute<std::\_\_Cr::unique\_ptr<std::\_\_Cr::\_\_thread\_struct, std::\_\_Cr::default\_delete[std::\_\_Cr::\_\_thread\_struct](javascript:void(0);) >, void (vk::Queue::\*)(marl::Scheduler \*), vk::Queue \*, marl::Scheduler \*, 2UL, 3UL> ./../../third\_party/libc++/src/include/\_\_thread/thread.h:221:5  

#9 0x7fe01a104a81 in void\* std::\_\_Cr::\_\_thread\_proxy<std::\_\_Cr::tuple<std::\_\_Cr::unique\_ptr<std::\_\_Cr::\_\_thread\_struct, std::\_\_Cr::default\_delete[std::\_\_Cr::\_\_thread\_struct](javascript:void(0);)>, void (vk::Queue::\*)(marl::Scheduler\*), vk::Queue\*, marl::Scheduler\*>>(void\*) ./../../third\_party/libc++/src/include/\_\_thread/thread.h:232:5  

#10 0x561eb9d6b1d8 in asan\_thread\_start(void\*) *asan\_rtl*:28

0x5110001943e8 is located 40 bytes inside of 200-byte region [0x5110001943c0,0x511000194488)  

freed by thread T19 here:  

#0 0x561eb9d6d376 in \_\_interceptor\_free *asan\_rtl*:3  

#1 0x7fe01c34ea8a in rx::vk::GarbageObject::destroy(rx::RendererVk\*) ./../../third\_party/angle/src/libANGLE/renderer/vulkan/vk\_utils.cpp:0:0  

#2 0x7fe01c167dda in rx::vk::SharedGarbage::destroyIfComplete(rx::RendererVk\*) ./../../third\_party/angle/src/libANGLE/renderer/vulkan/ResourceVk.cpp:88:20  

#3 0x7fe01c14df75 in rx::vk::SharedGarbageList[rx::vk::SharedGarbage](javascript:void(0);)::cleanupSubmittedGarbage(rx::RendererVk\*) ./../../third\_party/angle/src/libANGLE/renderer/vulkan/ResourceVk.h:241:26  

#4 0x7fe01c128a67 in rx::RendererVk::cleanupGarbage() ./../../third\_party/angle/src/libANGLE/renderer/vulkan/RendererVk.cpp:5259:24  

#5 0x7fe01c033cc8 in rx::vk::CommandProcessor::processTasksImpl(bool\*) ./../../third\_party/angle/src/libANGLE/renderer/vulkan/CommandProcessor.cpp:688:24  

#6 0x7fe01c0332f3 in rx::vk::CommandProcessor::processTasks() ./../../third\_party/angle/src/libANGLE/renderer/vulkan/CommandProcessor.cpp:616:32  

#7 0x7fe01c04a550 in \_\_invoke<void (rx::vk::CommandProcessor::\*)(), rx::vk::CommandProcessor \*, void> ./../../third\_party/libc++/src/include/\_\_type\_traits/invoke.h:312:25  

#8 0x7fe01c04a550 in \_\_thread\_execute<std::\_\_Cr::unique\_ptr<std::\_\_Cr::\_\_thread\_struct, std::\_\_Cr::default\_delete[std::\_\_Cr::\_\_thread\_struct](javascript:void(0);) >, void (rx::vk::CommandProcessor::\*)(), rx::vk::CommandProcessor \*, 2UL> ./../../third\_party/libc++/src/include/\_\_thread/thread.h:221:5  

#9 0x7fe01c04a550 in void\* std::\_\_Cr::\_\_thread\_proxy<std::\_\_Cr::tuple<std::\_\_Cr::unique\_ptr<std::\_\_Cr::\_\_thread\_struct, std::\_\_Cr::default\_delete[std::\_\_Cr::\_\_thread\_struct](javascript:void(0);)>, void (rx::vk::CommandProcessor::\*)(), rx::vk::CommandProcessor\*>>(void\*) ./../../third\_party/libc++/src/include/\_\_thread/thread.h:232:5  

#10 0x561eb9d6b1d8 in asan\_thread\_start(void\*) *asan\_rtl*:28

previously allocated by thread T0 (chrome) here:  

#0 0x561eb9d6d60d in \_\_interceptor\_malloc *asan\_rtl*:3  

#1 0x7fe01a45489b in allocate ./../../third\_party/swiftshader/src/System/Memory.cpp:81:42  

#2 0x7fe01a45489b in sw::allocateZeroOrPoison(unsigned long, unsigned long) ./../../third\_party/swiftshader/src/System/Memory.cpp:110:9  

#3 0x7fe01a126b46 in Create<vk::Image, VkNonDispatchableHandle<VkImage\_T \*>, VkImageCreateInfo, vk::Device \*> ./../../third\_party/swiftshader/src/Vulkan/VkObject.hpp:58:23  

#4 0x7fe01a126b46 in VkResult vk::ObjectBase<vk::Image, VkNonDispatchableHandle<VkImage\_T\*>>::Create<VkImageCreateInfo, vk::Device\*>(VkAllocationCallbacks const\*, VkImageCreateInfo const\*, VkNonDispatchableHandle<VkImage\_T\*>\*, vk::Device\*) ./../../third\_party/swiftshader/src/Vulkan/VkObject.hpp:92:10  

#5 0x7fe01a126a1f in vkCreateImage ./../../third\_party/swiftshader/src/Vulkan/libVulkan.cpp:2024:20  

#6 0x7fe01c2f62bf in init ./../../third\_party/angle/src

**Additional Comments:**

\*\*Chrome version: \*\* 120.0.6073.0 \*\*Channel: \*\* Dev

**OS:** Linux

## Attachments

- [crash.html](attachments/crash.html) (text/plain, 1.3 KB)
- [asan.log](attachments/asan.log) (text/plain, 25.3 KB)

## Timeline

### [Deleted User] (2023-10-22)

[Empty comment from Monorail migration]

### ma...@chromium.org (2023-10-24)

Interestingly there is an similar looking stack from a couple years ago: https://crbug.com/chromium/1270658

Severity-critical for a remotely-triggerable memory corruption in gpu process, which is not sandboxed in all platforms 
Foundin-120 as it repros in 120 but not in 119.
Copied OS from https://crbug.com/chromium/1270658, please update if that's not correct.



[Monorail components: Internals>GPU>SwiftShader]

### [Deleted User] (2023-10-24)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-24)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-10-24)

This is a critical security issue. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-10-24)

Setting Pri-0 to match security severity Critical. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-10-27)

Based on the information provided, this looks like a read from a buffer and there is not enough information to make a determination that this could be exploited to result in RCE. 
OP, if you have any information to demonstrate meaningful control of this value or the potential for RCE, we'd sincerely welcome that information. 
Reducing to sev-high based on the information provided. 

### am...@chromium.org (2023-10-27)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-28)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2023-11-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/9a5d75de4b501216963dd5f7b6eca048172ea6b1

commit 9a5d75de4b501216963dd5f7b6eca048172ea6b1
Author: Shahbaz Youssefi <syoussefi@chromium.org>
Date: Mon Oct 30 15:59:19 2023

Vulkan: Fix incompatible redefinition of cube faces

The TextureVk::mRedefinedLevels bitmask tracked which levels are
incompatibly redefined, greatly reducing the complexity of dealing with
GL's mutable textures.

It did not however take into account the fact that GL allows each
cubemap face to be separately redefined (unlike 2D arrays, where all
layers are defined together).  This change turns the bitmask into an
array of bitmasks.  Previously, a single bit represented whether the
level is incompatibly redefined.  Now, elements of the array track the
same information for each cube face.  For non-cube-map textures, only
element 0 is used.

Bug: chromium:1494664
Change-Id: I69568d3da2391796bf5f01505861fee42c6c8924
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/4986289
Reviewed-by: Charlie Lao <cclao@google.com>
Reviewed-by: Yuxin Hu <yuxinhu@google.com>
Commit-Queue: Shahbaz Youssefi <syoussefi@chromium.org>

[modify] https://crrev.com/9a5d75de4b501216963dd5f7b6eca048172ea6b1/src/tests/gl_tests/TextureTest.cpp
[modify] https://crrev.com/9a5d75de4b501216963dd5f7b6eca048172ea6b1/src/libANGLE/renderer/vulkan/vk_helpers.h
[modify] https://crrev.com/9a5d75de4b501216963dd5f7b6eca048172ea6b1/src/libANGLE/renderer/vulkan/TextureVk.h
[modify] https://crrev.com/9a5d75de4b501216963dd5f7b6eca048172ea6b1/src/libANGLE/renderer/vulkan/vk_helpers.cpp
[modify] https://crrev.com/9a5d75de4b501216963dd5f7b6eca048172ea6b1/src/tests/angle_end2end_tests_expectations.txt
[modify] https://crrev.com/9a5d75de4b501216963dd5f7b6eca048172ea6b1/src/libANGLE/renderer/vulkan/TextureVk.cpp
[modify] https://crrev.com/9a5d75de4b501216963dd5f7b6eca048172ea6b1/src/libANGLE/angletypes.h


### sy...@chromium.org (2023-11-01)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-01)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-01)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-11-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/74bdea67d7f382a72bb3ad5ce0a02c83be82b077

commit 74bdea67d7f382a72bb3ad5ce0a02c83be82b077
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Wed Nov 01 19:54:20 2023

Roll ANGLE from f71a5bade95e to 918028a253b0 (3 revisions)

https://chromium.googlesource.com/angle/angle.git/+log/f71a5bade95e..918028a253b0

2023-11-01 ynovikov@chromium.org Update bot detection in capture_replay_tests
2023-11-01 syoussefi@chromium.org Vulkan: Fix incompatible redefinition of cube faces
2023-11-01 angle-autoroll@skia-public.iam.gserviceaccount.com Roll vulkan-deps from e55b4f78bcf3 to 54bfabb1adb0 (11 revisions)

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/angle-chromium-autoroll
Please CC angle-team@google.com,syoussefi@google.com on the revert to ensure that a human
is aware of the problem.

To file a bug in ANGLE: https://bugs.chromium.org/p/angleproject/issues/entry
To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://issues.skia.org/issues/new?component=1389291&template=1850622

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86
Bug: chromium:1494664
Tbr: syoussefi@google.com
Change-Id: If568f4e07a4da3d3391040c92adca30066bc5172
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4998130
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#1218393}

[modify] https://crrev.com/74bdea67d7f382a72bb3ad5ce0a02c83be82b077/DEPS
[modify] https://crrev.com/74bdea67d7f382a72bb3ad5ce0a02c83be82b077/third_party/angle


### [Deleted User] (2023-11-02)

This release blocking issue appears to be targeted for one or more milestones which may have already branched:

 - M120, which branched on 2023-10-30 (Chromium branch: 6099, Chromium branch position: 1217362)

Because this issue was marked as fixed on or after branch day, a merge of any CLs which landed on or after branch day may be required.

If no merge is needed (e.g. the necessary CLs are already present in the relevant branch), please remove the Merge-TBD-## label and replace it with a Merge-NA-## label (where ## corresponds to the milestone under evaluation). If a merge is necessary, please add the appropriate Merge-Request-## labels. If you're not sure, reach out to the relevant release manager (can be found at https://chromiumdash.appspot.com/schedule).

To learn more about the merge process, including how to land any required merges, see https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sy...@chromium.org (2023-11-07)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-07)

Merge review required: a commit with DEPS changes was detected.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: harrysouders (Android), harrysouders (iOS), obenedict (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-11-07)

Thanks for fix here syoussefi@ 
120 merge approved for https://crrev.com/c/4986289
please merge this fix to 120 / branch 6099 at soonest so this fix can be included in the next 120 Beta update tomorrow -- ty! 

### sy...@chromium.org (2023-11-07)

Will do. For posterity:

1. Security fix
2. https://chromium-review.googlesource.com/c/angle/angle/+/4986289
3. It's been 6 days, likely got Canary testing on Android
4. No
5. N/A
6. N/A

### gi...@appspot.gserviceaccount.com (2023-11-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/fa028f307139f9f4c46dd81204d0872b233ce222

commit fa028f307139f9f4c46dd81204d0872b233ce222
Author: Shahbaz Youssefi <syoussefi@chromium.org>
Date: Mon Oct 30 15:59:19 2023

M120: Vulkan: Fix incompatible redefinition of cube faces

The TextureVk::mRedefinedLevels bitmask tracked which levels are
incompatibly redefined, greatly reducing the complexity of dealing with
GL's mutable textures.

It did not however take into account the fact that GL allows each
cubemap face to be separately redefined (unlike 2D arrays, where all
layers are defined together).  This change turns the bitmask into an
array of bitmasks.  Previously, a single bit represented whether the
level is incompatibly redefined.  Now, elements of the array track the
same information for each cube face.  For non-cube-map textures, only
element 0 is used.

Bug: chromium:1494664
Change-Id: I7e6673d5949fc4fa7a50a0990ad1866902c92829
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/5007224
Reviewed-by: Solti Ho <solti@google.com>

[modify] https://crrev.com/fa028f307139f9f4c46dd81204d0872b233ce222/src/tests/gl_tests/TextureTest.cpp
[modify] https://crrev.com/fa028f307139f9f4c46dd81204d0872b233ce222/src/libANGLE/renderer/vulkan/vk_helpers.h
[modify] https://crrev.com/fa028f307139f9f4c46dd81204d0872b233ce222/src/tests/angle_end2end_tests_expectations.txt
[modify] https://crrev.com/fa028f307139f9f4c46dd81204d0872b233ce222/src/libANGLE/renderer/vulkan/vk_helpers.cpp
[modify] https://crrev.com/fa028f307139f9f4c46dd81204d0872b233ce222/src/libANGLE/renderer/vulkan/TextureVk.h
[modify] https://crrev.com/fa028f307139f9f4c46dd81204d0872b233ce222/src/libANGLE/renderer/vulkan/TextureVk.cpp
[modify] https://crrev.com/fa028f307139f9f4c46dd81204d0872b233ce222/src/libANGLE/angletypes.h


### am...@google.com (2023-11-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-11-09)

Congratulations Cassidy Kim! The Chrome VRP Panel has decided to award you $10,000 for this report. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2023-11-11)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1494664?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-02-08)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40937251)*
