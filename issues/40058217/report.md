# Security: Page can cause autofill prompt to render near cursor in order to bypass intentional mouse movement input requirements for autofill (Bypass of issue 1240472 fix)

| Field | Value |
|-------|-------|
| **Issue ID** | [40058217](https://issues.chromium.org/issues/40058217) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Privacy |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | al...@alesandroortiz.com |
| **Assignee** | sc...@google.com |
| **Created** | 2021-12-13 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

A page can make a user select an autofill item with two consecutive clicks while moving the mouse \*\*slightly\*\* after the autofill prompt appears, which bypasses the fix for <https://crbug.com/chromium/1240472>.

Initially reported in:  

<https://bugs.chromium.org/p/chromium/issues/detail?id=1240472#c28>  

<https://bugs.chromium.org/p/chromium/issues/detail?id=1240472#c29>

Potential fix of implementing delay before allowing interactions with autofill prompt:  

<https://bugs.chromium.org/p/chromium/issues/detail?id=1241585#c2>  

<https://bugs.chromium.org/p/chromium/issues/detail?id=1240472#c30>

The details below are mostly verbatim from <https://crbug.com/chromium/1240472>, with differences bounded by two asterisks:

Normally Chrome requires an intentional selection by the user, either by moving the mouse over an autofill item or using the keyboard to select an autofill item.

When a user clicks an input field, the autofill prompt position is calculated a few moments after the mousedown event occurs. However, there is a delay between the mousedown event and when the calculation occurs. If a page moves the input field immediately after the mousedown event, the prompt position is calculated based on the input field's new position.

A page can use this delay to move the input field into a position that results in the autofill prompt rendering \*\*near\*\* the cursor location.

To make the click on the input field easy (first click), a page can place the input field under the cursor at all times (using mousemove events). Immediately after the first click, the input field is moved to make the autofill prompt render \*\*near\*\* the cursor. With the cursor \*\*near\*\* the autofill item, \*\*moving the mouse slightly in the direction of the autofill prompt and\*\* clicking a second time results in the page receiving the autofill data.

I've tested this with addresses (which includes name + email) and credit cards. For sample input, see the video recording.

**VERSION**  

Chrome Version: 98.0.4745.0 Canary (with <https://crbug.com/chromium/1240472> fix) and 96.0.4664.45 Stable (without <https://crbug.com/chromium/1240472> fix)  

Operating System: Windows 10 Version 20H2 (Build 19042.1348)

**REPRODUCTION CASE**  

PoC for address:  

Prerequisite: Have at least one address in chrome://settings/addresses

1. Navigate to <https://alesandroortiz.com/security/chromium/autofill-move-two-clicks.html>
2. Follow dot using mouse and click twice while following dots (i.e. moving mouse to the right)

PoC for credit card:  

Prerequisite: Have at least one credit card in chrome://settings/payments

1. Navigate to <https://alesandroortiz.com/security/chromium/autofill-move-two-clicks.html?creditcard>
2. (Same as prior PoC, follow dot and click twice)

For all PoCs:  

Observed: Autofilled data is provided to page, because page can cause user to select an autofill item with minimal mouse movement.  

Expected: Autofilled data is \*not\* provided to page, because page cannot cause user to select an autofill item without user intentionally moving mouse or using keyboard to select item.

With PoC modifications, the direction of the mouse can be in any direction (e.g. up, down, left, or right) since the attacker controls the autofill prompt placement relative to the mouse (and its expected movement). It's easier to do right/left since the second-click area is wider, but diagonal works almost as well, and up/down can also work well.

**CREDIT INFORMATION**  

Reporter credit: Alesandro Ortiz <https://AlesandroOrtiz.com>

## Attachments

- [autofill-move-two-clicks.html](attachments/autofill-move-two-clicks.html) (text/plain, 3.7 KB)
- [autofill-move-two-clicks-canary.mp4](attachments/autofill-move-two-clicks-canary.mp4) (video/mp4, 752.0 KB)
- [autofill-move-two-clicks-stable.mp4](attachments/autofill-move-two-clicks-stable.mp4) (video/mp4, 932.1 KB)
- [autofill-move-two-clicks-june2022.mp4](attachments/autofill-move-two-clicks-june2022.mp4) (video/mp4, 384.2 KB)

## Timeline

### al...@alesandroortiz.com (2021-12-13)

Please CC schwering@google.com into this crbug.

### [Deleted User] (2021-12-13)

[Empty comment from Monorail migration]

### do...@chromium.org (2021-12-13)

Thanks for the report. Adding folks from https://crbug.com/chromium/1240472.

[Monorail components: Privacy UI>Browser>Autofill>UI]

### [Deleted User] (2021-12-13)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-13)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-12-27)

schwering: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### al...@alesandroortiz.com (2022-01-05)

Friendly ping: Any progress on this crbug? Last update was around the holidays, so hoping this gets some attention this month.

### sc...@google.com (2022-01-10)

[Empty comment from Monorail migration]

### sc...@google.com (2022-01-14)

Thanks, we'll go for the 500 ms delay.

### sc...@google.com (2022-01-15)

As discussed in the feature sync, the CL [1] ignores clicks for a short period after the popup was shown. The default value is 500 ms. It's configurable by Finch.

During testing, I found it really difficult to click into a field, move the mouse, and click on a suggestion, all within 500 ms.

With this in mind, I'd suggest to scrap the planned study and metric about ignored click, and instead use the Finch feature as kill switch.

[1] https://chromium-review.googlesource.com/c/chromium/src/+/3391381

### gi...@appspot.gserviceaccount.com (2022-01-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/0599f9ef73f8415c6991d59d654aea262bdea785

commit 0599f9ef73f8415c6991d59d654aea262bdea785
Author: Christoph Schwering <schwering@google.com>
Date: Sat Jan 15 18:38:15 2022

[Autofill] Ignore clicks on Autofill popup right after show.

Bug: 1279268
Change-Id: I3ac9702daf031009b695cd748edb0727b9d31a05
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3391381
Reviewed-by: Mohamed Amir Yosef <mamir@chromium.org>
Commit-Queue: Christoph Schwering <schwering@google.com>
Cr-Commit-Position: refs/heads/main@{#959633}

[modify] https://crrev.com/0599f9ef73f8415c6991d59d654aea262bdea785/components/autofill/core/common/autofill_features.cc
[modify] https://crrev.com/0599f9ef73f8415c6991d59d654aea262bdea785/chrome/browser/ui/views/autofill/autofill_popup_view_native_views.cc
[modify] https://crrev.com/0599f9ef73f8415c6991d59d654aea262bdea785/components/autofill/core/common/autofill_features.h
[modify] https://crrev.com/0599f9ef73f8415c6991d59d654aea262bdea785/chrome/browser/ui/views/autofill/autofill_popup_base_view.h


### sc...@google.com (2022-01-15)

Dima, please test once [1] shows the CL has been released with the following flag:
  --enable-features=AutofillIgnoreEarlyClicksOnPopup:duration/500ms

### sc...@google.com (2022-01-16)

The CL also addresses https://crbug.com/chromium/1287364, which IMO is significantly more serious (it only needs a double-click, whereas this issue needs two clicks plus mouse movement).

### sc...@google.com (2022-01-19)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-01-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/ddc84409e820f5bc76b5ab7789f2dc9df341707b

commit ddc84409e820f5bc76b5ab7789f2dc9df341707b
Author: Christoph Schwering <schwering@google.com>
Date: Thu Jan 20 12:30:47 2022

[Autofill] Record metrics for handled and ignored suggestion clicks.

This CL adds a metric for the AutofillIgnoreEarlyClicksOnPopup
experiment. The metric records whether a click was an "early" click
(i.e., got ignored) or not, and if not, whether the click followed
an early click.

Bug: 1279268
Change-Id: Ibfdcd61050b482637892de87a908f2f6622e0e04
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3399825
Reviewed-by: Mohamed Amir Yosef <mamir@chromium.org>
Reviewed-by: Vidhan Jain <vidhanj@google.com>
Commit-Queue: Christoph Schwering <schwering@google.com>
Cr-Commit-Position: refs/heads/main@{#961419}

[modify] https://crrev.com/ddc84409e820f5bc76b5ab7789f2dc9df341707b/chrome/browser/ui/views/autofill/autofill_popup_view_native_views.cc
[modify] https://crrev.com/ddc84409e820f5bc76b5ab7789f2dc9df341707b/tools/metrics/histograms/metadata/autofill/histograms.xml
[modify] https://crrev.com/ddc84409e820f5bc76b5ab7789f2dc9df341707b/components/autofill/core/browser/metrics/autofill_metrics.h
[modify] https://crrev.com/ddc84409e820f5bc76b5ab7789f2dc9df341707b/components/autofill/core/browser/metrics/autofill_metrics.cc
[modify] https://crrev.com/ddc84409e820f5bc76b5ab7789f2dc9df341707b/tools/metrics/histograms/enums.xml


### al...@alesandroortiz.com (2022-01-21)

Verified as fixed in ASan build 961550 on Windows 10 using --enable-features=AutofillIgnoreEarlyClicksOnPopup:duration/500ms

The delay at least gives most users the ability to notice the prompt. If I'm a fast clicker and a bit distracted, it's not sufficient delay, but any higher delay would probably cause usability issues, so 500ms or something around there seems best. Looking forward to the feature study outcome.

Re: https://crbug.com/chromium/1279268#c13, want to note here that https://crbug.com/chromium/1287364 also has an additional fix specific to that crbug: https://bugs.chromium.org/p/chromium/issues/detail?id=1287364#c14

### me...@chromium.org (2022-02-01)

schwering: Can this be marked as fixed? Or are you planning to run a feature study? Thanks.

### sc...@google.com (2022-02-01)

The experiment is already happening (https://uma.googleplex.com/p/chrome/variations?sid=91040eb63d6181e138157fdbcd8f7272)

### [Deleted User] (2022-02-02)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-15)

schwering: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-02-28)

This issue appears to have been resolved and is under active experimentation; updating as Fixed 

### [Deleted User] (2022-03-01)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-01)

[Empty comment from Monorail migration]

### am...@google.com (2022-03-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-03-11)

Congratulations, Alesandro! The VRP Panel has decided to award you $3,000 for this report. Thank you for your efforts in discovering this bypass of the original mitigation and nice work! 

### al...@alesandroortiz.com (2022-03-11)

Thanks for the reward!

### am...@google.com (2022-03-11)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-04-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/c2c046d53810c6564051855355ae8c5459e87ea4

commit c2c046d53810c6564051855355ae8c5459e87ea4
Author: Christoph Schwering <schwering@google.com>
Date: Mon Apr 04 12:54:11 2022

[Autofill] Add fieldtrial testing config for AutofillIgnoreEarlyClicksOnPopup.

Bug: 1279268
Change-Id: Ieec973f1d0b316ae47380275b0ea1de34b13d508
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3567622
Reviewed-by: Matthias Körber <koerber@google.com>
Commit-Queue: Christoph Schwering <schwering@google.com>
Cr-Commit-Position: refs/heads/main@{#988466}

[modify] https://crrev.com/c2c046d53810c6564051855355ae8c5459e87ea4/testing/variations/fieldtrial_testing_config.json


### al...@alesandroortiz.com (2022-06-02)

Hi folks, this is scheduled to be disclosed in ~4 days (June ~6th), but still repros on Stable and Canary without any particular flags. It's definitely fixed when using --enable-features=AutofillIgnoreEarlyClicksOnPopup:duration/500ms (per https://crbug.com/chromium/1279268#c16)

Will the experiment be rolled out to everyone before then? If not, should this crbug be embargoed until fix is enabled for all users?

Attached is video of repro on 102.0.5005.63 Stable using https://alesandroortiz.com/security/chromium/autofill-move-two-clicks-centered.html

### am...@chromium.org (2022-06-02)

Hi schwering@, in the above https://crbug.com/chromium/1279268#c29, the reporter states this issue still reproduces on Canary and Stable without any flags being set. The fix commit appears to have made it to 102 branch 5005. Can you PTAL to confirm the fix commit resolves this issue or additional work is needed? Thank you!  

### sc...@google.com (2022-06-02)

Thanks for the heads up! The decision was just made today to move forward with the 250 ms timeout. The CLs that enable the feature on TOT and via Finch should launch within the next four days then. Should we still defer disclosure by a few days?

### al...@alesandroortiz.com (2022-06-02)

I'll trust the data and other requirements that resulted in the decision to use the 250ms timeout, but quick testing with the flag shows that it isn't effective mitigation in most of my repro attempts with the PoC, unless I'm particularly agile. Using https://tecagile.com/double-click-test/ and moving my mouse in a similar fashion as PoC shows that double clicking using external mouse results in 270-330ms delay between clicks, using touchpad results in 290-380ms delay between clicks. I would recommend at least 400ms if possible.

### gi...@appspot.gserviceaccount.com (2022-06-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/82e19da8a519522893be8aa5651d689fa5957a00

commit 82e19da8a519522893be8aa5651d689fa5957a00
Author: Christoph Schwering <schwering@google.com>
Date: Thu Jun 02 19:42:00 2022

[Autofill] Enable AutofillIgnoreEarlyClicksOnPopup by default.

Bug: 1279268
Change-Id: I0f0b5cd39cf791c292d2baf1f63f00f3bf265ad2
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3688112
Auto-Submit: Christoph Schwering <schwering@google.com>
Commit-Queue: Christoph Schwering <schwering@google.com>
Reviewed-by: Mohamed Amir Yosef <mamir@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1010234}

[modify] https://crrev.com/82e19da8a519522893be8aa5651d689fa5957a00/components/autofill/core/common/autofill_features.cc
[modify] https://crrev.com/82e19da8a519522893be8aa5651d689fa5957a00/testing/variations/fieldtrial_testing_config.json


### sc...@google.com (2022-06-03)

Amy, can we defer disclosing the bug for a while? For two reasons:
- The Finch config won't reach everyone.
- We're having another ongoing discussion about the time limit (250 ms, ..., 500 ms) (thanks, Alesandro, also for https://crbug.com/chromium/1279268#c32).

### [Deleted User] (2022-06-03)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-06-03)

Hi Christoph, sure thing. Theoretically now that this issue is reopened, it should not be disclosed. Since believe that the bot is gaining sentience, I'm going to go ahead and add the RV-SE tag with a next action of about six weeks from now to check in on this and determine if appropriate to disclose at that time. 

### gi...@appspot.gserviceaccount.com (2022-06-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/e31f63e09adafa2cb53c58d9f31254790a8c1bd3

commit e31f63e09adafa2cb53c58d9f31254790a8c1bd3
Author: Christoph Schwering <schwering@google.com>
Date: Mon Jun 27 21:41:38 2022

Revert "[Autofill] Enable AutofillIgnoreEarlyClicksOnPopup by default."

This reverts commit 82e19da8a519522893be8aa5651d689fa5957a00.

Reason for revert: after revisiting the timeout question, we want
to do one more round on 50% stable.

Original change's description:
> [Autofill] Enable AutofillIgnoreEarlyClicksOnPopup by default.
>
> Bug: 1279268
> Change-Id: I0f0b5cd39cf791c292d2baf1f63f00f3bf265ad2
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3688112
> Auto-Submit: Christoph Schwering <schwering@google.com>
> Commit-Queue: Christoph Schwering <schwering@google.com>
> Reviewed-by: Mohamed Amir Yosef <mamir@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#1010234}

Bug: 1279268
Change-Id: I31cc671c49b6196d23b43e72802b35b265372bb8
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3726461
Auto-Submit: Christoph Schwering <schwering@google.com>
Reviewed-by: Mohamed Amir Yosef <mamir@chromium.org>
Commit-Queue: Christoph Schwering <schwering@google.com>
Cr-Commit-Position: refs/heads/main@{#1018415}

[modify] https://crrev.com/e31f63e09adafa2cb53c58d9f31254790a8c1bd3/components/autofill/core/common/autofill_features.cc
[modify] https://crrev.com/e31f63e09adafa2cb53c58d9f31254790a8c1bd3/testing/variations/fieldtrial_testing_config.json


### gi...@appspot.gserviceaccount.com (2022-06-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/74650104e18a2c3e8a0e2c89518897d00f14e233

commit 74650104e18a2c3e8a0e2c89518897d00f14e233
Author: Christoph Schwering <schwering@google.com>
Date: Mon Jun 27 23:43:43 2022

[Autofill] Add fieldtrial testing config for AutofillIgnoreEarlyClicksOnPopup.

Bug: 1279268
Change-Id: I812075118488c2cb954ac3d4888909ec51ee21f1
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3726351
Commit-Queue: Christoph Schwering <schwering@google.com>
Auto-Submit: Christoph Schwering <schwering@google.com>
Quick-Run: Christoph Schwering <schwering@google.com>
Commit-Queue: Mohamed Amir Yosef <mamir@chromium.org>
Reviewed-by: Mohamed Amir Yosef <mamir@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1018464}

[modify] https://crrev.com/74650104e18a2c3e8a0e2c89518897d00f14e233/testing/variations/fieldtrial_testing_config.json


### da...@chromium.org (2022-07-05)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-03)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-08-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/d22dc7ad996cedc6e775087cf7b19a9ce47240a8

commit d22dc7ad996cedc6e775087cf7b19a9ce47240a8
Author: Christoph Schwering <schwering@google.com>
Date: Wed Aug 03 22:44:36 2022

[Autofill] Enable AutofillIgnoreEarlyClicksOnPopup by default.

Bug: 1279268
Change-Id: Ife3ca29926508354cdcc03c3660a7b6eae0b987b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3807505
Commit-Queue: Christoph Schwering <schwering@google.com>
Reviewed-by: Elizabeth Popova <lizapopova@google.com>
Auto-Submit: Christoph Schwering <schwering@google.com>
Cr-Commit-Position: refs/heads/main@{#1031252}

[modify] https://crrev.com/d22dc7ad996cedc6e775087cf7b19a9ce47240a8/components/autofill/core/common/autofill_features.cc


### gi...@appspot.gserviceaccount.com (2022-09-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/fcf24d6de4e9a2277a596873d3e7d5bbaa0c97d4

commit fcf24d6de4e9a2277a596873d3e7d5bbaa0c97d4
Author: Christoph Schwering <schwering@google.com>
Date: Fri Sep 02 17:31:25 2022

[Autofill] Clean up AutofillIgnoreEarlyClicksOnPopup.

Bug: 1279268, 1356532
Change-Id: Id63c11f041d3ed40edf253de2631fe2d2a78ece8
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3810272
Auto-Submit: Christoph Schwering <schwering@google.com>
Commit-Queue: Mohamed Amir Yosef <mamir@chromium.org>
Reviewed-by: Vidhan Jain <vidhanj@google.com>
Reviewed-by: Mohamed Amir Yosef <mamir@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1042644}

[modify] https://crrev.com/fcf24d6de4e9a2277a596873d3e7d5bbaa0c97d4/components/autofill/core/common/autofill_features.cc
[modify] https://crrev.com/fcf24d6de4e9a2277a596873d3e7d5bbaa0c97d4/testing/variations/fieldtrial_testing_config.json
[modify] https://crrev.com/fcf24d6de4e9a2277a596873d3e7d5bbaa0c97d4/tools/metrics/histograms/metadata/autofill/histograms.xml
[modify] https://crrev.com/fcf24d6de4e9a2277a596873d3e7d5bbaa0c97d4/chrome/browser/ui/views/autofill/autofill_popup_view_native_views.cc
[modify] https://crrev.com/fcf24d6de4e9a2277a596873d3e7d5bbaa0c97d4/components/autofill/core/browser/metrics/autofill_metrics.h
[modify] https://crrev.com/fcf24d6de4e9a2277a596873d3e7d5bbaa0c97d4/components/autofill/core/common/autofill_features.h
[modify] https://crrev.com/fcf24d6de4e9a2277a596873d3e7d5bbaa0c97d4/components/autofill/core/browser/metrics/autofill_metrics.cc


### al...@alesandroortiz.com (2022-09-08)

schwering@: Thanks for taking another look at this!

Verified as fixed in 107.0.5288.1 Canary with 500ms delay set in https://crbug.com/chromium/1279268#c43 commit, and also seems fixed in 105.0.5195.53 Stable (presumably via remote config setting the delay to 500ms).

I'll defer to owner and security team on when to disclose this crbug, since it already seems fixed in Stable therefore probably can be disclosed sooner than 14 weeks from today.

### [Deleted User] (2022-09-28)

[Empty comment from Monorail migration]

### fl...@google.com (2022-10-06)

This is landed in stable and fixed; marking it Fixed accordingly.

Given that there's been cleanup work in the meantime, I'll let it default to the 14 week countdown starting fromt he day it's marked fixed; Sheriffbot should make it public on January 12th.

### ad...@google.com (2022-10-06)

As it happens it's RestrictView-SecurityEmbargo which means our dear Sheriffbot won't open it up automatically. We should remove RV-SE at a similar time, so I've set NextAction.

### am...@chromium.org (2022-12-14)

Given the ongoing work to fully resolve this issue, the automation was not able to tag and include this issue for release notes and CVE processing when it was finally resolved. It appears this issue was mitigated in M107/Stable. Labeling accordingly and this will allow for this issue to be updated in release notes and CVE in coming days. 

### [Deleted User] (2023-01-13)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### al...@alesandroortiz.com (2023-01-13)

I think embargo can be removed on this, per https://crbug.com/chromium/1279268#c46.

### am...@chromium.org (2023-01-13)

[Empty comment from Monorail migration]

### pg...@google.com (2023-02-12)

[Empty comment from Monorail migration]

### pg...@google.com (2023-07-28)

[Empty comment from Monorail migration]

### pg...@google.com (2023-07-28)

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

This issue was migrated from crbug.com/chromium/1279268?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Privacy, UI>Browser>Autofill>UI]
[Monorail blocked-on: crbug.com/chromium/1341430]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058217)*
