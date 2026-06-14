# Heap-use-after-free in v8::internal::MemoryReducer::TimerTask::Run

| Field | Value |
|-------|-------|
| **Issue ID** | [40082480](https://issues.chromium.org/issues/40082480) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript |
| **Reporter** | th...@gmail.com |
| **Assignee** | ul...@chromium.org |
| **Created** | 2015-07-12 |
| **Bounty** | $3,500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6545737242902528

Fuzzer: Therealholden_worker
Job Type: Windows_asan_chrome_no_sandbox

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x07ba48f0
Crash State:
  v8::internal::MemoryReducer::TimerTask::Run
  base::internal::Invoker<base::IndexSequence<0>,base::internal::BindState<base::i
  base::debug::TaskAnnotator::RunTask
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=windows_asan_chrome_no_sandbox&range=338438:338441

Minimized Testcase (3.61 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96BQjFT6yi1y4cReePdUbNcofRAhvSYzGi6aE8-WPEpARzuFR66gEbbPI_M94KlUEvPZ7ZJyG7cOcKapk3T_mAD-WgD3hF_8sOQF9wq3swswccjj0GPJ6Ahz5qfo3FHBwUU5lncAFrxZsYP04bIAGcF2kaM0Q

Additional requirements: Requires HTTP

Filer: inferno

## Timeline

### in...@chromium.org (2015-07-12)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-07-12)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-07-13)

This medium+ severity security issue is a regression on trunk.

Please fix this asap. If you are unable to look into this soon, please revert your change.

- Your friendly ClusterFuzz

### ul...@chromium.org (2015-07-13)

This should be fixed by https://codereview.chromium.org/1230163002


### jl...@chromium.org (2015-07-13)

[Empty comment from Monorail migration]

### jl...@chromium.org (2015-07-13)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-07-14)

ClusterFuzz has detected this issue as potentially fixed, but it appears to be flaky.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6545737242902528

Fuzzer: Therealholden_worker
Job Type: Windows_asan_chrome_no_sandbox

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x07ba48f0
Crash State:
  v8::internal::MemoryReducer::TimerTask::Run
  base::internal::Invoker<base::IndexSequence<0>,base::internal::BindState<base::i
  base::debug::TaskAnnotator::RunTask
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=windows_asan_chrome_no_sandbox&range=338438:338441

Minimized Testcase (3.61 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96BQjFT6yi1y4cReePdUbNcofRAhvSYzGi6aE8-WPEpARzuFR66gEbbPI_M94KlUEvPZ7ZJyG7cOcKapk3T_mAD-WgD3hF_8sOQF9wq3swswccjj0GPJ6Ahz5qfo3FHBwUU5lncAFrxZsYP04bIAGcF2kaM0Q

Additional requirements: Requires HTTP

If you suspect that the result above is incorrect,try re-doing that job on the test case report page.

### cl...@chromium.org (2015-07-27)

ulan@: Uh oh! This issue is still open and hasn't been updated in the last 14 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### ha...@chromium.org (2015-08-06)

Ulan, can you confirm that this is fixed?

### ul...@chromium.org (2015-08-06)

Fixed in https://codereview.chromium.org/1230163002

### cl...@chromium.org (2015-08-06)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-11-12)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2016-06-30)

We found some old non-stable release bugs that weren't voted on and took them to the reward panel last week. This was one of them.

$3,500 for this one ($3k for the bug, 500 Fuzzer bonus). Payment should arrive in 1-2 weeks. Apologies for the delay.

### aw...@chromium.org (2016-06-30)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-07-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/509458?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40082480)*
