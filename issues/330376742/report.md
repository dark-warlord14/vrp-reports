# Security: HTML injection in chrome://browser-switch/

| Field | Value |
|-------|-------|
| **Issue ID** | [330376742](https://issues.chromium.org/issues/330376742) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Enterprise>BrowserSwitcher |
| **Platforms** | Linux, Mac, Windows |
| **Reporter** | ol...@gmail.com |
| **Assignee** | ni...@chromium.org |
| **Created** | 2024-03-19 |
| **Bounty** | $1,000.00 |

## Description

VULNERABILITY DETAILS
The "url" query parameter of the chrome://browser-switch allows HTML injection when the value is a file:/// scheme URL. This vulnerability could be exploited to craft a malicious link that, when opened, displays a convincing phishing message along with a download link. 
Any attempt of script injecting was blocked thanks to chrome://resources/js/parse_html_subset.js. 

VERSION
Chrome Version: 122.0.6261.129 stable
Operating System: Windows 11 Version 22H2

REPRODUCTION CASE
Go to the following link:
chrome://browser-switch/?url=file:///BUG1337<br><strong>To fix this issue please download and open the following file: <a href="https://www.example.com">Download</a></strong><!-- 

In a real life situation, this bug could be exploited by any Chrome extension with the "tabs" permission. A simple extension demonstrating this exploit is attached.


CREDIT INFORMATION
Reporter credit: Oleg 

## Attachments

- [background.js](attachments/background.js) (text/javascript, 218 B)
- [manifest.json](attachments/manifest.json) (application/json, 195 B)
- [1337.png](attachments/1337.png) (image/png, 84.7 KB)

## Timeline

### ni...@chromium.org (2024-03-21)

> This vulnerability could be exploited to craft a malicious link that, when opened, displays a convincing phishing message along with a download link.

Seems like a minor issue TBH. The HTML is sanitized, so you can't inject arbitrary HTML (as you point out).

Meanwhile, an extension could already open a new tab pointing to (a) any page on the web, or (b) a data:text/html URL, which *can* contain arbitrary HTML. Seems easier to phish a user that way.

```
chrome.tabs.create({url:'data:text/html,<h1>phishing</h1><script>alert("HELLO WORLD")</script>'})
```

### ol...@gmail.com (2024-03-21)

Thank you for your fast response.
This issue shares similarities with the problem outlined in https://issues.chromium.org/40059860, where HTML injection occurred through the extension name field, although that scenario is less likely than the current case.
In both instances, the reported problem involves the same injected payload.
Additionally, this phishing message stands out from the example you provided because it is hosted under a chrome:// URL, a type of URL typically considered highly trusted. 
An extension should not have the capability to inject or modify HTML content in Chrome's web UI pages.
As a result, users may be more likely to click on the link, assuming it is safe.

### ni...@chromium.org (2024-03-21)

In any case, it's worth fixing. crrev.com/c/5385550 is out for review. I'll let the security team make the decision WRT severity

### dc...@chromium.org (2024-03-22)

At best, I have trouble seeing this as anything more than medium (which is how it's already triaged).

### dc...@chromium.org (2024-03-22)

Based on <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/webui/chrome_web_ui_controller_factory.cc;l=758;drc=2e48e9c195ad24e45785d82724ea44412f307ac4>, this looks to only be reachable on Win+Mac+Linux.

### ap...@google.com (2024-03-22)

Project: chromium/src
Branch: main

commit 3e95c470f860dbc0e20c014bbffabb1d892392db
Author: Nicolas Ouellet-Payeur <nicolaso@chromium.org>
Date:   Fri Mar 22 14:50:07 2024

    [BrowserSwitcher] Escape URLs on chrome://browser-switch
    
    Fixed: 330376742
    Change-Id: Ib21cc29c8ba063bb39e74359c197c9ac7e8bb637
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5385550
    Reviewed-by: Julian Pastarmov <pastarmovj@chromium.org>
    Commit-Queue: Nicolas Ouellet-Payeur <nicolaso@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1276868}

M       chrome/browser/resources/browser_switch/app.ts

https://chromium-review.googlesource.com/5385550


### ni...@chromium.org (2024-03-22)

> Based on https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/webui/chrome_web_ui_controller_factory.cc;l=758;drc=2e48e9c195ad24e45785d82724ea44412f307ac4, this looks to only be reachable on Win+Mac+Linux.

Correct. This page is available on Windows, Mac, and desktop Linux

### pe...@google.com (2024-03-22)

Setting milestone because of s2 severity.

### pe...@google.com (2024-03-22)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### pe...@google.com (2024-03-22)

Requesting merge to beta (M124) because latest trunk commit (1276868) appears to be after beta branch point (1274542).
Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


### pe...@google.com (2024-03-23)

Merge review required: M124 is already shipping to beta.

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
Owners: eakpobaro (Android), eakpobaro (iOS), obenedict (ChromeOS), danielyip (Desktop)

### ni...@chromium.org (2024-03-25)

1. Security issue
2. crrev.com/c/5385550
3. Yes
4. Not a new feature
5. N/A, desktop Chrome only
6. No manual verification needed

### am...@chromium.org (2024-03-28)

<https://crrev.com/5385550> approved for backmerge to M124, please merge to M124 Beta -- branch 6367 -- at your earliest convenience

### pe...@google.com (2024-04-02)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ap...@google.com (2024-04-02)

Project: chromium/src
Branch: refs/branch-heads/6367

commit 5b5c6f663855fec0f8a86fd46d974311c2636c4e
Author: Nicolas Ouellet-Payeur <nicolaso@chromium.org>
Date:   Tue Apr 02 12:06:26 2024

    [BrowserSwitcher] Escape URLs on chrome://browser-switch
    
    (cherry picked from commit 3e95c470f860dbc0e20c014bbffabb1d892392db)
    
    Fixed: 330376742
    Change-Id: Ib21cc29c8ba063bb39e74359c197c9ac7e8bb637
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5385550
    Reviewed-by: Julian Pastarmov <pastarmovj@chromium.org>
    Commit-Queue: Nicolas Ouellet-Payeur <nicolaso@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1276868}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5412673
    Owners-Override: Daniel Yip <danielyip@google.com>
    Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Auto-Submit: Daniel Yip <danielyip@google.com>
    Cr-Commit-Position: refs/branch-heads/6367@{#452}
    Cr-Branched-From: d158c6dc6e3604e6f899041972edf26087a49740-refs/heads/main@{#1274542}

M       chrome/browser/resources/browser_switch/app.ts

https://chromium-review.googlesource.com/5412673


### am...@google.com (2024-04-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2024-04-11)

Thank you for the report, Oleg! The Chrome VRP Panel has decided to award you $1,000 based on the limited security impact and potential for user harm presented by this issue in this report. This was still an issue worth fixing, and since were able to make a security relevant change, we did want to reward you for this issue. A member of the Google finance team (p2p-vrp) will be in touch with you soon to arrange payment. Thank you for your efforts and reporting this issue to us!

### pe...@google.com (2024-06-29)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/330376742)*
