# ArrayBuffer OOR/W in glBufferData_Exec

| Field | Value |
|-------|-------|
| **Issue ID** | [40073848](https://issues.chromium.org/issues/40073848) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU>ANGLE |
| **Platforms** | Mac |
| **Reporter** | no...@ssd-disclosure.com |
| **Assignee** | ge...@chromium.org |
| **Created** | 2023-10-01 |
| **Bounty** | $10,000.00 |

## Description

**Steps to reproduce the problem:**  

Insufficient input validation for large size ArrayBuffer results in an Out of Bound (R/W) vulnerability in the `glBufferData_Exec` function of the GL driver.

**Problem Description:**

### ROOT CAUSE ANALYSIS

\* Due to various characteristics, it will not be possible to reproduce in ClusterFuzzer.  

\* Because it occurs within the GL Driver, accurate root cause analysis is impossible.  

\* Since this vulnerability is reproduced when a page is loaded more than three times, it may be related to GPU task scheduling.

```
angle::Result Buffer::bufferDataImpl(Context \*context,  
                                     BufferBinding target,  
                                     const void \*data,  
                                     GLsizeiptr size,  
                                     BufferUsage usage,  
                                     GLbitfield flags)  
{  
	...  
	  
    if (context && context->isRobustResourceInitEnabled() && !data && size > 0)  
    {  
        angle::MemoryBuffer \*scratchBuffer = nullptr;  
        ANGLE_CHECK_GL_ALLOC(  
            context, context->getZeroFilledBuffer(static_cast<size_t>(size), &scratchBuffer));  
        dataForImpl = scratchBuffer->data();  
    }  
  
	...  
}  

```

If the size of the ArrayBuffer is close to the maximum value of the `GLsizeiptr`(`signed long int`), an integer overflow occurs.

```
bool ScratchBuffer::getImpl(size_t requestedSize,  
                            MemoryBuffer \*\*memoryBufferOut,  
                            Optional<uint8_t> initValue)  
{  
    ...  
  
    if (mScratchMemory.size() < requestedSize)  
    {  
        if (!mScratchMemory.resize(requestedSize))  
        {  
            return false;  
        }  
        mResetCounter = mLifetime;  
        if (initValue.valid())  
        {  
            mScratchMemory.fill(initValue.value());  
        }  
    }  
      
    ...  
}  

```

The buffer is allocated by the size converted from the size in which the integer overflow has occurred to `size_t`.

```
angle::Result BufferGL::setData(const gl::Context \*context,  
                                gl::BufferBinding target,  
                                const void \*data,  
                                size_t size,  
                                gl::BufferUsage usage)  
{  
	...  
	ANGLE_GL_TRY(context, functions->bufferData(gl::ToGLenum(DestBufferOperationTarget), size, data,  
                                                ToGLenum(usage)));  
	...  
}  

```

When handling with data in `bufferData` functions of GL driver, the actual size of `data` and `size` parameters are different, resulting in out of bound r/w memory corruptions.

### RECOMMENDED PATCHES

```
--- a/third_party/angle/src/libANGLE/Buffer.cpp  
+++ b/third_party/angle/src/libANGLE/Buffer.cpp  
@@ -140,7 +140,7 @@  
         dataForImpl = scratchBuffer->data();  
     }  
   
-    if (mImpl->setDataWithUsageFlags(context, target, nullptr, dataForImpl, size, usage, flags) ==  
+    if (mImpl->setDataWithUsageFlags(context, target, nullptr, dataForImpl, static_cast<size_t>(size), usage, flags) ==  
         angle::Result::Stop)  
     {  
         // If setData fails, the buffer contents are undefined. Set a zero size to indicate that.  

```

When calling the `setData` function, if the `size` parameter is also converted to `size_t`, memory corruptions caused by different sizes from the `data` can be prevented.

---

### VERSION

\* Chrome Version: 116.0.5845.0 (Developer Build) (x86\_64)  

/ 118.0.5970.0 (Developer Build) (x86\_64)  

\* Operating System: macOS Monterey Version 12.6.8 (21G725)  

\* Hardware: Intel Core i5, 8GB RAM  

\* GPU: Intel Iris Graphics 540 1536 MB  

(\*\*I have attached the contents of the chrome://gpu page.\*\*)

### REPRODUCE CASE

You can simply reproduce by opening the attached `poc.html` in Chromium.

`./Chromium --no-sandbox poc.html`

### CREDIT

parkminchan, working for SSD Labs Korea.

**Additional Comments:**

\*\*Chrome version: \*\* 117.0.0.0 \*\*Channel: \*\* Stable

**OS:** Mac OS

## Attachments

- [readme.md](attachments/readme.md) (text/plain, 3.7 KB)
- [asan2.txt](attachments/asan2.txt) (text/plain, 17.2 KB)
- [asan1.txt](attachments/asan1.txt) (text/plain, 27.4 KB)
- [poc.html](attachments/poc.html) (text/plain, 1.3 KB)
- [GPU Internals.html](attachments/GPU Internals.html) (text/plain, 134.8 KB)

## Timeline

### [Deleted User] (2023-10-01)

[Empty comment from Monorail migration]

### an...@chromium.org (2023-10-01)

Thank you for the report!

Hi geofflang@chromium.org would you be able to help triage this bug? Thanks!

[Monorail components: Internals>GPU>ANGLE]

### an...@chromium.org (2023-10-01)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-01)

[Empty comment from Monorail migration]

### ad...@google.com (2023-10-01)

(I am a bot: this is an auto-cc on a security bug)

### [Deleted User] (2023-10-02)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-10-02)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sy...@chromium.org (2023-10-07)

Thank you for the report. Could you please clarify something? Where exactly is the integer overflow happening? Running your test on Linux, I see the buffer is being allocated with a size of 1933311996 (0x733BFFFC). The scratch memory in ScratchBuffer::getImpl is also being allocated with the same amount of memory. In both the allocation and usage path, it doesn't look like any size is being used higher than the one originally provided by the test (i.e. 1933311996). Could you please point me to where the overflow itself happens?

### ct...@chromium.org (2023-10-16)

Marking as Needs-Feedback. Reporter: could you provide more details as requested in https://crbug.com/chromium/1488269#c8 when you have a chance?

### no...@ssd-disclosure.com (2023-10-19)

First of all, I think I mis-analyzed the code when I did the Root Cause Analysis.

I've re-examined that my ASAN log also allocates as much space as 193331996, and it having crash reading 1933311996 (I think something else has happened, rather than something about integer overflow)The exact problem occurs within the `glBufferData_Exec` function, which is out of the chromium codebase and appears to be hard to do the exact RCA.


### sy...@chromium.org (2023-10-30)

Thank you. This is likely a mac GL driver bug.

### ad...@google.com (2023-11-13)

syouseffi@ geofflang@ hello, could you tell us your normal procedure when driver bugs are discovered? Would you report this upstream to Apple?

Even if the root cause is in Apple code, this is still exploitable via webgl content, so we still need to figure out a way to fix it - either by persuading the driver vendor to fix it or by somehow filtering out the offending code. Let us know your thoughts.

FWIW I tried to reproduce this on my Mac. OS X 14.1, Chromium M121(specifically revision eb5e82f8999a8201c55417df48f78c391ed8464e) with Intel UHD Graphics 630 1536 MB. It didn't reproduce, perhaps unsurprisingly.

### ge...@chromium.org (2023-11-13)

Normally we would try to work around this kind of issue in ANGLE or Chrome. In this case limiting the maximum buffer size would probably do it.

Apple doesn't fix any issues with the Intel drivers anymore unless it's a kernel-level security issue. We would file a radar if I expected it could be fixed.

### ge...@chromium.org (2023-11-13)

My mistake, the buffer size is 1.9GB which is reasonable (barely) for a GPU allocation.

### [Deleted User] (2023-11-14)

syoussefi: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sy...@chromium.org (2023-11-14)

@noamr, do you still claim that this fixes it?

```
-    if (mImpl->setDataWithUsageFlags(context, target, nullptr, dataForImpl, size, usage, flags) ==
+    if (mImpl->setDataWithUsageFlags(context, target, nullptr, dataForImpl, static_cast<size_t>(size), usage, flags) ==
         angle::Result::Stop)
     {
         // If setData fails, the buffer contents are undefined. Set a zero size to indicate that.
```

BufferImpl::setDataWithUsageFlags already takes the size parameter as `size_t`, it looks like that cast should be a noop.

### no...@ssd-disclosure.com (2023-11-26)

Minchin Park (answers - as he found this vulnerability, he works as part of our group at SSD Labs)
===
First of all, if I simply answer the question I got from you (Google), it's 'No'.As you say, the parameter is received as 'size_t' inside the function, so casting does not do anything else when calling the function.
===

### sy...@chromium.org (2023-11-27)

Thank you, is there any information relevant in the rest of the clipped message? As it stands, it's not clear what we could do about this driver bug.

### no...@ssd-disclosure.com (2023-11-29)

Please give credit to:
***Minchan Park***


### [Deleted User] (2023-12-06)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-11)

syoussefi: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-10)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-11)

[Empty comment from Monorail migration]

### sy...@chromium.org (2024-01-15)

As I mentioned in https://crbug.com/chromium/1488269#c18, it's not clear to me what could be done about this bug.

@Ken, this is a mac/Intel/GL bug in the driver with no clear workaround. Any ideas? Would these devices be switched to metal anytime soon?

### kb...@chromium.org (2024-01-24)

Sorry for the delay replying.

This machine (MacBookPro13,1 with Intel(R) Iris(TM) Graphics 540) will be switched to the Metal backend, hopefully soon, but this is the oldest hardware that will support ANGLE's Metal backend and it seems there are significant problems even with the Metal driver on it.

Agree with Geoff's suggestion in https://crbug.com/chromium/1488269#c13 above to limit the max buffer size on this configuration. Can we add a GL workaround in include/platform/gl_features.json and associated files which activates only on Mac / Intel, only for older GPUs, and forbids the buffer size from being larger than e.g. 1.5 GB (generating INVALID_OPERATION upon attempts to allocate a larger one)?

I don't know how we'd identify older GPUs exactly. Geoff and I discussed identifying Macs by machine model - see http://go/metal-hardware-class-breakdown - perhaps we could activate this workaround on MacBookPro14,* and lower (which are older Intel Iris Plus Graphics series), MacBookAir7,* and lower (pre-Intel UHD), MacMini7,* and lower (pre-Intel UHD), and iMac18,* and lower (pre-2018). Mac Pros used AMD GPUs and hopefully wouldn't need this workaround.

CC'ing a couple of Apple colleagues as FYI.


### sy...@chromium.org (2024-01-25)

Ok I think I can safely say I'm not the best person to handle this.

### is...@google.com (2024-01-25)

This issue was migrated from crbug.com/chromium/1488269?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-02-21)

Thank you for providing more feedback. Adding the requester to the CC list.

### ri...@google.com (2024-10-14)

[secondary shepherd] [kbr@chromium.org](mailto:kbr@chromium.org), would you be able to add the max buffer size limit in [comment#28](https://issues.chromium.org/issues/40073848#comment28), or if not, could you help find an appropriate owner?

### kb...@chromium.org (2024-10-14)

Geoff is the appropriate owner. In the time since this bug was filed, Chrome has shipped ANGLE's Metal backend on Intel Macs, significantly reducing the exposure even of this bug in Apple's OpenGL driver. Please reach out to Geoff to try to schedule the addition of a workaround to ANGLE's OpenGL backend on macOS.

### pe...@google.com (2024-10-29)

geofflang: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### pe...@google.com (2024-11-13)

geofflang: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### dx...@google.com (2026-02-19)

Project: angle/angle  

Branch:  main  

Author:  Geoff Lang [geofflang@chromium.org](mailto:geofflang@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7589937>

GL: Limit buffer size to 1gb on Intel Macs.

---


Expand for full commit details
```
     
    These drivers cannot handle allocations this large so add a limitation 
    which generates GL_INVALID_OPERATION. 
     
    Bug: chromium:40073848 
    Change-Id: Ibeffb7507e72e4fb5e2a23ed9b873c726c351361 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7589937 
    Commit-Queue: Shahbaz Youssefi <syoussefi@chromium.org> 
    Auto-Submit: Geoff Lang <geofflang@chromium.org> 
    Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>

```

---

Files:

- M `include/platform/autogen/FeaturesGL_autogen.h`
- M `include/platform/gl_features.json`
- M `src/libANGLE/Caps.h`
- M `src/libANGLE/ErrorStrings.h`
- M `src/libANGLE/renderer/gl/renderergl_utils.cpp`
- M `src/libANGLE/validationES2.cpp`
- M `src/libANGLE/validationES3.cpp`
- M `src/libANGLE/validationESEXT.cpp`
- M `src/tests/gl_tests/BufferDataTest.cpp`
- M `util/autogen/angle_features_autogen.cpp`
- M `util/autogen/angle_features_autogen.h`

---

Hash: [42ae4b5eee733709f37b9f7a50d227a6bc90af70](https://chromiumdash.appspot.com/commit/42ae4b5eee733709f37b9f7a50d227a6bc90af70)  

Date: Wed Feb 18 17:09:39 2026


---

### dx...@google.com (2026-02-19)

Project: chromium/src  

Branch:  main  

Author:  chromium-autoroll [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com)  

Link:    <https://chromium-review.googlesource.com/7592094>

Roll ANGLE from bfeb0d55d895 to 42ae4b5eee73 (2 revisions)

---


Expand for full commit details
```
     
    https://chromium.googlesource.com/angle/angle.git/+log/bfeb0d55d895..42ae4b5eee73 
     
    2026-02-19 geofflang@chromium.org GL: Limit buffer size to 1gb on Intel Macs. 
    2026-02-19 bsheedy@chromium.org Replace linux-intel 
     
    If this roll has caused a breakage, revert this CL and stop the roller 
    using the controls here: 
    https://autoroll.skia.org/r/angle-chromium-autoroll 
    Please CC angle-team@google.com,syoussefi@google.com on the revert to ensure that a human 
    is aware of the problem. 
     
    To file a bug in ANGLE: https://bugs.chromium.org/p/angleproject/issues/entry 
    To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry 
     
    To report a problem with the AutoRoller itself, please file a bug: 
    https://issues.skia.org/issues/new?component=1389291&template=1850622 
     
    Documentation for the AutoRoller is here: 
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md 
     
    Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:gpu-fyi-cq-mac-arm64;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86 
    Bug: chromium:40073848 
    Tbr: syoussefi@google.com 
    Change-Id: I46f95dc969114c20e1d9b0ba325a3110845c3b71 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7592094 
    Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Cr-Commit-Position: refs/heads/main@{#1586887}

```

---

Files:

- M `DEPS`
- M `third_party/angle`

---

Hash: [f51a685e768b632262beaf8bd95387fffe096655](https://chromiumdash.appspot.com/commit/f51a685e768b632262beaf8bd95387fffe096655)  

Date: Thu Feb 19 05:29:25 2026


---

### dn...@google.com (2026-02-23)

Reading the patch, this is now fixed even with an OpenGL backend.

### ch...@google.com (2026-02-23)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### sp...@google.com (2026-06-04)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $10000.00 for this report.

Rationale for this decision:
Baseline. Memory Corruption / RCE in a highly privileged process (e.g. GPU or network).


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-06-09)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40073848)*
