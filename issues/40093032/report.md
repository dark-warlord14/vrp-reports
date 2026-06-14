# OOB operation in swiftshader's JIT

| Field | Value |
|-------|-------|
| **Issue ID** | [40093032](https://issues.chromium.org/issues/40093032) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>GPU>SwiftShader |
| **Platforms** | Linux, Windows |
| **Reporter** | cd...@gmail.com |
| **Assignee** | ni...@google.com |
| **Created** | 2018-11-12 |
| **Bounty** | $1,000.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36

Steps to reproduce the problem:
1. run chrome ./poc.html

What is the expected behavior?

What went wrong?
Can get out of bound operation in swiftshader's ELF image memory(or JIT?).To get the crash stable,you can use args --disable-gpu to load swiftshader.
It crashes both in Win10 RS5 chrome 70.0.3538.102 stable version and ubuntu chromium asan 72.0.3594.0 version.

Did this work before? N/A 

Chrome version: 70.0.3538.102  Channel: stable
OS Version: win10 RS4
Flash Version:

## Attachments

- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)

## Timeline

### ke...@chromium.org (2018-11-12)

I haven't been able to reproduce this one either. Do you have a crash ID for it?

### cd...@gmail.com (2018-11-13)

I enabled the crash report.It crashed but somehow did not generate the crash ID and dmp file.
Could u please try the way to use page heap and refresh the page? And another way is using content_shell or add --single-process. All the way above does help to repro it easily and please add the important args: --disable-gpu.These are also helpful for https://crbug.com/chromium/904276.

By the way,the log in linux asan version is too short to help,just like this one :
Received signal 11 SEGV_MAPERR 7f9bf27704e4
    #0 0x558fded36e01 in __interceptor_backtrace /b/swarming/w/ir/kitchen-workdir/src/third_party/llvm/compiler-rt/lib/asan/../sanitizer_common/sanitizer_common_interceptors.inc:4024:13
    #1 0x558fe8efa371 in base::debug::StackTrace::StackTrace(unsigned long) /home/lly/chrome/src/out/asan/../../base/debug/stack_trace_posix.cc:820:41
    #2 0x558fe8ef9250 in base::debug::(anonymous namespace)::StackDumpSignalHandler(int, siginfo_t*, void*) /home/lly/chrome/src/out/asan/../../base/debug/stack_trace_posix.cc:341:3
    #3 0x7f9c17628390 in __funlockfile ??:?
    #4 0x7f9c17628390 in ?? ??:0
#4 0x7f9c050c8c79 <unknown>
  r8: 0000000000000000  r9: 0000000000000003 r10: 00000ff37bab2607 r11: 00007f9bdd5932b8
 r12: 00007f9c0345f810 r13: 00007f9c0345f810 r14: 0000000000000001 r15: 00007f9bf2776810
  di: 00007f9bf2776810  si: 00007f9c0345fa50  bp: 00007f9bd4e249f0  bx: 00007f9bd4e248c0
  dx: ffffffffffff8424  ax: 00000000ffffe100  cx: 00007f9bf27780c0  sp: 00007f9bd4e24660
  ip: 00007f9c050c8c79 efl: 0000000000010206 cgf: 002b000000000033 erf: 0000000000000004
 trp: 000000000000000e msk: 0000000000000000 cr2: 00007f9bf27704e4
[end of stack trace]
Calling _exit(1). Core file will not be generated.


### dr...@chromium.org (2018-11-15)

I haven't been able to reproduce this crash either, on Windows or Linux. Can you upload a crash from chrome://crashes? Or give more information on what version and configuration of Chrome you are using?

### dr...@chromium.org (2018-11-15)

[Empty comment from Monorail migration]

### cd...@gmail.com (2018-11-16)

"It crashes both in Win10 RS5 chrome 70.0.3538.102 stable version and ubuntu chromium asan 72.0.3594.0 version."

About the crash ID,i turn on the switch,but there is still nothing remained in chrome://crashes or  ~/.config/google-chrome/crashes.And i'll try to provide the details as possible as i can.

In ubuntu ,I test in asan-linux-release-606772 again.And it do repro again.Here are my steps:

1.Download the asan-linux-release-606772.
2.Put Poc.html and the utility.js,Di-3d.png  into the same directory.
3.Start a simple webserver like "python -m http.server 8080" from the directory.
4.Run ./chrome --disable-gpu http://127.0.0.1:8080/POC.html
*5.If it did not crash,press F5 to refresh the page.
*6.Do step 5 until crash happened.

Then crash happened.And perhaps cuz it crashed in the JIT memory space from libglesv2.so(swiftshader) in gpu process,the crash information is just one line like "Received signal 11 SEGV_ACCERR 633001514698".

So above are the information on what version and configuration of Chrome im using. Could u please tell me anything u need else? 

BTW,this still work with https://crbug.com/chromium/904276.


### sh...@chromium.org (2018-11-16)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### dr...@chromium.org (2018-11-16)

Excellent, thank you for the steps in #5, they worked perfectly. I had to refresh many times to get the message "Received signal 11 SEGV_ACCERR 633001514698", but it does occur reliably (with several refreshes each time) and does indicate a bug.

Assigning low severity due to the need for the flag --disable_gpu, and assigning to sugoi@ with the SwiftShader team for further triage.

[Monorail components: Internals>GPU>SwiftShader]

### cd...@gmail.com (2018-11-16)

Hi,@drubery
Please see the https://bugs.chromium.org/p/chromium/issues/detail?id=904714#8
https://crbug.com/chromium/904265#c8 by capn@chromium.org:
The --disable-gpu flag isn't strictly necessary. Chrome falls back to using SwiftShader when the GPU process crashes three times, which is easy to achieve. So any SwiftShader vulnerability affects all our users (see also https://googleprojectzero.blogspot.com/2018/10/heap-feng-shader-exploiting-swiftshader.html).

### dr...@chromium.org (2018-11-16)

I see. That's good to know. I had assumed crashing the GPU process was somewhat difficult. Moving to Medium then.

### su...@chromium.org (2018-11-16)

[Empty comment from Monorail migration]

### ca...@chromium.org (2018-11-16)

Thanks for reporting this. I'll have a closer look.

### sh...@chromium.org (2018-11-26)

nicolascapens: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ca...@chromium.org (2018-11-26)

Reproduced on Linux with local chrome build. Will try to reproduce on Windows now for ease of debugging.

### bu...@chromium.org (2018-11-28)

The following revision refers to this bug:
  https://swiftshader.googlesource.com/SwiftShader.git/+/79d0e565b0013c80c45769065c15b26058057262

commit 79d0e565b0013c80c45769065c15b26058057262
Author: Nicolas Capens <capn@google.com>
Date: Wed Nov 28 17:32:41 2018

Fix textureSize for non-uniform samplers.

GLSL textureSize() calls that use a sampler that is not a uniform,
should not use the index of the register as the texture unit index.
Instead the index is the value stored in the register itself.

https://crbug.com/chromium/904265

Change-Id: Iee1058e789daae15248ae5ffa940a0155dca61b5
Reviewed-on: https://swiftshader-review.googlesource.com/c/22910
Tested-by: Nicolas Capens <nicolascapens@google.com>
Reviewed-by: Alexis Hétu <sugoi@google.com>

[modify] https://crrev.com/79d0e565b0013c80c45769065c15b26058057262/src/Pipeline/PixelProgram.cpp
[modify] https://crrev.com/79d0e565b0013c80c45769065c15b26058057262/src/Pipeline/VertexProgram.cpp
[modify] https://crrev.com/79d0e565b0013c80c45769065c15b26058057262/src/Shader/PixelProgram.cpp
[modify] https://crrev.com/79d0e565b0013c80c45769065c15b26058057262/src/Shader/VertexProgram.cpp


### bu...@chromium.org (2018-11-29)

The following revision refers to this bug:
  https://swiftshader.googlesource.com/SwiftShader.git/+/a972758d6e10df761631daf1f33a2ef2a17cb699

commit a972758d6e10df761631daf1f33a2ef2a17cb699
Author: Nicolas Capens <capn@google.com>
Date: Thu Nov 29 01:44:34 2018

Work around Subzero constant folding limitation.

The Subzero JIT only supports constants in the second operand of
arithmetic operations, not the first. It assumes constant folding
already took place (true for NaCl which takes LLVM IR as input).
Reactor has constant folding as part of the static C++ compilation,
but the Optimizer may substitute the first operand for a constant
(i.e. constant propagation).

Addressing it in the Optimizer by not performing the substitution
is not trivial because we'd have to check each use. And it would
cost run-time performance. Ideally we'd have a pass for
legalization/optimization which performs constant folding.

For now, avoid hitting 'unreachable' code in Subzero by multiplying
constants at the Reactor level.

Fixes regression caused by https://swiftshader-review.googlesource.com/22910

https://crbug.com/chromium/904265
https://crbug.com/swiftshader/14

Change-Id: Ifdc72ac997ad5d71c1f7006259f54f3d715cb613
Reviewed-on: https://swiftshader-review.googlesource.com/c/22930
Tested-by: Nicolas Capens <nicolascapens@google.com>
Reviewed-by: Nicolas Capens <nicolascapens@google.com>

[modify] https://crrev.com/a972758d6e10df761631daf1f33a2ef2a17cb699/src/Pipeline/PixelProgram.cpp
[modify] https://crrev.com/a972758d6e10df761631daf1f33a2ef2a17cb699/src/Pipeline/VertexProgram.cpp
[modify] https://crrev.com/a972758d6e10df761631daf1f33a2ef2a17cb699/src/Shader/PixelProgram.cpp
[modify] https://crrev.com/a972758d6e10df761631daf1f33a2ef2a17cb699/src/Shader/VertexProgram.cpp


### bu...@chromium.org (2018-11-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/dfe266e269441ae61b64272e5550d44a2c3f7faf

commit dfe266e269441ae61b64272e5550d44a2c3f7faf
Author: Nicolas Capens <capn@chromium.org>
Date: Thu Nov 29 21:46:58 2018

Roll SwiftShader 8f20452..a972758

https://swiftshader.googlesource.com/SwiftShader.git/+log/8f20452..a972758

BUG=chromium:904265

TEST=bots

CQ_INCLUDE_TRYBOTS=luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:android_optional_gpu_tests_rel

Change-Id: I6b5a14c70cc6f3324542923b95bf2f1a87b336cc
Reviewed-on: https://chromium-review.googlesource.com/c/1355524
Reviewed-by: Alexis Hétu <sugoi@chromium.org>
Commit-Queue: Nicolas Capens <capn@chromium.org>
Cr-Commit-Position: refs/heads/master@{#612385}
[modify] https://crrev.com/dfe266e269441ae61b64272e5550d44a2c3f7faf/DEPS


### ni...@google.com (2018-11-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-11-30)

[Empty comment from Monorail migration]

### na...@google.com (2018-12-03)

[Empty comment from Monorail migration]

### wf...@chromium.org (2018-12-05)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-12-07)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-12-07)

Hi! $1000 for this report, many thanks!

### aw...@google.com (2018-12-07)

[Empty comment from Monorail migration]

### cd...@gmail.com (2018-12-10)

Thanks for the reward!
Cheers

### sh...@chromium.org (2018-12-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-12-14)

This bug requires manual review: DEPS changes referenced in bugdroid comments.
Please contact the milestone owner if you have questions.
Owners: govind@(Android), kariahda@(iOS), djmm@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ab...@chromium.org (2018-12-14)

Seems like this should be in M72 already, but can you please confirm?

### ca...@chromium.org (2018-12-16)

This is in M72 already: https://chromiumdash.appspot.com/commits?commit=dfe266e269441ae61b64272e5550d44a2c3f7faf&platform=Windows

### ab...@google.com (2018-12-18)

[Empty comment from Monorail migration]

### aw...@google.com (2019-01-28)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-01-28)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-02-19)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-03-08)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sa...@gmail.com (2020-09-25)

poc


### is...@google.com (2020-09-25)

This issue was migrated from crbug.com/chromium/904265?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093032)*
