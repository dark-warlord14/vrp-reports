# Security: URL spoofing via crafted flash file and UI overlay

| Field | Value |
|-------|-------|
| **Issue ID** | [40088591](https://issues.chromium.org/issues/40088591) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Fullscreen, Internals>Plugins>Flash, UI>Browser>Navigation, UI>Browser>Omnibox |
| **Platforms** | Linux, Windows |
| **Reporter** | ma...@gmail.com |
| **Assignee** | av...@chromium.org |
| **Created** | 2017-08-03 |
| **Bounty** | $1,000.00 |

## Description

URL spoofing via crafted flash file and UI overlay
2017.8.3


AFFECTED PRODUCTS
--------------------
chrome 59.0.3071.115


DESCRIPTION
--------------------
when ActionScript use navigateToURL function to open a new window
the URL updates before actual navigation
i guess it's similar to https://bugs.chromium.org/p/chromium/issues/detail?id=660498 (PDF)

when a new window with no toolbar is opened,it could overlay the fullscreen notification
it looks like https://bugs.chromium.org/p/chromium/issues/detail?id=565760

but when i only use flash to spoofing , as i write something into the spoofing page
the address turned to about:blank
so i combine the following two methods to finish this attack

1.spoofing to account.google.com:81 for 8 seconds (or longer)
make a fake page which tells user that there is a network error.
2.user click the reload button
then I draw fake address bar. open a new window to overlay the fullscreen notification


PoC
--------------------
online example

http://www.math1as.com/spoofing_poc.html

poc.zip for your local httpserver

attack1.gif shows spoofing only use method 1

attack2.gif shows the total attack

SOLUTION
--------------------
follow https://crbug.com/chromium/660498 to fix the flash problem
cancel full-screen mode when open a new window


CREDIT
--------------------
This vulnerability was discovered by mathiaswu of Tencent's Xuanwu Lab.

## Attachments

- [poc.zip](attachments/poc.zip) (application/octet-stream, 48.6 KB)
- [attack1.gif](attachments/attack1.gif) (image/gif, 350.1 KB)
- [attack2.gif](attachments/attack2.gif) (image/gif, 443.0 KB)
- [evil.as](attachments/evil.as) (text/plain, 409 B)
- [attack.webm](attachments/attack.webm) (video/webm, 301.3 KB)
- [Screen Shot 2017-08-08 at 2.39.39 PM.png](attachments/Screen Shot 2017-08-08 at 2.39.39 PM.png) (image/png, 21.6 KB)

## Timeline

### ma...@gmail.com (2017-08-03)

what's more , when a new window is opened during full-screen mode , the taskbar in bottom appears so that user can't realized that he is in full-screen mode

### ma...@gmail.com (2017-08-03)

so,this is the .webm video for the total attack

### ma...@gmail.com (2017-08-07)

I'm sorry to bother, but is there anyone to handle this issue?

### el...@chromium.org (2017-08-07)

I suspect this will indeed be quite similar to https://crbug.com/chromium/660498 in root cause.

[Monorail components: UI>Browser>Navigation]

### ts...@chromium.org (2017-08-08)

[Empty comment from Monorail migration]

[Monorail components: Internals>Plugins>Flash UI>Browser>Omnibox]

### ts...@chromium.org (2017-08-08)

[Empty comment from Monorail migration]

### cr...@chromium.org (2017-08-08)

Sounds like this is a fullscreen bug, if we're letting a popup show up over fullscreen mode and hide the fullscreen notification.  Shouldn't we exit fullscreen mode if a popup is shown?

Note that attack2.gif and the video in https://crbug.com/chromium/752003#c2 are the concerning ones.  attack1.gif shows expected behavior, where we reset the URL bar to about:blank if an opener window tries to modify the page while a slow URL is loading (per https://crbug.com/chromium/9682).

[Monorail components: Blink>Fullscreen]

### av...@chromium.org (2017-08-08)

We drop out of HTML5 fullscreen. I thought that the code that I use to do that would kick me out of Flash fullscreen. Is this using Flash fullscreen?

### cr...@chromium.org (2017-08-08)

The attached poc.zip has a modified version of Chrome's error page encoded in the attack page.  It seems to be using HTML5 fullscreen to launch the attack.  (Flash only appears to be used to open the URL in a new tab, though I'm not sure why that's needed.  It would work with slow links that open in a new tab as well, even without Flash.)

Here's the relevant code snippet:

<button id="reload-button" class="blue-button text-button" onclick="document.body.webkitRequestFullscreen();document.body.innerHTML='<img src=111.jpg width=\'101.5%\' height=\'6%\' style=\'margin-left:-8px;margin-top:-6px\' /><div style=\'background-color:white;width:102.5%;margin-left:-20px;height:96.5%;border-style:none;\'><br><br><h2>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;oh! this is a fake google</h2></div>';t=window.open('','','height=100,width=400,top=0,left=800,toolbar=no,menubar=no,scrollbars=no, resizable=no,location=no, status=no');t.document.write('overlay the fullscreen notification')">Reload</button>

That appears to work in a simpler test page, showing a popup over fullscreen.  Avi, do you want to take a look at that?

### av...@chromium.org (2017-08-08)

Re the video in https://crbug.com/chromium/752003#c2, that's not a JavaScript dialog. It's a popup.

### cr...@chromium.org (2017-08-08)

Right, we're discussing popups, not dialogs.  :)

### av...@chromium.org (2017-08-08)

Just realized that.

The easy answer is, if a page shows a popup, that should kick it out of fullscreen. Is that another Blink Intent?

The other answer would be to debug window ordering in Views, but that's not anything I know about.

### av...@chromium.org (2017-08-08)

In my Intent re dialogs exiting fullscreen, Jochen wrote (https://groups.google.com/a/chromium.org/d/msg/blink-dev/waIh70rrNKM/4h_da0DwBgAJ):

"I changed window.open() exiting fullscreen a long time ago, and I feel like doing the same for dialogs is in line with this."

This _should_ already be kicking pages out of fullscreen. What's going on?

### av...@chromium.org (2017-08-08)

FYI that change from Jochen is https://codereview.chromium.org/27599002 .

### av...@chromium.org (2017-08-08)

This change from Jochen fails on Windows, but works fine on the Mac. The change is deep in Blink, and I don't know why it fails.

### av...@chromium.org (2017-08-08)

Is there someone good with Blink who can investigate why the fullscreen exit isn't working on Windows?

### sh...@chromium.org (2017-08-09)

[Empty comment from Monorail migration]

### dc...@chromium.org (2017-08-10)

I did some debugging. I'm not sure why this doesn't repro on Mac, but it definitely repros on Linux as well. What I'm seeing is that FullyExitFullscreen takes this early return: https://cs.chromium.org/chromium/src/third_party/WebKit/Source/core/fullscreen/Fullscreen.cpp?rcl=4f9d2469ba713829aaa2e62fdd766a64cb5965d3&l=620

I believe this is because going into fullscreen mode is an async IPC, while creating a new window is a sync IPC.

One way to address this is to move the checks into the browser like https://chromium-review.googlesource.com/c/606987 proposes: even though fullscreen is an async IPC, and creating a new window is a sync IPC, this gives us the ordering guarantee that the fullscreen IPC arrives (and is processed before) the create new window IPC.

### av...@chromium.org (2017-08-10)

Here's an interesting twist. If you fully revert https://codereview.chromium.org/27599002 and do nothing more, showing a popup _still_ drops the page out of fullscreen on the Mac. The activation of the popup calls Browser::TabDeactivated, which calls ExclusiveAccessManager::OnTabDeactivated, which does the fullscreen drop.

I'm not clear what's going on on Windows, but I'll look into still doing it in WebContents.

### av...@chromium.org (2017-08-10)

And in fact, even if you don't revert https://codereview.chromium.org/27599002 but instrument fullscreen, it's not the code in Blink that kicks Chrome out of fullscreen, but actually that codepath through Browser::TabDeactivated.

My conclusion is that the code in https://codereview.chromium.org/27599002, while perhaps effective in the past and in the layout tests, has zero effect on modern Chrome for the user when it comes to fullscreen and popups.

My plan is to fully revert it and reimplement it in WebContents.

### av...@chromium.org (2017-08-10)

OTOH, the WPTs "fully-exit-fullscreen*" rely on window.open immediately kicking a page out of fullscreen synchronously from their point of view. Note that they escape the race by waiting for an "onfullscreenchange" handler callback before calling window.open.

Which means that to not break the WPTs we need to keep the existing code in Blink, we need to keep the existing code in Blink and add more in Chromium.

### av...@chromium.org (2017-08-10)

Specifically, these tests were added to test Fullscreen::fullyExitFullscreen() in https://chromium.googlesource.com/chromium/src/+/5dec13adba85193629911ce63d437cad5f2c3b88 and I'm a loath to remove them.

Philip, thoughts?

### fo...@chromium.org (2017-08-11)

This is the tests in https://cs.chromium.org/chromium/src/third_party/WebKit/LayoutTests/fullscreen/model/, right?

These are actually not part of web-platform-tests, because when I wrote them the window.open behavior wasn't mentioned in the spec (still isn't) and I think it also didn't work that way in all implementations. There's a FIXME in fully-exit-fullscreen.js lamenting the situation.

So, it would be fine to change these tests to cover whatever the new behavior is. Or will this be a case where content_shell doesn't work the same as chrome, so that it actually can't be tested with LayoutTests?

### av...@chromium.org (2017-08-11)

I'm not sure how fullscreen works in content shell, only that when I removed the Blink implementation those tests were failing. Because they use onfullscreenchange, they _should_ work with the new implementation, though. I can take a look.

(There would be a new test; see https://chromium-review.googlesource.com/c/606987 to see what I have in mind.)

### fo...@chromium.org (2017-08-11)

That looks OK to me. Having something spec'd and tested in wpt would be even nicer, but that's not happening in a hurry, and also not a high priority I think.

### av...@chromium.org (2017-08-11)

I just confirmed that this fixes the problem on Windows in a local build. Philip, if you're OK with switching to a browser-side fix, I'll rev the CL and send it out for review.

Thank you, all!

### sh...@chromium.org (2017-08-26)

avi: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chromium.org (2017-08-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/ba3b1b344017bbf36283464b51014fad15c2f3f4

commit ba3b1b344017bbf36283464b51014fad15c2f3f4
Author: Avi Drissman <avi@chromium.org>
Date: Tue Aug 29 18:16:13 2017

If a page shows a popup, end fullscreen.

This was implemented in Blink r159834, but it is susceptible
to a popup/fullscreen race. This CL reverts that implementation
and re-implements it in WebContents.

BUG=752003
TEST=WebContentsImplBrowserTest.PopupsFromJavaScriptEndFullscreen

Change-Id: Ia345cdeda273693c3231ad8f486bebfc3d83927f
Reviewed-on: https://chromium-review.googlesource.com/606987
Commit-Queue: Avi Drissman <avi@chromium.org>
Reviewed-by: Charlie Reis <creis@chromium.org>
Reviewed-by: Philip Jägenstedt <foolip@chromium.org>
Cr-Commit-Position: refs/heads/master@{#498171}
[modify] https://crrev.com/ba3b1b344017bbf36283464b51014fad15c2f3f4/content/browser/web_contents/web_contents_impl.cc
[modify] https://crrev.com/ba3b1b344017bbf36283464b51014fad15c2f3f4/content/browser/web_contents/web_contents_impl.h
[modify] https://crrev.com/ba3b1b344017bbf36283464b51014fad15c2f3f4/content/browser/web_contents/web_contents_impl_browsertest.cc
[modify] https://crrev.com/ba3b1b344017bbf36283464b51014fad15c2f3f4/third_party/WebKit/Source/core/page/ChromeClientImpl.cpp


### av...@chromium.org (2017-08-29)

So that's landed. Marking fixed; can the OP confirm on what I imagine will be the 3200 canary?

### sh...@chromium.org (2017-08-30)

[Empty comment from Monorail migration]

### aw...@google.com (2017-09-06)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-09-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2017-09-11)

Many thanks for the report ma7h1as.l@! The VRP Panel decided to award $1,000 for this bug.

### aw...@chromium.org (2017-09-12)

[Empty comment from Monorail migration]

### ma...@gmail.com (2017-09-12)

Thanks , please credit as Wenxu Wu of Tencent's Xuanwu Lab when you are ready to release a new version google.

### sh...@chromium.org (2017-09-15)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-09-15)

This bug requires manual review: M62 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: amineer@(Android), cmasso@(iOS), bhthompson@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2017-09-16)

Already in M62

### aw...@google.com (2017-10-16)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-10-18)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-12-06)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/752003?no_tracker_redirect=1

[Multiple monorail components: Blink>Fullscreen, Internals>Plugins>Flash, UI>Browser>Navigation, UI>Browser>Omnibox]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40088591)*
