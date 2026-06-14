# Google Update on Windows: COM Session Moniker EoP

| Field | Value |
|-------|-------|
| **Issue ID** | [341803763](https://issues.chromium.org/issues/341803763) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Updater |
| **Platforms** | Windows |
| **Reporter** | sy...@gmail.com |
| **Assignee** | ga...@google.com |
| **Created** | 2024-05-21 |
| **Bounty** | $5,000.00 |

## Description

# Security Bug

---

## VULNERABILITY DETAILS

The Google Updater COM service under Windows exposes COM interfaces and does not verify the caller properly. This can be abused by a low-privileged user to execute code in another user's session which can lead to Elevation of Privilege.

This technique was described by James Forshaw:

- <https://bugs.chromium.org/p/project-zero/issues/detail?id=1021>
- <https://bugs.chromium.org/p/project-zero/issues/detail?id=1683>

By using session moniker (<https://learn.microsoft.com/en-us/windows/win32/termserv/using-a-session-moniker>), one can execute the `LaunchCmdLine` method through the `IProcessLauncher` interface (with IID `ABC01078-F197-4B0B-ADBC-CFE684B39C82`) of the `GoogleUpdate.ProcessLauncher` COM Class (with CLSID `ABC01078-F197-4B0B-ADBC-CFE684B39C82`).

## VERSION

Microsoft Windows 11:

- Chrome Version: 124.0.6367.208 (Official Build) (64-bit) stable
- GoogleUpdater Version: 126.0.6462.0, opt, 32 bits
- Operating System: Microsoft Windows 11 Pro, 10.0.22621 Build 22621

Microsoft Windows Server 2019

- Chrome Version: 124.0.6367.207 (Official Build) (64-bit) stable
- GoogleUpdater Version: 126.0.6441.0, opt, 32 bits
- Operating System: Microsoft Windows Server 2019 Datacenter, 10.0.17763 Build 17763

## REPRODUCTION CASE

I've attached a proof of concept in C#. To test it, follow the following steps

1. Create two users on the same machine.
2. Perform an interactive console login for both users to ensure account setup has completed.
3. Execute the PoC as the attacker user and ensure it prints that it's going to start a new process.
4. Switch to the victim user's desktop (without logging out the attacker).
5. The `calc.exe` process should be started started in the victim's session and should be visible on the victim's desktop. Of course this could be any process including an arbitrary executable.

## CREDIT INFORMATION

Reporter credit: Sylvain Heiniger (@sploutchy) from Compass Security (<https://www.compass-security.com>)

## Attachments

- Program.cs (text/x-csharp, 4.5 KB)

## Timeline

### sy...@gmail.com (2024-05-21)

Just noticed that the IID for the `IProcessLauncher` interface above is wrong. It should be `128C2DA6-2BC0-44C0-B3F6-4EC22E647964`. Sorry for that.

### am...@chromium.org (2024-05-21)

updating as medium severity; SI-None since Updater isn't tied to the Chrome release channels

### ap...@google.com (2024-05-21)

Project: chromium/src
Branch: main

commit f6e0492350eaeeb7d66b4f96f77f000b62fe4cba
Author: S. Ganesh <ganesh@chromium.org>
Date:   Tue May 21 22:13:42 2024

    updater: remove implementations for LaunchCmdLine/LaunchCmdLineEx
    
    Due to potential security issues, these methods are deprecated.
    
    Fixed: b/341803763
    Change-Id: I00e4ee8f5932d94dea307e8ccac1647eb79a3576
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5552983
    Code-Coverage: findit-for-me@appspot.gserviceaccount.com <findit-for-me@appspot.gserviceaccount.com>
    Reviewed-by: Sorin Jianu <sorin@chromium.org>
    Commit-Queue: Sorin Jianu <sorin@chromium.org>
    Auto-Submit: S Ganesh <ganesh@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1304083}

M       chrome/updater/app/server/win/com_classes_legacy.cc

https://chromium-review.googlesource.com/5552983


### sy...@gmail.com (2024-06-24)

Hi everyone,
May I ask if you have any update concerning this issue?
I'd like to mention it in a blog post or a presentation on COM in the future, when will it be made public?
Thanks in advance,
Sylvain

### am...@chromium.org (2024-06-24)

Hello, thanks for reaching out. Security issues (unless under embargo) are automatically disclosed 14 weeks after they are fixed. This issue was closed as Fixed on 21 May, so it will be publicly disclosed on 27 August. You're welcome to include it in a blog post or presentation at that time or after. Thanks!

### sp...@google.com (2024-06-28)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $5000.00 for this report.

Rationale for this decision:
high-quality report of moderate impact LPE 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-06-28)

Congratulations Sylvain! Thank you for your efforts and reporting this issue to us -- nice work! 

### sy...@gmail.com (2024-07-11)

Hi everyone,
Thanks for the good news!
One more question from my side, will there be a CVE assigned for this?
Cheers,
Sylvain

### am...@chromium.org (2024-07-16)

Hi -- thanks for reaching out. Since updater falls outside of the standard Chrome version / release process, we'll need to do a one-off CVE for this, but it will need to be done at the time that we can publicly disclosure this issue (since there needs to be a public artifact for each CVE).
I've added put this on a hotlist to ensure this gets a CVE closer to that time. (cc: pgrace@)

### pe...@google.com (2024-08-28)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### sy...@gmail.com (2024-09-18)

Hi everyone,
Do you have any update on the CVE?
Although, as of which version of the Google Updater is the issue fixed?
Cheers,
Sylvain

### ga...@google.com (2024-09-18)

It is fixed in `GoogleUpdater` versions `128.0.6537.0` and above.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/341803763)*
