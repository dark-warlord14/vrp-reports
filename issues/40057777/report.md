# XSS from chrome-untrusted://new-tab-page URL parsing

| Field | Value |
|-------|-------|
| **Issue ID** | [40057777](https://issues.chromium.org/issues/40057777) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Internals>Sandbox>SiteIsolation, Platform>Extensions, UI>Browser>WebUI |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | nd...@protonmail.com |
| **Assignee** | ti...@chromium.org |
| **Created** | 2021-10-31 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36

Steps to reproduce the problem:
Direct URL navigation:
chrome-untrusted://new-tab-page/custom_background_image?url=https://a.a&size=%3C/style%3E%3Cscript%3Ealert(1)%3C/script%3E
From a extension with no permissions:
chrome.tabs.update(ID, {url: "chrome-untrusted://new-tab-page/custom_background_image?url=https://a.a&size=%3C/style%3E%3Cscript%3Ealert(1)%3C/script%3E"}, console.log);

What is the expected behavior?

What went wrong?
Get XSS from URL.

Did this work before? N/A 

Chrome version: 95.0.4638.54  Channel: n/a
OS Version: 10.0

This origin is used on new tabs.

## Timeline

### [Deleted User] (2021-10-31)

[Empty comment from Monorail migration]

### nd...@protonmail.com (2021-10-31)

[Comment Deleted]

### nd...@protonmail.com (2021-10-31)

[Comment Deleted]

### nd...@protonmail.com (2021-10-31)

[Comment Deleted]

### nd...@protonmail.com (2021-10-31)

[Comment Deleted]

### nd...@protonmail.com (2021-10-31)

[Comment Deleted]

### nd...@protonmail.com (2021-10-31)

[Comment Deleted]

### da...@chromium.org (2021-11-02)

This is a XSS attack that can be launched from a link on a malicious page (with a user click) and can run arbitrary JS in a privileged WebUI process.

We've had a few XSS attacks that needed to be done by copy/paste but this shows the new-tab-page is accepting parameters and executing them.

We should stop doing that immediately, or we need to sanitize them.

This should affect all desktop platforms equally. Android and IOS have different NTP machinery so not sure there.

I can reproduce this on stable M95 (95.0.4638.54)

[Monorail components: Internals>Sandbox>SiteIsolation UI>Browser>NewTabPage UI>Browser>WebUI]

### [Deleted User] (2021-11-02)

[Empty comment from Monorail migration]

### da...@chromium.org (2021-11-02)

[Empty comment from Monorail migration]

### da...@chromium.org (2021-11-02)

[Empty comment from Monorail migration]

[Monorail components: Platform>Extensions]

### da...@chromium.org (2021-11-02)

Note that we've seen a bunch of XSS in the search box in NTP, but this is different. It is in parsing `custom_background_image?url=https://a.a&size=%3C/style%3E%3Cscript%3Ealert(1)%3C/script%3E` from the URL itself.

### da...@chromium.org (2021-11-02)

[Empty comment from Monorail migration]

### da...@chromium.org (2021-11-02)

[Empty comment from Monorail migration]

### da...@chromium.org (2021-11-02)

In M94 asan I reach this:

[8570:8589:1102/152359.016439:FATAL:statement.cc(62)] Cannot call mutating statements on an invalid statement.

https://source.chromium.org/chromium/chromium/src/+/main:sql/statement.cc;drc=e5a38eddbdf45d7563a00d019debd11b803af1bb;l=62

  // Allow operations to fail silently if a statement was invalidated
  // because the database was closed by an error handler.
  DLOG_IF(FATAL, !ref_->was_valid())
      << "Cannot call mutating statements on an invalid statement.";

Putting this into the set of security bugs that are hidden behind DCHECKs.

### da...@chromium.org (2021-11-02)

I can reproduce on M94 94.0.4606.0

### [Deleted User] (2021-11-02)

[Empty comment from Monorail migration]

### lu...@chromium.org (2021-11-02)

RE: https://crbug.com/chromium/1265197#c8: This is a XSS attack that can be launched from a link on a malicious page

I've tried to repro this by

1. Navigating to https://example.com
2. In DevTools console executing:

      a = document.createElement('a')
      a.href = 'chrome-untrusted://new-tab-page/custom_background_image?url=https://a.a&size=%3C/style%3E%3Cscript%3Ealert(1)%3C/script%3E'
'chrome-untrusted://new-tab-page/custom_background_image?url=https://a.a&size=%3C/style%3E%3Cscript%3Ealert(1)%3C/script%3E'
      a.innerText = 'my link'
      document.body.appendChild(a)

3. Clicking the new link

The bug didn't repro for me (AFAICT) - the link was rewritten to about:blank#blocked.  I think this bug requires tricking the user into pasting the malicious link into the omnibox/etc (and cannot be exploited by just having a link from an attacker-controlled http/https page).

### [Deleted User] (2021-11-02)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### nd...@protonmail.com (2021-11-02)

[Comment Deleted]

### dp...@chromium.org (2021-11-02)

A few findings after a quick invesigation.

At [1] the following line is used
background-size: $i18nRaw{size};

The placeholders are filled in at [2]. The usage of $i18nRaw{} seems unnecessary. Note that i18nRaw{} does not do any escaping, unlike $i18n{} which should already escape the contents to avoid XSS attacks.

@tiborg: Is the usage of $i18nRaw{} placeholders in background_image.html needed, or can these be replaced with $i18n{} instead? 

[1] https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/resources/new_tab_page/untrusted/background_image.html;l=33;drc=4e9821341fcdc01080cff45cc7e1a6ebfd5e9bf3
[2] https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/webui/new_tab_page/untrusted_source.cc;l=294;drc=f9fff57f7a4235f6b6df58a1fa0a91ff702f8aa5

### dp...@chromium.org (2021-11-02)

> @tiborg: Is the usage of $i18nRaw{} placeholders in background_image.html needed, or can these be replaced with $i18n{} instead?

See proposed fix at https://chromium-review.googlesource.com/c/chromium/src/+/3258181.

### ti...@chromium.org (2021-11-02)

> @tiborg: Is the usage of $i18nRaw{} placeholders in background_image.html needed, or can these be replaced with $i18n{} instead?
dpapad@: As long as $i18n doesn't mangle URLs your fix should work.

Taking a step back though. chrome-untrusted://new-tab-page/custom_background_image runs in an unprivileged process, which should mitigate the security risk. Are we mostly worried that an attacker can make this frame appear a certain way and trick the user into doing something bad? If so, I like the suggestion of blocklisting navigations to chrome[-untrusted]://new-tab-page/... from extensions (possibly as a second layer of protection on top of sanitizing URL params were possible).

### dp...@chromium.org (2021-11-02)

> dpapad@: As long as $i18n doesn't mangle URLs your fix should work.

URLs should not be affected by any of the escaping done in $i18n{} AFAIK.

### ti...@chromium.org (2021-11-02)

> URLs should not be affected by any of the escaping done in $i18n{} AFAIK.
Sounds good. Thanks for change. Assigning to you for now to land this CL.

### nd...@protonmail.com (2021-11-02)

[Comment Deleted]

### gi...@appspot.gserviceaccount.com (2021-11-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/c812dc628e7a25349b7e63d64da5aaebe8ac2ead

commit c812dc628e7a25349b7e63d64da5aaebe8ac2ead
Author: dpapad <dpapad@chromium.org>
Date: Tue Nov 02 22:02:16 2021

NTP: Replace $i18nRaw{} usages with $i18n{} in new_tab_page/untrusted/

Bug: 1265197
Change-Id: I3c483eaeb352e38f3b51a2de2558e38e67cf7386
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3258181
Auto-Submit: dpapad <dpapad@chromium.org>
Commit-Queue: dpapad <dpapad@chromium.org>
Reviewed-by: Tibor Goldschwendt <tiborg@chromium.org>
Cr-Commit-Position: refs/heads/main@{#937561}

[modify] https://crrev.com/c812dc628e7a25349b7e63d64da5aaebe8ac2ead/chrome/browser/resources/new_tab_page/untrusted/background_image.html
[modify] https://crrev.com/c812dc628e7a25349b7e63d64da5aaebe8ac2ead/chrome/browser/resources/new_tab_page/untrusted/image.html


### dp...@chromium.org (2021-11-03)

@danakj: Can you help verifying that the fix above actually prevents the original issue?

### nd...@protonmail.com (2021-11-03)

While Im not the right person I will try to reply anyway :D

Example in https://crbug.com/chromium/1265197#c0 no longer works for this issue and it seems url=javascript:alert(1) results in a blank page.
However It creates a CSS parser issue with chrome-untrusted://new-tab-page/custom_background_image?url=https://a.a/) that should be escaped correctly.

Please tell me if https://crbug.com/chromium/1265197#c27 should be a separate issue as I dont know if its duplicate, invalid or the XSS is just being fixed first.


### dp...@chromium.org (2021-11-03)

> However It creates a CSS parser issue with chrome-untrusted://new-tab-page/custom_background_image?url=https://a.a/) that should be escaped correctly.

Can you elaborate? Besides the network request to "https://a.a/" failing, I don't see any other issue when I try loading this URL locally.

### nd...@protonmail.com (2021-11-03)

background-image: url(https://a.a/)); is invalid css.

### dp...@chromium.org (2021-11-03)

Ack. I don't think the |url| query parameter should be responsible for correcting incorrect URLs. As long as it's not creating any security issues, I don't think it matters for this bug. FWIW the issue in #30 happens before the fix that landed above anyway.

### nd...@protonmail.com (2021-11-04)

[Comment Deleted]

### nd...@protonmail.com (2021-11-05)

[Comment Deleted]

### nd...@protonmail.com (2021-11-09)

[Comment Deleted]

### dp...@chromium.org (2021-11-10)

> @danakj: Can you help verifying that the fix above actually prevents the original issue?

I have not heard back. Marking this as Fixed based on my own local testing. Please re-open if that's not the case.

### nd...@protonmail.com (2021-11-10)

[Comment Deleted]

### dp...@chromium.org (2021-11-10)

+devlin

> I was expecting this issue to be about the extension navigation policy,

Perhaps best to file a separate bug for the other ways to exploit the extension navigation policy?

### nd...@protonmail.com (2021-11-10)

[Comment Deleted]

### nd...@protonmail.com (2021-11-10)

I created https://bugs.chromium.org/p/chromium/issues/detail?id=1269049 for it :)

### [Deleted User] (2021-11-12)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-12)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-12)

Requesting merge to extended stable M94 because latest trunk commit (937561) appears to be after extended stable branch point (911515).

Requesting merge to stable M95 because latest trunk commit (937561) appears to be after stable branch point (920003).

Requesting merge to beta M96 because latest trunk commit (937561) appears to be after beta branch point (929512).

Not requesting merge to dev (M97) because latest trunk commit (937561) appears to be prior to dev branch point (938553). If this is incorrect, please replace the Merge-NA-97 label with Merge-Request-97. If other changes are required to fix this bug completely, please request a merge if necessary.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-11-12)

Merge review required: M96 has already been cut for stable release.

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
Owners: govind (Android), harrysouders (iOS), dgagnon (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-11-12)

Merge review required: M95 is already shipping to stable.

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
Owners: benmason (Android), harrysouders (iOS), None (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-11-12)

Merge review required: M94 is already shipping to stable.

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
Owners: govind (Android), harrysouders (iOS), matthewjoseph (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### dp...@chromium.org (2021-11-15)

tiborg@ can you or someone else from the NTP team take over the remaining work of merging this to previous releases as needed?

### ts...@chromium.org (2021-11-15)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-11-16)

sorry sheriffbot, no merge to M94 or M95 necessary, no further releases of either is planned 

### am...@chromium.org (2021-11-16)

Merge approved to M97, please merge to branch 4692 as soon as possible

### am...@chromium.org (2021-11-16)

Merge approved to M96, please merge to branch 4664 as soon as possible 

### ti...@chromium.org (2021-11-16)

Change landed before M-97 branched.

### gi...@appspot.gserviceaccount.com (2021-11-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/96d764cc45aeccb278a194dd6168718a2972c23a

commit 96d764cc45aeccb278a194dd6168718a2972c23a
Author: dpapad <dpapad@chromium.org>
Date: Tue Nov 16 20:29:45 2021

NTP: Replace $i18nRaw{} usages with $i18n{} in new_tab_page/untrusted/

(cherry picked from commit c812dc628e7a25349b7e63d64da5aaebe8ac2ead)

Bug: 1265197
Change-Id: I3c483eaeb352e38f3b51a2de2558e38e67cf7386
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3258181
Auto-Submit: dpapad <dpapad@chromium.org>
Commit-Queue: dpapad <dpapad@chromium.org>
Reviewed-by: Tibor Goldschwendt <tiborg@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#937561}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3285839
Commit-Queue: Tibor Goldschwendt <tiborg@chromium.org>
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Auto-Submit: Tibor Goldschwendt <tiborg@chromium.org>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/4664@{#1076}
Cr-Branched-From: 24dc4ee75e01a29d390d43c9c264372a169273a7-refs/heads/main@{#929512}

[modify] https://crrev.com/96d764cc45aeccb278a194dd6168718a2972c23a/chrome/browser/resources/new_tab_page/untrusted/background_image.html
[modify] https://crrev.com/96d764cc45aeccb278a194dd6168718a2972c23a/chrome/browser/resources/new_tab_page/untrusted/image.html


### jd...@chromium.org (2021-11-17)

Since you can't navigate to chrome-untrusted:// URLs directly, this requires direct user action to paste something into the omnibox. That's a big burden, and you can already do arbitrarily-bad stuff on a page using javascript: snippets pasted into the omnibox.

It's good that we fixed it, but this is probably Sev-Low.

### [Deleted User] (2021-11-17)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### nd...@protonmail.com (2021-11-17)

This is exploitable from any browser extension I know it seems no one cares about this case.
Also anything on chrome-untrusted:// can navigate to the url this seems like a valid issue since its meant to be "untrusted"

### am...@google.com (2021-11-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@google.com (2021-11-17)

Hello, the Chrome VRP has decided to reward you $500 for this report. We appreciate your efforts in reporting this issue to us. 

### nd...@protonmail.com (2021-11-17)

[Comment Deleted]

### nd...@protonmail.com (2021-11-18)

[Comment Deleted]

### nd...@protonmail.com (2021-11-23)

Replying to my comment because Im board :)
Extensions can now longer go to chrome-untrusted:// and from what I can tell the postMessage never gets received.

### am...@google.com (2021-11-24)

[Empty comment from Monorail migration]

### nd...@protonmail.com (2021-11-25)

[Comment Deleted]

### ad...@google.com (2021-12-03)

[Empty comment from Monorail migration]

### ad...@google.com (2021-12-03)

[Empty comment from Monorail migration]

### am...@google.com (2021-12-23)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-16)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1265197?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Internals>Sandbox>SiteIsolation, Platform>Extensions, UI>Browser>NewTabPage, UI>Browser>WebUI]
[Monorail mergedwith: crbug.com/chromium/1270137]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057777)*
