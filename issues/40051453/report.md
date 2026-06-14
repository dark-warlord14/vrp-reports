# Unexpected reveal of service worker interception by using nextHopProtocol

| Field | Value |
|-------|-------|
| **Issue ID** | [40051453](https://issues.chromium.org/issues/40051453) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>PerformanceAPIs |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | so...@gmail.com |
| **Assignee** | yo...@chromium.org |
| **Created** | 2020-02-06 |
| **Bounty** | $2,000.00 |

## Description

Context: https://bugs.chromium.org/p/chromium/issues/detail?id=1047915#c4

nextHopProtocol also needs to be protected by Timing-Allow-Origin.

## Timeline

### sh...@chromium.org (2020-02-06)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### yo...@chromium.org (2020-02-10)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-02-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/cf3e88c366ec69d74504f065daa0bdee07cf2fac

commit cf3e88c366ec69d74504f065daa0bdee07cf2fac
Author: Yoav Weiss <yoavweiss@chromium.org>
Date: Wed Feb 12 11:27:10 2020

[resource-timing] nextHopProtocol on iframes should be TAO protected

Implements https://github.com/w3c/resource-timing/pull/224

Bug: 1049510
Change-Id: Id8fc4b3a4de72b6a51c820a2352d88bea65c935f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2047023
Auto-Submit: Yoav Weiss <yoavweiss@chromium.org>
Commit-Queue: Yoav Weiss <yoavweiss@chromium.org>
Reviewed-by: Matt Falkenhagen <falken@chromium.org>
Reviewed-by: Ben Kelly <wanderview@chromium.org>
Reviewed-by: Annie Sullivan <sullivan@chromium.org>
Cr-Commit-Position: refs/heads/master@{#740624}

[modify] https://crrev.com/cf3e88c366ec69d74504f065daa0bdee07cf2fac/third_party/blink/renderer/core/timing/performance_resource_timing.cc
[modify] https://crrev.com/cf3e88c366ec69d74504f065daa0bdee07cf2fac/third_party/blink/renderer/core/timing/performance_resource_timing.h
[modify] https://crrev.com/cf3e88c366ec69d74504f065daa0bdee07cf2fac/third_party/blink/renderer/core/timing/performance_resource_timing_test.cc
[add] https://crrev.com/cf3e88c366ec69d74504f065daa0bdee07cf2fac/third_party/blink/web_tests/external/wpt/resource-timing/nextHopProtocol-tao-protected.https.html


### yo...@chromium.org (2020-02-12)

[Empty comment from Monorail migration]

### [Deleted User] (2020-02-15)

[Empty comment from Monorail migration]

### ts...@chromium.org (2020-03-11)

[Empty comment from Monorail migration]

### fa...@chromium.org (2020-04-27)

natashapabrai: This bug was originally reported by sor.karami@gmail.com in https://crbug.com/chromium/1047915. Does it need review for VRP? Adding reward-topanel in case it's eligible (if that's the right label).

### ad...@google.com (2020-05-06)

[Empty comment from Monorail migration]

### na...@google.com (2020-05-07)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-05-07)

Congrats! The Panel decided to award $2,000 for this report. 

### na...@google.com (2020-05-07)

[Empty comment from Monorail migration]

### ad...@google.com (2020-05-15)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-05-18)

[Empty comment from Monorail migration]

### [Deleted User] (2020-05-20)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@chromium.org (2020-05-21)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1049510?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail blocking: crbug.com/chromium/1047915]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40051453)*
