# Security: OpenFileViaShell may open executables in the same directory with similar filenames unexpectedly 

| Field | Value |
|-------|-------|
| **Issue ID** | [40052529](https://issues.chromium.org/issues/40052529) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>Downloads |
| **Platforms** | Windows |
| **Reporter** | sa...@gmail.com |
| **Assignee** | je...@google.com |
| **Created** | 2020-06-08 |
| **Bounty** | $500.00 |

## Description

Method in question: <https://source.chromium.org/chromium/chromium/src/+/master:ui/base/win/shell.cc;bpv=1;bpt=1;l=67?ss=chromium>

**VULNERABILITY DETAILS**  

The "OpenFileViaShell" method may open executable files with the same base file name as the file it is instructed to open. E.g. Open("file") will instead open "file.exe" or "file.bat" if it exists.

**VERSION**  

Chrome Version: 83.0.4103.97 stable  

Operating System: Windows 10 1909

**REPRODUCTION CASE**  

First visit "<https://download-trick.tails.workers.dev/driveby>" to get a batch file downloaded, then visit "<https://download-trick.tails.workers.dev/>" to get a different (safe) file downloaded, then open the "safe" file by clicking on the download in Chrome. This will trigger the required code path. You should get a smart screen warning from windows saying it preventing the batch file being run as it was unsigned, this can easily be worked around by providing a signed exe or bat file, for the sake of this demonstration I provided a clearly readable unsigned batch file.

Attached is the backend code I'm running to serve up the two files.

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: N/A

## Attachments

- [download-trick-worker.js](attachments/download-trick-worker.js) (text/plain, 538 B)

## Timeline

### mb...@chromium.org (2020-06-09)

brucedawson: Could you please take a look or help find another owner for this?

[Monorail components: UI>Browser>Downloads]

### [Deleted User] (2020-06-09)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### br...@chromium.org (2020-06-10)

Assigning to a teammate who has been working on somewhat similar bugs lately.

### je...@google.com (2020-06-10)

[Empty comment from Monorail migration]

### je...@google.com (2020-07-21)

I was able to reproduce this behavior. I created two simple files:
* "test.bat" containing `echo ".bat file" & pause`
* "test" containing `echo "no file extension" & pause`

I put "test.bat" in my Downloads folder and uploaded "test" to Google Drive (so I could download it using Chrome). When I downloaded "test" and ran it by double-clicking its name in the downloads bar at the bottom of the window, "test.bat" ran instead.

In the debugger, I observed that OpenFileViaShell() calls InvokeShellExecute(), which in turn calls Windows function ::ShellExecuteExW(). Chrome passes this function a SHELLEXECUTEINFO object containing the file path and some other flags. The path passed by Chrome is accurate (it points to "test"); however, ::ShellExecuteExW() opens "test.bat", if present, when given that path.

I'm not sure if ::ShellExecuteExW()'s behavior here is intentional (perhaps files without extensions are deprioritized for some reason?) or a bug, or if we need to pass some kind of flag telling it not to ignore files without extensions. I will do some research.

### je...@google.com (2020-07-21)

A few more observations:

@err immediately after `::ShellExecuteExW()` is 0 (success), so it doesn't seem to perceive any issue with the path it was given or its output.

Also, this behavior doesn't seem to happen with file extensions besides executables. For example, if "test.html" or "test.txt" is present in Downloads, attempting to open downloaded file "test" will result in Windows error "this file does not have an app associated with it for performing this action", showing the correct path to "test".

### je...@google.com (2020-07-21)

This behavior appears to be in line with how the Windows shell works in general, so it's likely safe to say that it's intentional (for Windows). For example, if "test" and "test.bat" are in the same directory, and I run "test" in Command Prompt or ".\test" in PowerShell, "test.bat" will be run. In other words, Windows appears to interpret a command without a file extension as an executable path first, and as a path to an extensionless file second.

I don't think this behavior is desirable for Chrome, however. If I type the path to "test" (no file extension) into the Omnibox, I get the file I requested, i.e., the one without the file extension. Similarly, if I were to download "test" and click it in the downloads bar, I would naturally expect the file I downloaded to be run, not for its path to be interpreted as a shell command.

Perhaps ::ShellExecuteExW() is a poor choice for this application, or there is some way to configure it to avoid this behavior.

### je...@google.com (2020-07-24)

There does not appear to be a way to call ::ShellExecuteExW() without invoking its behavior of interpreting a command without a file extension as an executable.

I discussed this briefly with brucedawson@ and he pointed out that a file with no extension has no type in Windows, so running it is essentially meaningless. This makes sense to me - in the 'working case' described above, where no .bat file is present, Windows just shows an error message. I am looking into whether it would be feasible to simply disable the "open" option for files without extensions.

### je...@google.com (2020-07-30)

I looked at the behavior on Linux, for comparison, and found that the extensionless file was correctly opened in the default text editor. The relevant code for this, `PlatformOpenVerifiedItem()`, just calls `xdg-open` on Linux, so it appears that Linux's built-in behavior simply handles this better.

I drafted a fix that would grey out the "Open" option for files without extensions, but after looking at the Linux version, I'm not too happy with this menu option being greyed out on one platform and available on others. I think it could be confusing and unexpected for users to see "Open" greyed out.

I'm playing with the idea of making "Open" act like "Show in folder" for these extensionless files instead - I think that would make it clearer that Chrome isn't actively preventing the user from opening the file, and showing the file in folder sets the user up nicely to open it via right-click -> Open With.

### je...@google.com (2020-08-11)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-08-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/8d2c055e9e3308bfe57d4feb7271b13431e79b61

commit 8d2c055e9e3308bfe57d4feb7271b13431e79b61
Author: Jesse McKenna <jessemckenna@google.com>
Date: Tue Aug 11 20:39:07 2020

Disable opening extensionless downloads on Windows

This change makes the "Open" option in the downloads bar act like
"Show in Folder" for files without file extensions on Windows.

This fixes an issue where Chrome could unexpectedly open the wrong
file when attempting to open an extensionless file while an executable
of the same name was present in the Downloads folder. For example,
downloading and opening "somefile" while "somefile.exe" was already
present in Downloads would result in "somefile.exe" being run. This
behavior is due to Windows' shell open functionality, which appears to
have special logic to interpret extensionless commands as potential
executables.

Prior to this change, if an extensionless file was opened without an
executable of the same name present (the more common scenario),
Windows would display error "No application is associated with the
specified file for this operation", so this change does not remove any
functionality apart from the ability to trigger this error popup.

Showing the extensionless file in folder sets the user up nicely to
open the file however they want from Windows Explorer via right-click
> Open With.

Bug: 1092518
Change-Id: I1a3bb519867548c916070cbfebd64d0017f5937b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2321528
Commit-Queue: Jesse McKenna <jessemckenna@google.com>
Reviewed-by: Shakti Sahu <shaktisahu@chromium.org>
Cr-Commit-Position: refs/heads/master@{#796968}

[modify] https://crrev.com/8d2c055e9e3308bfe57d4feb7271b13431e79b61/chrome/browser/extensions/api/downloads/downloads_api_browsertest.cc
[modify] https://crrev.com/8d2c055e9e3308bfe57d4feb7271b13431e79b61/components/download/internal/common/download_item_impl.cc


### je...@google.com (2020-08-13)

[Empty comment from Monorail migration]

### [Deleted User] (2020-08-14)

[Empty comment from Monorail migration]

### ad...@google.com (2020-08-17)

[Empty comment from Monorail migration]

### ad...@google.com (2020-08-19)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-08-19)

Thanks for the report! The VRP panel has decided to award $500 for this bug. Someone from our finance team will be in touch.

How would you like to be credited in the Chrome release notes? You say "N/A"... does that mean you'd like to be anonymous? If so we'll want to lock this bug down with Restrict-View-SecurityEmbargo so that people can't see your details. (It's already been opened to downstream Chromium embedders). But we'd much prefer to credit you properly in the release notes and open this bug up as normal in a few months.

### ad...@google.com (2020-08-20)

[Empty comment from Monorail migration]

### sa...@gmail.com (2020-08-24)

> How would you like to be credited in the Chrome release notes? You say "N/A"... does that mean you'd like to be anonymous? If so we'll want to lock this bug down with Restrict-View-SecurityEmbargo so that people can't see your details. (It's already been opened to downstream Chromium embedders). But we'd much prefer to credit you properly in the release notes and open this bug up as normal in a few months.

You can just put "Samuel Attard", no need to lock down this bug :D 

### ad...@google.com (2020-10-01)

[Empty comment from Monorail migration]

### ad...@google.com (2020-10-01)

Re https://crbug.com/chromium/1092518#c18, thanks! Will do.

### ad...@google.com (2020-10-05)

[Empty comment from Monorail migration]

### ad...@google.com (2020-11-03)

[Empty comment from Monorail migration]

### [Deleted User] (2020-11-21)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ti...@gmail.com (2021-01-07)

[Comment Deleted]

### is...@google.com (2021-01-07)

This issue was migrated from crbug.com/chromium/1092518?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40052529)*
