# iframe sandbox escape

| Field | Value |
|-------|-------|
| **Issue ID** | [40090810](https://issues.chromium.org/issues/40090810) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Mobile>Intents |
| **Platforms** | iOS |
| **Reporter** | s....@gmail.com |
| **Assignee** | mr...@chromium.org |
| **Created** | 2018-03-16 |
| **Bounty** | $1,000.00 |

## Description

Steps to reproduce the problem:
1. Go to https://attack.shhnjk.com/sptest.html
2. Click the link inside iframe

What is the expected behavior?
Nothing happens.

What went wrong?
googlechrome: scheme can escape iframe sandbox.

Did this work before? N/A 

Chrome version: 65.0.3325.152  Channel: stable
OS Version: iOS 11.2.6
Flash Version: 

PoC
<iframe src="data:text/html,<a href='googlechrome://test.shhnjk.com/alert.html'>CLICK ME</a>" sandbox></iframe>

## Timeline

### do...@chromium.org (2018-03-16)

I observe that the page opens a new window on Chrome for iOS, whereas it doesn't on Android or desktop. +iOS folks, is this something we're about to address, or does it need to go to WebKit?

[Monorail components: Blink>SecurityFeature>IFrameSandbox]

### eu...@chromium.org (2018-03-16)

Danyao, is this something that WebPlatform team can take?

[Monorail components: -Blink>SecurityFeature>IFrameSandbox Mobile>WebView>Glue]

### sh...@chromium.org (2018-03-16)

[Empty comment from Monorail migration]

### da...@chromium.org (2018-03-16)

Yep, I can take this. Custom scheme is handled in Chrome for iOS, so we can fix this outside WebKit.

### da...@chromium.org (2018-03-16)

This bug turned out more interesting than I realized. What seems to be happening is that WKWebView starts navigating the iframe to googlechrome://test.shhnjk.com/alert.html and notifies the embedder (Chrome in this case). Chrome decides that this is an external app URL triggered by a user click, so it allows it. This triggers a dialog "Do you want to open URL in Chrome?". Once I click yes, Chrome will be automatically triggered for all future links.

Not being a sandbox expert, I'm not sure where is the right place to stop this URL:
1. Should WKWebView prevent custom URL scheme from sandboxed iframe? <== This seems the most sensible to me because only WebKit knows that the iframe is sandboxed.
2. Should Chrome prevent googlechrome scheme from any iframe? (AFAIK, Chrome can't tell if an iframe is sandboxed or not)
3. Should Chrome in its googlechrome scheme handler somehow detect that the request comes from Chrome and stops it? <== This seems more blunt than necessary, but I can't think of reasons why this scheme would be used in normal web content.

The sandbox spec (https://html.spec.whatwg.org/multipage/iframe-embed-object.html#attr-iframe-sandbox) only mentions prevention of web capabilities. Custom URL scheme is an OS level capability.

+dominickn@: Do you know who can I ask about how custom scheme is handled in sandbox for Android?

### eu...@chromium.org (2018-03-16)

+Peter, who is the owner for googlechrome:// handling. I think googlechrome:// exists to allow other iOS apps to launch Chrome. If googlechrome:// is triggered from the main frame then performing the regular navigation sounds like a reasonable UX. If googlechrome:// is triggered from iframe, then we should probably just block the navigation (we can't really force iframe navigation and doing anything else does not seem like a correct option). 

Danyao's option #2 seems like the best fix here. Peter, WDYT?

[Monorail components: -Mobile>WebView>Glue Mobile>Intents]

### do...@chromium.org (2018-03-16)

I agree that either preventing the googlechrome:// scheme from being opened from any iframe, or ignoring googlechrome:// when opened from web content seems sensible. +mariokhomenko for how external navigations like this might be handled from iframes on Android.

### eu...@chromium.org (2018-03-17)

I don't know if Chrome for iOS currently supports googlechrome:// by performing the navigation. But if it does, then removing googlechrome:// support can break existing web sites. Maybe it's fine to break those sites?

### sh...@chromium.org (2018-03-17)

[Empty comment from Monorail migration]

### do...@chromium.org (2018-03-18)

I don't see any strong reason for websites to legitimately use the googlechrome:// scheme. On iOS, it opens Chrome again, which websites can do with <a> links (and in this case, the iframe is using it to escape the sandbox which should not happen). On other platforms, it varies from doing nothing (Mac) to running the system application picker (xdg-open on Linux) since there's no handler for the googlechrome:// scheme installed.

### ma...@chromium.org (2018-03-20)

I don't believe we do anything special about googlechrome:// URLs in Android. We specify them as something we handle through intents and when we receive an intent with one, we parse out the URL and load it. If triggered through iframe, it's considered an "external protocol URL" by our external nav handler and would just be dispatched as an intent to Chrome.

### da...@chromium.org (2018-03-22)

Thanks all for the input! It sounds like on Android, the blocking of googlechrome:// URL from a sandboxed iframe is probably happening somewhere inside content layer. Since this is not done in WebKit, for iOS Chrome, everyone seems to be OK with preventing googlechrome:// scheme from any iframe.

### s....@gmail.com (2018-03-30)

Just FYI, I would like to publish this bug on November if fixed. It’d be great if this bug could be fixed before that. Thanks!

### eu...@chromium.org (2018-03-30)

Mohammad, can we fix this in AppLauncherTabHelper?

### mr...@chromium.org (2018-03-30)

this may be related this crbug.com/804054 - i think for both we should deal with googlechrome:// urls same as http or https for googlechromes when launching from the same app.


### eu...@chromium.org (2018-03-30)

This bug has quite a few comments. And the recommendation was to ignore googlechrome:// navigations coming from WKWebView.

### sh...@chromium.org (2018-04-14)

mrefaat: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### va...@chromium.org (2018-04-18)

mrefaat@ -- friendly ping from the Security 👮. Could you please share an update on the progress here? Thanks.

### mr...@chromium.org (2018-04-18)

I'm going to refactoring the AppLauncher (this Quarter) in iOS soon during that I'll be looking into this case too.
Let me know if you think i should fix it before that ?

### sh...@chromium.org (2018-05-03)

mrefaat: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### do...@chromium.org (2018-07-23)

Security sheriff ping.

mrefaat: since this is a medium-impact security bug, we ideally want to fix it within one stable milestone of reporting. This has slipped quite a bit now and it's already a quarter past your comment in #19: is it possible to try and accelerate a fix?

### mr...@chromium.org (2018-07-23)

This fall off my radar, a fix will be sent for that before end of the week (7/27)


### do...@chromium.org (2018-07-23)

Thanks for picking this up! :)

### bu...@chromium.org (2018-07-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/eee00efa1b51ac9b3f1ae4500f1d77e901ab30ab

commit eee00efa1b51ac9b3f1ae4500f1d77e901ab30ab
Author: mrefaat <mrefaat@chromium.org>
Date: Thu Jul 26 23:58:34 2018

Block URLs with Chrome Bundle URL scheme from Launching in iframes.

More context in crbug.com/822518

Bug: 850760, 822518
Cq-Include-Trybots: luci.chromium.try:ios-simulator-full-configs;master.tryserver.chromium.mac:ios-simulator-cronet
Change-Id: I66e86fdc9813456ead16b1c43c41ac218ff2ac0a
Reviewed-on: https://chromium-review.googlesource.com/1147861
Commit-Queue: Mohammad Refaat <mrefaat@chromium.org>
Reviewed-by: Peter Lee <pkl@chromium.org>
Reviewed-by: Danyao Wang <danyao@chromium.org>
Cr-Commit-Position: refs/heads/master@{#578489}
[modify] https://crrev.com/eee00efa1b51ac9b3f1ae4500f1d77e901ab30ab/ios/chrome/browser/app_launcher/BUILD.gn
[modify] https://crrev.com/eee00efa1b51ac9b3f1ae4500f1d77e901ab30ab/ios/chrome/browser/app_launcher/app_launcher_tab_helper.mm
[modify] https://crrev.com/eee00efa1b51ac9b3f1ae4500f1d77e901ab30ab/ios/chrome/browser/app_launcher/app_launcher_tab_helper_unittest.mm
[modify] https://crrev.com/eee00efa1b51ac9b3f1ae4500f1d77e901ab30ab/ios/chrome/browser/chrome_url_util.h
[modify] https://crrev.com/eee00efa1b51ac9b3f1ae4500f1d77e901ab30ab/ios/chrome/browser/chrome_url_util.mm
[modify] https://crrev.com/eee00efa1b51ac9b3f1ae4500f1d77e901ab30ab/ios/chrome/browser/chrome_url_util_unittest.mm


### eu...@chromium.org (2018-07-31)

Should we mark this as fixed and send on retest?

### mr...@chromium.org (2018-07-31)

Yes, closing it.

### s....@gmail.com (2018-07-31)

Sounds like CSP sandbox wasn't considered in the fix. Are you fixing that in https://crbug.com/chromium/852489?

### sh...@chromium.org (2018-08-01)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-08-08)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-08-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-08-13)

Thanks as ever! $1,000 for this report. Cheers!

### aw...@google.com (2018-08-13)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-09-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-09-14)

This bug requires manual review: Less than 28 days to go before AppStore submit on M70
Please contact the milestone owner if you have questions.
Owners: benmason@(Android), kariahda@(iOS), geohsu@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ka...@chromium.org (2018-09-17)

This initially landed in M70. No merge needed.
https://storage.googleapis.com/chromium-find-releases-static/eee.html#eee00efa1b51ac9b3f1ae4500f1d77e901ab30ab

### ka...@chromium.org (2018-09-17)

[Empty comment from Monorail migration]

### aw...@google.com (2018-09-25)

[Empty comment from Monorail migration]

### aw...@google.com (2018-10-15)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-10-16)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-11-07)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-11-12)

[Empty comment from Monorail migration]

### is...@google.com (2018-11-12)

This issue was migrated from crbug.com/chromium/822518?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40090810)*
