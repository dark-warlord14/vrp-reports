# ORT DML EP: heap-buffer-overflow in CreateCpuResource via int4/uint4 constants

| Field | Value |
|-------|-------|
| **Issue ID** | [493566347](https://issues.chromium.org/issues/493566347) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebML |
| **Platforms** | Windows |
| **Reporter** | to...@gmail.com |
| **Assignee** | ra...@microsoft.com |
| **Created** | 2026-03-17 |
| **Bounty** | $10,000.00 |

## Description

**Summary:** ORT DML EP: new-delete-type-mismatch via WebNN quantizeLinear

**Program:** Google VRP

**URL:** <https://source.chromium.org/chromium/chromium/src/+/main:services/webnn/ort/graph_impl_ort.cc>

**Vulnerability type:** Memory Corruption (in a sandboxed process)

### Details

## Issue

ORT's DML execution provider has a new-delete-type-mismatch during graph session creation when the graph contains a `quantizeLinear` operation. An object is allocated as 192 bytes but deleted as 1 byte, corrupting the heap. ASan-instrumented ORT crashes the GPU process; without ASan the heap is silently corrupted.

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
  --enable-features=WebMachineLearningNeuralNetwork,WebNNOnnxRuntime \
  --disable-features=WebNNDirectML \
  --webnn-ort-library-path-for-testing=<path-to-ort> \
  --webnn-ort-allow-software-gpu-dml poc.html

```

Expected: `GPU process exited unexpectedly: exit_code=1`

### Attack scenario

This code should affect the Windows Chrome GPU process, which has elevated privileges, albeit not unsandboxed. The exploitability is on the harder side, since this size mismatch would cause freelist corruption. In this case the size on alloc was 192 and the size on dealloc was 1. I guess the opposite case would have been more severe, since the next alloc of size 192 would return a chunk with memory potentially overlapping with recently freed chunks. Maybe variant analysis will reveal this is possible.

## Attachments

- [asan_output.txt](attachments/asan_output.txt) (text/plain, 13.0 KB)
- [ort_verbose_log.txt](attachments/ort_verbose_log.txt) (text/plain, 28.4 KB)
- [poc.html](attachments/poc.html) (text/html, 1.7 KB)
- [asan_output.txt](attachments/asan_output_74625724.txt) (text/plain, 26.4 KB)
- [build_ort_msvc_asan.py](attachments/build_ort_msvc_asan.py) (text/x-python, 3.3 KB)
- [poc.html](attachments/poc_74623596.html) (text/html, 1.7 KB)
- [output.txt](attachments/output.txt) (text/plain, 5.3 KB)
- [build.bat](attachments/build.bat) (application/x-msdos-program, 1.3 KB)
- [README.md](attachments/README.md) (text/markdown, 2.2 KB)
- [wrl_asan_test.cpp](attachments/wrl_asan_test.cpp) (text/x-c++src, 4.4 KB)

## Timeline

### sp...@google.com (2026-03-17)

*NOTE: This is an automatically generated email*

Hi! Many thanks for sharing your report.

This email confirms we've received your message. We'll investigate the issue you've reported and get back to you once we have an update. In the meantime, you might want to take a look at the [list of frequently asked questions about Google Bug Hunters](https://bughunters.google.com/about/4925519884451840/frequently-asked-questions).

Also, if you have not already done so, create a profile on [the Google Bughunters site](https://bughunters.google.com/) if you'd like us to publicly recognize your contribution:

- [Leaderboard](https://bughunters.google.com/leaderboard) – You'll be added here if we issue a reward for your report.
- [Honorable Mentions](https://bughunters.google.com/leaderboard/honorable-mentions) – You'll be added here if you are not in the Hall of Fame, but we file a security vulnerability bug based on your report.

**Note that we only act on reports concerning vulnerabilities or technical security problems in one of our products. This is not the correct channel if you need to resolve a problem with your account, or want to report non-security bugs or suggest a new product feature.**

Good news! According to Google magic, your report is likely actionable for us, so it has been moved up in our queue by raising the priority. The next step is human expert review, which should happen slightly sooner now.

Cheers,   

Google Security Bot

[Follow us](https://twitter.com/googlevrp) on Twitter!

### ...@google.com (2026-03-17)

This report may qualify for the [Chrome Vulnerability Reward Program](https://bughunters.google.com/about/rules/chrome-friends/chrome-vulnerability-reward-program-rules). We are moving this report to the Chromium issue tracker.

### ts...@google.com (2026-03-18)

I'm not sure how to get Clusterfuzz to reproduce a case requiring the custom library, but the report seems complete and the ASAN trace is symbolized and present. Over to OWNERS.

### ts...@google.com (2026-03-18)

Assigning to tech lead, please re-assign as appropriate.


### ts...@google.com (2026-03-18)

Michael, sorry there are so many of these, routing suggestions appreciated.

### ra...@microsoft.com (2026-03-19)

> ORT built with clang-cl + ASan (-fsanitize=address), DML enabled (onnxruntime\_USE\_DML=ON).

@to...@gmail.com, please share instructions for how you're building ORT with CLang and ASAN on Windows.

### ra...@microsoft.com (2026-03-20)

@to...@gmail.com, so that we're both looking at the same issue, can you please paste the fully symbolized callstack at the time of the failure, *including* onnxruntime.dll symbols?

### ni...@intel.com (2026-03-20)

I cannot reproduce this issue on the latest Chrome Canary: 148.0.7742.1 (Official Build) canary-dcheck (64-bit) (cohort: DCHECK-64). I use the ORT (1.23.26.219) and DML EP of WindowsAppRuntime.1.8 (8000.806.2252.0) which is used by Chrome by default. When run poc.html, there is an error report on the page "Uncaught UnknownError: Failed to execute 'build' on 'MLGraphBuilder': Failed to create session."

### to...@gmail.com (2026-03-20)

I realize there is some complexity surrounding the reproduction of this issue. To save everyone time, I would like to prepare a detailed list of instructions and also a root cause analysis. I will reply soon. This applies to <https://issues.chromium.org/issues/494248550> as well

### to...@gmail.com (2026-03-23)

Here is how to reproduce the new-delete type mismatch. Please note that full symbolization seems to cause the crash to disappear, suggesting some UB as root cause. If you absolutely need it, I can try to give it another shot. Also, I switched to MSVC, since the build process is less complicated compared to clang.

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
change the bug or any code path — it only makes the external memory visible to
ASan's shadow memory.

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
ERROR: AddressSanitizer: new-delete-type-mismatch on 0x...:
  object passed to delete has wrong type:
  size of the allocated type:   192 bytes;
  size of the deallocated type: 1 bytes.

```

See `asan_output.txt` for the full trace.

## Notes

- **`allow_user_poisoning=0`** disables abseil's manual memory poisoning which
  otherwise causes a false-positive `use-after-poison` during ORT startup. This
  does not affect ASan's heap/stack/type-mismatch detection.
- **The current directory must be `<output_dir>`** so the GPU process finds
  `clang_rt.asan_dynamic-x86_64.dll` next to `onnxruntime.dll`.

### ra...@microsoft.com (2026-03-24)

[Fix new-delete mismatch in DML EP's QuantizeLinear operator](https://github.com/microsoft/onnxruntime/pull/27823)

### ad...@microsoft.com (2026-03-26)

Regarding the issue ASan is flagging, a hypothesis for the mismatch is ultimately due to exceptions being thrown from a RuntimeClass's constructor which exposes an issue in WRL during cleanup. In WRL, there's an allocator class which is using `operator new` for its internal allocation but in its destructor calls `delete` on its internal buffer. ASan is picking up on this sizing difference.

I attached the source code for a small program which illustrates the behavior across a few test cases. What I'm trying to understand is whether this is exploitable in practice. From some internal analysis and discussion, the default heap on Windows knows the size of the allocation and so would use that to free the correct size.

Any feedback here welcome.

### to...@gmail.com (2026-04-16)

Hey, following up on the last comment from March 26 and after reading the comment in SafeMakeOrThrow.h, I agree with the assessment that the size mismatch is *probably* benign under the default MSVC allocator, though I am not an expert with its internals. Could the status be updated to Fixed to reflect the [fix merged in ORT](https://github.com/microsoft/onnxruntime/pull/27823)?

### ch...@google.com (2026-04-16)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### re...@chromium.org (2026-04-17)

Setting "NA" since this fix is in a platform library.

### ch...@google.com (2026-04-17)

This is sufficiently serious that it should be merged to M147. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M147. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Security Merge Request:

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

This is sufficiently serious that it should be merged to M148. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M148. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

### ch...@google.com (2026-04-17)

**M147** merge request created. **Please update [crbug/503604809](https://crbug.com/503604809) to have this merge reviewed.**

### ch...@google.com (2026-04-17)

**M148** merge request created. **Please update [crbug/503605092](https://crbug.com/503605092) to have this merge reviewed.**

### sp...@google.com (2026-05-14)

*NOTE: This is an automatically generated email*

Hello,

Chrome Vulnerability Rewards Program (VRP) Panel has decided that the security impact of this
issue does not meet the criteria to qualify for a reward.

Rationale for this decision:

Not demonstrated in Chrome / ASAN only (Comments 13 and 14)

Note that the fact that this issue is not being rewarded does not mean
that the product team won't fix the issue. We have filed a bug with the product
team and they will review your report and decide if a fix is required. We'll
let you know if the issue was fixed.

Regards,   

Google Security Bot

*How did we do? Please fill out a [short anonymous survey](https://goo.gl/IR3KRH).*

### ch...@google.com (2026-07-25)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/493566347)*
