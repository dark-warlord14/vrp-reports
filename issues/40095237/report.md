# Use-after-free in findPlaceForCounter

| Field | Value |
|-------|-------|
| **Issue ID** | [40095237](https://issues.chromium.org/issues/40095237) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | mi...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2011-09-16 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

use-after-free with counters, 32 inside 72

**VERSION**  

Chrome Version:  

Chromium 16.0.884.0 (Developer Build 101535-dirty)  

OS Linux  

WebKit 535.4 (trunk@95290)  

JavaScript V8 3.6.4  

Operating System: linux 64bit

**REPRODUCTION CASE**  

attached

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: renderer + asan/vg  

Crash State:

ERROR: AddressSanitizer heap-use-after-free on address 0x00007fffdd208ca0 at pc 0x7ffff3cf0c13 bp 0x7fffffff51b0 sp 0x7fffffff5140  

READ of size 8 at 0x00007fffdd208ca0 thread T0  

#0 0x7ffff3cf0c13 in WebCore::findPlaceForCounter(WebCore::RenderObject\*, WTF::AtomicString const&, bool, WebCore::CounterNode\*&, WebCore::CounterNode\*&) third\_party/WebKit/Source/WebCore/rendering/RenderCounter.cpp:0  

#1 0x7ffff3ce88c8 in WebCore::makeCounterNode(WebCore::RenderObject\*, WTF::AtomicString const&, bool) third\_party/WebKit/Source/WebCore/rendering/RenderCounter.cpp:0

0x00007fffdd208ca0 is located 32 bytes inside of 72-byte region  

freed by thread T0 here:  

#0 0x7ffff621b0fa in free *asan\_rtl*  

#1 0x7ffff3ceddd8 in WTF::HashTable<WTF::RefPtr[WTF::AtomicStringImpl](javascript:void(0);), std::pair<WTF::RefPtr[WTF::AtomicStringImpl](javascript:void(0);), WTF::RefPtr[WebCore::CounterNode](javascript:void(0);)

## Attachments

- [vg-counter32.txt](attachments/vg-counter32.txt) (text/plain; charset=us-ascii, 9.4 KB)
- [counters32.txt](attachments/counters32.txt) (text/plain; charset=us-ascii, 11.7 KB)
- [count32r.html](attachments/count32r.html) (text/plain; charset=us-ascii, 348 B)

## Timeline

### in...@chromium.org (2011-09-16)

hits assert on trunk.

### in...@chromium.org (2011-09-16)

Another repro from 95520 from Miaubiz. This bug is crashing in counters, not related to fix in 95520.

<style>
  :before {
    display: table-row-group;
    content: "A";
  }
    @font-face { font-family: "A"; src: url(); }
    body { width: 2ex; }
  div::after {
    content:counter(ctr) url(-);

  }
  .table-row::after { display:table-row; }
  </style>                              
</html>
<style>
</style>

<div class="table-row">A</div>

### in...@chromium.org (2011-09-19)

[Empty comment from Monorail migration]

### ke...@chromium.org (2011-09-19)

[Empty comment from Monorail migration]

### [Deleted User] (2011-09-19)

That's quite presumptuous :P

### ke...@chromium.org (2011-09-19)

A little birdy told me you are all over this one. :D

### [Deleted User] (2011-09-21)

Filed upstream as https://bugs.webkit.org/show_bug.cgi?id=68563

### in...@chromium.org (2011-09-22)

testcase in c#2 is probably rendercounter issue. filed new bug http://code.google.com/p/chromium/issues/detail?id=97608.

### [Deleted User] (2011-10-04)

fix landed upstream as http://trac.webkit.org/changeset/96632

### js...@chromium.org (2011-10-05)

Batch update: assuming these security changes impacted stable based on some fuzzy filtering.

### in...@chromium.org (2011-10-07)

merged to m15 in r96955

### sc...@gmail.com (2011-10-19)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-10-19)

Thanks miaubiz. $1000

----
Boilerplate text:
Please do NOT publicly disclose details until a fix has been released to all our
users. Early public disclosure may cancel the provisional reward.
Also, please be considerate about disclosure when the bug affects a core library
that may be used by other products.
Please do NOT share this information with third parties who are not directly
involved in fixing the bug. Doing so may cancel the provisional reward.
Please be honest if you have already disclosed anything publicly or to third parties.
----

### sc...@gmail.com (2011-10-19)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-10-28)

Payment in system, can take up to a couple of weeks.

### [Deleted User] (2012-05-15)

Marking old security bugs Fixed..

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-01)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

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

This issue was migrated from crbug.com/chromium/96902?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095237)*
