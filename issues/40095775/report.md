# Security: Use-after-free of CommandLineAPIScope object

| Field | Value |
|-------|-------|
| **Issue ID** | [40095775](https://issues.chromium.org/issues/40095775) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Unknown |
| **Platforms** | Linux, Mac, Windows |
| **Reporter** | de...@gmail.com |
| **Assignee** | ya...@chromium.org |
| **Created** | 2019-07-20 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**   
When the user runs a command in the devtools console, the code that's run is given access to the console utility functions. This is implemented through the use of a CommandLineAPIScope object. This object has a specific lifetime, but it's possible for JavaScript code to

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095775)*
