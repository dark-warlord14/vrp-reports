# Security: Private file upload (data exfiltration)

| Field | Value |
|-------|-------|
| **Issue ID** | [40052821](https://issues.chromium.org/issues/40052821) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Mobile>Intents |
| **Platforms** | Android |
| **Reporter** | ka...@gmail.com |
| **Assignee** | qi...@chromium.org |
| **Created** | 2020-07-12 |
| **Bounty** | $1,000.00 |

## Description

**This template is ONLY for reporting security bugs. If you are reporting a**  

**Download Protection Bypass bug, please use the "Security - Download**  

**Protection" template. For all other reports, please use a different**  

**template.**

**Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com>**  

**/chromium/src/+/master/docs/security/faq.md**

**Please see the following link for instructions on filing security bugs:**  

**<https://www.chromium.org/Home/chromium-security/reporting-security-bugs>**

**Reports may be eligible for reward payments under the Chrome VRP:**  

**<http://g.co/ChromeBugRewards>**

**NOTE: Security bugs are normally made public once a fix has been widely**  

**deployed.**

**-------------------------**

**VULNERABILITY DETAILS**  

An incorrect path check in Chrome for Android upload feature private data exfiltration. A misinformed user might also upload private files such as their cookie's database to websites .

This is a bypass for fix in <https://bugs.chromium.org/p/chromium/issues/detail?id=859349>

**VERSION**

## Environment

- \*\*Device:\*\* HTC m8
- \*\*OS version:\*\* Android 9
- \*\*Package name:\*\* com.android.chrome
- \*\*App version:\*\* 83.0.4103.106 (`versionCode`: 410410670)

**REPRODUCTION CASE**

## Proof of concept

### Pre-conditions:

- Chrome configured
- PoC.apk installed (see attachements)
- Python3 installed
- ngrok (optional for easy tunneling)

### Steps:

- Start server.py
  
  `$ python3 server.py`
- Open server url in Chrome for Android
- Tap to upload a file
- Choose PoC (Chrome Internal) as file chooser

### Result

Content of `/data/data/com.android.chrome/shared_prefs/com.android.chrome_preferences.xml` is returned

### Expected result

No private data should be allowed to be uploaded

---

## Detailed explanation

This is the same vulnerability as <https://bugs.chromium.org/p/chromium/issues/detail?id=859349>. An incorrect path check allows private files to be uploaded with the following URI returned in the Picker:

```
val intent = Intent()  
intent.setDataAndType(  
    Uri.parse("file:///data/data/./com.android.chrome/shared_prefs/com.android.chrome_preferences.xml"),  
    "text/plain"  
)  
intent.flags =  
    intent.flags or Intent.FLAG_GRANT_WRITE_URI_PERMISSION or Intent.FLAG_GRANT_READ_URI_PERMISSION  

```

Because Chrome is comparing the absoluth path instead of a canonical path, it's possible to bypass the internal directory check by using `/./` in the pat or by using symlinks.

---

## Vulnerable code

- <https://github.com/chromium/chromium/blob/master/ui/android/java/src/org/chromium/ui/base/SelectFileDialog.java#L557>

```
if (!TextUtils.isEmpty(filePath) && !filePath.startsWith(PathUtils.getDataDirectory())) {  
    onFileSelected(mNativeSelectFileDialog, filePath, "");  
    return;  
}  

```

---

## Remediation

Convert this path to canonical before making the `startsWith` comparison.

---

## Attachments

- PoC.apk - Compiled binary
- ChromePathInternal.zip - Source code of the PoC application
- server.py - Python3 server to print uploaded files
- video.mp4 - screencap of the exploit in action

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: Pedro Oliveira

## Attachments

- [poc.apk](attachments/poc.apk) (application/octet-stream, 2.3 MB)
- [server.py](attachments/server.py) (text/plain, 737 B)
- [video.mp4](attachments/video.mp4) (video/mp4, 11.1 MB)
- [ChromePathInternal.zip](attachments/ChromePathInternal.zip) (application/octet-stream, 138.4 KB)

## Timeline

### mm...@google.com (2020-07-13)

Thanks for your report.

Chromies, please note that I did not attempt to reproduce this issue (don't have an android device at hand), so I'm traging this assuming it's reproducible.



[Monorail components: Mobile>Intents]

### [Deleted User] (2020-07-14)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-07-15)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-07-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/edd9caf30b3b44e9320d00839f7a21072d06f496

commit edd9caf30b3b44e9320d00839f7a21072d06f496
Author: Min Qin <qinmin@chromium.org>
Date: Thu Jul 16 17:15:15 2020

Use canonical path when determining whether a file is under private dir

BUG=1104628

Change-Id: Ief8b14f4b0f915b30ca28eb22612ffc5c7c00d2a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2298224
Reviewed-by: Peter Beverloo <peter@chromium.org>
Commit-Queue: Min Qin <qinmin@chromium.org>
Cr-Commit-Position: refs/heads/master@{#789089}

[modify] https://crrev.com/edd9caf30b3b44e9320d00839f7a21072d06f496/ui/android/java/src/org/chromium/ui/base/SelectFileDialog.java
[modify] https://crrev.com/edd9caf30b3b44e9320d00839f7a21072d06f496/ui/android/junit/src/org/chromium/ui/base/SelectFileDialogTest.java


### ka...@gmail.com (2020-07-16)

Hi team,

I don't see a canonicalization of PathUtils.getDataDirectory() so I'm afraid the exploit will still work because the default value of this should be /data/user/0 which is actually a symlink to /data/data/.

Can you confirm that the PoC is not working with that fix?

### [Deleted User] (2020-07-26)

qinmin: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### qi...@chromium.org (2020-07-27)

Interesting, I was testing on Android Lollipop and the data directory is /data/data/.  So I guess Android team have changed that in recent versions.

### ka...@gmail.com (2020-08-03)

Will this be fixed?

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-08-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/852c90becca2f6f53f84d65d7df960a518322383

commit 852c90becca2f6f53f84d65d7df960a518322383
Author: Min Qin <qinmin@chromium.org>
Date: Mon Aug 03 18:38:32 2020

Use Data directory's canonical path  when checking if a file is under it

the Data directory could be a sim link in recent Android versions.
So need to use canonical path when checking if a file is under it.

BUG=1104628

Change-Id: I403b9582e09a799e5c51d2687ce4928dea8e7e63
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2320071
Reviewed-by: Peter Beverloo <peter@chromium.org>
Commit-Queue: Min Qin <qinmin@chromium.org>
Cr-Commit-Position: refs/heads/master@{#794163}

[modify] https://crrev.com/852c90becca2f6f53f84d65d7df960a518322383/ui/android/java/src/org/chromium/ui/base/SelectFileDialog.java
[modify] https://crrev.com/852c90becca2f6f53f84d65d7df960a518322383/ui/android/junit/src/org/chromium/ui/base/SelectFileDialogTest.java


### ke...@chromium.org (2020-08-10)

qinmin@: Is there any more work to do on this, or can this bug be closed?

### qi...@chromium.org (2020-08-10)

[Empty comment from Monorail migration]

### [Deleted User] (2020-08-10)

[Empty comment from Monorail migration]

### ad...@google.com (2020-08-17)

[Empty comment from Monorail migration]

### [Deleted User] (2020-08-17)

Requesting merge to beta M85 because latest trunk commit (794163) appears to be after beta branch point (782793).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-08-17)

This bug requires manual review: We are only 7 days from stable.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), bindusuvarna@(iOS), dgagnon@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2020-08-17)

+adetaylo@ for M85 merge review and approval. Thank you.

 Please note we're cutting M85 Stable RC tomorrow, Tuesday noon (PDT).

### ad...@google.com (2020-08-17)

Approving merge to M85. Please merge to branch 4183, assuming no problems have shown up in Canary.

### go...@chromium.org (2020-08-17)

[Bulk Edit]

Please merge your change to M85 branch 4183 ASAP so we can pick it up for M85 Stable RC cut. Thank you.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-08-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/01ab55f109c1d2f96f811264ae09af573d4ea44c

commit 01ab55f109c1d2f96f811264ae09af573d4ea44c
Author: Min Qin <qinmin@chromium.org>
Date: Tue Aug 18 16:35:29 2020

Use canonical path when determining whether a file is under private dir

BUG=1104628

(cherry picked from commit edd9caf30b3b44e9320d00839f7a21072d06f496)

Change-Id: Ief8b14f4b0f915b30ca28eb22612ffc5c7c00d2a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2298224
Reviewed-by: Peter Beverloo <peter@chromium.org>
Commit-Queue: Min Qin <qinmin@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#789089}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2363110
Reviewed-by: Min Qin <qinmin@chromium.org>
Cr-Commit-Position: refs/branch-heads/4183@{#1581}
Cr-Branched-From: 740e9e8a40505392ba5c8e022a8024b3d018ca65-refs/heads/master@{#782793}

[modify] https://crrev.com/01ab55f109c1d2f96f811264ae09af573d4ea44c/ui/android/java/src/org/chromium/ui/base/SelectFileDialog.java
[modify] https://crrev.com/01ab55f109c1d2f96f811264ae09af573d4ea44c/ui/android/junit/src/org/chromium/ui/base/SelectFileDialogTest.java


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-08-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/db8b45b64b51afb3ace48dc3511e28cc4886aa34

commit db8b45b64b51afb3ace48dc3511e28cc4886aa34
Author: Min Qin <qinmin@chromium.org>
Date: Tue Aug 18 18:35:21 2020

Use Data directory's canonical path  when checking if a file is under it

the Data directory could be a sim link in recent Android versions.
So need to use canonical path when checking if a file is under it.

BUG=1104628

(cherry picked from commit 852c90becca2f6f53f84d65d7df960a518322383)

Change-Id: I403b9582e09a799e5c51d2687ce4928dea8e7e63
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2320071
Reviewed-by: Peter Beverloo <peter@chromium.org>
Commit-Queue: Min Qin <qinmin@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#794163}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2363109
Reviewed-by: Min Qin <qinmin@chromium.org>
Cr-Commit-Position: refs/branch-heads/4183@{#1584}
Cr-Branched-From: 740e9e8a40505392ba5c8e022a8024b3d018ca65-refs/heads/master@{#782793}

[modify] https://crrev.com/db8b45b64b51afb3ace48dc3511e28cc4886aa34/ui/android/java/src/org/chromium/ui/base/SelectFileDialog.java
[modify] https://crrev.com/db8b45b64b51afb3ace48dc3511e28cc4886aa34/ui/android/junit/src/org/chromium/ui/base/SelectFileDialogTest.java


### ad...@google.com (2020-08-19)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-08-19)

Thanks for the report! The VRP panel has decided to award $1000 for this bug. Someone from our finance team will get in touch.

### ad...@google.com (2020-08-20)

[Empty comment from Monorail migration]

### ad...@google.com (2020-08-24)

[Empty comment from Monorail migration]

### ad...@google.com (2020-08-24)

[Empty comment from Monorail migration]

### ad...@google.com (2020-09-21)

[Empty comment from Monorail migration]

### [Deleted User] (2020-11-16)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2021-03-29)

hi kanytu@ - we consider attachments/pocs included with reports to be an integral part of the report, so I've un-deleted them. Thanks!

### gi...@appspot.gserviceaccount.com (2022-06-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/c90687dab8ade225766bff9582d16d3fd80a9cd0

commit c90687dab8ade225766bff9582d16d3fd80a9cd0
Author: Min Qin <qinmin@chromium.org>
Date: Fri Jun 17 18:06:31 2022

Fix an issue that content URI can be used to upload files under app dir

BUG=1104628

Change-Id: Ic20569b0bf2e77fdc4480bfba6db7c710198552e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3701011
Reviewed-by: Tommy Nyquist <nyquist@chromium.org>
Commit-Queue: Min Qin <qinmin@chromium.org>
Reviewed-by: Finnur Thorarinsson <finnur@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1015426}

[modify] https://crrev.com/c90687dab8ade225766bff9582d16d3fd80a9cd0/ui/android/java/src/org/chromium/ui/base/SelectFileDialog.java
[modify] https://crrev.com/c90687dab8ade225766bff9582d16d3fd80a9cd0/chrome/android/javatests/src/org/chromium/chrome/browser/SelectFileDialogTest.java


### gi...@appspot.gserviceaccount.com (2022-06-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/810fc6c0bed41d1ef425242e91611362542802c4

commit 810fc6c0bed41d1ef425242e91611362542802c4
Author: Min Qin <qinmin@chromium.org>
Date: Wed Jun 29 01:13:56 2022

[M104] Fix an issue that content URI can be used to upload files under app dir

BUG=1104628

(cherry picked from commit c90687dab8ade225766bff9582d16d3fd80a9cd0)

Change-Id: Ic20569b0bf2e77fdc4480bfba6db7c710198552e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3701011
Reviewed-by: Tommy Nyquist <nyquist@chromium.org>
Commit-Queue: Min Qin <qinmin@chromium.org>
Reviewed-by: Finnur Thorarinsson <finnur@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1015426}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3731509
Cr-Commit-Position: refs/branch-heads/5112@{#425}
Cr-Branched-From: b13d3fe7b3c47a56354ef54b221008afa754412e-refs/heads/main@{#1012729}

[modify] https://crrev.com/810fc6c0bed41d1ef425242e91611362542802c4/ui/android/java/src/org/chromium/ui/base/SelectFileDialog.java
[modify] https://crrev.com/810fc6c0bed41d1ef425242e91611362542802c4/chrome/android/javatests/src/org/chromium/chrome/browser/SelectFileDialogTest.java


### gi...@appspot.gserviceaccount.com (2022-07-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/487ebee1df5f6ce1fda4c439dbf3542759d12d59

commit 487ebee1df5f6ce1fda4c439dbf3542759d12d59
Author: Min Qin <qinmin@chromium.org>
Date: Fri Jul 15 17:34:49 2022

[M103]Fix an issue that content URI can be used to upload files under app dir

BUG=1104628, 1329987

(cherry picked from commit c90687dab8ade225766bff9582d16d3fd80a9cd0)

Change-Id: Ic20569b0bf2e77fdc4480bfba6db7c710198552e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3701011
Reviewed-by: Tommy Nyquist <nyquist@chromium.org>
Commit-Queue: Min Qin <qinmin@chromium.org>
Reviewed-by: Finnur Thorarinsson <finnur@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1015426}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3764658
Reviewed-by: Krishna Govind <govind@chromium.org>
Commit-Queue: Krishna Govind <govind@chromium.org>
Owners-Override: Krishna Govind <govind@chromium.org>
Reviewed-by: Ted Choc <tedchoc@chromium.org>
Cr-Commit-Position: refs/branch-heads/5060@{#1235}
Cr-Branched-From: b83393d0f4038aeaf67f970a024d8101df7348d1-refs/heads/main@{#1002911}

[modify] https://crrev.com/487ebee1df5f6ce1fda4c439dbf3542759d12d59/ui/android/java/src/org/chromium/ui/base/SelectFileDialog.java
[modify] https://crrev.com/487ebee1df5f6ce1fda4c439dbf3542759d12d59/chrome/android/javatests/src/org/chromium/chrome/browser/SelectFileDialogTest.java


### gi...@appspot.gserviceaccount.com (2022-07-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/1e5fd85fa40c92fd64c9aa722af66c8d5e4cb9c5

commit 1e5fd85fa40c92fd64c9aa722af66c8d5e4cb9c5
Author: Min Qin <qinmin@chromium.org>
Date: Sat Jul 16 11:22:16 2022

[M102] Fix an issue that content URI can be used to upload files under app dir

BUG=1104628,1329987

(cherry picked from commit c90687dab8ade225766bff9582d16d3fd80a9cd0)

Change-Id: Ic20569b0bf2e77fdc4480bfba6db7c710198552e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3701011
Reviewed-by: Tommy Nyquist <nyquist@chromium.org>
Commit-Queue: Min Qin <qinmin@chromium.org>
Reviewed-by: Finnur Thorarinsson <finnur@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1015426}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3765372
Owners-Override: Krishna Govind <govind@chromium.org>
Reviewed-by: Krishna Govind <govind@chromium.org>
Cr-Commit-Position: refs/branch-heads/5005@{#1257}
Cr-Branched-From: 5b4d9450fee01f821b6400e947b3839727643a71-refs/heads/main@{#992738}

[modify] https://crrev.com/1e5fd85fa40c92fd64c9aa722af66c8d5e4cb9c5/ui/android/java/src/org/chromium/ui/base/SelectFileDialog.java
[modify] https://crrev.com/1e5fd85fa40c92fd64c9aa722af66c8d5e4cb9c5/chrome/android/javatests/src/org/chromium/chrome/browser/SelectFileDialogTest.java


### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1104628?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40052821)*
