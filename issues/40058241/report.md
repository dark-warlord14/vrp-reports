# Security: Heap-use-after-free in TabStrip::OnGroupCreated

| Field | Value |
|-------|-------|
| **Issue ID** | [40058241](https://issues.chromium.org/issues/40058241) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>TopChrome>TabStrip>TabGroups |
| **Platforms** | Linux |
| **Reporter** | me...@gmail.com |
| **Assignee** | dp...@chromium.org |
| **Created** | 2021-12-15 |
| **Bounty** | $7,000.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36

Steps to reproduce the problem:
1. download asan-linux-release-951397.zip and unzip
2. start a server at the folder of poc.html : `python -m SimpleHTTPServer 8605`
3. install the extension and allow website's popup
4. `./chrome`, click the group header button (don't release). When you see the popup tab is opened, drag the tabgroup away, this will create two tabgroup with the same GroupId
5. drag the tabgroup back

What is the expected behavior?

What went wrong?
If we have two tabgroups with the same id and drag to merge them, old TabGroupViews will be freed in function `TabStrip::OnGroupCreated` [1] by assigning a new unique_ptr to `group_views_[group]`. 
and this old TabgGroupViews will be used again in `TabStripLayoutHelper::SlotIsCollapsedTab`[2], which is stored in `slots_`.

[1] https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/tabs/tab_strip.cc;l=1245;drc=0e45c020c43b1a9f6d2870ff7f92b30a2f03a458;bpv=0;bpt=0
[2] https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/tabs/tab_strip_layout_helper.cc;l=443;drc=0e45c020c43b1a9f6d2870ff7f92b30a2f03a458;bpv=0;bpt=0

Did this work before? N/A 

Chrome version: 94.0.4606.81  Channel: n/a
OS Version:

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 22.4 KB)
- [poc.html](attachments/poc.html) (text/plain, 150 B)
- [background.js](attachments/background.js) (text/plain, 547 B)
- [manifest.json](attachments/manifest.json) (text/plain, 210 B)
- [video.webm](attachments/video.webm) (video/webm, 6.0 MB)
- [background.js](attachments/background.js) (text/plain, 367 B)
- [video1.webm](attachments/video1.webm) (video/webm, 547.5 KB)

## Timeline

### [Deleted User] (2021-12-15)

[Empty comment from Monorail migration]

### me...@gmail.com (2021-12-15)

update the background.js

### me...@chromium.org (2021-12-15)

Thanks for the report. I'm labeling this as medium severity: Despite being a bug in the UI, it needs an extension and a specific user gesture sequence to trigger, both of which are mitigating circumstances.

dpenning: Can I assign this to you since you are also looking at https://crbug.com/chromium/1270539? Thanks.

[Monorail components: UI>Browser>TopChrome>TabStrip>TabGroups]

### [Deleted User] (2021-12-15)

[Empty comment from Monorail migration]

### me...@gmail.com (2021-12-16)

Re Commnet 3:
Actually you can trigger this without extension, see video1.



### me...@gmail.com (2021-12-16)

1. start a server at the folder of poc.html : `python -m SimpleHTTPServer 8605`
2. open chrome with `./chrome http://127.0.0.1:8605/poc.html about:blank`
3.  add the first tab to a group, and do the same steps in https://crbug.com/chromium/1280205#c1


### [Deleted User] (2021-12-16)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-12-16)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-12-29)

dpenning: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### dp...@chromium.org (2022-01-03)

[Comment Deleted]

### [Deleted User] (2022-01-18)

dpenning: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### me...@gmail.com (2022-01-19)

any updates?

### dp...@chromium.org (2022-01-24)

https://chromium-review.googlesource.com/c/chromium/src/+/3404696 is out for review which fixes this behavior.

### dp...@chromium.org (2022-01-24)

[Empty comment from Monorail migration]

### dp...@chromium.org (2022-01-24)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-02)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-02-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/d90543a244cffcf5d267a720ed86a37f5edd5835

commit d90543a244cffcf5d267a720ed86a37f5edd5835
Author: David Pennington <dpenning@chromium.org>
Date: Thu Feb 17 17:15:45 2022

End TabDrag sessions before adding a new Tab to the TabStripModel

For multiple cases of TabGroupHeader dragging, when the tab strip model
is changed to have a new tab in the group, the context doesnt currently
pick it up. Because of this, the drag session needs to be ended before
the tab can enter into the TabStripModel. This is because it picks the
index for insertion based on where the group currently is, which may not
be the intended destination for the tab when the drag is in a certain
state.

In order to allow for this, a new signal is created for Observers of the
TabStripModel OnTabWillBeAdded which is called before any mutation
occurs. This allows the drag code to cancel or complete its drag session
before the new tab decides where it wants to go.



Bug: 1280205
Change-Id: Id1e7d752ea1253695bf2f7a229e637415f8523c2
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3404696
Reviewed-by: Connie Wan <connily@chromium.org>
Commit-Queue: David Pennington <dpenning@chromium.org>
Cr-Commit-Position: refs/heads/main@{#972499}

[modify] https://crrev.com/d90543a244cffcf5d267a720ed86a37f5edd5835/chrome/browser/ui/views/tabs/tab_drag_controller.h
[modify] https://crrev.com/d90543a244cffcf5d267a720ed86a37f5edd5835/chrome/browser/ui/views/tabs/browser_tab_strip_controller.h
[modify] https://crrev.com/d90543a244cffcf5d267a720ed86a37f5edd5835/chrome/browser/ui/tabs/tab_strip_model_observer.cc
[modify] https://crrev.com/d90543a244cffcf5d267a720ed86a37f5edd5835/chrome/browser/ui/tabs/tab_strip_model_observer.h
[modify] https://crrev.com/d90543a244cffcf5d267a720ed86a37f5edd5835/chrome/browser/ui/views/tabs/browser_tab_strip_controller.cc
[modify] https://crrev.com/d90543a244cffcf5d267a720ed86a37f5edd5835/chrome/browser/ui/tabs/tab_strip_model.cc
[modify] https://crrev.com/d90543a244cffcf5d267a720ed86a37f5edd5835/chrome/browser/ui/views/tabs/tab_drag_controller.cc
[modify] https://crrev.com/d90543a244cffcf5d267a720ed86a37f5edd5835/chrome/browser/ui/tabs/tab_strip_model.h
[modify] https://crrev.com/d90543a244cffcf5d267a720ed86a37f5edd5835/chrome/browser/ui/views/tabs/tab_strip_types.h


### me...@gmail.com (2022-02-22)

Since this uaf can be triggered without extension, can we label it as severity-High and mark it as fixed?

### me...@gmail.com (2022-03-01)

any updates?

### dp...@chromium.org (2022-03-01)

Marking as fixed. Tested that this issue is fixed on canary along with the merged issues.

### [Deleted User] (2022-03-01)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-02)

[Empty comment from Monorail migration]

### am...@google.com (2022-03-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-03-11)

Congratulations, the VRP Panel has decided to award you $7,000 for this report. While we greatly appreciate your efforts, we feel it is important to note that issues are heavily or solely reliant on user interaction are likely receive reduced reward amounts in the future as of our rule/policy changes in this regard [1]. Thank you again for your efforts and reporting this issue to us. 

[1] https://g.co/chrome/vrp 

### am...@google.com (2022-03-11)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-03-28)

[Empty comment from Monorail migration]

### am...@google.com (2022-03-29)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-08)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2022-07-22)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-29)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1280205?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/1281079, crbug.com/chromium/1282544]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058241)*
