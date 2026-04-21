# Security: Extension with <all_urls> permission can read arbitrary local files although  (Allow access to file URLs) is disabled

| Field | Value |
|-------|-------|
| **Issue ID** | [40061772](https://issues.chromium.org/issues/40061772) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>Extensions>API |
| **Platforms** | Fuchsia, Linux, Mac, Windows |
| **Reporter** | el...@gmail.com |
| **Assignee** | tj...@chromium.org |
| **Created** | 2022-11-16 |
| **Bounty** | $10,000.00 |

## Description

**VULNERABILITY DETAILS**

An extension with the <all\_urls> permission can read any file on the file system and send it's content to a remote host, using chrome.tabs.captureVisibleTab although extension (Allow access to file URLs) is disabled.

this bug is a fork of <https://bugs.chromium.org/p/chromium/issues/detail?id=810220>

## **VERSION** :-

Google Chrome Version: Version 107.0.5304.110 (Official Build) (64-bit)  

Microsoft Edge: Version 107.0.1418.42 (Official build) (64-bit)

## Operating System: Linux-Ubuntu 21.10

Google Chrome Version: 107.0.5304.107 (Official Build) (64-bit)

Operating System: Windows 10 Enterprise 2H1 Build (19043.1826)

## ========== **REPRODUCTION CASE** :-

## 1st Round:

Download attachment (PoC extension) and place in a Folder enable Developer mode and Load-unpacked then Select folder of Extension Created before upon loading will :

1- Create a new tab (using tabs.create) with its URL set to the value of the (fileToFetch=file:///etc/passwd) in Linux for Example;

2- Listen for tabs updates and try to take a screenshot (using chrome.tabs.captureVisibleTab) of the newly opened tab.

3- If the screenshot fails (which will occur upon opening of (file:///etc/passwd) at step 1 using tabs.create), reload the tab. This will cause the tab to be updated and a new screenshot to be taken.

4- When the screenshot is made the image data is displayed in extension Console (background.html), and send it to the exfiltration endpoint,specified by the value of exfiltration Endpoint constant (if it was Set).

5- The opened tab is closed

## ============ Second Round

Go to Extension Details under chrome://extensions/?id=EXTENSION-ID and (( Disable Allow access to file URLs)), then diasble and enable the extension or Reload it as shown in the Poc Video (shows two Rounds)

## What's Go Wrong:

-Local files Still can be exfiltrated By the Extension Although (Allow access to file URLs) not activated.  

-Extension with <all\_urls> permission and without enabling (Allow access to file URLs) can Navigate file:/// scheme using chrome.tabs.create method.

## What's Expected:

-if the extension with <all\_urls> permission and without enabling (Allow access to file URLs) we should do the following

1-Check permissions while using (chrome.tabs.create) method ,and not allow (Exclude) file:/// scheme from being opened by the extension.

2-Checking Permissions also like (1) and if the extension need to use (tabs.captureVisibleTab) and not to allow file:/// scheme files from being captured.

From there it is easy to create a command and control server( here we can add netcat listner to see using `nc -vlp 8888` at linux terminal) and By the Above Way an attacker could navigate through the file system and fetch arbitrary local files to His C&C Server.

---

**CREDIT INFORMATION**  

Reporter credit: Ahmed ElMasry

---

Thank you for your attention. with kind Regards

## Attachments

- [background.js](attachments/background.js) (text/plain, 1.3 KB)
- [manifest.json](attachments/manifest.json) (text/plain, 352 B)
- [Linux-Extension-PoC.mp4](attachments/Linux-Extension-PoC.mp4) (video/mp4, 7.7 MB)
- [Windows-PoC.mp4](attachments/Windows-PoC.mp4) (video/mp4, 7.3 MB)
- [background.js](attachments/background.js) (text/plain, 1.2 KB)
- [manifest.json](attachments/manifest.json) (text/plain, 352 B)
- [Canary-Arbitary-file-leak- 2022-12-20 16-38-47-957.mp4](attachments/Canary-Arbitary-file-leak- 2022-12-20 16-38-47-957.mp4) (video/mp4, 6.0 MB)
- [Dev-Arbitary-file-leak-2022-12-20 16-40-57-081.mp4](attachments/Dev-Arbitary-file-leak-2022-12-20 16-40-57-081.mp4) (video/mp4, 6.6 MB)

## Timeline

### el...@gmail.com (2022-11-16)

Ooops ,Forget to Add Title For the Report :

Title : Extension with <all_urls> permission can read arbitrary local files although  (Allow access to file URLs) is disabled.

### [Deleted User] (2022-11-16)

[Empty comment from Monorail migration]

### dr...@chromium.org (2022-11-16)

I am able to reproduce this in M107, so setting FoundIn accordingly and triaging like https://bugs.chromium.org/p/chromium/issues/detail?id=810220.

 rdevlin.cronin@ - this seems like a straightforward regression of https://bugs.chromium.org/p/chromium/issues/detail?id=810220

The fix for that bug claims:
- If the page is a file page (file:///), allow the capture if the
  extension has file access *and* either of the <all_urls> or
  activeTab permissions.

And this report has an extension that does not have file access, but can capture a file:// URL.

[Monorail components: Platform>Extensions>API]

### [Deleted User] (2022-11-17)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2022-11-22)

Looks like https://crbug.com/chromium/1385343#c3 aimed to set FoundIn-107. Doing so now. Ideally we'd check if this reproduces in M106 in case we want to merge back to the current Extended Stable branch, but I suspect this won't be fixed in time for 106 to still be extended stable.

### [Deleted User] (2022-11-22)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-23)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-11-29)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-30)

rdevlin.cronin: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@chromium.org (2022-12-01)

[Empty comment from Monorail migration]

### el...@gmail.com (2022-12-06)

Friendly Ping: any further updates on this?


### rd...@chromium.org (2022-12-08)

Thank you for the report!

You raise two issues here:
1) navigating to a file:-scheme URL without file permissions
2) capturing that file URL

Changing 1) isn't so straightforward.  Extensions are generally allowed to create tabs they don't have access to (e.g., I can create an example.com tab, even if I can't access example.com).  This is important for a few different reasons and use cases, such as session / history / bookmark managers (where I wouldn't want a bookmark manager extension to have access to _read_ my local files just because I bookmark a file).  We may discuss this more in the future, but for now, I don't think this is something we'll change.

2), on the other hand, is definitely a bug.  My suspicion is that what's happening is that, while reloading the page, our permission checks get mixed up about what the URL being rendered is.

I won't have time to look into this in the near future.  tjudkins@, you've tackled a few similar cases in the past; do you think this is something you could take a look at?

### [Deleted User] (2022-12-14)

tjudkins: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### el...@gmail.com (2022-12-15)

tjudkins@
Any further updates on this issue?
do you have some empty cycles to work on that case ?
Thanks

### tj...@chromium.org (2022-12-20)

Could you verify if 2 still replicates on a recent canary build? I've been trying to replicate it with some dubugging on a dev build and the lastError for not having access to capture the page is coming through every time with file access disabled.

### el...@gmail.com (2022-12-20)

Hi ..., tjudkins@

Yes it Repro's as Bug Shows before ,i've tested the bug with latest Chrome Canary and DEV , also attached PoC Videos for both Canary Repro, and DEV Repro .

=============
Chrome Version 111.0.5488.0 (Official Build) canary (64-bit)
windows 10 machine
=============
Chrome Version 110.0.5478.4 (Official Build) dev (64-bit)
windows 10 machine
=============
PS. kindly find the attached Poc Videos , also i've attached the extension file again.

### el...@gmail.com (2022-12-20)

[Empty comment from Monorail migration]

### tj...@chromium.org (2022-12-21)

Thanks for checking again, I've been able to narrow this down more. Interestingly this doesn't have to do with the reload and seems to actually be very specific to the order you are doing things in. If file access is removed while the extension is active, the extension is reloaded with the new access and the "Cannot access contents of the page" error occurs as you would expect (event after calling chrome.tabs.reload). However, if the extension is disabled first then file access is removed (as shown in your reproduction video), then when the extension is reenabled it still seems to have file access.

I'll dig into where this process is going wrong and get a CL with a fix up soon.

### gi...@appspot.gserviceaccount.com (2023-01-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/a5e2bf3eaeea3a0f7ba9af687f1ee99014aa26fe

commit a5e2bf3eaeea3a0f7ba9af687f1ee99014aa26fe
Author: Tim Judkins <tjudkins@chromium.org>
Date: Tue Jan 10 01:36:06 2023

[Extensions] Reload extension on changing fileAccess even if disabled

Changes to file access settings for an extension were not being applied
correctly for extensions which were disabled while the setting was
changed. This CL forces a reload of an extension when changing the file
access setting even if it is disabled, to ensure it is reinitialized
correctly. Also adds tests to better cover this case.

Bug: 1385343
Change-Id: I2de208b5e80b715515f613c55bf50b362913d1fa
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4123091
Reviewed-by: Devlin Cronin <rdevlin.cronin@chromium.org>
Commit-Queue: Tim <tjudkins@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1090642}

[modify] https://crrev.com/a5e2bf3eaeea3a0f7ba9af687f1ee99014aa26fe/chrome/browser/extensions/extension_util.cc
[modify] https://crrev.com/a5e2bf3eaeea3a0f7ba9af687f1ee99014aa26fe/chrome/test/BUILD.gn
[add] https://crrev.com/a5e2bf3eaeea3a0f7ba9af687f1ee99014aa26fe/chrome/browser/extensions/extension_util_unittest.cc


### tj...@chromium.org (2023-01-10)

[Empty comment from Monorail migration]

### el...@gmail.com (2023-01-10)

Hi..
I Confirm from my side this issue has been fixed, i've tested the fix on Chrome Canary Version 111.0.5529.0  official Build (64bit) at Windows 10 machine .

Thanks for your time and providing a fix for this issue.

### [Deleted User] (2023-01-10)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-10)

[Empty comment from Monorail migration]

### el...@gmail.com (2023-01-17)

Hi..,

Not sure if the panel already took a look at this report, but I would like to highlight that the impact of this bug was in allowing an attacker to leak local files and send it to Attacker C&C server ,by using an extension that only had the "<all_urls>" permission& (Disabled file access) from extension details page, but due to improper permission implemented the extension can real and crawl all user local files and send to Attacker, referring to what documentation state (File URLs may be captured only if the extension has been granted file access.) under  (captureVisibleTab) part https://developer.chrome.com/docs/extensions/reference/tabs/

For reference, (earlier similar report https://crbug.com/chromium/1176031 ) ,this bug allowed an extension with the "downloads" permission to leak user files to remote attacker , which I would argue has a similar impact to this issue, hope you consider this report as high quality report referencing bounty to the earlier report mentioned at 1176031 , referring to https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules and bounty amount table for high quality report with functional exploit, with information disclosure impact.

Thank you so much for protecting us.

### am...@google.com (2023-01-26)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-01-26)

Congratulations, Ahmed! The VRP Panel has decided to award you $10,000 for this report. Thank you for your efforts in discovering and reporting this issue to us -- great work! 

### el...@gmail.com (2023-01-27)

Awesome!!, Thank you so much Amy for the Reward🙂

### am...@google.com (2023-01-28)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-03-06)

[Empty comment from Monorail migration]

### am...@google.com (2023-03-07)

[Empty comment from Monorail migration]

### pg...@google.com (2023-03-07)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-04-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/daae694a4e92f8c97b0df0947e4cdcc2d0f69b23

commit daae694a4e92f8c97b0df0947e4cdcc2d0f69b23
Author: Tim Judkins <tjudkins@chromium.org>
Date: Tue Apr 11 20:58:51 2023

[Extensions] Use pref value for file access on installed extension load

This CL modifies the logic when loading an installed extension to base
the file access purely on the state of the related pref, rather than
any previously stored creation flags. Normally these should be aligned,
but in case they are not we want to stick to what the pref says as that
is the state we display to the user on the extension management page.

Also expands a related test and adds some more explicit testing for this
mismatch case.

Bug: 1385343, 1432284
Change-Id: I7c45a7a174665ee138c4a7a3fba77b3bbe381508
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4313067
Commit-Queue: Tim <tjudkins@chromium.org>
Reviewed-by: Devlin Cronin <rdevlin.cronin@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1128884}

[modify] https://crrev.com/daae694a4e92f8c97b0df0947e4cdcc2d0f69b23/chrome/browser/extensions/installed_loader.cc
[modify] https://crrev.com/daae694a4e92f8c97b0df0947e4cdcc2d0f69b23/chrome/browser/extensions/extension_service_unittest.cc


### [Deleted User] (2023-04-18)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1385343?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061772)*
