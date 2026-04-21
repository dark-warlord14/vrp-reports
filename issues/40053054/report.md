# Full CSP bypass by opening a blob URL in a new tab and reloading it with history.back

| Field | Value |
|-------|-------|
| **Issue ID** | [40053054](https://issues.chromium.org/issues/40053054) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>SecurityFeature>ContentSecurityPolicy |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | he...@gmail.com |
| **Assignee** | an...@chromium.org |
| **Created** | 2020-08-11 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

It is possible to bypass the CSP of a page by creating and opening a blob URL in a new tab that will redirect itself to another page and back using a meta redirect and history.back (similar to a page reload).

The blob URL inherits the CSP of the page that opened it, but after a page reload the CSP ends up being discarded, leading to a bypass of the directives that were previously set by the opener - which I believe shouldn't be happening.

**VERSION**  

Chrome Version: 84.0.4147.125 (Official Build)

**REPRODUCTION CASE**

1. Access <https://lbherrera.github.io/lab/chrome-csp/index.html>
2. Click anywhere on the page.
3. After a few seconds, an alert should pop up.

**CREDIT INFORMATION**  

Reporter credit: Luan Herrera (@lbherrera\_)

## Attachments

- [back.html](attachments/back.html) (text/plain, 37 B)
- [csp_bypass.js](attachments/csp_bypass.js) (text/plain, 298 B)
- [index.html](attachments/index.html) (text/plain, 289 B)

## Timeline

### va...@chromium.org (2020-08-12)

Reporter -- could you please attach the source here for us to be able triage the issue? Thanks.

arthursonzogni@ -- this looks somewhat similar to https://crbug.com/chromium/1073126. What do you think?

[Monorail components: Blink>SecurityFeature>ContentSecurityPolicy]

### ar...@chromium.org (2020-08-12)

This is not related to https://crbug.com/chromium/1073126. However, this has some similarities with https://crbug.com/chromium/1109167.

In the case of URLs with local scheme (about, blob, data, javascript, ...), CSP are inherited from the navigation initiator.

The first time the blob document loads, it inherits CSP from its openee.
The second time the blob document loads, this is an history navigation. I am not fully sure, but I think it inherits CSP from "/back.html", which doesn't contain any. The alternative would be inheriting CSP from nowhere, since history navigations are considered to be initiated from the browser process.

+CC mkwst for opinions about this.

If we want to change the behavior/spec, it means we would have to store the "initiator CSP policy" into the history entry.
This would require a lot of work, but that's something I prototyped recently for https://crbug.com/chromium/1109167. This might be possible.

### he...@gmail.com (2020-08-12)

[Comment Deleted]

### he...@gmail.com (2020-08-12)

#1: Sure.

### va...@chromium.org (2020-08-12)

Assigning to mkwst@ per https://crbug.com/chromium/1115298#c2


### va...@chromium.org (2020-08-12)

See also crbug.com/1115628

### [Deleted User] (2020-08-13)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-08-14)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-08-26)

mkwst: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ar...@chromium.org (2020-09-02)

pmeuleman@ and antoniosartori@ are going to improve how a given policy, like
CSP, are inherited across documents/navigations. (PolicyContainer)

There are many CSP bugs around inheritance below:
- https://crbug.com/chromium/1117687
- https://crbug.com/chromium/1115628
- https://crbug.com/chromium/1115298
- https://crbug.com/chromium/1115045
- https://crbug.com/chromium/1109167
- https://crbug.com/chromium/971231
- https://crbug.com/chromium/957606

I believe their future work might fix several issues in this list.

### [Deleted User] (2020-09-09)

mkwst: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-10-07)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-30)

[Empty comment from Monorail migration]

### [Deleted User] (2020-11-18)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-20)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### mk...@google.com (2021-03-01)

Assigning this to Antonio, as it seems pretty clear that the "right" solution is to finish implementing the policy container mechanism, and then to tie such a container to `blob:` (and `filesystem:` URLs) at creation time. That's still going to take some implementation and specification work, both of which are on his plate.

### [Deleted User] (2021-03-03)

[Empty comment from Monorail migration]

### an...@chromium.org (2021-03-04)

[Empty comment from Monorail migration]

### an...@chromium.org (2021-03-05)

This has been fixed by https://chromium-review.googlesource.com/c/chromium/src/+/2725520.

Full test coverage is here https://chromium-review.googlesource.com/c/chromium/src/+/2728996.

### [Deleted User] (2021-03-05)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-05)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-05)

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M89. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-03-05)

This bug requires manual review: Request affecting a post-stable build
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on ToT?
4. Does this change need to be merged into other active release branches (M-1, M+1)?
5. Why are these changes required in this milestone after branch?
6. Is this a new feature?
7. If it is a new feature, is it behind a flag using finch?

Chrome OS Only:
8. Was the change reviewed and approved by the Eng Prod Representative? See Eng Prod ownership by component: http://go/cros-engprodcomponents

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), bindusuvarna@(iOS), geohsu@(ChromeOS), pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2021-03-10)

antoniosartori@ both the CLs in https://crbug.com/chromium/1115298#c20 seem to be test CLs. Could you link to the fix CL? I'm adding a merge request to 90 since I'm not sure whether the fix landed before or after branch point. Assuming the situation is similar to the other current CSP fixes (maybe even the same CL?) I will approve merge to M90 and reject merge to M89.

### am...@google.com (2021-03-10)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@google.com (2021-03-10)

Congratulations, Luan! The VRP Panel has decided to award you $3000 for this report. Thanks for your efforts and nice work! 

### am...@google.com (2021-03-11)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-11)

This bug requires manual review: M90's targeted beta branch promotion date has already passed, so this requires manual review
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on ToT?
4. Does this change need to be merged into other active release branches (M-1, M+1)?
5. Why are these changes required in this milestone after branch?
6. Is this a new feature?
7. If it is a new feature, is it behind a flag using finch?

Chrome OS Only:
8. Was the change reviewed and approved by the Eng Prod Representative? See Eng Prod ownership by component: http://go/cros-engprodcomponents

Please contact the milestone owner if you have questions.
Owners: govind@(Android), bindusuvarna@(iOS), cindyb@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### an...@chromium.org (2021-03-11)

adetaylor@ sorry, I copied the link of the wrong CL.

This has been fixed by https://chromium-review.googlesource.com/c/chromium/src/+/2667858.

Since the CL depends on other work, is not easily cherry-pickable. Moreover, since it changes completely the way we initialise CSPs, it could come with its own risks. Because of that, I would prefer not to merge this to M90.

### an...@chromium.org (2021-03-11)

[Comment Deleted]

### sr...@google.com (2021-03-12)

adetaylor@ pls chime in your thoughts on this merge, if good, to wait , reject the merge to M90

### ad...@chromium.org (2021-03-12)

Thanks for https://crbug.com/chromium/1115298#c30 - sounds fine. Rejecting merge to M90.

### [Deleted User] (2021-06-11)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### he...@gmail.com (2021-06-11)

Hey, I just noticed that https://crbug.com/chromium/1115628 and https://crbug.com/chromium/1117687 were made public (reported a few days after I filed this issue) and they seem to have the same impact as the bug reported here, but the reward amount decided by the panel was substantially bigger. Would it be possible for the panel to revisit this or maybe to get a comment on their thoughts behind this decision? Thanks!

### am...@chromium.org (2021-06-14)

Hi Luan, I am happy to bring it back for review and re-consideration by the VRP Panel. 
Just for your awareness I would like to convey that the reward amounts for bug reports take in consideration the vulnerability itself and its impact, but also quality of the report, analysis provided in the report and follow-up interactions, especially exploits, patches, and other artifacts provided. Thanks! 


### am...@chromium.org (2021-06-23)

Hi Luan, the VRP Panel has revisited the reward decision and has re-reviewed this bug report. Unfortunately, the Panel declines to alter the reward amount based on this bug report. Thank you. 

### he...@gmail.com (2021-06-24)

Hi Amy, thanks for getting it back to the panel's attention. Just one last question so I can take my mind out of this, were there any particular comments behind the decision (impact wasn't considered the same, quality of the report, or the analysis provided in the report was lacking)? This feedback would be helpful so I know where to focus/improve in the future. Thanks again!

### am...@chromium.org (2021-06-24)

Hi Luan! Reports that provide full information, up front in the initial description, with a thorough analysis and explanation of issue and impact, with a working POC and/or exploit code are highly helpful and appreciated by us on the security team. These are most helpful to getting the bug report triaged and validated more immediately. This also assists us in getting it to the appropriate developer and in helping them identify the right path forward to a fix as quickly as possible. I hope this helps.
Thanks for all your efforts. I look forward to seeing future reports from you! 

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

This issue was migrated from crbug.com/chromium/1115298?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40053054)*
