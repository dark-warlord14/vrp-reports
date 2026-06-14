# V8 Invalid Read in v8::internal::HeapObject::IsHeapNumber

| Field | Value |
|-------|-------|
| **Issue ID** | [40095714](https://issues.chromium.org/issues/40095714) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>JavaScript |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | lu...@microsoft.com |
| **Assignee** | rm...@chromium.org |
| **Created** | 2019-07-15 |
| **Bounty** | $2,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36

Steps to reproduce the problem:

1. Test Environment

commit: 
```
	117ddc8f6d026dfef11a61a93467956d9247868c
```

x64.debug args.gn:

```
	is_component_build

## Attachments

- [reduced_poc.js](attachments/reduced_poc.js) (text/plain, 584 B)
- [original.js](attachments/original.js) (text/plain, 2.3 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095714)*
