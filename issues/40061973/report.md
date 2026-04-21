# UAF in OnSyncMessageEventReady

| Field | Value |
|-------|-------|
| **Issue ID** | [40061973](https://issues.chromium.org/issues/40061973) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Mojo>Bindings |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ro...@gmail.com |
| **Assignee** | ro...@google.com |
| **Created** | 2022-11-30 |
| **Bounty** | $4,000.00 |

## Description

**Steps to reproduce the problem:**  

1.

**Problem Description:**  

While I tried to reproduce <https://crbug.com/1376099>. I found This bug by accident. But I can't trigger it again. Luckily, I saved  

the first asan log file and analysis is as follows:

Endpoint object hold a raw\_ptr of AssociatedGroupController but it not observe AssociatedGroupController's lifecycle.

In OnSyncMessageEventReady. It hold the refcounted of both scoped\_refptr<Endpoint> [2] and scoped\_refptr<AssociatedGroupController>[3].  

And HandleIncomingMessage[4] can be any sync mojo call. This looks safe. However, if both the other refcounted of endpoint and AssociatedGroupController  

was gone. Then when OnSyncMessageEventReady function run to the end. The refcounted of Endpoint and AssociatedGroupController go to 0. It will delete both the Endpoint and AssociatedGroupController.  

Because the declaration of scoped\_refptr<Endpoint>[2] is ahead of scoped\_refptr<AssociatedGroupController>[3]. OnSyncMessageEventReady will first delete AssociatedGroupController. Then delete Endpoint object. Finally, In Endpoint's destructor function. UAF will happen when accessing the raw\_ptr of delete AssociatedGroupController object.

const raw\_ptr<ChannelAssociatedGroupController> controller\_; [1]  

void OnSyncMessageEventReady() {  

DCHECK(task\_runner\_->RunsTasksInCurrentSequence());

```
  scoped_refptr<Endpoint> keepalive(this);  ---------------[2]  
  scoped_refptr<AssociatedGroupController> controller_keepalive(  
      controller_.get());  ---------------------------[3]  
  base::AutoLock locker(controller_->lock_);  
  bool more_to_process = false;  
  if (!sync_messages_.empty()) {  
    MessageWrapper message_wrapper =  
        std::move(sync_messages_.front().second);  
    sync_messages_.pop_front();  

    bool dispatch_succeeded;  
    mojo::InterfaceEndpointClient\* client = client_;  
    {  
      base::AutoUnlock unlocker(controller_->lock_);  
      dispatch_succeeded =  
          client->HandleIncomingMessage(&message_wrapper.value());---------------------[4]  
    }  

    if (!sync_messages_.empty())  
      more_to_process = true;  

    if (!dispatch_succeeded)  
      controller_->RaiseError();  
  }  

  if (!more_to_process)  
    sync_watcher_->ResetEvent();  

  // If there are no queued sync messages and the peer has closed, there  
  // there won't be incoming sync messages in the future. If any  
  // SyncWatch() calls are on the stack for this endpoint, resetting the  
  // watcher will allow them to exit as the stack undwinds.  
  if (!more_to_process && peer_closed_)  
    sync_watcher_.reset();  
}  

```

**Additional Comments:**  

This is a mojo IPC implement bug which can be happened in any process without user interaction(include the browser process).  

bisect information: This bug was introduced in <https://codereview.chromium.org/2195953002>

\*\*Chrome version: \*\* 107.0.0.0 \*\*Channel: \*\* Stable

**OS:** Windows

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 29.9 KB)

## Timeline

### [Deleted User] (2022-11-30)

[Empty comment from Monorail migration]

### ro...@gmail.com (2022-11-30)

And in my understand. The fix of this bug is easy.
Just swap the order of this two lines code from:
      scoped_refptr<Endpoint> keepalive(this);
      scoped_refptr<AssociatedGroupController> controller_keepalive(
          controller_.get());
to:
      scoped_refptr<AssociatedGroupController> controller_keepalive(
          controller_.get());
      scoped_refptr<Endpoint> keepalive(this);

### ca...@chromium.org (2022-11-30)

rockot and dcheng: Can you PTAL? This seems like a valid bug, but there is no PoC to trigger it. I'm triageing this as High out of an abundance of caution, but feel free to adjust as appropriate.  Setting FoundIn-106 since this is not a recent regression

### [Deleted User] (2022-11-30)

[Empty comment from Monorail migration]

### ca...@chromium.org (2022-11-30)

[Empty comment from Monorail migration]

[Monorail components: Internals>Mojo>Core]

### ro...@google.com (2022-11-30)

Agreed about the fix. Great find, thanks for the report.

[Monorail components: -Internals>Mojo>Core Internals>Mojo>Bindings]

### gi...@appspot.gserviceaccount.com (2022-12-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/120b4b05ac7eaa9024f677394aa663c2702174ce

commit 120b4b05ac7eaa9024f677394aa663c2702174ce
Author: Ken Rockot <rockot@google.com>
Date: Thu Dec 01 01:44:05 2022

Mojo: Fix potential UAF in IPC Channel

Fixed: 1394692
Change-Id: I1753b79eb6e9230ebb663eca47295d81dd859068
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4066994
Commit-Queue: Ken Rockot <rockot@google.com>
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1077742}

[modify] https://crrev.com/120b4b05ac7eaa9024f677394aa663c2702174ce/ipc/ipc_mojo_bootstrap.cc


### [Deleted User] (2022-12-01)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-01)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-12-01)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-12-01)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-01)

Requesting merge to stable M108 because latest trunk commit (1077742) appears to be after stable branch point (1058933).

Requesting merge to dev M109 because latest trunk commit (1077742) appears to be after dev branch point (1070088).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-12-02)

Merge review required: M109 is already shipping to beta.

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
Owners: govind (Android), eakpobaro (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-12-02)

Merge review required: M108 is already shipping to stable.

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

### am...@chromium.org (2022-12-05)

M109 merge approved, please merge this fix to branch 5414 by EOD tomorrow, Tuesday, 6 December so this fix can be included in next M109 beta 

M108 merge approved, please merge this fix to branch 5359 by 10am Pacific, Friday, 9 December so this fix can be included in next week's M108 Stable refresh. 

### gi...@appspot.gserviceaccount.com (2022-12-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/779b6a52a9b76be3e06b601e3c0c031d5ee8012b

commit 779b6a52a9b76be3e06b601e3c0c031d5ee8012b
Author: Ken Rockot <rockot@google.com>
Date: Wed Dec 07 20:33:54 2022

[M109] Mojo: Fix potential UAF in IPC Channel

(cherry picked from commit 120b4b05ac7eaa9024f677394aa663c2702174ce)

Fixed: 1394692
Change-Id: I1753b79eb6e9230ebb663eca47295d81dd859068
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4066994
Commit-Queue: Ken Rockot <rockot@google.com>
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1077742}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4087145
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Auto-Submit: Ken Rockot <rockot@google.com>
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/5414@{#523}
Cr-Branched-From: 4417ee59d7bf6df7a9c9ea28f7722d2ee6203413-refs/heads/main@{#1070088}

[modify] https://crrev.com/779b6a52a9b76be3e06b601e3c0c031d5ee8012b/ipc/ipc_mojo_bootstrap.cc


### gi...@appspot.gserviceaccount.com (2022-12-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/d1d654d7322244ad394000ef2622c0871e856cfa

commit d1d654d7322244ad394000ef2622c0871e856cfa
Author: Ken Rockot <rockot@google.com>
Date: Wed Dec 07 20:35:15 2022

[M108] Mojo: Fix potential UAF in IPC Channel

(cherry picked from commit 120b4b05ac7eaa9024f677394aa663c2702174ce)

Fixed: 1394692
Change-Id: I1753b79eb6e9230ebb663eca47295d81dd859068
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4066994
Commit-Queue: Ken Rockot <rockot@google.com>
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1077742}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4085806
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Auto-Submit: Ken Rockot <rockot@google.com>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/5359@{#1115}
Cr-Branched-From: 27d3765d341b09369006d030f83f582a29eb57ae-refs/heads/main@{#1058933}

[modify] https://crrev.com/d1d654d7322244ad394000ef2622c0871e856cfa/ipc/ipc_mojo_bootstrap.cc


### [Deleted User] (2022-12-07)

LTS Milestone M102

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2022-12-08)

[Empty comment from Monorail migration]

### am...@google.com (2022-12-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-12-09)

Congratulations, Rox! The VRP Panel has decided to award you $4,000 for this report + $1,000 bisect bonus + $1,000 patch bonus for a total of $6,000 reward. As this issue lacks a PoC or other demonstration, in reviewing the analysis and fix and given that this issue happened once / haphazardly and cannot be reproduced, this issue appears to be moderately mitigated == $4,000 report reward amount. Thank you for your efforts and reporting this issue to us! 

### rz...@google.com (2022-12-09)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-09)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2022-12-09)

1. https://crrev.com/c/4085487
2. Low, no conflicts
3. 108, 109
4. Yes

### am...@google.com (2022-12-10)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-12-12)

[Empty comment from Monorail migration]

### gm...@google.com (2022-12-13)

[Empty comment from Monorail migration]

### pg...@google.com (2022-12-14)

[Empty comment from Monorail migration]

### pg...@google.com (2022-12-14)

[Empty comment from Monorail migration]

### gm...@google.com (2022-12-19)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-12-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/6370143d94fc67da0ab8c62ea3e7583b8f4f1f08

commit 6370143d94fc67da0ab8c62ea3e7583b8f4f1f08
Author: Ken Rockot <rockot@google.com>
Date: Tue Dec 20 13:24:59 2022

[M102-LTS] Mojo: Fix potential UAF in IPC Channel

(cherry picked from commit 120b4b05ac7eaa9024f677394aa663c2702174ce)

Fixed: 1394692
Change-Id: I1753b79eb6e9230ebb663eca47295d81dd859068
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4066994
Commit-Queue: Ken Rockot <rockot@google.com>
Cr-Original-Commit-Position: refs/heads/main@{#1077742}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4085487
Reviewed-by: Jana Grill <janagrill@google.com>
Owners-Override: Jana Grill <janagrill@google.com>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Cr-Commit-Position: refs/branch-heads/5005@{#1414}
Cr-Branched-From: 5b4d9450fee01f821b6400e947b3839727643a71-refs/heads/main@{#992738}

[modify] https://crrev.com/6370143d94fc67da0ab8c62ea3e7583b8f4f1f08/ipc/ipc_mojo_bootstrap.cc


### rz...@google.com (2022-12-20)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-09)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1394692?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061973)*
