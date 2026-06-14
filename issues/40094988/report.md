# Security DCHECK failure: !object || (object->IsText()) in layout_text.h

| Field | Value |
|-------|-------|
| **Issue ID** | [40094988](https://issues.chromium.org/issues/40094988) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>Layout |
| **Platforms** | Linux |
| **Reporter** | cl...@chromium.org |
| **Assignee** | ko...@chromium.org |
| **Created** | 2019-05-12 |
| **Bounty** | $3,500.00 |

## Description

Detailed report: https://clusterfuzz.com/testcase?key=6231084554125312

Fuzzer: attekett_dom_fuzzer
Job Type: linux_asan_chrome_media
Platform Id: linux

Crash Type: Security DCHECK failure
Crash Address: 
Crash State:
  !object || (object->IsText()) in layout_text.h
  blink::LayoutNGListItem::Updat

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094988)*
