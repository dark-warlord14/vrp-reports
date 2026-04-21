# Security: SameSite cookie bypass on Android by redirecting to to intent-picker

| Field | Value |
|-------|-------|
| **Issue ID** | [40061152](https://issues.chromium.org/issues/40061152) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Network>Cookies, Mobile>Intents |
| **Platforms** | Android |
| **Reporter** | ha...@gmail.com |
| **Assignee** | mt...@chromium.org |
| **Created** | 2022-09-26 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**  

Possible to bypass SameSite cookie on Android by redirecting to intent and continuing to stay in Chrome

**VERSION**  

Chrome Version: [105.0.5195.136] + [stable]  

Operating System: [Android 11; Samsung]

Note that I am using a Samsung for this. You must have already have a 2nd browser installed on your Android (in many phones Samsung browser is already installed.) If you are using emulator, you must install Firefox, and change the intent in package parameter in poc.py to point to org.mozilla.firefox.

**REPRODUCTION CASE**

1. Start webserver using python3 poc.py
2. Visit the webserver, click on (1) to set a samesite=strict cookie
3. Click on (2) to verify that the samesite=strict cookie is not set (Cookie header should not show up.)
4. Now, go to the address bar and append /redirect to the current URL, click continue in Chrome. We get redirected cross-site, but we are still sending the samesite=strict cookie.

Expected behaviour: SameSite=Strict cookie should not be sent cross-site (from our redirector site to httpbin.org)

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: Axel Chong

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 174 B)
- deleted (application/octet-stream, 0 B)
- [poc.py](attachments/poc.py) (text/plain, 514 B)
- [mobizen_20220927_024004.mp4](attachments/mobizen_20220927_024004.mp4) (video/mp4, 4.3 MB)
- [poc.py](attachments/poc.py) (text/plain, 705 B)
- [mobizen_20220930_173415.mp4](attachments/mobizen_20220930_173415.mp4) (video/mp4, 9.2 MB)

## Timeline

### [Deleted User] (2022-09-26)

[Empty comment from Monorail migration]

### ha...@gmail.com (2022-09-26)

[Comment Deleted]

### ha...@gmail.com (2022-09-26)

An external browser is not needed. Amended poc.py

### ha...@gmail.com (2022-09-26)

video: no intent selection is required

### mp...@chromium.org (2022-09-29)

I don't have an Android to reproduce, but it seems Android Chrome is treating intents like top-level user-initiated navigations rather than like normal redirects, at least if the intent is redirected to.

[Monorail components: Internals>Network>Cookies Mobile>Intents]

### mp...@chromium.org (2022-09-29)

Lowering severity to medium to match other SameSite=Strict bypasses.

### [Deleted User] (2022-09-29)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-29)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@gmail.com (2022-09-30)

Actually, I found out that even with normal redirects, SameSite cookie is sent, on default Chrome - https://bugs.chromium.org/p/chromium/issues/detail?id=1221316 (this is quite confusing actually, because I remembered it being fixed in this security report - https://bugs.chromium.org/p/chromium/issues/detail?id=830101, but it seems that it was disabled again). 

However, the secure SameSite behaviour can be enabled on Chrome via a feature flag hidden in chrome://flags > #enable-experimental-cookie-features. When this flag is enabled, then Chrome will not send the cookie on normal redirects, BUT it will still send the cookie for self-intent redirects. I have attached a modified poc.py along with the following STR:

0. On Android, Go to chrome://flags > Enable experimental cookie features
1. Start webserver using python3 poc.py
2. Visit the webserver, click on (1) to set a samesite=strict cookie
3. Click on (2) to verify that the samesite=strict cookie is not set (Cookie header should not show up.)
4. Now, go to the address bar and append /redirect-normal to the current URL, click continue in Chrome. We get redirected cross-site, but we do not send the SameSite cookie due to the feature flag being enabled (no cookie header)
5. Now, go to the address bar and append /redirect-intent to the current URL, click continue in Chrome. We get redirected cross-site, but we are still sending the samesite=strict cookie. (This case is not fixed with the feature flag.)

Given that https://bugs.chromium.org/p/chromium/issues/detail?id=1221316 will eventually be re-enabled. This should also be fixed in tandem. There should also be no breaking changes to worry about because only an attacker will use a self-intent to bypass security restrictions for navigations in Chrome.

### ha...@gmail.com (2022-09-30)

new video showing that intent URLs still send samesite cookie even after feature flag enabled (remove previously attached video to not clutter up space)

### mt...@chromium.org (2022-10-04)

Somebody familiar with cookies should triage this.

As for the intent picker issues, just to add some context on how this works, when we handle a fallback URL or a self-intent, we do a top-level navigation in a new tab and set the initiatorOrigin to the origin that sent the navigation. I have no idea what the expected behavior is or where we might be going wrong here.

### ha...@gmail.com (2022-10-04)

Maybe owner of https://bugs.chromium.org/p/chromium/issues/detail?id=1221316 can triage this?

### mt...@chromium.org (2022-10-04)

[Empty comment from Monorail migration]

### ha...@gmail.com (2022-10-04)

After reading https://bugs.chromium.org/p/chromium/issues/detail?id=830101, afaict this is whats happening (from my understanding of SameSite and redirector chains when flag is enabled)

1. Secure samesite cookie behaviour + normal redirect (w/ flag enabled)

None (entered in omnibox) -> http://attacker.site (redirector origin) -> http://httpbin.org (SameSite cookie not sent w/ flag enabled as origin 2 =/= origin 3)

2. Secure samesite cookie behaviour + intent redirect (w/ flag enabled)

None (entered in omnibox) -> ??? (redirector origin) -> http://httpbin.org (SameSite cookie sent???)

So the problem lies whether the origin that redirects to intent fills in the ??? and what value it fills in the redirect chain? (correct me if I am wrong)

### ha...@gmail.com (2022-10-04)

Hi mthiesse@, I have done some additional test and am fairly confident that the root cause is that the a redirection to an intent is not populating the origin correctly

If you were to go from Site A -> Site B (redirector) -> Site A normally this is what happens:

http://sitea.com -> http://siteb.com (normal redirection) --> http://sitea.com

This request has Sec-Fetch-Site of cross-site because the siteb.com =/= sitea.com

However if you were to redirected to an intent, lets say

http://sitea.com -> http://siteb.com (intent redirection) --> http://sitea.com

Then this request erroneously has Sec-Fetch-Site of same-origin even when siteb.com =/= sitea.com. 

My guess is that the whenever redirected to an intent it doesn't populate the origin. So origin remains null. Could you verify this @mthiesse?

This is a Sec-Fetch-Site bypass too (see https://www.w3.org/TR/fetch-metadata/#redirects of the Sec-Fetch-Site spec), but the fix here is probably the same (Populate the populator origin on an redirection to an intent)

### mt...@chromium.org (2022-10-04)

Hmm that doesn't seem to be the problem. I tried with with https://example.com -> https://mthiesse-test.glitch.me/redirect-to-chrome.html (intent) -> https://www.google.ca

The initiatorOrigin on the navigation to google.ca is (correctly?) set to mthiesse-test.glitch.me.

### ha...@gmail.com (2022-10-04)

Think it only works with Location header.

I set two glitch.me sites for you to more accurately test.

The redirector chain is:
https://morning-vivid-owner.glitch.me --> https://reminiscent-copper-crowd.glitch.me --> https://morning-vivid-owner.glitch.me

Note the same-origin value returned for sec-fetch-site which is not supposed to happen because of https://www.w3.org/TR/fetch-metadata/#redirects.

### ha...@gmail.com (2022-10-04)

[Comment Deleted]

### ha...@gmail.com (2022-10-04)

Go to https://morning-vivid-owner.glitch.me/poc-53aevgh, click on test and see the above occuring.

### ha...@gmail.com (2022-10-04)

I can confirm that only works with Location header (if you repeat the above with the location.href it correctly sends Sec-Fetch-Site of cross-site). So basically, 302 redirect to intent does not correctly populate the origin.

### [Deleted User] (2022-10-04)

[Empty comment from Monorail migration]

### mt...@chromium.org (2022-10-04)

[Empty comment from Monorail migration]

### mt...@chromium.org (2022-10-04)

I see sec-fetch-site: same-origin even though we're setting the initiator origin on the intent, and on the subsequent navigation from the intent the initiator origin is set to morning-vivid-owner.glitch.me

### mt...@chromium.org (2022-10-04)

Oh wait, that may be the bug - the initiator origin should be set to reminiscent-copper-crowd.glitch.me for that navigation.

If that's true, then the bug happens before any Intent processing/external navigation happens.

### mt...@chromium.org (2022-10-04)

Here are some logs that may make things a little clearer:
cr_UrlHandler: shouldOverrideUrlLoading called on https://morning-vivid-owner.glitch.me/poc-53aevgh
cr_UrlHandler: Browser initiated navigation chain.
cr_UrlHandler: shouldOverrideUrlLoading result: NO_OVERRIDE
cr_UrlHandler: shouldOverrideUrlLoading called on https://reminiscent-copper-crowd.glitch.me/redirect-aex457d
cr_UrlHandler: No specialized handler for URL
cr_UrlHandler: shouldOverrideUrlLoading result: NO_OVERRIDE
cr_UrlHandler: shouldOverrideUrlLoading called on intent://morning-vivid-owner.glitch.me/headers#Intent;scheme=https;package=com.android.chrome;end
cr_UrlHandler: Initiator origin host: morning-vivid-owner.glitch.me


### ha...@gmail.com (2022-10-04)

Yes, the initiator origin should be set to reminiscent-copper-crowd.glitch.me,

Now the chain is: https://morning-vivid-owner.glitch.me/headers -> https://morning-vivid-owner.glitch.me/headers, which is incorrect and probably explain both bugs.

I updated the https://morning-vivid-owner.glitch.me/poc-53aevgh with a new link named "normal" which should correctly show sec-fetch-site cross-site. So somethig went wrong with handling the initiatorOrigin for intent redirection if normal redirects work correctly.

### ha...@gmail.com (2022-10-04)

Also updated https://morning-vivid-owner.glitch.me/poc-53aevgh with a new link named "test-redirect-to-other", which is a intent redirection to example.com, this help determine if the initiatorOrigin determined from the previous https://morning-vivid-owner.glitch.me origin or the next http://example.com origin in the chain. If its the former, perhaps the initiator origin is only set for intents if a document body exists and in this case is incorrectly reusing the previous origin in the navigation chain to determine the current origin? As elaborated in https://crbug.com/chromium/1368230#c26, this problem is exclusive to intents as normal redirects work as intended (you can test by clicking the "normal" link in https://morning-vivid-owner.glitch.me/poc-53aevgh)

### mt...@chromium.org (2022-10-04)

Ah, found the bug, patch coming soon.

### mt...@chromium.org (2022-10-04)

Fix: https://chromium-review.googlesource.com/c/chromium/src/+/3925673

### mt...@chromium.org (2022-10-05)

Nevermind, my fix was wrong - not sure what tricked me into thinking it fixes the issue, but it doesn't.

The bug might have something to do with intent navigation not preserving the redirect chain? If the initiator origin is constant, I don't know what it is that we look at to determing if a redirect was cross-site.

### mt...@chromium.org (2022-10-05)

[Empty comment from Monorail migration]

### mt...@chromium.org (2022-10-05)

Actually yeah, it does look like the missing redirect chain would be at fault here: https://source.chromium.org/chromium/chromium/src/+/main:services/network/sec_header_helpers.cc;drc=8d399817282e3c12ed54eb23ec42a5e418298ec6;l=107

We could probably hack in a fix for that, but maybe the problem here is more fundamental?

It feels problematic that when we redirect to an app that the app can send the intent back to Chrome with an arbitrary URL on it, and the initiatorOrigin will be whatever origin sent the initial request that got redirected, not whichever origin sent the intent redirect, without any of the other information that would exist on the NavigationHandle, like the redirect chain or the SiteInstance, etc.

Thoughts?

### bi...@chromium.org (2022-10-05)

To make sure I understand this bug, is the situation that

A.com -(intent redirect)-> B.com 

results in B.com being sent its SameSite cookies?

It seems safest to me that if we're navigating from an intent redirect to always assume cross-site. Which in this case would result in SameSite cookies not being sent. Implementation wise this would probably look like using an opaque origin as the initiator.

In any case, it seems to me that the cookie code is performing correctly* with the information being given to it. It's just the information isn't correct.

* Relatedly, it's known that normal redirections can result in SameSite cookies being sent. This is something we're working on fixing
E.x.:
A.com --> B.com --> A.com
The final A.com will receive all its SameSite cookies even though we redirected through a different site.

### mt...@chromium.org (2022-10-05)

No, the situation is A.com -> B.com (uncommitted) -> (30x intent redirect) -> A.com.

We should be careful not to break the fixes for https://crbug.com/chromium/1092451 and https://crbug.com/chromium/1092025, which is why we initially started tracking the initiatorOrigin through intents.

However, it looks to me like it would be fine to just use an opaque origin as the initiator - I think the important part is we need to be sure not to leave the initiatorOrigin unset, as we treat navigations without an initiator as higher trust and coming from the browser IIRC.

### ha...@gmail.com (2022-10-05)

bingler@ for https://crbug.com/chromium/1368230#c33, this report is about a bypass even when cookie feature flag is enabled. It is also a sec-fetch-site bypass

### ha...@gmail.com (2022-10-06)

Regarding https://crbug.com/chromium/1368230#c33 and https://crbug.com/chromium/1368230#c34, I also don't see any problems with automatically treating any navigation containing intent URL as cross-site (for both sec-fetch-site and samesite cookies). It is abnormal for a site to do a 302 redirect to a self-intent which opens in the first place.

### mt...@chromium.org (2022-10-06)

One last question - should we be using an opaque initiator for all intents Chrome receives, or just the ones that come from websites? We generally trust other installed apps slightly more than we trust the web, but maybe it would be best if all intents were treated with less trust.

(I don't know in practice how much we privilege navigations without an initiatorOrigin, but given past bugs we clearly do to some extent)

### ha...@gmail.com (2022-10-06)

If you are asking me, I am unfamiliar with the security model for Android apps so am unsure. But I think treating an open intent from an external app as untrusted may cause some breaking change if an external app decides to launch a user to a site while expecting them to be authenticated via the browser application instead of a webview (due samesite cookie not being sent.) 

But again, am unsure of security model revolving around external apps.

### mt...@chromium.org (2022-10-06)

Haha sorry, the question was more directed at bingler@, but your response is helpful.

The problem with Android's app security model is we can't know the sender of intent, so we have no idea whether an association between the target website and the sending app exist.

I must admit after some reading I still have no idea how SameSite cookies are supposed to work in this context, so I'm counting on the navigation folks to guide me here.

Maybe the solution is when a website sends an intent back to Chrome we should use an opaque origin, but when an app sends an intent to Chrome we should use the origin of the target URL as the initiator so it doesn't look browser initiated but still gets SameSite cookies? Maybe only CCTs where we have a known association with an app should get SameSite cookies from an Intent? Or maybe intents looking browser initiated is totally fine and my concerns are unfounded?

### bi...@chromium.org (2022-10-06)

As far as cookies are concerned, we don't want to send SameSite=Strict cookies unless we're confident that the request came from the same site (or something of equivalent trust). Since coming from an intent isn't necessarily same-site I'm on the side of disallowing them in that case. 

But if we do allow Android apps some extra amount of trust then perhaps it's ok to loosen those restrictions in that case. I don't think I can make that call.

rsesek@, do you have any thoughts?



### [Deleted User] (2022-10-11)

rsesek: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rs...@chromium.org (2022-10-14)

We should not trust data from incoming Intents, both because (a) other apps on the device may not be trustworthy, and (b) websites can use Intent URLs/redirects to reflect back to Chrome and potentially use it to bypass SameSite restrictions. I don’t know if imposing this restriction will break anything, but I think we should try.

### bi...@chromium.org (2022-10-14)

[Empty comment from Monorail migration]

### mt...@chromium.org (2022-10-17)

Sounds good, I'll try making the change initially for non-CCTs and see if anything breaks, then we can tackle CCTs separately which are more likely to require things like samesite cookies for login flows (I assume?).

### ha...@gmail.com (2022-10-17)

Note to test if the fix works  
for samesite cookies you must enable feature flag hidden in chrome://flags > #enable-experimental-cookie-features as elaborated in https://crbug.com/chromium/1368230#c9. 

You may also test using sec fetch site in https://crbug.com/chromium/1368230#c27 which is likely another problem present due to incorrect propagation of the origin. The value of sec fetch site for a

A->B->A case

Must be cross-site due to https://www.w3.org/TR/fetch-metadata/#redirects

### [Deleted User] (2022-10-31)

mthiesse: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-11-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/91a950425330f85bab107b381021aab79d2a8709

commit 91a950425330f85bab107b381021aab79d2a8709
Author: Michael Thiessen <mthiesse@chromium.org>
Date: Tue Nov 01 15:38:36 2022

Use opaque origin for incoming Intent navigations.

Bug: 1368230
Change-Id: I392659173b0055ff01f6be84ebd5c4ff29d61fa0
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3966130
Reviewed-by: Robert Sesek <rsesek@chromium.org>
Commit-Queue: Michael Thiessen <mthiesse@chromium.org>
Reviewed-by: Yaron Friedman <yfriedman@chromium.org>
Reviewed-by: Clark DuVall <cduvall@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1065949}

[modify] https://crrev.com/91a950425330f85bab107b381021aab79d2a8709/chrome/android/java/src/org/chromium/chrome/browser/IntentHandler.java
[modify] https://crrev.com/91a950425330f85bab107b381021aab79d2a8709/components/external_intents/android/java/src/org/chromium/components/external_intents/ExternalNavigationHandler.java
[modify] https://crrev.com/91a950425330f85bab107b381021aab79d2a8709/weblayer/browser/java/org/chromium/weblayer_private/ExternalNavigationDelegateImpl.java
[modify] https://crrev.com/91a950425330f85bab107b381021aab79d2a8709/chrome/android/javatests/src/org/chromium/chrome/browser/IntentHandlerUnitTest.java
[modify] https://crrev.com/91a950425330f85bab107b381021aab79d2a8709/components/external_intents/android/java/src/org/chromium/components/external_intents/ExternalNavigationDelegate.java
[modify] https://crrev.com/91a950425330f85bab107b381021aab79d2a8709/chrome/android/java/src/org/chromium/chrome/browser/externalnav/ExternalNavigationDelegateImpl.java
[modify] https://crrev.com/91a950425330f85bab107b381021aab79d2a8709/chrome/browser/flags/android/chrome_feature_list.h
[modify] https://crrev.com/91a950425330f85bab107b381021aab79d2a8709/chrome/android/javatests/src/org/chromium/chrome/browser/externalnav/ExternalNavigationDelegateImplTest.java
[modify] https://crrev.com/91a950425330f85bab107b381021aab79d2a8709/components/external_intents/android/javatests/src/org/chromium/components/external_intents/ExternalNavigationHandlerTest.java
[modify] https://crrev.com/91a950425330f85bab107b381021aab79d2a8709/chrome/android/java/src/org/chromium/chrome/browser/externalnav/IntentWithRequestMetadataHandler.java
[modify] https://crrev.com/91a950425330f85bab107b381021aab79d2a8709/chrome/browser/flags/android/java/src/org/chromium/chrome/browser/flags/ChromeFeatureList.java
[modify] https://crrev.com/91a950425330f85bab107b381021aab79d2a8709/chrome/browser/flags/android/chrome_feature_list.cc
[modify] https://crrev.com/91a950425330f85bab107b381021aab79d2a8709/chrome/android/javatests/src/org/chromium/chrome/browser/externalnav/IntentWithRequestMetadataHandlerTest.java


### ha...@gmail.com (2022-11-03)

Hi, I can confirm the fix works for both sec-fetch-site and samesite cookie on 109.0.5397.0 Android Chrome Canary.

For samesite, following steps in https://crbug.com/chromium/1368230#c9 will no longer send the cookie,

For sec-fetch-site, using https://morning-vivid-owner.glitch.me/poc-53aevgh and clicking on the link called test > click on chrome canary on intent-picker, will result in cross-site being sent for sec-fetch-site value.

### mt...@chromium.org (2022-11-03)

Thanks for the confirmation. Note that I still need to fix this issue for Chrome Custom Tabs.

### gi...@appspot.gserviceaccount.com (2022-11-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/17de49605ad55134f155c94af7155f0968c15f11

commit 17de49605ad55134f155c94af7155f0968c15f11
Author: Michael Thiessen <mthiesse@chromium.org>
Date: Tue Nov 15 16:51:57 2022

Use an opaque initiator for intents to CCTs

Bug: 1368230
Change-Id: Ia7c70f27e523be50b98078335c6ac91dae55e828
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4021621
Commit-Queue: Michael Thiessen <mthiesse@chromium.org>
Reviewed-by: Ella Ge <eirage@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1071653}

[modify] https://crrev.com/17de49605ad55134f155c94af7155f0968c15f11/chrome/android/junit/src/org/chromium/chrome/browser/customtabs/content/CustomTabActivityUrlLoadingTest.java
[modify] https://crrev.com/17de49605ad55134f155c94af7155f0968c15f11/chrome/android/java/src/org/chromium/chrome/browser/customtabs/HiddenTabHolder.java
[modify] https://crrev.com/17de49605ad55134f155c94af7155f0968c15f11/chrome/android/java/src/org/chromium/chrome/browser/customtabs/content/CustomTabActivityNavigationController.java
[modify] https://crrev.com/17de49605ad55134f155c94af7155f0968c15f11/chrome/android/javatests/src/org/chromium/chrome/browser/customtabs/CustomTabActivityTest.java


### mt...@chromium.org (2022-11-15)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-15)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-15)

[Empty comment from Monorail migration]

### ad...@chromium.org (2022-11-22)

[Empty comment from Monorail migration]

### am...@google.com (2022-12-02)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-12-02)

Congratulations, Axel! The VRP Panel has decided to award you $5,000 for this report. Thank you for your efforts in discovering and reporting this issue to us -- nice work! 

### am...@google.com (2022-12-05)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-01-09)

https://crrev.com/c/3966130  (the fix specific to CCT) and was not backmerged to M109 (the original fix was landed on 109), so not updating this fix as shipping in M109 release tomorrow. If possible, please let's consider backmerge CCT-specific fix backmerged to M109 so this issue can be fixed in M109 respin. Adding manual merge request label so that this can get into the merge review queue. 

### [Deleted User] (2023-01-09)

Merge review required: M109 has already been cut for stable release.

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
Owners: govind (Android), eakpobaro (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-01-11)

please merge https://crrev.com/c/3966130 to m109, branch 5414 so the CCT related fix can be included with the general fix in M109/Stable  

### mt...@chromium.org (2023-01-11)

I assume you mean https://crrev.com/c/4021621, as 3966130 is the first CL which is already in 109.

### gi...@appspot.gserviceaccount.com (2023-01-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/e8feb6f4a58097d79b4fc70cacc7f403eed92d0a

commit e8feb6f4a58097d79b4fc70cacc7f403eed92d0a
Author: Michael Thiessen <mthiesse@chromium.org>
Date: Wed Jan 11 23:15:43 2023

Use an opaque initiator for intents to CCTs

(cherry picked from commit 17de49605ad55134f155c94af7155f0968c15f11)

Bug: 1368230
Change-Id: Ia7c70f27e523be50b98078335c6ac91dae55e828
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4021621
Commit-Queue: Michael Thiessen <mthiesse@chromium.org>
Reviewed-by: Ella Ge <eirage@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1071653}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4156856
Commit-Queue: Ella Ge <eirage@chromium.org>
Auto-Submit: Michael Thiessen <mthiesse@chromium.org>
Cr-Commit-Position: refs/branch-heads/5414@{#1347}
Cr-Branched-From: 4417ee59d7bf6df7a9c9ea28f7722d2ee6203413-refs/heads/main@{#1070088}

[modify] https://crrev.com/e8feb6f4a58097d79b4fc70cacc7f403eed92d0a/chrome/android/junit/src/org/chromium/chrome/browser/customtabs/content/CustomTabActivityUrlLoadingTest.java
[modify] https://crrev.com/e8feb6f4a58097d79b4fc70cacc7f403eed92d0a/chrome/android/java/src/org/chromium/chrome/browser/customtabs/content/CustomTabActivityNavigationController.java
[modify] https://crrev.com/e8feb6f4a58097d79b4fc70cacc7f403eed92d0a/chrome/android/java/src/org/chromium/chrome/browser/customtabs/HiddenTabHolder.java
[modify] https://crrev.com/e8feb6f4a58097d79b4fc70cacc7f403eed92d0a/chrome/android/javatests/src/org/chromium/chrome/browser/customtabs/CustomTabActivityTest.java


### [Deleted User] (2023-02-21)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2023-02-28)

[Empty comment from Monorail migration]

### pg...@google.com (2023-02-28)

[Empty comment from Monorail migration]

### pg...@google.com (2023-02-28)

looks like our automation process missed this bug! sorry about that - we will get this fixed!

### [Deleted User] (2023-02-28)

The older reward-topanel https://crbug.com/chromium/1334240 has been merged into this one. Please manually review this issue to see if the duplicate is potentially eligible for a reward.



### am...@chromium.org (2023-03-15)

[Empty comment from Monorail migration]

### pg...@google.com (2023-07-21)

[Empty comment from Monorail migration]

### pg...@google.com (2023-07-28)

[Empty comment from Monorail migration]

### pg...@google.com (2023-07-28)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-09-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/3ff479e9577a63690ee51de660ee18ac0a13f4ad

commit 3ff479e9577a63690ee51de660ee18ac0a13f4ad
Author: Michael Thiessen <mthiesse@chromium.org>
Date: Thu Sep 28 14:44:19 2023

Clean up OpaqueOriginForIncomingIntents

Kill switch shipped a year ago, safe to remove.

Bug: 1368230
Change-Id: Ic1242461c6f758649ac97f1309071fa7546a6877
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4898798
Commit-Queue: Michael Thiessen <mthiesse@chromium.org>
Reviewed-by: Yaron Friedman <yfriedman@chromium.org>
Code-Coverage: findit-for-me@appspot.gserviceaccount.com <findit-for-me@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#1202616}

[modify] https://crrev.com/3ff479e9577a63690ee51de660ee18ac0a13f4ad/chrome/browser/flags/android/chrome_feature_list.h
[modify] https://crrev.com/3ff479e9577a63690ee51de660ee18ac0a13f4ad/chrome/android/java/src/org/chromium/chrome/browser/IntentHandler.java
[modify] https://crrev.com/3ff479e9577a63690ee51de660ee18ac0a13f4ad/chrome/android/junit/src/org/chromium/chrome/browser/customtabs/content/CustomTabActivityUrlLoadingTest.java
[modify] https://crrev.com/3ff479e9577a63690ee51de660ee18ac0a13f4ad/chrome/android/java/src/org/chromium/chrome/browser/customtabs/HiddenTabHolder.java
[modify] https://crrev.com/3ff479e9577a63690ee51de660ee18ac0a13f4ad/chrome/android/java/src/org/chromium/chrome/browser/customtabs/content/CustomTabActivityNavigationController.java
[modify] https://crrev.com/3ff479e9577a63690ee51de660ee18ac0a13f4ad/chrome/android/junit/src/org/chromium/chrome/browser/IntentHandlerRobolectricTest.java
[modify] https://crrev.com/3ff479e9577a63690ee51de660ee18ac0a13f4ad/chrome/browser/flags/android/java/src/org/chromium/chrome/browser/flags/ChromeFeatureList.java
[modify] https://crrev.com/3ff479e9577a63690ee51de660ee18ac0a13f4ad/chrome/browser/flags/android/chrome_feature_list.cc
[modify] https://crrev.com/3ff479e9577a63690ee51de660ee18ac0a13f4ad/chrome/android/javatests/src/org/chromium/chrome/browser/customtabs/CustomTabActivityTest.java


### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1368230?no_tracker_redirect=1

[Multiple monorail components: Internals>Network>Cookies, Mobile>Intents]
[Monorail mergedwith: crbug.com/chromium/1334240]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061152)*
