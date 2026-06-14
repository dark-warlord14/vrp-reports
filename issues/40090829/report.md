# Security:  egl::Image::loadImageData - SwiftShader

| Field | Value |
|-------|-------|
| **Issue ID** | [40090829](https://issues.chromium.org/issues/40090829) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Internals>GPU |
| **Platforms** | Windows |
| **Reporter** | [Deleted User] |
| **Assignee** | zm...@chromium.org |
| **Created** | 2018-03-16 |
| **Bounty** | $1,000.00 |

## Description

I have tested this on asan-win32-release_x64-543221 and asan-linux-stable-65.0.3325.162.

Attached is the testcase and the asan log from windows.

==19496==ERROR: AddressSanitizer: access-violation on unknown address 0x25b8413143f0 (pc 0x7ff673cc9965 bp 0x00d61cff9e70 sp 0x00d61cff9de8 T0)
==19496==The signal is caused by a READ memory access.
    #0 0x7ff673cc9964 in memcpy f:\dd\vctools\crt\vcruntime\src\string\amd64\memcpy.asm:228
    #1 0x7ff6739baf7c in __asan_memcpy C:\b\rr\tmpt5wgjo\w\src\third_party\llvm\projects\compiler-rt\lib\asan\asan_interceptors_memintrinsics.cc:23
    #2 0x7fff3cdf1c15 in egl::Image::loadImageData(class egl::Context *,int,int,int,int,int,int,unsigned int,unsigned int,struct egl::PixelStorageModes const &,void const *) C:\b\c\b\win_asan_release\src\third_party\swiftshader\src\OpenGL\common\Image.cpp:1236:7
    #3 0x7fff3d3046f7 in es2::Texture::setImage(class egl::Context *,unsigned int,unsigned int,struct egl::PixelStorageModes const &,void const *,class egl::Image *) C:\b\c\b\win_asan_release\src\third_party\swiftshader\src\OpenGL\libGLESv2\Texture.cpp:341:10
    #4 0x7fff3d305104 in es2::Texture2D::setImage(class egl::Context *,int,int,int,int,unsigned int,unsigned int,struct egl::PixelStorageModes const &,void const *) C:\b\c\b\win_asan_release\src\third_party\swiftshader\src\OpenGL\libGLESv2\Texture.cpp:551:11
    #5 0x7fff3d2c906c in es2::TexImage2D(unsigned int,int,int,int,int,int,unsigned int,unsigned int,void const *) C:\b\c\b\win_asan_release\src\third_party\swiftshader\src\OpenGL\libGLESv2\libGLESv2.cpp:5024:13

## Attachments

- [loadImageData.html](attachments/loadImageData.html) (text/plain, 978 B)
- [asan.txt](attachments/asan.txt) (text/plain, 7.4 KB)

## Timeline

### cl...@chromium.org (2018-03-16)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4826449484447744.

### [Deleted User] (2018-03-17)

I missed a crucial point, you have to have hardware acceleration disabled for this to trigger.

### cl...@chromium.org (2018-03-17)

Detailed report: https://clusterfuzz.com/testcase?key=4826449484447744

Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: UNKNOWN READ
Crash Address: 0x1c17342934fa
Crash State:
  void egl::Transfer<
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=543603:543606

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=4826449484447744

See https://github.com/google/clusterfuzz-tools for more information.

A recommended severity was added to this bug. Please change the severity if it is inaccurate.


### cl...@chromium.org (2018-03-17)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Internals>GPU>SwiftShader]

### cl...@chromium.org (2018-03-17)

Automatically adding ccs based on suspected regression changelists:

Fix floating-point luminance/alpha pixel upload. by capn@google.com - https://swiftshader.googlesource.com/SwiftShader/+/a5a7566de1531d32b647d963e8f72bcd089a493a

Fix texture upload and internalformat handling. by capn@google.com - https://swiftshader.googlesource.com/SwiftShader/+/3b4a25c5365486981157f8ba9a2aee539c162a0d

If this is incorrect, please let us know why and apply the Test-Predator-Wrong-CLs label.

### sh...@chromium.org (2018-03-17)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-03-17)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-03-17)

[Empty comment from Monorail migration]

### es...@chromium.org (2018-03-18)

capn, can you take a look please? Thanks!

### sh...@chromium.org (2018-03-20)

This issue is marked as a release blocker with no OS labels associated. Please add an appropriate OS label.

All release blocking issues should have OS labels associated to it, so that the issue can tracked and promptly verified, once it gets fixed.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ca...@chromium.org (2018-03-20)

Reproduces on Windows as a page fault, and most probably affects all platforms.

While the WebGL code contains a deleteBuffer() call, no glDeleteBuffers() call is made at the driver level. Hence PIXEL_UNPACK_BUFFER remains in use, and the texImage2D() call's imgData argument is interpreted as an offset from the pixel buffer. Hence two pointers are getting added and the result is dereferenced, resulting in a crash. This is probably less fatal when using the GPU.

Action items:
1) Find out why the deleteBuffers() call doesn't reach the driver, and fix it.
2) Ensure that even if the deleteBuffers() call is removed from the WebGL source, that we don't use the PIXEL_UNPACK_BUFFER when calling texImage2D() with an explicit image array argument. Only GLintptr, an integer type, should be usable as an offset into PIXEL_UNPACK_BUFFER.
3) Clarify the spec.
4) Write a conformance test.

[Monorail components: -Internals>GPU>SwiftShader Internals>GPU]

### zm...@chromium.org (2018-03-20)

I'll take a look

### zm...@chromium.org (2018-03-21)

Initial study shows that calling BindBufferBase(UNIFORM_BUFFER) prevented the buffer from being deleted through glDeleteBuffers. This is definitely incorrect, because only unbound container objects should hold onto their buffer bindings, and uniform buffer bindings are not that.

I am looking into a fix of this.

### su...@chromium.org (2018-03-21)

[Empty comment from Monorail migration]

### zm...@chromium.org (2018-03-21)

capn: while I am working on fixing the command buffer side bug, it still seems to me odd that in SwiftShader, texImage2D() with a PIXEL_UNPACK_BUFFER bound triggers a crash. Shouldn't validation generate a GL error because the bound buffer with offset doesn't provide a large enough data store for the texImage2D() call?

### ca...@chromium.org (2018-03-22)

Thanks for pointing that out! Got a fix in the works: https://swiftshader-review.googlesource.com/17928

### zm...@chromium.org (2018-03-23)

[Empty comment from Monorail migration]

### zm...@chromium.org (2018-03-23)

CL is under review: https://chromium-review.googlesource.com/c/chromium/src/+/974463

### bu...@chromium.org (2018-03-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/60fe7720955f2104b402dda0df07ae9696465889

commit 60fe7720955f2104b402dda0df07ae9696465889
Author: Zhenyao Mo <zmo@chromium.org>
Date: Fri Mar 23 16:26:45 2018

Make sure at DeleteBuffers(), all bindings that need to be cleared are cleared

not only at GPU command buffer level (state tracking cache), but also at driver
level.

Otherwise since we might delay the actual call of glDeleteBuffers, then on the
driver side, bindings are still active, and inconsistent with the expectation.

Certain calls after that, for example, TexImage, or ReadPixels, will be
incorrectly affected by such inconsistency.

BUG=822976
TEST=gpu_unittests, test case from the bug
R=kbr@chromium.org,piman@chromium.org

Cq-Include-Trybots: luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;master.tryserver.chromium.android:android_optional_gpu_tests_rel;master.tryserver.chromium.win:win_optional_gpu_tests_rel
Change-Id: I737a2dcfd35bec3b7a36a0971a8437ea4e046ef8
Reviewed-on: https://chromium-review.googlesource.com/974463
Reviewed-by: Antoine Labour <piman@chromium.org>
Commit-Queue: Zhenyao Mo <zmo@chromium.org>
Cr-Commit-Position: refs/heads/master@{#545476}
[modify] https://crrev.com/60fe7720955f2104b402dda0df07ae9696465889/gpu/command_buffer/service/context_state.cc
[modify] https://crrev.com/60fe7720955f2104b402dda0df07ae9696465889/gpu/command_buffer/service/context_state.h
[modify] https://crrev.com/60fe7720955f2104b402dda0df07ae9696465889/gpu/command_buffer/service/gles2_cmd_decoder.cc
[modify] https://crrev.com/60fe7720955f2104b402dda0df07ae9696465889/gpu/command_buffer/service/gles2_cmd_decoder_unittest.cc
[modify] https://crrev.com/60fe7720955f2104b402dda0df07ae9696465889/gpu/command_buffer/service/gles2_cmd_decoder_unittest_buffers.cc
[modify] https://crrev.com/60fe7720955f2104b402dda0df07ae9696465889/gpu/command_buffer/service/gles2_cmd_decoder_unittest_drawing.cc
[modify] https://crrev.com/60fe7720955f2104b402dda0df07ae9696465889/gpu/command_buffer/service/indexed_buffer_binding_host.cc
[modify] https://crrev.com/60fe7720955f2104b402dda0df07ae9696465889/gpu/command_buffer/service/indexed_buffer_binding_host.h
[modify] https://crrev.com/60fe7720955f2104b402dda0df07ae9696465889/gpu/command_buffer/service/indexed_buffer_binding_host_unittest.cc
[modify] https://crrev.com/60fe7720955f2104b402dda0df07ae9696465889/gpu/command_buffer/service/vertex_array_manager.h
[modify] https://crrev.com/60fe7720955f2104b402dda0df07ae9696465889/gpu/command_buffer/service/vertex_attrib_manager.cc
[modify] https://crrev.com/60fe7720955f2104b402dda0df07ae9696465889/gpu/command_buffer/service/vertex_attrib_manager.h
[modify] https://crrev.com/60fe7720955f2104b402dda0df07ae9696465889/gpu/command_buffer/service/vertex_attrib_manager_unittest.cc


### cl...@chromium.org (2018-03-24)

ClusterFuzz has detected this issue as fixed in range 545475:545478.

Detailed report: https://clusterfuzz.com/testcase?key=4826449484447744

Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: UNKNOWN READ
Crash Address: 0x1c17342934fa
Crash State:
  void egl::Transfer<
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=543603:543606
Fixed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=545475:545478

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=4826449484447744

See https://github.com/google/clusterfuzz-tools for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2018-03-24)

ClusterFuzz testcase 4826449484447744 is verified as fixed, so closing issue as verified.

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### sh...@chromium.org (2018-03-24)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-03-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/aba72c74bd89ef4b0e845932e54325d98224628f

commit aba72c74bd89ef4b0e845932e54325d98224628f
Author: Zhenyao Mo <zmo@chromium.org>
Date: Sun Mar 25 19:17:22 2018

Explicitly unmap a buffer when deleting a mapped buffer.

This is because the actual glDeleteBuffers() might be delayed.

BUG=822976
TEST=gpu_unittests
R=kbr@chromium.org,piman@chromium.org

Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;master.tryserver.chromium.win:win_optional_gpu_tests_rel
Change-Id: Idc0504817e8d6d776cf6464a1acda3b0836b9a55
Reviewed-on: https://chromium-review.googlesource.com/978473
Reviewed-by: Kenneth Russell <kbr@chromium.org>
Commit-Queue: Zhenyao Mo <zmo@chromium.org>
Cr-Commit-Position: refs/heads/master@{#545711}
[modify] https://crrev.com/aba72c74bd89ef4b0e845932e54325d98224628f/gpu/command_buffer/service/buffer_manager.h
[modify] https://crrev.com/aba72c74bd89ef4b0e845932e54325d98224628f/gpu/command_buffer/service/gles2_cmd_decoder.cc
[modify] https://crrev.com/aba72c74bd89ef4b0e845932e54325d98224628f/gpu/command_buffer/service/gles2_cmd_decoder_unittest_buffers.cc


### aw...@google.com (2018-03-26)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-03-26)

The following revision refers to this bug:
  https://swiftshader.googlesource.com/SwiftShader.git/+/16a2a922cfd8251a462c9ea5f90105e4d686c211

commit 16a2a922cfd8251a462c9ea5f90105e4d686c211
Author: Nicolas Capens <capn@google.com>
Date: Mon Mar 26 20:23:58 2018

Validate pixel unpack buffer offset.

When a pixel unpack buffer is bound, glTexImage calls interpret the
<pixels> parameter as an offset into the pixel buffer. We weren't
validating that the accessed data falls within the buffer, when taking
the offset into account.

https://crbug.com/chromium/822976

Change-Id: I3ab23e3b135fd4ad1e55555eec95d584684f5d82
Reviewed-on: https://swiftshader-review.googlesource.com/17928
Tested-by: Nicolas Capens <nicolascapens@google.com>
Reviewed-by: Alexis Hétu <sugoi@google.com>

[modify] https://crrev.com/16a2a922cfd8251a462c9ea5f90105e4d686c211/src/OpenGL/libGLESv2/Context.cpp
[modify] https://crrev.com/16a2a922cfd8251a462c9ea5f90105e4d686c211/src/OpenGL/libGLESv2/utilities.cpp
[modify] https://crrev.com/16a2a922cfd8251a462c9ea5f90105e4d686c211/src/OpenGL/libGLESv2/utilities.h


### aw...@chromium.org (2018-04-01)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-04-01)

Thanks for the report! The VRP panel decided to award $1,000 for this report. Cheers!

### aw...@google.com (2018-04-01)

[Empty comment from Monorail migration]

### aw...@google.com (2018-04-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-06-30)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2018-06-30)

This issue was migrated from crbug.com/chromium/822976?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40090829)*
