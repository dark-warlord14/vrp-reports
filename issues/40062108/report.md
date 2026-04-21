# Security: ChromeOS pluginvm arbitrary chmod 777

| Field | Value |
|-------|-------|
| **Issue ID** | [40062108](https://issues.chromium.org/issues/40062108) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Unknown |
| **Platforms** | ChromeOS |
| **Reporter** | ro...@rorym.cnamara.com |
| **Assignee** | dt...@chromium.org |
| **Created** | 2022-12-07 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**  

When starting, vmplugin\_dispatcher will attempt to reset the permissions of the parallels\_crash\_dumps directory inside registered VMs. While vmplugin\_dispatcher is not running, if this directory is replaced with a symbolic link, when launched again the service will follow the symbolic link and reset the permissions of the parallels\_crash\_dumps directory (now a symbolic link), allowing for an arbitrary chmod 777 for paths owned by the pluginvm user.

This is a variant of the bug found in <https://crbug.com/chromium/1232658> (I can't see the specific sub-bug to link).

**VERSION**  

Google Chrome 107.0.5304.110 (Official Build) (64-bit)  

Revision 2a558545ab7e6fb8177002bf44d4fc1717cb2998-refs/branch-heads/5304@{#1202}  

Platform 15117.112.0 (Official Build) stable-channel eve  

Firmware Version Google\_Eve.9584.230.0

**REPRODUCTION CASE**  

Execute the attached shell script as follows:

sh <(cat pluginvm777.sh)

Observe that the permissions of the /run/daemon-store/pvm-dispatcher/[hash] directory change from 00750 to 2777.

DETAILS  

It is not clear the exact cause of this issue as prl\_disp\_service is not open source to my knowledge.

When the vmplugin\_dispatcher (prl\_disp\_service) service starts (via debugd), registered VMs will have their directory permissions reset. This includes the 'parallels\_crash\_dumps' directory which is set to 2777.  

Using the prlctl utility (not usable by chronos, sudo is used in the proof of concept) a valid VM can be moved from the default location into /run/chrome/wayland-0, which is bind mounted by the vmplugin\_dispatcher init script and is not validated to be a socket and not a directory. When in this (chronos controlled) directory, the VM directory contents can be replaced to create a symbolic link named 'parallels\_crash\_dumps', pointing to an arbitrary filesystem location (subject to the limitations of the vmplugin\_dispatcher mount namespace).

When the vmplugin\_dispatcher is then restarted, the service will call chmod against this path, following the symbolic link.

Requirements

- It is necessary to use the prlctl interface to exploit this vulnerability, which is not usually usable by the chronos user due to the permissions on /run/pvm disallowing access to the unix socket. The 'prlctl move' command is necessary to move a VM to a path that can be modified by the chronos user (in this case /run/chrome/wayland-0). Sudo is used in the proof of concept to emulate this access.

Impact

- Files and directories owned by pluginvm can be modified to allow all users to modify the contents

Recommendation

- Whatever was done for 1232658

## Attachments

- [pluginvm777.sh](attachments/pluginvm777.sh) (text/plain, 8.9 KB)

## Timeline

### [Deleted User] (2022-12-07)

[Empty comment from Monorail migration]

### ad...@google.com (2022-12-07)

[Empty comment from Monorail migration]

### be...@google.com (2022-12-07)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-09)

[Empty comment from Monorail migration]

### le...@google.com (2022-12-12)

Setting severity to low assuming there is no direct path to fulfil the requirements as user.
Please let me know if I am mistaken here.

[Monorail components: Security]

### [Deleted User] (2022-12-12)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-12)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aa...@google.com (2022-12-13)

This is the same root cause but different application of https://crbug.com/chromium/1232658 (sub-bug b/195347713 which isn't fixed yet AFAICT)

[Monorail blocked-on: b/195347713]

### dt...@chromium.org (2023-03-22)

b/195347713 is fixed, resolving.

### [Deleted User] (2023-03-23)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-23)

[Empty comment from Monorail migration]

### am...@google.com (2023-04-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-04-13)

Congratulations, Rory! The VRP Panel has decided to award you $5,000 for this report. Thank you for your efforts and reporting this issue to us -- great work! 

### ro...@rorym.cnamara.com (2023-04-14)

Thank you!

### am...@google.com (2023-04-14)

[Empty comment from Monorail migration]

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-30)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-06-30)

This issue was migrated from crbug.com/chromium/1398991?no_tracker_redirect=1

[Monorail blocked-on: b/195347713]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062108)*
