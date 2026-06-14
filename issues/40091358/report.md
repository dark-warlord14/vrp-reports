# Security: libglesv2 heap-buffer-overflow in VertexBuffer11::storeVertexAttributes

| Field | Value |
|-------|-------|
| **Issue ID** | [40091358](https://issues.chromium.org/issues/40091358) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>GPU>ANGLE |
| **Platforms** | Windows |
| **Reporter** | [Deleted User] |
| **Assignee** | jm...@chromium.org |
| **Created** | 2018-05-11 |
| **Bounty** | $1,000.00 |

## Description

I have tested this on the Chrome Canary 68.0.3426.0 and asan-win32-release_x64-554177.

4:041> r
rax=000001777ff60000 rbx=000001770f196d00 rcx=fffffffff4cbac41
rdx=ffffffff8dc7cc40 rsi=000001770dc92000 rdi=00000177800153c0
rip=00007fff91932377 rsp=00000071fcbfd628 rbp=0000000000000000
 r8=00000071fcbfdd30  r9=000001777ff60000 r10=000001770dbdcc40
r11=00000177768e2740 r12=000001770db4f320 r13=000001777ff60000
r14=0000000000000001 r15=000001770dbdcc40
iopl=0         nv up ei ng nz na po cy
cs=0033  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00010287
libglesv2!memcpy+0x57:
00007fff`91932377 f3a4            rep movs byte ptr [rdi],byte ptr [rsi]


4:041> k
 # Child-SP          RetAddr           Call Site
00 00000071`fcbfd628 00007fff`9175ead8 libglesv2!memcpy+0x57 [f:\dd\vctools\crt\vcruntime\src\string\amd64\memcpy.asm @ 137] 
01 00000071`fcbfd630 00007fff`917ee1b6 libglesv2!rx::VertexBuffer11::storeVertexAttributes+0xd4 [C:\b\c\b\win64_clang\src\third_party\angle\src\libANGLE\renderer\d3d\d3d11\VertexBuffer11.cpp @ 130] 
02 00000071`fcbfd790 00007fff`917670ff libglesv2!rx::StreamingVertexBufferInterface::storeDynamicAttribute+0x16e [C:\b\c\b\win64_clang\src\third_party\angle\src\libANGLE\renderer\d3d\VertexBuffer.cpp @ 178] 
03 00000071`fcbfd940 00007fff`91766cef libglesv2!rx::VertexDataManager::storeDynamicAttrib+0x167 [C:\b\c\b\win64_clang\src\third_party\angle\src\libANGLE\renderer\d3d\VertexDataManager.cpp @ 535] 
04 00000071`fcbfda10 00007fff`917d6e12 libglesv2!rx::VertexDataManager::storeDynamicAttribs+0xe7 [C:\b\c\b\win64_clang\src\third_party\angle\src\libANGLE\renderer\d3d\VertexDataManager.cpp @ 427] 

## Attachments

- [vertex.html](attachments/vertex.html) (text/plain, 3.2 KB)
- [vertex_log.txt](attachments/vertex_log.txt) (text/plain, 9.4 KB)
- [gpu.html](attachments/gpu.html) (text/plain, 180.5 KB)
- [WindowsASANGPUReport.txt](attachments/WindowsASANGPUReport.txt) (text/plain, 15.0 KB)

## Timeline

### cl...@chromium.org (2018-05-11)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6628109085048832.

### ct...@chromium.org (2018-05-11)

Thanks for the report! It looks like ClusterFuzz is having trouble reproducing this, and I'm not sure how to reproduce it on my local ASAN build. Does your POC cause an ASAN crash or are there other steps I should take to reproduce this?

[Monorail components: Internals>GPU>ANGLE]

### [Deleted User] (2018-05-11)

I have tested this on Windows 10 asan-win32-release_x64-554177. You just need to drag/drop the file. 

The following is the partial output from the ASAN build I have

==6132==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x11b8ba0bb7fe at pc 0x7ff675a4b367 bp 0x007f1fbf9f10 sp 0x007f1fbf9f58
READ of size 2 at 0x11b8ba0bb7fe thread T0
    #0 0x7ff675a4b390 in __asan_memcpy C:\b\rr\tmpm5zxwy\w\src\third_party\llvm\projects\compiler-rt\lib\asan\asan_interceptors_memintrinsics.cc:23
    #1 0x7fffa4086c45 in rx::CopyNativeVertexData<signed char,2,2,0>(unsigned char const *,unsigned __int64,unsigned __int64,unsigned char *) C:\b\c\b\win_asan_release\src\third_party\angle\src\libANGLE\renderer\d3d\d3d11\copyvertex.inl:17:9
    #2 0x7fffa407933d in rx::VertexBuffer11::storeVertexAttributes(struct gl::VertexAttribute const &,class gl::VertexBinding const &,unsigned int,int,int,int,unsigned int,unsigned char const *) C:\b\c\b\win_asan_release\src\third_party\angle\src\libANGLE\renderer\d3d\d3d11\VertexBuffer11.cpp:128:5
    #3 0x7fffa42666f6 in rx::StreamingVertexBufferInterface::storeDynamicAttribute(struct gl::VertexAttribute const &,class gl::VertexBinding const &,unsigned int,int,int,int,unsigned int *,unsigned char const *) C:\b\c\b\win_asan_release\src\third_party\angle\src\libANGLE\renderer\d3d\VertexBuffer.cpp:178:5
    #4 0x7fffa409b909 in rx::VertexDataManager::storeDynamicAttrib(class gl::Context const *,struct rx::TranslatedAttribute *,int,int,int) C:\b\c\b\win_asan_release\src\third_party\angle\src\libANGLE\renderer\d3d\VertexDataManager.cpp:535:5
    #5 0x7fffa409ad2f in rx::VertexDataManager::storeDynamicAttribs(class gl::Context const *,class std::vector<struct rx::TranslatedAttribute,class std::allocator<struct rx::TranslatedAttribute> > *,class angle::BitSetT<16,unsigned __int64,unsigned __int64> const &,int,int,int) C:\b\c\b\win_asan_release\src\third_party\angle\src\libANGLE\renderer\d3d\VertexDataManager.cpp:427:9
    #6 0x7fffa422b26b in rx::VertexArray11::updateDynamicAttribs(class gl::Context const *,class rx::VertexDataManager *,class gl::DrawCallParams const &,class angle::BitSetT<16,unsigned __int64,unsigned __int64> const &) C:\b\c\b\win_asan_release\src\third_party\angle\src\libANGLE\renderer\d3d\d3d11\VertexArray11.cpp:300:5
    #7 0x7fffa422a4a0 in rx::VertexArray11::syncStateForDraw(class gl::Context const *,class gl::DrawCallParams const &) C:\b\c\b\win_asan_release\src\third_party\angle\src\libANGLE\renderer\d3d\d3d11\VertexArray11.cpp:144:13

### sh...@chromium.org (2018-05-11)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ct...@chromium.org (2018-05-11)

Testing the same ASAN build on Windows Server 2016 and drag+top the test file, I still don't get a crash.

I do get a console warning about a GL error (the same occurred when testing on Mac and Linux ASAN builds):

[.Offscreen-For-WebGL-0000122423187080]GL ERROR :GL_INVALID_OPERATION : glDrawElements: attempt to draw with all attributes having non-zero divisors

+jmadill@: Could you help triage this or help find an owner who can?

### jm...@chromium.org (2018-05-11)

cthomp do you have a suggestion as for the priority of this bug?

Can take a look shortly. omair@krash.in can you save and attach the contents of your about:gpu in Canary? (save as webpage, complete). Thanks.

### ct...@chromium.org (2018-05-11)

Memory corruption in the GPU process would be Sev-High and P1. Tentatively setting M-68, but if we find it affects earlier releases we should bump that back to be sure we merge as appropriate.

### [Deleted User] (2018-05-11)

Attached.

### jm...@chromium.org (2018-05-11)

omair@krash.in - can you please double check your reproduction case and see if you are getting the validation error that cthomp mentioned in https://crbug.com/chromium/842028#c5? I'm getting the same error. This means that the draw call is aborted before it reaches the problematic code.  Can you also share any flags you're using to start the browser to reproduce the problem?

### jm...@chromium.org (2018-05-11)

Actually, I had a thought. cthomp can you also share your about:gpu? And maybe try using --use-cmd-decoder=passthrough? It might be because of the 50% experiment with the passthrough command decoder. I'll try doing an ASAN build when I have access to my Windows machine.

### [Deleted User] (2018-05-11)

I tested this on some of my local machines. With ATI GPUs there is no crash. With NVidia GPUs the crash happens without problems. ( I am assuming you guys are using Windows Machines to test this).

I am not using any flags to start Chrome.

### jm...@chromium.org (2018-05-11)

It seems to only happen with the passthrough command decoder. Each Windows computer has a 50/50 chance of being on passthrough or validating decoders, chances are cthomp was on the validating which was doing some extra validation.

I can reproduce the crash on Windows Canary. Investigating now.

### ct...@chromium.org (2018-05-11)

Attached is the chrome://gpu report from my Windows ASAN build before applying the flag. It does look like my build was not using the passthrough decoder. I had trouble getting the command line flag to work however, so I wasn't able to test with the passthrough decoder enabled. One caveat is that this is a virtual machine -- I don't have a physical Windows machine to test on.

Let me know if there's anything else I can help with testing/triaging. Do you think a Windows Chrome clusterfuzz run with `--use-cmd-decoder=passthrough` would work? Which decoder setting is the default on the CQ? I can start up a new analysis to test it.

### jm...@chromium.org (2018-05-11)

cthomp the passthrough decoder only works on a real GPU, with ANGLE. Not SwiftShader. That's why you're on the validating and also why the flag isn't working on the VM.

The setting on the CQ depends on the particular test. We have a bunch of tests that use the passthrough command decoder, but it looks like we had a test coverage gap here. I'm adding a regression test for this.

Geoff is the owner of the passthrough work - maybe he has thoughts on how to integrate this with clusterfuzz.

Should have a fix for the issue up soon-ish.

### ct...@chromium.org (2018-05-11)

That makes sense. For ClusterFuzz, I think the *_asan_chrome_with_gpu jobs could handle it, but I'm not sure (and they aren't sandboxed the same as the standard jobs).

Anyway, thank you for your quick handling of this :)

### jm...@chromium.org (2018-05-11)

[Empty comment from Monorail migration]

### jm...@chromium.org (2018-05-11)

Fix in review: https://chromium-review.googlesource.com/c/angle/angle/+/1055928

### jm...@chromium.org (2018-05-11)

Note this does affect 67, we can see about merging it back once it's backed in Canary. I don't think it affects 66.

### bu...@chromium.org (2018-05-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/18e323ab2cff6e4bab6473b70109a33fedd76c25

commit 18e323ab2cff6e4bab6473b70109a33fedd76c25
Author: Jamie Madill <jmadill@chromium.org>
Date: Sat May 12 01:29:43 2018

D3D11: Fix out-of-range access with robust access.

When using a vertex buffer with DYNAMIC usage, with robust buffer
access enabled, we would sometimes read out-of-bounds when using very
large values for the index range. An unchecked signed addition would
overflow and lead to reading a negative offset.

Fix this problem by keeping the value size_t whenever possible. Also do
clamped casts when converting to a smaller values.

Also adds a regression test.

Bug: chromium:842028
Change-Id: Ie630ac857c6acfc0bace849a03eebfbaa2fbe89a
Reviewed-on: https://chromium-review.googlesource.com/1055928
Commit-Queue: Jamie Madill <jmadill@chromium.org>
Reviewed-by: Geoff Lang <geofflang@chromium.org>

[modify] https://crrev.com/18e323ab2cff6e4bab6473b70109a33fedd76c25/src/libANGLE/renderer/vulkan/VertexArrayVk.h
[modify] https://crrev.com/18e323ab2cff6e4bab6473b70109a33fedd76c25/src/libANGLE/renderer/vulkan/vk_helpers.h
[modify] https://crrev.com/18e323ab2cff6e4bab6473b70109a33fedd76c25/src/libANGLE/renderer/d3d/d3d11/Renderer11.h
[modify] https://crrev.com/18e323ab2cff6e4bab6473b70109a33fedd76c25/src/libANGLE/renderer/d3d/d3d11/InputLayoutCache.cpp
[modify] https://crrev.com/18e323ab2cff6e4bab6473b70109a33fedd76c25/src/tests/gl_tests/RobustBufferAccessBehaviorTest.cpp
[modify] https://crrev.com/18e323ab2cff6e4bab6473b70109a33fedd76c25/src/libANGLE/renderer/d3d/BufferD3D.cpp
[modify] https://crrev.com/18e323ab2cff6e4bab6473b70109a33fedd76c25/src/libANGLE/renderer/d3d/BufferD3D.h
[modify] https://crrev.com/18e323ab2cff6e4bab6473b70109a33fedd76c25/src/libANGLE/renderer/d3d/d3d9/Renderer9.h
[modify] https://crrev.com/18e323ab2cff6e4bab6473b70109a33fedd76c25/src/libANGLE/renderer/d3d/VertexDataManager.cpp
[modify] https://crrev.com/18e323ab2cff6e4bab6473b70109a33fedd76c25/src/libANGLE/renderer/d3d/d3d11/Renderer11.cpp
[modify] https://crrev.com/18e323ab2cff6e4bab6473b70109a33fedd76c25/src/libANGLE/renderer/d3d/RendererD3D.h
[modify] https://crrev.com/18e323ab2cff6e4bab6473b70109a33fedd76c25/src/libANGLE/renderer/d3d/VertexDataManager.h
[modify] https://crrev.com/18e323ab2cff6e4bab6473b70109a33fedd76c25/src/libANGLE/renderer/vulkan/VertexArrayVk.cpp
[modify] https://crrev.com/18e323ab2cff6e4bab6473b70109a33fedd76c25/src/libANGLE/renderer/vulkan/vk_helpers.cpp
[modify] https://crrev.com/18e323ab2cff6e4bab6473b70109a33fedd76c25/src/libANGLE/renderer/d3d/d3d11/VertexBuffer11.h
[modify] https://crrev.com/18e323ab2cff6e4bab6473b70109a33fedd76c25/src/libANGLE/renderer/d3d/d3d9/VertexBuffer9.cpp
[modify] https://crrev.com/18e323ab2cff6e4bab6473b70109a33fedd76c25/src/libANGLE/renderer/d3d/d3d9/VertexBuffer9.h
[modify] https://crrev.com/18e323ab2cff6e4bab6473b70109a33fedd76c25/src/tests/perf_tests/IndexDataManagerTest.cpp
[modify] https://crrev.com/18e323ab2cff6e4bab6473b70109a33fedd76c25/src/libANGLE/params.h
[modify] https://crrev.com/18e323ab2cff6e4bab6473b70109a33fedd76c25/src/libANGLE/renderer/d3d/d3d9/Renderer9.cpp
[modify] https://crrev.com/18e323ab2cff6e4bab6473b70109a33fedd76c25/src/libANGLE/renderer/d3d/VertexBuffer.h
[modify] https://crrev.com/18e323ab2cff6e4bab6473b70109a33fedd76c25/src/libANGLE/renderer/d3d/VertexBuffer.cpp
[modify] https://crrev.com/18e323ab2cff6e4bab6473b70109a33fedd76c25/src/libANGLE/renderer/d3d/d3d11/VertexBuffer11.cpp
[modify] https://crrev.com/18e323ab2cff6e4bab6473b70109a33fedd76c25/src/libANGLE/params.cpp


### bu...@chromium.org (2018-05-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/bb0bdb7fbbb82ff5890a36cd80ad020c1091edf3

commit bb0bdb7fbbb82ff5890a36cd80ad020c1091edf3
Author: angle-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com <angle-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com>
Date: Sat May 12 04:06:24 2018

Roll src/third_party/angle/ 422f2ce24..18e323ab2 (1 commit)

https://chromium.googlesource.com/angle/angle.git/+log/422f2ce24c5b..18e323ab2cff

$ git log 422f2ce24..18e323ab2 --date=short --no-merges --format='%ad %ae %s'
2018-05-11 jmadill D3D11: Fix out-of-range access with robust access.

Created with:
  roll-dep src/third_party/angle
BUG=chromium:842028


The AutoRoll server is located here: https://angle-chromium-roll.skia.org

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, please contact the current sheriff, who should
be CC'd on the roll, and stop the roller if necessary.


CQ_INCLUDE_TRYBOTS=luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel
TBR=fjhenigman@chromium.org

Change-Id: Id5f71c374ee3cd238fc2b2965cc3751184b33279
Reviewed-on: https://chromium-review.googlesource.com/1056489
Reviewed-by: angle-chromium-autoroll <angle-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com>
Commit-Queue: angle-chromium-autoroll <angle-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#558111}
[modify] https://crrev.com/bb0bdb7fbbb82ff5890a36cd80ad020c1091edf3/DEPS


### sh...@chromium.org (2018-05-12)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-05-12)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2018-05-12)

+awhalley@ (Security TPM) for M67 merge review

### jm...@chromium.org (2018-05-14)

I can confirm this is fixed in Canary. Marking merge request. This security impact is pretty high, the fix is relatively small:

https://chromium-review.googlesource.com/1055928

It has baked in Canary over the weekend.

### sh...@chromium.org (2018-05-14)

This bug requires manual review: DEPS changes referenced in bugdroid comments.
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), kbleicher@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-05-14)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-05-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/b878f00db58ea27639b0ac89923f64cfcec3bb11

commit b878f00db58ea27639b0ac89923f64cfcec3bb11
Author: Jamie Madill <jmadill@chromium.org>
Date: Mon May 14 15:01:36 2018

Fix warnings from size_t conversions.

These casts could result in overflow.

Bug: chromium:842028
Change-Id: I998b638c58333a29f6bc9136ae3e81b90683cb72
Reviewed-on: https://chromium-review.googlesource.com/1057415
Reviewed-by: Luc Ferron <lucferron@chromium.org>
Commit-Queue: Jamie Madill <jmadill@chromium.org>

[modify] https://crrev.com/b878f00db58ea27639b0ac89923f64cfcec3bb11/src/libANGLE/renderer/d3d/VertexBuffer.h
[modify] https://crrev.com/b878f00db58ea27639b0ac89923f64cfcec3bb11/src/libANGLE/renderer/d3d/VertexBuffer.cpp
[modify] https://crrev.com/b878f00db58ea27639b0ac89923f64cfcec3bb11/src/libANGLE/renderer/d3d/d3d11/Renderer11.cpp


### go...@chromium.org (2018-05-14)

Is M67 merge request is only for CL - https://chromium-review.googlesource.com/1055928 per https://crbug.com/chromium/842028#c25? OR CL listed at #28 need a merge to M67 as well?


### jm...@chromium.org (2018-05-14)

Sorry yes, both CLs should probably go in. I would squash them into one.

### go...@chromium.org (2018-05-14)

No worries. CL listed at #28 just landed not in canary yet. So please update the bug with canary result tomorrow. Thank you.

### aw...@google.com (2018-05-14)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-05-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/9e7a5bd04dc7b4efc0874abc33986b392b2fe793

commit 9e7a5bd04dc7b4efc0874abc33986b392b2fe793
Author: angle-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com <angle-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com>
Date: Mon May 14 23:45:14 2018

Roll src/third_party/angle/ 5d2ccc534..5730c0bf4 (9 commits)

https://chromium.googlesource.com/angle/angle.git/+log/5d2ccc534d26..5730c0bf431e

$ git log 5d2ccc534..5730c0bf4 --date=short --no-merges --format='%ad %ae %s'
2018-05-14 geofflang Add more dEQP EGL expectations for Linux and Android.
2018-05-14 cwallez DisplayGLX: Close the X display if we own it.
2018-05-14 geofflang Add more dEQP EGL expectations for Linux and Android.
2018-05-14 geofflang DEQP: Print not supported messages from tests.
2018-05-14 geofflang Add dEQP EGL test expectations for Linux and Android.
2018-05-10 jmadill Vulkan: Implement masked color clear with depth.
2018-05-14 jmadill Fix libGLESv2 wrong .def file.
2018-05-14 jmadill Fix warnings from size_t conversions.
2018-04-23 lfy GLES1: Renderer (minimal)

Created with:
  roll-dep src/third_party/angle
BUG=chromium:834269,chromium:842028


The AutoRoll server is located here: https://angle-chromium-roll.skia.org

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, please contact the current sheriff, who should
be CC'd on the roll, and stop the roller if necessary.


CQ_INCLUDE_TRYBOTS=luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel
TBR=ynovikov@chromium.org

Change-Id: I1ac4625bc1c520a30186f260160dffbdf5787693
Reviewed-on: https://chromium-review.googlesource.com/1058172
Commit-Queue: angle-chromium-autoroll <angle-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com>
Reviewed-by: angle-chromium-autoroll <angle-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#558531}
[modify] https://crrev.com/9e7a5bd04dc7b4efc0874abc33986b392b2fe793/DEPS


### aw...@google.com (2018-05-17)

govind@ - good for 67

### go...@chromium.org (2018-05-17)

Approving merge to M67 branch 3396 based on https://crbug.com/chromium/842028#c35. Please merge ASAP. Thank you.

### bu...@chromium.org (2018-05-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/702006f4a07e4f0069f189679f5c84ebda7c5772

commit 702006f4a07e4f0069f189679f5c84ebda7c5772
Author: Jamie Madill <jmadill@chromium.org>
Date: Thu May 17 18:54:25 2018

D3D11: Fix out-of-range access with robust access.

When using a vertex buffer with DYNAMIC usage, with robust buffer
access enabled, we would sometimes read out-of-bounds when using very
large values for the index range. An unchecked signed addition would
overflow and lead to reading a negative offset.

Fix this problem by keeping the value size_t whenever possible. Also do
clamped casts when converting to a smaller values.

Also adds a regression test.

Also combined with 26b0bfb46: Fix warnings from size_t conversions.

Bug: chromium:842028
Change-Id: Ie1a8f476f3e97149362eb9855f08450c067ff807
Reviewed-on: https://chromium-review.googlesource.com/1064721
Reviewed-by: Jamie Madill <jmadill@chromium.org>

[modify] https://crrev.com/702006f4a07e4f0069f189679f5c84ebda7c5772/src/libANGLE/renderer/vulkan/VertexArrayVk.h
[modify] https://crrev.com/702006f4a07e4f0069f189679f5c84ebda7c5772/src/libANGLE/renderer/vulkan/vk_helpers.h
[modify] https://crrev.com/702006f4a07e4f0069f189679f5c84ebda7c5772/src/libANGLE/renderer/d3d/d3d11/Renderer11.h
[modify] https://crrev.com/702006f4a07e4f0069f189679f5c84ebda7c5772/src/libANGLE/renderer/d3d/d3d11/InputLayoutCache.cpp
[modify] https://crrev.com/702006f4a07e4f0069f189679f5c84ebda7c5772/src/tests/gl_tests/RobustBufferAccessBehaviorTest.cpp
[modify] https://crrev.com/702006f4a07e4f0069f189679f5c84ebda7c5772/src/libANGLE/renderer/d3d/BufferD3D.cpp
[modify] https://crrev.com/702006f4a07e4f0069f189679f5c84ebda7c5772/src/libANGLE/renderer/d3d/BufferD3D.h
[modify] https://crrev.com/702006f4a07e4f0069f189679f5c84ebda7c5772/src/libANGLE/renderer/d3d/d3d9/Renderer9.h
[modify] https://crrev.com/702006f4a07e4f0069f189679f5c84ebda7c5772/src/libANGLE/renderer/d3d/VertexDataManager.cpp
[modify] https://crrev.com/702006f4a07e4f0069f189679f5c84ebda7c5772/src/libANGLE/renderer/d3d/d3d11/Renderer11.cpp
[modify] https://crrev.com/702006f4a07e4f0069f189679f5c84ebda7c5772/src/libANGLE/renderer/d3d/RendererD3D.h
[modify] https://crrev.com/702006f4a07e4f0069f189679f5c84ebda7c5772/src/libANGLE/renderer/d3d/VertexDataManager.h
[modify] https://crrev.com/702006f4a07e4f0069f189679f5c84ebda7c5772/src/libANGLE/renderer/vulkan/VertexArrayVk.cpp
[modify] https://crrev.com/702006f4a07e4f0069f189679f5c84ebda7c5772/src/libANGLE/renderer/vulkan/vk_helpers.cpp
[modify] https://crrev.com/702006f4a07e4f0069f189679f5c84ebda7c5772/src/libANGLE/renderer/d3d/d3d11/VertexBuffer11.h
[modify] https://crrev.com/702006f4a07e4f0069f189679f5c84ebda7c5772/src/libANGLE/renderer/d3d/d3d9/VertexBuffer9.cpp
[modify] https://crrev.com/702006f4a07e4f0069f189679f5c84ebda7c5772/src/libANGLE/renderer/d3d/d3d9/VertexBuffer9.h
[modify] https://crrev.com/702006f4a07e4f0069f189679f5c84ebda7c5772/src/tests/perf_tests/IndexDataManagerTest.cpp
[modify] https://crrev.com/702006f4a07e4f0069f189679f5c84ebda7c5772/src/libANGLE/params.h
[modify] https://crrev.com/702006f4a07e4f0069f189679f5c84ebda7c5772/src/libANGLE/renderer/d3d/d3d9/Renderer9.cpp
[modify] https://crrev.com/702006f4a07e4f0069f189679f5c84ebda7c5772/src/libANGLE/renderer/d3d/VertexBuffer.h
[modify] https://crrev.com/702006f4a07e4f0069f189679f5c84ebda7c5772/src/libANGLE/renderer/d3d/VertexBuffer.cpp
[modify] https://crrev.com/702006f4a07e4f0069f189679f5c84ebda7c5772/src/libANGLE/renderer/d3d/d3d11/VertexBuffer11.cpp
[modify] https://crrev.com/702006f4a07e4f0069f189679f5c84ebda7c5772/src/libANGLE/params.cpp


### aw...@google.com (2018-05-17)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-05-21)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-05-21)

Nice one omair@! The VRP panel decided to award $1,000 for this report!

### aw...@google.com (2018-05-21)

(though they did also note that this should have been a Severity-Medium)

### aw...@chromium.org (2018-05-21)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-08-20)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2018-08-20)

This issue was migrated from crbug.com/chromium/842028?no_tracker_redirect=1

[Monorail blocked-on: crbug.com/angleproject/2389]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-03-12)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091358)*
