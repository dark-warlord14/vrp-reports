# Security: content security policy bypass by writing to loading Frame's ContentDocument

| Field | Value |
|-------|-------|
| **Issue ID** | [40089425](https://issues.chromium.org/issues/40089425) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>SecurityFeature>ContentSecurityPolicy |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ma...@gmail.com |
| **Assignee** | an...@chromium.org |
| **Created** | 2017-10-27 |
| **Bounty** | $1,000.00 |

## Description

AFFECTED PRODUCTS
--------------------
chrome 62.0.3202.62 stable


DESCRIPTION
--------------------
online demo:
http://xsser.math1as.com/csp2.html

this problem occurs because of when load a http URL , the csp would lost,but as a matter of fact, the document.domain is "about:blank" until

## Attachments

- [ff.jpg](attachments/ff.jpg) (image/jpeg, 47.3 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40089425)*
