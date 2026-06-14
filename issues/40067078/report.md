# Security: Device chooser dialogs do not show origin correctly for web pages with non-standard URLs

| Field | Value |
|-------|-------|
| **Issue ID** | [40067078](https://issues.chromium.org/issues/40067078) |
| **Status** | Fixed |
| **Severity** | Unknown |
| **Priority** | P4 |
| **Component** | Blink>Bluetooth, Blink>HID, Blink>Serial, Blink>USB |
| **Reporter** | al...@alesandroortiz.com |
| **Created** | 2023-07-08 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**   
Device chooser dialogs, such as Bluetooth, USB, Serial, HID, and others, do not show the requesting origin correctly for web pages with non-standard URLs [1], such as `about:blank`, `javascript:`, `blob:`, and `data:` URLs. There may be other unidentified schemes that al

## Attachments

- [device-chooser-basic_usb_javascript.png](attachments/device-chooser-basic_usb_javascript.png) (image/png, 29.5 KB)
- [device-chooser-basic_usb_about-blank-origin-spoof.png](attachments/device-chooser-basic_usb_about-blank-origin-spoof.png) (image/png, 29.6 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40067078)*
