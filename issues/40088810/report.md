# Security:  Use after free vulnerability about psdk in the latest version

| Field | Value |
|-------|-------|
| **Issue ID** | [40088810](https://issues.chromium.org/issues/40088810) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>Flash |
| **Platforms** | Windows |
| **Reporter** | ji...@gmail.com |
| **Assignee** | na...@google.com |
| **Created** | 2017-08-25 |
| **Bounty** | $5,000.00 |

## Description

VULNERABILITY DETAILS
This is a UAF vulnerability about psdk.

VERSION
pepflashplayer32_26_0_0_151 windows 7 x86
（ther operating systems may also crash,but not test）

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash:
5a6311a0 83c104          add     ecx,4
5a6311a3 8b01            mov     eax,dword ptr [ecx]
5a6311a5 ff10            call    dword ptr [eax]      ds:0023:feeefeee=????????

Crash State:
4:054> dd ecx
00d231c4  feeefeee feeefeee feeefeee feeefeee
00d231d4  feeefeee feeefeee feeefeee feeefeee
00d231e4  feeefeee feeefeee feeefeee feeefeee
00d231f4  feeefeee feeefeee feeefeee feeefeee



## Attachments

- [uaf_poc.swf](attachments/uaf_poc.swf) (application/octet-stream, 2.3 KB)

## Timeline

### ji...@gmail.com (2017-08-25)

Please tell Adobe I do not want to put this poc file in MAPP when report to Adobe.
Thank you!

### el...@chromium.org (2017-08-25)

[Empty comment from Monorail migration]

### el...@chromium.org (2017-08-25)

[Empty comment from Monorail migration]

[Monorail components: Internals>Plugins>Flash]

### ta...@google.com (2017-08-28)

natashenka@, would you be the right person to look at this?

### sh...@chromium.org (2017-08-29)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-08-29)

[Empty comment from Monorail migration]

### ji...@gmail.com (2017-08-31)

I'm sorry I forgot something shown below.

Credit is to "JieZeng of Tencent Zhanlu Lab".

Please report it as soon as possible.

### sh...@chromium.org (2017-09-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-09-08)

natashenka: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### na...@google.com (2017-09-08)

Thanks, I've reported this to Adobe

### sh...@chromium.org (2017-10-18)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-12-07)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-01-25)

[Empty comment from Monorail migration]

### na...@google.com (2018-01-25)

This is PSIRT-7239 and has been fixed

### aw...@google.com (2018-01-29)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-02-05)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-02-06)

And $5,000 for this one :-)

### aw...@chromium.org (2018-02-06)

[Empty comment from Monorail migration]

### ji...@gmail.com (2018-02-06)

OK,I will do not publicly disclose details with others.

### sh...@chromium.org (2018-02-08)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-02-08)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-02-09)

This bug requires manual review: M65 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), bhthompson@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2018-02-09)

[Bulk Edit]

+awhalley@ (Security TPM) for M65 merge review

### aw...@google.com (2018-02-09)

No merge needed

### aw...@chromium.org (2018-03-06)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-03-06)

[Comment Deleted]

### aw...@google.com (2018-03-07)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-05-04)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2018-05-04)

This issue was migrated from crbug.com/chromium/758848?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/758840]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40088810)*
