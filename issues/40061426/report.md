# Reading local files through an extension that only has the "downloads" permission

| Field | Value |
|-------|-------|
| **Issue ID** | [40061426](https://issues.chromium.org/issues/40061426) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>Extensions>API, UI>Browser>Downloads |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | he...@gmail.com |
| **Assignee** | qi...@chromium.org |
| **Created** | 2022-10-21 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**  

I was reading the source code of download\_target\_determiner.cc (<https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/download/download_target_determiner.cc>) and found out there is a bug in the ReplaceExtension function (<https://source.chromium.org/chromium/chromium/src/+/main:base/files/file_path.cc;drc=b3842582ae4610f1847d69076ad00570c2eafd79;l=463>), which allows an attacker to perform the attack described in <https://crbug.com/chromium/1176031> again.

When a download happens, you can listen for the chrome.downloads.onDeterminingFilename and suggest a new name for the file.  

There is a check on <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/download/download_target_determiner.cc;l=409> that prevents changing the extension of local files that are downloaded.

The above check was added to fix <https://crbug.com/chromium/1176031>.

But digging deeper, I realized there is an edge case that isn't being tracked in the ReplaceExtension function (which is being used to prevent the change of the extension of local files that are downloaded).

If file:///file.txt (local file) is downloaded, and you want to download it again and change its extension to file.html, the following happens:

if (download\_->GetURL().SchemeIsFile()) {  

base::FilePath file\_path;  

net::FileURLToFilePath(download\_->GetURL(), &file\_path);  

new\_path = new\_path.ReplaceExtension(file\_path.Extension());  

}

New\_path is the name you want to rename the file to, and file\_path is the name of the original file.

file\_path = file.txt  

new\_path = file.html

By using the values above, the code works as expected:  

new\_path = "file.txt".ReplaceExtension(".html")

As it would return "file.html", preventing an attacker to set a new extension to the local file.  

But on the edge case where the original file has no extension and the new file has, the following happens:

file\_path = History  

new\_path = History.html.html

new\_path = "History.html.html".ReplaceExtension("")

Inside the ReplaceExtension function, we can see that if the new extension is empty, the current extension is removed:

FilePath no\_ext = RemoveExtension();  

// If the new extension is "" or ".", then just remove the current extension.  

if (extension.empty() ||  

(extension.size() == 1 && extension[0] == kExtensionSeparator))  

return no\_ext;

Which results in new\_path being changed to "History.html" (as only the first ".html" is stripped).

This makes it possible to exploit <https://crbug.com/chromium/1176031> again, by using "chrome.downloads.onDeterminingFilename" to listen for downloads and then rename files by using the bug described above.

The behavior described above can be combined with the ability to trigger the download of a local resource by redirecting a local file to a different local file that Chrome is not able to display (e.g. binaries). This forces the file to be downloaded, which in turn ends up firing the "DeterminingFilename" event.

Having all that in mind, the attack to read local files looks like this:

1. User installs an extension that only asks for the "downloads" permission.
2. Using "chrome.downloads.download" an HTML containing the payload is downloaded.
3. Using the "chrome.downloads.onChanged" listener to retrieve the full path of the local file.
4. Using "chrome.tabs.create", we open the HTML file we just downloaded locally.
5. We redirect the local page ten times to make sure that the title of the page is written to the local History file. The title of the page contains a script tag that has our payload.
6. After the redirects are finished, the page is navigated to file:///home/user/.config/google-chrome/Default/History. Given Chrome is not able to display this page, it ends up being downloaded.
7. The "DeterminingFilename" event will fire, allowing the attacker to rename the file from "History" to "attack.html" using the bug described in this report.
8. The attacker's local HTML file is redirected to "attack.html" and the javascript code that was inserted earlier in the History file will trigger, allowing an attacker to leak the information.

I would like to highlight that the impact of this bug is in allowing an attacker to leak local files (more notably the user's cookies and history files) by using an extension that only had the "downloads" permission.

The attack can be launched silently, but the PoC isn't doing that to make what is happening clear.

For reference, last year there was <https://crbug.com/chromium/1176031>, which was similar to this issue and allowed an attacker to read local files, and <https://crbug.com/chromium/1310461> which allowed an extension to leak environment variables. Both only required the "downloads" permission and I would argue have a similar impact to this issue.

I have also attached a video (repro.mkv) reproducing this bug.

**VERSION**  

Chrome Version: 105.0.5195.125 (Official Build) (64-bit)  

Operating System: Ubuntu 20.04

**REPRODUCTION CASE**

1. Download "index.html" and serve the file on <http://localhost/index.html>
2. Download "extension.zip" and load it into Chrome.
3. After a few seconds an alert will show up stating it was executed inside a copy of the History file, allowing the attacker to leak the information.

**CREDIT INFORMATION**  

Reporter credit: Luan Herrera (@lbherrera\_)

## Attachments

- [extension.zip](attachments/extension.zip) (application/octet-stream, 1010 B)
- [index.html](attachments/index.html) (text/plain, 610 B)
- [repro.mkv](attachments/repro.mkv) (application/octet-stream, 3.5 MB)

## Timeline

### [Deleted User] (2022-10-21)

[Empty comment from Monorail migration]

### do...@chromium.org (2022-10-24)

Thanks for the report. +downloads folks, can you please take a look?

[Monorail components: Platform>Extensions>API UI>Browser>Downloads]

### [Deleted User] (2022-10-24)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-24)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-10-24)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### qi...@chromium.org (2022-10-27)

Thanks for the report. I think maybe the best option is to prevent local files from being renamed.
Or otherwise we have to recursively remove all extensions from file names if the local file doesn't have an extension. But recursively removing extension seems wierd in many cases.

### gi...@appspot.gserviceaccount.com (2022-11-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b8c563fbebdd80b7cce188f9982dd77f3f1a6153

commit b8c563fbebdd80b7cce188f9982dd77f3f1a6153
Author: Min Qin <qinmin@chromium.org>
Date: Fri Nov 04 20:39:37 2022

Don't allow extension to change the name if the download is a local file

BUG=1377165

Change-Id: I990274563a70cd2081a527ea4f36d524342f8c6c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3984464
Commit-Queue: Min Qin <qinmin@chromium.org>
Reviewed-by: David Trainor <dtrainor@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1067656}

[modify] https://crrev.com/b8c563fbebdd80b7cce188f9982dd77f3f1a6153/chrome/browser/download/download_target_determiner_unittest.cc
[modify] https://crrev.com/b8c563fbebdd80b7cce188f9982dd77f3f1a6153/chrome/browser/download/download_target_determiner.cc
[modify] https://crrev.com/b8c563fbebdd80b7cce188f9982dd77f3f1a6153/chrome/browser/extensions/api/downloads/downloads_api_browsertest.cc


### [Deleted User] (2022-11-10)

qinmin: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### qi...@chromium.org (2022-11-10)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-10)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-11)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-11-14)

another one the bot failed to label for 108 merge review (please note, merge will need to be completed by 10am Pacific tomorrow/Tuesday so this fix can be included in M108/Stable cut). Please let me know if there will any issues with this -- thank you!

### [Deleted User] (2022-11-14)

Merge review required: M108 is already shipping to beta.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), harrysouders (iOS), obenedict (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-11-15)

M108 merge approved, please merge this fix to branch 5359 at soonest (by 10am Pacific tomorrow/Tuesday) so this fix can be included in M108/Stable cut. Thank you! 

### am...@chromium.org (2022-11-15)

[Empty comment from Monorail migration]

### sr...@google.com (2022-11-15)

I have CP'ed the CL here - https://chromium-review.googlesource.com/c/chromium/src/+/4028777 please help monitor and land it asap as i am cutting stable RC today for M108

### gi...@appspot.gserviceaccount.com (2022-11-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/29c9e17c5bb51c058284afbecf99b4878b2ae82f

commit 29c9e17c5bb51c058284afbecf99b4878b2ae82f
Author: Min Qin <qinmin@chromium.org>
Date: Tue Nov 15 18:14:46 2022

Don't allow extension to change the name if the download is a local file

BUG=1377165

(cherry picked from commit b8c563fbebdd80b7cce188f9982dd77f3f1a6153)

Change-Id: I990274563a70cd2081a527ea4f36d524342f8c6c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3984464
Commit-Queue: Min Qin <qinmin@chromium.org>
Reviewed-by: David Trainor <dtrainor@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1067656}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4028777
Reviewed-by: Min Qin <qinmin@chromium.org>
Owners-Override: Srinivas Sista <srinivassista@chromium.org>
Commit-Queue: Srinivas Sista <srinivassista@chromium.org>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/5359@{#843}
Cr-Branched-From: 27d3765d341b09369006d030f83f582a29eb57ae-refs/heads/main@{#1058933}

[modify] https://crrev.com/29c9e17c5bb51c058284afbecf99b4878b2ae82f/chrome/browser/download/download_target_determiner_unittest.cc
[modify] https://crrev.com/29c9e17c5bb51c058284afbecf99b4878b2ae82f/chrome/browser/download/download_target_determiner.cc
[modify] https://crrev.com/29c9e17c5bb51c058284afbecf99b4878b2ae82f/chrome/browser/extensions/api/downloads/downloads_api_browsertest.cc


### am...@google.com (2022-11-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-11-18)

Congratulations, Luan! The VRP Panel has decided to award you $5,000 for this report. Thank you for your efforts and reporting this issue to us -- nice work! 

### am...@google.com (2022-11-19)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-11-28)

[Empty comment from Monorail migration]

### pg...@google.com (2022-11-29)

[Empty comment from Monorail migration]

### pg...@google.com (2022-11-29)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-16)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1377165?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Platform>Extensions>API, UI>Browser>Downloads]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061426)*
