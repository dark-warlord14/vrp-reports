# Security: heap-buffer-overflow in gpu::gles2::StrictIdHandler::FreeIds

| Field | Value |
|-------|-------|
| **Issue ID** | [40091547](https://issues.chromium.org/issues/40091547) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>WebGL, Internals>GPU>Internals |
| **Platforms** | Linux |
| **Reporter** | [Deleted User] |
| **Assignee** | kb...@chromium.org |
| **Created** | 2018-06-01 |
| **Bounty** | $3,000.00 |

## Description

I have tested this on the stable asan linux build (asan-linux-stable-67.0.3396.62).

ERROR: AddressSanitizer: heap-buffer-overflow on address 0x602000227832 at pc 0x5642e80f6294 bp 0x7ffec465d810 sp 0x7ffec465d808
WRITE of size 1 at 0x602000227832 thread T0 (chrome)
    #0 0x5642e80f6293 in gpu::gles2::StrictIdHandler::FreeIds(gpu::gles2::GLES2Implementation*, int, unsigned int const*, void (gpu::gles2::GLES2Implementation::*)(int, unsigned int const*)) gpu/command_buffer/client/share_group.cc:166:30
    #1 0x5642e804f5a6 in gpu::gles2::GLES2Implementation::DeleteBuffersHelper(int, unsigned int const*) gpu/command_buffer/client/gles2_implementation.cc:4344:14
    #2 0x5642f1952a04 in blink::WebGLBuffer::DeleteObjectImpl(gpu::gles2::GLES2Interface*) third_party/blink/renderer/modules/webgl/webgl_buffer.cc:49:7
    #3 0x5642f1c997e8 in blink::WebGLVertexArrayObjectBase::DispatchDetached(gpu::gles2::GLES2Interface*) third_party/blink/renderer/modules/webgl/webgl_vertex_array_object_base.cc:46:30
    #4 0x5642f1ba9121 in deleteVertexArrayMethod /mnt/scratch0/chromium/src/out/asan-linux-stable-67.0.3396.62/gen/third_party/blink/renderer/bindings/modules/v8/v8_webgl2_rendering_context.cc:7081:9
    #5 0x5642f1ba9121 in blink::V8WebGL2RenderingContext::deleteVertexArrayMethodCallback(v8::FunctionCallbackInfo<v8::Value> const&) /mnt/scratch0/chromium/src/out/asan-linux-stable-67.0.3396.62/gen/third_party/blink/renderer/bindings/modules/v8/v8_webgl2_rendering_context.cc:12956

## Attachments

- [gpu_freeids.html](attachments/gpu_freeids.html) (text/plain, 2.6 KB)
- [asan.txt](attachments/asan.txt) (text/plain, 14.2 KB)

## Timeline

### cl...@chromium.org (2018-06-01)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6067041178746880.

### cl...@chromium.org (2018-06-02)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Blink>WebGL Internals>GPU>Internals]

### cl...@chromium.org (2018-06-02)

Detailed report: https://clusterfuzz.com/testcase?key=6067041178746880

Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-buffer-overflow WRITE 1
Crash Address: 0x6090001db581
Crash State:
  gpu::gles2::StrictIdHandler::FreeIds
  gpu::gles2::GLES2Implementation::DeleteBuffersHelper
  blink::WebGLBuffer::DeleteObjectImpl
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=523898:523900

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6067041178746880

See https://github.com/google/clusterfuzz-tools for more information.

A recommended severity was added to this bug. Please change the severity if it is inaccurate.


### sh...@chromium.org (2018-06-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-06-02)

[Empty comment from Monorail migration]

### me...@chromium.org (2018-06-04)

pilam: Can you please take a look? Thanks.

### pi...@chromium.org (2018-06-04)

It looks like WebGL is freeing an id that was not generated via GenBuffers.

### pi...@chromium.org (2018-06-04)

Actually, never mind. StrictIdHandler is wrong, very wrong. Not sure why we've never run into this!

I should be able to fix this quickly.

### pi...@chromium.org (2018-06-04)

Ugh. Sorry for spam, no it's WebGL.

ids are allocated here: https://cs.chromium.org/chromium/src/gpu/command_buffer/client/share_group.cc?type=cs&q=StrictIdHandler&sq=package:chromium&g=0&l=137 (called by GenBuffers)
The state for |id| is stored at id_state_[id-1]. id_state_ is resized (up) when we allocate a new id. id_state_ is never resized down.
The OOB write is at https://cs.chromium.org/chromium/src/gpu/command_buffer/client/share_group.cc?type=cs&q=StrictIdHandler&sq=package:chromium&g=0&l=166, accessing id_state_[id - 1], where id is passed by WebGL, so that means that id was nor allocated by GenBuffers.
Or that the GLES2Implementation/ShareGroup was UAF, I suppose that's a possibility.

### kb...@chromium.org (2018-06-04)

The problematic deletion call appears to be:

setTimeout(function(){gl3.deleteVertexArray(vao);}, 100);

Investigating why.


### kb...@chromium.org (2018-06-04)

Symbolized stack:

Received signal 11 SEGV_MAPERR 000000000001
    #0 0x56354faa9c31 in __interceptor_backtrace /b/build/slave/linux_upload_clang/build/src/third_party/llvm/compiler-rt/lib/asan/../sanitizer_common/sanitizer_common_interceptors.inc:3980:13
    #1 0x7fef4ddfeccc in base::debug::StackTrace::StackTrace(unsigned long) ./../../base/debug/stack_trace_posix.cc:808:41
    #2 0x7fef4ddfdc4d in base::debug::(anonymous namespace)::StackDumpSignalHandler(int, siginfo_t*, void*) ./../../base/debug/stack_trace_posix.cc:334:3
    #3 0x7fef28ba30c0 in __funlockfile ??:?
    #4 0x7fef28ba30c0 in ?? ??:0
    #5 0x7fef397f29dc in gpu::gles2::StrictIdHandler::FreeIds(gpu::gles2::GLES2Implementation*, int, unsigned int const*, void (gpu::gles2::GLES2Implementation::*)(int, unsigned int const*)) ./../../gpu/command_buffer/client/share_group.cc:166:30
    #6 0x7fef397467d7 in gpu::gles2::GLES2Implementation::DeleteBuffersHelper(int, unsigned int const*) ./../../gpu/command_buffer/client/gles2_implementation.cc:4331:14
    #7 0x7fef2c6cada5 in blink::WebGLBuffer::DeleteObjectImpl(gpu::gles2::GLES2Interface*) ./../../third_party/blink/renderer/modules/webgl/webgl_buffer.cc:49:7
    #8 0x7fef2c777518 in blink::WebGLVertexArrayObjectBase::DispatchDetached(gpu::gles2::GLES2Interface*) ./../../third_party/blink/renderer/modules/webgl/webgl_vertex_array_object_base.cc:46:30
    #9 0x7fef2b889832 in deleteVertexArrayMethod ./gen/third_party/blink/renderer/bindings/modules/v8/v8_webgl2_rendering_context.cc:7553:9
    #10 0x7fef2b889832 in blink::V8WebGL2RenderingContext::deleteVertexArrayMethodCallback(v8::FunctionCallbackInfo<v8::Value> const&) ./gen/third_party/blink/renderer/bindings/modules/v8/v8_webgl2_rendering_context.cc:13881:0
    #11 0x7fef357fedaa in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo*) ./../../v8/src/api-arguments-inl.h:94:3
    #12 0x7fef357fc4e1 in v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate*, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::FunctionTemplateInfo>, v8::internal::Handle<v8::internal::Object>, v8::internal::BuiltinArguments) ./../../v8/src/builtins/builtins-api.cc:109:36
    #13 0x7fef357fa164 in v8::internal::Builtin_Impl_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate*) ./../../v8/src/builtins/builtins-api.cc:139:5
#12 0x7e938915777d <unknown>


### kb...@chromium.org (2018-06-04)

The bug's in the validation associated with deleteVertexArray. The global variable "vao" is reset to the WebGLVertexArrayObject associated with context gl2, but we attempt to delete the vao on context gl3.

The WebGL spec is missing text throughout that asserts that the objects passed in must be associated with this context. The tests which verify this assumption are also incomplete. In Chrome, there are more entry points than just this one which are missing this check.


### bu...@chromium.org (2018-06-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/482c0ed96b8bee5e22909f811f1cbe98152ce661

commit 482c0ed96b8bee5e22909f811f1cbe98152ce661
Author: Kenneth Russell <kbr@chromium.org>
Date: Tue Jun 05 07:41:04 2018

Generate GL errors more strictly in StrictIdHandler.

Generate INVALID_VALUE if the ID has either never been generated by
this context, or if it's already been deleted.

Bug: 848914
Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel
Change-Id: I203bc71ae36e3339326c2912bbfe21853d08176c
Reviewed-on: https://chromium-review.googlesource.com/1086365
Commit-Queue: Kenneth Russell <kbr@chromium.org>
Reviewed-by: Antoine Labour <piman@chromium.org>
Cr-Commit-Position: refs/heads/master@{#564396}
[modify] https://crrev.com/482c0ed96b8bee5e22909f811f1cbe98152ce661/gpu/command_buffer/client/gles2_implementation_unittest.cc
[modify] https://crrev.com/482c0ed96b8bee5e22909f811f1cbe98152ce661/gpu/command_buffer/client/share_group.cc


### cl...@chromium.org (2018-06-05)

ClusterFuzz has detected this issue as fixed in range 564395:564396.

Detailed report: https://clusterfuzz.com/testcase?key=6067041178746880

Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-buffer-overflow WRITE 1
Crash Address: 0x6090001db581
Crash State:
  gpu::gles2::StrictIdHandler::FreeIds
  gpu::gles2::GLES2Implementation::DeleteBuffersHelper
  blink::WebGLBuffer::DeleteObjectImpl
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=523898:523900
Fixed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=564395:564396

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6067041178746880

See https://github.com/google/clusterfuzz-tools for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2018-06-05)

ClusterFuzz testcase 6067041178746880 is verified as fixed, so closing issue as verified.

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### sh...@chromium.org (2018-06-05)

[Empty comment from Monorail migration]

### kb...@chromium.org (2018-06-05)

Requesting merge of 482c0ed96b8bee5e22909f811f1cbe98152ce661 to M67 and M68. It was designed (with piman@) as a small, self-contained fix which could be backported.

A more comprehensive fix for WebGL is coming in a subsequent commit which we won't aim to backport (though it turned out to not be that big, either).


### sh...@chromium.org (2018-06-05)

This bug requires manual review: Request affecting a post-stable build
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), kbleicher@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2018-06-05)

+awhalley@ (Security TPM) for M67/M68 merge review. Change listed at #17 482c0ed96b8bee5e22909f811f1cbe98152ce661  is not yet baked in canary/dev. 

### aw...@chromium.org (2018-06-05)

This will miss today's cut, but once it's been out in dev for a bit we should indeed merge to 67 in case there's another spin.


### ab...@google.com (2018-06-05)

Approving merge for M68. Branch:3440

### bu...@chromium.org (2018-06-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/25c3fc10bf0632e7c30f41030dbeb65089d5199a

commit 25c3fc10bf0632e7c30f41030dbeb65089d5199a
Author: Kenneth Russell <kbr@chromium.org>
Date: Wed Jun 06 18:59:15 2018

Generate GL errors more strictly in StrictIdHandler.

Generate INVALID_VALUE if the ID has either never been generated by
this context, or if it's already been deleted.

TBR=kbr@chromium.org

(cherry picked from commit 482c0ed96b8bee5e22909f811f1cbe98152ce661)

Bug: 848914
Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel
Change-Id: I203bc71ae36e3339326c2912bbfe21853d08176c
Reviewed-on: https://chromium-review.googlesource.com/1086365
Commit-Queue: Kenneth Russell <kbr@chromium.org>
Reviewed-by: Antoine Labour <piman@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#564396}
Reviewed-on: https://chromium-review.googlesource.com/1089454
Reviewed-by: Kenneth Russell <kbr@chromium.org>
Cr-Commit-Position: refs/branch-heads/3440@{#216}
Cr-Branched-From: 010ddcfda246975d194964ccf20038ebbdec6084-refs/heads/master@{#561733}
[modify] https://crrev.com/25c3fc10bf0632e7c30f41030dbeb65089d5199a/gpu/command_buffer/client/gles2_implementation_unittest.cc
[modify] https://crrev.com/25c3fc10bf0632e7c30f41030dbeb65089d5199a/gpu/command_buffer/client/share_group.cc


### bu...@chromium.org (2018-06-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/98095c718d7580b5d6715e5bfd8698234ecb4470

commit 98095c718d7580b5d6715e5bfd8698234ecb4470
Author: Kenneth Russell <kbr@chromium.org>
Date: Wed Jun 06 20:11:35 2018

Validate all incoming WebGLObjects.

A few entry points were missing the correct validation.

Tested with improved conformance tests in
https://github.com/KhronosGroup/WebGL/pull/2654 .

Bug: 848914
Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel
Change-Id: Ib98a61cc5bf378d1b3338b04acd7e1bc4c2fe008
Reviewed-on: https://chromium-review.googlesource.com/1086718
Reviewed-by: Kai Ninomiya <kainino@chromium.org>
Reviewed-by: Antoine Labour <piman@chromium.org>
Commit-Queue: Kenneth Russell <kbr@chromium.org>
Cr-Commit-Position: refs/heads/master@{#565016}
[modify] https://crrev.com/98095c718d7580b5d6715e5bfd8698234ecb4470/third_party/blink/renderer/modules/webgl/webgl2_rendering_context_base.cc
[modify] https://crrev.com/98095c718d7580b5d6715e5bfd8698234ecb4470/third_party/blink/renderer/modules/webgl/webgl_rendering_context_base.cc


### go...@chromium.org (2018-06-11)

Cl listed at #22 is not yet baked in Beta. So we won't consider this merge for this week M67 stable respin.

### aw...@chromium.org (2018-06-11)

Though #22 has been out in beta for a sufficient time, I'm OK leaving this one out of this week's respin.

### go...@chromium.org (2018-06-11)

Thank you  awhalley@. We won't take this merge in for this week M67 stable respin.

kbr@, Is Cl listed at #23 need a merge to M68? If yes, pls request a merge to M68. Thank you.

### aw...@chromium.org (2018-06-11)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-06-15)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@chromium.org (2018-06-15)

Nice one omair@ - $3,000 for this report!

### aw...@chromium.org (2018-06-15)

[Empty comment from Monorail migration]

### kb...@chromium.org (2018-06-20)

The CL in #23 does not need to be merged to M68. Thanks.


### aw...@chromium.org (2018-06-21)

Next 67 is going to be tightly focused, so we'll have this go out in 68

### kb...@chromium.org (2018-06-28)

[Empty comment from Monorail migration]

### aw...@google.com (2018-07-23)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-08-28)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-09-11)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2019-06-27)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-05)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-05)

This issue was migrated from crbug.com/chromium/848914?no_tracker_redirect=1

[Multiple monorail components: Blink>WebGL, Internals>GPU>Internals]
[Monorail blocking: crbug.com/chromium/857303]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091547)*
