# Heap-use-after-free in WebCore::copyKeysToReferencingVector

| Field | Value |
|-------|-------|
| **Issue ID** | [40077782](https://issues.chromium.org/issues/40077782) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Reporter** | cl...@gmail.com |
| **Assignee** | dc...@chromium.org |
| **Created** | 2013-07-13 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

The attached testcase crashes the latest chrome ASAN build. It involves events, javascript urls and frames. The testcase requires gc() in javascript.

**VERSION**  

Chrome Version: asan-symbolized-linux-release-211418

**REPRODUCTION CASE**  

See attached crash.html

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State: see attached crash.txt for ASAN log

## Attachments

- [crash.txt](attachments/crash.txt) (text/plain; charset=us-ascii, 14.1 KB)
- [crash.html](attachments/crash.html) (text/html; charset=us-ascii, 1.2 KB)

## Timeline

### in...@chromium.org (2013-07-13)

Great find cloudfuzzer! How would you like to be credited in the release notes.

### cl...@chromium.org (2013-07-13)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4962809746030592

Uploader: inferno@chromium.org

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x613000050dc8
Crash State:
  - crash stack -
  WebCore::copyKeysToReferencingVector
  WebCore::DeviceController::dispatchDeviceEvent
  - free stack -
  v8::internal::GlobalHandles::Node::PostGarbageCollectionProcessing
  v8::internal::GlobalHandles::PostGarbageCollectionProcessing
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=204670:204818

Minimized Testcase (1.15 Kb): https://cluster-fuzz.appspot.com/download/AMIfv97GcY9ovtUye24C8oHbwf2QQCHpt-Fc7ZXdZOhOn6Dze0M0KgHp-ke8-piQSPPxnG5c3A0g-UGwDuh8418J8pEQonHzyJ4os_fmHP5ksMe4-3xhtF69h7H14pOXhsxqyNf3vUEDPt9_nax4-oLKuGHyC9Yf4A



### in...@chromium.org (2013-07-13)

Looks like regression from http://src.chromium.org/viewvc/blink?view=rev&revision=151960

### dc...@chromium.org (2013-07-14)

Ugh. Since DeviceController is a Page supplement, if the frame is detached, then DOMWindow's destructor won't be able to unregister itself with the corresponding DeviceOrientationController, leaving behind a stale pointer.

### cl...@gmail.com (2013-07-14)

Thanks Inferno. Please credit "cloudfuzzer"

### dc...@chromium.org (2013-07-15)

[Empty comment from Monorail migration]

### dc...@chromium.org (2013-07-15)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-07-17)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=154359

------------------------------------------------------------------------
r154359 | dcheng@chromium.org | 2013-07-17T03:48:27.527989Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/page/DOMWindow.cpp?r1=154359&r2=154358&pathrev=154359

Remove device orientation listeners in DOMWindow::willDetachPage

Since DeviceOrientationController is a Page supplement, make sure to
unregister any listeners if the page is going to be detached. Otherwise,
it will be too late to do it in DOMWindow's destructor since page() will
already be null.

BUG=260110

Review URL: https://chromiumcodereview.appspot.com/19430002
------------------------------------------------------------------------

### in...@chromium.org (2013-07-17)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-07-19)

ClusterFuzz has detected this issue as fixed in range 212017:212182.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4962809746030592

Uploader: inferno@chromium.org

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x613000050dc8
Crash State:
  - crash stack -
  WebCore::copyKeysToReferencingVector
  WebCore::DeviceController::dispatchDeviceEvent
  - free stack -
  v8::internal::GlobalHandles::Node::PostGarbageCollectionProcessing
  v8::internal::GlobalHandles::PostGarbageCollectionProcessing
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=204670:204818
Fixed: https://cluster-fuzz.appspot.com/revisions?range=212017:212182

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv97GcY9ovtUye24C8oHbwf2QQCHpt-Fc7ZXdZOhOn6Dze0M0KgHp-ke8-piQSPPxnG5c3A0g-UGwDuh8418J8pEQonHzyJ4os_fmHP5ksMe4-3xhtF69h7H14pOXhsxqyNf3vUEDPt9_nax4-oLKuGHyC9Yf4A

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### bu...@chromium.org (2013-07-31)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=155204

------------------------------------------------------------------------
r155204 | cevans@chromium.org | 2013-07-31T02:24:41.496825Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/branches/chromium/1547/Source/core/page/DOMWindow.cpp?r1=155204&r2=155203&pathrev=155204

Merge 154359 "Remove device orientation listeners in DOMWindow::..."

> Remove device orientation listeners in DOMWindow::willDetachPage
> 
> Since DeviceOrientationController is a Page supplement, make sure to
> unregister any listeners if the page is going to be detached. Otherwise,
> it will be too late to do it in DOMWindow's destructor since page() will
> already be null.
> 
> BUG=260110
> 
> Review URL: https://chromiumcodereview.appspot.com/19430002

TBR=dcheng@chromium.org

Review URL: https://codereview.chromium.org/21043004
------------------------------------------------------------------------

### sc...@gmail.com (2013-07-31)

M29: http://src.chromium.org/viewvc/blink?view=rev&rev=155204

### sc...@gmail.com (2013-08-11)

Nice regression catch, $1000

### pa...@chromium.org (2013-08-19)

Finally kicking off the payment process for this one! Someone should be in contact in the next week (or so) to get your bank information. Thanks again for your help :)

### js...@chromium.org (2013-11-18)

Bulk release of old security bug reports.


### js...@chromium.org (2013-11-18)

Bulk release of old security bug reports.


### ti...@chromium.org (2014-02-28)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/260110?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40077782)*
