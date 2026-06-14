# Security: Heap-use-after-free in UsbChooserController::DisplayDevice

| Field | Value |
|-------|-------|
| **Issue ID** | [40086940](https://issues.chromium.org/issues/40086940) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>USB |
| **Platforms** | Windows |
| **Reporter** | ch...@gmail.com |
| **Assignee** | re...@chromium.org |
| **Created** | 2017-03-01 |
| **Bounty** | $5,000.00 |

## Description

Chrome Version: 58.0.3027.0 (Official Build) canary (64-bit)
Operating System: Windows 7

- Run chrome with --enable-experimental-web-platform-features flag.

rax=0000000000000000 rbx=000000000eb684c0 rcx=feeefeeefeeefeee
rdx=000000000031ec38 rsi=000000000031ed20 rdi=000000000bd8bb20
rip=000007fee1363c70 rsp=000000000031ec10 rbp=000000000031ed80
 r8=000000000ba03ae0  r9=0000000000008086 r10=0000000000003b34
r11=0000000000000000 r12=000000000031f070 r13=00000000025bae00
r14=0000000000000001 r15=0000000000000001
iopl=0         nv up ei pl nz na po nc
cs=0033  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00010206
chrome_7fedf610000!UsbChooserController::DisplayDevice+0xf0:
000007fe`e1363c70 488b01          mov     rax,qword ptr [rcx] ds:feeefeee`feeefeee=????????????????
0:000> k
Child-SP          RetAddr           Call Site
00000000`0031ec10 000007fe`e1363a67 chrome_7fedf610000!UsbChooserController::DisplayDevice+0xf0 [c:\b\build\slave\win64-pgo\build\src\chrome\browser\usb\usb_chooser_controller.cc @ 232]
00000000`0031ed00 000007fe`df992e98 chrome_7fedf610000!UsbChooserController::GotUsbDeviceList+0x67 [c:\b\build\slave\win64-pgo\build\src\chrome\browser\usb\usb_chooser_controller.cc @ 212]
00000000`0031eda0 000007fe`e096049b chrome_7fedf610000!base::internal::Invoker<base::internal::BindState<void (__cdecl content::AppCacheURLRequestJob::*)(content::AppCacheExecutableHandler::Response const & __ptr64) __ptr64,base::WeakPtr<content::AppCacheURLRequestJob> >,void __cdecl(content::AppCacheExecutableHandler::Response const & __ptr64)>::Run+0x48 [c:\b\build\slave\win64-pgo\build\src\base\bind_internal.h @ 343]
00000000`0031ede0 000007fe`df7cc876 chrome_7fedf610000!device::UsbServiceImpl::RefreshDevicesComplete+0x14b [c:\b\build\slave\win64-pgo\build\src\device\usb\usb_service_impl.cc @ 415]
00000000`0031ee40 000007fe`e000fa77 chrome_7fedf610000!base::internal::Invoker<base::internal::BindState<void (__cdecl media::AudioInputController::*)(void) __ptr64,base::WeakPtr<media::AudioInputController> >,void __cdecl(void)>::Run+0x46 [c:\b\build\slave\win64-pgo\build\src\base\bind_internal.h @ 343]
00000000`0031ee80 000007fe`e0961bc3 chrome_7fedf610000!`anonymous namespace'::BarrierInfo::Run+0x57 [c:\b\build\slave\win64-pgo\build\src\base\barrier_closure.cc @ 34]
00000000`0031eeb0 000007fe`e095f41d chrome_7fedf610000!base::internal::Invoker<base::internal::BindState<void (__cdecl device::UsbServiceImpl::*)(libusb_device * __ptr64,base::Callback<void __cdecl(void),1,1> const & __ptr64) __ptr64,base::WeakPtr<device::UsbServiceImpl>,libusb_device * __ptr64,base::Callback<void __cdecl(void),1,1> >,void __cdecl(void)>::Run+0x53 [c:\b\build\slave\win64-pgo\build\src\base\bind_internal.h @ 343]
00000000`0031eef0 000007fe`e0961b63 chrome_7fedf610000!device::`anonymous namespace'::OnDeviceOpenedReadDescriptors+0x4cd [c:\b\build\slave\win64-pgo\build\src\device\usb\usb_service_impl.cc @ 215]
00000000`0031f020 000007fe`e096ab9b chrome_7fedf610000!base::internal::Invoker<base::internal::BindState<void (__cdecl*)(unsigned char,unsigned char,unsigned char,bool,base::Callback<void __cdecl(void),1,1> const & __ptr64,base::Callback<void __cdecl(void),1,1> const & __ptr64,scoped_refptr<device::UsbDeviceHandle>),unsigned char,unsigned char,unsigned char,bool,base::Callback<void __cdecl(void),1,1>,base::Callback<void __cdecl(void),1,1> >,void __cdecl(scoped_refptr<device::UsbDeviceHandle>)>::Run+0x43 [c:\b\build\slave\win64-pgo\build\src\base\bind_internal.h @ 343]
00000000`0031f070 000007fe`dfa32c74 chrome_7fedf610000!base::internal::Invoker<base::internal::BindState<base::Callback<void __cdecl(scoped_refptr<device::UsbDeviceHandle>),1,1>,std::nullptr_t>,void __cdecl(void)>::Run+0x3b [c:\b\build\slave\win64-pgo\build\src\base\bind_internal.h @ 339]
00000000`0031f0a0 000007fe`e004a093 chrome_7fedf610000!base::internal::RunMixin<base::Callback<void __cdecl(void),0,0> >::Run+0x24 [c:\b\build\slave\win64-pgo\build\src\base\callback.h @ 68]
00000000`0031f0d0 000007fe`dfff9256 chrome_7fedf610000!base::debug::TaskAnnotator::RunTask+0x183 [c:\b\build\slave\win64-pgo\build\src\base\debug\task_annotator.cc @ 61]
00000000`0031f260 000007fe`dfff9e0a chrome_7fedf610000!base::MessageLoop::RunTask+0x1f6 [c:\b\build\slave\win64-pgo\build\src\base\message_loop\message_loop.cc @ 424]
00000000`0031f3c0 000007fe`e004a601 chrome_7fedf610000!base::MessageLoop::DoWork+0x48a [c:\b\build\slave\win64-pgo\build\src\base\message_loop\message_loop.cc @ 527]
00000000`0031f5c0 000007fe`e004a254 chrome_7fedf610000!base::MessagePumpForUI::DoRunLoop+0x71 [c:\b\build\slave\win64-pgo\build\src\base\message_loop\message_pump_win.cc @ 174]
00000000`0031f630 000007fe`e0020ed0 chrome_7fedf610000!base::MessagePumpWin::Run+0x54 [c:\b\build\slave\win64-pgo\build\src\base\message_loop\message_pump_win.cc @ 58]
00000000`0031f680 000007fe`dff268d8 chrome_7fedf610000!base::RunLoop::Run+0xc0 [c:\b\build\slave\win64-pgo\build\src\base\run_loop.cc @ 38]
00000000`0031f730 000007fe`df9bf28c chrome_7fedf610000!ChromeBrowserMainParts::MainMessageLoopRun+0x138 [c:\b\build\slave\win64-pgo\build\src\chrome\browser\chrome_browser_main.cc @ 2004]
00000000`0031f7b0 000007fe`df9b737c chrome_7fedf610000!content::BrowserMainRunnerImpl::Run+0x6c [c:\b\build\slave\win64-pgo\build\src\content\browser\browser_main_runner.cc @ 140]
00000000`0031f800 000007fe`dfed7e73 chrome_7fedf610000!content::BrowserMain+0x17c [c:\b\build\slave\win64-pgo\build\src\content\browser\browser_main.cc @ 49]


## Attachments

- [repro.html](attachments/repro.html) (text/plain, 849 B)
- [heap-use-after-free on address 0x1b50cd9c](attachments/heap-use-after-free on address 0x1b50cd9c) (text/plain, 10.3 KB)
- [Rec.mp4](attachments/Rec.mp4) (video/mp4, 201.1 KB)

## Timeline

### va...@chromium.org (2017-03-01)

[Empty comment from Monorail migration]

[Monorail components: Blink>USB]

### cl...@chromium.org (2017-03-01)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=4761348220387328

### cl...@chromium.org (2017-03-01)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=6719977190326272

### va...@chromium.org (2017-03-02)

I was able to reproduce this locally: crash/e2db8459c0000000 (and may be crash/7fe65459c0000000)

Marking as low severity since it requires using a command line switch.

### va...@chromium.org (2017-03-02)

[Empty comment from Monorail migration]

### ch...@gmail.com (2017-03-02)

In https://crbug.com/chromium/690775 it requires using the same command line and it Marked as high severity.

### re...@chromium.org (2017-03-02)

If the page has an Origin Trial key for the WebUSB feature then the command line flag is not necessary.

### re...@chromium.org (2017-03-02)

What is going on here is a race between the destruction of the RenderFrameHost associated with the popup window when the page calls Window.close() and the destruction of the UsbChooserController associated with the permission bubble created by calling navigator.usb.requestDevice(). If some action occurs, such as the list of USB devices being populated, after the RFH is destroyed and before the controller is destroyed then the controller accesses the freed RFH pointer.

This race shouldn't exist because the chooser bubble should be automatically dismissed before the RFH is destroyed but RenderFrameHost destruction is complicated.

### sh...@chromium.org (2017-03-02)

[Empty comment from Monorail migration]

### re...@chromium.org (2017-03-03)

Further investigation indicates that while the ChooserBubbleDelegate is destroyed when all of the bubbles associated with an RFH are closed the UsbChooserController, which is owned by classes deep within Views, is not.

Note to myself for tomorrow, work with msw@ to understand what the ownership model and widget destruction order here should be as I am not familiar enough with Views.

### bu...@chromium.org (2017-03-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/692db28a688889a7946b04debfd890673ae2269f

commit 692db28a688889a7946b04debfd890673ae2269f
Author: reillyg <reillyg@chromium.org>
Date: Mon Mar 06 23:00:42 2017

Force chooser bubbles to close synchronously.

This fixes a potential use-after-free because UsbChooserController holds
a raw pointer to the RenderFrameHost and so must be destroyed as part of
RenderFrameHost destruction.

BUG=697486

Review-Url: https://codereview.chromium.org/2724903008
Cr-Commit-Position: refs/heads/master@{#454989}

[modify] https://crrev.com/692db28a688889a7946b04debfd890673ae2269f/chrome/browser/ui/views/website_settings/chooser_bubble_ui_view.cc
[modify] https://crrev.com/692db28a688889a7946b04debfd890673ae2269f/chrome/browser/ui/views/website_settings/chooser_bubble_ui_view.h


### re...@chromium.org (2017-03-06)

[Empty comment from Monorail migration]

### ch...@gmail.com (2017-03-06)

[Comment Deleted]

### sh...@chromium.org (2017-03-07)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-03-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/5e296353d65aef23ed1b524a4c1b01e568f6c3cd

commit 5e296353d65aef23ed1b524a4c1b01e568f6c3cd
Author: reillyg <reillyg@chromium.org>
Date: Tue Mar 07 16:06:21 2017

Revert of Force chooser bubbles to close synchronously. (patchset #3 id:40001 of https://codereview.chromium.org/2724903008/ )

Reason for revert:
Reverting this patchset because it was insufficiently tested and introduced a new bug.

Original issue's description:
> Force chooser bubbles to close synchronously.
>
> This fixes a potential use-after-free because UsbChooserController holds
> a raw pointer to the RenderFrameHost and so must be destroyed as part of
> RenderFrameHost destruction.
>
> BUG=697486
>
> Review-Url: https://codereview.chromium.org/2724903008
> Cr-Commit-Position: refs/heads/master@{#454989}
> Committed: https://chromium.googlesource.com/chromium/src/+/692db28a688889a7946b04debfd890673ae2269f

TBR=msw@chromium.org
# Skipping CQ checks because original CL landed less than 1 days ago.
NOPRESUBMIT=true
NOTREECHECKS=true
NOTRY=true
BUG=697486,698927

Review-Url: https://codereview.chromium.org/2736793003
Cr-Commit-Position: refs/heads/master@{#455086}

[modify] https://crrev.com/5e296353d65aef23ed1b524a4c1b01e568f6c3cd/chrome/browser/ui/views/website_settings/chooser_bubble_ui_view.cc
[modify] https://crrev.com/5e296353d65aef23ed1b524a4c1b01e568f6c3cd/chrome/browser/ui/views/website_settings/chooser_bubble_ui_view.h


### re...@chromium.org (2017-03-07)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-03-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/f50d8d33c5da873242189cf73176d78a48549762

commit f50d8d33c5da873242189cf73176d78a48549762
Author: reillyg <reillyg@chromium.org>
Date: Tue Mar 14 22:55:00 2017

Remove RenderFrameHost pointer from ChooserController.

This change removes the raw RenderFrameHost pointer from
ChooserController and instead either computes necessary values (such as
the title) at construction time or stores a weak pointer to the object
derived from the RenderFrameHost.

BUG=697486

Review-Url: https://codereview.chromium.org/2746313002
Cr-Commit-Position: refs/heads/master@{#456876}

[modify] https://crrev.com/f50d8d33c5da873242189cf73176d78a48549762/chrome/browser/chooser_controller/chooser_controller.cc
[modify] https://crrev.com/f50d8d33c5da873242189cf73176d78a48549762/chrome/browser/chooser_controller/chooser_controller.h
[modify] https://crrev.com/f50d8d33c5da873242189cf73176d78a48549762/chrome/browser/chooser_controller/mock_chooser_controller.cc
[modify] https://crrev.com/f50d8d33c5da873242189cf73176d78a48549762/chrome/browser/chooser_controller/mock_chooser_controller.h
[modify] https://crrev.com/f50d8d33c5da873242189cf73176d78a48549762/chrome/browser/ui/android/usb_chooser_dialog_android.cc
[modify] https://crrev.com/f50d8d33c5da873242189cf73176d78a48549762/chrome/browser/ui/cocoa/extensions/chooser_dialog_cocoa_controller_unittest.mm
[modify] https://crrev.com/f50d8d33c5da873242189cf73176d78a48549762/chrome/browser/ui/views/device_chooser_content_view_unittest.cc
[modify] https://crrev.com/f50d8d33c5da873242189cf73176d78a48549762/chrome/browser/ui/views/extensions/chooser_dialog_view_unittest.cc
[modify] https://crrev.com/f50d8d33c5da873242189cf73176d78a48549762/chrome/browser/usb/usb_chooser_context.cc
[modify] https://crrev.com/f50d8d33c5da873242189cf73176d78a48549762/chrome/browser/usb/usb_chooser_context.h
[modify] https://crrev.com/f50d8d33c5da873242189cf73176d78a48549762/chrome/browser/usb/usb_chooser_controller.cc
[modify] https://crrev.com/f50d8d33c5da873242189cf73176d78a48549762/chrome/browser/usb/usb_chooser_controller.h
[modify] https://crrev.com/f50d8d33c5da873242189cf73176d78a48549762/chrome/browser/usb/web_usb_permission_provider.cc
[modify] https://crrev.com/f50d8d33c5da873242189cf73176d78a48549762/chrome/browser/usb/web_usb_permission_provider.h
[modify] https://crrev.com/f50d8d33c5da873242189cf73176d78a48549762/device/usb/webusb_descriptors.cc
[modify] https://crrev.com/f50d8d33c5da873242189cf73176d78a48549762/device/usb/webusb_descriptors.h


### re...@chromium.org (2017-03-14)

[Empty comment from Monorail migration]

### ms...@chromium.org (2017-03-14)

You might need to keep the status as Started to get merge-request attention (not sure).

### sh...@chromium.org (2017-03-15)

This bug requires manual review: Reverts referenced in bugdroid comments after merge request.
Please contact the milestone owner if you have questions.
Owners: amineer@(Android), cmasso@(iOS), bhthompson@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@google.com (2017-03-21)

We just let low severity roll into the next release without merges.  Please re-request a merge if you've a reason to believe this is a higher severity.

### ch...@gmail.com (2017-03-21)

It could be medium severity as https://crbug.com/chromium/698927.

### aw...@google.com (2017-03-31)

[Empty comment from Monorail migration]

### aw...@google.com (2017-04-05)

Changing to High per discussion at the VRP panel.

### aw...@google.com (2017-04-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-04-05)

This bug requires manual review: Reverts referenced in bugdroid comments after merge request.
Please contact the milestone owner if you have questions.
Owners: amineer@(Android), cmasso@(iOS), bhthompson@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2017-04-06)

+ awhalley@ for M58 merge review

### aw...@google.com (2017-04-06)

govind@ - Good for 58

### go...@chromium.org (2017-04-06)

Approving merge to M58 branch 3029 based on https://crbug.com/chromium/697486#c29. Please merge ASAP. Thank you.

### bu...@chromium.org (2017-04-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/7832e106ed7e343da9583d92f325faa5bc21a2ae

commit 7832e106ed7e343da9583d92f325faa5bc21a2ae
Author: Reilly Grant <reillyg@chromium.org>
Date: Thu Apr 06 21:43:21 2017

Remove RenderFrameHost pointer from ChooserController.

This change removes the raw RenderFrameHost pointer from
ChooserController and instead either computes necessary values (such as
the title) at construction time or stores a weak pointer to the object
derived from the RenderFrameHost.

BUG=697486

Review-Url: https://codereview.chromium.org/2746313002
Cr-Commit-Position: refs/heads/master@{#456876}
(cherry picked from commit f50d8d33c5da873242189cf73176d78a48549762)

Review-Url: https://codereview.chromium.org/2806603002 .
Cr-Commit-Position: refs/branch-heads/3029@{#616}
Cr-Branched-From: 939b32ee5ba05c396eef3fd992822fcca9a2e262-refs/heads/master@{#454471}

[modify] https://crrev.com/7832e106ed7e343da9583d92f325faa5bc21a2ae/chrome/browser/chooser_controller/chooser_controller.cc
[modify] https://crrev.com/7832e106ed7e343da9583d92f325faa5bc21a2ae/chrome/browser/chooser_controller/chooser_controller.h
[modify] https://crrev.com/7832e106ed7e343da9583d92f325faa5bc21a2ae/chrome/browser/chooser_controller/mock_chooser_controller.cc
[modify] https://crrev.com/7832e106ed7e343da9583d92f325faa5bc21a2ae/chrome/browser/chooser_controller/mock_chooser_controller.h
[modify] https://crrev.com/7832e106ed7e343da9583d92f325faa5bc21a2ae/chrome/browser/ui/android/usb_chooser_dialog_android.cc
[modify] https://crrev.com/7832e106ed7e343da9583d92f325faa5bc21a2ae/chrome/browser/ui/cocoa/extensions/chooser_dialog_cocoa_controller_unittest.mm
[modify] https://crrev.com/7832e106ed7e343da9583d92f325faa5bc21a2ae/chrome/browser/ui/views/device_chooser_content_view_unittest.cc
[modify] https://crrev.com/7832e106ed7e343da9583d92f325faa5bc21a2ae/chrome/browser/ui/views/extensions/chooser_dialog_view_unittest.cc
[modify] https://crrev.com/7832e106ed7e343da9583d92f325faa5bc21a2ae/chrome/browser/usb/usb_chooser_context.cc
[modify] https://crrev.com/7832e106ed7e343da9583d92f325faa5bc21a2ae/chrome/browser/usb/usb_chooser_context.h
[modify] https://crrev.com/7832e106ed7e343da9583d92f325faa5bc21a2ae/chrome/browser/usb/usb_chooser_controller.cc
[modify] https://crrev.com/7832e106ed7e343da9583d92f325faa5bc21a2ae/chrome/browser/usb/usb_chooser_controller.h
[modify] https://crrev.com/7832e106ed7e343da9583d92f325faa5bc21a2ae/chrome/browser/usb/web_usb_permission_provider.cc
[modify] https://crrev.com/7832e106ed7e343da9583d92f325faa5bc21a2ae/chrome/browser/usb/web_usb_permission_provider.h
[modify] https://crrev.com/7832e106ed7e343da9583d92f325faa5bc21a2ae/device/usb/webusb_descriptors.cc
[modify] https://crrev.com/7832e106ed7e343da9583d92f325faa5bc21a2ae/device/usb/webusb_descriptors.h


### aw...@chromium.org (2017-04-10)

[Empty comment from Monorail migration]

### aw...@google.com (2017-04-10)

Very nice - the panel decided to award $5,000 for this bug!

### aw...@chromium.org (2017-04-10)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-06-21)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-07-28)

[Empty comment from Monorail migration]

### is...@google.com (2018-07-28)

This issue was migrated from crbug.com/chromium/697486?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40086940)*
