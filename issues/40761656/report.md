# Loading remotely hosted JavaScript files in V3

| Field | Value |
|-------|-------|
| **Issue ID** | [40761656](https://issues.chromium.org/issues/40761656) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P4 |
| **Component** | Blink>SecurityFeature>ContentSecurityPolicy, Platform>Extensions |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | [Deleted User] |
| **Assignee** | rd...@chromium.org |
| **Created** | 2021-04-19 |
| **Bounty** | $1,000.00 |

## Description

As per the migration guide (https://developer.chrome.com/docs/extensions/mv3/intro/mv3-overview/#remotely-hosted-code) of the chrome extension V3, the extension can't allow loading of remotely hosted code like JavaScript or Wasm files, and the script-src directive of Content security policy (CSP)

## Attachments

- [V3-loads-remote-hosted-code.zip](attachments/V3-loads-remote-hosted-code.zip) (application/octet-stream, 1.9 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40761656)*
