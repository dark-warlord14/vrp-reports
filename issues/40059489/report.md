# UAF in ash::HatsDialog::Show

| Field | Value |
|-------|-------|
| **Issue ID** | [40059489](https://issues.chromium.org/issues/40059489) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>HaTS |
| **Platforms** | ChromeOS |
| **Reporter** | et...@gmail.com |
| **Assignee** | ja...@google.com |
| **Created** | 2022-04-27 |
| **Bounty** | $2,000.00 |

## Description

**Steps to reproduce the problem:**

1. apply patch to chromeos  
   
   This is to increase the race time, and it can also block the GetFormattedSiteContext function.

```
diff --git a/chrome/browser/ash/hats/hats_dialog.cc b/chrome/browser/ash/hats/hats_dialog.cc  
index da7f247164c47..5bc8752eb4ca7 100644  
--- a/chrome/browser/ash/hats/hats_dialog.cc  
+++ b/chrome/browser/ash/hats/hats_dialog.cc  
@@ -91,6 +91,7 @@ const std::string KeyEnumToString(DeviceInfoKey key) {  
 std::string HatsDialog::GetFormattedSiteContext(  
     const std::string& user_locale,  
     const base::flat_map<std::string, std::string>& product_specific_data) {  
+  sleep(20);  
   base::flat_map<std::string, std::string> context;  
   
   context[KeyEnumToString(DeviceInfoKey::BROWSER)] =  

```

2. Make sure your chromeos is pre-configured with two login users, refer to my video.
3. out/chromeos/chrome --use-system-clipboard --user-data-dir=/tmp/s289 --login-manager --force-happiness-tracking-system
4. Wait Survey Notification popup, click it, then switch to other login user.

**Problem Description:**

## Root Cause and some notes

[0] The `hats_dialog.get()` raw ptr is posted to a separate sequence

[1] `hats_dialog` may be destroyed in UI when GetFormattedSiteContext runs  

, causing a UAF in HatsDialog::Show callback.

The pattern of this vulnerability is similar to this issue.  

<https://bugs.chromium.org/p/chromium/issues/detail?id=1233975>

```
// static  
std::unique_ptr<HatsDialog> HatsDialog::CreateAndShow(  
    const HatsConfig& hats_config,  
    const base::flat_map<std::string, std::string>& product_specific_data) {  
  LOG(ERROR) << "sakura in HatsDialog::CreateAndShow" << std::endl;  
  DCHECK_CURRENTLY_ON(content::BrowserThread::UI);  
  
  Profile\* profile = ProfileManager::GetActiveUserProfile();  
  std::string user_locale =  
      profile->GetPrefs()->GetString(language::prefs::kApplicationLocale);  
  language::ConvertToActualUILocale(&user_locale);  
  if (!user_locale.length())  
    user_locale = kDefaultProfileLocale;  
  
  std::unique_ptr<HatsDialog> hats_dialog(  
      new HatsDialog(HatsFinchHelper::GetTriggerID(hats_config), profile,  
                     hats_config.histogram_name));  
  
  // Raw pointer is used here since the dialog is owned by the hats  
  // notification controller which lives until the end of the user session. The  
  // dialog will always be closed before that time instant.  
  base::ThreadPool::PostTaskAndReplyWithResult(  
      FROM_HERE, {base::MayBlock(), base::TaskPriority::BEST_EFFORT},  
      base::BindOnce(&GetFormattedSiteContext, user_locale,  
                     product_specific_data),  
      base::BindOnce(&HatsDialog::Show, base::Unretained(hats_dialog.get()))); //[0]  
  
  return hats_dialog;  
}  
  
void HatsDialog::Show(const std::string& site_context) { //[1]  
  DCHECK_CURRENTLY_ON(content::BrowserThread::UI);  
  
  // Link the trigger ID to fetch the correct survey.  
  url_ = std::string(kCrOSHaTSURL) + "?" + site_context +  
         "&trigger=" + trigger_id_;  
  
  chrome::ShowWebDialog(nullptr, ProfileManager::GetActiveUserProfile(), this);  
}  

```

- [0] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ash/hats/hats_dialog.cc;l=186?q=hats_dialog>
- [1] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ash/hats/hats_dialog.cc;l=191?q=hats_dialog>

## Other

### about flag

void HatsUnlockSurveyTrigger::ShowSurveyIfSelected(const AccountId& account\_id,  

AuthMethod method) {  

...  

// Checks prefs to make sure a survey hasn't already been shown to the user  

// this survey cycle, and rolls a die to determine if the survey should be  

// shown.  

if (!impl\_->ShouldShowSurveyToProfile(profile, hats\_config)) { // [0]  

return;  

}

...  

impl\_->ShowSurvey(profile, hats\_config, product\_specific\_data);  

}

`--force-happiness-tracking-system` is not necessary, it is just to pass the [0] check : "Checks prefs to make sure a survey hasn't already been shown to the user this survey cycle, and rolls a die to determine if the survey should be shown."

This is a function that can be triggered without the flag turned on, just to make it easier to reproduce.

### about other case

In addition, I submitted another issue(<https://bugs.chromium.org/p/chromium/issues/detail?id=1319229>), but different from the root cause of this issue, these are two different vulnerabilities, but the scenario triggered by the other vulnerability is hard.

But this vulnerability scenario is easy.

**Additional Comments:**

\*\*Chrome version: \*\* 100.0.4896.127 \*\*Channel: \*\* Not sure

**OS:** Linux

## Attachments

- [repro.mp4](attachments/repro.mp4) (video/mp4, 4.4 MB)
- [asan.log](attachments/asan.log) (text/plain, 24.1 KB)

## Timeline

### dt...@chromium.org (2022-04-27)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-27)

[Empty comment from Monorail migration]

### do...@chromium.org (2022-04-27)

Thanks for the detailed report! I agree there appears to be a bad assumption going on here.

+cclem who recently worked on this file, and other OWNERs for the directory. Can you please follow up on this? I'm setting Severity = High as this is a UaF in the browser process, but mitigated by the interaction required to get to it. Looks to me like this has possibly existed since 87[1]

1. https://source.chromium.org/chromium/chromium/src/+/ce2005851519dabc3458218cd275b56a91a429f2

[Monorail components: UI>Browser>HaTS]

### [Deleted User] (2022-04-27)

[Empty comment from Monorail migration]

### mu...@chromium.org (2022-04-27)

[Empty comment from Monorail migration]

### et...@gmail.com (2022-04-27)

[Comment Deleted]

### et...@gmail.com (2022-04-27)

hello,  can you take a look at this issue and help assign its owner?
https://bugs.chromium.org/p/chromium/issues/detail?id=1319229

This problem was tested during my discovery of this vulnerability.
Even though its scenes are hard, I think it should be fixed together as well.
Thanks :)

### [Deleted User] (2022-04-28)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### et...@gmail.com (2022-05-04)

Is anyone working on this issue? thanks :)

### kh...@chromium.org (2022-05-04)

> Is anyone working on this issue? thanks :)

I'll take a look this week (haven't gotten a chance yet). Updating milestone to M-103 since it's too late for M-100/101/102.

### [Deleted User] (2022-05-11)

cclem: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### kh...@chromium.org (2022-05-11)

Didn't get a chance to take a look last week, but I am still planning to get this working for M-103.

### [Deleted User] (2022-05-26)

khorimoto: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### et...@gmail.com (2022-06-02)

Hi, when will this bug be fixed? Thanks :)

### mu...@chromium.org (2022-06-21)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-26)

We commit ourselves to a 60 day deadline for fixing for high severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### et...@gmail.com (2022-07-01)

I think this will be a correct patch
https://chromium-review.googlesource.com/c/chromium/src/+/3642975
Please when will you apply and fix this vulnerability. thanks :)

### ja...@google.com (2022-07-01)

Kyle is currently OOO and will be back next week.
I know he was looking into testing his change, but that has turned out to be very difficult due to the current architecture.

I'll reach out and suggest we apply the fix ASAP, and I will address the testing issue in a later CL.

### jo...@chromium.org (2022-07-08)

Can we provide an update here? Has the fix gone in?

### ja...@google.com (2022-07-08)

Kyle was OOO this week as well.
He should be back next week, and we can get the change submitted ASAP upon his return.

### et...@gmail.com (2022-07-20)

Are there any plans to release a patch? thanks :)

### [Deleted User] (2022-08-03)

[Empty comment from Monorail migration]

### kh...@chromium.org (2022-08-07)

> Are there any plans to release a patch? thanks :)

Sorry for the long delay. We're aiming to land https://chromium-review.googlesource.com/c/chromium/src/+/3642975 in time for M-106. Thanks!

### et...@gmail.com (2022-09-02)

friendly ping :)
any update?

### mu...@chromium.org (2022-09-02)

Jack's been working on this recently, but the fix has been turning out to be more involved than we expected. Jack, could you provide more details on plans for addressing this?

### gi...@appspot.gserviceaccount.com (2022-09-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/209ccf99e39669294e1d2bfd64e80b714f61d824

commit 209ccf99e39669294e1d2bfd64e80b714f61d824
Author: Jack Shira <jackshira@google.com>
Date: Tue Sep 06 22:06:58 2022

[CrOS HaTS] Fix UAF issue with HatsDialog

When switching users, the current implementation of HatsDialog always
passes in the active user sessions, which may have changed since the
original HaTS notification was clicked. Since the UI context that is
tied to that user may no longer be available, a UAF can occur in this
situation.

This change checks to see if the current user is still the same user
that activated the notification, ensuring that the UI context will
exist before creating the dialog.

It also moves the triggering logic for the HatsDialog into the
HatsNotificationController. This allows the controller to properly
handle the life-cycle of the dialog, and prevents the UAF issue that
originally occurred.

There are three different scenarios that were manually tested:
1. Normal path: The user stays logged in and sees the dialog as
expected.
2. Switch path: The user clicks the notification and switches
to a different account before the dialog is displayed. In this case,
the dialog will not be displayed since a different user is using the
device.
3. Switch back path: The user clicks the notification, switches to a
different account, and then switches back to the original account before
the dialog is displayed. In this case, the dialog is displayed since the
original user has a valid UI context.

These tests were conducted by adding a `sleep(20);` call to the
beginning of `HatsDialog::GetFormattedSiteContext` to allow the tester
time to manually switch between accounts. The following arguments were
supplied to the built chrome binary invocation: `--login-manager --force-happiness-tracking-system --enable-features=HappinessTrackingSystem:prob/1.0/trigger_id/test`

Note: This CL is not unit tested due to the current design of the class,
which does not have a unittest file. A refactor would be required to
add a test, which is tracked by b/232329702.

LOW_COVERAGE_REASON=Only moved logic/tests, did not change tests

Bug: 1320139, 1319229
Change-Id: I73b52623a47a2f63ee961326a59ae94168aff0e9
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3828048
Reviewed-by: Miriam Zimmerman <mutexlox@chromium.org>
Commit-Queue: Jack Shira <jackshira@google.com>
Cr-Commit-Position: refs/heads/main@{#1043675}

[modify] https://crrev.com/209ccf99e39669294e1d2bfd64e80b714f61d824/chrome/browser/ash/hats/hats_dialog.h
[modify] https://crrev.com/209ccf99e39669294e1d2bfd64e80b714f61d824/chrome/browser/ash/hats/hats_notification_controller.cc
[modify] https://crrev.com/209ccf99e39669294e1d2bfd64e80b714f61d824/chrome/browser/ash/hats/hats_notification_controller_unittest.cc
[modify] https://crrev.com/209ccf99e39669294e1d2bfd64e80b714f61d824/chrome/browser/ash/hats/hats_dialog.cc
[modify] https://crrev.com/209ccf99e39669294e1d2bfd64e80b714f61d824/chrome/browser/ash/hats/hats_dialog_unittest.cc
[modify] https://crrev.com/209ccf99e39669294e1d2bfd64e80b714f61d824/chrome/browser/ash/hats/hats_notification_controller.h


### ja...@google.com (2022-09-07)

The above CL fixes the issue described.

### [Deleted User] (2022-09-08)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-08)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-08)

Requesting merge to beta M106 because latest trunk commit (1043675) appears to be after beta branch point (1036826).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-09-08)

Merge review required: M106 is already shipping to beta.

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

### kh...@chromium.org (2022-09-08)

Not attempting a merge to M-106 since we're only a week from stable branch cut.

### jo...@chromium.org (2022-09-19)

It would have been nice to merge this to 106. What was the concern here.

Severity-High bugs, per our SLO, https://chromium.googlesource.com/chromiumos/docs/+/HEAD/security_severity_guidelines.md#slo-matrices, should be merged to the next stable release.

### mu...@google.com (2022-09-19)

I believe that the thinking was that since this bug predated 106, it might not fit into the merge guidelines, especially so late into the release cycle.

### jo...@chromium.org (2022-09-19)

Right, but unfortunately that doesn't match our merge guidelines. The stable cut is tomorrow, we should attempt to merge this.

Security fixes are explicitly included in both phases of merge guidelines (https://g3doc.corp.google.com/company/teams/chromeos/processes/release/merging.md?cl=head).

1-Security fix.
2-https://chromium-review.googlesource.com/c/chromium/src/+/3828048
3-Yes.
4-No.
5-No EngProd necessary for security fixes.
6-No.

### [Deleted User] (2022-09-19)

Merge review required: M106 is already shipping to beta.

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

### mu...@google.com (2022-09-19)

Gotcha, thanks for the request and for filing out the form, Jorge!

### ce...@google.com (2022-09-20)

Merge approved for M106.

Merge category: Security Fix.

### jo...@chromium.org (2022-09-20)

We really need to land this today folks, we're cutting stable today.

### kh...@chromium.org (2022-09-20)

> We really need to land this today folks, we're cutting stable today.

mutexlox@ is working on a merge CL here: https://chromium-review.googlesource.com/c/chromium/src/+/3907835. We're resolving some merge conflicts.

ceb@, note that we also need this CL to be merged as well: https://chromium-review.googlesource.com/c/chromium/src/+/3878226. It accidentally forgot to tag this bug.

### mu...@google.com (2022-09-20)

ceb@: can you please also look at https://chromium-review.googlesource.com/c/chromium/src/+/3878226, which is a similarly important security fix, and see if that's alright to merge? same answers to the survey as in c#35.

### gi...@appspot.gserviceaccount.com (2022-09-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/ad5657079c76674da4598b2c638651d97e3ccfe4

commit ad5657079c76674da4598b2c638651d97e3ccfe4
Author: Jack Shira <jackshira@google.com>
Date: Tue Sep 20 20:37:28 2022

[CrOS HaTS] Fix UAF issue with HatsDialog

When switching users, the current implementation of HatsDialog always
passes in the active user sessions, which may have changed since the
original HaTS notification was clicked. Since the UI context that is
tied to that user may no longer be available, a UAF can occur in this
situation.

This change checks to see if the current user is still the same user
that activated the notification, ensuring that the UI context will
exist before creating the dialog.

It also moves the triggering logic for the HatsDialog into the
HatsNotificationController. This allows the controller to properly
handle the life-cycle of the dialog, and prevents the UAF issue that
originally occurred.

There are three different scenarios that were manually tested:
1. Normal path: The user stays logged in and sees the dialog as
expected.
2. Switch path: The user clicks the notification and switches
to a different account before the dialog is displayed. In this case,
the dialog will not be displayed since a different user is using the
device.
3. Switch back path: The user clicks the notification, switches to a
different account, and then switches back to the original account before
the dialog is displayed. In this case, the dialog is displayed since the
original user has a valid UI context.

These tests were conducted by adding a `sleep(20);` call to the
beginning of `HatsDialog::GetFormattedSiteContext` to allow the tester
time to manually switch between accounts. The following arguments were
supplied to the built chrome binary invocation: `--login-manager --force-happiness-tracking-system --enable-features=HappinessTrackingSystem:prob/1.0/trigger_id/test`

Note: This CL is not unit tested due to the current design of the class,
which does not have a unittest file. A refactor would be required to
add a test, which is tracked by b/232329702.

LOW_COVERAGE_REASON=Only moved logic/tests, did not change tests

(cherry picked from commit 209ccf99e39669294e1d2bfd64e80b714f61d824)

Bug: 1320139, 1319229
Change-Id: I73b52623a47a2f63ee961326a59ae94168aff0e9
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3828048
Reviewed-by: Miriam Zimmerman <mutexlox@chromium.org>
Commit-Queue: Jack Shira <jackshira@google.com>
Cr-Original-Commit-Position: refs/heads/main@{#1043675}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3907835
Auto-Submit: Miriam Zimmerman <mutexlox@chromium.org>
Commit-Queue: Kyle Horimoto <khorimoto@chromium.org>
Reviewed-by: Kyle Horimoto <khorimoto@chromium.org>
Cr-Commit-Position: refs/branch-heads/5249@{#527}
Cr-Branched-From: 4f7bea5de862aaa52e6bde5920755a9ef9db120b-refs/heads/main@{#1036826}

[modify] https://crrev.com/ad5657079c76674da4598b2c638651d97e3ccfe4/chrome/browser/ash/hats/hats_dialog.h
[modify] https://crrev.com/ad5657079c76674da4598b2c638651d97e3ccfe4/chrome/browser/ash/hats/hats_notification_controller_unittest.cc
[modify] https://crrev.com/ad5657079c76674da4598b2c638651d97e3ccfe4/chrome/browser/ash/hats/hats_notification_controller.cc
[modify] https://crrev.com/ad5657079c76674da4598b2c638651d97e3ccfe4/chrome/browser/ash/hats/hats_dialog.cc
[modify] https://crrev.com/ad5657079c76674da4598b2c638651d97e3ccfe4/chrome/browser/ash/hats/hats_dialog_unittest.cc
[modify] https://crrev.com/ad5657079c76674da4598b2c638651d97e3ccfe4/chrome/browser/ash/hats/hats_notification_controller.h


### [Deleted User] (2022-09-20)

LTS Milestone M102

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ce...@google.com (2022-09-20)

Regarding #41, assuming that CL is addressing the same issue in this bug, merge approved for M106. 

If there's a separate tracking bug, please add the Merge-Request-106 label and C/P the questionnaire answers. I'll approve the merge there as well.

### ad...@google.com (2022-09-21)

[Empty comment from Monorail migration]

### rz...@google.com (2022-09-21)

Same fix as https://crbug.com/1319229

### am...@google.com (2022-09-22)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-09-22)

Congratulations! The VRP Panel has decided to award you $2,000 for this report of a highly mitigated security bug (https://g.co/chrome/vrp)! Thank you for your efforts in reporting this issue to us! 

### am...@google.com (2022-09-23)

[Empty comment from Monorail migration]

### rz...@google.com (2022-09-26)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-26)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2022-09-26)

Removed the request, it's being handled on https://crbug.com/1319229

### am...@google.com (2022-09-27)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-10-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/36e00f2c03b59beed3431d15fb390919e31a4057

commit 36e00f2c03b59beed3431d15fb390919e31a4057
Author: Jack Shira <jackshira@google.com>
Date: Wed Oct 19 08:47:48 2022

[M102-LTS][CrOS HaTS] Fix UAF issue with HatsDialog

M102 merge issues:
  chrome/browser/ash/hats/hats_dialog.cc:
    Conflicts with the comments around the removed code
  chrome/browser/ash/hats/hats_notification_controller.h:
    - Include conflicts
  chrome/browser/ash/hats/hats_notification_controller.cc:
    - Include conflicts
    - OnShuttingDown() isn't present in M102

When switching users, the current implementation of HatsDialog always
passes in the active user sessions, which may have changed since the
original HaTS notification was clicked. Since the UI context that is
tied to that user may no longer be available, a UAF can occur in this
situation.

This change checks to see if the current user is still the same user
that activated the notification, ensuring that the UI context will
exist before creating the dialog.

It also moves the triggering logic for the HatsDialog into the
HatsNotificationController. This allows the controller to properly
handle the life-cycle of the dialog, and prevents the UAF issue that
originally occurred.

There are three different scenarios that were manually tested:
1. Normal path: The user stays logged in and sees the dialog as
expected.
2. Switch path: The user clicks the notification and switches
to a different account before the dialog is displayed. In this case,
the dialog will not be displayed since a different user is using the
device.
3. Switch back path: The user clicks the notification, switches to a
different account, and then switches back to the original account before
the dialog is displayed. In this case, the dialog is displayed since the
original user has a valid UI context.

These tests were conducted by adding a `sleep(20);` call to the
beginning of `HatsDialog::GetFormattedSiteContext` to allow the tester
time to manually switch between accounts. The following arguments were
supplied to the built chrome binary invocation: `--login-manager --force-happiness-tracking-system --enable-features=HappinessTrackingSystem:prob/1.0/trigger_id/test`

Note: This CL is not unit tested due to the current design of the class,
which does not have a unittest file. A refactor would be required to
add a test, which is tracked by b/232329702.

LOW_COVERAGE_REASON=Only moved logic/tests, did not change tests

(cherry picked from commit 209ccf99e39669294e1d2bfd64e80b714f61d824)

Bug: 1320139, 1319229
Change-Id: I73b52623a47a2f63ee961326a59ae94168aff0e9
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3828048
Commit-Queue: Jack Shira <jackshira@google.com>
Cr-Original-Commit-Position: refs/heads/main@{#1043675}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3910009
Reviewed-by: Achuith Bhandarkar <achuith@chromium.org>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Owners-Override: Achuith Bhandarkar <achuith@chromium.org>
Cr-Commit-Position: refs/branch-heads/5005@{#1371}
Cr-Branched-From: 5b4d9450fee01f821b6400e947b3839727643a71-refs/heads/main@{#992738}

[modify] https://crrev.com/36e00f2c03b59beed3431d15fb390919e31a4057/chrome/browser/ash/hats/hats_dialog.h
[modify] https://crrev.com/36e00f2c03b59beed3431d15fb390919e31a4057/chrome/browser/ash/hats/hats_notification_controller.cc
[modify] https://crrev.com/36e00f2c03b59beed3431d15fb390919e31a4057/chrome/browser/ash/hats/hats_notification_controller_unittest.cc
[modify] https://crrev.com/36e00f2c03b59beed3431d15fb390919e31a4057/chrome/browser/ash/hats/hats_dialog.cc
[modify] https://crrev.com/36e00f2c03b59beed3431d15fb390919e31a4057/chrome/browser/ash/hats/hats_dialog_unittest.cc
[modify] https://crrev.com/36e00f2c03b59beed3431d15fb390919e31a4057/chrome/browser/ash/hats/hats_notification_controller.h


### rz...@google.com (2022-10-19)

[Empty comment from Monorail migration]

### pg...@google.com (2022-11-01)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-15)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### is...@google.com (2023-05-24)

This issue was migrated from crbug.com/chromium/1320139?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059489)*
