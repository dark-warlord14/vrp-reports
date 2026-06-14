# Security: forced redirection from cross-origin iframe

| Field | Value |
|-------|-------|
| **Issue ID** | [40095928](https://issues.chromium.org/issues/40095928) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Mobile>iOSWeb>Security |
| **Platforms** | iOS |
| **Reporter** | el...@confiant.com |
| **Assignee** | aj...@google.com |
| **Created** | 2019-08-07 |
| **Bounty** | $3,000.00 |

## Description

Hi Team,

This bug report is a follow up in reference to: 

https://bugs.chromium.org/p/chromium/issues/detail?id=951782

The same malvertiser is back with another clever loophole that enables them to spawn a forced redirection from a cross-origin iframe that has standard ad serving attributes including "allow-top-navigation-by-user-activation".

This time they have a very similar payload that leverages 'onkeydown' instead of 'onblur'.

The browsers affected by this bug are:

Chrome on iOS (including current versions)
Safari on iOS
Safari on macOS 

These campaigns primarily target desktop devices - presumably because a 'keydown' event is much more likely on a desktop with a keyboard rather than a mobile device. However, if the page that the malicious ad is being served on has any sort of form or textarea, then the user will be redirected as soon as they start typing in that form.

While we recognize that the bug is much greater on desktop Safari, we hope that you can address this bug soon, because the attacker behind these malvertising campaigns runs them at massive scale - sometimes to the tune of hundreds of millions of impressions in just a matter of hours or days. Anything that throws a wrench in their ROI makes a difference.

We will be submitting a report to the Safari team shortly as well.

The poc attached has been reverse engineered from the malvertiser's payload. It was tested both on browserstack and on physical iOS devices.

In order to test the full impact, please load the poc.payload.html in the sandboxed iframe under a different origin. Sandbox.html includes a textarea outside of the iframe that you can use to launch the mobile keyboard.

Best,
Eliya Stein

## Attachments

- [poc.payload.html](attachments/poc.payload.html) (text/plain, 946 B)
- [sandbox.html](attachments/sandbox.html) (text/plain, 795 B)

## Timeline

### ke...@chromium.org (2019-08-07)

eugenebut@: Can you take this or triage further?

Marking this as P1 because it is being exploited in the wild.

[Monorail components: UI>Browser>PopupBlocker]

### eu...@chromium.org (2019-08-07)

[Empty comment from Monorail migration]

[Monorail components: -UI>Browser>PopupBlocker Mobile>iOSWeb>Security]

### aj...@chromium.org (2019-08-07)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-08-08)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### he...@google.com (2019-08-09)

eugenebut@: gambard is OoO til Aug. 21 and this is a P1 security bug. Maybe someone else can take a look?

### aj...@chromium.org (2019-08-09)

[Empty comment from Monorail migration]

### aj...@chromium.org (2019-08-12)

Fixed in https://trac.webkit.org/changeset/248491/webkit

### aj...@chromium.org (2019-09-11)

The fix from #7 is in iOS 13.0.

### sh...@chromium.org (2019-09-12)

[Empty comment from Monorail migration]

### na...@google.com (2019-09-16)

[Empty comment from Monorail migration]

### na...@google.com (2019-10-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### pa...@chromium.org (2019-10-09)

Congrats! The Panel decided to reward $3,000 for this report :) 

### na...@google.com (2019-10-09)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-12-18)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2019-12-18)

This issue was migrated from crbug.com/chromium/991568?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-03-19)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095928)*
