# UAF in MerchantViewerDataManager

| Field | Value |
|-------|-------|
| **Issue ID** | [40061803](https://issues.chromium.org/issues/40061803) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Shopping>Cart |
| **Platforms** | Android |
| **Reporter** | ha...@gmail.com |
| **Assignee** | yu...@chromium.org |
| **Created** | 2022-11-18 |
| **Bounty** | $1,000.00 |

## Description

**Steps to reproduce the problem:**  

This UAF is similar with the previous <https://crbug.com/chromium/1385709>, but their root cause and the UAF places are different.

**Problem Description:**  

browser UAF.

**Additional Comments:**

\*\*Chrome version: \*\* 107.0.5304.87 \*\*Channel: \*\* Stable

**OS:** Android

## Timeline

### ha...@gmail.com (2022-11-18)

## Details

`MerchantViewerDataManager` is a KeyedService. When we clean up the history data (e.g. the commerce data), the `BrowsingDataHistoryObserverService::OnURLsDeleted` will have the following call chain:

BrowsingDataHistoryObserverService::OnURLsDeleted
-> ClearCommerceData [1]
-> MerchantViewerDataManager::DeleteMerchantViewerDataForTimeRange or MerchantViewerDataManager::DeleteMerchantViewerDataForOrigins [2]
-> SessionProtoDB<T>::LoadAllEntries [3][4]  ( bound with the weak MerchantViewerDataManager::OnLoadAllEntriesForOriginsCallback and MerchantViewerDataManager::OnLoadAllEntriesForTimeRangeCallback callback )

If the SessionProtoDB is initialized with error, `SessionProtoDB<T>::LoadAllEntries` will post the callback to the background thread [5]. 

Therefore, the `MerchantViewerDataManager::OnLoadAllEntriesForOriginsCallback` and the `MerchantViewerDataManager::OnLoadAllEntriesForTimeRangeCallback` weak callback could be executed on the separate thread. And those callback doesn't checks whether the db result is success or not. This is problematic since the `MerchantViewerDataManager` may destroyed when those callback are executing and calls `HasValidDB()` function [6][7], accessing the freed `proto_db_` member variable in [8], leading to the UAF.


[1]https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/browsing_data/browsing_data_history_observer_service.cc;l=240;drc=603337a74bf04efd536b251a7f2b4eb44fe153a9

[2]https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/browsing_data/browsing_data_history_observer_service.cc;l=104-111;drc=603337a74bf04efd536b251a7f2b4eb44fe153a9

[3]https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/commerce/merchant_viewer/merchant_viewer_data_manager.cc;l=104-106;drc=603337a74bf04efd536b251a7f2b4eb44fe153a9

    proto_db_->LoadAllEntries(base::BindOnce(
        &MerchantViewerDataManager::OnLoadAllEntriesForOriginsCallback,  // [3]
        weak_ptr_factory_.GetWeakPtr(), std::move(deleted_hostnames)));

[4]https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/commerce/merchant_viewer/merchant_viewer_data_manager.cc;l=125-127;drc=603337a74bf04efd536b251a7f2b4eb44fe153a9

    proto_db_->LoadAllEntries(base::BindOnce(
        &MerchantViewerDataManager::OnLoadAllEntriesForTimeRangeCallback,  // [4]
        weak_ptr_factory_.GetWeakPtr(), created_after, created_before));


[5]https://source.chromium.org/chromium/chromium/src/+/main:components/session_proto_db/session_proto_db.h;l=206-208;drc=603337a74bf04efd536b251a7f2b4eb44fe153a9

[6]https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/commerce/merchant_viewer/merchant_viewer_data_manager.cc;l=34;drc=603337a74bf04efd536b251a7f2b4eb44fe153a9

void MerchantViewerDataManager::OnLoadAllEntriesForTimeRangeCallback(
    base::Time begin,
    base::Time end,
    bool success,
    MerchantSignals data) {
  DCHECK_CALLED_ON_VALID_SEQUENCE(sequence_checker_);
  if (!HasValidDB()) {  // [6]
    return;
  }

[7]https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/commerce/merchant_viewer/merchant_viewer_data_manager.cc;l=59;drc=603337a74bf04efd536b251a7f2b4eb44fe153a9

void MerchantViewerDataManager::OnLoadAllEntriesForOriginsCallback(
    const base::flat_set<std::string>& deleted_hostnames,
    bool success,
    MerchantSignals data) {
  DCHECK_CALLED_ON_VALID_SEQUENCE(sequence_checker_);
  if (!HasValidDB()) { // [7]
    return;
  }

[8]https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/commerce/merchant_viewer/merchant_viewer_data_manager.cc;l=139;drc=603337a74bf04efd536b251a7f2b4eb44fe153a9

bool MerchantViewerDataManager::HasValidDB() {
  return proto_db_ != nullptr;  // [8]
}


This UAF is introduced in the commit https://chromium-review.googlesource.com/c/chromium/src/+/2929448
Therefore, it has been a long time and affect all stable Android chromium.

### ha...@gmail.com (2022-11-18)

[Comment Deleted]

### [Deleted User] (2022-11-18)

[Empty comment from Monorail migration]

### ha...@gmail.com (2022-11-18)

[Comment Deleted]

### dr...@chromium.org (2022-11-21)

It's pretty hard for us to establish the exploitability of this bug without any kind of PoC, so +wychen@ and ayman@ as a courtesy that there might be a bug here. Please provide reproduction steps once you have them.

### ha...@gmail.com (2022-11-23)

[Comment Deleted]

### ca...@chromium.org (2022-11-30)

Traging this the same as 1385709. wychen can you PTAL? I think this is the same case of a very hard to trigger issue in the wild, but that is worth fixing. Thanks

[Monorail components: UI>Browser>Shopping>Cart]

### [Deleted User] (2022-11-30)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-30)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-11-30)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-12-02)

wychen: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-12-12)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-12-22)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-01-02)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-01-12)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@gmail.com (2023-01-19)

friendly ping -

### wy...@chromium.org (2023-01-19)

Yue, could you take a look at this one?

### yu...@chromium.org (2023-01-19)

Sure, thanks for filing! I think this issue has been fixed in https://chromium-review.googlesource.com/c/chromium/src/+/4088730 where instead of posting to background thread, we post the task in the current thread, so the callback won't run if MerchantViewerDataManager is destroyed hence no UAF. Therefore, I'm closing this as fixed, please lmk if there are any follow-up questions.

### [Deleted User] (2023-01-19)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-19)

[Empty comment from Monorail migration]

### am...@google.com (2023-01-26)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-01-26)

Congratulations! The VRP Panel has decided to award you $1,000 for this report of a heavily mitigated security bug. Thank you for you reporting this issue to us. 

### am...@google.com (2023-01-28)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-27)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1386011?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061803)*
