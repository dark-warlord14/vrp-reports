# Heap-use-after-free in sw::Renderer::finishRendering

| Field | Value |
|-------|-------|
| **Issue ID** | [40090436](https://issues.chromium.org/issues/40090436) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU>SwiftShader |
| **Platforms** | Linux, Mac, Windows |
| **Reporter** | [Deleted User] |
| **Assignee** | ca...@chromium.org |
| **Created** | 2018-02-09 |
| **Bounty** | $3,000.00 |

## Description

The attached testcase results in a use after free in asan-linux-release-535552 when hardware acceleration is disabled.

The following is the webGL renderer in my case:
Vendor:	WebKit
Renderer: WebKit WebGL
Unmasked Vendor: Google Inc.
Unmasked Renderer: Google SwiftShader

heap-use-after-free on address 0x60200002c13c at pc 0x7fa8bac1c497 bp 0x7fa89b6329e0 sp 0x7fa89b6329d8
READ of size 4 at 0x60200002c13c thread T13
    #0 0x7fa8bac1c496 in sw::Renderer::finishRendering(sw::Renderer::Task&) third_party/swiftshader/src/Renderer/Renderer.cpp:976:21

0x60200002c13c is located 12 bytes inside of 16-byte region [0x60200002c130,0x60200002c140)
freed by thread T0 (chrome) here:
    #0 0x55c534a3f552 in operator delete(void*) /b/build/slave/linux_upload_clang/build/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cc:149:3
    #1 0x7fa8bae19bc2 in es2::Query::~Query() third_party/swiftshader/src/OpenGL/libGLESv2/Query.cpp:35:2

previously allocated by thread T0 (chrome) here:
    #0 0x55c534a3e972 in operator new(unsigned long) /b/build/slave/linux_upload_clang/build/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cc:92:3
    #1 0x7fa8bae19cc6 in es2::Query::begin() third_party/swiftshader/src/OpenGL/libGLESv2/Query.cpp:57:12
    #2 0x55c5401b79af in gpu::gles2::GLES2DecoderImpl::HandleBeginQueryEXT(unsigned int, void const volatile*) gpu/command_buffer/service/gles2_cmd_decoder.cc:16806:19
    #3 0x55c54020d7dd in gpu::error::Error gpu::gles2::GLES2DecoderImpl::DoCommandsImpl<false>(unsigned int, void const volatile*, int, int*) gpu/command_buffer/service/gles2_cmd_decoder.cc:5568:18
    #4 0x55c5400f719a in gpu::CommandBufferService::Flush(int, gpu::AsyncAPIInterface*) gpu/command_buffer/service/command_buffer_service.cc:90:18
    #5 0x55c54136c2c4 in gpu::CommandBufferStub::OnAsyncFlush(int, unsigned int, bool) gpu/ipc/service/command_buffer_stub.cc:634:20

## Attachments

- [asan_swrender.log](attachments/asan_swrender.log) (text/plain, 9.4 KB)
- [swrender.html](attachments/swrender.html) (text/plain, 2.3 KB)

## Timeline

### in...@chromium.org (2018-02-09)

[Empty comment from Monorail migration]

[Monorail components: Internals>GPU>SwiftShader]

### cl...@chromium.org (2018-02-09)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4561719964467200.

### cl...@chromium.org (2018-02-09)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5118447986671616.

### in...@chromium.org (2018-02-09)

capn@, sugoi@ - can you please take a look, this reproduces very easily locally. Unsure why this is not reproducing on ClusterFuzz.

### cl...@chromium.org (2018-02-09)

Detailed report: https://clusterfuzz.com/testcase?key=4561719964467200

Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x60900161bb2c
Crash State:
  sw::Renderer::finishRendering
  es2::Query::~Query
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=531706:531716

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=4561719964467200

See https://github.com/google/clusterfuzz-tools for more information.

### sh...@chromium.org (2018-02-09)

[Empty comment from Monorail migration]

### ca...@chromium.org (2018-02-10)

Please add affected OSs.

### go...@chromium.org (2018-02-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-02-12)

This issue is marked as a release blocker with no OS labels associated. Please add an appropriate OS label.

All release blocking issues should have OS labels associated to it, so that the issue can tracked and promptly verified, once it gets fixed.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cm...@google.com (2018-02-12)

capn@ add affected OSs

### aw...@chromium.org (2018-02-12)

The initial report and clusterfuzz regression range are both M66.

### mb...@chromium.org (2018-02-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-02-27)

capn: Uh oh! This issue still open and hasn't been updated in the last 18 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### su...@chromium.org (2018-02-27)

[Empty comment from Monorail migration]

### cl...@chromium.org (2018-02-28)

ClusterFuzz has detected this issue as fixed in range 539590:539593.

Detailed report: https://clusterfuzz.com/testcase?key=4561719964467200

Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x60900161bb2c
Crash State:
  sw::Renderer::finishRendering
  es2::Query::~Query
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=531706:531716
Fixed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=539590:539593

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=4561719964467200

See https://github.com/google/clusterfuzz-tools for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### sh...@chromium.org (2018-03-07)

[Empty comment from Monorail migration]

### ct...@chromium.org (2018-03-23)

capn@: Is there any work remaining on this? From the date of clusterfuzz detecting this fixed, I think this made it into M66, and wouldn't need a merge. Does that sounds right?

### mm...@chromium.org (2018-03-30)

capn@, please take a look at c#17 and mark this Fixed if it is.

### ca...@chromium.org (2018-03-30)

I assume this was fixed by https://chromium-review.googlesource.com/939985

@dtapuska, does that seem probable? Can we do anything to help make the root cause of such a bug easier to detect?

### sh...@chromium.org (2018-03-30)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-10)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-04-10)

Nice one! The VRP panel decided to award $3,000 for this report.

### aw...@chromium.org (2018-04-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-04-27)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-04-27)

This bug requires manual review: M67 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), kbleicher@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2018-04-27)

CL listed at #19 ( https://chromium-review.googlesource.com/939985) is already in M67. I don't think any merge is needed. Removing " Merge-Review-67" label.

awhalley@, pls double check. Thank you.

### sh...@chromium.org (2018-07-06)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2018-07-06)

This issue was migrated from crbug.com/chromium/810736?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40090436)*
