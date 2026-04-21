# Security: UAF in GuestViewBase::StopTrackingEmbedderZoomLevel

| Field | Value |
|-------|-------|
| **Issue ID** | [40062221](https://issues.chromium.org/issues/40062221) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>Apps>BrowserTag |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ss...@gmail.com |
| **Assignee** | mc...@chromium.org |
| **Created** | 2022-12-14 |
| **Bounty** | $7,000.00 |

## Description

**VULNERABILITY DETAILS**

In the constructor of `GuestViewBase`[1], a raw\_ptr of `WebContents` is stored to its `owner_web_contents_`, which will be protected after the initialization completes[2].

`AppViewGuest` is one of the derived class of `GuestViewBase`, when we create a `<appview>` tag element and connect to other Chrome App, it will call `CreateGuestAndTransferOwnership` and create a new `GuestViewBase`[3].

```
void GuestViewManager::CreateGuestAndTransferOwnership(  
    const std::string& view_type,  
    content::WebContents\* owner_web_contents,  
    const base::Value::Dict& create_params,  
    OwnedGuestCreatedCallback callback) {  
  std::unique_ptr<GuestViewBase> guest =  
      CreateGuestInternal(owner_web_contents, view_type);  
  if (!guest) {  
    std::move(callback).Run(nullptr);  
    return;  
  }  
  auto\* raw_guest = guest.get();  
  raw_guest->Init(std::move(guest), create_params, std::move(callback));  
}  

```

After that it will start the initialization. In the `AppViewGuest::CreateWebContents` function, there is a path[4] that pends the initialization task and do it asynchronously. Note that `owner_web_contents_` is not protected until the initialization is complete, so if we close the window before the pending initialization task been executed, the freed `owner_web_contents_` will not be cleared, eventually causing use-after-free[5].

[1] <https://source.chromium.org/chromium/chromium/src/+/main:components/guest_view/browser/guest_view_base.cc;l=133;drc=38321ee39cd73ac2d9d4400c56b90613dee5fe29>

[2] <https://source.chromium.org/chromium/chromium/src/+/main:components/guest_view/browser/guest_view_base.cc;l=190;drc=38321ee39cd73ac2d9d4400c56b90613dee5fe29>

[3] <https://source.chromium.org/chromium/chromium/src/+/main:components/guest_view/browser/guest_view_manager.cc;l=180;drc=38321ee39cd73ac2d9d4400c56b90613dee5fe29>

[4] <https://source.chromium.org/chromium/chromium/src/+/main:extensions/browser/guest_view/app_view/app_view_guest.cc;l=208;drc=38321ee39cd73ac2d9d4400c56b90613dee5fe29>

[5] <https://source.chromium.org/chromium/chromium/src/+/main:components/guest_view/browser/guest_view_base.cc;l=843;drc=38321ee39cd73ac2d9d4400c56b90613dee5fe29>

**VERSION**

Operating System: Ubuntu 22.04  

Commit Id: [dev] 24d57d9242befaad23201aa42a40a7f4502f1254

**REPRODUCTION CASE**

To reproduce:

AppView needs to connect to any other Chrome App, so we need to add one other app first. We use the Camera App in our PoC.

1. install the Camera App at <https://chrome.google.com/webstore/detail/camera/hfhhnacclhffhdffklopdkcgdhifgngh>
2. download `background.js` and `manifest.json`
3. ./chrome --load-extension=/path/to/ext

Note that if you want to reproduce the ASAN log, please turn off the DCHECK.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: browser  

Crash State: see `asan.log`

**CREDIT INFORMATION**  

Reporter credit: avaue at S.S.L

## Attachments

- [asan.log](attachments/asan.log) (text/plain, 48.0 KB)
- [manifest.json](attachments/manifest.json) (text/plain, 249 B)
- [background.js](attachments/background.js) (text/plain, 205 B)
- [asan.log](attachments/asan.log) (text/plain, 40.0 KB)

## Timeline

### [Deleted User] (2022-12-14)

[Empty comment from Monorail migration]

### aj...@google.com (2022-12-14)

Hi - which DCHECKs is this hitting if they are enabled?

### aj...@google.com (2022-12-14)

Thanks this repros on Windows HEAD.

Note to developers - you will need a signed-in user to be able to install the Camera app.



### aj...@google.com (2022-12-14)

-> mcnee@chromium based on https://chromium-review.googlesource.com/c/chromium/src/+/3784297

-> Medium as this would be High but requires an extension and a particular app to be installed and a race.
-> FoundIn-108 based on commit above
-> OSes based on needing apps/extensions

[Monorail components: Platform>Apps>BrowserTag]

### aj...@google.com (2022-12-14)

-> lazyboy as mcnee is OOO

### [Deleted User] (2022-12-14)

[Empty comment from Monorail migration]

### ss...@gmail.com (2022-12-15)

Re #4> "Medium as this would be High but requires an extension and a particular app to be installed and a race."

Note that we don't need a particular app installed, any Chrome App in Chrome Web Store can be used to trigger the UAF.

The Camera App is used for a more convenient reproduction. Without the known app id, the attack may use some interfaces like `chrome.management.getAll`[1] to get all installed apps in Chrome.

[1] https://developer.chrome.com/docs/extensions/reference/management/#method-getAll

### [Deleted User] (2022-12-15)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-12-15)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-12-28)

lazyboy: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mc...@chromium.org (2023-01-03)

I'm back from OOO, so I can take this back.

### mc...@chromium.org (2023-01-03)

[Empty comment from Monorail migration]

### mc...@chromium.org (2023-01-05)

Yeah, we need to create the OwnerContentsObserver immediately, instead of after guest initialization, to be able to observe the destruction of the owner in this case.

And indeed, it looks like https://chromium-review.googlesource.com/c/chromium/src/+/3784297 is what regressed this.

### mc...@chromium.org (2023-01-05)

While writing tests for this I discovered the following: If the app to embed allows the request, that will also lead to a UAF as we attempt to access the owner [1] when creating the guest contents [2]. The underlying cause of not clearing the owner pointer is the same though.

From reading the old code, I suspect this allow case would have been an issue before my CL. For the deny case, the old code would have left the GuestViewManager in a bad state, but not in terms of memory safety.

[1] https://source.chromium.org/chromium/chromium/src/+/main:content/browser/browser_plugin/browser_plugin_guest.cc;drc=b8524150039182faf7988e9478a9eff89728ac03;l=37
[2] https://source.chromium.org/chromium/chromium/src/+/main:extensions/browser/guest_view/app_view/app_view_guest.cc;drc=b8524150039182faf7988e9478a9eff89728ac03;l=261

### gi...@appspot.gserviceaccount.com (2023-01-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/f29c9094a6153eb6f473b09fc9fb31b5eb744488

commit f29c9094a6153eb6f473b09fc9fb31b5eb744488
Author: Kevin McNee <mcnee@chromium.org>
Date: Tue Jan 10 20:21:20 2023

Ensure a GuestView's owner WebContents' destruction is observed for delayed init

We currently don't start observing a guest's owner's destruction until
after the creation of the guest WebContents. An AppView's guest
WebContents is created asynchronously after the embedding request
completes. If the owner is destroyed while the embedding request is
pending, we go on to access a stale pointer to the owner when the
request completes.

We now start observing the owner immediately, so we clear the owner
pointer when it is destroyed. We also check that the owner still exists
before proceesing with an accepted embedding request.

Bug: 1400841
Change-Id: I52ed4c98df25d5aea908d746900582c0465f01c4
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4140170
Auto-Submit: Kevin McNee <mcnee@chromium.org>
Reviewed-by: James Maclean <wjmaclean@chromium.org>
Commit-Queue: James Maclean <wjmaclean@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1090972}

[modify] https://crrev.com/f29c9094a6153eb6f473b09fc9fb31b5eb744488/chrome/test/data/extensions/platform_apps/app_view/shim/main.js
[modify] https://crrev.com/f29c9094a6153eb6f473b09fc9fb31b5eb744488/components/guest_view/browser/guest_view_base.cc
[modify] https://crrev.com/f29c9094a6153eb6f473b09fc9fb31b5eb744488/chrome/test/data/extensions/platform_apps/app_view/shim/skeleton/main.js
[modify] https://crrev.com/f29c9094a6153eb6f473b09fc9fb31b5eb744488/chrome/browser/apps/guest_view/app_view_browsertest.cc
[modify] https://crrev.com/f29c9094a6153eb6f473b09fc9fb31b5eb744488/extensions/browser/guest_view/app_view/app_view_guest.cc


### mc...@chromium.org (2023-01-10)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-11)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-11)

[Empty comment from Monorail migration]

### mc...@chromium.org (2023-01-12)

I see that sheriffbot didn't automatically request merges, but I assume we'd at least want this for M110, so adding that now.

Security team: Would you like merges to any earlier releases?

### [Deleted User] (2023-01-12)

Merge review required: M110 is already shipping to beta.

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
Owners: govind (Android), harrysouders (iOS), ceb (ChromeOS), danielyip (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mc...@chromium.org (2023-01-12)

1. Fixes a security issue.
2. https://chromium-review.googlesource.com/c/chromium/src/+/4140170
3. This is in a canary release, without issue. I tested with the automated tests introduced in that CL.
4. No
5. N/A
6. Automated tests should be enough.

### da...@google.com (2023-01-17)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-01-17)

Hi Kevin, thanks for your work on this issue and also tagging it to get into the merge view queue. I'd like to also get this backmerged to Stable/109, which means also to Extended/108. Please let me know if there's any potential issues with this. 
M110 merge approved, please merge to branch 5481
M109 merge approved, please merge to branch 5414 
m108 merge approved, please merge to branch 5359 
Please merge to these release branches at your earliest convenience and before this Friday, 10am Pacific, so this fix can be included in next week's m109/stable and m108/extended security respins. 

### mc...@chromium.org (2023-01-18)

Merge CLs:
https://chromium-review.googlesource.com/c/chromium/src/+/4178430
https://chromium-review.googlesource.com/c/chromium/src/+/4178431
https://chromium-review.googlesource.com/c/chromium/src/+/4178470

### gi...@appspot.gserviceaccount.com (2023-01-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/33f26ff5c42ad9ef117cd416bdee47c4444cdd88

commit 33f26ff5c42ad9ef117cd416bdee47c4444cdd88
Author: Kevin McNee <mcnee@chromium.org>
Date: Wed Jan 18 17:32:53 2023

M109: Ensure a GuestView's owner WebContents' destruction is observed for delayed init

Ensure a GuestView's owner WebContents' destruction is observed for delayed init

We currently don't start observing a guest's owner's destruction until
after the creation of the guest WebContents. An AppView's guest
WebContents is created asynchronously after the embedding request
completes. If the owner is destroyed while the embedding request is
pending, we go on to access a stale pointer to the owner when the
request completes.

We now start observing the owner immediately, so we clear the owner
pointer when it is destroyed. We also check that the owner still exists
before proceesing with an accepted embedding request.

(cherry picked from commit f29c9094a6153eb6f473b09fc9fb31b5eb744488)

Bug: 1400841
Change-Id: I52ed4c98df25d5aea908d746900582c0465f01c4
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4140170
Auto-Submit: Kevin McNee <mcnee@chromium.org>
Reviewed-by: James Maclean <wjmaclean@chromium.org>
Commit-Queue: James Maclean <wjmaclean@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1090972}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4178431
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/5414@{#1407}
Cr-Branched-From: 4417ee59d7bf6df7a9c9ea28f7722d2ee6203413-refs/heads/main@{#1070088}

[modify] https://crrev.com/33f26ff5c42ad9ef117cd416bdee47c4444cdd88/chrome/test/data/extensions/platform_apps/app_view/shim/main.js
[modify] https://crrev.com/33f26ff5c42ad9ef117cd416bdee47c4444cdd88/components/guest_view/browser/guest_view_base.cc
[modify] https://crrev.com/33f26ff5c42ad9ef117cd416bdee47c4444cdd88/chrome/test/data/extensions/platform_apps/app_view/shim/skeleton/main.js
[modify] https://crrev.com/33f26ff5c42ad9ef117cd416bdee47c4444cdd88/chrome/browser/apps/guest_view/app_view_browsertest.cc
[modify] https://crrev.com/33f26ff5c42ad9ef117cd416bdee47c4444cdd88/extensions/browser/guest_view/app_view/app_view_guest.cc


### gi...@appspot.gserviceaccount.com (2023-01-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/d08e7e82afbeb1efd8642f3fbc39344b1cde6296

commit d08e7e82afbeb1efd8642f3fbc39344b1cde6296
Author: Kevin McNee <mcnee@chromium.org>
Date: Wed Jan 18 18:07:18 2023

M110: Ensure a GuestView's owner WebContents' destruction is observed for delayed init

Ensure a GuestView's owner WebContents' destruction is observed for delayed init

We currently don't start observing a guest's owner's destruction until
after the creation of the guest WebContents. An AppView's guest
WebContents is created asynchronously after the embedding request
completes. If the owner is destroyed while the embedding request is
pending, we go on to access a stale pointer to the owner when the
request completes.

We now start observing the owner immediately, so we clear the owner
pointer when it is destroyed. We also check that the owner still exists
before proceesing with an accepted embedding request.

(cherry picked from commit f29c9094a6153eb6f473b09fc9fb31b5eb744488)

Bug: 1400841
Change-Id: I52ed4c98df25d5aea908d746900582c0465f01c4
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4140170
Auto-Submit: Kevin McNee <mcnee@chromium.org>
Reviewed-by: James Maclean <wjmaclean@chromium.org>
Commit-Queue: James Maclean <wjmaclean@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1090972}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4178430
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/5481@{#430}
Cr-Branched-From: 130f3e4d850f4bc7387cfb8d08aa993d288a67a9-refs/heads/main@{#1084008}

[modify] https://crrev.com/d08e7e82afbeb1efd8642f3fbc39344b1cde6296/chrome/test/data/extensions/platform_apps/app_view/shim/main.js
[modify] https://crrev.com/d08e7e82afbeb1efd8642f3fbc39344b1cde6296/components/guest_view/browser/guest_view_base.cc
[modify] https://crrev.com/d08e7e82afbeb1efd8642f3fbc39344b1cde6296/chrome/test/data/extensions/platform_apps/app_view/shim/skeleton/main.js
[modify] https://crrev.com/d08e7e82afbeb1efd8642f3fbc39344b1cde6296/chrome/browser/apps/guest_view/app_view_browsertest.cc
[modify] https://crrev.com/d08e7e82afbeb1efd8642f3fbc39344b1cde6296/extensions/browser/guest_view/app_view/app_view_guest.cc


### gi...@appspot.gserviceaccount.com (2023-01-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/9cb60016348ce409d74fc2dc5bf78a49de61d985

commit 9cb60016348ce409d74fc2dc5bf78a49de61d985
Author: Kevin McNee <mcnee@chromium.org>
Date: Wed Jan 18 18:24:22 2023

M108: Ensure a GuestView's owner WebContents' destruction is observed for delayed init

Ensure a GuestView's owner WebContents' destruction is observed for delayed init

We currently don't start observing a guest's owner's destruction until
after the creation of the guest WebContents. An AppView's guest
WebContents is created asynchronously after the embedding request
completes. If the owner is destroyed while the embedding request is
pending, we go on to access a stale pointer to the owner when the
request completes.

We now start observing the owner immediately, so we clear the owner
pointer when it is destroyed. We also check that the owner still exists
before proceesing with an accepted embedding request.

(cherry picked from commit f29c9094a6153eb6f473b09fc9fb31b5eb744488)

Bug: 1400841
Change-Id: I52ed4c98df25d5aea908d746900582c0465f01c4
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4140170
Auto-Submit: Kevin McNee <mcnee@chromium.org>
Reviewed-by: James Maclean <wjmaclean@chromium.org>
Commit-Queue: James Maclean <wjmaclean@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1090972}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4178470
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/5359@{#1349}
Cr-Branched-From: 27d3765d341b09369006d030f83f582a29eb57ae-refs/heads/main@{#1058933}

[modify] https://crrev.com/9cb60016348ce409d74fc2dc5bf78a49de61d985/chrome/test/data/extensions/platform_apps/app_view/shim/main.js
[modify] https://crrev.com/9cb60016348ce409d74fc2dc5bf78a49de61d985/components/guest_view/browser/guest_view_base.cc
[modify] https://crrev.com/9cb60016348ce409d74fc2dc5bf78a49de61d985/chrome/test/data/extensions/platform_apps/app_view/shim/skeleton/main.js
[modify] https://crrev.com/9cb60016348ce409d74fc2dc5bf78a49de61d985/chrome/browser/apps/guest_view/app_view_browsertest.cc
[modify] https://crrev.com/9cb60016348ce409d74fc2dc5bf78a49de61d985/extensions/browser/guest_view/app_view/app_view_guest.cc


### am...@chromium.org (2023-01-24)

[Empty comment from Monorail migration]

### am...@google.com (2023-01-24)

[Empty comment from Monorail migration]

### am...@google.com (2023-01-24)

[Empty comment from Monorail migration]

### am...@google.com (2023-01-26)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-01-26)

Congratulations, avaue! The VRP Panel has decided to award you $7,000 for this report of a mildly mitigated security bug. Thank you for your efforts and reporting this issue to us -- nice work! 

### am...@google.com (2023-01-28)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-20)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1400841?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062221)*
