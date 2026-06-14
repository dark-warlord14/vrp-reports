# Heap-buffer-overflow in autofill::AutofillPopupControllerImpl::UpdateDataListValues

| Field | Value |
|-------|-------|
| **Issue ID** | [40077807](https://issues.chromium.org/issues/40077807) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Reporter** | cl...@chromium.org |
| **Assignee** | cs...@chromium.org |
| **Created** | 2013-07-19 |
| **Bounty** | $1,000.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6682058713726976

Fuzzer: Miaubiz_css_fuzzer

Crash Type: Heap-buffer-overflow READ 8
Crash Address: 0x6030001f48c8
Crash State:
  - crash stack -
  autofill::AutofillPopupControllerImpl::UpdateDataListValues
  autofill::AutofillDriverImpl::OnMessageReceived
  non-virtual thunk to autofill::AutofillDriverImpl::OnMessageReceived
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=212371:212425

Minimized Testcase (0.64 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95Ejah15TTMFXzZOvNl03VbiCY2-FMD4ieiPUAXRslLityXirl2IENm6KOZDpwOGLQHQ4qycZgrjy8Rc1RlAx9N6L2Mp2SHKFGe9Np9E3aVfJeFOF5G7wQlBjeyD7Qioe_Sxg4XHvy_DVdelYUQ546VlQ9m5A

Additional requirements: Requires Interaction Gestures

## Timeline

### in...@chromium.org (2013-07-19)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-07-19)

[Empty comment from Monorail migration]

### cs...@chromium.org (2013-07-19)

Fix out for review, https://codereview.chromium.org/19809002/

### cs...@chromium.org (2013-07-19)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-07-20)

------------------------------------------------------------------------
r212702 | csharp@chromium.org | 2013-07-20T00:09:00.564483Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/ui/autofill/autofill_popup_controller_impl.cc?r1=212702&r2=212701&pathrev=212702
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/ui/autofill/autofill_popup_controller_unittest.cc?r1=212702&r2=212701&pathrev=212702

[Autofill] Fix UpdateDataListValues to handle Data List only Popups

The UpdateDataListValues function was incorrectly assuming that there
would be non-data list values in the popup whenever it was called,
but it is entirely possible for a popup to only contain data list
values.

R=isherman@chromium.org
BUG=261898

Review URL: https://chromiumcodereview.appspot.com/19809002
------------------------------------------------------------------------

### in...@chromium.org (2013-07-20)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-07-20)

------------------------------------------------------------------------
r212712 | jamesr@chromium.org | 2013-07-20T01:21:03.446749Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/ui/autofill/autofill_popup_controller_unittest.cc?r1=212712&r2=212711&pathrev=212712
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/ui/autofill/autofill_popup_controller_impl.cc?r1=212712&r2=212711&pathrev=212712

Revert 212702 "[Autofill] Fix UpdateDataListValues to handle Dat..."

> [Autofill] Fix UpdateDataListValues to handle Data List only Popups
> 
> The UpdateDataListValues function was incorrectly assuming that there
> would be non-data list values in the popup whenever it was called,
> but it is entirely possible for a popup to only contain data list
> values.
> 
> R=isherman@chromium.org
> BUG=261898
> 
> Review URL: https://chromiumcodereview.appspot.com/19809002

TBR=csharp@chromium.org

Review URL: https://codereview.chromium.org/19511005
------------------------------------------------------------------------

### in...@chromium.org (2013-07-20)

The security regression fix was reverted :(

### ja...@chromium.org (2013-07-20)

D'oh!  According to the win bots the test added in the fix was doing an out-of-bounds vector access :/

### bu...@chromium.org (2013-07-22)

------------------------------------------------------------------------
r212902 | csharp@chromium.org | 2013-07-22T17:17:10.782534Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/ui/autofill/autofill_popup_controller_unittest.cc?r1=212902&r2=212901&pathrev=212902
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/ui/autofill/autofill_popup_controller_impl.cc?r1=212902&r2=212901&pathrev=212902

[Autofill] Fix UpdateDataListValues to handle Data List only Popups

The UpdateDataListValues function was incorrectly assuming that there
would be non-data list values in the popup whenever it was called,
but it is entirely possible for a popup to only contain data list
values.

TBR=isherman@chromium.org
BUG=261898

Review URL: https://chromiumcodereview.appspot.com/19550009
------------------------------------------------------------------------

### in...@chromium.org (2013-07-22)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-07-23)

ClusterFuzz has detected this issue as fixed in range 212899:212906.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6682058713726976

Fuzzer: Miaubiz_css_fuzzer

Crash Type: Heap-buffer-overflow READ 8
Crash Address: 0x6030001f48c8
Crash State:
  - crash stack -
  autofill::AutofillPopupControllerImpl::UpdateDataListValues
  autofill::AutofillDriverImpl::OnMessageReceived
  non-virtual thunk to autofill::AutofillDriverImpl::OnMessageReceived
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=212371:212425
Fixed: https://cluster-fuzz.appspot.com/revisions?range=212899:212906

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv95Ejah15TTMFXzZOvNl03VbiCY2-FMD4ieiPUAXRslLityXirl2IENm6KOZDpwOGLQHQ4qycZgrjy8Rc1RlAx9N6L2Mp2SHKFGe9Np9E3aVfJeFOF5G7wQlBjeyD7Qioe_Sxg4XHvy_DVdelYUQ546VlQ9m5A

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### sc...@gmail.com (2013-08-11)

(Removed what looks like an incorrect Release-0 label)

$1000 for the bug.

### pa...@chromium.org (2013-08-20)

[Empty comment from Monorail migration]

### js...@chromium.org (2013-11-18)

Bulk release of old security bug reports.


### js...@chromium.org (2013-11-18)

Bulk release of old security bug reports.


### sh...@chromium.org (2016-06-22)

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

This issue was migrated from crbug.com/chromium/261898?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/263041]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40077807)*
