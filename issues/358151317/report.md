# heap-use-after-free on [PriceNotificationsPriceTrackingMediator navigateToWebpageForURL]

| Field | Value |
|-------|-------|
| **Issue ID** | [358151317](https://issues.chromium.org/issues/358151317) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Mobile |
| **Platforms** | iOS |
| **Chrome Version** | 127.0.0.0 |
| **Reporter** | li...@gmail.com |
| **Assignee** | da...@google.com |
| **Created** | 2024-08-08 |
| **Bounty** | $5,000.00 |

## Description

# Steps to reproduce the problem

repro:

1. apply patch
2. host poc8.html and navigate to <https://www.baidu.com>
3. click ... and click Price Track feature. wait site close then choice item.

# Problem Description

0. As a property of `PriceNotificationsPriceTrackingMediator`, webstate is not monitored, so if `webstate` is destroyed but this member is called, UAF will occur.

```
@interface PriceNotificationsPriceTrackingMediator () {
  // The service responsible for fetching a product's image data.
  std::unique_ptr<image_fetcher::ImageDataFetcher> _imageFetcher;
}
// The service responsible for interacting with commerce's price data
// infrastructure.
@property(nonatomic, assign) commerce::ShoppingService* shoppingService;
// The service responsible for managing bookmarks.
@property(nonatomic, readonly) bookmarks::BookmarkModel* bookmarkModel;
// The current browser state's webstate.
@property(nonatomic, assign) web::WebState* webState; // 
// The product data for the product contained on the site the user is currently
// viewing.
@property(nonatomic, assign) std::optional<commerce::ProductInfo>
    currentSiteProductInfo;
// The service responsible for updating the user's chrome-level push
// notification permissions for Price Tracking.
@property(nonatomic, assign) PushNotificationService* pushNotificationService;

@end

```

1. There is a good example in it. `PriceNotificationsTableViewController` is created in the start of `PriceNotificationsViewCoordinator`, and then calls `presentViewController` to display the view.

```
- (void)start {
  self.tableViewController = [[PriceNotificationsTableViewController alloc]
      initWithStyle:ChromeTableViewStyle()];
  [...]
  self.navigationController = [[TableViewNavigationController alloc]
      initWithTable:self.tableViewController];

  [...]
  [self.baseViewController presentViewController:self.navigationController
                                        animated:YES
                                      completion:nil];

  [super start];
}

```

2. We can call `navigateToWebpageForURL` with the following calling path, and the same is true for `navigateToBookmarks`.

```
    [PriceNotificationsPriceTrackingMediator navigateToWebpageForURL:disposition:]
    [PriceNotificationsPriceTrackingMediator navigateToWebpageForItem:]
    [PriceNotificationsTableViewController tableView:performPrimaryActionForRowAtIndexPath:]

```

3. However, `webState` is called in `navigateToWebpageForURL`. The webstate here is likely to be released, so it will cause UAF.

```
- (void)navigateToWebpageForURL:(const GURL&)URL
                    disposition:(WindowOpenDisposition)disposition {
  self.webState->OpenURL(web::WebState::OpenURLParams(   //<--
      URL, web::Referrer(), disposition, ui::PAGE_TRANSITION_GENERATED,
      /*is_renderer_initiated=*/false));
}
-------------------
- (void)navigateToBookmarks {
  [self.handler hidePriceNotifications];
  GURL URL = _webState->GetLastCommittedURL();
  [self.bookmarksHandler openToExternalBookmark:URL];
}

```

bitset:

1. navigateToBookmarks: introduced in <https://source.chromium.org/chromium/chromium/src/+/204e33bd233f57ac11dd89d20e459baa45eec771> owner is danieltwhite@
2. navigateToWebpageForURL: This vulnerability already existed as early as the navigateToWebpageForItem period. introduced in <https://source.chromium.org/chromium/chromium/src/+/1ed6132349413aba22cccb482200758e8711e864> owner is danieltwhite@
   so best owner is danieltwhite@
   [0]. <https://source.chromium.org/chromium/chromium/src/+/main:ios/chrome/browser/ui/price_notifications/price_notifications_price_tracking_mediator.mm;l=73>
   [1]. <https://source.chromium.org/chromium/chromium/src/+/main:ios/chrome/browser/ui/price_notifications/price_notifications_view_coordinator.mm;l=116?q=self.navigationController%5C%20%3D&ss=chromium%2Fchromium%2Fsrc>
   [3]. <https://source.chromium.org/chromium/chromium/src/+/main:ios/chrome/browser/ui/price_notifications/price_notifications_price_tracking_mediator.mm;l=558?q=navigateToWebpageForURL&ss=chromium%2Fchromium%2Fsrc>

why need patch:
In order to enable the PriceTrack feature, because dev cannot compile gaia and use the account normally, please let me know if there is a way. Then added some traceability to the PriceItem. These do not affect the main logic.

# Summary

heap-use-after-free on [PriceNotificationsPriceTrackingMediator navigateToWebpageForURL]

# Custom Questions

#### Type of crash:

browser

#### Crash state:

see log

# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: N/A

## Attachments

- [uaf9-asan.log](attachments/uaf9-asan.log) (text/plain, 22.1 KB)
- [uaf9.html](attachments/uaf9.html) (text/html, 247 B)
- [uaf9.patch](attachments/uaf9.patch) (text/x-diff, 4.5 KB)
- [showRepro.png](attachments/showRepro.png) (image/png, 317.7 KB)
- deleted (application/octet-stream, 0 B)

## Timeline

### li...@gmail.com (2024-08-08)

fix suggestions: use weakptr for webstate or observe the lifetime of webstate.

### ts...@google.com (2024-08-08)

Similar to prior report, miracleptr status omitted from Asan report, given weak_ptr<> in previous CL, presumably not a security issue.

### li...@gmail.com (2024-08-08)

RE #3
This is the ios architecture. I have not omitted anything because ios does not enable miracles.

### li...@gmail.com (2024-08-08)

redacted

### am...@chromium.org (2024-08-12)

assigning to danieltwhite@ and those involved with <https://crrev.com/c/4226574>
apologies for component noise, there's no good component for this specific issue except the rather broad one of UI>Browser>Mobile
reducing to medium severity due to the UI interaction and the patch, which stipulates a higher set of preconditions to trigger this issue

### pe...@google.com (2024-08-13)

Setting milestone because of s2 severity.

### ap...@google.com (2024-08-20)

Project: chromium/src
Branch: main

commit cd3f94134c1a26eab5eb2e2cb1c324b5e66c76cc
Author: Daniel White <danieltwhite@google.com>
Date:   Tue Aug 20 15:14:14 2024

    [iOS] Addressed Use-after-free in Price Tracking UI
    
    In this CL, the PriceNotificationsPriceTrackingMediator retention of the
    WebState object was replaced with a WeakPtr that stores the WebState
    object. This addresses the security issue identified by the attached bug.
    
    Fixed: b/358151317
    Change-Id: I3ab44e760c096f4311b9070f7ae319ac6622b137
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5786899
    Code-Coverage: findit-for-me@appspot.gserviceaccount.com <findit-for-me@appspot.gserviceaccount.com>
    Commit-Queue: Daniel White <danieltwhite@google.com>
    Reviewed-by: Sylvain Defresne <sdefresne@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1344154}

M       ios/chrome/browser/price_insights/coordinator/price_insights_modulator.mm
M       ios/chrome/browser/ui/price_notifications/price_notifications_price_tracking_mediator.h
M       ios/chrome/browser/ui/price_notifications/price_notifications_price_tracking_mediator.mm
M       ios/chrome/browser/ui/price_notifications/price_notifications_price_tracking_mediator_unittest.mm
M       ios/chrome/browser/ui/price_notifications/price_notifications_view_coordinator.mm

https://chromium-review.googlesource.com/5786899


### sp...@google.com (2024-09-12)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $5000.00 for this report.

Rationale for this decision:
$4,000 for report of moderately mitigated memory corruption in a sandboxed process + $1,000 bisect bonus


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-09-13)

Congratulation lime! Thank you for your efforts and reporting this issue to us!

### pe...@google.com (2024-11-27)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/358151317)*
