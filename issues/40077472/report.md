# Heap-use-after-free in WebCore::AudioNodeOutput::~AudioNodeOutput

| Field | Value |
|-------|-------|
| **Issue ID** | [40077472](https://issues.chromium.org/issues/40077472) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Reporter** | in...@chromium.org |
| **Assignee** | [Deleted User] |
| **Created** | 2013-04-26 |
| **Bounty** | $1,000.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=180675439

Fuzzer: Attekett_webaudio_fuzzer

Crash Type: Heap-use-after-free WRITE 4
Crash Address: 0x60e000008bc8
Crash State:
  - crash stack -
  WebCore::AudioNodeOutput::pull
  WebCore::AudioNodeInput::pull
  - free stack -
  WebCore::AudioDestinationChromium::~AudioDestinationChromium
  WebCore::AudioDestinationChromium::~AudioDestinationChromium
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=196281:196318

Minimized Testcase (656.35 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96znR3r13dSXxtqzgq3-gKP8lPuhfiObYDNhu_GsIIRSoK2orJXTPdZAgOBvVH2b3aLYsyHWRQaQdVKN8No717Rb8uOVWS6uVQWtD40lNcylYa-4unakcsz3HHm2AP5qwhfYuppY8QqGbujvXIneioZZJRHkQV9MZPmOPG1Lu2rLS0s5XU

## Attachments

- [180675439.zip](attachments/180675439.zip) (application/zip; charset=binary, 656.4 KB)
- [fuzz-179.html](attachments/fuzz-179.html) (text/plain; charset=us-ascii, 2.3 KB)
- [fuzz-54.html](attachments/fuzz-54.html) (text/plain; charset=us-ascii, 3.4 KB)

## Timeline

### in...@chromium.org (2013-04-26)

Repro enclosed. These look new variant after fix for https://code.google.com/p/chromium/issues/detail?id=179522.

### in...@chromium.org (2013-04-26)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=180112356

Fuzzer: Attekett_webaudio_fuzzer

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x60d0000079c4
Crash State:
  - crash stack -
  WebCore::AudioBus::zero
  WebCore::AudioNode::processIfNecessary
  - free stack -
  WebCore::AudioDestinationChromium::~AudioDestinationChromium
  WebCore::AudioDestinationChromium::~AudioDestinationChromium
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=187927:188004

Minimized Testcase (656.34 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95S-M5UM00eoF14WFkld2WRA1_fHD3Hn1E1eamxAu_7Mz4B--A8P9yTKisCue-KqxVW5pjgau6z5fY1rMXU5L4sKZd-0XrqjelmyWhoLud2BK4oTBbRb32hj4bjpkioJrOULmoqW6a6IFUjWZUFWzzI5UyM1fNL7dLlKghvfd7zbL6sDk0

### in...@chromium.org (2013-04-26)

Repro 2

### cl...@chromium.org (2013-04-26)

ClusterFuzz has detected this issue as fixed in range 196318:196327.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=180675439

Fuzzer: Attekett_webaudio_fuzzer

Crash Type: Heap-use-after-free WRITE 4
Crash Address: 0x60e000008bc8
Crash State:
  - crash stack -
  WebCore::AudioNodeOutput::pull
  WebCore::AudioNodeInput::pull
  - free stack -
  WebCore::AudioDestinationChromium::~AudioDestinationChromium
  WebCore::AudioDestinationChromium::~AudioDestinationChromium
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=196281:196318
Fixed: https://cluster-fuzz.appspot.com/revisions?range=196318:196327

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv96znR3r13dSXxtqzgq3-gKP8lPuhfiObYDNhu_GsIIRSoK2orJXTPdZAgOBvVH2b3aLYsyHWRQaQdVKN8No717Rb8uOVWS6uVQWtD40lNcylYa-4unakcsz3HHm2AP5qwhfYuppY8QqGbujvXIneioZZJRHkQV9MZPmOPG1Lu2rLS0s5XU

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### in...@chromium.org (2013-04-28)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=180734128

Fuzzer: Attekett_webaudio_fuzzer

Crash Type: Heap-use-after-free WRITE 4
Crash Address: 0x61300002e928
Crash State:
  - crash stack -
  WebCore::AudioNodeOutput::pull
  WebCore::AudioDestinationNode::render
  - free stack -
  WebCore::AudioDestinationChromium::~AudioDestinationChromium
  WebCore::AudioDestinationChromium::~AudioDestinationChromium
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=196281:196318

Minimized Testcase (3.39 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96Yf2xg0A-8zAth6OKHoQlZp1rXseY-QRzwk3nwObTmIEGirfnJUduZuRjErsv89P5ssUBTjHgT7V-ueW8rTkDV6J8VO7s6eYd4CHJDX5cOaQJh2oIZVB2IO2Mi9WCmZeasxZNzgiCyvCjtSmscQXjBA0VzXHDIaFcqEsbTD1Eo0F9G0U4

### in...@chromium.org (2013-04-28)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=180663381

Fuzzer: Attekett_webaudio_fuzzer

Crash Type: Heap-use-after-free WRITE 4
Crash Address: 0x60e00001f528
Crash State:
  - crash stack -
  WebCore::AudioNodeOutput::~AudioNodeOutput
  WebCore::AudioNode::~AudioNode
  - free stack -
  WebCore::AudioDestinationChromium::~AudioDestinationChromium
  WebCore::AudioDestinationChromium::~AudioDestinationChromium
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=196281:196318

Minimized Testcase (657.42 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94H36sD2TTb26BoYTBGofO89WJn_qSLQXjwUOqVcDBhfQaDZWuEGVuPly6CPzebrjfyRJkf-xiczSfqxNVHruja7luthC93LYCCHho3vs1DbotFBtH-ndCWt1v2ueryAnEzPdyU0REHwWCZxGZEXDvjHit50C17GjTdQmAjTd722gYPeqE

### in...@chromium.org (2013-04-28)

Another repro.

### [Deleted User] (2013-04-28)

inferno, could you share more details about the free stack? do you have the whole back track? thanks 

- free stack -
  WebCore::AudioDestinationChromium::~AudioDestinationChromium
  WebCore::AudioDestinationChromium::~AudioDestinationChromium

### in...@chromium.org (2013-04-28)

=================================================================
==325==ERROR: AddressSanitizer: heap-use-after-free on address 0x616000a27468 at pc 0x7f7230848aa3 bp 0x7f7215af62a0 sp 0x7f7215af6298
WRITE of size 4 at 0x616000a27468 thread T71 (AudioOutputDevi)
[325:326:0425/083255:ERROR:audio_output_device.cc(186)] Not implemented reached in virtual void media::AudioOutputDevice::OnStateChanged(AudioOutputIPCDelegate::State)
    #0 0x7f7230848aa2 in WTF::atomicDecrement(int volatile*) third_party/WebKit/Source/wtf/Atomics.h:111
    #1 0x7f7230848898 in WTF::ThreadSafeRefCountedBase::derefBase() third_party/WebKit/Source/wtf/ThreadSafeRefCounted.h:108:13
    #2 0x7f72316059ed in WTF::ThreadSafeRefCounted<WebCore::AudioBus>::deref() third_party/WebKit/Source/wtf/ThreadSafeRefCounted.h:136
    #3 0x7f7232c10259 in derefIfNotNull<WebCore::AudioBus> third_party/WebKit/Source/wtf/PassRefPtr.h:44
    #4 0x7f7232c10259 in WTF::RefPtr<WebCore::AudioBus>::operator=(WebCore::AudioBus*) third_party/WebKit/Source/wtf/RefPtr.h:126
    #5 0x7f7232c101dc in WebCore::AudioNodeOutput::pull(WebCore::AudioBus*, unsigned long) third_party/WebKit/Source/modules/webaudio/AudioNodeOutput.cpp:122
    #6 0x7f7232c0f2a6 in WebCore::AudioNodeInput::sumAllConnections(WebCore::AudioBus*, unsigned long) third_party/WebKit/Source/modules/webaudio/AudioNodeInput.cpp:211
    #7 0x7f7232c0f365 in WebCore::AudioNodeInput::pull(WebCore::AudioBus*, unsigned long) third_party/WebKit/Source/modules/webaudio/AudioNodeInput.cpp:239
    #8 0x7f7232c82195 in WebCore::AudioDestinationNode::render(WebCore::AudioBus*, WebCore::AudioBus*, unsigned long) third_party/WebKit/Source/modules/webaudio/AudioDestinationNode.cpp:76
    #9 0x7f7235a425c7 in WebCore::AudioPullFIFO::fillBuffer(unsigned long) third_party/WebKit/Source/core/platform/audio/AudioPullFIFO.cpp:65
    #10 0x7f7235a424f7 in WebCore::AudioPullFIFO::consume(WebCore::AudioBus*, unsigned long) third_party/WebKit/Source/core/platform/audio/AudioPullFIFO.cpp:52
    #11 0x7f72359e8649 in WebCore::AudioDestinationChromium::render(WebKit::WebVector<float*> const&, WebKit::WebVector<float*> const&, unsigned long) third_party/WebKit/Source/core/platform/audio/chromium/AudioDestinationChromium.cpp:148
    #12 0x7f7234117821 in content::RendererWebAudioDeviceImpl::RenderIO(media::AudioBus*, media::AudioBus*, int) content/renderer/media/renderer_webaudiodevice_impl.cc:98
    #13 0x7f72341175f8 in content::RendererWebAudioDeviceImpl::Render(media::AudioBus*, int) content/renderer/media/renderer_webaudiodevice_impl.cc:74
    #14 0x7f7235282646 in media::AudioOutputDevice::AudioThreadCallback::Process(int) media/audio/audio_output_device.cc:331
    #15 0x7f72353ba8e1 in media::AudioDeviceThread::Thread::Run() media/audio/audio_device_thread.cc:172
    #16 0x7f72353ba54e in media::AudioDeviceThread::Thread::ThreadMain() media/audio/audio_device_thread.cc:154
    #17 0x7f722f63fb18 in base::(anonymous namespace)::ThreadFunc(void*) base/threading/platform_thread_posix.cc:100
    #18 0x7f722e531f01 in __asan::AsanThread::ThreadStart(unsigned long)
    #19 0x7f7227993e99 in start_thread
    #20 0x7f7224a58cbc in ?? ??
0x616000a27468 is located 104 bytes inside of 160-byte region [0x616000a27400,0x616000a274a0)
freed by thread T0 (chrome) here:
    #0 0x7f722e52c3c2 in operator delete(void*)
    #1 0x7f72359e80b9 in WebCore::AudioDestinationChromium::~AudioDestinationChromium() third_party/WebKit/Source/core/platform/audio/chromium/AudioDestinationChromium.cpp:94
    #2 0x7f72359e7fed in WebCore::AudioDestinationChromium::~AudioDestinationChromium() third_party/WebKit/Source/core/platform/audio/chromium/AudioDestinationChromium.cpp:92
    #3 0x7f7232c2315b in WTF::OwnPtr<WebCore::AudioDestination>::operator=(WTF::PassOwnPtr<WebCore::AudioDestination> const&) third_party/WebKit/Source/wtf/OwnPtr.h:141
    #4 0x7f7232c23002 in WebCore::DefaultAudioDestinationNode::createDestination() third_party/WebKit/Source/modules/webaudio/DefaultAudioDestinationNode.cpp:81
    #5 0x7f7232c23491 in WebCore::DefaultAudioDestinationNode::setChannelCount(unsigned long, int&) third_party/WebKit/Source/modules/webaudio/DefaultAudioDestinationNode.cpp:131
    #6 0x7f723265ad93 in WebCore::AudioNodeV8Internal::channelCountAttrSetter(v8::Local<v8::String>, v8::Local<v8::Value>, v8::AccessorInfo const&) out/Release/obj/gen/webcore/bindings/V8AudioNode.cpp:149
    #7 0x7f72310c831e in v8::internal::JSObject::SetPropertyWithCallback(v8::internal::Object*, v8::internal::Name*, v8::internal::Object*, v8::internal::JSObject*, v8::internal::StrictModeFlag) v8/src/objects.cc:2235
    #8 0x7f72310cc3e6 in v8::internal::JSObject::SetPropertyForResult(v8::internal::LookupResult*, v8::internal::Name*, v8::internal::Object*, PropertyAttributes, v8::internal::StrictModeFlag, v8::internal::JSReceiver::StoreFromKeyed) v8/src/objects.cc:3224
    #9 0x7f72310c7946 in v8::internal::JSReceiver::SetProperty(v8::internal::Name*, v8::internal::Object*, PropertyAttributes, v8::internal::StrictModeFlag, v8::internal::JSReceiver::StoreFromKeyed) v8/src/objects.cc:2179
    #10 0x7f72310c7abb in v8::internal::JSReceiver::SetPropertyOrFail(v8::internal::Handle<v8::internal::JSReceiver>, v8::internal::Handle<v8::internal::Name>, v8::internal::Handle<v8::internal::Object>, PropertyAttributes, v8::internal::StrictModeFlag, v8::internal::JSReceiver::StoreFromKeyed) v8/src/objects.cc:2163
    #11 0x7f7230ff5eab in v8::internal::StoreIC::Store(v8::internal::InlineCacheState, v8::internal::StrictModeFlag, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::String>, v8::internal::Handle<v8::internal::Object>, v8::internal::JSReceiver::StoreFromKeyed) v8/src/ic.cc:1559
    #12 0x7f7230ff95f1 in v8::internal::StoreIC_Miss(v8::internal::Arguments, v8::internal::Isolate*) v8/src/ic.cc:2135
    #13 0x1ab172b0654d in
    #14 0x1ab172b4806c in
    #15 0x1ab172b25d03 in
    #16 0x1ab172b0c336 in
    #17 0x7f7230ef950d in v8::internal::Invoke(bool, v8::internal::Handle<v8::internal::JSFunction>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*, bool*) v8/src/execution.cc:119
    #18 0x7f7230e624a7 in v8::Script::Run() v8/src/api.cc:1819
    #19 0x7f7232823414 in WebCore::ScriptRunner::runCompiledScript(v8::Handle<v8::Script>, WebCore::ScriptExecutionContext*) third_party/WebKit/Source/bindings/v8/ScriptRunner.cpp:52
    #20 0x7f723280b28c in WebCore::ScriptController::compileAndRunScript(WebCore::ScriptSourceCode const&) third_party/WebKit/Source/bindings/v8/ScriptController.cpp:268:58
    #21 0x7f723280b62b in WebCore::ScriptController::evaluate(WebCore::ScriptSourceCode const&) third_party/WebKit/Source/bindings/v8/ScriptController.cpp:292
    #22 0x7f7230b800b6 in WebCore::ScriptElement::executeScript(WebCore::ScriptSourceCode const&) third_party/WebKit/Source/core/dom/ScriptElement.cpp:313
    #23 0x7f7230b7e0da in WebCore::ScriptElement::prepareScript(WTF::TextPosition const&, WebCore::ScriptElement::LegacyTypeSupport) third_party/WebKit/Source/core/dom/ScriptElement.cpp:244
    #24 0x7f72314babd9 in WebCore::HTMLScriptRunner::runScript(WebCore::Element*, WTF::TextPosition const&) third_party/WebKit/Source/core/html/parser/HTMLScriptRunner.cpp:310
    #25 0x7f72314ba97e in WebCore::HTMLScriptRunner::execute(WTF::PassRefPtr<WebCore::Element>, WTF::TextPosition const&) third_party/WebKit/Source/core/html/parser/HTMLScriptRunner.cpp:179
    #26 0x7f72314a14c1 in WebCore::HTMLDocumentParser::runScriptsForPausedTreeBuilder() third_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:258
    #27 0x7f72314a2e09 in WebCore::HTMLDocumentParser::processParsedChunkFromBackgroundParser(WTF::PassOwnPtr<WebCore::HTMLDocumentParser::ParsedChunk>) third_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:428
    #28 0x7f72314a10f5 in WebCore::HTMLDocumentParser::pumpPendingSpeculations() third_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:466
    #29 0x7f72314a19f2 in WebCore::HTMLDocumentParser::didReceiveParsedChunkFromBackgroundParser(WTF::PassOwnPtr<WebCore::HTMLDocumentParser::ParsedChunk>) third_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:316
    #30 0x7f723158623a in WTF::FunctionWrapper<void (WebCore::HTMLDocumentParser::*)(WTF::PassOwnPtr<WebCore::HTMLDocumentParser::ParsedChunk>)>::operator()(WTF::WeakPtr<WebCore::HTMLDocumentParser> const&, WTF::PassOwnPtr<WebCore::HTMLDocumentParser::ParsedChunk>) third_party/WebKit/Source/wtf/Functional.h:254
    #31 0x7f7231586105 in WTF::BoundFunctionImpl<WTF::FunctionWrapper<void (WebCore::HTMLDocumentParser::*)(WTF::PassOwnPtr<WebCore::HTMLDocumentParser::ParsedChunk>)>, void (WTF::WeakPtr<WebCore::HTMLDocumentParser>, WTF::PassOwnPtr<WebCore::HTMLDocumentParser::ParsedChunk>)>::operator()() third_party/WebKit/Source/wtf/Functional.h:522
    #32 0x7f723099f13d in WTF::callFunctionObject(void*) third_party/WebKit/Source/wtf/chromium/MainThreadChromium.cpp:61
    #33 0x7f722f57c8c2 in base::internal::InvokeHelper<false, void, base::internal::RunnableAdapter<void (*)(void*)>, void (void* const&)>::MakeItSo(base::internal::RunnableAdapter<void (*)(void*)>, void* const&) ./base/bind_internal.h:871
    #34 0x7f722f5d27c4 in base::MessageLoop::RunTask(base::PendingTask const&) base/message_loop.cc:474
    #35 0x7f722f5d300b in base::MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) base/message_loop.cc:486
    #36 0x7f722f5d32a1 in base::MessageLoop::DoWork() base/message_loop.cc:669
    #37 0x7f722f5df167 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) base/message_pump_default.cc:29
    #38 0x7f722f5d1e89 in base::MessageLoop::RunInternal() base/message_loop.cc:431
    #39 0x7f722f6131a9 in base::RunLoop::Run() base/run_loop.cc:45
    #40 0x7f722f5d09bd in base::MessageLoop::Run() base/message_loop.cc:311
    #41 0x7f7234020bb8 in content::RendererMain(content::MainFunctionParams const&) content/renderer/renderer_main.cc:226
    #42 0x7f722f357673 in content::RunZygote(content::MainFunctionParams const&, content::ContentMainDelegate*) content/app/content_main_runner.cc:383
    #43 0x7f722f358043 in content::RunNamedProcessTypeMain(std::string const&, content::MainFunctionParams const&, content::ContentMainDelegate*) content/app/content_main_runner.cc:439
    #44 0x7f722f358e53 in content::ContentMainRunnerImpl::Run() content/app/content_main_runner.cc:738
    #45 0x7f722f356d87 in content::ContentMain(int, char const**, content::ContentMainDelegate*) content/app/content_main.cc:35
    #46 0x7f722e539b46 in ChromeMain chrome/app/chrome_main.cc:32
    #47 0x7f722e539a8a in main chrome/app/chrome_exe_main_gtk.cc:39
    #48 0x7f722498676c in ?? ??
previously allocated by thread T0 (chrome) here:
    #0 0x7f722e52c202 in operator new(unsigned long)
    #1 0x7f72359e7bd5 in WebCore::AudioDestinationChromium::AudioDestinationChromium(WebCore::AudioIOCallback&, WTF::String const&, unsigned int, unsigned int, float) third_party/WebKit/Source/core/platform/audio/chromium/AudioDestinationChromium.cpp:77:14
    #2 0x7f72359e77a3 in WebCore::AudioDestination::create(WebCore::AudioIOCallback&, WTF::String const&, unsigned int, unsigned int, float) third_party/WebKit/Source/core/platform/audio/chromium/AudioDestinationChromium.cpp:50:12
    #3 0x7f7232c22ff2 in WebCore::DefaultAudioDestinationNode::createDestination() third_party/WebKit/Source/modules/webaudio/DefaultAudioDestinationNode.cpp:81
    #4 0x7f7232c22ef0 in WebCore::DefaultAudioDestinationNode::initialize() third_party/WebKit/Source/modules/webaudio/DefaultAudioDestinationNode.cpp:60
    #5 0x7f7232bf77b8 in WebCore::AudioContext::lazyInitialize() third_party/WebKit/Source/modules/webaudio/AudioContext.cpp:201
    #6 0x7f7232bf864d in WebCore::AudioContext::createBufferSource() third_party/WebKit/Source/modules/webaudio/AudioContext.cpp:338
    #7 0x7f72324a4dde in WebCore::AudioContextV8Internal::createBufferSourceMethod(v8::Arguments const&) out/Release/obj/gen/webcore/bindings/V8AudioContext.cpp:305
    #8 0x7f7230ea983f in v8::internal::MaybeObject* v8::internal::HandleApiCallHelper<false>(v8::internal::(anonymous namespace)::BuiltinArguments<(v8::internal::BuiltinExtraArguments)1>, v8::internal::Isolate*) v8/src/builtins.cc:1327
    #9 0x1ab172b0654d in
    #10 0x1ab172b46eef in
    #11 0x1ab172b25d03 in
    #12 0x1ab172b0c336 in
    #13 0x7f7230ef950d in v8::internal::Invoke(bool, v8::internal::Handle<v8::internal::JSFunction>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*, bool*) v8/src/execution.cc:119
    #14 0x7f7230e624a7 in v8::Script::Run() v8/src/api.cc:1819
    #15 0x7f7232823414 in WebCore::ScriptRunner::runCompiledScript(v8::Handle<v8::Script>, WebCore::ScriptExecutionContext*) third_party/WebKit/Source/bindings/v8/ScriptRunner.cpp:52
    #16 0x7f723280b28c in WebCore::ScriptController::compileAndRunScript(WebCore::ScriptSourceCode const&) third_party/WebKit/Source/bindings/v8/ScriptController.cpp:268:58
    #17 0x7f723280b62b in WebCore::ScriptController::evaluate(WebCore::ScriptSourceCode const&) third_party/WebKit/Source/bindings/v8/ScriptController.cpp:292
    #18 0x7f7230b800b6 in WebCore::ScriptElement::executeScript(WebCore::ScriptSourceCode const&) third_party/WebKit/Source/core/dom/ScriptElement.cpp:313
    #19 0x7f7230b7e0da in WebCore::ScriptElement::prepareScript(WTF::TextPosition const&, WebCore::ScriptElement::LegacyTypeSupport) third_party/WebKit/Source/core/dom/ScriptElement.cpp:244
    #20 0x7f72314babd9 in WebCore::HTMLScriptRunner::runScript(WebCore::Element*, WTF::TextPosition const&) third_party/WebKit/Source/core/html/parser/HTMLScriptRunner.cpp:310
    #21 0x7f72314ba97e in WebCore::HTMLScriptRunner::execute(WTF::PassRefPtr<WebCore::Element>, WTF::TextPosition const&) third_party/WebKit/Source/core/html/parser/HTMLScriptRunner.cpp:179
    #22 0x7f72314a14c1 in WebCore::HTMLDocumentParser::runScriptsForPausedTreeBuilder() third_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:258
    #23 0x7f72314a2e09 in WebCore::HTMLDocumentParser::processParsedChunkFromBackgroundParser(WTF::PassOwnPtr<WebCore::HTMLDocumentParser::ParsedChunk>) third_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:428
    #24 0x7f72314a10f5 in WebCore::HTMLDocumentParser::pumpPendingSpeculations() third_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:466
    #25 0x7f72314a19f2 in WebCore::HTMLDocumentParser::didReceiveParsedChunkFromBackgroundParser(WTF::PassOwnPtr<WebCore::HTMLDocumentParser::ParsedChunk>) third_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:316
    #26 0x7f723158623a in WTF::FunctionWrapper<void (WebCore::HTMLDocumentParser::*)(WTF::PassOwnPtr<WebCore::HTMLDocumentParser::ParsedChunk>)>::operator()(WTF::WeakPtr<WebCore::HTMLDocumentParser> const&, WTF::PassOwnPtr<WebCore::HTMLDocumentParser::ParsedChunk>) third_party/WebKit/Source/wtf/Functional.h:254
    #27 0x7f7231586105 in WTF::BoundFunctionImpl<WTF::FunctionWrapper<void (WebCore::HTMLDocumentParser::*)(WTF::PassOwnPtr<WebCore::HTMLDocumentParser::ParsedChunk>)>, void (WTF::WeakPtr<WebCore::HTMLDocumentParser>, WTF::PassOwnPtr<WebCore::HTMLDocumentParser::ParsedChunk>)>::operator()() third_party/WebKit/Source/wtf/Functional.h:522
    #28 0x7f723099f13d in WTF::callFunctionObject(void*) third_party/WebKit/Source/wtf/chromium/MainThreadChromium.cpp:61
    #29 0x7f722f57c8c2 in base::internal::InvokeHelper<false, void, base::internal::RunnableAdapter<void (*)(void*)>, void (void* const&)>::MakeItSo(base::internal::RunnableAdapter<void (*)(void*)>, void* const&) ./base/bind_internal.h:871
    #30 0x7f722f5d27c4 in base::MessageLoop::RunTask(base::PendingTask const&) base/message_loop.cc:474
    #31 0x7f722f5d300b in base::MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) base/message_loop.cc:486
    #32 0x7f722f5d32a1 in base::MessageLoop::DoWork() base/message_loop.cc:669
    #33 0x7f722f5df167 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) base/message_pump_default.cc:29
    #34 0x7f722f5d1e89 in base::MessageLoop::RunInternal() base/message_loop.cc:431
    #35 0x7f722f6131a9 in base::RunLoop::Run() base/run_loop.cc:45
    #36 0x7f722f5d09bd in base::MessageLoop::Run() base/message_loop.cc:311
    #37 0x7f7234020bb8 in content::RendererMain(content::MainFunctionParams const&) content/renderer/renderer_main.cc:226
    #38 0x7f722f357673 in content::RunZygote(content::MainFunctionParams const&, content::ContentMainDelegate*) content/app/content_main_runner.cc:383
    #39 0x7f722f358043 in content::RunNamedProcessTypeMain(std::string const&, content::MainFunctionParams const&, content::ContentMainDelegate*) content/app/content_main_runner.cc:439
    #40 0x7f722f358e53 in content::ContentMainRunnerImpl::Run() content/app/content_main_runner.cc:738
    #41 0x7f722f356d87 in content::ContentMain(int, char const**, content::ContentMainDelegate*) content/app/content_main.cc:35
    #42 0x7f722e539b46 in ChromeMain chrome/app/chrome_main.cc:32
    #43 0x7f722e539a8a in main chrome/app/chrome_exe_main_gtk.cc:39
    #44 0x7f722498676c in ?? ??
Thread T71 (AudioOutputDevi) created by T1 (Chrome_ChildIOT) here:
    #0 0x7f722e527dc8 in __interceptor_pthread_create
    #1 0x7f722f63f871 in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThread::Delegate*, unsigned long*, base::ThreadPriority) base/threading/platform_thread_posix.cc:164
    #2 0x7f722f63f9c8 in base::PlatformThread::CreateWithPriority(unsigned long, base::PlatformThread::Delegate*, unsigned long*, base::ThreadPriority) base/threading/platform_thread_posix.cc:273
    #3 0x7f72353b9b8a in media::AudioDeviceThread::Thread::Start() media/audio/audio_device_thread.cc:113
    #4 0x7f72353b9978 in media::AudioDeviceThread::Start(media::AudioDeviceThread::Callback*, int, char const*) media/audio/audio_device_thread.cc:77
    #5 0x7f7235281a16 in media::AudioOutputDevice::OnStreamCreated(base::FileDescriptor, int, int) media/audio/audio_output_device.cc:241
    #6 0x7f7234104c34 in content::AudioMessageFilter::OnStreamCreated(int, base::FileDescriptor, base::FileDescriptor, unsigned int) content/renderer/media/audio_message_filter.cc:182
    #7 0x7f7234104a22 in bool AudioMsg_NotifyStreamCreated::Dispatch<content::AudioMessageFilter, content::AudioMessageFilter, void (content::AudioMessageFilter::*)(int, base::FileDescriptor, base::FileDescriptor, unsigned int)>(IPC::Message const*, content::AudioMessageFilter*, content::AudioMessageFilter*, void (content::AudioMessageFilter::*)(int, base::FileDescriptor, base::FileDescriptor, unsigned int)) ./content/common/media/audio_messages.h:46
    #8 0x7f72341048bc in content::AudioMessageFilter::OnMessageReceived(IPC::Message const&) content/renderer/media/audio_message_filter.cc:123
    #9 0x7f722ffb2743 in IPC::ChannelProxy::Context::TryFilters(IPC::Message const&) ipc/ipc_channel_proxy.cc:79
    #10 0x7f722ffc4d14 in IPC::SyncChannel::SyncContext::OnMessageReceived(IPC::Message const&) ipc/ipc_sync_channel.cc:330
    #11 0x7f722ffbac1b in IPC::internal::ChannelReader::DispatchInputData(char const*, int) ipc/ipc_channel_reader.cc:90
    #12 0x7f722ffba7bc in IPC::internal::ChannelReader::ProcessIncomingMessages() ipc/ipc_channel_reader.cc:32
    #13 0x7f722ffac270 in IPC::Channel::ChannelImpl::OnFileCanReadWithoutBlocking(int) ipc/ipc_channel_posix.cc:641
    #14 0x7f722f56803d in base::MessagePumpLibevent::FileDescriptorWatcher::OnFileCanReadWithoutBlocking(int, base::MessagePumpLibevent*) base/message_pump_libevent.cc:102
    #15 0x7f722f5696a3 in base::MessagePumpLibevent::OnLibeventNotification(int, short, void*) base/message_pump_libevent.cc:359
    #16 0x7f722f6ad048 in event_process_active third_party/libevent/event.c:385
    #17 0x7f722f6ac2a1 in event_base_loop third_party/libevent/event.c:525
    #18 0x7f722f569dbc in base::MessagePumpLibevent::Run(base::MessagePump::Delegate*) base/message_pump_libevent.cc:262
    #19 0x7f722f5d1e89 in base::MessageLoop::RunInternal() base/message_loop.cc:431
    #20 0x7f722f6131a9 in base::RunLoop::Run() base/run_loop.cc:45
    #21 0x7f722f5d09bd in base::MessageLoop::Run() base/message_loop.cc:311
    #22 0x7f722f64e339 in base::Thread::ThreadMain() base/threading/thread.cc:197
    #23 0x7f722f63fb18 in base::(anonymous namespace)::ThreadFunc(void*) base/threading/platform_thread_posix.cc:100
    #24 0x7f722e531f01 in __asan::AsanThread::ThreadStart(unsigned long)
Thread T1 (Chrome_ChildIOT) created by T0 (chrome) here:
    #0 0x7f722e527dc8 in __interceptor_pthread_create
    #1 0x7f722f63f871 in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThread::Delegate*, unsigned long*, base::ThreadPriority) base/threading/platform_thread_posix.cc:164
    #2 0x7f722f63f71c in base::PlatformThread::Create(unsigned long, base::PlatformThread::Delegate*, unsigned long*) base/threading/platform_thread_posix.cc:265
    #3 0x7f722f64dbbc in base::Thread::StartWithOptions(base::Thread::Options const&) base/threading/thread.cc:93
    #4 0x7f723001d192 in content::ChildProcess::ChildProcess() content/common/child_process.cc:53
    #5 0x7f7233f99a8d in content::RenderProcess::RenderProcess() ./content/renderer/render_process.h:28
    #6 0x7f7233f99756 in content::RenderProcessImpl::RenderProcessImpl() content/renderer/render_process_impl.cc:44
    #7 0x7f7234020b61 in content::RendererMain(content::MainFunctionParams const&) content/renderer/renderer_main.cc:212
    #8 0x7f722f357673 in content::RunZygote(content::MainFunctionParams const&, content::ContentMainDelegate*) content/app/content_main_runner.cc:383
    #9 0x7f722f358043 in content::RunNamedProcessTypeMain(std::string const&, content::MainFunctionParams const&, content::ContentMainDelegate*) content/app/content_main_runner.cc:439
    #10 0x7f722f358e53 in content::ContentMainRunnerImpl::Run() content/app/content_main_runner.cc:738
    #11 0x7f722f356d87 in content::ContentMain(int, char const**, content::ContentMainDelegate*) content/app/content_main.cc:35
    #12 0x7f722e539b46 in ChromeMain chrome/app/chrome_main.cc:32
    #13 0x7f722e539a8a in main chrome/app/chrome_exe_main_gtk.cc:39
    #14 0x7f722498676c in ?? ??
Shadow bytes around the buggy address:
  0x0c2c8013ce30: fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa
  0x0c2c8013ce40: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c2c8013ce50: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c2c8013ce60: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c2c8013ce70: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
=>0x0c2c8013ce80: fd fd fd fd fd fd fd fd fd fd fd fd fd[fd]fd fd
  0x0c2c8013ce90: fd fd fd fd fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c2c8013cea0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c2c8013ceb0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c2c8013cec0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c2c8013ced0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07
  Heap left redzone:     fa
  Heap righ redzone:     fb
  Freed Heap region:     fd
  Stack left redzone:    f1
  Stack mid redzone:     f2
  Stack right redzone:   f3
  Stack partial redzone: f4
  Stack after return:    f5
  Stack use after scope: f8
  Global redzone:        f9
  Global init order:     f6
  Poisoned by user:      f7
  ASan internal:         fe
==325==ABORTING

### cl...@chromium.org (2013-04-29)

ClusterFuzz has detected this issue as fixed in range 196379:196380.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=180734128

Fuzzer: Attekett_webaudio_fuzzer

Crash Type: Heap-use-after-free WRITE 4
Crash Address: 0x61300002e928
Crash State:
  - crash stack -
  WebCore::AudioNodeOutput::pull
  WebCore::AudioDestinationNode::render
  - free stack -
  WebCore::AudioDestinationChromium::~AudioDestinationChromium
  WebCore::AudioDestinationChromium::~AudioDestinationChromium
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=196281:196318
Fixed: https://cluster-fuzz.appspot.com/revisions?range=196379:196380

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv96Yf2xg0A-8zAth6OKHoQlZp1rXseY-QRzwk3nwObTmIEGirfnJUduZuRjErsv89P5ssUBTjHgT7V-ueW8rTkDV6J8VO7s6eYd4CHJDX5cOaQJh2oIZVB2IO2Mi9WCmZeasxZNzgiCyvCjtSmscQXjBA0VzXHDIaFcqEsbTD1Eo0F9G0U4

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### in...@chromium.org (2013-05-01)

Most variants still reproduce. search for "AudioDestinationChromium" in ClusterFuzz search box.

### cr...@google.com (2013-05-01)

[Empty comment from Monorail migration]

### cr...@google.com (2013-05-02)

It seems like it could be that AudioOutputDevice::Stop() is not synchronous, but should be.  Trying to track down this |loop_for_join| stuff in AudioDeviceThread::Stop()

The AudioOutputDevice callback still appears to be "in-flight" after we've called Stop()

### da...@chromium.org (2013-05-02)

Maybe a similar to https://crbug.com/chromium/233026.

### [Deleted User] (2013-05-02)

chris, 

we found in some places, there are some AudioBus instances as class member variables that are not wrapperred with RefPtr so they will be deleted by destructor instead of deref(), which is the root cause of this issue.

after wrapper them with RefPtr, this issue disappeared. 

will provide a patch for your review. 

thanks 



### [Deleted User] (2013-05-02)

Submitted patch to https://codereview.chromium.org/14628008/ , please help review.
Thanks.

### [Deleted User] (2013-05-02)

the root cause is that:

when destroying AudioDestinationChromium, m_fifo(AudioPullFIFO) will be destroyed and so m_tempBus will be deleted as the member of AudioPullFIFO. But this bus may be in-place bus of other nodes. So in AudioNodeOutput::pull, when m_inPlaceBus is assigned to 0, it will try to delete it again when ref count becomes 0 and oops... 

### in...@chromium.org (2013-05-02)

Please do read Mark's email titled "Calling a Code 28 for Security Bugs" on chrome-team mailing list.

### in...@chromium.org (2013-05-06)

https://src.chromium.org/viewvc/blink?view=rev&revision=149804

### bu...@chromium.org (2013-05-06)

------------------------------------------------------------------------
r149804 | xingnan.wang@intel.com | 2013-05-06T21:37:49.180661Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/modules/webaudio/MediaStreamAudioDestinationNode.h?r1=149804&r2=149803&pathrev=149804
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/platform/audio/Reverb.cpp?r1=149804&r2=149803&pathrev=149804
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/platform/audio/chromium/AudioDestinationChromium.cpp?r1=149804&r2=149803&pathrev=149804
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/platform/audio/MultiChannelResampler.cpp?r1=149804&r2=149803&pathrev=149804
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/platform/audio/chromium/AudioDestinationChromium.h?r1=149804&r2=149803&pathrev=149804
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/platform/audio/AudioPullFIFO.cpp?r1=149804&r2=149803&pathrev=149804
   M http://src.chromium.org/viewvc/blink/trunk/Source/modules/webaudio/ScriptProcessorNode.cpp?r1=149804&r2=149803&pathrev=149804
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/platform/audio/AudioFIFO.cpp?r1=149804&r2=149803&pathrev=149804
   M http://src.chromium.org/viewvc/blink/trunk/Source/modules/webaudio/OfflineAudioDestinationNode.cpp?r1=149804&r2=149803&pathrev=149804
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/platform/chromium/support/WebAudioBus.cpp?r1=149804&r2=149803&pathrev=149804
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/platform/audio/SincResampler.cpp?r1=149804&r2=149803&pathrev=149804
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/platform/audio/AudioPullFIFO.h?r1=149804&r2=149803&pathrev=149804
   M http://src.chromium.org/viewvc/blink/trunk/Source/modules/webaudio/AudioDestinationNode.h?r1=149804&r2=149803&pathrev=149804
   M http://src.chromium.org/viewvc/blink/trunk/Source/modules/webaudio/ScriptProcessorNode.h?r1=149804&r2=149803&pathrev=149804
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/platform/audio/AudioFIFO.h?r1=149804&r2=149803&pathrev=149804
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/platform/audio/AudioBus.cpp?r1=149804&r2=149803&pathrev=149804
   M http://src.chromium.org/viewvc/blink/trunk/Source/modules/webaudio/AudioParam.cpp?r1=149804&r2=149803&pathrev=149804
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/platform/audio/AudioResampler.cpp?r1=149804&r2=149803&pathrev=149804
   M http://src.chromium.org/viewvc/blink/trunk/Source/modules/webaudio/ConvolverNode.cpp?r1=149804&r2=149803&pathrev=149804
   M http://src.chromium.org/viewvc/blink/trunk/Source/modules/webaudio/MediaStreamAudioDestinationNode.cpp?r1=149804&r2=149803&pathrev=149804
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/platform/audio/AudioBus.h?r1=149804&r2=149803&pathrev=149804
   M http://src.chromium.org/viewvc/blink/trunk/Source/modules/webaudio/AudioNodeInput.cpp?r1=149804&r2=149803&pathrev=149804
   M http://src.chromium.org/viewvc/blink/trunk/Source/modules/webaudio/AudioNodeOutput.cpp?r1=149804&r2=149803&pathrev=149804

Require use of
AudioBus::create() to avoid ref-counting issues

BUG=235733

Review URL: https://chromiumcodereview.appspot.com/14628008
------------------------------------------------------------------------

### cl...@chromium.org (2013-05-08)

ClusterFuzz has detected this issue as fixed in range 198631:198845.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=180112356

Fuzzer: Attekett_webaudio_fuzzer

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x60d0000079c4
Crash State:
  - crash stack -
  WebCore::AudioBus::zero
  WebCore::AudioNode::processIfNecessary
  - free stack -
  WebCore::AudioDestinationChromium::~AudioDestinationChromium
  WebCore::AudioDestinationChromium::~AudioDestinationChromium
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=187927:188004
Fixed: https://cluster-fuzz.appspot.com/revisions?range=198631:198845

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv95S-M5UM00eoF14WFkld2WRA1_fHD3Hn1E1eamxAu_7Mz4B--A8P9yTKisCue-KqxVW5pjgau6z5fY1rMXU5L4sKZd-0XrqjelmyWhoLud2BK4oTBbRb32hj4bjpkioJrOULmoqW6a6IFUjWZUFWzzI5UyM1fNL7dLlKghvfd7zbL6sDk0

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### cl...@chromium.org (2013-05-08)

ClusterFuzz has detected this issue as fixed in range 198631:198845.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=180663381

Fuzzer: Attekett_webaudio_fuzzer

Crash Type: Heap-use-after-free WRITE 4
Crash Address: 0x60e00001f528
Crash State:
  - crash stack -
  WebCore::AudioNodeOutput::~AudioNodeOutput
  WebCore::AudioNode::~AudioNode
  - free stack -
  WebCore::AudioDestinationChromium::~AudioDestinationChromium
  WebCore::AudioDestinationChromium::~AudioDestinationChromium
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=196281:196318
Fixed: https://cluster-fuzz.appspot.com/revisions?range=198631:198845

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv94H36sD2TTb26BoYTBGofO89WJn_qSLQXjwUOqVcDBhfQaDZWuEGVuPly6CPzebrjfyRJkf-xiczSfqxNVHruja7luthC93LYCCHho3vs1DbotFBtH-ndCWt1v2ueryAnEzPdyU0REHwWCZxGZEXDvjHit50C17GjTdQmAjTd722gYPeqE

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### sc...@gmail.com (2013-05-28)

M28: r151292

### sc...@gmail.com (2013-07-03)

@attekett: thanks! $1000 etc.

### in...@chromium.org (2013-07-10)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-08-20)

[Empty comment from Monorail migration]

### js...@chromium.org (2013-11-18)

Bulk release of old security bug reports.


### ti...@chromium.org (2014-02-28)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/235733?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40077472)*
