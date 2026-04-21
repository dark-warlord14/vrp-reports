# [sparkplug]baseline optimize  function PrologueFillFrame   register_count can be 0 .which can lead to code execution

| Field | Value |
|-------|-------|
| **Issue ID** | [40054891](https://issues.chromium.org/issues/40054891) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Compiler |
| **Platforms** | Linux |
| **Reporter** | vi...@gmail.com |
| **Assignee** | le...@chromium.org |
| **Created** | 2021-02-18 |
| **Bounty** | $5,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36

Steps to reproduce the problem:
1.run the poc file with the commandline  d8  --sparkplug --allow-natives-syntax  argmuents

What is the expected behavior?
register_count  should always check no matter debug or release version

What went wrong?
no check register_count  in release version ,which maybe lead to RCE 

Did this work before? N/A 

Chrome version: 87.0.4280.88  Channel: dev
OS Version: 10.0
Flash Version: 

git hash: c174643b08210c7136fb7cb588a62cfd42c25dcb
on ubuntu 18.04

## Attachments

- [poc.js](attachments/poc.js) (text/plain, 645 B)

## Timeline

### vi...@gmail.com (2021-02-18)

crash stack on debug version;
#
# Fatal error in ../../src/baseline/x64/baseline-compiler-x64-inl.h, line 422
# Debug check failed: register_count / kLoopUnrollSize > 0 (0 vs. 0).
#
#
#
#FailureMessage Object: 0x7ffc3f5a20c0
==== C stack trace ===============================

    /root/newv8/v8/out/x64.debug/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x1e) [0x7f303f78cf5e]
    /root/newv8/v8/out/x64.debug/libv8_libplatform.so(+0x55b4d) [0x7f303f70bb4d]
    /root/newv8/v8/out/x64.debug/libv8_libbase.so(V8_Fatal(char const*, int, char const*, ...)+0x231) [0x7f303f771651]
    /root/newv8/v8/out/x64.debug/libv8_libbase.so(+0x4101c) [0x7f303f77101c]
    /root/newv8/v8/out/x64.debug/libv8_libbase.so(V8_Dcheck(char const*, int, char const*)+0x27) [0x7f303f7716f7]
    /root/newv8/v8/out/x64.debug/libv8.so(v8::internal::baseline::BaselineCompiler::PrologueFillFrame()+0x393) [0x7f303d9cdf73]
    /root/newv8/v8/out/x64.debug/libv8.so(v8::internal::baseline::BaselineCompiler::Prologue()+0x11b) [0x7f303d9cdbcb]
    /root/newv8/v8/out/x64.debug/libv8.so(v8::internal::baseline::BaselineCompiler::GenerateCode()+0x38e) [0x7f303d9cf64e]
    /root/newv8/v8/out/x64.debug/libv8.so(v8::internal::GenerateBaselineCode(v8::internal::Isolate*, v8::internal::Handle<v8::internal::SharedFunctionInfo>)+0x156) [0x7f303da16066]
    /root/newv8/v8/out/x64.debug/libv8.so(+0x2431703) [0x7f303dae8703]
    /root/newv8/v8/out/x64.debug/libv8.so(v8::internal::Compiler::CompileBaseline(v8::internal::Isolate*, v8::internal::Handle<v8::internal::JSFunction>, v8::internal::Compiler::ClearExceptionFlag, v8::internal::IsCompiledScope*)+0x90) [0x7f303dae8410]
    /root/newv8/v8/out/x64.debug/libv8.so(+0x2f31d11) [0x7f303e5e8d11]
    /root/newv8/v8/out/x64.debug/libv8.so(v8::internal::Runtime_BytecodeBudgetInterruptFromBytecode(int, unsigned long*, v8::internal::Isolate*)+0x120) [0x7f303e5e8840]
    /root/newv8/v8/out/x64.debug/libv8.so(+0x1ccc51f) [0x7f303d38351f]
Received signal 4 ILL_ILLOPN 7f303f78a151
Illegal instruction (core dumped)


### [Deleted User] (2021-02-18)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-02-18)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5205158024511488.

### cl...@chromium.org (2021-02-18)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5688135686881280.

### jd...@chromium.org (2021-02-19)

verwaest@: can you help me triage this bug further? ClusterFuzz is struggling to repro it, but it appeared to repro for me at least.

[Monorail components: Blink>JavaScript]

### cl...@chromium.org (2021-02-19)

Sparkplug is disabled, so no security impact.

[Monorail components: -Blink>JavaScript Blink>JavaScript>Compiler]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-02-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/cd76e3607408a45dc260dec179b04f9368e3c7a1

commit cd76e3607408a45dc260dec179b04f9368e3c7a1
Author: Leszek Swirski <leszeks@chromium.org>
Date: Fri Feb 19 12:45:44 2021

[sparkplug] Fix frame fill

Change the frame fill to unconditionally subtract already pushed
registers from register count. This ensures that the decision to add a
push loop is dependent on the _remaining_ registers, not the _total_
registers.

Bug: v8:11420
Change-Id: Ide763654e66f0a8c827a00fca1b4a77be2052f76
Fixed: chromium:1179595
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2704672
Commit-Queue: Leszek Swirski <leszeks@chromium.org>
Commit-Queue: Igor Sheludko <ishell@chromium.org>
Auto-Submit: Leszek Swirski <leszeks@chromium.org>
Reviewed-by: Igor Sheludko <ishell@chromium.org>
Cr-Commit-Position: refs/heads/master@{#72863}

[modify] https://crrev.com/cd76e3607408a45dc260dec179b04f9368e3c7a1/src/baseline/x64/baseline-compiler-x64-inl.h
[modify] https://crrev.com/cd76e3607408a45dc260dec179b04f9368e3c7a1/src/baseline/arm64/baseline-compiler-arm64-inl.h


### [Deleted User] (2021-02-19)

[Empty comment from Monorail migration]

### [Deleted User] (2021-02-19)

[Empty comment from Monorail migration]

### am...@google.com (2021-03-04)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@google.com (2021-03-04)

Congratulations, virustacker@! The VRP Panel has decided to award you $5,000 for this report. A member of our finance team will be in touch soon to arrange payment. 
Nice work and thank you for reporting this issue! 

How would you like to be credited for this issue in release notes? 

### vi...@gmail.com (2021-03-04)

Thank you!    you can  use my twitter @ma1fan  

### am...@google.com (2021-03-05)

[Empty comment from Monorail migration]

### vi...@gmail.com (2021-03-11)

hello  amyressler, there is no one touch with me about the reward process. what's the status?

### am...@google.com (2021-03-11)

Hi, virustacker@, I just checked my notifications from the finance team and they report as of 8 March, "we have contacted the following researcher the begin the enrollment process : virustacker@gmail.com", please double-check your inbox and junk email. If you have not received an email from them about enrollment, please let me know and I will reach out to them to reinitiate the process. Thank you and apologies for the inconvenience. 

### vi...@gmail.com (2021-03-11)

Hello, amyressler,I have checked my email and junk mail,But I am not found the reward mail.

### am...@google.com (2021-03-11)

virustacker@ thanks for checking! I will reach out to finance and check on this. 

### am...@google.com (2021-03-12)

Hi, virustacker@. I have heard back from finance and there was a delay getting the enrollments sent out, but they have updated that they have initiated the initial enrollment message and will proceed with enrollment for all researchers from last week's reward processing immediately. We apologize for the delay. Please let me know if you don't receive an email about this by Monday. Thanks for your patience!



### vi...@gmail.com (2021-03-14)

Thank you, amyressler@ I have received enrollments,Thanks for you help!

### am...@google.com (2021-03-15)

Awesome, virustacker@ - you're very welcome and glad to hear you've received it! 

### [Deleted User] (2021-05-28)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2021-05-28)

This issue was migrated from crbug.com/chromium/1179595?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-03-07)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/chrome-blintz-user-guide

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40054891)*
