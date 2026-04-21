# Security: Amended fix for Side-channel attack against Autofill Preview

| Field | Value |
|-------|-------|
| **Issue ID** | [40054995](https://issues.chromium.org/issues/40054995) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Autofill |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | xu...@gmail.com |
| **Assignee** | ba...@chromium.org |
| **Created** | 2021-02-26 |
| **Bounty** | $5,000.00 |

## Description

https://crbug.com/chromium/1075734 fixed an autofill bug. The fix was released in M84.

In https://bugs.chromium.org/p/chromium/issues/detail?id=1075734#c26 the reporters indicated that the fix was insufficient, and a new fix was put in place, which it seems will be released in M89.

Filing a tracking bug for the new fix such that it gains a CVE, release notes credit, and possibly VRP reward.

## Timeline

### [Deleted User] (2021-02-26)

[Empty comment from Monorail migration]

### [Deleted User] (2021-02-26)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-02-26)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-02-26)

[Empty comment from Monorail migration]

### [Deleted User] (2021-02-26)

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M89. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pb...@google.com (2021-02-26)

+Adetaylor(Security TPM) for Merge decision.

### [Deleted User] (2021-02-26)

This bug requires manual review: We are only 3 days from stable.
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

### ad...@google.com (2021-02-26)

[Empty comment from Monorail migration]

### ad...@google.com (2021-03-02)

[Empty comment from Monorail migration]

### vs...@google.com (2021-03-03)

[Empty comment from Monorail migration]

### am...@google.com (2021-03-09)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-11)

[Empty comment from Monorail migration]

### am...@google.com (2021-03-17)

[Empty comment from Monorail migration]

### am...@google.com (2021-03-17)

[Empty comment from Monorail migration]

### zh...@google.com (2021-03-17)

[Empty comment from Monorail migration]

### am...@google.com (2021-03-18)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@google.com (2021-03-18)

Hello, Xu and Jason! Congratulations, the VRP Panel has decided to award you $5000 for this fix+original report! The panel revisited your original report and want to offer a higher reward for that report, plus the interaction that allowed us to know that the issue was not yet patched by the first fix and helped enable us to land a full fix. 
A member of our finance team will be in touch soon to make arrangements for payment. Thank you for this report and excellent work! 

### jp...@gmail.com (2021-03-18)

Hello! Thanks for the update and for revisiting the issue after the initial fix. Also, thank you for the additional award money, I'm sure Xu will appreciate it.

### am...@google.com (2021-03-18)

[Empty comment from Monorail migration]

### as...@google.com (2021-04-22)

[Empty comment from Monorail migration]

### [Deleted User] (2021-06-24)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1182767?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40054995)*
