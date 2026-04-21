# 
Chromium arbitrary file create/write and execute vulnerability

| Field | Value |
|-------|-------|
| **Issue ID** | [356328460](https://issues.chromium.org/issues/356328460) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Installer |
| **Platforms** | Windows |
| **Chrome Version** | 127.0.0.0 |
| **Reporter** | in...@gmail.com |
| **Assignee** | ga...@chromium.org |
| **Created** | 2024-07-30 |
| **Bounty** | $2,000.00 |

## Description

# Steps to reproduce the problem

1. Install chromium at system level using the command `mini_installer.exe --system-level` (It can come from SSCM or someone who has administrator access)
2. Uninstall chromium with SYSTEM account(SCCM or other deployment tools) using the setup.exe available in the install location using the command `"C:\Program Files\Chromium\Application\127.0.6533.0\Installer\setup.exe" --uninstall --system-level`
3. Uninstaller creates a file under C:\Windows\Temp on which even standard user(non admin) has write permission.
4. Using the NtApiDotNet.dll, a symlink can be created without requiring admin access to redirect the file creation to any other system critical resources which will lead to DOS or even code execution can be achieved.

# Problem Description

The culprit code is <https://source.chromium.org/chromium/chromium/src/+/main:chrome/installer/setup/uninstall.cc;l=1120> where the DIR\_TEMP results in C:\windows\temp when running as SYSTEM account. The function `MoveSetupOutOfInstallFolder` is meant for moving the setup.exe and also dlls(in case of component build) to the temporary location which is C:\windows\temp with a temporary name generated using GUID. The another issue is the name can be easily predicted since its being opened and closed. API like FindFirstChangeNotificationA can be used to know the new file name of the setup.exe which is going to be used while moving to C:\Windows\temp. The below POC code can be used to create a symlink. The work required for detecting the file name using FindFirstChangeNotificationA is not done as I am occupied with other things but I can share it in a day or two

# Import the NtApiDotNet module

Import-Module ".\NtApiDotNet.dll" -ErrorAction Stop

# Define the temporary path and get the Windows directory path using the environment variable

$tempDirectory = [System.IO.Path]::Combine($env:WINDIR, "Temp")
$system32Path = [System.IO.Path]::Combine($env:WINDIR, "System32")
$outputDllPath = [System.IO.Path]::Combine($system32Path, "drivers\cng1.sys")

# Find the file name using FindFirstChangeNotification API and target that file for creating symlink

#$guidDFileName - To do.

# Create a mount point

[NtApiDotNet.NtFile]::CreateMountPoint("??$tempDirectory", "\RPC Control", $null)

# Create a symbolic link

$outputLink = [NtApiDotNet.NtSymbolicLink]::Create("\RPC Control" + $guidDFileName, "??$outputDllPath")

# Additional Comments

This is similar to <https://issues.chromium.org/issues/40063745> which allows for permanent DOS but also provides code execution. Not sure if we can do much with setup.exe but with component build, dlls can be used. But can't think of any use case. But its a strong and easy candidate for making machine unbootable leading to permanent DOS

# Summary

Chromium arbitrary file create/write and execute vulnerability

# Additional Data

Category: Security   

Chrome Channel: Stable   

Regression: N/A

## Attachments

- [POC2.zip](attachments/POC2.zip) (application/zip, 1.1 MB)
- [HijackPOC.zip](attachments/HijackPOC.zip) (application/zip, 4.5 MB)

## Timeline

### dc...@chromium.org (2024-07-30)

Have you managed to reproduce an escalation of privilege using this vector? I've read through the report, and the snippet of code you referenced. The code in question seems like it would error out if someone tries to hijack one of the file paths by checking that the file move actually succeeds, and so it's difficult to see how this would lead to an actual bug.

### ap...@google.com (2024-07-30)

Project: chromium/src
Branch: main

commit a5bea52e51947236609acdf5ba052a5bcf1b96f8
Author: S. Ganesh <ganesh@chromium.org>
Date:   Tue Jul 30 22:30:08 2024

    chrome setup: use the secure temp directory instead of DIR_TEMP
    
    Fixed: 356328460
    Change-Id: I22fbc21d954f9bcba0d45eb9a19bc7857b3c621f
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5748495
    Commit-Queue: Will Harris <wfh@chromium.org>
    Auto-Submit: S Ganesh <ganesh@chromium.org>
    Code-Coverage: findit-for-me@appspot.gserviceaccount.com <findit-for-me@appspot.gserviceaccount.com>
    Reviewed-by: Will Harris <wfh@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1335132}

M       chrome/installer/setup/uninstall.cc

https://chromium-review.googlesource.com/5748495


### in...@gmail.com (2024-07-30)

Hi, I haven't exactly done it yet. But it should be possible to plant/replace exe or dlls on any restricted location including the critical paths of OS. Allow me a day, I can share you the POC you can use to verify which includes the filename detection too.
Let me share more details on how MoveSetupOutOfInstallFolder() at https://source.chromium.org/chromium/chromium/src/+/main:chrome/installer/setup/uninstall.cc;l=1103 can be exploited. The function base::CreateTemporaryFileInDir() at https://source.chromium.org/chromium/chromium/src/+/main:chrome/installer/setup/uninstall.cc;l=1134 not only generates the filename but also creates a file and deletes it since FLAG_CAN_DELETE_ON_CLOSE is set at https://source.chromium.org/chromium/chromium/src/+/main:base/files/file_util_win.cc;drc=105770df485ace262780d95126bb60b1a16ec340;l=607. I believe its for making sure a file with that name doesn't exist. Just a GetFileAttribute() would have been enough. Since it creates and deletes the file, our POC code can detect the file name which got created using FindFirstChangeNotification and listen to reason file closed and immediately create symbolic link before an actual move of setup.exe and dlls are moved to C:\windows\Temp https://source.chromium.org/chromium/chromium/src/+/main:chrome/installer/setup/uninstall.cc;drc=3e79aface557755e09fd9a58f53da14bebf3eb1f;l=1142. This is a race, POC code has to win to allow arbitrary write of exe or a dll on any location we want in the system and this race can be won.

### pe...@google.com (2024-07-31)

Setting milestone because of s2 severity.

### pe...@google.com (2024-07-31)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### pe...@google.com (2024-07-31)

Requesting merge to beta (M128) because latest trunk commit (1335132) appears to be after beta branch point (1331488).
Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.

### pe...@google.com (2024-07-31)

Merge review required: M128 is already shipping to beta.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: harrysouders (Android), harrysouders (iOS), obenedict (ChromeOS), pbommana (Desktop)

### dc...@chromium.org (2024-08-01)

It's still not clear to me there's an actual exploitable condition here.

Using the secure temp directory is definitely better; however, the question of whether or not `MoveSetupOutOfInstallFolder()` would actually succeed with squatting has not been addressed. The code you linked to very clearly returns `false` if `base::Move()` fails; given that, it's unclear how squatting the file location would actually help with an exploit, because `MoveSetupOutOfInstallFolder()` would simply fail.

### in...@gmail.com (2024-08-01)

base::Move() is using MoveFileEx with MOVEFILE_COPY_ALLOWED | MOVEFILE_REPLACE_EXISTING. This is required to allow move across drives. I beleive MoveFileEx is not atomic. That allows one to create a symlink soon after it deletes the file if it exists but just before the file is copied which can be used to create file anywhere is the system. I guess SetOpLock() can be used to synchronise these.

### in...@gmail.com (2024-08-01)

It's much more simpler like I had initially thought. No need of using the non atomic nature of MoveFileEx(). I just created a symlink with name same as the temporary filename generated(detected using directory watcher) just before the base::Move() operation and let base::Move() to proceed. It succeeded and the move indeed happened on the symlink target location and MoveSetupOutOfInstallFolder() was successful.

### dc...@chromium.org (2024-08-01)

OK, but if it's using `MOVEFILE_REPLACE_EXISTING`, doesn't that clobber the symlink that you tried to hijack the location of?

### pe...@google.com (2024-08-01)

The NextAction date has arrived: 2024-08-01
To opt-out from this automation rule, please add Optout-Blintz-Nextaction-Alert to the "Chromium Labels" custom field.

### in...@gmail.com (2024-08-01)

No, it is not. I just had a look at procmon. When MOVEFILE_REPLACE_EXISTING is passed, it seems that the handle of the existing file is being opened and data is being copied to that directly and the file is either being truncated or extended based on the file being replaced is larger or smaller respectively. So MoveFileEx wont fail. In fact, it creates the file in the symbolic link target. Strange thing is I didn't see WriteFile calls in procmon. Just SetEndOfFile was there with a single handle opened to the exiting file. Wondering how the buffer was written onto the existing file handle.

### in...@gmail.com (2024-08-03)

Attached is the POC on dotnet which has two projects. HijackPOC and Setup which generates HijackPOC.exe and Setup.exe. Using a temporary directories like D:\Windows\Temp and D:\Windows\System32 for POC. SO have them created.

Setup.exe simulates the behavior of temporary deletion happens with https://source.chromium.org/chromium/chromium/src/+/main:chrome/installer/setup/uninstall.cc;l=1184 and the actual move at https://source.chromium.org/chromium/chromium/src/+/main:chrome/installer/setup/uninstall.cc;l=1192

HijackPOC.exe hijacks the MoveFileEx operation by creating a symlink with the name same as temporary name used by Setup.exe under D:\Windows\Temp.

Steps to use:
1. Build the projects.
2. Run HijackPOC.exe as standard user - It will start monitoring D:\Windows\Temp for any .tmp file creation and creates Symlink as soon as the tmp file is known
3. Run Setup.exe as SYSTEM
4. Viola, you have the critical.dll which is a copy of Setup.exe in D:\Windows\System32

### in...@gmail.com (2024-08-03)

Also could someone explain about the hotlist/tag label `Needs-Feedback` tagged on this issue and what it means. If anything else is required from me, drop a comment. I will be happy to provide

### am...@chromium.org (2024-08-05)

re: c#16 needs-feedback is to denote when more information is requested from the reporter, the automation failed to remove it once it was updated with a response

removing from merge label; generally not applicable for installer / updater issues, but there are also significant preconditions here and we should let this change matriculate on its own

### ga...@google.com (2024-08-13)

We are merging [bug 356064205](https://issues.chromium.org/issues/356064205) to 128, so may make sense to merge this one to 128 as well.

### pe...@google.com (2024-08-13)

Merge review required: M128 has already been cut for stable release.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: harrysouders (Android), harrysouders (iOS), obenedict (ChromeOS), pbommana (Desktop)

### am...@chromium.org (2024-08-13)

<https://crrev.com/c/5748495> approved for merge to M128; please merge to branch 6613 by noon Pacific time tomorrow, Tuesday, 13 August so this fix can be included in the Early Stable cut and last beta of M128 being cut tomorrow

### ap...@google.com (2024-08-13)

Project: chromium/src
Branch: refs/branch-heads/6613

commit 741ed491de31c8eb8a9b447779b93df87bd3d3f4
Author: S. Ganesh <ganesh@chromium.org>
Date:   Tue Aug 13 12:40:30 2024

    chrome setup: use the secure temp directory instead of DIR_TEMP
    
    (cherry picked from commit a5bea52e51947236609acdf5ba052a5bcf1b96f8)
    
    Fixed: 356328460
    Change-Id: I22fbc21d954f9bcba0d45eb9a19bc7857b3c621f
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5748495
    Commit-Queue: Will Harris <wfh@chromium.org>
    Auto-Submit: S Ganesh <ganesh@chromium.org>
    Code-Coverage: findit-for-me@appspot.gserviceaccount.com <findit-for-me@appspot.gserviceaccount.com>
    Reviewed-by: Will Harris <wfh@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1335132}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5784546
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Commit-Queue: S Ganesh <ganesh@chromium.org>
    Cr-Commit-Position: refs/branch-heads/6613@{#991}
    Cr-Branched-From: 03c1799e6f9c7239802827eab5e935b9e14fceae-refs/heads/main@{#1331488}

M       chrome/installer/setup/uninstall.cc

https://chromium-review.googlesource.com/5784546


### sp...@google.com (2024-08-21)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
$2,000 for report of lower impact LPE with significant preconditions for exploitation


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-08-22)

Congratulations! Thank you for your efforts and reporting this issue to us.

### pe...@google.com (2024-11-06)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> $2,000 for report of lower impact LPE with significant preconditions for exploitation

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/356328460)*
