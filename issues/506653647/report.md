# WebGL Memory Corruption via Passthrough Decoder Bound Buffers Cache Desync

| Field | Value |
|-------|-------|
| **Issue ID** | [506653647](https://issues.chromium.org/issues/506653647) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | h2...@gmail.com |
| **Assignee** | kb...@google.com |
| **Created** | 2026-04-26 |
| **Bounty** | $35,000.00 |

## Description

# VULNERABILITY DETAILS

This is a use-after-free vulnerability in the passthrough command decoder of the WebGL imlpementation, reachable from a compromised renderer, resulting in memory corruption in the GPU process of Chrome.

The root cause is a missing cache-invalidation flag set in the passthrough GLES2 decode. The exact consequences of this and the crash signature depends on the ANGLE backend/driver, but on the configurations I tested it gives a memcpy targeting a stale pointer to a GPU memory allocation.

`GLES2DecoderPassthroughImpl::bound_buffers_` is a map of the current client buffer ID per target, avoiding per-Map/Unmap `glGetIntegerv` round-trips. For `GL_ELEMENT_ARRAY_BUFFER` specifically, the cache has a lazy update mechanism because the ELEMENT\_ARRAY binding is per-VAO state ([OpenGL ES 3.0.6 2.11 + Table 6.2 "Vertex Array Object State"](https://registry.khronos.org/OpenGL/specs/es/3.0/es_spec_3.0.pdf)) and some GL operations change it as a side effect rather than via an explicit `glBindBuffer`. For this caching to work, the invariant should hold: before any decoder consumer reads `bound_buffers_[GL_ELEMENT_ARRAY_BUFFER]`, either the cache has already been updated to match the driver, or `bound_element_array_buffer_dirty_` is set so the next `LazilyUpdateCurrentlyBoundElementArrayBuffer()` call refreshes it.

The `DoDeleteVertexArraysOES` implementation of ANGLE breaks that invariant. Per [OpenGL ES 3.0.6 2.11 "Vertex Array Objects"](https://registry.khronos.org/OpenGL/specs/es/3.0/es_spec_3.0.pdf), `If a vertex array object that is currently bound is deleted, the binding for that object reverts to zero and the default vertex array becomes current`. While the other GLES functions that may have similar side-effect correctly set `bound_element_array_buffer_dirty_`, `DoDeleteVertexArraysOES` does not.

A compromised renderer can exploit this as follows (relevant code snippets shown below):

1. Prime VAO0's ELEMENT\_ARRAY with `buf_0` (a 16 MB buffer, size chosen so that ANGLE will allocate it standalone rather than suballocating it from a shared slab).
2. Switch to a non-default VAO, bind `buf_1` to that VAO's ELEMENT\_ARRAY. At this point the service's `bound_buffers_[GL_ELEMENT_ARRAY_BUFFER]` is `buf_1`.
3. Delete the non-default VAO. The driver's ELEMENT\_ARRAY reverts to `buf_0` (per spec) but decoder's cache still says `buf_1` and the dirty flag is not set.
4. Call `MapBufferRange(GL_ELEMENT_ARRAY_BUFFER, 0, 16 MB, GL_MAP_WRITE_BIT | GL_MAP_INVALIDATE_BUFFER_BIT)`. The driver maps `buf_0` and returns `ptr_A`. The decoder's lazy-refresh early-exits on `bound_element_array_buffer_dirty_==false`, so it reads the stale `bound_buffers_[GL_ELEMENT_ARRAY_BUFFER]`, `buf_1` and inserts `buf_1 => { map_ptr = ptr_A, size = 16 MB, shm_id, shm_offset, WRITE|INVALIDATE_BUFFER }` into `resources_->mapped_buffer_map`. The key refers to `buf_1` but the stored pointer refers to the mapped `buf_0`.
5. Fill the returned shared-memory pointer with controlled bytes.
6. Bind `buf_1` to ELEMENT\_ARRAY on the client side, then issue a tiny `MapBufferRange(GL_ELEMENT_ARRAY_BUFFER, 0, 1, WRITE|INVALIDATE_RANGE)`: this populates the client-side `GLES2Implementation::mapped_buffer_range_map_[buf_1]` so that the later client-side `UnmapBuffer` validation accepts the call. This wouldn't strictly be necessary if the PoC used the command buffer directly. In `GLES2DecoderPassthroughImpl::DoMapBufferRange`, `std::map::insert` returns `{existing_iter, false}` on the duplicate key and silently drops the new record, so this is effectively a no-op on the service side. In DCHECK-enabled builds this is where the PoC aborts, on the `DCHECK(mapped_buffer_map.find(client_buffer) == end())` at `passthrough_doers.cc:4007-4008`.
7. `DeleteBuffers(buf_0)`. Because the 16 MB allocation was standalone (not suballocated), ANGLE's garbage machinery synchronously calls `vkDestroyBuffer` + `vkFreeMemory` from the same decoder thread that processed DeleteBuffers. `ptr_A` is now dangling.
8. `UnmapBuffer(GL_ELEMENT_ARRAY_BUFFER)`. The decoder looks up `bound_buffers_[GL_ELEMENT_ARRAY_BUFFER]`, which is  `buf_1`, finds the `mapped_buffer_map` entry from step 4 with the now-dangling `ptr_A`, and executes `memcpy(ptr_A, shm /*attacker bytes*/, 16 MB)` at `passthrough_doers.cc:4048`.

## Relevant Code Paths

`DoDeleteVertexArraysOES` in [gles2\_cmd\_decoder\_passthrough\_doers.cc:3916-3923](https://source.chromium.org/chromium/chromium/src/+/main:gpu/command_buffer/service/gles2_cmd_decoder_passthrough_doers.cc;l=3916;bpv=1;bpt=0) does not set `bound_element_array_buffer_dirty_ = true`:

```
error::Error GLES2DecoderPassthroughImpl::DoDeleteVertexArraysOES(
    GLsizei n,
    const volatile GLuint* arrays) {
    return DeleteHelper(n, arrays, &vertex_array_id_map_,
                      [this](GLsizei n, GLuint* arrays) {
                        api()->glDeleteVertexArraysOESFn(n, arrays);
                      });
}

```

For contrast, `DoBindVertexArrayOES` at [passthrough\_doers.cc:3932-3937](https://source.chromium.org/chromium/chromium/src/+/main:gpu/command_buffer/service/gles2_cmd_decoder_passthrough_doers.cc;l=3932;bpv=1;bpt=0) sets it.

```
error::Error GLES2DecoderPassthroughImpl::DoBindVertexArrayOES(GLuint array) {
  api()->glBindVertexArrayOESFn(
      GetVertexArrayServiceID(array, &vertex_array_id_map_));
  bound_element_array_buffer_dirty_ = true;              // correct pattern
  return error::kNoError;
}

```

If `bound_element_array_buffer_dirty_` is false, `LazilyUpdateCurrentlyBoundElementArrayBuffer` at [passthrough.cc:2593-2611](https://source.chromium.org/chromium/chromium/src/+/main:gpu/command_buffer/service/gles2_cmd_decoder_passthrough.cc;l=2593;bpv=1;bpt=0) returns early and `bound_buffers_[GL_ELEMENT_ARRAY_BUFFER]` retains its potentially stale value.

```
void GLES2DecoderPassthroughImpl::
    LazilyUpdateCurrentlyBoundElementArrayBuffer() {
  if (!bound_element_array_buffer_dirty_)
    return;                                              // early-exit
  GLint service_element_array_buffer = 0;
  api_->glGetIntegervFn(GL_ELEMENT_ARRAY_BUFFER_BINDING,
                        &service_element_array_buffer);
  GLuint client_element_array_buffer = 0;
  if (service_element_array_buffer != 0) {
    GetClientID(&resources_->buffer_id_map,
                static_cast<GLuint>(service_element_array_buffer),
                &client_element_array_buffer);
  }
  bound_buffers_[GL_ELEMENT_ARRAY_BUFFER] = client_element_array_buffer;
  bound_element_array_buffer_dirty_ = false;
}

```

At this point, invoking `MapBufferRange(GL_ELEMENT_ARRAY_BUFFER, 0, 16 MB, GL_MAP_WRITE_BIT | GL_MAP_INVALIDATE_BUFFER_BIT)` causes `DoMapBufferRange` at [passthrough\_doers.cc:3993-4013](https://source.chromium.org/chromium/chromium/src/+/main:gpu/command_buffer/service/gles2_cmd_decoder_passthrough_doers.cc;l=3993;bpv=1;bpt=0) to map `buf_0` but then insert that mapped pointer into `mapped_buffer_map` keyed by the stale `ELEMENT_ARRAY` in the cache, `buf_1`.

```
error::Error GLES2DecoderPassthroughImpl::DoMapBufferRange(
    GLenum target, GLintptr offset, GLsizeiptr size, GLbitfield access,
    void* ptr, int32_t data_shm_id, uint32_t data_shm_offset,
    uint32_t* result) {
  // ...
  // Maps buf_0
  void* mapped_ptr = api()->glMapBufferRangeFn(target, offset, size,
                                               filtered_access);
  // ...
  DCHECK(bound_buffers_.find(target) != bound_buffers_.end());
  if (target == GL_ELEMENT_ARRAY_BUFFER) {
    // No update because bound_element_array_buffer_dirty_ == false
    LazilyUpdateCurrentlyBoundElementArrayBuffer();
  }
  // STALE, client_buffer == buf_1
  GLuint client_buffer = bound_buffers_.at(target);

  MappedBuffer mapped_buffer_info;
  mapped_buffer_info.size = size;
  mapped_buffer_info.original_access = access;
  mapped_buffer_info.filtered_access = filtered_access;
  // ACTUAL mapped pointer of buf_0
  mapped_buffer_info.map_ptr = static_cast<uint8_t*>(mapped_ptr);
  mapped_buffer_info.data_shm_id = data_shm_id;
  mapped_buffer_info.data_shm_offset = data_shm_offset;

  DCHECK(resources_->mapped_buffer_map.find(client_buffer) ==
         resources_->mapped_buffer_map.end());
  resources_->mapped_buffer_map.insert(
      std::make_pair(client_buffer, mapped_buffer_info));
  *result = 1;
  return error::kNoError;
}

```

Now calling `DoDeleteBuffers` at [passthrough\_doers.cc:928-967](https://source.chromium.org/chromium/chromium/src/+/main:gpu/command_buffer/service/gles2_cmd_decoder_passthrough_doers.cc;l=928;bpv=1;bpt=0) with `buf_0` will remove the `mapped_buffer_map` entry for `buf_0` and actually free the backing allocation through the driver, while keeping the previously inserted entry for `buf_1` pointing to the same memory region.

```
error::Error GLES2DecoderPassthroughImpl::DoDeleteBuffers(
    GLsizei n,
    const volatile GLuint* buffers) {
  // ...
  // No update because bound_element_array_buffer_dirty_ == false
  LazilyUpdateCurrentlyBoundElementArrayBuffer();

  std::vector<GLuint> service_ids(n, 0);
  for (GLsizei ii = 0; ii < n; ++ii) {
    GLuint client_id = UNSAFE_TODO(buffers[ii]);              // = buf_0

    // Update the bound and mapped buffer state tracking
    for (auto& buffer_binding : bound_buffers_) {
      if (buffer_binding.second == client_id) {
        buffer_binding.second = 0;
      }
      resources_->mapped_buffer_map.erase(client_id);         // erases buf_0 only
    }

    service_ids[ii] =
        resources_->buffer_id_map.GetServiceIDOrInvalid(client_id);
    resources_->buffer_id_map.RemoveClientID(client_id);
    // ...
  }
  api()->glDeleteBuffersARBFn(n, service_ids.data());         // actual driver free
  return error::kNoError;
}

```

After this, calling `DoUnmapBuffer` at [passthrough\_doers.cc:4016-4056](https://source.chromium.org/chromium/chromium/src/+/main:gpu/command_buffer/service/gles2_cmd_decoder_passthrough_doers.cc;l=4016;bpv=1;bpt=0) with `GL_ELEMENT_ARRAY_BUFFER` skips the lazy update like the other functions because `bound_element_array_buffer_dirty_` is false. Then reads the stale `buf_1` id from `bound_buffers_` and finds the corresponing entry in `mapped_buffer_map`, which has the dangling `ptr_A` pointer, then memcpy's the contents of the shared memory region controlled by the renderer to `ptr_A`. The contents and the size of the write are both controlled here by the renderer.

```
error::Error GLES2DecoderPassthroughImpl::DoUnmapBuffer(GLenum target) {
  if (target == GL_ELEMENT_ARRAY_BUFFER) {
    // No update because bound_element_array_buffer_dirty_ == false
    LazilyUpdateCurrentlyBoundElementArrayBuffer();
  }
  auto bound_buffers_iter = bound_buffers_.find(target);
  // target/bound validation
  GLuint client_buffer = bound_buffers_iter->second;       // STALE
  auto mapped_buffer_info_iter =
      resources_->mapped_buffer_map.find(client_buffer);   // hits divergent entry
  if (mapped_buffer_info_iter == resources_->mapped_buffer_map.end()) {
    InsertError(GL_INVALID_OPERATION, "Buffer is not mapped.");
    return error::kNoError;
  }
  const MappedBuffer& map_info = mapped_buffer_info_iter->second;
  if ((map_info.filtered_access & GL_MAP_WRITE_BIT) != 0 &&
      (map_info.filtered_access & GL_MAP_FLUSH_EXPLICIT_BIT) == 0) {
    uint8_t* mem = GetSharedMemoryAs<uint8_t*>(
        map_info.data_shm_id, map_info.data_shm_offset, map_info.size);
    if (!mem) return error::kOutOfBounds;
    UNSAFE_TODO(memcpy(map_info.map_ptr, mem, map_info.size));  // L4048 — UAF/SEGV
  }
  api()->glUnmapBufferFn(target);
  resources_->mapped_buffer_map.erase(mapped_buffer_info_iter);
  return error::kNoError;
}

```

Below 8MB ANGLE sub-allocates out of a shared `BufferBlock` (one `vkAllocateMemory` call, reused for many client buffers); `DeleteBuffers` releases the sub-allocation but leaves the block's `VkDeviceMemory` alive. Above 8 MB each buffer gets its own `VkDeviceMemory` allocation that `DeleteBuffers` genuinely frees. This is purely an ANGLE constant and has the same value on every Vulkan backend Chrome ships.

`BufferSuballocationGarbage::destroyIfComplete` in [Suballocation.cpp:220-229](https://source.chromium.org/chromium/chromium/src/+/main:third_party/angle/src/libANGLE/renderer/vulkan/Suballocation.cpp;l=220;bpv=1;bpt=0)

```
bool BufferSuballocationGarbage::destroyIfComplete(Renderer *renderer) {
    if (renderer->hasResourceUseFinished(mLifetime)) {
        mBuffer.destroy(renderer->getDevice());
        mSuballocation.destroy(renderer);
        return true;
    }
    return false;
}

```

With no draw calls against the buffer, its `ResourceUse` is empty and `hasResourceUseFinished` is true, so ANGLE's garbage machinery calls `vkDestroyBuffer` + `vkFreeMemory` inline from the same decoder thread that processed `DoDeleteBuffers`. No explicit `glFinish` is needed for the free to retire before `DoUnmapBuffer`'s memcpy, though the PoC issues one anyway.

In current Chromium, no JS-reachable code path can drive this sequence: `WebGL2RenderingContextBase::getBufferSubData` is the only Blink caller of `MapBufferRange` and it always uses `GL_MAP_READ_BIT` and does Map+Unmap atomically per call, so the write memcpy is never reached from JS and the divergence cannot persist across calls. The attached renderer patch (`compromised_renderer.patch`) emulates a compromised renderer that has bypassed Blink's validation and issues the 17-op sequence directly.

# VERSION

Chrome Version: `149.0.7807.0` + dev (commit [`56162b7eb6dcf107cd6564598c28284a6983aecf`](https://source.chromium.org/chromium/chromium/src/+/56162b7eb6dcf107cd6564598c28284a6983aecf))

Operating System: Linux (Ubuntu 24.04, kernel 6.17.0-22-generic).

The issue is in the generic passthrough decoder of the Chromium WebGL implementation and thus present on all platforms. How it manifests depends on the GPU driver.

# REPRODUCTION CASE

GN args used for testing (`out/asan-rel-x64/args.gn`):

```
is_debug = false
is_asan = true
dcheck_always_on = false
is_component_build = false
treat_warnings_as_errors = false
symbol_level = 2

```

The attached renderer patch, `compromised_renderer.patch`, hijacks `WebGL2RenderingContextBase::getBufferSubData` when called with `target == 0xDEAD` to run the PoC sequence directly via `ContextGL()`. Normal `getBufferSubData` semantics are preserved for every other target value. No service-side code is modified.

Apply and build:

```
git apply compromised_renderer.patch
autoninja -C out/asan-rel-x64 chrome

```

I've included the crashing backtrace for SwiftShader, even though it's not enabled by default in Chrome anymore, for easy reproduction.

On SwiftShader, the PoC produces an ASan heap use-after-free report because SwiftShader backs `VkDeviceMemory` with `sw::allocateZeroOrPoison` -> `malloc()` ([swiftshader/src/System/Memory.cpp:76](https://source.chromium.org/chromium/chromium/src/+/main:third_party/swiftshader/src/System/Memory.cpp;l=76;bpv=1;bpt=0), [VkDeviceMemory.cpp:342-354](https://source.chromium.org/chromium/chromium/src/+/main:third_party/swiftshader/src/Vulkan/VkDeviceMemory.cpp;l=342;bpv=1;bpt=0)) and `vkFreeMemory` -> `free()`. The freed region stays mapped in the process address space but ASan has poisoned its shadow, so the decoder's 16 MB write into the dangling `map_ptr` is caught as `WRITE of size 16777216` at `passthrough_doers.cc:4048`. To reproduce on SwiftShader:

```
./chrome  --no-sandbox -use-angle=swiftshader --use-vulkan=swiftshader --enable-unsafe-swiftshader --enable-logging=stderr /data/poc/poc.html

```

See `swiftshader_bt.txt` for the full crash log.

Running the same PoC on an NVIDIA GPU results in a different crash. On native NVIDIA Vulkan the kernel-side driver maps host-visible `VkDeviceMemory` into the process via `mmap` and `vkFreeMemory` tears the mapping down, so the decoder's 16 MB write into the dangling `map_ptr` hits an unmapped page and Chrome's signal handler prints a raw `Received signal 11 SEGV_MAPERR`. To reproduce on NVIDIA:

```
./chrome --no-sandbox --use-gl=angle --use-angle=vulkan --enable-logging=stderr /data/poc/poc.html

```

See `nvidia_bt.txt`, verified on a GeForce RTX 2060, driver 580.126.09, Vulkan 1.4.312.

The bug itself is entirely driver-independent, the decoder-side memcpy is at the same `passthrough_doers.cc:4048` with the same `map_ptr` source in both runs. What differs between backends is only what `vkFreeMemory` does to the host mapping of the freed `VkDeviceMemory`.

# FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION

Type of crash: GPU process crash

Crash State: see `nvidia_bt.txt` and `swiftshader_bt.txt`

# CREDIT INFORMATION

Reporter credit: TFGC

## Attachments

- [compromised_renderer.patch](attachments/compromised_renderer.patch) (text/x-diff, 4.6 KB)
- [swiftshader_bt.txt](attachments/swiftshader_bt.txt) (text/plain, 45.0 KB)
- [nvidia_bt.txt](attachments/nvidia_bt.txt) (text/plain, 7.4 KB)
- [poc.html](attachments/poc.html) (text/html, 952 B)
- [updated_compromised_renderer.patch](attachments/updated_compromised_renderer.patch) (text/x-diff, 4.9 KB)

## Timeline

### h2...@gmail.com (2026-04-27)

Just noticed that <https://chromium-review.googlesource.com/c/angle/angle/+/7782484> breaks the PoC (but doesn't fix this issue). Here's an updated version of the renderer patch to work around that. Reproduction instructions still the same, just apply `updated_compromised_renderer.patch` instead of `compromised_renderer.patch`.

Updated patch tested on 82f18666452ae40287871b21538cbe80f8caacfa

### ka...@google.com (2026-04-29)

Looks like large uncontrolled UAF in GPU process, only accessible from compromised renderer. S1

### ka...@google.com (2026-04-29)

Sounds unlikely to have been a regression, so probably 144 which is the current LTS, but setting to 100 for good measure

### ch...@google.com (2026-04-29)

Setting milestone because of s0/s1 severity.

### dx...@google.com (2026-05-18)

Project: chromium/src  

Branch:  main  

Author:  Ken Russell [kbr@chromium.org](mailto:kbr@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7853561>

Dirty bound element array buffer in DoDeleteVertexArraysOES.

---


Expand for full commit details
```
     
    In the passthrough command decoder. Add a unit test from the bug 
    report, verified with ASAN to fix the bug. 
     
    Co-authored with jetski-cli. 
     
    Fixed: 506653647 
    Change-Id: Ie133e85e6babd6da16889728e5f0e97af2ce489c 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7853561 
    Reviewed-by: Zhenyao Mo <zmo@chromium.org> 
    Commit-Queue: Zhenyao Mo <zmo@chromium.org> 
    Auto-Submit: Kenneth Russell <kbr@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1632304}

```

---

Files:

- M `gpu/BUILD.gn`
- M `gpu/command_buffer/service/gles2_cmd_decoder_passthrough_doers.cc`
- A `gpu/command_buffer/tests/gl_vertex_arrays_unittest.cc`

---

Hash: [6944e2581ee7a67bc4f4b7c1d6a6b720097ba4e2](https://chromiumdash.appspot.com/commit/6944e2581ee7a67bc4f4b7c1d6a6b720097ba4e2)  

Date: Mon May 18 18:37:07 2026


---

### ch...@google.com (2026-05-20)

Requesting merge to M148 because latest trunk commit is in 150.

Security Merge Request:

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Requesting merge to M149 because latest trunk commit is in 150.

### ch...@google.com (2026-05-20)

**M148** merge request created. **Please update [crbug/514926870](https://crbug.com/514926870) to have this merge reviewed.**

### ch...@google.com (2026-05-20)

**M149** merge request created. **Please update [crbug/514929858](https://crbug.com/514929858) to have this merge reviewed.**

### dx...@google.com (2026-05-22)

Project: chromium/src  

Branch:  refs/branch-heads/7827  

Author:  Ken Russell [kbr@chromium.org](mailto:kbr@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7868495>

[M149] Dirty bound element array buffer in DoDeleteVertexArraysOES.

---


Expand for full commit details
```
     
    Original change's description: 
    > Dirty bound element array buffer in DoDeleteVertexArraysOES. 
    > 
    > In the passthrough command decoder. Add a unit test from the bug 
    > report, verified with ASAN to fix the bug. 
    > 
    > Co-authored with jetski-cli. 
    > 
    > Fixed: 506653647 
    > Change-Id: Ie133e85e6babd6da16889728e5f0e97af2ce489c 
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7853561 
    > Reviewed-by: Zhenyao Mo <zmo@chromium.org> 
    > Commit-Queue: Zhenyao Mo <zmo@chromium.org> 
    > Auto-Submit: Kenneth Russell <kbr@chromium.org> 
    > Cr-Commit-Position: refs/heads/main@{#1632304} 
     
    (cherry picked from commit 6944e2581ee7a67bc4f4b7c1d6a6b720097ba4e2) 
     
    Bug: 514929858,506653647 
    Change-Id: Ie133e85e6babd6da16889728e5f0e97af2ce489c 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7868495 
    Bot-Commit: rubber-stamper@appspot.gserviceaccount.com <rubber-stamper@appspot.gserviceaccount.com> 
    Auto-Submit: chrome-cherry-picker@chops-service-accounts.iam.gserviceaccount.com <chrome-cherry-picker@chops-service-accounts.iam.gserviceaccount.com> 
    Commit-Queue: rubber-stamper@appspot.gserviceaccount.com <rubber-stamper@appspot.gserviceaccount.com> 
    Cr-Commit-Position: refs/branch-heads/7827@{#1520} 
    Cr-Branched-From: 9f3e9aaccba63bd2ec30334e45e0bfd07ebcc8f1-refs/heads/main@{#1625079}

```

---

Files:

- M `gpu/BUILD.gn`
- M `gpu/command_buffer/service/gles2_cmd_decoder_passthrough_doers.cc`
- A `gpu/command_buffer/tests/gl_vertex_arrays_unittest.cc`

---

Hash: [5a74559606c40466150a209d5a3941b947c61a47](https://chromiumdash.appspot.com/commit/5a74559606c40466150a209d5a3941b947c61a47)  

Date: Fri May 22 20:43:02 2026


---

### pe...@google.com (2026-05-22)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### dx...@google.com (2026-05-22)

Project: chromium/src  

Branch:  refs/branch-heads/7778  

Author:  Ken Russell [kbr@chromium.org](mailto:kbr@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7869574>

[M148] Dirty bound element array buffer in DoDeleteVertexArraysOES.

---


Expand for full commit details
```
     
    Original change's description: 
    > Dirty bound element array buffer in DoDeleteVertexArraysOES. 
    > 
    > In the passthrough command decoder. Add a unit test from the bug 
    > report, verified with ASAN to fix the bug. 
    > 
    > Co-authored with jetski-cli. 
    > 
    > Fixed: 506653647 
    > Change-Id: Ie133e85e6babd6da16889728e5f0e97af2ce489c 
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7853561 
    > Reviewed-by: Zhenyao Mo <zmo@chromium.org> 
    > Commit-Queue: Zhenyao Mo <zmo@chromium.org> 
    > Auto-Submit: Kenneth Russell <kbr@chromium.org> 
    > Cr-Commit-Position: refs/heads/main@{#1632304} 
     
    (cherry picked from commit 6944e2581ee7a67bc4f4b7c1d6a6b720097ba4e2) 
     
    Bug: 514926870,506653647 
    Change-Id: Ie133e85e6babd6da16889728e5f0e97af2ce489c 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7869574 
    Auto-Submit: chrome-cherry-picker@chops-service-accounts.iam.gserviceaccount.com <chrome-cherry-picker@chops-service-accounts.iam.gserviceaccount.com> 
    Bot-Commit: rubber-stamper@appspot.gserviceaccount.com <rubber-stamper@appspot.gserviceaccount.com> 
    Cr-Commit-Position: refs/branch-heads/7778@{#3520} 
    Cr-Branched-From: 77f495ee216d4c3cc784d33658bad4778c0680ee-refs/heads/main@{#1610480}

```

---

Files:

- M `gpu/BUILD.gn`
- M `gpu/command_buffer/service/gles2_cmd_decoder_passthrough_doers.cc`
- A `gpu/command_buffer/tests/gl_vertex_arrays_unittest.cc`

---

Hash: [087a7c0d9026c398c0fcf019d6e1c928be41642c](https://chromiumdash.appspot.com/commit/087a7c0d9026c398c0fcf019d6e1c928be41642c)  

Date: Fri May 22 21:53:18 2026


---

### sp...@google.com (2026-06-04)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $35000.00 for this report.

Rationale for this decision:
High Quality UAF. Memory Corruption / RCE in a highly privileged process (e.g. GPU or network)


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### pe...@google.com (2026-06-17)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2026-06-17)

1. https://chromium-review.git.corp.google.com/c/chromium/src/+/7947243
2. Low - There was no conflict.
3. 148 and 149
4. Yes

### dx...@google.com (2026-06-20)

Project: chromium/src  

Branch:  refs/branch-heads/7559  

Author:  Ken Russell [kbr@chromium.org](mailto:kbr@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7947243>

[M144-LTS] Dirty bound element array buffer in DoDeleteVertexArraysOES.

---


Expand for full commit details
```
[M144-LTS] Dirty bound element array buffer in DoDeleteVertexArraysOES.

In the passthrough command decoder. Add a unit test from the bug
report, verified with ASAN to fix the bug.

Co-authored with jetski-cli.

(cherry picked from commit 6944e2581ee7a67bc4f4b7c1d6a6b720097ba4e2)

Fixed: 506653647
Change-Id: Ie133e85e6babd6da16889728e5f0e97af2ce489c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7853561
Reviewed-by: Zhenyao Mo <zmo@chromium.org>
Commit-Queue: Zhenyao Mo <zmo@chromium.org>
Auto-Submit: Kenneth Russell <kbr@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1632304}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7947243
Reviewed-by: Achuith Bhandarkar <achuith@chromium.org>
Owners-Override: Achuith Bhandarkar <achuith@chromium.org>
Commit-Queue: Gyuyoung Kim (xWF) <qkim@google.com>
Cr-Commit-Position: refs/branch-heads/7559@{#5038}
Cr-Branched-From: 223dfbac1c7542a06b422390d954afe5b560b607-refs/heads/main@{#1552494}

```

---

Files:

- M `gpu/BUILD.gn`
- M `gpu/command_buffer/service/gles2_cmd_decoder_passthrough_doers.cc`
- A `gpu/command_buffer/tests/gl_vertex_arrays_unittest.cc`

---

Hash: [6c4cd7d52734a8e30eceb9c85c90fc170b281cbd](https://chromiumdash.appspot.com/commit/6c4cd7d52734a8e30eceb9c85c90fc170b281cbd)  

Date: Sat Jun 20 14:37:13 2026


---

### ch...@google.com (2026-08-25)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/506653647)*
