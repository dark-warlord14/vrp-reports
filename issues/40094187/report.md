# chrome.dashboardPrivate API is exposed to whole origin of https://chrome.google.com

| Field | Value |
|-------|-------|
| **Issue ID** | [40094187](https://issues.chromium.org/issues/40094187) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Sandbox>SiteIsolation, Platform>Extensions, Webstore |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | Ju...@microsoft.com |
| **Assignee** | ct...@chromium.org |
| **Created** | 2019-03-01 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3714.0 Safari/537.36 Edg/74.1.88.0

Steps to reproduce the problem:
1. Go to https://www.google.com/
2. Open console, type `window.open("https://chrome.google.com/robots.txt")` and hit enter
3. Observe that both tabs are committed in the same process
4. Open console in https://chrome.google.com/robots.txt
5. Run following script
fetch("https://shhnjk.azurewebsites.net/manifest.php").then(r=>r.text()).then(manifest=>{
chrome.dashboardPrivate.showPermissionPromptForDelegatedInstall({id: "hdokiejnpimakedhajhdlcegeplioahd",manifest: manifest, delegatedUser: "USER_HERE"})
})

What is the expected behavior?
Either chrome.dashboardPrivate API isn't exposed or https://chrome.google.com/robots.txt should spawn a separate process

What went wrong?
Chrome Web Store hosted app is exposed to "https://chrome.google.com/webstore*"
https://cs.chromium.org/chromium/src/chrome/browser/resources/webstore_app/manifest.json

This means https://chrome.google.com/robots.txt is not a part of Chrome Web Store. But chrome.dashboardPrivate API is exposed to whole https://chrome.google.com origin. Therefore script execution + renderer compromise in *.google.com will also get access to chrome.dashboardPrivate API due to the fact that https://chrome.google.com/robots.txt will be treated as same-site to *.google.com.

Did this work before? N/A 

Chrome version: 72  Channel: stable
OS Version: 10.0
Flash Version:

## Timeline

### cr...@chromium.org (2019-03-01)

Thanks for the report!

Devlin, do you know how access to the dashboardPrivate API is managed?  (Feel free to reassign as needed.)

That API probably shouldn't be exposed origin-wide, given that the privileged CWS hosted app is restricted to the /webstore path.  I'm not sure about the severity-- would depend on what that API can do.

[Monorail components: Internals>Sandbox>SiteIsolation Platform>Extensions Webstore]

### ct...@chromium.org (2019-03-01)

The private API is granted based on https://cs.chromium.org/chromium/src/chrome/common/extensions/api/_api_features.json?l=300

"dashboardPrivate": [{
    "channel": "stable",
    "contexts": ["blessed_web_page", "web_page"],
    "matches": ["https://chrome.google.com/*"]
  }, {
    "channel": "stable",
    "contexts": ["blessed_extension"],
    "whitelist": [
      "B44D08FD98F1523ED5837D78D0A606EA9D6206E5"  // Web Store
    ]
  }]

So maybe we could update the match to "https://chrome.google.com/webstore/*?

### rd...@chromium.org (2019-03-01)

Yep, just changing the "matches" entry seems like it should work (I can't think of any non-webstore pieces that need access to it).  cthomp@, did you want to take that on?

### ct...@chromium.org (2019-03-02)

Sure, here's the quick CL for that change: https://crrev.com/c/1497631.

I'll run the trybots on it to make sure it doesn't break anything, and make sure locally that the webstore works as expected.

One question about the `matches` wildcard syntax: does this need to separately include "https://chrome.google.com/webstore" or does "/webstore/*" include that?

### rd...@chromium.org (2019-03-02)

/webstore/* should include /webstore (I just ran a unit test to verify).  Good question!

### ct...@chromium.org (2019-03-02)

Setting some security labels:

Conservatively treating this as a Severity-High, as it could potentially be used as a sandbox escape of a sort (installing a malicious extension). Per the severity guidelines: "For example, renderer sandbox escapes fall into this category as their impact is that of a critical severity bug, but they require the precondition of a compromised renderer."

Also, I think this dates back to https://codereview.chromium.org/1268853003 (per blame), so setting Impact-Stable.

### rd...@chromium.org (2019-03-02)

My $0.02, but I don't think this is severity-high - I don't think that access to this API is actually critical severity.  When installing an extension, we still show a native installation prompt, which can't be circumvented.

### ct...@chromium.org (2019-03-02)

Yeah, that's a reasonable mitigating factor. Looking at DashboardPrivateShowPermissionPromptForDelegatedInstallFunction::Run(), it looks like my main concern (that a malicious caller could "lie" in the installation prompt) shouldn't be possible (the manifest passed in the API param needs to match the manifest of the downloaded extension [1]). A malicious caller _could_ spam the install dialog, which would be highly annoying but also highly visible.

[1] https://cs.chromium.org/chromium/src/out/Debug/gen/chrome/common/extensions/api/dashboard_private.h?g=0&l=71

### Ju...@microsoft.com (2019-03-02)

>the manifest passed in the API param needs to match the manifest of the downloaded extension

Why can't attacker host malicious extension in the Chrome Web Store?

### ct...@chromium.org (2019-03-02)

They can but they can't lie about it AFAIK, so the installation prompt is still "valid" (making this similar to requiring complicated user interaction in other bugs). The extension itself is still restricted to the permissions it requests, for example.

I'm open to arguments either way though.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-03-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/1b661f83324b837ac34725c639d998d6ff23ff1d

commit 1b661f83324b837ac34725c639d998d6ff23ff1d
Author: Christopher Thompson <cthomp@chromium.org>
Date: Sat Mar 02 01:30:06 2019

Update chrome.dashboardPrivate API match

Bug: 937487
Change-Id: I2d985e28c56d4a7626e3d0c11a8be6d31499a66b
Reviewed-on: https://chromium-review.googlesource.com/c/1497631
Reviewed-by: Devlin <rdevlin.cronin@chromium.org>
Commit-Queue: Christopher Thompson <cthomp@chromium.org>
Cr-Commit-Position: refs/heads/master@{#637049}
[modify] https://crrev.com/1b661f83324b837ac34725c639d998d6ff23ff1d/chrome/common/extensions/api/_api_features.json


### ct...@chromium.org (2019-03-04)

Marking this as fixed and requesting merges (M-73, and M-72 just in case). The fix is minimal and should be safe to merge.

### sh...@chromium.org (2019-03-04)

This bug requires manual review: We are only 7 days from stable.
Please contact the milestone owner if you have questions.
Owners: benmason@(Android), kariahda@(iOS), cindyb@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ab...@google.com (2019-03-04)

Approved for 73. branch:3683

### wf...@chromium.org (2019-03-04)

Would an additional mitigation be to always isolate domains that have any special API access at all?

I think this is the only domain right now (visually groking the json) but that doesn't mean there might not be ones in the future.

### ct...@chromium.org (2019-03-04)

Yeah, potentially. I wonder if we could specifically add any private extension API URLs to the isolate origins list (ideally, automatically by them being listed in this json). This is maybe made tricky by cases like this one where the isolation boundary is actually more fine-grained than origins.

If I remember correctly the actual CWS URL (chrome.google.com/webstore/*) is process isolated already, but chrome.google.com isn't.

creis@ may have more opinions/context on this.

### ab...@google.com (2019-03-04)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-03-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/5722cbde15fe7dc5e66456f1b8c2e9df67159027

commit 5722cbde15fe7dc5e66456f1b8c2e9df67159027
Author: Christopher Thompson <cthomp@chromium.org>
Date: Mon Mar 04 17:40:29 2019

[M73] Update chrome.dashboardPrivate API match

Bug: 937487
Change-Id: I2d985e28c56d4a7626e3d0c11a8be6d31499a66b
Reviewed-on: https://chromium-review.googlesource.com/c/1497631
Reviewed-by: Devlin <rdevlin.cronin@chromium.org>
Commit-Queue: Christopher Thompson <cthomp@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#637049}(cherry picked from commit 1b661f83324b837ac34725c639d998d6ff23ff1d)
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1499724
Reviewed-by: Christopher Thompson <cthomp@chromium.org>
Cr-Commit-Position: refs/branch-heads/3683@{#730}
Cr-Branched-From: e51029943e0a38dd794b73caaf6373d5496ae783-refs/heads/master@{#625896}
[modify] https://crrev.com/5722cbde15fe7dc5e66456f1b8c2e9df67159027/chrome/common/extensions/api/_api_features.json


### cr...@appspot.gserviceaccount.com (2019-03-04)

The following revision refers to this bug: 
https://chromium.googlesource.com/chromium/src.git/+/5722cbde15fe7dc5e66456f1b8c2e9df67159027

Commit: 5722cbde15fe7dc5e66456f1b8c2e9df67159027
Author: cthomp@chromium.org
Commiter: cthomp@chromium.org
Date: 2019-03-04 17:40:29 +0000 UTC

[M73] Update chrome.dashboardPrivate API match

Bug: 937487
Change-Id: I2d985e28c56d4a7626e3d0c11a8be6d31499a66b
Reviewed-on: https://chromium-review.googlesource.com/c/1497631
Reviewed-by: Devlin <rdevlin.cronin@chromium.org>
Commit-Queue: Christopher Thompson <cthomp@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#637049}(cherry picked from commit 1b661f83324b837ac34725c639d998d6ff23ff1d)
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1499724
Reviewed-by: Christopher Thompson <cthomp@chromium.org>
Cr-Commit-Position: refs/branch-heads/3683@{#730}
Cr-Branched-From: e51029943e0a38dd794b73caaf6373d5496ae783-refs/heads/master@{#625896}

### na...@google.com (2019-03-04)

[Empty comment from Monorail migration]

### aw...@google.com (2019-03-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-03-05)

[Empty comment from Monorail migration]

### Ju...@microsoft.com (2019-03-06)

>If I remember correctly the actual CWS URL (chrome.google.com/webstore/*) is
>process isolated already, but chrome.google.com isn't.

Yes. I've filed https://crbug.com/chromium/939108 as a follow up.

### aw...@chromium.org (2019-03-13)

[Empty comment from Monorail migration]

### na...@google.com (2019-03-14)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### na...@google.com (2019-03-14)

Congrats! The Panel decided to reward $500 for this report :) 

### na...@google.com (2019-03-26)

[Empty comment from Monorail migration]

### aw...@google.com (2019-04-05)

[Empty comment from Monorail migration]

### aw...@google.com (2019-04-05)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-05-22)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-06-11)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2019-06-11)

This issue was migrated from crbug.com/chromium/937487?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Internals>Sandbox>SiteIsolation, Platform>Extensions, Webstore]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094187)*
