# CSP bypass by navigating same-origin page to JavaScript URI

| Field | Value |
|-------|-------|
| **Issue ID** | [40090789](https://issues.chromium.org/issues/40090789) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Blink>SecurityFeature>ContentSecurityPolicy |
| **Platforms** | iOS |
| **Reporter** | s....@gmail.com |
| **Assignee** | mo...@google.com |
| **Created** | 2018-03-14 |
| **Bounty** | $1,000.00 |

## Description

Steps to reproduce the problem:
1. Go to https://test.shhnjk.com/open_java.html
2. Click go button.
3. On the new tab, click go button again.

What is the expected behavior?
No alert should appear.

What went wrong?
CSP is bypassed by navigating Same-origin but not CSPed page to Javascript URL. See https://crbug.com/chromium/756040 for more details.

Did this work before? N/A 

Chrome version: 65.0.3325.152  Channel: stable
OS Version: iOS 11.2.6
Flash Version:

## Attachments

- deleted (application/octet-stream, 0 B)

## Timeline

### do...@chromium.org (2018-03-14)

[Empty comment from Monorail migration]

[Monorail components: Blink>SecurityFeature>ContentSecurityPolicy]

### mk...@chromium.org (2018-03-14)

Ah. My good friend iOS. I don't think there's much we're going to be able to do about this, as we're reliant on WebKit's CSP implementation.

Have you filed a similar bug against WebKit?

### mk...@chromium.org (2018-03-14)

(That said, I don't get an alert on iOS either. Looking at the code, I'm not sure how the bypass is expected to work. Did you change the PoC in the meantime?)

### an...@chromium.org (2018-03-14)

I believe this is just https://crbug.com/chromium/756040 re-raised for iOS specifically. This is an issue we fixed in August, I imagine that it might not be fixed in webkit.

The issue is you're basically allowed to execute inline scripts by simply opening a window with a javascript: uri.

We have this issue and 3 more raised recently around CSP and iOS. Is there are anything we can do on our side or is it just up to WebKit?

### do...@chromium.org (2018-03-14)

(Security sheriff) Thanks for taking a look here, I suspected that we might not be able to do much about these iOS CSP bugs.

It's a bit unfortunate, but I see two ways forward here:

1. close all of these iOS CSP bugs, and advise the reporter to contact WebKit?
2. we, as a consumer of WKWebView report to WebKit (in which case we could leave these open to flag in the report)

Thoughts?

### s....@gmail.com (2018-03-14)

>Have you filed a similar bug against WebKit?
I filed a worse bug to them where CSP is just bypassed by window.open("javascript:alert(1)"). They fixed it but this bug was still reproducible, so I told them that fix is incomplete and they filed their internal bug which I don't have visibility.

>(That said, I don't get an alert on iOS either. Looking at the code, I'm not sure how the
>bypass is expected to work. Did you change the PoC in the meantime?)
I re-tested and It's working in my iPhone 8. What do you see when you click the 2nd button?

>It's a bit unfortunate, but I see two ways forward here:
Attaching email conversation with palmer@. 

### sh...@chromium.org (2018-03-14)

[Empty comment from Monorail migration]

### mk...@chromium.org (2018-03-14)

Yup. I agree with Chris that bugs in Chrome on iOS are covered in the VRP as it's written today. I worry a bit about our ability to actually do anything about bugs in WebKit's web platform support (including security features like parsing changes, Fetch hardening, CSP, mixed content handling, etc.). I poked at folks internally to see if I'm wrong about the options I see, none of which I'm happy about.

### pa...@chromium.org (2018-03-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-03-15)

[Empty comment from Monorail migration]

### s....@gmail.com (2018-03-15)

I saw that other issues are marked as ExternalDependency. So is it formally confirmed that Chrome for iOS webkit bugs are eligible for bounty?

### es...@chromium.org (2018-03-16)

+awhalley for comment on #11

[Monorail components: -Blink>SecurityFeature>ContentSecurityPolicy]

### s....@gmail.com (2018-03-29)

This bug seems to be fixed by iOS 11.3 update.

### dd...@apple.com (2018-03-29)

> Yup. I agree with Chris that bugs in Chrome on iOS are covered in the VRP as it's written today. I worry a bit about our ability to actually do anything about bugs in WebKit's web platform support (including security features like parsing changes, Fetch hardening, CSP, mixed content handling, etc.). I poked at folks internally to see if I'm wrong about the options I see, none of which I'm happy about.

I realize you're probably talking about working around bugs in older iOS releases, but please report bugs via bugs.webkit.org or product-security@apple.com as soon as they're known. Reporting them here has a much smaller chance that they'll be noticed and fixed.


### s....@gmail.com (2018-04-04)

Hi, could anyone confirm the fix and mark as fixed?

### pa...@chromium.org (2018-04-04)

#14: OK, noted.

#15: I don't know if it is fixed yet.

### sh...@chromium.org (2018-04-18)

[Empty comment from Monorail migration]

### aw...@google.com (2018-04-27)

Looks fixed in or before 11.3.1

### sh...@chromium.org (2018-04-28)

[Empty comment from Monorail migration]

### aw...@google.com (2018-04-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-05-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-05-01)

This bug requires manual review: Less than 24 days to go before AppStore submit on M67
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), kbleicher@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@google.com (2018-05-01)

(nothing to merge here)

### ts...@chromium.org (2018-05-03)

Adding component for the sake of posterity.

[Monorail components: Blink>SecurityFeature>ContentSecurityPolicy]

### aw...@chromium.org (2018-05-04)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-05-04)

Nice one  s.h.h.n.j.k@ - $1,000 for this report.

### s....@gmail.com (2018-05-04)

Wow! This is great! Time to secure “Chrome for iOS” :)

### aw...@chromium.org (2018-05-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-08-04)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2018-08-04)

This issue was migrated from crbug.com/chromium/821640?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40090789)*
