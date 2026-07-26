# TFLite castInt4ToFloat heap-buffer-overflow (OOB Write) via WebNN dequantizeLinear

| Field | Value |
|-------|-------|
| **Issue ID** | [498063923](https://issues.chromium.org/issues/498063923) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebML |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | to...@gmail.com |
| **Assignee** | re...@chromium.org |
| **Created** | 2026-03-31 |
| **Bounty** | $33,000.00 |

## Description

---

### Report description

TFLite castInt4ToFloat heap-buffer-overflow (OOB Write) via WebNN dequantizeLinear

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

#### Which URL (or repository) have you found the vulnerability in?

third\_party/tflite/src/tensorflow/lite/kernels/cast.cc

---

### The problem

#### Please describe the technical details of the vulnerability

## Environment

Ubuntu, x86\_64. Should reproduce on any platform with the TFLite WebNN backend.

## Base Chromium revision

```
148.0.7759.0 (Developer Build, x86_64)
294ae18d736060977d16f6c5ca24ff2bf7de441d (2026-03-27)

```
## GN args

```
is_asan = true
is_debug = false
symbol_level = 1

```
## Build

```
cd chromium/src
git apply fix.patch
gn gen out/asan_shell
autoninja -C out/asan_shell content_shell

```
### About the patch (fix.patch)

TFLite uses an arena allocator (one large `malloc` for all intermediate tensors). ASAN only detects overflows past `malloc` boundaries, so intra-arena overflows are invisible. The following 11-line patch replaces arena-allocated tensors with individual `malloc`'d buffers in ASAN builds so the overflow is detectable. It is guarded by `#if defined(ADDRESS_SANITIZER)` and has no effect on non-ASAN builds.

Apply to `services/webnn/tflite/graph_impl_tflite.cc`, after the `AllocateTensors()` call around line 227:

```
#if defined(ADDRESS_SANITIZER)
    // Replace arena-allocated tensors with individually malloc'd buffers
    // so ASAN can detect intra-arena overflows. TFLite's arena is a single
    // malloc that hides overflows between adjacent tensors from ASAN.
    for (size_t i = 0; i < self->interpreter_->tensors_size(); ++i) {
      TfLiteTensor* t = self->interpreter_->tensor(i);
      if (t && t->allocation_type == kTfLiteArenaRw && t->bytes > 0) {
        self->interpreter_->SetCustomAllocationForTensor(
            static_cast<int>(i), {malloc(t->bytes), t->bytes},
            kTfLiteCustomAllocationFlagsSkipAlignCheck);
      }
    }
    self->interpreter_->AllocateTensors();
#endif

```
## Running the PoC

```
Xvfb :77 -screen 0 1024x768x24 -ac &
sleep 2
DISPLAY=:77 ASAN_OPTIONS="log_path=/tmp/asan_log:detect_leaks=0:halt_on_error=0" \
  ./out/asan_shell/content_shell --no-sandbox \
  --enable-features=WebMachineLearningNeuralNetwork \
  file:///path/to/poc.html

```

Wait ~15 seconds then check `/tmp/asan_log.<gpu_pid>` for the ASAN report.

## Root cause

The `castInt4ToFloat` function in `third_party/tflite/src/tensorflow/lite/kernels/cast.cc` (line 235-242) unpacks packed int4 values (2 per byte) into float32 output. The scalar loop writes TWO float values per iteration. When `num_elements` is odd, the last iteration writes `out_data[2*i+1]` one element past the output buffer. The compiler may merge the two adjacent float stores into a single 8-byte write, which is why ASAN reports `WRITE of size 8`.

The sister function `castUInt4ToFloat` (line 253) already has the correct fix: `if (2 * i + 1 < num_elements)`.

The PoC reaches this code through the WebNN JavaScript API:

1. `dequantizeLinear(int4_input, float32_scale, int4_zero_point)` where scale and zero\_point are **runtime inputs** (not constants)
2. Because scale/zero\_point are not constants, `SerializeQuantizeParams()` returns `nullopt`
3. The graph builder takes the emulated dequantize path (`graph_builder_tflite.cc:7842`)
4. The emulated path emits a TFLite `CAST(INT4 → FLOAT32)` operation (`graph_builder_tflite.cc:7852`)
5. With 5 elements (odd), `castInt4ToFloat` writes 4 bytes past the output buffer

## Fix

```
--- a/third_party/tflite/src/tensorflow/lite/kernels/cast.cc
+++ b/third_party/tflite/src/tensorflow/lite/kernels/cast.cc
@@ -238,7 +238,9 @@
     int32_t lower = static_cast<int8_t>(byte << 4) >> 4;
     int32_t higher = byte >> 4;
     out_data[2 * i] = (float)lower;
-    out_data[2 * i + 1] = (float)higher;
+    if (2 * i + 1 < num_elements) {
+      out_data[2 * i + 1] = (float)higher;
+    }
   }

```
## Bisection

**Introducing commit (reachable from WebNN):** `95d146ad435dc8f7cae3eeda239490b33740c71b` (2026-03-18)
**Title:** "Roll Media App from 5gYtZXHNpSNtYAiZU... to K-Q-Th-kyEbeRmXgk..."

This commit added `services/webnn/tflite/graph_builder_tflite.cc` with int4 support in `dequantize_linear_input` (`kInt4AndInts8Int32`), making the pre-existing `castInt4ToFloat` bug reachable from the WebNN API.

The underlying bug in `cast.cc` was introduced in upstream TensorFlow commit `3d9ee92b478` (2023-08-29, "reference int4->float32 cast") but was not exploitable from Chromium until the TFLite graph builder gained int4 dequantize support on 2026-03-18.

#### Impact analysis

## Affected platforms

All platforms using the TFLite WebNN backend: Linux, Android (ARM64, x86/x64), ChromeOS.

## Impact

- **Attack vector:** Any website using the WebNN API, no user interaction beyond navigation. WebNN is behind the `WebMachineLearningNeuralNetwork` feature flag (origin trial since Jan 2025).
- **Process:** GPU process. On Android, this is unsandboxed.
- **Primitive:** Heap buffer overflow (WRITE of size 8 per ASAN, attacker-controlled value from input nibble).
- **Consequence:** GPU process memory corruption. The overflow writes into adjacent heap memory with attacker-influenced data (the upper nibble of the last packed int4 byte).

---

### The cause

#### What version of Chrome have you found the security issue in?

148.0.7759.0 dev

#### Is the security issue related to a crash?

Yes, it is related to a crash.

#### Choose the type of vulnerability

Memory Corruption (in a non-sandboxed process)

#### How would you like to be publicly acknowledged for your report?

Tobias Wienand

## Attachments

- [fix.patch](attachments/fix.patch) (text/x-patch, 1.2 KB)
- [asan_output.txt](attachments/asan_output.txt) (text/plain, 45.5 KB)
- [poc.html](attachments/poc.html) (text/html, 1.3 KB)
- [poc.html](attachments/poc_75258962.html) (text/html, 1.3 KB)
- [Dockerfile](attachments/Dockerfile) (application/octet-stream, 3.3 KB)

## Timeline

### ch...@google.com (2026-04-01)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-04-01)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security Impact hotlist or the Severity field, and remove the ReleaseBlock hotlist.

### ch...@google.com (2026-04-01)

Setting Priority to P1 to match Severity s1. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### to...@gmail.com (2026-04-07)

Here is a Dockerfile to facilitate easy reproduction of the issue. Still reproduces on HEAD

### to...@gmail.com (2026-04-07)

`docker build -t bug . && docker run -v && $(pwd):/output bug && cat asan.*`

### re...@chromium.org (2026-04-08)

I don't have permission to edit the hotlists but this should be Security\_Impact-None because the WebNN Origin Trial has been disabled.

### to...@gmail.com (2026-04-08)

If I understand correctly the Chromium team is currently invested in hardening WebNN, not because the feature is "dead". Isn't there some way to have the team look at it?

### re...@chromium.org (2026-04-08)

Adjusting milestones to reflect that my team is working on these issues but they don't impact any current release channels (so the bots monitoring issues leave us alone).

### fl...@google.com (2026-04-09)

Switched it to Security\_Impact-None; thanks!

### re...@chromium.org (2026-04-13)

Filed [issue 502311475](https://issues.chromium.org/issues/502311475) to track integration TFLite with ASan so that errors like this can be caught without the patch required above.

### re...@chromium.org (2026-04-14)

Fix merged in <https://github.com/tensorflow/tensorflow/pull/115849> and will roll into Chromium with the next TFLite update.

### to...@gmail.com (2026-04-14)

Thanks for rapidly addressing the issue. I think this should be S0, since it is a write in an unsandboxed process (Android) reachable with a crafted html file, and similar reports also received S0.

### re...@chromium.org (2026-04-14)

Given the arena means that the next allocation is also most likely a tensor and the limited extent of the out-of-bounds write (4 bytes) I'm not convinced this is so severe but I'll let the security team decide.

### sp...@google.com (2026-04-22)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $33000.00 for this report.

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

### ch...@google.com (2026-07-22)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ch...@google.com (2026-07-23)

This Blink bug has been marked as either a release blocker or a vulnerability bug. Blink bugs affect all OSs supported by Chrome (except iOS), so the OS field has been updated to reflect this. Please update the bug with the correct OS field if it only affects a subset of OSes.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/498063923)*
