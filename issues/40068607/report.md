# Security: Hide Fullscreen Notification 

| Field | Value |
|-------|-------|
| **Issue ID** | [40068607](https://issues.chromium.org/issues/40068607) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>FullScreen |
| **Platforms** | Linux, Windows, ChromeOS |
| **Reporter** | pu...@gmail.com |
| **Assignee** | ta...@chromium.org |
| **Created** | 2023-08-03 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**

Using pointerLockElement  

Attacker Can Hide Fullscreen Notification.

**VERSION**  

Chrome Version: [115.0.5790.110] + [stable]  

Operating System: [Windows 10]

**REPRODUCTION CASE**

1. Open Pufindex.html
2. Click Anywhere on Page

**CREDIT INFORMATION**  

Reporter credit: [P Umar Farooq]

## Attachments

- [puf.mp4](attachments/puf.mp4) (video/mp4, 37.1 KB)
- [PufIndex.html](attachments/PufIndex.html) (text/plain, 364 B)
- [Poc.mp4](attachments/Poc.mp4) (video/mp4, 78.0 KB)
- [PufIndex.html](attachments/PufIndex.html) (text/plain, 535 B)

## Timeline

### pu...@gmail.com (2023-08-03)

To Reproduce:

1. Open Pufindex.html
2. Click Anywhere on Page
Done.

### [Deleted User] (2023-08-03)

[Empty comment from Monorail migration]

### pu...@gmail.com (2023-08-03)

Verified Version:

[117.0.5927.0] + [canary] Windows 10 (64-bit) 

[116.0.5845.49] + [beta] Windows 10 (64-bit)

[115.0.5790.110] + [stable] Windows 10 (64-bit)


### pu...@gmail.com (2023-08-03)

Expecting To Work with Linux & macOS To. Thanks, 

### ts...@chromium.org (2023-08-03)

Repro'd on linux m115. No full screen toast shown on black screen.

[Monorail components: UI>Browser>FullScreen]

### [Deleted User] (2023-08-03)

[Empty comment from Monorail migration]

### ts...@chromium.org (2023-08-03)

[Empty comment from Monorail migration]

### pu...@gmail.com (2023-08-03)

[Empty comment from Monorail migration]

### pu...@gmail.com (2023-08-03)

One Single Click Can Hide full screen toast Notification.

Updated [POC] 

To Reproduce:

1. Open Pufindex.html
2. Click Anywhere on Page
Done.

### [Deleted User] (2023-08-04)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-08-11)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-08-15)

[Empty comment from Monorail migration]

### th...@chromium.org (2023-08-16)

[secondary shepherd] 	jinsukkim@, could you confirm you intend to take a look at this, or if not, could you help re-triage?

### ji...@chromium.org (2023-08-16)

Sorry for the late response. Android is my turf. Unassigning myself.

### th...@chromium.org (2023-08-17)

mustaq@, I see you're assigned to the similar https://crbug.com/1373910. Could you take a look at this one as well?

Please note that this is not a duplicate, because: 1) this one hides all notifications, and 2) this issue accordingly is medium severity while the other is low severity.

I can reproduce this on Linux + Windows (both VMs) but not on Mac (not VM). I am not sure if the pattern is due to the VM or the OS, but for now, removing Mac from the OS list.

### [Deleted User] (2023-08-17)

mustaq: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-08-17)

[Empty comment from Monorail migration]

### mu...@chromium.org (2023-08-25)

Both https://crbug.com/chromium/1373910 and https://crbug.com/chromium/1469777 indicates a crack in `ExclusiveAccessManager` handling of back-to-back `ExclusiveAccessBubble`s, and tweaking any specific Blink API (fullscreen, pointerlock, etc) is not a solution here.

I think the Browser UI team should own both of these issues and look into a holistic solution.  I am unassigning myself to catch the attention of better owners.

### mu...@chromium.org (2023-08-25)

[Empty comment from Monorail migration]

### pg...@google.com (2023-09-04)

jinsuk, sorry to bring you in to all the fullscreen things - could you attempt to find a more appropriate owner here?

### [Deleted User] (2023-09-05)

jinsukkim: Uh oh! This issue still open and hasn't been updated in the last 19 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-09-05)

[Empty comment from Monorail migration]

### pu...@gmail.com (2023-09-19)

Would you kindly give me an update?

### pu...@gmail.com (2023-09-26)

Any Updates Regarding this Case?

### [Deleted User] (2023-10-11)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-10-24)

[Empty comment from Monorail migration]

### pu...@gmail.com (2023-11-02)

Any Updates on this issue?


### pu...@gmail.com (2023-11-24)

Ping: Any Updates.

### [Deleted User] (2023-12-06)

[Empty comment from Monorail migration]

### pu...@gmail.com (2023-12-13)

Friendly Reminder: Any Updates. Thanks

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

### pu...@gmail.com (2024-01-12)

Any Updates on this issue?

### am...@chromium.org (2024-01-26)

Thank you for the report. The fullscreen team is working on holistic security to better the security and functional aspects of Fullscreen capabilities in Chrome. This issue is visible to the correct team, but it may take some time before these reports are closed as resolved while this work takes place. Thank you for your patience in the meantime. 
updating owner to takumif@chromium.org, which is consistent for Fullscreen issues. 


### is...@google.com (2024-01-26)

This issue was migrated from crbug.com/chromium/1469777?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

### pu...@gmail.com (2024-04-15)

Would you kindly give me an update?

What’s the current status of this Issue.

Thank you!

### pu...@gmail.com (2024-08-13)

Verified Testing! Looks like this vulnerability is fixed! in latest Chrome Version 128.0.6613.27 beta & Version 129.0.6653.0 canary

Please Verify and Change Status to fixed

Thank you!

### am...@chromium.org (2024-08-19)

msw@ -- can you please verify
It looks like this could have been resolved by your work in <https://crrev.com/c/5445712> or related work?

### ms...@chromium.org (2024-08-30)

Seems this was fixed by https://crrev.com/c/5504449 for Issue 335009803 and Issue 334994009
$ python3 C:\src\chromium\src\tools\bisect-builds.py -a win -g 1331488  -b 1217362
https://chromium.googlesource.com/chromium/src/+log/53c3ff82e0d4a416492a8cb718a2089ba7f81901..79c9ff53a6685e7b1d7f5b4cf129266b19e91c9f

### sp...@google.com (2024-09-11)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $5000.00 for this report.

Rationale for this decision:
$5,000 for report of moderate impact exploitation mitigation bypass / security UI spoofing 


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-09-11)

Congratulations Puf! Thank you for your efforts and reporting this issue to us!

### pu...@gmail.com (2024-09-16)

Thanks for the reward Really appreciate it.

### pu...@gmail.com (2024-10-15)

Any update Regarding CVE for this Vulnerability
Thank you

### pe...@google.com (2024-12-07)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### am...@chromium.org (2024-12-09)

The fix for this issue <https://crrev.com/c/5504449> was associated with [issue 335009803](https://issues.chromium.org/issues/335009803) and 334994009; therefore, security automation was not able to identify this issue as CVE or release notes relevant.
The fix was landed in M128 and shipped in the milestone release of M128.
I've added the security release tag as well as the hotlist to ensure this issue is issued a CVE in our cleanup process.

cc: pgrace@

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40068607)*
