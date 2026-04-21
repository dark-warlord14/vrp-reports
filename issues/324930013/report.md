# monorail: issue chart page leaks unredacted emails

| Field | Value |
|-------|-------|
| **Issue ID** | [324930013](https://issues.chromium.org/issues/324930013) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Issue Tracker, Platform>DevTools |
| **Platforms** | Windows |
| **Reporter** | ha...@gmail.com |
| **Assignee** | dt...@google.com |
| **Created** | 2024-02-13 |
| **Bounty** | $500.00 |

## Description

Hello i would like to add some more pointers I found a way to escalate it and find the emails of all reporters also, here is the detailed report

Summary:
The Monorail project, hosted on its website at https://bugs.chromium.org, serves as the issue tracking tool for various chromium-related projects. Presently, there are 33 projects listed on bugs.chromium.org, with numerous experts and developers actively contributing to these projects. Each user involved in these projects possesses personally identifiable information (PII), including their email address. Notably, there is an option on the setup page allowing users to choose whether their email should be visible or not. If a user opts for their email to be invisible, the address is obscured with three dots (...) in the display.

Exploitation Steps:

1) Visit the Url: https://bugs.chromium.org
2)Open any project, in this case breakpad
https://bugs.chromium.org/p/google-breakpad/issues/
3)Switch to "Chart" mode.
4)Enable the "Developer Tool" of the browser (press F12).
5)Navigate to the "Network" tab.
6)Select Group by "Owner" in the "Choose group by" option.
7)Identify the "IssueSnapshot" POST request.
8)Examine the response payload for unmasked email addresses of owners.

Reproducibility:
The vulnerability can be replicated across various projects on 'https://bugs.chromium.org' by following the outlined steps, revealing the email addresses of issue owners marked as invisible.

Recommendation:
Immediate attention is required to address and rectify the PII disclosure vulnerability in the Monorail project's "Chart" mode. A comprehensive review of the data masking mechanisms should be conducted to ensure user privacy is upheld.

## Attachments

- [2024-02-12 01-06-41.mp4](attachments/2024-02-12 01-06-41.mp4) (video/mp4, 7.9 MB)
- [Screenshot_20240228-013640.jpg](attachments/Screenshot_20240228-013640.jpg) (image/jpeg, 330.1 KB)
- [Screenshot_20240228-013643.jpg](attachments/Screenshot_20240228-013643.jpg) (image/jpeg, 230.1 KB)

## Timeline

### el...@chromium.org (2024-02-13)

Thanks for the report. In fact it is not necessary to read the response payload - the unmasked email addresses are present on the page itself - eg, loading <https://bugs.chromium.org/p/google-breakpad/issues/list?mode=chart&groupby=owner> simply shows a bunch of unmasked email addresses. The IssueSnapshot response does give you more info, though.

### ha...@gmail.com (2024-02-13)

Yes that leads to email I'd disclosure and pii data leakages

### ap...@google.com (2024-02-14)

Project: infra/infra
Branch: main

commit c884c6a2a0ed0090b06611555d7fa610d3afc1c5
Author: Andrew Chang <andrewjc@google.com>
Date:   Wed Feb 14 19:48:23 2024

    Remove Owners from group by.
    
    bug: b/324930013
    
    Change-Id: Ie337349f062b998c46ee8bd110b08d7700b08dcc
    Reviewed-on: https://chromium-review.googlesource.com/c/infra/infra/+/5288837
    Commit-Queue: Andrew Chang <andrewjc@google.com>
    Reviewed-by: Dave Tu <dtu@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#63132}

M       appengine/monorail/api/issues_servicer.py
M       appengine/monorail/api/test/issues_servicer_test.py
M       appengine/monorail/services/chart_svc.py
M       appengine/monorail/services/test/chart_svc_test.py
M       appengine/monorail/static_src/elements/issue-list/mr-chart/mr-chart.js

https://chromium-review.googlesource.com/5288837


### ha...@gmail.com (2024-02-17)

Hello any updates on the patching of the issue?

### dt...@google.com (2024-02-20)

Andrew's change above removed the ability to group by Owner, from both the UI and the API. It was deployed on Thu Feb 15. I verified that that fixes this issue -- marking as verified.

### ha...@gmail.com (2024-02-20)

Any updates on the rewards for the following report?

### pe...@google.com (2024-02-20)

Dear owner, thanks for fixing this bug. We've reopened it because security bugs need the Severity (S0-S3) and the Found In set, which will enable the bots to request merges to the correct branches ( as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact (security@chromium.org) to arrange to set these labels and then this bug can be marked closed again. Thank you! Severity guidelines: https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues FoundIn guidelines: https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security Thanks for your time! 

### dt...@google.com (2024-02-20)

Assigning to Security Shepherd to answer questions about rewards and labels for Monorail, which is covered by VRP but is not Chrome browser itself.

### ha...@gmail.com (2024-02-20)

Yes thankyou for quick response.

### dr...@chromium.org (2024-02-20)

FoundIn doesn't really apply here, but we only generally verify back to the current Stable version, so I'll just do that.

We call leaking limited user information an S2 if it were a Chrome bug, so let's use that same severity.

### am...@chromium.org (2024-02-20)

Hello, thank you for reaching out and for your report of this issue.
Technically, issues regarding bug reporting infra are within the scope of the Google VRP (<https://bughunters.google.com/about/rules/6625378258649088/google-and-alphabet-vulnerability-reward-program-vrp-rules>) rather than the Chrome VRP <https://g.co/chrome/vrp>). We (Chrome VRP) are happy to take a look and collaborate with Google VRP on if this issue falls within scope and qualifies for a potential reward.

Reward decisions are made after an issue is closed as Fixed. The report goes into the VRP queue for VRP Panel review and assessment at a future VRP Panel -- usually within days to 1-2 weeks after the bug is closed as fixed, depending on when that transpires. Reward decisions are updated directly on the bug report as soon as they are made. For Chromium reports that will appear as a comment and the reward amount is updated in the vrp-reward field, in the fields list on the right side of the report. ------>
For more information, please see the Chrome VRP FAQ (<https://chromium.googlesource.com/chromium/src/+/main/docs/security/vrp-faq.md>).

### am...@chromium.org (2024-02-20)

Assigning back to dtu@ as verifier to close this issue once it is determined to be resolved.

### am...@chromium.org (2024-02-20)

removing security labels related to Chrome Browser milestones and release cycle

### dt...@google.com (2024-02-20)

The issue is verified to be resolved.

### pe...@google.com (2024-02-21)

Setting milestone because of s2 severity.

### pe...@google.com (2024-02-21)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ha...@gmail.com (2024-02-22)

Hello team wanted to know if there are any updates on transferring this report to Google VRP

### am...@chromium.org (2024-02-22)

The appropriate Google VRP folks have been added onto this bug.
A reward decision will be communicated directly here once that has transpired.

### am...@chromium.org (2024-02-23)

I attempted to route this to the Abuse VRP component, but was unsuccessful. The Abuse VRP folks will need to review this issue within this component.

### ha...@gmail.com (2024-02-23)

Can we create a new report in Google VRP and then just add the link to this vulnerablity report there and then do assessment of this?

### am...@chromium.org (2024-02-23)

No, we shouldn't do that. All the technical information including the fix is on this issue, and is important in the VRP assessment process. The Abuse VRP has assured me they have seen this and we'll be updating it with a reward decision soon.

### am...@chromium.org (2024-02-24)

\*\*\* Boilerplate reminders! \*\*\*
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact [security-vrp@chromium.org](mailto:security-vrp@chromium.org) with any questions.

---

### am...@chromium.org (2024-02-24)

Congratulations! The Abuse VRP has decided to award you $500 for this report of a minor privacy leak. Since this issue is in our tracker, we have been asked by the Abuse team to convey that to you.
If you have not been rewarded by another Google VRP prior, someone from the p2p-vrp finance team will be in touch with you soon to enroll you in the Google payment system in order to process your payment.
Thank you for your efforts and reporting this issue to us!

### ha...@gmail.com (2024-02-24)

Hello team the vulnerability is completely confidential and haven't been disclosed

### ha...@gmail.com (2024-02-24)

Thankyou soo much for support and swift patching.
Can I know if my name will be visible in hall of fame of Google or not?

### ha...@gmail.com (2024-02-27)

Can I know till when will my name will be visible in hall of fame of Google ?

### pe...@google.com (2024-02-27)

The Found In field may only contain numeric values.
Some values couldn't be corrected but were removed, please verify that any important data wasn't lost.
You can see the changes by toggling full history on the issue.

### ha...@gmail.com (2024-02-27)

Hello team Can I know till when will my name will be visible in hall of fame of Google ?

### am...@chromium.org (2024-02-27)

The "hall of fame" is no longer updated, there is only the Leaderboard (<https://bughunters.google.com/leaderboard>) and the honorable mentions (<https://bughunters.google.com/leaderboard/honorable-mentions>). You need to have created a profile for the Bughunters site to appear on either list.

### ha...@gmail.com (2024-02-27)

I have an account on bughunters website but I have reported this issue through issue tracker so how will it be added to bug hunters?

### pe...@google.com (2024-02-27)

Dear owner, thanks for fixing this bug. We've reopened it because security bugs need the Severity (S0-S3) and the Found In set, which will enable the bots to request merges to the correct branches ( as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact (security@chromium.org) to arrange to set these labels and then this bug can be marked closed again. Thank you! Severity guidelines: https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues FoundIn guidelines: https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security Thanks for your time! 

### am...@chromium.org (2024-02-27)

re [comment #31](https://issues.chromium.org/issues/324930013#comment31), we have various systems that sync data from other sources to the bughunters site. For Chromium / Chrome VRP, the reporters of security issues do not have to report bugs through the bughunters site to get credit / access in bughunters.
If you check your profile > Reports > My Report, this report should be included there in My Reports list (as long as you used the same email address to report this issue as is associated with your bughunters account).

### ha...@gmail.com (2024-02-27)

Hello I can't find this report in the my reports section of the bug hunters website . I have used the same email id

### ha...@gmail.com (2024-02-28)

Hello team any solution for the issue that I can't see this vulnerablity in my reports list?

### am...@chromium.org (2024-02-28)

Sorry, we can't help with this. You'll need to reach out to [bughunters-feedback@google.com](mailto:bughunters-feedback@google.com) for assistance. I'm going to delete the screenshots in your last public so they won't be accessible when this issue is eventually publicly disclosed.

### ha...@gmail.com (2024-03-10)

Hello any update on bounty amount transfer?

### am...@chromium.org (2024-03-11)

Hello, we in the security team do not handle payments. As mentioned in c#24, someone from the p2p-vrp finance team ([p2p-vrp@google.com](mailto:p2p-vrp@google.com)) should be reaching out to you regarding payment. Information about this reward was sent to them at that time, so you should have definitely heard from them by now about enrollment / payment. Please let me know if that is not the case and please reach out to them with any questions regarding payment status.

### ha...@gmail.com (2024-04-15)

Hello can you help me out with the hall of fame and leaderboard issue.
My name is still not added to the leaderboard.

### am...@chromium.org (2024-04-16)

Hello, unfortunately we can't help here. I believe you are in contact with the correct team already who manages the bughunters site and they are working on the issue.

### ha...@gmail.com (2024-05-02)

Hello ,
Please can I get any more suppot it has already been 3 months and have not received the Bounty amount yet , also there is so much delay in updating the leaderboard and hall of fame, it would be a great help if you take a look at it as it's been a long wait from my end.
Thankyou 

### am...@chromium.org (2024-05-02)

Hello, according to the records from p2p-vrp and Google finance your payment was fully processed on 15 April 2024. I will reach out to you via email with the invoice and purchase order documentation so that you can check on your side.

### pe...@google.com (2024-06-05)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ha...@gmail.com (2024-07-11)

Appeal reward reason: It's rated P1 and S1 and still only 500 dollars?

### ko...@google.com (2024-07-11)

Hey, Google VRP here.

This was rewarded from Google VRP rules, not Chrome's. in Google VRP the rewards are not tied to the issue tracker priority or severity (BTW, the bug is S2, and `Security_Impact-None` technically, not S1). The Abuse VRP panel (at that time Abuse VRP was under Google VRP, since then we separated the rules into <https://bughunters.google.com/about/rules/google-friends/5238081279623168/abuse-vulnerability-reward-program-rules#reward-amounts-for-abuse-related-vulnerabilities>) decided $500 based on the impact of the issue, which was deemed low.

### ra...@melento.ai (2026-02-17)

deleted

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/324930013)*
