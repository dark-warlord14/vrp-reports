#  Inadequate Registry management within the Chrome uninstaller resulting in privilege escalation

| Field | Value |
|-------|-------|
| **Issue ID** | [40069458](https://issues.chromium.org/issues/40069458) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Internals>Installer |
| **Platforms** | Windows |
| **Reporter** | b....@gmail.com |
| **Assignee** | ga...@chromium.org |
| **Created** | 2023-08-13 |
| **Bounty** | $3,000.00 |

## Description

---

### Report description


 Inadequate Registry management within the Chrome uninstaller resulting in privilege escalation


---

### Bug location


#### Which product or website have you found a vulnerability in?

Google Chrome


---

### The problem


#### Please describe the technical details of the vulnerability

Due to insecure deleting of registry keys in unprotected Windows registry locations by chrome uninstaller, it is possible for unprivileged attacker to take control of protected registry keys like `HKEY_CURRENT_USER\Software\Policies`. In this particular case, this can lead to setting local group policies for the currently logged in user that would have been otherwise inaccessible to standard users. subsequently unprivileged users running as a standard user, can then set a Windows policy like "AlwaysInstallElevated", and in case this policy was already set per-machine, the unprivileged attacker can then set it per-user, and subsequently run their code as an MSI installer to gain SYSTEM privileges on the system from a standard user.

Chrome uninstaller runs as elevated process and attempts to delete its own GUID (`{8A69D345-D564-463c-AFF1-A69D9E530F96}`) from the registry tree `HKCU\\Software\\(Wow6432Node\\)?Microsoft\\Active Setup\\Installed Components` if it is present there. This registry location is unprotected, meaning a standard user can write to. So a standard user/attacker can add Chrome's GUID `{8A69D345-D564-463c-AFF1-A69D9E530F96}` as a registry symlink and point it to any protected registry key within the HKCU registry hive (Windows doesn't allow creating symlink between registry hives for obvious security reasons). Now due to unexpected behavior of how Windows deletes registry symlinks, calling any documented Windows API that deletes a registry key, if that key happens to be a registry symlink key then the target will be deleted and not the link, which consequently will lead Chrome Uninstaller to delete the protected registry key (for example `HKEY_CURRENT_USER\Software\Policies`), once the protected registry key is deleted, the attacker can recreate the protected registry key but this time with WRITE permission for itself.

This impacts both consumer and enterprise/education builds of Chrome.


#### Please briefly explain who can exploit the vulnerability, and what they gain when doing so

Unprivileged attacker running as a standard user can gain access to any protected registry key within the HKCU registry hive on Windows. This can lead for example to gain control over `HKEY_CURRENT_USER\Software\Policies`, which then allows setting local group policies for the currently logged in user that would have been otherwise inaccessible to standard users. To leverage this even more the attacker can set the policy `AlwaysInstallElevated` per-user, and if it was already set per-machine, then they will be able to elevate their standard user to a SYSTEM by running their code as an MSI installer.

`AlwaysInstallElevated` is just one interesting policy out of thousands other policies from Microsoft, and many other vendors including Google that unprivileged attacker can take advantage of to gain additional permissions, access, and capabilities on the system. The following website provide a good overview of other policies an unprivileged attacker can take advantage of: `https://admx.help/`

Also, there could be other protected registry keys within HKCU registry hive other than `HKEY_CURRENT_USER\Software\Policies`, that the attacker can gain control of on successful exploitation.

PoC:
0. On a Windows machine with a standard account where you have Chrome installed already
1. As a standard user (not admin) check the permission on the registry key `HKEY_CURRENT_USER\Software\Policies`, you should see that you have read-only permssions. You can do that using the tool AccessChk for example:
```
C:\>AccessChk -nobanner -d -k HKEY_CURRENT_USER\Software\Policies
HKCU\Software\Policies
  RW NT AUTHORITY\SYSTEM
  RW BUILTIN\Administrators
  R  NT AUTHORITY\RESTRICTED
  R  WINDEV2209EVAL\Limited     <--- READ-ONLY
  R  APPLICATION PACKAGE AUTHORITY\ALL APPLICATION PACKAGES
  R  S-1-15-3-1024-1065365936-1281604716-3511738428-1654721687-432734479-3232135806-4053264122-3456934681
```
2. Confirm that we cannot set local group policies from a standard account by default
```
C:\>reg add HKCU\Software\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated /t REG_DWORD /d 1
ERROR: Access is denied.        <--- AS EXPECTED
```
3. Create a symlink as described in the description above that points to `HKCU\Software\Policies`, you can use the tool CreateRegSymlink.exe (download from link [3])
```
C:\tools>CreateRegSymlink.exe "HKCU\Software\Microsoft\Active Setup\Installed Components\{8A69D345-D564-463c-AFF1-A69D9E530F96}" HKCU\Software\Policies
Creating registry link from \Registry\User\S-1-5-21-1288456869-3879226829-2752375403-1001\Software\Microsoft\Active Setup\Installed Components\{8A69D345-D564-463c-AFF1-A69D9E530F96} to \Registry\User\S-1-5-21-1288456869-3879226829-2752375403-1001\Software\Policies
SUCCESS
```
4. Uninstall Chrome, chrome uninstaller will delete `HKCU\Software\Policies`
5. Recreate the registry key `HKCU\Software\Policies` as a *standard* user: `reg add HKCU\Software\Policies`. You actually don't need to do that, because the first process that tries to access this registry key as a standard user, will end up creating that for you. svchost.exe access that key very often so it will recreate it for you, and since svchost.exe impersonate the currently logged in user when it access that policies key, it will end up creating it with WRITE permission, as it uses the API RegCreateKey[Ex] to open the key, which also creates the key if it's not present.
6. Run AccessChk again on `HKCU\Software\Policies`
```
C:\>AccessChk -nobanner -d -k HKEY_CURRENT_USER\Software\Policies
HKCU\Software\Policies
  RW WINDEV2209EVAL\Limited     <--- WE HAVE WRITE PERMISSION NOW
  RW NT AUTHORITY\SYSTEM
  RW BUILTIN\Administrators
  R  NT AUTHORITY\RESTRICTED
```
7. As a "standard" user run the command below to set the policy `AlwaysInstallElevated` per user.
```
C:\>reg add HKCU\Software\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated /t REG_DWORD /d 1
The operation completed successfully.
```
8. Run your an MSI that lauches a cmd.exe, the newly spwaned cmd.exe will have a SYSTEM privileges. (I can provide on request, or you can create that using Metasploit). However, this assumes that `AlwaysInstallElevated` was previosuly set by an admin per-machine on the system: `C:\>reg add HKLM\Software\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated /t REG_DWORD /d 1`


Links:
1. https://learn.microsoft.com/en-us/windows/win32/msi/alwaysinstallelevated
2. https://learn.microsoft.com/en-us/sysinternals/downloads/accesschk
3. https://github.com/googleprojectzero/symboliclink-testing-tools/releases/download/v1.0/Release.7z


---

### The cause


#### What version of Chrome have you found the security issue in?

Latest, consumer/enterprise/education installers 


#### Is the security issue related to a crash?

No


#### Choose the type of vulnerability

Privilege Escalation 


#### How would you like to be publicly acknowledged for your report?

Bahaa Naamneh of Crosspoint Labs




## Attachments

- [procmon.png](attachments/procmon.png) (image/png, 139.8 KB)
- [IMG_3456.png](attachments/IMG_3456.png) (image/png, 251.7 KB)

## Timeline

### ch...@appspot.gserviceaccount.com (2023-08-13)

[Empty comment from Monorail migration]

### pg...@google.com (2023-08-13)

[Empty comment from Monorail migration]

### aj...@chromium.org (2023-08-14)

I've not completely repro'd this but it seems reasonable.

In particular - setup.exe /does/ delete HKCU\SOFTWARE\Microsoft\Active Setup\Installed Components\{8A69D345-D564-463c-AFF1-A69D9E530F96} as a trusted user in normal operations.

In some of my VM installs this is not a security issue as the local user already has RW access to the HKEY_CURRENT_USER\Software\Policies key

```
C:\src>c:\SysInternals\accesschk.exe -nobanner -d -k HKEY_CURRENT_USER\Software\Policies
HKCU\Software\Policies
  RW NT AUTHORITY\SYSTEM
  RW BUILTIN\Administrators
  R  NT AUTHORITY\RESTRICTED
  RW DESKTOP-K26HIJ4\user
  R  APPLICATION PACKAGE AUTHORITY\ALL APPLICATION PACKAGES
  R  S-1-15-3-1024-1065365936-1281604716-3511738428-1654721687-432734479-3232135806-4053264122-3456934681
```

But on other installs the normal user does not:

```
D:\> D:\SysInternals\accesschk.exe -nobanner -d -k HKEY_CURRENT_USER\Software\Policies
HKCU\Software\Policies
  RW NT AUTHORITY\SYSTEM
  RW BUILTIN\Administrators
  R  DOMAIN\user
  R  APPLICATION PACKAGE AUTHORITY\ALL APPLICATION PACKAGES
  R  S-1-15-3-1024-1065365936-1281604716-3511738428-1654721687-432734479-3232135806-4053264122-3456934681
```

See attached procmon.png for descending past the symlink and deleting children (note that the failed deletions succeed later once child keys are gone).

plus procmon traces of uninstallation:

without symlink - https://drive.google.com/file/d/1E4km9jFPYxSm8OgxMIrT4Sonnvq9lrRM/view?usp=sharing
with symlink - https://drive.google.com/file/d/1g5uIkPr2caN1RLnLFfmG8g48GAffwWsU/view?usp=drive_link

Impact
=======
This is a local attack and requires the user to be allowed to elevate to run the uninstaller  in step (4) at which point they could simply delete the key themselves so the practical effects of this are limited.

However, this might be useful in an insider threat situation where a user convinces an admin to reinstall chrome for them so we should address it.

Because of this the issue is Low severity at best. FoundIn 114 as current extended stable.

Thoughts
========
RegDelRecurse might need to become symlink aware - or perhaps we can use RegDeleteTree

https://source.chromium.org/chromium/chromium/src/+/main:base/win/registry.cc;drc=c8a629d7be311323904c523d33693af8f52d17e9;l=494



[Monorail components: Internals>Installer]

### [Deleted User] (2023-08-14)

[Empty comment from Monorail migration]

### wa...@chromium.org (2023-08-14)

[Empty comment from Monorail migration]

### b....@gmail.com (2023-08-15)

First, regarding your procmon output, on my VM I was able to completely delete the `policies` registry key.

Now as for your impact analysis:
Admin accounts on Windows are authorized to set local group policies, so naturally, they will have their `policies` registry key under HKCU with both READ and WRITE permissions. While standard/normal accounts are not, so they will have READ-ONLY access on `policies`. In corporate environment, if an employee is given a managed Windows system then he/she is most definitely given a standard/normal account on Windows. Also, even in consumer environment, standard/normal account is probably more common especially that Microsoft discourages people from running with Admin account by default.

I don't particularly agree with your impact classification, as this issue is just as relevant in the local attacker situation, so if an attacker manages to get their malware to run on the system, it's not that hard to get an admin to uninstall and then reinstall Chrome, and here is a scenario for how that can potentially happen:
1. Malware is running as part of a standard account on Windows on an employee laptop or grandma laptop
2. Malware can disrupt Chrome, potentially deleting files or registry keys that belong to the browser if it has access to do so. Otherwise, they can be more creative, for example introducing an error-displaying executable. This error message could suggest an 'uninstall', and then alter the Chrome shortcut on the user's desktop to point to this executable. I'm sure there are many other ways to cause Chrome to stop working on the user's system.
3. At this point the employee would call their IT department, or the grandma would call her grandson to fix Chrome for them, and obviously, uninstalling and then reinstalling Chrome will be high on their list of actions to fix it, if not the only possible action.

So a more sever impact definitely exist in the local attacker situation where an attacker wishes to elevate their privileges on the system, as this can be achieved within a very short time, likely within max a few hours, as described above.



### aj...@chromium.org (2023-08-15)

> regarding your procmon output

Sorry I wasn't clear - the operations did indeed eventually delete the entire subtree - the full trace is stored on the drive links I added.


### gr...@chromium.org (2023-08-15)

another option would be to have DeleteUserRegistryKeys in uninstall.cc check that key_path isn't a symlink before deleting it. then again, there are likely other keys in HKCU that a system-level uninstaller will delete, so making DeleteKey use REG_OPTION_OPEN_LINK seems like a good thing. if memory serves, base::DeletePathRecursively doesn't follow links, so doing the same in the registry is consistent.

### b....@gmail.com (2023-08-15)

I think you may want to adjust the severity of this issue, because it is actually worse than I initially thought. Chrome seems to give WRITE permission on registry keys (see below) within the HKLM registry hive to normal Windows users, which means a local attacker running as a standard/normal user can create a symlink to any key within HKLM and that can lead to serious consequences including: 
1) Removing all group policies set per-machine as it is possible to delete 'HKLM\SOFTWARE\Policies'. Recreating that key in HKLM to set group policies might be challenging, and haven't investigated that yet. 
2) Brick the entire operating system, since you can point the symlink to a critical registry key (for example to 'HKLM\SYSTEM\CurrentControlSet\Services') 
3) Possible complete privilege escalation from normal user to SYSTEM
4) Possibly overwriting protected registry values within HKLM

Here are the two registry keys that Chrome grants WRITE permission on to normal users (there could be more keys like that):

HKLM\SOFTWARE\WOW6432Node\Google\Update\ClientStateMedium\{8A69D345-D564-463C-AFF1-A69D9E530F96}\FirstNotDefault

HKLM\SOFTWARE\WOW6432Node\Google\Update\ClientStateMedium\{8A69D345-D564-463C-AFF1-A69D9E530F96}\LastWasDefault

### gr...@chromium.org (2023-08-15)

i've started kicking around a CL for this. i'm afraid it's going to be a little tricky. it seems that it's not possible to delete a link using the normal advapi winreg API. i'll hack on it a bit more tomorrow to see if i can get something working. @waffles: feel free to take it if you'd like. here's what i have so far: https://chromium-review.googlesource.com/c/chromium/src/+/4778429

### b....@gmail.com (2023-08-15)

That is correct, you cannot use Win32 APIs to delete registry symlinks! I gave a talk on registry symlinks during RSAC conference in April this year, here is the link for my talk for additional information on this topic: https://www.youtube.com/watch?v=8YTECpf4NF4

### aj...@chromium.org (2023-08-15)

Hi b.naamneh@gmail.com - I've set the severity based on the need for a local attacker and the need for Admin at some stage - our severity guidelines help us prioritize issues that affect people browsing the web and might not align with those of other products. Don't worry - we're actively looking at fixing this issue!

Thanks for the link to the talk!

### [Deleted User] (2023-08-15)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### b....@gmail.com (2023-08-15)

@ajgo, sounds good.

just fyi, I don't have time to test this today, but I'm almost certain I can achieve a full privilege escalation from a standard user to SYSTEM using this vulnerability by possibly:
1. Create a symlink at `HKLM\SOFTWARE\WOW6432Node\Google\Update\ClientStateMedium\{8A69D345-D564-463C-AFF1-A69D9E530F96}\FirstNotDefault` that points to an AppID that runs as a SYSTEM, for example, this `HKLM\SOFTWARE\Classes\AppID\{37096FBE-2F09-4FF6-8507-C6E4E1179839}` (which corresponds to the "Security Health Agent Host")
2. When Chrome uninstaller kicks in, the `AppID\{3709..39}` will be deleted
3. Since Windows merges both `HKEY_CURRENT_USER\Software\Classes` and `HKEY_LOCAL_MACHINE\SOFTWARE\Classes` into HKEY_CLASSES_ROOT, the local attacker can create the same GUID under `HKEY_CURRENT_USER\Software\Classes` but instead make the registry value `DllSurrogate` under it, point to its malicious executable
4. Next time a COM object is created to communicate with the original "Security Health Agent Host", should launch the local attacker executable as SYSTEM

This has not be validated, just a thought for a possible way a local attacker can fully elevate their privileges to SYSTEM.

Also, it's possible that there are other ways to achieve full privilege escalation to SYSTEM.

### ga...@chromium.org (2023-08-15)

Re https://crbug.com/chromium/1472558#c14, step 3 and 4 would not work, since if the integrity level of a process is higher than Medium, the COM runtime ignores per-user COM configuration and accesses only per-machine COM configuration. 

https://learn.microsoft.com/en-us/previous-versions/bb756926(v=msdn.10)#:~:text=Beginning%20with%20Windows,an%20elevated%20process.

### ga...@chromium.org (2023-08-16)

Hi @grt, I made a bunch of changes and uploaded a new patchset at https://chromium-review.googlesource.com/c/chromium/src/+/4778429/2. This is much more trickier. And the UT you wrote fails with my changes. Need to debug.

### gr...@chromium.org (2023-08-16)

after sleeping on it, how about we simply not touch symbolic links while deleting? my thinkig is: we didn't put them there, so we're not doing any harm if we fail to delete them. thoughts? i'll see how simple this is in my WIP CL.

### gr...@chromium.org (2023-08-16)

i've gone ahead and uploaded a patch set that skips symbolic links when deleting in base::win::RegKey, and has added complexity in RegistryOverrideManager to delete symlinks without following them. wdyt? it keeps the product code a bit simpler.

also, i went for a cheaper way to detect links. it's not 100% correct, but it's conservative (a possibility of false positives, but not false negatives). thoughts welcome.

i don't know what to do about the one failing test. yandex added that test. i'm inclined to delete it and see who complains. :-)  my cheap way to detect links requires opening a key with KEY_QUERY_VALUE to see if it has a SymbolicLinkValue REG_LINK value. if the rights only allow DELETE, this fails.

what test failure were you seeing with your code? can you make your variant detect-and-skip links rather than trying to delete them?

### ga...@chromium.org (2023-08-17)

I love your simpler logic for symbolic links, and have amended my change to use your logic to detect symbolic links, and removed all the NT undocumented enum/struct/defines. The test failure before was because the code needed `KEY_QUERY_VALUE` rights. 

I still have kept the logic to delete links. ptal: https://chromium-review.googlesource.com/c/chromium/src/+/4778429/2..7

The yandex test fails for me as well, same reason as yours. I'm ok with deleting it :)


### b....@gmail.com (2023-08-20)

The proposed solution for addressing the symbolic link deletion issue seems reasonable to me. However, there are two points I'd like to draw your attention to:

1. Ideally, it is not advisable to grant WRITE permissions to standard/regular Windows accounts for any key within the HKLM hive. It is recommended to be as restrictive as possible. Giving `KEY_SET_VALUE` and `KEY_CREATE_SUB_KEY` is risky, as it is in this case: https://github.com/chromium/chromium/blob/main/chrome/updater/app/app_server_win.cc#L106

2. Although issue #1 may no longer be a concern once your fix for deleting registry symlinks is merged, there could be a potential future problem. If a user manages to create a symlink at a writable location within the registry and point it to a protected registry key, and a privileged process associated with Chrome writes to that symlink, it may inadvertently modify the protected registry key. It's unlikely that the privileged process would write something like "Enable=0" or "Disable=1" which can be of value to the attacker, but it might invoke RegCopyTree API where the target is the key that happens to be modified to become a symlink by the attacker. This could be exploited by an attacker to manipulate the privileged process into copying values to a protected registry location through a symlink. E.g. to write "EnableLUA=0" to disable UAC in Windows.

I wouldn't categorize writing to a protected registry location via a registry symlink as an important issue at this moment, and you may choose to overlook it. However, it's good to stay aware of this potential vulnerability for future reference.

### ga...@chromium.org (2023-08-22)

Thank you for your feedback re https://crbug.com/chromium/1472558#c20, makes sense. We'll see if there is a way to do this going forward without modifying ACLs.

On a related, I landed a change to Omaha (GoogleUpdate) to delete symbolic links if they are encountered. This will ship with the next GoogleUpdate release next month.

### gi...@appspot.gserviceaccount.com (2023-08-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/73fb7b02ef1440141c3d725cb83b4f4c0114abdf

commit 73fb7b02ef1440141c3d725cb83b4f4c0114abdf
Author: Greg Thompson <grt@chromium.org>
Date: Tue Aug 22 08:49:29 2023

[windows] Do not follow symlinks when deleting keys in the registry

Also delete DeleteRegistryKeyTest.DeleteAccessRightIsEnoughToDelete,
which is incompatible with the new RegKey::DeleteKey.

Bug: 1472558
Change-Id: I15df7756766923772b477285249a6027f1211a7c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4789249
Reviewed-by: S Ganesh <ganesh@chromium.org>
Commit-Queue: Greg Thompson <grt@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1186355}

[modify] https://crrev.com/73fb7b02ef1440141c3d725cb83b4f4c0114abdf/base/win/registry.h
[modify] https://crrev.com/73fb7b02ef1440141c3d725cb83b4f4c0114abdf/chrome/installer/util/registry_util_unittest.cc
[modify] https://crrev.com/73fb7b02ef1440141c3d725cb83b4f4c0114abdf/base/win/registry.cc
[modify] https://crrev.com/73fb7b02ef1440141c3d725cb83b4f4c0114abdf/base/win/registry_unittest.cc


### gr...@chromium.org (2023-08-22)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-22)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-22)

[Empty comment from Monorail migration]

### am...@google.com (2023-09-21)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-09-21)

Congratulations Bahaa! The Chrome VRP Panel has decided to award you $3,000 for this report. The reward amount was based on the preconditions of local access + access to Admin page or social engineering of an Administrator. 
A member of our finance team will be in touch with you soon to arrange payment. Thank you for your efforts and reporting this issue to us -- nice work! 

### b....@gmail.com (2023-09-22)

Thank you, appreciate that!

### am...@google.com (2023-09-22)

[Empty comment from Monorail migration]

### pg...@google.com (2023-10-09)

[Empty comment from Monorail migration]

### pg...@google.com (2023-10-11)

[Empty comment from Monorail migration]

### pg...@google.com (2023-10-11)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-28)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ga...@chromium.org (2024-01-05)

Greg, does it also make sense to fix the "Brick the entire operating system, since you can point the registry link to a critical registry key (for example to 'HKLM\SYSTEM\CurrentControlSet\Services')" issue, so when Chrome writes to the ClientStateMedium key, it does not write to a symlinked entry?

If this does not make sense, please (re)close this issue, thank you!



### ga...@chromium.org (2024-01-05)

Re https://crbug.com/chromium/1472558#c34, it's not as bad if Chrome only write to `ClientStateMedium` when running at Medium integrity. In that case, Chrome would not be able to write to a redirected privileged entry, because of a lack of permissions.

The only case would be if an elevated instance were to write to `ClientStateMedium`. As long as that is not the case, we can close this issue. 

### gr...@chromium.org (2024-01-08)

AppendPostInstallTasks will try to create the key HKLM\Software\Google\Update\ClientStateMedium\{APPGUID} in a high integrity setup.exe. that's the only write i can find. i don't see any writes or deletes.

### ga...@chromium.org (2024-01-09)

Sounds good, I'll close this as fixed then, thanks Greg.

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1472558?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1472559]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40069458)*
