# UNKNOWN in blink::SQLStatementBackend::execute

| Field | Value |
|-------|-------|
| **Issue ID** | [40081332](https://issues.chromium.org/issues/40081332) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Storage |
| **Reporter** | cl...@chromium.org |
| **Assignee** | tk...@chromium.org |
| **Created** | 2015-02-04 |
| **Bounty** | $2,500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4615025003069440

Fuzzer: Therealholden_worker
Job Type: Linux_asan_chrome_v8_arm

Crash Type: UNKNOWN
Crash Address: 0x44c7240c
Crash State:
  blink::SQLStatementBackend::execute
  blink::SQLTransactionBackend::runCurrentStatementAndGetNextState
  blink::SQLTransactionBackend::runStatements
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_v8_arm&range=296680:296701

Minimized Testcase (1.84 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96GDuoHsgIC6QCI3mZLHbeyfbRh7cxlFA_r8DE1D5-pCenDv4_CXZaj_04cZ1LJGcIr6Zsj8q3FNrMGNyUozSRlr36_YCLQ91e_7XeVpjfs60YsmVoW16Z01xnRtA7PZO0QPAfsOqwAazfbOnXL0nThmXFoyA

Additional requirements: Requires Gestures

Additional requirements: Requires HTTP

Filer: mbarbella

## Timeline

### cl...@chromium.org (2015-02-04)

[Empty comment from Monorail migration]

### js...@chromium.org (2015-02-06)

keishi@ - Please investigate this stale pointer appears to be a regression from this CL: https://codereview.chromium.org/563703002

Also CC'ing michaeln@ as owner and tkent@ who also has a CL in range (but that one looks innocuous)


### js...@chromium.org (2015-02-06)

+haraken, since he has a CL in range that looks like the potential culprit as well.

### ha...@chromium.org (2015-02-08)

tkent-san: Would you mind taking a look at this?


### tk...@chromium.org (2015-02-10)

I couldn't reproduce this locally, and I found no suspicious code in modules/webdatabas/.

The testcase contains window.close().  I guess the Oilpan heap for the main thread is destructed before the database thread.
https://crbug.com/chromium/450051 might be the same bug.  Its testcase contains location.reload().


### mi...@chromium.org (2015-02-10)

When is the oilpan heap destroyed in the window.close() sequence? Can you point me to a function/method name for where the heap is destroyed so I can observe that. The database thread should be done upon return from DatabaseContext::stopDatabases(). Is the heap is destroyed prior to that?

### tk...@chromium.org (2015-02-10)

In window.close() case, the oilpan heap for the Blink main thread is terminated at:

   RenderThreadImpl::Shutdown -> blink::shutdown (WebKit.cpp) -> ThreadState::detachMainThread()

and DatabaseContext::stopDatabases() is not called at all.  In blink::shutdown, all of worker threads and the HTML parser thread are terminated explicitly.  Probably we need to terminate database threads here.

On the other hand, location.reload() seems to call stopDatabases().  https://crbug.com/chromium/450051 is a different bug.


### tk...@chromium.org (2015-02-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2015-02-12)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=190021

------------------------------------------------------------------
r190021 | tkent@chromium.org | 2015-02-12T04:28:48.618712Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/modules/InitModules.h?r1=190021&r2=190020&pathrev=190021
   M http://src.chromium.org/viewvc/blink/trunk/Source/modules/webdatabase/DatabaseManager.cpp?r1=190021&r2=190020&pathrev=190021
   M http://src.chromium.org/viewvc/blink/trunk/Source/modules/webdatabase/DatabaseManager.h?r1=190021&r2=190020&pathrev=190021
   M http://src.chromium.org/viewvc/blink/trunk/Source/web/WebKit.cpp?r1=190021&r2=190020&pathrev=190021
   M http://src.chromium.org/viewvc/blink/trunk/Source/modules/InitModules.cpp?r1=190021&r2=190020&pathrev=190021

Web SQL: Termiante database thread before finalizing the Oilpan heap for the Blink main thread.

Oilpan heap for the database thread should be finalized before finalizing the
main thread heap. Usually it's done in ExecutionContext::stopActiveDOMObjects().
When blink::shutdown() is called, stopActiveDOMObjects() was not called and
objects owned by the main thread is finalized though they were referred by the
database thread.  blink::shutdown() should terminate the database thread
explicitly.

BUG=455368,455789

Review URL: https://codereview.chromium.org/892343003
-----------------------------------------------------------------

### bu...@chromium.org (2015-02-12)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=190035

------------------------------------------------------------------
r190035 | tkent@chromium.org | 2015-02-12T09:54:34.322010Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/modules/webdatabase/DatabaseManager.cpp?r1=190035&r2=190034&pathrev=190035
   M http://src.chromium.org/viewvc/blink/trunk/Source/modules/webdatabase/DatabaseManager.h?r1=190035&r2=190034&pathrev=190035

DatabaseManager::terminateDatabaseThread should handle multiple DatabaseContexts.

This is a followup of Blink r190021 [1].

[1] http://src.chromium.org/viewvc/blink?view=rev&rev=190021

BUG=455368,455789

Review URL: https://codereview.chromium.org/913413002
-----------------------------------------------------------------

### tk...@chromium.org (2015-02-13)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-02-13)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### tk...@chromium.org (2015-02-16)

[Empty comment from Monorail migration]

### pe...@google.com (2015-02-16)

[Automated comment] Request affecting a post-stable build (M40), manual review required.

### pe...@google.com (2015-02-16)

Approved for M41 (branch: 2272)

### bu...@chromium.org (2015-02-16)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=190225

------------------------------------------------------------------
r190225 | tkent@chromium.org | 2015-02-16T07:00:58.213939Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/branches/chromium/2272/Source/web/WebKit.cpp?r1=190225&r2=190224&pathrev=190225
   M http://src.chromium.org/viewvc/blink/branches/chromium/2272/Source/modules/InitModules.cpp?r1=190225&r2=190224&pathrev=190225
   M http://src.chromium.org/viewvc/blink/branches/chromium/2272/Source/modules/InitModules.h?r1=190225&r2=190224&pathrev=190225
   M http://src.chromium.org/viewvc/blink/branches/chromium/2272/Source/modules/webdatabase/DatabaseManager.cpp?r1=190225&r2=190224&pathrev=190225
   M http://src.chromium.org/viewvc/blink/branches/chromium/2272/Source/modules/webdatabase/DatabaseManager.h?r1=190225&r2=190224&pathrev=190225

Merge 190021 "Web SQL: Termiante database thread before finalizi..."

> Web SQL: Termiante database thread before finalizing the Oilpan heap for the Blink main thread.
> 
> Oilpan heap for the database thread should be finalized before finalizing the
> main thread heap. Usually it's done in ExecutionContext::stopActiveDOMObjects().
> When blink::shutdown() is called, stopActiveDOMObjects() was not called and
> objects owned by the main thread is finalized though they were referred by the
> database thread.  blink::shutdown() should terminate the database thread
> explicitly.
> 
> BUG=455368,455789
> 
> Review URL: https://codereview.chromium.org/892343003

TBR=tkent@chromium.org

Review URL: https://codereview.chromium.org/930793002
-----------------------------------------------------------------

### bu...@chromium.org (2015-02-16)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=190226

------------------------------------------------------------------
r190226 | tkent@chromium.org | 2015-02-16T07:03:35.588775Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/branches/chromium/2272/Source/modules/webdatabase/DatabaseManager.cpp?r1=190226&r2=190225&pathrev=190226
   M http://src.chromium.org/viewvc/blink/branches/chromium/2272/Source/modules/webdatabase/DatabaseManager.h?r1=190226&r2=190225&pathrev=190226

Merge 190035 "DatabaseManager::terminateDatabaseThread should ha..."

> DatabaseManager::terminateDatabaseThread should handle multiple DatabaseContexts.
> 
> This is a followup of Blink r190021 [1].
> 
> [1] http://src.chromium.org/viewvc/blink?view=rev&rev=190021
> 
> BUG=455368,455789
> 
> Review URL: https://codereview.chromium.org/913413002

TBR=tkent@chromium.org

Review URL: https://codereview.chromium.org/925263004
-----------------------------------------------------------------

### pe...@chromium.org (2015-02-18)

Following discussions with Tim Willis, no more security fixes are going to M40.  M41 hits stable in 2 weeks.

### ti...@google.com (2015-02-26)

[Empty comment from Monorail migration]

### ti...@google.com (2015-03-03)

Congrats - $2500 for this report.

Notes from reward panel: $2000 for the bug + $500 ClusterFuzz bonus.

### ti...@google.com (2015-03-09)

[Empty comment from Monorail migration]

### ti...@google.com (2015-03-17)

Processing via our e-payment system can take up to six weeks, but the reward should be on its way to you. Thanks again for your help!

### cl...@chromium.org (2015-05-22)

Bulk update: removing view restriction from closed bugs.

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

This issue was migrated from crbug.com/chromium/455368?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081332)*
