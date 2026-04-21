# UAF in rx::vk::DynamicDescriptorPool::destroyCachedDescriptorSet

| Field | Value |
|-------|-------|
| **Issue ID** | [40068543](https://issues.chromium.org/issues/40068543) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU>Vulkan |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | em...@gmail.com |
| **Assignee** | sy...@chromium.org |
| **Created** | 2023-08-02 |
| **Bounty** | $10,000.00 |

## Description

**Steps to reproduce the problem:**  

tested os:  

ubuntu 22.04  

tested chromium:  

Chromium 116.0.5845.42  

Chromium 117.0.5926.0 (gs://chromium-browser-asan/linux-release/asan-linux-release-1178292.zip)  

/home/cowboy/chromium/src/out/chrome\_asan\_shared/chrome --disable-gpu --incognito --user-data-dir=/tmp/xx8 <http://localhost:8605/crash2/poc.html>  

repro steps:  

./chrome --disable-gpu --incognito --user-data-dir=/tmp/xx8 poc.html  

after wait for a while, it will crash.

**Problem Description:**  

==2096627==ERROR: AddressSanitizer: heap-use-after-free on address 0x5160000c7b80 at pc 0x7fabff19ad52 bp 0x7fabca456ca0 sp 0x7fabca456c98  

READ of size 16 at 0x5160000c7b80 thread T18  

#0 0x7fabff19ad51 in GroupSse2Impl ./../../third\_party/abseil-cpp/absl/container/internal/raw\_hash\_set.h:585:12  

#1 0x7fabff19ad51 in absl::container\_internal::EraseMetaOnly(absl::container\_internal::CommonFields&, absl::container\_internal::ctrl\_t\*, unsigned long) ./../../third\_party/abseil-cpp/absl/container/internal/raw\_hash\_set.cc:217:28  

#2 0x7fabff144316 in erase\_meta\_only ./../../third\_party/abseil-cpp/absl/container/internal/raw\_hash\_set.h:2431:5  

#3 0x7fabff144316 in erase ./../../third\_party/abseil-cpp/absl/container/internal/raw\_hash\_set.h:2136:5  

#4 0x7fabff144316 in unsigned long absl::container\_internal::raw\_hash\_set<absl::container\_internal::FlatHashMapPolicy<rx::vk::DescriptorSetDesc, std::\_\_Cr::unique\_ptr<rx::DescriptorSetCache::dsCacheEntry, std::\_\_Cr::default\_delete[rx::DescriptorSetCache::dsCacheEntry](javascript:void(0);)>>, absl::hash\_internal::Hash[rx::vk::DescriptorSetDesc](javascript:void(0);), std::\_\_Cr::equal\_to[rx::vk::DescriptorSetDesc](javascript:void(0);), std::\_\_Cr::allocator<std::\_\_Cr::pair<rx::vk::DescriptorSetDesc const, std::\_\_Cr::unique\_ptr<rx::DescriptorSetCache::dsCacheEntry, std::\_\_Cr::default\_delete[rx::DescriptorSetCache::dsCacheEntry](javascript:void(0);)>>>>::erase[rx::vk::DescriptorSetDesc](javascript:void(0);)(rx::vk::DescriptorSetDesc const&) ./../../third\_party/abseil-cpp/absl/container/internal/raw\_hash\_set.h:2112:5  

#5 0x7fabff0f5096 in eraseDescriptorSet ./../../third\_party/angle/src/libANGLE/renderer/vulkan/vk\_cache\_utils.h:2566:18  

#6 0x7fabff0f5096 in rx::vk::DynamicDescriptorPool::destroyCachedDescriptorSet(rx::RendererVk\*, rx::vk::DescriptorSetDesc const&) ./../../third\_party/angle/src/libANGLE/renderer/vulkan/vk\_helpers.cpp:3875:29  

#7 0x7fabff05b011 in DestroyCachedObject ./../../third\_party/angle/src/libANGLE/renderer/vulkan/vk\_cache\_utils.cpp:2627:24  

#8 0x7fabff05b011 in rx::vk::SharedCacheKeyManager<std::\_\_Cr::shared\_ptr<std::\_\_Cr::unique\_ptr<rx::vk::DescriptorSetDescAndPool, std::\_\_Cr::default\_delete[rx::vk::DescriptorSetDescAndPool](javascript:void(0);)>>>::destroyKeys(rx::RendererVk\*) ./../../third\_party/angle/src/libANGLE/renderer/vulkan/vk\_cache\_utils.cpp:6520:13  

#9 0x7fabfef95ebe in rx::vk::BufferBlock::destroy(rx::RendererVk\*) ./../../third\_party/angle/src/libANGLE/renderer/vulkan/Suballocation.cpp:73:32  

#10 0x7fabfef96ba7 in destroy ./../../third\_party/angle/src/libANGLE/renderer/vulkan/Suballocation.h:281:27  

#11 0x7fabfef96ba7 in rx::vk::SharedBufferSuballocationGarbage::destroyIfComplete(rx::RendererVk\*) ./../../third\_party/angle/src/libANGLE/renderer/vulkan/Suballocation.cpp:191:24  

#12 0x7fabfef44a20 in rx::RendererVk::cleanupGarbage() ./../../third\_party/angle/src/libANGLE/renderer/vulkan/RendererVk.cpp:5223:22  

#13 0x7fabfee3a381 in rx::vk::CommandProcessor::processTasksImpl(bool\*) ./../../third\_party/angle/src/libANGLE/renderer/vulkan/CommandProcessor.cpp:687:24  

#14 0x7fabfee39823 in rx::vk::CommandProcessor::processTasks() ./../../third\_party/angle/src/libANGLE/renderer/vulkan/CommandProcessor.cpp:615:32  

#15 0x7fabfee50480 in \_\_invoke<void (rx::vk::CommandProcessor::\*)(), rx::vk::CommandProcessor \*, void> ./../../buildtools/third\_party/libc++/trunk/include/\_\_type\_traits/invoke.h:308:25  

#16 0x7fabfee50480 in \_\_thread\_execute<std::\_\_Cr::unique\_ptr<std::\_\_Cr::\_\_thread\_struct, std::\_\_Cr::default\_delete[std::\_\_Cr::\_\_thread\_struct](javascript:void(0);) >, void (rx::vk::CommandProcessor::\*)(), rx::vk::CommandProcessor \*, 2UL> ./../../buildtools/third\_party/libc++/trunk/include/\_\_thread/thread.h:193:5  

#17 0x7fabfee50480 in void\* std::\_\_Cr::\_\_thread\_proxy<std::\_\_Cr::tuple<std::\_\_Cr::unique\_ptr<std::\_\_Cr::\_\_thread\_struct, std::\_\_Cr::default\_delete[std::\_\_Cr::\_\_thread\_struct](javascript:void(0);)>, void (rx::vk::CommandProcessor::\*)(), rx::vk::CommandProcessor\*>>(void\*) ./../../buildtools/third\_party/libc++/trunk/include/\_\_thread/thread.h:204:5  

#18 0x55a7e7ac8dea in asan\_thread\_start(void\*) *asan\_rtl*:31

0x5160000c7b80 is located 0 bytes inside of 600-byte region [0x5160000c7b80,0x5160000c7dd8)  

freed by thread T0 (chrome) here:  

#0 0x55a7e7afea9d in operator delete(void\*) *asan\_rtl*:3  

#1 0x7fabff1422c1 in absl::container\_internal::raw\_hash\_set<absl::container\_internal::FlatHashMapPolicy<rx::vk::DescriptorSetDesc, std::\_\_Cr::unique\_ptr<rx::DescriptorSetCache::dsCacheEntry, std::\_\_Cr::default\_delete[rx::DescriptorSetCache::dsCacheEntry](javascript:void(0);)>>, absl::hash\_internal::Hash[rx::vk::DescriptorSetDesc](javascript:void(0);), std::\_\_Cr::equal\_to[rx::vk::DescriptorSetDesc](javascript:void(0);), std::\_\_Cr::allocator<std::\_\_Cr::pair<rx::vk::DescriptorSetDesc const, std::\_\_Cr::unique\_ptr<rx::DescriptorSetCache::dsCacheEntry, std::\_\_Cr::default\_delete[rx::DescriptorSetCache::dsCacheEntry](javascript:void(0);)>>>>::prepare\_insert(unsigned long) ./../../third\_party/abseil-cpp/absl/container/internal/raw\_hash\_set.h:2612:7  

#2 0x7fabff1421bb in std::\_\_Cr::pair<unsigned long, bool> absl::container\_internal::raw\_hash\_set<absl::container\_i

**Additional Comments:**

\*\*Chrome version: \*\* 116.0.5845.42 \*\*Channel: \*\* Not sure

**OS:** Linux

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 2.6 KB)
- [asan.log](attachments/asan.log) (text/plain, 38.3 KB)

## Timeline

### [Deleted User] (2023-08-02)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-08-02)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5129084612575232.

### cl...@chromium.org (2023-08-02)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-08-02)

ClusterFuzz testcase 5129084612575232 appears to be flaky, updating reproducibility label.

### cl...@chromium.org (2023-08-03)

[Empty comment from Monorail migration]

### ts...@chromium.org (2023-08-03)

Looks like CF reproduced something similar but not exactly the same as this stack trace.  Restarting CF job to see if it can do better at finding a regression range.

In the mean time, assigning per renderer/vulkan/OWNERS 

[Monorail components: Internals>GPU>Vulkan]

### [Deleted User] (2023-08-03)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sy...@chromium.org (2023-08-07)

[Empty comment from Monorail migration]

### cc...@google.com (2023-08-07)

I think DynamicDescriptorPool is missing a lock to protect access from multi threads

### gi...@appspot.gserviceaccount.com (2023-08-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/7c69116fbbd8ce4241e5eb11f92845bdfa2e6da9

commit 7c69116fbbd8ce4241e5eb11f92845bdfa2e6da9
Author: Charlie Lao <cclao@google.com>
Date: Tue Aug 08 17:14:47 2023

Vulkan: Fix data race with DynamicDescriptorPool

Right now DynamicDescriptorPool::destroyCachedDescriptorSet can be
called from garbage clean up thread, while simultaneously accessed from
context main thread, and data race will happen and cause bugs. This can
only happen when the buffer is not being suballocated. In this case,
suballocation owns the bufferBlock and bufferBlock gets destroyed when
suballocation is destroyed from garbage collection thread. If buffer is
suballocated, the shared group owns pool which owns bufferBlocks and
they gets destroyed from shared group with the share group lock. This CL
avoids this race problem by release the shared cacheKey when the buffer
is released, while we still had the shared group lock.

Bug: chromium:1469542
Change-Id: Ic1f99e6b6083d63e4efb9c3f408921da62c006ac
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/4761365
Commit-Queue: Charlie Lao <cclao@google.com>
Reviewed-by: Yuxin Hu <yuxinhu@google.com>
Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>

[modify] https://crrev.com/7c69116fbbd8ce4241e5eb11f92845bdfa2e6da9/src/libANGLE/renderer/vulkan/vk_cache_utils.h
[modify] https://crrev.com/7c69116fbbd8ce4241e5eb11f92845bdfa2e6da9/src/tests/gl_tests/TransformFeedbackTest.cpp
[modify] https://crrev.com/7c69116fbbd8ce4241e5eb11f92845bdfa2e6da9/src/tests/gl_tests/UniformBufferTest.cpp
[modify] https://crrev.com/7c69116fbbd8ce4241e5eb11f92845bdfa2e6da9/src/libANGLE/renderer/vulkan/vk_helpers.h
[modify] https://crrev.com/7c69116fbbd8ce4241e5eb11f92845bdfa2e6da9/src/libANGLE/renderer/vulkan/vk_cache_utils.cpp
[modify] https://crrev.com/7c69116fbbd8ce4241e5eb11f92845bdfa2e6da9/src/libANGLE/renderer/vulkan/vk_helpers.cpp
[modify] https://crrev.com/7c69116fbbd8ce4241e5eb11f92845bdfa2e6da9/src/libANGLE/renderer/vulkan/Suballocation.h
[modify] https://crrev.com/7c69116fbbd8ce4241e5eb11f92845bdfa2e6da9/src/libANGLE/renderer/vulkan/TextureVk.cpp
[modify] https://crrev.com/7c69116fbbd8ce4241e5eb11f92845bdfa2e6da9/src/libANGLE/renderer/vulkan/BufferVk.cpp


### cc...@google.com (2023-08-10)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-10)

Dear owner, thanks for fixing this bug. We’ve reopened it because security bugs need Security_Severity and FoundIn labels set, which will enable the bots to request merges to the correct branches ( as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact (security@chromium.org) to arrange to set these labels and then this bug can be marked closed again. Thank you! Severity guidelines: https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues FoundIn guidelines: https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security Thanks for your time! 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2023-08-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/eac93c1d353d0477908e16304c0b843811a08ce6

commit eac93c1d353d0477908e16304c0b843811a08ce6
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Thu Aug 10 20:17:00 2023

Roll ANGLE from ae8a5cfd9195 to 7c69116fbbd8 (1 revision)

https://chromium.googlesource.com/angle/angle.git/+log/ae8a5cfd9195..7c69116fbbd8

2023-08-10 cclao@google.com Vulkan: Fix data race with DynamicDescriptorPool

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/angle-chromium-autoroll
Please CC angle-team@google.com,jonahr@google.com on the revert to ensure that a human
is aware of the problem.

To file a bug in ANGLE: https://bugs.chromium.org/p/angleproject/issues/entry
To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86
Bug: chromium:1469542
Tbr: jonahr@google.com
Change-Id: I0f7eeac833aa719ce1513575a24f313fff16bccc
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4770617
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#1182259}

[modify] https://crrev.com/eac93c1d353d0477908e16304c0b843811a08ce6/DEPS


### pg...@google.com (2023-08-11)

Looks like Clusterfuzz didn't pull through - filling in the labels so this can stay marked as fixed

### pg...@google.com (2023-08-11)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-12)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-12)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-08-12)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-12)

Requesting merge to stable M116 because latest trunk commit (1182259) appears to be after stable branch point (1160321).

Requesting merge to dev M117 because latest trunk commit (1182259) appears to be after dev branch point (1181205).

Merge review required: a commit with DEPS changes was detected.

Merge review required: a commit with DEPS changes was detected.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [116, 117].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-08-13)

Requesting merge to stable M116 because latest trunk commit (1182259) appears to be after stable branch point (1160321).

Requesting merge to dev M117 because latest trunk commit (1182259) appears to be after dev branch point (1181205).

Merge review required: a commit with DEPS changes was detected.

Merge review required: a commit with DEPS changes was detected.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [116, 117].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-08-14)

117 and 116 merges approved, please merge this fix (https://crrev.com/c/4761365) to 117/branch 5938 and 116/branch 5845 at your earliest convenience --ty

### pb...@google.com (2023-08-14)

Your Cl has been already approved for M117 Branch and we are cutting M117 Beta RC tomorrow i.e., Aug-15th, so request  you to get the CL's cherry pick before Noon tomorrow so that we get maximum Beta coverage for the CL please.



### am...@chromium.org (2023-08-14)

in tandem to the above message, please merge to 116 by EOD Thursday, 17 August, so this fix can be included in next week's weekly security refresh 

### am...@chromium.org (2023-08-14)

[Empty comment from Monorail migration]

### am...@google.com (2023-08-16)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-08-16)

Congratulations, Cassidy Kim! The VRP Panel has decided to award you $10,000 for this report of a security bug in the GPU process. Thank you for your efforts and reporting this issue to us -- nice work! 

### gi...@appspot.gserviceaccount.com (2023-08-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/b48983ab8c74d2fcd9ef17c80727affb9e690c53

commit b48983ab8c74d2fcd9ef17c80727affb9e690c53
Author: Charlie Lao <cclao@google.com>
Date: Tue Aug 08 17:14:47 2023

M116: Vulkan: Fix data race with DynamicDescriptorPool

Right now DynamicDescriptorPool::destroyCachedDescriptorSet can be
called from garbage clean up thread, while simultaneously accessed from
context main thread, and data race will happen and cause bugs. This can
only happen when the buffer is not being suballocated. In this case,
suballocation owns the bufferBlock and bufferBlock gets destroyed when
suballocation is destroyed from garbage collection thread. If buffer is
suballocated, the shared group owns pool which owns bufferBlocks and
they gets destroyed from shared group with the share group lock. This CL
avoids this race problem by release the shared cacheKey when the buffer
is released, while we still had the shared group lock.

Bug: chromium:1469542
Change-Id: Ie6235fcfb77dee2a12b2ebde44042c3845fc0aca
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/4790523
Reviewed-by: Yuly Novikov <ynovikov@chromium.org>

[modify] https://crrev.com/b48983ab8c74d2fcd9ef17c80727affb9e690c53/src/libANGLE/renderer/vulkan/vk_cache_utils.h
[modify] https://crrev.com/b48983ab8c74d2fcd9ef17c80727affb9e690c53/src/tests/gl_tests/TransformFeedbackTest.cpp
[modify] https://crrev.com/b48983ab8c74d2fcd9ef17c80727affb9e690c53/src/tests/gl_tests/UniformBufferTest.cpp
[modify] https://crrev.com/b48983ab8c74d2fcd9ef17c80727affb9e690c53/src/libANGLE/renderer/vulkan/vk_helpers.h
[modify] https://crrev.com/b48983ab8c74d2fcd9ef17c80727affb9e690c53/src/libANGLE/renderer/vulkan/vk_cache_utils.cpp
[modify] https://crrev.com/b48983ab8c74d2fcd9ef17c80727affb9e690c53/src/libANGLE/renderer/vulkan/vk_helpers.cpp
[modify] https://crrev.com/b48983ab8c74d2fcd9ef17c80727affb9e690c53/src/libANGLE/renderer/vulkan/Suballocation.h
[modify] https://crrev.com/b48983ab8c74d2fcd9ef17c80727affb9e690c53/src/libANGLE/renderer/vulkan/TextureVk.cpp
[modify] https://crrev.com/b48983ab8c74d2fcd9ef17c80727affb9e690c53/src/libANGLE/renderer/vulkan/BufferVk.cpp


### [Deleted User] (2023-08-17)

LTS Milestone M114

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2023-08-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/1c148a2d6a448b41ed396331a0cf62a30fc3c4d2

commit 1c148a2d6a448b41ed396331a0cf62a30fc3c4d2
Author: Charlie Lao <cclao@google.com>
Date: Tue Aug 08 17:14:47 2023

M117: Vulkan: Fix data race with DynamicDescriptorPool

Right now DynamicDescriptorPool::destroyCachedDescriptorSet can be
called from garbage clean up thread, while simultaneously accessed from
context main thread, and data race will happen and cause bugs. This can
only happen when the buffer is not being suballocated. In this case,
suballocation owns the bufferBlock and bufferBlock gets destroyed when
suballocation is destroyed from garbage collection thread. If buffer is
suballocated, the shared group owns pool which owns bufferBlocks and
they gets destroyed from shared group with the share group lock. This CL
avoids this race problem by release the shared cacheKey when the buffer
is released, while we still had the shared group lock.

Bug: chromium:1469542
Change-Id: Ib492607e266795c3d357c50d4ee6b09f20346ac2
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/4791061
Reviewed-by: Yuly Novikov <ynovikov@chromium.org>

[modify] https://crrev.com/1c148a2d6a448b41ed396331a0cf62a30fc3c4d2/src/libANGLE/renderer/vulkan/vk_cache_utils.h
[modify] https://crrev.com/1c148a2d6a448b41ed396331a0cf62a30fc3c4d2/src/tests/gl_tests/TransformFeedbackTest.cpp
[modify] https://crrev.com/1c148a2d6a448b41ed396331a0cf62a30fc3c4d2/src/tests/gl_tests/UniformBufferTest.cpp
[modify] https://crrev.com/1c148a2d6a448b41ed396331a0cf62a30fc3c4d2/src/libANGLE/renderer/vulkan/vk_helpers.h
[modify] https://crrev.com/1c148a2d6a448b41ed396331a0cf62a30fc3c4d2/src/libANGLE/renderer/vulkan/vk_cache_utils.cpp
[modify] https://crrev.com/1c148a2d6a448b41ed396331a0cf62a30fc3c4d2/src/libANGLE/renderer/vulkan/vk_helpers.cpp
[modify] https://crrev.com/1c148a2d6a448b41ed396331a0cf62a30fc3c4d2/src/libANGLE/renderer/vulkan/Suballocation.h
[modify] https://crrev.com/1c148a2d6a448b41ed396331a0cf62a30fc3c4d2/src/libANGLE/renderer/vulkan/TextureVk.cpp
[modify] https://crrev.com/1c148a2d6a448b41ed396331a0cf62a30fc3c4d2/src/libANGLE/renderer/vulkan/BufferVk.cpp


### am...@google.com (2023-08-18)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-08-18)

[Empty comment from Monorail migration]

### am...@google.com (2023-08-18)

[Empty comment from Monorail migration]

### pg...@google.com (2023-08-22)

[Empty comment from Monorail migration]

### rz...@google.com (2023-08-28)

[Empty comment from Monorail migration]

### rz...@google.com (2023-08-29)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-29)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2023-08-29)

1. https://crrev.com/c/4817006
2. Low, no conflicts
3. 117
4. Yes

### rz...@google.com (2023-08-30)

[Empty comment from Monorail migration]

### gm...@google.com (2023-09-18)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-09-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/26f0b9f8de30f44630e99159c17a64a6165bb4d2

commit 26f0b9f8de30f44630e99159c17a64a6165bb4d2
Author: Charlie Lao <cclao@google.com>
Date: Tue Aug 08 17:14:47 2023

[M114-LTS] Vulkan: Fix data race with DynamicDescriptorPool

Right now DynamicDescriptorPool::destroyCachedDescriptorSet can be
called from garbage clean up thread, while simultaneously accessed from
context main thread, and data race will happen and cause bugs. This can
only happen when the buffer is not being suballocated. In this case,
suballocation owns the bufferBlock and bufferBlock gets destroyed when
suballocation is destroyed from garbage collection thread. If buffer is
suballocated, the shared group owns pool which owns bufferBlocks and
they gets destroyed from shared group with the share group lock. This CL
avoids this race problem by release the shared cacheKey when the buffer
is released, while we still had the shared group lock.

Bug: chromium:1469542
Change-Id: Ic1f99e6b6083d63e4efb9c3f408921da62c006ac
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/4761365
Commit-Queue: Charlie Lao <cclao@google.com>
(cherry picked from commit 7c69116fbbd8ce4241e5eb11f92845bdfa2e6da9)
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/4817006
Reviewed-by: Simon Hangl <simonha@google.com>
Reviewed-by: Charlie Lao <cclao@google.com>

[modify] https://crrev.com/26f0b9f8de30f44630e99159c17a64a6165bb4d2/src/libANGLE/renderer/vulkan/vk_cache_utils.h
[modify] https://crrev.com/26f0b9f8de30f44630e99159c17a64a6165bb4d2/src/tests/gl_tests/TransformFeedbackTest.cpp
[modify] https://crrev.com/26f0b9f8de30f44630e99159c17a64a6165bb4d2/src/libANGLE/renderer/vulkan/vk_helpers.h
[modify] https://crrev.com/26f0b9f8de30f44630e99159c17a64a6165bb4d2/src/tests/gl_tests/UniformBufferTest.cpp
[modify] https://crrev.com/26f0b9f8de30f44630e99159c17a64a6165bb4d2/src/libANGLE/renderer/vulkan/Suballocation.h
[modify] https://crrev.com/26f0b9f8de30f44630e99159c17a64a6165bb4d2/src/libANGLE/renderer/vulkan/vk_cache_utils.cpp
[modify] https://crrev.com/26f0b9f8de30f44630e99159c17a64a6165bb4d2/src/libANGLE/renderer/vulkan/vk_helpers.cpp
[modify] https://crrev.com/26f0b9f8de30f44630e99159c17a64a6165bb4d2/src/libANGLE/renderer/vulkan/TextureVk.cpp
[modify] https://crrev.com/26f0b9f8de30f44630e99159c17a64a6165bb4d2/src/libANGLE/renderer/vulkan/BufferVk.cpp


### rz...@google.com (2023-09-21)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-18)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1469542?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40068543)*
