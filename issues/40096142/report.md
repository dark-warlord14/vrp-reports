# Security: OOB Access in V8 

| Field | Value |
|-------|-------|
| **Issue ID** | [40096142](https://issues.chromium.org/issues/40096142) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript, Blink>JavaScript>Runtime |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | hi...@gmail.com |
| **Assignee** | si...@chromium.org |
| **Created** | 2019-08-29 |
| **Bounty** | $10,000.00 |

## Description

(filed on behalf of the reporter)

The bug:

We know that, the size of JSFunctin object in v8 is not fixed. it may contain the field PrototypeOrInitialMap or not. But the macro [GetDerivedMap](https://cs.chromium.org/chromium/src/v8/src/builtins/base.tq?rcl=568f3984d3ead0863deb3e84eec4c0ccd33a49

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40096142)*
