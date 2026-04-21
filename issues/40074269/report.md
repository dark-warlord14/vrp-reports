# Security: Extension has access to a custom NTP

| Field | Value |
|-------|-------|
| **Issue ID** | [40074269](https://issues.chromium.org/issues/40074269) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Platform>Extensions |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | fa...@gmail.com |
| **Assignee** | da...@google.com |
| **Created** | 2023-10-06 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

This vulnerability is similar to [crbug.com/1428743](https://crbug.com/1428743)

When a victim is using other search engines as address bar, for example, bing/yahoo, the extension can execute JavaScript on the WebUI at chrome://newtab

**VERSION**  

Chrome Version: 117.0.5938.134 (Official Build) (64-bit) (cohort: Control)

**REPRODUCTION CASE**

1. Load the attached extension.
2. Observe that using both methods mentioned below, the extension can execute scripts to WebUI.

**CREDIT INFORMATION**  

Reporter credit: Shaheen Fazim

## Attachments

- [devtool-demo.mp4](attachments/devtool-demo.mp4) (video/mp4, 6.5 MB)
- [devtools.js](attachments/devtools.js) (text/plain, 94 B)
- [background.js](attachments/background.js) (text/plain, 48 B)
- [manifest.json](attachments/manifest.json) (text/plain, 181 B)
- [devtools.html](attachments/devtools.html) (text/plain, 35 B)
- [debugger-demo.mp4](attachments/debugger-demo.mp4) (video/mp4, 725.5 KB)
- [background.js](attachments/background.js) (text/plain, 441 B)
- [manifest.json](attachments/manifest.json) (text/plain, 178 B)
- [Screenshot 2023-10-10 at 9.51.54 AM.png](attachments/Screenshot 2023-10-10 at 9.51.54 AM.png) (image/png, 1021.7 KB)

## Timeline

### [Deleted User] (2023-10-06)

[Empty comment from Monorail migration]

### fa...@gmail.com (2023-10-06)

Using Chrome Devtool API:


### fa...@gmail.com (2023-10-06)

Using Chrome Debugger API:


### wf...@chromium.org (2023-10-06)

Thanks for your report. At first glance it does appear that extensions should not be able to script webui as stated in the extensions faq [1] "Automating WebUI or settings," ... "should not be possible for an extension with the debugger permission." but it's not clear to me whether simply opening a new tab here is getting the extension any privilege.

I'm going to pass this to the extensions folks to take a closer look, while I check that I can repro this issue locally...

[1] - https://chromium.googlesource.com/chromium/src/+/HEAD/extensions/docs/security_faq.md#what-privileges-does-the-debugger-permission-grant-an-extension_what-privileges-should-it-lack

[Monorail components: Platform>Extensions]

### wf...@chromium.org (2023-10-06)

[Empty comment from Monorail migration]

### wf...@chromium.org (2023-10-07)

[Empty comment from Monorail migration]

### jk...@google.com (2023-10-10)

The main difference between this bug and https://crbug.com/chromium/1428743 is that custom NTP does not have access to Mojo JS. And therefore, it does not have access to NTP modules[1].

However, it does have access to `chrome.embeddedSearch` API (see attached image), which at least have access to the most visited sites.

[1] https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/new_tab_page/modules/

### kr...@chromium.org (2023-10-10)

Solomon: Devlin seems busy so assigning to you.

I'm giving it medium based on A bug that allows an attacker to reliably read or infer browsing history (381808).

It can probably be found before 120, if you find the code causing this please update.

### [Deleted User] (2023-10-10)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-11)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-10-11)

[Empty comment from Monorail migration]

### so...@chromium.org (2023-10-12)

I'm planning on trying to reproduce this bug this week.

### [Deleted User] (2023-10-12)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rd...@chromium.org (2023-10-12)

dsv@, caseq@: looks like another instance where our debugging / devtools security checks aren't quite the same as our other APIs (where we properly disallow things like script injection from occurring).  Mind taking a look?

Security folks: Typically, for exploits involving extensions, we'd downgrade the severity by one level because it requires getting the user to install the malicious extension (either local access or significant social engineering or getting through our webstore review process, etc).  With that in mind and based on https://crbug.com/chromium/1490521#c8, I think we can probably put this as Low and remove RBS, but I'll let dsv@ and caseq@ chime in there and adjust if they feel appropriate.

### ds...@chromium.org (2023-10-16)

This is because custom NTP has a regular URL (e.g. https://www.bing.com/chrome/newtab) and it is a process flag that enables access to chrome.embeddedSearch.

It looks like extensions code is correctly handling this already at https://source.chromium.org/chromium/chromium/src/+/main:chrome/renderer/extensions/renderer_permissions_policy_delegate.cc;l=37;drc=f5bdc89c7395ed24f1b8d196a3bdd6232d5bf771;bpv=1;bpt=1

But this doesn't affect devtools extensions. Before I start investigate, maybe others know why is that?

### be...@google.com (2023-10-16)

Adding Hotlist-RBS-Removed for tracking purposes.

### rd...@chromium.org (2023-10-19)

> But this doesn't affect devtools extensions. Before I start investigate, maybe others know why is that?

Do you mean "is this intentional"?  I don't think so.  As for the underlying cause, I think it's because the check is in the renderer and works for the PermissionsData methods, but I think the majority of devtools and debugger API checks happen in the browser (e.g., the debugger one happens here [1]; I'm honestly not sure where all the devtools ones occur...)

[1] https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/extensions/api/debugger/debugger_api.cc;l=103-133;drc=724a6d19c3955f42acbea9bd9bcc6c5d9611bc53

### [Deleted User] (2023-11-01)

[Empty comment from Monorail migration]

### fa...@gmail.com (2023-11-20)

[Comment Deleted]

### fa...@gmail.com (2023-11-20)

Hi friendly ping, can we use [1] to fix debugger part of this issue so we can move forward, and open a different issue for devtool.Thank you.

### ds...@chromium.org (2023-11-21)

A custom NTP is not a Web UI, it has a regular URL.  The chrome.embeddedSearch API is exposed based on the instant render process flag [1] which is not available to DevTools. crrev.com/c/5048835 is blocking the entire origin for devtools extensions, which is the best mitigation I can think of.


[1]: https://source.chromium.org/chromium/chromium/src/+/main:chrome/common/chrome_switches.cc;l=368?q=switches::kInstantProcess

### ca...@chromium.org (2023-11-21)

So we're not really exposing anything beyond what an extension with a history permission would get in this case, right? Does not look to be much of a security issue IMO.


### gi...@appspot.gserviceaccount.com (2023-11-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/20887af5aa233d772aa38dcb48231af1e481f47c

commit 20887af5aa233d772aa38dcb48231af1e481f47c
Author: Danil Somsikov <dsv@chromium.org>
Date: Tue Nov 21 19:21:20 2023

Do not allow devtools extensions on remote new tab page origins

Bug: 1490521
Change-Id: I174e0b23861ef3464d72aaf5b0563ce27bab4131
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5048835
Reviewed-by: Andrey Kosyakov <caseq@chromium.org>
Auto-Submit: Danil Somsikov <dsv@chromium.org>
Commit-Queue: Andrey Kosyakov <caseq@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1227524}

[modify] https://crrev.com/20887af5aa233d772aa38dcb48231af1e481f47c/chrome/browser/devtools/devtools_browsertest.cc
[modify] https://crrev.com/20887af5aa233d772aa38dcb48231af1e481f47c/chrome/browser/devtools/devtools_ui_bindings.cc


### ds...@chromium.org (2023-11-22)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-11-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/devtools/devtools-frontend/+/37fef4ee2f5b9915eef66b34673fefa55420fb3b

commit 37fef4ee2f5b9915eef66b34673fefa55420fb3b
Author: Danil Somsikov <dsv@chromium.org>
Date: Wed Nov 22 08:12:00 2023

Also disallow devtools extensions on chrome-search:// scheme.

This has some extra API available similar to a remote NTP.

Bug: 1490521
Change-Id: Ibb6448f62c5af1d4a3ce00ac15e44f2a37229c02
Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/5052780
Reviewed-by: Philip Pfaffe <pfaffe@chromium.org>
Commit-Queue: Philip Pfaffe <pfaffe@chromium.org>
Auto-Submit: Danil Somsikov <dsv@chromium.org>

[modify] https://crrev.com/37fef4ee2f5b9915eef66b34673fefa55420fb3b/front_end/models/extensions/ExtensionServer.ts
[modify] https://crrev.com/37fef4ee2f5b9915eef66b34673fefa55420fb3b/test/unittests/front_end/models/extensions/ExtensionServer_test.ts


### [Deleted User] (2023-11-22)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-22)

[Empty comment from Monorail migration]

### am...@google.com (2023-11-30)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-11-30)

Congratulations Shaheen! The Chrome VRP Panel has decided to award you $2,000 for this report of user information disclosure. Thank you for your efforts and reporting this issue to us! 

### fa...@gmail.com (2023-11-30)

Thank you.

### am...@google.com (2023-11-30)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1490521?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-02-29)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40074269)*
