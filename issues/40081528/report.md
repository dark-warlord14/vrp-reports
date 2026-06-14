# Heap-buffer-overflow in blink::WebString::fromUTF8

| Field | Value |
|-------|-------|
| **Issue ID** | [40081528](https://issues.chromium.org/issues/40081528) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>WebGL |
| **Reporter** | w3...@gmail.com |
| **Assignee** | zm...@chromium.org |
| **Created** | 2015-03-03 |
| **Bounty** | $1,000.00 |

## Description

Running Chromium with --no-sandbox reproduces the issue

**VULNERABILITY DETAILS**  

==6700==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x04c7d0d0 at pc 0x111ef9b2 bp 0xdeadbeef sp 0x017cb550  

READ of size 4 at 0x04c7d0d0 thread T0  

[0304/012123:ERROR:client\_util.cc(258)] Could not find exported function RelaunchChromeBrowserWithNewCommandLineIfNeeded  

#0 0x111ef9b1 in WTF::String::fromUTF8 C:\b\build\slave\Win\_ASan\_Release\build\src\third\_party\WebKit\Source\wtf\text\ASCIIFastPath.h:91  

#1 0x111c1d65 in blink::WebString::fromUTF8 C:\b\build\slave\Win\_ASan\_Release\build\src\third\_party\WebKit\Source\wtf\text\WTFString.h:392  

#2 0x1a8f4f70 in gpu\_blink::WebGraphicsContext3DImpl::getActiveUniform C:\b\build\slave\Win\_ASan\_Release\build\src\gpu\blink\webgraphicscontext3d\_impl.cc:403  

#3 0x13aa2918 in blink::WebGLRenderingContextBase::getActiveUniform C:\b\build\slave\Win\_ASan\_Release\build\src\third\_party\WebKit\Source\core\html\canvas\WebGLRenderingContextBase.cpp:2117  

#4 0x1579c8b7 in blink::v8SetReturnValue<v8::FunctionCallbackInfo[v8::Value](javascript:void(0);),blink::WebGLActiveInfo> C:\b\build\slave\Win\_ASan\_Release\build\src\out\Release\gen\blink\bindings\core\v8\V8WebGLRenderingContext.cpp:1826  

#5 0x15730c4c in blink::AutocompleteErrorEvent::create C:\b\build\slave\Win\_ASan\_Release\build\src\out\Release\gen\blink\bindings\core\v8\V8WebGLRenderingContext.cpp:1832  

#6 0x11f8d5e8 in v8::internal::FunctionCallbackArguments::Call C:\b\build\slave\Win\_ASan\_Release\build\src\v8\src\arguments.cc:33  

#7 0x11b2a9fb in v8::internal::Builtins::InvokeApiFunction C:\b\build\slave\Win\_ASan\_Release\build\src\v8\src\builtins.cc:1077  

#8 0x11b3777b in v8::internal::Builtins::Builtins C:\b\build\slave\Win\_ASan\_Release\build\src\v8\src\builtins.cc:1100

0x04c7d0d1 is located 0 bytes to the right of 1-byte region [0x04c7d0d0,0x04c7d0d1)  

allocated by thread T0 here:  

#0 0x1074bf8 in malloc c:\b\build\slave\win\_asan\_release\build\src\third\_party\llvm\projects\compiler-rt\lib\asan\asan\_malloc\_win.cc:58  

#1 0x1bd6140d in operator new f:\dd\vctools\crt\crtw32\heap\new.cpp:59  

#2 0x1a8f4e28 in gpu\_blink::WebGraphicsContext3DImpl::getActiveUniform C:\b\build\slave\Win\_ASan\_Release\build\src\gpu\blink\webgraphicscontext3d\_impl.cc:390  

#3 0x13aa2918 in blink::WebGLRenderingContextBase::getActiveUniform C:\b\build\slave\Win\_ASan\_Release\build\src\third\_party\WebKit\Source\core\html\canvas\WebGLRenderingContextBase.cpp:2117  

#4 0x1579c8b7 in blink::v8SetReturnValue<v8::FunctionCallbackInfo[v8::Value](javascript:void(0);),blink::WebGLActiveInfo> C:\b\build\slave\Win\_ASan\_Release\build\src\out\Release\gen\blink\bindings\core\v8\V8WebGLRenderingContext.cpp:1826  

#5 0x15730c4c in blink::AutocompleteErrorEvent::create C:\b\build\slave\Win\_ASan\_Release\build\src\out\Release\gen\blink\bindings\core\v8\V8WebGLRenderingContext.cpp:1832  

#6 0x11f8d5e8 in v8::internal::FunctionCallbackArguments::Call C:\b\build\slave\Win\_ASan\_Release\build\src\v8\src\arguments.cc:33  

#7 0x11b2a9fb in v8::internal::Builtins::InvokeApiFunction C:\b\build\slave\Win\_ASan\_Release\build\src\v8\src\builtins.cc:1077  

#8 0x11b3777b in v8::internal::Builtins::Builtins C:\b\build\slave\Win\_ASan\_Release\build\src\v8\src\builtins.cc:1100

SUMMARY: AddressSanitizer: heap-buffer-overflow C:\b\build\slave\Win\_ASan\_Release\build\src\third\_party\WebKit\Source\wtf\text\ASCIIFastPath.h:91 WTF::String::fromUTF8

**VERSION**  

Chrome Version: Version 43.0.2321.0 (asan-win32-release-318863)  

Operating System: Windows

I have also tested this to work with Linux 64bit.

## Attachments

- [chrome-fromutf8.html](attachments/chrome-fromutf8.html) (text/html, 2.0 KB)
- [linux_asan_log.txt](attachments/linux_asan_log.txt) (text/plain, 10.8 KB)
- [win_gpu.txt](attachments/win_gpu.txt) (text/plain, 3.3 KB)
- [linux_gpu.txt](attachments/linux_gpu.txt) (text/plain, 2.5 KB)

## Timeline

### w3...@gmail.com (2015-03-05)

Attaching the ASAN log on linux.

### in...@chromium.org (2015-03-05)

Thanks a lot Omair for the report. Good to see you back! If you are interested in the Fuzzer Contribution Program on ClusterFuzz, definitely ping me, i can get you started.

### cl...@chromium.org (2015-03-05)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5663809184727040

### cl...@chromium.org (2015-03-05)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5793631886114816

### cl...@chromium.org (2015-03-05)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5663809184727040

Uploader: aarya@google.com
Job Type: Windows_asan_chrome

Crash Type: Heap-buffer-overflow READ 4
Crash Address: 0x0ca6acd0
Crash State:
  blink::WebString::fromUTF8
  gpu_blink::WebGraphicsContext3DImpl::getActiveUniform
  blink::WebGLRenderingContextBase::getActiveUniform
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=windows_asan_chrome&range=319249:319250

Minimized Testcase (1.71 Kb): https://cluster-fuzz.appspot.com/download/AMIfv97G5uPyp04JJ8eOZxu8Jy42vIS-JhBEfjbvVo6pE0sroZ0O7OaZVPFGBRsN0BhmFz1E3n-mAsQc1jBwBOkWP816hcNTXCIJtrQJiuIBcZP-SSOZWxzbtaT1QfC9P7sXIRxy5BRz3ykb2J4GJPzdp8QnQcsMQw



### cl...@chromium.org (2015-03-05)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5793631886114816

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-buffer-overflow READ 8
Crash Address: 0x6090001c65b0
Crash State:
  blink::WebString::fromUTF8
  gpu_blink::WebGraphicsContext3DImpl::getActiveUniform
  blink::WebGLRenderingContextBase::getActiveUniform
  

Minimized Testcase (1.71 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94r4RT8OdMh2ilEb43FagLVjiJqcQwgYUEL6sW1NoHXEw_9fj-B1vmdBSezHhdGXBzSF7ugx_KNgTHFTu2SMNQaf45SLyc6amOtxuBqvt46GD0J_lHAbzNVfzg7v2mMLHoeuiObfNayqEShhAVdzYUqmNAkzQ



### kb...@chromium.org (2015-03-05)

Could you please attach about:gpu output from the affected machines?

It looks to me like there is a bug in the OpenGL driver where it is not leaving the return values from glGetActiveUniform untouched as it should when an error is produced, as this test case does. The test case attempts to fetch an active uniform whose index is out of range.


### w3...@gmail.com (2015-03-05)

Attached the output as requested.

### zm...@chromium.org (2015-03-06)

I don't have access to the minimized testcase. 

@inferno: please help

### in...@chromium.org (2015-03-06)

please go to the report link [https://cluster-fuzz.appspot.com/testcase?key=5663809184727040] to access 

### zm...@chromium.org (2015-03-06)

OK, I think I fully understand the out-of-bound visit case.

We link a program successfully, then detach a shader, and try to relink.  Now we generate an error in command buffer, knowing that a shader is missing from the program.  However, in the driver the program is still valid with all states, because the failed link call never reaches there.

Now, we call getActiveUniform.  In the client side cache, we have zero active uniforms (this is correct), so we turn to service side in the hope to generate an GL error (This is an overdo in my eyes).  On the service side, we actually return with the information because the program on the driver is still valid.

SO where the out-of-bound write happens, is WebGraphicsContext3DImpl::getActiveUniform() on the client side, where we query the maximum uniform name length, which returns 1 (from cached states).  But the service side instead of generating an error, it returns a name that's beyond the buffer (size of 1) to hold the name, therefore, out-of-bound write.

### zm...@chromium.org (2015-03-06)

My proposal to fix this bug:

1) Always trust the cache, and generate an error on client side if cache indicates the query is invalid (for example, uniform index is out of bound).

2) We can actually delete all these individual query commands from the command buffer.  Because all the successful queries got their info from the client side cache, which is returned by the internal CHROMIUM super commands (lie GetProgramInfo, etc).  The only use of such individual query commands is for generate an error, and from here, they are not event doing that job successfully.  SO what we do with them?  Termination!

### zm...@chromium.org (2015-03-06)

[Empty comment from Monorail migration]

### zm...@chromium.org (2015-03-06)

Once we fix this bug and merge back to various releases, I'll add more test cases to WebGL conformance tests.  It's hard to believe we have such cases untested.

### bu...@chromium.org (2015-03-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/44ad5ecc3abf8f31d7e55a9ece5cea30a710fd77

commit 44ad5ecc3abf8f31d7e55a9ece5cea30a710fd77
Author: zmo <zmo@chromium.org>
Date: Mon Mar 09 22:13:19 2015

Fix glGetActiveUniform/Attrib crashes due to state inconsistency

between what Chrome thinks and what the driver is.

This is caused by we intercept invalid program and generate an error on
LinkProgram rather than passing it to the driver, so the driver still have
a valid program if the previous link succeeds.

BUG=463599
TEST=test case in the bug
R=sievers@chromium.org

Review URL: https://codereview.chromium.org/978193003

Cr-Commit-Position: refs/heads/master@{#319746}

[modify] http://crrev.com/44ad5ecc3abf8f31d7e55a9ece5cea30a710fd77/gpu/blink/webgraphicscontext3d_impl.cc


### in...@chromium.org (2015-03-09)

[Empty comment from Monorail migration]

### zm...@chromium.org (2015-03-09)

I think this should be merged back to all branches alive.

### ti...@google.com (2015-03-09)

zmo: I can take care of the merge requests for you (after the fix has had some bake time on trunk).

### bu...@chromium.org (2015-03-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/ac89bdd636a4a6d8f15415e69b40e546cb020567

commit ac89bdd636a4a6d8f15415e69b40e546cb020567
Author: zmo <zmo@chromium.org>
Date: Tue Mar 10 02:09:05 2015

Add a mechanism for command buffer to conditionally allow ES3 enums.

Although ultimately we want to remove validators from command buffer, but the
fastest way to allow an experimental WebGL 2 is actually appending the current
validators.

Appended the BufferTarget as an sample to make sure code generator works.

BUG=463599
TEST=gpu_unittests, webgl conformance tests
R=sievers@chromium.org

Review URL: https://codereview.chromium.org/987123003

Cr-Commit-Position: refs/heads/master@{#319819}

[modify] http://crrev.com/ac89bdd636a4a6d8f15415e69b40e546cb020567/gpu/command_buffer/build_gles2_cmd_buffer.py
[modify] http://crrev.com/ac89bdd636a4a6d8f15415e69b40e546cb020567/gpu/command_buffer/common/gles2_cmd_utils_implementation_autogen.h
[modify] http://crrev.com/ac89bdd636a4a6d8f15415e69b40e546cb020567/gpu/command_buffer/service/feature_info.cc
[modify] http://crrev.com/ac89bdd636a4a6d8f15415e69b40e546cb020567/gpu/command_buffer/service/feature_info.h
[modify] http://crrev.com/ac89bdd636a4a6d8f15415e69b40e546cb020567/gpu/command_buffer/service/gles2_cmd_decoder.cc
[modify] http://crrev.com/ac89bdd636a4a6d8f15415e69b40e546cb020567/gpu/command_buffer/service/gles2_cmd_validation.h
[modify] http://crrev.com/ac89bdd636a4a6d8f15415e69b40e546cb020567/gpu/command_buffer/service/gles2_cmd_validation_implementation_autogen.h


### cl...@chromium.org (2015-03-10)

ClusterFuzz has detected this issue as fixed in range 319619:319868.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5793631886114816

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-buffer-overflow READ 8
Crash Address: 0x6090001c65b0
Crash State:
  blink::WebString::fromUTF8
  gpu_blink::WebGraphicsContext3DImpl::getActiveUniform
  blink::WebGLRenderingContextBase::getActiveUniform
  
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=319619:319868

Minimized Testcase (1.71 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94r4RT8OdMh2ilEb43FagLVjiJqcQwgYUEL6sW1NoHXEw_9fj-B1vmdBSezHhdGXBzSF7ugx_KNgTHFTu2SMNQaf45SLyc6amOtxuBqvt46GD0J_lHAbzNVfzg7v2mMLHoeuiObfNayqEShhAVdzYUqmNAkzQ

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### cl...@chromium.org (2015-03-10)

[Empty comment from Monorail migration]

### ti...@google.com (2015-03-16)

[Empty comment from Monorail migration]

### ti...@google.com (2015-03-16)

Merge Requested to M42

### am...@google.com (2015-03-16)

Approved for M42 (branch: 2311)

### am...@google.com (2015-03-16)

[Automated comment] Request affecting a post-stable build (M41), manual review required.

### pe...@google.com (2015-03-20)

Merge approved for m41 branch 2272.

### ti...@google.com (2015-03-26)

@zmo - please merge to M42 (branch 2311). Please hold off of the merge to M41 until we have some beta coverage.

### kb...@chromium.org (2015-03-27)

Note: @zmo is out of the office for a few weeks. We should find someone else to do this merge.


### bu...@chromium.org (2015-03-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/73f24f1ef5e222566a84070887eb5120cdef55e8

commit 73f24f1ef5e222566a84070887eb5120cdef55e8
Author: Will Harris <wfh@chromium.org>
Date: Fri Mar 27 22:31:05 2015

Merge: Fix glGetActiveUniform/Attrib crashes due to state inconsistency

between what Chrome thinks and what the driver is.

This is caused by we intercept invalid program and generate an error on
LinkProgram rather than passing it to the driver, so the driver still have
a valid program if the previous link succeeds.

BUG=463599
TEST=test case in the bug
R=sievers@chromium.org

Review URL: https://codereview.chromium.org/978193003

Cr-Commit-Position: refs/heads/master@{#319746}
(cherry picked from commit 44ad5ecc3abf8f31d7e55a9ece5cea30a710fd77)

Review URL: https://codereview.chromium.org/1039423002

Cr-Commit-Position: refs/branch-heads/2311@{#368}
Cr-Branched-From: 09b7de5dd7254947cd4306de907274fa63373d48-refs/heads/master@{#317474}

[modify] http://crrev.com/73f24f1ef5e222566a84070887eb5120cdef55e8/gpu/blink/webgraphicscontext3d_impl.cc


### ti...@google.com (2015-03-27)

Thanks wfh!

Removing M41 target as it's too late for that milestone.

### in...@chromium.org (2015-04-13)

[Empty comment from Monorail migration]

### ti...@google.com (2015-04-14)

Congrats w3bd3vil - Our panel decided to reward you with $1000 for this report!

Someone from our finance area should be in contact in two weeks to collect payment details. Please contact me directly if this doesn't happen.

We'll credit you in our release notes as w3bd3vil. Please let me know if you'd like to use another name.

Cheers,
Tim


*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an established charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### ti...@google.com (2015-05-06)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-06-15)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2015-06-25)

Processing via our e-payment system can take up to two weeks, but the reward should be on its way to you. Thanks again for your help!

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-28)

[Empty comment from Monorail migration]

### is...@google.com (2018-07-28)

This issue was migrated from crbug.com/chromium/463599?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081528)*
