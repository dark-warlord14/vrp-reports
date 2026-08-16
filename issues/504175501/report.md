# Integer wrap in ANGLE IndexRange allows WebGL OOB vertex fetch

| Field | Value |
|-------|-------|
| **Issue ID** | [504175501](https://issues.chromium.org/issues/504175501) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>GPU>ANGLE |
| **Platforms** | Mac |
| **Reporter** | ra...@gmail.com |
| **Assignee** | ge...@google.com |
| **Created** | 2026-04-19 |
| **Bounty** | $2,000.00 |

## Description

VULNERABILITY DETAILS

The IndexRange(uint32_t start, uint32_t end) constructor at
third_party/angle/src/common/mathutil.h:875 computes
mCount = end - start + 1. For IndexRange(0, 0xffffffff) this
wraps to 0 and isEmpty() returns true.

ValidateDrawElementsCommon at validationES.h:1116 uses
isEmpty() to gate both maxElementIndex and ValidateDrawAttribs.
A WebGL1 drawElements(GL_POINTS, 2, GL_UNSIGNED_INT, 0) with
OES_element_index_uint enabled and element-array buffer
{0, 0xffffffff} is therefore accepted even though the second
index is out of range for the bound vertex-attribute buffer.
Primitive restart is off in WebGL1, so 0xffffffff reaches
ComputeTypedIndexRange as a real index.

The OOB vertex fetch reaches the GPU. On ANGLE Vulkan backends
whose physical device does not enable robustBufferAccess (the
ES2_Vulkan_SwiftShader configuration Chromium ships for
conformance testing is one such), this causes a GPU process
SIGSEGV at the address (0xffffffff * stride) mod 2^32 past the
bound vertex buffer. With WebGL side spray to cover the 4 GiB
region past the bound VBO, readPixels returns 16 bytes of
attacker placed GPU process memory.

VERSION

Chrome Version: 147.0.7727.102 stable
Operating System: Multi-platform, ANGLE code. Directly verified on:
macOS 26.4, Apple M1
Windows 11, NVIDIA GeForce RTX 5070 Ti Laptop GPU
Ubuntu 24.04 x86_64

REPRODUCTION CASE

To see the bypass directly at JS level, open poc.html in Chrome
on a backend where ANGLE runs its manual buffer-access validation.

On macOS (Apple Silicon), the default backend is already such a
backend. Just open the file:

open /Applications/Google\ Chrome.app poc.html

On Windows, the default backend is D3D11 which masks the OOB.
Use --use-angle=d3d9 to get an observable backend:

chrome.exe --use-angle=d3d9 --user-data-dir=C:\tmp\chrome-d3d9 path\to\poc.html

Expected output on an observable backend:

all_max_control=INVALID_OPERATION indices=[0xffffffff]
min_max_wrap_probe=NO_ERROR indices=[0x0,0xffffffff]
RESULT=SUSPICIOUS: mixed 0/UINT_MAX bypassed where all-UINT_MAX was rejected

On Windows D3D11/GL/Vulkan and on in-browser SwiftShader, both
calls return NO_ERROR. The bypass still fires inside ANGLE; the
resulting OOB is masked by the driver's robust buffer access.

To verify the memory safety consequence on the non-robust path
that Chrome ships for its own conformance tests, apply poc.patch
and run:

  autoninja -C out/Test angle_unittests angle_end2end_tests
  ./out/Test/angle_unittests --gtest_filter=Utilities.IndexRanges
  xvfb-run -a ./out/Test/angle_end2end_tests \
    --gtest_filter=WebGLDrawElementsTest.MixedUintMaxIndexRangeIsNotEmpty/ES2_Vulkan_SwiftShader

The unit test fails because isEmpty() returns true for the
full uint range. The end to end test under an is_asan=true
build produces an AddressSanitizer DEADLYSIGNAL whose register
state has rdx = r8 = r9 = 0xfffffff4 = (0xffffffff * 12) mod 2^32.
The attacker supplied index becomes the wrapped vertex fetch
byte offset.

CREDIT INFORMATION
Reporter credit: Rahul Raj

## Attachments

- [poc.html](attachments/poc.html) (text/html, 3.8 KB)
- [poc.patch](attachments/poc.patch) (text/x-diff, 3.0 KB)

## Timeline

### me...@google.com (2026-04-20)

Redirecting to GPU triage.

### pe...@google.com (2026-04-20)

@ra...@gmail.com

Difficult to evaluation severity. We have an out of bounds GPU read that behaves as though it is data exfiltration and not memory corruption. (aka no writes)

This doesnt seem to apply to any shipped skus but I cannot be definitive yet.
I think this is s1 unless we can prove memory corruption.

### ch...@google.com (2026-04-23)

Setting milestone because of s0/s1 severity.

### ge...@google.com (2026-04-27)

This is real but only affects Mac/Metal in practice. SwiftShader and D3D9 are no longer used in Chrome production builds.

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

### aj...@google.com (2026-05-05)

Medium Severity as this does not demonstrate a fully controlled 16 byte read.

### sp...@google.com (2026-05-05)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
Baseline. User information disclosure


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

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
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/504175501)*
