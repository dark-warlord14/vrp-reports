# Security: Chrome (Mac OS X) - Arbitrary File Permission Modification

| Field | Value |
|-------|-------|
| **Issue ID** | [40094390](https://issues.chromium.org/issues/40094390) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Internals>Installer |
| **Platforms** | Mac |
| **Reporter** | [Deleted User] |
| **Assignee** | mi...@google.com |
| **Created** | 2019-03-26 |
| **Bounty** | $500.00 |

## Description

Chrome Version : 73.0.3683.86
OS Version: Mac OS X 10.14.2

What steps will reproduce the problem?

I noticed when using Google Chrome on Mac OS X that it performs an insecure file write to /private/tmp that could lead to a privilege escalation and/or sensitive data being compromised via a basi

## Attachments

- [Chrome.flv](attachments/Chrome.flv) (application/octet-stream, 2.7 MB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094390)*
