# Security: Intent URLs also bypass CSP sandbox with "allow-popups" set

| Field | Value |
|-------|-------|
| **Issue ID** | [40063634](https://issues.chromium.org/issues/40063634) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>SecurityFeature, Mobile>Intents |
| **Platforms** | Android |
| **Reporter** | ha...@gmail.com |
| **Assignee** | ar...@chromium.org |
| **Created** | 2023-03-17 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

I noticed from comment in <https://chromium-review.googlesource.com/c/chromium/src/+/4294954> someone mentioned something about CSP sandbox. While testing the fix for the bugs 1365100, 1418061, I found that CSP sandbox can also be bypassed.

For context, the intended behaviour is that sandboxed content with allow-popups shouldn't cause the popup to escape sandbox. Here, a page on Android with CSP sandbox with "allow-popups" but no "allow-downloads" can initiate a download.

**VERSION**  

Chrome Version: 113.0.5656.0 (Canary which includes the fix for 1365100, 1418061)  

Operating System: Android 13

**REPRODUCTION CASE**  

I have made a site <https://fabulous-woozy-magic.glitch.me/csp.html> for you to test (though it would be hard to inspect the headers on Android, you can inspect it on Desktop however).

I have also attached a Python POC that essentially does the same thing.

By clicking the link in either, a download is initiated (it just downloads the HSTS preload list from <https://github.com/chromium/hstspreload.org/tags>) without allow-downloads set in CSP sandbox (<script>alert(1)</script> is just to verify that the CSP sandbox works correctly, by correctly blocking it.)

## Attachments

- [csp.py](attachments/csp.py) (text/plain, 561 B)

## Timeline

### [Deleted User] (2023-03-17)

[Empty comment from Monorail migration]

### ts...@chromium.org (2023-03-17)

Assigning per 1410061. I spent some time trying to configure android emulator against internal webserver with no luck, so can not offer a repro range.

[Monorail components: Blink>SecurityFeature]

### mt...@chromium.org (2023-03-17)

cc alexmos who made the CSP comments on https://chromium-review.googlesource.com/c/chromium/src/+/4294954

Probably not a regression at all, so no need for a repro range.

### mt...@chromium.org (2023-03-17)

From the CL: "NavigationHandle::SandboxFlagsToCommit() can only be used once we've received the final response for a navigation; its intent is to ensure we include both the current frame's sandbox flags with which the navigation was started, as well as any sandbox flags that were returned in HTTP response headers (in particular, via CSP: sandbox). I don't think the latter matter for intents, and also IIUC these checks are performed at NavigationThrottle::WillStartRequest/WillRedirectRequest time, which is too early to know the response anyway."

Seems this was wrong? I'm guessing the issue is CSP restrictions aren't included in sandbox flags, so we would also need to prevent fallback URLs/tab clobbering when CSP is present as well given we don't support persisting CSP through these yet.

Alternatively, I add support for redirecting the main frame in response to intent:// URLs (like I added for subframes). A lot more work, but possibly worth it in the long term to fix this entire class of bugs.

### mt...@chromium.org (2023-03-17)

[Empty comment from Monorail migration]

### mt...@chromium.org (2023-03-17)

[Empty comment from Monorail migration]

[Monorail components: Mobile>Intents]

### ad...@google.com (2023-03-17)

(I am a bot: this is an auto-cc on a security bug)

### [Deleted User] (2023-03-18)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mt...@chromium.org (2023-03-21)

[Empty comment from Monorail migration]

### ar...@google.com (2023-03-28)

@mtiesse, I don't think CSP:sandbox is what matters here. What matter is main-frame vs sub-frame.

You can probably reproduce the same issue without CSP:sandbox, by opening a popup from a `sandbox:allow-popups' iframe. This cause sandbox flags to be inherited to the popup's main-frame. From there you can bypass sandbox download.


At first glance, I think the fix is to make:
Load subfame Intents to Chrome in the subframe | https://chromium-review.googlesource.com/c/chromium/src/+/4174394

To work for main frame navigation. WDYT?

### mt...@chromium.org (2023-03-28)

No, you can't reproduce the issue without CSP:sandbox because I fixed it here: https://chromium-review.googlesource.com/c/chromium/src/+/4358250

I didn't realize the the CSP sandbox wasn't included in sandbox flags though, so the solution there didn't include CSP sandbox flags.

But yes, redirecting the main frame instead of clobbering with a new top level navigation should fix this class of problems including CSP flags.

### ar...@chromium.org (2023-03-28)

I forgot this patch. Then you are right!

Yes, we only take into account the sandbox flags that will be applied to the new document. However we don't take into account the ones from the initiator.

I guess the solutions are:
- Redirecting intent navigation no matter if they are in the main frame or the sub frame. This way, the general navigation logic applies, and we don't have to worry about other similar issues.
- Plumb what is needed to "reproduce" the missing logic. Sounds easy, but maybe not very futureproof.

### [Deleted User] (2023-04-11)

mthiesse: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-04-21)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2023-04-26)

Labelling as impacting stable per https://crbug.com/chromium/1425355#c3

### [Deleted User] (2023-04-26)

[Empty comment from Monorail migration]

### mt...@chromium.org (2023-05-08)

Arthur offered to help by exposing the CSP information needed by the intercept_navigation_delegate from navigation_handle.

For Posterity: I looked into making the delegate redirect the main frame instead of clobbering with a new top level navigation, but this would lead to a performance regression on all navigations, which would be a much much larger project to fix. Essentially, it would require moving from a NavigationThrottle which can do its checks async, to a UrlLoader which cannot currently do its checks async.

### ar...@google.com (2023-05-09)

[Empty comment from Monorail migration]

### ar...@google.com (2023-06-01)

Here is the patch about adding `NavigationHandle::SandboxFlagsInitiator()`
https://chromium-review.googlesource.com/c/chromium/src/+/4577279

### [Deleted User] (2023-07-03)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-07-13)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-07-24)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-08-03)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2023-08-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/3ebd74c36b54b172b5a03221f9e5ef96392c9470

commit 3ebd74c36b54b172b5a03221f9e5ef96392c9470
Author: Arthur Sonzogni <arthursonzogni@chromium.org>
Date: Fri Aug 11 08:47:50 2023

Add NavigationHandle::SandboxFlagsInitiator()

It represents the sandbox flags of the initiator of the navigation.

Bug: 1425355
Change-Id: I664a4b62139338f7a657774c43ca91c777a6356d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4577279
Reviewed-by: Michael Thiessen <mthiesse@chromium.org>
Commit-Queue: Arthur Sonzogni <arthursonzogni@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1182481}

[modify] https://crrev.com/3ebd74c36b54b172b5a03221f9e5ef96392c9470/content/public/test/mock_navigation_handle.h
[modify] https://crrev.com/3ebd74c36b54b172b5a03221f9e5ef96392c9470/content/browser/renderer_host/navigation_request.cc
[modify] https://crrev.com/3ebd74c36b54b172b5a03221f9e5ef96392c9470/content/browser/renderer_host/navigation_request_browsertest.cc
[modify] https://crrev.com/3ebd74c36b54b172b5a03221f9e5ef96392c9470/components/navigation_interception/intercept_navigation_delegate.cc
[modify] https://crrev.com/3ebd74c36b54b172b5a03221f9e5ef96392c9470/content/public/browser/navigation_handle.h
[modify] https://crrev.com/3ebd74c36b54b172b5a03221f9e5ef96392c9470/content/browser/renderer_host/navigation_request.h


### gi...@appspot.gserviceaccount.com (2023-08-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/ebb73e1e8698002f068a68063048a433a4fa2172

commit ebb73e1e8698002f068a68063048a433a4fa2172
Author: Mohamed Amir Yosef <mamir@chromium.org>
Date: Fri Aug 11 11:40:15 2023

Revert "Add NavigationHandle::SandboxFlagsInitiator()"

This reverts commit 3ebd74c36b54b172b5a03221f9e5ef96392c9470.

Reason for revert: The added test fails consistently on on builder chrome/ci/linux-chromeos-chrome
https://ci.chromium.org/ui/p/chrome/builders/ci/linux-chromeos-chrome/35063/overview

Original change's description:
> Add NavigationHandle::SandboxFlagsInitiator()
>
> It represents the sandbox flags of the initiator of the navigation.
>
> Bug: 1425355
> Change-Id: I664a4b62139338f7a657774c43ca91c777a6356d
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4577279
> Reviewed-by: Michael Thiessen <mthiesse@chromium.org>
> Commit-Queue: Arthur Sonzogni <arthursonzogni@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#1182481}

Bug: 1425355
Change-Id: I37f45a5b63c77b199a88a9cf8a5963bb4e1d5ba8
No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4770847
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Auto-Submit: Mohamed Amir Yosef <mamir@chromium.org>
Owners-Override: Mohamed Amir Yosef <mamir@chromium.org>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#1182523}

[modify] https://crrev.com/ebb73e1e8698002f068a68063048a433a4fa2172/content/public/test/mock_navigation_handle.h
[modify] https://crrev.com/ebb73e1e8698002f068a68063048a433a4fa2172/content/browser/renderer_host/navigation_request.cc
[modify] https://crrev.com/ebb73e1e8698002f068a68063048a433a4fa2172/components/navigation_interception/intercept_navigation_delegate.cc
[modify] https://crrev.com/ebb73e1e8698002f068a68063048a433a4fa2172/content/browser/renderer_host/navigation_request_browsertest.cc
[modify] https://crrev.com/ebb73e1e8698002f068a68063048a433a4fa2172/content/browser/renderer_host/navigation_request.h
[modify] https://crrev.com/ebb73e1e8698002f068a68063048a433a4fa2172/content/public/browser/navigation_handle.h


### gi...@appspot.gserviceaccount.com (2023-08-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/dc8508abeefee712bc4ed68611e150b856516482

commit dc8508abeefee712bc4ed68611e150b856516482
Author: Arthur Sonzogni <arthursonzogni@chromium.org>
Date: Thu Aug 17 08:42:42 2023

Reland "Add NavigationHandle::SandboxFlagsInitiator()"

This is a reland of commit 3ebd74c36b54b172b5a03221f9e5ef96392c9470

Original change's description:
> Add NavigationHandle::SandboxFlagsInitiator()
>
> It represents the sandbox flags of the initiator of the navigation.
>
> Bug: 1425355
> Change-Id: I664a4b62139338f7a657774c43ca91c777a6356d
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4577279
> Reviewed-by: Michael Thiessen <mthiesse@chromium.org>
> Commit-Queue: Arthur Sonzogni <arthursonzogni@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#1182481}

Bug: 1425355
Change-Id: I7ba1ce3ac4c5c91328786fed1faa87b235c9c5ec
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4784149
Reviewed-by: Michael Thiessen <mthiesse@chromium.org>
Commit-Queue: Arthur Sonzogni <arthursonzogni@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1184599}

[modify] https://crrev.com/dc8508abeefee712bc4ed68611e150b856516482/content/public/test/mock_navigation_handle.h
[modify] https://crrev.com/dc8508abeefee712bc4ed68611e150b856516482/content/browser/renderer_host/navigation_request.cc
[modify] https://crrev.com/dc8508abeefee712bc4ed68611e150b856516482/components/navigation_interception/intercept_navigation_delegate.cc
[modify] https://crrev.com/dc8508abeefee712bc4ed68611e150b856516482/content/browser/renderer_host/navigation_request_browsertest.cc
[modify] https://crrev.com/dc8508abeefee712bc4ed68611e150b856516482/content/public/browser/navigation_handle.h
[modify] https://crrev.com/dc8508abeefee712bc4ed68611e150b856516482/content/browser/renderer_host/navigation_request.h


### gi...@appspot.gserviceaccount.com (2023-08-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/d80a1af1f4fd43c06d7c2eb27b323cbe8fb929f5

commit d80a1af1f4fd43c06d7c2eb27b323cbe8fb929f5
Author: Michael Thiessen <mthiesse@chromium.org>
Date: Mon Aug 21 17:17:35 2023

Block fallback URLs from CSP-sandboxed external navigation

We don't support persisting sandbox flags through fallback URLs when
performing external navigation.

This is a follow-on to https://chromium-review.googlesource.com/c/chromium/src/+/4294954

Bug: 1425355
Change-Id: Iab9f309083322292fe884123320f0cd51c6c341e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4771297
Commit-Queue: Michael Thiessen <mthiesse@chromium.org>
Reviewed-by: Yaron Friedman <yfriedman@chromium.org>
Reviewed-by: Arthur Sonzogni <arthursonzogni@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1185932}

[modify] https://crrev.com/d80a1af1f4fd43c06d7c2eb27b323cbe8fb929f5/components/navigation_interception/intercept_navigation_delegate.cc
[add] https://crrev.com/d80a1af1f4fd43c06d7c2eb27b323cbe8fb929f5/chrome/test/data/android/url_overriding/subframe_navigation_parent_csp_sandbox.html
[add] https://crrev.com/d80a1af1f4fd43c06d7c2eb27b323cbe8fb929f5/chrome/test/data/android/url_overriding/subframe_navigation_parent_csp_sandbox.html.mock-http-headers
[modify] https://crrev.com/d80a1af1f4fd43c06d7c2eb27b323cbe8fb929f5/chrome/android/javatests/src/org/chromium/chrome/browser/externalnav/UrlOverridingTest.java


### mt...@chromium.org (2023-08-21)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-22)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-22)

[Empty comment from Monorail migration]

### ha...@gmail.com (2023-08-30)

Just an additional note here (which I think is also worth mentioning): this also allows site to bypass "allow-top-navigation-to-custom-protocols" which is a sandbox flag that only allows top-navigation to custom protocols (and not http / https)

### am...@google.com (2023-09-14)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-09-14)

Congratulations Axel! The VRP Panel has decided to award you $1,000 for this report based on exploitability and impact as presented. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2023-09-17)

[Empty comment from Monorail migration]

### pg...@google.com (2023-10-09)

[Empty comment from Monorail migration]

### pg...@google.com (2023-10-11)

[Empty comment from Monorail migration]

### pg...@google.com (2023-10-11)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-27)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-11-27)

This issue was migrated from crbug.com/chromium/1425355?no_tracker_redirect=1

[Multiple monorail components: Blink>SecurityFeature, Mobile>Intents]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40063634)*
