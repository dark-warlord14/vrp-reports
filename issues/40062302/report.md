# Security: heap-buffer-overflow in HidDeviceManager::GetApiDevicesFromList

| Field | Value |
|-------|-------|
| **Issue ID** | [40062302](https://issues.chromium.org/issues/40062302) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>Apps>API>HID, Platform>Extensions>API |
| **Platforms** | Windows |
| **Reporter** | un...@gmail.com |
| **Assignee** | ch...@chromium.org |
| **Created** | 2022-12-17 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

When choosing Hid devices in the page created by extension, heap buffer overflow occurs.

**VERSION**  

Chrome Version:111.0.5483.0 (Developer Build) (64-bit)  

Operating System:Windows 10 19045  

tested on <https://www.googleapis.com/download/storage/v1/b/chromium-browser-asan/o/win32-release_x64%2Fasan-win32-release_x64-1084688.zip?generation=1671266526092459&alt=media>

**REPRODUCTION CASE**

1. download chromium version from above link, and install extension according to uploaded files, an app window will be created by the extension.
2. click scan button on the app window, chrome.hid.getUserSelectedDevices() function in main.js will be called.
3. after scan result shows, choosing a device in the list, and click "select" button, OOB occurs.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash:browser

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 15.2 KB)
- [manifest.json](attachments/manifest.json) (text/plain, 206 B)
- [background.js](attachments/background.js) (text/plain, 139 B)
- [window.html](attachments/window.html) (text/plain, 259 B)
- [main.js](attachments/main.js) (text/plain, 301 B)
- [angular.min.js](attachments/angular.min.js) (text/plain, 122.6 KB)
- [poc.mp4](attachments/poc.mp4) (video/mp4, 1.0 MB)
- [window.html](attachments/window.html) (text/plain, 67 B)
- [main.js](attachments/main.js) (text/plain, 232 B)
- [picture1.png](attachments/picture1.png) (image/png, 235.9 KB)
- [picture2.png](attachments/picture2.png) (image/png, 230.0 KB)
- [poc on vm.mp4](attachments/poc on vm.mp4) (video/mp4, 2.8 MB)
- [issue1402000_chrome_app_package.zip](attachments/issue1402000_chrome_app_package.zip) (application/octet-stream, 45.0 KB)
- [issue1402000_usb.zip](attachments/issue1402000_usb.zip) (application/octet-stream, 45.2 KB)

## Timeline

### [Deleted User] (2022-12-17)

[Empty comment from Monorail migration]

### aj...@google.com (2022-12-17)

Thanks - we'll take a look on Monday - in the meantime do you have a smaller repro that doesn't require angular?

### un...@gmail.com (2022-12-18)

The following uploaded files removed the reference of angular.min.js, just replace the old files of the same name when reproduce.

### aj...@google.com (2022-12-19)

Thanks - I'm not able to reproduce - the list of devices is not even populating - it's possible I'm hitting some local reason for that though.

Are you running with any command line flags or features enabled?

### aj...@google.com (2022-12-19)

[Empty comment from Monorail migration]

### un...@gmail.com (2022-12-19)

I just run chrome.exe in command line, and no other flags or features needed. I'm not sure if it's the reason that several hid device or usb device attached to laptop is needed.

### [Deleted User] (2022-12-19)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### un...@gmail.com (2022-12-20)

I reproduced the crash in physical machine,  and I reproduced the bug on a virtual machine too. The problem I encountered on virtual machine was when I click "Scan", the result list of devices will show nothing(see in picture1). And I passthrough a device(eg, keyboard) into the virtual machine, the result shows correctly(see in picture 2).

If your virtual machine runs on VMware Workstation, you can refer the following link to passthrough the hid device into the virtual machine.
https://linuxhint.com/passthrough-usb-devices-vmware-workstation/

The video records the process of reproducing the bug on vm, hope that will be helpful for you.


### un...@gmail.com (2022-12-20)

Please use external keyboard or mouse when reproducing this bug. The keyboard or touch pad on laptop itself may not be recognized as hid device, since they are not connected through usb interface. 

### xi...@chromium.org (2022-12-20)

Thanks for the report! I don't have a physical windows machine and I'm not using VMware. I can't reproduce it on my physical Linux machine. The screencast does look convincing. chengweih@, could you help investigate? Thanks!

Setting severity to medium because it requires an extension installed. The code is around for a while so setting FoundIn label to M108 (current extended stable version).

[Monorail components: Platform>Apps>API>HID Platform>Extensions>API]

### [Deleted User] (2022-12-20)

[Empty comment from Monorail migration]

### ch...@google.com (2022-12-20)

[Empty comment from Monorail migration]

### re...@chromium.org (2022-12-20)

Updating the Security_Impact label because the chrome.hid.getUserSelectedDevices() method is only available on dev-channel. We should check however that the same issue doesn't exist with the chrome.usb.getUserSelectedDevices() method which is available on stable-channel.

### [Deleted User] (2022-12-20)

[Empty comment from Monorail migration]

### ch...@google.com (2022-12-20)

I can reproduce the same issue on my physical windows machine which is connected with one keyboard.

I found that when I tried testing with debug build would even hit the crash in [1].

[44776:12968:1220/151315.406:FATAL:hid_device_manager.cc(156)] Check failed: device_entry != resource_ids_.end().

I will check further and update.

[1] https://source.chromium.org/chromium/chromium/src/+/main:extensions/browser/api/hid/hid_device_manager.cc;l=156;drc=a3cb0e6330f3d54c4737f780326f62e60c4c87f3

### ch...@google.com (2022-12-20)

Added the package that I reproduced the issue with locally.

### xi...@chromium.org (2022-12-21)

Thanks for the investigation! We have replaced Security_Impact-Dev with the FoundIn- label. Please help verify if this issue can be affecting the stable-channel and update the FoundIn- label. For now, I will set FoundIn-110 since the API is only available on dev-channel.

### [Deleted User] (2022-12-21)

[Empty comment from Monorail migration]

### re...@chromium.org (2022-12-21)

Is there a label for "this is in dev-channel and will never be released to stable-channel"? That's the state of this API, since it is locked to dev-channel by https://source.chromium.org/chromium/chromium/src/+/main:extensions/common/api/_api_features.json;l=263;drc=fb4b50c629b706c5bcd818b76348cf2e84125057.

### aj...@google.com (2022-12-21)

@amyressler - see https://crbug.com/chromium/1402000#c19 this has an odd deployment pattern so might need careful steering through the merges.


### ch...@google.com (2022-12-21)

The reason for hitting the DCHECK[1] is due to the extensions::HidDeviceManager in the flow of directly invoking chrome.hid.getUserSelectedDevices won't properly call HidDeviceManager::LazyInitialize() and the internal tracking structure resource_id_[2] isn't synced with the device shown to the chooser. So it ended up hitting [1]

I will look further to see where the HidDeviceManager::LazyInitialize() should be called and how to make sure resource_id_ is synced in the scenario of using chrome.hid.getUserSelectedDevices


[1] https://source.chromium.org/chromium/chromium/src/+/main:extensions/browser/api/hid/hid_device_manager.cc;l=156;drc=a3cb0e6330f3d54c4737f780326f62e60c4c87f3
[2] https://source.chromium.org/chromium/chromium/src/+/main:extensions/browser/api/hid/hid_device_manager.cc;l=244;drc=a3cb0e6330f3d54c4737f780326f62e60c4c87f3

### re...@chromium.org (2022-12-21)

Even if we call HidDeviceManager::LazyInitialize() it might be possible for resource_ids_ to get out of sync with the value that is returned from the prompt because HidDevicePermissionsPrompt is talking directly to the HidManager Mojo service rather than getting device information through HidDeviceManager.

Looking at the USB version of this it looks like UsbDevicePermissionsPrompt implements extensions::UsbDeviceManager::Observer and so I'm guessing that the chrome.usb.getUserSelectedDevices() API won't have this same problem, though I would appreciate you checking just in case.

Given that the chrome.hid API is deprecated as part of the Chrome Apps deprecation and we never shipped chrome.hid.getUserSelectedDevices() beyond dev-channel I wonder if it's easier just to remove the code rather than fix it. We aren't likely to ever ship it to stable-channel.

### [Deleted User] (2022-12-22)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-12-22)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-12-22)

dear bot, I know you can't read comments (like https://crbug.com/chromium/1402000#c19), only labels, so I've adjusted the labels in a way you hopefully stop nagging my developer friends. 
Unfortunately, there is not a label for ""this is in dev-channel and will never be released to stable-channel"? That's the state of this API, since it is locked to dev-channel". I can't remove the foundin-110 or else you'll continue to get nags about adding a foundin- for the security bugs. 

ReleaseBlock-NA will quell it for now. 
Once this issue is fixed, it sheriffbot will add merge-request labels, you can simply add a merge-NA label to end these nags as well. Or just tag me onto the bug and I can assist. 

### [Deleted User] (2022-12-22)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@google.com (2022-12-22)

For USB counterpart concern, I created a USB chrome app top of the HID chrome app, the package can be found in the attachment.

chrome.usb.getUserSelectedDevices doesn't have this issue. It has similar condition that the prompt give it a device UsbDeviceManager isn't aware of, but the way it handle this situation is to lazily create an entry in the internal maps (i.e guid_to_id_map_[1] and id_to_guid_map_[2]).


```[3]
void UsbDeviceManager::GetApiDevice(
    const device::mojom::UsbDeviceInfo& device_in,
    api::usb::Device* device_out) {
  device_out->device = GetIdFromGuid(device_in.guid); // < --lazily create an entry for the guid
  ...
}
```


[1] https://source.chromium.org/chromium/chromium/src/+/main:extensions/browser/api/usb/usb_device_manager.h;l=121;drc=3decef66bc4c08b142a19db9628e9efe68973e64
[2] https://source.chromium.org/chromium/chromium/src/+/main:extensions/browser/api/usb/usb_device_manager.h;l=122;drc=3decef66bc4c08b142a19db9628e9efe68973e64
[3] https://source.chromium.org/chromium/chromium/src/+/main:extensions/browser/api/usb/usb_device_manager.cc;l=171;drc=3decef66bc4c08b142a19db9628e9efe68973e64;bpv=0;bpt=1


### ch...@google.com (2022-12-22)

Add the attachment for https://crbug.com/chromium/1402000#c27.

### gi...@appspot.gserviceaccount.com (2022-12-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/ca355315026b0bd2fa1539c186d922208908e484

commit ca355315026b0bd2fa1539c186d922208908e484
Author: Jack Hsieh <chengweih@chromium.org>
Date: Tue Dec 27 21:19:43 2022

Remove chrome.hid.getUserSelectedDevices

Remove chrome.hid.getUserSelectedDevices as it bears a security buG
according to crbug.com/1402000. The reason for removing this API rather
than fixing it is that the API is being deprecated as part of the Chrome
Apps deprecation and this API is never accessible beyond dev-channel.
Besides, the metric HID_GETUSERSELECTEDDEVICES of the histogram
Extensions.Functions.ExtensionCalls indicates no usage.

Bug: 1402000
Change-Id: I6bb523fd8b2e15eb42d45f2d33e9abedcaa7e7ce
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4121410
Reviewed-by: Devlin Cronin <rdevlin.cronin@chromium.org>
Commit-Queue: Jack Hsieh <chengweih@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1087179}

[modify] https://crrev.com/ca355315026b0bd2fa1539c186d922208908e484/extensions/common/api/_api_features.json
[modify] https://crrev.com/ca355315026b0bd2fa1539c186d922208908e484/extensions/browser/extension_function_histogram_value.h
[modify] https://crrev.com/ca355315026b0bd2fa1539c186d922208908e484/extensions/browser/api/hid/hid_api.h
[modify] https://crrev.com/ca355315026b0bd2fa1539c186d922208908e484/extensions/browser/api/hid/hid_apitest.cc
[modify] https://crrev.com/ca355315026b0bd2fa1539c186d922208908e484/extensions/common/api/hid.idl
[delete] https://crrev.com/55aa9653097c734e620a45a8832ad14836f2160b/extensions/test/data/api_test/hid/get_user_selected_devices/background.js
[modify] https://crrev.com/ca355315026b0bd2fa1539c186d922208908e484/tools/metrics/histograms/enums.xml
[modify] https://crrev.com/ca355315026b0bd2fa1539c186d922208908e484/extensions/browser/api/hid/hid_device_manager.h
[delete] https://crrev.com/55aa9653097c734e620a45a8832ad14836f2160b/extensions/test/data/api_test/hid/get_user_selected_devices/manifest.json
[modify] https://crrev.com/ca355315026b0bd2fa1539c186d922208908e484/extensions/browser/api/hid/hid_device_manager.cc
[modify] https://crrev.com/ca355315026b0bd2fa1539c186d922208908e484/extensions/browser/api/hid/hid_api.cc


### ch...@google.com (2022-12-28)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-28)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-28)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-28)

Requesting merge to dev M110 because latest trunk commit (1087179) appears to be after dev branch point (1084008).

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-12-28)

Merge approved: your change passed merge requirements and is auto-approved for M110. Please go ahead and merge the CL to branch 5481 (refs/branch-heads/5481) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: govind (Android), harrysouders (iOS), ceb (ChromeOS), danielyip (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-12-28)

API locked to dev channel (see comments #22 and #25) 

### [Deleted User] (2023-01-02)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-01-06)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@google.com (2023-01-06)

[Empty comment from Monorail migration]

### un...@gmail.com (2023-01-12)

Hi, can I get bug bounty for this issue? Thanks.

### am...@chromium.org (2023-01-12)

Hello, this report is labeled reward-topanel meaning that it will be up for assessment for a potential reward by the VRP panel at a forthcoming VRP panel session. This report will be updated accordingly when a decision has been made. 

### un...@gmail.com (2023-01-12)

Got it, thanks a lot.

### am...@google.com (2023-01-12)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-01-12)

Congratulations! The VRP Panel has decided to award you $2,000 for this report of a heavily mitigated security bug. A member of our finance team will be in touch with you soon to arrange payment. Thank you for your efforts in reporting this issue to us! 

### am...@google.com (2023-01-14)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-05)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1402000?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Platform>Apps>API>HID, Platform>Extensions>API]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062302)*
