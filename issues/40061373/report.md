# Security: Android: Bluetooth and USB chooser dialogs do not use top-level origin with permission delegation

| Field | Value |
|-------|-------|
| **Issue ID** | [40061373](https://issues.chromium.org/issues/40061373) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Bluetooth, Blink>USB, UI>Browser>Permissions>Prompts |
| **Platforms** | Android |
| **Reporter** | al...@alesandroortiz.com |
| **Assignee** | ch...@chromium.org |
| **Created** | 2022-10-16 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

This report describes same behavior affecting two different dialogs, but filing together since they're closely related.

In Android, the Bluetooth and USB chooser dialogs use a cross-origin frame's origin [1] instead of the top-level page's origin. Per <https://crbug.com/chromium/824985> and <https://crbug.com/chromium/1280233>, these APIs use permission delegation and should always show the top-level page's origin. These APIs can only be used by cross-origin iframes when delegated by the top-level frame.

For the USB API, the top-level origin also gains USB access to the device despite the dialog showing the iframe's origin, so this is also an origin spoof exactly like <https://crbug.com/chromium/1280233>.  

For the Bluetooth API, I'm not sure if it's possible for a top-level frame to access a paired device without showing the dialog (which would show the correct top-level page origin).

In Windows, this behaves as expected (top-level page origin is shown).

Bluetooth chooser dialog code:

<https://source.chromium.org/chromium/chromium/src/+/main:components/permissions/android/bluetooth_chooser_android.cc;l=32;drc=8ba1bad80dc22235693a0dd41fe55c0fd2dbdabd>

BluetoothChooserAndroid::BluetoothChooserAndroid(  

content::RenderFrameHost\* frame,  

const EventHandler& event\_handler,  

std::unique\_ptr<BluetoothChooserAndroidDelegate> delegate)  

: web\_contents\_(content::WebContents::FromRenderFrameHost(frame)),  

event\_handler\_(event\_handler),  

delegate\_(std::move(delegate)) {  

const url::Origin origin = frame->GetLastCommittedOrigin(); // [1] Frame is of initiator page, not top-level page

// [...]

java\_dialog\_.Reset(Java\_BluetoothChooserDialog\_create(  

env, window\_android, origin\_string,  

delegate\_->GetSecurityLevel(web\_contents\_), delegate\_->GetJavaObject(),  

reinterpret\_cast<intptr\_t>(this)));  

}

USB chooser dialog code:

<https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/android/device_dialog/usb_chooser_dialog_android.cc;l=52;drc=4a4d6b6c1d3838655299764b03e976a160612f30>

std::unique\_ptr<UsbChooserDialogAndroid> UsbChooserDialogAndroid::Create(  

content::RenderFrameHost\* render\_frame\_host,  

std::unique\_ptr[permissions::ChooserController](javascript:void(0);) controller,  

base::OnceClosure on\_close) {

// [...]

base::android::ScopedJavaLocalRef<jstring> origin\_string =  

base::android::ConvertUTF16ToJavaString(  

env, url\_formatter::FormatOriginForSecurityDisplay(  

render\_frame\_host->GetLastCommittedOrigin())); // [1] RFH is of initiator page, not top-level page

// [...]

dialog->java\_dialog\_.Reset(Java\_UsbChooserDialog\_create(  

env, window\_android, origin\_string, helper->GetSecurityLevel(),  

j\_profile\_android, reinterpret\_cast<intptr\_t>(dialog.get())));  

if (dialog->java\_dialog\_.is\_null())  

return nullptr;

return dialog;  

}

Note that the navigator.usb API did not seem to work in slightly-older M106 Stable versions, so please ensure you are in latest Stable or Canary to reproduce USB PoC.

**VERSION**  

Chrome Version: 106.0.5249.126 Stable, 109.0.5361.0 Canary  

Operating System: Android 12

**REPRODUCTION CASE**

Bluetooth:

1. Navigate to <https://alesandroortiz.com/chromium/bt-usb-permission-delegation.html?bt>
2. Tap the cross-origin iframe to open device chooser.

Observed: Initiator iframe page origin (<https://aogarantiza.com>) is shown in dialog.  

Expected: Top-level page origin (<https://alesandroortiz.com>) is shown in dialog.

USB:  

Pre-requisite: USB device connected to Android device, such as external microphone or keyboard.

1. Navigate to <https://alesandroortiz.com/chromium/bt-usb-permission-delegation.html?usb>
2. Tap the cross-origin iframe to open device chooser.
3. Select a device from the list and tap "Connect".

Observed: Initiator frame origin (<https://aogarantiza.com>) is shown in dialog. Allowing access provides access to the top-level page and any frames that have permission delegated, despite only the initiator frame's origin being shown in dialog.

To demonstrate that the top-level page also has access to the USB device, the PoC will show the output of navigator.usb.getDevices() every 3 seconds.  

This can also be verified by tapping the lock icon and seeing the permission for the USB device listed for the top-level page's origin.

Expected: Top-level page origin (<https://alesandroortiz.com>) is shown in dialog. Allowing access provides access to the top-level page and any frames that have permission delegated.

**CREDIT INFORMATION**  

Reporter credit: Alesandro Ortiz <https://AlesandroOrtiz.com>

## Attachments

- [bt-usb-permission-delegation.html](attachments/bt-usb-permission-delegation.html) (text/plain, 1.0 KB)
- [bt-usb-frame.html](attachments/bt-usb-frame.html) (text/plain, 1.2 KB)
- [bt-usb-permission-delegation.mp4](attachments/bt-usb-permission-delegation.mp4) (video/mp4, 1.6 MB)
- [bt-expected-windows-1.png](attachments/bt-expected-windows-1.png) (image/png, 39.5 KB)
- [usb-expected-windows-2.png](attachments/usb-expected-windows-2.png) (image/png, 41.2 KB)
- deleted (application/octet-stream, 0 B)
- [bt-android-discovery-permission-delegation.jpg](attachments/bt-android-discovery-permission-delegation.jpg) (image/jpeg, 68.7 KB)

## Timeline

### [Deleted User] (2022-10-16)

[Empty comment from Monorail migration]

### al...@alesandroortiz.com (2022-10-17)

I also filed https://crbug.com/chromium/1375133 which is related to this issue. Fixing this issue may also fix https://crbug.com/chromium/1375133.

### jd...@chromium.org (2022-10-18)

Reilly, would you mind taking a look at this and the other one, since you've worked on this stuff previously? I think Alesandro is right re: delegated permissions. Thank you!

[Monorail components: Blink>Bluetooth Blink>USB UI>Browser>Permissions>Prompts]

### [Deleted User] (2022-10-18)

[Empty comment from Monorail migration]

### al...@alesandroortiz.com (2022-10-18)

jdeblasio: OS labels seem to be opposite of what they should be ;) (same for https://crbug.com/chromium/1375133)

### [Deleted User] (2022-10-18)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-10-18)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### re...@chromium.org (2022-10-18)

This is the same as https://crbug.com/chromium/1280233, but applies only to Android as that issue fixed all the desktop platforms. Unfortunately as pointed out in the summary, there is separate Android-specific logic for choosing the origin to display in the dialog which wasn't updated at the same time.

Jack, can you take a look at this? The fix itself is trivial but we should make sure to add test coverage for this if it is missing.

### al...@alesandroortiz.com (2022-10-21)

I also see similar code in BluetoothScanningPromptAndroid that is reachable with chrome://flags/#enable-experimental-web-platform-features enabled and calling navigator.bluetooth.requestLEScan({acceptAllAdvertisements:true});

I confirmed that dialog also uses the incorrect origin on my Android device. See attached screenshot where top-level origin is https://alesandroortiz.com and initiator frame origin is https://aogarantiza.com. I can share PoC if requested.

https://source.chromium.org/chromium/chromium/src/+/main:components/permissions/android/bluetooth_scanning_prompt_android.cc;l=40;drc=8ba1bad80dc22235693a0dd41fe55c0fd2dbdabd

### al...@alesandroortiz.com (2022-10-21)

Attaching correct screenshot for https://crbug.com/chromium/1375132#c9.

### ch...@google.com (2022-10-28)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-31)

chengweih: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### re...@chromium.org (2022-10-31)

The fix for this is under review: https://chromium-review.googlesource.com/c/chromium/src/+/3966139

### gi...@appspot.gserviceaccount.com (2022-11-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b96dc03cef30a79345629bc604b23b3ca490c1fe

commit b96dc03cef30a79345629bc604b23b3ca490c1fe
Author: Jack Hsieh <chengweih@chromium.org>
Date: Tue Nov 01 00:25:04 2022

[Android] Use the origin of the main frame in chooser dialogs

Permissions dialogs (for WebUSB, WebBluetooth) should request permission
for the main origin (the origin embedding the iframe) and not the site
hosting the iframe as per crbug.com/802945. Update the Android UI code
to accurately display the main origin and add tests.

Bug: 1375132
Change-Id: Ib3f8a2aa69d0ac5a4c8338f2638a701f4fee929b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3966139
Reviewed-by: Reilly Grant <reillyg@chromium.org>
Commit-Queue: Jack Hsieh <chengweih@chromium.org>
Reviewed-by: Illia Klimov <elklm@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1065744}

[modify] https://crrev.com/b96dc03cef30a79345629bc604b23b3ca490c1fe/chrome/browser/ui/android/device_dialog/usb_chooser_dialog_android.cc
[add] https://crrev.com/b96dc03cef30a79345629bc604b23b3ca490c1fe/chrome/browser/ui/android/device_dialog/usb_chooser_dialog_android_unittest.cc
[modify] https://crrev.com/b96dc03cef30a79345629bc604b23b3ca490c1fe/components/permissions/android/bluetooth_scanning_prompt_android.h
[modify] https://crrev.com/b96dc03cef30a79345629bc604b23b3ca490c1fe/chrome/browser/ui/android/device_dialog/usb_chooser_dialog_android.h
[modify] https://crrev.com/b96dc03cef30a79345629bc604b23b3ca490c1fe/components/permissions/android/bluetooth_chooser_android.h
[add] https://crrev.com/b96dc03cef30a79345629bc604b23b3ca490c1fe/components/permissions/android/bluetooth_scanning_prompt_android_unittest.cc
[modify] https://crrev.com/b96dc03cef30a79345629bc604b23b3ca490c1fe/components/permissions/android/bluetooth_chooser_android.cc
[modify] https://crrev.com/b96dc03cef30a79345629bc604b23b3ca490c1fe/chrome/test/BUILD.gn
[modify] https://crrev.com/b96dc03cef30a79345629bc604b23b3ca490c1fe/components/permissions/BUILD.gn
[modify] https://crrev.com/b96dc03cef30a79345629bc604b23b3ca490c1fe/components/permissions/android/bluetooth_scanning_prompt_android.cc
[add] https://crrev.com/b96dc03cef30a79345629bc604b23b3ca490c1fe/components/permissions/android/bluetooth_chooser_android_unittest.cc


### re...@chromium.org (2022-11-01)

[Empty comment from Monorail migration]

### re...@chromium.org (2022-11-01)

Joe, given the lower severity of this issue and that M-107 is already on stable-channel what do you think about only merging this back to M-108, if at all?

### [Deleted User] (2022-11-01)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-02)

[Empty comment from Monorail migration]

### al...@alesandroortiz.com (2022-11-02)

Verified as fixed in 109.0.5395.0 Canary on Android 12. Tested with all three PoCs: BT, USB, and BT scanning/discovery dialog.

Unfortunately does not fix https://crbug.com/chromium/1375133 based on patch review and testing.

### am...@google.com (2022-11-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-11-11)

Congratulations, Alesandro! The VRP Panel has decided to award you $3,000 for this report. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2022-11-11)

[Empty comment from Monorail migration]

### al...@alesandroortiz.com (2022-11-18)

Thanks for the reward!

### am...@chromium.org (2023-01-09)

[Empty comment from Monorail migration]

### am...@google.com (2023-01-10)

[Empty comment from Monorail migration]

### pg...@google.com (2023-01-10)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-08)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1375132?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>Bluetooth, Blink>USB, UI>Browser>Permissions>Prompts]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061373)*
