# Security: Abuse the user's system environment variables in <a> download attribute may cause DLL Hijacking or Path Interception 

| Field | Value |
|-------|-------|
| **Issue ID** | [40059165](https://issues.chromium.org/issues/40059165) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>PlatformIntegration, UI>Browser>Downloads |
| **Platforms** | Windows |
| **Reporter** | 0x...@gmail.com |
| **Assignee** | qi...@chromium.org |
| **Created** | 2022-03-21 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

Chrome treats the "Save as" as a trusted operation even if the file extension is .exe or .dll.(<https://support.google.com/chrome/answer/95759>)  

When we set the system environment variables in the <a> download attribute and save the file with "Save as", it will cause security issues such as dll hijacking

PS:Microsoft Edge(Chromium based) treats "save as" as a untrusted operation. So the dangerous file will not be downloaded successfully.

**VERSION**  

Chrome Version: [102.0.4955.0 (Developer Build) (64-bit)] + [stable, beta, or dev]  

Operating System: [Windows 10]

**REPRODUCTION CASE**  

See the poc.gif

## Attachments

- [download.html](attachments/download.html) (text/plain, 66 B)
- [poc.gif](attachments/poc.gif) (image/gif, 3.5 MB)
- [edge.gif](attachments/edge.gif) (image/gif, 1.7 MB)

## Timeline

### [Deleted User] (2022-03-21)

[Empty comment from Monorail migration]

### an...@chromium.org (2022-03-22)

Verified in M98.
Similar question about making "Save as" an untrusted operation as in Edge.


[Monorail components: Blink>Storage>FileSystem]

### [Deleted User] (2022-03-22)

[Empty comment from Monorail migration]

### me...@chromium.org (2022-03-22)

This doesn't seem related to the file system API (besides that we had a similar issue there), rather this might be a downloads related issue?

[Monorail components: -Blink>Storage>FileSystem UI>Browser>Downloads]

### [Deleted User] (2022-03-23)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ct...@chromium.org (2022-06-01)

I think there are two components here:

1) "Save As" not triggering download warnings for dangerous download types.
2) "Save As" appears to be expanding the environment variable and saving the file under a different name and *outside the users downloads directory*.

The latter seems particularly bad, maybe? I verified on my Windows machine that the file is saved to my AppData directory instead of my downloads folder. It also appears to also reproduce in Edge per the reporter's GIFs. Bumping the severity up to Medium until we can convince ourselves it is lower severity.

Adding some more folks: +drubery@ for safe browsing, +qinmin@ for downloads -- what do you think?

### dr...@chromium.org (2022-06-02)

I don't think we're going to do anything about 1). Warnings the user solely based on the file type has never been particularly effective. It has very high false positives and high click through rates. I'm still comfortable with the heuristic of "if the user explicitly chose the filename+extension, it's probably okay". If this were preventing us from contacting Safe Browsing at all, that would be concerning.

2) definitely seems like it could be a security bug, but that behavior is probably in downloads code.

### [Deleted User] (2022-06-02)

qinmin: Uh oh! This issue still open and hasn't been updated in the last 73 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### qi...@chromium.org (2022-06-08)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-06-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/9cdce354cb3b0da5b4b311638973d407be7712b6

commit 9cdce354cb3b0da5b4b311638973d407be7712b6
Author: Min Qin <qinmin@chromium.org>
Date: Wed Jun 15 20:04:48 2022

Sanitize default file name in windows select file dialog

On windows, '%' is a special character and can be used for environment
variables. So if the default file name is '%DATADIR%', it can actually
refer to another directory and thus causing weird behaviors.
And '%' cannot be escaped when used in the file dialog. Both "^%" and
"%%" don't work. This CL mitigates the issue by replacing '%' with '_'.
This only affects the default file name when showing the dialog. Power
users can still change the file name by adding '%' if needed.

BUG=1308422

Change-Id: Ibb275f5c3c2c9458c20d1e97ad527f7c95184eaa
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3688608
Reviewed-by: Robert Liao <robliao@chromium.org>
Commit-Queue: Min Qin <qinmin@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1014602}

[modify] https://crrev.com/9cdce354cb3b0da5b4b311638973d407be7712b6/ui/shell_dialogs/execute_select_file_win.h
[modify] https://crrev.com/9cdce354cb3b0da5b4b311638973d407be7712b6/ui/shell_dialogs/execute_select_file_win.cc
[modify] https://crrev.com/9cdce354cb3b0da5b4b311638973d407be7712b6/ui/shell_dialogs/execute_select_file_win_unittest.cc


### qi...@chromium.org (2022-06-15)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-16)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-16)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-06-29)

the bot is sleeping on the job and fix commit has only made it to 105, getting this into merge review queue for 104 as this is a medium severity bug 

### [Deleted User] (2022-06-29)

Merge rejected: M104 is already shipping to beta and this issue is marked as a Pri-2, Pri-3, or Type-Feature.

Please contact the milestone owner if you have questions.
Owners: eakpobaro (Android), harrysouders (iOS), obenedict (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ct...@chromium.org (2022-06-29)

Looks like I forgot to bump the priority when I increased the severity to Medium. Updating to P-1 per our security guidelines and re-requesting the merge.

### [Deleted User] (2022-06-29)

Merge review required: M104 is already shipping to beta.

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
Owners: eakpobaro (Android), harrysouders (iOS), obenedict (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2022-06-29)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-06-29)

Congratulations! The VRP Panel has decided to award you $2,000 for this report. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2022-07-01)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-08)

M104 merge approved, please merge this fix to branch 5112 at your earliest convenience. 

### [Deleted User] (2022-07-12)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sr...@google.com (2022-07-12)

This CL is approved for Merge to M104, Please help complete all merges before 3pm PST today ( July 12) so that these can be included in this week's beta release going out tomorrow,. I will be cutting RC build today at 3pm PST

### gi...@appspot.gserviceaccount.com (2022-07-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/54e32332750c2bf9e13e5d426281f50a3664ccf8

commit 54e32332750c2bf9e13e5d426281f50a3664ccf8
Author: Min Qin <qinmin@chromium.org>
Date: Tue Jul 12 19:48:53 2022

[Merge 104] Sanitize default file name in windows select file dialog

On windows, '%' is a special character and can be used for environment
variables. So if the default file name is '%DATADIR%', it can actually
refer to another directory and thus causing weird behaviors.
And '%' cannot be escaped when used in the file dialog. Both "^%" and
"%%" don't work. This CL mitigates the issue by replacing '%' with '_'.
This only affects the default file name when showing the dialog. Power
users can still change the file name by adding '%' if needed.

BUG=1308422

(cherry picked from commit 9cdce354cb3b0da5b4b311638973d407be7712b6)

Change-Id: Ibb275f5c3c2c9458c20d1e97ad527f7c95184eaa
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3688608
Reviewed-by: Robert Liao <robliao@chromium.org>
Commit-Queue: Min Qin <qinmin@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1014602}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3758469
Cr-Commit-Position: refs/branch-heads/5112@{#822}
Cr-Branched-From: b13d3fe7b3c47a56354ef54b221008afa754412e-refs/heads/main@{#1012729}

[modify] https://crrev.com/54e32332750c2bf9e13e5d426281f50a3664ccf8/ui/shell_dialogs/execute_select_file_win.h
[modify] https://crrev.com/54e32332750c2bf9e13e5d426281f50a3664ccf8/ui/shell_dialogs/execute_select_file_win.cc
[modify] https://crrev.com/54e32332750c2bf9e13e5d426281f50a3664ccf8/ui/shell_dialogs/execute_select_file_win_unittest.cc


### am...@chromium.org (2022-08-01)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-08-02)

[Empty comment from Monorail migration]

[Monorail components: Internals>PlatformIntegration]

### am...@google.com (2022-08-02)

[Empty comment from Monorail migration]

### am...@google.com (2022-08-12)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-08-12)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-22)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2022-09-22)

This issue was migrated from crbug.com/chromium/1308422?no_tracker_redirect=1

[Multiple monorail components: Internals>PlatformIntegration, UI>Browser>Downloads]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059165)*
