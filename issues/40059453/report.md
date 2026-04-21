# UAF in ash::HatsDialog

| Field | Value |
|-------|-------|
| **Issue ID** | [40059453](https://issues.chromium.org/issues/40059453) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>HaTS |
| **Platforms** | ChromeOS |
| **Reporter** | et...@gmail.com |
| **Assignee** | ja...@google.com |
| **Created** | 2022-04-24 |
| **Bounty** | $3,000.00 |

## Description

**Steps to reproduce the problem:**  

1.Download chromeos from <https://commondatastorage.googleapis.com/chromium-browser-asan/index.html?prefix=linux-release-chromeos/asan-linux-release-995100>  

2. rm -rf ./chromeos1 && './linux-release-chromeos\_asan-linux-release-995100/asan-linux-release-995100/chrome' --use-system-clipboard --user-data-dir=./chromeos1 --force-happiness-tracking-system  

3. lock and unlock, and then Survey Notification will popup, click it.  

4. close chromeos

**Problem Description:**  

==411652==ERROR: AddressSanitizer: heap-use-after-free on address 0x60800006ce20 at pc 0x7fd76c9776b7 bp 0x7ffc1fb037b0 sp 0x7ffc1fb037a8  

READ of size 8 at 0x60800006ce20 thread T0 (chrome)  

#0 0x7fd76c9776b6 in GetWindowName ui/views/controls/webview/web\_dialog\_view.cc:202:23  

#1 0x7fd76c9776b6 in non-virtual thunk to views::WebDialogView::GetWindowName()  

#2 0x7fd79ce4d890 in views::WidgetDelegate::ShouldSaveWindowPlacement()  

#3 0x7fd79ce3bfcb in views::Widget::SaveWindowPlacement()  

#4 0x7fd79ce41878 in views::Widget::OnNativeWidgetActivationChanged(bool)  

#5 0x7fd79ceafd95 in views::NativeWidgetAura::OnWindowActivated(wm::ActivationChangeObserver::ActivationReason, aura::Window\*, aura::Window\*)  

#6 0x7fd79c79ff55 in wm::FocusController::SetActiveWindow(wm::ActivationChangeObserver::ActivationReason, aura::Window\*, aura::Window\*, bool)  

#7 0x7fd79c79d9fc in wm::FocusController::FocusAndActivateWindow(wm::ActivationChangeObserver::ActivationReason, aura::Window\*, bool)  

#8 0x7fd7992918ca in ash::Shell::~Shell()  

#9 0x7fd799299d51 in ash::Shell::~Shell()  

#10 0x562558a93920 in operator()  

#11 0x562558a93920 in std::\_\_Cr::unique\_ptr<AshShellInit, std::\_\_Cr::default\_delete<AshShellInit> >::reset(AshShellInit\*)  

#12 0x562558a934e9 in ChromeBrowserMainExtraPartsAsh::PostMainMessageLoopRun()  

#13 0x562552c528f6 in ChromeBrowserMainParts::PostMainMessageLoopRun()  

#14 0x56254fc17dd5 in ash::ChromeBrowserMainPartsAsh::PostMainMessageLoopRun()  

#15 0x7fd78afe03ab in content::BrowserMainLoop::ShutdownThreadsAndCleanUp()  

#16 0x7fd78afe551d in content::BrowserMainRunnerImpl::Shutdown()

0x60800006ce20 is located 0 bytes inside of 96-byte region [0x60800006ce20,0x60800006ce80)  

freed by thread T0 (chrome) here:  

#0 0x56254b7c8f4d in operator delete(void\*)  

#1 0x56254ffc0dde in operator() buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:54:5  

#2 0x56254ffc0dde in reset buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:315:7  

#3 0x56254ffc0dde in ~unique\_ptr buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:269:19  

#4 0x56254ffc0dde in ash::HatsNotificationController::~HatsNotificationController() chrome/browser/ash/hats/hats\_notification\_controller.cc:125:1  

#5 0x56254ffc10e9 in ash::HatsNotificationController::~HatsNotificationController() chrome/browser/ash/hats/hats\_notification\_controller.cc:118:59  

...  

#24 0x7fd78afe551d in content::BrowserMainRunnerImpl::Shutdown() content/browser/browser\_main\_runner\_impl.cc:184:17

previously allocated by thread T0 (chrome) here:  

#0 0x56254b7c86ed in operator new(unsigned long) /b/s/w/ir/cache/builder/src/third\_party/llvm/compiler-rt/lib/asan/asan\_new\_delete.cpp:95:3  

#1 0x56254ffbaa20 in ash::HatsDialog::CreateAndShow(ash::HatsConfig const&, base::flat\_map<std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char> >, std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char> >, std::\_\_Cr::less<void>, std::\_\_Cr::vector<std::\_\_Cr::pair<std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char> >, std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char> > >, std::\_\_Cr::allocator<std::\_\_Cr::pair<std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char> >, std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char> > > > > > const&) chrome/browser/ash/hats/hats\_dialog.cc:177:7  

#2 0x56254ffc2512 in ash::HatsNotificationController::Click(absl::optional<int> const&, absl::optional<std::\_\_Cr::basic\_string<char16\_t, std::\_\_Cr::char\_traits<char16\_t>, std::\_\_Cr::allocator<char16\_t> > > const&) chrome/browser/ash/hats/hats\_notification\_controller.cc:214:7  

#3 0x5625539f3f80 in NotificationPlatformBridgeChromeOs::HandleNotificationClicked(std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char> > const&) chrome/browser/notifications/notification\_platform\_bridge\_chromeos.cc:141:46  

#4 0x7fd79d5d0a20 in message\_center::MessageCenterImpl::ClickOnNotificationUnlocked(std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char> > const&, absl::optional<int> const&, absl::optional<std::\_\_Cr::basic\_string<char16\_t, std::\_\_Cr::char\_traits<char16\_t>, std::\_\_Cr::allocator<char16\_t> > > const&) ui/message\_center/message\_center\_impl.cc:467:15  

...

SUMMARY: AddressSanitizer: heap-use-after-free ui/views/controls/webview/web\_dialog\_view.cc:202:23 in GetWindowName

**Additional Comments:**

\*\*Chrome version: \*\* 100.0.4896.127 \*\*Channel: \*\* Stable

**OS:** Chrome OS

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 16.9 KB)
- [repro.mp4](attachments/repro.mp4) (video/mp4, 3.8 MB)
- [temp.png](attachments/temp.png) (image/png, 184.1 KB)

## Timeline

### et...@gmail.com (2022-04-24)

void HatsUnlockSurveyTrigger::ShowSurveyIfSelected(const AccountId& account_id,
                                                   AuthMethod method) {
   ...
  // Checks prefs to make sure a survey hasn't already been shown to the user
  // this survey cycle, and rolls a die to determine if the survey should be
  // shown.
  if (!impl_->ShouldShowSurveyToProfile(profile, hats_config)) { // [0]
    return;
  }

  ...
  impl_->ShowSurvey(profile, hats_config, product_specific_data);
}

`--force-happiness-tracking-system` is not necessary, it is just to pass the [0] check : "Checks prefs to make sure a survey hasn't already been shown to the user this survey cycle, and rolls a die to determine if the survey should be shown."

This is a function that can be triggered without the flag turned on, just to make it easier to reproduce.

### et...@gmail.com (2022-04-24)

smartlocker is only one of the paths of the HatsNotificationController constructor, but it can also be triggered from other paths.

### et...@gmail.com (2022-04-25)

Can anyone help confirm this issue, thanks :)

### do...@chromium.org (2022-04-28)

+HaTs folks, PTAL.

[Monorail components: UI>Browser>HaTS]

### [Deleted User] (2022-04-28)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-28)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-28)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### kh...@chromium.org (2022-04-28)

dannyrangel@, can you please take a look? The assumption from [1] is incorrect -- we shouldn't assume that the HatsDialog will not have been deleted by the time that the callback returns.

[1] https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ash/hats/hats_dialog.cc;l=179-186;drc=7f3bd3d40fffacda522b97ddfa94085a35d0a0c9

### [Deleted User] (2022-04-28)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### kh...@chromium.org (2022-04-28)

[Empty comment from Monorail migration]

### al...@google.com (2022-05-02)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-13)

khorimoto: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### kh...@chromium.org (2022-05-13)

SLO update: CL is in review (https://chromium-review.googlesource.com/c/chromium/src/+/3642975), but I'm still working on testing it.

### [Deleted User] (2022-05-25)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-29)

khorimoto: Uh oh! This issue still open and hasn't been updated in the last 15 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### et...@gmail.com (2022-06-20)

I noticed that M103 is about to be released, is anyone working on fixing this bug?


### mu...@chromium.org (2022-06-21)

Jack, were you going to take this?

### ja...@google.com (2022-06-21)

Roger, I will look into this. Thanks!

### [Deleted User] (2022-06-23)

We commit ourselves to a 60 day deadline for fixing for high severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jo...@chromium.org (2022-07-08)

Any updates here Jack?

### ja...@google.com (2022-07-08)

Kyle has a CL that addresses this, and he should be back next week.
Hopefully we can get it submitted ASAP when he returns.

https://chromium-review.googlesource.com/c/chromium/src/+/3642975

Also, I'm looking into making this change more testable, but that can be resolved in a followup CL.

### et...@gmail.com (2022-08-03)

hi, any update? thanks

### [Deleted User] (2022-08-03)

[Empty comment from Monorail migration]

### kh...@chromium.org (2022-08-07)

> hi, any update? thanks

Sorry for the long delay. We're aiming to land https://chromium-review.googlesource.com/c/chromium/src/+/3642975 in time for M-106. Thanks!

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

We just landed a fix for this with the above CL and this one: https://crrev.com/c/3878226

### ja...@google.com (2022-09-07)

[Empty comment from Monorail migration]

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

It would have been nice to merge this to 106. What was the concern here?

### et...@gmail.com (2022-09-20)

Hi, I think this issue should also be merged to 106.


### et...@gmail.com (2022-09-20)

Also I noticed that there are two commits for HatsDialog.
https://chromium-review.googlesource.com/c/chromium/src/+/3878226
https://chromium-review.googlesource.com/c/chromium/src/+/3828048

But both https://bugs.chromium.org/p/chromium/issues/detail?id=1320139 and this issue(1319229) only link to https://chromium-review.googlesource.com/c/chromium/src/+/3828048 .

I'm not sure if there is something wrong with this?

### jo...@chromium.org (2022-09-20)

It's the same CL that fixes this and https://crbug.com/chromium/1320139, so we requested the merge in https://crbug.com/chromium/1320139.

### et...@gmail.com (2022-09-20)

According to the description, I think https://chromium-review.googlesource.com/c/chromium/src/+/3878226 is the patch to fix this issue, not https://chromium-review.googlesource.com/c/chromium/src/+/3828048

### et...@gmail.com (2022-09-20)

I report two different UAFs for the same function with different root causes.
I think https://crbug.com/chromium/1319229#c25 gives the wrong patch, please read https://chromium-review.googlesource.com/c/chromium/src/+/3878226，it is correct.

### et...@gmail.com (2022-09-20)

So I think you also need to update the patch of this issue and merge this issue, thanks :)


### et...@gmail.com (2022-09-20)

Although https://chromium-review.googlesource.com/c/chromium/src/+/3878226 does not correctly specify the issue id, from the commit description, it is clear that this vulnerability is fixed.

### et...@gmail.com (2022-09-20)

https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ash/hats/hats_dialog.cc;l=91;bpv=1
I read the blame history for this file and I think so. Let me know if I'm wrong :)

### am...@chromium.org (2022-09-20)

Hello, OP, the merge for https://crrev.com/c/3878226 is being handled and discussed on https://crbug.com/chromium/1320139. :) 

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

### mu...@google.com (2022-09-20)

> 1. Was this issue a regression for the milestone it was found in?

This is a long-standing issue since at least M100. M-102 is definitely affected.

> 2. Is this issue related to a change or feature merged after the latest LTS Milestone?

I don't believe so.

### ad...@google.com (2022-09-21)

[Empty comment from Monorail migration]

### rz...@google.com (2022-09-21)

[Empty comment from Monorail migration]

### rz...@google.com (2022-09-22)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-22)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2022-09-22)

1. Just https://crrev.com/c/3910009
2. Low, only simple conflicts with includes and missing functions
3. 106
4. Yes

### gm...@google.com (2022-09-22)

[Empty comment from Monorail migration]

### mu...@google.com (2022-09-22)

> 1. Just https://crrev.com/c/3910009

Also  https://crrev.com/c/3878226; there are two CLs as part of this fix.

### am...@google.com (2022-09-22)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-09-22)

Congratulations! The VRP Panel has decided to award you $3,000 for this report of the moderately mitigated security bug (https://g.co/chrome/vrp). Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2022-09-23)

[Empty comment from Monorail migration]

### am...@google.com (2022-09-27)

[Empty comment from Monorail migration]

### gm...@google.com (2022-10-18)

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

This issue was migrated from crbug.com/chromium/1319229?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059453)*
