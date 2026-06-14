# Security: Autofill prompt can be obscured by FedCM bubble dialog

| Field | Value |
|-------|-------|
| **Issue ID** | [339481295](https://issues.chromium.org/issues/339481295) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Identity>FedCM |
| **Platforms** | Windows |
| **Reporter** | al...@alesandroortiz.com |
| **Assignee** | yi...@chromium.org |
| **Created** | 2024-05-09 |
| **Bounty** | $3,000.00 |

## Description

#### SUMMARY

The FedCM prompt has two dialog types [1]: bubble and modal. The bubble dialog renders near the top-right of the page while keeping the page interactive.

By opening the autofill prompt before the FedCM bubble, the autofill prompt will render below the FedCM bubble. The page can refocus the input field after the FedCM bubble opens, therefore the autofill prompt is interactive via keyboard.

Showing the FedCM prompt does not require user interaction.   

A compromised renderer can also open the autofill prompt and select the first item, reducing the user interaction to a single key press (enter key).

[1] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/webid/fedcm_account_selection_view_desktop.h;l=52;drc=6f3f85b321146cfc0f9eb81a74c7c2257821461e>

#### VULNERABILITY DETAILS

FedCM will call `ShowInactive()` [2] when trying to show the FedCM dialog. This keeps focus on the page, which allows the autofill prompt to stay open.

Autofill will close its prompt if the page loses focus, therefore prior to commit `4dba5c15131b39270294039b2a28c909110df621` [3] when the FedCM prompt stole focus, the autofill prompt would close automatically.

Showing the autofill prompt after the FedCM prompt will result in the autofill prompt showing above the FedCM prompt, therefore the issue only occurs if the FedCM prompt does not steal focus from the page.

I still need to test if the FedCM modal dialog is also affected (will provide update in comment).

[2] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/webid/fedcm_account_selection_view_desktop.cc;l=80;drc=7fc7c1c24a54c99fad89fadcbbbdcc8f9efda79e>

[3] <https://chromium.googlesource.com/chromium/src/+/4dba5c15131b39270294039b2a28c909110df621> (`[FedCM] Fix the widget stealing focus issue`)

#### VERSION

Chrome Version: 126.0.6467.2 Canary, 126.0.6452.3 Dev

Does not repro on 124.0.6367.119 Stable or 125.0.6422.41 Beta.

Operating System: Windows 10 Version 22H2 (Build 19045.4170)

#### BISECT

Introduced by commit <https://chromium.googlesource.com/chromium/src/+/4dba5c15131b39270294039b2a28c909110df621> (`[FedCM] Fix the widget stealing focus issue`)

Landed in 126.0.6451.0 about 8 days ago: <https://chromiumdash.appspot.com/commit/4dba5c15131b39270294039b2a28c909110df621>

Verified repro down to r1294453 (first known bad). r1294383 was previous known good.

#### REPRODUCTION CASE

Setup:

1. Run the attacker IDP server: `node server.js` (attached)

In real scenarios, an attacker can either host their own IDPs or use a legit IDP.

Prerequisites:

- Address scenarios: Have at least one address in chrome://settings/addresses
- Credit card scenarios: Have at least one credit card in chrome://settings/payments

##### Scenario 1a: Address, 2 keypresses

1. Navigate to <https://alesandroortiz.com/security/chromium/fedcm-autofill.html>
2. Press down arrow, then press enter

##### Scenario 1b: Credit card, 2 keypresses

1. Navigate to <https://alesandroortiz.com/security/chromium/fedcm-autofill.html?autofill=creditcard>
2. Press down arrow, then press enter

##### Scenario 2a: Address, 3 keypresses

1. Navigate to <https://alesandroortiz.com/security/chromium/fedcm-autofill.html?mode=three>
2. Press down arrow twice, then press enter

##### Scenario 2b: Credit card, 3 keypresses

1. Navigate to <https://alesandroortiz.com/security/chromium/fedcm-autofill.html?mode=three&autofill=creditcard>
2. Press down arrow twice, then press enter

For all scenarios:

Observed: Autofill prompt is interactive under FedCM bubble. Attacker obtains autofill data.

Expected: Autofill prompt is not interactive under FedCM bubble, or autofill prompt is closed if under FedCM bubble. Attacker does not obtain autofill data.

#### CREDIT INFORMATION

Reporter credit: Alesandro Ortiz <https://AlesandroOrtiz.com>

## Attachments

- [server.js](attachments/server.js) (text/javascript, 2.4 KB)
- fedcm-autofill.html (text/html, 4.3 KB)
- [fedcm-autofill.mp4](attachments/fedcm-autofill.mp4) (video/mp4, 2.4 MB)
- [Screenshot 2024-05-14 at 1.36.56 PM.png](attachments/Screenshot 2024-05-14 at 1.36.56 PM.png) (image/png, 223.3 KB)
- [fedcm-glitchdotme.mp4](attachments/fedcm-glitchdotme.mp4) (video/mp4, 947.4 KB)
- [fedcm-behind-address-ui-mac.mov](attachments/fedcm-behind-address-ui-mac.mov) (video/quicktime, 1.3 MB)

## Timeline

### al...@alesandroortiz.com (2024-05-09)

> I still need to test if the FedCM modal dialog is also affected (will provide update in comment).

Tested in 126.0.6467.2 Canary and modal dialog (shown in button mode) steals focus from page, so the issue only occurs with widget mode (bubble).

### ca...@chromium.org (2024-05-09)

Thanks for the report, triaging as medium severity based on previous similar bugs.

### ca...@chromium.org (2024-05-09)

yigu and tanzachary: Looks like this was introduced in crrev.com/c/5499438, can you PTAL (and reassign as appropriate)? Thanks.

### pe...@google.com (2024-05-10)

Setting milestone because of s2 severity.

### pe...@google.com (2024-05-10)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security Impact hotlist or the Severity field, and remove the ReleaseBlock hotlist.

### pe...@google.com (2024-05-10)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### yi...@chromium.org (2024-05-14)

We should probably apply similar protection as autofill does [1] such that the FedCM widget UI isn't shown if there's already another native UI shown on the top-right corner or there's a PictureInPicture window that could occlude the FedCM UI etc. This would also fix issue 339654392.

One thing that needs some extra attention is that we may need to allowlist the native UIs that precede the FedCM UI. e.g. user input sensitive UIs like "Autofill" UI should precede FedCM UI but the UserBypass Bubble which reminds users that the website may not work due to the lack of third-party cookies should NOT.

We can address this issue once https://chromium-review.googlesource.com/c/chromium/src/+/5527555 is landed.

[1] https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/autofill/popup/popup_view_views.cc;l=1110-1132



### al...@alesandroortiz.com (2024-05-14)

Plan in [#comment8](https://issues.chromium.org/issues/339481295#comment8) SGTM.

### yi...@chromium.org (2024-05-14)

It's interesting that the FedCM UI shows under the address UI for me. See screenshot.


### al...@alesandroortiz.com (2024-05-14)

Behavior from [#comment10](https://issues.chromium.org/issues/339481295#comment10) would be a timing issue. The FedCM prompt needs to be shown *after* the autofill prompt, since in this case the latest-opened UI will appear on top of already-opened UI.

### yi...@chromium.org (2024-05-14)

I did trigger the address UI first because otherwise it won't show up if the FedCM UI is present.

### al...@alesandroortiz.com (2024-05-14)

I'm still able to repro on 126.0.6478.0 Canary using same <https://webid-fcm.glitch.me/> page on Windows 10, by clicking input field to open autofill prompt first, then waiting for FedCM prompt to appear.

Does it also not repro with the report's PoC?

Since you're on Mac, that may affect something, but I wouldn't expect it to.

### al...@alesandroortiz.com (2024-05-14)

> otherwise [autofill] won't show up if the FedCM UI is present.

I'm also not able to repro this. If I click the input field even after FedCM prompt appears, then the autofill prompt appears (above the FedCM prompt, of course).

### yi...@chromium.org (2024-05-15)

> If I click the input field even after FedCM prompt appears, then the autofill prompt appears (above the FedCM prompt, of course).
That's interesting. There's a check here [1] so the autofill UI shouldn't show up.

> Since you're on Mac, that may affect something
Yeah, on Mac the FedCM UI appears underneath. See screenshot.

[1] https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/autofill/popup/popup_view_views.cc;l=1110-1132

### al...@alesandroortiz.com (2024-05-15)

Re: checks in [1] from [#comment15](https://issues.chromium.org/issues/339481295#comment15)... This is a bit out of my area of knowledge, but based on comments from prior autofill overlap issues, there almost always were some cross-platform discrepancies that caused some logic to only work in certain OSes. Someone from Views team might know better why those specific checks aren't working consistently across OSes.

At least this is verified in Windows, and I'll test ChromeOS and Linux shortly. If it repros on ChromeOS and Linux, I'll file a separate report for that.

### al...@alesandroortiz.com (2024-05-15)

Interestingly, on ChromeOS autofill also doesn't open if it overlaps with FedCM prompt. Testing Linux shortly.

Maybe someone from Views team might have insights as to why existing checks don't work on Windows but do work on most (all?) other platforms?

### al...@alesandroortiz.com (2024-05-15)

Linux has same behavior as ChromeOS too (autofill prompt doesn't open if overlapping FedCM prompt), so this seems like a Windows-only issue AFAICT.

### am...@chromium.org (2024-05-28)

Hi yigu@ at soonest, please provide an update on this issue. This is a security regression introduced in M126 by <https://crrev.com/c/5499438> and is considered a Stable release blocker for M126. Stable RC for M126 is scheduled to be cut on Tuesday, a week from today, so progress/updates at soonest are greatly appreciated.

### ap...@google.com (2024-05-28)

Project: chromium/src
Branch: main

commit 3184b5fda1b9a6abe1f4667f6eee281cb56bc2ac
Author: Yi Gu <yigu@chromium.org>
Date:   Tue May 28 23:33:49 2024

    [FedCM] Show active widget to take the focus when UI is displayed
    
    This patch reverted https://crrev.com/c/5499438. Starting a new patch
    due to merge conflicts with an auto-revert.
    
    Bug: 41482141, 339481295
    Change-Id: I504489ec22a58521c20561f7ac5c4513b6a195d2
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5578261
    Reviewed-by: Zachary Tan <tanzachary@chromium.org>
    Commit-Queue: Yi Gu <yigu@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1307125}

M       chrome/browser/ui/views/webid/fedcm_account_selection_view_desktop.cc

https://chromium-review.googlesource.com/5578261


### am...@chromium.org (2024-05-29)

Based on an off-bug chat with yigu@, the quickest and safest path to correct the regression for Stable M126 is to revert the change in c#20 that introduced these issues.
There is a document covering collaborative work between FedCM and Autofill to mitigate these types of issues in the future, but that will a lengthier and more complex endeavor.

Thank you for landing the revert. Please feel free to open, yigu@ and please open and link the tracking issue for the longer term mitigation effort with the autofill team once that issue has been opened and documented.
Going to close this issue as Fixed at this time, so we'll need to be sure that work is tracked. Thanks!

### pe...@google.com (2024-05-29)

Merge review required: M126 is already shipping to beta.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), govind (iOS), ceb (ChromeOS), srinivassista (Desktop)

### yi...@chromium.org (2024-05-30)

Please answer the following questions so that we can safely process your merge request:
1. Yes. This fixed a security regression.
2. https://chromium-review.googlesource.com/c/chromium/src/+/5578261
3. Yes
4. No
5. No
6. No

### pg...@google.com (2024-05-30)

sorry - reverting my merge approval to check a few more things at the moment

### pg...@google.com (2024-05-30)

Apologies for the noise! re-adding merge approval

Canary looks good - nothing notable or relevant to the revert that is the fix for this bug. S2, but given its introduction in M126 and the resulting stable release blocker status, merge approved for M126!

Please merge to branch 6478 by EOD tomorrow May 31 to get this fix into the early stable cut for M126 happening early next week!

### ap...@google.com (2024-05-30)

Project: chromium/src
Branch: refs/branch-heads/6478

commit 8a7707d8f85a5b91caf7e8b210ef832d1853fd75
Author: Yi Gu <yigu@chromium.org>
Date:   Thu May 30 19:11:17 2024

    [FedCM] Show active widget to take the focus when UI is displayed
    
    This patch reverted https://crrev.com/c/5499438. Starting a new patch
    due to merge conflicts with an auto-revert.
    
    (cherry picked from commit 3184b5fda1b9a6abe1f4667f6eee281cb56bc2ac)
    
    Bug: 41482141, 339481295
    Change-Id: I504489ec22a58521c20561f7ac5c4513b6a195d2
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5578261
    Reviewed-by: Zachary Tan <tanzachary@chromium.org>
    Commit-Queue: Yi Gu <yigu@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1307125}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5582473
    Cr-Commit-Position: refs/branch-heads/6478@{#879}
    Cr-Branched-From: e6143acc03189c5e52959545b110d6d17ecd5286-refs/heads/main@{#1300313}

M       chrome/browser/ui/views/webid/fedcm_account_selection_view_desktop.cc

https://chromium-review.googlesource.com/5582473


### al...@alesandroortiz.com (2024-05-30)

Verified as fixed on 127.0.6510.0 Canary on Windows 10.

I understand that a proper fix is more complex, as noted in [#comment8](https://issues.chromium.org/issues/339481295#comment8) and [#comment21](https://issues.chromium.org/issues/339481295#comment21), so I'm okay with this mitigation for now. Looking forward to the longer-term fixes.

### sp...@google.com (2024-06-13)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $3000.00 for this report.

Rationale for this decision:
$3,000 for report of security UI spoofing, mitigated by user gesture and dialog


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-06-13)

Congratulations, Alesandro! Thank your for your efforts and reporting this issue to us!

### al...@alesandroortiz.com (2024-06-13)

Thanks for the reward!

### am...@chromium.org (2024-06-13)

Apologies, this should have specified in the bot's update -- this reward amount was $2,000 for the report + $1,000 bisect bonus. Cheers!

### al...@alesandroortiz.com (2024-06-13)

Thanks for clarification! :)

### al...@alesandroortiz.com (2024-07-18)

Hi, [#comment21](https://issues.chromium.org/issues/339481295#comment21) mentioned there would be a follow-up issue for a proper fix. Was this created, and if so, what is the follow-up issue ID (even if restricted) for future reference?

This issue probably needs regression tests, as mentioned in related issue <https://issues.chromium.org/issues/340202281#comment10>

### al...@alesandroortiz.com (2024-09-04)

Hi, was the follow-up issue filed? (See [#comment33](https://issues.chromium.org/issues/339481295#comment33), [#comment21](https://issues.chromium.org/issues/339481295#comment21))

### yi...@chromium.org (2024-09-04)

Hi Alesandro, sorry that I missed comment 33. We opened a restricted issue crbug.com/364652018. 

### al...@alesandroortiz.com (2024-09-04)

Thanks! Will keep an eye out for CLs for that bug.

### pe...@google.com (2024-09-05)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/339481295)*
