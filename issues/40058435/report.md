# Security: heap-use-after-use in DiscountURLLoader::NavigateToDiscountURL

| Field | Value |
|-------|-------|
| **Issue ID** | [40058435](https://issues.chromium.org/issues/40058435) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Shopping>Cart |
| **Platforms** | Linux, Mac, Windows |
| **Reporter** | yu...@gmail.com |
| **Assignee** | yu...@chromium.org |
| **Created** | 2022-01-08 |
| **Bounty** | $16,000.00 |

## Description

**VULNERABILITY DETAILS**  

If we login a user and visit a url match cart rules, CartService will be created for the profile. When CartService construct, |cart\_db\_| initializing and so is the ProfileProtoDB instance |cart\_db\_->proto\_db\_|. The initialization of ProfileProtoDB is an async task run on background thread and will post ProfileProtoDB::OnDatabaseInitialized task to UI thread when it finished. Before ProfileProtoDB initialized, all queries to it will be stored in |deferred\_operations\_| and deferred running in OnDatabaseInitialized.

DiscountURLLoader::TabChangedAt has a callchain like |CartService::GetDiscountURL => CartService::LoadCart => CartDB::LoadCart => ProfileProtoDB<T>::LoadOneEntry|, if this happened before |cart\_db\_| initialized, callback binds with raw WebContents pointer will be stored. The WebContents could be destoryed before the callback run, UaF triggered in DiscountURLLoader::NavigateToDiscountURL.

<https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/persisted_state_db/profile_proto_db.h;drc=ce55a875516951f56c738b4527eb17ec9de7b6b1;l=383>  

<https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/persisted_state_db/profile_proto_db.h;drc=ce55a875516951f56c738b4527eb17ec9de7b6b1;l=393>

<https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/cart/discount_url_loader.cc;l=41>  

void DiscountURLLoader::TabChangedAt(content::WebContents\* contents,  

int index,  

TabChangeType change\_type) {  

...  

if (last\_interacted\_url\_ == contents->GetVisibleURL()) {  

cart\_service\_->GetDiscountURL(  

contents->GetVisibleURL(),  

base::BindOnce(&DiscountURLLoader::NavigateToDiscountURL,  

weak\_ptr\_factory\_.GetWeakPtr(), contents)); // callback bind with raw WebContents ptr  

}  

...  

}

<https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/persisted_state_db/profile_proto_db.h;drc=ce55a875516951f56c738b4527eb17ec9de7b6b1;l=180>  

void ProfileProtoDB<T>::LoadOneEntry(const std::string& key,  

LoadCallback callback) {  

if (InitStatusUnknown()) { // if db is still initializing, callback be stored in |deferred\_operations\_|  

deferred\_operations\_.push\_back(base::BindOnce(  

&ProfileProtoDB::LoadOneEntry, weak\_ptr\_factory\_.GetWeakPtr(), key,  

std::move(callback)));  

} else if (FailedToInit()) {  

...  

}

<https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/cart/discount_url_loader.cc;l=57>  

void DiscountURLLoader::NavigateToDiscountURL(content::WebContents\* contents,  

const GURL& discount\_url) {  

contents->GetController().LoadURL(discount\_url, content::Referrer(), // raw WebContents ptr use here may trigger UaF  

ui::PAGE\_TRANSITION\_FIRST, std::string());  

}

Fix suggestions:

1. use weakptr or observe the webcontents
2. dynamic get webcontents in callback again

**VERSION**  

Chrome Version: stable (according to source code)  

Operating System: except Android (CartServcie not work on android)

**REPRODUCTION CASE**  

I am not familiar with cart module and still investigating it. The steps below is analysed from source code.

1. Enable cart and discount features in chrome and login a user. (I am still confused about these cart and discount rules)
2. Prepare a large profile database or try slowly IO. (lengthen cart database initialize time)
3. Visit a ruled url like '<https://www.nike.com/cart>' (contruct CartService)
4. Trigger CartService::PrepareForNavigation through action or Mojo call (construct DiscountURLLoader instance in CartService and set |last\_interacted\_url\_|)
5. Refresh tab (trigger DiscountURLLoader::TabChangedAt with TabChangeType::kAll) and close it. (destory the WebContents,)
6. UaF may trigger soon. (cart database initialized and run callbacks)

Even there are lots of limits to trigger the bug, the race condition problem may could be triggerred by Mojo and lead to sandbox escape.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: browser

**CREDIT INFORMATION**  

Reporter credit: Wei Yuan(@vo\_sec) of MoyunSec VLab

## Timeline

### [Deleted User] (2022-01-08)

[Empty comment from Monorail migration]

### dr...@chromium.org (2022-01-10)

It would be great if you could get some kind of reliable reproduction steps, but for now CC'ing a code owner to see whether they think this is plausible.

[Monorail components: UI>Browser>Shopping>Cart]

### aj...@google.com (2022-01-18)

wychen: ptal - it would be good to know if these features currently enabled (in M97 or later?) - if you are not the right person to investigate please assign to someone else - thanks.


### [Deleted User] (2022-01-18)

[Empty comment from Monorail migration]

### yu...@chromium.org (2022-01-18)

Thanks for filing! This is a great catch. I can take this one as I wrote that part of code.

### [Deleted User] (2022-01-19)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-19)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-02-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/5b399d63e31334d6d61125f039907a0c5d358a50

commit 5b399d63e31334d6d61125f039907a0c5d358a50
Author: Yue Zhang <yuezhanggg@chromium.org>
Date: Tue Feb 01 18:05:45 2022

[RBD] Fix potential use-after-destroy of WebContents

Bug: 1285601
Change-Id: I7ed33e13189a024946bfad9ef9ec58f2d777b60f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3402408
Reviewed-by: Wei-Yin Chen <wychen@chromium.org>
Commit-Queue: Yue Zhang <yuezhanggg@chromium.org>
Cr-Commit-Position: refs/heads/main@{#965763}

[modify] https://crrev.com/5b399d63e31334d6d61125f039907a0c5d358a50/chrome/browser/cart/discount_url_loader.cc
[modify] https://crrev.com/5b399d63e31334d6d61125f039907a0c5d358a50/chrome/browser/cart/discount_url_loader.h


### [Deleted User] (2022-02-01)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-02)

yuezhanggg: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### yu...@chromium.org (2022-02-02)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-02)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-02)

[Empty comment from Monorail migration]

### am...@google.com (2022-02-23)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-02-23)

Congratulations -- the VRP Panel has decided to award you $16,000 for this report. Thank you for your efforts and nice work! 

### am...@google.com (2022-02-26)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-03-28)

[Empty comment from Monorail migration]

### am...@google.com (2022-03-29)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-11)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2022-07-22)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-29)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1285601?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058435)*
