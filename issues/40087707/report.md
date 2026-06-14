# Security: Mismatched Origin Display in WebUSB and WebBluetooth Permissions Dialogs

| Field | Value |
|-------|-------|
| **Issue ID** | [40087707](https://issues.chromium.org/issues/40087707) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Blink>Bluetooth, Blink>USB, UI>Browser>Permissions>Prompts |
| **Platforms** | Linux, Windows |
| **Reporter** | [Deleted User] |
| **Assignee** | re...@chromium.org |
| **Created** | 2017-05-17 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

A race condition exists allowing a malicious origin to display a WebUSB permission request in context of an arbitrary origin such as for example <https://google.com>.

Successful exploitation requires chrome://flags/#enable-experimental-web-platform-features to be enabled.  

It also requires user interaction.  

The origin requesting permissions is displayed in the permissions box.

We still see this as security relevant because the permissions dialog is visually connected to the origin and for average users it will be hard to notice that the origin does not match the permissions request origin.

**VERSION**  

Chrome Version: 58.0.3029.110 (64-bit) stable  

Operating System: Windows 10 Build 14393.rs1\_release\_sec.170427-1353

**REPRODUCTION CASE**  

Attached are three files:

- webusb-perm-poc.html - reproduction showing the WebUSB permission dialog being displayed on <https://www.google.com>
- webusb-permission-ui-confusion-1.jpg: Malicous site with a link to google.com
- webusb-permission-ui-confusion-2.jpg: Popup being displayed on google.com, but the request is for a different origin

## Attachments

- [webusb-permission-ui-confusion-1.jpg](attachments/webusb-permission-ui-confusion-1.jpg) (image/jpeg, 101.5 KB)
- [webusb-permission-ui-confusion-2.jpg](attachments/webusb-permission-ui-confusion-2.jpg) (image/jpeg, 188.9 KB)
- [webusb-perm-poc.html](attachments/webusb-perm-poc.html) (text/plain, 456 B)
- [webbt-perm-poc.html](attachments/webbt-perm-poc.html) (text/plain, 508 B)
- [paired.png](attachments/paired.png) (image/png, 12.0 KB)
- [poc-webusb.html](attachments/poc-webusb.html) (text/plain, 438 B)
- [poc-webbt.html](attachments/poc-webbt.html) (text/plain, 485 B)

## Timeline

### [Deleted User] (2017-05-17)

Addition: The race condition is between the change of location (and origin) and the display of the permissions dialog. A location change should trigger the permissions dialog to disappear, but the dialog stays.

### [Deleted User] (2017-05-17)


The same trick works for web-bluetooth, please see the attached poc.

### el...@chromium.org (2017-05-17)

[Empty comment from Monorail migration]

[Monorail components: UI>Browser>Permissions>Prompts]

### pa...@chromium.org (2017-05-17)

reillyg: Can you please route this to a likely fixer? Thanks.

[Monorail components: Blink>Bluetooth Blink>USB]

### pa...@chromium.org (2017-05-17)

[Empty comment from Monorail migration]

### re...@chromium.org (2017-05-17)

This is a duplicate of https://crbug.com/chromium/624700 and is only reproducible on Windows. The cause is a bug in Views on Windows which causes the request to dismiss the dialog to be lost for an as yet unknown reason. Importantly, clicking "Connect" does not grant any permissions as the backend for the dialog has already been destroyed.

### [Deleted User] (2017-05-17)

I can also reproduce the bug on Linux using the PoC at on Linux Chromium version 58.0.3029.110 (64-bit).

Also he pairing request succeeds as can be seen when you click connect and repeat the PoC.

I tested using the PoC at: https://www.x41-dsec.de/034uwf/confuse-webusb-perms.html

Either this is not a duplicate but a different bug, or it affects also other platforms besides Windows.
I cannot see 624700 from this account so I can't really check.

### re...@chromium.org (2017-05-17)

ChromeBubbleManager is what should be closing these bubbles on navigation and other operations. I could not reproduce on Linux and macOS but that may mean that the Views issue is a race condition. I was able to reproduce on Chrome OS with Chrome 59.0.3071.47.

https://cs.chromium.org/chromium/src/chrome/browser/ui/chrome_bubble_manager.cc

### [Deleted User] (2017-05-17)

Yes, it might be that the BubbleManager created after the navigation occured, or that it's attached to a separate frame. On Linux here there is actually a slight delay of some ms between the dialog showing and the navigation to the other domain, so maybe it's the latter. But I'm not that deep into the Chrome source to really know.

### pa...@chromium.org (2017-05-17)

The attacker origin does actually seem to get to pair to the USB device in question. (See attached screenshot.)

Either this might not be an exact duplicate of https://crbug.com/chromium/624700, or that issue should be tracked as a vulnerability, perhaps.

### pa...@chromium.org (2017-05-17)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-08-24)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### fe...@gmail.com (2018-05-31)

Hey,

I was able to reproduce this issue on Windows 10 and Linux (see exact versions below). I slightly adjusted the PoC above and attached them as it seems to work more consistent for me. Since WebUSB is turned on by default by now this works without enabling the chrome://flags/#enable-experimental-web-platform-features flag. The PoC for WebBluetooth still require the flag to be enabled.

As this is probably a race condition this does not work every time. However, I was able to reproduce this issue every time I executed the exploit right after a restart (chrome://restart). If I granted permission to a device it works again if I navigate back. If I click cancel it did not work again. It might require a fast and stable internet connection and decent hardware (tested on i5 and i7 cores). It might also be dependent on more currently unknown factors.

I could also reproduce that if a user connects a device to the attacker's origin in this dialog it will be paired. Permissions are also persistent over restarting Chrome/ium. I have not been able to test if a promise after requesting the device gets executed but I think this is not possible. This would lower the severity a bit as a victim has to visit the attacker's site twice.

Attack Scenario:
An attacker might use this in a social engineering scenario. To make it even less obvious that permissions are requested for a different origin one could use similar domain names by either buying a new domain similar to the target one or by using e.g. a self-hosted github.io site and as target github.com. An attacker could simply write an email / message to the victim while impersonating the target domain, stating that he / she gets <insert incentive here> if the victim would visit a link and connect their smartphone or Yubikey to it. After a user granted permission to his / her smartphone or Yubikey the victim (probably) has to visit the site a second time. After the victim visits the attacker's site again an attacker could compromise a connected smartphone via adb ( https://labs.mwrinfosecurity.com/blog/webusb/ ) or compromise a Yubikey-like hardware token as shown by Markus Vervier and Michele Orrù at OffensiveCon ( https://www.offensivecon.org/speakers/2018/markus-and-michele.html ). Which hardware to compromise is only limited by the imagination and time of the attacker.


Successfully tested for the following versions:

Google Chrome	67.0.3396.62 (Official Build) (64-bit)
Revision	babbbb5b433370f9a7feeb9f98a57599ad1c4676-refs/branch-heads/3396@{#702}
OS	Linux
JavaScript	V8 6.7.288.42
User Agent	Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36
Command Line	/opt/google/chrome/google-chrome --flag-switches-begin --flag-switches-end
Executable Path	/opt/google/chrome/google-chrome

---

Chromium	67.0.3396.62 (Official Build) Arch Linux (64-bit)
Revision	babbbb5b433370f9a7feeb9f98a57599ad1c4676-refs/branch-heads/3396@{#702}
OS	Linux
JavaScript	V8 6.7.288.42
Flash	29.0.0.171 /usr/lib/PepperFlash/libpepflashplayer.so
User Agent	Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36
Command Line	/usr/lib/chromium/chromium --ppapi-flash-path=/usr/lib/PepperFlash/libpepflashplayer.so --ppapi-flash-version=29.0.0.171 --flag-switches-begin --disable-touch-adjustment --enable-devtools-experiments --enable-experimental-web-platform-features --enable-scroll-prediction --extension-content-verification=enforce --show-saved-copy=secondary --top-chrome-md=material-hybrid --touch-events=disabled --flag-switches-end
Executable Path	/usr/lib/chromium/chromium

---

Google Chrome	66.0.3359.181 (Offizieller Build) (64-Bit) (cohort: Stable)
Revision	a10b9cedb40738cb152f8148ddab4891df876959-refs/branch-heads/3359@{#828}
OS	Windows
JavaScript	V8 6.6.346.32
User Agent	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36
Command Line	"C:\Users\<redacted>\AppData\Local\Google\Chrome\Application\chrome.exe" --flag-switches-begin --flag-switches-end
Executable Path	C:\Users\<redacted>\AppData\Local\Google\Chrome\Application\chrome.exe


### re...@chromium.org (2018-05-31)

Thanks for the update. It definitely raises the severity if contrary to https://crbug.com/chromium/723503#c6 the permission is successfully granted. I will take another look at this.

### [Deleted User] (2018-05-31)

Hi, just to note in https://crbug.com/chromium/723503#c7 it was also stated that the permission is successfully granted, I was of the impression the bug has been fixed, but maybe only the crash mentioned in the other ("duplicate") bug report?

### re...@chromium.org (2018-05-31)

[Empty comment from Monorail migration]

### do...@chromium.org (2018-05-31)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-06-01)

[Empty comment from Monorail migration]

### es...@chromium.org (2018-06-13)

Hey Reilly, did you have a chance to take another look at this?

### re...@chromium.org (2018-06-13)

I'm working on adding a browser_test to exercise this PoC. I can't reproduce the issue locally but I have a few theories.

### bu...@chromium.org (2018-06-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/2c6ce192cb3fb7bfbc3f3f862926dcb65c3891b4

commit 2c6ce192cb3fb7bfbc3f3f862926dcb65c3891b4
Author: Reilly Grant <reillyg@chromium.org>
Date: Sat Jun 23 22:41:47 2018

Ensure device choosers are closed on navigation

The requestDevice() IPCs can race with navigation. This change ensures
that choosers are closed on navigation and adds browser tests to
exercise this for Web Bluetooth and WebUSB.

Bug: 723503
Change-Id: I66760161220e17bd2be9309cca228d161fe76e9c
Reviewed-on: https://chromium-review.googlesource.com/1099961
Commit-Queue: Reilly Grant <reillyg@chromium.org>
Reviewed-by: Michael Wasserman <msw@chromium.org>
Reviewed-by: Jeffrey Yasskin <jyasskin@chromium.org>
Cr-Commit-Position: refs/heads/master@{#569900}
[modify] https://crrev.com/2c6ce192cb3fb7bfbc3f3f862926dcb65c3891b4/chrome/browser/ui/bluetooth/bluetooth_chooser_desktop.cc
[modify] https://crrev.com/2c6ce192cb3fb7bfbc3f3f862926dcb65c3891b4/chrome/browser/ui/bluetooth/bluetooth_chooser_desktop.h
[modify] https://crrev.com/2c6ce192cb3fb7bfbc3f3f862926dcb65c3891b4/chrome/browser/ui/browser.cc
[modify] https://crrev.com/2c6ce192cb3fb7bfbc3f3f862926dcb65c3891b4/chrome/browser/usb/usb_browsertest.cc
[modify] https://crrev.com/2c6ce192cb3fb7bfbc3f3f862926dcb65c3891b4/chrome/browser/usb/usb_tab_helper.cc
[modify] https://crrev.com/2c6ce192cb3fb7bfbc3f3f862926dcb65c3891b4/chrome/browser/usb/usb_tab_helper.h
[modify] https://crrev.com/2c6ce192cb3fb7bfbc3f3f862926dcb65c3891b4/chrome/browser/web_bluetooth_browsertest.cc
[modify] https://crrev.com/2c6ce192cb3fb7bfbc3f3f862926dcb65c3891b4/components/bubble/bubble_manager.cc
[modify] https://crrev.com/2c6ce192cb3fb7bfbc3f3f862926dcb65c3891b4/components/bubble/bubble_manager.h
[modify] https://crrev.com/2c6ce192cb3fb7bfbc3f3f862926dcb65c3891b4/content/browser/bluetooth/web_bluetooth_service_impl.cc


### sh...@chromium.org (2018-07-25)

[Empty comment from Monorail migration]

### me...@google.com (2018-07-27)

Reilly: Is there remaining work here? Can this be closed?

### re...@chromium.org (2018-07-27)

I think this can be closed. I had another patch which attempted to add additional browser_tests to make sure that we could always observe that the dialog was shown when it should be[1] but my methodology there was flawed and the tests were flaky. I would really appreciate it if Felix could try to reproduce this in their setup because I haven't been able to reproduce.

[1]: https://chromium-review.googlesource.com/c/chromium/src/+/1117577

### aw...@google.com (2018-07-28)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-28)

[Empty comment from Monorail migration]

### fe...@gmail.com (2018-07-30)

Hey Reilly,

Is your patch included in the 68 release? I just did a quick check and it still worked for me with the provided PoC.

This is the version I tested:

Chromium	68.0.3440.75 (Official Build) Arch Linux (64-bit)
Revision	cf598d63a4f1b9e7cd14f2a8433276b196e3e07d-refs/branch-heads/3440@{#738}
OS	        Linux

### re...@chromium.org (2018-07-30)

The fix should be in 69.0.3472.3 and later.

### sh...@chromium.org (2018-08-03)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-08-03)

This bug requires manual review: M69 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: amineer@(Android), kariahda@(iOS), cindyb@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### re...@chromium.org (2018-08-03)

The change above is already on the M-69 branch.

### aw...@chromium.org (2018-08-06)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@chromium.org (2018-08-06)

Thanks for the report, vervierx41@! The VRP panel decided to award $500 for this. A member of our finance team will be in touch to arrange payment. Also, how would you like to appear on the Chrome release notes?

### aw...@chromium.org (2018-08-06)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-08-07)

[Empty comment from Monorail migration]

### fe...@gmail.com (2018-08-07)

Hey Reilly,

I was not able to trigger the race condition on Chrome 69 with payloads that worked in Chrome 68. Seems fixed indeed.

Cheers,
Felix

### re...@chromium.org (2018-08-07)

Thank you for verifying.

### aw...@chromium.org (2018-08-16)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@chromium.org (2018-08-16)

[Empty comment from Monorail migration]

### aw...@google.com (2018-08-16)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-09-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-11-03)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2019-01-04)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-04)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-04)

This issue was migrated from crbug.com/chromium/723503?no_tracker_redirect=1

[Multiple monorail components: Blink>Bluetooth, Blink>USB, UI>Browser>Permissions>Prompts]
[Monorail mergedinto: crbug.com/chromium/624700]
[Monorail components added to Component Tags custom field.]

### dt...@google.com (2025-02-13)

Bulk update of issues accidentally marked as duplicate in issue tracker migration (b/325072672)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40087707)*
