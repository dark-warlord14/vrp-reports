# Security: Incomplete fix for CVE-2021-30577

| Field | Value |
|-------|-------|
| **Issue ID** | [40057132](https://issues.chromium.org/issues/40057132) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Updater |
| **Platforms** | Windows |
| **CVE IDs** | CVE-2021-30577 |
| **Reporter** | ve...@gmail.com |
| **Assignee** | ga...@chromium.org |
| **Created** | 2021-09-02 |
| **Bounty** | $10,000.00 |

## Description

**VULNERABILITY DETAILS**

CVE-2021-30577 had an incomplete fix.  

And please note that CVE-2021-30577 has been publicly disclosed before (here - <https://github.com/klinix5/GoogleUpdateSvcLPE>), I privately reported the bug (see #1183137 for details) but you didn't show any interests to fix it.  

Quick background about the C:\ permission  

By default C:\ isn't permissive enough to allow "NT AUTHORITY\Authenticated Users" to have FILE\_WRITE\_DATA on C:\  

However, I spotted in windows 10 2009 x64 Pro (also known as 20H2) that Authenticated Users had more permission on C:\ , this behaviour wasn't observed in older or newer versions of windows. (at least for me, there's reports that some newer windows versions had the same behaviour)  

And to make things more mysterious, the permissive C:\ didn't exist in all windows 10 2009 ISOs but only in few ones.

This behaviour was definitely OK as long as no one does something wrong in C:\ .  

But you did, Google Update service put a debug file in C:\GoogleUpdate.ini which will technically allow anyone with access to that file to specify where the log file is created.  

In #1204811, a user will no longer be able to specify the location of the log file and for now, it forcibly uses C:\ProgramData\Google\Update\Log as a working directory.  

This sounds secure, but the permissive DACL on the directories and the newly created file has a tiny flaw.  

The newly created directories inherit the DACL from c:\programdata which means that Users will have GENERIC\_WRITE access on the newly created directories.  

The newly created file is permissive enough to allow a user to delete it, this is mentioned here <https://github.com/google/omaha/blob/master/omaha/base/logging.cc#L1115>

We're more interested in delete permission because that is what we need to clear the directory from existing files.  

For now, the directory is empty. We can freely create and remove mount points.

Now to the actual vulnerability.

[The first bug]  

After calling CreateFileW, there's a check for mount point in  

<https://github.com/google/omaha/blob/master/omaha/base/logging.cc#L1105>  

Technically, you're too late for a security check.  

First of all, a user can specify AppendToFile=0 so dwCreationDisposition will be CREATE\_ALWAYS. This is sufficient for a user to overwrite existing files.  

Besides, a user can place an oplock to the file before the service attempts to open it in <https://github.com/google/omaha/blob/master/omaha/base/logging.cc#L1075> so we can predict when CreateFileW is called by the service.  

As I mentioned before, it's too late for a security check.  

There's a race condition between  

<https://github.com/google/omaha/blob/master/omaha/base/logging.cc#L1075>  

and  

<https://github.com/google/omaha/blob/master/omaha/base/logging.cc#L1105>  

If we removed the mount point using FSCTL\_DELETE\_MOUNT\_POINT before the check, then the service will process to write a security descriptor which allow a user to take over arbitrary files.  

The bug exploited in the following steps:

1. Create %ALLUSERSPROFILE%\Google\Update\Log\GoogleUpdate.log and place and place an oplock on it.
2. Start the service or wait for the scheduled task to start.
3. The OpLock will trigger, the oplocked file must be moved to a temporary location
4. Create a mount point from %ALLUSERSPROFILE%\Google\Update\Log -> \BaseNamedObjects\Restricted
5. Create an object manager symbolic link \BaseNamedObjects\Restricted\GoogleUpdate.log -> ??\C:<Any\_File>
6. Release the initial oplock
7. The service will be redirected to an arbitrary file.
8. Before the service call IsReparsePoint we should remove the mount point using FSCTL\_DELETE\_MOUNT\_POINT control code.
9. Now that we tricked the service that the parent isn't a mount point. We can recreate the junction, so arbitrary permissions will be written to any file from our choose.

[The second bug]  

Let's not get deep in FileLogWriter::CreateLoggingFile this time, you can notice in the beginning of the function that there's a check for file size. If the file size exceed the expected then it will archived.  

GoogleUpdate.ini allow us to specify the maximum file size using MaxLogFileSize=X, there seems to be no checks restricting the size of the file. So if we set a zero, it would be accepted. (Consider fixing that)  

Looking at FileLogWriter::ArchiveLoggingFile there seems to be no bother to check for mount points and it directly call File::Move in <https://github.com/google/omaha/blob/master/omaha/base/logging.cc#L1154>  

This can be easily abused by a user, if the correct symbolic links were created. Then a user will abuse this functionality for arbitrary file creation, move and deletion.

**VERSION**  

Chrome Version: 93.0.4577.63 Stable  

Google Installer Version: 1.3.36.81  

Operating System: Windows 10 2009 x64

**REPRODUCTION CASE**  

I'll provide a PoC soon.

**CREDIT INFORMATION**  

Reporter credit: Abdelhamid Naceri

## Attachments

- [ChromeUpdaterLPE.zip](attachments/ChromeUpdaterLPE.zip) (application/octet-stream, 236.7 KB)

## Timeline

### ve...@gmail.com (2021-09-02)

To whoever will see this first, please cc sorin and waffles. They are responsible for handling omaha.

### ve...@gmail.com (2021-09-02)

Side note, consider adding forshaw to this thread. He's the expert who will help to fix this correctly.

### [Deleted User] (2021-09-02)

[Empty comment from Monorail migration]

### ve...@gmail.com (2021-09-02)

I'll include my suggestion for a fix just in case.

Not really sure why you have chosen C:\GoogleUpdate.ini as a config file, you can definitely move it somewhere else. However, considering that it's something hard to do. We'll be applying work arounds to mitigate this issue.

[First bug]
Here - https://github.com/google/omaha/blob/master/omaha/base/logging.cc#L1079
* You should either specify OPEN_EXISTING or CREATE_NEW, otherwise a user can break boundaries.
* A check must be done using GetFileAttributes, specify CREATE_NEW if the file didn't exist. Otherwise, open it with OPEN_EXISTING.
* You should apply a lock on both, the parent directory and the file with FILE_SHARE_READ.
* After locking them, consider adding a check to verify the trust of the handles using GetFinalPathNameByHandle. This will ensure that you locked everything correctly.
* Now you can proceed to do whatever what you'd like to do safely.

For the second bug, it's a bit complicated. Might take more time for me to figure out a working solution.



### ad...@google.com (2021-09-02)

[Empty comment from Monorail migration]

### ad...@google.com (2021-09-02)

[Empty comment from Monorail migration]

### so...@chromium.org (2021-09-02)

[Empty comment from Monorail migration]

### ga...@chromium.org (2021-09-02)

[Empty comment from Monorail migration]

[Monorail components: Internals>Updater]

### ve...@gmail.com (2021-09-02)

I included a simple PoC for this, it should spawn a SYSTEM shell if it succeed.
The PoC must be executed in Windows 10 2009 x64 to succeed.

### ga...@chromium.org (2021-09-03)

Thank you very much halov. We will be shipping out a fix by the end of September.

Here is a description of what we are changing:

Description

Fix crbug/1245879: Security: Incomplete fix for CVE-2021-30577

Logging to files has been a continuing security issue for us. For that
reason, I am turning off logging to file. Omaha will continue to log to
the debugger via ::OutputDebugString.

Logging to file is still possible by setting an UpdateDev REG_DWORD
value "IsEnabledLogToFile". Setting "IsEnabledLogToFile" to 1 will
enable logging to %ALLUSERSPROFILE%\Google\Update\Log\GoogleUpdate.log.


### [Deleted User] (2021-09-04)

[Empty comment from Monorail migration]

### ad...@google.com (2021-09-07)

From https://crbug.com/chromium/1245879#c10 it sounds like this is confirmed as being a real bug, so applying labels suitably.

ganesh@ - if that fix has landed, please could you mark this as Fixed?

I understand that GoogleUpdate is dhsipped independently of Chrome releases, right? I'm marking it as Release-0-M94 so that we don't overlook it from a release notes point of view - Amy, you may decide to do something different, but hopefully this means it'll end up somewhere :)

### [Deleted User] (2021-09-07)

[Empty comment from Monorail migration]

### ga...@chromium.org (2021-09-07)

[Empty comment from Monorail migration]

### as...@google.com (2021-09-08)

Marking as NA for M90 LTS as Windows-only issue (same as original https://crbug.com/1204811).

### as...@google.com (2021-09-08)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-08)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-08)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-09-08)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-08)

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M94. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-09-08)

This bug requires manual review: We are only 12 days from stable.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/main/docs/process/merge_request.md#when-to-request-a-merge
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
Owners: govind@(Android), harrysouders@(iOS), matthewjoseph@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sr...@google.com (2021-09-08)

pls answer https://crbug.com/chromium/1245879#c21 for merge review. 

### wa...@chromium.org (2021-09-08)

No merge needed, as this releases independently of Chrome.

(Caveat: standalone installers bundle a version of Omaha so there is some coupling, but no change to the Chromium src tree is needed.)

### wa...@chromium.org (2021-09-20)

We will begin releasing a fixed (as per https://crbug.com/chromium/1245879#c10) GoogleUpdate this week.

### am...@google.com (2021-09-21)

[Empty comment from Monorail migration]

### am...@google.com (2021-10-08)

[Empty comment from Monorail migration]

### am...@google.com (2021-10-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-10-13)

Congratulations, Abdelhamid! The VRP Panel has decided to award you $10,000 for this report. Thank you for your thorough analysis of this issue from you first report to this one and helping us get it fully resolved! 

### ve...@gmail.com (2021-10-14)

Thank you !

### am...@google.com (2021-10-14)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-16)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1245879?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057132)*
