# [iOS] CSP Bypass via Service Worker

| Field | Value |
|-------|-------|
| **Issue ID** | [40057910](https://issues.chromium.org/issues/40057910) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Mobile>iOSWeb>Security |
| **Platforms** | iOS |
| **Reporter** | pr...@gmail.com |
| **Assignee** | aj...@google.com |
| **Created** | 2021-11-14 |
| **Bounty** | $500.00 |

## Description

Steps to reproduce the problem:
1. Open https://cm2.pw/research/sw/csp-bypass?url=https://httpbin.org/get
2. Notice the Content-Security-Policy
3. Click on Exec

You should see the response from httpbin.org printed on the screen even though the policy does not have httpbin.org in any of the CSP directives.

What is the expected behavior?
According to spec, the response to requests not whitelisted in the CSP policy should be blocked.

What went wrong?
 In WebKit, however, CSP violation does not occur at all which not only allows sending requests but also allows reading responses if enabled CORS.

Did this work before? N/A 

Chrome version: 97.0.4692.8  Channel: beta
OS Version: 15.2

Note: The vulnerability is specific to WebKit and does not reproduce on Chrome unless on iOS.

Link to WebKit Bug: https://bugs.webkit.org/show_bug.cgi?id=233098

## Attachments

- [csp-sw.html](attachments/csp-sw.html) (text/plain, 871 B)

## Timeline

### [Deleted User] (2021-11-14)

[Empty comment from Monorail migration]

### ts...@chromium.org (2021-11-15)

[Empty comment from Monorail migration]

### ts...@chromium.org (2021-11-15)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-16)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-16)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pr...@gmail.com (2021-12-13)

This has been fixed- https://bugs.webkit.org/show_bug.cgi?id=234140

### am...@chromium.org (2022-02-11)

[Empty comment from Monorail migration]

[Monorail components: Mobile>iOSWeb>Security]

### am...@chromium.org (2022-02-11)

Setting assignments and CC consistent with past similar issues (ex: https://crbug.com/chromium/1266631)
ajuma@ can you please update this as fixed?
This does not reproduce in Chrome on iOS, but I'm on stable version (98.0.4758.85) and this appears to be fixed in webkit for some time (since 13 December). 


### aj...@chromium.org (2022-02-11)

This is fixed in iOS 15.3. 

### [Deleted User] (2022-02-12)

[Empty comment from Monorail migration]

### am...@google.com (2022-02-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-02-18)

Thank you for reporting this issue to us, Prakash. The VRP Panel would like to reward you $500 as thanks for reporting this to us. 

### am...@google.com (2022-02-18)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-21)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2022-05-21)

This issue was migrated from crbug.com/chromium/1270117?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-03-19)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057910)*
