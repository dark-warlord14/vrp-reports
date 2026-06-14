# heap-use-after-free in AsyncCompileJob

| Field | Value |
|-------|-------|
| **Issue ID** | [40094206](https://issues.chromium.org/issues/40094206) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>WebAssembly |
| **Platforms** | Linux |
| **Reporter** | cd...@gmail.com |
| **Assignee** | cl...@chromium.org |
| **Created** | 2019-03-05 |
| **Bounty** | $3,000.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36

Steps to reproduce the problem:
1. download and unzip the release asan chromium :asan-linux-release-637662
2. Set up a webserver and put poc.html and the "res" dir in the same dir.
3. Run ./chrome  crash.html

What is the expected behavior?

What went wrong?
Can stably get UAF crash.

1.When finished baseline compilation,the CompilationStateCallback would post a task to notify that job had finished and pass a raw pointer of job to the task.
2.When we create a window that not for child_local_root_frame and close it,the RenderWidget would close immediately,which leads to the related isolate release all async compilation job.

Once the task in 1 has already been in task_runner and 2 happened at the same time,the use of raw pointer in  callback leads to a UAF bug. 

Did this work before? N/A 

Chrome version: 74.0.3726.0  Channel: stable
OS Version: 16.04
Flash Version:

## Attachments

- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)

## Timeline

### cl...@chromium.org (2019-03-06)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4870032933912576.

### oc...@chromium.org (2019-03-06)

can't reproduce.  clemensh@, could you please take a look at the provided stacktrace to see if there's something obvious here?

[Monorail components: Blink>JavaScript>WebAssembly]

### cl...@chromium.org (2019-03-06)

Testcase 4870032933912576 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=4870032933912576.

### cd...@gmail.com (2019-03-06)

Could you please try to refresh the page for several times if can not repro?

### cl...@chromium.org (2019-03-06)

Can reproduce, thanks for the report. Will look into it tomorrow.

### oc...@chromium.org (2019-03-07)

Assuming head impact here based on the version provided in the first report. Does this reproduce on stable/beta versions?

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-03-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/30fac0de6198074682aeb88829b59365778f918b

commit 30fac0de6198074682aeb88829b59365778f918b
Author: Clemens Hammacher <clemensh@chromium.org>
Date: Thu Mar 07 10:24:39 2019

[wasm] Fix UAF in AsyncCompileJob callbacks

Execute foreground tasks triggered by the {CompilationStateCallback}
via the {CompileStep} mechanism of {AsyncCompileJob} such that they get
cancelled when the AsyncCompileJob dies.

R=ahaas@chromium.org

Bug: chromium:938311
Change-Id: I2082f93f47988c014c8dee3ddf3e9b2940f6f531
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/1507674
Reviewed-by: Andreas Haas <ahaas@chromium.org>
Commit-Queue: Clemens Hammacher <clemensh@chromium.org>
Cr-Commit-Position: refs/heads/master@{#60082}
[modify] https://crrev.com/30fac0de6198074682aeb88829b59365778f918b/src/wasm/module-compiler.cc
[modify] https://crrev.com/30fac0de6198074682aeb88829b59365778f918b/src/wasm/module-compiler.h


### cl...@chromium.org (2019-03-07)

Got a more reliable reproducer, will try to run it through ClusterFuzz again.

### cl...@chromium.org (2019-03-07)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6247632109436928.

### cl...@chromium.org (2019-03-07)

Local bisect produced:
You are probably looking for a change made after 628004 (known good), but no later than 628009 (first known bad).
CHANGELOG URL:
  https://chromium.googlesource.com/chromium/src/+log/c000f9169e1071a5ff646983c22e8ca5e326c527..c18bad54fd63d51cd40a214790daee6e9f641477

This range contains this v8 roll: 93c0fb600ca54ab0d12d05e2d99475c2cd1ea034
Which contains: 5f6de71a375a6afda5aabb4eeeebd0e4b3c07aa9 ([wasm] Call callbacks from background)
This seems very plausible. That CL first shipped in 74.0.3690.0.

### cl...@chromium.org (2019-03-07)

Testcase 6247632109436928 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=6247632109436928.

### sh...@chromium.org (2019-03-07)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-03-07)

[Empty comment from Monorail migration]

### na...@google.com (2019-03-11)

[Empty comment from Monorail migration]

### cl...@chromium.org (2019-03-13)

This should be merge to M-74.

### cl...@chromium.org (2019-03-13)

[Empty comment from Monorail migration]

### cl...@chromium.org (2019-03-13)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-03-14)

Your change meets the bar and is auto-approved for M74. Please go ahead and merge the CL to branch 3729 (refs/branch-heads/3729) manually. Please contact milestone owner if you have questions.
Merge instructions: https://www.chromium.org/developers/how-tos/drover
Owners: govind@(Android), kariahda@(iOS), dgagnon@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cl...@chromium.org (2019-03-14)

Merged in https://crrev.com/c/1523328 (bugdroid asleep?).

### na...@google.com (2019-03-14)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### na...@google.com (2019-03-14)

Congrats! The Panel decided to reward $3,000 for this report :) 

### cl...@chromium.org (2019-03-15)

Congrats, well deserved! :D
Thanks for the report!

### cd...@gmail.com (2019-03-15)

Wow,thank you for the reward.Have good day.：)

### aw...@google.com (2019-03-15)

[Empty comment from Monorail migration]

### mm...@chromium.org (2019-05-13)

[Empty comment from Monorail migration]

### mm...@chromium.org (2019-05-17)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-06-13)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cl...@chromium.org (2020-02-17)

[Empty comment from Monorail migration]

### is...@google.com (2020-02-17)

This issue was migrated from crbug.com/chromium/938311?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail blocking: crbug.com/chromium/928199, crbug.com/chromium/937784]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094206)*
