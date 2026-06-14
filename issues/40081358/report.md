# Possibly invalid type cast in blink::V8LazyEventListener::prepareListenerObject

| Field | Value |
|-------|-------|
| **Issue ID** | [40081358](https://issues.chromium.org/issues/40081358) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Bindings |
| **Reporter** | pi...@live.nl |
| **Assignee** | jo...@chromium.org |
| **Created** | 2015-02-06 |
| **Bounty** | $3,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 6.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.111 Safari/537.36

Steps to reproduce the problem:
The problem is triggered on this page:

data:text/html,<!doctype html><html onmousedown="};}}}}); true?0x123456:(function() {{{{{"><script>document.documentElement.onmousedown;</script>

What is the expected behavior?
Nothing happens.

What went wrong?
The renderer crashes.

Did this work before? N/A 

Chrome version: 40.0.2214.111  Channel: stable
OS Version: 6.0 (Windows Vista, Windows Server 2008)
Flash Version: Shockwave Flash 16.0 r0

There seems to be an invalid type cast in blink::V8LazyEventListener::prepareListenerObject. Namely, it constructs JavaScript code through string concatenation, then runs it, and casts the return value into a function on line 170. However, with an incorrect `listenerSource`, the return value can be something different. The code is triggered by using inline HTML event listeners. I debugged the above page with WinDbg and found that inside v8::Function::Call, the register ecx points to the value 0x2468ac (which is 0x123456<<1), whereas I guess it should be a pointer to a function.

I think the line ASSERT(result->IsFunction()) is hit, but it looks like the snapshot I used [1] does not have asserts enabled.

The solution might be transforming the assert into the early return before it.

[1] https://commondatastorage.googleapis.com/chromium-browser-snapshots/index.html?prefix=Win/314811/

## Timeline

### cl...@chromium.org (2015-02-06)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5735247399354368

Uploader: mbarbella@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: UNKNOWN
Crash Address: 0x000000000000
Crash State:
  v8::Function::Call
  blink::V8ScriptRunner::callInternalFunction
  blink::V8LazyEventListener::prepareListenerObject
  

Unminimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv967MaMAxOSsNV10valIglGVVIQVEQYkZNGhFwNzsh4CfRnXD56FwyGKnB2xxHv0UMTXVgMih1G7NFtgfpWa9UOxZHEbdqKVCQDizgfiIO29ppVg7OQeGF_Pgp3ItMRN-1t2h5YxfzZwNIBbazQiz-xZOuJ7kw


Filer: mbarbella

### js...@chromium.org (2015-02-06)

jochen@ - I can't tell if this is dangerous or benign from a cursory inspection. Would you mind taking a closer look, if finding someone who could?

### ri...@chromium.org (2015-02-07)

Nice find, that code is pretty hilarious - I'm pretty sure this is high severity. What I would probably do is compile the inner function separately, then put it into the with chain by calling a function with an argument, if that's possible.

### cl...@chromium.org (2015-02-07)

[Empty comment from Monorail migration]

### jo...@chromium.org (2015-02-09)

quick fix is in the CQ: https://codereview.chromium.org/906193002

New V8 API is underway here: https://codereview.chromium.org/910683002

### bu...@chromium.org (2015-02-09)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=189796

------------------------------------------------------------------
r189796 | jochen@chromium.org | 2015-02-09T13:29:43.262409Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/security/lazy-event-listener.html?r1=189796&r2=189795&pathrev=189796
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/security/lazy-event-listener-expected.txt?r1=189796&r2=189795&pathrev=189796
   M http://src.chromium.org/viewvc/blink/trunk/Source/bindings/core/v8/V8LazyEventListener.cpp?r1=189796&r2=189795&pathrev=189796

Turn a bunch of ASSERTs into graceful failures when compiling listeners

BUG=456192
R=yangguo@chromium.org

Review URL: https://codereview.chromium.org/906193002
-----------------------------------------------------------------

### jo...@chromium.org (2015-02-09)

Marking as fixed for merging

### bu...@chromium.org (2015-02-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/30674bdeb45241836bc309e42f008e66908f65e1

commit 30674bdeb45241836bc309e42f008e66908f65e1
Author: jochen <jochen@chromium.org>
Date: Mon Feb 09 15:15:29 2015

Introduce a compile method that takes context extensions

BUG=chromium:456192
R=yangguo@chromium.org
LOG=y

Review URL: https://codereview.chromium.org/910683002

Cr-Commit-Position: refs/heads/master@{#26530}

[modify] http://crrev.com/30674bdeb45241836bc309e42f008e66908f65e1/include/v8.h
[modify] http://crrev.com/30674bdeb45241836bc309e42f008e66908f65e1/src/api.cc
[modify] http://crrev.com/30674bdeb45241836bc309e42f008e66908f65e1/test/cctest/test-compiler.cc


### cl...@chromium.org (2015-02-09)

[Empty comment from Monorail migration]

### pe...@google.com (2015-02-10)

[Automated comment] Request affecting a post-stable build (M40), manual review required.

### pe...@google.com (2015-02-10)

Approved for M41 (branch: 2272)

### bu...@chromium.org (2015-02-10)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=189920

------------------------------------------------------------------
r189920 | jochen@chromium.org | 2015-02-10T19:18:32.758523Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/branches/chromium/2272/LayoutTests/security/lazy-event-listener.html?r1=189920&r2=189919&pathrev=189920
   A http://src.chromium.org/viewvc/blink/branches/chromium/2272/LayoutTests/security/lazy-event-listener-expected.txt?r1=189920&r2=189919&pathrev=189920
   M http://src.chromium.org/viewvc/blink/branches/chromium/2272/Source/bindings/core/v8/V8LazyEventListener.cpp?r1=189920&r2=189919&pathrev=189920

Merge 189796 "Turn a bunch of ASSERTs into graceful failures whe..."

> Turn a bunch of ASSERTs into graceful failures when compiling listeners
> 
> BUG=456192
> R=yangguo@chromium.org
> 
> Review URL: https://codereview.chromium.org/906193002

TBR=jochen@chromium.org

Review URL: https://codereview.chromium.org/913713004
-----------------------------------------------------------------

### jo...@chromium.org (2015-02-10)

Note that the merge request is only for blink r189796

### pe...@google.com (2015-02-11)

[Automated comment] Request affecting a post-stable build (M40), manual review required.

### in...@chromium.org (2015-02-12)

[Empty comment from Monorail migration]

### ti...@google.com (2015-02-17)

Penny - based on #13 can you approve the merge of r189796 as well into M41? (Branch 2272).


### pe...@chromium.org (2015-02-17)

Yes, merge of r189796 approved for M41 (2272).  Merge away!

### ti...@google.com (2015-02-17)

Thanks pennymac!

jochen: as directed, please merge away for r189796.



### pe...@chromium.org (2015-02-17)

Jochen actually finished getting r189796 into 2272 a week ago (before he disappeared).

It was committed into M41/2272 as r189920.

Nothing to do here.

### in...@chromium.org (2015-02-17)

[Empty comment from Monorail migration]

### ti...@google.com (2015-02-26)

[Empty comment from Monorail migration]

### ti...@google.com (2015-03-03)

Congratulations - $3000 for this report.

### ti...@google.com (2015-03-06)

[Empty comment from Monorail migration]

### ti...@google.com (2015-04-06)

Processing via our e-payment system can take up to six weeks, but the reward should be on its way to you. Thanks again for your help!

### cl...@chromium.org (2015-05-18)

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

This issue was migrated from crbug.com/chromium/456192?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/457016]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081358)*
