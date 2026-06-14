# Untrustworthy navigation causes HTTP Basic Auth dialog origin confusion/spoofing

| Field | Value |
|-------|-------|
| **Issue ID** | [40051828](https://issues.chromium.org/issues/40051828) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser |
| **Platforms** | iOS |
| **Reporter** | ra...@gmail.com |
| **Assignee** | kk...@chromium.org |
| **Created** | 2020-03-22 |
| **Bounty** | $500.00 |

## Description

It's a regression bug of the https://crbug.com/chromium/149871 in the iOS.

Demo: http://lcamtuf.coredump.cx/authspoof/ 

## Attachments

- [Bug.mp4](attachments/Bug.mp4) (video/mp4, 154.3 KB)

## Timeline

### ra...@gmail.com (2020-03-23)

[Comment Deleted]

### es...@chromium.org (2020-03-24)

I don't know if this is a regression or not, but if it is, maybe related to https://chromium-review.googlesource.com/c/chromium/src/+/1680279? khorimoto, could you take a look please, and re-assign if appropriate?

### kh...@chromium.org (2020-03-24)

[Empty comment from Monorail migration]

### kk...@chromium.org (2020-03-24)

Sending to Pete for UX.  In past conversations, we'd decided that replacing the URL in the omnibox with the "Sign in to website" text and showing the requesting page's URL in the sign in dialog were sufficient.  That being said, for less technically literate users, having a page's rendered content visible behind the dialog seems like phishing attack vector.  We can fix this by blocking the content area when HTTP auth dialogs are displayed for a site whose hostname does not match the last committed URL.  Does this seem reasonable?

### [Deleted User] (2020-03-24)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ps...@chromium.org (2020-03-25)

> We can fix this by blocking the content area when HTTP auth dialogs are displayed for a site whose hostname does not match the last committed URL.  Does this seem reasonable?

Yes, that sounds great! When we block out the content area, I imagine white, but I started wondering: is there a different default webview background color while in dark mode? If yes, we should make sure our block out responds to the effective appearance.

### bd...@chromium.org (2020-04-06)

(Currently marshal) I assigned the component to this. Please update if it's not correct. 

[Monorail components: Mobile>iOSWebView]

### kk...@chromium.org (2020-04-06)

crrev.com/c/2136232

[Monorail components: -Mobile>iOSWebView UI>Browser]

### sr...@google.com (2020-04-09)

We are one week past M83 branch point and in light of COVID-19 and extra scrutiny of M83 release, we are currently accepting only P0/P1 bugs in this release. Please ensure your bug priority is set properly and if it is not a P0/P1 then please move it to the next milestone. If this is a release blocker for M83, please adjust the priority to P0/P1 as applicable.

### kk...@chromium.org (2020-04-09)

Moving milestone to M-84.  This bug is not a regression; https://crbug.com/chromium/149871 was for non-iOS platforms.  The fix in crrev.com/c/2136232 is the first time this will be fixed on iOS.  Given that the location bar does not show the rendered page's URL and the HTTP authentication dialog shows the requesting page's URL, this doesn't need to be release-blocking for M-83.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-04-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/0068e74c4235b549731b61e889ee502602c168fb

commit 0068e74c4235b549731b61e889ee502602c168fb
Author: Kurt Horimoto <kkhorimoto@google.com>
Date: Wed Apr 15 19:42:26 2020

[iOS] Block the content area for HTTP auth dialogs from a different host

This CL refactors the browser container to use a mediator and consumer.
The BrowserContainerMediator observes presentation of HTTP
authentication dialogs.  If one is presented from a different host than
the rendered page in the content area, a blocking view is inserted
behind the HTTP auth overlay to block out the page.

In order to support this change, a URL is added to the OverlayRequest
config so that it can be compared with the last committed URL of the
Browser's active WebState.

Bug: 1063690
Change-Id: I21c7abe83818180762e3a2dda6f764ea635ee42a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2136232
Commit-Queue: Kurt Horimoto <kkhorimoto@chromium.org>
Reviewed-by: Mark Cogan <marq@chromium.org>
Cr-Commit-Position: refs/heads/master@{#759367}

[modify] https://crrev.com/0068e74c4235b549731b61e889ee502602c168fb/ios/chrome/browser/overlays/public/web_content_area/http_auth_overlay.h
[modify] https://crrev.com/0068e74c4235b549731b61e889ee502602c168fb/ios/chrome/browser/overlays/public/web_content_area/http_auth_overlay.mm
[modify] https://crrev.com/0068e74c4235b549731b61e889ee502602c168fb/ios/chrome/browser/ui/browser_container/BUILD.gn
[add] https://crrev.com/0068e74c4235b549731b61e889ee502602c168fb/ios/chrome/browser/ui/browser_container/browser_container_consumer.h
[modify] https://crrev.com/0068e74c4235b549731b61e889ee502602c168fb/ios/chrome/browser/ui/browser_container/browser_container_coordinator.mm
[add] https://crrev.com/0068e74c4235b549731b61e889ee502602c168fb/ios/chrome/browser/ui/browser_container/browser_container_mediator.h
[add] https://crrev.com/0068e74c4235b549731b61e889ee502602c168fb/ios/chrome/browser/ui/browser_container/browser_container_mediator.mm
[add] https://crrev.com/0068e74c4235b549731b61e889ee502602c168fb/ios/chrome/browser/ui/browser_container/browser_container_mediator_unittest.mm
[modify] https://crrev.com/0068e74c4235b549731b61e889ee502602c168fb/ios/chrome/browser/ui/browser_container/browser_container_view_controller.h
[modify] https://crrev.com/0068e74c4235b549731b61e889ee502602c168fb/ios/chrome/browser/ui/browser_container/browser_container_view_controller.mm
[modify] https://crrev.com/0068e74c4235b549731b61e889ee502602c168fb/ios/chrome/browser/ui/location_bar/location_bar_mediator_unittest.mm
[modify] https://crrev.com/0068e74c4235b549731b61e889ee502602c168fb/ios/chrome/browser/ui/overlays/web_content_area/http_auth_dialogs/http_auth_dialog_overlay_mediator_unittest.mm
[modify] https://crrev.com/0068e74c4235b549731b61e889ee502602c168fb/ios/chrome/browser/web/web_state_delegate_tab_helper.mm


### kk...@chromium.org (2020-04-15)

[Empty comment from Monorail migration]

### [Deleted User] (2020-04-18)

[Empty comment from Monorail migration]

### na...@google.com (2020-04-20)

[Empty comment from Monorail migration]

### na...@google.com (2020-04-23)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-04-23)

Congrats the Panel decided to award $500 for this report!

### na...@google.com (2020-04-23)

[Empty comment from Monorail migration]

### kk...@chromium.org (2020-04-24)

[Empty comment from Monorail migration]

### ra...@gmail.com (2020-05-13)

[Comment Deleted]

### ra...@gmail.com (2020-06-02)

[Comment Deleted]

### na...@google.com (2020-06-04)

Panel re-assessed as this report to be the same as the original reward value.   

### ad...@google.com (2020-07-13)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-07-13)

[Empty comment from Monorail migration]

### ad...@google.com (2020-07-22)

[Empty comment from Monorail migration]

### [Deleted User] (2020-07-23)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2020-07-23)

This issue was migrated from crbug.com/chromium/1063690?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/1073710]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40051828)*
