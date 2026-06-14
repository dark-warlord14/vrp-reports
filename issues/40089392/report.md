# Security: Stack Buffer Overflow in QuicClientPromisedInfo::OnPromiseHeaders

| Field | Value |
|-------|-------|
| **Issue ID** | [40089392](https://issues.chromium.org/issues/40089392) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | Internals>Network>QUIC |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ne...@gmail.com |
| **Assignee** | rc...@chromium.org |
| **Created** | 2017-10-24 |
| **Bounty** | $10,500.00 |

## Description

VULNERABILITY DETAILS
The QUIC Protocol has a feature called "Server Push", where a server
can push resources to a client before they are explicitly requested,
to prevent unneeded round-trips. When handling push headers,
QuicClientPromisedInfo::OnPromiseHeaders assumes that the `:method`
header

## Attachments

- [asan.log](attachments/asan.log) (text/plain, 10.3 KB)
- deleted (application/octet-stream, 0 B)
- [server.patch](attachments/server.patch) (application/octet-stream, 1.3 KB)
- [www.example.org.tar](attachments/www.example.org.tar) (application/octet-stream, 8.5 KB)
- [fix.patch](attachments/fix.patch) (application/octet-stream, 1.9 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40089392)*
