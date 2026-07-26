# ORT DML EP: heap-buffer-overflow in CreateCpuResource via int4/uint4 constants

| Field | Value |
|-------|-------|
| **Issue ID** | [494248550](https://issues.chromium.org/issues/494248550) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebML |
| **Platforms** | Windows |
| **Reporter** | to...@gmail.com |
| **Assignee** | ra...@microsoft.com |
| **Created** | 2026-03-19 |
| **Bounty** | $10,000.00 |

## Description

---

### Report description

ORT DML EP: heap-buffer-overflow in CreateCpuResource via int4/uint4 constants

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

#### Which URL (or repository) have you found the vulnerability in?

onnxruntime/core/providers/dml/DmlExecutionProvider/src/DmlGraphFusionHelper.cpp

---

### The problem

#### Please describe the technical details of the vulnerability

## Issue

ORT's DML execution provider has a heap-buffer-overflow (OOB read) when processing int4/uint4 constant tensors during graph compilation. The DML EP aligns tensor byte sizes up to a multiple of 4, but then reads the aligned number of bytes from the original unaligned buffer via `memcpy`, reading past the heap allocation.

A web page can trigger this through the WebNN API by building a graph with a `dequantizeLinear` operation using an int4 constant input. Without ASan, the OOB bytes are silently copied into a GPU buffer.

## Root Cause

In `DmlGraphFusionHelper.cpp`, `ProcessInputData` calls `UnpackInitializer` to get a pointer and size for each constant tensor. At line 236:

```
tensorByteSize = AlignToPow2<size_t>(tensorByteSize, 4);

```

This rounds the size up to a 4-byte boundary (DML requirement). But at line 87, `CreateCpuResource` uses the aligned size to copy from the original buffer:

```
memcpy(bufferData, tensorPtr, tensorByteSize);

```

For int4/uint4 tensors, the packed byte length is `ceil(num_elements / 2)`, which is often not a multiple of 4. For example:

- 1 int4 element = 1 byte, aligned to 4 -> reads 3 bytes past allocation
- 3 int4 elements = 2 bytes, aligned to 4 -> reads 2 bytes past allocation
- 5 int4 elements = 3 bytes, aligned to 4 -> reads 1 byte past allocation

Confirmed with instrumentation:

```
[DML_DEBUG] AlignToPow2: 2197 -> 2200 (delta=3) name=_3
READ of size 2200 at 0x12416b250d15
SUMMARY: AddressSanitizer: heap-buffer-overflow DmlGraphFusionHelper.cpp:87 in CreateCpuResource

```
## Version

Chromium 136.0.7095.0 (`7bb7235f6c1c9`)
ORT 1.23.2, DML Execution Provider

## Build

```
gn args out/asan:
  is_asan = true
  is_debug = false

autoninja -C out/asan content_shell

```

ORT built with clang-cl + ASan (`-fsanitize=address`), DML enabled (`onnxruntime_USE_DML=ON`).

## Run

```
content_shell --no-sandbox \
  --enable-features=WebNNOnnxRuntime \
  --enable-blink-features=MachineLearningNeuralNetwork \
  --webnn-ort-library-path-for-testing=<path-to-ort-asan> \
  --allow-third-party-modules \
  --disable-gpu-sandbox \
  --in-process-gpu \
  poc.html

```

Expected: `GPU process exited unexpectedly: exit_code=1`

#### Impact analysis

- **Information disclosure**: Without ASan, silently reads 1-3 bytes of adjacent heap data into a GPU buffer, potentially leaking sensitive data from the GPU process heap
- **Affected configurations**: All Windows systems using ORT backend with DML EP (default for GPU device type on Windows with NVIDIA/AMD GPUs)

Affects the GPU process on Windows, which is less sandboxed than the renderer

---

### The cause

#### What version of Chrome have you found the security issue in?

136.0.7095.0 dev

#### Is the security issue related to a crash?

Yes, it is related to a crash.

#### Choose the type of vulnerability

Memory Corruption (in a sandboxed process)

#### How would you like to be publicly acknowledged for your report?

Tobias Wienand

## Attachments

- [asan_output.txt](attachments/asan_output.txt) (text/plain, 24.4 KB)
- [poc.html](attachments/poc.html) (text/html, 909 B)
- [asan_output.txt](attachments/asan_output_74628214.txt) (text/plain, 16.3 KB)
- [build_ort_msvc_asan.py](attachments/build_ort_msvc_asan.py) (text/x-python, 3.2 KB)
- [poc.html](attachments/poc_74623597.html) (text/html, 1.2 KB)

## Timeline

### cl...@appspot.gserviceaccount.com (2026-03-20)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5345826406694912.

### to...@gmail.com (2026-03-20)

As already mentioned in <https://issues.chromium.org/issues/493566347>, please give me a little time to understand why it doesn't reproduce. I will respond soon

### to...@gmail.com (2026-03-23)

Please kindly let me know whether these instructions work for you. I tested both empirically on two different GPUs and followed everything from scratch, arriving at the OOB trigger. Also the `poc.html` changed because I switched from clang to MSVC, making the build process less hacky.

## Environment

- Windows 11 Pro with a DirectML-capable GPU (tested on NVIDIA RTX 3060 and Intel Arc)
- Visual Studio 2022 Community (MSVC 14.44, Windows SDK 10.0.26100.0)
- Chromium 148.0.7734.0 (`d18477df02`)
- ONNX Runtime v1.23.2 (`a83fc4d58c`)

## Step 1: Build content\_shell

```
cd <chromium_src>
gn gen out/Default
autoninja -C out/Default content_shell

```
## Step 2: Build ORT v1.23.2 with MSVC ASan

Edit the paths at the top of `build_ort_msvc_asan.py` (`CHROMIUM_SRC`, `VCVARS`, `OUTPUT`) for your environment, then run:

```
python build_ort_msvc_asan.py

```

Clones ORT v1.23.2, applies one source patch (see below), and builds
`onnxruntime.dll` with `/fsanitize=address`.

Output: `<output_dir>/onnxruntime.dll` + `<output_dir>/clang_rt.asan_dynamic-x86_64.dll`

### Source patch

In `DmlGraphFusionHelper.cpp`, ORT receives tensor data as raw memory pointers
from Chromium. ASan cannot track these external pointers. The patch copies the
data to an ASan-tracked heap buffer so ASan can monitor accesses. This does not
change the bug — `AlignToPow2` still rounds up the size and the subsequent
`memcpy` still reads past the buffer boundary. The patch only makes the external
memory visible to ASan's shadow memory.

## Step 3: Run

```
cd <output_dir>
set ASAN_OPTIONS=allow_user_poisoning=0:log_path=asan_trace

<chromium_src>\out\Default\content_shell.exe --no-sandbox --run-web-tests --enable-features=WebMachineLearningNeuralNetwork,WebNNOnnxRuntime --webnn-ort-library-path-for-testing=<output_dir> file:///<path_to_poc>/poc.html

```
## Expected result

```
GPU process exited unexpectedly: exit_code=1
#CRASHED - gpu

```

ASan trace in `asan_trace.<pid>`:

```
ERROR: AddressSanitizer: heap-buffer-overflow on address 0x...:
READ of size 136 at 0x... thread T-1

```

The 135-byte int8 tensor is rounded to 136 by `AlignToPow2`, causing a 1-byte
overread. See `asan_output.txt` for the full trace.

## Notes

- **The bug is silent without ASan.** The overread silently copies 1-3 bytes of
  adjacent heap data into a GPU buffer. No crash occurs with the shipping ORT.
- **`allow_user_poisoning=0`** disables abseil's manual memory poisoning which
  otherwise causes a false-positive `use-after-poison` during ORT startup. This
  does not affect ASan's heap-buffer-overflow detection.
- **The current directory must be `<output_dir>`** so the GPU process finds
  `clang_rt.asan_dynamic-x86_64.dll` next to `onnxruntime.dll`.
- **The PoC uses int8[135] (dequantizeLinear)** because 135 bytes is not a
  multiple of 4, triggering `AlignToPow2(135, 4) = 136`. Any tensor type with
  non-4-aligned byte size triggers the same bug.

### ra...@microsoft.com (2026-03-24)

[Fix overflow in DmlGraphFusionHelper::ProcessInputData](https://github.com/microsoft/onnxruntime/pull/27815)

### el...@google.com (2026-03-24)

Was this really present as far back as 136? When did we aded this API?

### re...@chromium.org (2026-03-24)

We have been prototyping this API for a long time but it is only enabled by default in M147 as part of an Origin Trail.

### to...@gmail.com (2026-03-24)

The version 136 in my original report is a mistake, I believe. Must have been caused by my bisect. I tested this in a recent version (148.0.7734.0), not 136

### ch...@google.com (2026-03-25)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security Impact hotlist or the Severity field, and remove the ReleaseBlock hotlist.

### to...@gmail.com (2026-04-16)

Could the status be updated to `Fixed` to reflect the [fix merged in ORT](https://github.com/microsoft/onnxruntime/pull/27815)? Thanks

### ch...@google.com (2026-04-17)

This is sufficiently serious that it should be merged to M147. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M147. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Security Merge Request:

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

This is sufficiently serious that it should be merged to M148. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M148. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

### ch...@google.com (2026-04-17)

**M147** merge request created. **Please update [crbug/503604834](https://crbug.com/503604834) to have this merge reviewed.**

### ch...@google.com (2026-04-17)

**M148** merge request created. **Please update [crbug/503604951](https://crbug.com/503604951) to have this merge reviewed.**

### sp...@google.com (2026-05-14)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $10000.00 for this report.

Rationale for this decision:
High Quality - User information disclosure


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-07-25)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/494248550)*
