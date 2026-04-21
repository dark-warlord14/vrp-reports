# Security: Reloading iframes with data: src causes partial CSP bypass

| Field | Value |
|-------|-------|
| **Issue ID** | [40054299](https://issues.chromium.org/issues/40054299) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>SecurityFeature>ContentSecurityPolicy |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, iOS, ChromeOS |
| **Reporter** | ar...@gmail.com |
| **Assignee** | an...@chromium.org |
| **Created** | 2020-12-26 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

Certain embedded contexts, including iframes, are required to inherit the CSP of their parent under certain conditions. Section 3.5 - Policy Applicability of the CSP2 specification states that:

Unless the embedded resource is a globally unique identifier (or a srcdoc iframe), the embedded resource is controlled by the policy delivered with the resource. If the embedded resource is a globally unique identifier or srcdoc iframe, it inherits the policy of the context creating it.

Since data: URLs are globally unique identifiers, iframes loaded with a data: URL as their src are required to adhere to the CSP of their parent. Chrome enforces this behavior as expected when initially loading a page with an embedded data: iframe, but if the embedded iframe is reloaded by right-clicking and selecting "Reload frame", the iframe is allowed to run arbitrary scripts that should be blocked by the CSP.

An attacker can use this behavior to partially bypass a restrictive CSP on a website that allows embedding of user-controlled HTML if the attacker can convince a victim user to right click in an iframe and select "Reload frame". I call this a partial CSP bypass because even though this bug does permit the loading of disallowed scripts, iframes with a data: URL as their src are considered to have a null origin and are therefore cross-origin with their parent, limiting the impact of the bypass. A malicious script would have to take advantage of the postMessage api to communicate with its frame's parent or use a similar cross-origin communication method since it would not have access to the parent's DOM.

This behavior does not appear to be present in Firefox; right-clicking in an iframe with a data: src and selecting "This Frame -> Reload Frame" will not allow the frame to bypass the CSP and will instead print an additional CSP violation report to the console. It only appears to be present in chromium-based Chrome and Edge.

**VERSION**  

Chrome Version: [87.0.4280.88] + stable  

Edge Version: 87.0.664.66 (latest version)  

Operating System: Microsoft Windows 10 Home Version: 2004 10.0.19041 Build 19041.685

**REPRODUCTION CASE**  

Here is a basic HTML document that takes advantage of the issue:

<head>
<meta http-equiv="content-security-policy" content="script-src 'none';">
</head>
<body>
<iframe src="data:text/html,<script>alert('Fired script despite CSP restrictions')</script>">
</body>

To reproduce the issue:  

1. Load the above HTML in Chrome (I have attached an HTML document that contains the same HTML code as above).  

2. Notice a CSP violation printed to the console as the iframe attempts to load an inline script disallowed by the CSP specified by the meta tag. This is expected behavior.  

3. Right-click in the iframe and select "Reload frame".  

4. Notice the inline script executes and an alert box appears despite the CSP restrictions.

Let me know if you have any questions

## Attachments

- [partial csp circumvent demo.html](attachments/partial csp circumvent demo.html) (text/plain, 203 B)

## Timeline

### [Deleted User] (2020-12-26)

[Empty comment from Monorail migration]

### aj...@google.com (2020-12-27)

[Empty comment from Monorail migration]

[Monorail components: Blink>SecurityFeature]

### [Deleted User] (2020-12-27)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mk...@chromium.org (2021-01-11)

+Antonio and Paris to confirm and assign, as this seems quite related to policy container.

[Monorail components: -Blink>SecurityFeature Blink>SecurityFeature>ContentSecurityPolicy]

### an...@chromium.org (2021-01-18)

This should be fixed automatically when we include Content Security Policies in the Policy Container.

Assigning to myself. I'll check back when 1149272 is done.

### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### an...@chromium.org (2021-03-08)

[Empty comment from Monorail migration]

### an...@chromium.org (2021-03-08)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-11)

[Empty comment from Monorail migration]

### an...@chromium.org (2021-03-11)

Fixed by  https://chromium.googlesource.com/chromium/src/+/9f54facf59b877331575621edbac505ecf7003c5

### [Deleted User] (2021-03-11)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-12)

[Empty comment from Monorail migration]

### zh...@google.com (2021-03-17)

[Empty comment from Monorail migration]

### am...@google.com (2021-03-31)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@google.com (2021-03-31)

Hi, arw92342@! The VRP Panel has decided to award you $500 for this report. A member of our finance team will be in touch soon to arrange payment. In the meantime, please let me know how you would like to be credited (name or handle you'd like us to use) for this issue in the release notes. 

### ar...@gmail.com (2021-04-01)

Thank you so much @amyressler! You can use the name 'Austin Williams' for the credit.

### am...@google.com (2021-04-02)

[Empty comment from Monorail migration]

### [Deleted User] (2021-06-24)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pg...@google.com (2022-12-13)

[Empty comment from Monorail migration]

### pg...@google.com (2022-12-13)

[Empty comment from Monorail migration]

### pg...@google.com (2023-02-12)

[Empty comment from Monorail migration]

### pg...@google.com (2023-07-28)

[Empty comment from Monorail migration]

### pg...@google.com (2023-07-28)

[Empty comment from Monorail migration]

### is...@google.com (2023-07-28)

This issue was migrated from crbug.com/chromium/1161891?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail blocked-on: crbug.com/chromium/1185145]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40054299)*
