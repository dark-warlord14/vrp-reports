# Security: UAF in AppWindowContentsImpl::~AppWindowContentsImpl

| Field | Value |
|-------|-------|
| **Issue ID** | [40060350](https://issues.chromium.org/issues/40060350) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Platform>Apps, Platform>Apps>BrowserTag |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | jt...@gmail.com |
| **Assignee** | al...@chromium.org |
| **Created** | 2022-07-21 |
| **Bounty** | $10,000.00 |

## Description

**VULNERABILITY DETAILS**  

In ~WebContentsImpl, if mouse\_lock\_widget\_ is non-nullptr, it then calls the member function RejectMouseLockOrUnlockIfNecessary [1]. The mouse\_lock\_widget\_ will not be assigned to nullptr if there is an ongoing lock mouse request and WebContentsImpl::GotResponseToLockMouseRequest has not been called [2]. If the lock mouse request comes from a Guest View and the outer webcontents removes the Guest View without responding the request, the mouse\_lock\_widget\_ in outer webcontents instance will never be assigned to nullptr. This leads to UAF when the webcontents gets free.

[1] <https://source.chromium.org/chromium/chromium/src/+/main:content/browser/web_contents/web_contents_impl.cc;l=1032;drc=610603f89f0dd4da794848e4f8670a179efbcf38>  

[2] <https://source.chromium.org/chromium/chromium/src/+/main:content/browser/web_contents/web_contents_impl.cc;l=5295;drc=610603f89f0dd4da794848e4f8670a179efbcf38>

**VERSION**  

Chrome Version: 103.0.5060.134 stable + dev

**REPRODUCTION CASE**

1. Download the attached files to <dir>
2. Setup HTTPServer  
   
   cd path/to/dir && python -m SimpleHTTPServer 8000
3. Run  
   
   out/Asan/chrome --load-extension=path/to/dir

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: browser  

Crash State: See asan.log

## Attachments

- [manifest.json](attachments/manifest.json) (text/plain, 170 B)
- [background.js](attachments/background.js) (text/plain, 178 B)
- [page.html](attachments/page.html) (text/plain, 48 B)
- [page.js](attachments/page.js) (text/plain, 398 B)
- [poc.html](attachments/poc.html) (text/plain, 129 B)
- [asan.log](attachments/asan.log) (text/plain, 29.0 KB)
- [bug-1346245.txt](attachments/bug-1346245.txt) (text/plain, 26.7 KB)

## Timeline

### [Deleted User] (2022-07-21)

[Empty comment from Monorail migration]

### rs...@chromium.org (2022-07-21)

Thanks for the report. I can reproduce this on Mac.

[Monorail components: Platform>Apps]

### [Deleted User] (2022-07-21)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### re...@chromium.org (2022-07-21)

I'm not familiar with this code or how inner WebContents (GuestViews) are implemented.

It looks like we handle deletion of the RenderWidgetHost holding a mouse lock in WebContentsImpl::RenderWidgetDeleted() by calling LostMouseLock() however it looks like we might not properly traverse up the tree of WebContents in that function because we return early if the WebContents of the RenderWidgetHost is not ourselves.

Alex, I can take a look at this if you provide pointers on how the lifecycle of an inner WebContents works.

### [Deleted User] (2022-08-02)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-03)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-04)

benwells: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### re...@chromium.org (2022-08-04)

Moving ownership to Alex because Ben doesn't have time to respond to bugs anymore.

### al...@chromium.org (2022-08-10)

Thanks for the report!  I'm just coming back after OOO now and will try to take a closer look at this.  I can also repro locally.  I'm not really familiar with the mouse lock code; lfg@ originally updated it to work with inner WebContents in r441258, but he's no longer in Chrome.  Let me add mcnee@ or wjmaclean@ in case they know more.

Re: https://crbug.com/chromium/1346245#c4 about LostMouseLock: that seems like it should work properly for inner WebContents, since in the case where the widget's WebContents differs from the current one, it will just forward the call to the widget's WebContents, which will then walk over the chain of outer WebContents and clear mouse_lock_widget_ in each one.  The problem here seems to be that we never end up calling LostMouseLock() - we call RejectMouseLockOrUnlockIfNecessary() from ~WebContentsImpl when the inner WebContents gets destroyed, but that's not enough to get to LostMouseLock() when there's a request pending.  If the lock request is completed and not pending, it seems that RejectMouseLockOrUnlockIfNecessary does eventually reach LostMouseLock() via UnlockMouse() [1].

Digging into the code a bit, I think this kind of problem first came up in https://crbug.com/chromium/820593, where the call to RejectMouseLockOrUnlockIfNecessary() was added to ~WebContentsImpl in r542865.  It looks like that approach doesn't work for pending lock requests, though.

For the fix, a straightforward idea is to walk the chain of WebContents and clear mouse_lock_widget_ in ~WebContentsImpl (similarly to LostMouseLock(), or maybe we can just call it directly).  I also wonder whether we really need to set mouse_lock_widget_ on the WebContents chain at the time we receive the request (before we've actually decided whether it should be approved), as opposed to the time the request is granted (after which RejectMouseLockOrUnlockIfNecessary() should be sufficient to ensure we clear mouse_lock_widget_ pointers).

[1] https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/render_widget_host_view_event_handler.cc;l=216;drc=2fb84bdb28dcfe5eb7264f4e2f93ed4434d84f6b

[Monorail components: Platform>Apps>BrowserTag]

### gi...@appspot.gserviceaccount.com (2022-08-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/8380553a222cbc2c537ab67fc96e50f611ba4560

commit 8380553a222cbc2c537ab67fc96e50f611ba4560
Author: Alex Moshchuk <alexmos@chromium.org>
Date: Fri Aug 12 15:15:23 2022

Ensure mouse lock widget pointers are cleared in WebContents destructor

Requesting mouse/pointer lock (e.g., via requestPointerLock() from JS)
results in setting mouse_lock_widget_ to point to the
RenderWidgetHost that has the mouse lock, in both the widget's
WebContents and all its outer WebContents.  When a WebContents is
destroyed, it normally checks if it has an active mouse lock widget
and calls RejectMouseLockOrUnlockIfNecessary() if so. This usually
results in calling LostMouseLock(), which will clear
mouse_lock_widget_ in both the WebContents being destroyed and all its
ancestor WebContents.  However, there's a time window where this
doesn't work with <webview>, where a mouse lock request in the guest
has to go up to the embedder to asynchronously ask it for the
corresponding permission before it can be granted.  If the embedder
ends up destroying the <webview> guest while the guest's mouse lock
request is pending (prior to responding to that request), it could end
up with a stale mouse_lock_widget_ pointer, since
RejectMouseLockOrUnlockIfNecessary() follows a different path for
pending requests and doesn't clear those pointers.  Sadly, the
RenderWidgetHost destruction is also not going to trigger clearing
these pointers as it normally does, since ~WebContentsImpl clears
delegate_ pointers for all of its widgets before destroying them,
causing ~RenderWidgetHostImpl::Destroy() to not call
WebContentsImpl::RenderWidgetDeleted(), which normally does this.

This CL ensures that all mouse_lock_widget_ pointers are cleared on
the entire WebContents chain in the WebContentsImpl destructor. In the
future, we could also investigate not setting mouse_lock_widget_
before we actually decide that a mouse lock request should proceed,
and removing the current implementation's dependency on that behavior.

Bug: 1346245
Change-Id: Iaf1fec400ca47d7cb20c21ce145dc041317a7db6
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3823606
Reviewed-by: James Maclean <wjmaclean@chromium.org>
Commit-Queue: Alex Moshchuk <alexmos@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1034481}

[modify] https://crrev.com/8380553a222cbc2c537ab67fc96e50f611ba4560/content/public/test/browser_test_utils.h
[modify] https://crrev.com/8380553a222cbc2c537ab67fc96e50f611ba4560/chrome/browser/apps/guest_view/web_view_interactive_browsertest.cc
[add] https://crrev.com/8380553a222cbc2c537ab67fc96e50f611ba4560/chrome/test/data/extensions/platform_apps/web_view/pointer_lock_pending/main.js
[modify] https://crrev.com/8380553a222cbc2c537ab67fc96e50f611ba4560/content/public/test/browser_test_utils.cc
[add] https://crrev.com/8380553a222cbc2c537ab67fc96e50f611ba4560/chrome/test/data/extensions/platform_apps/web_view/pointer_lock_pending/test.js
[add] https://crrev.com/8380553a222cbc2c537ab67fc96e50f611ba4560/chrome/test/data/extensions/platform_apps/web_view/pointer_lock_pending/manifest.json
[modify] https://crrev.com/8380553a222cbc2c537ab67fc96e50f611ba4560/content/browser/web_contents/web_contents_impl.cc
[modify] https://crrev.com/8380553a222cbc2c537ab67fc96e50f611ba4560/content/browser/web_contents/web_contents_impl.h
[add] https://crrev.com/8380553a222cbc2c537ab67fc96e50f611ba4560/chrome/test/data/extensions/platform_apps/web_view/pointer_lock_pending/main.html


### al...@chromium.org (2022-08-12)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-12)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-12)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-12)

Requesting merge to stable M104 because latest trunk commit (1034481) appears to be after stable branch point (1012729).

Requesting merge to beta M105 because latest trunk commit (1034481) appears to be after beta branch point (1027018).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-08-13)

Merge review required: M105 is already shipping to beta.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), harrysouders (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-08-13)

Merge review required: M104 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: eakpobaro (Android), harrysouders (iOS), obenedict (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### al...@chromium.org (2022-08-15)

1. Why does your merge fit within the merge criteria for these milestones?
Fixes an important security issue.

2. What changes specifically would you like to merge? Please link to Gerrit.
https://chromium-review.googlesource.com/c/chromium/src/+/3823606

3. Have the changes been released and tested on canary?
The change has been released in canary and its stability has been verified.  The actual crash repro requires an ASAN build to observe, so it's not possible to test on an ordinary canary release.

4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
No.

5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
No.

6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.
Not sure that any additional testing is needed, but it should be possible to verify this fix on M104/105 with an ASAN build and the repro steps and files from the original description.

### am...@chromium.org (2022-08-17)

105 merge approved, please merge to branch 5195 at your earliest convenience 
104 merge approved, please merge this fix to branch 5112; there are not further planned releases of 104/stable, however this fix should be backported to be included in Extended Stable which will be released when 105 is promoted to stable -- thank you! 

### gi...@appspot.gserviceaccount.com (2022-08-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/859cf771d8364577cce49da5520b0e4b44ebb5a9

commit 859cf771d8364577cce49da5520b0e4b44ebb5a9
Author: Alex Moshchuk <alexmos@chromium.org>
Date: Thu Aug 18 23:51:27 2022

[M104] Ensure mouse lock widget pointers are cleared in WebContents destructor

Requesting mouse/pointer lock (e.g., via requestPointerLock() from JS)
results in setting mouse_lock_widget_ to point to the
RenderWidgetHost that has the mouse lock, in both the widget's
WebContents and all its outer WebContents.  When a WebContents is
destroyed, it normally checks if it has an active mouse lock widget
and calls RejectMouseLockOrUnlockIfNecessary() if so. This usually
results in calling LostMouseLock(), which will clear
mouse_lock_widget_ in both the WebContents being destroyed and all its
ancestor WebContents.  However, there's a time window where this
doesn't work with <webview>, where a mouse lock request in the guest
has to go up to the embedder to asynchronously ask it for the
corresponding permission before it can be granted.  If the embedder
ends up destroying the <webview> guest while the guest's mouse lock
request is pending (prior to responding to that request), it could end
up with a stale mouse_lock_widget_ pointer, since
RejectMouseLockOrUnlockIfNecessary() follows a different path for
pending requests and doesn't clear those pointers.  Sadly, the
RenderWidgetHost destruction is also not going to trigger clearing
these pointers as it normally does, since ~WebContentsImpl clears
delegate_ pointers for all of its widgets before destroying them,
causing ~RenderWidgetHostImpl::Destroy() to not call
WebContentsImpl::RenderWidgetDeleted(), which normally does this.

This CL ensures that all mouse_lock_widget_ pointers are cleared on
the entire WebContents chain in the WebContentsImpl destructor. In the
future, we could also investigate not setting mouse_lock_widget_
before we actually decide that a mouse lock request should proceed,
and removing the current implementation's dependency on that behavior.

(cherry picked from commit 8380553a222cbc2c537ab67fc96e50f611ba4560)

Bug: 1346245
Change-Id: Iaf1fec400ca47d7cb20c21ce145dc041317a7db6
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3823606
Reviewed-by: James Maclean <wjmaclean@chromium.org>
Commit-Queue: Alex Moshchuk <alexmos@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1034481}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3838431
Cr-Commit-Position: refs/branch-heads/5112@{#1498}
Cr-Branched-From: b13d3fe7b3c47a56354ef54b221008afa754412e-refs/heads/main@{#1012729}

[modify] https://crrev.com/859cf771d8364577cce49da5520b0e4b44ebb5a9/content/public/test/browser_test_utils.h
[modify] https://crrev.com/859cf771d8364577cce49da5520b0e4b44ebb5a9/chrome/browser/apps/guest_view/web_view_interactive_browsertest.cc
[add] https://crrev.com/859cf771d8364577cce49da5520b0e4b44ebb5a9/chrome/test/data/extensions/platform_apps/web_view/pointer_lock_pending/main.js
[modify] https://crrev.com/859cf771d8364577cce49da5520b0e4b44ebb5a9/content/public/test/browser_test_utils.cc
[add] https://crrev.com/859cf771d8364577cce49da5520b0e4b44ebb5a9/chrome/test/data/extensions/platform_apps/web_view/pointer_lock_pending/test.js
[add] https://crrev.com/859cf771d8364577cce49da5520b0e4b44ebb5a9/chrome/test/data/extensions/platform_apps/web_view/pointer_lock_pending/manifest.json
[modify] https://crrev.com/859cf771d8364577cce49da5520b0e4b44ebb5a9/content/browser/web_contents/web_contents_impl.cc
[modify] https://crrev.com/859cf771d8364577cce49da5520b0e4b44ebb5a9/content/browser/web_contents/web_contents_impl.h
[add] https://crrev.com/859cf771d8364577cce49da5520b0e4b44ebb5a9/chrome/test/data/extensions/platform_apps/web_view/pointer_lock_pending/main.html


### [Deleted User] (2022-08-18)

LTS Milestone M102

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### al...@chromium.org (2022-08-18)

https://crbug.com/chromium/1346245#c20:
1. Was this issue a regression for the milestone it was found in?
No, I'm guessing this existed for a while, much earlier than M102.  As mentioned in https://crbug.com/chromium/1346245#c9, there was an incomplete fix (r542865) for this kind of problem back in M67, and r1012729 just makes that fix more complete.

2. Is this issue related to a change or feature merged after the latest LTS Milestone?
No.

### gi...@appspot.gserviceaccount.com (2022-08-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/bc29f62797c4f8eb59ac7b908775d859be957fc4

commit bc29f62797c4f8eb59ac7b908775d859be957fc4
Author: Alex Moshchuk <alexmos@chromium.org>
Date: Fri Aug 19 00:38:50 2022

[M105] Ensure mouse lock widget pointers are cleared in WebContents destructor

Requesting mouse/pointer lock (e.g., via requestPointerLock() from JS)
results in setting mouse_lock_widget_ to point to the
RenderWidgetHost that has the mouse lock, in both the widget's
WebContents and all its outer WebContents.  When a WebContents is
destroyed, it normally checks if it has an active mouse lock widget
and calls RejectMouseLockOrUnlockIfNecessary() if so. This usually
results in calling LostMouseLock(), which will clear
mouse_lock_widget_ in both the WebContents being destroyed and all its
ancestor WebContents.  However, there's a time window where this
doesn't work with <webview>, where a mouse lock request in the guest
has to go up to the embedder to asynchronously ask it for the
corresponding permission before it can be granted.  If the embedder
ends up destroying the <webview> guest while the guest's mouse lock
request is pending (prior to responding to that request), it could end
up with a stale mouse_lock_widget_ pointer, since
RejectMouseLockOrUnlockIfNecessary() follows a different path for
pending requests and doesn't clear those pointers.  Sadly, the
RenderWidgetHost destruction is also not going to trigger clearing
these pointers as it normally does, since ~WebContentsImpl clears
delegate_ pointers for all of its widgets before destroying them,
causing ~RenderWidgetHostImpl::Destroy() to not call
WebContentsImpl::RenderWidgetDeleted(), which normally does this.

This CL ensures that all mouse_lock_widget_ pointers are cleared on
the entire WebContents chain in the WebContentsImpl destructor. In the
future, we could also investigate not setting mouse_lock_widget_
before we actually decide that a mouse lock request should proceed,
and removing the current implementation's dependency on that behavior.

(cherry picked from commit 8380553a222cbc2c537ab67fc96e50f611ba4560)

Bug: 1346245
Change-Id: Iaf1fec400ca47d7cb20c21ce145dc041317a7db6
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3823606
Reviewed-by: James Maclean <wjmaclean@chromium.org>
Commit-Queue: Alex Moshchuk <alexmos@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1034481}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3838330
Cr-Commit-Position: refs/branch-heads/5195@{#701}
Cr-Branched-From: 7aa3f074a7907975b001346cc0288d0214af8451-refs/heads/main@{#1027018}

[modify] https://crrev.com/bc29f62797c4f8eb59ac7b908775d859be957fc4/content/public/test/browser_test_utils.h
[modify] https://crrev.com/bc29f62797c4f8eb59ac7b908775d859be957fc4/chrome/browser/apps/guest_view/web_view_interactive_browsertest.cc
[add] https://crrev.com/bc29f62797c4f8eb59ac7b908775d859be957fc4/chrome/test/data/extensions/platform_apps/web_view/pointer_lock_pending/main.js
[modify] https://crrev.com/bc29f62797c4f8eb59ac7b908775d859be957fc4/content/public/test/browser_test_utils.cc
[add] https://crrev.com/bc29f62797c4f8eb59ac7b908775d859be957fc4/chrome/test/data/extensions/platform_apps/web_view/pointer_lock_pending/test.js
[add] https://crrev.com/bc29f62797c4f8eb59ac7b908775d859be957fc4/chrome/test/data/extensions/platform_apps/web_view/pointer_lock_pending/manifest.json
[modify] https://crrev.com/bc29f62797c4f8eb59ac7b908775d859be957fc4/content/browser/web_contents/web_contents_impl.cc
[modify] https://crrev.com/bc29f62797c4f8eb59ac7b908775d859be957fc4/content/browser/web_contents/web_contents_impl.h
[add] https://crrev.com/bc29f62797c4f8eb59ac7b908775d859be957fc4/chrome/test/data/extensions/platform_apps/web_view/pointer_lock_pending/main.html


### rz...@google.com (2022-08-19)

[Empty comment from Monorail migration]

### rz...@google.com (2022-08-19)

[Empty comment from Monorail migration]

### vo...@google.com (2022-08-23)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-23)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-08-23)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### vo...@google.com (2022-08-23)

M96:
1. M96: https://chromium-review.googlesource.com/c/chromium/src/+/3849903, M102: https://chromium-review.googlesource.com/c/chromium/src/+/3848803
2. Low - simple conflits in tests
3. M104
4. Yes


### gm...@google.com (2022-08-23)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-08-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/126c6e32ebe7a2ceb603ffdee97639caee7d6eb4

commit 126c6e32ebe7a2ceb603ffdee97639caee7d6eb4
Author: Zakhar Voit <voit@google.com>
Date: Wed Aug 24 10:54:26 2022

[M96-LTS] Ensure mouse lock widget pointers are cleared in WebContents destructor

Requesting mouse/pointer lock (e.g., via requestPointerLock() from JS)
results in setting mouse_lock_widget_ to point to the
RenderWidgetHost that has the mouse lock, in both the widget's
WebContents and all its outer WebContents.  When a WebContents is
destroyed, it normally checks if it has an active mouse lock widget
and calls RejectMouseLockOrUnlockIfNecessary() if so. This usually
results in calling LostMouseLock(), which will clear
mouse_lock_widget_ in both the WebContents being destroyed and all its
ancestor WebContents.  However, there's a time window where this
doesn't work with <webview>, where a mouse lock request in the guest
has to go up to the embedder to asynchronously ask it for the
corresponding permission before it can be granted.  If the embedder
ends up destroying the <webview> guest while the guest's mouse lock
request is pending (prior to responding to that request), it could end
up with a stale mouse_lock_widget_ pointer, since
RejectMouseLockOrUnlockIfNecessary() follows a different path for
pending requests and doesn't clear those pointers.  Sadly, the
RenderWidgetHost destruction is also not going to trigger clearing
these pointers as it normally does, since ~WebContentsImpl clears
delegate_ pointers for all of its widgets before destroying them,
causing ~RenderWidgetHostImpl::Destroy() to not call
WebContentsImpl::RenderWidgetDeleted(), which normally does this.

This CL ensures that all mouse_lock_widget_ pointers are cleared on
the entire WebContents chain in the WebContentsImpl destructor. In the
future, we could also investigate not setting mouse_lock_widget_
before we actually decide that a mouse lock request should proceed,
and removing the current implementation's dependency on that behavior.

(cherry picked from commit 8380553a222cbc2c537ab67fc96e50f611ba4560)

(cherry picked from commit 859cf771d8364577cce49da5520b0e4b44ebb5a9)

Bug: 1346245
Change-Id: Iaf1fec400ca47d7cb20c21ce145dc041317a7db6
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3823606
Commit-Queue: Alex Moshchuk <alexmos@chromium.org>
Cr-Original-Original-Commit-Position: refs/heads/main@{#1034481}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3838431
Cr-Original-Commit-Position: refs/branch-heads/5112@{#1498}
Cr-Original-Branched-From: b13d3fe7b3c47a56354ef54b221008afa754412e-refs/heads/main@{#1012729}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3849903
Owners-Override: Artem Sumaneev <asumaneev@google.com>
Commit-Queue: Zakhar Voit <voit@google.com>
Reviewed-by: Artem Sumaneev <asumaneev@google.com>
Cr-Commit-Position: refs/branch-heads/4664@{#1694}
Cr-Branched-From: 24dc4ee75e01a29d390d43c9c264372a169273a7-refs/heads/main@{#929512}

[modify] https://crrev.com/126c6e32ebe7a2ceb603ffdee97639caee7d6eb4/content/public/test/browser_test_utils.h
[modify] https://crrev.com/126c6e32ebe7a2ceb603ffdee97639caee7d6eb4/chrome/browser/apps/guest_view/web_view_interactive_browsertest.cc
[add] https://crrev.com/126c6e32ebe7a2ceb603ffdee97639caee7d6eb4/chrome/test/data/extensions/platform_apps/web_view/pointer_lock_pending/main.js
[modify] https://crrev.com/126c6e32ebe7a2ceb603ffdee97639caee7d6eb4/content/public/test/browser_test_utils.cc
[add] https://crrev.com/126c6e32ebe7a2ceb603ffdee97639caee7d6eb4/chrome/test/data/extensions/platform_apps/web_view/pointer_lock_pending/test.js
[add] https://crrev.com/126c6e32ebe7a2ceb603ffdee97639caee7d6eb4/chrome/test/data/extensions/platform_apps/web_view/pointer_lock_pending/manifest.json
[modify] https://crrev.com/126c6e32ebe7a2ceb603ffdee97639caee7d6eb4/content/browser/web_contents/web_contents_impl.cc
[modify] https://crrev.com/126c6e32ebe7a2ceb603ffdee97639caee7d6eb4/content/browser/web_contents/web_contents_impl.h
[add] https://crrev.com/126c6e32ebe7a2ceb603ffdee97639caee7d6eb4/chrome/test/data/extensions/platform_apps/web_view/pointer_lock_pending/main.html


### gi...@appspot.gserviceaccount.com (2022-08-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/d74d2b9f00c7cbc49dfc35d07cb685bfd28444bc

commit d74d2b9f00c7cbc49dfc35d07cb685bfd28444bc
Author: Zakhar Voit <voit@google.com>
Date: Wed Aug 24 10:59:16 2022

[M102-LTS] Ensure mouse lock widget pointers are cleared in WebContents destructor

Requesting mouse/pointer lock (e.g., via requestPointerLock() from JS)
results in setting mouse_lock_widget_ to point to the
RenderWidgetHost that has the mouse lock, in both the widget's
WebContents and all its outer WebContents.  When a WebContents is
destroyed, it normally checks if it has an active mouse lock widget
and calls RejectMouseLockOrUnlockIfNecessary() if so. This usually
results in calling LostMouseLock(), which will clear
mouse_lock_widget_ in both the WebContents being destroyed and all its
ancestor WebContents.  However, there's a time window where this
doesn't work with <webview>, where a mouse lock request in the guest
has to go up to the embedder to asynchronously ask it for the
corresponding permission before it can be granted.  If the embedder
ends up destroying the <webview> guest while the guest's mouse lock
request is pending (prior to responding to that request), it could end
up with a stale mouse_lock_widget_ pointer, since
RejectMouseLockOrUnlockIfNecessary() follows a different path for
pending requests and doesn't clear those pointers.  Sadly, the
RenderWidgetHost destruction is also not going to trigger clearing
these pointers as it normally does, since ~WebContentsImpl clears
delegate_ pointers for all of its widgets before destroying them,
causing ~RenderWidgetHostImpl::Destroy() to not call
WebContentsImpl::RenderWidgetDeleted(), which normally does this.

This CL ensures that all mouse_lock_widget_ pointers are cleared on
the entire WebContents chain in the WebContentsImpl destructor. In the
future, we could also investigate not setting mouse_lock_widget_
before we actually decide that a mouse lock request should proceed,
and removing the current implementation's dependency on that behavior.

(cherry picked from commit 8380553a222cbc2c537ab67fc96e50f611ba4560)

(cherry picked from commit 859cf771d8364577cce49da5520b0e4b44ebb5a9)

Bug: 1346245
Change-Id: Iaf1fec400ca47d7cb20c21ce145dc041317a7db6
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3823606
Commit-Queue: Alex Moshchuk <alexmos@chromium.org>
Cr-Original-Original-Commit-Position: refs/heads/main@{#1034481}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3838431
Cr-Original-Commit-Position: refs/branch-heads/5112@{#1498}
Cr-Original-Branched-From: b13d3fe7b3c47a56354ef54b221008afa754412e-refs/heads/main@{#1012729}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3848803
Owners-Override: Artem Sumaneev <asumaneev@google.com>
Commit-Queue: Zakhar Voit <voit@google.com>
Reviewed-by: Artem Sumaneev <asumaneev@google.com>
Cr-Commit-Position: refs/branch-heads/5005@{#1320}
Cr-Branched-From: 5b4d9450fee01f821b6400e947b3839727643a71-refs/heads/main@{#992738}

[modify] https://crrev.com/d74d2b9f00c7cbc49dfc35d07cb685bfd28444bc/content/public/test/browser_test_utils.h
[modify] https://crrev.com/d74d2b9f00c7cbc49dfc35d07cb685bfd28444bc/chrome/browser/apps/guest_view/web_view_interactive_browsertest.cc
[add] https://crrev.com/d74d2b9f00c7cbc49dfc35d07cb685bfd28444bc/chrome/test/data/extensions/platform_apps/web_view/pointer_lock_pending/main.js
[modify] https://crrev.com/d74d2b9f00c7cbc49dfc35d07cb685bfd28444bc/content/public/test/browser_test_utils.cc
[add] https://crrev.com/d74d2b9f00c7cbc49dfc35d07cb685bfd28444bc/chrome/test/data/extensions/platform_apps/web_view/pointer_lock_pending/test.js
[add] https://crrev.com/d74d2b9f00c7cbc49dfc35d07cb685bfd28444bc/chrome/test/data/extensions/platform_apps/web_view/pointer_lock_pending/manifest.json
[modify] https://crrev.com/d74d2b9f00c7cbc49dfc35d07cb685bfd28444bc/content/browser/web_contents/web_contents_impl.cc
[modify] https://crrev.com/d74d2b9f00c7cbc49dfc35d07cb685bfd28444bc/content/browser/web_contents/web_contents_impl.h
[add] https://crrev.com/d74d2b9f00c7cbc49dfc35d07cb685bfd28444bc/chrome/test/data/extensions/platform_apps/web_view/pointer_lock_pending/main.html


### vo...@google.com (2022-08-24)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-08-25)

[Empty comment from Monorail migration]

### am...@google.com (2022-08-30)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-08-30)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-08-30)

Congratulations! The VRP Panel has decided to award you $10,000 for this report based on being mitigated by needing to install an extension. This is only considered lightly/mildly mitigated in the updated Chrome VRP policies [1], the panel decided that it warranted much higher than that range due to the mitigation being the extension alone. Thank you for your efforts in reporting this issue to us and great work! 

### am...@google.com (2022-09-14)

[Empty comment from Monorail migration]

### ad...@google.com (2022-09-26)

[Empty comment from Monorail migration]

### ad...@google.com (2022-09-26)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-18)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1346245?no_tracker_redirect=1

[Multiple monorail components: Platform>Apps, Platform>Apps>BrowserTag]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060350)*
