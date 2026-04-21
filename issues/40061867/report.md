# Security: heap-use-after-free drop_target_event.cc:28 in ui::DropTargetEvent::DropTargetEvent

| Field | Value |
|-------|-------|
| **Issue ID** | [40061867](https://issues.chromium.org/issues/40061867) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Aura |
| **Platforms** | Windows |
| **Reporter** | m....@gmail.com |
| **Assignee** | da...@chromium.org |
| **Created** | 2022-11-22 |
| **Bounty** | $5,000.00 |

## Description

**VERSION**  

WIN10 X64  

asan-win32-release\_x64-1073735

**REPRODUCTION CASE**  

chrome --no-sandbox --user-data-dir=test  

Drag file in the chrome window

Type of crash: [browser process]

RCA  

Coming soon

# ASAN

==5452==ERROR: AddressSanitizer: heap-use-after-free on address 0x128e498aa670 at pc 0x7ffcd6b64179 bp 0x00fc037fd920 sp 0x00fc037fd968  

READ of size 1 at 0x128e498aa670 thread T0  

==5452==WARNING: Failed to use and restart external symbolizer!  

#0 0x7ffcd6b64178 in base::internal::`anonymous namespace'::CrashImmediatelyOnUseAfterFree C:\b\s\w\ir\cache\builder\src\base\memory\raw\_ptr.cc:162  

#1 0x7ffcd6b63ddb in base::internal::AsanBackupRefPtrImpl::AsanCheckIfValidDereference C:\b\s\w\ir\cache\builder\src\base\memory\raw\_ptr.cc:174  

#2 0x7ffcd7f45bb7 in ui::DropTargetEvent::DropTargetEvent C:\b\s\w\ir\cache\builder\src\ui\base\dragdrop\drop\_target\_event.cc:28  

#3 0x7ffcd26df218 in base::internal::FunctorTraits<void (content::WebContentsViewAura::\*)(ui::DropTargetEvent, std::Cr::unique\_ptr<content::DropData,std::Cr::default\_delete[content::DropData](javascript:void(0);) >, base::WeakPtr[content::RenderWidgetHostViewBase](javascript:void(0);), absl::optional[gfx::PointF](javascript:void(0);)),void>::Invoke<void (content::WebContentsViewAura::\*)(ui::DropTargetEvent, std::Cr::unique\_ptr<content::DropData,std::Cr::default\_delete[content::DropData](javascript:void(0);) >, base::WeakPtr[content::RenderWidgetHostViewBase](javascript:void(0);), absl::optional[gfx::PointF](javascript:void(0);)),base::WeakPtr[content::WebContentsViewAura](javascript:void(0);),ui::DropTargetEvent,std::Cr::unique\_ptr<content::DropData,std::Cr::default\_delete[content::DropData](javascript:void(0);) >,base::WeakPtr[content::RenderWidgetHostViewBase](javascript:void(0);),absl::optional[gfx::PointF](javascript:void(0);) > C:\b\s\w\ir\cache\builder\src\base\functional\bind\_internal.h:669  

#4 0x7ffcd26def5b in base::internal::Invoker<base::internal::BindState<void (content::WebContentsViewAura::\*)(ui::DropTargetEvent, std::Cr::unique\_ptr<content::DropData,std::Cr::default\_delete[content::DropData](javascript:void(0);) >, base::WeakPtr[content::RenderWidgetHostViewBase](javascript:void(0);), absl::optional[gfx::PointF](javascript:void(0);)),base::WeakPtr[content::WebContentsViewAura](javascript:void(0);),ui::DropTargetEvent,std::Cr::unique\_ptr<content::DropData,std::Cr::default\_delete[content::DropData](javascript:void(0);) > >,void (base::WeakPtr[content::RenderWidgetHostViewBase](javascript:void(0);), absl::optional[gfx::PointF](javascript:void(0);))>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind\_internal.h:893  

#5 0x7ffcd23554cd in content::RenderWidgetTargeter::TargetingRequest::RunCallback C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\render\_widget\_targeter.cc:136  

#6 0x7ffcd2357b4f in content::RenderWidgetTargeter::FoundTarget C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\render\_widget\_targeter.cc:427  

#7 0x7ffcd23598b2 in content::RenderWidgetTargeter::FoundFrameSinkId C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\render\_widget\_targeter.cc:405  

#8 0x7ffcd235e7a1 in base::internal::FunctorTraits<void (content::RenderWidgetTargeter::\*)(base::WeakPtr[content::RenderWidgetHostViewBase](javascript:void(0);), unsigned int, const gfx::PointF &, content::TracingUmaTracker, const viz::FrameSinkId &, const gfx::PointF &),void>::Invoke<void (content::RenderWidgetTargeter::\*)(base::WeakPtr[content::RenderWidgetHostViewBase](javascript:void(0);), unsigned int, const gfx::PointF &, content::TracingUmaTracker, const viz::FrameSinkId &, const gfx::PointF &),base::WeakPtr[content::RenderWidgetTargeter](javascript:void(0);),base::WeakPtr[content::RenderWidgetHostViewBase](javascript:void(0);),unsigned int,gfx::PointF,content::TracingUmaTracker,const viz::FrameSinkId &,const gfx::PointF &> C:\b\s\w\ir\cache\builder\src\base\functional\bind\_internal.h:669  

#9 0x7ffcd235e55e in base::internal::Invoker<base::internal::BindState<void (content::RenderWidgetTargeter::\*)(base::WeakPtr[content::RenderWidgetHostViewBase](javascript:void(0);), unsigned int, const gfx::PointF &, content::TracingUmaTracker, const viz::FrameSinkId &, const gfx::PointF &),base::WeakPtr[content::RenderWidgetTargeter](javascript:void(0);),base::WeakPtr[content::RenderWidgetHostViewBase](javascript:void(0);),unsigned int,gfx::PointF,content::TracingUmaTracker>,void (const viz::FrameSinkId &, const gfx::PointF &)>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind\_internal.h:893  

#10 0x7ffccd69fc18 in viz::mojom::InputTargetClient\_FrameSinkIdAt\_ForwardToCallback::Accept C:\b\s\w\ir\cache\builder\src\out\Release\_x64\gen\services\viz\public\mojom\hit\_test\input\_target\_client.mojom.cc:250  

#11 0x7ffcd6f2fd16 in mojo::InterfaceEndpointClient::HandleValidatedMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface\_endpoint\_client.cc:1002  

#12 0x7ffcd9dd2b6a in mojo::MessageDispatcher::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\message\_dispatcher.cc:43  

#13 0x7ffcd6f33bc6 in mojo::InterfaceEndpointClient::HandleIncomingMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface\_endpoint\_client.cc:694  

#14 0x7ffcd6f4a767 in mojo::internal::MultiplexRouter::ProcessIncomingMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\multiplex\_router.cc:1102  

#15 0x7ffcd6f4956d in mojo::internal::MultiplexRouter::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\multiplex\_router.cc:716  

#16 0x7ffcd9dd2b6a in mojo::MessageDispatcher::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\message\_dispatcher.cc:43  

#17 0x7ffcd6f29f00 in mojo::Connector::DispatchMessageW C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\connector.cc:561  

#18 0x7ffcd6f2b748 in mojo::Connector::ReadAllAvailableMessages C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\connector.cc:618  

#19 0x7ffcd6f2d11b in base::internal::Invoker<base::internal::BindState<void (mojo::Connector::\*)(unsigned int),base::internal::UnretainedWrapper[mojo::Connector,base::RawPtrBanDanglingIfSupported](javascript:void(0);) >,void (unsigned int)>::Run C:\b\s\w\ir\cache\builder\src\base\functional\bind\_internal.h:906  

#20 0x7ffcccd9c29f in base::RepeatingCallback<void (media::CdmContext::Event)>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:333  

#21 0x7ffccd7602c2 in base::internal::Invoker<base::internal::BindState<void (\*)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &),base::RepeatingCallback<void (unsigned int)> >,void (unsigned int, const mojo::HandleSignalsState &)>::Run C:\b\s\w\ir\cache\builder\src\base\functional\bind\_internal.h:906  

#22 0x7ffcca5c42a9 in base::RepeatingCallback<void (net::MDnsTransaction::Result, const net::RecordParsed \*)>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:333  

#23 0x7ffcd6f8826f in mojo::SimpleWatcher::OnHandleReady C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\system\simple\_watcher.cc:278  

#24 0x7ffcd6f8928c in base::internal::Invoker<base::internal::BindState<void (mojo::SimpleWatcher::\*)(int, unsigned int, const mojo::HandleSignalsState &),base::WeakPtr[mojo::SimpleWatcher](javascript:void(0);),int,unsigned int,mojo::HandleSignalsState>,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind\_internal.h:893  

#25 0x7ffcd6c5dc39 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:156  

#26 0x7ffcd9c69c61 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:449  

#27 0x7ffcd9c68752 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:300  

#28 0x7ffcd6d0f802 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:214  

#29 0x7ffcd6d0d980 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:78  

#30 0x7ffcd9c6c093 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:609  

#31 0x7ffcd6bea5de in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:141  

#32 0x7ffcd14721fd in content::BrowserMainLoop::RunMainMessageLoop C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_loop.cc:1048  

#33 0x7ffcd1478a9b in content::BrowserMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_runner\_impl.cc:162  

#34 0x7ffcd146af31 in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main.cc:32  

#35 0x7ffcd67a0305 in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:692  

#36 0x7ffcd67a3afd in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1230  

#37 0x7ffcd67a326e in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1086  

#38 0x7ffcd679e38e in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:344  

#39 0x7ffcd679f1e9 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:372  

#40 0x7ffcca1414a5 in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc:174  

#41 0x7ff6f2b26288 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main\_dll\_loader\_win.cc:166  

#42 0x7ff6f2b22c0a in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_exe\_main\_win.cc:391  

#43 0x7ff6f2f55fcb in \_\_scrt\_common\_main\_seh d:\a01\_work\12\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#44 0x7ffd6f9f244c in BaseThreadInitThunk+0x1c (C:\WINDOWS\System32\KERNEL32.DLL+0x18001244c)  

#45 0x7ffd7158dfb7 in RtlUserThreadStart+0x27 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x18005dfb7)

0x128e498aa670 is located 0 bytes inside of 8-byte region [0x128e498aa670,0x128e498aa678)  

freed by thread T0 here:  

#0 0x7ff6f2bd541d in free C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:82  

#1 0x7ffce4e5109c in views::DesktopDropTargetWin::OnDragOver C:\b\s\w\ir\cache\builder\src\ui\views\widget\desktop\_aura\desktop\_drop\_target\_win.cc:84  

#2 0x7ffce4e51ff5 in ui::DropTargetWin::DragOver C:\b\s\w\ir\cache\builder\src\ui\base\dragdrop\drop\_target\_win.cc:68  

#3 0x7ffd702952eb in DoDragDrop+0x110b (C:\WINDOWS\System32\ole32.dll+0x1800352eb)  

#4 0x7ffd71435542 in NdrNsSendReceive+0x322 (C:\WINDOWS\System32\RPCRT4.dll+0x180065542)  

#5 0x7ffd714a2bf9 in NdrClientCall3+0x1c99 (C:\WINDOWS\System32\RPCRT4.dll+0x1800d2bf9)  

#6 0x7ffd71412bd2 in NdrStubCall3+0xd2 (C:\WINDOWS\System32\RPCRT4.dll+0x180042bd2)  

#7 0x7ffd70f95cfe in CStdStubBuffer\_Invoke+0x6e (C:\WINDOWS\System32\combase.dll+0x1800c5cfe)  

#8 0x7ffd70f6df5c in WindowsGetStringRawBuffer+0x163c (C:\WINDOWS\System32\combase.dll+0x18009df5c)  

#9 0x7ffd70f6dce7 in WindowsGetStringRawBuffer+0x13c7 (C:\WINDOWS\System32\combase.dll+0x18009dce7)  

#10 0x7ffd70f990e0 in Ordinal67+0x6b0 (C:\WINDOWS\System32\combase.dll+0x1800c90e0)  

#11 0x7ffd70f70d16 in DllGetClassObject+0x7f6 (C:\WINDOWS\System32\combase.dll+0x1800a0d16)  

#12 0x7ffd70f195b8 in CoWaitForMultipleHandles+0x2e8 (C:\WINDOWS\System32\combase.dll+0x1800495b8)  

#13 0x7ffd70f76798 in DllGetClassObject+0x6278 (C:\WINDOWS\System32\combase.dll+0x1800a6798)  

#14 0x7ffd70f39f47 in Ordinal87+0x8c7 (C:\WINDOWS\System32\combase.dll+0x180069f47)  

#15 0x7ffd70f3a818 in Ordinal87+0x1198 (C:\WINDOWS\System32\combase.dll+0x18006a818)  

#16 0x7ffd6f528160 in DispatchMessageW+0x740 (C:\WINDOWS\System32\USER32.dll+0x180018160)  

#17 0x7ffd6f527c20 in DispatchMessageW+0x200 (C:\WINDOWS\System32\USER32.dll+0x180017c20)  

#18 0x7ffcd6d12036 in base::MessagePumpForUI::ProcessMessageHelper C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:531  

#19 0x7ffcd6d1001a in base::MessagePumpForUI::ProcessNextWindowsMessage C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:498  

#20 0x7ffcd6d0f9fa in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:209  

#21 0x7ffcd6d0d980 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:78  

#22 0x7ffcd9c6c093 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:609  

#23 0x7ffcd6bea5de in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:141  

#24 0x7ffcd14721fd in content::BrowserMainLoop::RunMainMessageLoop C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_loop.cc:1048  

#25 0x7ffcd1478a9b in content::BrowserMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_runner\_impl.cc:162  

#26 0x7ffcd146af31 in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main.cc:32  

#27 0x7ffcd67a0305 in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:692

previously allocated by thread T0 here:  

#0 0x7ff6f2bd551d in malloc C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:98  

#1 0x7ffceb32f05e in operator new d:\a01\_work\12\s\src\vctools\crt\vcstartup\src\heap\new\_scalar.cpp:35  

#2 0x7ffce4e508ea in views::DesktopDropTargetWin::Translate C:\b\s\w\ir\cache\builder\src\ui\views\widget\desktop\_aura\desktop\_drop\_target\_win.cc:146  

#3 0x7ffce4e50f39 in views::DesktopDropTargetWin::OnDragOver C:\b\s\w\ir\cache\builder\src\ui\views\widget\desktop\_aura\desktop\_drop\_target\_win.cc:79  

#4 0x7ffce4e51ff5 in ui::DropTargetWin::DragOver C:\b\s\w\ir\cache\builder\src\ui\base\dragdrop\drop\_target\_win.cc:68  

#5 0x7ffd702952eb in DoDragDrop+0x110b (C:\WINDOWS\System32\ole32.dll+0x1800352eb)  

#6 0x7ffd71435542 in NdrNsSendReceive+0x322 (C:\WINDOWS\System32\RPCRT4.dll+0x180065542)  

#7 0x7ffd714a2bf9 in NdrClientCall3+0x1c99 (C:\WINDOWS\System32\RPCRT4.dll+0x1800d2bf9)  

#8 0x7ffd71412bd2 in NdrStubCall3+0xd2 (C:\WINDOWS\System32\RPCRT4.dll+0x180042bd2)  

#9 0x7ffd70f95cfe in CStdStubBuffer\_Invoke+0x6e (C:\WINDOWS\System32\combase.dll+0x1800c5cfe)  

#10 0x7ffd70f6df5c in WindowsGetStringRawBuffer+0x163c (C:\WINDOWS\System32\combase.dll+0x18009df5c)  

#11 0x7ffd70f6dce7 in WindowsGetStringRawBuffer+0x13c7 (C:\WINDOWS\System32\combase.dll+0x18009dce7)  

#12 0x7ffd70f990e0 in Ordinal67+0x6b0 (C:\WINDOWS\System32\combase.dll+0x1800c90e0)  

#13 0x7ffd70f70d16 in DllGetClassObject+0x7f6 (C:\WINDOWS\System32\combase.dll+0x1800a0d16)  

#14 0x7ffd70f195b8 in CoWaitForMultipleHandles+0x2e8 (C:\WINDOWS\System32\combase.dll+0x1800495b8)  

#15 0x7ffd70f76798 in DllGetClassObject+0x6278 (C:\WINDOWS\System32\combase.dll+0x1800a6798)  

#16 0x7ffd70f39f47 in Ordinal87+0x8c7 (C:\WINDOWS\System32\combase.dll+0x180069f47)  

#17 0x7ffd70f3a818 in Ordinal87+0x1198 (C:\WINDOWS\System32\combase.dll+0x18006a818)  

#18 0x7ffd6f528160 in DispatchMessageW+0x740 (C:\WINDOWS\System32\USER32.dll+0x180018160)  

#19 0x7ffd6f527c20 in DispatchMessageW+0x200 (C:\WINDOWS\System32\USER32.dll+0x180017c20)  

#20 0x7ffcd6d12036 in base::MessagePumpForUI::ProcessMessageHelper C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:531  

#21 0x7ffcd6d1001a in base::MessagePumpForUI::ProcessNextWindowsMessage C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:498  

#22 0x7ffcd6d0f9fa in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:209  

#23 0x7ffcd6d0d980 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:78  

#24 0x7ffcd9c6c093 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:609  

#25 0x7ffcd6bea5de in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:141  

#26 0x7ffcd14721fd in content::BrowserMainLoop::RunMainMessageLoop C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_loop.cc:1048  

#27 0x7ffcd1478a9b in content::BrowserMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_runner\_impl.cc:162

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\s\w\ir\cache\builder\src\base\memory\raw\_ptr.cc:162 in base::internal::`anonymous namespace'::CrashImmediatelyOnUseAfterFree  

Shadow bytes around the buggy address:  

0x128e498aa380: f7 fa fd fa f7 fa fd fd f7 fa fd fa f7 fa fd fd  

0x128e498aa400: f7 fa fd fa f7 fa fd fd f7 fa fd fa f7 fa fd fd  

0x128e498aa480: f7 fa fd fa f7 fa fd fd f7 fa fd fa f7 fa fd fd  

0x128e498aa500: f7 fa fd fa f7 fa fd fd f7 fa 00 fa f7 fa fd fd  

0x128e498aa580: f7 fa fd fd f7 fa fd fd f7 fa fd fa f7 fa fd fd  

=>0x128e498aa600: f7 fa fd fd f7 fa fd fa f7 fa fd fd f7 fa[fd]fa  

0x128e498aa680: f7 fa fd fa f7 fa fd fd f7 fa fd fa f7 fa fd fa  

0x128e498aa700: f7 fa fd fa f7 fa fd fa f7 fa fd fa f7 fa fd fa  

0x128e498aa780: f7 fa fd fd f7 fa fd fa f7 fa fd fa f7 fa fd fa  

0x128e498aa800: f7 fa 00 00 f7 fa fd fa f7 fa 00 00 f7 fa fd fa  

0x128e498aa880: f7 fa fd fa f7 fa fd fa f7 fa fd fa f7 fa fd fa  

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

MiraclePtr Status: PROTECTED  

This crash occurred while a raw\_ptr<T> object containing a dangling pointer was being dereferenced.  

MiraclePtr is expected to make this crash non-exploitable once fully enabled.  

Refer to <https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md> for details.  

==5452==ABORTING

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 17.7 KB)
- [Video.mp4](attachments/Video.mp4) (video/mp4, 3.1 MB)
- deleted (application/octet-stream, 0 B)

## Timeline

### [Deleted User] (2022-11-22)

[Empty comment from Monorail migration]

### m....@gmail.com (2022-11-22)

[Empty comment from Monorail migration]

### m....@gmail.com (2022-11-22)

[Comment Deleted]

### m....@gmail.com (2022-11-22)

RCA
1. OnDragOver onwer data&event by unique_ptr	[1]
2. data&event assgin by OnDragOver->Translate	[2]
3. In function Translate,data&event will pass as raw ptr[3] and finally use by async mojo call
4. So when OnDragOver return,data&event will get free,and use when mojo function get call

https://source.chromium.org/chromium/chromium/src/+/main:ui/views/widget/desktop_aura/desktop_drop_target_win.cc;drc=3e1a26c44c024d97dc9a4c09bbc6a2365398ca2c;l=71
```
DWORD DesktopDropTargetWin::OnDragOver(IDataObject* data_object,
                                       DWORD key_state,
                                       POINT position,
                                       DWORD effect) {
  int drag_operation = ui::DragDropTypes::DRAG_NONE;
  std::unique_ptr<OSExchangeData> data;									***1***
  std::unique_ptr<ui::DropTargetEvent> event;
  DragDropDelegate* delegate;
  Translate(data_object, key_state, position, effect, &data, &event, &delegate);
  if (delegate)
    drag_operation = delegate->OnDragUpdated(*event).drag_operation;

  return ui::DragDropTypes::DragOperationToDropEffect(drag_operation);
}

```

https://source.chromium.org/chromium/chromium/src/+/main:ui/views/widget/desktop_aura/desktop_drop_target_win.cc;drc=3e1a26c44c024d97dc9a4c09bbc6a2365398ca2c;l=117
```
void DesktopDropTargetWin::Translate(
    IDataObject* data_object,
    DWORD key_state,
    POINT position,
    DWORD effect,
    std::unique_ptr<OSExchangeData>* data,
    std::unique_ptr<ui::DropTargetEvent>* event,
    DragDropDelegate** delegate) {
***CUT***

  *data = std::make_unique<OSExchangeData>(								***2***
      std::make_unique<OSExchangeDataProviderWin>(data_object));
  location = root_location;
  aura::Window::ConvertPointToTarget(root_window_, target_window_, &location);
  *event = std::make_unique<ui::DropTargetEvent>(
      *(data->get()), gfx::PointF(location), gfx::PointF(root_location),
      ui::DragDropTypes::DropEffectToDragOperation(effect));
  (*event)->set_flags(ConvertKeyStateToAuraEventFlags(key_state));
  if (target_window_changed)
    (*delegate)->OnDragEntered(*event->get());							***3***
}
```

### m....@gmail.com (2022-11-22)

[Empty comment from Monorail migration]

### ct...@chromium.org (2022-11-22)

Thanks for your report and the additional analysis! One quick question to help me assess severity and for reproducing: is this limited to the new tab page (as shown in your video in https://crbug.com/chromium/1392661#c5), or have you found drag interactions that can trigger this on attacker-controlled pages as well?

(In the meantime, I'll work on repro-ing and determining labels based on your report so far)

### ct...@chromium.org (2022-11-22)

Another question: Are you able to reproduce this without the --no-sandbox flag?

### m....@gmail.com (2022-11-23)

 --no-sandbox is just to make it easier to generate ASAN logs, and has nothing to do with the vulnerability itself.

Based on the current test, it seems that it is only triggered on the new tab. I am not sure if it can be triggered on attacker-controlled pages as well.

### ct...@chromium.org (2022-11-29)

Thanks. I'm able to reproduce this on a r1073735 ASAN build on Windows, as well as r1047710 (roughly M107) but not r1036825 (roughly M106).

From the stacktrace, it seems likely that this is a Windows-only crash, but please let us know if you're able to repro this on other platforms. Also, if you are able to provide more on the potential exploitability of this that would be very helpfiul -- it seems based on the stacktrace and the repro that this would be difficult for an attacker to use (i.e., it is a crash involving UI objects rather than the underlying shortcut data which could be attacker controlled).

Triaging to Windows UI folks and setting some security labels. robliao@ could you take a look or route to the right Windows UI owner?

- FoundIn-107: I'm able to reproduce this back to M107 (current Stable)
- Security_Severity-High: Conservatively setting this to High as it is a browser-process UAF but it requires specific user interactions on the NTP.

[Monorail components: UI>Aura]

### [Deleted User] (2022-11-29)

[Empty comment from Monorail migration]

### ro...@chromium.org (2022-11-29)

Routing to dayeung for Windows + DragDrop.

### [Deleted User] (2022-11-29)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-11-29)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-30)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-12-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/9f4b5761c546a118b7187c0c7ddcb9ee5756f32c

commit 9f4b5761c546a118b7187c0c7ddcb9ee5756f32c
Author: David Yeung <dayeung@chromium.org>
Date: Thu Dec 01 19:38:56 2022

Fix UaF in ui::DropTargetEvent::DropTargetEvent.

There is an async operation in WebContentsViewAura that uses a ui::DropTargetEvent. DropTargetEvent has a pointer to OSExchangeData which gets destroyed before the async operation is called. This triggers the UaF because the operation attempts to reference a freed object (OSExchangeData).

Fix is for WebContentsViewAura::DragUpdatedCallback to use a DropMetadata struct instead of a ui::DropTargetEvent. This is the same pattern used by other callbacks in WebContentsViewAura.

Bug: 1392661
Change-Id: I3c62a7473ef9b6cdd223f75fbda50671f539f9eb
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4070787
Reviewed-by: Avi Drissman <avi@chromium.org>
Commit-Queue: David Yeung <dayeung@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1078218}

[modify] https://crrev.com/9f4b5761c546a118b7187c0c7ddcb9ee5756f32c/content/browser/web_contents/web_contents_view_aura.h
[modify] https://crrev.com/9f4b5761c546a118b7187c0c7ddcb9ee5756f32c/content/browser/web_contents/web_contents_view_aura.cc


### [Deleted User] (2022-12-06)

dayeung: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### da...@chromium.org (2022-12-06)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-06)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-06)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-06)

Requesting merge to stable M108 because latest trunk commit (1078218) appears to be after stable branch point (1058933).

Requesting merge to beta M109 because latest trunk commit (1078218) appears to be after beta branch point (1070088).

Merge review required: M108 is already shipping to stable.

Merge review required: M109 is already shipping to beta.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [108, 109].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### da...@chromium.org (2022-12-06)

1. https://crrev.com/c/4070787
2. Yes, it's been verified in Canary
3. It's been verified with existing tests and manual testing. No known regressions or risks.
4. No, there aren't known compatibility risks.
5. I'm not sure if it's necessary. Test team can verify by launching Chrome ASAN build. Open "New tab" page. Drag a bookmark item to the address bar. Confirm it does not crash

### [Deleted User] (2022-12-07)

Requesting merge to stable M108 because latest trunk commit (1078218) appears to be after stable branch point (1058933).

Requesting merge to beta M109 because latest trunk commit (1078218) appears to be after beta branch point (1070088).

Merge review required: M108 is already shipping to stable.

Merge review required: M109 is already shipping to beta.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [108, 109].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-12-07)

M109 merge approved, please merge this fix to branch 5414 at your earliest convenience 
M108 merge approved, please merge this fix to branch 5359 at soonest / NLT 10am Friday PT, so this fix can be included in the M108/Stable security refresh 


### ad...@google.com (2022-12-08)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-12-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/eed5a4de2c40ce0a35e6412177178b4ef22a7239

commit eed5a4de2c40ce0a35e6412177178b4ef22a7239
Author: David Yeung <dayeung@chromium.org>
Date: Thu Dec 08 17:56:44 2022

Fix UaF in ui::DropTargetEvent::DropTargetEvent.

There is an async operation in WebContentsViewAura that uses a ui::DropTargetEvent. DropTargetEvent has a pointer to OSExchangeData which gets destroyed before the async operation is called. This triggers the UaF because the operation attempts to reference a freed object (OSExchangeData).

Fix is for WebContentsViewAura::DragUpdatedCallback to use a DropMetadata struct instead of a ui::DropTargetEvent. This is the same pattern used by other callbacks in WebContentsViewAura.

(cherry picked from commit 9f4b5761c546a118b7187c0c7ddcb9ee5756f32c)

Bug: 1392661
Change-Id: I3c62a7473ef9b6cdd223f75fbda50671f539f9eb
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4070787
Reviewed-by: Avi Drissman <avi@chromium.org>
Commit-Queue: David Yeung <dayeung@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1078218}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4085256
Cr-Commit-Position: refs/branch-heads/5359@{#1125}
Cr-Branched-From: 27d3765d341b09369006d030f83f582a29eb57ae-refs/heads/main@{#1058933}

[modify] https://crrev.com/eed5a4de2c40ce0a35e6412177178b4ef22a7239/content/browser/web_contents/web_contents_view_aura.h
[modify] https://crrev.com/eed5a4de2c40ce0a35e6412177178b4ef22a7239/content/browser/web_contents/web_contents_view_aura.cc


### gi...@appspot.gserviceaccount.com (2022-12-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/19b9873d220d55b703104a29c3a8a6adfa90f099

commit 19b9873d220d55b703104a29c3a8a6adfa90f099
Author: David Yeung <dayeung@chromium.org>
Date: Thu Dec 08 17:58:25 2022

Fix UaF in ui::DropTargetEvent::DropTargetEvent.

There is an async operation in WebContentsViewAura that uses a ui::DropTargetEvent. DropTargetEvent has a pointer to OSExchangeData which gets destroyed before the async operation is called. This triggers the UaF because the operation attempts to reference a freed object (OSExchangeData).

Fix is for WebContentsViewAura::DragUpdatedCallback to use a DropMetadata struct instead of a ui::DropTargetEvent. This is the same pattern used by other callbacks in WebContentsViewAura.

(cherry picked from commit 9f4b5761c546a118b7187c0c7ddcb9ee5756f32c)

Bug: 1392661
Change-Id: I3c62a7473ef9b6cdd223f75fbda50671f539f9eb
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4070787
Reviewed-by: Avi Drissman <avi@chromium.org>
Commit-Queue: David Yeung <dayeung@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1078218}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4085820
Cr-Commit-Position: refs/branch-heads/5414@{#551}
Cr-Branched-From: 4417ee59d7bf6df7a9c9ea28f7722d2ee6203413-refs/heads/main@{#1070088}

[modify] https://crrev.com/19b9873d220d55b703104a29c3a8a6adfa90f099/content/browser/web_contents/web_contents_view_aura.h
[modify] https://crrev.com/19b9873d220d55b703104a29c3a8a6adfa90f099/content/browser/web_contents/web_contents_view_aura.cc


### am...@chromium.org (2022-12-12)

[Empty comment from Monorail migration]

### pg...@google.com (2022-12-14)

[Empty comment from Monorail migration]

### pg...@google.com (2022-12-14)

[Empty comment from Monorail migration]

### am...@google.com (2022-12-15)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-12-15)

Congratulations! The VRP Panel has decided to award you $5,000 for this mitigated security bug. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2022-12-16)

[Empty comment from Monorail migration]

### ad...@chromium.org (2022-12-20)

[Empty comment from Monorail migration]

### xi...@chromium.org (2022-12-20)

[Empty comment from Monorail migration]

### xi...@chromium.org (2022-12-20)

[Empty comment from Monorail migration]

### xi...@chromium.org (2022-12-20)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-14)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1392661?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1393868, crbug.com/chromium/1394453, crbug.com/chromium/1402093, crbug.com/chromium/1402094]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061867)*
