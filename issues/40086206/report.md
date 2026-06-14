# Freeing invalid uninitialized pointer to bug_report_ object

| Field | Value |
|-------|-------|
| **Issue ID** | [40086206](https://issues.chromium.org/issues/40086206) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals |
| **Reporter** | ku...@gmail.com |
| **Assignee** | in...@chromium.org |
| **Created** | 2010-12-18 |
| **Bounty** | $1,000.00 |

## Description

Test chrome 10.0.612.1 dev windows xp sp3

1,Goto chrome://bugreport/
2,Refresh it or close the tab see crash

## Attachments

- [logout.txt](attachments/logout.txt) (text/x-c++; charset=us-ascii, 4.9 KB)
- [testcase.crx](attachments/testcase.crx) (application/octet-stream; charset=binary, 818 B)

## Timeline

### ku...@gmail.com (2010-12-18)

[Empty comment from Monorail migration]

### ku...@gmail.com (2010-12-18)

[Empty comment from Monorail migration]

### in...@chromium.org (2010-12-20)

Thanks Kuzzcc. Privileged chrome:// urls can be invoked using extensions (thanks for your example) and this invalid write is in the browser process, so i think secseverity-medium should be appropriate. Affects M8 Stable as well.

### in...@chromium.org (2010-12-20)

Patch uploaded for review.

### in...@chromium.org (2010-12-20)

Fixed in r69721. Needs to be merged to both m8, m9.

### in...@chromium.org (2010-12-20)

[Empty comment from Monorail migration]

### bu...@chromium.org (2010-12-20)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=69721

------------------------------------------------------------------------
r69721 | inferno@chromium.org | Mon Dec 20 09:34:11 PST 2010

Changed paths:
 M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/dom_ui/bug_report_ui.cc?r1=69721&r2=69720&pathrev=69721

Initialize bug_report_ to NULL so as make sure invalid pointer is not freed.

BUG=67393
TEST=NONE

Review URL: http://codereview.chromium.org/6066002
------------------------------------------------------------------------

### sc...@gmail.com (2010-12-20)

@kuzzcc: congratulations! We'd like to provisionally reward you a $1000 Chromium Security Reward.
As always, we reward at the higher $1000 level for good quality reports. In this case, we liked:
- The nice stack trace and exception record.
- A nice simple, small extension to demonstrate the bug.

If it's easy, can you also test your repros against the latest stable version of Chrome? This helps tell us whether we are looking at a regression or a bug that affects all of our stable users.


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

### rk...@chromium.org (2010-12-20)

Why is the SecSeverity high on this bug?
From what I can see, it's a crash because of an invalid read in the browser process, not sure how that is really exploitable?



### in...@chromium.org (2010-12-20)

@rkc, it is an invalid write in the browser process when trying to delete a invalid bug_report_ pointer. exploitability depends on how and when the url is initiated by the attacker using extensions.

BugReportHandler::~BugReportHandler() {
  // Just in case we didn't send off bug_report_ to SendReport
  if (bug_report_) {
    // If we're deleting the report object, cancel feedback collection first
    CancelFeedbackCollection();
    delete bug_report_;
  }
}

### ku...@gmail.com (2010-12-21)

chrome stable and chrome dev can't stay together.
so i did't test chrome stable

### ch...@gmail.com (2011-01-04)

merged to m8 as rev 70434

### in...@chromium.org (2011-01-04)

[Empty comment from Monorail migration]

### [Deleted User] (2011-01-04)

[Empty comment from Monorail migration]

### bu...@chromium.org (2011-01-06)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=70434

------------------------------------------------------------------------
r70434 | cdn@google.com | Tue Jan 04 11:53:57 PST 2011

Changed paths:
 M http://src.chromium.org/viewvc/chrome/branches/552/src/chrome/browser/dom_ui/bug_report_ui.cc?r1=70434&r2=70433&pathrev=70434

Merge 69721 - Initialize bug_report_ to NULL so as make sure invalid pointer is not freed.

BUG=67393
TEST=NONE

Review URL: http://codereview.chromium.org/6066002

Review URL: http://codereview.chromium.org/5960009
------------------------------------------------------------------------

### sc...@gmail.com (2011-01-10)

This sounds more like a Medium severity to me. The evil extension has "tabs" permission in the manifest, which is a moderately powerful permission. I expect it needs it to navigate to chrome://bugreport/

### ch...@gmail.com (2011-01-11)

merged to m9 as 71076

### [Deleted User] (2011-01-11)

Works fine with Google Chrome 8.0.552.237 (Official Build 70801) on Windows and Linux.

### sc...@gmail.com (2011-01-18)

Invoice finalized; payment is in e-payment system.

Was fixed in 8.0.552.237

### js...@chromium.org (2011-03-21)

[Empty comment from Monorail migration]

### [Deleted User] (2011-07-30)

[Comment Deleted]

### in...@chromium.org (2011-07-30)

This is medium severity because of the user interaction required. Please don't change security bug labels, esp bug severity levels without consulting with Security Team.

### js...@chromium.org (2011-10-05)

Batch update.

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### as...@chromium.org (2014-06-17)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### rk...@chromium.org (2019-05-07)

[Empty comment from Monorail migration]

### yu...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-06)

This issue was migrated from crbug.com/chromium/67393?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40086206)*
