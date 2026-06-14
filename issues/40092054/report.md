# Security: Kernel Level Memory Leak as a result of GDI object creations

| Field | Value |
|-------|-------|
| **Issue ID** | [40092054](https://issues.chromium.org/issues/40092054) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>Downloads |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **CVE IDs** | CVE-2012-2848 |
| **Reporter** | br...@gmail.com |
| **Assignee** | qi...@chromium.org |
| **Created** | 2018-07-28 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

Steps to reproduce:

1. enable 'select where to save downloads' feature in chrome settings so each file download prompts user for destination directory to save new file.
2. visit <https://script.google.com/macros/s/AKfycbzGfimeGFEvigB66-uW5id2-JeDGmfoNcudh2n2GsVdZ7OxhXm5/exec>

Expected result:  

GDI resource leak causing crash of ; heap based buffer overflow vulnerability; kernel-level memory leak

Opening a url containing octect/pdf data bypasses CORS restrictions, allowing <x>.pdf to be written to victims disk <N> times; no sanity check on the number of GDI object count in Chrome before calling "CreatePlatformCanvas" results in browser crash if user has enabled "select where to save downloads" feature in chrome settings.

Browser crashed with fatal error: "Failed to create DC in BeginPaint(). GLE = 1425, GDI object count: 10000, GDI peak count: 10001"

**VERSION**  

Browser/OS(s):

Win32 Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134

Win32 Mozilla Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/65.0.3325.181

MacIntel Mozilla Mozilla/5.0 (Macintosh; Intel Mac OS X 10\_13\_6) AppleWebKit/537.36 (KHTML like Gecko) Chrome/65.0.3325.181

Win32 Mozilla Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/67.0.3396.99

**REPRODUCTION CASE**

active web-app: <https://script.google.com/macros/s/AKfycbzGfimeGFEvigB66-uW5id2-JeDGmfoNcudh2n2GsVdZ7OxhXm5/exec>

video: <https://youtu.be/m9SD_7e-dQs>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: browser

Local Crash IDs:  

02d1dc60-fdf3-45d4-81ff-990ff8c1b7de  

e2102c48-254c-4ff4-83a9-bdc6cd19aa1c

## Attachments

- [issue_111617701.log](attachments/issue_111617701.log) (text/plain, 15.7 KB)

## Timeline

### mb...@chromium.org (2018-07-30)

Tentatively setting low severity for consistency with https://crbug.com/chromium/127522, but I'm a bit torn since it does require that the user accept a permission prompt to download multiple files.

The crash certainly isn't ideal, but we generally don't consider denial of service to be a vulnerability. More information on that at https://chromium.googlesource.com/chromium/src/+/master/docs/security/faq.md#Are-denial-of-service-issues-considered-security-bugs

qinmin, dtrainor: Are either of you the right people to take a look at this? Feel free to close if you don't think there's much that can be done here, or pass it back to me for re-triage if necessary.



[Monorail components: UI>Browser>Downloads]

### sh...@chromium.org (2018-07-31)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-08-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/b7fa845960fcf21001dbd3adf409e5c19046e4eb

commit b7fa845960fcf21001dbd3adf409e5c19046e4eb
Author: Min Qin <qinmin@chromium.org>
Date: Wed Aug 01 21:45:06 2018

Fix an DOS issue using download prompt dialog

This CL changes the behavior to show dialog one by one,
not showing all of them at once.
This CL also fixes an issue that DownloadFilePicker is not
deleted in some cases.

BUG=868619

Change-Id: I71958b8c8d1383d95996d00c58c84c5523e08bd1
Reviewed-on: https://chromium-review.googlesource.com/1157141
Commit-Queue: Min Qin <qinmin@chromium.org>
Reviewed-by: Xing Liu <xingliu@chromium.org>
Cr-Commit-Position: refs/heads/master@{#579955}
[modify] https://crrev.com/b7fa845960fcf21001dbd3adf409e5c19046e4eb/chrome/browser/download/chrome_download_manager_delegate.cc
[modify] https://crrev.com/b7fa845960fcf21001dbd3adf409e5c19046e4eb/chrome/browser/download/chrome_download_manager_delegate.h
[modify] https://crrev.com/b7fa845960fcf21001dbd3adf409e5c19046e4eb/chrome/browser/download/download_file_picker.cc
[modify] https://crrev.com/b7fa845960fcf21001dbd3adf409e5c19046e4eb/chrome/browser/download/download_test_file_activity_observer.cc


### qi...@chromium.org (2018-08-01)

Changed the implementation to show only 1 file selection dialog at a time, this should solve the issue 

### sh...@chromium.org (2018-08-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-08-08)

[Empty comment from Monorail migration]

### aw...@google.com (2018-08-13)

Thanks for the report! I'm afraid, however, that the VRP declined to reward for this bug.

### br...@gmail.com (2018-08-13)

Do the changes get merged into the stable version of Chrome though?

Will this report go on the list of security fixes in the next release as "n/a", while still mentioning what was fixed?

### br...@gmail.com (2018-08-16)

For CVE-2012-2848, you guys decided to reward a low impact security bug with the following comment:

"The panel decided to award $500 for this bug. The bug itself has little security value, but the fix is a good hardening measure. Thanks!"

https://bugs.chromium.org/p/chromium/issues/detail?id=127525

I know that was in the early stages of the rewards program, but is there any possibility for this report to also be reconsidered based on "the fix being a good hardening measure"?





### sh...@chromium.org (2018-11-08)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2018-11-08)

This issue was migrated from crbug.com/chromium/868619?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092054)*
