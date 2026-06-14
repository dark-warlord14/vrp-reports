# mXSS: Potential XSS via noembed tags parsed by DOMParser APIs

| Field | Value |
|-------|-------|
| **Issue ID** | [40094073](https://issues.chromium.org/issues/40094073) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>HTML>Parser |
| **Platforms** | Windows |
| **Reporter** | ma...@gmail.com |
| **Assignee** | tk...@chromium.org |
| **Created** | 2019-02-19 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3710.0 Safari/537.36

Steps to reproduce the problem:
Chrome decodes HTML entities inside <noembed> tags when it is parsed by DOMParser APIs.

For example:
A <noembed> B &lt;/noembed&gt; C &

## Attachments

- [chrome_mxss_domparser_noembed.html](attachments/chrome_mxss_domparser_noembed.html) (text/plain, 660 B)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094073)*
