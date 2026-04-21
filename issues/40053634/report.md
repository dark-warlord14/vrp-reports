# Security: chrome.debugger API bypasses the runtime_blocked_hosts Enterprise policy

| Field | Value |
|-------|-------|
| **Issue ID** | [40053634](https://issues.chromium.org/issues/40053634) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Enterprise, Platform>Extensions |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ro...@robwu.nl |
| **Assignee** | so...@chromium.org |
| **Created** | 2020-10-16 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**  

The ExtensionSettings.\*.runtime\_blocked\_hosts Enterprise policy is supposed to prevent extensions from accessing web content at the given hosts, regardless of the permissions declared by the extension. This is however not enforced for the chrome.debugger extension API. This allows extensions to bypass the security restrictions as configured by the enterprise policy.

**VERSION**  

Chrome Version: 86.0.4240.75 (stable) + 88.0.4294.0 (latest canary)  

Operating System: Tested with Linux, but applies to any.

**REPRODUCTION CASE**

1. Download the attached files (manifest.json, background.js, contentscript.js) and put it in a directory - the extension directory.
2. Create an Enterprise policy to block a domain, e.g. google.com. I believe that this policy is already active for Googlers, so if you are a Googler you could skip this step.  
   
   To configure on Chromium for Linux, put the following in /etc/chromium/policies/managed/block-google.json:

{  

"ExtensionSettings": {  

"\*": {  

"runtime\_blocked\_hosts": ["\*://\*.google.com"],  

"blocked\_permissions": []  

}  

}  

}

For Chrome or other platforms, see:  

\* Windows - <https://support.google.com/chrome/a/answer/7532015>  

\* macOS - <https://support.google.com/chrome/a/answer/7517624>  

\* Linux - <https://support.google.com/chrome/a/answer/7517525>

3. Start Chrome and visit chrome://policy to verify that the policy is active.
4. Visit chrome://extensions, enable developer mode and select the directory from step 1.
5. Visit an unrelated domain such as example.com to see that the extension is active. It will turn the page yellow and replace the content with "Added by content script" and "Added by chrome.debugger API"
6. Visit google.com/robots.txt

Expected:

- google.com/robots.txt should not be modified.

Actual:

- BAD: google.com/robots.txt became yellow and contains "Added by chrome.debugger API"
- (good: google.com/robots.txt does not have "Added by content script", as expected: i.e. the policy was partially effective)

## Attachments

- [manifest.json](attachments/manifest.json) (text/plain, 391 B)
- [background.js](attachments/background.js) (text/plain, 1.2 KB)
- [contentscript.js](attachments/contentscript.js) (text/plain, 141 B)

## Timeline

### bd...@chromium.org (2020-10-16)

Assigning to @caseq as there are other chrome.debugger bugs also assigned to them. 

### [Deleted User] (2020-10-30)

caseq: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-10-30)

[Empty comment from Monorail migration]

### ca...@chromium.org (2020-11-03)

Devlin, I'd rather keep the logic of chrome.debugger-specific permission checks down to the absolute minimum and try to rely on the common extension permission checks to the extent possible. Is there a better way to check URL access than we do here? https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/extensions/api/debugger/debugger_api.cc;drc=1ca6a4e6f1506c9f8cad9e3151608582e145b923;l=101

Shouldn't this API account for the policy overrides?


### [Deleted User] (2020-11-13)

devlin: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rd...@chromium.org (2020-11-19)

PermissionsData::IsRestrictedUrl() essentially checks if the URL is off-limits to all extensions by the Chrome browser, rather than off-limits to the extension.  Most access checks should use CanAccessPage() (which is actually called out here [1]).  Unfortunately, I don't think that works well with the debugger permission, which more implicitly grants access to everything (rather than explicitly adding host permissions).

One possibility would be to roll the policy host checks into IsRestrictedUrl().  I haven't done an audit of the other callsites to see whether that would make sense or not.

A simple-and-safe, though somewhat ugly, solution would be to check IsPolicyBlockedHost() in addition to IsRestrictedUrl() - that would probably be the path of least resistance (and what I'd start with, particularly, if we'd want to merge this back).

I won't be able to tackle this issue this week, but might be able to next week.  If anyone else can jump sooner, feel free.

[1] https://source.chromium.org/chromium/chromium/src/+/master:extensions/common/permissions/permissions_data.h;l=97;drc=efba8d2927574721d8e9c39c444a0c363694c312

### rd...@chromium.org (2020-11-19)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-20)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-03)

[Empty comment from Monorail migration]

### rd...@chromium.org (2021-03-04)

I haven't had the bandwidth to dig into this one much, and might not in the immediate future.

Karan, can you take a look?  https://crbug.com/chromium/1139156#c6 has some possible approaches.  I think for the near term, it might be best to start with the simplest approach of checking IsPolicyBlockedHost() directly in the debugger API, and then subsequently checking if we could include that more directly in IsRestrictedURL().

### [Deleted User] (2021-03-11)

[Empty comment from Monorail migration]

### zh...@google.com (2021-03-17)

[Empty comment from Monorail migration]

### ka...@chromium.org (2021-03-19)

[Empty comment from Monorail migration]

### rd...@chromium.org (2021-03-30)

Apologies; busy time for a lot of folks.  karandeepb@ mentioned he may not be able to get to this right away, but solomonkinard@ has graciously said he should be able to investigate.

solomonkinard@, can you take a look?  See https://crbug.com/chromium/1139156#c6 and https://crbug.com/chromium/1139156#c12 for some starting points.  crrev.com/1ca6a4e6f1506c9f8cad9e3151608582e145b923 is probably also a good example of how a fix / test in this area looks.

### so...@chromium.org (2021-03-30)

Looking. Thanks.

### so...@chromium.org (2021-04-05)

crrev.com/c/2803843

### gi...@appspot.gserviceaccount.com (2021-04-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/3565a34c63962a3d92310f1f2434dfa17fb2fa78

commit 3565a34c63962a3d92310f1f2434dfa17fb2fa78
Author: Solomon Kinard <solomonkinard@chromium.org>
Date: Wed Apr 07 22:29:27 2021

Extensions: Policy blocked hosts supersede `debugger` permission

Bug: 1139156
Change-Id: Iade012ca814b872d156763b034fbc2be1a647502
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2803843
Commit-Queue: Solomon Kinard <solomonkinard@chromium.org>
Reviewed-by: Karan Bhatia <karandeepb@chromium.org>
Reviewed-by: Devlin <rdevlin.cronin@chromium.org>
Cr-Commit-Position: refs/heads/master@{#870242}

[modify] https://crrev.com/3565a34c63962a3d92310f1f2434dfa17fb2fa78/chrome/browser/extensions/api/debugger/debugger_api.cc
[modify] https://crrev.com/3565a34c63962a3d92310f1f2434dfa17fb2fa78/chrome/browser/extensions/api/debugger/debugger_apitest.cc


### so...@chromium.org (2021-04-07)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-08)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-08)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-08)

Requesting merge to beta M90 because latest trunk commit (870242) appears to be after beta branch point (857950).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-04-08)

This bug requires manual review: We are only 4 days from stable.
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
Owners: govind@(Android), bindusuvarna@(iOS), cindyb@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2021-04-15)

Approving merge to M90; please merge to branch 4430, unless you have any stability or backwards-compatibility concerns in which case it's fine to leave this to ship in M91.

### sr...@google.com (2021-04-20)

Please complete your merges before thursday EOD PST, so these security fixes can go out in next M90 respin

### sr...@google.com (2021-04-22)

moving to assigned state to get attention for the pending merge

### so...@chromium.org (2021-04-22)

Thanks. crrev.com/c/2847204

### so...@chromium.org (2021-04-22)

Rubber Stamper: The change is not in the configured time window. Rubber Stamper is only allowed to review cherry-picks within 14 day(s). Learn more: go/rubber-stamper-user-guide.

### so...@chromium.org (2021-04-22)

I've just been told that the TPM that approved the merge can add a TPM override. Hopefully that person is subscribed to this thread.

### gi...@appspot.gserviceaccount.com (2021-04-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b440129ce7aaf7f9be0a1d4de7e58b8d344d7105

commit b440129ce7aaf7f9be0a1d4de7e58b8d344d7105
Author: Solomon Kinard <solomonkinard@chromium.org>
Date: Thu Apr 22 23:10:14 2021

[Merge M90][Extensions] Policy blocked hosts supersede `debugger`

(cherry picked from commit 3565a34c63962a3d92310f1f2434dfa17fb2fa78)

Bug: 1139156
Change-Id: Iade012ca814b872d156763b034fbc2be1a647502
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2803843
Commit-Queue: Solomon Kinard <solomonkinard@chromium.org>
Reviewed-by: Karan Bhatia <karandeepb@chromium.org>
Reviewed-by: Devlin <rdevlin.cronin@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#870242}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2847204
Auto-Submit: Solomon Kinard <solomonkinard@chromium.org>
Cr-Commit-Position: refs/branch-heads/4430@{#1334}
Cr-Branched-From: e5ce7dc4f7518237b3d9bb93cccca35d25216cbe-refs/heads/master@{#857950}

[modify] https://crrev.com/b440129ce7aaf7f9be0a1d4de7e58b8d344d7105/chrome/browser/extensions/api/debugger/debugger_api.cc
[modify] https://crrev.com/b440129ce7aaf7f9be0a1d4de7e58b8d344d7105/chrome/browser/extensions/api/debugger/debugger_apitest.cc


### am...@google.com (2021-04-22)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### [Deleted User] (2021-04-23)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-04-23)

[Empty comment from Monorail migration]

### so...@chromium.org (2021-04-23)

This was merged to M90 yesterday.

### am...@google.com (2021-04-23)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-04-23)

Hello Rob! Apologies for the late note, but congratulations! As you can see the VRP Panel has decided to award you $5000 for this report. Please also look out for the email I sent out to the VRP researchers community about forthcoming changes and temporarily delays in payment process starting this week! 

### as...@google.com (2021-04-26)

[Empty comment from Monorail migration]

### am...@google.com (2021-04-26)

[Empty comment from Monorail migration]

### gi...@google.com (2021-04-27)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-04-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/7490441baa47a74f7e4e789aca0df594cb1bbaf0

commit 7490441baa47a74f7e4e789aca0df594cb1bbaf0
Author: Solomon Kinard <solomonkinard@chromium.org>
Date: Tue Apr 27 12:31:55 2021

M86-LTS: Extensions: Policy blocked hosts supersede `debugger` permission

M86 merge conflicts and resolution:
* chrome/browser/extensions/api/debugger/debugger_apitest.cc
  Diff could not automatically find the place for new test. Add it
  as is manually.

(cherry picked from commit 3565a34c63962a3d92310f1f2434dfa17fb2fa78)

Bug: 1139156
Change-Id: Iade012ca814b872d156763b034fbc2be1a647502
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2803843
Commit-Queue: Solomon Kinard <solomonkinard@chromium.org>
Reviewed-by: Karan Bhatia <karandeepb@chromium.org>
Reviewed-by: Devlin <rdevlin.cronin@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#870242}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2848172
Reviewed-by: Victor-Gabriel Savu <vsavu@google.com>
Commit-Queue: Artem Sumaneev <asumaneev@google.com>
Owners-Override: Artem Sumaneev <asumaneev@google.com>
Cr-Commit-Position: refs/branch-heads/4240@{#1622}
Cr-Branched-From: f297677702651916bbf65e59c0d4bbd4ce57d1ee-refs/heads/master@{#800218}

[modify] https://crrev.com/7490441baa47a74f7e4e789aca0df594cb1bbaf0/chrome/browser/extensions/api/debugger/debugger_api.cc
[modify] https://crrev.com/7490441baa47a74f7e4e789aca0df594cb1bbaf0/chrome/browser/extensions/api/debugger/debugger_apitest.cc


### as...@google.com (2021-04-27)

[Empty comment from Monorail migration]

### am...@google.com (2021-04-30)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-03)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1139156?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Enterprise, Platform>Extensions]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40053634)*
