# Disable WebNN Origin Trial for M147

| Field | Value |
|-------|-------|
| **Issue ID** | [494823884](https://issues.chromium.org/issues/494823884) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>WebML |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ph...@chromium.org |
| **Assignee** | ph...@chromium.org |
| **Created** | 2026-03-22 |
| **Bounty** | $43,000.00 |

## Description

# Clamp-merge optimization corrupts maxPool2d padding via union aliasing, causing heap OOB write in GPU process

## Title

XNNPACK clamp-merge optimization overwrites maxPool2d padding fields through params union aliasing, leading to indirection buffer integer overflow and heap out-of-bounds write in the GPU process.

## Summary

A bug in XNNPACK's common-subgraph optimizer allows a web page to crash the GPU process through the WebNN JavaScript API. The `optimize_common_subgraphs_merge_clamps` function folds a unary clamp node into its producer by writing the merged activation bounds to `params.unary.clamp.min` and `params.unary.clamp.max`. When the producer is a max-pooling node, these two float stores silently overwrite `params.pooling_2d.padding_top` and `params.pooling_2d.padding_right` because `params` is a C union. By choosing clamp bounds whose IEEE-754 bit patterns encode large integers, an attacker corrupts the pooling geometry after all WebNN and TFLite validation has completed. The corrupted padding produces enormous output dimensions during reshape, which causes the indirection buffer size computation to overflow `size_t` and wrap to a small value. XNNPACK allocates the undersized buffer and then writes into it using indices derived from the true dimensions, producing an immediate heap buffer overflow. The crash occurs inside `AllocateTensors`, before any post-reshape output-size checks run. The PoC requires no source modifications and uses only standard WebNN API calls. Affected platforms: all platforms where the TFLite WebNN backend is active (Linux, ChromeOS by default; Windows and macOS when TFLite is the fallback).

## Bisect

### XNNPACK upstream — `optimize_common_subgraphs_merge_clamps` unconditionally writes `params.unary.clamp` on all `has_clamp` producer nodes

- Commit: `e9bc43cef4c8663d2831e5c99b6bf799f09168fa`
- Date: 2025-10-29
- Author: Pedro Gonnet ([gonnet@google.com](mailto:gonnet@google.com))
- Subject: Subgraph rewrites for Binary `minimum`, `maximum`, and Unary `clamp` nodes
- PiperOrigin-RevId: 825516864

This commit introduced three subgraph optimization functions: `optimize_common_subgraphs_min_max_to_clamp` (converts binary min/max pairs with a static scalar operand into a unary clamp node), `optimize_common_subgraphs_merge_clamps` (fuses a downstream clamp into its producer), and related no-op clamp removal. The merge function calls `has_clamp()` to decide whether a producer supports clamped activation; `has_clamp()` returns true for `xnn_node_type_max_pooling_2d` because max-pool does have activation output bounds. However, the merge writes the combined clamp range through `params.unary.clamp.{min,max}`, which aliases `params.pooling_2d.{padding_top,padding_right}` in the `xnn_node` params union. No type-aware dispatch exists — the function treats every `has_clamp`-capable producer as if its parameters live in the `unary` union member. The `has_clamp` helper itself was introduced earlier in commit `2e439340e66d` (2024-10-28, Dillon Sharlet, "Replace xnn\_node\_type\_\* for unary and binary elementwise ops"), but it was not used for union-aliased writes until this commit.

### Became web-reachable — XNNPACK rolled into Chromium

- Commit: `b279afdc83772e9182614ac54b4f9a8755616615`
- Date: 2026-01-08
- Author: Steven Holte ([holte@google.com](mailto:holte@google.com))
- Subject: Roll src/third\_party/xnnpack/src/ b666baacb..4574c4d9b (27 commits)
- Review: <https://chromium-review.googlesource.com/c/chromium/src/+/7416369>

This roll brought the merge\_clamps optimization into the Chrome build. The `maxPool2d` and `clamp` operators were already reachable from JavaScript through the WebNN API since commit `6c9e4fea79849343` (2024-03-13, Junwei Fu, "webnn: Support Pool2d in //services/webnn/tflite", <https://chromium-review.googlesource.com/c/chromium/src/+/5359192>). The WebNN TFLite graph builder emulates non-standard clamp ranges as explicit binary MIN/MAX pairs, which XNNPACK's new `optimize_common_subgraphs_min_max_to_clamp` converts back into a unary clamp node, completing the prerequisite chain for the merge to trigger on a max-pool producer.

## Root Cause

The `params` field in `struct xnn_node` is declared as a union:

```
// third_party/xnnpack/src/src/xnnpack/subgraph.h
union {
  struct {
    uint32_t padding_top;      // offset 0
    uint32_t padding_right;    // offset 4
    uint32_t padding_bottom;   // offset 8
    uint32_t padding_left;     // offset 12
    uint32_t pooling_height;   // offset 16
    ...
  } pooling_2d;
  ...
  union xnn_unary_params unary; // clamp.min at offset 0, clamp.max at offset 4
} params;

```

The `optimize_common_subgraphs_merge_clamps` function merges a downstream unary clamp into any producer that `has_clamp` returns true for, which includes `xnn_node_type_max_pooling_2d`:

```
// third_party/xnnpack/src/src/subgraph.c:2962-2969
input_producer_node->params.unary.clamp.min =
    math_min_f32(math_max_f32(input_producer_node->params.unary.clamp.min,
                              node->params.unary.clamp.min),
                 node->params.unary.clamp.max);
input_producer_node->params.unary.clamp.max =
    math_min_f32(math_max_f32(input_producer_node->params.unary.clamp.max,
                              node->params.unary.clamp.min),
                 node->params.unary.clamp.max);

```

When the producer is a pooling node, these stores alias `params.pooling_2d.padding_top` and `params.pooling_2d.padding_right`. The merged float value is the clamp's lower bound, reinterpreted as a 32-bit unsigned integer in the padding field. The PoC uses `Math.fround(1.9999998807907104)` as the clamp minimum, whose IEEE-754 representation is `0x3FFFFFFF`, so both `padding_top` and `padding_right` become 1073741823 after the merge.

This corruption happens inside XNNPACK's optimization pass, which runs after WebNN graph validation and TFLite serialization have already accepted the original, legitimate padding values `[1, 0, 0, 1]`.

With the corrupted padding and an input of shape `[1, 1, 2, 1]`, the reshape function in `reshape_max_pooling2d_nhwc` computes `output_height = 0x3FFFFFFF` and `output_width = 0x40000000`. The indirection buffer size is then derived as follows:

```
// third_party/xnnpack/src/src/operators/max-pooling-nhwc.c:482-488
const size_t step_height = pooling_size + (output_width - 1) * step_width * pooling_height;
const size_t indirection_buffer_size =
    sizeof(void*) * ((pooling_size - 1) + output_height * step_height);

```

With `pooling_size = 4`, `step_width = 1`, `pooling_height = 2`, `output_width = 0x40000000`, and `output_height = 0x3FFFFFFF`, the product `output_height * step_height` evaluates to `0x1FFFFFFFFFFFFFFE`. Adding `pooling_size - 1` yields `0x2000000000000001`, and multiplying by `sizeof(void*) = 8` produces `0x10000000000000008`, a 65-bit value that wraps around in `size_t` to just 8 bytes. XNNPACK allocates this 8-byte buffer and immediately passes it to `xnn_indirection_init_maxpool2d`, which iterates over the true `output_height * output_width` grid and writes pointer-sized entries at computed indices. The second iteration already writes past the single allocated slot, triggering a heap buffer overflow.

The overflow occurs inside the XNNPACK delegate's `Prepare` callback, which runs during `AllocateTensors`. This is before the WebNN TFLite backend's post-allocation output-size check at `graph_impl_tflite.cc`, so that check never executes.

## Reproduce

Tested at commit `3ad31ba232d9a804b4de78d788e391f82b40a906` on Windows with the existing ASAN component build (`out/asan-release`). No source modifications are required.

Serve `poc.html` over HTTP:

```
python -m http.server 8888

```

Launch Chrome:

```
set ASAN_OPTIONS=detect_odr_violation=0
out\asan-release\chrome.exe --no-sandbox ^
  --enable-features=WebMachineLearningNeuralNetwork ^
  --disable-features=WebNNOnnxRuntime ^
  --enable-logging=stderr ^
  --user-data-dir=%TEMP%\poc ^
  http://localhost:8888/poc.html

```

The GPU process crashes during `builder.build()` within a few seconds.

### Linux

Also tested on Linux x64 at the same commit. ASAN build configuration is the same (with `target_cpu = "x64"`).

Place `poc.html` in the source root and launch directly:

```
ASAN_OPTIONS=detect_odr_violation=0 out/asan-release/chrome \
  --no-sandbox \
  --enable-features=WebMachineLearningNeuralNetwork \
  --enable-logging=stderr \
  --user-data-dir=/tmp/poc-$(date +%s) \
  poc.html

```

The GPU process crashes identically:

```
==470034==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x7be9da125820
WRITE of size 8 at 0x7be9da125820 thread T42 (ThreadPoolForeg)
    #0 xnn_indirection_init_maxpool2d third_party/xnnpack/src/src/indirection.c:422:39
    #1 reshape_max_pooling2d_nhwc third_party/xnnpack/src/src/operators/max-pooling-nhwc.c:506:5
    ...
    #9 webnn::tflite::GraphImplTflite::ComputeResources::Create services/webnn/tflite/graph_impl_tflite.cc:221:34

0x7be9da125820 is located 8 bytes after 34359738392-byte region
SUMMARY: AddressSanitizer: heap-buffer-overflow indirection.c:422 in xnn_indirection_init_maxpool2d

```

The complete Linux ASAN log is in `asan-linux.log`.

### Windows

```
=================================================================
==14860==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x12697be41820 at pc 0x7ffdc3b6316a bp 0x00a0c2e0e860 sp 0x00a0c2e0e8a8
WRITE of size 8 at 0x12697be41820 thread T23
    #0 0x7ffdc3b63169 in xnn_indirection_init_maxpool2d D:\chromium\src\third_party\xnnpack\src\src\indirection.c:422:39
    #1 0x7ffdc4b175c3 in reshape_max_pooling2d_nhwc D:\chromium\src\third_party\xnnpack\src\src\operators\max-pooling-nhwc.c:506:5
    #2 0x7ffdc4b182af in xnn_reshape_max_pooling2d_nhwc_f32 D:\chromium\src\third_party\xnnpack\src\src\operators\max-pooling-nhwc.c:635:10
    #3 0x7ffdc4e1acb5 in reshape_max_pooling_operator D:\chromium\src\third_party\xnnpack\src\src\subgraph\max-pooling-2d.c:164:16
    #4 0x7ffdc3b9544d in xnn_reshape_runtime D:\chromium\src\third_party\xnnpack\src\src\runtime.c:877:30
    #5 0x7ffdc4f58fdc in tflite::xnnpack::`anonymous namespace'::SubgraphPrepare D:\chromium\src\third_party\tflite\src\tensorflow\lite\delegates\xnnpack\xnnpack_delegate.cc:7211:9
    #6 0x7ffdc5363325 in tflite::Subgraph::PrepareOpsStartingAt D:\chromium\src\third_party\tflite\src\tensorflow\lite\core\subgraph.cc:1540:44
    #7 0x7ffdc535ef6e in tflite::Subgraph::PrepareOpsAndTensors D:\chromium\src\third_party\tflite\src\tensorflow\lite\core\subgraph.cc:1588:7
    #8 0x7ffdc535d26f in tflite::Subgraph::AllocateTensors D:\chromium\src\third_party\tflite\src\tensorflow\lite\core\subgraph.cc:1035:25
    #9 0x7ffdc3a0b64b in webnn::tflite::GraphImplTflite::ComputeResources::Create D:\chromium\src\services\webnn\tflite\graph_impl_tflite.cc:221:34
    #10 0x7ffdc3a09378 in webnn::tflite::GraphImplTflite::CreateAndBuildOnBackgroundThread D:\chromium\src\services\webnn\tflite\graph_impl_tflite.cc:542:20

0x12697be41820 is located 8 bytes after 34359738392-byte region [0x12617be41800,0x12697be41818)
allocated by thread T23 here:
    #0 0x7ffeb7dbcb86  (clang_rt.asan_dynamic-x86_64.dll)
    #1 0x7ffdc4b1731c in reshape_max_pooling2d_nhwc D:\chromium\src\third_party\xnnpack\src\src\operators\max-pooling-nhwc.c:490:22

SUMMARY: AddressSanitizer: heap-buffer-overflow D:\chromium\src\third_party\xnnpack\src\src\indirection.c:422:39 in xnn_indirection_init_maxpool2d
==14860==ABORTING

```
## Credit

Please use c6eed09fc8b174b0f3eebedcceb1e792 as the credit for this vulnerability. Thank you.

## Attachments

- [asan-linux.log](attachments/asan-linux.log) (text/plain, 65.9 KB)
- [asan-mac.log](attachments/asan-mac.log) (text/plain, 75.6 KB)
- [poc.html](attachments/poc.html) (text/html, 1.6 KB)
- [asan.log](attachments/asan.log) (text/plain, 5.8 KB)

## Timeline

### je...@gmail.com (2026-03-22)

The recent CL [7689396](https://chromium-review.googlesource.com/c/chromium/src/+/7689396) ("webnn: validate intermediate padded tensor") adds a `ValidateIntermediatePaddedDescriptor` check in the WebNN validation layer for conv2d and pool2d, which validates that the intermediate padded tensor size does not exceed `tensor_byte_length_limit`. However, this check cannot prevent the present vulnerability because the two bugs operate at fundamentally different stages:

- CL 7689396 validates the **user-supplied** padding values during graph construction. In this exploit, the user-supplied padding is `[1, 0, 0, 1]`, which is small, legitimate, and passes all validation.
- The corruption occurs **after** validation, inside XNNPACK's `optimize_common_subgraphs_merge_clamps` optimization pass. This pass writes clamp activation bounds through `params.unary.clamp`, which aliases `params.pooling_2d.padding_top` and `params.pooling_2d.padding_right` in the C union, replacing the valid padding with attacker-controlled IEEE-754 bit patterns (`0x3FFFFFFF`). No Chromium-side validation can observe or prevent this internal XNNPACK mutation.

The fix must be applied in XNNPACK itself — either by adding type-aware dispatch to `optimize_common_subgraphs_merge_clamps` so that it writes activation bounds through the correct union member for each node type, or by excluding pooling nodes from the clamp-merge optimization entirely.

### je...@gmail.com (2026-03-22)

If you reproduce it using ClusterFuzz, please set the timeout to around 1 minutes. It may take some time to trigger(Depending on the machine configuration), but I have verified this on multiple latest versions across different systems.

### je...@gmail.com (2026-03-22)

Sorry, The test commit version mentioned in the report is incorrect. I actually reproduced it on version 653306df93309da543af912f87d874c92fec7658, but in any case, it can be reproduced on TOH.

```
commit 653306df93309da543af912f87d874c92fec7658 (HEAD -> main, origin/main, origin/HEAD)
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date:   Sat Mar 21 21:58:27 2026 -0700

    Roll WebView ARM64 Orderfile from xyOu6h2md8x2FcNYZ... to z2cHcXHI1rozEr1n3...
    
    If this roll has caused a breakage, revert this CL and stop the roller
    using the controls here:
    https://autoroll.skia.org/r/orderfile-webview-arm64-chromium
    Please CC woa-engprod@google.com on the revert to ensure that a human
    is aware of the problem.
    
    To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry
    
    To report a problem with the AutoRoller itself, please file a bug:
    https://issues.skia.org/issues/new?component=1389291&template=1850622
    
    Documentation for the AutoRoller is here:
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md
    
    Tbr: woa-engprod@google.com

```

### el...@google.com (2026-03-23)

XNNPACK -> reillyg@

### re...@chromium.org (2026-03-23)

Phillis, please take a look at this issue.

### ds...@google.com (2026-03-23)

I think this is an XNNPACK bug, fix is cl/888277390 (unconfirmed).

### ds...@google.com (2026-03-23)

External PR is here: <https://github.com/google/XNNPACK/pull/9761>

### ph...@chromium.org (2026-03-24)

@ds...@google.com that pull request got closed and nothing is merged?

### ds...@google.com (2026-03-24)

This is a copybara bug. The change was merged, just not in that PR. Here is the commit that was actually merged: <https://github.com/google/XNNPACK/commit/76cd487ce12fd058054128f4120474b39dab2900>

### ph...@chromium.org (2026-03-24)

got it, thanks @ds...@google.com! I've verified that it fixed the issue. I will work on rolling XNNPACK in chromium

### ph...@chromium.org (2026-03-25)

Merged <https://chromium-review.git.corp.google.com/c/chromium/src/+/7698554>

### ch...@google.com (2026-03-25)

Dear owner, thanks for fixing this bug. We've reopened it because:

- Security bugs need the Severity (S0-S3) and the Found In set, which will enable the bots to request merges to the correct branches (as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact ([security@chromium.org](mailto:security@chromium.org)) to arrange to set these labels. Severity guidelines: <https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues> FoundIn guidelines: <https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security>
  After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### el...@google.com (2026-03-25)

Security triage: web-reachable GPU corruption -> Sev-0, but it's not default-enabled so SecImpact-None.

### ph...@chromium.org (2026-03-25)

Verified it's fixed in canary. Request merge to 147

### ch...@google.com (2026-03-25)

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

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

### ph...@chromium.org (2026-03-25)

Why does your merge fit within the merge criteria for these milestones? It is a security issue.

What changes specifically would you like to merge? Please link to Gerrit.  

<https://github.com/google/XNNPACK/commit/76cd487ce12fd058054128f4120474b39dab2900> need to be manually cherry-picked to <https://chromium.googlesource.com/external/github.com/google/XNNPACK/+/refs/heads/chromium/7727>.

Have the changes been released and tested on canary? Yes.

Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels? Yes. It is enabled by default but kill-switchable with the WebMachineLearningNeuralNetwork flag.

If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing. No.

### ph...@chromium.org (2026-03-25)

Working on disabling WebNN for origin trial, so we don't need to merge this to M147 anymore. <https://issues.chromium.org/issues/496250248>

### sp...@google.com (2026-04-02)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $43000.00 for this report.

Rationale for this decision:
High quality. Memory corruption in a highly privileged process (e.g. GPU, network processes) with bisect


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-07-02)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> High quality. Memory corruption in a highly privileged process (e.g. GPU, network processes) with bisect

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/494823884)*
