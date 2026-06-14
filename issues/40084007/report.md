# Security: Universal XSS using deferred history loads

| Field | Value |
|-------|-------|
| **Issue ID** | [40084007](https://issues.chromium.org/issues/40084007) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Loader, UI>Browser>Navigation |
| **Reporter** | ma...@gmail.com |
| **Assignee** | dc...@chromium.org |
| **Created** | 2016-04-03 |
| **Bounty** | $7,500.00 |

## Description

**VULNERABILITY DETAILS**  

When a ScopedPageLoadDeferrer is destroyed, the deferring state is updated on the associated pages and loaders. If any history load was set aside during the event loop the deferrer has been protecting, it's processed during the update without checking if navigation is allowed on the frame:

---

## void FrameLoader::setDefersLoading(bool defers) { (...) if (!defers) { if (m\_deferredHistoryLoad) { load(FrameLoadRequest(nullptr, m\_deferredHistoryLoad->m\_request), m\_deferredHistoryLoad->m\_loadType, m\_deferredHistoryLoad->m\_item.get(), m\_deferredHistoryLoad->m\_historyLoadType); m\_deferredHistoryLoad.clear(); } m\_frame->navigationScheduler().startTimer(); scheduleCheckCompleted(); } }

This opens an avenue for an attacker to bypass the FrameNavigationDisabler.

**VERSION**  

Chrome 49.0.2623.110 (Stable)  

Chrome 50.0.2661.57 (Beta)  

Chrome 51.0.2693.2 (Dev)  

Chromium 51.0.2698.0 + Pepper Flash (Release build compiled today)

## Attachments

- [exploit.zip](attachments/exploit.zip) (application/octet-stream, 4.8 KB)

## Timeline

### rs...@chromium.org (2016-04-04)

[Empty comment from Monorail migration]

[Monorail components: Blink>Loader UI>Browser>Navigation]

### dc...@chromium.org (2016-04-04)

japhet@, what do you think about just moving the FrameNavigationDisabler check into FrameLoader::load()? We're just playing whack-a-mole here.

### rs...@chromium.org (2016-04-04)

[Empty comment from Monorail migration]

### ja...@chromium.org (2016-04-04)

I'm willing to try it. Does it pass tests?

### dc...@chromium.org (2016-04-04)

I have no idea if it passes tests, but the only places we instantiate the scoper are before firing XHR abort events when committing a provisional load and inside Document::detach. Both definitely seem like places where we never want to load something.

### dc...@chromium.org (2016-04-05)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-04-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/73563fee12defb21a8f955993b68907169e1ea6d

commit 73563fee12defb21a8f955993b68907169e1ea6d
Author: dcheng <dcheng@chromium.org>
Date: Tue Apr 05 22:39:27 2016

Move isNavigationAllowed() check to main entry point for loads.

Also document the difference between the two types of navigation
disablers and how they should be used.

BUG=600182

Review URL: https://codereview.chromium.org/1858833003

Cr-Commit-Position: refs/heads/master@{#385306}

[modify] https://crrev.com/73563fee12defb21a8f955993b68907169e1ea6d/third_party/WebKit/Source/core/frame/LocalFrame.cpp
[modify] https://crrev.com/73563fee12defb21a8f955993b68907169e1ea6d/third_party/WebKit/Source/core/loader/FrameLoader.cpp
[modify] https://crrev.com/73563fee12defb21a8f955993b68907169e1ea6d/third_party/WebKit/Source/core/loader/NavigationScheduler.cpp


### dc...@chromium.org (2016-04-05)

We should probably merge this, but I know there's some concerns due to the fix just landing today. I'll apply the merge request labels anyway and let people figure it out.

### ss...@google.com (2016-04-05)

timwillis@, what would you like to do about this merge? I leave this one up to you, since you understand the issue better than me. Please let govind@ know so she can trigger a RC.

### go...@chromium.org (2016-04-05)

Adding timwillis@ to the bug.

### dc...@chromium.org (2016-04-05)

OK, I just talked with timwillis@. We'll just merge this to M50. Merging this to M49 is too uncomfortably exciting.

### go...@chromium.org (2016-04-05)

Thank you dcheng@ and timwillis@.

### cl...@chromium.org (2016-04-06)

[Empty comment from Monorail migration]

### ti...@google.com (2016-04-06)

[Automated comment] Less than 2 weeks to go before stable on M50, manual review required.

### ti...@google.com (2016-04-07)

Merge approved for M50 (branch 2661). Pls go ahead merge.

### go...@chromium.org (2016-04-07)

Please merge your change to M50 branch 2661 by 5:00 PM PST on April 8th,Friday to make into the desktop Stable final build cut. Thank you.

### bu...@chromium.org (2016-04-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/a3a744f56382c972e1627fe9ee03fbcab4923582

commit a3a744f56382c972e1627fe9ee03fbcab4923582
Author: Daniel Cheng <dcheng@chromium.org>
Date: Thu Apr 07 22:50:15 2016

Move isNavigationAllowed() check to main entry point for loads.

Also document the difference between the two types of navigation
disablers and how they should be used.

BUG=600182

Review URL: https://codereview.chromium.org/1858833003

Cr-Commit-Position: refs/heads/master@{#385306}
(cherry picked from commit 73563fee12defb21a8f955993b68907169e1ea6d)

Review URL: https://codereview.chromium.org/1873583002 .

Cr-Commit-Position: refs/branch-heads/2661@{#514}
Cr-Branched-From: ef6f6ae5e4c96622286b563658d5cd62a6cf1197-refs/heads/master@{#378081}

[modify] https://crrev.com/a3a744f56382c972e1627fe9ee03fbcab4923582/third_party/WebKit/Source/core/frame/LocalFrame.cpp
[modify] https://crrev.com/a3a744f56382c972e1627fe9ee03fbcab4923582/third_party/WebKit/Source/core/loader/FrameLoader.cpp
[modify] https://crrev.com/a3a744f56382c972e1627fe9ee03fbcab4923582/third_party/WebKit/Source/core/loader/NavigationScheduler.cpp


### ti...@google.com (2016-05-23)

[Empty comment from Monorail migration]

### ti...@google.com (2016-05-25)

I feel a little like Captain Obvious, so why not let him explain it? 
https://media.giphy.com/media/3o7abGogJwT2eHXDKE/giphy.gif

I'll add it to your tab :)

### ti...@google.com (2016-06-17)

[Empty comment from Monorail migration]

### ti...@google.com (2016-06-17)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-07-13)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

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

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/600182?no_tracker_redirect=1

[Multiple monorail components: Blink>Loader, UI>Browser>Navigation]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084007)*
