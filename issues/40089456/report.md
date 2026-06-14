# Url bar spoof

| Field | Value |
|-------|-------|
| **Issue ID** | [40089456](https://issues.chromium.org/issues/40089456) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Reporter** | ku...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2011-03-31 |
| **Bounty** | $1,000.00 |

## Description

Test chrome 12.0.712.0 dev windows xp sp3 & chromium 12.0.719.0 (79793)

1,Click "clickme"


## Attachments

- [testcase.htm](attachments/testcase.htm) (text/plain; charset=us-ascii, 386 B)

## Timeline

### js...@chromium.org (2011-03-31)

@creis - Adding this to the pile. It may be a dupe of the ones you're looking at.

### in...@chromium.org (2011-04-04)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-04-04)

@inferno - I didn't confirm this before I added the CCs. Did you confirm it before assigning severity and milestone?

### cr...@chromium.org (2011-04-04)

I can confirm it.  It's hitting an assert in FrameLoaderClientImpl::dispatchDidStartProvisionalLoad():

    // If this load is what we expected from a client redirect, treat it as a
    // redirect from that original page. The expected redirect urls will be
    // cleared by DidCancelClientRedirect.
    bool completingClientRedirect = false;
    if (m_expectedClientRedirectSrc.isValid()) {
        // m_expectedClientRedirectDest could be something like
        // "javascript:history.go(-1)" thus we need to exclude url starts with
        // "javascript:". See bug: 1080873
        ASSERT(m_expectedClientRedirectDest.protocolIs("javascript")
            || m_expectedClientRedirectDest == url);


I'm tied up with a few other URL spoof bugs at the moment, but I'll look at it if others don't have time to.

### js...@chromium.org (2011-04-04)

Thanks Charlie.

### in...@chromium.org (2011-04-04)

Thanks Charlie for adding this to your bunch. 

Justin, yeah i did confirm it. Although i don't know if all of these are dupes or similar or whatever :)

### cr...@chromium.org (2011-04-07)

The FrameLoaderClientImpl assert is a red herring.  It's being tracked in http://webkit.org/b/44079.

The real issue here is that NavigationController was classifying the history.back() navigation as a same-page navigation, due to this check in ClassifyNavigation:
  if (pending_entry_ &&
      existing_entry != pending_entry_ &&
      pending_entry_->page_id() == -1) {
    // ...
    return NavigationType::SAME_PAGE;
  }

In this case, the pending entry does have page_id -1, but the existing entry doesn't match the page that's currently showing.  It should be straightforward to check that existing entry is the same as GetLastCommittedEntry before returning SAME_PAGE here.

### bu...@chromium.org (2011-04-08)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=80941

------------------------------------------------------------------------
r80941 | creis@chromium.org | Fri Apr 08 09:27:24 PDT 2011

Changed paths:
 M http://src.chromium.org/viewvc/chrome/trunk/src/content/browser/tab_contents/navigation_controller.cc?r1=80941&r2=80940&pathrev=80941
 M http://src.chromium.org/viewvc/chrome/trunk/src/content/browser/tab_contents/navigation_controller_unittest.cc?r1=80941&r2=80940&pathrev=80941

Fix classification of a history.back() that interrupts a pending navigation.

BUG=78031
TEST=NavigationControllerTest.LoadURL_BackPreemptsPending

Review URL: http://codereview.chromium.org/6801052
------------------------------------------------------------------------

### cr...@chromium.org (2011-04-08)

Fixed in r80941.

### sc...@gmail.com (2011-04-08)

Thanks, Charlie! Does this affect older versions (10 stable, 11 beta?) It affects both merging and release notes.

### sc...@gmail.com (2011-04-08)

Affects M10, M11. I'll merge it to M11.

### sc...@gmail.com (2011-04-08)

Merged to M11 @ r81005

### sc...@gmail.com (2011-04-08)

[Empty comment from Monorail migration]

### bu...@chromium.org (2011-04-08)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=81005

------------------------------------------------------------------------
r81005 | cevans@chromium.org | Fri Apr 08 15:42:38 PDT 2011

Changed paths:
 M http://src.chromium.org/viewvc/chrome/branches/696/src/content/browser/tab_contents/navigation_controller_unittest.cc?r1=81005&r2=81004&pathrev=81005
 M http://src.chromium.org/viewvc/chrome/branches/696/src/content/browser/tab_contents/navigation_controller.cc?r1=81005&r2=81004&pathrev=81005

Merge 80941 - Fix classification of a history.back() that interrupts a pending navigation.

BUG=78031
TEST=NavigationControllerTest.LoadURL_BackPreemptsPending

Review URL: http://codereview.chromium.org/6801052

TBR=creis@chromium.org
Review URL: http://codereview.chromium.org/6826017
------------------------------------------------------------------------

### sc...@gmail.com (2011-04-14)

@kuzzcc - another textbook spoof, thanks! And other provisional $1000 Chromium Security Reward for your help.

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

### bu...@chromium.org (2013-03-11)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

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

This issue was migrated from crbug.com/chromium/78031?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40089456)*
