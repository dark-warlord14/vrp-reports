# Security: PDFium Heap Buffer Overflow in CXFA_TextLayout::DoLayout

| Field | Value |
|-------|-------|
| **Issue ID** | [40093874](https://issues.chromium.org/issues/40093874) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Linux |
| **Reporter** | st...@gmail.com |
| **Assignee** | th...@chromium.org |
| **Created** | 2019-01-28 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**   
  
This issue affects the lastest version of PDFium ( https://pdfium.googlesource.com/pdfium/+/refs/heads/master ). When enabling XFA and ASAN, pdfium_test.exe shows the following log.  
  
Rendering PDF file C:\poc.pdf.  
Document has invalid cross reference table  
===

## Attachments

- deleted (application/octet-stream, 0 B)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093874)*
