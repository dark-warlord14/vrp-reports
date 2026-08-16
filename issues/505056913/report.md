# WebGL indexed-draw validation truncation on ANGLE Metal allows out-of-bounds vertex fetches

| Field | Value |
|-------|-------|
| **Issue ID** | [505056913](https://issues.chromium.org/issues/505056913) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>GPU>ANGLE |
| **Platforms** | Mac |
| **Reporter** | mu...@winfunc.com |
| **Assignee** | ge...@google.com |
| **Created** | 2026-04-21 |
| **Bounty** | $2,000.00 |

## Description

Security Bug

VULNERABILITY DETAILS

ANGLE's indexed-draw validator narrows the computed unsigned maximum element index to signed `GLint` before enforcing vertex-buffer bounds:

```
if (!ValidateDrawAttribs(context, entryPoint, static_cast<GLint>(indexRange.end())))
{
    return false;
}

```

That cast appears in `third_party/angle/src/libANGLE/validationES.h` in the source tree and is reachable after the correct 64-bit `maxElementIndex` comparison. On backends where `maxElementIndex` can exceed `INT_MAX` and WebGL relies on ANGLE's manual buffer-access validation, indices above `INT_MAX` can wrap negative at this point and bypass the attribute-limit rejection.

The attached browser PoC creates:

- one `vec4` vertex in an `ARRAY_BUFFER`
- one `UNSIGNED_INT` element index equal to `0x80000000`
- a normal `drawElements(gl.POINTS, 1, gl.UNSIGNED_INT, 0)` call

On the Metal-backed browser configuration below, the draw is accepted and returns `gl.getError() = 0x0`, even though the page references a vertex index far beyond the end of the one-vertex buffer and WebGL should reject the call with `GL_INVALID_OPERATION`.

This run did not produce a visible non-black pixel in the simple point-draw shader, but that does not weaken the validation result: the security bug here is that ANGLE accepts the out-of-bounds indexed draw at all.

VERSION

Chrome Version: Chromium `149.0.7805.0` + dev (local ASan build)
Source Revision: `9b1af1c3bfa10271c6f92691e32659acea5f941c`

Operating System: macOS `26.1` arm64

GPU / renderer: Apple M3 Pro / `ANGLE (Apple, ANGLE Metal Renderer: Apple M3 Pro, Unspecified Version)`

REPRODUCTION CASE

Attachments:

- `poc.html`
- `chrome_parent_metal_index_oob_asan_latest.log`
- `chrome_parent_metal_index_oob_ramp16.log`
- `chrome_parent_metal_index_oob.log` (active-release Chrome confirmation)

Numbered repro steps:

1. Serve the attached PoC locally:

```
python3 -m http.server 8001

```

2. Run Chromium directly with ANGLE Metal forced:

```
/Volumes/BOX/winfunc/winfunc_artifacts/TARGETS/chromium-index-oob-latest/out/asan_index_oob/Chromium.app/Contents/MacOS/Chromium \
  --user-data-dir=/tmp/chrome-index-oob \
  --no-first-run \
  --disable-background-networking \
  --disable-default-apps \
  --disable-sync \
  --metrics-recording-only \
  --enable-logging=stderr \
  --ignore-gpu-blocklist \
  --use-gl=angle \
  --use-angle=metal \
  http://127.0.0.1:8001/poc.html

```

Observed result:

```
[poc] UNMASKED_RENDERER_WEBGL=ANGLE (Apple, ANGLE Metal Renderer: Apple M3 Pro, Unspecified Version)
[poc] uploaded index=0x80000000 count=16 mode=ramp
[poc] gl.getError()=0x0
[poc] sum(rgb)=0 first16=0,0,0,255,...

```

The accepted draw is the proof. A correct WebGL implementation should reject this call before draw submission because the element index references vertex data far outside the bound attribute buffer.

This latest-build ASan browser run did not itself produce a sanitizer report under
`ASAN_OPTIONS=detect_leaks=0:abort_on_error=1:symbolize=1:log_path=...`; no
`index-oob-asan-run*` log files were emitted. The bug still manifests as invalid draw acceptance on
the current ASan build, which is consistent with the out-of-bounds fetch occurring in backend GPU
execution rather than in a CPU-side memory access path directly observable to ASan.

I also retained an active-release browser proof and the stronger 16-index variant:

```
[poc] uploaded index=0x80000000 count=16 mode=ramp
[poc] gl.getError()=0x0
[poc] sum(rgb)=0 ...

```

So on this Metal configuration the bug is not just a one-off acceptance of a single invalid index;
the draw remains accepted under a denser invalid index pattern as well.

Type of crash: N/A (out-of-bounds indexed draw acceptance; no crash required for proof)

Crash State:

```
N/A

```

Client ID (if relevant): N/A

CREDIT INFORMATION

Reporter credit: Mufeed VH from Winfunc Research (winfunc.com)

## Attachments

- [poc.html](attachments/poc.html) (text/html, 3.4 KB)
- [chrome_parent_metal_index_oob.log](attachments/chrome_parent_metal_index_oob.log) (text/plain, 8.4 KB)
- [chrome_parent_metal_index_oob_ramp16.log](attachments/chrome_parent_metal_index_oob_ramp16.log) (text/plain, 8.8 KB)
- [chrome_parent_metal_index_oob_asan_latest.log](attachments/chrome_parent_metal_index_oob_asan_latest.log) (text/plain, 3.5 KB)

## Timeline

### pe...@google.com (2026-04-22)

Out of bounds read on GPU (memory). Potential data exfiltration (cross origin)

### pe...@google.com (2026-04-22)

This is likely not Mac specific and applies to all platforms.

### ch...@google.com (2026-04-23)

Setting milestone because of s0/s1 severity.

### dx...@google.com (2026-04-29)

Project: angle/angle  

Branch:  main  

Author:  Geoff Lang [geofflang@chromium.org](mailto:geofflang@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7797469>

Fix overflows in IndexRange storage.

---


Expand for full commit details
```
     
    IndexRange stores mStart and mCount (instead of mEnd) as uint32_t. 
    mCount will overflow when the end index is UINT_MAX, this can happen 
    when primitive restart is disabled making UINT_MAX a valid index. 
     
    Also fix an invalid cast of IndexRange::end to a signed 32-bit integer 
    in ValidateDrawElementsCommon. 
     
    The test for this behaviour, WebGLCompatibilityTest.LargeIndexRange, had 
    a bug and did not call glVertexAttribPointer causing validation to fail 
    earlier due to buffer being bound to the attribute. 
     
    Also universally limit the max element index to UINT_MAX - 1 to protect 
    against incorrect math assuming draw count can fit in a 32-bit integer. 
     
    Fixed: chromium:504175501 
    Fixed: chromium:505056913 
    Fixed: chromium:506375217 
    Change-Id: I20ebd619e65801833862846a70d31138b2e576b5 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7797469 
    Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org> 
    Commit-Queue: Geoff Lang <geofflang@chromium.org>

```

---

Files:

- M `src/common/mathutil.h`
- M `src/libANGLE/Context.cpp`
- M `src/libANGLE/VertexAttribute.cpp`
- M `src/libANGLE/VertexAttribute.h`
- M `src/libANGLE/renderer/d3d/d3d9/Renderer9.cpp`
- M `src/libANGLE/renderer/renderer_utils.cpp`
- M `src/libANGLE/validationES.h`
- M `src/tests/gl_tests/WebGLCompatibilityTest.cpp`

---

Hash: [ff1b91d5f69e8253a5f8d7075a1253b287ebe9e2](https://chromiumdash.appspot.com/commit/ff1b91d5f69e8253a5f8d7075a1253b287ebe9e2)  

Date: Mon Apr 27 15:33:19 2026


---

### mu...@winfunc.com (2026-05-01)

Post-fix Question: I noticed the fix has landed in ANGLE main. Could you confirm whether this issue is expected to receive a CVE when it reaches Chrome Stable? Also, is it being considered for merge/cherry-pick to a Stable or Beta branch, or will it ride the normal release train?

### sp...@google.com (2026-05-05)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
Baseline. User information disclosure


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### mu...@winfunc.com (2026-05-15)

Question: How are CVEs assigned and on what basis? For this vulnerability, now that it's fixed, would a CVE be issued? I'd love to know if some findings are exempt or if there's a criteria for it.

### dx...@google.com (2026-05-25)

Project: angle/angle  

Branch:  chromium/7778  

Author:  Geoff Lang [geofflang@chromium.org](mailto:geofflang@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7870600>

M148: Fix overflows in IndexRange storage.

---


Expand for full commit details
```
     
    IndexRange stores mStart and mCount (instead of mEnd) as uint32_t. 
    mCount will overflow when the end index is UINT_MAX, this can happen 
    when primitive restart is disabled making UINT_MAX a valid index. 
     
    Also fix an invalid cast of IndexRange::end to a signed 32-bit integer 
    in ValidateDrawElementsCommon. 
     
    The test for this behaviour, WebGLCompatibilityTest.LargeIndexRange, had 
    a bug and did not call glVertexAttribPointer causing validation to fail 
    earlier due to buffer being bound to the attribute. 
     
    Also universally limit the max element index to UINT_MAX - 1 to protect 
    against incorrect math assuming draw count can fit in a 32-bit integer. 
     
    Fixed: chromium:514924845 
    Bug: chromium:504175501 
    Bug: chromium:505056913 
    Bug: chromium:506375217 
    Change-Id: I20ebd619e65801833862846a70d31138b2e576b5 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7797469 
    Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org> 
    Commit-Queue: Geoff Lang <geofflang@chromium.org> 
    (cherry picked from commit ff1b91d5f69e8253a5f8d7075a1253b287ebe9e2) 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7870600

```

---

Files:

- M `src/common/mathutil.h`
- M `src/libANGLE/Context.cpp`
- M `src/libANGLE/VertexAttribute.cpp`
- M `src/libANGLE/VertexAttribute.h`
- M `src/libANGLE/renderer/d3d/d3d9/Renderer9.cpp`
- M `src/libANGLE/renderer/renderer_utils.cpp`
- M `src/libANGLE/validationES.h`
- M `src/tests/gl_tests/WebGLCompatibilityTest.cpp`

---

Hash: [c05368c07ace2fcd1da4963b481283fc90400bec](https://chromiumdash.appspot.com/commit/c05368c07ace2fcd1da4963b481283fc90400bec)  

Date: Mon Apr 27 15:33:19 2026


---

### dx...@google.com (2026-05-27)

Project: angle/angle  

Branch:  chromium/7559  

Author:  Geoff Lang [geofflang@chromium.org](mailto:geofflang@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7866556>

[M144-LTS] Fix overflows in IndexRange storage.

---


Expand for full commit details
```
     
    IndexRange stores mStart and mCount (instead of mEnd) as uint32_t. 
    mCount will overflow when the end index is UINT_MAX, this can happen 
    when primitive restart is disabled making UINT_MAX a valid index. 
     
    Also fix an invalid cast of IndexRange::end to a signed 32-bit integer 
    in ValidateDrawElementsCommon. 
     
    The test for this behaviour, WebGLCompatibilityTest.LargeIndexRange, had 
    a bug and did not call glVertexAttribPointer causing validation to fail 
    earlier due to buffer being bound to the attribute. 
     
    Also universally limit the max element index to UINT_MAX - 1 to protect 
    against incorrect math assuming draw count can fit in a 32-bit integer. 
     
    Fixed: chromium:504175501 
    Fixed: chromium:505056913 
    Fixed: chromium:506375217 
    Change-Id: I20ebd619e65801833862846a70d31138b2e576b5 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7797469 
    Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org> 
    Commit-Queue: Geoff Lang <geofflang@chromium.org> 
    (cherry picked from commit ff1b91d5f69e8253a5f8d7075a1253b287ebe9e2) 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7866556 
    Commit-Queue: Gyuyoung Kim (xWF) <qkim@google.com> 
    Reviewed-by: Geoff Lang <geofflang@chromium.org>

```

---

Files:

- M `src/common/mathutil.h`
- M `src/libANGLE/Context.cpp`
- M `src/libANGLE/VertexAttribute.cpp`
- M `src/libANGLE/VertexAttribute.h`
- M `src/libANGLE/renderer/d3d/d3d9/Renderer9.cpp`
- M `src/libANGLE/renderer/renderer_utils.cpp`
- M `src/libANGLE/validationES.h`
- M `src/tests/gl_tests/WebGLCompatibilityTest.cpp`

---

Hash: [144d771e4fd65fcb386de198eb34e3bda9a795cf](https://chromiumdash.appspot.com/commit/144d771e4fd65fcb386de198eb34e3bda9a795cf)  

Date: Mon Apr 27 15:33:19 2026


---

### eb...@google.com (2026-08-13)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/505056913)*
