# UaF outside the sandbox (Print in onunload)

| Field | Value |
|-------|-------|
| **Issue ID** | [40086976](https://issues.chromium.org/issues/40086976) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | Internals>Printing |
| **Platforms** | Linux, Windows |
| **Reporter** | wa...@gmail.com |
| **Assignee** | th...@chromium.org |
| **Created** | 2017-03-06 |
| **Bounty** | $9,337.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36

Steps to reproduce the problem:
1. Open http://localhost/poc.html

What is the expected behavior?
No crash should occur.

What went wrong?
When the cross process navigation occurs, the onunload event of the iframe calls print() and PrintPreviewHandler::HandleGetPreview is called and manipulates freed memory (see stacktrace.txt).

This bug is in the browser process, outside the sandbox.

Did this work before? N/A 

Chrome version: 56.0.2924.87  Channel: stable
OS Version: 6.1 (Windows 7, Windows Server 2008 R2)
Flash Version:


## Attachments

- [poc.zip](attachments/poc.zip) (application/octet-stream, 2.8 KB)
- [698622_Mar_28.ogv](attachments/698622_Mar_28.ogv) (video/ogg, 783.5 KB)

## Timeline

### cl...@chromium.org (2017-03-06)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5314343278477312

### cl...@chromium.org (2017-03-06)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5808830782111744

### el...@chromium.org (2017-03-06)

This sounds similar to https://crbug.com/chromium/646671

### va...@chromium.org (2017-03-06)

dcheng@ -- do you want to take a stab at this or help find the owner?
thestig@ -- your CL touched that line last: http://crrev.com/2508923003

[Monorail components: Internals>Printing]

### va...@chromium.org (2017-03-06)

[Empty comment from Monorail migration]

### cl...@chromium.org (2017-03-07)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5314343278477312

Job Type: linux_asan_chrome_mp
Crash Type: Heap-use-after-free READ 8
Crash Address: 0x61a00009fc88
Crash State:
  PrintPreviewHandler::HandleGetPreview
  content::WebUIImpl::ProcessWebUIMessage
  bool IPC::MessageT<ViewHostMsg_WebUISend_Meta, std::__1::tuple<GURL, std::__1::b
  
Sanitizer: address (ASAN)

Recommended Security Severity: Critical

Reproducer Testcase: https://cluster-fuzz.appspot.com/download/AMIfv978LCtynPSNHrJmwFLvN_iGTF0JhMNfDZcyecn9cXI8_1-ecgLZjKkHFu8qrc7xjFTY-pFUAQY_sCo6BarVQ_tGKLW_4VseqH4IyMPyGfbsDozSprLVCM8kxFo27xGLETnb0J3uIH9x0MmrreJWa3I7iRZ2MSbFnF6x3Mdriykete3VNE0xWZZG2ptD08p0d12r0MxKZ_ODhpeKfXVGmr47u_zC4f1ZC0AIKzQEi9ERMvobSqQ1tcUyykaUSylA_cIrJQffRlyYUcGUGZZ6cLdhtmMWJFdRgT01o65lkXkUQfn1RmMWNNSw5MMxYcAbSi2kwKJW1BzYKRUbqMrcsB6ziIvRvseit6amcUt_K_ewoNCrOuo?testcase_id=5314343278477312


See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

A recommended severity was added to this bug. Please change the severity if it is inaccurate.


### sh...@chromium.org (2017-03-07)

[Empty comment from Monorail migration]

### th...@chromium.org (2017-03-08)

This looks like https://crbug.com/chromium/694382, actually.

### th...@chromium.org (2017-03-10)

[Empty comment from Monorail migration]

### ts...@chromium.org (2017-03-14)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-03-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/746da1cc6b2fbc2f725934542eedc49b41e5f17b

commit 746da1cc6b2fbc2f725934542eedc49b41e5f17b
Author: thestig <thestig@chromium.org>
Date: Thu Mar 16 06:18:21 2017

Properly clean up in PrintViewManager::RenderFrameCreated().

BUG=694382,698622

Review-Url: https://codereview.chromium.org/2742853003
Cr-Commit-Position: refs/heads/master@{#457363}

[modify] https://crrev.com/746da1cc6b2fbc2f725934542eedc49b41e5f17b/chrome/browser/printing/print_view_manager.cc
[add] https://crrev.com/746da1cc6b2fbc2f725934542eedc49b41e5f17b/chrome/browser/printing/print_view_manager_unittest.cc
[modify] https://crrev.com/746da1cc6b2fbc2f725934542eedc49b41e5f17b/chrome/test/BUILD.gn


### cr...@chromium.org (2017-03-16)

Note for release managers: This bug also causes https://crbug.com/chromium/702085, where users of the PDF Viewer extension will have all navigations and network requests fail if they click Back while the extension's print preview dialog is open (until Chrome restarts or the extension process is killed or restarted).  I assume it will be merged anyway due to the critical severity (which thestig@ confirmed), but I just wanted to note the additional impact in case it affects respin decisions.

### th...@chromium.org (2017-03-17)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-03-18)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-03-20)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-03-20)

Your change meets the bar and is auto-approved for M58. Please go ahead and merge the CL to branch 3029 manually. Please contact milestone owner if you have questions.
Owners: amineer@(Android), cmasso@(iOS), bhthompson@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### th...@chromium.org (2017-03-20)

M58 merge from last week: https://chromium.googlesource.com/chromium/src/+/23107311dcb2bc1ecfa1c0fbe63f5f210c154049

### aw...@google.com (2017-03-21)

[Empty comment from Monorail migration]

### th...@chromium.org (2017-03-22)

I haven't seen any bug reports related to the merge on M58+, so requesting a M57 merge.

### go...@chromium.org (2017-03-22)

+awhalley@ for M57 merge review.

### go...@chromium.org (2017-03-22)

[Empty comment from Monorail migration]

### aw...@google.com (2017-03-25)

govind@ - got 3 days of beta coverage from #17, looks good for 57

### go...@chromium.org (2017-03-25)

Approving merge to M57 branch 2987 based on https://crbug.com/chromium/698622#c12, #19 and #22. Please merge before 4:00 PM PT Monday (03/27). Thank you.

### bu...@chromium.org (2017-03-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/8839f8f3d22dc169ede6edad06d75735dbf3c34a

commit 8839f8f3d22dc169ede6edad06d75735dbf3c34a
Author: Lei Zhang <thestig@chromium.org>
Date: Mon Mar 27 03:40:04 2017

M57: Properly clean up in PrintViewManager::RenderFrameCreated().

BUG=694382,698622

Review-Url: https://codereview.chromium.org/2742853003
Cr-Commit-Position: refs/heads/master@{#457363}
(cherry picked from commit 746da1cc6b2fbc2f725934542eedc49b41e5f17b)

Review-Url: https://codereview.chromium.org/2775133002 .
Cr-Commit-Position: refs/branch-heads/2987@{#881}
Cr-Branched-From: ad51088c0e8776e8dcd963dbe752c4035ba6dab6-refs/heads/master@{#444943}

[modify] https://crrev.com/8839f8f3d22dc169ede6edad06d75735dbf3c34a/chrome/browser/printing/print_view_manager.cc
[add] https://crrev.com/8839f8f3d22dc169ede6edad06d75735dbf3c34a/chrome/browser/printing/print_view_manager_unittest.cc
[modify] https://crrev.com/8839f8f3d22dc169ede6edad06d75735dbf3c34a/chrome/test/BUILD.gn


### go...@chromium.org (2017-03-27)

[Empty comment from Monorail migration]

### go...@chromium.org (2017-03-27)

[Empty comment from Monorail migration]

### aw...@google.com (2017-03-28)

[Empty comment from Monorail migration]

### du...@chromium.org (2017-03-28)

Verified the issue on Win 10 and Ubuntu 14.04 using 58.0.3029.40 & 57.0.2987.130 and its working fine.

### aw...@google.com (2017-03-28)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-03-31)

[Empty comment from Monorail migration]

### aw...@google.com (2017-03-31)

Very nice!  The panel decided to award $8,000 for this bug, and also award a $1,337 bonus! (though they noted the initial report was rather bare - see g.co/ChromeBugRewards for what we consider a high quality report).  Thanks!

### aw...@chromium.org (2017-03-31)

[Empty comment from Monorail migration]

### wa...@gmail.com (2017-04-01)

Thanks for the award and thanks for the bonus :)

### sh...@chromium.org (2017-06-24)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/698622?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40086976)*
