# Security: UAF in USBDevice

| Field | Value |
|-------|-------|
| **Issue ID** | [40053520](https://issues.chromium.org/issues/40053520) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>USB |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | le...@gmail.com |
| **Assignee** | re...@chromium.org |
| **Created** | 2020-10-07 |
| **Bounty** | $10,000.00 |

## Description

**VULNERABILITY DETAILS**

The Open-IPC-Call[1] will create a |device\_handle| and push its raw-pointer into |handles\_|[2]. Frequent calls to Open-IPC-Call will cause the old |device\_handle| to be replaced[3] and destroyed. But it will not clean up the |handles\_|. Its raw pointer will be accessed when the device is unplugged or removed[4]. And the UAF will be triggered.

[1]. <https://source.chromium.org/chromium/chromium/src/+/master:services/device/public/mojom/usb_device.mojom;l=178;drc=19d2cb1a46cc964dba7c68ebf49c9b9f8786dae6>  

[2]. <https://source.chromium.org/chromium/chromium/src/+/master:services/device/usb/usb_device_impl.cc;l=138;drc=f7f8bdab8432311f1eb4eb965da4e7a4a207bdc8>  

[3]. <https://source.chromium.org/chromium/chromium/src/+/master:services/device/usb/mojo/device_impl.cc;l=163;drc=19d2cb1a46cc964dba7c68ebf49c9b9f8786dae6>  

[4]. <https://source.chromium.org/chromium/chromium/src/+/master:services/device/usb/usb_device.cc;l=122;drc=c5e1504da9cb1583a10bed486117feb37c0fe12b>

**VERSION**

Chrome Version: M86 stable  

Operating System: Windows, Mac

**REPRODUCTION CASE**

$ python ./copy\_mojo\_js\_bindings.py /path/to/chrome/.../out/asan/gen  

$ python -m SimpleHTTPServer  

$ out/asan/chrome --enable-blink-features=MojoJS --user-data-dir=/tmp/xxxx "<http://localhost:8000/poc.html>"  

Select a usb device, the UAF will be triggered when the device is unplugged or removed.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**

Type of crash: browser  

Crash State: see asan file

**CREDIT INFORMATION**

Reporter credit: Leecraso and Guang Gong of 360 Alpha Lab working with 360 BugCloud

## Attachments

- [asan](attachments/asan) (text/plain, 15.8 KB)
- [copy_mojo_js_bindings.py](attachments/copy_mojo_js_bindings.py) (text/plain, 512 B)
- [poc.html](attachments/poc.html) (text/plain, 629 B)

## Timeline

### me...@chromium.org (2020-10-07)

Thanks for the report. Reilly, could you PTAL?

Tentatively assigning high severity since the bug requires user interaction (selecting a usb device).

[Monorail components: Blink>USB]

### re...@chromium.org (2020-10-07)

I knew fixing that bug where we weren't actually doing anything in OnDisconnect() would come back to bite me.

### re...@chromium.org (2020-10-07)

OnDisconnect() is not the only consumer of the handle list. It is also used in the Windows backend to notify open connections when new child devices are enumerated. The comment in usb_device.h stating that UsbDeviceHandles will be removed from the list before they are freed relies on the assumption that Close() is called on the handle before its last reference is dropped. There are DCHECKs which test this but DeviceImpl has a bug as identified by the reporter where parallel calls to Open() can cause the UsbDeviceHandle to be replaced and the original not closed.

### re...@chromium.org (2020-10-07)

I am testing a potential fix: https://chromium-review.googlesource.com/c/chromium/src/+/2454846

### [Deleted User] (2020-10-07)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-10-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/1ed869ad4bb34e9868933cd2b20dc22ab83a5021

commit 1ed869ad4bb34e9868933cd2b20dc22ab83a5021
Author: Reilly Grant <reillyg@chromium.org>
Date: Wed Oct 07 23:26:36 2020

usb: Prevent parallel calls to UsbDevice::Open

This change adds a check to prevent a Mojo client from calling Open()
multiple times while the open is in progress.

Bug: 1135857
Change-Id: Ib467de9129673710b883d9e186c32c359f8592d8
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2454846
Auto-Submit: Reilly Grant <reillyg@chromium.org>
Reviewed-by: Matt Reynolds <mattreynolds@chromium.org>
Commit-Queue: Reilly Grant <reillyg@chromium.org>
Cr-Commit-Position: refs/heads/master@{#814940}

[modify] https://crrev.com/1ed869ad4bb34e9868933cd2b20dc22ab83a5021/services/device/usb/mojo/device_impl.cc
[modify] https://crrev.com/1ed869ad4bb34e9868933cd2b20dc22ab83a5021/services/device/usb/mojo/device_impl.h
[modify] https://crrev.com/1ed869ad4bb34e9868933cd2b20dc22ab83a5021/services/device/usb/mojo/device_impl_unittest.cc


### re...@chromium.org (2020-10-07)

Marking fixed as of the change above. Deferring to Mustafa (or sheriff-bot) to decide on requesting merges.

### [Deleted User] (2020-10-08)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-08)

Requesting merge to stable M86 because latest trunk commit (814940) appears to be after stable branch point (800218).

Requesting merge to beta M86 because latest trunk commit (814940) appears to be after beta branch point (800218).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-10-08)

This bug requires manual review: Request affecting a post-stable build
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on ToT?
4. Does this change need to be merged into other active release branches (M-1, M+1)?
5. Why are these changes required in this milestone after branch?
6. Is this a new feature?
7. If it is a new feature, is it behind a flag using finch?

Chrome OS Only:
8. Was the change reviewed and approved by the Eng Prod Representative? See Eng Prod ownership by component: http://go/cros-engprodcomponents

Please contact the milestone owner if you have questions.
Owners: govind@(Android), bindusuvarna@(iOS), geohsu@(ChromeOS),  pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### re...@chromium.org (2020-10-08)

1. Does your merge fit within the Merge Decision Guidelines?

I believe so. The M-86 target was chosen by sheriffbot based on the Security_Impact-Stable label.

2. Links to the CLs you are requesting to merge.

https://chromium-review.googlesource.com/c/chromium/src/+/2454846

3. Has the change landed and been verified on ToT?

Yes, the feature has been smoke-tested on 88.0.4286.0.

4. Does this change need to be merged into other active release branches (M-1, M+1)?

It should be merged into M-86 and M-87.

5. Why are these changes required in this milestone after branch?

A high-severity security issue was reported after branch.

6. Is this a new feature?

No.

7. If it is a new feature, is it behind a flag using finch?

N/A

### ad...@google.com (2020-10-12)

[Empty comment from Monorail migration]

### ad...@google.com (2020-10-12)

Just to reassure you this isn't being ignored - I'll go through the next round of M86 merge requests (including this one) on Monday afternoon as requested by release TPMs.

### ad...@google.com (2020-10-12)

Approving merge to M86. Please merge to branch 4240.

(Note to self for release notes purposes: if the OS label is to be believed, this doesn't affect Android).

### ad...@google.com (2020-10-12)

Commit 1ed869ad4bb34e9868933cd2b20dc22ab83a5021 landed in M88, so also adding merge approval for M87 (branch 4280).

### re...@chromium.org (2020-10-12)

This code is shared with Android.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-10-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/b47a65a8002da9da3ab563d9375ed80fa1c31041

commit b47a65a8002da9da3ab563d9375ed80fa1c31041
Author: Reilly Grant <reillyg@chromium.org>
Date: Mon Oct 12 22:38:45 2020

usb: Prevent parallel calls to UsbDevice::Open

This change adds a check to prevent a Mojo client from calling Open()
multiple times while the open is in progress.

(cherry picked from commit 1ed869ad4bb34e9868933cd2b20dc22ab83a5021)

Bug: 1135857
Change-Id: Ib467de9129673710b883d9e186c32c359f8592d8
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2454846
Auto-Submit: Reilly Grant <reillyg@chromium.org>
Reviewed-by: Matt Reynolds <mattreynolds@chromium.org>
Commit-Queue: Reilly Grant <reillyg@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#814940}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2466345
Reviewed-by: Reilly Grant <reillyg@chromium.org>
Cr-Commit-Position: refs/branch-heads/4240@{#1228}
Cr-Branched-From: f297677702651916bbf65e59c0d4bbd4ce57d1ee-refs/heads/master@{#800218}

[modify] https://crrev.com/b47a65a8002da9da3ab563d9375ed80fa1c31041/services/device/usb/mojo/device_impl.cc
[modify] https://crrev.com/b47a65a8002da9da3ab563d9375ed80fa1c31041/services/device/usb/mojo/device_impl.h
[modify] https://crrev.com/b47a65a8002da9da3ab563d9375ed80fa1c31041/services/device/usb/mojo/device_impl_unittest.cc


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-10-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/0904779c49be3807218e98148efe3fe34fca8313

commit 0904779c49be3807218e98148efe3fe34fca8313
Author: Reilly Grant <reillyg@chromium.org>
Date: Mon Oct 12 23:11:51 2020

usb: Prevent parallel calls to UsbDevice::Open

This change adds a check to prevent a Mojo client from calling Open()
multiple times while the open is in progress.

(cherry picked from commit 1ed869ad4bb34e9868933cd2b20dc22ab83a5021)

Bug: 1135857
Change-Id: Ib467de9129673710b883d9e186c32c359f8592d8
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2454846
Auto-Submit: Reilly Grant <reillyg@chromium.org>
Reviewed-by: Matt Reynolds <mattreynolds@chromium.org>
Commit-Queue: Reilly Grant <reillyg@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#814940}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2466346
Reviewed-by: Reilly Grant <reillyg@chromium.org>
Cr-Commit-Position: refs/branch-heads/4280@{#286}
Cr-Branched-From: ea420fb963f9658c9969b6513c56b8f47efa1a2a-refs/heads/master@{#812852}

[modify] https://crrev.com/0904779c49be3807218e98148efe3fe34fca8313/services/device/usb/mojo/device_impl.cc
[modify] https://crrev.com/0904779c49be3807218e98148efe3fe34fca8313/services/device/usb/mojo/device_impl.h
[modify] https://crrev.com/0904779c49be3807218e98148efe3fe34fca8313/services/device/usb/mojo/device_impl_unittest.cc


### ad...@google.com (2020-10-13)

[Empty comment from Monorail migration]

### ad...@google.com (2020-10-13)

[Empty comment from Monorail migration]

### ad...@google.com (2020-10-14)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-10-14)

Congratulations! The VRP program has decided to award $10,000 for this bug.

### ad...@google.com (2020-10-16)

[Empty comment from Monorail migration]

### ad...@google.com (2020-11-03)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-14)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1135857?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40053520)*
