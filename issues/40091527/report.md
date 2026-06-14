# use-after-poison in operator blink::ExecutionContext *

| Field | Value |
|-------|-------|
| **Issue ID** | [40091527](https://issues.chromium.org/issues/40091527) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>WebAudio |
| **Platforms** | Linux |
| **Reporter** | cd...@gmail.com |
| **Assignee** | rt...@chromium.org |
| **Created** | 2018-05-31 |
| **Bounty** | $1,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36

Steps to reproduce the problem:
Steps to reproduce the problem:
1. Build source code 
    config args.gn file as below:
		use_sanitizer_coverage = true
		is_asan = true
		is_debug = false
		enable_nacl = false
		treat_warnings_as_errors = false
	ninja -j4 -C out/chrome_asan chrome
2. Build a mini web server.
	I used python twisted module to build the webserver.
	1) copy poc.html and launcher.html into the htm dirctory 
	2) run python web.py
3. ./chrome --no-sandbox http://127.0.0.1:8605/launcher.html

What is the expected behavior?

What went wrong?
Could occasionally get "use-after-poison" crash.
The probability of repo differs depending on the performance of the machine.It means that could adjust the number in the launcher.html to make crash happen more（in my computer the number is 1050  ,1200)

Did this work before? N/A 

Chrome version: 68.0.3432.0  Channel: n/a
OS Version: ubuntu16.04
Flash Version: 

Please allow browser to pop the new tabs.

## Attachments

- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)

## Timeline

### me...@chromium.org (2018-05-31)

Thanks for the report.

tkent: Are you a good owner for this bug? If not, can you please reassign?

[Monorail components: Blink>Internals>Frames]

### tk...@chromium.org (2018-06-01)

Looks a WebAudio issues


[Monorail components: -Blink>Internals>Frames Blink>WebAudio]

### me...@chromium.org (2018-06-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-06-02)

[Empty comment from Monorail migration]

### rt...@chromium.org (2018-06-04)

[Empty comment from Monorail migration]

### me...@chromium.org (2018-06-04)

FWIW, I wasn't able to reproduce with an ASAN build. Could you please also update the Security_Impact label if you are able to repro? 

### rt...@chromium.org (2018-06-04)

I also cannot repro this (using ToT chrome). A zillion tabs were created and chrome consumed 20GB of memory before I stopped it.  There are lots of errors about "MojoAudioOutputIPC failed to acquire factory"

How long does this usually take?  Can you provide hints how to change the values in launcher.html to make this reproduce more often?

### cd...@gmail.com (2018-06-05)

It is not stable.In my machine,the first repro time was about 600s,and the next was longer. 

My core idea,in order to make crash more often, is to increase the times that windows open and close.So the values in launcher.html could be smaller if the performance of the machine was high.
Could you please try to change the value to a smaller(cuz my machine is not good enough) number? Or maybe increase the number of child windows such as child_4 ,child_5...

### cd...@gmail.com (2018-06-05)

According to the stack trace,we found that the finial function ：
"operator blink::ExecutionContext * " in /third_party/blink/renderer/platform/heap/member.h:88 is like another one,see at:
https://bugs.chromium.org/p/chromium/issues/detail?id=843151,

The first one is operator overloading,the next is implicit conversion。
I am not sure that if they are the same cause of the crash.Hope this may help.



### pa...@chromium.org (2018-06-05)

Is the --no-sandbox flag necessary for the PoC to work?

### rt...@chromium.org (2018-06-05)

Changed the limits to 250 and 500.  Locked up my machine hard for several hours until mmap eventually failed.

This is going to be hard to track down.

### pa...@chromium.org (2018-06-07)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-06-08)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rt...@chromium.org (2018-06-12)

Is there a bug in the repro case?  In launcher, you have

child_1 = window.open("http://127.0.0.1:8605/poc.html") ;

But in the timeout function, you do:

child1.close();

I assume you really wanted child_1.close()?

### rt...@chromium.org (2018-06-12)

Changing the repro case as mentioned in c#14 and adding child_[456] allowed me to reproduce this crash once in a while using ToT from this morning.

The backtrace is essentially the same:

=================================================================
==158820==ERROR: AddressSanitizer: use-after-poison on address 0x7e8065b8aa60 at pc 0x7f3f88b1892b bp 0x7ffe24cb6e20 sp 0x7ffe24cb6e18
READ of size 8 at 0x7e8065b8aa60 thread T0 (chrome)
    #0 0x7f3f88b1892a in operator blink::ExecutionContext * ./../../third_party/blink/renderer/platform/heap/member.h:88:32
    #1 0x7f3f88b1892a in LifecycleContext ./../../third_party/blink/renderer/platform/lifecycle_observer.h:44:0
    #2 0x7f3f88b1892a in GetExecutionContext ./../../third_party/blink/renderer/core/dom/context_lifecycle_observer.h:71:0
    #3 0x7f3f88b1892a in blink::BaseAudioContext::GetExecutionContext() const ./../../third_party/blink/renderer/modules/webaudio/base_audio_context.cc:980:0
    #4 0x7f3f88b78949 in blink::OfflineAudioDestinationHandler::NotifyComplete() ./../../third_party/blink/renderer/modules/webaudio/offline_audio_destination_node.cc:275:31

The offline context is basically done processing and wants to inform the main thread of that at line 275 in offline_audio_destination_node.cc:

  // The OfflineAudioContext might be gone.
  if (Context() && Context()->GetExecutionContext())
    Context()->FireCompletionEvent();

Maybe we're not checking correctly that the offline context is gone?

Perhaps due to some recent changes in oilpan and trace wrappers and such?

Could you take a look haraken?

### rt...@chromium.org (2018-06-12)

For the record this is what I'm using for launcher.html:

<script>
function test(){
 child_1 = window.open("http://127.0.0.1:8605/poc.html") ;
child_2 = window.open("http://127.0.0.1:8605/poc.html") ;
child_3 = window.open("http://127.0.0.1:8605/poc.html") ;

child_4 = window.open("http://127.0.0.1:8605/poc.html") ;
child_5 = window.open("http://127.0.0.1:8605/poc.html") ;
child_6 = window.open("http://127.0.0.1:8605/poc.html") ;
 }

test();
</script>

<script type="text/javascript">
setTimeout(function(){  

   location = location;
  },500/*1050*/)


setTimeout(function(){  

   child_1.close();
   child_2.close();
   child_3.close();

   child_4.close();
   child_5.close();
   child_6.close();
  },600/*1200*/)

</script>


### ha...@chromium.org (2018-06-13)

Who guarantees that Context() is alive? It seems like it's accessing AudioNode::context_, which is an UntracedMember. Why does it need to be an UntracedMember?

If Context() is accessed from a non-main thread, it must use CrossThreadPersistent.


Also (I'm not sure if this is related to this crash but) LifecycleObserver is not implemented in a thread-safe manner. It's wrong to access GetExecutionContext() from a non-main thread.



### ho...@chromium.org (2018-06-13)

haraken@

OfflineAudioDestinationHandler::NotifyComplete() runs on the main thread. So accessing Context() or GetExecutionContext() from the method should be thread-safe.

I am speculating what happens if when PostCrossThreadTask() is invoked after the main thread task runner goes away. I believe the task runner handles such case gracefully. Right?

### ha...@chromium.org (2018-06-14)

> OfflineAudioDestinationHandler::NotifyComplete() runs on the main thread. So accessing Context() or GetExecutionContext() from the method should be thread-safe.

Makes sense.

> I am speculating what happens if when PostCrossThreadTask() is invoked after the main thread task runner goes away. I believe the task runner handles such case gracefully. Right?

Then the task should not run in the first place.

I think that this is related to the fact that AudioNode::context_ is UntracedMember, which means that it is not traced by Oilpan.

Who guarantees that AudioNode::context_ is alive when OfflineAudioDestinationHandler::NotifyComplete() runs?


### rt...@chromium.org (2018-06-14)

The context owns the OfflineAudioDestinationHandler.

I suspect this is another case where the audio thread is running and processing audio but the context has been GCed on the main thread.

### ho...@chromium.org (2018-06-14)

Re #19:

I am testing a patch that makes AudioHandler::context_ CrossThreadPersistent. Will try to repro the case with it, but here's one question:

From UntracedMember to CrossThreadPersistent, will there be any performance impact? Because Context() getter in AudioHandler is a quite common pattern in WebAudio, it might have some side effect in terms of the rendering performance.

### ha...@chromium.org (2018-06-15)

There will be some performance impact because CrossThreadPersistent needs to acquire a GC lock. If another thread is running a GC, CrossThreadPersistent::Get is blocked.

Another issue is that changing UntracedMember to (CrossThread)Persistent has a risk of causing memory leaks because you're changing a raw pointer to a GC root.

Before making any change, I want to understand 1) why the context is prematurely collected and 2) what a right lifetime relationsihp should look like.


### ho...@chromium.org (2018-06-15)

Here's what I think:

> 1) why the context is prematurely collected

The WebAudio rendering mechanism relies on two different layers: (a) AudioNode and (b) AudioHandler.

AudioNode is a GC-mananged object whereas the AudioHandler is not. This is necessary because AudioHandlers are the component that renders the audio stream. Thus it should not be interfered by the GC for the stability of audio stream.

With that said, AudioHandlers often need to access BaseAudioContext to query the data required for the rendering. That is why the AudioHandler keeps a "UntracedMember" reference to BaseAudioContext. This is not ideal, but IIRC the clean separation was very difficult.

An Audiohandlers detached from its AudioNode is going to be kept in DeferredTaskHandler's orphan list. So AudioHandler can outlive its AudioNode, but we have not thought out the relationship between BaseAudioContext and AudioHandler. Theoretically, DTH can outlive BAC so I think it might be dangerous that AudioHandler posting a CrossThread task that accesses BAC.

https://cs.chromium.org/chromium/src/third_party/blink/renderer/modules/webaudio/deferred_task_handler.h?q=deferred_task&sq=package:chromium&g=0&l=51

> 2) what a right lifetime relationsihp should look like.

Even after user drop the reference to BAC, I think BAC should stay alive until all the AudioHandlers go away.

As a reference, we have a design doc written by tkent@:
https://docs.google.com/document/d/1MrHQ5RNMTEqlWMR-_yuqmxIG1lxvhA3xF32r2SJ732o/edit#heading=h.k54yjbta6lz8



### ha...@chromium.org (2018-06-18)

Thanks Hongchan for the summary!

> An Audiohandlers detached from its AudioNode is going to be kept in DeferredTaskHandler's orphan list. So AudioHandler can outlive its AudioNode, but we have not thought out the relationship between BaseAudioContext and AudioHandler. Theoretically, DTH can outlive BAC so I think it might be dangerous that AudioHandler posting a CrossThread task that accesses BAC.

Makes sense.

> Even after user drop the reference to BAC, I think BAC should stay alive until all the AudioHandlers go away.

Makes sense 2 :)



### ho...@chromium.org (2018-06-19)

It was impossible for me to repro this on my machine (32GB, 3.5G 12 Cores); it always locks up the machine without crashing. So I added these bash exports as rtoy@ suggested:

export G_SLICE=always-malloc
export NSS_DISABLE_ARENA_FREE_LIST=1
export NSS_DISABLE_UNLOAD=1
export ASAN_OPTIONS="detect_odr_violation=0 $ASAN_OPTIONS"

After this setting change and replacing UntracedMember with CrossThreadPersisent, I got an OOM crash instead of use-after-poison. I'll confirm this ToT to make sure the fix is effective and report back here.

### rt...@chromium.org (2018-06-19)

Those options used to be listed at http://www.chromium.org/developers/testing/addresssanitizer, but I see they aren't any more.  I had to have detect_odr_violation=0 because that always happened before I even had a chance to run the test.

### ho...@chromium.org (2018-06-20)

Sadly I wasn't able to repro the crash with ToT. This may mean that CrossThreadPersistent keeps things alive longer so it ends up with OOM.



### ab...@google.com (2018-07-03)

Bulk update: M68 stable cut is scheduled for July 19th. This issue is marked as RB-Stable, so please take a look at it before. Thanks!

### sh...@chromium.org (2018-07-04)

rtoy: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rt...@chromium.org (2018-07-10)

Using chromium rev 7d4a46981645aaa92f31a235d396ac0a29807c3c, I've been able to reproduce this pretty reliably using the test case from c#16.  I put in a few prints and get this:

  0x7ed5f98fada0: OfflineAudioContext::HasPendingActivity: is_rendering = 1
  0x7ed5f97f6650: OfflineAudioContext::HasPendingActivity: is_rendering = 1
  0x7ed5f98f9e30: OfflineAudioContext::HasPendingActivity: is_rendering = 1
  0x7ed5f991a7f0: OfflineAudioContext::HasPendingActivity: is_rendering = 0
  0x7ed5f98edf88: OfflineAudioContext::HasPendingActivity: is_rendering = 1
  0x7ed5f991ac88: OfflineAudioContext::HasPendingActivity: is_rendering = 1
  0x7ed5f99035e0: OfflineAudioContext::HasPendingActivity: is_rendering = 1
  0x7ed5f98e21e0: OfflineAudioContext::HasPendingActivity: is_rendering = 0
  0x6110000ed340: OfflineAudioDestinationHandler::NotifyComplete:   0x7e92db786f
00
  0x7e92db786f00: OfflineAudioContext::FireCompletionEvent
  0x6110000ffe00: OfflineAudioDestinationHandler::NotifyComplete:   0x7ed5f98eda
f0
  0x6110000dd580: OfflineAudioDestinationHandler::NotifyComplete:   0x7ed5f98fad
a0
=================================================================
==31847==ERROR: AddressSanitizer: use-after-poison on address 0x7ed5f98fadd8 at pc 0x7f0536082fab bp 0x7ffe4bc2e520 sp 0x7ffe4bc2e518


The interesting part is address 0x7ed5f98fada0, which the address for the offline context object.

We see here NotifyComplete is called just before the use-after-poison, but in the first line of the output HasPendingActivity is true (is_rendering = 1).

I thought this would keep the OfflineAudioContext object alive and since it's still alive, I thought the ExecutionContext would also be kept alive.  Maybe this is wrong?

### rt...@chromium.org (2018-07-11)

The prints in c#30 is a bit suspect because of all the tabs that are created in the test.  A unique identifier is needed to figure out what's happening.

### rt...@chromium.org (2018-07-11)

Added a UUID to each offline context so we can keep track of all of the contexts.  The output (where I've ripped out irrelevant stuff and shortened the UUID value) looks like:

  0x7ecefe8f7d30 584c8b7c: OfflineAudioContext::startOfflineRendering
  0x7ecefe8f7d30 584c8b7c: OfflineAudioContext::HasPendingActivity: is_rendering = 1
  0x7ecefe8f7d30 584c8b7c: OfflineAudioContext::HasPendingActivity: is_rendering = 1
  0x7ecefe8f7d30 584c8b7c: OfflineAudioContext::HasPendingActivity: is_rendering = 1
  0x7ecefe8f7d30 584c8b7c: OfflineAudioContext::HasPendingActivity: is_rendering = 1
  0x7ecefe8f7d30 584c8b7c: OfflineAudioContext::ContextDestroyed
  0x7ecefe8f7d30 584c8b7c: OfflineAudioContext::HasPendingActivity: is_rendering = 1
  0x7ecefe8f7d30 584c8b7c: OfflineAudioContext::HasPendingActivity: is_rendering = 1
  0x7ecefe8f7d30 584c8b7c: OfflineAudioContext::HasPendingActivity: is_rendering = 1
  0x611000128d00: OfflineAudioDestinationHandler::NotifyComplete:   0x7ecefe8f7d30
=================================================================
==105942==ERROR: AddressSanitizer: use-after-poison on address 0x7ecefe8f7e58 at pc 0x7f1074bd4445 bp 0x7ffc5cf25ab0 sp 0x7ffc5cf25aa8
READ of size 8 at 0x7ecefe8f7e58 thread T0 (chrome)

Notice that ContextDestroyed() is called. (I guess that's because execution context is going away?)

Then HasPendingActivity() is still being called (which returns true).

Finally, the offline context is done and calls NotifyComplete (on the main thread) to fire the completion event for the offline context.

@haraken: Is it correct that HasPendingActivity is still called after ContextDestroyed has been called?

If this is correct, then one possible solution is to inform the OfflineAudioDestinationHandler that the parent offline context has been (or will be) destroyed.  Then skip trying to fire the event because the execution context is (or will be) gone.

### ha...@chromium.org (2018-07-12)

> @haraken: Is it correct that HasPendingActivity is still called after ContextDestroyed has been called?

No. The return value of HasPendingActivity is ignored after the context is destroyed.

In general it doesn't make sense to keep running something after the context is destroyed. Would it be possible to close the offline context when the context gets destroyed? (i.e., in ContextLifecycleObserver::ContextDestroyed())


### ho...@chromium.org (2018-07-12)

So the problem here is that the pending notification (e.g. promise resolver) from the off-main thread arrives after the BaseAudioContext is gone. We were naively thinking that HasPendingActivity() will keep the BAC alive.

The what would be the best practice for those pending/orphan notifications from the off-main thread? Something like this would work?

 - BAC keeps the main thread task scheduler.
 - Then the off-main thread object always uses the task scheduler to post
   a cross-thread task.
 - When ExecutionContext goes away, the main thread task scheduler will throw away
   all the pending tasks in the queue.

It seems like this problem is happening quite a few places using cross-thread transaction in WebAudio, so I would like to establish a good pattern to handle it.

### rt...@chromium.org (2018-07-12)

I current hacky fix for this is to have OfflineAudioContext::ContextDestroyed() set a flag that the context is gone.  For this particular issue where NotifyComplete just return if the context is gone.  This appears to fix this bug.

But yeah, we need to do something better.

For an online (realtime) context, perhaps we can just kill the audio thread?  (There might be a problem with that if someone called close() and the context goes away before we're finished cleaning up.)

### ho...@chromium.org (2018-07-12)

rtoy@

Since I can't reproduce this locally, I would like to try one thing:
https://cs.chromium.org/chromium/src/third_party/blink/renderer/modules/webaudio/offline_audio_destination_node.cc?dr=C&g=0&l=269

Can we replace (Context() && Context()->GetExecutionContext()) with (main_thread_task_runner_) and see what happens?

### ho...@chromium.org (2018-07-12)

Re #35:

Not sure. If the task is already in the queue of the main thread task runner, it still might be firing after the audio thread is gone.

Yes, we really need to plan out the lifetime of BaseAudioContext (and its children).

### rt...@chromium.org (2018-07-12)

Using main_thread_task_runner_ didn't really fix this.  Instead of crashing in NotifyComplete, we get use-after-poison like so:

==166072==ERROR: AddressSanitizer: use-after-poison on address 0x7ef149602278 at
 pc 0x7f1ed328be80 bp 0x7fff3ca1a0f0 sp 0x7fff3ca1a0e8
READ of size 8 at 0x7ef149602278 thread T0 (chrome)
    #0 0x7f1ed328be7f in operator* ./../../base/memory/scoped_refptr.h:215:13
    #1 0x7f1ed328be7f in GetDeferredTaskHandler ./../../third_party/blink/renderer/modules/webaudio/base_audio_context.h:255:0
    #2 0x7f1ed328be7f in blink::OfflineAudioContext::FireCompletionEvent() ./../../third_party/blink/renderer/modules/webaudio/offline_audio_context.cc:356:0
    #3 0x7f1ed5067ba2 in Run ./../../base/callback.h:140:12
    #4 0x7f1ed5067ba2 in Run ./../../third_party/blink/renderer/platform/wtf/functional.h:320:0
    #5 0x7f1ed5067ba2 in blink::(anonymous namespace)::RunCrossThreadClosure(WTF::CrossThreadFunction<void ()>) ./../../third_party/blink/renderer/platform/web_task_runner.cc:15:0

I guess defered_task_handler_ has already been destroyed at this point.

### ho...@chromium.org (2018-07-12)

That's even worse. DeferredTaskHandler is supposed to outlive the BAC. If that's already gone, members in BAC are also gone. Having a flag for "destroyed context" in BAC would not be really helpful. No?

### rt...@chromium.org (2018-07-12)

Yes, I don't understand that since deferred_task_handler_ is a scoped_refptr object in the BaseAudioContext class.

But in this particular case, it doesn't happen because we don't actually fire the event because we know the context is gone, so that code path isn't executed and the flag is in the offline audio destination class.

### rt...@chromium.org (2018-07-12)

For anyone trying the repro case in c#16, be careful.  It creates tabs faster than it closes them, so you'll eventually have so many tabs open that your machine will lock up.

Change the timeouts to 600 for both still allows the test to reproduce, but it seems to take quite a bit longer.  But the number of tabs doesn't grow forever.

### ab...@google.com (2018-07-16)

any update on this bug yet? It's marked as RB-Stable for M68. Awhalley@ thoughts on this bug?

### rt...@chromium.org (2018-07-16)

I have a fix for this.  At least with the fix I can't reproduce the issue anymore.  But the issue is pretty hard to reproduce.  The fix is more like a work-around until we can come up with a better solution, but that requires a significant effort to redesign how all of this works.

### bu...@chromium.org (2018-07-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/e3af3e7e4ff664d70d04b64e0a1890c259cf90f5

commit e3af3e7e4ff664d70d04b64e0a1890c259cf90f5
Author: Raymond Toy <rtoy@chromium.org>
Date: Mon Jul 16 22:54:56 2018

Inform destination handler if execution context is gone.

When the execution context is being destroyed, inform the destination
handler of that so that we don't try to access the execution context
that is in the process of going away.

This CL only handles the specific case in https://crbug.com/chromium/848306, and is a simple
fix for that issue.  This really needs to be fixed in a better way, but
that requires significant design work.

Bug: 848306
Test: Manually run repro case and see that it doesn't happen
Change-Id: I89a4d397af15a823d9c25ef814195706f7b30b21
Reviewed-on: https://chromium-review.googlesource.com/1138722
Commit-Queue: Raymond Toy <rtoy@chromium.org>
Reviewed-by: Hongchan Choi <hongchan@chromium.org>
Reviewed-by: Kentaro Hara <haraken@chromium.org>
Cr-Commit-Position: refs/heads/master@{#575459}
[modify] https://crrev.com/e3af3e7e4ff664d70d04b64e0a1890c259cf90f5/third_party/blink/renderer/modules/webaudio/audio_destination_node.h
[modify] https://crrev.com/e3af3e7e4ff664d70d04b64e0a1890c259cf90f5/third_party/blink/renderer/modules/webaudio/base_audio_context.cc
[modify] https://crrev.com/e3af3e7e4ff664d70d04b64e0a1890c259cf90f5/third_party/blink/renderer/modules/webaudio/offline_audio_destination_node.cc


### rt...@chromium.org (2018-07-17)

cdsrc2016@gmail.com, please try a canary build to see if this still reproduces. I cannot reproduce this with a canary build myself, but it was always hard anyway.  The particular version I used for testing where it was reproducible no longer reproduces with the CL in c#44 applied.

### cd...@gmail.com (2018-07-19)

I tried the #44 build.Run for about one hour and no repro too.


### rt...@chromium.org (2018-07-19)

Thanks for testing!  I'm going to consider this fixed then.

### rt...@chromium.org (2018-07-19)

Does this need to be merged to M68?

### sh...@chromium.org (2018-07-19)

This bug requires manual review: We are only 4 days from stable.
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), kariahda@(iOS), bhthompson@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@google.com (2018-07-19)

It won't make the stable cut of 68, but once the change has spent some time in dev/canary we can look to merge it to 68 to get picked up in any stable updates.

### rt...@chromium.org (2018-07-19)

Sounds good.

### aw...@chromium.org (2018-07-19)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-20)

[Empty comment from Monorail migration]

### ab...@chromium.org (2018-07-20)

Rejecting merge for M68 right now.

### aw...@chromium.org (2018-07-23)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-07-30)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@chromium.org (2018-07-30)

Hi cdsrc2016@ thanks for both the report, and for being helpful as we fixed it. The VRP panel decided to award $1,000 :-)

### aw...@chromium.org (2018-07-30)

[Empty comment from Monorail migration]

### cd...@gmail.com (2018-07-31)

awhalley@  thanks very much for the reward~.

BTW,could this one be assigned a CVE?

### aw...@google.com (2018-07-31)

By default it'll be assigned one when M69 is released, but I'll make a note to get one issued sooner if needed.

### cd...@gmail.com (2018-08-01)

Thanks for that and we will wait for M69 :-) 

### aw...@chromium.org (2018-09-21)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-09-25)

Sorry for the delay. CVE allocated and listed on https://chromereleases.googleblog.com/2018/09/stable-channel-update-for-desktop.html

### aw...@chromium.org (2018-09-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-10-26)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2019-01-04)

[Empty comment from Monorail migration]

### is...@google.com (2019-01-04)

This issue was migrated from crbug.com/chromium/848306?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/853142]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091527)*
