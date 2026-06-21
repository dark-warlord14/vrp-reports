# NaN poisoning in k-rate SetValueCurve leads to out-of-bounds read in DelayNode

| Field | Value |
|-------|-------|
| **Issue ID** | [490533968](https://issues.chromium.org/issues/490533968) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Blink>WebAudio |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | je...@gmail.com |
| **Assignee** | mj...@chromium.org |
| **Created** | 2026-03-07 |
| **Bounty** | $2,000.00 |

## Description

# NaN poisoning in k-rate SetValueCurve leads to out-of-bounds read in DelayNode

## Summary

A crafted `setValueCurveAtTime` call on a k-rate `DelayNode.delayTime` AudioParam can produce a NaN delay value that propagates unchecked through `Delay::ProcessKRate`, causing `static_cast<int>(NaN)` to yield `INT_MIN` on x86/x64. This results in a massive out-of-bounds memory read (approximately 8 GB before the ring buffer), crashing the renderer process. The vulnerability affects all desktop platforms (Linux, macOS, Windows) on x86/x64 architectures.

## Root Cause

When `AudioParam::setValueCurveAtTime(curve, startTime, duration)` is called, the event creation code pre-computes the curve sampling rate as a per-second value:

```
// audio_param_handler.cc — CreateSetValueCurveEvent
double curve_points = (curve.size() - 1) / duration;

```

This computation runs on the main thread, where IEEE 754 subnormal handling is standard. If `duration` is a normal double just above `DBL_MIN` (approximately 2.225e-308) and the curve has enough points, the division overflows to positive infinity. For instance, a 6-element curve with `duration = 2.3e-308` produces `5 / 2.3e-308 ≈ 2.17e308`, which exceeds `DBL_MAX` and becomes `+inf`. The event stores this infinite `CurvePointsPerSecond` without any validation; the only checks on the event fields are `DCHECK(std::isfinite(...))` assertions that are compiled out in release builds.

The vulnerability manifests during audio rendering on the audio thread, which runs with x86 MXCSR flags DAZ (Denormals Are Zero) and FTZ (Flush To Zero) enabled for performance. The key property of the chosen `duration` is that it must be a normal (non-subnormal) double so that the audio thread does not flush it to zero when computing frame coverage. With `duration = 2.3e-308`, the product `sampleRate * duration = 48000 * 2.3e-308 ≈ 1.1e-303` is a normal double, and `ceil(1.1e-303) = 1`, meaning the SetValueCurve event covers exactly one audio frame. This allows the event's processing loop to execute.

Inside `ProcessSetValueCurve`, the scalar fallback path computes a virtual curve index for each frame:

```
// audio_param_handler.cc — ProcessSetValueCurve, scalar loop
double current_virtual_index =
    curve_virtual_index + k * curve_points_per_frame;

```

On the first iteration (`k = 0`) with `curve_virtual_index = 0` and `curve_points_per_frame = +inf`, IEEE 754 arithmetic produces `0 * inf = NaN`. The subsequent clamping of the curve index uses comparison operators that propagate NaN:

```
// audio_param_handler.cc — ProcessSetValueCurve, scalar loop
double delta = std::min(current_virtual_index - curve_index0, 1.0);

```

Since `std::min` uses `operator<` and NaN comparisons return false, the NaN survives as `delta`. The interpolated value `c0 + (c1 - c0) * NaN` evaluates to NaN because any arithmetic with NaN produces NaN.

The a-rate (sample-accurate) path is protected against NaN through `HandleNaNValues()` in `CalculateFinalValues`, but the k-rate path through `FinalValue()` and `ValueForContextTime()` lacks this protection entirely. After `ValuesForFrameRangeImpl` returns the NaN value, it passes through `Vclip` with a single-element span, which takes the scalar code path using `ClampTo()`. The `ClampTo` implementation in `math_extras.h` relies on comparison operators:

```
// math_extras.h — ClampToDirectComparison
if (value >= max) return max;
if (value <= min) return min;
return value;

```

Both comparisons against NaN evaluate to false, so the NaN value is returned unchanged. A `DCHECK(!__builtin_isnan(...))` guard exists but is absent in release builds.

The NaN delay value then enters `Delay::ProcessKRate`, where it passes through another `ClampTo` call unimpeded, and is converted to a buffer index:

```
// delay.cc — ProcessKRate
double delay_time = DelayTime(sample_rate);
delay_time = ClampTo(delay_time, 0.0, max_time);
double desired_delay_frames = delay_time * sample_rate;
double read_position = w_index + buffer_length - desired_delay_frames;
int read_index1 = static_cast<int>(read_position);
float* read_pointer = &buffer[read_index1];
memcpy(sample1, read_pointer, sizeof(*sample1) * std::min(frames_to_process, remainder));

```

On x86/x64, `static_cast<int>(NaN)` compiles to `cvttsd2si`, which returns `INT_MIN` (0x80000000) for NaN inputs. This produces `read_index1 = -2147483648`, causing the subsequent pointer arithmetic and `memcpy` to read approximately 8 GB before the start of the ring buffer. The access lands in unmapped memory, producing a `SEGV_MAPERR` signal.

## Reproduce

To reproduce this issue, check out Chromium at commit `e256102970bf347f2cc827935dbcb09ee18a3b60` and configure an ASAN release build. Place the following in `out/asan-release/args.gn`:

```
is_debug = false
is_asan = true
is_component_build = true
symbol_level = 1

```

Build Chrome with `autoninja -C out/asan-release chrome`. No source patches are required.

Copy `poc.html` from this directory to the Chromium source root `~/chromium/src/poc.html`, then launch Chrome with ASAN:

```
ASAN_OPTIONS=detect_odr_violation=0 \
  xvfb-run -a out/asan-release/chrome \
  --no-sandbox --disable-gpu \
  --user-data-dir=/tmp/poc-test \
  poc.html

```

On headless servers, `xvfb-run -a` provides a virtual display. The renderer process will crash within a few seconds with `Received signal 11 SEGV_MAPERR`, confirming an out-of-bounds memory read from inside `blink::Delay::ProcessKRate`. The crash address will be approximately 8 GB before the delay line ring buffer, which is the result of `static_cast<int>(NaN)` producing `INT_MIN` (0x80000000) as a buffer index on x86/x64. The crash log in `asan.log` contains the full stack trace and register dump.

### Crash Log

```
Received signal 11 SEGV_MAPERR 7b9950013800
#0 0x55f29ae6f046 ___interceptor_backtrace
#1 0x7f9bdad5f3e2 base::debug::CollectStackTrace                                base/debug/stack_trace_posix.cc:1048
#2 0x7f9bdad04c53 base::debug::StackTrace::StackTrace                            base/debug/stack_trace.cc:280
#3 0x7f9bdad5e67b base::debug::StackDumpSignalHandler                            base/debug/stack_trace_posix.cc:483
#4 0x7f9b6a242520 (signal handler)
#5 0x7f9b6a2c4881 memcpy                                                         memmove-vec-unaligned-erms.S:220
#6 0x55f29aec727c __asan_memcpy
#7 0x7f9b7f23d4cc blink::Delay::ProcessKRate                                     delay.cc:268
#8 0x7f9b72903999 blink::DelayHandler::Process                                   delay_handler.cc:84
#9 0x7f9b7283a8fe blink::AudioHandler::ProcessIfNecessary                        audio_handler.cc:331
#10 0x7f9b7285c7c6 blink::AudioNodeOutput::Pull                                  audio_node_output.cc:135
#11 0x7f9b7285995c blink::AudioNodeInput::SumAllConnections                      audio_node_input.cc:132
#12 0x7f9b72859de6 blink::AudioNodeInput::Pull                                   audio_node_input.cc:162
#13 0x7f9b7293900c blink::OfflineAudioDestinationHandler::RenderIfNotSuspended   offline_audio_destination_handler.cc:304
#14 0x7f9b72937b02 blink::OfflineAudioDestinationHandler::DoOfflineRendering     offline_audio_destination_handler.cc:188
#15 0x7f9b7293a2ad base::internal::Invoker<...>::RunOnce                         bind_internal.h:740
#16 0x7f9bdab614f3 base::TaskAnnotator::RunTaskImpl                              callback.h:155
#17 0x7f9bdabe29df ThreadControllerWithMessagePumpImpl::DoWorkImpl               task_annotator.h:112
#18 0x7f9bdabe19b7 ThreadControllerWithMessagePumpImpl::DoWork                   thread_controller_with_message_pump_impl.cc:346
#19 0x7f9bdaa03592 base::MessagePumpDefault::Run                                 message_pump_default.cc:42
#20 0x7f9bdabe4059 ThreadControllerWithMessagePumpImpl::Run                      thread_controller_with_message_pump_impl.cc:650
#21 0x7f9bdaacbb53 base::RunLoop::Run                                           run_loop.cc:135
#22 0x7f9b8007000d blink::scheduler::NonMainThreadImpl::SimpleThreadImpl::Run    non_main_thread_impl.cc:178
#23 0x7f9bdacde6fd base::ThreadFunc                                              platform_thread_posix.cc:102
#24 0x55f29aec7137 asan_thread_start
#25 0x7f9b6a294ac3 start_thread                                                  pthread_create.c:442
#26 0x7f9b6a326850 clone3                                                        clone3.S:81
  r8: 00000f9feb863b30  r9: 0000000000000008 r10: 0000000000000008 r11: 0000000000000000
 r12: 00007b9950013800 r13: 00000000000001bf r14: 0000000000000200 r15: 00007b9950013800
  di: 00007cfb5c35d780  si: 00007b9950013800  bp: 00007b9a92d7ad30  bx: 00007cfb5c35d780
  dx: 0000000000000200  ax: 00007cfb5c35d780  cx: 00000f9feb863af0  sp: 00007b9a92d7a4e8
  ip: 00007f9b6a2c4881 efl: 0000000000010206 cgf: 002b000000000033 erf: 0000000000000004
 trp: 000000000000000e msk: 0000000000000000 cr2: 00007b9950013800
[end of stack trace]

```
## Credit

Please use c6eed09fc8b174b0f3eebedcceb1e792 as the credit for this vulnerability. Thank you.

## Attachments

- [poc.html](attachments/poc.html) (text/html, 2.5 KB)
- [asan.log](attachments/asan.log) (text/plain, 3.1 KB)

## Timeline

### cl...@appspot.gserviceaccount.com (2026-03-08)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6049124012982272.

### 24...@project.gserviceaccount.com (2026-03-08)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the hotlistid:4801165.

### 24...@project.gserviceaccount.com (2026-03-08)

Automatically assigning owner based on suspected regression changelist https://chromium.googlesource.com/chromium/src/+/01b317e407ea1508075a46b80094a8a49c2080e1 (Rename AudioDelayDSPKernel to Delay

This will make it more clear that this class implements the delay
line internals.

Braces {} were added automatically by git cl format when the files
were renamed.

Bug: 954523
Change-Id: I232508e27f53ac20b928ae16f6ceb4d37dd5b2bc
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4470258
Reviewed-by: Kentaro Hara <haraken@chromium.org>
Reviewed-by: Hongchan Choi <hongchan@chromium.org>
Commit-Queue: Michael Wilson <mjwilson@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1136836}
).

If this is incorrect, please let us know why and apply the hotlistid:5433122. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### 24...@project.gserviceaccount.com (2026-03-08)

Detailed Report: https://clusterfuzz.com/testcase?key=6049124012982272

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: UNKNOWN READ
Crash Address: 0x79eb74bff800
Crash State:
  blink::Delay::ProcessKRate
  blink::DelayHandler::Process
  blink::AudioHandler::ProcessIfNecessary
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1136835:1136855

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6049124012982272

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary.

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


A recommended severity was added to this bug. Please change the severity if it is inaccurate.

### ch...@google.com (2026-03-09)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-03-09)

Setting Priority to P1 to match Severity s1. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### mj...@chromium.org (2026-03-09)

[#comment4](https://issues.chromium.org/issues/490533968#comment4) The suspected regression was just renaming classes, so it obfuscates the root cause which is probably older. I will need to investigate a bit.

### mj...@chromium.org (2026-03-09)

Fix in progress here: <https://crrev.com/c/7649841>

### dx...@google.com (2026-03-10)

Project: chromium/src  

Branch:  main  

Author:  Michael Wilson [mjwilson@chromium.org](mailto:mjwilson@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7649841>

Replace UNSAFE\_TODO in Delay with safe operations

---


Expand for full commit details
```
     
    This should cause no functional change. 
     
    It also required updating call sites to use span instead of pointers. 
     
    Bug: 401184803 
    Bug: 490533968 
    Change-Id: I13fd424ea4fa7cc679a5206ecb5ee7dd67c025e1 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7649841 
    Reviewed-by: Hongchan Choi <hongchan@chromium.org> 
    Commit-Queue: Michael Wilson <mjwilson@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1597393}

```

---

Files:

- M `third_party/blink/renderer/modules/webaudio/delay_handler.cc`
- M `third_party/blink/renderer/platform/audio/cpu/arm/delay_neon.cc`
- M `third_party/blink/renderer/platform/audio/cpu/x86/delay_sse2.cc`
- M `third_party/blink/renderer/platform/audio/delay.cc`
- M `third_party/blink/renderer/platform/audio/delay.h`
- M `third_party/blink/renderer/platform/audio/hrtf_panner.cc`

---

Hash: [b05c9128c8aa84f028bc336d899ac6c852622429](https://chromiumdash.appspot.com/commit/b05c9128c8aa84f028bc336d899ac6c852622429)  

Date: Tue Mar 10 23:19:05 2026


---

### 24...@project.gserviceaccount.com (2026-03-11)

ClusterFuzz testcase 6049124012982272 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1597392:1597393

If this is incorrect, please add the hotlistid:5433040 and re-open the issue.

### ch...@google.com (2026-03-11)

Security Merge Request Consideration: Requesting merge to stable (M146) because latest trunk commit (1597393) appears to be after stable branch point (1582197).
Security Merge Request Consideration: Requesting merge to dev (M147) because latest trunk commit (1597393) appears to be after dev branch point (1596535).
Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### ch...@google.com (2026-03-11)

**Merge approved:** your change passed merge requirements and is auto-approved for M147. Please go ahead and merge the CL to branch 7727 (refs/branch-heads/7727) manually. Please contact milestone owner if you have questions.
Merge instructions: <https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md>
Owners: alonbajayo (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), harrysouders (Mobile US), eakpobaro (Mobile EMEA)

### ch...@google.com (2026-03-11)

Merge review required: M146 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: lmenezes (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), govind (Mobile US), eakpobaro (Mobile EMEA)

### dr...@chromium.org (2026-03-12)

No crashes in Canary, approved.

### mj...@chromium.org (2026-03-16)

M147 merge is failing tests, and I'm not sure why. M146 merge looks good so far.

### ch...@google.com (2026-03-17)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### mj...@chromium.org (2026-03-17)

M147 now passing, it seems like it was transient / infra errors. Both merges are now in review.

### dx...@google.com (2026-03-18)

Project: chromium/src  

Branch:  refs/branch-heads/7680  

Author:  Michael Wilson [mjwilson@chromium.org](mailto:mjwilson@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7667424>

[M146] Replace UNSAFE\_TODO in Delay with safe operations

---


Expand for full commit details
```
     
    This should cause no functional change. 
     
    It also required updating call sites to use span instead of pointers. 
     
    (cherry picked from commit b05c9128c8aa84f028bc336d899ac6c852622429) 
     
    Bug: 401184803 
    Bug: 490533968 
    Change-Id: I13fd424ea4fa7cc679a5206ecb5ee7dd67c025e1 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7649841 
    Reviewed-by: Hongchan Choi <hongchan@chromium.org> 
    Commit-Queue: Michael Wilson <mjwilson@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1597393} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7667424 
    Auto-Submit: Michael Wilson <mjwilson@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7680@{#2802} 
    Cr-Branched-From: 76b7d80e5cda23fe6537eed26d68c92e995c7f39-refs/heads/main@{#1582197}

```

---

Files:

- M `third_party/blink/renderer/modules/webaudio/delay_handler.cc`
- M `third_party/blink/renderer/platform/audio/cpu/arm/delay_neon.cc`
- M `third_party/blink/renderer/platform/audio/cpu/x86/delay_sse2.cc`
- M `third_party/blink/renderer/platform/audio/delay.cc`
- M `third_party/blink/renderer/platform/audio/delay.h`
- M `third_party/blink/renderer/platform/audio/hrtf_panner.cc`

---

Hash: [cacf57930e37b7e5b54d9ba0a299da01ec574b2d](https://chromiumdash.appspot.com/commit/cacf57930e37b7e5b54d9ba0a299da01ec574b2d)  

Date: Wed Mar 18 17:52:40 2026


---

### pe...@google.com (2026-03-18)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### mj...@chromium.org (2026-03-18)

1. No, I think this issue may have been present for a long time.
2. No.

### mj...@chromium.org (2026-03-19)

I still can't get the change to land on M147; webaudio/AudioParam/audioparam-rate-change-357391257.html keeps timing out on the Windows builder. I don't think it's due to the change. M146 already landed.

### dx...@google.com (2026-03-19)

Project: chromium/src  

Branch:  refs/branch-heads/7727  

Author:  Michael Wilson [mjwilson@chromium.org](mailto:mjwilson@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7667384>

[M147] Replace UNSAFE\_TODO in Delay with safe operations

---


Expand for full commit details
```
     
    This should cause no functional change. 
     
    It also required updating call sites to use span instead of pointers. 
     
    (cherry picked from commit b05c9128c8aa84f028bc336d899ac6c852622429) 
     
    Bug: 401184803 
    Bug: 490533968 
    Change-Id: I13fd424ea4fa7cc679a5206ecb5ee7dd67c025e1 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7649841 
    Reviewed-by: Hongchan Choi <hongchan@chromium.org> 
    Commit-Queue: Michael Wilson <mjwilson@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1597393} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7667384 
    Cr-Commit-Position: refs/branch-heads/7727@{#808} 
    Cr-Branched-From: ce01102937348db7b88c8a4257ee4b3ac702eb1a-refs/heads/main@{#1596535}

```

---

Files:

- M `third_party/blink/renderer/modules/webaudio/delay_handler.cc`
- M `third_party/blink/renderer/platform/audio/cpu/arm/delay_neon.cc`
- M `third_party/blink/renderer/platform/audio/cpu/x86/delay_sse2.cc`
- M `third_party/blink/renderer/platform/audio/delay.cc`
- M `third_party/blink/renderer/platform/audio/delay.h`
- M `third_party/blink/renderer/platform/audio/hrtf_panner.cc`

---

Hash: [ad149bc9cc821d4056bf0f7d00d465c4bdab0dea](https://chromiumdash.appspot.com/commit/ad149bc9cc821d4056bf0f7d00d465c4bdab0dea)  

Date: Thu Mar 19 02:03:43 2026


---

### mj...@chromium.org (2026-03-19)

Got the change to land on M147, all currently approved merges are now complete.

### qk...@google.com (2026-03-23)

Labeled `LTS-NotApplicable-138` because there were many conflicts when merging the patch to M138.

### mj...@chromium.org (2026-03-23)

The fix does depend on some other changes:

The `Span()` and `MutableSpan()` methods were added to third\_party/blink/renderer/platform/audio/audio\_channel.h in <https://crrev.com/c/7611048>

The `as_span()` methods were added to third\_party/blink/renderer/platform/audio/audio\_array.h in <https://crrev.com/c/7624386>

Both of these were first landed in M147 and necessary parts were merged to M146.

### dx...@google.com (2026-03-25)

Project: chromium/src  

Branch:  refs/branch-heads/7680  

Author:  Levi Zim [rsworktech@outlook.com](mailto:rsworktech@outlook.com)  

Link:    <https://chromium-review.googlesource.com/7699551>

[M146] Fix blink compilation for platforms other than x86 and arm

---


Expand for full commit details
```
     
    Commit https://crrev.com/c/7649841 forgot to update the generic 
    implementation, causing compilation failures for platforms other than 
    x86 and arm. 
     
    This CL fixes it. 
     
    (cherry picked from commit 3bccbdead3efa7e91f7c9d4078106dedaed84fb8) 
     
    Bug: 401184803 
    Bug: 490533968 
    Change-Id: I9460ada952eeaa22fd571d299235fcfb5e1ef1c1 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7666544 
    Commit-Queue: Michael Wilson <mjwilson@chromium.org> 
    Auto-Submit: Levi Zim <rsworktech@outlook.com> 
    Reviewed-by: Michael Wilson <mjwilson@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1599945} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7699551 
    Commit-Queue: Levi Zim <rsworktech@outlook.com> 
    Cr-Commit-Position: refs/branch-heads/7680@{#3187} 
    Cr-Branched-From: 76b7d80e5cda23fe6537eed26d68c92e995c7f39-refs/heads/main@{#1582197}

```

---

Files:

- M `third_party/blink/renderer/platform/audio/delay.cc`

---

Hash: [40b2252b7cc7fe503031f9f5cdcb5063f5c00f6a](https://chromiumdash.appspot.com/commit/40b2252b7cc7fe503031f9f5cdcb5063f5c00f6a)  

Date: Wed Mar 25 09:20:55 2026


---

### dx...@google.com (2026-03-25)

Project: chromium/src  

Branch:  refs/branch-heads/7727  

Author:  Levi Zim [rsworktech@outlook.com](mailto:rsworktech@outlook.com)  

Link:    <https://chromium-review.googlesource.com/7699932>

[M147] Fix blink compilation for platforms other than x86 and arm

---


Expand for full commit details
```
     
    Commit https://crrev.com/c/7649841 forgot to update the generic 
    implementation, causing compilation failures for platforms other than 
    x86 and arm. 
     
    This CL fixes it. 
     
    (cherry picked from commit 3bccbdead3efa7e91f7c9d4078106dedaed84fb8) 
     
    Bug: 401184803 
    Bug: 490533968 
    Change-Id: I9460ada952eeaa22fd571d299235fcfb5e1ef1c1 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7666544 
    Commit-Queue: Michael Wilson <mjwilson@chromium.org> 
    Auto-Submit: Levi Zim <rsworktech@outlook.com> 
    Reviewed-by: Michael Wilson <mjwilson@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1599945} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7699932 
    Commit-Queue: Levi Zim <rsworktech@outlook.com> 
    Cr-Commit-Position: refs/branch-heads/7727@{#1460} 
    Cr-Branched-From: ce01102937348db7b88c8a4257ee4b3ac702eb1a-refs/heads/main@{#1596535}

```

---

Files:

- M `third_party/blink/renderer/platform/audio/delay.cc`

---

Hash: [550072b1cc1ece178deac0df268dbb180dd34703](https://chromiumdash.appspot.com/commit/550072b1cc1ece178deac0df268dbb180dd34703)  

Date: Wed Mar 25 09:46:57 2026


---

### ct...@chromium.org (2026-04-15)

Downgrading renderer read to S-2 per <https://chromium.googlesource.com/chromium/src/+/main/docs/security/severity-guidelines.md#:~:text=An%20out%2Dof%2Dbounds%20read%20in%20a%20renderer%20process>

### sp...@google.com (2026-04-16)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
Baseline. User information disclosure


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### qk...@google.com (2026-05-18)

Labeled Not-Applicable-144 because the fix required some dependent CLs that caused many conflicts. To avoid side effects in M144, it would be better not to merge them.

### ch...@google.com (2026-06-18)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/490533968)*
