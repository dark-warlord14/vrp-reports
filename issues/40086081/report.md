# Security: XSS in chrome://apps (NTP) after drag and drop

| Field | Value |
|-------|-------|
| **Issue ID** | [40086081](https://issues.chromium.org/issues/40086081) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Unknown |
| **Reporter** | ro...@robwu.nl |
| **Assignee** | ro...@robwu.nl |
| **Created** | 2016-11-25 |
| **Bounty** | $500.00 |

## Description

Chrome version: 54.0.2840.90 (stable), 57.0.2933.0 (latest)

A new tab page (chrome://apps) uses the result of drag and drop in an unsafe way (assigning to innerHTML of a element from an active document) - this is a XSS vulnerability. The page has no content security policy to mitigate this, and the NTP has many interesting APIs, including but not limited to:
- Enumerating the browsing history through favicons
- Querying who is signed in in Chrome
- Opening restricted URLs (including URLs that normally requires the user to manually type the URL, e.g. chrome://kill)
- Disabling extensions
- Launching apps
- Filling the preferences database with junk (AppLauncherHandler::HandleSaveAppPageName does not validate the bounds on the parameters)

Steps to reproduce:
1. Open index.html
2. Open the New Tab Page and click on Apps (or visit chrome://apps directly).
3. Drag any link from index.html to the area with the app tiles (e.g. the webstore tile).


Note: In the latest version of Chrome (57.0.2933.0) I see that there is a CSP, but for some reason it only blocks images, and not inline scripts: Content-Security-Policy: img-src chrome://extension-icon chrome://theme chrome://resources data:

[1] https://chromium.googlesource.com/chromium/src/+/a03615942fb43dd1d90af02ef3b45b95da2f7f2a/chrome/browser/resources/ntp4/apps_page.js#710

## Attachments

- [index.html](attachments/index.html) (text/plain, 1017 B)

## Timeline

### fi...@chromium.org (2016-11-25)

+ treib (to double check that we don't own this)

chrome://apps isn't owned by the NTP -> adding ChromeApps team

[Monorail components: Platform>Apps>Launcher]

### tr...@chromium.org (2016-11-25)

Yup, chrome://apps hasn't been part of the NTP for a long time. +dbeam

### ro...@robwu.nl (2016-11-25)

Patch: https://codereview.chromium.org/2527413002

The patch fixes the XSS issue and removes the ability to launch any powerful URL.
The other APIs are necessary for the NTP/app launcher to function, so I did not touch them.

### bu...@chromium.org (2016-11-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/15120efa4b9394086d687086e443f47290b5170a

commit 15120efa4b9394086d687086e443f47290b5170a
Author: rob <rob@robwu.nl>
Date: Tue Nov 29 09:38:50 2016

Fix XSS in app launcher and remove use of unvalidated URL

The third parameter of "launchApp" is only used for the webstore app,
and used to append utm_source=chrome-ntp-icon to the app URL.
But the launchApp handler did not validate that the URL is safe.
To fix that issue, I specialize the parameter for launchApp: It now takes the
source string ("chrome-ntp-icon") instead of a URL without validation.

BUG=668665
TEST=Manually using test case from bug report. Also opened the app launcher and
verified that clicking on the Webstore icon still leads to the same place.
CQ_INCLUDE_TRYBOTS=master.tryserver.chromium.linux:closure_compilation

Review-Url: https://codereview.chromium.org/2527413002
Cr-Commit-Position: refs/heads/master@{#434939}

[modify] https://crrev.com/15120efa4b9394086d687086e443f47290b5170a/chrome/browser/resources/ntp4/apps_page.js
[modify] https://crrev.com/15120efa4b9394086d687086e443f47290b5170a/chrome/browser/ui/webui/ntp/app_launcher_handler.cc


### ji...@chromium.org (2016-11-29)

[Empty comment from Monorail migration]

### ro...@robwu.nl (2016-11-30)

Verified fixed in 57.0.2937.0 on Canary (Windows).

### di...@chromium.org (2016-11-30)

Your change meets the bar and is auto-approved for M56 (branch: 2924)

### bu...@chromium.org (2016-11-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/40a0d587a65320cba1eab074774740c2f7a8a67b

commit 40a0d587a65320cba1eab074774740c2f7a8a67b
Author: Rob Wu <rob@robwu.nl>
Date: Wed Nov 30 11:40:37 2016

Fix XSS in app launcher and remove use of unvalidated URL

The third parameter of "launchApp" is only used for the webstore app,
and used to append utm_source=chrome-ntp-icon to the app URL.
But the launchApp handler did not validate that the URL is safe.
To fix that issue, I specialize the parameter for launchApp: It now takes the
source string ("chrome-ntp-icon") instead of a URL without validation.

BUG=668665
TEST=Manually using test case from bug report. Also opened the app launcher and
verified that clicking on the Webstore icon still leads to the same place.
CQ_INCLUDE_TRYBOTS=master.tryserver.chromium.linux:closure_compilation

Review-Url: https://codereview.chromium.org/2527413002
Cr-Commit-Position: refs/heads/master@{#434939}
(cherry picked from commit 15120efa4b9394086d687086e443f47290b5170a)

Review URL: https://codereview.chromium.org/2542593002 .

Cr-Commit-Position: refs/branch-heads/2924@{#186}
Cr-Branched-From: 3a87aecc31cd1ffe751dd72c04e5a96a1fc8108a-refs/heads/master@{#433059}

[modify] https://crrev.com/40a0d587a65320cba1eab074774740c2f7a8a67b/chrome/browser/resources/ntp4/apps_page.js
[modify] https://crrev.com/40a0d587a65320cba1eab074774740c2f7a8a67b/chrome/browser/ui/webui/ntp/app_launcher_handler.cc


### sh...@chromium.org (2016-11-30)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-12-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-12-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-12-12)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-12-12)

[Empty comment from Monorail migration]

### aw...@google.com (2016-12-19)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-24)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-03-08)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-28)

[Empty comment from Monorail migration]

### is...@google.com (2018-07-28)

This issue was migrated from crbug.com/chromium/668665?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40086081)*
