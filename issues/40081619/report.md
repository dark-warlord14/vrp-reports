# Heap-use-after-free in blink::TextFieldInputType::handleKeydownEventForSpinButton

| Field | Value |
|-------|-------|
| **Issue ID** | [40081619](https://issues.chromium.org/issues/40081619) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Reporter** | cl...@chromium.org |
| **Assignee** | tk...@chromium.org |
| **Created** | 2015-03-14 |
| **Bounty** | $1,500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6622863755313152

Fuzzer: Attekett_surku_fuzzer
Job Type: Linux_asan_chrome_media

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x6030000a97f0
Crash State:
  blink::TextFieldInputType::handleKeydownEventForSpinButton
  blink::NumberInputType::handleKeydownEvent
  blink::HTMLInputElement::defaultEventHandler
  

Unminimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv94r36bue8oltdRjyiZq2FsUeahVZzbqOM0ZgrgHDvGMLEY3WrLy4wwmRnevqD-24hDOxnHMXH7Cz3sfRbGY1JhClaE4VDJPtmEDWxjctBwsOBS-G9zQptYRchjUAwMh8uB6RuhraHtJ5XHDfOtGZmwOn2qPQQ


Filer: inferno

## Timeline

### in...@chromium.org (2015-03-14)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-03-14)

[Empty comment from Monorail migration]

### tk...@chromium.org (2015-03-16)

I couldn't reproduce this locally.

According to the stack, I guess spinButtonStepUp() in TextFieldInputType::handleKeydownEventForSpinButton() dispatches a |change| event, and use element() after it.

I'll make a speculative fix.


### tk...@chromium.org (2015-03-16)

[Empty comment from Monorail migration]

### bu...@chromium.org (2015-03-16)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=191896

------------------------------------------------------------------
r191896 | tkent@chromium.org | 2015-03-16T07:37:36.902766Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/html/forms/NumberInputType.cpp?r1=191896&r2=191895&pathrev=191896

Speculative fix of a crash in TextFieldInputType::handleKeydownEvent.

A 'change' event can be dispatched in handleKeydownEventForSpinButton().

BUG=467348

Review URL: https://codereview.chromium.org/1011653002
-----------------------------------------------------------------

### mb...@chromium.org (2015-03-17)

Assuming stable impact based on blame. Please correct this if that turns out not to be the case.

### cl...@chromium.org (2015-03-17)

[Empty comment from Monorail migration]

### tk...@chromium.org (2015-03-18)

I'm waiting CF runs the test again with ToT.  Is there a way to ask it explicitly?


### in...@chromium.org (2015-03-18)

This was a one-time crash, so cf can't confirm. we just assume that it is fixed and will reopen bug if we see same stack again.

### cl...@chromium.org (2015-03-19)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### cl...@chromium.org (2015-03-19)

ClusterFuzz has detected this issue as fixed in range 320820:320909.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6622863755313152

Fuzzer: Attekett_surku_fuzzer
Job Type: Linux_asan_chrome_media

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x6030000a97f0
Crash State:
  blink::TextFieldInputType::handleKeydownEventForSpinButton
  blink::NumberInputType::handleKeydownEvent
  blink::HTMLInputElement::defaultEventHandler
  
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_media&range=320820:320909

Unminimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv94r36bue8oltdRjyiZq2FsUeahVZzbqOM0ZgrgHDvGMLEY3WrLy4wwmRnevqD-24hDOxnHMXH7Cz3sfRbGY1JhClaE4VDJPtmEDWxjctBwsOBS-G9zQptYRchjUAwMh8uB6RuhraHtJ5XHDfOtGZmwOn2qPQQ

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### in...@chromium.org (2015-03-19)

I forced redo, but i think test is flaky, so even fixed range seems wrong.

### tk...@chromium.org (2015-03-22)

Merge-Requested for M41 and M42


### am...@google.com (2015-03-23)

Approved for M42 (branch: 2311)

### am...@google.com (2015-03-23)

[Automated comment] Request affecting a post-stable build (M41), manual review required.

### bu...@chromium.org (2015-03-23)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=192324

------------------------------------------------------------------
r192324 | tkent@chromium.org | 2015-03-23T00:32:56.062886Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/branches/chromium/2311/Source/core/html/forms/NumberInputType.cpp?r1=192324&r2=192323&pathrev=192324

Merge 191896 "Speculative fix of a crash in TextFieldInputType::..."

> Speculative fix of a crash in TextFieldInputType::handleKeydownEvent.
> 
> A 'change' event can be dispatched in handleKeydownEventForSpinButton().
> 
> BUG=467348
> 
> Review URL: https://codereview.chromium.org/1011653002

TBR=tkent@chromium.org

Review URL: https://codereview.chromium.org/1022343002
-----------------------------------------------------------------

### tk...@chromium.org (2015-03-23)

[Empty comment from Monorail migration]

### am...@google.com (2015-03-23)

[Automated comment] Request affecting a post-stable build (M41), manual review required.

### pe...@google.com (2015-03-24)

Merge approved for M41 branch 2272.

### ti...@google.com (2015-03-26)

@tkent - please merge to M41 (branch 2272) ASAP. It needs to be merged today to make the next stable release.

### tk...@chromium.org (2015-03-26)

#20, I merged it yesterday. It seems bugdroid is not working.
http://src.chromium.org/viewvc/blink?view=revision&revision=192584


### tk...@chromium.org (2015-03-26)

[Empty comment from Monorail migration]

### bu...@chromium.org (2015-03-31)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=192584

------------------------------------------------------------------
r192584 | tkent@chromium.org | 2015-03-26T06:33:17.621022Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/branches/chromium/2272/Source/core/html/forms/NumberInputType.cpp?r1=192584&r2=192583&pathrev=192584

Merge 191896 "Speculative fix of a crash in TextFieldInputType::..."

> Speculative fix of a crash in TextFieldInputType::handleKeydownEvent.
> 
> A 'change' event can be dispatched in handleKeydownEventForSpinButton().
> 
> BUG=467348
> 
> Review URL: https://codereview.chromium.org/1011653002

TBR=tkent@chromium.org

Review URL: https://codereview.chromium.org/1031333002
-----------------------------------------------------------------

### ti...@google.com (2015-04-27)

[Empty comment from Monorail migration]

### ti...@google.com (2015-06-14)

Congratulations - $1500 for this report ($1000 + $500 ClusterFuzz bonus)

We'll start payment via our new process, which should take 1-2 weeks. That 1-2 week period payment time frame starts from when you see the "reward-inprocess" label on this bug.

### cl...@chromium.org (2015-06-25)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2015-06-25)

Processing rewards - should be paid in approximately 2 weeks.

### ti...@google.com (2015-07-24)

Processing via our e-payment system can take up to two weeks, but the reward should be on its way to you. Thanks again for your help!

(Note: sorry for the delay here - it turns out in the new payment system, these payments were waiting for a second approval from me).

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/467348?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081619)*
