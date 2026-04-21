# Using Flash's ProgressEvent to extract the length of cross-site responses

| Field | Value |
|-------|-------|
| **Issue ID** | [40094386](https://issues.chromium.org/issues/40094386) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Plugins>Flash |
| **Platforms** | Windows |
| **CVE IDs** | CVE-2019-8075 |
| **Reporter** | ne...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2019-03-26 |
| **Bounty** | $1,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36

Steps to reproduce the problem:
This report is sent following request in https://crbug.com/chromium/124429941 (https://issuetracker.google.com/124429941).

Using Flash's ProgressEvent it is possible to extract the exact size of cross-site responses. The exploit works in all popular browsers if Flash is enabled for the attacking web page.

Example (enable Flash in the page):
https://u.cs.biu.ac.il/~gelernn/flash-size-exploit/

Extraction of the length to learn about Youtube watch history (due to some changes in Youtube, this demo is not as accurate as it used to be):
https://u.cs.biu.ac.il/~gelernn/fyuiweuhaeuhq/

Notice that this is a Flash feature that can be abused also in other browsers (while Flash is enabled).

What is the expected behavior?
The length of cross-site responses should not be available (security reasons. SOP).

What went wrong?
The length of cross-site responses can be extracted when Flash is enabled.

Did this work before? N/A 

Chrome version: 73.0.3683.86  Channel: stable
OS Version: 10.0
Flash Version: 

The Flash bug exists ~years at least. I know that Flash got report about it, and I tried to re-report about it using Google security team, as I assumed that request from Google will be taken more seriously (had a correspondence with Google security team about this bug).

## Timeline

### dr...@chromium.org (2019-03-26)

This reproduces this on M73. Triaging to Flash team.

I recognize that Flash is off-by-default in M76, but this is a fairly severe vulnerability, in that it can extract personal information about the user (e.g. Youtube watch history, as noted above). Are there any possible mitigations for ProgressEvent for M74 or M75?

[Monorail components: Internals>Plugins>Flash]

### ne...@gmail.com (2019-03-26)

Just saying that Youtube is a simple example. When search interfaces are more sophisticated (e.g., advanced search) and unprotected against CSRF, it is possible to extract much more sensitive info (in previous XS-Search reports to different companies, I demonstrated extraction of 16-digit credit card number in 10 seconds, or other secret codes).

### sh...@chromium.org (2019-03-27)

[Empty comment from Monorail migration]

### la...@google.com (2019-03-27)

This isn't something that the Chrome team can address.  It would need to be reported to and addressed upstream by Adobe.

### [Deleted User] (2019-03-27)

Please report this to the Adobe Product Security Incident Response Team <psirt at adobe dot com>.  They will happily follow up and drive this to resolution. 

It would be great if you could include source for your POC and a brief explanation of how ProgressEvent is providing a unique capability.  I took a quick look yesterday and it's not immediately clear to me, but I haven't had a lot of time to sit down and reverse-engineer it.

### ev...@google.com (2019-03-27)

Hi

This was reported to Adobe a few years ago. FYI

### ts...@chromium.org (2019-05-21)

Anthony, do you know who should be coordinating with adobe to drive them to a resolution? Please re-assign as appropriate.

### la...@google.com (2019-05-24)

psirt@ would likely be the right alias to raise this with, it's staffed by a number of folks at Adobe, so should get a pretty quick response.

Failing that, Jeromie (jeclark@) would likely be the best POC from Adobe to directly coordinate w/.  



### [Deleted User] (2019-05-28)

Yeah, just wanted to reiterate Anthony's comment that the Adobe Product Security Incident Response Team <psirt at adobe dot com> is your best resource for reporting and tracking security issues for any Adobe product.  That address is staffed 24/7/365, and they provide robust tracking and communication services across all of Adobe's products.

For the issue at hand, we've landed a fix, which will go out in our next monthly release.

If you'd like to take a look, the changes are CLs: 97503, 97504 and 97522 in Main, and 91856 in Evans


### sh...@chromium.org (2019-06-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-07-31)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-09-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-10-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-12-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2020-02-05)

[Empty comment from Monorail migration]

### [Deleted User] (2020-04-09)

[Empty comment from Monorail migration]

### [Deleted User] (2020-05-20)

[Empty comment from Monorail migration]

### [Deleted User] (2020-07-16)

[Empty comment from Monorail migration]

### [Deleted User] (2020-08-26)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-07)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-16)

@laforge - Per https://crbug.com/chromium/945997#c9, I believe the fix for this shipped back in June 2019.  Does this just need to be closed?

### la...@google.com (2020-10-16)

+1.  Marking this issue as Fixed.  Thanks for flagging.

### [Deleted User] (2020-10-17)

[Empty comment from Monorail migration]

### ad...@google.com (2020-10-18)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-19)

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M87. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-10-19)

This bug requires manual review: M87's targeted beta branch promotion date has already passed, so this requires manual review
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
Owners: benmason@(Android), bindusuvarna @(iOS), cindyb@(ChromeOS), lakpamarthy@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### la...@google.com (2020-10-19)

[Empty comment from Monorail migration]

### ad...@google.com (2020-10-23)

Adobe tell me that this is CVE-2019-8075 and was fixed in Flash 32.0.0.202.

### ad...@google.com (2020-10-23)

Adobe have also confirmed that they fixed the bug on the basis of _this_ report rather than any earlier reports, so I'll take this back to the VRP panel for discussion.

### ad...@google.com (2020-10-28)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-10-28)

Congratulations! The VRP panel has decided to award $1000 for this bug. Someone from our finance team will be in touch. As this was fixed in Flash a while ago, it doesn't really fit into our normal release notes process, but I will list this in the M87 release notes just so you get credited somewhere :) Hope that's OK. How would you like to be credited?

### ne...@gmail.com (2020-10-28)

Thanks.
Nethanel Gelernter, Cyberpion (https://www.cyberpion.com).

### ad...@google.com (2020-10-29)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-24)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### as...@google.com (2021-01-27)

Marking as not applicable as there is no flash in LTS.

### la...@chromium.org (2021-02-25)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

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

This issue was migrated from crbug.com/chromium/945997?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094386)*
