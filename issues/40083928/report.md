# Security: Universal XSS using a FrameNavigationDisabler bypass

| Field | Value |
|-------|-------|
| **Issue ID** | [40083928](https://issues.chromium.org/issues/40083928) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>Navigation |
| **Reporter** | ma...@gmail.com |
| **Assignee** | dc...@chromium.org |
| **Created** | 2016-03-24 |
| **Bounty** | $7,500.00 |

## Description

**VULNERABILITY DETAILS**  

When a top-level navigation is triggered on a frame displaying the initial empty document, FrameLoader::load is invoked directly:

---

## void LocalFrame::navigate(Document& originDocument, const KURL& url, bool replaceCurrentItem, UserGestureStatus userGestureStatus) { (...) if (isMainFrame() && !m\_loader.stateMachine()->committedFirstRealDocumentLoad()) { FrameLoadRequest request(&originDocument, url); request.resourceRequest().setHasUserGesture(userGestureStatus == UserGestureStatus::Active); m\_loader.load(request); } else { m\_navigationScheduler->scheduleLocationChange(&originDocument, url.getString(), replaceCurrentItem); } }

As a result, FrameNavigationDisabler will fail to prevent the navigation when the URL is loaded synchronously.

**VERSION**  

Chrome 49.0.2623.87 (Stable)  

Chrome 50.0.2661.49 (Beta)  

Chrome 51.0.2687.0 (Dev)  

Chromium 51.0.2690.0 + Pepper Flash (Release build compiled today)

## Attachments

- [exploit.zip](attachments/exploit.zip) (application/octet-stream, 2.6 KB)
- [14rrwu.jpg](attachments/14rrwu.jpg) (image/jpeg, 79.0 KB)

## Timeline

### wf...@chromium.org (2016-03-24)

Looks like something happening in navigation here, but I can't get the attached exploit to actually trigger. dcheng - Can you take a look?

[Monorail components: UI>Browser>Navigation]

### dc...@chromium.org (2016-03-24)

I'm unable to repro the test case with 50.0.2652.0 (Official Build) dev-m (64-bit): I just get the alert "this should never happen", even if I increased the timeout before calling go().

I have plugins unconditionally allowed, so I'm not sure what else I'm missing.

### ma...@gmail.com (2016-03-24)

This is odd, I haven't seen a single failure in the testing phase (all versions, Linux/Windows/VM/no VM, over 100 runs). I assume you're running the exploit from an HTTP server, can you verify that |location.href.split('exploit.html')[0] + 's.swf'| matches the actual location of the swf file? I'll have a closer look tomorrow and try to provide a debug version to pinpoint the problem.

### dc...@chromium.org (2016-03-24)

[Comment Deleted]

### wf...@chromium.org (2016-03-25)

I can get the alert from the test target domain when running off a web server.

### cl...@chromium.org (2016-03-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-03-25)

[Empty comment from Monorail migration]

### dc...@chromium.org (2016-03-28)

For future reference, the easiest way to test with PPAPI flash:
out/Release/chrome --ppapi-flash-path=/opt/google/chrome-unstable/PepperFlash/libpepflashplayer.so --ppapi-flash-version=21.0.0.193


### bu...@chromium.org (2016-03-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/f93a0e557dd97cc83d8b55953c2f57c5e2dfe07b

commit f93a0e557dd97cc83d8b55953c2f57c5e2dfe07b
Author: dcheng <dcheng@chromium.org>
Date: Tue Mar 29 00:16:20 2016

Always ignore navigation in Document::detach() in LocalFrame::navigate()

We already checked that FrameNavigation is enabled before trying to
schedule a LocationChange; however, it was possible to construct a
scenario with an opened window that would use the sync loading path and
bypass this check.

BUG=597532

Review URL: https://codereview.chromium.org/1840813002

Cr-Commit-Position: refs/heads/master@{#383627}

[modify] https://crrev.com/f93a0e557dd97cc83d8b55953c2f57c5e2dfe07b/third_party/WebKit/Source/core/frame/LocalFrame.cpp


### dc...@chromium.org (2016-03-29)

[Empty comment from Monorail migration]

### dc...@chromium.org (2016-03-29)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-03-29)

[Empty comment from Monorail migration]

### ti...@google.com (2016-03-29)

[Automated comment] Request affecting a post-stable build (M49), manual review required.

### ti...@google.com (2016-04-04)

tinazh@ / sshruthi@ - please approve for M49 (as there's likely to be one next week AFAICT) and M-50.



### ti...@google.com (2016-04-04)

Your change meets the bar and is auto-approved for M50 (branch: 2661)

### dc...@chromium.org (2016-04-05)

I think this patch may be superseded by https://codereview.chromium.org/1858833003. Let me see how the review on that goes.

### ss...@google.com (2016-04-05)

Merge approved for M49 (branch 2623)

### dc...@chromium.org (2016-04-05)

I'm clearing the merge requests on this. We should merge the fix in 600182 instead, as it addresses this bug as well as the new UXSS.

### ti...@google.com (2016-05-23)

[Empty comment from Monorail migration]

### ti...@google.com (2016-05-25)

[Empty comment from Monorail migration]

### ma...@gmail.com (2016-05-25)

:D Thanks!

### ti...@google.com (2016-06-17)

[Empty comment from Monorail migration]

### ti...@google.com (2016-06-17)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-07-05)

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

This issue was migrated from crbug.com/chromium/597532?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083928)*
