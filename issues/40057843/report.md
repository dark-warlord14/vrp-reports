# Security: Wild write in angle

| Field | Value |
|-------|-------|
| **Issue ID** | [40057843](https://issues.chromium.org/issues/40057843) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Internals>GPU>ANGLE |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ao...@gmail.com |
| **Assignee** | jm...@chromium.org |
| **Created** | 2021-11-06 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**  

ASan spots a wild write when the attached page is opened.

**VERSION**  

Chrome Version: Tested with 98.0.4694.0 and 97.0.4690.0  

Operating System: Linux, Debian 11.1

**REPRODUCTION CASE**  

Open the attached file. This should reproduce reproduce reliably. The flags "--use-gl=angle --use-angle=swiftshader" may be necessary.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: GPU thread  

Crash State:  

==3662404==ERROR: AddressSanitizer: SEGV on unknown address 0x616100089f96 (pc 0x7ff3594c487b bp 0x7ffe90e1e8a0 sp 0x7ffe90e1e540 T0)  

==3662404==The signal is caused by a WRITE memory access.  

SCARINESS: 30 (wild-addr-write)  

#0 0x7ff3594c487b in operator|= third\_party/angle/src/common/bitset\_utils.h:291:11  

#1 0x7ff3594c487b in setContentDefined third\_party/angle/src/libANGLE/renderer/vulkan/vk\_helpers.cpp:3959:43  

#2 0x7ff3594c487b in onWrite third\_party/angle/src/libANGLE/renderer/vulkan/vk\_helpers.cpp:5847:5  

#3 0x7ff3594c487b in rx::vk::ImageHelper::flushStagedUpdates(rx::ContextVk\*, gl::LevelIndexWrapper<int>, gl::LevelIndexWrapper<int>, unsigned int, unsigned int, angle::BitSetT<16ul, unsig  

ned long, unsigned long>) third\_party/angle/src/libANGLE/renderer/vulkan/vk\_helpers.cpp:6680:17  

#4 0x7ff3594c2139 in rx::vk::ImageHelper::flushSingleSubresourceStagedUpdates(rx::ContextVk\*, gl::LevelIndexWrapper<int>, unsigned int, unsigned int, rx::vk::ClearValuesArray\*, unsigned i  

nt) third\_party/angle/src/libANGLE/renderer/vulkan/vk\_helpers.cpp:6462:12  

#5 0x7ff35938147b in rx::RenderTargetVk::flushStagedUpdates(rx::ContextVk\*, rx::vk::ClearValuesArray\*, unsigned int, unsigned int) third\_party/angle/src/libANGLE/renderer/vulkan/RenderTargetVk.cpp:340:19  

#6 0x7ff359345267 in rx::FramebufferVk::flushColorAttachmentUpdates(gl::Context const\*, bool, unsigned int) third\_party/angle/src/libANGLE/renderer/vulkan/FramebufferVk.cpp  

#7 0x7ff35934593c in rx::FramebufferVk::syncState(gl::Context const\*, unsigned int, angle::BitSetT<28ul, unsigned long, unsigned long> const&, gl::Command) third\_party/angle/src/libANGLE/renderer/vulkan/FramebufferVk.cpp:1910:9  

#8 0x7ff358d672bb in gl::Framebuffer::syncState(gl::Context const\*, unsigned int, gl::Command) const third\_party/angle/src/libANGLE/Framebuffer.cpp:2059:9  

#9 0x7ff358c4e719 in syncDirtyObjects third\_party/angle/src/libANGLE/State.h:1181:9  

#10 0x7ff358c4e719 in syncDirtyObjects third\_party/angle/src/libANGLE/Context.inl.h:107:19  

#11 0x7ff358c4e719 in prepareForDraw third\_party/angle/src/libANGLE/Context.inl.h:117:5  

#12 0x7ff358c4e719 in drawArrays third\_party/angle/src/libANGLE/Context.inl.h:132:5  

#13 0x7ff358c4e719 in GL\_DrawArrays third\_party/angle/src/libGLESv2/entry\_points\_gles\_2\_0\_autogen.cpp:1109:22  

#14 0x55aa9be05a69 in gpu::gles2::GLES2DecoderPassthroughImpl::DoDrawArrays(unsigned int, int, int) gpu/command\_buffer/service/gles2\_cmd\_decoder\_passthrough\_doers.cc:1216:10  

#15 0x55aa9bdd412f in gpu::error::Error gpu::gles2::GLES2DecoderPassthroughImpl::DoCommandsImpl<false>(unsigned int, void const volatile\*, int, int\*) gpu/command\_buffer/service/gles2\_cmd\_decoder\_passthrough.cc:858:20  

#16 0x55aa9c249c95 in gpu::CommandBufferService::Flush(int, gpu::AsyncAPIInterface\*) gpu/command\_buffer/service/command\_buffer\_service.cc:70:18  

#17 0x55aa9c23d78f in gpu::CommandBufferStub::OnAsyncFlush(int, unsigned int, std::\_\_1::vector<gpu::SyncToken, std::\_\_1::allocator[gpu::SyncToken](javascript:void(0);) > const&) gpu/ipc/service/command\_buffer\_stub.cc:500:22  

#18 0x55aa9c23cd39 in gpu::CommandBufferStub::ExecuteDeferredRequest(gpu::mojom::DeferredCommandBufferRequestParams&) gpu/ipc/service/command\_buffer\_stub.cc:152:7  

#19 0x55aa9c250772 in gpu::GpuChannel::ExecuteDeferredRequest(mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);)) gpu/ipc/service/gpu\_channel.cc:666:13  

#20 0x55aa9c25cfbe in Invoke<void (gpu::GpuChannel::\*)(mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);)), base::WeakPtr[gpu::GpuChannel](javascript:void(0);), mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);) > base/bind\_internal.h:533:12  

#21 0x55aa9c25cfbe in void base::internal::InvokeHelper<true, void>::MakeItSo<void (gpu::GpuChannel::\*)(mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);)), base::WeakPtr[gpu::GpuChannel](javascript:void(0);), mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);) >(void (gpu::GpuChannel::\*&&)(mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);)), base::WeakPtr[gpu::GpuChannel](javascript:void(0);)&&, mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);)&&) base/bind\_internal.h:728:5  

#22 0x55aa9ac535f7 in Run base/callback.h:142:12  

#23 0x55aa9ac535f7 in gpu::Scheduler::RunNextTask() gpu/command\_buffer/service/scheduler.cc:685:26  

#24 0x55aa9663b203 in Run base/callback.h:142:12  

#25 0x55aa9663b203 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/task/common/task\_annotator.cc:157:32  

#26 0x55aa96678503 in RunTask<(lambda at ../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:358:29)> base/task/common/task\_annotator.h:73:5  

#27 0x55aa96678503 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence\_manager::LazyNow\*) base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:356:21  

#28 0x55aa96677d17 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:261:30  

#29 0x55aa966790d1 in non-virtual thunk to base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc  

#30 0x55aa965320ea in base::MessagePumpGlib::Run(base::MessagePump::Delegate\*) base/message\_loop/message\_pump\_glib.cc:405:48  

#31 0x55aa9667979b in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:468:12  

#32 0x55aa965b3ee9 in base::RunLoop::Run(base::Location const&) base/run\_loop.cc:140:14  

#33 0x55aaa24d5187 in content::GpuMain(content::MainFunctionParams const&) content/gpu/gpu\_main.cc:401:14  

#34 0x55aa953ee0e4 in content::RunZygote(content::ContentMainDelegate\*) content/app/content\_main\_runner\_impl.cc:615:14  

#35 0x55aa953f2141 in content::ContentMainRunnerImpl::Run(bool) content/app/content\_main\_runner\_impl.cc:1006:10  

#36 0x55aa953eb717 in content::RunContentProcess(content::ContentMainParams const&, content::ContentMainRunner\*) content/app/content\_main.cc:390:36  

#37 0x55aa953ed332 in content::ContentMain(content::ContentMainParams const&) content/app/content\_main.cc:418:10  

#38 0x55aa88475ba5 in ChromeMain chrome/app/chrome\_main.cc:172:12

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: Aki Helin, Solita

## Attachments

- [wild-write-angle.html](attachments/wild-write-angle.html) (text/plain, 3.4 KB)

## Timeline

### [Deleted User] (2021-11-06)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-11-08)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4833129678045184.

### va...@chromium.org (2021-11-08)

[Empty comment from Monorail migration]

[Monorail components: Internals>GPU>Vulkan]

### va...@chromium.org (2021-11-08)

(Not sure about OS-Android. syoussefi@ can you please comment on whether this is exploitable on Android?)
Not updating FoundIn yet, hoping ClusterFuzz will be able to do that (it does repro there).

### jm...@chromium.org (2021-11-08)

[Empty comment from Monorail migration]

[Monorail components: -Internals>GPU>Vulkan Internals>GPU>ANGLE]

### cl...@chromium.org (2021-11-08)

Detailed Report: https://clusterfuzz.com/testcase?key=4833129678045184

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: UNKNOWN WRITE
Crash Address: 0x6151000e2116
Crash State:
  rx::vk::ImageHelper::flushStagedUpdates
  rx::vk::ImageHelper::flushSingleSubresourceStagedUpdates
  rx::RenderTargetVk::flushStagedUpdates
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=816056:816058

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=4833129678045184

The reproduce tool requires a ClusterFuzz source checkout. To prepare one, run:

git clone https://github.com/google/clusterfuzz && cd clusterfuzz && git checkout tags/reproduce-tool-stable

To reproduce this issue, run:

./reproduce.sh -t https://clusterfuzz.com/testcase-detail/4833129678045184 -b /path/to/build

Please use the GN arguments provided in this report when building the binary. If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### sy...@chromium.org (2021-11-09)

I produced a minimal repro here: https://chromium-review.googlesource.com/c/angle/angle/+/3268492

I diagnosed this to the following:

- In the first draw call, the mutable texture's image is allocated at base level, and is sampled from.
- The mutable texture's base level is changed to 0
- The mutable texture's filtering is changed to mipmap
  * This makes the texture incomplete. State::updateActiveTextureStateOnSync removes the texture from the list of textures to sync
- The framebuffer is attached to mutable texture's level 0
- The second draw doesn't call TextureVk::syncState on the mutable texture, because it's incomplete. Its image remains allocated at level 1
- The draw call attempts to draw to level 0 of the texture, which is not within the allocated levels in its image

Not sure yet what's the best way to deal with this, should the front-end sync incomplete textures anyway if they are bound to the framebuffer? Should TextureVk::getAttachmentRenderTarget() effectively do syncState()?

### jm...@chromium.org (2021-11-09)

Yes, TextureVk::getAttachmentRenderTarget should flush out any necessary state changes using common code. If you need me to help you can reassign to me though I'm out most of today.

### gi...@appspot.gserviceaccount.com (2021-11-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/517ff220043348f1adfeeaecfb9d6ce5d2a1b576

commit 517ff220043348f1adfeeaecfb9d6ce5d2a1b576
Author: Shahbaz Youssefi <syoussefi@chromium.org>
Date: Tue Nov 09 04:57:16 2021

Add test for texture state change bug

Bug: chromium:1267624
Change-Id: I270e54921d40a2d139afdc78c90ab05164cbfabf
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3268492
Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>
Commit-Queue: Shahbaz Youssefi <syoussefi@chromium.org>

[modify] https://crrev.com/517ff220043348f1adfeeaecfb9d6ce5d2a1b576/src/tests/gl_tests/StateChangeTest.cpp
[modify] https://crrev.com/517ff220043348f1adfeeaecfb9d6ce5d2a1b576/src/tests/angle_end2end_tests_expectations.txt


### sy...@chromium.org (2021-11-09)

> If you need me to help you can reassign to me though I'm out most of today.

Thanks I appreciate it. That change would probably also fix anglebug.com/6014 by allowing https://chromium-review.googlesource.com/c/angle/angle/+/2915764 to be reverted (even though I generally like that change)

### [Deleted User] (2021-11-09)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-11-09)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jm...@chromium.org (2021-11-09)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-11-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/91d4d4d320061e29c6b8f99d85df02c1384734c2

commit 91d4d4d320061e29c6b8f99d85df02c1384734c2
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Tue Nov 09 19:33:36 2021

Roll ANGLE from 67a8cf07a740 to d3e677167124 (5 revisions)

https://chromium.googlesource.com/angle/angle.git/+log/67a8cf07a740..d3e677167124

2021-11-09 j.vigil@samsung.com EGL: EGL_KHR_lock_surface3
2021-11-09 sdefresne@chromium.org [ios] Remove support for building with Xcode clang
2021-11-09 syoussefi@chromium.org Fix invalidation of GL_FRAMEBUFFER invalidating READ FBO
2021-11-09 syoussefi@chromium.org Add test for texture state change bug
2021-11-09 syoussefi@chromium.org Vulkan: Fix deferred clears vs invalidate

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/angle-chromium-autoroll
Please CC jmadill@google.com on the revert to ensure that a human
is aware of the problem.

To file a bug in ANGLE: https://bugs.chromium.org/p/angleproject/issues/entry
To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86
Bug: chromium:1266466,chromium:1267424,chromium:1267624
Tbr: jmadill@google.com
Test: Test: angle_end2end_test --gtest_filter=EGLLockSurface3Test
Change-Id: I611b96a77dedf1a56353fa41bd31aa2806c3ea3d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3271112
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#939953}

[modify] https://crrev.com/91d4d4d320061e29c6b8f99d85df02c1384734c2/DEPS


### gi...@appspot.gserviceaccount.com (2021-11-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/0fcad6260a3e3943fb84657a3a7f488d1e155fb7

commit 0fcad6260a3e3943fb84657a3a7f488d1e155fb7
Author: Jamie Madill <jmadill@chromium.org>
Date: Tue Nov 09 19:02:08 2021

Vulkan: Fix edge case with changing base level.

Bug: chromium:1267624
Change-Id: I36b983fdbbb258454215abe827837517df5a5aff
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3270971
Commit-Queue: Jamie Madill <jmadill@chromium.org>
Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>

[modify] https://crrev.com/0fcad6260a3e3943fb84657a3a7f488d1e155fb7/src/libANGLE/renderer/vulkan/vk_caps_utils.cpp
[modify] https://crrev.com/0fcad6260a3e3943fb84657a3a7f488d1e155fb7/src/tests/angle_end2end_tests_expectations.txt
[modify] https://crrev.com/0fcad6260a3e3943fb84657a3a7f488d1e155fb7/src/libANGLE/renderer/vulkan/TextureVk.h
[modify] https://crrev.com/0fcad6260a3e3943fb84657a3a7f488d1e155fb7/src/libANGLE/renderer/vulkan/TextureVk.cpp


### gi...@appspot.gserviceaccount.com (2021-11-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/6740dab9fbc87cf66cdaff5548adc31db1616049

commit 6740dab9fbc87cf66cdaff5548adc31db1616049
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Wed Nov 10 17:34:54 2021

Roll ANGLE from 6e6947e68544 to 0fcad6260a3e (3 revisions)

https://chromium.googlesource.com/angle/angle.git/+log/6e6947e68544..0fcad6260a3e

2021-11-10 jmadill@chromium.org Vulkan: Fix edge case with changing base level.
2021-11-10 jonahr@google.com Reland "Metal: Reintroduce GPU power preference selection code."
2021-11-10 bsheedy@chromium.org Unskip RenderSolidColor test

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/angle-chromium-autoroll
Please CC jmadill@google.com on the revert to ensure that a human
is aware of the problem.

To file a bug in ANGLE: https://bugs.chromium.org/p/angleproject/issues/entry
To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86
Bug: chromium:1063962,chromium:1267624
Tbr: jmadill@google.com
Change-Id: I4a709a4783cc410b94f4cc411a7c1e4a129cf9b9
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3272336
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#940373}

[modify] https://crrev.com/6740dab9fbc87cf66cdaff5548adc31db1616049/DEPS


### jm...@chromium.org (2021-11-10)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-11-11)

ClusterFuzz testcase 4833129678045184 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=940359:940375

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### [Deleted User] (2021-11-12)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-12)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-12)

Requesting merge to dev M97 because latest trunk commit (940373) appears to be after dev branch point (938553).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-11-12)

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

### jm...@chromium.org (2021-11-12)

1. wild write in gpu process
2. https://chromium-review.googlesource.com/c/angle/angle/+/3270971
3. yes
4. no

### am...@chromium.org (2021-11-16)

Merge approved to M97, please confirm there are no stability issues or other concerns in Canary and please merge to fix to branch 4692 at your earliest convenience. Thanks! 

### gi...@appspot.gserviceaccount.com (2021-11-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/f4933235fb2c03b1d69f95624e97d159d1c78a1a

commit f4933235fb2c03b1d69f95624e97d159d1c78a1a
Author: Jamie Madill <jmadill@chromium.org>
Date: Tue Nov 09 19:02:08 2021

Vulkan: Fix edge case with changing base level.

Bug: chromium:1267624
Change-Id: I36b983fdbbb258454215abe827837517df5a5aff
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3270971
Commit-Queue: Jamie Madill <jmadill@chromium.org>
Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>
(cherry picked from commit 0fcad6260a3e3943fb84657a3a7f488d1e155fb7)
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3285444
Reviewed-by: Jamie Madill <jmadill@chromium.org>

[modify] https://crrev.com/f4933235fb2c03b1d69f95624e97d159d1c78a1a/src/libANGLE/renderer/vulkan/vk_caps_utils.cpp
[modify] https://crrev.com/f4933235fb2c03b1d69f95624e97d159d1c78a1a/src/libANGLE/renderer/vulkan/TextureVk.h
[modify] https://crrev.com/f4933235fb2c03b1d69f95624e97d159d1c78a1a/src/libANGLE/renderer/vulkan/TextureVk.cpp


### am...@google.com (2021-11-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-11-17)

Congratulations, Aki and Solita! The VRP Panel has decided to award you $5000 for this report. Nice work! 

### ao...@gmail.com (2021-11-17)

Awesome! Thanks :)

### am...@google.com (2021-11-18)

[Empty comment from Monorail migration]

### gm...@google.com (2022-01-12)

[Empty comment from Monorail migration]

### rz...@google.com (2022-02-01)

[Empty comment from Monorail migration]

### rz...@google.com (2022-02-01)

[Empty comment from Monorail migration]

### rz...@google.com (2022-02-04)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-04)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2022-02-04)

1. Number of CLs needed for this fix and links to them.
1, https://crrev.com/c/3427423

2. Level of complexity (High, Medium, Low - Explain)
Low, conflicts with different parameter for the initImageViews call

3. Has this been merged to a stable release? beta release?
97

4. Overall Recommendation (Yes, No)
Yes

Note: CI doesn't work for M96 branch, I built it locally and ran the unit_tests.

### gm...@google.com (2022-02-04)

ranzoni@google.com I need a bit more info about this one before I can approve. Let's talk on Monday.

### gm...@google.com (2022-02-07)

Update: angle unit tests are passing locally but we will check with angle maintainers. 

### gi...@appspot.gserviceaccount.com (2022-02-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/d1ee713ce6c5a29c4e37b14e28d1fef79d370095

commit d1ee713ce6c5a29c4e37b14e28d1fef79d370095
Author: Jamie Madill <jmadill@chromium.org>
Date: Tue Nov 09 19:02:08 2021

[M96-LTS] Vulkan: Fix edge case with changing base level.

M96 merge issues:
  TextureVk.cpp:
    conflict in initImageViews call, the last parameter is layerCount on
    M96, getImageViewLayerCount() on main
  angle_end2end_tests_expectations.txt:
    M96 doesn't contain the removed line from the original CL

Bug: chromium:1267624
Change-Id: I36b983fdbbb258454215abe827837517df5a5aff
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3270971
Commit-Queue: Jamie Madill <jmadill@chromium.org>
(cherry picked from commit 0fcad6260a3e3943fb84657a3a7f488d1e155fb7)
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3427423
Reviewed-by: Jamie Madill <jmadill@chromium.org>

[modify] https://crrev.com/d1ee713ce6c5a29c4e37b14e28d1fef79d370095/src/libANGLE/renderer/vulkan/vk_caps_utils.cpp
[modify] https://crrev.com/d1ee713ce6c5a29c4e37b14e28d1fef79d370095/src/libANGLE/renderer/vulkan/TextureVk.h
[modify] https://crrev.com/d1ee713ce6c5a29c4e37b14e28d1fef79d370095/src/libANGLE/renderer/vulkan/TextureVk.cpp


### gm...@google.com (2022-02-07)

[Empty comment from Monorail migration]

### rz...@google.com (2022-02-07)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-16)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1267624?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-03-12)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057843)*
