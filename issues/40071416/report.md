# Security vulnerability in WebP

| Field | Value |
|-------|-------|
| **Issue ID** | [40071416](https://issues.chromium.org/issues/40071416) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Images>Codecs |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | mk...@chromium.org |
| **Assignee** | jz...@chromium.org |
| **Created** | 2023-09-06 |
| **Bounty** | $10,000.00 |

## Description

Copying this from an email to security@chromium.org. Marking as critical based on evidence of use in the wild:

"""
OE095807245816 - please include this ID in replies to this thread.

Portions Copyright (c) 2023 Apple Inc.

Permission is hereby granted, free of charge, to any person obtaining

## Attachments

- [libwebp_HuffmanCodes-copy.pdf](attachments/libwebp_HuffmanCodes-copy.pdf) (application/pdf, 185.7 KB)
- [replicatevalue_poc.not_webp](attachments/replicatevalue_poc.not_webp) (application/octet-stream, 1.0 KB)
- [patch](attachments/patch) (text/plain, 9.9 KB)
- [patch](attachments/patch_53345418) (text/plain, 14.6 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40071416)*
