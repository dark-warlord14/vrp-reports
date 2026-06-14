# Security: Use after free in MojoCdmService

| Field | Value |
|-------|-------|
| **Issue ID** | [40096143](https://issues.chromium.org/issues/40096143) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | Internals>Media>Encrypted |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | hi...@gmail.com |
| **Assignee** | jr...@chromium.org |
| **Created** | 2019-08-29 |
| **Bounty** | $30,000.00 |

## Description

(filed on behalf of the reporter)

The bug:

The root cause is [MojoCdmService::Initialize](https://cs.chromium.org/chromium/src/media/mojo/mojom/content_decryption_module.mojom?l=82&ct=xref_jump_to_def) can be called multiple times. 

```c++
void MojoCdmService::Initialize(const std::string&

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40096143)*
