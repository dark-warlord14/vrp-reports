# Contact dialog can be shown over a cross-origin page which might confuse a user into leaking sensitive information to an attacker

| Field | Value |
|-------|-------|
| **Issue ID** | [40057597](https://issues.chromium.org/issues/40057597) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Contacts |
| **Platforms** | Android |
| **Reporter** | he...@gmail.com |
| **Assignee** | fi...@chromium.org |
| **Created** | 2021-10-13 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

When a user clicks on the attacker's page it is possible to use their activation to call navigator.contacts.select (Contact Picker API) and at the same time open a cross-origin page in a new window.

This causes the Contact permission dialog to show above the cross-origin page that was just opened and might confuse the user into leaking sensitive information (their contact list details) to an attacker.

Although the origin that requested the Contact Picker is shown in the dialog, I believe the dialog should have been dismissed when the window was opened as it is not entirely clear to the user the relation of the malicious origin with the underlying cross-origin page that is being shown in their screen.

The attack works best when the user hasn't granted Chrome the Contact permission and if a similar domain to the targeted origin being spoofed is used.

I have attached a video reproducing the attack.

**VERSION**  

Chrome Version: 94.0.4606.80  

Operating System: Android 11

**REPRODUCTION CASE**

1. Access <https://lbherrera.github.io/lab/chrome/contacts-crossorigin-147331/index.html> on Chrome for Android.
2. Click anywhere on the page (make sure you didn't give the Contacts permission to Chrome yet).
3. A permission dialog will show up and the underlying page will be from "www.google.com".
4. If you accept the permission and select a few of your contacts, they will be leaked to the attacker.

I have also attached the file used in the PoC - if you prefer, you can reproduce it by downloading and hosting index.html on a web server.

**CREDIT INFORMATION**  

Reporter credit: Luan Herrera (@lbherrera\_)

## Attachments

- [index.html](attachments/index.html) (text/plain, 958 B)
- [repro.mp4](attachments/repro.mp4) (video/mp4, 8.3 MB)

## Timeline

### [Deleted User] (2021-10-13)

[Empty comment from Monorail migration]

### ct...@chromium.org (2021-10-13)

Confirmed that this repros on trunk chromium. Although for me the system permission prompt comes up immediately on click so it "feels" like it is triggered from the click rather than the navigation. The contact picker UI does show the correct origin as expected. It seems plausible that all system permission prompts (like this one) can get navigated underneath, so maybe this should be handled for any and all system permission prompts. I'm not sure if Chrome can "cancel" the system prompt though.

https://crbug.com/chromium/1259492 is similar and might share a broader fix.

### bd...@chromium.org (2021-10-13)

@rayankans can you take a look at this? 

[Monorail components: Blink>Contacts]

### [Deleted User] (2021-10-13)

[Empty comment from Monorail migration]

### en...@chromium.org (2021-10-13)

I believe the Contacts API shipped in M80, so this theoretically could have been impacting Stable since M80.

### [Deleted User] (2021-10-13)

[Empty comment from Monorail migration]

### ra...@chromium.org (2021-10-14)

[Empty comment from Monorail migration]

### fi...@chromium.org (2021-10-14)

This is already mitigated by showing the origin, which clearly communicates with the user exactly what site will be receiving the data.

But, yes. It should be possible to run the origin check upon opening the dialog to make sure that the active contents haven't changed.

I spoke with Rayan, who said he wanted to take a look at this. 


### fi...@chromium.org (2021-10-14)

The question in my mind is whether we also need to guard against delays in navigation -- so that we need to install a notifier for when new foreground tabs open while the dialog is up and close the dialog. Because if the dialog stays up, then that has a very similar outcome (dialog shown on top of the wrong content). 

### ra...@chromium.org (2021-10-14)

> The question in my mind is whether we also need to guard against delays in navigation

Agreed, maybe let's get some clarity on this issue first as it will affect the solution. 

Is the security issue here that the new tab is opening _before_ the Contact Picker is shown leading to potential confusion for the user in regards to who the data is being shared with, or the fact that a new tab is being opened at all and the user returns to a different tab than the one requesting the contacts?

### ct...@chromium.org (2021-10-14)

I think more the former than the latter. (For the latter, the page could easily initiate a navigation on the promise completing for the API call (i.e., after the contact picker dialog completes) and I don't think we can or should prevent that.)

### fi...@chromium.org (2021-10-14)

Why does it matter if the navigation starts x ms before the contact picker shows or y ms after it shows? The end result for the user is exactly the same, is it not? They're seeing a dialog on top of site B but share with site A...

### fi...@chromium.org (2021-10-14)

Also, I'm not suggesting we prevent the site from navigating once they get back the results from the dialog. I'm saying if you fire off a request to show the dialog and another to open a new tab, it shouldn't matter (in terms of this issue) which one appears last -- they're both going to be on screen at the same time, so there is potential for confusion, right?

### [Deleted User] (2021-10-14)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ct...@chromium.org (2021-10-15)

I think the distinction is that the system permission dialog is displayed as an overlayed modal on top of the active page, while the contact picker is a full screen dialog that does not show any of the underlying page. To the user, a navigation starting *after* the contact picker shows is essentially indistinguishable from a navigation starting when the contact picker resolves (modulo some loading time but that could be manipulated by a clever attacker I think). Does that make my remark in https://crbug.com/chromium/1259694#c11 make more sense? I do think it would be good to drop both the system permission dialog *and* the contact picker dialog in these cases though.

### fi...@chromium.org (2021-10-18)

Oh, I see. So because the benign site navigation isn't visible to the user, there's no confusion on their part and we therefore don't need to automatically close the Contacts dialog.

That's fair, I guess. And simplifies the mitigation too.

### ct...@chromium.org (2021-10-18)

+mgiuca@ and ericwilligers@ for visibility (from https://crbug.com/chromium/1259654 which potentially shares some root cause/fix)

### gi...@appspot.gserviceaccount.com (2021-10-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/53568f244c8594f200ead4e042f29efb55f3be82

commit 53568f244c8594f200ead4e042f29efb55f3be82
Author: Rayan Kanso <rayankans@google.com>
Date: Thu Oct 28 13:07:26 2021

[Contacts] Check the WebContents are still active/valid before launching
picker

Bug: 1259694
Change-Id: I75e16c99f4cf64d110067c7cce30d789c0f92808
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3226375
Commit-Queue: Rayan Kanso <rayankans@chromium.org>
Reviewed-by: David Trainor <dtrainor@chromium.org>
Reviewed-by: Finnur Thorarinsson <finnur@chromium.org>
Cr-Commit-Position: refs/heads/main@{#935851}

[modify] https://crrev.com/53568f244c8594f200ead4e042f29efb55f3be82/components/browser_ui/contacts_picker/android/java/src/org/chromium/components/browser_ui/contacts_picker/ContactsPickerDialogTest.java
[modify] https://crrev.com/53568f244c8594f200ead4e042f29efb55f3be82/content/browser/contacts/contacts_provider_android.cc
[modify] https://crrev.com/53568f244c8594f200ead4e042f29efb55f3be82/content/public/android/java/src/org/chromium/content/browser/ContactsDialogHost.java
[modify] https://crrev.com/53568f244c8594f200ead4e042f29efb55f3be82/content/public/android/java/src/org/chromium/content_public/browser/ContactsPicker.java
[add] https://crrev.com/53568f244c8594f200ead4e042f29efb55f3be82/chrome/android/javatests/src/org/chromium/chrome/browser/contacts_picker/ContactsPickerLauncherTest.java
[modify] https://crrev.com/53568f244c8594f200ead4e042f29efb55f3be82/components/browser_ui/contacts_picker/android/BUILD.gn
[modify] https://crrev.com/53568f244c8594f200ead4e042f29efb55f3be82/chrome/android/chrome_test_java_sources.gni


### ra...@chromium.org (2021-10-28)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-29)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-29)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-11-03)

kickstarting merge-request/review process manually as sheriffbot has been doing this inconsistently since the migration to 4w stable release cycle and extended stable channel (known issue, https://crbug.com/chromium/1262390)

### [Deleted User] (2021-11-03)

Merge review required: M96 is already shipping to beta.

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
Owners: govind (Android), harrysouders (iOS), dgagnon (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2021-11-03)

+Amy (Security TPM) for M96 merge review. Thank you. 

### am...@chromium.org (2021-11-05)

finnur@, since you reviewed this fix would you be willing to take over the above checks (in https://crbug.com/chromium/1259694#c23) and merges since rayankans@ is out until 1 December? Since this is a pretty big fix it would be helpful if someone/you could confirm there have been no stability issues or other concerns since this fix landed on Canary. This is teed up for merge review for 96, which is approaching stable cut Tuesday next week, and having some eyes on before I approve merge would be appreciated. 

Please feel free to suggest someone else if there is a better fit to do this. Thank you! 

### am...@chromium.org (2021-11-08)

beverloo@ finnur@
See above comment, but tl;dr I'm looking for someone to take over review and merges for this issue ASAP. For this fix to be included in the M96 stable cut for release next week, it should be merged by EOD today. Thank you.

### am...@chromium.org (2021-11-08)

I see peter@ is already cc'ed, removing beverloo@ 

### fi...@chromium.org (2021-11-08)

1. Why does your merge fit within the merge criteria for these milestones?

It is fixing a security issue.
 
2. What changes specifically would you like to merge? Please link to Gerrit.

https://chromium-review.googlesource.com/c/chromium/src/+/3226375

3. Have the changes been released and tested on canary?

Yes.

4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?

Not a new feature. 

5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents

n/a

6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

No, it is covered by an automated test.

### gi...@appspot.gserviceaccount.com (2021-11-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/93ca0dccf68c7b23c6370298cfcd136f9db9373f

commit 93ca0dccf68c7b23c6370298cfcd136f9db9373f
Author: Rayan Kanso <rayankans@google.com>
Date: Mon Nov 08 20:49:30 2021

[Contacts] Check the WebContents are still active/valid
before launching picker

(cherry picked from commit 53568f244c8594f200ead4e042f29efb55f3be82)

Bug: 1259694
Change-Id: I75e16c99f4cf64d110067c7cce30d789c0f92808
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3226375
Commit-Queue: Rayan Kanso <rayankans@chromium.org>
Reviewed-by: David Trainor <dtrainor@chromium.org>
Reviewed-by: Finnur Thorarinsson <finnur@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#935851}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3265109
Auto-Submit: Finnur Thorarinsson <finnur@chromium.org>
Reviewed-by: Ted Choc <tedchoc@chromium.org>
Commit-Queue: Ted Choc <tedchoc@chromium.org>
Cr-Commit-Position: refs/branch-heads/4664@{#866}
Cr-Branched-From: 24dc4ee75e01a29d390d43c9c264372a169273a7-refs/heads/main@{#929512}

[modify] https://crrev.com/93ca0dccf68c7b23c6370298cfcd136f9db9373f/components/browser_ui/contacts_picker/android/java/src/org/chromium/components/browser_ui/contacts_picker/ContactsPickerDialogTest.java
[modify] https://crrev.com/93ca0dccf68c7b23c6370298cfcd136f9db9373f/content/browser/contacts/contacts_provider_android.cc
[modify] https://crrev.com/93ca0dccf68c7b23c6370298cfcd136f9db9373f/content/public/android/java/src/org/chromium/content/browser/ContactsDialogHost.java
[modify] https://crrev.com/93ca0dccf68c7b23c6370298cfcd136f9db9373f/content/public/android/java/src/org/chromium/content_public/browser/ContactsPicker.java
[add] https://crrev.com/93ca0dccf68c7b23c6370298cfcd136f9db9373f/chrome/android/javatests/src/org/chromium/chrome/browser/contacts_picker/ContactsPickerLauncherTest.java
[modify] https://crrev.com/93ca0dccf68c7b23c6370298cfcd136f9db9373f/components/browser_ui/contacts_picker/android/BUILD.gn
[modify] https://crrev.com/93ca0dccf68c7b23c6370298cfcd136f9db9373f/chrome/android/chrome_test_java_sources.gni


### am...@google.com (2021-11-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-11-11)

Congratulations, Luan - the VRP Panel has decided to award you $1000 for this report. Thank you for taking the time to report this issue to us. 

### am...@chromium.org (2021-11-11)

[Empty comment from Monorail migration]

### ad...@google.com (2021-11-12)

[Empty comment from Monorail migration]

### am...@google.com (2021-11-18)

[Empty comment from Monorail migration]

### am...@google.com (2021-12-23)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-03)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ml...@google.com (2022-02-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1259694?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/1295508]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057597)*
