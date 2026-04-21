# memory corruption in blink::ReadableStreamDefaultControllerWithScriptScope::Enqueue

| Field | Value |
|-------|-------|
| **Issue ID** | [40062564](https://issues.chromium.org/issues/40062564) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebRTC |
| **Platforms** | Linux, Mac |
| **Reporter** | em...@gmail.com |
| **Assignee** | gu...@chromium.org |
| **Created** | 2023-01-09 |
| **Bounty** | $3,000.00 |

## Description

**Steps to reproduce the problem:**  

os version:  

macos 12.6  

ubuntu 22.04  

chrome version:  

110.0.5467.0(for mac)  

110.0.5467.0(for ubuntu)  

111.0.5523.0(for ubuntu)

repro steps:

1. python3 -m http.server 8000 --dir=|path|
2. ./chrome <http://localhost:8000/crash.html> --incognito --user-data-dir=/tmp/x1 --disable-gpu --no-sandbox --user-data-dir=/tmp/x --use-fake-ui-for-media-stream  
   
   Many different crashes will be reproduced in ubuntu every time, I provided 3 of them in the attachment.  
   
   Only one kind of crash (Received signal 11 SEGV\_MAPERR 375bbd5a1758002) will be reproduced in mac (asan version).

**Problem Description:**  

Received signal 11 SEGV\_ACCERR 7db000002470  

#0 0x56105b7169b7 in backtrace /b/s/w/ir/cache/builder/src/third\_party/llvm/compiler-rt/lib/asan/../sanitizer\_common/sanitizer\_common\_interceptors.inc:4434:13  

#1 0x56106d24e59c in base::debug::CollectStackTrace(void\*\*, unsigned long) ./../../base/debug/stack\_trace\_posix.cc:894:7  

#2 0x56106cf934f2 in StackTrace ./../../base/debug/stack\_trace.cc:221:12  

#3 0x56106cf934f2 in base::debug::StackTrace::StackTrace() ./../../base/debug/stack\_trace.cc:218:28  

#4 0x56106d24cf3e in base::debug::(anonymous namespace)::StackDumpSignalHandler(int, siginfo\_t\*, void\*) ./../../base/debug/stack\_trace\_posix.cc:387:3  

#5 0x7f6f6d502520 in \_\_GI\_\_\_sigaction :?  

#6 0x561060e16798 in \_\_cxx\_atomic\_store<int> ./../../buildtools/third\_party/libc++/trunk/include/atomic:936:5  

#7 0x561060e16798 in store ./../../buildtools/third\_party/libc++/trunk/include/atomic:1529:10  

#8 0x561060e16798 in atomic\_store\_explicit<int> ./../../buildtools/third\_party/libc++/trunk/include/atomic:1878:10  

#9 0x561060e16798 in Release\_Store ./../../v8/src/base/atomicops.h:207:3  

#10 0x561060e16798 in Release\_Store<unsigned int> ./../../v8/src/base/atomic-utils.h:102:5  

#11 0x561060e16798 in Release\_Store ./../../v8/src/objects/tagged-field-inl.h:203:3  

#12 0x561060e16798 in set\_call\_code ./gen/v8/torque-generated/src/objects/templates-tq-inl.inc:359:3  

#13 0x561060e16798 in v8::FunctionTemplate::SetCallHandler(void (\*)(v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&), v8::Local[v8::Value](javascript:void(0);), v8::SideEffectType, v8::MemorySpan<v8::CFunction const> const&) ./../../v8/src/api/api.cc:1583:9  

#14 0x561060e15394 in v8::(anonymous namespace)::FunctionTemplateNew(v8::internal::Isolate\*, void (\*)(v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&), v8::Local[v8::Value](javascript:void(0);), v8::Local[v8::Signature](javascript:void(0);), int, v8::ConstructorBehavior, bool, v8::Local[v8::Private](javascript:void(0);), v8::SideEffectType, v8::MemorySpan<v8::CFunction const> const&, unsigned char, unsigned char, unsigned char) ./../../v8/src/api/api.cc:1442:26  

#15 0x561060e14d64 in v8::FunctionTemplate::New(v8::Isolate\*, void (\*)(v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&), v8::Local[v8::Value](javascript:void(0);), v8::Local[v8::Signature](javascript:void(0);), int, v8::ConstructorBehavior, v8::SideEffectType, v8::CFunction const\*, unsigned short, unsigned short, unsigned short) ./../../v8/src/api/api.cc:1490:10  

#16 0x56107cdc4af6 in blink::WrapperTypeInfo::GetV8ClassTemplate(v8::Isolate\*, blink::DOMWrapperWorld const&) const ./../../third\_party/blink/renderer/platform/bindings/wrapper\_type\_info.cc:0:0  

#17 0x56107cdaf8b7 in blink::V8ObjectConstructor::CreateInterfaceObject(blink::WrapperTypeInfo const\*, v8::Local[v8::Context](javascript:void(0);), blink::DOMWrapperWorld const&, v8::Isolate\*, v8::Local[v8::Function](javascript:void(0);), blink::V8ObjectConstructor::CreationMode) ./../../third\_party/blink/renderer/platform/bindings/v8\_object\_constructor.cc:78:13  

#18 0x56107cda7227 in blink::V8PerContextData::ConstructorForTypeSlowCase(blink::WrapperTypeInfo const\*) ./../../third\_party/blink/renderer/platform/bindings/v8\_per\_context\_data.cc:129:7  

#19 0x56107cda6c1e in blink::V8PerContextData::CreateWrapperFromCacheSlowCase(blink::WrapperTypeInfo const\*) ./../../third\_party/blink/renderer/platform/bindings/v8\_per\_context\_data.cc:98:46  

#20 0x56107cda4e55 in blink::V8DOMWrapper::CreateWrapper(blink::ScriptState\*, blink::WrapperTypeInfo const\*) ./../../third\_party/blink/renderer/platform/bindings/v8\_dom\_wrapper.cc:57:33  

#21 0x56107cd94083 in blink::ScriptWrappable::Wrap(blink::ScriptState\*) ./../../third\_party/blink/renderer/platform/bindings/script\_wrappable.cc:28:8  

#22 0x561079068b31 in blink::ToV8(blink::ScriptWrappable\*, v8::Local[v8::Object](javascript:void(0);), v8::Isolate\*) ./../../third\_party/blink/renderer/platform/bindings/to\_v8.h:47:19  

#23 0x5610849e21f3 in ToV8<blink::RTCEncodedAudioFrame \*&> ./../../third\_party/blink/renderer/platform/bindings/to\_v8.h:366:10  

#24 0x5610849e21f3 in void blink::ReadableStreamDefaultControllerWithScriptScope::Enqueue[blink::RTCEncodedAudioFrame\\*](javascript:void(0);)(blink::RTCEncodedAudioFrame\*) const ./../../third\_party/blink/renderer/core/streams/readable\_stream\_default\_controller\_with\_script\_scope.h:37:37  

#25 0x5610849e1e6e in blink::RTCEncodedAudioUnderlyingSource::OnFrameFromSource(std::Cr::unique\_ptr<webrtc::TransformableFrameInterface, std::Cr::default\_delete[webrtc::TransformableFrameInterface](javascript:void(0);)>) ./../../third\_party/blink/renderer/modules/peerconnection/rtc\_encoded\_audio\_underlying\_source.cc:96:17  

#26 0x561084a1d2ba in blink::RTCRtpSender::OnAudioFrameFromEncoder(std::Cr::unique\_ptr<webrtc::TransformableFrameInterface, std::Cr::default\_delete[webrtc::TransformableFrameInterface](javascript:void(0);)>) ./../../third\_party/blink/renderer/modules/peerconnection/rtc\_rtp\_sender.cc:954:44  

#27 0x561084a217f2 in Invoke<void (blink::RTCRtpSender::\*)(std::Cr::unique\_ptr<webrtc::TransformableFrameInterface, std::Cr::default\_delete[webrtc::TransformableFrameInterface](javascript:void(0);) >), cppgc::internal::BasicCrossThreadPersistent<

**Additional Comments:**

\*\*Chrome version: \*\* 110.0.5467.0 \*\*Channel: \*\* Stable

**OS:** Linux

## Attachments

- [crash.html](attachments/crash.html) (text/plain, 1.7 KB)
- [worker.js](attachments/worker.js) (text/plain, 81 B)
- [sig11-crash.log](attachments/sig11-crash.log) (text/plain, 12.7 KB)
- [stack-use-after-return.log](attachments/stack-use-after-return.log) (text/plain, 13.6 KB)
- [security-check-failed.log](attachments/security-check-failed.log) (text/plain, 15.1 KB)
- [heap-buffer-overflow.log](attachments/heap-buffer-overflow.log) (text/plain, 20.0 KB)
- [crash2.html](attachments/crash2.html) (text/plain, 1.9 KB)
- [launcher.sh](attachments/launcher.sh) (text/plain, 528 B)

## Timeline

### [Deleted User] (2023-01-09)

[Empty comment from Monorail migration]

### da...@chromium.org (2023-01-09)

The heap-buffer-overflow trace is v8::internal::HandleScope::ZapRange() zapping past its range:
  0x62500000e8f0 is located 0 bytes after 8176-byte region
which was previously set in v8::internal::HandleScope::Extend

Trying to repro on linux asan, but not getting any crash. I am trying without --use-fake-ui-for-media-stream, which is only meant to be used in tests.

If the crashes require that flag, then it represents bugs that can affect tests and cause flakiness but doesn't represent a security bug.

Reporter: do you have any repro that doesn't require that flag?

### em...@gmail.com (2023-01-10)

This is a new poc that can be reproduced without the --use-fake-ui-for-media-stream flag. When running, a 'use microphone' prompt will appear, click "allow".

In Linux:

./chrome http://localhost:8001/crash2.html --incognito --user-data-dir=/tmp/x1x3 --no-sandbox --no-zygote

In MacOS:

/Chromium.app/Contents/MacOS/Chromium --user-data-dir=/tmp/xx1 http://localhost:8001/crash2.html

It is easier to reproduce on MacOS without any flag.

### dc...@chromium.org (2023-01-13)

(This looks like a legitimate report; however, I have not been able to reproduce yet. I will try on a Mac later)

### dc...@chromium.org (2023-01-14)

I can reproduce this on a Mac but not on Linux. However, I cannot get a stack trace out of the ASAN prebuilt. The crash I'm seeing looks like a null dereference right now... will try a few more times.

### dc...@chromium.org (2023-01-14)

Hmm... now I'm having trouble with the repro case. I got it to crash once but it hasn't crashed since...

### em...@gmail.com (2023-01-14)

I can reproduce it stably on both Mac and Linux on my pc.Can you try this script (you need to modify the chrome path and crash.html path) by opening multiple browsers? 
thanks.


### em...@gmail.com (2023-01-14)

tested pc:
MacBook Pro 2021 
os version 12.6
chrome version:
asan-mac-release-1081214

### bo...@google.com (2023-01-18)

I also cannot reproduce this crash on Linux and I don't have an M1/M2 Mac to try. 

For transparency, I'm using this launcher script with the POC address passed from the command line, and hosted from a secure context:

#!/bin/bash
$CHROME_ASAN --incognito --user-data-dir=/tmp/x1 --disable-gpu --no-sandbox --no-zygote $1 &
$CHROME_ASAN --incognito --user-data-dir=/tmp/x2 --disable-gpu --no-sandbox --no-zygote $1 &
$CHROME_ASAN --incognito --user-data-dir=/tmp/x3 --disable-gpu --no-sandbox --no-zygote $1 && fg

I'm asking around to see if a colleague with an AArch64 Mac can attempt to reproduce, but for now this is inactionable until we have a reliable POC. 

### nh...@google.com (2023-01-18)

I was able to reproduce this with an asan build on an m1 mac using the PoC from https://crbug.com/chromium/1406034#c3. Here's the ASAN stacktrace:

[71612:259:0118/145416.838855:FATAL:permission_bubble_media_access_handler.cc(379)] Check failed: request_it != requests_map.end().
0   Chromium Framework                  0x000000028fba1688 base::debug::CollectStackTrace(void**, unsigned long) + 28
1   Chromium Framework                  0x000000028f8f08f8 base::debug::StackTrace::StackTrace() + 36
2   Chromium Framework                  0x000000028f939ac8 logging::LogMessage::~LogMessage() + 696
3   Chromium Framework                  0x000000028f93ba28 logging::LogMessage::~LogMessage() + 12
4   Chromium Framework                  0x000000028f8db750 logging::CheckError::~CheckError() + 88
5   Chromium Framework                  0x000000028ea413bc PermissionBubbleMediaAccessHandler::OnAccessRequestResponse(content::WebContents*, long long, blink::mojom::StreamDevicesSet const&, blink::mojom::MediaStreamRequestResult, std::Cr::unique_ptr<content::MediaStreamUI, std::Cr::default_delete<content::MediaStreamUI>>) + 952
6   Chromium Framework                  0x000000028ea421d4 PermissionBubbleMediaAccessHandler::OnAccessRequestResponseForBinding(content::WebContents*, long long, mojo::StructPtr<blink::mojom::StreamDevicesSet>, blink::mojom::MediaStreamRequestResult, std::Cr::unique_ptr<content::MediaStreamUI, std::Cr::default_delete<content::MediaStreamUI>>) + 312
7   Chromium Framework                  0x000000028ea4398c void base::internal::FunctorTraits<void (PermissionBubbleMediaAccessHandler::*)(content::WebContents*, long long, mojo::StructPtr<blink::mojom::StreamDevicesSet>, blink::mojom::MediaStreamRequestResult, std::Cr::unique_ptr<content::MediaStreamUI, std::Cr::default_delete<content::MediaStreamUI>>), void>::Invoke<void (PermissionBubbleMediaAccessHandler::*)(content::WebContents*, long long, mojo::StructPtr<blink::mojom::StreamDevicesSet>, blink::mojom::MediaStreamRequestResult, std::Cr::unique_ptr<content::MediaStreamUI, std::Cr::default_delete<content::MediaStreamUI>>), base::WeakPtr<PermissionBubbleMediaAccessHandler>, content::WebContents*, long long, mojo::StructPtr<blink::mojom::StreamDevicesSet>, blink::mojom::MediaStreamRequestResult, std::Cr::unique_ptr<content::MediaStreamUI, std::Cr::default_delete<content::MediaStreamUI>>>(void (PermissionBubbleMediaAccessHandler::*)(content::WebContents*, long long, mojo::StructPtr<blink::mojom::StreamDevicesSet>, blink::mojom::MediaStreamRequestResult, std::Cr::unique_ptr<content::MediaStreamUI, std::Cr::default_delete<content::MediaStreamUI>>), base::WeakPtr<PermissionBubbleMediaAccessHandler>&&, content::WebContents*&&, long long&&, mojo::StructPtr<blink::mojom::StreamDevicesSet>&&, blink::mojom::MediaStreamRequestResult&&, std::Cr::unique_ptr<content::MediaStreamUI, std::Cr::default_delete<content::MediaStreamUI>>&&) + 428
8   Chromium Framework                  0x000000028ea4372c base::internal::Invoker<base::internal::BindState<void (PermissionBubbleMediaAccessHandler::*)(content::WebContents*, long long, mojo::StructPtr<blink::mojom::StreamDevicesSet>, blink::mojom::MediaStreamRequestResult, std::Cr::unique_ptr<content::MediaStreamUI, std::Cr::default_delete<content::MediaStreamUI>>), base::WeakPtr<PermissionBubbleMediaAccessHandler>, base::internal::UnretainedWrapper<content::WebContents, base::unretained_traits::MayNotDangle>, long long, mojo::StructPtr<blink::mojom::StreamDevicesSet>, blink::mojom::MediaStreamRequestResult, std::Cr::unique_ptr<content::MediaStreamUI, std::Cr::default_delete<content::MediaStreamUI>>>, void ()>::RunOnce(base::internal::BindStateBase*) + 316
9   Chromium Framework                  0x000000028fa66938 base::TaskAnnotator::RunTaskImpl(base::PendingTask&) + 824
10  Chromium Framework                  0x000000028fad7898 base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) + 2928
11  Chromium Framework                  0x000000028fad61c8 base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() + 412
12  Chromium Framework                  0x000000028fbe710c base::MessagePumpCFRunLoopBase::RunWork() + 368
13  Chromium Framework                  0x000000028fbcd9a4 base::mac::CallWithEHFrame(void () block_pointer) + 16
14  Chromium Framework                  0x000000028fbe4c74 base::MessagePumpCFRunLoopBase::RunWorkSource(void*) + 320
15  CoreFoundation                      0x0000000186e7ca18 __CFRUNLOOP_IS_CALLING_OUT_TO_A_SOURCE0_PERFORM_FUNCTION__ + 28
16  CoreFoundation                      0x0000000186e7c9ac __CFRunLoopDoSource0 + 176
17  CoreFoundation                      0x0000000186e7c71c __CFRunLoopDoSources0 + 244
18  CoreFoundation                      0x0000000186e7b320 __CFRunLoopRun + 836
19  CoreFoundation                      0x0000000186e7a888 CFRunLoopRunSpecific + 612
20  HIToolbox                           0x000000019054ffa0 RunCurrentEventLoopInMode + 292
21  HIToolbox                           0x000000019054fde4 ReceiveNextEventCommon + 672
22  HIToolbox                           0x000000019054fb2c _BlockUntilNextEventMatchingListInModeWithFilter + 72
23  AppKit                              0x000000018a0fc424 _DPSNextEvent + 632
24  AppKit                              0x000000018a0fb5b4 -[NSApplication(NSEvent) _nextEventMatchingEventMask:untilDate:inMode:dequeue:] + 728
25  Chromium Framework                  0x000000028e86ae94 __71-[BrowserCrApplication nextEventMatchingMask:untilDate:inMode:dequeue:]_block_invoke + 364
26  Chromium Framework                  0x000000028fbcd9a4 base::mac::CallWithEHFrame(void () block_pointer) + 16
27  Chromium Framework                  0x000000028e86aaa0 -[BrowserCrApplication nextEventMatchingMask:untilDate:inMode:dequeue:] + 624
28  AppKit                              0x000000018a0ef9e4 -[NSApplication run] + 464
29  Chromium Framework                  0x000000028fbe91b8 base::MessagePumpNSApplication::DoRun(base::MessagePump::Delegate*) + 736
30  Chromium Framework                  0x000000028fbe3984 base::MessagePumpCFRunLoopBase::Run(base::MessagePump::Delegate*) + 628
31  Chromium Framework                  0x000000028fad9d54 base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) + 1172
32  Chromium Framework                  0x000000028f9f43a4 base::RunLoop::Run(base::Location const&) + 1160
33  Chromium Framework                  0x00000002889728e0 content::BrowserMainLoop::RunMainMessageLoop() + 600
34  Chromium Framework                  0x00000002889782b8 content::BrowserMainRunnerImpl::Run() + 284
35  Chromium Framework                  0x000000028896c7fc content::BrowserMain(content::MainFunctionParams) + 476
36  Chromium Framework                  0x000000028d3ee374 content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate*) + 564
37  Chromium Framework                  0x000000028d3f12c4 content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) + 1508
38  Chromium Framework                  0x000000028d3f0920 content::ContentMainRunnerImpl::Run() + 1560
39  Chromium Framework                  0x000000028d3ec998 content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) + 4192
40  Chromium Framework                  0x000000028d3ed070 content::ContentMain(content::ContentMainParams) + 312
41  Chromium Framework                  0x0000000280006854 ChromeMain + 1044
42  Chromium                            0x0000000102e24c58 main + 576
43  dyld                                0x0000000186a73e50 start + 2544
Task trace:
0   Chromium Framework                  0x000000028f4e8028 ___ZN24system_media_permissions12_GLOBAL__N_129MediaAuthorizationWrapperImpl25RequestAccessForMediaTypeEP8NSStringN4base12OnceCallbackIFvvEEE_block_invoke + 312
Crash keys:
  "ui_scheduler_async_stack" = "0x28F4E8028 0x0"
  "gpu-glver" = "OpenGL ES 2.0.0 (ANGLE 2.1.1 git hash: 63a2848a1264)"
  "gpu-generation-intel" = "0"
  "gpu-vsver" = "1.00"
  "gpu-psver" = "1.00"
  "gpu-driver" = "83"
  "gpu_count" = "1"
  "gpu-devid" = "0x0000"
  "gpu-venid" = "0x106b"
  "num-extensions" = "0"
  "breadcrumbs" = "0:00:06 Tab1 PageLoad
0:00:06 Tab1 FinishNav3
0:00:06 Tab1 StartNav3 #renderer-script #link
0:00:01 PermissionBubbleRequest
0:00:01 Tab1 PageLoad
0:00:01 Tab1 FinishNav2
0:00:01 Tab1 StartNav2 #renderer-script #link
0:00:01 Tab1 FinishNav1
0:00:00 Tab1 AddInfobar45
0:00:00 Browser1 Insert active Tab1 at 0
0:00:00 Tab1 StartNav1 #auto_toplevel
0:00:00 Startup
"
  "amfi-status" = "rv=0 status=0x0 allow_everything=0"
  "io_scheduler_async_stack" = "0x290093DC4 0x0"
  "variations" = "db59f83a-3f4a17df,8bccc03b-3f4a17df,2510663e-73703436,d5a65352-3f4a17df,7f6bf080-3f4a17df,5349039a-3f4a17df,9f476f76-3f4a17df,f3ed486d-3f4a17df,36d5ee52-3f4a17df,65570806-377be55a,ade3efeb-e1cc0f14,3fd33f16-27b09c4c,3095b8fe-3f4a17df,4ff8f5b5-caf7a452,17b84626-3f4a17df,92d2eb18-fa10226e,5f36436a-f799c15e,4852ec7f-3f4a17df,baee3c29-3f4a17df,9fe21c85-3f4a17df,250dda8b-3f4a17df,255dfea8-cf12f279,7c2504d0-3f4a17df,b3c54bb3-a04d2988,ef4764d7-c9f4d4ef,a779bb20-3f4a17df,f0682056-8259003e,2da2abac-b7f59038,d3566fbd-c6f74b94,741e95d4-3f4a17df,520b2a89-88bf9f37,b3c9749a-3f4a17df,1527f29f-3f4a17df,c4e32a07-cd09e241,1d0518a-3f4a17df,68f0d29d-3f4a17df,c98abd03-3bf4b625,42f1f10d-98837767,ad4acdda-3f4a17df,7fb629a1-60fdb59,90860314-3f4a17df,d6284ba0-3be74c4d,68971777-6f116e34,ca12356a-3f4a17df,931c5f72-3f4a17df,b1ceb06f-3f4a17df,afb5d7b8-3f4a17df,8c82550d-3f4a17df,9909b8ac-3f4a17df,2856aa31-3f4a17df,a2fd384c-cc71bb94,1fce7d57-3f4a17df,e8c68789-49a20295,d990c4ac-3f4a17df,e0e63e5f-decb98bf,f588ef31-3f4a17df,911e33b9-3f4a17df,5c7c8339-3f4a17df,e521d2ef-3f4a17df,7ec047c2-3f4a17df,3482a891-410c5d63,ec21b181-3f4a17df,53c131d9-e3ef03f6,4d936449-fd549ada,9e5c75f1-30e1b12b,1acce950-3f4a17df,c98a686c-3f4a17df,a18444ea-a18444ea,eddd0d82-3f4a17df,99c32967-f0a9a61e,df319cb2-27e0e1e8,4749874c-455e925b,caa76e48-caa76e48,26db9e79-f430c221,b6c668dd-3f4a17df,b0f15b33-b0f15b33,25fa4483-b9406639,7760b5b2-3f4a17df,5c4d440e-58c8ac88,de95f00f-3f4a17df,f112d133-3f4a17df,75ffb03a-3f4a17df,e52d4c86-3f4a17df,a8cfdb40-3f4a17df,234de0a0-ace4e138,e3fd1192-3f4a17df,f8b7087b-3d47f4f4,13427e22-3f4a17df,13e2821-c0236c9e,1d167f26-3f4a17df,8d7344de-3f4a17df,910af27f-3f4a17df,c9e4cf65-802823a4,e5726113-3f4a17df,586e7649-cc1e01dd,7a842d4a-b3a17800,ea23a088-41c37e8a,f2855e3d-de2b6078,fd051c38-3f4a17df,87f33ad6-3f4a17df,17cd3426-3f4a17df,da493d3c-3f4a17df,5c783e42-8f8fa88f,e898a92c-3f4a17df,1bb6a450-3f4a17df,bde7927d-bab20a64,870c1db8-3f4a17df,ef1cfe77-3f4a17df,363012bc-3f4a17df,263848e4-3f4a17df,95bc6922-3f4a17df,a79ba57a-f23d1dea,4949c1d8-3f4a17df,371f259c-3f4a17df,e11c0dd9-3586c521,f6e27768-f695fd79,3b96a1d-3f4a17df,6becb1e-a6ea97a2,595f5eb0-f23d1dea,dba92675-f23d1dea,42f0e0ea-75d6947c,160d8d8d-9d12ca0c,4ea303a6-3f4a17df,3042ad4b-ad2fa222,f654ad46-c94f66c2,cbc04857-3f4a17df,81b1a2c3-3f4a17df,1584cf60-3f4a17df,bbaef9b4-3f4a17df,55ba4cfa-3f4a17df,fc7e4d22-3f4a17df,c297985a-3f4a17df,8963b549-3f4a17df,8c153587-3f4a17df,7b9d3e0c-1dfe4688,d92d97b4-e913bec6,94f1fa38-66264bee,565dffc5-565dffc5,d0143dc1-3f4a17df,15d3083e-5ce60213,9a564e2a-3f4a17df,57675af7-3f4a17df,d664a1aa-3f4a17df,3e7d7783-a4655118,18324944-3f4a17df,2b0207ee-2b0207ee,206d80d-3f4a17df,186d6e2c-36c0e608,8987712e-3f4a17df,653bb15c-3f4a17df,2f7e7ede-3f4a17df,c5480a51-3f4a17df,31af02a2-3f4a17df,ed2101b4-3f4a17df,d6ad7f9a-a9080253,de0fa677-de0fa677,ad46906e-14a9a32f,a4dcbdd6-99907adb,f48c01d3-6eb2bd2b,b357b792-3f4a17df,ee9c60c1-3d47f4f4,9481ce98-3d47f4f4,4b935545-3d47f4f4,70678518-dee66fa8,be338734-dee66fa8,5f9907a9-dee66fa8,8eeccb9a-dee66fa8,2b465683-dee66fa8,9a38bae3-3d47f4f4,2d1e43a3-3d47f4f4,d69d967d-3695c92e,"
  "num-experiments" = "171"
  "switch-2" = "http://localhost:8000/crash2.html"
  "switch-1" = "--user-data-dir=/tmp/poc"
  "num-switches" = "4"
  "osarch" = "arm64"
  "pid" = "71612"
  "ptype" = "browser"

### em...@gmail.com (2023-01-18)

Thanks for your repro test.
This stack does not seem to be the result I expected. Can you test it again with manually click "allow" when "use cameraphone" pops up?.
It should reproduce an error like "Received signal 11 SEGV_ACCERR 375bc45a177bbd5".
thanks.

### bo...@google.com (2023-01-19)

Thank you @nharper! Both https://crbug.com/chromium/1406034#c10 and https://crbug.com/chromium/1406034#c11 are enough of an indication of bugs to warrant asking code owners to take a closer look.

Setting security flags:
- High severity due to memory corruption that can plausibly lead to remote code execution in the renderer sandbox. 
- Only Mac and Linux for now - even though we haven't been able to repro on Linux - but nothing about the call stack obviously suggests platform specific code. 
- Because of the difficulty we had reproducing this bug, FoundIn-110 is based only on the reporter's assessment. 

@owners - Thanks for your help! We found it infeasible to reproduce this report without an Aarch64 Mac, so if you struggle to diagnose the root cause through static analysis alone it may be more practical to set up a debug environment on a new Mac. 

[Monorail components: Blink>Network>StreamsAPI]

### [Deleted User] (2023-01-19)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-19)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-01-19)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ri...@chromium.org (2023-01-20)

The stack trace in #10 is in the browser process, whereas the original report is for a crash in the render process. I suspect there are two different bugs here.

### ri...@chromium.org (2023-01-20)

All ReadableStreamDefaultControllerWithScriptScope::Enqueue() is doing is entering a ScriptState::Scope and calling ToV8(). So although it appears in the stack trace I don't think it is the cause of the issue.

[Monorail components: -Blink>Network>StreamsAPI Blink>WebRTC]

### em...@gmail.com (2023-01-20)

[Comment Deleted]

### ni...@chromium.org (2023-01-20)

Hi Tomas, could you please take a look at this as a WebRTC owner? Thank you!

### to...@chromium.org (2023-01-20)

Guido - do you mind taking a look and see what the next steps could be?

From quickly looking at this, my guess is that audio_from_encoder_underlying_source_ (rtc_rtp_sender.cc) is being dereferenced without checking first if it's valid. This might potentially be related to this change or family of changes:

https://chromium-review.googlesource.com/c/chromium/src/+/3904102

### to...@chromium.org (2023-01-20)

[Empty comment from Monorail migration]

### gu...@chromium.org (2023-01-20)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-01-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/7590897a14ae86d3e357f6c5bfc9ec6bf087ba76

commit 7590897a14ae86d3e357f6c5bfc9ec6bf087ba76
Author: Guido Urdaneta <guidou@chromium.org>
Date: Fri Jan 20 19:31:46 2023

Fix audio check in RtcRtpSender

createEncodedAudioStreams() was incorrectly checking the presence of
video streams instead of audio streams.

Bug: 1406034
Change-Id: I1b18a28896afa8ecc639c3b999e10d93a2e9654c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4184358
Commit-Queue: Guido Urdaneta <guidou@chromium.org>
Commit-Queue: Tomas Gunnarsson <tommi@chromium.org>
Reviewed-by: Tomas Gunnarsson <tommi@chromium.org>
Auto-Submit: Guido Urdaneta <guidou@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1095169}

[modify] https://crrev.com/7590897a14ae86d3e357f6c5bfc9ec6bf087ba76/third_party/blink/web_tests/external/wpt/webrtc-encoded-transform/RTCPeerConnection-insertable-streams-video.https.html
[modify] https://crrev.com/7590897a14ae86d3e357f6c5bfc9ec6bf087ba76/third_party/blink/web_tests/external/wpt/webrtc-encoded-transform/RTCPeerConnection-insertable-streams-audio.https.html
[modify] https://crrev.com/7590897a14ae86d3e357f6c5bfc9ec6bf087ba76/third_party/blink/renderer/modules/peerconnection/rtc_rtp_sender.cc


### gu...@chromium.org (2023-01-21)

emilykim8708@: Can you try with the patch in https://crbug.com/chromium/1406034#c23 applied?

crash2.html produced the crash for me in seconds. After the patch I ran it for 20 minutes without issue.



### em...@gmail.com (2023-01-21)

confirmed.
OS:
macos:12.6
ubuntu:22.04
The issue did not repro after patching.

### gu...@chromium.org (2023-01-21)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-21)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-21)

[Empty comment from Monorail migration]

### gu...@chromium.org (2023-01-21)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-21)

Merge review required: M110 is already shipping to beta.

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

### am...@chromium.org (2023-01-23)

M110 merge approved, please merge this fix to branch 5481 at soonest -- thank you! 

### gi...@appspot.gserviceaccount.com (2023-01-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/5d601af37e836d583c2ee48114b1a13b912a2d2b

commit 5d601af37e836d583c2ee48114b1a13b912a2d2b
Author: Guido Urdaneta <guidou@chromium.org>
Date: Mon Jan 23 21:56:18 2023

Fix audio check in RtcRtpSender

createEncodedAudioStreams() was incorrectly checking the presence of
video streams instead of audio streams.

(cherry picked from commit 7590897a14ae86d3e357f6c5bfc9ec6bf087ba76)

Bug: 1406034
Change-Id: I1b18a28896afa8ecc639c3b999e10d93a2e9654c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4184358
Commit-Queue: Guido Urdaneta <guidou@chromium.org>
Commit-Queue: Tomas Gunnarsson <tommi@chromium.org>
Reviewed-by: Tomas Gunnarsson <tommi@chromium.org>
Auto-Submit: Guido Urdaneta <guidou@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1095169}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4190056
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/5481@{#591}
Cr-Branched-From: 130f3e4d850f4bc7387cfb8d08aa993d288a67a9-refs/heads/main@{#1084008}

[modify] https://crrev.com/5d601af37e836d583c2ee48114b1a13b912a2d2b/third_party/blink/web_tests/external/wpt/webrtc-encoded-transform/RTCPeerConnection-insertable-streams-video.https.html
[modify] https://crrev.com/5d601af37e836d583c2ee48114b1a13b912a2d2b/third_party/blink/web_tests/external/wpt/webrtc-encoded-transform/RTCPeerConnection-insertable-streams-audio.https.html
[modify] https://crrev.com/5d601af37e836d583c2ee48114b1a13b912a2d2b/third_party/blink/renderer/modules/peerconnection/rtc_rtp_sender.cc


### am...@google.com (2023-01-26)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-01-26)

Congratulations on another one, Cassidy Kim! The VRP Panel has decided to award you $3,000 for this report of a mitigated WebRTC security bug. Thank you for your efforts and reporting this issue to us -- nice work! 

### am...@google.com (2023-01-28)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-29)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1406034?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062564)*
