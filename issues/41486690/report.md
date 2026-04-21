# Extension sanitization bypass - Setting file extension as "%%" resorts to the previous text

| Field | Value |
|-------|-------|
| **Issue ID** | [41486690](https://issues.chromium.org/issues/41486690) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | UI>Browser>Downloads |
| **Platforms** | Windows |
| **Reporter** | br...@gmail.com |
| **Assignee** | qi...@chromium.org |
| **Created** | 2023-12-24 |
| **Bounty** | $1,000.00 |

## Description

**Steps to reproduce the problem:**

1. Download both of the attached files.
2. Run this: `python -m http.server --directory C:\Path\To\The\Downloaded\Files --bind 127.0.0.1`
3. Visit localhost.
4. Right click > Save As for Link 1, see that the dangerous extension .lnk gets replaced with .download.
5. Right click > Save As for Link 2, see that the dangerous extension .lnk attempts to get saved.

**Problem Description:**  

We can bypass extension sanitization by taking advantage of these facts:

1. Chrome removes %Data% from the filename
2. Chrome throws away empty file extensions

When clicking 'Save as' on a filename like 'file.lnk' it would get replaced by 'file.download' due to the dangerous nature of the file.

But a filename like 'file.lnk.%%' would bypass the sanitization and turn into 'file.lnk'

This is because the '%%' gets removed due to <https://bugs.chromium.org/p/chromium/issues/detail?id=1308422>  

And the empty extension would get thrown away, resorting to the previous text as the extension

**Additional Comments:**  

I submitted this to bughunters.google.com but I wasn't sure so I uploaded it here too

\*\*Chrome version: \*\* 122.0.0.0 \*\*Channel: \*\* Stable

**OS:** Windows

## Attachments

- [index.html](attachments/index.html) (text/plain, 357 B)
- [download.php](attachments/download.php) (text/plain, 101 B)
- [index.html](attachments/index.html) (text/plain, 1.1 KB)
- [malicious_link.download](attachments/malicious_link.download) (application/octet-stream, 3.4 KB)
- [script.ps1](attachments/script.ps1) (application/octet-stream, 935 B)

## Timeline

### [Deleted User] (2023-12-24)

[Empty comment from Monorail migration]

### br...@gmail.com (2023-12-25)

Affected versions at time of reporting - all
Stable 120.0.6099.129
Beta 121.0.6167.16
Dev 122.0.6205.0

### br...@gmail.com (2023-12-25)

A potential fix would be to add a placeholder when the '%%' is removed

le.
example.scf.%% -> example.scf.placeholder

### br...@gmail.com (2023-12-25)

The previous PoC compared the behavior when downloading dangerous files normally and with bypass and in that example download.php would contain the binary of the lnk file.

I've created a bit more advanced PoC that contains 3 files:
1. index.html 
2. script.ps1
3. malicious_link.download
It poses as a website that hosts the company rules in a word file but it is  in fact an lnk file that executes script.ps1 when opened

To try it out:
1. Download the attached files.
2. Run this: `python -m http.server --directory C:\Path\To\The\Downloaded\Files --bind 127.0.0.1`
3. Visit localhost.

Of course this exploit can do much more harm because it also allows downloading of scf files that allow gathering user hashes with almost no interaction https://nored0x.github.io/red-teaming/smb-share-scf-file-attacks/ but that would be difficult to demonstrate here


### hc...@google.com (2023-12-26)

[Empty comment from Monorail migration]

### hc...@google.com (2023-12-26)

[Empty comment from Monorail migration]

### ts...@chromium.org (2023-12-26)

Assigning and setting severity per previous https://crbug.com/chromium/1308422. Provisionally setting impact based on https://crbug.com/chromium/1514127#c2 and the age of the CL which fixed it, but will I need to verify later.  OS=windows, as the code is windows specific.

[Monorail components: UI>Browser>Downloads]

### [Deleted User] (2023-12-26)

[Empty comment from Monorail migration]

### br...@gmail.com (2023-12-27)

I can confirm that https://chromium.googlesource.com/chromium/src/+/806c5534cf6ca1e42c9537ea8ab756fb57d71e73 is the offending commit.

Bisect Results:

From the continuous build archive:

Latest Chrome Developer Build which did not contain the vulnerability - https://commondatastorage.googleapis.com/chromium-browser-snapshots/index.html?prefix=Win/1066951/
 [Version: 109.0.5399.5 (Developer Build)
Earliest Chrome Developer Build which contains the vulnerability - https://commondatastorage.googleapis.com/chromium-browser-snapshots/index.html?prefix=Win/1067319/
 [Version: 109.0.5400.0 (Developer Build)

This aligns with https://chromium.googlesource.com/chromium/src/+/806c5534cf6ca1e42c9537ea8ab756fb57d71e73 landing in 109.0.5400.0 according to https://storage.googleapis.com/chromium-find-releases-static/806.html#806c5534cf6ca1e42c9537ea8ab756fb57d71e73

### [Deleted User] (2023-12-27)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-12-27)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-12-27)

[Empty comment from Monorail migration]

### br...@gmail.com (2024-01-08)

Hi, any updates? In any case, the fix in https://crbug.com/chromium/1514127#c3 should be easy to implement. Or
allowing the "." to be the extension, like in previous versions would also work.

### [Deleted User] (2024-01-08)

qinmin: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-22)

qinmin: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2024-01-22)

This issue was migrated from crbug.com/chromium/1514127?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1514119, crbug.com/chromium/1514120]
[Monorail components added to Component Tags custom field.]

### br...@gmail.com (2024-02-14)

deleted

### ap...@google.com (2024-03-09)

Project: chromium/src
Branch: main

commit caf79bc86531931bc287cb21769c345af100a8dc
Author: Kovacs Zeteny <brightbulbapp@gmail.com>
Date:   Sat Mar 09 01:30:10 2024

    fix a bug that leads to resorting to potentially dangerous extension
    
    This CL adds a check to make sure the file extension is not "."
    after removing environment variables from filename on windows,
    to avoid extension resorting to previous dangerous extension.
    
    Bug: 41486690
    Change-Id: I9660d501de54734f0d919c2f2bea0d59d363ba67
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5331701
    Reviewed-by: Min Qin <qinmin@chromium.org>
    Commit-Queue: Xinghui Lu <xinghuilu@chromium.org>
    Reviewed-by: Xinghui Lu <xinghuilu@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1270521}

M       AUTHORS
M       chrome/browser/download/download_target_determiner.cc
M       chrome/browser/download/download_target_determiner_unittest.cc

https://chromium-review.googlesource.com/5331701


### br...@gmail.com (2024-03-09)

Hi, if this CL fixes the issue, can this be marked as fixed?
here is the commit: https://chromium.googlesource.com/chromium/src/+/caf79bc86531931bc287cb21769c345af100a8dc

### br...@gmail.com (2024-03-23)

Sorry, I do not mean to nag, but I'm unsure why I still haven't received a response, could you please give a quick update on the situation.

### am...@google.com (2024-04-25)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2024-04-25)

Congratulations! The Chrome VRP Panel has decided to award you $1,000 for this report of exploit mitigation bypass + $1,000 bisect bonus. While this report was not very security impactful, we did very much appreciate that wrote a patch, with a unit test, that you committed to Chromium directly. For this, we have decided to award you a patch bonus of $2,000.
A member of the Google finance p2p-vrp team will be in touch with you soon to arrange payment. In the meantime, please let us know what name/handle you would like us to use in acknowledging you for this finding.

Thank you for your efforts -- especially the patch authoring and submission work -- and reporting this issue to us!

### br...@gmail.com (2024-04-26)

Hello, thank you for your quick response! I do not want my email to be publicly visible, if possible, but it would be nice if you could acknowledge me under the alias "Azur".

### am...@chromium.org (2024-04-26)

Thank you! We don't reveal usernames or email addresses when the report is publicly disclosed (they are obfuscated in the report) nor when acknowledging the reporter for the finding, unless they've explicitly requested that. I've updated our acknowledgements file to ensure you're represented as Azur in public acknowledgements.

### pe...@google.com (2024-07-23)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/41486690)*
