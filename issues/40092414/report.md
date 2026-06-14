# Security: url spoofing using 304 status code

| Field | Value |
|-------|-------|
| **Issue ID** | [40092414](https://issues.chromium.org/issues/40092414) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>Navigation, UI>Browser>Omnibox |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | je...@gmail.com |
| **Assignee** | mm...@chromium.org |
| **Created** | 2018-09-09 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**   
By pasting a url in the omnibox that leads to a request with status code 304 (not modified) and then pressing enter, the page doesn't load but the url stays there. Using window.onbeforeunload it is possible to see when the user hits enter. This way one can create a malic

## Attachments

- [dangerous.html](attachments/dangerous.html) (text/plain, 1.0 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092414)*
