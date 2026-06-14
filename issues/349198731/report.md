# heap-use-after-free on DownloadManagerTabHelper::DidCreateDownload

| Field | Value |
|-------|-------|
| **Issue ID** | [349198731](https://issues.chromium.org/issues/349198731) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>Downloads |
| **Platforms** | iOS |
| **Chrome Version** | 126.0.0.0 |
| **Reporter** | li...@gmail.com |
| **Assignee** | sd...@google.com |
| **Created** | 2024-06-25 |
| **Bounty** | $11,000.00 |

## Description

# Steps to reproduce the problem

1. apply the patch, (The path of the patch is not important, just for better triggering)
2. see the mov.

# Problem Description

0. similar issue:40057634, the block function here uses completionHandler, so it is asynchronous, and then destroying this before `DidCreateDownload` is run will cause UAF, because in the block function, the member variable of this is used Equivalent to `this->member`.

```
void DownloadManagerTabHelper::SetCurrentDownload(
    std::unique_ptr<web::DownloadTask> task) {
  // If downloads are persistent, they cannot be lost once completed.
  if (!task_ || (task_->GetState() == web::DownloadTask::State::kComplete &&
                 !WillDownloadTaskBeSavedToDrive())) {
    // The task is the first download for this web state.
    DidCreateDownload(std::move(task));
    return;
  }

  __block std::unique_ptr<web::DownloadTask> block_task = std::move(task);
  [delegate_ downloadManagerTabHelper:this
              decidePolicyForDownload:block_task.get()
                    completionHandler:^(NewDownloadPolicy policy) {
                      if (policy == kNewDownloadPolicyReplace) {
                        DidCreateDownload(std::move(block_task)); //<--
                      }
                    }];
}

```

1. `DidCreateDownload` uses this member variables task\_, web\_state\_, delegate\_started\_

```
void DownloadManagerTabHelper::DidCreateDownload(
    std::unique_ptr<web::DownloadTask> task) {
  if (task_) {
    task_->RemoveObserver(this); //<-- UAF
    task_ = nullptr;//<--
  }
  task_ = std::move(task);//<--
  task_->AddObserver(this);//<--
  if (web_state_->IsVisible() && delegate_) {//<--
    delegate_started_ = true;//<--
    [delegate_ downloadManagerTabHelper:this
                      didCreateDownload:task_.get()//
                      webStateIsVisible:true];
  }
}

```

2. The life cycle of DownloadManagerTabHelper is related to `web::WebStateUserData`, which is equivalent to `SupportsUserData`, which means that `DownloadManagerTabHelper` will be destroyed after the web page is closed.

```
class DownloadManagerTabHelper
    : public web::WebStateUserData<DownloadManagerTabHelper>,
      public web::WebStateObserver,
      public web::DownloadTaskObserver {
 public:
  DownloadManagerTabHelper(const DownloadManagerTabHelper&) = delete;
  DownloadManagerTabHelper& operator=(const DownloadManagerTabHelper&) = delete;


```

[0]. <https://source.chromium.org/chromium/chromium/src/+/main:ios/chrome/browser/download/model/download_manager_tab_helper.mm;l=52;bpv=0;bpt=1>
[1]. <https://source.chromium.org/chromium/chromium/src/+/main:ios/chrome/browser/download/model/download_manager_tab_helper.mm;l=157;drc=90cac1911508d3d682a67c97aa62483eb712f69a;bpv=0;bpt=1>
[2]. <https://source.chromium.org/chromium/chromium/src/+/main:ios/chrome/browser/download/model/download_manager_tab_helper.h;l=27;drc=90cac1911508d3d682a67c97aa62483eb712f69a;bpv=0;bpt=1>

bitset:
<https://source.chromium.org/chromium/chromium/src/+/d3fe4f47ab33d6ca1e24712492e25f2f0e997695>

fix suggestion:
don't use member variable.

# Summary

heap-use-after-free on DownloadManagerTabHelper::DidCreateDownload

# Custom Questions

#### Type of crash:

browser

#### Crash state:

see uaf4-asan.log

# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: N/A

## Attachments

- [poc.mov](attachments/poc.mov) (video/quicktime, 49.2 MB)
- [uaf4-asan.log](attachments/uaf4-asan.log) (text/plain, 65.6 KB)
- [poc4.html](attachments/poc4.html) (text/html, 124 B)
- [uaf.diff](attachments/uaf.diff) (text/x-diff, 2.2 KB)
- [fix4.patch](attachments/fix4.patch) (text/x-diff, 1.7 KB)

## Timeline

### li...@gmail.com (2024-06-25)

Fix:
The root cause of the vulnerability is that `web_state_` is deleted, causing this to be deleted, and it is not completely asynchronous across threads, so we can use `weak_this` to fix it. After my verification, it works well.

### el...@chromium.org (2024-06-25)

Security shepherd: thanks for the report! I have also inspected the code and my findings match your own. Over to sdefresne@ from //ios/chrome/browser/download/model/OWNERS, and marking as Pri-1 / Sev-1 since this is a browser UaF.

### pe...@google.com (2024-06-26)

Setting milestone because of s0/s1 severity.

### sd...@google.com (2024-06-27)

Thank you for the report.

### ap...@google.com (2024-06-27)

Project: chromium/src
Branch: main

commit ef332eda241e4b8a6c3bf8d661fa8a92fc2758a1
Author: Sylvain Defresne <sdefresne@chromium.org>
Date:   Thu Jun 27 12:23:15 2024

    [ios] Use WeakPtr and callback to avoid capturing `this` in a block
    
    Use base::OnceCallback<...> and a base::WeakPtr<...> to avoid an
    accidental capture of `this` by a block (calling a non-static
    method requires `this`).
    
    Fixed: 349198731
    Change-Id: Ia068af4623d4963be6ab97df4924f513f404b524
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5663176
    Commit-Queue: Sylvain Defresne <sdefresne@chromium.org>
    Reviewed-by: Quentin Pubert <qpubert@google.com>
    Commit-Queue: Quentin Pubert <qpubert@google.com>
    Auto-Submit: Sylvain Defresne <sdefresne@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1320276}

M       ios/chrome/browser/download/model/download_manager_tab_helper.h
M       ios/chrome/browser/download/model/download_manager_tab_helper.mm

https://chromium-review.googlesource.com/5663176


### ea...@google.com (2024-06-27)

Merge review required: M126 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:

Why does your merge fit within the merge criteria for these milestones?
Chrome Browser: https://chromiumdash.appspot.com/branches
Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
What changes specifically would you like to merge? Please link to Gerrit.
Have the changes been released and tested on canary?
Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
[Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.
Please contact the milestone owner if you have questions. Owners: eakpobaro (Android), eakpobaro (iOS), ceb (ChromeOS), srinivassista (Desktop)

### sd...@google.com (2024-06-27)

1. Fix an exploitable UaF
2. <https://chromium-review.googlesource.com/c/chromium/src/+/5663176>
3. Just landed, so not yet.
4. See proof-of-concept in the original report.

### li...@gmail.com (2024-06-27)

Hi,please update the credit to : lime(@limeSec\_) From TIANGONG Team of Legendsec at QI-ANXIN Group, thanks. :)

### pe...@google.com (2024-06-28)

Merge review required: M127 is already shipping to beta.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: eakpobaro (Android), eakpobaro (iOS), alonbajayo (ChromeOS), danielyip (Desktop)

### sd...@google.com (2024-06-28)

1. Fix an exploitable UaF
2. <https://chromium-review.googlesource.com/c/chromium/src/+/5663176>
3. Just landed, so not yet.
4. No
5. Not applicable
6. See proof-of-concept in the original report.

### sp...@google.com (2024-07-03)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $11000.00 for this report.

Rationale for this decision:
$10,000 for report of mildly mitigated bug in a non-sandboxed process (mitigated by race and user gesture) +$1,000 bisect bonus


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-07-03)

Congratulations lime! Thank you for your efforts and reporting this issue to us -- nice work.

### am...@chromium.org (2024-07-03)

There is no canary on iOS we can't confirm performance and stability on Canary.
Extended Stable support is not relevant to iOS, and since this was landed right before release freeze, we don't have new data from which to work, so I'm declining merge to M126 Stable, the last update for which as Stable is on 15 July.

Let's go ahead and get this merged to M127 Beta, branch 6533.
This can be included in M127 early stable, being released on 17 July, so if there are any issues noted in Early Stable, this fix could be reverted before M127 Stable release.

### da...@google.com (2024-07-08)

Please land your merges before COP Tuesday to ensure it is included in this weeks Beta release.

For gitwatcher to update your merge request to Merge-Merged you will need to **include the bug id in the commit message**.


### pe...@google.com (2024-07-08)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### pe...@google.com (2024-07-12)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ap...@google.com (2024-07-15)

Project: chromium/src
Branch: refs/branch-heads/6533

commit 698aa7ddb0b69a5696801487d9acdd0556dec7c4
Author: Sylvain Defresne <sdefresne@chromium.org>
Date:   Mon Jul 15 08:47:39 2024

    [127][ios] Use WeakPtr and callback to avoid capturing `this` in a block
    
    Use base::OnceCallback<...> and a base::WeakPtr<...> to avoid an
    accidental capture of `this` by a block (calling a non-static
    method requires `this`).
    
    (cherry picked from commit ef332eda241e4b8a6c3bf8d661fa8a92fc2758a1)
    
    Fixed: 349198731
    Change-Id: Ia068af4623d4963be6ab97df4924f513f404b524
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5663176
    Commit-Queue: Sylvain Defresne <sdefresne@chromium.org>
    Reviewed-by: Quentin Pubert <qpubert@google.com>
    Commit-Queue: Quentin Pubert <qpubert@google.com>
    Auto-Submit: Sylvain Defresne <sdefresne@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1320276}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5703221
    Reviewed-by: Olivier Robin <olivierrobin@chromium.org>
    Commit-Queue: Olivier Robin <olivierrobin@chromium.org>
    Cr-Commit-Position: refs/branch-heads/6533@{#1465}
    Cr-Branched-From: 7e0b87ec6b8cb5cb2969e1479fc25776e582721d-refs/heads/main@{#1313161}

M       ios/chrome/browser/download/model/download_manager_tab_helper.h
M       ios/chrome/browser/download/model/download_manager_tab_helper.mm

https://chromium-review.googlesource.com/5703221


### pe...@google.com (2024-10-04)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/349198731)*
