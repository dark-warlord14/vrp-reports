# CSP is bypassed for status code 100, 101, and 102 pages.

| Field | Value |
|-------|-------|
| **Issue ID** | [40058593](https://issues.chromium.org/issues/40058593) |
| **Status** | Accepted |
| **Severity** | Unknown |
| **Priority** | P3 |
| **Component** | Blink>SecurityFeature>ContentSecurityPolicy |
| **Platforms** | Windows |
| **Reporter** | tj...@gmail.com |
| **Assignee** | an...@chromium.org |
| **Created** | 2022-01-26 |
| **Bounty** | $1,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Whale/3.12.129.46 Safari/537.36

Steps to reproduce the problem:
1. Access to the test.html page:
```test.html
<?php
    header("HTTP/: 100");
    header("Content-Security-Policy: default-src 'self'");
?>
<script>alert(1)</script>
```
2. We can see that the inline script is executed.

What is the expected behavior?
Inline script is executed in CSP environment where inline script should not be executed.

What went wrong?
This bug occurs when the status code is 100, 101, or 102. I don't know if this is intentional behavior, but it seems that there is no rule in the CSP spec to treat the CSP differently for the 100, 101, or 102 status codes.

If a web developer without a background writes a page that returns 100, 101, or 102 response codes, and there is an XSS vulnerability in the page, CSP bypass may occur.

Did this work before? N/A 

Chrome version: 96.0.4664.110  Channel: stable
OS Version: 10.0

## Timeline

### [Deleted User] (2022-01-26)

[Empty comment from Monorail migration]

### ca...@chromium.org (2022-01-27)

antoniosartori: Can you help further triage this? I don't see anything in the spec mentioning that CSP shouldn't apply for certain status codes, so this seems valid. I did not try to reproduce this since I didn't have a server setup, but the report seems plausible.

[Monorail components: Blink>SecurityFeature]

### [Deleted User] (2022-01-27)

[Empty comment from Monorail migration]

### an...@chromium.org (2022-01-27)

[Empty comment from Monorail migration]

[Monorail components: -Blink>SecurityFeature Blink>SecurityFeature>ContentSecurityPolicy]

### an...@chromium.org (2022-01-27)

I can reproduce. I believe this is not really a CSP problem, but rather a network bug. I opened https://crbug.com/1291482

### an...@chromium.org (2022-01-27)

[Empty comment from Monorail migration]

### tj...@gmail.com (2022-01-28)

Thanks for the response. 
If possible, can I see the content of the https://crbug.com/chromium/1291482? I want to follow the status of the report.

### am...@chromium.org (2022-01-28)

Issue was reported in M96 (and probably goes back further than that), setting foundin to appropriately reflect that 

### [Deleted User] (2022-01-28)

[Empty comment from Monorail migration]

### tj...@gmail.com (2022-05-15)

Hello team, this bug seems to be fixed now. I have confirmed that this bug is not reproduced!

### an...@chromium.org (2022-05-16)

Closing, since it looks like this was fixed through https://crbug.com/chromium/1291482.

Thanks tjddlf3604@gmail.com for checking.

### an...@chromium.org (2022-05-16)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-16)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-16)

[Empty comment from Monorail migration]

### am...@google.com (2022-06-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-06-13)

Congratulations! The VRP Panel has decided to award you $1,000 for this report. A member of our finance team will reach out to you soon to arrange payment. Thank you for your efforts and reporting this issue to us. 

### am...@google.com (2022-06-16)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-22)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-12-14)

[Empty comment from Monorail migration]

### is...@google.com (2022-12-14)

This issue was migrated from crbug.com/chromium/1291060?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail blocked-on: crbug.com/chromium/1291482]
[Monorail mergedinto: crbug.com/chromium/1291482]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058593)*
