# Security: Chrome incorrectly interprets newlines in HTTP headers in HTTP/3, allowing for some header splitting possibilities

| Field | Value |
|-------|-------|
| **Issue ID** | [40056840](https://issues.chromium.org/issues/40056840) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Internals>Network>QUIC |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | on...@gmail.com |
| **Assignee** | bn...@chromium.org |
| **Created** | 2021-08-10 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

While investigating a bug bounty report related to header splitting in our infrastructure we identified some unexpected behavior in Chrome. With HTTP/1.1, newlines injected into headers lead to header splitting because clients have no way to know that the newlines were not legitimately part of the request. In HTTP/3, the QPACK representation of headers should allow for clients to identify when newlines are included in incorrect locations and reject them.

In practice, Chrome appears to be parsing the headers in a way that leads to a limited form of header splitting. Specifically, a header with a newline in the value is being treated as two distinct headers with the same name. That would allow for header splitting via (for instance) a Set-Cookie header.

**VERSION**  

Chrome Version: 92.0.4515.131 + stable  

Operating System: OS X 11.5.1

**REPRODUCTION CASE**

1. Enable Quic support in the browser
2. Browse to <https://fb.mvfst.net/>
3. Browse to <https://fb.mvfst.net/15> with the Network tab open
4. Note that the Network tab indicates "injectheader" was sent twice with two distinct values.
5. Note that when trying to load the same page over HTTP/2 (HTTP/3 disabled) the response is rejected due to the newline

**CREDIT INFORMATION**  

Reporter credit: TBD (we'd like to give credit to the researcher who led us to discover the issue, but we need to get permission from them to publicly attribute the finding)

## Timeline

### [Deleted User] (2021-08-10)

[Empty comment from Monorail migration]

### wf...@chromium.org (2021-08-10)

Thanks for your report. I am passing to the net team for further investigation.

[Monorail components: Internals>Network>QUIC]

### [Deleted User] (2021-08-10)

[Empty comment from Monorail migration]

### rc...@chromium.org (2021-08-10)

[Empty comment from Monorail migration]

### rc...@chromium.org (2021-08-10)

[Empty comment from Monorail migration]

### rc...@chromium.org (2021-08-10)

[Empty comment from Monorail migration]

### fa...@chromium.org (2021-08-11)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-11)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ne...@meta.com (2021-08-12)

FYI, we found that Firefox has a similar issue but with greater exploitability (they will treat the header as two distinct headers, similar to how header splitting would work in HTTP/1.1). That issue was reported in https://bugzilla.mozilla.org/show_bug.cgi?id=1724896 alongside this report. The Mozilla team is preparing a fix now. I wanted to mention that here because there's a possibility that the fix will lead people to investigate and independently discover this behavior in Chrome.

### ne...@meta.com (2021-08-14)

Re: Credit Information, I got confirmation from the researcher. Credit can be attributed to Youssef Sammouda.

### [Deleted User] (2021-08-16)

[Empty comment from Monorail migration]

### ne...@meta.com (2021-08-18)

Mozilla released their fix today: https://www.mozilla.org/en-US/security/advisories/mfsa2021-37/

### bn...@chromium.org (2021-09-10)

[Empty comment from Monorail migration]

### bn...@chromium.org (2021-09-10)

[Empty comment from Monorail migration]

### bn...@chromium.org (2021-10-04)

This has been silently fixed in Chromium.

### [Deleted User] (2021-10-04)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-05)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-10)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2022-03-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-03-11)

Hi Youssef, sincere apologies in the delay in getting this issue to VRP Panel decision. While this issue was silently resolved in Chrome and fell outside of normal security processes, we did want to ensure you were at least rewarded for your discovery and efforts, so we would like to extend to you a $1,000 reward as a thank you. We genuinely appreciate you working with facebook to allow them to provide this discovery to us. Thank you, Neal for passing it along! 

### am...@google.com (2022-03-11)

[Empty comment from Monorail migration]

### st...@google.com (2022-11-22)

[Empty comment from Monorail migration]

### ad...@google.com (2022-12-14)

I'm trying to work out how and when we fixed this, for the sake of record keeping. I can't find any other bugs with plausible-sounding titles. git logs and crbug searches are not yielding an obvious candidate. We could potentially try to bisect, but as the original POC server is no longer up, and given the nuances of setting up a QUIC server I'm not going to try that. Instead I'll assume https://crbug.com/chromium/1238309#c15 was the date this landed in Chromium head, and pick a fix version from when that would have got to stable.

### ad...@google.com (2022-12-14)

[Empty comment from Monorail migration]

### pg...@google.com (2023-02-12)

[Empty comment from Monorail migration]

### pg...@google.com (2023-07-28)

[Empty comment from Monorail migration]

### pg...@google.com (2023-07-28)

[Empty comment from Monorail migration]

### is...@google.com (2023-07-28)

This issue was migrated from crbug.com/chromium/1238309?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40056840)*
