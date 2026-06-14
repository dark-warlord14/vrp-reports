# URL Bar Spoof

| Field | Value |
|-------|-------|
| **Issue ID** | [40089322](https://issues.chromium.org/issues/40089322) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | ku...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2011-03-26 |
| **Bounty** | $1,000.00 |

## Description

Test chrome 12.0.712.0 dev windows xp sp3

1,Open testcase.htm
2,Click 'clickme'



## Attachments

- deleted (application/octet-stream, 0 B)
- [testcase.htm](attachments/testcase.htm) (text/plain; charset=us-ascii, 408 B)

## Timeline

### in...@chromium.org (2011-03-30)

hits this assert 

/*
 There is a race condition between the layout and load completion that affects restoring the scroll position.
 We try to restore the scroll position at both the first layout and upon load completion.
 
 1) If first layout happens before the load completes, we want to restore the scroll position then so that the
 first time we draw the page is already scrolled to the right place, instead of starting at the top and later
 jumping down.  It is possible that the old scroll position is past the part of the doc laid out so far, in
 which case the restore silent fails and we will fix it in when we try to restore on doc completion.
 2) If the layout happens after the load completes, the attempt to restore at load completion time silently
 fails.  We then successfully restore it when the layout happens.
*/
void HistoryController::restoreScrollPositionAndViewState()
{
    if (!m_frame->loader()->stateMachine()->committedFirstRealDocumentLoad())
        return;

    ASSERT(m_currentItem);

Charlie, it would be great if you add this to your bunch of url spoof bugs.

### cr...@chromium.org (2011-03-31)

Sure, I'll take a look early next week when I get back in town.  CC'ing Mihai just as a heads up, since that's in HistoryController.

### cr...@chromium.org (2011-04-06)

There's a strange WebKit bug at the heart of this.  Turns out the following code does the wrong thing:
w = window.open(any_url);
w.document.write(1);
w.location.reload();

Instead of reloading any_url, we put the contents of the *opener* window in w.  I've filed http://webkit.org/b/57906 to track it.

The HistoryController crash in https://crbug.com/chromium/77507#c1 is somewhat of a red herring.  It's already being discussed at http://webkit.org/b/50331.

### cr...@chromium.org (2011-04-06)

Hmm, it turns out the behavior described in https://crbug.com/chromium/77507#c3 is intentional.  Adam points out that the document.write call causes the opener window to take over the new window, giving the new window its URL and security context.

That means we need to fix the aftermath of this situation.

1) NavigationController is currently ignoring the FrameNavigate message for the reload because it arrives with a page ID of -1.  Either we need to give it a valid page ID in the renderer or we need to stop ignoring it in NavigationController.  I'm trying to understand which is the right approach.

2) We may want to consider also sending a FrameNavigate message from the renderer after a document.write call.  This is how Firefox behaves-- it updates the URL bar immediately after the document.write call to show the URL of the calling page.

### ku...@gmail.com (2011-04-07)

[Comment Deleted]

### cr...@chromium.org (2011-04-08)

Re: https://crbug.com/chromium/77507#c5, yes, both test cases are due to the same bug.  Both set up a cross-process navigation and interrupt it with a navigation from the original renderer process.  (The test case attached here uses window.open() and w.opener=null, and the test case from 78384 uses view-source:.  Both result in the navigation happening in a separate renderer process.)

The tricky part about this bug is that the reload happens on a "page" without a NavigationEntry-- essentially on the about:blank page that we typically discard after the first successful navigation in the tab.  As a result, the FrameNavigate message has a page_id of -1, which causes NavigationController to ignore it.  I don't think we want to give it a page_id, because we intentionally don't keep this "page" in the browser history if you navigate away.

I'm working on a CL that tries to cancel the pending entry and refresh the URL bar if something like this happens, but it may need some more work.

### bu...@chromium.org (2011-04-12)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=81307

------------------------------------------------------------------------
r81307 | creis@chromium.org | Tue Apr 12 14:17:49 PDT 2011

Changed paths:
 M http://src.chromium.org/viewvc/chrome/trunk/src/content/browser/tab_contents/navigation_controller.cc?r1=81307&r2=81306&pathrev=81307
 M http://src.chromium.org/viewvc/chrome/trunk/src/content/browser/tab_contents/navigation_controller_unittest.cc?r1=81307&r2=81306&pathrev=81307

Ensure URL is updated after a cross-site navigation is pre-empted by
an "ignored" navigation.

BUG=77507
TEST=NavigationControllerTest.LoadURL_IgnorePreemptsPending

Review URL: http://codereview.chromium.org/6826015
------------------------------------------------------------------------

### cr...@chromium.org (2011-04-12)

Fixed in r81307.

### sc...@gmail.com (2011-04-13)

Thanks Charlie! We'll merge to M11.

### sc...@gmail.com (2011-04-15)

Merged to M11 at r81791

### bu...@chromium.org (2011-04-15)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=81791

------------------------------------------------------------------------
r81791 | cevans@chromium.org | Fri Apr 15 13:16:15 PDT 2011

Changed paths:
 M http://src.chromium.org/viewvc/chrome/branches/696/src/content/browser/tab_contents/navigation_controller_unittest.cc?r1=81791&r2=81790&pathrev=81791
 M http://src.chromium.org/viewvc/chrome/branches/696/src/content/browser/tab_contents/navigation_controller.cc?r1=81791&r2=81790&pathrev=81791

Merge 81307 - Ensure URL is updated after a cross-site navigation is pre-empted by
an "ignored" navigation.

BUG=77507
TEST=NavigationControllerTest.LoadURL_IgnorePreemptsPending

Review URL: http://codereview.chromium.org/6826015

TBR=creis@chromium.org
Review URL: http://codereview.chromium.org/6865026
------------------------------------------------------------------------

### sc...@gmail.com (2011-04-19)

@kuzzcc: another URL bar spoof, and to our surprise, a different root cause (and code change)! Also, a nice simple test case. Therefore we're rewarding this provisionally at the $1000 level for a Chromium Security Reward -- nice one!

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

This issue was migrated from crbug.com/chromium/77507?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/78384]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40089322)*
