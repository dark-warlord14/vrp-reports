# Security: Chrome Apps can access chrome.storage for other extensions via webview

| Field | Value |
|-------|-------|
| **Issue ID** | [40052905](https://issues.chromium.org/issues/40052905) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>Apps>BrowserTag |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | de...@gmail.com |
| **Assignee** | mc...@chromium.org |
| **Created** | 2020-07-22 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

One of the methods a Chrome App can use with a webview is loadDataWithBaseUrl. That method allows a custom base URL to be set, which, in effect, allows a context to be created with an arbitrary URL.

Using that fact, an app can access chrome.storage for another extension, by assigning the base URL to be a URL from the target extension. This also allows the app to impersonate the target extension when using chrome.runtime.sendMessage.

**VERSION**  

Chrome Version: Tested on 84.0.4147.89 (stable) and 86.0.4208.0 (canary)  

Operating System: Windows 10, version 1909

**REPRODUCTION CASE**

1. Install the attached app.
2. Once installed, the app will open page.html in a new app window.
3. page.html contains a webview and makes the following call:

webview.loadDataWithBaseUrl("data:text/html,<script>chrome.storage.local.set({appStorageKey: 'appStorageValue'});</script>", "chrome-extension://pkedcjkdefgpdelpbcmbmeomcjbeemfm/");

This should set the "appStorageKey" value within the local storage for the Chrome Media Router extension. To verify that, run the following code within the context of the Media Router extension:

chrome.storage.local.get("appStorageKey", function (item) {console.log(item);});

This should print the key and value that were set above.

As mentioned in the summary, it's also possible to impersonate another extension when using the chrome.runtime.sendMessage method. You can test that by adding a chrome.runtime.onMessage listener within the Media Router extension (for example), then calling chrome.runtime.sendMessage from the webview set up by the demonstration app.

**CREDIT INFORMATION**  

Reporter credit: David Erceg

## Attachments

- [background.js](attachments/background.js) (text/plain, 38 B)
- [manifest.json](attachments/manifest.json) (text/plain, 246 B)
- [page.html](attachments/page.html) (text/plain, 123 B)
- [page.js](attachments/page.js) (text/plain, 552 B)

## Timeline

### aj...@google.com (2020-07-22)

Setting High as this might allow a site isolation bypass. May be the same root cause as https://crbug.com/1106890 so CC'ing the same people.

[Monorail components: Platform>Apps>BrowserTag]

### mc...@chromium.org (2020-07-22)

Lowering severity as this requires a chrome app to be installed (see the reasoning in https://crbug.com/683523#c10).

### mc...@chromium.org (2020-07-22)

[Empty comment from Monorail migration]

### mc...@chromium.org (2020-07-22)

In |WebViewGuest::LoadDataWithBaseURL|, we don't appear to be checking that the provided base url has a known safe scheme unlike regular navigations via |WebViewGuest::LoadURLWithParams|.

Also, I checked the UMA histogram for this function and there are only 21 calls for 28 day Chrome OS stable and 9 calls for 28 day Win/Mac/Linux stable. So perhaps one option could simply be to remove this API instead of trying to make it safe. See also: https://docs.google.com/document/d/154nT5rF1CEdwyWSu56uZcmI8TiWazFET1XElii6KzwA/edit#heading=h.gqp9mv39vvrw (albeit in the context of android webview).

### [Deleted User] (2020-07-23)

Setting milestone and target because of Security_Impact=Head and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-07-23)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mc...@chromium.org (2020-07-23)

This isn't a recent regression. The API has existed since 2014 (see https://crbug.com/chromium/399790).

### aj...@google.com (2020-07-23)

Thanks for the updates! I've assigned this and the potentially related #1106890 to mcnee@ as we like security bugs to have owners. Feel free to assign to someone else if they will be working on a fix.

### wj...@chromium.org (2020-07-24)

Removing people who no longer work on WebView, and adding security team members for assessment.

### wj...@chromium.org (2020-07-24)

[Empty comment from Monorail migration]

### [Deleted User] (2020-07-24)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cr...@chromium.org (2020-07-25)

Hmm, it appears that loadDataWithBaseURL has almost no restrictions on what the base URL can be, and sets the origin of the data URL to it.  Why isn't it limited to URLs that the app has the ability to load within GuestViews?  That seems like a problem.  (In fact, it looks like you can even use chrome:// origins, though those don't load with any privileges within the GuestView and they're not subject to the problems from https://crbug.com/chromium/1106890.)

mcnee@: Can you elaborate on the scheme check you propose in https://crbug.com/chromium/1108126#c4?  I think chrome-extension:// is considered web safe since some extension URLs are web accessible.  I suspect we'll need something stronger, like requiring the app to have permission for the URL.

Then again, I would *love* to remove this API given the very low usage.  loadDataWithBaseURL is a huge headache on Android WebView, and I'd love not to have to deal with its corner cases on Chrome App <webview> as well.  I would heartily support any effort to remove it, though I suspect we'll need a quicker fix for this bug.  Hopefully the low usage also makes it easy to impose a security restriction on base URL?

(BTW, I agree that this is worse when combined with https://crbug.com/chromium/1106890, since you can probably choose any origin to attack, not just those in your app's manifest.  Still, they're each problems in their own right, and will need independent fixes.  Thanks for both reports!)

### cr...@chromium.org (2020-07-25)

I suspect this affects Chrome Apps on all platforms.

### cr...@chromium.org (2020-07-28)

lfg@: Would you be able to help with this security bug for a bit while wjmaclean@ is OOO?  (I was going to ask mcnee@ but it looks like he's out for a week as well.)  Feel free to find another owner, but hopefully we can find someone to help make progress on it.  Thanks!

### [Deleted User] (2020-08-05)

lfg: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-08-20)

lfg: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-10-07)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-30)

[Empty comment from Monorail migration]

### mc...@chromium.org (2020-11-11)

Oh, looks like this slipped through the cracks. I'll re-assign to myself and try to take a look later this week/early next week.

Re c#12: 
> Why isn't it limited to URLs that the app has the ability to load within GuestViews?
Presumably an oversight. This API was originally added in response to a feature request and while it went through a code review, it doesn't look like it got a security review.

> Can you elaborate on the scheme check you propose...
I was thinking HTTP(S) plus the embedder's own origin*, or possibly web safe excluding other extensions. The former is easier to reason about and seems like how the API should reasonably be used. The latter just addresses the immediate issue and is more conservative about adding restrictions and possibly breaking things, but I'd be worried about missing another case which could lead to a similar vulnerability. I'd lean towards the former for essentially the reason you mentioned: the very low usage would hopefully make breakage very unlikely.

* for accessible_resources purposes

### [Deleted User] (2020-11-18)

[Empty comment from Monorail migration]

### mc...@chromium.org (2020-11-23)

CL: https://chromium-review.googlesource.com/c/chromium/src/+/2553704

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-11-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/a36c6e3a16e134d9773d884c86c692d4d29764d1

commit a36c6e3a16e134d9773d884c86c692d4d29764d1
Author: Kevin McNee <mcnee@chromium.org>
Date: Wed Nov 25 17:46:26 2020

Restrict webview.loadDataWithBaseUrl base URL

There were no restrictions on which URLs could be used as the base URL
when using webview's loadDataWithBaseUrl API. This could allow for an
embedder to impersonate another extension through a webview.

We now restrict the base URL to HTTP(S) or the embedder's own origin.

Bug: 1108126
Change-Id: I093a3d2c75cfb2f307ceca43add513194df13854
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2553704
Reviewed-by: James MacLean <wjmaclean@chromium.org>
Commit-Queue: Kevin McNee <mcnee@chromium.org>
Cr-Commit-Position: refs/heads/master@{#831054}

[modify] https://crrev.com/a36c6e3a16e134d9773d884c86c692d4d29764d1/chrome/browser/apps/guest_view/web_view_browsertest.cc
[modify] https://crrev.com/a36c6e3a16e134d9773d884c86c692d4d29764d1/chrome/test/data/extensions/platform_apps/web_view/shim/main.js
[modify] https://crrev.com/a36c6e3a16e134d9773d884c86c692d4d29764d1/chrome/test/data/extensions/platform_apps/web_view/shim/manifest.json
[modify] https://crrev.com/a36c6e3a16e134d9773d884c86c692d4d29764d1/extensions/browser/api/guest_view/web_view/web_view_internal_api.cc
[modify] https://crrev.com/a36c6e3a16e134d9773d884c86c692d4d29764d1/extensions/browser/guest_view/web_view/web_view_guest.cc
[modify] https://crrev.com/a36c6e3a16e134d9773d884c86c692d4d29764d1/extensions/browser/guest_view/web_view/web_view_guest.h


### mc...@chromium.org (2020-11-25)

[Empty comment from Monorail migration]

### [Deleted User] (2020-11-25)

Requesting merge to beta M87 because latest trunk commit (831054) appears to be after beta branch point (812852).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-11-25)

This bug requires manual review: Request affecting a post-stable build
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on ToT?
4. Does this change need to be merged into other active release branches (M-1, M+1)?
5. Why are these changes required in this milestone after branch?
6. Is this a new feature?
7. If it is a new feature, is it behind a flag using finch?

Chrome OS Only:
8. Was the change reviewed and approved by the Eng Prod Representative? See Eng Prod ownership by component: http://go/cros-engprodcomponents

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), bindusuvarna @(iOS), cindyb@(ChromeOS), lakpamarthy@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### la...@google.com (2020-11-25)

+adetaylor to advise on the M87 merge

### ad...@chromium.org (2020-11-25)

I'll consider that when we're a bit closer to the next M87 security refresh and this bug (and others) have had more bake time in canary.

### mc...@chromium.org (2020-11-25)

The CL involves an API change. Even though we expect breakage to be unlikely (see c#19), it does not seem to me that this would meet the criteria for a post-stable merge.

An M88 merge seems like a good idea though.

### [Deleted User] (2020-11-26)

[Empty comment from Monorail migration]

### [Deleted User] (2020-11-26)

[Empty comment from Monorail migration]

### [Deleted User] (2020-11-26)

Your change meets the bar and is auto-approved for M88. Please go ahead and merge the CL to branch 4324 (refs/branch-heads/4324) manually. Please contact milestone owner if you have questions.
Merge instructions: https://www.chromium.org/developers/how-tos/drover
Owners: govind@(Android), bindusuvarna@(iOS), dgagnon@(ChromeOS), srinivassista @(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-11-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/e11cd65803b6a2f7f90aa2d5de43bbeeb8756d95

commit e11cd65803b6a2f7f90aa2d5de43bbeeb8756d95
Author: Kevin McNee <mcnee@chromium.org>
Date: Sat Nov 28 00:23:59 2020

Merge M88: Restrict webview.loadDataWithBaseUrl base URL

TBR=wjmaclean@chromium.org

Restrict webview.loadDataWithBaseUrl base URL

There were no restrictions on which URLs could be used as the base URL
when using webview's loadDataWithBaseUrl API. This could allow for an
embedder to impersonate another extension through a webview.

We now restrict the base URL to HTTP(S) or the embedder's own origin.

(cherry picked from commit a36c6e3a16e134d9773d884c86c692d4d29764d1)

Bug: 1108126
Change-Id: I093a3d2c75cfb2f307ceca43add513194df13854
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2553704
Reviewed-by: James MacLean <wjmaclean@chromium.org>
Commit-Queue: Kevin McNee <mcnee@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#831054}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2563286
Reviewed-by: Kevin McNee <mcnee@chromium.org>
Cr-Commit-Position: refs/branch-heads/4324@{#406}
Cr-Branched-From: c73b5a651d37a6c4d0b8e3262cc4015a5579c6c8-refs/heads/master@{#827102}

[modify] https://crrev.com/e11cd65803b6a2f7f90aa2d5de43bbeeb8756d95/chrome/browser/apps/guest_view/web_view_browsertest.cc
[modify] https://crrev.com/e11cd65803b6a2f7f90aa2d5de43bbeeb8756d95/chrome/test/data/extensions/platform_apps/web_view/shim/main.js
[modify] https://crrev.com/e11cd65803b6a2f7f90aa2d5de43bbeeb8756d95/chrome/test/data/extensions/platform_apps/web_view/shim/manifest.json
[modify] https://crrev.com/e11cd65803b6a2f7f90aa2d5de43bbeeb8756d95/extensions/browser/api/guest_view/web_view/web_view_internal_api.cc
[modify] https://crrev.com/e11cd65803b6a2f7f90aa2d5de43bbeeb8756d95/extensions/browser/guest_view/web_view/web_view_guest.cc
[modify] https://crrev.com/e11cd65803b6a2f7f90aa2d5de43bbeeb8756d95/extensions/browser/guest_view/web_view/web_view_guest.h


### la...@google.com (2020-11-30)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-11-30)

As a medium severity bug with an API change I agree this is not a candidate for M87 merge.

### ad...@chromium.org (2020-11-30)

[Empty comment from Monorail migration]

### ad...@google.com (2020-12-02)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-12-03)

Congratulations, the VRP panel has decided to award $3000 for this bug.

### ad...@google.com (2020-12-04)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-13)

[Empty comment from Monorail migration]

### am...@google.com (2021-01-19)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### as...@google.com (2021-01-28)

[Empty comment from Monorail migration]

### gi...@google.com (2021-01-29)

[Empty comment from Monorail migration]

### as...@google.com (2021-01-29)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-01-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/476026c8aae5b131f4aa4304cc8a220373dbe247

commit 476026c8aae5b131f4aa4304cc8a220373dbe247
Author: Kevin McNee <mcnee@chromium.org>
Date: Fri Jan 29 18:24:00 2021

Merge LTS-M86: Restrict webview.loadDataWithBaseUrl base URL

TBR=wjmaclean@chromium.org

Restrict webview.loadDataWithBaseUrl base URL

There were no restrictions on which URLs could be used as the base URL
when using webview's loadDataWithBaseUrl API. This could allow for an
embedder to impersonate another extension through a webview.

We now restrict the base URL to HTTP(S) or the embedder's own origin.

(cherry picked from commit a36c6e3a16e134d9773d884c86c692d4d29764d1)

(cherry picked from commit e11cd65803b6a2f7f90aa2d5de43bbeeb8756d95)

Bug: 1108126
Change-Id: I093a3d2c75cfb2f307ceca43add513194df13854
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2553704
Reviewed-by: James MacLean <wjmaclean@chromium.org>
Commit-Queue: Kevin McNee <mcnee@chromium.org>
Cr-Original-Original-Commit-Position: refs/heads/master@{#831054}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2563286
Reviewed-by: Kevin McNee <mcnee@chromium.org>
Cr-Original-Commit-Position: refs/branch-heads/4324@{#406}
Cr-Original-Branched-From: c73b5a651d37a6c4d0b8e3262cc4015a5579c6c8-refs/heads/master@{#827102}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2656319
Reviewed-by: Victor-Gabriel Savu <vsavu@google.com>
Commit-Queue: Artem Sumaneev <asumaneev@google.com>
Cr-Commit-Position: refs/branch-heads/4240@{#1533}
Cr-Branched-From: f297677702651916bbf65e59c0d4bbd4ce57d1ee-refs/heads/master@{#800218}

[modify] https://crrev.com/476026c8aae5b131f4aa4304cc8a220373dbe247/chrome/browser/apps/guest_view/web_view_browsertest.cc
[modify] https://crrev.com/476026c8aae5b131f4aa4304cc8a220373dbe247/extensions/browser/api/guest_view/web_view/web_view_internal_api.cc
[modify] https://crrev.com/476026c8aae5b131f4aa4304cc8a220373dbe247/extensions/browser/guest_view/web_view/web_view_guest.cc
[modify] https://crrev.com/476026c8aae5b131f4aa4304cc8a220373dbe247/extensions/browser/guest_view/web_view/web_view_guest.h
[modify] https://crrev.com/476026c8aae5b131f4aa4304cc8a220373dbe247/chrome/test/data/extensions/platform_apps/web_view/shim/manifest.json
[modify] https://crrev.com/476026c8aae5b131f4aa4304cc8a220373dbe247/chrome/test/data/extensions/platform_apps/web_view/shim/main.js


### as...@google.com (2021-01-29)

[Empty comment from Monorail migration]

### am...@google.com (2021-02-09)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-04)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1108126?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40052905)*
