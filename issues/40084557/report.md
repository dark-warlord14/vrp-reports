# Security: Devtools has Insuffient sanitization of remoteBase parameter

| Field | Value |
|-------|-------|
| **Issue ID** | [40084557](https://issues.chromium.org/issues/40084557) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>DevTools>Extensions |
| **Reporter** | gr...@gmail.com |
| **Assignee** | dg...@chromium.org |
| **Created** | 2016-06-12 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**   
Same vulnerability as https://crbug.com/chromium/571121. Fix for that issue is insufficient, as the sanitization process only checks if remoteBase URL starts with "https://chrome-devtools-frontend.appspot.com/". However, the loadScriptsPromise() that loads the remote scr

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084557)*
