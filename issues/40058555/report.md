# Security: CSS keylogger extension using PageStateMatcher and chrome.action.openPopup()

| Field | Value |
|-------|-------|
| **Issue ID** | [40058555](https://issues.chromium.org/issues/40058555) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>Extensions |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | st...@gmail.com |
| **Assignee** | rd...@chromium.org |
| **Created** | 2022-01-21 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**  

An extension without the permission to read the page's content can exfiltrate sensitive values using DeclarativeContent CSS selectors and chrome.action.openPopup().

**VERSION**  

Chrome Version: 99.0.4844.0 + dev  

Operating System: Windows 10

**REPRODUCTION CASE**

1. Install the extension and open the target page.
2. You will find the exfiltrated password value in the extension console.

chrome.declarativeContent API [0](https://developer.chrome.com/docs/extensions/reference/declarativeContent) allows to enable the extension action popup based on a CSS selector on the focused page.

First, we disable the action popup.

chrome.action.disable();

This code will enable the popup only if the current page has an iframe matching the specified selector.

chrome.declarativeContent.onPageChanged.addRules([{  

conditions: [  

new chrome.declarativeContent.PageStateMatcher({  

pageUrl: { hostEquals: 'example.com', schemes: ['https'] },  

css: ['iframe[src^="https://example.com/?access\_key=a"]']  

}),  

], actions: [  

new chrome.declarativeContent.ShowAction(),  

]  

}]);

If we try to open the popup programmatically [1](https://developer.chrome.com/docs/extensions/reference/action/#method-openPopup) and it fails with an error, it means the selector did not match. If no error is thrown, the selector was matched.

try {  

await chrome.action.openPopup();  

} catch (e) {  

error = true;  

}

Now, we can use binary search to quickly find the exact value of the attribute. In my testing, 50 queries per second works reliably.

We can use this technique to extract input values/passwords\*, leak access tokens from iframes and other sensitive data.

\* By default, CSS selectors won't match [value=...] attributes [2](https://css-tricks.com/css-keylogger/), but libraries like React set the value attribute directly on the element, making this attack feasible on a large number of websites.

**CREDIT INFORMATION**  

Reporter credit: Thomas Orlita

## Attachments

- [background.js](attachments/background.js) (text/plain, 2.0 KB)
- [manifest.json](attachments/manifest.json) (text/plain, 292 B)
- [popup.html](attachments/popup.html) (text/plain, 32 B)
- [popup.js](attachments/popup.js) (text/plain, 15 B)
- [poc.mp4](attachments/poc.mp4) (video/mp4, 556.5 KB)

## Timeline

### [Deleted User] (2022-01-21)

[Empty comment from Monorail migration]

### aj...@google.com (2022-01-21)

Hi Devlin could you take a look at this one there is a good video and poc. This might be a privacy issue, but I feel it is also a permissions bypass for extensions.

[Monorail components: Platform>Extensions]

### [Deleted User] (2022-01-21)

[Empty comment from Monorail migration]

### rd...@chromium.org (2022-01-22)

Oh, that's cool!  Great find!

Luckily, this API is still restricted to dev channel [1], so this won't reproduce on stable.  But definitely something we should fix.  I think a fairly straightforward solution would be to not consider a declaratively-visible popup for the API.  I'll see if I can do that next week.

[1] https://source.chromium.org/chromium/chromium/src/+/main:chrome/common/extensions/api/_api_features.json;l=66;drc=f568aedcc729dbe7746eebe57a1723ae0760220b

### [Deleted User] (2022-01-22)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-01-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/6f1205eddca62b071cc2ca2ed5d82d7fc1b5a89b

commit 6f1205eddca62b071cc2ca2ed5d82d7fc1b5a89b
Author: Devlin Cronin <rdevlin.cronin@chromium.org>
Date: Thu Jan 27 17:38:57 2022

[Extensions] Don't allow opening a popup for a declarative-shown action

Actions can be declaratively shown using the chrome.declarativeContent
API, where they can be active on a tab for certain CSS selectors. This
information should not be returned to the extension, since it can leak
information about the page.

The action.openPopup() (and browserAction.openPopup()) API will open a
popup on a given tab if the action is visible on the tab, and will
otherwise fail and return an error. Adjust this so that the API doesn't
include declarative action shows so that extensions can't indirectly
retrieve this information.

Adjust this for both APIs (action.openPopup() and
browserAction.openPopup()), and add a regression test.

Bug: 1289846
Change-Id: Ib9ea8b5474df2222287b972db7dbfe97d46dcbbc
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3413808
Reviewed-by: David Bertoni <dbertoni@chromium.org>
Commit-Queue: Devlin Cronin <rdevlin.cronin@chromium.org>
Cr-Commit-Position: refs/heads/main@{#964109}

[modify] https://crrev.com/6f1205eddca62b071cc2ca2ed5d82d7fc1b5a89b/extensions/browser/extension_action.cc
[modify] https://crrev.com/6f1205eddca62b071cc2ca2ed5d82d7fc1b5a89b/extensions/browser/extension_action_unittest.cc
[modify] https://crrev.com/6f1205eddca62b071cc2ca2ed5d82d7fc1b5a89b/chrome/browser/extensions/api/extension_action/extension_action_api.cc
[modify] https://crrev.com/6f1205eddca62b071cc2ca2ed5d82d7fc1b5a89b/extensions/browser/extension_action.h
[modify] https://crrev.com/6f1205eddca62b071cc2ca2ed5d82d7fc1b5a89b/chrome/browser/extensions/api/extension_action/extension_action_api_interactive_uitest.cc


### rd...@chromium.org (2022-01-27)

This should be fixed.

Since the API is restricted to dev channel, this probably doesn't need a merge (even though the original change landed in M99 and the fix was in M100).  I'd also lean towards downgrading the severity to "low" since a) this requires extension installation and b) it requires dev channel, but I'll leave that to the security folks. : )

Thank you again for the report!

### [Deleted User] (2022-01-28)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-28)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-28)

Requesting merge to beta M98 because latest trunk commit (964109) appears to be after beta branch point (950365).

Requesting merge to dev M99 because latest trunk commit (964109) appears to be after dev branch point (961656).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-28)

Merge approved: your change passed merge requirements and is auto-approved for M99. Please go ahead and merge the CL to branch 4844 (refs/branch-heads/4844) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: benmason (Android), harrysouders (iOS), cindyb (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-28)

Merge review required: M98 has already been cut for stable release.

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

### rd...@chromium.org (2022-01-28)

Wow, sheriffbot has been having a very interesting conversation with itself! ; )

I think there's no need for a merge here.  See comment c#8:

> Since the API is restricted to dev channel, this probably doesn't need a merge

### [Deleted User] (2022-01-30)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2022-03-03)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-03-03)

Congratulations, Thomas! The VRP Panel has decided to award you $5,000 for this report. Thank you for your efforts and good work! 

### am...@google.com (2022-03-04)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-03-28)

[Empty comment from Monorail migration]

### am...@google.com (2022-03-29)

[Empty comment from Monorail migration]

### gm...@google.com (2022-03-31)

Not Applicable to LTS-96 per https://crbug.com/chromium/1289846#c4

### [Deleted User] (2022-05-06)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2022-07-22)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-29)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1289846?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058555)*
