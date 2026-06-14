# Security: URL in Omnibox doesn't always match page content (repro 897641)

| Field | Value |
|-------|-------|
| **Issue ID** | [40095628](https://issues.chromium.org/issues/40095628) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>Extensions |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | tj...@chromium.org |
| **Created** | 2019-07-06 |
| **Bounty** | $1,000.00 |

## Description

Chrome Version: 77.0.3844.0 canary  

Operating System: Mac

**REPRODUCTION CASE**  

I’m able to repro the <https://crbug.com/chromium/897641>.

1. Install the attached extension.
2. the extension will open a new tab
3. Observe, that URL is updated incorrectly to google.com:1010 but content page still shows extension\_page.html

Note: Loading random websites with non-existent ports takes ~50 seconds for Chrome to show a 'This site can’t be reached' error msg. Which could still be enough time to trick some users.

## Attachments

- [Screen Shot 2019-07-06 at 17.15.27.png](attachments/Screen Shot 2019-07-06 at 17.15.27.png) (image/png, 69.0 KB)
- [poc.zip](attachments/poc.zip) (application/octet-stream, 5.0 KB)
- [background.js](attachments/background.js) (text/plain, 463 B)
- [extension_page.html](attachments/extension_page.html) (text/plain, 132 B)
- [manifest.json](attachments/manifest.json) (text/plain, 337 B)

## Timeline

### ch...@gmail.com (2019-07-06)

[Empty comment from Monorail migration]

### li...@chromium.org (2019-07-08)

Adding labels based on https://crbug.com/chromium/897641 and assigning to rdevlin.cronin, who looked at the last bug. Devlin, would you be able to help take a look? Thanks!

[Monorail components: Platform>Extensions]

### sh...@chromium.org (2019-07-09)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rd...@chromium.org (2019-07-12)

So, the basic flow here is:

Extension loads extension_page.html (internal extension page) in a tab
Extension navigates tab to google.com:1010 with tabs.update()
Extension intercepts navigation with webRequest and redirects to `javascript:`.
Page remains on extension_page.html, but omnibox says google.com:1010

There's two main issues here:
1. tabs.update() updates the tab as though it's a user navigation, which results in the URL in the omnibox being immediately changed to the pendingUrl.  There's some good discussion about this around [1] [2] [3] [4].  TL;DR: It'd be great to fix, and it's complicated.  I'd like to pursue this, but realistically, it will be a longer road (tracking down all expectations that change, notifying developers, etc).
2. We don't update the URL when the page is redirected to `javascript:`, even though the last committed URL (and thus the URL the page is displaying) doesn't match the omnibox.  This seems bad, because the same thing could happen if the user were to navigate to a slow-loading site.

@creis, I thought we ran into something similar in https://crbug.com/chromium/897641, which also spanned https://crbug.com/chromium/935175 and https://crbug.com/chromium/941653.  Did we miss a spot?  Is there a good candidate to take that on?

Note also that, while this is definitely bad, the practical security risk is somewhat mitigated.  The extension needs permission to access google.com in order to intercept and redirect the request, so anything they wanted to do through URL spoofing would be equally easily (or more easily) accomplished through script injection.  I'd be inclined to make this severity-low, but am happy to defer to other folks.

[1] https://cs.chromium.org/chromium/src/chrome/browser/extensions/api/tabs/tabs_api.cc?l=1341-1344&rcl=9dff7c8c73cdc0a881492793f486d30ec0c0ec89
[2] https://codereview.chromium.org/2475033002/
[3] https://bugs.chromium.org/p/chromium/issues/detail?id=897641#c2
[4] https://bugs.chromium.org/p/chromium/issues/detail?id=897641#c4

### rd...@chromium.org (2019-07-18)

creis@ is now OOO.  +alexmos@, lukasza@: please see #4.

### rd...@chromium.org (2019-07-26)

Friendly ping: creis@, alexmos@, lukasza@.

### cr...@chromium.org (2019-07-26)

Ah, sorry for missing this earlier.

Long story short, I think this boils down to needing to do option 1 from https://crbug.com/chromium/981628#c4: not showing the pending URL in the address bar when an extension navigates.

Longer explanation:

The attached repro case works, but for a very different reason than you'd expect.  It's triggering a slow navigation to https://www.google.com:1010, which shows up in the address bar because it's browser initiated, and it stays in the address bar for a little while until the navigation times out.  The repro doesn't actually rely at all on the web request API or a javascript: redirect.

The code is copied almost verbatim from https://crbug.com/chromium/897641 from a different reporter, except that targetUrl in background.js is changed from "https://www.google.com/" to "https://www.google.com:1010".  However, because the new URL is missing a trailing slash, the webRequest API rejects it with this error message:
"Unchecked runtime.lastError: 'https://www.google.com:1010' is not a valid URL pattern."

Thus, there's no redirect to javascript: when we navigate to https://www.google.com:1010.  In fact, if there were (by including the slash in "https://www.google.com:1010/"), then the fix for https://crbug.com/chromium/897641 kicks in and there's no URL spoof.  The URL is only visible because it's treated as a browser-initiated navigation.

In other words, the repro boils down to just chrome.tabs.create followed by chrome.tabs.update:

----

var newTabId;
var redirected = false;

chrome.tabs.onUpdated.addListener(function(tabId, changeInfo, tab) {
  if (changeInfo.status === "complete"
  && newTabId === tab.id
  && !redirected) {
    chrome.tabs.update(tab.id, {url: "https://www.google.com:1010", active: true});

    redirected = true;
  }
});

chrome.tabs.create({
  url: chrome.runtime.getURL("extension_page.html"),
  active: false
}, function (tab) {
  newTabId = tab.id;
});

----

(See also the attached minimal repro files.)

Also note that no permissions are needed at all for this, so the mitigating factor from https://crbug.com/chromium/981628#c4 doesn't apply.  (Interestingly, I think that mitigating factor should have applied to https://crbug.com/chromium/897641 now that you mention it, making that one low severity, since the attacker did need script access to the victim site to pull off the URL spoof.  Oh well.)

If there is a mitigating factor, it's that the spoof is temporary, only until the navigation to the bad port times out.  However, that takes a while, so I think it might be worth pursuing that change to make these extension navigations not show in the address bar.

Devlin, do you want to find someone to help push that along?

### cr...@chromium.org (2019-07-29)

nasko@ mentions he's tried to make the proposed change before, but found it was a breaking change for some extensions.  It may still be worth doing an announcement and changing the API behavior to not show the pending URL?

### rd...@chromium.org (2019-07-29)

@7, @8: Thanks for the investigation!  If this is just the slow-load spoof, is the severity + release block still accurate?  (In particular, I worry about our ability to get a change into M77 stable).

This is definitely a breaking change.  There are about a dozen tests that fail by just switching over to make extension navigations renderer-initiated, and also the concern of extensions relying on this behavior (though, hopefully, it's fairly niche).  Unfortunately, it's cropped up enough (and is fundamentally a problem) that I think it is something we'll need to tackle.

tjudkins@, I wonder if this is something you can grab as well?  We can chat about it a bit before you dive in.

### cr...@chromium.org (2019-07-29)

Agreed this doesn't feel like release-block Stable for M77.  Not sure about the severity-- it's a URL spoof, and the mitigating factors are (1) the attacker's extension needs to be installed, (2) the victim site needs to have a slow URL, and (3) the attack only lasts until the URL times out.  However, the port trick can be used on almost any site, and the timeout takes a while, so it mainly comes down to the need to have a malicious extension installed.

I'm inclined to leave as medium.  awhalley@, does that sound right, or do we treat malicious extension issues as low?

### aw...@google.com (2019-07-29)

Medium sounds right, as does targeting M78.  Thanks!

### sh...@chromium.org (2019-07-30)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### na...@chromium.org (2019-07-30)

Just a bit of context on https://crbug.com/chromium/981628#c8. What I tried to do is make a change to the extensions subsystem to move away from GetVisibleURL to GetLastCommittedURL, which changes the semantics of which URL is returned for a pending navigation. I believe making the change to extensions initiated navigations to be renderer-initiated instead of browser will have similar pitfalls, since GetVisibleURL will not return the URL of the pending navigation. As such, I think the potential for breakage and user/extension dev confusion is non-trivial and this change will need to be broadly communicated.
There is also additional potential change of behavior, since browser-initiated navigations can cancel ongoing navigation, while renderer-initiated navigation without user gesture does not. Given that extensions might not have user gesture, that means that the navigations they start can actually fail to cancel ongoing browser-initiated navigation and the result will look like a noop. However, I think this is lower probability event and I think it will be less of a breaking change than the difference in URL reported. Let's try it for M78 and ensure we communicate these changes to extension developers with clarity and enough time for them to update.

### rd...@chromium.org (2019-07-31)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-08-01)

tjudkins: Uh oh! This issue still open and hasn't been updated in the last 25 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### tj...@chromium.org (2019-08-05)

[Empty comment from Monorail migration]

### tj...@chromium.org (2019-08-07)

Adding karandeepb@ to get some input on handling some tests this change impacts.

### sh...@chromium.org (2019-09-11)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-09-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/92389f75d0c3e82e8c938a5eb19a8910db524760

commit 92389f75d0c3e82e8c938a5eb19a8910db524760
Author: Tim Judkins <tjudkins@chromium.org>
Date: Fri Sep 20 21:04:14 2019

[Extensions] Make tabs API update call renderer initiated

This change is to make sure the URL in the Omnibox matches the page
content for navigations made through the tabs API, to make sure that
pending navigations made through the tabs API are not displayed in the
omnibox.
This also involves adding a pending URL entry to the tabs object, which
exposes the current pending URL that has not yet committed, if there
is one.

Bug: 981628, 1000489
Change-Id: I649438987ab11c4389dfbc1ff303c661762ef565
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1737819
Commit-Queue: Tim Judkins <tjudkins@chromium.org>
Reviewed-by: Devlin <rdevlin.cronin@chromium.org>
Reviewed-by: Sam McNally <sammc@chromium.org>
Cr-Commit-Position: refs/heads/master@{#698617}

[modify] https://crrev.com/92389f75d0c3e82e8c938a5eb19a8910db524760/chrome/browser/chromeos/extensions/extension_tab_util_delegate_chromeos.cc
[modify] https://crrev.com/92389f75d0c3e82e8c938a5eb19a8910db524760/chrome/browser/chromeos/extensions/extension_tab_util_delegate_chromeos.h
[modify] https://crrev.com/92389f75d0c3e82e8c938a5eb19a8910db524760/chrome/browser/extensions/api/messaging/chrome_messaging_delegate.cc
[modify] https://crrev.com/92389f75d0c3e82e8c938a5eb19a8910db524760/chrome/browser/extensions/api/sessions/sessions_api.cc
[modify] https://crrev.com/92389f75d0c3e82e8c938a5eb19a8910db524760/chrome/browser/extensions/api/tabs/tabs_api.cc
[modify] https://crrev.com/92389f75d0c3e82e8c938a5eb19a8910db524760/chrome/browser/extensions/api/tabs/tabs_constants.cc
[modify] https://crrev.com/92389f75d0c3e82e8c938a5eb19a8910db524760/chrome/browser/extensions/api/tabs/tabs_constants.h
[modify] https://crrev.com/92389f75d0c3e82e8c938a5eb19a8910db524760/chrome/browser/extensions/api/tabs/tabs_test.cc
[modify] https://crrev.com/92389f75d0c3e82e8c938a5eb19a8910db524760/chrome/browser/extensions/api/web_request/web_request_apitest.cc
[modify] https://crrev.com/92389f75d0c3e82e8c938a5eb19a8910db524760/chrome/browser/extensions/extension_function_test_utils.cc
[modify] https://crrev.com/92389f75d0c3e82e8c938a5eb19a8910db524760/chrome/browser/extensions/extension_function_test_utils.h
[modify] https://crrev.com/92389f75d0c3e82e8c938a5eb19a8910db524760/chrome/browser/extensions/extension_tab_util.cc
[modify] https://crrev.com/92389f75d0c3e82e8c938a5eb19a8910db524760/chrome/browser/extensions/extension_tab_util.h
[modify] https://crrev.com/92389f75d0c3e82e8c938a5eb19a8910db524760/chrome/browser/extensions/extension_tab_util_unittest.cc
[modify] https://crrev.com/92389f75d0c3e82e8c938a5eb19a8910db524760/chrome/browser/extensions/menu_manager.cc
[modify] https://crrev.com/92389f75d0c3e82e8c938a5eb19a8910db524760/chrome/common/extensions/api/tabs.json
[modify] https://crrev.com/92389f75d0c3e82e8c938a5eb19a8910db524760/chrome/common/extensions/api/windows.json
[modify] https://crrev.com/92389f75d0c3e82e8c938a5eb19a8910db524760/chrome/common/extensions/docs/templates/intros/tabs.html
[modify] https://crrev.com/92389f75d0c3e82e8c938a5eb19a8910db524760/chrome/common/extensions/docs/templates/intros/windows.html
[modify] https://crrev.com/92389f75d0c3e82e8c938a5eb19a8910db524760/chrome/common/extensions/docs/templates/private/intro_tables/tabs_permissions.html
[modify] https://crrev.com/92389f75d0c3e82e8c938a5eb19a8910db524760/chrome/common/extensions/docs/templates/private/intro_tables/windows_permissions.html
[modify] https://crrev.com/92389f75d0c3e82e8c938a5eb19a8910db524760/chrome/test/data/extensions/api_test/extension_options/embed_self/test.js
[modify] https://crrev.com/92389f75d0c3e82e8c938a5eb19a8910db524760/chrome/test/data/extensions/api_test/native_bindings/extension/background.js
[modify] https://crrev.com/92389f75d0c3e82e8c938a5eb19a8910db524760/chrome/test/data/extensions/api_test/runtime/open_options_page/test.js
[modify] https://crrev.com/92389f75d0c3e82e8c938a5eb19a8910db524760/chrome/test/data/extensions/api_test/runtime/uninstall_url/test.js
[modify] https://crrev.com/92389f75d0c3e82e8c938a5eb19a8910db524760/chrome/test/data/extensions/api_test/service_worker/worker_based_background/basic/service_worker_background.js
[modify] https://crrev.com/92389f75d0c3e82e8c938a5eb19a8910db524760/chrome/test/data/extensions/api_test/service_worker/worker_based_background/tabs_basic/service_worker_background.js
[modify] https://crrev.com/92389f75d0c3e82e8c938a5eb19a8910db524760/chrome/test/data/extensions/api_test/service_worker/worker_based_background/tabs_events/service_worker_background.js
[modify] https://crrev.com/92389f75d0c3e82e8c938a5eb19a8910db524760/chrome/test/data/extensions/api_test/tabs/basics/a.html
[modify] https://crrev.com/92389f75d0c3e82e8c938a5eb19a8910db524760/chrome/test/data/extensions/api_test/tabs/basics/b.html
[modify] https://crrev.com/92389f75d0c3e82e8c938a5eb19a8910db524760/chrome/test/data/extensions/api_test/tabs/basics/c.html
[modify] https://crrev.com/92389f75d0c3e82e8c938a5eb19a8910db524760/chrome/test/data/extensions/api_test/tabs/basics/crud.js
[modify] https://crrev.com/92389f75d0c3e82e8c938a5eb19a8910db524760/chrome/test/data/extensions/api_test/tabs/basics/crud2.js
[modify] https://crrev.com/92389f75d0c3e82e8c938a5eb19a8910db524760/chrome/test/data/extensions/api_test/tabs/basics/d.html
[modify] https://crrev.com/92389f75d0c3e82e8c938a5eb19a8910db524760/chrome/test/data/extensions/api_test/tabs/basics/e.html
[modify] https://crrev.com/92389f75d0c3e82e8c938a5eb19a8910db524760/chrome/test/data/extensions/api_test/tabs/basics/events.js
[modify] https://crrev.com/92389f75d0c3e82e8c938a5eb19a8910db524760/chrome/test/data/extensions/api_test/tabs/basics/f.html
[modify] https://crrev.com/92389f75d0c3e82e8c938a5eb19a8910db524760/chrome/test/data/extensions/api_test/tabs/basics/move.js
[modify] https://crrev.com/92389f75d0c3e82e8c938a5eb19a8910db524760/chrome/test/data/extensions/api_test/tabs/basics/query.js
[modify] https://crrev.com/92389f75d0c3e82e8c938a5eb19a8910db524760/chrome/test/data/extensions/api_test/tabs/basics/update.js
[modify] https://crrev.com/92389f75d0c3e82e8c938a5eb19a8910db524760/chrome/test/data/extensions/api_test/tabs/host_permission/test.js
[modify] https://crrev.com/92389f75d0c3e82e8c938a5eb19a8910db524760/chrome/test/data/extensions/api_test/tabs/no_permissions/test.js
[modify] https://crrev.com/92389f75d0c3e82e8c938a5eb19a8910db524760/chrome/test/data/extensions/api_test/webrequest/framework.js
[modify] https://crrev.com/92389f75d0c3e82e8c938a5eb19a8910db524760/chrome/test/data/extensions/api_test/webrequest_public_session/framework.js
[modify] https://crrev.com/92389f75d0c3e82e8c938a5eb19a8910db524760/ui/file_manager/integration_tests/file_manager/open_sniffed_files.js


### rd...@chromium.org (2019-09-21)

Thanks for the hard work here, tjudkins@!  I know this was a tricky one.

Can you make sure to work with simeonv@ to announce these changes in chromium-extensions@?

creis@, nasko@: I'm also curious if this is one we should punt to M79 (which is where it landed by default).  It's been around forever, and that would give extension authors until December to update, instead of until late October.  But, if we're worried about folks snooping commits, that makes sense, too.  Let me know what you think.

### ch...@gmail.com (2019-09-22)

Verified on Chromium 79.0.3921.0 refs/heads/master@{#698776}. Fixed.

### cr...@chromium.org (2019-09-23)

Yes, thanks tjudkins@!  Also, I agree that r698617 doesn't seem like a very mergeable CL.  I'm ok with this staying in M79+ given how long it's been around and that it's limited to malicious extensions.  (Andrew, feel free to chime in if you disagree and want to encourage a merge, though.)

### sh...@chromium.org (2019-09-24)

[Empty comment from Monorail migration]

### na...@google.com (2019-09-27)

[Empty comment from Monorail migration]

### na...@google.com (2019-10-04)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2019-10-04)

Congrats! The Panel decided to reward $1,000 for this report :) 

### na...@google.com (2019-10-07)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-11-01)

Not requesting merge to beta (M79) because latest trunk commit (698617) appears to be prior to beta branch point (706915). If this is incorrect, please replace the Merge-na label with Merge-Request-79. If other changes are required to fix this bug completely, please request a merge if necessary.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-12-31)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2019-12-31)

This issue was migrated from crbug.com/chromium/981628?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095628)*
