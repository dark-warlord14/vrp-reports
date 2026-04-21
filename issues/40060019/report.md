# Security: potential use after free in OfflinePageModelTaskified::Unpublish

| Field | Value |
|-------|-------|
| **Issue ID** | [40060019](https://issues.chromium.org/issues/40060019) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Offline |
| **Platforms** | Android |
| **Reporter** | wx...@gmail.com |
| **Assignee** | iw...@chromium.org |
| **Created** | 2022-06-20 |
| **Bounty** | $1,000.00 |

## Description

**This template is ONLY for reporting security bugs. If you are reporting a**  

**Download Protection Bypass bug, please use the "Security - Download**  

**Protection" template. For all other reports, please use a different**  

**template.**

**Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com>**  

**/chromium/src/+/HEAD/docs/security/faq.md**

**Please see the following link for instructions on filing security bugs:**  

**<https://www.chromium.org/Home/chromium-security/reporting-security-bugs>**

**Reports may be eligible for reward payments under the Chrome VRP:**  

**<http://g.co/ChromeBugRewards>**

**NOTE: Security bugs are normally made public once a fix has been widely**  

**deployed.**

**-------------------------**

**VULNERABILITY DETAILS**  

**Please provide a brief explanation of the security issue.**

**VERSION**  

**Chrome Version: [x.x.x.x] + [stable, beta, or dev]**  

**Operating System: [Please indicate OS, version, and service pack level]**  

any version

**REPRODUCTION CASE**  

**Please include a demonstration of the security bug, such as an attached**  

**HTML or binary file that reproduces the bug when loaded in Chrome. PLEASE**  

**make the file as small as possible and remove any content not required to**  

**demonstrate the bug, or any personal or confidential information.**

**Please attach files directly, not in zip or other archive formats, and if**  

**you've created a demonstration site please also attach the files needed to**  

**reproduce the demonstration locally.**

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

**Type of crash: [tab, browser, etc.]**  

**Crash State: [see link above: stack trace \*with symbols\*, registers,**  

**exception record]**  

**Client ID (if relevant): [see link above]**

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

**Reporter credit: [goes here]**

## Timeline

### [Deleted User] (2022-06-20)

[Empty comment from Monorail migration]

### wx...@gmail.com (2022-06-20)

in function  OfflinePageModelTaskified::OnDeleteDone
```
void OfflinePageModelTaskified::OnDeleteDone(
    DeletePageCallback callback,
    DeletePageResult result,
    const std::vector<OfflinePageItem>& deleted_items) {
  UMA_HISTOGRAM_ENUMERATION("OfflinePages.DeletePageResult", result);
  std::vector<PublishedArchiveId> publish_ids;

  // Notify observers and run callback.
  for (const auto& item : deleted_items) {
    UMA_HISTOGRAM_ENUMERATION(
        "OfflinePages.DeletePageCount",
        model_utils::ToNamespaceEnum(item.client_id.name_space));
    offline_event_logger_.RecordPageDeleted(item.offline_id);
    for (Observer& observer : observers_)
      observer.OfflinePageDeleted(item);

    publish_ids.emplace_back(item.system_download_id, item.file_path);
  }

  // Remove the page from the system download manager. We don't need to wait for
  // completion before calling the delete page callback.
  task_runner_->PostTask(FROM_HERE,
                         base::BindOnce(&OfflinePageModelTaskified::Unpublish,  //here push sequence task 
                                        archive_publisher_.get(), publish_ids));

  if (!callback.is_null())
    std::move(callback).Run(result);
}
```

it post raw pointer archive_publisher_, when class OfflinePageModelTaskified is deleted, archive_publisher_ will be deleted.

then in function OfflinePageModelTaskified::Unpublish
```
void OfflinePageModelTaskified::Unpublish(
    OfflinePageArchivePublisher* publisher,
    const std::vector<PublishedArchiveId>& publish_ids) {
  if (!publish_ids.empty())
    publisher->UnpublishArchives(publish_ids);  // it will directly use raw_ptr
}
```

OfflinePageModelTaskified   is a keyed service when Profile destoryed, it will also be destroyed.
so it may win the race condition to cause uaf.



### wx...@gmail.com (2022-06-20)

the issue is similar as https://crbug.com/chromium/1337671

### xi...@chromium.org (2022-06-21)

Thanks for the report! Tentatively set severity to high, but if it turns out that the use of raw pointer is safe here, it should not be a security bug. +iwells@, could you take a look? Thanks!

[Monorail components: UI>Browser>Offline]

### [Deleted User] (2022-06-21)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-21)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### iw...@chromium.org (2022-06-28)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-06-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/1544702b7568494a9c5226d3dadf3dbf12e6e25a

commit 1544702b7568494a9c5226d3dadf3dbf12e6e25a
Author: Ian Wells <iwells@chromium.org>
Date: Wed Jun 29 16:59:26 2022

Use weak pointer to OfflinePageArchivePublisher as Unpublish() may run after publisher is destroyed

Also remove some unneeded includes.

Bug: 1337798
Change-Id: I47097cbb7341fc731789991ada9e63c7513d8cc7
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3733637
Reviewed-by: Dan H <harringtond@chromium.org>
Commit-Queue: Ian Wells <iwells@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1019208}

[modify] https://crrev.com/1544702b7568494a9c5226d3dadf3dbf12e6e25a/components/offline_pages/core/offline_page_test_archive_publisher.cc
[modify] https://crrev.com/1544702b7568494a9c5226d3dadf3dbf12e6e25a/components/offline_pages/core/offline_page_test_archive_publisher.h
[modify] https://crrev.com/1544702b7568494a9c5226d3dadf3dbf12e6e25a/chrome/browser/offline_pages/android/offline_page_archive_publisher_impl.h
[modify] https://crrev.com/1544702b7568494a9c5226d3dadf3dbf12e6e25a/components/offline_pages/core/offline_page_archive_publisher.h
[modify] https://crrev.com/1544702b7568494a9c5226d3dadf3dbf12e6e25a/chrome/browser/offline_pages/android/offline_page_archive_publisher_impl.cc
[modify] https://crrev.com/1544702b7568494a9c5226d3dadf3dbf12e6e25a/components/offline_pages/core/model/offline_page_model_taskified.cc
[modify] https://crrev.com/1544702b7568494a9c5226d3dadf3dbf12e6e25a/components/offline_pages/core/model/offline_page_model_taskified.h


### iw...@chromium.org (2022-06-29)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-29)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-29)

Requesting merge to extended stable M102 because latest trunk commit (1019208) appears to be after extended stable branch point (992738).

Requesting merge to stable M103 because latest trunk commit (1019208) appears to be after stable branch point (1002911).

Requesting merge to beta M104 because latest trunk commit (1019208) appears to be after beta branch point (1012729).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2022-06-29)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-30)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-30)

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

### [Deleted User] (2022-06-30)

Merge review required: M103 is already shipping to stable.

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
Owners: govind (Android), harrysouders (iOS), dgagnon (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-06-30)

Merge review required: M102 is already shipping to stable.

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

### iw...@google.com (2022-06-30)

1. Why does your merge fit within the merge criteria for these milestones?

This merge will fix a potential use-after-free bug that poses a security risk.

2. What changes specifically would you like to merge? Please link to Gerrit.

https://chromium-review.googlesource.com/c/chromium/src/+/3733637

3. Have the changes been released and tested on canary?

Yes.

4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?

Not a new feature.

5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents

N/A

6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

No manual testing required.

### am...@google.com (2022-07-06)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-07-06)

Congratulations! The VRP Panel has decided to award you $1,000 for this report. The reward amount was decided upon based on this issue not having a POC, stack trace, or other artifacts to demonstrate this issue. The potential for attacker control appears mitigated by a race condition. Additionally, based on analysis, there is no evidence this could be exploited without direct UI interaction and that this issue is not web accessible. We appreciate your efforts and reporting this issue to us. 

### wx...@gmail.com (2022-07-07)

[Comment Deleted]

### wx...@gmail.com (2022-07-07)

  Thanks, amy

### am...@google.com (2022-07-08)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-08)

Given the mitigations noted in https://crbug.com/chromium/1337798#c19, reducing to medium severity. 
M104 merge approved, please merge this fix to branch 5112 at your earliest convenience. 



### gi...@appspot.gserviceaccount.com (2022-07-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/52e52a441cf0b7b1312c0ad2c5a8ef0f364c630f

commit 52e52a441cf0b7b1312c0ad2c5a8ef0f364c630f
Author: Ian Wells <iwells@chromium.org>
Date: Fri Jul 08 20:40:20 2022

M104: Use weak pointer to OfflinePageArchivePublisher as Unpublish() may run after publisher is destroyed

Also remove some unneeded includes.

(cherry picked from commit 1544702b7568494a9c5226d3dadf3dbf12e6e25a)

Bug: 1337798
Change-Id: I47097cbb7341fc731789991ada9e63c7513d8cc7
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3733637
Reviewed-by: Dan H <harringtond@chromium.org>
Commit-Queue: Ian Wells <iwells@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1019208}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3738620
Commit-Queue: Dan H <harringtond@chromium.org>
Auto-Submit: Ian Wells <iwells@chromium.org>
Cr-Commit-Position: refs/branch-heads/5112@{#702}
Cr-Branched-From: b13d3fe7b3c47a56354ef54b221008afa754412e-refs/heads/main@{#1012729}

[modify] https://crrev.com/52e52a441cf0b7b1312c0ad2c5a8ef0f364c630f/components/offline_pages/core/offline_page_test_archive_publisher.cc
[modify] https://crrev.com/52e52a441cf0b7b1312c0ad2c5a8ef0f364c630f/components/offline_pages/core/offline_page_test_archive_publisher.h
[modify] https://crrev.com/52e52a441cf0b7b1312c0ad2c5a8ef0f364c630f/chrome/browser/offline_pages/android/offline_page_archive_publisher_impl.h
[modify] https://crrev.com/52e52a441cf0b7b1312c0ad2c5a8ef0f364c630f/components/offline_pages/core/offline_page_archive_publisher.h
[modify] https://crrev.com/52e52a441cf0b7b1312c0ad2c5a8ef0f364c630f/chrome/browser/offline_pages/android/offline_page_archive_publisher_impl.cc
[modify] https://crrev.com/52e52a441cf0b7b1312c0ad2c5a8ef0f364c630f/components/offline_pages/core/model/offline_page_model_taskified.cc
[modify] https://crrev.com/52e52a441cf0b7b1312c0ad2c5a8ef0f364c630f/components/offline_pages/core/model/offline_page_model_taskified.h


### am...@chromium.org (2022-08-01)

[Empty comment from Monorail migration]

### am...@google.com (2022-08-02)

[Empty comment from Monorail migration]

### am...@google.com (2022-08-12)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-08-12)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-05)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1337798?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060019)*
