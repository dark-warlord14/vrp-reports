# Security: Fatal error in ../../src/compiler/turboshaft/types.h

| Field | Value |
|-------|-------|
| **Issue ID** | [40065644](https://issues.chromium.org/issues/40065644) |
| **Status** | Accepted |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Compiler |
| **Platforms** | Linux |
| **Reporter** | sw...@gmail.com |
| **Assignee** | ni...@chromium.org |
| **Created** | 2023-06-12 |
| **Bounty** | $7,000.00 |

## Description

**VULNERABILITY DETAILS**

```
#  
# Fatal error in ../..--future  --allow-natives-syntax  --turboshaft-assert-types --always-turbofan/src/compiler/turboshaft/types.h, line 501  
# Debug check failed: 0 != special_values (0 vs. 0).  
#  
#  
#  
#FailureMessage Object: 0x7ffd5d9d7100  

```

**VERSION**  

v8: (08453b0d737a5ba8e9d7d41a7c90fef4adca9fe4)

**REPRODUCTION CASE**  

v8 build flags:is\_debug=true dcheck\_always\_on=true v8\_static\_library=true target\_cpu="x64"

run:  

./d8 ---future --allow-natives-syntax --turboshaft-assert-types --always-turbofan rrr.js

crash log:

```
#  
# Fatal error in ../../src/compiler/turboshaft/types.h, line 501  
# Debug check failed: 0 != special_values (0 vs. 0).  
#  
#  
#  
#FailureMessage Object: 0x7ffd5d9d7100  
==== C stack trace ===============================  
  
    /home/pwn/code/v8/out/fuzzbuild/d8(+0x7ab4c2) [0x556a784884c2]  
    /home/pwn/code/v8/out/fuzzbuild/d8(+0x7a9fd7) [0x556a78486fd7]  
    /home/pwn/code/v8/out/fuzzbuild/d8(+0x79c6df) [0x556a784796df]  
    /home/pwn/code/v8/out/fuzzbuild/d8(+0x79c075) [0x556a78479075]  
    /home/pwn/code/v8/out/fuzzbuild/d8(+0x32c4c2f) [0x556a7afa1c2f]  
    /home/pwn/code/v8/out/fuzzbuild/d8(+0x32c6fd2) [0x556a7afa3fd2]  
    /home/pwn/code/v8/out/fuzzbuild/d8(+0x32c8d5d) [0x556a7afa5d5d]  
    /home/pwn/code/v8/out/fuzzbuild/d8(+0x320bc95) [0x556a7aee8c95]  
    /home/pwn/code/v8/out/fuzzbuild/d8(+0x3209d55) [0x556a7aee6d55]  
    /home/pwn/code/v8/out/fuzzbuild/d8(+0x3204108) [0x556a7aee1108]  
    /home/pwn/code/v8/out/fuzzbuild/d8(+0x32039ee) [0x556a7aee09ee]  
    /home/pwn/code/v8/out/fuzzbuild/d8(+0x3203202) [0x556a7aee0202]  
    /home/pwn/code/v8/out/fuzzbuild/d8(+0x31ff89c) [0x556a7aedc89c]  
    /home/pwn/code/v8/out/fuzzbuild/d8(+0x31ff2a8) [0x556a7aedc2a8]  
    /home/pwn/code/v8/out/fuzzbuild/d8(+0x31fe880) [0x556a7aedb880]  
    /home/pwn/code/v8/out/fuzzbuild/d8(+0x29e2299) [0x556a7a6bf299]  
    /home/pwn/code/v8/out/fuzzbuild/d8(+0x29dbb9f) [0x556a7a6b8b9f]  
    /home/pwn/code/v8/out/fuzzbuild/d8(+0x29da19a) [0x556a7a6b719a]  
    /home/pwn/code/v8/out/fuzzbuild/d8(+0xa716c1) [0x556a7874e6c1]  
    /home/pwn/code/v8/out/fuzzbuild/d8(+0xa95f37) [0x556a78772f37]  
    /home/pwn/code/v8/out/fuzzbuild/d8(+0xa80fde) [0x556a7875dfde]  
    /home/pwn/code/v8/out/fuzzbuild/d8(+0xa833a3) [0x556a787603a3]  
    /home/pwn/code/v8/out/fuzzbuild/d8(+0x1ac462a) [0x556a797a162a]  
    /home/pwn/code/v8/out/fuzzbuild/d8(+0x1ac3ef8) [0x556a797a0ef8]  
    /home/pwn/code/v8/out/fuzzbuild/d8(+0x338b1f6) [0x556a7b0681f6]  
追踪与中断点陷阱 (核心已转储)  
  

```

**CREDIT INFORMATION**

Reporter credit: Zhaozhenjiang of pangulab

## Attachments

- [rrr.js](attachments/rrr.js) (text/plain, 4.9 KB)

## Timeline

### [Deleted User] (2023-06-12)

[Empty comment from Monorail migration]

### sw...@gmail.com (2023-06-12)

can still get this crash in the latest version of v8(head : 82ef4ba4ecc1bd875f8ad7d86882215a08447dad)

crash log( enable is_debug=ture):
```
#
# Fatal error in ../../src/compiler/turboshaft/types.h, line 501
# Debug check failed: 0 != special_values (0 vs. 0).
#
#
#
#FailureMessage Object: 0x7ffcc8b09840
==== C stack trace ===============================

    /home/pwn/code/v8/out/fuzzbuild2/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x13) [0x7f1b8dd6fcb3]
    /home/pwn/code/v8/out/fuzzbuild2/libv8_libplatform.so(+0x15c8d) [0x7f1b8dd1bc8d]
    /home/pwn/code/v8/out/fuzzbuild2/libv8_libbase.so(V8_Fatal(char const*, int, char const*, ...)+0x154) [0x7f1b8dd4fb34]
    /home/pwn/code/v8/out/fuzzbuild2/libv8_libbase.so(+0x275d5) [0x7f1b8dd4f5d5]
    /home/pwn/code/v8/out/fuzzbuild2/libv8.so(v8::internal::compiler::turboshaft::FloatType<64ul>::OnlySpecialValues(unsigned int)+0x6e) [0x7f1b90ead9de]
    /home/pwn/code/v8/out/fuzzbuild2/libv8.so(v8::internal::compiler::turboshaft::FloatType<64ul>::LeastUpperBound(v8::internal::compiler::turboshaft::FloatType<64ul> const&, v8::internal::compiler::turboshaft::FloatType<64ul> const&, v8::internal::Zone*)+0x289) [0x7f1b90eaf6d9]
    /home/pwn/code/v8/out/fuzzbuild2/libv8.so(v8::internal::compiler::turboshaft::Type::LeastUpperBound(v8::internal::compiler::turboshaft::Type const&, v8::internal::compiler::turboshaft::Type const&, v8::internal::Zone*)+0xa5) [0x7f1b90eb0b05]
    /home/pwn/code/v8/out/fuzzbuild2/libv8.so(+0x30b7155) [0x7f1b90e32155]
    /home/pwn/code/v8/out/fuzzbuild2/libv8.so(+0x30b5b77) [0x7f1b90e30b77]
    /home/pwn/code/v8/out/fuzzbuild2/libv8.so(+0x30b1907) [0x7f1b90e2c907]
    /home/pwn/code/v8/out/fuzzbuild2/libv8.so(+0x30b13ca) [0x7f1b90e2c3ca]
    /home/pwn/code/v8/out/fuzzbuild2/libv8.so(+0x30b0e97) [0x7f1b90e2be97]
    /home/pwn/code/v8/out/fuzzbuild2/libv8.so(+0x30aee00) [0x7f1b90e29e00]
    /home/pwn/code/v8/out/fuzzbuild2/libv8.so(+0x30ae7f6) [0x7f1b90e297f6]
    /home/pwn/code/v8/out/fuzzbuild2/libv8.so(+0x30ae07d) [0x7f1b90e2907d]
    /home/pwn/code/v8/out/fuzzbuild2/libv8.so(+0x2d8ff4c) [0x7f1b90b0af4c]
    /home/pwn/code/v8/out/fuzzbuild2/libv8.so(+0x2d8a653) [0x7f1b90b05653]
    /home/pwn/code/v8/out/fuzzbuild2/libv8.so(+0x2d89640) [0x7f1b90b04640]
    /home/pwn/code/v8/out/fuzzbuild2/libv8.so(v8::internal::OptimizedCompilationJob::ExecuteJob(v8::internal::RuntimeCallStats*, v8::internal::LocalIsolate*)+0xa7) [0x7f1b8f244407]
    /home/pwn/code/v8/out/fuzzbuild2/libv8.so(+0x14e50ab) [0x7f1b8f2600ab]
    /home/pwn/code/v8/out/fuzzbuild2/libv8.so(+0x14d52c8) [0x7f1b8f2502c8]
    /home/pwn/code/v8/out/fuzzbuild2/libv8.so(v8::internal::Compiler::CompileOptimized(v8::internal::Isolate*, v8::internal::Handle<v8::internal::JSFunction>, v8::internal::ConcurrencyMode, v8::internal::CodeKind)+0xb7) [0x7f1b8f251e17]
    /home/pwn/code/v8/out/fuzzbuild2/libv8.so(+0x204b3ca) [0x7f1b8fdc63ca]
    /home/pwn/code/v8/out/fuzzbuild2/libv8.so(+0x204ae8d) [0x7f1b8fdc5e8d]
    /home/pwn/code/v8/out/fuzzbuild2/libv8.so(+0xbca73d) [0x7f1b8e94573d]

```

### ar...@google.com (2023-06-12)

Thanks for reporting this!

I will start by uploading the test case to Clusterfuzz in case it can bisect and populate the right flags for the bug.

### cl...@chromium.org (2023-06-12)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4867641272107008.

### cl...@chromium.org (2023-06-12)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-06-12)

Detailed Report: https://clusterfuzz.com/testcase?key=4867641272107008

Fuzzer: None
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  0 != special_values in types.h
  v8::internal::compiler::turboshaft::FloatType<64ul>::OnlySpecialValues
  v8::internal::compiler::turboshaft::FloatType<64ul>::LeastUpperBound
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=87820:87821

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=4867641272107008

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### ar...@google.com (2023-06-12)

Thanks Clusterfuzz!

+ nicohartmann@ as owner.
+ ishell@google.com as current V8 security sheriff. Are the Security_{Severity, Impact} choosen by ClusterFuzz / me correct?

[Monorail components: Blink>JavaScript>Compiler]

### [Deleted User] (2023-06-12)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ni...@chromium.org (2023-06-13)

Taking a look. This requires --turboshaft, though, which is still behind --future, so not an immediate (security) risk.

### gi...@appspot.gserviceaccount.com (2023-06-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/06edd6bb4712ccd707738232e608a05543c55cf9

commit 06edd6bb4712ccd707738232e608a05543c55cf9
Author: Nico Hartmann <nicohartmann@chromium.org>
Date: Tue Jun 13 07:52:10 2023

[turboshaft] Handle kOnlySpecialValues => None transition in Intersect

Bug: v8:12783, chromium:1453973
Change-Id: Ib906ca45e4effb886a20fb757eb21af9d853b9f6
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4608070
Reviewed-by: Darius Mercadier <dmercadier@chromium.org>
Auto-Submit: Nico Hartmann <nicohartmann@chromium.org>
Commit-Queue: Nico Hartmann <nicohartmann@chromium.org>
Cr-Commit-Position: refs/heads/main@{#88186}

[modify] https://crrev.com/06edd6bb4712ccd707738232e608a05543c55cf9/src/compiler/turboshaft/types.cc
[modify] https://crrev.com/06edd6bb4712ccd707738232e608a05543c55cf9/src/compiler/turboshaft/typer.cc
[modify] https://crrev.com/06edd6bb4712ccd707738232e608a05543c55cf9/src/compiler/turboshaft/types.h
[add] https://crrev.com/06edd6bb4712ccd707738232e608a05543c55cf9/test/mjsunit/regress/regress-1453973.js


### ni...@chromium.org (2023-06-13)

[Empty comment from Monorail migration]

### be...@google.com (2023-06-13)

Adding Hotlist-RBS-Removed for tracking purposes.

### cl...@chromium.org (2023-06-13)

ClusterFuzz testcase 4867641272107008 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=88185:88186

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### [Deleted User] (2023-06-13)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-13)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-06-27)

Based on https://crbug.com/chromium/1453973#c9, this issue was reduced to low severity based on this issue being specific in turboshaft and it's status as future and not yet shipping. 
Issues in non-shipped features should carry the severity of the issue and that status of non-default / non-shipped feature should be reflected only in the SI-None label, which allows for a reduced pri- by the bot. 

If there reason to reduce severity, such as this issue would not result in renderer RCE because of some mitigation or not being a potentially exploitable security issue, please feel free to let me know so I can readjust accordingly. 

### sw...@gmail.com (2023-07-05)

Is there any update on the VRP information for this issue, please?

### am...@chromium.org (2023-07-05)

Hello, thanks for reaching out. This will be discussed at a future VRP panel. There are no VRP panel sessions this week due to the holiday in the US. 

### am...@google.com (2023-07-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-07-13)

Congratulations! The VRP Panel has decided to award you $7,000 for this report. A member of our finance team will be in touch with you soon to arrange payment. Thank you for your efforts and reporting this issue to us! 

### sw...@gmail.com (2023-07-14)

Thank you so much

### am...@google.com (2023-07-14)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-19)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-11-11)

Hello! We consider attachments/POCs and all analysis included with reports to be an integral part of the report (https://g.co/chrome/vrp/#investigating-and-reporting-bugs), even when included in comments, so I have undeleted them. Thank you!

### is...@google.com (2023-11-11)

This issue was migrated from crbug.com/chromium/1453973?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40065644)*
