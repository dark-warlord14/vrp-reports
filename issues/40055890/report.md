# Security: OOB read when window is closed while a link is being dragged over the tab strip

| Field | Value |
|-------|-------|
| **Issue ID** | [40055890](https://issues.chromium.org/issues/40055890) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>TopChrome>TabStrip |
| **Platforms** | Linux, Windows, ChromeOS |
| **Reporter** | de...@gmail.com |
| **Assignee** | dp...@chromium.org |
| **Created** | 2021-05-16 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**  

When dragging a link over the tab strip, if the window is closed, an OOB read can occur in the browser process. This is due to the fact that when the window is closed, each of the tabs will be closed first and the window itself will be closed a short time later. If a drag message is processed in between the time when the tabs are removed and the window is closed, an OOB read will occur in the tab vector.

**VERSION**  

Chrome Version: Tested on 92.0.4510.0 (latest asan build)  

Operating System: Windows 10, version 20H2

**REPRODUCTION CASE**

1. Install the attached extension.
2. Once installed, the extension will create a window with a single tab. Drag a link (e.g. a bookmark, or the URL shown in the omnibox) over the tab strip in that window. Ensure the drop arrow shown in the tab strip appears in the middle of the tab or to the right (i.e. dragging the item anywhere within the tab strip will work, except towards the very left edge of the window).
3. Five seconds after opening the window, the extension will close it. Providing the item being dragged is still over the tab strip, this should result in an out-of-bounds read in the browser process. You can verify that by going through these steps in an asan build.

Note that the effect here is somewhat dependent on timing (see the explanation below), so you may have to try a few times for it to work.

**CREDIT INFORMATION**  

Reporter credit: David Erceg

## Attachments

- [asan_output_883324.txt](attachments/asan_output_883324.txt) (text/plain, 18.4 KB)
- [background.js](attachments/background.js) (text/plain, 321 B)
- [manifest.json](attachments/manifest.json) (text/plain, 159 B)
- [page.html](attachments/page.html) (text/plain, 98 B)
- [page.js](attachments/page.js) (text/plain, 56 B)

## Timeline

### [Deleted User] (2021-05-16)

[Empty comment from Monorail migration]

### de...@gmail.com (2021-05-16)

When a window is closed, all of the tabs in that window are removed:

https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/browser.cc;l=934;drc=46bbb9795fcc1934c6cfbec096764f888c4d400a

Then, the window itself will be closed, through an asynchronous task:

https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/browser.cc;l=1267;drc=46bbb9795fcc1934c6cfbec096764f888c4d400a

Additionally, as part of a drag operation involving a link, an arrow will be shown at the location in the tab strip where the drop will occur, if completed.

As can be seen in TabStrip::GetDropBounds, the tab at the drop index will be retrieved and the index will be clamped, so that it's not larger than GetTabCount() - 1:

https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/tabs/tab_strip.cc;l=3380;drc=46bbb9795fcc1934c6cfbec096764f888c4d400a

However, when a window is in the process of being closed, it's possible for a drag message to be processed after all of the tabs in the window have been removed, but before the window itself has been closed. In that case, GetTabCount will return 0. That then means that the index passed to tab_at will be -1 and an out-of-bounds read will occur.

Because this issue is triggered when a window is closed, it is possible to trigger it via a webpage, however I think there are two reasons why that would be somewhat more difficult than triggering the issue using an extension:

1. The entire window needs to be closed. That then means that the webpage would likely need to be opened in a window by itself (so that closing the tab results in the entire window being closed).

2. The webpage would either need to have been opened by a script, or have no back/forward history entries. This is due to the fact that there are restrictions on when a page can call window.close:

https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/frame/dom_window.cc;l=344;drc=d2047b5fbf1da5e49ea1b6009eed130b357ac3e1

### xi...@chromium.org (2021-05-17)

Thanks for the report! Hopefully https://crbug.com/1198717#c11 will fix all these security issues by preventing extensions from modifying tab strip while a tab drag was in progress.

[Monorail components: UI>Browser>TabStrip]

### [Deleted User] (2021-05-17)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-05-26)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-30)

solomonkinard: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-06-13)

solomonkinard: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### so...@chromium.org (2021-06-29)

In me queue, but will ask for others to look.

### so...@chromium.org (2021-06-29)

[Empty comment from Monorail migration]

### ad...@google.com (2021-07-08)

solomonkinard@, I'm sorry, but security bugs need to be assigned and actively worked on. Please could you consult with one of your colleagues and work out who would be best to take care of this, then actively reassign?

[Monorail components: UI>Browser>TopChrome>TabStrip]

### ad...@google.com (2021-07-08)

Setting FoundIn-91 to match Security_Impact-Stable. I have no additional information that this can be reproduced in M91. But this label will become important to Sheriffbot in the near future.

### tb...@chromium.org (2021-07-08)

This is one of the ones that dpenning@ and I are reviewing.

### tb...@chromium.org (2021-07-09)

I can't reproduce this on Mac. The window close is blocked until the link drag ends.

### tb...@chromium.org (2021-07-09)

That said I do have a fix that I'm pretty confident in, I just can't test it myself since I only have access to a Mac. We'll go ahead and land it.

### gi...@appspot.gserviceaccount.com (2021-07-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/8c956ce0d96372940ec1702bbacec4b37cfa5357

commit 8c956ce0d96372940ec1702bbacec4b37cfa5357
Author: Taylor Bergquist <tbergquist@chromium.org>
Date: Tue Jul 13 00:20:43 2021

Handle an empty tabstrip in TabStrip::GetDropBounds.

Bug: 1209616
Change-Id: I7687d004bd970f94d5909e6c5349e0599022cf5d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3017667
Reviewed-by: Peter Boström <pbos@chromium.org>
Commit-Queue: Taylor Bergquist <tbergquist@chromium.org>
Cr-Commit-Position: refs/heads/master@{#900744}

[modify] https://crrev.com/8c956ce0d96372940ec1702bbacec4b37cfa5357/chrome/browser/ui/views/tabs/tab_strip.cc


### ad...@google.com (2021-07-14)

derceg86@ do you think you'd be kind enough to test this fix once it appears in Canary?

tbergquist@ - please could you mark it as Fixed if you believe it's likely to be a complete fix, so that Sheriffbot can do all the merge requests - https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/security-labels.md#TOC-Merge-labels. Thanks!

### tb...@chromium.org (2021-07-14)

[Empty comment from Monorail migration]

### [Deleted User] (2021-07-15)

[Empty comment from Monorail migration]

### [Deleted User] (2021-07-15)

[Empty comment from Monorail migration]

### [Deleted User] (2021-07-15)

Requesting merge to stable M91 because latest trunk commit (900744) appears to be after stable branch point (870763).

Requesting merge to beta M92 because latest trunk commit (900744) appears to be after beta branch point (885287).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-07-15)

This bug requires manual review: We are only 4 days from stable.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/main/docs/process/merge_request.md#when-to-request-a-merge
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
Owners: govind@(Android), benmason@(iOS), dgagnon@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2021-07-15)

We should get more bake time before merging to M92 - we should consider merging to M92 in a while to pick it up in a security refresh.

### de...@gmail.com (2021-07-16)

Re https://crbug.com/chromium/1209616#c16: I've tested a bit in Canary and the fix seems to work well.

### am...@google.com (2021-07-22)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@google.com (2021-07-22)

Congrats, David! The VRP Panel has decided to award you $5000 for this report. Another good one! 

### am...@google.com (2021-07-23)

Approved for merge to M92, please merge to branch 4515 at your earliest convenience. 
Also approving merge to M91 as this has become the Extended Stable release branch; please merged to branch 4472 as well. Thank you! 

### am...@google.com (2021-07-23)

[Empty comment from Monorail migration]

### sr...@google.com (2021-07-29)

re-opening to get engineer attention for the merge

Please merge to M92 asap ( before EOD thursday July 29)

### dp...@chromium.org (2021-07-29)

Cherry picked https://chromium-review.googlesource.com/c/chromium/src/+/3017667 to M92

### gi...@appspot.gserviceaccount.com (2021-07-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/0bff00317ed3ada8009d62e0ce3c39eb144b8589

commit 0bff00317ed3ada8009d62e0ce3c39eb144b8589
Author: Taylor Bergquist <tbergquist@chromium.org>
Date: Thu Jul 29 22:14:33 2021

Handle an empty tabstrip in TabStrip::GetDropBounds.

(cherry picked from commit 8c956ce0d96372940ec1702bbacec4b37cfa5357)

Bug: 1209616
Change-Id: I7687d004bd970f94d5909e6c5349e0599022cf5d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3017667
Reviewed-by: Peter Boström <pbos@chromium.org>
Commit-Queue: Taylor Bergquist <tbergquist@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#900744}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3061458
Reviewed-by: Taylor Bergquist <tbergquist@chromium.org>
Commit-Queue: David Pennington <dpenning@chromium.org>
Cr-Commit-Position: refs/branch-heads/4515@{#1918}
Cr-Branched-From: 488fc70865ddaa05324ac00a54a6eb783b4bc41c-refs/heads/master@{#885287}

[modify] https://crrev.com/0bff00317ed3ada8009d62e0ce3c39eb144b8589/chrome/browser/ui/views/tabs/tab_strip.cc


### am...@chromium.org (2021-07-30)

Hello dpenning@, as this issue was discovered in M91, could you please merge to M91 branch 4472, asap for this issue to be a part of the extended stable release since we are moving toward a 4W stable release cycle. Thanks you! 

### pb...@chromium.org (2021-07-30)

I'll take care of the merge, David's out today.

### [Deleted User] (2021-07-30)

We commit ourselves to a 60 day deadline for fixing for high severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2021-07-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/f1e13ea0f18645899c534d15ed88c9ddf40b23d3

commit f1e13ea0f18645899c534d15ed88c9ddf40b23d3
Author: Taylor Bergquist <tbergquist@chromium.org>
Date: Fri Jul 30 18:01:28 2021

Handle an empty tabstrip in TabStrip::GetDropBounds.

(cherry picked from commit 8c956ce0d96372940ec1702bbacec4b37cfa5357)

(cherry picked from commit 0bff00317ed3ada8009d62e0ce3c39eb144b8589)

Bug: 1209616
Change-Id: I7687d004bd970f94d5909e6c5349e0599022cf5d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3017667
Reviewed-by: Peter Boström <pbos@chromium.org>
Commit-Queue: Taylor Bergquist <tbergquist@chromium.org>
Cr-Original-Original-Commit-Position: refs/heads/master@{#900744}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3061458
Reviewed-by: Taylor Bergquist <tbergquist@chromium.org>
Commit-Queue: David Pennington <dpenning@chromium.org>
Cr-Original-Commit-Position: refs/branch-heads/4515@{#1918}
Cr-Original-Branched-From: 488fc70865ddaa05324ac00a54a6eb783b4bc41c-refs/heads/master@{#885287}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3062679
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Commit-Queue: Peter Boström <pbos@chromium.org>
Cr-Commit-Position: refs/branch-heads/4472@{#1586}
Cr-Branched-From: 3d60439cfb36485e76a1c5bb7f513d3721b20da1-refs/heads/master@{#870763}

[modify] https://crrev.com/f1e13ea0f18645899c534d15ed88c9ddf40b23d3/chrome/browser/ui/views/tabs/tab_strip.cc


### am...@chromium.org (2021-08-02)

[Empty comment from Monorail migration]

### am...@google.com (2021-08-02)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-05)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-06)

This bug is a regression and does not impact stable. Removing incorrectly added Release- labels.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-08-06)

[Empty comment from Monorail migration]

### am...@google.com (2021-08-06)

Closing as fixed as this was bug was reopened (in comment # 28) by release team to gain attention for merge, which has been achieved. Need to get the bot to stop removing valid labels. 

### [Deleted User] (2021-08-07)

This bug is a regression and does not impact stable. Removing incorrectly added Release- labels.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-08-07)

Dear owner, thanks for fixing this bug. We’ve reopened it because security bugs need Security_Severity and FoundIn labels set, which will enable the bots to request merges to the correct branches ( as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact (security@chromium.org) to arrange to set these labels and then this bug can be marked closed again. Thank you! Severity guidelines: https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues FoundIn guidelines: https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security Thanks for your time! 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-08-07)

[Empty comment from Monorail migration]

### ad...@google.com (2021-08-07)

Apologies for label change spam - this was a bug in our changes to make Sheriffbot work with the Extended Stable branch.

### rz...@google.com (2021-08-10)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-10)

[Empty comment from Monorail migration]

### gi...@google.com (2021-08-20)

[Empty comment from Monorail migration]

### gi...@google.com (2021-08-20)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-08-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/916bf13dd983af62491c68ea1b6a39f8de6f65a6

commit 916bf13dd983af62491c68ea1b6a39f8de6f65a6
Author: Taylor Bergquist <tbergquist@chromium.org>
Date: Mon Aug 23 11:57:31 2021

[M90-LTS] Handle an empty tabstrip in TabStrip::GetDropBounds.

(cherry picked from commit 8c956ce0d96372940ec1702bbacec4b37cfa5357)

Bug: 1209616
Change-Id: I7687d004bd970f94d5909e6c5349e0599022cf5d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3017667
Commit-Queue: Taylor Bergquist <tbergquist@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#900744}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3085325
Reviewed-by: Artem Sumaneev <asumaneev@google.com>
Owners-Override: Artem Sumaneev <asumaneev@google.com>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Cr-Commit-Position: refs/branch-heads/4430@{#1573}
Cr-Branched-From: e5ce7dc4f7518237b3d9bb93cccca35d25216cbe-refs/heads/master@{#857950}

[modify] https://crrev.com/916bf13dd983af62491c68ea1b6a39f8de6f65a6/chrome/browser/ui/views/tabs/tab_strip.cc


### rz...@google.com (2021-08-23)

[Empty comment from Monorail migration]

### am...@google.com (2021-08-26)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-15)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1209616?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40055890)*
