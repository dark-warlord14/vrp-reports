# Stack buffer overflow in angle shader translation

| Field | Value |
|-------|-------|
| **Issue ID** | [329271490](https://issues.chromium.org/issues/329271490) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Blink>WebGL, Internals>GPU, Internals>GPU>ANGLE |
| **Platforms** | Linux |
| **Reporter** | wg...@gmail.com |
| **Assignee** | ge...@chromium.org |
| **Created** | 2024-03-13 |
| **Bounty** | $2,000.00 |

## Description

VULNERABILITY DETAILS
The angle shader translator contains a stack buffer overflow that can be triggered via a malicious shader. The code path is reachable from chromium; in an ASAN build the GPU process crashes with an ASAN violation.

VERSION
Chrome Version: 124.0.6354.0 (Developer Build) (64-bit) 
Operating System: Ubuntu 23.10

REPRODUCTION CASE
I attached a .html file which should crash the GPU process with an ASAN violation. I also attached a shader that crashes a standalone build of the angle shader translator when invoked as `./angle_shader_translator -b=v -s=w2 -i a.vert`

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: GPU
Crash State:
==3670261==ERROR: AddressSanitizer: stack-buffer-overflow on address 0x7f3063513f31 at pc 0x7f305e29cf1e bp 0x7ffe9e8b9450 sp 0x7ffe9e8b9448
READ of size 1 at 0x7f3063513f31 thread T0 (chrome)
==3670261==WARNING: invalid path to external symbolizer!
==3670261==WARNING: Failed to use and restart external symbolizer!
    #0 0x7f305e29cf1d  (libGLESv2.so+0x129cf1d) (BuildId: d86f3b24bdc890ff)
    #1 0x7f305e29a9a9  (libGLESv2.so+0x129a9a9) (BuildId: d86f3b24bdc890ff)
    #2 0x7f305e2b38f9  (libGLESv2.so+0x12b38f9) (BuildId: d86f3b24bdc890ff)
    #3 0x7f305e2b075f  (libGLESv2.so+0x12b075f) (BuildId: d86f3b24bdc890ff)
    #4 0x7f305e2ad2c6  (libGLESv2.so+0x12ad2c6) (BuildId: d86f3b24bdc890ff)
    #5 0x7f305e2b292f  (libGLESv2.so+0x12b292f) (BuildId: d86f3b24bdc890ff)
    #6 0x7f305deccab8  (libGLESv2.so+0xeccab8) (BuildId: d86f3b24bdc890ff)
    #7 0x7f305ddbdfcb  (libGLESv2.so+0xdbdfcb) (BuildId: d86f3b24bdc890ff)
    #8 0x7f305dc7a335  (libGLESv2.so+0xc7a335) (BuildId: d86f3b24bdc890ff)
    #9 0x7f305de3293a  (libGLESv2.so+0xe3293a) (BuildId: d86f3b24bdc890ff)
    #10 0x55eb34512d0e  (chrome+0x27e43d0e) (BuildId: 8cb7073af1016a67)
    #11 0x55eb344c1ffd  (chrome+0x27df2ffd) (BuildId: 8cb7073af1016a67)
    #12 0x55eb349e03bb  (chrome+0x283113bb) (BuildId: 8cb7073af1016a67)
    #13 0x55eb349cf933  (chrome+0x28300933) (BuildId: 8cb7073af1016a67)
    #14 0x55eb349cee09  (chrome+0x282ffe09) (BuildId: 8cb7073af1016a67)
    #15 0x55eb349eb6d1  (chrome+0x2831c6d1) (BuildId: 8cb7073af1016a67)
    #16 0x55eb349fae26  (chrome+0x2832be26) (BuildId: 8cb7073af1016a67)
    #17 0x55eb349fac0c  (chrome+0x2832bc0c) (BuildId: 8cb7073af1016a67)
    #18 0x55eb317dfa6d  (chrome+0x25110a6d) (BuildId: 8cb7073af1016a67)
    #19 0x55eb317dd982  (chrome+0x2510e982) (BuildId: 8cb7073af1016a67)
    #20 0x55eb317e1573  (chrome+0x25112573) (BuildId: 8cb7073af1016a67)
    #21 0x55eb2c824864  (chrome+0x20155864) (BuildId: 8cb7073af1016a67)
    #22 0x55eb2c88614f  (chrome+0x201b714f) (BuildId: 8cb7073af1016a67)
    #23 0x55eb2c885139  (chrome+0x201b6139) (BuildId: 8cb7073af1016a67)
    #24 0x55eb2c886f0a  (chrome+0x201b7f0a) (BuildId: 8cb7073af1016a67)
    #25 0x55eb2c9ef502  (chrome+0x20320502) (BuildId: 8cb7073af1016a67)
    #26 0x55eb2c9f23c8  (chrome+0x203233c8) (BuildId: 8cb7073af1016a67)
    #27 0x7f3067362b2b  (/lib/x86_64-linux-gnu/libglib-2.0.so.0+0x5ab2b) (BuildId: 200be351efe83301ebaffb390ac30b652a88bac1)

Address 0x7f3063513f31 is located in stack of thread T0 (chrome) at offset 305 in frame
    #0 0x7f305e29a7bf  (libGLESv2.so+0x129a7bf) (BuildId: d86f3b24bdc890ff)
  This frame has 1 object(s): 
    [32, 240) 'creator' (line 300) <== Memory access at offset 305 overflows this variable
HINT: this may be a false positive if your program uses some custom stack unwind mechanism, swapcontext or vfork
      (longjmp and C++ exceptions *are* supported)
SUMMARY: AddressSanitizer: stack-buffer-overflow (libGLESv2.so+0x129cf1d) (BuildId: d86f3b24bdc890ff)
Shadow bytes around the buggy address: 
  0x7f3063513c80: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5
  0x7f3063513d00: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5
  0x7f3063513d80: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5
  0x7f3063513e00: f1 f1 f1 f1 00 00 00 00 00 00 00 00 00 00 00 00
  0x7f3063513e80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 f3 f3
=>0x7f3063513f00: f3 f3 f3 f3 f3 f3[f3]f3 00 00 00 00 00 00 00 00
  0x7f3063513f80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7f3063514000: f1 f1 f1 f1 00 00 00 00 00 00 00 00 00 00 00 00
  0x7f3063514080: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7f3063514100: 00 00 00 00 00 00 00 f2 f2 f2 f2 f2 f2 f2 f2 f2
  0x7f3063514180: f8 f8 f8 f3 f3 f3 f3 f3 00 00 00 00 00 00 00 00
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb

==3670261==ADDITIONAL INFO

==3670261==Note: Please include this section with the ASan report.
Task trace:
    #0 0x55eb317d7057  (chrome+0x25108057) (BuildId: 8cb7073af1016a67)


==3670261==END OF ADDITIONAL INFO
==3670261==ABORTING

CREDIT INFORMATION
Reporter credit: wgslfuzz

## Attachments

- [angle.html](attachments/angle.html) (text/html, 2.9 KB)
- [a.vert](attachments/a.vert) (application/octet-stream, 226 B)

## Timeline

### cl...@appspot.gserviceaccount.com (2024-03-13)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5113375771525120.

### ja...@chromium.org (2024-03-13)

I was able to reproduce this using the Chrome version specified in the bug report using Linux. I'll set the OS to cover at least Linux for now.

I'm adding geofflang who has looked at some similar issues in the past. geofflang@, can you take a look at this issue?

### ja...@chromium.org (2024-03-13)

I was only able to reproduce this on M124, so setting that as the found in.

### ja...@chromium.org (2024-03-14)

Moving geofflang to owner. Adding some others to CC to help find the right owner.

### ja...@chromium.org (2024-03-14)

Updating the severity to Medium (S2) to match Clusterfuzz's findings.

### pe...@google.com (2024-03-15)

Setting milestone because of s2 severity.

### pe...@google.com (2024-03-15)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security Impact hotlist or the Severity field, and remove the ReleaseBlock hotlist.

### pe...@google.com (2024-03-15)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ap...@google.com (2024-03-25)

Project: angle/angle
Branch: main

commit e996d187a93d9ca2efafdf0c2dfd8e4c518a0b24
Author: Geoff Lang <geofflang@chromium.org>
Date:   Tue Mar 19 13:29:24 2024

    Use TIntermRebuild for SeparateStructFromFunctionDeclarations
    
    This now handles the case of nested function calls to functions that
    define a struct in the return type all resolving to the correct
    re-written function.
    
    Bug: chromium:329271490
    Change-Id: I43904e09ec9c284c1b51c09b2caaab253f7b29b9
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/5376613
    Commit-Queue: Geoff Lang <geofflang@chromium.org>
    Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>

M       src/compiler/translator/Compiler.cpp
M       src/compiler/translator/tree_ops/SeparateStructFromFunctionDeclarations.cpp
M       src/compiler/translator/tree_ops/SeparateStructFromFunctionDeclarations.h
M       src/tests/gl_tests/GLSLTest.cpp

https://chromium-review.googlesource.com/5376613


### ap...@google.com (2024-03-25)

Project: chromium/src
Branch: main

commit 9bf3b052573c5d92d9d3b978698c0062947332a3
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date:   Mon Mar 25 22:54:06 2024

    Roll ANGLE from 2d4a027dc77a to c7985668bcdd (2 revisions)
    
    https://chromium.googlesource.com/angle/angle.git/+log/2d4a027dc77a..c7985668bcdd
    
    2024-03-25 syoussefi@chromium.org Add a few use-after-resolve framebuffer tests
    2024-03-25 geofflang@chromium.org Use TIntermRebuild for SeparateStructFromFunctionDeclarations
    
    If this roll has caused a breakage, revert this CL and stop the roller
    using the controls here:
    https://autoroll.skia.org/r/angle-chromium-autoroll
    Please CC angle-team@google.com,solti@google.com on the revert to ensure that a human
    is aware of the problem.
    
    To file a bug in ANGLE: https://bugs.chromium.org/p/angleproject/issues/entry
    To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry
    
    To report a problem with the AutoRoller itself, please file a bug:
    https://issues.skia.org/issues/new?component=1389291&template=1850622
    
    Documentation for the AutoRoller is here:
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md
    
    Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86
    Bug: chromium:329271490
    Tbr: solti@google.com
    Change-Id: I480fb106871bc1bdd23c5c42f15dc22535bf51f4
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5393888
    Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
    Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
    Cr-Commit-Position: refs/heads/main@{#1278006}

M       DEPS
M       third_party/angle

https://chromium-review.googlesource.com/5393888


### 24...@project.gserviceaccount.com (2024-03-26)

ClusterFuzz testcase 5113375771525120 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1277998:1278006

If this is incorrect, please add the hotlistid:5432646 and re-open the issue.

### ge...@chromium.org (2024-03-27)

This originally regressed in <https://chromium-review.googlesource.com/c/angle/angle/+/5191644> which was part of Chrome 124.0.6317.0. My fix landed in 125.0.6381.0. Requesting merge.

### pe...@google.com (2024-03-27)

Merge review required: a commit with DEPS changes was detected.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: eakpobaro (Android), eakpobaro (iOS), obenedict (ChromeOS), danielyip (Desktop)

### ge...@chromium.org (2024-03-27)

1. Yes
2. <https://chromium-review.googlesource.com/c/angle/angle/+/5376613>
3. Yes, 1 day. I will wait until ~1 week before merging.
4. No
5. N/A
6. N/A

### da...@google.com (2024-04-02)

Merge approved for M124 branch, please refer to <http://go/chrome-branches> for branch information.

### da...@google.com (2024-04-02)

Please land merge ASAP as we are looking to take Beta RC today for release tomorrow. Thanks.

### pe...@google.com (2024-04-08)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ap...@google.com (2024-04-08)

Project: angle/angle
Branch: chromium/6367

commit c884489868f982df423d572b6367bdd80110ab8a
Author: Geoff Lang <geofflang@chromium.org>
Date:   Tue Mar 19 13:29:24 2024

    M124: Use TIntermRebuild for SeparateStructFromFunctionDeclarations
    
    This now handles the case of nested function calls to functions that
    define a struct in the return type all resolving to the correct
    re-written function.
    
    Bug: chromium:329271490
    Change-Id: I43904e09ec9c284c1b51c09b2caaab253f7b29b9
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/5376613
    Commit-Queue: Geoff Lang <geofflang@chromium.org>
    Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>
    (cherry picked from commit e996d187a93d9ca2efafdf0c2dfd8e4c518a0b24)
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/5436353
    Reviewed-by: Yuly Novikov <ynovikov@chromium.org>

M       src/compiler/translator/Compiler.cpp
M       src/compiler/translator/tree_ops/SeparateStructFromFunctionDeclarations.cpp
M       src/compiler/translator/tree_ops/SeparateStructFromFunctionDeclarations.h
M       src/tests/gl_tests/GLSLTest.cpp

https://chromium-review.googlesource.com/5436353


### am...@google.com (2024-04-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2024-04-11)

Congratulations wgslfuzz! The Chrome VRP Panel has decided to award you $2,000 for this information disclosure / data leak. If you can demonstrate exploitable memory corruption that results in implications more than 1-byte read, we would be happy to reassess for a potentially higher reward. Thank you for your efforts and reporting this issue to us!

### pe...@google.com (2024-07-03)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/329271490)*
