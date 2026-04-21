# Security: Elevation of Privileges in chrome installer when removing scoped directory during updates

| Field | Value |
|-------|-------|
| **Issue ID** | [40058213](https://issues.chromium.org/issues/40058213) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Installer |
| **Platforms** | Windows |
| **Reporter** | ve...@gmail.com |
| **Assignee** | ga...@chromium.org |
| **Created** | 2021-12-12 |
| **Bounty** | $10,000.00 |

## Description

**VULNERABILITY DETAILS**

When chrome is updating, Omaha launches chrome installer with elevated privileges. The installer create a temporary directory in C:\Windows\Temp\scoped\_dirXXXX\_XXXXXXXXX and remove it.

[1] Directory creation -> <https://source.chromium.org/chromium/chromium/src/+/main:chrome/installer/setup/setup_main.cc;l=926>  

[2] CreateDirectoryW -> <https://source.chromium.org/chromium/chromium/src/+/main:base/files/file_util_win.cc;l=590>  

[3] GetTempDir -> <https://source.chromium.org/chromium/chromium/src/+/main:base/files/file_util_win.cc;l=604>  

[4] Directory deletion -> <https://source.chromium.org/chromium/chromium/src/+/main:chrome/installer/setup/setup_main.cc;l=944>  

[5] Recursive deletion -> <https://source.chromium.org/chromium/chromium/src/+/main:base/files/file_util_win.cc;l=74>

The exploitation isn't as easy as it sounds, C:\Windows\Temp ACL by default doesn't allow standard users to enumerate its content. Which makes this impossible to exploit due to the randomly generated number.  

However, there's an API that allows a standard user to monitor certain file operations in the Temp directory which is ReadDirectoryChangesW. By supplying a HANDLE to C:\Windows and specifying FILE\_NOTIFY\_CHANGE\_DIR\_NAME, an attacker can predict the directory name during the creation and place a directory junction inside it to exploit the arbitrary file deletion.

Exploiting arbitrary file deletion is pretty hard but not impossible, you can actually hijack windows defender binary during updates (files are created with secured DACL under C:\Windows\Temp) or by removing C:$WinREAgent or C:\Windows\Temp{random\_guid} to hijack dismhost binary.  

The technique that I'm using in the PoC is related to the registration of C:\Config.Msi, the PoC will register C:\Config.Msi as a secured directory. And will proceed to abuse this vulnerability to delete the folder, the installer service will assume C:\Config.Msi is safe to use because of its secured ACL. The PoC will abuse this kind of trust to hijack rollback script to gain elevated privileges.

A good fix should ensure that the scoped directory is created with a secure ACL  

-or-  

Consider not using C:\Windows\Temp in [3] at all when running as SYSTEM

**VERSION**  

Operating System: Windows 10 21H2

**REPRODUCTION CASE**  

Please follow those steps on a clean windows 10 21H2 installation to reproduce the issue.

1. Disable any active AV, they may remove the PoC because I'm reusing code from existing exploits
2. Download and install <https://drive.google.com/file/d/1CLDPWovo59EqjU2Y_BA-P0LQncV51sX9/view?usp=sharing> as an administrator (this is the offline installer for v94.0.4606.61)
3. Reboot
4. Run the PoC as a standard user
5. It should download and install the latest version through Google Omaha
6. If it succeeds, it should spawn a SYSTEM shell  
   
   And please note, in some rare cases. The PoC may fail for some reason I couldn't determine. Just kill the PoC, uninstall google chrome, and go back to step one.

**CREDIT INFORMATION**  

Abdelhamid Naceri

## Attachments

- [GoogleOmaha.zip](attachments/GoogleOmaha.zip) (application/octet-stream, 2.8 MB)

## Timeline

### [Deleted User] (2021-12-12)

[Empty comment from Monorail migration]

### do...@chromium.org (2021-12-13)

+waffles and some Windows experts, do you mind investigating this?

[Monorail components: Internals>Installer]

### [Deleted User] (2021-12-13)

[Empty comment from Monorail migration]

### wa...@chromium.org (2021-12-13)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-13)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-12-13)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### wa...@chromium.org (2021-12-14)

[Empty comment from Monorail migration]

### wa...@chromium.org (2021-12-14)

Thanks for the report & routing. Ganesh plans to take a look at this.

### ga...@chromium.org (2021-12-16)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-01-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/368a755a8d2364742b65f1ae5dbafbd99532683f

commit 368a755a8d2364742b65f1ae5dbafbd99532683f
Author: S. Ganesh <ganesh@chromium.org>
Date: Wed Jan 05 14:21:41 2022

Fix Security Elevation of Privilege in Chrome installer during update

We use the `new_setup_exe` directory as the working directory for
`ArchivePatchHelper::UncompressAndPatch`. For System installs, this
directory would be under %ProgramFiles% (a directory that only admins
can write to by default) and hence a secure location.

Bug: 1279188
Change-Id: I8f65ff67d588c46d81abc09616a08e19be2820e5
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3351102
Auto-Submit: S. Ganesh <ganesh@chromium.org>
Reviewed-by: Greg Thompson <grt@chromium.org>
Commit-Queue: Greg Thompson <grt@chromium.org>
Cr-Commit-Position: refs/heads/main@{#955697}

[modify] https://crrev.com/368a755a8d2364742b65f1ae5dbafbd99532683f/chrome/installer/setup/setup_main.cc
[modify] https://crrev.com/368a755a8d2364742b65f1ae5dbafbd99532683f/chrome/installer/util/util_constants.cc


### ga...@chromium.org (2022-01-05)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-05)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-07)

[Empty comment from Monorail migration]

### am...@google.com (2022-02-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-02-11)

Congratulations -- the VRP Panel has decided to award you $10,000 for this report! Thank you for reporting this issue to us and great work! 

### am...@google.com (2022-02-15)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-02-28)

[Empty comment from Monorail migration]

### am...@google.com (2022-03-01)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-15)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2022-07-21)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-21)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1279188?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058213)*
