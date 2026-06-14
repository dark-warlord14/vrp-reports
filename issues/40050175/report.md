# Security: URL bar spoofing on iOS 

| Field | Value |
|-------|-------|
| **Issue ID** | [40050175](https://issues.chromium.org/issues/40050175) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Mobile>iOSWeb>Security |
| **Platforms** | iOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | ga...@google.com |
| **Created** | 2019-09-19 |
| **Bounty** | $500.00 |

## Description

**VERSION**  

Chrome Version: 78.0.3904.20  

Operating System: iOS

**REPRODUCTION CASE**

1. Lunch the PoC
2. Click on the button to copy the link
3. Focus the address bar and past the link
4. Click on the link to stop pending

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 673 B)
- [6199AB97-2C3F-424F-8756-60F9C9AE4FDD.MP4](attachments/6199AB97-2C3F-424F-8756-60F9C9AE4FDD.MP4) (video/mp4, 498.7 KB)
- deleted (application/octet-stream, 0 B)

## Timeline

### ch...@gmail.com (2019-09-19)

[Empty comment from Monorail migration]

### rs...@chromium.org (2019-09-20)

mrsuyi: Could you take a look? I don’t have a device to try and repro this.

[Monorail components: Mobile>iOSWeb>Security]

### ju...@chromium.org (2019-09-20)

This reproduces with SlimNav both off an on, and on Safari too.

Chrome shows the pending url google.com with the old content, and then after 60 seconds reverts to showing the poc URL.  Chrome stops showing the loading bar after tapping the second link.  Chrome does not alert when tapping an invalid protocol url.

Safari also shows 'google.com' in the omnibox (it's pending), but they also display an alert saying the second link address is invalid.  After dismissing the alert, Safari still shows google.com with the old content, and then replaces the content with a 'stopped responding' page after 60 seconds.  Safari also stops showing the loading bar after tapping the second link.

The difference seems to be Chrome reverts to showing the poc page and url, Safari eventually shows google.com with a stopped responding page.

What is the correct thing to do here?  It is correct that we show google.com while it's pending, and still trying to load.  Perhaps it's just not that the loading progress bar or spinner aren't displayed?  Safari also doesn't show this.

If you don't tap on the link, Chrome eventually shows the 'site cannot be reached' error, so perhaps that's the bug?

Should chrome display alerts for invalid protocols?  Is not doing that part of the bug, or just not showing the spinner?

rsesek@ wdyt?  I think this is probably low severity. I'm not sure what is correct here...

### rs...@chromium.org (2019-09-20)

Thanks for taking a look. I agree it makes some sense for the address bar to show the pending load, but it should probably revert after it fails.

But this is really a question for Enamel, so CC +estark.

Regarding Sev-Low, I think this could be downgraded but our severity guidelines do put spoofs at Medium. I’ll let Enamel decide.

### ju...@chromium.org (2019-09-20)

>  but it should probably revert after it fails.

...it does revert after it fails.  I don't know why we don't show the loading bar anymore (like safari) or why we revert to the old page rather than show the failure page (different from safari).

### rs...@chromium.org (2019-09-20)

Sorry, I wrote “revert” when I meant “show the error page,” since it seems like a failed navigation.

### ju...@chromium.org (2019-09-20)

rsesek@ agreed

estart@ unsure if there's a security implication here, since the end result is either 'show error page with google in omnibox' or 'revert to poc url with old content'.

Not showing the progress bar might be worth filing a radar depending on the cause.

### es...@chromium.org (2019-09-20)

Agree with severity Medium, since this is a reasonably convincing spoof with some mitigations. (Convincing spoof with no mitigations would be High.)

Showing an error page seems like the right thing to do IMO.

### ju...@chromium.org (2019-09-20)

@estark, per offline conversation, can you link to a bug on differentiating pending vs committed urls?  It sounds like the lack of a progress bar is the spoof, and the not showing error page is a bug, but maybe not a spoof.  Do you agree?



### es...@chromium.org (2019-09-20)

Agree with #9. It doesn't look like we have an open bug for differentiating pending vs committed URLs, but it's discussed in https://bugs.chromium.org/p/chromium/issues/detail?id=719856#c11 and a number of bugs linked from that thread.

### sh...@chromium.org (2019-09-21)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-09-21)

[Empty comment from Monorail migration]

### mr...@chromium.org (2019-09-23)

Here is what happens:

1. User loads https://www.google.com:1234/ in omnibox;
2. KVO of WKWebView.URL=https://www.google.com:1234/ and WKWebView.loading=true are invoked;
3. WebStateImpl::IsLoading is set to true;
3. "decidePolicyForNavigationAction" and "didStartProvisionalNavigation" are invoked for https://www.google.com:1234/;
4. User taps on the link of htttps://www.verylongurl.googlecloudplatform.accounts.google.com in the page;
5. "decidePolicyForNavigationAction" is invoked for htttps://www.verylongurl.googlecloudplatform.accounts.google.com, with WKWebView.URL=https://www.google.com:1234/, and reaches here:
https://cs.chromium.org/chromium/src/ios/web/navigation/crw_wk_navigation_handler.mm?rcl=644d8a647b02c897606f5bf55f6da0584af3c899&l=382
6. WebStateImpl::IsLoading is set to false which emits a "webStateDidStopLoading" event to ToolbarMediator and hides the the progress bar:
https://cs.chromium.org/chromium/src/ios/chrome/browser/ui/toolbar/toolbar_mediator.mm?rcl=644d8a647b02c897606f5bf55f6da0584af3c899&l=130

The root cause here is that WebState::IsLoading is set to false while WKWebView.loading==true. I think only updating WebState::IsLoading in KVO of WKWebView.loading will fix this bug, and here is a design doc about it:
https://docs.google.com/document/d/1i2Ihhr6zfVs60lMXAFQuKpSh3eFs35s_pHF51a-Zujg/edit?usp=sharing

However that change will probably take a long time to be landed, and I don't have a feasible solution only for this bug right now.

### ka...@google.com (2019-10-01)

estark, +adetaylor

Please see c13. It looks like there is no feasible solution for this bug for M78, and RBS was added by sheriffbot in c11 after some investigations.

Please confirm it's ok to *not* have this fixed in M78 stable.

### ad...@chromium.org (2019-10-01)

justincohen@, can you confirm whether this bug has been around forever, or was introduced in M78? From https://crbug.com/chromium/1006012#c3 it sounds like it might have been around for a while, in which case I'll adjust Security_Impact and remove the RBS flag. (RBS was added by Sheriffbot on the grounds that this is a regression).

### ju...@chromium.org (2019-10-01)

 adetaylor@ This is not a new issue.

### ad...@chromium.org (2019-10-02)

Thanks.

### sh...@chromium.org (2019-10-07)

mrsuyi: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-10-22)

mrsuyi: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mr...@chromium.org (2019-10-31)

[Empty comment from Monorail migration]

### mr...@chromium.org (2019-10-31)

[Empty comment from Monorail migration]

### ch...@gmail.com (2019-11-07)

[Comment Deleted]

### ga...@chromium.org (2019-11-12)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-12-11)

[Empty comment from Monorail migration]

### ga...@chromium.org (2019-12-11)

estark@, 3 questions:
1. When the user tap on the invalid link (e.g. httttps://), is the correct behavior to display an alert saying "Trying to access invalid URL" (as the other browsers do)?
2. When a navigation fails because it was cancelled (as it is the case for the first navigation here after 60s and tapping on the invalid link), should we display and error page or revert back to the original page & URL?
3. Do we need to fix both of above two questions to mark this bug as fix or can we mark this bug as fixed once the spoofing issue is resolved and do the other changes separately?

### ga...@chromium.org (2019-12-13)

estark@: ping

### es...@chromium.org (2019-12-13)

Re #25:
1. That sounds fine from a security perspective, but you might want to check with UX.
2. Either one sounds fine to me from a security perspective; what do we do on other platforms? Reverting back to the original page and URL sounds slightly more natural to me.
3. I think once the spoof is fixed, we can mark this as fixed and file a separate bug for the other non-security changes.

### ga...@chromium.org (2019-12-16)

Thanks!
1. I have checked with UX, they would prefer a popup indicating an incorrect URL (on desktop we don't show anything)
2. On desktop we have the same behavior (i.e. reverting to the original URL). I think it is probably the best.
3. Thanks. This is rolling out as an experiment, the bug will be marked as fixed once we reach 100%.

### mr...@chromium.org (2019-12-16)

[Empty comment from Monorail migration]

### su...@chromium.org (2020-01-14)

Tested on:

App Version:  80.0.3987.50 beta
Devices: iPhone 6 Plus, iPhone XS
iOS Versions: 12.4.2, 13.3.1 Beta

Issue is fixed with feature flag #use-WKWebView-loading. Chrome shows the pending URL google.com with the old content and loading bar when the navigation expires after tapping on the incorrect link, it reverts to the original page and URL. 

### ch...@gmail.com (2020-01-16)

Verified on 80.0.3987.42 beta. Fixed.

### ch...@gmail.com (2020-01-20)

Is this should be marked as “Fixed”?

### ad...@chromium.org (2020-01-21)

gambard@ did you commit a fix here? Or was this fixed by another change? If the latter, please figure out the relevant crbug and mark this one as a duplicate, so we can ensure reporters are credited properly in release notes. Thanks.

### ga...@chromium.org (2020-01-28)

Closing this. It is rolling out via Finch and will be enabled by default soon.
Thanks for your patience.

### sh...@chromium.org (2020-01-28)

[Empty comment from Monorail migration]

### ad...@google.com (2020-01-30)

gambard@ per https://crbug.com/chromium/1006012#c33 I'm going to need a bit more help from you to make sure this is properly credited in the release notes and a CVE allocated. Will this be fixed in the initial release of M80? (Whether by Finch or code change.)

### ga...@chromium.org (2020-01-31)

The goal is to ramp up from 1% to 100% via Finch in M80.

### ad...@google.com (2020-02-02)

Thanks. I'll credit it on M80 then.

### na...@google.com (2020-02-03)

[Empty comment from Monorail migration]

### sh...@chromium.org (2020-02-03)

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M80. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2020-02-03)

This bug requires manual review: Less than -2 days to go before AppStore submit on M80
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
Owners: govind@(Android), Kariahda@(iOS), dgagnon@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ga...@chromium.org (2020-02-03)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-02-03)

[Empty comment from Monorail migration]

### aw...@google.com (2020-02-05)

Hi mrsuyi@ - some other Chromium embedders are interested in this bug now it's been included in M80 release notes.  Is Restrict-View-Google from https://crbug.com/chromium/1006012#c13 still needed (given the doc link will remain Google only) Thanks.

### ga...@chromium.org (2020-02-05)

I removed the Restrict-View-Google.

### su...@chromium.org (2020-02-05)

[Empty comment from Monorail migration]

### na...@google.com (2020-02-05)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### pa...@chromium.org (2020-02-06)

Congrats the Panel decided to award $500 for this report! 

### na...@google.com (2020-02-06)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-02-10)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-02-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/9a85728692b46f719dd2b0df05da5fbce93c7880

commit 9a85728692b46f719dd2b0df05da5fbce93c7880
Author: Gauthier Ambard <gambard@chromium.org>
Date: Thu Feb 27 07:56:08 2020

[iOS] Cleanup after using WK loading

This CL removes the code that was doing the switch for the feature to
use the WKWebView loading property.
The property is enabled to 100%.

Bug: 1006012,767092
Change-Id: Id4a4ca3ad18b24cb97e79c32aece943470d9d0a5
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2074641
Auto-Submit: Gauthier Ambard <gambard@chromium.org>
Reviewed-by: Eugene But <eugenebut@chromium.org>
Commit-Queue: Gauthier Ambard <gambard@chromium.org>
Cr-Commit-Position: refs/heads/master@{#744967}

[modify] https://crrev.com/9a85728692b46f719dd2b0df05da5fbce93c7880/ios/chrome/browser/flags/about_flags.mm
[modify] https://crrev.com/9a85728692b46f719dd2b0df05da5fbce93c7880/ios/chrome/browser/flags/ios_chrome_flag_descriptions.cc
[modify] https://crrev.com/9a85728692b46f719dd2b0df05da5fbce93c7880/ios/chrome/browser/flags/ios_chrome_flag_descriptions.h
[modify] https://crrev.com/9a85728692b46f719dd2b0df05da5fbce93c7880/ios/chrome/browser/ui/tab_grid/tab_grid_mediator_unittest.mm
[modify] https://crrev.com/9a85728692b46f719dd2b0df05da5fbce93c7880/ios/web/common/features.h
[modify] https://crrev.com/9a85728692b46f719dd2b0df05da5fbce93c7880/ios/web/common/features.mm
[modify] https://crrev.com/9a85728692b46f719dd2b0df05da5fbce93c7880/ios/web/navigation/crw_web_view_navigation_observer.mm
[modify] https://crrev.com/9a85728692b46f719dd2b0df05da5fbce93c7880/ios/web/navigation/crw_wk_navigation_handler.mm
[modify] https://crrev.com/9a85728692b46f719dd2b0df05da5fbce93c7880/ios/web/navigation/wk_based_navigation_manager_impl.mm
[modify] https://crrev.com/9a85728692b46f719dd2b0df05da5fbce93c7880/ios/web/web_state/ui/crw_web_controller.mm
[modify] https://crrev.com/9a85728692b46f719dd2b0df05da5fbce93c7880/ios/web/web_state/ui/crw_web_request_controller.mm
[modify] https://crrev.com/9a85728692b46f719dd2b0df05da5fbce93c7880/ios/web/web_state/web_state_observer_inttest.mm


### ad...@google.com (2020-03-04)

[Empty comment from Monorail migration]

### [Deleted User] (2020-05-06)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/1006012?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-03-19)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40050175)*
