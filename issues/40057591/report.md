# Security UI Spoofing on Chrome for Android due to the Contact permission dialog hiding the fullscreen alert message

| Field | Value |
|-------|-------|
| **Issue ID** | [40057591](https://issues.chromium.org/issues/40057591) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Contacts, Blink>Fullscreen, Blink>PermissionsAPI, UI>Browser>FullScreen |
| **Platforms** | Android |
| **CVE IDs** | CVE-2022-1307 |
| **Reporter** | he...@gmail.com |
| **Assignee** | ji...@chromium.org |
| **Created** | 2021-10-13 |
| **Bounty** | $7,500.00 |

## Description

**VULNERABILITY DETAILS**  

When a user clicks on the attacker's page it is possible to use their activation to call navigator.contacts.select (Contact Picker API) and at the same time request the page to enter fullscreen.

It seems that when both are called at the same time, the Contact permission dialog from the Contact Picker API gets precedence over the fullscreen alert message that notifies the user that they entered fullscreen.

Because the fullscreen message is never displayed, the user is not capable to know that they entered fullscreen, which allows an attacker to spoof the entire screen with attacker-controlled content.

The attack "looks" better when the user didn't grant Chrome the Contact permission (which I believe are most of the cases), but it works eitheir way.

I have attached a video reproducing the attack.

**VERSION**  

Chrome Version: 94.0.4606.80  

Operating System: Android 11

**REPRODUCTION CASE**

1. Access <https://lbherrera.github.io/lab/chrome/contacts-spoof-233217/index.html> on Chrome for Android.
2. Click anywhere on the page (make sure you didn't grant the Contact permission to Chrome yet).
3. A permission dialog will show up and the underlying page will spoof the omnibox as well as the "accounts.google.com" page.
4. You can dismiss the dialog and the page will remain spoofed.

I have also attached the files used in the PoC - if you prefer, you can reproduce it by downloading and hosting index.html and spoof.png on a web server.

**CREDIT INFORMATION**  

Reporter credit: Luan Herrera (@lbherrera\_)

## Attachments

- [index.html](attachments/index.html) (text/plain, 1.2 KB)
- [spoof.png](attachments/spoof.png) (image/png, 94.6 KB)
- [repro.mp4](attachments/repro.mp4) (video/mp4, 5.3 MB)
- [repro.mp4](attachments/repro.mp4) (video/mp4, 279.9 KB)

## Timeline

### [Deleted User] (2021-10-13)

[Empty comment from Monorail migration]

### ct...@chromium.org (2021-10-13)

Thanks for the report. I can confirm this reproduces on trunk chromium. This feels like a fairly substantial spoofing vector -- I can't recover to show the real omnibox as the page's click handler catches inputs. (Initially I thought this might be mitigated if we always showed the mini-URL bar like we have on iOS, but this uses document.requestFullscreen() which would bypass that still I think.)

https://crbug.com/chromium/1259694 is similar and might share a broader fix.

### bd...@chromium.org (2021-10-13)

@rayankans can you take a look at this? 

[Monorail components: Blink>Contacts]

### [Deleted User] (2021-10-13)

[Empty comment from Monorail migration]

### en...@chromium.org (2021-10-13)

I believe the Contacts API shipped in M80, so depending on whether there have been any changes on how we display the full-screen toast since, this theoretically could have been impacting Stable since M80. It is unclear to me if reproes on Android 10 and before as well.

@Avi as FYI, as there is a full-screen implications.

### en...@chromium.org (2021-10-13)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-13)

[Empty comment from Monorail migration]

### ra...@chromium.org (2021-10-14)

[Empty comment from Monorail migration]

### fi...@chromium.org (2021-10-14)

It is not too much of a stretch to imagine any other APIs that show a dialog could potentially cause the same issue, so to me this seems like it should be solved in a generic way, as opposed to playing whack-a-mole with individual features like the Contacts API.

### [Deleted User] (2021-10-14)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ct...@chromium.org (2021-10-15)

[Empty comment from Monorail migration]

### ra...@chromium.org (2021-10-19)

The other bug (crbug.com/1259694) is related tot he Contacts API, and a fix is being worked on.

As finnur@ mentioned, this is related to permissions rather than Contacts, assigning back to bdea@ for triage.

### bd...@chromium.org (2021-10-19)

@engedy can you take a look at this?

[Monorail components: -Blink>Contacts Blink>PermissionsAPI]

### [Deleted User] (2021-10-29)

engedy: Uh oh! This issue still open and hasn't been updated in the last 15 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-11-09)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-11-15)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-12)

We commit ourselves to a 60 day deadline for fixing for high severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-12)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### do...@chromium.org (2022-01-24)

Security marshall ping: this issue has exceeded the deadline we set for high severity vulnerabilities.

Since this is scoped to the contacts dialog, I'm going to reroute it to the contacts folks. If a more generic solution for other dialogs can be found, that's great, but for the time being, we should directly address this spoofing vector in the contacts picker. Finnur, do you mind investigating a fix here?

[Monorail components: Blink>Contacts]

### en...@chromium.org (2022-01-24)

Apologies, I have not been able to get to this. Finnur, can you please drive the fix for the Contacts API? Kamila volunteered to participate in the discussion from our side.

### [Deleted User] (2022-02-02)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-07)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-03-17)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2022-03-25)

finnur@, please could you confirm you're on top of this and have a plan?

### fi...@chromium.org (2022-03-28)

I don't think there's agreement on how to fix this. I'll follow up in email.

### [Deleted User] (2022-03-30)

[Empty comment from Monorail migration]

### bo...@chromium.org (2022-04-20)

Hi @finnur, did the email / discussion from https://crbug.com/chromium/1259492#c25 take place? If so please link any of the resulting docs/conclusions here so there's some shared visibility of open questions and/or next steps. 

### fi...@chromium.org (2022-04-28)

I've CC-ed you on the discussion.

### an...@chromium.org (2022-05-06)

Hi @finnur, could you provide an update? Is there any summary/conclusion from the offline email/discussion you can add here so that there is more visibility regarding status/next steps. Thanks!

### [Deleted User] (2022-05-25)

[Empty comment from Monorail migration]

### ma...@google.com (2022-06-02)

Security marshal bump. I also just pinged engedy@ about this and he says he will poke the email thread from https://crbug.com/chromium/1259492#c25.

### th...@chromium.org (2022-06-10)

Security marshal here. finnur@ / engedy@, are there any status updates that can be added to this ticket? (will ping as well)

### th...@chromium.org (2022-06-13)

Update on this is that the email thread has mostly been stagnant since the first few responses in late March (though I've now bumped it). There is not yet clarity on the thread on a path forward.

### [Deleted User] (2022-07-14)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-07-26)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-08-03)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-07)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-09-19)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-09-28)

[Empty comment from Monorail migration]

### xi...@chromium.org (2022-09-30)

+jinsukkim@/twellington@, would your team be able to help with this? There could be a general solution for both this issue and https://crbug.com/1356987 (External notifications from external apps can block Android fullscreen notification). Thanks!

[Monorail components: Blink>Fullscreen UI>Browser>FullScreen]

### ji...@chromium.org (2022-09-30)

[Empty comment from Monorail migration]

### ji...@chromium.org (2022-09-30)

A series of CLs landed early this year to fix similar issues. Just verified that they also addressed this issue. 

https://source.chromium.org/chromium/chromium/src/+/9126f59e3fe456c8bad83424bab74ec514380e79
https://source.chromium.org/chromium/chromium/src/+/5326b6967d000c677efa23b9f849145b0b06df07
https://source.chromium.org/chromium/chromium/src/+/4467745fff4dab3f622baf75e40aca552b9ab6dc

Video clip: https://drive.google.com/file/d/1Ny1QrtIXl-SxH652COzaTjZSnHfjBJ2W/view?usp=sharing


### he...@gmail.com (2022-09-30)

Hey! If they indeed fixed this issue (I can't check the video due to lack of permissions) then I think this report should be marked as Fixed instead of WontFix.

Since I am an external reporter this report merits consideration from the Chrome VRP panel (from looking at the Bug IDs referenced in the CLs, this report is older).

For the VRP consideration:
This vulnerability allowed an attacker to hide the fullscreen notification message and completely spoof the address bar on Chrome for mobile, with an impact similar to https://crbug.com/chromium/1270593.

### bo...@google.com (2022-09-30)

@herrerahlb, sorry about that. Reopening because WontFix is not appropriate in this case.

@jinsukkim, if this was a known issue and any (or all) the 3 CLs linked in https://crbug.com/chromium/1259492#c42 resolved this issue, then Duplicate would be a more accurate status. However, the CLs in https://crbug.com/chromium/1259492#c42 had these associated tracking bugs:

- https://crbug.com/1270052 (opened Nov '21)
- https://crbug.com/1301873 (opened Feb '22)
- https://crbug.com/1311683 (opened Mar '22)
- https://crbug.com/1316051 (opened Apr '22)

This report made on Oct '21 and precedes all of the existing bug reports, so if the bug is in fact related then it would have be more accurate to duplicate at least one of the subsequent reports on this bug. 

@herrerahlb or @jinsukkim, can either of you verify that the issue is now resolved in the latest shipping version of Chrome? If so, Fixed is an appropriate status. 

### he...@gmail.com (2022-09-30)

@bookholt, no problem, thanks! 

I tried to reproduce the issue on Google Chrome for Android (105.0.5195.136) and it is fixed. The fullscreen notification message is not being dismissed anymore by the Contact permission dialog.

I have attached a video trying to reproduce the issue.

### bo...@google.com (2022-10-03)

Thanks @herrerahlb. I'm marking this bug Fixed based on your input in https://crbug.com/chromium/1259492#c45. Our automation should now route this bug to VRP panel's review queue. 

@jinsukkim, if you're able, it would be helpful if you can also check and update this report to Verified if you're satisfied that it's fixed. Ideally we'd also have a test for to prevent regressions if that's feasible. 

Thanks to you both for your help!

Note for VRP friends: I may be missing some important context and I defer to you about the review outcome, but IMO it's important to point out this report seems to have taken an unfortunate path. Subsequent reports that were likely a duplicate of this report were not recognized as a dup, and instead received VRP rewards while this report waited in review purgatory. 

### ji...@chromium.org (2022-10-03)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-03)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-03)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-03)

This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M106. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M107. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-10-03)

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

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
Owners: govind (Android), eakpobaro (iOS), dgagnon (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-10-03)

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

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
Owners: eakpobaro (Android), harrysouders (iOS), ceb (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-10-05)

per https://crbug.com/chromium/1259492#c42, this issue was resolved by previously landed and merged CLs associated with other issues; nothing to merge here 

### am...@google.com (2022-10-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-10-13)

Congratulations, Luan! The VRP Panel has decided to award you $7500 for this report. Neat finding! Thank you for your efforts in finding and reporting this issue to us! 

### am...@google.com (2022-10-14)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-12-13)

Based on https://crbug.com/chromium/1259492#c42, various work from 3 different CLs can be considered responsible for resolving this issue. Based on timing, impact, and affected code, it looks like it can be narrowed down to https://ccrev.com/c/3372521 and https://ccrev.com/c/3501458. Since I cannot be entirely sure, I'm going to tie this one to the latest shipped fix (since it is possible that the combination of all this work is responsible for the mitigation of this issue). 

Luan, again apologies for the mix-up and mishandling of this report throughout that - while we did marshal it back to being considered for VRP, albeit a bit late,- still resulted in it being missed in inclusion in release notes and getting a CVE since there was no fix landed here or this bug linked to any CL that would have allowed CVE and release automation to pull this issue in for inclusion in release notes. 

added appropriate labels so this can be rectified as well as updating with CVE (CVE-2022-1307, already/also issued on https://crbug.com/chromium/1301873). Rather than creating a new release notes entry, the current entry for this CVE should be updated to also acknowledge this researcher who reported this report) 

### he...@gmail.com (2022-12-13)

No worries, thanks!

### [Deleted User] (2023-01-09)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pg...@google.com (2023-07-28)

The release notes have been updated to include this information! thank you for your patience!
https://chromereleases.googleblog.com/2022/04/stable-channel-update-for-desktop_11.html

### pg...@google.com (2023-07-28)

[Empty comment from Monorail migration]

### pg...@google.com (2023-08-25)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1259492?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>Contacts, Blink>Fullscreen, Blink>PermissionsAPI, UI>Browser>FullScreen]
[Monorail components added to Component Tags custom field.]

### dc...@chromium.org (2025-10-07)

Argh sorry I had the wrong bug open.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057591)*
