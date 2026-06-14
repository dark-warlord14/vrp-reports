# OOB write in sw::VertexProgram::Program

| Field | Value |
|-------|-------|
| **Issue ID** | [40093453](https://issues.chromium.org/issues/40093453) |
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
VertexProgram lacks of check the labelIndex when handling CALL inst:

in third_party/swiftshader/src/Shader/VertexProgram.cpp:99

		for(size_t i = 0; i < shader->getLength(); i++)
		{
			const Shader::Instruction *instruction = shader->getInstruction(i);
			Shader::Opcode opcode = instruction->opcode;

			if(opcode == Shader::OPCODE_CALL || opcode == Shader::OPCODE_CALLNZ)
			{
				const Dst &dst = instruction->dst;

				ASSERT(callRetBlock[dst.label].size() == dst.callSite);
				callRetBlock[dst.label].push_back(Nucleus::createBasicBlock());<---dst.lable may greater than 2048
			}
		}

The labelBlock's size is 2048,so if dst.lable is larger than that ,OOB write happened.

The poc is simple:construct more than 2048 functions and call them.And there's a limitation that the compiler allows less
than 4096 registers.So most of the function could have no args and retrun values.

An another exploit point (a stack buffer overflow read) takes place before this OOB write.

in third_party/swiftshader/src/Shader/Shader.cpp:1878

	void Shader::analyzeCallSites()
	{
		int callSiteIndex[2048] = {0};

		for(auto &inst : instruction)
		{
			if(inst->opcode == OPCODE_CALL || inst->opcode == OPCODE_CALLNZ)
			{
				int label = inst->dst.label;

				inst->dst.callSite = callSiteIndex[label]++;<---lack of check
			}
		}
	}

If label is more than 2048,could write the meta-data of stack into dst.callSite.

Did this work before? N/A 

Chrome version: 73.0.3639.0  Channel: stable
OS Version: 16.04
Flash Version:

## Attachments

- [utility.js](attachments/utility.js) (text/plain, 2.0 KB)
- [log](attachments/log) (text/plain, 2.6 KB)
- [crash.html](attachments/crash.html) (text/plain, 87.5 KB)

## Timeline

### ca...@chromium.org (2018-12-14)

[Empty comment from Monorail migration]

[Monorail components: Internals>GPU>SwiftShader]

### ca...@chromium.org (2018-12-14)

capn: Assigning to you (together with the seemingly similar bugs listed below) since you've been active in the related files. Can you take a look (and reassign as appropriate)? Thanks.

### ca...@chromium.org (2018-12-14)

[Empty comment from Monorail migration]

### ca...@chromium.org (2018-12-14)

Similar bugs:
crbug.com/915201
crbug.com/915206
crbug.com/915208

### cl...@chromium.org (2018-12-14)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5450330659356672.

### sh...@chromium.org (2018-12-15)

[Empty comment from Monorail migration]

### cl...@chromium.org (2018-12-15)

Detailed report: https://clusterfuzz.com/testcase?key=5450330659356672

Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Stack-buffer-overflow READ 4
Crash Address: 0x7fab4b7db820
Crash State:
  sw::Shader::analyzeCallSites
  sw::VertexShader::analyze
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=500345:500471

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5450330659356672

See https://github.com/google/clusterfuzz-tools for instructions to reproduce this bug locally.

The recommended severity (Security_Severity-Medium) is different from what was assigned to the bug. Please double check the accuracy of the assigned severity.

### ca...@chromium.org (2018-12-16)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-12-28)

sugoi: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### su...@chromium.org (2019-01-10)

Note that both PixelProgram and VertexProgram are affected.

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

Security sheriff here: Does the CL in c#11 fix the vulnerability, or is there still more work to be done here?

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

### cl...@chromium.org (2019-02-05)

ClusterFuzz testcase 5363100678881280 is still reproducing on tip-of-tree build (trunk).

Please re-test your fix against this testcase and if the fix was incorrect or incomplete, please re-open the bug. Otherwise, ignore this notification and add ClusterFuzz-Wrong label.

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

### cd...@gmail.com (2019-05-09)

Hello natashapabrai@, won't this one , https://crbug.com/chromium/915206  and https://crbug.com/chromium/915218 get the CVE id? 

### aw...@google.com (2019-07-08)

[Empty comment from Monorail migration]

### ad...@google.com (2019-11-20)

[Empty comment from Monorail migration]

### ad...@google.com (2020-01-03)

[Empty comment from Monorail migration]

### is...@google.com (2020-01-03)

This issue was migrated from crbug.com/chromium/915197?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/915201]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093453)*
