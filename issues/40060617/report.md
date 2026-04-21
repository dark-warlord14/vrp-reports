# Security: .url files can be saved via getFileHandle and redirect showSaveFilePicker to arbitrary file

| Field | Value |
|-------|-------|
| **Issue ID** | [40060617](https://issues.chromium.org/issues/40060617) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Storage>FileSystem |
| **Platforms** | Windows |
| **Reporter** | ha...@gmail.com |
| **Assignee** | as...@chromium.org |
| **Created** | 2022-08-19 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

The fix for <https://bugs.chromium.org/p/chromium/issues/detail?id=1307930> is not extended to getFileHandle(), as a result, getFileHandle() still allows one to save dangerous .url files

**VERSION**  

Chrome Version: 104.0.5112.101 (Official Build) (64-bit) (cohort: 104\_stable\_101\_rampup)  

Operating System: Windows 10 Version 21H2 (Build 19044.1889)

**REPRODUCTION CASE**

1. Follow instructions in filepicker-poc.html and save test.url file
2. Then go to filepicker-poc2.html, this is the same PoC as <https://bugs.chromium.org/p/chromium/issues/detail?id=1307930>, follow the instructions until you reach "Upload file" and upload test.url file
3. The system.ini file is uploaded.

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: Axel Chong

## Attachments

- [filepicker-poc.html](attachments/filepicker-poc.html) (text/plain, 1.5 KB)
- [filepicker-poc2.html](attachments/filepicker-poc2.html) (text/plain, 8.0 KB)
- [filepicker-poc.html](attachments/filepicker-poc.html) (text/plain, 1.8 KB)
- deleted (application/octet-stream, 0 B)
- [example.txt](attachments/example.txt) (text/plain, 132 B)

## Timeline

### ha...@gmail.com (2022-08-19)

This is the affected code: https://chromium.googlesource.com/chromium/src.git/+/refs/tags/104.0.5112.109/content/browser/file_system_access/file_system_access_directory_handle_impl.cc#442

"url" extensions are missing from this code

### [Deleted User] (2022-08-19)

[Empty comment from Monorail migration]

### sr...@google.com (2022-08-19)

Hey haxatron1@, can you check if the filepicker-poc.html is the correct file? It seems that's the same attachment you added in crbug.com/1354505.

### ha...@gmail.com (2022-08-19)

Oops, I accidentally added the wrong file, will attach the correct one when reach home in an hours time.

### [Deleted User] (2022-08-19)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@gmail.com (2022-08-19)

[Comment Deleted]

### ha...@gmail.com (2022-08-19)

Hi attached above is the correct file. Apologies for attaching the wrong one earlier!

### ha...@gmail.com (2022-08-19)

Ughh, this is the correct one 

### sr...@google.com (2022-08-21)

asully@, can you take a look at this? Sounds like a variant of crbug.com/1307930.

Note that I didn't reproduce the issue since I don't have a windows machine available. But the report sounds reasonable as it has a poc and a code pointer.

[Monorail components: Blink>Storage>FileSystem]

### [Deleted User] (2022-08-21)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-21)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-08-21)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### as...@chromium.org (2022-08-22)

This API can interact with the file system in a number of ways:
(1) download a new file (the "Save As" flow)
(2) create a new file in a directory the user has explicitly granted read/write access to (getFileHandle('test.url', { create: true }))  
(3) edit an existing file
(4) read an existing file

The first case is the most restrictive, while we are intentionally less restrictive in the extensions we block when interacting with files in a directory the user has already explicitly granted write access to. For example, we want to warn a user before downloading an .exe file somewhere, but we want to allow a syncing service to sync/edit .exe files already on their machine...

...That being said, for some extensions there is an argument for blocking entirely (which to this point we've only done for .lnk and .scf files). I'm not familiar enough with .url files to know what makes them more/less dangerous than .lnk files... Currently the line is drawn between (1) and (2). It seems tricky to draw the line anywhere else, since editing an existing file seems almost as bad as creating a new one, and it seems odd to allow read-only files which can never be upgraded to writable...

sroettger: I'll defer to you on this one. Is it okay to allow sites to edit .url files? Should we block them everywhere?

### ha...@gmail.com (2022-08-23)

Hi reporter here,

I don't see any reason why ".url" files are blocked in the file picker but not blocked in the file handle. As proven by the previous report https://bugs.chromium.org/p/chromium/issues/detail?id=1307930, ".url" files are dangerous because they can point to other files and when a user uploads a ".url" file, they will unknowingly upload the target file the ".url" will point to, which can contain sensitive information, even if the target file is located outside the folder the user grants getFileHandle() too. 

I don't see how the case of editing a file (3) applies here. If I am not wrong, getFileHandle() does number (2) and as such has the capabilities to create a file with any extension except for the blocked extension list in https://chromium.googlesource.com/chromium/src.git/+/refs/tags/104.0.5112.109/content/browser/file_system_access/file_system_access_directory_handle_impl.cc#442, which is missing the ".url" extension which is what this report is about.

### ha...@gmail.com (2022-09-07)

On further investigation, .url files are essentially shortcuts (ie. they function in the exact same way as .lnk files. Clicking on the example.url file below will launch calc.exe), so I don't see a reason why .lnk files are blocked here while .url files are not.

### ha...@gmail.com (2022-09-07)

On windows change the attached txt file to .url and then click on it, calc will open as a result, showing that it functions the same as a .lnk file. (I cannot upload .url extensions as chrome will automatically upload calc.exe instead of the .url file)

### [Deleted User] (2022-09-07)

asully: Uh oh! This issue still open and hasn't been updated in the last 15 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-09-22)

asully: Uh oh! This issue still open and hasn't been updated in the last 30 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-09-28)

[Empty comment from Monorail migration]

### as...@chromium.org (2022-09-30)

Sorry for the inactivity, I'm catching up after being OOO...

OP: thanks for the detailed examples. While an attack vector here still requires the site to know the path of a dangerous executable on disk, it also seems not very useful for a well-behaving site to create, edit, or sync .url files in the first place. Blocking sites from creating .url files seems reasonable

### gi...@appspot.gserviceaccount.com (2022-10-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/f98adc846aad672bba835f1a1bf5741648f4f5d6

commit f98adc846aad672bba835f1a1bf5741648f4f5d6
Author: Austin Sullivan <asully@chromium.org>
Date: Tue Oct 11 20:53:22 2022

FSA: Block .url files in getFileHandle and getEntries

Fixed: 1354518
Change-Id: I663d4481ccc2047c49d7466bbfe9751e8c140edf
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3945587
Reviewed-by: Marijn Kruisselbrink <mek@chromium.org>
Commit-Queue: Marijn Kruisselbrink <mek@chromium.org>
Auto-Submit: Austin Sullivan <asully@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1057675}

[modify] https://crrev.com/f98adc846aad672bba835f1a1bf5741648f4f5d6/content/browser/file_system_access/file_system_access_directory_handle_impl.cc
[modify] https://crrev.com/f98adc846aad672bba835f1a1bf5741648f4f5d6/content/browser/file_system_access/file_system_access_directory_handle_impl_unittest.cc


### [Deleted User] (2022-10-12)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-12)

[Empty comment from Monorail migration]

### ha...@gmail.com (2022-10-13)

Regarding https://crbug.com/chromium/1354518#c20, theres still the fact that an attacker can trick a user to upload a seemingly benign .url file which points to a file containing credentials and result in data disclosure. (This was demonstrated by the PoC in https://crbug.com/chromium/1354518#c0 and also the reason why .url files were blocked here https://bugs.chromium.org/p/chromium/issues/detail?id=1307930 (showSaveFilePicker variant) and https://bugs.chromium.org/p/chromium/issues/detail?id=1152327)



### as...@chromium.org (2022-10-14)

You are correct that users can still upload .url files (for now, at least), but as of https://crrev.com/c/3945587 these files can no longer be created from the web. This seems reasonably mitigated since
- the .url file must already exist on the user's machine, and
- the user must explicitly choose to upload that file or a parent directory

Is that correct, or is there something I'm misunderstanding here?

### ha...@gmail.com (2022-10-15)

Yes, I tested on Canary and its fixed. Was just elaborating on https://crbug.com/chromium/1354518#c20

### am...@google.com (2022-10-20)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-10-20)

Congratulations, Axel! The VRP Panel has decided to award you $1,000 for this report. Thank you for your efforts in reporting this issue to us! 

### am...@google.com (2022-10-21)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-11-28)

[Empty comment from Monorail migration]

### pg...@google.com (2022-11-29)

[Empty comment from Monorail migration]

### pg...@google.com (2022-11-29)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-18)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1354518?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060617)*
