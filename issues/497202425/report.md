# Integer overflow in ruy SumsBytes leads to heap OOB write in the GPU process via WebNN quantized Gemm

| Field | Value |
|-------|-------|
| **Issue ID** | [497202425](https://issues.chromium.org/issues/497202425) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebML |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | je...@gmail.com |
| **Assignee** | ju...@intel.com |
| **Created** | 2026-03-29 |
| **Bounty** | $11,000.00 |

## Description

# Integer overflow in ruy SumsBytes leads to heap OOB write in the GPU process via WebNN quantized Gemm

## Summary

A malicious web page can crash the GPU process by constructing a WebNN graph whose quantized int8 Gemm produces a packed matrix column count large enough to overflow the `int32` multiplication in ruy's `SumsBytes()`. The overflowed negative value poisons ruy's bump allocator, causing subsequent allocations to return pointers far outside the backing buffer. The resulting out-of-bounds write triggers SEGV in the GPU process. Under conditions where the allocator already holds a backing buffer from a prior ruy operation within the same graph, this escalates from a crash to a controlled heap out-of-bounds write. Affected platforms: all x86-64 and ARM platforms running Linux, macOS, Windows, or ChromeOS.

## Bisect

The `SumsBytes` function has used unchecked `int32` arithmetic since ruy was first vendored into Chromium with TFLite:

Introducing Commit (ruy): `a0ed9bde41f042c26c1270e0e981d0327136a535`

- Date: `2020-11-19`
- Author: `Michael Crouse`
- Review: <https://chromium-review.googlesource.com/c/chromium/src/+/2523426>

The bug became web-reachable when WebNN added QDQ fusion for Gemm on the TFLite backend:

Introducing Commit (WebNN reachability): `6e5458b43fdc3685cb17664e6709bd79a97dfb36`

- Date: `2025-06-19`
- Author: `junwei`
- Review: <https://chromium-review.googlesource.com/c/chromium/src/+/6641102>

## Root Cause

WebNN's TFLite graph builder fuses `dequantizeLinear -> gemm -> quantizeLinear` chains into quantized `FULLY_CONNECTED` operators via `CanFuseQuantizeAndGetOutput`. When the filter operand is a dynamic graph input rather than a constant, the XNNPACK delegate rejects the node because `VisitFullyConnectedNode` requires static allocation for non-float32 filters. The interpreter then falls back to the builtin TFLite kernel, which dispatches through `cpu_backend_gemm::Gemm` into ruy.

`SerializeGemm` performs no overflow checks on the GEMM dimensions that flow into ruy's internal packed-buffer calculations. A recent commit (d3f0e9e1304d2) added `CheckedNumeric` validation for Conv2D im2col temporary sizes, but the analogous check for GEMM packed dimensions is entirely absent.

Inside ruy, `CreatePackedLayout` rounds the source matrix dimensions up to multiples of the kernel tile size, storing the results in `int32_t` fields:

```
// third_party/ruy/src/ruy/create_trmul_params.h:42-51
inline void CreatePackedLayout(const MatLayout& src,
                               const KernelLayout& kernel_layout,
                               PMatLayout* packed_layout) {
  packed_layout->order = Order::kColMajor;
  packed_layout->rows = round_up_pot(src.rows, kernel_layout.rows);
  packed_layout->cols = round_up_pot(src.cols, kernel_layout.cols);
  packed_layout->stride = packed_layout->rows;
  packed_layout->kernel = kernel_layout;
}

```

`PMatLayout.rows` and `PMatLayout.cols` are `std::int32_t`. The overflow occurs in `SumsBytes`, which computes the byte count for per-column accumulator sums:

```
// third_party/ruy/src/ruy/mat.h:436-439
inline std::ptrdiff_t SumsBytes(const PEMat& packed) {
  return packed.layout.cols * packed.sums_type.size;
}

```

For a WebNN Gemm with `bTranspose: true` and filter shape `[536870911, 1]`, the TFLite `FULLY_CONNECTED` maps the filter as LHS with `rows = 536870911, cols = 1`. After ruy's frontend transposes the LHS, the packed layout becomes `rows = round_up_pot(1, 4) = 4, cols = round_up_pot(536870911, 8) = 536870912`. The multiplication `536870912 * 4` evaluates to 2147483648 in `int` arithmetic, wrapping to -2147483648.

This negative value propagates into `PreparePackedMatrices`:

```
// third_party/ruy/src/ruy/prepare_packed_matrices.cc:88-92
packed_matrix.data = allocator->AllocateBytesAvoidingAliasingWith(
    DataBytes(packed_matrix), params->src[side].data);
packed_matrix.sums = allocator->AllocateBytes(SumsBytes(packed_matrix));

```

The `DataBytes` allocation (~2 GB, positive) exceeds the backing buffer and falls through to `AllocateSlow`, leaving `current_` at 0. The `SumsBytes` allocation (-2147483648) then enters `AllocateFast`:

```
// third_party/ruy/src/ruy/allocator.cc:29-36
void* Allocator::AllocateFast(std::ptrdiff_t num_bytes) {
  if (current_ + num_bytes > size_) {
    return nullptr;
  }
  void* ret = static_cast<char*>(ptr_) + current_;
  current_ += num_bytes;
  return ret;
}

```

The signed comparison `0 + (-2147483648) > size_` evaluates to false because the left side is negative. The function returns `ptr_` and sets `current_` to -2147483648. Every subsequent positive allocation returns a pointer at `ptr_ + current_`, producing an out-of-bounds write target before the backing buffer. When the ruy allocator already holds a backing buffer from a prior operation in the same graph, this is a heap out-of-bounds write in the GPU process reachable from any web page.

The PoC chains two quantized GEMM nodes in a single WebNN graph: a tiny warm-up node whose output feeds into the malicious node via `dequantizeLinear`. This data dependency guarantees the warm-up executes first, and its `MulFrontEndFromTrMulParams` call ends with `FreeAll()` that consolidates the allocator's fallback blocks into a non-null backing buffer. When the malicious node runs, `ptr_` is non-null, so `AllocateFast` returns a valid-looking but out-of-bounds pointer instead of null.

All input tensors remain below WebNN's `INT_MAX` byte limit: the int8 filter is 536870911 bytes and its float32 intermediate is `536870911 * 4 = 2147483644`, just under the limit. No existing validation blocks the graph construction.

## Reproduce

Tested at commit `5e60c832cb8d7cddd0bc4f84d3c8864c80649afb` on Linux x86-64.

Build configuration (`out/asan-release/args.gn`):

```
is_asan = true
is_debug = false
dcheck_always_on = false
target_cpu = "x64"
is_component_build = true

```
```
autoninja -C out/asan-release chrome

```
```
cd ~/chromium/src
ASAN_OPTIONS=detect_odr_violation=0 xvfb-run -a \
  out/asan-release/chrome --no-sandbox \
  --enable-features=WebMachineLearningNeuralNetwork \
  --user-data-dir=/tmp/poc-$(date +%s) \
  issue_webnn_ruy_sums_overflow/poc.html

```

The GPU process crashes within seconds.

```
Received signal 11 SEGV_ACCERR 7d8808b4e500
#0 0x556504dd48d6 chrome
#1 0x7fb908760782 libbase.so
#2 0x7fb908705f63 libbase.so
#3 0x7fb90875fa1b libbase.so
#4 0x7fb896e42520 libc.so.6
#5 0x7fb88e745e7a libservices_webnn_webnn_service.so  ruy::TrMul (atomic store to OOB pointer)
#6 0x7fb88e7237ed libservices_webnn_webnn_service.so  ruy::MulFrontEndFromTrMulParams [frontend.cc:32]
#7 0x7fb88ee3db5c libservices_webnn_webnn_service.so  ruy::MulFrontEnd<int8> [frontend.h:94]
#8 0x7fb88ef059f8 libservices_webnn_webnn_service.so  GemmImplUsingRuy<int8>::Run
#9 0x7fb88ef054aa libservices_webnn_webnn_service.so  optimized_integer_ops::FullyConnected
#10 0x7fb88eefa8b5 libservices_webnn_webnn_service.so EvalQuantized<kGenericOptimized> [fully_connected.cc]
#11 0x7fb88eee83f2 libservices_webnn_webnn_service.so Eval<kGenericOptimized> [fully_connected.cc]
#12 0x7fb88eb72035 libservices_webnn_webnn_service.so tflite::Subgraph::InvokeImpl
#13 0x7fb88eb710cf libservices_webnn_webnn_service.so tflite::Subgraph::Invoke
#14 0x7fb88eb4f655 libservices_webnn_webnn_service.so tflite::impl::Interpreter::Invoke
#15 0x7fb88e0f44ee libservices_webnn_webnn_service.so webnn::tflite::GraphImplTflite::DoDispatch [graph_impl_tflite.cc:328]

GPU process exited unexpectedly: exit_code=11

```
## Credit

Please use c6eed09fc8b174b0f3eebedcceb1e792 as the credit for this vulnerability. Thank you.

## Attachments

- [poc.html](attachments/poc.html) (text/html, 3.3 KB)
- [asan.log](attachments/asan.log) (text/plain, 3.1 KB)

## Timeline

### xi...@chromium.org (2026-03-30)

Triage the same way as <https://crbug.com/494089502>

### ch...@google.com (2026-03-31)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-03-31)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security Impact hotlist or the Severity field, and remove the ReleaseBlock hotlist.

### ch...@google.com (2026-03-31)

Setting Priority to P1 to match Severity s1. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### dx...@google.com (2026-04-03)

Project: chromium/src  

Branch:  main  

Author:  junwei [junwei.fu@intel.com](mailto:junwei.fu@intel.com)  

Link:    <https://chromium-review.googlesource.com/7713288>

webnn: check ruy overflow for quantized gemm similar to conv2d

---


Expand for full commit details
```
     
    This CL adds a check for quantized gemm to detect potential overflows in 
    ruy's packed matrix computations, matching the existing logic for 
    Conv2d. It also refactors the common rounding logic into a shared 
    `RoundUp` helper function. 
     
    Bug: 497159159, 497202425 
    Change-Id: Id17eb8005f831903f081edbe430297bfb099fcd8 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7713288 
    Reviewed-by: Hu, Ningxin <ningxin.hu@intel.com> 
    Commit-Queue: Fu, Junwei <junwei.fu@intel.com> 
    Reviewed-by: Phillis Tang <phillis@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1609631}

```

---

Files:

- M `services/webnn/tflite/graph_builder_tflite.cc`

---

Hash: [f14935b3075916d884a13df9433babff822eb0de](https://chromiumdash.appspot.com/commit/f14935b3075916d884a13df9433babff822eb0de)  

Date: Fri Apr 3 02:42:57 2026


---

### ch...@google.com (2026-04-08)

Requesting merge to M147 because latest trunk commit (1609631) appears to be after M147 branch point (1596535).

Security Merge Request:

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

### ch...@google.com (2026-04-08)

**M147** merge request created. **Please update [crbug/500599285](https://crbug.com/500599285) to have this merge reviewed.**

### sp...@google.com (2026-04-22)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $11000.00 for this report.

Rationale for this decision:
Baseline with bisect. Memory corruption in a highly privileged process (e.g. GPU, network processes) 


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-07-16)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ch...@google.com (2026-07-17)

This Blink bug has been marked as either a release blocker or a vulnerability bug. Blink bugs affect all OSs supported by Chrome (except iOS), so the OS field has been updated to reflect this. Please update the bug with the correct OS field if it only affects a subset of OSes.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/497202425)*
