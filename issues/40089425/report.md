# Security: content security policy bypass by writing to loading Frame's ContentDocument

| Field | Value |
|-------|-------|
| **Issue ID** | [40089425](https://issues.chromium.org/issues/40089425) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>SecurityFeature>ContentSecurityPolicy |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ma...@gmail.com |
| **Assignee** | an...@chromium.org |
| **Created** | 2017-10-27 |
| **Bounty** | $1,000.00 |

## Description

AFFECTED PRODUCTS
--------------------
chrome 62.0.3202.62 stable


DESCRIPTION
--------------------
online demo:
http://xsser.math1as.com/csp2.html

this problem occurs because of when load a http URL , the csp would lost,but as a matter of fact, the document.domain is "about:blank" until finally load it.
i guess this issue is in order to prevent chrome from spoof attack, but caused new problem.


## Attachments

- [ff.jpg](attachments/ff.jpg) (image/jpeg, 47.3 KB)

## Timeline

### ma...@gmail.com (2017-10-27)

again, ff and safari would block it
even chrome 59 would block the request.

### ma...@gmail.com (2017-10-27)

so here is the patch:
when load a new URL ,for example, google.com
1.deal it as about:blank first, and inhreit the topframe's CSP
2.when finally load google.com , use the new CSP

### el...@chromium.org (2017-10-27)

Repros in Chrome 64

[Monorail components: Blink>SecurityFeature>ContentSecurityPolicy]

### pa...@chromium.org (2017-10-31)

I'm not sure what to rate the severity at. Any thoughts, mkwst or andypaicu? Medium?

### ma...@gmail.com (2017-10-31)

Re #4
similar with https://crbug.com/chromium/669086 and https://crbug.com/chromium/747847
bypass the following CSP
default-src 'self';script-src 'unsafe-inline';

### pa...@chromium.org (2017-10-31)

I'm going with Medium, since it breaks a security boundary and enables XSS (but not UXSS directly) if the site has an XSS vulnerability but for CSP. One could possibly argue Low, if you consider the latter condition a mitigating factor, but I think XSS is common enough that I wouldn't consider it much of a mitigation.

### el...@chromium.org (2017-10-31)

Re #6: Maybe I'm missing something, but in order for this to work, doesn't the attacker already have to have the ability to execute script (to drive the subframe)? 

Turning script execution into script execution doesn't seem terribly exciting.

### sh...@chromium.org (2017-11-10)

andypaicu: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### es...@chromium.org (2017-11-10)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-11-25)

andypaicu: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-01-25)

[Empty comment from Monorail migration]

### es...@chromium.org (2018-02-18)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-03-07)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-04-19)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-05-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-09-05)

[Empty comment from Monorail migration]

### an...@chromium.org (2018-09-20)

I suspect this bug has been fixed in the meantime together with one of the related ones (we did fix a bunch of inheritance issues in CSP) but the original link is not available and there is no exact description of how the bypass worked

Is there any chance to get the original link back up, or does anyone that commented here know enough details to help test this?

### ma...@gmail.com (2018-09-20)

Hi , I could confirm this was fixed in august , but I lost the original POC. 

### an...@chromium.org (2018-09-20)

Thank you, I will marked it as fixed then.

### sh...@chromium.org (2018-09-20)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-09-24)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-09-27)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-09-28)

Thanks for the report ma7h1as.l@ the VRP panel decided to award $1,000. Cheers!

### aw...@google.com (2018-09-28)

[Empty comment from Monorail migration]

### aw...@google.com (2018-09-28)

[Empty comment from Monorail migration]

### ma...@gmail.com (2018-09-28)

[Comment Deleted]

### ma...@gmail.com (2018-09-28)

re #24 thank you,  could you please change the credit information to "Wenxu Wu (@ma7h1as) of Tencent Security Xuanwu Lab" for all of my bugs in the future？

### aw...@google.com (2018-09-28)

I've updated our records, thanks!

### aw...@chromium.org (2018-09-28)

[Empty comment from Monorail migration]

### ma...@gmail.com (2018-10-15)

could you please assign a CVE-ID for it when releases M70 chrome,  thank you.

### sh...@chromium.org (2018-12-27)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-04)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-05)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-05)

This issue was migrated from crbug.com/chromium/779028?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40089425)*
