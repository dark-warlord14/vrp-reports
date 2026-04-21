# Security: Chrome Update - Arbitrary Folder Delete // Privilege Escalation

| Field | Value |
|-------|-------|
| **Issue ID** | [40052705](https://issues.chromium.org/issues/40052705) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Installer |
| **Platforms** | Windows |
| **Reporter** | he...@gmail.com |
| **Assignee** | wf...@chromium.org |
| **Created** | 2020-06-29 |
| **Bounty** | $500.00 |

## Description

Google Chrome Updater - mklink folder junction - delete folder recursively as SYSTEM-User

**VERSION**

Chrome Version: all  

Operating System: Windows 10, 10.0.19041.329, 2004

**REPRODUCTION CASE**

1. Create junction as non-admin -> mklink /j c:\windows\temp\CR\_00000.tmp c:\
2. Wait for the Google Chrome update
3. The update process does not check if it is a junction, follows it and deletes all possible folders and files
4. This allows the reconstruction of deleted folders and files with malicious content and leads to a possible Privilege Escalation.

**CREDIT INFORMATION**

Reporter credit: Andrew Hess (any1)

## Attachments

- [chrome_update_install_mklink_exploit.mp4](attachments/chrome_update_install_mklink_exploit.mp4) (video/mp4, 4.6 MB)

## Timeline

### he...@gmail.com (2020-06-29)

Physical attacks should not actually be reported. In my opinion this is a special case. Chrome has a special position of responsibility because of its market position. Especially on multi-user systems (terminal servers) the vulnerability can cause great damage.

### bd...@chromium.org (2020-06-29)

Thank you for reporting this. I'm marking this as Won't fix due to https://chromium.googlesource.com/chromium/src/+/master/docs/security/faq.md#Why-arent-physically_local-attacks-in-Chromes-threat-model

### bd...@chromium.org (2020-06-29)

Sending this over to waffles (feel free to reassign) in case there might be something that can be addressed here. Changing this to a non-security bug.

[Monorail components: Internals>Installer]

### wa...@chromium.org (2020-06-29)

Thanks Bettina.

If possible I'd like to keep the restrict-view labels while we investigate.

At least on the face of it, this appears to be a privilege escalation that reproduces on my machines.

The part we're uncertain about is the user's right to operate in C:\Windows\Temp. Adding a few Windows experts.

[Monorail components: Security]

### so...@chromium.org (2020-06-29)

The vulnerability seems real. As a non-elevated user, I am able to create such link in Windows temp (from a shell window), then elevated code (from a different shell window) can follow the junction and delete the target of the junction. 

### gr...@chromium.org (2020-06-30)

The remediation is for chrome/installer/mini_installer/mini_installer.cc's DeleteDirectoriesWithPrefix to skip directories that have reparse points, no? If so, this is trivial and I think we should do it. Feel free to either send a review my way, or ask me to do it (I don't want to steal your thunder if you want it, Josh. :-) ).

### wa...@chromium.org (2020-06-30)

Please, go for it, I think I understand the change (just a one-liner on :756?) but I'm not very familiar with the code or with NTFS junctions. 

A larger concern I think would be that if a user-level program can modify the contents of C:\Windows\Temp, are we certain we can trust what we've unpacked and are executing? Maybe in practice it is not an issue, but this seems like potentially a plentiful source of bugs. So I'd like to understand better what a user is permitted to do in C:\Windows\Temp.

### he...@gmail.com (2020-06-30)

Hello everyone,

i have already checked if the actual update destination folder can be attacked, e.g. via DLL hijacking from setup.exe. This is not possible, because normal users have no write permission there. Looks good for now.

Please also make sure that the updater/installer does not follow the C:\Windows\Temp\chrome_* folder with a junction. Could not look into the source code yet, if the same function is used.

With kind regards,
Andrew Hess

### he...@gmail.com (2020-06-30)

Maybe for security reasons, increase the possible places for the update temp folder. 16^5 = 1048576 possibilities are a bit few. 

### gr...@chromium.org (2020-07-01)

I have a CL up for the junction point issue. Thanks for bringing this to our attention, Andrew.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-07-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/a26f896bf8e7cad61907cdbc90da91ef50e6232e

commit a26f896bf8e7cad61907cdbc90da91ef50e6232e
Author: Greg Thompson <grt@chromium.org>
Date: Wed Jul 01 16:08:30 2020

Don't cross junction points when deleting old temp dirs.

During startup, the mini_installer attempts to free up disk space left
occupied by previous runs of the installer that may have failed to
perform their own cleanup. Such freeing shouldn't cross junction points
or links or other similar filesystem constructs, since such would not
have been created by a previous run. This CL simply skips over any
directories that have reparse points -- directories created by the
installer should not have any.

BUG=1100280
R=waffles@chromium.org

Change-Id: I20d874db50bd11faeac8e03522d162abcae095b0
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2276207
Commit-Queue: Greg Thompson <grt@chromium.org>
Commit-Queue: Joshua Pawlicki <waffles@chromium.org>
Auto-Submit: Greg Thompson <grt@chromium.org>
Reviewed-by: Joshua Pawlicki <waffles@chromium.org>
Cr-Commit-Position: refs/heads/master@{#784428}

[modify] https://crrev.com/a26f896bf8e7cad61907cdbc90da91ef50e6232e/chrome/installer/mini_installer/mini_installer.cc


### he...@gmail.com (2020-07-01)

Thank you for patching this. Are you opening a CVE on this or should I create one?

### gr...@chromium.org (2020-07-01)

Bouncing over to wfh@ for CVE question in https://crbug.com/chromium/1100280#c12.

### wf...@chromium.org (2020-07-06)

This seems to fall into the spirit of a security bug, even though it does require physical access to carry out the attack (and an attacker with physical access could do a lot more damage) - and also the fact that we did land a fix. So I'll chat with adetaylor about whether this needs a CVE and or to be evaluated for VRP panel. I'll add reward-topanel to make sure this doesn't slip through the cracks.

If this is Fixed in code then can it be marked Fixed?

### fo...@chromium.org (2020-07-07)

Looking at the patch you check for the reparse point on the top-level directory but not in RecursivelyDeleteDirectory so you could bypass the patch by just creating a sub-directory which is a reparse point unless there's some higher reason which prevents that from happening (I don't see one). This is of course irrespective of the racey nature of this check as an active attacking process on the system could switch a directory to a reparse point after the enumeration has occurred bypassing the initial check.

Also I'm not sure where the assessment of physical access is required. You need user level access (so not sandbox access) but certainly don't need to be physically present at the console from what I can tell. Supposedly at some point Windows will stop using C:\WINDOWS\TEMP for SYSTEM processes, but seems that it didn't make the cut for 2004.

You might want to loop me in on bugs of this nature in the future.

### ad...@chromium.org (2020-07-07)

Thanks for looping me in too!

An offline discussion took place today and the consensus is that we should consider this a valid security bug, so I'm adjusting thusly. The security FAQ will be adjusted (https://chromium-review.googlesource.com/c/chromium/src/+/2284209 - work in progress). The offline chat also determined that we're going to mark Security_Severity as Low. I'm assuming this affects stable builds so setting impact appropriately too.

By moving this to the security queue, several processes automatically fall into place:
- yes, a CVE will be allocated when we release the fix.
- sheriffbot will add all sorts of labels
- yes, we want to mark it fixed. waffles@, if you can confirm that the above fix is complete, please do so.

### gr...@chromium.org (2020-07-07)

forshaw: do you think we should resolve the raciness? for example, we could hold a handle on each normal directory while deleting its contents so that other software can't replace a regular dir with one that has a reparse point during the enumeration.

### he...@gmail.com (2020-07-07)

In my vulnerability test I saw that you already have a fallback for the setup.exe, if e.g. all 1048576 possible CR_* combinations are used. Why not do without C:\Windows\Temp and always use the fallback folder.

e.g. C:\Program Files (x86)\Google\Update\Install\{4088EA6E-B227-4CDC-8AC5-B796011D093E}\CR_5B32F.tmp\setup.exe

@forshaw: The Chrome's Vulnerability Disclosure Policy expresses itself very strangely there in terms of physical attacks. For me this vulnerability is not covered by it.

It is a great honor for me that Project Zero is represented here.

### [Deleted User] (2020-07-07)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2020-07-07)

After further discussion within the security team, we're going to ramp this up to High severity.

### fo...@chromium.org (2020-07-08)

grt@ solving the race would be good to do, normally the only real way to do that if you're deleting from an unsafe location is to open the file/directory target, compare the final path to the expected one and then use SetFileInformationByHandle to mark the file for deletion if it's as expected. However as noted by hess.andrew@ the best way would be to not create these files in the shared temporary folder at all, instead placing them in an admin only location. If that's what we're already resigning ourselves to do anyway if space in TEMP runs out then just promote it to the only way of doing it.

If neither of these approaches are acceptable then about the only thing to do is use some sort of out-of-band list of directories for deletion, such as writing to a HKEY_LOCAL_MACHINE admin only key when creating the directory and only removing directories in that list. Of course this could result in a stale list which could then be abused, but hopefully it'd be hard to do that generally (unless there's a trivial bug which could allow these entries to be created). 

Do we have any statistics on how often we're cleaning up directories? Is this related in someway to the unreliability of deleting files on Windows due to various reasons such as AV? I'm wondering how much we really need to do the cleanup, instead relying on the builtin Windows Disk Cleanup tool to do is for us?

### [Deleted User] (2020-07-08)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-07-08)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gr...@chromium.org (2020-07-10)

hi forshaw@. full disks is a common cause for install/update failure. this deletion was added to at least stop the filling-up of disks by our own code.

i'll take a look at making an updater-provided location the default. i also think we could be nicer about holding files open with the delete-on-close flag set so that they disappear automagically when we're done with them; even if we crash. if that would reduce the leaks to trips over the power cord and particularly bad a/v, maybe that's low enough into the noise floor that we can stop trying to do the deletes like this. wdyt?

### fo...@chromium.org (2020-07-10)

If we can mark all files as delete on close that would be perhaps the better solution but probably tricky to achieve in practice. Perhaps should push this to a separate improvement issue?

### ad...@google.com (2020-07-13)

grt@ - should we merge the commit in https://crbug.com/chromium/1100280#c11 to M85 and/or M84? Sheriffbot will automate the labelling for merge, but only after this bug is marked as Fixed.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-07-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/291165d216e5f40572745ca345b78cd927168762

commit 291165d216e5f40572745ca345b78cd927168762
Author: Greg Thompson <grt@chromium.org>
Date: Mon Jul 13 16:27:24 2020

Don't cross junction points when deleting old temp dirs (again).

https://crrev.com/784428 stopped recursing across junction points when
looking for CR_* or chrome_* directories. This CL does the same when
deleting within those directories.

BUG=1100280
R=forshaw@chromium.org

Change-Id: I7a4ef84d9df744cf5d0bd64d51065a571228520d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2292395
Reviewed-by: James Forshaw <forshaw@chromium.org>
Commit-Queue: Greg Thompson <grt@chromium.org>
Cr-Commit-Position: refs/heads/master@{#787752}

[modify] https://crrev.com/291165d216e5f40572745ca345b78cd927168762/chrome/installer/mini_installer/mini_installer.cc


### gr...@chromium.org (2020-07-13)

forshaw@: i think that r784428 and r787752 address the reported issue. while there is room for improvement (i'm pondering using using delete-on-close now), do you consider this enough to call the bug fixed and take the merges?

### [Deleted User] (2020-07-15)

[Empty comment from Monorail migration]

### gr...@chromium.org (2020-07-22)

wfh: could you comment on https://crbug.com/chromium/1100280#c28?

### [Deleted User] (2020-07-23)

wfh: Uh oh! This issue still open and hasn't been updated in the last 17 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### fo...@chromium.org (2020-08-03)

Sorry I missed this. I think the two revisions fix the immediate issue. 

### ad...@google.com (2020-08-03)

Marking as Fixed as discussed with wfh@. That would, I believe, cause Sheriffbot to add merge requests to M84 and M85, so I'll short circuit the process.

Please comment on any stability risks of merging. We'd likely merge to M84 this week for release early next week.

### [Deleted User] (2020-08-03)

This bug requires manual review: M85's targeted beta branch promotion date has already passed, so this requires manual review
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), bindusuvarna@(iOS), dgagnon@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2020-08-03)

I'd like to merge this to M84 and M85. The fix in gerrit will certainly give attackers useful clues about what they might do with this, so it seems wise to ship the fix rapidly.

wfh@, forshaw@, grt@, I'm approving merge here UNLESS you foresee any stability risks or if there any problems showing up in Canary - please check.
Approving merge to M85, branch 4183.
Approving merge to M84, branch 4147.

### gr...@chromium.org (2020-08-04)

I think they're super safe. They do nothing more than skip directories that have reparse points while doing a recursive delete.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-08-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/d4348f8f20a2c9f73ace20a5244d4825df15871c

commit d4348f8f20a2c9f73ace20a5244d4825df15871c
Author: Greg Thompson <grt@chromium.org>
Date: Tue Aug 04 16:21:48 2020

Don't cross junction points when deleting old temp dirs.

During startup, the mini_installer attempts to free up disk space left
occupied by previous runs of the installer that may have failed to
perform their own cleanup. Such freeing shouldn't cross junction points
or links or other similar filesystem constructs, since such would not
have been created by a previous run. This CL simply skips over any
directories that have reparse points -- directories created by the
installer should not have any.

BUG=1100280
R=​waffles@chromium.org

(cherry picked from commit a26f896bf8e7cad61907cdbc90da91ef50e6232e)

Change-Id: I20d874db50bd11faeac8e03522d162abcae095b0
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2276207
Commit-Queue: Greg Thompson <grt@chromium.org>
Commit-Queue: Joshua Pawlicki <waffles@chromium.org>
Auto-Submit: Greg Thompson <grt@chromium.org>
Reviewed-by: Joshua Pawlicki <waffles@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#784428}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2336086
Reviewed-by: Greg Thompson <grt@chromium.org>
Cr-Commit-Position: refs/branch-heads/4147@{#1020}
Cr-Branched-From: 16307825352720ae04d898f37efa5449ad68b606-refs/heads/master@{#768962}

[modify] https://crrev.com/d4348f8f20a2c9f73ace20a5244d4825df15871c/chrome/installer/mini_installer/mini_installer.cc


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-08-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/1cbc19b7d65be591c093df8ce3069d3acb8746cf

commit 1cbc19b7d65be591c093df8ce3069d3acb8746cf
Author: Greg Thompson <grt@chromium.org>
Date: Tue Aug 04 16:29:11 2020

Don't cross junction points when deleting old temp dirs.

During startup, the mini_installer attempts to free up disk space left
occupied by previous runs of the installer that may have failed to
perform their own cleanup. Such freeing shouldn't cross junction points
or links or other similar filesystem constructs, since such would not
have been created by a previous run. This CL simply skips over any
directories that have reparse points -- directories created by the
installer should not have any.

BUG=1100280
R=​waffles@chromium.org

(cherry picked from commit a26f896bf8e7cad61907cdbc90da91ef50e6232e)

Change-Id: I20d874db50bd11faeac8e03522d162abcae095b0
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2276207
Commit-Queue: Greg Thompson <grt@chromium.org>
Commit-Queue: Joshua Pawlicki <waffles@chromium.org>
Auto-Submit: Greg Thompson <grt@chromium.org>
Reviewed-by: Joshua Pawlicki <waffles@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#784428}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2336834
Reviewed-by: Greg Thompson <grt@chromium.org>
Cr-Commit-Position: refs/branch-heads/4183@{#1197}
Cr-Branched-From: 740e9e8a40505392ba5c8e022a8024b3d018ca65-refs/heads/master@{#782793}

[modify] https://crrev.com/1cbc19b7d65be591c093df8ce3069d3acb8746cf/chrome/installer/mini_installer/mini_installer.cc


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-08-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/3a81460dbe4e2518842438023811b05542aa94f5

commit 3a81460dbe4e2518842438023811b05542aa94f5
Author: Greg Thompson <grt@chromium.org>
Date: Tue Aug 04 16:57:45 2020

Don't cross junction points when deleting old temp dirs (again).

https://crrev.com/784428 stopped recursing across junction points when
looking for CR_* or chrome_* directories. This CL does the same when
deleting within those directories.

BUG=1100280
R=​forshaw@chromium.org

(cherry picked from commit 291165d216e5f40572745ca345b78cd927168762)

Change-Id: I7a4ef84d9df744cf5d0bd64d51065a571228520d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2292395
Reviewed-by: James Forshaw <forshaw@chromium.org>
Commit-Queue: Greg Thompson <grt@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#787752}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2335288
Reviewed-by: Greg Thompson <grt@chromium.org>
Cr-Commit-Position: refs/branch-heads/4183@{#1198}
Cr-Branched-From: 740e9e8a40505392ba5c8e022a8024b3d018ca65-refs/heads/master@{#782793}

[modify] https://crrev.com/3a81460dbe4e2518842438023811b05542aa94f5/chrome/installer/mini_installer/mini_installer.cc


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-08-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/a6fd9fe3f50a371ab2f165c282c61e60151ac2a2

commit a6fd9fe3f50a371ab2f165c282c61e60151ac2a2
Author: Greg Thompson <grt@chromium.org>
Date: Tue Aug 04 17:03:24 2020

Don't cross junction points when deleting old temp dirs (again).

https://crrev.com/784428 stopped recursing across junction points when
looking for CR_* or chrome_* directories. This CL does the same when
deleting within those directories.

BUG=1100280
R=​forshaw@chromium.org

(cherry picked from commit 291165d216e5f40572745ca345b78cd927168762)

Change-Id: I7a4ef84d9df744cf5d0bd64d51065a571228520d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2292395
Reviewed-by: James Forshaw <forshaw@chromium.org>
Commit-Queue: Greg Thompson <grt@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#787752}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2336088
Reviewed-by: Greg Thompson <grt@chromium.org>
Cr-Commit-Position: refs/branch-heads/4147@{#1021}
Cr-Branched-From: 16307825352720ae04d898f37efa5449ad68b606-refs/heads/master@{#768962}

[modify] https://crrev.com/a6fd9fe3f50a371ab2f165c282c61e60151ac2a2/chrome/installer/mini_installer/mini_installer.cc


### gr...@chromium.org (2020-08-04)

All merges done.

### [Deleted User] (2020-08-04)

[Empty comment from Monorail migration]

### ad...@google.com (2020-08-07)

[Empty comment from Monorail migration]

### ad...@google.com (2020-08-07)

[Empty comment from Monorail migration]

### ad...@google.com (2020-08-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-08-13)

Congratulations! The VRP panel has decided to award $500 for this bug. Someone from our finance team will be in touch to arrange payment.

### ad...@google.com (2020-08-13)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-08-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/3fca0043db3b3b90bbf7af30cfcc9c6d3d1203e9

commit 3fca0043db3b3b90bbf7af30cfcc9c6d3d1203e9
Author: Greg Thompson <grt@chromium.org>
Date: Mon Aug 17 22:03:57 2020

Create mini_installer.exe's work directory next to the binary.

mini_installer.exe requires a temporary directory in which to write
files during processing. Historically, this has been a directory under
%TMP%. While mini_installer does its level best to delete this directory
before terminating, it cannot always do so (e.g., third-party software
may have some files open, or the machine may lose power).
mini_installer.exe scans %TMP% at process startup to delete any stale
directories from previous runs to prevent unbounded accumulation said
directories.

In this CL, mini_installer.exe now creates its work directory in the
directory containing the executable itself. In the case of installations
driven by a variant of Omaha (e.g., Google Chrome), Omaha will
eventually clean any files/directories left behind.

This CL also results in successful runs sending up either 0x10000 or
0x20000 in ExtraCode1 based on whether or not the fallback to %TMP% was
used. This will inform us as to whether or not it's safe to remove that
fallback.

A note to the authors of other Chromium forks: this change in behavior
may impact you. Audit how your variant of mini_installer.exe is run and
ensure that any files or directories left in the same directory as it
are cleaned up.

BUG=516207,1100280

Change-Id: I7a8dd7981b26dbac10553747cfe32a40fb11f37b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2351989
Reviewed-by: S. Ganesh <ganesh@chromium.org>
Reviewed-by: Will Harris <wfh@chromium.org>
Commit-Queue: Greg Thompson <grt@chromium.org>
Cr-Commit-Position: refs/heads/master@{#798844}

[modify] https://crrev.com/3fca0043db3b3b90bbf7af30cfcc9c6d3d1203e9/chrome/installer/mini_installer/mini_installer.cc
[modify] https://crrev.com/3fca0043db3b3b90bbf7af30cfcc9c6d3d1203e9/chrome/installer/mini_installer/mini_installer.h
[modify] https://crrev.com/3fca0043db3b3b90bbf7af30cfcc9c6d3d1203e9/chrome/installer/mini_installer/mini_installer_unittest.cc


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-08-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/44f5ba08662c1ef755d920d0082c306f718de97a

commit 44f5ba08662c1ef755d920d0082c306f718de97a
Author: Greg Thompson <grt@chromium.org>
Date: Fri Aug 21 15:58:53 2020

[mini_installer] Move the fallback reporting to InstallerError.

https://crrev.com/798844 attempted to send up a signal regarding whether
or not the fallback temp directory was used. Unfortunately, Omaha does
not include the ExtraCode1 value for successful installs. It does,
however, send up success HRESULTS in the InstallerError value. This CL,
therefore, switches to that. The two values to look out for are
0x00044001 and 0x00044002 (two success HRESULTS in FACILITY_ITF that
otherwise appear to be unused).

BUG=516207,1100280

Change-Id: I319c5dbe7162543a71465238c5320719225fa1f7
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2368353
Auto-Submit: Greg Thompson <grt@chromium.org>
Commit-Queue: S. Ganesh <ganesh@chromium.org>
Reviewed-by: S. Ganesh <ganesh@chromium.org>
Cr-Commit-Position: refs/heads/master@{#800584}

[modify] https://crrev.com/44f5ba08662c1ef755d920d0082c306f718de97a/chrome/installer/mini_installer/mini_installer.cc


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-08-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/836a311cccea1d2af5c818886815511364121453

commit 836a311cccea1d2af5c818886815511364121453
Author: Greg Thompson <grt@chromium.org>
Date: Tue Aug 25 08:16:22 2020

Revert "[mini_installer] Move the fallback reporting to InstallerError."

This reverts commit 44f5ba08662c1ef755d920d0082c306f718de97a.

Reason for revert: This strategy doesn't work, so let's go back to the previous strategy. It doesn't work today, but will in an upcoming Google Update release.

Original change's description:
> [mini_installer] Move the fallback reporting to InstallerError.
> 
> https://crrev.com/798844 attempted to send up a signal regarding whether
> or not the fallback temp directory was used. Unfortunately, Omaha does
> not include the ExtraCode1 value for successful installs. It does,
> however, send up success HRESULTS in the InstallerError value. This CL,
> therefore, switches to that. The two values to look out for are
> 0x00044001 and 0x00044002 (two success HRESULTS in FACILITY_ITF that
> otherwise appear to be unused).
> 
> BUG=516207,1100280
> 
> Change-Id: I319c5dbe7162543a71465238c5320719225fa1f7
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2368353
> Auto-Submit: Greg Thompson <grt@chromium.org>
> Commit-Queue: S. Ganesh <ganesh@chromium.org>
> Reviewed-by: S. Ganesh <ganesh@chromium.org>
> Cr-Commit-Position: refs/heads/master@{#800584}

TBR=ganesh@chromium.org,grt@chromium.org

# Not skipping CQ checks because original CL landed > 1 day ago.

Bug: 516207
Bug: 1100280
Change-Id: I38f6d27904d8f822c949fb07285ae63830ce533a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2374206
Reviewed-by: Greg Thompson <grt@chromium.org>
Commit-Queue: Greg Thompson <grt@chromium.org>
Cr-Commit-Position: refs/heads/master@{#801304}

[modify] https://crrev.com/836a311cccea1d2af5c818886815511364121453/chrome/installer/mini_installer/mini_installer.cc


### ad...@google.com (2020-09-21)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-10-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/ec8aafcbc71f2a78e1a5fac714c0d11a3330c492

commit ec8aafcbc71f2a78e1a5fac714c0d11a3330c492
Author: Greg Thompson <grt@chromium.org>
Date: Fri Oct 30 05:55:16 2020

[mini_installer] Fix reporting of temp dir fallback metrics.

r798844 introduced a metric to report whether or not the work directory
was created in CWD or %TMP%. Sadly, the metric unconditionally reported
that the fallback was never used.

BUG=516207,1100280
R=wfh@chromium.org

Change-Id: I64140cac44dde7baf029e03c31e460a91fa177b3
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2508611
Commit-Queue: Greg Thompson <grt@chromium.org>
Auto-Submit: Greg Thompson <grt@chromium.org>
Reviewed-by: Will Harris <wfh@chromium.org>
Cr-Commit-Position: refs/heads/master@{#822538}

[modify] https://crrev.com/ec8aafcbc71f2a78e1a5fac714c0d11a3330c492/chrome/installer/mini_installer/mini_installer.cc


### gr...@chromium.org (2020-10-30)

Requesting merge of fix in r822538 to M87 4280 branch. It turns out that we were not getting accurate data for the metrics introduced in r798844. I would really like to have data sooner rather than later to make sure that r819537 (already merged to/shipping on 87 and 86) was the right thing. I'm pretty sure it was... If granted approval to merge, I would wait for one canary cycle to verify that all is well.

### [Deleted User] (2020-10-30)

[Empty comment from Monorail migration]

### la...@google.com (2020-10-30)

grt@ - can you confirm on the Canary channel first? I can approve the merge right after.

### [Deleted User] (2020-10-31)

This bug requires manual review: Reverts referenced in bugdroid comments after merge request.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on ToT?
4. Does this change need to be merged into other active release branches (M-1, M+1)?
5. Why are these changes required in this milestone after branch?
6. Is this a new feature?
7. If it is a new feature, is it behind a flag using finch?

Chrome OS Only:
8. Was the change reviewed and approved by the Eng Prod Representative? See Eng Prod ownership by component: http://go/cros-engprodcomponents

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), bindusuvarna @(iOS), cindyb@(ChromeOS), lakpamarthy@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gr...@chromium.org (2020-11-01)

r822538 initially landed in 88.0.4310.0. i don't see anything abnormal in the update success rate for that version or for 88.0.4310.3. i have no reason to believe that this is not safe to merge. thank you for considering it.

### la...@google.com (2020-11-02)

merge approved for M87 branch 4280

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-11-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/200b641a4271b9d2e51a4cc526773c1cd4df029c

commit 200b641a4271b9d2e51a4cc526773c1cd4df029c
Author: Greg Thompson <grt@chromium.org>
Date: Mon Nov 02 08:49:39 2020

[mini_installer] Fix reporting of temp dir fallback metrics.

r798844 introduced a metric to report whether or not the work directory
was created in CWD or %TMP%. Sadly, the metric unconditionally reported
that the fallback was never used.

BUG=516207,1100280
R=​wfh@chromium.org

(cherry picked from commit ec8aafcbc71f2a78e1a5fac714c0d11a3330c492)

Change-Id: I64140cac44dde7baf029e03c31e460a91fa177b3
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2508611
Commit-Queue: Greg Thompson <grt@chromium.org>
Auto-Submit: Greg Thompson <grt@chromium.org>
Reviewed-by: Will Harris <wfh@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#822538}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2513588
Reviewed-by: Greg Thompson <grt@chromium.org>
Cr-Commit-Position: refs/branch-heads/4280@{#1008}
Cr-Branched-From: ea420fb963f9658c9969b6513c56b8f47efa1a2a-refs/heads/master@{#812852}

[modify] https://crrev.com/200b641a4271b9d2e51a4cc526773c1cd4df029c/chrome/installer/mini_installer/mini_installer.cc


### [Deleted User] (2020-11-10)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cr...@appspot.gserviceaccount.com (2020-12-12)

The following revision refers to this bug: 
https://chromium.googlesource.com/chromium/src.git/+/200b641a4271b9d2e51a4cc526773c1cd4df029c

Commit: 200b641a4271b9d2e51a4cc526773c1cd4df029c
Author: grt@chromium.org
Commiter: commit-bot@chromium.org
Date: 2020-11-02 08:49:39 +0000 UTC

[mini_installer] Fix reporting of temp dir fallback metrics.

r798844 introduced a metric to report whether or not the work directory
was created in CWD or %TMP%. Sadly, the metric unconditionally reported
that the fallback was never used.

BUG=516207,1100280
R=​wfh@chromium.org

(cherry picked from commit ec8aafcbc71f2a78e1a5fac714c0d11a3330c492)

Change-Id: I64140cac44dde7baf029e03c31e460a91fa177b3
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2508611
Commit-Queue: Greg Thompson <grt@chromium.org>
Auto-Submit: Greg Thompson <grt@chromium.org>
Reviewed-by: Will Harris <wfh@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#822538}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2513588
Reviewed-by: Greg Thompson <grt@chromium.org>
Cr-Commit-Position: refs/branch-heads/4280@{#1008}
Cr-Branched-From: ea420fb963f9658c9969b6513c56b8f47efa1a2a-refs/heads/master@{#812852}


### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1100280?no_tracker_redirect=1

[Multiple monorail components: Internals>Installer, Security]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40052705)*
