# Regression: External protocol confirmation dialog may overlap with other origins

| Field | Value |
|-------|-------|
| **Issue ID** | [40064442](https://issues.chromium.org/issues/40064442) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Mobile>Intents, UI>Browser>Navigation |
| **Platforms** | iOS |
| **Reporter** | zy...@gmail.com |
| **Assignee** | qp...@google.com |
| **Created** | 2023-05-09 |
| **Bounty** | $2,000.00 |

## Description

**Steps to reproduce the problem:**

1. 1.Open the attached spoof\_ioschrome.html using iOS chrome:

```
<script>  
location.href = "tg:1"  
//location.href = "tel:1"  
setTimeout('location.href = "https://apple.com"', 500)  
</script>  

```

2. you should see the external protocol confirmation dialog overlaid on apple.com as shown in the screenshot soon.

**Problem Description:**  

Previously, I reported <https://crbug.com/chromium/1151644>: Security: Incorrect iOS Security UI when using external confirmation on Nov 22, 2020, it was triggered as duplicate with <https://crbug.com/chromium/1103119>.

<https://crbug.com/chromium/1103119> was fixed at 2021 at commit <https://chromium-review.googlesource.com/c/chromium/src/+/2627751>.

But I found this spoofing issue is still existed on iOS Chrome 113.0.5672.69（lastest version on iOS)

**Additional Comments:**  

All screenshots contain Chinese. Please feel free to ask me if you have any questions.

\*\*Chrome version: \*\* 113.0.5672.69 \*\*Channel: \*\* Stable

**OS:** iOS

## Attachments

- [spoof_ioschrome.html](attachments/spoof_ioschrome.html) (text/plain, 138 B)
- [PHOTO_20230509_103930056.jpg](attachments/PHOTO_20230509_103930056.jpg) (image/jpeg, 796.2 KB)
- [PHOTO_20230509_103930216.jpg](attachments/PHOTO_20230509_103930216.jpg) (image/jpeg, 654.3 KB)

## Timeline

### [Deleted User] (2023-05-09)

[Empty comment from Monorail migration]

### nh...@google.com (2023-05-09)

This is potentially a duplicate of crbug.com/1443158

### me...@chromium.org (2023-05-12)

ajuma: Can you please take a look? I CC'ed you on https://crbug.com/chromium/1443158 as well. Thanks.

[Monorail components: UI>Browser>Navigation]

### me...@chromium.org (2023-05-12)

Severity-medium since this overlays a dialog on top of apple.com. The repro is indeed similar to https://crbug.com/chromium/1443158, but the eventual UI treatment is significantly different:
 In this bug, it looks like apple.com is initiating a call, whereas in https://crbug.com/chromium/1443158 the message makes it clear that the user is navigating away from the page.

### aj...@chromium.org (2023-05-12)

The issue here is that in app_launcher_browser_agent.mm, we don't wait for the completion handler to get called in LaunchExternalApp.

One way to fix this bug would be for AppLauncherTabHelper::ShouldAllowRequest to defer calling its callback until its delegate (AppLauncherBrowserAgent) is no longer waiting for a completion handler call in LaunchExternalApp.

[Monorail components: Mobile>Intents]

### ad...@google.com (2023-05-12)

(I am a bot: this is an auto-cc on a security bug)

### dj...@chromium.org (2023-05-15)

[Empty comment from Monorail migration]

### qp...@google.com (2023-05-15)

[Empty comment from Monorail migration]

### qp...@google.com (2023-05-17)

Add reviewer to CC

### [Deleted User] (2023-05-22)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2023-05-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/f79cad2304b53fe4a6b92f16480ae874bb5b6d76

commit f79cad2304b53fe4a6b92f16480ae874bb5b6d76
Author: Quentin Pubert <qpubert@google.com>
Date: Fri May 26 09:43:46 2023

[iOS] Postpone policy decision callback while app launch pending

As of now, if there is an app launch request pending through `openURL`,
likely because the user is being prompted "Chrome wants to open App",
the web page can still load another page e.g. using `location.href=...`.
This makes it possible for a page to spoof the user by first triggering
an app launch request and then loading a page the user trusts.

To solve this issue, this CL ensures the app launch tab helper keeps
track of any pending app launch request and postpones all later policy
decision callbacks until the app launch completes. If a navigation
request arrives which should trigger an app launch, it will be canceled
if there is already an app launch pending in this tab. App launch
requests are already dismissed if the user is being prompted.

Fixed: 1443722
Change-Id: I94bbb5ccbcd99233611c890263ee9b522ed55923
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4543041
Reviewed-by: Sylvain Defresne <sdefresne@chromium.org>
Commit-Queue: Quentin Pubert <qpubert@google.com>
Reviewed-by: Ali Juma <ajuma@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1149629}

[modify] https://crrev.com/f79cad2304b53fe4a6b92f16480ae874bb5b6d76/ios/chrome/browser/app_launcher/app_launcher_browser_agent_unittest.mm
[modify] https://crrev.com/f79cad2304b53fe4a6b92f16480ae874bb5b6d76/ios/chrome/browser/app_launcher/app_launcher_browser_agent.mm
[modify] https://crrev.com/f79cad2304b53fe4a6b92f16480ae874bb5b6d76/ios/chrome/browser/app_launcher/app_launcher_tab_helper_delegate.h
[modify] https://crrev.com/f79cad2304b53fe4a6b92f16480ae874bb5b6d76/ios/chrome/browser/app_launcher/app_launcher_browser_agent.h
[modify] https://crrev.com/f79cad2304b53fe4a6b92f16480ae874bb5b6d76/ios/chrome/browser/app_launcher/app_launcher_tab_helper.h
[modify] https://crrev.com/f79cad2304b53fe4a6b92f16480ae874bb5b6d76/ios/chrome/browser/app_launcher/app_launcher_tab_helper.mm
[modify] https://crrev.com/f79cad2304b53fe4a6b92f16480ae874bb5b6d76/ios/chrome/browser/app_launcher/app_launcher_tab_helper_unittest.mm


### [Deleted User] (2023-05-26)

Dear owner, thanks for fixing this bug. We’ve reopened it because security bugs need Security_Severity and FoundIn labels set, which will enable the bots to request merges to the correct branches ( as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact (security@chromium.org) to arrange to set these labels and then this bug can be marked closed again. Thank you! Severity guidelines: https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues FoundIn guidelines: https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security Thanks for your time! 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-05-31)

qpubert: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### qp...@google.com (2023-06-01)

[Empty comment from Monorail migration]

### qp...@google.com (2023-06-01)

[Empty comment from Monorail migration]

### qp...@google.com (2023-06-01)

A few more CLs are required to fix this bug completely, right now pending review.

### [Deleted User] (2023-06-01)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-02)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2023-06-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/c98ce711f7159914d0d39e1f81a74bb4d69cede6

commit c98ce711f7159914d0d39e1f81a74bb4d69cede6
Author: Quentin Pubert <qpubert@google.com>
Date: Tue Jun 06 13:47:48 2023

[iOS] Pass completion handler to MailtoHandlerService::HandleMailtoURL()

As the app launcher browser agent now expects to be called back when an
app launch has completed, this CL extends the MailtoHandlerService API
to allow for passing a completion handler to HandleMailtoURL().

Other CLs will follow-up to provide implementations in all subclasses of
MailtoHandlerService() and clean-up. For the moment, a default
implementation is provided which simply forwards the URL to
`HandleMailtoURL(url)` and then calls the provided completion handler.

Bug: 1443722
Change-Id: Iab6d45303cf8f896b1b3602d9cdee706b186b25f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4577317
Commit-Queue: Quentin Pubert <qpubert@google.com>
Reviewed-by: Rohit Rao <rohitrao@chromium.org>
Reviewed-by: Olivier Robin <olivierrobin@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1153812}

[modify] https://crrev.com/c98ce711f7159914d0d39e1f81a74bb4d69cede6/ios/public/provider/chrome/browser/mailto_handler/mailto_handler_api.h
[modify] https://crrev.com/c98ce711f7159914d0d39e1f81a74bb4d69cede6/ios/chrome/browser/mailto_handler/mailto_handler_service.h
[modify] https://crrev.com/c98ce711f7159914d0d39e1f81a74bb4d69cede6/ios/chrome/browser/providers/mailto_handler/chromium_mailto_handler.mm
[modify] https://crrev.com/c98ce711f7159914d0d39e1f81a74bb4d69cede6/ios/chrome/browser/providers/mailto_handler/BUILD.gn
[modify] https://crrev.com/c98ce711f7159914d0d39e1f81a74bb4d69cede6/ios/chrome/browser/mailto_handler/BUILD.gn
[modify] https://crrev.com/c98ce711f7159914d0d39e1f81a74bb4d69cede6/ios/chrome/browser/mailto_handler/mailto_handler_service.mm
[modify] https://crrev.com/c98ce711f7159914d0d39e1f81a74bb4d69cede6/ios/chrome/browser/app_launcher/app_launcher_browser_agent_unittest.mm
[modify] https://crrev.com/c98ce711f7159914d0d39e1f81a74bb4d69cede6/ios/chrome/browser/app_launcher/app_launcher_browser_agent.mm
[modify] https://crrev.com/c98ce711f7159914d0d39e1f81a74bb4d69cede6/ios/chrome/test/providers/mailto_handler/test_mailto_handler.mm
[modify] https://crrev.com/c98ce711f7159914d0d39e1f81a74bb4d69cede6/ios/chrome/browser/mailto_handler/mailto_handler_service_factory.mm
[modify] https://crrev.com/c98ce711f7159914d0d39e1f81a74bb4d69cede6/ios/chrome/test/providers/mailto_handler/BUILD.gn


### gi...@appspot.gserviceaccount.com (2023-06-07)

The following revision refers to this bug:
  https://chrome-internal.googlesource.com/chrome/ios_internal/+/411680ba842c639f2e03a5b3a24c16cde6239d2f

commit 411680ba842c639f2e03a5b3a24c16cde6239d2f
Author: Quentin Pubert <qpubert@google.com>
Date: Wed Jun 07 12:16:57 2023


### gi...@appspot.gserviceaccount.com (2023-06-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/3b9d6d6136de875547ad0475d592000ef2e54737

commit 3b9d6d6136de875547ad0475d592000ef2e54737
Author: chromium-internal-autoroll <chromium-internal-autoroll@skia-corp.google.com.iam.gserviceaccount.com>
Date: Thu Jun 08 06:34:24 2023

Roll ios_internal from 491021d96544 to 33118dd71eb9

https://chrome-internal.googlesource.com/chrome/ios_internal.git/+log/491021d96544..33118dd71eb9

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://skia-autoroll.corp.goog/r/ios-internal-chromium-autoroll
Please CC chrome-brapp-engprod@google.com,eic@google.com,tinazwang@google.com on the revert to ensure that a human
is aware of the problem.

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Bug: chromium:1443722,chromium:1451941,chromium:1452207
Change-Id: I36796b6670e08531af756b08cd7a5e1d0d8dcdd6
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4597997
Commit-Queue: chromium-internal-autoroll <chromium-internal-autoroll@skia-corp.google.com.iam.gserviceaccount.com>
Bot-Commit: chromium-internal-autoroll <chromium-internal-autoroll@skia-corp.google.com.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#1154784}

[modify] https://crrev.com/3b9d6d6136de875547ad0475d592000ef2e54737/DEPS


### gi...@appspot.gserviceaccount.com (2023-06-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/fda971195288772725ee952225d59eecfaeef2b5

commit fda971195288772725ee952225d59eecfaeef2b5
Author: Quentin Pubert <qpubert@google.com>
Date: Tue Jun 13 10:58:36 2023

[iOS] Clean-up MailtoHandlerService::HandleMailtoURL()

This CL finishes removing MailtoHandlerService::HandleMailtoURL(url) now
that it has been replaced everywhere with its asynchronous alternative.

Fixed: 1443722
Change-Id: I3f3a1fb77b59e9db844a3bbf547d5f181968b33d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4601459
Reviewed-by: Olivier Robin <olivierrobin@chromium.org>
Commit-Queue: Quentin Pubert <qpubert@google.com>
Auto-Submit: Quentin Pubert <qpubert@google.com>
Reviewed-by: Rohit Rao <rohitrao@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1156828}

[modify] https://crrev.com/fda971195288772725ee952225d59eecfaeef2b5/ios/chrome/browser/mailto_handler/mailto_handler_service.h
[modify] https://crrev.com/fda971195288772725ee952225d59eecfaeef2b5/ios/chrome/browser/providers/mailto_handler/chromium_mailto_handler.mm
[modify] https://crrev.com/fda971195288772725ee952225d59eecfaeef2b5/ios/chrome/browser/mailto_handler/mailto_handler_service.mm
[modify] https://crrev.com/fda971195288772725ee952225d59eecfaeef2b5/ios/chrome/test/providers/mailto_handler/test_mailto_handler.mm


### [Deleted User] (2023-06-13)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-13)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-13)

Requesting merge to beta M115 because latest trunk commit (1156828) appears to be after beta branch point (1148114).

Merge review required: a commit with DEPS changes was detected.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [115].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### qp...@google.com (2023-06-14)

1. Which CLs should be backmerged? (Please include Gerrit links.)

- [iOS] Postpone policy decision callback while app launch pending
  (May 26, 11:43 AM) https://chromium-review.googlesource.com/c/chromium/src/+/4543041
- [iOS] Let -[GCRGrowthKitLinkOpener openURL:...] accept completion handler
  (May 26, 4:32 PM) https://critique.corp.google.com/cl/535613215
- [iOS] Pass completion handler to MailtoHandlerService::HandleMailtoURL()
  (Jun 06, 3:47 PM) https://chromium-review.googlesource.com/c/chromium/src/+/4577317
- [iOS] Pass a completion handler to MailtoHandlerService::HandleMailtoURL
  (Jun 07, 2:58 PM) https://chrome-internal-review.googlesource.com/c/chrome/ios_internal/+/6017416
- [iOS] Clean-up -[GCRGrowthKitLinkOpener openURL:hashedUserID:]
  (Jun 07, 4:01 PM) https://critique.corp.google.com/cl/538474787
- [iOS] Clean-up MailtoHandlerService::HandleMailtoURL()
  (Jun 13, 12:58 PM) https://chromium-review.googlesource.com/c/chromium/src/+/4601459

2. Has this fix been tested on Canary?

Tested on 116.0.5831.1 (Official Build) canary (64-bit)

3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?

Yes, to the best of my knowledge

4. Does this fix pose any known compatibility risks?

No, to the best of my knowledge

5. Does it require manual verification by the test team? If so, please describe required testing.

Unit tests are being submitted to prevent any future regressions


### [Deleted User] (2023-06-14)

Requesting merge to beta M115 because latest trunk commit (1156828) appears to be after beta branch point (1148114).

Merge review required: a commit with DEPS changes was detected.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [115].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### qp...@google.com (2023-06-15)

1. Which CLs should be backmerged? (Please include Gerrit links.)

- [iOS] Postpone policy decision callback while app launch pending
  (May 26, 11:43 AM) https://chromium-review.googlesource.com/c/chromium/src/+/4543041
- [iOS] Let -[GCRGrowthKitLinkOpener openURL:...] accept completion handler
  (May 26, 4:32 PM) https://critique.corp.google.com/cl/535613215
- [iOS] Pass completion handler to MailtoHandlerService::HandleMailtoURL()
  (Jun 06, 3:47 PM) https://chromium-review.googlesource.com/c/chromium/src/+/4577317
- [iOS] Pass a completion handler to MailtoHandlerService::HandleMailtoURL
  (Jun 07, 2:58 PM) https://chrome-internal-review.googlesource.com/c/chrome/ios_internal/+/6017416
- [iOS] Clean-up -[GCRGrowthKitLinkOpener openURL:hashedUserID:]
  (Jun 07, 4:01 PM) https://critique.corp.google.com/cl/538474787
- [iOS] Clean-up MailtoHandlerService::HandleMailtoURL()
  (Jun 13, 12:58 PM) https://chromium-review.googlesource.com/c/chromium/src/+/4601459

2. Has this fix been tested on Canary?

Tested on 116.0.5831.1 (Official Build) canary (64-bit)

3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?

Yes, to the best of my knowledge

4. Does this fix pose any known compatibility risks?

No, to the best of my knowledge

5. Does it require manual verification by the test team? If so, please describe required testing.

Unit tests are being submitted to prevent any future regressions

### [Deleted User] (2023-06-15)

Requesting merge to beta M115 because latest trunk commit (1156828) appears to be after beta branch point (1148114).

Merge review required: a commit with DEPS changes was detected.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [115].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-06-16)

Requesting merge to beta M115 because latest trunk commit (1156828) appears to be after beta branch point (1148114).

Merge review required: a commit with DEPS changes was detected.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [115].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-06-17)

Requesting merge to beta M115 because latest trunk commit (1156828) appears to be after beta branch point (1148114).

Merge review required: a commit with DEPS changes was detected.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [115].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-06-18)

Requesting merge to beta M115 because latest trunk commit (1156828) appears to be after beta branch point (1148114).

Merge review required: a commit with DEPS changes was detected.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [115].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### qp...@google.com (2023-06-19)

[Empty comment from Monorail migration]

### qp...@google.com (2023-06-19)

1. Which CLs should be backmerged? (Please include Gerrit links.)

- [iOS] Postpone policy decision callback while app launch pending
  (May 26, 11:43 AM) https://chromium-review.googlesource.com/c/chromium/src/+/4543041
- [iOS] Let -[GCRGrowthKitLinkOpener openURL:...] accept completion handler
  (May 26, 4:32 PM) https://critique.corp.google.com/cl/535613215
- [iOS] Pass completion handler to MailtoHandlerService::HandleMailtoURL()
  (Jun 06, 3:47 PM) https://chromium-review.googlesource.com/c/chromium/src/+/4577317
- [iOS] Pass a completion handler to MailtoHandlerService::HandleMailtoURL
  (Jun 07, 2:58 PM) https://chrome-internal-review.googlesource.com/c/chrome/ios_internal/+/6017416
- [iOS] Clean-up -[GCRGrowthKitLinkOpener openURL:hashedUserID:]
  (Jun 07, 4:01 PM) https://critique.corp.google.com/cl/538474787
- [iOS] Clean-up MailtoHandlerService::HandleMailtoURL()
  (Jun 13, 12:58 PM) https://chromium-review.googlesource.com/c/chromium/src/+/4601459

2. Has this fix been tested on Canary?

Tested on 116.0.5831.1 (Official Build) canary (64-bit)

3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?

Yes, to the best of my knowledge

4. Does this fix pose any known compatibility risks?

No, to the best of my knowledge

5. Does it require manual verification by the test team? If so, please describe required testing.

Unit tests are being submitted to prevent any future regressions

### go...@chromium.org (2023-06-20)

+Security TPMs for M115 merge review

### go...@chromium.org (2023-06-22)

Please note there are multiple CLs needed to merge, security severity medium and we're very late in M115 release cycle so best this can wait for M116.

But will let Security TPMs make a merge decision. 

### am...@chromium.org (2023-06-22)

Apologies, I had a draft response written but realizing I never submitted it. I evaluated these CLs and do not feel confident in backmerging this amount of changes for 115 at this juncture, especially given this change is dependent on internal changes in tandem with Chromium changes. While this sort of prompt overlay should not occur, it seems reasonable to delay the shipping of this fix in Stable given the scope of changes to backport.  

### am...@google.com (2023-06-24)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-06-24)

Congratulations! The VRP Panel has decided to award you $2,000 for this report. Thank you for your efforts and reporting this issue to us. 

### zy...@gmail.com (2023-06-25)

Thank you so much, Amy!

### am...@google.com (2023-06-26)

[Empty comment from Monorail migration]

### zy...@gmail.com (2023-07-04)

Hi, please credit to `retsew0x01`, thanks!

### am...@chromium.org (2023-08-11)

[Empty comment from Monorail migration]

### am...@google.com (2023-08-15)

[Empty comment from Monorail migration]

### pg...@google.com (2023-08-15)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-19)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### li...@gmail.com (2023-09-20)

[Comment Deleted]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1443722?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Mobile>Intents, UI>Browser>Navigation]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40064442)*
