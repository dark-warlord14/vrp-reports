# Security: A UAF in WebRTC

| Field | Value |
|-------|-------|
| **Issue ID** | [40062915](https://issues.chromium.org/issues/40062915) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebRTC, Internals>Media>ScreenCapture |
| **Platforms** | Windows |
| **Reporter** | om...@talon-sec.com |
| **Assignee** | al...@chromium.org |
| **Created** | 2023-02-04 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

The bug is triggered in `third_party\webrtc\modules\desktop_capture\win\wgc_capture_session.cc` in the `OnItemClosed` method causing the browser process to crash.

This method is being called from a message pumping thread (`DesktopMediaListCaptureThread`) as you can see the crash dump, and in case a video session is shutting down because the captured window is closed, there is a race between the COM thread and our thread that can lead to `OnItemClosed` being called on a freed `WgcCaptureSession`.

The problem starts in `CreateDispatcherQueueController` function that is being called on `third_party\webrtc\modules\desktop_capture\win\wgc_capturer_win.cc`.  

According to the MSDN, it creates a background COM thread that send messages to our message pumping thread. When a window is closed, it can be that `WgcCaptureSession` get destroyed (because of `ongoing_captures_.erase(capture_source_->GetSourceId());` when `GetFrame` from this window fails, or if the video session is closed by the user) while the COM thread tries to send a message (before `item_->remove_Closed` is called in `RemoveEventHandlers`) that will make `OnItemClosed` eventually be called in `DesktopMediaListCaptureThread` on freed `WgcCaptureSession`.

**VERSION**  

Chrome Version: 109.0.5414.120 (stable)  

Operating System: Windows

**REPRODUCTION CASE**  

We need to close a native window while it is being captured with `WgcCapturerWin` to trigger the race.  

There are 2 classes that webrtc uses to capture video in Windows:  

`WindowCapturerWinGdi` (primary) and `WgcCapturerWin` (secondary). It always start with `WindowCapturerWinGdi`, and only if it fails it falls back to `WgcCapturerWin`. It is decided in `FallbackDesktopCapturerWrapper::CaptureFrame`.

So our target is to make `WindowCapturerWinGdi` fail. But it is fairly easy task. In `WindowCapturerWinGdi::CaptureFrame` there is a check `IsWindow(window_)`  

to see if the windows is still valid before capturing the frame, and if it returns false, we fallback eventually to capture using `WgcCapturerWin`. It means that if we close the captured window before this check, all the next video captures will use `WgcCapturerWin`. We can actually visually see when this transfer between the capturing methods, because when `WgcCapturerWin` is in use, every window has a yellow frame. You can see it in the poc video.  

Now, we need to close any captured native window and the race occurs.

The way I reproduce the whole thing is with the screenshare window picker. No permission is needed from the user to show the window picker.  

The picker is good spot because it captures a video for each window in the system to show it in the thumbnails.

The POC is done with python on Windows 11 VM (with 8GB ram + 4 cpus). To run it just open 'poc.html' and run 'python poc.py' (notice that the bug is statistic, so maybe you need to increase the number of notepads to see a crash). The poc steps include:

- Create some notepad processes.
- Open the window picker for screensharing.
- Close the notepads in random timing, which cause at one point to move from  
  
  `WindowCapturerWinGdi` to `WgcCapturerWin`. It Can be visually confirmed by  
  
  the windows yellow border.
- Create some more notepads.
- Close them all at once and hope for the crash when `OnItemClosed` is called.

Some notes:

- I noticed weird behavior on my physical computer while reproducing this bug on  
  
  it. For example, sometimes the yellow border stayed around some windows after  
  
  chrome was terminated, or that the Screen Snipping tool (winkey+shift+s)  
  
  stopped working because it was crashing every time I tried to use it  
  
  afterwards. I attach a dump of that process crash too.
- I got another crash that doesn't show `OnItemClosed` in the stacktrace one  
  
  time. Not sure what happened there but it also looks like UAF on  
  
  `WgcCaptureSession`.
- If an attacker can create native windows from JS somehow, it can be pretty  
  
  straightforward to cause the crash. For example, using ctrl+shift+p show the  
  
  native printing window which can also be captured and trigger this bug  
  
  (although it's not possible to show it from js without `--disable-print- preview` AFAIK).

Suggested solution:

- To not use `OnItemClosed` at all and to check `IsWindow()` or any other way to  
  
  verify the capture window is still valid before capturing a frame.
- Need to check if `OnFrameArrived` can suffer from the same race problem.

Type of crash: browser  

Crash State:  

CONTEXT: (.ecxr)  

rax=0000000000000001 rbx=0000007ec79fc600 rcx=0000000000000007  

rdx=000000000000000f rsi=0000007ec79fbc60 rdi=0000000000000000  

rip=00007fff87badd7e rsp=0000007ec79fb340 rbp=0000007ec79fb4a0  

r8=0000000000000006 r9=0000007ec79fb2e8 r10=0000000000000017  

r11=0000000800800000 r12=0000000000000000 r13=0000007ec79fbe40  

r14=0000007ec79fb650 r15=0000007ec79fb680  

iopl=0 nv up ei pl nz na pe nc  

cs=0033 ss=0000 ds=0000 es=0000 fs=0053 gs=002b efl=00000202  

ucrtbase!abort+0x4e:  

00007fff`87badd7e cd29 int 29h  

Resetting default scope

EXCEPTION\_RECORD: (.exr -1)  

ExceptionAddress: 00007fff87badd7e (ucrtbase!abort+0x000000000000004e)  

ExceptionCode: c0000409 (Security check failure or stack buffer overrun)  

ExceptionFlags: 00000001  

NumberParameters: 1  

Parameter[0]: 0000000000000007  

Subcode: 0x7 FAST\_FAIL\_FATAL\_APP\_EXIT

PROCESS\_NAME: chrome.exe

ERROR\_CODE: (NTSTATUS) 0xc0000409 - The system detected an overrun of a stack-based buffer in this application. This overrun could potentially allow a malicious user to gain control of this application.

EXCEPTION\_CODE\_STR: c0000409

EXCEPTION\_PARAMETER1: 0000000000000007

STACK\_TEXT:  

0000007e`c79fb340 00007fff`87bad499 : 0000007e`00000003 0000007e`00000003 00000000`00000000 00000000`00000000 : ucrtbase!abort+0x4e  

0000007e`c79fb370 00007fff`87b736c0 : 0000007e`c79fc600 0000007e`c79fbc60 0000007e`c79fb650 0000007e`c79fb650 : ucrtbase!terminate+0x29  

0000007e`c79fb3a0 00007fff`87b7432e : 00000000`00000000 00007fff`876ee2cb 00000000`00000006 0000007e`c79fc600 : ucrtbase!FindHandler<\_\_FrameHandler4>+0x508  

0000007e`c79fb570 00007fff`87b72159 : 00007fff`74740000 0000007e`c79fc600 0000007e`c79fbe40 0000007e`c79fbc60 : ucrtbase!\_\_InternalCxxFrameHandler<\_\_FrameHandler4>+0x276  

0000007e`c79fb610 00007fff`8a068b1f : 0000007e`c79fea20 00000000`00000000 0000007e`c79fbc10 0000007e`c79fc600 : ucrtbase!\_CxxFrameHandler4+0xa9  

0000007e`c79fb680 00007fff`89ff5b9a : 0000007e`c79fc600 00007fff`74740000 00007fff`7474f2ee 00007fff`74769dd4 : ntdll!RtlpExecuteHandlerForException+0xf  

0000007e`c79fb6b0 00007fff`89ff2e63 : 00000000`00000000 0000007e`c79fc4b0 00000000`00000000 00007fff`89ff2dcf : ntdll!RtlDispatchException+0x25a  

0000007e`c79fbe00 00007fff`876e441c : 000097dd`2356f45e 0000007e`c79fe070 0000007e`c79fe830 00007fff`87b7221a : ntdll!RtlRaiseException+0x163  

0000007e`c79fc5e0 00007fff`87b74980 : 00007fff`7475d83b 0000007e`c79fd5d8 00000000`00000100 00000000`00000000 : KERNELBASE!RaiseException+0x6c  

0000007e`c79fc6c0 00007fff`8a068386 : 00007fff`00000001 00000000`00000002 0000007e`00000000 0000007e`c79fe830 : ucrtbase!\_\_FrameHandler4::CxxCallCatchBlock+0x1b0  

0000007e`c79fc7a0 00007fff`74752cfe : 0000027d`6d4785d8 00000000`00000000 0000027d`6d4e46b0 0000027d`66a30000 : ntdll!RcConsolidateFrames+0x6  

0000007e`c79fe9d0 00007fff`7474f2ee : 0000027d`6e2d5670 0000027d`6e2d56a0 0000027d`6e2d56a0 0000027d`6e2d5670 : GraphicsCapture!winrt::Windows::Graphics::Capture::implementation::GraphicsCaptureSession::Close+0x62  

0000007e`c79fea20 00007fff`74750bf2 : 0000027d`6e2d5670 00000000`00000000 0000027d`6d401590 00001d28`037676a8 : GraphicsCapture!winrt::impl::heap\_implements[winrt::Windows::Graphics::Capture::implementation::GraphicsCaptureSession](javascript:void(0);)::`vector deleting destructor'+0x1e 0000007e`c79fea50 00007fff`1e3fdc01 : 00000000`00000000 0000007e`b1876000 0000007e`b1876000 0000007e`c79feb50 : GraphicsCapture!winrt::implements<winrt::Windows::Graphics::Capture::implementation::Direct3D11CaptureFrame,winrt::Windows::Graphics::Capture::Direct3D11CaptureFrame,winrt::Windows::Foundation::IClosable>::Release+0x8a 0000007e`c79fea80 00007fff`7475831f : 00000000`00000000 0000027d`6d401590 0000027d`6d4633c0 00000000`00000000 : chrome!webrtc::WgcCaptureSession::OnItemClosed+0xb1 0000007e`c79fec00 00007fff`747576c1 : 00001d28`02839300 0000027d`6d4633c0 0000027d`66aa9240 00007fff`74756d10 : GraphicsCapture!winrt::impl::delegate<winrt::Windows::Foundation::TypedEventHandler<winrt::Windows::Graphics::Capture::GraphicsCaptureItem,winrt::Windows::Foundation::IInspectable>,<lambda_476b37be3204c070e6eb795c054f0517> >::Invoke+0x5f 0000007e`c79fec30 00007fff`74756d90 : 0000027d`6d4015a0 00000000`00000000 00000000`00000000 0000027d`6d4432a0 : GraphicsCapture!winrt::impl::invoke<winrt::Windows::Foundation::TypedEventHandler<winrt::Windows::Graphics::Capture::GraphicsCaptureItem,winrt::Windows::Foundation::IInspectable>,winrt::Windows::Graphics::Capture::implementation::GraphicsCaptureItemBase,std::nullptr_t>+0x35 0000007e`c79fec60 00007fff`8481bad3 : 0000007e`c79fed00 0000007e`c79fed28 00007fff`74756d10 0000027d`6d4633c0 : GraphicsCapture!<lambda_311ffe58968c8dd710760cfa38ccf01e>::<lambda_invoker_cdecl>+0x80 0000007e`c79feca0 00007fff`8481b87d : 0000027d`6b2d75e0 00007fff`74756d10 0000027d`6b2d75e0 00007fff`74756d10 : CoreMessaging!CFlat::SehSafe::Execute<<lambda_b6dd2ec3e47633f34c135ea03fcb8644> >+0x3f 0000007e`c79fecd0 00007fff`84861f12 : 0000027d`6d4c37a0 0000027d`00000000 00000000`00001bd4 0000007e`c79fed80 : CoreMessaging!Microsoft::CoreUI::Dispatch::WaitCallback::ImportAdapter$+0xcd 0000007e`c79fed50 00007fff`8483c956 : 0000027d`6b3b41b0 00000000`00000000 00000000`00001bd4 00000000`00000000 : CoreMessaging!Microsoft::CoreUI::Dispatch::RegisteredWait::DoCallback+0x42 0000007e`c79fed80 00007fff`8483c09b : 0000027d`6e3ec780 0000027d`6b3b2f40 0000027d`6e2d7e30 0000027d`6d440bc0 : CoreMessaging!Microsoft::CoreUI::Dispatch::DeferredCall::Callback_Dispatch+0x96 0000007e`c79fee40 00007fff`8483bd1d : 0000027d`00000010 00000000`00000000 00000000`00000001 0000027d`6d440bc0 : CoreMessaging!Microsoft::CoreUI::Dispatch::DeferredCallDispatcher::Callback_OnDispatch+0x12b 0000007e`c79fef00 00007fff`84839313 : 0000027d`6b3b4250 0000027d`6d4432a0 0000027d`6b2d7501 00000000`00000000 : CoreMessaging!Microsoft::CoreUI::Dispatch::EventLoop::Callback_RunCoreLoop+0x2ed 0000007e`c79fefc0 00007fff`84838dec : 0000027d`6b3b3ee0 0000027d`6b3b3ee0 0000027d`6b2d75e0 0000027d`6d4432a0 : CoreMessaging!Microsoft::CoreUI::Dispatch::UserAdapter::OnUserDispatch+0x3e3 0000007e`c79ff050 00007fff`84838a6b : 00000000`00000004 00000000`003106ae 00000000`00000000 0000027d`6b3b33f0 : CoreMessaging!Microsoft::CoreUI::Dispatch::UserAdapter::DoWork+0x1fc 0000007e`c79ff0e0 00007fff`87f21cec : 00000000`00000000 00000000`00000000 00000000`00000001 00000000`00000001 : CoreMessaging!Microsoft::CoreUI::Dispatch::UserAdapter::WindowProc+0x11b 0000007e`c79ff150 00007fff`87f2183c : 00000000`00000000 00007fff`84838950 00000000`003106ae 00000000`00000060 : USER32!UserCallWinProcCheckWow+0x33c 0000007e`c79ff2c0 00007fff`87f34cad : 00000000`00000000 00000000`00000000 00000000`00000001 0000007e`b1876800 : USER32!DispatchClientMessage+0x9c 0000007e`c79ff320 00007fff`8a067ad4 : aaaaaaaa`aaaaaaaa aaaaaaaa`aaaaaaaa aaaaaaaa`00000000 00007fff`19cc4da0 : USER32!_fnDWORD+0x3d 0000007e`c79ff380 00007fff`876713b4 : 00007fff`87f29faf 00000000`00000000 00000000`00000000 408f4000`00000000 : ntdll!KiUserCallbackDispatcherContinue 0000007e`c79ff408 00007fff`87f29faf : 00000000`00000000 00000000`00000000 408f4000`00000000 00000000`00000000 : win32u!NtUserPeekMessage+0x14 0000007e`c79ff410 00007fff`87f29f1a : 00000000`00000001 0000027d`672a1180 00000000`00000000 aaaaaaaa`aaaaaaaa : USER32!_PeekMessage+0x3f 0000007e`c79ff480 00007fff`19cbec06 : 00000000`00000000 00001d28`026ab9d0 00001d28`027759a0 00007fff`19d717f5 : USER32!PeekMessageW+0x13a 0000007e`c79ff4f0 00007fff`15f030c1 : 00001d28`026ab9d8 00007fff`1a9cdda7 0000705d`e58d6a97 0000705d`e58d6ac7 : chrome!base::MessagePumpForUI::DoRunLoop+0x576 0000007e`c79ff6f0 00007fff`1666d42f : 00007fff`2202e2f8 00000000`00000008 00001d28`02f6bc10 00007fff`1a7e3b23 : chrome!base::MessagePumpWin::Run+0x71 0000007e`c79ff750 00007fff`1666efab : 0000705d`e58d6b87 00007fff`87f27164 00000000`00000008 0000007e`c79ff8b8 : chrome!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run+0xdf 0000007e`c79ff7e0 00007fff`16f56da4 : 00000000`0000001d 00007fff`1acb09c7 0000007e`c79ff9a0 00007fff`1666e713 : chrome!base::RunLoop::Run+0x1db 0000007e`c79ff910 00007fff`16f56af9 : 00001d28`02f561c0 00007fff`16854969 00000000`00000000 0000007e`c79ffa40 : chrome!base::Thread::Run+0x44 0000007e`c79ff970 00007fff`168542db : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : chrome!base::Thread::ThreadMain+0x109 0000007e`c79ffa00 00007fff`886655a0 : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : chrome!base::`anonymous namespace'::ThreadFunc+0x11b  

0000007e`c79ffa90 00007fff`89fc485b : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : KERNEL32!BaseThreadInitThunk+0x10  

0000007e`c79ffac0 00000000`00000000 : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : ntdll!RtlUserThreadStart+0x2b

**CREDIT INFORMATION**  

Reporter credit: Omri Bushari (Talon Cyber Security)

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 291 B)
- [poc.py](attachments/poc.py) (text/plain, 797 B)
- [6485e599-2cef-40f9-a9d7-5f99d0b23328.dmp](attachments/6485e599-2cef-40f9-a9d7-5f99d0b23328.dmp) (application/octet-stream, 1.9 MB)
- [36888155-eb11-48fe-9dbb-9ee79f01e0dd.dmp](attachments/36888155-eb11-48fe-9dbb-9ee79f01e0dd.dmp) (application/octet-stream, 1.4 MB)
- [demo.mp4](attachments/demo.mp4) (video/mp4, 5.1 MB)
- [ScreenClippingHost.exe.33364.zip](attachments/ScreenClippingHost.exe.33364.zip) (application/octet-stream, 3.7 MB)
- [demo.mp4](attachments/demo.mp4) (video/mp4, 3.1 MB)

## Timeline

### [Deleted User] (2023-02-04)

[Empty comment from Monorail migration]

### om...@talon-sec.com (2023-02-04)

Forgot to attach the crash of ScreenClippingHost.exe.

### fl...@google.com (2023-02-07)

Hello & thanks for the bug report!

I'm not able to reproduce this due to some issues with my Windows emulator.  However, based on the writeup + what I'm seeing in the stacktrace, I think it's worth going on and assigning this.

olka@, I'm assigning this to you, since, as the Chromium-in-WebRTC sheriff, I'm hoping you know the best person to take a look at this.  Please reassign if that's not the case.  Thanks!

And, omrib@—those reproduction steps look good, but I think your demo video didn't upload correctly?  (At least, I can't see anything.)  At your convenience, if you could upload another video, that might be helpful for whoever does reproduce this, since it looks like it's somewhat timing-dependent and having an idea of just how random the timing should be might be helpful.

[Monorail components: Blink>WebRTC]

### ol...@google.com (2023-02-07)

[Empty comment from Monorail migration]

[Monorail components: Internals>Media>ScreenCapture]

### ol...@google.com (2023-02-07)

[Empty comment from Monorail migration]

### ha...@google.com (2023-02-07)

[Empty comment from Monorail migration]

### om...@talon-sec.com (2023-02-07)

I attached a new demo video. At 0:30 you can see where we move from `WindowCapturerWinGdi` to `WgcCapturerWin` (all the windows get yellow border).The crash is in 1:42 (it also causes the whole screen to become black for a sec).

### he...@chromium.org (2023-02-07)

I am not able to trigger usage of WGC in Stable (109.0.5414.120). Not even if I add --enable-features=AllowWgcDesktopCapture as a command-line option. I am on Windows 10 (12H2).

### he...@chromium.org (2023-02-07)

[Empty comment from Monorail migration]

### om...@talon-sec.com (2023-02-07)

I did my tests on Windows 11. Look at  `IsWgcSupported` in `third_party\webrtc\modules\desktop_capture\win\wgc_capturer_win.cc`. It might be that it returns false in your case

### he...@chromium.org (2023-02-07)

First of all: thanks for a high-quality report.

There are no error logs added in IsWgcSupported and I can enable WGC if I build latest chromium so something is strange here.

Reassigning to alcooper@ who knows the current status of WGC in Chrome.

omrib@talon-sec.com@ can you trigger WGC in stable even in an incognito tab or using a fresh --user-data-dir?

### he...@chromium.org (2023-02-07)

Also adding a more readable version of the and Exception Analysis from WinDbg based on 6485e599-2cef-40f9-a9d7-5f99d0b23328.dmp.

The link is Google-only but mainly contains the same crash state as in the initial report but in a more user-friendly format

https://paste.googleplex.com/5876137237413888?raw

### om...@talon-sec.com (2023-02-07)

henrika@chromium.org - yes i reproduced the crash easily also in incognito

### al...@chromium.org (2023-02-07)

I believe it's because WGC is used as a fallback due to some bugs that we'd seen primarily on Windows 11. This option configures it; https://source.chromium.org/chromium/chromium/src/+/main:third_party/webrtc/modules/desktop_capture/desktop_capture_options.h;drc=7216b27406d094834d8644a525370069a70d2f93;l=182
And this restricts it to Windows 11: https://source.chromium.org/chromium/chromium/src/+/main:third_party/webrtc/modules/desktop_capture/window_capturer_win.cc;drc=0c4306fc554c80506eb0f9b833a5d2a5fdd452d5;l=30

The patch was initially added due to some cross-process capture issues; primarily youtube: https://webrtc-review.googlesource.com/c/src/+/252625, and then restricted to Win 11 due to an (unrelated) crash: https://webrtc-review.googlesource.com/c/src/+/258821

To be sure I understand, it seems like the issue is that the underlying window is destroyed, but we may still try to capture it because we haven't received the ItemClosed notification yet? Or the item may not exist when we attempt to unsubscribe?
RE:
>  `OnItemClosed` eventually be called in `DesktopMediaListCaptureThread` 
I don't believe I'm seeing this method/call?

IMO, the bug that this originally patched seems fairly minor, so we may want to try forcibly disabling this behavior (which should be a fairly scoped fix, though unfortunately one that does not have a flag associated with it at present). I do not however have access to a windows 11 machine to ensure there are no other side-effects from disabling it.

### [Deleted User] (2023-02-07)

[Empty comment from Monorail migration]

### om...@talon-sec.com (2023-02-07)

The issue is `OnItemClosed` will be called on `WgcCaptureSession` that is already destroyed. 

It can happen if the window is closed just when we try to capture it. For example if you set a bp in `hr = capture_session->StartCapture(options_);` in `WgcCapturerWin::CaptureFrame()`, and then close the captured window, then the call will fail and `ongoing_captures_.erase(capture_source_->GetSourceId());` will be called, which will destroy `WgcCaptureSession`. 
During the destruction of `WgcCaptureSession`, the COM thread can still send the message that signals the window is closed. If it succeeded to send it before we reach `item_->remove_Closed` in `RemoveEventHandlers`, then `OnItemClosed` will be called on the freed object.

The easiest way to see it is to comment out the `item_->remove_Closed` line and close the captured window in the bp as I described. It will trigger the crash.

### al...@chromium.org (2023-02-07)

OnItemClosed just sets a bunch of variables to nullptr: https://source.chromium.org/chromium/chromium/src/+/main:third_party/webrtc/modules/desktop_capture/win/wgc_capture_session.cc;drc=0c4306fc554c80506eb0f9b833a5d2a5fdd452d5;l=394
Which the destructor triggered by the erase call should be doing as well, so it looks like the error may actually be in this part of the stack:

0000007e`c79fe9d0 00007fff`7474f2ee     : 0000027d`6e2d5670 0000027d`6e2d56a0 0000027d`6e2d56a0 0000027d`6e2d5670 : GraphicsCapture!winrt::Windows::Graphics::Capture::implementation::GraphicsCaptureSession::Close+0x62

Which is on the OS Side?
CaptureFrame should also be occuring on `DesktopMediaListCaptureThread`

I don't think it would be possible for us to call double close, and it looks like we aren't actually calling a method on the capturer.

Steve can you take a look/route to someone from the OS perspective?

### al...@chromium.org (2023-02-07)

(Sorry had queued up my response and didn't see yours), The destructor in the stack you gave looks to be the OS object triggering the breakpoint; you're saying there's a separate stack pointing at the event invocation of the already deleted object?

### st...@microsoft.com (2023-02-07)

Adding sunggch@microsoft.com to the CC to help investigate.

### su...@microsoft.com (2023-02-08)

It looks like the root cause might be deleting Item object inside ItemObject's Closed Event handler. it could leads to unexpected behavior like the above crash or different crash. 

WgcCaptureSession::OnItemClosed() {
item_ = nullptr;
}


When using only WGC by changing the code in DesktopCapturer::CreateRawWindowCapturer, the crash keeps happening whenever any window is closed because the Item object is destroyed; The caller of the OnItemClosed back to Item object where it was destroyed.

The potential fix is to move "item_ = nullptr" to the WgcCaptureSession dtor.  (btw, WgcCaptureSession will be destroyed only when Picker window is closed.)


### [Deleted User] (2023-02-08)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### al...@chromium.org (2023-02-08)

Let me try this out with a forced repro on my Windows 10 machine.

### al...@chromium.org (2023-02-08)

CL out: https://webrtc-review.googlesource.com/c/src/+/292762

FWIW, I did get a slightly different stack but I also did not build with ASAN. The stack did however still point to an issue with the OnItemClosed handler/event unregistration, so combined with the stack initially posted I feel reasonably confident in the fix.

### gi...@appspot.gserviceaccount.com (2023-02-08)

The following revision refers to this bug:
  https://webrtc.googlesource.com/src/+/318cf28945d80a0ac6f09382e507c95e649cc4c1

commit 318cf28945d80a0ac6f09382e507c95e649cc4c1
Author: Alexander Cooper <alcooper@chromium.org>
Date: Wed Feb 08 22:16:01 2023

Fix Destruction inside WGC Callback

If we are notified of the destruction of the window before a
CaptureFrame call can fail, then we may end up attempting to destroy the
underlying WGC object inside it's own event handler. This can be
problematic, as the class itself may want to run other code. Instead,
we just unsubscribe and signal that any future CaptureFrame calls should
reject.

This also removes setting "is_capture_started_=false" in the item closed
handler, as all that served to do is cause the WgcCapturerWin code to
attempt to restart the capturer, and somewhat muddies up our metrics.

Bug: chromium:1413005
Change-Id: Ibccb7a2e7ce531ba80b4b331b9bc2cda0ff75f4e
Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/292762
Auto-Submit: Alexander Cooper <alcooper@chromium.org>
Reviewed-by: Mark Foltz <mfoltz@chromium.org>
Commit-Queue: Mark Foltz <mfoltz@chromium.org>
Commit-Queue: Alexander Cooper <alcooper@chromium.org>
Cr-Commit-Position: refs/heads/main@{#39275}

[modify] https://crrev.com/318cf28945d80a0ac6f09382e507c95e649cc4c1/modules/desktop_capture/win/wgc_capture_session.cc


### al...@chromium.org (2023-02-09)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-02-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/3d1561bdccaa9ddfb944772208999eeab2b5b1cc

commit 3d1561bdccaa9ddfb944772208999eeab2b5b1cc
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Thu Feb 09 02:21:35 2023

Roll WebRTC from d8361ee6b7ab to 318cf28945d8 (1 revision)

https://webrtc.googlesource.com/src.git/+log/d8361ee6b7ab..318cf28945d8

2023-02-08 alcooper@chromium.org Fix Destruction inside WGC Callback

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/webrtc-chromium-autoroll
Please CC webrtc-chromium-sheriffs-robots@google.com,webrtc-infra@google.com on the revert to ensure that a human
is aware of the problem.

To file a bug in WebRTC: https://bugs.chromium.org/p/webrtc/issues/entry
To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Bug: chromium:1413005
Tbr: webrtc-chromium-sheriffs-robots@google.com
Change-Id: Ia36200272cfebf3b81fccb6ae61055a008bba655
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4234525
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#1103082}

[modify] https://crrev.com/3d1561bdccaa9ddfb944772208999eeab2b5b1cc/DEPS


### he...@chromium.org (2023-02-09)

omrib@talon-sec.com: could you please share some crash IDs from chrome://crashes which are related to main cases above. That way we can verify that the latest fix has the desired effect.

### om...@talon-sec.com (2023-02-09)

Sure:
d1653505-987f-428e-b0ec-a4642c27d86f
4c6c8fb6-e3f3-4218-b5bc-0716d8c25a21
fa4b0fff-3ae5-4dd8-8035-5ab185a3799e
d3a8629b-f435-48b7-b9e7-a1ddf790cf0a
0da1eb4b-6ca0-4e54-9ee9-e9def2da81f0

### he...@chromium.org (2023-02-09)

Did you really get those IDs from chrome://crashes?

Looks like names of DMP files to me.

### om...@talon-sec.com (2023-02-09)

Yes sorry for the confusion, at first it didn't show me the IDs but just the dump names.
Here are the IDs:
49df1e01322d8fea
2e1f7a59b4492b02
ef83ec6c0b6e6b38
aaa32c01e6d838f3
206f366970f61a2c

### [Deleted User] (2023-02-09)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-09)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-09)

Requesting merge to stable M110 because latest trunk commit (1103082) appears to be after stable branch point (1084008).

Requesting merge to dev M111 because latest trunk commit (1103082) appears to be after dev branch point (1097615).

Merge review required: a commit with DEPS changes was detected.

Merge review required: a commit with DEPS changes was detected.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [110, 111].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### al...@chromium.org (2023-02-09)

1. Which CLs should be backmerged? (Please include Gerrit links.)
The CL from https://crbug.com/chromium/1413005#c24

2. Has this fix been tested on Canary?
The CL in question does not appear to have made it to Canary yet, due to needing to be rolled into Chromium from WebRTC. Note that I also do not have a Windows 11 PC, so am unable to test the scenario described without local modifications.

3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
The fix should be safe, it defers destruction of a handful of objects until the destructor runs instead of when receiving an event. Events are unsubscribed and any usages of these object are either creations or have a corresponding check with the "is_item_closed_" bool that blocks their further usage. The expected next call into the class to generate a frame (which should come fairly rapidly) should trigger the object to be destroyed. Though I have not tracked the exact path, the repro scenario described above (e.g. with the picker open), may not query for a new frame, but does query the OS

4. Does this fix pose any known compatibility risks?
I do not believe so

5. Does it require manual verification by the test team? If so, please describe required testing.
I don't think manual verification is required; but it may be beneficial to test the repro described.

I will also note FWIW, that I did not get the exact stack mentioned in the bug or crash reports here; but one that combined with the fix leaves me reasonably confident that it should address the issue. I could also only repro the POC on my Windows 10 machine when running under a debugger, but that may be the result of not having an ASAN build that got lucky and just worked, or because this is partially a timing issue.


### [Deleted User] (2023-02-11)

Requesting merge to stable M110 because latest trunk commit (1103082) appears to be after stable branch point (1084008).

Requesting merge to beta M111 because latest trunk commit (1103082) appears to be after beta branch point (1097615).

Merge review required: a commit with DEPS changes was detected.

Merge review required: a commit with DEPS changes was detected.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [110, 111].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-02-12)

Requesting merge to stable M110 because latest trunk commit (1103082) appears to be after stable branch point (1084008).

Requesting merge to beta M111 because latest trunk commit (1103082) appears to be after beta branch point (1097615).

Merge review required: a commit with DEPS changes was detected.

Merge review required: a commit with DEPS changes was detected.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [110, 111].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-02-13)

The roll with this fix has made it to Canary now, not seeing any stability or other issues.
M111 merge approved, please merge to branch 5563 by EOD tomorrow, Tuesday 14 February so this fix can be included in next M111 beta
M110 merge approved, please merge to branch 5481 by 10am Pacific, Friday 17 February so this fix can be included in the next M110/Stable respin 

### am...@chromium.org (2023-02-13)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-02-13)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-02-13)

There is some sort of monorail sorcery happening with the merge labels, trying once more to ensure both labels stick as this is approved for merge to 111 and 110

### mf...@chromium.org (2023-02-13)

Alex is OOO so I'm picking this up.  I'm not sure how to cherry-pick a WebRTC commit into Chrome release branches.  I don't see any branches in the WebRTC repo that map onto Chromium release branch numbers [*].  I'll start casting about for any documentation on this.

[*] https://webrtc.googlesource.com/src/


### mf...@chromium.org (2023-02-13)

I found the following and will give it a shot.  If this is indeed the correct cherry-pick instructions, it  would be helpful to link them from the general Chrome branch instructions.

https://g3doc.corp.google.com/third_party/webrtc/g3doc/cherry_pick/index.md?cl=head&g3docserverpod=true


### ha...@google.com (2023-02-13)

[Empty comment from Monorail migration]

### il...@chromium.org (2023-02-13)

Yeah, these instructions are good.

### mf...@chromium.org (2023-02-13)

M111 cherry-pick is in the CQ.  Once that lands I'll start a cherry-pick to M110.

### gi...@appspot.gserviceaccount.com (2023-02-13)

The following revision refers to this bug:
  https://webrtc.googlesource.com/src/+/cb954cdb0814e2119b6cb0fe2512d532b5c1419c

commit cb954cdb0814e2119b6cb0fe2512d532b5c1419c
Author: Alexander Cooper <alcooper@chromium.org>
Date: Wed Feb 08 22:16:01 2023

Fix Destruction inside WGC Callback

If we are notified of the destruction of the window before a
CaptureFrame call can fail, then we may end up attempting to destroy the
underlying WGC object inside it's own event handler. This can be
problematic, as the class itself may want to run other code. Instead,
we just unsubscribe and signal that any future CaptureFrame calls should
reject.

This also removes setting "is_capture_started_=false" in the item closed
handler, as all that served to do is cause the WgcCapturerWin code to
attempt to restart the capturer, and somewhat muddies up our metrics.

(cherry picked from commit 318cf28945d80a0ac6f09382e507c95e649cc4c1)

Bug: chromium:1413005
No-Try: True
Change-Id: Ibccb7a2e7ce531ba80b4b331b9bc2cda0ff75f4e
Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/292762
Auto-Submit: Alexander Cooper <alcooper@chromium.org>
Reviewed-by: Mark Foltz <mfoltz@chromium.org>
Commit-Queue: Mark Foltz <mfoltz@chromium.org>
Commit-Queue: Alexander Cooper <alcooper@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#39275}
Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/293243
Bot-Commit: rubber-stamper@appspot.gserviceaccount.com <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/5563@{#2}
Cr-Branched-From: 6c032cb8356b0d3f717c4fcf50796241f2bba6c2-refs/heads/main@{#39207}

[modify] https://crrev.com/cb954cdb0814e2119b6cb0fe2512d532b5c1419c/modules/desktop_capture/win/wgc_capture_session.cc


### am...@chromium.org (2023-02-13)

[Comment Deleted]

### am...@chromium.org (2023-02-13)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-02-13)

I see this was already merged to M111/5563, but I was checking the monorail issue was resolved, removing label 

### gi...@appspot.gserviceaccount.com (2023-02-14)

The following revision refers to this bug:
  https://webrtc.googlesource.com/src/+/218b56e516386cd57c7513197528c3124bcd7ef3

commit 218b56e516386cd57c7513197528c3124bcd7ef3
Author: Alexander Cooper <alcooper@chromium.org>
Date: Wed Feb 08 22:16:01 2023

Fix Destruction inside WGC Callback

If we are notified of the destruction of the window before a
CaptureFrame call can fail, then we may end up attempting to destroy the
underlying WGC object inside it's own event handler. This can be
problematic, as the class itself may want to run other code. Instead,
we just unsubscribe and signal that any future CaptureFrame calls should
reject.

This also removes setting "is_capture_started_=false" in the item closed
handler, as all that served to do is cause the WgcCapturerWin code to
attempt to restart the capturer, and somewhat muddies up our metrics.

(cherry picked from commit 318cf28945d80a0ac6f09382e507c95e649cc4c1)

Bug: chromium:1413005
No-Try: True
Change-Id: Ibccb7a2e7ce531ba80b4b331b9bc2cda0ff75f4e
Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/292762
Auto-Submit: Alexander Cooper <alcooper@chromium.org>
Reviewed-by: Mark Foltz <mfoltz@chromium.org>
Commit-Queue: Mark Foltz <mfoltz@chromium.org>
Commit-Queue: Alexander Cooper <alcooper@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#39275}
Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/293246
Bot-Commit: rubber-stamper@appspot.gserviceaccount.com <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/5481@{#5}
Cr-Branched-From: 2e1a9a4ae0234d4b1ea7a6fd4188afa1fb20379d-refs/heads/main@{#38901}

[modify] https://crrev.com/218b56e516386cd57c7513197528c3124bcd7ef3/modules/desktop_capture/win/wgc_capture_session.cc


### am...@chromium.org (2023-02-20)

[Empty comment from Monorail migration]

### am...@google.com (2023-02-21)

[Empty comment from Monorail migration]

### pg...@google.com (2023-02-22)

[Empty comment from Monorail migration]

### am...@google.com (2023-03-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-03-09)

Congratulations Omri! The VRP Panel has decided to award you $2,000 for this report of a heavily mitigated security bug. Thank you for your efforts in discovering and reporting this issue to us! 

### am...@google.com (2023-03-11)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-19)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1413005?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>WebRTC, Internals>Media>ScreenCapture]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-02-28)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/chrome-blintz-user-guide

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062915)*
