# Security: Use-after-free with XSLT strip-space

| Field | Value |
|-------|-------|
| **Issue ID** | [40056191](https://issues.chromium.org/issues/40056191) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>XML |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | we...@aevum.de |
| **Assignee** | ja...@chromium.org |
| **Created** | 2021-06-12 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**   
There's a bug in libxslt which can result in use-after-free in connection with the <xsl:strip-space> feature. Under certain circumstances, function xsltApplyTemplates can delete text nodes which are still referenced from variables, keys or possibly other data structures.

## Attachments

- [uaf.xml](attachments/uaf.xml) (text/plain, 912 B)
- [0001-Fix-use-after-free-in-xsltApplyTemplates.patch](attachments/0001-Fix-use-after-free-in-xsltApplyTemplates.patch) (text/plain, 6.0 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40056191)*
