# ASSERTION FAILED: actualInfo->derefObjectFunction == wrapperTypeInfo.derefObjectFunction, UNKNOWN in blink::V8Event::createWrapper

| Field | Value |
|-------|-------|
| **Issue ID** | [40080081](https://issues.chromium.org/issues/40080081) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>Storage>IndexedDB |
| **Reporter** | cl...@chromium.org |
| **Assignee** | ta...@chromium.org |
| **Created** | 2014-07-20 |
| **Bounty** | $500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6053924400267264

Fuzzer: Therealholden_worker
Job Type: Linux_asan_chrome_mp

Crash Type: UNKNOWN
Crash Address: 0x00009f7537dd
Crash State:
  - crash stack -
  blink::V8Event::createWrapper
  blink::wrap
  blink::V8WorkerGlobalScopeEventListener::handleEvent
  

Unminimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv955gZfk5FBaTAVMIAGfeHbg3M6SxXEIXJGkFcFP3FY2lnEEuGa8EcPFuHpQPn12SDcLkye_zfKfySsLBSggI36WLAueFlcWvdHqfn3Sx7-yvNfMXi9vxK4lPE5O2qGCeH-YA6ux3fDAWAV90ia-qF_MWr3f3A

Filer: inferno@chromium.org

## Timeline

### in...@chromium.org (2014-07-20)

Hitting the bad cast assert.

ASSERTION FAILED: actualInfo->derefObjectFunction == wrapperTypeInfo.derefObjectFunction
gen/blink/bindings/core/v8/V8Event.cpp(503) : static v8::Handle<v8::Object> blink::V8Event::createWrapper(WTF::PassRefPtr<Event>, v8::Handle<v8::Object>, v8::Isolate *)

### cl...@chromium.org (2014-07-20)

[Empty comment from Monorail migration]

### js...@chromium.org (2014-07-21)

+cmumford, +haraken

haraken@ - is this indicative of a wrapper leaking between worlds?

(Sorry, OOO today, don't have easily browsable source handy.)

### ts...@chromium.org (2014-07-21)

This means that an object of one type known to IDL is being wrapped as another type.  Two possibilities:
1. Everything's fine - its a subclass, but the introspection code that divines the type isn't handling it properly.  You get a loss of generality, and some methods may be missing when you use it in JS down the road.
2. Everything's not fine - you've got a legitimate type confusion going on.

Figuring out which is happening is trivial if you can reproduce the assert under a debugger.  But this seems to be really hard to repro.


### cm...@chromium.org (2014-07-21)

tsepez@ I recently changed three DOMStrings to be enum's. I know that enum's are just DOMStrings with a finite set of legal values - so I don't think it would constitute a type change. Do you think this change may be related?

### js...@chromium.org (2014-07-21)

Ah, right - we'd seen that before when there was IDBCursorWithValue/IDBCursor confusion (one is a subclass of the other, both in C++-land and IDL-land).

Given the stacks, it sounds like it could be Event vs. IDBVersionChangeEvent confusion, since that's the only Event subclass in IDB.

### ts...@chromium.org (2014-07-21)

@cmumford - not likely.
@jsbell - most likely.

### in...@chromium.org (2014-07-22)

reliable repro is coming.

### cl...@chromium.org (2014-07-22)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5225114964590592

Fuzzer: Therealholden_worker
Job Type: Mac_asan_chrome

Crash Type: UNKNOWN
Crash Address: 0xfbadbeef
Crash State:
  - crash stack -
  WebCore::V8Event::createWrapper
  WebCore::wrap
  WebCore::V8WorkerGlobalScopeEventListener::handleEvent
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=mac_asan_chrome&range=274467:274646

Minimized Testcase (1.49 Kb): https://cluster-fuzz.appspot.com/download/AMIfv97RLoKbvmiUHKhTWi2X22Zk9GNlyrregz3MexywdGBex9lKbG01uE_Hsz5RUVtMICOUZFRKw5d5ddbdGeVAPk3Z-QsC4_8ydjN4ioP5k-XwHxeQjRtC2kFLbQdQhmj8KnTJj9xo6-BuUYjNXrOTtxvhP4fm9A
Filer: inferno@chromium.org

### ts...@chromium.org (2014-07-22)

Debug build seems to hit an earlier assert with the test case in #9.  We might want to start there.

### cl...@chromium.org (2014-07-24)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-07-28)

Jsbell@, did you get a chance to look at c#9 testcase. This is high severity bug that we want to get fixed soon, your help is appreciated.

### js...@chromium.org (2014-07-28)

Just starting to look; it doesn't appear to repro for me under a non-ASAN linux build. I notice that both stacks are a bit older than ToT; are folks still able to repro? (There were some oilpan fixes in there.) 

### js...@chromium.org (2014-07-28)

Heh, with an ASAN build I still don't repro, although when I close the window I do get an ASAN:SIGSEV... on a blink::Platform()::current() call. #$%@#$%@#$ Workers  #$%@#$%@#$%!

### js...@chromium.org (2014-07-28)

Finally got a repro of https://crbug.com/chromium/395411#c9 after a handful of runs. I'll keep at it.

### js...@chromium.org (2014-07-29)

Haven't found the root cause yet, but this is interesting:

Instrumenting the generated V8Event::createWrapper() to spew out the impl's interfaceName() and type(), this is seen in frame that asserts:

static v8::Handle<v8::Object> blink::V8Event::createWrapper(WTF::PassRefPtr<Event>, v8::Handle<v8::Object>, v8::Isolate *): IDBVersionChangeEvent / upgradeneeded

Note that this shouldn't happen - V8IDBVersionChangeEvent::createWrapper() should be called instead via ModuleProxy::wrapForEvent(), which is indeed what happens most of the time.

### js...@chromium.org (2014-07-29)

More breadcrumbs: V8IDBVersionChangeEvent::createWrapper() is being called, but its call to V8DOMWrapper::createWrapper() is yielding an empty wrapper, so the V8EventCustom::wrap() logic figures it's not a module event, and it bottoms out in V8Event::createWrapper().

Now... why is V8DOMWrapper::createWrapper() failing?

### js...@chromium.org (2014-07-29)

Next breadcrumb:

V8PerContextData::constructorForTypeSlowCase calls functionTemplate->GetFunction() and the returned handle is empty. FWIW, there's a comment reading:

// Getting the function might fail if we're running out of stack or memory.


### js...@chromium.org (2014-07-29)

I'm at a bit of a loss for what to look at next. I was initially thinking it might be racy behavior (GC vs. RefCounting, or Worker vs. main thread init) but it looks like it might just be OOM?

(In the task manager, the tab consistently climbs up to 770MB before hitting the assertion.)

### in...@chromium.org (2014-07-30)

Getting near OOM shouldn't return bad handle causing bad cast. Can you change this to release assert or have better fallback logic.

### js...@chromium.org (2014-07-30)

Agreed - if that's what's happening then we definitely need to catch it farther upstream (e.g. in constructorForTypeSlowCase) and either kill the renderer or rework how we're doing much of this logic.

I'm just not sure I'm interpreting what I'm seeing correctly, yet. It's still possible we're mucking things up and making v8 give us back an empty handle. Tips from other binding folks welcome!

### js...@chromium.org (2014-07-30)

+arv, in case he remembers anything more about the "Getting the function might fail" comment (> 2 years ago, though).

### ar...@chromium.org (2014-07-30)

Any object allocation may fail in V8 if you run out of memory. I'm not say that that is the case here but the V8 API has to take that into account.

### js...@chromium.org (2014-07-30)

Stupidly I sync'd this morning, now I'm hitting an unrelated DCHECK (due to worker shutdown race in chromium?) about 2/3 of the time, which is slowing down debugging. Tackling both in parallel, whee.

v8::FunctionTemplate::GetFunction()'s call to InstantiateFunction() is returning false, i.e. has_pending_exception is signaled. However, V8::IsDead() is reporting false, but I'm not sure how reliable that is.

### js...@chromium.org (2014-07-30)

Other issue sorted, back to this one. The v8::TryCatch V8PerContextData::constructorForTypeSlowCase has more tidbits:

HasCaught(): true, CanContinue(): false, HasTerminated(): true

Also, it's a v8 internal type TerminationException which is not representable in JS so there's no useful details....

### js...@chromium.org (2014-07-30)

Adding jochen@ just for another set of eyes. Still not sure if we're passing bad data in (although I can't see how), or if v8 has gotten into a bad state (but it's not signalling OOM).

### js...@chromium.org (2014-07-30)

Hrm, looks like this might be a race during Worker termination.

I'm seeing WorkerThread::stop() called on one thread, which eventually calls v8::V8::TerminateExecution(isolate). On another thread, the V8DOMWrapper::createWrapper() / v8::FunctionTemplate::GetFunction() is happening within the same isolate.


### js...@chromium.org (2014-07-30)

Yep. With some more detailed logging in place:

blink::V8PerContextData::constructorForTypeSlowCase(const blink::WrapperTypeInfo *) (isolate 0x62e000258400)
blink::WorkerScriptController::scheduleExecutionTermination() (isolate 0x62e000258400)
blink::V8PerContextData::constructorForTypeSlowCase(const blink::WrapperTypeInfo *): GetFunction() failed (isolate 0x62e000258400)

Since the point of scheduleExecutionTermination() is that we can call it at any time to try and terminate a long-running worker, we need to make the event side of things more resilient. (Basically, what arv@ as saying.)

...

In V8EventCustom we could modify the wrap() call into ModuleProxy::moduleProxy().wrapForEvent() to distinguish "no match" from "failed to wrap" so that it never falls into the V8Event::createWrapper() default. Or... do we even need the default, since there's a special case for V8Event up top?

(+abarth, +tasak, who touched nearby code recently)

### js...@chromium.org (2014-07-31)

Yeah, I think we can just have V8EventCustom's wrap() bottom out in ModuleProxy::moduleProxy().wrapForEvent(), and have that wrapForModuleEvent() ASSERT_NOT_REACHED() after the ...INTERFACES_FOR_EACH(TRY_TO_WRAP...).

Trying that locally, with fingers crossed.

### js...@chromium.org (2014-07-31)

Seems good locally, for some subset of tests at any rate, and the test from https://crbug.com/chromium/395411#c9 is stable now.

Up for try jobs at: 

https://codereview.chromium.org/424813007


### js...@chromium.org (2014-07-31)

[Empty comment from Monorail migration]

### js...@chromium.org (2014-07-31)

[Empty comment from Monorail migration]

### bu...@chromium.org (2014-07-31)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=179340

------------------------------------------------------------------
r179340 | jsbell@chromium.org | 2014-07-31T19:31:23.720345Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/bindings/modules/v8/ModuleBindingsInitializer.cpp?r1=179340&r2=179339&pathrev=179340
   M http://src.chromium.org/viewvc/blink/trunk/Source/bindings/core/v8/custom/V8EventCustom.cpp?r1=179340&r2=179339&pathrev=179340

Simply V8 wrapper generation for Event objects

When trying to determine what kind of wrapper to produce, we'd iterate
over core event types (exiting early) then try iterating over module
event types. If the latter yielded an empty handle we'd wrap the
object as just a V8Event, which is bogus. This could happen in a
worker if the object was indeed a module event type, but the worker
had been asynchronously stopped and v8 was politely failing to produce
a wrapper.

Remove the fallback case, and instead assert if we make it as far as
module event type iteration and no match is found.

BUG=395411
R=abarth,tasak

Review URL: https://codereview.chromium.org/424813007
-----------------------------------------------------------------

### in...@chromium.org (2014-07-31)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-08-03)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### in...@chromium.org (2014-08-03)

assuming impacts stable.

### js...@chromium.org (2014-08-03)

I'm on vacation. I think this was exposed by tasak@'s refactor and does not impact 37 or stable, can he take verify?

### in...@chromium.org (2014-08-06)

[Empty comment from Monorail migration]

### am...@chromium.org (2014-08-06)

Per c#37 this does not impact M37.  I'm removing the merge request, feel free to re-apply if I am incorrect.

### mb...@chromium.org (2014-08-19)

tasak@: Could you please confirm that this does not impact M37?

### ta...@chromium.org (2014-08-20)

mbarbella@:

Yeah, this issue does not impact M37, because my refactor didn't change any logic.

So chrome before my refactor has the same issue.



### in...@chromium.org (2014-08-20)

Tasak@, your comment is confusing. When you say chrome before your refactor has same issue, then it should impact m37, no ?

### aa...@google.com (2014-09-03)

Could not get tasak@ confimation on time, so punting to m38.

### in...@chromium.org (2014-10-07)

Not high severity, this is caught by our release assert.

### ti...@chromium.org (2014-10-07)

Congratulations - $500 for this report (caught by our release assert so low severity).

### cl...@chromium.org (2014-11-06)

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

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-28)

[Empty comment from Monorail migration]

### is...@google.com (2018-07-28)

This issue was migrated from crbug.com/chromium/395411?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080081)*
