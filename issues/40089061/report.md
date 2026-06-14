# URL bar spoof

| Field | Value |
|-------|-------|
| **Issue ID** | [40089061](https://issues.chromium.org/issues/40089061) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | ku...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2011-03-18 |
| **Bounty** | $1,000.00 |

## Description

Test chrome 11.0.696.14 dev windows xp sp3

## Attachments

- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- [stable screen.gif](attachments/stable screen.gif) (image/gif; charset=binary, 746.7 KB)
- [new testcase.zip](attachments/new testcase.zip) (application/zip; charset=binary, 824 B)
- [spoof.htm](attachments/spoof.htm) (text/plain; charset=us-ascii, 391 B)

## Timeline

### ku...@gmail.com (2011-03-18)

[Comment Deleted]

### ku...@gmail.com (2011-03-18)

[Empty comment from Monorail migration]

### ku...@gmail.com (2011-03-18)

Works fine on chrome 10.0.648.151

### js...@chromium.org (2011-03-18)

Confirmed on dev. Didn't have stable handy when I verified.

### ku...@gmail.com (2011-03-19)

New testcase

### js...@chromium.org (2011-03-21)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-03-22)

@mihaip - This looks like another issue with navigation timing. Could you take a look at it?

### mi...@chromium.org (2011-03-22)

Are there instructions on how the test case should be run (were they in https://crbug.com/chromium/76666#c1, which got deleted?)?

(+Charlie, since he's actually done the most work recently in this area)

### js...@chromium.org (2011-03-22)

I just ran the python locally and opened spoof.html from a local webserver on a different port.

### mi...@chromium.org (2011-03-22)

Thanks Justin. Here's a simplified version of spoof.htm (the repeated calls are not necessary).

### lc...@gmail.com (2011-03-22)

Also see bugs 75559 and 75560, which are probably related.

### cr...@chromium.org (2011-03-23)

I think I see what's happening here.  The view-source URL causes us to start a cross-site transition, loading it in a pending RenderViewHost.  When that fails with a 204 error, we aren't cleaning up enough state.  As a result, when the main renderer navigates after the error, RenderViewHost::OnMsgNavigate ignores it because is_waiting_for_unload_ack_ is still true.  Thus, we never call TabContents::DidNavigate and never update the navigation state.

We'll have to do a better job of cleaning up in TabContents::OnDidFailProvisionalLoadWithError.

@lcamtuf, can you CC me on issues 75559 and 75560?  I don't have access to them.

### lc...@gmail.com (2011-03-23)

Done

### js...@chromium.org (2011-03-23)

Not an extensions bug, but adding @aa and @erikkay because it's referenced in an extensions bug.

### bu...@chromium.org (2011-03-25)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=79440

------------------------------------------------------------------------
r79440 | creis@google.com | Fri Mar 25 12:44:19 PDT 2011

Changed paths:
 M http://src.chromium.org/viewvc/chrome/trunk/src/content/browser/renderer_host/render_view_host.h?r1=79440&r2=79439&pathrev=79440
 M http://src.chromium.org/viewvc/chrome/trunk/src/content/browser/renderer_host/resource_dispatcher_host.cc?r1=79440&r2=79439&pathrev=79440
 M http://src.chromium.org/viewvc/chrome/trunk/src/net/tools/testserver/testserver.py?r1=79440&r2=79439&pathrev=79440
 M http://src.chromium.org/viewvc/chrome/trunk/src/content/browser/renderer_host/render_view_host.cc?r1=79440&r2=79439&pathrev=79440
 M http://src.chromium.org/viewvc/chrome/trunk/src/content/browser/renderer_host/render_view_host_manager_browsertest.cc?r1=79440&r2=79439&pathrev=79440

Clean up unload-related state after the ack is received.

BUG=76666
TEST=RenderViewHostManagerTest.ClickLinkAfter204Error

Review URL: http://codereview.chromium.org/6724026
------------------------------------------------------------------------

### cr...@chromium.org (2011-03-25)

Fixed in r79440.

### sc...@gmail.com (2011-03-25)

Thanks Charlie!!
Since this is marked as High severity, I'll take the liberty of marking it WillMerge for M11. I'll take care of the merge next week, once the change has survived the main waterfall for a bit.

Any thoughts on whether this also resolves @lcamtuf's similar bug?

### cr...@chromium.org (2011-03-25)

This CL doesn't change when we start displaying the URL, so unfortunately it doesn't help with https://crbug.com/chromium/75559.  (The fact that this repro used a view-source: URL was just a convenient way to force a cross-site transition from a renderer-initiated navigation.)

Ditto for https://crbug.com/chromium/75560.

### sc...@gmail.com (2011-03-30)

[Empty comment from Monorail migration]

### bu...@chromium.org (2011-03-30)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=79780

------------------------------------------------------------------------
r79780 | cevans@chromium.org | Tue Mar 29 18:07:22 PDT 2011

Changed paths:
 M http://src.chromium.org/viewvc/chrome/branches/696/src/content/browser/renderer_host/resource_dispatcher_host.cc?r1=79780&r2=79779&pathrev=79780
 M http://src.chromium.org/viewvc/chrome/branches/696/src/content/browser/renderer_host/render_view_host.h?r1=79780&r2=79779&pathrev=79780
 M http://src.chromium.org/viewvc/chrome/branches/696/src/net/tools/testserver/testserver.py?r1=79780&r2=79779&pathrev=79780
 M http://src.chromium.org/viewvc/chrome/branches/696/src/content/browser/renderer_host/render_view_host.cc?r1=79780&r2=79779&pathrev=79780
 M http://src.chromium.org/viewvc/chrome/branches/696/src/content/browser/renderer_host/render_view_host_manager_browsertest.cc?r1=79780&r2=79779&pathrev=79780

Merge 79440 - Clean up unload-related state after the ack is received.

BUG=76666
TEST=RenderViewHostManagerTest.ClickLinkAfter204Error

Review URL: http://codereview.chromium.org/6724026

TBR=creis@google.com
Review URL: http://codereview.chromium.org/6777002
------------------------------------------------------------------------

### sc...@gmail.com (2011-04-14)

@kuzzcc: nice spoof bug. Repro demonstrates the issue simply enough; accordingly deserves a $1000 Chromium Security Reward. Congrats!

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

### sc...@gmail.com (2011-04-22)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-05-04)

Invoice finalized; payment is in e-payment system; it can take a couple of weeks.

### js...@chromium.org (2011-10-05)

Batch update.

### js...@chromium.org (2012-04-18)

Lifting view restrictions.

### js...@chromium.org (2012-04-18)

Lifting view restrictions.

### js...@chromium.org (2012-04-18)

[Empty comment from Monorail migration]

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

### aw...@chromium.org (2018-04-26)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-26)

This issue was migrated from crbug.com/chromium/76666?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40089061)*
