# Security: URL spoofing on iOS after UI action

| Field | Value |
|-------|-------|
| **Issue ID** | [40089962](https://issues.chromium.org/issues/40089962) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | UI>Browser>Navigation, UI>Browser>Omnibox |
| **Platforms** | iOS |
| **Reporter** | fg...@gmail.com |
| **Assignee** | eu...@chromium.org |
| **Created** | 2017-12-21 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

A fake login page which actually displays the URL for the attack target. In other words, instead of the URL showing the fake login page URL, it shows the target URL with the fake page contents, allowing for password collection by a malicious page.

**VERSION**  

Chrome Version: [63.0.3239.73] (latest)  

Operating System: iOS 11.2.1 (iPhone 7)

**REPRODUCTION CASE**  

See this video:  

<http://digilus.com/fake/Security_flaw2_FG.mp4>

It's critical that the fake page is initiated using a link click (which is why in the video, I click on the link to the page itself).

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

N/A

## Attachments

- [clip.mp4](attachments/clip.mp4) (video/mp4, 5.4 MB)

## Timeline

### fg...@gmail.com (2017-12-21)

[Comment Deleted]

### fg...@gmail.com (2017-12-21)

Better said, this appears to be a flaw that allows for specific CSS code to exploit the URL in iOS Chrome. This issue does not occur in Safari.

### el...@chromium.org (2017-12-21)

Interesting. The Omnibox appears to be in a corrupt state whereby the security status doesn't match the displayed URL (e.g. no lock icon).


[Monorail components: UI>Browser>Navigation UI>Browser>Omnibox]

### fg...@gmail.com (2017-12-23)

Any update on this?

Steps to reproduce:
1. Open a new Chrome tab
2. Navigate to a web page
3. Click on any link 
4. Navigate to Facebook
5. Click on a comment so that it causes a pop-up of the feed item with comments (see attached video)
6. Click the time on the top of the iOS screen UI
7. Chrome scrolls to the top of the screen, and the Omnibox corrupts, causes the URL display the same m.facebook.com hostname but the browser actually goes back to the first page in your history
8. Per my sample video, this could be a malicious login page that captures user data.

### rs...@chromium.org (2017-12-28)

eugenebut: Can you help route this?

### sh...@chromium.org (2017-12-28)

[Empty comment from Monorail migration]

### eu...@chromium.org (2017-12-28)

There are 2 problems:
1.) Chrome goes one extra entry back (will be tracked in crbug.com/797969)
2.) URL is spoofed (will be tracked here)


### eu...@chromium.org (2017-12-28)

Danyao, Kurt, crrev.com/c/846020 fixes the bug, and because this is URL spoofing issue I did not explain the root cause in CL description.

The bug happened because URLDidChangeWithoutDocumentChange: was mistakenly called and broke CRWSessionController state. Updating _documentURL right after same document navigations ensures that URLDidChangeWithoutDocumentChange: is not called.

This bug does not exist with WK-based navigation manager.

### da...@chromium.org (2018-01-02)

I'm not fully following the fix... Given that we can't put details in the CL, would you consider documenting the root cause in this bug?

The part that puzzles me is that URLDidChangeWithoutDocumentChange: doesn't interact with CRWSessionController. So I didn't understand how it corrupts CRWSessionController state.

It seems to me that the root cause may be a race condition between push/popState and back-forward navigation using history API. It seems that the comment UI may be implemented using a pushState, and touching the status bar scrolls up and performs a back navigation to dismiss the comment UI. Maybe goBack happened before pushState is completely finished. This may also explain why Chrome goes one extra entry back because the pushState history entry has not been built yet.

### eu...@chromium.org (2018-01-02)

URLDidChangeWithoutDocumentChange: calls registerLoadRequestForURL:, which interacts with session controller, that's where navigation state gets corrupted.

LegacyNavigationManagerImpl::FinishGoToIndex changes SessionController's LastCommittedURL for same document navigation, but leaves WebController's _documentURL unchanged. _documentURL should never be out of sync with LastCommittedURL, so the fix puts these 2 URLs in sync. Please note that corruption happens after LegacyNavigationManagerImpl::FinishGoToIndex.

Generally we should remove _documentURL at all, but that's a separate issue, which will be easier to fix after moving to WK-based navigation manager.

### da...@chromium.org (2018-01-02)

Thanks Eugene. I missed the pending URL update in reigsterLoadRequestForURL:. Fix LGTM.

### kk...@chromium.org (2018-01-04)

The fix LGTM, thanks for the detailed explanation in this bug.

### bu...@chromium.org (2018-01-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/601d03f44018fafd845334e1cec17cd01122d164

commit 601d03f44018fafd845334e1cec17cd01122d164
Author: Eugene But <eugenebut@google.com>
Date: Thu Jan 04 20:23:34 2018

Updated _documentURL for same-document navigations.

_documentURL is not needed for WK-based navigation manager
so there is not much value in adding unit tests for this
new code.

Bug: 796777
Cq-Include-Trybots: master.tryserver.chromium.mac:ios-simulator-cronet;master.tryserver.chromium.mac:ios-simulator-full-configs
Change-Id: Ib4635f6d6d20934ea3fb07793d460ac3c1a786e0
Reviewed-on: https://chromium-review.googlesource.com/846020
Reviewed-by: Kurt Horimoto <kkhorimoto@chromium.org>
Commit-Queue: Eugene But <eugenebut@chromium.org>
Cr-Commit-Position: refs/heads/master@{#527080}
[modify] https://crrev.com/601d03f44018fafd845334e1cec17cd01122d164/ios/web/navigation/legacy_navigation_manager_impl.h
[modify] https://crrev.com/601d03f44018fafd845334e1cec17cd01122d164/ios/web/navigation/legacy_navigation_manager_impl.mm
[modify] https://crrev.com/601d03f44018fafd845334e1cec17cd01122d164/ios/web/navigation/navigation_manager_delegate.h
[modify] https://crrev.com/601d03f44018fafd845334e1cec17cd01122d164/ios/web/navigation/navigation_manager_impl.h
[modify] https://crrev.com/601d03f44018fafd845334e1cec17cd01122d164/ios/web/navigation/navigation_manager_impl.mm
[modify] https://crrev.com/601d03f44018fafd845334e1cec17cd01122d164/ios/web/navigation/navigation_manager_impl_unittest.mm
[modify] https://crrev.com/601d03f44018fafd845334e1cec17cd01122d164/ios/web/navigation/wk_based_navigation_manager_impl.h
[modify] https://crrev.com/601d03f44018fafd845334e1cec17cd01122d164/ios/web/navigation/wk_based_navigation_manager_impl.mm
[modify] https://crrev.com/601d03f44018fafd845334e1cec17cd01122d164/ios/web/navigation/wk_based_navigation_manager_impl_unittest.mm
[modify] https://crrev.com/601d03f44018fafd845334e1cec17cd01122d164/ios/web/test/fakes/fake_navigation_manager_delegate.h
[modify] https://crrev.com/601d03f44018fafd845334e1cec17cd01122d164/ios/web/test/fakes/fake_navigation_manager_delegate.mm
[modify] https://crrev.com/601d03f44018fafd845334e1cec17cd01122d164/ios/web/web_state/navigation_and_load_callbacks_inttest.mm
[modify] https://crrev.com/601d03f44018fafd845334e1cec17cd01122d164/ios/web/web_state/ui/crw_web_controller.h
[modify] https://crrev.com/601d03f44018fafd845334e1cec17cd01122d164/ios/web/web_state/ui/crw_web_controller.mm
[modify] https://crrev.com/601d03f44018fafd845334e1cec17cd01122d164/ios/web/web_state/web_state_impl.h
[modify] https://crrev.com/601d03f44018fafd845334e1cec17cd01122d164/ios/web/web_state/web_state_impl.mm


### fg...@gmail.com (2018-01-04)

Is this issue eligible for the Chrome Rewards Program?  I understand there is a Reward Panel that meets every week but I haven't received any notifications and I'd like to know if this is being considered. 

### eu...@chromium.org (2018-01-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-01-04)

This bug requires manual review: Less than 15 days to go before AppStore submit on M64
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), kbleicher@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-01-05)

[Empty comment from Monorail migration]

### cm...@chromium.org (2018-01-05)

Please confirm the fix has been verified in canary

### eu...@chromium.org (2018-01-05)

Srikanth, Please retest with Canary.

### sr...@chromium.org (2018-01-08)

Tapping on the status bar redirects to the NTP, or another webpage if the Back History menu has more entries. Omnibox correctly reflects the URL and webpage contents.

Verified in M65.0.3315.0 Canary
Device: iPhoneX, iOS: 11.2.5

### cm...@google.com (2018-01-08)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-01-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/c19ad7352c4c53ecbf8e0ee1d03894be0803fef0

commit c19ad7352c4c53ecbf8e0ee1d03894be0803fef0
Author: Eugene But <eugenebut@google.com>
Date: Mon Jan 08 18:04:36 2018

Updated _documentURL for same-document navigations.

_documentURL is not needed for WK-based navigation manager
so there is not much value in adding unit tests for this
new code.

TBR=eugenebut@google.com

(cherry picked from commit 601d03f44018fafd845334e1cec17cd01122d164)

Bug: 796777
Cq-Include-Trybots: master.tryserver.chromium.mac:ios-simulator-cronet;master.tryserver.chromium.mac:ios-simulator-full-configs
Change-Id: Ib4635f6d6d20934ea3fb07793d460ac3c1a786e0
Reviewed-on: https://chromium-review.googlesource.com/846020
Reviewed-by: Kurt Horimoto <kkhorimoto@chromium.org>
Commit-Queue: Eugene But <eugenebut@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#527080}
Reviewed-on: https://chromium-review.googlesource.com/854398
Reviewed-by: Eugene But <eugenebut@chromium.org>
Cr-Commit-Position: refs/branch-heads/3282@{#445}
Cr-Branched-From: 5fdc0fab22ce7efd32532ee989b223fa12f8171e-refs/heads/master@{#520840}
[modify] https://crrev.com/c19ad7352c4c53ecbf8e0ee1d03894be0803fef0/ios/web/navigation/legacy_navigation_manager_impl.h
[modify] https://crrev.com/c19ad7352c4c53ecbf8e0ee1d03894be0803fef0/ios/web/navigation/legacy_navigation_manager_impl.mm
[modify] https://crrev.com/c19ad7352c4c53ecbf8e0ee1d03894be0803fef0/ios/web/navigation/navigation_manager_delegate.h
[modify] https://crrev.com/c19ad7352c4c53ecbf8e0ee1d03894be0803fef0/ios/web/navigation/navigation_manager_impl.h
[modify] https://crrev.com/c19ad7352c4c53ecbf8e0ee1d03894be0803fef0/ios/web/navigation/navigation_manager_impl.mm
[modify] https://crrev.com/c19ad7352c4c53ecbf8e0ee1d03894be0803fef0/ios/web/navigation/navigation_manager_impl_unittest.mm
[modify] https://crrev.com/c19ad7352c4c53ecbf8e0ee1d03894be0803fef0/ios/web/navigation/wk_based_navigation_manager_impl.h
[modify] https://crrev.com/c19ad7352c4c53ecbf8e0ee1d03894be0803fef0/ios/web/navigation/wk_based_navigation_manager_impl.mm
[modify] https://crrev.com/c19ad7352c4c53ecbf8e0ee1d03894be0803fef0/ios/web/navigation/wk_based_navigation_manager_impl_unittest.mm
[modify] https://crrev.com/c19ad7352c4c53ecbf8e0ee1d03894be0803fef0/ios/web/test/fakes/fake_navigation_manager_delegate.h
[modify] https://crrev.com/c19ad7352c4c53ecbf8e0ee1d03894be0803fef0/ios/web/test/fakes/fake_navigation_manager_delegate.mm
[modify] https://crrev.com/c19ad7352c4c53ecbf8e0ee1d03894be0803fef0/ios/web/web_state/navigation_and_load_callbacks_inttest.mm
[modify] https://crrev.com/c19ad7352c4c53ecbf8e0ee1d03894be0803fef0/ios/web/web_state/ui/crw_web_controller.h
[modify] https://crrev.com/c19ad7352c4c53ecbf8e0ee1d03894be0803fef0/ios/web/web_state/ui/crw_web_controller.mm
[modify] https://crrev.com/c19ad7352c4c53ecbf8e0ee1d03894be0803fef0/ios/web/web_state/web_state_impl.h
[modify] https://crrev.com/c19ad7352c4c53ecbf8e0ee1d03894be0803fef0/ios/web/web_state/web_state_impl.mm


### aw...@chromium.org (2018-01-12)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@chromium.org (2018-01-12)

Thanks! The VRP Panel decided to reward $500 for this report, due to the amount of user interaction required. A member of our finance team will be in touch to arrange payment. Also, how would you like to be credited in our release notes?

### aw...@chromium.org (2018-01-12)

[Empty comment from Monorail migration]

### fg...@gmail.com (2018-01-12)

That's great, thank you! I'm glad this will be resolved in the upcoming release.  To answer your question on credit, you may use my name, Frank Goytisolo.  If you need anything else, please let me know.

### pi...@chromium.org (2018-01-12)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-03-27)

[Empty comment from Monorail migration]

### aw...@google.com (2018-03-31)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-04-13)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2018-04-13)

This issue was migrated from crbug.com/chromium/796777?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: UI>Browser>Navigation, UI>Browser>Omnibox]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40089962)*
