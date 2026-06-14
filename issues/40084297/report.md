# Heap-use-after-free in CFX_StringDataTemplate<wchar_t>::Retain() 

| Field | Value |
|-------|-------|
| **Issue ID** | [40084297](https://issues.chromium.org/issues/40084297) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Reporter** | at...@gmail.com |
| **Assignee** | oc...@chromium.org |
| **Created** | 2016-05-12 |
| **Bounty** | $3,500.00 |

## Description



Tested on:

OS: Ubuntu 14.04

pdfium_test: linux-release-asan-symbolized-linux-release-393191

Note1: I found this issue when minimizing repro-file from https://cluster-fuzz.appspot.com/testcase?key=5080174055391232 I couldn't reproduce the wild-pointer-read from the CF report with an ASAN build. 

Note2: This issue shows up as an UAF only with pdfium_test, on chromium it shows up as a crash with a similar stack but as a null-pointer instead of an UAF.

Note3: Second repro-file is for a heap-buffer-overflow READ size 4, in pdfium_test. My minimizer caught it while minimizing the repro-file. Stack is so similar that I'm guessing it is the same root cause. In Chromium the repro-file causes null-pointer crash.

ASAN-trace:

Rendering PDF file /results/heap-use-after-free-8d2-641-d6d.pdf.
=================================================================
==4189==ERROR: AddressSanitizer: heap-use-after-free on address 0x62500017e968 at pc 0x0000009328d3 bp 0x7ffe1a67de10 sp 0x7ffe1a67de08
READ of size 8 at 0x62500017e968 thread T0
    #0 0x9328d2 in CFX_StringDataTemplate<wchar_t>::Retain() /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/fxcrt/cfx_string_data_template.h:53
    #1 0xaf2641 in (anonymous namespace)::StrTrim(CFX_WideString const&) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/fpdfsdk/javascript/PublicMethods.cpp:73
    #2 0xaf7d6d in AFNumber_Keystroke /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/fpdfsdk/javascript/PublicMethods.cpp:906 (discriminator 1)
    #3 0xb00472 in JSGlobalFunc<&CJS_PublicMethods::AFNumber_Keystroke> /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/fpdfsdk/javascript/JS_Define.h:454
    #4 0x17cbb5c in Call /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../v8/src/api-arguments.cc:15
    #5 0xbc06ac in HandleApiCallHelper /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../v8/src/builtins.cc:4620 (discriminator 1)
    #6 0xc30646 in Builtin_Impl_HandleApiCall /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../v8/src/builtins.cc:4638 (discriminator 5)
    #7 0xbcce34 in v8::internal::Builtin_HandleApiCall(int, v8::internal::Object**, v8::internal::Isolate*) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../v8/src/builtins.cc:4635 (discriminator 6)
.
.
.
0x62500017e968 is located 104 bytes inside of 8192-byte region [0x62500017e900,0x625000180900)
freed by thread T0 here:
    #0 0x4b651b in __interceptor_free ??:?
    #1 0x1dc2864 in v8::base::AccountingAllocator::Free(void*, unsigned long) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../v8/src/base/accounting-allocator.cc:23
    #2 0x1632421 in v8::internal::Zone::DeleteKeptSegment() /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../v8/src/zone.cc:195
    #3 0xec7877 in void v8::internal::HGraph::Run<v8::internal::HRepresentationChangesPhase>() /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../v8/src/crankshaft/hydrogen.h:477
    #4 0xea65b3 in v8::internal::HGraph::Optimize(v8::internal::BailoutReason*) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../v8/src/crankshaft/hydrogen.cc:4686
    #5 0xc9a06c in v8::internal::OptimizeGraph(v8::internal::HGraph*) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../v8/src/code-stubs-hydrogen.cc:24
    #6 0xc820ea in v8::internal::Handle<v8::internal::Code> v8::internal::DoGenerateCode<v8::internal::LoadFieldStub>(v8::internal::LoadFieldStub*) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../v8/src/code-stubs-hydrogen.cc:290 (discriminator 2)
.
.
.

ASAN-trace:(chromium)

==4681==ERROR: AddressSanitizer: SEGV on unknown address 0x000000000000 (pc 0x55a5d35e0d2a bp 0x7ffd8f439410 sp 0x7ffd8f439400 T0)
==4681==The signal is caused by a READ memory access.
==4681==Hint: address points to the zero page.
    #0 0x55a5d35e0d29 in CFX_StringDataTemplate<wchar_t>::Retain() /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/fxcrt/cfx_string_data_template.h:53
    #1 0x55a5d379f4c1 in (anonymous namespace)::StrTrim(CFX_WideString const&) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/fpdfsdk/javascript/PublicMethods.cpp:73
    #2 0x55a5d37a4bed in AFNumber_Keystroke /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/fpdfsdk/javascript/PublicMethods.cpp:906 (discriminator 1)
    #3 0x55a5d37ad2f2 in JSGlobalFunc<&CJS_PublicMethods::AFNumber_Keystroke> /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/fpdfsdk/javascript/JS_Define.h:454
    #4 0x55a5ca5ffbac in Call /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../v8/src/api-arguments.cc:15
    #5 0x55a5c99ba56c in HandleApiCallHelper /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../v8/src/builtins.cc:4620 (discriminator 1)
    #6 0x55a5c9a2a506 in Builtin_Impl_HandleApiCall /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../v8/src/builtins.cc:4638 (discriminator 5)
    #7 0x55a5c99c6cf4 in v8::internal::Builtin_HandleApiCall(int, v8::internal::Object**, v8::internal::Isolate*) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../v8/src/builtins.cc:4635 (discriminator 6)
.
.
.

## Attachments

- [heap-use-after-free-8d2-641-d6d.pdf](attachments/heap-use-after-free-8d2-641-d6d.pdf) (application/pdf, 300 B)
- [heap-buffer-overflow-b19-c75-64e.pdf](attachments/heap-buffer-overflow-b19-c75-64e.pdf) (application/pdf, 1.6 KB)

## Timeline

### cl...@chromium.org (2016-05-12)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5068754760761344

### cl...@chromium.org (2016-05-12)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5704946439159808

### cl...@chromium.org (2016-05-12)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5698145224228864

Fuzzer: attekett_surku_fuzzer
Job Type: linux_asan_chrome_chromeos
Platform Id: linux

Crash Type: UNKNOWN READ
Crash Address: 0x7f1c2be2a3ac
Crash State:
  CFX_WideString::TrimRight
  CFX_WideString::TrimRight
  CJS_PublicMethods::AFNumber_Keystroke
  
Recommended Security Severity: Medium


Unminimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv94MLdPwbVK_TeRxzBPoBG-VUYH_eYAmLqrzbkQOuxgPSrz3qisEoJ9Mxij6_ItMrwa0HzVWm_NTS4MgWeoisbrp0XbuUCQ8Ve9huqQ8YNcnmSVubj3-1tatzPMID1dvl8IyXZkVcUCx-p41da6UuUHEKI2slYxDYD7Q7avXnOkRnpGEWKE


Filer: mbarbella

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

### cl...@chromium.org (2016-05-12)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=6289379416342528

### mb...@chromium.org (2016-05-12)

Oliver, would you mind taking a look or helping to find an owner for this?

### mb...@chromium.org (2016-05-12)

[Empty comment from Monorail migration]

[Monorail components: Internals>Plugins>PDF]

### cl...@chromium.org (2016-05-12)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6289379416342528

Uploader: mbarbella@google.com
Job Type: linux_asan_pdfium
Platform Id: linux

Crash Type: UNKNOWN READ
Crash Address: 0x36e3000036e7
Crash State:
  CFX_WideString::TrimLeft
  CFX_WideString::TrimLeft
  CJS_PublicMethods::AFNumber_Keystroke
  
Recommended Security Severity: Medium

Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_pdfium&range=393062:393120

Minimized Testcase (0.29 Kb): https://cluster-fuzz.appspot.com/download/AMIfv9715F9fLIedE7yzlQtLly_jQtpHd5NiT_7-CfFo5ZnNWocU3rqFxE6WIc5dG1g7ERspWfdcEMH9c0FDR4J05bsG5HyUFrbGqNDDVanLQZyG94_X5XzeN8KziwOD07OcYudjqtP2edZ3RUhZP3Bq-XPkGFSuYw

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

The recommended severity is different from what was assigned to the bug. Please double check the accuracy of the assigned severity.


### oc...@chromium.org (2016-05-12)

CL: https://codereview.chromium.org/1977613002/

### bu...@chromium.org (2016-05-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/7257530cdb9298f9c03326b67786113f86ac380c

commit 7257530cdb9298f9c03326b67786113f86ac380c
Author: ochang <ochang@chromium.org>
Date: Fri May 13 00:43:31 2016

Roll PDFium 77f45f2..f6d9a61

https://pdfium.googlesource.com/pdfium.git/+log/77f45f2..f6d9a61

BUG=611352
TBR=thestig@chromium.org

TEST=bots

Review-Url: https://codereview.chromium.org/1977653002
Cr-Commit-Position: refs/heads/master@{#393412}

[modify] https://crrev.com/7257530cdb9298f9c03326b67786113f86ac380c/DEPS


### sh...@chromium.org (2016-05-13)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-05-13)

This issue is a security regression. If you are not able to fix this quickly, please revert the change that introduced it.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-05-13)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-05-13)

ClusterFuzz has detected this issue as fixed in range 393384:393413.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5698145224228864

Fuzzer: attekett_surku_fuzzer
Job Type: linux_asan_chrome_chromeos
Platform Id: linux

Crash Type: UNKNOWN READ
Crash Address: 0x7f1c2be2a3ac
Crash State:
  CFX_WideString::TrimRight
  CFX_WideString::TrimRight
  CJS_PublicMethods::AFNumber_Keystroke
  
Recommended Security Severity: Medium

Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_chromeos&range=364779:365132
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_chromeos&range=393384:393413

Unminimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv94MLdPwbVK_TeRxzBPoBG-VUYH_eYAmLqrzbkQOuxgPSrz3qisEoJ9Mxij6_ItMrwa0HzVWm_NTS4MgWeoisbrp0XbuUCQ8Ve9huqQ8YNcnmSVubj3-1tatzPMID1dvl8IyXZkVcUCx-p41da6UuUHEKI2slYxDYD7Q7avXnOkRnpGEWKE


See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2016-05-13)

ClusterFuzz has detected this issue as fixed in range 393401:393413.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5068754760761344

Uploader: mbarbella@google.com
Job Type: linux_asan_pdfium
Platform Id: linux

Crash Type: UNKNOWN READ
Crash Address: 0x00000943134c
Crash State:
  CFX_WideString::TrimRight
  CFX_WideString::TrimRight
  CJS_PublicMethods::AFNumber_Keystroke
  
Recommended Security Severity: Medium

Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_pdfium&range=393150:393183
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_pdfium&range=393401:393413

Minimized Testcase (1.59 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94zSLZsbQ0MtpTx9QqRVlEyDTWLEh1jnMGluGRsKrPKGl-6fnCMm5RKJ_LUie3ZuAOLC4H9tQ72gWF2Dt1p4Jr0rGQmtEcwoFx100CYZnlvgyEaqrmzhbUil7xl58S2IoCDIu3v1YrnsYqdV66hpQFRz-_kDQ

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2016-05-13)

ClusterFuzz has detected this issue as fixed in range 393401:393413.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5704946439159808

Uploader: mbarbella@google.com
Job Type: linux_msan_pdfium
Platform Id: linux

Crash Type: Use-of-uninitialized-value
Crash Address: 
Crash State:
  CJS_PublicMethods::AFNumber_Keystroke
  void JSGlobalFunc<&CJS_PublicMethods::AFNumber_Keystroke>
  v8::internal::FunctionCallbackArguments::Call
  
Recommended Security Severity: Medium

Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_msan_pdfium&range=393095:393120
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_msan_pdfium&range=393401:393413

Minimized Testcase (0.29 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95L_-DZVxWO36qS4aHYHeOzCWdur1ZC9UTqfPW-jbeApIT1xZl_TeGGO1pR2OKMzGqd_JBilCZLwvkY3fmG5Rtq4tIorCdab9_V2k9IiYIoS-nneSbirs_Jc9IAUWErUb2hnccW4D35FMt9A0XjE1X5IDjLEg

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### oc...@chromium.org (2016-05-13)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-05-13)

ClusterFuzz has detected this issue as fixed in range 393401:393413.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6289379416342528

Uploader: mbarbella@google.com
Job Type: linux_asan_pdfium
Platform Id: linux

Crash Type: UNKNOWN READ
Crash Address: 0x36e3000036e7
Crash State:
  CFX_WideString::TrimLeft
  CFX_WideString::TrimLeft
  CJS_PublicMethods::AFNumber_Keystroke
  
Recommended Security Severity: Medium

Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_pdfium&range=393062:393120
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_pdfium&range=393401:393413

Minimized Testcase (0.29 Kb): https://cluster-fuzz.appspot.com/download/AMIfv9715F9fLIedE7yzlQtLly_jQtpHd5NiT_7-CfFo5ZnNWocU3rqFxE6WIc5dG1g7ERspWfdcEMH9c0FDR4J05bsG5HyUFrbGqNDDVanLQZyG94_X5XzeN8KziwOD07OcYudjqtP2edZ3RUhZP3Bq-XPkGFSuYw

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### oc...@chromium.org (2016-05-13)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-05-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-05-14)

[Empty comment from Monorail migration]

### ti...@google.com (2016-06-24)

$3,500 for this report - Thanks again Atte!

### aw...@chromium.org (2016-07-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-08-20)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/611352?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084297)*
