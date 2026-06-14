# UI Spoofing in External Protocol confirmation

| Field | Value |
|-------|-------|
| **Issue ID** | [40088664](https://issues.chromium.org/issues/40088664) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser, UI>Browser>Navigation |
| **Platforms** | Linux, Mac, Windows |
| **Reporter** | zy...@gmail.com |
| **Assignee** | es...@chromium.org |
| **Created** | 2017-08-10 |
| **Bounty** | $1,000.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36

Steps to reproduce the problem:
1. open sop2.html,then click the link
2. you will find out that a pop window which asks to run 迅雷.app will show on the "apple.com"

Note:If your computer doesn't be installed 迅雷.app（a torrent downloader),you can try another link scheme "itmss://" for itunes

What is the expected behavior?
the pop window would be hidden when loading to apple.com

What went wrong?
the pop window will show on any website

Did this work before? N/A 

Chrome version: 62.0.3181.0  Channel: canary
OS Version: OS X 10.12.6
Flash Version:

## Attachments

- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- [old.png](attachments/old.png) (image/png, 134.3 KB)
- [new.png](attachments/new.png) (image/png, 136.5 KB)
- [spoof_external_protocols.html](attachments/spoof_external_protocols.html) (text/html, 240 B)

## Timeline

### zy...@gmail.com (2017-08-10)

here is the video for M62 canary:


### zy...@gmail.com (2017-08-10)

hide

### el...@chromium.org (2017-08-10)

This isn't a Same-origin-policy bypass, but it is a UI spoof. The prompt should either be suppressed until the launching tab is activated, or the launching tab should be made active when the prompt is shown).

As noted in https://crbug.com/chromium/713935, this prompt conveys very little information to allow the user to make a valid trust decision, so ensuring that it only appears in front of the invoking tab is somewhat important.

//src/chrome/browser/external_protocol/

[Monorail components: UI>Browser]

### ke...@chromium.org (2017-08-10)

meacer@: I am assigning to you mostly just because you are one of two owners of the external_protocol/ code. Do you know anyone better to take it?

Also cc'ing some people who might be interested in this bug.

### zy...@gmail.com (2017-08-11)

OK,thank you for updating summary

### sh...@chromium.org (2017-08-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-08-11)

[Empty comment from Monorail migration]

### el...@chromium.org (2017-08-15)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-08-25)

meacer: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2017-09-08)

meacer: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### me...@chromium.org (2017-09-14)

This doesn't seem easy to fix without knowing the initiator of a navigation.

The PoC is navigating a named window (which happens to have loaded apple.com) to an external protocol. We can't simply check the WebContents of the external protocol request, because it's the same WebContents as the apple.com tab. We need to be able to know window.opener on the browser side, which I believe isn't available (https://crbug.com/chromium/651895).

dcheng: Can you please confirm this?

### av...@chromium.org (2017-09-15)

Re https://crbug.com/chromium/754304#c3, why "suppress ... until"? An obvious easy answer that occurs to me is to just silently drop the external protocol dialog if the tab doing it isn't visible.

Is that an option?

### av...@chromium.org (2017-09-15)

Oh. Never mind my comment.

### me...@chromium.org (2017-09-15)

:) Right, that's the idea, but it's not currently possible.

External protocol handler dialog is like the HTTP auth dialog: It triggers a modal dialog before the navigation commits. HTTP auth dialogs display a blank interstitial when the request is cross origin. I'm wondering if we need to do something similar here, but then we'd show a blank interstitial for all external protocol dialogs which is not good.

### sh...@chromium.org (2017-10-18)

[Empty comment from Monorail migration]

### me...@chromium.org (2017-11-08)

dcheng: Ping for question #11 :)

### zy...@gmail.com (2017-12-04)

[Comment Deleted]

### sh...@chromium.org (2017-12-07)

[Empty comment from Monorail migration]

### zy...@gmail.com (2018-01-25)

Hi,anyone can help me to track this issue?
Thanks.

### sh...@chromium.org (2018-01-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-03-07)

[Empty comment from Monorail migration]

### zy...@gmail.com (2018-03-13)

So when will this issue be fixed?It has been half a year now.

### zy...@gmail.com (2018-04-16)

hello,anyone here?

### sh...@chromium.org (2018-04-19)

[Empty comment from Monorail migration]

### zy...@gmail.com (2018-05-14)

Hi,excuse me.
Can this issue be fixed at M67?

### sh...@chromium.org (2018-05-30)

[Empty comment from Monorail migration]

### ke...@chromium.org (2018-07-03)

[Empty comment from Monorail migration]

### ke...@chromium.org (2018-07-03)

meacer, avi: Ping. Has anybody given any more thought to this issue? This is approaching a year old.

### sh...@chromium.org (2018-07-25)

[Empty comment from Monorail migration]

### me...@chromium.org (2018-08-07)

I believe https://crbug.com/chromium/754304#c3 still applies here. 

> I'm wondering if we need to do something similar here, but then we'd show a blank interstitial for all external protocol dialogs which is not good.

This is the only approach I can think of, but I wonder if there is a navigation aspect to this as well. For example, can we always open external protocol dialogs in a new tab, and close the tab once the user accepts/cancels it? 

[Monorail components: UI>Browser>Navigation]

### sh...@chromium.org (2018-09-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-10-17)

[Empty comment from Monorail migration]

### zy...@gmail.com (2018-10-30)

Hi,chromium has been updated to 70,could you please process this report before next stable version update?

### me...@chromium.org (2018-11-06)

Does anyone from the navigations team think we shouldn't open all external protocol dialogs in a new tab? That sounds like a feasible solution to me: That way we won't overlay a modal dialog on top of the current page.

### me...@chromium.org (2018-12-03)

+creis, nasko for https://crbug.com/chromium/754304#c34.

### cr...@chromium.org (2018-12-03)

To clarify, are you thinking about letting the navigation proceed as normal up until the point we recognize it as an external protocol request (e.g., including the window.open call switching to the Apple tab in the example), and then manually creating a new about:blank tab as part of showing the dialog?  Then closing the about:blank tab and presumably ending up back at the Apple tab after the dialog goes away, before anyone can interact with the about:blank tab itself?

I don't see a reason that would cause problems, and it would seem to address the security UX issue here where the user incorrectly thinks the page under the dialog created the dialog.

It's not a great UX in general, though-- it's kind of ugly and heavyweight to create a new tab just to throw it away, and the about:blank URL in the address bar won't be very clear to the user.  (I don't think we want to show the requesting page's URL over that about:blank page, since it's not actually running in that tab.)  *Maybe* it would be safe to show the pending external protocol URL in the omnibox of that tab, if we can make sure no other tabs can script it.

This is indeed pretty close to the HTTP auth interstitial case, with the difference that we aren't going to leave when dismissing the dialog.  That means the plans for committed interstitials would prove disruptive here (i.e., the Apple page would incorrectly go away after the dialog).

Maybe the right thing for now is to proceed with your new tab approach to fix the security issue, and then talk with UX folks to design something better than modal dialogs for both HTTP Auth and external protocols in the long run.  In both cases, the request may not be coming from the underlying page, so we don't want it to be associated with that page.

### sh...@chromium.org (2018-12-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-01-30)

[Empty comment from Monorail migration]

### zy...@gmail.com (2019-02-24)

Hello,could you fix this issue before the upcoming release?

### me...@chromium.org (2019-03-12)

creis: Thanks for the detailed comment. I agree the UI isn't great, but I can't think of a simpler solution for the time being. I'll ask UI folks about this.

ericlaw: I think this bug might be relevant to your CL at https://crrev.com/c/1518831



### er...@microsoft.com (2019-03-12)

Interesting, I'd forgotten about this issue. 

The https://crrev.com/c/1518831 change simply closes a new tab that was created for an AppProtocol invocation (the tab must not have ever been navigated previously). When loading the POC, the tab has navigated previously (to Apple.com) and thus my CL has no effect on this scenario.

With regard to the spoof in this bug: Is there any reason we need to support named-target navigation for AppProtocol-schemed URIs at all? For non-builtin schemes, we could either ignore the |target| attribute entirely (which has the benefit of more clearly indicating which tab spawned the prompt), or we could treat any |target| specified as |_blank| (perhaps just updating LocalFrame::CanNavigateWithoutFramebusting or a similar method).  

### sh...@chromium.org (2019-03-13)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-04-24)

[Empty comment from Monorail migration]

### ad...@google.com (2019-05-02)

Chatted with meacer@ about this, and https://crbug.com/chromium/754304#c41. We think the plan is to give it a try.

### sh...@chromium.org (2019-06-06)

[Empty comment from Monorail migration]

### zy...@gmail.com (2019-07-19)

O_o Excuse me, It's been two years since this report was submitted, so I want to know what will be done with this report? 

### sh...@chromium.org (2019-07-31)

[Empty comment from Monorail migration]

### me...@chromium.org (2019-08-01)

zyzengstorm@: Sorry for the delay!

I have a draft CL that implements Eric's suggestion in https://crbug.com/chromium/754304#c41: https://chromium-review.googlesource.com/c/chromium/src/+/1730766

The CL ignores existing frames with the name passed to window.open if the protocol is an external protocol. It ends up opening the navigation in a new tab.

It's a renderer-side only fix. Renderers don't have a way of knowing whether a protocol should be treated as an external protocol so I had to improvise with IsExternalProtocol. 

I'd appreciate thoughts on this approach before I commit to it.

### me...@chromium.org (2019-08-14)

Ping for navigation folks re: the patch in #48

### es...@chromium.org (2019-09-10)

I'm grabbing this bug as part of our security UI fix-it.

I need to prototype this, but it appears we now have an initiator_origin attached to renderer-initiated navigations, which maybe wasn't around back in 2017. My preferred stopgap solution is to display the initiator origin in the dialog, with perhaps a second step of opening a new tab for dialogs where the initiating origin doesn't match the window on top of which we're showing the dialog.

Since neither of these stopgap steps is a great solution, I may separately add metrics for named-target navigations to external protocols and/or investigate how to implement that robustly. dcheng wisely pointed out that it's not clear how to implement that solution for navigations like this:
var w = window.open(...);
w.location="externalprotocol://";

### es...@chromium.org (2019-09-10)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-09-11)

[Empty comment from Monorail migration]

### es...@chromium.org (2019-09-12)

I've sent a question to UI review to see if they're okay adding an origin to the dialog (for renderer-initiated navs).

### er...@microsoft.com (2019-09-12)

Re #53: That UI change seems super-subtle; do you think it's enough to meaningfully mitigate this threat?

### es...@chromium.org (2019-09-13)

Re #54: nope, but as I mentioned in #50 it's a stopgap that we can get into M79. I think the second step is evaluating whether we can open a new tab for all external protocol dialogs or disregard targets for external protocol navigations. We likely need metrics for either of these second steps because they are (arguably) web-facing changes. Also not clear how to disregard a target when the target is a window you have a reference to -- see #50.

### es...@chromium.org (2019-09-13)

An additional measure we could take with M79 is a warning string that says something like "Only do this if you trust this site."

### jd...@chromium.org (2019-09-13)

[Empty comment from Monorail migration]

### er...@microsoft.com (2019-09-16)

> Also not clear how to disregard a target when the target is a window you have a reference to -- see #50.

Isn't there precedence for ignoring the target? E.g. if a context tries to navigate a sub-frame browsing context under a cross origin top-level document, that navigation ends up ignoring the target and opening in a new browser context. We would just declare that attempting to navigate another context to an external protocol means that the context is inherently not "familiar with" the target? https://html.spec.whatwg.org/multipage/browsers.html#the-rules-for-choosing-a-browsing-context-given-a-browsing-context-name

Re #56: I know y'all aren't keen on warning text like this, but I do think[1] that giving the user some context that they're being asked to make a security decision is useful, as we used to do at the bottom of the prompt[2] and as Chrome once did [3].

[1] https://textslashplain.com/2019/08/29/web-to-app-communication-app-protocols/
[2] https://textplain.files.wordpress.com/2019/08/iepermission.png
[3] https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/47/13/metablogapi/8802.image_5A36AE9B.png




### es...@chromium.org (2019-09-19)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-10-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/13b66bdf6719bcfedf549ff8ce2b18d2279e0396

commit 13b66bdf6719bcfedf549ff8ce2b18d2279e0396
Author: Emily Stark <estark@google.com>
Date: Fri Oct 04 17:11:45 2019

Add origin to external protocol dialog

This is a stopgap fix for the fact that it's unclear which frame
triggered a navigation to an external protocol. Eventually, we want to
implement some more robust fixes, like preventing a frame from
navigating another cross-origin frame to an external protocol, but
that'll involve a bit more investigation and metrics (to be added in a
follow-up CL).

Bug: 754304
Change-Id: Ie7e8722281e364397072ade566abfc3739338b49
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1829932
Reviewed-by: Ryan Sturm <ryansturm@chromium.org>
Reviewed-by: Bo <boliu@chromium.org>
Reviewed-by: James Cook <jamescook@chromium.org>
Reviewed-by: Istiaque Ahmed <lazyboy@chromium.org>
Reviewed-by: Alex Moshchuk <alexmos@chromium.org>
Reviewed-by: Elly Fong-Jones <ellyjones@chromium.org>
Reviewed-by: Mustafa Emre Acer <meacer@chromium.org>
Commit-Queue: Emily Stark <estark@chromium.org>
Cr-Commit-Position: refs/heads/master@{#702913}

[modify] https://crrev.com/13b66bdf6719bcfedf549ff8ce2b18d2279e0396/android_webview/browser/aw_content_browser_client.cc
[modify] https://crrev.com/13b66bdf6719bcfedf549ff8ce2b18d2279e0396/android_webview/browser/aw_content_browser_client.h
[modify] https://crrev.com/13b66bdf6719bcfedf549ff8ce2b18d2279e0396/chrome/app/generated_resources.grd
[add] https://crrev.com/13b66bdf6719bcfedf549ff8ce2b18d2279e0396/chrome/app/generated_resources_grd/IDS_EXTERNAL_PROTOCOL_MESSAGE.png.sha1
[add] https://crrev.com/13b66bdf6719bcfedf549ff8ce2b18d2279e0396/chrome/app/generated_resources_grd/IDS_EXTERNAL_PROTOCOL_MESSAGE_WITH_INITIATING_ORIGIN.png.sha1
[modify] https://crrev.com/13b66bdf6719bcfedf549ff8ce2b18d2279e0396/chrome/browser/chrome_content_browser_client.cc
[modify] https://crrev.com/13b66bdf6719bcfedf549ff8ce2b18d2279e0396/chrome/browser/chrome_content_browser_client.h
[modify] https://crrev.com/13b66bdf6719bcfedf549ff8ce2b18d2279e0396/chrome/browser/chromeos/external_protocol_dialog.cc
[modify] https://crrev.com/13b66bdf6719bcfedf549ff8ce2b18d2279e0396/chrome/browser/external_protocol/external_protocol_handler.cc
[modify] https://crrev.com/13b66bdf6719bcfedf549ff8ce2b18d2279e0396/chrome/browser/external_protocol/external_protocol_handler.h
[modify] https://crrev.com/13b66bdf6719bcfedf549ff8ce2b18d2279e0396/chrome/browser/external_protocol/external_protocol_handler_unittest.cc
[modify] https://crrev.com/13b66bdf6719bcfedf549ff8ce2b18d2279e0396/chrome/browser/prerender/prerender_test_utils.cc
[modify] https://crrev.com/13b66bdf6719bcfedf549ff8ce2b18d2279e0396/chrome/browser/site_isolation/chrome_site_per_process_browsertest.cc
[modify] https://crrev.com/13b66bdf6719bcfedf549ff8ce2b18d2279e0396/chrome/browser/ui/android/external_protocol_dialog_android.cc
[modify] https://crrev.com/13b66bdf6719bcfedf549ff8ce2b18d2279e0396/chrome/browser/ui/external_protocol_dialog_delegate.cc
[modify] https://crrev.com/13b66bdf6719bcfedf549ff8ce2b18d2279e0396/chrome/browser/ui/external_protocol_dialog_delegate.h
[modify] https://crrev.com/13b66bdf6719bcfedf549ff8ce2b18d2279e0396/chrome/browser/ui/views/external_protocol_dialog.cc
[modify] https://crrev.com/13b66bdf6719bcfedf549ff8ce2b18d2279e0396/chrome/browser/ui/views/external_protocol_dialog.h
[modify] https://crrev.com/13b66bdf6719bcfedf549ff8ce2b18d2279e0396/chrome/browser/ui/views/external_protocol_dialog_browsertest.cc
[modify] https://crrev.com/13b66bdf6719bcfedf549ff8ce2b18d2279e0396/content/browser/loader/navigation_url_loader_impl.cc
[modify] https://crrev.com/13b66bdf6719bcfedf549ff8ce2b18d2279e0396/content/public/browser/content_browser_client.cc
[modify] https://crrev.com/13b66bdf6719bcfedf549ff8ce2b18d2279e0396/content/public/browser/content_browser_client.h
[modify] https://crrev.com/13b66bdf6719bcfedf549ff8ce2b18d2279e0396/extensions/shell/browser/shell_content_browser_client.cc
[modify] https://crrev.com/13b66bdf6719bcfedf549ff8ce2b18d2279e0396/extensions/shell/browser/shell_content_browser_client.h


### es...@chromium.org (2019-10-04)

I'm going to close this issue now that the origin is shown in the dialog, and have filed https://crbug.com/chromium/1011429 for follow-up investigation and metrics on deprecating cross-origin initiated navigations to external protocols, along with other dangerous scenarios.

### es...@chromium.org (2019-10-04)

Also see https://crbug.com/chromium/1011431

### kn...@chromium.org (2019-10-04)

Is there a separate issue for ChromeOS external protocol dialogs?

### es...@chromium.org (2019-10-04)

Is there a ChromeOS equivalent dialog? All I could find was https://cs.chromium.org/chromium/src/chrome/browser/chromeos/external_protocol_dialog.cc?sq=package:chromium&g=0&targetos=chromeos which looks like a stub. +dominickn probably knows...

### kn...@chromium.org (2019-10-04)

Yeah, it's handled by the IntentPickerBubbleView[1] which gets shown here [2] for external protocols.

[1]: https://cs.chromium.org/chromium/src/chrome/browser/ui/views/intent_picker_bubble_view.cc
[2]: https://cs.chromium.org/chromium/src/chrome/browser/chromeos/arc/intent_helper/arc_external_protocol_dialog.cc?l=128&rcl=64cd7d12a39771f4c47c19f288a1add9d2a95985

### es...@chromium.org (2019-10-04)

Ahh, I missed that, thank you! Re-opening to implement there.

### kn...@chromium.org (2019-10-11)

[Empty comment from Monorail migration]

### ms...@chromium.org (2019-10-17)

[Empty comment from Monorail migration]

### es...@chromium.org (2019-10-21)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-10-23)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-10-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/5d2fdfbad03ae99daf38e211d79b840e000f9de5

commit 5d2fdfbad03ae99daf38e211d79b840e000f9de5
Author: Richard Knoll <knollr@chromium.org>
Date: Thu Oct 24 10:01:23 2019

Show origin in external protocol dialogs.

This will show the origin of the site requesting the external protocol
dialog below the list of apps and devices.
See screenshot: https://imgur.com/phoAsfI

Test: New automated tests added for views w/ and w/o origin.
unit_tests --gtest_filter=IntentPickerBubbleViewTest.InitiatingOriginView

Bug: 1010920,754304

TBR=satorux@chromium.org

Change-Id: I6637b43b7c8e847663d15d233f958430a51f4b4e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1850151
Commit-Queue: Richard Knoll <knollr@chromium.org>
Reviewed-by: Michael Wasserman <msw@chromium.org>
Reviewed-by: David Jacobo <djacobo@chromium.org>
Cr-Commit-Position: refs/heads/master@{#708966}

[modify] https://crrev.com/5d2fdfbad03ae99daf38e211d79b840e000f9de5/chrome/app/generated_resources.grd
[add] https://crrev.com/5d2fdfbad03ae99daf38e211d79b840e000f9de5/chrome/app/generated_resources_grd/IDS_INTENT_PICKER_BUBBLE_VIEW_INITIATING_ORIGIN.png.sha1
[modify] https://crrev.com/5d2fdfbad03ae99daf38e211d79b840e000f9de5/chrome/browser/apps/intent_helper/apps_navigation_throttle.cc
[modify] https://crrev.com/5d2fdfbad03ae99daf38e211d79b840e000f9de5/chrome/browser/chromeos/arc/intent_helper/arc_external_protocol_dialog.cc
[modify] https://crrev.com/5d2fdfbad03ae99daf38e211d79b840e000f9de5/chrome/browser/chromeos/arc/intent_helper/arc_external_protocol_dialog.h
[modify] https://crrev.com/5d2fdfbad03ae99daf38e211d79b840e000f9de5/chrome/browser/chromeos/external_protocol_dialog.cc
[modify] https://crrev.com/5d2fdfbad03ae99daf38e211d79b840e000f9de5/chrome/browser/ui/browser_window.h
[modify] https://crrev.com/5d2fdfbad03ae99daf38e211d79b840e000f9de5/chrome/browser/ui/views/frame/browser_view.cc
[modify] https://crrev.com/5d2fdfbad03ae99daf38e211d79b840e000f9de5/chrome/browser/ui/views/frame/browser_view.h
[modify] https://crrev.com/5d2fdfbad03ae99daf38e211d79b840e000f9de5/chrome/browser/ui/views/intent_picker_bubble_view.cc
[modify] https://crrev.com/5d2fdfbad03ae99daf38e211d79b840e000f9de5/chrome/browser/ui/views/intent_picker_bubble_view.h
[modify] https://crrev.com/5d2fdfbad03ae99daf38e211d79b840e000f9de5/chrome/browser/ui/views/intent_picker_bubble_view_unittest.cc
[modify] https://crrev.com/5d2fdfbad03ae99daf38e211d79b840e000f9de5/chrome/browser/ui/views/toolbar/toolbar_view.cc
[modify] https://crrev.com/5d2fdfbad03ae99daf38e211d79b840e000f9de5/chrome/browser/ui/views/toolbar/toolbar_view.h
[modify] https://crrev.com/5d2fdfbad03ae99daf38e211d79b840e000f9de5/chrome/test/base/test_browser_window.h


### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-10-31)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/9ed87b16907d4d00642d0957fdd017e1e483ffe4

commit 9ed87b16907d4d00642d0957fdd017e1e483ffe4
Author: Richard Knoll <knollr@chromium.org>
Date: Thu Oct 31 19:09:33 2019

Show origin in external protocol dialogs.

This will show the origin of the site requesting the external protocol
dialog below the list of apps and devices.
See screenshot: https://imgur.com/phoAsfI

Test: New automated tests added for views w/ and w/o origin.
unit_tests --gtest_filter=IntentPickerBubbleViewTest.InitiatingOriginView

(cherry picked from commit 5d2fdfbad03ae99daf38e211d79b840e000f9de5)

Bug: 1010920,754304
Change-Id: I6637b43b7c8e847663d15d233f958430a51f4b4e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1850151
Commit-Queue: Richard Knoll <knollr@chromium.org>
Reviewed-by: Michael Wasserman <msw@chromium.org>
Reviewed-by: David Jacobo <djacobo@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#708966}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1893938
Reviewed-by: Richard Knoll <knollr@chromium.org>
Cr-Commit-Position: refs/branch-heads/3945@{#378}
Cr-Branched-From: e4635fff7defbae0f9c29e798349f6fc0cce4b1b-refs/heads/master@{#706915}

[modify] https://crrev.com/9ed87b16907d4d00642d0957fdd017e1e483ffe4/chrome/app/generated_resources.grd
[add] https://crrev.com/9ed87b16907d4d00642d0957fdd017e1e483ffe4/chrome/app/generated_resources_grd/IDS_INTENT_PICKER_BUBBLE_VIEW_INITIATING_ORIGIN.png.sha1
[modify] https://crrev.com/9ed87b16907d4d00642d0957fdd017e1e483ffe4/chrome/browser/apps/intent_helper/apps_navigation_throttle.cc
[modify] https://crrev.com/9ed87b16907d4d00642d0957fdd017e1e483ffe4/chrome/browser/chromeos/arc/intent_helper/arc_external_protocol_dialog.cc
[modify] https://crrev.com/9ed87b16907d4d00642d0957fdd017e1e483ffe4/chrome/browser/chromeos/arc/intent_helper/arc_external_protocol_dialog.h
[modify] https://crrev.com/9ed87b16907d4d00642d0957fdd017e1e483ffe4/chrome/browser/chromeos/external_protocol_dialog.cc
[modify] https://crrev.com/9ed87b16907d4d00642d0957fdd017e1e483ffe4/chrome/browser/ui/browser_window.h
[modify] https://crrev.com/9ed87b16907d4d00642d0957fdd017e1e483ffe4/chrome/browser/ui/views/frame/browser_view.cc
[modify] https://crrev.com/9ed87b16907d4d00642d0957fdd017e1e483ffe4/chrome/browser/ui/views/frame/browser_view.h
[modify] https://crrev.com/9ed87b16907d4d00642d0957fdd017e1e483ffe4/chrome/browser/ui/views/intent_picker_bubble_view.cc
[modify] https://crrev.com/9ed87b16907d4d00642d0957fdd017e1e483ffe4/chrome/browser/ui/views/intent_picker_bubble_view.h
[modify] https://crrev.com/9ed87b16907d4d00642d0957fdd017e1e483ffe4/chrome/browser/ui/views/intent_picker_bubble_view_unittest.cc
[modify] https://crrev.com/9ed87b16907d4d00642d0957fdd017e1e483ffe4/chrome/browser/ui/views/toolbar/toolbar_view.cc
[modify] https://crrev.com/9ed87b16907d4d00642d0957fdd017e1e483ffe4/chrome/browser/ui/views/toolbar/toolbar_view.h
[modify] https://crrev.com/9ed87b16907d4d00642d0957fdd017e1e483ffe4/chrome/test/base/test_browser_window.h


### kn...@chromium.org (2019-11-01)

We're now showing the origin on CrOS as well, closing this now.

### sh...@chromium.org (2019-11-01)

[Empty comment from Monorail migration]

### na...@google.com (2019-11-04)

[Empty comment from Monorail migration]

### na...@google.com (2019-11-07)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2019-11-07)

Congrats! The Panel decided to reward $1,000 for this report. 

### na...@google.com (2019-11-07)

[Empty comment from Monorail migration]

### zy...@gmail.com (2019-11-07)

Wow! Thanks for the bounty.

### ad...@google.com (2019-12-05)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-12-06)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-12-10)

[Empty comment from Monorail migration]

### [Deleted User] (2020-02-15)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### oc...@google.com (2020-05-06)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-04)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-05)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/754304?no_tracker_redirect=1

[Multiple monorail components: UI>Browser, UI>Browser>Navigation]
[Monorail mergedwith: crbug.com/chromium/1078389, crbug.com/chromium/755455, crbug.com/chromium/859840]
[Monorail components added to Component Tags custom field.]

### zy...@gmail.com (2024-04-11)

Due to the loss of attachments during the migration process of the issue tracker, so re-upload it.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40088664)*
