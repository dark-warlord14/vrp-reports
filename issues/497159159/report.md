# Integer overflow in ruy pack kernel offset leads to heap OOB write in the GPU process via WebNN quantized Gemm

| Field | Value |
|-------|-------|
| **Issue ID** | [497159159](https://issues.chromium.org/issues/497159159) |
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

# Integer overflow in ruy pack kernel offset leads to heap OOB write in the GPU process via WebNN quantized Gemm

## Summary

A malicious web page can crash the GPU process by constructing a WebNN graph whose quantized int8 Gemm has a contraction dimension large enough to overflow the `int` offset arithmetic in ruy's AVX2 8-bit column-major packing kernel. The trailing-row `memcpy` computes its destination as `packed_ptr + Layout::kCols * non_trailing_rows`, where the multiplication wraps to a large negative value, and the `memcpy` writes approximately 2 GB before the correctly allocated packed buffer. Affected platforms: Linux, macOS, Windows, and ChromeOS on x86-64 with AVX2.

## Bisect

The trailing-row `memcpy` offset has used unchecked `int` arithmetic since the AVX2 pack kernel was first vendored into Chromium with TFLite and ruy:

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

WebNN's TFLite graph builder fuses `dequantizeLinear -> gemm -> quantizeLinear` chains into quantized `FULLY_CONNECTED` operators. When the filter operand is a dynamic graph input, the XNNPACK delegate rejects it via `CheckTensorStaticAllocation` and the interpreter falls back to the builtin TFLite kernel, which dispatches into ruy. `SerializeGemm` performs no overflow checks on the dimensions that flow into ruy's packing arithmetic.

For a WebNN Gemm with `bTranspose: true`, `A = int8[1, K]`, `B = int8[1, K]`, and K = 268435457, the TFLite `FULLY_CONNECTED` maps the filter as LHS with `rows = 1, cols = K`. After ruy's frontend transposes the LHS, the source matrix becomes `rows = K, cols = 1`. `CreatePackedLayout` rounds these to the AVX2 int8 kernel tile:

```
// third_party/ruy/src/ruy/create_trmul_params.h:42-51
packed_layout->rows = round_up_pot(src.rows, kernel_layout.rows);  // round_up_pot(268435457, 4) = 268435460
packed_layout->cols = round_up_pot(src.cols, kernel_layout.cols);  // round_up_pot(1, 8) = 8

```

The packed buffer is allocated correctly at approximately `268435460 * 8 = 2147483680` bytes. The overflow occurs later, inside the AVX2 packing kernel, when it handles trailing rows that do not fill a complete 32-row chunk:

```
// third_party/ruy/src/ruy/pack_avx2_fma.cc:571-581
constexpr int kChunkedRowMask = kNumRowChunks * Layout::kRows - 1;  // 31
const bool trailing_data = (src_rows & kChunkedRowMask) > 0;
if (trailing_data) {
  const int non_trailing_rows = src_rows & ~kChunkedRowMask;
  const int dst_rows = (src_rows + 3) & ~3;
  const int trailing_rows = dst_rows - non_trailing_rows;
  memcpy(packed_ptr + Layout::kCols * non_trailing_rows, trailing_buf,
         Layout::kCols * trailing_rows * sizeof(std::int8_t));
}

```

With `src_rows = 268435457`, `non_trailing_rows` is `268435457 & ~31 = 268435456`. The expression `Layout::kCols * non_trailing_rows` computes `8 * 268435456 = 2147483648` in `int` arithmetic, which wraps to -2147483648. The `memcpy` destination becomes `packed_ptr + (-2147483648)`, an out-of-bounds write target before the packed buffer, crashing the GPU process.

The same overflow pattern exists in the AVX and AVX-512 variants (`pack_avx.cc` and `pack_avx512.cc`) which share the identical trailing-row copy structure.

All input tensors remain below WebNN's `INT_MAX` byte limit: each int8 input is 268435457 bytes, and the float32 intermediate is `268435457 * 4 = 1073741828`, well within the limit. No existing validation blocks the graph construction.

## Reproduce

Tested at commit `5e60c832cb8d7cddd0bc4f84d3c8864c80649afb` on Linux x86-64 with AVX2.

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
  issue_webnn_ruy_pack_offset_overflow/poc.html

```

The GPU process crashes within seconds.

```
Received signal 11 SEGV_ACCERR 7b6fb52dfa00
#0 0x5562f83e98d6 chrome
#1 0x7f75d3f60782 libbase.so
#2 0x7f75d3f05f63 libbase.so
#3 0x7f75d3f5fa1b libbase.so
#4 0x7f7562442520 libc.so.6
#5 0x7f75624c4893 libc.so.6                           memcpy to overflowed destination
#6 0x5562f843fc6c chrome
#7 0x7f7559d40716 libservices_webnn_webnn_service.so  ruy::Pack8bitColMajorForAvx2 [pack_avx2_fma.cc:580]
#8 0x7f755a428991 libservices_webnn_webnn_service.so  ruy::RunPack<kAvx2Fma, FixedKernelLayout<kColMajor,4,8>> [pack_x86.h:99]
#9 0x7f7559d46c7d libservices_webnn_webnn_service.so  ruy::TrMulTask::Run
#10 0x7f7559d45d32 libservices_webnn_webnn_service.so ruy::TrMul
#11 0x7f7559d237ed libservices_webnn_webnn_service.so ruy::MulFrontEndFromTrMulParams [frontend.cc:32]
#12 0x7f755a43db5c libservices_webnn_webnn_service.so ruy::MulFrontEnd<int8> [frontend.h:94]
#13 0x7f755a5059f8 libservices_webnn_webnn_service.so GemmImplUsingRuy<int8>::Run
#14 0x7f755a5054aa libservices_webnn_webnn_service.so optimized_integer_ops::FullyConnected
#15 0x7f755a4fa8b5 libservices_webnn_webnn_service.so EvalQuantized<kGenericOptimized> [fully_connected.cc]
#16 0x7f755a4e83f2 libservices_webnn_webnn_service.so Eval<kGenericOptimized> [fully_connected.cc]
#17 0x7f755a172035 libservices_webnn_webnn_service.so tflite::Subgraph::InvokeImpl
#18 0x7f755a1710cf libservices_webnn_webnn_service.so tflite::Subgraph::Invoke
#19 0x7f755a14f655 libservices_webnn_webnn_service.so tflite::impl::Interpreter::Invoke
#20 0x7f75596f44ee libservices_webnn_webnn_service.so webnn::tflite::GraphImplTflite::DoDispatch [graph_impl_tflite.cc:328]

GPU process exited unexpectedly: exit_code=11

```
## Credit

Please use c6eed09fc8b174b0f3eebedcceb1e792 as the credit for this vulnerability. Thank you.

## Attachments

- [poc.html](attachments/poc.html) (text/html, 2.6 KB)
- [asan.log](attachments/asan.log) (text/plain, 3.9 KB)

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

**M147** merge request created. **Please update [crbug/500599662](https://crbug.com/500599662) to have this merge reviewed.**

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
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/497159159)*
