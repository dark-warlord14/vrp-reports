# Security: Out of bounds access in UsbDeviceHandleUsbfs::IsochronousTransferInternal

| Field | Value |
|-------|-------|
| **Issue ID** | [40074792](https://issues.chromium.org/issues/40074792) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | IO>USB |
| **Platforms** | Android, Linux, Mac, ChromeOS |
| **Reporter** | vu...@darknavy.com |
| **Assignee** | ma...@chromium.org |
| **Created** | 2023-10-13 |
| **Bounty** | $10,000.00 |

## Description

**VULNERABILITY DETAILS**  

A renderer can transfer USB isochronous packet through WebAPI `USBDevice.isochronousTransferOut`. Browser allocates a transfer structure, then calls platform dependent APIs to do real USB operations. Renderer provides `data` and `packetLengths` arguments. `packetLengths` is an array of isoc frame lengths. Browser doesn't validate that the buffer size is larger than the sum of `packetLengths`.

On Linux, there is actually a DCHECK [0].

```
  DCHECK_GE(buffer->size(), total_length); // [0]  
  std::unique_ptr<Transfer> transfer(new (packet_lengths.size())  
                                         Transfer(buffer, std::move(callback)));  
  transfer->urb.type = USBDEVFS_URB_TYPE_ISO;  
  transfer->urb.endpoint = endpoint_address;  
  transfer->urb.buffer_length = total_length;  

```

The malformed `packetLengths` array finally arrives in kernel via ioctl. Kernel will accumulate the array to get the total length, and read out-of-bound data to construct USB packets [1].

```
		for (totlen = u = 0; u < number_of_packets; u++) {  
			/\*  
			 \* arbitrary limit need for USB 3.1 Gen2  
			 \* sizemax: 96 DPs at SSP, 96 \* 1024 = 98304  
			 \*/  
			if (isopkt[u].length > 98304) {  
				ret = -EINVAL;  
				goto error;  
			}  
			totlen += isopkt[u].length;  
		}  
		u \*= sizeof(struct usb_iso_packet_descriptor);  
		uurb->buffer_length = totlen;  
  
  // ... snip ...  
  
				if (copy_from_user(as->urb->transfer_buffer, // [1]  
						   uurb->buffer,  
						   uurb->buffer_length)) {  
					ret = -EFAULT;  
					goto error;  
				}  

```

[0] <https://source.chromium.org/chromium/chromium/src/+/main:services/device/usb/usb_device_handle_usbfs.cc;drc=2e85357a8b76996981cc6f783853a49df2cedc3a;l=850>  

[1] <https://elixir.bootlin.com/linux/v6.2/source/drivers/usb/core/devio.c#L1839>

BISECT  

Introduced by <https://chromium.googlesource.com/chromium/src/+/fed1de7faf5d91a3282d461fd1c0657f8fe3a533>  

The vulnerable code has existed since the first implementation of USBFS.

**VERSION**  

Chrome Version: stable  

Operating System: Linux, Android

SUGGESTED FIX:  

Check arguments of `isochronousTransferOut`. Ensure `buffer` size is larger than the sum of `packetLengths`.

**REPRODUCTION CASE**  

To verify the vulnerability, we can check the `urb` kernel read is out of bounds. Apply `kernel.diff` and compile.  

$ python -m http.server  

$ ./chrome '<http://localhost:8000/poc.html>'

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Kernel log:  

[ 169.703275] urb buffer: 0x00003ddc01220fe0, length: 0x1ffe  

[ 169.703277] urb content: 00000000: 41 41 41 41 41 41 41 41 41 41 41 41 41 41 41 41 AAAAAAAAAAAAAAAA  

[ 169.703279] urb content: 00000010: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ................  

[ 169.703280] urb content: 00000020: 01 00 00 00 00 22 15 40 6e 64 68 69 00 00 00 00 .....".@ndhi....  

[ 169.703280] urb content: 00000030: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ................  

[ 169.703281] urb content: 00000040: 00 00 3d dc 01 22 04 20 50 ab 3e 00 dc 3d 00 00 ..=..". P.>..=..  

[ 169.703282] urb content: 00000050: 00 00 00 00 00 00 00 00 00 00 00 00 01 00 00 00 ................  

[ 169.703283] urb content: 00000060: 01 00 00 00 00 37 03 c0 e0 18 22 01 dc 3d 00 00 .....7...."..=..  

[ 169.703283] urb content: 00000070: 00 00 00 00 00 00 00 00 00 00 00 00 01 00 00 00 ................  

[ 169.703284] urb content: 00000080: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ................  

[ 169.703285] urb content: 00000090: 00 00 00 00 00 00 00 00 00 00 00 00 01 00 00 00 ................  

[ 169.703286] urb content: 000000a0: 02 00 00 00 00 e2 12 00 00 00 00 00 00 00 00 00 ................  

[ 169.703286] urb content: 000000b0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ................  

[ 169.703287] urb content: 000000c0: 00 00 3d dc 01 22 2c 80 58 93 3e 00 dc 3d 00 00 ..=..",.X.>..=..  

[ 169.703288] urb content: 000000d0: 00 00 00 00 00 00 00 00 00 00 00 00 01 00 00 00 ................  

[ 169.703288] urb content: 000000e0: 03 00 00 00 00 3b a5 20 00 00 00 00 00 00 52 40 .....;. ......R@  

[ 169.703289] urb content: 000000f0: 00 00 00 00 00 00 00 00 00 00 00 00 01 00 00 00 ................  

[ 169.703290] urb content: 00000100: 01 00 00 00 00 47 23 e0 01 00 00 00 dc 3d 00 00 .....G#......=..  

[ 169.703291] urb content: 00000110: 00 00 00 00 00 00 00 00 00 00 00 00 01 00 00 00 ................  

[ 169.703291] urb content: 00000120: 01 00 00 00 00 22 15 e0 6e 6a 61 62 69 00 00 00 ....."..njabi...  

[ 169.703292] urb content: 00000130: 00 00 00 00 00 00 00 00 00 00 00 00 01 00 00 00 ................  

[ 169.703293] urb content: 00000140: 80 27 18 01 dc 3d 00 00 00 00 00 00 00 00 00 00 .'...=..........  

[ 169.703293] urb content: 00000150: 00 00 00 00 00 00 00 00 00 00 00 00 01 00 00 00 ................  

[ 169.703294] urb content: 00000160: 02 00 00 00 00 22 02 a0 00 00 00 00 00 00 00 00 ....."..........  

[ 169.703295] urb content: 00000170: 00 00 00 00 00 00 00 00 00 00 00 00 01 00 00 00 ................  

[ 169.703295] urb content: 00000180: 01 00 00 00 00 22 02 80 00 00 00 00 00 00 00 00 ....."..........  

[ 169.703296] urb content: 00000190: 00 00 00 00 00 00 00 00 00 00 00 00 01 00 00 00 ................  

[ 169.703297] urb content: 000001a0: 02 00 00 00 00 22 16 00 00 00 00 00 00 00 00 00 ....."..........  

[ 169.703297] urb content: 000001b0: 00 00 00 00 00 00 00 00 00 00 00 00 01 00 00 00 ................  

[ 169.703298] urb content: 000001c0: 47 00 4c 00 56 00 44 00 45 00 4f 00 48 00 47 00 G.L.V.D.E.O.H.G.  

[ 169.703299] urb content: 000001d0: 00 00 00 00 00 00 00 00 00 00 00 00 01 00 00 00 ................  

[ 169.703300] urb content: 000001e0: 00 00 00 00 00 00 00 80 00 00 00 00 00 00 00 00 ................  

[ 169.703300] urb content: 000001f0: 00 00 00 00 00 00 00 00 00 00 00 00 01 00 00 00 ................  

[ 169.703301] urb content: 00000200: 02 00 00 00 00 22 09 00 00 00 00 00 00 00 00 00 ....."..........  

...

**CREDIT INFORMATION**  

Reporter credit: DarkNavy

## Attachments

- [kernel.diff](attachments/kernel.diff) (text/plain, 613 B)
- [poc.html](attachments/poc.html) (text/plain, 635 B)

## Timeline

### [Deleted User] (2023-10-13)

[Empty comment from Monorail migration]

### ct...@chromium.org (2023-10-13)

Thank you for this report and for the similar issue reported in https://crbug.com/chromium/1492382. The detailed investigation and bisection is very helpful.

reillyg@ could you please take a look?

A somewhat similar previous bug was previously reported in https://crbug.com/chromium/995732.

Looking at usb_device_handle_usbfs.h/cc, this code appears to be used on Android/ChromeOS/Linux, so marking OS labels accordingly. Do let us know if you think there is a broader issue beyond this specific platform implementation. (It wasn't immediately clear if the same issue affects e.g. the macOS implementation in usb_device_handle_mac.h/cc, but at a glance it appears that the buffer is directly created using the computed combined length [1] so should be safe.)

As this requires requesting access to a USB device via the WebUSB picker, but results in privileged context memory corruption (OOB read in kernel), marking this as Severity-High.

[1]: https://source.chromium.org/chromium/chromium/src/+/main:services/device/usb/usb_device_handle_mac.cc;l=497;drc=28154a6fbbcaa037ae8692d96bc114286c57f6c7

[Monorail components: IO>USB]

### [Deleted User] (2023-10-13)

[Empty comment from Monorail migration]

### ct...@chromium.org (2023-10-13)

[Empty comment from Monorail migration]

### ct...@chromium.org (2023-10-13)

Looking at https://crbug.com/chromium/1492382 in a bit more detail, both these reports share the same POC, but there are slightly different code paths used due to platform-specific code for interfacing with the USB subsystems. For clarity of investigation, I've merged that bug into this one, and added macOS as an affected OS here. Thank you for the detailed reports and investigation into the faulty logic in the code.

### ct...@chromium.org (2023-10-13)

(As an additional note, I think my initial quick read of macOS as not being affected in https://crbug.com/chromium/1492381#c2 is clearly wrong and I was looking at a different function for input where the buffer is safely constructed, versus in IsochonousTransferOut().)

### re...@chromium.org (2023-10-13)

I believe the same bug exists in usb_device_handle_impl.h/cc (the implementation currently used on macOS based on libusb).

The solution is a combination of input validation in Blink (to return an error if the buffer and packet lengths are mismatched) and validation in services/device/usb/mojo/device_impl.cc that the packet lengths sent over Mojo add up to the buffer also sent over Mojo. That should allow CHECKs in the platform-specific implementations to be valid.

### ma...@google.com (2023-10-14)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-14)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2023-10-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/bb36f739e7e0a3722beeb2744744195c22fd6143

commit bb36f739e7e0a3722beeb2744744195c22fd6143
Author: Matt Reynolds <mattreynolds@google.com>
Date: Fri Oct 20 19:40:38 2023

usb: Validate isochronous transfer packet lengths

USBDevice.isochronousTransferIn and
USBDevice.isochronousTransferOut take a parameter containing
a list of packet lengths. This CL adds validation that the
total packet length does not exceed the maximum buffer size.
For isochronousTransferOut, it also checks that the total
length of all packets in bytes is equal to the size of the
data buffer.

Passing invalid packet lengths causes the promise to be
rejected with a DataError.

Bug: 1492381, 1492384
Change-Id: Id9ae16c7e6f1c417e0fc4f21d53e9de11560b2b7
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4944690
Reviewed-by: Reilly Grant <reillyg@chromium.org>
Commit-Queue: Matt Reynolds <mattreynolds@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1212916}

[modify] https://crrev.com/bb36f739e7e0a3722beeb2744744195c22fd6143/services/device/usb/mojo/device_impl_unittest.cc
[modify] https://crrev.com/bb36f739e7e0a3722beeb2744744195c22fd6143/services/device/usb/mojo/device_impl.cc
[modify] https://crrev.com/bb36f739e7e0a3722beeb2744744195c22fd6143/third_party/blink/web_tests/external/wpt/webusb/usbDevice.https.any.js
[modify] https://crrev.com/bb36f739e7e0a3722beeb2744744195c22fd6143/third_party/blink/renderer/modules/webusb/usb_device.cc


### ma...@google.com (2023-10-20)

Requesting merge to 119 Beta

### [Deleted User] (2023-10-21)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-21)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-21)

Merge review required: M119 is already shipping to beta.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: eakpobaro (Android), eakpobaro (iOS), dgagnon (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-10-23)

hi mattreynolds@ -- thank you for fixing this issue. In the future, please simply update security bugs as Fixed once the resolving CLs are landed. This allows the bot to make the appropriate merge requests based on severity and impact. 
Given this, I've noticed that you have only requested merge to 119 beta. Last 119 beta cut is EOD tomorrow for release on Wednesday, but that RC is also being used for Early Stable. Please confirm there are not compatibility or stability risk with backmerge given this fix will go out in a Stable RC. 

Additionally, since this is a sev-high issue, it should also be backmerged to M118, which will be promoted to Extended Stable support next week. I have added that merge label. 

### ma...@google.com (2023-10-24)

> lease confirm there are not compatibility or stability risk with backmerge given this fix will go out in a Stable RC.

There's no compatibility or stability risk.

### am...@chromium.org (2023-10-24)

thank you for confirming 
119 and 118 merges approved for https://crrev.com/c/4944690
please merge this fix to 119 / branch 6045 by EOD today so this fix can be included in last 119 Beta (and 119 Early Stable) 
please merge this fix to branch 118 / 5993 at your convenience (but by EOD Friday 27 October) so this fix can be included in the first 118 Extended Stable release 

### gi...@appspot.gserviceaccount.com (2023-10-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/e5b53ae92f46bcf59c4582eae115c151967a39eb

commit e5b53ae92f46bcf59c4582eae115c151967a39eb
Author: Matt Reynolds <mattreynolds@google.com>
Date: Tue Oct 24 23:37:33 2023

[M-119] usb: Validate isochronous transfer packet lengths

USBDevice.isochronousTransferIn and
USBDevice.isochronousTransferOut take a parameter containing
a list of packet lengths. This CL adds validation that the
total packet length does not exceed the maximum buffer size.
For isochronousTransferOut, it also checks that the total
length of all packets in bytes is equal to the size of the
data buffer.

Passing invalid packet lengths causes the promise to be
rejected with a DataError.

(cherry picked from commit bb36f739e7e0a3722beeb2744744195c22fd6143)

Bug: 1492381, 1492384
Change-Id: Id9ae16c7e6f1c417e0fc4f21d53e9de11560b2b7
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4944690
Reviewed-by: Reilly Grant <reillyg@chromium.org>
Commit-Queue: Matt Reynolds <mattreynolds@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1212916}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4973819
Reviewed-by: Erhu Akpobaro <eakpobaro@google.com>
Cr-Commit-Position: refs/branch-heads/6045@{#925}
Cr-Branched-From: 905e8bdd32d891451d94d1ec71682e989da2b0a1-refs/heads/main@{#1204232}

[modify] https://crrev.com/e5b53ae92f46bcf59c4582eae115c151967a39eb/services/device/usb/mojo/device_impl_unittest.cc
[modify] https://crrev.com/e5b53ae92f46bcf59c4582eae115c151967a39eb/services/device/usb/mojo/device_impl.cc
[modify] https://crrev.com/e5b53ae92f46bcf59c4582eae115c151967a39eb/third_party/blink/web_tests/external/wpt/webusb/usbDevice.https.any.js
[modify] https://crrev.com/e5b53ae92f46bcf59c4582eae115c151967a39eb/third_party/blink/renderer/modules/webusb/usb_device.cc


### [Deleted User] (2023-10-24)

LTS Milestone M114

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ma...@google.com (2023-10-25)

1. Was this issue a regression for the milestone it was found in?

No

2. Is this issue related to a change or feature merged after the latest LTS Milestone?

No

### gi...@appspot.gserviceaccount.com (2023-10-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/80106e31c7ea8b38bfe9452879287edbcd8a3f3b

commit 80106e31c7ea8b38bfe9452879287edbcd8a3f3b
Author: Matt Reynolds <mattreynolds@google.com>
Date: Wed Oct 25 00:56:26 2023

[M-118] usb: Validate isochronous transfer packet lengths

USBDevice.isochronousTransferIn and
USBDevice.isochronousTransferOut take a parameter containing
a list of packet lengths. This CL adds validation that the
total packet length does not exceed the maximum buffer size.
For isochronousTransferOut, it also checks that the total
length of all packets in bytes is equal to the size of the
data buffer.

Passing invalid packet lengths causes the promise to be
rejected with a DataError.

(cherry picked from commit bb36f739e7e0a3722beeb2744744195c22fd6143)

Bug: 1492381, 1492384
Change-Id: Id9ae16c7e6f1c417e0fc4f21d53e9de11560b2b7
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4944690
Reviewed-by: Reilly Grant <reillyg@chromium.org>
Commit-Queue: Matt Reynolds <mattreynolds@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1212916}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4974416
Commit-Queue: Reilly Grant <reillyg@chromium.org>
Auto-Submit: Matt Reynolds <mattreynolds@chromium.org>
Cr-Commit-Position: refs/branch-heads/5993@{#1425}
Cr-Branched-From: 511350718e646be62331ae9d7213d10ec320d514-refs/heads/main@{#1192594}

[modify] https://crrev.com/80106e31c7ea8b38bfe9452879287edbcd8a3f3b/services/device/usb/mojo/device_impl_unittest.cc
[modify] https://crrev.com/80106e31c7ea8b38bfe9452879287edbcd8a3f3b/services/device/usb/mojo/device_impl.cc
[modify] https://crrev.com/80106e31c7ea8b38bfe9452879287edbcd8a3f3b/third_party/blink/web_tests/external/wpt/webusb/usbDevice.https.any.js
[modify] https://crrev.com/80106e31c7ea8b38bfe9452879287edbcd8a3f3b/third_party/blink/renderer/modules/webusb/usb_device.cc


### am...@google.com (2023-10-26)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-10-26)

Congratulations DarkNavy! The VRP Panel has decided to award you $10,000 for this report of a $10,000 for this report of a OOB read resulting in information disclosure + $1,000 bisect bonus. A member of our finance team will be in touch with you soon to arrange payment. Thank you for your efforts and reporting this issue to us -- nice work!  

### rz...@google.com (2023-10-26)

[Empty comment from Monorail migration]

### rz...@google.com (2023-10-27)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-27)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2023-10-27)

1. Just https://chromium-review.googlesource.com/q/topic:%225735_301111340%22
2. Low, just a couple of simple conflicts
3. 118, 119
4. Yes

### gm...@google.com (2023-10-27)

[Empty comment from Monorail migration]

### am...@google.com (2023-10-28)

[Empty comment from Monorail migration]

### pg...@google.com (2023-10-30)

[Empty comment from Monorail migration]

### pg...@google.com (2023-11-01)

[Empty comment from Monorail migration]

### pg...@google.com (2023-11-01)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-11-02)

[Empty comment from Monorail migration]

### na...@google.com (2023-11-02)

[Empty comment from Monorail migration]

### rz...@google.com (2023-11-03)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-27)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2024-01-27)

This issue was migrated from crbug.com/chromium/1492381?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1492382, crbug.com/chromium/1492384]
[Monorail components added to Component Tags custom field.]

### rz...@google.com (2024-03-11)

It looks like that automation isn't working for the LTS questionnaire, I will add the answers below:

1: <https://crrev.com/c/4979997>
2: Low, only a simple conflict
3: 118, 119
4: Yes

### ap...@google.com (2024-03-26)

Project: chromium/src
Branch: refs/branch-heads/5735

commit cde68978ec9a5d7546a75482ec4f927db5674651
Author: Matt Reynolds <mattreynolds@google.com>
Date:   Tue Mar 26 16:11:48 2024

    [M114-LTS] usb: Validate isochronous transfer packet lengths
    
    M114 merge issues:
      third_party/blink/renderer/modules/webusb/usb_device.cc:
        The data.ByteLength check after the data.IsDetached() check isn't present in
        the original change code. Kept the 114 version and added the new lines.
    
    USBDevice.isochronousTransferIn and
    USBDevice.isochronousTransferOut take a parameter containing
    a list of packet lengths. This CL adds validation that the
    total packet length does not exceed the maximum buffer size.
    For isochronousTransferOut, it also checks that the total
    length of all packets in bytes is equal to the size of the
    data buffer.
    
    Passing invalid packet lengths causes the promise to be
    rejected with a DataError.
    
    (cherry picked from commit bb36f739e7e0a3722beeb2744744195c22fd6143)
    
    Bug: 1492381, 1492384
    Change-Id: Id9ae16c7e6f1c417e0fc4f21d53e9de11560b2b7
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4944690
    Commit-Queue: Matt Reynolds <mattreynolds@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1212916}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4979997
    Owners-Override: Michael Ershov <miersh@google.com>
    Reviewed-by: Matt Reynolds <mattreynolds@chromium.org>
    Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
    Reviewed-by: Michael Ershov <miersh@google.com>
    Cr-Commit-Position: refs/branch-heads/5735@{#1714}
    Cr-Branched-From: 2f562e4ddbaf79a3f3cb338b4d1bd4398d49eb67-refs/heads/main@{#1135570}

M       services/device/usb/mojo/device_impl.cc
M       services/device/usb/mojo/device_impl_unittest.cc
M       third_party/blink/renderer/modules/webusb/usb_device.cc
M       third_party/blink/web_tests/external/wpt/webusb/usbDevice.https.any.js

https://chromium-review.googlesource.com/4979997


---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40074792)*
