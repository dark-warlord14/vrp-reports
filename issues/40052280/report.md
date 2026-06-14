# Security: URL spoofing using slow page loading on iOS

| Field | Value |
|-------|-------|
| **Issue ID** | [40052280](https://issues.chromium.org/issues/40052280) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Mobile>iOSWeb>PageLoad, UI>Browser>Navigation, UI>Browser>Omnibox |
| **Platforms** | iOS |
| **Reporter** | ra...@gmail.com |
| **Assignee** | ga...@google.com |
| **Created** | 2020-05-11 |
| **Bounty** | $500.00 |

## Description

1. click the poc
2. Click on the button
3. Spoofed




## Attachments

- [poc.html](attachments/poc.html) (text/plain, 439 B)
- [poc.html](attachments/poc_53203716.html) (text/plain, 439 B)
- [URLSpoof.mp4](attachments/URLSpoof.mp4) (video/mp4, 837.9 KB)

## Timeline

### ra...@gmail.com (2020-05-11)

[Comment Deleted]

### ra...@gmail.com (2020-05-11)

Okay this is bug regression: https://crbug.com/chromium/925598

Ps. I used one of the project's member URL for the slow loading website to maximise the attacking time.

### oc...@google.com (2020-05-11)

gambard, could you please take a look?  It looks like the mitigation implemented in https://crbug.com/chromium/925598 is in place here, although as can be seen in the video if you navigate away and back the progress bar resets to 0 and may not be as noticeable. 

Should we just merge this into https://crbug.com/chromium/938221? Or are there more mitigations possible? 

[Monorail components: Mobile>iOSWeb>PageLoad UI>Browser>Navigation UI>Browser>Omnibox]

### ga...@chromium.org (2020-05-11)

+creis@ from discussion on the other bug, to assess severity.
From my understanding the issue here is that the progress bar isn't correctly updated when changing tab. What happens is:
1. Load facebook.com and prevent the load from finishing after it is committed. At this point the content being displayed is the previous content, but the page is not interactable.
2. The user switch to another tab
3. The user switch back to the tab opened in #1.

The progress bar is displayed but with a progress of 0. The content displayed is still the malicious content, but the page is not interactable. The URL is facebook.com.

I will fix the progress bar issue.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-05-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/e77b87526e6523719e819988b8fefbcbe1f7e643

commit e77b87526e6523719e819988b8fefbcbe1f7e643
Author: Gauthier Ambard <gambard@chromium.org>
Date: Mon May 11 17:19:03 2020

[iOS] Fix progress bar when changing tab

This CL makes sure that the ProgressBar's progress is updated correctly
when the user switches tabs.

Fixed: 1081081
Change-Id: If6d4534b943aea661636ef9254777291abe539cd
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2193013
Commit-Queue: Gauthier Ambard <gambard@chromium.org>
Commit-Queue: Robbie Gibson <rkgibson@google.com>
Auto-Submit: Gauthier Ambard <gambard@chromium.org>
Reviewed-by: Robbie Gibson <rkgibson@google.com>
Cr-Commit-Position: refs/heads/master@{#767366}

[modify] https://crrev.com/e77b87526e6523719e819988b8fefbcbe1f7e643/ios/chrome/browser/ui/toolbar/toolbar_mediator.mm


### [Deleted User] (2020-05-11)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-05-11)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-05-11)

[Empty comment from Monorail migration]

### ra...@gmail.com (2020-05-12)

Hi, According to https://www.chromium.org/developers/severity-guidelines, This bug falls into  the "Complete control over the apparent origin in the omnibox" which is high. 

### ga...@chromium.org (2020-05-13)

Letting security folks answer this comment.

### cr...@chromium.org (2020-05-14)

https://crbug.com/chromium/1081081#c9: Thanks for the report, and for the progress bar fix from gambard@!  I agree with the medium severity rating from https://crbug.com/chromium/1081081#c3, due to the mitigating factors involved.  (See the example of "An address bar spoof where only certain URLs can be displayed, or with other mitigating factors" under Medium Severity at https://chromium.googlesource.com/chromium/src/+/master/docs/security/severity-guidelines.md.)

Here, the main mitigating factor is that the spoof page becomes non-interactive.  There's also an (i) instead of a padlock in the address bar, so Chrome isn't claiming the page to be secure yet.  (Technically, the progress bar is still visible at 0%, but I wouldn't count that as much of a mitigating factor-- no one would really notice that as a basis for thinking the page is still loading.)

### cr...@chromium.org (2020-05-14)

Is this also related to https://crbug.com/chromium/938221 and https://crbug.com/chromium/1076874?  The facebook URL looks like it commits but doesn't get a chance to paint.  If we could blank out the old page after a delay, this would presumably be less of an issue.

### ra...@gmail.com (2020-05-14)

[Comment Deleted]

### ra...@gmail.com (2020-05-14)

[Comment Deleted]

### ra...@gmail.com (2020-05-19)

[Comment Deleted]

### na...@google.com (2020-05-19)

[Empty comment from Monorail migration]

### [Deleted User] (2020-05-19)

Requesting merge to beta M83 because latest trunk commit (767366) appears to be after beta branch point (756066).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-05-19)

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
Owners: benmason@(Android), bindusuvarna@(iOS), cindyb@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### na...@google.com (2020-05-21)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-05-21)

Congrats! The Panel decided to award $500 for this report

### bi...@google.com (2020-05-21)

[Comment Deleted]

### bi...@google.com (2020-05-21)

[Empty comment from Monorail migration]

### bi...@google.com (2020-05-21)

adetaylor@ PTAL 

### [Deleted User] (2020-05-21)

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
Owners: benmason@(Android), bindusuvarna@(iOS), cindyb@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2020-05-21)

I am approving merge to M83, branch 4103, as it seems there _may_ be an imminent iOS refresh and this fix is very straightforward. Otherwise, this won't get released till M84 and that's OK with me.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-05-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/45894694dfd037f59dda76f63ab18018e1d9433b

commit 45894694dfd037f59dda76f63ab18018e1d9433b
Author: Gauthier Ambard <gambard@chromium.org>
Date: Fri May 22 04:58:26 2020

[iOS] Fix progress bar when changing tab

This CL makes sure that the ProgressBar's progress is updated correctly
when the user switches tabs.

(cherry picked from commit e77b87526e6523719e819988b8fefbcbe1f7e643)

Fixed: 1081081
Change-Id: If6d4534b943aea661636ef9254777291abe539cd
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2193013
Commit-Queue: Gauthier Ambard <gambard@chromium.org>
Commit-Queue: Robbie Gibson <rkgibson@google.com>
Auto-Submit: Gauthier Ambard <gambard@chromium.org>
Reviewed-by: Robbie Gibson <rkgibson@google.com>
Cr-Original-Commit-Position: refs/heads/master@{#767366}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2213109
Reviewed-by: Krishna Govind <govind@chromium.org>
Commit-Queue: Krishna Govind <govind@chromium.org>
Cr-Commit-Position: refs/branch-heads/4103@{#592}
Cr-Branched-From: 8ad47e8d21f6866e4a37f47d83a860d41debf514-refs/heads/master@{#756066}

[modify] https://crrev.com/45894694dfd037f59dda76f63ab18018e1d9433b/ios/chrome/browser/ui/toolbar/toolbar_mediator.mm


### ad...@google.com (2020-05-27)

[Empty comment from Monorail migration]

### ra...@gmail.com (2020-05-29)

[Comment Deleted]

### na...@google.com (2020-05-29)

[Empty comment from Monorail migration]

### ra...@gmail.com (2020-05-29)

[Comment Deleted]

### ad...@google.com (2020-06-02)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-06-03)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-06-03)

[Empty comment from Monorail migration]

### na...@google.com (2020-06-04)

Panel re-assessed as this report to be the same as the original reward value.  



### na...@google.com (2020-06-10)

[Empty comment from Monorail migration]

### na...@google.com (2020-06-22)

[Empty comment from Monorail migration]

### [Deleted User] (2020-08-17)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1081081?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Mobile>iOSWeb>PageLoad, UI>Browser>Navigation, UI>Browser>Omnibox]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-03-19)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40052280)*
