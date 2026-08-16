# OOB read in TFLite TransposeConvV2

| Field | Value |
|-------|-------|
| **Issue ID** | [505063249](https://issues.chromium.org/issues/505063249) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Blink>WebML |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | he...@gmail.com |
| **Assignee** | ju...@intel.com |
| **Created** | 2026-04-22 |
| **Bounty** | $3,000.00 |

## Description

Security Bug

Important: Please do not change the component of this bug manually.

Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/faq.md>

Please see the following link for instructions on filing security bugs: <https://www.chromium.org/Home/chromium-security/reporting-security-bugs>

Reports may be eligible for reward payments under the Chrome VRP: <https://g.co/chrome/vrp>

NOTE: Security bugs are normally made public once a fix has been widely deployed.

---

# Steps to reproduce the problem

## Steps to reproduce

1. In Windows, build ASAN Chrome:
   - Chromium commit `91c469d813f74136b9eff1861c8ffdbbbc30fe48` (Apr 9, 2026)
   - `args.gn`:

```
dcheck_always_on = false
enable_ipc_fuzzer = true
is_asan = true
is_clang = true
is_component_build = false
is_debug = false
target_cpu = "x64"
target_os = "win"
use_siso = true
v8_enable_verify_heap = true
symbol_level = 2

```

2. Place `poc.html` in a local folder, then start a local server:
   - `python3 -m http.server 8000`
3. Launch ASAN Chrome with WebNN enabled, force TFLite backend, and use `--no-sandbox` for ASAN output:
   - `.\chrome.exe --enable-features=WebMachineLearningNeuralNetwork --disable-features=WebNNOnnxRuntime,WebNNDirectML,WebNNLiteRT --no-sandbox http://localhost:8000/poc.html`
4. GPU process crashes. On ASAN build, log shows:
   - `AddressSanitizer: access-violation`

# Problem Description

### Description

This issue is a signed integer overflow in TFLite transpose-convolution `Col2im` index arithmetic, reachable from WebNN JS on forced TFLite backend.

### Impact

From an uncompromised renderer WebNN graph, this causes GPU process crash.  

On ASAN builds, this is detected as:

- `AddressSanitizer: access-violation`

### Root Cause

The root cause is unchecked signed `int` arithmetic when deriving output patch pointer offset:

```
// third_party/tflite/src/tensorflow/lite/kernels/internal/optimized/optimized_ops.h
T* im_patch_data = im_data + (h_pad * width + w_pad) * depth;

```

For this PoC, `h_pad` starts as `-pad_t`, and:

- `padTop=2000`
- `outputWidth=59971`
- `outputDepth=18`
- `padTop * outputWidth * outputDepth = 2158956000 > INT32_MAX`

So signed 32-bit intermediate overflows before pointer addition, and subsequent write:

```
im_patch_data[i] += col_data[i];

```

can access **out-of-bounds** memory.

### mitigation suggestion

Use checked 64-bit arithmetic for all `Col2im` pointer/index computations and reject configurations where any intermediate index/offset exceeds representable and bounded output region limits.

# Summary

WebNN/TFLite transpose-conv can trigger signed index overflow in `Col2im`, leading to GPU-process crash (`AddressSanitizer: access-violation` on ASAN).

# Custom Questions

#### Type of crash:

ASAN `access-violation` in GPU process.

#### Crash state:

ASAN stack trace root:

```
==19852==ERROR: AddressSanitizer: access-violation on unknown address 0x126543283780
==19852==The signal is caused by a READ memory access.
...
#0 0x7ffd02c86310 in tflite::optimized_ops::TransposeConvV2 ...\optimized_ops.h:5111
#1 0x7ffd02c83e79 in tflite::ops::builtin::transpose_conv::EvalFloat<1> ...\transpose_conv.cc:552
#2 0x7ffd02c7c840 in tflite::ops::builtin::transpose_conv::Eval<1> ...\transpose_conv.cc:859
#3 0x7ffd02374564 in tflite::Subgraph::InvokeImpl ...\subgraph.cc:1761
#6 0x7ffd0c1452fc in webnn::tflite::GraphImplTflite::ComputeResources::DoDispatch ...\graph_impl_tflite.cc:329
SUMMARY: AddressSanitizer: access-violation ...\optimized_ops.h:5111 in tflite::optimized_ops::TransposeConvV2

```

## Attachments

- [poc.html](attachments/poc.html) (text/html, 5.3 KB)
- [asan_log.txt](attachments/asan_log.txt) (text/plain, 11.7 KB)

## Timeline

### ns...@chromium.org (2026-04-22)

Thank you for your bug report.

Security-impact: none as this is a WebNN vuln.

P1/S1 as it looks like this is memory corruption on the GPU process for all platforms.

Over to the WebNN team.

Local testing trace:

```
3174799:3174799:0422/100716.979254:ERROR:services/webnn/webnn_context_provider_impl.cc:144] WebMachineLearningNeuralNetwork is an unsafe feature.
Created TensorFlow Lite XNNPACK delegate for CPU.
Received signal 11 SEGV_ACCERR 7bf601db2740
    #0 0x5582c145cd16 in ___interceptor_backtrace ??:0:0
    #1 0x5582dfa67e18 in base::debug::CollectStackTrace(base::span<void const*, 18446744073709551615ul, void const**>) ./../../base/debug/stack_trace_posix.cc:1050:7
    #2 0x5582dfa1796f in base::debug::StackTrace::StackTrace(unsigned long) ./../../base/debug/stack_trace.cc:280:20
    #3 0x5582dfa66f82 in base::debug::(anonymous namespace)::StackDumpSignalHandler(int, siginfo_t*, void*) ./../../base/debug/stack_trace_posix.cc:483:3
    #4 0x7ff635e40a70 in __GI___sigaction :?
    #5 0x5582e98e3cf5 in tflite::optimized_ops::TransposeConvV2(tflite::ConvParams const&, tflite::RuntimeShape const&, float const*, tflite::RuntimeShape const&, float const*, tflite::RuntimeShape const&, float const*, tflite::RuntimeShape const&, float*, tflite::RuntimeShape const&, float*, tflite::CpuBackendContext*) ./../../third_party/tflite/src/tensorflow/lite/kernels/internal/optimized/optimized_ops.h:5015:32
    #6 0x5582e98e1b15 in void tflite::ops::builtin::transpose_conv::EvalFloat<(tflite::ops::builtin::transpose_conv::KernelType)1>(TfLiteContext*, TfLiteTransposeConvParams const*, tflite::ops::builtin::transpose_conv::OpData const*, TfLiteTensor const*, TfLiteTensor const*, TfLiteTensor const*, TfLiteTensor const*, TfLiteTensor*, TfLiteTensor*) ./../../third_party/tflite/src/tensorflow/lite/kernels/transpose_conv.cc:552:7
    #7 0x5582e98d9ce0 in TfLiteStatus tflite::ops::builtin::transpose_conv::Eval<(tflite::ops::builtin::transpose_conv::KernelType)1>(TfLiteContext*, TfLiteNode*) ./../../third_party/tflite/src/tensorflow/lite/kernels/transpose_conv.cc:859:9
    #8 0x5582e58c0ec5 in tflite::Subgraph::InvokeImpl() ./../../third_party/tflite/src/tensorflow/lite/core/subgraph.cc:0:10
    #9 0x5582e58bfea5 in tflite::Subgraph::Invoke() ./../../third_party/tflite/src/tensorflow/lite/core/subgraph.cc:1653:17
    #10 0x5582e58a3ad6 in tflite::impl::Interpreter::Invoke() ./../../third_party/tflite/src/tensorflow/lite/core/interpreter.cc:246:48

```

### ns...@chromium.org (2026-04-22)

(I tested this on a build from 2026-04-21 so it doesn't look like a dupe of [issue 492668885](https://issues.chromium.org/issues/492668885).)

### qj...@chromium.org (2026-04-23)

:/ Looks like a bug in tflite?

+Ningxin

### re...@chromium.org (2026-04-23)

Wei is working on using generic limits as a general fix in this area.

### aj...@google.com (2026-04-23)

note that webnn is out of scope for the vrp at present

### ng...@gmail.com (2026-04-23)

The VRP FAQ at chromium.googlesource.com/chromium/src/+/HEAD/docs/security/vrp-faq.md states bugs in features behind command line flags are eligible, with the only exception being V8 --experimental. WebNN does not fall under that exception. Could you clarify under which written policy WebNN is currently excluded?

### aj...@google.com (2026-04-29)

RE comment 7 - webnn shows a clear message when [enabled in ASAN](https://chromium-review.googlesource.com/c/chromium/src/+/7728303) that it is unsafe.

### ng...@gmail.com (2026-04-29)

I understand, thank you for clarifying.

### dx...@google.com (2026-05-02)

Project: chromium/src  

Branch:  main  

Author:  Wei Wang [wei4.wang@intel.com](mailto:wei4.wang@intel.com)  

Link:    <https://chromium-review.googlesource.com/7801237>

[WebNN] Prevent TransposeConv2d col2im pointer offset overflow in TFLite

---


Expand for full commit details
```
     
    The col2im pointer offset in TFLite's optimized_ops.h is computed as 
    `(h_pad * width + w_pad) * depth`. This could allow a crafted input 
    to pass the current buffer size check while the actual offset overflows 
    int32, leading to an out-of-bounds memory access. 
     
    This CL adds a check to ensure the col2im pointer offset does not 
    exceed the maximum value of a 32-bit signed integer. 
     
    Bug: 505063249 
    Change-Id: I58d7c18f2fb76d1f82d3908dd43c79f16c57df5f 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7801237 
    Reviewed-by: Hu, Ningxin <ningxin.hu@intel.com> 
    Reviewed-by: Reilly Grant <reillyg@chromium.org> 
    Commit-Queue: Wang, Wei4 <wei4.wang@intel.com> 
    Cr-Commit-Position: refs/heads/main@{#1624216}

```

---

Files:

- M `services/webnn/tflite/graph_builder_tflite.cc`

---

Hash: [cb10fdc4932d59d0f208cb4de02c7447862f98cc](https://chromiumdash.appspot.com/commit/cb10fdc4932d59d0f208cb4de02c7447862f98cc)  

Date: Sat May 2 01:44:03 2026


---

### ch...@google.com (2026-08-14)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ch...@google.com (2026-08-15)

This Blink bug has been marked as either a release blocker or a vulnerability bug. Blink bugs affect all OSs supported by Chrome (except iOS), so the OS field has been updated to reflect this. Please update the bug with the correct OS field if it only affects a subset of OSes.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/505063249)*
