# Security: URL bar spoofing with using a file:/// URL

| Field | Value |
|-------|-------|
| **Issue ID** | [40050308](https://issues.chromium.org/issues/40050308) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Navigation |
| **Platforms** | iOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | aj...@google.com |
| **Created** | 2019-10-02 |
| **Bounty** | $500.00 |

## Description

**VERSION**  

Chrome Version: Chrome beta  

Operating System: iOS 13

**REPRODUCTION CASE**

1. Go to <https://lbstyle.github.io/o.html>
2. Click on the button.
3. Focus the address bar clear the existing address.
4. Paste the URL and enter.

Chrome should block navigation to file:/// URIs

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 683 B)
- [IMG_7254.MP4](attachments/IMG_7254.MP4) (video/mp4, 998.1 KB)

## Timeline

### mp...@google.com (2019-10-02)

Sorry, would you mind posting a video? What spoofing attack is this accomplishing? Just to make sure I'm triaging this correctly.

Thanks for the report as always!

### ch...@gmail.com (2019-10-02)

This is similar to issue https://crbug.com/chromium/994044 which is already fixed on iOS 12 but still repro on iOS 13.

### ch...@gmail.com (2019-10-02)

[Empty comment from Monorail migration]

### mp...@google.com (2019-10-02)

Okay, thanks!



[Monorail components: UI>Browser>Navigation]

### sh...@chromium.org (2019-10-03)

Setting milestone and target because of Security_Impact=Beta and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-10-03)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-10-03)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ju...@chromium.org (2019-10-03)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-10-03)

[Empty comment from Monorail migration]

### ka...@google.com (2019-10-09)

gambard, eugenebut, justincohen: Can one of you all take this security bug if you believe it should truly stay RBS?

mrsuyi is out until after stable cut next week.

### ga...@chromium.org (2019-10-09)

I think it can be moved to M79 as it requires a lot of action from the user. Also, it is the same behavior as if the user is trying to load a page that takes a very long time to answer.

### ka...@google.com (2019-10-09)

Ok thanks gambard.

### sh...@chromium.org (2019-10-17)

mrsuyi: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jd...@chromium.org (2019-10-24)

I'm downgrading this to medium because of the copy-paste interaction, but we'd still love to see some progress here. Any updates in the past two weeks? Thanks!

### mr...@chromium.org (2019-10-24)

I'll take a look soon. It seems that both progress bar and the omnibox are displaying the state of a new navigation that should have stopped. My work on "using WKWebView.loading for WebState::IsLoading" will probably fix the progress bar, not sure about the URL:
https://chromium-review.googlesource.com/c/chromium/src/+/1778864

### mr...@chromium.org (2019-10-25)

It seems that the attempt to load file://www.verylongurl.googlecloudplatform.accounts.google.com/ will freeze the web process, and only KVO callbacks are invoked, with WKWebView.URL=file://www.verylongurl.googlecloudplatform.accounts.google.com/ and WKWebView.loading=true.

Also, these logs are printed:
Received an unexpected URL from the web process: 'file://www.verylongurl.googlecloudplatform.accounts.google.com/'
[Process] 0x11b038218 - WebPageProxy::Ignoring request to load this main resource because it is outside the sandbox

+ajuma@ can you help confirm that if this is a WebKit bug that fails to revert WKWebView.URL back to committed URL and WKWebView.loading back to false?

If not, this means that WebKit is still trying to load the file:// URL without timeout.

### mr...@chromium.org (2019-10-25)

I can confirm that this is also reproducible on Safari, iOS 13.1.3. The page is interactive, while the omnibox is displaying the new URL and the progress bar is also displayed.

### aj...@chromium.org (2019-10-25)

Yes, this looks like a WebKit bug, where the problem is when we decide not to load a file URL:
https://github.com/WebKit/webkit/blob/master/Source/WebKit/UIProcess/WebPageProxy.cpp#L4741

WebKit inserts a navigation policy decision of Ignore, but doesn't call "m_pageLoadState.clearPendingAPIRequest(transaction);", so the load appears to never stop.

It doesn't appear to freeze the web process though: from the WebProcess' point of view, the load is cancelled because of navigation policy, and the previous page remains interactive.

### aj...@chromium.org (2019-10-25)

Discussing with justincohen@, there doesn't seem to be a good reason to even attempt navigation to such file:/// URLs. For file:/// URLs that we get from Copy-to-Chrome actions (i.e., files sent to Chrome by other apps), we'll have a chrome:// virtual URL, so that gives us a way to distinguish those URLs from user-entered URLs.

Here's a WIP patch implementing that approach: https://chromium-review.googlesource.com/c/chromium/src/+/1881667

Still need to add a test, but first wanted to see if this passes existing tests.

### aj...@chromium.org (2019-10-26)

Turns out it fails many existing tests. I'll take a closer look next week to see if there's a clean way to tweak the tests (or the patch) to fix the failures.

### aj...@chromium.org (2019-10-26)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-10-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/f9f9d7af01db5387cfa2104c09fe0ed8cbb26525

commit f9f9d7af01db5387cfa2104c09fe0ed8cbb26525
Author: Ali Juma <ajuma@chromium.org>
Date: Tue Oct 29 01:03:46 2019

[iOS] Disallow non-app-initiated navigations to file URLs

WKWebView and iOS do not permit navigation to arbitrary files on a
device's file system. Attempting to load such inaccessible files in
WKWebView can later trigger broken behavior (see crbug.com/1010526
for more details). To prevent this brokenness, disallow these
navigations right away, rather than waiting for WKWebView to disallow
them.

Bug: 1010526
Change-Id: Ieefb5befad659669a38efad127dfdb6e0179a165
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1881667
Commit-Queue: Ali Juma <ajuma@chromium.org>
Reviewed-by: Eugene But <eugenebut@chromium.org>
Cr-Commit-Position: refs/heads/master@{#710125}

[modify] https://crrev.com/f9f9d7af01db5387cfa2104c09fe0ed8cbb26525/ios/web/web_state/ui/crw_web_request_controller.mm
[modify] https://crrev.com/f9f9d7af01db5387cfa2104c09fe0ed8cbb26525/ios/web/web_state/web_state_observer_inttest.mm
[modify] https://crrev.com/f9f9d7af01db5387cfa2104c09fe0ed8cbb26525/ios/web/web_state/web_state_unittest.mm


### aj...@chromium.org (2019-10-29)

Verified fixed in Canary.

### sh...@chromium.org (2019-10-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-10-30)

Your change meets the bar and is auto-approved for M79. Please go ahead and merge the CL to branch 3945 (refs/branch-heads/3945) manually. Please contact milestone owner if you have questions.
Merge instructions: https://www.chromium.org/developers/how-tos/drover
Owners: benmason@(Android), kariahda@(iOS), cindyb@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aj...@chromium.org (2019-10-30)

Merged to M79: https://chromium-review.googlesource.com/c/chromium/src/+/1890002

### sh...@chromium.org (2019-11-04)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aj...@chromium.org (2019-11-04)

Merge has been completed (see https://crbug.com/chromium/1010526#c26). Not sure why bugdroid didn't comment.

### na...@google.com (2019-11-04)

[Empty comment from Monorail migration]

### na...@google.com (2019-11-21)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2019-11-21)

Congrats! The Panel decided to reward $500  for this report!

### na...@google.com (2019-11-21)

[Empty comment from Monorail migration]

### sh...@chromium.org (2020-02-04)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/1010526?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40050308)*
