# Security: Heap-use-after-free in ReadAnythingCoordinator::CreateAndRegisterEntry

| Field | Value |
|-------|-------|
| **Issue ID** | [40060288](https://issues.chromium.org/issues/40060288) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>TopChrome>SidePanel |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | me...@gmail.com |
| **Assignee** | ab...@google.com |
| **Created** | 2022-07-15 |
| **Bounty** | $4,000.00 |

## Description

**Steps to reproduce the problem:**

1. download asan-linux-release-1024589.zip and unzip
2. start a http server at the folder of poc.html
3. run `./chrome --enable-features=UserNotes,UnifiedSidePanel,ReadAnything http://127.0.0.1:8605/poc.html`
4. wait until UAF occurs

**Problem Description:**  

In Function `ReadAnythingCoordinator::CreateAndRegisterEntry`[1], it will create a unique\_ptr `side_panel_entry` and pass its raw ptr to `side_panel_entry_observation_`(1). But this unique\_ptr is std::move to `global_registry->Register`(2), and owned by `entries_`(3) in `SidePanelRegistry::Register`[2].

```
void ReadAnythingCoordinator::CreateAndRegisterEntry(  
    SidePanelRegistry\* global_registry) {  
  auto side_panel_entry = std::make_unique<SidePanelEntry>(  
      SidePanelEntry::Id::kReadAnything,  
      l10n_util::GetStringUTF16(IDS_READ_ANYTHING_TITLE),  
      ui::ImageModel::FromVectorIcon(kReaderModeIcon, ui::kColorIcon),  
      base::BindRepeating(&ReadAnythingCoordinator::CreateContainerView,  
                          base::Unretained(this)));  
  side_panel_entry_observation_.Observe(side_panel_entry.get());  // ->(1)  
  global_registry->Register(std::move(side_panel_entry));  // ->(2)  
}  

```
```
bool SidePanelRegistry::Register(std::unique_ptr<SidePanelEntry> entry) {  
  if (GetEntryForId(entry->id()))  
    return false;  
  for (SidePanelRegistryObserver& observer : observers_)  
    observer.OnEntryRegistered(entry.get());  
  entry->AddObserver(this);  
  entries_.push_back(std::move(entry));  // ->(3)  
  return true;  
}  

```

These two classes are derived from `BrowserUserData`/`SupportsUserData`, their lifetime is bound to the browser. However, `SidePanelRegistry` is released before `ReadAnythingCoordinator` if we close the whole tabs.

```
class ReadAnythingCoordinator : public BrowserUserData<ReadAnythingCoordinator>,  
class SidePanelRegistry final : public base::SupportsUserData::Data,  

```

Therefore the unique\_ptr `side_panel_entry` in the `entries_` will be reset and there is a dangling pointer in `side_panel_entry_observation_`. When `ReadAnythingCoordinator` is destructed, `ReadAnythingCoordinator` will remove all the observers including the dangling pointer `side_panel_entry` => UAF occurs.

[1] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/side_panel/read_anything/read_anything_coordinator.cc;l=66;drc=2dfe330b9a4792bcd0ca89acaac81c28f4d48a85;bpv=1;bpt=1>  

[2] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/side_panel/side_panel_registry.cc;l=61;drc=2dfe330b9a4792bcd0ca89acaac81c28f4d48a85>

**Additional Comments:**

\*\*Chrome version: \*\* 103.0.0.0 \*\*Channel: \*\* Not sure

**OS:** Linux

## Attachments

- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)

## Timeline

### [Deleted User] (2022-07-15)

[Empty comment from Monorail migration]

### me...@gmail.com (2022-07-18)

Update: 
If you can't repro this in the latest version on Linux, please use Mac to trigger this, thanks.

### dc...@chromium.org (2022-07-18)

I am able to repro. It looks like this was introduced by https://chromiumdash.appspot.com/commit/6d19b10b5fda471dfaa033931d35ed1aaae56724 (which was itself to fix another UaF issue), so tagging this with FoundIn-103.

Is it still appropriate to tag this with security impact none? are these features all off by default, mschillaci@?

I am tagging this with "High" based on the previous report though.


[Monorail components: UI>Accessibility]

### [Deleted User] (2022-07-18)

[Empty comment from Monorail migration]

### dc...@chromium.org (2022-07-18)

[Empty comment from Monorail migration]

### ms...@google.com (2022-07-18)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-20)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### me...@gmail.com (2022-07-26)

[Comment Deleted]

### me...@gmail.com (2022-08-02)

[Comment Deleted]

### [Deleted User] (2022-08-02)

mschillaci: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-08-02)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-03)

[Empty comment from Monorail migration]

### ab...@google.com (2022-08-05)

[Empty comment from Monorail migration]

### ab...@google.com (2022-08-05)

This is blocked behind a feature flag, Read Anything, which has not been enabled anywhere by default. I'm going to take this issue; moving Mark to cc.

### ab...@google.com (2022-08-05)

[Empty comment from Monorail migration]

### ab...@google.com (2022-08-15)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-30)

abigailbklein: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### me...@gmail.com (2022-09-01)

friendly ping~

### [Deleted User] (2022-09-13)

We commit ourselves to a 60 day deadline for fixing for high severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### me...@gmail.com (2022-09-21)

[Comment Deleted]

### [Deleted User] (2022-09-28)

[Empty comment from Monorail migration]

### me...@gmail.com (2022-09-29)

Hi abigailbklein@, it seems that your patch (https://chromium-review.googlesource.com/c/chromium/src/+/3820321) conflict, could you update it?

### ab...@google.com (2022-10-06)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-10-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/a1cf2dac62547361d560cbe39970d0c39b081418

commit a1cf2dac62547361d560cbe39970d0c39b081418
Author: Abigail Klein <abigailbklein@google.com>
Date: Wed Oct 12 15:53:38 2022

[Read Anything] Do not use ScopedObservation for SidePanelEntry
observation.

This was causing a UAF. When the browser window closed, both the
SidePanelEntry and the ReadAnythingCoordinator were destroyed at the
same time as they are SupportsUserData and BrowserUserData,
respectively. When the ScopedObservation attempted to remove observer,
the pointer had already been freed. This change adds
ReadAnythingCoordinator as an observer to SidePanelEntry and removes
it as an observer via deregistering it from SidePanelRegistry.

Bug: 1266555, 1344756, 1349795, 1352138, 1365832
Change-Id: Ib63faa9d385f577f1f96a0510759f07efa4b115a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3820321
Reviewed-by: Martin Kreichgauer <martinkr@google.com>
Commit-Queue: Abigail Klein <abigailbklein@google.com>
Cr-Commit-Position: refs/heads/main@{#1058076}

[modify] https://crrev.com/a1cf2dac62547361d560cbe39970d0c39b081418/chrome/browser/ui/views/side_panel/read_anything/read_anything_coordinator.cc
[modify] https://crrev.com/a1cf2dac62547361d560cbe39970d0c39b081418/chrome/browser/ui/views/side_panel/read_anything/read_anything_coordinator.h


### ab...@google.com (2022-10-12)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-12)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-10-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/485e1c0e23a6846096b537a665869f33a9798f89

commit 485e1c0e23a6846096b537a665869f33a9798f89
Author: Dana Fried <dfried@google.com>
Date: Wed Oct 12 17:47:04 2022

[Build Sheriff] Revert "[Read Anything] Do not use ScopedObservation for SidePanelEntry"

This reverts commit a1cf2dac62547361d560cbe39970d0c39b081418.

Reason for revert: Causing a number of test failures (see bug)
Bug: 1373964

Original change's description:
> [Read Anything] Do not use ScopedObservation for SidePanelEntry
> observation.
>
> This was causing a UAF. When the browser window closed, both the
> SidePanelEntry and the ReadAnythingCoordinator were destroyed at the
> same time as they are SupportsUserData and BrowserUserData,
> respectively. When the ScopedObservation attempted to remove observer,
> the pointer had already been freed. This change adds
> ReadAnythingCoordinator as an observer to SidePanelEntry and removes
> it as an observer via deregistering it from SidePanelRegistry.
>
> Bug: 1266555, 1344756, 1349795, 1352138, 1365832
> Change-Id: Ib63faa9d385f577f1f96a0510759f07efa4b115a
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3820321
> Reviewed-by: Martin Kreichgauer <martinkr@google.com>
> Commit-Queue: Abigail Klein <abigailbklein@google.com>
> Cr-Commit-Position: refs/heads/main@{#1058076}

Bug: 1266555, 1344756, 1349795, 1352138, 1365832
Change-Id: I8ba94a103171f191883c3b156c9666eb5768a8af
No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3949476
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Commit-Queue: Dana Fried <dfried@google.com>
Reviewed-by: Abigail Klein <abigailbklein@google.com>
Cr-Commit-Position: refs/heads/main@{#1058130}

[modify] https://crrev.com/485e1c0e23a6846096b537a665869f33a9798f89/chrome/browser/ui/views/side_panel/read_anything/read_anything_coordinator.cc
[modify] https://crrev.com/485e1c0e23a6846096b537a665869f33a9798f89/chrome/browser/ui/views/side_panel/read_anything/read_anything_coordinator.h


### [Deleted User] (2022-10-12)

Requesting merge to stable M106 because latest trunk commit (1058076) appears to be after stable branch point (1036826).

Requesting merge to beta M107 because latest trunk commit (1058076) appears to be after beta branch point (1047731).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-10-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/dfd25363b9ec4c342541554f21bcc1bb6f249adf

commit dfd25363b9ec4c342541554f21bcc1bb6f249adf
Author: Abigail Klein <abigailbklein@google.com>
Date: Wed Oct 12 19:04:19 2022

Reland of "[Read Anything] Do not use ScopedObservation for SidePanelEntry"

This reverts commit 485e1c0e23a6846096b537a665869f33a9798f89.

Reason for revert: Fix test failures

Original change's description:
> [Build Sheriff] Revert "[Read Anything] Do not use ScopedObservation for SidePanelEntry"
>
> This reverts commit a1cf2dac62547361d560cbe39970d0c39b081418.
>
> Reason for revert: Causing a number of test failures (see bug)
> Bug: 1373964
>
> Original change's description:
> > [Read Anything] Do not use ScopedObservation for SidePanelEntry
> > observation.
> >
> > This was causing a UAF. When the browser window closed, both the
> > SidePanelEntry and the ReadAnythingCoordinator were destroyed at the
> > same time as they are SupportsUserData and BrowserUserData,
> > respectively. When the ScopedObservation attempted to remove observer,
> > the pointer had already been freed. This change adds
> > ReadAnythingCoordinator as an observer to SidePanelEntry and removes
> > it as an observer via deregistering it from SidePanelRegistry.
> >
> > Bug: 1266555, 1344756, 1349795, 1352138, 1365832
> > Change-Id: Ib63faa9d385f577f1f96a0510759f07efa4b115a
> > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3820321
> > Reviewed-by: Martin Kreichgauer <martinkr@google.com>
> > Commit-Queue: Abigail Klein <abigailbklein@google.com>
> > Cr-Commit-Position: refs/heads/main@{#1058076}
>
> Bug: 1266555, 1344756, 1349795, 1352138, 1365832
> Change-Id: I8ba94a103171f191883c3b156c9666eb5768a8af
> No-Presubmit: true
> No-Tree-Checks: true
> No-Try: true
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3949476
> Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
> Commit-Queue: Dana Fried <dfried@google.com>
> Reviewed-by: Abigail Klein <abigailbklein@google.com>
> Cr-Commit-Position: refs/heads/main@{#1058130}

Bug: 1373964
Bug: 1266555, 1344756, 1349795, 1352138, 1365832
Change-Id: Ibee52fc389fc03e0e1a7fa24bed412a9d90a009e
No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3950072
Commit-Queue: Martin Kreichgauer <martinkr@google.com>
Auto-Submit: Abigail Klein <abigailbklein@google.com>
Reviewed-by: Martin Kreichgauer <martinkr@google.com>
Cr-Commit-Position: refs/heads/main@{#1058202}

[modify] https://crrev.com/dfd25363b9ec4c342541554f21bcc1bb6f249adf/chrome/browser/ui/views/side_panel/read_anything/read_anything_coordinator.cc
[modify] https://crrev.com/dfd25363b9ec4c342541554f21bcc1bb6f249adf/chrome/browser/ui/views/side_panel/read_anything/read_anything_toolbar_view_browsertest.cc
[modify] https://crrev.com/dfd25363b9ec4c342541554f21bcc1bb6f249adf/chrome/browser/ui/views/side_panel/read_anything/read_anything_coordinator.h


### [Deleted User] (2022-10-12)

Merge review required: a reverted commit was detected after the merge request.

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
Owners: govind (Android), eakpobaro (iOS), dgagnon (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-10-12)

Merge review required: a reverted commit was detected after the merge request.

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

### [Deleted User] (2022-10-13)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-10-13)

This reland just occurred 21 hours ago, so going to continue to defer merge approval for a bit to allow for sufficient bake time on canary. 

### am...@chromium.org (2022-10-17)

In reviewing the fix for merge review, I'm now realizing this issue is in Unified Side Panel which is not enabled by default, updating as SI-None. No merge is required here unless the plan is for this feature to be enabled or being field trial testing in M107 (please reach out to me if this is the case). 

### cl...@chromium.org (2022-10-19)

ClusterFuzz testcase 5133621486878720 is still reproducing on tip-of-tree build (trunk).

Please re-test your fix against this testcase and if the fix was incorrect or incomplete, please re-open the bug. Otherwise, ignore this notification and add the ClusterFuzz-Wrong label.

### am...@chromium.org (2022-10-19)

re-opening this bug as it appears this issue is reproducing on clusterfuzz: https://clusterfuzz.com/testcase?key=5133621486878720

abigailbklein@, can you PTAL and address when you have an opportunity? 



### me...@gmail.com (2022-10-23)

[Comment Deleted]

### me...@gmail.com (2022-11-03)

Hi Amy, I think the report of ClusterFuzz is wrong, because it use version Chromium: 1031638 to reproduce this issue. However, this issue is fixed on Chromium:1058202. And I also test it on my own Mac ,it is no longer reproducible on Chromium:1058202. So I think you could mark it as fixed:)


### me...@gmail.com (2022-11-11)

Hi amyressler@, could you please take a look at this issue? Thank you.

### am...@chromium.org (2022-11-11)

Thanks for the ping, Krace. Yes, there looks to be an issue with clusterfuzz and the mac build. Updating as fixed. 

### wf...@chromium.org (2022-11-16)

[Empty comment from Monorail migration]

[Monorail components: -UI>Accessibility UI>Browser>TopChrome>SidePanel]

### am...@google.com (2022-11-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-11-17)

Congratulations, Krace! The VRP Panel has decided to award you $4,000 for this report of a moderately mitigated security bug. Thank you for your effort and reporting this issue to us! 

### am...@google.com (2022-11-19)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-17)

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

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1344756?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/1349795, crbug.com/chromium/1352138, crbug.com/chromium/1365832]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060288)*
