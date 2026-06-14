# Out-of-bounds access in WebBluetoothServiceImpl

| Field | Value |
|-------|-------|
| **Issue ID** | [40050672](https://issues.chromium.org/issues/40050672) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Bluetooth |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | xb...@gmail.com |
| **Assignee** | od...@chromium.org |
| **Created** | 2019-11-13 |
| **Bounty** | $20,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36

Steps to reproduce the problem:
An out-of-bounds access or type-confusing vulnerability exists in the WebBluetoothServiceImpl::OnBluetoothScanningPromptEvent. When RequestScanningStart is called, a vulnerability can be triggered by generating a mojo connection error. A compromised renderer can exploit this vulnerability to achieve sandbox escape. 

TESTED VERSION
Google Chrome 78.0.3904.70 (Official Build) (64-bit)
Chromium 80.0.3948.0, 79.0.3923.0, 78.0.3895.0 (Developer Build) (64-bit)

DETAILS
#################################################################

# Out-of-bounds access or Type confusion
# WebBluetoothServiceImpl::OnBluetoothScanningPromptEvent
# https://cs.chromium.org/chromium/src/content/browser/bluetooth/web_bluetooth_service_impl.cc?l=295

void WebBluetoothServiceImpl::OnBluetoothScanningPromptEvent(
    BluetoothScanningPrompt::Event event,
    BluetoothDeviceScanningPromptController* prompt_controller) {
  DCHECK(!scanning_clients_.empty());                     <== DCHECK is not valid in the release

  auto client = scanning_clients_.end() - 1; <== There is no judgment as to whether scanning_clients_ is empty. 
                                                 If scanning_clients_ is empty, end()-1 will be out of bounds

  DCHECK((*client)->prompt_controller() == prompt_controller);   

  ......

  (*client)->RunRequestScanningStartCallback(std::move(result));  <== May cause type confusion
  (*client)->set_prompt_controller(nullptr);

# Trigger scanning_clients_ is cleared by a mojo error.
# WebBluetoothServiceImpl::ClearState
# if mojo If there is an error in the mojo interface it will destructor WebBluetoothServiceImpl.
# https://cs.chromium.org/chromium/src/content/browser/bluetooth/web_bluetooth_service_impl.cc?l=1826

void WebBluetoothServiceImpl::ClearState() {
  // Releasing the adapter will drop references to callbacks that have not yet
  // been executed. The receiver must be closed first so that this is allowed.
  receiver_.reset();

  characteristic_id_to_notify_session_.clear();
  scanning_clients_.clear();                      <== scanning_clients_ is empty
  pending_primary_services_requests_.clear();
  descriptor_id_to_characteristic_id_.clear();
  characteristic_id_to_service_id_.clear();
  service_id_to_device_address_.clear();
  connected_devices_.reset(
      new FrameConnectedBluetoothDevices(render_frame_host_));
  device_chooser_controller_.reset();
  device_scanning_prompt_controller_.reset();
  allowed_scan_filters_.clear();
  accept_all_advertisements_ = false;
  BluetoothAdapterFactoryWrapper::Get().ReleaseAdapter(this);
}

What is the expected behavior?

What went wrong?
# REPRODUCTION CASE
#################################################################
$ python ./copy_mojo_js_bindings.py E:\chromium_\src\out\gen
$ python -m SimpleHTTPServer&
$ E:\chromium_\src\out\release\chrome.exe --enable-blink-features=MojoJS --user-data-dir=D:\chrome\mojom\tmp\nonexist 

visit this webpage : 'http://127.0.0.1:8000/_poc_rescan_crash_client.html' 

If the version is lower than 80.0.3948.0, you need to modify the all "Mojo.bindInterface(blink.mojom.WebBluetoothService.name, mojo.makeRequest(ptr).handle,"context", true)" to "Mojo.bindInterface(blink.mojom.WebBluetoothService.name, mojo.makeRequest(ptr).handle)"

# CRASH
#################################################################
Please see the attachment crash.txt and crash.png

Did this work before? N/A 

Chrome version: 78.0.3904.70  Channel: stable
OS Version: 10.0
Flash Version:

## Attachments

- [crash.txt](attachments/crash.txt) (text/plain, 10.8 KB)
- [crash.png](attachments/crash.png) (image/png, 456.4 KB)
- [_poc_rescan_crash_client.html](attachments/_poc_rescan_crash_client.html) (text/plain, 1.4 KB)
- [copy_mojo_js_bindings.py](attachments/copy_mojo_js_bindings.py) (text/plain, 512 B)

## Timeline

### xb...@gmail.com (2019-11-13)

POC is here.

### do...@chromium.org (2019-11-13)

Thanks for the report. A compromised renderer that can escape the sandbox is a high severity security issue.

reillyg and juncai, can you urgently look into this?

[Monorail components: Blink>Bluetooth]

### do...@chromium.org (2019-11-13)

Also +cc other Bluetooth owners.

### re...@chromium.org (2019-11-13)

Ovidio, can you take a look at this today?

### do...@chromium.org (2019-11-14)

Upgrading to Critical severity after discussion with the broader security team. Please have a fix landed and merged to stable ASAP.

### aa...@google.com (2019-11-14)

[Empty comment from Monorail migration]

### aw...@google.com (2019-11-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-11-14)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-11-14)

This is a critical security issue. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### od...@google.com (2019-11-14)

[Empty comment from Monorail migration]

### ad...@google.com (2019-11-14)

[Comment Deleted]

### ad...@google.com (2019-11-14)

I am not sure why sheriffbot added RBB in https://crbug.com/chromium/1024116#c9 given that this impacts stable.

### go...@chromium.org (2019-11-14)

[Empty comment from Monorail migration]

### sr...@google.com (2019-11-14)

adejesush@ Thank you for looking into the fix for this issue, Wanted to share release dependencies and time line so we can make the right decision on next steps for this bug. This issue is deemed critical for M78 re-spin. we are currently targeting for a re-spin early next week,  With that , I would like to see based on your current investigation, do you feel we can get a fix in for this quickly and how complex do you think it would be to merge to a stable branch. 



### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-11-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/405c014642cc7aea722206149b767d7ef6611b9f

commit 405c014642cc7aea722206149b767d7ef6611b9f
Author: Ovidio Henriquez <odejesush@chromium.org>
Date: Thu Nov 14 23:04:47 2019

Fix OOB in OnBluetoothScanningPromptEvent

This changes fixes an OOB access that may occur in
WebBluetoothServiceImpl::OnBluetoothScanningPromptEvent(). The method
assumes that |scanning_clients_| will be populated when the method is
called, however it can be cleared if a Mojo connection error is
triggered.

The method now returns if |scanning_clients_| is empty, and it uses the
back() and pop() methods of vector to further prevent accidental OOB
access. Additionally, in BluetoothDeviceScanningPromptController, the
EventHandler binding is updated so that the lifetime of the class is
associated with the binding.

Bug: 1024116
Change-Id: I2008f7bc1ce65be1d94d39370ac8593f5ff418e8
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1916686
Commit-Queue: Ovidio de Jesús Ruiz-Henríquez <odejesush@chromium.org>
Reviewed-by: Reilly Grant <reillyg@chromium.org>
Cr-Commit-Position: refs/heads/master@{#715472}

[modify] https://crrev.com/405c014642cc7aea722206149b767d7ef6611b9f/content/browser/bluetooth/bluetooth_device_scanning_prompt_controller.cc
[modify] https://crrev.com/405c014642cc7aea722206149b767d7ef6611b9f/content/browser/bluetooth/web_bluetooth_service_impl.cc


### re...@chromium.org (2019-11-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-11-14)

This bug requires manual review: M79's targeted beta branch promotion date has already passed, so this requires manual review
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://goto.google.com/chrome-release-branch-merge-guidelines
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), kariahda@(iOS), cindyb@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-11-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/09c4804d5f18d0b2b0d4ffa7ac01b716ddd20afa

commit 09c4804d5f18d0b2b0d4ffa7ac01b716ddd20afa
Author: Ovidio Henriquez <odejesush@chromium.org>
Date: Thu Nov 14 23:29:27 2019

Fix OOB in OnBluetoothScanningPromptEvent

This changes fixes an OOB access that may occur in
WebBluetoothServiceImpl::OnBluetoothScanningPromptEvent(). The method
assumes that |scanning_clients_| will be populated when the method is
called, however it can be cleared if a Mojo connection error is
triggered.

The method now returns if |scanning_clients_| is empty, and it uses the
back() and pop() methods of vector to further prevent accidental OOB
access. Additionally, in BluetoothDeviceScanningPromptController, the
EventHandler binding is updated so that the lifetime of the class is
associated with the binding.

(cherry picked from commit 405c014642cc7aea722206149b767d7ef6611b9f)

Bug: 1024116
Change-Id: I2008f7bc1ce65be1d94d39370ac8593f5ff418e8
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1916686
Commit-Queue: Ovidio de Jesús Ruiz-Henríquez <odejesush@chromium.org>
Reviewed-by: Reilly Grant <reillyg@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#715472}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1918366
Reviewed-by: Krishna Govind <govind@chromium.org>
Cr-Commit-Position: refs/branch-heads/3967@{#6}
Cr-Branched-From: 4042baed2c289a6ca887f8d159058b419bc14df1-refs/heads/master@{#715079}

[modify] https://crrev.com/09c4804d5f18d0b2b0d4ffa7ac01b716ddd20afa/content/browser/bluetooth/bluetooth_device_scanning_prompt_controller.cc
[modify] https://crrev.com/09c4804d5f18d0b2b0d4ffa7ac01b716ddd20afa/content/browser/bluetooth/web_bluetooth_service_impl.cc


### go...@chromium.org (2019-11-14)

Merged the change to canary branch 3967 at #18 and triggering new canary #80.0.3967.4 for Android and Desktop from same branch. 

Please update bug with canary result tomorrow. 

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-11-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/267dcda84a0dcc514c75dd0effa219ffa2ac5cc5

commit 267dcda84a0dcc514c75dd0effa219ffa2ac5cc5
Author: Ovidio Henriquez <odejesush@chromium.org>
Date: Fri Nov 15 01:00:38 2019

Fix OOB in OnBluetoothScanningPromptEvent

This changes fixes an OOB access that may occur in
WebBluetoothServiceImpl::OnBluetoothScanningPromptEvent(). The method
assumes that |scanning_clients_| will be populated when the method is
called, however it can be cleared if a Mojo connection error is
triggered.

The method now returns if |scanning_clients_| is empty, and it uses the
back() and pop() methods of vector to further prevent accidental OOB
access. Additionally, in BluetoothDeviceScanningPromptController, the
EventHandler binding is updated so that the lifetime of the class is
associated with the binding.

(cherry picked from commit 405c014642cc7aea722206149b767d7ef6611b9f)

Bug: 1024116
Change-Id: I2008f7bc1ce65be1d94d39370ac8593f5ff418e8
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1916686
Commit-Queue: Ovidio de Jesús Ruiz-Henríquez <odejesush@chromium.org>
Reviewed-by: Reilly Grant <reillyg@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#715472}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1918661
Reviewed-by: Krishna Govind <govind@chromium.org>
Cr-Commit-Position: refs/branch-heads/3966@{#6}
Cr-Branched-From: 71c035fef1c65443a293696fa32c06aa85b22893-refs/heads/master@{#714552}

[modify] https://crrev.com/267dcda84a0dcc514c75dd0effa219ffa2ac5cc5/content/browser/bluetooth/bluetooth_device_scanning_prompt_controller.cc
[modify] https://crrev.com/267dcda84a0dcc514c75dd0effa219ffa2ac5cc5/content/browser/bluetooth/web_bluetooth_service_impl.cc


### go...@chromium.org (2019-11-15)

Android canary 80.0.3967.4 failed to build due to this bug: https://bugs.chromium.org/p/chromium/issues/detail?id=1024728#c2.

Merged the change to canary branch 3966 at #20 and triggering Android canary from same branch.

+benmason@ as FYI

### aa...@google.com (2019-11-15)

Since these require a compromised renderer, moving these to High as per current severity ratings.

### sh...@chromium.org (2019-11-15)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-11-15)

[Empty comment from Monorail migration]

### go...@chromium.org (2019-11-15)

How is the change looking in canary?

### re...@chromium.org (2019-11-15)

I'm investigating a regression in canary to determine if it is this change or another.

### go...@chromium.org (2019-11-15)

Per offline chat and mail thread, this change is merged to M78 branch 3904 - https://chromium.googlesource.com/chromium/src.git/+/2211f99710a932ac0c2333af213f21fdc66b8f36.
We will revert the change if this is the cause of regression in canary. 

### na...@google.com (2019-11-18)

[Empty comment from Monorail migration]

### go...@chromium.org (2019-11-18)

Approving merge to M79 branch 3945, please merge ASAP, thank you.

### ad...@google.com (2019-11-18)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-11-18)

[Empty comment from Monorail migration]

### go...@chromium.org (2019-11-18)

Please merge your change to M79 branch 3945 ASAP so we can pick it up for this week Beta release. Thank you.

### od...@chromium.org (2019-11-18)

The change was cherry picked and merged to branch 3945: https://chromium-review.googlesource.com/c/chromium/src/+/1922447

### go...@chromium.org (2019-11-18)

[Empty comment from Monorail migration]

### na...@google.com (2019-11-21)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2019-11-21)

Congrats! The Panel decided to reward $20,000  for this report!

### na...@google.com (2019-11-21)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-11-23)

[Empty comment from Monorail migration]

### mm...@chromium.org (2019-12-05)

odejesush@, thank you for fixing this issue. Chrome Security team needs your knowledge to prevent that whole class of bugs from happening elsewhere. We would greatly appreciate if you could tell us more about the issue by filling out the following form: https://forms.gle/VWKDUv9a8GXCCRWm7

### od...@chromium.org (2019-12-05)

Of course! I submitted the form ASAP.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-12-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/00defd2a1bd430d4fee099c198c389a8dae4183a

commit 00defd2a1bd430d4fee099c198c389a8dae4183a
Author: Ovidio Henriquez <odejesush@chromium.org>
Date: Thu Dec 12 22:49:56 2019

bluetooth: Test prompt controller OOB repro case

This change adds a unit test that reproduces the OOB bug that occurred
in WebBluetoothServiceImpl if it was cleared due to an error, but the
BluetoothDeviceScanningPromptController still called
OnBluetoothScanningPromptEvent. The OOB access happened on
WebBluetoothServiceImpl::scanning_clients_ because the method assumed
that it would not be empty at that point.

Bug: 1024116
Change-Id: I1bcd0a286fb0faef7a502aaca2144eed99e3de7f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1925883
Commit-Queue: Ovidio de Jesús Ruiz-Henríquez <odejesush@chromium.org>
Reviewed-by: Ovidio de Jesús Ruiz-Henríquez <odejesush@chromium.org>
Reviewed-by: Matt Reynolds <mattreynolds@chromium.org>
Auto-Submit: Ovidio de Jesús Ruiz-Henríquez <odejesush@chromium.org>
Cr-Commit-Position: refs/heads/master@{#724375}

[modify] https://crrev.com/00defd2a1bd430d4fee099c198c389a8dae4183a/content/browser/bluetooth/web_bluetooth_service_impl.h
[modify] https://crrev.com/00defd2a1bd430d4fee099c198c389a8dae4183a/content/browser/bluetooth/web_bluetooth_service_impl_unittest.cc


### mm...@chromium.org (2020-01-07)

[Empty comment from Monorail migration]

### [Deleted User] (2020-02-21)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/1024116?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40050672)*
