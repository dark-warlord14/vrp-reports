# UAF in CartHandler

| Field | Value |
|-------|-------|
| **Issue ID** | [40061782](https://issues.chromium.org/issues/40061782) |
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

will attach details and PoC soon.

**Problem Description:**  

browser UAF

**Additional Comments:**

\*\*Chrome version: \*\* 107.0.5304.87 \*\*Channel: \*\* Stable

**OS:** Mac OS

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 39.5 KB)
- [patch.diff](attachments/patch.diff) (text/plain, 2.3 KB)
- [1385709.webm](attachments/1385709.webm) (video/webm, 3.9 MB)
- [patch2.diff](attachments/patch2.diff) (text/plain, 2.3 KB)
- [main.js](attachments/main.js) (text/plain, 301 B)
- [manifest.json](attachments/manifest.json) (text/plain, 176 B)
- [1385709_with_ext.webm](attachments/1385709_with_ext.webm) (video/webm, 2.7 MB)

## Timeline

### ha...@gmail.com (2022-11-17)

## Details

CartModule is enabled by default currently, since `kNtpChromeCartModule` is enabled by default [1][2], consequently the `chromeCartModuleEnabled` will be set to true while loading the NTP webui. Therefore, the cart js module (v1 or v2) will be loaded in the NTP [4].
When the `ChromeCartModuleElement` is created in the NTP, in its `createCartElement` constructor, it will call `getMerchantCarts` mojo function of the `CartHandler` in [5]. 

The lifetime of `CartHandler` is bound with the WebContents, i.e., the NTP there. When its `GetMerchantCarts` mojo implementation is called, it will calls `LoadCartsWithFakeData` or the `LoadAllActiveCarts` of the CartService with its `GetCartDataCallback` weak callback binding. (Note that the logic of `LoadCartsWithFakeData` or `LoadAllActiveCarts` doesn't matter actually).

Take the `LoadAllActiveCarts` function of CartService for an example, i.e., the `else` control flow in [6]. The `CartService::LoadAllActiveCarts` function will have the following call chain:

CartService::LoadAllActiveCarts
-> CartDB::LoadAllCarts [7]
-> SessionProtoDB<T>::LoadAllEntries [8]

In `SessionProtoDB<T>::LoadAllEntries`, based on the above call chain, if the SessionProtoDB is initialized with error, i.e., the db file is corrupted or not success, it will post the callback to the background thread in [10].

> As for `LoadCartsWithFakeData` of CartService, it has the following callchain, which eventually also post the callback to the background thread in [14]

CartService::LoadCartsWithFakeData
-> CartDB::LoadCartsWithPrefix [12]
-> SessionProtoDB<T>::LoadContentWithPrefix [13]


The `callback` parameter ([10] or [14]) here is actually the `CartService::OnLoadCarts` in [8]. Moreover, the aforementioned `GetCartDataCallback` weak callback is actually bound with the `CartService::OnLoadCarts` callback in [7]. Therefore, the previous `GetCartDataCallback` with weak pointer will be executed no matter whether it is success or proto_pairs is empty in the background thread, since the `CartService::OnLoadCarts` callback is on the background thread. This is problematic because of the two reasons:

1. The previous weak pointer bound with `GetCartDataCallback`, i.e., the `CartHandler` is working on the UI thread. However, the validation of the `CartHandler` weak pointer is executed on the background thread, this would cause the weak pointer validation become invalid due to the thread racing. That's to say, by the time `CartHandler` is freed, the `GetCartDataCallback` callback could still be executed.
2. If the `GetCartDataCallback` is already executed, however, the `CartHandler` is destroyed on the UI thread, the `GetCartDataCallback` runnning on the background thread can't be canceled, which makes the `GetCartDataCallback` still executing even the `CartHandler` is freed.

The above two problems will make the `GetCartDataCallback` still executes even though `CartHandler` is freed (by closing the WebContents, i.e., the NTP), and results in the UAF while the accessing freed `cart_service_` member in [11].


[1]https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/new_tab_page/new_tab_page_util.cc;l=64-66;drc=b75fd5075a90ada27a3360df23fa08c83e24e995

[2]https://source.chromium.org/chromium/chromium/src/+/main:components/search/ntp_features.cc;l=78-80;drc=80c6dab8d39280b18eb5373b44a9a0e847378820

[3]https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/webui/new_tab_page/new_tab_page_ui.cc;l=481;drc=b75fd5075a90ada27a3360df23fa08c83e24e995

  source->AddBoolean("chromeCartModuleEnabled", IsCartModuleEnabled());

[4]https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/resources/new_tab_page/modules/module_descriptors.ts;l=38-44;drc=461cbce5dd50f3be929199ba41fd4ae47324b809

if (loadTimeData.getBoolean('chromeCartModuleEnabled')) {
  if (loadTimeData.getBoolean('modulesRedesignedEnabled')) {
    descriptorsV2.push(chromeCartV2Descriptor);
  } else {
    descriptors.push(chromeCartDescriptor);
  }
}

[5]https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/resources/new_tab_page/modules/cart/module.ts;l=520-530;drc=f8470ef0cdb0fb7c0a071f9aed2039af72f7ad85

async function createCartElement(): Promise<HTMLElement|null> {
  // getWarmWelcomeVisible makes server-side change and might flip the status of
  // whether welcome surface should show or not. Anything whose visibility
  // dependes on welcome surface (e.g. RBD consent) should check before
  // getWarmWelcomeVisible.
  const {consentVisible} =
      await ChromeCartProxy.getHandler().getDiscountConsentCardVisible();

  const {welcomeVisible} =
      await ChromeCartProxy.getHandler().getWarmWelcomeVisible();
  const {carts} = await ChromeCartProxy.getHandler().getMerchantCarts();    //   [5] call getMerchantCarts mojo function

[6]https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/cart/cart_handler.cc;l=29-38;drc=6dc39d60fea45c003424272efdb4c366119a9d7f

void CartHandler::GetMerchantCarts(GetMerchantCartsCallback callback) {
  DCHECK(IsCartModuleEnabled());
  if (base::GetFieldTrialParamValueByFeature(
          ntp_features::kNtpChromeCartModule,
          ntp_features::kNtpChromeCartModuleDataParam) == "fake") {
    cart_service_->LoadCartsWithFakeData(
        base::BindOnce(&CartHandler::GetCartDataCallback,
                       weak_factory_.GetWeakPtr(), std::move(callback)));  // [6] binds the GetCartDataCallback with weak pointer
  } else {
    cart_service_->LoadAllActiveCarts(
        base::BindOnce(&CartHandler::GetCartDataCallback,
                       weak_factory_.GetWeakPtr(), std::move(callback)));  // [6] binds the GetCartDataCallback with weak pointer
  }
}

[7]https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/cart/cart_service.cc;l=201-203;drc=b75fd5075a90ada27a3360df23fa08c83e24e995

void CartService::LoadAllActiveCarts(CartDB::LoadCallback callback) {
  cart_db_->LoadAllCarts(base::BindOnce(&CartService::OnLoadCarts,       // [7]
                                        weak_ptr_factory_.GetWeakPtr(),
                                        std::move(callback)));  // [7] binds the previous weak GetCartDataCallback to the callback parameter
}

[8]https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/cart/cart_db.cc;l=21;drc=b75fd5075a90ada27a3360df23fa08c83e24e995

void CartDB::LoadAllCarts(LoadCallback callback) {
  proto_db_->LoadAllEntries(std::move(callback));    // [8] the callback here is CartService::OnLoadCarts
}

[9]https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/cart/cart_service.cc;l=823-868;drc=b75fd5075a90ada27a3360df23fa08c83e24e995


void CartService::OnLoadCarts(CartDB::LoadCallback callback,
                              bool success,
                              std::vector<CartDB::KeyAndValue> proto_pairs) {
  if (commerce::IsFakeDataEnabled()) {
    std::sort(proto_pairs.begin(), proto_pairs.end(),
              CompareTimeStampForProtoPair);
    std::move(callback).Run(success, std::move(proto_pairs));    // [9] run the previous weak GetCartDataCallback
    return;
  }
  if (IsHidden()) {
    std::move(callback).Run(success, {});    // [9] run the previous weak GetCartDataCallback
    return;
  }
  std::set<std::string> merchants_to_erase;
  for (CartDB::KeyAndValue kv : proto_pairs) {
    const GURL& cart_url(GURL(kv.second.merchant_cart_url()));
    if (IsExpired(kv.second) || ShouldSkip(cart_url)) {
      // Removed carts should remain removed.
      if (!kv.second.is_removed()) {
        DeleteCart(cart_url, true);
      }
      merchants_to_erase.emplace(kv.second.key());
    }
  }
  proto_pairs.erase(
      std::remove_if(proto_pairs.begin(), proto_pairs.end(),
                     [merchants_to_erase](CartDB::KeyAndValue kv) {
                       return kv.second.is_hidden() || kv.second.is_removed() ||
                              merchants_to_erase.find(kv.second.key()) !=
                                  merchants_to_erase.end();
                     }),
      proto_pairs.end());
  for (auto proto_pair : proto_pairs) {
    if (RE2::FullMatch(re2::StringPiece(proto_pair.first),
                       GetSkipCartExtractionPattern())) {
      proto_pair.second.clear_product_image_urls();
      cart_db_->AddCart(proto_pair.first, proto_pair.second,
                        base::BindOnce(&CartService::OnOperationFinished,
                                       weak_ptr_factory_.GetWeakPtr()));
    }
  }
  // Sort items in timestamp descending order.
  std::sort(proto_pairs.begin(), proto_pairs.end(),
            CompareTimeStampForProtoPair);
  std::move(callback).Run(success, std::move(proto_pairs));    // [9] run the previous weak GetCartDataCallback
}

[10]https://source.chromium.org/chromium/chromium/src/+/main:components/session_proto_db/session_proto_db.h;l=199-208;drc=b75fd5075a90ada27a3360df23fa08c83e24e995

template <typename T>
void SessionProtoDB<T>::LoadAllEntries(LoadCallback callback) {
  if (InitStatusUnknown()) {
    deferred_operations_.push_back(
        base::BindOnce(&SessionProtoDB::LoadAllEntries,
                       weak_ptr_factory_.GetWeakPtr(), std::move(callback)));
  } else if (FailedToInit()) {
    base::ThreadPool::PostTask(    
        FROM_HERE,
        base::BindOnce(std::move(callback), false, std::vector<KeyAndValue>()));  // [10] post the callback to the threadpool with the empty proto_pairs
  } else {
    storage_database_->LoadEntries(
        base::BindOnce(&SessionProtoDB::OnLoadContent,
                       weak_ptr_factory_.GetWeakPtr(), std::move(callback)));
  }
}

[11]https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/cart/cart_handler.cc;l=69-98;drc=b75fd5075a90ada27a3360df23fa08c83e24e995

void CartHandler::GetCartDataCallback(GetMerchantCartsCallback callback,
                                      bool success,
                                      std::vector<CartDB::KeyAndValue> res) {
  std::vector<chrome_cart::mojom::MerchantCartPtr> carts;
  bool show_discount = cart_service_->IsCartDiscountEnabled();  // [11] since `CartHandler` could be freed already, access freed `cart_service_` member will cause UAF here.

[12]https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/cart/cart_service.cc;l=578-581;drc=b75fd5075a90ada27a3360df23fa08c83e24e995

[13]https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/cart/cart_db.cc;l=26;drc=b75fd5075a90ada27a3360df23fa08c83e24e995

[14]https://source.chromium.org/chromium/chromium/src/+/main:components/session_proto_db/session_proto_db.h;l=217-235;drc=b75fd5075a90ada27a3360df23fa08c83e24e995

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
        base::BindOnce(std::move(callback), false, std::vector<KeyAndValue>()));    // [14] post the callback to the threadpool with the empty proto_pairs

## Root cause

The root cause of this UAF are:
1. CartService (i.e., the profile lifetime) outlives CartHandler (i.e., the WebContent lifetime). 
2. the incorrect weak pointer usage here, lacking consider the racing invalidation of weak pointer in the background thread.

This means that, the callback in CartService won't be canceled when CartHandler is destroyed. And the callback of CartHandler is executed on the background thread, the weak pointer of `CartHandler` can't avoid / guarantee the callback being executed safely.

## PoC

There are many ways to trigger this PoC. 

### The ideal way (only require an malicious extension)

The ideal way is to enable `CartModule` in NTP, note that although it is enabled by default, it seems doesn't shown in the NTP. I managed to trigger it by both visit cart related web site but failed, this might caused by the reason that the CartModule may only enabled in the US country or the English-speaking region.

As previously mentioned, in the `createCartElement` constructor, it will call `getMerchantCarts` mojo function of the `CartHandler` in [5], which means by enable the cart module, the `getMerchantCarts` will be called when loading the NTP. We could use an malicious extension to constantly create and close the NTP to trigger this UAF. Since it could triggered by the extension, this is an serious issue.

### Require compromised renderer

Moreover, since the `CartHandler` is reachable from the NTP, we could leverage an UXSS (help to execute the `getMerchantCarts` mojo call in NTP) or the compromised NTP renderer to trigger this UAF.

Note that I'm also tried to trigger this from the normal compromised renderer, but always got `Connection error` from the mojom js when call `getMerchantCarts`. However, the `CartHandler` interface binding works well, which means that the `CartHandler` mojo is reachable. I haven't tried to use the c++ bindings in the compromised renderer. Hence this UAF may reachable by the compromised renderer in theory.

Here I provide an convenient method which leverage an compromised NTP renderer to trigger the UAF:

1. apply the attached patch. The patch simulate an possible blocking on the background thread, which is not related with the actual issue. Moreover, the patch also simulates a compromised NTP renderer (which could also be replaced by the UXSS, executing the `getMerchantCarts` js function in NTP). Finally, the patch simulate that the SessionProtoDB is initialized failed, which is a possible case.

2. open an new-tab-page in chromium, the UAF occurs.


## Biesect 

This UAF is introduced by the commit https://chromium-review.googlesource.com/c/chromium/src/+/2633972

Therefore, it has been a long time and affect all stable release Chrome.

## Patch suggestion

We could rewrite `CartHandler::GetCartDataCallback` to a static function, which get CartService dynamically, instead of accessing the possible freed `cart_service_` member.



### [Deleted User] (2022-11-17)

[Empty comment from Monorail migration]

### ha...@gmail.com (2022-11-17)

Attached the video of the second method

### ha...@gmail.com (2022-11-17)

Complement/Correction for the above methods: since the getMerchantCarts is reachable once the default NTP is loaded (not comprimised), we could also apply this attached patch2.diff to just simulate the normal NTP with cart module.

Note that this patch it self doesn't change any logic of the NTP, and actually not simulate the compromised NTP, due to the CartHandler itself as well as the getMerchantCarts is loaded while loading NTP by default. It just loading the CartHandler in advance (simluate the normal CartModule), to avoid some effort to enable CartModule in NTP.

Hence here attached an extension-only method PoC and the video. Please repro it by applying the patch2.diff and loading the attached extension:

./Chromium.app/Contents/MacOS/Chromium  --load-extension=/path/to/extension

### ha...@gmail.com (2022-11-17)

There are another UAF in the similar component, but with the different root cause and the UAF place. I've opened a new issue as https://crbug.com/chromium/1385831.

### dr...@chromium.org (2022-11-21)

I'm kind of skeptical about this one. I'm not sure an attacker can force the SessionDB to fail to initialize, so I think this can only apply to users who have corrupted databases for some other reason. But it does reproduce as claimed in M107, and I think we can do better here. Adding security labels and triaging to cart owners.

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

Thanks for filing and the detailed report! Agree to drubery@ in https://crbug.com/chromium/1385709#c6, I don't think an attacker could force SessionDB to fail to initialize. That said, we should fix this.

As for the fix itself, I think we can follow the idea of crbug.com/1385831, i.e. Check if the load is successful and early return if it fails. I'll come up a fix and merge it to M109. Thanks again for the report and lmk if you have further questions.

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


### yu...@chromium.org (2022-11-22)

[Empty comment from Monorail migration]

### yu...@chromium.org (2022-11-23)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-23)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-23)

Merge approved: your change passed merge requirements and is auto-approved for M109. Please go ahead and merge the CL to branch 5414 (refs/branch-heads/5414) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: govind (Android), eakpobaro (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-11-24)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-28)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pb...@google.com (2022-11-28)

[Bulk Edit] This merge has been approved for M109, please help complete your merges asap (before 4pm PST) today, so the change can be included in this week's RC build for dev/beta releases

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


### am...@google.com (2022-12-02)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-12-02)

Congratulations, Chaoyuan Peng! The VRP Panel has decided to award you $2,500 for this report of a heavily mitigated security bug + bisect bonus. Thank you for your efforts and reporting this issue to us! 

### ha...@gmail.com (2022-12-02)

[Comment Deleted]

### am...@chromium.org (2022-12-02)

Thank you for you for your comments and questions.  

Security_Impact-None is not a label that defines security impact in the conventional sense, in terms of the bug impact to users, but the label is used to define the impact of the bug to an active release channel of Chrome shipped to users. This label is specifically a part of and defined by our internal security bug triage and merge/release processes, only and is is not related to bug severity and exploitability. When we use the SI-None label, it means that the code with the vulnerability is not enabled by default in a shipped version of Chrome, such as that feature being behind a command line flag. 

I believe there is an issue here of word semantics, as we conveyed " I'm not sure an attacker can force the SessionDB to fail to initialize, so I think this can only apply to users who have corrupted databases for some other reason". 
and you conveyed 
>>>As for the corrupted SessionDB database, I think it only change the scope of the impacted users
>>> this demonstrates that the corrupted database precondition only affect the scope of impacted users. This precondition is not rare for users, 

The ability to leverage this bug against a victim use is mitigated by requiring the precondition of the corrupted database or a failed initialization of the SessionDB database. The attacker would have to find and leverage the a SessionDB database bug that results in this corruption. The ability to leverage this bug in a full chain attack is mitigated by the precondition required to trigger and exploit this UAF. 

In terms of the race, this is a documented mitigation in the Chrome VRP policies: 
"Moderately mitigated: Security bug with multiple mitigations; e.g. a malicious extension and two or fewer user interactions or winning a race condition"

>>>As for the racing, since the thread pool could be blocked easily by the compromised renderer, the racing could be easily achieved in the actual scenario. (e.g., open the multiple PoC at the same time).
This is still considered a mitigation, as the attacker would have to convince or frame the attack in such a way that the user would be easily convinced to reliably open the same version of the malicious web content over and over again at the same time.  This not something most users would expect to do in the normal web browsing - open multiple versions of the same web content at the same time- and is very much considered a mitigation. This is something that even done via an extension, would be very visible to the user and they could opt out of. 

In terms of this being executed by a malicious extension, that is also a mitigation. The user must be delivered and be convinced to install the extension, a mitigation from a fully remote exploitable bug and is also a documented mitigation in the Chrome VRP policies. 
"Not mitigated, i.e. does not require user interaction, installing an extension, or being triggered by browser shutdown, or profile destruction. Please see the 'Reward Amounts for Mitigated Security Bugs' section below for specific reward amounts and details."

I hope this helps explain why we consider these aspects mitigations and overall why we consider this bug to be highly mitigated. 


### ha...@gmail.com (2022-12-03)

Thanks very much for the detailed explanation. That make sense and I agree with that this is indeed hightly mitigated. Thanks you very much :)

### am...@chromium.org (2022-12-05)

Of course and you're very welcome - always happy to answer questions and provide insight into security decisions/judgements! 

### am...@google.com (2022-12-05)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-01-09)

[Empty comment from Monorail migration]

### am...@google.com (2023-01-10)

[Empty comment from Monorail migration]

### pg...@google.com (2023-01-10)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1385709?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061782)*
