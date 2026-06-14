# Security: heap-use-after-free blink::AudioSummingJunction::UpdateRenderingState

| Field | Value |
|-------|-------|
| **Issue ID** | [40089489](https://issues.chromium.org/issues/40089489) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebAudio |
| **Platforms** | Linux |
| **Reporter** | [Deleted User] |
| **Assignee** | rt...@chromium.org |
| **Created** | 2017-11-02 |
| **Bounty** | $3,000.00 |

## Description

I have tested this on asan-linux-release-513290 and asan-linux-stable-62.0.3202.75.

This is a UAF in webAudio

==21486==ERROR: AddressSanitizer: heap-use-after-free on address 0x60b000050550 at pc 0x55abc8b3e0f3 bp 0x7fe0b6a84190 sp 0x7fe0b6a84188
READ of size 4 at 0x60b000050550 thread T743 (AudioOutputDevi)
    #0 0x55abc8b3e0f2 in capacity third_party/WebKit/Source/platform/wtf/Vector.h:401:36
    #1 0x55abc8b3e0f2 in capacity third_party/WebKit/Source/platform/wtf/Vector.h:1010
    #2 0x55abc8b3e0f2 in WTF::Vector<std::__1::unique_ptr<blink::AudioDSPKernel, std::__1::default_delete<blink::AudioDSPKernel> >, 0ul, WTF::PartitionAllocator>::ShrinkCapacity(unsigned long) third_party/WebKit/Source/platform/wtf/Vector.h:1644
    #3 0x55abc8b3b95c in clear third_party/WebKit/Source/platform/wtf/Vector.h:1112:18
    #4 0x55abc8b3b95c in blink::AudioDSPKernelProcessor::Uninitialize() third_party/WebKit/Source/platform/audio/AudioDSPKernelProcessor.cpp:62
    #5 0x55abc8b42e1d in Uninitialize third_party/WebKit/Source/modules/webaudio/AudioBasicProcessorHandler.cpp:75:16
    #6 0x55abc8b42e1d in blink::AudioBasicProcessorHandler::CheckNumberOfChannelsForInput(blink::AudioNodeInput*) third_party/WebKit/Source/modules/webaudio/AudioBasicProcessorHandler.cpp:134
    #7 0x55abc89ff207 in blink::AudioSummingJunction::UpdateRenderingState() third_party/WebKit/Source/modules/webaudio/AudioSummingJunction.cpp:59:5
    #8 0x55abc8a04c8e in HandleDirtyAudioSummingJunctions third_party/WebKit/Source/modules/webaudio/DeferredTaskHandler.cpp:121:15
    #9 0x55abc8a04c8e in blink::DeferredTaskHandler::HandleDeferredTasks() third_party/WebKit/Source/modules/webaudio/DeferredTaskHandler.cpp:230
    #10 0x55abc8a120b5 in blink::BaseAudioContext::HandlePreRenderTasks(blink::AudioIOPosition const&) third_party/WebKit/Source/modules/webaudio/BaseAudioContext.cpp:780:30
    #11 0x55abc8a4ca43 in blink::AudioDestinationHandler::Render(blink::AudioBus*, blink::AudioBus*, unsigned long, blink::AudioIOPosition const&) third_party/WebKit/Source/modules/webaudio/AudioDestinationNode.cpp:79:14
    #12 0x55abc8aba7d2 in blink::AudioDestination::RequestRender(unsigned long, unsigned long, double, double, unsigned long) third_party/WebKit/Source/platform/audio/AudioDestination.cpp:184:15
    #13 0x55abc8ab9ea8 in blink::AudioDestination::Render(blink::WebVector<float*> const&, unsigned long, double, double, unsigned long) third_party/WebKit/Source/platform/audio/AudioDestination.cpp:143:5
    #14 0x55abc9514d57 in content::RendererWebAudioDeviceImpl::Render(base::TimeDelta, base::TimeTicks, int, media::AudioBus*) content/renderer/media/renderer_webaudiodevice_impl.cc:215:21
    #15 0x55abb3635b1c in media::SilentSinkSuspender::Render(base::TimeDelta, base::TimeTicks, int, media::AudioBus*) media/base/silent_sink_suspender.cc:83:14
    #16 0x55abb3539b27 in media::AudioOutputDevice::AudioThreadCallback::Process(unsigned int) media/audio/audio_output_device.cc:507:21
    #17 0x55abb3508991 in media::AudioDeviceThread::ThreadMain() media/audio/audio_device_thread.cc:100:18
    #18 0x55abba1aae9a in base::(anonymous namespace)::ThreadFunc(void*) base/threading/platform_thread_posix.cc:75:13
    #19 0x7fe11e83c6b9 in start_thread (/lib/x86_64-linux-gnu/libpthread.so.0+0x76b9)

## Attachments

- [DSP_UAF.html](attachments/DSP_UAF.html) (text/plain, 4.5 KB)
- [asan_uaf.txt](attachments/asan_uaf.txt) (text/plain, 24.7 KB)

## Timeline

### do...@chromium.org (2017-11-08)

rtoy/hongchan: can you please follow up on this?

[Monorail components: Blink>WebAudio]

### cl...@chromium.org (2017-11-08)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5541958587252736.

### sh...@chromium.org (2017-11-08)

[Empty comment from Monorail migration]

### rt...@chromium.org (2017-11-08)

Hmm. I see underruns in the output. I wonder if the repro case is too slow and causing glitches.

### ho...@chromium.org (2017-11-08)

I don't see AudioWorkletThread in the stack so we can safely rule out "dual thread rendering" situation. Also CF says this is not a security issue and not reproducible.

### [Deleted User] (2017-11-09)

I just tested this on a fresh ubuntu 16.04 (2 CPU/4GB RAM) machine on AWS with the stable asan build (with the file that I uploaded here) and it reproduces fine. I can provide access, if required.

Sometimes, what I have seen with this test case is that, it will pop up the "unresponsive" box and die after 10 seconds with the same UAF stacktrace.



### rt...@chromium.org (2017-11-09)

I can reproduce this on my linux box.  Asan says:

==180987==ERROR: AddressSanitizer: heap-use-after-free on address 0x60b000072524 at pc 0x7fb8dbd1b575 bp 0x7fb83edd62b0 sp 0x7fb83edd62a8
READ of size 4 at 0x60b000072524 thread T418 (AudioOutputDevi)
    #0 0x7fb8dbd1b574 in size third_party/WebKit/Source/platform/wtf/Vector.h:1009:32
    #1 0x7fb8dbd1b574 in push_back<std::__1::unique_ptr<blink::AudioDSPKernel, std::__1::default_delete<blink::AudioDSPKernel> > > third_party/WebKit/Source/platform/wtf/Vector.h:1690:0
    #2 0x7fb8dbd1b574 in blink::AudioDSPKernelProcessor::Initialize() third_party/WebKit/Source/platform/audio/AudioDSPKernelProcessor.cpp:51:0
    #3 0x7fb8daf5f286 in Initialize third_party/WebKit/Source/modules/webaudio/AudioBasicProcessorHandler.cpp:65:16
    #4 0x7fb8daf5f286 in blink::AudioBasicProcessorHandler::CheckNumberOfChannelsForInput(blink::AudioNodeInput*) third_party/WebKit/Source/modules/webaudio/AudioBasicProcessorHandler.cpp:144:0
    #5 0x7fb8dafc750e in blink::AudioSummingJunction::UpdateRenderingState() third_party/WebKit/Source/modules/webaudio/AudioSummingJunction.cpp:59:5
    #6 0x7fb8db012cb1 in HandleDirtyAudioSummingJunctions third_party/WebKit/Source/modules/webaudio/DeferredTaskHandler.cpp:121:15
    #7 0x7fb8db012cb1 in blink::DeferredTaskHandler::HandleDeferredTasks() third_party/WebKit/Source/modules/webaudio/DeferredTaskHandler.cpp:230:0
    #8 0x7fb8daff50b8 in blink::BaseAudioContext::HandlePreRenderTasks(blink::AudioIOPosition const&) third_party/WebKit/Source/modules/webaudio/BaseAudioContext.cpp:780:30
    #9 0x7fb8daf745b8 in blink::AudioDestinationHandler::Render(blink::AudioBus*, blink::AudioBus*, unsigned long, blink::AudioIOPosition const&) third_party/WebKit/Source/modules/webaudio/AudioDestinationNode.cpp:79:14
    #10 0x7fb8dbd20d22 in blink::AudioDestination::RequestRender(unsigned long, unsigned long, double, double, unsigned long) third_party/WebKit/Source/platform/audio/AudioDestination.cpp:184:15
    #11 0x7fb8dbd20468 in blink::AudioDestination::Render(blink::WebVector<float*> const&, unsigned long, double, double, unsigned long) third_party/WebKit/Source/platform/audio/AudioDestination.cpp:143:5
...
0x60b000072524 is located 36 bytes inside of 104-byte region [0x60b000072500,0x60b000072568)
freed by thread T0 (chrome) here:
    #0 0x5562fed048e2 in __interceptor_free ??:0:0
    #1 0x7fb8daf5ec7b in operator() buildtools/third_party/libc++/trunk/include/memory:2233:5
    #2 0x7fb8daf5ec7b in reset buildtools/third_party/libc++/trunk/include/memory:2546:0
    #3 0x7fb8daf5ec7b in ~unique_ptr buildtools/third_party/libc++/trunk/include/memory:2500:0
    #4 0x7fb8daf5ec7b in ~AudioBasicProcessorHandler third_party/WebKit/Source/modules/webaudio/AudioBasicProcessorHandler.cpp:58:0
    #5 0x7fb8daf5ec7b in blink::AudioBasicProcessorHandler::~AudioBasicProcessorHandler() third_party/WebKit/Source/modules/webaudio/AudioBasicProcessorHandler.cpp:55:0
    #6 0x7fb8daf581e6 in DeleteInternal<blink::AudioHandler> third_party/WebKit/Source/platform/wtf/ThreadSafeRefCounted.h:64:5
    #7 0x7fb8daf581e6 in Destruct third_party/WebKit/Source/platform/wtf/ThreadSafeRefCounted.h:44:0
    #8 0x7fb8daf581e6 in Release base/memory/ref_counted.h:386:0
    #9 0x7fb8daf581e6 in Release base/memory/scoped_refptr.h:276:0
    #10 0x7fb8daf581e6 in ~scoped_refptr base/memory/scoped_refptr.h:171:0
    #11 0x7fb8daf581e6 in blink::AudioNode::~AudioNode() third_party/WebKit/Source/modules/webaudio/AudioNode.h:307:0
    #12 0x7fb8dc4904ee in Finalize third_party/WebKit/Source/platform/heap/HeapPage.cpp:100:5
...
previously allocated by thread T0 (chrome) here:
    #0 0x5562fed04c23 in __interceptor_malloc ??:0:0
    #1 0x7fb8db063476 in PartitionAllocGenericFlags base/allocator/partition_allocator/partition_alloc.h:820:18
    #2 0x7fb8db063476 in PartitionAllocGeneric base/allocator/partition_allocator/partition_alloc.h:841:0
    #3 0x7fb8db063476 in FastMalloc third_party/WebKit/Source/platform/wtf/allocator/Partitions.h:123:0
    #4 0x7fb8db063476 in operator new third_party/WebKit/Source/platform/audio/AudioProcessor.h:48:0
    #5 0x7fb8db063476 in blink::WaveShaperNode::WaveShaperNode(blink::BaseAudioContext&) third_party/WebKit/Source/modules/webaudio/WaveShaperNode.cpp:40:0
    #6 0x7fb8db063acb in blink::WaveShaperNode::Create(blink::BaseAudioContext&, blink::ExceptionState&) third_party/WebKit/Source/modules/webaudio/WaveShaperNode.cpp:54:14
    #7 0x7fb8da4080cb in createWaveShaperMethod /media/rtoy/ssd2/chromium-asan/src/out/Release/gen/blink/bindings/modules/v8/V8BaseAudioContext.cpp:408:34


Not quite sure how it's possible to be reconfiguring the WaveShaper processor (due to changing the channel count) and also be deleting the WaveShaper node.

The test case only connects a panner node (stereo) to the wave shaper.  The wave shaper default channel count is 2 and a mode of "max".  There shouldn't be any reconfiguration of the processor at all.


### rt...@chromium.org (2017-11-10)

Using a debug build produces the following message:

[77691:77691:1110/112446.679071:FATAL:ThreadingPthreads.cpp(141)] Check failed: result == 0 (16 vs. 0)
    #0 0x564941834cb1 in __interceptor_backtrace ??:0:0
    #1 0x7febaab0952a in base::debug::StackTrace::StackTrace(unsigned long) /media/rtoy/ssd2/chromium-asan/src/out/Debug/../../base/debug/stack_trace_posix.cc:801:41
    #2 0x7febaab030bc in base::debug::StackTrace::StackTrace() /media/rtoy/ssd2/chromium-asan/src/out/Debug/../../base/debug/stack_trace.cc:199:28
    #3 0x7febaac8383c in logging::LogMessage::~LogMessage() /media/rtoy/ssd2/chromium-asan/src/out/Debug/../../base/logging.cc:581:29
    #4 0x7feb8d01b277 in WTF::MutexBase::~MutexBase() /media/rtoy/ssd2/chromium-asan/src/out/Debug/../../third_party/WebKit/Source/platform/wtf/ThreadingPthreads.cpp:141:3
    #5 0x7feb642d3415 in WTF::Mutex::~Mutex() /media/rtoy/ssd2/chromium-asan/src/out/Debug/../../third_party/WebKit/Source/platform/wtf/ThreadingPrimitives.h:92:18
    #6 0x7feb64b96d5a in blink::AudioDSPKernelProcessor::~AudioDSPKernelProcessor() /media/rtoy/ssd2/chromium-asan/src/out/Debug/../../third_party/WebKit/Source/platform/audio/AudioDSPKernelProcessor.h:51:23
    #7 0x7feb64c52d03 in blink::WaveShaperProcessor::~WaveShaperProcessor() /media/rtoy/ssd2/chromium-asan/src/out/Debug/../../third_party/WebKit/Source/modules/webaudio/WaveShaperProcessor.cpp:41:1
    #8 0x7feb64c52d29 in blink::WaveShaperProcessor::~WaveShaperProcessor() /media/rtoy/ssd2/chromium-asan/src/out/Debug/../../third_party/WebKit/Source/modules/webaudio/WaveShaperProcessor.cpp:38:45
    #9 0x7feb649da443 in operator() /media/rtoy/ssd2/chromium-asan/src/out/Debug/../../buildtools/third_party/libc++/trunk/include/memory:2233:5
    #10 0x7feb649da443 in reset /media/rtoy/ssd2/chromium-asan/src/out/Debug/../../buildtools/third_party/libc++/trunk/include/memory:2546:0
    #11 0x7feb649da443 in ~unique_ptr /media/rtoy/ssd2/chromium-asan/src/out/Debug/../../buildtools/third_party/libc++/trunk/include/memory:2500:0
    #12 0x7feb649da443 in blink::AudioBasicProcessorHandler::~AudioBasicProcessorHandler() /media/rtoy/ssd2/chromium-asan/src/out/Debug/../../third_party/WebKit/Source/modules/webaudio/AudioBasicProcessorHandler.cpp:58:0
    #13 0x7feb649da859 in blink::AudioBasicProcessorHandler::~AudioBasicProcessorHandler() /media/rtoy/ssd2/chromium-asan/src/out/Debug/../../third_party/WebKit/Source/modules/webaudio/AudioBasicProcessorHandler.cpp:55:59
    #14 0x7feb649cde49 in void WTF::ThreadSafeRefCounted<blink::AudioHandler, WTF::DefaultThreadSafeRefCountedTraits<blink::AudioHandler> >::DeleteInternal<blink::AudioHandler>(blink::AudioHandler const*) /media/rtoy/ssd2/chromium-asan/src/out/Debug/../../third_party/WebKit/Source/platform/wtf/ThreadSafeRefCounted.h:64:5
    #15 0x7feb649cddc5 in WTF::DefaultThreadSafeRefCountedTraits<blink::AudioHandler>::Destruct(blink::AudioHandler const*) /media/rtoy/ssd2/chromium-asan/src/out/Debug/../../third_party/WebKit/Source/platform/wtf/ThreadSafeRefCounted.h:44:5
    #16 0x7feb649cdd9c in base::RefCountedThreadSafe<blink::AudioHandler, WTF::DefaultThreadSafeRefCountedTraits<blink::AudioHandler> >::Release() const /media/rtoy/ssd2/chromium-asan/src/out/Debug/../../base/memory/ref_counted.h:386:7
    #17 0x7feb649cdd59 in scoped_refptr<blink::AudioHandler>::Release(blink::AudioHandler*) /media/rtoy/ssd2/chromium-asan/src/out/Debug/../../base/memory/scoped_refptr.h:276:8
    #18 0x7feb649cc9e9 in scoped_refptr<blink::AudioHandler>::~scoped_refptr() /media/rtoy/ssd2/chromium-asan/src/out/Debug/../../base/memory/scoped_refptr.h:171:7
    #19 0x7feb649cff9a in blink::AudioNode::~AudioNode() /media/rtoy/ssd2/chromium-asan/src/out/Debug/../../third_party/WebKit/Source/modules/webaudio/AudioNode.h:307:22
    #20 0x7feb64c52515 in blink::WaveShaperNode::~WaveShaperNode() /media/rtoy/ssd2/chromium-asan/src/out/Debug/../../third_party/WebKit/Source/modules/webaudio/WaveShaperNode.h:40:7

Error code 16 is Device or resource busy.

### rt...@chromium.org (2017-11-10)

+haraken for help and/or further triage on how to deal with the pthread destruction while busy, as shown in c#8.

### ha...@chromium.org (2017-11-11)

When can it happen? i.e., why is Device or Resource busy?



### rt...@chromium.org (2017-11-13)

Based on the backtraces from clusterfuzz in c#7, I think this happens because an AudioNode is being collected, deleting the underlying AudioHandler as well, but the AudioHandler is still being processed and has the lock.

I don't understand how that can happen either; handlers normally outlive the parent node, by design.  More study/experimentation needed.

### mm...@chromium.org (2017-11-21)

Friendly ping from security sheriff. This is High severity vulnerability, and we aim to deploy the patch to all Chrome users in under 60 days (as per https://www.chromium.org/developers/severity-guidelines)

### cl...@chromium.org (2017-11-22)

ClusterFuzz testcase 5541958587252736 is flaky and no longer crashes, so closing issue.

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### [Deleted User] (2017-11-23)

Am I right in assuming this issue is now closed as WontFix? Just looking for a confirmation.

### [Deleted User] (2017-11-23)

I just tested this on asan-linux-release-518854 and it crashes with the same track trace. Just that it takes a bit longer now to crash.

### mm...@chromium.org (2017-11-30)

Re-opening the issue, as per c#15.

### mm...@chromium.org (2017-11-30)

I filed a https://crbug.com/chromium/789992 regarding the WontFix applied in c#13.

### cl...@chromium.org (2017-11-30)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6648990736318464.

### cl...@chromium.org (2017-11-30)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6272784115433472.

### mm...@chromium.org (2017-11-30)

Do you use any specific ASAN_OPTIONS ?

Do you open the testcase from a disk, or serve it via HTTP?

### [Deleted User] (2017-11-30)

You can browse to http://13.127.61.222/59b71abbf1096af7933c608b2bd84bf6abd13dbea37a469585f6d6b12342355d.html wait for 10-60 seconds and you'll get the 'Aww Snap'
with 
1. Chrome/Android 
2. Windows/Chrome Stable
3. Mac/Chrome Stable 

Also, I don't use any ASAN_OPTIONS and it works with either disk or HTTP. It crashes both ways. (I have tested this on multiple device I could find at home)

The reason I am me being persistent about this particular crash is because I have a couple of others, which I can't really reduce  easily. So, I can't really determine if these are duplicates.

Below are some sample stack traces:

BUG1
----
chrome_child.dll!blink::AudioDSPKernelProcessor::Initialize + 0x2D (id: f5a) [[c:\b\c\b\win64_pgo\src\third_party\webkit\source\platform\audio\audiodspkernelprocessor.cpp @ 50]]
chrome_child.dll!blink::AudioBasicProcessorHandler::Initialize + 0x1A (id: b38) [[c:\b\c\b\win64_pgo\src\third_party\webkit\source\modules\webaudio\audiobasicprocessorhandler.cpp @ 67]]
chrome_child.dll!blink::AudioBasicProcessorHandler::CheckNumberOfChannelsForInput + 0x7C [[c:\b\c\b\win64_pgo\src\third_party\webkit\source\modules\webaudio\audiobasicprocessorhandler.cpp @ 147]]
chrome_child.dll!blink::AudioSummingJunction::UpdateRenderingState + 0xD5 [[c:\b\c\b\win64_pgo\src\third_party\webkit\source\modules\webaudio\audiosummingjunction.cpp @ 61]]
chrome_child.dll!blink::DeferredTaskHandler::HandleDirtyAudioSummingJunctions + 0x76 [[c:\b\c\b\win64_pgo\src\third_party\webkit\source\modules\webaudio\deferredtaskhandler.cpp @ 120]]
[snip]

chrome_child!blink::AudioDSPKernelProcessor::Initialize+0x2d:
00007ffe`866e3f8d ff5038          call    qword ptr [rax+38h] ds:d0cba4f4`f3020038=????????????????

BUG2
----
chrome_child.dll!blink::AudioHandler::IsInitialized (inlined function, id: 8d6) [[c:\b\c\b\win64_pgo\src\third_party\webkit\source\modules\webaudio\audionode.h @ 162]]
chrome_child.dll!blink::AudioHandler::ProcessIfNecessary + 0xA (id: 510) [[c:\b\c\b\win64_pgo\src\third_party\webkit\source\modules\webaudio\audionode.cpp @ 311]]
chrome_child.dll!blink::AudioNodeOutput::Pull + 0x61 [[c:\b\c\b\win64_pgo\src\third_party\webkit\source\modules\webaudio\audionodeoutput.cpp @ 141]]
chrome_child.dll!blink::AudioNodeInput::SumAllConnections + 0x5F [[c:\b\c\b\win64_pgo\src\third_party\webkit\source\modules\webaudio\audionodeinput.cpp @ 194]]
[snip]

chrome_child!blink::AudioHandler::IsInitialized [inlined in chrome_child!blink::AudioHandler::ProcessIfNecessary+0xa]:
00007ff9`a2b9ac6a 8a410c          mov     al,byte ptr [rcx+0Ch] ds:48b934e4`b401000c=??

BUG3
----
chrome_child.dll!blink::BaseAudioContext::currentTime + 0x9 (id: 036) [[c:\b\c\b\win64_pgo\src\third_party\webkit\source\modules\webaudio\baseaudiocontext.h @ 141]]
chrome_child.dll!blink::AudioHandler::ProcessIfNecessary + 0x2E (id: 510) [[c:\b\c\b\win64_pgo\src\third_party\webkit\source\modules\webaudio\audionode.cpp @ 320]]
chrome_child.dll!blink::DeferredTaskHandler::ProcessAutomaticPullNodes + 0x32 [[c:\b\c\b\win64_pgo\src\third_party\webkit\source\modules\webaudio\deferredtaskhandler.cpp @ 169]]
chrome_child.dll!blink::AudioDestinationHandler::Render + 0x141 [[c:\b\c\b\win64_pgo\src\third_party\webkit\source\modules\webaudio\audiodestinationnode.cpp @ 108]]
[snip]

chrome_child!blink::BaseAudioContext::currentTime+0x9:
00007ffd`d45605e1 488b4958        mov     rcx,qword ptr [rcx+58h] ds:70616c72`65766f78=????????????????

BUG4
----
chrome_child.dll!blink::AudioHandler::ProcessIfNecessary + 0x23 (id: 510) [[c:\b\c\b\win64_pgo\src\third_party\webkit\source\modules\webaudio\audionode.cpp @ 319]]
chrome_child.dll!blink::AudioNodeOutput::Pull + 0x61 (id: e93) [[c:\b\c\b\win64_pgo\src\third_party\webkit\source\modules\webaudio\audionodeoutput.cpp @ 141]]
chrome_child.dll!blink::AudioNodeInput::SumAllConnections + 0x5F [[c:\b\c\b\win64_pgo\src\third_party\webkit\source\modules\webaudio\audionodeinput.cpp @ 194]]
chrome_child.dll!blink::AudioNodeInput::Pull + 0x4D [[c:\b\c\b\win64_pgo\src\third_party\webkit\source\modules\webaudio\audionodeinput.cpp @ 223]]
[snip]

chrome_child!blink::AudioHandler::ProcessIfNecessary+0x23:
00007ff8`4eacac83 ff5010          call    qword ptr [rax+10h] ds:00007ff8`4eaca0c0=0574c9854860498b

Here is a google drive link with for the unreduced testcases https://drive.google.com/file/d/187B7prc9aEF2SQFL8wOt0uEF80xvIiLL/view?usp=sharing 
Password for the file is zaMNhL5x8Sy69B7n

### mm...@chromium.org (2017-11-30)

Thanks for the additional details. It looks like we can reproduce your crashes, but not reliably. How often does it reproduce for you?

Also, you said we need to wait 10-60 seconds. Do you expect that 60 seconds is the top boundary and it would be always enough to crash?

I'm just trying to find a way to reliably reproduce those on ClusterFuzz, then we'll get de-duplication for free and make life of our developers easier as well.

### cl...@chromium.org (2017-11-30)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5099386433699840.

### cl...@chromium.org (2017-11-30)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5544130028765184.

### cl...@chromium.org (2017-11-30)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6571000874663936.

### cl...@chromium.org (2017-11-30)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5796676790124544.

### cl...@chromium.org (2017-11-30)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5788608425623552.

### rt...@chromium.org (2017-11-30)

I can reproduce this locally on my linux machine with ToT from this
morning, using the original DSP_UAF.html test.  A crash happens in
about 10-15 sec or so.

However, when I add a few debugging printfs, this no longer happens,
even after a few minutes of running.

This is going to take quite a bit of time to understand and fix.


### [Deleted User] (2017-11-30)

Max, I think 60 should do for the upperlimit (I reduced the DSP_UAF.html using 30) on Stable non ASAN builds. But it takes considerably longer on ASAN builds to reduce, I kinda skipped that part.

### rt...@chromium.org (2017-11-30)

Adding one fprintf in ~AudioBasicProcessorHandler makes the problem go away. :-(

### sh...@chromium.org (2017-12-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-12-07)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-12-15)

rtoy: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2017-12-30)

rtoy: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-01-02)

We commit ourselves to a 60 day deadline for fixing for high severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rt...@chromium.org (2018-01-05)

Clusterfuzz can't reproduce this, and after updating to ToT, the repro case takes much longer to reproduce (on linux).


### rt...@chromium.org (2018-01-08)

This seems to be not reproducible (or at least very hard).  I let the test case run over the weekend, using ToT from Friday morning. It's still running 2+ days later.


### rt...@chromium.org (2018-01-10)

For whatever reason, this started reproducing pretty reliably this
week on my linux machine.  Fix is being reviewed.

The problem is that a node (WaveShaper) is being processed by the
audio graph due to a change in the number of channels to it's input.
However, the owning AudioNode is getting collected while this is
happening.  This deletes the AudioHandler (because the AudioNode is
the only reference), causing the WaveShaper handler and associated
members to disappear while the audio thread is touching it.

The solution is that when the AudioNode is being collected, add its
handler to the orphan handler list.  This keeps the handler alive.
When the audio thread is finished rendering, item on the orphan list
are collected, causing the handlers to go away safely.

With the fix the test case ran over night without crashing. (It was
reliably crashing the last few days.)


### bu...@chromium.org (2018-01-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/378072c18b481665b71c4d6718f4e507896695b0

commit 378072c18b481665b71c4d6718f4e507896695b0
Author: Raymond Toy <rtoy@chromium.org>
Date: Wed Jan 10 20:17:35 2018

Keep AudioHandlers alive until they can be safely deleted.

When an AudioNode is disposed, the handler is also disposed.  But add
the handler to the orphan list so that the handler stays alive until
the context can safely delete it.  If we don't do this, the handler
may get deleted while the audio thread is processing the handler (due
to, say, channel count changes and such).

Because of this change, handlers don't go away immediately in an
offline context.  The handlers will only go away when rendering is
started or when the context itself is GCed.  Update
cycle-connection-gc.html test to start rendering.  And add a new test,
cycle-connection-gc-render.html, to verify that the handlers are
collected when the context is collected.

Bug: 780919
Test: cycle-connection-gc.html, cycle-connection-gc-render.html
Change-Id: Ibb7c46d5727ddb9f8dec4c48cb5cfebebb4144b3
Reviewed-on: https://chromium-review.googlesource.com/858230
Commit-Queue: Raymond Toy <rtoy@chromium.org>
Reviewed-by: Hongchan Choi <hongchan@chromium.org>
Cr-Commit-Position: refs/heads/master@{#528406}
[add] https://crrev.com/378072c18b481665b71c4d6718f4e507896695b0/third_party/WebKit/LayoutTests/webaudio/internals/cycle-connection-gc-render-expected.txt
[add] https://crrev.com/378072c18b481665b71c4d6718f4e507896695b0/third_party/WebKit/LayoutTests/webaudio/internals/cycle-connection-gc-render.html
[modify] https://crrev.com/378072c18b481665b71c4d6718f4e507896695b0/third_party/WebKit/LayoutTests/webaudio/internals/cycle-connection-gc.html
[modify] https://crrev.com/378072c18b481665b71c4d6718f4e507896695b0/third_party/WebKit/Source/modules/webaudio/AudioNode.cpp


### bu...@chromium.org (2018-01-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/f88fdc177092bb375d7f1a38a70a23f8e14abc03

commit f88fdc177092bb375d7f1a38a70a23f8e14abc03
Author: Alexei Filippov <alph@chromium.org>
Date: Wed Jan 10 22:05:24 2018

Revert "Keep AudioHandlers alive until they can be safely deleted."

This reverts commit 378072c18b481665b71c4d6718f4e507896695b0.

Reason for revert:
Broke tests https://ci.chromium.org/buildbot/chromium.webkit/WebKit%20Linux%20Trusty%20Leak/14197

Original change's description:
> Keep AudioHandlers alive until they can be safely deleted.
> 
> When an AudioNode is disposed, the handler is also disposed.  But add
> the handler to the orphan list so that the handler stays alive until
> the context can safely delete it.  If we don't do this, the handler
> may get deleted while the audio thread is processing the handler (due
> to, say, channel count changes and such).
> 
> Because of this change, handlers don't go away immediately in an
> offline context.  The handlers will only go away when rendering is
> started or when the context itself is GCed.  Update
> cycle-connection-gc.html test to start rendering.  And add a new test,
> cycle-connection-gc-render.html, to verify that the handlers are
> collected when the context is collected.
> 
> Bug: 780919
> Test: cycle-connection-gc.html, cycle-connection-gc-render.html
> Change-Id: Ibb7c46d5727ddb9f8dec4c48cb5cfebebb4144b3
> Reviewed-on: https://chromium-review.googlesource.com/858230
> Commit-Queue: Raymond Toy <rtoy@chromium.org>
> Reviewed-by: Hongchan Choi <hongchan@chromium.org>
> Cr-Commit-Position: refs/heads/master@{#528406}

TBR=rtoy@chromium.org,hongchan@chromium.org

Change-Id: If0fdce08057d3e624b6cd56b958fb753d89fb672
No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Bug: 780919
Reviewed-on: https://chromium-review.googlesource.com/860779
Reviewed-by: Alexei Filippov <alph@chromium.org>
Commit-Queue: Alexei Filippov <alph@chromium.org>
Cr-Commit-Position: refs/heads/master@{#528441}
[delete] https://crrev.com/e65d6289cd28260dcd05078ffd49ebdd8e8dbf77/third_party/WebKit/LayoutTests/webaudio/internals/cycle-connection-gc-render-expected.txt
[delete] https://crrev.com/e65d6289cd28260dcd05078ffd49ebdd8e8dbf77/third_party/WebKit/LayoutTests/webaudio/internals/cycle-connection-gc-render.html
[modify] https://crrev.com/f88fdc177092bb375d7f1a38a70a23f8e14abc03/third_party/WebKit/LayoutTests/webaudio/internals/cycle-connection-gc.html
[modify] https://crrev.com/f88fdc177092bb375d7f1a38a70a23f8e14abc03/third_party/WebKit/Source/modules/webaudio/AudioNode.cpp


### bu...@chromium.org (2018-01-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/071df33edf2c8b4375fa432a83953359f93ea9e4

commit 071df33edf2c8b4375fa432a83953359f93ea9e4
Author: Raymond Toy <rtoy@chromium.org>
Date: Fri Jan 12 00:34:43 2018

Keep AudioHandlers alive until they can be safely deleted.

When an AudioNode is disposed, the handler is also disposed.  But add
the handler to the orphan list so that the handler stays alive until
the context can safely delete it.  If we don't do this, the handler
may get deleted while the audio thread is processing the handler (due
to, say, channel count changes and such).

For an realtime context, always save the handler just in case the
audio thread is running after the context is marked as closed (because
the audio thread doesn't instantly stop when requested).

For an offline context, only need to do this when the context is
running because the context is guaranteed to be stopped if we're not
in the running state.  Hence, there's no possibility of deleting the
handler while the graph is running.

This is a revert of
https://chromium-review.googlesource.com/c/chromium/src/+/860779, with
a fix for the leak.

Bug: 780919
Change-Id: Ifb6b5fcf3fbc373f5779256688731245771da33c
Reviewed-on: https://chromium-review.googlesource.com/862723
Reviewed-by: Hongchan Choi <hongchan@chromium.org>
Commit-Queue: Raymond Toy <rtoy@chromium.org>
Cr-Commit-Position: refs/heads/master@{#528829}
[modify] https://crrev.com/071df33edf2c8b4375fa432a83953359f93ea9e4/third_party/WebKit/Source/modules/webaudio/AudioNode.cpp


### bu...@chromium.org (2018-01-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/fd6a5115103b3e6a52ce15858c5ad4956df29300

commit fd6a5115103b3e6a52ce15858c5ad4956df29300
Author: Taiju Tsuiki <tzik@chromium.org>
Date: Fri Jan 12 05:42:54 2018

Revert "Keep AudioHandlers alive until they can be safely deleted."

This reverts commit 071df33edf2c8b4375fa432a83953359f93ea9e4.

Reason for revert:
This CL seems to cause an AudioNode leak on the Linux leak bot.
The log is:
https://ci.chromium.org/buildbot/chromium.webkit/WebKit%20Linux%20Trusty%20Leak/14252
* webaudio/AudioNode/audionode-connect-method-chaining.html
* webaudio/Panner/pannernode-basic.html
* webaudio/dom-exceptions.html

Original change's description:
> Keep AudioHandlers alive until they can be safely deleted.
> 
> When an AudioNode is disposed, the handler is also disposed.  But add
> the handler to the orphan list so that the handler stays alive until
> the context can safely delete it.  If we don't do this, the handler
> may get deleted while the audio thread is processing the handler (due
> to, say, channel count changes and such).
> 
> For an realtime context, always save the handler just in case the
> audio thread is running after the context is marked as closed (because
> the audio thread doesn't instantly stop when requested).
> 
> For an offline context, only need to do this when the context is
> running because the context is guaranteed to be stopped if we're not
> in the running state.  Hence, there's no possibility of deleting the
> handler while the graph is running.
> 
> This is a revert of
> https://chromium-review.googlesource.com/c/chromium/src/+/860779, with
> a fix for the leak.
> 
> Bug: 780919
> Change-Id: Ifb6b5fcf3fbc373f5779256688731245771da33c
> Reviewed-on: https://chromium-review.googlesource.com/862723
> Reviewed-by: Hongchan Choi <hongchan@chromium.org>
> Commit-Queue: Raymond Toy <rtoy@chromium.org>
> Cr-Commit-Position: refs/heads/master@{#528829}

TBR=rtoy@chromium.org,hongchan@chromium.org

Change-Id: Ibf406bf6ed34ea1f03e86a64a1e5ba6de0970c6f
No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Bug: 780919
Reviewed-on: https://chromium-review.googlesource.com/863402
Reviewed-by: Taiju Tsuiki <tzik@chromium.org>
Commit-Queue: Taiju Tsuiki <tzik@chromium.org>
Cr-Commit-Position: refs/heads/master@{#528888}
[modify] https://crrev.com/fd6a5115103b3e6a52ce15858c5ad4956df29300/third_party/WebKit/Source/modules/webaudio/AudioNode.cpp


### es...@chromium.org (2018-01-17)

Friendly ping from the security sheriff -- any progress on getting the CL relanded?

### rt...@chromium.org (2018-01-17)

I have a new CL where I think I've fixed the leaks.  Waiting for leak bot to confirm my local results.

### rt...@chromium.org (2018-01-18)

Leak bot says no leaks.

@estark: Should I wait until after the M65 branch that's coming up soon? I think I'd prefer to let it back on canary for a bit and merge back to M65 (and earlier, if needed).

### es...@chromium.org (2018-01-18)

It should be okay to wait as long as it does get merged back to 65. Thanks for the fix!

### bu...@chromium.org (2018-01-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/ebcf9595bf908b515ffcd31374b071697a69faed

commit ebcf9595bf908b515ffcd31374b071697a69faed
Author: Raymond Toy <rtoy@chromium.org>
Date: Mon Jan 22 17:03:07 2018

Keep AudioHandlers alive until they can be safely deleted.

When an AudioNode is disposed, the handler is also disposed.  But add
the handler to the orphan list so that the handler stays alive until
the context can safely delete it.  If we don't do this, the handler
may get deleted while the audio thread is processing the handler (due
to, say, channel count changes and such).

For an realtime context, save the handler if the context is not closed.
(Nothing will clean up the handler if the context is closed.)

For an offline context, only need to do this when the context is
running because the context is guaranteed to be stopped if we're not
in the running state.  Hence, there's no possibility of deleting the
handler while the graph is running.

Bug: 780919
Change-Id: Id8ba47f48504c5681121facebfc5acb85b05de87
Reviewed-on: https://chromium-review.googlesource.com/868841
Reviewed-by: Hongchan Choi <hongchan@chromium.org>
Commit-Queue: Raymond Toy <rtoy@chromium.org>
Cr-Commit-Position: refs/heads/master@{#530892}
[modify] https://crrev.com/ebcf9595bf908b515ffcd31374b071697a69faed/third_party/WebKit/Source/modules/webaudio/AudioNode.cpp


### rt...@chromium.org (2018-01-23)

Ran this fix overnight with an linux asan build.  No crashes.

I'm going to let this bake on canary for a few more days and request a merge to 65 then.

### sh...@chromium.org (2018-01-25)

[Empty comment from Monorail migration]

### rt...@chromium.org (2018-01-29)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-01-29)

This bug requires manual review: Reverts referenced in bugdroid comments after merge request.
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), bhthompson@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2018-01-29)

+awhalley@ (Security TPM) for M65 merge review.

Also is this need a merge to M64? If yes, please request a merge to M64. Thank you.

### rt...@chromium.org (2018-01-29)

Yes, this will probably need to go to M64 as well.  I'll request that after the M65 merge (if approved).

### go...@chromium.org (2018-01-29)

Approving merge to M65 branch 3325 per offline chat with awhalley@. 

### go...@chromium.org (2018-01-30)

Pls merge your change to M65 branch 3325 ASAP so we can pick it up for next M65 dev release. Thank you.

### bu...@chromium.org (2018-01-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/e1cef84dd8817fb952a9a07a7d085ee678d6d08e

commit e1cef84dd8817fb952a9a07a7d085ee678d6d08e
Author: Raymond Toy <rtoy@chromium.org>
Date: Tue Jan 30 19:23:36 2018

Keep AudioHandlers alive until they can be safely deleted.

When an AudioNode is disposed, the handler is also disposed.  But add
the handler to the orphan list so that the handler stays alive until
the context can safely delete it.  If we don't do this, the handler
may get deleted while the audio thread is processing the handler (due
to, say, channel count changes and such).

For an realtime context, save the handler if the context is not closed.
(Nothing will clean up the handler if the context is closed.)

For an offline context, only need to do this when the context is
running because the context is guaranteed to be stopped if we're not
in the running state.  Hence, there's no possibility of deleting the
handler while the graph is running.

Bug: 780919
Change-Id: Id8ba47f48504c5681121facebfc5acb85b05de87
Reviewed-on: https://chromium-review.googlesource.com/868841
Reviewed-by: Hongchan Choi <hongchan@chromium.org>
Commit-Queue: Raymond Toy <rtoy@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#530892}(cherry picked from commit ebcf9595bf908b515ffcd31374b071697a69faed)
Reviewed-on: https://chromium-review.googlesource.com/893626
Reviewed-by: Raymond Toy <rtoy@chromium.org>
Cr-Commit-Position: refs/branch-heads/3325@{#180}
Cr-Branched-From: bc084a8b5afa3744a74927344e304c02ae54189f-refs/heads/master@{#530369}
[modify] https://crrev.com/e1cef84dd8817fb952a9a07a7d085ee678d6d08e/third_party/WebKit/Source/modules/webaudio/AudioNode.cpp


### rt...@chromium.org (2018-01-30)

Requesting merge to M64, but I'll let it bake on M65 for a day or so.

### sh...@chromium.org (2018-01-30)

This bug requires manual review: Request affecting a post-stable build
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), kbleicher@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ab...@chromium.org (2018-01-30)

Why is this critical for M64? We need to ensure we only take absolutely critical merges in since M64 is already ramping up to stable.

### rt...@chromium.org (2018-01-30)

I will have to defer to the security team on how critical this is.

estark@ WDYT?

### aw...@google.com (2018-01-31)

Giving what's going on with M64 right now, we can keep this in 65.

### ab...@chromium.org (2018-01-31)

Rejecting merge for M64. 

### rt...@chromium.org (2018-01-31)

Clusterfuzz can't reproduce this, but as best as I can tell with a local build, this no longer produces.

Closing.

### aw...@google.com (2018-02-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-02-08)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-02-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-02-09)

Nice one omair@ - the VRP panel decided to award $3,000 for this report!

### aw...@google.com (2018-02-09)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-03-06)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-03-06)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-05-10)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@google.com (2018-11-14)

[Empty comment from Monorail migration]

### is...@google.com (2018-11-14)

This issue was migrated from crbug.com/chromium/780919?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

### ti...@chromium.org (2024-06-27)

Adding `ClusterFuzz-Ignore` hotlist to all `ClusterFuzz-Wrong` issues per crbug.com/40285975.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40089489)*
