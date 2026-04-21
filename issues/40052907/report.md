# Security: bypas of the protection of input field cache

| Field | Value |
|-------|-------|
| **Issue ID** | [40052907](https://issues.chromium.org/issues/40052907) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Autofill |
| **Reporter** | gc...@gmail.com |
| **Assignee** | ma...@chromium.org |
| **Created** | 2020-07-22 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**  

this is a report to a security vulnerability in google chrome/chromium browser as high-quality report with functional exploit. this vulnerability allows attackers to steal the cache of input fields like usernames, e-mail adresses, telephone numbers from any site like twitter, google and any others.

**VERSION**  

Exploit tested with the following properties:  

Google Chrome (windows) version: 84.0.4147.89 (64bit) + stable  

Chromium (linux) Version: 83.0.4103.61 (64bit) + stable  

Operating System: windows 10 version 1909 and ubuntu 18.04.4

...please note, that this vulnerability is also partially avaible in some other browsers:  

Windows 10 Version 1909:  

Mozilla Firefox (current version) only in full screen (F11)  

Opera Browser (current version) without restriction  

ubuntu (18.04.4):  

Opera Browser (current version) without restriction  

Mozilla Firefox (current version) as a maximized window or in full screen

...please also note, i have not tested apple systems!

**REPRODUCTION CASE**  

i wrote an extensive pdf document (german) and 2 finished exploit codes for you!  

the exploit use a vulnerability in showing of cache of input fields. your browser suggests the saved entries of input fields like safed user logins (username, email, phone number...) or cached search word any similar entered things. all users see that and nobody will send critical information to unknown sites. but this can be hide by full bypassing the visibility of all fields and suggests. in this case nobody are able to notice that they are sending their data to unknown attackers.

attachd files:  

arrows.html (stable - solve a small captcha to get hijacked any cached input of fieldname "username")

arrows-game.html: (experimental - play a little jamp and run game to get hijacked any cached input of fieldname "username")

game-vid.mp4: show a test example with the experimental version of exploit (arrows-game.html) stealing the username from cached input of the login field on twitter

arrows.pdf: extensive pdf document (german) about the vulnerability, how it works...

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

no crashes!

**CREDIT INFORMATION**  

Reporter credit: if u like, u can notice me as "Nadja Ungethuem" from "www.unnex.de"

---

thank you for your attention. with kind regards nadja

## Attachments

- [arrows.html](attachments/arrows.html) (text/plain, 2.7 KB)
- [arrows-game.html](attachments/arrows-game.html) (text/plain, 5.7 KB)
- [game-vid.mp4](attachments/game-vid.mp4) (video/mp4, 2.7 MB)
- [arrows.pdf](attachments/arrows.pdf) (application/pdf, 141.3 KB)

## Timeline

### gc...@gmail.com (2020-07-22)


...just a link to a online example of "arrows.html". it hijack the input-field named "username": http://unnex.de/98013-awe139128y-arrows.html

### aj...@google.com (2020-07-22)

Thanks for the report. CC'd autofill folks, please let me know if this is not considered a security bug.

[Monorail components: UI>Browser>Autofill]

### [Deleted User] (2020-07-23)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-07-23)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aj...@google.com (2020-07-27)

Ping? Any initial thoughts?

### ba...@chromium.org (2020-07-27)

Thank you for the ping. This slipped my inbox. We will investigate tomorrow.

### ba...@chromium.org (2020-07-28)

Mohamed, is this something you could drive and prioritize?

I think the problem is in AutofillPopupViewNativeViews::DoUpdateBoundsAndRedrawPopup().

It tries to fit the popup blow the input element and falls back to "above the input element".

For "above the input element" it check whether there is enough space between the top of the embedding window (not content area) and the top edge of the input element. The interesting point here is that the input element's top edge is below the omnibar.

I think that should suppress the popup unless it's lower edge is not at least a few pixels into the webcontents area and the height of the popup_bounds contains at least one row.

### ba...@chromium.org (2020-07-28)

[Empty comment from Monorail migration]

### ma...@chromium.org (2020-07-28)

I have looked into this.
Dominic's theory looks correct.  I think the top edge of the input element is even above the omnibox (and even outside Chrome Window). The top is set to -100px.  On Mac, the distance above the content area is around 80 pixels.

I will start working on a fix.

### gc...@gmail.com (2020-07-28)

[Comment Deleted]

### gc...@gmail.com (2020-07-28)

that's nice to see, that u spend your time to fix that security vulnerability wich one classified as medium risk.
well, but my most intention to report bugs to google is the bug bounty program and their rewards (especially in the economic crisis also came with corona).
when and where can i find out how my "high-quality report with 2 functional exploits" is rewarded?

### ba...@chromium.org (2020-07-28)

adding reward-topanel for https://crbug.com/chromium/1108181#c11.

### ma...@chromium.org (2020-07-29)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-08-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/6024ffbd6cb21c49bea0095510684be6cf63f2bc

commit 6024ffbd6cb21c49bea0095510684be6cf63f2bc
Author: Mohamed Amir Yosef <mamir@chromium.org>
Date: Tue Aug 04 19:15:49 2020

[Autofill] Introduce AutofillPopupViewDelegate::GetWebContents()

Follow up CL will make use of this API.

Bug: 1108181
Change-Id: I931e2aac81ff5164b129c8556b0bb27d1e15fc6e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2333835
Reviewed-by: Vasilii Sukhanov <vasilii@chromium.org>
Reviewed-by: Evan Stade <estade@chromium.org>
Commit-Queue: Mohamed Amir Yosef <mamir@chromium.org>
Cr-Commit-Position: refs/heads/master@{#794660}

[modify] https://crrev.com/6024ffbd6cb21c49bea0095510684be6cf63f2bc/chrome/browser/autofill/autofill_keyboard_accessory_adapter.cc
[modify] https://crrev.com/6024ffbd6cb21c49bea0095510684be6cf63f2bc/chrome/browser/autofill/autofill_keyboard_accessory_adapter.h
[modify] https://crrev.com/6024ffbd6cb21c49bea0095510684be6cf63f2bc/chrome/browser/autofill/mock_autofill_popup_controller.h
[modify] https://crrev.com/6024ffbd6cb21c49bea0095510684be6cf63f2bc/chrome/browser/ui/autofill/autofill_popup_controller_impl.cc
[modify] https://crrev.com/6024ffbd6cb21c49bea0095510684be6cf63f2bc/chrome/browser/ui/autofill/autofill_popup_controller_impl.h
[modify] https://crrev.com/6024ffbd6cb21c49bea0095510684be6cf63f2bc/chrome/browser/ui/autofill/autofill_popup_view_delegate.h
[modify] https://crrev.com/6024ffbd6cb21c49bea0095510684be6cf63f2bc/chrome/browser/ui/cocoa/touchbar/credit_card_autofill_touch_bar_controller_unittest.mm
[modify] https://crrev.com/6024ffbd6cb21c49bea0095510684be6cf63f2bc/chrome/browser/ui/passwords/password_generation_popup_controller_impl.cc
[modify] https://crrev.com/6024ffbd6cb21c49bea0095510684be6cf63f2bc/chrome/browser/ui/passwords/password_generation_popup_controller_impl.h
[modify] https://crrev.com/6024ffbd6cb21c49bea0095510684be6cf63f2bc/chrome/browser/ui/views/autofill/autofill_popup_base_view_browsertest.cc


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-08-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/6807096dde5351d61424e2e4ffac270d0a0b355f

commit 6807096dde5351d61424e2e4ffac270d0a0b355f
Author: Mohamed Amir Yosef <mamir@chromium.org>
Date: Tue Aug 04 22:52:39 2020

[Autofill] Suppress autofill dropdown when there is insufficient space

Details are in the linked bug.

Bug: 1108181
Change-Id: If32e2aaf7ab5b38d18607813bf0b6a407826e0c2
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2323392
Commit-Queue: Mohamed Amir Yosef <mamir@chromium.org>
Reviewed-by: Evan Stade <estade@chromium.org>
Reviewed-by: Dominic Battré <battre@chromium.org>
Cr-Commit-Position: refs/heads/master@{#794750}

[modify] https://crrev.com/6807096dde5351d61424e2e4ffac270d0a0b355f/chrome/browser/autofill/autofill_interactive_uitest.cc
[modify] https://crrev.com/6807096dde5351d61424e2e4ffac270d0a0b355f/chrome/browser/ui/views/autofill/autofill_popup_base_view.cc
[modify] https://crrev.com/6807096dde5351d61424e2e4ffac270d0a0b355f/chrome/browser/ui/views/autofill/autofill_popup_base_view.h
[modify] https://crrev.com/6807096dde5351d61424e2e4ffac270d0a0b355f/chrome/browser/ui/views/autofill/autofill_popup_view_native_views.cc
[modify] https://crrev.com/6807096dde5351d61424e2e4ffac270d0a0b355f/chrome/browser/ui/views/autofill/autofill_popup_view_native_views.h
[modify] https://crrev.com/6807096dde5351d61424e2e4ffac270d0a0b355f/chrome/browser/ui/views/autofill/autofill_popup_view_utils.cc
[modify] https://crrev.com/6807096dde5351d61424e2e4ffac270d0a0b355f/chrome/browser/ui/views/autofill/autofill_popup_view_utils.h
[modify] https://crrev.com/6807096dde5351d61424e2e4ffac270d0a0b355f/chrome/browser/ui/views/autofill/autofill_popup_view_utils_unittest.cc
[modify] https://crrev.com/6807096dde5351d61424e2e4ffac270d0a0b355f/components/autofill/core/browser/ui/popup_types.h


### ma...@chromium.org (2020-08-04)

[Empty comment from Monorail migration]

### [Deleted User] (2020-08-05)

[Empty comment from Monorail migration]

### [Deleted User] (2020-08-05)

Requesting merge to beta M85 because latest trunk commit (794750) appears to be after beta branch point (782793).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-08-05)

This bug requires manual review: M85's targeted beta branch promotion date has already passed, so this requires manual review
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
Owners: benmason@(Android), bindusuvarna@(iOS), dgagnon@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-08-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/129ff747e0d002ee427574eed8485f71036a7d15

commit 129ff747e0d002ee427574eed8485f71036a7d15
Author: Mohamed Amir Yosef <mamir@chromium.org>
Date: Thu Aug 06 10:38:18 2020

[Autofill] Fix crash in AutofillPopupViewNativeViews

This CL checks body_container_ for nullness.
body_container_ could be null if there are only footer items.

Bug: 1113255,1108181
Change-Id: I9ed145c1d18baf8b13deab8c44cc510b3bb781eb
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2339479
Commit-Queue: Mohamed Amir Yosef <mamir@chromium.org>
Reviewed-by: Evan Stade <estade@chromium.org>
Cr-Commit-Position: refs/heads/master@{#795409}

[modify] https://crrev.com/129ff747e0d002ee427574eed8485f71036a7d15/chrome/browser/ui/views/autofill/autofill_popup_view_native_views.cc
[modify] https://crrev.com/129ff747e0d002ee427574eed8485f71036a7d15/chrome/browser/ui/views/autofill/autofill_popup_view_native_views_unittest.cc


### ma...@chromium.org (2020-08-06)

- This is fixing a P1 security bug.

- I would like to merge the CLs
https://chromium-review.googlesource.com/c/chromium/src/+/2333835
https://chromium-review.googlesource.com/c/chromium/src/+/2323392
https://chromium-review.googlesource.com/c/chromium/src/+/2339479

- The first 2 CLs have been on Canary already for 2 days. The 3rd CL just landed today, it's a crash fix.

- It's NOT a new feature and NOT behind a feature toggle.


### ad...@google.com (2020-08-10)

Approving merge to M85, branch 4183.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-08-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/d6ff8fd2a7a129a48a05df7f329c59d41ee733e7

commit d6ff8fd2a7a129a48a05df7f329c59d41ee733e7
Author: Mohamed Amir Yosef <mamir@chromium.org>
Date: Tue Aug 11 08:23:26 2020

[Autofill] Introduce AutofillPopupViewDelegate::GetWebContents()

Follow up CL will make use of this API.

TBR=estade@chromium.org

(cherry picked from commit 6024ffbd6cb21c49bea0095510684be6cf63f2bc)

Bug: 1108181
Change-Id: I931e2aac81ff5164b129c8556b0bb27d1e15fc6e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2333835
Reviewed-by: Vasilii Sukhanov <vasilii@chromium.org>
Reviewed-by: Evan Stade <estade@chromium.org>
Commit-Queue: Mohamed Amir Yosef <mamir@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#794660}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2346669
Reviewed-by: Mohamed Amir Yosef <mamir@chromium.org>
Cr-Commit-Position: refs/branch-heads/4183@{#1396}
Cr-Branched-From: 740e9e8a40505392ba5c8e022a8024b3d018ca65-refs/heads/master@{#782793}

[modify] https://crrev.com/d6ff8fd2a7a129a48a05df7f329c59d41ee733e7/chrome/browser/autofill/autofill_keyboard_accessory_adapter.cc
[modify] https://crrev.com/d6ff8fd2a7a129a48a05df7f329c59d41ee733e7/chrome/browser/autofill/autofill_keyboard_accessory_adapter.h
[modify] https://crrev.com/d6ff8fd2a7a129a48a05df7f329c59d41ee733e7/chrome/browser/autofill/mock_autofill_popup_controller.h
[modify] https://crrev.com/d6ff8fd2a7a129a48a05df7f329c59d41ee733e7/chrome/browser/ui/autofill/autofill_popup_controller_impl.cc
[modify] https://crrev.com/d6ff8fd2a7a129a48a05df7f329c59d41ee733e7/chrome/browser/ui/autofill/autofill_popup_controller_impl.h
[modify] https://crrev.com/d6ff8fd2a7a129a48a05df7f329c59d41ee733e7/chrome/browser/ui/autofill/autofill_popup_view_delegate.h
[modify] https://crrev.com/d6ff8fd2a7a129a48a05df7f329c59d41ee733e7/chrome/browser/ui/cocoa/touchbar/credit_card_autofill_touch_bar_controller_unittest.mm
[modify] https://crrev.com/d6ff8fd2a7a129a48a05df7f329c59d41ee733e7/chrome/browser/ui/passwords/password_generation_popup_controller_impl.cc
[modify] https://crrev.com/d6ff8fd2a7a129a48a05df7f329c59d41ee733e7/chrome/browser/ui/passwords/password_generation_popup_controller_impl.h
[modify] https://crrev.com/d6ff8fd2a7a129a48a05df7f329c59d41ee733e7/chrome/browser/ui/views/autofill/autofill_popup_base_view_browsertest.cc


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-08-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/65bbe7edda8c9065c9c254ada2da1af7cd5776b6

commit 65bbe7edda8c9065c9c254ada2da1af7cd5776b6
Author: Mohamed Amir Yosef <mamir@chromium.org>
Date: Tue Aug 11 10:46:19 2020

[Autofill] Suppress autofill dropdown when there is insufficient space

Details are in the linked bug.


TBR=estade@chromium.org

(cherry picked from commit 6807096dde5351d61424e2e4ffac270d0a0b355f)

Bug: 1108181
Change-Id: If32e2aaf7ab5b38d18607813bf0b6a407826e0c2
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2323392
Commit-Queue: Mohamed Amir Yosef <mamir@chromium.org>
Reviewed-by: Evan Stade <estade@chromium.org>
Reviewed-by: Dominic Battré <battre@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#794750}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2346353
Reviewed-by: Mohamed Amir Yosef <mamir@chromium.org>
Cr-Commit-Position: refs/branch-heads/4183@{#1399}
Cr-Branched-From: 740e9e8a40505392ba5c8e022a8024b3d018ca65-refs/heads/master@{#782793}

[modify] https://crrev.com/65bbe7edda8c9065c9c254ada2da1af7cd5776b6/chrome/browser/autofill/autofill_interactive_uitest.cc
[modify] https://crrev.com/65bbe7edda8c9065c9c254ada2da1af7cd5776b6/chrome/browser/ui/views/autofill/autofill_popup_base_view.cc
[modify] https://crrev.com/65bbe7edda8c9065c9c254ada2da1af7cd5776b6/chrome/browser/ui/views/autofill/autofill_popup_base_view.h
[modify] https://crrev.com/65bbe7edda8c9065c9c254ada2da1af7cd5776b6/chrome/browser/ui/views/autofill/autofill_popup_view_native_views.cc
[modify] https://crrev.com/65bbe7edda8c9065c9c254ada2da1af7cd5776b6/chrome/browser/ui/views/autofill/autofill_popup_view_native_views.h
[modify] https://crrev.com/65bbe7edda8c9065c9c254ada2da1af7cd5776b6/chrome/browser/ui/views/autofill/autofill_popup_view_utils.cc
[modify] https://crrev.com/65bbe7edda8c9065c9c254ada2da1af7cd5776b6/chrome/browser/ui/views/autofill/autofill_popup_view_utils.h
[modify] https://crrev.com/65bbe7edda8c9065c9c254ada2da1af7cd5776b6/chrome/browser/ui/views/autofill/autofill_popup_view_utils_unittest.cc
[modify] https://crrev.com/65bbe7edda8c9065c9c254ada2da1af7cd5776b6/components/autofill/core/browser/ui/popup_types.h


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-08-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/740bcd69d01c1a5c662cd5bbcb9e8c523e1c040f

commit 740bcd69d01c1a5c662cd5bbcb9e8c523e1c040f
Author: Mohamed Amir Yosef <mamir@chromium.org>
Date: Tue Aug 11 11:37:29 2020

[Autofill] Fix crash in AutofillPopupViewNativeViews

This CL checks body_container_ for nullness.
body_container_ could be null if there are only footer items.

TBR=estade@chromium.org

(cherry picked from commit 129ff747e0d002ee427574eed8485f71036a7d15)

Bug: 1113255,1108181
Change-Id: I9ed145c1d18baf8b13deab8c44cc510b3bb781eb
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2339479
Commit-Queue: Mohamed Amir Yosef <mamir@chromium.org>
Reviewed-by: Evan Stade <estade@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#795409}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2349291
Reviewed-by: Mohamed Amir Yosef <mamir@chromium.org>
Cr-Commit-Position: refs/branch-heads/4183@{#1400}
Cr-Branched-From: 740e9e8a40505392ba5c8e022a8024b3d018ca65-refs/heads/master@{#782793}

[modify] https://crrev.com/740bcd69d01c1a5c662cd5bbcb9e8c523e1c040f/chrome/browser/ui/views/autofill/autofill_popup_view_native_views.cc
[modify] https://crrev.com/740bcd69d01c1a5c662cd5bbcb9e8c523e1c040f/chrome/browser/ui/views/autofill/autofill_popup_view_native_views_unittest.cc


### ad...@google.com (2020-08-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-08-13)

gcunnex@, thanks for the report. The VRP panel has decided to award $5000 here, congratulations! Someone from our finance team will be in touch to arrange payment.

### ad...@google.com (2020-08-13)

[Empty comment from Monorail migration]

### ad...@google.com (2020-08-24)

[Empty comment from Monorail migration]

### ad...@google.com (2020-08-24)

[Empty comment from Monorail migration]

### ad...@google.com (2020-09-21)

[Empty comment from Monorail migration]

### [Deleted User] (2020-11-11)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2020-11-11)

This issue was migrated from crbug.com/chromium/1108181?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40052907)*
