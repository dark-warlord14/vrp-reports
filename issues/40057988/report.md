# Security: HeapOverflow in PageLoadMetrics

| Field | Value |
|-------|-------|
| **Issue ID** | [40057988](https://issues.chromium.org/issues/40057988) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>Navigation>BFCache |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | le...@gmail.com |
| **Assignee** | ha...@chromium.org |
| **Created** | 2021-11-22 |
| **Bounty** | $15,000.00 |

## Description

**VULNERABILITY DETAILS**

In function |DispatchEventsAfterBackForwardCacheRestore|[1], when visiting |new\_timings|, |i| will be passed into |OnFirstInputAfterBackForwardCacheRestoreInPage|[2], and finally as the index to access |back\_forward\_cache\_restores\_|[3] and |back\_forward\_cache\_navigation\_ids\_|[4].

The |new\_timings| could be updated through the mojo IPC Call |UpdateTiming|[5], so we can trigger the out-of-bounds by constructing the size of the array |back\_forward\_cache\_timings|[6].

[1]. <https://source.chromium.org/chromium/chromium/src/+/main:components/page_load_metrics/browser/page_load_tracker.cc;l=136;drc=4ad3249a94f386ee2d5c8509cea424e5538bb173>  

[2]. <https://source.chromium.org/chromium/chromium/src/+/main:components/page_load_metrics/browser/page_load_tracker.cc;l=167;drc=4ad3249a94f386ee2d5c8509cea424e5538bb173>  

[3]. <https://source.chromium.org/chromium/chromium/src/+/main:components/page_load_metrics/browser/page_load_tracker.cc;l=925;drc=4ad3249a94f386ee2d5c8509cea424e5538bb173>  

[4]. <https://source.chromium.org/chromium/chromium/src/+/main:components/page_load_metrics/browser/observers/back_forward_cache_page_load_metrics_observer.cc;l=630;drc=3233aff82f01ca09e58cca68917979460de336fd>  

[5]. <https://source.chromium.org/chromium/chromium/src/+/main:components/page_load_metrics/common/page_load_metrics.mojom;l=392;drc=e0bcd799231fef912ab8d1fa938aab46c022b273>  

[6]. <https://source.chromium.org/chromium/chromium/src/+/main:components/page_load_metrics/common/page_load_metrics.mojom;l=163;drc=739200ab4a3bb86eefcc1aa6d74fd65530618f56>

And because it will compare the contents of the out-of-bounds access with the controllable input[7], the attacker can leak memory data through the difference of the code execution time in different branches.

I also attached the exploit code demo in the following files, it could leak 8 bytes of data in 10+s without any user gesture.

[7]. <https://source.chromium.org/chromium/chromium/src/+/main:components/page_load_metrics/browser/page_load_metrics_util.cc;l=133;drc=5f3febba100f999ed17423e0e030d040e20c8204>

Fix suggestion: suggestion.diff

**VERSION**  

Chrome Version: stable  

Operating System: All

**REPRODUCTION CASE**

Apply the attached poc.diff  

$ python -m SimpleHTTPServer 8000  

$ python -m SimpleHTTPServer 8001  

$ out/asan/chrome --user-data-dir=/tmp/xxxx "<http://localhost:8000/poc.html>"

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: browser  

Crash State: see asan file

**CREDIT INFORMATION**  

Reporter credit: Leecraso and Guang Gong of 360 Alpha Lab

## Attachments

- [asan](attachments/asan) (text/plain, 26.9 KB)
- [poc.diff](attachments/poc.diff) (text/plain, 9.0 KB)
- [poc.html](attachments/poc.html) (text/plain, 468 B)
- [page2.html](attachments/page2.html) (text/plain, 192 B)
- deleted (application/octet-stream, 0 B)
- [suggestion.diff](attachments/suggestion.diff) (text/plain, 1.7 KB)

## Timeline

### [Deleted User] (2021-11-22)

[Empty comment from Monorail migration]

### mp...@chromium.org (2021-11-22)

It seems the DCHECK here: https://source.chromium.org/chromium/chromium/src/+/main:components/page_load_metrics/browser/page_load_tracker.cc;drc=de68be3f18ba99cc01d75903e167ca09bade253c;l=134
Probably should not be a DCHECK but instead should be something like mojo::ReportBadMessage().

It looks like this is only triggerable from a compromised renderer and provides a noisy "less than" primitive on an out-of-bounds read. I think attempting an information leak here would be very difficult given that it relies on measuring execution timing (for a non-synchronous mojo message) and it requires some very very precise massaging of the heap (and probably the ability to allocate copies of the secret data over and over). So I'll mark this as Severity_Medium.

[Monorail components: UI>Browser>Navigation>BFCache]

### [Deleted User] (2021-11-22)

[Empty comment from Monorail migration]

### le...@gmail.com (2021-11-23)

[Comment Deleted]

### mp...@chromium.org (2021-11-23)

> This dcheck is irrelevant to the vulnerability, it even could ensure that the size of new_timings become larger.
True though this should still be a mojo::ReportBadMessage(). Your proposed patch works but I wonder if there's a less error-prone way to mojo::ReportBadMessage() as soon as possible in case small code-path changes reopen this vulnerability.

>  In fact it is not the case
Thank you! Yes I misinterpreted how |i| was being used. 70% in 10s is quite high and could presumably be improved. I'll bump this to High Severity as it amounts to an OOB read in the browser process and we'll want to make sure merges are applied as quickly as possible.

### al...@google.com (2021-11-23)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-23)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-11-23)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@chromium.org (2021-11-24)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-11-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/1059bf191cc8c7a8a10fd667522b6949e8de0f35

commit 1059bf191cc8c7a8a10fd667522b6949e8de0f35
Author: Hajime Hoshi <hajimehoshi@chromium.org>
Date: Wed Nov 24 15:26:07 2021

Fix a possible out-of-bound access in components/page_load_metrics

`new_timings` is iterated at
`DispatchEventsAfterBackForwardCacheRestore` and the index is used for
`back_forward_cache_restores_` at
`PageLoadTracker::GetBackForwardCacheRestore`.  On the other hand,
`new_timings` can be updated via mojo message
`PageLoadMetrics.UpdateTiming`, then in theory it is possible to make
`new_timings` larger than `back_forward_cache_restores_`. This could
cause an out-of-bound access.

This change fixes this out-of-bound access to
`back_forward_cache_restores_` by adding boundary checks.

Bug: 1272403
Change-Id: I9eae03f55b63f353f36d8372930f16034dcea7a4
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3299751
Commit-Queue: Nicolás Peña Moreno <npm@chromium.org>
Reviewed-by: Nicolás Peña Moreno <npm@chromium.org>
Cr-Commit-Position: refs/heads/main@{#944966}

[modify] https://crrev.com/1059bf191cc8c7a8a10fd667522b6949e8de0f35/components/page_load_metrics/browser/observers/back_forward_cache_page_load_metrics_observer.cc
[modify] https://crrev.com/1059bf191cc8c7a8a10fd667522b6949e8de0f35/components/page_load_metrics/browser/page_load_tracker.cc


### ha...@chromium.org (2021-11-25)

[Empty comment from Monorail migration]

### ha...@chromium.org (2021-11-25)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-25)

Merge review required: M97 is already shipping to beta.

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
Owners: benmason (Android), harrysouders (iOS), ceb (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-11-25)

Merge review required: M96 is already shipping to stable.

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
Owners: govind (Android), harrysouders (iOS), dgagnon (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@chromium.org (2021-11-26)

1. This is a critical security fix for the issue that the heap data on browser could be leaked from a compromised renderer.
2. https://chromium-review.googlesource.com/c/chromium/src/+/3299751
3. Yes
4. No
5. n/a
6. No


### am...@chromium.org (2021-11-29)

marking as fixed given commits + completed questionnaire; hajimehoshi@ for future reference, please marked Fixed issues immediately upon fix so sheriffbot can add correct merge request/review labels accordingly, and you won't have to manually request them as well. Thanks! :) 

### am...@chromium.org (2021-11-29)

merge approved for M97; please merge to branch 4692 ASAP so this fix can be included in tomorrow's beta cut 

merge approved for M96; please merge to branch 4664 by EOD Friday, 3 December so this fix can be included in next week's stable respin 

### [Deleted User] (2021-11-30)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-30)

[Empty comment from Monorail migration]

### ha...@chromium.org (2021-12-01)

[Empty comment from Monorail migration]

### ha...@chromium.org (2021-12-01)

I'm now submitting merges:

https://chromium-review.googlesource.com/c/chromium/src/+/3307157
https://chromium-review.googlesource.com/c/chromium/src/+/3307214

### ha...@chromium.org (2021-12-01)

> https://chromium-review.googlesource.com/c/chromium/src/+/3307214

This is for M97 and there are some test failures:
https://ci.chromium.org/ui/p/chromium-m97/builders/try/fuchsia_x64/812/overview

> # Debug check failed: kCanBeWeak || (!IsSmi() == HAS_STRONG_HEAP_OBJECT_TAG(ptr_)).

> # Debug check failed: !node->has_destructor() implies nullptr == node->parameter().

I don't think these are related to my fix. Maybe this is related to crbug.com/1155959.

syg@, do you have any insights?

### gi...@appspot.gserviceaccount.com (2021-12-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/9dd8b9a39e64a3ab90e7957d1225a1955d8da43f

commit 9dd8b9a39e64a3ab90e7957d1225a1955d8da43f
Author: Hajime Hoshi <hajimehoshi@chromium.org>
Date: Fri Dec 03 04:12:48 2021

Fix a possible out-of-bound access in components/page_load_metrics

`new_timings` is iterated at
`DispatchEventsAfterBackForwardCacheRestore` and the index is used for
`back_forward_cache_restores_` at
`PageLoadTracker::GetBackForwardCacheRestore`.  On the other hand,
`new_timings` can be updated via mojo message
`PageLoadMetrics.UpdateTiming`, then in theory it is possible to make
`new_timings` larger than `back_forward_cache_restores_`. This could
cause an out-of-bound access.

This change fixes this out-of-bound access to
`back_forward_cache_restores_` by adding boundary checks.

(cherry picked from commit 1059bf191cc8c7a8a10fd667522b6949e8de0f35)

Bug: 1272403
Change-Id: I9eae03f55b63f353f36d8372930f16034dcea7a4
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3299751
Commit-Queue: Nicolás Peña Moreno <npm@chromium.org>
Reviewed-by: Nicolás Peña Moreno <npm@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#944966}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3307157
Commit-Queue: Hajime Hoshi <hajimehoshi@chromium.org>
Cr-Commit-Position: refs/branch-heads/4664@{#1216}
Cr-Branched-From: 24dc4ee75e01a29d390d43c9c264372a169273a7-refs/heads/main@{#929512}

[modify] https://crrev.com/9dd8b9a39e64a3ab90e7957d1225a1955d8da43f/components/page_load_metrics/browser/observers/back_forward_cache_page_load_metrics_observer.cc
[modify] https://crrev.com/9dd8b9a39e64a3ab90e7957d1225a1955d8da43f/components/page_load_metrics/browser/page_load_tracker.cc


### [Deleted User] (2021-12-03)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2021-12-03)

[Empty comment from Monorail migration]

### ad...@google.com (2021-12-03)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-12-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/bd673db3b1d6b2eaccf3238d7711228a4aa522e3

commit bd673db3b1d6b2eaccf3238d7711228a4aa522e3
Author: Hajime Hoshi <hajimehoshi@chromium.org>
Date: Mon Dec 06 07:43:18 2021

Fix a possible out-of-bound access in components/page_load_metrics

`new_timings` is iterated at
`DispatchEventsAfterBackForwardCacheRestore` and the index is used for
`back_forward_cache_restores_` at
`PageLoadTracker::GetBackForwardCacheRestore`.  On the other hand,
`new_timings` can be updated via mojo message
`PageLoadMetrics.UpdateTiming`, then in theory it is possible to make
`new_timings` larger than `back_forward_cache_restores_`. This could
cause an out-of-bound access.

This change fixes this out-of-bound access to
`back_forward_cache_restores_` by adding boundary checks.

(cherry picked from commit 1059bf191cc8c7a8a10fd667522b6949e8de0f35)

Bug: 1272403
Change-Id: I9eae03f55b63f353f36d8372930f16034dcea7a4
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3299751
Commit-Queue: Nicolás Peña Moreno <npm@chromium.org>
Reviewed-by: Nicolás Peña Moreno <npm@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#944966}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3307214
Commit-Queue: Hajime Hoshi <hajimehoshi@chromium.org>
Cr-Commit-Position: refs/branch-heads/4692@{#738}
Cr-Branched-From: 038cd96142d384c0d2238973f1cb277725a62eba-refs/heads/main@{#938553}

[modify] https://crrev.com/bd673db3b1d6b2eaccf3238d7711228a4aa522e3/components/page_load_metrics/browser/observers/back_forward_cache_page_load_metrics_observer.cc
[modify] https://crrev.com/bd673db3b1d6b2eaccf3238d7711228a4aa522e3/components/page_load_metrics/browser/page_load_tracker.cc


### am...@google.com (2021-12-06)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-12-06)

Congratulations, Leecraso and Guang Gong! The VRP Panel has decided to award you $15,000 for this report. Thank you for your efforts and nice work! 

### le...@gmail.com (2021-12-07)

Thanks for the reward! But there is a little question that confuses me:

This is a report of a vulnerability that can be exploited without any user interaction, with exploit codes and an accepted patch. I'm kind of confused why the bounty is lower than those hard-to-exploit vulnerabilities which may require lots of specific user interaction or almost impossible race competition.

### am...@chromium.org (2021-12-07)

Hi leecraso@, thanks for the question. 
This was actually rewarded higher than the "hard-to-exploit" vulnerabilities that require user interaction, tight race conditions, and/or malicious extension installation, which have been rewarded at $7000-$10,000 on average. 

This issue, while in the browser process, is an OOB access resulting in an 8-byte data leak, so it was also judged as a user information disclosure with a bonus for report quality and exploit than a full memory corruption in a full memory corruption in the browser process. 


### le...@gmail.com (2021-12-07)

Prety thanks for your patient explanation!

### am...@google.com (2021-12-07)

[Empty comment from Monorail migration]

### am...@google.com (2021-12-23)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-08)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1272403?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057988)*
