# Security: Web sites can open privileged pages via remote debugging server (CSRF)

| Field | Value |
|-------|-------|
| **Issue ID** | [40090539](https://issues.chromium.org/issues/40090539) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Platform>DevTools |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ro...@robwu.nl |
| **Assignee** | ds...@chromium.org |
| **Created** | 2018-02-19 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

When Chrome is started with the --remote-debugging-port=PORT flag, an undocumented HTTP API becomes available at <http://127.0.0.1:PORT/>.  

One of the APIs is /json/new?(url\_here), which is susceptible to cross-site request forgery. Attackers can use this from a web page to open arbitrary URLs in a new tab, including URLs that are normally unreachable from renderers such as those at the chrome: or chrome-devtools: scheme.

The port can easily be found, e.g. by enumerating all ports, do a portscan, or use information leaks such as <https://crbug.com/chromium/813541>.

**VERSION**  

Chrome Version: 64.0.3282.167 (stable) + 66.0.3351.0 (canary)

**REPRODUCTION CASE**

1. Start Chrome with --remote-debugging-port=9222
2. Open data:text/html,<img src="http://127.0.0.1:9222/json/new?chrome://quit"> and observe that the browser from the first step quits.

Currently this HTTP endpoint accepts any HTTP verb. It can be changed to something like "PUT" or "PATCH" so that normal web pages cannot reach this API endpoint any more (because web pages can only use GET and POST).  

Clients of the remote debugging protocol can then switch from GET to this new HTTP verb, and still be compatible with old Chrome and new patched Chrome.

## Timeline

### ro...@robwu.nl (2018-02-19)

[Empty comment from Monorail migration]

[Monorail components: -Platform>Apps>DevTools Platform>DevTools]

### ro...@robwu.nl (2018-02-19)

s/CRSF/CSRF/ (cross-site request forgery)

### oc...@chromium.org (2018-02-19)

pfeldman, could you please take a look at this, or help with assigning it to the right person? Thanks.

### sh...@chromium.org (2018-02-20)

[Empty comment from Monorail migration]

### pf...@chromium.org (2018-03-05)

[Empty comment from Monorail migration]

### dg...@chromium.org (2018-03-05)

[Empty comment from Monorail migration]

### mm...@chromium.org (2019-04-30)

[Empty comment from Monorail migration]

### dg...@chromium.org (2019-05-08)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-09-11)

[Empty comment from Monorail migration]

### ha...@chromium.org (2019-09-26)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-09-26)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-10-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-12-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2020-02-05)

[Empty comment from Monorail migration]

### [Deleted User] (2020-04-09)

[Empty comment from Monorail migration]

### [Deleted User] (2020-05-20)

[Empty comment from Monorail migration]

### [Deleted User] (2020-07-16)

[Empty comment from Monorail migration]

### [Deleted User] (2020-08-26)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-07)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-30)

[Empty comment from Monorail migration]

### [Deleted User] (2020-11-18)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-20)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-03)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-11)

[Empty comment from Monorail migration]

### zh...@google.com (2021-03-17)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-15)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-26)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-07)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-11)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-22)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-15)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-02)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-30)

[Empty comment from Monorail migration]

### ds...@chromium.org (2022-04-21)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-04-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/a31c9dbd54d1d6b05c31392e86087e3912ba15eb

commit a31c9dbd54d1d6b05c31392e86087e3912ba15eb
Author: Danil Somsikov <dsv@chromium.org>
Date: Mon Apr 25 11:14:21 2022

Add UMA metrics and console errors when mutating actions of the devtools
HTTP server are invoked with an unsafe HTTP verb.

Bug: 813542
Change-Id: Ic4c5157ea0e7e6d8af53dd29596055c8821620a0
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3595822
Reviewed-by: Andrey Kosyakov <caseq@chromium.org>
Reviewed-by: Changhao Han <changhaohan@chromium.org>
Auto-Submit: Danil Somsikov <dsv@chromium.org>
Commit-Queue: Danil Somsikov <dsv@chromium.org>
Cr-Commit-Position: refs/heads/main@{#995652}

[modify] https://crrev.com/a31c9dbd54d1d6b05c31392e86087e3912ba15eb/content/browser/devtools/devtools_http_handler.cc
[modify] https://crrev.com/a31c9dbd54d1d6b05c31392e86087e3912ba15eb/content/browser/devtools/devtools_http_handler_unittest.cc
[modify] https://crrev.com/a31c9dbd54d1d6b05c31392e86087e3912ba15eb/tools/metrics/histograms/enums.xml
[modify] https://crrev.com/a31c9dbd54d1d6b05c31392e86087e3912ba15eb/tools/metrics/histograms/metadata/dev/histograms.xml


### bm...@chromium.org (2022-05-11)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-25)

[Empty comment from Monorail migration]

### ds...@chromium.org (2022-07-19)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-03)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-28)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-30)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-12-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/devtools/devtools-frontend/+/1343de2553587df456404825abb7e79a5a62b6c4

commit 1343de2553587df456404825abb7e79a5a62b6c4
Author: Danil Somsikov <dsv@chromium.org>
Date: Fri Dec 02 17:19:16 2022

Use PUT HTTP verb in describeWithRealConnection so that we can remove support for GET and POST.

Bug: 813542
Change-Id: I15753c1955d984bb9450d2d139a8beae4c04d8c3
Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/4076329
Reviewed-by: Alex Rudenko <alexrudenko@chromium.org>
Auto-Submit: Danil Somsikov <dsv@chromium.org>
Commit-Queue: Alex Rudenko <alexrudenko@chromium.org>

[modify] https://crrev.com/1343de2553587df456404825abb7e79a5a62b6c4/test/unittests/front_end/helpers/RealConnection.ts


### bm...@chromium.org (2022-12-09)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-12-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/1b944abea3ffeef729174b6a802d2d805a38ce2c

commit 1b944abea3ffeef729174b6a802d2d805a38ce2c
Author: Danil Somsikov <dsv@chromium.org>
Date: Fri Dec 16 13:38:27 2022

Disallow GET, POST and OPTIONS for /json/new

Bug: 813542
Change-Id: I26394df661adb39f07045854366223236a1eeecb
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4110715
Auto-Submit: Danil Somsikov <dsv@chromium.org>
Reviewed-by: Alex Rudenko <alexrudenko@chromium.org>
Commit-Queue: Danil Somsikov <dsv@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1084279}

[add] https://crrev.com/1b944abea3ffeef729174b6a802d2d805a38ce2c/content/public/test/mock_devtools_agent_host.cc
[add] https://crrev.com/1b944abea3ffeef729174b6a802d2d805a38ce2c/content/public/test/mock_devtools_agent_host.h
[modify] https://crrev.com/1b944abea3ffeef729174b6a802d2d805a38ce2c/components/devtools/simple_devtools_protocol_client/simple_devtools_protocol_client_unittest.cc
[modify] https://crrev.com/1b944abea3ffeef729174b6a802d2d805a38ce2c/content/browser/devtools/devtools_http_handler.cc
[modify] https://crrev.com/1b944abea3ffeef729174b6a802d2d805a38ce2c/content/browser/devtools/devtools_http_handler_unittest.cc
[modify] https://crrev.com/1b944abea3ffeef729174b6a802d2d805a38ce2c/content/test/BUILD.gn


### ds...@chromium.org (2022-12-16)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-17)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-17)

[Empty comment from Monorail migration]

### am...@google.com (2023-01-12)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-01-12)

Congratulations, Rob! The VRP Panel has decided to award you $3,000 for this report. Thank you for your efforts (back in 2018) in discovering and reporting this issue! 

### am...@google.com (2023-01-14)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-24)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-04-10)

Because the span of time from the UMA metrics CLs to the fix CLs, our automation didn't recognize this issue as newly fixed. The fixes for this issue shipped in M111 milestone. Updating with release label and label to trigger this to be included in the orphaned bugs process when it is next run. 

### pg...@google.com (2023-04-26)

[Empty comment from Monorail migration]

### pg...@google.com (2023-07-28)

[Empty comment from Monorail migration]

### pg...@google.com (2023-07-28)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/813542?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40090539)*
