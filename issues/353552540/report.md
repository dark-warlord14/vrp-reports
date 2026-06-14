# AddressSanitizer: heap-use-after-free on [SharingCoordinator start]

| Field | Value |
|-------|-------|
| **Issue ID** | [353552540](https://issues.chromium.org/issues/353552540) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>Sharing |
| **Platforms** | iOS |
| **Chrome Version** | 126.0.0.0 |
| **Reporter** | li...@gmail.com |
| **Assignee** | sd...@google.com |
| **Created** | 2024-07-17 |
| **Bounty** | $11,000.00 |

## Description

# Steps to reproduce the problem

repro:
1. apply patch.diff which simplify trigger。
2. run poc.html then click the share button

# Problem Description

0. `ThreadPool::PostTaskAndReplyWithResult` in the `start` function passes `currentWebState` as a parameter, but this Objc class is controlled by ARC. So his two life cycles may not be consistent.

```
- (void)start {
  web::WebState* currentWebState =
      self.browser->GetWebStateList()->GetActiveWebState();
  if (currentWebState &&
      ShareFileDownloadTabHelper::ShouldDownload(currentWebState)) {
    // Creating the directory can block the main thread, so perform it on a
    // background sequence, then on current sequence complete the workflow.
    __weak SharingCoordinator* weakSelf = self;
    base::ThreadPool::PostTaskAndReplyWithResult(
        FROM_HERE, {base::TaskPriority::USER_VISIBLE, base::MayBlock()},
        base::BindOnce(&CreateDestinationDirectoryAndRemoveObsoleteFiles),
        base::BindOnce(^(BOOL directoryCreated) {
          [weakSelf startDownloadWithExistingDirectory:directoryCreated
                                              webState:currentWebState]; // <-- here pass the webState 
        }));
  } else {
    [self startActivityService];
  }
}

```

1. In fact, it is. If `WebState` is destroyed before this Reply is run, UAF will result. This is where use comes in.

- 1.1
  ```
  - (void)start {
  id<ShareDownloadOverlayCommands> handler = HandlerForProtocol(
      self.browser->GetCommandDispatcher(), ShareDownloadOverlayCommands);
  self.viewController = [[ShareDownloadOverlayViewController alloc]
      initWithBaseView:_webState->GetView() //<---- use here
              handler:handler];
  
  UIView* overlayedView = self.viewController.view;
  [UIView animateWithDuration:kOverlayViewAnimationDuration
                  animations:^{
                      [overlayedView setAlpha:1.0];
                  }];
  }
  
  ```
- 1.2

```
- (void)startDownloadFromWebState:(web::WebState*)webState {
  self.isDownloadCanceled = NO;
  NSString* tempDirPath = GetTemporaryDocumentDirectory();
  ShareFileDownloadTabHelper* helper =
      ShareFileDownloadTabHelper::FromWebState(webState); // use here
  self.filePath = [tempDirPath
      stringByAppendingPathComponent:base::SysUTF16ToNSString(
                                         helper->GetFileNameSuggestion())];
  self.fileNSURL = [NSURL fileURLWithPath:self.filePath];

      __weak SharingCoordinator* weakSelf = self;
      webState->DownloadCurrentPage(self.filePath, self,  // use here
                                    ^(id<CRWWebViewDownload> download) {
                                      weakSelf.download = download;
                                    });
}

```

- [0]. <https://source.chromium.org/chromium/chromium/src/+/main:ios/chrome/browser/ui/sharing/sharing_coordinator.mm;l=212;drc=34ad7f3844f882baf3d31a6bc6e300acaa0e3fc8;bpv=0;bpt=1>
- [1.1]. <https://source.chromium.org/chromium/chromium/src/+/main:ios/chrome/browser/ui/sharing/share_download_overlay_coordinator.mm;l=47;bpv=0;bpt=1>
- [1.2]. <https://source.chromium.org/chromium/chromium/src/+/main:ios/chrome/browser/ui/sharing/sharing_coordinator.mm;l=308;drc=34ad7f3844f882baf3d31a6bc6e300acaa0e3fc8;bpv=0;bpt=1>

fix suggestions:
Since `webstate` is used in many places, I think it is better to use weakptr not add a WebStateDestory observer to the class. Because I only saw the initialization of \_webState and did not see any zeroing operation.

```
@interface ShareDownloadOverlayCoordinator () {
 // Web state that will receive the overlay view.
 raw_ptr<web::WebState> _webState;
}

```

bitset:

1. Although \_webState is not set to 0 here, I think the key to this problem is still in use, so I pointed the bitset to <https://source.chromium.org/chromium/chromium/src/+/0ee2fb6db0754b2579419265bb64dbc4463410c3>
2. This will be introduced in October 2022 at the earliest.

*NOTE*

1. The reason why patch is needed is to simplify my trigger operation, because there are many components that use this function (see 1.jpg)
2. The root cause of the vulnerability has nothing to do with the path.
3. There's no guarantee that it can't be triggered without a user gesture, since a large number of components use it.

# Summary

AddressSanitizer: heap-use-after-free on [SharingCoordinator start]

# Custom Questions

#### Type of crash:

browser

#### Crash state:

see uaf.log

#### Reporter credit:

lime(@limeSec\_) From TIANGONG Team of Legendsec at QI-ANXIN Group,

# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: N/A

## Attachments

- [1.png](attachments/1.png) (image/png, 466.4 KB)
- [poc.html](attachments/poc.html) (text/html, 218 B)
- [uaf.log](attachments/uaf.log) (text/plain, 63.3 KB)
- [patch.diff](attachments/patch.diff) (text/x-diff, 1.6 KB)
- [example.mov](attachments/example.mov) (video/quicktime, 22.4 MB)
- [fix.patch](attachments/fix.patch) (text/x-diff, 1.1 KB)

## Timeline

### li...@gmail.com (2024-07-17)

1. Because Reply runs on this thread, and multiple functions of `startDownloadWithExistingDirectory` can trigger UAF, so I provide a patch for your reference. This one get a `Weakptr` to cancel the running of Reply, which plays a good role here. see fix.patch
2. And here i upload a trigger video. see example.mov

### dr...@chromium.org (2024-07-17)

[security triage] I don't have an iOS development environment, so I'm trusting the reporter's (reasonable-sounding) claims here. This looks like memory corruption in an unsandboxed process without any user interaction, which is critical severity. I don't think the race is that mitigating, as I expect `CreateDestinationDirectoryAndRemoveObsoleteFiles` to do several interactions with disk, which should leave a reasonable-sized window for closing the new window. marq@ - there's no closer OWNER for sharing\_coordinator.mm, can you take a look?

### pe...@google.com (2024-07-18)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2024-07-18)

Setting Priority to P0 to match Severity s0. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ap...@google.com (2024-07-22)

Project: chromium/src
Branch: main

commit 7f0725c2c6c28395b2132a2fdfc5c354005a72fd
Author: Sylvain Defresne <sdefresne@chromium.org>
Date:   Mon Jul 22 12:55:46 2024

    [ios] Fix blocks in SharingCoordinator
    
    Use helper functions and methods to avoid accidentely capturing
    pointers to C++ objects in blocks. Also use base::WeakPtr<...>
    when capturing pointers to C++ objects to prevent UaF.
    
    Use base::ThreadPool::CreateSequencedTaskRunner() to ensure that
    all IO operations are correctly sequenced and do not race with
    each others.
    
    Fixed: 353552540
    Change-Id: Ia6945093b063e8834288ce583e3c73fef8d9b64f
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5725110
    Commit-Queue: Mark Cogan <marq@chromium.org>
    Auto-Submit: Sylvain Defresne <sdefresne@chromium.org>
    Code-Coverage: findit-for-me@appspot.gserviceaccount.com <findit-for-me@appspot.gserviceaccount.com>
    Reviewed-by: Mark Cogan <marq@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1331013}

M       ios/chrome/browser/ui/sharing/share_download_overlay_coordinator.h
M       ios/chrome/browser/ui/sharing/share_download_overlay_coordinator.mm
M       ios/chrome/browser/ui/sharing/sharing_coordinator.mm

https://chromium-review.googlesource.com/5725110


### pe...@google.com (2024-07-23)

Merge review required: M127 is already shipping to stable.

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

### sd...@google.com (2024-07-23)

1. Fixes a security issue
2. <https://chromium-review.googlesource.com/c/chromium/src/+/5725110>
3. Yes
4. No
5. Not applicable
6. No

### pe...@google.com (2024-07-23)

**Merge approved:** your change passed merge requirements and is auto-approved for M128. Please go ahead and merge the CL to branch 6613 (refs/branch-heads/6613) manually. Please contact milestone owner if you have questions.
Merge instructions: <https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md>
Owners: harrysouders (Android), harrysouders (iOS), obenedict (ChromeOS), pbommana (Desktop)

### sd...@google.com (2024-07-24)

It looks like the CL landed before M128 branched. So no need to CP to M128.

### sp...@google.com (2024-07-24)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $11000.00 for this report.

Rationale for this decision:
$10,000 for report of mildly mitigated memory corruption in the browser process, mitigated by race and precondition of window shutdown + $1,000 bisect bonus


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-07-25)

Thank you for the report, lime. In addition to the above mentioned mitigations, your patch comments out a function and it's unclear how this would be potentially exploited outside of this patch in a real world scenario.
In the future, when supporting report with a patch needed to trigger the issue, please ensure that you explain, as part of the repro, the reason for the patch and attempt to demonstrate or explain how the issue could be exploited outside the conditions specified by the patch. [1]

[1] <https://chromium.googlesource.com/chromium/src/+/master/docs/security/vrp-faq.md#report-attachments>

### am...@chromium.org (2024-07-25)

Hi sdefresne@ -- apologies for any unnecessary prioritization by this as a P0/S0; in assessment, this issue was determined to be mitigated and not consistent to a critical severity issue. Updating as high severity.

### li...@gmail.com (2024-07-25)

RE: #12

Hi, Amy, i see, and will pay attention to that in the future.

### am...@chromium.org (2024-08-01)

M127 merge approved, please merge this fix to branch 6533 by 10am Pacific Friday, 2 August so this fix can be included in the next M127 Stable update -- thank you

### sd...@google.com (2024-08-02)

The CP has not landed yet because of infra failures of the CQ or failures to unrelated tests (i.e. integration tests that do not go through this API). Still trying to get the CP to land through the CQ.

### ap...@google.com (2024-08-02)

Project: chromium/src
Branch: refs/branch-heads/6533

commit b3afa79695dd14dc054006ffd17f8a1afca8c943
Author: Sylvain Defresne <sdefresne@chromium.org>
Date:   Fri Aug 02 17:24:43 2024

    [m127][ios] Fix blocks in SharingCoordinator
    
    Use helper functions and methods to avoid accidentely capturing
    pointers to C++ objects in blocks. Also use base::WeakPtr<...>
    when capturing pointers to C++ objects to prevent UaF.
    
    Use base::ThreadPool::CreateSequencedTaskRunner() to ensure that
    all IO operations are correctly sequenced and do not race with
    each others.
    
    (cherry picked from commit 7f0725c2c6c28395b2132a2fdfc5c354005a72fd)
    
    Fixed: 353552540
    Change-Id: Ia6945093b063e8834288ce583e3c73fef8d9b64f
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5725110
    Commit-Queue: Mark Cogan <marq@chromium.org>
    Auto-Submit: Sylvain Defresne <sdefresne@chromium.org>
    Code-Coverage: findit-for-me@appspot.gserviceaccount.com <findit-for-me@appspot.gserviceaccount.com>
    Reviewed-by: Mark Cogan <marq@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1331013}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5753007
    Commit-Queue: Sylvain Defresne <sdefresne@chromium.org>
    Reviewed-by: Olivier Robin <olivierrobin@chromium.org>
    Cr-Commit-Position: refs/branch-heads/6533@{#1879}
    Cr-Branched-From: 7e0b87ec6b8cb5cb2969e1479fc25776e582721d-refs/heads/main@{#1313161}

M       ios/chrome/browser/ui/sharing/share_download_overlay_coordinator.h
M       ios/chrome/browser/ui/sharing/share_download_overlay_coordinator.mm
M       ios/chrome/browser/ui/sharing/sharing_coordinator.mm

https://chromium-review.googlesource.com/5753007


### pe...@google.com (2024-10-29)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/353552540)*
