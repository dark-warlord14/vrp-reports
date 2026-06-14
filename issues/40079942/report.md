# Heap-use-after-free in WebCore::KURL::~KURL

| Field | Value |
|-------|-------|
| **Issue ID** | [40079942](https://issues.chromium.org/issues/40079942) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Network>WebSockets |
| **Reporter** | cl...@chromium.org |
| **Assignee** | yh...@chromium.org |
| **Created** | 2014-06-30 |
| **Bounty** | $2,000.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5865596040249344

Fuzzer: Therealholden_worker
Job Type: Windows_asan_chrome

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x00bbf320
Crash State:
  - crash stack -
  WebCore::KURL::~KURL
  WebCore::NewWebSocketChannelImpl::~NewWebSocketChannelImpl
  - free stack -
  WebCore::NewWebSocketChannelImpl::fail
  WebCore::NewWebSocketChannelImpl::didFail
  

Unminimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv95RxGq__MGtehWVJLLroZxzQbZTPYEp45G6Ch4lGNvIpoGxOFsF7XlOlfce1U8Bhd9LFwThgdLpk0MiZVp-osJSGafRppbT3axVF9-9Pt6RnfsvoEaPXSWLN4Yd-vEkmd7dFFs1DWQ9gaQa6Gy0GTEYZkInsA

Additional requirements: Requires Interaction Gestures
Filer: inferno@chromium.org

## Timeline

### in...@chromium.org (2014-06-30)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-06-30)

[Empty comment from Monorail migration]

### rs...@chromium.org (2014-06-30)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-06-30)

This medium+ severity security issue is a regression on trunk.

Please fix this asap. If you are unable to look into this soon, please revert your change.

- Your friendly ClusterFuzz

### in...@chromium.org (2014-06-30)

yhirano@ does this impact stable, beta ?

### yh...@chromium.org (2014-07-01)

NewWebSocketChannelImpl was enabled on 37.
On 36 it is not used.

### in...@chromium.org (2014-07-01)

Thanks, fixing tags.

### cl...@chromium.org (2014-07-01)

[Empty comment from Monorail migration]

### yh...@chromium.org (2014-07-01)

[Empty comment from Monorail migration]

### bu...@chromium.org (2014-07-02)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=177359

------------------------------------------------------------------
r177359 | yhirano@chromium.org | 2014-07-02T08:08:05.347970Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/modules/websockets/WorkerThreadableWebSocketChannel.cpp?r1=177359&r2=177358&pathrev=177359

[WebSocket] Task creation should be separated from task posting.

Having a complex argument as a waitForMethodCompletion may keep alive
temporary objects which must be killed before posting a task to another
thread.

BUG=390174

Review URL: https://codereview.chromium.org/368453003
-----------------------------------------------------------------

### in...@chromium.org (2014-07-02)

[Empty comment from Monorail migration]

### bu...@chromium.org (2014-07-02)

Is there a merge required here?

### cl...@chromium.org (2014-07-02)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### yh...@chromium.org (2014-07-03)

inferno@, sorry, I was wrong.
This is not a NewWebSocketChannelImpl bug and it affects M36.
Hence merging to M36 and M37 is needed.

+tyoshino as I will be OOO until Jul 9.


### ty...@chromium.org (2014-07-03)

The change to merge is http://src.chromium.org/viewvc/blink?view=revision&revision=177359

### yh...@chromium.org (2014-07-03)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-07-03)

[Empty comment from Monorail migration]

### yh...@chromium.org (2014-07-03)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-07-07)

amineer@ - Merge-Requested for M37 (branch 2062).

tyoshino@ - Please merge once approved by amineer@

### yh...@chromium.org (2014-07-09)

timwillis@: I requested merge for M36 (and I will request for M37 after that), is that OK?



### ma...@google.com (2014-07-10)

This needs to be qualified on 37 before we can consider it for 36.  Replacing 36 label for 37.  When verified, feel free to request merge into 36.

### bu...@chromium.org (2014-07-10)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=177815

------------------------------------------------------------------
r177815 | hiroshige@chromium.org | 2014-07-10T10:39:58.094107Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/page/NetworkStateNotifier.cpp?r1=177815&r2=177814&pathrev=177815
   M http://src.chromium.org/viewvc/blink/trunk/Source/modules/webdatabase/SQLTransactionClient.cpp?r1=177815&r2=177814&pathrev=177815
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/dom/ExecutionContext.cpp?r1=177815&r2=177814&pathrev=177815
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/dom/CrossThreadTask.h?r1=177815&r2=177814&pathrev=177815
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/dom/MessagePort.cpp?r1=177815&r2=177814&pathrev=177815
   M http://src.chromium.org/viewvc/blink/trunk/Source/modules/mediastream/MediaStreamTrackSourcesRequestImpl.cpp?r1=177815&r2=177814&pathrev=177815
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/dom/ExecutionContext.h?r1=177815&r2=177814&pathrev=177815
   M http://src.chromium.org/viewvc/blink/trunk/Source/web/ServiceWorkerGlobalScopeProxy.cpp?r1=177815&r2=177814&pathrev=177815
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/dom/Document.cpp?r1=177815&r2=177814&pathrev=177815
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/workers/WorkerObjectProxy.cpp?r1=177815&r2=177814&pathrev=177815
   M http://src.chromium.org/viewvc/blink/trunk/Source/modules/websockets/WorkerThreadableWebSocketChannel.cpp?r1=177815&r2=177814&pathrev=177815
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/dom/ExecutionContextTask.h?r1=177815&r2=177814&pathrev=177815
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/dom/Document.h?r1=177815&r2=177814&pathrev=177815

Replace CallClosureTask::create(bind()) with createCrossThreadTask()

Background: 
The code pattern of 
postTask(CallClosureTask::create(bind(args))) 
is thread unsafe for posting tasks crossing threads, even if args are
deep-copied, due to temporary objects (created as the return value of bind()
and deep copy functions such as String::isolatedCopy()). 

Solution by this CL: 
Created createCrossThreadTask() and replaced all
CallClosureTask::create(bind()) with createCrossThreadTask().
createCrossThreadTask calls bind and does deep copy (if necessary) by
CrossThreadCopier inside createCrossThreadTask, like createCallbackTask.
This is safer for cross-thread task posting because all temporary objects are
created inside createCrossThreadTask (not in its caller), and thus destroyed
before returning from createCrossThreadTask (i.e. before calling postTask). 

Removed postTask() and postInspectorTask() that accepts Closure&
(i.e. return value of bind()).

BUG=390851
BUG=390174

Review URL: https://codereview.chromium.org/374583002
-----------------------------------------------------------------

### am...@chromium.org (2014-07-11)

which revisions are you requesting for a merge?

### yh...@chromium.org (2014-07-14)

http://src.chromium.org/viewvc/blink?view=revision&revision=177359


### am...@chromium.org (2014-07-14)

merge of blink r177359 approved for m37 beta branch 2062

### bu...@chromium.org (2014-07-15)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=178129

------------------------------------------------------------------
r178129 | yhirano@chromium.org | 2014-07-15T03:25:55.027655Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/branches/chromium/2062/Source/modules/websockets/WorkerThreadableWebSocketChannel.cpp?r1=178129&r2=178128&pathrev=178129

Merge 177359 "[WebSocket] Task creation should be separated from..."

> [WebSocket] Task creation should be separated from task posting.
> 
> Having a complex argument as a waitForMethodCompletion may keep alive
> temporary objects which must be killed before posting a task to another
> thread.
> 
> BUG=390174
> 
> Review URL: https://codereview.chromium.org/368453003

TBR=yhirano@chromium.org, amineer@chromium.org

Review URL: https://codereview.chromium.org/391833004
-----------------------------------------------------------------

### yh...@chromium.org (2014-07-22)

Requesting merge for M36: http://src.chromium.org/viewvc/blink?view=revision&revision=177359

### [Deleted User] (2014-07-22)

Verified on Beta?

### yh...@chromium.org (2014-07-22)

Oh, I've just noticed that the latest beta 37.0.2062.20 doesn't include blink:178129. I should wait more...


### in...@chromium.org (2014-07-22)

Beta verification is not part of the process for security bugs. If you want to add new things, please talk to me and Tim.

### ti...@chromium.org (2014-07-22)

matthewyuan@ - to clarify, although beta verification is a "nice to have", sometimes we don't get that luxury with security bugs. I'll add this bug to the list of M36 release 1 candidates that I'll discuss tomorrow with inferno@ and get back to you.

### am...@google.com (2014-07-23)


Please note that all merge requests must have been on or rolled into trunk
for at least 24 hours to be considered for merging (to ensure full bot
coverage and give an opportunity for any necessary reverts to occur).

To help facilitate this request, if you could please answer the following:
--------------------------------------------------------------------------
1) Has this change been on trunk for at least 24 hours?

2) Has this change shipped to at least one canary release (where applicable)?

3) Has anyone verified that these changes resolve the issue and cause no new
   crashes?

4) Why is this necessary for this milestone?

Thanks!

(this message is auto-generated each time the merge-request label is
applied; if you have previously answered these questions kindly disregard)


### yh...@chromium.org (2014-07-24)

1) Has this change been on trunk for at least 24 hours?
Yes.

2) Has this change shipped to at least one canary release (where applicable)?
Yes.

3) Has anyone verified that these changes resolve the issue and cause no new
   crashes?
We didn't succeed to reproduce the crash on our environment and hence we couldn't verify that the crash is resolved.
This is a thread-related crash and hard to reproduce.

4) Why is this necessary for this milestone?
This is a use-after-free bug although it rarely happens.


### [Deleted User] (2014-07-28)

this got into the latest beta for 37, 37.0.2062.44, can you check to see if this caused any new stability issues on that branch?  I need to know in order to consider this change for merge.

### yh...@chromium.org (2014-07-29)

Currently there are five crashes for Chrome and three crashes for Chrome_Mac including NewWebSocketChannel in the stack trace and none of them are related to this bug.


https://crash.corp.google.com/browse?q=product.name%3D%27Chrome%27%20AND%20product.version%3D%2737.0.2062.44%27%20OMIT%20RECORD%20IF%20SUM(REGEXP(CrashedStackTrace.StackFrame.FunctionName%2C%20%27NewWebSocketChannelImpl%27))%20%3D%200#samplereports

https://crash.corp.google.com/browse?q=product.name%3D%27Chrome_Mac%27%20AND%20product.version%3D%2737.0.2062.44%27%20OMIT%20RECORD%20IF%20SUM(REGEXP(CrashedStackTrace.StackFrame.FunctionName%2C%20%27NewWebSocketChannelImpl%27))%20%3D%200#samplereports

### yh...@chromium.org (2014-07-29)

Currently there are no crashes including WorkerThreadableWebSocketChannel in the stack trace.

https://crash.corp.google.com/browse?q=product.name%3D%27Chrome%27%20AND%20product.version%3D%2737.0.2062.44%27%20OMIT%20RECORD%20IF%20SUM(REGEXP(CrashedStackTrace.StackFrame.FunctionName%2C%20%27WorkerThreadableWebSocketChannel%27))%20%3D%200

https://crash.corp.google.com/browse?q=product.name%3D%27Chrome_Mac%27%20AND%20product.version%3D%2737.0.2062.44%27%20OMIT%20RECORD%20IF%20SUM(REGEXP(CrashedStackTrace.StackFrame.FunctionName%2C%20%27WorkerThreadableWebSocketChannel%27))%20%3D%200


### [Deleted User] (2014-07-29)

[Empty comment from Monorail migration]

### bu...@chromium.org (2014-07-30)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=179211

------------------------------------------------------------------
r179211 | yhirano@chromium.org | 2014-07-30T08:43:07.583992Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/branches/chromium/1985/Source/modules/websockets/WorkerThreadableWebSocketChannel.cpp?r1=179211&r2=179210&pathrev=179211

Merge 177359 "[WebSocket] Task creation should be separated from..."

> [WebSocket] Task creation should be separated from task posting.
>
> Having a complex argument as a waitForMethodCompletion may keep alive
> temporary objects which must be killed before posting a task to another
> thread.
>
> BUG=390174
>
> Review URL: https://codereview.chromium.org/368453003

R=tyoshino@chromium.org
TBR=matthewyuan@chromium.org, yhirano@chromium.org

Review URL: https://codereview.chromium.org/425223002
-----------------------------------------------------------------

### in...@chromium.org (2014-08-02)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-08-06)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-08-06)

Congrats Collin - $2000 for this report (UAF, but does not look like there is control between use and free).

### ti...@chromium.org (2014-09-18)

[Empty comment from Monorail migration]

### ti...@google.com (2014-10-07)

Processing via our e-payment system can take a few weeks, but reward should be on its way to you. Thanks again for your help!

### cl...@chromium.org (2014-10-08)

Bulk update: removing view restriction from closed bugs.

### tk...@chromium.org (2015-11-26)

[Empty comment from Monorail migration]

### tk...@chromium.org (2015-11-27)

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

This issue was migrated from crbug.com/chromium/390174?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40079942)*
