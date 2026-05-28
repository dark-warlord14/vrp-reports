# WebNN ScatterND integer overflow in TFLite bounds check allows for 512MB controlled heap OOB write

| Field | Value |
|-------|-------|
| **Issue ID** | [481776048](https://issues.chromium.org/issues/481776048) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebML |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **CVE IDs** | CVE-2022-35939 |
| **Reporter** | ci...@gmail.com |
| **Assignee** | ju...@intel.com |
| **Created** | 2026-02-04 |
| **Bounty** | $43,000.00 |

## Description

---

### Report description

WebNN ScatterND integer overflow in TFLite bounds check allows for 512MB controlled heap OOB write

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

#### Which URL (or repository) have you found the vulnerability in?

<https://chromium.googlesource.com/chromium/src/+/main/services/webnn/tflite/graph_builder_tflite.cc>

---

### The problem

#### Please describe the technical details of the vulnerability

## Vulnerability Details

`SerializeScatterND` (`graph_builder_tflite.cc:7879`) passes runtime indices directly to TFLite with no bounds validation. The other scatter/gather ops either clamp (Gather, GatherND via `SerializeGatherIndices`) or reject runtime indices entirely (GatherElements, ScatterElements — constant-only).

TFLite's bounds check in `reference_ops::ScatterNd` (`third_party/tflite/src/tensorflow/lite/kernels/internal/reference/reference_ops.h`) has an int32 overflow:

```
if (to_pos < 0 || to_pos + slice_size > output_flat_size) {
    return kTfLiteError;
}

```

With `shape=[3, 536870912]` int8 and index `3`:

- `to_pos` = 1,610,612,736
- `to_pos + slice_size` = 2,147,483,648 → wraps to -2,147,483,648
- -2,147,483,648 > 1,610,612,736 → false → bypassed

Result: 536,870,912 bytes of attacker-controlled data written past the buffer end. The attacker controls the write content via the `updates` tensor.

The write occurs in the GPU process.

**Bisect:** Introduced in [`b4d4b4cb019bd7240a52daa4ba61e3cc814f0384`](https://github.com/tensorflow/tensorflow/commit/b4d4b4cb019bd7240a52daa4ba61e3cc814f0384) (fix for CVE-2022-35939, TF 2.10.0).

**Suggested fix:**

```
if (to_pos < 0 || static_cast<int64_t>(to_pos) + slice_size > output_flat_size) {

```
## Version

**Chrome:** 144.0.7559.110 (Stable), 146.0.7655.0 (Dev)

**OS:** macOS 15.7.2, Windows 11. Cross-platform.

**Flags:** `--enable-features=WebMachineLearningNeuralNetwork --in-process-gpu`
WebNN is behind a flag (W3C spec implementation in progress). `--in-process-gpu` is for crash visibility only, the bug triggers without it.

## Reproduction

1. Kill all Chrome instances, relaunch with flags above
2. Open `scatternd_heap_oob.html`, click "Trigger OOB Write"
3. Chrome crashes — `EXC_BREAKPOINT / SIGTRAP` (PartitionAlloc heap corruption)

Standalone proof (no browser):

```
clang++ -O2 -fno-strict-overflow -fsanitize=address -g -o bug370_asan bug370_asan_proof.cc
./bug370_asan

```

Symbolized stack trace (thread 0, main thread):

```
  #0  __pthread_kill + 10
  #1  pthread_kill + 259
  #2  abort + 126
  #3  __sanitizer::Abort() + 88
  #4  __sanitizer::Die() + 97
  #5  __asan::ScopedInErrorReport::~ScopedInErrorReport() + 1300
  #6  __asan::ReportGenericError() + 1782
  #7  __asan_report_load1 + 54
  #8  ScatterNd_vulnerable() at bug370_asan_proof.cc:98    ← OOB access detected here
  #9  test_overflow_exploit() at bug370_asan_proof.cc:191  [inline]
  #10 main() at bug370_asan_proof.cc:262
  #11 start + 3056

```

**Attachments:**

- `scatternd_heap_oob.html` — Browser PoC (59 lines)
- `bug370_asan_proof.cc` — Standalone proof, ASan `heap-buffer-overflow`
- `crash_chrome_stable.ips` — Stable 144 crash
- `crash_report_chrome_dev.ips` — Dev 146 crash
- `crash_asan_standalone.ips` — ASan crash with symbolication

## Crash Details

**Type:** GPU process

**Stable 144.0.7559.110** (2/2):

```
Exception Type:  EXC_BREAKPOINT (SIGTRAP)
Termination Reason: Trace/BPT trap: 5
Faulting Thread: ThreadPoolSingleThreadSharedForegroundBlocking4

```

**Dev 146.0.7655.0** (5/5):

```
Exception Type:  EXC_BREAKPOINT (SIGTRAP)
Termination Reason: Trace/BPT trap: 5
Faulting Thread: ThreadPoolForegroundWorker

```

Both are `PA_IMMEDIATE_CRASH()` from PartitionAlloc detecting heap metadata corruption.

**lldb on ASan Chromium** , the PoC fills the `updates` tensor with `0x42`. Breakpoint on `EvalScatterNd<int>`, int8 output tensor at `0x29E183840`, size `0x60000000`. After return, `0x42` appears at every OOB position:

```
(lldb) memory read -c 64 0x2FE183840
0x2fe183840: 42 42 42 42 42 42 42 42 42 42 42 42 42 42 42 42  BBBBBBBBBBBBBBBB
0x2fe183850: 42 42 42 42 42 42 42 42 42 42 42 42 42 42 42 42  BBBBBBBBBBBBBBBB
0x2fe183860: 42 42 42 42 42 42 42 42 42 42 42 42 42 42 42 42  BBBBBBBBBBBBBBBB
0x2fe183870: 42 42 42 42 42 42 42 42 42 42 42 42 42 42 42 42  BBBBBBBBBBBBBBBB

(lldb) memory read -c 16 0x30E183840    # +256MB
0x30e183840: 42 42 42 42 42 42 42 42 42 42 42 42 42 42 42 42  BBBBBBBBBBBBBBBB

(lldb) memory read -c 16 0x31E183840    # +512MB (first byte past the write)
0x31e183840: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................

```

512MB of attacker-controlled `0x42` past the buffer boundary, stopping exactly at `slice_size`.

Note: ASan Chromium doesn't flag the OOB because TFLite's `SimpleMemoryArena` allocates a single contiguous buffer for all tensors (~6.4GB), and the OOB write stays within it. The standalone proof uses `new[]` with normal red zones, so ASan triggers immediately.

#### Impact analysis

Any website can trigger a 512MB attacker-controlled heap write in Chrome's GPU process if the user has enabled the WebNN feature flag. The attacker controls the write content (via the updates tensor) and the
write offset (via the indices tensor). No user interaction is required beyond navigating to the page. The GPU process runs with a weaker sandbox than the renderer and has IPC channels to the browser process,
making this a potential stepping stone for sandbox escape.

---

### The cause

#### What version of Chrome have you found the security issue in?

Stable, Dev

#### Is the security issue related to a crash?

Yes, it is related to a crash.

#### Choose the type of vulnerability

Memory Corruption (in a non-sandboxed process)

#### How would you like to be publicly acknowledged for your report?

cinzinga

## Attachments

- [scatternd_heap_oob.html](attachments/scatternd_heap_oob.html) (text/html, 2.3 KB)
- [bug370_asan_proof.cc](attachments/bug370_asan_proof.cc) (application/octet-stream, 9.6 KB)
- [crash_chrome_stable.ips](attachments/crash_chrome_stable.ips) (application/octet-stream, 86.5 KB)
- [crash_asan_standalone.ips](attachments/crash_asan_standalone.ips) (application/octet-stream, 6.7 KB)
- [crash_report_chrome_dev.ips](attachments/crash_report_chrome_dev.ips) (application/octet-stream, 92.1 KB)
- [scatternd_heap_oob.html](attachments/scatternd_heap_oob.html) (text/html, 2.3 KB)
- [scatternd_small_tensor_oob.html](attachments/scatternd_small_tensor_oob.html) (text/html, 3.0 KB)
- [symbolized_crash.txt](attachments/symbolized_crash.txt) (text/plain, 2.9 KB)

## Timeline

### ja...@chromium.org (2026-02-05)

[security triage] Thanks for the report. I've tried the proof of concept and was able to crash the GPU process. My version of Chrome didn't output the same error messages though.

I'm going to third\_party/tflite owners to take a look.

### ja...@google.com (2026-02-05)

I'm changing component to Blink > WebML based on [issue 477562219](https://issues.chromium.org/issues/477562219) being in that component as well.

### ja...@chromium.org (2026-02-05)

Adding owners from: <https://source.chromium.org/chromium/chromium/src/+/main:third_party/tflite/OWNERS;drc=568190239aac35ab38773f91a2215320315af436>

### ja...@chromium.org (2026-02-05)

Hi bug reporter, can you please file a bug with the upstream about this issue?

My guess is that would be here: <https://github.com/tensorflow/tensorflow/issues>

### ja...@chromium.org (2026-02-05)

[security triage] Setting severity to High (S1) for being memory corruption in the GPU but on platforms where it is sandboxed.

This is a preliminary severity level and may change as we learn more about the bug.

### ci...@gmail.com (2026-02-05)

> Hi bug reporter, can you please file a bug with the upstream about this issue?

<https://github.com/tensorflow/tensorflow?tab=security-ov-file#reporting-vulnerabilities>

The "Reporting vulnerabilities" section of the README states:

> Please use Google Bug Hunters reporting form to report security vulnerabilities.

Which is how this report was submitted. Please let me know if I need to make a second report anywhere.

Thanks

### pe...@google.com (2026-02-05)

Thank you for providing more feedback. Adding the requester to the CC list.

### ro...@chromium.org (2026-02-05)

sending to reillyg for //services/webnn/tflite/graph_builder_tflite.cc to take a look at the call ste in chromium.

I'm not sure if this is something that should be fixed by the caller (WebNN) or the callee (TFLite)

### re...@chromium.org (2026-02-05)

The issue should be fixed in TFLite but adding clamping to Chromium is good defense-in-depth against this class of bugs in TFLite and its hardware-specific delegates.

### re...@chromium.org (2026-02-05)

Junwei, please add clamping for scatter indices similar to what we have for gather indices and make sure we have test cases for overflow in both scatter and gather indices in the conformance test suite.

### re...@chromium.org (2026-02-05)

A question to investigate: Is clamping enough here or is it possible for a valid index to still trigger overflow due to the use of an `int` for `to_pos`?

I think the answer is "no". The large dimensions in the proof-of-concept make it easy for the index calculation to overflow and allows the arbitrary write to be very large but if the untrusted indices were forced to be within the bounds of the output tensor then it would not be possible to cause `to_pos` to overflow regardless of the output tensor size.

### ch...@google.com (2026-02-05)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### re...@chromium.org (2026-02-05)

Junwei, [comment #12](https://issues.chromium.org/issues/481776048#comment12) is related to your question in <https://chromium-review.googlesource.com/c/chromium/src/+/7546434/comments/26de0ca9_02d33744>. We can't reliably have the bots executing a test which requires allocating tensors of the size used in the proof-of-concept.

Reporter, could you help by providing a PoC using small tensors?

### ci...@gmail.com (2026-02-05)

Due to the nature of this bug, small tensors cannot trigger the original vulnerability. The integer overflow in TFLite's bounds check:

```
if (to_pos < 0 || to_pos + slice_size > output_flat_size)

```

requires `to_pos + slice_size` to overflow `int32_t` and wrap negative, which only happens when `slice_size` is in the `~1.5-2GB range`.

The large-tensor test could be retained as a manual-only regression test with a comment noting it requires multi-gigabyte allocations.

### re...@chromium.org (2026-02-05)

Couldn't you get `to_pos` close enough to `INT_MAX` using large values in `indices` that a smaller `slice_size` would overflow it?

### ci...@gmail.com (2026-02-05)

Good thought, updated PoC attached, and crash confirmed on:

- 146.0.7668.0 (Developer Build) (x86\_64)
- 146.0.7655.0 (Official Build) dev (x86\_64)

### dx...@google.com (2026-02-06)

Project: chromium/src  

Branch:  main  

Author:  Reilly Grant [reillyg@chromium.org](mailto:reillyg@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7546434>

webnn: Support negative indices and clamping for ScatterND in TFLite

---


Expand for full commit details
```
     
    The TFLite SCATTER_ND kernel does not support negative indices and may 
    exhibit undefined behavior if indices are out of bounds. so clamp the 
    values in `indices` to be in range of [-N, N-1] and transform negative 
    indices to positive the same as GatherND. 
     
    Bug: 481776048 
    Change-Id: I8dc11ca07400b30df82ad265efdeef88ebbfbbfe 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7546434 
    Reviewed-by: Robbie McElrath <rmcelrath@chromium.org> 
    Commit-Queue: Hu, Ningxin <ningxin.hu@intel.com> 
    Reviewed-by: Hu, Ningxin <ningxin.hu@intel.com> 
    Commit-Queue: Reilly Grant <reillyg@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1580553}

```

---

Files:

- M `services/webnn/tflite/graph_builder_tflite.cc`
- M `third_party/blink/web_tests/external/wpt/webnn/conformance_tests/scatterND.https.any.js`

---

Hash: [233323a72bc99df5c860c6da5711e1fb348686ac](https://chromiumdash.appspot.com/commit/233323a72bc99df5c860c6da5711e1fb348686ac)  

Date: Fri Feb 6 02:12:58 2026


---

### ch...@google.com (2026-02-06)

Setting milestone because of s0/s1 severity.

### re...@chromium.org (2026-02-06)

Changed milestone from 144 to 146 because this code has been disabled-by-default until M-146.

### aj...@google.com (2026-02-06)

Is this also reachable on Android?

### re...@chromium.org (2026-02-06)

Yes.

### aj...@google.com (2026-02-06)

Sadly makes this a critical as Android GPU is not well sandboxed.

### re...@chromium.org (2026-02-07)

Apologies for the churn. The change in [comment #18](https://issues.chromium.org/issues/481776048#comment18) resolves this issue and has landed in time for the M-146 branch cut so I believe this issue has been resolved.

### ch...@google.com (2026-02-07)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### ch...@google.com (2026-02-11)

Security Merge Request Consideration: Not requesting merge to dev (M146) because latest trunk commit (1580553) appears to be prior to dev branch point (1582197). If this is incorrect please remove NA-146 from the 'Merge' field and add 146 to the 'Merge-Request' field If other changes are required to fix this bug completely please request a merge if necessary.
Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### aj...@google.com (2026-02-13)

Severity -> High as Android OT is being disabled.

### ci...@gmail.com (2026-03-04)

Attaching a fully symbolized crash trace from a Chrome ASan source build (symbolized\_crash.txt). The symbolized stack confirms the full Chrome → WebNN → TFLite → ScatterNd call chain. I understand the fix has already landed — thank you for the quick turnaround on that, and apologies for the delay on this.

### sp...@google.com (2026-03-05)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $43000.00 for this report.

Rationale for this decision:
High Quality with Bisect. Memory corruption in a highly privileged process (e.g. GPU, network processes) 


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-05-17)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/481776048)*
