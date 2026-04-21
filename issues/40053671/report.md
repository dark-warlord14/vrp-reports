# Security: showSaveFilePicker allowing to save .lnk and .local files on windows!

| Field | Value |
|-------|-------|
| **Issue ID** | [40053671](https://issues.chromium.org/issues/40053671) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Storage>FileSystem |
| **Platforms** | Linux, Mac, Windows |
| **CVE IDs** | CVE-2010-2568 |
| **Reporter** | ma...@gmail.com |
| **Assignee** | as...@chromium.org |
| **Created** | 2020-10-20 |
| **Bounty** | $1,000.00 |

## Description

New bug based on "Comment by [maciekpul@gmail.com](mailto:maciekpul@gmail.com) on Sun, Oct 18, 2020, 4:56 PM GMT+2 (a day ago)": <https://bugs.chromium.org/p/chromium/issues/detail?id=1137247#c12>

**VULNERABILITY DETAILS**  

showSaveFilePicker allowing to save .lnk and .local files on windows! + extra spoof it as .jpeg (based on bug from <https://bugs.chromium.org/p/chromium/issues/detail?id=1137247>).

Based on default/main chrome download function:  

showSaveFilePicker bypassing the function "IsShellIntegratedExtension": <https://source.chromium.org/chromium/chromium/src/+/master:net/base/filename_util_internal.cc;drc=1c58af32060fa0ef3cfd4037fdc7913092d16ba2;l=155?q=%20EnsureSafeExtension&ss=chromium>

if extension ".lnk" or ".local" then Chrome should CHANGE extension to ".download", but not doing this:  

<https://source.chromium.org/chromium/chromium/src/+/master:net/base/filename_util_internal.cc;drc=1c58af32060fa0ef3cfd4037fdc7913092d16ba2;l=195?q=%20EnsureSafeExtension&ss=chromium>

.lnk files are very dangerous and used in two ways:

1. Spoof extension on windows - totally hide the real extension of the file.
2. .lnk files may be used to execute arbitrary code (see <https://nvd.nist.gov/vuln/detail/CVE-2010-2568>).  
   
   <https://www.thezdi.com/blog/2020/3/25/cve-2020-0729-remote-code-execution-through-lnk-files>  
   
   Possible RCE by saving a .lnk file.

and

.local files may determine which DLLs to load for an application in Windows.

URL EXAMPLE: <https://nfz.dev/lnk.html>

**VERSION**  

Chrome Version: [86.0.4240.75] + [stable]  

Operating System: [Windows 10 OS Version 1903 (Build 18362.1082)]

**REPRODUCTION CASE**  

Fetch .lnk/.local and add accept - extension ".lnk"/".local"

SOLUTION  

Replace ".lnk" and ".local" with ".download" or block downloading such a file.

Reporter credit: Maciej Pulikowski

## Attachments

- [picture21.png](attachments/picture21.png) (image/png, 24.0 KB)
- [picture20.png](attachments/picture20.png) (image/png, 38.5 KB)
- [lnk2.gif](attachments/lnk2.gif) (image/gif, 18.2 MB)
- [lnk.html](attachments/lnk.html) (text/plain, 4.6 KB)

## Timeline

### oc...@google.com (2020-10-21)

[Empty comment from Monorail migration]

[Monorail components: Blink>Storage>FileSystem]

### [Deleted User] (2020-10-21)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-10-21)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-10-30)

[Empty comment from Monorail migration]

### [Deleted User] (2020-11-03)

mek: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-11-17)

mek: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ma...@gmail.com (2020-11-18)

Bug still persists in 87 version

### me...@chromium.org (2020-11-19)

Sorry for the lack of updates here, we should have a fix for this soon (by just disallowing these extensions).

### ma...@gmail.com (2020-11-19)

Ok. No worries :) 

I have found the same bug in getFileHandle() method.

https://bugs.chromium.org/p/chromium/issues/detail?id=1150810

### me...@chromium.org (2020-11-30)

Can you CC me on that other bug? It doesn't seem security bug triage has triaged that bug to me yet...

Like the other issues, spec PR for this bug is https://github.com/WICG/file-system-access/pull/252.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-12-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/c75c5a1e1d72fc923c82ebcaeacc874c88215eff

commit c75c5a1e1d72fc923c82ebcaeacc874c88215eff
Author: Austin Sullivan <asully@chromium.org>
Date: Fri Dec 04 13:44:29 2020

Add restrictions to allowed extensions for File System Access API

These restrictions apply to showOpenFilePicker and showSaveFilePicker.

Existing restriction:
- Extension must start with "."

New restrictions:
- Allowed code points: [A-Za-z0-9+.]
- Extension length cannot exceed to 16, inclusive of leading "."
- Extension cannot end with "."
- Extension cannot end with "local" or "lnk"

Bug: 1137247, 1140410, 1140417, 1152327
Change-Id: I593f7ca60e05177402885bd3026add16b3a07d0c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2568534
Reviewed-by: Marijn Kruisselbrink <mek@chromium.org>
Commit-Queue: Austin Sullivan <asully@chromium.org>
Cr-Commit-Position: refs/heads/master@{#833695}

[modify] https://crrev.com/c75c5a1e1d72fc923c82ebcaeacc874c88215eff/content/browser/file_system_access/file_system_chooser.cc
[modify] https://crrev.com/c75c5a1e1d72fc923c82ebcaeacc874c88215eff/content/browser/file_system_access/file_system_chooser_unittest.cc
[modify] https://crrev.com/c75c5a1e1d72fc923c82ebcaeacc874c88215eff/third_party/blink/renderer/modules/file_system_access/global_native_file_system.cc
[modify] https://crrev.com/c75c5a1e1d72fc923c82ebcaeacc874c88215eff/third_party/blink/web_tests/external/wpt/native-file-system/showPicker-errors.https.window.js


### as...@chromium.org (2020-12-04)

[Empty comment from Monorail migration]

### [Deleted User] (2020-12-04)

[Empty comment from Monorail migration]

### [Deleted User] (2020-12-04)

[Empty comment from Monorail migration]

### [Deleted User] (2020-12-05)

Requesting merge to beta M88 because latest trunk commit (833695) appears to be after beta branch point (827102).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-12-05)

This bug requires manual review: M88's targeted beta branch promotion date has already passed, so this requires manual review
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on ToT?
4. Does this change need to be merged into other active release branches (M-1, M+1)?
5. Why are these changes required in this milestone after branch?
6. Is this a new feature?
7. If it is a new feature, is it behind a flag using finch?

Chrome OS Only:
8. Was the change reviewed and approved by the Eng Prod Representative? See Eng Prod ownership by component: http://go/cros-engprodcomponents

Please contact the milestone owner if you have questions.
Owners: govind@(Android), bindusuvarna@(iOS), dgagnon@(ChromeOS), srinivassista @(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sr...@google.com (2020-12-07)

asully@ pls answer https://crbug.com/chromium/1140417#c16 for merge review. 

### ad...@google.com (2020-12-07)

There's merge approval for this CL in https://crbug.com/chromium/1152327, so removing the duplication.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-12-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/96db1e0e8c1dfdfab9b8e305e3d2f3ffc9e1ba49

commit 96db1e0e8c1dfdfab9b8e305e3d2f3ffc9e1ba49
Author: Austin Sullivan <asully@chromium.org>
Date: Mon Dec 07 22:09:02 2020

Add restrictions to allowed extensions for File System Access API

These restrictions apply to showOpenFilePicker and showSaveFilePicker.

Existing restriction:
- Extension must start with "."

New restrictions:
- Allowed code points: [A-Za-z0-9+.]
- Extension length cannot exceed to 16, inclusive of leading "."
- Extension cannot end with "."
- Extension cannot end with "local" or "lnk"

(cherry picked from commit c75c5a1e1d72fc923c82ebcaeacc874c88215eff)

Bug: 1137247, 1140403, 1140410, 1140417, 1140435, 1152327
Change-Id: I593f7ca60e05177402885bd3026add16b3a07d0c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2568534
Reviewed-by: Marijn Kruisselbrink <mek@chromium.org>
Commit-Queue: Austin Sullivan <asully@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#833695}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2576109
Commit-Queue: Marijn Kruisselbrink <mek@chromium.org>
Auto-Submit: Austin Sullivan <asully@chromium.org>
Cr-Commit-Position: refs/branch-heads/4324@{#649}
Cr-Branched-From: c73b5a651d37a6c4d0b8e3262cc4015a5579c6c8-refs/heads/master@{#827102}

[modify] https://crrev.com/96db1e0e8c1dfdfab9b8e305e3d2f3ffc9e1ba49/content/browser/file_system_access/file_system_chooser.cc
[modify] https://crrev.com/96db1e0e8c1dfdfab9b8e305e3d2f3ffc9e1ba49/content/browser/file_system_access/file_system_chooser_unittest.cc
[modify] https://crrev.com/96db1e0e8c1dfdfab9b8e305e3d2f3ffc9e1ba49/third_party/blink/renderer/modules/file_system_access/global_native_file_system.cc
[modify] https://crrev.com/96db1e0e8c1dfdfab9b8e305e3d2f3ffc9e1ba49/third_party/blink/web_tests/external/wpt/native-file-system/showPicker-errors.https.window.js


### ad...@google.com (2020-12-10)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-12-10)

Congratulations, the VRP panel has decided to award $1000 for this bug (and for two of your others, for $3000 total). Someone from our finance team will be in touch.

### ad...@google.com (2020-12-10)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-13)

[Empty comment from Monorail migration]

### am...@google.com (2021-01-19)

[Empty comment from Monorail migration]

### ja...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### as...@google.com (2021-01-27)

[Empty comment from Monorail migration]

### am...@google.com (2021-02-09)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-12)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1140417?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40053671)*
