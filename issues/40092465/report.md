# Security: ChromeOS root Command Execution

| Field | Value |
|-------|-------|
| **Issue ID** | [40092465](https://issues.chromium.org/issues/40092465) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Network>VPN |
| **Platforms** | ChromeOS |
| **Reporter** | ro...@rorym.cnamara.com |
| **Assignee** | xz...@chromium.org |
| **Created** | 2018-09-15 |
| **Bounty** | $11,337.00 |

## Description

**VULNERABILITY DETAILS**   
Using vulnerabilities in cups, shill, and insecure upstart configuration files, it was found to be possible to obtain root command execution in Chrome OS.  
This vulnerability chain requires manual installation, and is likely not automatable without substantial browser e

## Attachments

- [exploit.ppd](attachments/exploit.ppd) (application/octet-stream, 232.3 KB)
- [dataurl.pdf](attachments/dataurl.pdf) (application/pdf, 14.5 KB)
- [shillesc.sh](attachments/shillesc.sh) (text/plain, 1.7 KB)
- [cupstestppd_pathrestriction.patch](attachments/cupstestppd_pathrestriction.patch) (application/octet-stream, 695 B)
- [openvpn_management_server_EscapeToQuote_username.patch](attachments/openvpn_management_server_EscapeToQuote_username.patch) (application/octet-stream, 748 B)
- [cupsd_init_symlink.patch](attachments/cupsd_init_symlink.patch) (application/octet-stream, 836 B)
- [server.conf](attachments/server.conf) (application/octet-stream, 266 B)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092465)*
