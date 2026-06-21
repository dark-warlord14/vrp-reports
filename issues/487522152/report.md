# Dawn QueueWriteBufferXl / QueueWriteTextureXl OOB Heap Read via GetSourceData() Fast Path

| Field | Value |
|-------|-------|
| **Issue ID** | [487522152](https://issues.chromium.org/issues/487522152) |
| **Status** | Accepted |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Dawn |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | gr...@gmail.com |
| **Assignee** | ba...@chromium.org |
| **Created** | 2026-02-25 |
| **Bounty** | $2,000.00 |

## Description

Hi Guys, its me again. Since my last was sadly a dupe (non public) i decided to pick up the pace. That's why I'm finishing the pocs I've already collected and submitting them.

## Summary

A compromised renderer (one with arbitrary code execution, e.g., via a separate renderer exploit) can trigger an out-of-bounds read past a shared memory allocation in Chrome's GPU process by exploiting a missing size check in the `QueueWriteBufferXl` and `QueueWriteTextureXl` wire command handlers. This is an IPC boundary bug in the Dawn wire protocol. The `GetSourceData()` fast path returns a raw pointer to shared memory without any size information. The caller blindly passes the attacker-controlled `cmd.size` from the wire command to `memcpy`, reading past the shared memory allocation boundary into adjacent GPU-process memory. The OOB data is copied into a GPU staging buffer and can be exfiltrated back to the renderer via `mapAsync(READ)`.

**Component:** Dawn wire server (WebGPU IPC)
**Process:** GPU process (reads OOB from shared memory into GPU-owned staging buffer)
**Attack vector:** Compromised renderer sends a crafted Dawn wire command (requires renderer compromise first)
**Chromium version tested:** 147.0.7701.0
**Affected functions:** `DoQueueWriteBufferXl` (ServerQueue.cpp:99-106), `DoQueueWriteTextureXl` (ServerQueue.cpp:168-175)

## Vulnerability Details

### Root Cause

The Dawn wire server implements two code paths for handling `QueueWriteBufferXl` (and `QueueWriteTextureXl`) commands. The **fast path** uses `GetSourceData()` which returns a bare pointer with no size metadata. The **fallback path** uses `DeserializeDataUpdate()` which has proper bounds checks. The fast path bypasses these bounds checks entirely.

### Vulnerable Code

**1. GetSourceData() returns raw pointer without size** (`gpu/command_buffer/service/dawn_service_memory_transfer_service.cc:128`):

```
class WriteHandleImpl
    : public dawn::wire::server::MemoryTransferService::WriteHandle {
  // ...
  uint8_t* GetSourceData() const override { return buffer_data_view_.data(); }
  //        ^^^^^^^^ Returns raw pointer — NO SIZE INFORMATION

 private:
  base::raw_span<uint8_t> buffer_data_view_;  // has .size() but it's not returned!
};

```

The `buffer_data_view_` span knows its own size (set from `MemoryTransferHandle.size` during `DeserializeWriteHandle`), but `GetSourceData()` only returns the `.data()` pointer, discarding the size.

**2. DoQueueWriteBufferXl uses cmd.size without checking against handle size** (`third_party/dawn/src/dawn/wire/server/ServerQueue.cpp:99-106`):

```
WireResult Server::DoQueueWriteBufferXl(Known<WGPUQueue> queue,
                                        Known<WGPUBuffer> buffer,
                                        uint64_t bufferOffset,
                                        uint64_t size,           // ← attacker-controlled from wire
                                        /* ... */) {
    // ...
    uint8_t* sourceData = writeHandle->GetSourceData();   // line 101: raw ptr, no size
    if (sourceData) {
        mProcs->queueWriteBuffer(queue->handle, buffer->handle, bufferOffset,
                                 sourceData,
                                 static_cast<size_t>(size));    // line 103-104: uses cmd.size!
        return WireResult::Success;                             // line 105: no bounds check
    }
    // ...fallback path with DeserializeDataUpdate (HAS bounds checks)...
}

```

The `size` parameter comes directly from the wire command (`cmd.size`), which is controlled by the compromised renderer. There is no validation that `size <= writeHandle's shared memory allocation size`.

Note: `QueueBase::WriteBuffer` (Queue.cpp:334) calls `ValidateWriteBuffer` which checks `size <= buffer->GetSize()` (the destination GPU buffer's size). This only validates against the *destination* buffer, not the *source* SHM. The attacker controls the destination buffer's size (via `createBuffer`), so this validation does not prevent exploitation — the attacker simply creates a destination buffer large enough to accommodate `cmd.size`.

**3. The memcpy that reads OOB** (`third_party/dawn/src/dawn/native/Queue.cpp` → `Buffer.cpp`):

`queueWriteBuffer` calls `WriteBufferImpl` → `UploadData`, which does:

```
memcpy(reservation.mappedPointer, data, dataSize);
// data = sourceData from GetSourceData() (shared memory pointer)
// dataSize = cmd.size from wire command (attacker-controlled)
// reads past shared memory allocation if cmd.size > handle.size

```
### Contrast: The Safe Path Has Bounds Checks

The fallback path through `DeserializeDataUpdate()` (`dawn_service_memory_transfer_service.cc:112-117`) properly validates:

```
bool DeserializeDataUpdate(const void*, size_t, size_t offset, size_t size) override {
    auto targetData = GetTarget();
    if (offset > targetData.size() || size > targetData.size() - offset) {
        return false;  // ← Check 1: vs target buffer
    }
    if (offset > buffer_data_view_.size() ||
        size > buffer_data_view_.size() - offset) {
        return false;  // ← Check 2: vs SHM allocation — THIS IS WHAT GetSourceData LACKS
    }
    memcpy(targetData.data() + offset, buffer_data_view_.data() + offset, size);
    return true;
}

```

The `GetSourceData()` fast path **bypasses both of these checks**.

### Second Affected Function: DoQueueWriteTextureXl

The identical `GetSourceData()` fast-path vulnerability exists in `DoQueueWriteTextureXl` (`ServerQueue.cpp:168-175`):

```
WireResult Server::DoQueueWriteTextureXl(Known<WGPUQueue> queue,
                                         const WGPUTexelCopyTextureInfo* destination,
                                         uint64_t dataSize,     // ← attacker-controlled
                                         /* ... */) {
    // ...
    uint8_t* sourceData = writeHandle->GetSourceData();   // line 170: raw ptr, no size
    if (sourceData) {
        mProcs->queueWriteTexture(queue->handle, destination, sourceData,
                                  static_cast<size_t>(dataSize), dataLayout, writeSize);
        return WireResult::Success;                        // line 174: no bounds check
    }
    // ...fallback path with DeserializeDataUpdate (HAS bounds checks)...
}

```

The `dataSize` parameter from the wire command is passed directly to `queueWriteTexture` without cross-checking against the WriteHandle's SHM allocation size — the same missing validation as `DoQueueWriteBufferXl`.

### Data Flow (Attacker Perspective)

```
Compromised Renderer                          GPU Process
─────────────────────                         ───────────
1. CreateWriteHandle(4096)
   → SHM allocated: 4096 bytes
   → MemoryTransferHandle.size = 4096

2. Forge wire command:
   QueueWriteBufferXl {
     size: 4160                               3. DeserializeWriteHandle()
     writeHandleCreateInfo: handle               → WriteHandleImpl with 4096-byte SHM view
   }
                                              4. GetSourceData()
                                                 → returns shm_ptr (raw, no size)

                                              5. queueWriteBuffer(shm_ptr, 4160)
                                                 → memcpy(staging, shm_ptr, 4160)
                                                 → READS 64 BYTES PAST SHM ALLOCATION
                                                 → OOB data copied into staging buffer
                                                 → staging buffer DMA'd to GPU buffer

6. MapAsync(READ) on dest buffer
   → OOB data exfiltrated back to renderer

```
### How a Compromised Renderer Triggers This

A compromised renderer has full control over the Dawn wire command stream. Specifically:

1. **Wire command serialization** happens in `third_party/dawn/src/dawn/wire/client/Queue.cpp:221`. The client sets `cmd.size = size` where `size` is the actual data size. A compromised renderer can modify this to any value.
2. **MemoryTransferHandle** (`gpu/command_buffer/common/dawn_memory_transfer_handle.h`) is serialized into the wire command create info. The `handle.size` field is set during `AllocateTransferBuffer` (`gpu/command_buffer/client/dawn_client_memory_transfer_service.cc:138`). The compromised renderer can set `cmd.size` larger than `handle.size`.
3. **No server-side cross-validation**: The server deserializes the handle (which sets `buffer_data_view_` to `handle.size` bytes) and the wire command (which has the attacker's `cmd.size`) independently. Nothing compares `cmd.size` against `buffer_data_view_.size()` on the `GetSourceData()` path.
4. **Type mismatch amplifies OOB range**: `MemoryTransferHandle.size` is `uint32_t` (max ~4GB SHM), while `cmd.size` in the wire command is `uint64_t`. The OOB read delta is bounded by the destination GPU buffer size (attacker-controlled, up to `maxBufferSize` which is typically 256MB), since `ValidateWriteBuffer` checks `size <= buffer->GetSize()`. The attacker simply creates a destination buffer large enough to accommodate the desired `cmd.size`.

### Impact

**Information disclosure from GPU process memory.** The OOB read copies data from memory adjacent to the SHM allocation in the GPU process address space into a staging buffer, which is then DMA'd to a GPU buffer. If the destination buffer has `MapRead | CopyDst` usage (valid per WebGPU spec), the renderer can read back the leaked data via `mapAsync(READ)`.

**Proven:** In the e2e demo, 64 bytes from an adjacent transfer buffer sub-allocation (pattern `0xC3` from seed buffer #3) were exfiltrated back to the renderer via `mapAsync(READ)`. This demonstrates cross-allocation information disclosure within the GPU process. The leaked bytes (`0xC3`) were NOT written by the exploiting writeBuffer call (which wrote `0xBB`); they originated from a *different* transfer operation's SHM region, confirming the OOB read crosses suballocation boundaries within the `MappedMemoryManager` chunk.

In a multi-origin scenario, the adjacent SHM sub-allocations would contain transfer data from **other origins'** WebGPU operations sharing the same GPU process — this is cross-origin information disclosure.

**Exploitation value — ASLR bypass primitive:** In modern browser exploitation, compromising the renderer is only step one. To escape the sandbox via the GPU process, an attacker typically needs two primitives: a memory corruption bug and an information leak to bypass ASLR. This vulnerability provides a highly controlled, weaponizable ASLR bypass primitive. By grooming the GPU process heap (allocating and freeing WebGPU objects to place target objects adjacent to the SHM buffer), an attacker can read vtable pointers, heap metadata, or other objects adjacent to the transfer buffer and exfiltrate GPU-process base addresses back to the compromised renderer. With larger OOB deltas that extend past the SHM mapping, the read may reach GPU process heap data directly (allocator metadata, vtable pointers, function pointers) or trigger a crash on unmapped pages.

**Severity considerations:**

- GPU process is shared across all renderers — leak affects all origins
- On Android, the GPU process is typically less sandboxed (`kAndroidGpuSandbox` is `FEATURE_DISABLED_BY_DEFAULT` at `sandbox/policy/features.cc:115`); therefore GPU-process disclosure carries higher value for exploit chains. Chrome VRP rules treat Android GPU process issues at elevated severity since the process is effectively unsandboxed
- Read primitive is bounded by the destination GPU buffer size (attacker-controlled, up to `maxBufferSize` which is typically 256MB). The attacker must create a destination buffer >= `cmd.size` for the write to pass `ValidateWriteBuffer`
- WebGPU is enabled by default in Chrome stable on desktop and Android (the `--enable-unsafe-webgpu` flag in the PoC is required only for content\_shell / local builds, not for Chrome stable)
- This is a GPU-process boundary issue; a compromised renderer is an expected attacker model for Chrome sandbox boundaries (per [Chromium's security label guidance](https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md), simulating a compromised renderer via patching is a valid demonstration method for sandbox-boundary bugs)

### Affected Platforms

All platforms where Chrome's WebGPU uses the Chromium memory transfer service (shared-memory-backed `WriteHandleImpl::GetSourceData()`):

| Platform | Affected | GPU Sandbox |
| --- | --- | --- |
| Linux Desktop | Yes | seccomp-bpf |
| Windows Desktop | Yes | Win32k lockdown |
| macOS Desktop | Yes | Seatbelt |
| ChromeOS | Yes | seccomp-bpf |
| Android | Yes | **None** (unsandboxed by default) |

## Reproduction

### Method 1: Standalone PoC (recommended for quick verification)

The standalone PoC (`poc_oob_read.cc`) replicates the exact vulnerable code path without requiring a full Chrome build. It runs three tests:

**Build (Linux):**

```
clang++ -std=c++20 -fsanitize=address -g -O0 -o poc_oob_read poc_oob_read.cc

```

**Build (Android via NDK):**

```
$NDK/toolchains/llvm/prebuilt/linux-x86_64/bin/x86_64-linux-android34-clang++ \
    -std=c++20 -fsanitize=address -g -O0 -static -o poc_oob_read_android poc_oob_read.cc
adb push poc_oob_read_android /data/local/tmp/

```

**Run:**

```
./poc_oob_read 1   # Test 1: ASan heap-buffer-overflow READ (crashes)
./poc_oob_read 2   # Test 2: Data exfiltration demo (shows leaked data)
./poc_oob_read 3   # Test 3: Safe path (DeserializeDataUpdate) correctly rejects

```

**Test 1** allocates 128 bytes of SHM, passes `cmd.size=192` to the simulated `DoQueueWriteBufferXl`, and triggers a 64-byte OOB read. ASan reports `heap-buffer-overflow READ of size 192 at 0x... located 0 bytes after 128-byte region`.

**Test 2** places a victim struct (fake vtable pointer, heap address, secret keys) adjacent to the SHM allocation and demonstrates that the OOB read copies the victim data into the staging buffer.

**Test 3** uses the same size mismatch but forces the fallback `DeserializeDataUpdate` path, which correctly rejects the operation at `buffer_data_view_.size()` bounds check (line 115-117).

### Method 2: Chrome GPU Process Crash (ASan build)

Requires two Chromium patches and an ASan build:

**Patch 1 — Client-side** (`third_party/dawn/src/dawn/wire/client/Queue.cpp`):
Inflate `cmd.size` by 64 bytes in the `WriteBufferXL` function to simulate a compromised renderer. Also lower the XL threshold from 4MB to 1KB.

**Patch 2 — Server-side** (`gpu/command_buffer/service/dawn_service_memory_transfer_service.cc`):
Modify `GetSourceData()` to copy SHM data into a heap allocation before returning. This is necessary because the original SHM is `mmap`'d shared memory which is not ASan-instrumented. The heap copy makes the OOB read ASan-detectable without changing the vulnerability semantics.

See `chrome_trigger_patch.diff` for both patches.

**Steps:**

```
# Apply patches
cd /home/compaile/chromium/src
git apply /path/to/chrome_trigger_patch.diff

# Build ASan release
autoninja -C out/asan-release content_shell

# Run with SwiftShader (for machines without GPU)
VK_ICD_FILENAMES=$(pwd)/out/asan-release/vk_swiftshader_icd.json \
DISPLAY=:10.0 \
ASAN_OPTIONS=detect_odr_violation=0 \
out/asan-release/content_shell --enable-features=Vulkan trigger_oob_read.html

```

The GPU process crashes with:

```
ERROR: AddressSanitizer: heap-buffer-overflow on address 0x75c1918bed00
READ of size 4160 at 0x75c1918bed00 thread T0 (content_shell)
    #0 __asan_memcpy
    #1 dawn::native::vulkan::Buffer::UploadData  BufferVk.cpp:669
    #2 dawn::native::QueueBase::WriteBufferImpl   Queue.cpp:344
    #3 dawn::native::QueueBase::WriteBuffer        Queue.cpp:337
    #4 dawn::native::QueueBase::APIWriteBuffer     Queue.cpp:320
    #5 dawn::native::NativeQueueWriteBuffer        ProcTable.cpp:1432
    #6 Server::DoQueueWriteBufferXl                ServerQueue.cpp:103
    ...
    #28 content::GpuMain                           gpu_main.cc:479

0x75c1918bed00 is located 0 bytes after 4096-byte region [0x75c1918bdd00,0x75c1918bed00)

```

Full ASan output in `asan_oob_read_chrome_gpu.txt`.

### Method 3: End-to-End Exfiltration (Chrome with real GPU)

This demonstrates the complete attack chain: a compromised renderer exfiltrates GPU-process heap data back to JavaScript.

**Setup:** Apply the client-side-only patch (`compromised_renderer.patch`) to Dawn's wire client. This simulates a compromised renderer by:

1. Lowering `kWriteXLThreshold` from 4MB to 1KB (forces the XL path for smaller buffers)
2. Inflating `cmd.size` by 64 bytes in `WriteBufferXL` (the wire command claims more data than the SHM allocation)

```
cd /home/compaile/chromium/src
git -C third_party/dawn apply compromised_renderer.patch
autoninja -C out/asan-release chrome

```

**Run:**

```
# Serve the trigger page (WebGPU requires a secure context)
python3 -m http.server 8099 &

# Launch Chrome (any build — ASan not required, SHM is mmap'd)
ASAN_OPTIONS=detect_odr_violation=0 \
out/asan-release/chrome \
    --enable-features=WebGPU \
    --enable-unsafe-webgpu \
    http://localhost:8099/trigger_oob_read_e2e.html

```

**Result — INFORMATION DISCLOSURE CONFIRMED:**

The trigger page seeds the GPU process transfer buffer with recognizable patterns (0xC0–0xC7), then performs a `writeBuffer` call that the patched client inflates by 64 bytes. The GPU process reads 64 bytes past the SHM allocation, copies the OOB data into a staging buffer, which is DMA'd to a `MAP_READ|COPY_DST` GPU buffer. The renderer maps the buffer and reads back the leaked data.

```
[A] Legitimate data [0x000, 0x1000):
    Expected: all 0xBB (our writeBuffer data)
    Result:   ALL 0xBB - correct

[B] LEAKED OOB DATA [0x1000, 0x1040):
    These 64 bytes were read PAST the SHM allocation
    in the GPU process and exfiltrated back to the renderer.
  LEAKED bytes [4096..4159]:
    001000: c3 c3 c3 c3 c3 c3 c3 c3 c3 c3 c3 c3 c3 c3 c3 c3 |................|
    001010: c3 c3 c3 c3 c3 c3 c3 c3 c3 c3 c3 c3 c3 c3 c3 c3 |................|
    001020: c3 c3 c3 c3 c3 c3 c3 c3 c3 c3 c3 c3 c3 c3 c3 c3 |................|
    001030: c3 c3 c3 c3 c3 c3 c3 c3 c3 c3 c3 c3 c3 c3 c3 c3 |................|

    Status: NON-ZERO DATA LEAKED! (64/64 non-zero bytes)
    The OOB read captured data from adjacent GPU process memory.
    This data was NOT part of our 0xBB writeBuffer payload.
    INFORMATION DISCLOSURE CONFIRMED.

[C] Post-OOB region [0x1040, 0x2000):
    Expected: all zeros (not written to by writeBuffer)
    Result:   ALL ZEROS - correct (confirms exact OOB boundary)

```

The leaked `0xC3` bytes are from seed buffer #3 (pattern `0xC0 + 3`), confirming the OOB read captured data from an adjacent SHM allocation in the GPU process heap. The exact boundary at `0x1040` confirms the read overflowed by exactly `cmd.size - handle.size = 64` bytes.

Note: The GPU process also generates validation errors ("Write range does not fit in buffer size") for the seed buffers, because the inflated `cmd.size` (4160) exceeds those 4096-byte buffers. These are non-fatal validation errors — the OOB read and exfiltration still succeed on the target buffer (8192 bytes).

Full output in `e2e_output.txt`. Screenshot in `e2e_screenshot.png`.

## Severity Assessment

We assess this as **Medium-High** on desktop platforms and **High** on Android:

- **Desktop:** OOB read in sandboxed GPU process, reachable from compromised renderer (expected attacker model for sandbox-boundary bugs). Provides a controlled, repeatable ASLR bypass / information leak primitive for exploit chains targeting the GPU process. Proven: cross-allocation transfer buffer disclosure. With heap grooming, likely extends to vtable pointers and allocator metadata.
- **Android:** OOB read in **unsandboxed** GPU process. Leaked data includes cross-origin content from other renderers' GPU operations. The GPU process has no sandbox by default (`kAndroidGpuSandbox` is `FEATURE_DISABLED_BY_DEFAULT`), making this primitive directly useful for full exploit chains without additional sandbox escapes.

This is a GPU-process boundary issue — a compromised renderer is the expected attacker model per Chromium's own security guidelines for IPC/sandbox-boundary vulnerabilities.

## Suggested Fix

Add a size parameter to `GetSourceData()` or validate `cmd.size` against the handle's allocation size before using the fast path. The same fix must be applied to both `DoQueueWriteBufferXl` (ServerQueue.cpp:101) and `DoQueueWriteTextureXl` (ServerQueue.cpp:170):

**Option A: Add size output parameter to GetSourceData** (minimal change):

```
// In WireServer.h (WriteHandle base class):
virtual uint8_t* GetSourceData(size_t* sourceSize) const {
    if (sourceSize) *sourceSize = 0;
    return nullptr;
}

// In dawn_service_memory_transfer_service.cc (WriteHandleImpl):
uint8_t* GetSourceData(size_t* sourceSize) const override {
    if (sourceSize) *sourceSize = buffer_data_view_.size();
    return buffer_data_view_.data();
}

// In ServerQueue.cpp (DoQueueWriteBufferXl):
size_t sourceSize = 0;
uint8_t* sourceData = writeHandle->GetSourceData(&sourceSize);
if (sourceData && sourceSize >= static_cast<size_t>(size)) {
    mProcs->queueWriteBuffer(queue->handle, buffer->handle, bufferOffset,
                             sourceData, static_cast<size_t>(size));
    return WireResult::Success;
}

```

**Option B: Return span instead of raw pointer** (safer, API change):

```
// In WireServer.h:
virtual std::span<const uint8_t> GetSourceData() const {
    return {};
}

// In DoQueueWriteBufferXl:
auto sourceData = writeHandle->GetSourceData();
if (!sourceData.empty() && sourceData.size() >= static_cast<size_t>(size)) {
    mProcs->queueWriteBuffer(queue->handle, buffer->handle, bufferOffset,
                             sourceData.data(), static_cast<size_t>(size));
    return WireResult::Success;
}

```
## Files in This Report

| File | Description |
| --- | --- |
| `report.md` | This report |
| `poc_oob_read.cc` | Standalone PoC source (3 tests) — canonical |
| `poc_oob_read` | Compiled Linux binary (ASan, for convenience) |
| `poc_oob_read_android` | Compiled Android x86\_64 binary (ASan, for convenience) |
| `compromised_renderer.patch` | Minimal client-side-only patch showing what a compromised renderer does |
| `asan_oob_read_linux.txt` | ASan crash output — standalone PoC on Linux |
| `asan_oob_read_android.txt` | ASan crash output — standalone PoC on Android emulator |
| `asan_oob_read_chrome_gpu.txt` | ASan crash output — Chrome GPU process (content\_shell) |
| `trigger_oob_read.html` | WebGPU JavaScript trigger page for Chrome (ASan crash) |
| `trigger_oob_read_e2e.html` | End-to-end exfiltration trigger page (seeds, leaks, hexdumps) |
| `e2e_output.txt` | Captured output from e2e exfiltration run |
| `e2e_screenshot.png` | Screenshot of Chrome showing leaked data |
| `chrome_trigger_patch.diff` | Two-file patch for Chrome ASan reproduction |

## Key Source File References

| File | Lines | What |
| --- | --- | --- |
| `gpu/command_buffer/service/dawn_service_memory_transfer_service.cc` | 128 | `GetSourceData()` — returns raw pointer, no size |
| `gpu/command_buffer/service/dawn_service_memory_transfer_service.cc` | 112-117 | `DeserializeDataUpdate()` — the bounds checks that GetSourceData bypasses |
| `third_party/dawn/src/dawn/wire/server/ServerQueue.cpp` | 99-106 | `DoQueueWriteBufferXl` — uses `cmd.size` with `GetSourceData()` pointer |
| `third_party/dawn/src/dawn/wire/server/ServerQueue.cpp` | 108-122 | Fallback path with `DeserializeDataUpdate` (safe) |
| `third_party/dawn/src/dawn/wire/server/ServerQueue.cpp` | 168-175 | `DoQueueWriteTextureXl` — same vulnerable `GetSourceData()` fast path |
| `third_party/dawn/include/dawn/wire/WireServer.h` | 146 | `GetSourceData()` virtual interface — returns bare `uint8_t*` |
| `gpu/command_buffer/common/dawn_memory_transfer_handle.h` | 16-20 | `MemoryTransferHandle` struct with `size` field |
| `gpu/command_buffer/client/dawn_client_memory_transfer_service.cc` | 118-128 | Client `CreateWriteHandle` — sets `handle.size` |
| `third_party/dawn/src/dawn/native/Queue.cpp` | 337-344 | `WriteBufferImpl` → calls `UploadData` |
| `sandbox/policy/features.cc` | 115 | `kAndroidGpuSandbox` = `FEATURE_DISABLED_BY_DEFAULT` |
| CREDIT INFORMATION |  |  |

Reporter credit: Grischa Hauser

## Attachments

- [asan_oob_read_android.txt](attachments/asan_oob_read_android.txt) (text/plain, 4.3 KB)
- [asan_oob_read_chrome_gpu.txt](attachments/asan_oob_read_chrome_gpu.txt) (text/plain, 17.7 KB)
- [asan_oob_read_linux.txt](attachments/asan_oob_read_linux.txt) (text/plain, 4.5 KB)
- [chrome_trigger_patch.diff](attachments/chrome_trigger_patch.diff) (text/x-diff, 1.7 KB)
- [compromised_renderer.patch](attachments/compromised_renderer.patch) (text/x-diff, 1.1 KB)
- [e2e_output.txt](attachments/e2e_output.txt) (text/plain, 4.9 KB)
- [e2e_screenshot.png](attachments/e2e_screenshot.png) (image/png, 226.2 KB)
- [poc_oob_read.cc](attachments/poc_oob_read.cc) (text/x-c++src, 21.1 KB)
- [trigger_oob_read.html](attachments/trigger_oob_read.html) (text/html, 4.6 KB)
- [trigger_oob_read_e2e.html](attachments/trigger_oob_read_e2e.html) (text/html, 12.4 KB)

## Timeline

### cw...@chromium.org (2026-02-27)

Looking at this, we should spanify the interface, both for `SetTarget*` and `GetSourceData`. It will be mildly annoying with the a 5-way CL but can be done pretty quickly.

### aj...@google.com (2026-02-28)

Does this require `--enable-unsafe-webgpu` if so this may not be a security vulnerability?

### gr...@gmail.com (2026-02-28)

Yeah, similar to the other report. I made the assumption that replacing the receiving side (mmap not ASAN instrumented) with ASAN supported to make it visible is common practice, but it's apparently not. So while it's technically an OOB read, it's just inside adjacent sub-allocations, not arbitrary/private memory. So I don't know if that is considered feasible or not. Not high priority for sure IMO (also my initial assessment of the severity was off, sorry for that).

### mp...@google.com (2026-03-04)

The duplicate issue linked above indicates that this is a feasible OOB read.

### mp...@google.com (2026-03-04)

I think --enable-unsafe-webgpu is just to enable webgpu support on Linux for the PoC, this bug is in the Dawn Wire server and so it's used on all platforms that support WebGPU.

### dx...@google.com (2026-03-04)

Project: dawn  

Branch:  main  

Author:  Brandon Jones [bajones@chromium.org](mailto:bajones@chromium.org)  

Link:    <https://dawn-review.googlesource.com/295115>

Add GetSourceSize to WriteHandle

---


Expand for full commit details
```
     
    Allows WriteHandle source data to be bounds checked. This CL does not 
    perform the bounds checking. Part 1 of a 3-part patch. 
     
    Bug: 487522152 
    Change-Id: I157cbfbc59683c0406f642827a7d8be781611d1f 
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/295115 
    Reviewed-by: Loko Kung <lokokung@google.com> 
    Commit-Queue: Brandon Jones <bajones@chromium.org> 
    Reviewed-by: Corentin Wallez <cwallez@chromium.org>

```

---

Files:

- M `include/dawn/wire/WireServer.h`

---

Hash: 33a083f7a9e71cfe7e8a9b05c94fda00e5715900  

Date: Wed Mar 4 19:57:57 2026


---

### me...@google.com (2026-03-04)

Setting tentative FoundIn=147. bajones@, could you please double check? Does this affect earlier versions?

### dx...@google.com (2026-03-04)

Project: chromium/src  

Branch:  main  

Author:  chromium-autoroll [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com)  

Link:    <https://chromium-review.googlesource.com/7632225>

Roll Dawn from ad8d51fbdd59 to 33a083f7a9e7 (9 revisions)

---


Expand for full commit details
```
     
    https://dawn.googlesource.com/dawn.git/+log/ad8d51fbdd59..33a083f7a9e7 
     
    2026-03-04 bajones@chromium.org Add GetSourceSize to WriteHandle 
    2026-03-04 titouan@google.com [Fuzzing] Return non-zero on LLVMFuzzerInitialize failure. 
    2026-03-04 bsheedy@google.com Migrate Linux/x64/fuzz/rel to Starlark 
    2026-03-04 bsheedy@google.com Remove Mac/x64 infra/specs entries 
    2026-03-04 chouinard@google.com Remove expected failures for i32 QC Win ops 
    2026-03-04 mridulgoyal@google.com [Kotlin][WebGPU] Refactor enum definitions to use a nested annotation. 
    2026-03-04 bsheedy@google.com Treat fuzz builders as parent builders 
    2026-03-04 bsheedy@google.com Migrate Mac/x64 to Starlark 
    2026-03-04 dawn-automated-expectations@chops-service-accounts.iam.gserviceaccount.com Roll third_party/webgpu-cts/ 21ecca5d7..d213d4b8d (1 commit) 
     
    If this roll has caused a breakage, revert this CL and stop the roller 
    using the controls here: 
    https://autoroll.skia.org/r/dawn-chromium-autoroll 
    Please CC cwallez@google.com,dsinclair@google.com on the revert to ensure that a human 
    is aware of the problem. 
     
    To file a bug in Dawn: https://bugs.chromium.org/p/dawn/issues/entry 
    To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry 
     
    To report a problem with the AutoRoller itself, please file a bug: 
    https://issues.skia.org/issues/new?component=1389291&template=1850622 
     
    Documentation for the AutoRoller is here: 
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md 
     
    Cq-Include-Trybots: luci.chromium.try:dawn-android-arm-deps-rel;luci.chromium.try:dawn-android-arm64-deps-rel;luci.chromium.try:dawn-linux-x64-deps-rel;luci.chromium.try:dawn-mac-x64-deps-rel;luci.chromium.try:dawn-mac-arm64-deps-rel;luci.chromium.try:dawn-win10-x64-deps-rel;luci.chromium.try:dawn-win10-x86-deps-rel;luci.chromium.try:dawn-win11-arm64-deps-rel;luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:gpu-fyi-cq-mac-arm64;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:gpu-fyi-cq-android-arm64 
    Bug: chromium:485816035,chromium:485900045,chromium:487522152 
    Tbr: dsinclair@google.com 
    Change-Id: I8da7316cb20ae513fa7175558ca704038dcb0e43 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7632225 
    Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Cr-Commit-Position: refs/heads/main@{#1594247}

```

---

Files:

- M `DEPS`
- M `third_party/dawn`

---

Hash: [7c052d36dbdd33adf2a5903a9a611a249f5f9977](https://chromiumdash.appspot.com/commit/7c052d36dbdd33adf2a5903a9a611a249f5f9977)  

Date: Wed Mar 4 22:32:44 2026


---

### dx...@google.com (2026-03-05)

Project: chromium/src  

Branch:  main  

Author:  Brandon Jones [bajones@chromium.org](mailto:bajones@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7632342>

Implement GetSourceSize for Dawn WriteHandleImpl

---


Expand for full commit details
```
     
    Allows data to be bounds-checked. Does not actually perform the bounds 
    checks. This change is part 2 of a 3-part patch. 
     
    Bug: 487522152 
    Change-Id: Id3d678a8c97570a982335e03dfc4796304763b41 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7632342 
    Reviewed-by: Loko Kung <lokokung@google.com> 
    Reviewed-by: Kai Ninomiya <kainino@chromium.org> 
    Commit-Queue: Brandon Jones <bajones@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1594444}

```

---

Files:

- M `gpu/command_buffer/service/dawn_service_memory_transfer_service.cc`

---

Hash: [408d634878efe2f32ab8d2e7aaeab20455b99cf2](https://chromiumdash.appspot.com/commit/408d634878efe2f32ab8d2e7aaeab20455b99cf2)  

Date: Thu Mar 5 03:46:02 2026


---

### ch...@google.com (2026-03-05)

Setting milestone because of s2 severity.

### ch...@google.com (2026-03-05)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security Impact hotlist or the Severity field, and remove the ReleaseBlock hotlist.

### ba...@chromium.org (2026-03-05)

The code in question was originally added in Chrome 144.

### dx...@google.com (2026-03-05)

Project: dawn  

Branch:  main  

Author:  Brandon Jones [bajones@chromium.org](mailto:bajones@chromium.org)  

Link:    <https://dawn-review.googlesource.com/295116>

Perform bounds checking on WriteHandle SourceData

---


Expand for full commit details
```
     
    Performs bounds checking on the SourceData of a WriteHandle using the 
    newely added GetSourceSize() method. Part 3 of a 3-part patch. 
     
    Bug: 487522152 
    Change-Id: Iaa076a262fe0ead987d2e05b10c8f89f36e06c92 
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/295116 
    Commit-Queue: Brandon Jones <bajones@chromium.org> 
    Reviewed-by: Loko Kung <lokokung@google.com>

```

---

Files:

- M `src/dawn/wire/server/ServerQueue.cpp`

---

Hash: 6f6dc291774d504ebcde49fdb59e46df1f20c541  

Date: Thu Mar 5 21:09:07 2026


---

### dx...@google.com (2026-03-06)

Project: chromium/src  

Branch:  main  

Author:  chromium-autoroll [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com)  

Link:    <https://chromium-review.googlesource.com/7640431>

Roll Dawn from 79dba80f5cd9 to 5e1594bc4130 (14 revisions)

---


Expand for full commit details
```
     
    https://dawn.googlesource.com/dawn.git/+log/79dba80f5cd9..5e1594bc4130 
     
    2026-03-05 bsheedy@google.com Migrate Linux/x86/fuzz/dbg to Starlark 
    2026-03-05 bsheedy@google.com Migrate Win/x86/rel to Starlark 
    2026-03-05 bsheedy@google.com Remove Mac/x64/dbg infra/specs entries 
    2026-03-05 bsheedy@google.com Migrate Mac/x64/dbg to Starlark 
    2026-03-05 bsheedy@google.com Remove Linux/x86/fuzz/rel infra/specs entries 
    2026-03-05 bsheedy@google.com Remove Linux/x64/fuzz/dbg infra/specs entries 
    2026-03-05 bajones@chromium.org Perform bounds checking on WriteHandle SourceData 
    2026-03-05 jrprice@google.com [tint] Add WGSL validation utility to Resolver tests 
    2026-03-05 dsinclair@chromium.org [ir][decode] Add missing bounds checks on enums. 
    2026-03-05 cwallez@chromium.org [dawn] Add a minimal common/Algebra.h with Matrix/Vector 
    2026-03-05 bsheedy@google.com Migrate Linux/x86/fuzz/rel to Starlark 
    2026-03-05 bsheedy@google.com Migrate Linux/x64/fuzz/dbg to Starlark 
    2026-03-05 dsinclair@chromium.org Simplify some ir builder methods. 
    2026-03-05 amaiorano@google.com [native] Move ResourceTableDefaultResources to its own header/cpp 
     
    If this roll has caused a breakage, revert this CL and stop the roller 
    using the controls here: 
    https://autoroll.skia.org/r/dawn-chromium-autoroll 
    Please CC cwallez@google.com,dsinclair@google.com on the revert to ensure that a human 
    is aware of the problem. 
     
    To file a bug in Dawn: https://bugs.chromium.org/p/dawn/issues/entry 
    To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry 
     
    To report a problem with the AutoRoller itself, please file a bug: 
    https://issues.skia.org/issues/new?component=1389291&template=1850622 
     
    Documentation for the AutoRoller is here: 
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md 
     
    Cq-Include-Trybots: luci.chromium.try:dawn-android-arm-deps-rel;luci.chromium.try:dawn-android-arm64-deps-rel;luci.chromium.try:dawn-linux-x64-deps-rel;luci.chromium.try:dawn-mac-x64-deps-rel;luci.chromium.try:dawn-mac-arm64-deps-rel;luci.chromium.try:dawn-win10-x64-deps-rel;luci.chromium.try:dawn-win10-x86-deps-rel;luci.chromium.try:dawn-win11-arm64-deps-rel;luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:gpu-fyi-cq-mac-arm64;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:gpu-fyi-cq-android-arm64 
    Bug: chromium:468988322,chromium:473354063,chromium:485816035,chromium:487522152,chromium:487652626 
    Tbr: dsinclair@google.com 
    Change-Id: I1c76fc9ff96e5d5a2db83ac3cb2375420160b97e 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7640431 
    Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Cr-Commit-Position: refs/heads/main@{#1595094}

```

---

Files:

- M `DEPS`
- M `third_party/dawn`

---

Hash: [9c2aa95522992c9395f94c361956b5b1cecf0b16](https://chromiumdash.appspot.com/commit/9c2aa95522992c9395f94c361956b5b1cecf0b16)  

Date: Fri Mar 6 02:33:54 2026


---

### dx...@google.com (2026-03-11)

Project: dawn  

Branch:  main  

Author:  Brandon Jones [bajones@chromium.org](mailto:bajones@chromium.org)  

Link:    <https://dawn-review.googlesource.com/296376>

Return a span for WriteHandle Source

---


Expand for full commit details
```
     
    Builds on the previous changes to WriteHandle to support bounds checking 
    and updates the public method to return a span instead of a separate 
    data/size. The data/size methods are still present, though now private, 
    because that's the only way we can properly overload them from Chromium. 
     
    Bug: 487522152 
    Change-Id: If276cf5961a33102673b37388ea31612d0010005 
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/296376 
    Reviewed-by: Corentin Wallez <cwallez@chromium.org> 
    Auto-Submit: Brandon Jones <bajones@chromium.org> 
    Commit-Queue: Corentin Wallez <cwallez@chromium.org> 
    Reviewed-by: Loko Kung <lokokung@google.com>

```

---

Files:

- M `include/dawn/wire/WireServer.h`
- M `src/dawn/wire/server/ServerQueue.cpp`

---

Hash: d97a08f4dd57f3ab211ed0cb8a68c002f09d0b5a  

Date: Wed Mar 11 09:14:49 2026


---

### dx...@google.com (2026-03-12)

Project: chromium/src  

Branch:  main  

Author:  chromium-autoroll [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com)  

Link:    <https://chromium-review.googlesource.com/7658937>

Roll Dawn from b2cbf25a0364 to ad824e2cb346 (45 revisions)

---


Expand for full commit details
```
     
    https://dawn.googlesource.com/dawn.git/+log/b2cbf25a0364..ad824e2cb346 
     
    2026-03-12 bsheedy@google.com Generate .pyl files from Starlark 
    2026-03-11 kainino@chromium.org [cts] Skip an OOM crash on Pixel 6, triage related expectations 
    2026-03-11 kainino@chromium.org Revert "[dawn][native] Add support filteringness attributes to GetBindGroupLayout" 
    2026-03-11 jrprice@google.com [ir] Clone explicit template parameters on builtin calls 
    2026-03-11 beaufort.francois@gmail.com Sync webgpu.h changes and remove "compat" tag 
    2026-03-11 petermcneeley@google.com [tint] Minor metal validation bug for relaxed math 
    2026-03-11 bajones@chromium.org Return a span for WriteHandle Source 
    2026-03-11 dawn-autoroll@skia-public.iam.gserviceaccount.com Roll Chromium from 87e7333c9482 to 8d43dd57d980 (676 revisions) 
    2026-03-11 dawn-autoroll@skia-public.iam.gserviceaccount.com Roll ANGLE from 29b36dd0b852 to 41b52b413169 (10 revisions) 
    2026-03-11 dawn-autoroll@skia-public.iam.gserviceaccount.com Roll DirectX Shader Compiler from e9be4c440ce8 to 4f398bffdbba (5 revisions) 
    2026-03-11 shaoboyan@microsoft.com vulkan: Fix descriptor set rebinding on push constant range change 
    2026-03-11 jiawei.shao@intel.com Enable SharedBufferMemoryTests.BeginAccessInitialization on WARP 
    2026-03-11 bsheedy@google.com Remove Linux/TSan infra/specs entries 
    2026-03-10 bsheedy@google.com Migrate Linux/TSan to Starlark 
    2026-03-10 lokokung@google.com [dawn][wire] Adds a lock to the server-side buffer object. 
    2026-03-10 bsheedy@google.com Make dawn_end2end_tests definitions more generic 
    2026-03-10 bsheedy@google.com Fix clusterfuzz corpus args 
    2026-03-10 bajones@chromium.org Restrict Vulkan Dynamic Rendering on Mali-G68 GPUs 
    2026-03-10 chrome-branch-day@chops-service-accounts.iam.gserviceaccount.com Activate dawn M147 
    2026-03-10 petermcneeley@google.com [dawn] Minor triage of pixel 10 cts bugs 
    2026-03-10 jrprice@google.com [tint] Remove TINT_REFLECT_EQUALS macro 
    2026-03-10 dawn-autoroll@skia-public.iam.gserviceaccount.com Roll vulkan-deps from 9117cef67a60 to b55a0e69f29d (11 revisions) 
    2026-03-10 dawn-autoroll@skia-public.iam.gserviceaccount.com Roll Chromium from cdd0b0ea31d7 to 87e7333c9482 (692 revisions) 
    2026-03-10 dawn-autoroll@skia-public.iam.gserviceaccount.com Roll ANGLE from b1b19492e609 to 29b36dd0b852 (13 revisions) 
    2026-03-10 dawn-autoroll@skia-public.iam.gserviceaccount.com Roll DirectX Shader Compiler from 2888a8764a33 to e9be4c440ce8 (7 revisions) 
    2026-03-10 jiawei.shao@intel.com Define shared buffer memory d3d12 file handle descriptor in dawn.json 
    2026-03-10 bsheedy@google.com Remove Win/MSVC/dbg infra/specs entries 
    2026-03-09 bsheedy@google.com Migrate Win/MSVC/dbg to Starlark 
    2026-03-09 bsheedy@google.com Remove Linux/clusterfuzz infra/specs entries 
    2026-03-09 jrprice@google.com [msl] Run CanGenerate() from Generate() 
    2026-03-09 bsheedy@google.com Migrate Linux/clusterfuzz to Starlark 
    2026-03-09 jrprice@google.com [msl] Use Result for Validate*() and test helpers 
    2026-03-09 kainino@chromium.org [dawn][metal] Fix robustness issues around buffer lengths being u32 
    2026-03-09 jrprice@google.com [tint] Remove dead code for textureStore clamping 
    2026-03-09 cwallez@chromium.org [dawn][native] Add support filteringness attributes to GetBindGroupLayout 
    2026-03-09 jrprice@google.com [msl] Simplify vertex pulling entry point check 
    2026-03-09 bsheedy@google.com Remove Win/MSVC/rel infra/specs entries 
    2026-03-09 bsheedy@google.com Migrate missed Win/ASan test exceptions 
    2026-03-09 amaiorano@google.com Fix validation on nullptr color attachment 
    2026-03-09 senorblanco@chromium.org GL: fix multithreaded buffer mapping tests. 
    2026-03-09 bsheedy@google.com Migrate Win/MSVC/rel to Starlark 
    2026-03-09 kylechar@google.com Add RenderPassRenderArea feature 
    2026-03-09 bsheedy@google.com Swap Win/ARM64 mirrored builder 
    2026-03-09 amaiorano@google.com [dawn] Add samplers to ResourceTableTests.HasResourceCompatibilityAllTypes test 
    2026-03-09 cwallez@chromium.org [YUV AHB] Add test checking RGB of Vulkan YCbCr sampler 
     
    If this roll has caused a breakage, revert this CL and stop the roller 
    using the controls here: 
    https://autoroll.skia.org/r/dawn-chromium-autoroll 
    Please CC cwallez@google.com,gman@google.com on the revert to ensure that a human 
    is aware of the problem. 
     
    To file a bug in Dawn: https://bugs.chromium.org/p/dawn/issues/entry 
    To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry 
     
    To report a problem with the AutoRoller itself, please file a bug: 
    https://issues.skia.org/issues/new?component=1389291&template=1850622 
     
    Documentation for the AutoRoller is here: 
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md 
     
    Cq-Include-Trybots: luci.chromium.try:dawn-android-arm-deps-rel;luci.chromium.try:dawn-android-arm64-deps-rel;luci.chromium.try:dawn-linux-x64-deps-rel;luci.chromium.try:dawn-mac-x64-deps-rel;luci.chromium.try:dawn-mac-arm64-deps-rel;luci.chromium.try:dawn-win10-x64-deps-rel;luci.chromium.try:dawn-win10-x86-deps-rel;luci.chromium.try:dawn-win11-arm64-deps-rel;luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:gpu-fyi-cq-mac-arm64;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:gpu-fyi-cq-android-arm64 
    Bug: chromium:386255678,chromium:407748576,chromium:421288698,chromium:451928481,chromium:452840618,chromium:468988322,chromium:470014334,chromium:473354063,chromium:479233871,chromium:485816035,chromium:486441214,chromium:486866985,chromium:487522152,chromium:487593147,chromium:488613135,chromium:489152883,chromium:490378523,chromium:491869936,chromium:491881355 
    Tbr: gman@google.com 
    Test: Test: MetalBufferRobustnessTest.* 
    Change-Id: I46a192df2c7fb6305a7bc2d10d35b0bc7139fcc8 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7658937 
    Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Cr-Commit-Position: refs/heads/main@{#1598189}

```

---

Files:

- M `DEPS`
- M `third_party/dawn`

---

Hash: [c6d422798c9dfbb3ea5453a55744ad9296e4e772](https://chromiumdash.appspot.com/commit/c6d422798c9dfbb3ea5453a55744ad9296e4e772)  

Date: Thu Mar 12 03:42:35 2026


---

### gr...@gmail.com (2026-04-08)

Hi just a quick question after 3 Weeks, is there anything else you need from me so it can go from fixed to verified? (assuming thats the correct order like in my first issue). Thanks!

### gr...@gmail.com (2026-05-04)

Thanks for the status update. Is there any information if the panel will/did vote on this? Especially since this was before the VRP changes so i was curious about the status/handling of this report.

Thanks!

### cw...@chromium.org (2026-05-06)

The issues has the `reward-topanel` tag so it should be handled by the VRP panel and I assume they'll use the rules at the time the issue was submitted (I'm not part of the panel though). Things take time though because there are a lot of issues in the queue for the panel.

### gr...@gmail.com (2026-05-06)

Alright. Thanks for the update!

### ch...@google.com (2026-06-12)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### sp...@google.com (2026-06-15)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
Basline. User information disclosure.


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/487522152)*
