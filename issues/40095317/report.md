# Security: URL bar spoofing on iOS with history.back()

| Field | Value |
|-------|-------|
| **Issue ID** | [40095317](https://issues.chromium.org/issues/40095317) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | UI>Browser>Navigation |
| **Platforms** | iOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | ju...@chromium.org |
| **Created** | 2019-06-06 |
| **Bounty** | $3,000.00 |

## Description

**VERSION**  

Chrome Version: 75.0.3770.67 beta  

Operating System: iOS 12.3.1

**REPRODUCTION CASE**

- Enable slim-navigation-manager

1. Go to <https://lbstyle.github.io/x.html>
2. Click on the button and wait
3. On <https://lbstyle.github.io/attack.html>, click on the button.
4. Observe

## Attachments

- [0486158C-6CBC-4515-AFAD-6583F55C2672.MP4](attachments/0486158C-6CBC-4515-AFAD-6583F55C2672.MP4) (video/mp4, 245.4 KB)
- [x.html](attachments/x.html) (text/plain, 248 B)
- [attack.html](attachments/attack.html) (text/plain, 502 B)
- [7DC0D98B-6C50-4E81-8D3D-A7331B8C9420.MP4](attachments/7DC0D98B-6C50-4E81-8D3D-A7331B8C9420.MP4) (video/mp4, 936.5 KB)

## Timeline

### ch...@gmail.com (2019-06-06)

[Empty comment from Monorail migration]

### wf...@chromium.org (2019-06-06)

Thanks for your report. Initial Triage.

[Monorail components: UI>Browser>Navigation]

### wf...@chromium.org (2019-06-06)

Please upload full source for your PoC. We prefer not to visit external sites when doing reproductions.

"Please attach files directly, not in zip or other archive formats, and if
you've created a demonstration site please also attach the files needed to
reproduce the demonstration locally."

### da...@chromium.org (2019-06-06)

+eugenebut@, justincohen@ to triage.

### ch...@gmail.com (2019-06-06)

[Empty comment from Monorail migration]

### wf...@chromium.org (2019-06-06)

[note: haven't reproed this myself yet] - but question to the reporter - is the UI responsive when in this state i.e. could a user enter data or submit any information? from reading the code, it looks like it's in a tight refresh loop? Tentatively setting Low, but this might be Medium.

### wf...@chromium.org (2019-06-06)

[Empty comment from Monorail migration]

### ju...@chromium.org (2019-06-06)

[Empty comment from Monorail migration]

### wf...@chromium.org (2019-06-06)

[Empty comment from Monorail migration]

### ch...@gmail.com (2019-06-06)

The content area is interactive, so the user can enter enter data. I think the risk here should be higher than low.

### ch...@gmail.com (2019-06-06)

[Empty comment from Monorail migration]

### wf...@chromium.org (2019-06-06)

thanks for the added info. Again, I have not been able to repro this myself (justin, gabriel, can you help, please?) but given this I think it meets "Complete control over the apparent origin in the omnibox" which would be High.

### eu...@chromium.org (2019-06-06)

This is WKWebView bug, which I don't know how to workaround (yet).

self.webView.backForwardList.currentItem.URL returns https://www.google.com/ which is wrong
self.webView.URL returns https://lbstyle.github.io/attack.html which is correct

So this bug will not show up in Safari (and perhaps Firefox) because Safari uses self.webView.URL for the address bar.

The whole idea of slim nav was built on the concept of trusting self.webView.backForwardList.currentItem. The only possible workaround I can think of would be to "fix" self.webView.backForwardList.currentItem somehow. Ali, would you mind taking a look if we can do something from Chrome side to prevent self.webView.backForwardList.currentItem from breaking?

### ch...@gmail.com (2019-06-07)

Similar to https://crbug.com/chromium/887273.

### aj...@chromium.org (2019-06-07)

We can't directly control currentItem from the Chrome side. In the current architecture, currentItem lives in the UIProcess, but the WebProcesses are responsible for updating it by sending IPCs to the UIProcess. The bugs we're seeing in this area come from the fact that with the new (in iOS 12.2) process-swap-on-navigation logic, there are multiple WebProcesses corresponding to a single backForwardList, and the UIProcess sometimes gets confused about which WebProcess updates to accept and which to ignore. The real fix is to do a proper refactoring in WebKit so that the UIProcess is responsible for updating the backForwardList.

The most we can do on the Chrome side is to notice when currentItem seems wrong, and then react to that. The tricky part about this is that we can't check too early in the navigation (since the currentItem and the webView.URL won't necessarily match), and if we check too late then the page becomes interactive while the wrong URL is still possibly shown.

On the more general question of trusting currentItem, webView.URL seems more trustworthy in the current state of things -- just from a practical standpoint, bugs where webView.URL is wrong affect all WKWebView clients, so those bugs are going to get fixed with high priority in WebKit. 

### sh...@chromium.org (2019-06-07)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### eu...@chromium.org (2019-06-07)

ios/web has specific API, which was shaped by Chromium design and Legacy Navigation Manager implementation:

NavigationManager::GetLastCommittedItem (I think this relies on webView.backForwardList.currentItem)
NavigationManager::GetVisibleItem (relies on NavigationManager::GetLastCommittedItem)
WebState::GetLastCommittedURL (relies on NavigationManager::GetLastCommittedItem)
WebState::GetVisibleIURL (relies on NavigationManager::GetVisibleItem)

So this whole chain of trust collapses if we can't rely on webView.backForwardList.currentItem. If we can't fix webView.backForwardList.currentItem then I think we have 2 options:

1.) drop GetLastCommittedItem/GetVisibleItem and make WebState::GetLastCommittedURL/GetVisibleIURL rely on webView.URL and webView.backForwardList.currentItem.URL
2). make NavigationManager::GetLastCommittedItem rely on webView.URL and webView.backForwardList.currentItem.URL

#1 will probably take a lot of time to implement. As for #2, I have no idea how to do this in practice (but hopefully CCed folks have some clue).


### aj...@chromium.org (2019-06-10)

I've started debugging this, and it turns out that it reproduces even *without* process-swap-on-navigation. In particular, it also reproduces on iOS 12.1.

Continuing to debug to figure out how we're getting into this state.

### aj...@chromium.org (2019-06-11)

What's happening is that the history.go() call on attack.html moves the back/forward list to the google.com item (since the back/forward list is move preemptively on back/forward navigations) but the navigation is interrupted by a setLocation call before it even gets to didStartProvisionalNavigation. After that, there's a never-ending cycle of: 1) document.write call sets the location back to attack.html 2) a setLocation call changes to the location to https://jigsaw.w3.org. Since no navigation ever commits, we stay in a state where the google.com item is the current item.

In general, WebKit doesn't undo a back/forward navigation history update when the navigation is interrupted by another navigation. This is longstanding behavior dating back at least to https://bugs.webkit.org/show_bug.cgi?id=48812. WebKit will only undo a back/forward history update if we respond to the navigation policy decision with "Ignore", or if the load is cancelled without any new provisional load taking its place. 

In this particular bug, the google.com load is being interrupted even before it reaches the code added in the bug mentioned above. If we changed the logic in FrameLoader::loadWithDocumentLoader so that the call to policyChecker().setLoadType(type) happens after policyChecker().stopCheck(), then back/forward loads that are cancelled by another load while still in the policy stage would still have their history change undone, but that would just make the attack more challenging timing-wise.

### sr...@chromium.org (2019-06-12)

[Empty comment from Monorail migration]

### ju...@chromium.org (2019-06-13)

WKBackForwardList was put on hold.

### ju...@chromium.org (2019-06-13)

[Empty comment from Monorail migration]

### ju...@chromium.org (2019-06-13)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-06-13)

[Empty comment from Monorail migration]

### li...@chromium.org (2019-06-17)

Justin, did you want RBS removed?

### ju...@chromium.org (2019-06-17)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-06-18)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-06-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/a11f4f77f56d7fbea2ddbb11e6a201ba8f59f8cb

commit a11f4f77f56d7fbea2ddbb11e6a201ba8f59f8cb
Author: Justin Cohen <justincohen@google.com>
Date: Tue Jun 18 20:14:26 2019

[ios/web] Suppress visibleItem during lastCommittedItem mismatch.

WKWebView is more aggressive than Chromium in updating the visible
URL, and there are many cases where the WKWebView URL has updated and
Chromium still displays the last committed item.  Normally this is
managed by WKBasedNavigationManagerImpl last committed, but there are a
few periods during fast navigations where WKWebView URL has updated
and ios/web can't always verify what should be shown for the visible
item. More importantly, there are bugs in WkWebView where WKWebView's
URL and backForwardList.currentItem can fall out of sync.  While those
bugs should be fixed, safeguard visibleItem by returning documentURL
in those untrusted situations.

Bug: 971740

Change-Id: Iafaa274fc871203a08b71dfd4ec71b03119ee8a7
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1656095
Commit-Queue: Justin Cohen <justincohen@chromium.org>
Reviewed-by: Gauthier Ambard <gambard@chromium.org>
Reviewed-by: Eugene But <eugenebut@chromium.org>
Reviewed-by: Ali Juma <ajuma@chromium.org>
Reviewed-by: Danyao Wang <danyao@chromium.org>
Cr-Commit-Position: refs/heads/master@{#670180}

[modify] https://crrev.com/a11f4f77f56d7fbea2ddbb11e6a201ba8f59f8cb/ios/chrome/browser/tabs/tab_unittest.mm
[modify] https://crrev.com/a11f4f77f56d7fbea2ddbb11e6a201ba8f59f8cb/ios/web/navigation/navigation_manager_impl_unittest.mm
[modify] https://crrev.com/a11f4f77f56d7fbea2ddbb11e6a201ba8f59f8cb/ios/web/navigation/wk_based_navigation_manager_impl.h
[modify] https://crrev.com/a11f4f77f56d7fbea2ddbb11e6a201ba8f59f8cb/ios/web/navigation/wk_based_navigation_manager_impl.mm
[modify] https://crrev.com/a11f4f77f56d7fbea2ddbb11e6a201ba8f59f8cb/ios/web/navigation/wk_based_navigation_manager_impl_unittest.mm
[modify] https://crrev.com/a11f4f77f56d7fbea2ddbb11e6a201ba8f59f8cb/ios/web/web_state/web_state_impl.mm


### ju...@chromium.org (2019-06-18)

I'd like to merge this to M76 so we can attempt another (very) small slimnav experiment.  This change only affects slimmav, which we do not plan to enable at any high percentage for M76, so the risk to non-slimnav is zero.

### sh...@chromium.org (2019-06-18)

This bug requires manual review: M76 has already been promoted to the beta branch, so this requires manual review
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://goto.google.com/chrome-release-branch-merge-guidelines
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: govind@(Android), kariahda@(iOS), cindyb@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-06-19)

[Empty comment from Monorail migration]

### aj...@chromium.org (2019-06-19)

I've filed https://bugs.webkit.org/show_bug.cgi?id=199027 for the underlying WebKit issue, to clarify whether this is intentional behavior or a bug.

### ju...@chromium.org (2019-06-20)

benmason@ per c30, yes, c28, security fixes, no, yes.

### be...@chromium.org (2019-06-20)

Approved.

### sh...@chromium.org (2019-06-24)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### na...@google.com (2019-06-24)

[Empty comment from Monorail migration]

### ka...@google.com (2019-06-24)

[Empty comment from Monorail migration]

### ka...@google.com (2019-06-24)

[Empty comment from Monorail migration]

### su...@chromium.org (2019-06-25)

Verified in:

App Version: 77.0.3834.0 canary
Devices: iPhone X, iPhone 8 Plus
iOS Versions: 12.3.1, 12.4 beta 5

Followed the steps mentioned in https://crbug.com/chromium/971740#c0 & 11,  on navigating back from https://lbstyle.github.io/attack.html, page doesn't redirect to google.com

Video:
https://drive.google.com/open?id=1G3_AVYHE2VOUX2b6ziLeoZJaP7FfEeXc

### ju...@chromium.org (2019-06-25)

kariahda@ I'd like to also merge a followup to crrev.com/c/1669577 here: crrev.com/c/1673566

This change only affects SlimNav, which will be off for M76 or at a very low experiment percentage.

### sh...@chromium.org (2019-06-25)

This bug requires manual review: M76 has already been promoted to the beta branch, so this requires manual review
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://goto.google.com/chrome-release-branch-merge-guidelines
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: govind@(Android), kariahda@(iOS), cindyb@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ju...@chromium.org (2019-06-25)

kariahda@ per c41, yes, c40, yes, security fixes, no, yes.

### su...@chromium.org (2019-06-26)

[Empty comment from Monorail migration]

### vb...@chromium.org (2019-06-26)

App Version: 76.0.3809.43 beta
Devices: iPhone 7 plus, iPad Pro
iOS Versions: 12.3.1, 12.2

Verified following the steps mentioned in https://crbug.com/chromium/971740#c0 & 11,  on navigating back from https://lbstyle.github.io/attack.html, page doesn't redirect to google.com

### sh...@chromium.org (2019-06-28)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ka...@google.com (2019-06-28)

Approved, please merge asap.

### cr...@appspot.gserviceaccount.com (2019-06-29)

The following revision refers to this bug: 
https://chromium.googlesource.com/chromium/src.git/+/12e033c8ac1ba3a57e6f870a17a92c18052b2edf

Commit: 12e033c8ac1ba3a57e6f870a17a92c18052b2edf
Author: justincohen@google.com
Commiter: justincohen@chromium.org
Date: 2019-06-29 16:09:01 +0000 UTC

[ios/web] Move SlimNav VisibleItem trust check to LastCommitted.

As a followup to http://crrev.com/c/1669577, move the trust check to
LastCommitted so all WebState APIs can return a trusted URL rather than
just VisibleItem.

(cherry picked from commit a0804ddd74812ba8fc4efa56fc928289a663af67)

BUG: 971740
Change-Id: Ia912007c6bfc65efa0443a07b072d9ed8075cedd
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1673566
Commit-Queue: Justin Cohen <justincohen@chromium.org>
Reviewed-by: Gauthier Ambard <gambard@chromium.org>
Reviewed-by: Ali Juma <ajuma@chromium.org>
Reviewed-by: Eugene But <eugenebut@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#672146}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1682715
Reviewed-by: Justin Cohen <justincohen@chromium.org>
Cr-Commit-Position: refs/branch-heads/3809@{#661}
Cr-Branched-From: d82dec1a818f378c464ba307ddd9c92133eac355-refs/heads/master@{#665002}


### na...@google.com (2019-07-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### pa...@chromium.org (2019-07-17)

Congrats! The Panel decided to reward $3,000 for this report!

### ch...@gmail.com (2019-07-18)

Nice reward! - Thanks! 

### na...@google.com (2019-07-18)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-09-25)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/971740?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail blocking: crbug.com/chromium/789582]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095317)*
