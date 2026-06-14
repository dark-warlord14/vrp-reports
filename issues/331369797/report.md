# use-after-poison in blink::AudioContext::OnRenderError

| Field | Value |
|-------|-------|
| **Issue ID** | [331369797](https://issues.chromium.org/issues/331369797) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>WebAudio |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | em...@gmail.com |
| **Assignee** | ho...@chromium.org |
| **Created** | 2024-03-26 |
| **Bounty** | $8,000.00 |

## Description

tested os:ubuntu 22.04
tested chrome version:
Version 125.0.6368.2 (Developer Build) (64-bit)

Repro Steps:
./chrome --autoplay-policy=no-user-gesture-required  --user-data-dir=/tmp/xx1 http://localhost:8880/crash.html

Bisect info:
 https://chromium-review.googlesource.com/c/chromium/src/+/5277872

 ==1==ERROR: AddressSanitizer: use-after-poison on address 0x7ef1002682a8 at pc 0x55baed287c91 bp 0x7ffe36961670 sp 0x7ffe36961668
READ of size 4 at 0x7ef1002682a8 thread T0 (chrome)
    #0 0x55baed287c90 in Load ./../../v8/include/cppgc/internal/member-storage.h:85:58
    #1 0x55baed287c90 in GetRaw ./../../v8/include/cppgc/member.h:52:54
    #2 0x55baed287c90 in Get ./../../v8/include/cppgc/member.h:270:52
    #3 0x55baed287c90 in GetContextLifecycleNotifier ./../../third_party/blink/renderer/platform/context_lifecycle_observer.h:25:22
    #4 0x55baed287c90 in blink::ExecutionContextLifecycleObserver::GetExecutionContext() const ./../../third_party/blink/renderer/core/execution_context/execution_context_lifecycle_observer.cc:40:41
    #5 0x55baf2e2d639 in blink::AudioContext::OnRenderError() ./../../third_party/blink/renderer/modules/webaudio/audio_context.cc:1198:47
    #6 0x55baf2f7ec3b in Invoke<void (blink::RealtimeAudioDestinationHandler::*)(), const base::WeakPtr<blink::RealtimeAudioDestinationHandler> &> ./../../base/functional/bind_internal.h:738:12
    #7 0x55baf2f7ec3b in MakeItSo<void (blink::RealtimeAudioDestinationHandler::*)(), std::__Cr::tuple<base::WeakPtr<blink::RealtimeAudioDestinationHandler> > > ./../../base/functional/bind_internal.h:954:5
    #8 0x55baf2f7ec3b in void base::internal::Invoker<base::internal::FunctorTraits<void (blink::RealtimeAudioDestinationHandler::*&&)(), base::WeakPtr<blink::RealtimeAudioDestinationHandler>&&>, base::internal::BindState<true, true, false, void (blink::RealtimeAudioDestinationHandler::*)(), base::WeakPtr<blink::RealtimeAudioDestinationHandler>>, void ()>::RunImpl<void (blink::RealtimeAudioDestinationHandler::*)(), std::__Cr::tuple<base::WeakPtr<blink::RealtimeAudioDestinationHandler>>, 0ul>(void (blink::RealtimeAudioDestinationHandler::*&&)(), std::__Cr::tuple<base::WeakPtr<blink::RealtimeAudioDestinationHandler>>&&, std::__Cr::integer_sequence<unsigned long, 0ul>) ./../../base/functional/bind_internal.h:1067:14
    #9 0x55bae1a68bd6 in Run ./../../base/functional/callback.h:156:12
    #10 0x55bae1a68bd6 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task_annotator.cc:203:34
    #11 0x55bae1ac5ed3 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:475:11)> ./../../base/task/common/task_annotator.h:90:5
    #12 0x55bae1ac5ed3 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:473:23
    #13 0x55bae1ac4f64 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:338:40
    #14 0x55bae1ac6b5a in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0:0
    #15 0x55bae1977fa6 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_default.cc:40:55
    #16 0x55bae1ac789b in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:641:12
    #17 0x55bae1a05efe in base::RunLoop::Run(base::Location const&) ./../../base/run_loop.cc:134:14
    #18 0x55baf735a188 in content::RendererMain(content::MainFunctionParams) ./../../content/renderer/renderer_main.cc:367:16
    #19 0x55badf48ce5f in content::RunZygote(content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:676:14
    #20 0x55badf48e155 in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:780:12
    #21 0x55badf490679 in content::ContentMainRunnerImpl::Run() ./../../content/app/content_main_runner_impl.cc:1146:10
    #22 0x55badf48aef4 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) ./../../content/app/content_main.cc:333:36
    #23 0x55badf48ba11 in content::ContentMain(content::ContentMainParams) ./../../content/app/content_main.cc:346:10
    #24 0x55bad0e11e08 in ChromeMain ./../../chrome/app/chrome_main.cc:192:12
    #25 0x7b29af429d8f in __libc_start_call_main ./csu/../sysdeps/nptl/libc_start_call_main.h:58:16

Address 0x7ef1002682a8 is a wild pointer inside of access range of size 0x000000000004.
SUMMARY: AddressSanitizer: use-after-poison (/home/pwn11/chromium/src/out/release/chrome+0x2aae2c90) (BuildId: 5de75dc9ffa5276f)
Shadow bytes around the buggy address:
  0x7ef100268000: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x7ef100268080: 00 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x7ef100268100: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x7ef100268180: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x7ef100268200: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 00
=>0x7ef100268280: f7 f7 f7 f7 f7[f7]f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x7ef100268300: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x7ef100268380: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x7ef100268400: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 00 f7
  0x7ef100268480: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x7ef100268500: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb

==1==ADDITIONAL INFO

==1==Note: Please include this section with the ASan report.
Task trace:
    #0 0x55baf2f7d1d0 in blink::RealtimeAudioDestinationHandler::OnRenderError() ./../../third_party/blink/renderer/modules/webaudio/realtime_audio_destination_handler.cc:263:24


==1==END OF ADDITIONAL INFO
==1==ABORTING


## Attachments

- [crash.html](attachments/crash.html) (text/html, 503 B)
- [asan.log](attachments/asan.log) (text/plain, 6.3 KB)
- [launcher.sh](attachments/launcher.sh) (text/x-sh, 694 B)
- [crash2.html](attachments/crash2.html) (text/html, 578 B)
- [asan2.log](attachments/asan2.log) (text/plain, 32.6 KB)
- [launcher2.sh](attachments/launcher2.sh) (text/x-sh, 693 B)

## Timeline

### cl...@appspot.gserviceaccount.com (2024-03-26)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4889577919021056.

### pa...@chromium.org (2024-03-26)

[security shepherd] I could not reproduce this right now on the specified version. I just started CF on this, and I'll retry reproducing tomorrow morning first thing.

### em...@gmail.com (2024-03-26)

Different PC environments might affect the probability of reproducing the issue. If you cannot consistently reproduce it, you might try opening multiple browsers. I have written a simple script that can open multiple browsers at once and allows for convenient simultaneous closure with just one key (ctrl+c); this should quickly reproduce the issue.
./launcher.sh 2>&1 |grep -E 'AddressS'

### pa...@chromium.org (2024-03-27)

Thanks for providing more information! I was able to get the DCHECK assertion, but when removing dchecks, I couldn't get the UaP to trigger:

```
[1091350:21:0327/094052.645733:FATAL:audio_destination.cc(213)] Check failed: IsMainThread(). 

```

However, reading the code, it seems to me that it's possible to trigger this UaP.

Assigning sinafirooz@ who authored the recent changes. Setting Sev1 to be conservative here, but if it turns out this UaP can't be triggered eventually, I guess we'll need to re-assess this. sinafirooz@ can you help further triage this?

### pe...@google.com (2024-03-27)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### si...@google.com (2024-03-27)

Hi Paul,

I got a separate crash report for the `DCHECK` (Please see <http://crbug.com/40252553>). Can you please help me understand how the `DCHECK` is causing the UaP?

### pa...@chromium.org (2024-03-28)

Hi Sina. After reading the code more, I am definitely unsure whether this could actually lead to a UaP, except from reading the stack trace provided by the reporter, which matches with what we get with the DCHECK. As an owner, if you feel like this UaP cannot be triggered, I'll follow your judgment. Unless reporter has another more reliable way to trigger the UaP?

### em...@gmail.com (2024-03-29)

I'm not quite sure why it can't be reproduced on other PCs. I just downloaded the new version of Chrome (asan build), and one browser can reproduce it stably. Could you try the modified crash2.html to see if it can be reproduced?
tested chrome version: 
Chromium 125.0.6387.0(gs://chromium-browser-asan/linux-release/asan-linux-release-1280080.zip)

repro steps:
./chrome --autoplay-policy=no-user-gesture-required  --user-data-dir=/tmp/xx1 http://localhost:8880/crash2.html --incognito

### cl...@appspot.gserviceaccount.com (2024-03-29)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5167465641738240.

### pa...@chromium.org (2024-03-29)

Thanks for persevering on this reporter, I really do appreciate this. I was eventually convinced the UaP could be triggered, so I tried again early today, and I could eventually reproduce the UaP!

Leaving S1 for the severity, since it is a memory corruption in the renderer process but that doesn't require a user interaction. Anyways, this is now indeed a UaP and not just a `DCHECK` hit.

@sinafirooz, I could only reproduce this with the new crash2.html file **and** using the `launcher.sh` script. I used `125.0.6387.0`. It required me quite a few runs to reproduce, but it eventually does.

### 24...@project.gserviceaccount.com (2024-03-29)

Testcase 5167465641738240 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=5167465641738240.

### em...@gmail.com (2024-03-29)

Occasionally, I can also reproduce a UAF, which might provide more information. Please refer to it.

### ho...@chromium.org (2024-04-01)

I tried everything suggested in this bug (crash, crash2, launcher.sh) and even with the more robust gc() function, but couldn't reproduce the issue. (Debian Linux)

### ho...@chromium.org (2024-04-01)

That said, here's why it could happen:

1. Create multiple AudioContext instances and quickly dropped them.
2. Each instance will try to activate an underlying audio stream/device; this validation/notification is queued in the TaskRunner.
3. AudioContext instances are GCed; everything including RealtimeAudioDestinationHandler, AudioDestination will be gone.
4. The TaskRunner was so busy with spamming, now it begins the validation/notification.
5. The task scheduled has a reference to RealtimeAudioDestinationHandler, which is already gone. UAF happens.

The one thing I wanted to confirm was RADH was specifically using AsWeakPtr() for its scheduled task to avoid UAF. If I can reproduce this locally, I can try to figure out why the weak pointer validation is not working.

### ho...@chromium.org (2024-04-01)

emilykim8708@

Do you have an actual sound device on your reproduction environment? (e.g. a physical desktop/laptop instead of a VM instance)

### em...@gmail.com (2024-04-01)

Yes, I reproduced it on a desktop computer with real audio device.

### pe...@google.com (2024-04-03)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security Impact hotlist or the Severity field, and remove the ReleaseBlock hotlist.

### si...@google.com (2024-04-03)

My linux desktop didn't reproduce the issue either. I am getting the error message below:

```
[1517172:1517206:0403/103121.316954:ERROR:platform_thread_linux.cc(295)] Failed to set realtime priority for thread 1542677: Operation not permitted (1)

```

Is anything wrong with my setup?

### ho...@google.com (2024-04-03)

No. That's normal. It's because Linux does not allow an application (Chromium) to request a realtime priority thread. That's not relevant to this UAP issue and safe to ignore.

### em...@gmail.com (2024-04-04)

Hi, could you try using this new script? After running it, just leave it alone and wait for a few minutes to see if the issue can be reproduced?
Usage:
# Usage: ./script_name <executable_path> <url> <number_of_max_executions>
launcher2.sh ~/asan-linux-release/chrome http://localhost:8880/crash.html 5 2>&1|grep -E 'Address'

### si...@chromium.org (2024-04-05)

I tried the new shell script, to no avail.

### ol...@chromium.org (2024-04-08)

Looks like the root cause is like this:

[RealtimeAudioDestinationHandler::CreatePlatformDestination()](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/webaudio/realtime_audio_destination_handler.cc;l=331;drc=a169ebabcd533a7f5489ac17c1df80f8b89c6fee) passes 'this' as a reference to 'platform\_destination\_' member of AudioDestination type.

It looks safe at a first glance, since it appears that RealtimeAudioDestinationHandler owns 'platform\_destination\_'.

But the fact is - it does not: **AudioDestination is refcounted, and RealtimeAudioDestinationHandler is not**. So there is no guarantee AudioDestination is destroyed when RealtimeAudioDestinationHandler is destroyed.

So platform\_destination\_ can outlive RealtimeAudioDestinationHandler and thus call its OnRenderError() after RealtimeAudioDestinationHandler (and thus the [context](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/webaudio/audio_handler.h;l=242;drc=a169ebabcd533a7f5489ac17c1df80f8b89c6fee)) is destroyed.

If I have not missed something, the short-term fix would be to pass RealtimeAudioDestinationHandler as a weak pointer into AudioDestination.

### ho...@google.com (2024-04-08)

Re: [#comment23](https://issues.chromium.org/issues/331369797#comment23)

> AudioDestination is refcounted, and RealtimeAudioDestinationHandler is not

Hmm. I am not sure. [AudioHandler](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/webaudio/audio_handler.h;drc=a169ebabcd533a7f5489ac17c1df80f8b89c6fee;l=27) is ThreadSafeRefCounted and RADH inherits from it. The AudioHandler being ThreadSafeRefCounted is sort of the backbone of WebAudio's rendering mechanism.

> If I have not missed something, the short-term fix would be to pass RealtimeAudioDestinationHandler as a weak pointer into AudioDestination.

AudioDestination is in `platform/audio`, and RADH is in `modules/webaudio`. The stuff in `platform` can be used in `modules`, but the opposite is not allowed.

### ol...@google.com (2024-04-08)

> Hmm. I am not sure. AudioHandler is ThreadSafeRefCounted and RADH inherits from it. The AudioHandler being ThreadSafeRefCounted is sort of the backbone of WebAudio's rendering mechanism.

Ok, that I missed. But for this case it does not matter: we are passing RealtimeAudioDestinationHandler into AudioDestination as AudioIOCallback& callback - it's not ref-counted.

But also if RealtimeAudioDestinationHandler is refcounted, how do we guarantee that it can only be destroyed on the main thread? Usually it's very hard/infeasible to enforce for refcounted objects. And if there is no guarantee, we should not use weak pointers [here](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/webaudio/realtime_audio_destination_handler.cc;l=262?q=RealtimeAudioDestinationHandler&ss=chromium%2Fchromium%2Fsrc), but rather bind it as a shared pointer. (That would be a separate bug.)

> AudioDestination is in platform/audio, and RADH is in modules/webaudio. The stuff in platform can be used in modules, but the opposite is not allowed.

I'm not sure I understand this comment. We are already passing it.

### ho...@google.com (2024-04-08)

(This is not a response to [#comment25](https://issues.chromium.org/issues/331369797#comment25))

Now I found a way to reproduce with the local ASAN build reliably. The stack trace looks a bit different but it's in the same ballpark:

```
#0 0x16fab34cf in blink::ExecutionContextLifecycleObserver::GetExecutionContext() const+0x5f (/Users/hongchan/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/125.0.6408.0/Chromium Framework:x86_64+0x1b1c44cf)
    #0 0x1755e8ed5 in blink::AudioContext::OnRenderError() ??:0:0
    #1 0x17574d293 in void base::internal::Invoker<base::internal::FunctorTraits<void (blink::RealtimeAudioDestinationHandler::*&&)(), base::WeakPtr<blink::RealtimeAudioDestinationHandler>&&>, base::internal::BindState<true, true, false, void (blink::RealtimeAudioDestinationHandler::*)(), base::WeakPtr<blink::RealtimeAudioDestinationHandler>>, void ()>::RunImpl<void (blink::RealtimeAudioDestinationHandler::*)(), std::__Cr::tuple<base::WeakPtr<blink::RealtimeAudioDestinationHandler>>, 0ul>(void (blink::RealtimeAudioDestinationHandler::*&&)(), std::__Cr::tuple<base::WeakPtr<blink::RealtimeAudioDestinationHandler>>&&, std::__Cr::integer_sequence<unsigned long, 0ul>) ??:0:0
    #2 0x1648e2cbe in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ??:0:0
    #3 0x164941617 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) ??:0:0
    #4 0x1649406c0 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ??:0:0
    #5 0x164942344 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ??:0:0
    #6 0x1647ef4c8 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ??:0:0
    #7 0x164943036 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ??:0:0
    #8 0x16488124e in base::RunLoop::Run(base::Location const&) ??:0:0
    #9 0x179a9f908 in content::RendererMain(content::MainFunctionParams) ??:0:0
    #10 0x16223793a in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*) ??:0:0
    #11 0x162239a4d in content::ContentMainRunnerImpl::Run() ??:0:0
    #12 0x1622358d9 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) ??:0:0
    #13 0x16223632c in content::ContentMain(content::ContentMainParams) ??:0:0
    #14 0x1548f441c in ChromeMain ??:0:0
    #16 0x1091acd40 in main+0x260 (/Users/hongchan/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/125.0.6408.0/Helpers/Chromium Helper (Renderer).app/Contents/MacOS/Chromium Helper (Renderer):x86_64+0x100000d40)
    #16 0x7ff817934365 in 0xfffffffffff5c365

```

Getting `GetExecutionContext()` from the AudioContext after GC is causing UAP.

I got the idea from the original stack trace - the OnRenderError was invoked from the audio thread, not the main thread constructor.

```
    #4 0x5f64c07af82f in media::AudioDeviceThread::ThreadMain() ./../../media/audio/audio_device_thread.cc:118:16

```

So I try to forcibly call OnRenderError from `AudioDeviceThread::ThreadMain()` and it almost immediately causes UAP. Now I am starting to work on the actual fix.

### ho...@google.com (2024-04-08)

Re [#comment25](https://issues.chromium.org/issues/331369797#comment25):

> we are passing RealtimeAudioDestinationHandler into AudioDestination as AudioIOCallback& callback - it's not ref-counted.

Yes. I agree that this is the problem. I am working on the analysis and solutions and will share it soon.

> I'm not sure I understand this comment. We are already passing it.

What I meant was we can't pass it as RADH and we had to pass it as AudioIOCallback (with a partial interface). It's against the rule to expose the module class directly to the platform class.

### ap...@google.com (2024-04-08)

Project: chromium/src
Branch: main

commit e05ae3b16fcd5c28b73ee1204f859a5702e5e778
Author: Michael Wilson <mjwilson@chromium.org>
Date:   Mon Apr 08 22:28:05 2024

    Flag guard WebAudio OnRenderError handling
    
    Bug: 331369797
    Change-Id: I59125d2c87f3b5e4378bb179bd42616cae474c93
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5427770
    Reviewed-by: Hongchan Choi <hongchan@chromium.org>
    Commit-Queue: Michael Wilson <mjwilson@chromium.org>
    Reviewed-by: Ian Kilpatrick <ikilpatrick@chromium.org>
    Reviewed-by: Sina Firoozabadi <sinafirooz@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1284133}

M       content/renderer/media/renderer_webaudiodevice_impl.cc
M       third_party/blink/common/features.cc
M       third_party/blink/public/common/features.h
M       third_party/blink/renderer/modules/webaudio/audio_context.cc
M       third_party/blink/renderer/modules/webaudio/realtime_audio_destination_handler.cc
M       third_party/blink/renderer/platform/audio/audio_destination.cc
M       third_party/blink/renderer/platform/audio/audio_destination_test.cc

https://chromium-review.googlesource.com/5427770


### mj...@chromium.org (2024-04-08)

With the patch landed in #comment28 the OnRenderError handling should be disabled by default which should stop the error from occurring.

Submitter, are you able to check on a tip-of-tree build if the use-after-poison still happens?  Otherwise the change should go to canary soon.

### ho...@google.com (2024-04-08)

Following up on [#comment26](https://issues.chromium.org/issues/331369797#comment26) + [#comment28](https://issues.chromium.org/issues/331369797#comment28): after rebasing to ToT I don't see the UAP crash anymore.

To emilykim8708@: The patch in [#comment28](https://issues.chromium.org/issues/331369797#comment28) is not in ant releases yet, but you can check the available version later:
<https://chromiumdash.appspot.com/commits?revision=r1284133&platform=Windows>

### em...@gmail.com (2024-04-09)

I confirm that the issue has been fixed.
tested version:
-   1284246.zip

### em...@gmail.com (2024-04-09)

Sorry, I didn't carefully review the code of CL before testing, and it still reproduced after using --enable-features=WebAudioHandleOnRenderError.
tested version:
-   1284246.zip

### ho...@chromium.org (2024-04-09)

Thanks for your attention on this, emilykim87087@!

Just to confirm: you provided "--enable-features=WebAudioHandleOnRenderError" and it does reproduce on ToT. Right?

If so, that's working as intended; we are still working on the actual fix but added a flag to guard this new code path.

### em...@gmail.com (2024-04-09)

Yes, it can only be reproduced when using "-- enable features=WebAudioHandleOnRenderError".

### mj...@chromium.org (2024-04-09)

Great, that's what we expected!  I will request merge of crrev.com/c/5427770 to M124.

### pe...@google.com (2024-04-09)

Merge review required: M124 has already been cut for stable release.

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
Owners: eakpobaro (Android), eakpobaro (iOS), obenedict (ChromeOS), danielyip (Desktop)

### mj...@chromium.org (2024-04-09)

1. Why does your merge fit within the merge criteria for these milestones?
This issue is a release blocker.

2. What changes specifically would you like to merge? Please link to Gerrit.
https://crrev.com/c/5427770

3. Have the changes been released and tested on canary?
Yes, landed in 125.0.6408.0

4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
No, this is adding a flag guard to an existing feature.

5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
N/A

6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.
The test team may have difficulty verifying the fix.  I would like to ask the submitter and hongchan@ to help verifying the fix in 124 after the merge.

### ho...@chromium.org (2024-04-10)

Today I tried to reproduce the issue on following builds on Linux CloudTop, but it was not successful.

- ToT ASAN Version 125.0.6410.0
- Pre-built ASAN Version 125.0.6396.0 (Revision 1281583)

### am...@chromium.org (2024-04-12)

after an off-bug chat with mjwilson@ approving this flag guarding change (<https://crrev.com/c/5427770>) for merge to M124, please merge this fix to branch 6367 at soonest so this fix can be included in recuts for M124 Stable and desktop

### ap...@google.com (2024-04-12)

Project: chromium/src
Branch: refs/branch-heads/6367

commit cd0e5b0bca78ffe85d566cf44bc06658cf8b42ac
Author: Michael Wilson <mjwilson@chromium.org>
Date:   Fri Apr 12 17:55:26 2024

    Flag guard WebAudio OnRenderError handling
    
    (cherry picked from commit e05ae3b16fcd5c28b73ee1204f859a5702e5e778)
    
    Bug: 331369797
    Change-Id: I59125d2c87f3b5e4378bb179bd42616cae474c93
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5427770
    Reviewed-by: Hongchan Choi <hongchan@chromium.org>
    Commit-Queue: Michael Wilson <mjwilson@chromium.org>
    Reviewed-by: Ian Kilpatrick <ikilpatrick@chromium.org>
    Reviewed-by: Sina Firoozabadi <sinafirooz@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1284133}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5445094
    Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Auto-Submit: Daniel Yip <danielyip@google.com>
    Owners-Override: Daniel Yip <danielyip@google.com>
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Cr-Commit-Position: refs/branch-heads/6367@{#791}
    Cr-Branched-From: d158c6dc6e3604e6f899041972edf26087a49740-refs/heads/main@{#1274542}

M       content/renderer/media/renderer_webaudiodevice_impl.cc
M       third_party/blink/common/features.cc
M       third_party/blink/public/common/features.h
M       third_party/blink/renderer/modules/webaudio/audio_context.cc
M       third_party/blink/renderer/modules/webaudio/realtime_audio_destination_handler.cc
M       third_party/blink/renderer/platform/audio/audio_destination.cc
M       third_party/blink/renderer/platform/audio/audio_destination_test.cc

https://chromium-review.googlesource.com/5445094


### go...@google.com (2024-04-22)

Reminder M125 is already in Beta and Stable promotion is coming soon. Please review this bug and assess if this is indeed a RBS. If not, please remove the RBS label. If so, please make sure to land the fix and request a merge into the release branch ASAP. Thank you.

### mj...@chromium.org (2024-04-22)

The flag guard is already in M125 so this should not be a release blocker anymore.  I will remove the label.

### am...@chromium.org (2024-04-23)

Note for future security-release handling: flag guarding was put in place to negate the security impact of this issue. An actual fix for this issue is still in progress (which is while this issue remains open), once the fix is landed, this issue be considered fixed in that release in which the fix is shipped.

### ol...@google.com (2024-04-25)

hongchan@ probably something like this <https://chromium-review.googlesource.com/c/chromium/src/+/5489221>?

Could you try it? (I just sketched it, have not tested).

If it works, I can clean it up and land.

### pe...@google.com (2024-04-25)

hongchan: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ho...@chromium.org (2024-04-25)

I am still working on the reproduction of the issue on linux platform, and have not been successful.

On macOS, it reproduces only with the modification on the Render() code (e.g. forcibly causing error while running) so I wouldn't say it is perfect.

Will try the speculative fix in [#comment44](https://issues.chromium.org/issues/331369797#comment44) tomorrow on macOS.

### ol...@google.com (2024-04-26)

Can we figure a unit test for the behavior?

### ho...@google.com (2024-04-26)

I tried on both cloudtop and macOS ASAN. The provided repro case and the shell script do not work on anywhere.

On macOS (with actual audio devices), it can be reproduced with a very specific/intentional change:

```
// audio_device_thread.cc: L83-L87
uint32_t buffer_index = 0;
  while (true) {
    callback_->OnSocketError();     // <== This
    uint32_t pending_data = 0;
    size_t bytes_read = socket_.Receive(&pending_data, sizeof(pending_data));

```

On top of this change, I tried to apply the speculative CL (<https://crrev.com/c/5489221>) but sadly it still crashes ASAN.

My next idea is to hold the AudioContext alive until it gets signaled by RWADI. (error or no error)

### ho...@google.com (2024-04-26)

Also confirmed that the pre-built chromium-126.0.6442.0-mac-asan crashes with the following command:

`./chromium-126.0.6442.0-mac-asan/Chromium.app/Contents/MacOS/Chromium --disable-gpu --enable-features=WebAudioHandleOnRenderError --autoplay-policy=no-user-gesture-required --incognito --use-mock-keychain http://localhost:8000/crash2.html`

The stack trace a bit different from what the reporter provided, but it is consistent with what I see from [#comment48](https://issues.chromium.org/issues/331369797#comment48) repro attempt:

```
==73605==ERROR: AddressSanitizer: use-after-poison on address 0x7ee3002d2980 at pc 0x000176972480 bp 0x7ff7b07c82c0 sp 0x7ff7b07c82b8
READ of size 4 at 0x7ee3002d2980 thread T0
==73605==WARNING: invalid path to external symbolizer!
==73605==WARNING: Failed to use and restart external symbolizer!
    #0 0x17697247f in blink::ExecutionContextLifecycleObserver::GetExecutionContext() const+0x5f
    #1 0x17c301a09 in blink::AudioContext::OnRenderError()+0xc9
    #2 0x17c464f63 in void base::internal::Invoker<base::internal::FunctorTraits<void (blink::RealtimeAudioDestinationHandler::*&&)(), base::WeakPtr<blink::RealtimeAudioDestinationHandler>&&>, base::internal::BindState<true, true, false, void (blink::RealtimeAudioDestinationHandler::*)(), base::WeakPtr<blink::RealtimeAudioDestinationHandler>>, void ()>::RunImpl<void (blink::RealtimeAudioDestinationHandler::*)(), std::__Cr::tuple<base::WeakPtr<blink::RealtimeAudioDestinationHandler>>, 0ul>(void (blink::RealtimeAudioDestinationHandler::*&&)(), std::__Cr::tuple<base::WeakPtr<blink::RealtimeAudioDestinationHandler>>&&, std::__Cr::integer_sequence<unsigned long, 0ul>)+0x1d3
...

```

In all, GetExecutionContext() returns a raw pointer to the main thread EC, but it's already gone after GC.

### ol...@google.com (2024-04-26)

On which thread AudioContext is garbage-collected? Maybe weak\_ptr does not work in this case because execution on the main thread races with destruction on some other thread (GC thread pool)? We probably should stop using weak\_ptr and post using shared\_ptr instead.

### ho...@google.com (2024-04-26)

> On which thread AudioContext is garbage-collected? Maybe weak\_ptr does not work in this case because execution on the main thread races with destruction on some other thread (GC thread pool)?

I am assuming it's the main thread. We have a IsMainThread() check in some destructors and they have been passing the check all these years.

### ap...@google.com (2024-04-29)

Project: chromium/src
Branch: main

commit 50eb6f8c2f57ebf5f0eb2480eb544f93e88673f5
Author: Hongchan Choi <hongchan@chromium.org>
Date:   Mon Apr 29 17:28:47 2024

    Check initialization state before accessing GC-managed objects
    
    The RADH::OnRenderError function call assumes the validity of the
    associated AudioContext, which is a GC-managed object. This CL
    fixes the assumption by checking the initialization state of the
    RADH (which is changed before GC happens).
    
    Bug: 331369797
    Test: Local reproduction doesn't crash ASAN with this change
    Change-Id: I2eb0ae55c6f6c1283b9fa9b31f1beca6f18a252b
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5497083
    Commit-Queue: Hongchan Choi <hongchan@chromium.org>
    Reviewed-by: Michael Wilson <mjwilson@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1293784}

M       third_party/blink/renderer/modules/webaudio/audio_context.cc
M       third_party/blink/renderer/modules/webaudio/realtime_audio_destination_handler.cc

https://chromium-review.googlesource.com/5497083


### ho...@chromium.org (2024-04-30)

Re: emilykim8707@

Could you try your reproduction with the latest ASAN (after r1293784)?

### em...@gmail.com (2024-05-01)


I confirm that the new version has not reproduced UAP or any similar security issues again.
Test version: r1294281

### ho...@chromium.org (2024-05-01)

Thanks for the confirmation! Then I am marking this as fixed.

### pe...@google.com (2024-05-01)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### ho...@chromium.org (2024-05-01)

Re: [#comment56](https://issues.chromium.org/issues/331369797#comment56)

1. Yes.
2. Yes.

### am...@chromium.org (2024-05-02)

manually adding merge review labels for the fix in c#52; going to let this get a bit more bake time since it was just landed yesterday

### am...@chromium.org (2024-05-02)

I just realized this was landed two days ago, not one. I've just reviewed this fix and am not seeing any issues since this was landed.
M125 and M124 merge approved for <https://crrev.com/c/5497083> -- please merge this fix to M125 / branch 6422 and M124 Stable/ branch 6367 by EOD tomorrow Thursday, 2 May so this fix can be included in the next respective updates for each.

### rz...@google.com (2024-05-02)

Adding to the LTS-NotApplicable-120 hotlist based on [comment #57](https://issues.chromium.org/issues/331369797#comment57)

### pe...@google.com (2024-05-02)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### ap...@google.com (2024-05-02)

Project: chromium/src
Branch: refs/branch-heads/6422

commit 2f9e1beefe10e98ee4d1e7c0bdcf8f3c57ccc24d
Author: Hongchan Choi <hongchan@chromium.org>
Date:   Thu May 02 17:34:35 2024

    Check initialization state before accessing GC-managed objects
    
    The RADH::OnRenderError function call assumes the validity of the
    associated AudioContext, which is a GC-managed object. This CL
    fixes the assumption by checking the initialization state of the
    RADH (which is changed before GC happens).
    
    (cherry picked from commit 50eb6f8c2f57ebf5f0eb2480eb544f93e88673f5)
    
    Bug: 331369797
    Test: Local reproduction doesn't crash ASAN with this change
    Change-Id: I2eb0ae55c6f6c1283b9fa9b31f1beca6f18a252b
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5497083
    Commit-Queue: Hongchan Choi <hongchan@chromium.org>
    Reviewed-by: Michael Wilson <mjwilson@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1293784}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5510827
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Cr-Commit-Position: refs/branch-heads/6422@{#601}
    Cr-Branched-From: 9012208d0ce02e0cf0adb9b62558627c356f3278-refs/heads/main@{#1287751}

M       third_party/blink/renderer/modules/webaudio/audio_context.cc
M       third_party/blink/renderer/modules/webaudio/realtime_audio_destination_handler.cc

https://chromium-review.googlesource.com/5510827


### ap...@google.com (2024-05-02)

Project: chromium/src
Branch: refs/branch-heads/6367

commit adc5a73165eb2484855e1c4d31381489f8b88c71
Author: Hongchan Choi <hongchan@chromium.org>
Date:   Thu May 02 19:31:43 2024

    Check initialization state before accessing GC-managed objects
    
    The RADH::OnRenderError function call assumes the validity of the
    associated AudioContext, which is a GC-managed object. This CL
    fixes the assumption by checking the initialization state of the
    RADH (which is changed before GC happens).
    
    (cherry picked from commit 50eb6f8c2f57ebf5f0eb2480eb544f93e88673f5)
    
    Bug: 331369797
    Test: Local reproduction doesn't crash ASAN with this change
    Change-Id: I2eb0ae55c6f6c1283b9fa9b31f1beca6f18a252b
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5497083
    Commit-Queue: Hongchan Choi <hongchan@chromium.org>
    Reviewed-by: Michael Wilson <mjwilson@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1293784}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5510833
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Cr-Commit-Position: refs/branch-heads/6367@{#1071}
    Cr-Branched-From: d158c6dc6e3604e6f899041972edf26087a49740-refs/heads/main@{#1274542}

M       third_party/blink/renderer/modules/webaudio/audio_context.cc
M       third_party/blink/renderer/modules/webaudio/realtime_audio_destination_handler.cc

https://chromium-review.googlesource.com/5510833


### sp...@google.com (2024-05-09)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $8000.00 for this report.

Rationale for this decision:
$7,000 reward for memory corruption in the renderer / sandboxed process + $1,000 bisect bonus

Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. Two other things we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.
* If you are already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have already registered, there is no need to repeat the process and you’ll automatically be paid soon. If you have any payment related questions or issues, please reach out to p2p-vrp@google.com.

### pe...@google.com (2024-05-10)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-05-16)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-08-08)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/331369797)*
