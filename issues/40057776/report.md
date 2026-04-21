# Referrer leakage via object & embed tags despite setting referrer policy to no-referrer

| Field | Value |
|-------|-------|
| **Issue ID** | [40057776](https://issues.chromium.org/issues/40057776) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Blink>SecurityFeature>Referrer |
| **Platforms** | iOS |
| **Reporter** | pr...@gmail.com |
| **Assignee** | aj...@google.com |
| **Created** | 2021-10-31 |
| **Bounty** | $2,000.00 |

## Description

Steps to reproduce the problem:
Tested on: Mozilla/5.0 (iPhone; CPU iPhone OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Mobile/15E148 Safari/604.1

WebKit based browsers leak referrer to resources embedded via object and embed tags when went back. I've created a POC for easier reproduction and understanding of the issue which you can access at;
http://cm2.pw/poc/referrer

Here's what happens;
- The page loads 3 embedded contents- iframe, object & embed
- The page quickly redirects to /?xss=<script>history.go(-1)</script>
- That page at /?xss executes the JavaScript history.go function and redirects back to where it came from

If you notice carefully, when the page first loaded, the embedded resources didn't receive referrer. But when they got redirected back, object & embed'd resources did get the referrer.

What is the expected behavior?
Exclude referer in all subsequent requests

What went wrong?
Referer is being sent

Did this work before? N/A 

Chrome version: 97.0.4682.3  Channel: beta
OS Version: 15.2

Note: It only affects WebKit's implementation of Referrer Policy.

Reference:
https://bugs.webkit.org/show_bug.cgi?id=221171
https://bugs.chromium.org/p/chromium/issues/detail?id=823241

## Attachments

- [referrer.html](attachments/referrer.html) (text/plain, 511 B)

## Timeline

### [Deleted User] (2021-10-31)

[Empty comment from Monorail migration]

### da...@chromium.org (2021-11-02)

Here's what I see in all 3 boxes on M96:

GET / HTTP/1.1
host: raw.cm2.pw
connection: Keep-Alive
accept-encoding: gzip
x-forwarded-for: 34.82.196.204
x-forwarded-proto: http
upgrade-insecure-requests: 1
user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.0 Safari/537.36
accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
accept-language: en-US,en;q=0.9

on M95:

GET / HTTP/1.1
host: raw.cm2.pw
connection: Keep-Alive
accept-encoding: gzip
x-forwarded-for: 34.82.196.204
x-forwarded-proto: http
upgrade-insecure-requests: 1
user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.0 Safari/537.36
accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
accept-language: en-US,en;q=0.9

on M94:

GET / HTTP/1.1
host: raw.cm2.pw
connection: Keep-Alive
accept-encoding: gzip
x-forwarded-for: 34.82.196.204
x-forwarded-proto: http
upgrade-insecure-requests: 1
user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.0 Safari/537.36
accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
accept-language: en-US,en;q=0.9


It's similar on TOT. Am I missing what I should be looking for?

[Monorail components: Internals>Sandbox>SiteIsolation]

### cr...@chromium.org (2021-11-02)

[Empty comment from Monorail migration]

[Monorail components: Blink>SecurityFeature>Referrer]

### da...@chromium.org (2021-11-02)

Oh I see this is iOS only. I don't have a way to repro that and not sure that we can do anything here then. Do we track WebKit bugs?

=> ios team

### ro...@chromium.org (2021-11-02)

=> ajuma

### aj...@chromium.org (2021-11-02)

I cc'd a few more folks on https://bugs.webkit.org/show_bug.cgi?id=221171 to try to get more traction on it.

### na...@chromium.org (2021-11-02)

Removing SiteIsolation component, as it is not present on iOS.

[Monorail components: -Internals>Sandbox>SiteIsolation]

### [Deleted User] (2021-11-04)

[Empty comment from Monorail migration]

### ts...@chromium.org (2021-11-15)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-16)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pr...@gmail.com (2022-02-11)

This also seems fixed but no updates has been provided in the original report.

### aj...@chromium.org (2022-02-14)

I can't reproduce this on iOS 15.3.

### [Deleted User] (2022-02-14)

Dear owner, thanks for fixing this bug. We’ve reopened it because security bugs need Security_Severity and FoundIn labels set, which will enable the bots to request merges to the correct branches ( as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact (security@chromium.org) to arrange to set these labels and then this bug can be marked closed again. Thank you! Severity guidelines: https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues FoundIn guidelines: https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security Thanks for your time! 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aj...@chromium.org (2022-02-14)

Marking FoundIn-97 to match the original report and make the bot happy, but this is an iOS bug rather than a Chrome bug, so any version of Chrome will exhibit this bug on affected iOS versions.

### [Deleted User] (2022-02-14)

Dear owner, thanks for fixing this bug. We’ve reopened it because security bugs need Security_Severity and FoundIn labels set, which will enable the bots to request merges to the correct branches ( as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact (security@chromium.org) to arrange to set these labels and then this bug can be marked closed again. Thank you! Severity guidelines: https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues FoundIn guidelines: https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security Thanks for your time! 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-02-14)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-28)

ajuma: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-03-16)

ajuma: Uh oh! This issue still open and hasn't been updated in the last 30 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### th...@chromium.org (2022-06-13)

[Empty comment from Monorail migration]

### an...@google.com (2022-07-12)

Sheriffbot was erroneously reopening this issue, but has been patched since the last time it reopened. https://crrev.com/i/4211045

### [Deleted User] (2022-07-13)

[Empty comment from Monorail migration]

### am...@google.com (2022-07-21)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-07-21)

Congratulations, Prakash! The VRP Panel has decided to award you $2,000 for this report. Thank you for your efforts and reporting this issue to us and Apple/webkit! 

### am...@google.com (2022-07-22)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-19)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2022-10-19)

This issue was migrated from crbug.com/chromium/1265193?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail blocked-on: crbug.com/chromium/1336016]
[Monorail components added to Component Tags custom field.]

### wf...@chromium.org (2024-07-08)

[issue 351582198](https://issues.chromium.org/issues/351582198) says this still reproduces, so I am re-opening for this to be verified. Please close bug again if you cannot reproduce.

### pe...@google.com (2024-07-08)

Thank you for providing more feedback. Adding the requester to the CC list.

### aj...@google.com (2024-07-08)

Tested on iOS 17.5 and current Stable (126.0.6478.153) and this does not reproduce.

### du...@gmail.com (2024-07-09)

Dear all,

I said in the report this behavior happens in Chrome 126 on Android. So sorry and please have a look at the link http://cm2.pw/poc/referrer on Chrome 126 on Android. The referer information is shown.

### aj...@google.com (2024-07-09)

I don't have access to [bug 351582198](https://issues.chromium.org/issues/351582198), but I'd suggest commenting there asking someone to de-duplicate it from this one.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057776)*
