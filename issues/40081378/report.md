# Security: Extensions can silently debug (run code) in ANY tab and escape the sandbox

| Field | Value |
|-------|-------|
| **Issue ID** | [40081378](https://issues.chromium.org/issues/40081378) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>Extensions, Platform>Extensions>API |
| **Reporter** | ro...@robwu.nl |
| **Assignee** | ro...@robwu.nl |
| **Created** | 2015-02-09 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

**Please provide a brief explanation of the security issue.**

The chrome.debugger extension API can attach to targets at any origin, including URLs such as file://, chrome://, chrome-extension:// and the Chrome Web store. Attaching to privileged targets is usually forbidden when the target is specified by tabId or extensionId. However, it is also possible to attach to a target by targetId, which is not subjected to any validation. This targetId can easily be obtained using the chrome.debugger.getTargets method (<https://developer.chrome.com/extensions/debugger#method-getTargets>).

Usually, background extensions cannot be debugged unless --silent-debugger-extension-api is set. However, this limitation can easily be avoided by opening chrome-extension://[extensionid]/manifest.json. This file always exists, and an extension can always open this URL. Hence, any installed extension that has access to juicy APIs can be abused by this bug.

Because of these capabilities, anything that can be displayed in a tab is completely compromised when a user installs an extension that exploits this bug. Here are some severe attacks that can be carried out.  

(When I write "Open X", I mean "Open X in a tab, attach a debugger and run code to realise the remaining steps).

- Chrome OS only: Full system compromise if the user has installed the Secure Shell extension <https://chrome.google.com/webstore/detail/secure-shell/pnhechapfaindjhompbnflcldabbghjo>, which uses the private chrome.terminalPrivate API, which offers direct access to a shell.
- Unconstrained read access to local files:
  
  1. Open chrome://extensions
  2. Enable "Allow access to file URLs":  
     
     chrome.send('extensionSettingsAllowFileAccess', [extensionId, true]);
  3. Use XMLHttpRequest to scrape the disk.
- Query the location of the Chrome binary and user profile directory.
  
  1. Open chrome://version
  2. Scrape the data.
- Write access to local files:
  
  1. Open chrome://settings-frame
  2. Set the download directory to any location:  
     
     chrome.send('setStringPref', ['download.default\_directory', '/home/'])
  3. Use the chrome.downloads.download extension API to save files to any subdirectory:  
     
     chrome.downloads.download({ url: 'data:text/plain,I commited a crime', filename: 'username/confession.txt' });
- Execute random files OUTSIDE THE SANDBOX:
  
  1. Open chrome://settings-frame
  2. Set the download "directory" to a file: chrome.send('setStringPref', ['download.default\_directory', 'C:\\windows\\system32\\notepad.exe'])
  3. Open chrome://downloads
  4. Open the downloads "directory":  
     
     chrome.send('openDownloadsFolder');
- Theft of encryption keys and other sensitive data from extensions:
  
  1. Open chrome-extension://[extensionid]/manifest.json
  2. If the data is hidden at the background page:  
     
     var data = chrome.extension.getBackgroundPage().getTopSecretInformationFromExtension();
  3. If the data is just stored in localStorage, chrome.storage, IndexedDB, FileSystem API or whatever:  
     
     // Invoke any of these APIs to access the data

**VERSION**  

Chrome Version: Chromium 40.0.2214.91, Google Chrome 42.0.2300.0  

Operating System: Linux x64 (but applicable to any OS)

**REPRODUCTION CASE**  

**Please include a demonstration of the security bug, such as an attached**  

**HTML or binary file that reproduces the bug when loaded in Chrome. PLEASE**  

**make the file as small as possible and remove any content not required to**  

**demonstrate the bug.**

I've attached an extension that uses the following permissions:

- "debugger" to get access to the API (required)
- "management" to query the list of installed extensions to find a target for the proof of concept.  
  
  (not necessary in reality, because the list of extensions is also available in chrome.debugger.getTargets)

1. Make sure that you have installed at least one other extension.
2. Load the attached extension.
3. Upon load, it picks another extension and invokes "alert" to open a dialog in the context of another extension.
4. Observe a dialog that is displayed in another extension.

This steps-to-reproduce is safe to run, it proves that there is a vulnerability in the chrome.debugger API. If you want to check whether the other scenarios are true, just open the console and run the shown commands. After all, the chrome.debugger API can do anything what the console is capable of,.

---

Some pointers for resolving the problem:

1. Obviously, check whether the debuggee target should be accessible. That has to be done here:  
   
   <https://chromium.googlesource.com/chromium/src/+/3ef9ec9e43e5e5b7aca6ea935407a469d7b528cf/chrome/browser/extensions/api/debugger/debugger_api.cc#530>
2. The sandbox escape bug can be mitigated by checking whether the "download directory" is really a directory before saving the pref:  
   
   <https://chromium.googlesource.com/chromium/src/+/bfe0fce99e0da81fd9f07bd4cc4e6587cc342046/chrome/browser/download/download_prefs.cc#140>
3. And perhaps also before "opening" it, because the directory might be replaced with a file between setting and using the pref (e.g. due to Sync?).  
   
   <https://chromium.googlesource.com/chromium/src/+/6796a8b5cb45f30c72e64d32261a9e2219d45981/chrome/browser/ui/webui/downloads_dom_handler.cc#558>
4. And also in the chrome.downloads.showDefaultFolder() extension API:  
   
   <https://chromium.googlesource.com/chromium/src/+/1b32ffb4800e222e3a9c92f78081246b02e83ec5/chrome/browser/extensions/api/downloads/downloads_api.cc#1329>

## Attachments

- [manifest.json](attachments/manifest.json) (application/json, 220 B)
- [background.js](attachments/background.js) (text/javascript, 4.1 KB)

## Timeline

### js...@chromium.org (2015-02-09)

rob@ Were you planning on fixnig this one, or do we need to find an owner?

### ro...@robwu.nl (2015-02-09)

I will take it.

(After fixing 1, I want to follow up with a feature request for debugging extensions with user consent, because it would be unfortunate if users cannot debug extension pages due to this fix.)

### [Deleted User] (2015-02-09)

Adding Devlin who has fixed a problem in the debugging API before.

### ro...@robwu.nl (2015-02-09)

I'm already working on a patch. The fix itself is straightforward, writing the tests takes a bit more time.

### me...@chromium.org (2015-02-09)

Nice find. For my own understanding, is this different than https://crbug.com/chromium/367567 because  somehow targetID wasn't checked? tabId, extensionId and targetId seem to be the only three debuggee identifiers, but I'm wondering if it's also possible to use another identifier such as url by some convoluted means.

### ro...@robwu.nl (2015-02-09)

#5 This bug is indeed similar to https://crbug.com/chromium/367567. That bug was fixed by adding validation for tabId/extensionId, but apparently targetId was overlooked.

In the bug you're referring to, there is a link to https://crbug.com/chromium/386988, which shows an exploit similar to the one in my report. Surprisingly, that bug also uses chrome.downloads.showDefaultFolder() to escape the sandbox, but the method is still vulnerable. I assume that not fixing this method is an oversight, so I will also submit a patch to make sure that this method cannot be abused again to escape the sandbox (suggestions 2-4 of my bug report).

### me...@chromium.org (2015-02-09)

The download bug referred in https://crbug.com/chromium/386988 is already being worked on at https://crbug.com/chromium/387037 (restricted), so you don't need to worry about it for now.

### ro...@robwu.nl (2015-02-09)

#7 Could you put me on the cc list of https://crbug.com/chromium/387037?

### me...@chromium.org (2015-02-09)

#8: Done.

### bu...@chromium.org (2015-02-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/409bf9d6104f83c80cd85bd261784b39cab8e93e

commit 409bf9d6104f83c80cd85bd261784b39cab8e93e
Author: rob <rob@robwu.nl>
Date: Tue Feb 10 23:37:07 2015

Validate debuggee.targetId before use in chrome.debugger

And refactored the tests to make sure that the debugger is detached upon
returning from RunAttachFunction. Previously, if the debugger
unexpectedly succeeded in attaching, the method would return (because
empty error != some error), causing the attached debugger to not be
detached.

R=rdevlin.cronin@chromium.org
BUG=456841
TEST=browser_tests DebuggerApiTest.DebuggerNotAllowedOnOtherExtensionPages

Review URL: https://codereview.chromium.org/910053002

Cr-Commit-Position: refs/heads/master@{#315675}

[modify] http://crrev.com/409bf9d6104f83c80cd85bd261784b39cab8e93e/chrome/browser/extensions/api/debugger/debugger_api.cc
[modify] http://crrev.com/409bf9d6104f83c80cd85bd261784b39cab8e93e/chrome/browser/extensions/api/debugger/debugger_apitest.cc


### me...@chromium.org (2015-02-13)

Is there any work remaining? Can we close this as fixed now?

### ro...@robwu.nl (2015-02-13)

The issue is no longer exploitable in M-42, but the other bug (#7) still needs to be fixed. Apparently that is being worked on, so all issues here are resolved.

Given the impact of this bug, a merge to 41 might be justifiable.

And I'd really appreciate an alternative method to debug extensions with explicit user consent, so that this fix does not break the workflow of developers who use the debugging feature for legitimate purposes. Could you run extplorer to see which extensions use the debugger permission, and send the result to me for a quick analysis?

### me...@chromium.org (2015-02-13)

Fix is small enough to merge. I'll see what I can do about other extensions using |debugger| permission.

### pe...@google.com (2015-02-13)

Approved for M41 (branch: 2272)

### cl...@chromium.org (2015-02-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2015-02-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/9768ebe3814ebf553851a5005620c048d5f1e1c6

commit 9768ebe3814ebf553851a5005620c048d5f1e1c6
Author: Rob Wu <rob@robwu.nl>
Date: Fri Feb 20 16:31:43 2015

Validate debuggee.targetId before use in chrome.debugger

And refactored the tests to make sure that the debugger is detached upon
returning from RunAttachFunction. Previously, if the debugger
unexpectedly succeeded in attaching, the method would return (because
empty error != some error), causing the attached debugger to not be
detached.

R=rdevlin.cronin@chromium.org
BUG=456841
TEST=browser_tests DebuggerApiTest.DebuggerNotAllowedOnOtherExtensionPages

Review URL: https://codereview.chromium.org/910053002

Cr-Commit-Position: refs/heads/master@{#315675}
(cherry picked from commit 409bf9d6104f83c80cd85bd261784b39cab8e93e)

Review URL: https://codereview.chromium.org/942103004

Cr-Commit-Position: refs/branch-heads/2272@{#343}
Cr-Branched-From: 827a380cfdb31aa54c8d56e63ce2c3fd8c3ba4d4-refs/heads/master@{#310958}

[modify] http://crrev.com/9768ebe3814ebf553851a5005620c048d5f1e1c6/chrome/browser/extensions/api/debugger/debugger_api.cc
[modify] http://crrev.com/9768ebe3814ebf553851a5005620c048d5f1e1c6/chrome/browser/extensions/api/debugger/debugger_apitest.cc


### ti...@google.com (2015-02-26)

[Empty comment from Monorail migration]

### ti...@google.com (2015-03-03)

Congrats - $1000 for this report.

As a side note, be aware that payment of bugs is always at the discretion of the panel. I mention this as you are in the AUTHORS file for chromium but the panel determined that your access and code changes in this case did not cause a conflict that would prohibit payment.

You'll be listed in the release notes today as "Rob Wu". Thanks!

### ti...@google.com (2015-03-06)

[Empty comment from Monorail migration]

### ti...@google.com (2015-03-17)

Processing via our e-payment system can take up to six weeks, but the reward should be on its way to you. Thanks again for your help!

### cl...@chromium.org (2015-05-22)

Bulk update: removing view restriction from closed bugs.

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### yu...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-06)

This issue was migrated from crbug.com/chromium/456841?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Platform>Extensions, Platform>Extensions>API]
[Monorail blocked-on: crbug.com/chromium/387037]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081378)*
