# UNKNOWN in blink::WebSpeechSynthesisVoice::operator

| Field | Value |
|-------|-------|
| **Issue ID** | [40081337](https://issues.chromium.org/issues/40081337) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Speech |
| **Reporter** | ch...@gmail.com |
| **Assignee** | to...@chromium.org |
| **Created** | 2015-02-05 |
| **Bounty** | $2,000.00 |

## Description

**VERSION**  

Chrome Version: Chromium 42.0.2295.0 (Build of Dev) (32-bit) + 40.0.2214.94 m  

Operating System: Windows 7

**REPRODUCTION CASE**

1. Open Speech.html
2. Make the mic disabled
3. Crash

# **FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**

==1704==ERROR: AddressSanitizer: access-violation on unknown address 0x47d7d7d9 (pc 0x19b45ff3 bp 0x001fad18 sp 0x001fad14 T0)  

#0 0x19b45ff2 in blink::WebSpeechSynthesisVoice::operator blink::PlatformSpeechSynthesisVoice \* C:\b\build\slave\Win\_ASan\_Release\build\src\third\_party\WebKit\Source\platform\  

heap\Handle.h:403  

#1 0x128ce861 in blink::SpeechRecognitionClientProxy::didReceiveError C:\b\build\slave\Win\_ASan\_Release\build\src\third\_party\WebKit\Source\web\SpeechRecognitionClientProxy.cp  

p:130  

#2 0x16711fc3 in content::SpeechRecognitionDispatcher::OnErrorOccurred C:\b\build\slave\Win\_ASan\_Release\build\src\content\renderer\speech\_recognition\_dispatcher.cc:194  

#3 0x16710b3d in content::SpeechRecognitionDispatcher::OnMessageReceived C:\b\build\slave\Win\_ASan\_Release\build\src\base\tuple.h:246  

#4 0x16513716 in content::RenderViewImpl::OnMessageReceived C:\b\build\slave\Win\_ASan\_Release\build\src\content\renderer\render\_view\_impl.cc:1280  

#5 0x184f64d9 in content::MessageRouter::RouteMessage C:\b\build\slave\Win\_ASan\_Release\build\src\content\common\message\_router.cc:54  

#6 0x184f63f6 in content::MessageRouter::OnMessageReceived C:\b\build\slave\Win\_ASan\_Release\build\src\content\common\message\_router.cc:46  

#7 0x163512af in content::ChildThreadImpl::OnMessageReceived C:\b\build\slave\Win\_ASan\_Release\build\src\content\child\child\_thread\_impl.cc:539  

#8 0x18437506 in IPC::ChannelProxy::Context::OnDispatchMessage C:\b\build\slave\Win\_ASan\_Release\build\src\ipc\ipc\_channel\_proxy.cc:282  

#9 0x1697e74b in base::internal::Invoker<2,base::internal::BindState<base::internal::RunnableAdapter<void (\_\_thiscall content::WebRtcLocalAudioRenderer::\*)(media::AudioParamet  

ers const &)>,void \_\_cdecl(content::WebRtcLocalAudioRenderer \*,media::AudioParameters const &),void \_\_cdecl(content::WebRtcLocalAudioRenderer \*,media::AudioParameters)>,void \_\_cde  

cl(content::WebRtcLocalAudioRenderer \*,media::AudioParameters const &)>::Run C:\b\build\slave\Win\_ASan\_Release\build\src\base\bind\_internal.h:185  

#10 0x1033e5a1 in base::debug::TaskAnnotator::RunTask C:\b\build\slave\Win\_ASan\_Release\build\src\base\callback.h:396  

#11 0x16b6dd3c in content::TaskQueueManager::DoWork C:\b\build\slave\Win\_ASan\_Release\build\src\content\renderer\scheduler\task\_queue\_manager.cc:416  

#12 0x17985360 in base::internal::Invoker<2,base::internal::BindState<base::internal::RunnableAdapter<void (\_\_thiscall content::TaskQueueManager::\*)(bool)>,void \_\_cdecl(conten  

t::TaskQueueManager \*,bool),void \_\_cdecl(base::WeakPtr[content::TaskQueueManager](javascript:void(0);),bool)>,void \_\_cdecl(content::TaskQueueManager \*,bool)>::Run C:\b\build\slave\Win\_ASan\_Release\bui  

ld\src\base\bind\_internal.h:185  

#13 0x1033e5a1 in base::debug::TaskAnnotator::RunTask C:\b\build\slave\Win\_ASan\_Release\build\src\base\callback.h:396  

#14 0x102664e8 in base::MessageLoop::RunTask C:\b\build\slave\Win\_ASan\_Release\build\src\base\message\_loop\message\_loop.cc:443  

#15 0x10267c47 in base::MessageLoop::DoWork C:\b\build\slave\Win\_ASan\_Release\build\src\base\message\_loop\message\_loop.cc:453  

#16 0x1033fed2 in base::MessagePumpDefault::Run C:\b\build\slave\Win\_ASan\_Release\build\src\base\message\_loop\message\_pump\_default.cc:32  

#17 0x102652c6 in base::MessageLoop::RunHandler C:\b\build\slave\Win\_ASan\_Release\build\src\base\message\_loop\message\_loop.cc:409  

#18 0x10340b46 in base::RunLoop::Run C:\b\build\slave\Win\_ASan\_Release\build\src\base\run\_loop.cc:55  

#19 0x102647ad in base::MessageLoop::Run C:\b\build\slave\Win\_ASan\_Release\build\src\base\message\_loop\message\_loop.cc:302  

#20 0x16623e14 in content::RendererMain C:\b\build\slave\Win\_ASan\_Release\build\src\content\renderer\renderer\_main.cc:228  

#21 0x10223d87 in content::RunNamedProcessTypeMain C:\b\build\slave\Win\_ASan\_Release\build\src\content\app\content\_main\_runner.cc:423  

#22 0x1022793d in content::ContentMainRunnerImpl::Run C:\b\build\slave\Win\_ASan\_Release\build\src\content\app\content\_main\_runner.cc:803  

#23 0x102236db in content::ContentMain C:\b\build\slave\Win\_ASan\_Release\build\src\content\app\content\_main.cc:19  

#24 0xfe71148 in ChromeMain C:\b\build\slave\Win\_ASan\_Release\build\src\chrome\app\chrome\_main.cc:66  

#25 0xa892f2 in MainDllLoader::Launch C:\b\build\slave\Win\_ASan\_Release\build\src\chrome\app\client\_util.cc:225  

#26 0xa81784 in main C:\b\build\slave\Win\_ASan\_Release\build\src\chrome\app\chrome\_exe\_main\_win.cc:157  

#27 0xc9ab88 in \_\_tmainCRTStartup f:\dd\vctools\crt\crtw32\startup\crt0.c:255  

#28 0x75bb1173 in BaseThreadInitThunk+0x11 (C:\Windows\system32\kernel32.dll+0x51173)  

#29 0x7744b3f4 in RtlInitializeExceptionChain+0x62 (C:\Windows\SYSTEM32\ntdll.dll+0x5b3f4)  

#30 0x7744b3c7 in RtlInitializeExceptionChain+0x35 (C:\Windows\SYSTEM32\ntdll.dll+0x5b3c7)

AddressSanitizer can not provide additional info.  

SUMMARY: AddressSanitizer: SEGV C:\b\build\slave\Win\_ASan\_Release\build\src\third\_party\WebKit\Source\platform\heap\Handle.h:403 blink::WebSpeechSynthesisVoice::operator blink::Pl  

atformSpeechSynthesisVoice \*  

==1704==ABORTING

## Attachments

- [speech.html](attachments/speech.html) (text/html, 239 B)
- [2342911.mp4](attachments/2342911.mp4) (application/octet-stream, 564.8 KB)

## Timeline

### wf...@chromium.org (2015-02-05)

I get an assert on my build with dcheck_always_on=1

Child-SP          RetAddr           Call Site
0000002e`24a4d280 00007ffa`7d9ee364 chrome_child!base::debug::BreakDebugger+0xd [d:\src\gclient\src\base\debug\debugger_win.cc @ 21]
0000002e`24a4d2b0 00007ffa`7f202ac9 chrome_child!logging::LogMessage::~LogMessage+0x224 [d:\src\gclient\src\base\logging.cc @ 642]
0000002e`24a4d760 00007ffa`7f203006 chrome_child!content::SpeechRecognitionDispatcher::GetHandleFromID+0xa9 [d:\src\gclient\src\content\renderer\speech_recognition_dispatcher.cc @ 313]
0000002e`24a4d8a0 00007ffa`7f203327 chrome_child!content::SpeechRecognitionDispatcher::OnErrorOccurred+0x96 [d:\src\gclient\src\content\renderer\speech_recognition_dispatcher.cc @ 197]
(Inline Function) --------`-------- chrome_child!DispatchToMethodImpl+0x11 [d:\src\gclient\src\base\tuple.h @ 246]
(Inline Function) --------`-------- chrome_child!DispatchToMethod+0x11 [d:\src\gclient\src\base\tuple.h @ 253]
(Inline Function) --------`-------- chrome_child!SpeechRecognitionMsg_ErrorOccurred::Dispatch+0x2d [d:\src\gclient\src\content\common\speech_recognition_messages.h @ 109]
0000002e`24a4d8e0 00007ffa`7f1a4497 chrome_child!content::SpeechRecognitionDispatcher::OnMessageReceived+0x2e7 [d:\src\gclient\src\content\renderer\speech_recognition_dispatcher.cc @ 58]
0000002e`24a4da90 00007ffa`7fa6a8cf chrome_child!content::RenderViewImpl::OnMessageReceived+0x217 [d:\src\gclient\src\content\renderer\render_view_impl.cc @ 1280]
0000002e`24a4e230 00007ffa`7f141726 chrome_child!content::MessageRouter::RouteMessage+0x3f [d:\src\gclient\src\content\common\message_router.cc @ 56]
0000002e`24a4e260 00007ffa`7fa41da2 chrome_child!content::ChildThreadImpl::OnMessageReceived+0xd6 [d:\src\gclient\src\content\child\child_thread_impl.cc @ 539]
0000002e`24a4e390 00007ffa`7da2627e chrome_child!IPC::ChannelProxy::Context::OnDispatchMessage+0x1c2 [d:\src\gclient\src\ipc\ipc_channel_proxy.cc @ 283]
(Inline Function) --------`-------- chrome_child!base::Callback<void __cdecl(void)>::Run+0x8 [d:\src\gclient\src\base\callback.h @ 396]
0000002e`24a4e470 00007ffa`7f2fed29 chrome_child!base::debug::TaskAnnotator::RunTask+0x26e [d:\src\gclient\src\base\debug\task_annotator.cc @ 65]
0000002e`24a4e5d0 00007ffa`7f2fe6c0 chrome_child!content::TaskQueueManager::ProcessTaskFromWorkQueue+0x69 [d:\src\gclient\src\content\renderer\scheduler\task_queue_manager.cc @ 419]
0000002e`24a4e650 00007ffa`7f637f95 chrome_child!content::TaskQueueManager::DoWork+0x120 [d:\src\gclient\src\content\renderer\scheduler\task_queue_manager.cc @ 389]
(Inline Function) --------`-------- chrome_child!base::internal::RunnableAdapter<void (__cdecl media::cast::FrameSender::*)(bool)>::Run+0x6 [d:\src\gclient\src\base\bind_internal.h @ 185]
(Inline Function) --------`-------- chrome_child!base::internal::InvokeHelper<1,void,base::internal::RunnableAdapter<void (__cdecl media::cast::FrameSender::*)(bool)>,void __cdecl(base::WeakPtr<media::cast::FrameSender> const &,bool const &)>::MakeItSo+0x2f [d:\src\gclient\src\base\bind_internal.h @ 391]
0000002e`24a4e7b0 00007ffa`7da2627e chrome_child!base::internal::Invoker<2,base::internal::BindState<base::internal::RunnableAdapter<void (__cdecl media::cast::FrameSender::*)(bool) __ptr64>,void __cdecl(media::cast::FrameSender * __ptr64,bool),void __cdecl(base::WeakPtr<media::cast::FrameSender>,bool)>,void __cdecl(media::cast::FrameSender * __ptr64,bool)>::Run+0x45 [d:\src\gclient\src\base\bind_internal.h @ 563]
(Inline Function) --------`-------- chrome_child!base::Callback<void __cdecl(void)>::Run+0x8 [d:\src\gclient\src\base\callback.h @ 396]
0000002e`24a4e7e0 00007ffa`7d9f49ea chrome_child!base::debug::TaskAnnotator::RunTask+0x26e [d:\src\gclient\src\base\debug\task_annotator.cc @ 65]
0000002e`24a4e940 00007ffa`7d9f3885 chrome_child!base::MessageLoop::RunTask+0x23a [d:\src\gclient\src\base\message_loop\message_loop.cc @ 446]
(Inline Function) --------`-------- chrome_child!base::MessageLoop::DeferOrRunPendingTask+0x48 [d:\src\gclient\src\base\message_loop\message_loop.cc @ 453]
0000002e`24a4eab0 00007ffa`7da286e8 chrome_child!base::MessageLoop::DoWork+0x3e5 [d:\src\gclient\src\base\message_loop\message_loop.cc @ 566]
0000002e`24a4eb60 00007ffa`7da2960e chrome_child!base::MessagePumpDefault::Run+0x128 [d:\src\gclient\src\base\message_loop\message_pump_default.cc @ 32]
0000002e`24a4ecb0 00007ffa`7d9f4688 chrome_child!base::RunLoop::Run+0x2e [d:\src\gclient\src\base\run_loop.cc @ 56]
0000002e`24a4ed10 00007ffa`7f1d800e chrome_child!base::MessageLoop::Run+0x18 [d:\src\gclient\src\base\message_loop\message_loop.cc @ 303]
0000002e`24a4ed70 00007ffa`7d9b4c16 chrome_child!content::RendererMain+0x56e [d:\src\gclient\src\content\renderer\renderer_main.cc @ 229]
0000002e`24a4f090 00007ffa`7d9b4ad6 chrome_child!content::RunNamedProcessTypeMain+0xf6 [d:\src\gclient\src\content\app\content_main_runner.cc @ 423]
0000002e`24a4f1f0 00007ffa`7d9b1740 chrome_child!content::ContentMainRunnerImpl::Run+0x166 [d:\src\gclient\src\content\app\content_main_runner.cc @ 803]
0000002e`24a4f390 00007ffa`7d8ef1d5 chrome_child!content::ContentMain+0x30 [d:\src\gclient\src\content\app\content_main.cc @ 21]
0000002e`24a4f3c0 00007ff6`88679831 chrome_child!ChromeMain+0x85 [d:\src\gclient\src\chrome\app\chrome_main.cc @ 69]
0000002e`24a4f450 00007ff6`88674ebe chrome!MainDllLoader::Launch+0x401 [d:\src\gclient\src\chrome\app\client_util.cc @ 228]
0000002e`24a4f580 00007ff6`886d7ee0 chrome!wWinMain+0xfe [d:\src\gclient\src\chrome\app\chrome_exe_main_win.cc @ 158]
0000002e`24a4f730 00007ffa`b78b13d2 chrome!__tmainCRTStartup+0x148 [f:\dd\vctools\crt\crtw32\startup\crt0.c @ 251]
0000002e`24a4f770 00007ffa`b87103c4 KERNEL32!BaseThreadInitThunk+0x22
0000002e`24a4f7a0 00000000`00000000 ntdll!RtlUserThreadStart+0x34

const WebSpeechRecognitionHandle& SpeechRecognitionDispatcher::GetHandleFromID(
    int request_id) {
  HandleMap::iterator iter = handle_map_.find(request_id);
  DCHECK(iter != handle_map_.end()); <-- DCHECK fails
  return iter->second;
}

I'll also try with a normal release build.

### cl...@chromium.org (2015-02-05)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=6746181265784832

### wf...@chromium.org (2015-02-05)

I get an access violation on Canary 42.0.2295.0

0:011> g
(15f4.3328): Access violation - code c0000005 (first chance)
First chance exceptions are reported before any exception handling.
This exception may be expected and handled.
chrome_child!blink::Persistent<blink::DOMError,blink::ThreadLocalPersistents<0> >::get [inlined in chrome_child!blink::WebIDBDatabaseError::operator blink::DOMError * __ptr64+0xa]:
00007ffa`8983b442 488b4220        mov     rax,qword ptr [rdx+20h] ds:00000000`0000002f=????????????????
0:000> k
Child-SP          RetAddr           Call Site
(Inline Function) --------`-------- chrome_child!blink::Persistent<blink::DOMError,blink::ThreadLocalPersistents<0> >::get [c:\b\build\slave\win64\build\src\third_party\webkit\source\platform\heap\handle.h @ 403]
(Inline Function) --------`-------- chrome_child!blink::PtrStorageImpl<blink::DOMError,1>::get+0xa [c:\b\build\slave\win64\build\src\third_party\webkit\public\platform\webprivateptr.h @ 116]
(Inline Function) --------`-------- chrome_child!blink::WebPrivatePtr<blink::DOMError>::get+0xa [c:\b\build\slave\win64\build\src\third_party\webkit\public\platform\webprivateptr.h @ 233]
000000bc`2e6cccf8 00007ffa`88e33115 chrome_child!blink::WebIDBDatabaseError::operator blink::DOMError * __ptr64+0xa [c:\b\build\slave\win64\build\src\third_party\webkit\source\web\webidbdatabaseerror.cpp @ 61]
000000bc`2e6ccd00 00007ffa`890a0a2c chrome_child!blink::SpeechRecognitionClientProxy::didReceiveError+0x1d [c:\b\build\slave\win64\build\src\third_party\webkit\source\web\speechrecognitionclientproxy.cpp @ 132]
000000bc`2e6ccd40 00007ffa`890a0dfb chrome_child!content::SpeechRecognitionDispatcher::OnErrorOccurred+0xd0 [c:\b\build\slave\win64\build\src\content\renderer\speech_recognition_dispatcher.cc @ 197]
(Inline Function) --------`-------- chrome_child!DispatchToMethodImpl+0x11 [c:\b\build\slave\win64\build\src\base\tuple.h @ 246]
(Inline Function) --------`-------- chrome_child!DispatchToMethod+0x11 [c:\b\build\slave\win64\build\src\base\tuple.h @ 253]
(Inline Function) --------`-------- chrome_child!SpeechRecognitionMsg_ErrorOccurred::Dispatch+0x30 [c:\b\build\slave\win64\build\src\content\common\speech_recognition_messages.h @ 109]
000000bc`2e6ccd70 00007ffa`8905779e chrome_child!content::SpeechRecognitionDispatcher::OnMessageReceived+0x3af [c:\b\build\slave\win64\build\src\content\renderer\speech_recognition_dispatcher.cc @ 55]
000000bc`2e6ccf10 00007ffa`89528983 chrome_child!content::RenderViewImpl::OnMessageReceived+0xfa [c:\b\build\slave\win64\build\src\content\renderer\render_view_impl.cc @ 1280]
000000bc`2e6cd700 00007ffa`89008ad9 chrome_child!content::MessageRouter::RouteMessage+0x4f [c:\b\build\slave\win64\build\src\content\common\message_router.cc @ 55]
000000bc`2e6cd730 00007ffa`89509d10 chrome_child!content::ChildThreadImpl::OnMessageReceived+0xc9 [c:\b\build\slave\win64\build\src\content\child\child_thread_impl.cc @ 539]
000000bc`2e6cd850 00007ffa`87c0a7b6 chrome_child!IPC::ChannelProxy::Context::OnDispatchMessage+0x128 [c:\b\build\slave\win64\build\src\ipc\ipc_channel_proxy.cc @ 283]
(Inline Function) --------`-------- chrome_child!base::Callback<void __cdecl(void)>::Run+0xa [c:\b\build\slave\win64\build\src\base\callback.h @ 396]
000000bc`2e6cd930 00007ffa`891563b5 chrome_child!base::debug::TaskAnnotator::RunTask+0x416 [c:\b\build\slave\win64\build\src\base\debug\task_annotator.cc @ 65]
000000bc`2e6cdac0 00007ffa`89155f08 chrome_child!content::TaskQueueManager::ProcessTaskFromWorkQueue+0x55 [c:\b\build\slave\win64\build\src\content\renderer\scheduler\task_queue_manager.cc @ 419]
000000bc`2e6cdb40 00007ffa`891565cd chrome_child!content::TaskQueueManager::DoWork+0x80 [c:\b\build\slave\win64\build\src\content\renderer\scheduler\task_queue_manager.cc @ 389]
(Inline Function) --------`-------- chrome_child!base::internal::RunnableAdapter<void (__cdecl content::TaskQueueManager::*)(bool)>::Run+0x8 [c:\b\build\slave\win64\build\src\base\bind_internal.h @ 185]
(Inline Function) --------`-------- chrome_child!base::internal::InvokeHelper<1,void,base::internal::RunnableAdapter<void (__cdecl content::TaskQueueManager::*)(bool)>,void __cdecl(base::WeakPtr<content::TaskQueueManager> const &,bool const &)>::MakeItSo+0x36 [c:\b\build\slave\win64\build\src\base\bind_internal.h @ 391]
000000bc`2e6cdb80 00007ffa`87c0a7b6 chrome_child!base::internal::Invoker<2,base::internal::BindState<base::internal::RunnableAdapter<void (__cdecl content::TaskQueueManager::*)(bool) __ptr64>,void __cdecl(content::TaskQueueManager * __ptr64,bool),void __cdecl(base::WeakPtr<content::TaskQueueManager>,bool)>,void __cdecl(content::TaskQueueManager * __ptr64,bool)>::Run+0x51 [c:\b\build\slave\win64\build\src\base\bind_internal.h @ 563]
(Inline Function) --------`-------- chrome_child!base::Callback<void __cdecl(void)>::Run+0xa [c:\b\build\slave\win64\build\src\base\callback.h @ 396]
000000bc`2e6cdbb0 00007ffa`87bd0377 chrome_child!base::debug::TaskAnnotator::RunTask+0x416 [c:\b\build\slave\win64\build\src\base\debug\task_annotator.cc @ 65]
000000bc`2e6cdd40 00007ffa`87bd0b1a chrome_child!base::MessageLoop::RunTask+0x2c7 [c:\b\build\slave\win64\build\src\base\message_loop\message_loop.cc @ 446]
(Inline Function) --------`-------- chrome_child!base::MessageLoop::DeferOrRunPendingTask+0xac [c:\b\build\slave\win64\build\src\base\message_loop\message_loop.cc @ 453]
000000bc`2e6cf070 00007ffa`87c06b6e chrome_child!base::MessageLoop::DoWork+0x23a [c:\b\build\slave\win64\build\src\base\message_loop\message_loop.cc @ 566]
000000bc`2e6cf120 00007ffa`87bcff8a chrome_child!base::MessagePumpDefault::Run+0x13e [c:\b\build\slave\win64\build\src\base\message_loop\message_pump_default.cc @ 32]
000000bc`2e6cf290 00007ffa`87c07f34 chrome_child!base::MessageLoop::RunHandler+0xda [c:\b\build\slave\win64\build\src\base\message_loop\message_loop.cc @ 410]
000000bc`2e6cf300 00007ffa`87bcfae2 chrome_child!base::RunLoop::Run+0xf4 [c:\b\build\slave\win64\build\src\base\run_loop.cc @ 56]
000000bc`2e6cf350 00007ffa`8907ee99 chrome_child!base::MessageLoop::Run+0x42 [c:\b\build\slave\win64\build\src\base\message_loop\message_loop.cc @ 303]
000000bc`2e6cf3b0 00007ffa`88abed36 chrome_child!content::RendererMain+0x5c5 [c:\b\build\slave\win64\build\src\content\renderer\renderer_main.cc @ 229]
000000bc`2e6cf6c0 00007ffa`88abec47 chrome_child!content::RunNamedProcessTypeMain+0xb6 [c:\b\build\slave\win64\build\src\content\app\content_main_runner.cc @ 440]
000000bc`2e6cf710 00007ffa`88abbcf8 chrome_child!content::ContentMainRunnerImpl::Run+0xb7 [c:\b\build\slave\win64\build\src\content\app\content_main_runner.cc @ 803]
000000bc`2e6cf7b0 00007ffa`88a2885e chrome_child!content::ContentMain+0x30 [c:\b\build\slave\win64\build\src\content\app\content_main.cc @ 21]
000000bc`2e6cf7e0 00007ff6`ef09fcb0 chrome_child!ChromeMain+0x82 [c:\b\build\slave\win64\build\src\chrome\app\chrome_main.cc @ 69]
000000bc`2e6cf870 00007ff6`ef09f1a2 chrome!MainDllLoader::Launch+0x380 [c:\b\build\slave\win64\build\src\chrome\app\client_util.cc @ 226]
000000bc`2e6cf9a0 00007ff6`ef0c8fa4 chrome!wWinMain+0xde [c:\b\build\slave\win64\build\src\chrome\app\chrome_exe_main_win.cc @ 158]
000000bc`2e6cfb50 00007ffa`b78b13d2 chrome!__tmainCRTStartup+0x148 [f:\dd\vctools\crt\crtw32\startup\crt0.c @ 251]
000000bc`2e6cfb90 00007ffa`b87103c4 KERNEL32!BaseThreadInitThunk+0x22
000000bc`2e6cfbc0 00000000`00000000 ntdll!RtlUserThreadStart+0x34

clusterfuzz will do the bisect.


### cl...@chromium.org (2015-02-05)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6746181265784832

Uploader: wfh@chromium.org
Job Type: Windows_asan_chrome

Crash Type: UNKNOWN
Crash Address: 0xbebebece
Crash State:
  blink::WebSpeechSynthesisVoice::operator
  blink::SpeechRecognitionClientProxy::didReceiveError
  content::SpeechRecognitionDispatcher::OnErrorOccurred
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=windows_asan_chrome&range=314607:314621

Minimized Testcase (0.23 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv97CKLsvWu3P1OzivZDOFpiC4mVGIRJN2bodb3ZcFdUI5XdCuU9pN9cMhwqYrqQpA_3hiRaqKN9e_o8XWnI6hyeTisW7BteoxJV8GSn17UKPbmJVPHH6S8wj7eY30oyhLnopHUJBEFCXWjpeZ3YO32snx9EwqQ
<script>
 var recognition = new webkitSpeechRecognition();
  recognition.onend = function() {
    recognition.start();
    recognition.stop();
  };
  recognition.start();
  setTimeout(function(){recognition.stop();}, 200)
</script>




### cl...@chromium.org (2015-02-05)

[Empty comment from Monorail migration]

### ch...@gmail.com (2015-02-05)

I tested on stable 40.0.2214.94 m 
eax=5a488240 ebx=0018ec14 ecx=86024bd7 edx=0018ebc8 esi=86024bd7 edi=00c8f870
eip=5fbdc355 esp=0018ebb4 ebp=0018ebc0 iopl=0         nv up ei ng nz na pe nc
cs=001b  ss=0023  ds=0023  es=0023  fs=003b  gs=0000             efl=00010286
chrome_child!blink::EventTarget::dispatchEvent+0xc:
5fbdc355 8b06            mov     eax,dword ptr [esi]  ds:0023:86024bd7=????????
0:000> k
  *** Stack trace for last set context - .thread/.cxr resets it
ChildEBP RetAddr  
0018ebc0 60aa452b chrome_child!blink::EventTarget::dispatchEvent+0xc [c:\b\build\slave\win\build\src\third_party\webkit\source\core\events\eventtarget.cpp @ 195]
0018ebd0 60a4c345 chrome_child!blink::SpeechRecognition::didReceiveError+0x1a [c:\b\build\slave\win\build\src\third_party\webkit\source\modules\speech\speechrecognition.cpp @ 132]
0018ebe0 60badeda chrome_child!blink::SpeechRecognitionClientProxy::didReceiveError+0x34 [c:\b\build\slave\win\build\src\third_party\webkit\source\web\speechrecognitionclientproxy.cpp @ 132]
0018ec00 60bad861 chrome_child!content::SpeechRecognitionDispatcher::OnErrorOccurred+0x64 [c:\b\build\slave\win\build\src\content\renderer\speech_recognition_dispatcher.cc @ 197]
0018ec1c 5fbe0ac7 chrome_child!SpeechRecognitionMsg_ErrorOccurred::Dispatch<content::SpeechRecognitionDispatcher,content::SpeechRecognitionDispatcher,void,void (__thiscall content::SpeechRecognitionDispatcher::*)(int,content::SpeechRecognitionError const &)>+0x30 [c:\b\build\slave\win\build\src\content\common\speech_recognition_messages.h @ 109]
0018ecf0 5fbdf66d chrome_child!content::SpeechRecognitionDispatcher::OnMessageReceived+0x1a2 [c:\b\build\slave\win\build\src\content\renderer\speech_recognition_dispatcher.cc @ 55]
0018f108 5fb84730 chrome_child!content::RenderViewImpl::OnMessageReceived+0xc0 [c:\b\build\slave\win\build\src\content\renderer\render_view_impl.cc @ 1310]
0018f118 5fb84708 chrome_child!content::MessageRouter::RouteMessage+0x24 [c:\b\build\slave\win\build\src\content\common\message_router.cc @ 55]
0018f124 5faf925b chrome_child!content::MessageRouter::OnMessageReceived+0x1d [c:\b\build\slave\win\build\src\content\common\message_router.cc @ 47]
0018f1b0 5faf9197 chrome_child!content::ChildThread::OnMessageReceived+0xa4 [c:\b\build\slave\win\build\src\content\child\child_thread.cc @ 502]
0018f1e4 5faf90fc chrome_child!IPC::ChannelProxy::Context::OnDispatchMessage+0x98 [c:\b\build\slave\win\build\src\ipc\ipc_channel_proxy.cc @ 275]
0018f1f4 5faf8240 chrome_child!base::internal::Invoker<2,base::internal::BindState<base::internal::RunnableAdapter<void (__thiscall content::RtcDtmfSenderHandler::Observer::*)(std::basic_string<char,std::char_traits<char>,std::allocator<char> > const &)>,void __cdecl(content::RtcDtmfSenderHandler::Observer *,std::basic_string<char,std::char_traits<char>,std::allocator<char> > const &),void __cdecl(content::RtcDtmfSenderHandler::Observer *,std::basic_string<char,std::char_traits<char>,std::allocator<char> >)>,void __cdecl(content::RtcDtmfSenderHandler::Observer *,std::basic_string<char,std::char_traits<char>,std::allocator<char> > const &)>::Run+0x16 [c:\b\build\slave\win\build\src\base\bind_internal.h @ 1253]
0018f2a4 5faf7bfe chrome_child!base::debug::TaskAnnotator::RunTask+0x39c [c:\b\build\slave\win\build\src\base\debug\task_annotator.cc @ 63]
0018f2dc 5faf7a89 chrome_child!base::MessageLoop::RunTask+0xe4 [c:\b\build\slave\win\build\src\base\message_loop\message_loop.cc @ 449]
0018f420 5faf9941 chrome_child!base::MessageLoop::DoWork+0x375 [c:\b\build\slave\win\build\src\base\message_loop\message_loop.cc @ 566]
0018f44c 5faf7663 chrome_child!base::MessagePumpDefault::Run+0xc8 [c:\b\build\slave\win\build\src\base\message_loop\message_pump_default.cc @ 33]
0018f470 5faf756b chrome_child!base::MessageLoop::RunHandler+0x65 [c:\b\build\slave\win\build\src\base\message_loop\message_loop.cc @ 416]
0018f498 5faf8b72 chrome_child!base::RunLoop::Run+0x88 [c:\b\build\slave\win\build\src\base\run_loop.cc @ 56]
0018f4bc 5fb5a2b0 chrome_child!base::MessageLoop::Run+0x46 [c:\b\build\slave\win\build\src\base\message_loop\message_loop.cc @ 309]
0018f744 5faf0692 chrome_child!content::RendererMain+0x292 [c:\b\build\slave\win\build\src\content\renderer\renderer_main.cc @ 235]


### wf...@chromium.org (2015-02-05)

clusterfuzz appears to be having issues bisecting this so I'll do a manual bisect

### wf...@chromium.org (2015-02-05)

I biesect this all the way back to the original speech enable in 14f843ea9e67bea9a8d05403cd73ae82879e4138 so this certainly affects stable :)

### js...@chromium.org (2015-02-06)

Seems to trigger as long as a mic isn't enabled, so I'll leave it at high.

tommi@ - Can you help find an owner for this?

### cl...@chromium.org (2015-02-07)

[Empty comment from Monorail migration]

### to...@chromium.org (2015-02-07)

Dominic - can you take a look?

### cl...@chromium.org (2015-02-20)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-02-21)

dmazzoni@: Uh oh! This issue is still open and hasn't been updated in the last 14 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2015-03-10)

dmazzoni@: Uh oh! This issue is still open and hasn't been updated in the last 31 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### ch...@gmail.com (2015-03-11)

dmazzoni, Could you please take a look at this when you get a chance?

### cl...@chromium.org (2015-03-23)

ClusterFuzz has detected this issue as fixed in range 0:320722.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6746181265784832

Uploader: wfh@chromium.org
Job Type: Windows_asan_chrome

Crash Type: UNKNOWN
Crash Address: 0xbebebece
Crash State:
  blink::WebSpeechSynthesisVoice::operator
  blink::SpeechRecognitionClientProxy::didReceiveError
  content::SpeechRecognitionDispatcher::OnErrorOccurred
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=windows_asan_chrome&range=314607:314621
Fixed: https://cluster-fuzz.appspot.com/revisions?job=windows_asan_chrome&range=0:320722

Minimized Testcase (0.23 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv97CKLsvWu3P1OzivZDOFpiC4mVGIRJN2bodb3ZcFdUI5XdCuU9pN9cMhwqYrqQpA_3hiRaqKN9e_o8XWnI6hyeTisW7BteoxJV8GSn17UKPbmJVPHH6S8wj7eY30oyhLnopHUJBEFCXWjpeZ3YO32snx9EwqQ
<script>
 var recognition = new webkitSpeechRecognition();
  recognition.onend = function() {
    recognition.start();
    recognition.stop();
  };
  recognition.start();
  setTimeout(function(){recognition.stop();}, 200)
</script>

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### cl...@chromium.org (2015-03-27)

dmazzoni@: Uh oh! This issue is still open and hasn't been updated in the last 48 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### in...@chromium.org (2015-04-01)

This is not fixed, another testcase coming.

### cl...@chromium.org (2015-04-01)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5329490335498240

Fuzzer: Inferno_layout_test_unmodified
Job Type: Windows_asan_chrome

Crash Type: UNKNOWN
Crash Address: 0xbebebece
Crash State:
  blink::WebSpeechSynthesisVoice::operator
  blink::SpeechRecognitionClientProxy::didReceiveError
  content::SpeechRecognitionDispatcher::OnErrorOccurred
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=windows_asan_chrome&range=322945:322984

Minimized Testcase (0.33 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95BnLI5sDYIv1TFg_wl2kG7s87WUBkztlH28_KwKDBrQ47Xts9ggTHNNwmaA2bLpzHvLvpGwIgWnWfcNffyyP6fts8odguZYk2pVqKnOXzIkWhreO_MGkxNdoQRV8-yMHOS7VFl5tWXbZMMl31yw2Z9UDkj0A

Filer: inferno

### cl...@chromium.org (2015-04-03)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-04-08)

You have far exceeded the 60-day deadline for fixing this high severity security vulnerability.

We commit ourselves to this deadline and appreciate your utmost priority on this issue.

If you are unable to look into this soon, please find someone else to own this.

- Your friendly ClusterFuzz

### ch...@gmail.com (2015-04-09)

dmazzoni@: Any updates on this bug?

### ch...@gmail.com (2015-04-14)

dmazzoni@ - Could you please take a look at this high severity security bug as soon as possible.

### dm...@chromium.org (2015-04-15)

I think WebSpeechSynthesisVoice in the stack trace is a red herring; the original error and the minimized test case all involve only speech recognition code.

@hans, could you take a look?


### ha...@chromium.org (2015-04-15)

tommi: Is there anyone working on speech recognition these days?

### to...@chromium.org (2015-04-16)

hey Hans - I just got back.  Unfortunately everyone on the team that would know this (or even blink), are out at the moment :(  I don't suppose you have some bandwidth to work on this?

### ch...@gmail.com (2015-04-24)

Hans@: This bug is still open and hasn't been updated, since this is a high security vulnerability. Could you please fix this this one as soon as possible? 

### ha...@chromium.org (2015-04-24)

I haven't been able to reproduce this.

Using an ASan build on Windows and the repro from #19, I've tried both with mic available and not available, allowing or denying permission to the mic, and leaving it running for a couple of minutes. Has anyone on this thread been able to reproduce this manually?

I should also point out that I'm not a good owner for this bug since I haven't worked on anything media-related for years. It's really tommi that owns this, but I agreed to take a look.

### ha...@chromium.org (2015-04-24)

From #1:
> const WebSpeechRecognitionHandle& SpeechRecognitionDispatcher::GetHandleFromID(
>     int request_id) {
>   HandleMap::iterator iter = handle_map_.find(request_id);
>   DCHECK(iter != handle_map_.end()); <-- DCHECK fails
>   return iter->second;
> }

If this is indeed something that's happening in the wild, a stop-gap measure could be to bail out from didReceiveError et al. if there is no entry for the request_id in handle_map_.

### ch...@gmail.com (2015-04-24)

I'm still able to reproduce this manually as long as a mic isn't enabled.

### ha...@chromium.org (2015-04-24)

> I'm still able to reproduce this manually as long as a mic isn't enabled.

Can you clarify what you mean by mic isn't enabled? Do you mean that you deny the page access to it, or that the system doesn't have a mic?

How are you accessing the html file (http, https, or file://)?

### ch...@gmail.com (2015-04-24)

> Can you clarify what you mean by mic isn't enabled? Do you mean that you deny the page access to it, or that the system doesn't have a mic?

I don't allow the mic. I have recorded a video to see how I accessing the html file.

### ch...@gmail.com (2015-04-24)

If you using an ASAN build on Windows, is better to accessing the html file as file://..../testcase.html 

### ha...@chromium.org (2015-04-24)

Thanks for the video, that's very helpful. I still can't get this to reproduce, though :-/

wfh, does this still reproduce for you?

tommi: What do you think about just sticking "if (handle_map_.find(request_id) == handle_map_.end()) dcheck && return" in OnErrorOccurred (and possibly some others)? It's not ideal obviously, but should make the code more robust against whatever is causing this problem.

### ha...@chromium.org (2015-05-05)

-> tommi. I'm not currently looking at this.

### cl...@chromium.org (2015-05-15)

[Empty comment from Monorail migration]

### wf...@chromium.org (2015-05-18)

yes I can still repro

all the methods on SpeechRecognitionClientProxy do dereference the handle so we'd have to sprinkle a lot of checks here - isn't it possible to work out why the renderer is being sent an id of an invalid handle - perhaps some inconsistent state between browser and renderer is going on?

### wf...@chromium.org (2015-05-18)

I think this is specifically related to SPEECH_RECOGNITION_ERROR_NOT_ALLOWED error when access is denied then something is going awry.


### wf...@chromium.org (2015-05-18)

the spec says:

https://dvcs.w3.org/hg/speech-api/raw-file/tip/speechapi.html#dfn-utteranceonend

end event - Fired when this utterance has completed being spoken. If this event fires, the error event must not be fired for this utterance.

it seems like from within the onend it shouldn't be firing an onerror - which is what is happening here, maybe we need some metadata in the browser to track that onend is being called and not to fire onerror?

### wf...@chromium.org (2015-05-19)

is there anyone else I can add to this bug to make headway?

### in...@chromium.org (2015-05-19)

primiano@, tommi@, can you please take a look. Please note that this is high severity security bug that needs to be fixed this week as part of security fixit.

### pr...@chromium.org (2015-05-20)

As discussed offline, I am not working on this anymore and unfortunately don't have any spare bandwidth to look at this.

### wf...@chromium.org (2015-05-20)

This will now crash since the code that references the removed handle has been replaced with a CHECK - so while the security issue is gone, the underlying bug is still present - primiano when will you likely have time to look at this?

### cr...@chromium.org (2015-05-20)

primiano@ said he's not working on this anymore in https://crbug.com/chromium/455735#c42.  tommi@, can you resolve the CHECK failures?

### cl...@chromium.org (2015-05-20)

ClusterFuzz has detected this issue as potentially fixed, but it appears to be flaky.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5329490335498240

Fuzzer: Inferno_layout_test_unmodified
Job Type: Windows_asan_chrome

Crash Type: UNKNOWN
Crash Address: 0xbebebece
Crash State:
  blink::WebSpeechSynthesisVoice::operator
  blink::SpeechRecognitionClientProxy::didReceiveError
  content::SpeechRecognitionDispatcher::OnErrorOccurred
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=windows_asan_chrome&range=322945:322984

Minimized Testcase (0.33 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95BnLI5sDYIv1TFg_wl2kG7s87WUBkztlH28_KwKDBrQ47Xts9ggTHNNwmaA2bLpzHvLvpGwIgWnWfcNffyyP6fts8odguZYk2pVqKnOXzIkWhreO_MGkxNdoQRV8-yMHOS7VFl5tWXbZMMl31yw2Z9UDkj0A

If you suspect that the result above is incorrect,try re-doing that job on the test case report page.

### wf...@chromium.org (2015-05-21)

The fix to https://crbug.com/chromium/470777 has fixed this security issue, so I've raised a feature https://crbug.com/chromium/490487 to track fixing the issue that now causes as CHECK, and mark this security bug fixed.

### cl...@chromium.org (2015-05-21)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### ti...@google.com (2015-07-08)

From reading this bug, it looks like a merge isn't required here. Please update if that understanding is incorrect.

### ch...@gmail.com (2015-07-08)

Tim - Is this report qualified for a chromium security reward?


### ti...@google.com (2015-07-08)

Always happy to take your reports to the panel! :)

### cl...@chromium.org (2015-08-27)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2015-08-31)

[Empty comment from Monorail migration]

### ti...@google.com (2015-10-09)

Congrats - $2000 for this report. I'll start payment next week, so you should have the cash ~2 weeks from today.

Thanks!

### ti...@google.com (2015-10-16)

[Empty comment from Monorail migration]

### ti...@google.com (2015-10-29)

Payment is on its way - should arrive in ~7 days. Thanks again for your report!

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/455735?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081337)*
