# Heap corruption in GPU process via unchecked tensor rank in WebNN constant transpose

| Field | Value |
|-------|-------|
| **Issue ID** | [493099940](https://issues.chromium.org/issues/493099940) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebML |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | je...@gmail.com |
| **Assignee** | we...@intel.com |
| **Created** | 2026-03-16 |
| **Bounty** | $36,000.00 |

## Description

# Heap corruption in GPU process via unchecked tensor rank in WebNN constant transpose

## Summary

A memory corruption vulnerability exists in Chromium's WebNN implementation on all desktop platforms (Windows, macOS, Linux). When a compromised renderer sends a `CreateGraph` Mojo message containing a constant operand with rank 7 or 8 and a non-empty `pending_permutation`, the GPU process passes this rank directly to XNNPACK's one-shot transpose without validation. XNNPACK rejects ranks above 6 through an error path that calls `free()` on stack-allocated objects, corrupting allocator metadata in the GPU process. Since the GPU process runs outside the renderer sandbox, this represents a sandbox-escape attack surface.

## Bisect

Introducing Commit: `cdd1f63c02a65c37ccdb85e85b25dbec456c9914`

- Date: 2026-02-25
- Author: chromium-autoroll
- Review: <https://chromium-review.googlesource.com/c/chromium/src/+/7606043>

## Root Cause

The vulnerability arises from a mismatch between WebNN's maximum tensor rank (8) and XNNPACK's maximum supported dimensions (6), combined with an unsafe error cleanup path in XNNPACK's one-shot transpose functions.

WebNN accepts operand descriptors with up to 8 dimensions, as enforced in `ValidateAndGetByteLength`:

```
// services/webnn/public/cpp/operand_descriptor.h
if (shape.size() > 8) {
  return base::unexpected(
      "Invalid descriptor: The maximum rank of an operand is 8.");
}

```

XNNPACK only supports up to 6:

```
// third_party/xnnpack/src/include/xnnpack.h
#define XNN_MAX_TENSOR_DIMS 6

```

During graph creation, `WebNNGraphBuilderImpl::CreateGraph` posts `TransposePendingPermutation` to a thread pool. This function iterates over all constant operands that carry a `pending_permutation` (set by `ConstantFoldingTransformer` when a transpose of a constant is folded) and calls the appropriate XNNPACK one-shot transpose function:

```
// services/webnn/webnn_graph_builder_impl.cc
case 4: {
  xnn_status status = xnn_run_transpose_nd_x32(
      data.data(), transposed_data.data(), rank,
      shape.data(), perm.data(), 0, nullptr);
  CHECK_EQ(status, xnn_status_success);
  break;
}

```

The `rank` variable comes directly from the operand descriptor's shape and is not clamped to `XNN_MAX_TENSOR_DIMS` before the call.

Inside XNNPACK, `xnn_run_transpose_nd_x32` delegates to `run_transpose_nd`, which allocates the operator and its compute parameters on the stack:

```
// third_party/xnnpack/src/src/operators/transpose-nd.c
enum xnn_status run_transpose_nd(...) {
  struct xnn_operator transpose_op;
  memset(&transpose_op, 0, sizeof(transpose_op));
  struct compute_parameters compute;
  memset(&compute, 0, sizeof(compute));
  transpose_op.compute = &compute;
  ...
  enum xnn_status status = reshape_transpose_nd(&transpose_op, num_dims, ...);
}

```

When `reshape_transpose_nd` detects that `num_dims` exceeds `XNN_MAX_TENSOR_DIMS`, it branches to its error label, which unconditionally calls `xnn_delete_operator`:

```
// third_party/xnnpack/src/src/operators/transpose-nd.c
if (num_dims > XNN_MAX_TENSOR_DIMS) {
  xnn_log_error(...);
  goto error;
}
...
error:
  xnn_delete_operator(transpose_op);
  return status;

```

This error cleanup was written for the normal create/reshape/run path where the operator is heap-allocated. In the one-shot path, `transpose_op` is a stack-local variable. `xnn_delete_operator` calls `xnn_destroy_operator`, which frees `op->compute` (the stack address of `compute`), and then frees `op` itself (the stack address of `transpose_op`):

```
// third_party/xnnpack/src/src/operator-utils.c
enum xnn_status xnn_destroy_operator(xnn_operator_t op) {
  ...
  xnn_release_memory(op->compute);  // free(&compute) - stack address
  ...
}

// third_party/xnnpack/src/src/operator-delete.c
enum xnn_status xnn_delete_operator(xnn_operator_t op) {
  enum xnn_status status = xnn_destroy_operator(op);
  ...
  xnn_release_simd_memory(op);      // free(&transpose_op) - stack address
  ...
}

```

Both `xnn_release_memory` and `xnn_release_simd_memory` resolve to the allocator's `deallocate` function. Passing a stack address to `free()` is undefined behavior that corrupts allocator metadata. With standard malloc implementations this corrupts the freelist, potentially allowing subsequent allocations to return attacker-influenced addresses. PartitionAlloc detects the invalid address and terminates; ASAN reports it as a bad-free.

A compromised renderer can reach this code path by constructing a Mojo `CreateGraph` message containing a constant operand descriptor with rank 7 or 8 and a matching `pending_permutation` array. The `CreateForDeserialization` path in the GPU process validates that the permutation is well-formed but does not enforce XNNPACK's 6-dimension limit. The `kWebNNUseXNNPackForConstantTransposeFolding` feature is enabled by default.

## Reproduce

Tested at commit `3ad31ba232` on Windows 10 x64.

ASAN build configuration (`out/asan-release/args.gn`):

```
is_asan = true
is_debug = false
target_cpu = "x64"
is_component_build = true

```

The PoC requires a renderer-side patch to bypass the rank-6 validation for transpose inputs (simulating a compromised renderer). Apply the attached `patch.diff`, then rebuild:

```
cd D:\chromium\src
git apply issue_xnnpack004/patch.diff
autoninja -C out/asan-release chrome

```

Start an HTTP server and launch Chrome:

```
python -m http.server 9900 --bind 127.0.0.1 -d issue_xnnpack004

set ASAN_OPTIONS=detect_odr_violation=0
out\asan-release\chrome.exe --no-sandbox --enable-features=WebMachineLearningNeuralNetwork --enable-logging=stderr --user-data-dir=%TEMP%\poc_xnnpack004 http://127.0.0.1:9900/poc.html

```

The GPU process crashes within seconds. ASAN log:

```
==32108==ERROR: AddressSanitizer: attempting free on address which was not malloc()-ed: 0x127612b85650 in thread T23
    #0 0x7ffeb7dbc82f  (clang_rt.asan_dynamic-x86_64.dll+0x18004c82f)
    #1 0x7ffe10cba999 in xnn_destroy_operator third_party\xnnpack\src\src\operator-utils.c:197:3
    #2 0x7ffe10ca5575 in xnn_delete_operator third_party\xnnpack\src\src\operator-delete.c:21:28
    #3 0x7ffe11c56fcd in reshape_transpose_nd third_party\xnnpack\src\src\operators\transpose-nd.c:414:3
    #4 0x7ffe11c599ca in xnn_run_transpose_nd_x32 third_party\xnnpack\src\src\operators\transpose-nd.c:700:10
    #5 0x7ffe108889a1 in TransposePendingPermutation services\webnn\webnn_graph_builder_impl.cc:2824:31
    #6 0x7ffe108b30fa in base::internal::Invoker<...>::RunOnce base\functional\bind_internal.h:982:12
    #7 0x7ffe108d74ae in base::internal::ReturnAsParamAdapter<...> base\task\post_task_and_reply_with_result_internal.h:23:48
    #8 0x7ffe108d7d48 in base\functional\bind_internal.h:982:12
    #9 0x7ffecce8359b in base::internal::PostTaskAndReplyRelay::RunTaskAndPostReply base\threading\post_task_and_reply_impl.h:45:28
    #10 0x7ffecce83b44 in base::internal::Invoker<...>::RunOnce base\functional\bind_internal.h:982:12
    #11 0x7ffeccdd3e28 in base::TaskAnnotator::RunTaskImpl base\task\common\task_annotator.cc:229:34
    #12 0x7ffeccebe44c in base::internal::TaskTracker::RunContinueOnShutdown base\task\thread_pool\task_tracker.cc:668:3
    #13 0x7ffeccebcb94 in base::internal::TaskTracker::RunTask base\task\thread_pool\task_tracker.cc:506:5
    #14 0x7ffeccebbb4b in base::internal::TaskTracker::RunAndPopNextTask base\task\thread_pool\task_tracker.cc:394:5
    #15 0x7ffeccee7d20 in base::internal::WorkerThread::RunWorker base\task\thread_pool\worker_thread.cc:473:36
    #16 0x7ffeccee6b6f in base::internal::WorkerThread::RunPooledWorker base\task\thread_pool\worker_thread.cc:359:3
    #17 0x7ffecd05a45e in base::ThreadFunc base\threading\platform_thread_win.cc:112:13
    #18 0x7ffeb7dcdc6e  (clang_rt.asan_dynamic-x86_64.dll+0x18005dc6e)
    #19 0x7fff5b8b7373  (KERNEL32.DLL+0x180017373)
    #20 0x7fff5c4bcc90  (ntdll.dll+0x18004cc90)

Address 0x127612b85650 is located in stack of thread T23 at offset 592 in frame
    #0 0x7ffe11c5979f in xnn_run_transpose_nd_x32 third_party\xnnpack\src\src\operators\transpose-nd.c:699

  This frame has 2 object(s):
    [32, 528) 'transpose_op' (line 627)
    [592, 680) 'compute' (line 629) <== Memory access at offset 592 is inside this variable

Thread T23 created by T0 here:
    #0 0x7ffeb7dcdb84  (clang_rt.asan_dynamic-x86_64.dll+0x18005db84)
    #1 0x7ffecd059116 in base::CreateThreadInternal base\threading\platform_thread_win.cc:178:7
    #2 0x7ffeccee4f6f in base::internal::WorkerThread::Start base\task\thread_pool\worker_thread.cc:185:3
    #9 0x7ffe7b05b61a in content::GpuMain content\gpu\gpu_main.cc:421:16
    #10 0x7ffe816add1c in content::RunOtherNamedProcessTypeMain content\app\content_main_runner_impl.cc:762:14

SUMMARY: AddressSanitizer: bad-free third_party\xnnpack\src\src\operator-utils.c:197:3 in xnn_destroy_operator

Task trace:
    #0 in webnn::WebNNGraphBuilderImpl::CreateGraph services\webnn\webnn_graph_builder_impl.cc:2966:7

Command line: "out\asan-release\chrome.exe" --type=gpu-process --no-sandbox ...

```
## Credit

Please use c6eed09fc8b174b0f3eebedcceb1e792 as the credit for this vulnerability. Thank you.

## Attachments

- [asan.log](attachments/asan.log) (text/plain, 16.7 KB)
- [patch.diff](attachments/patch.diff) (text/x-diff, 1.2 KB)
- [poc.html](attachments/poc.html) (text/html, 1.8 KB)

## Timeline

### dr...@chromium.org (2026-03-16)

This reproduces as claimed. Because the WebNN Origin Trial is now disabled, this is Security\_Impact-None. Since it corrupts GPU memory without any preconditions, including on Android, marking S0.

### re...@chromium.org (2026-03-16)

The WebNN OT was re-enabled for desktop platforms in M-147 so this has security impact.

### cl...@appspot.gserviceaccount.com (2026-03-16)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5969289429417984.

### re...@chromium.org (2026-03-17)

Reporter, you can use MojoJS to develop a PoC that simulates a compromised renderer without requiring a patch.

### je...@gmail.com (2026-03-17)

I'm sorry, I'm not good at writing POCs with mojojs. Since #c2 has already reproduced it following my steps, it seems unnecessary?

Additionally, there seems to be an issue with Bisect, and I will update my bisect.

### je...@gmail.com (2026-03-17)

## Correct Bisect:

- Commit: 49152d6f530370d57a4735548477ce3f88d38ceb
- Date: 2025-09-21
- Author: JianxiaoLuIntel ([jianxiao.lu@intel.com](mailto:jianxiao.lu@intel.com))
- Subject: "WebNN: Use XNNPack to transpose pending permutation for weights"
- CL: <https://chromium-review.googlesource.com/c/chromium/src/+/6907217>

The reported bisect cdd1f63c02a65c37ccdb85e85b25dbec456c9914 (2026-02-25, ANGLE autoroll) is incorrect. The actual introducing commit is the one above, which replaced the safe manual element-by-element transpose loop in TransposePendingPermutation with direct calls to XNNPACK's xnn\_run\_transpose\_nd\_x\* functions, without checking that the rank is within XNNPACK's XNN\_MAX\_TENSOR\_DIMS = 6 limit. The original implementation by Phillis Tang (commit 60956efeeb295, 2025-08-01, "webnn: implement constant folding for transpose") was safe.

You can assign it based on bisect, thanks :)

### ni...@intel.com (2026-03-17)

@we...@intel.com will help on this issue. Thanks.

### ni...@intel.com (2026-03-17)

We may want to fall back to transpose loop implementation if constant tensor rank > XNN\_MAX\_TENSOR\_DIMS.

### ch...@google.com (2026-03-17)

Setting Priority to P0 to match Severity s0. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### dx...@google.com (2026-03-17)

Project: chromium/src  

Branch:  main  

Author:  Wei Wang [wei4.wang@intel.com](mailto:wei4.wang@intel.com)  

Link:    <https://chromium-review.googlesource.com/7673718>

[WebNN] Fall back to transpose loop implementation if rank > XNN\_MAX\_TENSOR\_DIMS

---


Expand for full commit details
```
     
    XNNPack's transpose implementation requires that the rank should not 
    exceed XNN_MAX_TENSOR_DIMS[1]. So fall back to transpose loop 
    implementation in `TransposePendingPermutation` if the requirement is 
    not met. 
     
    [1] https://github.com/google/XNNPACK/blob/925bce2ece9a38fdaef01a706a1758231894eaf0/src/operators/transpose-nd.c#L171 
     
    Bug: 493099940 
    Change-Id: Ie13366453d25d7a94e07975773c5e8ae058d917b 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7673718 
    Reviewed-by: Phillis Tang <phillis@chromium.org> 
    Reviewed-by: Hu, Ningxin <ningxin.hu@intel.com> 
    Commit-Queue: Reilly Grant <reillyg@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1600765}

```

---

Files:

- M `services/webnn/webnn_graph_builder_impl.cc`

---

Hash: [d379682812b1624202bd0b4c820b361afc8ecda2](https://chromiumdash.appspot.com/commit/d379682812b1624202bd0b4c820b361afc8ecda2)  

Date: Tue Mar 17 20:16:59 2026


---

### ch...@google.com (2026-03-18)

Security Merge Request Consideration: Requesting merge to beta (M147) because latest trunk commit (1600765) appears to be after beta branch point (1596535).
Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### ch...@google.com (2026-03-18)

Merge review required: M147 is already shipping to beta.

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

### re...@chromium.org (2026-03-18)

**Which CLs should be backmerged?**

<https://chromium-review.googlesource.com/7673718>

**Has this fix been verified on Canary to not pose any stability regressions?** Yes.   

**Does this fix pose any potential non-verifiable stability risks?** No.   

**Does this fix pose any known compatibility risks?** No.   

**Does it require manual verification by the test team?** No.

### re...@chromium.org (2026-03-18)

**Why does your merge fit within the merge criteria for these milestones?**  

It is a security issue.

**What changes specifically would you like to merge?**  

<https://chromium-review.googlesource.com/7673718>

**Have the changes been released and tested on canary?**  

Yes.

**Is this a new feature?**  

Yes. It is enabled by default but kill-switchable with the `WebMachineLearningNeuralNetwork` flag.

**If this merge addresses a major issue in the stable channel, does it require manual verification by the test team?**  

No.

### dr...@chromium.org (2026-03-20)

No crashes in Canary. Merge approved to M147.

### dx...@google.com (2026-03-21)

Project: chromium/src  

Branch:  refs/branch-heads/7727  

Author:  Wei Wang [wei4.wang@intel.com](mailto:wei4.wang@intel.com)  

Link:    <https://chromium-review.googlesource.com/7688755>

[M147] [WebNN] Fall back to transpose loop implementation if rank > XNN\_MAX\_TENSOR\_DIMS

---


Expand for full commit details
```
     
    XNNPack's transpose implementation requires that the rank should not 
    exceed XNN_MAX_TENSOR_DIMS[1]. So fall back to transpose loop 
    implementation in `TransposePendingPermutation` if the requirement is 
    not met. 
     
    [1] https://github.com/google/XNNPACK/blob/925bce2ece9a38fdaef01a706a1758231894eaf0/src/operators/transpose-nd.c#L171 
     
    (cherry picked from commit d379682812b1624202bd0b4c820b361afc8ecda2) 
     
    Bug: 493099940 
    Change-Id: Ie13366453d25d7a94e07975773c5e8ae058d917b 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7673718 
    Reviewed-by: Phillis Tang <phillis@chromium.org> 
    Reviewed-by: Hu, Ningxin <ningxin.hu@intel.com> 
    Commit-Queue: Reilly Grant <reillyg@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1600765} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7688755 
    Auto-Submit: Reilly Grant <reillyg@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7727@{#1081} 
    Cr-Branched-From: ce01102937348db7b88c8a4257ee4b3ac702eb1a-refs/heads/main@{#1596535}

```

---

Files:

- M `services/webnn/webnn_graph_builder_impl.cc`

---

Hash: [1b8caedd85097ecd40cb8fa9119cfca1d6cf3d12](https://chromiumdash.appspot.com/commit/1b8caedd85097ecd40cb8fa9119cfca1d6cf3d12)  

Date: Sat Mar 21 04:28:15 2026


---

### pe...@google.com (2026-03-21)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### re...@chromium.org (2026-03-21)

This feature was not enabled in M144.

### qk...@google.com (2026-03-24)

Labeled `LTS-NotApplicable-138` because M138 doens't have the suspected CL[1].

[1] https://chromium-review.googlesource.com/c/chromium/src/+/6907217

### qk...@google.com (2026-03-24)

Labeled `LTS-NotApplicable-144` because M144 has the suspected CL[1], but the feature was not enabled M144 according to comment #19.

[1] https://chromium-review.googlesource.com/c/chromium/src/+/6907217

### ds...@google.com (2026-03-27)

cl/890298213 (external PR: <https://github.com/google/XNNPACK/pull/9793>) will at least fix the bad-free crash.

### wf...@chromium.org (2026-04-01)

adding Android based on [comment#2](https://issues.chromium.org/issues/493099940#comment2)

### dx...@google.com (2026-04-01)

Project: chromium/src  

Branch:  main  

Author:  Wei Wang [wei4.wang@intel.com](mailto:wei4.wang@intel.com)  

Link:    <https://chromium-review.googlesource.com/7703552>

[WebNN] Add unit test for `TransposePendingPermutation` with rank greater than 6

---


Expand for full commit details

```[WebNN] Add unit test for `TransposePendingPermutation` with rank greater than 6

```
Add regression unit test for `TransposePendingPermutation` with rank 
greater than 6. In this case, it should fall back to transpose loop 
implementation instead of XNNPack's transpose implementation. 
 
Bug: 493099940 
Change-Id: I441f8cdf4461d8a5ffeafcfcea615dff447cf598 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7703552 
Reviewed-by: Phillis Tang <phillis@chromium.org> 
Commit-Queue: Wang, Wei4 <wei4.wang@intel.com> 
Reviewed-by: Hu, Ningxin <ningxin.hu@intel.com> 
Cr-Commit-Position: refs/heads/main@{#1608247}

```
```

---

Files:
* M       `services/webnn/webnn_graph_builder_impl_unittest.cc`
* M       `services/webnn/webnn_test_utils.cc`
* M       `services/webnn/webnn_test_utils.h`

---

Hash: [f3dd0b08e1b3010fd9c87dba240e4175176ff468](https://chromiumdash.appspot.com/commit/f3dd0b08e1b3010fd9c87dba240e4175176ff468)\
Date: Wed Apr 1 01:59:03 2026

</details>

---

```

### aj...@google.com (2026-04-01)

Sev High as Desktop Platforms

### sp...@google.com (2026-04-02)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $36000.00 for this report.

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

### ch...@google.com (2026-06-24)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/493099940)*
