# Chrome iOS is Vulnerable to Permission Tapjacking

| Field | Value |
|-------|-------|
| **Issue ID** | [341353783](https://issues.chromium.org/issues/341353783) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Mobile>iOSWeb>Security |
| **Platforms** | iOS |
| **Reporter** | fa...@gmail.com |
| **Assignee** | mi...@google.com |
| **Created** | 2024-05-18 |
| **Bounty** | $1,000.00 |

## Description

Security Bug

---

**VULNERABILITY DETAILS**

Using a simple double tap from a victim, an attacker’s site can enable security permissions like location, camera, or microphone permissions from the victim.

Similar to Chrome for Android and desktop, the iOS version of Chrome should also enable clickjacking protection (such as a delay between consecutive clicks) to protect users from such attacks.

**VERSION**

Chrome Version: 125.0.6422.51

Operating System: iOS 17.5

**REPRODUCTION CASE**

1. Download the proof of concept file below: poc.html.
2. Open this file on an iOS device or visit <https://test-ece44.web.app/ios/poc.html> for testing.

**CREDIT INFORMATION**

Reporter credit: Shaheen Fazim

## Attachments

- iOS-camera-demo.mp4 (video/mp4, 2.7 MB)
- poc.html (text/html, 1.3 KB)
- iOS Tapjack.html (text/html, 1.3 KB)
- new-demo.mp4 (video/mp4, 1.4 MB)
- new.html (text/html, 2.3 KB)

## Timeline

### ph...@chromium.org (2024-05-20)

[fazim.pentester@gmail.com](mailto:fazim.pentester@gmail.com): Could you also upload the poc.html as an attachment, so we don't rely on the poc you hosted?

### ph...@chromium.org (2024-05-20)

Security shepherd: I can reproduce on iOS. However, after the second tap, it was very clear that I enabled camera permission and there's a banner that I can click to edit the permission, so not sure if this is a serious vulnerability.

### ph...@chromium.org (2024-05-20)

rohitrao@: Could you help triage this Chrome iOS issue?

### fa...@gmail.com (2024-05-20)

Hi there, yes for camera iOS shows a banner, but other permissions like microphone can also be captured.

### fa...@gmail.com (2024-05-20)

I used the camera just as an example, but any permission could alert the user later by an icon, or the site can be closed easily. However, the initial quick snapshot from the camera most useful thing for an attacker site.

### pe...@google.com (2024-05-20)

Setting Priority to P2 to match Severity s3. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### fa...@gmail.com (2024-06-18)

Ping.

### am...@chromium.org (2024-07-13)

Hello, Shaheen, thank you for checking in on this issue. Since this is a low severity issue, there is no SLO and work on low severity issues must come behind time sensitive work on more critical issues.
This is in the hands of the correct team. I've reassigned to ajuma@ for specific visbility there, but it may be some time before this issue can be prioritized.

### aj...@google.com (2024-07-15)

We could try to do something similar to what Android did in <https://chromium-review.googlesource.com/c/chromium/src/+/4242477>, disabling the permission dialog buttons for 500ms. That would require changes in ios/chrome/browser/overlays/, specifically to [PermissionsDialogRequest](https://source.chromium.org/chromium/chromium/src/+/main:ios/chrome/browser/overlays/model/public/web_content_area/permissions_dialog_overlay.h;l=26;bpv=1;bpt=1).

### fa...@gmail.com (2024-07-24)

Friendly ping.

### mi...@google.com (2024-07-25)

Thanks for the ping. I'm taking a look working around this per Ali's recommendataion in [#comment10](https://issues.chromium.org/issues/341353783#comment10)
However, per [#comment2](https://issues.chromium.org/issues/341353783#comment2), could you please attach the poc source to this bug?

### mi...@google.com (2024-07-25)

deleted

### fa...@gmail.com (2024-07-25)

Yes.

### ap...@google.com (2024-07-26)

Project: chromium/src
Branch: main

commit 48164a2450f89e79f23fb0954d7768e40efc8ada
Author: Mike Dougherty <michaeldo@chromium.org>
Date:   Fri Jul 26 17:36:08 2024

    Initially disable alert action buttons
    
    Fixed: 341353783
    Change-Id: I54408c4839a88f671c3ca330a8b2c138d5848914
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5742453
    Reviewed-by: Sergio Collazos <sczs@chromium.org>
    Code-Coverage: findit-for-me@appspot.gserviceaccount.com <findit-for-me@appspot.gserviceaccount.com>
    Commit-Queue: Mike Dougherty <michaeldo@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1333654}

M       ios/chrome/browser/alert_view/ui_bundled/alert_consumer.h
M       ios/chrome/browser/alert_view/ui_bundled/alert_view_controller.mm
M       ios/chrome/browser/alert_view/ui_bundled/test/fake_alert_consumer.h
M       ios/chrome/browser/ui/overlays/web_content_area/alerts/alert_overlay_coordinator.mm
M       ios/chrome/browser/web/model/http_auth_egtest.mm

https://chromium-review.googlesource.com/5742453


### sp...@google.com (2024-08-01)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
baseline report of lower impact web platform privilege escalation


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-08-02)

Thank you for your efforts and reporting this issue to us, Shaheen!

### fa...@gmail.com (2024-08-02)

Thanks for the fix and the bounty.

### fa...@gmail.com (2024-08-03)

Hi VRP Panel,

I would like to reevaluate this issue. It seems the Chrome VRP team will be busy next week, so I would like to request reevaluation the week after next.

I believe the reason behind only a 1,000 reward for a permission tapjacking issue is that my video demo shows the camera notification. However, this is not exactly the case. The attacker's website could redirect the tab or cancel this notification immediately after granting permission, capturing one frame as an image without the victim knowing. I have also mentioned this in [comment #6](https://issues.chromium.org/issues/341353783#comment6) while arguing for higher severity.

> I used the camera just as an example, but any permission could alert the user later by an icon, or the site can be closed easily. However, the initial quick snapshot from the camera most useful thing for an attacker site (Message last modified on May 20, 2024 08:26PM).

I have attached the video demo as well.

You could also test this online by visiting: <https://test-ece44.web.app/ios/new.html>. I have also attached the file, but it requires you to host it on an HTTPS server to make the permissions work.

### fa...@gmail.com (2024-08-03)

Above is a method to avoid the camera notification. I don't know if this is a security issue. It seems it's easy to avoid this notification showing the camera in use, as mentioned above. However, the original issue here is the iOS permission prompt, which was vulnerable to tapjacking, which is fixed now.

### fa...@gmail.com (2024-08-09)

See also issue: https://issues.chromium.org/issues/357143196 (duplicate).

This mentions another vulnerability reported by me, which is a different case affecting Incognito leaving prompt. This issue is also fixed as part of the same root cause (not publicly released), so two different attack scenarios are currently provided. I hope the VRP panel takes this into consideration as well.

### fa...@gmail.com (2024-08-28)

Hi, kindly update on this fixed issue.

### am...@chromium.org (2024-09-10)

Hi Shaheen, we have not done a reassessment on this issue yet, which is why there has not yet been an update.
I did want to respond to c#21, the other issue ([crbug.com/357143196](https://crbug.com/357143196)) is a duplicate, same root cause and similar attack vector and preconditions. This would not warrant a higher reward.
That being said, we will still give it another look at a future VRP panel session.

### am...@chromium.org (2024-09-11)

Hi Shaheen, we did give this another look today, but we have determined that this reward is sufficient for this issue and impact. It is also consistent with recent reward amounts for click/tap jacking given the visibility of the prompt to the user (even if quickly) and the low potential for user harm.

### fa...@gmail.com (2024-09-11)

Well, thanks for checking the issue again.

### pe...@google.com (2024-11-02)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/341353783)*
