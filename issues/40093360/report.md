# Security: V8: Incorrect type information on SpeculativeSafeIntegerSubtract

| Field | Value |
|-------|-------|
| **Issue ID** | [40093360](https://issues.chromium.org/issues/40093360) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Compiler |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ja...@gmail.com |
| **Assignee** | na...@google.com |
| **Created** | 2018-12-10 |
| **Bounty** | $5,000.00 |

## Description

== VULNERABILITY DETAILS ==

The typer sets the type of SpeculativeSafeIntegerSubtract to an
intersection with kSafeInteger. This is missing the -0 case. In
particular, ((-0) - 0) should return (-0), but due to the
intersection, the typer ignores this return value. This can be used to
perform

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093360)*
