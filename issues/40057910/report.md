# [iOS] CSP Bypass via Service Worker

| Field | Value |
|-------|-------|
| **Issue ID** | [40057910](https://issues.chromium.org/issues/40057910) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Mobile>iOSWeb>Security |
| **Platforms** | iOS |
| **Reporter** | pr...@gmail.com |
| **Assignee** | aj...@google.com |
| **Created** | 2021-11-14 |
| **Bounty** | $500.00 |

## Description

Steps to reproduce the problem:
1. Open https://cm2.pw/research/sw/csp-bypass?url=https://httpbin.org/get
2. Notice the Content-Security-Policy
3. Click on Exec

You should see the response from httpbin.org printed on the screen even though the policy does not have httpbin.org in any of the CSP

## Attachments

- [csp-sw.html](attachments/csp-sw.html) (text/plain, 871 B)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057910)*
