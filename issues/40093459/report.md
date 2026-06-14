# OOB operation in SwiftShader JIT code.

| Field | Value |
|-------|-------|
| **Issue ID** | [40093459](https://issues.chromium.org/issues/40093459) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU>SwiftShader |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | cd...@gmail.com |
| **Assignee** | ca...@chromium.org |
| **Created** | 2018-12-14 |
| **Bounty** | $1,000.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36

Steps to reproduce the problem:
1. download and unzip the release asan chromium :asan-linux-release-613801
2. Run ./chrome --disable-gpu crash.html

What is the expected behavior?

What went wrong?
Can stable get crash.
The class VertexProgram in third_party/swiftshader/src/Shader/VertexProgram.hpp has member:

52:Int enableIndex;
53:Array<Int4, 1 + 24> enableStack;

The enableIndex comes from insts of vertexshader and lacks of check.Once it is greater than the size of enablestack,the JIT code could leads to a wrong memory operation.

And another member has the same problem:

Int stackIndex;   
Array<UInt, 16> callStack;

The stackIndex is directly used without check.

This kind of code still exists in the PixelProgram.So could these be devided into different issus?

Did this work before? N/A 

Chrome version: 73.0.3639.0  Channel: stable
OS Version: 16.04
Flash Version:


## Attachments

- [utility.js](attachments/utility.js) (text/plain, 2.0 KB)
- [gl-matrix-min.js](attachments/gl-matrix-min.js) (text/plain, 52.9 KB)
- [log](attachments/log) (text/plain, 768 B)
- [crash.html](attachments/crash.html) (text/plain, 6.2 KB)
- [crash.html](attachments/crash_52955973.html) (text/plain, 6.0 KB)

## Timeline

### ca...@chromium.org (2018-12-14)

[Empty comment from Monorail migration]

[Monorail components: Internals>GPU>SwiftShader]

### ca...@chromium.org (2018-12-14)

sugoi: Can you take a look and further triage? Thanks.

### cl...@chromium.org (2018-12-14)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5958244297867264.

### cl...@chromium.org (2018-12-14)

Testcase 5958244297867264 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=5958244297867264.

### sh...@chromium.org (2018-12-15)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-12-28)

sugoi: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### su...@chromium.org (2019-01-08)

Verified placing the js files in the proper directories, but still can't reproduce locally.

### cd...@gmail.com (2019-01-09)

Sorry for the wrong js path in crash.html.
Please try this one.



### su...@chromium.org (2019-01-09)

Ok, got it. I was expecting a crash, which didn't happen, but I see the OOB memory access happening.

### cd...@gmail.com (2019-01-10)

Execuse me,but this crash.html does lead to a very stably crash once the page was loaded~

Did u mean #9 is to https://crbug.com/chromium/915208?

### su...@chromium.org (2019-01-10)

We might just be using different versions. The bug was logged against Chrome 67. I'm testing using Chrome 73 and I'm using top of tree SwiftShader rather than the one that's currently shipped with Chromium. There have been a few loop related fixes recently, so the behavior may have been modified.

In any case, since the OOB issue is reproducible and is the source of the crash you are experiencing, we can start with fixing that.

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


### sh...@chromium.org (2019-01-25)

sugoi: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ct...@chromium.org (2019-01-28)

Security sheriff here: Does the CL in c#12 fix the vulnerability, or is there still more work to be done here?

### su...@chromium.org (2019-01-28)

The vulnerability is fixed, but the rendering is still incorrect, which is why I left the bug open.

### su...@chromium.org (2019-01-28)

Removing Security flag, lowering priority to P2 and assigning to capn@ for correctness fix.

### ct...@chromium.org (2019-01-29)

We typically prefer to file a separate bug for non-security related followup work. Can we create a new bug for that and close this out? That way we can process the security bug as finished (VRP, etc.).

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

Congrats! The Panel has decided to reward $1000 for this report :) 

### na...@google.com (2019-02-07)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-05-08)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@google.com (2019-07-09)

[Empty comment from Monorail migration]

### ad...@google.com (2019-11-20)

[Empty comment from Monorail migration]

### ad...@google.com (2020-01-03)

[Empty comment from Monorail migration]

### is...@google.com (2020-01-03)

This issue was migrated from crbug.com/chromium/915218?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093459)*
