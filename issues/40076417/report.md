# Security: Pwnium 2 TCMalloc profile bug

| Field | Value |
|-------|-------|
| **Issue ID** | [40076417](https://issues.chromium.org/issues/40076417) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Reporter** | jo...@chromium.org |
| **Assignee** | mo...@google.com |
| **Created** | 2012-10-10 |
| **Bounty** | $60,000.00 |

## Description

Pwnium 2 TCMalloc profile bug.

## Timeline

### bu...@chromium.org (2012-10-10)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=161037

------------------------------------------------------------------------
r161037 | palmer@chromium.org | 2012-10-10T04:12:42.845339Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/1229/src/chrome/renderer/chrome_render_process_observer.cc?r1=161037&r2=161036&pathrev=161037
   M http://src.chromium.org/viewvc/chrome/branches/1229/src/chrome/renderer/chrome_render_process_observer.h?r1=161037&r2=161036&pathrev=161037
   M http://src.chromium.org/viewvc/chrome/branches/1229/src/chrome/browser/renderer_host/chrome_render_message_filter.cc?r1=161037&r2=161036&pathrev=161037
   M http://src.chromium.org/viewvc/chrome/branches/1229/src/chrome/browser/renderer_host/chrome_render_message_filter.h?r1=161037&r2=161036&pathrev=161037
   M http://src.chromium.org/viewvc/chrome/branches/1229/src/chrome/common/render_messages.h?r1=161037&r2=161036&pathrev=161037

Disable tcmalloc profile files.

BUG=154983
Review URL: https://codereview.chromium.org/11087040
------------------------------------------------------------------------

### bu...@chromium.org (2012-10-10)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=161048

------------------------------------------------------------------------
r161048 | jorgelo@chromium.org | 2012-10-10T05:15:26.513466Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/renderer/chrome_render_process_observer.cc?r1=161048&r2=161047&pathrev=161048
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/renderer/chrome_render_process_observer.h?r1=161048&r2=161047&pathrev=161048
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/renderer_host/chrome_render_message_filter.cc?r1=161048&r2=161047&pathrev=161048
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/renderer_host/chrome_render_message_filter.h?r1=161048&r2=161047&pathrev=161048
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/common/render_messages.h?r1=161048&r2=161047&pathrev=161048

Disable tcmalloc profile files.

BUG=154983
TBR=darin@chromium.org
NOTRY=true

Review URL: https://chromiumcodereview.appspot.com/11087041
------------------------------------------------------------------------

### bu...@chromium.org (2012-10-10)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=161050

------------------------------------------------------------------------
r161050 | kerz@chromium.org | 2012-10-10T05:21:32.439718Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/1229_92/src/chrome/browser/renderer_host/chrome_render_message_filter.h?r1=161050&r2=161049&pathrev=161050
   M http://src.chromium.org/viewvc/chrome/branches/1229_92/src/chrome/common/render_messages.h?r1=161050&r2=161049&pathrev=161050
   M http://src.chromium.org/viewvc/chrome/branches/1229_92/src/chrome/renderer/chrome_render_process_observer.cc?r1=161050&r2=161049&pathrev=161050
   M http://src.chromium.org/viewvc/chrome/branches/1229_92/src/chrome/renderer/chrome_render_process_observer.h?r1=161050&r2=161049&pathrev=161050
   M http://src.chromium.org/viewvc/chrome/branches/1229_92/src/chrome/browser/renderer_host/chrome_render_message_filter.cc?r1=161050&r2=161049&pathrev=161050

Merge 161048 - Disable tcmalloc profile files.

BUG=154983
TBR=darin@chromium.org
NOTRY=true

Review URL: https://chromiumcodereview.appspot.com/11087041

TBR=jorgelo@chromium.org
Review URL: https://codereview.chromium.org/11092041
------------------------------------------------------------------------

### bu...@chromium.org (2012-10-10)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=161051

------------------------------------------------------------------------
r161051 | kerz@chromium.org | 2012-10-10T05:24:06.118692Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/1271/src/chrome/renderer/chrome_render_process_observer.h?r1=161051&r2=161050&pathrev=161051
   M http://src.chromium.org/viewvc/chrome/branches/1271/src/chrome/browser/renderer_host/chrome_render_message_filter.cc?r1=161051&r2=161050&pathrev=161051
   M http://src.chromium.org/viewvc/chrome/branches/1271/src/chrome/browser/renderer_host/chrome_render_message_filter.h?r1=161051&r2=161050&pathrev=161051
   M http://src.chromium.org/viewvc/chrome/branches/1271/src/chrome/common/render_messages.h?r1=161051&r2=161050&pathrev=161051
   M http://src.chromium.org/viewvc/chrome/branches/1271/src/chrome/renderer/chrome_render_process_observer.cc?r1=161051&r2=161050&pathrev=161051

Merge 161048 - Disable tcmalloc profile files.

BUG=154983
TBR=darin@chromium.org
NOTRY=true

Review URL: https://chromiumcodereview.appspot.com/11087041

TBR=jorgelo@chromium.org
Review URL: https://codereview.chromium.org/11094041
------------------------------------------------------------------------

### bu...@chromium.org (2012-10-10)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=161053

------------------------------------------------------------------------
r161053 | kerz@chromium.org | 2012-10-10T05:27:34.321905Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/1180/src/chrome/browser/renderer_host/chrome_render_message_filter.cc?r1=161053&r2=161052&pathrev=161053
   M http://src.chromium.org/viewvc/chrome/branches/1180/src/chrome/browser/renderer_host/chrome_render_message_filter.h?r1=161053&r2=161052&pathrev=161053
   M http://src.chromium.org/viewvc/chrome/branches/1180/src/chrome/common/render_messages.h?r1=161053&r2=161052&pathrev=161053
   M http://src.chromium.org/viewvc/chrome/branches/1180/src/chrome/renderer/chrome_render_process_observer.cc?r1=161053&r2=161052&pathrev=161053
   M http://src.chromium.org/viewvc/chrome/branches/1180/src/chrome/renderer/chrome_render_process_observer.h?r1=161053&r2=161052&pathrev=161053

Merge 161048 - Disable tcmalloc profile files.

BUG=154983
TBR=darin@chromium.org
NOTRY=true

Review URL: https://chromiumcodereview.appspot.com/11087041

TBR=jorgelo@chromium.org
Review URL: https://codereview.chromium.org/11090041
------------------------------------------------------------------------

### sc...@gmail.com (2012-10-10)

[Empty comment from Monorail migration]

### wa...@chromium.org (2012-10-10)

As requested, impact from a CrOS perspective.

Arbitrary file write as user chronos outside of the sandbox allows for signed-in user profile tampering, limited pre-sign-in state tampering, and limited log tampering (for those owned by the signed in user).  This would allow an attacker to replace Bookmarks, Preferences, or another local profile file or files.  Notably, replacing a well-known, pre-installed extension manifest file and associated start file would allow cross-origin bypass leading to data exfiltration and persistence across signed in sessions with updates for that extension disabled.  SecSeverity-High applies to CrOS too even if explicit out-of-sandbox arbitrary code execution is stopped by existing CrOS mitigations.

### sc...@gmail.com (2012-10-11)

[Empty comment from Monorail migration]

### [Deleted User] (2012-10-11)

Verified that this CL made it into the CrOS 2465.209.0 (Chrome 21.0.1180.92) build this morning.

### sc...@gmail.com (2012-10-19)

Payment sent for wire.

### pa...@chromium.org (2012-10-23)

We need to get this merged into Clank, too. As with the SVG one, it should be an easy merge.

### kl...@chromium.org (2012-10-23)

Clank doesn't use TCMalloc.

### pa...@chromium.org (2012-10-23)

Excellent, thanks. :)

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-06-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-29)

[Empty comment from Monorail migration]

### is...@google.com (2018-07-29)

This issue was migrated from crbug.com/chromium/154983?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40076417)*
