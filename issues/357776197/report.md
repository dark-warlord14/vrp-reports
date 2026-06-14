# heap-use-after-free on [ParcelTrackingOptInMediator didTapAlwaysTrack]

| Field | Value |
|-------|-------|
| **Issue ID** | [357776197](https://issues.chromium.org/issues/357776197) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>ParcelTracking |
| **Platforms** | iOS |
| **Chrome Version** | 127.0.0.0 |
| **Reporter** | li...@gmail.com |
| **Assignee** | sm...@chromium.org |
| **Created** | 2024-08-06 |
| **Bounty** | $2,000.00 |

## Description

# Steps to reproduce the problem

repro:

1. apply the patch.
2. host the uaf8.html
3. wait for display the view then wait for site close, click AlwaysTrack and allow button.

# Problem Description

0. There is a raw pointer in the marked area that has not been observed, so there is a risk of UAF.

```
@implementation ParcelTrackingOptInCoordinator {
  raw_ptr<web::WebState> _webState;  // <--- raw_ptr
  NSArray<CustomTextCheckingResult*>* _parcels;
  ParcelTrackingOptInMediator* _mediator;
  ParcelTrackingOptInViewController* _viewController;
}


```

1. Then, in the `start` method of `ParcelTrackingOptInCoordinator`, it is passed to `ParcelTrackingOptInMediator`, and then the `presentViewController` is called to display the view.

```
- (void)start {
  [super start];
  _mediator = [[ParcelTrackingOptInMediator alloc] initWithWebState:_webState]; // 
  _mediator.parcelTrackingCommandsHandler = HandlerForProtocol(
      self.browser->GetCommandDispatcher(), ParcelTrackingOptInCommands);
  _viewController = [[ParcelTrackingOptInViewController alloc] init];
  _viewController.actionHandler = _viewController;
  _viewController.delegate = self;
  _viewController.presentationController.delegate = self;
  [self.baseViewController presentViewController:_viewController
                                        animated:YES
                                      completion:nil];
  base::UmaHistogramBoolean(parcel_tracking::kOptInPromptDisplayedHistogramName,
                            true);
}

```

2. Then, in the logic of the `AlwaysTrack` button in its view, once the user selects the `alwaysTrack` option and confirms, its `didTapAlwayTrack` method will be called. However, if the webState is released while the view is displayed, the marked area `_webState` becomes a hanging pointer. This leads to UAF.

```
- (void)didTapAlwaysTrack:(NSArray<CustomTextCheckingResult*>*)parcelList {
  commerce::ShoppingService* shoppingService =
      commerce::ShoppingServiceFactory::GetForBrowserState(
          _webState->GetBrowserState()); //！
  TrackParcels(shoppingService, parcelList, std::string(),
               _parcelTrackingCommandsHandler, true,
               TrackingSource::kAutoTrack);
}

```

[0]. <https://source.chromium.org/chromium/chromium/src/+/main:ios/chrome/browser/ui/parcel_tracking/parcel_tracking_opt_in_coordinator.mm;l=26;drc=c55c4a4997144a5ff358f3271f5a304dd1eff57d>
[1]. <https://source.chromium.org/chromium/chromium/src/+/main:ios/chrome/browser/ui/parcel_tracking/parcel_tracking_opt_in_coordinator.mm;l=47;drc=41374c974d98f8cf67134f9ddb8d96d398154dfe;bpv=1;bpt=1>
[2]. <https://source.chromium.org/chromium/chromium/src/+/main:ios/chrome/browser/ui/parcel_tracking/parcel_tracking_opt_in_mediator.mm;l=30;drc=41374c974d98f8cf67134f9ddb8d96d398154dfe;bpv=0;bpt=1>

bitset:
<https://source.chromium.org/chromium/chromium/src/+/f50e47b4284bf099f85c1dd3903d7d372877b1e9>

owner is hiramahmood@。

Notice: why need patch?
Because the function requires user login and adding packages, the role of the patch is to add packages that need to be tracked, and then the patch drops the branch that verifies whether to login.

fix suggestions:
use weakptr for webstate or observe the lifetime of webstate.

# Summary

heap-use-after-free on [ParcelTrackingOptInMediator didTapAlwaysTrack]

# Custom Questions

#### Type of crash:

browser

#### Crash state:

see asan.log

# Additional Data

Category: Security   

Chrome Channel: Stable   

Regression: N/A

## Attachments

- [uaf8-asan.log](attachments/uaf8-asan.log) (text/plain, 49.9 KB)
- [uaf8.html](attachments/uaf8.html) (text/html, 248 B)
- [uaf8.patch](attachments/uaf8.patch) (text/x-diff, 3.5 KB)
- [action.png](attachments/action.png) (image/png, 355.5 KB)

## Timeline

### ts...@google.com (2024-08-06)

ios only and requires patch, so automated reproduction not possible, nor do I have an IOS build at present.  Taking Asan trace at face value. Assigning to author of crashing method. Tentatively S1/P1 but ...
Reporter: VRP assessment will be complicated by patch implications. You may increase your chances of any reward by clearly documenting the pre-conditions that need to be met in the wild for this to have any impact. 

### li...@gmail.com (2024-08-06)

RE #2
Nice day !

1. I have made it very clear that users need to have login with **Apple ID**, but I can't build a loginable version of chrome using google api (don't know how to build it)(So I think this should not be a pre-condition, because users who set chrome as the default browser in the production version will login in advance) and another one : **Parcels** that can be tracked. According to the code I read, this can be controlled through the dom and javascript.
2. The view shown in **action.png** will be displayed. You only need to select **AlwaysTrack button** after the site is closed to trigger it. If you have any questions, you can always come to me :)

### th...@google.com (2024-08-06)

I think we just need to assign _webState to nullptr in the mediator's -disconnect to avoid the UAF issue. And a if (!_webState) check in the code in question for good measure.

### ts...@google.com (2024-08-08)

Also, this is a raw_ptr<>, so should be protected by miracleptr, miracleptr status omitted from Asan report, presuming not a security bug.

### li...@gmail.com (2024-08-08)

RE #5:
Also, This is the ios architecture. I have not omitted anything because ios does not enable miracles.

### am...@chromium.org (2024-08-12)

This issue was missing a foundin- / security impact, so I've updated accordingly
Also reduced the severity to medium due to the preconditions to exploitation and the requirement of the patch to navigate those

### pe...@google.com (2024-08-13)

Setting milestone because of s2 severity.

### sm...@chromium.org (2024-08-14)

Ok, I have been able to reproduce. I agree that the patch provided is just to make things easier (I had to patch the code even more to get access to parcel tracking as someone outside the USA!). The actual reproduction for a real user would be:

1. Be logged into Chrome, in the USA
2. Visit a website that contains a detectable tracking number
3. This will trigger the offer-to-track UI
4. While the UI is visible and before the user does anything, the underlying website has to close itself/be closed somehow
5. If the user then selects 'Always Track' and then clicks Continue, then the UAF situation will occur.

For me on a local build of ios (with ios-internal) this crashes in RawPtrBackupRefImpl::SafelyUnwrapPtrForDereference, which has a line of:

```
      PA_BASE_CHECK(IsPointeeAlive(address));  // Detects use-after-free.

```

But I have not checked if this protection is actually present for real users.

Stack:

```
#0	0x000000010d0274c3 in partition_alloc::internal::logging::LogMessage::~LogMessage() at /Users/smcgruer/bling/src/base/allocator/partition_allocator/src/partition_alloc/partition_alloc_base/log_message.cc:129
#1	0x00000001092b2165 in partition_alloc::internal::logging::check_error::Check::~Check() at /Users/smcgruer/bling/src/base/allocator/partition_allocator/src/partition_alloc/partition_alloc_base/check.h:115
#2	0x00000001092b20b5 in partition_alloc::internal::logging::check_error::Check::~Check() at /Users/smcgruer/bling/src/base/allocator/partition_allocator/src/partition_alloc/partition_alloc_base/check.h:115
#3	0x000000010b0f5e41 in web::WebState* base::internal::RawPtrBackupRefImpl<false, false>::SafelyUnwrapPtrForDereference<web::WebState>(web::WebState*) at /Users/smcgruer/bling/src/base/allocator/partition_allocator/src/partition_alloc/pointers/raw_ptr_backup_ref_impl.h:228
#4	0x000000010b0f5ce8 in base::raw_ptr<web::WebState, (partition_alloc::internal::RawPtrTraits)0>::GetForDereference() const at /Users/smcgruer/bling/src/base/allocator/partition_allocator/src/partition_alloc/pointers/raw_ptr.h:1010
#5	0x000000010b0f48e5 in base::raw_ptr<web::WebState, (partition_alloc::internal::RawPtrTraits)0>::operator->() const at /Users/smcgruer/bling/src/base/allocator/partition_allocator/src/partition_alloc/pointers/raw_ptr.h:703
#6	0x000000010c6b7e4a in -[ParcelTrackingOptInMediator didTapAlwaysTrack:] at /Users/smcgruer/bling/src/ios/chrome/browser/parcel_tracking/ui_bundled/parcel_tracking_opt_in_mediator.mm:30
#7	0x000000010c6b76ad in -[ParcelTrackingOptInCoordinator alwaysTrackTapped] at /Users/smcgruer/bling/src/ios/chrome/browser/parcel_tracking/ui_bundled/parcel_tracking_opt_in_coordinator.mm:77
#8	0x000000010c6b8a6b in -[ParcelTrackingOptInViewController confirmationAlertPrimaryAction] at /Users/smcgruer/bling/src/ios/chrome/browser/parcel_tracking/ui_bundled/parcel_tracking_opt_in_view_controller.mm:112
#9	0x000000010bfec65d in -[ConfirmationAlertViewController didTapPrimaryActionButton] at /Users/smcgruer/bling/src/ios/chrome/common/ui/confirmation_alert/confirmation_alert_view_controller.mm:574
#10	0x00007ff805ce5824 in -[UIApplication sendAction:to:from:forEvent:] ()
#11	0x00007ff80535b2c3 in -[UIControl sendAction:to:forEvent:] ()
#12	0x00007ff80535b6b8 in -[UIControl _sendActionsForEvents:withEvent:] ()
#13	0x00007ff80535761f in -[UIButton _sendActionsForEvents:withEvent:] ()
#14	0x00007ff805359e7d in -[UIControl touchesEnded:withEvent:] ()
#15	0x00007ff805d291ca in -[UIWindow _sendTouchesForEvent:] ()
#16	0x00007ff805d2b3ac in -[UIWindow sendEvent:] ()
#17	0x00007ff805d0028e in -[UIApplication sendEvent:] ()
#18	0x00007ff805db102b in __dispatchPreprocessedEventFromEventQueue ()
#19	0x00007ff805db4154 in __processEventQueue ()
#20	0x00007ff805da9d34 in __eventFetcherSourceCallback ()
#21	0x00007ff800429ff3 in __CFRUNLOOP_IS_CALLING_OUT_TO_A_SOURCE0_PERFORM_FUNCTION__ ()
#22	0x00007ff800429f35 in __CFRunLoopDoSource0 ()
#23	0x00007ff800429732 in __CFRunLoopDoSources0 ()
#24	0x00007ff800423e67 in __CFRunLoopRun ()
#25	0x00007ff8004236ed in CFRunLoopRunSpecific ()
#26	0x00007ff8103ba08f in GSEventRunModal ()
#27	0x00007ff805cdf6ee in -[UIApplication _run] ()
#28	0x00007ff805ce416e in UIApplicationMain ()
#29	0x000000010929d46a in (anonymous namespace)::RunUIApplicationMain(int, char**) at /Users/smcgruer/bling/src/ios/chrome/app/chrome_exe_main.mm:63
#30	0x000000010902e7d2 in ChromeMain(int, char**) at /Users/smcgruer/bling/src/ios/chrome/app/chrome_exe_main.mm:117

```

My next step is to investigate the suggested fix above in [comment #4](https://issues.chromium.org/issues/357776197#comment4)

### sm...@chromium.org (2024-08-15)

I have a CL out to thegreenfrog@ to address this, but there's a few points of discussion to have in the review. Hoping to land a fix by early next week at latest.

### ap...@google.com (2024-08-20)

Project: chromium/src
Branch: main

commit b04c04e07aaddc14712e43ec76cab7f637d415dd
Author: Stephen McGruer <smcgruer@chromium.org>
Date:   Tue Aug 20 12:48:52 2024

    [iOS] Pass ShoppingService directly to ParcelTrackingOptInMediator
    
    Previously the controller passed a webState from the coordinator
    down to the mediator, and then later retrieved the ShoppingService
    from it. However per go/bling-fascicle-3-mediators this is incorrect;
    the mediator should receive service specific dependencies directly
    rather than 'backbone' classes.
    
    This also is more correct for the lifecycle of the opt-in dialog;
    it is not tied to the underlying page which can technically go away
    while the dialog is still showing (e.g., if some javascript calls
    window.close()).
    
    Bug: 357776197
    Change-Id: I877af1036f779208f41cfad4ebf0d3395498e5fc
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5788248
    Reviewed-by: Gauthier Ambard <gambard@chromium.org>
    Code-Coverage: findit-for-me@appspot.gserviceaccount.com <findit-for-me@appspot.gserviceaccount.com>
    Commit-Queue: Stephen McGruer <smcgruer@chromium.org>
    Reviewed-by: Chris Lu <thegreenfrog@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1344091}

M       ios/chrome/browser/browser_view/ui_bundled/browser_coordinator.mm
M       ios/chrome/browser/parcel_tracking/ui_bundled/parcel_tracking_opt_in_coordinator.h
M       ios/chrome/browser/parcel_tracking/ui_bundled/parcel_tracking_opt_in_coordinator.mm
M       ios/chrome/browser/parcel_tracking/ui_bundled/parcel_tracking_opt_in_coordinator_unittest.mm
M       ios/chrome/browser/parcel_tracking/ui_bundled/parcel_tracking_opt_in_mediator.h
M       ios/chrome/browser/parcel_tracking/ui_bundled/parcel_tracking_opt_in_mediator.mm
M       ios/chrome/browser/parcel_tracking/ui_bundled/parcel_tracking_opt_in_view_controller_delegate.h

https://chromium-review.googlesource.com/5788248


### sp...@google.com (2024-08-28)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
$1,000 for report of highly mitigated security bug + $1,000 bisect bonus


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-08-29)

Congratulations lime! Thank you for your efforts and reporting this issue to us.

### pe...@google.com (2024-11-27)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/357776197)*
