# Security: .url files can redirect showSaveFilePicker into an arbitrary file

| Field | Value |
|-------|-------|
| **Issue ID** | [40059141](https://issues.chromium.org/issues/40059141) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Storage>FileSystem |
| **Platforms** | Windows |
| **Reporter** | ve...@gmail.com |
| **Assignee** | as...@chromium.org |
| **Created** | 2022-03-18 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**

This is based on #1152327

An attacker needs to convince the user to save and upload the saved file, this will result in opening an arbitrary file. The fix was fairly easy, you just blocked saving .lnk files which was enough to mitigate the issue.  

However, there's also .url files which acts almostly as same as .lnk files. Windows file picker behaviour follows any .url to its target which can be abused maliciously to read arbitrary files.

A good fix should blacklist .url files.

**VERSION**  

Chrome Version: 99.0.4844.74 stable  

Operating System: Windows 11

**REPRODUCTION CASE**

open PoC.html and save the given file and try to upload the saved file, it should upload c:\windows\system.ini instead.

**CREDIT INFORMATION**  

Reporter credit: Abdelhamid Naceri

## Attachments

- [PoC.html](attachments/PoC.html) (text/plain, 8.0 KB)

## Timeline

### ma...@chromium.org (2022-03-19)

Confirmed the poc in m98 and m99. Setting foundin-98.
Setting severity-high, component, assignee, cc based on https://crbug.com/chromium/1152327.

[Monorail components: Blink>Storage>FileSystem]

### [Deleted User] (2022-03-19)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-03-21)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-21)

[Empty comment from Monorail migration]

### ad...@google.com (2022-03-28)

schenney says:
> Next week I'll look into what it would take, and start trying things out. My plan is to write something up so that someone else can fix it even if I don't get to it.

### [Deleted User] (2022-03-30)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-02)

mek: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### me...@chromium.org (2022-04-06)

[Empty comment from Monorail migration]

### as...@chromium.org (2022-04-06)

[Empty comment from Monorail migration]

### as...@chromium.org (2022-04-15)

This bug was discussed on the following doc [1], where it was decided that we'll add an extra prompt when a user attempts to save a file with a dangerous extension.

That being said, an argument could be made that we should block .url files wholesale, like we do for .lnk files. 

Looking at the downloads code doesn't seem to be of much help here (never mind that we already diverge on blocking/sanitization behavior - see https://crbug.com/chromium/1154757). Curiously, it looks like .url files are DANGEROUS [2] and .lnk files are a lower danger level (ALLOW_ON_USER_GESTURE), while filename sanitization follows a different set of rules entirely [3], blocking only .lnk and .local files only on Windows... 

[1] http://docs/document/d/1WMh6iw_r_4mBN2iJfDkr1Aevichyr472kDbPKl80K00?resourcekey=0-UWSDns1SzeN3eHy0u5WWZA 
[2] https://crsrc.org/c/components/safe_browsing/content/resources/download_file_types.asciipb;l=1730
[3] https://crsrc.org/c/net/base/filename_util_internal.cc;l=187

### as...@chromium.org (2022-04-18)

[Empty comment from Monorail migration]

### do...@chromium.org (2022-04-28)

Sheriff ping: is there some progress towards a fix here? This security bug has been open for a significant amount of time now.

### as...@chromium.org (2022-04-28)

[Empty comment from Monorail migration]

### as...@chromium.org (2022-04-28)

I created a new bug to track the status of the new prompt

The argument for blocking .url files wholesale still applies, though... +ajgo for thoughts (see https://crbug.com/chromium/1307930#c10)

### aj...@chromium.org (2022-04-28)

Selecting a .url file in the picker definitely has surprising effects for a person that later attempts to upload the file, and I can see a convincing phish that tries to do this.

So we should probably block .url downloads. It might be necessary to find out if they are used in practice first though - perhaps the safebrowsing team already have metrics, or maybe some need to be added.

However the download/upload steps required perhaps lower the severity so ->Medium.

### an...@chromium.org (2022-05-09)

asully@, ajgo@: what should the next steps be for this issue? thanks!

### as...@chromium.org (2022-05-09)

I have a CL in the works to block download of .url files. Meanwhile, we're working with UX folks to figure out exactly what the prompt described in https://crbug.com/chromium/1320877 will look like

### gi...@appspot.gserviceaccount.com (2022-05-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/22c61cfae5d1b37c773e638d342488ae11118b51

commit 22c61cfae5d1b37c773e638d342488ae11118b51
Author: Austin Sullivan <asully@chromium.org>
Date: Thu May 12 04:52:20 2022

FSA: Sanitize .url files

Bug: 1307930
Change-Id: I7ed3cca5942a5334ba761d269bdd8961fa9d13fe
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3638698
Reviewed-by: Marijn Kruisselbrink <mek@chromium.org>
Commit-Queue: Marijn Kruisselbrink <mek@chromium.org>
Auto-Submit: Austin Sullivan <asully@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1002495}

[modify] https://crrev.com/22c61cfae5d1b37c773e638d342488ae11118b51/content/browser/file_system_access/file_system_chooser.cc
[modify] https://crrev.com/22c61cfae5d1b37c773e638d342488ae11118b51/content/browser/file_system_access/file_system_chooser_unittest.cc
[modify] https://crrev.com/22c61cfae5d1b37c773e638d342488ae11118b51/content/browser/file_system_access/file_system_chooser_browsertest.cc


### as...@chromium.org (2022-05-12)

I'll mark this as closed since the API will no longer allow you to suggest .url files for download.

If the user changes the extension in the file picker to be a .url file, they'll soon  (once https://crrev.com/c/3638058 lands to address https://crbug.com/chromium/1320877) be prompted to confirm they want to download the file (on Windows, at least), since .url is listed as DANEROUS in https://crsrc.org/c/components/safe_browsing/content/resources/download_file_types.asciipb

### as...@chromium.org (2022-05-12)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-12)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-12)

[Empty comment from Monorail migration]

### am...@google.com (2022-05-24)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-05-24)

Congratulations, Abdelhamid! The VRP Panel has decided to award you $2,000 for this report. Thank you for your efforts and taking the time to report this issue to us. 

### am...@google.com (2022-05-24)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-06-21)

[Empty comment from Monorail migration]

### am...@google.com (2022-06-21)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-29)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-18)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### fa...@gmail.com (2023-01-14)

[Comment Deleted]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1307930?no_tracker_redirect=1

[Monorail blocked-on: crbug.com/chromium/1320877]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059141)*
