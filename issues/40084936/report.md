# Use-after-poison in blink::CompositorAnimationPlayer::NotifyAnimationStarted

| Field | Value |
|-------|-------|
| **Issue ID** | [40084936](https://issues.chromium.org/issues/40084936) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Animation |
| **Platforms** | Linux |
| **Reporter** | at...@gmail.com |
| **Assignee** | al...@chromium.org |
| **Created** | 2016-07-25 |
| **Bounty** | $3,500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5078527401787392

Fuzzer: attekett_dom_fuzzer
Job Type: linux_asan_chrome_media
Platform Id: linux

Crash Type: Use-after-poison READ 8
Crash Address: 0x7e9287e2d1d0
Crash State:
  blink::CompositorAnimationPlayer::NotifyAnimationStarted
  cc::ElementAnimations::NotifyAnimationStarted
  cc::AnimationHost::SetAnimationEvents
  
Recommended Security Severity: High

Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_media&range=376988:377035

Minimized Testcase (0.65 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv95G5jt1IuF1YDuD6-CrBL5SrKpxEN-PTOXLjDhvuK_dm3UigX7E1fqGxmXvolSEtUYcgal2k-JJkPV37CRGE9-ZLYmm4V05osYCkBjQtFtxXxt2wk7dlWgfPdwa7YBK5Yx_aoMagti8ed66R7m0gO0b5h7-5Q?testcase_id=5078527401787392
<menu id="app-context-menu">
<script> 
function convertArrayToStrings(array){; return array};
var test0=document.getElementById("app-context-menu")
var test1=test0.appendChild(document.createElement("ul"))
var test3=test1.appendChild(document.createElement("cite"))
var test4=test0.appendChild(document.createElement("font"))
var test7=test3.appendChild(document.createElement("marquee"))

setInterval(function(){
test4.appendChild(test7.cloneNode());
})

test4.style.zoom=3.525269266217947


setTimeout(function(){
})
setTimeout(function(){
test7.style.zoom=3.525269266217947
})


setTimeout(function(){
})
document.body.style.zoom=3.5822747899219394


</script>


Filer: aarya

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

## Timeline

### aa...@google.com (2016-07-25)

regression from https://chromium.googlesource.com/chromium/src/+/8ce9d13097b1b0e14b9710b0b2670a510e258502

### ke...@chromium.org (2016-07-25)

[Empty comment from Monorail migration]

[Monorail components: Blink>Scroll]

### ym...@chromium.org (2016-07-26)

[Comment Deleted]

### sh...@chromium.org (2016-07-26)

[Empty comment from Monorail migration]

### ym...@chromium.org (2016-07-26)

Debugging further, it looks like the CompositorAnimationPlayer is bogus to begin with. Looking into it further...

### ym...@chromium.org (2016-07-26)

The range in the bug is wrong. The crash is reproducible well before the oldest change in the range.

I did a manual bisect and got this narrow range:
https://chromium.googlesource.com/chromium/src/+log/29a24a77f2641ec45924093e06049ad03cdcaa5a..0c56dabf4895816405464b4955d4824c56e450a3

Reverting https://codereview.chromium.org/1698093005 fixes the crash.

Assigning to alancutter.

### al...@chromium.org (2016-07-27)

Ran a (non-asan) debug build of content_shell and hit the crash site after a couple of minutes.
At frame 1 cc::ElementAnimations::NotifyPlayersAnimationStarted() it's iterating through players_list_ and the current value of node is 0x3636363636363636 which looks rather dodgy.

players_list_->head() and players_list_->end() look normal (0x35113e1c5c68 and 0x35113c64f390 respectively).



cc::AnimationPlayer inherits from base::RefCounted and base::LinkNode.
base::LinkNode has no destructor.
~AnimationPlayer() doesn't remove itself from a linked list if it's in one.
I believe this is the root cause of the crash, my patch probably just makes it more likely that AnimationPlayers are cleaned up.

### al...@chromium.org (2016-07-27)

Looks like my theory is incorrect, AnimationPlayer is never in a linked list by the time ~AnimationPlayer() is called during this crash repro.

### al...@chromium.org (2016-07-27)

Tried making cc::AnimationPlayer inherit from base::RefCountedThreadSafe since blink::CompositorAnimationPlayer has a scoped_refptr to it.
Didn't fix the crash but seems like something that should be done anyway.

### al...@chromium.org (2016-07-27)

Small breakthrough, node seems to get deleted during the callback.

#3  0x00007ffff1266036 in cc::ElementAnimations::NotifyPlayersAnimationStarted (this=0x252cbf8126e0, 
    monotonic_time=19 days, 4:37:56.787160, target_property=cc::TargetProperty::TRANSFORM, group=99)
    at ../../cc/animation/element_animations.cc:1444
1444        DCHECK(node->next() != (void*)(0x3636363636363636));
(gdb) l
1439      for (PlayersListNode* node = players_list_->head();
1440           node != players_list_->end(); node = node->next(), count++) {
1441        DCHECK(node->next() != (void*)(0x3636363636363636));
1442        AnimationPlayer* player = node->value();
1443        player->NotifyAnimationStarted(monotonic_time, target_property, group);
1444        DCHECK(node->next() != (void*)(0x3636363636363636));
1445      }
1446    }
1447
1448    void ElementAnimations::NotifyPlayersAnimationFinished(

Notice it's the second DCHECK that fails, not the first.

Capturing next = node->next(); before calling the callback doesn't seem to fix the crash though but now node dereferences to 0x3636363636363636 instead of equalling it.

### al...@chromium.org (2016-07-27)

[Empty comment from Monorail migration]

[Monorail components: -Blink>Scroll Blink>Animation]

### al...@chromium.org (2016-07-27)

I believe the proper fix would be to replace the use of base::LinkedList with base::ObserverList however that's unlikely to be suitable for merging into stable.
A "quick fix" patch is not obvious to me here.

I'm out for the day, passing on to ymalik to take over.

### aj...@chromium.org (2016-07-27)

To summarize the current state, it sounds like we're now (more aggressively?) deleting animations during NotifyAnimationStarted, which (in this example) results in the currently visited node and its successor node getting deleted during NotifyAnimationStarted, which breaks the iteration in ElementAnimations::NotifyPlayersAnimationStarted since we're using a linked list.

Using base::ObserverList seems like the right fix to me too. I tried thinking of "quick fixes", but everything I could think of amounted to hackily re-implementing some of the functionality of ObserverList on top of a linked list, which actually seems riskier to me.

### ym...@chromium.org (2016-07-27)

I agree that base::ObserverList is probably what we need. I also agree that this fix is unlikely suitable for merging into stable. FWIW, alancutter's change that made this crash more visible made it to M50, and it doesn't seem to be a real issue in practice. 

### ym...@chromium.org (2016-07-27)

I verified that using base::ObserverList fixes the crash. Patch here: https://codereview.chromium.org/2189813002/

@allancutter can you verify that this indeed fixes the crash.

### al...@chromium.org (2016-07-28)

Thanks for continuing the work here.

If my patch reverted cleanly then it would probably a good candidate for merging into stable. Unfortunately there are conflicts when reverting on ToT and since it's of a memory management nature I doubt it's safe to merge.

I'm unable to build https://codereview.chromium.org/2189813002/, animation_player_observer.h is missing from the upload.

### al...@chromium.org (2016-07-28)

I made an attempt at a mergeable patch by taking refs of players_list_ before iteration but it didn't work, I'm not entirely sure why.
Posting it here for information sharing.
https://codereview.chromium.org/2187813003

### ym...@chromium.org (2016-07-28)

re #16, animation_player_observer.h was removed but I forgot to remove it from the includes. Please try again.

### jb...@chromium.org (2016-07-28)

#17: Re-reading the above, it sounded from above that the problem was removal from players_list_, rather than the player itself being freed. If so, taking a ref won't prevent it from being removed from players_list_.

(Aside: The unit test in ymalik's CL calls AnimationTimeline::DetachPlayer, which more calls ElementAnimations::RemovePlayer after some indirection, then destroys it. I think it's the ElementAnimations::RemovePlayer bit that's connected to the corruption of players_list_, rather than the destruction.)

### al...@chromium.org (2016-07-28)

I'm still seeing the crash with https://codereview.chromium.org/2189813002/ applied running an ASAN build of content_shell.

    #0 0x7f5ba9fdd0d2 in ?? ./out/asan/../../third_party/WebKit/Source/platform/animation/CompositorAnimationPlayer.cpp:92:21
    #1 0x7f5bae43813e in NotifyPlayersAnimationFinished ./out/asan/../../cc/animation/element_animations.cc:1440:3
    #2 0x7f5bae421c6f in SetAnimationEvents ./out/asan/../../cc/animation/animation_host.cc:320:27
    #3 0x7f5bae757503 in SetAnimationEvents ./out/asan/../../cc/trees/layer_tree_host.cc:757:20
    #4 0x7f5bae83ce89 in SetAnimationEvents ./out/asan/../../cc/trees/proxy_main.cc:99:21

### ym...@chromium.org (2016-07-28)

I verified that my unittest crashes in the same way in the linked list case (without my patch). I didn't test my patch on asan actually. looking.. 

### al...@chromium.org (2016-07-28)

#19: I also added a check for whether node is nullptr in the loop condition. If the current node gets removed then next will be nullptr and the loop should terminate. Probably not correct behaviour but shouldn't crash.

I believe the players_list_ is mutated by blink::Animation getting GC'd resulting in the following call chain:
=> ~Animation()
=> destroyCompositorPlayer()
=> detachCompositorTimeline()
=> timeline->playerDestroyed(*this)
=>  m_animationTimeline->DetachPlayer(client.compositorPlayer()->animationPlayer())

### ym...@chromium.org (2016-07-28)

Yeah, it still crashes on ASAN with https://codereview.chromium.org/2189813002/. Not sure what's going on.

I'm OOO for the day. @alancutter, sending it your way.

### al...@chromium.org (2016-07-28)

https://chromium.googlesource.com/chromium/src/+/master/third_party/WebKit/Source/platform/heap/BlinkGCAPIReference.md#GarbageCollectedFinalized states that "finalization is done at an arbitrary time after the object becomes unreachable."

I believe that the blink::Animation object that owns the CompositorAnimationPlayer is being poisoned prior to ~Animation executing and getting a chance to free CompositorAnimationPlayer which in its destructor would remove the cc::AnimationPlayer from cc::ElementAnimations.

blink::Animations needs to use Oilpan's USING_PRE_FINALIZER() macro to ensure the handles to it from the impl thread get cleaned up before it gets poisoned.

### al...@chromium.org (2016-07-28)

Created two line fix that no longer crashes ASAN content_shell, please confirm patch: https://codereview.chromium.org/2188623006


Other TODOs to do that came out of this investigation:
 - Use ObserverList for players_list_(https://codereview.chromium.org/2189813002/)
 - Make cc::AnimationPlayer inherit from RefCountedThreadSafe
 - Make blink::Animation's destructor virtual


### al...@chromium.org (2016-07-28)

[Empty comment from Monorail migration]

### ym...@chromium.org (2016-07-28)

Can confirm that the crash is gone on ASAN with https://codereview.chromium.org/2188623006.

Though, I get the following assertion failure on a debug build.

ASSERTION FAILED: !m_orderedPreFinalizers.contains(PreFinalizer(self, T::invokePreFinalizer))
../../third_party/WebKit/Source/platform/heap/ThreadState.h(403) : void blink::ThreadState::registerPreFinalizer(T *) [T = blink::Animation]

Received signal 11 SEGV_MAPERR 0000fbadbeef
#0 0x7fe005dafe5e base::debug::StackTrace::StackTrace()
#1 0x7fe005daf99f base::debug::(anonymous namespace)::StackDumpSignalHandler()
#2 0x7fdff34a9330 <unknown>
#3 0x7fdfed682db7 blink::ThreadState::registerPreFinalizer<>()
#4 0x7fdfed67e3f5 blink::Animation::createCompositorPlayer()
#5 0x7fdfed67e21b blink::Animation::preCommit()
#6 0x7fdfed6db3b6 blink::CompositorPendingAnimations::update()
#7 0x7fdfed6e2e7e blink::DocumentAnimations::updateCompositorAnimations()
#8 0x7fdfee04022c blink::PaintLayerCompositor::updateIfNeededRecursiveInternal()
#9 0x7fdfee03ff3b blink::PaintLayerCompositor::updateIfNeededRecursive()




### bu...@chromium.org (2016-07-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/7fec064b3a37032605f091ba1ba52846c0e05824

commit 7fec064b3a37032605f091ba1ba52846c0e05824
Author: alancutter <alancutter@chromium.org>
Date: Fri Jul 29 02:03:30 2016

Add pre finalizer to Animation to ensure compositor handles get cleaned up

BUG=631052

Review-Url: https://codereview.chromium.org/2188623006
Cr-Commit-Position: refs/heads/master@{#408554}

[modify] https://crrev.com/7fec064b3a37032605f091ba1ba52846c0e05824/third_party/WebKit/Source/core/animation/Animation.cpp
[modify] https://crrev.com/7fec064b3a37032605f091ba1ba52846c0e05824/third_party/WebKit/Source/core/animation/Animation.h


### al...@chromium.org (2016-07-29)

[Empty comment from Monorail migration]

### go...@chromium.org (2016-07-29)

+ awhalley for M52 and M53 approval. Change listed at #28 is not yet baked in Canary. 

### sh...@chromium.org (2016-07-29)

[Empty comment from Monorail migration]

### di...@chromium.org (2016-07-30)

[Automated comment] Request affecting a post-stable build (M52), manual review required.

### di...@chromium.org (2016-07-30)

Your change meets the bar and is auto-approved for M53 (branch: 2785)

### di...@chromium.org (2016-07-30)

[Automated comment] Request affecting a post-stable build (M52), manual review required.

### cl...@chromium.org (2016-07-31)

ClusterFuzz has detected this issue as fixed in range 408444:408557.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5078527401787392

Fuzzer: attekett_dom_fuzzer
Job Type: linux_asan_chrome_media
Platform Id: linux

Crash Type: Use-after-poison READ 8
Crash Address: 0x7e9287e2d1d0
Crash State:
  blink::CompositorAnimationPlayer::NotifyAnimationStarted
  cc::ElementAnimations::NotifyAnimationStarted
  cc::AnimationHost::SetAnimationEvents
  
Recommended Security Severity: High

Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_media&range=376988:377035
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_media&range=408444:408557

Minimized Testcase (0.65 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv95G5jt1IuF1YDuD6-CrBL5SrKpxEN-PTOXLjDhvuK_dm3UigX7E1fqGxmXvolSEtUYcgal2k-JJkPV37CRGE9-ZLYmm4V05osYCkBjQtFtxXxt2wk7dlWgfPdwa7YBK5Yx_aoMagti8ed66R7m0gO0b5h7-5Q?testcase_id=5078527401787392
<menu id="app-context-menu">
<script> 
function convertArrayToStrings(array){; return array};
var test0=document.getElementById("app-context-menu")
var test1=test0.appendChild(document.createElement("ul"))
var test3=test1.appendChild(document.createElement("cite"))
var test4=test0.appendChild(document.createElement("font"))
var test7=test3.appendChild(document.createElement("marquee"))

setInterval(function(){
test4.appendChild(test7.cloneNode());
})

test4.style.zoom=3.525269266217947


setTimeout(function(){
})
setTimeout(function(){
test7.style.zoom=3.525269266217947
})


setTimeout(function(){
})
document.body.style.zoom=3.5822747899219394


</script>


See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### bu...@chromium.org (2016-08-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/6f29a4298592591e73ba3a05b8244f4669d1d90e

commit 6f29a4298592591e73ba3a05b8244f4669d1d90e
Author: Alan Cutter <alancutter@chromium.org>
Date: Mon Aug 01 00:26:43 2016

Add pre finalizer to Animation to ensure compositor handles get cleaned up

BUG=631052

Review-Url: https://codereview.chromium.org/2188623006
Cr-Commit-Position: refs/heads/master@{#408554}
(cherry picked from commit 7fec064b3a37032605f091ba1ba52846c0e05824)

Review URL: https://codereview.chromium.org/2198723002 .

Cr-Commit-Position: refs/branch-heads/2785@{#422}
Cr-Branched-From: 68623971be0cfc492a2cb0427d7f478e7b214c24-refs/heads/master@{#403382}

[modify] https://crrev.com/6f29a4298592591e73ba3a05b8244f4669d1d90e/third_party/WebKit/Source/core/animation/Animation.cpp
[modify] https://crrev.com/6f29a4298592591e73ba3a05b8244f4669d1d90e/third_party/WebKit/Source/core/animation/Animation.h


### aw...@chromium.org (2016-08-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-08-02)

Nice one, $3,500 for this bug.

### aw...@chromium.org (2016-08-04)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-08-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/66cb1320242db9ce2954a539dc2d5410bf033dbd

commit 66cb1320242db9ce2954a539dc2d5410bf033dbd
Author: ymalik <ymalik@chromium.org>
Date: Fri Aug 05 20:01:07 2016

ElementAnimations should hold an ObservableList of AnimationPlayers.

Before this, the AnimationPlayers were held in a linked list, and
modifying the list while iterating could cause undefined behavior.

BUG=631052
CQ_INCLUDE_TRYBOTS=master.tryserver.blink:linux_precise_blink_rel

Review-Url: https://codereview.chromium.org/2189813002
Cr-Commit-Position: refs/heads/master@{#410152}

[modify] https://crrev.com/66cb1320242db9ce2954a539dc2d5410bf033dbd/cc/animation/animation_player.h
[modify] https://crrev.com/66cb1320242db9ce2954a539dc2d5410bf033dbd/cc/animation/element_animations.cc
[modify] https://crrev.com/66cb1320242db9ce2954a539dc2d5410bf033dbd/cc/animation/element_animations.h
[modify] https://crrev.com/66cb1320242db9ce2954a539dc2d5410bf033dbd/cc/animation/element_animations_unittest.cc
[modify] https://crrev.com/66cb1320242db9ce2954a539dc2d5410bf033dbd/cc/test/animation_timelines_test_common.cc


### aw...@chromium.org (2016-08-10)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-08-30)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-09-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-11-04)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### ad...@google.com (2021-03-25)

[Empty comment from Monorail migration]

### is...@google.com (2021-03-25)

This issue was migrated from crbug.com/chromium/631052?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084936)*
