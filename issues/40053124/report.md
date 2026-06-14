# Security: Cross-Origin Redirect Detection with fetch (XS-Leak)

| Field | Value |
|-------|-------|
| **Issue ID** | [40053124](https://issues.chromium.org/issues/40053124) |
| **Status** | Accepted |
| **Severity** | Unknown |
| **Priority** | P4 |
| **Component** | Blink>Network>FetchAPI |
| **Reporter** | ku...@googlemail.com |
| **Created** | 2020-08-19 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**

It is possible to detect server redirects (3XX) with fetch and redirect mode "manual".

If the fetch redirect mode it is set to manual, redirects are not automatically followed and a special "opaqueredirect" response is returned. Normally, "redirect: manual" can not be used with no-cors requests. Chrome will return the following error:

> Request mode is "no-cors" but the redirect mode is not "follow".

However, when a "cors" request is issued with "redirect: manual" and a redirect occurs, an opaqueredirect-response is returned. In other browsers a CORS-policy error is raised instead (assuming cors is not allowed).

This allows an attacker to detect redirects for cross-origin sites. This can be used to detect the login status of a user: eg. <https://myaccount.google.com> will redirect to <https://myaccount.google.com/intro> if the user is not logged in.

**VERSION**

Chrome Version: 84.0.4147.125 (Official Build) (64-bit), stable  

Operating System: macOS Catalina OSX 10.15.5

**REPRODUCTION CASE**

What steps will reproduce the problem?

(1) Open poc.html that is attached to this report.  

(2) Press "Check" the button. If not logged into google a redirect will occur and the redirect is detected by the poc.

**CREDIT INFORMATION**

@kuntekinte

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 1.0 KB)

## Timeline

### mp...@chromium.org (2020-08-21)

Thanks for the report. This is a known issue, so marking as duplicate.

[Monorail components: Blink>Network>FetchAPI]

### am...@chromium.org (2022-01-28)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-01-28)

The later reported https://crbug.com/chromium/1251179 was triaged and a mitigation landed for it so adjusting this earlier report according; the VRP Panel reward is extended accordingly. 
A member of our finance team will be in touch soon to arrange payment. Thank for bringing this issue to our attention and allowing us the opportunity to rectify it. 

### [Deleted User] (2022-01-28)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2022-01-29)

[Empty comment from Monorail migration]

### is...@google.com (2022-01-29)

This issue was migrated from crbug.com/chromium/1119450?no_tracker_redirect=1

[Monorail mergedinto: crbug.com/chromium/1251179]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40053124)*
