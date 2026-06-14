# Security: (Shared) (WebSQL) Worker races cause invalid pointers in DatabaseObserver::databaseClosed and DatabaseObserver::reportOpenDatabaseResult

| Field | Value |
|-------|-------|
| **Issue ID** | [40077669](https://issues.chromium.org/issues/40077669) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink, Blink>Workers |
| **Reporter** | th...@gmail.com |
| **Assignee** | me...@chromium.org |
| **Created** | 2013-06-13 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

Chrome crashes in DatabaseObserver::databaseClosed and DatabaseObserver::reportOpenDatabaseResult with an invalid pointer when multiple (random name) databases are opened while the script reloads (continuously) from multiple shared workers onmessage events.

Many other trivial 0-ptr crashes like chromiumOpen, chromiumAccess and chromiumDelete can occur. All seem to be caused by worker races.

It is also possible that the script causes an invalid handle (stack corruption?) while reloading the worker (process). Without a debugger this can (probably) happen unnoticed.

**VERSION**  

Chrome Version: 27.0.1453.110 stable - 29.0.1538.0 continuous (trace)  

Operating System: Windows: XP SP3, 7 SP1

**REPRODUCTION CASE**  

Launch the added script

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: worker  

Crash State: see added stack trace files

## Attachments

- [databaseclosed_crash_trace.txt](attachments/databaseclosed_crash_trace.txt) (text/x-c++; charset=us-ascii, 8.6 KB)
- [reportopendatabaseresult_crash_trace.txt](attachments/reportopendatabaseresult_crash_trace.txt) (text/x-c++; charset=us-ascii, 20.7 KB)
- [websql_dbclosed_reportopen_crash_repro.html](attachments/websql_dbclosed_reportopen_crash_repro.html) (text/plain; charset=us-ascii, 786 B)
- [249502_invalid_handle_trace_x32.txt](attachments/249502_invalid_handle_trace_x32.txt) (text/plain; charset=iso-8859-1, 5.3 KB)
- [249502_invalid_handle_trace_x64.txt](attachments/249502_invalid_handle_trace_x64.txt) (text/plain; charset=us-ascii, 4.6 KB)

## Timeline

### me...@google.com (2013-06-13)

It's a UAF in DatabaseObserver. WorkerThread's web_database_observer_impl_ is passed to WebDatabase::setObserver when worker thread is created. The observer is freed when thread shuts down, but it's still used in DatabaseObserver.

I've touched this stuff recently, I can take a look.

### me...@chromium.org (2013-06-18)

CC'ing folks who have commented on bugs similar to this.

As I mentioned in #1, the problem is that web_database_observer_impl_ is being used from DatabaseObserver after the worker thread shuts down. This is causing a UAF.

I tried to patch this by calling web_database_observer_impl_->WaitForAllDatabasesToClose(); in WorkerThread::Shutdown before anything else, but that brings other null derefs such as Platform::current.

### mi...@chromium.org (2013-06-18)

I gotta question the priority and severity of this class of bug that occurs only in the act of exiting the process, past the point of no return.

The root cause of these problems are that content::WorkerThread/RenderThread shutdown and destruction occur prior the the background threads started in blink having run to completion. A systemic way to deal with that would be the better than one off "fixes" to each individual symptom of that larger problem.

WebKit::shutdown() could be responsible for terminating those background threads. Or instead of getting that far along, the ChildThread could send a sync IPC to the browser process that sayz "kill me now". Code execution on the child thread will never get past that point. So we'd never even try to shutdown webkit.

cc'ing adam who was looking into recasting wecore's threading in terms of chromium's primitives.


In this particular case, there is one instance of WebDatabaseObserverImpl created in the process. It's deleted by content::WorkerThread and content::RenderThread (depending on process type) at the end of time. I think leaking that observer object instead of deleting it would "fix" this bug.

### me...@chromium.org (2013-06-18)

>I gotta question the priority and severity of this class of bug that occurs only in the act of exiting the process, past the point of no return.

Yes, I didn't initially realize this was during process exit.

> Or instead of getting that far along, the ChildThread could send a sync IPC to the browser process that sayz "kill me now".

Is it possible that killing the worker process instantly by the browser process can corrupt IDB and those kind of stuff?

### js...@chromium.org (2013-06-18)

> Is it possible that killing the worker process instantly by the browser process can corrupt IDB and those kind of stuff?

The various storage APIs need to be robust against crashing renderer (or shared worker) processes anyway. IDB has specific tests in this area to ensure the state is consistent even if a renderer process crashes, give or take any unknown bugs in this area.

+1 to webcore -> chromium threading; when I saw abarth's initial work in that area I was optimistic we could resolve this more easily.


### ab...@chromium.org (2013-06-18)

> +1 to webcore -> chromium threading; when I saw abarth's initial work in that area I was optimistic we could resolve this more easily.

I'm not currently working on doing that conversion, but I'm happy to share what I learned in my investigation.

### mi...@chromium.org (2013-06-18)

> Is it possible that killing the worker process instantly by the browser
> process can corrupt IDB and those kind of stuff?

IDB not so much compared to websql, but in both cases we do have stuff in place to defend against random renderer crashes, we have to have that no matter what. In websql's case, we rely on sqlites transaction journal files.

I don't think killing the worker/renderer instantly in ~process would actually change anything in this regard since given the current state of affairs, the background threads are still running at exit time anyway and i suspect they're ultimately getting killed off w/o running to completion anyway.

We'd want to be careful about flushing the outgoing ipc queue, or rather, not changing the behavior in that regard.



### me...@chromium.org (2013-07-09)

[Empty comment from Monorail migration]

### th...@gmail.com (2013-07-19)

On 7(/8) x32/x64, the repro (also) causes invalid handle issues (with memory corruption) on worker shutdown. 

I have no idea if this is related. It may be related to another issue.

Also, I can't repro this on Linux (with ASAN).


### js...@chromium.org (2013-08-27)

This seems to have gone idle. @meacer, are we able to reproduce anything, are you still looking into this, or should we find a new owner?

### in...@chromium.org (2013-09-03)

Bulk move. M29 is released.

### in...@chromium.org (2013-09-03)

Fix labels.

### in...@chromium.org (2013-09-03)

[Empty comment from Monorail migration]

### me...@chromium.org (2013-09-10)

[Empty comment from Monorail migration]

### me...@chromium.org (2013-09-10)

As an initial fix, sending a sync IPC to request killing the worker process seems to work. I'll polish the patch a bit.

### me...@chromium.org (2013-09-11)

Here is a first attempt: https://codereview.chromium.org/23496052/

### me...@chromium.org (2013-09-17)

+atwilson so that he can see this bug.

### at...@chromium.org (2013-09-19)

[Empty comment from Monorail migration]

### jo...@chromium.org (2013-09-19)

re #16: I think this just covers up the bug

We need to spin down the database thread when shutting down WebKit. Maybe we should consider rebasing and landing https://bugs.webkit.org/show_bug.cgi?id=68303

that would break a lot of dependencies on the database thread.

### mi...@chromium.org (2013-09-20)

Worth discussing the gist of this approach vs an alternative, here's my take.

This solution in the CL is better than writing code to carefully terminate and
join webcore's background threads within WebKit::shutdown() without introducing
a deadlock. Any solution of that form would likely not be correct and would
practically speaking never be fully tested. Security vulnerabilities would still
be there. This solution makes this class of shutdown bug impossible. That's has a lot of appeal.

I don't think reviving the old patch jochen referred to and landing it would resolve this problem.


### jo...@chromium.org (2013-09-23)

Killing the process to get shutdown right is a rather heavy handed solution IMO.

Also, we might run into the same problem with renderers. And what about ChromeView where we run in single-process mode?

The patch I was referring to solves the following problem: Currently, the database thread owns all WebDatabases - in order to close a database, you need to spin down the database thread. The patch changes this, so you can delete a database on the main thread, and the database thread just retains enough information to inform the embedder when a database was closed. While not part of the patch, this would make it possible to change the interface that the database closed callback just gets the database name and security origin and not the entire database. Then the database thread doesn't own anything it could use after freeing it.

### mi...@chromium.org (2013-09-23)

> Killing the process to get shutdown right is a rather heavy handed solution IMO.

Yes it is.

> Also, we might run into the same problem with renderers.

Renderers don't run shared workers atm, but it's true that if/when renderers do run shared workers, i'd say we might want to adopt this strategy there too.

> And what about ChromeView where we run in single-process mode?

Single-process mode definitely doesn't run shared workers.

> The patch I was referring to solves the following problem...

All that is fine and good, but you realize while that large change might make it a little easier to deal with WebSQL issues at shutdown, it doesn't actually include changes to handle process shutdown better, subsequent changes are required for that (who knows how large).  Also it does nothing about any other subsystem. A much wider range of things go wrong in worker process shutdown.

Also how many new bugs does the large change you referenced introduce?

The approach is this CL casts a pretty wide net. From a security point of view, I think this is very appealing.

### in...@chromium.org (2013-09-25)

Did you saw our new criteria for possibly issuing higher rewards? See http://www.chromium.org/Home/chromium-security/vulnerability-rewards-program/reward-nomination-process
E.g. If you are able to provide a repro that faulted at an address of 0x41414141, it will qualify for the new higher rewards. Or, if you can show that you have control between free and crash points, etc.

### cl...@chromium.org (2013-09-27)

meacer@: you haven't provided any bug update or come up with a fix for this issue in the last 7 days. Please note that this is a medium+ severity security vulnerability that needs your immediate response. If you have a patch in progress and don't want future nags, please add a codereview link and a WIP label. If the issue is already fixed or you can't reproduce it, please close the bug.

### me...@chromium.org (2013-09-27)

Mr Clusterfuzz: The CL for killing the worker right before exit is still being discussed in email threads.

### in...@chromium.org (2013-09-28)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-10-01)

Fixing milestone and impact labels.

### ke...@chromium.org (2013-10-02)

[Empty comment from Monorail migration]

### th...@gmail.com (2013-10-02)

The title of the merged https://crbug.com/chromium/303154 (found by automated testing?) does not refer to the real issue (ThreadDataTable::RemoveAllThreads UAF). It does refer to one of the trivial crashes I mention in the original comment.

This ChromeURLRequestContextGetter::GetURLRequestContext 0-ptr browser crash is actually an old one (https://crbug.com/chromium/99242).

### me...@chromium.org (2013-10-02)

Re #29: Yes, the automated test hit a null pointer rather than the UAF. It might hit the UAF when we rerun. But the root causes for the bugs are the same, so that's why we merged it into this one.

### [Deleted User] (2013-10-17)

meacer@ are you actively working on this or should we find another owner?

### cl...@chromium.org (2013-10-18)

You have far exceeded the 60-day deadline for fixing this high severity security vulnerability.

We commit ourselves to this deadline and appreciate your utmost priority on this issue.

If you are unable to look into this soon, please find someone else to own this.

### me...@chromium.org (2013-10-21)

There was already a patch for this sitting around: https://codereview.chromium.org/23496052/

We discussed offline and it looks like there is a risk of exploitation, so I'm going to land the patch soon. Jochen said that he started working on shutting down threads correctly. My patch is going to be a bandaid in the meanwhile.

### bu...@chromium.org (2013-11-05)

------------------------------------------------------------------------
r233099 | meacer@chromium.org | 2013-11-05T22:13:37.912217Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/content/worker/worker_thread.h?r1=233099&r2=233098&pathrev=233099
   M http://src.chromium.org/viewvc/chrome/trunk/src/content/browser/worker_host/worker_process_host.cc?r1=233099&r2=233098&pathrev=233099
   M http://src.chromium.org/viewvc/chrome/trunk/src/content/browser/worker_host/worker_process_host.h?r1=233099&r2=233098&pathrev=233099
   M http://src.chromium.org/viewvc/chrome/trunk/src/content/worker/worker_thread.cc?r1=233099&r2=233098&pathrev=233099
   M http://src.chromium.org/viewvc/chrome/trunk/src/content/common/worker_messages.h?r1=233099&r2=233098&pathrev=233099

Kill worker process by way of a sync IPC message before it cleans up.

When a worker process shuts down, it shuts down WebKit. If there are
other threads running in the worker process, this leads to crashes.
This fix tries to kill the worker process forcibly so that no cleanup
takes place.

BUG=249502

Review URL: https://codereview.chromium.org/23496052
------------------------------------------------------------------------

### in...@chromium.org (2013-11-06)

[Empty comment from Monorail migration]

### me...@chromium.org (2013-11-06)

Ok, so this is tentatively fixed with https://codereview.chromium.org/23496052 but Jochen is already working on shutting down threads correctly in worker processes. That will be the actual fix for this whole class of worker bugs. Until then, I'm closing this bug and a few similar bugs that this patch should have fixed.

### me...@chromium.org (2013-11-06)

To clarify #36: https://codereview.chromium.org/23496052 doesn't fix https://crbug.com/chromium/243840 which is also a worker related bug. That bug is different since it manifests itself during a profile being closed.

### cl...@chromium.org (2013-11-06)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-11-06)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

Your fix is very close to the branch point. After the branch happens, please make sure to check if your fix is in.

- Your friendly ClusterFuzz

### cl...@chromium.org (2013-11-06)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-11-06)

------------------------------------------------------------------------
r233367 | jochen@chromium.org | 2013-11-06T21:11:42.771746Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/content/child/web_database_observer_impl.cc?r1=233367&r2=233366&pathrev=233367
   M http://src.chromium.org/viewvc/chrome/trunk/src/content/child/web_database_observer_impl.h?r1=233367&r2=233366&pathrev=233367

Decouple lifetime of database thread and WebDatabase, chromium side.

Add a method to WebDatabaseObserver to close a database without holding
on to an actual WebDatabase. This will make it possible to decouple the
lifetime of WebDatabase and the database thread.

BUG=249502
R=jam@chromium.org

Review URL: https://codereview.chromium.org/50883004
------------------------------------------------------------------------

### in...@chromium.org (2013-11-11)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-11-11)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-11-11)

[Empty comment from Monorail migration]

### ka...@google.com (2013-11-11)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-11-12)

------------------------------------------------------------------------
r234344 | meacer@chromium.org | 2013-11-12T00:16:33.888160Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/1700/src/content/worker/worker_thread.cc?r1=234344&r2=234343&pathrev=234344
   M http://src.chromium.org/viewvc/chrome/branches/1700/src/content/common/worker_messages.h?r1=234344&r2=234343&pathrev=234344
   M http://src.chromium.org/viewvc/chrome/branches/1700/src/content/worker/worker_thread.h?r1=234344&r2=234343&pathrev=234344
   M http://src.chromium.org/viewvc/chrome/branches/1700/src/content/browser/worker_host/worker_process_host.cc?r1=234344&r2=234343&pathrev=234344
   M http://src.chromium.org/viewvc/chrome/branches/1700/src/content/browser/worker_host/worker_process_host.h?r1=234344&r2=234343&pathrev=234344

Merge 233099 "Kill worker process by way of a sync IPC message b..."

> Kill worker process by way of a sync IPC message before it cleans up.
> 
> When a worker process shuts down, it shuts down WebKit. If there are
> other threads running in the worker process, this leads to crashes.
> This fix tries to kill the worker process forcibly so that no cleanup
> takes place.
> 
> BUG=249502
> 
> Review URL: https://codereview.chromium.org/23496052

TBR=meacer@chromium.org

Review URL: https://codereview.chromium.org/69753002
------------------------------------------------------------------------

### me...@chromium.org (2013-11-12)

Jochen: Do we need to merge r233367 as well?

### me...@chromium.org (2013-11-12)

From mail thread: No need to merge.

### in...@chromium.org (2013-12-02)

Merge-Requested for m31.

### jo...@chromium.org (2013-12-02)

I believe that this is fixed on ToT and we can remove the stop-gap.

I'll try to verify locally that this dosn't repro anymore after removing the stop-gap.

### la...@google.com (2013-12-02)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-12-03)

Merged r233099 to m31 in r238433.

### in...@chromium.org (2013-12-03)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-12-03)

------------------------------------------------------------------------
r238433 | inferno@chromium.org | 2013-12-03T18:27:04.918288Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/1650/src/content/worker/worker_thread.cc?r1=238433&r2=238432&pathrev=238433
   M http://src.chromium.org/viewvc/chrome/branches/1650/src/content/common/worker_messages.h?r1=238433&r2=238432&pathrev=238433
   M http://src.chromium.org/viewvc/chrome/branches/1650/src/content/worker/worker_thread.h?r1=238433&r2=238432&pathrev=238433
   M http://src.chromium.org/viewvc/chrome/branches/1650/src/content/browser/worker_host/worker_process_host.cc?r1=238433&r2=238432&pathrev=238433
   M http://src.chromium.org/viewvc/chrome/branches/1650/src/content/browser/worker_host/worker_process_host.h?r1=238433&r2=238432&pathrev=238433

Merge 233099 "Kill worker process by way of a sync IPC message b..."

> Kill worker process by way of a sync IPC message before it cleans up.
> 
> When a worker process shuts down, it shuts down WebKit. If there are
> other threads running in the worker process, this leads to crashes.
> This fix tries to kill the worker process forcibly so that no cleanup
> takes place.
> 
> BUG=249502
> 
> Review URL: https://codereview.chromium.org/23496052

TBR=meacer@chromium.org

Review URL: https://codereview.chromium.org/102543003
------------------------------------------------------------------------

### mb...@chromium.org (2013-12-03)

Thanks for the report! This one qualifies for a $1000 reward. It did not qualify at a higher reward level because it did not seem like this would be easily exploitable.

### th...@gmail.com (2013-12-03)

Thanks!

### in...@chromium.org (2013-12-03)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-12-03)

giving compile failures on m31 merge, punting to m32.

### mb...@chromium.org (2013-12-03)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-12-03)

------------------------------------------------------------------------
r238483 | inferno@chromium.org | 2013-12-03T23:32:41.856164Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/1650/src/content/worker/worker_thread.cc?r1=238483&r2=238482&pathrev=238483
   M http://src.chromium.org/viewvc/chrome/branches/1650/src/content/common/worker_messages.h?r1=238483&r2=238482&pathrev=238483
   M http://src.chromium.org/viewvc/chrome/branches/1650/src/content/worker/worker_thread.h?r1=238483&r2=238482&pathrev=238483
   M http://src.chromium.org/viewvc/chrome/branches/1650/src/content/browser/worker_host/worker_process_host.cc?r1=238483&r2=238482&pathrev=238483
   M http://src.chromium.org/viewvc/chrome/branches/1650/src/content/browser/worker_host/worker_process_host.h?r1=238483&r2=238482&pathrev=238483

Revert 238433 "Merge 233099 "Kill worker process by way of a syn..."

> Merge 233099 "Kill worker process by way of a sync IPC message b..."
> 
> > Kill worker process by way of a sync IPC message before it cleans up.
> > 
> > When a worker process shuts down, it shuts down WebKit. If there are
> > other threads running in the worker process, this leads to crashes.
> > This fix tries to kill the worker process forcibly so that no cleanup
> > takes place.
> > 
> > BUG=249502
> > 
> > Review URL: https://codereview.chromium.org/23496052
> 
> TBR=meacer@chromium.org
> 
> Review URL: https://codereview.chromium.org/102543003

TBR=inferno@chromium.org

Review URL: https://codereview.chromium.org/103243002
------------------------------------------------------------------------

### pa...@chromium.org (2013-12-18)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-12-18)

Payment just kicked off here. Thanks again for your help!

### mb...@chromium.org (2014-01-10)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-02-28)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-03-28)

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

This issue was migrated from crbug.com/chromium/249502?no_tracker_redirect=1

[Multiple monorail components: Blink, Blink>Workers]
[Monorail mergedwith: crbug.com/chromium/258609, crbug.com/chromium/303154]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40077669)*
