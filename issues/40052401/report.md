# Security: UAF in ChromeOS Login

| Field | Value |
|-------|-------|
| **Issue ID** | [40052401](https://issues.chromium.org/issues/40052401) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Enterprise |
| **Platforms** | ChromeOS |
| **Reporter** | le...@gmail.com |
| **Assignee** | fa...@chromium.org |
| **Created** | 2020-05-25 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**

ChallengeResponseAuthKeysLoader uses ScopedObserver[1] to monitor ExtensionHost. When the extension\_host\_observer\_ is released, ExtensionHost::RemoveObserver will be called. ExtensionHost could be released through IPC call[2], and the has\_loaded\_once check[3] also could be bypassed through the renderer-side[4]. So we can destroy ExtensionHost before ChallengeResponseAuthKeysLoader is released, and the UAF will be triggered.

This bug may cause the sandbox escape.

[1]. <https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/chromeos/login/challenge_response_auth_keys_loader.cc;l=323?originalUrl=https:%2F%2Fcs.chromium.org%2F>  

[2]. <https://source.chromium.org/chromium/chromium/src/+/master:extensions/common/extension_messages.h;l=921?originalUrl=https:%2F%2Fcs.chromium.org%2F>  

[3]. <https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/chromeos/login/challenge_response_auth_keys_loader.cc;l=284?originalUrl=https:%2F%2Fcs.chromium.org%2F>  

[4]. <https://source.chromium.org/chromium/chromium/src/+/master:content/renderer/render_frame_impl.cc;l=5441?originalUrl=https:%2F%2Fcs.chromium.org%2F>

**VERSION**  

Chrome Version: stable  

Operating System: ChromeOS only

**REPRODUCTION CASE**

Apply the attached patch, launch the ChromeOS. Lock the screen and click the "start" ("->") button. The rotating animation is shown for a few seconds and the UAF will be triggered. (May require multiple clicks to trigger)

The browser-side patch aims to emulate a login screen extension, it will not affect the vulnerability.  

The renderer-side patch emulates a compromised renderer.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: browser  

Crash State: the attached asan file  

**Client ID (if relevant): [see link above]**

**CREDIT INFORMATION**  

Reporter credit: Leecraso and Guang Gong of 360 Alpha Lab working with 360 BugCloud(<https://bugcloud.360.cn/>)

## Attachments

- [poc.patch](attachments/poc.patch) (text/plain, 3.4 KB)
- [asan](attachments/asan) (text/plain, 22.1 KB)
- [ui.patch](attachments/ui.patch) (text/plain, 1.6 KB)

## Timeline

### le...@gmail.com (2020-05-25)

Also the patch to emulate the challenge-response authentication support for the user, sorry for missing it.

### ke...@chromium.org (2020-05-25)

[Empty comment from Monorail migration]

### ra...@chromium.org (2020-05-25)

fabiansommer/emaxx: could you ptal a look at this? From an initial scan it seems that the issue may have been introduced in https://chromium-review.googlesource.com/c/chromium/src/+/2078584

Marking this as Medium severity as I think there are several mitigating factors:
1) The screen has to be locked to trigger this
2) It appears that this unlock flow is only used for challenge-response authentication where extensions need to be loaded (e.g. smart card authentication) - emaxx, correct me if I'm wrong
3) It appears to require a compromised renderer

[Monorail components: UI>Shell>LockScreen]

### ra...@chromium.org (2020-05-25)

Also I marked this as stable impact. The offending code is M82. It's possible the code hasn't actually made it to stable yet but it probably would be soon (in the M83 release)

### em...@chromium.org (2020-05-26)

Thanks for the report.

IIUC, this bug only affects the enterprise-enrolled devices that have smart card related device policies configured, since otherwise we'll exit early at https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/chromeos/login/challenge_response_auth_keys_loader.cc;l=256;drc=ad179764079ae4594fcae8808af45489b9ce092e?originalUrl=https:%2F%2Fcs.chromium.org%2F (even if the attacker found a way to hit this code, which would require emulating a client-certificate based SAML user authentication).

[Monorail components: Enterprise]

### em...@chromium.org (2020-05-26)

Unless I'm missing something, a quick fix would be to observe OnExtensionHostDestroyed() and unsubscribe from the ExtensionHost before it gets deleted.

### ra...@chromium.org (2020-05-26)

[Empty comment from Monorail migration]

### [Deleted User] (2020-05-26)

[Empty comment from Monorail migration]

### ra...@chromium.org (2020-05-26)

Thanks for getting on to this quickly!

### em...@chromium.org (2020-05-26)

fabiansommer@ is working on the CL: https://crrev.com/c/2215056.

### em...@chromium.org (2020-05-28)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-05-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/71a7eb5a6bcca1b60b32c23892e3518cfc0555af

commit 71a7eb5a6bcca1b60b32c23892e3518cfc0555af
Author: Fabian Sommer <fabiansommer@chromium.org>
Date: Fri May 29 00:56:55 2020

Fix observers in ChallengeResponseAuthKeysLoader

Stop observing with scoped observers when the observed objects are
destroyed.

Fixed: 1086124
Change-Id: Ib0aa9e6eb3dc346a441ecdd0416649622ff03f17
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2215056
Reviewed-by: Maksim Ivanov <emaxx@chromium.org>
Reviewed-by: Denis Kuznetsov [CET] <antrim@chromium.org>
Commit-Queue: Maksim Ivanov <emaxx@chromium.org>
Cr-Commit-Position: refs/heads/master@{#772977}

[modify] https://crrev.com/71a7eb5a6bcca1b60b32c23892e3518cfc0555af/chrome/browser/chromeos/login/challenge_response_auth_keys_loader.cc
[modify] https://crrev.com/71a7eb5a6bcca1b60b32c23892e3518cfc0555af/chrome/browser/chromeos/login/challenge_response_auth_keys_loader_browsertest.cc


### [Deleted User] (2020-05-29)

[Empty comment from Monorail migration]

### na...@google.com (2020-06-01)

[Empty comment from Monorail migration]

### [Deleted User] (2020-06-01)

Requesting merge to beta M84 because latest trunk commit (772977) appears to be after beta branch point (768962).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-06-01)

This bug requires manual review: M84's targeted beta branch promotion date has already passed, so this requires manual review
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: govind@(Android), bindusuvarna@(iOS), marinakz@(ChromeOS), pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### le...@gmail.com (2020-06-03)

Thanks for the quick fix! But i think the mentioned two mitigation in https://crbug.com/chromium/1086124#c2 is just a normal login method for those user.  :p

### jo...@chromium.org (2020-06-05)

I would certainly merge this high-severity bug fix into M84.

### fa...@chromium.org (2020-06-05)

Responding to https://crbug.com/chromium/1086124#c16:
> 1. Does your merge fit within the Merge Decision Guidelines?
Yes
> 2. Links to the CLs you are requesting to merge.
https://chromium.googlesource.com/chromium/src.git/+/71a7eb5a6bcca1b60b32c23892e3518cfc0555af
> 3. Has the change landed and been verified on master/ToT?
Yes
> 4. Why are these changes required in this milestone after branch?
Fix for a security vulnerability
> 5. Is this a new feature?
No
> 6. If it is a new feature, is it behind a flag using finch?
N/A

Responding to https://crbug.com/chromium/1086124#c17: This is indeed the normal login method for those users. However, since it only just launched in M83, not many users use it (so far).

### ci...@chromium.org (2020-06-08)

Merge approved, M83.

### ci...@chromium.org (2020-06-08)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-06-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/50106ee7d84d433fefc2ed2df4b39bcee6ac1925

commit 50106ee7d84d433fefc2ed2df4b39bcee6ac1925
Author: Fabian Sommer <fabiansommer@chromium.org>
Date: Tue Jun 09 13:28:47 2020

Fix observers in ChallengeResponseAuthKeysLoader

This is a merge of commit 71a7eb5a6bcca1b60b32c23892e3518cfc0555af
into the release branch.

Original commit message:
> Fix observers in ChallengeResponseAuthKeysLoader
>
> Stop observing with scoped observers when the observed objects are
> destroyed.
>
> Fixed: 1086124
> Change-Id: Ib0aa9e6eb3dc346a441ecdd0416649622ff03f17
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2215056
> Reviewed-by: Maksim Ivanov <emaxx@chromium.org>
> Reviewed-by: Denis Kuznetsov [CET] <antrim@chromium.org>
> Commit-Queue: Maksim Ivanov <emaxx@chromium.org>
> Cr-Commit-Position: refs/heads/master@{#772977}
(cherry picked from commit 71a7eb5a6bcca1b60b32c23892e3518cfc0555af)

Bug: 1086124
Change-Id: I2c1647934e7cea29b406c6bbdee61984967f6e49
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2235846
Reviewed-by: Maksim Ivanov <emaxx@chromium.org>
Commit-Queue: Maksim Ivanov <emaxx@chromium.org>
Cr-Commit-Position: refs/branch-heads/4103@{#674}
Cr-Branched-From: 8ad47e8d21f6866e4a37f47d83a860d41debf514-refs/heads/master@{#756066}

[modify] https://crrev.com/50106ee7d84d433fefc2ed2df4b39bcee6ac1925/chrome/browser/chromeos/login/challenge_response_auth_keys_loader.cc
[modify] https://crrev.com/50106ee7d84d433fefc2ed2df4b39bcee6ac1925/chrome/browser/chromeos/login/challenge_response_auth_keys_loader_browsertest.cc


### ad...@google.com (2020-06-12)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-06-12)

[Empty comment from Monorail migration]

### ma...@google.com (2020-06-15)

M84 Merge approved

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-06-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/b56268c7d758ef860fdfa36729ee0c26f78d00a8

commit b56268c7d758ef860fdfa36729ee0c26f78d00a8
Author: Fabian Sommer <fabiansommer@chromium.org>
Date: Tue Jun 16 12:16:04 2020

Fix observers in ChallengeResponseAuthKeysLoader

This is a merge of commit 71a7eb5a6bcca1b60b32c23892e3518cfc0555af
into M84 beta.

Original commit message:
> Fix observers in ChallengeResponseAuthKeysLoader
>
> Stop observing with scoped observers when the observed objects are
> destroyed.
>
> Fixed: 1086124
> Change-Id: Ib0aa9e6eb3dc346a441ecdd0416649622ff03f17
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2215056
> Reviewed-by: Maksim Ivanov <emaxx@chromium.org>
> Reviewed-by: Denis Kuznetsov [CET] <antrim@chromium.org>
> Commit-Queue: Maksim Ivanov <emaxx@chromium.org>
> Cr-Commit-Position: refs/heads/master@{#772977}
(cherry picked from commit 71a7eb5a6bcca1b60b32c23892e3518cfc0555af)

Change-Id: I0d78af75ebc736bd0a805bc4eb4daa19d130a180
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2246150
Commit-Queue: Maksim Ivanov <emaxx@chromium.org>
Reviewed-by: Maksim Ivanov <emaxx@chromium.org>
Cr-Commit-Position: refs/branch-heads/4147@{#658}
Cr-Branched-From: 16307825352720ae04d898f37efa5449ad68b606-refs/heads/master@{#768962}

[modify] https://crrev.com/b56268c7d758ef860fdfa36729ee0c26f78d00a8/chrome/browser/chromeos/login/challenge_response_auth_keys_loader.cc
[modify] https://crrev.com/b56268c7d758ef860fdfa36729ee0c26f78d00a8/chrome/browser/chromeos/login/challenge_response_auth_keys_loader_browsertest.cc


### ad...@google.com (2020-07-23)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-07-23)

Congratulations! The VRP panel has decided to award $5000 for this bug. Thanks for the report.

### ad...@google.com (2020-07-23)

[Empty comment from Monorail migration]

### [Deleted User] (2020-09-04)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2021-01-14)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1086124?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Enterprise, UI>Shell>LockScreen]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40052401)*
