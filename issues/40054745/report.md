# Reading local files through an extension that only has the "downloads" permission

| Field | Value |
|-------|-------|
| **Issue ID** | [40054745](https://issues.chromium.org/issues/40054745) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>Extensions, UI>Browser>Downloads |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | he...@gmail.com |
| **Assignee** | qi...@chromium.org |
| **Created** | 2021-02-09 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**  

It seems possible to use "chrome.downloads.onDeterminingFilename" to listen for downloads and then rename files. This also works for local files even if the "Allow access to file URLs" setting is not enabled.

The behavior described above can be combined with the ability to trigger the download of a local resource by redirecting a local file to a different local file that Chrome is not able to display (e.g. binaries). This forces the file to be downloaded, which in turn ends up firing the "DeterminingFilename" event.

Having all that in mind, the attack to read local files looks like this:

1. User installs an extension that only asks for the "downloads" permission.
2. Using "chrome.downloads.download" an HTML containing the payload is downloaded.
3. Using the "chrome.downloads.onChanged" listener the full path of the local file is retrieved.
4. Using "chrome.tabs.create" we open the HTML file we just downloaded locally.
5. We redirect the local page ten times to make sure that the title of the page is written to the local History file. The title of the page contains a script tag that has our payload.
6. After the redirects are finished, the page is navigated to file:///C:/Users/name/AppData/Local/Google/Chrome/User Data/Default/History. Given Chrome is not able to display this page, it ends up being downloaded.
7. The "DeterminingFilename" event will fire, allowing the attacker to rename the file from "History" to "attack.html".
8. The attacker's local HTML file is redirected to "attack.html" and the javascript code that was inserted earlier in the History file will trigger, allowing an attacker to leak the information.

This seems to be a regression of <https://crbug.com/chromium/989078>.

**VERSION**  

Chrome Version: 88.0.4324.150 (Official Build) (64-bit)  

Operating System: Windows 10

**REPRODUCTION CASE**

1. Download extension.zip and load it into Chrome.
2. After a few seconds an alert will show up stating it was executed inside a copy of the History file, allowing the attacker to leak the information.

Here's an unlisted video demonstrating the issue:  

<https://youtu.be/GChBn2TAwqA>

**CREDIT INFORMATION**  

Reporter credit: Luan Herrera (@lbherrera\_)

## Attachments

- deleted (application/octet-stream, 0 B)
- [bug-1176031.html](attachments/bug-1176031.html) (text/plain, 628 B)
- [extension.zip](attachments/extension.zip) (application/octet-stream, 721 B)

## Timeline

### [Deleted User] (2021-02-09)

[Empty comment from Monorail migration]

### rs...@chromium.org (2021-02-09)

Thanks for the report. It seems like the core issue is that an extension is able to first manipulate the filename of a download and then cause it to open in the browser using the chrome.tabs.create API. Since tabs.create does not require the tabs permission (https://chrome-apps-doc2.appspot.com/extensions/tabs.html#method-create), this can indeed just be done with the browser.

I deleted the PoC in c#0 because it fetches remote content. Attached is a re-packaged extension that will instead fetch the attached HTML file from localhost:8080.

Assigning to qinmin from https://crbug.com/chromium/989078.

[Monorail components: Platform>Extensions UI>Browser>Downloads]

### rs...@chromium.org (2021-02-09)

[Empty comment from Monorail migration]

### qi...@chromium.org (2021-02-10)

I think we can block this by blocking download of file URLs, or maybe we should add a permission on chrome.tabs.create.

### qi...@chromium.org (2021-02-10)

For this issue, the network layer finds the MIME type of the "History" file is application/octet-stream, and renaming it to "attack.html" is allowed. This bypasses the fix we introduced in 989078.
I could do a quick fix to disallow file extension changes for all File URLs. But the root cause is still in chrome.tabs.create. We shouldn't allow FILE urls to be loaded if "allow access to FILE URL" permission is missing.

### qi...@chromium.org (2021-02-10)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-02-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/46ea0eff0cd5f2987bb028dabc56720232d3bfb6

commit 46ea0eff0cd5f2987bb028dabc56720232d3bfb6
Author: Min Qin <qinmin@chromium.org>
Date: Fri Feb 19 17:35:04 2021

Don't allow extensions to overwrite file extensions on file URLs

This CL will block extension to overwrite existing extensions on File
URLs. For example, file:///text.txt cannot be renamed to text.html.

BUG=1176031

Change-Id: I4a0227ee4662a156941348e801135fc0a0549a61
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2685485
Commit-Queue: Min Qin <qinmin@chromium.org>
Reviewed-by: Xing Liu <xingliu@chromium.org>
Cr-Commit-Position: refs/heads/master@{#855740}

[modify] https://crrev.com/46ea0eff0cd5f2987bb028dabc56720232d3bfb6/chrome/browser/download/download_target_determiner.cc
[modify] https://crrev.com/46ea0eff0cd5f2987bb028dabc56720232d3bfb6/chrome/browser/extensions/api/downloads/downloads_api_browsertest.cc


### rs...@chromium.org (2021-02-24)

Is this fixed, or is there more work to do?

### qi...@chromium.org (2021-02-24)

This is fixed for the PoC. But the root cause is still not fixed. We need to ask for  "Allow access to file URLs"  permission for extensions want to open a url.
Not sure who is the right owner for "chrome.tabs.create".

assigning to rdevlin@ to triage.

### [Deleted User] (2021-02-25)

rdevlin.cronin: Uh oh! This issue still open and hasn't been updated in the last 16 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-03-03)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-11)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-12)

rdevlin.cronin: Uh oh! This issue still open and hasn't been updated in the last 31 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### zh...@google.com (2021-03-17)

[Empty comment from Monorail migration]

### rd...@chromium.org (2021-03-18)

qinmin@, can you clarify why an extension should require file access to open an URL to a file tab?  Opening the tab should *not* grant it access to the tab (i.e., it should not be able to execute script or read the page's content), and file URLs have a null origin, so cannot fetch other file URLs.  What's the security risk with opening a tab to a file URL?

(Additionally, there's valid reasons to do this, e.g. bookmark / session / tab managers, etc)

### qi...@chromium.org (2021-03-18)

rdevlin@, for the attack report in #1, the attacker is obviously able to open a downloaded file URL and run java script in that file.
The executed javascript can 
1. change location.href to trigger downloading other file URLs,
2. insert arbitrary javascript into browser history file.

The first behavior seems dangerous, as it can possibly put a sensitive file into download/ dir.
Not sure about the impact of the second behavior after my change. But I think it could be used in other exploits.

### [Deleted User] (2021-04-15)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-26)

[Empty comment from Monorail migration]

### ad...@google.com (2021-07-08)

[Empty comment from Monorail migration]

### va...@chromium.org (2021-07-21)

Assigning to rdevlin.cronin@ to respond to https://crbug.com/chromium/1176031#c16

### rd...@chromium.org (2021-07-22)

The extension cannot directly run JS in the opened file tab.  This was done by a combination of abuse in the downloads API and the fact that opening the history file caused it to be downloaded, and then allowed the extension to change the file type and have Chrome open it, as described by rsesek.  Extensions should not be able to make Chrome open a downloaded file without the downloads.open() permission.

By itself, opening a tab to a file: URL does not cause the extension to have access to the content of that file, and thus I don't think we need to require the file permission to do so (the permission is to *access* files, which the extension cannot do just by opening the tab).

Let me know if I'm missing something, and there's a way for an extension to access the content of the local file *without* the downloads API here.  Otherwise, this seems like it's an issue in the downloads API.

### [Deleted User] (2021-08-05)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-07)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-16)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-11)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-22)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-15)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-02)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-30)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-25)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-03)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-28)

[Empty comment from Monorail migration]

### he...@gmail.com (2022-10-10)

Hey! Rdevlin.cronin@'s assessment on https://crbug.com/chromium/1176031#c21 seems to be correct. The fix on https://crbug.com/chromium/1176031#c7 fixes this issue and prevents the attack from happening. Could this report be marked as fixed and the points raised on https://crbug.com/chromium/1176031#c16 filled in another report for consideration (although I don't think by itself they can be exploited)?

Thanks!

### qi...@chromium.org (2022-10-10)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-10)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-11)

[Empty comment from Monorail migration]

### he...@gmail.com (2022-10-19)

Not sure if the panel already took a look at this report, but I would like to highlight that the impact of this bug was in allowing an attacker to leak local files (more notably the user's cookies and history files) by using an extension that only had the "downloads" permission.

For reference, earlier this year there was a bug (https://crbug.com/chromium/1310461) that allowed an extension with the "downloads" permission to leak environment variables, which I would argue has a similar impact to this issue.

### xi...@chromium.org (2022-10-19)

[Empty comment from Monorail migration]

### am...@google.com (2022-10-20)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-10-20)

Congratulations, Luan! The VRP Panel has decided to award you $5,000 for this report. Thank you for your efforts in discovering and reporting this issue to us -- nice report and nice work! 

### am...@google.com (2022-10-21)

[Empty comment from Monorail migration]

### pg...@google.com (2022-12-13)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-16)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pg...@google.com (2023-02-12)

[Empty comment from Monorail migration]

### pg...@google.com (2023-07-28)

[Empty comment from Monorail migration]

### pg...@google.com (2023-07-28)

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

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1176031?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Platform>Extensions, UI>Browser>Downloads]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40054745)*
