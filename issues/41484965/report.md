# Security: Enterprise Policy Bypass Vulnerability Allows Download of Internal/Blocked Files

| Field | Value |
|-------|-------|
| **Issue ID** | [41484965](https://issues.chromium.org/issues/41484965) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>Storage>FileSystem, UI>Browser>Downloads |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **CVE IDs** | CVE-2023-4904 |
| **Reporter** | fa...@gmail.com |
| **Assignee** | ha...@google.com |
| **Created** | 2023-12-16 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

The `window.showSaveFilePicker` file handle can bypass download policies set by an enterprise in Chrome.

**VERSION**  

Chrome Version: 120.0.6099.110 (Official Build) (64-bit) (cohort: M120 Rollout)  

Operating System: Windows 11

To set up Enterprise policy of Chrome on other platforms, see:  

\* Windows - <https://support.google.com/chrome/a/answer/7532015>  

\* macOS - <https://support.google.com/chrome/a/answer/7517624>  

\* Linux - <https://support.google.com/chrome/a/answer/7517525>

**REPRODUCTION CASE**

1. Download the `poc.html` file.
2. Set the enterprise policy using the following settings (which are configured to block all downloads by the enterprise):

```
{ "DownloadRestrictions": 3 }  

```

On Windows, go to `regedit.exe`,

`Computer\HKEY_CURRENT_USER\SOFTWARE\Policies\Google\Chrome`

and add a new value pair with the name `DownloadRestrictions` and the value `3`.

3. Check if this policy is applied in Chrome and visit the `poc.html` page to test downloads.

**CREDIT INFORMATION**  

Reporter credit: Shaheen Fazim

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 1.2 KB)
- [demo.mp4](attachments/demo.mp4) (video/mp4, 3.5 MB)

## Timeline

### fa...@gmail.com (2023-12-16)

Similar issue: https://crbug.com/1453501 (Reference: https://nvd.nist.gov/vuln/detail/CVE-2023-4904)

### [Deleted User] (2023-12-16)

[Empty comment from Monorail migration]

### fa...@gmail.com (2023-12-17)

Expected:
- Downloads should not be allowed when blocked by the enterprise policy.

Actual:
- The enterprise policy is successfully bypassed using showSaveFilePicker(), and files can be downloaded to the user's device.

### ch...@chromium.org (2023-12-18)

Thanks for your report.

I can reproduce on M120 on Linux. I imagine it applies to all platforms on which the policy exists.

I think the problem is that showSaveFilePicker doesn't go through the normal download code paths so it isn't caught by the usual checks for the DownloadRestrictions policy in ChromeDownloadManagerDelegate.

christinesm: Could you please take a look? Is there somewhere we can apply a check for the enterprise policy?

cc qinmin: Do we consider these to be downloads according to the enterprise policy? (I think we do, but just wanted to check.)

[Monorail components: Blink>Storage>FileSystem UI>Browser>Downloads]

### ch...@chromium.org (2023-12-18)

Hi chlily@, will take a look into this - cc'ing my colleagues who also work on File System Access.

### ch...@chromium.org (2023-12-18)

Hi ydago@, could you please take a look at this bug as it pertains to the Chrome Enterprise policy and triage further if needed? (Looks like the owner of this policy, zmin@, is OOO for a while).

ayui@ and I dug into this further and are wondering if the scenario outlined in this bug is technically considered a 'download' under the current policy? When the downloads enterprise policy is enabled (for example, under the more restrictive policy #3 outlined here [1], is the expectation that the user should not be able to save any file via a file picker, regardless of directory destination?

Since this policy has existed since M61, pre local file access, maybe it's possible this policy only considered the saveFile() API.

[1] https://chromeenterprise.google/policies/#DownloadRestrictions

### [Deleted User] (2023-12-19)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-12-19)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-31)

ydago: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### yd...@chromium.org (2024-01-03)

[Empty comment from Monorail migration]

### yd...@chromium.org (2024-01-03)

[Empty comment from Monorail migration]

### do...@chromium.org (2024-01-03)

`window.showSaveFilePicker` is a new-ish API for file downloads, and as such isn't hooked in every policy that interacts with downloads. I think as a workaround until this bug is fixed you could use this policy:
https://chromeenterprise.google/policies/#FileSystemWriteBlockedForUrls

With that being said, I'm not the most knowledgeable on this topic so I might be missing something. @rogerta I know you looked at something somewhat related to this recently, WDYT?

### yd...@chromium.org (2024-01-03)

Hello, sorry for the delays, I have checked a little bit into it and found that the policy is not checked at all in the code path which seems starts here FileSystemAccessManagerImpl::ChooseEntries.
It unfortunately does not seem like a trivial fix and I have no experience with this code area, I will pass it down to a team that has worked on similar policies.

### do...@chromium.org (2024-01-03)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-15)

rogerta: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### fa...@gmail.com (2024-01-25)

Hi, friendly ping. 

### is...@google.com (2024-01-25)

This issue was migrated from crbug.com/chromium/1512384?no_tracker_redirect=1

[Multiple monorail components: Blink>Storage>FileSystem, UI>Browser>Downloads]
[Monorail components added to Component Tags custom field.]

### fa...@gmail.com (2024-02-05)

Friendly ping.

### fa...@gmail.com (2024-03-05)

Friendly ping.

### ro...@chromium.org (2024-03-08)

Sorry for the delay. There is a [CL in review](https://chromium-review.googlesource.com/c/chromium/src/+/5301485) to fix the upload cases using `showOpenFilePicker()` and `showDirectoryPicker()`. `showSaveFilePicker()` will be done as a followup CL.

### fa...@gmail.com (2024-03-20)

Hi CL, 'Add content analysis to File System Access Javascript API' has been approved and merged. Any update on this issue? Thanks.

### fa...@gmail.com (2024-04-02)

Hi, it's been a long time. Can we update on this issue?

### ro...@google.com (2024-04-02)

Work in progress, tracked in [b/310657981](https://issues.chromium.org/issues/310657981).

### na...@google.com (2024-07-04)

Update:

The previous assignee (rogerta@) has left the company. We are aware of the issue and it is in our Q3 planning to add download scanning support for `window.showSaveFilePicker` and make download restrictions work properly.

### pe...@google.com (2024-10-26)

nancylanxiao: Uh oh! This issue still open and hasn't been updated in the last 113 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### pe...@google.com (2024-11-14)

haihan: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### fa...@gmail.com (2025-02-19)

Hi, any updates on this issue? Thanks!

### ha...@google.com (2025-06-25)

Deep scanning support for FSA API is ramping up in m138.

### ch...@google.com (2025-09-10)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### ch...@google.com (2025-09-22)

Dear owner, thanks for fixing this bug. We've reopened it because:

- Some CLs listed in the “Fixed By Code Changes” field are invalid and have been removed. Please provide an appropriate Gerrit url that matches the pattern: `https://<host>-review.googlesource.com/c/<repo>/+/<change_number>` or use the value 'NA' and re-mark this bug as fixed. If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### aj...@google.com (2025-10-08)

adjusting severity as this is a limited bypass.

### sp...@google.com (2025-10-14)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
for pointing out a potential gap in our policy enforcement


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2025-12-30)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/41484965)*
