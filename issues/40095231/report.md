# UXSS via Object::GetRealNamedPropertyInPrototypeChain

| Field | Value |
|-------|-------|
| **Issue ID** | [40095231](https://issues.chromium.org/issues/40095231) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | se...@gmail.com |
| **Assignee** | ab...@chromium.org |
| **Created** | 2011-09-16 |
| **Bounty** | $2,337.00 |

## Description

**VULNERABILITY DETAILS**   
As in http://code.google.com/p/chromium/issues/detail?id=95671, an attacker changes the name of a child frame, however, this time it's set to the name of one of the window.__proto__ properties.  
  
Then Object::GetRealNamedPropertyInPrototypeChain is used to get that pr

## Attachments

- [repro-6.html](attachments/repro-6.html) (text/html; charset=us-ascii, 570 B)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095231)*
