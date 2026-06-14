# Security: Heap-use-after-free in SharingDialogView::WindowClosing()

| Field | Value |
|-------|-------|
| **Issue ID** | [40050060](https://issues.chromium.org/issues/40050060) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | UI>Browser>Sharing |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | kn...@chromium.org |
| **Created** | 2019-09-05 |
| **Bounty** | $15,000.00 |

## Description

**VERSION**  

Chrome Version: Chromium 78.0.3903.0 (Developer Build) (64-bit)  

Operating System: All

**REPRODUCTION CASE**

1. Open index.html
2. Click on the button
3. On PoC.html click on the link wait

(gdb) x/1i $rip  

=> 0x55555cc6b602 <\_ZThn24\_N17SharingDialogView13WindowClosingEv+18>: mov 0x58(%rcx),%rcx  

(gdb) bt  

#0 0x000055555cc6b602 in non-virtual thunk to SharingDialogView::WindowClosing() ()  

#1 0x000055555bfd30b0 in views::Widget::OnNativeWidgetDestroying() ()  

#2 0x000055555bff0bf3 in non-virtual thunk to views::NativeWidgetAura::OnWindowDestroying(aura::Window\*) ()  

#3 0x000055555b832294 in aura::Window::~Window() ()  

#4 0x000055555b832b3e in aura::Window::~Window() ()  

#5 0x000055555a61d26f in base::TaskAnnotator::RunTask(char const\*, base::PendingTask\*) ()  

#6 0x000055555a62dafc in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence\_manager::LazyNow\*, bool\*)  

()  

#7 0x000055555a62d7e8 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoSomeWork() ()  

#8 0x000055555a5ea827 in base::(anonymous namespace)::WorkSourceDispatch(\_GSource\*, int (\*)(void\*), void\*) ()  

#9 0x00007ffff5aee197 in g\_main\_context\_dispatch () from /lib/x86\_64-linux-gnu/libglib-2.0.so.0  

#10 0x00007ffff5aee3f0 in ?? () from /lib/x86\_64-linux-gnu/libglib-2.0.so.0  

#11 0x00007ffff5aee49c in g\_main\_context\_iteration () from /lib/x86\_64-linux-gnu/libglib-2.0.so.0  

#12 0x000055555a5ea692 in base::MessagePumpGlib::Run(base::MessagePump::Delegate\*) ()  

#13 0x000055555a62e429 in non-virtual thunk to base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ()  

#14 0x000055555a606437 in base::RunLoop::Run() ()  

#15 0x000055555a2784a7 in ChromeBrowserMainParts::MainMessageLoopRun(int\*) ()  

#16 0x0000555558aff44b in content::BrowserMainLoop::RunMainMessageLoopParts() ()  

#17 0x0000555558b01222 in content::BrowserMainRunnerImpl::Run() ()  

#18 0x0000555558afc60f in content::BrowserMain(content::MainFunctionParams const&) ()  

#19 0x000055555a20ea8f in content::ContentMainRunnerImpl::RunServiceManager(content::MainFunctionParams&, bool) ()  

#20 0x000055555a20e7d6 in content::ContentMainRunnerImpl::Run(bool) ()  

#21 0x000055555a25a81d in service\_manager::Main(service\_manager::MainParams const&) ()  

#22 0x000055555a20cae1 in content::ContentMain(content::ContentMainParams const&) ()  

#23 0x0000555557f6b1bf in ChromeMain ()  

#24 0x00007ffff184f830 in \_\_libc\_start\_main (main=0x555557f6b130 <main>, argc=1, argv=0x7fffffffddc8, init=<optimized out>, fini=<optimized out>,  

rtld\_fini=<optimized out>, stack\_end=0x7fffffffddb8) at ../csu/libc-start.c:291  

#25 0x0000555557f6b02a in \_start ()

## Attachments

- [index.html](attachments/index.html) (text/plain, 76 B)
- [poc.html](attachments/poc.html) (text/plain, 94 B)

## Timeline

### es...@chromium.org (2019-09-06)

Confirmed on ToT. Adding sharing OWNERS to please investigate; I'll start on a bisect.

[Monorail components: UI>Browser>Sharing]

### es...@chromium.org (2019-09-06)

You are probably looking for a change made after 692896 (known good), but no later than 692901 (first known bad).
CHANGELOG URL:
  https://chromium.googlesource.com/chromium/src/+log/1dc6265c2545f7e9a6f0a4b4721606e2951502f1..13e0e5dc80650349062d2a6af19d183bb357f465

Reassigning to knollr as https://chromium-review.googlesource.com/c/chromium/src/+/1755915 looks most relevant from the regression range.

### es...@chromium.org (2019-09-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-09-07)

This is a critical security issue. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-09-07)

Setting Pri-0 to match security severity Critical. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pe...@chromium.org (2019-09-08)

--> Richard as I'm traveling to Japan, and +Alex since I'm not sure when Richard will follow. PTAL at this p0 security issue.

### pe...@chromium.org (2019-09-08)

Thank you for the bisect Emily! We'll take care of this.

### kn...@chromium.org (2019-09-08)

Hi, thanks for the report and the bisect, very helpful in getting to the bottom of this :-)

Sorry for the late response, I now had a closer look at this. First things first:
Hotfix CL that we could merge into M78: https://crrev.com/c/1789150
More complete follow-up with regression test: https://crrev.com/c/1789149

TLDR: Unfortunately this issue is already present in M77. All of this is behind a flag that we planned to turn on for M77, but in case this is too risky, we'll have to delay that to M78.

More details about the cause:
The CL mentioned in c#2 did cause this issue to be visible as an actual crash. Unfortunately the real source of the UAF got introduced quite a while earlier in https://crrev.com/c/1709429.
That CL changed the lifetime of ClickToCallSharingDialogController (now called ClickToCallUiController) from being owned by ClickToCallDialogView (now called SharingDialogView) to now being tied to the WebContents as a WebContentsUserData. The ClickToCallDialogView (which is a LocationBarBubbleDelegateView) closes itself when the WebContents gets destroyed [1], but the actual call to WidgetDelegate::WindowClosing happens asynchronously, after the WebContents has been destroyed already [2]. Inside ClickToCallDialogView::WindowClosing we then try to notify the already deleted controller [3] that the bubble got closed, which causes this UAF.
The fix is to check if the WebContents is still valid before accessing the controller.

[1]: https://cs.chromium.org/chromium/src/chrome/browser/ui/views/location_bar/location_bar_bubble_delegate_view.cc?l=91&rcl=1558754bd5a878f56a3118513d8e3605b25b951c
[2]: https://cs.chromium.org/chromium/src/ui/views/widget/desktop_aura/desktop_window_tree_host_platform.cc?l=196&rcl=1558754bd5a878f56a3118513d8e3605b25b951c
[3]: https://cs.chromium.org/chromium/src/chrome/browser/ui/views/sharing/sharing_dialog_view.cc?l=336&rcl=1558754bd5a878f56a3118513d8e3605b25b951c

### go...@chromium.org (2019-09-09)

Reminder M78 Beta promotion is coming soon. Please review this bug and assess if this is indeed a RBS. If not, please remove the RBS label. If so, please make sure to land the fix and request a merge into the release branch ASAP. Thank you

### go...@chromium.org (2019-09-09)

+adetaylor@ (Security TPM), could you ptal as this is M78 Beta blocker? Thank you.

### al...@chromium.org (2019-09-09)

[Empty comment from Monorail migration]

### al...@chromium.org (2019-09-09)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-09-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/fd7196aeb220da48823350fe6f9ed8ef02133b61

commit fd7196aeb220da48823350fe6f9ed8ef02133b61
Author: Richard Knoll <knollr@chromium.org>
Date: Mon Sep 09 09:57:23 2019

Hotfix UAF when closing tab with sharing dialog.

This fixes a UAF when closing a tab while there is a
SharingDialog open.

Bug: 1000934
Change-Id: Ie8f6e52626ee834bc72acfe318c5a28aafe27635
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1789150
Commit-Queue: Alex Chau <alexchau@chromium.org>
Reviewed-by: Alex Chau <alexchau@chromium.org>
Cr-Commit-Position: refs/heads/master@{#694682}

[modify] https://crrev.com/fd7196aeb220da48823350fe6f9ed8ef02133b61/chrome/browser/ui/views/sharing/sharing_dialog_view.cc


### al...@chromium.org (2019-09-09)

[Empty comment from Monorail migration]

### al...@chromium.org (2019-09-09)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-09-09)

This bug requires manual review: We don't branch M78 until 2019-09-05.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://goto.google.com/chrome-release-branch-merge-guidelines
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: govind@(Android), kariahda@(iOS), geohsu@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-09-09)

This bug requires manual review: We are only 0 days from stable.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://goto.google.com/chrome-release-branch-merge-guidelines
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), kariahda@(iOS), dgagnon@(ChromeOS), lakpamarthy@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### al...@chromium.org (2019-09-09)

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: M-77 branch point is tomorrow, we won't have enough time to let the change last 24 hour on canary. The change is one-line and very safe, it adds a check if web_contents() is present before closing the dialog, and only affect the SharingDiagloView itself. It's also a P0 security bug, the one-line fix is safer than a revert.
2. Links to the CLs you are requesting to merge. https://chromium-review.googlesource.com/c/chromium/src/+/1789150
3. Has the change landed and been verified on master/ToT? Yes, verified on ToT.
4. Why are these changes required in this milestone after branch? Bug is only discovered on Sep 5, way after branch point. Not reproducible without macro that close the dialog automatically.
5. Is this a new feature? No.
6. If it is a new feature, is it behind a flag using finch? No.

### go...@chromium.org (2019-09-09)

+benmason@, dgagnon@ lakpamarthy@  (M77 Release TPMS)

Re #18, M77 is going to stable tomorrow and stable RC is already cut for Android and Desktop,  I will let M77 Release TPMs and adetaylor@ to decide on merge. 

### ad...@chromium.org (2019-09-09)

knollr@ re https://crbug.com/chromium/1000934#c8 could you clarify the status of this in M77?

Specifically, you say it's behind a flag. Can you confirm that M77 (and earlier releases) are *not* vulnerable to this problem unless the flag is enabled?

If that's the case then we should merge this to M78, and yes it's a beta blocker.

As for M77 either of these outcomes are OK with me, and you should discuss with the release TPMs which you do:

* Merge this fix back to a respin of M77 so that you can enable the flag; or
* Don't merge this to M77 and don't enable the flag!

As to the general riskiness of turning on this feature in M77/M78/etc. does this report enable you to identify any surfaces that could benefit from a new fuzzer?

### go...@chromium.org (2019-09-09)

Thank you adetaylor@.

For M78 merge, pls update bug with canary result tomorrow, will approve merge to M78 if change looks good in canary. Thank you.

### sh...@chromium.org (2019-09-09)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### la...@google.com (2019-09-09)

knollr@ - please confirm if disabling the flag would take the vulnerability out for M77. I would prefer we not enable the flag for M77.  I will reject this review for M77 once knollr@ responds.


### mv...@chromium.org (2019-09-09)

knollr@ seems to be on a long flight at the moment - this is behind the ClickToCallUI feature flag which is disabled by default. It is currently enabled in 50% of Canary / Dev / Beta. I'll ping our team on this, but not cherry-picking this in M77 would mean we have to delay further experimentation and our intended launch to M78.

### mv...@chromium.org (2019-09-09)

[Empty comment from Monorail migration]

### al...@chromium.org (2019-09-09)

[Empty comment from Monorail migration]

### kn...@chromium.org (2019-09-09)

Hi, yes, I agree with https://crbug.com/chromium/1000934#c24, it's behind a disabled by default flag. This bug can only trigger with that flag *enabled*. Pre M77 versions are not vulnerable to this at all.
As for any new fuzzers, I'm not sure what we already test, but closing tabs randomly while using features could potentially discover these?

### ad...@chromium.org (2019-09-09)

Thanks for the very informative comments knollr@ and mvanouwerkerk@. Much appreciated.

Regarding fuzzers I think you're right. CF does already inject random UI events so would probably eventually have found this.

### ch...@gmail.com (2019-09-09)

I wasn't able to repro this on Chromium 79.0.3908.0 (Developer Build) (64-bit) master@{#694743} after landing the patch. I will double-check on tomorrow's Canary. Thanks for the quick fix!

### la...@google.com (2019-09-09)

Per my offline convo with sarraf@, we would not be enabling the ClickToCallUI feature flag for M77 Stable release tomorrow as this would expose the vulnerability. We would enable the feature flag should we decide to refresh M77 Stable channel.



### la...@google.com (2019-09-09)

rejecting the M77 merge for now

### pe...@chromium.org (2019-09-10)

lakpamarthy: will that be reconsidered if there's a need for a 77 refresh? how can we be on the list of refresh considerations?

### sh...@chromium.org (2019-09-10)

[Empty comment from Monorail migration]

### la...@google.com (2019-09-10)

peter@ - we are working on a label convention for re-spin candidates. In the interim, I will work with adetaylor@ to lineup all re-spin candidates for a potential M77 Stable refresh.

### sr...@google.com (2019-09-10)

merge approved to M78, branch:3904

Please complete your merge before 12pm PST today so it can be included in this week dev release

### go...@chromium.org (2019-09-10)

Please merge your change to M78 branch 3904 by 1:00 PM PT today, so we can pick it up for tomorrow's dev release.

If change is already merged to M78 and nothing is pending for M78, pls remove "Merge=Approved-78" label. Thank you. 

### hi...@chromium.org (2019-09-10)

Already merged in branch 3904 - https://chromium-review.googlesource.com/c/chromium/src/+/1796242.
Thanks for checking :)

### al...@chromium.org (2019-09-11)

[Empty comment from Monorail migration]

### al...@chromium.org (2019-09-11)

[Empty comment from Monorail migration]

### go...@chromium.org (2019-09-13)

Looks like this is good to include in next M77 respin  "Security_Severity-Critical" but change is not yet baked in M78 Dev.

+adetaylor@ (Security TPM), wdyt?

### ad...@google.com (2019-09-13)

Yes please. This allows the sharing team to enable a feature.

### sh...@chromium.org (2019-09-13)

This bug requires manual review: Request affecting a post-stable build
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://goto.google.com/chrome-release-branch-merge-guidelines
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), kariahda@(iOS), dgagnon@(ChromeOS), lakpamarthy@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2019-09-14)

Thank you  adetaylor@.

How safe is the change to merge to M77 without M78 coverage? 
Per https://crbug.com/chromium/1000934#c27 the feature is behind flag and we will be able to disable via Finch if anything goes wrong, correct?

### go...@chromium.org (2019-09-14)

Also removing "Merge-Rejected-77" label per https://crbug.com/chromium/1000934#c41. 

### ad...@google.com (2019-09-14)

Re https://crbug.com/chromium/1000934#c43 I believe that's correct, yes.

I'm resetting it to Security_Impact-Stable per https://crbug.com/chromium/1000934#c8.

### ad...@google.com (2019-09-14)

And to answer the question in https://crbug.com/chromium/1000934#c43 - how safe is this? - the fix looks extremely safe.

### go...@chromium.org (2019-09-14)

Approving merge to M77 branch 3865 based on https://crbug.com/chromium/1000934#c46. 

### kn...@chromium.org (2019-09-15)

Merged into M77 branch 3865, thanks all!
CL: https://crrev.com/c/1803922

### al...@chromium.org (2019-09-16)

Re https://crbug.com/chromium/1000934#c43, it has been in M78 since 78.0.3904.10.

Yes, we can disable the feature via Finch.

### na...@google.com (2019-09-16)

[Empty comment from Monorail migration]

### ad...@google.com (2019-09-18)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-09-18)

[Empty comment from Monorail migration]

### na...@google.com (2019-09-19)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2019-09-19)

Congrats! The Panel decided to reward $15,000 for this report :) 

### na...@google.com (2019-09-19)

[Empty comment from Monorail migration]

### ch...@gmail.com (2019-09-19)

Nice reward! thanks as ever!

### ad...@chromium.org (2019-11-23)

[Empty comment from Monorail migration]

### mm...@chromium.org (2019-12-03)

knollr@, thank you for fixing this issue. Chrome Security team needs your knowledge to prevent that whole class of bugs from happening elsewhere. We would greatly appreciate if you could tell us more about the issue by filling out the following form: https://forms.gle/VWKDUv9a8GXCCRWm7

### mm...@chromium.org (2019-12-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-12-17)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2019-12-17)

This issue was migrated from crbug.com/chromium/1000934?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1001251]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40050060)*
