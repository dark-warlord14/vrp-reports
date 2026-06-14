# Heap-use-after-free in WebCore::SpeechSynthesis::cancel

| Field | Value |
|-------|-------|
| **Issue ID** | [40078946](https://issues.chromium.org/issues/40078946) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Speech |
| **Reporter** | ch...@gmail.com |
| **Assignee** | dm...@chromium.org |
| **Created** | 2014-02-19 |
| **Bounty** | $4,000.00 |

## Description

**VULNERABILITY DETAILS**  

It is possible to use m\_currentSpeechUtterance variable of SpeechSynthesis.cpp, after it is freed.

Test Case:

<script>
speechSynthesis.speak(new SpeechSynthesisUtterance("Hello"));
speechSynthesis.cancel();
window.gc();
speechSynthesis.cancel();
</script>
## Same or Similar Issues

1). <https://code.google.com/p/chromium/issues/detail?id=222192>  

Based on changeset I assume this issue is fixed for mac and not for linux. Anyway need to further investigate.  

2). <https://code.google.com/p/chromium/issues/detail?id=252054>  

3). <https://code.google.com/p/chromium/issues/detail?id=240584>

**VERSION**  

Chrome Version: [34.0.1847.0 (Developer Build 251903) aura] + [trunk build]  

Blink Version: 537.36 (@167392)

```
            \* Does Not reproduce in official beta version 33.0.1750.112.  
              But reproduces in beta version 33.0.1750.91 built with Asan.  
              Downloaded prebuilt asan version from   
              https://commondatastorage.googleapis.com/chromium-browser-asan/index.html  

```

Operating System: [Ubuntu 12.04 64 bit]

**REPRODUCTION CASE**

1. Run chrome built with asan with this flag.  
   
   --js-flags="--expose-gc"
2. Run above mentioned test case in chrome.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: [tab]  

Crash State: [Address sanitizer output]  

AddressSanitizer: heap-use-after-free on address 0x60c00001fccc at pc 0x7ff450886c66 bp 0x7fff561136c0 sp 0x7fff561136b8  

READ of size 1 at 0x60c00001fccc thread T0 (chrome)  

#0 0x7ff450886c65 in WTF::RefCountedBase::ref() out/Release/../../third\_party/WebKit/Source/wtf/RefCounted.h:61  

#1 0x7ff4531bad37 in WebCore::SpeechSynthesis::cancel() out/Release/../../third\_party/WebKit/Source/modules/speech/SpeechSynthesis.cpp:130  

#2 0x7ff452791f9c in WebCore::SpeechSynthesisV8Internal::cancelMethodCallback(v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&) out/Release/gen/blink/bindings/V8SpeechSynthesis.cpp:176  

#3 0x7ff4514e3dd0 in v8::internal::FunctionCallbackArguments::Call(void (\*)(v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&)) out/Release/../../v8/src/arguments.cc:56  

#4 0x7ff450f26bed in v8::internal::MaybeObject\* v8::internal::HandleApiCallHelper<false>(v8::internal::(anonymous namespace)::BuiltinArguments<(v8::internal::BuiltinExtraArguments)1>, v8::internal::Isolate\*) out/Release/../../v8/src/builtins.cc:1215  

#5 0x7ff450f21c15 in v8::internal::Builtin\_HandleApiCall(int, v8::internal::Object\*\*, v8::internal::Isolate\*) out/Release/../../v8/src/builtins.cc:1231

0x60c00001fccc is located 12 bytes inside of 128-byte region [0x60c00001fcc0,0x60c00001fd40)  

freed by thread T0 (chrome) here:  

#0 0x7ff44d5da9d1 in \_\_interceptor\_free *asan\_rtl*  

#1 0x7ff451003758 in v8::internal::GlobalHandles::Node::PostGarbageCollectionProcessing(v8::internal::Isolate\*) out/Release/../../v8/src/global-handles.cc:270  

#2 0x7ff451003250 in v8::internal::GlobalHandles::PostGarbageCollectionProcessing(v8::internal::GarbageCollector, v8::internal::GCTracer\*) out/Release/../../v8/src/global-handles.cc:679  

#3 0x7ff4510393c1 in v8::internal::Heap::PerformGarbageCollection(v8::internal::GarbageCollector, v8::internal::GCTracer\*, v8::GCCallbackFlags) out/Release/../../v8/src/heap.cc:1161  

#4 0x7ff45103890d in v8::internal::Heap::CollectGarbage(v8::internal::GarbageCollector, char const\*, char const\*, v8::GCCallbackFlags) out/Release/../../v8/src/heap.cc:822  

#5 0x7ff450eef044 in v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, char const\*, v8::GCCallbackFlags) out/Release/../../v8/src/heap-inl.h:558  

#6 0x7ff451038425 in v8::internal::Heap::CollectAllGarbage(int, char const\*, v8::GCCallbackFlags) out/Release/../../v8/src/heap.cc:712  

#7 0x7ff4514e3dd0 in v8::internal::FunctionCallbackArguments::Call(void (\*)(v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&)) out/Release/../../v8/src/arguments.cc:56  

#8 0x7ff450f26bed in v8::internal::MaybeObject\* v8::internal::HandleApiCallHelper<false>(v8::internal::(anonymous namespace)::BuiltinArguments<(v8::internal::BuiltinExtraArguments)1>, v8::internal::Isolate\*) out/Release/../../v8/src/builtins.cc:1215  

#9 0x7ff450f21c15 in v8::internal::Builtin\_HandleApiCall(int, v8::internal::Object\*\*, v8::internal::Isolate\*) out/Release/../../v8/src/builtins.cc:1231  

#10 0x7ff450faefa5 in v8::internal::Invoke(bool, v8::internal::Handle[v8::internal::JSFunction](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*, bool\*) out/Release/../../v8/src/execution.cc:119  

#11 0x7ff450ed3238 in v8::Script::Run() out/Release/../../v8/src/api.cc:1743  

#12 0x7ff452e23f8c in WebCore::V8ScriptRunner::runCompiledScript(v8::Handle[v8::Script](javascript:void(0);), WebCore::ExecutionContext\*, v8::Isolate\*) out/Release/../../third\_party/WebKit/Source/bindings/v8/V8ScriptRunner.cpp:97  

#13 0x7ff452dbf7b1 in WebCore::ScriptController::executeScriptAndReturnValue(v8::Handle[v8::Context](javascript:void(0);), WebCore::ScriptSourceCode const&, WebCore::AccessControlStatus) out/Release/../../third\_party/WebKit/Source/bindings/v8/ScriptController.cpp:213  

#14 0x7ff452dc34d7 in WebCore::ScriptController::evaluateScriptInMainWorld(WebCore::ScriptSourceCode const&, WebCore::AccessControlStatus, WebCore::ScriptController::ExecuteScriptPolicy) out/Release/../../third\_party/WebKit/Source/bindings/v8/ScriptController.cpp:617  

#15 0x7ff452dc39bc in WebCore::ScriptController::executeScriptInMainWorld(WebCore::ScriptSourceCode const&, WebCore::AccessControlStatus) out/Release/../../third\_party/WebKit/Source/bindings/v8/ScriptController.cpp:588  

#16 0x7ff450c0426f in WebCore::ScriptLoader::executeScript(WebCore::ScriptSourceCode const&) out/Release/../../third\_party/WebKit/Source/core/dom/ScriptLoader.cpp:333  

#17 0x7ff450c01405 in WebCore::ScriptLoader::prepareScript(WTF::TextPosition const&, WebCore::ScriptLoader::LegacyTypeSupport) out/Release/../../third\_party/WebKit/Source/core/dom/ScriptLoader.cpp:243  

#18 0x7ff45187caa0 in WebCore::HTMLScriptRunner::runScript(WebCore::Element\*, WTF::TextPosition const&) out/Release/../../third\_party/WebKit/Source/core/html/parser/HTMLScriptRunner.cpp:297  

#19 0x7ff45187c81d in WebCore::HTMLScriptRunner::execute(WTF::PassRefPtr[WebCore::Element](javascript:void(0);), WTF::TextPosition const&) out/Release/../../third\_party/WebKit/Source/core/html/parser/HTMLScriptRunner.cpp:172  

#20 0x7ff451861f3a in WebCore::HTMLDocumentParser::runScriptsForPausedTreeBuilder() out/Release/../../third\_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:255  

#21 0x7ff451863f76 in WebCore::HTMLDocumentParser::processParsedChunkFromBackgroundParser(WTF::PassOwnPtr[WebCore::HTMLDocumentParser::ParsedChunk](javascript:void(0);)) out/Release/../../third\_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:436  

#22 0x7ff451861be5 in WebCore::HTMLDocumentParser::pumpPendingSpeculations() out/Release/../../third\_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:474  

#23 0x7ff4518625cd in WebCore::HTMLDocumentParser::didReceiveParsedChunkFromBackgroundParser(WTF::PassOwnPtr[WebCore::HTMLDocumentParser::ParsedChunk](javascript:void(0);)) out/Release/../../third\_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:317  

#24 0x7ff45194b1c0 in WTF::FunctionWrapper<void (WebCore::HTMLDocumentParser::\*)(WTF::PassOwnPtr[WebCore::HTMLDocumentParser::ParsedChunk](javascript:void(0);))>::operator()(WTF::WeakPtr[WebCore::HTMLDocumentParser](javascript:void(0);) const&, WTF::PassOwnPtr[WebCore::HTMLDocumentParser::ParsedChunk](javascript:void(0);)) out/Release/../../third\_party/WebKit/Source/wtf/Functional.h:210  

#25 0x7ff45194b041 in WTF::BoundFunctionImpl<WTF::FunctionWrapper<void (WebCore::HTMLDocumentParser::\*)(WTF::PassOwnPtr[WebCore::HTMLDocumentParser::ParsedChunk](javascript:void(0);))>, void (WTF::WeakPtr[WebCore::HTMLDocumentParser](javascript:void(0);), WTF::PassOwnPtr[WebCore::HTMLDocumentParser::ParsedChunk](javascript:void(0);))>::operator()() out/Release/../../third\_party/WebKit/Source/wtf/Functional.h:420

previously allocated by thread T0 (chrome) here:  

#0 0x7ff44d5dabd1 in \_\_interceptor\_malloc *asan\_rtl*  

#1 0x7ff4509b0f9a in WTF::partitionAllocGenericFlags(WTF::PartitionRootGeneric\*, int, unsigned long) out/Release/../../third\_party/WebKit/Source/wtf/PartitionAlloc.h:530  

#2 0x7ff4531bdffd in WebCore::SpeechSynthesisUtterance::create(WebCore::ExecutionContext\*, WTF::String const&) out/Release/../../third\_party/WebKit/Source/modules/speech/SpeechSynthesisUtterance.cpp:35  

#3 0x7ff4527f8dee in WebCore::SpeechSynthesisUtteranceV8Internal::constructor(v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&) out/Release/gen/blink/bindings/V8SpeechSynthesisUtterance.cpp:439  

#4 0x7ff4527f899a in WebCore::V8SpeechSynthesisUtterance::constructorCallback(v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&) out/Release/gen/blink/bindings/V8SpeechSynthesisUtterance.cpp:477  

#5 0x7ff4514e3dd0 in v8::internal::FunctionCallbackArguments::Call(void (\*)(v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&)) out/Release/../../v8/src/arguments.cc:56  

#6 0x7ff450f25fcc in v8::internal::MaybeObject\* v8::internal::HandleApiCallHelper<true>(v8::internal::(anonymous namespace)::BuiltinArguments<(v8::internal::BuiltinExtraArguments)1>, v8::internal::Isolate\*) out/Release/../../v8/src/builtins.cc:1215  

#7 0x7ff450f21d65 in v8::internal::Builtin\_HandleApiCallConstruct(int, v8::internal::Object\*\*, v8::internal::Isolate\*) out/Release/../../v8/src/builtins.cc:1236  

#8 0x7ff450faefa5 in v8::internal::Invoke(bool, v8::internal::Handle[v8::internal::JSFunction](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*, bool\*) out/Release/../../v8/src/execution.cc:119  

#9 0x7ff450ed3238 in v8::Script::Run() out/Release/../../v8/src/api.cc:1743  

#10 0x7ff452e23f8c in WebCore::V8ScriptRunner::runCompiledScript(v8::Handle[v8::Script](javascript:void(0);), WebCore::ExecutionContext\*, v8::Isolate\*) out/Release/../../third\_party/WebKit/Source/bindings/v8/V8ScriptRunner.cpp:97  

#11 0x7ff452dbf7b1 in WebCore::ScriptController::executeScriptAndReturnValue(v8::Handle[v8::Context](javascript:void(0);), WebCore::ScriptSourceCode const&, WebCore::AccessControlStatus) out/Release/../../third\_party/WebKit/Source/bindings/v8/ScriptController.cpp:213  

#12 0x7ff452dc34d7 in WebCore::ScriptController::evaluateScriptInMainWorld(WebCore::ScriptSourceCode const&, WebCore::AccessControlStatus, WebCore::ScriptController::ExecuteScriptPolicy) out/Release/../../third\_party/WebKit/Source/bindings/v8/ScriptController.cpp:617  

#13 0x7ff452dc39bc in WebCore::ScriptController::executeScriptInMainWorld(WebCore::ScriptSourceCode const&, WebCore::AccessControlStatus) out/Release/../../third\_party/WebKit/Source/bindings/v8/ScriptController.cpp:588  

#14 0x7ff450c0426f in WebCore::ScriptLoader::executeScript(WebCore::ScriptSourceCode const&) out/Release/../../third\_party/WebKit/Source/core/dom/ScriptLoader.cpp:333  

#15 0x7ff450c01405 in WebCore::ScriptLoader::prepareScript(WTF::TextPosition const&, WebCore::ScriptLoader::LegacyTypeSupport) out/Release/../../third\_party/WebKit/Source/core/dom/ScriptLoader.cpp:243  

#16 0x7ff45187caa0 in WebCore::HTMLScriptRunner::runScript(WebCore::Element\*, WTF::TextPosition const&) out/Release/../../third\_party/WebKit/Source/core/html/parser/HTMLScriptRunner.cpp:297  

#17 0x7ff45187c81d in WebCore::HTMLScriptRunner::execute(WTF::PassRefPtr[WebCore::Element](javascript:void(0);), WTF::TextPosition const&) out/Release/../../third\_party/WebKit/Source/core/html/parser/HTMLScriptRunner.cpp:172  

#18 0x7ff451861f3a in WebCore::HTMLDocumentParser::runScriptsForPausedTreeBuilder() out/Release/../../third\_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:255  

#19 0x7ff451863f76 in WebCore::HTMLDocumentParser::processParsedChunkFromBackgroundParser(WTF::PassOwnPtr[WebCore::HTMLDocumentParser::ParsedChunk](javascript:void(0);)) out/Release/../../third\_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:436  

#20 0x7ff451861be5 in WebCore::HTMLDocumentParser::pumpPendingSpeculations() out/Release/../../third\_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:474  

#21 0x7ff4518625cd in WebCore::HTMLDocumentParser::didReceiveParsedChunkFromBackgroundParser(WTF::PassOwnPtr[WebCore::HTMLDocumentParser::ParsedChunk](javascript:void(0);)) out/Release/../../third\_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:317  

#22 0x7ff45194b1c0 in WTF::FunctionWrapper<void (WebCore::HTMLDocumentParser::\*)(WTF::PassOwnPtr[WebCore::HTMLDocumentParser::ParsedChunk](javascript:void(0);))>::operator()(WTF::WeakPtr[WebCore::HTMLDocumentParser](javascript:void(0);) const&, WTF::PassOwnPtr[WebCore::HTMLDocumentParser::ParsedChunk](javascript:void(0);)) out/Release/../../third\_party/WebKit/Source/wtf/Functional.h:210  

#23 0x7ff45194b041 in WTF::BoundFunctionImpl<WTF::FunctionWrapper<void (WebCore::HTMLDocumentParser::\*)(WTF::PassOwnPtr[WebCore::HTMLDocumentParser::ParsedChunk](javascript:void(0);))>, void (WTF::WeakPtr[WebCore::HTMLDocumentParser](javascript:void(0);), WTF::PassOwnPtr[WebCore::HTMLDocumentParser::ParsedChunk](javascript:void(0);))>::operator()() out/Release/../../third\_party/WebKit/Source/wtf/Functional.h:420  

#24 0x7ff4509b122d in WTF::callFunctionObject(void\*) out/Release/../../third\_party/WebKit/Source/wtf/MainThread.cpp:62

Assert failiure on Debug Build:

ASSERTION FAILED: !m\_currentSpeechUtterance  

../../third\_party/WebKit/Source/modules/speech/SpeechSynthesis.cpp(134) : void WebCore::SpeechSynthesis::cancel()

## Attachments

- [speechuaf_2.html](attachments/speechuaf_2.html) (text/html, 796 B)
- [speechuaf3.html](attachments/speechuaf3.html) (text/html, 778 B)

## Timeline

### cl...@chromium.org (2014-02-19)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-02-19)

[Empty comment from Monorail migration]

### [Deleted User] (2014-02-20)

[Empty comment from Monorail migration]

### ch...@gmail.com (2014-02-21)

Does not reproduce in a trunk release build without ASAN.

### ch...@gmail.com (2014-02-23)

It is possible to allocate float* pointer in same memory address of the freed m_currentSpeechUtterance.
But newly allocated float pointer also gets freed before the next use of m_currentSpeechUtterance.


1. Build chrome release build with debug symbols and without optimization.
   1.1. GYP_DEFINES='release_extra_cflags="-g -O0" ' gclient runhooks
   1.2. ninja -C out/Release chrome
2. Start a gdb debug session for chrome to open attached speechuaf_2.html.
   Chrome should be started with --js-flags="--expose-gc" flag.
   Webgl should be enabled. If not use --ignore-gpu-blacklist flag.
3. Create a breakpoint to first line of SpeechSynthesis::cancel() method od SpeechSynthesis.cpp.
4. Create a breakpoint in jsArrayToIntArray method of V8WebGLRenderingContextCustom.cpp which points to this line.
   return data;
5. Once gdb hits breakpoint, print m_currentSpeechUtterance pointer.
   (gdb) p m_currentSpeechUtterance
   $1 = {m_ptr = 0x3a886099c280}
6. View memory at the address of above pointer.
   x /31fw 0x3a886099c280
7. Continue from breakpoint.
8. Once gdb hits second breakpoint, print float* data pointer.
   (gdb) p data
   $2 = (float *) 0x3a886099c280
   * Note that data pointer is allocated at the same address as of m_currentSpeechUtterance pointer.
9. View memory at the address of data pointer.
   x /31fw 0x3a886099c280
   * Note that memory values are all changed to -2.
10. Continue from breakpoint.
11. Once gdb hits breakpoint again, print contents of m_currentSpeechUtterance pointer.
   (gdb) p m_currentSpeechUtterance
   $3 = {m_ptr = 0x3a886099c280}
   * Note that m_currentSpeechUtterance still exists at the same memory location.
12. View memory at the address of m_currentSpeechUtterance pointer
    x /31fw 0x3a886099c280
    
    * Values of first 2 words are changed, but following -2 values remain.
      I think values of first 2 words change because float* data pointer also gets freed.
      But I am not sure why exactly that happens.

### cl...@chromium.org (2014-02-24)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-02-24)

ClusterFuzz is analyzing your testcase. See https://cluster-fuzz.appspot.com/testcase?key=4777607321092096

### cl...@chromium.org (2014-02-24)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4777607321092096

Uploader: wfh@chromium.org
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 1
Crash Address: 0x61000002458c
Crash State:
  - crash stack -
  WebCore::SpeechSynthesis::cancel
  WebCore::SpeechSynthesisV8Internal::cancelMethodCallback
  - free stack -
  v8::internal::GlobalHandles::Node::PostGarbageCollectionProcessing
  v8::internal::GlobalHandles::PostGarbageCollectionProcessing
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=234149:234156

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv95B5Ntpun35wD4ph0Ty5l2dS6X04tWukDi4Ved08gAxI8dP_oC4b46Ba3TuxZ1V4IJ8Q2pW65s7-A899gA0vnDbiIstE8UbAUygDQVUzT9fbTCggiQMz5ODZfZug5Cwngb6xKK9JboNciMvsCoZvwuWZJgs2A



### wf...@chromium.org (2014-02-24)

dmazzoni we can replicate this issue on clusterfuzz and appears to be related to speech - can you take a look?

### in...@chromium.org (2014-02-24)

This is a bad regression on m33. We need to fix it in a day or two (m33 patch 1 shipping this week) or otherwise disable the feature.

### ch...@gmail.com (2014-02-25)

If there a reason for setting the severity to Medium for this use after free?

### in...@chromium.org (2014-02-25)

Yes, that looks wrong. Sorry about that.

### cl...@chromium.org (2014-02-25)

[Empty comment from Monorail migration]

### ts...@chromium.org (2014-02-25)

[Empty comment from Monorail migration]

### dm...@chromium.org (2014-02-25)

[Empty comment from Monorail migration]

### dm...@chromium.org (2014-02-26)

https://codereview.chromium.org/180553004/


### bu...@chromium.org (2014-02-28)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=168092

------------------------------------------------------------------------
r168092 | dmazzoni@google.com | 2014-02-28T08:19:18.887733Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/speechsynthesis/speech-synthesis-cancel-twice-expected.txt?r1=168092&r2=168091&pathrev=168092
   M http://src.chromium.org/viewvc/blink/trunk/Source/modules/speech/SpeechSynthesis.h?r1=168092&r2=168091&pathrev=168092
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/speechsynthesis/speech-synthesis-cancel-twice.html?r1=168092&r2=168091&pathrev=168092
   M http://src.chromium.org/viewvc/blink/trunk/Source/modules/speech/testing/PlatformSpeechSynthesizerMock.cpp?r1=168092&r2=168091&pathrev=168092
   M http://src.chromium.org/viewvc/blink/trunk/Source/modules/speech/testing/PlatformSpeechSynthesizerMock.h?r1=168092&r2=168091&pathrev=168092
   M http://src.chromium.org/viewvc/blink/trunk/Source/modules/speech/SpeechSynthesis.cpp?r1=168092&r2=168091&pathrev=168092

Fix use-after-free of m_currentSpeechUtterance.

SpeechSynthesis.cpp incorrectly assumed that calling
m_platformSpeechSynthesizer->cancel() would immediately call
didFinishSpeaking or speakingErrorOccurred, which would null out
m_currentSpeechUtterance. This assumption was true in WebKit/Mac, but
Chromium's platform implementation is asynchronous, so that call may
come later.

Fix the issue and simplify the logic by getting rid of the raw pointer
to the current utterance altogether. Now the RefPtr at the front of the
utterance queue is the current utterance, and the platform implementation
is allowed to fire events on utterances that are no longer in the queue.

BUG=344881
R=abarth@chromium.org

Review URL: https://codereview.chromium.org/180553004
------------------------------------------------------------------------

### bu...@chromium.org (2014-02-28)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=168111

------------------------------------------------------------------------
r168111 | apavlov@chromium.org | 2014-02-28T09:27:15.961361Z

Changed paths:
   D http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/speechsynthesis/speech-synthesis-cancel-twice-expected.txt?r1=168111&r2=168110&pathrev=168111
   M http://src.chromium.org/viewvc/blink/trunk/Source/modules/speech/SpeechSynthesis.h?r1=168111&r2=168110&pathrev=168111
   D http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/speechsynthesis/speech-synthesis-cancel-twice.html?r1=168111&r2=168110&pathrev=168111
   M http://src.chromium.org/viewvc/blink/trunk/Source/modules/speech/testing/PlatformSpeechSynthesizerMock.cpp?r1=168111&r2=168110&pathrev=168111
   M http://src.chromium.org/viewvc/blink/trunk/Source/modules/speech/testing/PlatformSpeechSynthesizerMock.h?r1=168111&r2=168110&pathrev=168111
   M http://src.chromium.org/viewvc/blink/trunk/Source/modules/speech/SpeechSynthesis.cpp?r1=168111&r2=168110&pathrev=168111

Revert of Fix use-after-free of m_currentSpeechUtterance. (https://codereview.chromium.org/180553004/)

Reason for revert:
Linux build broken:

../../third_party/WebKit/Source/modules/speech/SpeechSynthesis.cpp:228:12: error: cannot convert 'std::nullptr_t' to 'WebCore::SpeechSynthesisUtterance*' in return

Original issue's description:
> Fix use-after-free of m_currentSpeechUtterance.
> 
> SpeechSynthesis.cpp incorrectly assumed that calling
> m_platformSpeechSynthesizer->cancel() would immediately call
> didFinishSpeaking or speakingErrorOccurred, which would null out
> m_currentSpeechUtterance. This assumption was true in WebKit/Mac, but
> Chromium's platform implementation is asynchronous, so that call may
> come later.
> 
> Fix the issue and simplify the logic by getting rid of the raw pointer
> to the current utterance altogether. Now the RefPtr at the front of the
> utterance queue is the current utterance, and the platform implementation
> is allowed to fire events on utterances that are no longer in the queue.
> 
> BUG=344881
> R=abarth@chromium.org
> 
> Committed: https://src.chromium.org/viewvc/blink?view=rev&revision=168092

TBR=abarth@chromium.org,dmazzoni@chromium.org
NOTREECHECKS=true
NOTRY=true
BUG=344881

Review URL: https://codereview.chromium.org/184263003
------------------------------------------------------------------------

### in...@chromium.org (2014-02-28)

Oh no, it was reverted for a minor compile failure. Please fix that and merge to m33, m34 branches asap. The m33 patch 1 is getting cut at 5 pm and we want the fix to go in before Pwn2own.

### cl...@chromium.org (2014-02-28)

[Empty comment from Monorail migration]

### bu...@chromium.org (2014-02-28)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=168169

------------------------------------------------------------------------
r168169 | dmazzoni@google.com | 2014-02-28T23:42:09.289841Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/modules/speech/SpeechSynthesis.cpp?r1=168169&r2=168168&pathrev=168169

Fix use-after-free of m_currentSpeechUtterance.

SpeechSynthesis.cpp incorrectly assumed that calling
m_platformSpeechSynthesizer->cancel() would immediately call
didFinishSpeaking or speakingErrorOccurred, which would null out
m_currentSpeechUtterance. This assumption was true in WebKit/Mac, but
Chromium's platform implementation is asynchronous, so that call may
come later.

Fix the issue and simplify the logic by getting rid of the raw pointer
to the current utterance altogether. Now the RefPtr at the front of the
utterance queue is the current utterance, and the platform implementation
is allowed to fire events on utterances that are no longer in the queue.

BUG=344881
R=abarth@chromium.org

Committed: https://src.chromium.org/viewvc/blink?view=rev&revision=168092

Review URL: https://codereview.chromium.org/180553004
------------------------------------------------------------------------

### bu...@chromium.org (2014-02-28)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=168170

------------------------------------------------------------------------
r168170 | dmazzoni@google.com | 2014-02-28T23:47:02.640379Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/modules/speech/SpeechSynthesis.cpp?r1=168170&r2=168169&pathrev=168170

Revert 168169 "Fix use-after-free of m_currentSpeechUtterance."

Wrong merge base when committing!

> Fix use-after-free of m_currentSpeechUtterance.
> 
> SpeechSynthesis.cpp incorrectly assumed that calling
> m_platformSpeechSynthesizer->cancel() would immediately call
> didFinishSpeaking or speakingErrorOccurred, which would null out
> m_currentSpeechUtterance. This assumption was true in WebKit/Mac, but
> Chromium's platform implementation is asynchronous, so that call may
> come later.
> 
> Fix the issue and simplify the logic by getting rid of the raw pointer
> to the current utterance altogether. Now the RefPtr at the front of the
> utterance queue is the current utterance, and the platform implementation
> is allowed to fire events on utterances that are no longer in the queue.
> 
> BUG=344881
> R=abarth@chromium.org
> 
> Committed: https://src.chromium.org/viewvc/blink?view=rev&revision=168092
> 
> Review URL: https://codereview.chromium.org/180553004

TBR=dmazzoni@google.com

Review URL: https://codereview.chromium.org/185093002
------------------------------------------------------------------------

### bu...@chromium.org (2014-02-28)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=168171

------------------------------------------------------------------------
r168171 | dmazzoni@google.com | 2014-02-28T23:50:59.387346Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/speechsynthesis/speech-synthesis-cancel-twice.html?r1=168171&r2=168170&pathrev=168171
   M http://src.chromium.org/viewvc/blink/trunk/Source/modules/speech/testing/PlatformSpeechSynthesizerMock.cpp?r1=168171&r2=168170&pathrev=168171
   M http://src.chromium.org/viewvc/blink/trunk/Source/modules/speech/testing/PlatformSpeechSynthesizerMock.h?r1=168171&r2=168170&pathrev=168171
   M http://src.chromium.org/viewvc/blink/trunk/Source/modules/speech/SpeechSynthesis.cpp?r1=168171&r2=168170&pathrev=168171
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/speechsynthesis/speech-synthesis-cancel-twice-expected.txt?r1=168171&r2=168170&pathrev=168171
   M http://src.chromium.org/viewvc/blink/trunk/Source/modules/speech/SpeechSynthesis.h?r1=168171&r2=168170&pathrev=168171

Fix use-after-free of m_currentSpeechUtterance.

SpeechSynthesis.cpp incorrectly assumed that calling
m_platformSpeechSynthesizer->cancel() would immediately call
didFinishSpeaking or speakingErrorOccurred, which would null out
m_currentSpeechUtterance. This assumption was true in WebKit/Mac, but
Chromium's platform implementation is asynchronous, so that call may
come later.

Fix the issue and simplify the logic by getting rid of the raw pointer
to the current utterance altogether. Now the RefPtr at the front of the
utterance queue is the current utterance, and the platform implementation
is allowed to fire events on utterances that are no longer in the queue.

BUG=344881
R=abarth@chromium.org

Committed: https://src.chromium.org/viewvc/blink?view=rev&revision=168092

Committed: https://src.chromium.org/viewvc/blink?view=rev&revision=168169

Review URL: https://codereview.chromium.org/180553004
------------------------------------------------------------------------

### bu...@chromium.org (2014-03-01)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=168172

------------------------------------------------------------------------
r168172 | dmazzoni@google.com | 2014-03-01T00:21:03.813423Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/branches/chromium/1847/LayoutTests/fast/speechsynthesis/speech-synthesis-cancel-twice.html?r1=168172&r2=168171&pathrev=168172
   M http://src.chromium.org/viewvc/blink/branches/chromium/1847/Source/modules/speech/testing/PlatformSpeechSynthesizerMock.cpp?r1=168172&r2=168171&pathrev=168172
   M http://src.chromium.org/viewvc/blink/branches/chromium/1847/Source/modules/speech/testing/PlatformSpeechSynthesizerMock.h?r1=168172&r2=168171&pathrev=168172
   M http://src.chromium.org/viewvc/blink/branches/chromium/1847/Source/modules/speech/SpeechSynthesis.cpp?r1=168172&r2=168171&pathrev=168172
   A http://src.chromium.org/viewvc/blink/branches/chromium/1847/LayoutTests/fast/speechsynthesis/speech-synthesis-cancel-twice-expected.txt?r1=168172&r2=168171&pathrev=168172
   M http://src.chromium.org/viewvc/blink/branches/chromium/1847/Source/modules/speech/SpeechSynthesis.h?r1=168172&r2=168171&pathrev=168172

Merge 168171 "Fix use-after-free of m_currentSpeechUtterance."

> Fix use-after-free of m_currentSpeechUtterance.
> 
> SpeechSynthesis.cpp incorrectly assumed that calling
> m_platformSpeechSynthesizer->cancel() would immediately call
> didFinishSpeaking or speakingErrorOccurred, which would null out
> m_currentSpeechUtterance. This assumption was true in WebKit/Mac, but
> Chromium's platform implementation is asynchronous, so that call may
> come later.
> 
> Fix the issue and simplify the logic by getting rid of the raw pointer
> to the current utterance altogether. Now the RefPtr at the front of the
> utterance queue is the current utterance, and the platform implementation
> is allowed to fire events on utterances that are no longer in the queue.
> 
> BUG=344881
> R=abarth@chromium.org
> 
> Committed: https://src.chromium.org/viewvc/blink?view=rev&revision=168092
> 
> Committed: https://src.chromium.org/viewvc/blink?view=rev&revision=168169
> 
> Review URL: https://codereview.chromium.org/180553004

TBR=dmazzoni@google.com

Review URL: https://codereview.chromium.org/184763004
------------------------------------------------------------------------

### bu...@chromium.org (2014-03-01)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=168174

------------------------------------------------------------------------
r168174 | dmazzoni@google.com | 2014-03-01T00:42:16.586212Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/branches/chromium/1750/Source/modules/speech/SpeechSynthesis.cpp?r1=168174&r2=168173&pathrev=168174
   A http://src.chromium.org/viewvc/blink/branches/chromium/1750/LayoutTests/fast/speechsynthesis/speech-synthesis-cancel-twice-expected.txt?r1=168174&r2=168173&pathrev=168174
   M http://src.chromium.org/viewvc/blink/branches/chromium/1750/Source/modules/speech/SpeechSynthesis.h?r1=168174&r2=168173&pathrev=168174
   A http://src.chromium.org/viewvc/blink/branches/chromium/1750/LayoutTests/fast/speechsynthesis/speech-synthesis-cancel-twice.html?r1=168174&r2=168173&pathrev=168174
   M http://src.chromium.org/viewvc/blink/branches/chromium/1750/Source/modules/speech/testing/PlatformSpeechSynthesizerMock.cpp?r1=168174&r2=168173&pathrev=168174

Merge 168171 "Fix use-after-free of m_currentSpeechUtterance."

> Fix use-after-free of m_currentSpeechUtterance.
> 
> SpeechSynthesis.cpp incorrectly assumed that calling
> m_platformSpeechSynthesizer->cancel() would immediately call
> didFinishSpeaking or speakingErrorOccurred, which would null out
> m_currentSpeechUtterance. This assumption was true in WebKit/Mac, but
> Chromium's platform implementation is asynchronous, so that call may
> come later.
> 
> Fix the issue and simplify the logic by getting rid of the raw pointer
> to the current utterance altogether. Now the RefPtr at the front of the
> utterance queue is the current utterance, and the platform implementation
> is allowed to fire events on utterances that are no longer in the queue.
> 
> BUG=344881
> R=abarth@chromium.org
> 
> Committed: https://src.chromium.org/viewvc/blink?view=rev&revision=168092
> 
> Committed: https://src.chromium.org/viewvc/blink?view=rev&revision=168169
> 
> Review URL: https://codereview.chromium.org/180553004

TBR=dmazzoni@google.com

Review URL: https://codereview.chromium.org/177603009
------------------------------------------------------------------------

### cl...@chromium.org (2014-03-01)

ClusterFuzz has detected this issue as fixed in range 254228:254337.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4777607321092096

Uploader: wfh@chromium.org
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 1
Crash Address: 0x61000002458c
Crash State:
  - crash stack -
  WebCore::SpeechSynthesis::cancel
  WebCore::SpeechSynthesisV8Internal::cancelMethodCallback
  - free stack -
  v8::internal::GlobalHandles::Node::PostGarbageCollectionProcessing
  v8::internal::GlobalHandles::PostGarbageCollectionProcessing
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=234149:234156
Fixed: https://cluster-fuzz.appspot.com/revisions?range=254228:254337

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv95B5Ntpun35wD4ph0Ty5l2dS6X04tWukDi4Ved08gAxI8dP_oC4b46Ba3TuxZ1V4IJ8Q2pW65s7-A899gA0vnDbiIstE8UbAUygDQVUzT9fbTCggiQMz5ODZfZug5Cwngb6xKK9JboNciMvsCoZvwuWZJgs2A

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### la...@google.com (2014-03-01)

This wasn't merge-requested or approved by anyone.  Also broke the official build w/ no action taken.  Reverting.

### bu...@chromium.org (2014-03-01)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=168249

------------------------------------------------------------------------
r168249 | laforge@chromium.org | 2014-03-01T22:29:42.423353Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/branches/chromium/1750/Source/modules/speech/SpeechSynthesis.cpp?r1=168249&r2=168248&pathrev=168249
   D http://src.chromium.org/viewvc/blink/branches/chromium/1750/LayoutTests/fast/speechsynthesis/speech-synthesis-cancel-twice-expected.txt?r1=168249&r2=168248&pathrev=168249
   M http://src.chromium.org/viewvc/blink/branches/chromium/1750/Source/modules/speech/SpeechSynthesis.h?r1=168249&r2=168248&pathrev=168249
   D http://src.chromium.org/viewvc/blink/branches/chromium/1750/LayoutTests/fast/speechsynthesis/speech-synthesis-cancel-twice.html?r1=168249&r2=168248&pathrev=168249
   M http://src.chromium.org/viewvc/blink/branches/chromium/1750/Source/modules/speech/testing/PlatformSpeechSynthesizerMock.cpp?r1=168249&r2=168248&pathrev=168249

Revert 168174 "Merge 168171 "Fix use-after-free of m_currentSpee..."

> Merge 168171 "Fix use-after-free of m_currentSpeechUtterance."
> 
> > Fix use-after-free of m_currentSpeechUtterance.
> > 
> > SpeechSynthesis.cpp incorrectly assumed that calling
> > m_platformSpeechSynthesizer->cancel() would immediately call
> > didFinishSpeaking or speakingErrorOccurred, which would null out
> > m_currentSpeechUtterance. This assumption was true in WebKit/Mac, but
> > Chromium's platform implementation is asynchronous, so that call may
> > come later.
> > 
> > Fix the issue and simplify the logic by getting rid of the raw pointer
> > to the current utterance altogether. Now the RefPtr at the front of the
> > utterance queue is the current utterance, and the platform implementation
> > is allowed to fire events on utterances that are no longer in the queue.
> > 
> > BUG=344881
> > R=abarth@chromium.org
> > 
> > Committed: https://src.chromium.org/viewvc/blink?view=rev&revision=168092
> > 
> > Committed: https://src.chromium.org/viewvc/blink?view=rev&revision=168169
> > 
> > Review URL: https://codereview.chromium.org/180553004
> 
> TBR=dmazzoni@google.com
> 
> Review URL: https://codereview.chromium.org/177603009

TBR=dmazzoni@google.com
Review URL: https://codereview.chromium.org/181063010
------------------------------------------------------------------------

### bu...@chromium.org (2014-03-04)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=168408

------------------------------------------------------------------------
r168408 | dmazzoni@google.com | 2014-03-04T22:23:55.699186Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/branches/chromium/1750/Source/modules/speech/SpeechSynthesis.cpp?r1=168408&r2=168407&pathrev=168408
   M http://src.chromium.org/viewvc/blink/branches/chromium/1750/Source/modules/speech/SpeechSynthesis.h?r1=168408&r2=168407&pathrev=168408

Manual merge of r168171 to the 1750 branch.

https://codereview.chromium.org/180553004

BUG=344881


------------------------------------------------------------------------

### in...@chromium.org (2014-03-04)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-03-06)

[Empty comment from Monorail migration]

### ch...@gmail.com (2014-03-06)

Comment about Exploitability
-----------------------------

* Below mentioned infomation can be wrong, because I am still learning through trial and error.

Tested on Chrome version (Trunk build) - 35.0.1852.0 (Developer Build 252541) aura
Built chrome with these commands
GYP_DEFINES='release_extra_cflags="-g -O0" ' gclient runhooks.
ninja -C out/Release chrome

1. It is possible to allocate another object in freed space of SpeechSynthesisUtterance object.
2. But it is not possible to fill freed space with exact values I want, since ArrayBuffers and other similar objects are allocated in a seperate parition.
3. However it is possible to allocate  float* data or int* data in freed space through V8WebGLRenderingContextCustom.uniformMatrixHelper or V8WebGLRenderingContextCustom.uniformHelperi methods.
  But that float* or int* object gets deleted before next use or SpeechSynthesisUtterance.
  See https://crbug.com/chromium/344881#c5.
4. But it is possible to modify m_refCount variable of deleted SpeechSynthesisUtterance object through the values of int* array.
5. Attached example (speechuaf3.html) modifies the m_refCount of SpeechSynthesisUtterance to 0. 
6. So when the second call to SpeechSynthesis::cancel() is made (This is where use after free happens), ref() method of SpeechSynthesisUtterance gets called.
7. So m_refCount of SpeechSynthesisUtterance is incremented to 1.
8. In the same method deref() of SpeechSynthesisUtterance object also gets called.
9. Since m_refCount == 1, delete is called for SpeechSynthesisUtterance (previously freed) object.
   See deref() method of RefCounted.h file.
10. This is the disassmeply of last part of deref() method where delete is called.

    Memory location of m_currentSpeechUtterance : 0x3e523679c280
    Memory location of m_refCount of m_currentSpeechUtterance : 0x3e523679c288
    .................
    .................
   0x0000555558e3cf57 <+41>:    mov    -0x8(%rbp),%rax  ; i r $rax = 0x3e523679c280
   0x0000555558e3cf5b <+45>:    sub    $0x8,%rax        ; i r $rax = 0x3e523679c288
   0x0000555558e3cf5f <+49>:    mov    (%rax),%rax      ; i r $rax = 0x3e523679c280
   0x0000555558e3cf62 <+52>:    add    $0x8,%rax        ; i r $rax = 0xc37936523e0000
   0x0000555558e3cf66 <+56>:    mov    (%rax),%rax      ; i r $rax = 0xc37936523e0008
                                                          SIGSEGV, Segmentation fault
   0x0000555558e3cf69 <+59>:    mov    -0x8(%rbp),%rdx
   0x0000555558e3cf6d <+63>:    sub    $0x8,%rdx
   0x0000555558e3cf71 <+67>:    mov    %rdx,%rdi
   0x0000555558e3cf74 <+70>:    callq  *%rax
   0x0000555558e3cf76 <+72>:    leaveq 
   0x0000555558e3cf77 <+73>:    retq

11. I think segfault happens because first few bytes of int* data (located in same address (0x3e523679c280) as of freed m_currentSpeechUtterance)
    is changed when it is freed.
    0x0000555558e3cf66 <+56>:    mov    (%rax),%rax      ; i r $rax = 0xc37936523e0008
                                                          SIGSEGV, Segmentation fault
12. If it is possible to allocate an object which does not get freed before the next use of m_currentSpeechUtterance, then it will be possible to control the value of first few bytes.
13. Then I think it may be possible to reach 
    callq  *%rax
    and possibly exploit this bug.

### ti...@chromium.org (2014-03-07)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-03-07)

[Empty comment from Monorail migration]

### ch...@gmail.com (2014-03-12)

[Comment Deleted]

### ti...@chromium.org (2014-04-14)

My apologies for the delay here - $4000 for this one. I'll start the payment process today.

### ti...@chromium.org (2014-04-15)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-04-23)

Processing via our e-payment system can take up to 30 days, but reward should be on its way to you. Thanks again for your help!


### cl...@chromium.org (2014-06-11)

Bulk update: removing view restriction from closed bugs.

### cl...@chromium.org (2016-02-02)

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

This issue was migrated from crbug.com/chromium/344881?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40078946)*
