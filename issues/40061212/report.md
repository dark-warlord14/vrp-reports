# UAF in SelectFileDialogLinuxKde::CallKDialogOutput

| Field | Value |
|-------|-------|
| **Issue ID** | [40061212](https://issues.chromium.org/issues/40061212) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser |
| **Platforms** | Linux |
| **Reporter** | ro...@gmail.com |
| **Assignee** | lu...@chromium.org |
| **Created** | 2022-10-03 |
| **Bounty** | $7,000.00 |

## Description

**Steps to reproduce the problem:**  

1.prepare a kde desktop linux and launch chrome.  

2.python -m SimHTTPServer.  

3.run out/asan/chrome.  

4.Browse <http://localhost:8000/poc.html>.  

5.click the save and close the tab.  

6.UAF happen.

**Problem Description:**  

This bug was introduced in <https://chromium-review.googlesource.com/c/chromium/src/+/3764409>.

SelectFileDialogLinuxKde::CreateSelectFolderDialog will pass a weakptr to pipe\_task\_runner. pipe\_task\_runner is a threadpool sequence. And if the SelectFileDialogLinuxKde was created by pdfprinthandler. Then the lifetime of SelectFileDialogLinuxKde will be bound to the current Webcontent. If current Webcontents was destroyed when CallKDialogOutput is running in the threadpool. Then UAF happen.  

void SelectFileDialogLinuxKde::CreateSelectFolderDialog(  

Type type,  

const std::string& title,  

const base::FilePath& default\_path,  

gfx::AcceleratedWidget parent,  

void\* params) {  

int title\_message\_id = (type == SELECT\_UPLOAD\_FOLDER)  

? IDS\_SELECT\_UPLOAD\_FOLDER\_DIALOG\_TITLE  

: IDS\_SELECT\_FOLDER\_DIALOG\_TITLE;  

scoped\_refptr<RefCountedKDialogOutputParams> results =  

base::MakeRefCounted<RefCountedKDialogOutputParams>();  

pipe\_task\_runner\_->PostTaskAndReply(  

FROM\_HERE,  

base::BindOnce(  

&SelectFileDialogLinuxKde::CallKDialogOutput, base::AsWeakPtr(this), ------[1]  

KDialogParams(  

"--getexistingdirectory", GetTitle(title, title\_message\_id),  

default\_path.empty() ? \*last\_opened\_path() : default\_path, parent,  

false, false),  

results),  

base::BindOnce(  

&SelectFileDialogLinuxKde::OnSelectSingleFolderDialogResponse,  

base::AsWeakPtr(this), parent, params, results));  

}

**Additional Comments:**

\*\*Chrome version: \*\* 106.0.0.0 \*\*Channel: \*\* Not sure

**OS:** Linux

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 34.6 KB)
- [poc.html](attachments/poc.html) (text/plain, 72 B)
- [Screenshot from 2022-10-17 09-21-16.png](attachments/Screenshot from 2022-10-17 09-21-16.png) (image/png, 224.2 KB)

## Timeline

### [Deleted User] (2022-10-03)

[Empty comment from Monorail migration]

### ro...@gmail.com (2022-10-03)

[Comment Deleted]

### mp...@chromium.org (2022-10-03)

[Empty comment from Monorail migration]

[Monorail components: Platform>Apps>FileManager UI>Browser]

### [Deleted User] (2022-10-03)

[Empty comment from Monorail migration]

### lu...@chromium.org (2022-10-04)

I've reverted the CL that caused the issue.

I'll keep this bug open and assigned to me to fix this issue before re-introducing that change.

Note that the offending CL isn't a top priority for me, so this might be open for a while without update.

### [Deleted User] (2022-10-04)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-10-04)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-10-04)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### lu...@chromium.org (2022-10-05)

The CL the introduced the issue has been reverted:
https://chromium-review.googlesource.com/c/chromium/src/+/3930092

I'll close this bug for now and will follow up with the proper fix on the bug:
https://bugs.chromium.org/p/chromium/issues/detail?id=1316211

### am...@chromium.org (2022-10-05)

Since this is an externally reported / VRP it should stay open until the fix is landed, please also link this issue number in the fix CL when you land the fix in https://crbug.com/chromium/1316211. Reopening and marking as blockedon https://crbug.com/chromium/1316211. 

### am...@chromium.org (2022-10-05)

[Empty comment from Monorail migration]

### lu...@chromium.org (2022-10-05)

The CL that fixed the issue has already landed.
https://chromium-review.googlesource.com/c/chromium/src/+/3930092

Unfortunately it isn't directly linked in the bug. 

This bug isn't blocked by 1316211, I'll only reland the code for 1316211 after fixing this UAF. Until then, this bug doesn't affect users anymore.

I'm closing the bug because I'm receiving reminders that I own a release blocker. Now I don't have more actions to take on this bug.

### [Deleted User] (2022-10-06)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-06)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-10-14)

Thank you for this report. The VRP Panel must unfortunately decline a reward for this issue as this issue was part of ongoing work and previously known at the time of this report and prior. 

### ro...@gmail.com (2022-10-14)

[Comment Deleted]

### am...@chromium.org (2022-10-14)

Hello, this work in which this bug was introduced was ongoing in in progress as part of a greater refactor as reported and in progress in https://crbug.com/chromium/1316211, which began back in April. 
We tend to discourage hunting for bugs in head/main for this particular reason, as these collisions are prone to happen. Given the ongoing efforts in 1316211 and the greater documentation of the work planned there, we feel like there is clear evidence this would have been resolved. 

### ro...@gmail.com (2022-10-14)

[Comment Deleted]

### am...@chromium.org (2022-10-14)

Hi rox! I just chatted with the developer on this issue who was kind enough to take the time to reach out about this issue. They conveyed they find this report genuinely helpful in understanding a different type of UAF that they had not yet identified and was introduced by their code that you pointed out. 
Based on that, this issue will go back to the VRP Panel next week for an assessment of a potential VRP reward. :) 

### ro...@gmail.com (2022-10-14)

[Comment Deleted]

### [Deleted User] (2022-10-14)

This is sufficiently serious that it should be merged to dev. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M108. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-10-14)

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

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
Owners: govind (Android), harrysouders (iOS), obenedict (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### lu...@chromium.org (2022-10-16)

The fix is already merged on M108:
https://chromium-review.googlesource.com/c/chromium/src/+/3930092



### am...@google.com (2022-10-20)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-10-20)

Congratulations, Rox! The VRP Panel has decided to award you $7,000 for this report of a mildly mitigated security bug. Thank you for your efforts in discovering and reporting this issue to us -- nice work!

### ro...@gmail.com (2022-10-20)

Thanks！

### am...@google.com (2022-10-21)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-12)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1370439?no_tracker_redirect=1

[Multiple monorail components: Platform>Apps>FileManager, UI>Browser]
[Monorail blocked-on: crbug.com/chromium/1316211]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061212)*
