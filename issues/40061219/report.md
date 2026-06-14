# Security: Files saved through showSaveFilePicker have unexpected read access

| Field | Value |
|-------|-------|
| **Issue ID** | [40061219](https://issues.chromium.org/issues/40061219) |
| **Status** | Verified |
| **Severity** | S3-Low |
| **Priority** | P4 |
| **Component** | Blink>Storage>FileSystem |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | re...@gmail.com |
| **Assignee** | ay...@chromium.org |
| **Created** | 2022-10-03 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

The showSaveFilePicker() method from the File System Access API can be used to open a read/write handle to a file chosen by the user. The save dialog displayed looks identical to a file download or the "save as" functionality, which implies that a file is being saved, but not read. This can be used to trick a user into editing the downloaded file with sensitive data and then reading the contents of the file with no further user interaction.

I imagine this potentially being used in attack scenarios such as websites offering downloads for fillable PDF templates, software configuration files that require tokens added into them, and so on.

I would suggest making the handle from the showSaveFilePicker() method write-only. If a read is attempted, additional confirmation should be requested from the user.

**VERSION**  

Chrome Version: 106.0.5249.91 Stable, 107.0.5304.18 Beta, 108.0.5327.0 Dev  

Operating System: Windows 10/11, macOS 12.5.1, Linux

**REPRODUCTION CASE**  

The attached HTML file can be opened locally as a file or hosted in a secure context (https).  

This issue can be reproduced on Windows, Mac, and Linux (I have not tested it on ChromeOS).

1. Open the poc.html file in Chrome.
2. Use the link on the site to "download" a fillable text file.
3. Open the downloaded file locally in a text editor, fill it out, and save it.
4. The website will display the contents of the edited text file.

The above example is also demonstrated in the attached demo video.

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: Jasper Rebane (popstonia)

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 1.2 KB)
- [demo.mp4](attachments/demo.mp4) (video/mp4, 1.2 MB)
- [Screenshot 2023-09-28 at 10.52.36 AM.png](attachments/Screenshot 2023-09-28 at 10.52.36 AM.png) (image/png, 182.7 KB)

## Timeline

### [Deleted User] (2022-10-03)

[Empty comment from Monorail migration]

### mp...@chromium.org (2022-10-03)

Thanks for the report! This does seem problematic.

[Monorail components: Blink>Storage>FileSystem]

### mp...@chromium.org (2022-10-03)

Thanks for the report! This does seem problematic.

### [Deleted User] (2022-10-03)

[Empty comment from Monorail migration]

### as...@chromium.org (2022-10-03)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-04)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-10-04)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-10-18)

asully: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-11-01)

asully: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### as...@chromium.org (2022-11-01)

Marking P2 since this is a known issue. Ideally we've have a nice way to track whether a file has changed from outside the web and invalidate the file accordingly, but that's a bigger task than it seems

### [Deleted User] (2022-11-30)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-08)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-05)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-31)

[Empty comment from Monorail migration]

### pg...@google.com (2023-07-21)

[Secondary shepherd]
Chatted with the owner of the bug offline - the fix for this may require a larger re-design and will be discussed in depth for a way forward in the near future

### [Deleted User] (2023-08-16)

[Empty comment from Monorail migration]

### pg...@google.com (2023-09-20)

[Empty comment from Monorail migration]

### pg...@google.com (2023-09-21)

The main concern here is that the UI makes it unclear that the access being given is a read + write - not just a write. 

The next steps for this bug are:
1. to mitigate by updating the title of the file picker from "Save As" to something that is more representative of the permissions being given and 
2. to separate out the read and write accesses into different permission flows for long term for clarity

@asully to comment with an expected timeline for the above in case another secondar shepherd comes along to ping you to ask (:

### ay...@chromium.org (2023-09-22)

Thanks for the summary pgrace@

#1 seems like a reasonable first step, we'll have to discuss with UX folks for an approved string that is appropriate here. I can kick this off now.

#2 will take some time to do this carefully. We don't want to break sites so we'd want to understand how this is used, and how this change would affect existing sites. We'll need to add metrics so this will take a few milestones until we can decide if this is a feasible route. 

### ay...@chromium.org (2023-09-27)

[Empty comment from Monorail migration]

### me...@chromium.org (2023-09-27)

Redirecting to dwarren for content design input

### dw...@google.com (2023-09-28)

I think I understand the problem. The file picker dialog appears as if the user's action is only to "Save as". In fact, the website has read access to the saved file and this isn't clear to the user. 

The suggestion is to change the "Save" button to something like "Save and share as" (see the attached screenshot for context).

I can appreciate how a string change like this is the fastest way to try to warn the user that something more than just "Save" is going on, but I'm not sure "Save and share as" is sufficient. Speaking from a sampling of 1 (myself), users aren't aware that it's even possible for a site to obtain read access to a downloaded file. I think I'd interpret "Save and share as" as if I'm going to download the file and, if I want, I can then share it with my friends with the file name I provide (share with friends through Gmail or other means). 

I understand we're tackling this vulnerability in various stages, but can we imagine changing the UI to warn the user in the first round? Is there room, for example, to add a sentence that says something like "Be careful! Any changes you make to this file will be accessible to this site"? Or how hard would it be to add a learn more path? A learn more path would be useful because we could get away with a confusing button label (if we had to), and count on the user to look to learn more if they're confused. 

Assuming there isn't time/resources to add a warning messages, and assuming changing the label of the "Save" button is the best we can do as a first effort, perhaps:
Save (edits you make are visible to the site)
Save and share file with site
Save — this site can access your edits
Save — site can access changes
Save — site can see edits
Save and edit site's file <explore direction where we make it clear that the file "belongs" to the site? Probably not clear to user, but it's an idea...>

None of these feel good to me but I have trouble seeing how we can express the danger in a button that is typically a single word long. Maybe a quick meeting to discuss? 




### as...@chromium.org (2023-09-28)

[Empty comment from Monorail migration]

### ay...@chromium.org (2023-10-05)

To summarize in-person discussions with dwarren@ here, our next steps are to...

1. Update title to be "Warning: this site can see edits you make"

2. Measure usage and figure out feasibility of separating out the read/write access

Depending on 2, if not feasible, next step would be either to

- Work with UX folks to update file picker flow to better inform user of permissions given. Possibly to show a prompt after selection (similar to directory picker)

OR

- Remove read permission when selecting a file, and revert title string to no longer say that the site can see the edits you make


(Thanks @dwarren for your help!)

### [Deleted User] (2023-10-11)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-10-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/ca5225714d6eafdac2b0278aef6d42fe33844722

commit ca5225714d6eafdac2b0278aef6d42fe33844722
Author: Ayu Ishii <ayui@chromium.org>
Date: Wed Oct 11 21:27:30 2023

FileSystem: Add title to save file picker

This change adds a title for the file picker when
the showSaveFilePicker is used. This title should be
updated again if we decide to separate read/write access.

Screenshot[internal]: http://screen/4F9vv7C2Nj6UPu8

Bug: 1370761
Change-Id: I66d6be3fc8a9827fb059477ba473061f0ad109f4
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4924047
Commit-Queue: Ayu Ishii <ayui@chromium.org>
Reviewed-by: Daseul Lee <dslee@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1208496}

[add] https://crrev.com/ca5225714d6eafdac2b0278aef6d42fe33844722/chrome/app/generated_resources_grd/IDS_FILE_SYSTEM_ACCESS_CHOOSER_OPEN_SAVE_FILE_TITLE.png.sha1
[modify] https://crrev.com/ca5225714d6eafdac2b0278aef6d42fe33844722/chrome/browser/file_system_access/chrome_file_system_access_permission_context.cc
[modify] https://crrev.com/ca5225714d6eafdac2b0278aef6d42fe33844722/chrome/app/generated_resources.grd


### [Deleted User] (2023-12-06)

[Empty comment from Monorail migration]

### yu...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-10)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-11)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-11)

This issue was migrated from crbug.com/chromium/1370761?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

### ps...@google.com (2024-02-14)

Hello ayui@,

I see in https://g-issues.chromium.org/issues/40061219#comment25 that there were some planned next steps. Were there any updates regarding this bug?

[Secondary security shepherd]

### ay...@chromium.org (2024-03-06)

There haven't been any updates on the work here. There are some other ongoing discussions on how we might want to have write-only access (context: [crbug/328458680](https://crbug.com/328458680)), therefore I will close this issue as the main concern is mitigated with the string update, and track further work on write-only access on [crbug/328458680](https://crbug.com/328458680).

### am...@google.com (2024-03-14)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### re...@gmail.com (2024-03-14)

Thank you for the reward! Would it be possible to change the name credited to "Lyra Rebane (rebane2001)"?

### am...@chromium.org (2024-03-14)

Thank you for the report! Upon further assessment, we don't believe this should have been classified as a security issue and this did not result in a change to the security posture of Chrome. Since this did result in a UI change and a new feature request for write-only access, we did want to extend a small thank you reward for your report. Thanks again for taking the time to discover and report this issue!

### re...@gmail.com (2024-03-14)

Ah, sounds fair. Thanks again for the reward :)

### am...@chromium.org (2024-03-14)

:)
re: c#45 -- of course!
This issue won't show up in release notes, but I've updated our database for future issues to be credited with the updated credit name and handle accordingly!

### pe...@google.com (2024-06-13)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061219)*
