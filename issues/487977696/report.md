# ANGLE D3D11 drawLineLoop Integer Overflow causes GPU OOB Write

| Field | Value |
|-------|-------|
| **Issue ID** | [487977696](https://issues.chromium.org/issues/487977696) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU>ANGLE |
| **Platforms** | Windows |
| **Reporter** | ci...@gmail.com |
| **Assignee** | se...@chromium.org |
| **Created** | 2026-02-26 |
| **Bounty** | $23,000.00 |

## Description

---

### Report description

ANGLE D3D11 drawLineLoop Integer Overflow causes GPU OOB Write

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

#### Which URL (or repository) have you found the vulnerability in?

<https://chromium.googlesource.com/angle/angle/+/refs/heads/main/src/libANGLE/renderer/d3d/d3d11/Renderer11.cpp>

---

### The problem

#### Please describe the technical details of the vulnerability

Renderer11::drawLineLoop has an integer overflow when computing the size of a mapped index buffer. The overflow check at line 2073 only validates the non-primitive-restart case (count+1 elements). When primitive restart is enabled, GetLineLoopIndices calls GetLineLoopWithRestartIndexCount which can return a significantly larger count due to index expansion at each restart boundary. The expanded output count multiplied by sizeof(GLuint) overflows unsigned int at line 2086-2087, truncating spaceNeeded to zero. The subsequent memcpy at line 2096 uses the full untruncated size, writing approximately 4GB of attacker-influenced data into a 16KB streaming index buffer.

### Affected Code

Renderer11.cpp, drawLineLoop():

```
// Line 2073-2078: overflow check only validates (count+1), not primitive restart expansion
bool indexCheck = static_cast<unsigned int>(count) + 1 >
                  (std::numeric_limits<unsigned int>::max() / sizeof(unsigned int));

// Line 2080-2081: GetLineLoopIndices expands indices beyond what the check allows
GetLineLoopIndices(indices, type, static_cast<GLuint>(count),
                   glState.isPrimitiveRestartEnabled(), &mScratchIndexDataBuffer);

// Line 2086-2087: unsigned int truncation (e.g. 1073741824 * 4 = 0x100000000 -> 0)
unsigned int spaceNeeded =
    static_cast<unsigned int>(sizeof(GLuint) * mScratchIndexDataBuffer.size());

// Line 2096-2097: memcpy uses full untruncated size, not spaceNeeded
memcpy(mappedMemory, &mScratchIndexDataBuffer[0],
       sizeof(GLuint) * mScratchIndexDataBuffer.size());

```
### Steps to Reproduce

1. Open Chrome on Windows (D3D11 is the default ANGLE backend, no flags needed)
2. Navigate to the attached poc\_lineloop\_d3d11.html
3. The page auto-fires: creates a WebGL2 context, allocates an element array buffer with 805306368 UNSIGNED\_BYTE indices in the pattern [0, 1, 0xFF] repeating (0xFF = primitive restart), then calls gl.drawElements(gl.LINE\_LOOP, 805306368, gl.UNSIGNED\_BYTE, 0)
4. GPU process crashes with access violation (WRITE of 4GB)

Note: the PoC allocates ~805MB for the element array buffer. Systems with less than ~2GB of available GPU process memory may fail the allocation before reaching the overflow.

Tested on:

- Chrome 145.0.7632.110 (stable, Windows 11) -- GPU process crash
- Chromium 146.0.7678.0 ASan (Windows 11, --in-process-gpu) -- heap-buffer-overflow WRITE of size 4294967296 at Renderer11.cpp:2096

With --in-process-gpu, the crash occurs in the browser process address space.

### ASan Output

```
==21376==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x12722fe50000 at pc 0x7ffcdf71b4fc bp 0x00ed077fdb70 sp 0x00ed077fdbb8
WRITE of size 4294967296 at 0x12722fe50000 thread T23
    #0 0x7ffcdf71b4fb  (clang_rt.asan_dynamic-x86_64.dll+0x18004b4fb)
    #1 0x7ffcdb3fe543 in rx::Renderer11::drawLineLoop Renderer11.cpp:2096:5
    #2 0x7ffcdb401b6d in rx::Renderer11::drawElements Renderer11.cpp:1970:16
    #3 0x7ffcdb3b0a49 in rx::Context11::drawElements Context11.cpp:361:12
    #4 0x7ffcdabbacfb in GL_DrawElements entry_points_gles_2_0_autogen.cpp:1862:22
    #5 0x7ffc7d294f7b in gl::RealGLApi::glDrawElementsFn gl_gl_api_implementation.cc:401:16
    #6 0x7ffc7dae946b in gpu::gles2::GLES2DecoderPassthroughImpl::DoDrawElements gles2_cmd_decoder_passthrough_doers.cc:1163:10
    #7 0x7ffc7db338ea in gpu::gles2::GLES2DecoderPassthroughImpl::HandleDrawElements gles2_cmd_decoder_passthrough_handlers.cc:138:10
    #8 0x7ffc7db51cbc in gpu::gles2::GLES2DecoderPassthroughImpl::DoCommandsImpl gles2_cmd_decoder_passthrough.cc:742:20
    #9 0x7ffc67ce5e7b in gpu::CommandBufferService::Flush command_buffer_service.cc:267:35
    #10 0x7ffc7dcfd071 in gpu::CommandBufferStub::OnAsyncFlush command_buffer_stub.cc:504:22

0x12722fe50000 is located 6144 bytes before 359576-byte region [0x12722fe51800,0x12722fea9498)

SUMMARY: AddressSanitizer: heap-buffer-overflow Renderer11.cpp:2096:5 in rx::Renderer11::drawLineLoop

```

Full unabridged ASan output is attached as asan\_output.txt.

### Fix

Replace the unsigned int spaceNeeded with size\_t, or validate mScratchIndexDataBuffer.size() after GetLineLoopIndices returns (accounting for primitive restart expansion) rather than only validating count+1 before the call:

```
size_t spaceNeeded = sizeof(GLuint) * mScratchIndexDataBuffer.size();
ANGLE_CHECK(GetImplAs<Context11>(context),
            spaceNeeded <= std::numeric_limits<unsigned int>::max(),
            "Line loop index buffer too large", GL_OUT_OF_MEMORY);

```

The same fix should be applied to drawTriangleFan (line 2168).

### Bisect

The vulnerable code was introduced in ANGLE commit 0d3537c224c7df5b90a2cf77678eb0987b6b7a30 ("D3D11: Implement ES3 primitive restart with line loops", 2015-11-06). This commit introduced `unsigned int spaceNeeded = static_cast<unsigned int>(sizeof(GLuint) * mScratchIndexDataBuffer.size())` (truncation), and added a memcpy using the full untruncated `sizeof(GLuint) * mScratchIndexDataBuffer.size()` — but did not update the pre-existing overflow check to account for the expanded index count.

#### Impact analysis

Heap buffer overflow in the GPU process, reachable from JavaScript via WebGL2 on any webpage. No flags or special configuration required. D3D11 is the default ANGLE backend on all Windows Chrome installations. The overflow writes approximately 4GB of partially attacker-controlled data (vertex index values from the element array buffer) into a 16KB D3D11 streaming index buffer. With --in-process-gpu the corruption occurs in the browser process address space.

---

### The cause

#### What version of Chrome have you found the security issue in?

145.0.7632.110 Stable

#### Is the security issue related to a crash?

Yes, it is related to a crash.

#### Choose the type of vulnerability

Memory Corruption (in a sandboxed process)

#### How would you like to be publicly acknowledged for your report?

cinzinga

## Attachments

- [poc_lineloop_d3d11.html](attachments/poc_lineloop_d3d11.html) (text/html, 4.7 KB)
- [asan_output.txt](attachments/asan_output.txt) (text/plain, 5.7 KB)

## Timeline

### li...@chromium.org (2026-02-26)

@sy...@chromium.org do you mind taking a look or routing as necessary?

### sy...@chromium.org (2026-02-26)

Rerouting to Geoff for d3d/

### ch...@google.com (2026-02-27)

Setting milestone because of s0/s1 severity.

### se...@chromium.org (2026-03-04)

I can repro the crash in Chrome/Win m145 Stable as well as a local m147 build at r1591978.

I attempted a C++ port of the poc (will clean up and upload). It didn't crash, but gave this error:

WARN: Debug.cpp:184 (gl::Debug::insertMessage): GL error: HIGH: Error: 0x00000505, in ....\src\libANGLE\renderer\d3d\d3d11\ResourceManager11.cpp, rx::ResourceManager11::allocate:491. Internal D3D11 error: HRESULT: 0x8007000E: Error allocating Buffer

An ASAN build gave no errors either, but it's clear that the computed spaceNeeded value overflows.

### se...@chromium.org (2026-03-06)

It's a bit surprising to me that this is exploitable, since it should be failing the memory allocation in the [call to reserveBufferSpace()](https://source.chromium.org/chromium/chromium/src/+/main:third_party/angle/src/libANGLE/renderer/d3d/d3d9/Renderer9.cpp;l=1582), which is wrapped in an `ANGLE_TRY()`.

In fact, this is what I see in a local build (with `dcheck_always_on=false`):

```
GpuProcessHost: The GPU process died due to out of memory.

```

But in a Canary build, I see:

```
GpuProcessHost: The GPU process crashed! Exit code: STATUS_ACCESS_VIOLATION.

```

Nevertheless, I've put up a patch here: <https://chromium-review.googlesource.com/c/angle/angle/+/7637780>

### dx...@google.com (2026-03-06)

Project: angle/angle  

Branch:  main  

Author:  Stephen White [senorblanco@chromium.org](mailto:senorblanco@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7637780>

D3D11: fix overflow in line loop and triangle fan

---


Expand for full commit details
```
     
    If an index buffer is created of element type less than 32bit (e.g., 
    GL_UNSIGNED_BYTE) and used in a line loop or triangle fan, D3D11 must 
    widen it to 32-bit. This can cause an overflow if the widened size in 
    bytes is greater than INT_MAX. The fix is to detect the overflow and 
    abort. 
     
    Bug: chromium:487977696 
    Change-Id: I57b1dcc9b3d968da88282164a5f92386500c6205 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7637780 
    Reviewed-by: Geoff Lang <geofflang@chromium.org> 
    Commit-Queue: Stephen White <senorblanco@chromium.org>

```

---

Files:

- M `src/libANGLE/renderer/d3d/d3d11/Renderer11.cpp`
- M `src/tests/gl_tests/LineLoopTest.cpp`

---

Hash: [4b7aace914924f634c4148c41e6fc87198867fa5](https://chromiumdash.appspot.com/commit/4b7aace914924f634c4148c41e6fc87198867fa5)  

Date: Wed Mar 4 20:44:30 2026


---

### dx...@google.com (2026-03-07)

Project: chromium/src  

Branch:  main  

Author:  chromium-autoroll [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com)  

Link:    <https://chromium-review.googlesource.com/7645129>

Roll ANGLE from 56c952c65e74 to 4b7aace91492 (3 revisions)

---


Expand for full commit details
```
     
    https://chromium.googlesource.com/angle/angle.git/+log/56c952c65e74..4b7aace91492 
     
    2026-03-06 senorblanco@chromium.org D3D11: fix overflow in line loop and triangle fan 
    2026-03-06 cclao@google.com Reland "Use arm_control_flow_integrity = "none" for AOSP autoroller" 
    2026-03-06 cclao@google.com Vulkan: Enable supportsTileMemoryHeap 
     
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
     
    Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:gpu-fyi-cq-mac-arm64;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86 
    Bug: chromium:487977696 
    Tbr: ynovikov@google.com 
    Change-Id: Ia6066fe8ce8621bce7fcc234e554613adeb72a57 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7645129 
    Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Cr-Commit-Position: refs/heads/main@{#1595832}

```

---

Files:

- M `DEPS`
- M `third_party/angle`

---

Hash: [92e674d7690cac16f439be11b9621316ed986034](https://chromiumdash.appspot.com/commit/92e674d7690cac16f439be11b9621316ed986034)  

Date: Sat Mar 7 01:43:12 2026


---

### ch...@google.com (2026-03-07)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### ch...@google.com (2026-03-10)

Security Merge Request Consideration: Requesting merge to extended stable (M144) because latest trunk commit (1595832) appears to be after extended stable branch point (1552494).
Security Merge Request Consideration: Requesting merge to stable (M145) because latest trunk commit (1595832) appears to be after stable branch point (1568190).
Security Merge Request Consideration: Requesting merge to beta (M146) because latest trunk commit (1595832) appears to be after beta branch point (1582197).
Security Merge Request - Manual Review: Merge review required: a commit with DEPS changes was detected.

Security Merge Request - Manual Review: Merge review required: a commit with DEPS changes was detected.

Security Merge Request - Manual Review: Merge review required: a commit with DEPS changes was detected.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [144, 145, 146].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### dr...@chromium.org (2026-03-11)

No crashes in Canary. Approving merge to M146. We don't plan any more M144 or M145 releases, so removing those labels.

### dx...@google.com (2026-03-11)

Project: angle/angle  

Branch:  chromium/7680  

Author:  Stephen White [senorblanco@chromium.org](mailto:senorblanco@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7657185>

M146: D3D11: fix overflow in line loop and triangle fan

---


Expand for full commit details
```
     
    If an index buffer is created of element type less than 32bit (e.g., 
    GL_UNSIGNED_BYTE) and used in a line loop or triangle fan, D3D11 must 
    widen it to 32-bit. This can cause an overflow if the widened size in 
    bytes is greater than INT_MAX. The fix is to detect the overflow and 
    abort. 
     
    Bug: chromium:487977696 
    Change-Id: I57b1dcc9b3d968da88282164a5f92386500c6205 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7637780 
    Reviewed-by: Geoff Lang <geofflang@chromium.org> 
    Commit-Queue: Stephen White <senorblanco@chromium.org> 
    (cherry picked from commit 4b7aace914924f634c4148c41e6fc87198867fa5) 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7657185

```

---

Files:

- M `src/libANGLE/renderer/d3d/d3d11/Renderer11.cpp`
- M `src/tests/gl_tests/LineLoopTest.cpp`

---

Hash: [e05753c6d05b17b23d514038957469c70b75475c](https://chromiumdash.appspot.com/commit/e05753c6d05b17b23d514038957469c70b75475c)  

Date: Wed Mar 4 20:44:30 2026


---

### sp...@google.com (2026-03-31)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $16000.00 for this report.

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

### ci...@gmail.com (2026-04-02)

Thanks for the "Memory corruption in a highly privileged process (e.g. GPU, network processes)" reward!

The Chrome scope states: "Memory Corruption / RCE in a highly privileged process (e.g. GPU or network processes) [3]"

Where footnote [3] indicates "Amounts are based on the precondition of a compromised renderer, otherwise the equivalent renderer reward will also be added."

This finding does not rely on a compromised renderer, since it is web-reachable I believe it qualifies for footnote [3]'s renderer reward.

### aj...@google.com (2026-04-21)

-> panel for reassessment see comment 14

### sp...@google.com (2026-05-05)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $7000.00 for this report.

Rationale for this decision:
Does not require a compromised renderer so bonus eligible. Sorry for missing this earlier.


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-06-16)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/487977696)*
