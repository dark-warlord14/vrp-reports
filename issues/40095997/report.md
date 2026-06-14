# Security: URL bar spoofing with using a file:/// URL

| Field | Value |
|-------|-------|
| **Issue ID** | [40095997](https://issues.chromium.org/issues/40095997) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | UI>Browser>Navigation |
| **Platforms** | iOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | mr...@chromium.org |
| **Created** | 2019-08-15 |
| **Bounty** | $500.00 |

## Description

**VERSION**  

Chrome Version: 77.0.3865.21 beta  

Operating System: iOS

**REPRODUCTION CASE**

This is similar to <https://crbug.com/chromium/989497>

1. Go to <https://lbstyle.github.io/o.html>
2. Click on the button.
3. Focus the address bar clear the existing address.
4. Paste the URL and enter.

Actual: Observe that ..tform.accounts.google.com URL displayed but the content area still shows lbstyle.github contents.

Expected: Page should not be displayed ..tform.accounts.google.com URL.

## Attachments

- [6843BFFE-6C96-4750-A8C5-B6E1E40321D1.MP4](attachments/6843BFFE-6C96-4750-A8C5-B6E1E40321D1.MP4) (video/mp4, 685.9 KB)
- [test case](attachments/test case) (text/plain, 683 B)

## Timeline

### ch...@gmail.com (2019-08-15)

[Empty comment from Monorail migration]

### mm...@chromium.org (2019-08-15)

[Empty comment from Monorail migration]

[Monorail components: UI>Browser>Navigation]

### sh...@chromium.org (2019-08-15)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ju...@chromium.org (2019-08-15)

[Empty comment from Monorail migration]

### mr...@chromium.org (2019-08-19)

It seems that if a provisional navigation is cancelled because the URL response cannot be rendered or downloaded in "decidePolicyForNavigationResponse":
https://cs.chromium.org/chromium/src/ios/web/navigation/crw_wk_navigation_handler.mm?rcl=7f17aecf4b96ef4c98c95ec0f7f5388c90348a52&l=463
the WKNavigation is not removed before [webStateImpl setIsLoading:false] in "didFailProvisionalNavigation]:
https://cs.chromium.org/chromium/src/ios/web/navigation/crw_wk_navigation_handler.mm?rcl=7f17aecf4b96ef4c98c95ec0f7f5388c90348a52&l=1687
Therefore when omnibox tries to update the URL from LocationBarModelDelegateIOS:
https://cs.chromium.org/chromium/src/ios/chrome/browser/ui/location_bar/location_bar_model_delegate_ios.mm?rcl=a33b60a9aa426175772f1e90f0804bd80bf7de2f&l=43
The navigation item is fetched from CRWWebController:
https://cs.chromium.org/chromium/src/ios/web/web_state/ui/crw_web_controller.mm?rcl=5eb34f49e9d46449307ea5ac3d44cb57175c96c8&l=570
Notice that "DidFinishNavigation" is not called in this case. I think the expected way of how it works is:
1. Omnibox should use "DidStartNavigation/DidStopNavigation" to update the URL instead of "DidStartLoading/DidStopLoading";
2. "DidStopNavigation" should be always paired with "DidStartNavigation".

eugenebut@ do you have any idea about how should we fix this?





### eu...@chromium.org (2019-08-19)

1.) Omnibox should use DidStartNavigation/DidStopNavigation, but updating URL in DidStartLoading/DidStopLoading should not cause URL spoof
2.) Agreed. Also did you mean to say that DidFinishNavigation should be always paired with DidStartNavigation?

Did we get DidStartNavigation callback with this bug?

### mr...@chromium.org (2019-08-20)

#6 Yes, I mean DidStartNavigation/DidFinishNavigation, and yes, "didStartNavigation" is called on LocationBarMediator.

### eu...@chromium.org (2019-08-20)

Thanks. Missing DidFinishNavigation call is a bug.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-08-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/1a83050a2165bb913d2b8aa9c0cd51490197159b

commit 1a83050a2165bb913d2b8aa9c0cd51490197159b
Author: Yi Su <mrsuyi@chromium.org>
Date: Tue Aug 20 22:19:43 2019

Remove WKNavigation in didFailProvisionalNavigation if cancelled

When a URL is rejected by //ios/web policy in
decidePolicyForNavigationResponse, didFailProvisionalNavigation will be
invoked later with "kWebKitErrorFrameLoadInterruptedByPolicyChange". In
this case, the WKNavigation should be removed from
CRWWKNavigationHandler.navigationStates so that WebStateObservers will
not get URL of the rejected navigation.

Bug: 994044
Change-Id: Ia764442316a32bddbd686460160f5e064d1cfa70
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1762229
Reviewed-by: Eugene But <eugenebut@chromium.org>
Commit-Queue: Yi Su <mrsuyi@chromium.org>
Cr-Commit-Position: refs/heads/master@{#688752}

[modify] https://crrev.com/1a83050a2165bb913d2b8aa9c0cd51490197159b/ios/web/navigation/crw_wk_navigation_handler.mm


### mr...@chromium.org (2019-08-20)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-08-20)

This bug requires manual review: Less than 17 days to go before AppStore submit on M77
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
Owners: benmason@(Android), kariahda@(iOS), dgagnon@(ChromeOS), lakpamarthy@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-08-21)

[Empty comment from Monorail migration]

### mr...@chromium.org (2019-08-23)

1. Does your merge fit within the Merge Decision Guidelines?
Yes.

2. Links to the CLs you are requesting to merge.
https://chromium-review.googlesource.com/c/chromium/src/+/1762229

3. Has the change landed and been verified on master/ToT?
Landed, not verified yet.

4. Why are these changes required in this milestone after branch?
Security issue.

5. Is this a new feature?
No.

### na...@google.com (2019-08-26)

[Empty comment from Monorail migration]

### ka...@google.com (2019-08-26)

Test, can we get verification here please.

### ka...@google.com (2019-08-28)

[Empty comment from Monorail migration]

### sr...@chromium.org (2019-08-28)

mrsuyi@ Can you let me know what is the expected behaviour here?
When I performed steps from original report, I see blue progress bar stuck at 10% loading forever. I am expecting a chrome error page should be displayed immediately.

Tested on M78.0.3895.0 canary, iPhoneX, iOS13.1

### wf...@chromium.org (2019-08-28)

Hi from VRP panel! chromium.khalil - Please remember to attach full PoC to the bug and not just rely on an external link.

### ch...@gmail.com (2019-08-28)

Oh okey... thanks! 

### na...@google.com (2019-08-28)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### pa...@chromium.org (2019-08-28)

Congrats! The Panel decided to reward $500 for this report! 

### na...@google.com (2019-08-28)

[Empty comment from Monorail migration]

### mr...@chromium.org (2019-08-29)

srikanthg@ the expected behavior should be like this:
1. Load https://lbstyle.github.io/o.html;
2. Load file://www.verylongurl.googlecloudplatform.accounts.google.com/;
3. Omnibox shows file://www.verylongurl.googlecloudplatform.accounts.google.com/, and progress bar appears;
4. Navigation is failed due to //ios/web policy;
5. Omnibox shows https://lbstyle.github.io/o.html, and progress bar disappears;

This is the same on Safari. Can you provide the environment you are using?

### sr...@chromium.org (2019-08-29)

Actually I just checked, the issue is fixed on iOS12.4.1 iPhone7plus with SlimNav OFF and ON.
But reproduces ONLY on iOS13.1 on iPhoneX, with SlimNav OFF and ON.
At step#5 omnibox still showing file://.....google.com and progress bar at 10%.

Please check the video below.
https://drive.google.com/file/d/1bnnaEzWorsoX0S-HfQrkrmv16oOvCoWF/view



### sh...@chromium.org (2019-08-29)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ka...@google.com (2019-09-03)

Seems like we should still merge the fix in c13. If it's still reproing on iOS 13.1 iPhone X, should this be considered an RBS still?

### ka...@google.com (2019-09-03)

[Empty comment from Monorail migration]

### ka...@google.com (2019-09-04)

Srikanth, can we file another bug for iOS 13/iPhone X repro and re-mark this one fixed?

### sr...@chromium.org (2019-09-05)

Verified on M78.0.3903.0 canary
Issue is not reproduced with Slim Nav OFF and ON.
Device: iPhone7
iOS: 12.4

I will report a new bug to track the fix on iOS13.

### sr...@chromium.org (2019-09-06)

Verified on iOS12.4.1 iPhone6plus
Build: M77.0.3865.69 beta

### sh...@chromium.org (2019-09-09)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-09-13)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-12-12)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-07-14)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mr...@google.com (2020-07-14)

[Empty comment from Monorail migration]

### is...@google.com (2020-07-14)

This issue was migrated from crbug.com/chromium/994044?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095997)*
