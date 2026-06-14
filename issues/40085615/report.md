# Security: Internal functions leaked when DevTools is open

| Field | Value |
|-------|-------|
| **Issue ID** | [40085615](https://issues.chromium.org/issues/40085615) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>DevTools>Extensions |
| **Reporter** | pi...@live.nl |
| **Assignee** | ko...@chromium.org |
| **Created** | 2016-10-06 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**   
If DevTools is open, then a script [1] is run in the context of the webpage. The script has some cases of `__proto__: null`, presumably to prevent accessors on `Object.prototype` from messing with the objects in there. However, the assignment `InjectedScript.primitiveTyp

## Attachments

- [bug.html](attachments/bug.html) (text/plain, 2.1 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40085615)*
