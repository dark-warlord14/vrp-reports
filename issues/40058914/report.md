# Security:  Bypass Apk Warning In Andriod

| Field | Value |
|-------|-------|
| **Issue ID** | [40058914](https://issues.chromium.org/issues/40058914) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Downloads |
| **Platforms** | Android |
| **Reporter** | pu...@gmail.com |
| **Assignee** | qi...@chromium.org |
| **Created** | 2022-02-27 |
| **Bounty** | $1,000.00 |

## Description

Peace Be Upon You

Bypass Apk Warning In Chrome Andriod  

Using A Basic Html/Js Code  

Please Check The Code

**VERSION**  

Chrome Version: [93.0.4577.82]  

Operating System: [Andriod]

if you have any questions let me know

Thank You

## Attachments

- [Puf Demo.html](attachments/Puf Demo.html) (text/plain, 1.1 KB)
- [Apk Warning.jpg](attachments/Apk Warning.jpg) (image/jpeg, 77.5 KB)
- deleted (application/octet-stream, 0 B)
- [puf2.mp4](attachments/puf2.mp4) (video/mp4, 421.3 KB)

## Timeline

### pu...@gmail.com (2022-02-27)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-27)

[Empty comment from Monorail migration]

### pu...@gmail.com (2022-03-01)

Any Update ? 


### dc...@chromium.org (2022-03-03)

I tried this out on an Android device. I navigated to the test page and clicked [Open]. I got a dialog about where to save the file, followed immediately afterwards by a dialog that APKs might be harmful. So I don't see a bypass.

Can you clarify the steps, or explain where the bypass is?

### pu...@gmail.com (2022-03-03)

[Comment Deleted]

### [Deleted User] (2022-03-03)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pu...@gmail.com (2022-03-03)

Peace Be Upon You

I Have Tested In my Andriod 

it's working here

please check this file

thank you.

### dc...@chromium.org (2022-03-04)

Simplified repro:

<script>
function Puf(uri, name) {
  var link = document.createElement("a");
  link.download = name;
  link.href = uri;
  link.click();
}
function openWin()
{
Puf("data:application/vnd.android.package-archive;base64,UGVhY2UgQmUgVXBvbiBZb3U=", "apk.puf")
}
</script>
<input type="button" onclick="openWin();" value="open"/>

The problem is that the download is called apk.puf, and doesn't trigger the dangerous download prompt, but when we actually save the file, we add the apk extension (probably because of the MIME type).

Tagging with FoundIn-93 based on reporter's Chrome version, though the oldest I was able to test was 99.

[Monorail components: UI>Browser>Downloads]

### [Deleted User] (2022-03-04)

[Empty comment from Monorail migration]

### pu...@gmail.com (2022-03-04)

Peace Be Upon You

Is this valid bug sir ?

Thank you 

### [Deleted User] (2022-03-04)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### dc...@chromium.org (2022-03-05)

Yes, it looks like a valid bug to me--that's why it's tagged with a severity and an impact.

### pu...@gmail.com (2022-03-05)

Thank You ~

### qi...@chromium.org (2022-03-07)

This is an interesting bug. Chrome will create the filename apk.puf for the download. However, Android uses MediaStore to store all the downloads since Q. And MediaStore will change the file name when chrome creates the content URI.

### qi...@chromium.org (2022-03-09)

[Empty comment from Monorail migration]

### qi...@chromium.org (2022-03-09)

[Empty comment from Monorail migration]

### pu...@gmail.com (2022-03-10)

Peace Be Upon You

Are there any updates sir?

Thank you

### gi...@appspot.gserviceaccount.com (2022-03-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/49bbefe192eabd120f9af9aa1e18ab0116cce891

commit 49bbefe192eabd120f9af9aa1e18ab0116cce891
Author: Min Qin <qinmin@chromium.org>
Date: Thu Mar 17 21:11:18 2022

Fix an issue dangerous dialog is not shown for some apk download

On Android Q+, download will create a different intermediate content
Uri after target determination. However, creating the content Uri
might cause the file name to change, as Android tries to correct the
file name using MIME type. And the new file name may be of a dangerous
type.
However, the dangerous file check happens in target determination. So
creating the intermediate content Uri later allows such file names to
bypass dangerous file check.
This CL fixes the issue by moving content URI creation into target
determination stage, right before dangerous download check. And this
will also simplify the logic in DownloadItemImpl as it now gets the
target content Uri instead of an unused file path after target
determination.

BUG=1301180

Change-Id: Ie4561e8d0b4b3a87ec7a041f3ac71f23866fce04
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3508375
Reviewed-by: Xing Liu <xingliu@chromium.org>
Reviewed-by: Alex Moshchuk <alexmos@chromium.org>
Reviewed-by: Junbo Ke <juke@chromium.org>
Reviewed-by: Clark DuVall <cduvall@chromium.org>
Reviewed-by: Tommy Nyquist <nyquist@chromium.org>
Commit-Queue: Min Qin <qinmin@chromium.org>
Cr-Commit-Position: refs/heads/main@{#982422}

[modify] https://crrev.com/49bbefe192eabd120f9af9aa1e18ab0116cce891/components/download/public/common/download_file.h
[modify] https://crrev.com/49bbefe192eabd120f9af9aa1e18ab0116cce891/chrome/browser/download/download_target_determiner_unittest.cc
[modify] https://crrev.com/49bbefe192eabd120f9af9aa1e18ab0116cce891/chrome/browser/download/chrome_download_manager_delegate.h
[modify] https://crrev.com/49bbefe192eabd120f9af9aa1e18ab0116cce891/chrome/browser/download/download_target_info.h
[modify] https://crrev.com/49bbefe192eabd120f9af9aa1e18ab0116cce891/components/download/internal/common/in_progress_download_manager.cc
[modify] https://crrev.com/49bbefe192eabd120f9af9aa1e18ab0116cce891/weblayer/browser/download_manager_delegate_impl.cc
[modify] https://crrev.com/49bbefe192eabd120f9af9aa1e18ab0116cce891/chrome/browser/download/download_target_determiner.cc
[modify] https://crrev.com/49bbefe192eabd120f9af9aa1e18ab0116cce891/content/shell/browser/shell_download_manager_delegate.cc
[modify] https://crrev.com/49bbefe192eabd120f9af9aa1e18ab0116cce891/content/public/browser/download_manager_delegate.h
[modify] https://crrev.com/49bbefe192eabd120f9af9aa1e18ab0116cce891/chromecast/browser/cast_download_manager_delegate.cc
[modify] https://crrev.com/49bbefe192eabd120f9af9aa1e18ab0116cce891/components/download/public/common/download_utils.h
[modify] https://crrev.com/49bbefe192eabd120f9af9aa1e18ab0116cce891/content/browser/download/download_manager_impl.cc
[modify] https://crrev.com/49bbefe192eabd120f9af9aa1e18ab0116cce891/components/download/public/common/download_item_impl_delegate.h
[modify] https://crrev.com/49bbefe192eabd120f9af9aa1e18ab0116cce891/components/download/internal/common/download_item_impl_unittest.cc
[modify] https://crrev.com/49bbefe192eabd120f9af9aa1e18ab0116cce891/chrome/browser/lifetime/browser_close_manager_browsertest.cc
[modify] https://crrev.com/49bbefe192eabd120f9af9aa1e18ab0116cce891/components/download/internal/common/download_item_impl.cc
[modify] https://crrev.com/49bbefe192eabd120f9af9aa1e18ab0116cce891/chrome/browser/download/download_target_determiner_delegate.h
[modify] https://crrev.com/49bbefe192eabd120f9af9aa1e18ab0116cce891/chrome/browser/download/download_target_determiner.h
[modify] https://crrev.com/49bbefe192eabd120f9af9aa1e18ab0116cce891/chrome/browser/download/chrome_download_manager_delegate.cc
[modify] https://crrev.com/49bbefe192eabd120f9af9aa1e18ab0116cce891/content/browser/download/download_manager_impl_unittest.cc
[modify] https://crrev.com/49bbefe192eabd120f9af9aa1e18ab0116cce891/components/download/public/common/download_file_impl.h
[modify] https://crrev.com/49bbefe192eabd120f9af9aa1e18ab0116cce891/components/download/internal/common/download_utils.cc
[modify] https://crrev.com/49bbefe192eabd120f9af9aa1e18ab0116cce891/chrome/browser/download/chrome_download_manager_delegate_unittest.cc
[modify] https://crrev.com/49bbefe192eabd120f9af9aa1e18ab0116cce891/components/download/internal/common/download_item_impl_delegate.cc
[modify] https://crrev.com/49bbefe192eabd120f9af9aa1e18ab0116cce891/components/download/internal/common/download_file_impl.cc
[modify] https://crrev.com/49bbefe192eabd120f9af9aa1e18ab0116cce891/components/download/public/common/mock_download_item_impl.h
[modify] https://crrev.com/49bbefe192eabd120f9af9aa1e18ab0116cce891/content/browser/devtools/protocol/devtools_download_manager_delegate.cc
[modify] https://crrev.com/49bbefe192eabd120f9af9aa1e18ab0116cce891/components/download/public/common/download_item_impl.h


### gi...@appspot.gserviceaccount.com (2022-03-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/5bfe30827bd88638cfc6438ec4a283463e55bbb1

commit 5bfe30827bd88638cfc6438ec4a283463e55bbb1
Author: Min Qin <qinmin@chromium.org>
Date: Fri Mar 18 07:08:45 2022

Fix test failure on android 11 bots

BUG=1301180

Change-Id: I78789baf21e253df9705c8b433da8c088689e127
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3534549
Reviewed-by: Shakti Sahu <shaktisahu@chromium.org>
Commit-Queue: Min Qin <qinmin@chromium.org>
Cr-Commit-Position: refs/heads/main@{#982606}

[modify] https://crrev.com/5bfe30827bd88638cfc6438ec4a283463e55bbb1/components/download/internal/common/download_item_impl_unittest.cc
[modify] https://crrev.com/5bfe30827bd88638cfc6438ec4a283463e55bbb1/chrome/browser/download/chrome_download_manager_delegate_unittest.cc


### ma...@chromium.org (2022-03-18)

[Empty comment from Monorail migration]

### pu...@gmail.com (2022-03-23)

[Comment Deleted]

### [Deleted User] (2022-03-24)

qinmin: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pu...@gmail.com (2022-03-25)

[Empty comment from Monorail migration]

### pu...@gmail.com (2022-03-28)

Peace Be Upon You

 - is this eligible for VRP?

Thank You

### qi...@chromium.org (2022-03-28)

 I guess yes, but will leave it to the security team to decide.

### qi...@chromium.org (2022-03-28)

[Empty comment from Monorail migration]

### pu...@gmail.com (2022-03-28)

Thank You Very Much Sir

### pu...@gmail.com (2022-03-29)

[Comment Deleted]

### [Deleted User] (2022-03-29)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-29)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-29)

Requesting merge to beta M100 because latest trunk commit (982606) appears to be after beta branch point (972766).

Requesting merge to dev M101 because latest trunk commit (982606) appears to be after dev branch point (982481).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-03-29)

Merge approved: your change passed merge requirements and is auto-approved for M101. Please go ahead and merge the CL to branch 4951 (refs/branch-heads/4951) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: benmason (Android), harrysouders (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-03-29)

Merge review required: M100 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), harrysouders (iOS), dgagnon (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-03-31)

Hi qinmin@ -- this issue is already approved for merge to M101 (branch 4951), please merge this fix at your earliest convenience. 

As this is a rather textually large and non-trivial for a medium severity issue and M100 is now Stable channel, I am believe it may be best to hold off merging this to Stable channel for a respin and waiting to get this into M101. Please let me know if you see any issues with that. 


### am...@chromium.org (2022-03-31)

in response to https://crbug.com/chromium/1301180#c24 -- hello and thanks to your question, now that this issue has been resolved it will sent to the VRP Panel for consideration for a potential reward. This did not make the cutoff for this week, so it may be a couple of week until this issue is evaluated. The reward decision will be applied directly to this report, so you will see an update here when that happens. 

### pu...@gmail.com (2022-04-01)

Thank You So Much Sir
i have one question Sir
My English is Not Good, it will effect My reward ?
Thank You

### am...@chromium.org (2022-04-01)

Hello, thanks for your question, but no -- your English proficiency does not impact the VRP Reward. Reward judgements are solely made based on:
- bug impact
- report quality (how well the report explains the issue and impact of it and how well it demonstrates potential exploitability) 
- potential bonuses for exploits and analysis 

Please see https://g.co/chrome/vrp for our full VRP rules and policies. 

### pu...@gmail.com (2022-04-01)

[Comment Deleted]

### pu...@gmail.com (2022-04-01)

[Comment Deleted]

### [Deleted User] (2022-04-05)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### qi...@chromium.org (2022-04-05)

[Empty comment from Monorail migration]

### xi...@chromium.org (2022-04-05)

[Empty comment from Monorail migration]

### am...@google.com (2022-04-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-04-14)

Congratulations! The VRP Panel has decided to award you $1,000 for your report. A member of our finance team will be in touch with you soon to arrange payment. 
Please let us know the name (or tag/handle/other identifier) you would like us to use in providing acknowledgement to you for reporting this issue. 
Thank you for your efforts and reporting this issue to us. 

### pu...@gmail.com (2022-04-15)

Thank You! Sir

Name : Umar Farooq


### am...@google.com (2022-04-16)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-04-25)

[Empty comment from Monorail migration]

### am...@google.com (2022-04-26)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-05)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2022-07-26)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-29)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1301180?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1307647]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058914)*
