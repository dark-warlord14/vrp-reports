# Heap-use-after-free in blink::AudioBus::Zero

| Field | Value |
|-------|-------|
| **Issue ID** | [40087505](https://issues.chromium.org/issues/40087505) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>Media>Audio |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | cl...@chromium.org |
| **Assignee** | ho...@chromium.org |
| **Created** | 2017-04-30 |
| **Bounty** | $3,500.00 |

## Description

Detailed report: https://clusterfuzz.com/testcase?key=6078622650859520

Fuzzer: attekett_webaudio_fuzzer
Job Type: windows_asan_chrome
Platform Id: windows

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x0ec27680
Crash State:
  blink::AudioBus::Zero
  blink::AudioBus::CopyFrom
  blink::AudioDestinationHandler::Render
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=windows_asan_chrome&range=467817:467851

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6078622650859520


Issue filed automatically.

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

## Timeline

### cl...@chromium.org (2017-05-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-05-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-05-01)

This issue is a security regression. If you are not able to fix this quickly, please revert the change that introduced it.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2017-05-01)

[Empty comment from Monorail migration]

### pa...@chromium.org (2017-05-01)

hongchan, can you please take a look? Thanks!

[Monorail components: Blink>Media>Audio]

### ho...@chromium.org (2017-05-01)

I believe I have a tentative fix for this:
https://codereview.chromium.org/2854463002

I will land this soon.

### ho...@chromium.org (2017-05-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-05-02)

This issue is a security regression. If you are not able to fix this quickly, please revert the change that introduced it.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chromium.org (2017-05-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/d94da1744907ed1bb90e37756806841609b0cc52

commit d94da1744907ed1bb90e37756806841609b0cc52
Author: hongchan <hongchan@chromium.org>
Date: Tue May 02 18:55:46 2017

Improve thread creation in plaform/audio/AudioDestination

After the introduction of the new rendering thread for WebAudio in
AudioDestination, two racy situnations were observed by ClusterFuzz.

These race conditions become critical especially when the AudioContext
is in the tear-down stage; when the main thread is dumping its member
variables, the rendering thread is still trying to access them.

This CL moves the thread creation logic into Start() and Stop() methods
in AudioDestination. By doing so, the thread is always be in sync with
the associated audio device and the thread can be safely deleted when
the AudioContext goes away.

BUG=716358, 716945
TEST=(The local TSAN/ASAN passed the repro test cases.)

Review-Url: https://codereview.chromium.org/2853923002
Cr-Commit-Position: refs/heads/master@{#468726}

[modify] https://crrev.com/d94da1744907ed1bb90e37756806841609b0cc52/third_party/WebKit/Source/platform/audio/AudioDestination.cpp
[modify] https://crrev.com/d94da1744907ed1bb90e37756806841609b0cc52/third_party/WebKit/Source/platform/audio/AudioDestination.h


### ho...@chromium.org (2017-05-02)

[Empty comment from Monorail migration]

### cl...@chromium.org (2017-05-03)

ClusterFuzz has detected this issue as fixed in range 468701:468764.

Detailed report: https://clusterfuzz.com/testcase?key=6078622650859520

Fuzzer: attekett_webaudio_fuzzer
Job Type: windows_asan_chrome
Platform Id: windows

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x0ec27680
Crash State:
  blink::AudioBus::Zero
  blink::AudioBus::CopyFrom
  blink::AudioDestinationHandler::Render
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=windows_asan_chrome&range=467817:467851
Fixed: https://clusterfuzz.com/revisions?job=windows_asan_chrome&range=468701:468764

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6078622650859520


See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### sh...@chromium.org (2017-05-03)

[Empty comment from Monorail migration]

### ho...@chromium.org (2017-05-03)

Per #11, ClusterFuzz verified the fix.

### aw...@chromium.org (2017-05-15)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-05-15)

And $3,500 for this one :-)

### aw...@chromium.org (2017-05-15)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-05-18)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-08-09)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2017-08-09)

This issue was migrated from crbug.com/chromium/716945?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40087505)*
