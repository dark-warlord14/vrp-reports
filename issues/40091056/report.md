# Security: Web Worker - Use After Free with Cross Thread Persisten Node

| Field | Value |
|-------|-------|
| **Issue ID** | [40091056](https://issues.chromium.org/issues/40091056) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>GarbageCollection, Blink>Storage |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | lo...@gmail.com |
| **Assignee** | lu...@chromium.org |
| **Created** | 2018-04-10 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

Steps to reproduce:

```
1. Run server side script UAF_PersistentNode_PoC.js in Node.js ( node UAF_PersistentNode_PoC.js ).  
2. Enter http://localhost:12345 in Chrome browser.  
3. Chrome crashes in CrossThreadPersistentRegion::ShouldTracePersistentNode()  ( or CrossThreadPersistentRegion::PrepareForThreadStateTermination() ) by accessing memory of a Cross Thread Persisten Node after it's freed.  

	(2260.7438): Access violation - code c0000005 (!!! second chance !!!)  
	eax=41f21878 ebx=2b692294 ecx=2b692284 edx=0b95c4b0 esi=0b95c4b0 edi=0000000e  
	eip=102ce7cd esp=0516dde8 ebp=0516ddec iopl=0         nv up ei pl nz na pe nc  
	cs=0023  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00210206  
	chrome_child!blink::PersistentBase<blink::(anonymous namespace)::DummyGCBase,blink::kNonWeakPersistentConfiguration,blink::kCrossThreadPersistentConfiguration>::Get [inlined in chrome_child!blink::CrossThreadPersistentRegion::ShouldTracePersistentNode+0x9]:  
	102ce7cd 8b00            mov     eax,dword ptr [eax]  ds:002b:41f21878=????????  

```

**VERSION**  

Chrome Version: Google Chrome 67.0.3386.1 (Official Build) dev (32-bit) (cohort: Dev)  

Operating System: Windows 10

**REPRODUCTION CASE** (The following is the worker code, full server code is in UAF\_PersistentNode\_PoC.js)

```
fetch("");  
close();  
caches.open("");  

```

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State:

The memory of the PersistentNode 41f21878 was in page 0x41f21000 (of length 0x1e000), which was freed in ThreadState::DetachCurrentThread() -> ThreadState::RunTerminationGC() -> Heap().RemoveAllPages().

```
6:040> g  
Breakpoint 3 hit  
eax=2b64dfc0 ebx=00000001 ecx=2b605a24 edx=00000000 esi=2b605a24 edi=2b605a20  
eip=0fd86423 esp=0c27f65c ebp=0c27f65c iopl=0         nv up ei pl nz na pe nc  
cs=0023  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00000206  
chrome_child!base::SetSystemPagesAccessInternal [inlined in chrome_child!base::DecommitSystemPages+0x3]:  
0fd86423 6800400000      push    4000h  

6:040> dv  
		address = 0x41f21000  
		 length = 0x1e000  
  accessibility = <value unavailable>  
6:040> k  
 # ChildEBP RetAddr    
00 (Inline) -------- chrome_child!base::SetSystemPagesAccessInternal [C:\b\c\b\win_clang\src\base\allocator\partition_allocator\page_allocator_internals_win.h @ 70]  
01 (Inline) -------- chrome_child!base::SetSystemPagesAccess [C:\b\c\b\win_clang\src\base\allocator\partition_allocator\page_allocator.cc @ 205]  
02 (Inline) -------- chrome_child!base::DecommitSystemPagesInternal [C:\b\c\b\win_clang\src\base\allocator\partition_allocator\page_allocator_internals_win.h @ 82]  
03 0c27f65c 0fdf2b3e chrome_child!base::DecommitSystemPages+0x3 [C:\b\c\b\win_clang\src\base\allocator\partition_allocator\page_allocator.cc @ 210]  
04 0c27f670 0fdf2aeb chrome_child!blink::MemoryRegion::Decommit+0x10 [C:\b\c\b\win_clang\src\third_party\WebKit\Source\platform\heap\PageMemory.cpp @ 26]  
05 0c27f684 10f2d8e3 chrome_child!blink::PagePool::Add+0x15 [C:\b\c\b\win_clang\src\third_party\WebKit\Source\platform\heap\PagePool.cpp @ 36]  
06 0c27f69c 10f2dafa chrome_child!blink::NormalPageArena::FreePage+0x2f [C:\b\c\b\win_clang\src\third_party\WebKit\Source\platform\heap\HeapPage.cpp @ 716]  
07 0c27f6a8 10f2d0db chrome_child!blink::NormalPage::RemoveFromHeap+0xe [C:\b\c\b\win_clang\src\third_party\WebKit\Source\platform\heap\HeapPage.cpp @ 1319]  
08 0c27f6b4 10f2b416 chrome_child!blink::BaseArena::RemoveAllPages+0x1f [C:\b\c\b\win_clang\src\third_party\WebKit\Source\platform\heap\HeapPage.cpp @ 121]  
09 0c27f6c4 10f2edda chrome_child!blink::ThreadHeap::RemoveAllPages+0x18 [C:\b\c\b\win_clang\src\third_party\WebKit\Source\platform\heap\Heap.cpp @ 564]  
0a 0c27f6d0 1201ebfb chrome_child!blink::ThreadState::DetachCurrentThread+0x18 [C:\b\c\b\win_clang\src\third_party\WebKit\Source\platform\heap\ThreadState.cpp @ 205]  
0b 0c27f6e4 12017aed chrome_child!blink::WorkerBackingThread::ShutdownOnBackingThread+0x4b [C:\b\c\b\win_clang\src\third_party\WebKit\Source\core\workers\WorkerBackingThread.cpp @ 125]  
0c 0c27f6f0 109e6631 chrome_child!blink::WorkerThread::PerformShutdownOnWorkerThread+0x1d [C:\b\c\b\win_clang\src\third_party\WebKit\Source\core\workers\WorkerThread.cpp @ 522]  
0d (Inline) -------- chrome_child!base::OnceCallback<void ()>::Run+0x13 [C:\b\c\b\win_clang\src\base\callback.h @ 95]  
0e 0c27f70c 103c5bd0 chrome_child!`anonymous namespace'::DiscardDeviceInfosAndCallContinuation+0x26 [C:\b\c\b\win_clang\src\services\video_capture\device_factory_media_to_mojo_adapter.cc @ 61]  
0f 0c27f71c 103c5bac chrome_child!base::internal::FunctorTraits<void (\*)(WTF::CrossThreadFunction<void ()>),void>::Invoke<WTF::CrossThreadFunction<void ()> >+0x1e [C:\b\c\b\win_clang\src\base\bind_internal.h @ 402]  
10 (Inline) -------- chrome_child!base::internal::InvokeHelper<0,void>::MakeItSo+0x9 [C:\b\c\b\win_clang\src\base\bind_internal.h @ 530]  
11 (Inline) -------- chrome_child!base::internal::Invoker<base::internal::BindState<void (\*)(WTF::CrossThreadFunction<void ()>),WTF::CrossThreadFunction<void ()> >,void ()>::RunImpl+0x9 [C:\b\c\b\win_clang\src\base\bind_internal.h @ 604]  
12 0c27f72c 0fd4b48f chrome_child!base::internal::Invoker<base::internal::BindState<void (\*)(WTF::CrossThreadFunction<void ()>),WTF::CrossThreadFunction<void ()> >,void ()>::RunOnce+0x12 [C:\b\c\b\win_clang\src\base\bind_internal.h @ 572]  
13 (Inline) -------- chrome_child!base::OnceCallback<void ()>::Run+0x10 [C:\b\c\b\win_clang\src\base\callback.h @ 95]  
14 0c27f798 10f4aa79 chrome_child!base::debug::TaskAnnotator::RunTask+0x9f [C:\b\c\b\win_clang\src\base\debug\task_annotator.cc @ 61]  
15 0c27f878 0fd6c3e2 chrome_child!blink::scheduler::internal::ThreadControllerImpl::DoWork+0xe1 [C:\b\c\b\win_clang\src\third_party\WebKit\Source\platform\scheduler\base\thread_controller_impl.cc @ 164]  
16 (Inline) -------- chrome_child!base::internal::FunctorTraits<void (media::AudioRendererImpl::\*)(media::PipelineStatus) __attribute__((thiscall)),void>::Invoke+0x1b [C:\b\c\b\win_clang\src\base\bind_internal.h @ 447]  
17 (Inline) -------- chrome_child!base::internal::InvokeHelper<1,void>::MakeItSo+0x38 [C:\b\c\b\win_clang\src\base\bind_internal.h @ 550]  
18 (Inline) -------- chrome_child!base::internal::Invoker<base::internal::BindState<void (media::AudioRendererImpl::\*)(media::PipelineStatus) __attribute__((thiscall)),base::WeakPtr<media::AudioRendererImpl>,media::PipelineStatus>,void ()>::RunImpl+0x38 [C:\b\c\b\win_clang\src\base\bind_internal.h @ 604]  
19 0c27f894 0fd4b48f chrome_child!base::internal::Invoker<base::internal::BindState<void (media::AudioRendererImpl::\*)(media::PipelineStatus) __attribute__((thiscall)),base::WeakPtr<media::AudioRendererImpl>,media::PipelineStatus>,void ()>::Run+0x42 [C:\b\c\b\win_clang\src\base\bind_internal.h @ 589]  
1a (Inline) -------- chrome_child!base::OnceCallback<void ()>::Run+0x10 [C:\b\c\b\win_clang\src\base\callback.h @ 95]  
1b 0c27f8fc 0fd4b3e3 chrome_child!base::debug::TaskAnnotator::RunTask+0x9f [C:\b\c\b\win_clang\src\base\debug\task_annotator.cc @ 61]  
1c 0c27f90c 0fd4b0e6 chrome_child!base::internal::IncomingTaskQueue::RunTask+0x13 [C:\b\c\b\win_clang\src\base\message_loop\incoming_task_queue.cc @ 125]  
1d 0c27f990 0fd4af03 chrome_child!base::MessageLoop::RunTask+0x1b6 [C:\b\c\b\win_clang\src\base\message_loop\message_loop.cc @ 392]  
1e 0c27f9b0 0fd42773 chrome_child!base::MessageLoop::DeferOrRunPendingTask+0x53 [C:\b\c\b\win_clang\src\base\message_loop\message_loop.cc @ 403]  
1f 0c27fa60 0fd42687 chrome_child!base::MessageLoop::DoWork+0xd3 [C:\b\c\b\win_clang\src\base\message_loop\message_loop.cc @ 447]  
20 0c27fa7c 0fd425df chrome_child!base::MessagePumpDefault::Run+0x87 [C:\b\c\b\win_clang\src\base\message_loop\message_pump_default.cc @ 38]  
21 0c27fa8c 0fd4244e chrome_child!base::MessageLoop::Run+0x1f [C:\b\c\b\win_clang\src\base\message_loop\message_loop.cc @ 342]  
22 0c27fa9c 0fd4241b chrome_child!base::RunLoop::Run+0x2e [C:\b\c\b\win_clang\src\base\run_loop.cc @ 136]  
23 0c27faa4 0fd41bb5 chrome_child!base::Thread::Run+0xb [C:\b\c\b\win_clang\src\base\threading\thread.cc @ 256]  
24 0c27fae4 1103affb chrome_child!base::Thread::ThreadMain+0x155 [C:\b\c\b\win_clang\src\base\threading\thread.cc @ 341]  
25 0c27fb08 76308654 chrome_child!base::`anonymous namespace'::ThreadFunc+0xbb [C:\b\c\b\win_clang\src\base\threading\platform_thread_win.cc @ 94]  
26 0c27fb1c 77b74a77 KERNEL32!BaseThreadInitThunk+0x24  
27 0c27fb64 77b74a47 ntdll!__RtlUserThreadStart+0x2f  
28 0c27fb74 00000000 ntdll!_RtlUserThreadStart+0x1b  

```

Later the persistent node (0x41f21878) was used again in CrossThreadPersistentRegion::ShouldTracePersistentNode() ( or CrossThreadPersistentRegion::PrepareForThreadStateTermination() ):

```
6:120> g  
(2260.7438): Access violation - code c0000005 (!!! second chance !!!)  
eax=41f21878 ebx=2b692294 ecx=2b692284 edx=0b95c4b0 esi=0b95c4b0 edi=0000000e  
eip=102ce7cd esp=0516dde8 ebp=0516ddec iopl=0         nv up ei pl nz na pe nc  
cs=0023  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00210206  
chrome_child!blink::PersistentBase<blink::(anonymous namespace)::DummyGCBase,blink::kNonWeakPersistentConfiguration,blink::kCrossThreadPersistentConfiguration>::Get [inlined in chrome_child!blink::CrossThreadPersistentRegion::ShouldTracePersistentNode+0x9]:  
102ce7cd 8b00            mov     eax,dword ptr [eax]  ds:002b:41f21878=????????  
6:120> !analyze -v  
\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*  
\*                                                                             \*  
\*                        Exception Analysis                                   \*  
\*                                                                             \*  
\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*  

GetUrlPageData2 (WinHttp) failed: 12002.  

FAULTING_IP:   
chrome_child!blink::CrossThreadPersistentRegion::ShouldTracePersistentNode+9 [C:\b\c\b\win_clang\src\third_party\WebKit\Source\platform\heap\PersistentNode.cpp @ 136]  
102ce7cd 8b00            mov     eax,dword ptr [eax]  

EXCEPTION_RECORD:  (.exr -1)  
ExceptionAddress: 102ce7cd (chrome_child!blink::PersistentBase<blink::(anonymous namespace)::DummyGCBase,blink::kNonWeakPersistentConfiguration,blink::kCrossThreadPersistentConfiguration>::Get)  
   ExceptionCode: c0000005 (Access violation)  
  ExceptionFlags: 00000000  
NumberParameters: 2  
   Parameter[0]: 00000000  
   Parameter[1]: 41f21878  
Attempt to read from address 41f21878  

FAULTING_THREAD:  00007438  

DEFAULT_BUCKET_ID:  INVALID_POINTER_READ  

PROCESS_NAME:  chrome.exe  

ERROR_CODE: (NTSTATUS) 0xc0000005 - The instruction at 0x%p referenced memory at 0x%p. The memory could not be %s.  

EXCEPTION_CODE: (NTSTATUS) 0xc0000005 - The instruction at 0x%p referenced memory at 0x%p. The memory could not be %s.  

EXCEPTION_PARAMETER1:  00000000  

EXCEPTION_PARAMETER2:  41f21878  

READ_ADDRESS:  41f21878   

FOLLOWUP_IP:   
chrome_child!blink::CrossThreadPersistentRegion::ShouldTracePersistentNode+9 [C:\b\c\b\win_clang\src\third_party\WebKit\Source\platform\heap\PersistentNode.cpp @ 136]  
102ce7cd 8b00            mov     eax,dword ptr [eax]  

BUGCHECK_STR:  INVALID_POINTER_READ  

NTGLOBALFLAG:  400  

APPLICATION_VERIFIER_FLAGS:  0  

APP:  chrome.exe  

ANALYSIS_VERSION: 10.0.10240.9 x86fre  

LAST_CONTROL_TRANSFER:  from 102bc4d1 to 102ce7cd  

STACK_TEXT:    
0516ddec 102bc4d1 0b95c4b0 2b692294 000000f2 chrome_child!blink::CrossThreadPersistentRegion::ShouldTracePersistentNode+0x9  
0516de28 102bc388 0b95c4b0 102ce7c4 0516de48 chrome_child!blink::PersistentRegion::TracePersistentNodes+0x75  
0516de74 102bc2bb 0b95c4b0 00000000 00000000 chrome_child!blink::ThreadState::VisitPersistents+0x2e  
0516debc 102bc165 0b95c4b0 7e866666 41b26667 chrome_child!blink::ThreadHeap::VisitPersistentRoots+0x3b  
0516def0 10f2f039 7e7f7cee 41b26667 0fe692bf chrome_child!blink::ThreadState::MarkPhaseVisitRoots+0x39  
0516e048 10471c5f 00000001 00000000 00000001 chrome_child!blink::ThreadState::CollectGarbage+0xfb  
0516e0f8 10466d7f 07a27ac0 00000002 00000020 chrome_child!blink::V8GCController::GcEpilogue+0x17f  
0516e210 1046454f 00000001 00000020 00000001 chrome_child!v8::internal::Heap::PerformGarbageCollection+0xe3f  
0516e288 10c849d1 00000002 00000008 00000020 chrome_child!v8::internal::Heap::CollectGarbage+0x38f  
0516e2a0 10c6a630 3519794e 00000000 0516e340 chrome_child!v8::internal::Heap::HandleGCRequest+0x91  
0516e2bc 1042283d 3db664d9 00000016 00001fff chrome_child!v8::internal::StackGuard::HandleInterrupts+0x90  
0516e2ec 10423b1f 0516e340 00000000 0ff3101f chrome_child!v8::internal::JsonParser<1>::ParseJsonValue+0x4d  
0516e374 10422b6b 0516e3fc 3db664d9 00000017 chrome_child!v8::internal::JsonParser<1>::ParseJsonObject+0x92f  
0516e3a8 10423b1f 0516e3fc 00000000 0ff3101f chrome_child!v8::internal::JsonParser<1>::ParseJsonValue+0x37b  
0516e430 10422b6b 0516e4b8 3db664d9 00000003 chrome_child!v8::internal::JsonParser<1>::ParseJsonObject+0x92f  
0516e464 10423b1f 0516e4b8 00000000 0516e4d8 chrome_child!v8::internal::JsonParser<1>::ParseJsonValue+0x37b  
0516e4ec 10422b6b 0516e558 0516e64c 0516e64c chrome_child!v8::internal::JsonParser<1>::ParseJsonObject+0x92f  
0516e520 10422675 0516e558 0516e578 0516e578 chrome_child!v8::internal::JsonParser<1>::ParseJsonValue+0x37b  
0516e56c 10422450 0516e5cc 0516e66c 00005476 chrome_child!v8::internal::JsonParser<1>::ParseJson+0x75  
0516e5f0 10acacf6 0516e610 07a27ac0 0516e66c chrome_child!v8::internal::JsonParser<1>::Parse+0x50  
0516e624 102f3b3b 07a27ac0 0516e654 228890fe chrome_child!v8::internal::Builtin_Impl_JsonParse+0x136  
0516e630 228890fe 00000006 0516e670 07a27ac0 chrome_child!v8::internal::Builtin_JsonParse+0x1b  
WARNING: Frame IP not in any known module. Following frames may be wrong.  
0516e654 22892c78 4f584185 3930b7fd 0000000c 0x228890fe  
0516e690 22890964 00000000 0c114101 3db04471 0x22892c78  
0516e6b0 22886ef1 00000000 00000000 00000002 0x22890964  
0516e6dc 10c6a285 4f584185 5c4347b9 3db04471 0x22886ef1  
0516e754 0ffce573 00000000 0a50bf30 0a50bf2c chrome_child!v8::internal::`anonymous namespace'::Invoke+0x365  
0516e788 1007e2cd 0516e7b8 07a27ac0 0a50bf30 chrome_child!v8::internal::Execution::Call+0x83  
0516e81c 1007dd2c 0516e83c 0a50bf54 0a50bf2c chrome_child!v8::Function::Call+0x26d  
0516e8d0 11da4281 0516e90c 0a50bf30 3aa8ec80 chrome_child!blink::V8ScriptRunner::CallFunction+0x2fc  
0516e930 11da385a 0516e96c 5c1a1cc0 4d3d3108 chrome_child!blink::`anonymous namespace'::V8FunctionExecutor::Execute+0x161  
0516e9a0 11da357f 00000000 3594db08 3594db18 chrome_child!blink::PausableScriptExecutor::ExecuteAndDestroySelf+0x9a  
0516e9e8 11d7fc70 5c1a1cc0 07a27ac0 0a50bf1c chrome_child!blink::PausableScriptExecutor::CreateAndRun+0x1ff  
0516ea1c 10fe2454 0a50bf1c 0a50bf0c 0a50bf18 chrome_child!blink::WebLocalFrameImpl::RequestExecuteV8Function+0x30  
0516ea80 10fd659c 0516eae8 00000002 0ba996e8 chrome_child!extensions::ScriptContext::SafeCallFunction+0xe0  
0516eb04 10fd66fe 0516eb6c 0516eb84 00000002 chrome_child!extensions::ModuleSystem::CallModuleMethodSafe+0xba  
0516eb34 10fd34e1 0516eb6c 0516eb84 0516eb4c chrome_child!extensions::ModuleSystem::CallModuleMethodSafe+0x3a  
0516ebac 10fdf126 0b9ab840 0ba4bff8 0ba4bfe0 chrome_child!extensions::JSRendererMessagingService::DispatchOnMessageToListeners+0xeb  
0516ebd8 10fdf3fc 0ba4bff8 0ba4bfe0 0b9ab840 chrome_child!extensions::RendererMessagingService::DeliverMessageToScriptContext+0xbe  
0516ebf0 0fdc5934 0ba4bfc8 0b9ab840 0bac4020 chrome_child!base::internal::Invoker<base::internal::BindState<void (extensions::RendererMessagingService::\*)(const extensions::Message &, const extensions::PortId &, extensions::ScriptContext \*) __attribute__((thiscall)),base::internal::UnretainedWrapper<extensions::RendererMessagingService>,extensions::Message,extensions::PortId>,void (extensions::ScriptContext \*)>::Run+0x18  
0516ec1c 10fdf045 0516ec3c 079d7e68 0516ec38 chrome_child!extensions::ScriptContextSet::ForEach+0x7c  
0516ec64 10fc8921 0a50f3c0 0516ece0 0516ecc0 chrome_child!extensions::RendererMessagingService::DeliverMessage+0x89  
0516ec88 10fc8844 0516ece0 0516ecc0 0b9ba118 chrome_child!extensions::ExtensionFrameHelper::OnExtensionDeliverMessage+0x31  
0516ed0c 0fe740c2 0ba47eb8 0a52bb70 0a52bb70 chrome_child!IPC::MessageT<ExtensionMsg_DeliverMessage_Meta,std::tuple<extensions::PortId,extensions::Message>,void>::Dispatch<extensions::ExtensionFrameHelper,extensions::ExtensionFrameHelper,void,void (extensions::ExtensionFrameHelper::\*)(const extensions::PortId &, const extensions::Message &) __attribute__((thiscall))>+0x86  
0516ed90 0fe724c3 0ba47eb8 0516f7ac 0516ed80 chrome_child!extensions::ExtensionFrameHelper::OnMessageReceived+0x270  
0516f0ac 0fdc110d 0ba47eb8 0516f0f8 139aa088 chrome_child!content::RenderFrameImpl::OnMessageReceived+0x175  
0516f0c0 0fdc10eb 0ba47eb8 0516f138 0fd4b48f chrome_child!IPC::ChannelProxy::Context::OnDispatchMessage+0x1f  
0516f0cc 0fd4b48f 0ba47ea0 1317c744 00000081 chrome_child!base::internal::Invoker<base::internal::BindState<void (extensions::AutomationMessageFilter::\*)(const IPC::Message &) __attribute__((thiscall)),scoped_refptr<extensions::AutomationMessageFilter>,IPC::Message>,void ()>::Run+0x13  
0516f138 10f4aa79 130f5178 0516f1a8 079bcbc0 chrome_child!base::debug::TaskAnnotator::RunTask+0x9f  
0516f218 0fd6c3e2 00000000 10f4a998 0516f260 chrome_child!blink::scheduler::internal::ThreadControllerImpl::DoWork+0xe1  
0516f234 0fd4b48f 079a78b8 00000000 77b513ee chrome_child!base::internal::Invoker<base::internal::BindState<void (media::AudioRendererImpl::\*)(media::PipelineStatus) __attribute__((thiscall)),base::WeakPtr<media::AudioRendererImpl>,media::PipelineStatus>,void ()>::Run+0x42  
0516f29c 0fd4b3e3 131139e8 0516f358 0516f330 chrome_child!base::debug::TaskAnnotator::RunTask+0x9f  
0516f2ac 0fd4b0e6 0516f358 130f509d 079b2900 chrome_child!base::internal::IncomingTaskQueue::RunTask+0x13  
0516f330 0fd4af03 0516f358 0fd494ec 1887a19a chrome_child!base::MessageLoop::RunTask+0x1b6  
0516f350 0fd42773 00000000 130f5195 130f509d chrome_child!base::MessageLoop::DeferOrRunPendingTask+0x53  
0516f3fc 0fd42687 079a7080 079a7078 079b289c chrome_child!base::MessageLoop::DoWork+0xd3  
0516f418 0fd425df 079b2898 0516f450 0516f438 chrome_child!base::MessagePumpDefault::Run+0x87  
0516f428 0fd4244e 00000001 0516f440 0516f50c chrome_child!base::MessageLoop::Run+0x1f  
0516f438 0fd2f33d 00000000 07994ad0 009bf0a8 chrome_child!base::RunLoop::Run+0x2e  
0516f50c 0fd2eedb 0516f5f4 07505080 0000001a chrome_child!content::RendererMain+0x415  
0516f5dc 0fd28eb6 0516f608 0516f5f4 0516f7a8 chrome_child!content::RunNamedProcessTypeMain+0x10c  
0516f630 0fd04587 005e0000 00000003 0516f74c chrome_child!content::ContentMainRunnerImpl::Run+0x8e  
0516f73c 0fd04268 0516f748 0516f74c 1310ed10 chrome_child!service_manager::Main+0x26e  
0516f778 0fd01915 0516f794 0516f784 0516f780 chrome_child!content::ContentMain+0x33  
0516f7d8 00ec3002 00ec0000 0516f820 b0817237 chrome_child!ChromeMain+0x108  
0516f864 00ec145d 00ec0000 b0817237 00000047 chrome!MainDllLoader::Launch+0x230  
0516f9d0 00f7e6d8 00ec0000 00000000 075d3450 chrome!wWinMain+0x45d  
0516fa1c 76308654 05285000 76308630 059e161d chrome!__scrt_common_main_seh+0xf6  
0516fa30 77b74a77 05285000 046489e3 00000000 KERNEL32!BaseThreadInitThunk+0x24  
0516fa78 77b74a47 ffffffff 77b99eaa 00000000 ntdll!__RtlUserThreadStart+0x2f  
0516fa88 00000000 00f7e750 05285000 00000000 ntdll!_RtlUserThreadStart+0x1b  


FAULTING_SOURCE_LINE:  C:\b\c\b\win_clang\src\third_party\WebKit\Source\platform\heap\PersistentNode.cpp  

FAULTING_SOURCE_FILE:  C:\b\c\b\win_clang\src\third_party\WebKit\Source\platform\heap\PersistentNode.cpp  

FAULTING_SOURCE_LINE_NUMBER:  136  

FAULTING_SOURCE_CODE:    
   121:   T\* operator->() const { return \*this; }  
   122:   
   123:   T\* Get() const {  
   124:     CheckPointer();  
>  125:     return raw_;  
   126:   }  
   127:   
   128:   template <typename U>  
   129:   PersistentBase& operator=(U\* other) {  
   130:     Assign(other);  


SYMBOL_STACK_INDEX:  0  

SYMBOL_NAME:  chrome_child!blink::CrossThreadPersistentRegion::ShouldTracePersistentNode+9  

FOLLOWUP_NAME:  MachineOwner  

MODULE_NAME: chrome_child  

IMAGE_NAME:  chrome_child.dll  

DEBUG_FLR_IMAGE_TIMESTAMP:  5ac30884  

STACK_COMMAND:  ~120s ; kb  

BUCKET_ID:  INVALID_POINTER_READ_chrome_child!blink::CrossThreadPersistentRegion::ShouldTracePersistentNode+9  

PRIMARY_PROBLEM_CLASS:  INVALID_POINTER_READ_chrome_child!blink::CrossThreadPersistentRegion::ShouldTracePersistentNode+9  

FAILURE_PROBLEM_CLASS:  INVALID_POINTER_READ  

FAILURE_EXCEPTION_CODE:  c0000005  

FAILURE_IMAGE_NAME:  chrome_child.dll  

FAILURE_FUNCTION_NAME:  blink::CrossThreadPersistentRegion::ShouldTracePersistentNode  

FAILURE_SYMBOL_NAME:  chrome_child.dll!blink::CrossThreadPersistentRegion::ShouldTracePersistentNode  

FAILURE_BUCKET_ID:  INVALID_POINTER_READ_c0000005_chrome_child.dll!blink::CrossThreadPersistentRegion::ShouldTracePersistentNode  

ANALYSIS_SOURCE:  UM  

FAILURE_ID_HASH_STRING:  um:invalid_pointer_read_c0000005_chrome_child.dll!blink::crossthreadpersistentregion::shouldtracepersistentnode  

FAILURE_ID_HASH:  {28d2ce5b-6d23-b6da-6b00-43597c3c7d3d}  

Followup:     MachineOwner  
---------  

```

## Attachments

- [UAF_PersistentNode_PoC.js](attachments/UAF_PersistentNode_PoC.js) (text/plain, 914 B)

## Timeline

### ca...@chromium.org (2018-04-11)

[Empty comment from Monorail migration]

### ca...@chromium.org (2018-04-11)

This was reproducible by ClusterFuzz (https://clusterfuzz.com/testcase?key=5710027462279168), but I had not added the issue number so it filed a new issue.

### ca...@chromium.org (2018-04-11)

lucmult: Assigning this one to you since ClusterFuzz points to https://chromium-review.googlesource.com/c/chromium/src/+/875510 as the regression, can you take a look and reassign if not appropriate?

[Monorail components: Blink]

### ca...@chromium.org (2018-04-11)

[Empty comment from Monorail migration]

### ch...@chromium.org (2018-04-11)

[Empty comment from Monorail migration]

[Monorail components: -Blink Blink>Storage]

### lu...@chromium.org (2018-04-12)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-04-12)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-04-12)

[Empty comment from Monorail migration]

### no...@chromium.org (2018-04-13)

+inferno@, +ochang@, +mmoroz@ help needed.  

Luciano is a googler and this is his first release-block-stable P0. He is access-denied loading the clusterfuzz report.  Possible to fix?

### cl...@chromium.org (2018-04-13)

Detailed report: https://clusterfuzz.com/testcase?key=5710027462279168

Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: UNKNOWN READ
Crash Address: 0x7eae66f618a0
Crash State:
  blink::PersistentBase<blink::DummyGCBase,
  blink::CrossThreadPersistentRegion::PrepareForThreadStateTermination
  blink::ThreadState::RunTerminationGC
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=544931:544932

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5710027462279168

Additional requirements: Requires HTTP

See https://github.com/google/clusterfuzz-tools for more information.

### oc...@chromium.org (2018-04-13)

The clusterfuzz report was associated with a different monorail issue. I've fixed this and confirmed that it works for Luciano now.

### lu...@chromium.org (2018-04-13)

Hi all,

I was talking to noel@ and the safest course of action for the time being is to revert the patch.

We have to revert 2 or 3 patches:
Main patch: https://chromium-review.googlesource.com/c/chromium/src/+/875510
Follow patch #1 - Remove IPC messages definition: https://chromium-review.googlesource.com/c/chromium/src/+/907769
Follow up patch #2 - Check for nullptr: https://chromium-review.googlesource.com/c/chromium/src/+/981633




### no...@chromium.org (2018-04-13)

ochang++ Thanks for the quick reply.  #12 yeap, safe course, but yeah there is a branch cut for M67 going on, so it'll be a interesting set of reverts ...

### lu...@chromium.org (2018-04-13)

I chatted with sammc@ and we're holding off on reverting these patches.

Furthermore, he also helped me debug this further and we found a potential fix.

I'll write a test and try to run on clusterfuzz (after lunch and meetings).

### no...@chromium.org (2018-04-13)

SGTM.

### lu...@chromium.org (2018-04-13)

Hi, 

The fix we came up with doesn't fix all occurrences of this issue.

I created a LayoutTest that causes the renderer crash even with our fix:
https://chromium-review.googlesource.com/c/chromium/src/+/1011467



### lu...@chromium.org (2018-04-13)

sammc@ found a possible circular reference and we're trying on patch #2:

https://chromium-review.googlesource.com/c/chromium/src/+/1011467

### lu...@chromium.org (2018-04-13)

The fix seems to fix the issue, The test failed with timeout instead of crashing as was happening before, which I'll check closely by Monday (in Sydney).

I've sent for review:
https://chromium-review.googlesource.com/c/chromium/src/+/1011467

### sh...@chromium.org (2018-04-13)

This issue is marked as a release blocker with no OS labels associated. Please add an appropriate OS label.

All release blocking issues should have OS labels associated to it, so that the issue can tracked and promptly verified, once it gets fixed.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ct...@chromium.org (2018-04-13)

(Adding OS labels -- sounds like this affects all Blink platforms.)

### cl...@chromium.org (2018-04-16)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Blink>MemoryAllocator>GarbageCollection]

### bu...@chromium.org (2018-04-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/5a45635a2827710b23f7637f7b300cb966261197

commit 5a45635a2827710b23f7637f7b300cb966261197
Author: Luciano Pacheco <lucmult@chromium.org>
Date: Tue Apr 17 06:13:56 2018

Change Cache Storage callback to WeakPersistent instead of Persistent

This fixes a memory leak and renderer crash as described below.

Change Cache Storage "open" method callback to have a WeakPersistent
reference to CacheStorage to avoid a circular reference between them.
Remove Persistent<CacheStorage> from callback for "delete" since it
wasn't used.

WebServiceWorkerCacheStorageImpl keeps the callback while waiting for
mojo response from browser process which keeps CacheStorage alive,
CacheStorage also has a reference to WebServiceWQorkerCacheStorage,
which is implemented by WebServiceCacheStorageImpl, creating the
circular reference, this situation leads to memory leak because those
can't be garbage collected properly on some termination conditions,
this leak in turn would cause renderer to crash when starting a new
worker and trying to reuse pointer to address cleaned by Oilpan heap.

When a worker is terminated with pending WithCacheCallback objects,
the termination GC callback will access the Persistent handle. However,
it will point to an object in a dead Oilpan heap and cause a segfault.

Using a WeakPersistent is a workaround to prevent this crash, since
the termination GC callback won't try to access it. In the future,
Oilpan might be updated to handle this more gracefully see
https://crbug.com/831117.

The added test catches two conditions where renderer process was
crashing:
1. When initializing Cache Storage after "close()".
2. Initializing Cache Storage before "close()" and issuing new calls,
that trigger mojo after "close()".

Bug: 831054
Change-Id: I6620d8107c00aed1c386c869dc1a793bc51d97fa
Reviewed-on: https://chromium-review.googlesource.com/1011467
Commit-Queue: Luciano Pacheco (SYD) <lucmult@chromium.org>
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Reviewed-by: Kentaro Hara <haraken@chromium.org>
Cr-Commit-Position: refs/heads/master@{#551262}
[add] https://crrev.com/5a45635a2827710b23f7637f7b300cb966261197/third_party/WebKit/LayoutTests/http/tests/cachestorage/serviceworker/worker-closer.js
[add] https://crrev.com/5a45635a2827710b23f7637f7b300cb966261197/third_party/WebKit/LayoutTests/http/tests/cachestorage/serviceworker/worker-closer2.js
[add] https://crrev.com/5a45635a2827710b23f7637f7b300cb966261197/third_party/WebKit/LayoutTests/http/tests/cachestorage/worker-deleted.html
[modify] https://crrev.com/5a45635a2827710b23f7637f7b300cb966261197/third_party/blink/renderer/modules/cachestorage/cache_storage.cc


### lu...@chromium.org (2018-04-17)

I have run clusterfuzz locally with the patch above and it seems to fix the issue.

I'm marking this bug as fixed for now.

If any additional checks or merge on branches are required from me just re-open and I'll work on it. This is my first security release-blocker, so I don't know the exact next steps. :-)

### sh...@chromium.org (2018-04-17)

[Empty comment from Monorail migration]

### cl...@chromium.org (2018-04-19)

ClusterFuzz testcase 4600406068690944 is verified as fixed, so closing issue as verified.

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### cl...@chromium.org (2018-04-19)

ClusterFuzz has detected this issue as fixed in range 551260:551263.

Detailed report: https://clusterfuzz.com/testcase?key=5710027462279168

Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: UNKNOWN READ
Crash Address: 0x7eae66f618a0
Crash State:
  blink::PersistentBase<blink::DummyGCBase,
  blink::CrossThreadPersistentRegion::PrepareForThreadStateTermination
  blink::ThreadState::RunTerminationGC
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=544931:544932
Fixed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=551260:551263

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5710027462279168

Additional requirements: Requires HTTP

See https://github.com/google/clusterfuzz-tools for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### no...@chromium.org (2018-04-19)

#25, #26 confirms the fix (good). 

Wash-up would be to decide if a merge into release branches (M66?) is wanted + easy + safe.

### lu...@chromium.org (2018-04-20)

I tested on my current stable: 66.0.3359.117 and it isn't affected by this bug.



### lu...@chromium.org (2018-04-20)

Checked my dev channel: 67.0.3396.10 is still affected by this bug.

I'm checking further if and how to merge on M67 branch.

### lu...@chromium.org (2018-04-20)

I tested on Canary 68.0.3399.0: and it's fixed.

So I'm proceeding with merge request for M67 as documented here:
https://sites.google.com/a/google.com/chromeos/for-team-members/chronos-download/pmo/merge-instructions-to-a-release-branch?pli=1

### lu...@chromium.org (2018-04-20)

[Empty comment from Monorail migration]

### no...@chromium.org (2018-04-20)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-04-20)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-04-20)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-04-21)

Your change meets the bar and is auto-approved for M67. Please go ahead and merge the CL to branch 3396 manually. Please contact milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), kbleicher@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chromium.org (2018-04-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/df9b0d3b053b079dfeef6c703fa222fbb889c1e2

commit df9b0d3b053b079dfeef6c703fa222fbb889c1e2
Author: Luciano Pacheco <lucmult@chromium.org>
Date: Sat Apr 21 04:56:11 2018

Change Cache Storage callback to WeakPersistent instead of Persistent

This fixes a memory leak and renderer crash as described below.

Change Cache Storage "open" method callback to have a WeakPersistent
reference to CacheStorage to avoid a circular reference between them.
Remove Persistent<CacheStorage> from callback for "delete" since it
wasn't used.

WebServiceWorkerCacheStorageImpl keeps the callback while waiting for
mojo response from browser process which keeps CacheStorage alive,
CacheStorage also has a reference to WebServiceWQorkerCacheStorage,
which is implemented by WebServiceCacheStorageImpl, creating the
circular reference, this situation leads to memory leak because those
can't be garbage collected properly on some termination conditions,
this leak in turn would cause renderer to crash when starting a new
worker and trying to reuse pointer to address cleaned by Oilpan heap.

When a worker is terminated with pending WithCacheCallback objects,
the termination GC callback will access the Persistent handle. However,
it will point to an object in a dead Oilpan heap and cause a segfault.

Using a WeakPersistent is a workaround to prevent this crash, since
the termination GC callback won't try to access it. In the future,
Oilpan might be updated to handle this more gracefully see
https://crbug.com/831117.

The added test catches two conditions where renderer process was
crashing:
1. When initializing Cache Storage after "close()".
2. Initializing Cache Storage before "close()" and issuing new calls,
that trigger mojo after "close()".

Bug: 831054
Change-Id: I6620d8107c00aed1c386c869dc1a793bc51d97fa
Reviewed-on: https://chromium-review.googlesource.com/1011467
Commit-Queue: Luciano Pacheco (SYD) <lucmult@chromium.org>
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Reviewed-by: Kentaro Hara <haraken@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#551262}(cherry picked from commit 5a45635a2827710b23f7637f7b300cb966261197)
Reviewed-on: https://chromium-review.googlesource.com/1023450
Reviewed-by: Luciano Pacheco (SYD) <lucmult@chromium.org>
Cr-Commit-Position: refs/branch-heads/3396@{#192}
Cr-Branched-From: 9ef2aa869bc7bc0c089e255d698cca6e47d6b038-refs/heads/master@{#550428}
[add] https://crrev.com/df9b0d3b053b079dfeef6c703fa222fbb889c1e2/third_party/WebKit/LayoutTests/http/tests/cachestorage/serviceworker/worker-closer.js
[add] https://crrev.com/df9b0d3b053b079dfeef6c703fa222fbb889c1e2/third_party/WebKit/LayoutTests/http/tests/cachestorage/serviceworker/worker-closer2.js
[add] https://crrev.com/df9b0d3b053b079dfeef6c703fa222fbb889c1e2/third_party/WebKit/LayoutTests/http/tests/cachestorage/worker-deleted.html
[modify] https://crrev.com/df9b0d3b053b079dfeef6c703fa222fbb889c1e2/third_party/blink/renderer/modules/cachestorage/cache_storage.cc


### lu...@chromium.org (2018-04-21)

Merged on M67 branch:

https://chromium-review.googlesource.com/c/chromium/src/+/1023450

Watching waterfall/builders.

### aw...@google.com (2018-04-23)

[Empty comment from Monorail migration]

### aw...@google.com (2018-04-25)

Actually a use after free, changing to severity High

### lu...@chromium.org (2018-04-26)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-27)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-04-27)

Nice one - $3,000 for this report. Thanks!

### aw...@chromium.org (2018-04-27)

[Empty comment from Monorail migration]

### aw...@google.com (2018-04-30)

[Empty comment from Monorail migration]

### lf...@chromium.org (2018-06-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-28)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### va...@chromium.org (2021-09-16)

[Empty comment from Monorail migration]

[Monorail components: -Blink>MemoryAllocator>GarbageCollection Blink>GarbageCollection]

### is...@google.com (2021-09-16)

This issue was migrated from crbug.com/chromium/831054?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>GarbageCollection, Blink>Storage]
[Monorail blocking: crbug.com/chromium/612287]
[Monorail mergedwith: crbug.com/chromium/831580, crbug.com/chromium/833150]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091056)*
