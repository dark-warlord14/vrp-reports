# Security: URLBlocklist can be bypassed using chrome://download-internals

| Field | Value |
|-------|-------|
| **Issue ID** | [40065551](https://issues.chromium.org/issues/40065551) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Enterprise, UI>Browser>Downloads, UI>Browser>WebUI |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | tu...@gmail.com |
| **Assignee** | qi...@chromium.org |
| **Created** | 2023-06-09 |
| **Bounty** | $1,000.00 |

## Description

When Chrome has URLBlocklist policy in place, it is possible for an end-user/attacker to bypass it to access and download URLs that are blocked by navigating to chrome://download-internals and using the feature to access the blocked URLs.

To reproduce:

1. Set up chrome policy to block https://example.com or access to the local file system file://C: (this is usually done in kiosks) by adding a registry entry (if on Windows) Computer\HKEY_CURRENT_USER\SOFTWARE\Policies\Google\Chrome\URLBlocklist 
1=example.com

2. Open Chrome browser and confirm the policy is applied by visiting chrome://policy

3. Try to open example.com in the browser. Notice it is blocked 

4. Open chrome://download-internals

5. Enter the blocked URL in the download field and notice that it bypasses the security policy

Kindly refer to the attached screenshots. 

I used this bypass during a pentest to access the local file system in a locked down kiosk, or it can be used to download malware and bypass the organization policy.

Version tested: Chrome 114.0.5735.110 (Official Build) (64-bit)

## Attachments

- [1.JPG](attachments/1.JPG) (image/jpeg, 88.7 KB)
- [2.JPG](attachments/2.JPG) (image/jpeg, 115.4 KB)
- [3.JPG](attachments/3.JPG) (image/jpeg, 221.6 KB)
- [4.JPG](attachments/4.JPG) (image/jpeg, 51.4 KB)

## Timeline

### [Deleted User] (2023-06-09)

[Empty comment from Monorail migration]

### tu...@gmail.com (2023-06-09)

Forgot to add attachment showing how the URL is blocked.

### ar...@chromium.org (2023-06-09)

I can reproduce.

I added: /etc/opt/chrome/policies/managed/test.json 
{
	"URLBlocklist": ["https://arthursonzogni.com"]
}

and I can download "https://arthursonzogni.com" from `chrome://download-internal`.

### ar...@google.com (2023-06-09)

Thanks for this bug report!

The same issue was mentioned a year ago in:
https://bugs.chromium.org/p/chromium/issues/detail?id=1335567#c20

[Monorail components: Enterprise UI>Browser>Downloads UI>Browser>WebUI]

### ar...@google.com (2023-06-09)

[Empty comment from Monorail migration]

### dp...@chromium.org (2023-06-15)

Re-opening this as a stand-alone bug per the rationale at https://bugs.chromium.org/p/chromium/issues/detail?id=1335567#c40.

This bug could for example be addressed by the upcoming proposal of putting all debug WebUIs behind a peramnent flag. Stay tuned.

### xi...@chromium.org (2023-06-20)

Thanks for the report. +dtrainor@, the original author of chrome://download-internals. Setting the same severity as https://crbug.com/1335567. I think we should probably check the URLBlocklist policy before starting the download here[1].

[1] https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:chrome/browser/ui/webui/download_internals/download_internals_ui_message_handler.cc;l=107;drc=51e1b713f6da38219910bf8fb93a81262340bf97

### [Deleted User] (2023-06-20)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-21)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-06-23)

dtrainor: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### dt...@chromium.org (2023-06-30)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-07)

qinmin: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-07-10)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2023-07-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/bb94d0497a8a194ecb006a79e46e0293ccf3d5a9

commit bb94d0497a8a194ecb006a79e46e0293ccf3d5a9
Author: Min Qin <qinmin@chromium.org>
Date: Wed Jul 19 01:00:31 2023

Don't start URL download on internals page if it blocked by a policy

BUG=1453501

Change-Id: I8cb3d22fe996b4d6f930c1193146a6f4f6db4817
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4688344
Reviewed-by: David Trainor <dtrainor@chromium.org>
Commit-Queue: Min Qin <qinmin@chromium.org>
Reviewed-by: Min Qin <qinmin@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1172094}

[modify] https://crrev.com/bb94d0497a8a194ecb006a79e46e0293ccf3d5a9/chrome/browser/ui/BUILD.gn
[modify] https://crrev.com/bb94d0497a8a194ecb006a79e46e0293ccf3d5a9/chrome/browser/ui/webui/download_internals/download_internals_ui_message_handler.cc


### qi...@chromium.org (2023-07-19)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-19)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-19)

[Empty comment from Monorail migration]

### am...@google.com (2023-08-02)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-08-02)

Congratulations! The Chrome VRP Panel has decided to award you $1,000 for this report of a baseline exploit mitigation bypass in bypassing this security policy. A member of our finance team will be in touch with you soon to arrange payment. In the interim, please let us know the name/other identifier you would like us to use in acknowledging you for this finding. Thank you for your efforts and reporting this issue to us. 

### tu...@gmail.com (2023-08-04)

Thanks a lot, appreciated. 

You can use Tudor Enache with @tudorhacks handle. 

### am...@google.com (2023-08-05)

[Empty comment from Monorail migration]

### dp...@chromium.org (2023-08-30)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-09-09)

[Empty comment from Monorail migration]

### pg...@google.com (2023-09-12)

[Empty comment from Monorail migration]

### pg...@google.com (2023-09-12)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1453501?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Enterprise, UI>Browser>Downloads, UI>Browser>WebUI]
[Monorail mergedinto: crbug.com/chromium/1335567]
[Monorail components added to Component Tags custom field.]

### cr...@chromium.org (2024-09-19)

This bug was incorrectly marked as a duplicate of <https://crbug.com/40059921> during the Buganizer migration, due to temporarily being duplicated between comments 4 and 6 on <https://bugs.chromium.org/p/chromium/issues/detail?id=1453501&no_tracker_redirect=1>. See <http://b/325072672> for more about that problem during the migration.

I'm splitting it back out and marking it as Fixed, as it was in the older Monorail bug tracker.

### pe...@google.com (2024-09-19)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### nd...@protonmail.com (2024-09-19)

This does seem duplicate it was split because the other bug was a unorganized mess lol.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40065551)*
