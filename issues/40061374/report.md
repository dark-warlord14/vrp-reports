# Security: Device chooser dialogs do not show origin if initiator origin is opaque

| Field | Value |
|-------|-------|
| **Issue ID** | [40061374](https://issues.chromium.org/issues/40061374) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Bluetooth, Blink>HID, Blink>Serial, Blink>USB, UI>Browser>Permissions>Prompts |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | al...@alesandroortiz.com |
| **Assignee** | si...@chromium.org |
| **Created** | 2022-10-16 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

This report describes same behavior affecting two different dialogs, but filing together since they're closely related.

In Android, the Bluetooth and USB chooser dialogs do not show origin if initiator is opaque because they look only at the initiator frame's LastCommittedOrigin() [1]. A subsequent DCHECK [2] in the Bluetooth code further indicates this code does not expect opaque origins. The dialog uses the return value [3] of url\_formatter::FormatOriginForSecurityDisplay() which is an empty string for opaque origins, therefore the dialog shows an empty string.

Empty origin in dialog can be achieved by an opaque iframe, a non-opaque iframe that creates its own sandboxed iframe, or any other way that allows creation of opaque origins.

This may be mitigated by a fix for <https://crbug.com/chromium/1375132> if the top-level page can never be opaque; otherwise, the code must handle opaque origins. I have not tested top-level page with opaque origin behavior in other OSes, so the issue may exist there as well if it's possible to create an opaque top-level page that can use these APIs.

Bluetooth chooser dialog code:

<https://source.chromium.org/chromium/chromium/src/+/main:components/permissions/android/bluetooth_chooser_android.cc;l=32;drc=8ba1bad80dc22235693a0dd41fe55c0fd2dbdabd>

BluetoothChooserAndroid::BluetoothChooserAndroid(  

content::RenderFrameHost\* frame,  

const EventHandler& event\_handler,  

std::unique\_ptr<BluetoothChooserAndroidDelegate> delegate)  

: web\_contents\_(content::WebContents::FromRenderFrameHost(frame)),  

event\_handler\_(event\_handler),  

delegate\_(std::move(delegate)) {  

const url::Origin origin = frame->GetLastCommittedOrigin(); // [1]  

DCHECK(!origin.opaque()); // [2]

ScopedJavaLocalRef<jobject> window\_android =  

web\_contents\_->GetNativeView()->GetWindowAndroid()->GetJavaObject();

// Create (and show) the BluetoothChooser dialog.  

JNIEnv\* env = AttachCurrentThread();  

ScopedJavaLocalRef<jstring> origin\_string =  

base::android::ConvertUTF16ToJavaString(  

env, url\_formatter::FormatOriginForSecurityDisplay(origin)); // [3]  

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

render\_frame\_host->GetLastCommittedOrigin())); // [1] [3]

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

1. Navigate to <https://alesandroortiz.com/chromium/bt-usb.html?bt>
2. Tap the iframe to open device chooser.

USB:  

Pre-requisite: USB device connected to Android device, such as external microphone or keyboard.

1. Navigate to <https://alesandroortiz.com/chromium/bt-usb.html?usb>
2. Tap the iframe to open device chooser.

For both scenarios:  

Observed: No origin is shown in dialog.  

Expected: Either top-level page origin is shown in dialog, dialog is not shown, or other safer behavior.

**CREDIT INFORMATION**  

Reporter credit: Alesandro Ortiz <https://AlesandroOrtiz.com>

## Attachments

- [bt-usb.html](attachments/bt-usb.html) (text/plain, 583 B)
- [bt-usb-frame.html](attachments/bt-usb-frame.html) (text/plain, 1.2 KB)
- [bt-usb-opaque-origin.mp4](attachments/bt-usb-opaque-origin.mp4) (video/mp4, 906.9 KB)
- [bt-expected-windows-1.png](attachments/bt-expected-windows-1.png) (image/png, 39.5 KB)
- [usb-expected-windows-2.png](attachments/usb-expected-windows-2.png) (image/png, 41.2 KB)
- [bt-windows-top-level-opaque-new-perms-feature.png](attachments/bt-windows-top-level-opaque-new-perms-feature.png) (image/png, 42.5 KB)
- [usb-windows-top-level-opaque.png](attachments/usb-windows-top-level-opaque.png) (image/png, 26.8 KB)
- [hid-windows-top-level-opaque.png](attachments/hid-windows-top-level-opaque.png) (image/png, 27.4 KB)
- [serial-windows-top-level-opaque.png](attachments/serial-windows-top-level-opaque.png) (image/png, 23.2 KB)
- [bt-android-discovery-opaque-origin.jpg](attachments/bt-android-discovery-opaque-origin.jpg) (image/jpeg, 52.1 KB)

## Timeline

### [Deleted User] (2022-10-17)

[Empty comment from Monorail migration]

### jd...@chromium.org (2022-10-18)

This one too. Thanks, Reilly!

[Monorail components: Blink>Bluetooth Blink>USB UI>Browser>Permissions>Prompts]

### [Deleted User] (2022-10-18)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-18)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-10-18)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### re...@chromium.org (2022-10-18)

I'm checking with the team on whether a top-level frame can have an opaque origin. Since the UI displays the correct frame's origin on desktop platforms (https://crbug.com/chromium/1375132 is Android-specific) it should be possible to test a PoC for that case.

### re...@chromium.org (2022-10-18)

I've confirmed that a top-level frame can have an opaque origin. For example, if the "Content-Security-Policy: sandbox" header is sent by the server. I've created https://acute-saber-gray.glitch.me/ as a demonstration of how this works with the device APIs that use the chooser dialog.

Other permission-requesting APIs such as navigator.geolocation.getCurrentPosition() seem to automatically deny the permission request. I think this is the correct behavior as the only alternative is to only allow ephemeral permission grants for opaque origins and the permission storage infrastructure is not set up for that.

### re...@chromium.org (2022-10-19)

Sina is going to take a look at fixing this for Web Bluetooth, WebHID, Web Serial and WebUSB. CCing Jack who is working on the related Android-specific issue and can give Sina a hand.

### re...@chromium.org (2022-10-19)

[Empty comment from Monorail migration]

[Monorail components: Blink>HID Blink>Serial]

### re...@chromium.org (2022-10-19)

The tasks that are needed to resolve this bug are (for each API):

1. Add checks in Blink for SecurityOrigin::IsOpaque() to the permission requesting APIs which throw a helpful error message so developers understand what is going on. Example from Web Locks: https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/locks/lock_manager.cc;l=270;drc=b93c76d7f427e3e2267063f03a82aff2bdf66ce8
2. Add Web Platform Tests for this behavior.
3. Add checks in //content/browser which call mojo::Receiver::ReportBadMessage() if a renderer for an opaque origin tries to call these APIs. The checks added in (1) should prevent this from ever happening unless the renderer is compromised.
4. Add tests for these checks.

The Web Locks example shows that some specifications explicitly call out an API being unavailable to opaque origins. I'm not sure we actually want to specify that in this case because as mentioned in https://crbug.com/chromium/1375133#c7 there is a way to handle permission-requesting APIs for opaque origins but it just isn't supported by Chrome's permissions architecture.

### al...@alesandroortiz.com (2022-10-20)

reillyg@: Thanks for confirming top-level opaque origins are possible in https://crbug.com/chromium/1375133#c7.

Using your demo, this is observed behavior on Windows using Canary 109.0.5369.0:

Bluetooth:
    * With WebBluetoothNewPermissionsBackend disabled (default): Hits this browser-side CHECK():
https://source.chromium.org/chromium/chromium/src/+/main:content/browser/bluetooth/bluetooth_allowed_devices_map.cc;l=22;drc=4e1b7bc33d42b401d7d9ad1dcba72883add3e2af
    * With WebBluetoothNewPermissionsBackend enabled: Shows empty origin in dialog (see attached screenshot), so a browser-side CHECK must also be added in this code path.

USB, HID, Serial: Shows empty origin dialog (see attached screenshots), so a browser-side CHECK must be added for these chooser dialogs.

### al...@alesandroortiz.com (2022-10-20)

Another way to create an opaque top-level page is to open a new page (popup/tab) from a sandboxed frame, although this requires an additional user interaction compared to the CSP: sandbox HTTP header method. The new page will inherit the opener's sandbox flags.

PoC of this method, tested on Windows and Android:
1. Navigate to https://alesandroortiz.com/security/chromium/open-opaque-page.html
2. Interact with sandboxed iframe (click or press any key) to open new page (tab in this case, can also be a popup)
3. Click anywhere on the opened sandboxed page (which is same PoC from report: https://alesandroortiz.com/security/chromium/bt-usb-frame.html?usb )

Observed: No origin is shown in dialog due to opaque origin. `window.origin` of page is `null`.

Would appreciate it if someone updates the bug title to remove "Android" and maybe change "Bluetooth and USB chooser dialogs" to "Device chooser dialogs" (since it also affects Serial + HID).

### re...@chromium.org (2022-10-20)

[Empty comment from Monorail migration]

### si...@chromium.org (2022-10-20)

[Empty comment from Monorail migration]

### al...@alesandroortiz.com (2022-10-21)

I also see similar code in BluetoothScanningPromptAndroid that is reachable with chrome://flags/#enable-experimental-web-platform-features enabled and calling navigator.bluetooth.requestLEScan({acceptAllAdvertisements:true});

I confirmed that dialog also does not show origin on my Android device. See attached screenshot where top-level origin is https://alesandroortiz.com and initiator frame origin is opaque. Trying this with top-level page seems to also hit the CHECK described in https://crbug.com/chromium/1375133#c11, but it might work with WebBluetoothNewPermissionsBackend enabled (I don't know how to enable it on my device, so I can't verify). I can share PoC if requested.

https://source.chromium.org/chromium/chromium/src/+/main:components/permissions/android/bluetooth_scanning_prompt_android.cc;l=40;drc=8ba1bad80dc22235693a0dd41fe55c0fd2dbdabd

### ch...@google.com (2022-10-25)

[Empty comment from Monorail migration]

### ch...@google.com (2022-10-25)

[Empty comment from Monorail migration]

### ch...@google.com (2022-10-25)

[Empty comment from Monorail migration]

### ch...@google.com (2022-10-31)

[Empty comment from Monorail migration]

### al...@alesandroortiz.com (2022-11-02)

FYI, patch for related https://crbug.com/chromium/1375132 landed but does not affect any behavior reported in this crbug (not surprising, but wanted to explicitly make a note of this).

### [Deleted User] (2022-11-04)

sinafirooz: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### si...@chromium.org (2022-11-04)

I am currently investigating the issue. Will provide more updates early next week.

### [Deleted User] (2022-11-18)

sinafirooz: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### si...@google.com (2022-11-23)

I created crrev.com/c/4050183. The CL ignores opaque origins' access requests to Bluetooth. The same will be added to other devices after cleaning the code up and making sure the proper message will be shown to the user.

### [Deleted User] (2022-11-30)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-02)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### si...@google.com (2023-01-05)

crrev.com/c/4113162 is about to be done submitting to CQ. The CL fixes the issue on render side for Web Bluetooth APIs. I need to write tests for the code on browser side of the Web Bluetooth API and repeat the two CLs in HID, Serial, and USB.

### gi...@appspot.gserviceaccount.com (2023-01-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/5921c8faeff0048f179c698b1935f1a183bb10f2

commit 5921c8faeff0048f179c698b1935f1a183bb10f2
Author: gsinafirooz <sinafirooz@google.com>
Date: Thu Jan 05 00:39:26 2023

Reject Web Bluetooth requests with an opaque origin

The Web Bluetooth API tracks permissions using the origin of the top-level document in the frame tree. If this document has an opaque origin then there is no way to format the origin for display to the user in permission prompts or to write their decision in the preferences file.

Access to the Web Bluetooth API from such contexts should therefore be blocked.

Bug: 1375133
Change-Id: Idf737c1806eac4342e0fe716e2561e51aa127f53
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4113162
Reviewed-by: Reilly Grant <reillyg@chromium.org>
Commit-Queue: Sina Firoozabadi <sinafirooz@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1089042}

[modify] https://crrev.com/5921c8faeff0048f179c698b1935f1a183bb10f2/third_party/blink/renderer/modules/bluetooth/bluetooth.cc
[add] https://crrev.com/5921c8faeff0048f179c698b1935f1a183bb10f2/third_party/blink/web_tests/external/wpt/bluetooth/getAvailability/sandboxed_iframe.https.window.js
[add] https://crrev.com/5921c8faeff0048f179c698b1935f1a183bb10f2/third_party/blink/web_tests/external/wpt/bluetooth/requestLEScan/reject_opaque_origin.https.html.headers
[add] https://crrev.com/5921c8faeff0048f179c698b1935f1a183bb10f2/third_party/blink/web_tests/external/wpt/bluetooth/requestDevice/reject_opaque_origin.https.html.headers
[add] https://crrev.com/5921c8faeff0048f179c698b1935f1a183bb10f2/third_party/blink/web_tests/external/wpt/bluetooth/getDevices/reject_opaque_origin.https.html
[modify] https://crrev.com/5921c8faeff0048f179c698b1935f1a183bb10f2/third_party/blink/web_tests/external/wpt/bluetooth/requestDevice/request-from-sandboxed-iframe.https.window.js
[add] https://crrev.com/5921c8faeff0048f179c698b1935f1a183bb10f2/third_party/blink/web_tests/external/wpt/bluetooth/requestLEScan/sandboxed_iframe.https.window.js
[add] https://crrev.com/5921c8faeff0048f179c698b1935f1a183bb10f2/third_party/blink/web_tests/external/wpt/bluetooth/getDevices/sandboxed_iframe.https.window.js
[add] https://crrev.com/5921c8faeff0048f179c698b1935f1a183bb10f2/third_party/blink/web_tests/external/wpt/bluetooth/getAvailability/reject_opaque_origin.https.html.headers
[add] https://crrev.com/5921c8faeff0048f179c698b1935f1a183bb10f2/third_party/blink/web_tests/external/wpt/bluetooth/requestLEScan/reject_opaque_origin.https.html
[modify] https://crrev.com/5921c8faeff0048f179c698b1935f1a183bb10f2/third_party/blink/web_tests/external/wpt/bluetooth/resources/health-thermometer-iframe.html
[modify] https://crrev.com/5921c8faeff0048f179c698b1935f1a183bb10f2/third_party/blink/web_tests/external/wpt/bluetooth/requestDevice/cross-origin-iframe.sub.https.window.js
[add] https://crrev.com/5921c8faeff0048f179c698b1935f1a183bb10f2/third_party/blink/web_tests/external/wpt/bluetooth/requestDevice/sandboxed_iframe.https.window.js
[add] https://crrev.com/5921c8faeff0048f179c698b1935f1a183bb10f2/third_party/blink/web_tests/external/wpt/bluetooth/getAvailability/reject_opaque_origin.https.html
[add] https://crrev.com/5921c8faeff0048f179c698b1935f1a183bb10f2/third_party/blink/web_tests/external/wpt/bluetooth/getDevices/reject_opaque_origin.https.html.headers
[add] https://crrev.com/5921c8faeff0048f179c698b1935f1a183bb10f2/third_party/blink/web_tests/external/wpt/bluetooth/requestDevice/reject_opaque_origin.https.html


### ts...@chromium.org (2023-01-12)

sinafirooz - did the CL above fix the issue?  If so, please close this bug. Otherwise, can you tell us what work remains?  Thanks!

### gi...@appspot.gserviceaccount.com (2023-01-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/8a27399d0dc11027826fabe2639a8ce64a0c3863

commit 8a27399d0dc11027826fabe2639a8ce64a0c3863
Author: Sina Firoozabadi <sinafirooz@google.com>
Date: Wed Jan 25 22:32:26 2023

Reject Web HID requests with an opaque origin

The Web HID API tracks permissions using the origin of the top-level document in the frame tree. If this document has an opaque origin then there is no way to format the origin for display to the user in permission prompts or to write their decision in the preferences file.

Access to the Web HID API from such contexts should therefore be blocked.

Bug: 1375133
Change-Id: I7992b2886e882bbbb097b0460114f0a02a02e34f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4133535
Reviewed-by: Reilly Grant <reillyg@chromium.org>
Commit-Queue: Sina Firoozabadi <sinafirooz@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1097051}

[add] https://crrev.com/8a27399d0dc11027826fabe2639a8ce64a0c3863/third_party/blink/web_tests/wpt_internal/hid/requestDevice/reject_opaque_origin.https.html.headers
[add] https://crrev.com/8a27399d0dc11027826fabe2639a8ce64a0c3863/third_party/blink/web_tests/wpt_internal/hid/resources/open-in-iframe.html
[modify] https://crrev.com/8a27399d0dc11027826fabe2639a8ce64a0c3863/third_party/blink/renderer/modules/hid/hid.cc
[add] https://crrev.com/8a27399d0dc11027826fabe2639a8ce64a0c3863/third_party/blink/web_tests/wpt_internal/hid/getDevices/reject_opaque_origin.https.html
[add] https://crrev.com/8a27399d0dc11027826fabe2639a8ce64a0c3863/third_party/blink/web_tests/wpt_internal/hid/requestDevice/reject_opaque_origin.https.html
[add] https://crrev.com/8a27399d0dc11027826fabe2639a8ce64a0c3863/third_party/blink/web_tests/wpt_internal/hid/getDevices/reject_opaque_origin.https.html.headers
[add] https://crrev.com/8a27399d0dc11027826fabe2639a8ce64a0c3863/third_party/blink/web_tests/wpt_internal/hid/getDevices/sandboxed_iframe.https.window.js
[add] https://crrev.com/8a27399d0dc11027826fabe2639a8ce64a0c3863/third_party/blink/web_tests/wpt_internal/hid/requestDevice/sandboxed_iframe.https.window.js


### si...@google.com (2023-01-25)

Quick update by far:

          | browser | render |
Bluetooth |   WIP   |  DONE  |
HID       |   WIP   |  DONE  |
Serial    |   WIP   |  WIP   |
USB       |   WIP   |  WIP   |

### [Deleted User] (2023-02-08)

[Empty comment from Monorail migration]

### ch...@google.com (2023-02-10)

Hi Reilly,

I tried to figure out how the opaque origin in WebUSB/WebHID service worker case. i.e whether we should have opaque origin check in [1] (WebUSB service worker create()) and [2] (WebHID service worker create()).

By looking at Service Workers spec about opaque origin in [3] and [4], it seems as long as the service worker's worker/window client is an opaque origin, service worker is not available to the clients. And for the extension service worker case, it would always be extension origin. 

So, do you think it is fair to say we can ignore handling opaque origin for service worker cases?

[1] https://source.chromium.org/chromium/chromium/src/+/main:content/browser/usb/web_usb_service_impl.cc;l=186;drc=adac219925ef5d9c9a954d189c2e4b8852a4bbed
[2] https://source.chromium.org/chromium/chromium/src/+/main:content/browser/hid/hid_service.cc;l=200;drc=adac219925ef5d9c9a954d189c2e4b8852a4bbed
[3] https://www.w3.org/TR/service-workers/#control-and-use-window-client
[4] https://www.w3.org/TR/service-workers/#control-and-use-worker-client



### re...@chromium.org (2023-02-10)

I think we should still report a bad message in that case, but I agree that since Service Workers aren't available to pages with opaque origins it's hard to write a test for it.

### ho...@chromium.org (2023-02-16)

[Empty comment from Monorail migration]

### ch...@google.com (2023-02-28)

An email thread related to this can be found at : https://groups.google.com/a/google.com/g/deviceapi-team/c/-7UlNX0y4y8

### gi...@appspot.gserviceaccount.com (2023-03-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/63530bf3e5b5592eaa64d55c8e21a3492ba00a7e

commit 63530bf3e5b5592eaa64d55c8e21a3492ba00a7e
Author: Jack Hsieh <chengweih@chromium.org>
Date: Fri Mar 03 00:35:32 2023

Add top level frame security origin in GlobalWorkerScope

Add a new field of top level frame security origin in GlobalWorkerScope,
so that worker thread on the renderer side can use it to check if it has
the right permission for some operations according to top level frame’s
security origin. For example, a worker can use it to check if the top
level frame has an opaque origin hence blocking access to WebUSB API.

Bug: 1375133
Change-Id: I0bcbdcee583daf75823fd87bbea866130984b46e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4251485
Reviewed-by: Hiroki Nakagawa <nhiroki@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1112560}

[modify] https://crrev.com/63530bf3e5b5592eaa64d55c8e21a3492ba00a7e/third_party/blink/renderer/core/loader/empty_clients.h
[modify] https://crrev.com/63530bf3e5b5592eaa64d55c8e21a3492ba00a7e/third_party/blink/renderer/core/workers/dedicated_worker_test.h
[modify] https://crrev.com/63530bf3e5b5592eaa64d55c8e21a3492ba00a7e/third_party/blink/renderer/core/workers/dedicated_worker_test.cc
[modify] https://crrev.com/63530bf3e5b5592eaa64d55c8e21a3492ba00a7e/third_party/blink/renderer/core/workers/worker_global_scope.cc
[modify] https://crrev.com/63530bf3e5b5592eaa64d55c8e21a3492ba00a7e/third_party/blink/renderer/core/workers/global_scope_creation_params.h
[modify] https://crrev.com/63530bf3e5b5592eaa64d55c8e21a3492ba00a7e/third_party/blink/renderer/core/workers/dedicated_worker.cc
[modify] https://crrev.com/63530bf3e5b5592eaa64d55c8e21a3492ba00a7e/third_party/blink/renderer/core/workers/global_scope_creation_params.cc
[modify] https://crrev.com/63530bf3e5b5592eaa64d55c8e21a3492ba00a7e/third_party/blink/renderer/core/workers/worker_global_scope.h
[modify] https://crrev.com/63530bf3e5b5592eaa64d55c8e21a3492ba00a7e/third_party/blink/renderer/core/workers/dedicated_worker.h


### gi...@appspot.gserviceaccount.com (2023-03-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/0d2f7d8d41ac2bc092cd21174236cfa4be96f0ae

commit 0d2f7d8d41ac2bc092cd21174236cfa4be96f0ae
Author: Jack Hsieh <chengweih@chromium.org>
Date: Fri Mar 03 00:35:32 2023

Reject Web Serial requests with an opaque origin

The Web Serial API tracks permissions using the origin of the top-level
document in the frame tree. If this document has an opaque origin then
there is no way to format the origin for display to the user in
permission prompts or to write their decision in the preferences file.

Access to the Web Serial API from such contexts should therefore be
blocked.

Bug: 1375133
Change-Id: I4552ae74d480aa8df9ff93527fc85618bc03b947
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4112689
Reviewed-by: Reilly Grant <reillyg@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1112561}

[modify] https://crrev.com/0d2f7d8d41ac2bc092cd21174236cfa4be96f0ae/third_party/blink/renderer/modules/serial/serial.cc
[add] https://crrev.com/0d2f7d8d41ac2bc092cd21174236cfa4be96f0ae/third_party/blink/web_tests/external/wpt/serial/getPorts/reject_opaque_origin.https.html
[add] https://crrev.com/0d2f7d8d41ac2bc092cd21174236cfa4be96f0ae/third_party/blink/web_tests/external/wpt/serial/requestPort/reject_opaque_origin.https.html
[add] https://crrev.com/0d2f7d8d41ac2bc092cd21174236cfa4be96f0ae/third_party/blink/web_tests/external/wpt/serial/requestPort/sandboxed_iframe.https.window.js
[add] https://crrev.com/0d2f7d8d41ac2bc092cd21174236cfa4be96f0ae/third_party/blink/web_tests/external/wpt/serial/resources/open-in-iframe.html
[add] https://crrev.com/0d2f7d8d41ac2bc092cd21174236cfa4be96f0ae/third_party/blink/web_tests/external/wpt/serial/requestPort/reject_opaque_origin.https.html.headers
[add] https://crrev.com/0d2f7d8d41ac2bc092cd21174236cfa4be96f0ae/third_party/blink/web_tests/external/wpt/serial/getPorts/reject_opaque_origin.https.html.headers
[add] https://crrev.com/0d2f7d8d41ac2bc092cd21174236cfa4be96f0ae/third_party/blink/web_tests/external/wpt/serial/getPorts/sandboxed_iframe.https.window.js


### gi...@appspot.gserviceaccount.com (2023-03-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/47b4f7b306b3d6aa4a2d94e61b5bfbc653440591

commit 47b4f7b306b3d6aa4a2d94e61b5bfbc653440591
Author: Jack Hsieh <chengweih@chromium.org>
Date: Mon Mar 06 05:57:34 2023

Reland "Add top level frame security origin in GlobalWorkerScope"

This reverts commit a1497e151b9c0fa094a48a6cb97c235abd41c8df.

Reason for revert: Fixed the failure of https://ci.chromium.org/ui/p/chromium/builders/ci/linux-ubsan-vptr/21391/overview.

Original change's description:
> Revert "Add top level frame security origin in GlobalWorkerScope"
>
> Revert submission 4112689
>
> Reason for revert: suspect for introducing test failures for
> DedicatedWorkerTest.TopLevelFrameSecurityOrigin, for example
> https://ci.chromium.org/ui/p/chromium/builders/ci/linux-ubsan-vptr/21391/overview
>
> Reverted changes: /q/submissionid:4112689
>
> Change-Id: I5d9f05f031f312c4e37d908e5d112f5289ba30bc
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4307115
> Commit-Queue: Mikel Astiz <mastiz@chromium.org>
> Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
> Owners-Override: Mikel Astiz <mastiz@google.com>
> Cr-Commit-Position: refs/heads/main@{#1112817}

Change-Id: I759b90d7b56ab28a43a550bdd940e6765da09c23
Bug: 1375133
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4307819
Reviewed-by: Hiroki Nakagawa <nhiroki@chromium.org>
Commit-Queue: Jack Hsieh <chengweih@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1113254}

[modify] https://crrev.com/47b4f7b306b3d6aa4a2d94e61b5bfbc653440591/third_party/blink/renderer/core/loader/empty_clients.h
[modify] https://crrev.com/47b4f7b306b3d6aa4a2d94e61b5bfbc653440591/third_party/blink/renderer/core/workers/dedicated_worker_test.h
[modify] https://crrev.com/47b4f7b306b3d6aa4a2d94e61b5bfbc653440591/third_party/blink/renderer/core/workers/dedicated_worker_test.cc
[modify] https://crrev.com/47b4f7b306b3d6aa4a2d94e61b5bfbc653440591/third_party/blink/renderer/core/workers/worker_global_scope.cc
[modify] https://crrev.com/47b4f7b306b3d6aa4a2d94e61b5bfbc653440591/third_party/blink/renderer/core/workers/dedicated_worker.cc
[modify] https://crrev.com/47b4f7b306b3d6aa4a2d94e61b5bfbc653440591/third_party/blink/renderer/core/workers/global_scope_creation_params.cc
[modify] https://crrev.com/47b4f7b306b3d6aa4a2d94e61b5bfbc653440591/third_party/blink/renderer/core/workers/global_scope_creation_params.h
[modify] https://crrev.com/47b4f7b306b3d6aa4a2d94e61b5bfbc653440591/third_party/blink/renderer/core/workers/worker_global_scope.h
[modify] https://crrev.com/47b4f7b306b3d6aa4a2d94e61b5bfbc653440591/third_party/blink/renderer/core/workers/dedicated_worker.h


### gi...@appspot.gserviceaccount.com (2023-03-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/f16775dd9caa6debbe57f01640259605ebf8d337

commit f16775dd9caa6debbe57f01640259605ebf8d337
Author: Sina Firoozabadi <sinafirooz@google.com>
Date: Mon Mar 06 23:08:43 2023

Refactor the Web Bluetooth tests to pass in a `PendingReceiver` rather than having it owned by `TestRenderFrameHost`.

Bug: 1375133
Change-Id: I9267127714db681c6c6e41ad86e5a6273cf34846
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4214467
Reviewed-by: Robert Kroeger <rjkroege@chromium.org>
Reviewed-by: Reilly Grant <reillyg@chromium.org>
Commit-Queue: Sina Firoozabadi <sinafirooz@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1113641}

[modify] https://crrev.com/f16775dd9caa6debbe57f01640259605ebf8d337/content/test/test_render_frame_host.h
[modify] https://crrev.com/f16775dd9caa6debbe57f01640259605ebf8d337/content/browser/bluetooth/frame_connected_bluetooth_devices_unittest.cc
[modify] https://crrev.com/f16775dd9caa6debbe57f01640259605ebf8d337/content/test/test_render_frame_host.cc
[modify] https://crrev.com/f16775dd9caa6debbe57f01640259605ebf8d337/content/browser/bluetooth/web_bluetooth_service_impl_unittest.cc


### gi...@appspot.gserviceaccount.com (2023-03-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/9c66680b649045a5e59d9bac785025639c3f53ed

commit 9c66680b649045a5e59d9bac785025639c3f53ed
Author: Sina Firoozabadi <sinafirooz@google.com>
Date: Wed Mar 08 00:20:01 2023

Reject HidService interface requests from opaque origins

The Web HID API tracks permissions using the origin of the top-level document in the frame tree. If a document has an opaque origin then the requests to access Web HID get rejected on renderer side.

To add a second layer of security in case of the renderer process being compromised, responding to the Web HID mojoms from such renderer process should be avoided.

Bug: 1375133
Change-Id: I76dcccae558ef583787d646746671086d8199940
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4112672
Commit-Queue: Sina Firoozabadi <sinafirooz@chromium.org>
Reviewed-by: Reilly Grant <reillyg@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1114294}

[modify] https://crrev.com/9c66680b649045a5e59d9bac785025639c3f53ed/content/browser/hid/hid_service.cc
[modify] https://crrev.com/9c66680b649045a5e59d9bac785025639c3f53ed/content/browser/hid/hid_service_unittest.cc


### gi...@appspot.gserviceaccount.com (2023-03-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/36a29bcbf4d9b5967bfbc4cf3540c1355ca57d09

commit 36a29bcbf4d9b5967bfbc4cf3540c1355ca57d09
Author: Sina Firoozabadi <sinafirooz@google.com>
Date: Wed Mar 08 02:29:36 2023

Drop Web Bluetooth mojoms from a renderer process of an opaque origin

The Web Bluetooth API tracks permissions using the origin of the
top-level document in the frame tree. If a document has an opaque origin
then the requests to access Web Bluetooth get rejected on renderer side.

To add a second layer of security in case of the renderer process being
compromised, responding to the Web Bluetooth mojoms from such renderer
process should be avoided.

Disable-Rts: True
Bug: 1375133
Change-Id: Icbc6da4127e9c10f659d43e64cd5d7d1e207d02f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4114125
Reviewed-by: Reilly Grant <reillyg@chromium.org>
Commit-Queue: Sina Firoozabadi <sinafirooz@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1114352}

[modify] https://crrev.com/36a29bcbf4d9b5967bfbc4cf3540c1355ca57d09/content/browser/bluetooth/frame_connected_bluetooth_devices_unittest.cc
[modify] https://crrev.com/36a29bcbf4d9b5967bfbc4cf3540c1355ca57d09/content/browser/bluetooth/web_bluetooth_service_impl.cc
[modify] https://crrev.com/36a29bcbf4d9b5967bfbc4cf3540c1355ca57d09/content/browser/bluetooth/web_bluetooth_service_impl_unittest.cc
[modify] https://crrev.com/36a29bcbf4d9b5967bfbc4cf3540c1355ca57d09/content/browser/bluetooth/web_bluetooth_service_impl.h


### gi...@appspot.gserviceaccount.com (2023-03-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/4b9452a25735187b50c20d77e229b87d095f31d0

commit 4b9452a25735187b50c20d77e229b87d095f31d0
Author: Jack Hsieh <chengweih@chromium.org>
Date: Wed Mar 08 04:51:07 2023

serial: Reject using Serial API in an opaque origin

Rejects renderer's request of using Serial API when the top-level
document has an opaque origin.

Bug: 1375133
Change-Id: I14488099dda296b0fcf62f25ffef3e6e76e566ae
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4237816
Reviewed-by: Reilly Grant <reillyg@chromium.org>
Reviewed-by: Alex Moshchuk <alexmos@chromium.org>
Commit-Queue: Jack Hsieh <chengweih@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1114388}

[modify] https://crrev.com/4b9452a25735187b50c20d77e229b87d095f31d0/content/browser/renderer_host/render_frame_host_impl.cc
[modify] https://crrev.com/4b9452a25735187b50c20d77e229b87d095f31d0/content/browser/serial/serial_unittest.cc


### gi...@appspot.gserviceaccount.com (2023-03-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/dc0a8d8a80e653e13af8ff8cab0bf44b0f0baad0

commit dc0a8d8a80e653e13af8ff8cab0bf44b0f0baad0
Author: Jack Hsieh <chengweih@chromium.org>
Date: Mon Mar 13 19:57:29 2023

Reject Web USB requests with an opaque origin

The Web USB API tracks permissions using the origin of the top-level
document in the frame tree. If this document has an opaque origin then
there is no way to format the origin for display to the user in
permission prompts or to write their decision in the preferences file.

Access to the Web USB API from such contexts should therefore be
blocked.

Bug: 1375133
Change-Id: I47952bb230b3fdf0bfbc76f46d1ef91c19fc7ea1
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4248258
Reviewed-by: Reilly Grant <reillyg@chromium.org>
Commit-Queue: Jack Hsieh <chengweih@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1116559}

[add] https://crrev.com/dc0a8d8a80e653e13af8ff8cab0bf44b0f0baad0/third_party/blink/web_tests/external/wpt/webusb/requestDevice/reject_opaque_origin.https.html.headers
[modify] https://crrev.com/dc0a8d8a80e653e13af8ff8cab0bf44b0f0baad0/third_party/blink/web_tests/external/wpt/webusb/resources/open-in-worker.js
[add] https://crrev.com/dc0a8d8a80e653e13af8ff8cab0bf44b0f0baad0/third_party/blink/web_tests/external/wpt/webusb/requestDevice/reject_opaque_origin.https.html
[add] https://crrev.com/dc0a8d8a80e653e13af8ff8cab0bf44b0f0baad0/third_party/blink/web_tests/external/wpt/webusb/requestDevice/sandboxed_iframe.https.window.js
[add] https://crrev.com/dc0a8d8a80e653e13af8ff8cab0bf44b0f0baad0/third_party/blink/web_tests/external/wpt/webusb/getDevices/reject_opaque_origin.https.html.headers
[add] https://crrev.com/dc0a8d8a80e653e13af8ff8cab0bf44b0f0baad0/third_party/blink/web_tests/external/wpt/webusb/getDevices/sandboxed_iframe.https.window.js
[modify] https://crrev.com/dc0a8d8a80e653e13af8ff8cab0bf44b0f0baad0/third_party/blink/web_tests/wpt_internal/webusb/usbDevice-iframe.https.html
[modify] https://crrev.com/dc0a8d8a80e653e13af8ff8cab0bf44b0f0baad0/third_party/blink/web_tests/external/wpt/resources/chromium/webusb-child-test.js
[modify] https://crrev.com/dc0a8d8a80e653e13af8ff8cab0bf44b0f0baad0/third_party/blink/renderer/modules/webusb/usb.h
[add] https://crrev.com/dc0a8d8a80e653e13af8ff8cab0bf44b0f0baad0/third_party/blink/web_tests/external/wpt/webusb/getDevices/reject_opaque_origin.https.html
[modify] https://crrev.com/dc0a8d8a80e653e13af8ff8cab0bf44b0f0baad0/third_party/blink/web_tests/external/wpt/webusb/resources/open-in-iframe.html
[modify] https://crrev.com/dc0a8d8a80e653e13af8ff8cab0bf44b0f0baad0/third_party/blink/web_tests/external/wpt/webusb/usbDevice-worker.https.html
[modify] https://crrev.com/dc0a8d8a80e653e13af8ff8cab0bf44b0f0baad0/third_party/blink/web_tests/external/wpt/webusb/usbDevice-iframe.https.html
[modify] https://crrev.com/dc0a8d8a80e653e13af8ff8cab0bf44b0f0baad0/third_party/blink/renderer/modules/webusb/usb.cc


### gi...@appspot.gserviceaccount.com (2023-03-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/425ab488f26e70965a5109675a57ef38e504d344

commit 425ab488f26e70965a5109675a57ef38e504d344
Author: Jack Hsieh <chengweih@chromium.org>
Date: Mon Mar 13 21:19:03 2023

usb: Reject using WebUSB API in an opaque origin

Rejects renderer's request of using WebUSB API when the top-level
document has an opaque origin.

Bug: 1375133
Change-Id: I1b449389e55ea8ead412ea9e87fc99971997b491
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4237626
Reviewed-by: Hiroki Nakagawa <nhiroki@chromium.org>
Commit-Queue: Jack Hsieh <chengweih@chromium.org>
Reviewed-by: Alex Moshchuk <alexmos@chromium.org>
Reviewed-by: Reilly Grant <reillyg@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1116595}

[modify] https://crrev.com/425ab488f26e70965a5109675a57ef38e504d344/content/browser/usb/web_usb_service_impl_unittest.cc
[modify] https://crrev.com/425ab488f26e70965a5109675a57ef38e504d344/content/browser/renderer_host/render_frame_host_impl.cc
[modify] https://crrev.com/425ab488f26e70965a5109675a57ef38e504d344/content/browser/service_worker/service_worker_host.cc


### gi...@appspot.gserviceaccount.com (2023-03-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/aa06c8661961d40785c11a436cfdb35e2270dff0

commit aa06c8661961d40785c11a436cfdb35e2270dff0
Author: Jack Hsieh <chengweih@chromium.org>
Date: Mon Mar 13 23:37:52 2023

serial: Handle opaque top level origin in addedEventListener

In navigator.serial.addEventListener, throw an exception if the request
is coming from a context whose top level frame has an opaque origin.

Bug: 1375133
Change-Id: Ie8ad8333b901f795f55658894551c73f755029c4
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4313307
Commit-Queue: Jack Hsieh <chengweih@chromium.org>
Reviewed-by: Reilly Grant <reillyg@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1116683}

[modify] https://crrev.com/aa06c8661961d40785c11a436cfdb35e2270dff0/third_party/blink/renderer/modules/serial/serial.cc
[modify] https://crrev.com/aa06c8661961d40785c11a436cfdb35e2270dff0/third_party/blink/web_tests/external/wpt/serial/serial-disabled-by-permissions-policy.https.sub.html
[modify] https://crrev.com/aa06c8661961d40785c11a436cfdb35e2270dff0/third_party/blink/web_tests/external/wpt/serial/requestPort/sandboxed_iframe.https.window.js
[modify] https://crrev.com/aa06c8661961d40785c11a436cfdb35e2270dff0/third_party/blink/web_tests/external/wpt/serial/getPorts/sandboxed_iframe.https.window.js


### gi...@appspot.gserviceaccount.com (2023-03-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/2ca2e08e92a6bc67d23517c4ae8efbd0cfa2e8fe

commit 2ca2e08e92a6bc67d23517c4ae8efbd0cfa2e8fe
Author: Jack Hsieh <chengweih@chromium.org>
Date: Wed Mar 15 01:03:48 2023

hid: Handle opaque top level origin in addedEventListener

In navigator.hid.addEventListener, throw an exception if the request
is coming from a context whose top level frame has an opaque origin.

Bug: 1375133
Change-Id: I43d3c59eb4715d5c1b970d6f466a256c580582d6
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4337726
Commit-Queue: Jack Hsieh <chengweih@chromium.org>
Reviewed-by: Reilly Grant <reillyg@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1117306}

[modify] https://crrev.com/2ca2e08e92a6bc67d23517c4ae8efbd0cfa2e8fe/third_party/blink/renderer/modules/hid/hid.cc
[add] https://crrev.com/2ca2e08e92a6bc67d23517c4ae8efbd0cfa2e8fe/third_party/blink/web_tests/wpt_internal/hid/hid_connectionEvents_hid_disallowed.https.html.headers
[add] https://crrev.com/2ca2e08e92a6bc67d23517c4ae8efbd0cfa2e8fe/third_party/blink/web_tests/wpt_internal/hid/hid_connectionEvents_hid_disallowed.https.html


### ch...@google.com (2023-03-15)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-15)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-15)

[Empty comment from Monorail migration]

### am...@google.com (2023-03-22)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-03-22)

Congratulations on another one, Alesandro! The VRP Panel has decided to award you $3,000 for this report. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2023-03-27)

[Empty comment from Monorail migration]

### al...@alesandroortiz.com (2023-04-22)

VRP Panel: Thanks for the reward!

sinafirooz@ and chengweih@: Thanks for thoroughly fixing the issues! I'm still reviewing the CLs, but PoCs all are verified as fixed on latest Canary on Windows and Android. Some fixes aren't on M112 Stable, but seem like they will be in M113 which will be released as Stable in a few days.

Specifically, the PoC [1] from https://crbug.com/chromium/1375133#c12 still repros on Windows (112.0.5615.49 Stable) and Android (112.0.5615.135 Stable). Does not repro on Windows Canary 114.0.5728.0.

[1] https://alesandroortiz.com/security/chromium/open-opaque-page.html

### am...@chromium.org (2023-04-24)

This issue specifically isn't labeled for M112 release since last scheduled M112/Stable release was shipped last week and these fixes were not backmerged to M112 and the latter fixes were landed in M113. M113/Stable RC has not yet been cut and is scheduled to be released next week, these fixes should all ship in that Stable channel update at that time. 

### am...@chromium.org (2023-04-28)

[Empty comment from Monorail migration]

### pg...@google.com (2023-05-02)

[Empty comment from Monorail migration]

### pg...@google.com (2023-05-02)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-21)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1375133?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>Bluetooth, Blink>HID, Blink>Serial, Blink>USB, UI>Browser>Permissions>Prompts]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061374)*
