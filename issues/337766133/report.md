# Heap-Buffer-Overflow in glgCopyRowsWithMemCopy

| Field | Value |
|-------|-------|
| **Issue ID** | [337766133](https://issues.chromium.org/issues/337766133) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU>ANGLE |
| **Platforms** | Mac |
| **Chrome Version** | 124.0.0.0 |
| **CVE IDs** | CVE-2021-4058 |
| **Reporter** | de...@gmail.com |
| **Assignee** | ge...@google.com |
| **Created** | 2024-04-29 |
| **Bounty** | $11,000.00 |

## Description

# Steps to reproduce the problem

/

# Problem Description

## Description

This vulnerability occurs in the GPU process and may lead to sandbox escape.

## Root Cause

This vulnerability comes from the incomplete repair of CVE-2021-4058: <https://issues.chromium.org/issues/40057837>
We should set pixel unpack state for compressed textures. However, the fix here only fixes the compressedTexImage3D part, and the vulnerability can still be triggered through webgl's compressedTexSubImage3D function.

## Test Environment

- OS: macOS Ventura 13.5.2(22G91)
- iMac GPU : AMD Radeon Pro Vega 48
- mac-release\_asan-mac-release-1293464
- download link: <https://commondatastorage.googleapis.com/chromium-browser-asan/index.html?prefix=mac-release/asan-mac-release-129>

## reproduce

```
1. Download the newest asan-mac-release chromium
2. ./Chromium.app/Contents/MacOS/Chromium --user-data-dir=./user --enable-logging=stderr --use-angle=gl http://127.0.0.1:8000/poc.html

```
## Fix Patch

```
diff --git a/src/libANGLE/renderer/gl/TextureGL.cpp b/src/libANGLE/renderer/gl/TextureGL.cpp
index 2e3d4c852..485847b24 100644
--- a/src/libANGLE/renderer/gl/TextureGL.cpp
+++ b/src/libANGLE/renderer/gl/TextureGL.cpp
@@ -664,6 +664,7 @@ angle::Result TextureGL::setCompressedSubImage(const gl::Context *context,
         nativegl::GetCompressedSubTexImageFormat(functions, features, format);
 
     stateManager->bindTexture(getType(), mTextureID);
+    ANGLE_TRY(stateManager->setPixelUnpackState(context, unpack));
     if (nativegl::UseTexImage2D(getType()))
     {
         ASSERT(area.z == 0 && area.depth == 1);


```
# Summary

Heap-Buffer-Overflow in glgCopyRowsWithMemCopy

# Custom Questions

#### Type of crash:

gpu

#### Reporter credit:

gelatin dessert

# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: N/A

## Attachments

- [fix.patch](attachments/fix.patch) (text/x-diff, 618 B)
- [poc.html](attachments/poc.html) (text/html, 603 B)
- [asan.log](attachments/asan.log) (text/plain, 35.2 KB)
- [reproduce.png](attachments/reproduce.png) (image/png, 1.5 MB)

## Timeline

### ap...@google.com (2024-05-01)

Project: angle/angle
Branch: main

commit 1bb1ee061fe0bce322fb93b447a72e72c993a1f2
Author: Geoff Lang <geofflang@chromium.org>
Date:   Mon Apr 29 15:27:36 2024

    GL: Sync unpack state for glCompressedTexSubImage3D
    
    Unpack state is supposed to be ignored for compressed tex image calls
    but some drivers use it anyways and read incorrect data.
    
    Texture3DTestES3.PixelUnpackStateTexSubImage covers this case.
    
    Bug: chromium:337766133
    Change-Id: Ic11a056113b1850bd5b4d6840527164a12849a22
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/5498735
    Commit-Queue: Shahbaz Youssefi <syoussefi@chromium.org>
    Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>

M       src/libANGLE/renderer/gl/TextureGL.cpp

https://chromium-review.googlesource.com/5498735


### ap...@google.com (2024-05-01)

Project: chromium/src
Branch: main

commit 1482ceff2751de09848e30d4d9eb179a9ef924a2
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date:   Wed May 01 19:14:47 2024

    Roll ANGLE from 53811e86cc33 to caebfea1f9dd (2 revisions)
    
    https://chromium.googlesource.com/angle/angle.git/+log/53811e86cc33..caebfea1f9dd
    
    2024-05-01 cclao@google.com Vulkan: Make PipelineBarrierArray a class
    2024-05-01 geofflang@chromium.org GL: Sync unpack state for glCompressedTexSubImage3D
    
    If this roll has caused a breakage, revert this CL and stop the roller
    using the controls here:
    https://autoroll.skia.org/r/angle-chromium-autoroll
    Please CC angle-team@google.com,cnorthrop@google.com on the revert to ensure that a human
    is aware of the problem.
    
    To file a bug in ANGLE: https://bugs.chromium.org/p/angleproject/issues/entry
    To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry
    
    To report a problem with the AutoRoller itself, please file a bug:
    https://issues.skia.org/issues/new?component=1389291&template=1850622
    
    Documentation for the AutoRoller is here:
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md
    
    Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86
    Bug: chromium:337766133
    Tbr: cnorthrop@google.com
    Change-Id: I27fbc7f1718c5cf305ceb1c569b2b9b787c0f4ee
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5505902
    Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
    Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
    Cr-Commit-Position: refs/heads/main@{#1294996}

M       DEPS
M       third_party/angle

https://chromium-review.googlesource.com/5505902


### th...@chromium.org (2024-05-01)

Setting the Found In to 124. I can reproduce this on M124 on Mac (checked M126 as well with an earlier version than with the fix above, and it also reproduces there).

### th...@chromium.org (2024-05-01)

IIUC, there's no compromised renderer, and the stack trace indicates memory corruption in the GPU process. Setting the severity as Critical.

### de...@gmail.com (2024-05-02)

Please mark this issue as fixed, and I see that the fix.patch I provided is fully adopted. Please chrome vrp to consider patch reward.

### pe...@google.com (2024-05-02)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2024-05-02)

Setting Priority to P0 to match Severity s0. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### pe...@google.com (2024-05-02)

Requesting merge to stable (M124) because latest trunk commit (1294996) appears to be after stable branch point (1274542).
Requesting merge to beta (M125) because latest trunk commit (1294996) appears to be after beta branch point (1287751).
Merge review required: a commit with DEPS changes was detected.


Merge review required: a commit with DEPS changes was detected.


Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [124, 125].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


### am...@chromium.org (2024-05-03)

The roll with this fix landed on Canary yesterday afternoon but there was not a successful build of Canary since that time, so there is no canary data at present available for review here. And given the minimal time on Canary in general, need to let this bake a bit longer before approving for backmerge to 124 and for M125 Stable Cut occurring on Tuesday.

### am...@chromium.org (2024-05-06)

M125 and M124 merges approved for <https://chromium-review.googlesource.com/c/angle/angle/+/5498735>
Please merge this fix to M125 / branch 6422 and M124/ branch 6367 as soon as possible and before the M125 Stable RC cut tomorrow

### am...@chromium.org (2024-05-06)

I don't see anything about this code that would make this issue specific to Mac, updating the OSes accordingly. I've reached out the primary shepherd to confirm impact to Android since this issue was assessed as a S0.

### ap...@google.com (2024-05-06)

Project: angle/angle
Branch: chromium/6422

commit f4447386db891f772a4472864834612b23d5f525
Author: Geoff Lang <geofflang@chromium.org>
Date:   Mon Apr 29 15:27:36 2024

    M125: GL: Sync unpack state for glCompressedTexSubImage3D
    
    Unpack state is supposed to be ignored for compressed tex image calls
    but some drivers use it anyways and read incorrect data.
    
    Texture3DTestES3.PixelUnpackStateTexSubImage covers this case.
    
    Bug: chromium:337766133
    Change-Id: Ic11a056113b1850bd5b4d6840527164a12849a22
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/5498735
    Commit-Queue: Shahbaz Youssefi <syoussefi@chromium.org>
    Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>
    (cherry picked from commit 1bb1ee061fe0bce322fb93b447a72e72c993a1f2)
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/5518812
    Commit-Queue: Srinivas Sista <srinivassista@chromium.org>
    Reviewed-by: Srinivas Sista <srinivassista@chromium.org>

M       src/libANGLE/renderer/gl/TextureGL.cpp

https://chromium-review.googlesource.com/5518812


### ap...@google.com (2024-05-06)

Project: angle/angle
Branch: chromium/6367

commit c67f290ef0f0433acb766c024d28c6f59f48b909
Author: Geoff Lang <geofflang@chromium.org>
Date:   Mon Apr 29 15:27:36 2024

    M124: GL: Sync unpack state for glCompressedTexSubImage3D
    
    Unpack state is supposed to be ignored for compressed tex image calls
    but some drivers use it anyways and read incorrect data.
    
    Texture3DTestES3.PixelUnpackStateTexSubImage covers this case.
    
    Bug: chromium:337766133
    Change-Id: Ic11a056113b1850bd5b4d6840527164a12849a22
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/5498735
    Commit-Queue: Shahbaz Youssefi <syoussefi@chromium.org>
    Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>
    (cherry picked from commit 1bb1ee061fe0bce322fb93b447a72e72c993a1f2)
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/5518811
    Commit-Queue: Srinivas Sista <srinivassista@chromium.org>
    Reviewed-by: Srinivas Sista <srinivassista@chromium.org>

M       src/libANGLE/renderer/gl/TextureGL.cpp

https://chromium-review.googlesource.com/5518811


### ge...@google.com (2024-05-06)

> I don't see anything about this code that would make this issue specific to Mac, updating the OSes accordingly. I've reached out the primary shepherd to confirm impact to Android since this issue was assessed as a S0.

This is an Apple AMD GPU driver bug so it only affects that one GPU on Macs. The fix was to work around it in ANGLE.

### sp...@google.com (2024-05-09)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $11000.00 for this report.

Rationale for this decision:
$10,000 reward for memory corruption in the GPU process + $1,000 patch bonus 

Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. Two other things we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.
* If you are already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have already registered, there is no need to repeat the process and you’ll automatically be paid soon. If you have any payment related questions or issues, please reach out to p2p-vrp@google.com.

### de...@gmail.com (2024-05-09)

The reward for high quality reporting of GPU vulnerabilities is $15,000.
I've provided the full RCA, reproduction steps and ASAN LOG along with the fix patch, so this is a bit confusing.
If you have other requirements regarding report quality, please let me know.

```
High-quality reports must be reliably reproducible and consist of a proof of concept (POC), symbolized stack trace (if applicable), and steps to reproduce.

Memory Corruption in a highly privileged process (e.g. GPU or network processes) for High-quality reports: $15,000
https://bughunters.google.com/about/rules/chrome-friends/5745167867576320/chrome-vulnerability-reward-program-rules

```

### am...@chromium.org (2024-05-10)

Hi, thanks for the question -- we did think this was a good and solid baseline report, as I think we are missing the "full RCA" you referenced. In the original report it appears that you simply referenced this as a variant of a previous issue due to an incomplete fix of CVE-2021-4058.

You did receive a patch bonus for your fix patch so that was definitely acknowledged as well.
We did have discussion about this, but we are happy to take another look if you would like.

### de...@gmail.com (2024-05-10)

RCA can actually be summarized in just one sentence, I just didn't paste some code into the report like others did.
`We should set pixel unpack state for compressed textures.`

However, I also pointed out the problematic code locations and highlighted the shortcomings of previous patches. I believe developers can fully understand what I meant by RCA.
`However, the fix here only addresses the compressedTexImage3D part, and the vulnerability can still be triggered through webgl's compressedTexSubImage3D function.`

If by RCA you mean a comprehensive code analysis and UAF explanation, then perhaps this isn't a good RCA. Anyway, thank you for your explanation.

### pe...@google.com (2024-08-09)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/337766133)*
