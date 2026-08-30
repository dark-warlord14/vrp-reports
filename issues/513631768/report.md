# WebGPU T2B Compute-Blit No-Submit Stale Buffer Disclosure

| Field | Value |
|-------|-------|
| **Issue ID** | [513631768](https://issues.chromium.org/issues/513631768) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Dawn |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, iOS, ChromeOS |
| **Reporter** | sh...@dongspace.info |
| **Assignee** | sh...@google.com |
| **Created** | 2026-05-16 |
| **Bounty** | $1,000.00 |

## Description

Security Bug

Important: Please do not change the component of this bug manually.

Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/faq.md>

Please see the following link for instructions on filing security bugs: <https://www.chromium.org/Home/chromium-security/reporting-security-bugs>

Reports may be eligible for reward payments under the Chrome VRP: <https://g.co/chrome/vrp>

NOTE: Security bugs are normally made public once a fix has been widely deployed.

---

### VULNERABILITY DETAILS

`third_party/dawn/src/dawn/native/BlitTextureToBuffer.cpp` marks a WebGPU
destination buffer initialized while encoding a `copyTextureToBuffer()` command
that uses Dawn's T2B compute-blit path:

```
// Skip clearing the buffer if this is full size copy.
dst.buffer->SetInitialized(fullSizeCopy || dst.buffer->IsInitialized());

```

This is a security issue because WebGPU command buffers do not have to be
submitted. A web page can call `encoder.finish()` and intentionally drop the
returned `GPUCommandBuffer`. In that case the compute blit never executes and
never writes the destination buffer, but Dawn's persistent buffer metadata still
says the buffer is initialized.

A later submitted `copyBufferToBuffer()` from the same destination buffer then
skips Dawn's lazy zero-initialization path and exposes stale GPU allocation
contents to JavaScript through a `MAP_READ` buffer.

The broken invariant is:

```
BufferBase::mIsDataInitialized must become true only after the buffer contents
were actually initialized by submitted GPU work, CPU upload, map-at-creation
initialization, or allocator-level clearing.

```

`fullSizeCopy` only proves that the encoded T2B operation would overwrite the
whole buffer if it executed. It does not prove that the command buffer will ever
be submitted.

This is the same bug class as the timestamp `resolveQuerySet` no-submit issue
fixed in Dawn by `b073946efb` / Chromium backport `36a8c01`, where an analogous
encode-time `SetInitialized(true)` call was removed because encoded work may
never execute.

### DEMONSTRATED IMPACT

The demonstrated impact is stale GPU allocation disclosure within one Dawn
`GPUDevice` allocator scope when the `use_blit_for_t2b` path is reachable.

Script with access to a `GPUDevice` can recover bytes from WebGPU resources
that were previously destroyed or dropped within that same `GPUDevice`, if it
can allocate a matching buffer size class and trigger the no-submit T2B
compute-blit path.

This can expose application-level GPU data such as image-processing
intermediates, ML/inference tensors, render targets, texture readback buffers,
or other transient WebGPU resources after the application has dropped or
destroyed the original resource.

**A practical attacking scenario**

A same-origin third-party script (e.g. imported `<script src=xxx>` tags, which can be compromised analytics, ad, or CDN dependency) — that
activates after the destroy step has full access to that GPUDevice but no API path to the
destroyed weights or activations. This bug provides the path: allocate a matching-size
buffer, no-submit T2B, read back the destroyed allocation slot.

### VERSION

Chrome Version: `148.0.7778.167` Stable
Operating System: Android 15, Pixel 6, ARM Mali Valhall GPU, Vulkan backend

Result:

```
Positive with --enable-dawn-features=use_blit_for_t2b
Negative without the Dawn T2B feature on this device
--enable-unsafe-webgpu not required

```

Chrome Version: `148.0.7778.168` Stable
Operating System: Windows 10 Version 22H2, Build `19045.6466`,
NVIDIA GeForce RTX 3070 Ti, driver `32.0.15.7602`

Result:

```
No flags: negative on this host. chrome://gpu shows the default usable WebGPU
adapter is D3D12, and the D3D11 WebGPU adapter is blocklisted. 
With --enable-dawn-features=use_blit_for_t2b: positive stale GPU buffer
disclosure.

```

Chrome Version: `149.0.7827.14` Beta
Operating System: Windows 10 Version 22H2, Build `19045.6466`,
NVIDIA GeForce RTX 3070 Ti, driver `32.0.15.7602`

Result:

```
No flags: negative on this host for the same D3D12-default / D3D11-blocklisted
reason.
With --enable-dawn-features=use_blit_for_t2b: positive stale GPU buffer
disclosure.

```
### REPRODUCTION CASE

#### Android PoC verification steps

Use these steps for Android Chrome. The tested Pixel 6 path required the
non-rooted Chrome command-line mechanism plus `use_blit_for_t2b`.

1. In Chrome, open:

```
chrome://flags/#enable-command-line-on-non-rooted-devices

```

2. Set it to `Enabled`.
3. Relaunch Chrome.
4. With USB debugging enabled, install the command line. From this folder on
   the computer, either push the provided template:

```
adb push chrome-command-line.txt /data/local/tmp/chrome-command-line

```

Then restart Chrome.
5. Set up the http server.

```
python3 -m http.server 18099 --bind 127.0.0.1
adb reverse tcp:18099 tcp:18099
adb shell am force-stop com.android.chrome
adb shell am start -n com.android.chrome/com.google.android.apps.chrome.Main \
  -d http://127.0.0.1:18099/poc.html

```
#### Windows PoC verification steps

The server setup procedure is the same as Android. The command line to start Chrome with certain command lines can be:

```
$Chrome = "$env:LOCALAPPDATA\Google\Chrome\Application\chrome.exe"
if (!(Test-Path $Chrome)) { $Chrome = "$env:ProgramFiles\Google\Chrome\Application\chrome.exe" }
& $Chrome `
  --user-data-dir="$env:TEMP\webgpu-t2b-repro-stable" `
  --no-first-run `
  --no-default-browser-check `
  --enable-dawn-features=use_blit_for_t2b `
  http://127.0.0.1:18099/poc.html

```

The `poc.html` is attached below.
The PoC performs the following sequence:

```
1. Victim: Create one GPUDevice.
2. Victim: Create a prior WebGPU resource containing a per-trial positional nonce.
3. Victim: Destroy/drop that prior resource.
4. Victim: Submit an empty command buffer and await queue.onSubmittedWorkDone() so
   Dawn can recycle the prior allocation.
5. Attacker: Allocate an attacker buffer of the same size class.
6. Attacker: Encode a full-buffer copyTextureToBuffer() into the attacker buffer.
7. Attacker: Call encoder.finish() but do not submit that command buffer.
8. Attacker: Submit a separate copyBufferToBuffer(attacker -> MAP_READ buffer).
9. Attacker: Map the readback buffer and check for current or historical nonce bytes.

```

The critical bug is step 7: `copyTextureToBuffer()` marks the attacker buffer
initialized during encoding, but the command buffer is never submitted and the
attacker buffer is never actually written by the T2B blit.

**How to Read `poc.html`**

The page highlights the no-submit attack rows and keeps the full JSON under
"Raw CHROVUS\_LINE output".

Important fields:

```
didSubmit=false
  This is the vulnerable no-submit path. The T2B command buffer was finished
  and dropped instead of being submitted.

nonZero / allZero
  A safe no-submit read should return all zeroes because the destination buffer
  should still require Dawn lazy initialization. nonZero > 0 in a no-submit
  attack trial means stale bytes were exposed.

linearMatches
  Number of texels matching the current trial pattern
  [x_low_byte, y_low_byte, nonce_byte_0, nonce_byte_1] at the expected row-major
  position. This is the strongest current-trial proof.

nonceOnly
  Number of texels containing the current nonce in bytes 2 and 3 but not at the
  expected row-major position. This still proves recovery of current-trial data,
  and usually reflects driver tiling/swizzling.

historicalNonceHits
  Matches for nonces from earlier trials. Hits in T3/T4 are useful because those
  trials do not create a current primer allocation before the no-submit read.

```

Trial meanings:

```
T1_L2_positional_4M
  Primes and destroys a 4MB texture, then performs a no-submit T2B read into a
  same-size attacker buffer. Current nonce hits are a positive leak.

T2_L2_positional_4M_spray
  Same size class as T1, with allocator spray. Current or historical nonce hits
  show stale allocation reuse.

T3_no_prime_null_4M
  No current primer is created. Historical nonce hits show residual bytes from
  an earlier trial, not from the current trial's own write.

T4_no_prime_null_4M_spray
  Same as T3, with allocator spray to exercise reuse behavior.

T5_L2_positional_256K
  Repeats the current nonce leak test in a smaller 256KB size class.

```

The expected positive pattern is:

```
Any no-submit attack row with:

  didSubmit=false
  allZero=0
  linearMatches + nonceOnly > 0

or:

  didSubmit=false
  allZero=0
  historicalNonceHits[*].hits > 0

```

`T3` and `T4` are especially useful for explaining impact because they
demonstrate historical residual data without a current same-trial primer.

CREDIT INFORMATION
Externally reported security bugs may appear in Chrome release notes. If this bug is included, how would you like to be credited?
Reporter credit: Chrovus

## Attachments

- [poc.html](attachments/poc.html) (text/html, 11.3 KB)
- [01_chrome_version.png](attachments/01_chrome_version.png) (image/png, 322.9 KB)
- [02_poc_top_summary.png](attachments/02_poc_top_summary.png) (image/png, 219.9 KB)
- [03_raw_evidence.png](attachments/03_raw_evidence.png) (image/png, 218.8 KB)
- [chrome-command-line.txt](attachments/chrome-command-line.txt) (text/plain, 83 B)

## Timeline

### sh...@dongspace.info (2026-05-16)

Forgot to upload the /data/local/tmp/chrome-command-line file.

### ch...@google.com (2026-05-17)

Setting Priority to P3 to match Severity s3. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### cw...@chromium.org (2026-05-18)

Shrek, PTAL, since this is an optimization, I think we can remove it for now with a TODO to add it later. Please also add a test that would have caught the issue.

### cw...@chromium.org (2026-05-18)

P2 / S2 for uninitialized GPU memory read.

### ch...@google.com (2026-05-19)

Setting milestone because of s2 severity.

### dx...@google.com (2026-05-20)

Project: dawn  

Branch:  main  

Author:  Shrek Shao [shrekshao@google.com](mailto:shrekshao@google.com)  

Link:    <https://dawn-review.googlesource.com/309588>

Remove the optimization of a clearing buffer in BlitTextureToBuffer

---


Expand for full commit details
```
     
    This optimization is temporarily removed because we cannot mark 
    the buffer as initialized until the command buffer is submitted. 
     
    FIXED: 513631768 
    Change-Id: Ie6f539e07139c5eefef9ddf87231af346d7a9e28 
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/309588 
    Auto-Submit: Shrek Shao <shrekshao@google.com> 
    Reviewed-by: Loko Kung <lokokung@google.com> 
    Commit-Queue: Shrek Shao <shrekshao@google.com>

```

---

Files:

- M `src/dawn/native/BlitTextureToBuffer.cpp`
- M `src/dawn/tests/end2end/BufferZeroInitTests.cpp`
- M `src/dawn/tests/end2end/CopyTests.cpp`
- M `src/dawn/tests/end2end/TextureZeroInitTests.cpp`

---

Hash: 6ea97833a636247bc137ee6d24efd0ac7a68111d  

Date: Wed May 20 18:06:10 2026


---

### sp...@google.com (2026-05-27)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
ASAN Read. Browser / Network / GPU (From web contents)


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-08-27)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/513631768)*
