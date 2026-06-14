# Security: WinUSB - multiple issues

| Field | Value |
|-------|-------|
| **Issue ID** | [40090681](https://issues.chromium.org/issues/40090681) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>USB |
| **Platforms** | Windows |
| **CVE IDs** | CVE-2018-6125 |
| **Reporter** | cn...@yubico.com |
| **Assignee** | re...@chromium.org |
| **Created** | 2018-03-05 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**

= Background

Please see the presentation from <https://www.offensivecon.org/speakers/2018/markus-and-michele.html> if you have a way to get access to it. We received a partial copy of their slide deck last week which mentioned only the CCID -> U2F issue as later publicized in <https://www.wired.com/story/chrome-yubikey-phishing-webusb/> We started testing everything related in earnest then, and have been in touch with individuals at google last week and over the weekend with our findings. This issue is meant to get the ball rolling on some critical fixes as quickly as possible.

It's certainly possible we made a mistake in our rapid testing. We will submit our test code tomorrow so you can evaluate and inform us if we missed something.

= Issues

This section outlines a few issues and some preliminary test results, starting with the ones we consider critical for the FIDO ecosystem.

1. Critical: On Windows 10/x64, Chrome's WinUSB implementation appears to allow the standard U2F HID interface to be claimed on all tokens we could find and test. Other platforms do not seem to allow this.

We successfully sent INIT data to the OUT endpoint and read a valid response from the IN endpoint through this interface on all tokens. While we have not mocked enough of a USB stack in javascript to ask for and receive a full U2F authentication, we feel it is extremely likely that this will work and would rather err on the side of notifying the Chrome team ASAP. This would obviously allow a website that tricks a user into allowing access to their token to override the AppID/RpID and ChannelID/TokenBinding MITM protections that the FIDO ecosystem relies on.

2. Critical: ChromeOS and Android consistently allow the CCID interface to be claimed by WebUSB. Other OSs are inconsistent, but we expect any Linux distribution where the /dev entries are user accessible and gnome-keyring, pcscd, and scdaemon are not running will allow this. Also, not all USB Smart Card readers are CCID, and thus blocking CCID may not fix this issue comprehensively.

2a) As the paper's authors noted, for USB authenticators where U2F is exposed over CCID, the same appid/channelid bypass as 1) above is possible. We have confirmed that the YubiKey NEO and the Feitian ePass FIDO K9 expose the U2F applet via AID a0000006472f as described by the \*NFC\* U2F spec. It is very likely that many NFC+USB tokens expose U2F over CCID because that's how it's specified over NFC, and the CCID interface is often shared with both interfaces SmartCard implementations.

2b) For PIV, GIDS, and OpenPGP Smart Cards, PINs could be locked out, cards could be permanently destroyed, signatures could be made with Card Authentication keys without user PIN, and PINs could be phished to allow using any key and bypassing the expected MITM protections of mutual TLS using such keys.

2c) For Java Cards with default or derived keys, applications could be installed/deleted, users could be locked out, etc.

3. Likely Critical (unconfirmed): Because U2F is specified via CCID for NFC tokens, any platform where a USB NFC reader can be claimed by WebUSB can also have the user place their standard NFC U2F token into the reader's field and bypass the appid/channelid protections as in 1) and 2) above.

We haven't finished testing this yet due to lack of hardware at home over the weekend, but expect more comments/findings to follow this week as we test. Issues 2a, 2b, and 2c above would all be applicable over NFC.

4. Serious: Most users who allow their USB devices to be accessed by WebUSB applications likely do not know that many devices could be deliberately ransomed or accidentally permanently damaged by those applications.

Many non-security-oriented USB devices have insecure firmware update mechanisms, or at least consider the USB host to be as far as the trust boundary goes. We were able to exchange messages with a $6,000 oscilloscope and expensive USB speakers using WebUSB but didn't go very far to avoid breaking them. Users with USB equipment like audio or visual interfaces, synthesizers, or digitizers would have no idea their devices could be bricked just by clicking "approve" when their intent was to simply \*use\* their device with a site. It even appears that webDFU was considered as part of the development of WebUSB (<https://github.com/devanlai/webdfu> is linked from the repo) but we believe that non-technical users will not understand the implications of webDFU from malicious or compromised sites.

= Summary

While it is consistent with the community specification, we believe the root cause of the issues above is that Chrome's WebUSB implementation seems to rely only on underlying operating system behavior and perfect user knowledge to control which USB devices are made available to which web sites. Because the underlying operating system behavior is inconsistent across OSs and even distributions, and because users are rarely equipped to understand the full implications of allowing a website direct USB access to a device, this combination sets the stage for a myriad of potential issues.

We understand and laud the goal of getting certain potentially dubious software drivers out of the kernel or other privileged processes and into a well tested origin-bound sandbox in user space, but there are other serious security considerations which should be contemplated as part of the WebUSB threat model. We were unable to find a comprehensive public threat model for WebUSB on its W3C Incubator Community Group page other than the very brief Security and Privacy section of the standard at <https://wicg.github.io/webusb/#security-and-privacy> which considers two broad cases then appears to say user consent plus secure contexts are all that is needed. There is also a closed and somewhat wild security issue at <https://github.com/WICG/webusb/issues/50> but no conclusions appear to be drawn there. Please let us know if we have missed something.

While all of this is being considered, we would like all of our devices (separate ticket to follow) to be blacklisted in Chrome's WebUSB implementation and look forward to your feedback.

**VERSION**  

Chrome Version: 64.0.3282.186  

Operating System: Microsoft Windows [Version 10.0.16299.248] (x64) et. al.

**REPRODUCTION CASE**

We have a (protected) appspot site up to demonstrate and will attach code to this bug as soon as we can.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**

N/A

## Timeline

### el...@chromium.org (2018-03-05)

[Empty comment from Monorail migration]

[Monorail components: Blink>USB]

### ke...@chromium.org (2018-03-05)

Thanks for submitting this. Assigning for further triage. I suspect more people should be cc'd here but I don't know who off-hand.

### ke...@chromium.org (2018-03-05)

[Empty comment from Monorail migration]

### re...@chromium.org (2018-03-05)

1) Disabling libusb's HID backend (which attempts, only on Windows, to make HID devices look like USB devices) is being done to resolve https://crbug.com/chromium/818472. https://crbug.com/chromium/818081 tracks then also adding an explicit block list for the HID (and other) device classes so that issues like this can't sneak in.

2) A resolution for https://crbug.com/chromium/818081 could also include blocking the CCID interface class.

3) NFC doesn't have a device class. Readers I have seen appear to be serial devices with a USB interface on top of that. It is unclear at this point the best way to block access to NFC readers if we wished to.

### ag...@chromium.org (2018-03-05)

[Empty comment from Monorail migration]

### aw...@google.com (2018-03-05)

[Empty comment from Monorail migration]

### ag...@chromium.org (2018-03-05)

[Empty comment from Monorail migration]

### aw...@google.com (2018-03-05)

Tracking for 66 at this stage. Will consider a 65 merge once any code changes land.

### go...@chromium.org (2018-03-05)

[Empty comment from Monorail migration]

### cn...@yubico.com (2018-03-06)

Re: https://crbug.com/chromium/1) above, we successfully did a U2F register and authenticate today with arbitrary channelid/rpid fields as we expected would work after claiming the HID U2F interface. Please let us know if you need additional information.

### bu...@chromium.org (2018-03-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/ac149a8d4371c0e01e0934fdd57b09e86f96b5b9

commit ac149a8d4371c0e01e0934fdd57b09e86f96b5b9
Author: Reilly Grant <reillyg@chromium.org>
Date: Wed Mar 07 01:32:04 2018

Remove libusb-Windows support for HID devices

This patch removes the Windows-specific support in libusb that provided
a translation between the WinUSB API and the HID API. Applications
currently depending on this using the chrome.usb API should switch to
using the chrome.hid API.

Bug: 818592
Change-Id: I82ee6ccdcbccc21d2910dc62845c7785e78b64f6
Reviewed-on: https://chromium-review.googlesource.com/951635
Reviewed-by: Ken Rockot <rockot@chromium.org>
Commit-Queue: Reilly Grant <reillyg@chromium.org>
Cr-Commit-Position: refs/heads/master@{#541265}
[modify] https://crrev.com/ac149a8d4371c0e01e0934fdd57b09e86f96b5b9/third_party/libusb/src/libusb/os/windows_usb.c
[modify] https://crrev.com/ac149a8d4371c0e01e0934fdd57b09e86f96b5b9/third_party/libusb/src/libusb/os/windows_usb.h


### cn...@yubico.com (2018-03-07)

Regarding https://crbug.com/chromium/3) above:

We found that on macOS and on Windows 10, CCID compliant NFC readers can be claimed occasionally but only very very unreliably. We think it is likely a race condition with the system CCID subsystems, but currently have no data to support that theory.

We also found that an extremely common and inexpensive NFC reader we have, the Identive SCL3711, uses a vendor specific (0xff) class/subclass/protocol on its usb interface and thus can be claimed on windows and macos. This device is based on the NXP pn531/pn532 chipset which is very common and is used in many inexpensive readers. Blocking all HID and CCID class devices wouldn't prevent the issues listed in 2a, 2b, and 2c on readers like this one.

We will test CCID and non CCID USB NFC readers on Linux and ChromeOS tomorrow.

### re...@chromium.org (2018-03-08)

[Empty comment from Monorail migration]

### re...@chromium.org (2018-03-08)

[Empty comment from Monorail migration]

### re...@chromium.org (2018-03-08)

Requesting merge of ac149a8d4371c0e01e0934fdd57b09e86f96b5b9 to M-66.

### go...@chromium.org (2018-03-09)

Is this need a merge to M65? If yes, pls request a merge to M65. 
awhalley@ (Security TPM) for merge review.

### re...@chromium.org (2018-03-09)

The patch above is large. I would like to see it merged to M-66 and given a little more time to surface issues before releasing in M-65. Can you give me a sense for what the timeline is for M-65 respins?

### aw...@google.com (2018-03-09)

Approving merge to m66 per chat with govind@ and reilyg@

### bu...@chromium.org (2018-03-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/20aaf51d748440ee4440eea1981abf428be7d0e1

commit 20aaf51d748440ee4440eea1981abf428be7d0e1
Author: Reilly Grant <reillyg@chromium.org>
Date: Fri Mar 09 02:04:22 2018

[M-66] Remove libusb-Windows support for HID devices

This patch removes the Windows-specific support in libusb that provided
a translation between the WinUSB API and the HID API. Applications
currently depending on this using the chrome.usb API should switch to
using the chrome.hid API.

Bug: 818592
Change-Id: I82ee6ccdcbccc21d2910dc62845c7785e78b64f6
Reviewed-on: https://chromium-review.googlesource.com/951635
Reviewed-by: Ken Rockot <rockot@chromium.org>
Commit-Queue: Reilly Grant <reillyg@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#541265}(cherry picked from commit ac149a8d4371c0e01e0934fdd57b09e86f96b5b9)
Reviewed-on: https://chromium-review.googlesource.com/956765
Reviewed-by: Reilly Grant <reillyg@chromium.org>
Cr-Commit-Position: refs/branch-heads/3359@{#125}
Cr-Branched-From: 66afc5e5d10127546cc4b98b9117aff588b5e66b-refs/heads/master@{#540276}
[modify] https://crrev.com/20aaf51d748440ee4440eea1981abf428be7d0e1/third_party/libusb/src/libusb/os/windows_usb.c
[modify] https://crrev.com/20aaf51d748440ee4440eea1981abf428be7d0e1/third_party/libusb/src/libusb/os/windows_usb.h


### re...@chromium.org (2018-03-09)

I will be tracking the stability of this change and requesting merge to M-65 once it is proven out in the next dev or beta release. Updating milestone to reflect that.

### sh...@chromium.org (2018-03-09)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-03-10)

[Empty comment from Monorail migration]

### re...@chromium.org (2018-03-12)

Stability looks good on 66.0.3359.22.

### aw...@google.com (2018-03-12)

govind - good for 65

### go...@chromium.org (2018-03-12)

Approving merge to M65 branch 3325 based on https://crbug.com/chromium/818592#c24 and per offline group chat with reillyg@ & awhalley@. 

### go...@chromium.org (2018-03-12)

Pls request a merge to M66 also if needed. Thank you.

### bu...@chromium.org (2018-03-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/fc27079ded1fe584047cd0830c3d95110a1fb6aa

commit fc27079ded1fe584047cd0830c3d95110a1fb6aa
Author: Reilly Grant <reillyg@chromium.org>
Date: Mon Mar 12 17:56:20 2018

[M-65] Remove libusb-Windows support for HID devices

This patch removes the Windows-specific support in libusb that provided
a translation between the WinUSB API and the HID API. Applications
currently depending on this using the chrome.usb API should switch to
using the chrome.hid API.

Bug: 818592
Change-Id: I82ee6ccdcbccc21d2910dc62845c7785e78b64f6
Reviewed-on: https://chromium-review.googlesource.com/951635
Reviewed-by: Ken Rockot <rockot@chromium.org>
Commit-Queue: Reilly Grant <reillyg@chromium.org>
Cr-Original-Original-Commit-Position: refs/heads/master@{#541265}(cherry picked from commit ac149a8d4371c0e01e0934fdd57b09e86f96b5b9)
Reviewed-on: https://chromium-review.googlesource.com/956765
Reviewed-by: Reilly Grant <reillyg@chromium.org>
Cr-Original-Commit-Position: refs/branch-heads/3359@{#125}
Cr-Original-Branched-From: 66afc5e5d10127546cc4b98b9117aff588b5e66b-refs/heads/master@{#540276}(cherry picked from commit 20aaf51d748440ee4440eea1981abf428be7d0e1)
Reviewed-on: https://chromium-review.googlesource.com/959281
Cr-Commit-Position: refs/branch-heads/3325@{#692}
Cr-Branched-From: bc084a8b5afa3744a74927344e304c02ae54189f-refs/heads/master@{#530369}
[modify] https://crrev.com/fc27079ded1fe584047cd0830c3d95110a1fb6aa/third_party/libusb/src/libusb/os/windows_usb.c
[modify] https://crrev.com/fc27079ded1fe584047cd0830c3d95110a1fb6aa/third_party/libusb/src/libusb/os/windows_usb.h


### aw...@google.com (2018-03-13)

[Empty comment from Monorail migration]

### aw...@google.com (2018-03-22)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-16)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-04-16)

Many thanks for the report! The Chrome VRP decided to award $5,000 for this report. We'll be in touch to arrange payment.

### aw...@google.com (2018-04-16)

[Empty comment from Monorail migration]

### aw...@google.com (2018-04-16)

Many thanks for your decision to donate this reward. We'll double the amount to $10,000 :-)

### aw...@google.com (2018-04-17)

[Empty comment from Monorail migration]

### aw...@google.com (2018-04-17)

[Empty comment from Monorail migration]

### aw...@google.com (2018-05-03)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-05-29)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-05-29)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-06-11)

Planning on making this public on 2018-06-13, setting next action date to remind us.

### aw...@chromium.org (2018-06-13)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-06-13)

[Empty comment from Monorail migration]

### ad...@google.com (2019-12-03)

Removing "CVE_description-missing" from pre-2019 issue because we're not going to submit any such missing descriptions.

### ad...@google.com (2021-11-02)

[Empty comment from Monorail migration]

### pg...@google.com (2022-11-04)

Looks like the description was submitted: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2018-6125
removing the label CVE_description-missing

### pg...@google.com (2022-11-04)

[Empty comment from Monorail migration]

### is...@google.com (2022-11-04)

This issue was migrated from crbug.com/chromium/818592?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail blocking: crbug.com/chromium/813280]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40090681)*
