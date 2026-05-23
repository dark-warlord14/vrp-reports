# Chrome's updater.exe is prone to privilege escalation through privileged file deletion

| Field | Value |
|-------|-------|
| **Issue ID** | [400740865](https://issues.chromium.org/issues/400740865) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Updater>Client |
| **Platforms** | Windows |
| **Reporter** | s3...@gmx.net |
| **Assignee** | ga...@chromium.org |
| **Created** | 2025-03-04 |
| **Bounty** | $5,000.00 |

## Description

# Attack Scenario

> **Please note that this exploit especially poses a risk in a corporate environment where users normally don’t have administrative privileges, and client software is distributed using centrally managed software distribution tools like MS SCCM running with elevated privileges like SYSTEM. This mostly affects Windows clients, but can also affect Windows servers, e.g. if used as a Terminalserver for multiple users.**

# Summary

Chrome's *updater.exe* is prone to a privilege escalation vulnerability to **NT AUTHORITY/SYSTEM** due to insecure usage of temporary directories and files in *C:\Windows\Temp\updater-backup*.

The tested Chrome offline installer version 135.0.7023.0 was downloaded from the official [website](https://dl.google.com/tag/s/appguid%3D%7B8A69D345-D564-463C-AFF1-A69D9E530F96%7D%26iid%3D%7B56787149-4681-A319-3886-9DC85D90D41F%7D%26lang%3Den%26browser%3D3%26usagestats%3D0%26appname%3DGoogle%2520Chrome%26needsadmin%3Dprefers%26ap%3Dx64-statsdef_1%26installdataindex%3Dempty/chrome/install/ChromeStandaloneSetup64.exe). The test was conducted on a fully patched Windows 11 x86-64 version.

When the installation or update is triggered in **SYSTEM** context, the installer runs *updater.exe* which deletes the folder *C:\Windows\Temp\updater-backup* including any containing files. This privileged deletion can be abused by a non-admin user to elevate his privileges to **NT AUTHORITY/SYSTEM**.

In a corporate environment, where software is distributed via a centrally manged software distribution solution, a local non-admin user may be able to trigger the installation by himself, or may wait for the update installation to be triggered by the software distribution process. The installation itself is then running with elevated rights, almost always in the context of **NT AUTHORITY/SYSTEM**.

# Suggested CVSS Score

[CVSS 8.8 high](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H)

- Scope changed: Due to elevation of privileges form non-admin to **SYSTEM**
- CIA: high impact on all 3 categories due to highest permissions achieved on the box, and potentially beyond.
- local attack vector with only low privileges required (non-admin)
- **No** user interaction as per CVSS definition. User is not attacked but user is the attacker, or the computer has been already compromised where also no user interaction is required

# Suggested CWEs

CWE-427: Uncontrolled Search Path Element
CWE-269: Improper Privilege Management

# Exploit Description

The exploit begins with creating and setting a so-called [opportunistic lock](https://learn.microsoft.com/en-us/windows/win32/fileio/opportunistic-locks) on *C:\Config.MSI* which is used further down for the MSI Installer trick to escalate privileges (oplock 1).

Furthermore, we create the folder *C:\Windows\Temp\updater-backup* as non-admin user which is allowed by default (Windows default permissions) and a file named *zztrick.txt* in it. The we create another oplock 2 on the file to stop *updater.exe* when the file is about to be deleted.

When *updater.exe* tries to delete *zztrick.txt*, the file is moved to another location still holding the oplock. After that we convert *C:\Windows\Temp\updater-backup* into a junction to the object manager namespace *\RPC CONTROL* which succeeds because the folder is empty at this point. Additionally, we create a pseudo-symlink named *\RPC CONTROL\zztrick.txt* pointing to *C:\Config.msi::$INDEX\_ALLOCATION*. The latter allows for the deletion of the directory *C:\Config.msi* with a **file** delete operation (Windows-specific). This setup redirects any access to *C:\Windows\Temp\updater-backup\zztrick.txt* directly to *C:\Config.msi::$INDEX\_ALLOCATION*.

Finally, the exploit releases oplock 2 which in turn allows *updater.exe* to delete *C:\Windows\Temp\updater-backup\zztrick.txt*. But since it now effectively refers to *C:\Config.msi::$INDEX\_ALLOCATION* via the above pseudo-symlink the directory *C:\Config.msi* is affected, not *C:\Windows\Temp\updater-backup\zztrick.txt*.

The deletion now hits oplock 1, which triggers the MSI installer trick. Note that we're using the advanced version of the MSI installer trick as documented as of September 3rd, 2024 which doesn't rely on the race condition anymore. The advanced version is now using an own two stage approach, still leveraging MSI installer for elevation of privileges.

For a detailed description on this specific MSI insataller trick please refer to the above ZDI link.

A highly shortened description: A prepared MSI installer is used twice to finally copy the dll named *HID.DLL* (which spawns a system shell) to *C:\Program Files\Common Files\microsoft shared\ink*. Since the MSI installer is running with elevated privileges, the file copy succeeds.

The system shell can then be spawned by opening the on screen keyboard (*osk.exe*) and hitting Ctrl-Alt-Del which loads also our dropped *HID.DLL*, and thus opens a system shell on Windows' secure desktop.

## Steps To Reproduce

P1. Compile the attached project *FilesystemEoPsNewChrome* using e.g. Visual Studio and make sure you use the correct bitness (x86 vs. x64) of the attacked system (almost always x64) as well as the release configuration (don’t use debug configuration).
I have adjusted *FolderContentsDeleteToFolderDelete.cpp* of the *FolderContentsDeleteToFolderDelete* sub-project to fit the above exploit requirements.

For your convenience I have also attached the compiled exe's.

1. Copy both exe's to a temporary folder, e.g. *C:\Temp\exploit*.
2. Open two Windows command terminals as a non-admin user.
3. In the first terminal run *FolderOrFileDeleteToSystem.exe* of FilesystemEoPs:
   `C:\Temp\exploit\FolderOrFileDeleteToSystem.exe`
   This is the one taking care of *C:\Config.MSI* as well as placing our system shell to the required location via the MSI Installer trick.
4. In the second terminal, run the patched *FolderContentsDeleteToFolderDelete.exe* of FilesystemEoPs:
   `C:\Temp\exploit\FolderContentsDeleteToFolderDelete.exe`
   This (patched) tool creates *C:\Windows\Temp\updater-backup* and the dummy file *C:\Windows\Temp\updater-backup\zztrick.txt* and sets an oplock on it, then waits for the deletion. The tool will provide details about each stage and its success.
5. Trigger the installation of the Chrome installer in **SYSTEM** context. To mimic a corporate software management solution, open an elevated command prompt with **SYSTEM** rights, e.g. by using Sysinternals `psexec -i -s cmd.exe`.
6. Shortly after you should see the success message in terminal 2 (*FolderContentsDeleteToFolderDelete.exe*).
7. In terminal 1 (*FolderOrFileDeleteToSystem.exe*) after some seconds you should see another success message.
   This tool created a *HID.DLL* file in *C:\Program Files\Common Files\microsoft shared\ink* which is responsible for getting a command terminal in **SYSTEM** context via the rollback mechanism of Windows MSI installer exploited by the tool.
8. Finally, open the on screen keyboard (Windows+R, osk.exe) and hit Ctrl-Alt-Del which will provide the **SYSTEM** shell after some seconds.
9. Cleanup: Delete *C:\Program Files\Common Files\microsoft shared\ink\HID.DLL* which can be done by a normal user without admin rights.

Please also find attached a screencast of the whole exploit including Sysinternal's procmon oputput showing the relevant parts.

## Conclusion

This issue stems from using default directory permission inheritance of *C:\Windows\Temp* and deleting a user-controlled file and directory in *C:\Windows\Temp\updater-backup* at installation time through a privileged process.

Always make sure, temporary folder permissions are restricted, especially for privileged processes.

Furthermore, you should add protection for this kind of attack by using [Process Mitigation Policy](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-setprocessmitigationpolicy) for *updater.exe*.

## Impact

The exploit allows for privilege escalation to *NT AUTHORITY/SYSTEM* which is the highest privilege on a Windows box and constitutes for a full compromise. An attacker who achieves SYSTEM privileges can install malware such as keyloggers or ransomware, or dump locally cached credentials (SAM, LSASS, etc.). The latter may allow to move laterally through the network.
As the installer may be used on both, Windows client computers as well as Windows servers, the worst impact could be the lost of the whole Active Directory domain which can be devastating for companies.

## Attachments

- [FilesystemEoPsNewChrome.7z](attachments/FilesystemEoPsNewChrome.7z) (application/x-7z-compressed, 49.4 KB)
- [FolderContentsDeleteToFolderDelete.exe](attachments/FolderContentsDeleteToFolderDelete.exe) (application/x-msdos-program, 233.5 KB)
- [FolderOrFileDeleteToSystem.exe](attachments/FolderOrFileDeleteToSystem.exe) (application/x-msdos-program, 507.0 KB)
- [PoC-Google-ChromeUpdater-EoP.mkv](attachments/PoC-Google-ChromeUpdater-EoP.mkv) (video/x-matroska, 1.8 MB)

## Timeline

### pg...@google.com (2025-03-05)

Hi, thanks for the report!

Am I correct in understanding that this exploit has the prerequisite of unrestricted write access to the device?

### s3...@gmx.net (2025-03-05)

Hi,

It's a local privilege escalation vulnerability which requires access as a low privileged user on Windows, no administrator access is required.

I hope this answers the question.

Regards,
Sandro

### pe...@google.com (2025-03-05)

Thank you for providing more feedback. Adding the requester to the CC list.

### pg...@google.com (2025-03-05)

thanks for the clarification!

unfortunately, local attacks are not part of Chrome's security threat model: <https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/faq.md#why-arent-physically_local-attacks-in-chromes-threat-model>

### s3...@gmx.net (2025-03-06)

Hi,

Thanks for the feedback, but I only partially agree.

While I agree that in case of a home/private user being almost always also working with an account which is in the administrators group and thus, can run any program with elevated permissions including SYSTEM rendering this exploit useless, I disagree in case of locked down enterprise environments.

In the latter case - as stated in my attack scenario statement - users usually don't have administrator permissions and can't install software by their own but only from a corporate's software shop like Microsof SCCM or similar, where software is managed centrally and the installation or updates are run through a service running in SYSTEM context in Windows.

Whenever the Chrome installer is executed in such an environment, any non-admin user can locally elevate his privileges to SYSTEM, although he doesn't belong to the administrators group. This also allows malicious internal users or even adversaries taken over a user's device through phishing e.g., to take over control of the Windows box, access local stored credentials from LSASS memory etc. and conduct lateral movement.

Moreover, there is a feature available to prevent such attacks, as already stated see [Process Mitigation Policy](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-setprocessmitigationpolicy).

So from my perspective, not fixing this vulnerability leaves especially corporate environments at risk of being directly compromised through Chrome.

Maybe you should consider differentiating home versus corporate environments in your local attack threat model.

Regards,
Sandro

### pg...@google.com (2025-03-06)

Thanks for the additional context - I see the distinction you are making.

For users in a corp managed ecosystem, the attack scenario that you are listing requires one of:

- physical access to an unlocked device
- control over the device by other means (e.g. phishing) providing remote code execution/filesystem access

however, given one of those preconditions, I believe the concern you point out is that the attacker can perform privilege escalation to admin status. While this is already a no-op in a non-corp environment, there is no danger of lateral movement, but in corp environments, because users may not have admin privileges, this is almost a level of protection/limitation users expect to have, but are being robbed of via this privilege escalation which in turn can potentially be utilized to compromise the rest of the corp infrastructure.

Can you provide the code of the exe binaries you've attached?

### pg...@google.com (2025-03-06)

Hi Ganesh, we're waiting on the code for the provided binaries, but assigning to you in the meantime for you to take a look in case you don't need the binaries!

Apologies - I haven't attempted to repro because I don't have a physical windows device or been able to dissect the binaries.

### s3...@gmx.net (2025-03-07)

Hi,

The source code of the exe's is already attached in *FilesystemEoPsNewChrome.7z* (as a Visual Studio project) of my initial report. Please let me know, if there are any issues with it.

Regards,
Sandro

### ap...@google.com (2025-03-07)

Project: chromium/src  

Branch: main  

Author: S. Ganesh <[ganesh@chromium.org](mailto:ganesh@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6330882>

updater: use a secure temp directory as the backup directory in setup

---


Expand for full commit details
```
updater: use a secure temp directory as the backup directory in setup 
 
Fixed: 400740865 
Change-Id: Icf2135265e40818354c595a0a90c304b87f156a6 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6330882 
Reviewed-by: Joshua Pawlicki <waffles@chromium.org> 
Commit-Queue: Joshua Pawlicki <waffles@chromium.org> 
Auto-Submit: S Ganesh <ganesh@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#1429422}

```

---

Files:

- M `chrome/updater/util/win_util.cc`
- M `chrome/updater/util/win_util.h`
- M `chrome/updater/util/win_util_unittest.cc`
- M `chrome/updater/win/setup/win_setup.cc`

---

Hash: d08d1eb70bf8f1807eb71eb7451244a510563827  

Date:  Fri Mar 07 03:22:13 2025


---

### ch...@google.com (2025-03-07)

Setting milestone because of s2 severity.

### ch...@google.com (2025-03-07)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ch...@google.com (2025-03-07)

Security Merge Request Consideration: Requesting merge to beta (M135) because latest trunk commit (1429422) appears to be after beta branch point (1427262).
Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### ga...@chromium.org (2025-03-07)

This fix is to the `updater` codebase, and no merge is needed.

### pg...@google.com (2025-03-07)

Adding hotlist to remind myself that this needs release notes off-cycle given that the fix is in updater

### ch...@google.com (2025-03-08)

**Merge approved:** your change passed merge requirements and is auto-approved for M135. Please go ahead and merge the CL to branch 7049 (refs/branch-heads/7049) manually. Please contact milestone owner if you have questions.
Merge instructions: <https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md>
Owners: alonbajayo (ChromeOS), pbommana (Desktop US), danielyip (Desktop EMEA), harrysouders (Mobile US), eakpobaro (Mobile EMEA)

### sp...@google.com (2025-03-13)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $5000.00 for this report.

Rationale for this decision:
high-quality report of moderate impact local privilege escalation 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-03-13)

Congratulations! Thank you for your efforts and reporting this issue to us -- nice work!

### s3...@gmx.net (2025-03-14)

redacted

### sp...@google.com (2025-04-10)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $5000.00 for this report.

Rationale for this decision:
[reassessment reward decision] Upon reassessment, this issue meets the criteria for high-quality && high impact local privilege escalation, with some preconditions to exploit 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-04-10)

Thank you for reaching out for a reassessment on this one, Sandro. We concur that this issue is a higher quality report and of higher impact, albeit with some preconditions to exploit and therefore warrants a higher reward. Congrats!

### am...@chromium.org (2025-04-10)

Hi Sandro, the new reassessment reward was an additional $5,000 on top of the $5,000 you were previous rewarded, bringing your total reward for this issue to $10,000.

I've manually updated the `vrp-reward` field to reflect $10,000, but please ignore it if the bots change it back. The automation is responsible for getting the reward information to the payments automation, which would have already been achieved. But the bots may set it back to $5,000 to reflect this more recent additional reward.

### s3...@gmx.net (2025-04-11)

Hi,

Thank you so much!

Regards,
Sandro

### s3...@gmx.net (2025-05-05)

Hi,

Just a quick additional question:

Will there be a CVE assigned for this issue?

Thanks,
Sandro

### pg...@google.com (2025-05-05)

Hi Sandro,
yes, but as this part of the code does not ship with the Chrome release cycle, a CVE will be assigned and submitted once this bug goes public. thanks!

### s3...@gmx.net (2025-05-05)

Hi,

Thank you for the prompt response and confirmation!

Best regards,
Sandro

### ch...@google.com (2025-06-14)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> high-quality report of moderate impact local privilege escalation

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/400740865)*
