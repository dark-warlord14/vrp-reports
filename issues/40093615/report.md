# Security: World Editable GitHub Repository Wikis for chromium

| Field | Value |
|-------|-------|
| **Issue ID** | [40093615](https://issues.chromium.org/issues/40093615) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Infra>Git |
| **Reporter** | sm...@gmail.com |
| **Assignee** | dp...@chromium.org |
| **Created** | 2019-01-02 |
| **Bounty** | $500.00 |

## Description

Hi chromium team,

Not completely sure if this is in scope but I think it's worth you knowing about it.

Description

Your GitHub account contains 8 repositories with world-editable wiki pages. This means anyone with a GitHub account, even if they are not a contributor to the repository, has read and write access to the wiki page(s) of those repositories.

Vulnerable Account/Repository List

Going through all of your organization's public facing repositories, I found the following to offer excessive permissions, which most organizations usually don't intend:
chromium/ballista
chromium/blink-intent-tracker
chromium/crsym
chromium/dom-distiller-dist
chromium/eclipse-gn
chromium/ozone-client
chromium/requestautocomplete-magento-extension
chromium/web-page-replay

Impact

This issue is most likely to result in a social engineering or reputational attack. Social engineering could be conducted a number of ways: requesting users visit a malicious site, instructions to install a malicious library, etc. Reputational damage can also be done by hosting content on the wiki pages, such as images, which would not coincide with your brand's values.

Reproduction

1. Authenticate as a GitHub user. It's important to do this with an account which is not a collaborator of the repo. This will help avoid false positives.
2. Visit `https://github.com/<account>/<repository>/wiki`
3. Select the "Edit" or "New Page" button.
4. Add any content you would like and select the "Save Page" button.
5. Notice the repo's wiki has been successfully updated.

Note: During my testing of this issue I did NOT create or make any changes to your wiki pages. This issue can be confirmed without doing so.

Remediation

Unfortunately, at this time I don't believe there is an account-wide setting to make editing wikis only available to repo contributors. There is however, a setting to do this for each repo. To do this visit `https://github.com/<account>/<repository>/settings` and enable "Restrict editing to collaborators only." You can also simply disable the wiki. For more information, see: https://help.github.com/articles/changing-access-permissions-for-wikis/ and https://help.github.com/articles/disabling-wikis/.

I have seen this issue come up mainly due to two reasons:
1. Engineers and developers fork a repo which inherits the setting to allow world read/write access and they don't realize it.
2. A private repo which has the setting to allow world read/write access is open sourced and the setting is never checked during this process.

Hope this helps, please let me know if I can provide any further information.

## Timeline

### ts...@chromium.org (2019-01-02)

Thanks for the report, and for finding a way to demonstrate this without actually modifying any pages. We appreciate that.

[Monorail components: Infra>Git]

### dp...@chromium.org (2019-01-02)

Thanks! I've gone through and disabled the wikis for the listed repos.

### sh...@chromium.org (2019-01-03)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-01-03)

[Empty comment from Monorail migration]

### na...@google.com (2019-01-07)

[Empty comment from Monorail migration]

### na...@google.com (2019-01-10)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### pa...@chromium.org (2019-01-10)

Thanks for your report. The panel has decided to reward $500 :) 

Since you are a new reporter a member of our finance will be in touch. 

Additionally, how would you like to be credited in release notes?


### na...@google.com (2019-01-10)

[Empty comment from Monorail migration]

### sm...@gmail.com (2019-01-31)

Apologies for the late reply, work has been busy. Thanks to your team for taking the time to review my report and conduct remediation so quickly. In regards to credit, you can use my name "Daniel South" or my handle "SmeegeSec". Admittedly I'm not sure if any other of my information would be applicable for the release notes credit.

Thanks again, have a great rest of your week.

Regards,
Daniel

### sh...@chromium.org (2019-04-11)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2019-04-11)

This issue was migrated from crbug.com/chromium/918454?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093615)*
