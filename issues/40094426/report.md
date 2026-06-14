# use-after-free happening in unittest LayerTreeHostImplTest.ScrollSnapOnY

| Field | Value |
|-------|-------|
| **Issue ID** | [40094426](https://issues.chromium.org/issues/40094426) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Blink>Input, Blink>Scroll |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | Ma...@microsoft.com |
| **Assignee** | sa...@chromium.org |
| **Created** | 2019-03-28 |
| **Bounty** | $3,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3739.0 Safari/537.36 Edg/75.0.111.0

Steps to reproduce the problem:
1. Run the command cc_unittests --gtest_filter="LayerTreeHostImplTest.ScrollSnapOnY" --gtest_repeat=100
2. Even though the

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094426)*
