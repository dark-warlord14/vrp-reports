# V8 OOB write BigInt64Array.of and BigInt64Array.from side effect neuter

| Field | Value |
|-------|-------|
| **Issue ID** | [40092033](https://issues.chromium.org/issues/40092033) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | bt...@gmail.com |
| **Assignee** | jk...@chromium.org |
| **Created** | 2018-07-26 |
| **Bounty** | $5,000.00 |

## Description

Vulnerability Details
This appears to be a bug that was introduced after fixing 816961. I don't have permission to view the issue, but the regression test `regress-crbug-816961.js` covers all cases except the BigInt64Array codepath.

`TypedArrayOf`(builtins-typedarray.cc:1634) has a special case

## Attachments

- [bigint-v8.js](attachments/bigint-v8.js) (text/plain, 492 B)
- [gdb_output.txt](attachments/gdb_output.txt) (text/plain, 6.9 KB)
- [bigint-v8.js](attachments/bigint-v8_53265232.js) (text/plain, 484 B)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092033)*
