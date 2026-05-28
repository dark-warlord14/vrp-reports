# Segv on unknown address in v8::internal::TracedHandlesImpl::Create

| Field | Value |
|-------|-------|
| **Issue ID** | [40062839](https://issues.chromium.org/issues/40062839) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>API, Blink>JavaScript>GarbageCollection, Blink>ViewTransitions |
| **Platforms** | Linux, Mac, Windows |
| **Reporter** | m....@gmail.com |
| **Assignee** | kh...@chromium.org |
| **Created** | 2023-01-31 |
| **Bounty** | $9,000.00 |

## Description

Detailed Report: https://clusterfuzz.com/testcase?key=4511251945422848

Fuzzer: b0ring_webidl_fuzzer
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Segv on unknown address
Crash Address: 
Crash State:
  v8::internal::TracedHandlesImpl::Create
  v8::internal::GlobalizeTracedReference
  void blink::ScriptPromiseResolver::ResolveOrReject<v8::Local<v8::Value>>
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1096338:1096365

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=4511251945422848

Issue filed automatically.

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


## Timeline

### cl...@chromium.org (2023-01-31)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-01-31)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Blink>JavaScript>API Blink>JavaScript>GarbageCollection]

### cl...@chromium.org (2023-01-31)

Automatically adding ccs based on suspected regression changelists:

view-transitions: Flip status to stable. by khushalsagar@chromium.org - https://chromium.googlesource.com/chromium/src/+/c03f83e180726ba898a2191f616aa7df9c581510

Enabling CSS Color 4 on Stable by aaronhk@chromium.org - https://chromium.googlesource.com/chromium/src/+/01e5a054351e7c9c6df05cdb0cdf5241f088e449

If this is incorrect, please let us know why and apply the Test-Predator-Wrong-CLs label.

### [Deleted User] (2023-01-31)

[Empty comment from Monorail migration]

### ml...@chromium.org (2023-01-31)

Looks like a GC problem here, investigating.

### ml...@chromium.org (2023-01-31)

This is related to 
  Enabling CSS Color 4 on Stable by aaronhk@chromium.org - https://chromium.googlesource.com/chromium/src/+/01e5a054351e7c9c6df05cdb0cdf5241f088e449

ViewTransition defines:
```
 using PromiseProperty =
      ScriptPromiseProperty<ToV8UndefinedGenerator, v8::Local<v8::Value>>;
```

This is creating a garbarage collected object (ScriptPromiseProperty) that contains a v8::Local which is stack scoped [1]. The result is a memory corruption in the GCed object as it points to V8 data structures that are stack-scoped. This corruption can lead to crashes (best case) and UAF (worst case).

Most other use cases of ScriptPromiseProperty point to DOMException, or e.g. ScriptState which are both supported. Can this be used here as well?

Is this already shipped somehwere?

[1] https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/view_transition/view_transition.h;l=203?q=view_transition.h&ss=chromium

[Monorail components: Blink>ViewTransitions]

### aa...@chromium.org (2023-01-31)

 mlippautz@, how do you know this is related to my CL? CSS Color does not touch anything related to view transitions whereas the other CL identified by clusterfuzz does:

https://chromium-review.googlesource.com/c/chromium/src/+/4181494



### ml...@chromium.org (2023-01-31)

Oh, I am so sorry. I screwed this up when writing the message and copying the CL ids. It's indeed related to view-transitions. Reassigning.

### [Deleted User] (2023-01-31)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-01-31)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ml...@chromium.org (2023-02-03)

Any update here? This can cause crashes in the GC that are impossible to diagnose from Chrome crashes as they will not be attributed back to view transitions.

### kh...@chromium.org (2023-02-03)

Sorry I was OOO until today. Looking now.

### kh...@chromium.org (2023-02-03)

https://chromium-review.googlesource.com/c/chromium/src/+/4219327 has the fix. I confirmed by running the test case locally.

### gi...@appspot.gserviceaccount.com (2023-02-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/86cac84ce6ce529764310ff6edf4feddc32315bc

commit 86cac84ce6ce529764310ff6edf4feddc32315bc
Author: Khushal Sagar <khushalsagar@chromium.org>
Date: Fri Feb 03 21:28:01 2023

view-transition: Use ScriptValue instead of v8::Local in promises.

ScriptPromiseProperty caches the value used when rejecting a promise.
Use ScriptValue here instead of v8::Local since the latter is stack
scoped.

R=bokan@chromium.org, vmpstr@chromium.org

Fixed: 1411558
Change-Id: Iaa10712c064a4291187bfb18325d523caeb43150
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4219327
Reviewed-by: David Bokan <bokan@chromium.org>
Commit-Queue: David Bokan <bokan@chromium.org>
Reviewed-by: Vladimir Levin <vmpstr@chromium.org>
Auto-Submit: Khushal Sagar <khushalsagar@chromium.org>
Commit-Queue: Khushal Sagar <khushalsagar@chromium.org>
Commit-Queue: Vladimir Levin <vmpstr@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1101196}

[modify] https://crrev.com/86cac84ce6ce529764310ff6edf4feddc32315bc/third_party/blink/renderer/core/view_transition/view_transition.h
[modify] https://crrev.com/86cac84ce6ce529764310ff6edf4feddc32315bc/third_party/blink/renderer/core/view_transition/view_transition.cc


### kh...@chromium.org (2023-02-03)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-04)

[Empty comment from Monorail migration]

### kh...@chromium.org (2023-02-04)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-04)

Merge approved: your change passed merge requirements and is auto-approved for M111. Please go ahead and merge the CL to branch 5563 (refs/branch-heads/5563) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: harrysouders (Android), harrysouders (iOS), dgagnon (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cl...@chromium.org (2023-02-04)

ClusterFuzz testcase 4511251945422848 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1101194:1101198

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### pb...@google.com (2023-02-06)

[Bulk Edit] This merge has been approved for M111, please help complete your merges asap (before 3pm PST) today, so the change can be included in this week's RC build for dev/beta releases.`

We would like to get the changes as much Dev/beta time as possible, so please complete your merges asap to M111 branch(go/chrome-branches).

### gi...@appspot.gserviceaccount.com (2023-02-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/343d97dd473f2ff8ce4e95cb4aa73a497c30406f

commit 343d97dd473f2ff8ce4e95cb4aa73a497c30406f
Author: Khushal Sagar <khushalsagar@chromium.org>
Date: Tue Feb 07 00:04:38 2023

view-transition: Use ScriptValue instead of v8::Local in promises.

ScriptPromiseProperty caches the value used when rejecting a promise.
Use ScriptValue here instead of v8::Local since the latter is stack
scoped.

R=​bokan@chromium.org, vmpstr@chromium.org

(cherry picked from commit 86cac84ce6ce529764310ff6edf4feddc32315bc)

Fixed: 1411558
Change-Id: Iaa10712c064a4291187bfb18325d523caeb43150
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4219327
Reviewed-by: David Bokan <bokan@chromium.org>
Commit-Queue: David Bokan <bokan@chromium.org>
Reviewed-by: Vladimir Levin <vmpstr@chromium.org>
Auto-Submit: Khushal Sagar <khushalsagar@chromium.org>
Commit-Queue: Khushal Sagar <khushalsagar@chromium.org>
Commit-Queue: Vladimir Levin <vmpstr@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1101196}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4225895
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/5563@{#223}
Cr-Branched-From: 3ac59a6729cdb287a7ee629a0004c907ec1b06dc-refs/heads/main@{#1097615}

[modify] https://crrev.com/343d97dd473f2ff8ce4e95cb4aa73a497c30406f/third_party/blink/renderer/core/view_transition/view_transition.h
[modify] https://crrev.com/343d97dd473f2ff8ce4e95cb4aa73a497c30406f/third_party/blink/renderer/core/view_transition/view_transition.cc


### am...@google.com (2023-02-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-02-10)

Congratulations! The VRP Panel has decided to award you $7,000 for this report + $2,000 fuzzer bonus. Thank you for your efforts toward fuzzing Chrome -- great work! 

### am...@chromium.org (2023-02-10)

[Empty comment from Monorail migration]

### am...@google.com (2023-02-10)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-13)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1411558?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>JavaScript>API, Blink>JavaScript>GarbageCollection, Blink>ViewTransitions]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062839)*
