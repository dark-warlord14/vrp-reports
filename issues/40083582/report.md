# Crash (assert) in blink::AudioDelayDSPKernel::process

| Field | Value |
|-------|-------|
| **Issue ID** | [40083582](https://issues.chromium.org/issues/40083582) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Media>Audio, Blink>WebAudio |
| **Platforms** | Linux |
| **Reporter** | at...@gmail.com |
| **Assignee** | mo...@google.com |
| **Created** | 2016-01-30 |
| **Bounty** | $1,500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5213979443462144

Fuzzer: attekett_webaudio_fuzzer
Job Type: linux_asan_chrome_chromeos
Platform Id: linux

Crash Type: UNKNOWN
Crash Address: 0x7f5f69e0d800
Crash State:
  blink::AudioDelayDSPKernel::process
  blink::AudioDSPKernelProcessor::process
  blink::AudioBasicProcessorHandler::process
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_chromeos&range=366571:366586

Minimized Testcase (0.67 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95i5-lPKHp1PyWgV8WkcaumLDzOfunYiMZSQEJ49jise1b9Xi0he5uK3WMhLBjr8w4Qb6EA5yqP9mjA4zIV6GBYORzH9WM762U9igwsZUjXJwF4o7ndjIj-6FZiFyTGHnotGyudwn1cGGObmGRRfb_9BH6UFQ

Filer: inferno

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

## Timeline

### in...@chromium.org (2016-01-30)

Author: bratell
Component: chromium
Changelist: https://chromium.googlesource.com/chromium/src//+/881b6566ecacfe9154e1f115c588e76cec8a513a
Time: Tue Dec 22 10:58:39 2015
File AudioDelayDSPKernel.cpp is changed in this cl (and is part of stack frame #0, "blink::AudioDelayDSPKernel::process")
Minimum distance from crash line to modified line: 19. (file: AudioDelayDSPKernel.cpp, crashed on: 143, modified: 124).

Suspected Component: chromium
Suspected Cr- Label: Cr-Blink-WebAudio

### in...@chromium.org (2016-01-30)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-01-30)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-01-30)

This medium+ severity security issue is a regression on trunk.

Please fix this asap. If you are unable to look into this soon, please revert your change.

- Your friendly ClusterFuzz

### [Deleted User] (2016-02-01)

It's an ASSERT triggered by the NaN in the fuzzer test.

### [Deleted User] (2016-02-01)

Possible fix https://codereview.chromium.org/1657763002/

### mm...@chromium.org (2016-02-01)

[Empty comment from Monorail migration]

### mm...@chromium.org (2016-02-01)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-02-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/f6e3d4665d9261e4fef2b5931e4c75ecb5e032bf

commit f6e3d4665d9261e4fef2b5931e4c75ecb5e032bf
Author: bratell <bratell@opera.com>
Date: Mon Feb 01 18:59:37 2016

Handle NaN in the Audio delay curves.

Since switching from std::min to clampTo NaN has caused ASSERTs.
This restores the old behaviour of no ASSERT and a delay interpreted
as maxDelayTime.

BUG=582699
R=rtoy@chromium.org

Review URL: https://codereview.chromium.org/1657763002

Cr-Commit-Position: refs/heads/master@{#372710}

[modify] http://crrev.com/f6e3d4665d9261e4fef2b5931e4c75ecb5e032bf/third_party/WebKit/Source/platform/audio/AudioDelayDSPKernel.cpp


### in...@chromium.org (2016-02-01)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-02-01)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-02-02)

ClusterFuzz has detected this issue as fixed in range 372666:372742.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5213979443462144

Fuzzer: attekett_webaudio_fuzzer
Job Type: linux_asan_chrome_chromeos
Platform Id: linux

Crash Type: UNKNOWN
Crash Address: 0x7f5f69e0d800
Crash State:
  blink::AudioDelayDSPKernel::process
  blink::AudioDSPKernelProcessor::process
  blink::AudioBasicProcessorHandler::process
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_chromeos&range=366571:366586
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_chromeos&range=372666:372742

Minimized Testcase (0.67 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95i5-lPKHp1PyWgV8WkcaumLDzOfunYiMZSQEJ49jise1b9Xi0he5uK3WMhLBjr8w4Qb6EA5yqP9mjA4zIV6GBYORzH9WM762U9igwsZUjXJwF4o7ndjIj-6FZiFyTGHnotGyudwn1cGGObmGRRfb_9BH6UFQ

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### [Deleted User] (2016-02-02)

[Empty comment from Monorail migration]

### ss...@google.com (2016-03-21)

Renaming Blink>Audio to Blink>Media>Audio for better characterization

[Monorail components: -Blink>Audio Blink>Media>Audio]

### sh...@chromium.org (2016-05-10)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ti...@google.com (2016-06-30)

(part of backlog reward round)

Congrats - $1500 for this report ($1k for the bug, 500 for the fuzzer).

### aw...@chromium.org (2016-06-30)

[Comment Deleted]

### aw...@chromium.org (2016-06-30)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-07-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/582699?no_tracker_redirect=1

[Multiple monorail components: Blink>Media>Audio, Blink>WebAudio]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083582)*
