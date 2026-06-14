# Security: On Chrome OS, any webpage is able to interface with the Chrome Goodies extension

| Field | Value |
|-------|-------|
| **Issue ID** | [40064406](https://issues.chromium.org/issues/40064406) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Unknown |
| **Platforms** | ChromeOS |
| **Reporter** | ad...@gmail.com |
| **Assignee** | ch...@google.com |
| **Created** | 2023-05-07 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

By putting `chrome-extension://kddnkjkcjddckihglkfcickdhbmaodcn/broker.html` inside an iframe, any webpage is able to access `chrome.echoPrivate.getUserConsent` or `chrome.echoPrivate.getOfferInfo` by posting messages to that iframe. Neither one of these requires any user action to trigger.

The user consent prompt is able to block any additional input to the browser window. Thus, a malicious page could display another prompt the moment the user closes one, which would prevent the user from leaving the page. The prompt also looks slightly more legitimate than simply using alert(). The page is also able to change the title of the prompt to something arbitrary, which could be used to trick the user into redeeming offers.

Getting the available offers also reveals the promo codes for anything the user has previously redeemed, the serviceID of the last prompt the user has received, and the user's device family.

**VERSION**  

Chrome Version: 112.0.5615.134 stable  

Operating System: Chrome OS 112.0.5615.134 stable

**REPRODUCTION CASE**  

A POC is available at <https://ading.fr.to/echoanywhere/>. The files for it have been attached to this report.

**CREDIT INFORMATION**  

Reporter credit: Allen Ding (ading2210 on Github)

## Attachments

- [index.html](attachments/index.html) (text/plain, 2.8 KB)
- [echo.js](attachments/echo.js) (text/plain, 2.3 KB)

## Timeline

### [Deleted User] (2023-05-07)

[Empty comment from Monorail migration]

### ad...@gmail.com (2023-05-07)

Note that the URL for the POC is actually at https://ading.dev/echoanywhere/

### ad...@gmail.com (2023-05-08)

It also seems to be possible to redeem offers that the device isn't supposed to be eligible for. For instance, I was able to redeem the "minecraft.2023" offer, which isn't listed on the Chrome perks page. 

### nh...@google.com (2023-05-08)

[Empty comment from Monorail migration]

### ch...@google.com (2023-05-08)

Your report will be worked on in the Buganizer system (link: https://issuetracker.google.com/issues/281468020). You have been cc'ed on that report and should have access to it at this time to follow along while it is being worked on.

[Monorail blocking: b/281468020]

### [Deleted User] (2023-05-08)

[Empty comment from Monorail migration]

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-26)

[Empty comment from Monorail migration]

### ch...@google.com (2023-08-11)

Fix approved and merged (see: https://issuetracker.google.com/issues/281468020)

CLs: Merged:​<none>      crrev/i/6242691

### ch...@google.com (2023-08-11)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-11)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-11)

[Empty comment from Monorail migration]

### st...@google.com (2023-08-15)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-15)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@google.com (2023-09-19)

Exploitability - Explain why/why not the bug is reachable and/or exploitable For example, if a bug mentions a race, details are needed about how easy that race would be to achieve / can the attack retry infinite times to win the race, etc..

It is a denial of service attack. The user needs to be tricked into setting up their web page to this malicious page that exploit Chrome Goodies extension and uses the model user consent prompt.

The page can also steal some user information, such as promo codes, etc

Privileges and Capabilities - Identify which process is exploited and where code execution potentially can be achieved if the attacker can break out of that process, and explain why

Chrome API, specifically for ChromeOS. No privilege boundaries are crossed. User data can be released.

Origin of fix - Is the issue already known upstream, fixed by work from a previously known or reported issue, provided by the reporter, or any other information that would be relevant toward reward eligibility

Not an upstream. CrOS Engineers fixed it.

Mitigation - Detail any regarding mitigation considerations (we're run across a few comments, such as "we considered this issue to be highly mitigated" without explanation)

This is a web based exploit targeting DOS and stealing some information. There are no mitigation for that.

Severity assessment - why not higher, why not lower

Medium Severity: DoS is Security Impact None but the promo codes leak is a "sensitive user information that an attacker can exfiltrate" per our guidelines.

Why not high severity? The bug itself cannot be persisted unless the user is tricked into 1) opening the web page, 2) setting that as their homepage.

Why not low severity? The bug can directly access potential sensitive user information (such as promo codes).

### am...@chromium.org (2023-09-26)

[Empty comment from Monorail migration]

### ad...@gmail.com (2023-11-15)

Any updates on the reward for this bug? It's been over 90 days since a reward was confirmed and over 190 days since I reported it.

### [Deleted User] (2023-11-17)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@google.com (2023-12-07)

[Empty comment from Monorail migration]

### am...@google.com (2023-12-08)

[Empty comment from Monorail migration]

### is...@google.com (2023-12-08)

This issue was migrated from crbug.com/chromium/1443214?no_tracker_redirect=1

[Monorail blocking: b/281468020]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40064406)*
