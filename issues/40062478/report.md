# V8 type confusion of object as v8::Function in CallMethodOnFrame

| Field | Value |
|-------|-------|
| **Issue ID** | [40062478](https://issues.chromium.org/issues/40062478) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Platform>DevTools |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | wx...@gmail.com |
| **Assignee** | sz...@chromium.org |
| **Created** | 2023-01-03 |
| **Bounty** | $1,000.00 |

## Description

**Steps to reproduce the problem:**  

1.  

2.a  

3.

**Problem Description:**  

a

**Additional Comments:**

\*\*Chrome version: \*\* 108.0.0.0 \*\*Channel: \*\* Not sure

**OS:** Windows

## Attachments

- [0001-type-confusion-check.patch](attachments/0001-type-confusion-check.patch) (text/plain, 957 B)
- [0001-fix-type-confusion.patch](attachments/0001-fix-type-confusion.patch) (text/plain, 996 B)

## Timeline

### wx...@gmail.com (2023-01-03)

bug reason
```
v8::MaybeLocal<v8::Value> CallMethodOnFrame(LocalFrame* local_frame,
                                            const String& object_name,
                                            const String& method_name,
                                            base::Value::List arguments,
                                            WebV8ValueConverter* converter) {
  v8::Local<v8::Context> context = MainWorldScriptContext(local_frame);

  v8::Context::Scope context_scope(context);
  WTF::Vector<v8::Local<v8::Value>> args;
  for (const auto& argument : arguments) {
    args.push_back(converter->ToV8Value(argument, context));
  }

  v8::Local<v8::Value> object;
  v8::Local<v8::Value> method;
  if (!GetProperty(context, context->Global(), object_name).ToLocal(&object) ||
      !GetProperty(context, object, method_name).ToLocal(&method)) {
    return v8::MaybeLocal<v8::Value>();
  }

  CHECK(method->IsFunction());
  return local_frame->DomWindow()
      ->GetScriptController()
      .EvaluateMethodInMainWorld(v8::Local<v8::Function>::Cast(method), object,       // here will cast to v8::Function without check its type
                                 static_cast<int>(args.size()), args.data());
}
```

### wx...@gmail.com (2023-01-03)

the type confusion is hard to trigger.

```
[5200:13452:0103/222014.054:FATAL:local_frame_mojo_handler.cc(220)] Check failed: method->IsFunction().
Backtrace:
        base::debug::CollectStackTrace [0x00007FFC3BC84162+18] (D:\work\fuzz\chromium\src\base\debug\stack_trace_win.cc:329)
        base::debug::StackTrace::StackTrace [0x00007FFC3E99BEEA+26] (D:\work\fuzz\chromium\src\base\debug\stack_trace.cc:218)
        logging::LogMessage::~LogMessage [0x00007FFC3BADD818+696] (D:\work\fuzz\chromium\src\base\logging.cc:719)
        logging::LogMessage::~LogMessage [0x00007FFC3BAE1470+16] (D:\work\fuzz\chromium\src\base\logging.cc:712)
        blink::LocalFrameMojoHandler::JavaScriptMethodExecuteRequest [0x00007FFC442022AD+4877] (D:\work\fuzz\chromium\src\third_party\blink\renderer\core\frame\local_frame_mojo_handler.cc:897)
        blink::mojom::blink::LocalFrameStubDispatch::AcceptWithResponder [0x00007FFC397F4B8A+4718] (D:\work\fuzz\chromium\src\out\asan\gen\third_party\blink\public\mojom\frame\frame.mojom-blink.cc:15010)
        blink::mojom::blink::LocalFrameStub<mojo::RawPtrImplRefTraits<blink::mojom::blink::LocalFrame> >::AcceptWithResponder [0x00007FFC4420C8EF+287] (D:\work\fuzz\chromium\src\out\asan\gen\third_party\blink\public\mojom\frame\frame.mojom-blink.h:2101)
        mojo::InterfaceEndpointClient::HandleValidatedMessage [0x00007FFC3BEAF41B+1875] (D:\work\fuzz\chromium\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:961)
        mojo::MessageDispatcher::Accept [0x00007FFC3EF61F31+563] (D:\work\fuzz\chromium\src\mojo\public\cpp\bindings\lib\message_dispatcher.cc:48)
        mojo::InterfaceEndpointClient::HandleIncomingMessage [0x00007FFC3BEB3CDA+396] (D:\work\fuzz\chromium\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:694)
        IPC::`anonymous namespace'::ChannelAssociatedGroupController::AcceptOnEndpointThread [0x00007FFC3C472D42+988] (D:\work\fuzz\chromium\src\ipc\ipc_mojo_bootstrap.cc:1076)
        base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message),scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>,mojo::Message>,void ()>::RunOnce [0x00007FFC3C46B17B+387] (D:\work\fuzz\chromium\src\base\functional\bind_internal.h:924)
        base::TaskAnnotator::RunTaskImpl [0x00007FFC3BBE9BF1+897] (D:\work\fuzz\chromium\src\base\task\common\task_annotator.cc:165)
        base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl [0x00007FFC3EDF57AC+3372] (D:\work\fuzz\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:484)
        base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork [0x00007FFC3EDF43CC+524] (D:\work\fuzz\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:335)
        base::MessagePumpDefault::Run [0x00007FFC3EDC6E04+468] (D:\work\fuzz\chromium\src\base\message_loop\message_pump_default.cc:48)
        base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run [0x00007FFC3EDF7D44+1060] (D:\work\fuzz\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:644)
        base::RunLoop::Run [0x00007FFC3BB78D9F+1215] (D:\work\fuzz\chromium\src\base\run_loop.cc:142)
        content::RendererMain [0x00007FFC3E7F234F+3003] (D:\work\fuzz\chromium\src\content\renderer\renderer_main.cc:330)
        content::RunOtherNamedProcessTypeMain [0x00007FFC3B71E154+1456] (D:\work\fuzz\chromium\src\content\app\content_main_runner_impl.cc:750)
        content::ContentMainRunnerImpl::Run [0x00007FFC3B720992+2608] (D:\work\fuzz\chromium\src\content\app\content_main_runner_impl.cc:1108)
        content::RunContentProcess [0x00007FFC3B71BAD3+3015] (D:\work\fuzz\chromium\src\content\app\content_main.cc:344)
        content::ContentMain [0x00007FFC3B71C92E+416] (D:\work\fuzz\chromium\src\content\app\content_main.cc:372)
        ChromeMain [0x00007FFC2F0A14A6+930] (D:\work\fuzz\chromium\src\chrome\app\chrome_main.cc:176)
        MainDllLoader::Launch [0x00007FF6ABD762F9+2073] (D:\work\fuzz\chromium\src\chrome\app\main_dll_loader_win.cc:166)
        main [0x00007FF6ABD72C27+7099] (D:\work\fuzz\chromium\src\chrome\app\chrome_exe_main_win.cc:391)
        __scrt_common_main_seh [0x00007FF6AC1AF15C+268] (D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288)
        BaseThreadInitThunk [0x00007FFCCAF326BD+29]
        RtlUserThreadStart [0x00007FFCCC46DFB8+40]
Task trace:
Backtrace:
        IPC::`anonymous namespace'::ChannelAssociatedGroupController::Accept [0x00007FFC3C469D3B+3581] (D:\work\fuzz\chromium\src\ipc\ipc_mojo_bootstrap.cc:1018)
Crash keys:
  "gpu-generation-intel" = "0"
  "gpu-vsver" = "5.0"
  "gpu-psver" = "5.0"
  "gpu-driver" = "30.0.14.7212"
  "gpu-rev" = "161"
  "gpu-subid" = "0x221610de"
  "gpu_count" = "1"
  "gpu-devid" = "0x2216"
  "gpu-venid" = "0x10de"
  "view-count" = "1"
  "loaded-origin-0" = "devtools://devtools"
  "web-frame-count" = "1"
  "top-origin" = "devtools://devtools"
  "url-chunk" = "devtools://devtools/bundled/devtools_app.html?remoteBase=https://chrome-devtools-frontend.appspot.com/serve_file/@7f0aad0ea9d9757ee1db7c3c00ab722653800a9a/&can_dock=true"
  "blink_scheduler_async_stack" = "0x7FFC3C469D3B 0x0"
  "v8_ro_space_firstpage_address" = "0xc800000000"
  "v8_isolate_address" = "0x1257e8520400"
  "variations" = "2510663e-3f4a17df,df319cb2-27e0e1e8,c264dd48-8a1381f4,8963b549-3f4a17df,3e7d7783-f38a9353,586e7649-cc1e01dd,e5726113-3f4a17df,3e8fe123-3f4a17df,ba227809-3f4a17df,c5480a51-3f4a17df,15e85316-3f4a17df,aa21b4f1-3f4a17df,2e42ee4a-ade68764,d6284ba0-3be74c4d,9d165456-3f4a17df,13e2821-c0236c9e,eddd0d82-3f4a17df,13427e22-3f4a17df,f2855e3d-de2b6078,870c1db8-3f4a17df,42f0e0ea-75d6947c,87f33ad6-3f4a17df,afb5d7b8-3f4a17df,4d936449-fd549ada,88e143f7-e3ef03f6,1bb6a450-3f4a17df,1a80e9be-3898461f,250dda8b-3f4a17df,b6c668dd-3f4a17df,ef1cfe77-3f4a17df,9f476f76-3f4a17df,78634d5f-2ba5dc1c,4749874c-455e925b,7c2504d0-3f4a17df,c98a686c-3f4a17df,251b2579-3f4a17df,1acce950-3f4a17df,12733ec4-3f4a17df,206d80d-3f4a17df,a2fd384c-cc71bb94,e521d2ef-3f4a17df,55ba4cfa-3f4a17df,f654ad46-c94f66c2,f8b7087b-3d47f4f4,5c4d440e-58c8ac88,fd051c38-3f4a17df,cbc04857-3f4a17df,65570806-377be55a,d0143dc1-3f4a17df,42f1f10d-98837767,363012bc-3f4a17df,18324944-3f4a17df,520b2a89-88bf9f37,1584cf60-3f4a17df,81b1a2c3-3f4a17df,dfa02032-7ae17237,565dffc5-565dffc5,d92d97b4-e913bec6,4852ec7f-3f4a17df,483d5a5e-d379aaa3,263848e4-3f4a17df,3042ad4b-ad2fa222,3fd33f16-da51fc56,c297985a-3f4a17df,90bfc781-3f4a17df,e0e63e5f-decb98bf,f588ef31-3f4a17df,911e33b9-3f4a17df,829fa6ed-3f4a17df,95bc6922-3f4a17df,36d5ee52-3f4a17df,2f7e7ede-3f4a17df,61c68934-3f4a17df,5e3a236d-59e286d0,e79de56c-dee0823,357a64de-dee0823,8bccc03b-3f4a17df,7e398fb8-3f4a17df,5349039a-3f4a17df,d664a1aa-3f4a17df,625646ce-3f4a17df,53c131d9-e3ef03f6,a7780b9-3f4a17df,fcad39d1-3f4a17df,a79ba57a-f23d1dea,9e5c75f1-30e1b12b,c4e32a07-cd09e241,255dfea8-cf12f279,4cc28303-3f4a17df,1527f29f-3f4a17df,b3c9749a-3f4a17df,e440672e-3f4a17df,ca5a2953-ff983c32,da493d3c-3f4a17df,f3ed486d-3f4a17df,5c783e42-8f8fa88f,b3c54bb3-a04d2988,bde7927d-bab20a64,3482a891-410c5d63,4ff8f5b5-caf7a452,234de0a0-ace4e138,b7a22696-2cd5fcd8,3c68a36c-3f4a17df,ca12356a-3f4a17df,d3566fbd-c6f74b94,a779bb20-3f4a17df,ea23a088-5c589c16,e898a92c-3f4a17df,5f36436a-f799c15e,7fb629a1-60fdb59,2da2abac-b7f59038,186d6e2c-36c0e608,4ea303a6-3f4a17df,4949c1d8-3f4a17df,e3fd1192-3f4a17df,de95f00f-3f4a17df,fc7e4d22-3f4a17df,baee3c29-3f4a17df,9fe21c85-3f4a17df,68f0d29d-3f4a17df,15d3083e-5ce60213,c9e4cf65-802823a4,9a564e2a-3f4a17df,31af02a2-3f4a17df,371f259c-3f4a17df,cac0a91c-3f4a17df,d990c4ac-3f4a17df,5c7c8339-3f4a17df,a18444ea-a18444ea,ef4764d7-c9f4d4ef,9909b8ac-3f4a17df,e52d4c86-3f4a17df,1fce7d57-3f4a17df,7760b5b2-3f4a17df,e8c68789-49a20295,caa76e48-caa76e48,b0f15b33-b0f15b33,94f1fa38-66264bee,2b0207ee-2b0207ee,ad4acdda-3f4a17df,90860314-3f4a17df,931c5f72-3f4a17df,7ec047c2-3f4a17df,ade3efeb-e1cc0f14,b1ceb06f-3f4a17df,5e7b62b9-3f4a17df,db59f83a-3f4a17df,57675af7-3f4a17df,ec21b181-3f4a17df,160d8d8d-9d12ca0c,1d0518a-3f4a17df,fabf21f1-3f4a17df,6becb1e-a6ea97a2,f6e27768-f695fd79,3b96a1d-3f4a17df,dba92675-f23d1dea,595f5eb0-f23d1dea,bef5c006-3f4a17df,c98abd03-3bf4b625,17b84626-3f4a17df,8d7344de-3f4a17df,b53f3ef9-3f4a17df,2856aa31-3f4a17df,"
  "num-experiments" = "163"
  "switch-14" = "--disable-features=PrivateNetworkAccessForWorkersWarningOnly"
  "switch-13" = "--enable-features=BlockInsecurePrivateNetworkRequests,BlockInsec"
  "switch-12" = "--field-trial-handle=1804,i,13931548274380169838,687712020798452"
  "switch-11" = "--mojo-platform-channel-handle=4660"
  "switch-10" = "--launch-time-ticks=1067100715102"
  "switch-9" = "--time-ticks-at-unix-epoch=-1671688487142084"
  "switch-8" = "--renderer-client-id=10"
  "switch-7" = "--enable-main-frame-before-activation"
  "switch-6" = "--num-raster-threads=4"
  "switch-5" = "--device-scale-factor=1"
  "switch-4" = "--lang=zh-CN"
  "switch-3" = "--video-capture-use-gpu-memory-buffer"
  "switch-2" = "--enable-experimental-web-platform-features"
  "switch-1" = "--no-sandbox"
  "num-switches" = "16"
```

### [Deleted User] (2023-01-03)

[Empty comment from Monorail migration]

### wx...@gmail.com (2023-01-03)

the patch should be used in the release asan version, you can also use the debug version to trigger.

### wx...@gmail.com (2023-01-03)

[Empty comment from Monorail migration]

### wx...@gmail.com (2023-01-03)

here is the steps to trigger..I try to upload the video, but it failed.. so I upload to here
https://drive.google.com/file/d/12YFVOcVjV03hLXJxEejfQI0Ei8t4eewz/view?usp=sharing

### da...@chromium.org (2023-01-03)

> the patch should be used in the release asan version, you can also use the debug version to trigger.

Note that CHECK occurs in all builds of chrome, it does not need ASAN or debug builds. Whereas without the CHECK, a sanitizer build should produce a warning on the type confusion.. I think UBSAN should if there's a vtable, with the -fsanitize=vptr check enabled (it's in the default checks).

Can you please provide steps to reproduce?

### da...@chromium.org (2023-01-03)

This is happening in Mojo method LocalFrameMojoHandler::JavaScriptMethodExecuteRequest(), my understanding is this must be a method property that the browser requests to execute, via: https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/render_frame_host_impl.cc;l=2509-2522?ss=chromium%2Fchromium%2Fsrc&q=f:browser%20JavaScriptMethodExecuteRequest

### wx...@gmail.com (2023-01-03)

I think you follow the https://crbug.com/chromium/1404704#c6 steps to trigger in  the debug version without patch. 
here 
```
DevToolsUIBindings::DispatchProtocolMessage
->RenderFrameHostImpl::ExecuteJavaScriptMethod
->LocalFrameMojoHandler::JavaScriptMethodExecuteRequest
```
if you open devtools page, it will use the function DevToolsUIBindings::DispatchProtocolMessage. so we can set 
enter ```DevtoolsAPI.dispatchmessage=0x41414141;``` into the devtools page to cause type confusion. but it may need ui interaction.



### da...@chromium.org (2023-01-05)

1) Visit chrome://inspect
2) Click "Open dedicated DevTools for Node"
3) This opens a devtools popup window
4) In the popup window console, run ```DevtoolsAPI.dispatchmessage=0x41414141;```

There is no crash for me in ASAN M109.

Logically, the type confusion makes sense from the code inspection, if the method_name property can be controlled, however it's not clear how to reproduce that. So giving this a low severity.

The code has been around more than a year, tagging found in stable.

[Monorail components: Blink]

### [Deleted User] (2023-01-05)

[Empty comment from Monorail migration]

### bo...@chromium.org (2023-01-05)

I couldn't repro from #10 ("Open dedicated DevTools for Node" appears to require connecting to a running Node.js instance). However, I was able to trigger a CHECK in ToT (without any patches applied) by following these steps:

1) Visit chrome://inspect
2) Open devtools (F12/Ctrl-Shift-i/etc.)
3) Click on 'other' in the left hand pane.
4) Click 'inspect' on one of the 'devtools://' targets - this opens a devtools window
5) In the devtools window console, run `DevtoolsAPI.dispatchMessage=0x41414141;`

I hit this check:

[870122:1:0105/151854.899206:FATAL:v8_initializer.cc(727)] V8 error: Value is not a Function (v8::Function::Cast).
#0 0x7f377d7f117c base::debug::CollectStackTrace()
#1 0x7f377d5285ea base::debug::StackTrace::StackTrace()
#2 0x7f377d5285a5 base::debug::StackTrace::StackTrace()
#3 0x7f377d5790c9 logging::LogMessage::~LogMessage()
#4 0x7f3744f5423c blink::ReportV8FatalError()
#5 0x7f373cba55b5 v8::Function::CheckCast()
#6 0x7f3745e3990c blink::(anonymous namespace)::CallMethodOnFrame()
#7 0x7f3745e39136 blink::LocalFrameMojoHandler::JavaScriptMethodExecuteRequest()
#8 0x7f3747d953d2 blink::mojom::blink::LocalFrameStubDispatch::AcceptWithResponder()
#9 0x7f3745e49e89 blink::mojom::blink::LocalFrameStub<>::AcceptWithResponder()
#10 0x7f377cfcfef0 mojo::InterfaceEndpointClient::HandleValidatedMessage()
#11 0x7f377cfcfa39 mojo::InterfaceEndpointClient::HandleIncomingMessageThunk::Accept()
#12 0x7f377cfe7d8b mojo::MessageDispatcher::Accept()
#13 0x7f377cfd2026 mojo::InterfaceEndpointClient::HandleIncomingMessage()
#14 0x7f37743400de IPC::(anonymous namespace)::ChannelAssociatedGroupController::AcceptOnEndpointThread()
#15 0x7f3774334936 base::internal::FunctorTraits<>::Invoke<>()
#16 0x7f377433485d base::internal::InvokeHelper<>::MakeItSo<>()
#17 0x7f37743347dd _ZN4base8internal7InvokerINS0_9BindStateIMN3IPC12_GLOBAL__N_132ChannelAssociatedGroupControllerEFvN4mojo7MessageEEJ13scoped_refptrIS5_ES7_EEEFvvEE7RunImplIS9_NSt2Cr5tupleIJSB_S7_EEEJLm0ELm1EEEEvOT_OT0_NSG_16integer_sequenceImJXspT1_EEEE
#18 0x7f3774334757 base::internal::Invoker<>::RunOnce()
#19 0x7f377d4dec51 _ZNO4base12OnceCallbackIFvvEE3RunEv
#20 0x7f377d6d9e8e base::TaskAnnotator::RunTaskImpl()
#21 0x7f377d731770 base::TaskAnnotator::RunTask<>()
#22 0x7f377d73138b base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl()
#23 0x7f377d730512 base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()
#24 0x7f377d7316a3 base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()
#25 0x7f377d5a201f base::MessagePumpDefault::Run()
#26 0x7f377d731d75 base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run()
#27 0x7f377d658e65 base::RunLoop::Run()
#28 0x7f377aed2a11 content::RendererMain()
#29 0x7f377b4b89b1 content::RunZygote()
#30 0x7f377b4b94a8 content::RunOtherNamedProcessTypeMain()
#31 0x7f377b4ba6aa content::ContentMainRunnerImpl::Run()
#32 0x7f377b4b6989 content::RunContentProcess()
#33 0x7f377b4b7292 content::ContentMain()
#34 0x55d0096f41d3 ChromeMain
#35 0x55d0096f4052 main
#36 0x7f373262920a (/usr/lib/x86_64-linux-gnu/libc.so.6+0x29209)
#37 0x7f37326292bc __libc_start_main
#38 0x55d0096f3f6a _start

This method was added in https://crrev.com/cfb8f8d50b13023ac561d2b7b1bc14d254538557; sadym@, could you triage further?



[Monorail components: -Blink Platform>DevTools]

### ya...@google.com (2023-01-09)

Maksim is OOO. Mathias, is there anyone else who could take a look at this?

### ma...@chromium.org (2023-01-09)

Prior to Maksim, Benedikt was working on that CL. Benedikt, does https://crbug.com/chromium/1404704#c12 ring any bells?

### bm...@chromium.org (2023-01-09)

Simon, can you take a look please?

### gi...@appspot.gserviceaccount.com (2023-01-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/8e7cd572e5a76e436577e5d26460497da8667eea

commit 8e7cd572e5a76e436577e5d26460497da8667eea
Author: Simon Zünd <szuend@chromium.org>
Date: Wed Jan 11 05:55:14 2023

[devtools] Ensure that invoked method is an actual v8::Function

CallMethodOnFrame invokes a function part of an object which in turn
is installed on globalThis. E.g. globalThis['foo'].bar();

CallMethodOnFrame already bails out if 'foo' or 'bar' can't be found,
but we should also bail out if 'bar' is not an actual function.

Fixed: 1404704
Change-Id: I67c0883a53b358176898bd04fad3c45cf98721ed
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4150308
Reviewed-by: David Bokan <bokan@chromium.org>
Commit-Queue: Simon Zünd <szuend@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1091189}

[modify] https://crrev.com/8e7cd572e5a76e436577e5d26460497da8667eea/third_party/blink/renderer/core/frame/local_frame_mojo_handler.cc


### sz...@chromium.org (2023-01-11)

Thanks for the report! Fix is in-flight here: https://crrev.com/c/4150308.

Please note that this bug can only be exploited if the DevTools renderer has been compromised already.

### wx...@gmail.com (2023-01-11)

LGTM

### wx...@gmail.com (2023-01-11)

there also have a similar bug https://crbug.com/chromium/1405574, could you please also take a look ?

### [Deleted User] (2023-01-11)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-11)

[Empty comment from Monorail migration]

### am...@google.com (2023-01-26)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-01-27)

Congratulations! The VRP Panel has decided to award you $1,000 for this report of a heavily mitigated security bug. Thank you for your efforts and reporting this issue to us. 

### am...@google.com (2023-01-28)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-03-06)

[Empty comment from Monorail migration]

### am...@google.com (2023-03-07)

[Empty comment from Monorail migration]

### pg...@google.com (2023-03-07)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-20)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-04-20)

This issue was migrated from crbug.com/chromium/1404704?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062478)*
