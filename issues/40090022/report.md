# Security: privileged XSS in chrome-devtools://devtools/remote with old frontend (insufficient validation of remoteFrontendUrl)

| Field | Value |
|-------|-------|
| **Issue ID** | [40090022](https://issues.chromium.org/issues/40090022) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Platform>DevTools |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ro...@robwu.nl |
| **Assignee** | ro...@robwu.nl |
| **Created** | 2017-12-31 |
| **Bounty** | $2,500.00 |

## Description

**VULNERABILITY DETAILS**  

chrome-devtools://devtools/remote/ loads remote resources via chrome-devtools-frontend.appspot.com.  

This site hosts old versions of the DevTools frontend, including several versions with a XSS vulnerability, e.g. <https://chrome-devtools-frontend.appspot.com/serve_rev/@191797/devtools.html>  

Basically: <iframe src='[urldecoded remoteFrontEndUrl][rest of query string]'></iframe>

devtools\_ui\_bindings.cc has validation, but SanitizeFrontendQueryParam [1] is not sufficiently strict:

- ws and service-backend can contain anything except for ? and &.
- remoteFrontendUrl's reference fragment can contain anything (scheme, host, path and query string are strictly validated).

This is sufficient to construct a chrome-devtools:-URL that

1. exploits the XSS vulnerability and
2. bypasses the XSS auditor
3. grants the XSS payload access to privileged APIs (local file and network access)  
   
   (including the ability to have persistent XSS in the DevTools, e.g. via watch expressions)

This vulnerability can be exploited as follows:

- Via vulerabilities that allow web pages to open privileged URLs, e.g. <https://crbug.com/chromium/798096>
- Via Chrome extensions (that intentionally open such URLs).
- Via Chrome extensions (that inadvertently open such URLs, by performing navigations on behalf of external/network request - this is not uncommon and has happened even in Google-authored extensions)
- Via the omnibox (pasting or drag-and-drop - <https://crbug.com/chromium/149877>).

**VERSION**  

Chrome Version: 63.0.3239.108 (stable) + 65.0.3309.0 (canary)

**REPRODUCTION CASE**  

Paste the following URL in the omnibox:  

chrome-devtools://devtools/remote/serve\_rev/@191797/devtools.html?remoteFrontendUrl=https%3A%2F%2Fchrome-devtools-frontend.appspot.com%2Fserve\_rev%2F%401337%2Fdevtools.html%23%27onload%3D1&ws=alert(typeof(DevToolsHost)):0//

It shows a dialog box with the text "object" (which indicates that the privileged DevToolsHost object is available to the injected script).

Explanation of XSS:

- The "src" attribute is quoted with single quotes. The remoteFrontendUrl parameter is url-decoded, so any embedded %27 will be decoded to '.
- The XSS auditor would normally block inline event handlers or injected tags, so we can at most add the following prefix:  
  
  'onload=1
- To complete the XSS, we need to append more data. Fortunately for attackers, the vulnerable page reconstruct the query string and appends it to the URL. Since the "ws" parameter is not sanitized, we can append arbitrary code that starts with "?ws="  
  
  ?ws=alert(typeof(DevToolsHost)):0//

(the 1 in onload=1 evaluates to true; the // gets rid of the existing closing '), so effectively we are able to inject an arbitrary script.  

It is difficult to teach the XSS Auditor to block this kind of XSS, but the vulnerabilities that allowed for this XSS can be fixed.

SOLUTIONS  

In this case, a sufficient fix is to disallow single quotes in remoteFrontendUrl, ws and service-backend (all other permitted query parameters already disallow the ' character). This prevents attackers from injecting HTML outside the "src" attribute.

DEFENSE IN DEPTH  

To fix the problem of old frontends in general, I recommend to block older devtools in Chrome.  

The most effective way to do this is to replace the /serve\_rev/ endpoint with a new name. /serve\_rev/ was introduced over 4 years ago (616d494697cd87234a27666cb4cf20dd33f96c34, Chrome 30) and the attack surface is very large.

- If renaming /serve\_rev/ is too complicated (because the infrastructure is also involved), then at least stricten the revision validation. Currently any alphanumeric sequence is permitted by SanitizeRevision [2]. The revisions are git hashes, which are hexadecimal characters of length 40. In the far past, Blink's SVN revision numbers were used instead (until Chrome 45 according to my archived builds). The XSS-vulnerable devtools.html was removed in ce99db1aeccd3228a85fa45806dc72839c84c99b (Chrome 44).  
  
  Tightening the revision number validation would also break my exploit.

[1] <https://chromium.googlesource.com/chromium/src/+/3dda5f542cf410efa531ab17886199b35551290d/chrome/browser/devtools/devtools_ui_bindings.cc#388>  

[2] <https://chromium.googlesource.com/chromium/src/+/3dda5f542cf410efa531ab17886199b35551290d/chrome/browser/devtools/devtools_ui_bindings.cc#324>

## Timeline

### ro...@robwu.nl (2017-12-31)

Patch: https://chromium-review.googlesource.com/c/chromium/src/+/846979

This implements my first suggestion from the bug report.
If you run the test again, XSS will still occur, but the privileged DevTools API won't be exposed (the alert dialog shows "undefined") - I have locally verified the patch.

### ro...@robwu.nl (2017-12-31)

The remoteFrontendUrl parameter was removed together with the XSS vulnerability in ce99db1aeccd3228a85fa45806dc72839c84c99b. If we don't mind dropping support for such old frontends, then another way to fix the bug is to remove the remoteFrontendUrl parameter from the validation logic.

### rs...@chromium.org (2017-12-31)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-01-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/24bbdc5f95f80a7700e232a272a6ea1811c0dcaf

commit 24bbdc5f95f80a7700e232a272a6ea1811c0dcaf
Author: Rob Wu <rob@robwu.nl>
Date: Fri Jan 05 10:17:38 2018

Improve sanitization of remoteFrontendUrl in DevTools

This change ensures that the decoded remoteFrontendUrl parameter cannot
contain any single quote in its value. As of this commit, none of the
permitted query params in SanitizeFrontendQueryParam can contain single
quotes.
Note that the existing SanitizeEndpoint function does not explicitly
check for single quotes. This is fine since single quotes in the query
string are already URL-encoded and the values validated by
SanitizeEndpoint are not url-decoded elsewhere.

BUG=798163
TEST=Manually, see https://crbug.com/798163#c1
TEST=./unit_tests --gtest_filter=DevToolsUIBindingsTest.SanitizeFrontendURL

Change-Id: I5a08e8ce6f1abc2c8d2a0983fef63e1e194cd242
Reviewed-on: https://chromium-review.googlesource.com/846979
Reviewed-by: Dmitry Gozman <dgozman@chromium.org>
Commit-Queue: Rob Wu <rob@robwu.nl>
Cr-Commit-Position: refs/heads/master@{#527250}
[modify] https://crrev.com/24bbdc5f95f80a7700e232a272a6ea1811c0dcaf/chrome/browser/devtools/devtools_ui_bindings.cc
[modify] https://crrev.com/24bbdc5f95f80a7700e232a272a6ea1811c0dcaf/chrome/browser/devtools/devtools_ui_bindings_unittest.cc


### ro...@robwu.nl (2018-01-14)

Verified fixed in 65.0.3322.0 using the STR from the report (after opening chrome-devtools://devtools and then the chrome-devtools:-URL with the XSS payload, I get a 404 page instead of a dialog).

Requesting merge of 24bbdc5f95f80a7700e232a272a6ea1811c0dcaf to block the XSS that in the worst case allows execution of external programs (https://crbug.com/chromium/798222).

### sh...@chromium.org (2018-01-14)

This bug requires manual review: We are only 8 days from stable.
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), kbleicher@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-01-14)

[Empty comment from Monorail migration]

### aw...@google.com (2018-01-16)

[Empty comment from Monorail migration]

### ab...@chromium.org (2018-01-16)

Approving merge for M64. Branch:3282

### cm...@chromium.org (2018-01-17)

Please merge this today before 3:00PM PST

### cm...@chromium.org (2018-01-18)

Ping!

### bu...@chromium.org (2018-01-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/774cd13955b2b84fc8230fbffeb21cfa8e50c6ad

commit 774cd13955b2b84fc8230fbffeb21cfa8e50c6ad
Author: Rob Wu <rob@robwu.nl>
Date: Thu Jan 18 21:40:42 2018

Improve sanitization of remoteFrontendUrl in DevTools

This change ensures that the decoded remoteFrontendUrl parameter cannot
contain any single quote in its value. As of this commit, none of the
permitted query params in SanitizeFrontendQueryParam can contain single
quotes.
Note that the existing SanitizeEndpoint function does not explicitly
check for single quotes. This is fine since single quotes in the query
string are already URL-encoded and the values validated by
SanitizeEndpoint are not url-decoded elsewhere.

BUG=798163
TEST=Manually, see https://crbug.com/798163#c1
TEST=./unit_tests --gtest_filter=DevToolsUIBindingsTest.SanitizeFrontendURL
TBR=rob@robwu.nl

(cherry picked from commit 24bbdc5f95f80a7700e232a272a6ea1811c0dcaf)

Change-Id: I5a08e8ce6f1abc2c8d2a0983fef63e1e194cd242
Reviewed-on: https://chromium-review.googlesource.com/846979
Reviewed-by: Dmitry Gozman <dgozman@chromium.org>
Commit-Queue: Rob Wu <rob@robwu.nl>
Cr-Original-Commit-Position: refs/heads/master@{#527250}
Reviewed-on: https://chromium-review.googlesource.com/874473
Reviewed-by: Rob Wu <rob@robwu.nl>
Cr-Commit-Position: refs/branch-heads/3282@{#542}
Cr-Branched-From: 5fdc0fab22ce7efd32532ee989b223fa12f8171e-refs/heads/master@{#520840}
[modify] https://crrev.com/774cd13955b2b84fc8230fbffeb21cfa8e50c6ad/chrome/browser/devtools/devtools_ui_bindings.cc
[modify] https://crrev.com/774cd13955b2b84fc8230fbffeb21cfa8e50c6ad/chrome/browser/devtools/devtools_ui_bindings_unittest.cc


### aw...@google.com (2018-01-22)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-01-24)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-01-29)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-01-29)

Nice one! The VRP panel decided to award $2,000 for this report, with an extra $500 for supplying the patch.  Cheers!

### aw...@chromium.org (2018-01-29)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-03-27)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-04-22)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### aw...@google.com (2018-10-05)

[Empty comment from Monorail migration]

### is...@google.com (2018-10-05)

This issue was migrated from crbug.com/chromium/798163?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40090022)*
