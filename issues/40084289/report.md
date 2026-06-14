# Heap-use-after-free in v8::Isolate::VisitHandlesWithClassIds

| Field | Value |
|-------|-------|
| **Issue ID** | [40084289](https://issues.chromium.org/issues/40084289) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Platforms** | Windows |
| **Reporter** | th...@gmail.com |
| **Assignee** | ha...@chromium.org |
| **Created** | 2016-05-11 |
| **Bounty** | $3,500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4623653819383808

Fuzzer: therealholden_worker
Job Type: windows_asan_content_shell
Platform Id: windows

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x1c80b204
Crash State:
  v8::Isolate::VisitHandlesWithClassIds
  blink::V8GCController::traceDOMWrappers
  blink::ThreadState::visitPersistents
  
Recommended Security Severity: High

Regressed: https://cluster-fuzz.appspot.com/revisions?job=windows_asan_content_shell&range=390670:390734

Unminimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv97Aw1lfci1FFnutmP8We0DwPKeAH6CUywwsPVqDzaBMBYAncywkN3ZgLilwvDGCuBIguRNDEOdHH42SxItWm52-vyxTPbBfRI3rFVKBdK6T_FaNYvtPtH6wCh3Xigr00_DggzTRq4SBgu1xytZ2ILDNMyArtQ


Additional requirements: Requires HTTP

Filer: mmoroz

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

## Timeline

### mm...@chromium.org (2016-05-11)

Looks a bit similar to https://crbug.com/chromium/610340, but not sure.

### jo...@chromium.org (2016-05-11)

worker thread executing stuff after blink's main thread was shut down.

kinuko because worker

assigning to haraken as he recently changed handling of shutdown

### ha...@chromium.org (2016-05-11)

This is a bug of Oilpan.

1) The main thread calls blink::shutdown().
2) The main thread destroys the V8 isolate.
3) Worker threads are still running and can trigger Oilpan's GC (<== this causes the crash).
4) The main thread calls modulesInitializer().shutdown() and joins all workers.

A right fix would be to move 4) to between 1) and 2).


### [Deleted User] (2016-05-11)

Overlap with https://crbug.com/chromium/459380 and/or https://crbug.com/chromium/610340 ?

### ha...@chromium.org (2016-05-11)

I don't think so, since both https://crbug.com/chromium/459380 and https://crbug.com/chromium/610340 are happening during V8 GC, not Oilpan's GC.


### cl...@chromium.org (2016-05-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-05-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-05-11)

This issue is a security regression. If you are not able to fix this quickly, please revert the change that introduced it.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chromium.org (2016-05-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/3c35abf17d76b2e4fe491a703b68b17c48725eeb

commit 3c35abf17d76b2e4fe491a703b68b17c48725eeb
Author: haraken <haraken@chromium.org>
Date: Wed May 11 14:06:54 2016

All worker threads should be joined before main thread's V8 isolate is destroyed

Currently the following scenario can happen:

1) The main thread calls blink::shutdown().
2) The main thread calls V8Initializer::shutdown(), which destroys the V8 isolate.
3) Worker threads are still running and can trigger Oilpan's GC (<== this accesses the isolate and causes crash).
4) The main thread calls modulesInitializer().shutdown() and joins all workers.

To address the issue, this CL moves 4) to between 1) and 2).

BUG=610987

Review-Url: https://codereview.chromium.org/1969673004
Cr-Commit-Position: refs/heads/master@{#392913}

[modify] https://crrev.com/3c35abf17d76b2e4fe491a703b68b17c48725eeb/third_party/WebKit/Source/web/WebKit.cpp


### ha...@chromium.org (2016-05-11)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-05-12)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-05-12)

[Empty comment from Monorail migration]

### oc...@chromium.org (2016-05-13)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-06-09)

ClusterFuzz has detected this testcase as flaky and is unable to reproduce it in the original crash revision. Skipping fixed testing check and marking it as potentially fixed.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4623653819383808

Fuzzer: therealholden_worker
Job Type: windows_asan_content_shell
Platform Id: windows

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x1c80b204
Crash State:
  v8::Isolate::VisitHandlesWithClassIds
  blink::V8GCController::traceDOMWrappers
  blink::ThreadState::visitPersistents
  
Recommended Security Severity: High

Regressed: https://cluster-fuzz.appspot.com/revisions?job=windows_asan_content_shell&range=390670:390734

Unminimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv97Aw1lfci1FFnutmP8We0DwPKeAH6CUywwsPVqDzaBMBYAncywkN3ZgLilwvDGCuBIguRNDEOdHH42SxItWm52-vyxTPbBfRI3rFVKBdK6T_FaNYvtPtH6wCh3Xigr00_DggzTRq4SBgu1xytZ2ILDNMyArtQ


Additional requirements: Requires HTTP

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### aw...@chromium.org (2016-07-20)

Congratulations - $3,500 for this bug!

### aw...@chromium.org (2016-08-04)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-08-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-08-18)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/610987?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084289)*
