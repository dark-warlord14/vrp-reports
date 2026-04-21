# Security: Google Update for Windows allows arbitrary file creation when logs are enabled

| Field | Value |
|-------|-------|
| **Issue ID** | [40091989](https://issues.chromium.org/issues/40091989) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Internals>Installer |
| **Platforms** | Windows |
| **Reporter** | cl...@gmail.com |
| **Assignee** | ga...@chromium.org |
| **Created** | 2018-07-22 |
| **Bounty** | $5,000.00 |

## Description

SUMMARY

The permissive access rights on the log folder & files set by GoogleUpdate on Windows (when logs are enabled) can be abused to create arbitrary files with write access. This can be used by an unprivileged user to obtain SYSTEM privileges.

**VULNERABILITY DETAILS**

When configured to produce logs, Google Update will create a log file in C:\ProgramData\Google\Update\Log.  

The "Users" group can create files/folders in this directory, as well as modify its attributes. The log file is created with SYSTEM privileges (without impersonation), and is also made writable to the Users group (see FileLogWriter::CreateLoggingFile() in Omaha), presumably so that user processes can also create/write to log files.

This can be abused by an unprivileged user to create files as SYSTEM.  

Indeed, because Users can write attributes to the Log directory, an unprivileged user can change it to an NTFS junction that points to an arbitrary directory like C:\Windows\System32 before restarting the update process (e.g. by logging out and logging back in to trigger the update task).  

When a log is generated, a privileged GoogleUpdate.exe process will create a log file in C:\Windows\System32 and set its access rights, offering write access to the Users group.

With a writable file in System32, a user can get code execution as SYSTEM, by leveraging a technique found by James Forshaw and described here:  

<https://googleprojectzero.blogspot.com/2018/04/windows-exploitation-tricks-exploiting.html>  

(Basically, the privileged DiagHub service can be made to load, from C:\Windows\System32, a file with any extension as a DLL.)

Alternatively, using another one of James' tricks, the Log directory can be made a junction to the \RPC Control\ object directory, where users can create a symbolic link with the name of the log file, pointing to an arbitrary path, thus also choosing the file name. It can be used to create a DLL that will be loaded from C:\Program Files (x86)\Google\Update by the GoogleUpdate process – there are a few that show up in Procmon.

One hurdle to overcome for exploitation is the fact that the current log file is locked by existing update (or crash/reporting) processes in many cases, preventing its move/removal and the creation of the mount point (directory must be empty).  

However, the update service has a start type of "automatic (delayed start)", so there is a small window between system boot and the start of the first update service. One way to exploit this is using a scheduled task that runs at user logon, deletes or moves the existing log files, and changes the Log directory into a mount point to the desired location.

The attack scenario is a managed computer (e.g. entreprise laptop) with Google Chrome installed with admin privileges and Google Update log files enabled.  

Because the C:\GoogleUpdate.ini file cannot be created by unprivileged users, this vulnerability only occurs in non-default configurations, when Google Update log files are enabled as part of the deployment, or later by an administrator / GPO / etc.  

The update troubleshooting instructions at <https://support.google.com/chrome/a/answer/6350036> give an example configuration that can be used to set up logging, I used this configuration in my tests.

**VERSION**

Chrome Version: 67.0.3396.99 stable (note: sable/beta/dev versions use the same version of Google Update)  

Google Update version: 1.3.33.17  

Operating System: Windows 10 1803 (10.0.17134.112) x64

**REPRODUCTION CASE**

To put the test machine in a vulnerable configuration, create the file C:\GoogleUpdate.ini with content from <https://support.google.com/chrome/a/answer/6350036> (also attached for convenience).

The provided PoC is a set of utilities from James Forshaw and 2 batch scripts to automate the attack. It implements the first exploitation method described above (creation of the log file in System32 and load as DLL in the DiagHub service) in a logon scheduled task (the first script just sets up the files in C:\Temp, registers the task and reboots).

Usage instructions:

1. Run runme.bat as an unprivileged user, to setup the task and reboot the machine
2. Logon as soon as the machine has rebooted
3. When prompted, open Chrome's settings page to trigger an update check
4. Once the check if finished, go back to the command prompt and continue

You should get a cmd shell as SYSTEM.

Sources:  

CreateMountPoint.exe and DeleteMountPoint.exe are part of <https://github.com/google/symboliclink-testing-tools>  

FakeDllLoader.exe and FakeDll.dll are based on the exploit created by James for P0 bug #1428 and described in his article. The original code is at the end of the report (the full PoC in poc\_sd\_full.zip): <https://bugs.chromium.org/p/project-zero/issues/detail?id=1428#c9>  

FakeDllLoader.cpp is PocStorSvc.cpp without the parts specific to bug #1428, and with the name of the file to load from System32 passed as parameter to the exe.

CONSIDERATIONS FOR FIX

There are several ways this vulnerability could be fixed, a simple one may be using separate logs for user and SYSTEM processes with access restrictions on the SYSTEM logs / log directory to prevent modification, removing the code that adds an ACE to allow Users write access to logs, and adding checks to make sure SYSTEM processes do not write in user logs. User logs could then be created in each user's own directory (AppData) to prevent the same kind of attacks between users.

Another solution could be to remove all write access from Users, write all logs as SYSTEM and have a kind of broker for user logs (this would increase the attack surface a little bit, but there's already a broker to trigger updates from user processes). The log files could then be create in a location that is only writable by SYSTEM.

Also, the default permissive ACLs of C:\ProgramData\Google[\Update] could be hardened — as defence in depth if not part of the fix — to remove write access for users by default if it's not needed.

## Attachments

- [poc.zip](attachments/poc.zip) (application/octet-stream, 267.8 KB)
- [GoogleUpdate.ini](attachments/GoogleUpdate.ini) (application/octet-stream, 214 B)
- [FakeDllLoader.cpp](attachments/FakeDllLoader.cpp) (text/plain, 4.1 KB)

## Timeline

### wf...@chromium.org (2018-07-23)

Seems like a possible privilege escalation using Google Update, but the preconditions seem rare, in particular:

>Because the C:\GoogleUpdate.ini file cannot be created by unprivileged users, this vulnerability only occurs in non-default configurations, when Google Update log files are enabled as part of the deployment, or later by an administrator / GPO / etc.

I wonder how often this configuration happens?

Sorin, can you take a look at this, or find someone to address it?

[Monorail components: Internals>Installer]

### ct...@chromium.org (2018-07-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-08-06)

sorin: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ga...@chromium.org (2018-08-06)

This configuration only happens if someone deliberately creates/copies a googleupdate.ini file to C:\. googleupdate.ini is not added by administrator/GPO/etc, so this is only in very rare cases when the Omaha team asks a user for debug logs.

Cool exploit though. We will consider some of the mitigations as a defense in depth.

### ga...@chromium.org (2018-08-06)

[Empty comment from Monorail migration]

### cl...@gmail.com (2018-08-06)

Thanks!

There is indeed no deployment configuration that would create this file by default.
The scenario I had in mind was a sysadmin trying to collect update logs (either for troubleshooting or to keep an eye on Chrome updates) that would create this file on user workstations following the instructions in the update FAQ. But that must be a very rare case indeed.

### wf...@chromium.org (2018-08-06)

given mitigations and low chance of this happening in the wild, I'm bumping to Low.

### gr...@chromium.org (2018-08-07)

I had considered doing something special in Chrome's enterprise installer to put the .ini file in place before an install and remove it afterward so that we could help admins collect logs in a more automated fashion. I'll keep this issue in mind before doing so.

### sh...@chromium.org (2018-08-07)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-09-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-10-17)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-12-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-01-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-03-13)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-04-24)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-06-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-07-31)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-09-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-10-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-12-11)

[Empty comment from Monorail migration]

### cl...@gmail.com (2019-12-19)

Hi,

FWIW this bug also impacts 3rd-party software that uses Google Update (and may have log enabled by default), such as Dropbox.

It was also reported to them last year - before I realised its updater is based on Chrome's updater and opened this issue - but was not patched (or not completely) at the time.
It has been independently discovered 3 month ago by someone else, and is now public :
https://decoder.cloud/2019/12/18/from-dropboxupdater-to-nt-authoritysystem/

### sh...@chromium.org (2020-02-05)

[Empty comment from Monorail migration]

### [Deleted User] (2020-04-09)

[Empty comment from Monorail migration]

### [Deleted User] (2020-05-20)

[Empty comment from Monorail migration]

### [Deleted User] (2020-07-16)

[Empty comment from Monorail migration]

### [Deleted User] (2020-08-26)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-07)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-30)

[Empty comment from Monorail migration]

### [Deleted User] (2020-11-18)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-20)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-03)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-11)

[Empty comment from Monorail migration]

### zh...@google.com (2021-03-17)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-15)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-26)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-07)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-11)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-22)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-15)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-02)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-30)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-25)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-03)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-28)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-30)

[Empty comment from Monorail migration]

### ga...@chromium.org (2022-12-08)

Google Update does not create a log file by default any more. Only if `IsEnabledLogToFile` is set to 1 under:
32-bit—HKLM\Software\Google\UpdateDev\
64-bit—HKLM\Software\WOW6432Node\Google\UpdateDev\

### [Deleted User] (2022-12-08)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-09)

[Empty comment from Monorail migration]

### am...@google.com (2022-12-15)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-12-16)

Congratulations! The VRP Panel has decided to award you $5,000 for this report. A member of our finance team will be in touch with you soon to arrange payment. Thank you for your patience while this issue was resolved and closed and additional thank you for your efforts in reporting this issue to us! 

### am...@google.com (2022-12-16)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-16)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-05)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/866311?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091989)*
