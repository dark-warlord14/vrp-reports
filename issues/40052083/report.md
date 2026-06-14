# Security:  UAF  in DistillerJavaScriptService (Android)

| Field | Value |
|-------|-------|
| **Issue ID** | [40052083](https://issues.chromium.org/issues/40052083) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>ReaderMode |
| **Platforms** | Android |
| **Reporter** | ra...@gmail.com |
| **Assignee** | md...@chromium.org |
| **Created** | 2020-04-21 |
| **Bounty** | $20,000.00 |

## Description

**This template is ONLY for reporting security bugs. If you are reporting a**  

**Download Protection Bypass bug, please use the "Security - Download**  

**Protection" template. For all other reports, please use a different**  

**template.**

**Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com>**  

**/chromium/src/+/master/docs/security/faq.md**

**Please see the following link for instructions on filing security bugs:**  

**<https://www.chromium.org/Home/chromium-security/reporting-security-bugs>**

**Reports may be eligible for reward payments under the Chrome VRP:**  

**<http://g.co/ChromeBugRewards>**

**NOTE: Security bugs are normally made public once a fix has been widely**  

**deployed.**

**-------------------------**

**VULNERABILITY DETAILS**

when create DistillerJavaScriptService, DistillerJavaScriptServiceImpl object take render\_frame\_host by setting in distiller\_ui\_handle\_ .[1]  

then in HandleDistillerOpenSettingsCall, distiller\_ui\_handle\_ call rfh->IsCurrent() in OpenSettings()->WebContents::FromRenderFrameHost() [2][3]  

but render\_frame\_host can be deleted before HandleDistillerOpenSettingsCall is executed. therefore we can trigger UAF.  

rfh->IsCurrent() is virtual func. so it can lead to sandbox escape  

[1] : <https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/chrome_browser_interface_binders.cc;drc=546f632da779d87d55ddbbea5a2890e8f6db124e;l=252?originalUrl=https:%2F%2Fcs.chromium.org%2FF>  

[2] : <https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/android/dom_distiller/distiller_ui_handle_android.cc;drc=546f632da779d87d55ddbbea5a2890e8f6db124e;l=22?originalUrl=https:%2F%2Fcs.chromium.org%2F>  

[3] : <https://source.chromium.org/chromium/chromium/src/+/master:content/browser/web_contents/web_contents_impl.cc;drc=546f632da779d87d55ddbbea5a2890e8f6db124e;l=377?originalUrl=https:%2F%2Fcs.chromium.org%2F>

**VERSION**  

Chrome Version: chromium 84, maybe can trigger in stable channel  

Operating System: android

**REPRODUCTION CASE**  

environment setting is similar to <https://bugs.chromium.org/p/chromium/issues/detail?id=977462>  

Setup  

\* Build chromium for android and install chrome\_public\_apk  

\* Enable "command line flags on non rooted" to use MojoJS (<https://www.chromium.org/developers/how-tos/run-chromium-with-flags#TOC-Android>)  

\* Set the flag --enable-blink-features=MojoJS  

\* out/Pixel/bin/chrome\_public\_apk argv --args=' --enable-blink-features=MojoJS'  

\* Relaunch chromium and ensure enable-blink-features=MojoJS is enabled in chrome://version

you need generate DistillerJavaScriptService mojo js

poc is attached

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: browser

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: :Woojin Oh(@pwn\_expoit) of STEALIEN

## Attachments

- [repo.zip](attachments/repo.zip) (application/octet-stream, 1.5 MB)
- [crash.txt](attachments/crash.txt) (text/plain, 11.8 KB)
- [repo.zip](attachments/repo_53391140.zip) (application/octet-stream, 1.5 MB)

## Timeline

### me...@chromium.org (2020-04-21)

nyquist: PTAL as DOM distiller owner and reassign as appropriate?

I believe this requires a compromised rendered (because of MojoJS usage) so setting severity=high even though the UAF is in the browser process.

[Monorail components: UI>Browser>ReaderMode]

### [Deleted User] (2020-04-21)

Setting milestone and target because of Security_Impact=Head and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-04-21)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-04-21)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ra...@gmail.com (2020-04-21)

it is more reliable poc code. it need --enable-blink-features=MojoJS,MojoJSTest flags. compromised renderer can set this flags. in addition,  the code that include this vulnerability is merged M80 (https://chromium-review.googlesource.com/c/chromium/src/+/1892631). 

Perhaps not Security_Impact-Head, but Security_Impact-Stable

### wy...@chromium.org (2020-04-21)

I'm taking a look.

### wy...@chromium.org (2020-04-22)

I have several potential solutions for this security issue:

1. Make GetDistillerUIHandle a WebContentsUserData, then it naturally has access to a WebContents, so that we can avoid retaining a RenderFrameHost. We only need one GetDistillerUIHandle per profile, so making this per-WebContents is less efficient.

2. Remove OpenSettings(), since we are not using it right now. We currently have both the entry point and the settings in Java. OpenSettings() is to support having the entry point in web-UI and the settings in Java. We might migrate both the entry point and the settings from Java-UI to web-UI in the future. Either way, we don't need OpenSettings(). The followup question is, do we remove the JS binding entirely, or leave the boilerplate code so that the next time we need it, it's easier to add it back?



### md...@chromium.org (2020-04-22)

There's no point in keeping around unused code; I was actually thinking about removing this the other day. If we need it back we can always use the deletion patch as a basis. How does that sound?

### wy...@chromium.org (2020-04-22)

Sounds good. I'll go ahead and remove it entirely.

### md...@chromium.org (2020-04-24)

Turns out the javascript services are needed after all: https://chromium-review.googlesource.com/c/chromium/src/+/2152901

I'll look into alternative fixes.

### am...@google.com (2020-04-27)

Please ignore, no action required - we are testing automation around potential SLOs for release blockers.  Email me with any concerns.

### am...@google.com (2020-04-29)

Please ignore, no action required - we are testing automation around potential SLOs for release blockers.  Email me with any concerns.

### [Deleted User] (2020-05-07)

wychen: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2020-05-07)

A prior comment / related label was applied to this bug: "Please ignore, no action required - we are testing automation around potential SLOs for release blockers.  Email me with any concerns."

This wording was poor - the *comment and the label RB-SLO-<Fix|Comment>* should be ignored, but this bug is still considered a release blocker that should be fixed as quickly as possible.  *Please do not ignore this bug* and continue to work on it as a top priority.

I apologize for any confusion this may have caused, and the new comment applied to bugs by this automation that is being tested will be more clear: "Please ignore this comment and the new label, and continue to work on this release blocking bug urgently - we are testing automation around potential SLOs for release blockers.  Email me with any concerns."

### [Deleted User] (2020-05-08)

wychen: Uh oh! This issue still open and hasn't been updated in the last 15 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-05-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/23697cba0fd129e9643bb9affbd3d4790472d7dc

commit 23697cba0fd129e9643bb9affbd3d4790472d7dc
Author: Matt Jones <mdjones@chromium.org>
Date: Fri May 08 22:06:44 2020

Remove unused openSetting implementation for dom distiller JS

The UI handle infrastructure will be removed in a followup.

Bug: 1073015
Change-Id: I5a427f58b26a69816acd462e09e6ceebb80d704b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2190041
Reviewed-by: Tommy Nyquist <nyquist@chromium.org>
Reviewed-by: Wei-Yin Chen (陳威尹) <wychen@chromium.org>
Commit-Queue: Matthew Jones <mdjones@chromium.org>
Cr-Commit-Position: refs/heads/master@{#766992}

[modify] https://crrev.com/23697cba0fd129e9643bb9affbd3d4790472d7dc/chrome/browser/android/dom_distiller/distiller_ui_handle_android.cc


### md...@chromium.org (2020-05-08)

[Empty comment from Monorail migration]

### [Deleted User] (2020-05-09)

[Empty comment from Monorail migration]

### na...@google.com (2020-05-11)

[Empty comment from Monorail migration]

### ad...@google.com (2020-05-13)

The earlier setting of Security_Impact-Head resulted in M-84, which prevented Sheriffbot from setting Merge-Request-83. Doing so now.

mdjones@/wychen@ how does this look in Canary? Do you have any stability concerns about merging this to M83? It'll likely make the first M83 security refresh.

### md...@chromium.org (2020-05-13)

This code has been unused/unchanged for a pretty long time, merging to 83 should be no problem.

### wy...@chromium.org (2020-05-13)

Not sure if it matters. I remember we use Merge-Request-XX instead of Merge_Request-XX in the past.

### [Deleted User] (2020-05-13)

This bug requires manual review: To minimize risk and increase branch stability, all merge requests are being reviewed manually by the release team.
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
Owners: benmason@(Android), bindusuvarna@(iOS), cindyb@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### md...@chromium.org (2020-05-13)

1. Does your merge fit within the Merge Decision Guidelines?
  Yes
2. Links to the CLs you are requesting to merge.
  https://chromium-review.googlesource.com/c/chromium/src/+/2190041
3. Has the change landed and been verified on master/ToT?
  Yes
4. Why are these changes required in this milestone after branch?
  Potential use-after-free vulnerability.
5. Is this a new feature?
  No
6. If it is a new feature, is it behind a flag using finch?
  N/A

### na...@google.com (2020-05-14)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-05-14)

Congrats! The Panel decided to award $20,000 for this report. 


### be...@google.com (2020-05-14)

Adrian: Not planning on taking this for first release of M83, would this be OK to follow up in security re-spin?

### ad...@google.com (2020-05-14)

Approving merge to M83, branch 4103.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-05-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/7c9173e32d4cdc9a45c12ed6323907ef93dcc525

commit 7c9173e32d4cdc9a45c12ed6323907ef93dcc525
Author: Matt Jones <mdjones@chromium.org>
Date: Thu May 14 21:30:22 2020

Remove unused openSetting implementation for dom distiller JS

The UI handle infrastructure will be removed in a followup.

(cherry picked from commit 23697cba0fd129e9643bb9affbd3d4790472d7dc)

Bug: 1073015
Change-Id: I5a427f58b26a69816acd462e09e6ceebb80d704b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2190041
Reviewed-by: Tommy Nyquist <nyquist@chromium.org>
Reviewed-by: Wei-Yin Chen (陳威尹) <wychen@chromium.org>
Commit-Queue: Matthew Jones <mdjones@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#766992}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2202524
Reviewed-by: Ben Mason <benmason@chromium.org>
Cr-Commit-Position: refs/branch-heads/4103@{#548}
Cr-Branched-From: 8ad47e8d21f6866e4a37f47d83a860d41debf514-refs/heads/master@{#756066}

[modify] https://crrev.com/7c9173e32d4cdc9a45c12ed6323907ef93dcc525/chrome/browser/android/dom_distiller/distiller_ui_handle_android.cc


### na...@google.com (2020-05-15)

[Empty comment from Monorail migration]

### ad...@google.com (2020-05-15)

[Empty comment from Monorail migration]

### ra...@gmail.com (2020-05-18)

Can i get CVE credit? 

### ad...@chromium.org (2020-05-18)

Yes. We allocate CVEs as we produce the release notes, which will be happening today, for release tomorrow.

### ad...@chromium.org (2020-05-18)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-05-21)

[Empty comment from Monorail migration]

### mm...@chromium.org (2020-06-30)

wychen@, thank you for fixing this issue. Chrome Security team needs your knowledge to prevent that whole class of bugs from happening elsewhere. We would greatly appreciate if you could tell us more about the issue by filling out the following form: https://forms.gle/VWKDUv9a8GXCCRWm7

### wy...@chromium.org (2020-06-30)

Matt did all the fixing. Assign owner accordingly. Matt, would you mind filling out the form?

### md...@chromium.org (2020-07-01)

I've filled out and submitted the form.

### mm...@chromium.org (2020-07-07)

[Empty comment from Monorail migration]

### [Deleted User] (2020-08-15)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1073015?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40052083)*
