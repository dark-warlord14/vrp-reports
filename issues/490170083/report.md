# ANGLE BlitGL copySubTextureCPUReadback Controlled Heap Overflow via Unsynchronized PACK_ROW_LENGTH

| Field | Value |
|-------|-------|
| **Issue ID** | [490170083](https://issues.chromium.org/issues/490170083) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | Internals>GPU>ANGLE |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ci...@gmail.com |
| **Assignee** | ge...@chromium.org |
| **Created** | 2026-03-05 |
| **Bounty** | $90,000.00 |

## Description

---

### Report description

ANGLE BlitGL copySubTextureCPUReadback Controlled Heap Overflow via Unsynchronized PACK\_ROW\_LENGTH

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

#### Which URL (or repository) have you found the vulnerability in?

<https://source.chromium.org/chromium/chromium/src/+/main:third_party/angle/src/libANGLE/renderer/gl/BlitGL.cpp>

---

### The problem

#### Please describe the technical details of the vulnerability

`kTexImageDirtyBits` in ANGLE's `Context.cpp` omits `DIRTY_BIT_PACK_STATE` and `DIRTY_BIT_PACK_BUFFER_BINDING`. When `copySubTextureCPUReadback` (BlitGL.cpp) calls `glReadPixels` on a scratch heap buffer, it inherits stale `GL_PACK_ROW_LENGTH` from native GL, causing a controlled heap overflow. Triggered from JavaScript via WebGL2, no compromised renderer required.

Data written is attacker-controlled via source WebGL canvas pixel data (RGBA bytes rendered by attacker). Write offset is attacker-controlled via `PACK_ROW_LENGTH` which sets row stride. Write size is `width * 4` bytes per row, tunable via source canvas dimensions.

Tight primitive: width=2, height=2, `PACK_ROW_LENGTH=N` gives exactly 8 controlled bytes at offset `N*4` past the scratch buffer.

Attack Chain:

1. Set `PACK_ROW_LENGTH=N`. Forwarded to ANGLE via command buffer (`gles2_implementation.cc` uses `break`, not `return`, for this param).
2. Bind PBO, then readPixels. This bypasses `ScopedPackStateRowLengthReset` (disabled when PBO bound, `passthrough_doers.cc:2661`). ANGLE syncs `PACK_ROW_LENGTH=N` to native GL.
3. Unbind and delete PBO. `StateManagerGL::deleteBuffer` unbinds PBO in native GL. `PACK_ROW_LENGTH` persists.
4. Call `texImage2D(SRGB8_ALPHA8, webglCanvas)`. SRGB dest forces CPU readback path (`TextureGL.cpp:1113,1133` skip fast paths when `destSRGB=true`). WebGL canvas source is texture-backed, routes through `CopySubTextureCHROMIUM` to `copySubTextureCPUReadback`.
5. Overflow. `BlitGL.cpp:859` calls native `glReadPixels` with stale `PACK_ROW_LENGTH=N`, stride `N*4` bytes per row into a `width*height*4*2` byte scratch buffer.

### Affected Code

```
// third_party/angle/src/libANGLE/Context.cpp:86-89
constexpr state::DirtyBits kTexImageDirtyBits{
    state::DIRTY_BIT_UNPACK_STATE,
    state::DIRTY_BIT_UNPACK_BUFFER_BINDING,
    // Missing: DIRTY_BIT_PACK_STATE, DIRTY_BIT_PACK_BUFFER_BINDING
};

```

`syncStateForTexImage()` uses `kTexImageDirtyBits`. It syncs unpack state but never pack state. Compare with `kReadPixelsDirtyBits` (line 94) which correctly includes `DIRTY_BIT_PACK_STATE`.

When `copySubTextureCPUReadback` (BlitGL.cpp:859) calls `mFunctions->readPixels()` into a scratch buffer, it reads with whatever `PACK_ROW_LENGTH` was last synced to native GL by a prior `readPixels` call. The scratch buffer is sized for `width * height * 4 * 2` (32KB for 64x64), but native GL writes with stride `PACK_ROW_LENGTH * 4`, overflowing the buffer.

### Steps to Reproduce

1. Build Chromium with ASan (`is_asan = true`) or use an ASan-instrumented build.
2. Save the attached `poc.html`.
3. Run:

```
./chrome --no-sandbox --ignore-gpu-blocklist --single-process poc.html

```

4. ASan reports `heap-buffer-overflow` (or `heap-use-after-free`) on the `Chrome_InProcGp` thread at `BlitGL::copySubTextureCPUReadback`.

No GPU hardware required. Reproduces on stock Linux VMs with Mesa llvmpipe.

### ASan Output

PACK\_ROW\_LENGTH=4096. Full trace in asan\_out.txt:

```
==175475==ERROR: AddressSanitizer: heap-use-after-free on address 0x75876315dab0
WRITE of size 8 at 0x75876315dab0 thread T17 (Chrome_InProcGp)
    #0 memcpy
    #1-#4 libgallium (Mesa readpixels)
    #5 rx::BlitGL::copySubTextureCPUReadback BlitGL.cpp:859
    #6 rx::TextureGL::copySubTextureHelper TextureGL.cpp:1150
    ...
    #12 GLES2DecoderPassthroughImpl::DoCopySubTextureCHROMIUM passthrough_doers.cc:4501

0x75876315dab0 is located 16 bytes inside of 29-byte region [0x75876315daa0,0x75876315dabd)
freed by thread T17 (Chrome_InProcGp) here:
    #0 operator delete
    #1 llvm::MCContext::reset()

MiraclePtr Status: NOT PROTECTED

```

Controlled bytes written at controlled offset past the scratch buffer. Landed in a freed LLVM MCContext region, likely reclaimable via heap spray.

### Fix

Add pack state dirty bits to `kTexImageDirtyBits`:

```
constexpr state::DirtyBits kTexImageDirtyBits{
    state::DIRTY_BIT_UNPACK_STATE,
    state::DIRTY_BIT_UNPACK_BUFFER_BINDING,
    state::DIRTY_BIT_PACK_STATE,            // ADD
    state::DIRTY_BIT_PACK_BUFFER_BINDING,   // ADD
};

```

Or reset pack state in `copySubTextureCPUReadback` before `readPixels` (BlitGL.cpp:859), similar to how it already resets pack state after (line 873-876).

### Bisect

Introduced in ANGLE commit <https://chromium.googlesource.com/angle/angle/+/aadc8f376a> ("Implement the CPU fallback for CopyTextureCHROMIUM on OpenGL", 2017-08-11). This commit added `copySubTextureCPUReadback` with `readPixels` before `setPixelPackState`. Pack state was never reset before the read, from day one. Rolled into Chromium via <https://chromium.googlesource.com/chromium/src/+/ed7971c95c05a> (2017-08-30), shipping in Chrome 63 (December 2017).

The PBO bypass path that disables `ScopedPackStateRowLengthReset` when a PBO is bound was added in <https://chromium.googlesource.com/chromium/src/+/5899dbdc3d96d> ("Implement async ReadPixels for the passthrough command decoder", 2017-10-05), making the stale state reachable.

#### Impact analysis

Heap overflow in the GPU process from unprivileged WebGL2 JavaScript, no compromised renderer required. The attacker controls the write data (source canvas pixels), write offset (PACK\_ROW\_LENGTH), and write size (source canvas width). The overflow target is a malloc'd scratch buffer with no MiraclePtr protection. On Linux, the GPU process is sandboxed but not as tightly as the renderer.

---

### The cause

#### What version of Chrome have you found the security issue in?

147.0.7703.0 (Developer Build) (64-bit)

#### Is the security issue related to a crash?

Yes, it is related to a crash.

#### Choose the type of vulnerability

Memory Corruption (in a sandboxed process)

#### How would you like to be publicly acknowledged for your report?

cinzinga

## Attachments

- [poc.html](attachments/poc.html) (text/html, 4.8 KB)
- [asan_out.txt](attachments/asan_out.txt) (text/plain, 27.7 KB)
- [crash_control.html](attachments/crash_control.html) (text/html, 4.7 KB)

## Timeline

### ci...@gmail.com (2026-03-05)

The report includes `--no-sandbox` in the steps to reproduce, but that flag is not needed for the ASan build.

### ci...@gmail.com (2026-03-06)

Appending an updated PoC with proof of controlled write to controlled offset on Chrome Stable.

- 145.0.7632.159 (Official Build) (64-bit), Ubuntu 24.04.4 LTS Kernel 6.17.0-14-generic (x86\_64), Mesa 25.2.8
  (llvmpipe software renderer). No GPU hardware required.

```
google-chrome --ignore-gpu-blocklist --single-process ./crash_control.html

```

Segmentation fault (core dumped) — highly reliable in my testing.

GDB analysis of core dump shows attacker-controlled pixel data (0x41414141 0x42424242) in RBX, RDI, and on the stack.
The crash dereferences RDI (mov 0x8(%rdi),%rdi) using the attacker's payload as a pointer:

```
Core was generated by `/opt/google/chrome/chrome --ignore-gpu-blocklist --single-process file:///home/'.
Program terminated with signal SIGSEGV, Segmentation fault.
#0  0x00005e688feafe39 in ?? ()
[Current thread is 1 (Thread 0x78f803694680 (LWP 53670))]
(gdb) info registers
rax            0xc                 12
rbx            0x4242424241414141  4774451407296217409
rcx            0x4                 4
rdx            0x2                 2
rsi            0x1                 1
rdi            0x4242424241414141  4774451407296217409
rbp            0x7fffcee348f0      0x7fffcee348f0
rsp            0x7fffcee348e0      0x7fffcee348e0
r8             0xfffe              65534
r9             0x5e689b045a40      103803370363456
r10            0x196402578c20      27917326715936
r11            0x1                 1
r12            0x196401b8cb48      27917316311880
r13            0x19640209ce60      27917321621088
r14            0x19640209cc80      27917321620608
r15            0x1964003a7620      27917291255328
rip            0x5e688feafe39      0x5e688feafe39
eflags         0x10206             [ PF IF RF ]
cs             0x33                51
ss             0x2b                43
ds             0x0                 0
es             0x0                 0
fs             0x0                 0
gs             0x0                 0
fs_base        0x78f803694680      133006604453504
gs_base        0x0                 0
(gdb) x/5i $rip
=> 0x5e688feafe39:	mov    0x8(%rdi),%rdi
   0x5e688feafe3d:	test   %rdi,%rdi
   0x5e688feafe40:	jne    0x5e688feafe51
   0x5e688feafe42:	mov    (%rbx),%rbx
   0x5e688feafe45:	test   %rbx,%rbx
(gdb) bt
#0  0x00005e688feafe39 in ?? ()
#1  0x000000000000000c in ?? ()
#2  0x4242424241414141 in ?? ()
#3  0x00007fffcee34970 in ?? ()
#4  0x00005e688e2ea8e3 in ?? ()
#5  0x00007fffcee34a60 in ?? ()
#6  0x0000196401d62400 in ?? ()
#7  0x000019640209cdc0 in ?? ()
#8  0x00005e688df46575 in ?? ()
#9  0x0000000000000018 in ?? ()
#10 0x00007fffcee34a60 in ?? ()
#11 0x00003b3e80fcfe20 in ?? ()
#12 0x00005e689b045a40 in __bss_start ()
#13 0x0000196401dc4140 in ?? ()
#14 0x0000196401d623f0 in ?? ()
#15 0x00005e689b03a8d8 in __bss_start ()
#16 0x7fffffffffffffff in ?? ()
#17 0x0000196401d62400 in ?? ()
#18 0x00001964015f15e0 in ?? ()
#19 0x00007fffcee34990 in ?? ()
#20 0x00005e689371d5b9 in ?? ()
#21 0x0000000000000002 in ?? ()
#22 0x0000000000000001 in ?? ()
#23 0x00007fffcee349c0 in ?? ()
#24 0x00005e68936de389 in ?? ()
#25 0x00001964015f15e0 in ?? ()
#26 0x0000196401d62530 in ?? ()
#27 0x0000000000000000 in ?? ()
(gdb) 

```

The write lands at scratch\_buffer\_base + PACK\_ROW\_LENGTH × 4. The attacker sets PACK\_ROW\_LENGTH to any value N in JavaScript via gl.pixelStorei(), selecting which heap object to corrupt. The value written is attacker-controlled pixel data (the 0x4242424241414141 in RBX/RDI above). Both address and value are attacker-controlled, resulting in an arbitrary write primitive.

### cl...@appspot.gserviceaccount.com (2026-03-06)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5790258482315264.

### ct...@google.com (2026-03-06)

[security shepherd]

Uploaded the improved POC to clusterfuzz to see if it can repro. If it doesn't I'll also test the original POC.

Recent similar (?) bugs: [Issue 489116591](https://issues.chromium.org/issues/489116591) and [Issue 489579953](https://issues.chromium.org/issues/489579953), but they appear to go through a different code path.

### ci...@gmail.com (2026-03-07)

Looks like ClusterFuzz ran with `--use-angle=swiftshader`. The bug is in ANGLE's GL backend (BlitGL::copySubTextureCPUReadback at BlitGL.cpp:859), which is not active under SwiftShader.

Running with `--use-angle=gl` should work. Although Linux generally defaults to GL backend, so no special flags should be needed.

### cl...@appspot.gserviceaccount.com (2026-03-09)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4563905934196736.

### ci...@gmail.com (2026-03-09)

ClusterFuzz output shows "WebGL2 blocklisted" and "error: WebGL2 not available", meaning the POC did not run.

Also, both  `--use-angle=swiftshader` and `--use-angle=gl` are passed in that run, just GL is needed.

I recommend running with `--ignore-gpu-blocklist` or a bot that supports WebGL2.

### cl...@appspot.gserviceaccount.com (2026-03-10)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5364750099611648.

### jd...@chromium.org (2026-03-10)

Clusterfuzz thinks this is sev-critical. I think that might be wrong, but conservatively deferring to it for now.

### 24...@project.gserviceaccount.com (2026-03-11)

Detailed Report: https://clusterfuzz.com/testcase?key=5364750099611648

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-buffer-overflow WRITE {*}
Crash Address: 0x7ab2e61a7800
Crash State:
  ___interceptor_memcpy
  swrast_dri.so
  
Sanitizer: address (ASAN)

Recommended Security Severity: Critical

Crash Revision: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&revision=1597173

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5364750099611648

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary.

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


A recommended severity was added to this bug. Please change the severity if it is inaccurate.

### ci...@gmail.com (2026-03-11)

Thanks for the triage, security shepherd. I am not sure how ClusterFuzz determines its severity, but I can highlight the security context here:

1. Web-reachable, no compromised renderer required.
2. Controlled write value: attacker-chosen source canvas pixels (arbitrary RGBA bytes)
3. Controlled write offset: base address + (PACK\_ROW\_LENGTH × 4), where PACK\_ROW\_LENGTH is any JS-settable integer (arbitrary heap offset selection)
4. GDB confirms attacker pixel bytes land in RDI and get dereferenced as a pointer (crash at `mov 0x8(%rdi),%rdi`)
5. ClusterFuzz confirms `--single-process` was not needed

### ch...@google.com (2026-03-11)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-03-11)

Setting Priority to P0 to match Severity s0. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### dx...@google.com (2026-03-30)

Project: angle/angle  

Branch:  main  

Author:  Geoff Lang [geofflang@chromium.org](mailto:geofflang@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7708753>

GL: Fix pack state for BlitGL::copySubTextureCPUReadback

---


Expand for full commit details
```
     
    copySubTextureCPUReadback does both ReadPixels and TexImage calls and 
    needs to make sure the client's pack states are not used. It does this 
    but in the wrong order causing an invalid pack state to be used for the 
    ReadPixels call. 
     
    Bug: chromium:490170083 
    Change-Id: I93dcabf52edd6e4e08f999aaa0d96d1fc325211a 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7708753 
    Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org> 
    Commit-Queue: Geoff Lang <geofflang@chromium.org>

```

---

Files:

- M `src/libANGLE/renderer/gl/BlitGL.cpp`
- M `src/tests/capture_replay_tests/capture_replay_expectations.txt`
- M `src/tests/gl_tests/CopyTextureTest.cpp`

---

Hash: [b149a5c62d76ab536929afc5bba2b2774da46102](https://chromiumdash.appspot.com/commit/b149a5c62d76ab536929afc5bba2b2774da46102)  

Date: Fri Mar 27 20:13:31 2026


---

### dx...@google.com (2026-03-30)

Project: chromium/src  

Branch:  main  

Author:  chromium-autoroll [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com)  

Link:    <https://chromium-review.googlesource.com/7710948>

Roll ANGLE from 482561f7b8b0 to b149a5c62d76 (2 revisions)

---


Expand for full commit details
```
     
    https://chromium.googlesource.com/angle/angle.git/+log/482561f7b8b0..b149a5c62d76 
     
    2026-03-30 geofflang@chromium.org GL: Fix pack state for BlitGL::copySubTextureCPUReadback 
    2026-03-30 syoussefi@chromium.org Manual roll vulkan-deps from 008b485ddfe9 to 547e0f27522b (14 revisions) 
     
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
    Bug: chromium:490170083 
    Tbr: syoussefi@google.com 
    Change-Id: I3ec3d06a84c7d8ac4173ac50b82189a06eb42a15 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7710948 
    Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Cr-Commit-Position: refs/heads/main@{#1607327}

```

---

Files:

- M `DEPS`
- M `third_party/angle`

---

Hash: [83bf019fd3486d97e5907e1991d61c83a6743d70](https://chromiumdash.appspot.com/commit/83bf019fd3486d97e5907e1991d61c83a6743d70)  

Date: Mon Mar 30 20:04:46 2026


---

### ch...@google.com (2026-03-31)

Security Merge Request:

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Requesting merge to stable (M146) because latest trunk commit (1607327) appears to be after stable branch point (1582197).

Merge review required: a commit with DEPS changes was detected.

Requesting merge to beta (M147) because latest trunk commit (1607327) appears to be after beta branch point (1596535).

Merge review required: a commit with DEPS changes was detected.

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### ge...@chromium.org (2026-03-31)

1. <https://chromium-review.googlesource.com/7708753>
2. For 1 day.
3. No.
4. No.
5. No.

### dr...@chromium.org (2026-04-01)

No crashes in Canary after 24 hours. Approved to merge to M147. We don't plan any more M146 releases, so removing that request.

### dx...@google.com (2026-04-02)

Project: angle/angle  

Branch:  chromium/7727  

Author:  Geoff Lang [geofflang@chromium.org](mailto:geofflang@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7722439>

M147: GL: Fix pack state for BlitGL::copySubTextureCPUReadback

---


Expand for full commit details
```
     
    copySubTextureCPUReadback does both ReadPixels and TexImage calls and 
    needs to make sure the client's pack states are not used. It does this 
    but in the wrong order causing an invalid pack state to be used for the 
    ReadPixels call. 
     
    Bug: chromium:490170083 
    Change-Id: I93dcabf52edd6e4e08f999aaa0d96d1fc325211a 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7708753 
    Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org> 
    Commit-Queue: Geoff Lang <geofflang@chromium.org> 
    (cherry picked from commit b149a5c62d76ab536929afc5bba2b2774da46102) 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7722439

```

---

Files:

- M `src/libANGLE/renderer/gl/BlitGL.cpp`
- M `src/tests/capture_replay_tests/capture_replay_expectations.txt`
- M `src/tests/gl_tests/CopyTextureTest.cpp`

---

Hash: [cbc4f074126e6f1acf72ad620a28cd4a8dd86f2a](https://chromiumdash.appspot.com/commit/cbc4f074126e6f1acf72ad620a28cd4a8dd86f2a)  

Date: Fri Mar 27 20:13:31 2026


---

### pe...@google.com (2026-04-02)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### sp...@google.com (2026-04-02)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $90000.00 for this report.

Rationale for this decision:
High Quality. Memory corruption in a highly privileged process (e.g. GPU, network processes) 


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### pe...@google.com (2026-04-20)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2026-04-20)

1. https://chromium-review.git.corp.google.com/c/angle/angle/+/7778732
2. Low - There was no conflict.
3. 147
4. Yes. the bug was introduced in 2017.

### dx...@google.com (2026-04-21)

Project: angle/angle  

Branch:  chromium/7559  

Author:  Geoff Lang [geofflang@chromium.org](mailto:geofflang@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7778732>

[M144-LTS] GL: Fix pack state for BlitGL::copySubTextureCPUReadback

---


Expand for full commit details
```
     
    copySubTextureCPUReadback does both ReadPixels and TexImage calls and 
    needs to make sure the client's pack states are not used. It does this 
    but in the wrong order causing an invalid pack state to be used for the 
    ReadPixels call. 
     
    Bug: chromium:490170083 
    Change-Id: I93dcabf52edd6e4e08f999aaa0d96d1fc325211a 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7708753 
    Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org> 
    Commit-Queue: Geoff Lang <geofflang@chromium.org> 
    (cherry picked from commit b149a5c62d76ab536929afc5bba2b2774da46102) 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7778732 
    Commit-Queue: Gyuyoung Kim (xWF) <qkim@google.com> 
    Reviewed-by: Geoff Lang <geofflang@chromium.org>

```

---

Files:

- M `src/libANGLE/renderer/gl/BlitGL.cpp`
- M `src/tests/capture_replay_tests/capture_replay_expectations.txt`
- M `src/tests/gl_tests/CopyTextureTest.cpp`

---

Hash: [9f511d47469557c3766c28da69dc8d67833da9fd](https://chromiumdash.appspot.com/commit/9f511d47469557c3766c28da69dc8d67833da9fd)  

Date: Fri Mar 27 20:13:31 2026


---

### ch...@google.com (2026-07-07)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/490170083)*
