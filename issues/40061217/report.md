# Arbitrary URI Origin Spoof on Chrome Android Incognito mode

| Field | Value |
|-------|-------|
| **Issue ID** | [40061217](https://issues.chromium.org/issues/40061217) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>Navigation |
| **Platforms** | Android |
| **Reporter** | pr...@gmail.com |
| **Assignee** | me...@chromium.org |
| **Created** | 2022-10-03 |
| **Bounty** | $1,000.00 |

## Description

**Steps to reproduce the problem:**  

Open <http://pwning.click/chromextel.php> on incognito tab to reproduce this- a prompt will pop up after cross origin navigation to <https://abc.xyz> asking to leave or stay: "\*This site\* is about to share information with an app outside of Incognito mode."

The difference here is that this is not tel: uri specific behavior issue like <https://crbug.com/1369350> but works for all runnable external uri on incognito mode.

**Problem Description:**  

Arbitrary URI Origin Spoof on Chrome Android Incognito mode

**Additional Comments:**

\*\*Chrome version: \*\* 107.0.5304.15 \*\*Channel: \*\* Beta

**OS:** Android

## Timeline

### pr...@gmail.com (2022-10-03)

https://pwning.click/20221003_204514.mp4

### [Deleted User] (2022-10-03)

[Empty comment from Monorail migration]

### mp...@chromium.org (2022-10-03)

Thanks for the report, also assigning to meacer@.

[Monorail components: UI>Browser>Navigation]

### [Deleted User] (2022-10-03)

[Empty comment from Monorail migration]

### pr...@gmail.com (2023-05-06)

I reported an exactly same bug here first but https://bugs.chromium.org/p/chromium/issues/detail?id=1404621 has been rewarded which need to be re-addressed. Thanks!

### cr...@chromium.org (2023-05-08)

Thanks for following up!  Adding amyressler@ and mthiesse@ to confirm if this is the same as https://crbug.com/chromium/1404621, and whether it qualifies for a reward as well.

### mt...@chromium.org (2023-05-08)

Yep, looks like it is the same issue, fixed by the fix to https://crbug.com/chromium/1404621.

### pr...@gmail.com (2023-05-08)

Btw, note that this could have been used to spoof prompt for launching popular browser based on old chromium e.g. Samsung internet like https://bugs.chromium.org/p/chromium/issues/detail?id=1249962 and that'll prompt "*This site* is about to share information with an app outside of Incognito mode." from https://www.samsung.com/us/support/owners/app/samsung-internet origin this now becomes severe issue just like https://bugs.chromium.org/p/chromium/issues/detail?id=1249962 since the prompt is convincing so users are likely just gonna allow prompt from that legitimate samsung internet site that's gonna open samsung internet with chrome n-days leading to compromising users' devices.

### pr...@gmail.com (2023-05-08)

Which I was able to reproduce by window.open() on latest so it looks like this before the fix with location property. Please consider bumping up severity and reward with this affect and I'll open a new report for the one that's not fixed

https://pwning.click/samsungprompt.mp4

### mt...@chromium.org (2023-05-08)

The window.open workaround is known and reported in https://crbug.com/chromium/1422272.

I'll defer to the security team, but I don't think this warrants a bump in the severity level due to https://crbug.com/chromium/1249962 as what we wanted to prevent there was silently switching browsers, and we're aware that if the incognito dialog is shown that the chooser dialog for other browsers will be skipped as the user knows they're leaving Chrome (and are no longer subject to Chrome's security measures).

It would probably be nice to let the user know what app they're about to launch with the incognito dialog though.

### pr...@gmail.com (2023-05-08)

I see, is general spoof issue also reported? since that also yields to chooser dialog spoof in normal mode chrome

### pr...@gmail.com (2023-05-08)

tbh, this is not a fair situation because if my report was correctly triaged and fixed instead of later report, I'd have been also reported window.open() first as well as I already had a test page to check after this original location spoof get fixed, if I knew about it.

### mt...@chromium.org (2023-05-08)

meacer@ can probably answer that - I'm not on the security team so don't have access to most security bugs.

### pr...@gmail.com (2023-05-08)

I understand this can happen sometime, I'm letting u know as a reporter/hunter who just want to play a fair game here (regardless of bug impact), which is not the case here imo.

### am...@chromium.org (2023-05-08)

Apologies that this issue and https://crbug.com/chromium/1404621 were assigned to different owners and the latter issue wasn't recognized as an existing reported when it was triaged or being resolved. This unfortunately does happen sometimes due to the size of Chrome. I'm going to go ahead and close this issue as Fixed so it can be included in VRP assessment. 
Unfortunately, regarding issue https://crbug.com/chromium/1370705#c10 and it being already known/reported as per 1422272, there is not much we can do there. That report was submitted over two months ago. It would also not be fair to that reporter to consider their report a duplicate at this time. 
In the future, if there is a test you would use to re-test the patch or mitigations that should be considered in resolution that you are aware of, it is best to submit them in the original report when at all possible to help ensure the resolution meets all the scenarios and aspects of the issues you have discovered. 

mthiesse@ I concur no severity change is needed here given the aspects noted in https://crbug.com/chromium/1370705#c10. 


### pr...@gmail.com (2023-05-09)

This issue was reported more than 7 months ago and it'd be max only a few weeks later I'd have reported on window.open() for both normal chrome and incognito mode; that's still more than 5 months ago which is way long before the second reporter (2 months ago). So what is the best way to avoid this happening in the future? do I need to tag someone else if the report owner is completely silence for weeks? I need an update on https://bugs.chromium.org/p/chromium/issues/detail?id=1369350 too. 

### am...@chromium.org (2023-05-09)

>> So what is the best way to avoid this happening in the future? 
our security triage team has slowly grown over time to include new members to the security team that are also new to the triage rotation, so we'll all work together to ensure we're all keeping an eye out for duplicates of issues of previously reported issues when triaging security bugs and ensure they are merged in the correct direction and assigned the same owner for confirmation

>> what is the best way to avoid this happening in the future? do I need to tag someone else if the report owner is completely silence for weeks?
For high and medium severity bugs, it is okay to ping owners; however, with low severity bugs there is no SLO and changes that involve web spec issues or UI changes are more complicated and slower to progress. If you need someone to look into one of your reports, please email security-vrp@chromium.org. 
Again, with low severity issues the answer may just be that this work isn't able to be prioritized yet, but we can check to ensure that the owner knows of the issue. 

 >>> I need an update on https://bugs.chromium.org/p/chromium/issues/detail?id=1369350 too.
Thanks for pointing that out. It looks like this reports is a duplicate of a previously reported issue, so thank you for allowing us to merge these reports to ensure what happened here does not happen to that reporter. 


### [Deleted User] (2023-05-09)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-09)

[Empty comment from Monorail migration]

### pr...@gmail.com (2023-05-09)

https://crbug.com/chromium/1370705#c17: Thank you for the answers and update!

### am...@google.com (2023-05-12)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-05-12)

Congratulations! The VRP Panel has decided to award you $1,000 for this report. Thank you for your efforts and reporting this issue to us.

### am...@google.com (2023-05-14)

[Empty comment from Monorail migration]

### pr...@gmail.com (2023-05-25)

Again, I checked this was fixed through https://twitter.com/BugsChromium thanks to that account for making me realise this was actually fixed lately but triaged by later report.

We need to embargo here since some mobile browsers actually allows to run app even without a prompt with same PoC- but firefox has a same impact to this report (already reported all of them).

### [Deleted User] (2023-08-15)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pr...@gmail.com (2023-10-22)

Could you please check that https://crbug.com/chromium/1370705#c9 worked without popup blocker which is different to https://crbug.com/chromium/1422272 ?

### is...@google.com (2023-10-22)

This issue was migrated from crbug.com/chromium/1370705?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061217)*
