# Security: Use after Free in content::AccessibilityEventRecorderWin::AccessibleObjectFromWindowWrapper 

| Field | Value |
|-------|-------|
| **Issue ID** | [40057908](https://issues.chromium.org/issues/40057908) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Internals>Accessibility |
| **Platforms** | Windows |
| **Reporter** | ha...@gmail.com |
| **Assignee** | al...@chromium.org |
| **Created** | 2021-11-14 |
| **Bounty** | $1,000.00 |

## Description

This vulnerability is a new point, and I accidentally triggered this crash, but after I analyzed it, it is indeed a real UAF vulnerability.The asan log of this UAF is not complete, but I still analyzed the specific reasons.

[0]<https://source.chromium.org/chromium/chromium/src/+/main:content/browser/accessibility/accessibility_event_recorder.h;drc=86646d357f0decd9b33e54afe7a36227088aba98;l=53>

BrowserAccessibilityManager\* const manager\_; //hold raw pointer

[1] <https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/render_frame_host_impl.cc;l=2589?q=AccessibilityFatalError&ss=chromium%2Fchromium%2Fsrc>

void RenderFrameHostImpl::AccessibilityFatalError() {  

browser\_accessibility\_manager\_.reset(nullptr); the unique ptr was destroyed  

if (accessibility\_reset\_token\_ || !render\_accessibility\_)  

return;

accessibility\_fatal\_error\_count\_++;  

if (accessibility\_fatal\_error\_count\_ > max\_accessibility\_resets\_) {  

// This will both create an "Aw Snap..." and generate a second crash report  

// in addition to the DumpWithoutCrashing() for the first reset.  

render\_accessibility\_->FatalError();  

} else {  

// Crash keys set in BrowserAccessibilityManager::Unserialize().  

if (accessibility\_fatal\_error\_count\_ == 1) {  

// Only send crash report first time -- don't skew crash stats too much.  

base::debug::DumpWithoutCrashing();  

}  

AccessibilityReset();  

}  

}

[2] <https://source.chromium.org/chromium/chromium/src/+/main:content/browser/accessibility/accessibility_event_recorder_win.cc;l=356?q=content::AccessibilityEventRecorderWin::AccessibleObjectFromWindowWrapper%20&ss=chromium%2Fchromium%2Fsrc>

HRESULT AccessibilityEventRecorderWin::AccessibleObjectFromWindowWrapper(  

HWND hwnd,  

DWORD dw\_id,  

REFIID riid,  

void\*\* ppv\_object) {  

HRESULT hr = ::AccessibleObjectFromWindow(hwnd, dw\_id, riid, ppv\_object);  

if (SUCCEEDED(hr))  

return hr;

if (!manager\_) // No manager when outside of Chrome tests.  

return E\_FAIL;

// The above call to ::AccessibleObjectFromWindow fails for unknown  

// reasons every once in a while on the bots. Work around it by grabbing  

// the object directly from the BrowserAccessibilityManager.  

HWND accessibility\_hwnd =  

manager\_->delegate()->AccessibilityGetAcceleratedWidget(); //but the raw pointer was still used and UAF here  

if (accessibility\_hwnd != hwnd)  

return E\_FAIL;

IAccessible\* obj = ToBrowserAccessibilityComWin(manager\_->GetRoot());  

obj->AddRef();  

\*ppv\_object = obj;  

return S\_OK;  

}

=================================================================  

==30828==ERROR: AddressSanitizer: heap-use-after-free on address 0x12bfd72a5bb0 at pc 0x7ffa4924e1bb bp 0x00bcb91fe210 sp 0x00bcb91fe258  

READ of size 8 at 0x12bfd72a5bb0 thread T0  

==30828==WARNING: Failed to use and restart external symbolizer!  

#0 0x7ffa4924e1ba in content::AccessibilityEventRecorderWin::AccessibleObjectFromWindowWrapper C:\b\s\w\ir\cache\builder\src\content\browser\accessibility\accessibility\_event\_recorder\_win.cc:356  

#1 0x7ffa49247e4b in content::AccessibilityEventRecorderWin::OnWinEventHook C:\b\s\w\ir\cache\builder\src\content\browser\accessibility\accessibility\_event\_recorder\_win.cc:149  

#2 0x7ffa492478ac in content::AccessibilityEventRecorderWin::WinEventHookThunk C:\b\s\w\ir\cache\builder\src\content\browser\accessibility\accessibility\_event\_recorder\_win.cc:98  

#3 0x7ffaf415c045 in RemovePropW+0x135 (C:\WINDOWS\System32\user32.dll+0x18002c045)  

#4 0x7ffaf43c4833 in KiUserCallbackDispatcher+0x23 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x1800a4833)  

#5 0x7ffaf1f019b3 in NtUserNotifyWinEvent+0x13 (C:\WINDOWS\System32\win32u.dll+0x1800019b3)  

#6 0x7ffaf415a69b in NotifyWinEvent+0xfb (C:\WINDOWS\System32\user32.dll+0x18002a69b)  

#7 0x7ffaf3ce8bb2 in TF\_Notify+0x10df2 (C:\WINDOWS\System32\MSCTF.dll+0x180028bb2)  

#8 0x7ffaf3cd9bc5 in TF\_Notify+0x1e05 (C:\WINDOWS\System32\MSCTF.dll+0x180019bc5)  

#9 0x7ffaf3cd96c8 in TF\_Notify+0x1908 (C:\WINDOWS\System32\MSCTF.dll+0x1800196c8)  

#10 0x7ffaf3cf0b25 in TF\_UninitSystem+0x1e65 (C:\WINDOWS\System32\MSCTF.dll+0x180030b25)  

#11 0x7ffaf415c045 in RemovePropW+0x135 (C:\WINDOWS\System32\user32.dll+0x18002c045)  

#12 0x7ffaf43c4833 in KiUserCallbackDispatcher+0x23 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x1800a4833)  

#13 0x7ffaf1f01553 in NtUserMessageCall+0x13 (C:\WINDOWS\System32\win32u.dll+0x180001553)  

#14 0x7ffaf4145867 in GetWindow+0xb37 (C:\WINDOWS\System32\user32.dll+0x180015867)  

#15 0x7ffaf4145275 in GetWindow+0x545 (C:\WINDOWS\System32\user32.dll+0x180015275)  

#16 0x7ffa5856e3bf in views::HWNDMessageHandler::OnWndProc C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd\_message\_handler.cc:1025  

#17 0x7ffa51d84c36 in gfx::WindowImpl::WndProc C:\b\s\w\ir\cache\builder\src\ui\gfx\win\window\_impl.cc:307  

#18 0x7ffa51d83551 in base::win::WrappedWindowProc<&gfx::WindowImpl::WndProc> C:\b\s\w\ir\cache\builder\src\base\win\wrapped\_window\_proc.h:74  

#19 0x7ffaf4149d62 in CallWindowProcW+0x5c2 (C:\WINDOWS\System32\user32.dll+0x180019d62)  

#20 0x7ffaf414972b in SendMessageW+0xbcb (C:\WINDOWS\System32\user32.dll+0x18001972b)  

#21 0x7ffaf4157029 in FillRect+0xb9 (C:\WINDOWS\System32\user32.dll+0x180027029)  

#22 0x7ffaf43c4833 in KiUserCallbackDispatcher+0x23 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x1800a4833)  

#23 0x7ffaf1f014d3 in NtUserPeekMessage+0x13 (C:\WINDOWS\System32\win32u.dll+0x1800014d3)  

#24 0x7ffaf4151f65 in PeekMessageW+0x225 (C:\WINDOWS\System32\user32.dll+0x180021f65)  

#25 0x7ffaf4151e7f in PeekMessageW+0x13f (C:\WINDOWS\System32\user32.dll+0x180021e7f)  

#26 0x7ffa4f019221 in base::MessagePumpForUI::ProcessNextWindowsMessage C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:500  

#27 0x7ffa4f018b93 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:215  

#28 0x7ffa4f016ec8 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:78  

#29 0x7ffa51a4c365 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:463  

#30 0x7ffa4eeefcf3 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:140  

#31 0x7ffa481fac81 in content::BrowserMainLoop::RunMainMessageLoop C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_loop.cc:1005  

#32 0x7ffa481fff8d in content::BrowserMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_runner\_impl.cc:152  

#33 0x7ffa481f471a in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main.cc:49  

#34 0x7ffa4abcb4e0 in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:641  

#35 0x7ffa4abcdde9 in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1137  

#36 0x7ffa4abccfd3 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1004  

#37 0x7ffa4abc99e2 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:390  

#38 0x7ffa4abcaa24 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:418  

#39 0x7ffa445e147f in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc:172  

#40 0x7ff77ffa5b45 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main\_dll\_loader\_win.cc:170  

#41 0x7ff77ffa2c31 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_exe\_main\_win.cc:382  

#42 0x7ff78039d17f in \_\_scrt\_common\_main\_seh d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#43 0x7ffaf2d46aaf in BaseThreadInitThunk+0xf (C:\WINDOWS\System32\KERNEL32.DLL+0x180016aaf)  

#44 0x7ffaf4371dba in RtlUserThreadStart+0x2a (C:\WINDOWS\SYSTEM32\ntdll.dll+0x180051dba)

0x12bfd72a5bb0 is located 48 bytes inside of 584-byte region [0x12bfd72a5b80,0x12bfd72a5dc8)  

freed by thread T0 here:  

#0 0x7ff78005227b in free C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:82  

#1 0x7ffa4928a6e3 in content::BrowserAccessibilityManagerWin::~BrowserAccessibilityManagerWin C:\b\s\w\ir\cache\builder\src\content\browser\accessibility\browser\_accessibility\_manager\_win.cc:86  

#2 0x7ffa48c95159 in content::RenderFrameHostImpl::AccessibilityFatalError C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\render\_frame\_host\_impl.cc:2558  

#3 0x7ffa48ccbee9 in content::RenderFrameHostImpl::HandleAXEvents C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\render\_frame\_host\_impl.cc:7124  

#4 0x7ffa4802abfa in base::internal::Invoker<base::internal::BindState<void (content::RenderFrameHostImpl::\*)(const ui::AXTreeID &, mojo::StructPtr[content::mojom::AXUpdatesAndEvents](javascript:void(0);), int),base::WeakPtr[content::RenderFrameHostImpl](javascript:void(0);),ui::AXTreeID,mojo::StructPtr[content::mojom::AXUpdatesAndEvents](javascript:void(0);),int>,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind\_internal.h:753  

#5 0x7ffa51a44bcf in base::`anonymous namespace'::PostTaskAndReplyRelay::RunTaskAndPostReply C:\b\s\w\ir\cache\builder\src\base\threading\post\_task\_and\_reply\_impl.cc:100  

#6 0x7ffa51a45413 in base::internal::Invoker<base::internal::BindState<void (\*)(base::(anonymous namespace)::PostTaskAndReplyRelay),base::(anonymous namespace)::PostTaskAndReplyRelay>,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind\_internal.h:753  

#7 0x7ffa4ef6fffa in base::TaskAnnotator::RunTask C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:178  

#8 0x7ffa51a4af4f in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:358  

#9 0x7ffa51a4a668 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:261  

#10 0x7ffa4f018c36 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:220  

#11 0x7ffa4f016ec8 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:78  

#12 0x7ffa51a4c365 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:463  

#13 0x7ffa4eeefcf3 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:140  

#14 0x7ffa481fac81 in content::BrowserMainLoop::RunMainMessageLoop C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_loop.cc:1005  

#15 0x7ffa481fff8d in content::BrowserMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_runner\_impl.cc:152  

#16 0x7ffa481f471a in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main.cc:49  

#17 0x7ffa4abcb4e0 in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:641  

#18 0x7ffa4abcdde9 in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1137  

#19 0x7ffa4abccfd3 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1004  

#20 0x7ffa4abc99e2 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:390  

#21 0x7ffa4abcaa24 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:418  

#22 0x7ffa445e147f in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc:172  

#23 0x7ff77ffa5b45 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main\_dll\_loader\_win.cc:170  

#24 0x7ff77ffa2c31 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_exe\_main\_win.cc:382  

#25 0x7ff78039d17f in \_\_scrt\_common\_main\_seh d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#26 0x7ffaf2d46aaf in BaseThreadInitThunk+0xf (C:\WINDOWS\System32\KERNEL32.DLL+0x180016aaf)  

#27 0x7ffaf4371dba in RtlUserThreadStart+0x2a (C:\WINDOWS\SYSTEM32\ntdll.dll+0x180051dba)

previously allocated by thread T0 here:  

#0 0x7ff78005237b in malloc C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:98  

#1 0x7ffa61753c6a in operator new d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\heap\new\_scalar.cpp:35  

#2 0x7ffa492849e0 in content::BrowserAccessibilityManager::Create C:\b\s\w\ir\cache\builder\src\content\browser\accessibility\browser\_accessibility\_manager\_win.cc:69  

#3 0x7ffa48cbc830 in content::RenderFrameHostImpl::GetOrCreateBrowserAccessibilityManager C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\render\_frame\_host\_impl.cc:8647  

#4 0x7ffa48ccafd9 in content::RenderFrameHostImpl::HandleAXEvents C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\render\_frame\_host\_impl.cc:7092  

#5 0x7ffa4802abfa in base::internal::Invoker<base::internal::BindState<void (content::RenderFrameHostImpl::\*)(const ui::AXTreeID &, mojo::StructPtr[content::mojom::AXUpdatesAndEvents](javascript:void(0);), int),base::WeakPtr[content::RenderFrameHostImpl](javascript:void(0);),ui::AXTreeID,mojo::StructPtr[content::mojom::AXUpdatesAndEvents](javascript:void(0);),int>,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind\_internal.h:753  

#6 0x7ffa51a44bcf in base::`anonymous namespace'::PostTaskAndReplyRelay::RunTaskAndPostReply C:\b\s\w\ir\cache\builder\src\base\threading\post\_task\_and\_reply\_impl.cc:100  

#7 0x7ffa51a45413 in base::internal::Invoker<base::internal::BindState<void (\*)(base::(anonymous namespace)::PostTaskAndReplyRelay),base::(anonymous namespace)::PostTaskAndReplyRelay>,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind\_internal.h:753  

#8 0x7ffa4ef6fffa in base::TaskAnnotator::RunTask C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:178  

#9 0x7ffa51a4af4f in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:358  

#10 0x7ffa51a4a668 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:261  

#11 0x7ffa4f018c36 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:220  

#12 0x7ffa4f016ec8 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:78  

#13 0x7ffa51a4c365 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:463  

#14 0x7ffa4eeefcf3 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:140  

#15 0x7ffa481fac81 in content::BrowserMainLoop::RunMainMessageLoop C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_loop.cc:1005  

#16 0x7ffa481fff8d in content::BrowserMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_runner\_impl.cc:152  

#17 0x7ffa481f471a in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main.cc:49  

#18 0x7ffa4abcb4e0 in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:641  

#19 0x7ffa4abcdde9 in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1137  

#20 0x7ffa4abccfd3 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1004  

#21 0x7ffa4abc99e2 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:390  

#22 0x7ffa4abcaa24 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:418  

#23 0x7ffa445e147f in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc:172  

#24 0x7ff77ffa5b45 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main\_dll\_loader\_win.cc:170  

#25 0x7ff77ffa2c31 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_exe\_main\_win.cc:382  

#26 0x7ff78039d17f in \_\_scrt\_common\_main\_seh d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#27 0x7ffaf2d46aaf in BaseThreadInitThunk+0xf (C:\WINDOWS\System32\KERNEL32.DLL+0x180016aaf)

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\s\w\ir\cache\builder\src\content\browser\accessibility\accessibility\_event\_recorder\_win.cc:356 in content::AccessibilityEventRecorderWin::AccessibleObjectFromWindowWrapper  

Shadow bytes around the buggy address:  

0x04ebd1bd4b20: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x04ebd1bd4b30: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x04ebd1bd4b40: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x04ebd1bd4b50: fd fd fd fd fd fd fd fd fd fd fd fd fa fa fa fa  

0x04ebd1bd4b60: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

=>0x04ebd1bd4b70: fd fd fd fd fd fd[fd]fd fd fd fd fd fd fd fd fd  

0x04ebd1bd4b80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x04ebd1bd4b90: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x04ebd1bd4ba0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x04ebd1bd4bb0: fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa  

0x04ebd1bd4bc0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

Shadow byte legend (one shadow byte represents 8 application bytes):  

Addressable: 00  

Partially addressable: 01 02 03 04 05 06 07  

Heap left redzone: fa  

Freed heap region: fd  

Stack left redzone: f1  

Stack mid redzone: f2  

Stack right redzone: f3  

Stack after return: f5  

Stack use after scope: f8  

Global redzone: f9  

Global init order: f6  

Poisoned by user: f7  

Container overflow: fc  

Array cookie: ac  

Intra object redzone: bb  

ASan internal: fe  

Left alloca redzone: ca  

Right alloca redzone: cb  

==30828==ABORTING

**VERSION**  

Chrome Version: 98.0.4704.1  

Operating System: windows 11 22489.1000

credit information:

Zhihua Yao of KunLun Lab

## Attachments

- [repro.mp4](attachments/repro.mp4) (video/mp4, 6.2 MB)

## Timeline

### [Deleted User] (2021-11-14)

[Empty comment from Monorail migration]

### ha...@gmail.com (2021-11-14)

[Comment Deleted]

### ts...@chromium.org (2021-11-15)

[Empty comment from Monorail migration]

[Monorail components: Internals>Accessibility]

### [Deleted User] (2021-11-15)

[Empty comment from Monorail migration]

### ts...@chromium.org (2021-11-15)

[Empty comment from Monorail migration]

### dt...@chromium.org (2021-11-15)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-16)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-11-28)

aleventhal: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### al...@chromium.org (2021-11-30)

@hackyzh002, the AccessibilityEventRecorderWin is only used in chrome://accessibility.
Did your steps involve loading that page?

### al...@chromium.org (2021-11-30)

Talked this over with a colleague. We don't believe this is a security issue, because it's impossible to run the event recorder except in tests, unless you visit chrome://accessibility.

### [Deleted User] (2021-11-30)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-30)

[Empty comment from Monorail migration]

### ha...@gmail.com (2021-11-30)

@aleventhal,please see this issue,happen in chrome://help-app,https://bugs.chromium.org/p/chromium/issues/detail?id=1232628

### al...@chromium.org (2021-11-30)

@hackyzh002, this bug cannot occur in chrome://help-app.
However, it could occur when using chrome://accessibility.
Either way, it's not a security error as the user cannot be forced to visit those pages.

### ha...@gmail.com (2021-11-30)

I'm just giving an example, so https://crbug.com/chromium/1232628 can't be regarded as a security issue? 

### al...@chromium.org (2021-12-01)

I think https://crbug.com/chromium/1232628 is unrelated.

Can you describe reproducible steps so make this bug happen?

### al...@chromium.org (2021-12-01)

[Empty comment from Monorail migration]

### ha...@gmail.com (2021-12-02)

hello  aleventhal@,I uploaded this video again. This UAF is easy to reproduce in version 97.0.4682.0 because it will refresh automatically.And this vulnerability should be relatively easy to fix.Finally, thank you for responding so much.I think fixing the vulnerability is the main purpose. :)

### al...@chromium.org (2021-12-02)

WIP CL: https://chromium-review.googlesource.com/c/chromium/src/+/3307486

### al...@chromium.org (2021-12-02)

Looks like the steps are:
1. Load chrome://accessibility
2. Check  web accessibility
3. Rapidly repeatedly toggle the native a11y API support checkbox 

It doesn't make a lot of sense to consider chrome:// crashes as actual security vulnerabilities.
You can't inject code into them, link to them from another page, or load them remotely. A user would have to manually go to that page themselves.

That said, thanks for the bug and we will address by having it manually force a safe crash in this case (where the a11y messaging system gets confused).

### gi...@appspot.gserviceaccount.com (2021-12-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/96df51a947a4603c9c5c202d23bb0d2b9af1c0fe

commit 96df51a947a4603c9c5c202d23bb0d2b9af1c0fe
Author: Aaron Leventhal <aleventhal@google.com>
Date: Thu Dec 02 23:39:01 2021

Crash immediately on AX error when AX inspect features are used

Fixes a UAF in the accessibility event recorder when an
event came in after an AccessibilityFatalError(), The UAF occurs
when attempt was made to access the raw pointer manager_,
which was previously released by the manager's owner RenderFrameHostImpl
when ::AccessibilityFatalError() tried to gracefully reset
accessibility without crashing the renderer. Now,
AccessibilityFatalError() forces a crash when any developer feature
such as the event recorder is used.

There is an benefit of this approach: any AccessibilityFatalError()
that occurs during content_browsertests or after a developer has used
chrome://accessibility will crash immediately.
Better to crash immediately than to try to swallow bad serializations.
Note that the fail fast flag is purposely kept on, because using
chrome://accessibility shows that the user is a developer.

Bug: 1270095
Change-Id: Ib14c39d3f674713c07769eb37d5221a5353277d7
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3307486
Auto-Submit: Aaron Leventhal <aleventhal@chromium.org>
Reviewed-by: Alex Moshchuk <alexmos@chromium.org>
Reviewed-by: Nektarios Paisios <nektar@chromium.org>
Commit-Queue: Aaron Leventhal <aleventhal@chromium.org>
Cr-Commit-Position: refs/heads/main@{#947745}

[modify] https://crrev.com/96df51a947a4603c9c5c202d23bb0d2b9af1c0fe/content/public/browser/ax_inspect_factory.cc
[modify] https://crrev.com/96df51a947a4603c9c5c202d23bb0d2b9af1c0fe/content/public/browser/ax_inspect_factory_fuchsia.cc
[modify] https://crrev.com/96df51a947a4603c9c5c202d23bb0d2b9af1c0fe/content/browser/accessibility/browser_accessibility_manager.h
[modify] https://crrev.com/96df51a947a4603c9c5c202d23bb0d2b9af1c0fe/content/public/browser/ax_inspect_factory_win.cc
[modify] https://crrev.com/96df51a947a4603c9c5c202d23bb0d2b9af1c0fe/content/browser/renderer_host/render_frame_host_impl.cc
[modify] https://crrev.com/96df51a947a4603c9c5c202d23bb0d2b9af1c0fe/content/browser/accessibility/accessibility_event_recorder_win.cc
[modify] https://crrev.com/96df51a947a4603c9c5c202d23bb0d2b9af1c0fe/content/public/browser/ax_inspect_factory_android.cc
[modify] https://crrev.com/96df51a947a4603c9c5c202d23bb0d2b9af1c0fe/content/browser/web_contents/web_contents_impl.cc
[modify] https://crrev.com/96df51a947a4603c9c5c202d23bb0d2b9af1c0fe/content/public/browser/ax_inspect_factory_auralinux.cc
[modify] https://crrev.com/96df51a947a4603c9c5c202d23bb0d2b9af1c0fe/content/browser/accessibility/browser_accessibility_manager.cc
[modify] https://crrev.com/96df51a947a4603c9c5c202d23bb0d2b9af1c0fe/content/public/browser/ax_inspect_factory_mac.mm


### al...@chromium.org (2021-12-03)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-03)

Dear owner, thanks for fixing this bug. We’ve reopened it because security bugs need Security_Severity and FoundIn labels set, which will enable the bots to request merges to the correct branches ( as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact (security@chromium.org) to arrange to set these labels and then this bug can be marked closed again. Thank you! Severity guidelines: https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues FoundIn guidelines: https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security Thanks for your time! 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2021-12-03)

We consider browser process use-after-free to be Critical, but if it requires "unusual or unlikely user interaction" we consider the severity to be mitigated down by one or two levels. I'm therefore going to rate this Security_Severity-Medium.

### [Deleted User] (2021-12-04)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-04)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-12-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/40368c45857e8f0f4602de3dd8f91d038214ca02

commit 40368c45857e8f0f4602de3dd8f91d038214ca02
Author: Alexander Surkov <asurkov@igalia.com>
Date: Mon Dec 20 20:18:30 2021

ax_inspect: loose content dependency for ax event recorders

Get rid of content::BrowserAccessibilityManager dependency in event
recorders where possible.

Besides it allows to ship ax_dump tools with no content dependency, it
also helps to avoid bugs like
https://bugs.chromium.org/p/chromium/issues/detail?id=1270095.

Bug: 1270095
Change-Id: I2fc67f2c0990cd75277bf6497eae7d698e3cb925
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3342128
Reviewed-by: Nektarios Paisios <nektar@chromium.org>
Reviewed-by: Alex Moshchuk <alexmos@chromium.org>
Commit-Queue: Alexander Surkkov <asurkov@igalia.com>
Cr-Commit-Position: refs/heads/main@{#953001}

[modify] https://crrev.com/40368c45857e8f0f4602de3dd8f91d038214ca02/content/browser/BUILD.gn
[delete] https://crrev.com/d552cb6edf05e5d6d5d8db2115d563a27abb55c2/content/browser/accessibility/accessibility_event_recorder.h
[modify] https://crrev.com/40368c45857e8f0f4602de3dd8f91d038214ca02/content/browser/accessibility/accessibility_event_recorder_win.cc
[modify] https://crrev.com/40368c45857e8f0f4602de3dd8f91d038214ca02/content/browser/accessibility/dump_accessibility_browsertest_base.cc
[modify] https://crrev.com/40368c45857e8f0f4602de3dd8f91d038214ca02/content/public/browser/ax_inspect_factory_android.cc
[modify] https://crrev.com/40368c45857e8f0f4602de3dd8f91d038214ca02/content/browser/accessibility/accessibility_event_recorder_fuchsia.h
[delete] https://crrev.com/d552cb6edf05e5d6d5d8db2115d563a27abb55c2/content/browser/accessibility/accessibility_event_recorder.cc
[modify] https://crrev.com/40368c45857e8f0f4602de3dd8f91d038214ca02/content/browser/accessibility/accessibility_event_recorder_mac.h
[modify] https://crrev.com/40368c45857e8f0f4602de3dd8f91d038214ca02/content/browser/accessibility/accessibility_event_recorder_auralinux.cc
[modify] https://crrev.com/40368c45857e8f0f4602de3dd8f91d038214ca02/content/public/browser/ax_inspect_factory.cc
[modify] https://crrev.com/40368c45857e8f0f4602de3dd8f91d038214ca02/content/public/browser/ax_inspect_factory_fuchsia.cc
[modify] https://crrev.com/40368c45857e8f0f4602de3dd8f91d038214ca02/content/browser/accessibility/accessibility_event_recorder_win.h
[modify] https://crrev.com/40368c45857e8f0f4602de3dd8f91d038214ca02/content/browser/accessibility/accessibility_event_recorder_uia_win.h
[modify] https://crrev.com/40368c45857e8f0f4602de3dd8f91d038214ca02/content/browser/accessibility/accessibility_event_recorder_fuchsia.cc
[modify] https://crrev.com/40368c45857e8f0f4602de3dd8f91d038214ca02/content/browser/accessibility/accessibility_event_recorder_mac.mm
[modify] https://crrev.com/40368c45857e8f0f4602de3dd8f91d038214ca02/content/browser/accessibility/accessibility_event_recorder_auralinux.h
[modify] https://crrev.com/40368c45857e8f0f4602de3dd8f91d038214ca02/content/browser/accessibility/accessibility_event_recorder_uia_win.cc
[modify] https://crrev.com/40368c45857e8f0f4602de3dd8f91d038214ca02/content/public/browser/ax_inspect_factory_mac.mm


### ha...@gmail.com (2022-01-08)

Hello, Any reward update?

### am...@chromium.org (2022-01-13)

We are working bugs in prioritized (high to low severity) and are working through a bit of a backlog due from the festive/holiday season in the US. Potential reward decisions will be updated here as they are made. We appreciate your patience as we work thorough our backlog. 

### am...@google.com (2022-01-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ha...@gmail.com (2022-01-13)

Hello,This is the uaf of the browser, I think the bounty knife should be raised by 10000, this should not be 1000

### ha...@gmail.com (2022-01-13)

[Comment Deleted]

### ha...@gmail.com (2022-01-13)

And a friend of mine just described, there are 5000 without actual repro, which is a bit unfair, https://bugs.chromium.org/p/chromium/issues/detail?id=1243117 This has 15,000 without actual  repro, I don't know what you think 

### am...@chromium.org (2022-01-14)

Hello, this reward amount was not determine solely because there was no POC or reproduction, but also because 
1) this bug does not appear to be reachable from the web and triggering it would require considerable amount of UI gesture
2) the amount of UI gesture is quite exception and unusable, the chances of an attacker convincing a user to engage with the UI in this way to exploit this bug seem very low 
3) there would be very limited attacker control to exploit this issue, so with the very low exploitability potential, the reward extended is much lower

If you can provide a POC that displays a way to trigger and exploit this issue without exception UI gesture and demonstrate greater control of this vulnerability, we would be happy to revisit this issue and reassess the reward amount. 


### am...@google.com (2022-01-14)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-02-01)

[Empty comment from Monorail migration]

### am...@google.com (2022-02-01)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-02-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/f83fa6cdedd695d2df732899c1865121667548cb

commit f83fa6cdedd695d2df732899c1865121667548cb
Author: Alexander Surkov <asurkov@igalia.com>
Date: Fri Feb 11 14:01:51 2022

ax_inspect: no content dependency for UIA event recorder

Get rid of content::BrowserAccessibilityManager dependency in UIA event
recorder.

Besides it allows to ship ax_dump tools with no content dependency, it
also helps to avoid bugs like
https://bugs.chromium.org/p/chromium/issues/detail?id=1270095.

Bug: 1270095
Change-Id: I5f0cc5628d297d28877d862c0b27b82a4c4f9d53
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3449579
Reviewed-by: Nektarios Paisios <nektar@chromium.org>
Reviewed-by: Avi Drissman <avi@chromium.org>
Commit-Queue: Alexander Surkkov <asurkov@igalia.com>
Cr-Commit-Position: refs/heads/main@{#969919}

[modify] https://crrev.com/f83fa6cdedd695d2df732899c1865121667548cb/ui/accessibility/platform/inspect/ax_inspect.h
[modify] https://crrev.com/f83fa6cdedd695d2df732899c1865121667548cb/content/public/browser/ax_inspect_factory_win.cc
[modify] https://crrev.com/f83fa6cdedd695d2df732899c1865121667548cb/content/browser/accessibility/dump_accessibility_browsertest_base.cc
[modify] https://crrev.com/f83fa6cdedd695d2df732899c1865121667548cb/content/browser/accessibility/accessibility_event_recorder_uia_win.h
[modify] https://crrev.com/f83fa6cdedd695d2df732899c1865121667548cb/content/browser/web_contents/web_contents_impl.cc
[modify] https://crrev.com/f83fa6cdedd695d2df732899c1865121667548cb/content/browser/accessibility/accessibility_win_browsertest.cc
[modify] https://crrev.com/f83fa6cdedd695d2df732899c1865121667548cb/content/browser/accessibility/accessibility_event_recorder_uia_win.cc
[modify] https://crrev.com/f83fa6cdedd695d2df732899c1865121667548cb/content/public/browser/ax_inspect_factory_mac.mm


### [Deleted User] (2022-03-12)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sa...@gmail.com (2022-03-12)

I think the VRP team did not make the right decision on the award. 
This issue is no different from the PoC steps https://crbug.com/1201032 ($25K) report. 

1. Go to chrome://accessibility/
2. open debug console with F12
3. copy & paste & run following script

```
 function sleep(delay) {
            return new Promise((resolve) => setTimeout(resolve, delay));
        }

        var tab1 = open("chrome://accessibility/");
        await sleep(1000);
        tab1.location.reload();
        await sleep(2000);

        with(tab1) {

            document.querySelector("body > div:nth-child(3) > div:nth-child(1) > div:nth-child(5) > label").click()
            for (let index = 0; index < 100000; index++) {
                document.querySelector("#native").click()
                await sleep(100)


            }

        }

```

I also suggest the VRP team increase the minimum bounty for memory issues. 
The consequences of memory problems for a user are critical and require high level engineering. 
It deserves more awards than an XSS issue.

amyressler@, can you take a look at this report again?

### wx...@gmail.com (2022-03-12)

Wow, amazing poc.

### am...@chromium.org (2022-03-13)

Hi samet - thanks for reaching out about this. 
The report you reference in comparison (https://crbug.com/chromium/1201032) was awarded $25,000 because it was a report of five separate UAFs. It also required a second set of POCs to be provided, because as you can see in the original reward decision (https://bugs.chromium.org/p/chromium/issues/detail?id=1201032#c38) the VRP Panel originally declined a reward due to the reliance on on direct access to dev tools to trigger those UAF bugs. The researcher provided a whole new set of POCs that demonstrated these vulnerabilities being triggered via an extension and remote content without the direct access to dev tools. For this new set of reports and POCs they were extended a $25,000 reward. 

For this case, https://crbug.com/chromium/1270095#c34 clearly explains the reward judgement. 
For UAFs and other memory corruption in the browser process, we generally reward between $15,000 to $30,000 for bugs that can be exploited via remote content and without requiring direct access to dev tools or series of user interactions such as though accessibility and debug consoles as required with this bug. 
As has always been communicated in our VRP rules, "The amounts listed are for good quality reports that don't require complex or unlikely user interaction." 

As there has been a trend away from reports of issues that can be exploited by remote content and more toward reports for issues that have a strong or sole dependency on user interaction, we have needed to update our policies and rules in order to reflect our priorities for impactful bug reports. This was also directly communicated to the researcher community in February via email: 
"Reports of issues that rely heavily or solely on user interaction, instead of being triggered by remote content, will generally receive significantly reduced rewards. Less convincing or more constrained bug submissions will likely qualify for reduced reward amounts, as chosen at the discretion of the reward panel."

We - the VRP Panel on behalf of Chrome Security-  need to prioritize the issues that have the most impact to our users and can be most damaging when used by an attacker. Memory corruption issues are very harmful and impactful when they can be easily and covertly exploited by an attacker and provide the attacker control once the issue has been triggered. Thus, we have updated our VRP rules and reward policies to reflect this prioritization. 

At the time this was rewarded, based on the information presented, an exceptional amount of unusual user interaction is required to trigger this issue. Not only is it unlikely a user can be reasonably convinced to follow these steps, but even if an attacker could convince the user to do so, there is still limited exploitation potential and they would be left with little control to exploit this issue to meaningful ends. 

https://crbug.com/chromium/1270095#c34 also provided an open invitation to the original researcher to provide further analysis or a new POC or other demonstration requiring less user interaction or improved exploitation potential. Had we would have received such, we would have happily reassessed the issue and provided a reward, similar to the process in https://crbug.com/chromium/1201032. 



### am...@chromium.org (2022-03-13)

I forgot to add, please see https://g.co/chrome/vrp for full VRP rules and policies, especially with regard to the quoted policy language above. 

### sa...@gmail.com (2022-03-13)

Hi Amy, Sorry, I didn't know that the technique used in the extension (https://crbug.com/1201032#c39) was different. Thank you for the detailed explanation. :)

### am...@google.com (2022-04-05)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-21)

[Empty comment from Monorail migration]

### ha...@google.com (2022-10-05)

Crash no longer being reported, issue presumed fixed

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1270095?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057908)*
