# Heap-use-after-free in content::IndexedDBBackingStore::Transaction::ChainedBlobWriterImpl::ReportWriteC

| Field | Value |
|-------|-------|
| **Issue ID** | [40083362](https://issues.chromium.org/issues/40083362) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | Blink>Storage>IndexedDB |
| **Platforms** | Windows |
| **Reporter** | th...@gmail.com |
| **Assignee** | cm...@chromium.org |
| **Created** | 2015-12-10 |
| **Bounty** | $5,500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6608324696473600

Fuzzer: therealholden_worker
Job Type: windows_asan_chrome
Platform Id: windows

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x05981d80
Crash State:
  content::IndexedDBBackingStore::Transaction::ChainedBlobWr

## Attachments

- [asan_trace.txt](attachments/asan_trace.txt) (text/plain, 11.9 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083362)*
