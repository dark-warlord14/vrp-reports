# UAF in CartService

| Field | Value |
|-------|-------|
| **Issue ID** | [40061793](https://issues.chromium.org/issues/40061793) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Shopping>Cart |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ha...@gmail.com |
| **Assignee** | wy...@chromium.org |
| **Created** | 2022-11-17 |
| **Bounty** | $2,500.00 |

## Description

**Steps to reproduce the problem:**  

This UAF is similar with the previous <https://crbug.com/chromium/1385709>. However, their root cause and the UAF places are different. Will attach details and PoC soon.

**Problem Description:**  

browser UAF.

**Additional Comments:**

\*\*Chrome version: \*\* 107.0.5304.87 \*\*Channel: \*\* Stable

**OS:** Mac OS

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 35.6 KB)
- [main.js](attachments/main.js) (text/plain, 362 B)
- [manifest.json](attachments/manifest.json) (text/plain, 176 B)
- [patch.diff](attachments/patch.diff) (text/plain, 1.8 KB)

## Timeline

### ha...@gmail.com (2022-11-17)

## Details

This UAF is similar with the previous UAF issue, however, the UAF places are different.

As the previous issue's details mentioned, when CartModule is loaded in NTP, it will call `getMerchantCarts` mojo function of the `CartHandler` [1]. 

Then `GetMerchantCarts` mojo implementation [2] have the following call chain:

CartService::LoadAllActiveCarts
-> CartDB::LoadAllCarts [3]
-> SessionProtoDB<T>::LoadAllEntries [4]

In `SessionProtoDB<T>::LoadAllEntries`, based on the above call chain, if the SessionProtoDB is initialized with error, i.e., the db file is corrupted or not success, it will post the callback to the background thread in [5].

> As for `LoadCartsWithFakeData` of CartService, it has the following callchain, which eventually also post the callback to the background thread in [6]

CartService::LoadCartsWithFakeData
-> CartDB::LoadCartsWithPrefix [7]
-> SessionProtoDB<T>::LoadContentWithPrefix [8]


Note that the weak pointer binding for `CartService::OnLoadCarts` function in [3] and [7] are problematic because they are posted to the background thread in [5][6].  While the `CartService` is destroyed on the UI thread, the `CartService::OnLoadCarts` executed in the background will not be canceled. This would lead to UAF when `CartService::OnLoadCarts` tries to access the 


1. The previous weak pointer bound with `GetCartDataCallback`, i.e., the `CartHandler` is working on the UI thread. However, the validation of the `CartHandler` weak pointer is executed on the background thread, this would cause the weak pointer validation become invalid due to the thread racing. That's to say, by the time `CartHandler` is freed, the `GetCartDataCallback` callback could still be executed.
2. If the `GetCartDataCallback` is already executed, however, the `CartHandler` is destroyed on the UI thread, the `GetCartDataCallback` runnning on the background thread can't be canceled, which makes the `GetCartDataCallback` still executing even the `CartHandler` is freed.

The above two problems will make the `GetCartDataCallback` still executes even though `CartHandler` is freed (by closing the WebContents, i.e., the NTP).

Since `commerce::IsFakeDataEnabled()` is false by default, `GetCartDataCallback` will calls `IsHidden` function, which results in the UAF while the accessing freed `cart_service_` member in [10] (note that the `NtpModulesRedesigned` feature used in `IsHidden` is disabled by default [11], hence `IsHidden` could access the `profile_` by default).


[1]https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/resources/new_tab_page/modules/cart/module.ts;l=520-530;drc=f8470ef0cdb0fb7c0a071f9aed2039af72f7ad85

async function createCartElement(): Promise<HTMLElement|null> {
  // getWarmWelcomeVisible makes server-side change and might flip the status of
  // whether welcome surface should show or not. Anything whose visibility
  // dependes on welcome surface (e.g. RBD consent) should check before
  // getWarmWelcomeVisible.
  const {consentVisible} =
      await ChromeCartProxy.getHandler().getDiscountConsentCardVisible();

  const {welcomeVisible} =
      await ChromeCartProxy.getHandler().getWarmWelcomeVisible();
  const {carts} = await ChromeCartProxy.getHandler().getMerchantCarts();    //   [1] call getMerchantCarts mojo function

[2]https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/cart/cart_handler.cc;l=29-38;drc=6dc39d60fea45c003424272efdb4c366119a9d7f

void CartHandler::GetMerchantCarts(GetMerchantCartsCallback callback) {
  DCHECK(IsCartModuleEnabled());
  if (base::GetFieldTrialParamValueByFeature(
          ntp_features::kNtpChromeCartModule,
          ntp_features::kNtpChromeCartModuleDataParam) == "fake") {
    cart_service_->LoadCartsWithFakeData(
        base::BindOnce(&CartHandler::GetCartDataCallback,
                       weak_factory_.GetWeakPtr(), std::move(callback)));  // [2]
  } else {
    cart_service_->LoadAllActiveCarts(
        base::BindOnce(&CartHandler::GetCartDataCallback,
                       weak_factory_.GetWeakPtr(), std::move(callback)));  // [2]
  }
}

[3]https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/cart/cart_service.cc;l=201-203;drc=b75fd5075a90ada27a3360df23fa08c83e24e995

void CartService::LoadAllActiveCarts(CartDB::LoadCallback callback) {
  cart_db_->LoadAllCarts(base::BindOnce(&CartService::OnLoadCarts,       // [3] binds CartService::OnLoadCarts with the CartService weak pointer
                                        weak_ptr_factory_.GetWeakPtr(),
                                        std::move(callback)));

[4]https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/cart/cart_db.cc;l=21;drc=b75fd5075a90ada27a3360df23fa08c83e24e995

void CartDB::LoadAllCarts(LoadCallback callback) {
  proto_db_->LoadAllEntries(std::move(callback));    // [4] the callback here is CartService::OnLoadCarts
}

[5]https://source.chromium.org/chromium/chromium/src/+/main:components/session_proto_db/session_proto_db.h;l=199-208;drc=b75fd5075a90ada27a3360df23fa08c83e24e995

template <typename T>
void SessionProtoDB<T>::LoadAllEntries(LoadCallback callback) {
  if (InitStatusUnknown()) {
    deferred_operations_.push_back(
        base::BindOnce(&SessionProtoDB::LoadAllEntries,
                       weak_ptr_factory_.GetWeakPtr(), std::move(callback)));
  } else if (FailedToInit()) {
    base::ThreadPool::PostTask(    
        FROM_HERE,
        base::BindOnce(std::move(callback), false, std::vector<KeyAndValue>()));  // [5] post the callback to the threadpool with the empty proto_pairs
  } else {
    storage_database_->LoadEntries(
        base::BindOnce(&SessionProtoDB::OnLoadContent,
                       weak_ptr_factory_.GetWeakPtr(), std::move(callback)));
  }
}


[6]https://source.chromium.org/chromium/chromium/src/+/main:components/session_proto_db/session_proto_db.h;l=217-235;drc=b75fd5075a90ada27a3360df23fa08c83e24e995

template <typename T>
void SessionProtoDB<T>::LoadContentWithPrefix(const std::string& key_prefix,
                                              LoadCallback callback) {
  if (InitStatusUnknown()) {
    deferred_operations_.push_back(base::BindOnce(
        &SessionProtoDB::LoadContentWithPrefix, weak_ptr_factory_.GetWeakPtr(),
        key_prefix, std::move(callback)));
  } else if (FailedToInit()) {
    base::ThreadPool::PostTask(
        FROM_HERE,
        base::BindOnce(std::move(callback), false, std::vector<KeyAndValue>()));    // [6] post the callback to the threadpool with the empty proto_pairs

[7]https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/cart/cart_service.cc;l=578-581;drc=b75fd5075a90ada27a3360df23fa08c83e24e995

void CartService::LoadCartsWithFakeData(CartDB::LoadCallback callback) {
  cart_db_->LoadCartsWithPrefix(
      kFakeDataPrefix,
      base::BindOnce(&CartService::OnLoadCarts, weak_ptr_factory_.GetWeakPtr(),  // [7] binds CartService::OnLoadCarts with the CartService weak pointer
                     std::move(callback)));
}


[8]https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/cart/cart_db.cc;l=26;drc=b75fd5075a90ada27a3360df23fa08c83e24e995

void CartDB::LoadCartsWithPrefix(const std::string& prefix,
                                 LoadCallback callback) {
  proto_db_->LoadContentWithPrefix(prefix, std::move(callback)); // [8]
}

[9]https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/cart/cart_service.cc;l=832;drc=b75fd5075a90ada27a3360df23fa08c83e24e995

void CartService::OnLoadCarts(CartDB::LoadCallback callback,
                              bool success,
                              std::vector<CartDB::KeyAndValue> proto_pairs) {
  if (commerce::IsFakeDataEnabled()) {
    std::sort(proto_pairs.begin(), proto_pairs.end(),
              CompareTimeStampForProtoPair);
    std::move(callback).Run(success, std::move(proto_pairs));
    return;
  }
  if (IsHidden()) {    // [9] CartService could be destroyed already
    std::move(callback).Run(success, {});    
    return;
  }


[10]https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/cart/cart_service.cc;l=191-192;drc=b75fd5075a90ada27a3360df23fa08c83e24e995

bool CartService::IsHidden() {
  return !base::FeatureList::IsEnabled(ntp_features::kNtpModulesRedesigned) &&  // [10] kNtpModulesRedesigned feature is disabled by default
         profile_->GetPrefs()->GetBoolean(prefs::kCartModuleHidden); // [10] access the freed `profile_` member, leading to the UAF
}

[11]https://source.chromium.org/chromium/chromium/src/+/main:components/search/ntp_features.cc;l=157-159;drc=b75fd5075a90ada27a3360df23fa08c83e24e995

BASE_FEATURE(kNtpModulesRedesigned,
             "NtpModulesRedesigned",
             base::FEATURE_DISABLED_BY_DEFAULT);




## Root cause

The root cause of this UAF is that CartService incorrectly use the weak pointer in [3][7], since the `CartService::OnLoadCarts` callback runs on the background thread, the weak pointer here plays no effect.

## PoC

To reproduce with the extension-only PoC:

1. Apply the attached patch. The patch simulate an possible blocking on the background thread, which is not related with the actual issue. Moreover, the patch also simulates the normal CartModule loading in the NTP (alsoalready mentioned in the previous issue). Finally, the patch simulates that the SessionProtoDB is initialized failed, which is a possible case.

2. Load the attached extension in chromium, the UAF occurs. ASan stack trace is attached as asan.txt


### [Deleted User] (2022-11-17)

[Empty comment from Monorail migration]

### ha...@gmail.com (2022-11-17)

[Comment Deleted]

### ha...@gmail.com (2022-11-17)

[Comment Deleted]

### dr...@chromium.org (2022-11-21)

I have similar concerns on this one about whether an attacker can really get the SessionDB to be corrupted. But still triaging to code owners to fix the pointer lifetime issues.

[Monorail components: UI>Browser>Shopping>Cart]

### [Deleted User] (2022-11-21)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-21)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-11-21)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### yu...@chromium.org (2022-11-21)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-11-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/562c79148a15dfa49f376aa6290847fab0f43d75

commit 562c79148a15dfa49f376aa6290847fab0f43d75
Author: Yue Zhang <yuezhanggg@chromium.org>
Date: Tue Nov 22 19:09:41 2022

[ChromeCart] Check cart load success

This CL fixes a potential UAF bug. When ChromeCart database (backed by
SessionProtoDB) fails to initialize, the callbacks from load attempts
will be posted to thread pool[1]. This could lead to the callback to
not be canceled and still execute after the component that initializes
the callback (e.g. CartService, CartHandler) is destroyed, and the
callback execution could potentially trigger UAF. This CL fixes this
issue by adding checks in the corresponding callbacks, and early return
if the load was failed.


[1] https://source.chromium.org/chromium/chromium/src/+/main:components/session_proto_db/session_proto_db.h;l=205-208;drc=7b5df6d4083453cd77a2fd7a1ca1ffce54154f4b;bpv=1;bpt=0

Bug: 1385831, 1385709
Change-Id: I75dfa658e988c16ed8a97839a7f57e5d615d0bf6
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4044017
Reviewed-by: David Maunder <davidjm@chromium.org>
Reviewed-by: David Trainor <dtrainor@chromium.org>
Commit-Queue: Yue Zhang <yuezhanggg@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1074781}

[modify] https://crrev.com/562c79148a15dfa49f376aa6290847fab0f43d75/components/session_proto_db/session_proto_storage.h
[modify] https://crrev.com/562c79148a15dfa49f376aa6290847fab0f43d75/chrome/browser/cart/cart_handler.cc
[modify] https://crrev.com/562c79148a15dfa49f376aa6290847fab0f43d75/chrome/browser/cart/cart_service.cc


### gi...@appspot.gserviceaccount.com (2022-11-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/6dd9cfd1cd7680dcc17a216518892c1fa762c237

commit 6dd9cfd1cd7680dcc17a216518892c1fa762c237
Author: Yue Zhang <yuezhanggg@chromium.org>
Date: Tue Nov 29 00:19:26 2022

[M109][ChromeCart] Check cart load success

This CL fixes a potential UAF bug. When ChromeCart database (backed by
SessionProtoDB) fails to initialize, the callbacks from load attempts
will be posted to thread pool[1]. This could lead to the callback to
not be canceled and still execute after the component that initializes
the callback (e.g. CartService, CartHandler) is destroyed, and the
callback execution could potentially trigger UAF. This CL fixes this
issue by adding checks in the corresponding callbacks, and early return
if the load was failed.


[1] https://source.chromium.org/chromium/chromium/src/+/main:components/session_proto_db/session_proto_db.h;l=205-208;drc=7b5df6d4083453cd77a2fd7a1ca1ffce54154f4b;bpv=1;bpt=0

(cherry picked from commit 562c79148a15dfa49f376aa6290847fab0f43d75)

Bug: 1385831, 1385709
Change-Id: I75dfa658e988c16ed8a97839a7f57e5d615d0bf6
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4044017
Reviewed-by: David Maunder <davidjm@chromium.org>
Reviewed-by: David Trainor <dtrainor@chromium.org>
Commit-Queue: Yue Zhang <yuezhanggg@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1074781}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4048972
Reviewed-by: Wei-Yin Chen <wychen@chromium.org>
Commit-Queue: Wei-Yin Chen <wychen@chromium.org>
Cr-Commit-Position: refs/branch-heads/5414@{#274}
Cr-Branched-From: 4417ee59d7bf6df7a9c9ea28f7722d2ee6203413-refs/heads/main@{#1070088}

[modify] https://crrev.com/6dd9cfd1cd7680dcc17a216518892c1fa762c237/components/session_proto_db/session_proto_storage.h
[modify] https://crrev.com/6dd9cfd1cd7680dcc17a216518892c1fa762c237/chrome/browser/cart/cart_handler.cc
[modify] https://crrev.com/6dd9cfd1cd7680dcc17a216518892c1fa762c237/chrome/browser/cart/cart_service.cc


### [Deleted User] (2022-11-29)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-02)

wychen: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### yu...@chromium.org (2022-12-02)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-02)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-02)

[Empty comment from Monorail migration]

### am...@google.com (2022-12-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-12-09)

Congratulations! The VRP Panel has decided to award you $2,500 for this report of this highly mitigated security bug. Thank you for efforts and reporting this issue to us! 

### am...@google.com (2022-12-10)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-01-09)

[Empty comment from Monorail migration]

### am...@google.com (2023-01-10)

[Empty comment from Monorail migration]

### pg...@google.com (2023-01-10)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-10)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1385831?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061793)*
