# Security: set_state global_handles renderer crash (UAF) with Web Workers and Web SQL

| Field | Value |
|-------|-------|
| **Issue ID** | [40078653](https://issues.chromium.org/issues/40078653) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Storage |
| **Reporter** | th...@gmail.com |
| **Assignee** | jo...@chromium.org |
| **Created** | 2014-01-09 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

Chrome (renderer) crashes when a document is reloading (triggered by the worker) while the worker is using a Web SQL database at the same time.

**VERSION**  

Chrome Version: ToT 34.0.1777.0 (243865), ASAN/ToT 34.0.1777.0 (Developer Build 243816)  

Operating System: Ubuntu 13.10 x64

I can't repro this on v31.0.1650.63 (stable).

**REPRODUCTION CASE**  

Launch the added repro file

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: renderer, heap-use-after-free, read of size 1  

Crash State: see added ASAN trace

## Attachments

- [webworker_websql_crash_asan_trace.txt](attachments/webworker_websql_crash_asan_trace.txt) (text/plain, 11.4 KB)
- [webworker_websql_crash_repro.html](attachments/webworker_websql_crash_repro.html) (text/html, 1.2 KB)
- [chrome_beta_33_0_1750_58_asan_trace.txt](attachments/chrome_beta_33_0_1750_58_asan_trace.txt) (text/plain, 9.1 KB)

## Timeline

### cl...@chromium.org (2014-01-09)

ClusterFuzz is analyzing your testcase. See https://cluster-fuzz.appspot.com/testcase?key=5673893729665024

### jl...@chromium.org (2014-01-10)

Reproduced on tip of tree (r244031) with ASAN. I'm not sure why ClusterFuzz can't reproduce it yet.

adamk: could this be https://codereview.chromium.org/103473002 ? Would you mind taking a look or help find an Owner?

### cl...@chromium.org (2014-01-10)

ClusterFuzz is analyzing your testcase. See https://cluster-fuzz.appspot.com/testcase?key=6301855260868608

### ad...@chromium.org (2014-01-10)

It might be my change, but I wouldn't blame it just because OwnPtr is in the stack trace; previously it (probably) would've been deleted by RefPtr. But I'll see if I'll definitely take a look (likely tomorrow). CCing other WebSQL-aware folks.

### cl...@chromium.org (2014-01-10)

[Empty comment from Monorail migration]

### ad...@chromium.org (2014-01-10)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-01-13)

[Empty comment from Monorail migration]

### ad...@chromium.org (2014-01-13)

Still working on generating an ASAN build (got sidetracked Friday) but another thing that's new is the gin bindings layer.

### ad...@chromium.org (2014-01-13)

Okay, I can reproduce. Not gin-related, so removing Jochen.

And I don't think this is new: the old RefPtr-based code would have also crashed in this case. If I had to guess why it didn't crash before it's just because this is pretty racy: it only crashes if the Database cleanup tasks get posted after the worker thread has posted its own cleanup task.

There's already code that's supposed to keep this from happening in WorkerThreadShutdownStartTask::performTask (Source/core/workers/WorkerThread.cpp); will have to dig further to see that's not happening.

### ad...@chromium.org (2014-01-13)

+eseidel who, it appears, wrote this database synchronization code in the first place.

### th...@gmail.com (2014-01-13)

I cannot repro this with Chrome/Chromium beta either (v32.0.1700.72 (asan)).

Also, on Windows 8.1 (with ToT), the same sad tab/renderer crash (global-handles stack) seems to occur.

### th...@gmail.com (2014-01-14)

Further testing with ToT (continuous) on Ubuntu (x64) shows that it starts crashing @ 237763. 237762 does not crash.

### [Deleted User] (2014-01-14)

The ASAN stack trace make it look like a V8SQLCallback is firing after Worker thread shutdown.  Maybe workers fail to cancel all SQL callbacks during shutdown?

### ad...@chromium.org (2014-01-14)

With the revision range from #12, http://src.chromium.org/viewvc/blink?revision=162796&view=revision looks like the likely culprit (so re-adding jochen one more time). Here's the range: http://build.chromium.org/f/chromium/perf/dashboard/ui/changelog_blink.html?url=/trunk&range=162695:162816&mode=html

And yes, #13 is correct that for some reason the callbacks aren't being cancelled until after the WorkerThreadFinished task runs. I've got a plan to fix that today.

### jo...@chromium.org (2014-01-14)

we have tons of these bugs, and we know about them since quite a while.

The fix is to move worker thread from wtf threading to blink threading and shut it down correctly.

### mi...@chromium.org (2014-01-14)

re #13, it's not trying to invoke the V8SQLCallback, its trying to delete the callback... but it's doing so after v8 has been killed off.


### ad...@chromium.org (2014-01-14)

I now have a handle on what's happening. Check out this stack trace captured in SQLCallbackWrapper:

 [0x7fd81d94c6cc] WebCore::SQLCallbackWrapper<>::SafeReleaseTask::SafeReleaseTask()
 [0x7fd81d94c557] WebCore::SQLCallbackWrapper<>::SafeReleaseTask::create()
 [0x7fd81d94b3e2] WebCore::SQLCallbackWrapper<>::clear()
 [0x7fd81d94cbe9] WebCore::SQLCallbackWrapper<>::~SQLCallbackWrapper()
 [0x7fd81d94b909] WebCore::SQLTransaction::~SQLTransaction()
 [0x7fd81d94b989] WebCore::SQLTransaction::~SQLTransaction()
 [0x7fd81d94b9ec] WebCore::SQLTransaction::~SQLTransaction()
 [0x7fd81d9227e3] WTF::ThreadSafeRefCounted<>::deref()
 [0x7fd81d9271bd] WTF::derefIfNotNull<>()
 [0x7fd81d94f498] WTF::RefPtr<>::~RefPtr()
 [0x7fd81d94f510] WTF::RefPtr<>::operator=()
 [0x7fd81d94d1b3] WebCore::SQLTransactionBackend::doCleanup()
 [0x7fd81d94ebcc] WebCore::SQLTransactionBackend::notifyDatabaseThreadIsShuttingDown()
 [0x7fd81d936064] WebCore::DatabaseBackend::DatabaseTransactionTask::taskCancelled()
 [0x7fd81d935c01] WebCore::DatabaseTask::run()
 [0x7fd8209e19d2] base::internal::RunnableAdapter<>::Run()
 [0x7fd8209e193c] base::internal::InvokeHelper<>::MakeItSo()
 [0x7fd8209e18e5] base::internal::Invoker<>::Run()
 [0x7fd82193d1de] base::Callback<>::Run()
 [0x7fd8219fb013] base::MessageLoop::RunTask()

Note that this stack is the result of simply running the transaction task, rather than the cleanupDatabaseThread task. Before r162796, terminating the thread synchronously caused the DatabaseThread to stop processing tasks. But after that patch, tasks were still allowed to be queued (and run) until the cleanupDatabaseThread task ran.

### ad...@chromium.org (2014-01-14)

Assigning to Jochen, as it seems like the easiest fix is to revert r162796 (which fixes this problem for me locally). But that "fix" brings back various flakiness during thread shutdown, so I don't think it's necessarily what we want to do.

### cl...@chromium.org (2014-01-16)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-01-18)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-01-21)

[Empty comment from Monorail migration]

### me...@chromium.org (2014-01-21)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-01-22)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-01-22)

This medium+ severity security issue is a regression on trunk.

Please fix this asap. If you are unable to look into this soon, please revert your change.

- Your friendly ClusterFuzz

### me...@chromium.org (2014-01-22)

[Empty comment from Monorail migration]

### jo...@chromium.org (2014-01-27)

[Empty comment from Monorail migration]

### jo...@chromium.org (2014-01-27)

[Empty comment from Monorail migration]

### jo...@chromium.org (2014-01-28)

bumping to m35, refactoring the workerthread is making process, but it's going to take longer than m34

### th...@gmail.com (2014-02-11)

Starting with version 33.0.1750.29, the same crash/UAF also happens with Chrome beta (same trace).

### th...@gmail.com (2014-02-13)

#29 asan trace

### cl...@chromium.org (2014-02-17)

jochen@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### th...@gmail.com (2014-02-24)

This issue now impacts the stable version (starting @ 33.0.1750.117). The trace is the same as the one added to c#30.

However, on stable, the UAF seems to have been caused (started @ beta 33.0.1750.29) by a different cl than the 11185062 cl belonging to r162796 (no traces of it in the beta version ?). There are a lot of worker/database related changes in it though.

Also the UAF seems to have been hidden (or fixed?) on trunk starting @ version 249611. But again, there does not seem to be a specific fix mentioning this issue/cl.

### jo...@chromium.org (2014-02-24)

The UAF is there since forever :-(

It just gets more or less easy to trigger. The fix we're working on is to shut down the worker thread instead of detaching it and hoping it won't crash.

I have a number of separate bugs on file about fixing the worker thread.

### in...@chromium.org (2014-02-24)

[Empty comment from Monorail migration]

### jo...@chromium.org (2014-02-27)

got a CL for this: https://codereview.chromium.org/183093002/


### bu...@chromium.org (2014-02-27)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=168059

------------------------------------------------------------------------
r168059 | jochen@chromium.org | 2014-02-27T22:57:35.229272Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/modules/webdatabase/DatabaseThread.cpp?r1=168059&r2=168058&pathrev=168059

Ensure that scheduled tasks are executed during db thread shutdown

Since closing the databases on the database thread can schedule
new cleanup tasks, we need to postTask the notificatino that we're done.

BUG=333058
R=michaeln@chromium.org, abarth@chromium.org

Review URL: https://codereview.chromium.org/183093002
------------------------------------------------------------------------

### in...@chromium.org (2014-02-27)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-02-28)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### mb...@chromium.org (2014-03-01)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-03-04)

Please be prepared to merge this tomorrow (once approved).

### la...@google.com (2014-03-05)

[Empty comment from Monorail migration]

### bu...@chromium.org (2014-03-05)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=168543

------------------------------------------------------------------------
r168543 | inferno@chromium.org | 2014-03-05T23:24:11.573861Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/branches/chromium/1750/Source/modules/webdatabase/DatabaseThread.cpp?r1=168543&r2=168542&pathrev=168543

Merge 168059 "Ensure that scheduled tasks are executed during db..."

> Ensure that scheduled tasks are executed during db thread shutdown
> 
> Since closing the databases on the database thread can schedule
> new cleanup tasks, we need to postTask the notificatino that we're done.
> 
> BUG=333058
> R=michaeln@chromium.org, abarth@chromium.org
> 
> Review URL: https://codereview.chromium.org/183093002

TBR=jochen@chromium.org

Review URL: https://codereview.chromium.org/187623004
------------------------------------------------------------------------

### ti...@chromium.org (2014-03-05)

[Empty comment from Monorail migration]

### bu...@chromium.org (2014-03-05)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=168544

------------------------------------------------------------------------
r168544 | inferno@chromium.org | 2014-03-05T23:25:23.513831Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/branches/chromium/1847/Source/modules/webdatabase/DatabaseThread.cpp?r1=168544&r2=168543&pathrev=168544

Merge 168059 "Ensure that scheduled tasks are executed during db..."

> Ensure that scheduled tasks are executed during db thread shutdown
> 
> Since closing the databases on the database thread can schedule
> new cleanup tasks, we need to postTask the notificatino that we're done.
> 
> BUG=333058
> R=michaeln@chromium.org, abarth@chromium.org
> 
> Review URL: https://codereview.chromium.org/183093002

TBR=jochen@chromium.org

Review URL: https://codereview.chromium.org/187923008
------------------------------------------------------------------------

### ti...@chromium.org (2014-03-07)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-04-14)

My apologies for the delay here - $1000 for this one. I'll start the payment process today.

### ti...@chromium.org (2014-04-15)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-04-18)

Processing via our e-payment system can take a few weeks, but reward should be on its way to you (Ref #233620). Thanks again for your help!

### cl...@chromium.org (2014-06-05)

Bulk update: removing view restriction from closed bugs.

### cl...@chromium.org (2016-02-02)

[Empty comment from Monorail migration]

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

This issue was migrated from crbug.com/chromium/333058?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/338108]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40078653)*
