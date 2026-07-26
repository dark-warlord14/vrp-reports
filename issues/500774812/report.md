# heap-buffer-overflow in Dawn BufferGL::MapAtCreationImpl

| Field | Value |
|-------|-------|
| **Issue ID** | [500774812](https://issues.chromium.org/issues/500774812) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | Dawn |
| **Platforms** | Android |
| **Reporter** | ki...@gmail.com |
| **Assignee** | ka...@google.com |
| **Created** | 2026-04-09 |
| **Bounty** | $33,000.00 |

## Description

# VULNERABILITY DETAILS

A heap out-of-bounds write vulnerability exists in the Dawn OpenGL backend when handling buffer mapping at creation (`MapAtCreationImpl`) with `Toggle::GLDefer` enabled.

The root cause resides in a size discrepancy between the logical buffer size (`GetSize()`) and the underlying physical allocation size (`GetAllocatedSize()`). When creating a buffer with `wgpu::BufferUsage::Uniform`, `BufferGL` forces a 16-byte alignment on the allocated size [0]:

```
    uint64_t alignment = 4u;
    // Round uniform buffer sizes up to a multiple of 16 bytes since Tint will polyfill them as
    // array<vec4u, ...>.
    if (GetUsage() & wgpu::BufferUsage::Uniform) {
        alignment = 16u;
    }
    mAllocatedSize = Align(std::max(GetSize(), uint64_t(4u)), alignment); // [0]

```

Later, when `mappedAtCreation` is `true`, `BufferGL::MapAtCreationImpl` is invoked. If the `Toggle::GLDefer` is active, the backend defers OpenGL mapping operations and instead backs the buffer with a staging `std::vector` (`mCPUStaging`). However, it allocates this staging vector using the smaller logical size `GetSize()`, rather than the aligned `mAllocatedSize` [1]:

```
MaybeError Buffer::MapAtCreationImpl() {
    auto device = ToBackend(GetDevice());
    if (device->IsToggleEnabled(Toggle::GLDefer)) {
        mCPUStaging.resize(GetSize()); // [1]
        mMappedData = mCPUStaging.data();
        return {};
    }

```

Immediately after `MapAtCreationImpl` returns successfully, the frontend `dawn::native::BufferBase::MapAtCreation` attempts to initialize the mapped memory using `memset`. It incorrectly uses the larger `GetAllocatedSize()` for the zero-fill length [2].

```
    size_t size = GetAllocatedSize();
    void* ptr = GetMappedPointer();

    DeviceBase* device = GetDevice();
    if (device->IsToggleEnabled(Toggle::LazyClearResourceOnFirstUse) &&
        !device->IsToggleEnabled(Toggle::DisableLazyClearForMappedAtCreationBuffer)) {
        // The staging buffer is created with `MappedAtCreation == true` and the main buffer will
        // actually get initialized when the staging data is copied in. (But we mark the main buffer
        // as initialized now.)
        if (!usingStagingBuffer) {
            memset(ptr, uint8_t(0u), size); // [2]
            device->IncrementLazyClearCountForTesting();
        }

```

By requesting a buffer with an unaligned size that is a multiple of 4 (e.g., `4004`), the frontend validation checks pass. `GetSize()` will be `4004`, while `GetAllocatedSize()` will be rounded up to `4016` (due to the `Uniform` 16-byte alignment). `std::vector::resize` allocates exactly `4004` bytes space on the heap. The `memset` then writes `4016` bytes of zeroes into the heap buffer, resulting in an out-of-bounds write of 12 bytes.

[0] <https://source.chromium.org/chromium/chromium/src/+/main:third_party/dawn/src/dawn/native/opengl/BufferGL.cpp;drc=90c0abf9d97868ddecb9cede383b5f4f25bf7e91;l=107>

[1] <https://source.chromium.org/chromium/chromium/src/+/main:third_party/dawn/src/dawn/native/opengl/BufferGL.cpp;drc=90c0abf9d97868ddecb9cede383b5f4f25bf7e91;l=208>

[2] <https://source.chromium.org/chromium/chromium/src/+/main:third_party/dawn/src/dawn/native/Buffer.cpp;drc=90c0abf9d97868ddecb9cede383b5f4f25bf7e91;l=602>

# BISECTION

Introduced by Dawn upstream commit [0] which added the `Toggle::GLDefer` deferred GL backend logic and incorrectly used `GetSize()`.

This regression was rolled into Chromium in commit [1].

[0] <https://dawn.googlesource.com/dawn.git/+/bdea3d0e47c9c28c8ed405af6fc2e9eab9426eab> (OpenGL backend: implement deferred GL calls)

[1] <https://chromium.googlesource.com/chromium/src/+/b58dbf3a32e04be3f3dcddf69ce9f732f5a643db> (Roll Dawn from f9a0941385f4 to 05dc9c2bdab3 (33 revisions))

# VERSION

Chrome Version: HEAD

Operating System: Linux

# REPRODUCTION CASE

1. Build Chromium with Asan.
2. Host the `poc.html` on an HTTP server.
3. Run Chrome against the PoC.

```
$ python3 -m http.server
$ ./out/asan/chrome --use-webgpu-adapter=opengles --force-webgpu-compat --enable-dawn-features=gl_defer "http://localhost:8000/poc.html"

```
# CRASH INFORMATION

Type of crash: GPU process

Crash log: see the attached `asan.txt` ASan trace.

# SUGGESTED FIX

Update `MapAtCreationImpl` to resize the staging vector based on `GetAllocatedSize()` instead of `GetSize()`.

See `fix.patch` for details.

# CREDIT INFORMATION

Reporter credit: Anonymous

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 17.9 KB)
- [poc.html](attachments/poc.html) (text/html, 809 B)
- [fix.patch](attachments/fix.patch) (text/x-diff, 571 B)

## Timeline

### pe...@google.com (2026-04-09)

@ka...@chromium.org Stephen is out. Who is next in line to look at GL vulns?

### pe...@google.com (2026-04-09)

in reality our allocators probably do not allow for lower alignments than 16 bytes for memory allocations. This bug might simply stomp allocated memory.

### ka...@chromium.org (2026-04-10)

gl\_defer is not enabled by default (and the renderer process cannot enable it). AFAICT it is only intended for multithreaded usage from Graphite ([bug 451928481](https://issues.chromium.org/issues/451928481)). We should fix this but I believe it has no security impact.

### ka...@chromium.org (2026-04-11)

I think this bug exists in the non-GLDefer codepath too.

### ka...@chromium.org (2026-04-11)

M135 for WebGPU Compatibility Mode origin trial. M146 for actually shipping WebGPU Compatibility Mode.

The origin trial is still active. ~~If we merge this back, a note: I'm not sure if origin trials are allowed in LTS, but if so, we can just turn off the origin trial rather than merge back to LTS.~~ Never mind, LTS is a ChromeOS and we haven't shipped the GLES backend on ChromeOS.

That said the impact is probably small here because the overflow is only 12 bytes (end of array up to the next multiple of 16) and I think in practice there can probably never actually be anything allocated there?

### ka...@chromium.org (2026-04-11)

Actually the origin trial [ends in 10 days](https://developer.chrome.com/origintrials/#/view_trial/1489002626799370241) anyway.

### ka...@chromium.org (2026-04-11)

I am pretty confident this DOES exist without GLDefer, just unfortunately it's difficult to catch in the non-GLDefer case (when the mapping comes from the GL driver instead of a regular allocation). For example when running on ANGLE on SwiftShader, SwiftShader sub-allocates the memory from some larger region, or something like that, that prevents ASan from catching it. But if I just print the glMapBufferRange size and the memset size, it definitely overflows.

### dx...@google.com (2026-04-11)

Project: dawn  

Branch:  main  

Author:  Kai Ninomiya [kainino@chromium.org](mailto:kainino@chromium.org)  

Link:    <https://dawn-review.googlesource.com/302195>

[dawn][opengl] Fix size of MappedAtCreation mapping

---


Expand for full commit details
```
     
    The updated test catches this with ASan in the case where GLDefer is 
    enabled (which it does) but the bug also exists in the non-GLDefer case. 
    Just can't catch it with ASan. 
     
    There isn't an equivalent issue in the non-MappedAtCreation case because 
    the buffer is initialized from the GPU (even if it's mappable, though in 
    that case the usage can't have Uniform anyway so the size isn't rounded 
    up). 
     
    Fixes: 500774812 
    Change-Id: Iaf7f4b8ee5b69c4f5a41f39d10d2cce9cfd983e5 
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/302195 
    Commit-Queue: Kai Ninomiya <kainino@chromium.org> 
    Auto-Submit: Kai Ninomiya <kainino@chromium.org> 
    Reviewed-by: Quyen Le <lehoangquyen@chromium.org>

```

---

Files:

- M `src/dawn/native/opengl/BufferGL.cpp`
- M `src/dawn/tests/end2end/BufferTests.cpp`

---

Hash: 493241c40dc94ca283c5e2b42a03911df870f359  

Date: Sat Apr 11 06:37:14 2026


---

### ch...@google.com (2026-04-11)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-04-11)

This is sufficiently serious that it should be merged to M146. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M146. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Security Merge Request:

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

This is sufficiently serious that it should be merged to M147. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M147. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to M148. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M148. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

### ch...@google.com (2026-04-11)

**M146** merge request created. **Please update [crbug/501628822](https://crbug.com/501628822) to have this merge reviewed.**

### ch...@google.com (2026-04-11)

**M147** merge request created. **Please update [crbug/501627927](https://crbug.com/501627927) to have this merge reviewed.**

### ch...@google.com (2026-04-11)

**M148** merge request created. **Please update [crbug/501628330](https://crbug.com/501628330) to have this merge reviewed.**

### dx...@google.com (2026-04-17)

Project: dawn  

Branch:  chromium/7680  

Author:  Kai Ninomiya [kainino@chromium.org](mailto:kainino@chromium.org)  

Link:    <https://dawn-review.googlesource.com/303196>

[M146] [dawn][opengl] Fix size of MappedAtCreation mapping

---


Expand for full commit details
```
     
    Clean cherry-pick, except that the GLDefer case didn't exist in M146 so 
    the code here changed a bit. 
     
    > The updated test catches this with ASan in the case where GLDefer is 
    > enabled (which it does) but the bug also exists in the non-GLDefer case. 
    > Just can't catch it with ASan. 
    > 
    > There isn't an equivalent issue in the non-MappedAtCreation case because 
    > the buffer is initialized from the GPU (even if it's mappable, though in 
    > that case the usage can't have Uniform anyway so the size isn't rounded 
    > up). 
     
    Fixes: 500774812 
    Change-Id: Iaf7f4b8ee5b69c4f5a41f39d10d2cce9cfd983e5 
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/302195 
    Commit-Queue: Kai Ninomiya <kainino@chromium.org> 
    Auto-Submit: Kai Ninomiya <kainino@chromium.org> 
    Reviewed-by: Quyen Le <lehoangquyen@chromium.org> 
    (cherry picked from commit 493241c40dc94ca283c5e2b42a03911df870f359) 
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/303196 
    Reviewed-by: Brandon Jones <bajones@chromium.org> 
    Commit-Queue: Brandon Jones <bajones@chromium.org>

```

---

Files:

- M `src/dawn/native/opengl/BufferGL.cpp`
- M `src/dawn/tests/end2end/BufferTests.cpp`

---

Hash: a39aaa3e1e2095d9f45d9d97eee4abeae2c563f4  

Date: Fri Apr 17 21:46:47 2026


---

### sp...@google.com (2026-04-22)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $33000.00 for this report.

Rationale for this decision:
Baseline with bisect. Memory corruption in a highly privileged process (e.g. GPU, network processes) 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-07-19)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/500774812)*
