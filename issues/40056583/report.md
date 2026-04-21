# Cross-site information leak - Leaking cross-origin redirect destination URI due to CORS (iOS)

| Field | Value |
|-------|-------|
| **Issue ID** | [40056583](https://issues.chromium.org/issues/40056583) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Mobile>iOSWeb>Security |
| **Platforms** | iOS |
| **CVE IDs** | CVE-2021-30888 |
| **Reporter** | pr...@gmail.com |
| **Assignee** | mo...@google.com |
| **Created** | 2021-07-19 |
| **Bounty** | $1,000.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4573.0 Safari/537.36

Steps to reproduce the problem:
I've prepared a sample page for easier reproduction of the issue.

To validate the vulnerability, simply visit in iOS;
https://cm2.pw/fetch?url=https://fb.com/4&catch

There, we should see that it tries to redirect to facebook.com and is blocked by CORS as shown in screenshot below;

To demonstrate an impact, we can steal tokens from sites that have SSOs (and do not have mitigations in place or use SameSite cookies). I've previously made a video that should suffice to prove the impact- https://youtu.be/tL95kmDq4N0

What is the expected behavior?
Errors thrown after following a cross-origin redirect using fetch(), are leaking redirect target URLs. Safari is leaking cross-origin redirect information in JavaScript in its implementation of Fetch API when the returned response issues 3xx redirect and does not have an appropriate CORS policy. The specifics about what went wrong with a CORS request are not available to JavaScript code in any other browsers and that's to be expected as they may leak sensitive information like OAuth tokens and whatnot (CORS Error Handling). Since most Single Sign-On (SSO) systems use redirects to pass codes/tokens around, it could prove critical.

Chrome for iOS is also affected as they share the same engine on all iOS devices.

What went wrong?
When sent a CORS request (mode=cors), and the returned response is a 3xx redirect and does not have appropriate CORS policy to allow cross-origin reads (ACAO: *|Origin), an error is thrown with specifics about the reason. The error information is also available to JavaScript and can be read easily with a catch block of fetch API. For example, like;
```
fetch('https://fb.com/4',{mode:'cors',credentials:'include',redirect:'follow'}).catch(error=>alert(error))
```

Did this work before? N/A 

Chrome version: 93.0.4573.0  Channel: dev
OS Version: 

I've already filed the report to Safari;
<rdar://problem/80757697>

### References
https://blog.lbherrera.me/posts/appcache-forgotten-tales/
https://bugs.chromium.org/p/chromium/issues/detail?id=1152226
https://bugs.chromium.org/p/chromium/issues/detail?id=799847
https://bugs.webkit.org/show_bug.cgi?id=208089

## Attachments

- [WebKit-CORS-leak.png](attachments/WebKit-CORS-leak.png) (image/png, 72.1 KB)

## Timeline

### [Deleted User] (2021-07-19)

[Empty comment from Monorail migration]

### jd...@chromium.org (2021-07-19)

Thanks for your report. Please post all relevant files needed to reproduce the issue directly to this bug (one at a time, not compressed). As soon as we have that information, I can further triage. Thanks very much.

### do...@chromium.org (2021-07-21)

From my read of the problem, it looks like the issue is in WebKit specifically? Is there anything Chrome can do if Apple doesn't fix the problem?

### da...@chromium.org (2021-07-23)

[Empty comment from Monorail migration]

[Monorail components: Internals>Sandbox>SiteIsolation]

### da...@chromium.org (2021-07-23)

Right this sounds like a WebKit problem, sorry for sending this to SiteIsolation. We can ask Bling if there's anything we can do.

[Monorail components: -Internals>Sandbox>SiteIsolation Mobile>iOSWeb]

### pr...@gmail.com (2021-07-25)

My apology, I missed all emails :(

re #3 The only code required to reproduce the issue is;
```html
<script>
const url = 'https://fb.com/4'; 
fetch(url, {
  mode:'cors',
  credentials:'include',
  redirect:'follow'
}).catch(error=>alert(error))
</script>
```

re #4, Yes, the issues is in WebKit and I'm not sure if Chrome can do anything.

### [Deleted User] (2021-07-25)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aj...@chromium.org (2021-07-26)

Thanks for reporting this issue! This needs to be fixed in WebKit, so I'm marking this blocked on rdar://problem/80757697.

[Monorail components: -Mobile>iOSWeb Mobile>iOSWeb>Security]

### [Deleted User] (2021-07-27)

[Empty comment from Monorail migration]

### pr...@gmail.com (2021-11-12)

Just letting you know that it's been fixed and shipped already- https://support.apple.com/HT212875

### Excerpt from the link;
Available for: macOS Big Sur and macOS Catalina
Impact: A malicious website using Content Security Policy reports may be able to leak information via redirect behavior
Description: An information leakage issue was addressed.
CVE-2021-30888: Prakash (@1lastBr3ath)

### aj...@chromium.org (2021-11-15)

Thanks! Here are the corresponding release notes for iOS 15.1: https://support.apple.com/en-us/HT212867

### [Deleted User] (2021-11-15)

Dear owner, thanks for fixing this bug. We’ve reopened it because security bugs need Security_Severity and FoundIn labels set, which will enable the bots to request merges to the correct branches ( as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact (security@chromium.org) to arrange to set these labels and then this bug can be marked closed again. Thank you! Severity guidelines: https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues FoundIn guidelines: https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security Thanks for your time! 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aj...@chromium.org (2021-11-15)

This is a bug in WebKit, not in Chromium, so there are no Chromium merges for this. Setting FoundIn doesn't really make sense since it affects all milestones on iOS < 15.1, and will be fixed in all milestones on iOS >= 15.1. To make the bot happy, I'll set this to FoundIn M93, matching the initial report.

### [Deleted User] (2021-11-15)

Dear owner, thanks for fixing this bug. We’ve reopened it because security bugs need Security_Severity and FoundIn labels set, which will enable the bots to request merges to the correct branches ( as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact (security@chromium.org) to arrange to set these labels and then this bug can be marked closed again. Thank you! Severity guidelines: https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues FoundIn guidelines: https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security Thanks for your time! 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-11-15)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-15)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aj...@chromium.org (2021-11-15)

+adetaylor, for help with getting the bot to let us mark this as Fixed (see comments 12 and 14).

### ad...@chromium.org (2021-11-15)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-16)

[Empty comment from Monorail migration]

### am...@google.com (2021-11-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-11-17)

Hello, Prakash - the VRP Panel has decided to award you $1000 for this report. Thank you for reporting this issue in webkit to us! 

### am...@google.com (2021-11-18)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-22)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2022-02-22)

This issue was migrated from crbug.com/chromium/1230444?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-03-19)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40056583)*
