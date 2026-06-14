# Security: FedCM prompt bubble can be obscured by Video/Document PiP window, allow for hidden login

| Field | Value |
|-------|-------|
| **Issue ID** | [339654392](https://issues.chromium.org/issues/339654392) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Identity>FedCM |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | al...@alesandroortiz.com |
| **Assignee** | cb...@chromium.org |
| **Created** | 2024-05-10 |
| **Bounty** | $2,000.00 |

## Description

#### SUMMARY

The FedCM prompt does not have input protections if the associated window is visible, allowing for hidden login if the prompt is obscured by a Video or Document PiP window.

Showing the FedCM prompt does not require user interaction.   

A compromised renderer can open popups without user interaction, so the PoCs dependent on popups can be performed with minimal user interaction.

The FedCM prompt has two dialog types [1]: bubble and modal. I've only verified this so far with the bubble dialog, but it may also work with the modal dialog (will provide update in comment).

[1] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/webid/fedcm_account_selection_view_desktop.h;l=52;drc=6f3f85b321146cfc0f9eb81a74c7c2257821461e>

#### VULNERABILITY DETAILS

The FedCM prompt will remain visible and interactive as long as the invoking page is partially visible.

A page can show a Video or Document PiP window over a normal window with a FedCM prompt to obscure the prompt.

An attacker can instruct the user to press keys while the FedCM prompt is obscured, resulting in login without user awareness.

POTENTIAL SOLUTION

In the FedCM dialog, implement same input protections as permission prompt buttons. Permission prompt buttons are not interactive if they are fully obscured, even if the associated window is partially visible.

#### VERSION

Chrome Version: 126.0.6469.0 Canary, 124.0.6367.119 Stable.

Operating System: Windows 10 Version 22H2 (Build 19045.4170)

#### BISECT

This reproduces in versions prior to FedCM being enabled by default, so it likely reproduces from the very early working implementations of FedCM.

Verified repro down to 105.0.5169.0 (commit 021475c2d0fb9d12a99148ad73a26c6bdbf06c92) with current PoCs.

FedCM is enabled by default starting with M108: <https://caniuse.com/mdn-api_identitycredential>

Between 105 and 108, behavior repros with FedCM flag enabled. Versions prior to 105.0.5169.0 need modified PoCs, since the API changed a couple of times before reaching Stable.

#### REPRODUCTION CASE

Setup:

1. Run a simulated IDP server: `node server-single-account.js` (attached)

In real scenarios, an attacker would use a legit IDP since they would want real credentials.

##### Scenario 1a: Document PiP (using large PiP window)

Note: By itself, this can obscure *most* of the FedCM prompt in a maximized window since Document PiP windows are limited to 80% of screen width/height.
However, when chained with other PiP issues the prompt can be fully covered.

1. Navigate to <https://alesandroortiz.com/security/chromium/fedcm-documentpip.html>
2. Press any key twice
3. Press tab twice, then press enter (then wait a few seconds for login to complete)

##### Scenario 1b: Document PiP (using popup)

1. Navigate to <https://alesandroortiz.com/security/chromium/fedcm-documentpip.html?mode=popup>
2. Hold enter key (or press any key three times)
3. Press tab twice, then press enter (then wait a few seconds for login to complete)

##### Scenario 2: Video PiP

1. Navigate to <https://alesandroortiz.com/security/chromium/fedcm-videopip.html>
2. Press any key twice
3. Press tab twice, then press enter (then wait a few seconds for login to complete)

For all scenarios:

Observed: FedCM bubble remains open under PiP window. User is able to interact with bubble. Attacker is able to obtain login token without user awareness.

Expected: FedCM bubble closes or is not interactive when under a PiP window. Attacker cannot obtain login token without user awareness.

#### CREDIT INFORMATION

Reporter credit: Alesandro Ortiz <https://AlesandroOrtiz.com>

## Attachments

- fedcm-documentpip.html (text/html, 3.1 KB)
- [fedcm-videopip.html](attachments/fedcm-videopip.html) (text/html, 3.0 KB)
- [fedcm-pip-login.mp4](attachments/fedcm-pip-login.mp4) (video/mp4, 11.7 MB)
- [server-single-account.js](attachments/server-single-account.js) (text/javascript, 2.3 KB)
- fedcm-videopip.html (text/html, 2.9 KB)
- [pip-hello-world.webm](attachments/pip-hello-world.webm) (video/webm, 11.7 KB)
- [pip-permission-chromeos.html](attachments/pip-permission-chromeos.html) (text/html, 850 B)
- [permission-ui-obscured-by-pip-window.mov](attachments/permission-ui-obscured-by-pip-window.mov) (video/quicktime, 3.3 MB)
- [fedcm-documentpip-modal.html](attachments/fedcm-documentpip-modal.html) (text/html, 1.6 KB)
- [fedcm-documentpip-modal-popup.html](attachments/fedcm-documentpip-modal-popup.html) (text/html, 1.1 KB)
- [fedcm-documentpip-modal.mp4](attachments/fedcm-documentpip-modal.mp4) (video/mp4, 7.6 MB)

## Timeline

### al...@alesandroortiz.com (2024-05-10)

Forgot to attach simulated IDP.

### al...@alesandroortiz.com (2024-05-10)

Also verified repro with the modal dialog. Will provide PoC for modal dialog within a day or so.

### ad...@google.com (2024-05-10)

I can reproduce this using 124.0.6367.0 for the "using large PiP window" and "using popup" workflows. The video pip doesn't quite work for me possibly because I am missing blank.html, but anyway that's more than enough for me to consider this a valid bug and pass it on. Thanks for the very clear report and ready reproduction steps.

Severity:
I'm not sure how severe we'd consider it to perform the authentication without user awareness, but it seems reasonably serious to me, about as serious as a permission prompt bypass would be. It's hard, but not impossible, to imagine users being coerced to press the keystrokes required to interact with the hidden dialogs. I would regard this as S2 or S3 - I'm going to err on the side of caution and call it S2 because perhaps there are easier sets of keystrokes or similar.

FoundIn: I agree this likely dates back to FedCM introduction.

### ad...@google.com (2024-05-10)

<https://crrev.com/7fc7c1c24a54c99fad89fadcbbbdcc8f9efda79e> suggests yigu@ has been working in this area - perhaps you can pass this on in the right direction even if you're not the right person to fix it? Thanks.

### al...@alesandroortiz.com (2024-05-10)

Thanks for triage. Agreed it's similar to permission prompt bypass, since FedCM is browser UI (despite its in-page location and different appearance).

Because it's browser UI, it's possible (and responsible) to give it similar protections as other browser UI.

> The video pip doesn't quite work for me possibly because I am missing blank.html

Sorry, forgot to mention in report to create an empty `blank.html` (or update the PoC to open any same-origin URL). This is needed because the Document PiP window won't open on `about:blank` pages even if same-origin. However, this isn't needed for the Video PiP PoC, so I'll provide updated PoC soon.

### pe...@google.com (2024-05-10)

Setting milestone because of s2 severity.

### pe...@google.com (2024-05-10)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### al...@alesandroortiz.com (2024-05-10)

Updated Video PiP PoC attached (only changes `blank.html` to `about:blank` and removes `load` event listener). Hosted PoC was also updated.

### al...@alesandroortiz.com (2024-05-10)

Also attached video file for Video PiP PoC.

### yi...@chromium.org (2024-05-13)

Thank you Alesandro Ortiz for reporting this bug. I'm wondering whether this would affect other browser UIs. e.g. on https://permission.site, one can use keyboard to open a permission prompt asking for camera access. Would users be tricked to grant those permissions with the same PiP thing?

### al...@alesandroortiz.com (2024-05-13)

No\* because permission prompts implement input protection that prevents buttons from being used if partially or fully obscured by certain UIs, including Video and Document PiP windows.

IIRC there are other open issues to implement this protection for other sensitive UIs.

This protection was implemented for permission prompts in this May 2023 commit: <https://chromium.googlesource.com/chromium/src/+/073278eae6d6ce07cc40107567907e545ec56157>

The protection above is what I referred to in the report's `POTENTIAL SOLUTION` section.

\*I recently found some bypasses: [issue 338634231](https://issues.chromium.org/issues/338634231), [issue 339818327](https://issues.chromium.org/issues/339818327)

### al...@alesandroortiz.com (2024-05-13)

Current implementation of permission prompt protections uses `PictureInPictureOcclusionTracker`.

<https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/permissions/permission_prompt_base_view.cc;l=71;drc=41d53a863ef269e6d53fea38cc1d3feda6c3df78>

<https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/picture_in_picture/picture_in_picture_occlusion_tracker.h;l=18;drc=41d53a863ef269e6d53fea38cc1d3feda6c3df78>

### yi...@chromium.org (2024-05-13)

Interesting. I can use keyboard to navigate to the Camera Permission UI and interact with it while it's completely occluded by Google Meet PiP window.

### al...@alesandroortiz.com (2024-05-13)

Hm, I'm unable to repro this on Stable nor Canary on Windows 10 using my own PoC.

Which OS are you using? Might be an OS-specific bug that might affect other protections too.

### yi...@chromium.org (2024-05-14)

I'm on Mac which does have its own rules w.r.t. navigating through browser native UIs

### yi...@chromium.org (2024-05-14)

Just tested on ChromeOS and the navigation could go into the Camera Permission UI as well.

### al...@alesandroortiz.com (2024-05-14)

Thanks for testing. I have a ChromeOS device and ~~verified there last night too~~ (see [#comment20](https://issues.chromium.org/issues/339654392#comment20)). Will need to test Linux VM soon.

Is it okay if I file new security report for those bypasses? I'll need to check my backlog of open reports, but I don't think I have one open for this.

### yi...@chromium.org (2024-05-14)

Yeah I think it makes sense to fix the OcclusionTracker issue in general. Also, as mentioned in [1], autofill seems to check PiP occlusion in a different way.

[1] https://issues.chromium.org/u/1/issues/339481295#comment8

### al...@alesandroortiz.com (2024-05-14)

Re: the permission prompt issue (not the FedCM prompt)

Hm, my ChromeOS device actually hadn't updated (I thought it had, but must have failed) so it was still running a *very* old version. On actually-updated 124.0.6367.154 Stable, Platform 15823.51.0 snappy, I'm not able to repro with either my PoC or with Google Meet.

Also unable to repro on Ubuntu 22.04 LTS on Stable.

Are you on a different version, or maybe an experiment is affecting the behavior on your devices?

Are you using the Google Meet app or website? I tested with the Google Meet website. Maybe the app behaves differently.

### yi...@chromium.org (2024-05-14)

I'm using the Google Meet website with Chrome Stable ver. M125.

The permission prompt issue was supposed to be fixed in https://issues.chromium.org/u/1/issues/40061953. I can ping that bug with a screen recording.

### al...@alesandroortiz.com (2024-05-14)

That other bug is public, so don't post any reproducing issues there.

I'll test once again with ChromeOS on Beta channel. If I'm unable to repro on Beta, I'll let you know so you can make a new report.

Might be something on Beta since M125 hasn't hit stable yet per <https://chromiumdash.appspot.com/releases>

### al...@alesandroortiz.com (2024-05-14)

Still unable to repro the permission prompt issue on ChromeOS 125.0.622.31 Beta.

My repro steps are:

1. Open <https://aogarantiza.com/chromium/pip-permission-chromeos.html> (with buttons somewhat visible so we can see what's happening)
2. Press any key twice
3. Press tab three times to select "Allow", then press enter (or click on any visible button in the permission prompt)
   Also does not work if fully obscured, since permission prompt is hidden in those cases.

Similarly, with Google Meet:

1. Start Meet meeting and open PiP window
2. Open new tab, go to <https://permission.site>
3. Resize window so it's mostly behind the PiP window
4. Using keyboard, select the "Camera" button and press enter (or click the "Camera" button)
5. Press tab three times to select "Allow", then press enter (or click on any visible button in the permission prompt)

If I'm doing roughly the same repro steps as you, then you can submit a report since I am unable to repro. If there's something I should do differently, I'll try it and report if I can finally repro.

### al...@alesandroortiz.com (2024-05-14)

Attached source of my PoC

### yi...@chromium.org (2024-05-14)

It's interesting that even though the UI is displayed and I can use keyboard to navigate through the buttons, the only thing that works is triggering the "X" button. i.e. pressing "enter" or "space" on other buttons don't do anything. See screenshots.

### yi...@chromium.org (2024-05-14)

I think what we are seeing is the same, the UI can show up but the meaningful buttons are not clickable.
I was expecting that the UI doesn't show up at all but on second thought it may be better to show without allowing button clicks.

### al...@alesandroortiz.com (2024-05-14)

Yeah, it's WAI if the buttons are visible or focusable, but it would be a problem if they can be actually pressed to allow the permission. Thanks for the video and clarification!

### al...@alesandroortiz.com (2024-05-16)

Following up on [#comment3](https://issues.chromium.org/issues/339654392#comment3):

Modal dialog PoC, verified on 126.0.6478.8 Canary. I can file separate bug if the fix is different than for the bubble dialog.

Setup:

1. Run a simulated IDP server: `node server-single-account.js` (attached in [#comment2](https://issues.chromium.org/issues/339654392#comment2))   
   
   In real scenarios, an attacker would use a legit IDP since they would want real credentials.
2. If running locally and don't want to use my origin's OT token, enable chrome://flags/#fedcm-button-mode

Repro steps:

1. Navigate to <https://alesandroortiz.com/security/chromium/fedcm-documentpip-modal.html>
2. Hold any key (or press enter three times)
3. Press tab twice, then press enter

To see the modal slightly behind the PiP window, without affecting the repro, use `?debug=1` param.

### pe...@google.com (2024-05-29)

yigu: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### pe...@google.com (2024-06-14)

tanzachary: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### al...@alesandroortiz.com (2024-07-17)

This still repros on 128.0.6601.0 Canary.

### cb...@chromium.org (2024-07-17)

Hi Tommy, it seems you are familiar with PiP. Could you take a look at this bug? It seems like the PiP window is showing on top of another window but does not take focus.

### cb...@chromium.org (2024-07-18)

OK I have found <https://chromium-review.googlesource.com/c/chromium/src/+/5115431>. Seems fairly straightforward to add similar code to FedCM.

<https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/permissions/permission_prompt_bubble.cc;l=69;bpv=1;bpt=0> is possibly also interesting

### al...@alesandroortiz.com (2024-07-18)

Using `PictureInPictureOcclusionTracker` [1] is probably the best way. The stated goal [2] is to move most/all of the existing patchwork of PiP overlap checks to use that class. The class takes care of additional scenarios that may not be handled with other existing checks.

[1] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/picture_in_picture/picture_in_picture_occlusion_tracker.h>

[2] See <https://issues.chromium.org/issues/338634231#comment9> and the preceding comment for context

### cb...@chromium.org (2024-07-18)

Yes thanks -- the change I linked does use PictureInPictureOcclusionTracker

### ap...@google.com (2024-07-22)

Project: chromium/src
Branch: main

commit 19fac6ad5022592ff9b4a438a3e5fc128c0deee0
Author: Christian Biesinger <cbiesinger@chromium.org>
Date:   Mon Jul 22 20:51:30 2024

    [FedCM] Disable the FedCM dialog when occluded
    
    Bug: 339654392
    Change-Id: I97c105276c4442d80b9f506d0ae111aa13837f31
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5721458
    Reviewed-by: Yi Gu <yigu@chromium.org>
    Commit-Queue: Christian Biesinger <cbiesinger@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1331313}

M       chrome/browser/ui/views/webid/account_selection_bubble_view.cc
M       chrome/browser/ui/views/webid/account_selection_modal_view.cc
M       chrome/browser/ui/views/webid/account_selection_view_base.cc
M       chrome/browser/ui/views/webid/account_selection_view_base.h
M       chrome/browser/ui/views/webid/fedcm_account_selection_view_desktop.cc
M       chrome/browser/ui/views/webid/fedcm_account_selection_view_desktop_browsertest.cc

https://chromium-review.googlesource.com/5721458


### cb...@chromium.org (2024-07-23)

Fixed in 128.0.6613.0

Alesandro, if you could test this in Canary I would appreciate that!

### al...@alesandroortiz.com (2024-07-23)

Thanks for fixing, Christian!

Verified as fixed in 128.0.6613.0 Canary on Windows 10 for both bubble and modal dialogs, using these PoCs:

- <https://alesandroortiz.com/security/chromium/fedcm-documentpip.html>
- <https://alesandroortiz.com/security/chromium/fedcm-documentpip.html?mode=popup>
- <https://alesandroortiz.com/security/chromium/fedcm-videopip.html>
- <https://alesandroortiz.com/security/chromium/fedcm-documentpip-modal.html>

Also verified that dialogs remain protected after manually moving PiP window.

### cb...@chromium.org (2024-07-23)

Thank you!

### sp...@google.com (2024-07-31)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
report of lower impact user information disclosure 


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-07-31)

Congratulations Alesandro! Thank you for your efforts and reporting this issue to us.

### al...@alesandroortiz.com (2024-08-01)

Thanks for the reward!

I'm assuming $1k base reward + $1k bisect bonus. (No need to reply if this is correct.)

### am...@chromium.org (2024-08-02)

Hi Alesandro, thanks for the question -- the reward amount was $2,000 for the report, which is why a breakdown was not provided.
While we appreciate all the information you provided in the `bisect` section, ultimately there was not commit provided that introduced this issue.
We specifically bonus the commit, not only to understand how back this issue has existed and what impacted release channels are impacted by the issue, but also to understand what code change introduced the regression and also the engineer, which makes owner assignment much more efficient during triage.
As you can see here, this issue bounced around a little bit before it was resolved. :)

### al...@alesandroortiz.com (2024-08-22)

Thanks for the clarification on bisect bonus. I'll keep that in mind for the future. :)

### pe...@google.com (2024-09-10)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### rz...@google.com (2024-09-12)

Labelling as not applicable for LTS 120, the changed code isn't present in 6099 branch.

### pe...@google.com (2024-09-12)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### rz...@google.com (2024-09-12)

1. <https://crrev.com/c/5849128>
2. Low, no conflicts
3. 128
4. Yes

### ap...@google.com (2024-09-13)

Project: chromium/src
Branch: refs/branch-heads/6478

commit 6d20b6f0d7f25757db3def797ce203ffe65bec65
Author: Gyuyoung Kim <qkim@google.com>
Date:   Fri Sep 13 13:55:20 2024

    [M126-LTS][FedCM] Disable the FedCM dialog when occluded
    
    (cherry picked from commit 19fac6ad5022592ff9b4a438a3e5fc128c0deee0)
    
    Bug: 339654392
    Change-Id: I97c105276c4442d80b9f506d0ae111aa13837f31
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5721458
    Reviewed-by: Yi Gu <yigu@chromium.org>
    Commit-Queue: Christian Biesinger <cbiesinger@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1331313}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5849128
    Reviewed-by: Christian Biesinger <cbiesinger@chromium.org>
    Owners-Override: Artem Sumaneev <asumaneev@google.com>
    Commit-Queue: Gyuyoung Kim (xWF) <qkim@google.com>
    Reviewed-by: Artem Sumaneev <asumaneev@google.com>
    Cr-Commit-Position: refs/branch-heads/6478@{#1961}
    Cr-Branched-From: e6143acc03189c5e52959545b110d6d17ecd5286-refs/heads/main@{#1300313}

M       chrome/browser/ui/views/webid/account_selection_bubble_view.cc
M       chrome/browser/ui/views/webid/account_selection_modal_view.cc
M       chrome/browser/ui/views/webid/account_selection_view_base.cc
M       chrome/browser/ui/views/webid/account_selection_view_base.h
M       chrome/browser/ui/views/webid/fedcm_account_selection_view_desktop.cc
M       chrome/browser/ui/views/webid/fedcm_account_selection_view_desktop_browsertest.cc

https://chromium-review.googlesource.com/5849128


### ap...@google.com (2024-09-17)

Project: chromium/src
Branch: refs/branch-heads/6478_182

commit 4ee87c3e73859fa058a276bd4594a89be5c12069
Author: Gyuyoung Kim <qkim@google.com>
Date:   Tue Sep 17 15:39:25 2024

    [CfM-R126][FedCM] Disable the FedCM dialog when occluded
    
    (cherry picked from commit 19fac6ad5022592ff9b4a438a3e5fc128c0deee0)
    
    (cherry picked from commit 6d20b6f0d7f25757db3def797ce203ffe65bec65)
    
    Bug: 339654392
    Change-Id: I97c105276c4442d80b9f506d0ae111aa13837f31
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5721458
    Reviewed-by: Yi Gu <yigu@chromium.org>
    Commit-Queue: Christian Biesinger <cbiesinger@chromium.org>
    Cr-Original-Original-Commit-Position: refs/heads/main@{#1331313}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5849128
    Reviewed-by: Christian Biesinger <cbiesinger@chromium.org>
    Owners-Override: Artem Sumaneev <asumaneev@google.com>
    Commit-Queue: Gyuyoung Kim (xWF) <qkim@google.com>
    Reviewed-by: Artem Sumaneev <asumaneev@google.com>
    Cr-Original-Commit-Position: refs/branch-heads/6478@{#1961}
    Cr-Original-Branched-From: e6143acc03189c5e52959545b110d6d17ecd5286-refs/heads/main@{#1300313}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5869443
    Owners-Override: Kyle Williams <kdgwill@chromium.org>
    Reviewed-by: Niko Tsirakis <ntsirakis@google.com>
    Commit-Queue: Kyle Williams <kdgwill@chromium.org>
    Cr-Commit-Position: refs/branch-heads/6478_182@{#77}
    Cr-Branched-From: 5b5d8292ddf182f8b2096fa665b473b6317906d5-refs/branch-heads/6478@{#1776}
    Cr-Branched-From: e6143acc03189c5e52959545b110d6d17ecd5286-refs/heads/main@{#1300313}

M       chrome/browser/ui/views/webid/account_selection_bubble_view.cc
M       chrome/browser/ui/views/webid/account_selection_modal_view.cc
M       chrome/browser/ui/views/webid/account_selection_view_base.cc
M       chrome/browser/ui/views/webid/account_selection_view_base.h
M       chrome/browser/ui/views/webid/fedcm_account_selection_view_desktop.cc
M       chrome/browser/ui/views/webid/fedcm_account_selection_view_desktop_browsertest.cc

https://chromium-review.googlesource.com/5869443


### pe...@google.com (2024-10-30)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/339654392)*
