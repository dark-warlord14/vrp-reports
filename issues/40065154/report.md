# Security: UAF in AutofillSnackbarController

| Field | Value |
|-------|-------|
| **Issue ID** | [40065154](https://issues.chromium.org/issues/40065154) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | UI>Browser>Autofill>Payments |
| **Platforms** | Android |
| **Reporter** | jt...@gmail.com |
| **Assignee** | si...@google.com |
| **Created** | 2023-06-01 |
| **Bounty** | $20,000.00 |

## Description

**VULNERABILITY DETAILS**  

If user accepts a virtual credit card suggestion for autofill, ChromeAutofillClient::OnVirtualCardDataAvailable is called after the credit card info was fetched. On android platform, it then calls AutofillSnackbarControllerImpl::Show to show the virtual card snackbar [1]. The problem is that AutofillSnackbarControllerImpl::Show does not check whether there is already a snackbar view. Consider the following scenario:

1. While the first snackbar is showing, the second call to AutofillSnackbarControllerImpl::Show would create another java instance of AutofillSnackbarController at line [2]. Thus there would be two AutofillSnackbarController objects and both of them have a member variable `mNativeAutofillSnackbarView` which is a raw pointer pointing to the same c++ object AutofillSnackbarViewAndroid [3].
2. The first snackbar would be dismissed due to timeout, and it would notify AutofillSnackbarViewAndroid through its java method onDismissNoAction. It then calls AutofillSnackbarViewAndroid::OnDismissed and would destroy AutofillSnackbarViewAndroid at line [4].
3. The second snackbar also be dismissed due to timeout (or perform any action on it), and a UAF would occur when the java object tries to invoke the JNI function and access the already freed AutofillSnackbarViewAndroid.

bisect: This was introduced in <https://chromium.googlesource.com/chromium/src/+/c22f6fd19ba72cb2d6a3e54a47b3afeaa4956da7>

[1] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/autofill/chrome_autofill_client.cc;l=978;drc=66941d1f0cfe9155b400aef887fe39a403c1f518>  

[2] <https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:chrome/browser/ui/android/autofill/snackbar/autofill_snackbar_view_android.cc;l=39;drc=66941d1f0cfe9155b400aef887fe39a403c1f518>  

[3] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/android/java/src/org/chromium/chrome/browser/autofill/AutofillSnackbarController.java;l=25;drc=66941d1f0cfe9155b400aef887fe39a403c1f518>  

[4] <https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:chrome/browser/ui/android/autofill/snackbar/autofill_snackbar_view_android.cc;l=64;drc=66941d1f0cfe9155b400aef887fe39a403c1f518>

**VERSION**  

Chrome Version: stable + dev  

Operating System: Android

**REPRODUCTION CASE**

1. Apply the attached browser.diff patch, this is to add an enrolled virtual card and disable the security connection check(https) in autofill, for the convenience of reproduction in the local asan environment.
2. Host poc.html at localhost  
   
   python3 -m http.server 8000  
   
   adb reverse tcp:8000 tcp:8000
3. Launch chromium and navigate to <http://localhost:8000/poc.html>
4. Use the virtual card for autofill twice

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: browser  

Crash State: see asan.log for stack trace

## Attachments

- [patch.diff](attachments/patch.diff) (text/plain, 4.6 KB)
- [poc.html](attachments/poc.html) (text/plain, 791 B)
- [asan.log](attachments/asan.log) (text/plain, 12.1 KB)

## Timeline

### [Deleted User] (2023-06-01)

[Empty comment from Monorail migration]

### jt...@gmail.com (2023-06-01)

[Comment Deleted]

### ct...@chromium.org (2023-06-01)

Thank you for the detailed report!

Assigning to vinnypersky@ based on your bisect information and cc'ing schwering@.

This is a UAF in the browser process, so I am conservatively setting this as Severity-Critical. This does require some user interaction, but the interaction seems like something a typical user would do on a page or could be convinced to do by an attacker-controlled shopping cart UI (for example, get the user to try to check out and trigger this once, then hide the previous CC input and ask them to re-enter it, triggering this UAF). (Per our severity guidelines, more involved user interaction can downgrade severity one level, and "very unlikely interactions" can be treated as functional bugs [1].)

[1]: https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md

[Monorail components: UI>Browser>Autofill>Payments]

### [Deleted User] (2023-06-01)

[Empty comment from Monorail migration]

### vi...@google.com (2023-06-01)

Thanks for the report! Redirecting this bug to our android expert, Sid. 

### si...@google.com (2023-06-01)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-02)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### si...@google.com (2023-06-02)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-06-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/721bef843b216bd9bcd57f671112c8a0f449a3ae

commit 721bef843b216bd9bcd57f671112c8a0f449a3ae
Author: siashah <siashah@chromium.org>
Date: Mon Jun 05 17:52:13 2023

Do not show a snackbar if already showing one

This is a temporary fix and in the future we would overwrite the
dismiss the currently showing snackbar and show the new one with proper
garbage collection. crbug.com/1450942

Bug: 1450568
Change-Id: I064d76eccc06c6e23fcde9fd1122e87068ffa1c5
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4583539
Reviewed-by: Christoph Schwering <schwering@google.com>
Commit-Queue: Siddharth Shah <siashah@chromium.org>
Reviewed-by: Vinny Persky <vinnypersky@google.com>
Cr-Commit-Position: refs/heads/main@{#1153332}

[modify] https://crrev.com/721bef843b216bd9bcd57f671112c8a0f449a3ae/chrome/browser/ui/autofill/payments/autofill_snackbar_controller_impl.cc
[modify] https://crrev.com/721bef843b216bd9bcd57f671112c8a0f449a3ae/chrome/browser/ui/autofill/payments/autofill_snackbar_controller_impl.h
[modify] https://crrev.com/721bef843b216bd9bcd57f671112c8a0f449a3ae/chrome/browser/ui/autofill/payments/autofill_snackbar_controller_impl_unittest.cc


### si...@google.com (2023-06-06)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-06)

Merge review required: M114 is already shipping to stable.

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

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### si...@google.com (2023-06-06)

1. Why does your merge fit within the merge criteria for these milestones?
Security bug

2. What changes specifically would you like to merge? Please link to Gerrit.
https://chromium-review.googlesource.com/c/chromium/src/+/4583539

3. Have the changes been released and tested on canary?
Yes

4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
This is a bugfix and it is not behind a Finch flag

6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.
Verified manually in Canary. 

### am...@chromium.org (2023-06-06)

hello siashah@ thank you for landing this fix! As per security merge triage processes, please simply update the bug as Fixed once the fix CL has been landed. This will allow the automation to add the appropriate labels and request appropriate merges based on severity and impact. As this fix was landed on 116, it will also need to be merge reviewed for backmerge to 115, so I've added that label accordingly.
Since this fix just landed yesterday, I'll revisit tomorrow for merge review after a bit more bake time on canary. TY! 

### [Deleted User] (2023-06-07)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-07)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-06-08)

115 and 114 merge approved for https://chromium-review.googlesource.com/c/chromium/src/+/4583539
please merge to branches 5790 and 5735 respectively by EOD tomorrow (Friday 9 June) so this fix can be included included in the next M114/Stable and M115/Beta updates 

### gi...@appspot.gserviceaccount.com (2023-06-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/ec1c6f256e1d7f82abdcffac78f926f109e4df93

commit ec1c6f256e1d7f82abdcffac78f926f109e4df93
Author: siashah <siashah@chromium.org>
Date: Thu Jun 08 20:24:43 2023

Do not show a snackbar if already showing one

This is a temporary fix and in the future we would overwrite the
dismiss the currently showing snackbar and show the new one with proper
garbage collection. crbug.com/1450942

(cherry picked from commit 721bef843b216bd9bcd57f671112c8a0f449a3ae)

Bug: 1450568
Change-Id: I064d76eccc06c6e23fcde9fd1122e87068ffa1c5
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4583539
Reviewed-by: Christoph Schwering <schwering@google.com>
Commit-Queue: Siddharth Shah <siashah@chromium.org>
Reviewed-by: Vinny Persky <vinnypersky@google.com>
Cr-Original-Commit-Position: refs/heads/main@{#1153332}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4601968
Cr-Commit-Position: refs/branch-heads/5735@{#1207}
Cr-Branched-From: 2f562e4ddbaf79a3f3cb338b4d1bd4398d49eb67-refs/heads/main@{#1135570}

[modify] https://crrev.com/ec1c6f256e1d7f82abdcffac78f926f109e4df93/chrome/browser/ui/autofill/payments/autofill_snackbar_controller_impl.cc
[modify] https://crrev.com/ec1c6f256e1d7f82abdcffac78f926f109e4df93/chrome/browser/ui/autofill/payments/autofill_snackbar_controller_impl_unittest.cc
[modify] https://crrev.com/ec1c6f256e1d7f82abdcffac78f926f109e4df93/chrome/browser/ui/autofill/payments/autofill_snackbar_controller_impl.h


### gi...@appspot.gserviceaccount.com (2023-06-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/39dc7b949d0ffc704ef3debe3c79b4c4b9082cb8

commit 39dc7b949d0ffc704ef3debe3c79b4c4b9082cb8
Author: siashah <siashah@chromium.org>
Date: Thu Jun 08 20:26:04 2023

Do not show a snackbar if already showing one

This is a temporary fix and in the future we would overwrite the
dismiss the currently showing snackbar and show the new one with proper
garbage collection. crbug.com/1450942

(cherry picked from commit 721bef843b216bd9bcd57f671112c8a0f449a3ae)

Bug: 1450568
Change-Id: I064d76eccc06c6e23fcde9fd1122e87068ffa1c5
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4583539
Reviewed-by: Christoph Schwering <schwering@google.com>
Commit-Queue: Siddharth Shah <siashah@chromium.org>
Reviewed-by: Vinny Persky <vinnypersky@google.com>
Cr-Original-Commit-Position: refs/heads/main@{#1153332}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4599286
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/5790@{#499}
Cr-Branched-From: 1d71a337b1f6e707a13ae074dca1e2c34905eb9f-refs/heads/main@{#1148114}

[modify] https://crrev.com/39dc7b949d0ffc704ef3debe3c79b4c4b9082cb8/chrome/browser/ui/autofill/payments/autofill_snackbar_controller_impl.cc
[modify] https://crrev.com/39dc7b949d0ffc704ef3debe3c79b4c4b9082cb8/chrome/browser/ui/autofill/payments/autofill_snackbar_controller_impl_unittest.cc
[modify] https://crrev.com/39dc7b949d0ffc704ef3debe3c79b4c4b9082cb8/chrome/browser/ui/autofill/payments/autofill_snackbar_controller_impl.h


### am...@chromium.org (2023-06-12)

[Empty comment from Monorail migration]

### am...@google.com (2023-06-13)

[Empty comment from Monorail migration]

### pg...@google.com (2023-06-13)

[Empty comment from Monorail migration]

### am...@google.com (2023-06-16)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-06-16)

Congratulations, Rong Jian! The VRP Panel has decided to award you $20,000 for this report + $1,000 bisect bonus. Thank you for your efforts and reporting this issue to us -- nice work! 

### am...@google.com (2023-06-17)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-13)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1450568?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40065154)*
