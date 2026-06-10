# Heap Buffer Overflow (READ) in TFLite + XNNPack via WebNN

| Field | Value |
|-------|-------|
| **Issue ID** | [483971526](https://issues.chromium.org/issues/483971526) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebML |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | to...@gmail.com |
| **Assignee** | re...@chromium.org |
| **Created** | 2026-02-12 |
| **Bounty** | $43,000.00 |

## Description

---

### Report description

Heap Buffer Overflow (READ) in TFLite + XNNPack via WebNN

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

#### Which URL (or repository) have you found the vulnerability in?

<https://source.chromium.org/chromium/chromium/src/+/main:third_party/xnnpack/src/src/xx-copy/xx-copy-scalar-memcpy.c;l=18;drc=1bbe3261c7cd6ca9d140b5cea7aed9df2982418a>

---

### The problem

#### Please describe the technical details of the vulnerability

# XNNPACK heap-buffer-overflow (OOB Read) via WebNN concat + avgPool2d ceil rounding

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
symbol_level = 1

```
## Build

```
cd chromium/src
gn gen out/asan_shell
autoninja -C out/asan_shell content_shell

```
## Running the PoC

WebNN is behind a feature flag. The GPU process is a separate process, so its ASAN errors don't appear on the main process stderr. Setting `ASAN_OPTIONS` with `log_path` captures per-process ASAN output to disk.

```
ASAN_OPTIONS="log_path=/tmp/asan_log:detect_leaks=0" ./out/asan_shell/content_shell --enable-features=WebMachineLearningNeuralNetwork file:///path/to/poc.html

```

The GPU process crashes during graph dispatch (inference). ASAN output is at `/tmp/asan_log.<gpu_pid>`. The poc.html file is included in this report.

## ASAN output

```
==3511981==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x7cf3f8f74708 at pc 0x60c72c4ed02b bp 0x7be37d4f98a0 sp 0x7be37d4f9060
READ of size 12 at 0x7cf3f8f74708 thread T71 (ThreadPoolForeg)
    #0 __asan_memcpy
    #1 xnn_xx_copy_ukernel__scalar_memcpy  third_party/xnnpack/src/src/xx-copy/xx-copy-scalar-memcpy.c:18:3
    #2 xnn_compute_univector_strided       third_party/xnnpack/src/src/operator-run.c:1733:5
    #3 xnn_run_operator_with_index         third_party/xnnpack/src/src/operator-run.c:2482:9
    #4 xnn_invoke_runtime                  third_party/xnnpack/src/src/runtime.c:1207:38
    #5 SubgraphInvoke                      third_party/tflite/src/tensorflow/lite/delegates/xnnpack/xnnpack_delegate.cc:1421:25
    #6 tflite::Subgraph::Invoke()          third_party/tflite/src/tensorflow/lite/core/subgraph.cc:1653:17
    #7 DoDispatch                          services/webnn/tflite/graph_impl_tflite.cc:306:41

0x7cf3f8f74708 is located 0 bytes after 200-byte region [0x7cf3f8f74640,0x7cf3f8f74708)
allocated by thread T71 here:
    #0 operator new(unsigned long)
    #1 SubgraphInit  third_party/tflite/src/tensorflow/lite/delegates/xnnpack/xnnpack_delegate.cc:1230:12

SUMMARY: AddressSanitizer: heap-buffer-overflow third_party/xnnpack/src/src/xx-copy/xx-copy-scalar-memcpy.c:18:3

```
## Root cause

The bug is in `GetPool2dTfLitePaddingMode()` in `graph_builder_tflite.cc` (line 354):

```
base::expected<TfLitePadding, std::string> GetPool2dTfLitePaddingMode(
    const mojom::Padding2d& padding2d, ..., const webnn::Size2d<uint32_t>& output) {
  std::array<uint32_t, 4> explicit_padding = { ... };
  std::array<uint32_t, 4> no_padding = {0, 0, 0, 0};
  if (explicit_padding == no_padding) {
    return TfLitePadding{.mode = ::tflite::Padding_VALID};  // BUG
  }
  // ... ceil rounding handling code (lines 394-412) never reached ...
}

```

When explicit padding is `[0,0,0,0]`, the function immediately returns `Padding_VALID` without checking whether the output dimensions require ceil rounding. This bypasses the ceil rounding handling code at lines 394-412, which would add extra ending padding to make TFLite's floor-based formula produce the correct output size.

The consequence is a shape mismatch between WebNN's validated graph and XNNPACK's internal computation: WebNN computes pool output shapes using ceil rounding, but XNNPACK recomputes them using floor division. The concat operator then reads past the smaller actual allocation.

Removing the early return and rebuilding content\_shell eliminates the crash.

## Bisection

**Introducing commit:** `6c9e4fea79849343c09bae0214cd76904f43be22` (2024-03-13)
**Title:** "webnn: Support Pool2d in in //services/webnn/tflite"
**CL:** <https://chromium-review.googlesource.com/c/chromium/src/+/5359192>

The parent commit returned `"pool2d is not implemented"` for pool2d. This commit added `SerializePool2d()`, which reused `GetTfLitePaddingMode()` (written for Conv2d) without ceil rounding awareness. The Blink IDL already had `roundingType: 'ceil'` at this point, so the bug was immediately reachable from JavaScript.

Verified by simulating both states on the current tree: disabling pool2d serialization produces no crash; re-enabling it reproduces the heap-buffer-overflow.

#### Impact analysis

## Affected platforms

Tested on Linux (x86\_64) with the TFLite+XNNPACK backend. The bug is in `graph_builder_tflite.cc` which is used on all platforms with the TFLite backend: Linux, Android (ARM64, x86/x64), and ChromeOS.

## Impact

- **Attack vector:** Any website, no user interaction required beyond navigation. WebNN is behind a feature flag (`WebMachineLearningNeuralNetwork`), which is not yet enabled by default, but eligible for VRP according to the [rules](https://bughunters.google.com/about/rules/chrome-friends/chrome-vulnerability-reward-program-rules#chrome-fuzzer-program:~:text=Bugs%20in%20unlaunched,message%20at%20runtime.) and it is also in origin trial since Jan 31: <https://chromium-review.googlesource.com/c/chromium/src/+/7518276>.
- **Process:** GPU process. On Android, this is unsandboxed.
- **Primitive:** OOB heap read.
- **Consequence:** Heap leak in a process shared between different origins. Maybe useful if heap leak can propagate back to JS

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

- [poc.html](attachments/poc.html) (text/html, 1.8 KB)
- [asan.log](attachments/asan.log) (text/plain, 34.4 KB)

## Timeline

### cl...@appspot.gserviceaccount.com (2026-02-12)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5154738714640384.

### re...@chromium.org (2026-02-12)

Junwei, please take a look at this similar padding computation bug.

### aj...@google.com (2026-02-12)

Repros on Windows with appropriate options:

```
D:\chromium\src [(95b70d9...)]> run-chrome-asan --no-first-run --disable-extensions --no-sandbox --enable-features=WebMachineLearningNeuralNetwork --disable-features=WebNNOnnxRuntime --enable-logging --log-file=d:\temp\asan.log D:\pocs\baba-483971526\poc.html

... asan.log
=================================================================
==21984==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x11e6605a12e0 at pc 0x7ffc4940b37c bp 0x004f8a1fe1f0 sp 0x004f8a1fe238
READ of size 12 at 0x11e6605a12e0 thread T34
[22472:57432:0212/143748.173:ERROR:google_apis\gcm\engine\registration_request.cc:291] Registration response error message: DEPRECATED_ENDPOINT
    #0 0x7ffc4940b37b  (d:\chromium\src\out\Asan\clang_rt.asan_dynamic-x86_64.dll+0x18004b37b)
    #1 0x7ffbb6391b97 in xnn_xx_copy_ukernel__scalar_memcpy D:\chromium\src\third_party\xnnpack\src\src\xx-copy\xx-copy-scalar-memcpy.c:18:3


```

Setting S0 as (pending an OT being turned off) this affects Android.

### aj...@google.com (2026-02-12)

foundin 124 based on bisect from reporter.

### ch...@google.com (2026-02-13)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-02-13)

Setting Priority to P0 to match Severity s0. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### aj...@google.com (2026-02-13)

Severity -> High as Android OT is being disabled.

### cl...@appspot.gserviceaccount.com (2026-02-18)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5655717692243968.

### cl...@appspot.gserviceaccount.com (2026-02-19)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5463324414115840.

### re...@chromium.org (2026-02-20)

Proposed fix out for review: <https://chromium-review.googlesource.com/c/chromium/src/+/7591423>

### dx...@google.com (2026-02-20)

Project: chromium/src  

Branch:  main  

Author:  Reilly Grant [reillyg@chromium.org](mailto:reillyg@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7591423>

webnn: Compute TFLite padding even without explicit padding

---


Expand for full commit details
```
     
    TFLite and WebNN differ on their default rounding modes and so we always 
    need to do the checks below to figure out if padding is needed. 
     
    The test changes update an existing failing test which now produces a 
    different value. 
     
    Fixed: 483971526 
    Change-Id: I15bb79370e39b05f1d0bc49ac75c56127be5b5bc 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7591423 
    Reviewed-by: Jiewei Qian <qjw@chromium.org> 
    Auto-Submit: Reilly Grant <reillyg@chromium.org> 
    Commit-Queue: Jiewei Qian <qjw@chromium.org> 
    Commit-Queue: Reilly Grant <reillyg@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1587587}

```

---

Files:

- M `services/webnn/tflite/graph_builder_tflite.cc`
- M `third_party/blink/web_tests/platform/linux/virtual/webnn-service-with-gpu/external/wpt/webnn/conformance_tests/averagePool2d.https.any_gpu-expected.txt`
- M `third_party/blink/web_tests/platform/mac/virtual/webnn-service-with-gpu/external/wpt/webnn/conformance_tests/averagePool2d.https.any_gpu-expected.txt`
- M `third_party/blink/web_tests/virtual/webnn-service-on-cpu/external/wpt/webnn/conformance_tests/averagePool2d.https.any_cpu-expected.txt`
- M `third_party/blink/web_tests/virtual/webnn-service-on-npu/external/wpt/webnn/conformance_tests/averagePool2d.https.any_npu-expected.txt`

---

Hash: [ce45888b8732e18758b0ee299bc307c2be7e062e](https://chromiumdash.appspot.com/commit/ce45888b8732e18758b0ee299bc307c2be7e062e)  

Date: Fri Feb 20 02:53:10 2026


---

### ch...@google.com (2026-02-20)

Security Merge Request Consideration: Requesting merge to extended stable (M144) because latest trunk commit (1587587) appears to be after extended stable branch point (1552494).
Security Merge Request Consideration: Requesting merge to stable (M145) because latest trunk commit (1587587) appears to be after stable branch point (1568190).
Security Merge Request Consideration: Requesting merge to beta (M146) because latest trunk commit (1587587) appears to be after beta branch point (1582197).
Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### re...@chromium.org (2026-02-20)

ClusterFuzz has confirmed that <https://clusterfuzz.com/testcase-detail/5463324414115840> has been fixed.

### re...@chromium.org (2026-02-20)

**Which CLs should be backmerged? (Please include Gerrit links.)**  

<https://chromium-review.googlesource.com/7591423>

**Has this fix been verified on Canary to not pose any stability regressions?**  

Not yet, 147.0.7698.0 has not yet been released.

**Does this fix pose any potential non-verifiable stability risks?**  

Given the test coverage we have an ClusterFuzz verification this should be safe.

**Does this fix pose any known compatibility risks?**  

The fix changed the output of one test which was already producing an incorrect value, indicating that there continue to be some correctness issues in this area but the passing test cases continue to pass.

**Does it require manual verification by the test team? If so, please describe required testing.**  

No.

### ch...@google.com (2026-02-21)

Merge review required: M146 is already shipping to beta.

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
Owners: lmenezes (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), govind (Mobile US), eakpobaro (Mobile EMEA)

### re...@chromium.org (2026-02-23)

**Why does your merge fit within the merge criteria for these milestones?**  

Yes, this is a security issue.

**What changes specifically would you like to merge? Please link to Gerrit:**  

<https://chromium-review.googlesource.com/c/chromium/src/+/7591423>

**Have the changes been released and tested on canary?**  

Yes.

**Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?**  

Yes, it is enabled at 100% (waterfall) but can be controlled by the `WebMachineLearningNeuralNetwork` feature flag.

**If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing:**  

No manual testing required.

### dr...@chromium.org (2026-02-24)

No crashes in Canary. Given this is an S1 security bug, we should merge to all three active release branches. Approving all three now.

### dx...@google.com (2026-02-24)

Project: chromium/src  

Branch:  refs/branch-heads/7680  

Author:  Reilly Grant [reillyg@chromium.org](mailto:reillyg@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7600617>

[M-146] webnn: Compute TFLite padding even without explicit padding

---


Expand for full commit details
```
     
    TFLite and WebNN differ on their default rounding modes and so we always 
    need to do the checks below to figure out if padding is needed. 
     
    The test changes update an existing failing test which now produces a 
    different value. 
     
    (cherry picked from commit ce45888b8732e18758b0ee299bc307c2be7e062e) 
     
    Fixed: 483971526 
    Change-Id: I15bb79370e39b05f1d0bc49ac75c56127be5b5bc 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7591423 
    Reviewed-by: Jiewei Qian <qjw@chromium.org> 
    Auto-Submit: Reilly Grant <reillyg@chromium.org> 
    Commit-Queue: Jiewei Qian <qjw@chromium.org> 
    Commit-Queue: Reilly Grant <reillyg@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1587587} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7600617 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Cr-Commit-Position: refs/branch-heads/7680@{#1181} 
    Cr-Branched-From: 76b7d80e5cda23fe6537eed26d68c92e995c7f39-refs/heads/main@{#1582197}

```

---

Files:

- M `services/webnn/tflite/graph_builder_tflite.cc`
- M `third_party/blink/web_tests/platform/linux/virtual/webnn-service-with-gpu/external/wpt/webnn/conformance_tests/averagePool2d.https.any_gpu-expected.txt`
- M `third_party/blink/web_tests/platform/mac/virtual/webnn-service-with-gpu/external/wpt/webnn/conformance_tests/averagePool2d.https.any_gpu-expected.txt`
- M `third_party/blink/web_tests/virtual/webnn-service-on-cpu/external/wpt/webnn/conformance_tests/averagePool2d.https.any_cpu-expected.txt`
- M `third_party/blink/web_tests/virtual/webnn-service-on-npu/external/wpt/webnn/conformance_tests/averagePool2d.https.any_npu-expected.txt`

---

Hash: [60d0cd906918708ecb27c1f73cbd748d0249f5aa](https://chromiumdash.appspot.com/commit/60d0cd906918708ecb27c1f73cbd748d0249f5aa)  

Date: Tue Feb 24 02:23:50 2026


---

### re...@chromium.org (2026-02-24)

Due to merge conflicts I'm going to stop at cherry-picking this to M-146, the first release where the feature including this code is enabled by default.

### go...@google.com (2026-02-24)

Please merge your change to M146 by 11:00 AM PT, Tuesday, Feb 24th so it gets picked up for M146 Early Stable release. Thank you.

### go...@google.com (2026-02-24)

[Bulk Edit]

Please merge your change to M146 by 12:30 PM PT, today, Feb 24th so it gets picked up for M146 Early Stable release tomorrow. Thank you.

### sr...@chromium.org (2026-02-24)

pls complete the merges to 145/144 as well 

### pe...@google.com (2026-02-24)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### re...@chromium.org (2026-02-24)

drubery@, are you okay not merging this to M-145 and M-144 since this feature was not enabled by default on those releases and the code changed substantially between M-145 and M-146 so this is a non-trivial merge.

### dr...@chromium.org (2026-02-24)

Ah, yes. I forgot that's what we'd been doing for WebNN bugs. Removing the 144 and 145 merge labels.

### qk...@google.com (2026-02-26)

Added "Not-Applicable-138"  because M138 codebase doesn't have the function that the fix modified. Thus, we cannot merge the fix[1] to M138 without dependent CLs. And the feature was not enabled in M144 by default. So we added LTS-NotApplicable-144 lable as well.

[1] https://chromium-review.git.corp.google.com/c/chromium/src/+/7600617

### sp...@google.com (2026-03-05)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $43000.00 for this report.

Rationale for this decision:
High quality with Bisect. Memory corruption in a highly privileged process (e.g. GPU, network processes).


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-05-30)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/483971526)*
