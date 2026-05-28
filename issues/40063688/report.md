# Security: UAF in blink::MLGraphXnnpack::ComputeOnBackgroundThread

| Field | Value |
|-------|-------|
| **Issue ID** | [40063688](https://issues.chromium.org/issues/40063688) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebML |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | m....@gmail.com |
| **Assignee** | qj...@chromium.org |
| **Created** | 2023-03-20 |
| **Bounty** | $8,000.00 |

## Description

UAF in blink::MLGraphXnnpack::ComputeOnBackgroundThread

#Version
asan-win32-release_x64-1119039

#Reproduce
chrome --js-flags="-expose-gc" --no-sandbox --enable-blink-test-features --allow-file-access-from-files --user-data-dir=test --enable-logging=stderr poc.html poc.html poc.html poc.html poc.html
Ensure that the number of poc.html tabs is double the number of CPU cores for stable reproduction

#Type of crash
render tab

#Analysis
The root cause is the same as 1425370, 
but it is caused by different calls to different CLs, 
so I report here separately, please do not duplicate to another, 
because it involves VRP issues

1. MLGraphXnnpack::ComputeAsyncImpl can called from worker thread
2. ComputeAsyncImpl will post ComputeOnBackgroundThread to the thread pool for execution, where the parameters are wrapped in WrapCrossThreadPersistent[1]
3. When worker thread get terminal, ComputeOnBackgroundThread will access freed object cause UAF[3]

[1] https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/ml/webnn/ml_graph_xnnpack.cc;drc=c91306793e6bc6889ac28e1a98176c004f3558fc;l=1268
[2]
https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/ml/webnn/ml_graph_xnnpack.cc;drc=c91306793e6bc6889ac28e1a98176c004f3558fc;l=1283


#bisect:
https://chromium-review.googlesource.com/c/chromium/src/+/4237384

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 11.4 KB)
- [poc.html](attachments/poc.html) (text/plain, 1.2 KB)

## Timeline

### [Deleted User] (2023-03-20)

[Empty comment from Monorail migration]

### ts...@chromium.org (2023-03-20)

Couldn't reproduce locally (possibly because I have too many cores), but given a meaningful ASAN trace and a bisect, we can proceed.
VRP will later decide whether this is the same as 1425370 after both are fixed.
Alas, the ml/ directory does not have DIR_METADATA, setting component to generic modularization.

[Monorail components: Blink>Internals>Modularization]

### qj...@chromium.org (2023-03-21)

[Empty comment from Monorail migration]

[Monorail components: -Blink>Internals>Modularization Blink>WebML]

### [Deleted User] (2023-03-21)

The assigned owner "ningxin.hu@intel.com" is not able to receive e-mails, please re-triage.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### qj...@chromium.org (2023-03-22)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-03-24)

introduced in 112, requires --enable-blink-test-features so setting as SI-None

### am...@chromium.org (2023-03-24)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-03-24)

Hi qjw@, since this bug cannot be assigned to ningxin.hu due to email bounce-backs, so ownership is rejected by the bot, is it okay if we assign this to you? 
Security bugs cannot go without owners so it's putting red in our triage dashboard. Please feel free to reassign to someone who can accept ownership if there is someone this can be assigned to. Thanks! 

### am...@chromium.org (2023-03-24)

[Empty comment from Monorail migration]

### qj...@chromium.org (2023-03-27)

Yep. I can take the owner (per security triage policy). Ningxin has been working on a fix and should be the owner.

I'm not sure what's causing the email bounce (this has caused some nuance that we can mostly work around).

### ni...@intel.com (2023-03-30)

The fix is ready for review: https://chromium-review.googlesource.com/c/chromium/src/+/4382891

I verified locally that the UAF issue disappeared after applying the fix. If someone else can help verify, that would be highly appreciated.

### gi...@appspot.gserviceaccount.com (2023-04-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/7131bbb91d0bbcd502b53add8a8c715f2b9dffc6

commit 7131bbb91d0bbcd502b53add8a8c715f2b9dffc6
Author: Ningxin Hu <ningxin.hu@intel.com>
Date: Wed Apr 05 00:31:54 2023

WebNN: Disable async build and compute methods for dedicated worker

This CL disables async `MLGraphBuilder.build()` and
`MLContext.compute()` for dedicated worker context, because the current
implementation is not safe to be called in a Web worker.

The existing `MLGraphXnnpack::BuildAsyncImpl()` and
`MLGraphXnnpack::ComputeAsyncImpl()` send the objects wrapped by
`CrossThreadPersistent` [1] to worker pool thread for processing.
However, `CrossThreadPersistent` doesn't protect the heap owning an
object from terminating. This would cause UAF (use-after-free) issue,
when the calling Web worker thread terminates, e.g. user code calls
`worker.terminate()`, `MLGraphXnnpack::BuildOnBackgroundThread()` or
`MLGraphXnnpack::ComputeOnBackgroundThread()` running worker pool thread
may access these freed objects.

The longer-term solution is left as TODOs. It may refer to the similar
fix of `FileSystemAccessRegularFileDelegate` [2] that transfers the
ownership of objects instead of wrapping them in
`CrossThreadPersistent`.

[1]: https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/platform/heap/cross_thread_persistent.h;drc=ddf482c0cf47fc8e47e5cfc5c112e2313e066cb8;l=13
[2]: https://bugs.chromium.org/p/chromium/issues/detail?id=1299743

Bug: 1425370,1425922
Change-Id: I294ab87859cc0954ae4f97e759e5111cef537a92
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4360360
Commit-Queue: ningxin hu <ningxin.hu@intel.com>
Reviewed-by: Jiewei Qian <qjw@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1126346}

[modify] https://crrev.com/7131bbb91d0bbcd502b53add8a8c715f2b9dffc6/third_party/blink/web_tests/platform/mac/external/wpt/webnn/relu.https.any.worker-expected.txt
[modify] https://crrev.com/7131bbb91d0bbcd502b53add8a8c715f2b9dffc6/third_party/blink/web_tests/platform/mac/external/wpt/webnn/pooling.https.any.worker-expected.txt
[add] https://crrev.com/7131bbb91d0bbcd502b53add8a8c715f2b9dffc6/third_party/blink/web_tests/platform/win/external/wpt/webnn/softmax.https.any.worker-expected.txt
[add] https://crrev.com/7131bbb91d0bbcd502b53add8a8c715f2b9dffc6/third_party/blink/web_tests/platform/win/external/wpt/webnn/leaky_relu.https.any.worker-expected.txt
[modify] https://crrev.com/7131bbb91d0bbcd502b53add8a8c715f2b9dffc6/third_party/blink/web_tests/platform/mac/external/wpt/webnn/reshape.https.any.worker-expected.txt
[modify] https://crrev.com/7131bbb91d0bbcd502b53add8a8c715f2b9dffc6/third_party/blink/web_tests/platform/win/external/wpt/webnn/pooling.https.any.worker-expected.txt
[modify] https://crrev.com/7131bbb91d0bbcd502b53add8a8c715f2b9dffc6/third_party/blink/web_tests/platform/mac/external/wpt/webnn/clamp.https.any.worker-expected.txt
[modify] https://crrev.com/7131bbb91d0bbcd502b53add8a8c715f2b9dffc6/third_party/blink/web_tests/platform/win/external/wpt/webnn/conv2d.https.any.worker-expected.txt
[modify] https://crrev.com/7131bbb91d0bbcd502b53add8a8c715f2b9dffc6/third_party/blink/renderer/modules/ml/webnn/ml_graph_builder.idl
[modify] https://crrev.com/7131bbb91d0bbcd502b53add8a8c715f2b9dffc6/third_party/blink/web_tests/platform/mac/external/wpt/webnn/leaky_relu.https.any.worker-expected.txt
[modify] https://crrev.com/7131bbb91d0bbcd502b53add8a8c715f2b9dffc6/third_party/blink/web_tests/webexposed/global-interface-listing-dedicated-worker-expected.txt
[add] https://crrev.com/7131bbb91d0bbcd502b53add8a8c715f2b9dffc6/third_party/blink/web_tests/platform/win/external/wpt/webnn/relu.https.any.worker-expected.txt
[modify] https://crrev.com/7131bbb91d0bbcd502b53add8a8c715f2b9dffc6/third_party/blink/web_tests/platform/mac/external/wpt/webnn/pad.https.any.worker-expected.txt
[modify] https://crrev.com/7131bbb91d0bbcd502b53add8a8c715f2b9dffc6/third_party/blink/renderer/modules/ml/webnn/ml_graph_xnnpack.cc
[add] https://crrev.com/7131bbb91d0bbcd502b53add8a8c715f2b9dffc6/third_party/blink/web_tests/platform/win/external/wpt/webnn/hard_swish.https.any.worker-expected.txt
[modify] https://crrev.com/7131bbb91d0bbcd502b53add8a8c715f2b9dffc6/third_party/blink/web_tests/platform/mac/external/wpt/webnn/softmax.https.any.worker-expected.txt
[modify] https://crrev.com/7131bbb91d0bbcd502b53add8a8c715f2b9dffc6/third_party/blink/web_tests/platform/win/external/wpt/webnn/pad.https.any.worker-expected.txt
[add] https://crrev.com/7131bbb91d0bbcd502b53add8a8c715f2b9dffc6/third_party/blink/web_tests/platform/win/external/wpt/webnn/transpose.https.any.worker-expected.txt
[modify] https://crrev.com/7131bbb91d0bbcd502b53add8a8c715f2b9dffc6/third_party/blink/web_tests/platform/win/external/wpt/webnn/gemm.https.any.worker-expected.txt
[modify] https://crrev.com/7131bbb91d0bbcd502b53add8a8c715f2b9dffc6/third_party/blink/web_tests/platform/mac/external/wpt/webnn/elementwise_binary.https.any.worker-expected.txt
[add] https://crrev.com/7131bbb91d0bbcd502b53add8a8c715f2b9dffc6/third_party/blink/web_tests/platform/win/external/wpt/webnn/concat.https.any.worker-expected.txt
[add] https://crrev.com/7131bbb91d0bbcd502b53add8a8c715f2b9dffc6/third_party/blink/web_tests/platform/win/external/wpt/webnn/reshape.https.any.worker-expected.txt
[add] https://crrev.com/7131bbb91d0bbcd502b53add8a8c715f2b9dffc6/third_party/blink/web_tests/platform/win/external/wpt/webnn/clamp.https.any.worker-expected.txt
[modify] https://crrev.com/7131bbb91d0bbcd502b53add8a8c715f2b9dffc6/third_party/blink/web_tests/platform/mac/external/wpt/webnn/conv2d.https.any.worker-expected.txt
[modify] https://crrev.com/7131bbb91d0bbcd502b53add8a8c715f2b9dffc6/third_party/blink/web_tests/platform/win/external/wpt/webnn/elementwise_binary.https.any.worker-expected.txt
[modify] https://crrev.com/7131bbb91d0bbcd502b53add8a8c715f2b9dffc6/third_party/blink/web_tests/platform/mac/external/wpt/webnn/concat.https.any.worker-expected.txt
[add] https://crrev.com/7131bbb91d0bbcd502b53add8a8c715f2b9dffc6/third_party/blink/web_tests/platform/win/external/wpt/webnn/sigmoid.https.any.worker-expected.txt
[modify] https://crrev.com/7131bbb91d0bbcd502b53add8a8c715f2b9dffc6/third_party/blink/web_tests/platform/win/external/wpt/webnn/idlharness.https.any.worker-expected.txt
[modify] https://crrev.com/7131bbb91d0bbcd502b53add8a8c715f2b9dffc6/third_party/blink/web_tests/platform/mac/external/wpt/webnn/idlharness.https.any.worker-expected.txt
[modify] https://crrev.com/7131bbb91d0bbcd502b53add8a8c715f2b9dffc6/third_party/blink/web_tests/platform/mac/external/wpt/webnn/sigmoid.https.any.worker-expected.txt
[modify] https://crrev.com/7131bbb91d0bbcd502b53add8a8c715f2b9dffc6/third_party/blink/web_tests/platform/mac/external/wpt/webnn/transpose.https.any.worker-expected.txt
[modify] https://crrev.com/7131bbb91d0bbcd502b53add8a8c715f2b9dffc6/third_party/blink/renderer/modules/ml/ml_context.idl
[modify] https://crrev.com/7131bbb91d0bbcd502b53add8a8c715f2b9dffc6/third_party/blink/web_tests/platform/mac/external/wpt/webnn/hard_swish.https.any.worker-expected.txt
[modify] https://crrev.com/7131bbb91d0bbcd502b53add8a8c715f2b9dffc6/third_party/blink/web_tests/platform/mac/external/wpt/webnn/gemm.https.any.worker-expected.txt


### gi...@appspot.gserviceaccount.com (2023-04-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/beb6d8733810e43dc3878d0d202f435d2eaa6835

commit beb6d8733810e43dc3878d0d202f435d2eaa6835
Author: Ningxin Hu <ningxin.hu@intel.com>
Date: Tue Apr 18 04:49:35 2023

WebNN: Fix UAF issue in MLGraphXnnpack::ComputeOnBackgroundThread()

This CL follows the CL [1] and continues to fix the UAF issue of
`MLGraphXnnpack`. This CL replaces the usage of `CrossThreadPersistent`
[2] with `CrossThreadHandle` [3] in `ComputeOnBackgroundThread()` to
pass GC objects back and forth between the calling thread and background
thread and ensure these objects are only accessed by the thread owning
the heap.

To prevent the calling thread from modifying the input and output
buffers while `ComputeOnBackgroundThread()` is running, the input and
output `ArrayBufferView` should be transferred first. However, because
the transferred `ArrayBufferView` is still allocated on the heap, it is
not safe to be accessed in the background thread. This CL splits the
`ArrayBufferView` transferring algorithm into two steps. First, an
`ArrayBufferView` is transferred to `ArrayBufferViewInfo` which doesn’t
contain any GC objects and can be safely posted to the background thread
for accessing. After the background thread finishes the computation, the
`ArrayBufferViewInfo` will be posted back to the calling thread. And it
will be used to create a new `ArrayBufferView` and return to user code.

To avoid `MLGraphXnnpack` who owns the XNNPACK Runtime being released
while `ComputeOnBackgroundThread()` is running, this CL introduces
`XnnRuntimeWrapper` that wraps XNNPACK Runtime object and its supporting
objects. `XnnRuntimeWrapper` inherits `ThreadSafeRefCounted` and is kept
alive by `scoped_refptr` while the background thread invokes the
runtime. XNNPACK Runtime invocation is not thread safe. To avoid using
lock, a `SequencedTaskRunner` is used to invoke the XNNPACK Runtime in a
worker pool thread.

[1]: https://chromium-review.googlesource.com/c/chromium/src/+/4373880
[2]: https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/platform/heap/cross_thread_persistent.h;l=16
[3]: https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/platform/heap/cross_thread_handle.h;l=49

Bug: 1425922
Change-Id: I8f65465112061f2a96cf99ae7a3bc43b01aa4782
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4382891
Reviewed-by: Jiewei Qian <qjw@chromium.org>
Commit-Queue: ningxin hu <ningxin.hu@intel.com>
Cr-Commit-Position: refs/heads/main@{#1131676}

[modify] https://crrev.com/beb6d8733810e43dc3878d0d202f435d2eaa6835/third_party/blink/renderer/modules/ml/webnn/ml_graph_cros.cc
[modify] https://crrev.com/beb6d8733810e43dc3878d0d202f435d2eaa6835/third_party/blink/renderer/modules/ml/webnn/ml_graph_cros.h
[modify] https://crrev.com/beb6d8733810e43dc3878d0d202f435d2eaa6835/third_party/blink/renderer/modules/ml/webnn/ml_graph_xnnpack.cc
[modify] https://crrev.com/beb6d8733810e43dc3878d0d202f435d2eaa6835/third_party/blink/renderer/modules/ml/webnn/ml_graph_builder_test.cc
[modify] https://crrev.com/beb6d8733810e43dc3878d0d202f435d2eaa6835/third_party/blink/renderer/modules/ml/webnn/ml_graph.cc
[modify] https://crrev.com/beb6d8733810e43dc3878d0d202f435d2eaa6835/third_party/blink/renderer/modules/ml/webnn/ml_graph.h
[modify] https://crrev.com/beb6d8733810e43dc3878d0d202f435d2eaa6835/third_party/blink/renderer/modules/ml/webnn/ml_graph_xnnpack.h


### ni...@intel.com (2023-04-18)

The fixes for this issue and related https://bugs.chromium.org/p/chromium/issues/detail?id=1425370 have been landed. Thanks the review by Jiewei @qjw@chromium.org!

Regarding to the discussion with Jiewei in CL review (https://chromium-review.googlesource.com/c/chromium/src/+/4382891/comment/07788023_587e758d/), as a  follow-up, I'll open an issue against WebNN spec to discuss the async methods in dedicated worker that cause this security issue. My question is whether there are any restrictions to discuss this security issue in public. When this issue can be viewed by public?

### am...@chromium.org (2023-04-18)

Security issues should be marked fixed as soon as the resolving CL has landed. Once that is achieved the bug is automatically publicly disclosed 14 weeks after updated as fixed (as long as the bug is not under security embargo). Any web spec issue that is opened before that time should avoid explicit details of the any security issues, such as this, that have not yet been publicly disclosed.

### [Deleted User] (2023-04-18)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-18)

[Empty comment from Monorail migration]

### ni...@intel.com (2023-04-19)

Thanks for the guideline @amyressler@chromium.org! I'll follow this guideline when discuss WebNN spec issue in WebML WG.

### am...@google.com (2023-04-27)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-04-27)

Congratulations! The VRP Panel has decided to award you $7,000 for this report + $1,000 bisect bonus. Thank you for your effort and reporting this issue to us -- nice work! 

### am...@google.com (2023-04-29)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-25)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-07-25)

This issue was migrated from crbug.com/chromium/1425922?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40063688)*
