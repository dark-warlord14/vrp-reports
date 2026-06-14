# URL is updated incorrectly when navigating to external app urls

| Field | Value |
|-------|-------|
| **Issue ID** | [40095364](https://issues.chromium.org/issues/40095364) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Unknown |
| **Platforms** | iOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | eu...@chromium.org |
| **Created** | 2019-06-11 |
| **Bounty** | $500.00 |

## Description

Splitting https://crbug.com/chromium/973056#c2 from original report http://crbug/972411

App Version: M75.0.377.0 stable
iOS Version: 12.4
Device: iPhoneX
URL: 

Steps to reproduce:
  1. Launch Google Chrome
  2. Goto google.com
  3. Goto https://lbstyle.github.io/spoof.html in the same tab
  4. Tap on Cancel and Wait

Observed results: Observe that URL is updated incorrectly ti lbstyle.github but content page still shows google.com

Expected results: URL and Content area should always match

Reported by external user at http://crbug/972411


## Timeline

### sr...@chromium.org (2019-06-11)

cc'ing the original reporter of the bug. [chromium.khalil]

### eu...@chromium.org (2019-06-11)

Fixed here: https://bugs.chromium.org/p/chromium/issues/detail?id=972411#c12

### eu...@chromium.org (2019-06-11)

Mustafa, could you please help to asses severity for this security bug. Thank you!

### me...@chromium.org (2019-06-11)

Eugene: I think this should be the same as https://crbug.com/chromium/972411. It's currently marked severity-high but I left a comment saying it could be medium.

### eu...@chromium.org (2019-06-11)

Thank you Mustafa! Requesting cherry-pick then. Srikanth, could you please retest the fix with the latest canary. 

### me...@chromium.org (2019-06-11)

(Let's mark this as medium in the meanwhile.)

### sh...@chromium.org (2019-06-12)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-06-12)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-06-12)

Your change meets the bar and is auto-approved for M76. Please go ahead and merge the CL to branch 3809 (refs/branch-heads/3809) manually. Please contact milestone owner if you have questions.
Merge instructions: https://www.chromium.org/developers/how-tos/drover
Owners: govind@(Android), kariahda@(iOS), cindyb@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ka...@google.com (2019-06-13)

This bug has been approved for a merge. Please merge asap to give the fixes time to bake on beta. Thanks.

### eu...@chromium.org (2019-06-13)

The fix was merged here: https://bugs.chromium.org/p/chromium/issues/detail?id=972411#c23

### sr...@chromium.org (2019-06-13)

I verified the repro steps on M770.3824.0 canary.
The bug is FIXED with SlimNav OFF.
But the same steps still reproduces the bug when SlimNav is ON.

Eugene, can you please let me know if this is expected?

### ka...@google.com (2019-06-13)

[Empty comment from Monorail migration]

### eu...@chromium.org (2019-06-13)

I think slim nav issue is a separate one. Justin, do you think your fix addresses this problem? We should probably file a separate bug for this anyway.

### sr...@chromium.org (2019-06-13)

Thanks for the clarification. I will mark this as Verified. and file a new bug for SlimNav ON case.

### ch...@gmail.com (2019-06-17)

[Comment Deleted]

### ch...@gmail.com (2019-06-17)

Qualified for reward-topanel?

### ct...@chromium.org (2019-06-19)

Should be -- added the label so it goes to the panel.

### ju...@chromium.org (2019-06-25)

[Empty comment from Monorail migration]

### ch...@gmail.com (2019-07-31)

Any update on reward-topanel? - Thanks.

### na...@google.com (2019-08-01)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### pa...@chromium.org (2019-08-01)

Congrats! The Panel decided to reward you $500 for this report! 

### na...@google.com (2019-08-01)

[Empty comment from Monorail migration]

### pa...@chromium.org (2019-08-01)

srikanthg@chromium.org - please let me know how you would like to be credited in our release notes 

### sr...@chromium.org (2019-08-01)

reply#24
chromium.khalil@gmail.com is the original reporter of the bug in 972411.
I split the bug into two different versions to track the fixes.

### ad...@google.com (2019-09-09)

I am marking this as released in M77 to ensure credits appear in the release notes, although in fact it looks like at least one of the commits from https://crbug.com/chromium/972411 was merged to M76.

### ad...@google.com (2019-09-09)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-09-09)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-09-18)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@chromium.org (2019-11-23)

[Empty comment from Monorail migration]

### sr...@chromium.org (2019-12-13)

+Subha for verification

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/973056?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/976933]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095364)*
