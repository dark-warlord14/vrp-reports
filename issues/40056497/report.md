# Feedback WebUIDialog does not observe Profile lifetime

| Field | Value |
|-------|-------|
| **Issue ID** | [40056497](https://issues.chromium.org/issues/40056497) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Profiles, UI>Browser>ReportAnIssue |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | wx...@gmail.com |
| **Assignee** | ni...@chromium.org |
| **Created** | 2021-07-12 |
| **Bounty** | $5,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36

Steps to reproduce the problem:
- lanch chrome
- open a feedback window
- open guest profile window
- close the browsing windows
- right click the feedback window picture

my chromium version is c67cc106efe1964c5d589b88badf67aa512a2649

What is the expected behavior?

What went wrong?
browser crashes

Did this work before? N/A 

Chrome version: 91.0.4472.124  Channel: n/a
OS Version: 10.0

## Attachments

- [uaf.txt](attachments/uaf.txt) (text/plain, 21.1 KB)
- [poc.mp4](attachments/poc.mp4) (video/mp4, 9.6 MB)
- [Screenshot 2021-08-03 at 09.29.29.png](attachments/Screenshot 2021-08-03 at 09.29.29.png) (image/png, 206.6 KB)

## Timeline

### [Deleted User] (2021-07-12)

[Empty comment from Monorail migration]

### wx...@gmail.com (2021-07-12)

[Empty comment from Monorail migration]

### wx...@gmail.com (2021-07-12)

[Comment Deleted]

### wx...@gmail.com (2021-07-12)

My chromium version is c67cc106efe1964c5d589b88badf67aa512a2649

### rs...@chromium.org (2021-07-12)

These are all related to DestroyOriginalProfileNow(), as filed per request in https://crbug.com/chromium/1227691.

I’m triaging all of these the same; please feel free to dupe/reassign as needed. Some of these seem like they may have the same underlying root cause.

Also, the reporter says that these are from M91, but in https://crbug.com/chromium/1227691, it was said that the DestroyProfileOnBrowserClose experiment wasn’t launched to stable.

[Monorail components: UI>Browser>Profiles]

### [Deleted User] (2021-07-13)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jd...@chromium.org (2021-07-14)

[Empty comment from Monorail migration]

### [Deleted User] (2021-07-14)

[Empty comment from Monorail migration]

### [Deleted User] (2021-07-15)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### do...@chromium.org (2021-07-24)

[Empty comment from Monorail migration]

### do...@chromium.org (2021-07-24)

Bringing together about 5-6 bugs into this one as it was the earliest report (that I currently know about)

Can I ask relevant folks here (Feedback app team, Profile team) to help identify the right approach to addressing this. Should:

1) something in Profile signal to all open windows attached to that profile when it's closing and therefore the windows should close?
2) all windows belonging to a profile ensure they observe that profile's lifecycle events and close themselves when the profile is deleted
3) if (2), should ShowWebDialog do this automatically for all of its consumers

Context and stacktrace:

Chrome Version: c09c0792bb28a3a186c2f1efbabc34a7417d4a49
Lacros Version (if applicable): (copy from chrome://version)
OS: Linux

What steps will reproduce the problem?
(1) Open Chromium and click Experiments icon > Send Feedback
(2) Open a guest profile (or any other profile)
(3) Close the original profile window without closing the feedback window

What is the expected result?
Either the Feedback window is closed or the browser context is not destroyed.

What happens instead?
Browser crashes with the DCHECK below. Without DCHECKs any interaction with the feedback window (e.g., clicking on a link) causes a crash. It appears that browser dialogs expect the browser context to be alive as long as the dialog lives but it does not appear to be the case: https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/browser_dialogs.h;l=101;drc=23ee32391a2364af6e4ed7573f4b2d2e380e441b


1580073:1580073:0723/083643.526694:FATAL:browser_context_impl.cc(88)] Check failed: false. rph_with_bc_reference : {  pl='{ chrome://feedback/ }' lsn=2 }
#0 0x7f2af91ea379 base::debug::CollectStackTrace()
#1 0x7f2af90e6063 base::debug::StackTrace::StackTrace()
#2 0x7f2af91074d4 logging::LogMessage::~LogMessage()
#3 0x7f2af9107f1e logging::LogMessage::~LogMessage()
#4 0x7f2af5cd7d89 content::BrowserContext::Impl::~Impl()
#5 0x7f2af5cd55a7 content::BrowserContext::~BrowserContext()
#6 0x555cca1e6153 Profile::~Profile()
#7 0x555cca7fd9e5 ProfileImpl::~ProfileImpl()
#8 0x555cca7fda0e ProfileImpl::~ProfileImpl()
#9 0x555cca800314 ProfileDestroyer::DestroyOriginalProfileNow()
#10 0x555cca7fff93 ProfileDestroyer::DestroyProfileWhenAppropriate()
#11 0x555cca81b833 ProfileManager::ProfileInfo::~ProfileInfo()
#12 0x555cca81ecc2 std::__Cr::__tree<>::erase()
#13 0x555cca81a553 ProfileManager::RemoveProfile()
#14 0x555cca81a41a ProfileManager::DeleteProfileIfNoKeepAlive()
#15 0x555cca81a0a3 ProfileManager::RemoveKeepAlive()
#16 0x555cca822d2e ScopedProfileKeepAlive::RemoveKeepAliveOnUIThread()
#17 0x7f2af917d49d base::TaskAnnotator::RunTask()
#18 0x7f2af919f66e base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl()
#19 0x7f2af919edcb base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()
#20 0x7f2af919fcb2 base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()
#21 0x7f2af911660f base::MessagePumpGlib::Run()
#22 0x7f2af91a021b base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run()
#23 0x7f2af9151350 base::RunLoop::Run()
#24 0x7f2af5cefdc6 content::BrowserMainLoop::RunMainMessageLoop()
#25 0x7f2af5cf1ac2 content::BrowserMainRunnerImpl::Run()
#26 0x7f2af5ced1a7 content::BrowserMain()
#27 0x7f2af67c02e1 content::ContentMainRunnerImpl::RunBrowser()
#28 0x7f2af67bfc6f content::ContentMainRunnerImpl::Run()
#29 0x7f2af67bd2aa content::RunContentProcess()
#30 0x7f2af67bdd1e content::ContentMain()
#31 0x555cc9abac1e ChromeMain
#32 0x7f2ae781ad0a __libc_start_main
#33 0x555cc9abaa3a _start
Task trace:
#0 0x555cca822c1a ScopedProfileKeepAlive::~ScopedProfileKeepAlive()
#1 0x7f2af144424a views::DesktopWindowTreeHostPlatform::Close()
#2 0x555ccbb2a275 Browser::TabStripEmpty()
#3 0x7f2af766beed IPC::(anonymous namespace)::ChannelAssociatedGroupController::Accept()
#4 0x7f2af89de49f mojo::SimpleWatcher::Context::Notify()

[Monorail components: OS>Systems>Feedback UI>Browser>ReportAnIssue]

### do...@chromium.org (2021-07-24)

[Empty comment from Monorail migration]

### do...@chromium.org (2021-07-24)

[Empty comment from Monorail migration]

### do...@chromium.org (2021-07-24)

[Empty comment from Monorail migration]

### do...@chromium.org (2021-07-24)

[Empty comment from Monorail migration]

### do...@chromium.org (2021-07-24)

[Empty comment from Monorail migration]

### do...@chromium.org (2021-07-24)

[Empty comment from Monorail migration]

### do...@chromium.org (2021-07-24)

[Empty comment from Monorail migration]

### do...@chromium.org (2021-07-24)

[Empty comment from Monorail migration]

### do...@chromium.org (2021-07-24)

[Empty comment from Monorail migration]

### xi...@google.com (2021-07-26)

Does this happen on Chrome OS too? How to reproduce it? I do not see the same option to start a guess profile. 

I agreed that we should discuss how to solve the issue. I can represent the feedback app. Who are the contacts for profile and showWebDialog?

### al...@chromium.org (2021-07-26)

re c#5: Looking at the screencast from c#2, the reported uses a custom Chromium build. It looks like the DestroyProfileOnBrowserClose feature was never shipped beyond 50% canary and dev.

re c#11: There are basically two approaches:

1) essentially what you've described in your comment. Windows should listen for profile destruction events and close themselves when a profile is closing.
2) keep ScopedProfileKeepAlive object in all windows belonging to a profile so that a profile is not destroyed until all windows are closed

2) matches to the current behavior with disabled DestroyProfileOnBrowserClose more closely and I don't see a reason for changing this behavior.

### dr...@chromium.org (2021-07-26)

I don't think we should keep a ScopedProfileKeepAlive object in all windows belonging to a profile. This is not what browser windows do for example. I really prefer 1 here, unless there is a strong reason to prevent the profile from being deleted.

### al...@chromium.org (2021-07-26)

> This is not what browser windows do for example. 

I do not think this is correct. See [1]. How else browser windows would indicate that the profile should be kept alive?

We have a separate keep alive [2] for App windows, for example.

[1] https://source.chromium.org/chromium/chromium/src/+/5e65dec098742af43e5dfca8ace6e7c99776dd53:chrome/browser/ui/browser.h;drc=d8ef0e3e7389b6d9d97ce16249551d88739e9b38;l=1098
[2] https://source.chromium.org/chromium/chromium/src/+/5e65dec098742af43e5dfca8ace6e7c99776dd53:chrome/browser/profiles/profile_keep_alive_types.h;drc=0d99d5d1985df1f0788ccdaa43b34e8d248bf2c1;l=49


### dr...@chromium.org (2021-07-26)

If we want to implement https://crbug.com/chromium/130656, we want the user to be able to close a profile.
To do this we need to actively close all UIs when deleting the profile, rather than doing the opposite (retaining the profile). If we add more ScopedProfileKeepAlive, we also run into the risk of leaking profiles (profiles not being actually destroyed).

Indeed I see that browsers have a scoped keep alive (I didn't know this). I think the main point for browsers in my opinion is that there is a way to actively close all browsers for the current profile, which gives the user an effective way to delete their profile. If we want to add a profile keepalive here, then ideally we need the "close all browsers" button to also close this dialog somehow.

I see nicolaso@ already owns this bug, and is probably the person with the most context on this, so anyway I would defer to him.

### [Deleted User] (2021-07-27)

nicolaso: Uh oh! This issue still open and hasn't been updated in the last 15 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ni...@chromium.org (2021-08-02)

> If we add more ScopedProfileKeepAlive, we also run into the risk of leaking profiles (profiles not being actually destroyed).

That risk is unfortunate, but hard to avoid. We do have _some_ metrics [1] on leaked profiles, so we can see how often this happens in the wild.

Adding a ScopedProfileKeepAlive is easy, and at least it fixes the crash. It may cause leaks, but it's still better than pre-DestroyProfileOnBrowserClose behavior.

> If we want to add a profile keepalive here, then ideally we need the "close all browsers" button to also close this dialog somehow.

Let me make sure I understand correctly--you mean that when all browsers are closed by the user (via their X button), this would automatically close the Feedback UI? We could do the same for similar UI surfaces (e.g., the Task Manager window).

Or is there an existing "Close all browsers" button I'm not aware of?

Anyways, to fix the dangling RPH, WebDialogView [2] would listen for OnBrowserRemoved() (or maybe OnBrowserClosed()?) and close itself when the last browser window closes... One issue is, deleting that RPH will race with the Browser's destruction. So in some cases, this would still leak an RPH and fail to delete the Profile...

Note that we can fix this by combining both approaches:

  1. WebDialogView holds a ScopedProfileKeepAlive until it closes (via its Delegate)
  2. WebDialogView observes BrowserList, and close itself according to the logic above.
  3. The RPH gets deleted.
  4. WebDialogView gets deleted after(?) the RPH, releasing the keepalive.
  5. Because there's no more keepalive, delete the Profile (this is now safe, because of #3).

Let's start with the keepalive, and see if we want to implement the rest.

[1] https://crgo.dev/c/b/profiles/profile_manager.cc;l=521;drc=f60c8d2b2478e42fe420cb5012e304d72f1f2613
[2] https://crgo.dev/c/ui/views/controls/webview/web_dialog_view.h

### dr...@chromium.org (2021-08-03)

There is a "close all browsers" button, see screenshot.

### ni...@chromium.org (2021-08-03)

Huh, you learn something new every day. Well then, let's at least make that button close the feedback UI at the same time

### [Deleted User] (2021-08-05)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-07)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-15)

This bug is out of response SLO. Please update the bug with the current status today.
This bug update has been provided as part of a bug SLO pilot, please provide feedback through the contact info at go/cros-bug-slos-feedback

Chrome OS response SLOs are listed at go/cros-bug-slos.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-08-16)

[Empty comment from Monorail migration]

### an...@google.com (2021-08-17)

[Empty comment from Monorail migration]

### do...@chromium.org (2021-08-17)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-17)

nicolaso: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### xi...@google.com (2021-08-19)

[Empty comment from Monorail migration]

### xi...@google.com (2021-08-19)

Who is actually working on this? Can you provide an update? Thanks

### ni...@chromium.org (2021-08-19)

Working on it at crrev.com/c/3107529. Currently blocked on code review

### ni...@chromium.org (2021-08-19)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-08-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/56206060b562e43b49459aec7a7aaa39e2aae84e

commit 56206060b562e43b49459aec7a7aaa39e2aae84e
Author: Nicolas Ouellet-Payeur <nicolaso@chromium.org>
Date: Fri Aug 20 14:40:50 2021

[Feedback] Add ScopedProfileKeepAlive in WebUI dialog

The WebUI dialog didn't hold a ScopedProfileKeepAlive, which means its
RPH could leak when the Profile gets deleted.

Add a ScopedProfileKeepAlive to delay Profile destruction until the
RPH is properly cleaned up.

The extension version of the feedback dialog doesn't need this, since
ChromeAppWindowDelegate already holds a ScopedProfileKeepAlive.

Bug: 1228248
Change-Id: Ie0dae104f01fd148843964dea1a6606c5f3faf67
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3107529
Commit-Queue: Nicolas Ouellet-Payeur <nicolaso@chromium.org>
Reviewed-by: Jimmy Gong <jimmyxgong@chromium.org>
Reviewed-by: John Lee <johntlee@chromium.org>
Cr-Commit-Position: refs/heads/main@{#913789}

[modify] https://crrev.com/56206060b562e43b49459aec7a7aaa39e2aae84e/chrome/browser/profiles/profile_keep_alive_types.cc
[modify] https://crrev.com/56206060b562e43b49459aec7a7aaa39e2aae84e/chrome/browser/profiles/profile_keep_alive_types.h
[modify] https://crrev.com/56206060b562e43b49459aec7a7aaa39e2aae84e/chrome/browser/ui/webui/feedback/feedback_dialog.cc
[modify] https://crrev.com/56206060b562e43b49459aec7a7aaa39e2aae84e/chrome/browser/ui/webui/feedback/feedback_dialog.h
[modify] https://crrev.com/56206060b562e43b49459aec7a7aaa39e2aae84e/tools/metrics/histograms/enums.xml


### xi...@google.com (2021-08-23)

Has the fix been verified? Can we close this issue? Thank you!

### ni...@chromium.org (2021-08-25)

Hasn't been verified (I'm the only one who tested the change AFAICT), but it is fixed

### [Deleted User] (2021-08-25)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-25)

[Empty comment from Monorail migration]

### am...@google.com (2021-09-01)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-09-01)

Congratulations! The VRP Panel has decided to award you $5000 for this report. Thank you for your efforts and your continued reports! (the seeing us in the next bug happened rather quick :))

### wx...@gmail.com (2021-09-01)

Still waiting for you in next bug :), lol

### am...@google.com (2021-09-02)

[Empty comment from Monorail migration]

### vo...@google.com (2021-10-12)

Marking as not applicable to M90 LTS because the code for the feedback dialog was added after M90 and I wasn't able to reproduce this issue on LTS.

### am...@chromium.org (2021-10-19)

[Empty comment from Monorail migration]

### am...@google.com (2021-10-19)

[Empty comment from Monorail migration]

### am...@google.com (2021-11-02)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1228248?no_tracker_redirect=1

[Multiple monorail components: OS>Systems>Feedback, UI>Browser>Profiles, UI>Browser>ReportAnIssue]
[Monorail mergedwith: crbug.com/chromium/1228249, crbug.com/chromium/1228251, crbug.com/chromium/1228253, crbug.com/chromium/1228255, crbug.com/chromium/1228256, crbug.com/chromium/1228257, crbug.com/chromium/1228259, crbug.com/chromium/1231764, crbug.com/chromium/1231967, crbug.com/chromium/1240329]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40056497)*
