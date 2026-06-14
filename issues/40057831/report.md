# SameSite cookies leak via embedded browsing context

| Field | Value |
|-------|-------|
| **Issue ID** | [40057831](https://issues.chromium.org/issues/40057831) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Network>Cookies |
| **Platforms** | iOS |
| **Reporter** | pr...@gmail.com |
| **Assignee** | bi...@chromium.org |
| **Created** | 2021-11-05 |
| **Bounty** | $500.00 |

## Description

Steps to reproduce the problem:
### Reproduction Steps
1. Visit https://cm2.pw/cookies?url=/?xss=%3Ciframe+src=%22https://egesuite.net/?q=%3Ca+href=//raw.cm2.pw%3EDUMP%22+style=%22height:750px;width:750px%22%3E%3C/iframe%3E

2. Click on DUMP
3. Notice cookies which include also includes Lax & Strict cookies

Here's what's happening;
- cm2.pw/cookies sets different cookies with SameSite attributes- None, Lax & Strict
- Thereafter, issues a redirect to url specified on via ?url using location.href
- cm2.pw/?xss= just echoes the value passed as-is which creates an iframe pointing to egesuite.net (child window)
- egesuit.net/?q= also jsut echoes the value passed as-is which creates an <a> tag pointing to raw.cm2.pw
- Now, when you click DUMP, it just navigates to raw.cm2.pw within the iframe (Note: it's not a top-level navigation)
- raw.cm2.pw simply dumps the request it received

Here, cm2.pw is the parent window, egesuite.net is the child window and raw.cm2.pw is SameSite with cm2.pw

What is the expected behavior?
SameSite cookies shouldn't have been sent

What went wrong?
SameSite cookies were sent

Did this work before? N/A 

Chrome version: 97.0.4688.2  Channel: beta
OS Version: 15.2

The issue is identical to https://crbug.com/1166211 but is specific to WebKit and it not only sends Lax cookies, but it also sends all cookies- None, Lax and Strict, all included.

Link to WebKit Bug: https://bugs.webkit.org/show_bug.cgi?id=232748

## Timeline

### [Deleted User] (2021-11-05)

[Empty comment from Monorail migration]

### va...@chromium.org (2021-11-08)

miketaylr@ -- assigning to you for now though this is an issue in WebKit.
ajuma@ may be able to help get visibility into https://bugs.webkit.org/show_bug.cgi?id=232748

[Monorail components: Internals>Network>Cookies]

### mi...@chromium.org (2021-11-08)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-08)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bi...@chromium.org (2021-11-09)

Looking into this, I can reproduce the issue.

### ad...@google.com (2021-11-11)

bingler@ great. Do you know whether this affects M94, M95, M96, or only M97+? Please could you label this bug with FoundIn-nn, where nn is the earliest of those four branches? That will ensure that the right merges get prompted, as well as ensuring correct credits in release notes, CVE allocation, etc. Thanks!

### bi...@chromium.org (2021-11-11)

adetaylor@
I confirmed the behavior on iOS 15.1, Chrome 95 as of today.

However after speaking with the Chrome iOS team I can confirm that Chrome is not at fault here. Except for a few special cases (which this does not fall under) Chrome does not control which cookies are set/sent and when. That is completely up to WebKit.

I don't have access to the reporter's WebKit bug, but assuming it's the same information, that is the correct escalation route.

I've made no attempt to check other versions of Chrome as they'll all behave the same for a given WebKit version.

### ad...@google.com (2021-11-12)

OK thank you. There's nothing for us to do here, then. I'm going to mark this as ExternalDependency.

### [Deleted User] (2021-11-12)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-12)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-12)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-11-15)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-02)

[Empty comment from Monorail migration]

### pr...@gmail.com (2022-02-11)

This is fixed as well- https://bugs.webkit.org/show_bug.cgi?id=234507 (which is referred in my report- https://bugs.webkit.org/show_bug.cgi?id=232748)

### am...@chromium.org (2022-02-12)

hello, bingler@ -- this issue appears to be fixed in Webkit. Can you confirm and if there's no further actions here, update as Fixed. 

### bi...@chromium.org (2022-02-14)

On iOS 15.3.1 I can confirm this appears to be fixed. Only the cookies with samesite=None, and unspecified samesite values are echoed back.

I believe webkit still treats unspecified samesite as if they were samesite=none, so this is expected.

### [Deleted User] (2022-02-14)

[Empty comment from Monorail migration]

### am...@google.com (2022-02-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-02-18)

Thank you for reporting this issue to us, Prakash. The VRP Panel would like to reward you $500 as thanks for reporting this to us. 

### am...@google.com (2022-02-18)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-23)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1267318?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057831)*
