# Security: Possible for extension to escape sandbox via Input.synthesizeTapGesture

| Field | Value |
|-------|-------|
| **Issue ID** | [40053103](https://issues.chromium.org/issues/40053103) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Platform>DevTools, Platform>Extensions |
| **Platforms** | Linux, Windows, ChromeOS |
| **Reporter** | de...@gmail.com |
| **Assignee** | ds...@chromium.org |
| **Created** | 2020-08-17 |
| **Bounty** | $10,000.00 |

## Description

**VULNERABILITY DETAILS**  

When using the chrome.debugger API, one of the methods an extension can call is Input.synthesizeTapGesture. That method allows tap gestures to be dispatched.

Because that method dispatches tap gestures to the active tab (rather than specifically the tab being debugged), an extension can dispatch a tap event to the chrome://downloads/ page. Doing this allows the extension to open a downloaded item by effectively clicking the associated link. This then allows the extension to escape the sandbox.

**VERSION**  

Chrome Version: Tested on 84.0.4147.125 (stable) and 86.0.4236.0 (canary)  

Operating System: Windows 10, version 2004

**REPRODUCTION CASE**

1. Install the attached extension.
2. Wait about 5 seconds.
3. The target executable (in this case, Process Explorer) should be started.

**CREDIT INFORMATION**  

Reporter credit: David Erceg

## Attachments

- [background.js](attachments/background.js) (text/plain, 5.9 KB)
- [manifest.json](attachments/manifest.json) (text/plain, 221 B)
- [page.html](attachments/page.html) (text/plain, 98 B)
- [page.js](attachments/page.js) (text/plain, 612 B)

## Timeline

### de...@gmail.com (2020-08-17)

Here are the steps the demonstration extension goes through:

1. The extension downloads the target executable.
2. It then opens chrome://downloads/ in a new tab.
3. Next, it opens page.html in a second tab and attaches the debugger to it using chrome.debugger.attach.
4. It then dispatches a tap gesture to page.html using Input.synthesizeTapGesture. This is done only so that the height of the top portion of the browser UI can be determined (the reason for this is explained below).
5. It then updates the chrome://downloads/ tab, to make it the active tab.
6. It then dispatches another tap gesture using Input.synthesizeTapGesture. Because the chrome://downloads/ tab was made active in step 5, the tap event will be dispatched to it. Using the fact that the position of the link for the first item on the downloads page can be deterministically calculated, the tap gesture is dispatched at that position. That results in the link being clicked and the file downloaded in step 1 being opened.

### de...@gmail.com (2020-08-17)

I believe the general reason why this works is that Input.synthesizeTapGesture dispatches the tap event to the root view, rather than a specific page:

https://source.chromium.org/chromium/chromium/src/+/master:content/browser/devtools/protocol/input_handler.cc;l=1412;drc=3d3ee67f6904c527aca96b54588cb1008a17b23e

So the tap event will be routed to whichever tab is active, rather than whichever tab has the debugger attached to it.

In step 4 in https://crbug.com/chromium/1117173#c1, it's mentioned that the height of the top portion of the browser UI is calculated by the extension. This is for the following reason:

The coordinates passed to Input.synthesizeTapGesture are client coordinates - that is, relative to the top left corner of the page.

From bisecting Chromium builds, it appears that a change made in 2019 means that when the gesture is dispatched to a tab other than the one being debugged (because another tab is the active tab), the coordinates are relative to the top left corner of the browser window. This is the relevant change:

https://crrev.com/d78b413dc9ad34a07b8ca1e3b9c3e640bb4a41f5

So that means that a point of (0,0) will refer to the top left corner of the browser window. Before that commit, (0,0) always referred to the top left corner of the page, regardless of which tab was active.

Ultimately, the demonstration extension here has to account for this. The left edge of the browser window is at the same point as the left edge of the page, so there's no change required there.

However, the extension needs to determine the height of the top portion of the browser UI (which includes the tab strip, omnibox, bookmarks toolbar and any infobars).

To do this, it dispatches a tap gesture to page.html at (0,0) using Input.synthesizeTapGesture. A click handler on the page can then retrieve the y coordinate of that click in screen coordinates using event.screenY. window.screenY indicates the position of the top of the browser in screen coordinates. event.screenY - window.screenY is then the height of the top part of the browser UI.

When the extension calculates the point that needs to be clicked to open the first item that appears on the downloads page, it offsets the y coordinate by the height of the top part of the browser UI.

Determining the point on the downloads page that needs to be clicked is simple enough, as the spacing between elements on the page is fixed.

The behavior above does mean that an extension can dispatch tap events to the top part of the browser UI. For example, calling Input.synthesizeTapGesture with a point of (10, 10) should select the first tab.

### va...@chromium.org (2020-08-17)

[Empty comment from Monorail migration]

[Monorail components: Platform>DevTools Platform>Extensions]

### co...@chromium.org (2020-08-17)

Some UI context:

NativeViewHostAura is for integrating platform native windows with our Views UI toolkit. It embeds an aura::Window inside a View. Chrome displays a tab's WebContents using this class. Each WebContents has its own OS-native window tree for rendering and input handling.

Since the hosted window isn't necessarily the same size as the host View, NativeViewHostAura creates a separate "clipping" window that tracks the bounds of the host View. The hosted window is reparented to this clipping window. This way, the hosted window won't be drawn outside the host View's bounds.

When a tab is active, its WebContents's window is a child of the clipping window positioned at (0,0) relative to it. When switching tabs, the old window is removed from the native window tree.

Before my CL the deactivating tab's window was moved to the clipping window's position. After, it's not modified at all.

My guess is the event synthesis code does the following:
1. Get the root window of the WebContents's native window tree. For active tabs, this is the clipping window. For inactive tabs, this is just WebContentsViewAura's window
2. Get the screen position of the root window
3. Offset this screen position by the arguments to Input.synthesizeTapGesture
4. Dispatch the event to the resulting screen coordinates

Since an inactive tab's screen position is now (0,0) this means the event is dispatched out of the active tab's contents. It seems like dispatching to the active tab, regardless of which tab is being debugged, only worked by accident.

However, I don't understand how this event dispatching works. I'm surprised the chrome.debugger API allows dispatching events outside of the debugged tab. Is this intentional? Seems like it was breaking sandboxing before my CL.

Adding folks with more context on event handling, and Devlin who is the extensions lead.

### bm...@chromium.org (2020-08-18)

[Empty comment from Monorail migration]

### [Deleted User] (2020-08-18)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-08-18)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-08-26)

[Empty comment from Monorail migration]

### ca...@chromium.org (2020-08-31)

[Empty comment from Monorail migration]

### ad...@google.com (2020-09-10)

caseq@ please could we have an update?

### [Deleted User] (2020-09-15)

caseq: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-09-29)

caseq: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-10-07)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-16)

We commit ourselves to a 60 day deadline for fixing for high severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### va...@chromium.org (2020-10-22)

Friendly ping from the security 👮 for this High severity bug. Any updates?

For high severity vulnerabilities, we aim to deploy the patch to all Chrome
users in under 60 days.

### [Deleted User] (2020-10-30)

[Empty comment from Monorail migration]

### [Deleted User] (2020-11-18)

[Empty comment from Monorail migration]

### ts...@chromium.org (2020-11-30)

Assigning up devtools mgt chain to see if we can get some traction on this issue.

### ca...@chromium.org (2020-11-30)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-20)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-03)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-11)

[Empty comment from Monorail migration]

### zh...@google.com (2021-03-17)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-15)

[Empty comment from Monorail migration]

### rs...@chromium.org (2021-05-05)

caseq: Any updates on this? 

### [Deleted User] (2021-05-26)

[Empty comment from Monorail migration]

### ad...@google.com (2021-07-08)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-05)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-07)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-16)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-11)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-22)

[Empty comment from Monorail migration]

### ad...@google.com (2021-09-23)

dsv@, should we hand this one over to you?

### ds...@chromium.org (2021-09-24)

Sure

### ds...@chromium.org (2021-09-30)

I cannot reproduce this now. Adding console.log to the page.js click handlers produces two log messages, so it looks like both input events are being dispatched correctly.

### de...@gmail.com (2021-10-04)

The demonstration extension still reproduces the issue for me on Chrome 96.0.4660.4 (canary) on Windows 10.

It's also simple enough to verify whether or not input events can be dispatched to places outside of the tab being debugged. For example, going through the following steps should result in the first tab being selected:

1. Create a new tab.
2. From an extension with the debugger permission, use chrome.debugger.attach to attach the debugger to the tab.
3. Switch to another tab,
4. From the extension run:

chrome.debugger.sendCommand({tabId: targetTabId}, "Input.synthesizeTapGesture", {x: 10, y: 10, tapCount: 1});

(10, 10) is within the bounds of the first tab in the tab strip and should result in that tab being selected.

### ds...@chromium.org (2021-10-04)

I see, I can reproduce on Linux as well. It just doesn't reproduce on Mac.

### dt...@chromium.org (2021-10-07)

[Empty comment from Monorail migration]

### fl...@chromium.org (2021-10-07)

[Empty comment from Monorail migration]

### ds...@chromium.org (2021-10-12)

[Empty comment from Monorail migration]

### ds...@chromium.org (2021-10-19)

[Empty comment from Monorail migration]

### ke...@chromium.org (2021-10-19)

[Empty comment from Monorail migration]

### ke...@chromium.org (2021-10-19)

https://crbug.com/chromium/1117173#c2 and https://crbug.com/chromium/1117173#c4 almost captured the root cause, but with slightly vague use of the Aura terminology. I will try to clarify.

In Aura, there are two structures: aura::Window and WindowTreeHost. aura::Window represents virtual windows, including tabs, bubbles and menus. WindowTreeHost represents physical windows backed by os' native windows. A WindowTreeHost, as its name suggests, hosts trees of aura::Windows.

Input.synthesizeTapGesture injects events to a WindowTreeHost [1], so it appears to send event to the browser window. It should inject to the aura::Window instead, presumably by using aura::Window::delegate()->OnEvent(). 

[1] https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/input/synthetic_gesture_target_aura.cc;drc=34bf2c428f6a94b662601151aef4211a32dde74d;l=69

### mu...@chromium.org (2021-10-20)

I agree with https://crbug.com/chromium/1117173#c47.  |EventInjector| is designed [1] to mimic OS input, so any access to this class from a content-exposed API (like chrome.debugger in this case) should be restricted in a manner suggested in https://crbug.com/chromium/1117173#c47.  

Another fix could be making event->ConvertLocationToTarget() aware of the corner case mentioned in https://crbug.com/chromium/1117173#c4.  I can see in synthetic_gesture_target_aura.cc that all (five) callers of event_injector_.Inject() first "fixes" event location using ConvertLocationToTarget() [2].  Can't we add some clipping/clamping etc in this location fixer method?

[1] https://source.chromium.org/chromium/chromium/src/+/main:ui/aura/event_injector.h;drc=c8c123536f8e93a36ba0f032674accdd77a62215;l=20
[2] https://source.chromium.org/search?q=file:synthetic_gesture_target_aura.cc%20event_injector_.Inject&ss=chromium%2Fchromium%2Fsrc

### ke...@chromium.org (2021-10-20)

I think fixing location is not enough. Even if we clip the event to the content area (so that debugger has no way to click on the toolbar), the event will be sent to the active window, rather than the tab the debugger attaches to. 

### gi...@appspot.gserviceaccount.com (2021-11-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/devtools/devtools-frontend/+/e210181996259e41fa926cc79e788d7a44e22a86

commit e210181996259e41fa926cc79e788d7a44e22a86
Author: Danil Somsikov <dsv@chromium.org>
Date: Fri Nov 05 13:58:56 2021

Extract a few useful helper functions out of a specific browser test case

Bug: 1117173
Change-Id: Ia35fd52c8f8f88955dd705a968958d8f49e4cd1c
Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/3264204
Reviewed-by: Simon Zünd <szuend@chromium.org>
Commit-Queue: Danil Somsikov <dsv@chromium.org>

[modify] https://crrev.com/e210181996259e41fa926cc79e788d7a44e22a86/front_end/Tests.js


### gi...@appspot.gserviceaccount.com (2021-11-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/7d1caa6ede42056461b2ededf4d983d28c68e073

commit 7d1caa6ede42056461b2ededf4d983d28c68e073
Author: Danil Somsikov <dsv@chromium.org>
Date: Fri Nov 05 18:43:54 2021

Add from_devtools_debugger parameter to gesture params and pointer
driver and use it to set kFromDebugger modififier.

This modifier will be used for a different event routing in target.

Bug: 1117173
Change-Id: I0da662f4dffee7eb0702bf99e901d3cbbdf6135b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3259628
Reviewed-by: Dave Tapuska <dtapuska@chromium.org>
Reviewed-by: Keren Zhu <kerenzhu@chromium.org>
Commit-Queue: Danil Somsikov <dsv@chromium.org>
Cr-Commit-Position: refs/heads/main@{#938874}

[modify] https://crrev.com/7d1caa6ede42056461b2ededf4d983d28c68e073/content/browser/renderer_host/input/synthetic_pointer_action_unittest.cc
[modify] https://crrev.com/7d1caa6ede42056461b2ededf4d983d28c68e073/content/browser/renderer_host/input/synthetic_touch_driver.cc
[modify] https://crrev.com/7d1caa6ede42056461b2ededf4d983d28c68e073/content/common/input/synthetic_gesture_params.h
[modify] https://crrev.com/7d1caa6ede42056461b2ededf4d983d28c68e073/content/browser/renderer_host/input/synthetic_pen_driver.cc
[modify] https://crrev.com/7d1caa6ede42056461b2ededf4d983d28c68e073/content/browser/renderer_host/input/synthetic_pointer_action.cc
[modify] https://crrev.com/7d1caa6ede42056461b2ededf4d983d28c68e073/content/browser/renderer_host/input/synthetic_mouse_driver.cc
[modify] https://crrev.com/7d1caa6ede42056461b2ededf4d983d28c68e073/content/browser/renderer_host/input/synthetic_pointer_driver.h
[modify] https://crrev.com/7d1caa6ede42056461b2ededf4d983d28c68e073/content/browser/renderer_host/input/synthetic_pointer_driver.cc
[modify] https://crrev.com/7d1caa6ede42056461b2ededf4d983d28c68e073/content/common/input/synthetic_gesture_params.cc


### gi...@appspot.gserviceaccount.com (2021-11-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/d8c84a421a745f7df370feb26495bd92b7be44e8

commit d8c84a421a745f7df370feb26495bd92b7be44e8
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Fri Nov 05 22:33:21 2021

Roll DevTools Frontend from ab2249a5c608 to e21018199625 (9 revisions)

https://chromium.googlesource.com/devtools/devtools-frontend.git/+log/ab2249a5c608..e21018199625

2021-11-05 dsv@chromium.org Extract a few useful helper functions out of a specific browser test case
2021-11-05 tvanderlippe@chromium.org Fix focus debuggee command
2021-11-05 tvanderlippe@chromium.org Reland "Fix all issues found by StyleLint 14"
2021-11-05 tvanderlippe@chromium.org Fix eslint tests for Windows
2021-11-05 kahinds@microsoft.com Emulate `forced-colors` media feature UI
2021-11-05 devtools-ci-autoroll-builder@chops-service-accounts.iam.gserviceaccount.com Update DevTools DEPS.
2021-11-05 kprokopenko@chromium.org Improve accessibility of hide issues 3 dot menu
2021-11-05 mathias@chromium.org Support arbitrary characters in Network Search queries
2021-11-05 yangguo@chromium.org Consistently use red color for animation scrub

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/devtools-frontend-chromium
Please CC devtools-waterfall-sheriff-onduty@grotations.appspotmail.com on the revert to ensure that a human
is aware of the problem.

To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Bug: chromium:1117173,chromium:1130859,chromium:1254681
Tbr: devtools-waterfall-sheriff-onduty@grotations.appspotmail.com
Change-Id: Ic6b86189933192b20321ed8f197b3c9438708090
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3261979
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#938988}

[modify] https://crrev.com/d8c84a421a745f7df370feb26495bd92b7be44e8/DEPS


### gi...@appspot.gserviceaccount.com (2021-11-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/devtools/devtools-frontend/+/12509d78acea044e226d57d7212a47747b7ba140

commit 12509d78acea044e226d57d7212a47747b7ba140
Author: Danil Somsikov <dsv@chromium.org>
Date: Fri Nov 05 14:03:47 2021

Add test to verify correct routing of synthetic events

Bug: 1117173
Change-Id: I8a4a11394c547303e0a6508c6d9a83113bd58924
Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/3264205
Commit-Queue: Danil Somsikov <dsv@chromium.org>
Auto-Submit: Danil Somsikov <dsv@chromium.org>
Reviewed-by: Simon Zünd <szuend@chromium.org>

[modify] https://crrev.com/12509d78acea044e226d57d7212a47747b7ba140/front_end/Tests.js


### gi...@appspot.gserviceaccount.com (2021-11-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b760dabb9781d894541a9b27961ea5f825077627

commit b760dabb9781d894541a9b27961ea5f825077627
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Mon Nov 08 12:50:25 2021

Roll DevTools Frontend from 3f5d0240c56c to 264703fc1129 (5 revisions)

https://chromium.googlesource.com/devtools/devtools-frontend.git/+log/3f5d0240c56c..264703fc1129

2021-11-08 tvanderlippe@chromium.org Add loadLegacyModule on Runtime for browser tests
2021-11-08 sadym@chromium.org Disable flaky test.
2021-11-08 kprokopenko@chromium.org Improve accessibility of Query String Parameters buttons in
2021-11-08 dsv@chromium.org Add myself to front_end/OWNERS
2021-11-08 dsv@chromium.org Add test to verify correct routing of synthetic events

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/devtools-frontend-chromium
Please CC devtools-waterfall-sheriff-onduty@grotations.appspotmail.com on the revert to ensure that a human
is aware of the problem.

To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Bug: chromium:1117173,chromium:1148291,chromium:1245541,chromium:1266640
Tbr: devtools-waterfall-sheriff-onduty@grotations.appspotmail.com
Change-Id: Ib4aac667bea2635fd02763092789c8c108010fbe
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3267555
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#939322}

[modify] https://crrev.com/b760dabb9781d894541a9b27961ea5f825077627/DEPS


### gi...@appspot.gserviceaccount.com (2021-11-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/39baf6a25f3035f2de59af22a554493516a086d5

commit 39baf6a25f3035f2de59af22a554493516a086d5
Author: Danil Somsikov <dsv@chromium.org>
Date: Tue Nov 09 21:01:23 2021

Propagate from_devtools_debugger in gestures.

Bug: 1117173
Change-Id: I1f093a97aec0bb898afca66d27404af79670f1ac
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3259636
Commit-Queue: Danil Somsikov <dsv@chromium.org>
Reviewed-by: Dave Tapuska <dtapuska@chromium.org>
Reviewed-by: Keren Zhu <kerenzhu@chromium.org>
Cr-Commit-Position: refs/heads/main@{#940000}

[modify] https://crrev.com/39baf6a25f3035f2de59af22a554493516a086d5/content/browser/renderer_host/input/synthetic_gesture_controller_unittest.cc
[modify] https://crrev.com/39baf6a25f3035f2de59af22a554493516a086d5/content/browser/renderer_host/input/synthetic_touchpad_pinch_gesture.cc
[modify] https://crrev.com/39baf6a25f3035f2de59af22a554493516a086d5/content/browser/renderer_host/input/synthetic_touchscreen_pinch_gesture.cc
[modify] https://crrev.com/39baf6a25f3035f2de59af22a554493516a086d5/content/browser/renderer_host/input/synthetic_tap_gesture.cc
[modify] https://crrev.com/39baf6a25f3035f2de59af22a554493516a086d5/content/browser/renderer_host/input/synthetic_smooth_move_gesture.h
[modify] https://crrev.com/39baf6a25f3035f2de59af22a554493516a086d5/content/browser/renderer_host/input/synthetic_smooth_scroll_gesture.cc
[modify] https://crrev.com/39baf6a25f3035f2de59af22a554493516a086d5/content/browser/renderer_host/input/synthetic_smooth_drag_gesture.cc
[modify] https://crrev.com/39baf6a25f3035f2de59af22a554493516a086d5/content/browser/renderer_host/input/synthetic_smooth_move_gesture.cc


### [Deleted User] (2021-11-15)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-11-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/8a8a3311f21bf6e164403df68338549ead56ab03

commit 8a8a3311f21bf6e164403df68338549ead56ab03
Author: Danil Somsikov <dsv@chromium.org>
Date: Wed Nov 17 10:18:29 2021

Set from_devtools_debugger in CDP events handler and use it in aura gesture target to dispatch to the specific view instead of a root window.

Bug: 1117173
Change-Id: I02eaa35b8f4bd961018c5d8d80eb639319baeb8f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3263968
Commit-Queue: Danil Somsikov <dsv@chromium.org>
Reviewed-by: Andrey Kosyakov <caseq@chromium.org>
Reviewed-by: Keren Zhu <kerenzhu@chromium.org>
Reviewed-by: Dave Tapuska <dtapuska@chromium.org>
Cr-Commit-Position: refs/heads/main@{#942533}

[modify] https://crrev.com/8a8a3311f21bf6e164403df68338549ead56ab03/chrome/browser/devtools/protocol/devtools_protocol_browsertest.cc
[modify] https://crrev.com/8a8a3311f21bf6e164403df68338549ead56ab03/content/browser/renderer_host/input/synthetic_gesture_target_aura.cc
[modify] https://crrev.com/8a8a3311f21bf6e164403df68338549ead56ab03/content/browser/devtools/protocol/input_handler.cc


### ds...@chromium.org (2021-11-17)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-11-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/devtools/devtools-frontend/+/5393258246a45f76573e726e3062531092c3b329

commit 5393258246a45f76573e726e3062531092c3b329
Author: Danil Somsikov <dsv@chromium.org>
Date: Tue Nov 16 19:32:11 2021

Revert "Add test to verify correct routing of synthetic events"

This reverts commit 12509d78acea044e226d57d7212a47747b7ba140.

Reason for revert: Implemented browser test differently on the chromium side

Original change's description:
> Add test to verify correct routing of synthetic events
>
> Bug: 1117173
> Change-Id: I8a4a11394c547303e0a6508c6d9a83113bd58924
> Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/3264205
> Commit-Queue: Danil Somsikov <dsv@chromium.org>
> Auto-Submit: Danil Somsikov <dsv@chromium.org>
> Reviewed-by: Simon Zünd <szuend@chromium.org>

Bug: 1117173
Change-Id: I86600c3fd34e394230429dcc01c07605d9029ee6
Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/3284819
Reviewed-by: Simon Zünd <szuend@chromium.org>
Commit-Queue: Danil Somsikov <dsv@chromium.org>

[modify] https://crrev.com/5393258246a45f76573e726e3062531092c3b329/front_end/Tests.js


### ds...@chromium.org (2021-11-17)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-11-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/1ce2a9705ea298a095e9fcb76dab86ae148288f7

commit 1ce2a9705ea298a095e9fcb76dab86ae148288f7
Author: Danil Somsikov <dsv@chromium.org>
Date: Wed Nov 17 13:01:45 2021

Fix DevToolsProtocolTest.InputDispatchEventsToCorrectTarget

Bug: 1117173
Change-Id: I7fd46360201c04093192ccc2d8e0ea3fa0dabe44
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3288691
Commit-Queue: Danil Somsikov <dsv@chromium.org>
Commit-Queue: Yang Guo <yangguo@chromium.org>
Auto-Submit: Danil Somsikov <dsv@chromium.org>
Reviewed-by: Yang Guo <yangguo@chromium.org>
Cr-Commit-Position: refs/heads/main@{#942566}

[modify] https://crrev.com/1ce2a9705ea298a095e9fcb76dab86ae148288f7/chrome/browser/devtools/protocol/devtools_protocol_browsertest.cc


### gi...@appspot.gserviceaccount.com (2021-11-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/7afe0cfe101cff18ca4a88d7cdc4f890f1292515

commit 7afe0cfe101cff18ca4a88d7cdc4f890f1292515
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Wed Nov 17 13:01:36 2021

Roll DevTools Frontend from 89ee3035df04 to 5393258246a4 (1 revision)

https://chromium.googlesource.com/devtools/devtools-frontend.git/+log/89ee3035df04..5393258246a4

2021-11-17 dsv@chromium.org Revert "Add test to verify correct routing of synthetic events"

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/devtools-frontend-chromium
Please CC devtools-waterfall-sheriff-onduty@grotations.appspotmail.com on the revert to ensure that a human
is aware of the problem.

To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Bug: chromium:1117173
Tbr: devtools-waterfall-sheriff-onduty@grotations.appspotmail.com
Change-Id: Ie04a1650a91c6cfbe551b628213cdf76d69d3582
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3289331
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#942565}

[modify] https://crrev.com/7afe0cfe101cff18ca4a88d7cdc4f890f1292515/DEPS


### gi...@appspot.gserviceaccount.com (2021-11-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/cbea10c3e252c61a37cb0ae84f5fc8675f8c32b2

commit cbea10c3e252c61a37cb0ae84f5fc8675f8c32b2
Author: Danil Somsikov <dsv@chromium.org>
Date: Wed Nov 17 15:27:26 2021

Revert "Fix DevToolsProtocolTest.InputDispatchEventsToCorrectTarget"

This reverts commit 1ce2a9705ea298a095e9fcb76dab86ae148288f7.

Reason for revert: Still failing

Original change's description:
> Fix DevToolsProtocolTest.InputDispatchEventsToCorrectTarget
>
> Bug: 1117173
> Change-Id: I7fd46360201c04093192ccc2d8e0ea3fa0dabe44
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3288691
> Commit-Queue: Danil Somsikov <dsv@chromium.org>
> Commit-Queue: Yang Guo <yangguo@chromium.org>
> Auto-Submit: Danil Somsikov <dsv@chromium.org>
> Reviewed-by: Yang Guo <yangguo@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#942566}

Bug: 1117173
Change-Id: I86c050fcdcfd8c8c67eb94bce277efd7e096f097
No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3288990
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Owners-Override: Olga Sharonova <olka@google.com>
Commit-Queue: Danil Somsikov <dsv@chromium.org>
Cr-Commit-Position: refs/heads/main@{#942611}

[modify] https://crrev.com/cbea10c3e252c61a37cb0ae84f5fc8675f8c32b2/chrome/browser/devtools/protocol/devtools_protocol_browsertest.cc


### gi...@appspot.gserviceaccount.com (2021-11-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/2f6c66c4d269301b52cee896d0bdfd749a77919b

commit 2f6c66c4d269301b52cee896d0bdfd749a77919b
Author: Danil Somsikov <dsv@chromium.org>
Date: Wed Nov 17 15:34:46 2021

Revert "Set from_devtools_debugger in CDP events handler and use it in aura gesture target to dispatch to the specific view instead of a root window."

This reverts commit 8a8a3311f21bf6e164403df68338549ead56ab03.

Reason for revert: Fails tests

Original change's description:
> Set from_devtools_debugger in CDP events handler and use it in aura gesture target to dispatch to the specific view instead of a root window.
>
> Bug: 1117173
> Change-Id: I02eaa35b8f4bd961018c5d8d80eb639319baeb8f
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3263968
> Commit-Queue: Danil Somsikov <dsv@chromium.org>
> Reviewed-by: Andrey Kosyakov <caseq@chromium.org>
> Reviewed-by: Keren Zhu <kerenzhu@chromium.org>
> Reviewed-by: Dave Tapuska <dtapuska@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#942533}

Bug: 1117173
Change-Id: I23a5351d6367ac1c795202a7b8313fb170a351c7
No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3289267
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Owners-Override: Olga Sharonova <olka@google.com>
Commit-Queue: Danil Somsikov <dsv@chromium.org>
Cr-Commit-Position: refs/heads/main@{#942614}

[modify] https://crrev.com/2f6c66c4d269301b52cee896d0bdfd749a77919b/chrome/browser/devtools/protocol/devtools_protocol_browsertest.cc
[modify] https://crrev.com/2f6c66c4d269301b52cee896d0bdfd749a77919b/content/browser/renderer_host/input/synthetic_gesture_target_aura.cc
[modify] https://crrev.com/2f6c66c4d269301b52cee896d0bdfd749a77919b/content/browser/devtools/protocol/input_handler.cc


### gi...@appspot.gserviceaccount.com (2021-11-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/42f3de93ec0ae3cd8e855aec1631a26baf66a523

commit 42f3de93ec0ae3cd8e855aec1631a26baf66a523
Author: Danil Somsikov <dsv@chromium.org>
Date: Thu Nov 18 08:08:43 2021

Reland "Set from_devtools_debugger in CDP events handler and use it in aura gesture target to dispatch to the specific view instead of a root window."

This is a reland of 8a8a3311f21bf6e164403df68338549ead56ab03

Original change's description:
> Set from_devtools_debugger in CDP events handler and use it in aura gesture target to dispatch to the specific view instead of a root window.
>
> Bug: 1117173
> Change-Id: I02eaa35b8f4bd961018c5d8d80eb639319baeb8f
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3263968
> Commit-Queue: Danil Somsikov <dsv@chromium.org>
> Reviewed-by: Andrey Kosyakov <caseq@chromium.org>
> Reviewed-by: Keren Zhu <kerenzhu@chromium.org>
> Reviewed-by: Dave Tapuska <dtapuska@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#942533}

Bug: 1117173
Change-Id: Ideee602bedfaec59c1077b57e46de29605ac7500
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3289268
Commit-Queue: Danil Somsikov <dsv@chromium.org>
Reviewed-by: Keren Zhu <kerenzhu@chromium.org>
Reviewed-by: Dave Tapuska <dtapuska@chromium.org>
Reviewed-by: Andrey Kosyakov <caseq@chromium.org>
Cr-Commit-Position: refs/heads/main@{#942994}

[modify] https://crrev.com/42f3de93ec0ae3cd8e855aec1631a26baf66a523/chrome/browser/devtools/protocol/devtools_protocol_browsertest.cc
[modify] https://crrev.com/42f3de93ec0ae3cd8e855aec1631a26baf66a523/content/browser/renderer_host/input/synthetic_gesture_target_aura.cc
[modify] https://crrev.com/42f3de93ec0ae3cd8e855aec1631a26baf66a523/content/browser/devtools/protocol/input_handler.cc


### ds...@chromium.org (2021-11-18)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-20)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-20)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-20)

Requesting merge to stable M96 because latest trunk commit (942533) appears to be after stable branch point (929512).

Requesting merge to beta M97 because latest trunk commit (942533) appears to be after beta branch point (938553).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-11-20)

Merge review required: a commit with DEPS changes was detected.

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
Owners: benmason (Android), harrysouders (iOS), ceb (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-11-20)

Merge review required: a commit with DEPS changes was detected.

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
Owners: govind (Android), harrysouders (iOS), dgagnon (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2021-11-24)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-11-24)

Congratulations -- the VRP Panel has decided to award you $10,000 for this report! Thank you for this report as well as catching that this issue wasn't fully mitigated and also for your patience throughout. 

### am...@google.com (2021-11-24)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-11-29)

merge approved for M97; please merge to branch 4692 ASAP so this can be included in tomorrow's beta cut 

### pb...@google.com (2021-11-29)

Your change has been approved for M97 branch,please go ahead and merge the CL's to M97 branch:4692 manually asap so that they would be part of this week's first M97 Beta release.

### gi...@appspot.gserviceaccount.com (2021-11-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b928de80cf41ffea6e7530510f5afded3c9d5dbd

commit b928de80cf41ffea6e7530510f5afded3c9d5dbd
Author: Danil Somsikov <dsv@chromium.org>
Date: Tue Nov 30 15:47:36 2021

Add from_devtools_debugger parameter to gesture params and pointer
driver and use it to set kFromDebugger modififier.

This modifier will be used for a different event routing in target.

(cherry picked from commit 7d1caa6ede42056461b2ededf4d983d28c68e073)

Bug: 1117173
Change-Id: I0da662f4dffee7eb0702bf99e901d3cbbdf6135b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3259628
Reviewed-by: Dave Tapuska <dtapuska@chromium.org>
Reviewed-by: Keren Zhu <kerenzhu@chromium.org>
Commit-Queue: Danil Somsikov <dsv@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#938874}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3306401
Cr-Commit-Position: refs/branch-heads/4692@{#581}
Cr-Branched-From: 038cd96142d384c0d2238973f1cb277725a62eba-refs/heads/main@{#938553}

[modify] https://crrev.com/b928de80cf41ffea6e7530510f5afded3c9d5dbd/content/browser/renderer_host/input/synthetic_pointer_action_unittest.cc
[modify] https://crrev.com/b928de80cf41ffea6e7530510f5afded3c9d5dbd/content/browser/renderer_host/input/synthetic_touch_driver.cc
[modify] https://crrev.com/b928de80cf41ffea6e7530510f5afded3c9d5dbd/content/common/input/synthetic_gesture_params.h
[modify] https://crrev.com/b928de80cf41ffea6e7530510f5afded3c9d5dbd/content/browser/renderer_host/input/synthetic_pen_driver.cc
[modify] https://crrev.com/b928de80cf41ffea6e7530510f5afded3c9d5dbd/content/browser/renderer_host/input/synthetic_pointer_action.cc
[modify] https://crrev.com/b928de80cf41ffea6e7530510f5afded3c9d5dbd/content/browser/renderer_host/input/synthetic_mouse_driver.cc
[modify] https://crrev.com/b928de80cf41ffea6e7530510f5afded3c9d5dbd/content/browser/renderer_host/input/synthetic_pointer_driver.h
[modify] https://crrev.com/b928de80cf41ffea6e7530510f5afded3c9d5dbd/content/browser/renderer_host/input/synthetic_pointer_driver.cc
[modify] https://crrev.com/b928de80cf41ffea6e7530510f5afded3c9d5dbd/content/common/input/synthetic_gesture_params.cc


### gi...@appspot.gserviceaccount.com (2021-11-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/dd478b5b72d26df36ad4e49576771ceaebc91c81

commit dd478b5b72d26df36ad4e49576771ceaebc91c81
Author: Danil Somsikov <dsv@chromium.org>
Date: Tue Nov 30 15:48:09 2021

Propagate from_devtools_debugger in gestures.

(cherry picked from commit 39baf6a25f3035f2de59af22a554493516a086d5)

Bug: 1117173
Change-Id: I1f093a97aec0bb898afca66d27404af79670f1ac
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3259636
Commit-Queue: Danil Somsikov <dsv@chromium.org>
Reviewed-by: Dave Tapuska <dtapuska@chromium.org>
Reviewed-by: Keren Zhu <kerenzhu@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#940000}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3307039
Cr-Commit-Position: refs/branch-heads/4692@{#582}
Cr-Branched-From: 038cd96142d384c0d2238973f1cb277725a62eba-refs/heads/main@{#938553}

[modify] https://crrev.com/dd478b5b72d26df36ad4e49576771ceaebc91c81/content/browser/renderer_host/input/synthetic_gesture_controller_unittest.cc
[modify] https://crrev.com/dd478b5b72d26df36ad4e49576771ceaebc91c81/content/browser/renderer_host/input/synthetic_touchpad_pinch_gesture.cc
[modify] https://crrev.com/dd478b5b72d26df36ad4e49576771ceaebc91c81/content/browser/renderer_host/input/synthetic_touchscreen_pinch_gesture.cc
[modify] https://crrev.com/dd478b5b72d26df36ad4e49576771ceaebc91c81/content/browser/renderer_host/input/synthetic_tap_gesture.cc
[modify] https://crrev.com/dd478b5b72d26df36ad4e49576771ceaebc91c81/content/browser/renderer_host/input/synthetic_smooth_move_gesture.h
[modify] https://crrev.com/dd478b5b72d26df36ad4e49576771ceaebc91c81/content/browser/renderer_host/input/synthetic_smooth_scroll_gesture.cc
[modify] https://crrev.com/dd478b5b72d26df36ad4e49576771ceaebc91c81/content/browser/renderer_host/input/synthetic_smooth_move_gesture.cc
[modify] https://crrev.com/dd478b5b72d26df36ad4e49576771ceaebc91c81/content/browser/renderer_host/input/synthetic_smooth_drag_gesture.cc


### gi...@appspot.gserviceaccount.com (2021-12-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/dc80138b8fffa70558d7fbfe8445a5bb94304fbf

commit dc80138b8fffa70558d7fbfe8445a5bb94304fbf
Author: Danil Somsikov <dsv@chromium.org>
Date: Wed Dec 01 09:29:13 2021

Reland "Set from_devtools_debugger in CDP events handler and use it in aura gesture target to dispatch to the specific view instead of a root window."

This is a reland of 8a8a3311f21bf6e164403df68338549ead56ab03

Original change's description:
> Set from_devtools_debugger in CDP events handler and use it in aura gesture target to dispatch to the specific view instead of a root window.
>
> Bug: 1117173
> Change-Id: I02eaa35b8f4bd961018c5d8d80eb639319baeb8f
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3263968
> Commit-Queue: Danil Somsikov <dsv@chromium.org>
> Reviewed-by: Andrey Kosyakov <caseq@chromium.org>
> Reviewed-by: Keren Zhu <kerenzhu@chromium.org>
> Reviewed-by: Dave Tapuska <dtapuska@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#942533}

(cherry picked from commit 42f3de93ec0ae3cd8e855aec1631a26baf66a523)

Bug: 1117173
Change-Id: Ideee602bedfaec59c1077b57e46de29605ac7500
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3289268
Commit-Queue: Danil Somsikov <dsv@chromium.org>
Reviewed-by: Keren Zhu <kerenzhu@chromium.org>
Reviewed-by: Dave Tapuska <dtapuska@chromium.org>
Reviewed-by: Andrey Kosyakov <caseq@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#942994}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3306366
Cr-Commit-Position: refs/branch-heads/4692@{#618}
Cr-Branched-From: 038cd96142d384c0d2238973f1cb277725a62eba-refs/heads/main@{#938553}

[modify] https://crrev.com/dc80138b8fffa70558d7fbfe8445a5bb94304fbf/chrome/browser/devtools/protocol/devtools_protocol_browsertest.cc
[modify] https://crrev.com/dc80138b8fffa70558d7fbfe8445a5bb94304fbf/content/browser/renderer_host/input/synthetic_gesture_target_aura.cc
[modify] https://crrev.com/dc80138b8fffa70558d7fbfe8445a5bb94304fbf/content/browser/devtools/protocol/input_handler.cc


### ad...@google.com (2021-12-09)

As this was approved to M97, we should also approve for M96 as it is Extended Stable. Approving merge to M96 branch 4664. If this is for some reason especially difficult to merge to M96, let us know and we can discuss.

### gi...@appspot.gserviceaccount.com (2021-12-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/d9355c804504f688f4f9501e51e49347ea721e9b

commit d9355c804504f688f4f9501e51e49347ea721e9b
Author: Danil Somsikov <dsv@chromium.org>
Date: Tue Dec 14 07:59:49 2021

Propagate from_devtools_debugger in gestures.

(cherry picked from commit 39baf6a25f3035f2de59af22a554493516a086d5)

Bug: 1117173
Change-Id: I1f093a97aec0bb898afca66d27404af79670f1ac
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3259636
Commit-Queue: Danil Somsikov <dsv@chromium.org>
Reviewed-by: Dave Tapuska <dtapuska@chromium.org>
Reviewed-by: Keren Zhu <kerenzhu@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#940000}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3329863
Cr-Commit-Position: refs/branch-heads/4664@{#1301}
Cr-Branched-From: 24dc4ee75e01a29d390d43c9c264372a169273a7-refs/heads/main@{#929512}

[modify] https://crrev.com/d9355c804504f688f4f9501e51e49347ea721e9b/content/browser/renderer_host/input/synthetic_gesture_controller_unittest.cc
[modify] https://crrev.com/d9355c804504f688f4f9501e51e49347ea721e9b/content/browser/renderer_host/input/synthetic_touchpad_pinch_gesture.cc
[modify] https://crrev.com/d9355c804504f688f4f9501e51e49347ea721e9b/content/browser/renderer_host/input/synthetic_touchscreen_pinch_gesture.cc
[modify] https://crrev.com/d9355c804504f688f4f9501e51e49347ea721e9b/content/browser/renderer_host/input/synthetic_tap_gesture.cc
[modify] https://crrev.com/d9355c804504f688f4f9501e51e49347ea721e9b/content/browser/renderer_host/input/synthetic_smooth_move_gesture.h
[modify] https://crrev.com/d9355c804504f688f4f9501e51e49347ea721e9b/content/browser/renderer_host/input/synthetic_smooth_scroll_gesture.cc
[modify] https://crrev.com/d9355c804504f688f4f9501e51e49347ea721e9b/content/browser/renderer_host/input/synthetic_smooth_drag_gesture.cc
[modify] https://crrev.com/d9355c804504f688f4f9501e51e49347ea721e9b/content/browser/renderer_host/input/synthetic_smooth_move_gesture.cc


### gi...@appspot.gserviceaccount.com (2021-12-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/f47ac69cbc9b2268e8b440624121922a60b6d121

commit f47ac69cbc9b2268e8b440624121922a60b6d121
Author: Danil Somsikov <dsv@chromium.org>
Date: Tue Dec 14 07:59:22 2021

Add from_devtools_debugger parameter to gesture params and pointer
driver and use it to set kFromDebugger modififier.

This modifier will be used for a different event routing in target.

(cherry picked from commit 7d1caa6ede42056461b2ededf4d983d28c68e073)

Bug: 1117173
Change-Id: I0da662f4dffee7eb0702bf99e901d3cbbdf6135b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3259628
Reviewed-by: Dave Tapuska <dtapuska@chromium.org>
Reviewed-by: Keren Zhu <kerenzhu@chromium.org>
Commit-Queue: Danil Somsikov <dsv@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#938874}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3329604
Cr-Commit-Position: refs/branch-heads/4664@{#1300}
Cr-Branched-From: 24dc4ee75e01a29d390d43c9c264372a169273a7-refs/heads/main@{#929512}

[modify] https://crrev.com/f47ac69cbc9b2268e8b440624121922a60b6d121/content/browser/renderer_host/input/synthetic_pointer_action_unittest.cc
[modify] https://crrev.com/f47ac69cbc9b2268e8b440624121922a60b6d121/content/browser/renderer_host/input/synthetic_touch_driver.cc
[modify] https://crrev.com/f47ac69cbc9b2268e8b440624121922a60b6d121/content/common/input/synthetic_gesture_params.h
[modify] https://crrev.com/f47ac69cbc9b2268e8b440624121922a60b6d121/content/browser/renderer_host/input/synthetic_pen_driver.cc
[modify] https://crrev.com/f47ac69cbc9b2268e8b440624121922a60b6d121/content/browser/renderer_host/input/synthetic_pointer_action.cc
[modify] https://crrev.com/f47ac69cbc9b2268e8b440624121922a60b6d121/content/browser/renderer_host/input/synthetic_mouse_driver.cc
[modify] https://crrev.com/f47ac69cbc9b2268e8b440624121922a60b6d121/content/browser/renderer_host/input/synthetic_pointer_driver.h
[modify] https://crrev.com/f47ac69cbc9b2268e8b440624121922a60b6d121/content/browser/renderer_host/input/synthetic_pointer_driver.cc
[modify] https://crrev.com/f47ac69cbc9b2268e8b440624121922a60b6d121/content/common/input/synthetic_gesture_params.cc


### gi...@appspot.gserviceaccount.com (2021-12-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/2209dbe47389fb257374a7a6ce1b18722daeaf79

commit 2209dbe47389fb257374a7a6ce1b18722daeaf79
Author: Danil Somsikov <dsv@chromium.org>
Date: Tue Dec 14 09:00:04 2021

[m96] Reland "Set from_devtools_debugger in CDP events handler and use it in aura gesture target to dispatch to the specific view instead of a root window."

This is a reland of 8a8a3311f21bf6e164403df68338549ead56ab03

Original change's description:
> Set from_devtools_debugger in CDP events handler and use it in aura gesture target to dispatch to the specific view instead of a root window.
>
> Bug: 1117173
> Change-Id: I02eaa35b8f4bd961018c5d8d80eb639319baeb8f
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3263968
> Commit-Queue: Danil Somsikov <dsv@chromium.org>
> Reviewed-by: Andrey Kosyakov <caseq@chromium.org>
> Reviewed-by: Keren Zhu <kerenzhu@chromium.org>
> Reviewed-by: Dave Tapuska <dtapuska@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#942533}

(cherry picked from commit 42f3de93ec0ae3cd8e855aec1631a26baf66a523)

Bug: 1117173
Change-Id: Ideee602bedfaec59c1077b57e46de29605ac7500
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3289268
Commit-Queue: Danil Somsikov <dsv@chromium.org>
Reviewed-by: Keren Zhu <kerenzhu@chromium.org>
Reviewed-by: Dave Tapuska <dtapuska@chromium.org>
Reviewed-by: Andrey Kosyakov <caseq@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#942994}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3329843
Cr-Commit-Position: refs/branch-heads/4664@{#1302}
Cr-Branched-From: 24dc4ee75e01a29d390d43c9c264372a169273a7-refs/heads/main@{#929512}

[modify] https://crrev.com/2209dbe47389fb257374a7a6ce1b18722daeaf79/chrome/browser/devtools/protocol/devtools_protocol_browsertest.cc
[modify] https://crrev.com/2209dbe47389fb257374a7a6ce1b18722daeaf79/content/browser/renderer_host/input/synthetic_gesture_target_aura.cc
[modify] https://crrev.com/2209dbe47389fb257374a7a6ce1b18722daeaf79/content/browser/devtools/protocol/input_handler.cc


### am...@chromium.org (2022-01-04)

[Empty comment from Monorail migration]

### am...@google.com (2022-01-04)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-27)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-07-29)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1117173?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Platform>DevTools, Platform>Extensions]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40053103)*
