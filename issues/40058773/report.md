# Security: Chrome Enterprise MSI installer Elevation of Privileges Vulnerability

| Field | Value |
|-------|-------|
| **Issue ID** | [40058773](https://issues.chromium.org/issues/40058773) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Installer |
| **Platforms** | Windows |
| **Reporter** | ve...@gmail.com |
| **Assignee** | ga...@chromium.org |
| **Created** | 2022-02-14 |
| **Bounty** | $20,000.00 |

## Description

**VULNERABILITY DETAILS**  

I have been deploying chrome in some windows server installations, and I apparently deploying it through MSI packages is faster & easier.  

While doing that, I noticed a thing, the MSI packages are repairable for standard users.  

In other words, standard users can tell windows installer service to launch a repair operation using the commandline "msiexec /fa C:\Windows\Installer<msi\_package>" or using  

<https://docs.microsoft.com/en-us/windows/win32/api/msi/nf-msi-msireinstallproductw>

When a user launch the chrome MSI reparation, Windows Installer Service (which runs as SYSTEM) will write "Google Update Setup" in C:\Windows\Installer<random\_hex>.tmp and execute it.  

I took a quick look at Google Update Setup. This component will write another executable "GoogleUpdate.exe" into a secure directory "C:\Program Files (x86)\Google\Temp" making it a secure operation.  

But there's a catch, before writing the executable, update setup will check if "C:\Program Files (x86)\Google\Temp" is accessible by calling GetTempFileName. After that the newly created file is removed and replaced by a directory which should contain the "GoogleUpdate.exe"  

The issue is, if the directory is not accessible. Update setup will expand %TEMP% environment variable and use it as a working directory.  

Before we talk about the exploitability, an attacker with standard user privileges will face an issue. Making "C:\Program Files (x86)\Google\Temp" inaccessible for a process that runs as SYSTEM means we should be able to delete it or having enough access to rewrite the DACL.  

In a default configuration, a user may not have such access.  

However, I decided the make things a little bit different. Instead of making "C:\Program Files (x86)\Google\Temp" inaccessible, perhaps we could lock anything created inside it ?  

And apparently, it worked. After the GetTempFileName call, I locked the file with FILE\_SHARE\_READ to make sure that the file removal and the directory creation will fail. This caused the update setup to use %TEMP% instead.

What makes things worst, is how the installer launch the executable initially. The installer make sure that certain process properties match the user ones, the installer launches google update setup with a modified SYSTEM token with a session id that match the user one. The most interesting part is the environment variable, the installer launches update setup with the same environment variable as the user. Which means %TEMP% will resolve to C:\Users<user\_name>\AppData\Local\Temp instead of the default "C:\Windows\Temp" which makes the exploitability significantly easier for the user.  

An attacker can simply hijack "GoogleUpdate.exe" after it is written, then just wait for update setup to launch it as SYSTEM.

**VERSION**  

Chrome Version: 98.0.4758.82 (Stable x64)  

Operating System: Windows 10 21H1, Windows Server 2019

**REPRODUCTION CASE**  

There is a C++ proof of concept attached as a PoC, please use the following steps as guidance to reproduce this issue.

1. Make sure to install chrome MSI package as administrator, use this link to download it <https://chromeenterprise.google/browser/download/#windows-tab> (Please select MSI package)
2. Run the PoC as a standard user
3. If it succeeds, a SYSTEM shell should be spawned

Reporter credit: Abdelhamid Naceri

## Attachments

- [ChromeMsiLPE.zip](attachments/ChromeMsiLPE.zip) (application/octet-stream, 96.2 KB)

## Timeline

### ve...@gmail.com (2022-02-14)

Adding attachments.

### [Deleted User] (2022-02-14)

[Empty comment from Monorail migration]

### ve...@gmail.com (2022-02-14)

*Windows 10 21H2 not 21H1, sorry for the mistake.

### ad...@google.com (2022-02-14)

Thanks for the report!

I haven't tried to reproduce this but the explanation seems really clear.

waffles@, ganesh@, could you take a look? Tagging as medium severity per the precedent of https://crbug.com/chromium/1279188.

[Monorail components: Internals>Installer]

### [Deleted User] (2022-02-14)

[Empty comment from Monorail migration]

### ga...@chromium.org (2022-02-14)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-15)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ga...@chromium.org (2022-02-15)

This fix will go out with the next release of Google Update, likely by the end of March:

Fix Security Chrome Enterprise MSI installer Elevation of Privileges Vulnerability

This CL removes the fallback to %TEMP% if we are running as Admin and then unable to create a temp directory under %PROGRAMFILES%.

Affected files

//depot/googleclient/omaha/mi_exe_stub/mi.cc


### [Deleted User] (2022-02-16)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-16)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-16)

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M99. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-02-16)

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: benmason (Android), harrysouders (iOS), ceb (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-02-17)

no fix to merge here; part of Updater release cycle 

### am...@google.com (2022-03-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-03-17)

Congratulations, Abdelhamid! The VRP Panel has decided to award you $20,000 for this report. Thank you for your highly detailed report, complete with the functional exploit! We appreciate your efforts and reporting this issue to us! 

### am...@google.com (2022-03-17)

[Empty comment from Monorail migration]

### ve...@gmail.com (2022-03-18)

Amazing !

### [Deleted User] (2022-05-25)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1297269?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058773)*
