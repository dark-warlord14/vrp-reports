# Security: UAF with Blob creation and Shared Workers

| Field | Value |
|-------|-------|
| **Issue ID** | [40080169](https://issues.chromium.org/issues/40080169) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Workers |
| **Reporter** | th...@gmail.com |
| **Assignee** | tz...@chromium.org |
| **Created** | 2014-08-06 |
| **Bounty** | $1,500.00 |

## Description

**VULNERABILITY DETAILS**  

An UAF (or a Segv) happens when a new window is opened and closed (automatically) from an onmessage event triggered by a shared worker with a Blob creation loop.

**VERSION**  

Chrome Version: 36.0.1985.125 stable up to ToT 287661 (Asan)  

Operating System: Ubuntu x64, Windows x86

**REPRODUCTION CASE**

1. Launch the added repro file
2. Click "Start" (link)

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State: see added stack trace (287661)

## Attachments

- [blob_sharedworker_asan_trace.txt](attachments/blob_sharedworker_asan_trace.txt) (text/plain, 13.0 KB)
- [blob_sharedworker_repro.html](attachments/blob_sharedworker_repro.html) (text/html, 545 B)
- [blob_sharedworker_repro2b.html](attachments/blob_sharedworker_repro2b.html) (text/html, 539 B)
- [blob_sharedworkers_36_0_1985_125_stable_asan_trace.txt](attachments/blob_sharedworkers_36_0_1985_125_stable_asan_trace.txt) (text/plain, 9.1 KB)
- [288859_asan_trace.txt](attachments/288859_asan_trace.txt) (text/plain, 13.0 KB)

## Timeline

### in...@chromium.org (2014-08-06)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-08-06)

ClusterFuzz is analyzing your testcase. See https://cluster-fuzz.appspot.com/testcase?key=5634867452706816

### in...@chromium.org (2014-08-07)

Therealholden@, can you please remove the clicking the start link dependency. We usually feed all our testcases to CF to avoid manual triage.

### th...@gmail.com (2014-08-07)

I can't, because it is an essential part of the UAF. The script needs an isolated process created by a new tab (combined with noreferrer) which can only be opened by user input (link, or button?). 

Frames run within the process of the current window (although 330264 probably changes this) and separate (process) windows cannot be closed anymore from script.

The only user input required is clicking a link (or a button which I've used before). I've added a button and improved the script slightly. It may need a few runs before the UAF occurs because the Segv seems to occur more frequently than the UAF.



### in...@chromium.org (2014-08-07)

Nasko, could this be coming from your workers refactoring ? Can you please take a look or help with an owner ?

### na...@chromium.org (2014-08-07)

The createThread is the old codepath, so I doubt the refactoring is at fault. Also the report mentions stable (m36), which also doesn't have the new code.
I can try to take a look once I'm back in the office Aug 11th, but in the meantime someone else familiar with workers can investigate.

### in...@chromium.org (2014-08-07)

Haraken@, can you please take a look.

### me...@chromium.org (2014-08-07)

[Empty comment from Monorail migration]

### ha...@chromium.org (2014-08-08)

I cannot reproduce the crash, but uploaded a speculative fix here: https://codereview.chromium.org/455613003/


### ha...@chromium.org (2014-08-08)

(Feel free to take this bug; I'm not familiar with the code around this.)


### ha...@chromium.org (2014-08-08)

I won't have time to look at this until Monday, so let me assign this to nasko@.


### cl...@chromium.org (2014-08-09)

[Empty comment from Monorail migration]

### na...@chromium.org (2014-08-11)

Looking at the stack traces further, it is UaF because the main thread has exited, while the worker thread is still running. This is solved with my work on moving workers to use WebThread and the issue doesn't repro on a build with those changes.

I'm not sure this is easily fixable in the older codebase using the WTF threads. At least not in any clean way, as it uses global objects torn down when the main thread exits.

Jochen, does V8 have a way of checking if platform is initialized or torn down?

### th...@gmail.com (2014-08-12)

I can still repro this with 288859. The stack trace is the same as the one from #0 (287661), but differs from the #4 trace (stable).

### cl...@chromium.org (2014-08-18)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-08-19)

nasko@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### na...@chromium.org (2014-08-19)

Assigning to tzik@, who is working on a CL to ensure all workers are stopped before exiting the main thread.

### cl...@chromium.org (2014-08-26)

tzik@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### wf...@chromium.org (2014-09-02)

tzik@ any update on this High severity UAF?

### cl...@chromium.org (2014-09-03)

tzik@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### tz...@chromium.org (2014-09-03)

[Empty comment from Monorail migration]

### tz...@chromium.org (2014-09-08)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-09-08)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### ti...@chromium.org (2014-09-23)

tzik@ - was this addressed in http://src.chromium.org/viewvc/blink?view=revision&revision=181309?

If so, I assume that we would want to merge this to M38 beta this week to address this bug. Is my understanding correct?

### in...@chromium.org (2014-09-24)

[Empty comment from Monorail migration]

### [Deleted User] (2014-09-24)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-09-24)

tzik@ - please merge to M38 / branch 2125

### tz...@chromium.org (2014-09-25)

#24
Yes, it does.

Merging r181309 to 2125.

### ma...@google.com (2014-09-26)

Please process the merge approval if you haven't.

### tz...@chromium.org (2014-09-27)

Oops. Sorry, this issue is not automatically updated, since the original commit wasn't associated to this.
Updating the issue manually from http://crbug.com/374201#29

----------

#29 bugdroid1@chromium.org
The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=182647

------------------------------------------------------------------
r182647 | tzik@chromium.org | 2014-09-25T03:42:02.469885Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/branches/chromium/2125/Source/core/workers/WorkerThread.h?r1=182647&r2=182646&pathrev=182647
   M http://src.chromium.org/viewvc/blink/branches/chromium/2125/Source/core/Init.cpp?r1=182647&r2=182646&pathrev=182647
   M http://src.chromium.org/viewvc/blink/branches/chromium/2125/Source/core/workers/WorkerThread.cpp?r1=182647&r2=182646&pathrev=182647

Merge 181309 "[Worker] Stop all workers in Blink shutdown sequence"

> [Worker] Stop all workers in Blink shutdown sequence
> 
> Ensure all workers not to outlive the main thread.
> 
> BUG=374201,399803
> 
> Review URL: https://codereview.chromium.org/292173002

TBR=tzik@chromium.org

Review URL: https://codereview.chromium.org/604643002
-----------------------------------------------------------------

### ti...@chromium.org (2014-10-03)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-10-07)

Congrats Collin - $1000 for this report under our new reward structure plus an additional $500 fuzzer bonus for running this fuzzer on ClusterFuzz.

### ti...@google.com (2014-12-08)

Payment in progress

### ti...@google.com (2014-12-09)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-12-15)

Bulk update: removing view restriction from closed bugs.

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

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/401115?no_tracker_redirect=1

[Monorail blocked-on: crbug.com/chromium/405420]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080169)*
