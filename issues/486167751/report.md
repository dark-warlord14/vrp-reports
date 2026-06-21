# WebNN LiteRT: heap-buffer-overflow write in XNNPACK subconv2d via convTranspose2d

| Field | Value |
|-------|-------|
| **Issue ID** | [486167751](https://issues.chromium.org/issues/486167751) |
| **Status** | Verified |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | Blink>WebML |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | to...@gmail.com |
| **Assignee** | re...@chromium.org |
| **Created** | 2026-02-20 |
| **Bounty** | $25,000.00 |

## Description

---

### Report description

WebNN LiteRT: heap-buffer-overflow write in XNNPACK subconv2d via convTranspose2d

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

#### Which URL (or repository) have you found the vulnerability in?

<https://source.chromium.org/chromium/chromium/src/+/main:services/webnn/tflite/buffer_content_tflite.cc>

---

### The problem

#### Please describe the technical details of the vulnerability

# XNNPACK heap-buffer-overflow (OOB Write) via WebNN LiteRT convTranspose2d

## Environment

Ubuntu + AMD processor (for completeness, shouldn't matter).

## Base Chromium revision

```
a0062e558d37e03d9129522e5a3c6c29946d8195 (2026-02-10)

```
## GN args

```
is_asan = true
is_debug = false
webnn_use_litert = true

```
## Build

```
cd chromium/src
gn gen out/litert_asan
autoninja -C out/litert_asan content_shell

```
## Running the PoC

The LiteRT backend is selected via the `webnn_use_litert` build flag. Because it runs in the GPU process (`--single-process` merges all processes so ASAN output is visible on stderr):

```
xvfb-run --auto-servernum ./out/litert_asan/content_shell \
  --no-sandbox --single-process \
  --enable-blink-features=MachineLearningNeuralNetwork \
  file:///path/to/poc.html

```

The crash occurs during `ctx.dispatch()` (inference). The poc.html file is included in this report.

## ASAN output

```
==3198744==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x7a9607f98390 at pc 0x59b44f7c1419 bp 0x7965e97f8bf0 sp 0x7965e97f8be8
WRITE of size 4 at 0x7a9607f98390 thread T9 (ThreadPoolForeg)
    #0 xnn_f32_igemm_minmax_ukernel_1x8__fma3_broadcast  third_party/xnnpack/src/src/f32-igemm/gen/f32-igemm-1x8-minmax-fma3-broadcast.c:109:9
    #1 xnn_compute_subconv2d                              third_party/xnnpack/src/src/operator-run.c:1243:3
    #2 thread_parallelize_5d_tile_2d                      third_party/pthreadpool/src/src/portable-api.c:3152:5
    #3 PthreadPoolJob::Run(base::JobDelegate*)            third_party/pthreadpool/chromium/jobs.cc:165:5
    ...
    #8 pthreadpool_parallelize                            third_party/pthreadpool/chromium/jobs.cc:297:10
    #9 pthreadpool_parallelize_5d_tile_2d                 third_party/pthreadpool/src/src/portable-api.c:5467:5
    #10 xnn_run_operator_with_index                       third_party/xnnpack/src/src/operator-run.c:2691:9
    #11 xnn_invoke_runtime                                third_party/xnnpack/src/src/runtime.c:1207:38
    #12 SubgraphInvoke                                    third_party/tflite/src/tensorflow/lite/delegates/xnnpack/xnnpack_delegate.cc:1421:25
    #13 tflite::Subgraph::InvokeImpl()                    third_party/tflite/src/tensorflow/lite/core/subgraph.cc
    #14 tflite::Subgraph::Invoke()                        third_party/tflite/src/tensorflow/lite/core/subgraph.cc:1653:17
    #15 LiteRtCompiledModelT::Run(...)                    third_party/litert/src/litert/runtime/compiled_model.cc:1357:26
    ...
    #21 DoDispatch                                        services/webnn/tflite/graph_impl_litert.cc

0x7a9607f98390 is located 16 bytes after 320-byte region [0x7a9607f98240,0x7a9607f98380)
allocated by thread T5 (ThreadPoolSingl) here:
    #0 posix_memalign
    #1 base::AlignedAlloc(unsigned long, unsigned long)   base/memory/aligned_memory.cc:35:13
    #2 webnn::tflite::BufferContent::BufferContent(unsigned long)  services/webnn/tflite/buffer_content_tflite.cc:33:15
    #3 webnn::tflite::TensorImplTflite::Create(...)       gen/third_party/libc++/src/include/__memory/unique_ptr.h:756:30
    #4 ContextImplLiteRt::CreateTensorImpl(...)            services/webnn/tflite/context_impl_litert.cc:126:10

SUMMARY: AddressSanitizer: heap-buffer-overflow third_party/xnnpack/src/src/f32-igemm/gen/f32-igemm-1x8-minmax-fma3-broadcast.c:109:9

```
## Root cause

`BufferContent::BufferContent()` in `buffer_content_tflite.cc` (line 33) allocates output tensors as:

```
buffer_(base::AlignedAlloc(AddPaddingIfNecessary(size),
                           ::tflite::kDefaultTensorAlignment))

```

where `AddPaddingIfNecessary()` adds `XNN_EXTRA_BYTES` (16 bytes on x86\_64). The inline comment says "XNNPACK may read up to XNN\_EXTRA\_BYTES beyond the buffer."

`DoDispatch()` in `graph_impl_litert.cc` (line 236) passes this buffer to LiteRT:

```
base::span<uint8_t> data = buffers.at(output.tensor_index)->AsSpan();
auto litert_buffer_or = ::litert::TensorBuffer::CreateFromHostMemory(
    *env_, tensor_type, data.data(), data.size());

```

`AsSpan()` returns only the logical tensor size (without the extra 16 bytes). LiteRT and the underlying XNNPACK runtime then operate directly on this buffer.

As the ASAN trace shows, for `convTranspose2d` with `stride=[3,3]`, XNNPACK's `xnn_compute_subconv2d` path ends up writing past the allocation via the IGEMM microkernel (`_mm_store_ss` at `f32-igemm-1x8-minmax-fma3-broadcast.c:109`).

For the PoC shapes (input `[1,2,7,3]`, filter `[1,3,3,3]`, stride `[3,3]`, output `[1,4,19,1]`):

- Logical output: 76 floats = 304 bytes
- Allocation: 304 + 16 = 320 bytes
- XNNPACK writes at offset 336: 16 bytes past the allocation

#### Impact analysis

## Affected platforms

Tested on Linux (x86\_64) with the LiteRT+XNNPACK backend. The LiteRT backend is selected at build time via `webnn_use_litert = true`. XNNPACK is used when `build_tflite_with_xnnpack` is true, which is the case on all platforms except ARM32 and Fuchsia (see `third_party/tflite/features.gni`).

## Impact

- **Attack vector:** Any website, no user interaction required beyond navigation. WebNN is behind a feature flag (`MachineLearningNeuralNetwork`), which is not yet enabled by default, but eligible for VRP according to the [rules](https://bughunters.google.com/about/rules/chrome-friends/chrome-vulnerability-reward-program-rules#chrome-fuzzer-program:~:text=Bugs%20in%20unlaunched,message%20at%20runtime.) and it is also in origin trial since Jan 31: <https://chromium-review.googlesource.com/c/chromium/src/+/7518276>.
- **Process:** GPU process.
- **Primitive:** OOB heap write. The overflow is a 4-byte write 16 bytes past a 320-byte heap allocation.
- **Consequence:** Heap corruption in the GPU process.

---

### The cause

#### What version of Chrome have you found the security issue in?

147.0.7681.0 dev

#### Is the security issue related to a crash?

Yes, it is related to a crash.

#### Choose the type of vulnerability

Memory Corruption (in a non-sandboxed process)

#### How would you like to be publicly acknowledged for your report?

Tobias Wienand

## Attachments

- [poc.html](attachments/poc.html) (text/html, 2.2 KB)
- [model0.tflite](attachments/model0.tflite) (application/octet-stream, 904 B)
- [Fri Feb 20 2026 17:17:46 GMT-0800 (Pacific Standard Time).png](attachments/Fri Feb 20 2026 17_17_46 GMT-0800 (Pacific Standard Time).png) (image/png, 125.8 KB)

## Timeline

### an...@chromium.org (2026-02-20)

Provisionally set FoundIn to M147 as I haven't tried reproducing this myself. Also marked Security Impact as None because of the feature being experimental.

### re...@chromium.org (2026-02-20)

The `webnn_use_litert` flag is still disabled but I appreciate Tobias looking at this path because it is going to be the default soon.

### an...@chromium.org (2026-02-20)

@re...@chromium.org can you suggest an assignee for this issue?

### re...@chromium.org (2026-02-20)

It looks like this might be the same XNNPACK bug as I was trying to investigate in [issue 378101116](https://issues.chromium.org/issues/378101116) before the test case I had for that issue stopped reproducing the issue. In that case the OOB write was in `xnn_f32_igemm_minmax_ukernel_4x2c4__sse` but I whatever bounds checking error might be in the caller rather than either that or `xnn_f32_igemm_minmax_ukernel_1x8__fma3_broadcast` itself. Or the same logic error is present in both kernels.

### an...@chromium.org (2026-02-20)

Thanks for that info. I'll go ahead and assign this issue to you then. Feel free to mark it as a duplicate of [issue 378101116](https://issues.chromium.org/issues/378101116) if the root cause turns out to be the same.

### re...@chromium.org (2026-02-20)

Dillon, adding you here in case you're curious and want to take a look at this before I get a chance to. I can attach the TFLite model that reproduces this if the root cause isn't obvious from the PoC and you need to run it through TFLite or LiteRT without the added weight of Chrome involved.

### cl...@appspot.gserviceaccount.com (2026-02-20)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5274316442632192.

### re...@chromium.org (2026-02-20)

It looks like the reason this only reproduces under LiteRT is that TFLite rejects the model by returning an error from `Interpreter::AllocateTensors()`. ClusterFuzz doesn't build with LiteRT so it can't reproduce the issue.

### ds...@google.com (2026-02-20)

I think cl/873079506 will fix this, but I'm not 100% sure, please try it and let me know if this is still an issue.

### re...@chromium.org (2026-02-21)

Unfortunately it does not. See the attached TFLite model.

### ds...@google.com (2026-02-21)

Hmm, that model doesn't reproduce any asan failures, either before or after my fix. I'm a little suspicious because the graph in that tflite file contains an explicit padding op (see attachement), so it might not actually be exercising the buggy codepath.

### ds...@google.com (2026-02-21)

I've now replicated (I think) exactly the case reported here:

```
input_shape={1, 2, 7, 3}
output_shape={1, 4, 19, 1}
filter_shape={1, 3, 3, 3}
kh={.size=3, .dilation=1, .stride=3, .padding_min=1, .padding_max=1}
kw={.size=3, .dilation=1, .stride=3, .padding_min=1, .padding_max=1}

```

This seems to pass with --config=asan. But it passes both before and after my fix, so we're still missing something about the repro.

### re...@chromium.org (2026-02-21)

The PAD operator is added by the code here, which figures out whether padding is required for TFLite's implementation to match WebNN's padding semantics:

<https://source.chromium.org/chromium/chromium/src/+/main:services/webnn/tflite/graph_builder_tflite.cc;l=4068;drc=ce45888b8732e18758b0ee299bc307c2be7e062e>

I don't entirely trust that the logic in `GetTfLitePaddingMode` is correct.

As a sanity check, are you sure that whatever harness you are using is allocating buffers of the correct size for ASan to be complaining as it does?

### ds...@google.com (2026-02-21)

I believe so. It's unfortunately fairly complicated logic, because we allocate extra space before/after the buffer so we can "manually" detect OOB writes (for platforms without asan). But we poison those bytes for asan/msan.

Note that when I tested model0.tflite, I used TFLite's `benchmark_model` tool, so that is a different, independent implementation.

### re...@chromium.org (2026-02-21)

I'm surprised that `benchmark_tool` worked because it seems like, at least with the version and configuration of TFLite used in Chrome this model will fail to load because `Interpreter::AllocateTensors()` returns `kTfLiteError`, while it loads successfully with LiteRT and then hits this ASan error. I need to rebuild Chrome with TFLite's debug logging enabled to understand the cause of that error.

However, while reproducing this locally I've also discovered that there is a flaw in how we build LiteRT in Chrome ([issue 486228093](https://issues.chromium.org/issues/486228093)) which may cause any number of pathological behaviors in LiteRT and XNNPACK so we might be chasing ghosts here.

### re...@chromium.org (2026-03-04)

I can still reproduce this after resolving [issue 486228093](https://issues.chromium.org/issues/486228093).

The reason this isn't failing in the TFLite case is that TFLite rejects the custom allocation we use for the input tensor because it doesn't match the size of the tensor in the graph. In this case we allocate a 304 byte tensor but TFLite expects a 1,456 byte buffer. I expect that some transformation has occurred during either the graph building or loading process which causes the tensor size or shape to mismatch.

### re...@chromium.org (2026-03-04)

TFLite thinks the output tensor should be [1,13,28,1] instead of the [1,4,19,1] shape that we expect.

### dx...@google.com (2026-03-05)

Project: chromium/src  

Branch:  main  

Author:  Reilly Grant [reillyg@chromium.org](mailto:reillyg@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7635520>

webnn: Check that TFLite and WebNN tensor sizes match

---


Expand for full commit details
```
     
    Add checks after the generated TFLite model has been loaded that its 
    input and output tensors are the sizes that we expect them to be. 
     
    Bug: 486167751 
    Change-Id: I83dc396204a05477ea94bde2f236cbd5629b2ab9 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7635520 
    Auto-Submit: Reilly Grant <reillyg@chromium.org> 
    Reviewed-by: Hu, Ningxin <ningxin.hu@intel.com> 
    Commit-Queue: Hu, Ningxin <ningxin.hu@intel.com> 
    Cr-Commit-Position: refs/heads/main@{#1594456}

```

---

Files:

- M `services/webnn/tflite/graph_impl_tflite.cc`
- M `third_party/blink/web_tests/platform/mac/virtual/webnn-service-with-gpu/external/wpt/webnn/conformance_tests/conv_transpose2d.https.any_gpu-expected.txt`
- M `third_party/blink/web_tests/virtual/webnn-service-on-cpu/external/wpt/webnn/conformance_tests/conv_transpose2d.https.any_cpu-expected.txt`
- M `third_party/blink/web_tests/virtual/webnn-service-on-npu/external/wpt/webnn/conformance_tests/conv_transpose2d.https.any_npu-expected.txt`

---

Hash: [cdac78194a2c3588df9f25738d7d1501ca52bab7](https://chromiumdash.appspot.com/commit/cdac78194a2c3588df9f25738d7d1501ca52bab7)  

Date: Thu Mar 5 04:40:43 2026


---

### re...@chromium.org (2026-03-06)

The change of shape is caused by the XNNPACK delegate using XNNPACK's subgraph reshaping feature. This is supposed to optimize the graph for dynamic shapes but by changing the size of a graph output it means WebNN and TFLite no longer agree on the correct tensor shapes.

### re...@chromium.org (2026-03-11)

<https://chromium-review.googlesource.com/7630663> fixes the immediate crash when using LiteRT by doing the same buffer size checks as I added in in [comment #19](https://issues.chromium.org/issues/486167751#comment19). However we still need to understand the underlying XNNPACK behavior that causes this.

### re...@chromium.org (2026-03-11)

Marking the vulnerability aspect of this as fixed. No merge to release branches is necessary as this was only exploitable with additional build flags set. The underlying issue is tracked in [issue 491869941](https://issues.chromium.org/issues/491869941).

### wf...@chromium.org (2026-03-18)

memory corruption in GPU on Android accessible from the web is sev-critical

### sp...@google.com (2026-03-20)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $25000.00 for this report.

Rationale for this decision:
Baseline memory corruption in a non-sandboxed process


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-06-18)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/486167751)*
