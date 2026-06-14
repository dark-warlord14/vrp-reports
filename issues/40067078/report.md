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

Device chooser dialogs, such as Bluetooth, USB, Serial, HID, and others, do not show the requesting origin correctly for web pages with non-standard URLs [1], such as `about:blank`, `javascript:`, `blob:`, and `data:` URLs. There may be other unidentified schemes that also trigger this behavior.

[1] `SchemeRegistry.standard_schemes` does not include `about`, `data`, `blob`, or `javascript` schemes:  

<https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:components/url_formatter/elide_url.cc;l=334;drc=255b4e7036f1326f2219bd547d3d6dcf76064870>

For example, a tab/popup opened with URL `about:blank` will result in the dialog showing `about:blank` instead of the committed origin's hostname (e.g. `example.com` if that hostname is the opener). In comparison, other security-sensitive UI such as other permission prompts, JS dialogs, etc. use the committed origin instead of the committed URL.

For some URLs, the URL is shown as-is and elided starting from the end of the URL (`...[end of attacker-controlled URL string] wants to connect`).  

For other URLs, the URL is completely ommitted without showing an elipsis (`wants to connect`).

In cases where the URL is shown, the URL can be manipulated by the attacker in a myriad of ways to show arbitrary strings, including spoofing hostnames/origins.

In all identified scenarios, the page can have arbitrary attacker content. This makes it easier to provide instructions to the user.

Opening window with some blocked URLs, such as `javascript:` URLs or `data:` URLs, results in no origin shown and no ellipsis (`wants to connect`).

### Bisect

Bisect confirms commit 89707e4be0e98af60d6a862282a045496c1a9422 from March 27, 2023 changed device chooser dialogs to use the UrlIdentity logic with incorrect parameters (URL instead of origin).  

Commit landed in 114.0.5680.0 Canary, 114.0.5735.45 Stable per <https://chromiumdash.appspot.com/commit/89707e4be0e98af60d6a862282a045496c1a9422>

Prior to that commit, the dialogs used the RFH's `LastCommittedOrigin()` formatted by `url_formatter::FormatOriginForSecurityDisplay()`:  

<https://chromium.googlesource.com/chromium/src/+/edc1087324b8131a57f62b1418fadc8076d4da0b/components/permissions/chooser_title_util.cc>

### Root cause

The issue occurs because `CreateChooserTitle()` [2] passes the RFH's `LastCommittedURL()` value [2a] to UrlIdentity::CreateFromUrl() [2b]. Unfortunately, `LastCommittedURL()` returns the attacker-controlled URL in the identified scenarios.

[2] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/chooser_controller/title_util.cc;l=40;drc=89707e4be0e98af60d6a862282a045496c1a9422>

```
std::u16string CreateChooserTitle(content::RenderFrameHost\* render_frame_host,  
                                  int title_string_id) {  
  if (!render_frame_host) {  
    return u"";  
  }  
  // Ensure the permission request is attributed to the main frame.  
  render_frame_host = render_frame_host->GetMainFrame();  
  
  const GURL& url = render_frame_host->GetLastCommittedURL();          // <----- [2a] Gets committed URL instead of committed origin  
  Profile\* profile =  
      Profile::FromBrowserContext(render_frame_host->GetBrowserContext());  
  
  UrlIdentity identity = UrlIdentity::CreateFromUrl(  
      profile, url, kUrlIdentityAllowedTypes, kUrlIdentityOptions);    // <----- [2b] Passes committed URL to UrlIdentity::CreateFromUrl()  
  
  return l10n_util::GetStringFUTF16(title_string_id, identity.name);  
}  

```

`UrlIdentity::CreateFromUrl()` calls `CreateDefaultUrlIdentityFromUrl()` which calls `url_formatter::FormatUrlForSecurityDisplay()` with `url_formatter::SchemeDisplay::OMIT_CRYPTOGRAPHIC` arg here:  

<https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/url_identity.cc;l=46;drc=c903d85cc58386b3a390c505e2b09f44b9a0a4ab>

`url_formatter:FormatUrlForSecurityDisplay()` probably calls `url_formatter::FormatUrl()` since `about:blank` probably fails the `url.IsStandard()` (`GURL::IsStandard()`) condition:  

<https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:components/url_formatter/elide_url.cc;l=334;drc=255b4e7036f1326f2219bd547d3d6dcf76064870>

Side note: `GURL::IsStandard()` eventually checks against `SchemeRegistry.standard_schemes` which does not include `about`, `data`, `blob`, or `javascript` schemes:  

<https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:components/url_formatter/elide_url.cc;l=334;drc=255b4e7036f1326f2219bd547d3d6dcf76064870>

### Patch

To fix, the call to `GetLastCommittedURL()` [2a] should be replaced with `GetLastCommittedOrigin()`, and get a URL based on the origin using `origin.GetURL()` to pass to `UrlIdentity::CreateFromUrl()`. This is the approach used in other safe call sites, such as `DisplayMediaAccessHandler::GetApplicationTitle()`:  

<https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:chrome/browser/media/webrtc/display_media_access_handler.cc;l=63;drc=255b4e7036f1326f2219bd547d3d6dcf76064870>

I've uploaded a CL to fix this, although I have not yet verified the patch's behavior since I don't have a build environment immediately available.

<https://chromium-review.googlesource.com/c/chromium/src/+/4672069>

### All dialogs that use `CreateChooserTitle()`

The following dialogs use `CreateChooserTitle()` and are almost certainly impacted by this bug. This list is based on source.chromium.org references.

ChromeBluetoothDelegateImplClient::ShowBluetoothScanningPrompt():  

<https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:chrome/browser/bluetooth/chrome_bluetooth_delegate_impl_client.cc;l=71;drc=255b4e7036f1326f2219bd547d3d6dcf76064870>

ChromeBluetoothChooserController::ChromeBluetoothChooserController():  

<https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:chrome/browser/ui/bluetooth/chrome_bluetooth_chooser_controller.cc;l=56;drc=255b4e7036f1326f2219bd547d3d6dcf76064870>

UsbChooserController::UsbChooserController():  

<https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:chrome/browser/usb/usb_chooser_controller.cc;l=95;drc=255b4e7036f1326f2219bd547d3d6dcf76064870>

HidChooserController::HidChooserController():  

<https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:chrome/browser/ui/hid/hid_chooser_controller.cc;l=87;drc=255b4e7036f1326f2219bd547d3d6dcf76064870>

SerialChooserController::SerialChooserController():  

<https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:chrome/browser/ui/serial/serial_chooser_controller.cc;l=75-76;drc=255b4e7036f1326f2219bd547d3d6dcf76064870>

PrivateNetworkDeviceChooserController::PrivateNetworkDeviceChooserController():  

<https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:chrome/browser/private_network_access/private_network_device_chooser_controller.cc;l=36-37;drc=255b4e7036f1326f2219bd547d3d6dcf76064870>

DevicePermissionsDialogController::DevicePermissionsDialogController():  

<https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:chrome/browser/extensions/device_permissions_dialog_controller.cc;l=16-19;drc=255b4e7036f1326f2219bd547d3d6dcf76064870>

**VERSION**  

Chrome Version: (All channels) 114.0.5735.199 Stable, 115.0.5790.75 Beta, 116.0.5845.14 Dev, 117.0.5876.0 Canary  

Operating System: Windows 10 Version 22H2 (Build 19045.3086)

**REPRODUCTION CASE**

### Full PoCs

I'll provide full hosted PoCs and video recordings by next week.

### Minimal examples using USB device chooser

Note: All these PoCs should work for other types of device choosers, such as Bluetooth, HID, Serial, etc.

Repro steps:

1. Open any page (such as <https://example.com> )
2. Open DevTools Console
3. Either enable "Treat code evaluation as user action" in Console options, or click on the page within 5 seconds before executing `window.open()` calls.
4. Run a sample payload below
5. Click on opened page to open device chooser  
   
   (Repeat above for each payload.)

`javascript:` URL (`wants to connect`):  

window.open('javascript:window.addEventListener("click", () => { navigator.usb.requestDevice({filters:[]}); });"<h1>Click anywhere</h1>"');

`data:` URL (`wants to connect`):  

var newWin = window.open('data:text/html,hello');  

newWin.document.open(); newWin.document.write('<h1>Click anywhere</h1>'); newWin.document.close();  

newWin.addEventListener('click', () => { newWin.navigator.usb.requestDevice({filters:[]}); });

`about:blank#...` URL (`...[string] wants to connect`):

\* Spoof origin (`...example.com wants to connect`):  

var newWin = window.open('about:blank#%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20example.com');  

newWin.document.open(); newWin.document.write('<title>Hello</title><h1>Click anywhere</h1>'); newWin.document.close();  

newWin.addEventListener('click', () => { newWin.navigator.usb.requestDevice({filters:[]}); });

\* Show arbitrary text (`...message from Chrome: example.com wants to connect`):  

var newWin = window.open('about:blank#%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20Please select device. Chrome');  

newWin.document.open(); newWin.document.write('<title>Hello</title><h1>Click anywhere</h1>'); newWin.document.close();  

newWin.addEventListener('click', () => { newWin.navigator.usb.requestDevice({filters:[]}); });

\* Show no origin (`...wants to connect`):  

var newWin = window.open('about:blank#%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20');  

newWin.document.open(); newWin.document.write('<title>Hello</title><h1>Click anywhere</h1>'); newWin.document.close();  

newWin.addEventListener('click', () => { newWin.navigator.usb.requestDevice({filters:[]}); });

`blob:` URL `...[string] wants to connect`):  

Although less useful for an attacker, this can also be reproduced with blob URLs.  

e.g. On page `blob:https://example.com/b1775f8c-80b5-4f16-b75e-817a5e15e79e`, dialog will show `.../b1775f8c-80b5-4f16-b75e-817a5e15e79e`. (Blob URLs can also have hash added, so all the `about:blank#...` examples above also work with these URLs.)

var blob = new Blob(['<script>window.addEventListener("click", () => { navigator.usb.requestDevice({filters:[]});; });</script><title>Hello</title><h1>Click anywhere</h1>'], {type: 'text/html'});  

window.open(URL.createObjectURL(blob));

**CREDIT INFORMATION**  

Reporter credit: Alesandro Ortiz <https://AlesandroOrtiz.com>

## Attachments

- [device-chooser-basic_usb_javascript.png](attachments/device-chooser-basic_usb_javascript.png) (image/png, 29.5 KB)
- [device-chooser-basic_usb_about-blank-origin-spoof.png](attachments/device-chooser-basic_usb_about-blank-origin-spoof.png) (image/png, 29.6 KB)

## Timeline

### [Deleted User] (2023-07-08)

[Empty comment from Monorail migration]

### al...@alesandroortiz.com (2023-07-08)

[Comment Deleted]

### al...@alesandroortiz.com (2023-07-08)

Additional note regarding opaque origins, which might be a separate vulnerability.

Most device choosers are blocked from opaque origins (enforced by renderer + browser) after https://crbug.com/chromium/1375133 was fixed. However, I'm not sure if all the uses of `GetChooserTitle()` identified above are protected against opaque origins, so it's possible some of them are still vulnerable to https://crbug.com/chromium/1375133 after the issue reported in this crbug is fixed.

### al...@alesandroortiz.com (2023-07-08)

Couple of screenshots to help with triage until I create full PoCs.

* device-chooser-basic_usb_javascript.png - Screenshot of `javascript:` URL PoC above.
* device-chooser-basic_usb_about-blank-origin-spoof.png - Screenshot of `about:blank#...` spoof origin PoC above.

### al...@alesandroortiz.com (2023-07-08)

Added author and reviewers of original CL [1] as reviewers to proposed fix CL [2].

Triager: Please cc reviewers in [2] if they don't already have access to this crbug.

[1] https://chromium-review.googlesource.com/c/chromium/src/+/4346716
[2] https://chromium-review.googlesource.com/c/chromium/src/+/4672069 

### aw...@google.com (2023-07-10)

[Empty comment from Monorail migration]

### re...@chromium.org (2023-07-10)

It looks like this might be a duplicate of https://crbug.com/chromium/1459281.

[Monorail components: Blink>Bluetooth Blink>HID Blink>Serial Blink>USB]

### re...@chromium.org (2023-07-10)

[Empty comment from Monorail migration]

### al...@alesandroortiz.com (2023-07-10)

Can I get cc'd into the original bug if possible? Thanks.

If we end up using the current CL, I can update the commit message to mention both crbug IDs.

### al...@alesandroortiz.com (2023-07-12)

Thanks for cc'ing me into original bug. Definitely seems like this report is a duplicate, although this report does demonstrate additional scenarios, such as showing another origin or showing no origin (vs. original report only showing `about:blank`). This report also shows different ways to reach this state and provides bisect + root cause analysis + patch. Not sure if that's sufficient for even a small reward.

Since this is a duplicate, I won't provide full PoCs unless it will result in a reward or increase reward.

There's also an additional scenario that leads to no origin being shown in the dialog:

204 response (`wants to connect`):
var newWin = window.open('https://google.com/generate_204'); // The URL here doesn't matter as long as it returns 204, can be cross-origin to opener
newWin.document.open(); newWin.document.write('<title>Hello</title><h1>Click anywhere</h1>'); newWin.document.close();
newWin.addEventListener('click', () => { newWin.navigator.usb.requestDevice({filters:[]}); });

### gi...@appspot.gserviceaccount.com (2023-07-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/5fb01bbdacd8fd2c2d3a59885092fdf69c40c84e

commit 5fb01bbdacd8fd2c2d3a59885092fdf69c40c84e
Author: Alesandro Ortiz <alesandro@alesandroortiz.com>
Date: Wed Jul 19 22:40:10 2023

Use committed origin instead of committed URL in device chooser dialogs

Bug: 1463149,1459281
Change-Id: Ia1d81b82b654d22d44215ecde73d8d24d27ce983
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4672069
Reviewed-by: Reilly Grant <reillyg@chromium.org>
Commit-Queue: Zelin Liu <zelin@chromium.org>
Commit-Queue: Reilly Grant <reillyg@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1172637}

[modify] https://crrev.com/5fb01bbdacd8fd2c2d3a59885092fdf69c40c84e/chrome/browser/chooser_controller/title_util_browsertest.cc
[modify] https://crrev.com/5fb01bbdacd8fd2c2d3a59885092fdf69c40c84e/chrome/browser/chooser_controller/title_util.cc


### al...@alesandroortiz.com (2023-07-19)

Will verify patch once it's on Canary. Thanks for review + merge, reilly@ and zelin@!

### al...@alesandroortiz.com (2023-07-21)

Verified as fixed on 117.0.5901.0 Canary on Windows 10 using minimal PoCs in https://crbug.com/chromium/1463149#c0.

### am...@chromium.org (2023-08-02)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-08-02)

Congratulations, Alesandro. The VRP Panel has decided to award you a $1,000 patch bonus for your patch submitted here, but was landed in respect to the previously submitted report for this issue. Thank you for your efforts and writing and submitting this patch! 

### al...@alesandroortiz.com (2023-08-02)

Thanks for the patch bonus! Appreciate it given the unusual situation.

### am...@chromium.org (2023-08-03)

Thank you for submitting and testing the patch even though you knew your report was a duplicate! We greatly appreciate the follow through here. 

### am...@google.com (2023-08-05)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-11-01)

This issue was migrated from crbug.com/chromium/1463149?no_tracker_redirect=1

[Multiple monorail components: Blink>Bluetooth, Blink>HID, Blink>Serial, Blink>USB]
[Monorail mergedinto: crbug.com/chromium/1459281]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40067078)*
