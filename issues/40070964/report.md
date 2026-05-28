# Security: https://bugs.chromium.org/p/chromium/issues/detail?id=1259694 can be reproduced

| Field | Value |
|-------|-------|
| **Issue ID** | [40070964](https://issues.chromium.org/issues/40070964) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Contacts |
| **Platforms** | Android |
| **Reporter** | du...@gmail.com |
| **Assignee** | fi...@chromium.org |
| **Created** | 2023-08-30 |
| **Bounty** | $1,000.00 |

## Description

**This template is ONLY for reporting security bugs. If you are reporting a**  

**Download Protection Bypass bug, please use the "Security - Download**  

**Protection" template. For all other reports, please use a different**  

**template.**

**Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com>**  

**/chromium/src/+/HEAD/docs/security/faq.md**

**Please see the following link for instructions on filing security bugs:**  

**<https://www.chromium.org/Home/chromium-security/reporting-security-bugs>**

**Reports may be eligible for reward payments under the Chrome VRP:**  

**<http://g.co/ChromeBugRewards>**

**NOTE: Security bugs are normally made public once a fix has been widely**  

**deployed.**

**-------------------------**

**VULNERABILITY DETAILS**  

The website redirection happens in the background while the Contacts dialog appears.

**VERSION**  

Chrome Version: 116 + [stable]  

Operating System: Android 13

**REPRODUCTION CASE**  

**Please include a demonstration of the security bug, such as an attached**  

**HTML or binary file that reproduces the bug when loaded in Chrome. PLEASE**  

**make the file as small as possible and remove any content not required to**  

**demonstrate the bug, or any personal or confidential information.**

**Please attach files directly, not in zip or other archive formats, and if**  

**you've created a demonstration site please also attach the files needed to**  

**reproduce the demonstration locally.**

Not granting the Contacts permission to Chrome will show a scenario that can trick users.

Open the attached file, click on.

Video of demo:

<https://drive.google.com/file/d/12SafAsmcChqi0wTY56hQCiLm-goguO29/view?usp=drivesdk>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

**Type of crash: [tab, browser, etc.]**  

**Crash State: [see link above: stack trace \*with symbols\*, registers,**  

**exception record]**  

**Client ID (if relevant): [see link above]**

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: Khiem Tran

## Attachments

- [index.html](attachments/index.html) (text/plain, 958 B)

## Timeline

### [Deleted User] (2023-08-30)

[Empty comment from Monorail migration]

### ph...@chromium.org (2023-08-31)

It does seem that I can reproduce 1259694 which is supposed to be fixed.

finnur@ could you take a look at this please?



[Monorail components: Blink>Contacts]

### [Deleted User] (2023-08-31)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-31)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### du...@gmail.com (2023-09-13)

I think you fixed it once you can fix it twice ;).

### [Deleted User] (2023-09-13)

finnur: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### du...@gmail.com (2023-09-19)

A friendly ping.

### du...@gmail.com (2023-09-19)

This bus can still be reproduced on Android 117.

### [Deleted User] (2023-09-28)

finnur: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### du...@gmail.com (2023-10-02)

Hey, this is one-month assigned, may you have a look at it?

### [Deleted User] (2023-10-11)

[Empty comment from Monorail migration]

### du...@gmail.com (2023-10-12)

A friendly ping for a faster fixing ;).

### du...@gmail.com (2023-10-23)

Hey, over 50 days, a friendly ping for this report ;).

### du...@gmail.com (2023-10-26)

Hi there, 55 days passed, and it still appears in 118.

### du...@gmail.com (2023-10-28)

A friendly pinging ;)

### du...@gmail.com (2023-11-01)

Hey, it's two months.

### du...@gmail.com (2023-11-02)

It still happens in 119, man.

### du...@gmail.com (2023-11-06)

This is a over two months bug, guys ;)

### du...@gmail.com (2023-11-08)

It's over 68 days to have a fixing...

### du...@gmail.com (2023-11-10)

Two months and nine days.

### du...@gmail.com (2023-11-16)

A friendly ping after two months and 16 days ;).

### du...@gmail.com (2023-11-17)

A friendly ping, after two months and 17 days ;).

### du...@gmail.com (2023-11-30)

Three months, almost, guys ;)

### [Deleted User] (2023-12-06)

[Empty comment from Monorail migration]

### du...@gmail.com (2023-12-10)

Hi, you will not fix it? ^^

### du...@gmail.com (2023-12-26)

Hey, fix it soon and the 120 will have it resolved in early 2024, yay ;). This kind of bug appears many times but this time it will be fixed fully after many major changes you did recently as I can saw.

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-10)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-11)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-11)

This issue was migrated from crbug.com/chromium/1477282?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

### du...@gmail.com (2024-03-15)

A friendly ping

### fi...@chromium.org (2024-10-10)

Thanks, and sorry for the late response -- this fell through the cracks.

The video accompanying the report has been removed, so I can't say for sure what the OP saw, but I tested with the html file and it looks like the presumed exploit would work something like this:

1. The attacker sets up a site (e.g. attacker.example.com/exploit.html) and gets the victim to click on that page.
2. As a result of clicking, the Contacts Picker opens.
3. Additionally (also as a result of the Contacts Picker opening) the page opens a trustworthy site in a new tab (thereby hiding the exploit site).
4. The user selects one or more contacts and closes the Contacts Picker.
5. The contacts are shared with attacker.example.com, but the trustworthy site is shown, not the exploit site.

I don't see this a viable exploit for the following reasons:

a) In step 2 the Contacts Picker opens full screen, so the user doesn't notice the navigation to a more trustworthy site. From their point of view they only see attacker.example.com (the page that launched the dialog).

... but more importantly...

b) In step 2 the Contacts Picker clearly states --in bold-- that any data will be shared with attacker.example.com, not the trustworthy site. 


### pg...@google.com (2024-10-10)

[Secondary shepherd]

Thank you for the re-assessment, Finnur@!

the original bug (now [issue 40057597](https://issues.chromium.org/issues/40057597)) also opened up the contact picker in full screen and stated in bold where the data is to be shared. And I as far as I understand, cthomp@ recommended that both the permission dialog and contacts picker be dropped if we notice that navigation has taken place. the submitted fix for the original bug to was to not launch the picker, only though. The POC has not changed from the original report.

I am unable to repro that the content picker shows up on Android 130.0.6723.40. The permission dialog still shows, but the picker does not.

However, phao@ had been able to confirm that this was reproducible back in Aug 31 2023 at the time of report. Marking this bug as fixed, as there is no contacts data that gets leaked to an attacker page thanks to dropping of the contacts picker.

cc'ing cthomp@, who is my go-to for UI security and has commented on the old bug too to double check me (:

### sp...@google.com (2024-10-22)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
baseline report of lower impact user information disclosure 


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-10-22)

Congratulations Khiem. Thank you for your efforts!

### du...@gmail.com (2024-10-22)

Thanks, Amy. Hope will try the first time getting the reward via Bugcrowd smoothly.

### pe...@google.com (2025-01-17)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### du...@gmail.com (2025-01-20)

deleted

### am...@chromium.org (2025-01-20)

It has come to our attention that your are spamming report comments, such as with your email address or other comments unrelated to the bug. We must kindly remind request you please stop this behavior as comments should be used only to make relevant technical updates to a bug or its resolution.

### du...@gmail.com (2025-01-20)

I commented to already public from your side for easier search to reread. Sorry for that.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40070964)*
