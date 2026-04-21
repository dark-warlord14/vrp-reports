# Origin spoofing in WebUSB

| Field | Value |
|-------|-------|
| **Issue ID** | [40058243](https://issues.chromium.org/issues/40058243) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>HID, Blink>Serial, Blink>USB |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | bu...@gmail.com |
| **Assignee** | re...@chromium.org |
| **Created** | 2021-12-15 |
| **Bounty** | $3,000.00 |

## Description

Chrome Version : 96.0.4664.93 (Official Build) (64-bit) (cohort: Stable)  

**URLs (if applicable) :**  

**Other browsers tested:**  

Add OK or FAIL, along with the version, after other browsers where you  

**have tested this issue:**  

Safari: N/A  

Firefox: N/A  

Edge: OK

**What steps will reproduce the problem?**  

**(1)** Embed an iframe on an attacker web page to embed a target website that uses the WebUSB feature. The attacker web page can be hosted on a different domain (e.g. evil.com) than the target web page (e.g. good.com).  

**(2)** In the iframe, click on a UI element that initiates a WebUSB operation.

**What is the expected result?**  

The WebUSB confirmation box shows the domain of the iframe (good.com) and lists the filtered USB devices. When a device is selected, only the iframe (good.com) should has access to the selected device.

**What happens instead?**  

The parent web page (evil.com) and the iframe (good.com) will both have access to the selected device regardless of who initiated the request (parent web page or the iframe). This allows an adversary to use another domain to convince the user that it connects to the official one. This becomes especially problematic if a desktop/mobile web app is accessed via the "add to home screen" option, because that hides the URL address bar of the browser. On chrome://settings/content/usbDevices, Chrome states that the selected device is only connected to the parent web page (evil.com), but effectively, both the iframe and the parent have access to the selected device.

Note that this issue does not apply for websites that explicitly prevent third-party sites from embedding them in an iframe using e.g X-Frame headers (see <https://developer.mozilla.org/fr/docs/Web/HTTP/Headers/X-Frame-Options>)

Attached is the following:

- a PoC pretending to connect to the Vysor Android mirroring service (<https://app.vysor.io/#/>)
- a skeleton example for the issue and its effect
- demo videos for both examples

## Attachments

- [app.vysor.io demo.mp4](attachments/app.vysor.io demo.mp4) (video/mp4, 1.4 MB)
- [poc demo.mp4](attachments/poc demo.mp4) (video/mp4, 3.3 MB)
- [sample code.zip](attachments/sample code.zip) (application/octet-stream, 2.8 KB)

## Timeline

### ve...@chromium.org (2021-12-15)

[Empty comment from Monorail migration]

[Monorail components: Blink>USB]

### re...@chromium.org (2021-12-15)

This was missed during the changes made in https://crbug.com/chromium/824985 to implement permissions delegation for WebUSB and related APIs. crrev/c/2352885 updated the permission management code to use the top-level origin but didn't update the permissions UI code to display the top-level origin to the user in the permission request itself. To fix this CreateExtensionAwareChooserTitle() and permissions::CreateChooserTitle() need to be updated to call GetMainFrame() on the provided RenderFrameHost.

[Monorail components: Blink>HID Blink>Serial]

### re...@chromium.org (2021-12-15)

Chris will put together a fix.

### cm...@google.com (2021-12-20)

[Empty comment from Monorail migration]

### cm...@chromium.org (2022-01-09)

WIP test CL at https://crrev.com/c/3353956

### cm...@google.com (2022-01-11)

Reilly:

Can I give https://crrev.com/c/3353956 to you for completion? I started to convert the unit-test to a browsertest as requested by jam@. At present he test loads the frame, but CreateChooserTitle fails to load the string resource (at least on Windows).

### re...@chromium.org (2022-01-22)

I've fixed up the unit tests and sent the change back to Andy for review. There's a better way then what jam@ suggested.

### gi...@appspot.gserviceaccount.com (2022-01-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b13ddd23f2696a1a823ee13794cfdb3102d8e9f7

commit b13ddd23f2696a1a823ee13794cfdb3102d8e9f7
Author: Reilly Grant <reillyg@chromium.org>
Date: Tue Jan 25 20:43:44 2022

Use the origin/name of the main frame in chooser dialogs

Permissions dialogs (for WebUSB, WebHID, and Web Serial) should request
permission for the main origin (the origin embedding the iframe) and not
the site hosting the iframe as per crbug.com/802945. Update the UI code
to accurately display the main origin (or extension name) and add tests.

Bug: 1280233
Change-Id: Ia3bf9274eb49c1d842e204a518635cc1187f3d3d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3353956
Reviewed-by: Scott Violet <sky@chromium.org>
Reviewed-by: Andy Paicu <andypaicu@chromium.org>
Commit-Queue: Reilly Grant <reillyg@chromium.org>
Cr-Commit-Position: refs/heads/main@{#963184}

[add] https://crrev.com/b13ddd23f2696a1a823ee13794cfdb3102d8e9f7/chrome/browser/chooser_controller/title_util_unittest.cc
[modify] https://crrev.com/b13ddd23f2696a1a823ee13794cfdb3102d8e9f7/components/permissions/chooser_title_util.cc
[modify] https://crrev.com/b13ddd23f2696a1a823ee13794cfdb3102d8e9f7/components/permissions/chooser_title_util.h
[modify] https://crrev.com/b13ddd23f2696a1a823ee13794cfdb3102d8e9f7/chrome/browser/chooser_controller/title_util.h
[modify] https://crrev.com/b13ddd23f2696a1a823ee13794cfdb3102d8e9f7/components/permissions/BUILD.gn
[add] https://crrev.com/b13ddd23f2696a1a823ee13794cfdb3102d8e9f7/components/permissions/chooser_title_util_unittest.cc
[modify] https://crrev.com/b13ddd23f2696a1a823ee13794cfdb3102d8e9f7/chrome/test/BUILD.gn
[modify] https://crrev.com/b13ddd23f2696a1a823ee13794cfdb3102d8e9f7/chrome/browser/chooser_controller/title_util.cc


### re...@chromium.org (2022-01-25)

[Empty comment from Monorail migration]

### re...@chromium.org (2022-01-26)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-26)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-26)

Dear owner, thanks for fixing this bug. We’ve reopened it because security bugs need Security_Severity and FoundIn labels set, which will enable the bots to request merges to the correct branches ( as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact (security@chromium.org) to arrange to set these labels and then this bug can be marked closed again. Thank you! Severity guidelines: https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues FoundIn guidelines: https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security Thanks for your time! 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aj...@google.com (2022-01-26)

Setting some labels and remarking as Fixed.

Medium as this is a limited origin spoof.
FoundIn-96 based on report.

### re...@chromium.org (2022-01-26)

Assigning this medium severity because this isn't origin spoofing in the Omnibox but allows a site to tamper with trusted security UX.

### [Deleted User] (2022-01-26)

Dear owner, thanks for fixing this bug. We’ve reopened it because security bugs need Security_Severity and FoundIn labels set, which will enable the bots to request merges to the correct branches ( as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact (security@chromium.org) to arrange to set these labels and then this bug can be marked closed again. Thank you! Severity guidelines: https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues FoundIn guidelines: https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security Thanks for your time! 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-26)

[Empty comment from Monorail migration]

### re...@chromium.org (2022-01-26)

Bad bot. This issue already has Security_Severity and FoundIn labels set.

### bu...@gmail.com (2022-01-27)

Thank you Reilly,

Regards,
Abdulla Aldoseri

### [Deleted User] (2022-01-27)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-27)

[Empty comment from Monorail migration]

### bu...@gmail.com (2022-02-11)

Dears, 

Is there anyting from my side need to be completed to assign a CVE for this issue?

Regards,
Abdulla Aldoseri

### am...@google.com (2022-02-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-02-11)

Congratulations - the VRP Panel has decided to award you $3,000 for this report. A member of our finance team will be in touch soon to arrange payment. In the meantime, please let us know what name/handle/tag you would like us to use when acknowledging you for this issue. Thank you for reporting this issue to us and nice work! 

### am...@chromium.org (2022-02-11)

adding merge review labels because sheriffbot is sleeping on the job


### am...@chromium.org (2022-02-11)

Hi Abdulla, regarding your question in https://crbug.com/chromium/1280233#c21: no, there is no action needed from you for CVE assignment. A CVE will be allocated on this issue at the time the patch is included in a Stable channel release. It will be updated directly on this issue and published in stable channel release notes and acknowledgements. Thank you. 

### am...@google.com (2022-02-14)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-02-17)

[Comment Deleted]

### am...@chromium.org (2022-02-17)

Merge approved to M99, please merge to branch 4844 at your earliest availability. 
(Deleted above comment with incorrect branch number) 

### pb...@google.com (2022-02-17)

[Bulk update] Your change has been approved for M99 branch please refer to go/chrome-branches for branch info and merge the CL's to M99 branch manually asap so that they would be part of next week's M99 Beta release.

### gi...@appspot.gserviceaccount.com (2022-02-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/8bfb46438804357f5b914ee8bea6de5223a5ca71

commit 8bfb46438804357f5b914ee8bea6de5223a5ca71
Author: Reilly Grant <reillyg@chromium.org>
Date: Fri Feb 18 07:48:33 2022

[Merge M-99] Use the origin/name of the main frame in chooser dialogs

Permissions dialogs (for WebUSB, WebHID, and Web Serial) should request
permission for the main origin (the origin embedding the iframe) and not
the site hosting the iframe as per crbug.com/802945. Update the UI code
to accurately display the main origin (or extension name) and add tests.

(cherry picked from commit b13ddd23f2696a1a823ee13794cfdb3102d8e9f7)

Bug: 1280233
Change-Id: Ia3bf9274eb49c1d842e204a518635cc1187f3d3d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3353956
Reviewed-by: Scott Violet <sky@chromium.org>
Reviewed-by: Andy Paicu <andypaicu@chromium.org>
Commit-Queue: Reilly Grant <reillyg@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#963184}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3472815
Auto-Submit: Reilly Grant <reillyg@chromium.org>
Commit-Queue: Andy Paicu <andypaicu@chromium.org>
Cr-Commit-Position: refs/branch-heads/4844@{#647}
Cr-Branched-From: 007241ce2e6c8e5a7b306cc36c730cd07cd38825-refs/heads/main@{#961656}

[add] https://crrev.com/8bfb46438804357f5b914ee8bea6de5223a5ca71/chrome/browser/chooser_controller/title_util_unittest.cc
[modify] https://crrev.com/8bfb46438804357f5b914ee8bea6de5223a5ca71/components/permissions/chooser_title_util.h
[modify] https://crrev.com/8bfb46438804357f5b914ee8bea6de5223a5ca71/components/permissions/chooser_title_util.cc
[modify] https://crrev.com/8bfb46438804357f5b914ee8bea6de5223a5ca71/chrome/browser/chooser_controller/title_util.h
[modify] https://crrev.com/8bfb46438804357f5b914ee8bea6de5223a5ca71/chrome/test/BUILD.gn
[add] https://crrev.com/8bfb46438804357f5b914ee8bea6de5223a5ca71/components/permissions/chooser_title_util_unittest.cc
[modify] https://crrev.com/8bfb46438804357f5b914ee8bea6de5223a5ca71/components/permissions/BUILD.gn
[modify] https://crrev.com/8bfb46438804357f5b914ee8bea6de5223a5ca71/chrome/browser/chooser_controller/title_util.cc


### am...@chromium.org (2022-02-28)

[Empty comment from Monorail migration]

### am...@google.com (2022-03-01)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-05)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2022-07-21)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-29)

[Empty comment from Monorail migration]

### is...@google.com (2022-07-29)

This issue was migrated from crbug.com/chromium/1280233?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>HID, Blink>Serial, Blink>USB]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058243)*
