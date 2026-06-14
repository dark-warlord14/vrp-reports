# Heap-use-after-free in v8::internal::JSObject::GetElementWithInterceptor

| Field | Value |
|-------|-------|
| **Issue ID** | [40055123](https://issues.chromium.org/issues/40055123) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink, Blink>JavaScript |
| **Reporter** | ax...@gmail.com |
| **Assignee** | ar...@chromium.org |
| **Created** | 2012-03-16 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

Usea-after-free in JavaScript engine.

**VERSION**  

Version 19.0.1068.0 (126348), Developer Build on Ubuntu 10.10

**REPRODUCTION CASE**  

Unfortunately can't provide testcase currently - this is one of those rare cases, when reproduction does not works. Decided to provide at least stack trace, probably it can be useful. This bug appears quite frequently, so, probably later I will get finally the testcase.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

==5320== ERROR: AddressSanitizer heap-use-after-free on address 0x7ffbb6a02888 at pc 0x7ffbdcb07aa9 bp 0x7fff610c4cb0 sp 0x7fff610c4ca8  

READ of size 8 at 0x7ffbb6a02888 thread T0  

#0 0x7ffbdcb07aa9 in WebCore::toV8(WebCore::CSSStyleSheet\*) ???:0  

#1 0x7ffbd77a348e in v8::internal::JSObject::GetElementWithInterceptor(v8::internal::Object\*, unsigned int) /media/Chromium/chromium/depot\_tools/src/v8/src/objects.cc:10097  

#2 0x7ffbd78fe004 in v8::internal::Runtime::GetObjectProperty(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);)) /media/Chromium/chromium/depot\_tools/src/v8/src/runtime.cc:4182  

#3 0x7ffbd7be13fc in v8::internal::KeyedLoadIC::Load(v8::internal::InlineCacheState, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), bool) /media/Chromium/chromium/depot\_tools/src/v8/src/ic.cc:1195  

#4 0x7ffbd7beccd5 in v8::internal::KeyedLoadIC\_Miss(v8::internal::Arguments, v8::internal::Isolate\*) /media/Chromium/chromium/depot\_tools/src/v8/src/ic.cc:1987  

#5 0x2ef9fe00614e  

#6 0x2ef9fe0ca0e0  

#7 0x2ef9fe0c6822  

#8 0x2ef9fe0e89ed  

#9 0x2ef9fe06e4b3  

#10 0x2ef9fe022647  

#11 0x2ef9fe011137  

#12 0x7ffbd74e3278 in v8::internal::Invoke(bool, v8::internal::Handle[v8::internal::JSFunction](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*, bool\*) /media/Chromium/chromium/depot\_tools/src/v8/src/execution.cc:118  

#13 0x7ffbd742d586 in v8::Script::Run() /media/Chromium/chromium/depot\_tools/src/v8/src/api.cc:1588  

#14 0x7ffbd9152a03 in WebCore::V8Proxy::runScript(v8::Handle[v8::Script](javascript:void(0);)) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/bindings/v8/V8Proxy.cpp:382  

#15 0x7ffbd9151bab in WebCore::V8Proxy::evaluate(WebCore::ScriptSourceCode const&, WebCore::Node\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/bindings/v8/V8Proxy.cpp:353  

#16 0x7ffbd997eda7 in ~Scope /media/Chromium/chromium/depot\_tools/src/v8/include/v8.h:3577  

#17 0x7ffbd97b8c64 in WebCore::InspectorInstrumentation::hasFrontends() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/inspector/InspectorInstrumentation.h:225  

#18 0x7ffbd8dc85d8 in WebCore::ThreadTimers::sharedTimerFiredInternal() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/platform/ThreadTimers.cpp:118  

#19 0x7ffbd69f1256 in base::Callback<void ()()>::Run() const /media/Chromium/chromium/depot\_tools/src/./base/callback.h:272  

#20 0x7ffbd69f1ab8 in MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:470  

#21 0x7ffbd69f3498 in MessageLoop::DoDelayedWork(base::TimeTicks\*) /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:698  

#22 0x7ffbd69fd2ce in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) /media/Chromium/chromium/depot\_tools/src/base/message\_pump\_default.cc:33  

#23 0x7ffbd69efe1e in MessageLoop::RunInternal() /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:418  

#24 0x7ffbd69ee00f in ~AutoRunState /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:745  

#25 0x7ffbdbdc9b5c in RendererMain(content::MainFunctionParams const&) /media/Chromium/chromium/depot\_tools/src/content/renderer/renderer\_main.cc:241  

#26 0x7ffbd69464b6 in RunZygote /media/Chromium/chromium/depot\_tools/src/content/app/content\_main\_runner.cc:245  

#27 0x7ffbd6944a2a in content::ContentMain(int, char const\*\*, content::ContentMainDelegate\*) /media/Chromium/chromium/depot\_tools/src/content/app/content\_main.cc:35  

#28 0x7ffbd53abc97 in ChromeMain /media/Chromium/chromium/depot\_tools/src/chrome/app/chrome\_main.cc:32  

#29 0x7ffbd53abbeb in main /media/Chromium/chromium/depot\_tools/src/chrome/app/chrome\_exe\_main\_gtk.cc:18  

#30 0x7ffbce7bbd8e in \_\_libc\_start\_main /build/buildd/eglibc-2.12.1/csu/libc-start.c:258  

0x7ffbb6a02888 is located 8 bytes inside of 136-byte region [0x7ffbb6a02880,0x7ffbb6a02908)  

freed by thread T0 here:  

#0 0x7ffbdd14b9d2 in operator delete(void\*) ??:0  

#1 0x7ffbd753eb39 in v8::internal::RuntimeProfiler::IsEnabled() /media/Chromium/chromium/depot\_tools/src/v8/src/runtime-profiler.h:50  

previously allocated by thread T0 here:  

#0 0x7ffbdd14b852 in operator new(unsigned long) ??:0  

#1 0x7ffbd8b88258 in WebCore::HTMLStyleElement::create(WebCore::QualifiedName const&, WebCore::Document\*, bool) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/html/HTMLStyleElement.cpp:70  

#2 0x7ffbda6cd5aa in WTF::PassRefPtr[WebCore::HTMLStyleElement](javascript:void(0);)::leakRef() const /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/JavaScriptCore/wtf/PassRefPtr.h:161  

#3 0x7ffbda6c4c63 in WTF::PassRefPtr[WebCore::HTMLElement](javascript:void(0);)::operator WebCore::HTMLElement\* WTF::PassRefPtr[WebCore::HTMLElement](javascript:void(0);)::\*() const /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/JavaScriptCore/wtf/PassRefPtr.h:82  

#4 0x7ffbd8acd759 in WTF::PassRefPtr[WebCore::HTMLElement](javascript:void(0);)::leakRef() const /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/JavaScriptCore/wtf/PassRefPtr.h:161  

#5 0x7ffbda57ff00 in WTF::PassRefPtr[WebCore::Element](javascript:void(0);)::leakRef() const /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/JavaScriptCore/wtf/PassRefPtr.h:161  

#6 0x7ffbd7494da3 in HandleApiCallHelper /media/Chromium/chromium/depot\_tools/src/v8/src/builtins.cc:1136  

#7 0x2ef9fe00614e  

#8 0x2ef9fe0ca1aa  

#9 0x2ef9fe0c6822  

#10 0x2ef9fe0e89ed  

#11 0x2ef9fe06e4b3  

#12 0x2ef9fe022647  

#13 0x2ef9fe011137  

#14 0x7ffbd74e3278 in v8::internal::Invoke(bool, v8::internal::Handle[v8::internal::JSFunction](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*, bool\*) /media/Chromium/chromium/depot\_tools/src/v8/src/execution.cc:118  

#15 0x7ffbd742d586 in v8::Script::Run() /media/Chromium/chromium/depot\_tools/src/v8/src/api.cc:1588  

#16 0x7ffbd9152a03 in WebCore::V8Proxy::runScript(v8::Handle[v8::Script](javascript:void(0);)) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/bindings/v8/V8Proxy.cpp:382  

#17 0x7ffbd9151bab in WebCore::V8Proxy::evaluate(WebCore::ScriptSourceCode const&, WebCore::Node\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/bindings/v8/V8Proxy.cpp:353  

#18 0x7ffbd997eda7 in ~Scope /media/Chromium/chromium/depot\_tools/src/v8/include/v8.h:3577  

#19 0x7ffbd97b8c64 in WebCore::InspectorInstrumentation::hasFrontends() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/inspector/InspectorInstrumentation.h:225  

#20 0x7ffbd8dc85d8 in WebCore::ThreadTimers::sharedTimerFiredInternal() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/platform/ThreadTimers.cpp:118  

==5320== ABORTING  

Stats: 109M malloced (128M for red zones) by 331569 calls  

Stats: 19M realloced by 16069 calls  

Stats: 103M freed by 306260 calls  

Stats: 0M really freed by 0 calls  

Stats: 260M (66588 full pages) mmaped in 65 calls  

mmaps by size class: 8:262128; 9:40955; 10:28665; 11:18423; 12:3072; 13:1024; 14:512; 15:128; 16:64; 17:160; 18:96; 19:32; 20:16;  

mallocs by size class: 8:248081; 9:37212; 10:25489; 11:16687; 12:2322; 13:911; 14:418; 15:100; 16:64; 17:143; 18:95; 19:32; 20:15;  

frees by size class: 8:225725; 9:35875; 10:24598; 11:16216; 12:2223; 13:830; 14:382; 15:87; 16:52; 17:135; 18:93; 19:31; 20:13;  

rfrees by size class:  

Stats: malloc large: 285 small slow: 1343  

Shadow byte and word:  

0x1fff76d40511: fd  

0x1fff76d40510: fd fd fd fd fd fd fd fd  

More shadow bytes:  

0x1fff76d404f0: fd fd fd fd fd fd fd fd  

0x1fff76d404f8: fd fd fd fd fd fd fd fd  

0x1fff76d40500: fa fa fa fa fa fa fa fa  

0x1fff76d40508: fa fa fa fa fa fa fa fa  

=>0x1fff76d40510: fd fd fd fd fd fd fd fd  

0x1fff76d40518: fd fd fd fd fd fd fd fd  

0x1fff76d40520: fd fd fd fd fd fd fd fd  

0x1fff76d40528: fd fd fd fd fd fd fd fd  

0x1fff76d40530: fa fa fa fa fa fa fa fa

## Attachments

- [tc-20-03-12-uaf.zip](attachments/tc-20-03-12-uaf.zip) (application/zip; charset=binary, 637 B)
- [test-case.zip](attachments/test-case.zip) (application/zip; charset=binary, 992 B)

## Timeline

### [Deleted User] (2012-03-16)

I'm not sure that we will be able to do much without a testcase. Kind of looks like the ownerNode went away but I don't think I understand the lifetime of CSSStyleSheets and their style elements well enough to find the bug. I'll investigate a bit but I'm not overly optimistic :)

### js...@chromium.org (2012-03-17)

I asked him to file this so the v8 guys could have a look, in case the stack trace gives them a clue. If not we'll close it out. However, since it's not confirmed, please don't assign labels that could be misleading.

### da...@chromium.org (2012-03-19)

This looks like a crash in the bindings, not in V8 itself. Adding the bindings guys.

### ar...@chromium.org (2012-03-19)

cdn: What makes you think this is related to ownerNode? I'm curious because we rolled back a change that involved ownerNode. See https://bugs.webkit.org/show_bug.cgi?id=80880 for more details

### [Deleted User] (2012-03-19)

arv, Total guess based on a look at the code around where the crash occurs. A bad ownerNode seemed like the only thing in WebCore::toV8() that could cause a read av.

I am not at all confident in that analysis though :)

### [Deleted User] (2012-03-19)

Oh also if you look at the stack where it was allocated it is creating a style element. Would the ownerNode for a CssStyleSheet would be a style element?

I'll stop guessing now

### ax...@gmail.com (2012-03-19)

Good news - I am able to reproduce crash now, will try to provide reduced testcase tomorrow.

### [Deleted User] (2012-03-19)

Excellent!

Want to post what you have now and we can run it through our minimizer. I promise it won't affect the bounty :)

### ax...@gmail.com (2012-03-19)

Unfortunately can't do it right now, because testcase is too complicated - requires too much stuff to be done manually and cannot be automated. Actually, it's a part of fuzzing framework and has also bunch of dependencies. Tomorrow I will post minimized version, I'm working on it.

### [Deleted User] (2012-03-19)

No worries. Thanks for continuing to bang on this one.

### ax...@gmail.com (2012-03-20)

Attaching testcase and here is a new ASan log:
=================================================================
==4607== ERROR: AddressSanitizer heap-use-after-free on address 0x7fc65ad84c88 at pc 0x7fc6786ffaa9 bp 0x7fffd98b71d0 sp 0x7fffd98b71c8
READ of size 8 at 0x7fc65ad84c88 thread T0
    #0 0x7fc6786ffaa9 in WebCore::toV8(WebCore::CSSStyleSheet*) ???:0
    #1 0x7fc67339b48e in v8::internal::JSObject::GetElementWithInterceptor(v8::internal::Object*, unsigned int) /media/Chromium/chromium/depot_tools/src/v8/src/objects.cc:10097
    #2 0x7fc6734f6004 in v8::internal::Runtime::GetObjectProperty(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>) /media/Chromium/chromium/depot_tools/src/v8/src/runtime.cc:4182
    #3 0x7fc6737d93fc in v8::internal::KeyedLoadIC::Load(v8::internal::InlineCacheState, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, bool) /media/Chromium/chromium/depot_tools/src/v8/src/ic.cc:1195
    #4 0x7fc6737e4cd5 in v8::internal::KeyedLoadIC_Miss(v8::internal::Arguments, v8::internal::Isolate*) /media/Chromium/chromium/depot_tools/src/v8/src/ic.cc:1987
    #5 0x226d1c0614e
    #6 0x226d1c45020
    #7 0x226d1c22647
    #8 0x226d1c11137
    #9 0x7fc6730db278 in v8::internal::Invoke(bool, v8::internal::Handle<v8::internal::JSFunction>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*, bool*) /media/Chromium/chromium/depot_tools/src/v8/src/execution.cc:118
    #10 0x7fc673025586 in v8::Script::Run() /media/Chromium/chromium/depot_tools/src/v8/src/api.cc:1588
    #11 0x7fc674d4aa03 in WebCore::V8Proxy::runScript(v8::Handle<v8::Script>) /media/Chromium/chromium/depot_tools/src/third_party/WebKit/Source/WebCore/bindings/v8/V8Proxy.cpp:382
    #12 0x7fc674d49bab in WebCore::V8Proxy::evaluate(WebCore::ScriptSourceCode const&, WebCore::Node*) /media/Chromium/chromium/depot_tools/src/third_party/WebKit/Source/WebCore/bindings/v8/V8Proxy.cpp:353
    #13 0x7fc675576da7 in ~Scope /media/Chromium/chromium/depot_tools/src/v8/include/v8.h:3577
    #14 0x7fc6753b0d68 in WebCore::InspectorInstrumentation::hasFrontends() /media/Chromium/chromium/depot_tools/src/third_party/WebKit/Source/WebCore/inspector/InspectorInstrumentation.h:225
    #15 0x7fc6749c05d8 in WebCore::ThreadTimers::sharedTimerFiredInternal() /media/Chromium/chromium/depot_tools/src/third_party/WebKit/Source/WebCore/platform/ThreadTimers.cpp:118
    #16 0x7fc6725e9256 in base::Callback<void ()()>::Run() const /media/Chromium/chromium/depot_tools/src/./base/callback.h:272
    #17 0x7fc6725e9ab8 in MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) /media/Chromium/chromium/depot_tools/src/base/message_loop.cc:470
    #18 0x7fc6725eada9 in MessageLoop::DoWork() /media/Chromium/chromium/depot_tools/src/base/message_loop.cc:660
    #19 0x7fc6725f5277 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) /media/Chromium/chromium/depot_tools/src/base/message_pump_default.cc:28
    #20 0x7fc6725e7e1e in MessageLoop::RunInternal() /media/Chromium/chromium/depot_tools/src/base/message_loop.cc:418
    #21 0x7fc6725e600f in ~AutoRunState /media/Chromium/chromium/depot_tools/src/base/message_loop.cc:745
    #22 0x7fc6779c1b5c in RendererMain(content::MainFunctionParams const&) /media/Chromium/chromium/depot_tools/src/content/renderer/renderer_main.cc:241
    #23 0x7fc67253e4b6 in RunZygote /media/Chromium/chromium/depot_tools/src/content/app/content_main_runner.cc:245
    #24 0x7fc67253ca2a in content::ContentMain(int, char const**, content::ContentMainDelegate*) /media/Chromium/chromium/depot_tools/src/content/app/content_main.cc:35
    #25 0x7fc670fa3c97 in ChromeMain /media/Chromium/chromium/depot_tools/src/chrome/app/chrome_main.cc:32
    #26 0x7fc670fa3beb in main /media/Chromium/chromium/depot_tools/src/chrome/app/chrome_exe_main_gtk.cc:18
    #27 0x7fc66a3b3d8e in __libc_start_main /build/buildd/eglibc-2.12.1/csu/libc-start.c:258
0x7fc65ad84c88 is located 8 bytes inside of 144-byte region [0x7fc65ad84c80,0x7fc65ad84d10)
freed by thread T0 here:
    #0 0x7fc678d439d2 in operator delete(void*) ??:0
    #1 0x7fc673136b39 in v8::internal::RuntimeProfiler::IsEnabled() /media/Chromium/chromium/depot_tools/src/v8/src/runtime-profiler.h:50
previously allocated by thread T0 here:
    #0 0x7fc678d43852 in operator new(unsigned long) ??:0
    #1 0x7fc676655fe4 in WebCore::SVGStyleElement::create(WebCore::QualifiedName const&, WebCore::Document*, bool) /media/Chromium/chromium/depot_tools/src/third_party/WebKit/Source/WebCore/svg/SVGStyleElement.cpp:51
    #2 0x7fc6763fcf79 in WTF::PassRefPtr<WebCore::SVGStyleElement>::leakRef() const /media/Chromium/chromium/depot_tools/src/third_party/WebKit/Source/JavaScriptCore/wtf/PassRefPtr.h:161
    #3 0x7fc6763f6728 in WTF::PassRefPtr<WebCore::SVGElement>::operator WebCore::SVGElement* WTF::PassRefPtr<WebCore::SVGElement>::*() const /media/Chromium/chromium/depot_tools/src/third_party/WebKit/Source/JavaScriptCore/wtf/PassRefPtr.h:82
    #4 0x7fc6740eb7c8 in WTF::PassRefPtr<WebCore::SVGElement>::leakRef() const /media/Chromium/chromium/depot_tools/src/third_party/WebKit/Source/JavaScriptCore/wtf/PassRefPtr.h:161
    #5 0x7fc6754cc4fa in WTF::PassRefPtr<WebCore::Element>::leakRef() const /media/Chromium/chromium/depot_tools/src/third_party/WebKit/Source/JavaScriptCore/wtf/PassRefPtr.h:161
    #6 0x7fc6742fd3b6 in xmlParseStartTag2 /media/Chromium/chromium/depot_tools/src/third_party/libxml/src/parser.c:9126
    #7 0x7fc6743061c9 in xmlParseTryOrFinish /media/Chromium/chromium/depot_tools/src/third_party/libxml/src/parser.c:10847
    #8 0x7fc67430395c in xmlParseChunk /media/Chromium/chromium/depot_tools/src/third_party/libxml/src/parser.c:11625
    #9 0x7fc6754cac50 in WebCore::DocumentParser::isStopped() const /media/Chromium/chromium/depot_tools/src/third_party/WebKit/Source/WebCore/dom/DocumentParser.h:69
    #10 0x7fc6754c4965 in ~RefPtr /media/Chromium/chromium/depot_tools/src/third_party/WebKit/Source/JavaScriptCore/wtf/RefPtr.h:58
    #11 0x7fc678358279 in ~Deque /media/Chromium/chromium/depot_tools/src/third_party/WebKit/Source/JavaScriptCore/wtf/Deque.h:370
    #12 0x7fc6752a0e9f in WebCore::DocumentLoader::commitData(char const*, unsigned long) /media/Chromium/chromium/depot_tools/src/third_party/WebKit/Source/WebCore/loader/DocumentLoader.cpp:327
    #13 0x7fc67403b618 in WebKit::FrameLoaderClientImpl::committedLoad(WebCore::DocumentLoader*, char const*, int) /media/Chromium/chromium/depot_tools/src/third_party/WebKit/Source/WebKit/chromium/src/FrameLoaderClientImpl.cpp:1137
    #14 0x7fc6752a0abc in WebCore::DocumentLoader::commitLoad(char const*, int) /media/Chromium/chromium/depot_tools/src/third_party/WebKit/Source/WebCore/loader/DocumentLoader.cpp:313
    #15 0x7fc67533622e in WebCore::ResourceLoader::didReceiveData(char const*, int, long long, bool) /media/Chromium/chromium/depot_tools/src/third_party/WebKit/Source/WebCore/loader/ResourceLoader.cpp:292
    #16 0x7fc675313450 in WebCore::MainResourceLoader::didReceiveData(char const*, int, long long, bool) /media/Chromium/chromium/depot_tools/src/third_party/WebKit/Source/WebCore/loader/MainResourceLoader.cpp:464
    #17 0x7fc67533791b in WebCore::InspectorInstrumentation::hasFrontends() /media/Chromium/chromium/depot_tools/src/third_party/WebKit/Source/WebCore/inspector/InspectorInstrumentation.h:225
    #18 0x7fc673af77f2 in ResourceDispatcher::OnReceivedData(IPC::Message const&, int, base::FileDescriptor, int, int) /media/Chromium/chromium/depot_tools/src/content/common/resource_dispatcher.cc:404
    #19 0x7fc673af5f45 in ResourceDispatcher::DispatchMessage(IPC::Message const&) /media/Chromium/chromium/depot_tools/src/./content/common/resource_messages.h:155
    #20 0x7fc673af4290 in ResourceDispatcher::OnMessageReceived(IPC::Message const&) /media/Chromium/chromium/depot_tools/src/content/common/resource_dispatcher.cc:326
    #21 0x7fc6739ee75f in ChildThread::OnMessageReceived(IPC::Message const&) /media/Chromium/chromium/depot_tools/src/content/common/child_thread.cc:172
    #22 0x7fc672700e13 in IPC::ChannelProxy::Context::OnDispatchMessage(IPC::Message const&) /media/Chromium/chromium/depot_tools/src/ipc/ipc_channel_proxy.cc:268
==4607== ABORTING
Stats: 48M malloced (35M for red zones) by 74186 calls
Stats: 1M realloced by 1905 calls
Stats: 45M freed by 58757 calls
Stats: 0M really freed by 0 calls
Stats: 116M (29716 full pages) mmaped in 29 calls
  mmaps   by size class: 8:65532; 9:16382; 10:8190; 11:2047; 12:1024; 13:1536; 14:256; 15:384; 16:64; 17:64; 18:16; 19:8; 20:8; 22:5;
  mallocs by size class: 8:57634; 9:8577; 10:4433; 11:1317; 12:378; 13:1335; 14:144; 15:254; 16:44; 17:46; 18:12; 19:2; 20:5; 22:5;
  frees   by size class: 8:43495; 9:7992; 10:4138; 11:1065; 12:290; 13:1313; 14:127; 15:247; 16:37; 17:29; 18:12; 19:2; 20:5; 22:5;
  rfrees  by size class:
Stats: malloc large: 70 small slow: 415
Shadow byte and word:
  0x1ff8cb5b0991: fd
  0x1ff8cb5b0990: fd fd fd fd fd fd fd fd
More shadow bytes:
  0x1ff8cb5b0970: fd fd fd fd fd fd fd fd
  0x1ff8cb5b0978: fd fd fd fd fd fd fd fd
  0x1ff8cb5b0980: fa fa fa fa fa fa fa fa
  0x1ff8cb5b0988: fa fa fa fa fa fa fa fa
=>0x1ff8cb5b0990: fd fd fd fd fd fd fd fd
  0x1ff8cb5b0998: fd fd fd fd fd fd fd fd
  0x1ff8cb5b09a0: fd fd fd fd fd fd fd fd
  0x1ff8cb5b09a8: fd fd fd fd fd fd fd fd
  0x1ff8cb5b09b0: fa fa fa fa fa fa fa fa



### ke...@chromium.org (2012-03-21)

Unfortunately cluster-fuzz still isn't giving us any information, so your ASAN stack trace is still the most information we have.

I can reproduce this fairly easily in debug on Windows, however. It looks like a CSSStyleSheet object has a stale pointer in m_ownerNode.

Ax330d's ASAN dump says it is freed by the runtime profiler?

arv can you have a peek at this again?

### da...@chromium.org (2012-03-21)

Assigning to arv, since he's been looking at it up to this point and it should really get attention since it's a reproducible crash. If you need any V8 help, please let me know.

### js...@chromium.org (2012-04-08)

This seems to have stalled. It looks like high-severity based on the report.

@arv - Are you working on this, and if not, do you know who should be?

### ar...@chromium.org (2012-04-09)

I'll look at it again.

The test case seems to do a lot of thing that should not matter. I'll see if I can repro this in ASAN and scale back the test further.

### ar...@chromium.org (2012-04-09)

One more thing. This is not a binding issue. It just a use after free.

### [Deleted User] (2012-04-09)

It seems like the timer is calling on a svg element that has already been freed?

### ar...@chromium.org (2012-04-09)

My gut feeling is that we are not correctly invalidating the StyleSheetList when we removed the nodes.


### ar...@chromium.org (2012-04-09)

I managed to reduce this further. It no longer uses a range and it now uses an HTML file (SVGStyleElement has the same removeFromDocument as HTMLStyleElement).

### ar...@chromium.org (2012-04-10)

https://bugs.webkit.org/show_bug.cgi?id=83605

### ar...@chromium.org (2012-04-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-04-10)

https://bugs.webkit.org/show_bug.cgi?id=83605

### ar...@chromium.org (2012-04-10)

[Empty comment from Monorail migration]

### ar...@chromium.org (2012-04-10)

[Empty comment from Monorail migration]

### ar...@chromium.org (2012-04-11)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-04-11)

http://trac.webkit.org/changeset/113887

### sc...@gmail.com (2012-04-22)

Does anyone happen to know if this affects M18 stable? Or just an M19 regression?


### in...@chromium.org (2012-04-24)

Thanks Ax330d for finally getting a awesome repro to reproduce this bug. It was really helpful to see the root problem. This qualifies for $1000 Chromium Security Reward.

### in...@chromium.org (2012-04-24)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-04-30)

M19: http://trac.webkit.org/changeset/115611

### sc...@gmail.com (2012-05-10)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-05-14)

[Empty comment from Monorail migration]

### [Deleted User] (2012-05-15)

Updating status to Fixed on security bugs which were fixed when m19 went to stable.

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-14)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-01)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-06-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/118642?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink, Blink>JavaScript]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40055123)*
