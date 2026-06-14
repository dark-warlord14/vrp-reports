# Security: TexImage3D heap-buffer-overflow in WebKit Webgl

| Field | Value |
|-------|-------|
| **Issue ID** | [40090247](https://issues.chromium.org/issues/40090247) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Blink>WebGL |
| **Platforms** | Mac |
| **Reporter** | [Deleted User] |
| **Assignee** | ka...@chromium.org |
| **Created** | 2018-01-21 |
| **Bounty** | $1,000.00 |

## Description

TexImage3D heap-buffer-overflow in WebKit Webgl on macOS. Tested on asan-mac-release-529226.zip

AddressSanitizer: heap-buffer-overflow on address 0x61700007c080 at pc 0x00010158b1f2 bp 0x7ffeee70bcd0 sp 0x7ffeee70b480
READ of size 336 at 0x61700007c080 thread T0
    #0 0x10158b1f1 in __asan_memcpy (libclang_rt.asan_osx_dynamic.dylib:x86_64+0x521f1)
    #1 0x112c95ec9 in gpu::gles2::GLES2Implementation::TexImage3D(unsigned int, int, int, int, int, int, int, unsigned int, unsigned int, void const*) gles2_implementation.cc:2932
    #2 0x11e1e8557 in blink::WebGLRenderingContextBase::TexImageHelperImageData(blink::WebGLRenderingContextBase::TexImageFunctionID, unsigned int, int, int, int, unsigned int, unsigned int, int, int, int, int, blink::ImageData*, blink::IntRect const&, int) WebGLRenderingContextBase.cpp
    #3 0x11e133733 in blink::WebGL2RenderingContextBase::texImage3D(unsigned int, int, int, int, int, int, int, unsigned int, unsigned int, blink::ImageData*) WebGL2RenderingContextBase.cpp:1787
    #4 0x11d40a0c3 in blink::WebGL2RenderingContextV8Internal::texImage3DMethod(v8::FunctionCallbackInfo<v8::Value> const&) V8WebGL2RenderingContext.cpp:1557
    #5 0x10bf20872 in v8::internal::FunctionCallbackArguments::Call(void (*)(v8::FunctionCallbackInfo<v8::Value> const&)) api-arguments.cc:26
    #6 0x10c121394 in v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate*, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::FunctionTemplateInfo>, v8::internal::Handle<v8::internal::Object>, v8::internal::BuiltinArguments) builtins-api.cc:112

## Attachments

- [TexImage3D.html](attachments/TexImage3D.html) (text/plain, 1.7 KB)
- [asan.txt](attachments/asan.txt) (text/plain, 13.5 KB)

## Timeline

### np...@chromium.org (2018-01-22)

[Empty comment from Monorail migration]

[Monorail components: Blink>WebGL]

### cl...@chromium.org (2018-01-22)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6409661350936576.

### cl...@chromium.org (2018-01-22)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6621085813702656.

### cl...@chromium.org (2018-01-22)

Detailed report: https://clusterfuzz.com/testcase?key=6621085813702656

Job Type: linux_asan_chrome_mp
Crash Type: Heap-buffer-overflow READ {*}
Crash Address: 0x617000059400
Crash State:
  gpu::gles2::GLES2Implementation::TexImage3D
  blink::WebGLRenderingContextBase::TexImageHelperImageData
  blink::WebGL2RenderingContextBase::texImage3D
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=495528:495531

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6621085813702656

See https://github.com/google/clusterfuzz-tools for more information.

A recommended severity was added to this bug. Please change the severity if it is inaccurate.


### sh...@chromium.org (2018-01-22)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-01-22)

[Empty comment from Monorail migration]

### [Deleted User] (2018-01-30)

Out of curiosity, why would CF assign this a Medium rating?

### ra...@chromium.org (2018-01-31)

bajones: could you ptal? 

### sh...@chromium.org (2018-02-04)

bajones: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### me...@chromium.org (2018-02-14)

Brandon are you looking into this?

Could you please mark this bug as started or let me know if it should be assigned to someone else?

Thank you

### me...@chromium.org (2018-02-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-02-18)

bajones: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-03-07)

[Empty comment from Monorail migration]

### mm...@chromium.org (2018-03-30)

Friendly ping from the security sheriff. Can we get any update on this?

### sh...@chromium.org (2018-04-18)

[Empty comment from Monorail migration]

### [Deleted User] (2018-04-23)

It's been a while since there has been an update to this. Can I get an update on this?

### rs...@chromium.org (2018-05-08)

kainino: Can you take a look? (bajones pointed me your way)

### ka...@chromium.org (2018-05-08)

Sure, I'll take a look (probably tomorrow)

### ka...@chromium.org (2018-05-10)

#7: I'm guessing it's Severity-Medium because it's a buffer overflow in the renderer process (page/JS process). The renderer process is sandboxed and relatively untrusted, so it isn't high severity.

In particular, Site Isolation (origin-per-process, also used as a Spectre mitigation), makes this even less of an attack vector.

However, of course, we should still fix it as any buffer overrun is dangerous.

### rs...@chromium.org (2018-05-10)

Sorry, missed the question in #7. But #19 is right: buffer overflows start as High, but get lowered to Medium with mitigating factors (e.g., confined to renderer sandbox).

### bu...@chromium.org (2018-05-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/b43de74aa37a65c608308a122098204ab9c2702f

commit b43de74aa37a65c608308a122098204ab9c2702f
Author: Kai Ninomiya <kainino@chromium.org>
Date: Wed May 16 03:48:25 2018

fix incorrect TexImage3D params w/ UNPACK_IMAGE_HEIGHT

Bug: 804123
Test: http://github.com/KhronosGroup/WebGL/pull/2646
Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel
Change-Id: Ifbce9b93f0b35817881e1e34930cbac22a1e8b98
Reviewed-on: https://chromium-review.googlesource.com/1053573
Reviewed-by: Kenneth Russell <kbr@chromium.org>
Commit-Queue: Kai Ninomiya <kainino@chromium.org>
Cr-Commit-Position: refs/heads/master@{#558962}
[modify] https://crrev.com/b43de74aa37a65c608308a122098204ab9c2702f/third_party/blink/renderer/modules/webgl/webgl_rendering_context_base.cc


### cl...@chromium.org (2018-05-16)

ClusterFuzz has detected this issue as fixed in range 558961:558963.

Detailed report: https://clusterfuzz.com/testcase?key=6621085813702656

Job Type: linux_asan_chrome_mp
Crash Type: Heap-buffer-overflow READ {*}
Crash Address: 0x617000059400
Crash State:
  gpu::gles2::GLES2Implementation::TexImage3D
  blink::WebGLRenderingContextBase::TexImageHelperImageData
  blink::WebGL2RenderingContextBase::texImage3D
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=495528:495531
Fixed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=558961:558963

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6621085813702656

See https://github.com/google/clusterfuzz-tools for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2018-05-16)

ClusterFuzz testcase 6621085813702656 is verified as fixed, so closing issue as verified.

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### sh...@chromium.org (2018-05-16)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-05-21)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-05-29)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-06-04)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@chromium.org (2018-06-04)

Nice one! The VRP panel decided to reward $1,000 for this report. Thanks!

### aw...@chromium.org (2018-06-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-06-08)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-06-08)

This bug requires manual review: M68 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), kariahda@(iOS), bhthompson@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ab...@google.com (2018-06-08)

[Empty comment from Monorail migration]

### aw...@google.com (2018-07-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-08-22)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-08-28)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-01-04)

[Empty comment from Monorail migration]

### is...@google.com (2019-01-04)

This issue was migrated from crbug.com/chromium/804123?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40090247)*
