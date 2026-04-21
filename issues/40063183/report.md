# Security: Chrome on Android can self-intent into CCT, allowing sandboxed iframe allow-popups-to-escape-sandbox bypass.

| Field | Value |
|-------|-------|
| **Issue ID** | [40063183](https://issues.chromium.org/issues/40063183) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>SecurityFeature>IFrameSandbox, Mobile>Intents |
| **Platforms** | Android |
| **Reporter** | ha...@gmail.com |
| **Assignee** | mt...@chromium.org |
| **Created** | 2023-02-21 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

Chrome on Android can launch an intent to itself and open up a CCT. I would say that this would probably count as a popup.

However, an iframe sandbox with allow-popups but not allow-popups-to-escape-sandbox can self-intent into CCT on Chrome. This opens a popup (or a CCT) which is not sandboxed, allowing for downloads / script execution etc. Normally, an iframe sandbox with allow-popups set but not allow-popups-to-escape-sandbox will inherit the sandbox flags from the parent window (ref: <https://googlechrome.github.io/samples/allow-popups-to-escape-sandbox/>)

REPRODUCTION

1. With latest Chrome canary (a similar bug was fixed on Android and is awaiting merge to Stable - <https://crbug.com/chromium/1365100>) on Android head over to <https://elastic-nimble-elephant.glitch.me/iframe-test.html>
2. Click the link in iframe, CCT popup and you should get alert modal even when iframe sandbox allow-scripts / allow-modals unset.

Perhaps block Chrome from self-launching into a CCT?

iframe-test.html

```
<p>Intent CCT target=_blank </p>  
<iframe srcdoc="<a href='intent://elastic-nimble-elephant.glitch.me/execute-script.html#Intent;scheme=https;package=com.chrome.canary;S.android.support.customtabs.extra.SESSION=asdf;end' target=_blank>test</a>" sandbox="allow-popups"></iframe>  

```

execute-script.html

```
<script>alert(1)</script>  

```

**VERSION**  

Chrome Version: 112.0.5609.0 Canary  

Operating System: Android 13

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: Axel Chong

## Timeline

### [Deleted User] (2023-02-21)

[Empty comment from Monorail migration]

### sr...@google.com (2023-02-22)

mthiesse@ could you take a look at this?

Note that I didn't reproduce since I don't have an Android device + build environment available and the report sounds reasonable to me.

[Monorail components: Blink>SecurityFeature>IFrameSandbox Mobile>Intents]

### [Deleted User] (2023-02-22)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-22)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-02-22)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2023-02-22)

(I am a bot: this is an auto-cc on a security bug)

### mt...@chromium.org (2023-02-24)

> Perhaps block Chrome from self-launching into a CCT?
This is something I've wanted to do for a while, but I was worried about possibly breaking things without good reason. Maybe this is a good reason.

However, I'm very confused about how this wasn't fixed by https://chromium-review.googlesource.com/c/chromium/src/+/4174394 which prevents us from launching *anything* from our own package - including CCT.

Looking into it.

### ha...@gmail.com (2023-02-24)

The difference is that now it has the "_blank".

For normal intents (CCT not opened) I can confirm Chrome opens a new popup via _blank but it is correctly sandboxed in the popup.

### mt...@chromium.org (2023-02-24)

Ah yeah, when the navigation has a gesture and the subframe targets a new window, it's no longer considered a subframe navigation. This means we probably need to plumb whether the frame is sandboxed into Java and block the navigation for sandboxed main frames too.

### mt...@chromium.org (2023-02-24)

[Empty comment from Monorail migration]

### mt...@chromium.org (2023-02-24)

Note that we'll also have to disable fallback URLs for sandboxed main frames as we don't support carrying the sandbox attributes through fallback URLs in the main frame :/

### gi...@appspot.gserviceaccount.com (2023-03-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/8fd3520bac845685e87a7450ebbf9f868ff7197f

commit 8fd3520bac845685e87a7450ebbf9f868ff7197f
Author: Michael Thiessen <mthiesse@chromium.org>
Date: Fri Mar 10 20:55:47 2023

Block intents to self, and block fallback URLs in sandboxed main frames

Intents to self and main frame fallback URLs don't currently support
maintaining sandbox attributes. I've been wanting to block intents to
self for a while, and this seems like a good reason to finally do it -
we'll instead just load the intent's target URL in the browser (unless
the frame is sandboxed, in which case we just block the navigation).

This is guarded by a kill switch in case we find that important use
cases are relying on intenting to the current browser (which would be
very weird).

Bug: 1418061
Change-Id: Iaa836be3783122ba6d3fa286bfbf131b0b5cf494
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4294954
Reviewed-by: Alex Moshchuk <alexmos@chromium.org>
Reviewed-by: Arthur Sonzogni <arthursonzogni@chromium.org>
Commit-Queue: Michael Thiessen <mthiesse@chromium.org>
Code-Coverage: Findit <findit-for-me@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#1115894}

[modify] https://crrev.com/8fd3520bac845685e87a7450ebbf9f868ff7197f/android_webview/java/src/org/chromium/android_webview/AwContents.java
[add] https://crrev.com/8fd3520bac845685e87a7450ebbf9f868ff7197f/chrome/test/data/android/url_overriding/subframe_navigation_child_blank.html
[modify] https://crrev.com/8fd3520bac845685e87a7450ebbf9f868ff7197f/chrome/android/java/src/org/chromium/chrome/browser/dom_distiller/ReaderModeManager.java
[modify] https://crrev.com/8fd3520bac845685e87a7450ebbf9f868ff7197f/components/external_intents/android/java/src/org/chromium/components/external_intents/ExternalIntentsFeatures.java
[modify] https://crrev.com/8fd3520bac845685e87a7450ebbf9f868ff7197f/components/navigation_interception/android/java/src/org/chromium/components/navigation_interception/InterceptNavigationDelegate.java
[modify] https://crrev.com/8fd3520bac845685e87a7450ebbf9f868ff7197f/components/external_intents/android/external_intents_features.h
[modify] https://crrev.com/8fd3520bac845685e87a7450ebbf9f868ff7197f/components/external_intents/android/java/src/org/chromium/components/external_intents/ExternalNavigationHandler.java
[modify] https://crrev.com/8fd3520bac845685e87a7450ebbf9f868ff7197f/chrome/android/javatests/src/org/chromium/chrome/browser/tab/InterceptNavigationDelegateTest.java
[add] https://crrev.com/8fd3520bac845685e87a7450ebbf9f868ff7197f/chrome/test/data/android/url_overriding/subframe_navigation_parent_sandbox.html
[modify] https://crrev.com/8fd3520bac845685e87a7450ebbf9f868ff7197f/components/external_intents/android/external_intents_features.cc
[modify] https://crrev.com/8fd3520bac845685e87a7450ebbf9f868ff7197f/content/browser/renderer_host/navigation_request.h
[modify] https://crrev.com/8fd3520bac845685e87a7450ebbf9f868ff7197f/chrome/android/javatests/src/org/chromium/chrome/browser/customtabs/CustomTabExternalNavigationTest.java
[modify] https://crrev.com/8fd3520bac845685e87a7450ebbf9f868ff7197f/chrome/test/data/android/url_overriding/subframe_navigation_parent.html
[modify] https://crrev.com/8fd3520bac845685e87a7450ebbf9f868ff7197f/components/external_intents/android/javatests/src/org/chromium/components/external_intents/ExternalNavigationHandlerTest.java
[modify] https://crrev.com/8fd3520bac845685e87a7450ebbf9f868ff7197f/content/public/test/mock_navigation_handle.h
[modify] https://crrev.com/8fd3520bac845685e87a7450ebbf9f868ff7197f/chrome/android/java/src/org/chromium/chrome/browser/compositor/bottombar/OverlayPanelContent.java
[modify] https://crrev.com/8fd3520bac845685e87a7450ebbf9f868ff7197f/components/external_intents/android/java/src/org/chromium/components/external_intents/ExternalNavigationParams.java
[modify] https://crrev.com/8fd3520bac845685e87a7450ebbf9f868ff7197f/content/browser/renderer_host/navigation_request.cc
[modify] https://crrev.com/8fd3520bac845685e87a7450ebbf9f868ff7197f/components/navigation_interception/intercept_navigation_delegate.cc
[modify] https://crrev.com/8fd3520bac845685e87a7450ebbf9f868ff7197f/chrome/android/javatests/src/org/chromium/chrome/browser/contextualsearch/ContextualSearchManagerTest.java
[modify] https://crrev.com/8fd3520bac845685e87a7450ebbf9f868ff7197f/chrome/android/javatests/src/org/chromium/chrome/browser/externalnav/UrlOverridingTest.java
[modify] https://crrev.com/8fd3520bac845685e87a7450ebbf9f868ff7197f/content/public/browser/navigation_handle.h
[modify] https://crrev.com/8fd3520bac845685e87a7450ebbf9f868ff7197f/components/external_intents/android/java/src/org/chromium/components/external_intents/InterceptNavigationDelegateImpl.java


### mt...@chromium.org (2023-03-13)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-13)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-13)

[Empty comment from Monorail migration]

### am...@google.com (2023-03-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-03-17)

Congratulations, Axel! The VRP Panel has decided to award you $1,000 for this report. Thank you for reporting follow-on issue to us! 

### mt...@chromium.org (2023-03-17)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-17)

Merge review required: M112 is already shipping to beta.

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
Owners: govind (Android), govind (iOS), obenedict (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mt...@chromium.org (2023-03-17)

This has had time to bake on Canary, and we've got a kill switch in place for if things go wrong. Given it's a medium security bug, we should probably try to get this into 112.

### am...@google.com (2023-03-17)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-03-20)

Based on this size of this change and that it is for Android, I was not originally planning on backmerging this fix; so thank you for the information about the kill switch mthiesse@ 

M112 merge approved, please merge to branch 5615 at your earliest convenience 

### go...@chromium.org (2023-03-21)

Please merge your change to M112 by 2:00 PM PT Tuesday, 03/21 so we can take it in for this week's beta release. 

Branch Details: https://chromiumdash.appspot.com/branches

### go...@chromium.org (2023-03-21)

Please merge your change to M112 by 2:00 PM PT Today, 03/21 so we can take it in for this week's beta release. 

Branch Details: https://chromiumdash.appspot.com/branches

### gi...@appspot.gserviceaccount.com (2023-03-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/909ce8710aaf0b886597d20972c949a722106384

commit 909ce8710aaf0b886597d20972c949a722106384
Author: Michael Thiessen <mthiesse@chromium.org>
Date: Tue Mar 21 16:27:21 2023

Block intents to self, and block fallback URLs in sandboxed main frames

Intents to self and main frame fallback URLs don't currently support
maintaining sandbox attributes. I've been wanting to block intents to
self for a while, and this seems like a good reason to finally do it -
we'll instead just load the intent's target URL in the browser (unless
the frame is sandboxed, in which case we just block the navigation).

This is guarded by a kill switch in case we find that important use
cases are relying on intenting to the current browser (which would be
very weird).

(cherry picked from commit 8fd3520bac845685e87a7450ebbf9f868ff7197f)

Bug: 1418061
Change-Id: Iaa836be3783122ba6d3fa286bfbf131b0b5cf494
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4294954
Reviewed-by: Alex Moshchuk <alexmos@chromium.org>
Reviewed-by: Arthur Sonzogni <arthursonzogni@chromium.org>
Commit-Queue: Michael Thiessen <mthiesse@chromium.org>
Code-Coverage: Findit <findit-for-me@appspot.gserviceaccount.com>
Cr-Original-Commit-Position: refs/heads/main@{#1115894}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4358250
Reviewed-by: Yaron Friedman <yfriedman@chromium.org>
Reviewed-by: Bo Liu <boliu@chromium.org>
Cr-Commit-Position: refs/branch-heads/5615@{#706}
Cr-Branched-From: 9c6408ef696e83a9936b82bbead3d41c93c82ee4-refs/heads/main@{#1109224}

[add] https://crrev.com/909ce8710aaf0b886597d20972c949a722106384/chrome/test/data/android/url_overriding/subframe_navigation_child_blank.html
[modify] https://crrev.com/909ce8710aaf0b886597d20972c949a722106384/android_webview/java/src/org/chromium/android_webview/AwContents.java
[modify] https://crrev.com/909ce8710aaf0b886597d20972c949a722106384/components/navigation_interception/android/java/src/org/chromium/components/navigation_interception/InterceptNavigationDelegate.java
[modify] https://crrev.com/909ce8710aaf0b886597d20972c949a722106384/chrome/android/java/src/org/chromium/chrome/browser/dom_distiller/ReaderModeManager.java
[modify] https://crrev.com/909ce8710aaf0b886597d20972c949a722106384/components/external_intents/android/java/src/org/chromium/components/external_intents/ExternalIntentsFeatures.java
[modify] https://crrev.com/909ce8710aaf0b886597d20972c949a722106384/components/external_intents/android/java/src/org/chromium/components/external_intents/ExternalNavigationHandler.java
[modify] https://crrev.com/909ce8710aaf0b886597d20972c949a722106384/components/external_intents/android/external_intents_features.h
[modify] https://crrev.com/909ce8710aaf0b886597d20972c949a722106384/components/external_intents/android/external_intents_features.cc
[modify] https://crrev.com/909ce8710aaf0b886597d20972c949a722106384/chrome/android/javatests/src/org/chromium/chrome/browser/tab/InterceptNavigationDelegateTest.java
[add] https://crrev.com/909ce8710aaf0b886597d20972c949a722106384/chrome/test/data/android/url_overriding/subframe_navigation_parent_sandbox.html
[modify] https://crrev.com/909ce8710aaf0b886597d20972c949a722106384/content/browser/renderer_host/navigation_request.h
[modify] https://crrev.com/909ce8710aaf0b886597d20972c949a722106384/chrome/android/javatests/src/org/chromium/chrome/browser/customtabs/CustomTabExternalNavigationTest.java
[modify] https://crrev.com/909ce8710aaf0b886597d20972c949a722106384/chrome/test/data/android/url_overriding/subframe_navigation_parent.html
[modify] https://crrev.com/909ce8710aaf0b886597d20972c949a722106384/components/external_intents/android/javatests/src/org/chromium/components/external_intents/ExternalNavigationHandlerTest.java
[modify] https://crrev.com/909ce8710aaf0b886597d20972c949a722106384/content/public/test/mock_navigation_handle.h
[modify] https://crrev.com/909ce8710aaf0b886597d20972c949a722106384/components/external_intents/android/java/src/org/chromium/components/external_intents/ExternalNavigationParams.java
[modify] https://crrev.com/909ce8710aaf0b886597d20972c949a722106384/chrome/android/java/src/org/chromium/chrome/browser/compositor/bottombar/OverlayPanelContent.java
[modify] https://crrev.com/909ce8710aaf0b886597d20972c949a722106384/content/browser/renderer_host/navigation_request.cc
[modify] https://crrev.com/909ce8710aaf0b886597d20972c949a722106384/components/navigation_interception/intercept_navigation_delegate.cc
[modify] https://crrev.com/909ce8710aaf0b886597d20972c949a722106384/content/public/browser/navigation_handle.h
[modify] https://crrev.com/909ce8710aaf0b886597d20972c949a722106384/chrome/android/javatests/src/org/chromium/chrome/browser/contextualsearch/ContextualSearchManagerTest.java
[modify] https://crrev.com/909ce8710aaf0b886597d20972c949a722106384/chrome/android/javatests/src/org/chromium/chrome/browser/externalnav/UrlOverridingTest.java
[modify] https://crrev.com/909ce8710aaf0b886597d20972c949a722106384/components/external_intents/android/java/src/org/chromium/components/external_intents/InterceptNavigationDelegateImpl.java


### am...@chromium.org (2023-03-31)

[Empty comment from Monorail migration]

### pg...@google.com (2023-04-04)

[Empty comment from Monorail migration]

### pg...@google.com (2023-04-04)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-19)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1418061?no_tracker_redirect=1

[Multiple monorail components: Blink>SecurityFeature>IFrameSandbox, Mobile>Intents]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40063183)*
