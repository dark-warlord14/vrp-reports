# Cross-site information leak - CSP Violation reports contain blockedURI's hostname

| Field | Value |
|-------|-------|
| **Issue ID** | [40057810](https://issues.chromium.org/issues/40057810) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Mobile>iOSWeb>Security |
| **Platforms** | iOS |
| **Reporter** | pr...@gmail.com |
| **Assignee** | aj...@google.com |
| **Created** | 2021-11-03 |
| **Bounty** | $2,000.00 |

## Description

Steps to reproduce the problem:
For reproduction;
1. Open http://cm2.pw/jub0bs_xorigin?url=https://fb.com/4&domain=fb.com
2. Click on Exploit (in case you have pop-up blocker enabled)

You should see the report printed on screen with blockedURI set to origin of the redirected URL i.e. https://www.facebook.com.

What is the expected behavior?
blockedURI should be set to origin of the original request as per spec

What went wrong?
blockedURI contains origin of the redirected location

Did this work before? N/A 

Chrome version: 97.0.4688.2  Channel: beta
OS Version: 15.2

Note: The vulnerability is specific to WebKit and doesn't reproduce on Chrome itself.

Link to WebKit Bug: https://bugs.webkit.org/show_bug.cgi?id=232660

## Attachments

- [form-action.html](attachments/form-action.html) (text/plain, 1.0 KB)

## Timeline

### [Deleted User] (2021-11-03)

[Empty comment from Monorail migration]

### va...@chromium.org (2021-11-04)

ajuma@ -- can you please help triage this? Thanks.
The issue is reportedly not reproducible in Chrome but can you check if this is reproducible on Safari?


[Monorail components: Mobile>iOSWeb>Security]

### va...@chromium.org (2021-11-04)

Setting impact to None for now but please feel free to change it if we can repro this in Chrome.

### aj...@chromium.org (2021-11-04)

This does reproduce in Chrome on iOS (since the underlying cause is a WebKit bug that affects all browsers on iOS) but does not reproduce in Chrome on macOS.

Marking as an external dependency on https://bugs.webkit.org/show_bug.cgi?id=232660.



### [Deleted User] (2021-11-04)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-04)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pr...@gmail.com (2021-11-05)

Just letting you know that this has been fixed already- https://commits.webkit.org/r285320

### aj...@chromium.org (2021-11-05)

Thanks for the update. Adding a NextAction date to check if the WebKit fix has shipped.

### aj...@chromium.org (2021-12-01)

Still hasn't shipped.

### aj...@chromium.org (2022-02-07)

Fixed in iOS 15.3.

### [Deleted User] (2022-02-08)

[Empty comment from Monorail migration]

### am...@google.com (2022-02-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-02-11)

Congratulations - the VRP Panel has decided to award you $2,000 for this report. Thanks for your efforts and reporting this issue to us! 

### am...@google.com (2022-02-15)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-16)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2022-05-16)

This issue was migrated from crbug.com/chromium/1266631?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-03-19)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

### os...@gmail.com (2025-05-06)

deleted

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057810)*
