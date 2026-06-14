# Security: Failed Debug Check in src/compiler/verifier.cc, line 121

| Field | Value |
|-------|-------|
| **Issue ID** | [40094379](https://issues.chromium.org/issues/40094379) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Compiler |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows |
| **Reporter** | tm...@acu.edu |
| **Assignee** | ja...@chromium.org |
| **Created** | 2019-03-26 |
| **Bounty** | $3,000.00 |

## Description

Note: Not super familiar with v8, so this might not be a security issue.  
  
**VULNERABILITY DETAILS**   
A debug check fails when running either of the attached scripts. This was found with Fuzzilli (https://github.com/googleprojectzero/fuzzilli)  
  
**VERSION**   
v8 Master branch, Commit 33fa60

## Attachments

- [testcase1.js](attachments/testcase1.js) (text/plain, 1.2 KB)
- [testcase2.js](attachments/testcase2.js) (text/plain, 922 B)
- [liveBuildCrash.js](attachments/liveBuildCrash.js) (text/plain, 925 B)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094379)*
