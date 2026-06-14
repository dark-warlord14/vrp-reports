# WebCore::SVGUseElement::updateContainerOffsets ExecAV@Arbitrary (1dc75f12fe3750aa1828ea20506a5d54)

| Field | Value |
|-------|-------|
| **Issue ID** | [40079507](https://issues.chromium.org/issues/40079507) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | ao...@gmail.com |
| **Assignee** | ma...@chromium.org |
| **Created** | 2010-03-01 |
| **Bounty** | $500.00 |

## Description

Opening the attached SVG file or a page containing it causes a segmentation
fault in WebCore::SVGUseElement::setHrefBaseValue in 32-bit Ubuntu 9.10.
Builds 36515 up to the current 40259 appear to be affected. In 64-bit
Fedora 12 the issue manifests as the tab getting stuck in loading, sad tab
or

## Attachments

- [bad2.svg](attachments/bad2.svg) (text/plain; charset=us-ascii, 133 B)
- [svg2-gdb.txt](attachments/svg2-gdb.txt) (text/plain, English; charset=us-ascii, 6.4 KB)
- [WebCore..SVGUseElement..updateContainerOffsets ExecAV@Arbitrary (1dc75f12fe3750aa1828ea20506a5d54).html](attachments/WebCore..SVGUseElement..updateContainerOffsets ExecAV@Arbitrary (1dc75f12fe3750aa1828ea20506a5d54).html) (exported SGML document text, 452.9 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40079507)*
