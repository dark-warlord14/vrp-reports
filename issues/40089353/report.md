# Security: Fullscreen notification can be overlapped

| Field | Value |
|-------|-------|
| **Issue ID** | [40089353](https://issues.chromium.org/issues/40089353) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>FullScreen |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **CVE IDs** | CVE-2017-15386 |
| **Reporter** | ma...@gmail.com |
| **Assignee** | av...@chromium.org |
| **Created** | 2017-10-19 |
| **Bounty** | $1,000.00 |

## Description

AFFECTED PRODUCTS
--------------------
chrome 62 stable


DESCRIPTION
--------------------
attacker could call an alert function in the popup without exit fullscreen mode
and overlay the security notification
bypass the patch of CVE-2017-15386 (https://crbug.com/chromium/752003)
Online demo http://xsser.math1as.com/bypass.html

## Attachments

- [attack.gif](attachments/attack.gif) (image/gif, 170.2 KB)

## Timeline

### ma...@gmail.com (2017-10-19)

as a result: the old patch just exit fullscreen when window.open is called, so it is not a good idea just block window.open

### el...@chromium.org (2017-10-19)

This POC results in a blocked popup notification and then a few misplaced windows. Can you please explain in prose what you're trying to accomplish and include screenshots demonstrating the effect?

I /think/ you're simply noting that a window.open()-spawned window can be placed above the notification that a window has gone full-screen? Is that right?

[Monorail components: UI>Browser>FullScreen]

### ma...@gmail.com (2017-10-19)

yes,a popup window would overlay the notification
the result behaves the same with https://crbug.com/chromium/776418#c9 in https://crbug.com/chromium/752003
(attacker draws a fake addressbar on the top of this page, but user would not know because of the notification is overlapped)

### ke...@chromium.org (2017-10-19)

elawrence, avi: Random question... both window.open() and the fullscreen API require user gestures. Apparently not separate ones, though. Does one of them not consume the gesture?

### av...@chromium.org (2017-10-19)

I don't believe fullscreen requires a gesture, but I'm not sure. You'd have to ask a gesture person.

Meanwhile, window.open() is supposed to kick the caller out of fullscreen. I fixed that a few months ago. Is that broken? (Looking at the repro now.)

### av...@chromium.org (2017-10-19)

Is what's going on that while new popups kick the caller out of fullscreen, you can reposition old ones, and activate them with alert dialogs?


### ma...@gmail.com (2017-10-19)

yes,now window.open() would kick the caller fullscreen mode
but this poc shows a way to bypass your rule
3 steps:
1. window(A) open window(B) (about:blank)
2. window(A) open window(C) (page with a fake addressbar)
3. window(C) request fullscreen mode , then i call alert function on window(B)
so that window(B) overlay the notification on window(C)


### ma...@gmail.com (2017-10-19)

Re #6
the window.open is called before request fullscreen API
so that window(C) would not be kicked out of fullscreen

### av...@chromium.org (2017-10-19)

This is mitigated by running against the popup blocker, then. I needed to disable it to see what you're doing.

### ma...@gmail.com (2017-10-20)

Re #2
Re #9

now I write a POC which would show this attack (similar with https://crbug.com/chromium/752003)
and do not need to disable anything

Online Demo http://xsser.math1as.com/fullscreen.html


### ma...@gmail.com (2017-10-20)

and here comes the attack.gif
shows a same attack result with the old bug
so this is how i bypass the patch

### ts...@chromium.org (2017-10-20)

[Empty comment from Monorail migration]

### av...@chromium.org (2017-10-20)

First, this isn't a critical issue because this requires the popup blocker to be disabled.

Second, I'm not sure what to do here. Can we make the fullscreen bubble always be on top of browser windows?

I'm removing activation from everything I can, which will fix this, though that's currently an ongoing project.

### ma...@gmail.com (2017-10-20)

Re #13
follow my new POC , if user give a gesture(click the link) instead of using window.open , it would not need the popup blocker to be disabled

### ma...@gmail.com (2017-10-20)

Re #13
your second problem is easy to be answered
in the old bug,the patch kick the opener out of fullscreen
in this bug,if any function like alert,prompt is called , you could kick the window's opener out of fullscreen mode

### ma...@gmail.com (2017-10-20)

old patch: Window A open Window B, B kick out its opener
new patch: Window A open Window B,Window B call alert,prompt,focus function, B kick out its opener

### av...@google.com (2017-10-20)

The problem is that the window that is calling alert/prompt isn't the window that's in fullscreen.

Right now the removal of activation is my solution here.

### sh...@chromium.org (2017-10-22)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-11-04)

avi: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2017-11-18)

avi: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pa...@chromium.org (2017-12-04)

+Security UX peeps

Any chance this can be fixed in M-64? M-63 has passed.

### av...@chromium.org (2017-12-04)

Oh! I misunderstood what was going on, and thought that I needed to remove activation from dialogs.

Here's what happens:
1. The page has a link for a click. The user clicks, which shows a popup.
2. The page then refreshes to content that socially engineers another click from the user. The page uses that click to go fullscreen to a fake site. Meanwhile, the page calls focus() on the popup, which brings it to the front.

I thought the page was using dialogs to activate, rather than using window.focus(). If we look at the DOMWindow::focus() implementation, window.focus() is restricted to the case where the parent window is forcing a popup to be focused.

I'm not sure what to do here. We can drop our support for window.focus() entirely, but that kills the case where a page, say, uses a popup to implement a calendar control (the user focuses the main page again, and then the main page tries to hold the popup window above itself).

Is that a direction we want to pursue?

### ra...@chromium.org (2017-12-05)

tapted: is it possible to make this notification show up on top of all the windows? 

In general, if other windows show up above the fullscreen window, should we just exit fullscreen? 

### ta...@chromium.org (2017-12-05)

did you ask me that already at http://crbug.com/550017#c24 ?

### ra...@chromium.org (2017-12-05)

Sorry if I did! I just chatted again with mgiuca and it's not easy to control the stack order. What we want to do is exit fullscreen whenever a popup is triggered during fullscreen (i.e. there should never be anything on top of fullscreen).

### ta...@chromium.org (2017-12-05)

hehe - sorry for the cheeky response :). I've caught up on the issue here. It's a lot of the same problems in https://crbug.com/chromium/550017 .

I think on Mac we may be able to do something custom by setting a window level or using NSWindowStyleMaskHUDWindow . Apple's documentation for these really sucks btw :/. Using these may introduce other problems.

For Windows, there didn't seem to be a good alternative. There's `AlwaysOnTop` but that may also need us to break the parent/child relationship, which may break other things.

But these feel like workarounds anyway. Popups shouldn't work in fullscreen.

For example, if I go to http://xsser.math1as.com/fullscreen.html and press Ctrl+Cmd+f to get "AppKit" fullscreen on Mac, the popup shows in a tab. If you're in HTML5 fullscreen rather than AppKit fullscreen, booting a user out of fullscreen seems like the right fix.

### av...@chromium.org (2017-12-05)

Please read https://crbug.com/chromium/776418#c22.

We *already* drop fullscreen when a popup is displayed. In this case, the popup is *already there* when we go fullscreen. The main page calls window.activate() on the popup to bring it to the front.

What are you proposing? That _any_ activation of _any_ popup window breaks fullscreen of _all_ fullscreened elements?

### ra...@chromium.org (2017-12-05)

Sorry I did read #22 but I didn't see the connection. I think that focussing another window over the fullscreen window should have the same effect of exiting fullscreen? 

### ta...@chromium.org (2017-12-05)

hm - we need to consider a dual-monitor setup. A user can have a fullscreen YouTube on one monitor, and regular browser windows on the other monitor. If a website makes a popup, it shouldn't boot YouTube out of fullscreen. If a website makes a popup, moves it to the other monitor, and activates it, it probably also shouldn't boot youtube out of fullscreen. But perhaps we can prevent window activation of the popup in this case, or prevent/moveout any popups that would overlap fullscreen windows.

### av...@chromium.org (2018-01-05)

How about if a page calls window.activate(), it gets kicked out of fullscreen?

Activation is inherently a multiwindow action while fullscreen is immersive. They're contradictory.

### av...@chromium.org (2018-01-05)

Reporter: http://xsser.math1as.com/fullscreen.html is not responding. Can you check it? I want to test a fix I'm working on.

### ma...@gmail.com (2018-01-08)

I am sorry, i will fix it as soon as possible

### av...@google.com (2018-01-08)

Proposing a fix in https://crbug.com/chromium/800056.

### av...@google.com (2018-01-08)

ma7: No problem; thank you for maintaining your site and sorry for the delay.

### ma...@gmail.com (2018-01-09)

re #34
already fixed, it works

### av...@chromium.org (2018-01-09)

I just tested https://crrev.com/c/852378 against your POC and it works. I have it under consideration for an Intent on blink-dev.

### av...@chromium.org (2018-01-24)

This appears to affect Firefox as well; filed https://bugzilla.mozilla.org/show_bug.cgi?id=1432856 .

### bu...@chromium.org (2018-02-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/36f801fdbec07d116a6f4f07bb363f10897d6a51

commit 36f801fdbec07d116a6f4f07bb363f10897d6a51
Author: Avi Drissman <avi@chromium.org>
Date: Thu Feb 01 20:06:04 2018

If a page calls |window.focus()|, kick it out of fullscreen.

BUG=776418, 800056

Change-Id: I1880fe600e4814c073f247c43b1c1ac80c8fc017
Reviewed-on: https://chromium-review.googlesource.com/852378
Reviewed-by: Nasko Oskov <nasko@chromium.org>
Reviewed-by: Philip Jägenstedt <foolip@chromium.org>
Commit-Queue: Avi Drissman <avi@chromium.org>
Cr-Commit-Position: refs/heads/master@{#533790}
[modify] https://crrev.com/36f801fdbec07d116a6f4f07bb363f10897d6a51/content/browser/frame_host/render_frame_host_delegate.h
[modify] https://crrev.com/36f801fdbec07d116a6f4f07bb363f10897d6a51/content/browser/frame_host/render_frame_host_impl.cc
[modify] https://crrev.com/36f801fdbec07d116a6f4f07bb363f10897d6a51/content/browser/frame_host/render_frame_host_impl.h
[modify] https://crrev.com/36f801fdbec07d116a6f4f07bb363f10897d6a51/content/browser/web_contents/web_contents_impl.cc
[modify] https://crrev.com/36f801fdbec07d116a6f4f07bb363f10897d6a51/content/browser/web_contents/web_contents_impl.h
[modify] https://crrev.com/36f801fdbec07d116a6f4f07bb363f10897d6a51/content/browser/web_contents/web_contents_impl_browsertest.cc
[modify] https://crrev.com/36f801fdbec07d116a6f4f07bb363f10897d6a51/content/common/frame_messages.h
[modify] https://crrev.com/36f801fdbec07d116a6f4f07bb363f10897d6a51/content/renderer/render_frame_impl.cc
[modify] https://crrev.com/36f801fdbec07d116a6f4f07bb363f10897d6a51/content/renderer/render_frame_impl.h
[modify] https://crrev.com/36f801fdbec07d116a6f4f07bb363f10897d6a51/content/renderer/render_view_impl.cc
[modify] https://crrev.com/36f801fdbec07d116a6f4f07bb363f10897d6a51/content/renderer/render_view_impl.h
[modify] https://crrev.com/36f801fdbec07d116a6f4f07bb363f10897d6a51/content/shell/test_runner/web_view_test_client.cc
[modify] https://crrev.com/36f801fdbec07d116a6f4f07bb363f10897d6a51/content/shell/test_runner/web_view_test_client.h
[modify] https://crrev.com/36f801fdbec07d116a6f4f07bb363f10897d6a51/content/shell/test_runner/web_view_test_proxy.h
[modify] https://crrev.com/36f801fdbec07d116a6f4f07bb363f10897d6a51/third_party/WebKit/Source/core/exported/WebViewTest.cpp
[modify] https://crrev.com/36f801fdbec07d116a6f4f07bb363f10897d6a51/third_party/WebKit/Source/core/frame/DOMWindow.cpp
[modify] https://crrev.com/36f801fdbec07d116a6f4f07bb363f10897d6a51/third_party/WebKit/Source/core/loader/EmptyClients.h
[modify] https://crrev.com/36f801fdbec07d116a6f4f07bb363f10897d6a51/third_party/WebKit/Source/core/loader/FrameLoader.cpp
[modify] https://crrev.com/36f801fdbec07d116a6f4f07bb363f10897d6a51/third_party/WebKit/Source/core/page/ChromeClient.h
[modify] https://crrev.com/36f801fdbec07d116a6f4f07bb363f10897d6a51/third_party/WebKit/Source/core/page/ChromeClientImpl.cpp
[modify] https://crrev.com/36f801fdbec07d116a6f4f07bb363f10897d6a51/third_party/WebKit/Source/core/page/ChromeClientImpl.h
[modify] https://crrev.com/36f801fdbec07d116a6f4f07bb363f10897d6a51/third_party/WebKit/Source/core/page/CreateWindow.cpp
[modify] https://crrev.com/36f801fdbec07d116a6f4f07bb363f10897d6a51/third_party/WebKit/public/web/WebViewClient.h


### av...@chromium.org (2018-02-15)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-02-16)

[Empty comment from Monorail migration]

### aw...@google.com (2018-02-19)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-02-26)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-02-26)

Congratulations ma7h1as.l@! The VRP Panel has decided to award $1,000 for this report. Cheers!

### aw...@chromium.org (2018-02-27)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-03-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-03-16)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-03-16)

This bug requires manual review: M66 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), josafat@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ab...@google.com (2018-03-19)

No need for merge. 

### aw...@google.com (2018-04-17)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-05-25)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2019-01-04)

[Empty comment from Monorail migration]

### is...@google.com (2019-01-04)

This issue was migrated from crbug.com/chromium/776418?no_tracker_redirect=1

[Monorail blocking: crbug.com/chromium/800056]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40089353)*
