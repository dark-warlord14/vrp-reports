# Security: use after free in swiftshader

| Field | Value |
|-------|-------|
| **Issue ID** | [40057932](https://issues.chromium.org/issues/40057932) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Internals>GPU>SwiftShader |
| **Platforms** | Linux, Mac, Windows |
| **Reporter** | ao...@gmail.com |
| **Assignee** | sy...@chromium.org |
| **Created** | 2021-11-16 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**  

A use after free occurs when the attached page is opened.

**VERSION**  

Chrome Version: 98.0.4706.0 (prebuilt 941492)  

Operating System: Linux, Debian 11.1

**REPRODUCTION CASE**  

Open the attached page.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: GPU process  

Crash State:  

==788177==ERROR: AddressSanitizer: heap-use-after-free on address 0x614000092328 at pc 0x7f6c61c0ef84 bp 0x7f6c57f65370 sp 0x7f6c57f65368  

READ of size 4 at 0x614000092328 thread T18  

SCARINESS: 45 (4-byte-read-heap-use-after-free)  

#0 0x7f6c61c0ef83 in vk::Format::getAspectFormat(unsigned int) const third\_party/swiftshader/src/Vulkan/VkFormat.cpp:177:10  

#1 0x7f6c61c1f0ac in getFormat third\_party/swiftshader/src/Vulkan/VkImage.cpp:861:16  

#2 0x7f6c61c1f0ac in vk::Image::copy(vk::Buffer\*, VkBufferImageCopy2KHR const&, bool) third\_party/swiftshader/src/Vulkan/VkImage.cpp:565:22  

#3 0x7f6c61bf3996 in vk::CommandBuffer::submit(vk::CommandBuffer::ExecutionState&) third\_party/swiftshader/src/Vulkan/VkCommandBuffer.cpp:1757:12  

#4 0x7f6c61c39a75 in vk::Queue::submitQueue(vk::Queue::Task const&) third\_party/swiftshader/src/Vulkan/VkQueue.cpp:236:42  

#5 0x7f6c61c3892e in vk::Queue::taskLoop(marl::Scheduler\*) third\_party/swiftshader/src/Vulkan/VkQueue.cpp:288:4  

#6 0x7f6c61c3b80a in \_\_invoke<void (vk::Queue::\*)(marl::Scheduler \*), vk::Queue \*, marl::Scheduler \*, void> buildtools/third\_party/libc++/trunk/include/type\_traits:3897:1  

#7 0x7f6c61c3b80a in \_\_thread\_execute<std::\_\_1::unique\_ptr<std::\_\_1::\_\_thread\_struct, std::\_\_1::default\_delete[std::\_\_1::\_\_thread\_struct](javascript:void(0);) >, void (vk::Queue::\*)(marl::Scheduler \*), vk::Queue \*, marl::Scheduler \*, 2UL, 3UL> buildtools/third\_party/libc++/trunk/include/thread:280:5  

#8 0x7f6c61c3b80a in void\* std::\_\_1::\_\_thread\_proxy<std::\_\_1::tuple<std::\_\_1::unique\_ptr<std::\_\_1::\_\_thread\_struct, std::\_\_1::default\_delete[std::\_\_1::\_\_thread\_struct](javascript:void(0);) >, void (vk::Queue::\*)(marl::Scheduler\*), vk::Queue\*, marl::Scheduler\*> >(void\*) buildtools/third\_party/libc++/trunk/include/thread:291:5  

#9 0x7f6c6bf71608 in start\_thread /build/glibc-eX1tMB/glibc-2.31/nptl/pthread\_create.c:477:8

**CREDIT INFORMATION**  

Reporter credit: Aki Helin, Solita

## Attachments

- [chrome-uaf-getAspectFormat.html](attachments/chrome-uaf-getAspectFormat.html) (text/plain, 2.2 KB)

## Timeline

### [Deleted User] (2021-11-16)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-11-18)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6505703323533312.

### cl...@chromium.org (2021-11-19)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-11-19)

Detailed Report: https://clusterfuzz.com/testcase?key=6505703323533312

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x61200013e828
Crash State:
  vk::Format::getAspectFormat
  vk::Image::copy
  vk::CommandBuffer::submit
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=885401:885402

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6505703323533312

The reproduce tool requires a ClusterFuzz source checkout. To prepare one, run:

git clone https://github.com/google/clusterfuzz && cd clusterfuzz && git checkout tags/reproduce-tool-stable

To reproduce this issue, run:

./reproduce.sh -t https://clusterfuzz.com/testcase-detail/6505703323533312 -b /path/to/build

Please use the GN arguments provided in this report when building the binary. If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


A recommended severity was added to this bug. Please change the severity if it is inaccurate.

### mp...@chromium.org (2021-11-19)

[Empty comment from Monorail migration]

[Monorail components: Internals>GPU>SwiftShader]

### mp...@chromium.org (2021-11-19)

[Empty comment from Monorail migration]

### mp...@chromium.org (2021-11-19)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-20)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ni...@google.com (2021-11-22)

Alexis can you have a look at this?

### su...@chromium.org (2021-11-22)

+syoussefi@

This is a 100% repro (tried it 5 times, got the ASAN failure 5 times) case where ANGLE's garbage collector deletes an object SwiftShader is still using in a Queue submit. I'll try to get more info, but it looks like this test case isn't as flaky as the other ones we've received so far.

### sy...@chromium.org (2021-11-23)

Looks like a case where ANGLE is missing a retain() call on an image that's being used by the command buffer. If you can turn the test into an end2end test, we can reduce it further and I can help you figure out what's missing (or take over from there)

### su...@chromium.org (2021-11-24)

I created the end2end test you requested:
https://chromium-review.googlesource.com/c/angle/angle/+/3300899
It throws a ton of UNASSIGNED-CoreValidation-DrawState-InvalidCommandBuffer-VkImage errors, so that's probably it.
Sending over to you to complete the investigation.

### gi...@appspot.gserviceaccount.com (2021-12-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/8f6f5a4bb28d4f9cef8b747c9cd384ebcebb2a6a

commit 8f6f5a4bb28d4f9cef8b747c9cd384ebcebb2a6a
Author: Shahbaz Youssefi <syoussefi@chromium.org>
Date: Wed Dec 01 04:48:30 2021

Vulkan: Fix image respecify's usage tracking

When respecifying an image due to mip level count changes, the previous
image is staged as an update to the new image.  The resource usage info
was not being transferred to the image being staged as an update,
causing it to be prematurely deleted.

Test based on one authored by sugoi@google.com.

Bug: chromium:1270658
Bug: angleproject:4835
Change-Id: I215c65ba700d7be608d0910d3cb37fcfdf297a2a
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3308921
Commit-Queue: Shahbaz Youssefi <syoussefi@chromium.org>
Reviewed-by: Jamie Madill <jmadill@chromium.org>

[modify] https://crrev.com/8f6f5a4bb28d4f9cef8b747c9cd384ebcebb2a6a/src/libANGLE/renderer/vulkan/ResourceVk.h
[modify] https://crrev.com/8f6f5a4bb28d4f9cef8b747c9cd384ebcebb2a6a/src/tests/gl_tests/MipmapTest.cpp
[modify] https://crrev.com/8f6f5a4bb28d4f9cef8b747c9cd384ebcebb2a6a/src/libANGLE/renderer/vulkan/ResourceVk.cpp
[modify] https://crrev.com/8f6f5a4bb28d4f9cef8b747c9cd384ebcebb2a6a/src/libANGLE/renderer/vulkan/vk_helpers.cpp


### gi...@appspot.gserviceaccount.com (2021-12-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/a1bfeb949fd02f2f73ab62b4d20a1493cbc6189a

commit a1bfeb949fd02f2f73ab62b4d20a1493cbc6189a
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Wed Dec 01 19:46:35 2021

Roll ANGLE from 9d91064d6c8b to 8f6f5a4bb28d (2 revisions)

https://chromium.googlesource.com/angle/angle.git/+log/9d91064d6c8b..8f6f5a4bb28d

2021-12-01 syoussefi@chromium.org Vulkan: Fix image respecify's usage tracking
2021-12-01 ynovikov@chromium.org Skip MultithreadingTestES3.MultithreadFenceTexImage on TSAN

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/angle-chromium-autoroll
Please CC ynovikov@google.com on the revert to ensure that a human
is aware of the problem.

To file a bug in ANGLE: https://bugs.chromium.org/p/angleproject/issues/entry
To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86
Bug: chromium:1270658
Tbr: ynovikov@google.com
Change-Id: I9c3efef21a7597128fc824de424a95cf7a3ebaeb
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3311384
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#947153}

[modify] https://crrev.com/a1bfeb949fd02f2f73ab62b4d20a1493cbc6189a/DEPS


### sy...@chromium.org (2021-12-02)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-12-03)

ClusterFuzz testcase 6505703323533312 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=947149:947157

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### [Deleted User] (2021-12-03)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-03)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-03)

Requesting merge to stable M96 because latest trunk commit (947153) appears to be after stable branch point (929512).

Requesting merge to beta M97 because latest trunk commit (947153) appears to be after beta branch point (938553).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-12-03)

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
Owners: benmason (Android), harrysouders (iOS), ceb (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-12-03)

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
Owners: govind (Android), harrysouders (iOS), dgagnon (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sy...@chromium.org (2021-12-03)

1. Security bug
2. https://chromium-review.googlesource.com/c/angle/angle/+/3308921
3. Landed no Dec 1. Could use a few more days before merging
4. No
5. N/A
6. N/A

### am...@chromium.org (2021-12-06)

merge approved for M96 and M97; please go ahead and merge to M96/branch 4664 and M97/branch 4692 at your convenience 
M96 stable refresh was released today, but this fix should be included in M96 Extended Stable support 
Please merge to M97 before EOD 14 December so this fix can be included in M97 Stable 



### gi...@appspot.gserviceaccount.com (2021-12-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/f55d3ffa8f28fe609c07d127f89a60bb9ec52faa

commit f55d3ffa8f28fe609c07d127f89a60bb9ec52faa
Author: Shahbaz Youssefi <syoussefi@chromium.org>
Date: Wed Dec 01 04:48:30 2021

M97: Vulkan: Fix image respecify's usage tracking

When respecifying an image due to mip level count changes, the previous
image is staged as an update to the new image.  The resource usage info
was not being transferred to the image being staged as an update,
causing it to be prematurely deleted.

Test based on one authored by sugoi@google.com.

Bug: chromium:1270658
Bug: angleproject:4835
Change-Id: Ib1762e57bfff732fca52f5c65ae8fd305b9d13f0
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3318258
Reviewed-by: Lingfeng Yang <lfy@google.com>

[modify] https://crrev.com/f55d3ffa8f28fe609c07d127f89a60bb9ec52faa/src/libANGLE/renderer/vulkan/ResourceVk.h
[modify] https://crrev.com/f55d3ffa8f28fe609c07d127f89a60bb9ec52faa/src/tests/gl_tests/MipmapTest.cpp
[modify] https://crrev.com/f55d3ffa8f28fe609c07d127f89a60bb9ec52faa/src/libANGLE/renderer/vulkan/ResourceVk.cpp
[modify] https://crrev.com/f55d3ffa8f28fe609c07d127f89a60bb9ec52faa/src/libANGLE/renderer/vulkan/vk_helpers.cpp


### gi...@appspot.gserviceaccount.com (2021-12-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/2b98abd8cb6caae2f3b6cd9e5ab7e70f2ee25e57

commit 2b98abd8cb6caae2f3b6cd9e5ab7e70f2ee25e57
Author: Shahbaz Youssefi <syoussefi@chromium.org>
Date: Wed Dec 01 04:48:30 2021

M96: Vulkan: Fix image respecify's usage tracking

When respecifying an image due to mip level count changes, the previous
image is staged as an update to the new image.  The resource usage info
was not being transferred to the image being staged as an update,
causing it to be prematurely deleted.

Test based on one authored by sugoi@google.com.

Bug: chromium:1270658
Bug: angleproject:4835
Change-Id: I9810f8940e0107bc8a04fa3fb9c26a045c0d689c
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3318257
Reviewed-by: Lingfeng Yang <lfy@google.com>

[modify] https://crrev.com/2b98abd8cb6caae2f3b6cd9e5ab7e70f2ee25e57/src/libANGLE/renderer/vulkan/ResourceVk.h
[modify] https://crrev.com/2b98abd8cb6caae2f3b6cd9e5ab7e70f2ee25e57/src/tests/gl_tests/MipmapTest.cpp
[modify] https://crrev.com/2b98abd8cb6caae2f3b6cd9e5ab7e70f2ee25e57/src/libANGLE/renderer/vulkan/ResourceVk.cpp
[modify] https://crrev.com/2b98abd8cb6caae2f3b6cd9e5ab7e70f2ee25e57/src/libANGLE/renderer/vulkan/vk_helpers.cpp


### sy...@chromium.org (2021-12-06)

Done

### am...@google.com (2021-12-06)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-12-06)

Congratulations, Aki! The VRP Panel has decided to award you $5,000 for this report. Thank you for this report and nice work! 

### ad...@chromium.org (2021-12-10)

[Empty comment from Monorail migration]

### ad...@google.com (2021-12-10)

[Empty comment from Monorail migration]

### am...@google.com (2022-01-06)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-01-06)

^^ info was already sent to finance for payment processing on 7 December, automation borked and did not update here accordingly and was discovered and fixed today

### [Deleted User] (2022-03-11)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### do...@gmail.com (2022-04-13)

Let me know @junov if i can add any additional info to this bug.  thx

### am...@chromium.org (2022-07-29)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1270658?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/1271949, crbug.com/chromium/1271950]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057932)*
