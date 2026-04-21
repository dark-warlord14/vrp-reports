# Security: WebGL Texture RenderTarget Vulkan backend UAF

| Field | Value |
|-------|-------|
| **Issue ID** | [40942112](https://issues.chromium.org/issues/40942112) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU>ANGLE |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | d8...@gmail.com |
| **Assignee** | sy...@chromium.org |
| **Created** | 2023-11-13 |
| **Bounty** | $15,000.00 |

## Description




When angle try to copy texture to image2d ( copyTex2image2D ), it will redefine the texture read render, and normal circumstance chrome will not allow render target and source texture is the same


This validation only work under WebGL context:
https://source.chromium.org/chromium/chromium/src/+/main:third_party/angle/src/libANGLE/validationES.cpp;l=4378;drc=125dea0015c8b18e70d42e249437c3e49fe18ae1;bpv=0;bpt=1


A compromised renderer can create a context not valid for WebGL and bypass the check thus allow a texture that is currently bound for rendering is also attached to the framebuffer that is currently bound as the target for rendering and trigger this UAF potentially turn into sandbox escape.



And the rendertarget is deleted:
https://source.chromium.org/chromium/chromium/src/+/main:third_party/angle/src/libANGLE/renderer/vulkan/TextureVk.cpp;l=3739;drc=125dea0015c8b18e70d42e249437c3e49fe18ae1

But when created, the pointer of rendertarget has been cached at:
https://source.chromium.org/chromium/chromium/src/+/main:third_party/angle/src/libANGLE/renderer/RenderTargetCache.h;l=166;drc=125dea0015c8b18e70d42e249437c3e49fe18ae1

And later being reuse at:
https://source.chromium.org/chromium/chromium/src/+/main:third_party/angle/src/libANGLE/renderer/vulkan/FramebufferVk.cpp;l=993

About exploitability:
I just do a quick check and seems to me that between the freed memory and reuse there is a windows of chance the freed memory can be replaced by attacker controlled here:


https://source.chromium.org/chromium/chromium/src/+/main:third_party/angle/src/libANGLE/renderer/vulkan/TextureVk.cpp;l=1150


 because angle will wait until command buffer is full ( or some other conditions ) and it will flush all commands to the GPU, it mean that attacker can prepare as many commands as he want and trigger this code path:

Per my test, i'm able to trigger some allocation in between :

https://source.chromium.org/chromium/chromium/src/+/main:third_party/angle/src/libANGLE/renderer/vulkan/SecondaryCommandBuffer.cpp;l=178

Reproduce by patching chrome to turn WebGL context to false and run with command:
./out/asan/chrome --user-data-dir=/tmp/c2  --use-angle=vulkan http://127.0.0.1:8000/test3.html


## Attachments

- [test3.html](attachments/test3.html) (text/plain, 1.9 KB)
- [asan.log](attachments/asan.log) (text/plain, 27.3 KB)
- deleted (application/octet-stream, 0 B)
- [chrome.patch](attachments/chrome.patch) (text/x-diff, 1.1 KB)

## Timeline

### d8...@gmail.com (2023-11-13)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-13)

[Empty comment from Monorail migration]

### dr...@chromium.org (2023-11-13)

I get a slightly different stack trace, but still some memory corruption in M119. This is memory corruption in an unsandboxed process (GPU process is not sandboxed on all platforms), but assumes a compromised renderer. So assigning High Severity. Assigning to some third_party/angle OWNERS for further investigation.


My stack trace, for posterity:

Received signal 11 SI_KERNEL000000000000
 Possibly a General Protection Fault, can be due to a non-canonical address dereference. See "Intel 64 and IA-32 Architectures Software Developer’s Manual", Volume 1, Section 3.3.7.1.
#0 0x7fb64dbac70c base::debug::CollectStackTrace()
#1 0x7fb64db5d08a base::debug::StackTrace::StackTrace()
#2 0x7fb64db5d045 base::debug::StackTrace::StackTrace()
#3 0x7fb64dbac043 base::debug::(anonymous namespace)::StackDumpSignalHandler()
    #0 0x7fb5fda8d510 in __GI___sigaction :?
#5 0x7fb5e016976c <unknown>
#6 0x7fb5e014b4ec <unknown>
#7 0x7fb5e01e559f <unknown>
#8 0x7fb5e0191933 <unknown>
#9 0x7fb5e028e892 <unknown>
#10 0x7fb5e028e5b9 <unknown>
#11 0x7fb5e06cbfa3 <unknown>
#12 0x7fb5e04ff29e <unknown>
#13 0x7fb5e0042891 <unknown>
#14 0x7fb5e00d512a <unknown>
#15 0x7fb63e76c641 gl::GLApiBase::glCopyTexImage2DFn()
#16 0x7fb5fa19ead2 gpu::gles2::GLES2DecoderPassthroughImpl::DoCopyTexImage2D()
#17 0x7fb5fa1d97d7 gpu::gles2::GLES2DecoderPassthroughImpl::HandleCopyTexImage2D()
#18 0x7fb5fa179c85 gpu::gles2::GLES2DecoderPassthroughImpl::DoCommandsImpl<>()
#19 0x7fb5fa16b485 gpu::gles2::GLES2DecoderPassthroughImpl::DoCommands()
#20 0x7fb63f2c3756 gpu::CommandBufferService::Flush()
#21 0x7fb5fd93a1da gpu::CommandBufferStub::OnAsyncFlush()
#22 0x7fb5fd939bca gpu::CommandBufferStub::ExecuteDeferredRequest()
#23 0x7fb5fd962d10 gpu::GpuChannel::ExecuteDeferredRequest()
#24 0x7fb5fd97a9ec base::internal::FunctorTraits<>::Invoke<>()
#25 0x7fb5fd97a8d9 base::internal::InvokeHelper<>::MakeItSo<>()
#26 0x7fb5fd97a82d base::internal::Invoker<>::RunImpl<>()
#27 0x7fb5fd97a7a7 base::internal::Invoker<>::RunOnce()
#28 0x7fb63f2dc084 base::OnceCallback<>::Run()
#29 0x7fb63f2fc22c gpu::SchedulerDfs::ExecuteSequence()
#30 0x7fb63f2fad29 gpu::SchedulerDfs::RunNextTask()
#31 0x7fb63f30e9fa base::internal::FunctorTraits<>::Invoke<>()
#32 0x7fb63f30e96c base::internal::InvokeHelper<>::MakeItSo<>()
#33 0x7fb63f30e8fd base::internal::Invoker<>::RunImpl<>()
#34 0x7fb63f30e887 base::internal::Invoker<>::RunOnce()
#35 0x7fb64d818324 base::OnceCallback<>::Run()
#36 0x7fb64d9f9c83 base::TaskAnnotator::RunTaskImpl()
#37 0x7fb64da633f0 base::TaskAnnotator::RunTask<>()
#38 0x7fb64da62e41 base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl()
#39 0x7fb64da62370 base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()
#40 0x7fb64da63113 base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()
#41 0x7fb64dbe74e5 base::MessagePumpGlib::Run()
#42 0x7fb64da63acc base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run()
#43 0x7fb64d96f19b base::RunLoop::Run()
#44 0x7fb6436d9562 content::GpuMain()
#45 0x7fb648391a86 content::RunZygote()
#46 0x7fb6483922c8 content::RunOtherNamedProcessTypeMain()
#47 0x7fb6483936a7 content::ContentMainRunnerImpl::Run()
#48 0x7fb64838fd5a content::RunContentProcess()
#49 0x7fb6483903c6 content::ContentMain()
#50 0x55ae03035f4d ChromeMain
#51 0x55ae03035c72 main
    #1 0x7fb5fda786ca in __libc_start_call_main ./csu/../sysdeps/nptl/libc_start_call_main.h:58:16
#53 0x7fb5fda78785 __libc_start_main
#54 0x55ae03035b8a _start


[Monorail components: Internals>GPU>ANGLE]

### [Deleted User] (2023-11-13)

[Empty comment from Monorail migration]

### ad...@google.com (2023-11-13)

(I am a bot: this is an auto-cc on a security bug)

### [Deleted User] (2023-11-14)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-11-27)

geofflang: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### an...@chromium.org (2023-11-28)

[security shepherd]: Hey geofflang@, just following up on the status of this bug. Are you able to take a look or is there someone else you can pass this on to? Thanks!

### sy...@chromium.org (2023-12-05)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-05)

[Empty comment from Monorail migration]

### ad...@google.com (2023-12-05)

(I am a bot: this is an auto-cc on a security bug)

### [Deleted User] (2023-12-06)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-06)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2023-12-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/b8ca8de438417fefeb821d184322b26cb5d56a2c

commit b8ca8de438417fefeb821d184322b26cb5d56a2c
Author: Shahbaz Youssefi <syoussefi@chromium.org>
Date: Tue Dec 05 18:36:53 2023

Vulkan: Don't crash when glCopyTexImage2D redefines itself

The Vulkan backend marks a level being redefined as such before doing
the copy.  If a single-level texture was being redefined, it releases it
so it can be immediately reallocated.  If the source of the copy is the
same texture, this causes a crash.

This can be properly supported by using a temp image to do the copy, but
that is not implemented in this change.

Bug: chromium:1501798
Change-Id: I9dde99aa0b88bc7d5f582ff15772f70b36f424e0
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/5089150
Reviewed-by: Charlie Lao <cclao@google.com>
Commit-Queue: Shahbaz Youssefi <syoussefi@chromium.org>

[modify] https://crrev.com/b8ca8de438417fefeb821d184322b26cb5d56a2c/src/tests/gl_tests/CopyTexImageTest.cpp
[modify] https://crrev.com/b8ca8de438417fefeb821d184322b26cb5d56a2c/src/tests/angle_end2end_tests_expectations.txt
[modify] https://crrev.com/b8ca8de438417fefeb821d184322b26cb5d56a2c/src/libANGLE/renderer/vulkan/TextureVk.cpp


### sy...@chromium.org (2023-12-07)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-12-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/29c738339311efd06b3fd7c83439cd8747f49295

commit 29c738339311efd06b3fd7c83439cd8747f49295
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Thu Dec 07 22:24:44 2023

Roll ANGLE from 8dbdd57cbc20 to b8ca8de43841 (1 revision)

https://chromium.googlesource.com/angle/angle.git/+log/8dbdd57cbc20..b8ca8de43841

2023-12-07 syoussefi@chromium.org Vulkan: Don't crash when glCopyTexImage2D redefines itself

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/angle-chromium-autoroll
Please CC abdolrashidi@google.com,angle-team@google.com on the revert to ensure that a human
is aware of the problem.

To file a bug in ANGLE: https://bugs.chromium.org/p/angleproject/issues/entry
To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://issues.skia.org/issues/new?component=1389291&template=1850622

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86
Bug: chromium:1501798
Tbr: abdolrashidi@google.com
Change-Id: I7499d81aa4c4133c5c9455de62b918606951924f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5100382
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#1234738}

[modify] https://crrev.com/29c738339311efd06b3fd7c83439cd8747f49295/DEPS
[modify] https://crrev.com/29c738339311efd06b3fd7c83439cd8747f49295/third_party/angle


### [Deleted User] (2023-12-08)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-08)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-08)

Requesting merge to stable M120 because latest trunk commit (1234738) appears to be after stable branch point (1217362).

Requesting merge to beta M121 because latest trunk commit (1234738) appears to be after beta branch point (1233107).

Merge review required: a commit with DEPS changes was detected.

Merge review required: a commit with DEPS changes was detected.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [120, 121].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-12-09)

Requesting merge to stable M120 because latest trunk commit (1234738) appears to be after stable branch point (1217362).

Requesting merge to beta M121 because latest trunk commit (1234738) appears to be after beta branch point (1233107).

Merge review required: a commit with DEPS changes was detected.

Merge review required: a commit with DEPS changes was detected.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [120, 121].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-12-10)

Requesting merge to stable M120 because latest trunk commit (1234738) appears to be after stable branch point (1217362).

Requesting merge to beta M121 because latest trunk commit (1234738) appears to be after beta branch point (1233107).

Merge review required: a commit with DEPS changes was detected.

Merge review required: a commit with DEPS changes was detected.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [120, 121].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-12-11)

Requesting merge to stable M120 because latest trunk commit (1234738) appears to be after stable branch point (1217362).

Requesting merge to beta M121 because latest trunk commit (1234738) appears to be after beta branch point (1233107).

Merge review required: a commit with DEPS changes was detected.

Merge review required: a commit with DEPS changes was detected.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [120, 121].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-12-11)

M121 and M120 merges approved for https://crrev.com/c/5089150
While I have checked stability and perf data and see no issues, since we are going into a release freeze, please confirm there are no stability or other risks/ concerns with backmerging this fix. 
Once confirming, please merge this fix to M121 Beta / branch 6167 at soonest (by EOD Tuesday 12 December) so this fix can be included in the next M121 Beta. 
Please merge this fix to M120 Stable / branch 6099 at your convenience so this fix can be included in the first Stable update following the forthcoming release freeze. 

### go...@google.com (2023-12-12)

Please merge your change to M121 before 2:00 PM PT today so we can take it in for tomorrow's beta (Last Beta release before holiday freeze).

Branch details: https://chromiumdash.appspot.com/branches

### am...@google.com (2023-12-14)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-12-14)

Congratulations! The Chrome VRP Panel has decided to award you $15,000 for this high-quality report of memory corruption in the GPU process. A member of our p2p-vrp@ finance team will be in touch with you soon to arrange payment. 
In the meantime, please let us know the name / handle or other identifier you would like us to use in acknowledging you for this finding. 
Thank you for your efforts and reporting this issue to us -- great work! 

### d8...@gmail.com (2023-12-14)

Thanks team and Amy!
 Please help add credit to: Toan (suto) Pham of Qrious Secure.

### [Deleted User] (2023-12-15)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2023-12-15)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-12-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/87ab2b373e8b0dd2f176a3890b754ad75e3d6c20

commit 87ab2b373e8b0dd2f176a3890b754ad75e3d6c20
Author: Shahbaz Youssefi <syoussefi@chromium.org>
Date: Tue Dec 05 18:36:53 2023

M121: Vulkan: Don't crash when glCopyTexImage2D redefines itself

The Vulkan backend marks a level being redefined as such before doing
the copy.  If a single-level texture was being redefined, it releases it
so it can be immediately reallocated.  If the source of the copy is the
same texture, this causes a crash.

This can be properly supported by using a temp image to do the copy, but
that is not implemented in this change.

Bug: chromium:1501798
Change-Id: Iab57055bdf5908357f30289f3aa62cce0fd31d95
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/5143831
Reviewed-by: Cody Northrop <cnorthrop@google.com>

[modify] https://crrev.com/87ab2b373e8b0dd2f176a3890b754ad75e3d6c20/src/tests/gl_tests/CopyTexImageTest.cpp
[modify] https://crrev.com/87ab2b373e8b0dd2f176a3890b754ad75e3d6c20/src/tests/angle_end2end_tests_expectations.txt
[modify] https://crrev.com/87ab2b373e8b0dd2f176a3890b754ad75e3d6c20/src/libANGLE/renderer/vulkan/TextureVk.cpp


### gi...@appspot.gserviceaccount.com (2023-12-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/01f439363dcbc21ff2012fb1feb542d275261b3b

commit 01f439363dcbc21ff2012fb1feb542d275261b3b
Author: Shahbaz Youssefi <syoussefi@chromium.org>
Date: Tue Dec 05 18:36:53 2023

M120: Vulkan: Don't crash when glCopyTexImage2D redefines itself

The Vulkan backend marks a level being redefined as such before doing
the copy.  If a single-level texture was being redefined, it releases it
so it can be immediately reallocated.  If the source of the copy is the
same texture, this causes a crash.

This can be properly supported by using a temp image to do the copy, but
that is not implemented in this change.

Bug: chromium:1501798
Change-Id: I3a902b1e9eec41afd385d9c75a8c95dc986070a8
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/5143829
Reviewed-by: Cody Northrop <cnorthrop@google.com>

[modify] https://crrev.com/01f439363dcbc21ff2012fb1feb542d275261b3b/src/tests/gl_tests/CopyTexImageTest.cpp
[modify] https://crrev.com/01f439363dcbc21ff2012fb1feb542d275261b3b/src/tests/angle_end2end_tests_expectations.txt
[modify] https://crrev.com/01f439363dcbc21ff2012fb1feb542d275261b3b/src/libANGLE/renderer/vulkan/TextureVk.cpp


### [Deleted User] (2023-12-21)

LTS Milestone M114

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2024-01-03)

[Empty comment from Monorail migration]

### pg...@google.com (2024-01-04)

[Empty comment from Monorail migration]

### pg...@google.com (2024-01-04)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### sy...@chromium.org (2024-01-12)

> 1. Was this issue a regression for the milestone it was found in?
> 2. Is this issue related to a change or feature merged after the latest LTS Milestone?

The bug is quite old (at least a few years), so merging to LTS makes sense.

### rz...@google.com (2024-01-16)

[Empty comment from Monorail migration]

### rz...@google.com (2024-01-17)

1. Just https://crrev.com/c/5200755
2. Low, only conflicts in comments
3. 120, 121
4. Yes

### rz...@google.com (2024-01-22)

[Empty comment from Monorail migration]

### rz...@google.com (2024-01-22)

[Empty comment from Monorail migration]

### na...@google.com (2024-01-22)

Merge approved for LTS-114 

### na...@google.com (2024-01-22)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2024-01-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/3f6ffdb286bdfcb8be570714201dca6e1c9f2027

commit 3f6ffdb286bdfcb8be570714201dca6e1c9f2027
Author: Shahbaz Youssefi <syoussefi@chromium.org>
Date: Tue Dec 05 18:36:53 2023

[M114-LTS] Vulkan: Don't crash when glCopyTexImage2D redefines itself

M114 merge issues:
  renderer/vulkan/TextureVk.cpp:
    Confliciting comments

The Vulkan backend marks a level being redefined as such before doing
the copy.  If a single-level texture was being redefined, it releases it
so it can be immediately reallocated.  If the source of the copy is the
same texture, this causes a crash.

This can be properly supported by using a temp image to do the copy, but
that is not implemented in this change.

Bug: chromium:1501798
Change-Id: I9dde99aa0b88bc7d5f582ff15772f70b36f424e0
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/5089150
Commit-Queue: Shahbaz Youssefi <syoussefi@chromium.org>
(cherry picked from commit b8ca8de438417fefeb821d184322b26cb5d56a2c)
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/5200755
Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>

[modify] https://crrev.com/3f6ffdb286bdfcb8be570714201dca6e1c9f2027/src/tests/gl_tests/CopyTexImageTest.cpp
[modify] https://crrev.com/3f6ffdb286bdfcb8be570714201dca6e1c9f2027/src/tests/angle_end2end_tests_expectations.txt
[modify] https://crrev.com/3f6ffdb286bdfcb8be570714201dca6e1c9f2027/src/libANGLE/renderer/vulkan/TextureVk.cpp


### rz...@google.com (2024-01-23)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-23)

This issue was migrated from crbug.com/chromium/1501798?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-03-15)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### am...@chromium.org (2024-03-16)

The patch file from c#2 seems to have been deleted, restoring it here

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40942112)*
