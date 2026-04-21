# Referrer Policy bypass with javascript URL

| Field | Value |
|-------|-------|
| **Issue ID** | [40090848](https://issues.chromium.org/issues/40090848) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>SecurityFeature>Referrer |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | s....@gmail.com |
| **Assignee** | mo...@google.com |
| **Created** | 2018-03-19 |
| **Bounty** | $1,000.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36

Steps to reproduce the problem:
1. Go to https://test.shhnjk.com/stop_url.html
2. Click on go link

What is the expected behavior?
No referrer sent

What went wrong?
Referrer policy isn't inherited to Javascript URL navigation within same window. Maybe you want to fix it?

Did this work before? N/A 

Chrome version: 65.0.3325.162  Channel: stable
OS Version: OS X 10.13.3
Flash Version: 

PoC
<meta name="referrer" content="no-referrer">
<a href='javascript:"<iframe src=https://test.shhnjk.com/referrer.php>"'>go</a>

## Timeline

### el...@chromium.org (2018-03-19)

[Empty comment from Monorail migration]

[Monorail components: Blink>SecurityFeature>Referrer]

### es...@chromium.org (2018-03-19)

Yep, this sounds like a bug. Per Step 12 of https://html.spec.whatwg.org/#javascript-protocol, we should be setting the referrer policy to the response that we navigate to from the Javascript result.

### ts...@chromium.org (2018-05-03)

elaw - looks like you took care of a similar thing in view-source, would you also like to take a stab at this one?  Otherwise, bounce back to me.

### el...@chromium.org (2018-05-04)

Unfortunately, our handling of JavaScript uris is very different than that of ViewSource, and I don't know how we'd go about carrying over the RP settings from the old document to the new one.


### ts...@chromium.org (2018-05-15)

back to sheriff for triage.

### mk...@chromium.org (2018-05-22)

estark@, eisinger@: Can one of you find someone to poke at this? +dcheng@ might also be familiar enough with the mechanism here to point someone in the right direction.

We should also look at other bits of the document's policy that ought to be applied: CSP, etc.

### jo...@chromium.org (2018-05-22)

oh gawd, the javascript protocol :/

### sh...@chromium.org (2018-09-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-10-17)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-12-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-01-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-03-13)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-04-24)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-06-06)

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

### an...@google.com (2021-07-22)

This has been fixed by the policy container work (https://bugs.chromium.org/p/chromium/issues/detail?id=1130587). There is a WPT for this https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/web_tests/external/wpt/referrer-policy/generic/inheritance/iframe-inheritance-javascript.html.

### [Deleted User] (2021-07-22)

[Empty comment from Monorail migration]

### [Deleted User] (2021-07-22)

[Empty comment from Monorail migration]

### am...@google.com (2021-07-28)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@google.com (2021-07-28)

Hi Jun, the VRP Panel has decided to award you $1,000 for this report. Thank you for reporting this issue as well as for your extreme patience while a comprehensive fix via PolicyContainer was being worked and being left open for some time after, thus not allowing the automation to sweep it into the VRP workflow until very recently. 

### am...@google.com (2021-07-29)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-30)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-05)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-06)

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

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/823241?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40090848)*
