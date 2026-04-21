# Security: UAF in WebAppIdentityUpdate

| Field | Value |
|-------|-------|
| **Issue ID** | [40056991](https://issues.chromium.org/issues/40056991) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>WebAppInstalls |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | le...@gmail.com |
| **Assignee** | er...@chromium.org |
| **Created** | 2021-08-24 |
| **Bounty** | $7,000.00 |

## Description

**VULNERABILITY DETAILS**  

When creating the dialog |WebAppIdentityUpdateConfirmationView|[1], the parent window will be bound to |GetTopLevelNativeWindow()|. The window will not close when the WebContents get destroyed. Click the "Uninstall app" button will call the cancel function[2], and UAF will be triggered when |web\_contents\_| get accessed[3].

[1]. <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/web_apps/web_app_identity_update_confirmation_view.cc;l=233;drc=0ce9df69ba9e32bafc53c3d90db8a707c243da40>  

[2]. <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/web_apps/web_app_identity_update_confirmation_view.cc;l=206;drc=0ce9df69ba9e32bafc53c3d90db8a707c243da40>  

[2]. <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/web_apps/web_app_identity_update_confirmation_view.cc;l=208;drc=0ce9df69ba9e32bafc53c3d90db8a707c243da40>

**VERSION**  

Chrome Version: stable  

Operating System: test in Linux and Windows

**REPRODUCTION CASE**

Apply the attached patch.diff \*  

$ python -m SimpleHTTPServer  

$ out/asan/chrome --user-data-dir=/tmp/xxxx --enable-features=PwaUpdateDialogForNameAndIcon "<http://localhost:8000/poc.html>" "<http://localhost:8888>"  

Click "Uninstall app".

[\*] The browser patch aims to simulate a web app to show the dialog, it has nothing to do with the vulnerability itself. Please notify me if necessary and I will construct a web app to bypass these checks.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: browser  

Crash State: see asan file

**CREDIT INFORMATION**  

Reporter credit: Leecraso and Guang Gong of 360 Alpha Lab

## Attachments

- [asan](attachments/asan) (text/plain, 14.9 KB)
- [patch.diff](attachments/patch.diff) (text/plain, 3.2 KB)
- [poc.html](attachments/poc.html) (text/plain, 114 B)
- [web_app_poc.zip](attachments/web_app_poc.zip) (application/octet-stream, 515.7 KB)
- [demo.mp4](attachments/demo.mp4) (video/mp4, 1.4 MB)

## Timeline

### [Deleted User] (2021-08-24)

[Empty comment from Monorail migration]

### le...@gmail.com (2021-08-24)

Sorry, I forgot to modify the Chrome Version, it should be beta with feature flag.

### dr...@chromium.org (2021-08-24)

This does reproduce as claimed. Assigning Memory Severity since this is browser process memory corruption, but you do need to convince the user to install a crafted, malicious web app, then trigger the identity update prompt while the user is on a specific page.

dmurph@, ericwilligers@ - can you take a look? I can't really evaluate how plausibly that patch simulates a legitimate web app.

[Monorail components: UI>Browser>WebAppInstalls]

### [Deleted User] (2021-08-24)

[Empty comment from Monorail migration]

### er...@chromium.org (2021-08-25)

[Empty comment from Monorail migration]

### er...@chromium.org (2021-08-25)

I think this dialog is still behind a disabled feature flag -  kPwaUpdateDialogForNameAndIcon

https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/browser_features.cc;drc=f7e9f5b591817bc7d11a08d602341d3e6fd8dc6b;l=57

Web servers and Service Workers for PWAs can update the manifests they serve (including title and icon changes) at any time.


### le...@gmail.com (2021-08-25)

yes

### [Deleted User] (2021-08-25)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-08-25)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cm...@chromium.org (2021-08-25)

[Empty comment from Monorail migration]

### es...@chromium.org (2021-08-25)

I've removed some labels that I don't think apply because this is a feature that hasn't shipped and won't ship till m95 at the earliest.

### [Deleted User] (2021-08-25)

[Empty comment from Monorail migration]

### dr...@chromium.org (2021-08-25)

Updating Impact per #11

### [Deleted User] (2021-08-25)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-08-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/53b3d81efd83448765424b5afa1ca547f7dfed57

commit 53b3d81efd83448765424b5afa1ca547f7dfed57
Author: Eric Willigers <ericwilligers@chromium.org>
Date: Wed Aug 25 21:35:59 2021

WebAppIdentityUpdateConfirmationView stores profile

WebAppIdentityUpdateConfirmationView retains a pointer to the app's
profile.

This avoids the need to look up the profile in member functions.

Bug: 1242841
Change-Id: I028bc08f212faf53956b2eabf661f600f353371a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3118765
Commit-Queue: Eric Willigers <ericwilligers@chromium.org>
Reviewed-by: Evan Stade <estade@chromium.org>
Reviewed-by: Daniel Murphy <dmurph@chromium.org>
Cr-Commit-Position: refs/heads/main@{#915346}

[modify] https://crrev.com/53b3d81efd83448765424b5afa1ca547f7dfed57/chrome/browser/ui/views/web_apps/web_app_identity_update_confirmation_view.cc
[modify] https://crrev.com/53b3d81efd83448765424b5afa1ca547f7dfed57/chrome/browser/ui/views/web_apps/web_app_identity_update_confirmation_view.h


### er...@chromium.org (2021-08-25)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-26)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-26)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-08-26)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-26)

Requesting merge to beta M93 because latest trunk commit (915346) appears to be after beta branch point (902210).

Requesting merge to dev M94 because latest trunk commit (915346) appears to be after dev branch point (911515).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-08-26)

This bug requires manual review: We are only 4 days from stable.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/main/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on ToT?
4. Does this change need to be merged into other active release branches (M-1, M+1)?
5. Why are these changes required in this milestone after branch?
6. Is this a new feature?
7. If it is a new feature, is it behind a flag using finch?

Chrome OS Only:
8. Was the change reviewed and approved by the Eng Prod Representative? See Eng Prod ownership by component: http://go/cros-engprodcomponents

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), govind@(iOS), geohsu@(ChromeOS), pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### es...@chromium.org (2021-08-26)

I don't know how to remove enough labels to accurately describe this bug.

The feature has not shipped so we definitely do not need merges to 93/94.

### es...@chromium.org (2021-08-26)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-26)

Dear owner, thanks for fixing this bug. We’ve reopened it because security bugs need Security_Severity and FoundIn labels set, which will enable the bots to request merges to the correct branches ( as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact (security@chromium.org) to arrange to set these labels and then this bug can be marked closed again. Thank you! Severity guidelines: https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues FoundIn guidelines: https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security Thanks for your time! 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### es...@chromium.org (2021-08-26)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-26)

[Empty comment from Monorail migration]

### es...@chromium.org (2021-08-26)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-27)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2021-09-01)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-09-01)

Congratulations Leecraso and Guang Gong, the VRP Panel has decided to award you $7000 for this report. Thank you for this report and nice finding! 

### le...@gmail.com (2021-09-02)

Considering that the bounty amount and security severity may be underestimated, I wrote a poc that is easy to trigger the bug without any patch.

REPRODUCTION CASE:

$ python server.py
$ out/asan/chrome --user-data-dir=/tmp/xxxx --enable-features=PwaUpdateDialogForNameAndIcon "http://localhost:8000/index.html"

1. Install the web app and click the trigger button.
2. Click "Uninstall app" after the poc page is closed

### am...@chromium.org (2021-09-03)

hi leecraso@ - thanks for this updated POC! I've gone ahead and bypassed sending your reward info to finance for processing. We will certainly revisit this issue at next week's VRP Panel for potential reward adjustment.
 
Given this issue is requires enabling a disabled feature flag AND installing a crafted malicious web app + some user gesture, the current security severity seems sufficient. 

### am...@chromium.org (2021-09-08)

hi leecraso@, apologies the VRP Panel has decided that the original reward amount is sufficient for this issue given the high degree of mitigations of required to trigger this vulnerability, including installation of the malicious web application and the amount of user gesture. As this is also in a PWA install update feature disabled by default, the VRP Panel deems the initial reward decision to be suitable for this report. 

### le...@gmail.com (2021-09-09)

Thank you, Amy. I will submit higher quality bug issues next time.

### am...@google.com (2021-09-09)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-03)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1242841?no_tracker_redirect=1

[Monorail blocking: crbug.com/chromium/1220070]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40056991)*
