# Use-After-Free in Inspector Heap Profiler

| Field | Value |
|-------|-------|
| **Issue ID** | [483853098](https://issues.chromium.org/issues/483853098) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Platform>DevTools, Platform>DevTools>Memory |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ma...@gmail.com |
| **Assignee** | sz...@google.com |
| **Created** | 2026-02-12 |
| **Bounty** | Confirmed (amount unknown) |

## Description

---

## VULNERABILITY DETAILS

### Summary

A Use-After-Free (UAF) vulnerability exists in `V8HeapProfilerAgentImpl::stopTrackingHeapObjects` within the V8 inspector. The function synchronously calls `takeHeapSnapshotNow`, which can trigger a callback to the frontend (e.g., DevTools or d8) via `HeapSnapshotProgress::ReportProgressValue`. If this callback destroys the inspector session, the `V8HeapProfilerAgentImpl` object is freed, but the ongoing `TakeHeapSnapshot` operation continues to access its member `m_frontend`, leading to a UAF.

### Detail

The vulnerability is located in `src/inspector/v8-heap-profiler-agent-impl.cc`. When `stopTrackingHeapObjects` is called with `reportProgress: true`, it creates a `HeapSnapshotProgress` object that holds a raw pointer to `m_frontend`:

```
// src/inspector/v8-heap-profiler-agent-impl.cc

Response V8HeapProfilerAgentImpl::takeHeapSnapshotNow(...) {
  // ...
  std::unique_ptr<HeapSnapshotProgress> progress;
  if (protocolOptions.m_reportProgress)
    progress.reset(new HeapSnapshotProgress(&m_frontend)); // Raw pointer stored

  // ...
  options.control = progress.get();
  // ...
  const v8::HeapSnapshot* snapshot = profiler->TakeHeapSnapshot(options);
  // ...
}

```

The `HeapSnapshotProgress::ReportProgressValue` method uses this pointer:

```
  ControlOption ReportProgressValue(uint32_t done, uint32_t total) override {
    m_frontend->reportHeapSnapshotProgress(done, total, std::nullopt);
    // ...
    m_frontend->flush(); // Triggers callback to frontend
    return kContinue;
  }

```

V8's `TakeHeapSnapshot` periodically calls `ReportProgressValue`. The `flush()` call sends a message to the frontend. In `d8` (and Chrome), this can result in the synchronous execution of a JavaScript callback (e.g., `receive` in d8).

If the attacker controls this callback (or if a malicious page triggers a navigation/close during the snapshot), they can destroy the inspector session. This destroys `V8HeapProfilerAgentImpl` and `m_frontend`. However, the stack is still inside `TakeHeapSnapshot`. When the callback returns, execution continues, and subsequent accesses to `m_frontend` (e.g., in `ReportProgressValue` or later in `takeHeapSnapshotNow` via `HeapSnapshotOutputStream`) cause a Use-After-Free.

## VERSION

Chrome Version: `14.5.201.7`
V8 Commit: `fffd2bdc35a900b4312833885d9d30803580670e`

## REPRODUCTION CASE

1. Create `reproduction_uaf.js`:

```
var count = 0;
function receive(msg) {
    try {
        var m = JSON.parse(msg);
        if (m.method === "HeapProfiler.reportHeapSnapshotProgress") {
            count++;
            print("[+] Intercepted HeapProfiler.reportHeapSnapshotProgress (count: " + count + ")");
            if (count === 1) {
                print("[+] Executing arbitrary JS inside snapshot generation.");
                // In an exploit scenario, the inspector session would be destroyed here.
            }
        }
    } catch(e) {}
}
var msg_id = 1;
function send_msg(method, params) {
    var msg = JSON.stringify({id: msg_id++, method: method, params: params});
    send(msg);
}
print("[*] Enabling HeapProfiler...");
send_msg("HeapProfiler.enable");
send_msg("HeapProfiler.startTrackingHeapObjects");
print("[*] Triggering vulnerable path (stopTrackingHeapObjects with reportProgress)...");
send_msg("HeapProfiler.stopTrackingHeapObjects", {reportProgress: true});
print("[*] Done.");

```

2. Run with `d8` (Debug+ASAN build recommended to see the assertion failure confirming the synchronous callback in critical section):

```
./out/asan/d8 --enable-inspector reproduction_uaf.js

```
## CRASH LOG

```
[*] Enabling HeapProfiler...
[*] Triggering vulnerable path (stopTrackingHeapObjects with reportProgress)...


#
# Fatal error in ../../src/heap/heap-allocator-inl.h, line 79
# Debug check failed: AllowHeapAllocation::IsAllowed().
#
#
#
#FailureMessage Object: 0x706433175c60
==== C stack trace ===============================

    out/asan/d8(__interceptor_backtrace+0x46) [0x565818213066]
    /home/leo/v8/v8_src/v8/out/asan/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x34) [0x7464427aacd4]
    /home/leo/v8/v8_src/v8/out/asan/libv8_libplatform.so(+0x3336b) [0x74644270036b]
    /home/leo/v8/v8_src/v8/out/asan/libv8_libbase.so(V8_Fatal(char const*, int, char const*, ...)+0x2a0) [0x746442773b10]
    /home/leo/v8/v8_src/v8/out/asan/libv8_libbase.so(+0x5407f) [0x74644277307f]
    /home/leo/v8/v8_src/v8/out/asan/libv8.so(+0x4a36776) [0x74643b636776]
    /home/leo/v8/v8_src/v8/out/asan/libv8.so(v8::internal::Factory::AllocateRaw(int, v8::internal::AllocationType, v8::internal::AllocationAlignment, v8::internal::AllocationHint)+0x5a) [0x74643b5d300a]
...

```
## Bisect

The vulnerability was introduced in commit `211a6a86370e` which added the `reportProgress` logic and the `HeapSnapshotProgress` class with the raw pointer.

```
commit 211a6a86370e281045766299981881669466858e
Author: kozyatinskiy <kozyatinskiy@chromium.org>
Date:   Tue Nov 22 10:57:03 2016 -0800

    [inspector] report progress for heap snapshot
...

```
## CREDIT INFORMATION

Reporter credit: Zhenpeng (Leo) Lin at depthfirst

## Timeline

### za...@google.com (2026-02-12)

security shepherd: seems to be a UAF vulnerability in the V8 Inspector's `V8HeapProfilerAgentImpl`, affecting Chrome's Renderer process when DevTools is used. The bisect looks very convincing. Assigning this to v8 shepherd to take a look. Thanks.

### ch...@google.com (2026-02-12)

This V8 bug has been marked as either a release blocker or a vulnerability bug. V8 bugs affect all OSs supported by Chrome, so the OS field has been updated to reflect this. Please update the bug with the correct OS field if it only affects a subset of OSes.

### cl...@appspot.gserviceaccount.com (2026-02-12)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4752411209957376.

### 24...@project.gserviceaccount.com (2026-02-13)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the hotlistid:4801165.

### 24...@project.gserviceaccount.com (2026-02-13)

Detailed Report: https://clusterfuzz.com/testcase?key=4752411209957376

Fuzzer: None
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  AllowHeapAllocation::IsAllowed() in heap-allocator-inl.h
  v8::internal::AllocationResult v8::internal::HeapAllocator::AllocateRaw<
  v8::internal::Factory::AllocateRaw
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=79145:79486

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=4752411209957376

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary.

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### om...@chromium.org (2026-02-13)

Dominik, can you take a look?   

The report says UAF, but in practice what is an allocation when allocations are not allowed (`Debug check failed: AllowHeapAllocation::IsAllowed()`) and involving heap snapshots.

### 24...@project.gserviceaccount.com (2026-02-13)

Detailed Report: https://clusterfuzz.com/testcase?key=4752411209957376

Fuzzer: None
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  AllowHeapAllocation::IsAllowed() in heap-allocator-inl.h
  v8::internal::AllocationResult v8::internal::HeapAllocator::AllocateRaw<
  v8::internal::Factory::AllocateRaw
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=79145:79486

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=4752411209957376

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary.

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### ch...@google.com (2026-02-13)

Setting milestone because of s0/s1 severity.

### di...@chromium.org (2026-02-13)

It looks to me like this is more an issue in the inspector/DevTools than the GC.

### pe...@google.com (2026-02-13)

The issue's primary component must be in the Component Tags, so re-adding it. To change the primary component, use the edit button at the top of the issue, just above the title.

### di...@chromium.org (2026-02-13)

@sz...@chromium.org: Can you please assign the right person?

### sz...@google.com (2026-02-16)

This might actually be a "Use-after-free" but not with the repro that is provided. This is basically a duplicate of <https://crbug.com/40071155>, where we disconnect the V8 session while CDP commands are still running. In this case, the `d8` repro is not really valid/helpful as the V8 inspector implementation in `d8` is sufficiently different from blink that the repro doesn't transfer cleanly.

The actual "Use-after-free" on session disconnect happens in `DevToolsSession` of blink:

1. The V8 session is kept alive via `std::shared_ptr` as long as a CDP call is on the stack. That means as long as `TakeHeapSnapshot` is running, on the V8 side, everything is alive and well (session and agents).
2. The problem is the "Channel", which is the blink `DevToolsSession` passed to the V8 session via raw pointer. Now this is CPPGC reference but since `V8InspectorSessionImpl` is not a GC object, this reference is lost and the channel becomes a dangling pointer.
3. As the repro rightly points out, once the session disconnects during `TakeHeapSnapshot`, the `channel` reference may or may not become stale, depending on the GC timing.

To fix this, we need to extend the life-time of the blink `DevToolsSession` as long as the `V8InspectorSession` is alive.

### dx...@google.com (2026-02-17)

Project: v8/v8  

Branch:  main  

Author:  Simon Zünd [szuend@chromium.org](mailto:szuend@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7582274>

[inspector] Use V8InspectorImpl in search-util.(h|cc) directly

---


Expand for full commit details
```
     
    Bug: 483853098 
    Change-Id: I68ef4ac98b0c9049e1dcbf5583f505b4130a2141 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7582274 
    Commit-Queue: Eric Leese <leese@chromium.org> 
    Auto-Submit: Simon Zünd <szuend@chromium.org> 
    Reviewed-by: Eric Leese <leese@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#105291}

```

---

Files:

- M `src/inspector/search-util.cc`
- M `src/inspector/search-util.h`
- M `src/inspector/v8-debugger-agent-impl.cc`
- M `src/inspector/v8-inspector-session-impl.cc`

---

Hash: [7f76ad2f8489f88464b46015fe6307ae6c4442af](https://chromiumdash.appspot.com/commit/7f76ad2f8489f88464b46015fe6307ae6c4442af)  

Date: Tue Feb 17 05:07:25 2026


---

### dx...@google.com (2026-02-17)

Project: v8/v8  

Branch:  main  

Author:  Simon Zünd [szuend@chromium.org](mailto:szuend@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7583177>

[inspector] Add GC managed ManagedChannel

---


Expand for full commit details
```
     
    This CL adds a new cppgc::GarbageCollected ManagedChannel class. This 
    allows the V8 inspector to extend the life-time of the channel until the 
    V8InspectorSessionImpl is cleaned up. This is required since the blink 
    DevToolsSession can detach while a CDP call is still on the stack (via 
    nested run loop). 
     
    The V8InspectorSessionImpl uses the new ManagedChannel directly. For 
    existing connect* methods, we add an internal GC-managed wrapper object. 
     
    Bug: 483853098 
    Change-Id: I870fa9ecf983cb68ac33c300426f3d8da4768f11 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7583177 
    Reviewed-by: Philip Pfaffe <pfaffe@chromium.org> 
    Commit-Queue: Simon Zünd <szuend@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#105294}

```

---

Files:

- M `include/v8-inspector.h`
- M `src/inspector/v8-inspector-impl.cc`
- M `src/inspector/v8-inspector-impl.h`
- M `src/inspector/v8-inspector-session-impl.cc`
- M `src/inspector/v8-inspector-session-impl.h`

---

Hash: [7c5f35c5221fb4af94f7909dc0377f83632450dc](https://chromiumdash.appspot.com/commit/7c5f35c5221fb4af94f7909dc0377f83632450dc)  

Date: Tue Feb 17 09:30:45 2026


---

### dx...@google.com (2026-02-18)

Project: chromium/src  

Branch:  main  

Author:  Simon Zünd [szuend@chromium.org](mailto:szuend@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7585774>

[inspector] Pass ManagedChannel when connecting to V8

---


Expand for full commit details
```
     
    This CL makes DevToolsSession inherit from V8Inspector::ManagedChannel. 
    This allows the V8 inspector to extend the life-time as needed, should 
    there still be CDP commands in-flight when the session detaches. 
     
    Bug: 40071155 
    Fixed: 483853098 
    Change-Id: Ia6ecd31df995c358ea2fcc9f48f59cd3ee7ad4f3 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7585774 
    Reviewed-by: Alex Rudenko <alexrudenko@chromium.org> 
    Commit-Queue: Simon Zünd <szuend@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1586235}

```

---

Files:

- M `third_party/blink/renderer/core/inspector/devtools_session.cc`
- M `third_party/blink/renderer/core/inspector/devtools_session.h`

---

Hash: [7d8b22f0bcaa82823f31b8bd53e026a670c5a64f](https://chromiumdash.appspot.com/commit/7d8b22f0bcaa82823f31b8bd53e026a670c5a64f)  

Date: Wed Feb 18 07:08:16 2026


---

### ch...@google.com (2026-02-18)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### sz...@google.com (2026-02-18)

The CL <https://crrev.com/c/7585774> fixes the problem outlined in [comment #13](https://issues.chromium.org/issues/483853098#comment13). The DCHECK in the initial report is still happening, but that is not a vulnerability, but a misuse of our test harness.

Going forward, any report requiring `--enable-inspector` on `d8` will be treated as a bug report and not as a vulnerability. We appreciate the effort but we don't ship this configuration. If you find a vulnerability in the V8 inspector, it needs to reproduce in either `chrome` or `content_shell`.

I'll point out though that this report made me go back and look at [issue 40071155](https://issues.chromium.org/issues/40071155) again, which lead to the fix in <https://crrev.com/c/7585774>. So some attribution is warranted :)

### dx...@google.com (2026-02-18)

Project: v8/v8  

Branch:  main  

Author:  Simon Zünd [szuend@chromium.org](mailto:szuend@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7586558>

[d8] Add clarifying comment for --enable-inspector

---


Expand for full commit details
```
     
    Bug: 483853098 
    Change-Id: I504ffc893217094f1a6fbbbddbba1182b67c7df7 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7586558 
    Commit-Queue: Michael Lippautz <mlippautz@chromium.org> 
    Auto-Submit: Simon Zünd <szuend@chromium.org> 
    Reviewed-by: Michael Lippautz <mlippautz@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#105306}

```

---

Files:

- M `src/d8/d8.h`

---

Hash: [a82eceb9984ee40be9ea43bcd7d1424df4c226fb](https://chromiumdash.appspot.com/commit/a82eceb9984ee40be9ea43bcd7d1424df4c226fb)  

Date: Wed Feb 18 06:08:50 2026


---

### ch...@google.com (2026-02-18)

Security Merge Request Consideration: Requesting merge to extended stable (M144) because latest trunk commit (1586235) appears to be after extended stable branch point (1552494).
Security Merge Request Consideration: Requesting merge to stable (M145) because latest trunk commit (1586235) appears to be after stable branch point (1568190).
Security Merge Request Consideration: Requesting merge to beta (M146) because latest trunk commit (1586235) appears to be after beta branch point (1582197).
Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### dx...@google.com (2026-02-19)

Project: v8/v8  

Branch:  main  

Author:  Simon Zünd [szuend@chromium.org](mailto:szuend@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7587614>

[inspector] Split Channel hierarchy to prevent illegal downcast

---


Expand for full commit details
```
     
    Bug: 483853098 
    Change-Id: I588b836123aec1962ff53f7f871b6c8012c243bf 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7587614 
    Reviewed-by: Omer Katz <omerkatz@chromium.org> 
    Commit-Queue: Simon Zünd <szuend@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#105324}

```

---

Files:

- M `include/v8-inspector.h`

---

Hash: [89196c7f7ef80da5978ad2e160943416a6018fda](https://chromiumdash.appspot.com/commit/89196c7f7ef80da5978ad2e160943416a6018fda)  

Date: Thu Feb 19 05:19:41 2026


---

### ch...@google.com (2026-02-20)

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

### ch...@google.com (2026-02-20)

Merge review required: M145 is already shipping to stable.

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
Owners: andywu (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), harrysouders (Mobile US), eakpobaro (Mobile EMEA)

### ch...@google.com (2026-02-20)

Merge review required: M144 is already shipping to stable.

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
Owners: alonbajayo (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), govind (Mobile US), eakpobaro (Mobile EMEA)

### dr...@chromium.org (2026-02-21)

No crashes in Canary, merge approved to all three channels.

### go...@google.com (2026-02-24)

Please merge your change to M146 by 11:00 AM PT, Tuesday, Feb 24th so it gets picked up for M146 Early Stable release. Thank you.

### dx...@google.com (2026-02-24)

Project: v8/v8  

Branch:  refs/branch-heads/14.6  

Author:  Simon Zünd [szuend@chromium.org](mailto:szuend@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7595086>

Merged: [inspector] Use V8InspectorImpl in search-util.(h|cc) directly

---


Expand for full commit details
```
     
    Bug: 483853098 
    (cherry picked from commit 7f76ad2f8489f88464b46015fe6307ae6c4442af) 
     
    Change-Id: I01051c95c2a4a4a8404164dc631f05eb37855c11 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7595086 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Commit-Queue: Simon Zünd <szuend@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/14.6@{#9} 
    Cr-Branched-From: e04c3a1a2543bdbee7beac8846c9cbe8f657636f-refs/heads/14.6.202@{#1} 
    Cr-Branched-From: 3b0b01e6594ec362369dc16f069012a81748c8ba-refs/heads/main@{#105132}

```

---

Files:

- M `src/inspector/search-util.cc`
- M `src/inspector/search-util.h`
- M `src/inspector/v8-debugger-agent-impl.cc`
- M `src/inspector/v8-inspector-session-impl.cc`

---

Hash: [6d74d8f931b5bda46b539ac4b2ac929091a06655](https://chromiumdash.appspot.com/commit/6d74d8f931b5bda46b539ac4b2ac929091a06655)  

Date: Tue Feb 17 05:07:25 2026


---

### dx...@google.com (2026-02-24)

Project: v8/v8  

Branch:  refs/branch-heads/14.6  

Author:  Simon Zünd [szuend@chromium.org](mailto:szuend@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7600418>

Merged: [inspector] Add GC managed ManagedChannel

---


Expand for full commit details
```
     
    This CL adds a new cppgc::GarbageCollected ManagedChannel class. This 
    allows the V8 inspector to extend the life-time of the channel until the 
    V8InspectorSessionImpl is cleaned up. This is required since the blink 
    DevToolsSession can detach while a CDP call is still on the stack (via 
    nested run loop). 
     
    The V8InspectorSessionImpl uses the new ManagedChannel directly. For 
    existing connect* methods, we add an internal GC-managed wrapper object. 
     
    Bug: 483853098 
    (cherry picked from commit 7c5f35c5221fb4af94f7909dc0377f83632450dc) 
     
    Change-Id: Iab2f5e252156d6eb1aaedb393f55539a4131df13 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7600418 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Commit-Queue: Simon Zünd <szuend@chromium.org> 
    Auto-Submit: Simon Zünd <szuend@chromium.org> 
    Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Cr-Commit-Position: refs/branch-heads/14.6@{#11} 
    Cr-Branched-From: e04c3a1a2543bdbee7beac8846c9cbe8f657636f-refs/heads/14.6.202@{#1} 
    Cr-Branched-From: 3b0b01e6594ec362369dc16f069012a81748c8ba-refs/heads/main@{#105132}

```

---

Files:

- M `include/v8-inspector.h`
- M `src/inspector/v8-inspector-impl.cc`
- M `src/inspector/v8-inspector-impl.h`
- M `src/inspector/v8-inspector-session-impl.cc`
- M `src/inspector/v8-inspector-session-impl.h`

---

Hash: [78f84b8677d0e268d6d4444fb551655abba6a5db](https://chromiumdash.appspot.com/commit/78f84b8677d0e268d6d4444fb551655abba6a5db)  

Date: Tue Feb 17 09:30:45 2026


---

### dx...@google.com (2026-02-24)

Project: chromium/src  

Branch:  refs/branch-heads/7680  

Author:  Simon Zünd [szuend@chromium.org](mailto:szuend@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7602272>

[M146] [inspector] Pass ManagedChannel when connecting to V8

---


Expand for full commit details
```
     
    This CL makes DevToolsSession inherit from V8Inspector::ManagedChannel. 
    This allows the V8 inspector to extend the life-time as needed, should 
    there still be CDP commands in-flight when the session detaches. 
     
    Bug: 40071155 
    Fixed: 483853098 
     
    (cherry picked from commit 7d8b22f0bcaa82823f31b8bd53e026a670c5a64f) 
     
    Change-Id: I9bded1b9d0ea491f146d9f83045cd396540aff54 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7602272 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Auto-Submit: Simon Zünd <szuend@chromium.org> 
    Reviewed-by: Alex Rudenko <alexrudenko@chromium.org> 
    Commit-Queue: Alex Rudenko <alexrudenko@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7680@{#1207} 
    Cr-Branched-From: 76b7d80e5cda23fe6537eed26d68c92e995c7f39-refs/heads/main@{#1582197}

```

---

Files:

- M `third_party/blink/renderer/core/inspector/devtools_session.cc`
- M `third_party/blink/renderer/core/inspector/devtools_session.h`

---

Hash: [2ea2412f22e4864badb0ba6b1072cf12879cdc8c](https://chromiumdash.appspot.com/commit/2ea2412f22e4864badb0ba6b1072cf12879cdc8c)  

Date: Tue Feb 24 10:25:59 2026


---

### go...@google.com (2026-02-24)

[Bulk Edit]

Please merge your change to M146 by 12:30 PM PT, today, Feb 24th so it gets picked up for M146 Early Stable release tomorrow. Thank you.

### sr...@chromium.org (2026-02-24)

Pls complete the merges to 145 and 144 branches so this goes out next week to stable respin @sz...@chromium.org 

### pe...@google.com (2026-02-24)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### ch...@google.com (2026-02-25)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### dx...@google.com (2026-02-25)

Project: v8/v8  

Branch:  refs/branch-heads/14.4  

Author:  Simon Zünd [szuend@chromium.org](mailto:szuend@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7606139>

Merged: [inspector] Use V8InspectorImpl in search-util.(h|cc) directly

---


Expand for full commit details
```
     
    Bug: 483853098 
    (cherry picked from commit 7f76ad2f8489f88464b46015fe6307ae6c4442af) 
     
    Change-Id: I1ee1b2b06feb3530784e97010eca697b0628d087 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7606139 
    Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Auto-Submit: Simon Zünd <szuend@chromium.org> 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Cr-Commit-Position: refs/branch-heads/14.4@{#56} 
    Cr-Branched-From: 80acc26727d5a34e77dabeebe7c9213ec1bd4768-refs/heads/14.4.258@{#1} 
    Cr-Branched-From: ce7e597e90f6df3fa4b6df224bc613b80c635450-refs/heads/main@{#104020}

```

---

Files:

- M `src/inspector/search-util.cc`
- M `src/inspector/search-util.h`
- M `src/inspector/v8-debugger-agent-impl.cc`
- M `src/inspector/v8-inspector-session-impl.cc`

---

Hash: [f27fe50cbd34017bef9097b587a042044e4b912d](https://chromiumdash.appspot.com/commit/f27fe50cbd34017bef9097b587a042044e4b912d)  

Date: Tue Feb 17 05:07:25 2026


---

### dx...@google.com (2026-02-25)

Project: v8/v8  

Branch:  refs/branch-heads/14.5  

Author:  Simon Zünd [szuend@chromium.org](mailto:szuend@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7603477>

Merged: [inspector] Use V8InspectorImpl in search-util.(h|cc) directly

---


Expand for full commit details
```
     
    Bug: 483853098 
    (cherry picked from commit 7f76ad2f8489f88464b46015fe6307ae6c4442af) 
     
    Change-Id: I25218d51b6204b7436235084aaf25edda5984cc6 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7603477 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Auto-Submit: Simon Zünd <szuend@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/14.5@{#22} 
    Cr-Branched-From: f09d67c66114951c0ea3dc9d4b025461670a9557-refs/heads/14.5.201@{#2} 
    Cr-Branched-From: 3f006438f768659ed9776359a421dc432edce53f-refs/heads/main@{#104623}

```

---

Files:

- M `src/inspector/search-util.cc`
- M `src/inspector/search-util.h`
- M `src/inspector/v8-debugger-agent-impl.cc`
- M `src/inspector/v8-inspector-session-impl.cc`

---

Hash: [30d118749c5608d4bacb9131eac9e69ebd8f110f](https://chromiumdash.appspot.com/commit/30d118749c5608d4bacb9131eac9e69ebd8f110f)  

Date: Tue Feb 17 05:07:25 2026


---

### dx...@google.com (2026-02-25)

Project: v8/v8  

Branch:  refs/branch-heads/14.5  

Author:  Simon Zünd [szuend@chromium.org](mailto:szuend@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7606140>

Merged: [inspector] Add GC managed ManagedChannel

---


Expand for full commit details
```
     
    This CL adds a new cppgc::GarbageCollected ManagedChannel class. This 
    allows the V8 inspector to extend the life-time of the channel until the 
    V8InspectorSessionImpl is cleaned up. This is required since the blink 
    DevToolsSession can detach while a CDP call is still on the stack (via 
    nested run loop). 
     
    The V8InspectorSessionImpl uses the new ManagedChannel directly. For 
    existing connect* methods, we add an internal GC-managed wrapper object. 
     
    Bug: 483853098 
    (cherry picked from commit 7c5f35c5221fb4af94f7909dc0377f83632450dc) 
     
    Change-Id: Ic971494b5c5f80bfde489a2919d30d3b56cf041b 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7606140 
    Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Auto-Submit: Simon Zünd <szuend@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/14.5@{#24} 
    Cr-Branched-From: f09d67c66114951c0ea3dc9d4b025461670a9557-refs/heads/14.5.201@{#2} 
    Cr-Branched-From: 3f006438f768659ed9776359a421dc432edce53f-refs/heads/main@{#104623}

```

---

Files:

- M `include/v8-inspector.h`
- M `src/inspector/v8-inspector-impl.cc`
- M `src/inspector/v8-inspector-impl.h`
- M `src/inspector/v8-inspector-session-impl.cc`
- M `src/inspector/v8-inspector-session-impl.h`

---

Hash: [075b85f502f8946515b2857bae18eeec8afe4fbe](https://chromiumdash.appspot.com/commit/075b85f502f8946515b2857bae18eeec8afe4fbe)  

Date: Tue Feb 17 09:30:45 2026


---

### pe...@google.com (2026-02-25)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2026-02-25)

1. https://chromium-review.git.corp.google.com/c/v8/v8/+/7606179 and https://chromium-review.git.corp.google.com/c/v8/v8/+/7604235
2. Low - There was no conflict.
3. 144, 145, and 146
4. Yes, the issue was introduced by https://codereview.chromium.org/2523743003 many years ago. So M138 needs to have the fixes.


### dx...@google.com (2026-02-25)

Project: v8/v8  

Branch:  refs/branch-heads/14.4  

Author:  Simon Zünd [szuend@chromium.org](mailto:szuend@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7606219>

Merged: [inspector] Add GC managed ManagedChannel

---


Expand for full commit details
```
     
    This CL adds a new cppgc::GarbageCollected ManagedChannel class. This 
    allows the V8 inspector to extend the life-time of the channel until the 
    V8InspectorSessionImpl is cleaned up. This is required since the blink 
    DevToolsSession can detach while a CDP call is still on the stack (via 
    nested run loop). 
     
    The V8InspectorSessionImpl uses the new ManagedChannel directly. For 
    existing connect* methods, we add an internal GC-managed wrapper object. 
     
    Bug: 483853098 
    (cherry picked from commit 7c5f35c5221fb4af94f7909dc0377f83632450dc) 
     
    Change-Id: I05e54bf8cdb1a579193b21e52f889870673c2577 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7606219 
    Auto-Submit: Simon Zünd <szuend@chromium.org> 
    Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Cr-Commit-Position: refs/branch-heads/14.4@{#58} 
    Cr-Branched-From: 80acc26727d5a34e77dabeebe7c9213ec1bd4768-refs/heads/14.4.258@{#1} 
    Cr-Branched-From: ce7e597e90f6df3fa4b6df224bc613b80c635450-refs/heads/main@{#104020}

```

---

Files:

- M `include/v8-inspector.h`
- M `src/inspector/v8-inspector-impl.cc`
- M `src/inspector/v8-inspector-impl.h`
- M `src/inspector/v8-inspector-session-impl.cc`
- M `src/inspector/v8-inspector-session-impl.h`

---

Hash: [47f9535d4a8f36bc0becf2c34d797c763c478229](https://chromiumdash.appspot.com/commit/47f9535d4a8f36bc0becf2c34d797c763c478229)  

Date: Tue Feb 17 09:30:45 2026


---

### 24...@project.gserviceaccount.com (2026-02-25)

ClusterFuzz testcase 4752411209957376 is still reproducing on the latest available build  r105401.

Please re-test your fix against this testcase and if the fix was incorrect or incomplete, please re-open the bug. Otherwise, ignore this notification and add the hotlistid:5433040.

### dx...@google.com (2026-02-25)

Project: chromium/src  

Branch:  refs/branch-heads/7559  

Author:  Simon Zünd [szuend@chromium.org](mailto:szuend@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7606141>

[M144] [inspector] Pass ManagedChannel when connecting to V8

---


Expand for full commit details
```
     
    This CL makes DevToolsSession inherit from V8Inspector::ManagedChannel. 
    This allows the V8 inspector to extend the life-time as needed, should 
    there still be CDP commands in-flight when the session detaches. 
     
    Bug: 40071155 
    Fixed: 483853098 
    (cherry picked from commit 7d8b22f0bcaa82823f31b8bd53e026a670c5a64f) 
     
    Change-Id: If97b600d695e066aacd283d92c7dba7ba1e112c6 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7606141 
    Reviewed-by: Alex Rudenko <alexrudenko@chromium.org> 
    Auto-Submit: Simon Zünd <szuend@chromium.org> 
    Commit-Queue: Simon Zünd <szuend@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7559@{#4760} 
    Cr-Branched-From: 223dfbac1c7542a06b422390d954afe5b560b607-refs/heads/main@{#1552494}

```

---

Files:

- M `third_party/blink/renderer/core/inspector/devtools_session.cc`
- M `third_party/blink/renderer/core/inspector/devtools_session.h`

---

Hash: [523d8b83478e992b99dcbfdf347e06e4e7ac9371](https://chromiumdash.appspot.com/commit/523d8b83478e992b99dcbfdf347e06e4e7ac9371)  

Date: Wed Feb 25 09:54:12 2026


---

### dx...@google.com (2026-02-25)

Project: chromium/src  

Branch:  refs/branch-heads/7632  

Author:  Simon Zünd [szuend@chromium.org](mailto:szuend@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7604098>

[M145] [inspector] Pass ManagedChannel when connecting to V8

---


Expand for full commit details
```
     
    This CL makes DevToolsSession inherit from V8Inspector::ManagedChannel. 
    This allows the V8 inspector to extend the life-time as needed, should 
    there still be CDP commands in-flight when the session detaches. 
     
    Bug: 40071155 
    Fixed: 483853098 
    (cherry picked from commit 7d8b22f0bcaa82823f31b8bd53e026a670c5a64f) 
     
    Change-Id: I46d2dd9b825865f223c2e891f21805884a1e6559 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7604098 
    Commit-Queue: Simon Zünd <szuend@chromium.org> 
    Auto-Submit: Simon Zünd <szuend@chromium.org> 
    Reviewed-by: Alex Rudenko <alexrudenko@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7632@{#3355} 
    Cr-Branched-From: 0bbdf2913883391365383b0a5dfe7bf9fd1a5213-refs/heads/main@{#1568190}

```

---

Files:

- M `third_party/blink/renderer/core/inspector/devtools_session.cc`
- M `third_party/blink/renderer/core/inspector/devtools_session.h`

---

Hash: [a58cdac50a6fbaf631f03d0fc707339617c521a3](https://chromiumdash.appspot.com/commit/a58cdac50a6fbaf631f03d0fc707339617c521a3)  

Date: Wed Feb 25 10:02:09 2026


---

### dx...@google.com (2026-03-04)

Project: v8/v8  

Branch:  refs/branch-heads/13.8  

Author:  Simon Zünd [szuend@chromium.org](mailto:szuend@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7604235>

[M138-LTS][inspector] Use V8InspectorImpl in search-util.(h|cc) directly

---


Expand for full commit details
```
     
    (cherry picked from commit 7f76ad2f8489f88464b46015fe6307ae6c4442af) 
     
    Bug: 483853098 
    Change-Id: I68ef4ac98b0c9049e1dcbf5583f505b4130a2141 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7582274 
    Commit-Queue: Eric Leese <leese@chromium.org> 
    Auto-Submit: Simon Zünd <szuend@chromium.org> 
    Reviewed-by: Eric Leese <leese@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#105291} 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7604235 
    Commit-Queue: Gyuyoung Kim (xWF) <qkim@google.com> 
    Reviewed-by: Simon Zünd <szuend@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/13.8@{#96} 
    Cr-Branched-From: 61ddd471ece346840bbebbb308dceb4b4ce31b28-refs/heads/13.8.258@{#1} 
    Cr-Branched-From: fdb5de2c741658e94944f2ec1218530e98601c23-refs/heads/main@{#100480}

```

---

Files:

- M `src/inspector/search-util.cc`
- M `src/inspector/search-util.h`
- M `src/inspector/v8-debugger-agent-impl.cc`
- M `src/inspector/v8-inspector-session-impl.cc`

---

Hash: [082a248a66c9ad317055ac11891c39c0e4fe9a85](https://chromiumdash.appspot.com/commit/082a248a66c9ad317055ac11891c39c0e4fe9a85)  

Date: Tue Feb 17 05:07:25 2026


---

### aj...@google.com (2026-03-05)

switching to type=bug following comment 18

### sp...@google.com (2026-03-05)

*NOTE: This is an automatically generated email*

Hello,

Chrome Vulnerability Rewards Program (VRP) Panel has decided that the security impact of this
issue does not meet the criteria to qualify for a reward.

Rationale for this decision:

This has been determined not to be a vulnerability but rather a bug thus not eligible.

Note that the fact that this issue is not being rewarded does not mean
that the product team won't fix the issue. We have filed a bug with the product
team and they will review your report and decide if a fix is required. We'll
let you know if the issue was fixed.

Regards,   

Google Security Bot

*How did we do? Please fill out a [short anonymous survey](https://goo.gl/IR3KRH).*

### dx...@google.com (2026-03-10)

Project: v8/v8  

Branch:  refs/branch-heads/13.8  

Author:  Gyuyoung Kim [qkim@google.com](mailto:qkim@google.com)  

Link:    <https://chromium-review.googlesource.com/7606179>

[M138-LTS][inspector] Add GC managed ManagedChannel

---


Expand for full commit details
```
     
    This CL adds a new cppgc::GarbageCollected ManagedChannel class. This 
    allows the V8 inspector to extend the life-time of the channel until the 
    V8InspectorSessionImpl is cleaned up. This is required since the blink 
    DevToolsSession can detach while a CDP call is still on the stack (via 
    nested run loop). 
     
    The V8InspectorSessionImpl uses the new ManagedChannel directly. For 
    existing connect* methods, we add an internal GC-managed wrapper object. 
     
    (cherry picked from commit 7c5f35c5221fb4af94f7909dc0377f83632450dc) 
     
    Bug: 483853098 
    Change-Id: I870fa9ecf983cb68ac33c300426f3d8da4768f11 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7583177 
    Reviewed-by: Philip Pfaffe <pfaffe@chromium.org> 
    Commit-Queue: Simon Zünd <szuend@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#105294} 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7606179 
    Reviewed-by: Simon Zünd <szuend@chromium.org> 
    Commit-Queue: Gyuyoung Kim (xWF) <qkim@google.com> 
    Cr-Commit-Position: refs/branch-heads/13.8@{#100} 
    Cr-Branched-From: 61ddd471ece346840bbebbb308dceb4b4ce31b28-refs/heads/13.8.258@{#1} 
    Cr-Branched-From: fdb5de2c741658e94944f2ec1218530e98601c23-refs/heads/main@{#100480}

```

---

Files:

- M `DEPS`
- M `include/v8-inspector.h`
- M `src/inspector/v8-inspector-impl.cc`
- M `src/inspector/v8-inspector-impl.h`
- M `src/inspector/v8-inspector-session-impl.cc`
- M `src/inspector/v8-inspector-session-impl.h`

---

Hash: [e9bb0688e0420da2815312e76f7b1a607face365](https://chromiumdash.appspot.com/commit/e9bb0688e0420da2815312e76f7b1a607face365)  

Date: Thu Mar 5 02:41:16 2026


---

### qk...@google.com (2026-04-12)

Labeled `LTS-Merge-Merged-144` because the patch was already merged to M144.

### ch...@google.com (2026-05-28)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> This has been determined not to be a vulnerability but rather a bug thus not eligible.
> 
> 
> Note that the fact that this issue is not being rewarded does not mean
> that the product team won't fix the issue. We have filed a bug with the product
> team and they will review your report and decide if a fix is required. We'll
> let you know if the issue was fixed.
> 
> Regards, \
> Google Security Bot
> 
> *How did we do? Please fill out a [short anonymous survey](https://goo.gl/IR3KRH).*

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/483853098)*
