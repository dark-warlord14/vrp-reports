# Security: SEGV in turboshaft-loop-peeling

| Field | Value |
|-------|-------|
| **Issue ID** | [41491373](https://issues.chromium.org/issues/41491373) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Blink>JavaScript, Blink>JavaScript>Compiler |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **CVE IDs** | CVE-2016-9651, CVE-2017-5053 |
| **Reporter** | ki...@gmail.com |
| **Assignee** | dm...@chromium.org |
| **Created** | 2024-01-15 |
| **Bounty** | $8,000.00 |

## Description

VULNERABILITY DETAILS
## INTRODUCE
After bisect, it was determined that following commit caused this problem.

- Commit Info
    - Version: 91113
    - link: https://crrev.com/bde0ed46a0fd612b6126988c54c1100c56a80b7a
- Commit Message

```
commit bde0ed46a0fd612b6126988c54c1100c56a80b7a
Author: Nico

## Attachments

- [poc.js](attachments/poc.js) (text/plain, 450 B)
- deleted (application/octet-stream, 0 B)
- [poc.js](attachments/poc_53290269.js) (text/plain, 450 B)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/41491373)*
