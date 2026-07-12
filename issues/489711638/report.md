# Security: WinUSB - multiple issues

| Field | Value |
|-------|-------|
| **Issue ID** | [489711638](https://issues.chromium.org/issues/489711638) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>USB |
| **Platforms** | Windows |
| **CVE IDs** | CVE-2018-6125, CVE-2023-45866 |
| **Reporter** | cn...@yubico.com |
| **Assignee** | re...@chromium.org |
| **Created** | 2026-03-04 |
| **Bounty** | $5,000.00 |

## Description

---

### Report description

WebUSB bug bypasses Chromium's protected USB class restrictions, giving any webpage unrestricted access to USB devices.

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

#### Which URL (or repository) have you found the vulnerability in?

<https://chromium.googlesource.com/chromium/src/+/main/services/device/usb/mojo/device_impl.cc>

---

### The problem

#### Please describe the technical details of the vulnerability

WebUSB's `controlTransferOut` and `controlTransferIn` allow any webpage to send arbitrary USB control transfers to **all interfaces** on a device — including protected classes (Bluetooth 0xE0, mass storage, smart cards, WiFi adapters and more) — by setting `recipient: "device"`. This completely bypasses Chromium's `blocked_interface_classes_` enforcement, which was introduced in [CVE-2018-6125](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2018-6125) (<https://issues.chromium.org/issues/40090681>) to prevent web pages from accessing security-sensitive USB interfaces.

The attack requires only **one click** from the user — selecting any USB device in the WebUSB chooser. After that single click, the webpage has full, unrestricted control over the device, including all protected interfaces the user never intended to expose.

A single call to `device.controlTransferOut({requestType: 'class', recipient: 'device', request: 0, value: 0, index: 0}, hciPayload)` sends arbitrary HCI commands to a USB Bluetooth adapter (for example) — despite class 0xE0 being blocked. The same bypass works for any protected USB device class.

**PoC attached:** `bt_exploit_poc.html` — single-page exploit that demonstrates full, unrestricted HCI control of a USB Bluetooth adapter from a webpage (I chose to focus on BT dongle for this PoC because I did not have any other hardware to test this on, but this is valid for smart cards, WiFi chips, and many other protected devices). The PoC shows:

1. Connect to any USB BT dongle via the WebUSB chooser.
2. Verify `claimInterface(0)` is blocked (class 0xE0 protection active).
3. Bypass the protection: send `HCI_Write_Scan_Enable` + `HCI_Write_Simple_Pairing_Mode` via `controlTransferOut(recipient:'device')` — the dongle becomes discoverable + connectable to nearby devices.
4. Change the dongle's Bluetooth name to an arbitrary string (sends `HCI_Write_Local_Name` + `HCI_Write_Extended_Inquiry_Response`) — visible on any nearby phone/laptop scanning for Bluetooth.
5. Send additional HCI commands: disable authentication, disable encryption, read BD\_ADDR — proving full HCI control.
   (Of course, after the first click from the user that chooses the device, the next clicks are not needed, and I added the buttons in the PoC page for ease of understanding the attack steps.)

**PoC video - <https://youtu.be/o7nxTAua9wA>** Demonstrates the exploit end-to-end on two machines. A second computer's Bluetooth scan initially doesn't show the target device. The victim machine runs the PoC: connects the USB BT dongle, verifies `claimInterface` is blocked, then clicks "Make Connectable." The second computer's scan now shows the dongle appearing as "Bluetooth - Ariel's MacBook Pro." The PoC then changes the name to "HACKED\_BY\_WEBUSB" — the second computer's rescan confirms the name change. Finally, bonus commands disable authentication and encryption, proving unrestricted HCI access.

**Tested on:** Chrome Version 145.0.7632.117 macOS 26.3 and Ubuntu 24.04. Affects all platforms with WebUSB support (Windows, macOS, Linux, ChromeOS, etc).

**Root cause:**

The CVE-2018-6125 fix added `blocked_interface_classes_` to prevent web access to sensitive USB classes (Bluetooth 0xE0, mass storage 0x08, etc.). This protection is correctly enforced in `ClaimInterface()` (device\_impl.cc:277–282), which checks every alternate setting's class code before allowing an interface to be claimed.

However, `HasControlTransferPermission()` was implemented with an early-return that **exempts** DEVICE and OTHER recipients from all validation:

```
// device_impl.cc:162-164
if (recipient != UsbControlTransferRecipient::INTERFACE &&
    recipient != UsbControlTransferRecipient::ENDPOINT) {
  return true;  // ← BUG: skips blocked_interface_classes_ check entirely
}

```

This creates a 2-layer bypass:

1. **Renderer (Blink):** `ConvertControlTransferParameters` performs no validation for `recipient: "device"` — no `EnsureInterfaceClaimed`, no class check.
2. **Browser (device service):** `HasControlTransferPermission` returns `true` unconditionally for DEVICE/OTHER recipients — no `blocked_interface_classes_` check.

The fix should validate that DEVICE-recipient control transfers do not target functionality of blocked interface classes. For class-specific requests (`requestType: "class"`), the `index` field typically identifies the target interface — this should be checked against `blocked_interface_classes_` regardless of recipient type.

#### Impact analysis

Any website can exploit this — no special permissions, no extensions, no user login required. The user only needs to click once in the WebUSB
device chooser. Obtaining this click is straightforward via social engineering — a phishing page posing as a legitimate USB device configuration
tool, firmware updater, or printer setup wizard naturally prompts the user to "select your device" from the chooser - no security warning present.

What the attacker gains — full control over protected USB device classes:

- Bluetooth adapter takeover: As shown in the PoC video - send arbitrary HCI commands to take over the system's Bluetooth radio — make it discoverable, disable
  authentication and encryption, change its name. This likely enables CVE-2023-45866-style keyboard injection: a nearby attacker pairs as a
  fake HID keyboard via SSP Just Works (no user prompt) and injects keystrokes for remote code execution.
- WiFi adapter firmware overwrite: USB WiFi chipsets (Realtek RTL8xxxU, Atheros, MediaTek) accept firmware upload via vendor
  control transfers on EP0. A webpage could theoretically push a backdoored firmware image, achieving persistent code execution on the WiFi chip
  that survives browser restarts.
- Many other attacks that I did not verify; Smart card readers, FIDO keys, and mass storage devices all accept commands via control
  transfers — theoretically allowing certificate exfiltration, data theft, or unauthorized signing from a webpage. DFU-capable devices (keyboards,
  mice, dongles) could have their firmware overwritten for persistent hardware compromise.

The core issue: the user clicks "Connect" for one device, but the attacker silently accesses every protected interface on it. The CVE-2018-6125
protection that was supposed to prevent exactly this is completely bypassed.

---

### The cause

#### What version of Chrome have you found the security issue in?

Version 145.0.7632.117 Stable

#### Is the security issue related to a crash?

No, it is not related to a crash.

#### Choose the type of vulnerability

Exploit Mitigation Bypass

#### How would you like to be publicly acknowledged for your report?

Ariel Simon

## Attachments

- [bt_exploit_poc.html](attachments/bt_exploit_poc.html) (text/html, 11.7 KB)
- [bt_exploit_poc.html](attachments/bt_exploit_poc_73976679.html) (text/html, 11.7 KB)

## Timeline

### me...@google.com (2026-03-05)

Thanks for the report.

reillyg: Could you please take a look?

### re...@chromium.org (2026-03-05)

The mitigation here is probably to look at whether the device class is on the restricted class list, or if there is no interface that isn't on the restricted class list, when deciding whether to allow commands which are not directed to a particular interface. Reading the spec strictly the device shouldn't be replying to HCI commands that aren't directed to the interface but it's easy to skip those checks in firmware.

Matt is the current owner for this feature.

### ch...@google.com (2026-03-05)

Setting milestone because of s0/s1 severity.

### re...@chromium.org (2026-03-05)

There's an unfortunate trade-off here where I suspect that fixing this will probably break some legitimate sites using WebUSB because interacting with their unprotected interfaces requires sending control transfers with a recipient of `"device"` or `"other"`.

As for exploitability, what steps outside the browser were required in order for you to get Chrome to access the device? For example on Windows a manual driver change was likely required. This is probably blocked by the permission\_broker on ChromeOS. It may be exploitable without extra steps on macOS.

### ar...@gmail.com (2026-03-05)

On macOS latest version (26.3) : No steps outside the browser were required. Plugged in a USB BT dongle (CSR8510), opened Chrome, ran the PoC, HCI commands were accepted immediately.
I did not test this on Windows.

### dx...@google.com (2026-03-19)

Project: chromium/src  

Branch:  main  

Author:  Alvin Ji [alvinji@chromium.org](mailto:alvinji@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7677820>

WebUSB: Strengthen control transfer protection for protected classes

---


Expand for full commit details
```
     
    Strengthens control transfer permissions to block requests targeting 
    protected interface classes like HID or Mass Storage. Requests are now 
    scrutinized for protected interfaces via the wIndex field regardless of 
    recipient. Standard requests for device-level management remain allowed. 
    This behavior is gated by the kWebUsbProtectedClassControlTransferBlock 
    feature flag. 
     
    Bug: 489711638 
    Change-Id: Ic69c88f81e2a10abcaa80832b330d3789493f3b2 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7677820 
    Reviewed-by: Reilly Grant <reillyg@chromium.org> 
    Commit-Queue: Alvin Ji <alvinji@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1601756}

```

---

Files:

- M `services/device/public/cpp/device_features.cc`
- M `services/device/public/cpp/device_features.h`
- M `services/device/usb/mojo/BUILD.gn`
- M `services/device/usb/mojo/device_impl.cc`
- M `services/device/usb/mojo/device_impl.h`
- M `services/device/usb/mojo/device_impl_unittest.cc`

---

Hash: [89b42d2d3326ebad6e0494009d5d92f2dbaf12ef](https://chromiumdash.appspot.com/commit/89b42d2d3326ebad6e0494009d5d92f2dbaf12ef)  

Date: Thu Mar 19 04:55:14 2026


---

### dx...@google.com (2026-03-24)

Project: chromium/src  

Branch:  main  

Author:  Rob Pitkin [robpitkin@google.com](mailto:robpitkin@google.com)  

Link:    <https://chromium-review.googlesource.com/7685741>

[WebUSB] Add UMA for control transfer permission telemetry

---


Expand for full commit details
```
     
    This CL adds comprehensive UMA telemetry to track the impact of the 
    WebUSB control transfer security fix (b:489711638). 
     
    Two distinct metrics are introduced: 
     
    1. WebUsb.ControlTransferPermissionOutcome: An enumerated histogram 
    tracking the high-level result of every permission check (Allowed, 
    Blocked, Interface Not Found, or No Configuration). This provides the 
    denominator needed to calculate real-world breakage ratios. 
     
    2. WebUsb.ControlTransferBlocked.{Direction}.{Type}: A tokenized sparse 
    histogram that records the specific USB interface class code being 
    blocked. This allows for granular root-cause analysis, helping 
    distinguish between malicious tunneling attempts and legitimate, 
    non-standard device routing that may have been caught by the new 
    restrictions. 
     
    The HasControlTransferPermission method signature was updated to include 
    the transfer direction to support the tokenized variants. 
     
    Bug: 489711638 
    Test: Verified with chrome://histograms using local test page. 
    Change-Id: Ibf7d49eb6b06b77e0c105b722fa03e55c6833a37 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7685741 
    Reviewed-by: Reilly Grant <reillyg@chromium.org> 
    Reviewed-by: Alvin Ji <alvinji@chromium.org> 
    Commit-Queue: Rob Pitkin <robpitkin@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1604293}

```

---

Files:

- M `services/device/usb/mojo/device_impl.cc`
- M `services/device/usb/mojo/device_impl.h`
- M `tools/metrics/histograms/enums.xml`
- M `tools/metrics/histograms/metadata/others/histograms.xml`

---

Hash: [e30b44e5d05722b43747fd04dcb8c6b52c5b56bc](https://chromiumdash.appspot.com/commit/e30b44e5d05722b43747fd04dcb8c6b52c5b56bc)  

Date: Tue Mar 24 19:20:55 2026


---

### ch...@google.com (2026-03-25)

Merge review required: M147 has already been cut for stable release.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: alonbajayo (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), harrysouders (Mobile US), eakpobaro (Mobile EMEA)

### ch...@google.com (2026-03-25)

Merge review required: M146 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: lmenezes (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), govind (Mobile US), eakpobaro (Mobile EMEA)

### al...@chromium.org (2026-03-26)

deleted

### ch...@google.com (2026-03-26)

Merge review required: M147 has already been cut for stable release.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: alonbajayo (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), harrysouders (Mobile US), eakpobaro (Mobile EMEA)

### ch...@google.com (2026-03-26)

Merge review required: M146 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: lmenezes (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), govind (Mobile US), eakpobaro (Mobile EMEA)

### al...@chromium.org (2026-03-26)

Hi @sr...@google.com  For "Merge review required: M147 has already been cut for stable release."

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?
The bug reveal an exploitable approach for a malicious website to control user machine's bluetooth adapter once user grant the usb bluetooth adapter permission to website. 

2. What changes specifically would you like to merge? Please link to Gerrit.
https://chromium-review.git.corp.google.com/c/chromium/src/+/7677820
https://chromium-review.git.corp.google.com/c/chromium/src/+/7685741

3. Have the changes been released and tested on canary?
Yes

4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
No

5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? 
N/A

6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.
No



### al...@chromium.org (2026-03-26)

Hi @sr...@google.com  For "Merge review required: M146 is already shipping to stable."

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?
The bug reveal an exploitable approach for a malicious website to control user machine's bluetooth adapter once user grant the usb bluetooth adapter permission to website. 

2. What changes specifically would you like to merge? Please link to Gerrit.
https://chromium-review.git.corp.google.com/c/chromium/src/+/7677820
https://chromium-review.git.corp.google.com/c/chromium/src/+/7685741

3. Have the changes been released and tested on canary?
Yes

4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
No

5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? 
N/A

6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.
No



### dr...@chromium.org (2026-03-26)

No crashes in Canary, approved to merge to M146 and M147.

### dx...@google.com (2026-03-26)

Project: chromium/src  

Branch:  refs/branch-heads/7727  

Author:  Alvin Ji [alvinji@chromium.org](mailto:alvinji@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7705645>

[M147] WebUSB: Strengthen control transfer protection for protected classes

---


Expand for full commit details
```
     
    Strengthens control transfer permissions to block requests targeting 
    protected interface classes like HID or Mass Storage. Requests are now 
    scrutinized for protected interfaces via the wIndex field regardless of 
    recipient. Standard requests for device-level management remain allowed. 
    This behavior is gated by the kWebUsbProtectedClassControlTransferBlock 
    feature flag. 
     
    (cherry picked from commit 89b42d2d3326ebad6e0494009d5d92f2dbaf12ef) 
     
    Bug: 489711638 
    Change-Id: Ic69c88f81e2a10abcaa80832b330d3789493f3b2 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7677820 
    Reviewed-by: Reilly Grant <reillyg@chromium.org> 
    Commit-Queue: Alvin Ji <alvinji@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1601756} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7705645 
    Reviewed-by: Matt Reynolds <mattreynolds@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7727@{#1603} 
    Cr-Branched-From: ce01102937348db7b88c8a4257ee4b3ac702eb1a-refs/heads/main@{#1596535}

```

---

Files:

- M `services/device/public/cpp/device_features.cc`
- M `services/device/public/cpp/device_features.h`
- M `services/device/usb/mojo/BUILD.gn`
- M `services/device/usb/mojo/device_impl.cc`
- M `services/device/usb/mojo/device_impl.h`
- M `services/device/usb/mojo/device_impl_unittest.cc`

---

Hash: [e35eb23a825edf77482f52a06c73c1f7d5e6365d](https://chromiumdash.appspot.com/commit/e35eb23a825edf77482f52a06c73c1f7d5e6365d)  

Date: Thu Mar 26 22:18:21 2026


---

### dx...@google.com (2026-03-26)

Project: chromium/src  

Branch:  refs/branch-heads/7680  

Author:  Alvin Ji [alvinji@chromium.org](mailto:alvinji@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7705887>

[M146] WebUSB: Strengthen control transfer protection for protected classes

---


Expand for full commit details
```
     
    Strengthens control transfer permissions to block requests targeting 
    protected interface classes like HID or Mass Storage. Requests are now 
    scrutinized for protected interfaces via the wIndex field regardless of 
    recipient. Standard requests for device-level management remain allowed. 
    This behavior is gated by the kWebUsbProtectedClassControlTransferBlock 
    feature flag. 
     
    (cherry picked from commit 89b42d2d3326ebad6e0494009d5d92f2dbaf12ef) 
     
    Bug: 489711638 
    Change-Id: Ic69c88f81e2a10abcaa80832b330d3789493f3b2 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7677820 
    Reviewed-by: Reilly Grant <reillyg@chromium.org> 
    Commit-Queue: Alvin Ji <alvinji@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1601756} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7705887 
    Reviewed-by: Matt Reynolds <mattreynolds@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7680@{#3291} 
    Cr-Branched-From: 76b7d80e5cda23fe6537eed26d68c92e995c7f39-refs/heads/main@{#1582197}

```

---

Files:

- M `services/device/public/cpp/device_features.cc`
- M `services/device/public/cpp/device_features.h`
- M `services/device/usb/mojo/BUILD.gn`
- M `services/device/usb/mojo/device_impl.cc`
- M `services/device/usb/mojo/device_impl.h`
- M `services/device/usb/mojo/device_impl_unittest.cc`

---

Hash: [da6257f9494029844717cd9ea67306d466d30b06](https://chromiumdash.appspot.com/commit/da6257f9494029844717cd9ea67306d466d30b06)  

Date: Thu Mar 26 22:38:14 2026


---

### pe...@google.com (2026-03-30)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### pe...@google.com (2026-04-08)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2026-04-08)

1. https://chromium-review.git.corp.google.com/c/chromium/src/+/7725849
2. Low - There was no conflict.
3. 146 and 147
4. Yes, the CL that introduced this bug was merged in 2018.

### sp...@google.com (2026-04-08)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
Baseline. Web Platform Privilege Escalation


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### an...@google.com (2026-04-10)

Merge approved for LTS-138

### dx...@google.com (2026-04-11)

Project: chromium/src  

Branch:  refs/branch-heads/7727  

Author:  Rob Pitkin [robpitkin@google.com](mailto:robpitkin@google.com)  

Link:    <https://chromium-review.googlesource.com/7750165>

[M147] [WebUSB] Add UMA for control transfer permission telemetry

---


Expand for full commit details
```
     
    Original change's description: 
    > [WebUSB] Add UMA for control transfer permission telemetry 
    > 
    > This CL adds comprehensive UMA telemetry to track the impact of the 
    > WebUSB control transfer security fix (b:489711638). 
    > 
    > Two distinct metrics are introduced: 
    > 
    > 1. WebUsb.ControlTransferPermissionOutcome: An enumerated histogram 
    > tracking the high-level result of every permission check (Allowed, 
    > Blocked, Interface Not Found, or No Configuration). This provides the 
    > denominator needed to calculate real-world breakage ratios. 
    > 
    > 2. WebUsb.ControlTransferBlocked.{Direction}.{Type}: A tokenized sparse 
    > histogram that records the specific USB interface class code being 
    > blocked. This allows for granular root-cause analysis, helping 
    > distinguish between malicious tunneling attempts and legitimate, 
    > non-standard device routing that may have been caught by the new 
    > restrictions. 
    > 
    > The HasControlTransferPermission method signature was updated to include 
    > the transfer direction to support the tokenized variants. 
    > 
    > Bug: 489711638 
    > Test: Verified with chrome://histograms using local test page. 
    > Change-Id: Ibf7d49eb6b06b77e0c105b722fa03e55c6833a37 
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7685741 
    > Reviewed-by: Reilly Grant <reillyg@chromium.org> 
    > Reviewed-by: Alvin Ji <alvinji@chromium.org> 
    > Commit-Queue: Rob Pitkin <robpitkin@chromium.org> 
    > Cr-Commit-Position: refs/heads/main@{#1604293} 
     
    (cherry picked from commit e30b44e5d05722b43747fd04dcb8c6b52c5b56bc) 
     
    Bug: 500520293,489711638 
    Change-Id: Ibf7d49eb6b06b77e0c105b722fa03e55c6833a37 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7750165 
    Reviewed-by: Matt Reynolds <mattreynolds@chromium.org> 
    Commit-Queue: Alvin Ji <alvinji@chromium.org> 
    Reviewed-by: Alvin Ji <alvinji@chromium.org> 
    Auto-Submit: Chrome Cherry Picker <chrome-cherry-picker@chops-service-accounts.iam.gserviceaccount.com> 
    Cr-Commit-Position: refs/branch-heads/7727@{#2637} 
    Cr-Branched-From: ce01102937348db7b88c8a4257ee4b3ac702eb1a-refs/heads/main@{#1596535}

```

---

Files:

- M `services/device/usb/mojo/device_impl.cc`
- M `services/device/usb/mojo/device_impl.h`
- M `tools/metrics/histograms/enums.xml`
- M `tools/metrics/histograms/metadata/others/histograms.xml`

---

Hash: [1253fda8a5aca8f9a8ce69eddddb2eae68904644](https://chromiumdash.appspot.com/commit/1253fda8a5aca8f9a8ce69eddddb2eae68904644)  

Date: Sat Apr 11 00:09:59 2026


---

### pe...@google.com (2026-04-15)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2026-04-15)

1. https://chromium-review.git.corp.google.com/c/chromium/src/+/7760942 and https://chromium-review.git.corp.google.com/c/chromium/src/+/7762723
2. Low - There was no conflict.
3. 146 and 147
4. Yes, the CL that introduced this bug was merged in 2018.

### dx...@google.com (2026-04-30)

Project: chromium/src  

Branch:  refs/branch-heads/7559  

Author:  Alvin Ji [alvinji@chromium.org](mailto:alvinji@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7760942>

[M144-LTS] WebUSB: Strengthen control transfer protection for protected classes

---


Expand for full commit details
```
     
    Strengthens control transfer permissions to block requests targeting 
    protected interface classes like HID or Mass Storage. Requests are now 
    scrutinized for protected interfaces via the wIndex field regardless of 
    recipient. Standard requests for device-level management remain allowed. 
    This behavior is gated by the kWebUsbProtectedClassControlTransferBlock 
    feature flag. 
     
    (cherry picked from commit 89b42d2d3326ebad6e0494009d5d92f2dbaf12ef) 
     
    Bug: 489711638 
    Change-Id: Ic69c88f81e2a10abcaa80832b330d3789493f3b2 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7677820 
    Reviewed-by: Reilly Grant <reillyg@chromium.org> 
    Commit-Queue: Alvin Ji <alvinji@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1601756} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7760942 
    Commit-Queue: Gyuyoung Kim (xWF) <qkim@google.com> 
    Reviewed-by: Achuith Bhandarkar <achuith@chromium.org> 
    Reviewed-by: Matt Reynolds <mattreynolds@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7559@{#4834} 
    Cr-Branched-From: 223dfbac1c7542a06b422390d954afe5b560b607-refs/heads/main@{#1552494}

```

---

Files:

- M `services/device/public/cpp/device_features.cc`
- M `services/device/public/cpp/device_features.h`
- M `services/device/usb/mojo/BUILD.gn`
- M `services/device/usb/mojo/device_impl.cc`
- M `services/device/usb/mojo/device_impl.h`
- M `services/device/usb/mojo/device_impl_unittest.cc`

---

Hash: [1407a8a377d026c2b36b9616147d2dc24ca3feca](https://chromiumdash.appspot.com/commit/1407a8a377d026c2b36b9616147d2dc24ca3feca)  

Date: Thu Apr 30 03:13:35 2026


---

### ch...@google.com (2026-07-07)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/489711638)*
