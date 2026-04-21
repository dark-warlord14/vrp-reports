# CSP Bypass (Old Issue)

| Field | Value |
|-------|-------|
| **Issue ID** | [40060310](https://issues.chromium.org/issues/40060310) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Mobile>iOSWeb>Security |
| **Platforms** | iOS |
| **Reporter** | ia...@gmail.com |
| **Assignee** | aj...@google.com |
| **Created** | 2022-07-16 |
| **Bounty** | $3,000.00 |

## Description

**Steps to reproduce the problem:**  

.I used the same environment used in previous report.

\*\*Test\*\*  

iPhone 12 Running iOS 15.5  

iOS Google Chrome 103.0.5060.63  

Safari is also affected as of now.

\*\*POC Video\*\* (Unlisted)  

<https://youtu.be/uChtLNQTNFY>

\*\*REPRODUCTION CASE\*\*

There are two origins involved in this PoC.  

attacker origin: <https://cgpq29r51wfnl2zd-attacker.okay.blue>  

victim origin: <https://cgpq29r51wfnl2zd-victim.netlify.app>

All paths on the victim origin have a CSP of: default-src 'none'; script-src 'unsafe-inline'

There is also a secret value located at <https://cgpq29r51wfnl2zd-victim.netlify.app/secret>. Because of CSP, the victim origin is normally not able to fetch() the secret.

Therefore, if you visit <https://cgpq29r51wfnl2zd-victim.netlify.app/blocked> an error should appear in the console.

However, if you visit the attacker page at <https://cgpq29r51wfnl2zd-attacker.okay.blue>, the secret value should appear in an alert().

**Problem Description:**  

I was going through an older issue which was fixed in 2020 and found that this vulnerability is still affecting iOS Google Chrome.

Please do let me know if I can share anything.

**Additional Comments:**

\*\*Chrome version: \*\* 103.0.5060.63 \*\*Channel: \*\* Stable

**OS:** iOS

## Attachments

- deleted (application/octet-stream, 0 B)

## Timeline

### [Deleted User] (2022-07-16)

[Empty comment from Monorail migration]

### do...@chromium.org (2022-07-17)

Can you please provide the older issue that you were looking at?

### ia...@gmail.com (2022-07-17)

This one https://bugs.chromium.org/p/chromium/issues/detail?id=1115628

### do...@chromium.org (2022-07-18)

https://crbug.com/chromium/1115628 is not applicable to iOS as the CSP implementation is in Webkit, not in Chrome itself. 

Reporter, can you confirm whether you see the same issue in iOS Safari? If so, it needs to be fixed by Apple.

+ajuma and other iOS folks.

[Monorail components: Mobile>iOSWeb>Security]

### [Deleted User] (2022-07-18)

[Empty comment from Monorail migration]

### ia...@gmail.com (2022-07-18)

Yes, it is reproducible on Safari as well.

### do...@chromium.org (2022-07-18)

#6: thanks. ajuma@ et al, can you follow up filing this to Apple / what the right next steps are?

### ia...@gmail.com (2022-07-18)

I have already reported this to Apple ;)

### aj...@chromium.org (2022-07-18)

Thanks! In that case, the next step is to wait for a fix to land in WebKit.

### [Deleted User] (2022-07-18)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-18)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-07-18)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ia...@gmail.com (2022-07-22)

I can see that report is marked as "reward-topanel" Just checking any updates on bounty :) 

### aj...@chromium.org (2022-07-22)

Bounties are awarded after bugs are fixed. To help with this process, please follow-up here when you hear back from Apple about the bug being fixed in WebKit, and then we'll mark this bug Fixed.

### ia...@gmail.com (2022-07-22)

I am working Apple Team since 2020 on Bug Bounties I can confirm they will take good amount of time to roll out the fix! Is it possible to make an exception here and award this report prior. I will maintain the confidentiality without any doubt.

Else I need to wait for good amount of time for bounty to be awarded!

### ia...@gmail.com (2022-08-21)

Hello Team,

This issue is now fixed for Google Chrome (Version 104.0.5112.101 (Official Build) (arm64)
) for Mac but Google Chrome is iOS Version is still affected. Will update here once Apple release an update for iOS as well.

### [Deleted User] (2022-09-28)

[Empty comment from Monorail migration]

### ia...@gmail.com (2022-10-25)

Hello All,

This vulnerability is now fixed on MacOS and iOS Chrome in recent release of iOS 16.1.

Please proceed with the next step.

### ia...@gmail.com (2022-10-27)

Hello All,

This vulnerability is now fixed on MacOS and iOS Chrome in recent release of iOS 16.1.

Please proceed with the next step.

### aj...@chromium.org (2022-10-27)

Sorry for missing https://crbug.com/chromium/1345045#c18! Marking as Fixed.

### ia...@gmail.com (2022-10-27)

Hope we can move this upto reward top panel.

### [Deleted User] (2022-10-27)

[Empty comment from Monorail migration]

### am...@google.com (2022-11-03)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-11-03)

Congratulations! The VRP Panel has decided to award you $3,000 for this report. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2022-11-04)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1345045?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-03-19)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060310)*
