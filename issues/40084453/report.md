# Security: Universal XSS using a ScopedPageLoadDeferrer bypass

| Field | Value |
|-------|-------|
| **Issue ID** | [40084453](https://issues.chromium.org/issues/40084453) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ma...@gmail.com |
| **Assignee** | ki...@chromium.org |
| **Created** | 2016-06-02 |
| **Bounty** | $8,000.00 |

## Description

**VULNERABILITY DETAILS**  

This is an architectural problem with the implementation of ScopedPageLoadDeferrer. Basically, it works by marking pages as deferred at the time a deferrer is instantiated. The issue is that pages created past this point don't defer loads by default. An attacker can move an iframe across the deferral boundary, which allows synchronous cross-origin navigations in unexpected circumstances.

**VERSION**  

Chrome 51.0.2704.79 (Stable)  

Chrome 51.0.2704.63 (Beta)  

Chrome 52.0.2743.19 (Dev)  

Chromium 53.0.2757.0 (Release build compiled today)

## Attachments

- [exploit.zip](attachments/exploit.zip) (application/octet-stream, 2.5 KB)

## Timeline

### ma...@gmail.com (2016-06-02)

I was thinking about 2 alternative solutions:

1. Make new ordinary pages inherit the deferral state from the opener frame's page. Unfortunately, that'd also require updating |m_deferredFrames| on a ScopedPageLoadDeferrer to ensure that new pages are marked as non-deferred later when the deferrer is destroyed. That'd probably require making the class more static, and I'm not sure how to reconcile that with multiple deferrers on the stack. Meh.
2. Ban creating new windows from frames belonging to deferred pages. Popping new pages from behind a modal dialog is a somewhat shady concept, and this is a very simple solution, so if it doesn't break anything, I'd go for it.

I've made an attempt at implementing #2 in https://codereview.chromium.org/2035973002.

### fe...@chromium.org (2016-06-03)

Thanks for the report, and the start on a patch!

### fe...@chromium.org (2016-06-03)

dcheng@, would you be a good owner for this? If so, PTAL?

### fe...@chromium.org (2016-06-03)

or perhaps tasak@, i see you have recently done work in core/page?

[Monorail components: Blink]

### dc...@chromium.org (2016-06-03)

Nooooooooo. kinuko@, can someone from the Tokyo loading team investigate this so we can distribute the load for these bugs?

japhet@ or I will be happy to review any changes.

### ja...@chromium.org (2016-06-03)

As a matter of cleanup, we probably should make the deferred loading flag a per-process flag instead of a per-page flag. That wouldn't stop about:blank navigations during load deferral, though I think it would stop data: urls?

### ma...@gmail.com (2016-06-03)

I was thinking about this, but then I noticed the constructor takes an excluded page as a parameter and I concluded a more fine-grained control over the deferral state might be desirable for some reason(s). data: URIs are loaded asynchronously, so they're subject to deferral, yes.

### ja...@chromium.org (2016-06-03)

I don't think we actually ever set an exclusion page (probably vestigial from the WebKit era), so that hopefully isn't a limiting factor.

### ki...@chromium.org (2016-06-06)

 :( cc-ing some folks who might be able to investigate it a little further

### ki...@chromium.org (2016-06-09)

I feel we could probably land both? Marius's patch seems to work but also feels very specific so I'm afraid there could potentially be other similar issues, while changing like Nate suggests might need to touch a lot more files (as well as might be a bit controversial) and may take a little more time.

### ja...@chromium.org (2016-06-09)

Yeah, I think it makes sense to land Marius's patch, then do my idea separately.

### sh...@chromium.org (2016-06-23)

kinuko: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pa...@chromium.org (2016-07-01)

We have a fix and it is LGTM'd. This is a High severity bug; is there any reason not to land the fix?

I suggest we land it ASAP and merge it back into 52. It's a simple patch so it should be a clean merge.

### ki...@chromium.org (2016-07-04)

The band-aid fix by marius is LGTM'ed about 2~3 weeks ago but looks like it's not landed yet-- let me just try CQ now.

### bu...@chromium.org (2016-07-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/25a8ae78165cd8725465d26e02a342d7121c42f4

commit 25a8ae78165cd8725465d26e02a342d7121c42f4
Author: marius.mlynski <marius.mlynski@gmail.com>
Date: Mon Jul 04 06:24:56 2016

Don't allow deferred frames to create new windows.

New pages never defer loads, which makes it difficult for ScopedPageLoadDeferrer
to protect against synchronous loads.

This patch adds a check in ChromeClientImpl::createWindow.

BUG=616907

Review-Url: https://codereview.chromium.org/2035973002
Cr-Commit-Position: refs/heads/master@{#403640}

[modify] https://crrev.com/25a8ae78165cd8725465d26e02a342d7121c42f4/third_party/WebKit/Source/web/ChromeClientImpl.cpp
[modify] https://crrev.com/25a8ae78165cd8725465d26e02a342d7121c42f4/third_party/WebKit/Source/web/tests/ChromeClientImplTest.cpp


### ki...@chromium.org (2016-07-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-07-04)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-07-05)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-07-14)

[Empty comment from Monorail migration]

### go...@chromium.org (2016-07-14)

Before we approve merge to M52, Could you please confirm whether this change is baked/verified in Canary and safe to merge?

### go...@chromium.org (2016-07-15)

[Comment Deleted]

### go...@chromium.org (2016-07-15)

+awhalley@, can we take this in for M52 release next week?

### aw...@chromium.org (2016-07-15)

OK for M52.

### go...@chromium.org (2016-07-15)

Approving merge to M52 branch 2743 based on https://crbug.com/chromium/616907#c23. Please merge ASAP or latest by 4:00 PM PST on Monday, 07/18 so we can take it for next week M52 Stable promotion release.

Also does this require a merge to M53 as well?

### aw...@chromium.org (2016-07-15)

+govind@ yes, also needed for M53

### go...@chromium.org (2016-07-15)

Approving merge to M53 branch 2785. Please merge ASAP or latest by 4:00 PM PST on Monday, 07/18. Thank you.

### bu...@chromium.org (2016-07-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/cbe0b97d5cf56f8eaab3b2fc57b925c69d8f7aa0

commit cbe0b97d5cf56f8eaab3b2fc57b925c69d8f7aa0
Author: Kinuko Yasuda <kinuko@chromium.org>
Date: Sun Jul 17 10:12:01 2016

Don't allow deferred frames to create new windows.

New pages never defer loads, which makes it difficult for ScopedPageLoadDeferrer
to protect against synchronous loads.

This patch adds a check in ChromeClientImpl::createWindow.

BUG=616907

Review-Url: https://codereview.chromium.org/2035973002
Cr-Commit-Position: refs/heads/master@{#403640}
(cherry picked from commit 25a8ae78165cd8725465d26e02a342d7121c42f4)

Review URL: https://codereview.chromium.org/2160473002 .

Cr-Commit-Position: refs/branch-heads/2743@{#658}
Cr-Branched-From: 2b3ae3b8090361f8af5a611712fc1a5ab2de53cb-refs/heads/master@{#394939}

[modify] https://crrev.com/cbe0b97d5cf56f8eaab3b2fc57b925c69d8f7aa0/third_party/WebKit/Source/web/ChromeClientImpl.cpp
[modify] https://crrev.com/cbe0b97d5cf56f8eaab3b2fc57b925c69d8f7aa0/third_party/WebKit/Source/web/tests/ChromeClientImplTest.cpp


### bu...@chromium.org (2016-07-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/65422dba656b2dc51c4a36e6398d5391ae9ef120

commit 65422dba656b2dc51c4a36e6398d5391ae9ef120
Author: Kinuko Yasuda <kinuko@chromium.org>
Date: Sun Jul 17 10:24:16 2016

Don't allow deferred frames to create new windows.

New pages never defer loads, which makes it difficult for ScopedPageLoadDeferrer
to protect against synchronous loads.

This patch adds a check in ChromeClientImpl::createWindow.

BUG=616907

Review-Url: https://codereview.chromium.org/2035973002
Cr-Commit-Position: refs/heads/master@{#403640}
(cherry picked from commit 25a8ae78165cd8725465d26e02a342d7121c42f4)

Review URL: https://codereview.chromium.org/2159643002 .

Cr-Commit-Position: refs/branch-heads/2785@{#172}
Cr-Branched-From: 68623971be0cfc492a2cb0427d7f478e7b214c24-refs/heads/master@{#403382}

[modify] https://crrev.com/65422dba656b2dc51c4a36e6398d5391ae9ef120/third_party/WebKit/Source/web/ChromeClientImpl.cpp
[modify] https://crrev.com/65422dba656b2dc51c4a36e6398d5391ae9ef120/third_party/WebKit/Source/web/tests/ChromeClientImplTest.cpp


### ki...@chromium.org (2016-07-17)

Merged to M52 and M53.

### ma...@gmail.com (2016-07-17)

Not sure if tests are compiled for beta/stable, but ChromeClientImplTest.cpp may fail due to a mismatch of arguments provided to WebView::create:

https://chromium.googlesource.com/chromium/src.git/+/52.0.2743.79/third_party/WebKit/Source/web/WebViewImpl.cpp#332

### ki...@chromium.org (2016-07-17)

Thanks for the heads-up. We don't seem building webkit_unit_tests for Beta/Stable, but will be watching alerts.

### bu...@chromium.org (2016-07-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/fdaa78ddc7867123001e1c91e79f1f0e830b7e69

commit fdaa78ddc7867123001e1c91e79f1f0e830b7e69
Author: Kinuko Yasuda <kinuko@chromium.org>
Date: Mon Jul 18 15:12:13 2016

Fix build failure for the broken merge on M52/M53 tree

BUG=628975, 616907
TBR=govind@chromium.org

Review URL: https://codereview.chromium.org/2162463002 .

Cr-Commit-Position: refs/branch-heads/2743@{#661}
Cr-Branched-From: 2b3ae3b8090361f8af5a611712fc1a5ab2de53cb-refs/heads/master@{#394939}

[modify] https://crrev.com/fdaa78ddc7867123001e1c91e79f1f0e830b7e69/third_party/WebKit/Source/web/tests/ChromeClientImplTest.cpp


### aw...@chromium.org (2016-07-19)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-07-25)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-07-25)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-07-25)

Nice - $8,000 for this one, Marius.

### aw...@chromium.org (2016-07-25)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-08-31)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-10)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/616907?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084453)*
