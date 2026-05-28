# Security: 

| Field | Value |
|-------|-------|
| **Issue ID** | [40055006](https://issues.chromium.org/issues/40055006) |
| **Status** | Fixed |
| **Severity** | Unknown |
| **Priority** | P4 |
| **Component** | Internals>Installer |
| **Reporter** | ve...@gmail.com |
| **Created** | 2021-02-28 |
| **Bounty** | $10,000.00 |

## Description

Platform : Windows 10 2009
Class : Elevation of Privileges
Security Boundary : Users
Severity : High
Summary:
The Google Update Service allow authenticated users to specify the log file path resulting in privilege escalation.

Description:
When google chrome is being installed as an administrator it also register Google Update Service to allow google chrome self update without elevation.
As described here https://github.com/google/omaha/blob/master/doc/ClientLog.md , the google update service can be configured to produce a log file. The configuration file is placed in C:\GoogleUpdate.ini in the past this was not a bad idea at all since C:\ default ACL doesn't allow authenticated users to create files there and even if we had the permission to do that we can't since it's protected by integrity enforcement and only processes with High integrity are allowed to create or modify files there. But recently Microsoft has done some changes to windows, _I assume_ prior to windows 10 2004 authenticated users are now allowed to create files in C:\ which expose the google update service to risk. However we can still say it's not a security boundary if the google update service sanitize things properly, unfortunately the logging configuration will allow us to specify the log file location as a parameter:

[LoggingSettings]
EnableLogging=1
LogFilePath="C:\path\tolog"  <- Path to log file

Again this won't a problem as long as the update service doesn't do anything dangerous. But normally since it's a log, log data must be written to the file. For now an attacker might be able to achieve arbitrary file overwrite bug. Unfortunately again the bug doesn't stop here in [LoggingSettings] there's a parameter that allow the maximum log file size, if the file exceeded the log file size it will renamed from "test.log" to "test.log.bak" as you can see here:

[LoggingSettings]
EnableLogging=1
LogFilePath="C:\test.log"
MaxLogFileSize=10000000 ; <- it can be set to 0

What makes the bug more dangerous, isn't the file move, a new file is created and will have rewritten ACL that allow users to have the GENERIC_WRITE access right to the file which allow an attacker to take over files.

The only problem remaining is starting the service itself, the service cannot be started on demand since the startup type is set to : manual and the service ACL doesn't allow the service to be executed, but the service expose a COM interface "GoogleUpdate.OnDemandCOMClassSvc" which can be used to start the service without elevation.

The best way to fix this bug is to use a path that's not write-able by users to load the configuration file.

Environment:
Chrome Version: 88.0.4324.190 (Official Build) (64-bit)
Google Update Service Version: 1.3.36.71
Operating System: Windows 10 2009 (20H2) x64 bit.

STEPS TO REPRODUCE
1. Install google chrome as an administrator
2. Reboot
3. Make sure that "Google Update Service (gupdatem)" isn't running otherwise the PoC will fail.
4. Now as a non-admin user run the PoC and give a file to take over.
5. The PoC will succeed and the file is now write-able.

CREDIT : Abdelhamid Naceri (halov)

## Attachments

- [poc_img.jpg](attachments/poc_img.jpg) (image/jpeg, 195.3 KB)
- [ChromeUpdaterLPE.zip](attachments/ChromeUpdaterLPE.zip) (application/octet-stream, 73.3 KB)

## Timeline

### [Deleted User] (2021-02-28)

[Empty comment from Monorail migration]

### do...@chromium.org (2021-03-02)

Attacks requiring physical access to a user's machine are not in Chrome's threat model.[1] If you have physical access to a machine, there is nothing Chrome can do to prevent theft or compromise of data or otherwise.

1. https://chromium.googlesource.com/chromium/src/+/master/docs/security/faq.md#Why-arent-physically_local-attacks-in-Chromes-threat-model

### [Deleted User] (2021-06-08)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### nd...@protonmail.com (2021-07-07)

Per https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/faq.md#what-if-a-chrome-component-breaks-an-os-security-boundary
"If Chrome or any of its components (e.g. updater) can be abused to perform a local privilege escalation, then it may be treated as a valid security vulnerability."
Last time people wanted to fixed this and paid for it so maybe it should not be set as "WontFix" even if its just marked as a normal bug.


### am...@google.com (2021-09-02)

[Empty comment from Monorail migration]

[Monorail components: Internals>Installer]

### am...@chromium.org (2021-09-02)

hi ve23halo - our sincere apologies as it appears that your report was incorrectly triaged at the time. Unfortunately, as we do see a great many bug reports, mistakes happen, and it appears one happened in this case. We would like to extend to you the same VRP reward of $10,000 as was extended to the researcher that received the VRP reward for this issue. 
Additionally, we have updated the release notes for the release with this fix (https://chromereleases.googleblog.com/2021/07/stable-channel-update-for-desktop_20.html) to ensure that this issue is also attributed to you and your original report.


### am...@chromium.org (2021-09-02)

[Empty comment from Monorail migration]

### am...@google.com (2021-09-02)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### pr...@gmail.com (2021-09-02)

[Comment Deleted]

### nd...@protonmail.com (2021-09-02)

Congratulations Abdelhamid Naceri :D

### am...@google.com (2021-09-02)

[Empty comment from Monorail migration]

### ve...@gmail.com (2021-09-13)

Oh, thank you !

### is...@google.com (2021-09-13)

This issue was migrated from crbug.com/chromium/1183137?no_tracker_redirect=1

[Monorail mergedinto: crbug.com/chromium/1204811]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40055006)*
