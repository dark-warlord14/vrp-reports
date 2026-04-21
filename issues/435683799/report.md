# heap-buffer-overflow in ANGLE for Chromium on MacOS

| Field | Value |
|-------|-------|
| **Issue ID** | [435683799](https://issues.chromium.org/issues/435683799) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU>ANGLE |
| **Platforms** | Mac |
| **Reporter** | ul...@gmail.com |
| **Assignee** | ge...@chromium.org |
| **Created** | 2025-08-01 |
| **Bounty** | $10,000.00 |

## Description

**Summary:** heap-buffer-overflow in ANGLE for Chromium on MacOS

**Program:** Google VRP

**Vulnerability type:** Memory Corruption (in a non-sandboxed process)

### Details

**Vulnerability Description**

A heap buffer overflow can be triggered in rx::TextureMtl::convertAndSetPerSliceSubImage on the GPUProcesss when rendering WebGL sub-texture images with distinct texture internal formats than the parent texture image.

**Attack Preconditions**

Victim must be running Chrome in MacOS and visit an attacker controlled site.
Reproduced with Chromium commit `55ef465252c430118795e71960faa4bd7d9a39c0` on MacOS

**Reproduction Steps / POC**

1. Build Chrome on MacOS with ASAN enabled
2. host and navigate to the attached `testcase.html`
3. You should see the attached ASAN report `asan_crashlog.txt`. The following is a cropped snippet:

```
==12947==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x0001203c4800 at pc 0x000118d786b4 bp 0x00016f303e40 sp 0x00016f303e38
READ of size 1 at 0x0001203c4800 thread T0
==12947==WARNING: invalid path to external symbolizer!
==12947==WARNING: Failed to use and restart external symbolizer!
    #0 0x000118d786b0 in angle::LoadLA8ToRGBA8(angle::ImageLoadContext const&, unsigned long, unsigned long, unsigned long, unsigned char const*, unsigned long, unsigned long, unsigned char*, unsigned long, unsigned long)+0x970 (/Users/user/Research/sources/Chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/140.0.7332.0/Libraries/libGLESv2.dylib:arm64+0x1a906b0)
    #1 0x000118bee448 in rx::TextureMtl::convertAndSetPerSliceSubImage(gl::Context const*, int, MTLRegion const&, gl::InternalFormat const&, unsigned int, angle::Format const&, unsigned long, unsigned long, gl::Buffer*, unsigned char const*, std::__Cr::shared_ptr<rx::mtl::Texture> const&)+0x9d4 (/Users/user/Research/sources/Chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/140.0.7332.0/Libraries/libGLESv2.dylib:arm64+0x1906448)
    #2 0x000118becbdc in rx::TextureMtl::setPerSliceSubImage(gl::Context const*, int, MTLRegion const&, gl::InternalFormat const&, unsigned int, angle::Format const&, unsigned long, unsigned long, gl::Buffer*, unsigned char const*, std::__Cr::shared_ptr<rx::mtl::Texture> const&)+0x19c (/Users/user/Research/sources/Chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/140.0.7332.0/Libraries/libGLESv2.dylib:arm64+0x1904bdc)
    #3 0x000118be3e04 in rx::TextureMtl::setSubImageImpl(gl::Context const*, gl::ImageIndex const&, gl::Box const&, gl::InternalFormat const&, unsigned int, gl::PixelUnpackState const&, gl::Buffer*, unsigned char const*)+0x4d4 (/Users/user/Research/sources/Chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/140.0.7332.0/Libraries/libGLESv2.dylib:arm64+0x18fbe04)
    #4 0x000118be4364 in rx::TextureMtl::setCompressedSubImage(gl::Context const*, gl::ImageIndex const&, gl::Box const&, unsigned int, gl::PixelUnpackState const&, unsigned long, unsigned char const*)+0x80 (/Users/user/Research/sources/Chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/140.0.7332.0/Libraries/libGLESv2.dylib:arm64+0x18fc364)
    #5 0x000117bd337c in gl::Texture::setCompressedSubImage(gl::Context const*, gl::PixelUnpackState const&, gl::TextureTarget, int, gl::Box const&, unsigned int, unsigned long, unsigned char const*)+0x2d8 (/Users/user/Research/sources/Chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/140.0.7332.0/Libraries/libGLESv2.dylib:arm64+0x8eb37c)
    #6 0x0001179c21c4 in gl::Context::compressedTexSubImage2DRobust(gl::TextureTarget, int, int, int, int, int, unsigned int, int, int, void const*)+0x190 (/Users/user/Research/sources/Chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/140.0.7332.0/Libraries/libGLESv2.dylib:arm64+0x6da1c4)
    #7 0x0001173e4fb0 in GL_CompressedTexSubImage2DRobustANGLE+0x41c (/Users/user/Research/sources/Chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/140.0.7332.0/Libraries/libGLESv2.dylib:arm64+0xfcfb0)
    #8 0x00031c062dac in gpu::gles2::GLES2DecoderPassthroughImpl::DoCompressedTexSubImage2D(unsigned int, int, int, int, int, int, unsigned int, int, int, void const*)+0xd4 (/Users/user/Research/sources/Chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/140.0.7332.0/Chromium Framework:arm64+0x1c062dac)
    #9 0x00031c0d3864 in gpu::gles2::GLES2DecoderPassthroughImpl::HandleCompressedTexSubImage2DBucket(unsigned int, void const volatile*)+0x244 (/Users/user/Research/sources/Chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/140.0.7332.0/Chromium Framework:arm64+0x1c0d3864)
    #10 0x00031c0e46dc in gpu::error::Error gpu::gles2::GLES2DecoderPassthroughImpl::DoCommandsImpl<false>(unsigned int, void const volatile*, int, int*)+0x280 

```
### Attack scenario

This heap-buffer-overflow is product of the poor tracking of texture internal formats across texture image and sub-image instances, leading to an `internalFormat` type-confusion that can be abused to cause reads (and potentially writes) to OOB data. For a read scenario, since the OOB data is written to the texture buffer itself, this data can be retrieved via a framebuffer in a similar way as shown below, which would successfully achieve an info-leak primitive:

```
// constraint texture base level to be 3 to get the data back in the right format
gl.texParameteri(gl.TEXTURE_2D_ARRAY, gl.TEXTURE_BASE_LEVEL, 3);
gl.texParameteri(gl.TEXTURE_2D_ARRAY, gl.TEXTURE_MAX_LEVEL, 3);

// create a framebuffer to read the data back from the texture
var fb = gl.createFramebuffer();
gl.bindFramebuffer(gl.FRAMEBUFFER, fb);
gl.framebufferTextureLayer(gl.FRAMEBUFFER, gl.COLOR_ATTACHMENT0, texture, 1, 0);

var check = gl.checkFramebufferStatus(gl.FRAMEBUFFER)
if (check == gl.FRAMEBUFFER_COMPLETE) {
    var floatData = new Float32Array(height * width * depth * 12); 
    gl.readPixels(0, 0, width, height, gl.RG, gl.FLOAT, floatData);
    
    var uintData = new Uint8Array(floatData);
    for (let i = 0; i < uintData.length; i += 1)
        console.log(uintData[i].toString(16));

} else {
    console.error('Framebuffer is not complete: 0x' + check.toString(16));
}

```

## Attachments

- testcase.html (text/html, 2.2 KB)
- asan_crashlog.txt (text/plain, 39.5 KB)

## Timeline

### sp...@google.com (2025-08-01)

*NOTE: This is an automatically generated email*

Hi! Many thanks for sharing your report.

This email confirms we've received your message. We'll investigate the issue you've reported and get back to you once we have an update. In the meantime, you might want to take a look at the [list of frequently asked questions about Google Bug Hunters](https://bughunters.google.com/about/4925519884451840/frequently-asked-questions).

Also, if you have not already done so, create a profile on [the Google Bughunters site](https://bughunters.google.com/) if you'd like us to publicly recognize your contribution:

- [Leaderboard](https://bughunters.google.com/leaderboard) – You'll be added here if we issue a reward for your report.
- [Honorable Mentions](https://bughunters.google.com/leaderboard/honorable-mentions) – You'll be added here if you are not in the Hall of Fame, but we file a security vulnerability bug based on your report.

**Note that we only act on reports concerning vulnerabilities or technical security problems in one of our products. This is not the correct channel if you need to resolve a problem with your account, or want to report non-security bugs or suggest a new product feature.**

Good news! According to Google magic, your report is likely actionable for us, so it has been moved up in our queue by raising the priority. The next step is human expert review, which should happen slightly sooner now.

Cheers,   

Google Security Bot

[Follow us](https://twitter.com/googlevrp) on Twitter!

### yh...@google.com (2025-08-04)

This report may qualify for the [Chrome Vulnerability Reward Program](https://bughunters.google.com/about/rules/chrome-friends/5745167867576320/chrome-vulnerability-reward-program-rules). We are moving this report to the Chromium issue tracker.

### ja...@chromium.org (2025-08-04)

[security shepherd]

Thanks for the report. I don't have MacOS to test this on, but I'm going to treat this as speculatively true and assign some teammates to take a look.

### ja...@chromium.org (2025-08-04)

[security shepherd]
Since we consider the GPU process sandboxed on MacOS: assigning this medium (S2).

### ja...@chromium.org (2025-08-04)

[security shepherd]

The provided stack trace was for M140, but this may impact earlier builds.

geofflang@, can you take a look or pass to someone on your team who can try reproducing this? Thank you

### ja...@chromium.org (2025-08-04)

Reporter, can you reproduce this on earlier versions of Chrome?

### ul...@gmail.com (2025-08-05)

I have reproduced this vulnerability in an earlier commit before I pulled to latest at the time of reporting. But I don't recall which commit that was. I can checkout to any specific commit and test for you If you need me to

### pe...@google.com (2025-08-05)

Thank you for providing more feedback. Adding the requester to the CC list.

### ch...@google.com (2025-08-05)

Setting milestone because of s2 severity.

### ch...@google.com (2025-08-05)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security Impact hotlist or the Severity field, and remove the ReleaseBlock hotlist.

### ul...@gmail.com (2025-08-13)

redacted

### ch...@google.com (2025-08-19)

geofflang: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ge...@google.com (2025-08-19)

I'm working on adding a repro. I think this should not be RBS though, since it's not a recent regression.

I change the access to limited.

### ch...@google.com (2025-08-20)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security Impact hotlist or the Severity field, and remove the ReleaseBlock hotlist.

### dx...@google.com (2025-08-22)

Project: angle/angle  

Branch:  main  

Author:  Geoff Lang [geofflang@chromium.org](mailto:geofflang@chromium.org)  

Link:    <https://chromium-review.googlesource.com/6838878>

Metal: Fix potential incorrect format used for texSubImage

---


Expand for full commit details
```
     
    TextureMtl caches the most recent format used for a texture 
    redefinition in mFormat. During subImage calls, this format may not be 
    the same as the image being uploaded to. 
     
    Pass ImageDefinitionMtl to these functions which reference mFormat, it 
    contains the format of the image being updated. 
     
    MacOS OpenGL is skipped because the driver generates errors in 
    glCompressedTexImage2D. 
     
    Bug: chromium:435683799 
    Change-Id: Idec6f71870c2d376cad3a5e3628b957009bdced9 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/6838878 
    Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org> 
    Reviewed-by: Quyen Le <lehoangquyen@chromium.org> 
    Commit-Queue: Geoff Lang <geofflang@chromium.org>

```

---

Files:

- M `src/libANGLE/renderer/metal/TextureMtl.h`
- M `src/libANGLE/renderer/metal/TextureMtl.mm`
- M `src/tests/angle_end2end_tests_expectations.txt`
- M `src/tests/gl_tests/CopyTexImageTest.cpp`

---

Hash: [86a8d11c82dde4fd1cf51a7f28a22d148d245339](https://chromiumdash.appspot.com/commit/86a8d11c82dde4fd1cf51a7f28a22d148d245339)  

Date: Mon Aug 11 20:45:39 2025


---

### dx...@google.com (2025-08-22)

Project: chromium/src  

Branch:  main  

Author:  chromium-autoroll [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com)  

Link:    <https://chromium-review.googlesource.com/6874835>

Roll ANGLE from e00691780c09 to 20dca0b943c2 (3 revisions)

---


Expand for full commit details
```
     
    https://chromium.googlesource.com/angle/angle.git/+log/e00691780c09..20dca0b943c2 
     
    2025-08-22 yuxinhu@google.com Add a new TInterfaceBlock class member to hint ANGLE default Uniform 
    2025-08-22 ynovikov@chromium.org Skip slow test on Mac Metal AMD 
    2025-08-22 geofflang@chromium.org Metal: Fix potential incorrect format used for texSubImage 
     
    If this roll has caused a breakage, revert this CL and stop the roller 
    using the controls here: 
    https://autoroll.skia.org/r/angle-chromium-autoroll 
    Please CC angle-team@google.com,ynovikov@google.com on the revert to ensure that a human 
    is aware of the problem. 
     
    To file a bug in ANGLE: https://bugs.chromium.org/p/angleproject/issues/entry 
    To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry 
     
    To report a problem with the AutoRoller itself, please file a bug: 
    https://issues.skia.org/issues/new?component=1389291&template=1850622 
     
    Documentation for the AutoRoller is here: 
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md 
     
    Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86 
    Bug: chromium:435683799 
    Tbr: ynovikov@google.com 
    Change-Id: Ic81f370c8da1f50dc76aa886b4afcb8cc518743e 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6874835 
    Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Cr-Commit-Position: refs/heads/main@{#1505220}

```

---

Files:

- M `DEPS`
- M `third_party/angle`

---

Hash: [26833113075abd6314e9b0d5429caf4c3a330e75](https://chromiumdash.appspot.com/commit/26833113075abd6314e9b0d5429caf4c3a330e75)  

Date: Fri Aug 22 18:25:53 2025


---

### kb...@chromium.org (2025-08-22)

Removing ReleaseBlock-Stable again because this is not a recent regression.

### ch...@google.com (2025-08-23)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M140. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [140].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### am...@chromium.org (2025-08-25)

While the GPU process is sandboxed on MacOS, this is still considered a high-severity (S1) issue given the potential for an overflow and OOB write.
I've also adjusted the found-in, as this is not a recent regression. Ordinarily this should be considered for backmerge to current Stable and Extended Stable, however, based on the timing of this fix landing it will not be included in this week's releases, which are the last planned releases of M139 Stable and M138 Extended Stable. Therefore, I'm not adjusting the merge review tags and this will only be reviewed for backmerge to M140 Stable.

### am...@chromium.org (2025-08-25)

<https://chromium-review.googlesource.com/c/angle/angle/+/6838878> approved for merge to M140; please merge this fix to branch 7339 ASAP so this fix can be included in tomorrow's Stable RC cut for release next week.

### dx...@google.com (2025-08-26)

Project: angle/angle  

Branch:  chromium/7339  

Author:  Geoff Lang [geofflang@chromium.org](mailto:geofflang@chromium.org)  

Link:    <https://chromium-review.googlesource.com/6885241>

M140: Metal: Fix potential incorrect format used for texSubImage

---


Expand for full commit details
```
     
    TextureMtl caches the most recent format used for a texture 
    redefinition in mFormat. During subImage calls, this format may not be 
    the same as the image being uploaded to. 
     
    Pass ImageDefinitionMtl to these functions which reference mFormat, it 
    contains the format of the image being updated. 
     
    MacOS OpenGL is skipped because the driver generates errors in 
    glCompressedTexImage2D. 
     
    Bug: chromium:435683799 
    Change-Id: Idec6f71870c2d376cad3a5e3628b957009bdced9 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/6838878 
    Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org> 
    Reviewed-by: Quyen Le <lehoangquyen@chromium.org> 
    Commit-Queue: Geoff Lang <geofflang@chromium.org> 
    (cherry picked from commit 86a8d11c82dde4fd1cf51a7f28a22d148d245339) 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/6885241 
    Reviewed-by: Corentin Wallez <cwallez@chromium.org>

```

---

Files:

- M `src/libANGLE/renderer/metal/TextureMtl.h`
- M `src/libANGLE/renderer/metal/TextureMtl.mm`
- M `src/tests/angle_end2end_tests_expectations.txt`
- M `src/tests/gl_tests/CopyTexImageTest.cpp`

---

Hash: [cbc4153da8d5796b0fbb3cf288e97bee19436191](https://chromiumdash.appspot.com/commit/cbc4153da8d5796b0fbb3cf288e97bee19436191)  

Date: Mon Aug 11 20:45:39 2025


---

### sp...@google.com (2025-08-28)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $10000.00 for this report.

Rationale for this decision:
report of memory corruption in a highly privileged process (GPU) 


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### ul...@gmail.com (2025-08-29)

Thanks that’s much appreciated. I will wait for bugcrowds email and I’ll let you know if I face any issues. I would also like to ask would this issue be given a CVE?  Thanks

### ch...@google.com (2025-11-29)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> report of memory corruption in a highly privileged process (GPU)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/435683799)*
