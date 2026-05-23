# Security: UAF in GoogleSearchDomainMixingMetricsEmitter

| Field | Value |
|-------|-------|
| **Issue ID** | [40058303](https://issues.chromium.org/issues/40058303) |
| **Status** | Fixed |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | le...@gmail.com |
| **Assignee** | pk...@chromium.org |
| **Created** | 2021-12-21 |
| **Bounty** | $10,000.00 |

## Description

**VULNERABILITY DETAILS**  

After enable the EmitGoogleSearchDomainMixingMetrics feature, a delayed task with `Unretained(this)` will be post into ui thread[1]. The `task_runner_` comes from `content::GetUIThreadTaskRunner`, so there is no guarantee that this task will not be executed after `GoogleSearchDomainMixingMetricsEmitter` get destructed. When this task is executed after `GoogleSearchDomainMixingMetricsEmitter` is destroyed, the UAF will be triggered.

[1]. <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/google/google_search_domain_mixing_metrics_emitter.cc;l=87;drc=0e45c020c43b1a9f6d2870ff7f92b30a2f03a458>

**VERSION**  

Chrome Version: stable with feature flag: EmitGoogleSearchDomainMixingMetrics  

Operating System: test in Linux & Win

**REPRODUCTION CASE**  

Apply the attached poc.diff \*  

$ python -m SimpleHTTPServer  

$ out/asan/chrome --user-data-dir=/tmp/xxxx "<http://localhost:8000/poc.html>"

[\*] The time patch aims to ensure that you can trigger the bug when you first run chrome with user-data-dir that does not exist, or you should make sure that you have launched chrome one day ago[2].

Enabling the LogBreadcrumbs feature aims to expand[3] the window time between the destruction of `GoogleSearchDomainMixingMetricsEmitter` and the exit of the browser process, in order to stably trigger this bug without any user gesture, it has nothing to do with the bug itself.  

Or you can trigger it through user interaction as demo.mp4: create a new account to open a new window and close the new window.

[2]. <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/google/google_search_domain_mixing_metrics_emitter.cc;l=90;drc=b0ca279cada36205f1d4a6e5f730f249ea07a6c0>  

[3]. <https://source.chromium.org/chromium/chromium/src/+/main:components/breadcrumbs/core/breadcrumb_persistent_storage_manager.cc;l=328;drc=78c2388afd6944e1084ffcc4bedf2105863aa14a>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: browser  

Crash State: see asan file

**CREDIT INFORMATION**  

Reporter credit: Leecraso and Guang Gong of 360 Alpha Lab

## Attachments

- [asan](attachments/asan) (text/plain, 13.3 KB)
- [poc.diff](attachments/poc.diff) (text/plain, 2.3 KB)
- [poc.html](attachments/poc.html) (text/plain, 140 B)
- [demo.mp4](attachments/demo.mp4) (video/mp4, 3.9 MB)

## Timeline

### [Deleted User] (2021-12-21)

[Empty comment from Monorail migration]

### me...@chromium.org (2021-12-21)

Thanks for the report.

qfiard seems to be the owner of this code, but he's OOO. pkasting, could you PTAL in the meantime?

I'm setting impact=none since the feature is disabled by default.

[Monorail components: Infra>Codesearch]

### me...@chromium.org (2021-12-21)

[Empty comment from Monorail migration]

[Monorail components: -Infra>Codesearch Internals]

### pk...@chromium.org (2022-01-10)

Seems easy enough to patch with a weak pointer factory.

### pk...@chromium.org (2022-01-10)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-01-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/33c7a83130858bbd922ccaef1e9acf29e385acb2

commit 33c7a83130858bbd922ccaef1e9acf29e385acb2
Author: Peter Kasting <pkasting@chromium.org>
Date: Tue Jan 11 02:08:44 2022

Use a weak pointer factory for metrics emitter tasks.

This prevents UAF if the emitter is destroyed before the tasks run.

Bug: 1281763
Change-Id: I2c5255e72c2780b2b4fa60ba15b13c4c5a56fcf6
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3378382
Auto-Submit: Peter Kasting <pkasting@chromium.org>
Reviewed-by: Ilya Sherman <isherman@chromium.org>
Commit-Queue: Ilya Sherman <isherman@chromium.org>
Cr-Commit-Position: refs/heads/main@{#957378}

[modify] https://crrev.com/33c7a83130858bbd922ccaef1e9acf29e385acb2/chrome/browser/google/google_search_domain_mixing_metrics_emitter.cc
[modify] https://crrev.com/33c7a83130858bbd922ccaef1e9acf29e385acb2/chrome/browser/google/google_search_domain_mixing_metrics_emitter.h


### le...@gmail.com (2022-01-11)

yes, and the fix works in my test, I think the issue could be marked as fixed.

### pk...@chromium.org (2022-01-11)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-12)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-12)

[Empty comment from Monorail migration]

### am...@google.com (2022-01-20)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-01-20)

Congratulations, leecraso! The VRP Panel has decided to award you $10,000 for this report. Great work! 

### am...@google.com (2022-01-22)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-19)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2022-04-19)

This issue was migrated from crbug.com/chromium/1281763?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058303)*
