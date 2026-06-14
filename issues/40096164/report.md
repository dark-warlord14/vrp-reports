# Security: Possible to spoof URL through use of document.open

| Field | Value |
|-------|-------|
| **Issue ID** | [40096164](https://issues.chromium.org/issues/40096164) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Navigation |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | de...@gmail.com |
| **Assignee** | ar...@chromium.org |
| **Created** | 2019-09-02 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**   
When a browser-initiated navigation is pending, a page can override it with something like location.reload, at least in the case where the page has user activation. If a page with user activation calls location.reload followed by document.open, any pending navigation wil

## Attachments

- [index.html](attachments/index.html) (text/plain, 533 B)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40096164)*
