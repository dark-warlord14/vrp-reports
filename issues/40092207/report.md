# Heap-buffer-overflow in media::VideoFrame::visible_data

| Field | Value |
|-------|-------|
| **Issue ID** | [40092207](https://issues.chromium.org/issues/40092207) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Internals>Core |
| **Platforms** | Linux, Mac |
| **Reporter** | cl...@chromium.org |
| **Assignee** | mc...@chromium.org |
| **Created** | 2018-08-17 |
| **Bounty** | $1,500.00 |

## Description

Detailed report: https://clusterfuzz.com/testcase?key=6542630163578880

Fuzzer: attekett_surku_fuzzer
Job Type: linux_asan_chrome_media
Platform Id: linux

Crash Type: Heap-buffer-overflow READ 4
Crash Address: 0x603000134ccc
Crash State:
  media::VideoFrame::visible_data
  media::CopyRowsToRGBABuffer
  base::internal::Invoker<base::internal::BindState<void
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_media&range=583622:583623

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6542630163578880

Issue filed automatically.

See https://github.com/google/clusterfuzz-tools for more information.

## Attachments

- [clusterfuzz-testcase-6542630163578880.webm](attachments/clusterfuzz-testcase-6542630163578880.webm) (video/webm, 89.5 KB)

## Timeline

### cl...@chromium.org (2018-08-17)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Internals>Core]

### cl...@chromium.org (2018-08-17)

Automatically assigning owner based on suspected regression changelist https://chromium.googlesource.com/chromium/src/+/1e53b4ec05f2485450a177c372e38b6215341a1c (GMBVFPool: support I420A VideoFrames).

If this is incorrect, please let us know why and apply the Test-Predator-Wrong-CLs label. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### sh...@chromium.org (2018-08-17)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-08-17)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-08-17)

[Empty comment from Monorail migration]

### cl...@chromium.org (2018-08-17)

[Empty comment from Monorail migration]

### mc...@chromium.org (2018-08-18)

[Empty comment from Monorail migration]

### mc...@chromium.org (2018-08-18)

The problem uncovered by Asan, which I can repro on my machine, is that
we have a bunch of I420A videoframes, as expected, and then we get the
very last frame I420.  We don't expect that, and just try to access the
alpha channel and bam.

### mc...@chromium.org (2018-08-18)

Attaching the webm that causes the failure (nothing mysterious with it,
it's out friendly bear).

### bu...@chromium.org (2018-08-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/ecd725db6011e2b5a6f8f569e8585c7eb0ab38f2

commit ecd725db6011e2b5a6f8f569e8585c7eb0ab38f2
Author: Miguel Casas <mcasas@chromium.org>
Date: Mon Aug 20 22:10:46 2018

GMBVFPool: bail if VideoFrame format forces change of OutputFormat

ClusterFuzz encountered an issue if a given VideoFrame comes and
causes a change of OutputFormat: in the bug below, an I420 VF
was received after a series of I420A ones, and caused a crash
when the alpha channel was accessed. This might happen more
generally if the received VideoFrames cause a change of
OutputFormat and we access what we don't have.

This CL addresses that by comparing the current |output_format_|
with what is derived out of the incoming VideoFrame. If they
differ, we just bail.

Bug: 875158, 875670
Change-Id: I961b5bf95651a3888482957ee0b7acd48149d467
Reviewed-on: https://chromium-review.googlesource.com/1180543
Commit-Queue: Miguel Casas <mcasas@chromium.org>
Reviewed-by: Dale Curtis <dalecurtis@chromium.org>
Cr-Commit-Position: refs/heads/master@{#584574}
[modify] https://crrev.com/ecd725db6011e2b5a6f8f569e8585c7eb0ab38f2/media/video/gpu_memory_buffer_video_frame_pool.cc
[modify] https://crrev.com/ecd725db6011e2b5a6f8f569e8585c7eb0ab38f2/media/video/gpu_memory_buffer_video_frame_pool_unittest.cc


### cl...@chromium.org (2018-08-21)

ClusterFuzz has detected this issue as fixed in range 584573:584574.

Detailed report: https://clusterfuzz.com/testcase?key=6542630163578880

Fuzzer: attekett_surku_fuzzer
Job Type: linux_asan_chrome_media
Platform Id: linux

Crash Type: Heap-buffer-overflow READ 4
Crash Address: 0x603000134ccc
Crash State:
  media::VideoFrame::visible_data
  media::CopyRowsToRGBABuffer
  base::internal::Invoker<base::internal::BindState<void
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_media&range=583622:583623
Fixed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_media&range=584573:584574

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6542630163578880

See https://github.com/google/clusterfuzz-tools for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2018-08-21)

ClusterFuzz testcase 6542630163578880 is verified as fixed, so closing issue as verified.

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### sh...@chromium.org (2018-08-21)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-09-05)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-09-05)

Nice one! The VRP panel decided to award $1,000 for this, plus a $500 clusterfuzz bonus.

### aw...@chromium.org (2018-09-11)

[Empty comment from Monorail migration]

### aw...@google.com (2018-09-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-11-27)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/875158?no_tracker_redirect=1

[Monorail blocking: crbug.com/chromium/873345]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092207)*
