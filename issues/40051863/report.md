# UAF in base::SupportsUserData::SetUserData

| Field | Value |
|-------|-------|
| **Issue ID** | [40051863](https://issues.chromium.org/issues/40051863) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Payments |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | cd...@gmail.com |
| **Assignee** | ro...@chromium.org |
| **Created** | 2020-03-27 |
| **Bounty** | $20,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36

Steps to reproduce the problem:
1 python3.6m -m http.server 8605
2 ./crhome  --user-dir=/tmp/nonexist --incognito  http://127.0.0.1:8605/crash.html
3 Close the browser manually.

What is the expected behavior?

What went wrong?
Received signal 11 SEGV_MAPERR fffffbbfae73e631
#0 0x55f2c0ac9229 base::debug::CollectStackTrace()
#1 0x55f2c0a2f5b3 base::debug::StackTrace::StackTrace()
#2 0x55f2c0ac8d71 base::debug::(anonymous namespace)::StackDumpSignalHandler()
#3 0x7f89845bb890 <unknown>
#4 0x55f2c0a73b8b base::SupportsUserData::SetUserData()
#5 0x55f2bee3990e content::BrowserContext::GetPermissionController()
#6 0x55f2bf0d248f content::(anonymous namespace)::CheckPermissionForPaymentApps()
#7 0x55f2bf0d6fe4 base::internal::Invoker<>::RunOnce()
#8 0x55f2bf0d5d38 base::internal::Invoker<>::RunOnce()
#9 0x55f2c0a7642b base::TaskAnnotator::RunTask()
#10 0x55f2c0a86e9e base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl()
#11 0x55f2c0a86c51 base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoSomeWork()
#12 0x55f2c0a45667 base::(anonymous namespace)::WorkSourceDispatch()
#13 0x7f89826d8417 g_main_context_dispatch
#14 0x7f89826d8650 <unknown>
#15 0x7f89826d86dc g_main_context_iteration
#16 0x55f2c0a454c2 base::MessagePumpGlib::Run()
#17 0x55f2c0a87719 base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run()
#18 0x55f2c0a5eda2 base::RunLoop::Run()
#19 0x55f2c06afd83 ChromeBrowserMainParts::MainMessageLoopRun()
#20 0x55f2bee4af8b content::BrowserMainLoop::RunMainMessageLoopParts()
#21 0x55f2bee4cf32 content::BrowserMainRunnerImpl::Run()
#22 0x55f2bee47e9d content::BrowserMain()
#23 0x55f2c0643f35 content::ContentMainRunnerImpl::RunServiceManager()
#24 0x55f2c0643c3a content::ContentMainRunnerImpl::Run()
#25 0x55f2c0692f93 service_manager::Main()
#26 0x55f2c0642011 content::ContentMain()
#27 0x55f2be24c5ae ChromeMain
#28 0x7f897e54ab97 __libc_start_main
#29 0x55f2be24c3ea _start
  r8: 00007ffce53e68b8  r9: 0000000000000001 r10: 00007ffce53e6470 r11: 0000000000000001
 r12: 00000442fe287990 r13: 000055f2bcb62210 r14: 00000442f771c9d0 r15: 00000442f771c9c0
  di: 0000000000000030  si: fffffffffffde1d1  bp: 00007ffce53e6700  bx: 00000442f771c9d0
  dx: 0000000000000030  ax: fffffbbfae73e631  cx: 00007f8984baa000  sp: 00007ffce53e66c0
  ip: 000055f2c0a73b8b efl: 0000000000010202 cgf: 002b000000000033 erf: 0000000000000005
 trp: 000000000000000e msk: 0000000000000000 cr2: fffffbbfae73e631
[end of stack trace]
Calling _exit(1). Core file will not be generated.

Did this work before? N/A 

Chrome version: Chromium 83.0.4095.0   Channel: stable
OS Version: Ubuntu18.04
Flash Version:

## Attachments

- [poc.zip](attachments/poc.zip) (application/octet-stream, 4.9 KB)

## Timeline

### cd...@gmail.com (2020-03-27)

[Empty comment from Monorail migration]

### jd...@chromium.org (2020-03-27)

Thanks for the report.

rouslan@: Can you take a look at this report? All CCing danyao@ for visibility.

It's not clear to me how controllable this is, but the failed check (see below) is in the browser process, so assigning Sev-High. It may be worse.

It took me a while to be able to reproduce this, and I can only do so in trunk, but conservatively setting Security_Impact-Stable until someone can look a bit more at it.

Loading the PoC causes Chrome to hang for a while. Trying to close Chrome during this time usually triggers the crash. If you wait too long (>10 seconds?), it's more likely to not crash.

[Monorail components: Blink>Payments]

### ro...@chromium.org (2020-03-27)

Do we have any crash identifiers from chrome://crashes?

CheckPermissionForPaymentApps() uses a raw pointer for browser_context. Is that pointer null or something else?

### ro...@chromium.org (2020-03-27)

Stack seems to suggest that browser_context is null. It does not seem to have a weak pointer. What's the standard procedure for checking whether the browser context is gone?

### ro...@chromium.org (2020-03-28)

Jinho: Do you have any suggestions on how to fix this "use after free"? It appears that browser_context can be freed before CheckPermissionForPaymentApps() is called.

### [Deleted User] (2020-03-30)

[Comment Deleted]

### [Deleted User] (2020-03-30)

rouslan@,

Since the main() function is called recursively in the attached JS code, it seems that the process is terminated and the BrowserContext is also destroyed. To track the BrowserContext's life, we might make the PaymentAppProvider to KeyedService or might use ChildProcessSecurityPolicy.
However, I think the root cause is that the PaymentRequest constructor in JS side calls GetAllPaymentApps() internally. Since the constructor is not asynchronous, we should defer to call the GetAllPaymentApps() until canMakePayment() or show() is called.

try {
   new PaymentRequest([{ supportedMethods: "https://xxxxx.com/pay" }], ..., {});
} catch (e) {
    // The "https://xxxxx.com/pay" causes some error but JS authors can't catch it.
}
One workaround might be that we make the JS context stop in the error situation.

### ro...@google.com (2020-04-07)

I plan to look into it this sprint.

### ro...@google.com (2020-04-09)

https://chromium-review.googlesource.com/2144311 is WIP

### ad...@google.com (2020-04-09)

Thanks for keeping this crbug updated with your progress - it's much appreciated.

### [Deleted User] (2020-04-09)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-04-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/2d0aad1e7602a7076d86772cc159b891cf2cf03b

commit 2d0aad1e7602a7076d86772cc159b891cf2cf03b
Author: Rouslan Solomakhin <rouslan@chromium.org>
Date: Sat Apr 11 15:19:59 2020

[Web Payment] Browser context owned callback.

Before this patch, an unowned function pointer would be invoked
asynchronously with a reference to the possibly freed reference to the
browser context, which could cause use after free in certain
circumstances.

This patch makes the browser context own the callback and binds the
function with a weak pointer, so freeing the browser context invalidates
the weak pointer, which cancels the callback execution.

After this patch, freeing the browser context aborts the asynchronous
callback that dereferences the browser context, so the use after free
is prevented.

Bug: 1065298
Change-Id: Id6de3099a55c4505e94a8a6d21fb25d6d2b34c6c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2144311
Reviewed-by: Danyao Wang <danyao@chromium.org>
Commit-Queue: Rouslan Solomakhin <rouslan@chromium.org>
Cr-Commit-Position: refs/heads/master@{#758404}

[modify] https://crrev.com/2d0aad1e7602a7076d86772cc159b891cf2cf03b/content/browser/payments/payment_app_provider_impl.cc


### ro...@google.com (2020-04-11)

cdsrc2016@ and/or jdeblasio@: Can you please double-check that the bug no longer reproduces after https://chromiumdash.appspot.com/commit/2d0aad1e7602a7076d86772cc159b891cf2cf03b ?

### [Deleted User] (2020-04-12)

[Empty comment from Monorail migration]

### [Deleted User] (2020-04-12)

Requesting merge to stable M81 because latest trunk commit (758404) appears to be after stable branch point (737173).

Requesting merge to beta M81 because latest trunk commit (758404) appears to be after beta branch point (737173).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-04-12)

This bug requires manual review: Request affecting a post-stable build
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
Owners: benmason@(Android), bindusuvarna@(iOS), geohsu@(ChromeOS), pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cd...@gmail.com (2020-04-13)

Hhi，@rouslan
After patch in c#12, no uaf reproduced anymore(tried 10+times).

### ro...@google.com (2020-04-13)

Thank you, cdsrc2016@.

### ro...@google.com (2020-04-13)

> 1. Does your merge fit within the Merge Decision Guidelines?

Yes.

> 2. Links to the CLs you are requesting to merge.

https://crrev.com/c/2144311

> 3. Has the change landed and been verified on master/ToT?

Yes.

> 4. Why are these changes required in this milestone after branch?

Fixing a security bug.

> 5. Is this a new feature?

No.

> 6. If it is a new feature, is it behind a flag using finch?

N/A.

### pb...@google.com (2020-04-13)

Please request M83 merge and adding Adetaylor(Security TPM)

### ro...@google.com (2020-04-13)

Requesting M-83 merge. Thank you for the reminder.

### [Deleted User] (2020-04-13)

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

### sr...@google.com (2020-04-13)

Merge approved for M-83, branch:4103, Please merge your changes asap so we can include in dev RC for tomorrow ( before 2pm PST)

adetaylor@ FYI

### na...@google.com (2020-04-13)

[Empty comment from Monorail migration]

### ro...@google.com (2020-04-13)

Does anyone have any idea what's happening with drover?

$ git-drover --cherry-pick 2d0aad1e7602a7076d86772cc159b891cf2cf03b --branch 4103
Going to cherry-pick
"""
b'commit 2d0aad1e7602a7076d86772cc159b891cf2cf03b\nAuthor: Rouslan Solomakhin <rouslan@chromium.org>\nDate:   Sat Apr 11 15:19:59 2020 +0000\n\n    [Web Payment] Browser context owned callback.\n    \n    Before this patch, an unowned function pointer would be invoked\n    asynchronously with a reference to the possibly freed reference to the\n    browser context, which could cause use after free in certain\n    circumstances.\n    \n    This patch makes the browser context own the callback and binds the\n    function with a weak pointer, so freeing the browser context invalidates\n    the weak pointer, which cancels the callback execution.\n    \n    After this patch, freeing the browser context aborts the asynchronous\n    callback that dereferences the browser context, so the use after free\n    is prevented.\n    \n    Bug: 1065298\n    Change-Id: Id6de3099a55c4505e94a8a6d21fb25d6d2b34c6c\n    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2144311\n    Reviewed-by: Danyao Wang <danyao@chromium.org>\n    Commit-Queue: Rouslan Solomakhin <rouslan@chromium.org>\n    Cr-Commit-Position: refs/heads/master@{#758404}\n'"""
to 4103. Continue (y/n)? y
Traceback (most recent call last):
  File "/home/rouslan/depot_tools/git_drover.py", line 466, in <module>
    main()
  File "/home/rouslan/depot_tools/git_drover.py", line 457, in main
    cherry_pick_change(options.branch, options.cherry_pick,
  File "/home/rouslan/depot_tools/git_drover.py", line 379, in cherry_pick_change
    drover.run()
  File "/home/rouslan/depot_tools/git_drover.py", line 146, in run
    self._run_internal()
  File "/home/rouslan/depot_tools/git_drover.py", line 155, in _run_internal
    self._create_checkout()
  File "/home/rouslan/depot_tools/git_drover.py", line 236, in _create_checkout
    parent_git_dir = os.path.join(self._parent_repo, self._run_git_command(
  File "/home/rouslan/.vpython-root/037449/lib/python3.8/posixpath.py", line 90, in join
    genericpath._check_arg_types('join', a, *p)
  File "/home/rouslan/.vpython-root/037449/lib/python3.8/genericpath.py", line 155, in _check_arg_types
    raise TypeError("Can't mix strings and bytes in path components") from None
TypeError: Can't mix strings and bytes in path components


### ro...@google.com (2020-04-13)

Drover worked on my workstation: https://crrev.com/c/2147843 is being submitted to branch 4103.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-04-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/f6ead152294500077ca301af55ac404e17e14f62

commit f6ead152294500077ca301af55ac404e17e14f62
Author: Rouslan Solomakhin <rouslan@chromium.org>
Date: Mon Apr 13 20:49:46 2020

[Merge M83][Web Payment] Browser context owned callback.

Before this patch, an unowned function pointer would be invoked
asynchronously with a reference to the possibly freed reference to the
browser context, which could cause use after free in certain
circumstances.

This patch makes the browser context own the callback and binds the
function with a weak pointer, so freeing the browser context invalidates
the weak pointer, which cancels the callback execution.

After this patch, freeing the browser context aborts the asynchronous
callback that dereferences the browser context, so the use after free
is prevented.

TBR=rouslan@chromium.org

(cherry picked from commit 2d0aad1e7602a7076d86772cc159b891cf2cf03b)

Bug: 1065298
Change-Id: Id6de3099a55c4505e94a8a6d21fb25d6d2b34c6c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2144311
Reviewed-by: Danyao Wang <danyao@chromium.org>
Commit-Queue: Rouslan Solomakhin <rouslan@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#758404}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2147843
Reviewed-by: Rouslan Solomakhin <rouslan@chromium.org>
Cr-Commit-Position: refs/branch-heads/4103@{#109}
Cr-Branched-From: 8ad47e8d21f6866e4a37f47d83a860d41debf514-refs/heads/master@{#756066}

[modify] https://crrev.com/f6ead152294500077ca301af55ac404e17e14f62/content/browser/payments/payment_app_provider_impl.cc


### ad...@google.com (2020-04-15)

rouslan@, approving merge also to M81 branch 4044. Please have a look to see there are no new crashes in this area on Canary (it looks like it probably also made it into the dev release 83.0.4103.14).

### ro...@chromium.org (2020-04-15)

The crash database contains 4 crash reports with this eact signature in the following versions:
1 report in 74.0.3729.136
2 reports in 79.0.3945.93
1 report in 79.0.3945.116

When looking for all crash stacks that contain CheckPermissionForPaymentApps, but not necessarily this exact stack trace, then there're 51 total reports with the latest being in 80.0.3987.137.

Both queries show no crashes M81 and later, but that could be because of a small sample size: about 1 crash per week.

I'm going ahead and merging into M81 because the fix should be safe.

### na...@google.com (2020-04-15)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-04-15)

Congrats! The Panel decided to award you $20,000 for this report! 

### na...@google.com (2020-04-15)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-04-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/686d1bfbcb8f4fc0f1c45f1dea61f41730961b4a

commit 686d1bfbcb8f4fc0f1c45f1dea61f41730961b4a
Author: Rouslan Solomakhin <rouslan@chromium.org>
Date: Wed Apr 15 23:03:07 2020

[Merge M81][Web Payment] Browser context owned callback.

Before this patch, an unowned function pointer would be invoked
asynchronously with a reference to the possibly freed reference to the
browser context, which could cause use after free in certain
circumstances.

This patch makes the browser context own the callback and binds the
function with a weak pointer, so freeing the browser context invalidates
the weak pointer, which cancels the callback execution.

After this patch, freeing the browser context aborts the asynchronous
callback that dereferences the browser context, so the use after free
is prevented.

TBR=rouslan@chromium.org

(cherry picked from commit 2d0aad1e7602a7076d86772cc159b891cf2cf03b)

Bug: 1065298
Change-Id: Id6de3099a55c4505e94a8a6d21fb25d6d2b34c6c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2144311
Reviewed-by: Danyao Wang <danyao@chromium.org>
Commit-Queue: Rouslan Solomakhin <rouslan@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#758404}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2151474
Reviewed-by: Rouslan Solomakhin <rouslan@chromium.org>
Cr-Commit-Position: refs/branch-heads/4044@{#942}
Cr-Branched-From: a6d9daf149a473ceea37f629c41d4527bf2055bd-refs/heads/master@{#737173}

[modify] https://crrev.com/686d1bfbcb8f4fc0f1c45f1dea61f41730961b4a/content/browser/payments/payment_app_provider_impl.cc


### ad...@google.com (2020-04-20)

I'm assuming this affects more platforms than just Linux. Please fix if not.

### ad...@google.com (2020-04-20)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-04-20)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-05-21)

[Empty comment from Monorail migration]

### mm...@chromium.org (2020-06-30)

rouslan@, thank you for fixing this issue. Chrome Security team needs your knowledge to prevent that whole class of bugs from happening elsewhere. We would greatly appreciate if you could tell us more about the issue by filling out the following form: https://forms.gle/VWKDUv9a8GXCCRWm7

### ro...@google.com (2020-07-13)

Done!

### mm...@google.com (2020-07-14)

[Empty comment from Monorail migration]

### [Deleted User] (2020-07-18)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1065298?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40051863)*
