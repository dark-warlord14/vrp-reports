# ANGLE D3D11: stale ID3D11Buffer pointer in TransformFeedback11 mBuffers leads to use-after-free in GPU process via SOSetTargets

| Field | Value |
|-------|-------|
| **Issue ID** | [489791425](https://issues.chromium.org/issues/489791425) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU>ANGLE |
| **Platforms** | Windows |
| **Reporter** | je...@gmail.com |
| **Assignee** | ge...@chromium.org |
| **Created** | 2026-03-05 |
| **Bounty** | $11,000.00 |

## Description

# ANGLE D3D11: stale ID3D11Buffer pointer in TransformFeedback11 mBuffers leads to use-after-free in GPU process via SOSetTargets

## Summary

The ANGLE D3D11 backend caches raw `ID3D11Buffer*` pointers in `TransformFeedback11::mBuffers` but never clears entries whose corresponding GL buffer binding has become null. When a WebGL2 program binds a transform feedback buffer to an unused slot, performs a TF draw to populate the cache, then deletes the buffer and initiates a second TF draw, the stale pointer is passed to `ID3D11DeviceContext::SOSetTargets`, which dereferences the freed COM object. This is a use-after-free in the GPU process on Windows systems using the D3D11 rendering backend. The vulnerability is deterministic and triggers on every attempt.

Platform: Windows only (D3D11 backend). Requires a GPU with D3D11 support.

## Bisect

Introducing Commit: `73bd218e12d26a626e0b21625606593ad2a5fd1a`

- Date: 2016-07-15
- Author: Geoff Lang [geofflang@chromium.org](mailto:geofflang@chromium.org)
- Review: <https://chromium-review.googlesource.com/360910>

## Root Cause

`TransformFeedback11` maintains a vector of raw `ID3D11Buffer*` pointers that mirror the GL-level indexed buffer bindings for stream output. When `getSOBuffers` prepares the buffer array for `SOSetTargets`, it iterates over all slots but only writes into `mBuffers[i]` when the corresponding binding is non-null.

```
// third_party/angle/src/libANGLE/renderer/d3d/d3d11/TransformFeedback11.cpp
for (size_t bindingIdx = 0; bindingIdx < mBuffers.size(); bindingIdx++)
{
    const auto &binding = mState.getIndexedBuffer(bindingIdx);
    if (binding.get() != nullptr)
    {
        Buffer11 *storage = GetImplAs<Buffer11>(binding.get());
        BufferFeedback feedback;
        ANGLE_TRY(storage->getBuffer(context, BUFFER_USAGE_VERTEX_OR_TRANSFORM_FEEDBACK,
                                     &mBuffers[bindingIdx], &feedback));
        binding.get()->applyImplFeedback(context, feedback);
    }
    // Missing: else { mBuffers[bindingIdx] = nullptr; }
}

```

When a binding transitions from non-null to null, as happens when `deleteBuffer` detaches the buffer from the transform feedback object, the corresponding `mBuffers` entry retains the old `ID3D11Buffer*`. The pointer returned by `Buffer11::getBuffer` is a non-owning raw pointer obtained via `.get()` on the internal `Resource11<ID3D11Buffer>` wrapper, with no `AddRef` performed. Once the `Buffer11` is destroyed by `deleteBuffer`, its destructor releases the underlying `ID3D11Buffer` through `TypedData::~TypedData`, which calls `Release()` and drops the COM refcount to zero.

Meanwhile, `TransformFeedback11::bindIndexedBuffer`, called during the detach path, marks the object as dirty and updates the offset but does not clear `mBuffers[index]`.

```
// third_party/angle/src/libANGLE/renderer/d3d/d3d11/TransformFeedback11.cpp
angle::Result TransformFeedback11::bindIndexedBuffer(
    const gl::Context *context,
    size_t index,
    const gl::OffsetBindingPointer<gl::Buffer> &binding)
{
    mIsDirty              = true;
    mBufferOffsets[index] = static_cast<UINT>(binding.getOffset());
    mRenderer->getStateManager()->invalidateTransformFeedback();
    return angle::Result::Continue;
}

```

The number of buffers passed to `SOSetTargets` is determined by `getNumSOBuffers`, which returns `mBuffers.size()`, the total number of indexed buffer slots (typically 4 on D3D11), regardless of how many the linked program actually requires.

```
// third_party/angle/src/libANGLE/renderer/d3d/d3d11/TransformFeedback11.cpp
UINT TransformFeedback11::getNumSOBuffers() const
{
    return static_cast<UINT>(mBuffers.size());
}

```

The validation performed by `ValidateProgramExecutableXFBBuffersPresent` only checks slots up to `programExecutable->getTransformFeedbackBufferCount()`. For a program linked with `INTERLEAVED_ATTRIBS` and a single varying, this count is 1, so only slot 0 is validated. Slot 1 can be null without causing a validation failure, yet `mBuffers[1]` still holds the dangling pointer and is passed to `SOSetTargets`.

```
// third_party/angle/src/libANGLE/validationES.cpp
bool ValidateProgramExecutableXFBBuffersPresent(const Context *context,
                                                const ProgramExecutable *programExecutable)
{
    size_t programXfbCount = programExecutable->getTransformFeedbackBufferCount();
    const TransformFeedback *transformFeedback = context->getState().getCurrentTransformFeedback();
    for (size_t programXfbIndex = 0; programXfbIndex < programXfbCount; ++programXfbIndex)
    {
        const OffsetBindingPointer<Buffer> &buffer =
            transformFeedback->getIndexedBuffer(programXfbIndex);
        if (!buffer.get())
        {
            return false;
        }
    }
    return true;
}

```

The trigger sequence exploits this gap between the number of slots the program needs and the number `getSOBuffers` passes to D3D. The attacker binds a buffer to a slot unused by the program, performs a TF draw to cache its D3D pointer, unbinds and deletes it, then begins a new TF pass. Because validation only checks program-required slots, the second `beginTransformFeedback` succeeds, and the subsequent draw call feeds the stale pointer to `SOSetTargets`. The D3D11 runtime attempts to access the freed COM object, resulting in a use-after-free.

## Reproduce

This bug affects the ANGLE D3D11 backend and can only be reproduced on Windows with a GPU that uses the D3D11 rendering path. It was tested on Chromium commit `cdd1f63c02a65c37ccdb85e85b25dbec456c9914`.

No source code modifications are required. The PoC is a self-contained HTML file that triggers the vulnerability through the WebGL2 Transform Feedback API.

To build Chromium, use a release configuration. Create `out/release/args.gn` with the following content, then run `gn gen out/release` and `autoninja -C out/release chrome`.

```
is_debug = false
dcheck_always_on = false
target_cpu = "x64"

```

Because the use-after-free occurs on a D3D11 COM object allocated by the Windows system heap rather than by an ASAN-instrumented allocator, ASAN cannot detect this bug. Windows Page Heap is the appropriate detection tool. Enable it by running the following command in an elevated (Administrator) command prompt, where the path to `gflags.exe` may vary depending on the Windows SDK installation.

```
"C:\Program Files (x86)\Windows Kits\10\Debuggers\x64\gflags.exe" /p /enable chrome.exe /full

```

Serve the PoC over HTTP. From the directory containing `poc.html`, start a local server with `python -m http.server 8080`.

Launch Chrome with the following command.

```
out\release\chrome.exe --no-sandbox --user-data-dir=%TEMP%\angl107_test --no-first-run --disable-default-apps --disable-extensions http://localhost:8080/poc.html

```

The PoC runs 50 iterations of the trigger sequence automatically. Within several seconds, the GPU process will crash with an access violation inside `d3d11!CContext::TID3D11DeviceContext_SOSetTargets_<2>`, and Chrome will report "The GPU process has crashed" in its stderr output. A Crashpad dump is written to the user data directory under `Crashpad/reports/`. Analyzing the dump with WinDbg confirms the crash occurs when `SOSetTargets` dereferences a dangling `ID3D11Buffer*` pointer at a page marked `PAGE_NOACCESS` by the page heap.

After testing, disable page heap by running the following command in an elevated prompt.

```
"C:\Program Files (x86)\Windows Kits\10\Debuggers\x64\gflags.exe" /p /disable chrome.exe

```
### Crash log

```
Chrome stderr:
[12552:19208:WARNING:content\browser\gpu\gpu_process_host.cc:1441] The GPU process has crashed 1 time(s)
[12552:19208:INFO:CONSOLE:0] "WebGL: CONTEXT_LOST_WEBGL: loseContext: context lost"
[12552:19208:WARNING:content\browser\gpu\gpu_process_host.cc:1021] Reinitialized the GPU process after a crash. The reported initialization time was 214 ms

WinDbg crash dump analysis (GPU process):

EXCEPTION_RECORD:
ExceptionAddress: 00007ff94483640a (d3d11!CContext::TID3D11DeviceContext_SOSetTargets_<2>+0xda)
   ExceptionCode: c0000005 (Access violation)
  ExceptionFlags: 00000000
NumberParameters: 2
   Parameter[0]: 0000000000000000
   Parameter[1]: 000001b1b6e68fd0
Attempt to read from address 000001b1b6e68fd0

CONTEXT:
rax=0000000000000000 rbx=000001b1a02052a0 rcx=0000000000000001
rdx=000001b1b6e68e78 rsi=0000000000000000 rdi=0000000000000004
rip=00007ff94483640a rsp=000000abd43fd690 rbp=0000000000000000
 r8=0000000000000000  r9=0000204800173d28 r10=000000abd43fd6c1
r11=0000000000000000 r12=0000204800038f80 r13=0000000000014000
r14=0000000000000001 r15=0000204800173d20

Faulting instruction:
d3d11!CContext::TID3D11DeviceContext_SOSetTargets_<2>+0xda:
00007ff94483640a  cmp dword ptr [rdx+158h],eax  ds:000001b1b6e68fd0=????????

NTGLOBALFLAG:  2000000
APPLICATION_VERIFIER_LOADED: 1
FAILURE_BUCKET_ID:  INVALID_POINTER_READ_AVRF_c0000005_d3d11.dll!CContext::TID3D11DeviceContext_SOSetTargets__2_

STACK_TEXT:
d3d11!CContext::TID3D11DeviceContext_SOSetTargets_<2>+0xda
libglesv2!glStartTilingQCOM+0x32bece  (StateManager11::syncTransformFeedbackBuffers)
libglesv2!glStartTilingQCOM+0x32b1f6  (StateManager11::updateState)
libglesv2!glStartTilingQCOM+0x2ff2fe  (Context11::drawArrays)
libglesv2!GL_DrawArrays+0x31f         (gl::Context::drawArrays)
chrome!...                             (GPU command buffer dispatch)

```

The register `rdx` holds the value `000001b1b6e68e78`, which is the dangling `ID3D11Buffer*` from `mBuffers[1]`. The D3D11 runtime reads at `rdx+0x158` (`000001b1b6e68fd0`), which falls on a `PAGE_NOACCESS` guard page placed by the page heap around the freed allocation. This confirms a use-after-free on the released COM object.

## Credit

Please use c6eed09fc8b174b0f3eebedcceb1e792 as the credit for this vulnerability. Thank you.

## Attachments

- [poc.html](attachments/poc.html) (text/html, 5.4 KB)
- [crash.log](attachments/crash.log) (text/plain, 4.1 KB)
- [readme.md](attachments/readme.md) (text/markdown, 2.2 KB)
- [b7ab035a-4ddb-4598-a050-e71c2911c070.dmp](attachments/b7ab035a-4ddb-4598-a050-e71c2911c070.dmp) (application/octet-stream, 4.3 MB)

## Timeline

### je...@gmail.com (2026-03-05)

--no-sandbox was a typo when copying, no need for --no-sandbox，This is a UAF vulnerability directly triggered by a GPU process

### ct...@google.com (2026-03-05)

Thanks for the report! Could you share an uploaded crash report ID from this as well (via chrome://crashes)?

### je...@gmail.com (2026-03-06)

b7ab035a-4ddb-4598-a050-e71c2911c070

Chrome Version: 145.0.7632.160 (Chrome Stable)

I'm not sure if my request was successfully uploaded, so I've attached it in the attachment.

### jd...@chromium.org (2026-03-09)

Thanks for that. I've set flags conservatively assuming this report is valid, but I have not personally reproduced it.

geofflang@: would you mind taking a look? Thank you!

### ch...@google.com (2026-03-10)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-03-10)

Setting Priority to P1 to match Severity s1. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### dx...@google.com (2026-03-25)

Project: angle/angle  

Branch:  main  

Author:  Geoff Lang [geofflang@chromium.org](mailto:geofflang@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7689826>

D3D11: Fix buffer state tracking in TransformFeedback11.

---


Expand for full commit details
```
     
    TransformFeedback11::getSOBuffers would only update the elements of 
    mBuffers if the GL buffer binding was non-null. This could lead to 
    setting a previously-deleted buffer on the DeviceContext later. 
     
    Update the state tracking in TransformFeedback11 to null out entries in 
    mBuffers every time a new buffer is bound and add a null check when 
    synchronizing mBuffers. 
     
    Bug: angleproject:489791425 
    Change-Id: Ic80e36c1511d5e14d41a13c56f5055c55f36bc20 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7689826 
    Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org> 
    Commit-Queue: Geoff Lang <geofflang@chromium.org>

```

---

Files:

- M `src/libANGLE/renderer/d3d/d3d11/TransformFeedback11.cpp`
- M `src/tests/gl_tests/TransformFeedbackTest.cpp`

---

Hash: [06e6c6b59454d0a122fb274b2e1dd0ab09ffb638](https://chromiumdash.appspot.com/commit/06e6c6b59454d0a122fb274b2e1dd0ab09ffb638)  

Date: Mon Mar 23 16:30:56 2026


---

### ch...@google.com (2026-03-26)

Security Merge Request:

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M146. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M147. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

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

Branch:  chromium/7680  

Author:  Geoff Lang [geofflang@chromium.org](mailto:geofflang@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7717655>

M146: D3D11: Fix buffer state tracking in TransformFeedback11.

---


Expand for full commit details
```
     
    TransformFeedback11::getSOBuffers would only update the elements of 
    mBuffers if the GL buffer binding was non-null. This could lead to 
    setting a previously-deleted buffer on the DeviceContext later. 
     
    Update the state tracking in TransformFeedback11 to null out entries in 
    mBuffers every time a new buffer is bound and add a null check when 
    synchronizing mBuffers. 
     
    Bug: angleproject:489791425 
    Change-Id: Ic80e36c1511d5e14d41a13c56f5055c55f36bc20 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7689826 
    Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org> 
    Commit-Queue: Geoff Lang <geofflang@chromium.org> 
    (cherry picked from commit 06e6c6b59454d0a122fb274b2e1dd0ab09ffb638) 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7717655

```

---

Files:

- M `src/libANGLE/renderer/d3d/d3d11/TransformFeedback11.cpp`
- M `src/tests/gl_tests/TransformFeedbackTest.cpp`

---

Hash: [788e6d6c17e82282a25d8a323aac9e5fc4c6bddb](https://chromiumdash.appspot.com/commit/788e6d6c17e82282a25d8a323aac9e5fc4c6bddb)  

Date: Mon Mar 23 16:30:56 2026


---


---

Project: angle/angle  

Branch:  chromium/7727  

Author:  Geoff Lang [geofflang@chromium.org](mailto:geofflang@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7717656>

M147: D3D11: Fix buffer state tracking in TransformFeedback11.

---


Expand for full commit details
```
     
    TransformFeedback11::getSOBuffers would only update the elements of 
    mBuffers if the GL buffer binding was non-null. This could lead to 
    setting a previously-deleted buffer on the DeviceContext later. 
     
    Update the state tracking in TransformFeedback11 to null out entries in 
    mBuffers every time a new buffer is bound and add a null check when 
    synchronizing mBuffers. 
     
    Bug: angleproject:489791425 
    Change-Id: Ic80e36c1511d5e14d41a13c56f5055c55f36bc20 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7689826 
    Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org> 
    Commit-Queue: Geoff Lang <geofflang@chromium.org> 
    (cherry picked from commit 06e6c6b59454d0a122fb274b2e1dd0ab09ffb638) 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7717656

```

---

Files:

- M `src/libANGLE/renderer/d3d/d3d11/TransformFeedback11.cpp`
- M `src/tests/gl_tests/TransformFeedbackTest.cpp`

---

Hash: [dbeb8c9415e1531858e09da1537e682bb509b9fc](https://chromiumdash.appspot.com/commit/dbeb8c9415e1531858e09da1537e682bb509b9fc)  

Date: Mon Mar 23 16:30:56 2026


---

### sp...@google.com (2026-04-10)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $11000.00 for this report.

Rationale for this decision:
Baseline with bisect. Memory corruption in a highly privileged process (e.g. GPU, network processes) 


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-07-02)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/489791425)*
