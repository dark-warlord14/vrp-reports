# Integer overflow in XNNPACK MaxPool2d indirection buffer sizing leads to heap out-of-bounds write in GPU process

| Field | Value |
|-------|-------|
| **Issue ID** | [493082093](https://issues.chromium.org/issues/493082093) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Internals>OptimizationGuide |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | je...@gmail.com |
| **Assignee** | ph...@chromium.org |
| **Created** | 2026-03-16 |
| **Bounty** | $43,000.00 |

## Description

# Integer overflow in XNNPACK MaxPool2d indirection buffer sizing leads to heap out-of-bounds write in GPU process

## Summary

An integer overflow in XNNPACK's max pooling operator allows a web page to crash the GPU process via the WebNN API. The function `reshape_max_pooling2d_nhwc` computes the size of an indirection buffer using unchecked `size_t` arithmetic on attacker-controlled kernel dimensions. By choosing two pooling window dimensions whose product is slightly above 2^60, the resulting buffer size wraps around 2^64 to a small value. XNNPACK allocates this undersized buffer and then writes into it using indices derived from the true, enormous kernel, producing a heap out-of-bounds write that crashes the GPU process almost immediately. The bug is reachable from any origin through the WebNN `maxPool2d` JavaScript API on platforms where TFLite is the active WebNN backend. On Linux and ChromeOS, TFLite is the default backend and the vulnerability triggers with no special flags. On Windows, the default backend is ONNX Runtime, which handles the operation safely; the bug triggers only when ORT is unavailable (Windows App Runtime not installed) or explicitly disabled, causing a fallback to TFLite. On macOS, the default backend is CoreML, and TFLite is similarly a fallback.

Platform: Linux, ChromeOS (default config); Windows, macOS (TFLite fallback only). No GPU requirement.

## Root Cause

WebNN's graph validation layer checks that individual pooling window dimensions are nonzero, that the effective filter size fits in a `uint32_t`, and that the output tensor dimensions are representable. It does not, however, place any upper bound on the window dimensions themselves, nor does it verify that the product of window height and width is safe for downstream arithmetic. The only multiplication overflow check on window size exists for L2 pooling and is absent for max and average pooling.

When a `maxPool2d` operation reaches the XNNPACK delegate through TFLite, the function `reshape_max_pooling2d_nhwc` recalculates pooling geometry using native `size_t` arithmetic:

```
// third_party/xnnpack/src/src/operators/max-pooling-nhwc.c:474-488
const size_t pooling_height = max_pooling_op->convolution_op->kernel_height;
const size_t pooling_width = max_pooling_op->convolution_op->kernel_width;
const size_t pooling_size = pooling_height * pooling_width;
const size_t output_height = max_pooling_op->convolution_op->output_height;
const size_t output_width = max_pooling_op->convolution_op->output_width;

const size_t step_width =
  max_pooling_op->convolution_op->dilation_width > 1
    ? pooling_width
    : min(max_pooling_op->convolution_op->stride_width, pooling_width);
const size_t step_height =
  pooling_size + (output_width - 1) * step_width * pooling_height;

const size_t indirection_buffer_size =
  sizeof(void*) * ((pooling_size - 1) + output_height * step_height);

```

None of these multiplications are checked for overflow. With `kernel_height = 0x40010000` (1073774592) and `kernel_width = 0x3FFF8001` (1073709057), `pooling_size` evaluates to approximately 2^60 + 32768. When `output_height` and `output_width` are both 1, `step_height` equals `pooling_size` and the final expression becomes `sizeof(void*) * (2 * pooling_size - 1)`, which is 2^64 + 524280. On a 64-bit platform this wraps to 524280. XNNPACK allocates a 524280-byte buffer, enough for 65535 pointers.

The subsequent call to `xnn_indirection_init_maxpool2d` iterates over the full kernel dimensions and writes pointer values into the buffer using an index computed from the real kernel geometry:

```
// third_party/xnnpack/src/src/indirection.c:415-422
for (size_t output_y = 0; output_y < output_height; output_y++) {
  for (size_t pooling_y = 0; pooling_y < kernel_height; pooling_y++) {
    for (size_t output_x = 0; output_x < output_width; output_x++) {
      for (size_t pooling_x = 0; pooling_x < kernel_width; pooling_x++) {
        const size_t index = output_y * step_height
          + output_x * step_width * kernel_height
          + pooling_x * kernel_height + pooling_y;
        indirection_buffer[index] = ...;
      }
    }
  }
}

```

With `output_height = output_width = 1`, the outer two loops execute once, and the inner two loops iterate across the full kernel. The first iteration (`pooling_x=0, pooling_y=0`) writes at index 0 (valid). The second iteration (`pooling_x=1, pooling_y=0`) writes at index `kernel_height` = 0x40010000, which is approximately 8 GB past the 524 KB buffer. This is a stable, immediate out-of-bounds write that crashes the GPU process on the second store.

The attacker keeps both input and output tensors at the minimum size of 1x1x1x1 by supplying explicit padding values that match SAME semantics. For a 1x1 input with stride 1, the SAME padding for a given kernel dimension `k` is `floor((k-1)/2)` on one side and `ceil((k-1)/2)` on the other. WebNN's TFLite serializer recognizes these values as equivalent to SAME padding and emits a TFLite `MAX_POOL_2D` node with `Padding_SAME`, which XNNPACK's delegate processes through `VisitMaxPool2DNode` and `xnn_define_max_pooling_2d`. The define-time validation in XNNPACK computes the pooling size as a `uint32_t`, which also wraps but to a nonzero value, passing the only guard (`pooling_size == 0`). The true overflow occurs later in the reshape phase where `size_t` arithmetic is used.

## Reproduce

This reproduction targets Chromium commit `9e902837356530423619fe4f1445f24a39e879f8`. Check out that revision with `git checkout 9e902837356530423619fe4f1445f24a39e879f8`.

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
  --user-data-dir=/tmp/poc-xnnpack \
  --enable-logging=stderr \
  file://$(pwd)/issue_xnnpack_maxpool_overflow/poc.html

```

The `--no-sandbox` flag is required for ASAN to function correctly in child processes; without it, the GPU process's seccomp-bpf sandbox prevents ASAN's signal handler from operating. Do not use `--disable-gpu` as the vulnerability is in the GPU process.

The GPU process will crash with `SIGSEGV` (exit\_code=11) within seconds of opening the page. The symbolized crash stack shows the overflow path:

```
#4  xnn_indirection_init_maxpool2d        third_party/xnnpack/src/src/indirection.c:422
#5  reshape_max_pooling2d_nhwc            third_party/xnnpack/src/src/operators/max-pooling-nhwc.c:506
#6  xnn_reshape_max_pooling2d_nhwc_f32    third_party/xnnpack/src/src/operators/max-pooling-nhwc.c:635
#7  reshape_max_pooling_operator          third_party/xnnpack/src/src/subgraph/max-pooling-2d.c:164
#8  xnn_reshape_runtime                   third_party/xnnpack/src/src/runtime.c:877
#9  tflite::xnnpack::SubgraphPrepare()    third_party/tflite/.../xnnpack_delegate.cc:1266
#10 tflite::Subgraph::PrepareOpsStartingAt()  third_party/tflite/.../subgraph.cc:1540
#11 tflite::Subgraph::AllocateTensors()   third_party/tflite/.../subgraph.cc:1035
#12 webnn::tflite::GraphImplTflite::ComputeResources::Create()  services/webnn/tflite/graph_impl_tflite.cc:221
#13 webnn::tflite::GraphImplTflite::CreateAndBuildOnBackgroundThread()  services/webnn/tflite/graph_impl_tflite.cc:542

```

The full symbolized Linux crash log is provided in `asan_linux.log`.

### Windows (TFLite fallback)

On Windows, the default WebNN backend is ONNX Runtime. Disable it to force the TFLite/XNNPACK path:

```
set ASAN_OPTIONS=detect_odr_violation=0
out\asan-release\chrome.exe --no-sandbox ^
  --enable-features=WebMachineLearningNeuralNetwork ^
  --disable-features=WebNNOnnxRuntime ^
  --user-data-dir=%TEMP%\poc-xnnpack ^
  --enable-logging=stderr ^
  file:///path/to/issue_xnnpack_maxpool_overflow/poc.html

```

ASAN output from the Windows GPU process:

```
==8156==ERROR: AddressSanitizer: access-violation on unknown address 0x02f2e3990300 (pc 0x7ff833c363d2 bp 0x000000000001 sp 0x00f7b0bfe660 T9)
==8156==The signal is caused by a READ memory access.
    #0 0x7ff833c363d1 in xnn_indirection_init_maxpool2d D:\chromium\src\third_party\xnnpack\src\src\indirection.c:422
    #1 0x7ff833e3bb43 in reshape_max_pooling2d_nhwc D:\chromium\src\third_party\xnnpack\src\src\operators\max-pooling-nhwc.c:506
    #2 0x7ff833e3c82f in xnn_reshape_max_pooling2d_nhwc_f32 D:\chromium\src\third_party\xnnpack\src\src\operators\max-pooling-nhwc.c:635
    #3 0x7ff833fa9f55 in reshape_max_pooling_operator D:\chromium\src\third_party\xnnpack\src\src\subgraph\max-pooling-2d.c:164
    #4 0x7ff833c60ebd in xnn_reshape_runtime D:\chromium\src\third_party\xnnpack\src\src\runtime.c:877
    #5 0x7ff8504a5e4c in tflite::xnnpack::SubgraphPrepare D:\chromium\src\third_party\tflite\src\tensorflow\lite\delegates\xnnpack\xnnpack_delegate.cc:7211
    #6 0x7ff84b1d3e45 in tflite::Subgraph::PrepareOpsStartingAt D:\chromium\src\third_party\tflite\src\tensorflow\lite\core\subgraph.cc:1540
    #7 0x7ff84b1d052e in tflite::Subgraph::PrepareOpsAndTensors D:\chromium\src\third_party\tflite\src\tensorflow\lite\core\subgraph.cc:1588
    #8 0x7ff84b1ceb0f in tflite::Subgraph::AllocateTensors D:\chromium\src\third_party\tflite\src\tensorflow\lite\core\subgraph.cc:1035
    #9 0x7ff855491501 in webnn::tflite::GraphImplTflite::ComputeResources::Create D:\chromium\src\services\webnn\tflite\graph_impl_tflite.cc:221
    #10 0x7ff85548f465 in webnn::tflite::GraphImplTflite::CreateAndBuildOnBackgroundThread D:\chromium\src\services\webnn\tflite\graph_impl_tflite.cc:542

```
## Credit

Please use c6eed09fc8b174b0f3eebedcceb1e792 as the credit for this vulnerability. Thank you.

## Attachments

- [poc.html](attachments/poc.html) (text/html, 3.1 KB)
- [asan.log](attachments/asan.log) (text/plain, 8.0 KB)
- [asan_linux.log](attachments/asan_linux.log) (text/plain, 5.3 KB)

## Timeline

### je...@gmail.com (2026-03-17)

## Bisect

### XNNPACK upstream

- Commit: b455b1209fc0f28eef8ef647fcd4425705363bcf
- Date: 2019-09-27
- Author: XNNPACK Team
- Subject: Initial open-source release
- URL: <https://github.com/google/XNNPACK/commit/b455b1209fc0f28eef8ef647fcd4425705363bcf>

The unchecked size\_t arithmetic for indirection\_buffer\_size has existed since XNNPACK's very first open-source commit. Every subsequent refactor changed the terms in the formula but never added overflow checks.

### First rolled into Chromium

- Commit: 85e288dd5b7281bb261ae332938f2d0246d616f3
- Date: 2022-04-26
- Author: Robert Ogden
- Subject: Add XNNPACK Support to TFLite on Linux\_x64
- Review: <https://chromium-review.googlesource.com/c/chromium/src/+/3606753>

### Became web-reachable

- Commit: 6c9e4fea79849343c09bae0214cd76904f43be22
- Date: 2024-03-13
- Author: Junwei Fu ([junwei.fu@intel.com](mailto:junwei.fu@intel.com))
- Subject: webnn: Support Pool2d in //services/webnn/tflite
- Review: <https://chromium-review.googlesource.com/c/chromium/src/+/5359192>

This commit added SerializePool2d() which passes uint32\_t window dimensions directly to TFLite's CreatePool2DOptions without upper-bound validation, allowing attacker-chosen kernel sizes to flow from the WebNN JS API through TFLite into XNNPACK's vulnerable reshape path.

### cl...@appspot.gserviceaccount.com (2026-03-18)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4688405292154880.

### ts...@google.com (2026-03-18)

Assigning to tech lead, please re-assign as appropriate.

### ts...@google.com (2026-03-18)

Setting provisional OS to desktop and found-in to extended stable.

### ch...@google.com (2026-03-19)

Setting milestone because of s0/s1 severity.

### da...@google.com (2026-04-13)

Mike, can you triage this and fine the right owner? These are high priority to address.

### je...@gmail.com (2026-04-14)

<https://issues.chromium.org/u/5/issues/493747582#comment9>
Please check if the fix for this issue also resolves the problem. These are two completely different vulnerabilities, but there might be a unified high-level fix for them.

> [-] Exception: TypeError: Failed to execute 'maxPool2d' on 'MLGraphBuilder': The padded intermediate operand is invalid: Invalid descriptor: The number of elements is too large.

### wi...@chromium.org (2026-04-14)

WebNN exploits can be assigned to [services/webnn/OWNERS](https://source.chromium.org/chromium/chromium/src/+/main:services/webnn/OWNERS).

### ph...@chromium.org (2026-04-21)

I think this is fixed.
It's now returning:

```
[-] Exception: TypeError: Failed to execute 'maxPool2d' on 'MLGraphBuilder': The padded intermediate operand is invalid: Invalid descriptor: The number of elements is too large.

```

### ch...@google.com (2026-04-21)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### je...@gmail.com (2026-04-24)

Hi, Can you mark and confirm it as Fixed?

### sp...@google.com (2026-05-14)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $43000.00 for this report.

Rationale for this decision:
High quality with bisect - Memory corruption in a highly privileged process (e.g. GPU, network processes) 


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-05-20)

This is sufficiently serious that it should be merged to M148. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M148. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Security Merge Request:

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

This is sufficiently serious that it should be merged to M149. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M149. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

### ch...@google.com (2026-05-20)

**M148** merge request created. **Please update [crbug/514925137](https://crbug.com/514925137) to have this merge reviewed.**

### ch...@google.com (2026-05-20)

**M149** merge request created. **Please update [crbug/514928523](https://crbug.com/514928523) to have this merge reviewed.**

### eb...@google.com (2026-08-13)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/493082093)*
