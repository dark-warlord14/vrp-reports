# Security: Lackluster "File System Access API" block-list provides full disk read/write access

| Field | Value |
|-------|-------|
| **Issue ID** | [40059686](https://issues.chromium.org/issues/40059686) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>Storage>FileSystem |
| **Platforms** | Windows |
| **Reporter** | ha...@gmail.com |
| **Assignee** | ds...@chromium.org |
| **Created** | 2022-05-18 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

The "File System Access API"'s block-list on sensitive system locations protecting "FileSystemFileHandle" calls is lackluster and can be bypassed, allowing Chromium to read/write arbitrarily to a users disk.  

On Windows, passing "C:" to "window.showOpenFilePicker()" is prevented with the warning: "can't open this folder because it contains system files" due to the Chromium block-list:  

<https://chromium.googlesource.com/chromium/src/+/refs/heads/master/chrome/browser/file_system_access/chrome_file_system_access_permission_context.cc#154>  

However, by using UNC path aliases such as "\localhost\C$", users can be socially engineered into sharing their entire disk with a malicious site.  

This access provides threat actors arbitrary read/write access allowing for instance: reading credentials, planting malware / ransomware by writing code to e.g user startup folders, altering chromium settings etc...  

Similar bypasses are likely present on other platforms as well, if not for full disk access, but other sensitive locations e.g "~/.bash\_history" on Linux.

**VERSION**  

Chrome Version: 101.0.4951.67 (Official Build) (64-bit) (cohort: Stable)  

Microsoft Edge Version: 101.0.1210.47 (Official build) (64-bit)  

Operating System: Microsoft Windows 10 Enterprise 10.0.19044 N/A Build 19044

**REPRODUCTION CASE**  

See attached .html additionally available live at: <https://harrisonm.com/browser2c> (assumes Windows with Chrome/Edge)

SUGGESTED FIX  

If possible, move to a "allow-list" rather than a "block-list" approach, and consider only allowing user environment folders and below e.g "C:\Users\Username" (or OS equivalent). Alternatively, greater scrutinise the block-list and consider excluding file shares e.g "\host\share" (or OS equivalent) and other known sensitive locations.

**CREDIT INFORMATION**  

Reporter credit: [harrison.mitchell@cybercx.com.au](mailto:harrison.mitchell@cybercx.com.au) / harrisonm.com

## Attachments

- [browser2c.html](attachments/browser2c.html) (text/plain, 2.3 KB)

## Timeline

### [Deleted User] (2022-05-18)

[Empty comment from Monorail migration]

### ke...@chromium.org (2022-05-18)

Thanks for the report.

asully@: Can you have a look at this or reassign?

[Monorail components: Blink>Storage>FileSystem]

### [Deleted User] (2022-05-18)

[Empty comment from Monorail migration]

### as...@chromium.org (2022-05-18)

+mek for more context on the blocklist. Did we ever consider an allowlist?

### me...@chromium.org (2022-05-19)

In one of the earlier security focused design docs for this feature (https://docs.google.com/document/d/1v5_DoJm7TpmQJkE2dbUDX6ecDZtK7aA2DJAH8Y8WsvQ/edit?usp=sharing) I wrote "We should reserve this kind of extreme blocklist for very rare cases. If a user very explicitly wants to edit a certain file with a web app, we should probably just let them." which seem to get agreement from the security team.

The list was really meant more as a way to reduce accidental sharing of "too much" or "too sensitive" data, rather than as a way to make it impossible to do things. Using this API for websites to interoperate with other native applications wouldn't work particularly well if we forced users to store their data in specific directories/places.

Having said that, it might be good to do some kind of path normalization before comparing against the block list, although I somehow doubt we'd be able to do normalization that fully blocks access in every way to these paths. Also, if you can convince a user to select a particular file or directory with the file system access API, you can just as well convince the user to do the same for <input type=file> giving the website just as much (read-only) access. And for write access we have safe browsing and mark-of-the-web/quarantine that is supposed to protect against malware etc.

### ha...@gmail.com (2022-09-13)

👋 Registering intention to publicly disclose.

### me...@chromium.org (2022-09-22)

[Empty comment from Monorail migration]

### ds...@chromium.org (2022-09-22)

[Empty comment from Monorail migration]

### ay...@chromium.org (2022-09-22)

[Empty comment from Monorail migration]

### as...@chromium.org (2022-09-30)

We should normalize the UNC path to a full file path before checking it against the blocklist

Also, to those who discussed this recently, should we mark https://crbug.com/chromium/1358458 as a dup of this bug?

### ds...@chromium.org (2022-10-03)

[Empty comment from Monorail migration]

### ds...@chromium.org (2022-10-03)

Marked as duplicate. Starting on the fix patch.

### gi...@appspot.gserviceaccount.com (2022-11-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/915abdbb04e2d71e288a87786a5293a83080db37

commit 915abdbb04e2d71e288a87786a5293a83080db37
Author: Daseul Lee <dslee@chromium.org>
Date: Tue Nov 01 16:02:36 2022

[FSA] Reject UNC paths from the file and directory pickers on Windows

Currently, there is no feasible way to resolve various types of UNC paths into a canonicalized path that can be checked against the existing blocklist. In order to avoid bypassing the blocklist, UNC paths will be blocked on open*Picker() FSA API.

Bug: 1326788
Change-Id: Ie5ad0db9a680fe5629f566228c727e4e819a15ce
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3993498
Reviewed-by: Austin Sullivan <asully@chromium.org>
Commit-Queue: Daseul Lee <dslee@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1065960}

[modify] https://crrev.com/915abdbb04e2d71e288a87786a5293a83080db37/chrome/browser/file_system_access/chrome_file_system_access_permission_context_unittest.cc
[modify] https://crrev.com/915abdbb04e2d71e288a87786a5293a83080db37/chrome/browser/file_system_access/chrome_file_system_access_permission_context.cc


### ds...@chromium.org (2022-11-04)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-04)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-04)

[Empty comment from Monorail migration]

### am...@google.com (2022-11-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-11-11)

Congratulations, Harrison! The VRP Panel has decided to award you $1,000 for this report. A member of our finance team will be in touch with you soon to arrange payment. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2022-11-11)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-01-09)

[Empty comment from Monorail migration]

### am...@google.com (2023-01-10)

[Empty comment from Monorail migration]

### pg...@google.com (2023-01-10)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-02-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/01d8e55690c9f59f58c5ae1361d707f08a33be51

commit 01d8e55690c9f59f58c5ae1361d707f08a33be51
Author: Daseul Lee <dslee@chromium.org>
Date: Mon Feb 06 18:20:53 2023

[FSA] Update UNC path rejection to only local UNC path on Windows.

The previous check `PathIsUNC()` was too broad and included both external/network UNC path as well as local UNC path (i.e. "\\LOCALHOST\c$\..."). As we want to avoid different variants of "local" UNC from bypassing the blocklist check (and that we currently do not have any blocklist on external path), external UNC path will be allowed again with this change. Unfortunately, there is no complete way to normalize different variations of Windows path, so we use some heuristics by checking (1) UNC root via `base::FilePath::IsNetwork()`, (2) hostname, which may represent local system and (3) `$` character in share name.

Bug: 1326788, 1408321
Change-Id: I030b2719781ac21a145ceb83ce53e7f129b4ce2f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4200953
Reviewed-by: Austin Sullivan <asully@chromium.org>
Commit-Queue: Daseul Lee <dslee@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1101673}

[modify] https://crrev.com/01d8e55690c9f59f58c5ae1361d707f08a33be51/chrome/browser/file_system_access/chrome_file_system_access_permission_context.h
[modify] https://crrev.com/01d8e55690c9f59f58c5ae1361d707f08a33be51/chrome/browser/file_system_access/chrome_file_system_access_permission_context_unittest.cc
[modify] https://crrev.com/01d8e55690c9f59f58c5ae1361d707f08a33be51/chrome/browser/file_system_access/chrome_file_system_access_permission_context.cc


### gi...@appspot.gserviceaccount.com (2023-02-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/0f9b05df02296253562df4d3155fb9e79ea7927b

commit 0f9b05df02296253562df4d3155fb9e79ea7927b
Author: Daseul Lee <dslee@chromium.org>
Date: Mon Feb 06 18:32:14 2023

Revert "[FSA] Update UNC path rejection to only local UNC path on Windows."

This reverts commit 01d8e55690c9f59f58c5ae1361d707f08a33be51.

Reason for revert: Missed using CharType instead of char.

Original change's description:
> [FSA] Update UNC path rejection to only local UNC path on Windows.
>
> The previous check `PathIsUNC()` was too broad and included both external/network UNC path as well as local UNC path (i.e. "\\LOCALHOST\c$\..."). As we want to avoid different variants of "local" UNC from bypassing the blocklist check (and that we currently do not have any blocklist on external path), external UNC path will be allowed again with this change. Unfortunately, there is no complete way to normalize different variations of Windows path, so we use some heuristics by checking (1) UNC root via `base::FilePath::IsNetwork()`, (2) hostname, which may represent local system and (3) `$` character in share name.
>
> Bug: 1326788, 1408321
> Change-Id: I030b2719781ac21a145ceb83ce53e7f129b4ce2f
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4200953
> Reviewed-by: Austin Sullivan <asully@chromium.org>
> Commit-Queue: Daseul Lee <dslee@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#1101673}

Bug: 1326788, 1408321
Change-Id: I57872f266df109f2b0fb652e3d4d5b4aaaaad6f2
No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4225233
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Auto-Submit: Daseul Lee <dslee@chromium.org>
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#1101679}

[modify] https://crrev.com/0f9b05df02296253562df4d3155fb9e79ea7927b/chrome/browser/file_system_access/chrome_file_system_access_permission_context.h
[modify] https://crrev.com/0f9b05df02296253562df4d3155fb9e79ea7927b/chrome/browser/file_system_access/chrome_file_system_access_permission_context_unittest.cc
[modify] https://crrev.com/0f9b05df02296253562df4d3155fb9e79ea7927b/chrome/browser/file_system_access/chrome_file_system_access_permission_context.cc


### gi...@appspot.gserviceaccount.com (2023-02-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/403d13a8451b8a6b75a4d57945e7ada5b5fb52d2

commit 403d13a8451b8a6b75a4d57945e7ada5b5fb52d2
Author: Daseul Lee <dslee@chromium.org>
Date: Mon Feb 06 21:46:55 2023

Reland "[FSA] Update UNC path rejection to only local UNC path on Windows."

This is a reland of commit 01d8e55690c9f59f58c5ae1361d707f08a33be51

Original change's description:
> [FSA] Update UNC path rejection to only local UNC path on Windows.
>
> The previous check `PathIsUNC()` was too broad and included both external/network UNC path as well as local UNC path (i.e. "\\LOCALHOST\c$\..."). As we want to avoid different variants of "local" UNC from bypassing the blocklist check (and that we currently do not have any blocklist on external path), external UNC path will be allowed again with this change. Unfortunately, there is no complete way to normalize different variations of Windows path, so we use some heuristics by checking (1) UNC root via `base::FilePath::IsNetwork()`, (2) hostname, which may represent local system and (3) `$` character in share name.
>
> Bug: 1326788, 1408321
> Change-Id: I030b2719781ac21a145ceb83ce53e7f129b4ce2f
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4200953
> Reviewed-by: Austin Sullivan <asully@chromium.org>
> Commit-Queue: Daseul Lee <dslee@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#1101673}

Bug: 1326788, 1408321
Change-Id: I329391304b9afd7ed0160c8bd3e41985e81f4a3e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4226252
Commit-Queue: Daseul Lee <dslee@chromium.org>
Code-Coverage: Findit <findit-for-me@appspot.gserviceaccount.com>
Reviewed-by: James Forshaw <forshaw@chromium.org>
Reviewed-by: Austin Sullivan <asully@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1101794}

[modify] https://crrev.com/403d13a8451b8a6b75a4d57945e7ada5b5fb52d2/chrome/browser/file_system_access/chrome_file_system_access_permission_context.h
[modify] https://crrev.com/403d13a8451b8a6b75a4d57945e7ada5b5fb52d2/chrome/browser/file_system_access/chrome_file_system_access_permission_context_unittest.cc
[modify] https://crrev.com/403d13a8451b8a6b75a4d57945e7ada5b5fb52d2/chrome/browser/file_system_access/chrome_file_system_access_permission_context.cc


### gi...@appspot.gserviceaccount.com (2023-02-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/d7bff53e82d9ab435cd6c3d91052b90c3fe7ffd7

commit d7bff53e82d9ab435cd6c3d91052b90c3fe7ffd7
Author: Daseul Lee <dslee@chromium.org>
Date: Tue Feb 07 23:42:17 2023

[M111] Reland "[FSA] Update UNC path rejection to only local UNC path on Windows."

This is a reland of commit 01d8e55690c9f59f58c5ae1361d707f08a33be51

Original change's description:
> [FSA] Update UNC path rejection to only local UNC path on Windows.
>
> The previous check `PathIsUNC()` was too broad and included both external/network UNC path as well as local UNC path (i.e. "\\LOCALHOST\c$\..."). As we want to avoid different variants of "local" UNC from bypassing the blocklist check (and that we currently do not have any blocklist on external path), external UNC path will be allowed again with this change. Unfortunately, there is no complete way to normalize different variations of Windows path, so we use some heuristics by checking (1) UNC root via `base::FilePath::IsNetwork()`, (2) hostname, which may represent local system and (3) `$` character in share name.
>
> Bug: 1326788, 1408321
> Change-Id: I030b2719781ac21a145ceb83ce53e7f129b4ce2f
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4200953
> Reviewed-by: Austin Sullivan <asully@chromium.org>
> Commit-Queue: Daseul Lee <dslee@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#1101673}

(cherry picked from commit 403d13a8451b8a6b75a4d57945e7ada5b5fb52d2)

Bug: 1326788, 1408321
Change-Id: I329391304b9afd7ed0160c8bd3e41985e81f4a3e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4226252
Commit-Queue: Daseul Lee <dslee@chromium.org>
Code-Coverage: Findit <findit-for-me@appspot.gserviceaccount.com>
Reviewed-by: James Forshaw <forshaw@chromium.org>
Reviewed-by: Austin Sullivan <asully@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1101794}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4226858
Auto-Submit: Daseul Lee <dslee@chromium.org>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/5563@{#249}
Cr-Branched-From: 3ac59a6729cdb287a7ee629a0004c907ec1b06dc-refs/heads/main@{#1097615}

[modify] https://crrev.com/d7bff53e82d9ab435cd6c3d91052b90c3fe7ffd7/chrome/browser/file_system_access/chrome_file_system_access_permission_context_unittest.cc
[modify] https://crrev.com/d7bff53e82d9ab435cd6c3d91052b90c3fe7ffd7/chrome/browser/file_system_access/chrome_file_system_access_permission_context.h
[modify] https://crrev.com/d7bff53e82d9ab435cd6c3d91052b90c3fe7ffd7/chrome/browser/file_system_access/chrome_file_system_access_permission_context.cc


### gi...@appspot.gserviceaccount.com (2023-02-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/cc8e0ba6a32b9c546efbdfcb5261320035319e20

commit cc8e0ba6a32b9c546efbdfcb5261320035319e20
Author: Daseul Lee <dslee@chromium.org>
Date: Wed Feb 08 18:59:04 2023

[M110] Reland "[FSA] Update UNC path rejection to only local UNC path on Windows."

This is a reland of commit 01d8e55690c9f59f58c5ae1361d707f08a33be51

Original change's description:
> [FSA] Update UNC path rejection to only local UNC path on Windows.
>
> The previous check `PathIsUNC()` was too broad and included both external/network UNC path as well as local UNC path (i.e. "\\LOCALHOST\c$\..."). As we want to avoid different variants of "local" UNC from bypassing the blocklist check (and that we currently do not have any blocklist on external path), external UNC path will be allowed again with this change. Unfortunately, there is no complete way to normalize different variations of Windows path, so we use some heuristics by checking (1) UNC root via `base::FilePath::IsNetwork()`, (2) hostname, which may represent local system and (3) `$` character in share name.
>
> Bug: 1326788, 1408321
> Change-Id: I030b2719781ac21a145ceb83ce53e7f129b4ce2f
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4200953
> Reviewed-by: Austin Sullivan <asully@chromium.org>
> Commit-Queue: Daseul Lee <dslee@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#1101673}

(cherry picked from commit 403d13a8451b8a6b75a4d57945e7ada5b5fb52d2)

Bug: 1326788, 1408321
Change-Id: I329391304b9afd7ed0160c8bd3e41985e81f4a3e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4226252
Commit-Queue: Daseul Lee <dslee@chromium.org>
Code-Coverage: Findit <findit-for-me@appspot.gserviceaccount.com>
Reviewed-by: James Forshaw <forshaw@chromium.org>
Reviewed-by: Austin Sullivan <asully@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1101794}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4226852
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/5481@{#1052}
Cr-Branched-From: 130f3e4d850f4bc7387cfb8d08aa993d288a67a9-refs/heads/main@{#1084008}

[modify] https://crrev.com/cc8e0ba6a32b9c546efbdfcb5261320035319e20/chrome/browser/file_system_access/chrome_file_system_access_permission_context_unittest.cc
[modify] https://crrev.com/cc8e0ba6a32b9c546efbdfcb5261320035319e20/chrome/browser/file_system_access/chrome_file_system_access_permission_context.h
[modify] https://crrev.com/cc8e0ba6a32b9c546efbdfcb5261320035319e20/chrome/browser/file_system_access/chrome_file_system_access_permission_context.cc


### [Deleted User] (2023-02-10)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2023-02-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/8112f045a8c00aca00032fa057be0da38a9c1709

commit 8112f045a8c00aca00032fa057be0da38a9c1709
Author: Daseul Lee <dslee@chromium.org>
Date: Fri Feb 10 18:55:06 2023

Reland "[FSA] Update UNC path rejection to only local UNC path on Windows."

This is a reland of commit 01d8e55690c9f59f58c5ae1361d707f08a33be51

Original change's description:
> [FSA] Update UNC path rejection to only local UNC path on Windows.
>
> The previous check `PathIsUNC()` was too broad and included both external/network UNC path as well as local UNC path (i.e. "\\LOCALHOST\c$\..."). As we want to avoid different variants of "local" UNC from bypassing the blocklist check (and that we currently do not have any blocklist on external path), external UNC path will be allowed again with this change. Unfortunately, there is no complete way to normalize different variations of Windows path, so we use some heuristics by checking (1) UNC root via `base::FilePath::IsNetwork()`, (2) hostname, which may represent local system and (3) `$` character in share name.
>
> Bug: 1326788, 1408321
> Change-Id: I030b2719781ac21a145ceb83ce53e7f129b4ce2f
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4200953
> Reviewed-by: Austin Sullivan <asully@chromium.org>
> Commit-Queue: Daseul Lee <dslee@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#1101673}

(cherry picked from commit 403d13a8451b8a6b75a4d57945e7ada5b5fb52d2)

Bug: 1326788, 1408321
Change-Id: I329391304b9afd7ed0160c8bd3e41985e81f4a3e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4226252
Commit-Queue: Daseul Lee <dslee@chromium.org>
Code-Coverage: Findit <findit-for-me@appspot.gserviceaccount.com>
Reviewed-by: James Forshaw <forshaw@chromium.org>
Reviewed-by: Austin Sullivan <asully@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1101794}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4240562
Reviewed-by: Prudhvikumar Bommana <pbommana@google.com>
Owners-Override: Prudhvikumar Bommana <pbommana@google.com>
Commit-Queue: Prudhvikumar Bommana <pbommana@google.com>
Cr-Commit-Position: refs/branch-heads/5481_77@{#4}
Cr-Branched-From: 65ed616c6e8ee3fe0ad64fe83796c020644d42af-refs/branch-heads/5481@{#839}
Cr-Branched-From: 130f3e4d850f4bc7387cfb8d08aa993d288a67a9-refs/heads/main@{#1084008}

[modify] https://crrev.com/8112f045a8c00aca00032fa057be0da38a9c1709/chrome/browser/file_system_access/chrome_file_system_access_permission_context.h
[modify] https://crrev.com/8112f045a8c00aca00032fa057be0da38a9c1709/chrome/browser/file_system_access/chrome_file_system_access_permission_context_unittest.cc
[modify] https://crrev.com/8112f045a8c00aca00032fa057be0da38a9c1709/chrome/browser/file_system_access/chrome_file_system_access_permission_context.cc


### is...@google.com (2023-02-10)

This issue was migrated from crbug.com/chromium/1326788?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1358458]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059686)*
