# Security:  Use After Free in JavaScriptDialogHelper::OnPermissionResponse

| Field | Value |
|-------|-------|
| **Issue ID** | [40059961](https://issues.chromium.org/issues/40059961) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Platform>Apps>BrowserTag |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ka...@gmail.com |
| **Assignee** | mc...@chromium.org |
| **Created** | 2022-06-14 |
| **Bounty** | $16,000.00 |

## Description

**VULNERABILITY DETAILS**

Root cause:  

Use of Unretained(this) can cause UAF when OnPermissionResponse is called as a callback.

Code link:  

<https://source.chromium.org/chromium/chromium/src/+/main:extensions/browser/guest_view/web_view/javascript_dialog_helper.cc;l=67;drc=3e5c589a0a562f655182c1453b773df4eb6d1a82>

web\_view\_permission\_helper->RequestPermission(  

WEB\_VIEW\_PERMISSION\_TYPE\_JAVASCRIPT\_DIALOG, request\_info,  

base::BindOnce(&JavaScriptDialogHelper::OnPermissionResponse,  

base::Unretained(this), std::move(callback)),

Detail:  

Based on the code below, in the function RunJavaScriptDialog, it will call web\_view\_permission\_helper->RequestPermission to ask for the right permission to run the dialog.  

When the length of pending\_permission\_requests\_ already reached to kMaxOutstandingPermissionRequests. A Task will be posted to run the callback passed in, asynchronously.  

However, the first argument bound to the callback(OnPermissionResponse) was a raw pointer. When the webview itself was destroyed before running the Task, the instance of JavaScriptDialogHelper will also be freed, which leads to UAF.

<https://source.chromium.org/chromium/chromium/src/+/main:extensions/browser/guest_view/web_view/javascript_dialog_helper.cc;l=64;drc=3e5c589a0a562f655182c1453b773df4eb6d1a82>

web\_view\_permission\_helper->RequestPermission(  

WEB\_VIEW\_PERMISSION\_TYPE\_JAVASCRIPT\_DIALOG, request\_info,  

base::BindOnce(&JavaScriptDialogHelper::OnPermissionResponse,  

base::Unretained(this), std::move(callback)),  

false /\* allowed\_by\_default \*/);

<https://source.chromium.org/chromium/chromium/src/+/main:extensions/browser/guest_view/web_view/web_view_permission_helper.cc;l=282;drc=0efb6d773049903754513a26452384975fd06740>

if (pending\_permission\_requests\_.size() >=  

webview::kMaxOutstandingPermissionRequests) {  

// Let the stack unwind before we deny the permission request so that  

// objects held by the permission request are not destroyed immediately  

// after creation. This is to allow those same objects to be accessed again  

// in the same scope without fear of use after freeing.  

base::ThreadTaskRunnerHandle::Get()->PostTask(  

FROM\_HERE,  

base::BindOnce(std::move(callback), allowed\_by\_default, std::string()));  

return webview::kInvalidPermissionRequestID;  

}

**VERSION**  

Chrome Version: [102.0.5005.115] + [stable]

**REPRODUCTION CASE**

1. Download the attached files to your working directory
2. Setup httpserver  
   
   python -m SimpleHTTPServer 8000
3. Elsewhere run  
   
   .\chrome.exe --load-extension=<your working directory>
4. Wait a few seconds to see the crash log. If it's not show in 10 seconds, kill the browser process and restart from step 3.

FIX  

The attached fix.diff shows my suggestion about how to fix this issue by changing the Unretained(this) to WeakPtr.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: browser

**CREDIT INFORMATION**  

Reporter credit: anonymous

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 16.1 KB)
- [manifest.json](attachments/manifest.json) (text/plain, 168 B)
- [backgroud.js](attachments/backgroud.js) (text/plain, 51 B)
- [index.html](attachments/index.html) (text/plain, 48 B)
- [main.js](attachments/main.js) (text/plain, 755 B)
- [poc.html](attachments/poc.html) (text/plain, 277 B)
- [fix.diff](attachments/fix.diff) (text/plain, 1.6 KB)

## Timeline

### [Deleted User] (2022-06-14)

[Empty comment from Monorail migration]

### xi...@chromium.org (2022-06-15)

Thanks for the report! +avi@ based on the blame history. Normally UaF in browser process is critical, but since installing an extension is required, setting it to high.

[Monorail components: Platform>Apps>BrowserTag]

### [Deleted User] (2022-06-15)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-16)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mc...@chromium.org (2022-06-20)

Hi. Thanks for the report.

The poc doesn't seem to be working for me, but I agree with the analysis in the description and the suggested fix.

Fortunately, it looks like all the other callers of RequestPermission are already using weak ptrs.

### gi...@appspot.gserviceaccount.com (2022-06-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/1c09b9292dba7dfdc28b9bd09c61e3a0faf7b302

commit 1c09b9292dba7dfdc28b9bd09c61e3a0faf7b302
Author: Kevin McNee <mcnee@chromium.org>
Date: Mon Jun 20 18:04:34 2022

Use weak ptr for webview JavaScriptDialogHelper callback

This can be called asynchronously, potentially after the associated
WebViewGuest is destroyed.

Bug: 1336266
Change-Id: I8a4ec5ab124a9d5ca2ad45b1915666c8b7c98f79
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3715049
Reviewed-by: James Maclean <wjmaclean@chromium.org>
Auto-Submit: Kevin McNee <mcnee@chromium.org>
Commit-Queue: James Maclean <wjmaclean@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1015960}

[modify] https://crrev.com/1c09b9292dba7dfdc28b9bd09c61e3a0faf7b302/extensions/browser/guest_view/web_view/javascript_dialog_helper.cc
[modify] https://crrev.com/1c09b9292dba7dfdc28b9bd09c61e3a0faf7b302/extensions/browser/guest_view/web_view/javascript_dialog_helper.h


### mc...@chromium.org (2022-06-20)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-21)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-21)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-21)

Requesting merge to stable M102 because latest trunk commit (1015960) appears to be after stable branch point (992738).

Requesting merge to beta M103 because latest trunk commit (1015960) appears to be after beta branch point (1002911).

Requesting merge to dev M104 because latest trunk commit (1015960) appears to be after dev branch point (1012729).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-06-21)

Merge review required: M103 is already shipping to stable.

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
Owners: govind (Android), harrysouders (iOS), dgagnon (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-06-21)

Merge review required: M102 is already shipping to stable.

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
Owners: eakpobaro (Android), harrysouders (iOS), ceb (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-06-21)

Merge approved: your change passed merge requirements and is auto-approved for M104. Please go ahead and merge the CL to branch 5112 (refs/branch-heads/5112) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: eakpobaro (Android), harrysouders (iOS), obenedict (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2022-06-24)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-06-24)

Congratulations! The VRP Panel has decided to award you $16,000 for this report. Thank you for your efforts and reporting this issue to us - great work! 

### mc...@chromium.org (2022-06-24)

Regarding merges:
1. This is a fix for a security issue (UAF).
2. https://chromium-review.googlesource.com/c/chromium/src/+/3715049
3. It has been released on canary without issue. However, I haven't tested canary explicitly, since I was unable to get the poc to work for me (see https://crbug.com/chromium/1336266#c5).
4. No
5. N/A
6. No

### gi...@appspot.gserviceaccount.com (2022-06-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/5127878b838941503511e6a40fd20ef58fa8daa2

commit 5127878b838941503511e6a40fd20ef58fa8daa2
Author: Kevin McNee <mcnee@chromium.org>
Date: Fri Jun 24 17:16:18 2022

M104: Use weak ptr for webview JavaScriptDialogHelper callback

Use weak ptr for webview JavaScriptDialogHelper callback

This can be called asynchronously, potentially after the associated
WebViewGuest is destroyed.

(cherry picked from commit 1c09b9292dba7dfdc28b9bd09c61e3a0faf7b302)

Bug: 1336266
Change-Id: I8a4ec5ab124a9d5ca2ad45b1915666c8b7c98f79
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3715049
Reviewed-by: James Maclean <wjmaclean@chromium.org>
Auto-Submit: Kevin McNee <mcnee@chromium.org>
Commit-Queue: James Maclean <wjmaclean@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1015960}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3723947
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/5112@{#273}
Cr-Branched-From: b13d3fe7b3c47a56354ef54b221008afa754412e-refs/heads/main@{#1012729}

[modify] https://crrev.com/5127878b838941503511e6a40fd20ef58fa8daa2/extensions/browser/guest_view/web_view/javascript_dialog_helper.cc
[modify] https://crrev.com/5127878b838941503511e6a40fd20ef58fa8daa2/extensions/browser/guest_view/web_view/javascript_dialog_helper.h


### [Deleted User] (2022-06-24)

LTS Milestone M102

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mc...@chromium.org (2022-06-24)

Re https://crbug.com/chromium/1336266#c18:
1. No, this was an existing issue.
2. No.

### rz...@google.com (2022-06-27)

[Empty comment from Monorail migration]

### rz...@google.com (2022-06-27)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-27)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2022-06-27)

1.  Just https://crrev.com/c/3726008
2. Low, simple conflicts for a member regarding its type
3. 104
4. Yes

### gm...@google.com (2022-06-27)

[Empty comment from Monorail migration]

### am...@google.com (2022-07-01)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-08)

M102/M103 merges approved; please merge this fix to M102/ES (branch 5005) and M103/Stable (5060) at your earliest convenience. Thank you! 

### gm...@google.com (2022-07-11)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-11)

LTS Milestone M102

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mc...@chromium.org (2022-07-11)

M102 and M103 merges:
https://chromium-review.googlesource.com/c/chromium/src/+/3755322
https://chromium-review.googlesource.com/c/chromium/src/+/3755452

### gi...@appspot.gserviceaccount.com (2022-07-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/767e9de4da9dade622515d62a3c4ea2b78ed616f

commit 767e9de4da9dade622515d62a3c4ea2b78ed616f
Author: Kevin McNee <mcnee@chromium.org>
Date: Mon Jul 11 22:07:40 2022

M103: Use weak ptr for webview JavaScriptDialogHelper callback

Use weak ptr for webview JavaScriptDialogHelper callback

This can be called asynchronously, potentially after the associated
WebViewGuest is destroyed.

(cherry picked from commit 1c09b9292dba7dfdc28b9bd09c61e3a0faf7b302)

Bug: 1336266
Change-Id: I8a4ec5ab124a9d5ca2ad45b1915666c8b7c98f79
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3715049
Reviewed-by: James Maclean <wjmaclean@chromium.org>
Auto-Submit: Kevin McNee <mcnee@chromium.org>
Commit-Queue: James Maclean <wjmaclean@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1015960}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3755452
Cr-Commit-Position: refs/branch-heads/5060@{#1197}
Cr-Branched-From: b83393d0f4038aeaf67f970a024d8101df7348d1-refs/heads/main@{#1002911}

[modify] https://crrev.com/767e9de4da9dade622515d62a3c4ea2b78ed616f/extensions/browser/guest_view/web_view/javascript_dialog_helper.cc
[modify] https://crrev.com/767e9de4da9dade622515d62a3c4ea2b78ed616f/extensions/browser/guest_view/web_view/javascript_dialog_helper.h


### [Deleted User] (2022-07-12)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-07-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/1eb2af928ada1a00f26d7379e00c3c3f7a9749f4

commit 1eb2af928ada1a00f26d7379e00c3c3f7a9749f4
Author: Kevin McNee <mcnee@chromium.org>
Date: Thu Jul 14 16:15:42 2022

M102: Use weak ptr for webview JavaScriptDialogHelper callback

Use weak ptr for webview JavaScriptDialogHelper callback

This can be called asynchronously, potentially after the associated
WebViewGuest is destroyed.

(cherry picked from commit 1c09b9292dba7dfdc28b9bd09c61e3a0faf7b302)

Bug: 1336266
Change-Id: I8a4ec5ab124a9d5ca2ad45b1915666c8b7c98f79
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3715049
Reviewed-by: James Maclean <wjmaclean@chromium.org>
Auto-Submit: Kevin McNee <mcnee@chromium.org>
Commit-Queue: James Maclean <wjmaclean@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1015960}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3755322
Commit-Queue: Kevin McNee <mcnee@chromium.org>
Cr-Commit-Position: refs/branch-heads/5005@{#1245}
Cr-Branched-From: 5b4d9450fee01f821b6400e947b3839727643a71-refs/heads/main@{#992738}

[modify] https://crrev.com/1eb2af928ada1a00f26d7379e00c3c3f7a9749f4/extensions/browser/guest_view/web_view/javascript_dialog_helper.cc
[modify] https://crrev.com/1eb2af928ada1a00f26d7379e00c3c3f7a9749f4/extensions/browser/guest_view/web_view/javascript_dialog_helper.h


### am...@chromium.org (2022-07-19)

[Empty comment from Monorail migration]

### gm...@google.com (2022-07-19)

[Empty comment from Monorail migration]

### am...@google.com (2022-07-19)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-07-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/15221b0f1fd79040ce5f99c2f2c955ff98d71b23

commit 15221b0f1fd79040ce5f99c2f2c955ff98d71b23
Author: Kevin McNee <mcnee@chromium.org>
Date: Wed Jul 20 09:53:43 2022

[M96-LTS] Use weak ptr for webview JavaScriptDialogHelper callback

M96 merge issues:
  javascript_dialog_helper.h:
    Conflicting types for web_view_guest_

This can be called asynchronously, potentially after the associated
WebViewGuest is destroyed.

(cherry picked from commit 1c09b9292dba7dfdc28b9bd09c61e3a0faf7b302)

Bug: 1336266
Change-Id: I8a4ec5ab124a9d5ca2ad45b1915666c8b7c98f79
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3715049
Auto-Submit: Kevin McNee <mcnee@chromium.org>
Commit-Queue: James Maclean <wjmaclean@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1015960}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3726008
Reviewed-by: Simon Hangl <simonha@google.com>
Owners-Override: Simon Hangl <simonha@google.com>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Cr-Commit-Position: refs/branch-heads/4664@{#1665}
Cr-Branched-From: 24dc4ee75e01a29d390d43c9c264372a169273a7-refs/heads/main@{#929512}

[modify] https://crrev.com/15221b0f1fd79040ce5f99c2f2c955ff98d71b23/extensions/browser/guest_view/web_view/javascript_dialog_helper.cc
[modify] https://crrev.com/15221b0f1fd79040ce5f99c2f2c955ff98d71b23/extensions/browser/guest_view/web_view/javascript_dialog_helper.h


### rz...@google.com (2022-07-20)

[Empty comment from Monorail migration]

### rz...@google.com (2022-07-20)

Already merged to 102

### am...@google.com (2022-07-28)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-28)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-27)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1336266?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059961)*
