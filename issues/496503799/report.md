# heap-buffer-overflow in ANGLE VertexArrayVk::convertVertexBufferCPU

| Field | Value |
|-------|-------|
| **Issue ID** | [496503799](https://issues.chromium.org/issues/496503799) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU>ANGLE |
| **Platforms** | Linux, ChromeOS |
| **Reporter** | ki...@gmail.com |
| **Assignee** | cc...@google.com |
| **Created** | 2026-03-26 |
| **Bounty** | $16,000.00 |

## Description

# VULNERABILITY DETAILS

A heap-buffer-overflow exists in the ANGLE Vulkan backend's CPU-side vertex format conversion path. When a partial buffer update (via `bufferSubData`) dirties only a small range of a large vertex buffer, the subsequent `convertVertexBufferCPU` function computes the copy length using the total buffer capacity instead of the dirty range size, causing an out-of-bounds write into the conversion buffer.

In `convertVertexBufferCPU`, when the conversion buffer is not entirely dirty, the function iterates over dirty ranges [0]:

```
        const std::vector<RangeDeviceSize> &dirtyRanges = conversion->getDirtyBufferRanges();
        for (const RangeDeviceSize &dirtyRange : dirtyRanges) // [0]
        {
            if (dirtyRange.empty())
            {
                // consolidateDirtyRanges may end up with invalid range if it gets merged.
                continue;
            }

            uint32_t srcOffset, dstOffset, numVertices;
            CalculateOffsetAndVertexCountForDirtyRange(srcBuffer, conversion, srcFormat, dstFormat,
                                                       dirtyRange, &srcOffset, &dstOffset,
                                                       &numVertices);

            if (numVertices > 0)
            {
                const uint8_t *srcBytes = src + srcOffset;
                size_t bytesToCopy      = maxNumVertices * dstFormat.pixelBytes; // [1]
                ANGLE_TRY(StreamVertexData(contextVk, conversion->getBuffer(), srcBytes, // [2]
                                           bytesToCopy, dstOffset, maxNumVertices, srcStride,
                                           vertexLoadFunction));
            }
        }

```

`CalculateOffsetAndVertexCountForDirtyRange` computes `dstOffset` based on where the dirty range begins within the buffer — when the dirty range is near the end of the buffer, `dstOffset` points near the end of the conversion buffer.

However, `bytesToCopy` at [1] is computed from `maxNumVertices`, which represents the total vertex count derived from the *entire* buffer capacity. The conversion buffer is allocated with exactly `maxNumVertices * dstFormat.pixelBytes` bytes. When `StreamVertexData` is called at [2], `vertexLoadFunction` copies `maxNumVertices` vertices starting from `dstOffset` into the conversion buffer, writing far past the buffer's end.

`StreamVertexData` writes directly to the destination buffer at the given offset [3]:

```
    uint8_t *dst = dstBufferHelper->getMappedMemory() + dstOffset;

    if (vertexLoadFunction != nullptr)
    {
        vertexLoadFunction(srcData, srcStride, vertexCount, dst); // [3]
    }

```

The conversion buffer is allocated with `maxNumVertices * dstStride` bytes via `CalculateMaxVertexCountForConversion` [4]:

```
    ANGLE_TRY(contextVk->initBufferForVertexConversion(conversion, maxNumVertices * dstStride, // [4]
                                                       hostVisible));

```

So when `dstOffset` is near the end and the copy length equals the full buffer size, the write overflows the conversion buffer heap allocation.

To reach the vulnerable CPU conversion path, the vertex attribute stride or offset must be unaligned with the format's component size, causing `bindingIsAligned` to evaluate to false. This triggers the CPU fallback path in `syncNeedsConversionAttrib` [5]:

```
        if (bindingIsAligned)
        {
            ANGLE_TRY(
                convertVertexBufferGPU(contextVk, bufferVk, conversion, srcFormat, dstFormat));
        }
        else
        {
            ANGLE_VK_PERF_WARNING(contextVk, GL_DEBUG_SEVERITY_HIGH,
                                  "GPU stall due to vertex format conversion of unaligned data");

            ANGLE_TRY(convertVertexBufferCPU(contextVk, bufferVk, conversion, srcFormat, dstFormat, // [5]
                                             vertexFormat.getVertexLoadFunction()));
        }

```

WebGL contexts enforce stride/offset alignment via `ValidateWebGLVertexAttribPointer`, blocking this path. However, a compromised renderer can request an `OPENGLES2` context type instead of `CONTEXT_TYPE_WEBGL1/2` when creating the GPU command buffer — `CONTEXT_TYPE_OPENGLES2` is a legitimate context type that is fully supported by the IPC serialization layer and GPU service. With `isWebGL()` returning false, the alignment validation is bypassed, and unaligned stride/offset values reach the Vulkan backend.

[0] <https://source.chromium.org/chromium/chromium/src/+/main:third_party/angle/src/libANGLE/renderer/vulkan/VertexArrayVk.cpp;drc=216f1f0264f2b729c45c6aa7a038dc592c4551cc;l=850>

[1] <https://source.chromium.org/chromium/chromium/src/+/main:third_party/angle/src/libANGLE/renderer/vulkan/VertexArrayVk.cpp;drc=216f1f0264f2b729c45c6aa7a038dc592c4551cc;l=866>

[2] <https://source.chromium.org/chromium/chromium/src/+/main:third_party/angle/src/libANGLE/renderer/vulkan/VertexArrayVk.cpp;drc=216f1f0264f2b729c45c6aa7a038dc592c4551cc;l=867>

[3] <https://source.chromium.org/chromium/chromium/src/+/main:third_party/angle/src/libANGLE/renderer/vulkan/VertexArrayVk.cpp;drc=216f1f0264f2b729c45c6aa7a038dc592c4551cc;l=236>

[4] <https://source.chromium.org/chromium/chromium/src/+/main:third_party/angle/src/libANGLE/renderer/vulkan/VertexArrayVk.cpp;drc=216f1f0264f2b729c45c6aa7a038dc592c4551cc;l=370>

[5] <https://source.chromium.org/chromium/chromium/src/+/main:third_party/angle/src/libANGLE/renderer/vulkan/VertexArrayVk.cpp;drc=216f1f0264f2b729c45c6aa7a038dc592c4551cc;l=1323>

# BISECTION

Introduced by ANGLE commit [0] which added fine-grained dirty range tracking for vertex buffer conversion but incorrectly used the full-buffer vertex count (`maxNumVertices`) instead of the dirty-range vertex count (`numVertices`) when computing the copy size.

This was rolled into Chromium in commit [1].

[0] <https://chromium.googlesource.com/angle/angle/+/53476d6ff2740267db0c0573644378621c4e7d78>

[1] <https://chromium.googlesource.com/chromium/src/+/2580fab69bf8f219b97a3e812122dca566c525e0>

# VERSION

Chrome Version: HEAD

Operating System: Linux

# REPRODUCTION CASE

This vulnerability requires a compromised renderer. The attached `renderer.patch` modifies the renderer process to request `CONTEXT_TYPE_OPENGLES2` instead of WebGL context types, bypassing WebGL alignment checks.

1. Apply the renderer patch and build Chromium with ASan.
2. Host `poc.html` on an HTTP server.
3. Run Chrome against the PoC.

```
$ git apply renderer.patch && autoninja -C out/asan chrome
$ python3 -m http.server
$ ./out/asan/chrome --use-angle=vulkan "http://localhost:8000/poc.html"

```
# CRASH INFORMATION

Type of crash: GPU process

Crash log: see the attached `asan.txt` ASan trace.

# CREDIT INFORMATION

Reporter credit: Anonymous

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 17.8 KB)
- [poc.html](attachments/poc.html) (text/html, 4.0 KB)
- [renderer.patch](attachments/renderer.patch) (text/x-diff, 773 B)
- [renderer_new.patch](attachments/renderer_new.patch) (text/x-diff, 1.3 KB)

## Timeline

### ki...@gmail.com (2026-03-27)

To avoid ambiguity, as the previous patch might have been interpreted as a modification to the GPU service, I have updated it with a new version that only modifies the renderer (two patches are essentially the same).

### wf...@chromium.org (2026-03-27)

aha you already answered the question I was going to ask :) thank you.

### wf...@chromium.org (2026-03-27)

I have no reproduced this yet, but the poc seems very reasonable, the asan stack seems valid, and the patch is valid (renderer only) so I am triaging this as a Sev-High security issue, and will pass to the development team.

### wf...@chromium.org (2026-03-27)

I think since this is vulkan backend that only linux and chromeos are vulnerable but reporter please can you confirm?

### sy...@chromium.org (2026-03-28)

Charlie's agreed to take a look at this. Thank you!

### ki...@gmail.com (2026-03-28)

Re #4
I don't have a convenient environment on other platforms to test this. I believe only Linux and ChromeOS are affected by default. However, on other platforms, it should also be affected if it falls back to software rendering (SwiftShader) or if --use-angle=vulkan is manually specified.

### ch...@google.com (2026-03-28)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-03-28)

Setting Priority to P1 to match Severity s1. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### dx...@google.com (2026-03-31)

Project: angle/angle  

Branch:  main  

Author:  Charlie Lao [cclao@google.com](mailto:cclao@google.com)  

Link:    <https://chromium-review.googlesource.com/7712217>

Vulkan: Fix heap-buffer-overflow in convertVertexBufferCPU

---


Expand for full commit details
```
     
    There was a bug in vulkan backend 
    VertexArrayVk::convertVertexBufferCPU() that it streams more data than 
    buffer it allocates. A test has been added to expose the 
    heap-buffer-overflow bug. The bug is also fixed in the CL. 
     
    Bug: b/496503799 
    Change-Id: I79f8619699a9c82ea7d35e4849edfb91866c3623 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7712217 
    Reviewed-by: Amirali Abdolrashidi <abdolrashidi@google.com> 
    Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org> 
    Commit-Queue: Charlie Lao <cclao@google.com>

```

---

Files:

- M `src/libANGLE/renderer/vulkan/VertexArrayVk.cpp`
- M `src/tests/angle_end2end_tests_expectations.txt`
- M `src/tests/gl_tests/BufferDataTest.cpp`

---

Hash: [a96c6e3e7e3abb396109be762c06c2b2784fbde7](https://chromiumdash.appspot.com/commit/a96c6e3e7e3abb396109be762c06c2b2784fbde7)  

Date: Mon Mar 30 19:01:45 2026


---

### ch...@google.com (2026-04-01)

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

### dr...@chromium.org (2026-04-01)

We don't plan any more M146 releases, so removing that merge label. Will consider for M147 merge once this has been in Canary 24 hours.

### dr...@chromium.org (2026-04-03)

No crashes in Canary after 24 hours, approved to merge to M147.

### ch...@google.com (2026-04-07)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2026-04-11)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### sp...@google.com (2026-04-23)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $16000.00 for this report.

Rationale for this decision:
High Quality with Bisect. Memory corruption in a highly privileged process (e.g. GPU, network processes) 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-07-08)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/496503799)*
