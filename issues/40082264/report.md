# Security: window.history.replaceState fails to enforce domain security

| Field | Value |
|-------|-------|
| **Issue ID** | [40082264](https://issues.chromium.org/issues/40082264) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | mi...@gmail.com |
| **Assignee** | js...@chromium.org |
| **Created** | 2010-07-22 |
| **Bounty** | $1,000.00 |

## Description

The HTML5 spec states, as part of the algorithm for window.history.replaceState:

Compare the resulting absolute URL to the document's address. If any part of these two URLs differ other than the <path>, <query>, and <fragment> components, then raise a SECURITY_ERR exception and abort these steps.

In fact, chromium follows this, throwing the following error:

Error: SECURITY_ERR: DOM Exception 18

However, if the page has a `<base>` tag, with an href set to any arbitrary domain, window.history.replaceState is allowed to change document.location to that arbitary domain, and is updated in the URL bar.

The attached usecase should make it obvious why this is a huge security bug--you can spoof any site *including* the URL.

I can reproduce this in Chromium/Mac 6.0.469.0 (52652), as well as Chrome/Mac 6.0.466.4 dev and Chrome/Mac 5.0.375.99 stable.

Steps to reproduce:

1) Open fakelogin.html either locally or at http://miketaylr.com/test/h4x/fakelogin.html
2) Observe URL or document.location
3) Click the 'Apply Hacks' button in the top bar
4) Observe the URL changing to Gmail's login path, including base domain

5) Enter your Gmail login information and get pwned (don't really do this :P)

It should be noted that this is not possible in the builds of Gecko that support window.history.replaceState, so Chromium/Chrome is the only one vulnerable here.

## Attachments

- [fakelogin.html](attachments/fakelogin.html) (text/x-c++; charset=utf-8, 14.7 KB)

## Timeline

### mi...@gmail.com (2010-07-22)

Also, it should be noted that if you do a view-source on the test document after applying the replaceState, it brings up the Gmail login page source--since apparently it performs an HTTP request of document.location.

### js...@chromium.org (2010-07-22)

I confirmed in stable, trunk and Safari. Seems like this might be a dupe of https://crbug.com/chromium/41435, but the trick with the base tag ups the severity. Taking a look now.


### js...@chromium.org (2010-07-22)

Okay, it's totally unrelated to https://crbug.com/chromium/41435. However, both bugs are in the same place, so I'm just going to knock them out at the same time. I can probably get fixes on both in today.

### in...@chromium.org (2010-07-22)

[Empty comment from Monorail migration]

### js...@chromium.org (2010-07-23)

Fix landed upstream as: http://trac.webkit.org/changeset/63925


### mi...@gmail.com (2010-07-23)

Having had more time to play with this, I've found that window.history.pushState({}, "", "/accounts/ServiceLogin?service=mail") produces the same effect.

Does the current change fix this as well? Should it be its own ticket?

### js...@chromium.org (2010-07-23)

Thanks Mike, but the second case is effectively the same as the first. Relative URLs resolve against the current base URL. By setting the base element you're overriding the current base URL.

### js...@chromium.org (2010-07-23)

[Empty comment from Monorail migration]

### sc...@gmail.com (2010-07-23)

Whoa, Justin did you just fix that in 5hrs? :)

URL bar spoofs are treated as SecSeverity-High; tag updated.

### mi...@gmail.com (2010-07-23)

Thanks for moving so fast on this one. The more I think about it, the more I'm terrified--considering the amount of market share this could be used against.

Nice work.

### sc...@gmail.com (2010-07-23)

@miketaylr: aside from the fast fix, there is more good news :) You've provisionally qualified for a $1000 Chromium Security Reward. As per our recent blog post (http://blog.chromium.org/2010/07/celebrating-six-months-of-chromium.html), we are increasing the reward value above the base $500 because of the very high quality of your report.

In terms of release timeframes, we have a patch release going out next week and this fix will make the next patch after that.

### mi...@gmail.com (2010-07-23)

yay! :D

### js...@chromium.org (2010-07-26)

Had to reland to fix a functional regression: http://trac.webkit.org/changeset/64077

We'll let it hit dev channel and then roll into the next stable update.


### bu...@gmail.com (2010-08-05)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=55077 

------------------------------------------------------------------------
r55077 | inferno@chromium.org | 2010-08-05 09:45:32 -0700 (Thu, 05 Aug 2010) | 29 lines
Changed paths:
   A http://src.chromium.org/viewvc/chrome/branches/WebKit/472/LayoutTests/fast/loader/stateobjects/replacestate-base-illegal-expected.txt
   A http://src.chromium.org/viewvc/chrome/branches/WebKit/472/LayoutTests/fast/loader/stateobjects/replacestate-base-illegal.html
   A http://src.chromium.org/viewvc/chrome/branches/WebKit/472/LayoutTests/fast/loader/stateobjects/replacestate-base-legal-expected.txt
   A http://src.chromium.org/viewvc/chrome/branches/WebKit/472/LayoutTests/fast/loader/stateobjects/replacestate-base-legal.html
   A http://src.chromium.org/viewvc/chrome/branches/WebKit/472/LayoutTests/fast/loader/stateobjects/resources/replacestate-base-pass.html
   M http://src.chromium.org/viewvc/chrome/branches/WebKit/472/WebCore/page/History.cpp?r1=55077&r2=55076

Merge 64077 - 2010-07-26  Justin Schuh  <jschuh@chromium.org>

        Reviewed by Darin Fisher.

        Check history state against origin before setting
        https://bugs.webkit.org/show_bug.cgi?id=42858

        Tests: fast/loader/stateobjects/replacestate-base-illegal.html
               fast/loader/stateobjects/replacestate-base-legal.html

        * page/History.cpp:
        (WebCore::History::urlForState):
        (WebCore::History::stateObjectAdded):
2010-07-26  Justin Schuh  <jschuh@chromium.org>

        Reviewed by Darin Fisher.

        Check history state when base URL is changed
        https://bugs.webkit.org/show_bug.cgi?id=42858

        * fast/loader/stateobjects/replacestate-base-illegal-expected.txt: Added.
        * fast/loader/stateobjects/replacestate-base-illegal.html: Added.
        * fast/loader/stateobjects/replacestate-base-legal-expected.txt: Added.
        * fast/loader/stateobjects/replacestate-base-legal.html: Added.
        * fast/loader/stateobjects/resources/replacestate-base-pass.html: Added.

BUG=49964

Review URL: http://codereview.chromium.org/3017060
------------------------------------------------------------------------


### ch...@gmail.com (2010-08-09)

[Empty comment from Monorail migration]

### sc...@gmail.com (2010-08-17)

This was merged to 375:

http://src.chromium.org/viewvc/chrome?view=rev&revision=55467

Merge 64077 - 2010-07-26  Justin Schuh  <jschuh@chromium.org>

        Reviewed by Darin Fisher.

        Check history state against origin before setting
        https://bugs.webkit.org/show_bug.cgi?id=42858

        Tests: fast/loader/stateobjects/replacestate-base-illegal.html
               fast/loader/stateobjects/replacestate-base-legal.html

        * page/History.cpp:
        (WebCore::History::urlForState):
        (WebCore::History::stateObjectAdded):
2010-07-26  Justin Schuh  <jschuh@chromium.org>

        Reviewed by Darin Fisher.

        Check history state when base URL is changed
        https://bugs.webkit.org/show_bug.cgi?id=42858

        * fast/loader/stateobjects/replacestate-base-illegal-expected.txt: Added.
        * fast/loader/stateobjects/replacestate-base-illegal.html: Added.
        * fast/loader/stateobjects/replacestate-base-legal-expected.txt: Added.
        * fast/loader/stateobjects/replacestate-base-legal.html: Added.
        * fast/loader/stateobjects/resources/replacestate-base-pass.html: Added.


Review URL: http://codereview.chromium.org/3106001

### sc...@gmail.com (2010-08-18)

[Empty comment from Monorail migration]

### [Deleted User] (2010-08-18)

[Empty comment from Monorail migration]

### [Deleted User] (2010-08-18)

The URL doesn't change anymore. Verified in 5.0.375.127 (Official Build 55887).

### [Deleted User] (2010-08-18)

Works fine with Google Chrome 5.0.375.127 (Official Build 55887) on Win XP and Linux Ubuntu 9.04

### [Deleted User] (2010-08-18)

I checked it on Mac :)

### sc...@gmail.com (2010-08-19)

Heya Mike -- the fix is now live for all our users. Thanks for your help.
Since this is your first reward with us, please e-mail cevans@chromium.org for details on how to collect!

### mi...@gmail.com (2010-08-20)

Hey, that's great news! Many thanks to all that helped get this fixed and for making the web a safer place. :)

### sc...@gmail.com (2010-08-31)

Payment is in the electronic system.... keep an eye out for arrival since it's your first payment :) May take a few weeks. Unfortunately, banks are not as fast as the Chrome Security Team.

Thanks again.

### js...@chromium.org (2011-03-21)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-10-05)

Batch update.

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

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/49964?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40082264)*
