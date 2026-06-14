# Heap-use-after-free in blink::WorkerSharedTimer::OnTimeout

| Field | Value |
|-------|-------|
| **Issue ID** | [40080141](https://issues.chromium.org/issues/40080141) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Workers |
| **Reporter** | cl...@chromium.org |
| **Assignee** | na...@chromium.org |
| **Created** | 2014-08-01 |
| **Bounty** | $3,000.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5123080332509184

Fuzzer: Therealholden_worker
Job Type: Windows_asan_chrome

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x0e95b128
Crash State:
  - crash stack -
  blink::WorkerSharedTimer::OnTimeout
  blink::GeolocationClientProxy::startUpdating
  - free stack -
  blink::WorkerThreadShutdownStartTask::`scalar
  blink::WorkerThread::~WorkerThread
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=windows_asan_chrome&range=286338:286568

Minimized Testcase (1.17 Kb): https://cluster-fuzz.appspot.com/download/AMIfv97LL94o8ag-VtsuZ15pt6_-lOLMfNuUKlMmyD_FLB4s86Ujk3iO6GHHIylYNcbsHDOy5iktMbCfnz4K_TULU7uFlEIO3GyJPwwNp7CCOWs9jjue5zEyuRYzxU8_-J6L5i4GsgrHDMgrrqKLBqwmlsGibMWPJw

Filer: inferno

## Timeline

### in...@chromium.org (2014-08-01)

could this be regression from http://src.chromium.org/viewvc/blink?view=rev&revision=179155

### jo...@chromium.org (2014-08-01)

looks like the shutdown start tasks nulls the shared timer, and some later access doesn't null check it?

### in...@chromium.org (2014-08-02)

New testcase coming, definitely regression from http://src.chromium.org/viewvc/blink?view=rev&revision=179309. Nasko, can you please help to fix.

### cl...@chromium.org (2014-08-02)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6527517861085184

Fuzzer: Therealholden_worker
Job Type: Mac_asan_chrome

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x44061128
Crash State:
  - crash stack -
  blink::WorkerSharedTimer::OnTimeout
  blink::Task::run
  - free stack -
  blink::WorkerThread::~WorkerThread
  blink::DedicatedWorkerThread::~DedicatedWorkerThread
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=mac_asan_chrome&range=287002:287043

Minimized Testcase (1.03 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96JQeUkVzdBxTUc0eCZuN7CUIT0W7cmv1ihg9LXRn7vfLf59CSF7Xwm-isg0AjNSitWj0qEBpBH-ztTg1xPnCCbFnxXTivhL5o-RissYGjj3sf3H-l3UVfttgy4rBcnE4KXDmeoPpCzfqyvtFtsL0cn5J6Zow

Filer: inferno

### na...@chromium.org (2014-08-02)

There have been followup fixes going in. Let's see what happens after clusterfuzz tries these. I know I fixed the first test case and have tested it. The second one seems very much similar, so I expect it to be fixed too.

### in...@chromium.org (2014-08-02)

Thanks! I will close bug as soon as CF responds with a fixed message.

### bu...@chromium.org (2014-08-03)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=179453

------------------------------------------------------------------
r179453 | nasko@chromium.org | 2014-08-03T10:52:55.880085Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/workers/WorkerThread.cpp?r1=179453&r2=179452&pathrev=179453
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/workers/WorkerThread.h?r1=179453&r2=179452&pathrev=179453

Use WorkerThreadTask for timer and idle notification in WorkerThread.

The shared timer and idle notification tasks don't need to execute once the stop() method has been called. This change ensures that by wrapping them up in WorkerThreadTask.
Also, the WorkerThreadTask::run method wasn't checking for valid WorkerGlobalScope. It is possible for a task to be posted to the message loop after the cleanup is posted, which results in a crash.

BUG=301515,399495

Review URL: https://codereview.chromium.org/430813007
-----------------------------------------------------------------

### cl...@chromium.org (2014-08-03)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-08-03)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-08-03)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-08-03)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-08-03)

This medium+ severity security issue is a regression on trunk.

Please fix this asap. If you are unable to look into this soon, please revert your change.

- Your friendly ClusterFuzz

### na...@chromium.org (2014-08-04)

This should be fixed after blink r179453.

### in...@chromium.org (2014-08-04)

Marking as fixed for now. will reopen if i see it still crashing on CF.

### cl...@chromium.org (2014-08-07)

ClusterFuzz has detected this issue as fixed in range 287200:287259.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6527517861085184

Fuzzer: Therealholden_worker
Job Type: Mac_asan_chrome

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x44061128
Crash State:
  - crash stack -
  blink::WorkerSharedTimer::OnTimeout
  blink::Task::run
  - free stack -
  blink::WorkerThread::~WorkerThread
  blink::DedicatedWorkerThread::~DedicatedWorkerThread
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=mac_asan_chrome&range=287002:287043
Fixed: https://cluster-fuzz.appspot.com/revisions?job=mac_asan_chrome&range=287200:287259

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv96JQeUkVzdBxTUc0eCZuN7CUIT0W7cmv1ihg9LXRn7vfLf59CSF7Xwm-isg0AjNSitWj0qEBpBH-ztTg1xPnCCbFnxXTivhL5o-RissYGjj3sf3H-l3UVfttgy4rBcnE4KXDmeoPpCzfqyvtFtsL0cn5J6Zow

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### cl...@chromium.org (2014-08-09)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-10-07)

$3500 for this report ($3000 for the bug, $500 for ClusterFuzz). 

### cl...@chromium.org (2014-11-10)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2014-12-08)

Payment in progress

### ti...@google.com (2014-12-09)

[Empty comment from Monorail migration]

### ti...@google.com (2014-12-22)

Processing via our e-payment system can take up to six weeks, but the reward should be on its way to you. Thanks again for your help!

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/399495?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080141)*
