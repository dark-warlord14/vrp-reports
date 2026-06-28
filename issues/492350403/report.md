# Heap Buffer Overflow in TFLite + XNNPack via WebNN

| Field | Value |
|-------|-------|
| **Issue ID** | [492350403](https://issues.chromium.org/issues/492350403) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P0 |
| **Component** | Blink>WebML |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | to...@gmail.com |
| **Assignee** | re...@chromium.org |
| **Created** | 2026-03-13 |
| **Bounty** | $33,000.00 |

## Description

### Summary

[optimize\_common\_subgraphs\_scaled\_sum\_to\_mean](https://source.chromium.org/chromium/chromium/src/+/main:third_party/xnnpack/src/src/subgraph.c;l=2451) rewrites a broadcasted binary op into a unary `reduce_mean` without verifying that the singleton constant's rank doesn't exceed the reduced tensor's rank, silently dropping broadcasting semantics so that downstream convolution reshapes produce an undersized buffer and the heap-buffer-overflow.

### Details

The WebNN trigger is straightforward: `reduceSum(input, {axes:[0,1], keepDimensions:false})` produces a lower-rank tensor, and a following `div` or `mul` by a constant shaped `[1,1,1,1]` is still valid because Blink broadcasts the reduction result back up to rank 4. For the attached PoCs, the reduction result is logically `[16,8]`, while the binary output seen by WebNN/TFLite is `[1,1,16,8]`.

The rewrite in [optimize\_common\_subgraphs\_scaled\_sum\_to\_mean](https://source.chromium.org/chromium/chromium/src/+/main:third_party/xnnpack/src/src/subgraph.c;l=2451) treats any static one-element tensor as scalar-like and replaces the binary node with a unary reduce, but it never checks whether the binary op was relying on higher-rank broadcasting:

```
struct xnn_value* reduce_value = &subgraph->values[node->inputs[0]];
struct xnn_value* arg_value = &subgraph->values[node->inputs[1]];
if (xnn_shape_multiply_all_dims(&arg_value->shape) != 1 ||
    !xnn_value_is_static(arg_value->allocation_type)) {
  if (xnn_shape_multiply_all_dims(&reduce_value->shape) == 1 &&
      xnn_value_is_static(reduce_value->allocation_type)) {
    swap_value_pointers(&reduce_value, &arg_value);
  } else {
    return xnn_status_success;
  }
}
...
XNN_RETURN_IF_ERROR(xnn_define_static_reduce_v2(
                        subgraph,
                        reduce_node_type == xnn_node_type_static_sum
                            ? xnn_reduce_mean
                            : xnn_reduce_mean_squared,
                        num_reduction_axes, reduction_axes, input_value->id,
                        output_id, reduce_node->flags),
                    "Failed to create new `Mean` or `Mean Squared` node.");

```

This is the similar bug class (of [issue 483445078](https://issues.chromium.org/issues/483445078) probably) that was fixed for `minimum` / `maximum` to `clamp`: [optimize\_common\_subgraphs\_min\_max\_to\_clamp](https://source.chromium.org/chromium/chromium/src/+/main:third_party/xnnpack/src/src/subgraph.c;l=2862) now explicitly rejects rewrites when `arg_value->shape.num_dims > input_value->shape.num_dims`, but `scaled_sum_to_mean` still lacks that guard.

Once the binary output ID has been rebound to a unary reduce node, [reshape\_reduce\_operator](https://source.chromium.org/chromium/chromium/src/+/main:third_party/xnnpack/src/src/subgraph/static-reduce.c;l=149) recomputes the output shape solely from the reduction axes and input dimensions, so it drops the higher-rank broadcasted shape that the original binary operator exported:

```
size_t num_skip_axis = 0;
for (size_t input_idx = 0; input_idx < input_num_dims; ++input_idx) {
  bool is_axis = false;
  ...
  if (!is_axis) {
    output_value->shape.dim[input_idx - num_skip_axis] = input_dims[input_idx];
  }
}
output_value->shape.num_dims = input_num_dims - num_skip_axis;
const size_t new_size = xnn_runtime_tensor_get_size(output_value);

```

The spatial consumers then trust that reused value as if it were still NHWC. [reshape\_convolution\_operator](https://source.chromium.org/chromium/chromium/src/+/main:third_party/xnnpack/src/src/subgraph/convolution-2d.c;l=661) reads `dim[0..2]` unconditionally and forces a 4D output shape:

```
  const size_t batch_size = values[input_id].shape.dim[0];
  const size_t input_height = values[input_id].shape.dim[1];
  const size_t input_width = values[input_id].shape.dim[2];

...

  output_value->shape.dim[0] = batch_size;
  output_value->shape.dim[1] = output_height;
  output_value->shape.dim[2] = output_width;
  output_value->shape.dim[3] = output_pixel_stride;

  output_value->shape.num_dims = 4;

```

Finally, the conv/deconv reshape logic interprets that lower-rank value as 4D NHWC and cause the heap-buffer-overflow in `xnn_f32_igemm_minmax_ukernel_10x8__fma3_broadcast`.

### Bisection

This issue is introduced by the commit <https://source.chromium.org/chromium/_/chromium/external/github.com/google/XNNPACK/+/27c1929b344882a6dfb95771ef8ab662f1ad010e>, which introduce the incorrect implementation of `optimize_common_subgraphs_scaled_sum_to_mean` function.

### Reproduction

Run chrome from `https://storage.googleapis.com/chromium-browser-asan/linux-release/asan-linux-release-1598914.zip` with the following command:

```
./chrome --enable-features=ExperimentalWebMachineLearningNeuralNetwork,WebMachineLearningNeuralNetwork --no-sandbox poc.html

```

You would observe the heap-buffer-overflow in `asan.txt`

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 43.2 KB)
- [poc.html](attachments/poc.html) (text/html, 1.6 KB)
- [model0.tflite](attachments/model0.tflite) (application/octet-stream, 1.2 KB)

## Timeline

### cl...@appspot.gserviceaccount.com (2026-03-13)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6246152819212288.

### th...@chromium.org (2026-03-13)

[security shepherd] Adding Security\_Impact-None due to required flags, and kicking off CF.

### th...@chromium.org (2026-03-13)

CF has been a bit slow in the past couple days, so triaging manually. I can repro on linux M146 extended stable. Based on the docs [1](https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/severity-guidelines.md#toc-critical-severity) [2](https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/process-sandboxes-by-platform.md#not-sandboxed-on-some-platforms), this is critical severity since this is a UAF in the gpu process at least on linux which the docs say is not sandboxed, but I'm checking internally. It also might be accessible on Android (e.g. if this is similarly accessible like <https://crbug.com/481776048>).

reillyg@: could you PTAL? Notably: is this accessible by default for any users (e.g. via origin trial, etc)? If so, then we should remove the Security\_Impact-None label.

### re...@chromium.org (2026-03-13)

Setting the milestone to M-147 and removing Android from the impacted OS's because this feature is only available via Origin Trial on desktop platforms past this milestone. It was disabled on M-146.

### ds...@google.com (2026-03-13)

Coincidentally, I happen to have a WIP cl/882268043 to completely remove/replace this rewrite, because it's broken for another reason: if the subgraph gets reshaped such that the size of the reduction changes, the rewrite is not valid any more.

### re...@chromium.org (2026-03-13)

Thanks Dilon. Once your change lands we can roll it into M-147. I've attached the TFLite model generated by WebNN for poc.html.

### ds...@google.com (2026-03-13)

<https://github.com/google/XNNPACK/pull/9671> is the open source version of this fix. I will likely submit it Monday.

### ch...@google.com (2026-03-14)

Setting Priority to P0 to match Severity s0. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### 24...@project.gserviceaccount.com (2026-03-15)

Detailed Report: https://clusterfuzz.com/testcase?key=6246152819212288

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-buffer-overflow READ 4
Crash Address: 0x7b5910662520
Crash State:
  xnn_f32_igemm_minmax_ukernel_10x8__fma3_broadcast
  xnn_compute_igemm
  pthreadpool_parallelize_4d_tile_2d_dynamic
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1537577:1537594

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6246152819212288

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary.

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


A recommended severity was added to this bug. Please change the severity if it is inaccurate.

### 24...@project.gserviceaccount.com (2026-03-15)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the hotlistid:4801165.

### ch...@google.com (2026-03-15)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security Impact hotlist or the Severity field, and remove the ReleaseBlock hotlist.

### ds...@google.com (2026-03-16)

The fix for this is submitted to XNNPACK (<https://github.com/google/XNNPACK/pull/9671>, cl/884165426)

### sr...@chromium.org (2026-03-16)

PTAL at the RBS for 147,  Stable RC cut for 147 is next week so please help get these fixes landed on trunk and verify on canary and request a merge to 147 , We will cut RC build next tuesday march 24
If this is not a blocker for 147 stable, please drop the RBS label on the bug

### re...@chromium.org (2026-03-16)

Verified that this issue is not reproducible under and ASan build with an updated XNNPACK once <https://crrev.com/c/7670309> lands.

### dx...@google.com (2026-03-17)

Project: chromium/src  

Branch:  main  

Author:  Reilly Grant [reillyg@chromium.org](mailto:reillyg@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7670309>

Roll TFLite/LiteRT to Next Green Version

---


Expand for full commit details
```
     
    Version Changes: 
    XNNPACK: 15e04ff8b61e0bc2118bad268447be5b2075aa66 to b1ba7db0d48be76c032061b98d68f094b066e53e 
    tflite: d20369f4f226598800e0d406db567d2d1c17fa95 to da1b60beb415211263748ba44021921876192556 
    litert: 36dcf5a2ac1d6cc02df53d5e3f5bcd6dd6876ff0 to 2d7ebf8846ee010e4766c925c228bdea993f7322 
     
    Bug: 388311883, 492350403 
    Cq-Include-Trybots: luci.chrome.try:optimization_guide-linux;luci.chrome.try:optimization_guide-mac-arm64;luci.chrome.try:optimization_guide-mac-x64;luci.chrome.try:optimization_guide-win32;luci.chrome.try:optimization_guide-win64 
    Include-Ci-Only-Tests: chromium.android:android-pie-arm64-rel|android_browsertests 
    No-Try: true 
    Change-Id: Ib1e942968f032efe072c1c907595799959e314d8 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7670309 
    Commit-Queue: Reilly Grant <reillyg@chromium.org> 
    Reviewed-by: Steven Holte <holte@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1600753}

```

---

Files:

- M `DEPS`
- M `third_party/litert/README.chromium`
- M `third_party/litert/src`
- M `third_party/tflite/README.chromium`
- M `third_party/tflite/src`
- M `third_party/xnnpack/BUILD.gn`
- M `third_party/xnnpack/README.chromium`
- M `third_party/xnnpack/src`

---

Hash: [4c34b3025a538acdc12e767e9bf9e96b1a76cbdc](https://chromiumdash.appspot.com/commit/4c34b3025a538acdc12e767e9bf9e96b1a76cbdc)  

Date: Tue Mar 17 20:06:38 2026


---

### ch...@google.com (2026-03-18)

Security Merge Request Consideration: Requesting merge to beta (M147) because latest trunk commit (1600753) appears to be after beta branch point (1596535).
Security Merge Request - Manual Review: Merge review required: a commit with DEPS changes was detected.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [147].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### 24...@project.gserviceaccount.com (2026-03-18)

ClusterFuzz testcase 6246152819212288 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1600740:1600756

If this is incorrect, please add the hotlistid:5433040 and re-open the issue.

### re...@chromium.org (2026-03-18)

**Which CLs should be backmerged? (Please include Gerrit links.)**

<https://github.com/google/XNNPACK/pull/9671> needs to be cherry-picked onto <https://chromium.googlesource.com/external/github.com/google/XNNPACK/+/refs/heads/chromium/7727>.

**Has this fix been verified on Canary to not pose any stability regressions?** Yes.   

**Does this fix pose any potential non-verifiable stability risks?** No.   

**Does this fix pose any known compatibility risks?** No.   

**Does it require manual verification by the test team?** No.

### dr...@chromium.org (2026-03-20)

No crashes in Canary. Approved to merge to M147.

### dx...@google.com (2026-03-21)

Project: external/github.com/google/XNNPACK  

Branch:  chromium/7727  

Author:  Reilly Grant [reillyg@google.com](mailto:reillyg@google.com)  

Link:    <https://chromium-review.googlesource.com/7689940>

[M147] Allow redundant reduction axes, and out of bounds reduction axes

---


Expand for full commit details
```
     
    TFlite allows the same axis to be specified in a reduction multiple times, and expects it to be treated like set, i.e. these should be deduplicated. Because of the way reshaping works, it can be difficult at delegation or subgraph creation time to determine if this is happening, so we can't just not delegate such ops. 
     
    TFlite also allows specifying reduction of a "scalar" with a reduction axis list of {0} (not {}. This is a super annoying behavior, but we need to handle it, because we can't determine if this is happening at delegation time. I think it is reasonable to simply allow out of bounds reduction axes, and just ignore them. This basically treats that reduction axis as an implied dimension of extent 1, which a lot of other things do already (e.g. binary elementwise ops). 
     
    As a result of this, I realized that the sum => mean rewrite we do currently is not safe from reshaping. The graph might be equivalent to a mean at the time of construction, but become not so after reshaping. (This would almost certainly be a bug in the client code, but it's a bug that we should not silently fix for the client.) 
     
    In addition, I think the sum => mean rewrite probably has negligible impact on performance. I locally modified the layer norm benchmark to use a sum + multiply to implement the two means, and the performance impact is actually an improvement (though very small, and that doesn't really make sense): 
    ``` 
    name                                                                time/op       time/op     vs base 
    FP32LayerNorm/M:128/N:256/K:512/NormMask:1/process_time/real_time   73.64m ± 2%   74.00m ± 1%       ~ (p=0.394 n=6) 
    FP32LayerNorm/M:128/N:256/K:512/NormMask:2/process_time/real_time   69.82m ± 1%   69.31m ± 1%  -0.74% (p=0.041 n=6) 
    FP32LayerNorm/M:128/N:256/K:512/NormMask:3/process_time/real_time   69.82m ± 2%   69.29m ± 1%       ~ (p=0.485 n=6) 
    FP32LayerNorm/M:128/N:256/K:512/NormMask:4/process_time/real_time   62.28m ± 1%   61.31m ± 1%  -1.56% (p=0.009 n=6) 
    FP32LayerNorm/M:128/N:256/K:512/NormMask:5/process_time/real_time   61.80m ± 1%   61.77m ± 1%       ~ (p=0.699 n=6) 
    FP32LayerNorm/M:128/N:256/K:512/NormMask:6/process_time/real_time   60.46m ± 2%   59.42m ± 2%  -1.72% (p=0.041 n=6) 
    FP32LayerNorm/M:128/N:256/K:512/NormMask:7/process_time/real_time   60.01m ± 2%   59.42m ± 3%       ~ (p=0.240 n=6) 
    geomean                                                             65.21m        64.71m       -0.76% 
    ``` 
     
    To fix this issue, I've replaced this rewrite with a `widen_fp16_accumulators` rewrite, that leaves the subgraph mostly intact, but changes the types of the intermediate tensors to fp32, and inserts a convert to fp16 after the division. 
     
    (Cherry-picked from commit de3504fd8cfcedf194cd0ae43afb37cdff824aa2.) 
     
    PiperOrigin-RevId: 884165426 
    Bug: 492350403 
    Change-Id: I74b0d03c6ce57674ca9d16e9f93e7f9f3a37108d

```

---

Files:

- M `src/operators/reduce-nd.c`
- M `src/subgraph.c`
- M `test/operators/reduce-nd.cc`
- M `test/subgraph/static-reduce.cc`

---

Hash: [abd8e60edf09db5f5ba8e7fa2f1fcab0ae0807e1](https://chromiumdash.appspot.com/commit/abd8e60edf09db5f5ba8e7fa2f1fcab0ae0807e1)  

Date: Sat Mar 21 00:26:44 2026


---

### pe...@google.com (2026-03-21)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### re...@chromium.org (2026-03-21)

Adjusted "Found In" because WebNN isn't enabled by default in M-146. It isn't enabled by default in M-144 either so it does not need to be considered for ChromeOS LTS.

### qk...@google.com (2026-03-23)

Labled 'LTS-NotApplicable-138/144' because the feature was not enabled by default in M138 and M144 according to the [comment #23](https://issues.chromium.org/issues/492350403#comment23).

### sp...@google.com (2026-05-21)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $3000.00 for this report.

Rationale for this decision:
Baseline with bisect. User information disclosure


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-06-24)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/492350403)*
