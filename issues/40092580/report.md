# Data URLs can be loaded on the top frame using iOS Mobile Chrome

| Field | Value |
|-------|-------|
| **Issue ID** | [40092580](https://issues.chromium.org/issues/40092580) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>Navigation |
| **Platforms** | iOS |
| **Reporter** | pi...@gmail.com |
| **Assignee** | eu...@chromium.org |
| **Created** | 2018-09-29 |
| **Bounty** | $500.00 |

## Description

Steps to reproduce the problem:
1. View "<script>document.location.href = "data:text/html,Hello!";</script>" on Desktop Chrome
2. Notice "Not allowed to navigate top frame to data URL" error in developer console
3. View same page in mobile Chrome for iOS
4. Watch top frame load the data URL with

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092580)*
