# Security: H.264 scaling list parsing overflow

| Field | Value |
|-------|-------|
| **Issue ID** | [40077097](https://issues.chromium.org/issues/40077097) |
| **Status** | New |
| **Severity** | S4-Minimal |
| **Priority** | P4 |
| **Component** | Unknown |
| **Platforms** | Linux, ChromeOS |
| **Reporter** | jo...@chromium.org |
| **Assignee** | po...@chromium.org |
| **Created** | 2013-03-08 |
| **Bounty** | $40,000.00 |

## Description

In content/common/gpu/media/h264_parser.cc:

res = ParseScalingList(sizeof(sps->scaling_list4x4[i]),
                       sps->scaling_list4x4[i], &use_default);

sizeof(sps->scaling_list4x4[i]) is used in that function as a count of
int-sized elements, causing an overflow.

## Timeline

### bu...@chromium.org (2013-03-08)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=186899

------------------------------------------------------------------------
r186899 | jln@chromium.org | 2013-03-08T05:42:38.462039Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/content/common/gpu/media/h264_parser.cc?r1=186899&r2=186898&pathrev=186899

Fix GPU overflow


BUG=181083

Review URL: https://chromiumcodereview.appspot.com/12593006
------------------------------------------------------------------------

### po...@chromium.org (2013-03-08)

[Empty comment from Monorail migration]

### be...@chromium.org (2013-03-08)

Pwnium fix - approved for 25 and 26.  Danielle - blame me in the event of epic fail.

### bu...@chromium.org (2013-03-08)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=186904

------------------------------------------------------------------------
r186904 | posciak@google.com | 2013-03-08T06:44:59.605739Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/1364/src/content/common/gpu/media/h264_parser.cc?r1=186904&r2=186903&pathrev=186904

Merge 186899
> Fix GPU overflow
> 
> 
> BUG=181083
> 
> Review URL: https://chromiumcodereview.appspot.com/12593006

TBR=jln@chromium.org
Review URL: https://codereview.chromium.org/12558010
------------------------------------------------------------------------

### bu...@chromium.org (2013-03-08)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=186903

------------------------------------------------------------------------
r186903 | posciak@google.com | 2013-03-08T06:43:04.918819Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/1364_152/src/content/common/gpu/media/h264_parser.cc?r1=186903&r2=186902&pathrev=186903

Merge 186899
> Fix GPU overflow
> 
> 
> BUG=181083
> 
> Review URL: https://chromiumcodereview.appspot.com/12593006

TBR=jln@chromium.org
Review URL: https://codereview.chromium.org/12536005
------------------------------------------------------------------------

### bu...@chromium.org (2013-03-08)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=186905

------------------------------------------------------------------------
r186905 | posciak@google.com | 2013-03-08T06:46:46.929313Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/1410/src/content/common/gpu/media/h264_parser.cc?r1=186905&r2=186904&pathrev=186905

Merge 186899
> Fix GPU overflow
> 
> 
> BUG=181083
> 
> Review URL: https://chromiumcodereview.appspot.com/12593006

TBR=jln@chromium.org
Review URL: https://codereview.chromium.org/12682002
------------------------------------------------------------------------

### po...@chromium.org (2013-03-08)

[Empty comment from Monorail migration]

### jo...@chromium.org (2013-03-08)

[Empty comment from Monorail migration]

### jo...@chromium.org (2013-03-08)

Thanks Stéphane for CQ'ing and Pawel for the merges!

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-14)

For lack of a better place to put it, we'll tag Pinkie's overall $40,000 reward here, for the Pwnium partial.

### jo...@chromium.org (2013-03-15)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-19)

[Empty comment from Monorail migration]

### [Deleted User] (2013-04-02)

[Empty comment from Monorail migration]

### js...@chromium.org (2013-04-11)

Bulk edit for SecurityNotify.

### pa...@chromium.org (2013-04-26)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-06-10)

[Empty comment from Monorail migration]

### js...@chromium.org (2013-11-18)

Bulk release of old security bug reports.


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

### ti...@chromium.org (2023-07-07)

[Empty comment from Monorail migration]

### is...@google.com (2023-07-07)

This issue was migrated from crbug.com/chromium/181083?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40077097)*
