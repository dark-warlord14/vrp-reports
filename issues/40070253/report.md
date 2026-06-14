# Heap-use-after-free in media::AudioOutputDevice::AudioThreadCallback::Process

| Field | Value |
|-------|-------|
| **Issue ID** | [40070253](https://issues.chromium.org/issues/40070253) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | Internals, Internals>Media>Audio |
| **Reporter** | at...@gmail.com |
| **Assignee** | sc...@chromium.org |
| **Created** | 2012-09-09 |
| **Bounty** | $3,133.00 |

## Description


Repro-file as attachment.

Chrome version: Chromium 23.0.1261.0

ASAN-output:

==2049== ERROR: AddressSanitizer heap-use-after-free on address 0x7f13f23ce690 at pc 0x7f1471a40773 bp 0x7f140468c7d0 sp 0x7f140468c7c8
READ of size 8 at 0x7f13f23ce690 thread T546
==2049== AddressSanitizer: while reporting a bug found another one.Ignoring.
    #0 0x7f1471a40772 in media::AudioOutputDevice::AudioThreadCallback::Process(int) ???:0
    #1 0x7f1471b19e28 in media::AudioDeviceThread::Thread::Run() ???:0
    #2 0x7f1471b19aa6 in media::AudioDeviceThread::Thread::ThreadMain() ???:0
    #3 0x7f146c8e32d7 in base::(anonymous namespace)::ThreadFunc(void*) ../../base/threading/platform_thread_posix.cc:0
    #4 0x7f1473d9039b in __asan::AsanThread::ThreadStart() ??:0
0x7f13f23ce690 is located 16 bytes inside of 296-byte region [0x7f13f23ce680,0x7f13f23ce7a8)
freed by thread T399 here:
==2049== AddressSanitizer: while reporting a bug found another one.Ignoring.
    #0 0x7f1473d96110 in operator delete(void*) ??:0
    #1 0x7f1471a6f16f in media::Pipeline::FinishDestroyingFiltersTask() ???:0
    #2 0x7f1471a6ae03 in media::Pipeline::TeardownStateTransitionTask() ???:0
    #3 0x7f146c865159 in MessageLoop::RunTask(base::PendingTask const&) ???:0
    #4 0x7f146c8656ef in MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) ???:0
    #5 0x7f146c8664e5 in MessageLoop::DoWork() ???:0


## Attachments

- [chrome-heap-use-after-free-mediaAudioOutputDeviceAudioThreadCallbackProcess.html](attachments/chrome-heap-use-after-free-mediaAudioOutputDeviceAudioThreadCallbackProcess.html) (text/html; charset=us-ascii, 547 B)
- [chrome-heap-use-after-free-mediaAudioOutputDeviceAudioThreadCallbackProcess.html](attachments/chrome-heap-use-after-free-mediaAudioOutputDeviceAudioThreadCallbackProcess_53216023.html) (text/html; charset=us-ascii, 513 B)

## Timeline

### in...@chromium.org (2012-09-10)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-09-10)

[Empty comment from Monorail migration]

### at...@gmail.com (2012-09-10)

The original repro-file was unstable depending on hardware. 

I think it was because of timing was done by calculation v=Math.max(-1e1,Math.min(1e4,0e6*Math.sin(j*Math.pow(2,k/C)/695)))/Math.exp(j++/5e3);

I created new repro-file where the timing is done by a function pausecomp(millis).

For my laptop running with Intel i5-3210M CPU the millisecond value for reproduce was 6-10ms. For some reason the repro-file didn't work with laptop using AMD E-450 CPU it might be that the timing needs to count in the time used by the new Audio()

I'll look into reproducing this issue with slower machines later.

### da...@chromium.org (2012-09-10)

I believe this is related to scherkus' recent refactoring of the Pipeline. He's got some other patches in the queue which he thinks will resolve this.

### sc...@chromium.org (2012-09-10)

Thanks for the report!

http://codereview.chromium.org/10837206/ should correct a host of shutdown-related bugs -- should be landed within next day or so

### sc...@chromium.org (2012-09-10)

[Empty comment from Monorail migration]

### sc...@chromium.org (2012-09-10)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-09-10)

Andrew can you please confirm if this affects m22. Pwnium is planned for m22, and we definitely should merge this if affected.

### sc...@chromium.org (2012-09-11)

will take a look!

### at...@gmail.com (2012-09-13)

Has the whole patch already landed on trunk?

### sc...@chromium.org (2012-09-13)

The patch dalecurtis@ was referring to landed as r156011

### at...@gmail.com (2012-09-13)

So should this be fixed? I can still see the crash with slightly different stack trace. Tried with ASAN build of Chromium 23.0.1266.0 (Developer Build 156516) and the repro-file from https://crbug.com/chromium/147499#c3.

==31279== ERROR: AddressSanitizer heap-use-after-free on address 0x7fa38f6dba90 at pc 0x7fa4172d2c11 bp 0x7fa3deb907d0 sp 0x7fa3deb907c8
READ of size 8 at 0x7fa38f6dba90 thread T1172
    #0 0x7fa4172d2c10 in media::AudioOutputDevice::AudioThreadCallback::Process(int) ???:0
    #1 0x7fa4173b06e8 in media::AudioDeviceThread::Thread::Run() ???:0
    #2 0x7fa4173b0366 in media::AudioDeviceThread::Thread::ThreadMain() ???:0
    #3 0x7fa412036c97 in base::(anonymous namespace)::ThreadFunc(void*) ../../base/threading/platform_thread_posix.cc:0
    #4 0x7fa41982d75a in __asan::AsanThread::ThreadStart() ??:0
0x7fa38f6dba90 is located 16 bytes inside of 296-byte region [0x7fa38f6dba80,0x7fa38f6dbba8)
freed by thread T1033 here:
    #0 0x7fa419834180 in operator delete(void*) ??:0
    #1 0x7fa417303015 in media::Pipeline::OnStopCompleted(media::PipelineStatus) ???:0
    #2 0x7fa41730db3f in media::SerialRunner::RunNextInSeries(media::PipelineStatus) ???:0
    #3 0x7fa411e7c634 in base::internal::Invoker<1, base::internal::BindState<base::Callback<void (media::PipelineStatus)>, void (media::PipelineStatus), void (media::PipelineStatus)>, void (media::PipelineStatus)>::Run(base::internal::BindStateBase*) ???:0
    #4 0x7fa411fb739d in MessageLoop::RunTask(base::PendingTask const&) ???:0
    #5 0x7fa411fb796f in MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) ???:0
    #6 0x7fa411fb87c9 in MessageLoop::DoWork() ???:0
    #7 0x7fa411fc2b96 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ???:0
    #8 0x7fa411fb624c in MessageLoop::RunInternal() ???:0
    #9 0x7fa411ffa631 in base::RunLoop::Run() ???:0
.
.
.

### sc...@chromium.org (2012-09-13)

Hrmm... AudioDeviceThread::Thread always accesses callback_ under a lock. During teardown, AudioRendererImpl::Stop() ends up clearing callback_ to NULL under a lock. I'm a bit lost as to how we end up inside AudioOutputDevice::AudioThreadCallback::Process().

tommi: do you have any ideas? This bug is likely independent of any recent changes.

### to...@chromium.org (2012-09-13)

Here's what I think is the problem:

Pipeline::OnStopCompleted is called before the AudioOutputDevice instance has actually finished its teardown.  So AudioOutputDevice is being deleted while it's still running.

This happens because AudioOutputDevice::Stop only begins the Stop process.  Stop is complete when AudioOutputDevice::ShutdownOnIOThread has completed.  Before we get there however, the object gets deleted.

Given the urgency, here is a quick and dirty way to avoid this problem:

Change the call to SerialRunner::Run() to not signal done_cb after all tasks have been run.  Instead, change it to post a task to the IO thread.  This new task should then signal the done_cb.

Granted, this is pretty ugly since it assumes some implementation details of the AudioOutputDevice, but it should work since the last task is posted after the ShutdownOnIOThread task.  So, we should be guaranteed that shutdown has been completed when the new task executes, and only then can we call OnStopCompleted.

### sc...@chromium.org (2012-09-14)

Yuck. That's probably it.

I've got two ideas that I'm going to prototype:
  1) Make AudioOutputDevice::Stop() accept a completion callback.
As you note, it's actually an async method but it appears synchronous. We can pass in the callback from AudioRendererImpl::Stop() into AOD::Stop() so that it's safe to delete everything.
  2) AOD::Stop() internally calls AddRef() and Release() when stop has finished, potentially self deleting itself
It's ugly but if we're looking for the short-term / small fix then it might be ok...

### sc...@chromium.org (2012-09-18)

Oh my... all my attempts have failed because it's even more heinous than I though :(

This is what's happening:
 1) AudioRendererImpl::Start() calls AudioOutputDevice::Start(), which kicks off on IPC to create the stream
 2) AudioRendererImpl::Stop() is called, which calls  AudioDeviceThread::Stop()
 3) AudioRendererImpl executed the Pipeline callback, which eventually leads to deleting AudioRendererImpl
 4) AudioOutputDevice::OnStreamCreated() is called, which actually call AudioDeviceThread::Start()
 5) AudioDeviceThread spins up the thread w/ the original pointer to AudioRendererImpl
 6) AudioDeviceThread crashes as soon as it executes the callback

My fix is to use a NULL AudioDeviceThread as a check that Stop() has been called and we never should start again.

### sc...@chromium.org (2012-09-18)

http://codereview.chromium.org/10938006/

### sc...@chromium.org (2012-09-18)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-09-18)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=157378

------------------------------------------------------------------------
r157378 | scherkus@chromium.org | 2012-09-18T17:43:11.304003Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/media/audio/audio_output_device.h?r1=157378&r2=157377&pathrev=157378
   M http://src.chromium.org/viewvc/chrome/trunk/src/media/audio/audio_output_device_unittest.cc?r1=157378&r2=157377&pathrev=157378
   M http://src.chromium.org/viewvc/chrome/trunk/src/media/audio/audio_output_device.cc?r1=157378&r2=157377&pathrev=157378

Prevent AudioDeviceThread from starting if clients have called Stop().

Due to ordering of messages between the media thread and the IO thread it was possible for AudioOutputDevice to receive OnStreamCreated() after AudioRendererImpl had called Stop(). Since AudioRendererImpl is deleted shortly after calling Stop(), AudioDeviceThread would get started with a callback pointer to a potentially deleted AudioRendererImpl.

BUG=147499
TEST=media_unittests, asan build w/ test file included in bug report

Review URL: https://codereview.chromium.org/10938006
------------------------------------------------------------------------

### in...@chromium.org (2012-09-18)

Do you think m22 can be affected ? We shouldn't be going to Pwnium with this sec-critical.

### sc...@chromium.org (2012-09-18)

Definitely affected. AFAIK this code has been around for longer than M22...

### in...@chromium.org (2012-09-18)

Ok, then we will merge it. Thanks for confirming.

### sc...@chromium.org (2012-09-19)

heads up: do NOT merge -- the fix introduced a null-ptr crash, see https://crbug.com/chromium/150805

### bu...@chromium.org (2012-09-19)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=157626

------------------------------------------------------------------------
r157626 | scherkus@chromium.org | 2012-09-19T22:18:10.343551Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/media/audio/audio_output_device.h?r1=157626&r2=157625&pathrev=157626
   M http://src.chromium.org/viewvc/chrome/trunk/src/media/audio/audio_output_device_unittest.cc?r1=157626&r2=157625&pathrev=157626
   M http://src.chromium.org/viewvc/chrome/trunk/src/media/audio/audio_output_device.cc?r1=157626&r2=157625&pathrev=157626

Revert r157378 as it caused WebRTC to dereference null pointers when restarting a call.

I've kept my unit test changes intact but disabled until I get a proper fix.

BUG=147499,150805
TBR=henrika

Review URL: https://codereview.chromium.org/10946040
------------------------------------------------------------------------

### bu...@chromium.org (2012-09-19)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=157630

------------------------------------------------------------------------
r157630 | karen@chromium.org | 2012-09-19T22:29:02.018353Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/1271/src/media/audio/audio_output_device_unittest.cc?r1=157630&r2=157629&pathrev=157630
   M http://src.chromium.org/viewvc/chrome/branches/1271/src/media/audio/audio_output_device.cc?r1=157630&r2=157629&pathrev=157630
   M http://src.chromium.org/viewvc/chrome/branches/1271/src/media/audio/audio_output_device.h?r1=157630&r2=157629&pathrev=157630

Merge 157626 - Revert r157378 as it caused WebRTC to dereference null pointers when restarting a call.

I've kept my unit test changes intact but disabled until I get a proper fix.

BUG=147499,150805
TBR=henrika

Review URL: https://codereview.chromium.org/10946040

TBR=scherkus@chromium.org
Review URL: https://codereview.chromium.org/10957004
------------------------------------------------------------------------

### bu...@chromium.org (2012-09-20)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=157841

------------------------------------------------------------------------
r157841 | scherkus@chromium.org | 2012-09-20T21:17:51.796844Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/media/audio/audio_output_device.h?r1=157841&r2=157840&pathrev=157841
   M http://src.chromium.org/viewvc/chrome/trunk/src/media/audio/audio_output_device_unittest.cc?r1=157841&r2=157840&pathrev=157841
   M http://src.chromium.org/viewvc/chrome/trunk/src/media/audio/audio_output_device.cc?r1=157841&r2=157840&pathrev=157841

Prevent AudioDeviceThread from starting if clients have called Stop() (round 2).

My first attempt at a fix (r157378) was no good as it's legal to repeatedly start and stop an AudioOutputDevice. This time around we use flag to track a pending stop so we don't start AudioDeviceThread knowing the client had requested a stop.

BUG=147499


Review URL: https://chromiumcodereview.appspot.com/10958004
------------------------------------------------------------------------

### sc...@chromium.org (2012-09-21)

Requesting to merge r157841 to M23.

Merging just r157841 to M22 will likely have merge conflicts in audio_output_device_unittest.cc. You can either:
  1) Merge all three (r157378 r157626 r157841)
  2) Ignore unit test conflicts for r157841 (the new tests I added/refactored won't get run, but should be fine)

### in...@chromium.org (2012-09-21)

Security bugs have blanket merge approval unless we get explicitly notified.

### in...@chromium.org (2012-09-21)

i like 2) and skip the tests.

### sc...@chromium.org (2012-09-21)

Merged into M23.

Do we want to let it bake for a bit before merging directly to M22? I'll prep and test the CL. You tell me when to pull the trigger :)

### bu...@chromium.org (2012-09-21)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=158006

------------------------------------------------------------------------
r158006 | scherkus@chromium.org | 2012-09-21T16:47:07.347334Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/1271/src/media/audio/audio_output_device_unittest.cc?r1=158006&r2=158005&pathrev=158006
   M http://src.chromium.org/viewvc/chrome/branches/1271/src/media/audio/audio_output_device.cc?r1=158006&r2=158005&pathrev=158006
   M http://src.chromium.org/viewvc/chrome/branches/1271/src/media/audio/audio_output_device.h?r1=158006&r2=158005&pathrev=158006

Merge 157841 - Prevent AudioDeviceThread from starting if clients have called Stop() (round 2).

My first attempt at a fix (r157378) was no good as it's legal to repeatedly start and stop an AudioOutputDevice. This time around we use flag to track a pending stop so we don't start AudioDeviceThread knowing the client had requested a stop.

BUG=147499


Review URL: https://chromiumcodereview.appspot.com/10958004

TBR=scherkus@chromium.org
Review URL: https://codereview.chromium.org/10964043
------------------------------------------------------------------------

### in...@chromium.org (2012-09-21)

So here is the deal, we have yet another 2-3 days before the final m22 beta/stable refresh. We need to remember to merge this or we will go to pwnium with a sec-critical bug. If you dont think this is risky fix, we should merge it to m22 and keep a very close eye for next 2-3 days on canary.

### sc...@chromium.org (2012-09-21)

OK I built an asan version of M22 w/ and w/o my changes.

Unit tests still pass and verified asan exception no longer happens. Tested WebRTC and all seems to be good.

Going to merge...

### bu...@chromium.org (2012-09-21)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=158021

------------------------------------------------------------------------
r158021 | scherkus@chromium.org | 2012-09-21T17:55:19.450789Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/1229/src/media/audio/audio_output_device.cc?r1=158021&r2=158020&pathrev=158021
   M http://src.chromium.org/viewvc/chrome/branches/1229/src/media/audio/audio_output_device.h?r1=158021&r2=158020&pathrev=158021

Merge 157841 - Prevent AudioDeviceThread from starting if clients have called Stop() (round 2).

My first attempt at a fix (r157378) was no good as it's legal to repeatedly start and stop an AudioOutputDevice. This time around we use flag to track a pending stop so we don't start AudioDeviceThread knowing the client had requested a stop.

BUG=147499


Review URL: https://chromiumcodereview.appspot.com/10958004

TBR=scherkus@chromium.org
Review URL: https://codereview.chromium.org/10962036
------------------------------------------------------------------------

### sc...@gmail.com (2012-09-21)

Seems like an easy race to win reliably; I'm inclined to leave the severity at critical.

### sc...@gmail.com (2012-09-25)

@attekett: technically a critical bug, so $3133.7 reward! Congrats!

### at...@gmail.com (2012-09-25)

Awesome! First critical I have stumbled upon.

### pa...@google.com (2012-09-26)

[Empty comment from Monorail migration]

### pa...@google.com (2012-09-26)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-10-02)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-10-12)

[Empty comment from Monorail migration]

### js...@chromium.org (2012-12-20)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

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

This issue was migrated from crbug.com/chromium/147499?no_tracker_redirect=1

[Multiple monorail components: Internals, Internals>Media>Audio]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40070253)*
