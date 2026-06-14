# libANGLE heap-buffer-overflow triggered by WebGL2 on Windows 10

| Field | Value |
|-------|-------|
| **Issue ID** | [40094331](https://issues.chromium.org/issues/40094331) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>GPU>ANGLE |
| **Platforms** | Windows |
| **Reporter** | ta...@gmail.com |
| **Assignee** | jm...@chromium.org |
| **Created** | 2019-03-19 |
| **Bounty** | $1,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36

Steps to reproduce the problem:
To reproduce the problem, load the attached HTML with Chromium ASAN build on Windows 10.

ASAN log:
=================================================================
==3572==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x11fe08bce3a3 at pc 0x7ff69bf0515a bp 0x003fb85fa640 sp 0x003fb85fa688
READ of size 3 at 0x11fe08bce3a3 thread T0
    #0 0x7ff69bf05183 in __asan_memcpy C:\b\rr\tmpapv6or\w\src\third_party\llvm\projects\compiler-rt\lib\asan\asan_interceptors_memintrinsics.cc:22
    #1 0x7ffbf29bc513 in rx::CopyNativeVertexData<signed char,3,4,1>(unsigned char const *,unsigned __int64,unsigned __int64,unsigned char *) C:\b\swarming\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\copyvertex.inc:43:9
    #2 0x7ffbf29ac8f2 in rx::VertexBuffer11::storeVertexAttributes(class gl::Context const *,struct gl::VertexAttribute const &,class gl::VertexBinding const &,enum gl::VertexAttribType,int,unsigned __int64,int,unsigned int,unsigned char const *) C:\b\swarming\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\d3d\d3d11\VertexBuffer11.cpp:129:5
    #3 0x7ffbf2c8bc17 in rx::StreamingVertexBufferInterface::storeDynamicAttribute(class gl::Context const *,struct gl::VertexAttribute const &,class gl::VertexBinding const &,enum gl::VertexAttribType,int,unsigned __int64,int,unsigned int *,unsigned char const *) C:\b\swarming\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\d3d\VertexBuffer.cpp:187:5
    #4 0x7ffbf29d2e03 in rx::VertexDataManager::storeDynamicAttrib(class gl::Context const *,struct rx::TranslatedAttribute *,int,unsigned __int64,int) C:\b\swarming\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\d3d\VertexDataManager.cpp:544:5
    #5 0x7ffbf29d20d8 in rx::VertexDataManager::storeDynamicAttribs(class gl::Context const *,class std::vector<struct rx::TranslatedAttribute,class std::allocator<struct rx::TranslatedAttribute> > *,class angle::BitSetT<16,unsigned __int64,unsigned __int64> const &,int,unsigned __int64,int) C:\b\swarming\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\d3d\VertexDataManager.cpp:436:9
    #6 0x7ffbf2c52898 in rx::VertexArray11::updateDynamicAttribs(class gl::Context const *,class rx::VertexDataManager *,int,int,enum gl::DrawElementsType,void const *,int,int,class angle::BitSetT<16,unsigned __int64,unsigned __int64> const &) C:\b\swarming\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\d3d\d3d11\VertexArray11.cpp:317:5
    #7 0x7ffbf2c51b85 in rx::VertexArray11::syncStateForDraw(class gl::Context const *,int,int,enum gl::DrawElementsType,void const *,int,int) C:\b\swarming\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\d3d\d3d11\VertexArray11.cpp:160:13
    #8 0x7ffbf28a615a in rx::StateManager11::updateState(class gl::Context const *,enum gl::PrimitiveMode,int,int,enum gl::DrawElementsType,void const *,int,int) C:\b\swarming\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\d3d\d3d11\StateManager11.cpp:2164:5
    #9 0x7ffbf29be83f in rx::Context11::drawArraysInstanced(class gl::Context const *,enum gl::PrimitiveMode,int,int,int) C:\b\swarming\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\d3d\d3d11\Context11.cpp:262:5
    #10 0x7ffbf2551148 in gl::Context::drawArraysInstanced(enum gl::PrimitiveMode,int,int,int) C:\b\swarming\w\ir\cache\builder\src\third_party\angle\src\libANGLE\Context.cpp:2184:5
    #11 0x7ffbf2291650 in gl::DrawArraysInstanced(unsigned int,int,int,int) C:\b\swarming\w\ir\cache\builder\src\third_party\angle\src\libGLESv2\entry_points_gles_3_0_autogen.cpp:464:22
    #12 0x7ffc0432e9bd in gpu::gles2::GLES2DecoderPassthroughImpl::DoDrawArraysInstancedANGLE(unsigned int,int,int,int) C:\b\swarming\w\ir\cache\builder\src\gpu\command_buffer\service\gles2_cmd_decoder_passthrough_doers.cc:4233:10
    #13 0x7ffc033220c7 in gpu::gles2::GLES2DecoderPassthroughImpl::HandleDrawArraysInstancedANGLE(unsigned int,void const volatile *) C:\b\swarming\w\ir\cache\builder\src\gpu\command_buffer\service\gles2_cmd_decoder_passthrough_handlers.cc:1753:10
    #14 0x7ffc010099eb in gpu::gles2::GLES2DecoderPassthroughImpl::DoCommandsImpl<0>(unsigned int,void const volatile *,int,int *) C:\b\swarming\w\ir\cache\builder\src\gpu\command_buffer\service\gles2_cmd_decoder_passthrough.cc:655:20
    #15 0x7ffc01008de6 in gpu::gles2::GLES2DecoderPassthroughImpl::DoCommands(unsigned int,void const volatile *,int,int *) C:\b\swarming\w\ir\cache\builder\src\gpu\command_buffer\service\gles2_cmd_decoder_passthrough.cc:593:12
    #16 0x7ffc00f86e49 in gpu::CommandBufferService::Flush(int,class gpu::AsyncAPIInterface *) C:\b\swarming\w\ir\cache\builder\src\gpu\command_buffer\service\command_buffer_service.cc:69:18
    #17 0x7ffbfe58851c in gpu::CommandBufferStub::OnAsyncFlush(int,unsigned int,class std::vector<struct gpu::SyncToken,class std::allocator<struct gpu::SyncToken> > const &) C:\b\swarming\w\ir\cache\builder\src\gpu\ipc\service\command_buffer_stub.cc:543:22
    #18 0x7ffbfe587dff in IPC::MessageT<struct GpuCommandBufferMsg_AsyncFlush_Meta,class std::tuple<int,unsigned int,class std::vector<struct gpu::SyncToken,class std::allocator<struct gpu::SyncToken> > >,void>::Dispatch<class gpu::CommandBufferStub,class gpu::CommandBufferStub,void,void ( gpu::CommandBufferStub::*)(int,unsigned int,class std::vector<struct gpu::SyncToken,class std::allocator<struct gpu::SyncToken> > const &)>(class IPC::Message const *,class gpu::CommandBufferStub *,class gpu::CommandBufferStub *,void *,void ( gpu::CommandBufferStub::*)(int,unsigned int,class std::vector<struct gpu::SyncToken,class std::allocator<struct gpu::SyncToken> > const &)) C:\b\swarming\w\ir\cache\builder\src\ipc\ipc_message_templates.h:146:7
    #19 0x7ffbfe58515e in gpu::CommandBufferStub::OnMessageReceived(class IPC::Message const &) C:\b\swarming\w\ir\cache\builder\src\gpu\ipc\service\command_buffer_stub.cc:193:7
    #20 0x7ffbfc11583f in gpu::GpuChannel::HandleMessageHelper(class IPC::Message const &) C:\b\swarming\w\ir\cache\builder\src\gpu\ipc\service\gpu_channel.cc:566:23
    #21 0x7ffbfc11011a in gpu::GpuChannel::HandleMessage(class IPC::Message const &) C:\b\swarming\w\ir\cache\builder\src\gpu\ipc\service\gpu_channel.cc:543:3
    #22 0x7ffbfbdcca37 in gpu::Scheduler::RunNextTask(void) C:\b\swarming\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler.cc:529:24
    #23 0x7ffc002f1337 in base::TaskAnnotator::RunTask(char const *,struct base::PendingTask *) C:\b\swarming\w\ir\cache\builder\src\base\task\common\task_annotator.cc:104:33
    #24 0x7ffbfd12cc93 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(class base::sequence_manager::LazyNow *,bool *) C:\b\swarming\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:336:21
    #25 0x7ffbfd12c4da in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoSomeWork(void) C:\b\swarming\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:217:7
    #26 0x7ffbfd0e73f3 in base::MessagePumpDefault::Run(class base::MessagePump::Delegate *) C:\b\swarming\w\ir\cache\builder\src\base\message_loop\message_pump_default.cc:39:55
    #27 0x7ffbfd12e4bc in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool) C:\b\swarming\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:403:12
    #28 0x7ffbfafe59a2 in base::RunLoop::Run(void) C:\b\swarming\w\ir\cache\builder\src\base\run_loop.cc:157:14
    #29 0x7ffbfcee695f in content::GpuMain(struct content::MainFunctionParams const &) C:\b\swarming\w\ir\cache\builder\src\content\gpu\gpu_main.cc:358:14
    #30 0x7ffbfaedcb5a in content::ContentMainRunnerImpl::Run(bool) C:\b\swarming\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:879:10
    #31 0x7ffbfaef284a in service_manager::Main(struct service_manager::MainParams const &) C:\b\swarming\w\ir\cache\builder\src\services\service_manager\embedder\main.cc:416:29
    #32 0x7ffbfaedb414 in content::ContentMain(struct content::ContentMainParams const &) C:\b\swarming\w\ir\cache\builder\src\content\app\content_main.cc:19:10
    #33 0x7ffbf4181327 in ChromeMain C:\b\swarming\w\ir\cache\builder\src\chrome\app\chrome_main.cc:103:12
    #34 0x7ff69bec7cdd in MainDllLoader::Launch(struct HINSTANCE__ *,class base::TimeTicks) C:\b\swarming\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:202:12
    #35 0x7ff69bec2352 in main C:\b\swarming\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:229:20
    #36 0x7ff69c238927 in __scrt_common_main_seh d:\agent\_work\2\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #37 0x7ffc66a981f3  (C:\WINDOWS\System32\KERNEL32.DLL+0x1800181f3)
    #38 0x7ffc6715a250  (C:\WINDOWS\SYSTEM32\ntdll.dll+0x18006a250)

Address 0x11fe08bce3a3 is a wild pointer.
SUMMARY: AddressSanitizer: heap-buffer-overflow C:\b\rr\tmpapv6or\w\src\third_party\llvm\projects\compiler-rt\lib\asan\asan_interceptors_memintrinsics.cc:22 in __asan_memcpy
Shadow bytes around the buggy address:
  0x0415c9cf9c20: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0415c9cf9c30: 00 00 00 00 00 00 00 00 00 00 00 07 fa fa fa fa
  0x0415c9cf9c40: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0415c9cf9c50: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0415c9cf9c60: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
=>0x0415c9cf9c70: fa fa fa fa[fa]fa fa fa fa fa fa fa fa fa fa fa
  0x0415c9cf9c80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0415c9cf9c90: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0415c9cf9ca0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0415c9cf9cb0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0415c9cf9cc0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
  Shadow gap:              cc
==3572==ABORTING
[4740:10816:0319/160929.027:ERROR:gles2_cmd_decoder_passthrough_doers.cc(4455)] NOT IMPLEMENTED

What is the expected behavior?
Nothing occurs.

What went wrong?
Heap overflow is detected in GPU process in libANGLE.

Did this work before? N/A 

Chrome version: 74.0.3726.0  Channel: stable
OS Version: 10.0
Flash Version:

## Attachments

- [test3-final.html](attachments/test3-final.html) (text/plain, 1.5 KB)
- [test2-2.html](attachments/test2-2.html) (text/plain, 148.4 KB)
- [gpu.html](attachments/gpu.html) (text/plain, 121.2 KB)

## Timeline

### ta...@gmail.com (2019-03-19)

It seems this attached PoC (not-so-simplified) can directly crash the Chrome release (it has the same call stack trace as shown above under the ASAN build). Hmm, but I do not know how to get the stack trace of the GPU process with windbg.  

### cl...@chromium.org (2019-03-21)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6301154033139712.

### ke...@chromium.org (2019-03-22)

jmadill@: I'm passing you some more ANGLE crash reports, can you help triage these and determine if any are dupes?

I've been having trouble with Windows ASAN although I can confirm that the teswt case in https://crbug.com/chromium/943709#c1 crashes the GPU on stable.

[Monorail components: Internals>GPU>ANGLE]

### ke...@chromium.org (2019-03-22)

[Empty comment from Monorail migration]

### dr...@chromium.org (2019-04-01)

Friendly security sheriff ping, any update on this?

### jm...@chromium.org (2019-04-01)

I'll look at it asap.

### jm...@chromium.org (2019-04-01)

tarafans7@gmail.com can you share the contents of your about:gpu? Save as webpage, complete, then attach to this issue.

### ta...@gmail.com (2019-04-02)

I attached, thanks.

### jm...@chromium.org (2019-04-02)

Reproduced issue and fix in progress:

https://crrev.com/c/1548441

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-04-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/0719a88e7f248f5e9d46e54f73c182ed7fb1b5c5

commit 0719a88e7f248f5e9d46e54f73c182ed7fb1b5c5
Author: Jamie Madill <jmadill@chromium.org>
Date: Wed Apr 03 18:23:01 2019

Fix OOB access for dynamic attribs with offsets.

We were not properly adding the offset to compute the right bounds.

Bug: chromium:943709
Change-Id: I93e714b46dd366d5833fffa858ea3ab0322ffa92
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/1548441
Commit-Queue: Jamie Madill <jmadill@chromium.org>
Reviewed-by: Jonah Ryan-Davis <jonahr@google.com>

[modify] https://crrev.com/0719a88e7f248f5e9d46e54f73c182ed7fb1b5c5/src/tests/gl_tests/RobustResourceInitTest.cpp
[modify] https://crrev.com/0719a88e7f248f5e9d46e54f73c182ed7fb1b5c5/src/libANGLE/renderer/d3d/VertexDataManager.cpp


### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-04-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/b7ac0fff329293bdf02ce18fbd2b7246ec664a08

commit b7ac0fff329293bdf02ce18fbd2b7246ec664a08
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Wed Apr 03 20:10:00 2019

Roll src/third_party/angle 24980278a08a..0719a88e7f24 (2 commits)

https://chromium.googlesource.com/angle/angle.git/+log/24980278a08a..0719a88e7f24


git log 24980278a08a..0719a88e7f24 --date=short --no-merges --format='%ad %ae %s'
2019-04-03 jmadill@chromium.org Fix OOB access for dynamic attribs with offsets.
2019-04-03 syoussefi@chromium.com Disable Clear and TextureUpload perf tests on D3D11


Created with:
  gclient setdep -r src/third_party/angle@0719a88e7f24

The AutoRoll server is located here: https://autoroll.skia.org/r/angle-chromium-autoroll

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, please contact the current sheriff, who should
be CC'd on the roll, and stop the roller if necessary.

CQ_INCLUDE_TRYBOTS=luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel

BUG=chromium:943709,chromium:945415
TBR=syoussefi@chromium.org

Change-Id: I45298854d9522ba37c2f19457d305df2a01fa473
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1551402
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#647435}
[modify] https://crrev.com/b7ac0fff329293bdf02ce18fbd2b7246ec664a08/DEPS


### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-04-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/85b04bb2e38b1278716a71806e32c404fc030955

commit 85b04bb2e38b1278716a71806e32c404fc030955
Author: Jamie Madill <jmadill@chromium.org>
Date: Thu Apr 04 15:26:42 2019

Minor cleanups to copy vertex.

Makes the files parsable as c++ files.

Bug: chromium:943709
Change-Id: I6f7d718f9773fe4a7f72828ee9cd56beb5577c66
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/1545528
Reviewed-by: Geoff Lang <geofflang@chromium.org>
Commit-Queue: Jamie Madill <jmadill@chromium.org>

[modify] https://crrev.com/85b04bb2e38b1278716a71806e32c404fc030955/src/libGLESv2.gni
[delete] https://crrev.com/12b25347dc68d4666b41d0fc116f7a6e0ae9ab85/src/libANGLE/renderer/copyvertex.inc
[add] https://crrev.com/85b04bb2e38b1278716a71806e32c404fc030955/src/libANGLE/renderer/copyvertex.inc.h
[modify] https://crrev.com/85b04bb2e38b1278716a71806e32c404fc030955/src/libANGLE/renderer/copyvertex.h


### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-04-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/d8cb3a5cfade5fd81d42b1507a4a73c0c3ea033a

commit d8cb3a5cfade5fd81d42b1507a4a73c0c3ea033a
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Thu Apr 04 18:59:42 2019

Roll src/third_party/angle 12b25347dc68..896e7ded5f25 (2 commits)

https://chromium.googlesource.com/angle/angle.git/+log/12b25347dc68..896e7ded5f25


git log 12b25347dc68..896e7ded5f25 --date=short --no-merges --format='%ad %ae %s'
2019-04-04 jmadill@chromium.org Use compressed internal format as 'format' in tables.
2019-04-04 jmadill@chromium.org Minor cleanups to copy vertex.


Created with:
  gclient setdep -r src/third_party/angle@896e7ded5f25

The AutoRoll server is located here: https://autoroll.skia.org/r/angle-chromium-autoroll

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, please contact the current sheriff, who should
be CC'd on the roll, and stop the roller if necessary.

CQ_INCLUDE_TRYBOTS=luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel

BUG=chromium:943709
TBR=syoussefi@chromium.org

Change-Id: Ib25e71b05301b9dcf879a9212e72effce69ef991
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1553659
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#647847}
[modify] https://crrev.com/d8cb3a5cfade5fd81d42b1507a4a73c0c3ea033a/DEPS


### jm...@chromium.org (2019-04-04)

Should be fixed in Canary. Needs verification.

### sh...@chromium.org (2019-04-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-04-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-04-05)

This bug requires manual review: M74 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: govind@(Android), kariahda@(iOS), dgagnon@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ab...@google.com (2019-04-08)

how safe is this merge? Why is it critical?

### jm...@chromium.org (2019-04-08)

Abdul, it could trigger a heap buffer overflow in the GPU process. The fix is here:

https://chromium-review.googlesource.com/c/angle/angle/+/1548441

It should be fairly safe. It has been baking in Canary a few days.

### ab...@google.com (2019-04-09)

Branch:3729

### na...@google.com (2019-04-10)

[Empty comment from Monorail migration]

### jm...@chromium.org (2019-04-10)

[Empty comment from Monorail migration]

### na...@google.com (2019-04-10)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### na...@google.com (2019-04-10)

Congrats! The Panel decided to reward $1,000 for this report! 

### na...@google.com (2019-04-10)

[Empty comment from Monorail migration]

### jm...@chromium.org (2019-04-15)

[Empty comment from Monorail migration]

### ab...@google.com (2019-04-16)

[Empty comment from Monorail migration]

### aw...@google.com (2019-04-17)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-04-22)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-06-27)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-07-12)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2019-07-12)

This issue was migrated from crbug.com/chromium/943709?no_tracker_redirect=1

[Monorail blocking: crbug.com/chromium/951451]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-03-12)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094331)*
