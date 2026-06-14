# Security: Use-after-free in CPDFXFA_Page::GetDisplayMatrix

| Field | Value |
|-------|-------|
| **Issue ID** | [40092622](https://issues.chromium.org/issues/40092622) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | hu...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2018-10-05 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

Use-after-free in CPDFXFA\_Page::GetDisplayMatrix

**VERSION**  

Operating System: Windows 10  

chrome with pdfium XFA enabled

**REPRODUCTION CASE**

1. Build chrome with XFA enabled
2. open file `poc.pdf` in chrome
3. Click to the button `remerge` to trigger bug

This time, a object `CXFA_FFPageView` is free in the `click` event and after that is uses again by PDFiumEngine. In `click` event, i set up the javascript handler like below:

```
xfa.template.remerge()  

```

Context when crash

```
\*\*\* WARNING: Unable to verify checksum for C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA_03_10_18\src\out\chromium_pdfium_xfa_03_10\chrome.dll  
eax=0093c658 ebx=00000000 ecx=415f6fec edx=0093c658 esi=d3473f26 edi=0093c794  
eip=6405bf4a esp=0093c5a0 ebp=0093c5a4 iopl=0         nv up ei pl nz na po nc  
cs=0023  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00010202  
chrome!fxcrt::UnownedPtr<CXFA_Node>::operator->+0xa:  
6405bf4a 8b01            mov     eax,dword ptr [ecx]  ds:002b:415f6fec=????????  
   
3:054> kp  
 # ChildEBP RetAddr    
00 0093c5a4 6514232b chrome!fxcrt::UnownedPtr<CXFA_Node>::operator->(void)+0xa [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA_03_10_18\src\third_party\pdfium\core\fxcrt\unowned_ptr.h @ 102]   
01 0093c618 64047468 chrome!CXFA_ContainerLayoutItem::GetPageSize(void)+0x3b [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA_03_10_18\src\third_party\pdfium\xfa\fxfa\parser\cxfa_containerlayoutitem.cpp @ 34]   
02 0093c680 63fb431d chrome!CXFA_FFPageView::GetDisplayMatrix(struct FX_RECT \* rtDisp = 0x0093c794, int iRotate = 0n0)+0x48 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA_03_10_18\src\third_party\pdfium\xfa\fxfa\cxfa_ffpageview.cpp @ 127]   
03 0093c6d4 62ae22d9 chrome!CPDFXFA_Page::GetDisplayMatrix(struct FX_RECT \* rect = 0x0093c794, int iRotate = 0n0)+0x12d [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA_03_10_18\src\third_party\pdfium\fpdfsdk\fpdfxfa\cpdfxfa_page.cpp @ 182]   
04 0093c7b8 62ae219f chrome!`anonymous namespace'::FFLCommon(struct fpdf_form_handle_t__ \* hHandle = 0x131f2fb0, struct fpdf_bitmap_t__ \* bitmap = 0x2ab6cfd0, void \* recorder = 0x00000000, struct fpdf_page_t__ \* fpdf_page = 0x2ad8afe0, int start_x = 0n3, int start_y = 0n3, int size_x = 0n816, int size_y = 0n1056, int rotate = 0n0, int flags = 0n259)+0x129 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA_03_10_18\src\third_party\pdfium\fpdfsdk\fpdf_formfill.cpp @ 186]   
05 0093c83c 61a11d5b chrome!FPDF_FFLDraw(struct fpdf_form_handle_t__ \* hHandle = 0x131f2fb0, struct fpdf_bitmap_t__ \* bitmap = 0x2ab6cfd0, struct fpdf_page_t__ \* page = 0x2ad8afe0, int start_x = 0n3, int start_y = 0n3, int size_x = 0n816, int size_y = 0n1056, int rotate = 0n0, int flags = 0n259)+0xbf [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA_03_10_18\src\third_party\pdfium\fpdfsdk\fpdf_formfill.cpp @ 576]   
06 0093cb70 61a10fbd chrome!chrome_pdf::PDFiumEngine::FinishPaint(int progressive_index = 0n0, class pp::ImageData \* image_data = 0x345c6d84)+0x38b [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA_03_10_18\src\pdf\pdfium\pdfium_engine.cc @ 2965]   
07 0093d038 61a3df0a chrome!chrome_pdf::PDFiumEngine::Paint(class pp::Rect \* rect = 0x0093d2bc, class pp::ImageData \* image_data = 0x345c6d84, class std::vector<pp::Rect,std::allocator<pp::Rect> > \* ready = 0x0093d2ac { size=0 }, class std::vector<pp::Rect,std::allocator<pp::Rect> > \* pending = 0x0093d29c { size=0 })+0x7cd [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA_03_10_18\src\pdf\pdfium\pdfium_engine.cc @ 817]   
08 0093d434 62b02ea1 chrome!chrome_pdf::OutOfProcessInstance::OnPaint(class std::vector<pp::Rect,std::allocator<pp::Rect> > \* paint_rects = 0x0093d5e0 { size=1 }, class std::vector<PaintManager::ReadyRect,std::allocator<PaintManager::ReadyRect> > \* ready = 0x0093d628 { size=0 }, class std::vector<pp::Rect,std::allocator<pp::Rect> > \* pending = 0x0093d618 { size=0 })+0x50a [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA_03_10_18\src\pdf\out_of_process_instance.cc @ 1180]   
09 0093d708 62b03d41 chrome!PaintManager::DoPaint(void)+0x311 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA_03_10_18\src\pdf\paint_manager.cc @ 237]   
0a 0093d7fc 62b04196 chrome!PaintManager::OnFlushComplete(void)+0xe1 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA_03_10_18\src\pdf\paint_manager.cc @ 331]   
0b 0093d81c 62b040ef chrome!pp::CompletionCallbackFactory<PaintManager,pp::ThreadSafeThreadTraits>::Dispatcher0<void (class PaintManager \* object = 0x345c6e08, int result = 0n0)+0x36 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA_03_10_18\src\ppapi\utility\completion_callback_factory.h @ 607]   
\*\*\* WARNING: Unable to verify checksum for C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA_03_10_18\src\out\chromium_pdfium_xfa_03_10\ppapi_shared.dll  
0c 0093d840 22d70b8b chrome!pp::CompletionCallbackFactory<PaintManager,pp::ThreadSafeThreadTraits>::CallbackData<pp::CompletionCallbackFactory<PaintManager,pp::ThreadSafeThreadTraits>::Dispatcher0<void (void \* user_data = 0x33e4eff0, int result = 0n0)+0x3f [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA_03_10_18\src\ppapi\utility\completion_callback_factory.h @ 584]   
0d 0093d860 22d70b37 ppapi_shared!PP_RunCompletionCallback(struct PP_CompletionCallback \* cc = 0x33fa2fe0, int result = 0n0)+0x2b [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA_03_10_18\src\ppapi\c\pp_completion_callback.h @ 241]   
0e 0093d88c 22d7010e ppapi_shared!ppapi::CallWhileUnlocked<void,PP_CompletionCallback \*,int,PP_CompletionCallback \*,int>(<function> \* function = 0x22d70b60, struct PP_CompletionCallback \*\* p1 = 0x0093d8dc, int \* p2 = 0x0093d8fc)+0x47 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA_03_10_18\src\ppapi\shared_impl\proxy_lock.h @ 136]   
0f 0093d8f4 23a48971 ppapi_shared!ppapi::TrackedCallback::Run(int result = 0n0)+0x1be [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA_03_10_18\src\ppapi\shared_impl\tracked_callback.cc @ 141]   
10 0093d90c 23a48fff ppapi_proxy!ppapi::proxy::Graphics2DResource::OnPluginMsgFlushACK(class ppapi::proxy::ResourceMessageReplyParams \* params = 0x4180afe0)+0x31 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA_03_10_18\src\ppapi\proxy\graphics_2d_resource.cc @ 160]   
11 0093d934 23a48f0c ppapi_proxy!base::internal::FunctorTraits<void (<function> \* method = 0x23a48940, class scoped_refptr<ppapi::proxy::Graphics2DResource> \* receiver_ptr = 0x33d8aff0 [0x2] 0x30878f88 {...}, class ppapi::proxy::ResourceMessageReplyParams \* args = 0x4180afe0)+0x4f [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA_03_10_18\src\base\bind_internal.h @ 516]   
12 0093d974 23a48e86 ppapi_proxy!base::internal::InvokeHelper<0,void>::MakeItSo<void (<function> \*\* functor = 0x33d8afe8, class scoped_refptr<ppapi::proxy::Graphics2DResource> \* args = 0x33d8aff0 [0x2] 0x30878f88 {...}, class ppapi::proxy::ResourceMessageReplyParams \* args = 0x4180afe0)+0x7c [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA_03_10_18\src\base\bind_internal.h @ 616]   
13 0093d9a0 23a48d64 ppapi_proxy!base::internal::Invoker<base::internal::BindState<void (<function> \*\* functor = 0x33d8afe8, class std::tuple<scoped_refptr<ppapi::proxy::Graphics2DResource> > \* bound = 0x33d8aff0 [0x2] 0x30878f88 {...}, class ppapi::proxy::ResourceMessageReplyParams \* unbound_args = 0x4180afe0)+0x66 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA_03_10_18\src\base\bind_internal.h @ 689]   
14 0093d9d0 239fd69d ppapi_proxy!base::internal::Invoker<base::internal::BindState<void (class base::internal::BindStateBase \* base = 0x33d8afd0, class ppapi::proxy::ResourceMessageReplyParams \* unbound_args = 0x4180afe0)+0x54 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA_03_10_18\src\base\bind_internal.h @ 671]   
15 0093d9f8 239fd627 ppapi_proxy!base::RepeatingCallback<void (class ppapi::proxy::ResourceMessageReplyParams \* args = 0x4180afe0)+0x4d [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA_03_10_18\src\base\callback.h @ 129]   
16 0093da18 239fd53a ppapi_proxy!ppapi::proxy::DispatchResourceReplyImpl<base::RepeatingCallback<void (class base::RepeatingCallback<void (const ppapi::proxy::ResourceMessageReplyParams &)> \* callback = 0x436c6ff4, class ppapi::proxy::ResourceMessageReplyParams \* params = 0x4180afe0, class std::tuple<> \* args_tuple = 0x0093da9c)+0x37 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA_03_10_18\src\ppapi\proxy\dispatch_reply_message.h @ 58]   
17 0093da58 23a4a114 ppapi_proxy!ppapi::proxy::DispatchResourceReply<base::RepeatingCallback<void (class base::RepeatingCallback<void (const ppapi::proxy::ResourceMessageReplyParams &)> \* callback = 0x436c6ff4, class ppapi::proxy::ResourceMessageReplyParams \* params = 0x4180afe0, class std::tuple<> \* args_tuple = 0x0093da9c)+0x6a [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA_03_10_18\src\ppapi\proxy\dispatch_reply_message.h @ 69]   
18 0093db68 23a49f63 ppapi_proxy!ppapi::proxy::DispatchResourceReplyOrDefaultParams<IPC::MessageT<PpapiPluginMsg_Graphics2D_FlushAck_Meta>,base::RepeatingCallback<void (class base::RepeatingCallback<void (const ppapi::proxy::ResourceMessageReplyParams &)> \* callback = 0x436c6ff4, class ppapi::proxy::ResourceMessageReplyParams \* reply_params = 0x4180afe0, class IPC::Message \* \*\*\* WARNING: Unable to verify checksum for C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA_03_10_18\src\out\chromium_pdfium_xfa_03_10\message_support.dll  
msg = 0x4180af90 {size = 0x10})+0x154 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA_03_10_18\src\ppapi\proxy\dispatch_reply_message.h @ 143]   
19 0093db90 23a8d200 ppapi_proxy!ppapi::proxy::PluginResourceCallback<IPC::MessageT<PpapiPluginMsg_Graphics2D_FlushAck_Meta>,base::RepeatingCallback<void (class ppapi::proxy::ResourceMessageReplyParams \* reply_params = 0x4180afe0, class IPC::Message \* msg = 0x4180af90 {size = 0x10})+0x33 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA_03_10_18\src\ppapi\proxy\plugin_resource_callback.h @ 41]   
1a 0093dd18 23a89ec5 ppapi_proxy!ppapi::proxy::PluginResource::OnReplyReceived(class ppapi::proxy::ResourceMessageReplyParams \* params = 0x4180afe0, class IPC::Message \* msg = 0x4180af90 {size = 0x10})+0x330 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA_03_10_18\src\ppapi\proxy\plugin_resource.cc @ 55]   
1b 0093de24 23a8c781 ppapi_proxy!ppapi::proxy::PluginMessageFilter::DispatchResourceReply(class ppapi::proxy::ResourceMessageReplyParams \* reply_params = 0x4180afe0, class IPC::Message \* nested_msg = 0x4180af90 {size = 0x10})+0x155 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA_03_10_18\src\ppapi\proxy\plugin_message_filter.cc @ 116]   
1c 0093de4c 23a8c646 ppapi_proxy!base::internal::FunctorTraits<void (<function> \*\* function = 0x4180af8c, class ppapi::proxy::ResourceMessageReplyParams \* args = 0x4180afe0, class IPC::Message \* args = 0x4180af90 {size = 0x10})+0x51 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA_03_10_18\src\base\bind_internal.h @ 416]   
1d 0093de78 23a8c5df ppapi_proxy!base::internal::InvokeHelper<0,void>::MakeItSo<void (<function> \*\* functor = 0x4180af8c, class ppapi::proxy::ResourceMessageReplyParams \* args = 0x4180afe0, class IPC::Message \* args = 0x4180af90 {size = 0x10})+0x56 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA_03_10_18\src\base\bind_internal.h @ 616]   
1e 0093de9c 23a8c48f ppapi_proxy!base::internal::Invoker<base::internal::BindState<void (<function> \*\* functor = 0x4180af8c, class std::tuple<ppapi::proxy::ResourceMessageReplyParams,IPC::Message> \* bound = 0x4180af90)+0x6f [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA_03_10_18\src\base\bind_internal.h @ 689]   
\*\*\* WARNING: Unable to verify checksum for C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA_03_10_18\src\out\chromium_pdfium_xfa_03_10\base.dll  
1f 0093dec4 6b32e890 ppapi_proxy!base::internal::Invoker<base::internal::BindState<void (class base::internal::BindStateBase \* base = 0x4180af78)+0x3f [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA_03_10_18\src\base\bind_internal.h @ 671]   
20 0093dee8 6b391053 base!base::OnceCallback<void (void)+0x50 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA_03_10_18\src\base\callback.h @ 100]   
21 0093e060 6b424c2f base!base::debug::TaskAnnotator::RunTask(char \* queue_function = 0x6b73bb97 "MessageLoop::PostTask", struct base::PendingTask \* pending_task = 0x0093e260)+0x433 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA_03_10_18\src\base\debug\task_annotator.cc @ 101]   
22 0093e21c 6b425129 base!base::MessageLoop::RunTask(struct base::PendingTask \* pending_task = 0x0093e260)+0x38f [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA_03_10_18\src\base\message_loop\message_loop.cc @ 434]   
23 0093e258 6b425608 base!base::MessageLoop::DeferOrRunPendingTask(struct base::PendingTask pending_task = struct base::PendingTask)+0x49 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA_03_10_18\src\base\message_loop\message_loop.cc @ 448]   
24 0093e360 6b430c71 base!base::MessageLoop::DoWork(void)+0x188 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA_03_10_18\src\base\message_loop\message_loop.cc @ 517]   
25 0093e3b0 6b424526 base!base::MessagePumpDefault::Run(class base::MessagePump::Delegate \* delegate = 0x0093e8f0)+0x51 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA_03_10_18\src\base\message_loop\message_pump_default.cc @ 37]   
26 0093e568 6b4f6028 base!base::MessageLoop::Run(bool application_tasks_allowed = true)+0x1e6 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA_03_10_18\src\base\message_loop\message_loop.cc @ 386]   
\*\*\* WARNING: Unable to verify checksum for C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA_03_10_18\src\out\chromium_pdfium_xfa_03_10\content.dll  
27 0093e7f0 57611fcf base!base::RunLoop::Run(void)+0x1e8 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA_03_10_18\src\base\run_loop.cc @ 102]   
28 0093eb88 5b8341af content!content::PpapiPluginMain(struct content::MainFunctionParams \* parameters = 0x0093ec34)+0x52f [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA_03_10_18\src\content\ppapi_plugin\ppapi_plugin_main.cc @ 160]   
29 0093ebc0 5b8352fa content!content::RunOtherNamedProcessTypeMain(class std::basic_string<char,std::char_traits<char>,std::allocator<char> > \* process_type = 0x0093edc8 "ppapi", struct content::MainFunctionParams \* main_function_params = 0x0093ec34, class content::ContentMainDelegate \* delegate = 0x0093f2fc)+0xaf [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA_03_10_18\src\content\app\content_main_runner_impl.cc @ 564]   
2a 0093ede8 5b831a62 content!content::ContentMainRunnerImpl::Run(bool start_service_manager_only = false)+0x3ba [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA_03_10_18\src\content\app\content_main_runner_impl.cc @ 899]   
\*\*\* WARNING: Unable to verify checksum for C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA_03_10_18\src\out\chromium_pdfium_xfa_03_10\embedder.dll  
2b 0093ee00 13fa3ef3 content!content::ContentServiceManagerMainDelegate::RunEmbedderProcess(void)+0x32 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA_03_10_18\src\content\app\content_service_manager_main_delegate.cc @ 53]   
2c 0093f218 5b833fcc embedder!service_manager::Main(struct service_manager::MainParams \* params = 0x0093f23c)+0x713 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA_03_10_18\src\services\service_manager\embedder\main.cc @ 472]   
2d 0093f264 5dce132f content!content::ContentMain(struct content::ContentMainParams \* params = 0x0093f2dc)+0x5c [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA_03_10_18\src\content\app\content_main.cc @ 20]   
\*\*\* WARNING: Unable to verify checksum for chrome.exe  
2e 0093f348 0025b9ef chrome!ChromeMain(struct HINSTANCE__ \* instance = 0x00250000, struct sandbox::SandboxInterfaceInfo \* sandbox_info = 0x0093f3dc, int64 exe_entry_point_ticks = 0n7894161016)+0x1ef [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA_03_10_18\src\chrome\app\chrome_main.cc @ 102]   
2f 0093f480 00251478 chrome_exe!MainDllLoader::Launch(struct HINSTANCE__ \* instance = 0x00250000, class base::TimeTicks exe_entry_point_ticks = class base::TimeTicks)+0x44f [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA_03_10_18\src\chrome\app\main_dll_loader_win.cc @ 201]   
30 0093f7d4 004c8c0e chrome_exe!wWinMain(struct HINSTANCE__ \* instance = 0x00250000, struct HINSTANCE__ \* prev = 0x00000000)+0x478 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA_03_10_18\src\chrome\app\chrome_exe_main_win.cc @ 229]   
31 0093f7ec 004c8d61 chrome_exe!invoke_main(void)+0x1e [f:\dd\vctools\crt\vcstartup\src\startup\exe_common.inl @ 123]   
32 0093f844 004c8e2d chrome_exe!__scrt_common_main_seh(void)+0x151 [f:\dd\vctools\crt\vcstartup\src\startup\exe_common.inl @ 283]   
33 0093f84c 004c8e38 chrome_exe!__scrt_common_main(void)+0xd [f:\dd\vctools\crt\vcstartup\src\startup\exe_common.inl @ 326]   
34 0093f854 754c8484 chrome_exe!wWinMainCRTStartup(void)+0x8 [f:\dd\vctools\crt\vcstartup\src\startup\exe_wwinmain.cpp @ 17]   
35 0093f868 771f305a KERNEL32!BaseThreadInitThunk+0x24  
36 0093f8b0 771f302a ntdll!__RtlUserThreadStart+0x2f  
37 0093f8c0 00000000 ntdll!_RtlUserThreadStart+0x1b  

```

## Attachments

- [poc.pdf](attachments/poc.pdf) (application/pdf, 130.7 KB)
- [log_crash.txt](attachments/log_crash.txt) (text/plain, 22.1 KB)

## Timeline

### me...@chromium.org (2018-10-05)

hnakashima, can you please take a look, and also adjust Security_Impact label? Thanks.

[Monorail components: Internals>Plugins>PDF]

### hn...@chromium.org (2018-10-05)

XFA is not enabled, so impact is none.

### hn...@chromium.org (2018-10-09)

[Empty comment from Monorail migration]

### hn...@chromium.org (2018-10-10)

[Empty comment from Monorail migration]

### cl...@chromium.org (2018-12-11)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6200544575881216.

### cl...@chromium.org (2018-12-11)

Testcase 6200544575881216 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=6200544575881216.

### hu...@gmail.com (2018-12-17)

[Comment Deleted]

### bu...@chromium.org (2019-01-07)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/4ae52355703d27771c30bf6d99dc211083fc86d2

commit 4ae52355703d27771c30bf6d99dc211083fc86d2
Author: Tom Sepez <tsepez@chromium.org>
Date: Mon Jan 07 20:39:29 2019

Do not cache page views in CPDFXFA_Pages

It might change, so look it up anew by index.

Bug: chromium:892574
Change-Id: I76e2bea4f92225860eaa57e6d7faa4b5e3ad9109
Reviewed-on: https://pdfium-review.googlesource.com/c/47810
Reviewed-by: Lei Zhang <thestig@chromium.org>
Commit-Queue: Tom Sepez <tsepez@chromium.org>

[modify] https://crrev.com/4ae52355703d27771c30bf6d99dc211083fc86d2/fpdfsdk/fpdfxfa/cpdfxfa_page.h
[modify] https://crrev.com/4ae52355703d27771c30bf6d99dc211083fc86d2/fpdfsdk/fpdfxfa/cpdfxfa_page.cpp
[modify] https://crrev.com/4ae52355703d27771c30bf6d99dc211083fc86d2/fpdfsdk/fpdfxfa/cpdfxfa_docenvironment.cpp


### bu...@chromium.org (2019-01-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/e9befd5cdef0e772163c1b60a22c1e0938f2d4db

commit e9befd5cdef0e772163c1b60a22c1e0938f2d4db
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Tue Jan 08 01:23:15 2019

Roll src/third_party/pdfium b6f0a1af7b64..4ae52355703d (2 commits)

https://pdfium.googlesource.com/pdfium.git/+log/b6f0a1af7b64..4ae52355703d


git log b6f0a1af7b64..4ae52355703d --date=short --no-merges --format='%ad %ae %s'
2019-01-07 tsepez@chromium.org Do not cache page views in CPDFXFA_Pages
2019-01-07 tsepez@chromium.org Do not cache m_hMixXFAWidget in CPDFSDK_Widget.


Created with:
  gclient setdep -r src/third_party/pdfium@4ae52355703d

The AutoRoll server is located here: https://autoroll.skia.org/r/pdfium-autoroll

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, please contact the current sheriff, who should
be CC'd on the roll, and stop the roller if necessary.



BUG=chromium:892574,chromium:884122
TBR=dsinclair@chromium.org

Change-Id: I158e34719f04b49b974b84fe4de532e7e292ceac
Reviewed-on: https://chromium-review.googlesource.com/c/1399483
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#620564}
[modify] https://crrev.com/e9befd5cdef0e772163c1b60a22c1e0938f2d4db/DEPS


### ts...@chromium.org (2019-01-09)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-01-10)

[Empty comment from Monorail migration]

### na...@google.com (2019-01-14)

[Empty comment from Monorail migration]

### na...@google.com (2019-01-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### pa...@chromium.org (2019-01-17)

Congrats! The Panel decided to reward $3,000 for this report :)

### aw...@google.com (2019-01-21)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-04-18)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2019-04-18)

This issue was migrated from crbug.com/chromium/892574?no_tracker_redirect=1

[Monorail blocking: crbug.com/chromium/62400]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092622)*
