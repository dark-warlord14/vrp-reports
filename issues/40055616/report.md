# Security: Container-overflow when extension is disabled or uninstalled while dragging icon in extensions toolbar

| Field | Value |
|-------|-------|
| **Issue ID** | [40055616](https://issues.chromium.org/issues/40055616) |
| **Status** | Assigned |
| **Severity** | Unknown |
| **Priority** | P2 |
| **Component** | Platform>Extensions |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | de...@gmail.com |
| **Assignee** | em...@chromium.org |
| **Created** | 2021-04-21 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

When the icon for an extension is being dragged within the extensions toolbar, if that extension is disabled or uninstalled, a container-overflow will occur in the browser process.

**VERSION**  

Chrome Version: Tested on 92.0.4484.0 (latest asan build)  

Operating System: Windows 10, version 20H2

**REPRODUCTION CASE**

1. Install the attached extension.
2. Pin the extension's icon in the toolbar.
3. Click the icon, then start dragging it.
4. Two seconds after being clicked, the extension will uninstall itself (using chrome.management.uninstallSelf). This will trigger a container-overflow when the icon is dragged within the extensions toolbar. You can verify that by going through these steps in an asan build.

**CREDIT INFORMATION**  

Reporter credit: David Erceg

## Attachments

- asan_output_874548.txt (text/plain, 15.4 KB)
- [background.js](attachments/background.js) (text/plain, 144 B)
- [manifest.json](attachments/manifest.json) (text/plain, 191 B)

## Timeline

### [Deleted User] (2021-04-21)

[Empty comment from Monorail migration]

### de...@gmail.com (2021-04-21)

The issue here is that when an extension icon is being dragged, the icon will be updated by ExtensionsToolbarContainer::SetExtensionIconVisibility:

https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/ui/views/extensions/extensions_toolbar_container.cc;l=689;drc=bb4ed2497aadfe10f59390ff6cd6bee010bb9663

That method retrieves the extension from the set of currently pinned items. However, when the extension is unloaded, it will be removed from the set:

https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/ui/toolbar/toolbar_actions_model.cc;l=211;drc=325a806757116ea8b6b7a4a6ef786fd2a7b6fa37

That means that the iterator that's retrieved will point to the end of the pinned_action_ids_ vector. The value will then be unconditionally used:

https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/ui/views/extensions/extensions_toolbar_container.cc;l=697;drc=bb4ed2497aadfe10f59390ff6cd6bee010bb9663

resulting in a container-overflow.

Note that if there are no other pinned extensions, asan will show an access violation, with a close to null address. The same out-of-bounds access occurs, however, the invalid value will never be used, and extension_view will be set to null, which will then cause the access violation reported by asan.

### ca...@chromium.org (2021-04-22)

Assigning severity medium due to the high amount of interaction required.

lazyboy: Can you help triage this further? Thanks

[Monorail components: Platform>Extensions]

### [Deleted User] (2021-04-22)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-04-22)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-05-05)

lazyboy: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2021-05-19)

[Comment Deleted]

### la...@chromium.org (2021-05-20)

I mistakenly linked the CL in https://crbug.com/chromium/1201060#c7, apologies.

### [Deleted User] (2021-05-26)

[Empty comment from Monorail migration]

### [Deleted User] (2021-06-03)

lazyboy: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2021-06-03)

[Comment Deleted]

### la...@chromium.org (2021-06-03)

FYI: The above CL incorrectly points to this bug. That CL should point to https://bugs.chromium.org/p/chromium/issues/detail?id=1201031 instead.

### gi...@appspot.gserviceaccount.com (2021-06-11)

[Comment Deleted]

### gi...@appspot.gserviceaccount.com (2021-06-11)

[Comment Deleted]

### ad...@google.com (2021-07-08)

Setting FoundIn-91 due to Security_Impact-Stable. That should be close enough to keep Sheriffbot happy.


### la...@chromium.org (2021-07-13)

Adding to chrome-fixit-2021-security based on adetaylor@'s suggestion, I only slightly looked into this and sent out a cursory CL. Here's the CL if someone want's to take a look:
https://chromium-review.googlesource.com/c/chromium/src/+/2909770

### ad...@google.com (2021-07-14)

Thanks! Security bugs still need to have a responsible individual though, so I'm parking it back on you, sorry :)

### [Deleted User] (2021-08-05)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-07)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-16)

[Empty comment from Monorail migration]

### rs...@chromium.org (2021-08-19)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-11)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-22)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-15)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-02)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-30)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-25)

[Empty comment from Monorail migration]

### ts...@chromium.org (2022-07-20)

lazyboy/rdevlin - is there perhaps another person who might have time to take a look at this very old bug? Thanks!

### [Deleted User] (2022-08-03)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-28)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-30)

[Empty comment from Monorail migration]

### ad...@chromium.org (2022-12-01)

[Empty comment from Monorail migration]

### so...@chromium.org (2023-01-25)

[Empty comment from Monorail migration]

### so...@chromium.org (2023-01-25)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-08)

[Empty comment from Monorail migration]

### so...@chromium.org (2023-02-14)

[Empty comment from Monorail migration]

### so...@chromium.org (2023-02-14)

[Empty comment from Monorail migration]

### em...@chromium.org (2023-02-15)

This is the same as crbug.com/1266510 which was fixed on crrev.com/c/3263281 by drag and dropping only if there is an action for the extension dragged. I beleive the fix should cover this bug too, thus marking as duplicate.

Adding reward-topanel in case they need input here (same bug filled in two different places)

### [Deleted User] (2023-02-16)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-03-02)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-03-02)

Congratulations David! The VRP Panel has decided to award you $1,000 for this report. Unfortunately, there was a bank error in another researcher's favor as the fix for this issue was landed on a later reported bug. Apologies that we're just getting around to catch this and rewarding this to you now. Thank you again for your efforts and reporting this issue to us and again - apologies for the delay! 

### am...@google.com (2023-03-03)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-26)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1201060?no_tracker_redirect=1

[Monorail mergedinto: crbug.com/chromium/1266510]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40055616)*
