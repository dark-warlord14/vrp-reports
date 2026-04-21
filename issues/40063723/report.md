# Security: Extensions with "download" permissions can read local files by using FSA API

| Field | Value |
|-------|-------|
| **Issue ID** | [40063723](https://issues.chromium.org/issues/40063723) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>Extensions>API, UI>Browser>Downloads |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ha...@gmail.com |
| **Assignee** | qi...@chromium.org |
| **Created** | 2023-03-22 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

I have devised a method for a malicious extension with "download" permissions but no access to file:// URLs to read local files with unregistered MIME type such as History on Chrome on Windows.

This method combines aspects of <https://bugs.chromium.org/p/chromium/issues/detail?id=1377165> and the File System Access API.

How it works is as follows:

Suppose we want to steal  

"file:///C:/Users/User/AppData/Local/Google/Chrome/User%20Data/Default/History"

1. We get the user to hold "Enter". This opens the save file picker via showSaveFilePicker with a suggested name of "History". The extension now has an active file handle pointing to "History".
2. The extension registered an onDeterminingFilename listener at the start with a conflictAction of overwrite. The important thing this does is that it has the ability to overwrite any existing file with the same name.

This means that if a user downloads a file named History to the Downloads folder then onDeterminingFilename will overwrite the old History file in the Downloads folder with the new one.

3. The extension then navigates to "file:///C:/Users/User/AppData/Local/Google/Chrome/User%20Data/Default/History"  
   
   since this has the unregistered MIME type a download is initiated and onDeterminingFilename triggered.
4. The "History" file in Step 1) is overwritten with the new "History" file that we want to steal
5. The active file handle is pointing to the "History" file with the contents that we want to steal. The extension can then read this active file handle to steal the contents.

**VERSION**  

Chrome Version: 113.0.5668.0 (Official Build) canary (64-bit) (cohort: Clang-64)  

Operating System: Windows 10 Version 21H2 (Build 19044.2728)

**REPRODUCTION CASE**

1. Replace the "filename" variable in script-inline.js with the file you want to steal. Best if you steal the Chrome history file located at "file:///C:/Users/<YOUR\_USERNAME>/AppData/Local/Google/Chrome/User%20Data/Default/History", where <YOUR\_USERNAME> is your Windows username.
2. Install the extension and uncheck access to file:// URLs
3. Go to script.html of the extension and then hold Enter key for a while. The alert popped up showing the contents of the History file.

SUGGESTION  

If I were to say what went wrong, it would be onDeterminingFilename should not be triggered on downloads initiated from file:// URLs without file:// URL access checked.

## Attachments

- [background.js](attachments/background.js) (text/plain, 147 B)
- [manifest.json](attachments/manifest.json) (text/plain, 300 B)
- [script.html](attachments/script.html) (text/plain, 57 B)
- [script-inline.js](attachments/script-inline.js) (text/plain, 830 B)
- [Untitled_ Mar 22, 2023 9_55 PM.webm](attachments/Untitled_ Mar 22, 2023 9_55 PM.webm) (video/webm, 1.4 MB)
- [manifest.json](attachments/manifest.json) (text/plain, 249 B)
- [script.html](attachments/script.html) (text/plain, 57 B)
- [script-inline.js](attachments/script-inline.js) (text/plain, 1.3 KB)

## Timeline

### [Deleted User] (2023-03-22)

[Empty comment from Monorail migration]

### ha...@gmail.com (2023-03-22)

[Empty comment from Monorail migration]

### ha...@gmail.com (2023-03-22)

Note: Canary is not a requirement for this bug. It was the just the browser I used to test the bug at the time of submit. Chrome stable also works, version: 111.0.5563.110 (Official Build) (64-bit) (cohort: 111_Win_110_Ramup) 

### hc...@google.com (2023-03-22)

Thanks for the report. @qinmin or @devlin, can you take a look? 

[Monorail components: Platform>Extensions>API UI>Browser>Downloads]

### [Deleted User] (2023-03-22)

[Empty comment from Monorail migration]

### qi...@chromium.org (2023-03-22)

I guess the best way to fix this is to disable onDeterminingFilename for file URLs. This gives attackers less control on manipulating the local files, and thus make all such attacks difficult to carry out.

### qi...@chromium.org (2023-03-22)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-23)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-03-24)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-03-24)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-06)

qinmin: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-04-20)

qinmin: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2023-04-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/4b77ed5a3fb2add8a9f6604b10594fce09681405

commit 4b77ed5a3fb2add8a9f6604b10594fce09681405
Author: Min Qin <qinmin@chromium.org>
Date: Fri Apr 21 21:46:51 2023

Don't inform extensions for file URL downloads

BUG=1426807

Change-Id: Id61dd71f2750dc3b06a41a3103f7a6b265c694b2
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4363720
Commit-Queue: Min Qin <qinmin@chromium.org>
Reviewed-by: David Trainor <dtrainor@chromium.org>
Code-Coverage: Findit <findit-for-me@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#1134065}

[modify] https://crrev.com/4b77ed5a3fb2add8a9f6604b10594fce09681405/chrome/browser/download/download_target_determiner_unittest.cc
[modify] https://crrev.com/4b77ed5a3fb2add8a9f6604b10594fce09681405/chrome/browser/download/download_target_determiner.cc
[modify] https://crrev.com/4b77ed5a3fb2add8a9f6604b10594fce09681405/chrome/browser/extensions/api/downloads/downloads_api_browsertest.cc


### ha...@gmail.com (2023-04-26)

Friendly ping on this issue

### tj...@chromium.org (2023-04-26)

qinmin@/ haxatron1@: Does the change in https://crbug.com/chromium/1426807#c13 resolve the issue, or is there more that remains to fix this?

### qi...@chromium.org (2023-04-26)

Yes, #13 should fix the issue

### ha...@gmail.com (2023-04-27)

[Comment Deleted]

### ha...@gmail.com (2023-04-27)

[Comment Deleted]

### qi...@chromium.org (2023-04-27)

I cannot access that bug but I assume they are separate issues since that one will not use extension.

### ha...@gmail.com (2023-04-27)

[Comment Deleted]

### ha...@gmail.com (2023-04-27)

[Comment Deleted]

### [Deleted User] (2023-04-27)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-27)

[Empty comment from Monorail migration]

### ad...@chromium.org (2023-04-27)

[Empty comment from Monorail migration]

### ha...@gmail.com (2023-05-04)

Not sure if anything has been decided yet but I wanted to point out that it is possible for an attacker to determine the OS username of the victim using the same extension "downloads" API by first downloading a plaintext file and then querying its local filename. The attached extension below steals the History file without the need to specify the username.

Additionally unlike bug https://bugs.chromium.org/p/chromium/issues/detail?id=1377165, this allows for stealing of more files than History file, with the precondition that visiting the URL will initiate a download. The following are some examples which initiates downloads and can thus be stolen by this attack

binary files
.zip files,
.docx files

### am...@google.com (2023-05-05)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-05-05)

Congratulations, Axel! The VRP Panel has decided to award you $2,000 for this report. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2023-05-05)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-05-25)

[Empty comment from Monorail migration]

### am...@google.com (2023-05-30)

[Empty comment from Monorail migration]

### pg...@google.com (2023-05-30)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-03)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1426807?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Platform>Extensions>API, UI>Browser>Downloads]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40063723)*
