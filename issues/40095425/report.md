# heap-use-after-free in ContextProvider

| Field | Value |
|-------|-------|
| **Issue ID** | [40095425](https://issues.chromium.org/issues/40095425) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>Canvas, Blink>Paint, Blink>WebGL, Internals>GPU |
| **Platforms** | Linux |
| **Reporter** | cd...@gmail.com |
| **Assignee** | kh...@chromium.org |
| **Created** | 2019-06-18 |
| **Bounty** | $3,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36

Steps to reproduce the problem:
1.Build asan 77.0.3828.0 version of chrome
2.Run ./chrome poc.html

What is the expected behavior?

What went wrong?
3.Reproduce uaf immediately.

Did this work before? N/A 

Chrome version: Version 77.0.3828.0 (Developer Build) (64-bit)  Channel: dev
OS Version: 18.04
Flash Version:

## Attachments

- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)

## Timeline

### cl...@chromium.org (2019-06-18)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6283760601006080.

### cl...@chromium.org (2019-06-18)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5470827008622592.

### me...@chromium.org (2019-06-18)

[Empty comment from Monorail migration]

[Monorail components: Blink>Canvas Internals>GPU]

### cl...@chromium.org (2019-06-18)

Detailed report: https://clusterfuzz.com/testcase?key=5470827008622592

Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x60d00007ba28
Crash State:
  blink::OffscreenCanvasRenderingContext2D::PushFrame
  blink::OffscreenCanvas::BeginFrame
  viz::mojom::blink::CompositorFrameSinkClientStubDispatch::Accept
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=670082:670083

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5470827008622592

See https://github.com/google/clusterfuzz-tools for instructions to reproduce this bug locally.

### me...@google.com (2019-06-18)

Not sure if this is a GPU or canvas issue. Ken, can you please help triage?

[Monorail components: Blink>WebGL]

### kb...@chromium.org (2019-06-18)

This is a canvas / OffscreenCanvas issue. fserb@ could you please triage?


### cl...@chromium.org (2019-06-18)

Detailed report: https://clusterfuzz.com/testcase?key=6283760601006080

Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x60d0000822f8
Crash State:
  blink::OffscreenCanvasRenderingContext2D::PushFrame
  blink::OffscreenCanvas::BeginFrame
  viz::mojom::blink::CompositorFrameSinkClientStubDispatch::Accept
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=668982:668987

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6283760601006080

Additional requirements: Requires HTTP

See https://github.com/google/clusterfuzz-tools for instructions to reproduce this bug locally.

### sh...@chromium.org (2019-06-19)

Setting milestone and target because of Security_Impact=Head and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-06-19)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-06-19)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### fs...@chromium.org (2019-06-20)

Khushal,
I think this is related to the new resources.

I couldn't repro locally, but I tried to find where we would be  destroying the 3DProvider and not releasing the pointer, but I couldn't. Ideas?

### kh...@chromium.org (2019-06-20)

Looks like I missed some null context checks: https://chromium-review.googlesource.com/c/chromium/src/+/1670290

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-06-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/e8ad9851a7870557f7fe2b5670ca4371af82dd71

commit e8ad9851a7870557f7fe2b5670ca4371af82dd71
Author: Khushal <khushalsagar@chromium.org>
Date: Fri Jun 21 22:53:09 2019

canvas2d: Always check for lost context.

R=fserb@chromium.org

Bug: 976136
Change-Id: If2bd977fca8c7fecff485c7735abc5c487f8666a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1670290
Auto-Submit: Khushal <khushalsagar@chromium.org>
Commit-Queue: Fernando Serboncini <fserb@chromium.org>
Reviewed-by: Fernando Serboncini <fserb@chromium.org>
Cr-Commit-Position: refs/heads/master@{#671442}

[modify] https://crrev.com/e8ad9851a7870557f7fe2b5670ca4371af82dd71/third_party/blink/renderer/platform/graphics/canvas_resource_provider.cc


### kh...@chromium.org (2019-06-21)

[Empty comment from Monorail migration]

### kh...@chromium.org (2019-06-21)

[Empty comment from Monorail migration]

### cl...@chromium.org (2019-06-21)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Blink>Paint]

### sh...@chromium.org (2019-06-22)

[Empty comment from Monorail migration]

### cl...@chromium.org (2019-06-22)

ClusterFuzz testcase 5747069523984384 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_msan_content_shell_drt&range=671439:671442

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### na...@google.com (2019-06-24)

[Empty comment from Monorail migration]

### na...@google.com (2019-07-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### pa...@chromium.org (2019-07-17)

Congrats! The Panel decided to reward $3,000 for this report!

### cd...@gmail.com (2019-07-18)

Thanks for the reward, Cheers!

### na...@google.com (2019-07-18)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-09-28)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/976136?no_tracker_redirect=1

[Multiple monorail components: Blink>Canvas, Blink>Paint, Blink>WebGL, Internals>GPU]
[Monorail mergedwith: crbug.com/chromium/977587]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095425)*
