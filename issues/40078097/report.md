# Heap-use-after-free in WTF::equalNonNull

| Field | Value |
|-------|-------|
| **Issue ID** | [40078097](https://issues.chromium.org/issues/40078097) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | jo...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2013-09-13 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

At this stage (it's almost 3am UK time) I haven't done any analysis beyond what is obvious from the symbolized asan output. The id of an HTML object element (object2 in the testcase) is freed before the element itself is freed. This issue can be triggered in a few ways, I went with cloneNode() as it iterates over all properties of an element.

The repro case is reliable, but very picky about the order things are in. I hope to add more detail soon.

**VERSION**  

Chrome Version: 31.0.1627.0  

Operating System: Xubuntu 13.04

**REPRODUCTION CASE**  

A minimized testcase is attached. For ease of reproduction, enable the use of window.gc() in the JS flags. A full symbolized ASAN output is also attached.

## Attachments

- [asan_sym.txt](attachments/asan_sym.txt) (text/plain; charset=us-ascii, 12.6 KB)
- [repro.html](attachments/repro.html) (text/html; charset=us-ascii, 1.3 KB)

## Timeline

### sc...@gmail.com (2013-09-13)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-09-13)

Ah, this could be something I caused personally ;-)

### cl...@chromium.org (2013-09-13)

ClusterFuzz is now working on this testcase. See https://cluster-fuzz.appspot.com/testcase?key=5591671945297920

### in...@chromium.org (2013-09-13)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-09-13)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5591671945297920

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x60a0001258c4
Crash State:
  - crash stack -
  WTF::equalNonNull
  WTF::KeyValuePair<WTF::StringImpl*, unsigned int>* WTF::HashTable<WTF::StringImpl*, WTF::KeyValuePai
  - free stack -
  WebCore::ElementData::deref
  WebCore::Element::~Element
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=213363:213377

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv94Jk9ZmbQnnHGCMZGqVhTIZOWiJq0Jum-GFGlqs9-bJ--xNxMeCoF_oLmiaxdR2X3h4ohb7WFdUrRwY-arWJ95SGZ6jOcd4k5VVuCuzVrg58tSB1wXij1nr7uInY3qXgraKQGtdC_fvhMPA6iQiixZhfRG9sQ



### cl...@chromium.org (2013-09-18)

ClusterFuzz thinks that this bug might be eligible for a reward! Forwarding to reward panel for consideration.

### in...@chromium.org (2013-09-25)

Did you saw our new criteria for possibly issuing higher rewards? See http://www.chromium.org/Home/chromium-security/vulnerability-rewards-program/reward-nomination-process
E.g. If you are able to provide a repro that faulted at an address of 0x41414141, it will qualify for the new higher rewards. Or, if you can show that you have control between free and crash points, etc.

### jw...@chromium.org (2013-09-27)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-09-28)

cevans@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!)

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2013-10-01)

Fixing impact labels.

### in...@chromium.org (2013-10-06)

Sorry for the multiple nag comments in the last 24 hrs. It was supposed to be just one per week :), but a bug in sheriffbot caused it to generate multiple ones. Sorry for the inconvenience.

### cl...@chromium.org (2013-10-06)

cevans@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!)

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2013-10-15)

cevans@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!)

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2013-10-18)

ClusterFuzz has detected this issue as fixed in range 222822:222891.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5591671945297920

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x60a0001258c4
Crash State:
  - crash stack -
  WTF::equalNonNull
  WTF::KeyValuePair<WTF::StringImpl*, unsigned int>* WTF::HashTable<WTF::StringImpl*, WTF::KeyValuePai
  - free stack -
  WebCore::ElementData::deref
  WebCore::Element::~Element
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=213363:213377
Fixed: https://cluster-fuzz.appspot.com/revisions?range=222822:222891

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv94Jk9ZmbQnnHGCMZGqVhTIZOWiJq0Jum-GFGlqs9-bJ--xNxMeCoF_oLmiaxdR2X3h4ohb7WFdUrRwY-arWJ95SGZ6jOcd4k5VVuCuzVrg58tSB1wXij1nr7uInY3qXgraKQGtdC_fvhMPA6iQiixZhfRG9sQ

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### cl...@chromium.org (2013-10-18)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5591671945297920

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x60a0001258c4
Crash State:
  - crash stack -
  WTF::equalNonNull
  WTF::KeyValuePair<WTF::StringImpl*, unsigned int>* WTF::HashTable<WTF::StringImpl*, WTF::KeyValuePai
  - free stack -
  WebCore::ElementData::deref
  WebCore::Element::~Element
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=213363:213377

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv94Jk9ZmbQnnHGCMZGqVhTIZOWiJq0Jum-GFGlqs9-bJ--xNxMeCoF_oLmiaxdR2X3h4ohb7WFdUrRwY-arWJ95SGZ6jOcd4k5VVuCuzVrg58tSB1wXij1nr7uInY3qXgraKQGtdC_fvhMPA6iQiixZhfRG9sQ



### sc...@gmail.com (2013-10-21)

Ok, I let this sit for far too long.
Looks like a simple fix for an object lifetime issue exposed by http://src.chromium.org/viewvc/blink?view=rev&rev=154790

### sc...@gmail.com (2013-10-21)

[Empty comment from Monorail migration]

### jo...@gmail.com (2013-10-21)

Ok, but if AtomicStringImpl / StringImpl are functionally the same, care to explain how this creates object lifetime issues? It was always a RefPtr wasn't it?

### sc...@gmail.com (2013-10-21)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-10-22)

So the two hash keys are:
Old: AtomicStringImpl*
New: StringImpl*

The code has always buggy insofar as a stale pointer gets left in the hash set. Interestingly, though, the hash function for AtomicStringImpl* is just a pointer compare. So ASAN will never see it, although there could still be adverse side effects. StringImpl*, however, has a hash function override that dereferences the pointer in order to fetch and maybe compute a hash. So a stale pointer here is now visible to ASAN.

### in...@chromium.org (2013-10-22)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-10-22)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=160250

------------------------------------------------------------------------
r160250 | cevans@chromium.org | 2013-10-22T20:01:13.944247Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/dom/id-attribute-shared.html?r1=160250&r2=160249&pathrev=160250
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/html/HTMLDocument.cpp?r1=160250&r2=160249&pathrev=160250
   M http://src.chromium.org/viewvc/blink/trunk/Source/bindings/v8/custom/V8WindowCustom.cpp?r1=160250&r2=160249&pathrev=160250
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/html/HTMLDocument.h?r1=160250&r2=160249&pathrev=160250
   M http://src.chromium.org/viewvc/blink/trunk/Source/bindings/v8/V8WindowShell.cpp?r1=160250&r2=160249&pathrev=160250
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/dom/id-attribute-shared-expected.txt?r1=160250&r2=160249&pathrev=160250

Fix tracking of the id attribute string if it is shared across elements.

The patch to remove AtomicStringImpl:
http://src.chromium.org/viewvc/blink?view=rev&rev=154790

Exposed a lifetime issue with strings for id attributes. We simply need to use
AtomicString.

BUG=290566

Review URL: https://codereview.chromium.org/33793004
------------------------------------------------------------------------

### sc...@gmail.com (2013-10-22)

Dear release manager: I request merge! :)
Obviously, I'll make sure it hits a dev channel successfully before merging.

Aside from fixing a security bug (which is partly an M30 regression, unfortunately), this should also fix a known source of crash reports in the wild (see https://crbug.com/chromium/265502 where SyzyASAN caught it).

### cl...@chromium.org (2013-10-23)

ClusterFuzz has detected this issue as fixed in range 230072:230091.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5591671945297920

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x60a0001258c4
Crash State:
  - crash stack -
  WTF::equalNonNull
  WTF::KeyValuePair<WTF::StringImpl*, unsigned int>* WTF::HashTable<WTF::StringImpl*, WTF::KeyValuePai
  - free stack -
  WebCore::ElementData::deref
  WebCore::Element::~Element
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=213363:213377
Fixed: https://cluster-fuzz.appspot.com/revisions?range=230072:230091

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv94Jk9ZmbQnnHGCMZGqVhTIZOWiJq0Jum-GFGlqs9-bJ--xNxMeCoF_oLmiaxdR2X3h4ohb7WFdUrRwY-arWJ95SGZ6jOcd4k5VVuCuzVrg58tSB1wXij1nr7uInY3qXgraKQGtdC_fvhMPA6iQiixZhfRG9sQ

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### la...@google.com (2013-10-24)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-10-29)

merged to m31 in r160842

### bu...@chromium.org (2013-10-29)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=160842

------------------------------------------------------------------------
r160842 | inferno@chromium.org | 2013-10-29T16:41:32.630257Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/branches/chromium/1650/LayoutTests/fast/dom/id-attribute-shared-expected.txt?r1=160842&r2=160841&pathrev=160842
   A http://src.chromium.org/viewvc/blink/branches/chromium/1650/LayoutTests/fast/dom/id-attribute-shared.html?r1=160842&r2=160841&pathrev=160842
   M http://src.chromium.org/viewvc/blink/branches/chromium/1650/Source/core/html/HTMLDocument.cpp?r1=160842&r2=160841&pathrev=160842
   M http://src.chromium.org/viewvc/blink/branches/chromium/1650/Source/bindings/v8/custom/V8WindowCustom.cpp?r1=160842&r2=160841&pathrev=160842
   M http://src.chromium.org/viewvc/blink/branches/chromium/1650/Source/core/html/HTMLDocument.h?r1=160842&r2=160841&pathrev=160842
   M http://src.chromium.org/viewvc/blink/branches/chromium/1650/Source/bindings/v8/V8WindowShell.cpp?r1=160842&r2=160841&pathrev=160842

Merge 160250 "Fix tracking of the id attribute string if it is s..."

> Fix tracking of the id attribute string if it is shared across elements.
> 
> The patch to remove AtomicStringImpl:
> http://src.chromium.org/viewvc/blink?view=rev&rev=154790
> 
> Exposed a lifetime issue with strings for id attributes. We simply need to use
> AtomicString.
> 
> BUG=290566
> 
> Review URL: https://codereview.chromium.org/33793004

TBR=cevans@chromium.org

Review URL: https://codereview.chromium.org/50463004
------------------------------------------------------------------------

### sc...@gmail.com (2013-11-05)

[Empty comment from Monorail migration]

### mb...@chromium.org (2013-11-08)

Thanks for the report! This one qualifies for a $1000 reward. It did not qualify at a higher reward level because there does not seem to be control between the free and use, and because this is in the string heap partition.

### in...@chromium.org (2013-11-12)

[Empty comment from Monorail migration]

### js...@chromium.org (2013-11-14)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-12-18)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-12-18)

Hey Jon, payment process kicked off on this one. Thanks! :)

### cl...@chromium.org (2014-02-06)

Bulk update: removing view restriction from closed bugs.

### ti...@chromium.org (2014-02-28)

[Empty comment from Monorail migration]

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

This issue was migrated from crbug.com/chromium/290566?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/265502, crbug.com/chromium/288171, crbug.com/chromium/309860]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40078097)*
