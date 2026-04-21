# Arbitrary file deletion in google chrome updater in master/chrome/updater/installer.cc

| Field | Value |
|-------|-------|
| **Issue ID** | [40053248](https://issues.chromium.org/issues/40053248) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Installer |
| **Platforms** | Windows |
| **Reporter** | ve...@gmail.com |
| **Assignee** | gr...@chromium.org |
| **Created** | 2020-09-04 |
| **Bounty** | $1,000.00 |

## Description

Arbitrary file deletion in google chrome updater
Platform: Windows
Class: Elevation of Privileges
Security Boundary: Users

Summary:
The google chrome updater perform file deletion in a user write-able location while running as SYSTEM without checking for reparse point allowing arbitrary file deletion for non administrative accounts.

Description:
When chrome updating itself it seem look like there's a procedure to download and execute the chrome updater from the google Google Update Service (gupdate), when the updater is executed he will attempt to look for any folder with the filter C:\Windows\Temp\CR_*.* any folder found will be marked for deletion, I created a file in C:\Windows\Temp\CR_blah.tmp but the chrome updater ignore the file, after taking a look in chromium updater code I found a function in master/chrome/updater/installer.cc line 101, there's a class construction base::FileEnumerator file_enumerator(app_install_dir, false,
                                       base::FileEnumerator::DIRECTORIES);
The syntax of the class constructor is 
FileEnumerator(const FilePath& root_path, bool recursive, int file_type); 
(can be found under master/base/files/file_enumerator.h)
I assume that "int file_type" put a filter on the file enumerator and return the specified type only, that's why files are ignored. By the way anything else than a directory will be ignored even symbolic links, there's still a way to trigger the bug.
In master/base/files/file_util_win.cc there's a function called DeletePathRecursively which is being called by the chrome updater in master/chrome/updater/installer.cc (line 110). The function DeletePathRecursively by itself call another one called DeleteFileAndRecordMetrics which is being called for logs and other stuff that we don't need to care about them, the function which do the actual file deletion is DoDeleteFile and DeleteFileRecursive.
This function call the standard WINAPI at (line 158, 337, 350, 154) without doing any checks against directory junctions which result in arbitrary file deletion.
The filter base::FileEnumerator::DIRECTORIES can be easily bypassed using the james forshaw symbolic link testing tool, abusing oplocks to catch the handle and then set a junction to an arbitrary location.
Now, about the bug. The bug trigger once there's an update available for chrome which the issue is only exploitable on every major chromium release a malicious user or malware could sleep until a major version of chromium is released, to demonstrate the issue I attached an older version of google chrome v84 in order to be able to reproduce the issue.

Steps to reproduce:
1-As an administrator install the attached ChromeStandaloneSetup64.exe
2-Now as a standard user run the poc it will tell you to open chrome and navigate to chrome://settings/help
3-Wait for the update to complete
4-After a few minutes the target file will be deleted.

Few notes: the bug only trigger when chrome is installed as an administrator (by default), however if chrome installed as a user the bug wouldn't trigger (cause the Google Update Service isn't installed). Also the reason why I attached an outdated version of chrome is it's the only way to trigger the issue. And also am just assuming that master/chrome/updater/installer.cc is the vulnerable part of code am not sure, but probably master/base/files/file_util_win.cc is the cause of the vulnerability.

PoC:
I've provided PoC as a c++ project, and a demo video to demonstrate the deletion of the file c:\windows\win.ini as an unprivileged user, which is by default non delete-able from non administrative account.

Tested On: Windows 10 2004, Google Chrome v84.

Fix:
Based on my experience (after finding more than 10 bugs on windows) I created a micro path for master/base/files/file_util_win.cc which add the function DeleteFile_S which actually check if the opened file match the expected file to be opened if it doesn't, the function cancel the file deletion, otherwise the file is deleted.

Note: looks like I can't attach the google chrome standalone installer since the maximum file size 10mb, the standalone package is about ~70mb so here's a download link for the package https://getintopca.com/google-chrome-84-offline-installer-free-download/

## Attachments

- [Demo.mkv](attachments/Demo.mkv) (application/octet-stream, 6.8 MB)
- [ChromeUpdater_LPE.zip](attachments/ChromeUpdater_LPE.zip) (application/octet-stream, 141.7 KB)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- [mini_installer.cc](attachments/mini_installer.cc) (text/plain, 39.6 KB)

## Timeline

### ve...@gmail.com (2020-09-04)

I forget to attach the patched file_util_win.cc, here's it.
Thanks !

### rs...@chromium.org (2020-09-04)

Thanks for the report.

Will: Is this a dupe of https://crbug.com/chromium/1100280?

[Monorail components: Internals>Installer]

### ve...@gmail.com (2020-09-04)

hmmmmm, I guess it's not a duplicate, in https://crbug.com/chromium/1100280 they're talking about a bug that leave the old installation files behind without cleaning them. This one is talking about the cleanup procedure is being done improperly so it result in security bug, I don't think that's a duplicate.
Thanks for the triage !

### so...@chromium.org (2020-09-05)

Can you test your proof of concept with a Chrome build that has the fix for crbug.com/1100280 please?

At a high level, crbug.com/1100280 and this bug seem to have the root cause and effects (C:\Windows\Temp\CR_*.*, junction points, and deleting arbitrary files during Chrome updates).

### ve...@gmail.com (2020-09-05)

I cant access to the https://crbug.com/chromium/1100280, it say access denied it probably has a view restriction. Can you do something about it ?

### so...@chromium.org (2020-09-05)

I can't do anything about you crbug privileges. (wfh@ could) but my suggestion still stands: plz test your proof of concept using a build newer than the latest M84 stable.
 
You said it above: "Also the reason why I attached an outdated version of chrome is it's the only way to trigger the issue.". 
If the vulnerability has been closed in M84+, then it is very likely this crbug is going to  be resolved as a "duplicate" or "won't fix (obsolete).

### ve...@gmail.com (2020-09-05)

Am wondering why the newly downloaded installer is named as the latest version of chrome ? doesn't that mean that the installer is on the latest release ?

### so...@chromium.org (2020-09-06)

What we see in the attached picture is `GoogleUpdate` (the updater) running the installer for Chrome 85.0.4183.83. That version is the latest Chrome version at the moment. The updater is in the process of updating Chrome to its latest stable version.

### ve...@gmail.com (2020-09-06)

Since the installer is on the latest version (as you saw on it's name), this mean that the poc is working on the latest release of google chrome installer, I guess the latest version of chrome installer is vulnerable.

### ve...@gmail.com (2020-09-06)

I am sure now that the latest version of the chrome update is vulnerable.

### ve...@gmail.com (2020-09-06)

Take your time to verify if the exploit is working on the latest version of chrome updater

### so...@chromium.org (2020-09-08)

[Empty comment from Monorail migration]

### wf...@chromium.org (2020-09-08)

grt - can you further triage this?

### gr...@chromium.org (2020-09-14)

ah, i think i see. although we no longer recurse through reparse points, we do attempt to delete them via ::DeleteFileW, which goes through the reparse point rather than deleting it. ugh. i'll send up yet another CL to just leave the junction point alone altogether rather than try to delete it -- since Chrome would never create a junction point, i don't think it should blindly delete one.

thanks for filing this.

### gr...@chromium.org (2020-09-14)

wfh: i imagine we should make base::DeleteFile and base::DeletePathRecursively not delete files/dirs with reparse points by default, and maybe add new functions for the rare case where that is desired. wdyt?

### ga...@chromium.org (2020-09-14)

Re https://crbug.com/chromium/1125018#c15, this is what we implemented in Omaha in cl/324025104, would be interested to hear counter-points if any.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-09-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/57c8233813e518519beadd7816331f32f86915af

commit 57c8233813e518519beadd7816331f32f86915af
Author: Greg Thompson <grt@chromium.org>
Date: Mon Sep 14 19:15:05 2020

[mini_installer] Leave files with reparse points alone when deleting.

mini_installer recursively deletes directories left behind from previous
runs. As it recurses through them, it may delete files with reparse
points in those dirs. This is bad, since such files may actually be
maliciously-created links to other entities on the filesystem. This CL
skips anything with a reparse point during deletion -- since Chrome
never creates files/dirs with reparse points, it shouldn't try to delete
them.

BUG=1125018
R=wfh@chromium.org

Change-Id: I9897947ed883a91758c31990ed0b9648c38d2942
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2409698
Auto-Submit: Greg Thompson <grt@chromium.org>
Commit-Queue: Will Harris <wfh@chromium.org>
Reviewed-by: Will Harris <wfh@chromium.org>
Cr-Commit-Position: refs/heads/master@{#806715}

[modify] https://crrev.com/57c8233813e518519beadd7816331f32f86915af/chrome/installer/mini_installer/mini_installer.cc


### ve...@gmail.com (2020-09-14)

[Comment Deleted]

### ve...@gmail.com (2020-09-14)

[Comment Deleted]

### ad...@google.com (2020-09-15)

grt@ is https://crbug.com/chromium/1125018#c17 a complete fix? If so, please would you mark this as Fixed such that Sheriffbot initiates merge procedures? As a high severity bug impacting stable, we'd normally merge this back to M86 and M85 if you're confident of the fix. We'll be cutting a new M85 security refresh towards the end of this week.

The fix looks sane to me and looks like the sort of thing we'd want to merge, unless you've got any remote concerns that sometimes we actually might legitimately need to deal with reparse points in any conceivable situation.

### gr...@chromium.org (2020-09-16)

[Empty comment from Monorail migration]

### gr...@chromium.org (2020-09-16)

Yes, I believe it's a complete fix. I think a merge is safe and a good idea.

### ve...@gmail.com (2020-09-16)

[Comment Deleted]

### ve...@gmail.com (2020-09-16)

The patch doesn't seems to be enough for me. Did you read the poc ?

### gr...@chromium.org (2020-09-16)

Requesting merges. They're tee'd up at:

- M86: https://chromium-review.googlesource.com/c/chromium/src/+/2412336
  and:
- M85: https://chromium-review.googlesource.com/c/chromium/src/+/2413488

Please take the liberty of sending them to the CQ if you'd like.

### [Deleted User] (2020-09-16)

This bug requires manual review: M86's targeted beta branch promotion date has already passed, so this requires manual review
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
Owners: govind@(Android), bindusuvarna@(iOS), geohsu@(ChromeOS),  pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gr...@chromium.org (2020-09-16)

ve23: could you clarify what you think is lacking? thanks.

### gr...@chromium.org (2020-09-16)

(note that chrome/updater/installer.cc is not used in the case that you have reported.)

### ve...@gmail.com (2020-09-16)

grt: The security patch you did can be considered as a bug fix not security patch, if you tested the poc that I've provided on it will still work and it will delete an arbitrary file. Actually there's a bug in the old code of how the mini installer is behaving with reparse point 
https://chromium-review.googlesource.com/c/chromium/src/+/2412336/1/chrome/installer/mini_installer/mini_installer.cc#760
in line 771:
if ((find_data.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY) &&
          !(find_data.dwFileAttributes & FILE_ATTRIBUTE_REPARSE_POINT)) <- useless check and can be still fooled {
        RecursivelyDeleteDirectory(path);<- the bug exist within the function itself
      } else {
        ::DeleteFile(path->get());<- it's a bug not security vulnerability
      }
the mini installer will check if it a directory if it, it will be deleted with RecursivelyDeleteDirectory(path); otherwise if it's a file or symlink it will be deleted with DeleteFile function which will return ACCESS_DENIED if it's a reparse point. The bug patch by (grt) was just fixing the DeleteFile bug and now it will ignore reparse points. Anyway you did a simple condition to check if the search result is a reparse point and it will be ignored if it's a reparse point, btw that's not enough to prevent arbitrary file deletion cause of a race condition. If we created a reparse point after the check in line 760 (the patched one) we will achieve arbitrary file deletion. It's not needed to race with the mini installer, since we can use oplocks. The oplock will freeze any DeleteFile call and will switch reparse point you can refer to my poc (exploit.cpp)
FileOpLock* lk = FileOpLock::CreateLock(hFile, cb);
lk->WaitForLock(INFINITE);
so as soon the deletefile function is being called in mini updater the poc will freeze the delete operation and execute the callback function "void cb()" which will remove the file from the directory and switch a reparse point to an arbitrary location and will result in arbitrary file delete. So a simple check such as GetFileAttributes and 
if (find_data.dwFileAttributes & FILE_ATTRIBUTE_REPARSE_POINT) wouldn't work.
The best way to fix those bugs is to impersonate the user or check if the expected file is opened by calling GetFinalPathNameByHandleW and simply check if anything is wrong. Btw I always wanted to contribute in chromium project where I can submit the patch ?


### gr...@chromium.org (2020-09-16)

thanks for the very cool rundown. now i see what you mean. i've read about oplocks in the past, but don't (yet) have any direct experience with them.

a contribution would be welcome. you can follow through instructions for how to contribute starting here: https://chromium.googlesource.com/chromium/src/+/master/docs/contributing.md

### ve...@gmail.com (2020-09-17)

I am working on it, Thanks.

### sr...@google.com (2020-09-17)

adetaylor@ are you going to approve the merge for M85 for this one?

### ve...@gmail.com (2020-09-17)

I created a mini patched function of DeleteFile and RemoveDirectory which will check if the expected file or directory is opened, if it match it will be deleted otherwise it will left behind.
grt: I really had a bad time trying to make a contribute to chromium project (really my internet speed suck, it take more than 5 min to render this page), can you do it for me, and can you add me in the CC or something.
Thanks.


### ve...@gmail.com (2020-09-17)

[Empty comment from Monorail migration]

### ad...@google.com (2020-09-17)

Re https://crbug.com/chromium/1125018#c32 nope! Looks like more work is needed for now.

### ve...@gmail.com (2020-09-18)

[Comment Deleted]

### gr...@chromium.org (2020-09-22)

ve23: thanks for the file. i'll take a look.

### ad...@google.com (2020-09-22)

I'm going to remove the merge requests here until this is definitely fully fixed.

### gr...@chromium.org (2020-09-23)

i've thrown together two possibilities:
- https://chromium-review.googlesource.com/c/chromium/src/+/2425052: this one leaves files/dirs behind if they have reparse points. i think this is the way to go.
- https://chromium-review.googlesource.com/c/chromium/src/+/2425052: this one deletes files/dirs that have reparse points. i don't think we should do this, but i went through the motions anyway to be sure i understood your proposal.

regarding your proposal: could you explain why it's necessary to use GetFinalPathNameByHandle? is there a case where FILE_FLAG_OPEN_REPARSE_POINT does not suppress processing a potential reparse point? my understanding was that opening with FILE_FLAG_OPEN_REPARSE_POINT and then deleting through the handle via SetFileInformationByHandle is sufficient to be sure that only the desired item is being deleted.

thanks.

### ve...@gmail.com (2020-09-23)

grt: The patch is really useless and the poc I've attached before will still work perfectly (you can test it by yourself)
The following scenario will explain how GetFinalPathNameByHandle will fix the issue
The poc will create C:\Windows\Temp\CR_test and C:\Windows\Temp\CR_test\pci.sys (no link were created), and then lock the pci.sys file with oplock
The mini installer will calls the QueryDirectory API's to query subcontent, and for each file there's a check if it's a reparse point it will be ignored.
The mini installer will try to delete the pci.sys with your DeletePathNoFollow function, the CreateFile call inside DeletePathNoFollow will trigger the oplock created before
The poc will move the file to a temporary location with the same handle used to create the oplock so it wouldn't block itself, and the a reparse point will be created from c:\windows\temp\CR_test -> c:\windows\system32\drivers and then the oplock will be released.
The mini installer will open c:\windows\system32\drivers\pci.sys instead of c:\windows\temp\CR_test\pci.sys.
You will probably say what about the check https://chromium-review.googlesource.com/c/chromium/src/+/2425052/1/chrome/installer/mini_installer/delete_file.cc (line 33), its useless cause you are opening an actual file not a reparse point this can only work if you are opening a reparse point (such as c:\windows\temp\CR_test).
But if you implemented GetFinalPathNameByHandle even if a reparse occurred you will check if the expected file is opened in our case the expected file isn't opened cause we opened c:\windows\system32\drivers\pci.sys instead of c:\windows\temp\CR_test\pci.sys so you will close your handle and return ACCESS_DENIED.
Anyway SetFileInformationByHandle is enough to make sure that the only desired item is being deleted since you are not opening any new handle.
I am not the only guy who use this function to prevent reparse point attack, Microsoft, Bitdefender, Kaspersky by Themselves use GetFinalPathNameByHandle so they can delete files securely, you can see that everywhere in WER (Windows Error Reporting Tool).
And before I forget the FILE_FLAG_OPEN_REPARSE_POINT isn't sufficient to prevent reparse point, by the it's used in DeleteFile and RemoveDirectory to create a handle sooo anyway... 
Also james forshaw reviewed my submission am so happy with that, I am a huge fan :)

### gr...@chromium.org (2020-09-23)

aaah, so the magic is that you're using a reparse point somewhere along the path to the file being operated on, not on the file itself. snazzy. my apologies for not looking at your poc sooner.

it sounds like https://crrev.com/c/2424162 is the way to go. i'm wondering if GetFinalPathNameByHandle could bite us, though. we use GetTempPath, which could conceivably return a path string that doesn't round-trip through GetFinalPathNameByHandle with no modifications. should we open a handle to that directory, call GetFinalPathNameByHandle on it, and use that as the basis for all other path manipulation? hmm.

i'll work on some tests in the meantime.

this is fun. :-)

### fo...@chromium.org (2020-09-23)

Yes, you can't just check the end file to see if it's a reparse point. About the only way to go at the moment is to use GetFinalPathNameByHandle to check the end result and back out if it doesn't match what you expected. In theory temp could be over a reparse point as well, especially if the code every runs as a user.

But this comes back to the last issue we had, perhaps we just shouldn't be dropping files to an untrusted location like the temporary path in the first place. That would solve the issues of file planting/symlink attacks.

### gr...@chromium.org (2020-09-23)

we shouldn't be putting new files in %TMP% any longer, except as a fallback. i'm hoping for some metrics to tell me that the new location is working reliably and that the fallback isn't being used before deleting the old code. so, another approach is to do nothing right now, wait a bit for the datas (Oct, i suspect), then delete this recursive delete in %TMP%. wdyt?

### fo...@chromium.org (2020-09-23)

If we're currently using the somewhere other than %TMP% as the primary location, is this bug exploiting a pre-patch installer? Or is it activating the fallback process? Based on the comment "Also the reason why I attached an outdated version of chrome is it's the only way to trigger the issue" does that means it's currently _sort of_ patched already?

### gr...@chromium.org (2020-09-23)

as of Chrome 86.0.4237.0, we first try to expand things into the directory holding the mini_installer. this is ordinarily a directory created by Google Update somewhere within %ProgramFiles(x86)%\Google\Update. we use %TMP% as a fallback in case we fail to get the exe's dir or fail to create a directory within that dir. i suspect (but can't prove) that we ~never use the fallback in production. these are the metrics i'm waiting for.

the deletion code in question, though, is something that runs before all of that. we long ago had reason to believe that disk full was a major reason for install/update failure. to mitigate this, we added code to delete anything left behind by previous runs of the installer. i am comfortable removing that deletion if we are okay removing the %TMP% fallback, since i hear from the Google Update team that GU will delete the dir into which it drops Chrome's installer at some point in the future (e.g., when the next installer runs, perhaps). if we can rely on that to clean up our messes, then let's ditch this "recursive delete in a user-writable dir" code.

### fo...@chromium.org (2020-09-23)

Okay so basically in the same area from last time, the cleanup run even if it doesn't use that directory for installation. The best security fix is one which removes the code so if we can do that it'd be preferable rather than trying to work around filesystem weirdness.

### ve...@gmail.com (2020-09-24)

grt: that should work for you https://crrev.com/c/2424162
forshaw: I agree, that's the best way to deal with those bugs, it's to make sure you're deleting files in a user non write-able location.

### gr...@chromium.org (2020-09-30)

a new version of Google Update that reports whether the fallback temp dir is used is starting to roll out now. with luck, i'll soon have data to support removal of the old code.

### [Deleted User] (2020-10-07)

[Empty comment from Monorail migration]

### gr...@chromium.org (2020-10-16)

it looks like the fallback to %TMP% was not used for any of the installs or updates in the past seven days. i think this means we're clear to pull the code with one caveat:

https://crbug.com/chromium/1138157 got me thinking that getting rid of the fallback means that installation will fail with no indication of why if someone were to grab a mini_installer and try to run it from a read-only directory. should we care? all installs of Google Chrome should be done by way of Google Update, so it will only be an issue for developers or others who expect to somehow grab a mini_installer and run it.

we could leave the fallback to %TMP% in-place and simply remove the problematic "clean up from previous attempts" code. i'm okay with this since all true official Google Chrome installs should be protected from filling up disks thanks to Google Update.

thoughts?

### fo...@chromium.org (2020-10-16)

Yeah it might make sense to leave the fallback if there's no other choice but don't do any cleanup as very few if any installations should ever take the temp route and there should be little to cleanup (and even then it was presumably only an issue if the installer crashed?)

### wf...@chromium.org (2020-10-19)

how far up channels has the code referenced in #50 reached? Is it in Stable yet?

### gr...@chromium.org (2020-10-20)

Yes; 86.0.4237.0 has the "stop using %TMP%" CL.

The "stop cleaning old junk in %TMP%" CL is waiting for an LGTM here: https://chromium-review.googlesource.com/c/chromium/src/+/2484651

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-10-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/96b03812b037c11eaa4d85c5b178ee663116fa00

commit 96b03812b037c11eaa4d85c5b178ee663116fa00
Author: Greg Thompson <grt@chromium.org>
Date: Wed Oct 21 22:01:38 2020

[mini_installer] Remove code to delete files left behind by previous runs.

Once upon a time, mini_installer.exe created a directory in %TMP% in
which to place files while it performed its work. Since it may fail to
delete these files (e.g., due to crashes or interference by A/V
software), it was given the power to delete files left behind by
previous executions. This is all well and good, except that organic
system-level installs did this work in a user's %TMP% directory rather
than in the system's. Starting in r798844, mini_installer now puts its
work directory next to itself. For installs driven by Google Update, GU
will take care of (eventually) deleting anything left behind. Since this
appears to be working reliably, we no longer need the %TMP% cleanup
code.

One caveat to this change is that files/dirs may once again accumulate
in %TMP% if mini_installer is run from a directory in which it does not
have write access. This will never be the case for proper Google Chrome
installs.

BUG=1125018
R=forshaw@chromium.org

Change-Id: I50a768585d25ebdd508fc88f8036580a01bd8727
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2484651
Reviewed-by: James Forshaw <forshaw@chromium.org>
Commit-Queue: Greg Thompson <grt@chromium.org>
Cr-Commit-Position: refs/heads/master@{#819537}

[modify] https://crrev.com/96b03812b037c11eaa4d85c5b178ee663116fa00/chrome/installer/mini_installer/mini_installer.cc


### gr...@chromium.org (2020-10-22)

r819537 initially landed in 88.0.4300.0. The merge is safe since this is purely deletion of code that runs before installation of Chrome.

### ad...@chromium.org (2020-10-22)

OK. "The merge is safe" - just to confirm, you'd be comfortable with merging this back to the next M86 security refresh? (Sheriffbot will start to add merge requests tomorrow)

### [Deleted User] (2020-10-22)

[Empty comment from Monorail migration]

### gr...@chromium.org (2020-10-23)

I am comfortable. I'm trying to stretch my mind to see how this could backfire, and I'm coming up dry.

### ad...@chromium.org (2020-10-23)

OK, let's do that then. Approving merge to M87, branch 4280, and M86, branch 4240. (Sheriffbot didn't add the merge requests because it got confused that there had previously been merge requests here).

Please could you wait for a day of Canary coverage before merging.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-10-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/90f05460497157dfbcbb45364898b2827dceb24c

commit 90f05460497157dfbcbb45364898b2827dceb24c
Author: Greg Thompson <grt@chromium.org>
Date: Mon Oct 26 09:07:11 2020

[mini_installer] Remove code to delete files left behind by previous runs.

Once upon a time, mini_installer.exe created a directory in %TMP% in
which to place files while it performed its work. Since it may fail to
delete these files (e.g., due to crashes or interference by A/V
software), it was given the power to delete files left behind by
previous executions. This is all well and good, except that organic
system-level installs did this work in a user's %TMP% directory rather
than in the system's. Starting in r798844, mini_installer now puts its
work directory next to itself. For installs driven by Google Update, GU
will take care of (eventually) deleting anything left behind. Since this
appears to be working reliably, we no longer need the %TMP% cleanup
code.

One caveat to this change is that files/dirs may once again accumulate
in %TMP% if mini_installer is run from a directory in which it does not
have write access. This will never be the case for proper Google Chrome
installs.

BUG=1125018
R=​forshaw@chromium.org

(cherry picked from commit 96b03812b037c11eaa4d85c5b178ee663116fa00)

Change-Id: I50a768585d25ebdd508fc88f8036580a01bd8727
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2484651
Reviewed-by: James Forshaw <forshaw@chromium.org>
Commit-Queue: Greg Thompson <grt@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#819537}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2497167
Reviewed-by: Greg Thompson <grt@chromium.org>
Cr-Commit-Position: refs/branch-heads/4280@{#753}
Cr-Branched-From: ea420fb963f9658c9969b6513c56b8f47efa1a2a-refs/heads/master@{#812852}

[modify] https://crrev.com/90f05460497157dfbcbb45364898b2827dceb24c/chrome/installer/mini_installer/mini_installer.cc


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-10-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/0d4263f222c95dd599cf7ee3b258a0b6dccf6eb0

commit 0d4263f222c95dd599cf7ee3b258a0b6dccf6eb0
Author: Greg Thompson <grt@chromium.org>
Date: Mon Oct 26 09:24:04 2020

[mini_installer] Remove code to delete files left behind by previous runs.

Once upon a time, mini_installer.exe created a directory in %TMP% in
which to place files while it performed its work. Since it may fail to
delete these files (e.g., due to crashes or interference by A/V
software), it was given the power to delete files left behind by
previous executions. This is all well and good, except that organic
system-level installs did this work in a user's %TMP% directory rather
than in the system's. Starting in r798844, mini_installer now puts its
work directory next to itself. For installs driven by Google Update, GU
will take care of (eventually) deleting anything left behind. Since this
appears to be working reliably, we no longer need the %TMP% cleanup
code.

One caveat to this change is that files/dirs may once again accumulate
in %TMP% if mini_installer is run from a directory in which it does not
have write access. This will never be the case for proper Google Chrome
installs.

BUG=1125018
R=forshaw@chromium.org

(cherry picked from commit 96b03812b037c11eaa4d85c5b178ee663116fa00)

Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2484651
Reviewed-by: James Forshaw <forshaw@chromium.org>
Commit-Queue: Greg Thompson <grt@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#819537}
Change-Id: Ia12dff9f7bff79ececd598ba7af8bae43df8c709
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2497443
Reviewed-by: Greg Thompson <grt@chromium.org>
Cr-Commit-Position: refs/branch-heads/4240@{#1329}
Cr-Branched-From: f297677702651916bbf65e59c0d4bbd4ce57d1ee-refs/heads/master@{#800218}

[modify] https://crrev.com/0d4263f222c95dd599cf7ee3b258a0b6dccf6eb0/chrome/installer/mini_installer/mini_installer.cc


### gr...@chromium.org (2020-10-26)

Canary looked good; merges complete.

### ad...@google.com (2020-10-26)

[Empty comment from Monorail migration]

### ad...@google.com (2020-10-28)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-10-28)

Congratulations, the VRP panel has decided to award $1000 for this report ($500 for the original report and another $500 for the extra problems you spotted during the discussion). Someone from our finance team will get in touch with you. How would you like to be credited in the Chrome release notes?

### ve...@gmail.com (2020-10-28)

Hi, Thanks for the reward. Please acknowledge me with the following alias "Abdelhamid Naceri (halov)" and thank you again !

### ad...@chromium.org (2020-10-28)

Will do. Thank you!

### ad...@google.com (2020-10-29)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-10-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/ec19a7645cbb4709b5e35e5c3c77d328afa55848

commit ec19a7645cbb4709b5e35e5c3c77d328afa55848
Author: Greg Thompson <grt@chromium.org>
Date: Fri Oct 30 17:57:17 2020

[mini_installer] Remove code to delete files left behind by previous runs.

Once upon a time, mini_installer.exe created a directory in %TMP% in
which to place files while it performed its work. Since it may fail to
delete these files (e.g., due to crashes or interference by A/V
software), it was given the power to delete files left behind by
previous executions. This is all well and good, except that organic
system-level installs did this work in a user's %TMP% directory rather
than in the system's. Starting in r798844, mini_installer now puts its
work directory next to itself. For installs driven by Google Update, GU
will take care of (eventually) deleting anything left behind. Since this
appears to be working reliably, we no longer need the %TMP% cleanup
code.

One caveat to this change is that files/dirs may once again accumulate
in %TMP% if mini_installer is run from a directory in which it does not
have write access. This will never be the case for proper Google Chrome
installs.

BUG=1125018
R=​forshaw@chromium.org

(cherry picked from commit 96b03812b037c11eaa4d85c5b178ee663116fa00)

(cherry picked from commit 0d4263f222c95dd599cf7ee3b258a0b6dccf6eb0)

Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2484651
Reviewed-by: James Forshaw <forshaw@chromium.org>
Commit-Queue: Greg Thompson <grt@chromium.org>
Cr-Original-Original-Commit-Position: refs/heads/master@{#819537}
Change-Id: Ia12dff9f7bff79ececd598ba7af8bae43df8c709
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2497443
Reviewed-by: Greg Thompson <grt@chromium.org>
Cr-Original-Commit-Position: refs/branch-heads/4240@{#1329}
Cr-Original-Branched-From: f297677702651916bbf65e59c0d4bbd4ce57d1ee-refs/heads/master@{#800218}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2509369
Commit-Queue: Achuith Bhandarkar <achuith@chromium.org>
Cr-Commit-Position: refs/branch-heads/4240_112@{#7}
Cr-Branched-From: 427c00d3874b6abcf4c4c2719768835fc3ef26d6-refs/branch-heads/4240@{#1291}
Cr-Branched-From: f297677702651916bbf65e59c0d4bbd4ce57d1ee-refs/heads/master@{#800218}

[modify] https://crrev.com/ec19a7645cbb4709b5e35e5c3c77d328afa55848/chrome/installer/mini_installer/mini_installer.cc


### ad...@google.com (2020-10-30)

[Empty comment from Monorail migration]

### ad...@google.com (2020-10-30)

[Empty comment from Monorail migration]

### ad...@google.com (2020-11-03)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-28)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1125018?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40053248)*
