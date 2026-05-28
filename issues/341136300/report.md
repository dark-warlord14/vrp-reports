# Extensions can run JS on any priveledged origin by using chrome.devtools.inspectedWindow.reload and crashing the page

| Field | Value |
|-------|-------|
| **Issue ID** | [341136300](https://issues.chromium.org/issues/341136300) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Platform>Extensions |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ad...@gmail.com |
| **Assignee** | pf...@google.com |
| **Created** | 2024-05-16 |
| **Bounty** | Confirmed (amount unknown) |

## Description

As requested, I am submitted this as a separate issue. The original bug report (with the full chain leading to a sandbox escape) is located at <https://issues.chromium.org/issues/338248595>

## VULNERABILITY DETAILS

1. The user opens devtools on any unprivileged page, which will load our devtools extension as an iframe and give access to the chrome.devtools API
2. The extension navigates the inspected page to `example.org`, then it evaluates `location.href = "about:blank"` inside the page. This resets the page's origin.
3. The extension runs `chrome.devtools.inspectedWindow.reload` and puts a `debugger` statement in the `injectedScript` argument.
4. The extension runs `chrome.devtools.inspectedWindow.reload` again with the JS payload in the `injectedScript` argument. This crashes the inspected page.
5. The extension navigates the crashed page to a chrome:// page, which will cause the previously queued up JS to execute on the privileged page.

## EXPLANATION

An extension with the `devtools_page` permission in its manifest.json file can use the `chrome.devtools.inspectedWindow.reload` API, which reloads the inspected page and injects a content script. It is possible to use this API to run arbitrary JS on *any* page, even if it is supposed to be disallowed.

Normally, pending devtools commands are discarded after a page crash. However, [`Page.reload` method calls are whitelisted and will not be removed](https://source.chromium.org/chromium/chromium/src/+/main:content/browser/devtools/devtools_session.cc;l=483-488?q=ClearPendingMessages&ss=chromium%2Fchromium%2Fsrc). Essentially this is due to an incomplete fix for [crbug.com/40053357](https://issues.chromium.org/issues/40053357). If the page crashes while it is being reloaded by the extension, then the JS will be queued to run after the page is reloaded another time. Thus, we can just navigate the inspected page to any privileged page of our choosing (with `chrome.tabs.update`), and our custom JS will run on the page we navigate to.

A crash can be caused with the `debugger` statement in the content script, or with `[...new Array(2**31)]`. Using the `debugger` statement causes a crash since it puts [`navigation_commit_state_` into an unexpected state](https://source.chromium.org/chromium/chromium/src/+/main:content/renderer/render_frame_impl.cc;l=1345-1346;drc=770f3fce3719ee18c102ad0b1a347d82147fbb1a). This happens when `RenderFrameImpl::SynchronouslyCommitAboutBlankForBug778318` is run, which modifies [`_navigation_commit_state` to a different value](https://source.chromium.org/chromium/chromium/src/+/main:content/renderer/render_frame_impl.cc;l=5622?q=navigation_commit_state_&ss=chromium%2Fchromium%2Fsrc). This also means that if the debugger statement is used, the page must be on the `about:blank` URL for the crash to occur.

Resetting the inspected page's origin must occur since we do not want to crash our own extension process. Note that using the `debugger` statement isn't the only way to cause a crash here. You can also use `[...new Array(2**31)]`, but this will take a a few seconds longer to run. As long as the page crashes while the reload command is still pending, the exploit will work.

### BISECT

The mechanism which queues up devtools messages after a crash was added 9 years ago, on [commit a8622c18940eac1db5c75685d0c09c7eedecf833](https://chromium.googlesource.com/chromium/src/+/a8622c18940eac1db5c75685d0c09c7eedecf833) (position 332838).

I confirmed that this is the commit which introduced this bug, since I was able to reproduce it on version 45.0.2423.0 ([position 332839](https://commondatastorage.googleapis.com/chromium-browser-snapshots/index.html?prefix=Win/332839/)), but not on [position 332834](https://commondatastorage.googleapis.com/chromium-browser-snapshots/index.html?prefix=Win/332834/).

### PATCH

Removing the exception for `Page.reload` commands in `DevToolsSession::ClearPendingMessages` is enough to fix this bug. I have tested this to work by compiling and running Chromium with the patch applied. I've attached the diff for this as `fix-devtools-reload-bug.patch`.

## VERSION

Chrome Version: 124.0.6367.201 stable

Operating System: Debian 12

## REPRODUCTION

1. Download the files attached to this report, and place them in the same folder.
2. Load the attached files as a Chrome extension.
3. Open devtools on about:blank or any other unprivileged page.
4. The extension will navigate to chrome://settings and show an alert.

A video is attached which demonstrates this process.

## CREDIT INFORMATION

Reporter credit: Allen Ding

## Attachments

- [devtools.html](attachments/devtools.html) (text/html, 73 B)
- [devtools.js](attachments/devtools.js) (text/javascript, 1.3 KB)
- [manifest.json](attachments/manifest.json) (application/json, 274 B)
- [worker.js](attachments/worker.js) (text/javascript, 149 B)
- [fix-devtools-reload-bug.patch](attachments/fix-devtools-reload-bug.patch) (text/x-diff, 817 B)
- [chrome_devtools_exploit.mp4](attachments/chrome_devtools_exploit.mp4) (video/mp4, 784.5 KB)
- [chrome_devtools_bug.mp4](attachments/chrome_devtools_bug.mp4) (video/mp4, 926.7 KB)
- [Screenshot_2024-05-24_09-54-39.png](attachments/Screenshot_2024-05-24_09-54-39.png) (image/png, 77.3 KB)
- [devtools.js](attachments/devtools.js) (text/javascript, 1.3 KB)

## Timeline

### el...@chromium.org (2024-05-16)

Security shepherd: sending to the same assignee as [issue 338248595](https://issues.chromium.org/issues/338248595) with similar pri/sev :)

### pf...@google.com (2024-05-17)

caseq@: As the author of this do you have thoughts on the proposed fix? Should Page.reload be exempt from being discarded? It's specifically the falling through that's causing the issue here.

### pe...@google.com (2024-05-17)

Setting milestone because of s0/s1 severity.

### ca...@google.com (2024-05-23)

My recollection is that these lines were there because something was breaking if we just discarded Page.reload in this case -- I would assume it would have to do with reloading a page with a ctrl+r pressed in the front-end after a page crash. But I tried the proposed fix, and (1) [I don't see any tests failing now](https://chromium-review.googlesource.com/c/chromium/src/+/5565191?tab=checks) and (2) the underlying functionality appears to be broken even without the proposed change (I assume this could have been the result of migration to the tab target, as we're apparently disconnecting the crashed session now).

So.. I guess you could try that fix and see if anything breaks. Or you could limit that to the case of when the page has navigated to a DOM UI origin. Also, I just noticed you [landed this](https://chromium-review.googlesource.com/c/chromium/src/+/5542082), I assume this should help?

### pf...@google.com (2024-05-24)

You are right, cannot reproduce the bug with the loaderId restriction anymore! ading2019@ can you confirm?

### ad...@gmail.com (2024-05-24)

I'm still able to reproduce this bug with the loaderId changes. I tested on [position 1305741](https://commondatastorage.googleapis.com/chromium-browser-snapshots/index.html?prefix=Linux_x64/1305741/), which does have the loaderId fix in it. I checked this by looking at the JS in the devtools frontend, and sure enough it is passing the loaderId properly. See my attached video and screenshot for a demonstration of this. I'm still using the exact same POC that was uploaded to this issue before, except that I increased the duration of the last sleep to 1000ms.

### pf...@google.com (2024-06-03)

I'm able to reproduce this as well. Pinning the reload to a loaderId isn't sufficient. So far I've not been able to repoduce it in a custom build in order to track down the casue. It's extremely timing sensitive. I'm inclined to go with un-specialcasing Page.reload. My best hypothesis currently is that the Page.reload arrives on the "old" document, schedules the injection, and then gets interrupted by the crash.

### pf...@google.com (2024-06-04)

Assigning to caseq@ to make a call on the tentative fix CL.

### ts...@google.com (2024-06-10)

I pinged caseq offline to get a call made, perhaps. Thanks

### ca...@google.com (2024-06-10)

As I stated above, I don't object against the suggested fix as long as it doesn't cause any regressions. While I've ran a CQ against it on a WIP CL, I hope you could follow through by accompanying the change with some test coverage.

As for the loaderId check -- Philip, I had another look at your CL and realized you only verify the loaderId on the browser side. Would it help against this attack vector if we were also to [verify the loaderId on the renderer side](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/inspector/inspector_page_agent.cc;l=676)?

### ap...@google.com (2024-06-18)

Project: chromium/src
Branch: main

commit 43b8b682d05c75caf0daf1643b84575009cc0052
Author: Philip Pfaffe <pfaffe@chromium.org>
Date:   Tue Jun 18 10:04:45 2024

    Prevent script injection on reload when racing with a navigation
    
    DevTools passes the loaderId now when calling Page.reload, in order to
    prevent accidentally reloading the wrong page when a navigation occurred
    concurrently. It can still happen that the navigation kicks in in between the reload iniated in the browser and the script injection that happens in the renderer, which would run the injected script on the wrong target. We need to check the loaderId also on the renderer side.
    
    Fixed: 341136300
    Change-Id: I891fb37fa10e6789c8697a0f29bf7118788a9319
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5625857
    Reviewed-by: Andrey Kosyakov <caseq@chromium.org>
    Commit-Queue: Philip Pfaffe <pfaffe@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1316330}

M       third_party/blink/renderer/core/inspector/build.gni
M       third_party/blink/renderer/core/inspector/inspector_page_agent.cc
M       third_party/blink/renderer/core/inspector/inspector_page_agent.h
A       third_party/blink/renderer/core/inspector/inspector_page_agent_unittest.cc

https://chromium-review.googlesource.com/5625857


### pe...@google.com (2024-06-18)

Requesting merge to stable (M126) because latest trunk commit (1316330) appears to be after stable branch point (1300313).
Requesting merge to beta (M127) because latest trunk commit (1316330) appears to be after beta branch point (1313161).
Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.

### pe...@google.com (2024-06-19)

Merge review required: M127 is already shipping to beta.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: eakpobaro (Android), eakpobaro (iOS), alonbajayo (ChromeOS), danielyip (Desktop)

### pe...@google.com (2024-06-19)

Merge review required: M126 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: eakpobaro (Android), eakpobaro (iOS), ceb (ChromeOS), srinivassista (Desktop)

### am...@chromium.org (2024-06-20)

Given the regression concerns noted in #11 and upon reviewing the change, I would like this fix to get a bit more bake time on Canary before a potential backmerge. I'll revisit and re-review early next week.

### am...@chromium.org (2024-06-25)

Since there is an M127 Beta update this week, let's get this fix into that if possible; please merge to branch 6533 at soonest so this fix can be included in tomorrow's M127 Beta update. 
The M126 Stable update for this week was cut on Friday and released on Monday; we are going into a release freeze. I'll revisit this later in the week or early next week for potential M126 Stable merge for the update following release freeze. 

### ap...@google.com (2024-06-26)

Project: chromium/src
Branch: refs/branch-heads/6533

commit b2b1d3f5f039c55e2da44353bae763cae796b6b7
Author: Philip Pfaffe <pfaffe@chromium.org>
Date:   Wed Jun 26 09:20:25 2024

    Prevent script injection on reload when racing with a navigation
    
    DevTools passes the loaderId now when calling Page.reload, in order to
    prevent accidentally reloading the wrong page when a navigation occurred
    concurrently. It can still happen that the navigation kicks in in between the reload iniated in the browser and the script injection that happens in the renderer, which would run the injected script on the wrong target. We need to check the loaderId also on the renderer side.
    
    (cherry picked from commit 43b8b682d05c75caf0daf1643b84575009cc0052)
    
    Fixed: 341136300
    Change-Id: I891fb37fa10e6789c8697a0f29bf7118788a9319
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5625857
    Reviewed-by: Andrey Kosyakov <caseq@chromium.org>
    Commit-Queue: Philip Pfaffe <pfaffe@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1316330}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5656772
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Commit-Queue: Danil Somsikov <dsv@chromium.org>
    Reviewed-by: Danil Somsikov <dsv@chromium.org>
    Auto-Submit: Philip Pfaffe <pfaffe@chromium.org>
    Cr-Commit-Position: refs/branch-heads/6533@{#707}
    Cr-Branched-From: 7e0b87ec6b8cb5cb2969e1479fc25776e582721d-refs/heads/main@{#1313161}

M       third_party/blink/renderer/core/inspector/build.gni
M       third_party/blink/renderer/core/inspector/inspector_page_agent.cc
M       third_party/blink/renderer/core/inspector/inspector_page_agent.h
A       third_party/blink/renderer/core/inspector/inspector_page_agent_unittest.cc

https://chromium-review.googlesource.com/5656772


### pe...@google.com (2024-06-26)

LTS Milestone M126

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### am...@chromium.org (2024-07-01)

The parent / umbrella issue has still not been resolved. This issue will be evaluated by the VRP Panel once that occurs.

### pe...@google.com (2024-07-02)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### rz...@google.com (2024-07-09)

1. <https://crrev.com/c/5672472>
2. Low, there were a few simple merge conflicts
3. 127
4. Yes

### am...@chromium.org (2024-07-15)

M126 merge approved for <https://crrev.com/c/5625857> -- please merge this fix to branch 6478 at your earliest convenience so this fix can be included in the M126 Extended Stable release next week

### ap...@google.com (2024-07-15)

Project: chromium/src
Branch: refs/branch-heads/6478

commit e4ecc269979f94db9a9e0eb73287ee84a57b9576
Author: Philip Pfaffe <pfaffe@chromium.org>
Date:   Mon Jul 15 17:24:05 2024

    Prevent script injection on reload when racing with a navigation
    
    DevTools passes the loaderId now when calling Page.reload, in order to
    prevent accidentally reloading the wrong page when a navigation occurred
    concurrently. It can still happen that the navigation kicks in in between the reload iniated in the browser and the script injection that happens in the renderer, which would run the injected script on the wrong target. We need to check the loaderId also on the renderer side.
    
    (cherry picked from commit 43b8b682d05c75caf0daf1643b84575009cc0052)
    
    Fixed: 341136300
    Change-Id: I891fb37fa10e6789c8697a0f29bf7118788a9319
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5625857
    Reviewed-by: Andrey Kosyakov <caseq@chromium.org>
    Commit-Queue: Philip Pfaffe <pfaffe@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1316330}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5708170
    Auto-Submit: Daniel Yip <danielyip@google.com>
    Owners-Override: Daniel Yip <danielyip@google.com>
    Reviewed-by: Philip Pfaffe <pfaffe@chromium.org>
    Cr-Commit-Position: refs/branch-heads/6478@{#1775}
    Cr-Branched-From: e6143acc03189c5e52959545b110d6d17ecd5286-refs/heads/main@{#1300313}

M       third_party/blink/renderer/core/inspector/build.gni
M       third_party/blink/renderer/core/inspector/inspector_page_agent.cc
M       third_party/blink/renderer/core/inspector/inspector_page_agent.h
A       third_party/blink/renderer/core/inspector/inspector_page_agent_unittest.cc

https://chromium-review.googlesource.com/5708170


### am...@chromium.org (2024-07-17)

The Chrome VRP panel has decided to award [crbug.com/338248595](https://crbug.com/338248595), the parent bug for this issue, a VRP reward of $20,000, because the reward has already been communicated and updated on [issue 338248595](https://issues.chromium.org/issues/338248595), updating the reward tag on this issue as 0.  

Congratulations Allen and nice work!

### ap...@google.com (2024-07-30)

Project: chromium/src
Branch: refs/branch-heads/6099

commit b3cb06fe890bb8d74d826e5c53031476d77c32c1
Author: Philip Pfaffe <pfaffe@chromium.org>
Date:   Tue Jul 30 14:41:18 2024

    [M120-LTS] Prevent script injection on reload when racing with a navigation
    
    M120 merge issues:
      third_party/blink/renderer/core/inspector/inspector_page_agent.cc:
        - loader_id isn't a parameter of reload() in 120, kept only the
        SetPending() relevant call.
        - the script.empty() check on DidCreateMainWorldContext() doesn't
        exist in 120. Kept the change as it is on the original fix, except
        for the evaluate call that also doesn't exist in 120.
    
    DevTools passes the loaderId now when calling Page.reload, in order to
    prevent accidentally reloading the wrong page when a navigation occurred
    concurrently. It can still happen that the navigation kicks in in between the reload iniated in the browser and the script injection that happens in the renderer, which would run the injected script on the wrong target. We need to check the loaderId also on the renderer side.
    
    (cherry picked from commit 43b8b682d05c75caf0daf1643b84575009cc0052)
    
    Fixed: 341136300
    Change-Id: I891fb37fa10e6789c8697a0f29bf7118788a9319
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5625857
    Commit-Queue: Philip Pfaffe <pfaffe@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1316330}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5672472
    Reviewed-by: Alex Rudenko <alexrudenko@chromium.org>
    Reviewed-by: Victor Gabriel Savu <vsavu@google.com>
    Commit-Queue: Roger Felipe Zanoni da Silva (xWF) <rzanoni@google.com>
    Cr-Commit-Position: refs/branch-heads/6099@{#2050}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}

M       third_party/blink/renderer/core/inspector/build.gni
M       third_party/blink/renderer/core/inspector/inspector_page_agent.cc
M       third_party/blink/renderer/core/inspector/inspector_page_agent.h
A       third_party/blink/renderer/core/inspector/inspector_page_agent_unittest.cc

https://chromium-review.googlesource.com/5672472


### pe...@google.com (2024-09-25)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/341136300)*
