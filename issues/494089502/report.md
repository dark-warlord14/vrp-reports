# Missing size validation in WebNN TFLite quantize parameter serialization leads to out-of-bounds read in the GPU process

| Field | Value |
|-------|-------|
| **Issue ID** | [494089502](https://issues.chromium.org/issues/494089502) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | Blink>WebML |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | je...@gmail.com |
| **Assignee** | ju...@intel.com |
| **Created** | 2026-03-19 |
| **Bounty** | $43,000.00 |

## Description

# Missing size validation in WebNN TFLite quantize parameter serialization leads to out-of-bounds read in the GPU process

## Summary

The WebNN TFLite graph builder's `SerializeQuantizeParams` function writes renderer-controlled quantization vectors directly into a FlatBuffer without checking the per-buffer size limit or the cumulative model size threshold. A web page can construct a `quantizeLinear`/`dequantizeLinear` chain whose scale and zero-point constants, after type expansion from `int8` to `int64`, push the serialized FlatBuffer past the 2 GiB offset boundary. The resulting 32-bit offset corruption causes an out-of-bounds read in the GPU process when TFLite attempts to parse the model. This affects all 64-bit desktop platforms (Windows, macOS, Linux) that use the WebNN TFLite CPU backend.

## Bisect

### `SerializeQuantizeParams` introduced without size checks

- Commit: `2b2c367f7d8c34bb152181c1fdfc5ea20b01ca64`
- Date: 2024-11-20
- Author: Junwei Fu ([junwei.fu@intel.com](mailto:junwei.fu@intel.com))
- Subject: webnn: Support int4 dequantization and per-channel quantization
- Review: <https://chromium-review.googlesource.com/c/chromium/src/+/6015965>

This commit introduced `SerializeQuantizeParams` with direct `builder_.CreateVector<float>(scale_value)` and `builder_.CreateVector<int64_t>(zero_point_value)` calls, bypassing any buffer size checks. The `GetConstantInt64Value` helper widens every int8 element to int64\_t (8x amplification), but no limit is enforced on the resulting vector size or cumulative FlatBuffer size.

### FlatBuffer safety limits added but `SerializeQuantizeParams` NOT updated

- Commit: `74d7d5aa2b36a43f13da256dcc06c437d35def71`
- Date: 2026-02-06
- Author: Reilly Grant ([reillyg@chromium.org](mailto:reillyg@chromium.org))
- Subject: webnn: Add safety limits to the size of a Flatbuffer model
- Review: <https://chromium-review.googlesource.com/c/chromium/src/+/7552465>

This commit introduced `kMaxInlineBufferSize` (128 MiB) and `kFlatbufferSafetyThreshold` (1.5 GiB) with checks in `SerializeBuffer` and `CreateUninitializedVector`, but `SerializeQuantizeParams` was not updated to use either guard.

## Root Cause

Chromium's WebNN TFLite translation layer is aware that FlatBuffers cannot safely exceed 2 GiB. A comment in the source explicitly documents this concern, and two constants enforce safety limits:

```
// services/webnn/tflite/graph_builder_tflite.cc:61-67
// Flatbuffers cannot be larger than 2 GiB however the library does not provide
// feedback when this limit is exceeded and can instead encounter integer
// overflows. To avoid this, limit the size of buffers that have to be included
// directly in the Flatbuffer (rather than as external weights) and refuse to
// add additional buffers once the total size approaches a safety threshold.
constexpr size_t kMaxInlineBufferSize = 128 * 1024 * 1024;        /* 128 MiB */
constexpr size_t kFlatbufferSafetyThreshold = 1536 * 1024 * 1024; /* 1.5 GiB */

```

The normal tensor data serialization path, `SerializeBuffer`, correctly checks both limits before writing anything into the FlatBuffer:

```
// services/webnn/tflite/graph_builder_tflite.cc:3004-3008
if (buffer.size() > kMaxInlineBufferSize) {
    return base::unexpected("Buffer size is over inline limit.");
}
if (builder_.GetSize() > kFlatbufferSafetyThreshold) {
    return base::unexpected("Model too large.");
}

```

The helper `CreateUninitializedVector`, used by the blockwise quantization expansion path, also enforces identical checks.

`SerializeQuantizeParams`, however, bypasses both guards. When the scale and zero-point shapes match the input exactly (the standard per-channel quantization case where the block size equals 1), the function takes a code path that calls `builder_.CreateVector` directly:

```
// services/webnn/tflite/graph_builder_tflite.cc:7036-7039
} else {
    scale_offset = builder_.CreateVector<float>(scale_value);
    zero_point_offset = builder_.CreateVector<int64_t>(zero_point_value);
}

```

There is no check on the size of the vectors, and no check on the cumulative `builder_.GetSize()` after the call. This path is reached for every `quantizeLinear` and `dequantizeLinear` operation whose scale and zero-point operands are constants with the same shape as the input along each axis.

An amplification effect makes this especially dangerous. The `GetConstantInt64Value` function reads the constant data in its original data type and widens every element to `int64_t`:

```
// services/webnn/tflite/graph_builder_tflite.cc:6913-6916
base::FixedArray<int64_t> typed_value(operand.descriptor.NumberOfElements());

```

An `int8` zero-point constant with N elements occupies N bytes in the renderer, but after widening, `CreateVector<int64_t>` writes 8N bytes into the FlatBuffer. The validation layer only checks the original tensor byte length against `tensor_byte_length_limit` (which is `INT_MAX` on 64-bit), so an attacker can pass tensors that individually satisfy all WebNN validation constraints while the expanded representation in the FlatBuffer is eight times larger.

Since each `quantizeLinear` or `dequantizeLinear` operation independently serializes its quantize parameters (there is no deduplication when the same constant operand is referenced by multiple operations), chaining several such operations with the same scale and zero-point constants multiplies the FlatBuffer growth linearly. A chain of 10 operations with 20-million-element rank-1 constants produces approximately 2.4 GiB of inline quantize parameter vectors, far exceeding both the 1.5 GiB safety threshold and the 2 GiB FlatBuffer hard limit.

The `FlatBufferBuilder` used by Chromium is instantiated as `FlatBufferBuilderImpl<false>`, which uses `uint32_t` for its internal `SizeT`. The `FLATBUFFERS_ASSERT(size() < max_size_)` check in `vector_downward::ensure_space` is compiled out in release builds because it expands to `assert()`, which is disabled when `NDEBUG` is defined. The builder therefore continues to grow its internal buffer past 2 GiB without any error. Once the model is finalized and passed to `FlatBufferModel::BuildFromBuffer`, TFLite's `InterpreterBuilder` constructor calls `ReadAllMetadata`, which follows the corrupted 32-bit offsets and reads from an invalid address.

## Reproduce

Tested at commit `3ad31ba232d9a804b4de78d788e391f82b40a906`.

No source modifications are required. The bug is triggered entirely from JavaScript through the WebNN API.

Configure an ASAN release build. Create `out/asan-release/args.gn` with the following content:

```
is_debug = false
dcheck_always_on = false
is_asan = true
is_component_build = false

```

Build Chrome with `autoninja -C out/asan-release chrome`.

### Linux (default TFLite backend)

On Linux, TFLite is the default WebNN backend. Launch Chrome from the source root:

```
ASAN_OPTIONS=detect_odr_violation=0 out/asan-release/chrome \
  --no-sandbox \
  --enable-features=WebMachineLearningNeuralNetwork \
  --user-data-dir=/tmp/poc-tflite004 \
  --enable-logging=stderr \
  file://$(pwd)/issue_tflite004/poc.html

```

The GPU process crashes within approximately 10 seconds with `SEGV_MAPERR` (signal 11, exit\_code=11). The PoC first runs a small sanity test (N=1000), then a medium test (N=5M), then a chain of 10 `quantizeLinear`/`dequantizeLinear` operations with N=20M. The chain test drives the FlatBuffer to over 3.6 GiB; TFLite crashes when parsing the corrupted model offsets:

```
Received signal 11 SEGV_MAPERR 7bdeeae41eae
#5 0x7fe1c280a6e2 (libservices_webnn_webnn_service.so)  ReadAllMetadata
#6 0x7fe1c280a01e (libservices_webnn_webnn_service.so)  InterpreterBuilder
#7 0x7fe1c1a45df8 (libservices_webnn_webnn_service.so)  ComputeResources::Create
GPU process exited unexpectedly: exit_code=11

```

The complete Linux crash log is provided in `segv-linux.log`.

### Windows

On Windows, `--disable-features=WebNNOnnxRuntime` is needed to fall through to TFLite.

```
out\asan-release\chrome.exe --no-sandbox ^
  --enable-features=WebMachineLearningNeuralNetwork ^
  --disable-features=WebNNOnnxRuntime ^
  --enable-logging=stderr ^
  poc.html

```

The GPU process crashes with an ASAN access-violation READ in `ReadAllMetadata`.

```
=================================================================
==28856==ERROR: AddressSanitizer: access-violation on unknown address 0x127a7b3feeae (pc 0x7ffdddf1161d bp 0x0022ffbfea10 sp 0x0022ffbfe9a0 T22)
==28856==The signal is caused by a READ memory access.
    #0 0x7ffdddf1161c in tflite::impl::FlatBufferModelBase<class tflite::impl::FlatBufferModel>::ReadAllMetadata(struct tflite::Model const *) D:\chromium\src\third_party\tflite\src\tensorflow\compiler\mlir\lite\core\model_builder_base.h:505:31
    #1 0x7ffdddf10efe in tflite::impl::InterpreterBuilder::InterpreterBuilder(struct tflite::Model const *, class tflite::OpResolver const &, class tflite::ErrorReporter *, class tflite::InterpreterOptions const *, class tflite::Allocation const *) D:\chromium\src\third_party\tflite\src\tensorflow\lite\core\interpreter_builder.cc:243:17
    #2 0x7ffddc9ab08f in webnn::tflite::GraphImplTflite::ComputeResources::Create(enum webnn::mojom::Device, struct webnn::tflite::GraphBuilderTflite::Result) D:\chromium\src\services\webnn\tflite\graph_impl_tflite.cc:168:34
    #3 0x7ffddc9a98d8 in webnn::tflite::GraphImplTflite::CreateAndBuildOnBackgroundThread D:\chromium\src\services\webnn\tflite\graph_impl_tflite.cc:542:20
    #4 0x7ffddc9b1a4a in base::internal::Invoker D:\chromium\src\base\functional\bind_internal.h:982:12
    #5 0x7ffddc9cd12e in base::internal::ReturnAsParamAdapter D:\chromium\src\base\task\post_task_and_reply_with_result_internal.h:23:48
    #6 0x7ffddc9cdd48 in base::internal::Invoker D:\chromium\src\base\functional\bind_internal.h:982:12
    #7 0x7ffecce8359b in base::internal::PostTaskAndReplyRelay::RunTaskAndPostReply D:\chromium\src\base\threading\post_task_and_reply_impl.h:45:28
    #8 0x7ffecce83b44 in base::internal::Invoker D:\chromium\src\base\functional\bind_internal.h:982:12
    #9 0x7ffeccdd3e28 in base::TaskAnnotator::RunTaskImpl D:\chromium\src\base\task\common\task_annotator.cc:229:34
    #10 0x7ffeccebe44c in base::internal::TaskTracker::RunContinueOnShutdown D:\chromium\src\base\task\thread_pool\task_tracker.cc:668:3
    #11 0x7ffeccebcb94 in base::internal::TaskTracker::RunTask D:\chromium\src\base\task\thread_pool\task_tracker.cc:506:5
    #12 0x7ffeccebbb4b in base::internal::TaskTracker::RunAndPopNextTask D:\chromium\src\base\task\thread_pool\task_tracker.cc:394:5
    #13 0x7ffeccee7d20 in base::internal::WorkerThread::RunWorker D:\chromium\src\base\task\thread_pool\worker_thread.cc:473:36
    #14 0x7ffeccee6b6f in base::internal::WorkerThread::RunPooledWorker D:\chromium\src\base\task\thread_pool\worker_thread.cc:359:3
    #15 0x7ffecd05a45e in base::`anonymous namespace'::ThreadFunc D:\chromium\src\base\threading\platform_thread_win.cc:112:13

SUMMARY: AddressSanitizer: access-violation D:\chromium\src\third_party\tflite\src\tensorflow\compiler\mlir\lite\core\model_builder_base.h:505:31 in tflite::impl::FlatBufferModelBase<class tflite::impl::FlatBufferModel>::ReadAllMetadata(struct tflite::Model const *)

Thread T22 created by T0 here:
    #0 0x7ffeb7dcdb84  (clang_rt.asan_dynamic-x86_64.dll)
    #1 0x7ffecd059116 in base::`anonymous namespace'::CreateThreadInternal D:\chromium\src\base\threading\platform_thread_win.cc:178:7
    #2 0x7ffeccee4f6f in base::internal::WorkerThread::Start D:\chromium\src\base\task\thread_pool\worker_thread.cc:185:3
    #3 0x7ffed571b61a in content::GpuMain D:\chromium\src\content\gpu\gpu_main.cc:421:16

Task trace:
    #0 0x7ffddc9a7bb5 in webnn::tflite::GraphImplTflite::CreateAndBuild D:\chromium\src\services\webnn\tflite\graph_impl_tflite.cc:503:7
    #1 0x7ffddc6bb88f in webnn::WebNNContextImpl::CreateWeightsFile D:\chromium\src\services\webnn\webnn_context_impl.cc:149:13
    #2 0x7ffe08b093e0 in viz::GpuServiceImpl::InitializeWithHostInternal D:\chromium\src\components\viz\service\gl\gpu_service_impl.cc:464:15

```
## Credit

Please use c6eed09fc8b174b0f3eebedcceb1e792 as the credit for this vulnerability. Thank you.

## Attachments

- [segv-linux.log](attachments/segv-linux.log) (text/plain, 8.5 KB)
- [segv-mac.log](attachments/segv-mac.log) (text/plain, 3.5 KB)
- [poc.html](attachments/poc.html) (text/html, 7.1 KB)
- [asan.log](attachments/asan.log) (text/plain, 22.1 KB)

## Timeline

### cl...@appspot.gserviceaccount.com (2026-03-19)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4564935250051072.

### re...@chromium.org (2026-03-19)

Ningxin, can you find someone on your team to take a look?

### re...@chromium.org (2026-03-19)

ClusterFuzz isn't reproducing this but I suspect the issue is just that it takes too long for all the phases of the PoC to complete. The theory of this issue is sound. There should be checks around this and any other usage of `builder_.CreateVector` which serialize an operand directly into the FlatBuffer.

### 24...@project.gserviceaccount.com (2026-03-19)

Testcase 4564935250051072 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=4564935250051072.

### es...@chromium.org (2026-03-20)

I'm marking FoundIn as M147 because per <https://chromestatus.com/feature/5176273954144256> the feature only entered origin trial in M147. Could one of the feature developers please correct me if this bug would have affected production Chrome users prior to M147? Thank you!

### ch...@google.com (2026-03-20)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security Impact hotlist or the Severity field, and remove the ReleaseBlock hotlist.

### re...@chromium.org (2026-03-20)

> Could one of the feature developers please correct me if this bug would have affected production Chrome users prior to M147? Thank you!

Nope, that's correct. Thank you for checking.

### dx...@google.com (2026-03-20)

Project: chromium/src  

Branch:  main  

Author:  junwei [junwei.fu@intel.com](mailto:junwei.fu@intel.com)  

Link:    <https://chromium-review.googlesource.com/7687063>

[WebNN] Add FlatBuffer size checks in TFLite graph builder

---


Expand for full commit details
```
     
    Check `kFlatbufferSafetyThreshold` in `FinishAndTakeResult` before 
    finalizing the model to ensure the total size is within safe limits. 
     
    And ensure `scale_value` and `zero_point_value` individual vectors stay 
    below `kMaxInlineBufferSize` in `SerializeQuantizeParams`. 
     
    Bug: 494089502 
    Change-Id: I95f36ac05e48620ea974993c2bfcda41dca0b68b 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7687063 
    Reviewed-by: Hu, Ningxin <ningxin.hu@intel.com> 
    Commit-Queue: Hu, Ningxin <ningxin.hu@intel.com> 
    Reviewed-by: Reilly Grant <reillyg@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1602908}

```

---

Files:

- M `services/webnn/tflite/graph_builder_tflite.cc`
- M `services/webnn/tflite/graph_builder_tflite.h`

---

Hash: [f11378f6ab6b1a0adae27269a845b9e52dd8a988](https://chromiumdash.appspot.com/commit/f11378f6ab6b1a0adae27269a845b9e52dd8a988)  

Date: Fri Mar 20 23:39:43 2026


---

### ch...@google.com (2026-03-21)

Security Merge Request:

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Requesting merge to beta (M147) because latest trunk commit (1602908) appears to be after beta branch point (1596535).

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### re...@chromium.org (2026-03-21)

**Which CLs should be backmerged? (Please include Gerrit links.)**  

<https://chromium-review.googlesource.com/7687063>

**Has this fix been verified on Canary to not pose any stability regressions?**  

It has been verified by manual testing and unit tests and we'll get Canary stability signals by Monday.

**Does this fix pose any potential non-verifiable stability risks?**  

No.

**Does this fix pose any known compatibility risks?**  

It slightly reduces the maximum model size supported by WebNN but this limit was set large enough to be unlikely to cause problems.

**Does it require manual verification by the test team? If so, please describe required testing.**  

No.

### ch...@google.com (2026-03-21)

Merge review required: M147 is already shipping to beta.

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
Owners: alonbajayo (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), harrysouders (Mobile US), eakpobaro (Mobile EMEA)

### dr...@chromium.org (2026-03-23)

No crashes in Canary, approved to merge to M147.

### dx...@google.com (2026-03-24)

Project: chromium/src  

Branch:  refs/branch-heads/7727  

Author:  junwei [junwei.fu@intel.com](mailto:junwei.fu@intel.com)  

Link:    <https://chromium-review.googlesource.com/7694961>

[M147] [WebNN] Add FlatBuffer size checks in TFLite graph builder

---


Expand for full commit details
```
     
    Check `kFlatbufferSafetyThreshold` in `FinishAndTakeResult` before 
    finalizing the model to ensure the total size is within safe limits. 
     
    And ensure `scale_value` and `zero_point_value` individual vectors stay 
    below `kMaxInlineBufferSize` in `SerializeQuantizeParams`. 
     
    (cherry picked from commit f11378f6ab6b1a0adae27269a845b9e52dd8a988) 
     
    Bug: 494089502 
    Change-Id: I95f36ac05e48620ea974993c2bfcda41dca0b68b 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7687063 
    Reviewed-by: Hu, Ningxin <ningxin.hu@intel.com> 
    Commit-Queue: Hu, Ningxin <ningxin.hu@intel.com> 
    Reviewed-by: Reilly Grant <reillyg@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1602908} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7694961 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Commit-Queue: Reilly Grant <reillyg@chromium.org> 
    Auto-Submit: Reilly Grant <reillyg@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7727@{#1312} 
    Cr-Branched-From: ce01102937348db7b88c8a4257ee4b3ac702eb1a-refs/heads/main@{#1596535}

```

---

Files:

- M `services/webnn/tflite/graph_builder_tflite.cc`
- M `services/webnn/tflite/graph_builder_tflite.h`

---

Hash: [d95bc59d4f0af2abf24ea259c369754e777130ab](https://chromiumdash.appspot.com/commit/d95bc59d4f0af2abf24ea259c369754e777130ab)  

Date: Tue Mar 24 00:02:19 2026


---

### pe...@google.com (2026-03-24)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### re...@chromium.org (2026-03-24)

This does not need to be merged to M144 because the feature was not enabled by default in M144.

### qk...@google.com (2026-03-25)

Labeled `LTS-NotApplicable-144`/`LTS-NotApplicable-138` because the feature was not enabled in M144 according to comment #16. 

### aj...@google.com (2026-04-23)

sev=crit as on android - impact=none

### sp...@google.com (2026-04-24)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $43000.00 for this report.

Rationale for this decision:
High Quality with Bisect. Memory corruption in a highly privileged process (e.g. GPU, network processes) 


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-06-27)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/494089502)*
