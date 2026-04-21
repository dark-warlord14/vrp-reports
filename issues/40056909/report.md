# Security: UAF in EditAddressProfileView::WindowClosing

| Field | Value |
|-------|-------|
| **Issue ID** | [40056909](https://issues.chromium.org/issues/40056909) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>Autofill |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | jt...@gmail.com |
| **Assignee** | ma...@chromium.org |
| **Created** | 2021-08-18 |
| **Bounty** | $17,000.00 |

## Description

**VULNERABILITY DETAILS**

EditAddressProfileView stores a raw pointer `controller_` to EditAddressProfileDialogControllerImpl. The controller is attached to WebContents and is deleted when the specified WebContents destroyed. However, EditAddressProfileView was not notified when controller being deleted thus a UAF would occur if `controller_` was accessed again.

**REPRODUCTION CASE**

This bug can be triggered without a compromised renderer.  

Steps to reproduce:

1. Setup a HTTPServer  
   
   python -m SimpleHTTPServer 8000
2. Run asan build chrome with the following command  
   
   ./chrome --enable-features=AutofillAddressProfileSavePrompt <http://localhost:8000/poc.html>
3. Click the 'Edit address' icon in the SaveAddress bubble, which shows the EditAddress bubble
4. Close the tab to trigger the UAF

A suggested patch is also attached (fix.diff), which add HideBubble logic similar to AutofillBubbleControllerBase.

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 1.2 KB)
- [asan.log](attachments/asan.log) (text/plain, 26.2 KB)
- [fix.diff](attachments/fix.diff) (text/plain, 3.3 KB)

## Timeline

### [Deleted User] (2021-08-18)

[Empty comment from Monorail migration]

### ad...@google.com (2021-08-21)

[Empty comment from Monorail migration]

[Monorail components: UI>Browser>Autofill]

### ad...@google.com (2021-08-21)

Working on reproducing this.

### ad...@google.com (2021-08-21)

This doesn't reproduce with a Mac ASAN build of 92.0.4506.0 or 95.0.4617.0 (914025). I don't get a SaveAddress bubble at all.

However, I do believe that this class should indeed be a WebContentsObserver (or similar) and without it this class does seem prone to UaF. Therefore I'm going to pass this onto the feature team.

The code in edit_address_profile_view.h doesn't seem to have changed since M92 so setting labels on that basis. As a browser process UaF this would be critical severity, but it's mitigated down to High severity by the need for user interaction.

### [Deleted User] (2021-08-21)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-21)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-08-21)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-08-21)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-01)

mamir: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### do...@chromium.org (2021-09-02)

+battre, can you help get some attention on this?

### ma...@chromium.org (2021-09-02)

It's on my radar!
I have been swamped under work/perf the last two weeks, but I am expecting to look into this very soon!

### ma...@chromium.org (2021-09-02)

[Empty comment from Monorail migration]

### ma...@chromium.org (2021-09-02)

Fix is in review: https://crrev.com/c/3139926

### es...@chromium.org (2021-09-02)

Changing labels snce this requires enabling a feature on the command line (which is still not enabled by default even on trunk). Unless it's enabled by a finch experiment? mamir@ to confirm.

### ma...@chromium.org (2021-09-02)

Good catch!
It's only Canary/Dev at the moment, and Beta will start soon with M94.

### gi...@appspot.gserviceaccount.com (2021-09-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b524be0c56ec35a36eefc9c3b5b8af414ae0f3ab

commit b524be0c56ec35a36eefc9c3b5b8af414ae0f3ab
Author: Mohamed Amir Yosef <mamir@chromium.org>
Date: Fri Sep 03 00:29:16 2021

[Autofill] Fix crash when closing window while address edit dialog open

More details are in the linked bug.

Bug: 1240884
Change-Id: If27c7ac4c5030ee8b96bcc77ee73944992c597cd
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3139926
Commit-Queue: Mohamed Amir Yosef <mamir@chromium.org>
Reviewed-by: Evan Stade <estade@chromium.org>
Cr-Commit-Position: refs/heads/main@{#917903}

[modify] https://crrev.com/b524be0c56ec35a36eefc9c3b5b8af414ae0f3ab/chrome/browser/ui/autofill/edit_address_profile_dialog_controller_impl.cc
[modify] https://crrev.com/b524be0c56ec35a36eefc9c3b5b8af414ae0f3ab/chrome/browser/ui/autofill/edit_address_profile_dialog_controller_impl.h
[add] https://crrev.com/b524be0c56ec35a36eefc9c3b5b8af414ae0f3ab/chrome/browser/ui/autofill/edit_address_profile_dialog_controller_impl_browsertest.cc
[modify] https://crrev.com/b524be0c56ec35a36eefc9c3b5b8af414ae0f3ab/chrome/test/BUILD.gn


### ma...@chromium.org (2021-09-03)

[Empty comment from Monorail migration]

### ma...@chromium.org (2021-09-03)

[Empty comment from Monorail migration]

### ma...@chromium.org (2021-09-03)

[Empty comment from Monorail migration]

### ma...@chromium.org (2021-09-03)

[Empty comment from Monorail migration]

### ma...@chromium.org (2021-09-03)

[Empty comment from Monorail migration]

### ma...@chromium.org (2021-09-03)

Adding FoundIn-94 label since we are planning to launch this with M94

### ma...@chromium.org (2021-09-03)

[Empty comment from Monorail migration]

### ma...@chromium.org (2021-09-03)

1. Does your merge fit within the Merge Decision Guidelines?
 This CL fixes a UAF security bug and does not add new functionality and the fix is rather trivial and covered by newly added tests.

2. Links to the CLs you are requesting to merge.
https://chromium-review.googlesource.com/c/chromium/src/+/3139926

3. Has the change landed and been verified on ToT?
Yes

4. Does this change need to be merged into other active release branches (M-1, M+1)?
No

5. Why are these changes required in this milestone after branch?
The regressions that is associated with a feature that was introduced in M92 surfaced while experimenting.

6. Is this a new feature?
No

7. If it is a new feature, is it behind a flag using finch?
The functionality that is affected by this fix is behind a finch flag.


### sr...@google.com (2021-09-03)

[Empty comment from Monorail migration]

### ma...@chromium.org (2021-09-03)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-09-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/ca78d2eee813eb84b7816580db0aa4087af37564

commit ca78d2eee813eb84b7816580db0aa4087af37564
Author: Mohamed Amir Yosef <mamir@chromium.org>
Date: Fri Sep 03 20:10:07 2021

[Autofill] Fix crash when closing window while address edit dialog open

More details are in the linked bug.

(cherry picked from commit b524be0c56ec35a36eefc9c3b5b8af414ae0f3ab)

Bug: 1240884
Change-Id: If27c7ac4c5030ee8b96bcc77ee73944992c597cd
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3139926
Commit-Queue: Mohamed Amir Yosef <mamir@chromium.org>
Reviewed-by: Evan Stade <estade@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#917903}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3141419
Auto-Submit: Mohamed Amir Yosef <mamir@chromium.org>
Reviewed-by: Elizabeth Popova <lizapopova@google.com>
Reviewed-by: Peter Kasting <pkasting@chromium.org>
Commit-Queue: Peter Kasting <pkasting@chromium.org>
Cr-Commit-Position: refs/branch-heads/4606@{#708}
Cr-Branched-From: 35b0d5a9dc8362adfd44e2614f0d5b7402ef63d0-refs/heads/master@{#911515}

[modify] https://crrev.com/ca78d2eee813eb84b7816580db0aa4087af37564/chrome/browser/ui/autofill/edit_address_profile_dialog_controller_impl.cc
[modify] https://crrev.com/ca78d2eee813eb84b7816580db0aa4087af37564/chrome/browser/ui/autofill/edit_address_profile_dialog_controller_impl.h
[add] https://crrev.com/ca78d2eee813eb84b7816580db0aa4087af37564/chrome/browser/ui/autofill/edit_address_profile_dialog_controller_impl_browsertest.cc
[modify] https://crrev.com/ca78d2eee813eb84b7816580db0aa4087af37564/chrome/test/BUILD.gn


### [Deleted User] (2021-09-04)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-04)

[Empty comment from Monorail migration]

### am...@google.com (2021-09-08)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-09-08)

Congratulations! The VRP Panel has decided to award you $17,000 for this report + patch bonus. Nice work and thank you for this report! 

### am...@google.com (2021-09-09)

[Empty comment from Monorail migration]

### vo...@google.com (2021-10-25)

Marking as not applicable for M90-LTS because the regression was introduced after M90.

### [Deleted User] (2021-12-10)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2021-12-10)

This issue was migrated from crbug.com/chromium/1240884?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40056909)*
