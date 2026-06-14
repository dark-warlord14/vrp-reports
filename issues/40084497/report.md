# Security: Devtools old remote frontend allows running privileged scripts via overwriting localStorage settings

| Field | Value |
|-------|-------|
| **Issue ID** | [40084497](https://issues.chromium.org/issues/40084497) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>DevTools>Extensions |
| **Reporter** | gr...@gmail.com |
| **Assignee** | dg...@chromium.org |
| **Created** | 2016-06-07 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**   
Specially crafted input to whitelisted URLs on Devtools remote frontend, allows an attacker to manipulate Devtool settings stored in localStorage. One possible injection point that allows attacker to run arbitrary javascript code is via watchExpression that runs in the c

## Attachments

- [Devtools-Crafted-URI1.txt](attachments/Devtools-Crafted-URI1.txt) (text/plain, 1.4 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084497)*
