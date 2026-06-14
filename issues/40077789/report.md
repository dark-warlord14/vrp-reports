# Heap-use-after-free in WebCore::TimerBase::start

| Field | Value |
|-------|-------|
| **Issue ID** | [40077789](https://issues.chromium.org/issues/40077789) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Reporter** | cl...@gmail.com |
| **Assignee** | sc...@chromium.org |
| **Created** | 2013-07-15 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

The attached test case crashes chrome's asan build. Javascript gc() has to be enabled. A document element is freed and used again during finishedLoading.

**VERSION**  

Chrome Version: asan-symbolized-linux-release-211418  

Operating System: Linux 64bit

**REPRODUCTION CASE**  

The testcase is attached in a zip file as it requires multiple files. crash.html will trigger the crash

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State: see attached crash.log for ASAN output

## Attachments

- [crash.log](attachments/crash.log) (text/plain; charset=us-ascii, 15.4 KB)
- [crash.zip](attachments/crash.zip) (application/zip; charset=binary, 915 B)

## Timeline

### cl...@chromium.org (2013-07-16)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6004963159310336

Uploader: inferno@chromium.org

Crash Type: Heap-use-after-free WRITE 8
Crash Address: 0x61e00002b568
Crash State:
  - crash stack -
  WebCore::TimerBase::start
  WebCore::Document::finishedParsing
  - free stack -
  WebCore::DOMWindow::setDocument
  WebCore::DOMWindow::~DOMWindow
  

Minimized Testcase (0.62 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95WFnEIvGNVF8tqXNIkrBIrSlFlz6-S77kNJs0vYXfGR6Evo4ZG_w6NELkt-xqTjbP53qZOjL9fnBPj5qZa4rqzu296iE1imqnDohT0KB2YcrEv_6ryuysB5w4aaIrsNRScyfA84wVID9hoKRYfhdPxXskynw



### in...@chromium.org (2013-07-16)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-07-16)

The stale object here is SVG document.
previously allocated by thread T0 (chrome) here:
    #0 0x7fa0947bab65 in __interceptor_malloc _asan_rtl_
    #1 0x7fa096d00dad in WebCore::SVGDocument::create(WebCore::Frame*, WebCore::KURL const&) src/third_party/WebKit/Source/core/svg/SVGDocument.h:37

Can one of the SVG experts take this bug please :)

### in...@chromium.org (2013-07-16)

[Empty comment from Monorail migration]

### sc...@chromium.org (2013-07-16)

I'll take it.

### sc...@chromium.org (2013-07-22)

Patch going up.

### bu...@chromium.org (2013-07-22)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=154680

------------------------------------------------------------------------
r154680 | schenney@chromium.org | 2013-07-22T20:33:16.114803Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/loader/iframe-src-change-onload-crash.html?r1=154680&r2=154679&pathrev=154680
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/loader/resources/empty.xml?r1=154680&r2=154679&pathrev=154680
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/loader/iframe-src-change-onload-crash-expected.txt?r1=154680&r2=154679&pathrev=154680
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/dom/Document.cpp?r1=154680&r2=154679&pathrev=154680

Protect documents from deletion when their onload removes them

When an XML document is the src of an iframe, and the onload method
changes the src to something else, the XML document may be garbage
collected before the original load is completed. Bad things result.

In this patch we protect the document in Document::finishedParsing.

R=abarth@chromium.org,eseidel@chromium.org,inferno@chromium.org
BUG=260428

Review URL: https://chromiumcodereview.appspot.com/19962002
------------------------------------------------------------------------

### in...@chromium.org (2013-07-22)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-07-23)

ClusterFuzz has detected this issue as fixed in range 213073:213078.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6004963159310336

Uploader: inferno@chromium.org

Crash Type: Heap-use-after-free WRITE 8
Crash Address: 0x61e00002b568
Crash State:
  - crash stack -
  WebCore::TimerBase::start
  WebCore::Document::finishedParsing
  - free stack -
  WebCore::DOMWindow::setDocument
  WebCore::DOMWindow::~DOMWindow
  
Fixed: https://cluster-fuzz.appspot.com/revisions?range=213073:213078

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv95WFnEIvGNVF8tqXNIkrBIrSlFlz6-S77kNJs0vYXfGR6Evo4ZG_w6NELkt-xqTjbP53qZOjL9fnBPj5qZa4rqzu296iE1imqnDohT0KB2YcrEv_6ryuysB5w4aaIrsNRScyfA84wVID9hoKRYfhdPxXskynw

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### bu...@chromium.org (2013-07-31)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=155205

------------------------------------------------------------------------
r155205 | cevans@chromium.org | 2013-07-31T02:29:26.156187Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/branches/chromium/1547/LayoutTests/loader/iframe-src-change-onload-crash-expected.txt?r1=155205&r2=155204&pathrev=155205
   M http://src.chromium.org/viewvc/blink/branches/chromium/1547/Source/core/dom/Document.cpp?r1=155205&r2=155204&pathrev=155205
   A http://src.chromium.org/viewvc/blink/branches/chromium/1547/LayoutTests/loader/iframe-src-change-onload-crash.html?r1=155205&r2=155204&pathrev=155205
   A http://src.chromium.org/viewvc/blink/branches/chromium/1547/LayoutTests/loader/resources/empty.xml?r1=155205&r2=155204&pathrev=155205

Merge 154680 "Protect documents from deletion when their onload ..."

> Protect documents from deletion when their onload removes them
> 
> When an XML document is the src of an iframe, and the onload method
> changes the src to something else, the XML document may be garbage
> collected before the original load is completed. Bad things result.
> 
> In this patch we protect the document in Document::finishedParsing.
> 
> R=abarth@chromium.org,eseidel@chromium.org,inferno@chromium.org
> BUG=260428
> 
> Review URL: https://chromiumcodereview.appspot.com/19962002

TBR=schenney@chromium.org

Review URL: https://codereview.chromium.org/21286005
------------------------------------------------------------------------

### sc...@gmail.com (2013-07-31)

M29: http://src.chromium.org/viewvc/blink?view=rev&rev=155205

### sc...@gmail.com (2013-08-11)

Awesome! $1000

### pa...@chromium.org (2013-08-16)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-08-19)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-08-19)

[Empty comment from Monorail migration]

### js...@chromium.org (2013-11-18)

Bulk release of old security bug reports.


### js...@chromium.org (2013-11-18)

Bulk release of old security bug reports.


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

This issue was migrated from crbug.com/chromium/260428?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40077789)*
