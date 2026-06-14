# OOB write in sw::VertexProgram::WHILE

| Field | Value |
|-------|-------|
| **Issue ID** | [40093456](https://issues.chromium.org/issues/40093456) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU>SwiftShader |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | cd...@gmail.com |
| **Assignee** | ca...@chromium.org |
| **Created** | 2018-12-14 |
| **Bounty** | $3,000.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36

Steps to reproduce the problem:
1. download and unzip the release asan chromium :asan-linux-release-613801
2. Run ./chrome --disable-gpu crash.html

What is the expected behavior?

What went wrong?
In third_party/swiftshader/src/Shader/VertexProgram.cpp:1467

void VertexProgram::WHILE(const Src &temporaryRegister)
	{
		enableIndex++;

		BasicBlock *loopBlock = Nucleus::createBasicBlock();
		BasicBlock *testBlock = Nucleus::createBasicBlock();
		BasicBlock *endBlock = Nucleus::createBasicBlock();

		loopRepTestBlock[loopRepDepth] = testBlock;<---loopRepDepth lacks of check
		loopRepEndBlock[loopRepDepth] = endBlock;
         ...
        }
The member loopRepDepth lacks of check,if it is greater than 4,OOB write happened.

POC sees in crash.html.

This buggy code won't cause a crash cuz the OOB write occurs inside the object memory and the data labelBlock has the same structure with loopRepEndBlock.But it could affect the control-flow of JIT code.

Did this work before? N/A 

Chrome version: 73.0.3639.0  Channel: stable
OS Version: 16.04
Flash Version:

## Attachments

- [utility.js](attachments/utility.js) (text/plain, 2.0 KB)
- [gl-matrix-min.js](attachments/gl-matrix-min.js) (text/plain, 52.9 KB)
- [crash.html](attachments/crash.html) (text/plain, 3.2 KB)

## Timeline

### ca...@chromium.org (2018-12-14)

[Empty comment from Monorail migration]

[Monorail components: Internals>GPU>SwiftShader]

### ca...@chromium.org (2018-12-14)

[Empty comment from Monorail migration]

### cl...@chromium.org (2018-12-14)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4829151468716032.

### cl...@chromium.org (2018-12-14)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6200330850926592.

### cl...@chromium.org (2018-12-14)

Testcase 6200330850926592 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=6200330850926592.

### cl...@chromium.org (2018-12-14)

Testcase 4829151468716032 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=4829151468716032.

### sh...@chromium.org (2018-12-15)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-12-15)

[Empty comment from Monorail migration]

### ca...@chromium.org (2018-12-16)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-12-28)

sugoi: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-01-12)

sugoi: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chromium.org (2019-01-17)

The following revision refers to this bug:
  https://swiftshader.googlesource.com/SwiftShader.git/+/48d47a4912684bfa4d23d3cdaab60046bf3d0468

commit 48d47a4912684bfa4d23d3cdaab60046bf3d0468
Author: Alexis Hetu <sugoi@google.com>
Date: Thu Jan 17 18:44:38 2019

Fixed all OOB accesses in VertexProgram and PixelProgram

A lot of arrays in VertexProgram and PixelProgram have fixed sizes,
so programs that have more nested loops or ifs or deeper call stacks
can cause OOB accesses, which causes security issues in Chromium.

Index clamping was added to prevent any OOB memory accesses here.

This could eventually be fixed properly by first verifying these sizes
and giving shader compile errors when these limits are exceeded.

https://crbug.com/chromium/915197 chromium:915206 chromium:915218 b/116373662

Change-Id: I2d0710ed0ce6585f139cba49d5b5d8c909ae6391
Reviewed-on: https://swiftshader-review.googlesource.com/c/23568
Tested-by: Alexis Hétu <sugoi@google.com>
Reviewed-by: Corentin Wallez <cwallez@google.com>

[modify] https://crrev.com/48d47a4912684bfa4d23d3cdaab60046bf3d0468/src/Common/Types.hpp
[modify] https://crrev.com/48d47a4912684bfa4d23d3cdaab60046bf3d0468/src/Main/Config.hpp
[modify] https://crrev.com/48d47a4912684bfa4d23d3cdaab60046bf3d0468/src/Shader/PixelProgram.cpp
[modify] https://crrev.com/48d47a4912684bfa4d23d3cdaab60046bf3d0468/src/Shader/PixelProgram.hpp
[modify] https://crrev.com/48d47a4912684bfa4d23d3cdaab60046bf3d0468/src/Shader/Shader.cpp
[modify] https://crrev.com/48d47a4912684bfa4d23d3cdaab60046bf3d0468/src/Shader/VertexProgram.cpp
[modify] https://crrev.com/48d47a4912684bfa4d23d3cdaab60046bf3d0468/src/Shader/VertexProgram.hpp


### ct...@chromium.org (2019-01-28)

Security sheriff here: Does the CL in c#12 fix the vulnerability, or is there still more work to be done here?

### ca...@chromium.org (2019-01-28)

[Empty comment from Monorail migration]

### su...@chromium.org (2019-01-28)

The vulnerability is fixed, but the rendering is still incorrect, which is why I left the bug open.

### su...@chromium.org (2019-01-28)

Removing Security flag, lowering priority to P2 and assigning to capn@ for correctness fix.

### su...@chromium.org (2019-01-29)

OOB problem fixed.

Correctness issue created here:
https://b.corp.google.com/issues/123587120

### sh...@chromium.org (2019-01-30)

[Empty comment from Monorail migration]

### ct...@chromium.org (2019-01-30)

Restoring security labels.

### na...@google.com (2019-02-04)

[Empty comment from Monorail migration]

### na...@google.com (2019-02-07)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### na...@google.com (2019-02-07)

Congrats! The Panel has decided to reward $3000 for this report :) 

### na...@google.com (2019-02-07)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-05-08)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mm...@chromium.org (2019-05-13)

[Empty comment from Monorail migration]

### mm...@chromium.org (2019-05-17)

[Empty comment from Monorail migration]

### aw...@google.com (2019-07-08)

[Empty comment from Monorail migration]

### ad...@google.com (2019-11-20)

[Empty comment from Monorail migration]

### ad...@google.com (2020-01-03)

[Empty comment from Monorail migration]

### is...@google.com (2020-01-03)

This issue was migrated from crbug.com/chromium/915206?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/915208]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093456)*
