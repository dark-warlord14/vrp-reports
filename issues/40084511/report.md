# Security: Parameter sanitization failure in DevTools leads to privileged script execution

| Field | Value |
|-------|-------|
| **Issue ID** | [40084511](https://issues.chromium.org/issues/40084511) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>DevTools>Extensions |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | gr...@gmail.com |
| **Assignee** | dg...@chromium.org |
| **Created** | 2016-06-08 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**   
Same vulnerability as https://crbug.com/chromium/607939. Fix for it is insufficient as it checks only if "remoteFrontendUrl" starts with "https://chrome-devtools-frontend.appspot.com/" but fails to sanitize any data that follows it. Since the remoteFrontendUrl is decoded

## Attachments

- [Devtools-Crafted-URI2.txt](attachments/Devtools-Crafted-URI2.txt) (text/plain, 1.7 KB)
- [SuggestedPatchFunction.txt](attachments/SuggestedPatchFunction.txt) (text/plain, 546 B)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084511)*
