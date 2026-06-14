# Tracking bug for ANGLE memory corruption on Windows

| Field | Value |
|-------|-------|
| **Issue ID** | [40092830](https://issues.chromium.org/issues/40092830) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | Unknown |
| **Platforms** | Windows |
| **Reporter** | sc...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2011-07-20 |
| **Bounty** | $1,337.00 |

## Description

https://code.google.com/p/angleproject/source/detail?r=702
(See https://code.google.com/p/angleproject/issues/detail?id=139 for description of code flaw, it's a buffer overflow).

It's in Windows-specific code.

Already merged to M13, just filing for tracking purposes. I'm trying to track down who to credit.

## Timeline

### sc...@gmail.com (2011-07-21)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-08-01)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-08-01)

Regrettably, there are still crashes seen after ANGLE r702
I chatted with Michael Braithwaite, who has come up with a way to reproduce it and proposed additional patch, on https://code.google.com/p/angleproject/issues/detail?id=139

Vangelis / Ken, can we get a careful review and final fix from upstream ANGLE? We'll want to patch the final fix into M13 first patch, in a couple of weeks.

### [Deleted User] (2011-08-04)

Created a branch for Angle starting at rev 705 and merged in angle rev 712 that's supposed to fix the issue.

Need to change the DEPS file in the 835 buildspec to point it to the angle branch.

https://chromereviews.googleplex.com/3133072/

kerz, ok to make the change? 

### la...@google.com (2011-08-04)

[Empty comment from Monorail migration]

### ke...@google.com (2011-08-04)

LGTM

### [Deleted User] (2011-08-04)

DEPS file change committed at rev 16834 .

### ke...@google.com (2011-08-04)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-08-04)

Sorry Kerz, but putting back to Merge-Approved since we intend to merge back to M13.
Changed milestone to M13 to get it off your tracking radar.

### sc...@gmail.com (2011-08-12)

Ok, r712 on ANGLE trunk (on top of r702 trunk) finally fixes this. We confirmed this with M14 dev channel. Merged to M13 for the patch with r726

### sc...@gmail.com (2011-08-16)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-08-16)

@michaelbraithwaite: thanks so much for the heroic effort to finally fix this properly! Crashes in this area seem completely gone with the latest fix applied. The level of support you provided in fixing this bug really impressed the Chromium rewards panel, so we'd like to offer you a $1337 Chromium Security Reward. Congrats!

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

### sc...@gmail.com (2011-08-23)

@michaelbraithwaite: e-mail cevans@chromium.org for steps to collect your reward.

### js...@chromium.org (2011-10-05)

Batch update.

### sc...@gmail.com (2011-10-21)

Reward should now be in payment system... sorry for the delay! Might take a week or two for the wire to finalize.

### [Deleted User] (2012-05-15)

Marking old security bugs Fixed.. 

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-11)

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

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-26)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-26)

This issue was migrated from crbug.com/chromium/89836?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092830)*
