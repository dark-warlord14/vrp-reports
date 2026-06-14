# WebAudio render that coincides with GC graph mutation can cause snap

| Field | Value |
|-------|-------|
| **Issue ID** | [40080869](https://issues.chromium.org/issues/40080869) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebAudio |
| **Reporter** | ma...@gmail.com |
| **Assignee** | tk...@chromium.org |
| **Created** | 2014-11-18 |
| **Bounty** | $4,000.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36

Steps to reproduce the problem:
1. Run any Chrome/Chromium version >= 38 with GC exposed to JS with --js-flags="--expose_gc" command line option
2. Visit http://jsbin.com/mavade/1  ( JS source visible @ http://jsbin.com/mavade/1/edit?js )
3. Refresh page until crash occurs

What is the expected behavior?
Nasty noise is audible. Tab doesn't crash.

What went wrong?
Nasty noise is audible. Tab often crashes.

Our production app occasionally crashes for our users who are on stable Chrome (38). We have reproduced the crash on Chrome versions all the way to canary. The test case (see jsbin url) is my best attempt at producing a small and minimal reproduction script.

In our app, the WebAudio crashes occur during seemingly unrelated memory heavy events, leading me to believe that this bug is GC related.

Debugging Chromium (using copious log statements) gives further clues that the crash is caused by mutation of the audio node graph by the garbage collector while the audio thread is traversing the graph during an audio render cycle.

This may or may not be related to https://code.google.com/p/chromium/issues/detail?id=431546 and https://code.google.com/p/chromium/issues/detail?id=433479 .

The recent lock-addressing commits https://codereview.chromium.org/615913002 and https://codereview.chromium.org/703203005 do not solve the issue.

Crashed report ID: 

How much crashed? Just one tab

Is it a problem with a plugin? No 

Did this work before? Yes Chrome <= 37 (pre oilpan changes)

Chrome version: 38.0.2125.122  Channel: stable
OS Version: OS X 10.9.5
Flash Version: Shockwave Flash 15.0 r0

Crashes on linux, windows and mac.

## Timeline

### ma...@gmail.com (2014-11-19)

An observation of a minor issue:

bool AudioContext::isGraphOwner()
{
    return m_contextGraphMutex.locked();
}

is NOT equivalent to the pre-oilpan:

bool AudioContext::isGraphOwner() const
{
    return currentThread() == m_graphOwnerThread;
}


This makes all the many ASSERT(isGraphOwner()) invocations misleading/wrong/useless.

### ma...@gmail.com (2014-11-19)

It appears that there is no protection against an AudioSummingJunction's m_renderingOutputs diverging from memory-allocated-reality between the time that the outputs are captured within the AudioSummingJunction::updateRenderingState invocation (at the start of rendering) and the time those m_renderingOutputs are actually traversed during the render pull. A node destroying GC event that coincides with the render could be causing these occasional dangling pointer dereferences.

Part of the issue seems to be the directionality of the strong referencing of nodes and of the rendering traversal of nodes. Strong referencing between nodes (via their outputs and inputs) only occurs in the downstream direction whereas rendering traversal occurs in the upstream direction.


Traversal locking or upstream strong referencing should be added to protect those nodes (from being disposed/destroyed) that are destined to be traversed during a render. Probably easier said than done.


(Disclaimer: my focus on looking at the WebAudio implementation is to find a JS workaround, not fix the root issue, so this cursory investigation and interpretation might be plain wrong)

### [Deleted User] (2014-11-20)

Able to repro this issue on Windows7 using: latest stable: 39.0.2171.65 

This is regression issue, broken in M38.

CL: http://build.chromium.org/f/chromium/perf/dashboard/ui/changelog_blink.html?url=/trunk&range=180220:180287&mode=html
Blink: http://build.chromium.org/f/chromium/perf/dashboard/ui/changelog_blink.html?url=/trunk&range=180281%3A180276

Suspect: r180277	
@haraken@chromium.org: Could you please look into this issue. 

### ha...@chromium.org (2014-11-20)

The WebAudio thread is not attached to Oilpan, so the thread shouldn't be stopped by a GC.


### ke...@chromium.org (2014-12-01)

[Empty comment from Monorail migration]

### ke...@chromium.org (2014-12-01)

[Comment Deleted]

### ke...@chromium.org (2014-12-01)

[Empty comment from Monorail migration]

### rt...@chromium.org (2014-12-01)

haraken: But GC will run while the audio thread is running, right? That would be bad if objects are collected while the audio thread thinks those objects are still alive.

### ma...@gmail.com (2014-12-01)

rtoy: That matches my understanding.

GC comprises two main steps, mark (tracing) and sweep (deallocating).
The mark phase will trigger many trace invocations into the WebAudio graph, with indeterminate ordering and timing.

Audio rendering occurs frequently, and probably take less time to complete than a typical GC.
A GC can occur at any time, and lasts for unknown duration (probably proportional to the complexity of the heap?).

A GC can temporally overlap with an audio rendering (any part of it) that is already in-progress.
An audio rendering can temporally overlap with a GC (any part of it) that is already in-progress.
It is also possible that multiple audio renderings will temporally overlap with a single GC.

The possibilities are many, and the implications of them on the current implementation are (for me) unfathomable.

### cl...@chromium.org (2014-12-02)

haraken@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### ha...@chromium.org (2014-12-02)

> haraken: But GC will run while the audio thread is running, right? That would be bad if objects are collected while the audio thread thinks those objects are still alive.

If the audio thread is using an audio object, the object should be protected via AudioContext::refNode. Even if a GC runs while the audio thread is using the object, the object shouldn't be collected.

If that is not the case, something wrong is going on... e.g., we forget to protect some object.


### ma...@gmail.com (2014-12-03)

There might be at least one problem concerning the locking of the source nodes (the m_referencedNodes).

Consider these lines in the AudioContext::trace method:
{
    AutoLocker lock(this);
    visitor->trace(m_referencedNodes);
}
https://code.google.com/p/chromium/codesearch#chromium/src/third_party/WebKit/Source/modules/webaudio/AudioContext.cpp&q=AudioContext::trace&sq=package:chromium&l=1086&type=cs

It looks at-a-glance like access is protected into the m_referencedNodes vector, but I think this is misleading. 

m_referencedNodes is a member, so the trace into the vector itself (and thus tracing out all the items in the vector) is deferred by pushing the pending visit onto a stack. The actual vector trace is performed some time later during the GC, when the graph lock is no longer held.
At least, this is what I understand to happen (but I'm going to double check right now and I'll post a correction if I find this not to be the case).

Why does this heap vector need to be a Member, why can't it be owned by the context instance directly?

### ma...@gmail.com (2014-12-03)

I confirmed that the heap will trace the contents of the m_referencedNodes vector long after the AudioContext::trace method has completed. Thus, the lock is useless.

Changing the declaration of m_referencedNodes from:
Member<HeapVector<Member<AudioNode>>> m_referencedNodes;
to:
HeapVector<Member<AudioNode>> m_referencedNodes;

Appears to solve one half of the bug (but there might be others).


I think the test script exercises two bugs:
* destination connected node chains with a source node
* destination connected node chains without a source node
The end result of either bug is similar, a dangling pointer is dereferenced while traversing the node graph during a render. I think the root causes are not the same.

http://jsbin.com/mavade/1 exercises both bugs courtesy of the statement
    if (Math.random() > 0.5)
which randomly creates chains with and without source nodes.

The http://jsbin.com/mavade/2 variation removes the randomisation around source nodes. The node chains will always have a source node attached. This fails far less frequently. With the changes to m_referencedNodes so as to not be a Member, this variation has not yet crashed, so this might be the problem for the "has source node" case.


If I'm right, that just leaves the "has no source node" case to deal with, which looks to be much more difficult to solve.

### ma...@gmail.com (2014-12-04)

This commit https://codereview.chromium.org/703203005 made the Member changes. I cannot see the bug corresponding to it, I can only assume for security reasons?
Given my input on this bug, could permission somehow be granted to me to view the bug at https://code.google.com/p/chromium/issues/detail?id=427651 so that I can better understand the rationale behind the changes to m_referencedNodes?

### rt...@chromium.org (2014-12-04)

First, I really appreciate your looking into this.
  
Second, yes it's a security issue. I will need to investigate whether you should be allowed to look at the issue itself.  However, the bug report doesn't really contain any additional information other than a stack trace that shows that the audio thread and GC thread are touching m_referencedNodes.

### ha...@chromium.org (2014-12-04)

Mark: Thanks, your investigation sounds right!

tkent-san: Would you take a look at this?


### tk...@chromium.org (2014-12-04)

Working on the m_referencedNode issue.


### bu...@chromium.org (2014-12-04)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=186482

------------------------------------------------------------------
r186482 | tkent@chromium.org | 2014-12-04T07:14:04.240005Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/modules/webaudio/AudioContext.cpp?r1=186482&r2=186481&pathrev=186482
   M http://src.chromium.org/viewvc/blink/trunk/Source/modules/webaudio/AudioContext.h?r1=186482&r2=186481&pathrev=186482

Web Audio: Oilpan: Correctly trace m_referencedNodes elements within a lock.

Blink r184963 [1] was not a right fix.  Oilpan marker pushed m_referencedNodes
to a stack and released the lock immediately, then iterated it later.
We need to make m_referencedNode HeapVector, not Member<HeapVector>
to iterate it immediately.

[1] http://src.chromium.org/viewvc/blink?view=revision&revision=184963

BUG=434136

Review URL: https://codereview.chromium.org/776203002
-----------------------------------------------------------------

### rt...@chromium.org (2014-12-04)

I can confirm that with ToT chromium (which has the above CL applied), http://jsbin.com/mavade/2 no longer crashes.  But it seems to run for just 143 gc-ing messages.  http://jsbin.com/mavade/1 still causes a crash.

### ma...@gmail.com (2014-12-05)

The test script looks like this:

    for (var i = 0; i < 1000; i++) {
...
        if (i % 7 === 0) {
            console.log('gc-ing')
            gc();
        }
    }

so 143 GC-ing messages sounds about right (1000 / 7 ~ 143).

Feel free to fork those JS bins and increase the number of iterations from 1000 upwards, or twiddle with the various magic numbers. The numbers were found through trial and error and have no special significance, other than causing semi-reliable crashes on the machines I tested it on.

Tweaking the numbers or the graph structures within the script could possibly expose other threading related bugs.

### tk...@chromium.org (2014-12-05)

I reproduced the crash with http://jsbin.com/mavade/1.

  * frame #0: 0x00000001151e24de libblink_web.dylib`blink::Member<blink::AudioContext>::get(this=0x2a2a2a2a2a2a2a32) const + 30 at Handle.h:627
    frame #1: 0x00000001151e14bc libblink_web.dylib`blink::AudioSummingJunction::context(this=0x2a2a2a2a2a2a2a2a) + 44 at AudioSummingJunction.h:47
    frame #2: 0x00000001151e6785 libblink_web.dylib`blink::AudioNodeInput::pull(this=0x2a2a2a2a2a2a2a2a, inPlaceBus=0x0000000000000000, framesToProcess=128) + 53 at AudioNodeInput.cpp:209
    frame #3: 0x00000001151e079a libblink_web.dylib`blink::AudioNode::pullInputs(this=0x00003e0a02a02f78, framesToProcess=128) + 202 at AudioNode.cpp:428
    frame #4: 0x00000001151e01d2 libblink_web.dylib`blink::AudioNode::processIfNecessary(this=0x00003e0a02a02f78, framesToProcess=128) + 242 at AudioNode.cpp:391
    frame #5: 0x00000001151e7b22 libblink_web.dylib`blink::AudioNodeOutput::pull(this=0x00001399202908c0, inPlaceBus=0x0000000000000000, framesToProcess=128) + 418 at AudioNodeOutput.cpp:143
    frame #6: 0x00000001151e6704 libblink_web.dylib`blink::AudioNodeInput::sumAllConnections(this=0x00001399202818c0, summingBus=0x0000273abbe8a1c0, framesToProcess=128) + 532 at AudioNodeInput.cpp:200
    frame #7: 0x00000001151e6881 libblink_web.dylib`blink::AudioNodeInput::pull(this=0x00001399202818c0, inPlaceBus=0x0000273abbe88b68, framesToProcess=128) + 305 at AudioNodeInput.cpp:228
    frame #8: 0x00000001151dac22 libblink_web.dylib`blink::AudioDestinationNode::render(this=0x00003e0a02a01b30, sourceBus=0x0000000000000000, destinationBus=0x0000273abbe88b68, numberOfFrames=128) + 226 at AudioDestinationNode.cpp:82
    frame #9: 0x00000001151dad34 libblink_web.dylib`non-virtual thunk to blink::AudioDestinationNode::render(this=0x00003e0a02a01bf0, sourceBus=0x0000000000000000, destinationBus=0x0000273abbe88b68, numberOfFrames=128) + 68 at AudioDestinationNode.cpp:99
    frame #10: 0x0000000128ec3508 libblink_platform.dylib`blink::AudioDestination::provideInput(this=0x00000001385003a0, bus=0x0000273abbe88b68, framesToProcess=128) + 216 at AudioDestination.cpp:175
    frame #11: 0x0000000128ec356c libblink_platform.dylib`non-virtual thunk to blink::AudioDestination::provideInput(this=0x00000001385003a8, bus=0x0000273abbe88b68, framesToProcess=128) + 60 at AudioDestination.cpp:176
    frame #12: 0x0000000128ec57c5 libblink_platform.dylib`blink::AudioPullFIFO::fillBuffer(this=0x0000000138500440, numberOfFrames=256) + 117 at AudioPullFIFO.cpp:65
    frame #13: 0x0000000128ec5713 libblink_platform.dylib`blink::AudioPullFIFO::consume(this=0x0000000138500440, destination=0x0000273abbe88ab8, framesToConsume=256) + 147 at AudioPullFIFO.cpp:52
    frame #14: 0x0000000128ec340c libblink_platform.dylib`blink::AudioDestination::render(this=0x00000001385003a0, sourceData=0x000000013d800cc8, audioData=0x000000013d800cd8, numberOfFrames=256) + 620 at AudioDestination.cpp:164
    frame #15: 0x000000011fc3aa66 libcontent.dylib`content::RendererWebAudioDeviceImpl::Render(this=0x0000000138500960, dest=0x000000012c705c10, audio_delay_milliseconds=15) + 230 at renderer_webaudiodevice_impl.cc:90

will investigate.


### tk...@chromium.org (2014-12-05)

>    frame #4: 0x00000001151e01d2 libblink_web.dylib`blink::AudioNode::processIfNecessary(this=0x00003e0a02a02f78, framesToProcess=128) + 242 at AudioNode.cpp:391

This AudioNode was already GCed.
This node is in a GainNode change without a source node.  So, collecting it is a correct behavior.  Probably a raw pointer to the collected AudioNode (or AudioNodeOutput?) is left in a live object.


### tk...@chromium.org (2014-12-05)

> This node is in a GainNode change

change -> chain


### tk...@chromium.org (2014-12-05)

I confirmed the observation #2 was totally correct.  An object in AudioSummingJunction::m_renderingOutputs is swept.
Web Audio code had a mechanism to avoid AudioNode destruction during audio rendering before enabling Oilpan.


### tk...@chromium.org (2014-12-05)

I have no good ideas for now.

* We can make m_renderingOutputs strong references.  If we did so, AudioNodes without source nodes wouldn't be garbage-collected automatically.

* It might be possible to add a way to delay Oilpan sweep.  However, such changes can't be merged to branches.


### tk...@chromium.org (2014-12-05)

[Empty comment from Monorail migration]

### rt...@chromium.org (2014-12-05)

Re https://crbug.com/chromium/434136#c24. Pre-oilpan, webaudio managed ref counting itself and when all connection refs went away and the normal ref was going to be decremented to 0, webaudio would check if this was happening in the audio thread. If not, no problem. If so, the deref would be deferred by not dereffing (I think) and placing the node in a vector.  In the post-render handler, the vector of deferred derefs would be handled and the ref count would be finally decremented, deleting the objects.  Somewhere in there, downstream connections would be disconnected so that the graph would never try to pull on a node that would be deleted.

RE #25: What does "AudioNodes without source nodes" mean? And could webaudio do something to collect them?

I think we need to do something and leaking nodes is better than crashing.


### rt...@chromium.org (2014-12-05)

[Empty comment from Monorail migration]

### ma...@gmail.com (2014-12-08)

Intentionally leaking nodes doesn't seem like a good idea.
The overall cost of leaking a chain of seemingly simple nodes could be quite high, especially when one considers the owned audio busses (and other platform audio instances, like processors).

To be blunt (please forgive me, I'm tired), comparing the post-oilpan implementation to the pre-oilpan implementation I find:
* more code,
* code with more hard-to-reason-about runtime behaviour,
* incorrect bug-causing run-time-behaviour that constitutes a security risk with no obvious quick/long-fix. There might be more security bugs that are masquerading as one - we've found at least two so far.

By changing the code to intentionally leak, you'll be switching these security bugs for:
* still incorrect run-time-behaviour when compared to the WebAudio specification, by leaking in more edge-cases than the previous implementation did.

This might be an acceptable short-term situation if there was an ongoing effort to resolve the underlying design incompatibilities and if there were obvious and tangible benefits.
How does the WebAudio implementation (or maintainers/consumers) benefit from these recent oilpan changes?

Please correct me if I'm wrong, but all I see are problems. The current "bolt-on" oilpan implementation isn't a good solution to anything, other than perhaps one of code-consistency within the greater blink codebase.


***
As a short-term solution, is it possible to restore the pre-oilpan WebAudio implementation?

Better the custom-ref-counted devil we know. It was crazy, with it's two types of references, but it was secure and it mostly conformed to the WebAudio specification.


***
As a long-term solution, let us all collaborate on an oilpan-aware WebAudio implementation. One that offers tighter integration with oilpan, utilising things like it's stop-the-world GCs (and ephemeron fixed-point loops) to simplify the overall design. One that has easier-to-reason-about locking and thread safety. One that aims to address some of the long-standing bugs ( https://code.google.com/p/chromium/issues/detail?id=437126 for example).


I've been rambling about this now and then over here: https://groups.google.com/a/chromium.org/forum/#!topic/blink-dev/Tb10UapXwpg .
Please join-in when these WebAudio oil-fires have been extinguished.


### tk...@chromium.org (2014-12-08)

> RE #25: What does "AudioNodes without source nodes" mean? And could webaudio do something to collect them?

It means Math.random() <= 0.5 case in http://jsbin.com/mavade/1 addLongNodeGraph().  They are AudioNode objects in the graph, but to be collected.

#29,
Oilpan always clears swept memory.  So, we don't have a security risk.
Reverting Oilpan is a doable option, but it will be a large change and we can't merge it to branches.



### ma...@gmail.com (2014-12-08)

> Oilpan always clears swept memory.  So, we don't have a security risk.

Given the use of upstream raw pointers, and the runtime complexities of the code, how certain can we be that this is *always* safe?

Consider two connected nodes, "A" and "B". "A" is downstream to "B".
A GC event occurs. "A" remains alive but "B" is destructed.
Lets also assume that the renderer doesn't pick-up these changes. A GC or other graph mutation (from JS care-of the attacker) are tying up the graph lock, preventing handlePreRenderTasks from pulling them in through handleDirtyAudioSummingJunctions. Thus, at some point during rendering, "A" will attempt to pull from "B".
Nothing zeros "A"'s pointer to where "B" once was. An attacker could arrange for an array buffer to occupy the region formally occupied by "B". It is unlikely that the timings would work out, theres probably randomisation involved in allocation (I hope), but it is still a risk?

Or am I missing something that prevents this scenario, with absolute certainty?

### rt...@chromium.org (2014-12-08)

Re #29: I did not mean for intentionally leaking nodes to be a permanent solution. It's only a temporary solution until a solution is found.

I would not be opposed to removing Oilpan for now, but long-term, I think oilpan is here to stay.

### tk...@chromium.org (2014-12-09)

Oilpan team discussed this issue, and we had no good idea to resolve this in Oilpan.  So, we'll do:

1. Making m_renderingOutputs strong references to avoid crashes.  It will cause AudioNode leaks, but it's better than crash.   This change should be merged to Google Chrome 40 branch (and 39 too if possible)
2. Disable Oilpan in Web Audio.


### tk...@chromium.org (2014-12-09)

#31,
We have separated heaps for String buffer and array buffer.  It's same in non-Oilpan, but Oilpan is safer because of memory zero-fill.




### ma...@gmail.com (2014-12-09)

tkent #33:
If the pre-oilpan implementation is to be restored, why do m_renderingOutputs need to be strong references?
The pre-oilpan implementation was safe (enough), and didn't leak (too much).
Why change the old code beyond the absolute bare minimum required?

tkent #34:
Nice, separate heaps for "array buffer like" and "non-array buffer like". Thanks for the info. I now have yet more code to explore :)

In response, I change my argument in https://crbug.com/chromium/434136#c31 from:
> Nothing zeros "A"'s pointer to where "B" once was. An attacker could arrange for an array buffer to occupy the region formally occupied by "B".

to now read:
> Nothing zeros "A"'s pointer to where "B" once was. An attacker could arrange for a carefully chosen and configured oilpan object to occupy the region formally occupied by "B". By carefully chosen and configured I mean that the object has a memory footprint that is controllable in an appropriate way, such as having JS configurable member variables at the correct locations. There are, after all, plenty of objects to choose from.

To be clear, the crux of my argument is that "A"'s pointer to "B" is not zeroed. Thus "A"'s pointer now points to something unexpected, something that is theoretically capable of being exploited.

Thank you for your patience in answering my queries, I eagerly await your response to this latest barrage.

### rt...@chromium.org (2014-12-09)

For #33, I think tkent means that for M40 and M39 that has already been released, we cannot revert back to oilpan because such a change would be too large to be accepted by the M40 and M39 release managers.  Making m_renderingOutputs be a strong reference is probably small enough to be accepted and should fix these crashes (at the expense of leaking nodes).

Reverting oilpan will happen in ToT chromium.

tkent@: Please correct me if I'm wrong!

I am rather sad to see oilpan go. I can't help but think there is something wrong in the webaudio code itself that isn't keeping nodes around long enough.  Webaudio should keep these nodes alive until such a point that the audio graph knows they are no longer in use and can deref them after they have been removed from the graph and can never be accessed again.

### ha...@chromium.org (2014-12-10)

Reverting Oilpan is the last resort, and I think we should spend a bit more time in considering a way to fix the issue with Oilpan.

It is not only sad to revert Oilpan but also never easy for a couple of reasons:

- The WebAudio hierarchy is huge.

- AudioNode derives EventTarget, and AudioContext derives EventTarget and ActiveDOMObject. In Oilpan, both EventTarget and ActiveDOMObject are implemented assuming that they are on heap. If we want to put AudioNode and AudioContext off heap, we need to introduce another version of EventTarget and ActiveDOMObject. That seems way too complicated.


### ha...@chromium.org (2014-12-11)

Another idea (which might not work): What happens if we strongly trace m_renderingOutputs only in a GC that is triggered while the audio thread is doing rendering? In other GCs, we don't trace m_renderingOutputs.


### tk...@chromium.org (2014-12-11)

#38,
It's better than https://codereview.chromium.org/782603004/, but won't resolve this issue.  A typical WebAudio usage is to render audio all the time, I think.


### ma...@gmail.com (2014-12-11)

Re #38
It wouldn't stop the rug from pulled out from under the feet of the renderer.

Consider this scenario (best viewed in monospace):

----- increasing time ------>
[trace]        [sweep]                   (main thread)
             [render]                    (rendering thread)

At the precise moment of tracing, no rendering is being performed, thus the nodes will be deallocated during the sweep. Bad news for the renderer.

### rt...@chromium.org (2014-12-11)

Yes, once created, the audio thread basically never stops running, unless you use the just recently added context.suspend() method.

And as Mark says, tracing is not the problem.  Sweeping while the audio thread is rendering is the problem.

### bu...@chromium.org (2014-12-11)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=186914

------------------------------------------------------------------
r186914 | tkent@chromium.org | 2014-12-11T05:10:50.528063Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/modules/webaudio/AudioSummingJunction.cpp?r1=186914&r2=186913&pathrev=186914

Web Audio: Oilpan: Trace AudioSummingJunction::m_renderingOutputs

m_renderingOutpus is a vector of AudioNodeOutput raw pointers.  They are raw
pointers because the vector is allocated in the audio rendering thread, which
has no Oilpan support.  However, They can be last references to the AudioNodeOutput
objects, and Oilpan GC during audio rendering could collect the objects.  We
need to trace the contents of m_renderingOutputs.

This CL fixes crashes.  But unused AudioNodes in the graph are not
destructed automatically unless JavaScript code explicitly disconnect
them from the graph.

BUG=434136

Review URL: https://codereview.chromium.org/782603004
-----------------------------------------------------------------

### tk...@chromium.org (2014-12-15)

41.0.2249.0 canary doesn't crash with with http://jsbin.com/mavade/1 .  Request to merge r186482 and r186914.


### ma...@google.com (2014-12-15)

Approved for M40 (branch: 2214)

### bu...@chromium.org (2014-12-15)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=187106

------------------------------------------------------------------
r187106 | tkent@chromium.org | 2014-12-15T00:49:06.146377Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/branches/chromium/2214/Source/modules/webaudio/AudioContext.cpp?r1=187106&r2=187105&pathrev=187106
   M http://src.chromium.org/viewvc/blink/branches/chromium/2214/Source/modules/webaudio/AudioContext.h?r1=187106&r2=187105&pathrev=187106

Merge 186482 "Web Audio: Oilpan: Correctly trace m_referencedNod..."

> Web Audio: Oilpan: Correctly trace m_referencedNodes elements within a lock.
> 
> Blink r184963 [1] was not a right fix.  Oilpan marker pushed m_referencedNodes
> to a stack and released the lock immediately, then iterated it later.
> We need to make m_referencedNode HeapVector, not Member<HeapVector>
> to iterate it immediately.
> 
> [1] http://src.chromium.org/viewvc/blink?view=revision&revision=184963
> 
> BUG=434136
> 
> Review URL: https://codereview.chromium.org/776203002

TBR=tkent@chromium.org

Review URL: https://codereview.chromium.org/805713002
-----------------------------------------------------------------

### bu...@chromium.org (2014-12-15)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=187107

------------------------------------------------------------------
r187107 | tkent@chromium.org | 2014-12-15T00:50:58.973826Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/branches/chromium/2214/Source/modules/webaudio/AudioSummingJunction.cpp?r1=187107&r2=187106&pathrev=187107

Merge 186914 "Web Audio: Oilpan: Trace AudioSummingJunction::m_r..."

> Web Audio: Oilpan: Trace AudioSummingJunction::m_renderingOutputs
> 
> m_renderingOutpus is a vector of AudioNodeOutput raw pointers.  They are raw
> pointers because the vector is allocated in the audio rendering thread, which
> has no Oilpan support.  However, They can be last references to the AudioNodeOutput
> objects, and Oilpan GC during audio rendering could collect the objects.  We
> need to trace the contents of m_renderingOutputs.
> 
> This CL fixes crashes.  But unused AudioNodes in the graph are not
> destructed automatically unless JavaScript code explicitly disconnect
> them from the graph.
> 
> BUG=434136
> 
> Review URL: https://codereview.chromium.org/782603004

TBR=tkent@chromium.org

Review URL: https://codereview.chromium.org/799613005
-----------------------------------------------------------------

### tk...@chromium.org (2014-12-15)

I'd like to merge r186482 and r186914 to M39 branch too if we have another M39 push.


### cl...@chromium.org (2014-12-15)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-12-15)

No more m39 pushes.

### in...@chromium.org (2014-12-15)

[Empty comment from Monorail migration]

### ti...@google.com (2015-01-22)

Congratulations - $4000 for this report! Notes from reward panel: "2 bugs here @ $2000 per bug. Thanks for being so helpful as well!"

We've credited you in the Chrome release notes as "mark.buer". Let me know if you want to use a different name/handle and we'll be in contact in a few weeks to arrange payment.

### ma...@gmail.com (2015-01-23)

Wow! Fantastic :-) Thank you Google.

Some of the investigation for this was done on work time, thus could we please have the release notes credit:

mark.buer@booktrack.com

Thanks again.

### ti...@google.com (2015-01-23)

Done: http://googlechromereleases.blogspot.com/2015/01/stable-update.html

Thanks Mark!

### tk...@chromium.org (2015-02-06)

https://crbug.com/chromium/455993 covers the intentional leak by Blink r186914.


### bu...@chromium.org (2015-02-17)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=190366

------------------------------------------------------------------
r190366 | tkent@chromium.org | 2015-02-17T23:48:19.934304Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/platform/heap/ThreadState.cpp?r1=190366&r2=190365&pathrev=190366
   M http://src.chromium.org/viewvc/blink/trunk/Source/modules/webaudio/AudioContext.cpp?r1=190366&r2=190365&pathrev=190366
   M http://src.chromium.org/viewvc/blink/trunk/Source/modules/webaudio/AudioNode.cpp?r1=190366&r2=190365&pathrev=190366
   M http://src.chromium.org/viewvc/blink/trunk/Source/platform/heap/Heap.cpp?r1=190366&r2=190365&pathrev=190366
   M http://src.chromium.org/viewvc/blink/trunk/Source/platform/heap/HeapTest.cpp?r1=190366&r2=190365&pathrev=190366
   M http://src.chromium.org/viewvc/blink/trunk/Source/platform/heap/ThreadState.h?r1=190366&r2=190365&pathrev=190366
   M http://src.chromium.org/viewvc/blink/trunk/Source/modules/webaudio/AudioContext.h?r1=190366&r2=190365&pathrev=190366
   M http://src.chromium.org/viewvc/blink/trunk/Source/modules/webaudio/AudioSummingJunction.cpp?r1=190366&r2=190365&pathrev=190366
   M http://src.chromium.org/viewvc/blink/trunk/Source/platform/heap/Heap.h?r1=190366&r2=190365&pathrev=190366

WebAudio: Fix AudioNode leak in a case that AudioNode is not disconnected from the graph explicitly.

The main purpose of this CL is to introduce ThreadState::markAsZombie
and ThreadState::purifyZombies, and to apply them for WebAudio.
Objects marked as zombies are not finalized until purifyZombies is
called.

This CL also adds MarkingTasks, which enable to run tasks before/
after Oilpan marking. AudioContext implements MarkingTask in order to
call purifyZombie before marking, and simplify AudioContext::trace.


BUG=434136,455993

Review URL: https://codereview.chromium.org/802593004
-----------------------------------------------------------------

### bu...@chromium.org (2015-02-20)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=190508

------------------------------------------------------------------
r190508 | tkent@chromium.org | 2015-02-20T00:49:38.435664Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/platform/heap/ThreadState.cpp?r1=190508&r2=190507&pathrev=190508
   M http://src.chromium.org/viewvc/blink/trunk/Source/modules/webaudio/AudioContext.cpp?r1=190508&r2=190507&pathrev=190508
   M http://src.chromium.org/viewvc/blink/trunk/Source/modules/webaudio/AudioNode.cpp?r1=190508&r2=190507&pathrev=190508
   M http://src.chromium.org/viewvc/blink/trunk/Source/platform/heap/Heap.cpp?r1=190508&r2=190507&pathrev=190508
   M http://src.chromium.org/viewvc/blink/trunk/Source/platform/heap/HeapTest.cpp?r1=190508&r2=190507&pathrev=190508
   M http://src.chromium.org/viewvc/blink/trunk/Source/platform/heap/ThreadState.h?r1=190508&r2=190507&pathrev=190508
   M http://src.chromium.org/viewvc/blink/trunk/Source/modules/webaudio/AudioContext.h?r1=190508&r2=190507&pathrev=190508
   M http://src.chromium.org/viewvc/blink/trunk/Source/modules/webaudio/AudioSummingJunction.cpp?r1=190508&r2=190507&pathrev=190508
   M http://src.chromium.org/viewvc/blink/trunk/Source/platform/heap/Heap.h?r1=190508&r2=190507&pathrev=190508

Revert of WebAudio: Fix AudioNode leak in a case that AudioNode is not disconnected from the graph explicitly. (patchset #5 id:100001 of https://codereview.chromium.org/802593004/)

Reason for revert:
Caused multiple problems.  crbug.com/459605 crbug.com/459862 crbug.com/460254

Original issue's description:
> WebAudio: Fix AudioNode leak in a case that AudioNode is not disconnected from the graph explicitly.
> 
> The main purpose of this CL is to introduce ThreadState::markAsZombie
> and ThreadState::purifyZombies, and to apply them for WebAudio.
> Objects marked as zombies are not finalized until purifyZombies is
> called.
> 
> This CL also adds MarkingTasks, which enable to run tasks before/
> after Oilpan marking. AudioContext implements MarkingTask in order to
> call purifyZombie before marking, and simplify AudioContext::trace.
> 
> 
> BUG=434136,455993
> 
> Committed: https://src.chromium.org/viewvc/blink?view=rev&revision=190366

TBR=oilpan-reviews@chromium.org,rtoy@chromium.org,haraken@chromium.org
NOPRESUBMIT=true
NOTREECHECKS=true
NOTRY=true
BUG=434136,455993

Review URL: https://codereview.chromium.org/940963005
-----------------------------------------------------------------

### ti...@google.com (2015-03-09)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-03-23)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2015-06-03)

Processing via our *new* e-payment system should only take a 7-10 days and the reward should be on its way to you. Thanks again for your help!

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

This issue was migrated from crbug.com/chromium/434136?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/428249, crbug.com/chromium/431546]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080869)*
