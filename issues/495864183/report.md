# Integer overflow in TFLite StridedSlice output dimension computation leads to heap buffer overflow in the GPU process

| Field | Value |
|-------|-------|
| **Issue ID** | [495864183](https://issues.chromium.org/issues/495864183) |
| **Status** | Accepted |
| **Severity** | S4-Minimal |
| **Priority** | P0 |
| **Component** | Blink>WebML |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | je...@gmail.com |
| **Assignee** | ly...@google.com |
| **Created** | 2026-03-25 |
| **Bounty** | $43,000.00 |

## Description

# Integer overflow in TFLite StridedSlice output dimension computation leads to heap buffer overflow in the GPU process

## Summary

The TFLite STRIDED\_SLICE kernel computes output tensor dimensions using the integer ceiling expression `(dim_shape + stride - 1) / stride`. When `dim_shape` and `stride` are both large positive `int32_t` values whose sum exceeds `INT32_MAX`, the addition overflows, producing a negative dimension. This negative dimension propagates through `BytesRequired` and `TfLiteTensorResizeMaybeCopy` as a near-maximum `size_t` value, causing a second unsigned wraparound when the 16-byte XNN padding is added, resulting in a 1-byte heap allocation. The subsequent `StridedSlice` evaluation writes 17 bytes into this 1-byte buffer, yielding a 16-byte heap buffer overflow. The vulnerability is reachable from any web page via the WebNN `slice()` API, which maps to TFLite's STRIDED\_SLICE on Linux. Because WebNN executes in the GPU process, this constitutes a GPU process crash triggerable from an unprivileged renderer without any sandbox escape prerequisite. Affected platform: Linux (TFLite backend for WebNN). No special GPU hardware is required; the `cpu` device type suffices.

## Bisect

Introducing Commit (TFLite): `8cedce08e98d8f11e3ee5ced7a25fb830ccfb935`

- Date: 2026-03-18
- Author: Reilly Grant
- Description: "Avoid casting dimensions to float in STRIDED\_SLICE ResizeOutputTensor"

The commit replaced a `std::ceil(dim_shape / float(stride))` computation with the integer expression `(dim_shape + stride - 1) / stride`. The original float-based computation, while imprecise for large values, did not suffer from signed integer overflow. The replacement introduced the overflow for cases where `dim_shape + stride - 1` exceeds `INT32_MAX`.

Rolled into Chromium via: `77b4bf2e3f249e53833be98b98bb582c13a38ed3` (2026-03-19, "Roll TFLite/LiteRT to Next Green Version", TFLite range `4e546f69670b..67d816626bf2`).

## Root Cause

The WebNN `slice()` operation is serialized to a TFLite `STRIDED_SLICE` operator by `GraphBuilderTflite::SerializeSlice`. The `begin`, `end`, and `strides` tensors are embedded as constants in the FlatBuffer model. When all inputs to the STRIDED\_SLICE node are constant or persistent, the kernel's `Prepare` function enters a constant-folding path that both resizes the output tensor and immediately evaluates the operation:

```
// third_party/tflite/src/tensorflow/lite/kernels/strided_slice.cc
if (IsConstantOrPersistentTensor(op_context.input) &&
    IsConstantOrPersistentTensor(op_context.begin) &&
    IsConstantOrPersistentTensor(op_context.end)) {
  SetTensorToPersistentRo(op_context.output);
  TF_LITE_ENSURE_OK(context, ResizeOutputTensor(context, &op_context));
  op_data->noop = true;
  return EvalImpl(context, node);
}

```

Inside `ResizeOutputTensor`, the output dimension for each axis is computed by an integer ceiling division. For a positive stride and a positive `dim_shape` (which equals `end - begin`), the code reaches:

```
// third_party/tflite/src/tensorflow/lite/kernels/strided_slice.cc
dim_shape = (dim_shape + stride - 1) / stride;

```

With `dim_shape = 2147483647` (INT32\_MAX) and `stride = 126322568`, the addition `dim_shape + stride - 1` evaluates to `2273806214`, which exceeds `INT32_MAX` and wraps to `-2021161082` under two's complement. The subsequent division `-2021161082 / 126322568` truncates toward zero, producing `-15`. This negative value is pushed into the output shape vector and passed to `context->ResizeTensor`.

The `ResizeTensor` implementation calls `BytesRequired`, which multiplies dimension values after implicitly converting them to `size_t`. The conversion of `-15` to `size_t` yields `18446744073709551601`. `MultiplyAndCheckOverflow` does not reject this because multiplying by 1 (the initial count) does not overflow:

```
// third_party/tflite/src/tensorflow/lite/util.cc
TF_LITE_ENSURE_MSG(
    context_,
    MultiplyAndCheckOverflow(old_count, dims[k], &count) == kTfLiteOk,
    "BytesRequired number of elements overflowed.\n");

```

The resulting `num_bytes` value of `18446744073709551601` is passed to `TfLiteTensorResizeMaybeCopy`, which adds 16 bytes of XNN padding:

```
// third_party/tflite/src/tensorflow/lite/core/c/common.cc
size_t alloc_bytes = num_bytes + /*XNN_EXTRA_BYTES=*/16;

```

This addition wraps the `uint64_t` value to `1`, so `malloc(1)` allocates a single byte. The tensor's `bytes` field is set to the near-maximum `size_t` value, and `data` points to the 1-byte allocation.

Control then returns to `Prepare`, which calls `EvalImpl`. The reference `StridedSlice<int8_t>` implementation computes start and stop indices from the original, uncorrupted `begin`/`end`/`stride` tensors. For `start=0`, `end=2147483647`, `stride=126322568`, the inner loop iterates 17 times (offsets 0, 126322568, ..., 2021161088). Each iteration calls `SequentialTensorWriter<signed char>::Write`, which increments an output pointer:

```
// third_party/tflite/src/tensorflow/lite/kernels/internal/portable_tensor.h
void Write(int position) { *output_ptr_++ = input_data_[position]; }

```

The first write lands within the 1-byte allocation. The remaining 16 writes overflow the buffer, corrupting adjacent heap metadata or objects.

The PoC constructs the persistent input tensor without transferring 2 GiB from the renderer. It creates a 1-byte UINT8 constant and uses WebNN `tile()` to replicate it to shape `[2147483647]`. TFLite's TILE kernel also performs constant folding, marking its output as `kTfLitePersistentRo`, which is allocated entirely within the GPU process. The subsequent STRIDED\_SLICE sees a persistent input and enters the constant-folding path described above.

The XNNPACK delegate rejects STRIDED\_SLICE nodes with strides other than 1, so the operation falls through to the vulnerable builtin kernel.

## Reproduce

Tested at Chromium commit `5e60c832cb8d7cddd0bc4f84d3c8864c80649afb` (2026-03-25).

Build:

```
autoninja -C ~/chromium/src/out/asan-release chrome

```

Run:

```
ASAN_OPTIONS=detect_odr_violation=0 ~/chromium/src/out/asan-release/chrome \
  --no-sandbox \
  --enable-features=WebMachineLearningNeuralNetwork \
  --user-data-dir=/tmp/poc-$(date +%s) \
  file:///path/to/poc.html

```

The GPU process crashes with a heap-buffer-overflow report within seconds of page load. The system requires approximately 8 GiB of available memory (the TILE constant-folding allocates a 2 GiB tensor within the GPU process under ASAN).

ASAN log:

```
==378626==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x7bbf758461b1 at pc 0x7f9f7bcefc61 bp 0x7b9b23d9f9f0 sp 0x7b9b23d9f9e8
WRITE of size 1 at 0x7bbf758461b1 thread T49 (ThreadPoolForeg)
    #0 tflite::reference_ops::StridedSlice<signed char> portable_tensor.h:128:45
    #1 tflite::ops::builtin::strided_slice::EvalImpl strided_slice.h:140:3
    #2 tflite::ops::builtin::strided_slice::Prepare strided_slice.cc:335:12
    #3 tflite::Subgraph::PrepareOpsStartingAt subgraph.cc:1540:44
    #4 tflite::Subgraph::PrepareOpsAndTensors subgraph.cc:1588:7
    #5 tflite::Subgraph::AllocateTensors subgraph.cc:1035:25
    #6 webnn::tflite::GraphImplTflite::ComputeResources::Create graph_impl_tflite.cc:221:34
    #7 webnn::tflite::GraphImplTflite::CreateAndBuildOnBackgroundThread graph_impl_tflite.cc:542:20

0x7bbf758461b1 is located 0 bytes after 1-byte region [0x7bbf758461b0,0x7bbf758461b1)
allocated by thread T49 here:
    #0 malloc
    #1 TfLiteTensorResizeMaybeCopy common.cc
    #2 tflite::Subgraph::ResizeTensorImpl subgraph.cc:2077:7
    #3 tflite::Subgraph::ResizeTensor subgraph.cc:1844:9
    #4 tflite::ops::builtin::strided_slice::ResizeOutputTensor strided_slice.cc:242:7
    #5 tflite::ops::builtin::strided_slice::Prepare strided_slice.cc:333:32
    #6 tflite::Subgraph::PrepareOpsStartingAt subgraph.cc:1540:44
    #7 tflite::Subgraph::PrepareOpsAndTensors subgraph.cc:1588:7
    #8 tflite::Subgraph::AllocateTensors subgraph.cc:1035:25
    #9 webnn::tflite::GraphImplTflite::ComputeResources::Create graph_impl_tflite.cc:221:34
    #10 webnn::tflite::GraphImplTflite::CreateAndBuildOnBackgroundThread graph_impl_tflite.cc:542:20

SUMMARY: AddressSanitizer: heap-buffer-overflow portable_tensor.h:128:45 in StridedSlice<signed char>
==378626==ABORTING

```
## Credit

Please use c6eed09fc8b174b0f3eebedcceb1e792 as the credit for this vulnerability. Thank you.

## Attachments

- [poc.html](attachments/poc.html) (text/html, 2.8 KB)
- [asan.log](attachments/asan.log) (text/plain, 65.3 KB)

## Timeline

### je...@gmail.com (2026-03-25)

Please note that this vulnerability also requires a large memory allocation. Therefore, if you are using ClusterFuzz to reproduce it, please ensure a timeout of at least one minute and a memory allocation of at least 16GB.

### wf...@chromium.org (2026-03-25)

component is from `third_party/tflite/DIR_METADATA`

### je...@gmail.com (2026-03-26)

You can assign it to the team working on issue #493310462(<https://issues.chromium.org/u/5/issues/493310462>), as they previously fixed a similar issue for me.

### wf...@chromium.org (2026-03-27)

this is a memory corruption write in GPU process (sandboxed: non-android) accessible from the web, so it's a sev-high.

### ch...@google.com (2026-03-28)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-03-28)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security Impact hotlist or the Severity field, and remove the ReleaseBlock hotlist.

### ch...@google.com (2026-03-28)

Setting Priority to P1 to match Severity s1. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### ph...@chromium.org (2026-03-30)

Since we already disabled WebNN by default, decreasing severity.

### ly...@google.com (2026-04-01)

Should be resolved in <https://github.com/google-ai-edge/LiteRT/commit/9cfd6731e01199d0c846a20b619637fb531a7ac2>.

### ly...@google.com (2026-04-01)

TFLite change is rolled to ToT <https://chromium-review.git.corp.google.com/c/chromium/src/+/7718680>, mark this bug as fixed.

### aj...@google.com (2026-06-18)

-> S0 as this includes Android.

### ch...@google.com (2026-06-19)

This is sufficiently serious that it should be merged to M148. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M148. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Security Merge Request:

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

This is sufficiently serious that it should be merged to M149. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M149. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to M150. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M150. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

### ch...@google.com (2026-06-19)

**M148** merge request created. **Please update [crbug/525661666](https://crbug.com/525661666) to have this merge reviewed.**

### ch...@google.com (2026-06-19)

**M149** merge request created. **Please update [crbug/525661650](https://crbug.com/525661650) to have this merge reviewed.**

### ch...@google.com (2026-06-19)

**M150** merge request created. **Please update [crbug/525661985](https://crbug.com/525661985) to have this merge reviewed.**

### re...@chromium.org (2026-06-22)

Adding the Security\_Impact-None hotlist because WebNN hasn't shipped.

### sp...@google.com (2026-06-22)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $43000.00 for this report.

Rationale for this decision:
High quality. ASAN write with renderer and bisect. Nice!


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-07-09)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ch...@google.com (2026-07-10)

This Blink bug has been marked as either a release blocker or a vulnerability bug. Blink bugs affect all OSs supported by Chrome (except iOS), so the OS field has been updated to reflect this. Please update the bug with the correct OS field if it only affects a subset of OSes.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/495864183)*
