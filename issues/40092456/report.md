# Security: Use-after-free in CPDFSDK_Widget::GetMixXFAWidget

| Field | Value |
|-------|-------|
| **Issue ID** | [40092456](https://issues.chromium.org/issues/40092456) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | hu...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2018-09-14 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

Use-after-free in CPDFSDK\_Widget::GetMixXFAWidget

**VERSION**  

Operating System: Windows 10  

chrome with pdfium XFA enabled

**REPRODUCTION CASE**

1. Build chrome with XFA enabled + enable PageHeap
2. open file `poc.pdf` in chrome

Detail vulnerability

Root cause of this bug is the same with bug `860697` (<https://bugs.chromium.org/p/chromium/issues/detail?id=860697>) but this time i use method `remerge` to trigger delete `CXFA_FFTextEdit` object. So in `enter` event handler, i setup this script

```
xfa.form.remerge()  

```

Details when crash

```
(1da8.1714): Access violation - code c0000005 (first chance)  
First chance exceptions are reported before any exception handling.  
This exception may be expected and handled.  
\*\*\* WARNING: Unable to verify checksum for C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\out\chromium_pdfium_xfa_12_09\chrome.dll  
eax=6e85ef80 ebx=00000000 ecx=6e85efbc edx=e07fbc5a esi=35052ff8 edi=00000004  
eip=64fa155a esp=012fd274 ebp=012fd278 iopl=0         nv up ei pl nz na po nc  
cs=0023  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00210202  
chrome!fxcrt::UnownedPtr<CXFA_Node>::Get+0xa:  
64fa155a 8b01            mov     eax,dword ptr [ecx]  ds:002b:6e85efbc=????????  
\*\*\* WARNING: Unable to verify checksum for C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\out\chromium_pdfium_xfa_12_09\v8.dll  
3:039> kp  
 # ChildEBP RetAddr    
00 012fd278 64fa28f2 chrome!fxcrt::UnownedPtr<CXFA_Node>::Get(void)+0xa [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\core\fxcrt\unowned_ptr.h @ 91]   
01 012fd284 6605ffa1 chrome!CXFA_FFWidget::GetNode(void)+0x12 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\cxfa_ffwidget.h @ 155]   
02 012fd300 650111bb chrome!CPDFSDK_Widget::Synchronize(bool bSynchronizeElse = false)+0x41 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fpdfsdk\cpdfsdk_widget.cpp @ 272]   
03 012fd32c 6501375c chrome!CPDFSDK_InterForm::SynchronizeField(class CPDF_FormField \* pFormField = 0x32b5efd0)+0x7b [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fpdfsdk\cpdfsdk_interform.cpp @ 281]   
04 012fd368 64ff7ec7 chrome!CPDFSDK_InterForm::AfterValueChange(class CPDF_FormField \* pField = 0x32b5efd0)+0x2c [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fpdfsdk\cpdfsdk_interform.cpp @ 600]   
05 012fd380 64ff8cc4 chrome!CPDF_FormField::NotifyAfterValueChange(void)+0x57 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\core\fpdfdoc\cpdf_formfield.cpp @ 911]   
06 012fd454 64ff923a chrome!CPDF_FormField::SetValue(class fxcrt::WideString \* value = 0x35052ff8, bool bDefault = false, NotificationOption notify = kNotify (0n1))+0x334 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\core\fpdfdoc\cpdf_formfield.cpp @ 379]   
07 012fd484 668d0178 chrome!CPDF_FormField::SetValue(class fxcrt::WideString \* value = 0x35052ff8, NotificationOption notify = kNotify (0n1))+0x3a [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\core\fpdfdoc\cpdf_formfield.cpp @ 408]   
08 012fd5ac 668cfe3a chrome!`anonymous namespace'::SetValue(class CPDFSDK_FormFillEnvironment \* pFormFillEnv = 0x33ddcfb0, class fxcrt::WideString \* swFieldName = 0x6e26efec, int nControlIndex = 0n-1, class std::vector<fxcrt::WideString,std::allocator<fxcrt::WideString> > \* strArray = 0x012fd620)+0x228 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\cjs_field.cpp @ 431]   
09 012fd644 668ded56 chrome!CJS_Field::set_value(class CJS_Runtime \* pRuntime = 0x36100f98, class v8::Local<v8::Value> vp = class v8::Local<v8::Value>)+0x20a [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\cjs_field.cpp @ 2167]   
0a 012fd6c0 668c353e chrome!JSPropSetter<CJS_Field,&CJS_Field::set_value>(char \* prop_name_string = 0x674fdf37 "value", char \* class_name_string = 0x67c422c4 "Field", class v8::Local<v8::String> property = class v8::Local<v8::String>, class v8::Local<v8::Value> value = class v8::Local<v8::Value>, class v8::PropertyCallbackInfo<void> \* info = 0x012fd750)+0xd6 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\js_define.h @ 111]   
0b 012fd6fc 18abe113 chrome!CJS_Field::set_value_static(class v8::Local<v8::String> property = class v8::Local<v8::String>, class v8::Local<v8::Value> value = class v8::Local<v8::Value>, class v8::PropertyCallbackInfo<void> \* info = 0x012fd750)+0x5e [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\cjs_field.h @ 91]   
0c 012fd770 18bba4b3 v8!v8::internal::PropertyCallbackArguments::CallAccessorSetter(class v8::internal::Handle<v8::internal::AccessorInfo> accessor_info = class v8::internal::Handle<v8::internal::AccessorInfo>, class v8::internal::Handle<v8::internal::Name> name = class v8::internal::Handle<v8::internal::Name>, class v8::internal::Handle<v8::internal::Object> value = class v8::internal::Handle<v8::internal::Object>)+0x2c3 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\v8\src\api-arguments-inl.h @ 343]   
0d 012fd7e0 18bd0b2a v8!v8::internal::Object::SetPropertyWithAccessor(class v8::internal::LookupIterator \* it = 0x012fd888, class v8::internal::Handle<v8::internal::Object> value = class v8::internal::Handle<v8::internal::Object>, v8::internal::ShouldThrow should_throw = kDontThrow (0n1))+0x203 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\v8\src\objects.cc @ 1706]   
0e 012fd82c 18bd07fa v8!v8::internal::Object::SetPropertyInternal(class v8::internal::LookupIterator \* it = 0x012fd888, class v8::internal::Handle<v8::internal::Object> value = class v8::internal::Handle<v8::internal::Object>, v8::internal::LanguageMode language_mode = <Value unavailable error>, v8::internal::Object::StoreFromKeyed store_mode = 0n19912804 (No matching enumerant), bool \* found = 0x012fd853)+0x27a [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\v8\src\objects.cc @ 5083]   
0f 012fd864 18aaf2e8 v8!v8::internal::Object::SetProperty(class v8::internal::LookupIterator \* it = 0x012fd888, class v8::internal::Handle<v8::internal::Object> value = class v8::internal::Handle<v8::internal::Object>, v8::internal::LanguageMode language_mode = kSloppy (0n0), v8::internal::Object::StoreFromKeyed store_mode = CERTAINLY_NOT_STORE_FROM_KEYED (0n1))+0x4a [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\v8\src\objects.cc @ 5138]   
10 012fd8e0 18ab68fd v8!v8::internal::StoreIC::Store(class v8::internal::Handle<v8::internal::Object> object = class v8::internal::Handle<v8::internal::Object>, class v8::internal::Handle<v8::internal::Name> name = class v8::internal::Handle<v8::internal::Name>, class v8::internal::Handle<v8::internal::Object> value = class v8::internal::Handle<v8::internal::Object>, v8::internal::Object::StoreFromKeyed store_mode = CERTAINLY_NOT_STORE_FROM_KEYED (0n1))+0x458 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\v8\src\ic\ic.cc @ 1429]   
11 012fd994 18ab65ca v8!v8::internal::__RT_impl_Runtime_StoreIC_Miss(class v8::internal::Arguments args = class v8::internal::Arguments, class v8::internal::Isolate \* isolate = 0x3557e840)+0x14d [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\v8\src\ic\ic.cc @ 2282]   
12 012fda08 4713de2a v8!v8::internal::Runtime_StoreIC_Miss(int args_length = 0n5, class v8::internal::Object \*\* args_object = 0x012fda44, class v8::internal::Isolate \* isolate = 0x3557e840)+0x8a [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\v8\src\ic\ic.cc @ 2268]   
WARNING: Frame IP not in any known module. Following frames may be wrong.  
13 012fda2c 4f39f538 0x4713de2a  
14 012fda70 35b9d2b5 0x4f39f538  
15 012fda9c 35b9557c 0x35b9d2b5  
16 012fdab0 35b8b8d1 0x35b9557c  
17 012fdadc 1896df56 0x35b8b8d1  
18 012fdb64 1896da47 v8!v8::internal::`anonymous namespace'::Invoke(class v8::internal::Isolate \* isolate = 0x00000004, bool is_construct = <Value unavailable error>, class v8::internal::Handle<v8::internal::Object> target = class v8::internal::Handle<v8::internal::Object>, class v8::internal::Handle<v8::internal::Object> receiver = class v8::internal::Handle<v8::internal::Object>, int argc = 0n0, class v8::internal::Handle<v8::internal::Object> \* args = 0x00000000, class v8::internal::Handle<v8::internal::Object> new_target = class v8::internal::Handle<v8::internal::Object>, v8::internal::Execution::MessageHandling message_handling = kReport (0n0), v8::internal::Execution::Target execution_target = kCallable (0n0))+0x446 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\v8\src\execution.cc @ 155]   
19 012fdb9c 1896d991 v8!v8::internal::`anonymous namespace'::CallInternal(class v8::internal::Isolate \* isolate = <Value unavailable error>, class v8::internal::Handle<v8::internal::Object> callable = class v8::internal::Handle<v8::internal::Object>, class v8::internal::Handle<v8::internal::Object> receiver = class v8::internal::Handle<v8::internal::Object>, int argc = 0n0, class v8::internal::Handle<v8::internal::Object> \* argv = 0x00000000, v8::internal::Execution::MessageHandling message_handling = kReport (0n0), v8::internal::Execution::Target target = kCallable (0n0))+0xa7 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\v8\src\execution.cc @ 191]   
1a 012fdbc0 1838a2cb v8!v8::internal::Execution::Call(class v8::internal::Isolate \* isolate = 0x3557e840, class v8::internal::Handle<v8::internal::Object> callable = class v8::internal::Handle<v8::internal::Object>, class v8::internal::Handle<v8::internal::Object> receiver = class v8::internal::Handle<v8::internal::Object>, int argc = 0n0, class v8::internal::Handle<v8::internal::Object> \* argv = 0x00000000)+0x21 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\v8\src\execution.cc @ 202]   
1b 012fdc88 65f89966 v8!v8::Script::Run(class v8::Local<v8::Context> context = class v8::Local<v8::Context>)+0x2fb [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\v8\src\api.cc @ 2122]   
1c 012fde30 65f970be chrome!CFXJS_Engine::Execute(class fxcrt::WideString \* script = 0x012fdfac)+0x396 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\cfxjs_engine.cpp @ 534]   
1d 012fde54 6690f7ee chrome!CJS_Runtime::ExecuteScript(class fxcrt::WideString \* script = 0x012fdfac)+0x2e [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\cjs_runtime.cpp @ 176]   
1e 012fdf44 6687e199 chrome!CJS_EventContext::RunScript(class fxcrt::WideString \* script = 0x012fdfac)+0x31e [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\cjs_event_context.cpp @ 53]   
1f 012fdf8c 6687e083 chrome!CJS_App::RunJsScript(class CJS_Runtime \* pRuntime = 0x36100f98, class fxcrt::WideString \* wsScript = 0x012fdfac)+0x89 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\cjs_app.cpp @ 433]   
20 012fdfb4 66e20668 chrome!CJS_App::TimerProc(class GlobalTimer \* pTimer = 0x0eb42fd0)+0x83 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\cjs_app.cpp @ 420]   
21 012fe024 63a74f17 chrome!GlobalTimer::Trigger(int nTimerID = 0n2)+0xd8 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\global_timer.cpp @ 52]   
22 012fe03c 63a74eda chrome!base::internal::FunctorTraits<void (<function> \*\* function = 0x18050ff4, int \* args = 0x18050ff8)+0x37 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\bind_internal.h @ 416]   
23 012fe058 63a74e9a chrome!base::internal::InvokeHelper<0,void>::MakeItSo<void (<function> \*\* functor = 0x18050ff4, int \* args = 0x18050ff8)+0x3a [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\bind_internal.h @ 616]   
24 012fe074 63a74d6f chrome!base::internal::Invoker<base::internal::BindState<void (<function> \*\* functor = 0x18050ff4, class std::tuple<int> \* bound = 0x18050ff8)+0x4a [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\bind_internal.h @ 689]   
\*\*\* WARNING: Unable to verify checksum for C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\out\chromium_pdfium_xfa_12_09\base.dll  
25 012fe09c 6c2c6f81 chrome!base::internal::Invoker<base::internal::BindState<void (class base::internal::BindStateBase \* base = 0x18050fe0)+0x3f [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\bind_internal.h @ 671]   
26 012fe0b8 6c5cea71 base!base::RepeatingCallback<void (void)+0x31 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\callback.h @ 129]   
27 012fe0e8 6c5ce1e5 base!base::RepeatingTimer::RunUserTask(void)+0x71 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\timer\timer.cc @ 304]   
28 012fe144 6c5ce04c base!base::internal::TimerBase::RunScheduledTask(void)+0x125 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\timer\timer.cc @ 232]   
29 012fe158 6c5cf26c base!base::internal::BaseTimerTaskInternal::Run(void)+0x3c [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\timer\timer.cc @ 50]   
2a 012fe168 6c5cf1cf base!base::internal::FunctorTraits<void (<function> \* method = 0x6c5ce010, class base::internal::BaseTimerTaskInternal \*\* receiver_ptr = 0x012fe1a4)+0x1c [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\bind_internal.h @ 516]   
2b 012fe18c 6c5cf125 base!base::internal::InvokeHelper<0,void>::MakeItSo<void (<function> \*\* functor = 0x0ebbeff4, class base::internal::BaseTimerTaskInternal \*\* args = 0x012fe1a4)+0x4f [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\bind_internal.h @ 616]   
2c 012fe1ac 6c5cefd4 base!base::internal::Invoker<base::internal::BindState<void (<function> \*\* functor = 0x0ebbeff4, class std::tuple<base::internal::OwnedWrapper<base::internal::BaseTimerTaskInternal> > \* bound = 0x0ebbeff8)+0x55 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\bind_internal.h @ 689]   
2d 012fe1d4 6c2ce410 base!base::internal::Invoker<base::internal::BindState<void (class base::internal::BindStateBase \* base = 0x0ebbefe0)+0x54 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\bind_internal.h @ 658]   
2e 012fe1f8 6c3309e3 base!base::OnceCallback<void (void)+0x50 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\callback.h @ 100]   
2f 012fe370 6c3c33df base!base::debug::TaskAnnotator::RunTask(char \* queue_function = 0x6c6d7a9f "MessageLoop::PostTask", struct base::PendingTask \* pending_task = 0x012fe568)+0x433 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\debug\task_annotator.cc @ 103]   
30 012fe524 6c3c38d9 base!base::MessageLoop::RunTask(struct base::PendingTask \* pending_task = 0x012fe568)+0x38f [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\message_loop\message_loop.cc @ 434]   
31 012fe560 6c3c40a6 base!base::MessageLoop::DeferOrRunPendingTask(struct base::PendingTask pending_task = struct base::PendingTask)+0x49 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\message_loop\message_loop.cc @ 448]   
32 012fe6a0 6c3cf551 base!base::MessageLoop::DoDelayedWork(class base::TimeTicks \* next_delayed_work_time = 0x315a0ff0)+0x246 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\message_loop\message_loop.cc @ 558]   
33 012fe6f0 6c3c2cd6 base!base::MessagePumpDefault::Run(class base::MessagePump::Delegate \* delegate = 0x012fec08)+0x81 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\message_loop\message_pump_default.cc @ 41]   
34 012fe898 6c493998 base!base::MessageLoop::Run(bool application_tasks_allowed = true)+0x1e6 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\message_loop\message_loop.cc @ 386]   
\*\*\* WARNING: Unable to verify checksum for C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\out\chromium_pdfium_xfa_12_09\content.dll  
35 012feb08 58731e7f base!base::RunLoop::Run(void)+0x1e8 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\run_loop.cc @ 102]   
36 012feea0 5c93beef content!content::PpapiPluginMain(struct content::MainFunctionParams \* parameters = 0x012fef4c)+0x52f [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\content\ppapi_plugin\ppapi_plugin_main.cc @ 160]   
37 012feed8 5c93d03a content!content::RunOtherNamedProcessTypeMain(class std::basic_string<char,std::char_traits<char>,std::allocator<char> > \* process_type = 0x012ff0d0, struct content::MainFunctionParams \* main_function_params = 0x012fef4c, class content::ContentMainDelegate \* delegate = 0x012ff5ec)+0xaf [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\content\app\content_main_runner_impl.cc @ 563]   
38 012ff0f0 5c9397a2 content!content::ContentMainRunnerImpl::Run(bool start_service_manager_only = false)+0x3ba [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\content\app\content_main_runner_impl.cc @ 898]   
\*\*\* WARNING: Unable to verify checksum for C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\out\chromium_pdfium_xfa_12_09\embedder.dll  
39 012ff108 50513ef3 content!content::ContentServiceManagerMainDelegate::RunEmbedderProcess(void)+0x32 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\content\app\content_service_manager_main_delegate.cc @ 53]   
3a 012ff508 5c93bd0c embedder!service_manager::Main(struct service_manager::MainParams \* params = 0x012ff52c)+0x713 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\services\service_manager\embedder\main.cc @ 472]   
3b 012ff554 5ee2132f content!content::ContentMain(struct content::ContentMainParams \* params = 0x012ff5cc)+0x5c [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\content\app\content_main.cc @ 20]   
3c 012ff638 0015b9ef chrome!ChromeMain(struct HINSTANCE__ \* instance = 0x00150000, struct sandbox::SandboxInterfaceInfo \* sandbox_info = 0x012ff6cc, int64 exe_entry_point_ticks = <Memory access error>)+0x1ef [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\chrome\app\chrome_main.cc @ 102]   
3d 012ff770 00151478 chrome_exe!MainDllLoader::Launch(struct HINSTANCE__ \* instance = 0x00150000, class base::TimeTicks exe_entry_point_ticks = class base::TimeTicks)+0x44f [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\chrome\app\main_dll_loader_win.cc @ 201]   
3e 012ffaa8 003c9a4e chrome_exe!wWinMain(struct HINSTANCE__ \* instance = 0x00150000, struct HINSTANCE__ \* prev = 0x00000000)+0x478 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\chrome\app\chrome_exe_main_win.cc @ 229]   
3f 012ffac0 003c9ba1 chrome_exe!invoke_main(void)+0x1e [f:\dd\vctools\crt\vcstartup\src\startup\exe_common.inl @ 123]   
40 012ffb18 003c9c6d chrome_exe!__scrt_common_main_seh(void)+0x151 [f:\dd\vctools\crt\vcstartup\src\startup\exe_common.inl @ 283]   
41 012ffb20 003c9c78 chrome_exe!__scrt_common_main(void)+0xd [f:\dd\vctools\crt\vcstartup\src\startup\exe_common.inl @ 326]   
42 012ffb28 76418484 chrome_exe!wWinMainCRTStartup(void)+0x8 [f:\dd\vctools\crt\vcstartup\src\startup\exe_wwinmain.cpp @ 17]   
43 012ffb3c 77db2fea KERNEL32!BaseThreadInitThunk+0x24  
44 012ffb84 77db2fba ntdll!__RtlUserThreadStart+0x2f  
45 012ffb94 00000000 ntdll!_RtlUserThreadStart+0x1b  

```

## Attachments

- [poc.pdf](attachments/poc.pdf) (application/pdf, 1.8 MB)
- [log_crash.txt](attachments/log_crash.txt) (text/plain, 23.4 KB)

## Timeline

### rs...@chromium.org (2018-09-14)

[Empty comment from Monorail migration]

[Monorail components: Internals>Plugins>PDF]

### ts...@chromium.org (2018-09-14)

Assigning to hnakashima who handled 860697

### sh...@chromium.org (2018-09-15)

[Empty comment from Monorail migration]

### hn...@chromium.org (2018-09-18)

This is another example of bug that would be fixed by queuing events instead of calling them in a reentrant fashion.

### hn...@chromium.org (2018-09-18)

[Empty comment from Monorail migration]

### hn...@chromium.org (2018-10-12)

[Empty comment from Monorail migration]

### hn...@chromium.org (2018-10-12)

[Empty comment from Monorail migration]

### hu...@gmail.com (2018-10-17)

Hi folks, 

Is there any update for this issue yet? 


### th...@chromium.org (2018-10-17)

Not yet. We need to find a new bug owner.

### th...@chromium.org (2018-10-17)

And there's no XFA on Android.

### ts...@chromium.org (2019-01-04)

[Empty comment from Monorail migration]

### bu...@chromium.org (2019-01-07)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/51229b6be5cab7e8c5c80534a4b82d537ee62860

commit 51229b6be5cab7e8c5c80534a4b82d537ee62860
Author: Tom Sepez <tsepez@chromium.org>
Date: Mon Jan 07 20:24:59 2019

Do not cache m_hMixXFAWidget in CPDFSDK_Widget.

It might go stale as part of a CXFA_LayoutPageMgr::PrepareLayout().

Bug: chromium:884122
Change-Id: I61bd42b5f18a3a6e1f17ec399889c7e74e0825d8
Reviewed-on: https://pdfium-review.googlesource.com/c/47790
Reviewed-by: Lei Zhang <thestig@chromium.org>
Commit-Queue: Tom Sepez <tsepez@chromium.org>

[modify] https://crrev.com/51229b6be5cab7e8c5c80534a4b82d537ee62860/fpdfsdk/cpdfsdk_widget.cpp
[modify] https://crrev.com/51229b6be5cab7e8c5c80534a4b82d537ee62860/fpdfsdk/cpdfsdk_widget.h


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

### na...@google.com (2019-01-24)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### na...@google.com (2019-01-24)

Congrats! The Panel has decided to reward $3,000 for this report! 

### na...@google.com (2019-01-24)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-04-18)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2019-04-18)

This issue was migrated from crbug.com/chromium/884122?no_tracker_redirect=1

[Monorail blocking: crbug.com/chromium/62400]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092456)*
