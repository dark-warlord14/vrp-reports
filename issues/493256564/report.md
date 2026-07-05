# ANGLE Metal Stale mFormat Cache causes GPU OOB WRITE

| Field | Value |
|-------|-------|
| **Issue ID** | [493256564](https://issues.chromium.org/issues/493256564) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU>ANGLE |
| **Platforms** | Mac |
| **Reporter** | ci...@gmail.com |
| **Assignee** | ge...@chromium.org |
| **Created** | 2026-03-16 |
| **Bounty** | $77,000.00 |

## Description

---

### Report description

ANGLE Metal Stale mFormat Cache causes GPU OOB WRITE

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

#### Which URL (or repository) have you found the vulnerability in?

<https://source.chromium.org/chromium/chromium/src/+/main:third_party/angle/src/libANGLE/renderer/metal/TextureMtl.mm>

---

### The problem

#### Please describe the technical details of the vulnerability

Heap buffer overflow with attacker-controlled data in the GPU process via stale mFormat cache in ANGLE's Metal backend. Incomplete fix for chromium:435683799.

TextureMtl::redefineImage (TextureMtl.mm:2067) unconditionally sets mFormat for any texImage2D level, including out-of-range levels that do not trigger storage reallocation. Calling texImage2D at mip level 14 (TEXTURE\_MAX\_LEVEL=4) with format R8 poisons mFormat to R8 (1 byte/pixel) while the native Metal texture remains RGBA8 (4 bytes/pixel).

readPixelsImpl then sizes readPixelRowBuffer as Wx1 bytes. Metal's getBytes writes Wx4 bytes of actual RGBA8 data, overflowing 3xW bytes of attacker-controlled pixel data past the buffer.

### Steps to Reproduce

**Stable** (Chrome 145.0.7632.160, macOS x86\_64, Intel GPU, Metal backend):

```
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome file:///path/to/poc_write_crash.html

```

No flags required. Default configuration. The page auto-reloads and the GPU process crashes within 1-2 page loads.

chrome://crashes IDs:

- 897c7d4318e7beb6
- 63aee33eb14f4815

Terminal output from the crash:

```
*** Terminating app due to uncaught exception 'NSInvalidArgumentException', reason: '-[__NSCFNumber storageMode]: unrecognized selector sent to instance 0x4141414141414141'

```

The 0x4141414141414141 value is attacker-controlled pixel data from the overflow reaching ObjC dispatch. Full symbolized stack trace attached as crash\_trace.txt.

### Proposed Fix

Guard the mFormat cache update so it only applies to levels within native storage:

```
    // Cache last defined image format:
-   mFormat                      = mtlFormat;
+   if (imageWithinNativeStorageLevels)
+   {
+       mFormat                  = mtlFormat;
+   }

```

The variable imageWithinNativeStorageLevels is already computed at line 2043 and gates the storage reallocation at line 2052. It should also gate the format cache update.

### Bisect

The unconditional mFormat assignment was introduced in ANGLE commit fe26bae452 ("Metal backend implementation pt 2", 2019-10-10). Present since the Metal backend was first implemented, approximately Chrome 80.

The incomplete fix was commit 86a8d11c82 ("Metal: Fix potential incorrect format used for texSubImage", 2025-08-11), which patched setPerSliceSubImage and convertAndSetPerSliceSubImage but left line 2067 unfixed.

#### Impact analysis

- Web-accessible via WebGL2 (no compromised renderer required).
- GPU process heap overflow with attacker-controlled data (pixel values).
- macOS only (Metal backend, Intel GPUs).
- Seven affected code paths from the same stale mFormat root cause.

---

### The cause

#### What version of Chrome have you found the security issue in?

145.0.7632.160 Stable

#### Is the security issue related to a crash?

Yes, it is related to a crash.

#### Choose the type of vulnerability

Memory Corruption (in a sandboxed process)

#### How would you like to be publicly acknowledged for your report?

cinzinga

## Attachments

- [crash_trace.txt](attachments/crash_trace.txt) (text/plain, 3.5 KB)
- [poc_write_crash.html](attachments/poc_write_crash.html) (text/html, 3.9 KB)
- [poc_rip_v3.html](attachments/poc_rip_v3.html) (text/html, 9.9 KB)
- [poc_rce_v2.html](attachments/poc_rce_v2.html) (text/html, 5.5 KB)
- [poc_rce_v2.mov](attachments/poc_rce_v2.mov) (video/quicktime, 50.5 MB)
- deleted (application/octet-stream, 0 B)

## Timeline

### ci...@gmail.com (2026-03-16)

Additional evidence of exploitation capability:

RIP control: poc\_rip\_v3.html overwrites a callback function pointer with attacker pixel data. Crashpad dump shows the instruction pointer set to the attacker's chosen value: rip=0x0000414141414141.

chrome://crashes ID: `b39522c5395d7307`

Symbolized stack trace:

```
(lldb) bt
* thread #9, stop reason = EXC_BAD_ACCESS (code=1, address=0x414141414141)
  * frame #0: 0x0000414141414141
    frame #1: 0x000000012a805c63 Google Chrome Framework`base::sequence_manager::internal::WorkQueue::RemoveCancelledTasks(base::sequence_manager::internal::WorkQueue::RemoveCancelledTasksPolicy) + 195
    frame #2: 0x000000012e5caed0 Google Chrome Framework`non-virtual thunk to base::sequence_manager::internal::SequenceManagerImpl::SelectNextTask(base::LazyNow&, base::sequence_manager::internal::SequencedTaskSource::SelectTaskOption) + 432
    frame #3: 0x000000012e5d518e Google Chrome Framework`non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() + 766
    frame #4: 0x000000012e5e6eff Google Chrome Framework`base::MessagePumpKqueue::Run(base::MessagePump::Delegate*) + 1391
    frame #5: 0x000000012b8fb704 Google Chrome Framework`base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) + 212
    frame #6: 0x000000012b8fb032 Google Chrome Framework`base::RunLoop::Run(base::Location const&) + 338
    frame #7: 0x000000012c3b557c Google Chrome Framework`content::(anonymous namespace)::ChildIOThread::Run(base::RunLoop*) (.8bc93281f6dcb1070b114aed88069750) + 172
    frame #8: 0x000000012c8a1a43 Google Chrome Framework`base::Thread::ThreadMain() + 419
    frame #9: 0x000000012b4d8600 Google Chrome Framework`base::(anonymous namespace)::ThreadFunc(void*) + 256
(lldb) reg read
General Purpose Registers:
       rax = 0x0000414141414141
       rbx = 0x0000010c00076db0
[snipped for brevity]
       r15 = 0x0000010c002faf18
       rip = 0x0000414141414141
    rflags = 0x0000000000010246

```

### ci...@gmail.com (2026-03-17)

I was able to escalate this submission to RCE in Chrome's GPU process on macOS. This POC writes a command string + system() address into adjacent PartitionAlloc slots, then Chrome's internal callback dispatch calls `system("w>~/z")` through the corrupted object.

POC + video attached.

The batch script in the video relaunches Chrome with `--disable-gpu-sandbox` (for an observable POC) and auto-reloads the page until the overflow hits a live object (~5-10%). The system() address is a per-boot constant that needs updating after reboot. Video shows `~/z` being created with `w` output, proving arbitrary command execution from a WebGL page.

### dr...@chromium.org (2026-03-17)

[security triage] I don't have a device supporting Metal to test on, but this looks plausible enough. Assigning provisional severity and triaging akin to <https://crbug.com/435683799>.

### ch...@google.com (2026-03-18)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-03-18)

Setting Priority to P1 to match Severity s1. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### dx...@google.com (2026-03-24)

Project: angle/angle  

Branch:  main  

Author:  Geoff Lang [geofflang@chromium.org](mailto:geofflang@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7684363>

Metal: Remove TextureMtl::mFormat

---


Expand for full commit details
```
     
    TextureMtl::mFormat is supposed to represent the format of the native 
    storage but it was updated to the last format set on any mip level, even 
    if it is not in the native storage. This is extremely error prone, a lot 
    of the Metal texturing code relied on it being properly set. 
     
    Remove mFormat and query it from the native storage or the specific 
    image desc. 
     
    Bug: chromium:493256564 
    Change-Id: I629c009b34c7ef7ca5fa7a97f5845accf22b13b8 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7684363 
    Commit-Queue: Geoff Lang <geofflang@chromium.org> 
    Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>

```

---

Files:

- M `src/libANGLE/renderer/metal/TextureMtl.h`
- M `src/libANGLE/renderer/metal/TextureMtl.mm`
- M `src/tests/gl_tests/TextureTest.cpp`

---

Hash: [6d8b704e2a185c82430a339d70508742887a962f](https://chromiumdash.appspot.com/commit/6d8b704e2a185c82430a339d70508742887a962f)  

Date: Thu Mar 19 19:17:08 2026


---

### dx...@google.com (2026-03-25)

Project: chromium/src  

Branch:  main  

Author:  chromium-autoroll [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com)  

Link:    <https://chromium-review.googlesource.com/7699166>

Roll ANGLE from 08332c72dbba to 31ef14e93549 (3 revisions)

---


Expand for full commit details
```
     
    https://chromium.googlesource.com/angle/angle.git/+log/08332c72dbba..31ef14e93549 
     
    2026-03-24 a.annestrand@samsung.com OpenCL: Add BETA extension define for C/R 
    2026-03-24 g.tammana@samsung.com OpenCL: Make getSupportedFormats as const 
    2026-03-24 geofflang@chromium.org Metal: Remove TextureMtl::mFormat 
     
    If this roll has caused a breakage, revert this CL and stop the roller 
    using the controls here: 
    https://autoroll.skia.org/r/angle-chromium-autoroll 
    Please CC angle-team@google.com,yuxinhu@google.com on the revert to ensure that a human 
    is aware of the problem. 
     
    To file a bug in ANGLE: https://bugs.chromium.org/p/angleproject/issues/entry 
    To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry 
     
    To report a problem with the AutoRoller itself, please file a bug: 
    https://issues.skia.org/issues/new?component=1389291&template=1850622 
     
    Documentation for the AutoRoller is here: 
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md 
     
    Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:gpu-fyi-cq-mac-arm64;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86 
    Bug: chromium:493256564 
    Tbr: yuxinhu@google.com 
    Change-Id: I03cb599c3ced63bca9833747b55404d7e6e9ad2c 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7699166 
    Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Cr-Commit-Position: refs/heads/main@{#1604533}

```

---

Files:

- M `DEPS`
- M `third_party/angle`

---

Hash: [b8ff30ff67090453df6c69fe9068c2bf8affeb1c](https://chromiumdash.appspot.com/commit/b8ff30ff67090453df6c69fe9068c2bf8affeb1c)  

Date: Wed Mar 25 01:35:52 2026


---

### ch...@google.com (2026-03-25)

Security Merge Request:

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Requesting merge to stable (M146) because latest trunk commit (1604533) appears to be after stable branch point (1582197).

Merge review required: a commit with DEPS changes was detected.

Requesting merge to beta (M147) because latest trunk commit (1604533) appears to be after beta branch point (1596535).

Merge review required: a commit with DEPS changes was detected.

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### dr...@chromium.org (2026-03-27)

No crashes in Canary after 24 hours. Approved to merge to M146 and M147. Our release cut for M146 is Monday at 11am Pacific time, so please try to land by then.

### ch...@google.com (2026-03-31)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### sr...@chromium.org (2026-03-31)

We are cutting M147 RC today around 12pm PST, if your merge is critical to be incliuded in the RC build and is not able to make that cut off, please reach out to me , ( i can give some buffer for critical fixes that needs to included in RC) 

### dx...@google.com (2026-04-01)

2 changes merged

---

Project: angle/angle  

Branch:  chromium/7727  

Author:  Geoff Lang [geofflang@chromium.org](mailto:geofflang@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7717654>

M147: Metal: Remove TextureMtl::mFormat

---


Expand for full commit details
```
     
    TextureMtl::mFormat is supposed to represent the format of the native 
    storage but it was updated to the last format set on any mip level, even 
    if it is not in the native storage. This is extremely error prone, a lot 
    of the Metal texturing code relied on it being properly set. 
     
    Remove mFormat and query it from the native storage or the specific 
    image desc. 
     
    Bug: chromium:493256564 
    Change-Id: I629c009b34c7ef7ca5fa7a97f5845accf22b13b8 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7684363 
    Commit-Queue: Geoff Lang <geofflang@chromium.org> 
    Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org> 
    (cherry picked from commit 6d8b704e2a185c82430a339d70508742887a962f) 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7717654

```

---

Files:

- M `src/libANGLE/renderer/metal/TextureMtl.h`
- M `src/libANGLE/renderer/metal/TextureMtl.mm`
- M `src/tests/gl_tests/TextureTest.cpp`

---

Hash: [7cde4ef59f6c434ea78cc3ec43be699a9acbab49](https://chromiumdash.appspot.com/commit/7cde4ef59f6c434ea78cc3ec43be699a9acbab49)  

Date: Thu Mar 19 19:17:08 2026


---


---

Project: angle/angle  

Branch:  chromium/7680  

Author:  Geoff Lang [geofflang@chromium.org](mailto:geofflang@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7717653>

M146: Metal: Remove TextureMtl::mFormat

---


Expand for full commit details
```
     
    TextureMtl::mFormat is supposed to represent the format of the native 
    storage but it was updated to the last format set on any mip level, even 
    if it is not in the native storage. This is extremely error prone, a lot 
    of the Metal texturing code relied on it being properly set. 
     
    Remove mFormat and query it from the native storage or the specific 
    image desc. 
     
    Bug: chromium:493256564 
    Change-Id: I629c009b34c7ef7ca5fa7a97f5845accf22b13b8 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7684363 
    Commit-Queue: Geoff Lang <geofflang@chromium.org> 
    Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org> 
    (cherry picked from commit 6d8b704e2a185c82430a339d70508742887a962f) 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7717653

```

---

Files:

- M `src/libANGLE/renderer/metal/TextureMtl.h`
- M `src/libANGLE/renderer/metal/TextureMtl.mm`
- M `src/tests/gl_tests/TextureTest.cpp`

---

Hash: [d1100603964278cd89c5eb94707fbca242c788bf](https://chromiumdash.appspot.com/commit/d1100603964278cd89c5eb94707fbca242c788bf)  

Date: Thu Mar 19 19:17:08 2026


---

### aj...@google.com (2026-04-06)

VRP Category: gpu\_corrupt
Severity: S1
Summary: GPU process heap overflow RCE in ANGLE Metal backend.

Comment created using go/buganizer-mcp-server

### sp...@google.com (2026-05-14)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $70000.00 for this report.

Rationale for this decision:
High quality - Memory corruption in a highly privileged process (e.g. GPU, network processes) 


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ci...@gmail.com (2026-05-19)

Hi team, a few comments for the Security-VRP-Reassessment-Request:

1. First, thanks for the "arbitrary write"-tier award!
2. I believe [comment #3](https://issues.chromium.org/issues/493256564#comment3) demonstrates "RCE"-tier, but I have also attached a video showing all command line flags used to achieve RCE on 145.0.7632.117 (Official Build) (x86\_64). No non-compliant flags like single-process were used.
3. I believe this also qualifies for the renderer bonus as no compromised renderer is required per footnote [3]: "Amounts are based on the precondition of a compromised renderer, otherwise the equivalent renderer reward will also be added."
4. Was the bisect incorrect on this one?

Thanks

### sp...@google.com (2026-05-26)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $7000.00 for this report.

Rationale for this decision:
After reviewing your reassessment request, the panel has decided to award you an additional $7,000 for renderer bonus.


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-07-01)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/493256564)*
