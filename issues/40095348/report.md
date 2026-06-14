# Security: Multiple vulnerabilities in chromeos-disk-firmware.sh

| Field | Value |
|-------|-------|
| **Issue ID** | [40095348](https://issues.chromium.org/issues/40095348) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | OS>Systems |
| **Platforms** | ChromeOS |
| **Reporter** | tm...@gmail.com |
| **Assignee** | gw...@chromium.org |
| **Created** | 2019-06-10 |
| **Bounty** | $1,000.00 |

## Description

The chromeos-disk-firmware-update.sh[1] script is called at boot from chromeos-disk-firmware-update.conf[2] during init. It is used to check for updates in the root disk firmware.

To actually exploit these issues, an attacker requires the following:
1) Deleting the /mnt/stateful_partition/unencr

## Attachments

- [chromeos-disk-firmware-update.patch](attachments/chromeos-disk-firmware-update.patch) (application/octet-stream, 6.4 KB)
- [chromeos-disk-firmware-update-remove-tmpdir-usage.patch](attachments/chromeos-disk-firmware-update-remove-tmpdir-usage.patch) (application/octet-stream, 3.8 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095348)*
