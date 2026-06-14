# Security: SwiftShader sw::Renderer::taskLoop

| Field | Value |
|-------|-------|
| **Issue ID** | [40089435](https://issues.chromium.org/issues/40089435) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Internals>GPU>SwiftShader |
| **Platforms** | Windows |
| **Reporter** | [Deleted User] |
| **Assignee** | su...@chromium.org |
| **Created** | 2017-10-28 |
| **Bounty** | $1,000.00 |

## Description

I have tested this vulnerability on Windows 10 and Windows ASAN build asan-coverage-win32-release-506366 and asan-win32-release-512393

2ff217c7 f30f7e0c10      movq    xmm1,mmword ptr [eax+edx] ds:002b:23d73000=????????????????
5:118:x86> k
 # ChildEBP RetAddr  
WARNING: Frame IP not in any known module. Following frames may be wrong.
00 2d26fb08 0e400210 0x2ff217c7
*** WARNING: Unable to verify checksum for C:\Users\omair\Desktop\asan-win32-release-509608\swiftshader\libglesv2.dll
01 2d26fb50 525a7161 0xe400210
02 2d26fb70 525a702c libglesv2!sw::Renderer::taskLoop+0x4f [C:\b\c\b\win_asan_release\src\third_party\swiftshader\src\Renderer\Renderer.cpp @ 726] 
03 2d26fba4 525a6f7e libglesv2!sw::Renderer::threadLoop+0x7e [C:\b\c\b\win_asan_release\src\third_party\swiftshader\src\Renderer\Renderer.cpp @ 716] 
04 2d26fbbc 52a5bc0f libglesv2!sw::Renderer::threadFunction+0x54 [C:\b\c\b\win_asan_release\src\third_party\swiftshader\src\Renderer\Renderer.cpp @ 708] 
*** WARNING: Unable to verify checksum for chrome.exe
05 2d26fbd4 0157ea72 libglesv2!sw::Thread::startFunction+0x5d [C:\b\c\b\win_asan_release\src\third_party\swiftshader\src\Common\Thread.cpp @ 58] 
06 2d26fbe8 0157da5e chrome!__asan::AsanThread::ThreadStart+0x92 [e:\b\build\slave\win_upload_clang\build\src\third_party\llvm\projects\compiler-rt\lib\asan\asan_thread.cc @ 267] 
07 2d26fbf8 759f8744 chrome!asan_thread_start+0x1e [e:\b\build\slave\win_upload_clang\build\src\third_party\llvm\projects\compiler-rt\lib\asan\asan_win.cc @ 137] 
08 2d26fc0c 772e582d KERNEL32!BaseThreadInitThunk+0x24
09 2d26fc54 772e57fd ntdll_77280000!__RtlUserThreadStart+0x2f
0a 2d26fc64 00000000 ntdll_77280000!_RtlUserThreadStart+0x1b


The asan builds seem to be having some problem currently on Windows and can't get the symbolized stack trace
==13916==ERROR: AddressSanitizer: access-violation on unknown address 0x233d3000 (pc 0x2f5e17c7 bp 0x2c4df764 sp 0x2c4df370 T37)
    #0 0x2f5e17c6  (<unknown module>)
    #1 0xd70720f  (<unknown module>)
    #2 0x5275a002  (c:\Users\omair\Desktop\asan-win32-release-512393\swiftshader\libglesv2.dll+0x1041a002)
    #3 0x52759ecd  (c:\Users\omair\Desktop\asan-win32-release-512393\swiftshader\libglesv2.dll+0x10419ecd)
    #4 0x52759e1f  (c:\Users\omair\Desktop\asan-win32-release-512393\swiftshader\libglesv2.dll+0x10419e1f)


## Attachments

- [Chrome_swshader.html](attachments/Chrome_swshader.html) (text/plain, 3.1 KB)

## Timeline

### el...@chromium.org (2017-10-29)

[Empty comment from Monorail migration]

[Monorail components: Internals>GPU>SwiftShader]

### cl...@chromium.org (2017-10-30)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5370139066499072.

### cl...@chromium.org (2017-10-31)

[Empty comment from Monorail migration]

### pa...@chromium.org (2017-10-31)

jbauman, do you still work on GPU stuff, and SwiftShader in particular? If not, can you please recommend a better person to take this bug? Thanks!

Also, this might affect more platforms besides Windows? Including Fuchsia?

### kb...@chromium.org (2017-10-31)

[Empty comment from Monorail migration]

### cl...@chromium.org (2017-10-31)

Detailed report: https://clusterfuzz.com/testcase?key=5370139066499072

Job Type: windows_asan_chrome
Crash Type: UNKNOWN READ
Crash Address: 0x0dab2000
Crash State:
  Register
  Register
  Register
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=windows_asan_chrome&range=512219:512265

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5370139066499072

See https://github.com/google/clusterfuzz-tools for more information.

A recommended severity was added to this bug. Please change the severity if it is inaccurate.


### sh...@chromium.org (2017-10-31)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-10-31)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2017-10-31)

[Empty comment from Monorail migration]

### ca...@chromium.org (2017-11-02)

Alexis has started looking into this.

### bu...@chromium.org (2017-11-02)

The following revision refers to this bug:
  https://swiftshader.googlesource.com/SwiftShader.git/+/7a8ed2e14ad40356a624826df166c41fec7e2525

commit 7a8ed2e14ad40356a624826df166c41fec7e2525
Author: Alexis Hetu <sugoi@google.com>
Date: Thu Nov 02 15:32:24 2017

Prevent initializing outline edges to out of bound values

When multisampling is enabled, outline edges were getting
initialized to one of the  primitive's X position. If the
primitive was out of bounds, then the default position was
out of bounds, which led to an initial out of bounds memory
access.

Added a clamp to fix the issue.

https://crbug.com/chromium/779364

Change-Id: I4661f4229ee28a3032c763ed18dde799d3c3926b
Reviewed-on: https://swiftshader-review.googlesource.com/13528
Tested-by: Alexis Hétu <sugoi@google.com>
Reviewed-by: Nicolas Capens <nicolascapens@google.com>

[modify] https://crrev.com/7a8ed2e14ad40356a624826df166c41fec7e2525/src/Shader/SetupRoutine.cpp


### mm...@chromium.org (2017-11-16)

omair@, out of curiosity, what techniques have you used to find that issue?

### mm...@chromium.org (2017-11-16)

Hm, it seems to be a duplicate of https://crbug.com/chromium/779325.

### [Deleted User] (2017-11-16)

https://crbug.com/chromium/779364#c12:
Fuzzing (you can stop reading here) with ML and AI (Cyber). On my own built up, cloud based, state of the art, fuzzing infrastructure aka two instances of Chrome.


### mm...@chromium.org (2017-11-16)

Thanks for your answer, I wish we could give rewards for awesome bugs comments.

Regarding duplication, I'll defer to the bug owner to decide that. Either way, looking forward to seeing more reports from you :)

### cl...@chromium.org (2017-11-17)

Detailed report: https://clusterfuzz.com/testcase?key=5370139066499072

Job Type: windows_asan_chrome
Crash Type: UNKNOWN READ
Crash Address: 0x0dab2000
Crash State:
  Register
  Register
  Register
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=windows_asan_chrome&range=512219:512265

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5370139066499072

See https://github.com/google/clusterfuzz-tools for more information.

### cl...@chromium.org (2017-12-02)

ClusterFuzz has detected this issue as fixed in range 521083:521102.

Detailed report: https://clusterfuzz.com/testcase?key=5370139066499072

Job Type: windows_asan_chrome
Crash Type: UNKNOWN READ
Crash Address: 0x0dab2000
Crash State:
  Register
  Register
  Register
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=windows_asan_chrome&range=512219:512265
Fixed: https://clusterfuzz.com/revisions?job=windows_asan_chrome&range=521083:521102

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5370139066499072

See https://github.com/google/clusterfuzz-tools for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2017-12-02)

ClusterFuzz testcase 5370139066499072 is verified as fixed, so closing issue as verified.

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### sh...@chromium.org (2017-12-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-12-08)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2017-12-08)

omair@ - Groovy! The VRP Panel decided to award $1,000 for this report. Thanks!

### aw...@chromium.org (2017-12-08)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-03-10)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-03-27)

[Empty comment from Monorail migration]

### aw...@google.com (2018-03-31)

[Empty comment from Monorail migration]

### is...@google.com (2018-03-31)

This issue was migrated from crbug.com/chromium/779364?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40089435)*
