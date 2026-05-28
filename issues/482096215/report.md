# WebNN BlockwiseExpandConstant FlatBuffers overflow allows for controlled heap OOB write in GPU process

| Field | Value |
|-------|-------|
| **Issue ID** | [482096215](https://issues.chromium.org/issues/482096215) |
| **Status** | New |
| **Severity** | S4-Minimal |
| **Priority** | P0 |
| **Component** | Blink>WebML |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ci...@gmail.com |
| **Assignee** | re...@chromium.org |
| **Created** | 2026-02-05 |
| **Bounty** | $36,000.00 |

## Description

---

### Report description

WebNN BlockwiseExpandConstant FlatBuffers overflow allows for controlled heap OOB write in GPU process

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

#### Which URL (or repository) have you found the vulnerability in?

<https://chromium.googlesource.com/chromium/src/+/main/services/webnn/tflite/graph_builder_tflite.cc>

---

### The problem

#### Please describe the technical details of the vulnerability

- Chrome Stable **144.0.7559.110** (SIGTRAP crash — macOS)
- ASan Chromium **146.0.7668.0** (heap-buffer-overflow confirmed via ASan + lldb — macOS)

macOS 15.7.2 (Intel x86\_64). The vulnerable code is in the TFLite backend (`services/webnn/tflite/graph_builder_tflite.cc`), which is the default CPU backend on macOS Intel and Linux.

Flags:

```
--enable-features=WebMachineLearningNeuralNetwork --in-process-gpu

```
## Steps to Reproduce

1. Kill all running Chrome instances
2. Launch ASan Chromium with the flags above
3. Open `blockwise_int64_poc.html` (controlled int8 > int64 write) or `blockwise_float_41414141.html` (arbitrary float32 write)
4. Wait ~30 seconds for graph building to trigger the overflow
5. ASan reports `heap-buffer-overflow` — WRITE of size 8 (int64 path) or WRITE of size 4 (float path)

For lldb proof of controlled write (ASan build, `--single-process` added for ASan thread visibility):

```
lldb -- ./Chromium.app/Contents/MacOS/Chromium \
  --enable-features=WebMachineLearningNeuralNetwork \
  --in-process-gpu --single-process \
  --user-data-dir=/tmp/chrome_blockwise
(lldb) breakpoint set -n __asan_report_store8   # for int64 PoC
(lldb) breakpoint set -n __asan_report_store4   # for float PoC
(lldb) run
# Navigate to PoC file
# On breakpoint hit:
(lldb) register read r9       # int64 path: r9 = 0x0000000000000042
(lldb) register read xmm0     # float path: xmm0 = 0x...41414141

```
## Description

`BlockwiseExpandConstant<T>()` in `graph_builder_tflite.cc:7063` expands block-wise quantization constants by creating a FlatBuffers vector of size `block_size * values.size()` elements. For `quantizeLinear` with large inputs, the expanded scale (float32, 4 bytes each) and zero\_point (int64, 8 bytes each) vectors are appended to FlatBuffers' internal serialization buffer (`vector_downward`).

FlatBuffers uses `uint32_t` offsets (`uoffset_t`) to reference data within the buffer. When the cumulative buffer size exceeds 2^32 bytes (4 GB), these offsets silently truncate. The `CreateUninitializedVector` call at line 7054 returns a pointer derived from a truncated offset, causing `std::ranges::fill` at line 7068 to write attacker-controlled values past the heap allocation boundary.

Two crash signatures, same root cause:

#### Heap-buffer-overflow (OOB write at 4GB boundary)

When the total FlatBuffers buffer exceeds 4GB, offset truncation causes `BlockwiseExpandConstant` to write past the allocation.

Vulnerable code (`graph_builder_tflite.cc:7063-7071`):

```
template <typename DataType>
  requires(std::is_same_v<DataType, float> || std::is_same_v<DataType, int64_t>)
flatbuffers::Offset<flatbuffers::Vector<DataType>>
GraphBuilderTflite::BlockwiseExpandConstant(base::span<const DataType> values,
                                            uint32_t block_size) {
  auto [block_wise_offset, block_wise_span_buffer] =
      CreateUninitializedVector<DataType>(block_size * values.size());  // line 7066
  for (size_t i = 0; i < values.size(); ++i) {
    std::ranges::fill(
        block_wise_span_buffer.subspan(i * block_size, block_size), values[i]);  // OOB WRITE
  }
  return block_wise_offset;
}

```

The `CreateUninitializedVector` wrapper at line 7052 calls `builder_.CreateUninitializedVector<DataType>(length, &buffer)`. FlatBuffers' internal `vector_downward::reallocate` allocates the buffer correctly (size\_t, no overflow), but the returned `buffer` pointer is computed using a truncated `uoffset_t`, pointing past the allocation.

A secondary crash (heap-use-after-free) also occurs when a single expanded vector exceeds ~2GB, due to FlatBuffers' internal reallocation. Same root cause, same fix.

#### Attacker control

The written values are attacker-controlled:

**Int64 path (zero\_point):** The `Int8Array` zero\_point values provided via JavaScript are sign-extended to int64. Any int8 value (-128 to 127) produces a controlled 8-byte value:

- `0x42` → writes `0x0000000000000042`
- `0xFF` (-1) → writes `0xFFFFFFFFFFFFFFFF`
- `0x80` (-128) → writes `0xFFFFFFFFFFFFFF80`

**Float path (scale):** The `Float32Array` scale values are written as raw IEEE 754 bit patterns. Any 32-bit value can be encoded as a float, giving a full arbitrary 4-byte write:

- `0x41414141` → stored as float `12.078...`, written as 4 bytes `41 41 41 41`
- `0xDEADBEEF` → stored as float `-6.259...e18`, written as 4 bytes `EF BE AD DE`

The float path requires a three-op graph that exploits TFLite's reverse serialization order (operations are serialized last-defined-first), positioning the controlled scale to cross the 4GB boundary.

## Proof of Controlled Write

#### Int64 path: r9 = 0x42

Using `blockwise_int64_poc.html` with `CONTROLLED_VALUE = 0x42`:

```
(lldb) breakpoint set -n __asan_report_store8
(lldb) run
# Navigate to blockwise_int64_poc.html

Process stopped at __asan_report_store8

(lldb) register read r9
      r9 = 0x0000000000000042

```

r9 = 0x42, matching CONTROLLED\_VALUE from the PoC.

#### Float path: xmm0 = 0x41414141

Using `blockwise_float_41414141.html` with controlled float encoding `0x41414141`:

```
(lldb) breakpoint set -n __asan_report_store4
(lldb) run
# Navigate to blockwise_float_41414141.html

Process stopped at __asan_report_store4

(lldb) register read --format hex xmm0
    xmm0 = 0x00000000000000000000000041414141

```

xmm0 = 0x41414141, confirming the attacker-controlled bit pattern.

## Crash Details

#### Chrome Stable 144.0.7559.110 (`blockwise_int64_poc.html`)

```
Exception Type:  EXC_BREAKPOINT (SIGTRAP)
Termination Reason: Trace/BPT trap: 5
Faulting Thread: 49

```

`PA_IMMEDIATE_CRASH()` — PartitionAlloc detecting heap metadata corruption from the OOB write.

#### ASan: heap-buffer-overflow (int64 path, `blockwise_int64_poc.html`)

```
==81845==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x014dd3112c00
WRITE of size 8 at 0x014dd3112c00 thread T9
    #0 std::ranges::fill(CheckedContiguousIterator<long long>, ...)
    #1 BlockwiseExpandConstant<long long>+0x67f
    #2 SerializeQuantizeParams+0x9c2
    #3 SerializeQuantizeLinear+0x8f5
    #4 SerializeOperation+0x2556
    #5 CreateAndBuild+0x4dd
    #6 CreateAndBuildOnBackgroundThread+0x2ac

0x014dd3112c00 is located 0 bytes after 4831839232-byte region [0x014cb3112800,0x014dd3112c00)
allocated by thread T9 here:
    #0 __asan_memmove
    #1 operator new(unsigned long)
    #2 flatbuffers::vector_downward::reallocate
    #3 BlockwiseExpandConstant<long long>+0x17f
    #4 SerializeQuantizeParams+0x9c2

SUMMARY: AddressSanitizer: heap-buffer-overflow in std::ranges::fill ... BlockwiseExpandConstant

```

The write is at offset **0 bytes after** the 4,831,839,232-byte (~4.5GB) allocation. The allocation was made by `flatbuffers::vector_downward::reallocate` inside `BlockwiseExpandConstant<long long>`.

#### ASan: heap-buffer-overflow (float path, `blockwise_float_41414141.html`)

```
==82449==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x014e71815e00
WRITE of size 4 at 0x014e71815e00 thread T10
    #0 std::ranges::fill(CheckedContiguousIterator<float>, ...)
    #1 BlockwiseExpandConstant<float>+0x67f
    #2 SerializeQuantizeParams+0x9a2
    #3 SerializeQuantizeLinear+0x8f5
    #4 SerializeOperation+0x2556
    #5 CreateAndBuild+0x4dd
    #6 CreateAndBuildOnBackgroundThread+0x2ac

0x014e71815e00 is located 0 bytes after 4812965376-byte region [0x014d52a15800,0x014e71815e00)
allocated by thread T10 here:
    #0 __asan_memmove
    #1 operator new(unsigned long)
    #2 flatbuffers::vector_downward::reallocate
    #3 BlockwiseExpandConstant<float>+0x17f

SUMMARY: AddressSanitizer: heap-buffer-overflow in std::ranges::fill ... BlockwiseExpandConstant<float>

```

WRITE of size 4 in `BlockwiseExpandConstant<float>` confirms the float code path. The 4,812,965,376-byte (~4.5GB) allocation is from FlatBuffers' `vector_downward::reallocate`.

## Bisect

Introduced in commit [`7ca28ae03d19`](https://chromium.googlesource.com/chromium/src/+/7ca28ae03d197a73f4582bcdb421b086a3cb64d0) — *"webnn: Support block-wise quantize/dequantize"* , August 18, 2025. This commit added `BlockwiseExpandConstant` to `graph_builder_tflite.cc`. Chromium position: refs/heads/main@{#1502528}. Bug: 377172670.

## Suggested Fix

Add a size check in `BlockwiseExpandConstant` before creating the vector, rejecting expansions that would push the FlatBuffers buffer past the `uint32_t` offset limit:

```
template <typename DataType>
flatbuffers::Offset<flatbuffers::Vector<DataType>>
GraphBuilderTflite::BlockwiseExpandConstant(base::span<const DataType> values,
                                            uint32_t block_size) {
  const size_t total_elements = static_cast<size_t>(block_size) * values.size();
  const size_t total_bytes = total_elements * sizeof(DataType);

  // FlatBuffers uses uint32_t offsets. Reject if this vector alone
  // or the cumulative buffer would exceed the 2GB safe limit.
  if (total_bytes > std::numeric_limits<int32_t>::max()) {
    // Return error or empty offset
  }

  auto [block_wise_offset, block_wise_span_buffer] =
      CreateUninitializedVector<DataType>(total_elements);
  // ...
}

```

Alternatively, the WebNN validation layer (`webnn_graph_impl.cc`) could reject `quantizeLinear`/`dequantizeLinear` operations where `input_size * sizeof(expanded_type)` would exceed a safe threshold, preventing the large expansion from reaching the TFLite serializer.

#### Impact analysis

The write occurs during `builder.build()` in the GPU process. Without `--in-process-gpu`, this is a GPU process heap corruption that crashes the tab. With `--in-process-gpu`, the OOB write occurs in the browser process.

The attacker controls the value written: arbitrary 4-byte patterns via the float path, or 256 distinct 8-byte values via the int8→int64 path. On release builds without ASan, this overwrites adjacent heap memory — PartitionAlloc metadata or other heap objects.

---

### The cause

#### What version of Chrome have you found the security issue in?

Stable

#### Is the security issue related to a crash?

Yes, it is related to a crash.

#### Choose the type of vulnerability

Memory Corruption (in a sandboxed process)

#### How would you like to be publicly acknowledged for your report?

cinzinga

## Attachments

- [blockwise_int64_poc.html](attachments/blockwise_int64_poc.html) (text/html, 2.7 KB)
- [blockwise_float_41414141.html](attachments/blockwise_float_41414141.html) (text/html, 4.1 KB)

## Timeline

### cl...@appspot.gserviceaccount.com (2026-02-05)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4997450905354240.

### 24...@project.gserviceaccount.com (2026-02-06)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the hotlistid:4801165.

### 24...@project.gserviceaccount.com (2026-02-06)

Detailed Report: https://clusterfuzz.com/testcase?key=4997450905354240

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-buffer-overflow WRITE 8
Crash Address: 0x76fa28b59c00
Crash State:
  webnn::tflite::GraphBuilderTflite::SerializeQuantizeParams
  webnn::tflite::GraphBuilderTflite::SerializeQuantizeLinear
  webnn::tflite::GraphBuilderTflite::SerializeOperation
  
Sanitizer: address (ASAN)

Recommended Security Severity: Critical

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1580438:1580442

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=4997450905354240

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary.

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


A recommended severity was added to this bug. Please change the severity if it is inaccurate.

### ch...@google.com (2026-02-06)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-02-06)

Setting Priority to P0 to match Severity s0. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### aj...@google.com (2026-02-06)

Adding folks from [b/481049079](https://issues.chromium.org/issues/481049079) is WebMachineLearningNeuralNetwork OT enabled yet?

### aj...@google.com (2026-02-06)

This might be reachable on all OSes? Not clear from gn. <https://source.chromium.org/chromium/chromium/src/+/main:services/webnn/features.gni;l=12> & <https://source.chromium.org/chromium/chromium/src/+/main:services/webnn/BUILD.gn;l=145?q=graph_builder_tflite.cc&ss=chromium%2Fchromium%2Fsrc>

### re...@chromium.org (2026-02-06)

Yes, TFLite is enabled on all platforms and is the fallback path for older macOS and Windows clients.

Looking at the internals of the Flatbuffers library I am concerned that just limiting the size of individual buffers is insufficient as an attacker could construct a graph requiring a series of smaller buffers which still add up to enough to cause `uoffset_t` to overflow. There does not appear to be any mechanism within it to catch when the internal buffer has grown to a size that cannot be represented with a `uoffset_t` when `size_t` and `uoffset_t` are not the same type.

### re...@chromium.org (2026-02-06)

Thinking this over I remembered that I had previously considered this scenario when switching `SerializeBuffer` to use a separate weights buffer (now a weights file). That change was intended to fix exactly this scenario where a constant value would overflow the allowed length of a Flatbuffer file. With constants written separately that only left the possibility that the graph structure itself could exceed the Flatbuffer limit. My logic at the time was that since the size of a `WebNNGraphInfo` structure is limited to the maximum size of a Mojo IPC message ([128 MiB](https://source.chromium.org/chromium/chromium/src/+/main:content/app/initialize_mojo_core.cc;l=31;drc=976a71ef2a509d4391d814b52b9f4700fdf35789;bpv=1;bpt=1?q=maximum&ss=chromium%2Fchromium%2Fsrc:mojo%2F&start=11)) it would need to grow by a factor of 16 to exceed the Flatbuffer limit during the conversion performed by `GraphBuilderTflite` which seemed like a safe enough margin.

The exception to this logic is exposed by this issue, where an attacker-controlled buffer *must* be placed in the Flatbuffer instead of being written to the weights file.

I think the solution is to implement a conservative check: When writing a large constant to the weights file the constant must be smaller than 128 MiB and there must be at least 512 MiB of available space in the Flatbuffer. This should leave a sufficient margin of error to prevent this class of issues and any reasonable model will be far from hitting these limits.

### dx...@google.com (2026-02-07)

Project: chromium/src  

Branch:  main  

Author:  Reilly Grant [reillyg@chromium.org](mailto:reillyg@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7552465>

webnn: Add safety limits to the size of a Flatbuffer model

---


Expand for full commit details
```
     
    The Flatbuffer library does not protect itself against a flatbuffer 
    becoming larger than the 2 GiB limit, which can put it at risk of 
    various integer overflow issues because the offset type is only 32-bits. 
     
    This change enforces a safety threshold on the total buffer size and 
    limits the size of tensors that can be added to the buffer as inline 
    values. 
     
    Fixed: 482096215 
    Change-Id: Id2f56fa92cd4fddf7f0c19f3b4e04430ae0b6022 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7552465 
    Reviewed-by: Alex Gough <ajgo@chromium.org> 
    Auto-Submit: Reilly Grant <reillyg@chromium.org> 
    Commit-Queue: Alex Gough <ajgo@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1581295}

```

---

Files:

- M `services/webnn/tflite/graph_builder_tflite.cc`
- M `services/webnn/tflite/graph_builder_tflite.h`

---

Hash: [74d7d5aa2b36a43f13da256dcc06c437d35def71](https://chromiumdash.appspot.com/commit/74d7d5aa2b36a43f13da256dcc06c437d35def71)  

Date: Sat Feb 7 06:55:27 2026


---

### 24...@project.gserviceaccount.com (2026-02-08)

ClusterFuzz testcase 4997450905354240 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1581294:1581295

If this is incorrect, please add the hotlistid:5433040 and re-open the issue.

### ch...@google.com (2026-02-11)

Security Merge Request Consideration: Not requesting merge to dev (M146) because latest trunk commit (1581295) appears to be prior to dev branch point (1582197). If this is incorrect please remove NA-146 from the 'Merge' field and add 146 to the 'Merge-Request' field If other changes are required to fix this bug completely please request a merge if necessary.
Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### sp...@google.com (2026-02-20)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $36000.00 for this report.

Rationale for this decision:
Memory corruption in a highly privileged process (e.g. GPU, network processes) + bisect


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### sp...@google.com (2026-03-03)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $7000.00 for this report.

Rationale for this decision:
After review we are rewarding and additional $7000 for baseline renderer compromise


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-05-17)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/482096215)*
