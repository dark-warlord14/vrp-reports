# Security: UAF in UsbDeviceHandleMac::AsyncIoCallback

| Field | Value |
|-------|-------|
| **Issue ID** | [40074794](https://issues.chromium.org/issues/40074794) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | IO>USB |
| **Platforms** | Mac |
| **Reporter** | vu...@darknavy.com |
| **Assignee** | ma...@chromium.org |
| **Created** | 2023-10-13 |
| **Bounty** | $8,000.00 |

## Description

**VULNERABILITY DETAILS**  

A renderer can transfer USB control packets through WebAPI `USBDevice.controlTransferIn/controlTransferOut`. Browser will handle it by async API `DeviceRequestAsyncTO` with a callback function `AsyncIoCallback` [0]. Browser should make sure `transfer_ptr` is not free'd when the callback is called.

```
  IOReturn kr = (\*device_interface_)  
                    ->DeviceRequestAsyncTO(  
                        device_interface_, &device_request, &AsyncIoCallback, // [0]  
                        reinterpret_cast<void\*>(transfer_ptr));  

```

All transfers stored in device are free'd at [1]. A renderer could reach this function by calling `USBDevice.reset` or `USBDevice.selectConfiguration`.

```
void UsbDeviceHandleMac::Clear() {  
  base::flat_set<std::unique_ptr<Transfer>, base::UniquePtrComparator>  
      transfers;  
  transfers.swap(transfers_);  
  for (auto& transfer : transfers) {  
    DCHECK(transfer);  
    if (transfer->type == mojom::UsbTransferType::ISOCHRONOUS) {  
      ReportIsochronousTransferError(std::move(transfer->isochronous_callback),  
                                     transfer->packet_lengths,  
                                     mojom::UsbTransferStatus::TRANSFER_ERROR);  
    } else {  
      std::move(transfer->generic_callback)  
          .Run(mojom::UsbTransferStatus::TRANSFER_ERROR,  
               std::move(transfer->buffer), 0);  
    }  
  }  
  transfers.clear(); // [1]  
  interfaces_.clear();  
  sources_.clear();  
}  

```

The async callback is managed by MacOS `CFRunLoopSourceRef`. Control packets are bound to `device_source_`, which is neglected in `UsbDeviceHandleMac::Clear`. One can do a control request, and clear transfers immediately, resulting in UAF in `AsyncIoCallback`.

[0] <https://source.chromium.org/chromium/chromium/src/+/main:services/device/usb/usb_device_handle_mac.cc;drc=f5bdc89c7395ed24f1b8d196a3bdd6232d5bf771;l=460>  

[0] <https://source.chromium.org/chromium/chromium/src/+/main:services/device/usb/usb_device_handle_mac.cc;drc=f5bdc89c7395ed24f1b8d196a3bdd6232d5bf771;l=884>

BISECT  

Introduced by <https://chromium.googlesource.com/chromium/src/+/87dddee8310c66a56d6fbf8c8d1889a06885bd6e>  

which adds `device_source_` to handle USB control packets.

**VERSION**  

Chrome Version: stable  

Operating System: Mac

SUGGESTED FIX:  

Invalidate `device_source_` in `UsbDeviceHandleMac::Clear`. See fix.diff

**REPRODUCTION CASE**  

The bug is in the new Mac USB implementation. Reproduction needs to enable the NewUsbBackend feature.  

$ python -m http.server  

$ ./chrome --enable-features=NewUsbBackend '<http://localhost:8000/poc.html>'

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: browser  

Crash log: see asan.txt

**CREDIT INFORMATION**  

Reporter credit: DarkNavy

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 674 B)
- [asan.txt](attachments/asan.txt) (text/plain, 31.3 KB)
- [fix.diff](attachments/fix.diff) (text/plain, 461 B)

## Timeline

### [Deleted User] (2023-10-13)

[Empty comment from Monorail migration]

### ct...@chromium.org (2023-10-13)

Thank you for your detailed reports and for another USB vuln, and for the suggested patch! Adding reillyg@ and mattreynolds@ here as well.

This is a UAF in a privileged process, but it requires a WebUSB device picker selection by the user, so marking this as Severity-High.

The NewUsbBackend on macOS is not enabled by default in tree and does not appear to be enabled by any server-side configurations (this appears to have been previously rolled out for Windows only), so marking this as Impact-None.

[Monorail components: IO>USB]

### re...@chromium.org (2023-10-13)

This one is lower priority since the new macOS backend isn't enabled by default and we have no plans to do so any time soon.

### ma...@google.com (2023-10-26)

[Empty comment from Monorail migration]

### ma...@google.com (2023-10-26)

[Empty comment from Monorail migration]

### an...@chromium.org (2023-11-30)

[security shepherd] mattreynolds@, reillyg@ is there a feature bug we can block w/ this bug to make sure it's fixed before the eventual feature release? Thanks!

### ma...@google.com (2023-11-30)

[Empty comment from Monorail migration]

### ja...@chromium.org (2023-12-14)

I'm sending out crrev.com/c/5124493 to annotate the feature flag with a TODO pointing to this bug. I'll pass it to mattreynolds for review.

### gi...@appspot.gserviceaccount.com (2023-12-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/a79600ff1896d45ce952bd58f4afd2aa13290ca1

commit a79600ff1896d45ce952bd58f4afd2aa13290ca1
Author: Javier Castro <jacastro@chromium.org>
Date: Fri Dec 15 17:15:22 2023

Annotate NewUsbBackend feature flag with launch blocking TODO

We'll need to address https://crbug.com/1492383 before we can enable
NewUsbBackend for Mac OS. Adding this TODO by the feature flag to make
sure we don't forget to resolve the issue in the future.

Change-Id: I942f19ca730581fda24656324e12216a7fa8210c
Bug: 1492383,1096743
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5124493
Reviewed-by: Matt Reynolds <mattreynolds@chromium.org>
Commit-Queue: Javier Castro <jacastro@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1238113}

[modify] https://crrev.com/a79600ff1896d45ce952bd58f4afd2aa13290ca1/device/base/features.cc


### ph...@chromium.org (2024-01-19)

[security shepherd] mattreynolds@: Are there any plans to launch this feature?  If not, could that code be removed rather than keeping vulnerable code production code base?

### ma...@google.com (2024-01-23)

We don't have any plans to launch this in 2024 but the code should not be removed.

### is...@google.com (2024-01-23)

This issue was migrated from crbug.com/chromium/1492383?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail blocking: crbug.com/chromium/1096743]
[Monorail components added to Component Tags custom field.]

### am...@chromium.org (2024-04-26)

[secondary security shepherd] hi mattreynolds@, since there are no plans to launch this feature in 2024, why is code removal not an option? Is this a candidate to potentially move to Chrome for Testing (CfT) when that work is finalized?

If removal or moving to Chrome for Testing is not an option, we'll need to keep checking in about this issue since it is a high severity security bug that exists in the Chrome code base. Can you please set a next action date and information about when this issue may be expected to be resolved.

### re...@chromium.org (2024-04-26)

Given the code in question is pretty isolated I'm okay with landing a CL to remove it and keeping the issue open so it's still being tracked and it'll be easy to revert the CL removing it when the team is ready to pick up work on it again.

### ma...@chromium.org (2024-04-26)

> why is code removal not an option

Code removal is an option, but I would prefer not to remove code that we still plan to release even if we don't have plans to work on it this year. The feature is already disabled by default and effectively removed from supported configurations. My team is working on fixing other security and crash bugs which I consider higher priority than this bug since they affect features which are already launched.

> Is this a candidate to potentially move to Chrome for Testing (CfT) when that work is finalized?

Would this make it so the base::Feature is available in CfT but not in normal Chrome channels? I think that would work.

> Can you please set a next action date and information about when this issue may be expected to be resolved.

I've set NextAction for +2 weeks.

Resolving this issue requires creating a custom manual test to verify that the USB transfer is not written into the deallocated buffer. Once we can verify the fix in https://crrev.com/c/4944991 is safe then we can merge it and resolve this bug.

### ap...@google.com (2024-05-06)

Project: chromium/src
Branch: main

commit 44c8ef69554107c416a57af784c2f6b01070ecd1
Author: Alvin Ji <alvinji@chromium.org>
Date:   Mon May 06 21:40:31 2024

    usb: Remove macOS experimental usb backend
    
    Temporarily remove the experimental macOS USB backend to address a
    security vulnerability (crbug.com/40074794). This CL can be reverted to restore the feature once the issue is resolved.
    
    Bug: 40074794
    Change-Id: I8ede11cbc94e64b1565c04313d0e02a5849cdae2
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5513119
    Commit-Queue: Alvin Ji <alvinji@chromium.org>
    Reviewed-by: Matt Reynolds <mattreynolds@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1297127}

M       device/base/features.cc
M       device/base/features.h
M       services/device/usb/BUILD.gn
D       services/device/usb/usb_device_handle_mac.cc
D       services/device/usb/usb_device_handle_mac.h
D       services/device/usb/usb_device_mac.cc
D       services/device/usb/usb_device_mac.h
M       services/device/usb/usb_service.cc
D       services/device/usb/usb_service_mac.cc
D       services/device/usb/usb_service_mac.h
M       services/device/usb/usb_service_unittest.cc

https://chromium-review.googlesource.com/5513119


### el...@chromium.org (2024-05-07)

Hi! Security shepherd here - in light of #17, is this now Fixed?

### al...@chromium.org (2024-05-07)

We created crrev.com/c/5513119 to remove the vulnerable code temporarily before we have resources to address the security but report by this issue. 
I assume we could keep this bug open but decreased to lower priority?


### ma...@chromium.org (2024-05-07)

Let's close the issue since the code has been removed

### pe...@google.com (2024-05-09)

The NextAction date has arrived: 2024-05-09 
 To opt-out from this automation rule, please add Optout-Blintz-Nextaction-Alert to the "Chromium Labels" custom field.

### sp...@google.com (2024-05-15)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $8000.00 for this report.

Rationale for this decision:
$7,000 for this report of mildly mitigated memory corruption in a non-sandboxed process + $1,000 bisect bonus -- nice work!

Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. Two other things we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.
* If you are already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have already registered, there is no need to repeat the process and you’ll automatically be paid soon. If you have any payment related questions or issues, please reach out to p2p-vrp@google.com.

### pe...@google.com (2024-08-14)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> $7,000 for this report of mildly mitigated memory corruption in a non-sandboxed process + $1,000 bisect bonus -- nice work!
> 
> Thank you for your efforts and helping us make Chrome more secure for all users!
> 
> Cheers,
> Chrome VRP Panel Bot
> 
> 
> P.S. Two other things we'd like to mention:
> 
> * Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a 

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40074794)*
