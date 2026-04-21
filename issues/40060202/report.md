# Security: `chrome.downloads.onDeterminingFilename` can be used to bypass the fix for issue 1310461 and steal environment variables

| Field | Value |
|-------|-------|
| **Issue ID** | [40060202](https://issues.chromium.org/issues/40060202) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>Extensions>API |
| **Platforms** | Windows |
| **Reporter** | la...@gmail.com |
| **Assignee** | qi...@chromium.org |
| **Created** | 2022-07-07 |
| **Bounty** | $7,000.00 |

## Description

**VULNERABILITY DETAILS**  

After looking at <https://crbug.com/chromium/1310461> and the `chrome.downloads` API, I found `chrome.downloads.onDeterminingFilename`[1] which states that "During the filename determination process, extensions will be given the opportunity to override the target DownloadItem.filename". Well, it turns out that this can be used to bypass the fix for <https://crbug.com/chromium/1310461>.

[1] <https://developer.chrome.com/docs/extensions/reference/downloads/#event-onDeterminingFilename>

**VERSION**  

Chrome Version: Version 103.0.5060.114 (Official Build) (64-bit)  

Operating System: Windows 10

**REPRODUCTION CASE**  

I have attached a video demonstrating the issue and the files for the extension to reproduce the issue.

**CREDIT INFORMATION**  

Reporter credit: Maurice Dauer

## Attachments

- [poc.mp4](attachments/poc.mp4) (video/mp4, 2.0 MB)
- [bg.js](attachments/bg.js) (text/plain, 436 B)
- [manifest.json](attachments/manifest.json) (text/plain, 311 B)
- [issue.patch](attachments/issue.patch) (text/plain, 813 B)
- [updated_poc.mp4](attachments/updated_poc.mp4) (video/mp4, 2.7 MB)

## Timeline

### [Deleted User] (2022-07-07)

[Empty comment from Monorail migration]

### da...@chromium.org (2022-07-07)

I do see this happening in M102.

[Monorail components: Platform>Apps>API]

### da...@chromium.org (2022-07-07)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-07)

[Empty comment from Monorail migration]

### la...@gmail.com (2022-07-08)

I have attached a patch that fixes this issue, also I think the component should be Platform>Extensions>API (like in https://crbug.com/chromium/1310461) instead of Platform>Apps>API.

### sa...@chromium.org (2022-07-11)

[Empty comment from Monorail migration]

[Monorail components: -Platform>Apps>API Platform>Extensions>API]

### qi...@chromium.org (2022-07-11)

This should have been fixed by https://chromium-review.googlesource.com/c/chromium/src/+/3688608. Can you try chrome 104 and see if this happens?

The issue is related to Windows save file dialog, which honors the env environment. And the CL will replace the % characters before showing the save file dialog

### la...@gmail.com (2022-07-11)

Yes, I can confirm that the CL fixes the issue, but it seems to have only landed in chrome 105, on chrome 104 it is still reproducible. However, when playing around with the fix, I noticed that there is still a way to leak environment variables. The file extension for a download is automatically generated from the URL path when there is no `filename` specified and by specifying a download URL like `https://example.com/test.%USERNAME%`, `%USERNAME%` can be leaked.

Updated bg.js
```
chrome.downloads.onChanged.addListener(
    function(item) {
      if (!item.filename) {
        return;
      }
  
      console.log(item);
    }
);
  
chrome.downloads.download({
    url: 'https://example.com/test.%USERNAME%', 
    saveAs: true,
});
```

Do you want me to open a new issue or just updated this issue?

### [Deleted User] (2022-07-12)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-12)

[Empty comment from Monorail migration]

### qi...@chromium.org (2022-07-13)

The fix got recently merged to 104, so it may take some days to reach beta.

For using extension to expose env, i can repro the issue. Reopen this issue.

### gi...@appspot.gserviceaccount.com (2022-07-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/5e105f0bc3443e873924b92778574ffbb792c645

commit 5e105f0bc3443e873924b92778574ffbb792c645
Author: Min Qin <qinmin@chromium.org>
Date: Fri Jul 15 19:30:46 2022

Fix an issue extensions can be used to expose env variables

On windows save file dialog, the file extension type can also be used
to expose env variables. The extension is passed separately from the
file name to be saved. This CL sanitizes the extension before it is
being used. The CL also removes unused AppendExtensionIfNeeded().

BUG=1342586

Change-Id: Ic79f2dfef01022c4ca86e5ce08fa46ac91125812
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3759498
Reviewed-by: Robert Liao <robliao@chromium.org>
Commit-Queue: Min Qin <qinmin@chromium.org>
Reviewed-by: Scott Violet <sky@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1024868}

[modify] https://crrev.com/5e105f0bc3443e873924b92778574ffbb792c645/ui/shell_dialogs/execute_select_file_win.h
[modify] https://crrev.com/5e105f0bc3443e873924b92778574ffbb792c645/ui/shell_dialogs/execute_select_file_win.cc
[add] https://crrev.com/5e105f0bc3443e873924b92778574ffbb792c645/ui/shell_dialogs/select_file_utils_win.h
[add] https://crrev.com/5e105f0bc3443e873924b92778574ffbb792c645/ui/shell_dialogs/select_file_utils_win_unittest.cc
[delete] https://crrev.com/a5dc7175b20f6b2d6b8e97c3c9861553ae804386/ui/shell_dialogs/execute_select_file_win_unittest.cc
[modify] https://crrev.com/5e105f0bc3443e873924b92778574ffbb792c645/ui/shell_dialogs/select_file_dialog_win.cc
[modify] https://crrev.com/5e105f0bc3443e873924b92778574ffbb792c645/ui/shell_dialogs/BUILD.gn


### la...@gmail.com (2022-07-19)

Can confirm that this fixes the issue, thanks for the quick fix!

### sa...@chromium.org (2022-07-27)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-08-01)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-08-01)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-08-01)

following merging https://crbug.com/chromium/1343393 into this issue, raising severity to medium given impact 

### am...@chromium.org (2022-08-01)

As this issue has the same root cause and fix as https://crbug.com/chromium/1343393, manually adding merge approval as this would have been approved from merge through that report, but there is no reason to not consolidate the two from what I am seeing. 

Please merge this fix to branch 5195 at your earliest convenience so this fix can be included in the M105 cut for beta promotion. Thank you! 

### [Deleted User] (2022-08-02)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-08-02)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2022-08-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-08-11)

Congratulations, Maurice! The VRP Panel has decided to award you $7,000 for this report. Thank you for your efforts and reporting this issue to us! 

### gi...@appspot.gserviceaccount.com (2022-08-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/fc8ee3d8ae6ac4cd303840b5be5fc58edcded9b2

commit fc8ee3d8ae6ac4cd303840b5be5fc58edcded9b2
Author: Min Qin <qinmin@chromium.org>
Date: Fri Aug 12 17:38:34 2022

Fix an issue extensions can be used to expose env variables

On windows save file dialog, the file extension type can also be used
to expose env variables. The extension is passed separately from the
file name to be saved. This CL sanitizes the extension before it is
being used. The CL also removes unused AppendExtensionIfNeeded().

BUG=1342586

(cherry picked from commit 5e105f0bc3443e873924b92778574ffbb792c645)

Change-Id: Ic79f2dfef01022c4ca86e5ce08fa46ac91125812
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3759498
Reviewed-by: Robert Liao <robliao@chromium.org>
Commit-Queue: Min Qin <qinmin@chromium.org>
Reviewed-by: Scott Violet <sky@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1024868}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3828426
Reviewed-by: Prudhvikumar Bommana <pbommana@google.com>
Commit-Queue: Srinivas Sista <srinivassista@chromium.org>
Owners-Override: Srinivas Sista <srinivassista@chromium.org>
Cr-Commit-Position: refs/branch-heads/5112@{#1455}
Cr-Branched-From: b13d3fe7b3c47a56354ef54b221008afa754412e-refs/heads/main@{#1012729}

[modify] https://crrev.com/fc8ee3d8ae6ac4cd303840b5be5fc58edcded9b2/ui/shell_dialogs/execute_select_file_win.h
[modify] https://crrev.com/fc8ee3d8ae6ac4cd303840b5be5fc58edcded9b2/ui/shell_dialogs/execute_select_file_win.cc
[add] https://crrev.com/fc8ee3d8ae6ac4cd303840b5be5fc58edcded9b2/ui/shell_dialogs/select_file_utils_win.h
[add] https://crrev.com/fc8ee3d8ae6ac4cd303840b5be5fc58edcded9b2/ui/shell_dialogs/select_file_utils_win_unittest.cc
[modify] https://crrev.com/fc8ee3d8ae6ac4cd303840b5be5fc58edcded9b2/ui/shell_dialogs/select_file_dialog_win.cc
[delete] https://crrev.com/5f96ffc742689421abb8f2e1865c55066873e244/ui/shell_dialogs/execute_select_file_win_unittest.cc
[modify] https://crrev.com/fc8ee3d8ae6ac4cd303840b5be5fc58edcded9b2/ui/shell_dialogs/BUILD.gn


### am...@google.com (2022-08-12)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-08-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/0113acbb3e3f5f53e8b9a44b42a6dc9506eeabbe

commit 0113acbb3e3f5f53e8b9a44b42a6dc9506eeabbe
Author: Srinivas Sista <srinivassista@chromium.org>
Date: Fri Aug 12 23:20:23 2022

Revert "Fix an issue extensions can be used to expose env variables"

This reverts commit fc8ee3d8ae6ac4cd303840b5be5fc58edcded9b2.

Reason for revert: Wrong CL merged 

Original change's description:
> Fix an issue extensions can be used to expose env variables
>
> On windows save file dialog, the file extension type can also be used
> to expose env variables. The extension is passed separately from the
> file name to be saved. This CL sanitizes the extension before it is
> being used. The CL also removes unused AppendExtensionIfNeeded().
>
> BUG=1342586
>
> (cherry picked from commit 5e105f0bc3443e873924b92778574ffbb792c645)
>
> Change-Id: Ic79f2dfef01022c4ca86e5ce08fa46ac91125812
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3759498
> Reviewed-by: Robert Liao <robliao@chromium.org>
> Commit-Queue: Min Qin <qinmin@chromium.org>
> Reviewed-by: Scott Violet <sky@chromium.org>
> Cr-Original-Commit-Position: refs/heads/main@{#1024868}
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3828426
> Reviewed-by: Prudhvikumar Bommana <pbommana@google.com>
> Commit-Queue: Srinivas Sista <srinivassista@chromium.org>
> Owners-Override: Srinivas Sista <srinivassista@chromium.org>
> Cr-Commit-Position: refs/branch-heads/5112@{#1455}
> Cr-Branched-From: b13d3fe7b3c47a56354ef54b221008afa754412e-refs/heads/main@{#1012729}

Bug: 1342586
Change-Id: I0a810ba0210bdbdb289f2088b371e629e6c00232
No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3829082
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Owners-Override: Srinivas Sista <srinivassista@chromium.org>
Commit-Queue: Srinivas Sista <srinivassista@chromium.org>
Cr-Commit-Position: refs/branch-heads/5112@{#1460}
Cr-Branched-From: b13d3fe7b3c47a56354ef54b221008afa754412e-refs/heads/main@{#1012729}

[modify] https://crrev.com/0113acbb3e3f5f53e8b9a44b42a6dc9506eeabbe/ui/shell_dialogs/execute_select_file_win.h
[modify] https://crrev.com/0113acbb3e3f5f53e8b9a44b42a6dc9506eeabbe/ui/shell_dialogs/execute_select_file_win.cc
[delete] https://crrev.com/9c5a91ab811705e8a5fcfebfdf78efd9b88077ad/ui/shell_dialogs/select_file_utils_win.h
[delete] https://crrev.com/9c5a91ab811705e8a5fcfebfdf78efd9b88077ad/ui/shell_dialogs/select_file_utils_win_unittest.cc
[add] https://crrev.com/0113acbb3e3f5f53e8b9a44b42a6dc9506eeabbe/ui/shell_dialogs/execute_select_file_win_unittest.cc
[modify] https://crrev.com/0113acbb3e3f5f53e8b9a44b42a6dc9506eeabbe/ui/shell_dialogs/select_file_dialog_win.cc
[modify] https://crrev.com/0113acbb3e3f5f53e8b9a44b42a6dc9506eeabbe/ui/shell_dialogs/BUILD.gn


### am...@chromium.org (2022-08-16)

Hi qinmin@ based on CL mix-up on another security bug, it looks like the merge of this fix to 104 got reverted. Could you please reland this fix to M104/branch 5112 at your earliest convenience. Sincere apologies for the inconvenience! 
This will miss today's respin of M104, but can be included in Extended Stable release when M105 is promoted to stable. Thank you! 

### [Deleted User] (2022-08-22)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sr...@google.com (2022-08-23)

Pls confirm this CP is good - https://chromium-review.googlesource.com/c/chromium/src/+/3828096 and land it for M104.

### gi...@appspot.gserviceaccount.com (2022-08-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/c826f732d3ce8404bf2ffacf56a450796af72d9b

commit c826f732d3ce8404bf2ffacf56a450796af72d9b
Author: Min Qin <qinmin@chromium.org>
Date: Wed Aug 24 16:47:51 2022

[M104] Reland "Fix an issue extensions can be used to expose env variables"

This reverts commit 0113acbb3e3f5f53e8b9a44b42a6dc9506eeabbe.

Reason for revert: Not sure why the previous CL got reverted and the reason is wrong CL merged. Got a merge request on crbug.com/1342586. 

Original change's description:
> Revert "Fix an issue extensions can be used to expose env variables"
>
> This reverts commit fc8ee3d8ae6ac4cd303840b5be5fc58edcded9b2.
>
> Reason for revert: Wrong CL merged 
>
> Original change's description:
> > Fix an issue extensions can be used to expose env variables
> >
> > On windows save file dialog, the file extension type can also be used
> > to expose env variables. The extension is passed separately from the
> > file name to be saved. This CL sanitizes the extension before it is
> > being used. The CL also removes unused AppendExtensionIfNeeded().
> >
> > BUG=1342586
> >
> > (cherry picked from commit 5e105f0bc3443e873924b92778574ffbb792c645)
> >
> > Change-Id: Ic79f2dfef01022c4ca86e5ce08fa46ac91125812
> > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3759498
> > Reviewed-by: Robert Liao <robliao@chromium.org>
> > Commit-Queue: Min Qin <qinmin@chromium.org>
> > Reviewed-by: Scott Violet <sky@chromium.org>
> > Cr-Original-Commit-Position: refs/heads/main@{#1024868}
> > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3828426
> > Reviewed-by: Prudhvikumar Bommana <pbommana@google.com>
> > Commit-Queue: Srinivas Sista <srinivassista@chromium.org>
> > Owners-Override: Srinivas Sista <srinivassista@chromium.org>
> > Cr-Commit-Position: refs/branch-heads/5112@{#1455}
> > Cr-Branched-From: b13d3fe7b3c47a56354ef54b221008afa754412e-refs/heads/main@{#1012729}
>
> Bug: 1342586
> Change-Id: I0a810ba0210bdbdb289f2088b371e629e6c00232
> No-Presubmit: true
> No-Tree-Checks: true
> No-Try: true
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3829082
> Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
> Owners-Override: Srinivas Sista <srinivassista@chromium.org>
> Commit-Queue: Srinivas Sista <srinivassista@chromium.org>
> Cr-Commit-Position: refs/branch-heads/5112@{#1460}
> Cr-Branched-From: b13d3fe7b3c47a56354ef54b221008afa754412e-refs/heads/main@{#1012729}

Bug: 1342586
Change-Id: Ifad51641dd2fc8033cb4676fa7897bb036234f2b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3828096
Reviewed-by: Min Qin <qinmin@chromium.org>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Owners-Override: Srinivas Sista <srinivassista@chromium.org>
Commit-Queue: Srinivas Sista <srinivassista@chromium.org>
Cr-Commit-Position: refs/branch-heads/5112@{#1519}
Cr-Branched-From: b13d3fe7b3c47a56354ef54b221008afa754412e-refs/heads/main@{#1012729}

[modify] https://crrev.com/c826f732d3ce8404bf2ffacf56a450796af72d9b/ui/shell_dialogs/execute_select_file_win.h
[modify] https://crrev.com/c826f732d3ce8404bf2ffacf56a450796af72d9b/ui/shell_dialogs/execute_select_file_win.cc
[add] https://crrev.com/c826f732d3ce8404bf2ffacf56a450796af72d9b/ui/shell_dialogs/select_file_utils_win_unittest.cc
[add] https://crrev.com/c826f732d3ce8404bf2ffacf56a450796af72d9b/ui/shell_dialogs/select_file_utils_win.h
[delete] https://crrev.com/935534929e206e4e08510f2e19e10dc2fac0d0fa/ui/shell_dialogs/execute_select_file_win_unittest.cc
[modify] https://crrev.com/c826f732d3ce8404bf2ffacf56a450796af72d9b/ui/shell_dialogs/select_file_dialog_win.cc
[modify] https://crrev.com/c826f732d3ce8404bf2ffacf56a450796af72d9b/ui/shell_dialogs/BUILD.gn


### am...@chromium.org (2022-08-29)

[Empty comment from Monorail migration]

### am...@google.com (2022-08-30)

[Empty comment from Monorail migration]

### ad...@google.com (2022-09-26)

[Empty comment from Monorail migration]

### ad...@google.com (2022-09-26)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-07)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1342586?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/1342317, crbug.com/chromium/1343393]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060202)*
