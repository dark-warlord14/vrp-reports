# Security: In File System Access API Hide Extension & Dangerous Warning Using PiP - Picture in Picture

| Field | Value |
|-------|-------|
| **Issue ID** | [40076292](https://issues.chromium.org/issues/40076292) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P4 |
| **Component** | Blink>Media>PictureInPicture, Blink>Storage>FileSystem |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | pu...@gmail.com |
| **Assignee** | li...@chromium.org |
| **Created** | 2023-11-07 |
| **Bounty** | Confirmed (amount unknown) |

## Description

**VULNERABILITY DETAILS**

In File System Access API Hide Extension & Dangerous Warning Using PiP - Picture in Picture

Using documentPictureInPicture.requestWindow width, height pip Window We Can hide Filetype Extension & Dangerous Warning

**VERSION**  

120.0.6099.5 (Official Build) beta (64-bit)  

Operating System: [Windows 10 (64-bit)]

**REPRODUCTION CASE**

1. Host Index.html & Puf2.html In Your Local Host or Server
2. Open <http://127.0.0.1/>
3. Click Anywhere on Page
4. Click [Save Text file]
5. Select a Folder to Save
6. [Save]

**CREDIT INFORMATION**  

Reporter credit: [Puf]

## Attachments

- [Poc video.mp4](attachments/Poc video.mp4) (video/mp4, 659.9 KB)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- [Window.PNG](attachments/Window.PNG) (image/png, 24.7 KB)
- [pip edge reproduce.mp4](attachments/pip edge reproduce.mp4) (video/mp4, 840.7 KB)
- [Latest Update.mp4](attachments/Latest Update.mp4) (video/mp4, 765.5 KB)
- [Reproduce.mp4](attachments/Reproduce.mp4) (video/mp4, 564.2 KB)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- [Screenshot #1.PNG](attachments/Screenshot #1.PNG) (image/png, 15.2 KB)
- [Latest Reproduce .mp4](attachments/Latest Reproduce .mp4) (video/mp4, 486.1 KB)
- [Screenshot.png](attachments/Screenshot.png) (image/png, 24.7 KB)
- [Reproduce.mp4](attachments/Reproduce.mp4) (video/mp4, 564.2 KB)

## Timeline

### [Deleted User] (2023-11-07)

[Empty comment from Monorail migration]

### es...@chromium.org (2023-11-08)

Thanks for the report.

I was able to reproduce this on Linux stable and I assume it's not a regression. Note that the files must be hosted from an HTTPS origin to reproduce (e.g., follow instructions at [1] to host locally). The dangerous file warning at [2] is truncated. It can be scrolled to see the full message but this is very awkward.

I feel like PiP windows are not supposed to be able to trigger any dialog, thus perhaps showSaveFilePicker() should be disabled in a PiP window? I'm interpreting this as a PiP bug but cc'ing File System Access owners in case they have thoughts too.

I'm going to tentatively rate this as Low severity. The two mitigating factors are: (1) 2 clicks required, and (2) this warning seems like a fairly weak mitigation to begin with, and user-facing warnings are not mentioned at all in the security considerations section of the File System Access API [3]. It seems that the real mitigations against downloading dangerous executables are not marking downloaded files as executable, malware scans, and Mark-of-the-Web or similar.

[1] https://gist.github.com/DannyHinshaw/a3ac5991d66a2fe6d97a569c6cdac534
[2] https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/file_system_access/file_system_access_dangerous_file_dialog.cc;l=51?q=IDS_FILE_SYSTEM_ACCESS_DANGEROUS_FILE_TEXT&ss=chromium&start=11
[3] https://wicg.github.io/file-system-access/#security-considerations

### es...@chromium.org (2023-11-08)

[Empty comment from Monorail migration]

[Monorail components: Blink>Media>PictureInPicture Blink>Storage>FileSystem]

### [Deleted User] (2023-11-08)

[Empty comment from Monorail migration]

### st...@chromium.org (2023-11-08)

Could you use window.open() with small enough width/height params to open a popup and accomplish the same thing? If so, then it might not be a pip-exclusive issue, but more of a small-window issue

### [Deleted User] (2023-11-08)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pu...@gmail.com (2023-11-08)

https://crbug.com/chromium/1500317#c2 We can Complete Hide The dangerous file warning. in PiP - Picture in Picture & scroll does not Work using small pip window

### is...@google.com (2023-11-08)

This issue was migrated from crbug.com/chromium/1500317?no_tracker_redirect=1

[Multiple monorail components: Blink>Media>PictureInPicture, Blink>Storage>FileSystem]
[Monorail components added to Component Tags custom field.]

### pu...@gmail.com (2024-05-29)

Would you kindly give me an update?

What’s the current status of this Issue.

Thank you!

### st...@chromium.org (2024-05-29)

Sorry, I haven't had a chance to look further into this issue. Are you able to do this same thing with a standard popup window using window.open() with the same width/height?

### pu...@gmail.com (2024-05-29)

Yes, I Have Reported similar Issue for window popup too <https://issues.chromium.org/issues/40067068>

### pu...@gmail.com (2024-06-21)

...

### pu...@gmail.com (2024-06-28)

Would you kindly give me an update?

What’s the current status of this Issue.

Thank you!

### pu...@gmail.com (2024-08-07)

Would you kindly give me an update? any progress here

What’s the current status of this Issue.

Thank you!

### pu...@gmail.com (2024-08-07)

if we reproduce same issue in Microsoft edge browser

when the user points out the curser to the dialog in pip window, the permission dialog switch to normal size so the user can see the important information in pip window

i have attached edge browser reproduce video

### pu...@gmail.com (2024-11-04)

looks like this vulnerability is fixed! in latest Chrome Version 132.0.6813.0 (Official Build) canary (64-bit) Windows 10

Please kindly Verify and Change Status to fixed

I Have Attached Latest Reproduce Video

### pu...@gmail.com (2024-11-04)

- New Updated Added = Warning: this site can see edits you make

### pu...@gmail.com (2024-11-05)

deleted

### pu...@gmail.com (2024-11-07)

Hello @liberato

can you please verify It looks like this could have been fixed by your work in <https://issues.chromium.org/issues/374985447>

Thank you

### pu...@gmail.com (2024-11-12)

Friendly ping

### aj...@chromium.org (2024-11-15)

-> new owner - see comment 20

### pu...@gmail.com (2024-11-19)

Improved Report

- When a user clicks on the attacker's PIP window page it is possible to Spoof Malicious Extension & Hide the Dangerous Warning message on Permission dialog in PIP Window
- Because the Dangerous Warning message is Hidden on Permission dialog & Malicious file is spoofed with legit extension due to this Vulnerability, the user is not capable to know exact file information, which allows attacker to Spoof File extension and hide the Dangerous Warning message which Convince user to save the Malicious file

attached a video reproducing the attack
I have also attached the files used in the PoC

REPRODUCTION CASE

1. Load Attacked POC.html & PIP.html in one Folder on Your Localhost or Server
2. Open POC.html
3. Click anywhere on page
4. PIP window will show up, click [Save Text file] button in PIP Window
5. Select a Folder to Save
6. Permission Dialog will show up without any Warning Message and legit spoofed file extension now click on [Save] Button on Permission dialog

### pu...@gmail.com (2024-11-21)

deleted

### pu...@gmail.com (2024-11-26)

Friendly ping

### pu...@gmail.com (2024-11-29)

Friendly ping

### pu...@gmail.com (2024-12-04)

Friendly ping

### am...@chromium.org (2024-12-05)

@steimel and @liberato Can you please confirm this issue is resolved? There seem to be a number of previously reported very similar-ish issues related to PIP.
If possible, it would be helpful to understand if [issue 374985447](https://issues.chromium.org/issues/374985447) is a standalone bug or a sub-bug to partially resolve another / other known issues.
Thank you.

### pu...@gmail.com (2025-01-19)

Friendly ping regarding Status

Thank you

### pu...@gmail.com (2025-01-30)

I have Verified this issue is resolved I have Attached latest reproduce video

Please kindly Update this issue if it is resolved

Thank you

### pu...@gmail.com (2025-02-26)

Hope you are well

any Update Regarding status

Thank you

### pu...@gmail.com (2025-03-03)

it's been long time no update on status

Any update Regarding status

Thank you

### aj...@chromium.org (2025-03-12)

Marking fixed - no information on what might have fixed this.

### ch...@google.com (2025-03-12)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### am...@chromium.org (2025-03-13)

We can no longer close issues without fix commit information. Until what change fixed this has been identified, we're unfortunately unable to close this.

### pu...@gmail.com (2025-03-14)

I have provided ref <https://issues.chromium.org/issues/374985447> this maybe fixed this issue, but Owner of this issue knows best about it.

I don't know when the owner of this issue is going to response on this thread, I think I have to wait

Thank you amy, for the update here

### pu...@gmail.com (2025-04-25)

I'm providing a reference after several days of thorough searching, I have successfully identified the CL that fixed this Vulnerability

Reference:

<https://issues.chromium.org/issues/384719892>

CL: <https://chromium-review.googlesource.com/c/chromium/src/+/6107999>

<https://chromiumdash.appspot.com/commit/e77c4b725defb9710dd047a46490153cd60e8fbc>

### pu...@gmail.com (2025-05-06)

Friendly Reminder:

I'm providing a reference after several days of thorough searching, I have successfully identified the CL that fixed this bug

Reference:

<https://issues.chromium.org/issues/384719892>

CL: <https://chromium-review.googlesource.com/c/chromium/src/+/6107999>

<https://chromiumdash.appspot.com/commit/e77c4b725defb9710dd047a46490153cd60e8fbc>

I kindly request you update its status to fixed

Thank you for your time and support

### pu...@gmail.com (2025-05-29)

Friendly Reminder:

I kindly request you update its status

### pu...@gmail.com (2025-06-23)

please update status of this issue to Fixed? Thanks!

I have provided the commit above

### pu...@gmail.com (2025-07-22)

Friendly Remainder please update status of this issue to Fixed? Thanks!

I have provided the commit above

### ch...@google.com (2025-07-23)

Dear owner, thanks for fixing this bug. We've reopened it because:

- Some CLs listed in the “Fixed By Code Changes” field are invalid and have been removed. Please provide an appropriate Gerrit url that matches the pattern: `https://<host>-review.googlesource.com/c/<repo>/+/<change_number>` or use the value 'NA' and re-mark this bug as fixed. If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### pu...@gmail.com (2025-07-24)

thank you for the update
I think can't close this Vulnerability without cl

### aj...@chromium.org (2025-07-29)

hush robot.

### ch...@google.com (2025-07-29)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### pu...@gmail.com (2025-07-29)

again reopened :'(

### pu...@gmail.com (2025-07-29)

Please Change Fixed by Code Changes:​ NA

### pu...@gmail.com (2025-07-30)

Thank you for Updating the issue, but the issue has unfortunately reopened.

Thank you

### sp...@google.com (2025-08-28)

** NOTE: This is an automatically generated email **

Hello,

Chrome Vulnerability Rewards Program (VRP) Panel has decided that the security impact of this issue does not meet the criteria to qualify for a reward.

Rationale for this decision:
Thank you for the report. There is no evidence this scenario could be reasonably exploited to result in user harm nor is it clear that any fix or security beneficial change resulted from this report. Therefore, this report is unfortunately not eligible for a Chrome VRP reward.

Please note that the fact that this issue is not being rewarded does not mean that the product team won't fix the issue. We have filed a bug with the product team and they will review your report and decide if a fix is required. We'll let you know if the issue was fixed.

Regards,
Google Security Bot


--
How did we do? Please fill out a short anonymous survey (https://goo.gl/IR3KRH).

### pu...@gmail.com (2025-08-28)

Thank you for the update

I would like to submit some information regarding this vulnerability & would like to request a reassessment based on the following points:

The vulnerability allows an attacker to:

Hide the Dangerous Warning Message in permission dialog & Spoof a Malicious File Extension in dialog

Hiding the Dangerous Warning Message: When a user is prompted to save a file, in Chrome File System API dialog display a warning dialog if the file type is potentially dangerous. The vulnerability allows this critical warning message to be obscured or hidden from view within the PIP window. I have attached evidence

Spoofing a Malicious File Extension: An attacker can make a malicious file appear as if it has a legitimate and safe file extension rather than its true, dangerous extension in File System API dialog

The file name is displayed with a spoofed extension, making it appear harmless.

The security warning that would normally alert the user to the file's true nature is obscured.

This combination deceives the user into believing the file is safe to download and open, as they are not presented with the standard red flags. The user is thus convinced to save a malicious file without knowing the actual risks.

Please kindly reassess

Thank you for your time and for reconsidering my report.

### pu...@gmail.com (2025-08-28)

> We have filed a bug with the product team, and they will review your report and decide if a fix is required. We'll let you know if the issue was fixed.

I can confirm that the 'Dangerous Warning' issue has been resolved I'm able to see the 'Dangerous Warning'. I verified the fix in the latest version several months ago. For your reference I have attached a video for your review. See: <https://issues.chromium.org/issues/40076292#comment30>

### am...@chromium.org (2025-08-29)

Hello, that message is an artifact of the SPUR tooling that is not been updated to reflect Chrome VRP processed, we are not saying this issue is not fixed. We are saying that this report did not have impact on or result in any security beneficial change. The changes related to this being resolved were part of known and ongoing work and were not an outcome of this report.

Additionally, this is not realistically exploitable in our opinion. In the file chooser process a user can see the really long set of extensions and this will stick out to a user. This doesn't appear harmless to a user, because most users would not expect to see that many file extensions for a single file.
While we appreciate the report, we do consider this a functional issue.

### pu...@gmail.com (2025-08-29)

Thank you 💚 I am grateful for your attention to this. I appreciate your prompt response

### ch...@google.com (2025-11-11)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> Thank you for the report. There is no evidence this scenario could be reasonably exploited to result in user harm nor is it clear that any fix or security beneficial change resulted from this report. Therefore, this report is unfortunately not eligible for a Chrome VRP reward.
> 
> Please note that the fact that this issue is not being rewarded does not mean that the product team won't fix the issue. We have filed a bug with the product team and they will review your report and decide if a fix is re

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40076292)*
