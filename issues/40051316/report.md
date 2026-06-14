# Security: Possible to bypass restrictions on multiple downloads by initiating download from data: frame

| Field | Value |
|-------|-------|
| **Issue ID** | [40051316](https://issues.chromium.org/issues/40051316) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>Downloads |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | de...@gmail.com |
| **Assignee** | qi...@chromium.org |
| **Created** | 2020-01-21 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

Typically it's not possible for a page to download more than one file without further user interaction. However, by initiating a download from an opaque origin, a page can, in certain circumstances, download multiple files.

**VERSION**  

Chrome Version: Tested on 79.0.3945.130 (stable) and 81.0.4034.0 (canary)  

Operating System: Windows 10, version 1909

**REPRODUCTION CASE**

1. Open index.html.
2. This page will initiate a download of an empty text file, one download every 5 seconds.

Some explanation of that's happening:

If on a page you have a data: sub-frame that performs the following steps:

var newWindow = open();  

newWindow.location.href = "...url-to-download-file...";

The frame will be able to download multiple files without any restrictions.

From some testing, this won't work if the frame tries to download multiple files by setting its own location, or that of its parent. It also won't work if the new window the frame opens points to a regular http/https page (it has to be something like about:blank).

However, going through the above steps would likely mean that the user would have to interact with the page first (e.g. by clicking it), so that the page could successfully call window.open.

In the demonstration, there's no user interaction required, because the page changes its visible URL to about:blank (there are some comments in main.js that explain this). A data: frame on the page will then be able to download multiple files without any restrictions.

**CREDIT INFORMATION**  

Reporter credit: David Erceg

## Attachments

- [index.html](attachments/index.html) (text/plain, 203 B)
- [main.js](attachments/main.js) (text/plain, 1.0 KB)

## Timeline

### es...@chromium.org (2020-01-21)

Downloads folks, could you please take a look and see if this is working as intended or not? Thanks!

[Monorail components: UI>Browser>Downloads]

### es...@chromium.org (2020-01-22)

Tentatively triaging as Low severity, though I'm not sure this should be tracked as a security bug, and would still like to hear from downloads people on whether this is a known issue or not.

### sh...@chromium.org (2020-01-22)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### dt...@chromium.org (2020-01-23)

Min can you take a look?  Thanks!

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-02-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/220ecb7e354511f3c457d99841a9c09ac3964995

commit 220ecb7e354511f3c457d99841a9c09ac3964995
Author: Min Qin <qinmin@chromium.org>
Date: Tue Feb 11 18:59:47 2020

Fix an issue that opaque origin triggered download is not throttled

If a download is triggered by opaque origin, currently we create an origin
from main WebContents' URL to determine if the download should be blocked.
However, if main WebContents' URL is also an opaque origin, the newly
created origin will be different from the previous origin. And making
the download always allowed.
This CL fixes the issue by using the originating opaque origin instead
if the WebContents' origin is opaque. An alternative solution is to
assign a dedicated opaque origin to the main WebContents.

BUG=1044277

Change-Id: Ia38280f4237ba5cd35c7afcf350734833fb9d002
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2048843
Commit-Queue: Min Qin <qinmin@chromium.org>
Reviewed-by: Xing Liu <xingliu@chromium.org>
Cr-Commit-Position: refs/heads/master@{#740375}

[modify] https://crrev.com/220ecb7e354511f3c457d99841a9c09ac3964995/chrome/browser/download/download_request_limiter.cc
[modify] https://crrev.com/220ecb7e354511f3c457d99841a9c09ac3964995/chrome/browser/download/download_request_limiter_unittest.cc


### qi...@chromium.org (2020-02-11)

[Empty comment from Monorail migration]

### [Deleted User] (2020-02-15)

[Empty comment from Monorail migration]

### na...@google.com (2020-02-18)

[Empty comment from Monorail migration]

### na...@google.com (2020-02-20)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-02-20)

Congrats! The Panel decided to award $500 for this report

### na...@google.com (2020-02-20)

[Empty comment from Monorail migration]

### ad...@google.com (2020-05-15)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-05-18)

[Empty comment from Monorail migration]

### [Deleted User] (2020-05-20)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@chromium.org (2020-05-21)

[Empty comment from Monorail migration]

### qi...@chromium.org (2021-09-24)

[Empty comment from Monorail migration]

### is...@google.com (2021-09-24)

This issue was migrated from crbug.com/chromium/1044277?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1055073]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40051316)*
