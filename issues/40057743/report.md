# Security: UAF in SharingHub

| Field | Value |
|-------|-------|
| **Issue ID** | [40057743](https://issues.chromium.org/issues/40057743) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | UI>Browser>Sharing |
| **Platforms** | ChromeOS |
| **Reporter** | le...@gmail.com |
| **Assignee** | kr...@chromium.org |
| **Created** | 2021-10-28 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**

I think this bug was caused by this submission: <https://source.chromium.org/chromium/chromium/src/+/f50ae42daa8b4d22db68202a38afa9dc17680b06>

|OnSharesheetClosed| is bound[1] as a callback function |close\_callback\_|.

When class |SharingHubBubbleController| is destructing, the |CloseBubble| function[2] will be called. It will finally call |CloseWidgetWithAnimateFadeOut|[3], and bind[4] |CloseWidgetWithReason| as a callback function into ClosureAnimationObserver.

After that, |CloseBubble| executed completed and |SharingHubBubbleController| got destructed.

Then the close animation is complete, and the callback function |close\_callback\_| will be run[5].

The UAF will be triggered when the member variable of |SharingHubBubbleController| gets accessed[6].

[1]. <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/sharing_hub/sharing_hub_bubble_controller.cc;l=250;drc=9ae9ed4ac1d95f497b5a96e30fe389931f66946d>  

[2]. <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/sharing_hub/sharing_hub_bubble_controller.cc;l=81;drc=9ae9ed4ac1d95f497b5a96e30fe389931f66946d>  

[3]. <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/ash/sharesheet/sharesheet_bubble_view.cc;l=703;drc=54cf9f5d213529f4d01a59d8a51e8c266af22138>  

[4]. <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/ash/sharesheet/sharesheet_bubble_view.cc;l=722;drc=54cf9f5d213529f4d01a59d8a51e8c266af22138>  

[5]. <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/ash/sharesheet/sharesheet_bubble_view.cc;l=732;drc=54cf9f5d213529f4d01a59d8a51e8c266af22138>  

[6]. <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/sharing_hub/sharing_hub_bubble_controller.cc;l=267;drc=9ae9ed4ac1d95f497b5a96e30fe389931f66946d>

Above all, ~SharingHubBubbleController => CloseBubble => CloseWidgetWithAnimateFadeOut => ~SharingHubBubbleController Done => close animation done => CloseWidgetWithReason => OnSharesheetClosed => UAF triggered

**VERSION**  

Chrome Version: stable with ChromeOSSharingHub feature flag[\*], this flag is enabled by default in the development version  

Operating System: ChromeOS

[\*] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/common/chrome_features.cc;l=911;bpv=1;bpt=0;drc=028804eacce58120729a00c1b1b828a0e3188a30>

**REPRODUCTION CASE**

$ python -m SimpleHTTPServer  

$ out/asan/chrome --user-data-dir=/tmp/xxxx "<http://localhost:8000/poc.html>"  

Click the "share" icon in the location bar

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: browser  

Crash State: see asan file

**CREDIT INFORMATION**  

Reporter credit: Leecraso and Guang Gong of 360 Alpha Lab

## Attachments

- [asan](attachments/asan) (text/plain, 24.5 KB)
- [poc.html](attachments/poc.html) (text/plain, 123 B)

## Timeline

### [Deleted User] (2021-10-28)

[Empty comment from Monorail migration]

### le...@gmail.com (2021-10-28)

Correction: beta with ChromeOSSharingHub feature flag, not yet merged into stable version.

### da...@chromium.org (2021-10-28)

[Empty comment from Monorail migration]

[Monorail components: UI>Browser>Sharing]

### da...@chromium.org (2021-10-28)

See the asan attachment in #0 for the stack traces.

Thanks for the high quality report, leecraso@.

If the blamed CL is correct, this was introduced in M96. If another CL caused it please update the release it occured in!

### [Deleted User] (2021-10-28)

[Empty comment from Monorail migration]

### da...@chromium.org (2021-10-28)

You may consider using base::SafeRef for ViewTracker::view_ so that such crashes in the future would not be security vulnerabilities.

### je...@chromium.org (2021-10-28)

@ellyjones, is this the same bug as 1249491 ?

### el...@chromium.org (2021-10-28)

#7: Basically yes - there is a whole cloud of bugs around Sharing Hub & the CrOS share sheet since the lifetimes on them are very weird.

### kr...@chromium.org (2021-10-28)

[Empty comment from Monorail migration]

### kr...@chromium.org (2021-10-28)

[Empty comment from Monorail migration]

### kr...@chromium.org (2021-10-28)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-10-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/617f27e56acfe2e4849125da3670fc91db5ae995

commit 617f27e56acfe2e4849125da3670fc91db5ae995
Author: Kristi Park <kristipark@chromium.org>
Date: Thu Oct 28 21:54:40 2021

[CrOSSharingHub] Prevent UAF callback to destructed controller

When SharingHubBubbleController is destroyed by WebContents, it calls
CloseBubble on SharesheetBubbleView if the Sharesheet is still open.
However, SharesheetBubbleView will attempt to invoke a callback to the
freed controller in order to notify it that the bubble was closed.

Prevent this by using base::WeakPtr for the callback instead of
base::Unretained.

Bug: 1264282
Change-Id: I1a1fda8d40bfd1d5a76652bdc9068b61aa0ce016
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3251711
Reviewed-by: Elly Fong-Jones <ellyjones@chromium.org>
Commit-Queue: Kristi Park <kristipark@chromium.org>
Cr-Commit-Position: refs/heads/main@{#936123}

[modify] https://crrev.com/617f27e56acfe2e4849125da3670fc91db5ae995/chrome/browser/ui/sharing_hub/sharing_hub_bubble_controller.cc
[modify] https://crrev.com/617f27e56acfe2e4849125da3670fc91db5ae995/chrome/browser/ui/sharing_hub/sharing_hub_bubble_controller.h


### kr...@chromium.org (2021-10-28)

[Empty comment from Monorail migration]

### kr...@chromium.org (2021-10-28)

Preemptive merge request to 96

### da...@chromium.org (2021-10-29)

Thank you for the quick fix. Can you confirm that this bug was first introduced in M96?

### [Deleted User] (2021-10-29)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-29)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-10-29)

[Empty comment from Monorail migration]

### da...@chromium.org (2021-10-29)

> Thank you for the quick fix. Can you confirm that this bug was first introduced in M96?

Bump.


### el...@chromium.org (2021-10-29)

The culprit CL for this bug, f50ae42daa8b4d22db68202a38afa9dc17680b06, is in 96.0.4651.0 and later. However, there may have been similar UAFs (albeit with different trigger conditions) in 95 or 94 - eg, it's hard to prove e0e1b4522a43cfeb146bd2c8f3dea922fcc27509 doesn't have a similar problem.

### ad...@google.com (2021-10-29)

Sheriffbot removed the merge request due to a known sheriffbot bug -  https://crbug.com/chromium/1264282.

Re-adding on the assumption that this does not affect older than M96.

### ad...@chromium.org (2021-10-29)

oops, that should have been https://crbug.com/chromium/1253642

### da...@chromium.org (2021-10-29)

Thanks elly

### [Deleted User] (2021-10-29)

Merge review required: M96 is already shipping to beta.

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

### kr...@chromium.org (2021-10-29)

1. Security vulnerability fix
2. https://chromium-review.googlesource.com/c/chromium/src/+/3251711
3.  Yes
4.  Yes, behind a finch flag. Experiment active 10% stable.
5.  No applicable eng prod representative
6.  N/A

### dg...@google.com (2021-11-01)

Marking as merge rejected for M96. Experiments/new features should be disabled if causing issues on a branch as we do not accept these types of changes after branch. See go/cros-merge-guidelines#newfeatures.

Is this the same issue reported in crbug/1264703 ?

### dg...@google.com (2021-11-01)

[Empty comment from Monorail migration]

### dg...@google.com (2021-11-01)

[Empty comment from Monorail migration]

### dg...@google.com (2021-11-01)

Reopening for https://crbug.com/chromium/1264282#c26

### kr...@chromium.org (2021-11-01)

https://crbug.com/chromium/1264282#c26 This bug is separate from https://crbug.com/chromium/1264703

### da...@chromium.org (2021-11-02)

> Marking as merge rejected for M96. Experiments/new features should be disabled if causing issues on a branch as we do not accept these types of changes after branch.

Should we open a different P0 bug to disable the experiment?

### dg...@google.com (2021-11-02)

I filed crbug/1265989: Disable UAF in SharingHub Experiment in M96 (see crbug/1264282) to disable the experiment.

### am...@google.com (2021-11-03)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-11-03)

Hi leecraso@ another report (https://crbug.com/chromium/1261516) for this issue was filed earlier than this one. We did; however, did see specific value in your report that allowed this bug to be quickly triaged as well as accelerating root cause identification and fix. So while typically the later reported duplicate would not be eligible for VRP Panel, in this specific case we have evaluated both reports and wanted to extend a $5000 reward to you for this report. Thank you for your report!

### am...@chromium.org (2021-11-03)

[Comment Deleted]

### am...@google.com (2021-11-04)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-08)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### is...@google.com (2023-05-24)

This issue was migrated from crbug.com/chromium/1264282?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/1261516, crbug.com/chromium/1263252]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057743)*
