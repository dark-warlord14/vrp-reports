# Validating Decoder Stale PACK_ALIGNMENT causes GPU Heap OOB Write

| Field | Value |
|-------|-------|
| **Issue ID** | [505077859](https://issues.chromium.org/issues/505077859) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | Internals>GPU |
| **Platforms** | Android |
| **Reporter** | ci...@gmail.com |
| **Assignee** | va...@chromium.org |
| **Created** | 2026-04-21 |
| **Bounty** | $43,000.00 |

## Description

---

### Report description

Validating Decoder Stale PACK\_ALIGNMENT causes GPU Heap OOB Write

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

#### Which URL (or repository) have you found the vulnerability in?

<https://source.chromium.org/chromium/chromium/src/+/main:gpu/command_buffer/service/gles2_cmd_copy_texture_chromium.cc>

---

### The problem

#### Please describe the technical details of the vulnerability

`PrepareUnpackBuffer()` allocates a `width * height * 4` RGBA scratch buffer and calls `glReadPixels(..., GL_RGBA, GL_UNSIGNED_BYTE, ...)` on Android for the fallback readback path used by `GL_RGB / GL_FLOAT` uploads. The code assumes tightly packed rows, but attacker-controlled `GL_PACK_ALIGNMENT` is still honored because the validating decoder forwards pack state to native GL and Blink resets only unpack state before this path. With `PACK_ALIGNMENT = 8` and `width = 3`, each row is written with a 16-byte stride even though only 12 bytes per row are allocated.

The PoC sets `PACK_ALIGNMENT = 8` and uploads a `3 x 8192` source canvas with per-row markers via `texImage2D(GL_TEXTURE_2D, 0, GL_RGB9_E5, GL_RGB, GL_HALF_FLOAT, srcCanvas)`, reaching `PrepareUnpackBuffer()` on Android with the undersized buffer.

At those dimensions, the allocation is `98304` bytes, but rows are written at 16-byte stride. The last 2048 rows therefore go out of bounds, yielding 24576 bytes of attacker-controlled data written over roughly 32 KB beyond the allocation.

### Steps to Reproduce

Serve `poc.html` over HTTP and open it in Chrome on Android. No flags required.

#### Crash Evidence

1. Symbolized ASan stack trace (from Android content shell) attached as symbolized\_stack\_trace.txt
2. Chrome Stable tombstone is from com.android.chrome:privileged\_process\* (CrGpuMain), signal 11 SEGV\_ACCERR (write), with the fault in ReadPixels/glReadPixels
3. chrome://crashes `0e2b36268c1779c4` or `311f8eaf5e9c3abb`

### Proposed Fix

Either compute the allocation using the effective packed row stride, or temporarily force a safe `GL_PACK_ALIGNMENT` around the internal `glReadPixels` call and restore the previous value.

### Bisect

Introduced by commit `986a220965888` (`Add readback path for CopyTextureCHROMIUM`, 2017-03-30), which added the fallback readback path and its tight-row allocation assumption.

#### Impact analysis

- Web-accessible via WebGL2 on Android, no compromised renderer required.
- GPU process linear heap overwrite of attacker-controlled pixel data, 24576 bytes, deterministic geometry.
- On current Android phone builds, this reaches the GPU process without the Android GPU sandbox enabled by default.

---

### The cause

#### What version of Chrome have you found the security issue in?

147.0.7727.101 (Official Build) (64-bit)

#### Is the security issue related to a crash?

Yes, it is related to a crash.

#### Choose the type of vulnerability

Memory Corruption (in a non-sandboxed process)

#### How would you like to be publicly acknowledged for your report?

cinzinga

## Attachments

- [poc.html](attachments/poc.html) (text/html, 1.5 KB)
- [tombstone.txt](attachments/tombstone.txt) (text/plain, 487.6 KB)
- [symbolized_stack_trace.txt](attachments/symbolized_stack_trace.txt) (text/plain, 23.4 KB)
- [poc_crash_control.html](attachments/poc_crash_control.html) (text/html, 4.8 KB)
- [tombstone.txt](attachments/tombstone_75832310.txt) (text/plain, 514.0 KB)

## Timeline

### ci...@gmail.com (2026-04-22)

Attached PoC (poc\_crash\_control.html) achieves SIGBUS fault address 0x7b41414141 on Chrome Stable 147.0.7727.101 (Pixel 10 / Android 16) at 50-75% reliability. The 4 low bytes of the instruction pointer are fully attacker-controlled via WebGL pixel values. Full 8-byte control is achievable by switching to WIDTH=3.

chrome://crashes `699d0db09ec7f7629` or `7e014ee796d4d85e`

Tombstone attached as well.

### ch...@google.com (2026-04-23)

Setting milestone because of s0/s1 severity.

### dx...@google.com (2026-04-23)

Project: chromium/src  

Branch:  main  

Author:  Vasiliy Telezhnikov [vasilyt@chromium.org](mailto:vasilyt@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7789335>

Fix pack/unpack state during DoReadbackAndTexImage

---


Expand for full commit details
```
     
    Bug: 505077859 
    Change-Id: If5fd8a788710e0a7b0724fdfacfa309416a2b153 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7789335 
    Reviewed-by: Geoff Lang <geofflang@chromium.org> 
    Commit-Queue: Vasiliy Telezhnikov <vasilyt@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1619750}

```

---

Files:

- M `gpu/command_buffer/service/gles2_cmd_copy_texture_chromium.cc`

---

Hash: [ae8c96f69539e21694476ca6e3fad3f125698850](https://chromiumdash.appspot.com/commit/ae8c96f69539e21694476ca6e3fad3f125698850)  

Date: Thu Apr 23 20:58:48 2026


---

### sp...@google.com (2026-05-05)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $43000.00 for this report.

Rationale for this decision:
High quality with bisect. Memory corruption in a highly privileged process (e.g. GPU, network processes) 


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-05-20)

Requesting merge to M148 because latest trunk commit is in 149.

Security Merge Request:

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

### ch...@google.com (2026-05-20)

**M148** merge request created. **Please update [crbug/514925105](https://crbug.com/514925105) to have this merge reviewed.**

### dx...@google.com (2026-05-22)

Project: chromium/src  

Branch:  refs/branch-heads/7778  

Author:  Vasiliy Telezhnikov [vasilyt@chromium.org](mailto:vasilyt@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7869748>

[M148] Fix pack/unpack state during DoReadbackAndTexImage

---


Expand for full commit details
```
     
    Original change's description: 
    > Fix pack/unpack state during DoReadbackAndTexImage 
    > 
    > Bug: 505077859 
    > Change-Id: If5fd8a788710e0a7b0724fdfacfa309416a2b153 
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7789335 
    > Reviewed-by: Geoff Lang <geofflang@chromium.org> 
    > Commit-Queue: Vasiliy Telezhnikov <vasilyt@chromium.org> 
    > Cr-Commit-Position: refs/heads/main@{#1619750} 
     
    (cherry picked from commit ae8c96f69539e21694476ca6e3fad3f125698850) 
     
    Bug: 514925105,505077859 
    Change-Id: If5fd8a788710e0a7b0724fdfacfa309416a2b153 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7869748 
    Reviewed-by: Geoff Lang <geofflang@chromium.org> 
    Commit-Queue: Vasiliy Telezhnikov <vasilyt@chromium.org> 
    Reviewed-by: Vasiliy Telezhnikov <vasilyt@chromium.org> 
    Auto-Submit: chrome-cherry-picker@chops-service-accounts.iam.gserviceaccount.com <chrome-cherry-picker@chops-service-accounts.iam.gserviceaccount.com> 
    Cr-Commit-Position: refs/branch-heads/7778@{#3486} 
    Cr-Branched-From: 77f495ee216d4c3cc784d33658bad4778c0680ee-refs/heads/main@{#1610480}

```

---

Files:

- M `gpu/command_buffer/service/gles2_cmd_copy_texture_chromium.cc`

---

Hash: [5f0f0f57182373f61ac4ccba9fb9560751c3cb2e](https://chromiumdash.appspot.com/commit/5f0f0f57182373f61ac4ccba9fb9560751c3cb2e)  

Date: Fri May 22 14:46:30 2026


---

### ch...@google.com (2026-08-01)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/505077859)*
