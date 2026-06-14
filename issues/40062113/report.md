# Security: ChromeOS wpa_supplicant arbitrary shared object load

| Field | Value |
|-------|-------|
| **Issue ID** | [40062113](https://issues.chromium.org/issues/40062113) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Unknown |
| **Platforms** | ChromeOS |
| **Reporter** | ro...@rorym.cnamara.com |
| **Assignee** | dr...@chromium.org |
| **Created** | 2022-12-07 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**   
Dbus callers of wpa_supplicant CreateInterface (users root, wpa, shill) can induce wpa_supplicant to load a shared object by defining it in a new configuration file and passing the file to CreateInterface. A separate wpa_supplicant dbus caller (any user) can inject a fil

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062113)*
