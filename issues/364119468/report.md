# Clickjacking on permission prompt using PIP

| Field | Value |
|-------|-------|
| **Issue ID** | [364119468](https://issues.chromium.org/issues/364119468) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>Media>PictureInPicture, UI>Browser>Permissions, UI>Browser>Permissions>Prompts |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | sa...@gmail.com |
| **Assignee** | en...@chromium.org |
| **Created** | 2024-09-03 |
| **Bounty** | $1,000.00 |

## Description

VULNERABILITY DETAILS

This vulnerability is clickjacking on the permission prompt using the pip window and select option.the impact is clickjacking on permission prompt

VERSION
Chrome Version: 130.0.6695.0 (Official Build) canary (64-bit)
Operating System: Windows 10

REPRODUCTION CASE
1. open pocfedcm.html
2. double click on "click here" button
3. do double click on "Double  Click here.." option


CREDIT INFORMATION
Externally reported security bugs may appear in Chrome release notes. If this bug is included, how would you like to be credited?
Reporter credit: [goes here]

## Attachments

- [bandicam 2024-09-03 17-43-30-938.mp4](attachments/bandicam 2024-09-03 17-43-30-938.mp4) (video/mp4, 1.5 MB)
- deleted (application/octet-stream, 0 B)
- [clickjackpipwindow.html](attachments/clickjackpipwindow.html) (text/html, 2.2 KB)
- [permshow.html](attachments/permshow.html) (text/html, 216 B)
- [urldomainnotshow.png](attachments/urldomainnotshow.png) (image/png, 235.8 KB)
- [buttonnotshown.html](attachments/buttonnotshown.html) (text/html, 372 B)
- [buttonnotshow.png](attachments/buttonnotshow.png) (image/png, 218.5 KB)
- [bandicam 2025-11-05 15-52-12-554.mp4](attachments/bandicam 2025-11-05 15-52-12-554.mp4) (video/mp4, 2.4 MB)

## Timeline

### ct...@chromium.org (2024-09-03)

The description and POC appear to be a duplicate of your earlier [Issue 362010093](https://issues.chromium.org/issues/362010093) -- did you mean to upload a new issue involving picture-in-picture instead of <select>?

### sa...@gmail.com (2024-09-03)

It's just the same name but different from 362010093

### ct...@chromium.org (2024-09-03)

Ah okay the poc code was a bit hard to read (in the future, pretty-printed/cleaned up POCs make things much easier). The distinction is that the <select> is added into the pip window, which then is interacted with to overlay on top of the FedCM dialog for click jacking. [Issue 362010093](https://issues.chromium.org/issues/362010093) is still not fixed it looks like -- do you have reason to think these have different root causes?

### sa...@gmail.com (2024-09-03)

the difference is that the permission prompt appears in a new window behind the pip window whereas in fedcm it is in the same window

### pe...@google.com (2024-09-03)

Thank you for providing more feedback. Adding the requester to the CC list.

### ct...@chromium.org (2024-09-03)

I'm still a bit confused: in the poc the permission prompt lines are commented out and only the FedCM line is triggered. Stepping through the video very closely I now see that a camera permission is shown, coming up from a popup window that is positioned behind the PiP (so the permission popup gets rendered upwards due to small window). This was made more confusing because the window is titled "fedcmv1.html" but there is no FedCM involvement here.

Could you make sure you have uploaded the full updated POC here and please do a cleanup pass on it to make sure it is fully as intended? Then I can work on triaging this to the right folks.

### sa...@gmail.com (2024-09-03)

REPRODUCTION CASE

1. download clickjackpipwindow.html and permshow.html
2. open clickjackpipwindow.html
3. double click on "click here" button
4. do double click on "Double Click here.." option

besides clickjacking the origin domain on the permission prompt is not visible (cut off at the top) causing confusion.

### ct...@chromium.org (2024-09-04)

Thank you! That helps a lot.

Passing this to the Permissions team as this seems like the root cause is in how we determine page visibility/focus given the existence of a PiP window. engedy@ could you help look at this or help re-assign?

Also CC'ing PiP folks in case they have ideas.

### ct...@chromium.org (2024-09-04)

Setting Severity-Low (S3) due to the multiple user interactions required. I can't repro on Stable, partially due to Stable not seeming to have the new Camera permission prompt (see the screenshot in [Comment #8](https://issues.chromium.org/issues/364119468#comment8) for reference). I believe that is behind the kCameraMicPreview flag, which appears to be enabled via Finch starting in M127, so setting FoundIn-128 for the current Stable (with the right experiment groups, this seems likely reproducible).

### ct...@chromium.org (2024-09-04)

cc'ing the CameraMicPreview owners as well for visibility.

### pe...@google.com (2024-09-04)

Setting Priority to P2 to match Severity s3. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### sa...@gmail.com (2024-09-05)

the permission button on the permission prompt is not visible (cut off at the buttom)

### pe...@google.com (2024-09-05)

The NextAction date has arrived: 2024-09-05
To opt-out from this automation rule, please add Optout-Blintz-Nextaction-Alert to the "Chromium Labels" custom field.

### br...@chromium.org (2024-09-30)

The presence of the camera/mic preview would only change the position of the buttons. I think this should still be reproducible without it as long as the select popup is adjusted to be positioned over the allow button.

### sa...@gmail.com (2025-01-21)

hello any updates?

### sa...@gmail.com (2025-03-14)

hello any updates?

### sa...@gmail.com (2025-11-05)

hello this bug is fixed because i can't reproduce this bug on Version 144.0.7509.0 (Official Build) canary (64-bit). when after double click the select option, the select option is closed then  it cannot allow the permission (the permission prompt still appears.  Can you set this bug to fixed?

### ch...@google.com (2025-11-13)

Dear owner, thanks for fixing this bug. We've reopened it because:

- Some CLs listed in the “Fixed By Code Changes” field are invalid and have been removed. Please provide an appropriate Gerrit url that matches the pattern: `https://<host>-review.googlesource.com/c/<repo>/+/<change_number>` or use the value 'NA' and re-mark this bug as fixed. If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### sp...@google.com (2025-12-09)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
Web Platform Privilege Escalation


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-03-04)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> Web Platform Privilege Escalation

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/364119468)*
