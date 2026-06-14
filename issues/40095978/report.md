# Use-after-poison in blink::Node::EnsureEventTargetData

| Field | Value |
|-------|-------|
| **Issue ID** | [40095978](https://issues.chromium.org/issues/40095978) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>DOM, Blink>GarbageCollection, Blink>JavaScript>GarbageCollection |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | cl...@chromium.org |
| **Assignee** | om...@chromium.org |
| **Created** | 2019-08-13 |
| **Bounty** | $3,000.00 |

## Description

Detailed report: https://clusterfuzz.com/testcase?key=6219506298257408

Fuzzer: domino
Job Type: linux_asan_chrome_v8_arm
Platform Id: linux

Crash Type: Use-after-poison READ 4
Crash Address: 0xe9f81938
Crash State:
  blink::Node::EnsureEventTargetData
  blink::EventTarget::AddEventListenerInternal
  blink::EventTarget::addEventListener
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_v8_arm&range=684580:684590

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6219506298257408

Additional requirements: Requires HTTP

Issue filed automatically.

See https://github.com/google/clusterfuzz-tools for instructions to reproduce this bug locally.

## Timeline

### cl...@chromium.org (2019-08-13)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Blink>DOM]

### sh...@chromium.org (2019-08-14)

Setting milestone and target because of Security_Impact=Head and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-08-14)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-08-14)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2019-08-14)

So I have to take ownership of this bug just to be able to see what it is?

### [Deleted User] (2019-08-14)

The repro html is:
<script src='script-86.js'></script>
<script>
  window.addEventListener('load', start)
</script>

and script-86.js is:
window.o = {}
o[1] = document
 o[4] = o[1].createElementNS('http://www.w3.org/1999/xhtml', 'canvas') 
 o[3] = o[4].getContext('webgl2', { antialias: false}) 
 o[5] = o[3].createProgram() 
 o[6] = o[3].createShader(o[3].VERTEX_SHADER) 
 o[3].attachShader(o[5], o[6]) 
 o[4].setAttribute('height', 1) 
 o[4].width = 32767 
 gc();  
 o[3].getAttachedShaders(o[5]) 
 o[4].height = -1 
 o[4].addEventListener([32], {}) 

The gc() is apparently collecting map at [1]. Which it doesn't look like it should do, since it is DEFINE_STATIC_LOCAL. By my reading of that macro, it should be protected from this type of ASAN use after poison.

I'm ccing keishi@chromium.org (because of [2]) - do you have better context on this one?

The clusterfuzz regression range ([3]) doesn't look right, but maybe I missed something.

[1] https://cs.chromium.org/chromium/src/third_party/blink/renderer/core/dom/node.cc?rcl=aa07cbc3c366378d2797ad8a73f61c0099eba6e5&l=2114
[2] https://chromium.googlesource.com/chromium/src/+/aa07cbc3c366378d2797ad8a73f61c0099eba6e5
[3] https://chromium.googlesource.com/chromium/src/+log/b3fea0a48363b35641da71c93d3301b4d3ebe39d..b0aef7a480856b0089f25074550e4949b8f447e7?pretty=fuller&n=10000

[Monorail components: Blink>JavaScript>GC Infra>Client>Oilpan]

### jd...@chromium.org (2019-08-19)

I'm going to assign this to keishi@ based on c#6 for now. keishi@: feel free to re-assign if you think there's someone with more context; I just want to make sure this bug gets attention from someone. Thanks!

- a friendly security sheriff

### sh...@chromium.org (2019-08-28)

keishi: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-09-11)

keishi: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sr...@google.com (2019-09-11)

keishi@ friendly ping , to help take a look into this issue

### sr...@google.com (2019-09-17)

Friendly ping !

### ke...@chromium.org (2019-09-18)

Regression range contains r684588  Reland "heap: Enable concurrent sweeping" so I think it could be related.
https://chromium.googlesource.com/chromium/src/+log/b3fea0a48363b35641da71c93d3301b4d3ebe39d..b0aef7a480856b0089f25074550e4949b8f447e7?pretty=fuller&n=10000

bikineev, would you take a look? Thanks

### sr...@google.com (2019-09-30)

bikineev@ can you ptal, this is marked as RBS for M78 stable, and we are in beta for M78, pls help review if this is stable blocker if not pls remove the label

### bi...@chromium.org (2019-09-30)

I don't see any way how it might be related to concurrent sweeping. Concurrent sweeping can make the bug more reproducible (since memory reclamation happens faster). I suppose the actual issue is somewhere in the user code.

### sr...@google.com (2019-10-01)

+adetaylor@ can you ptal and see which team should look into this issue

### ad...@chromium.org (2019-10-01)

I'm punting this back to keishi@ who, based on https://crbug.com/chromium/993415#c6, probably has best understanding of DEFINE_STATIC_LOCAL and thus the best chance to decide why it may have been freed unexpectedly. (From a brief look I agree with the analysis in https://crbug.com/chromium/993415#c6 that this does appear to be the map which has been freed).

One other thing, though. inferno@ - how much do we trust the testcase minimizer? The minimized test case still includes some WebGL stuff. Do we trust that this is strictly necessary for the problem to reproduce? If so perhaps it could be something wacky involving GPU buffer allocation overwriting other memory? (Far fetched maybe).

I haven't tried to reproduce this, but for anyone who can, it might be interesting to remove the JS code related to the canvas and see if it still repros.

### sr...@google.com (2019-10-03)

keishi@ can you ptal at this , also should this be RBS for M78 - adetaylor@ 

### ad...@chromium.org (2019-10-04)

ClusterFuzz claims that this was introduced in M78, therefore is a regression, therefore should indeed be RBS.

The regression task has been run twice, and each time landed upon the same commit range - https://chromium.googlesource.com/chromium/src/+log/b3fea0a48363b35641da71c93d3301b4d3ebe39d..b0aef7a480856b0089f25074550e4949b8f447e7?pretty=fuller&n=10000
The only one of those that seems plausible is the commit to enable concurrent sweeping: 204cc754589917b51d9f80ff93dd67dbf1a4f74.

It seems to me that we will need to revert that commit unless we find an explanation for this sooner. Per https://crbug.com/chromium/993415#c14, the concurrent sweeping merely reveals the problem rather than causing it, but even if that's the case we don't want to do anything that makes exploitable bugs more realistically exploitable, so it would still need to be reverted. Also, honestly, it seems a bit weird that a static local hashmap would ever be subject to GC, so I am slightly suspicious that this actually is a bug in concurrent GC (though I know nothing about it so that's an argument based on coincidences rather than actual technical knowledge).

I suppose there's a third option which is that somehow the concurrent GC is not adequately communicating the nature of pages across to ASAN. I've no idea how that stuff works, either :)

bikineev@, we'd really appreciate your help in the investigation too. +mlippautz@ and haraken@ who have been involved in the concurrent GC design document.

### ad...@google.com (2019-10-04)

I had a chat with inferno@ about this and he suspects that the WebGL/big height things within the minimized test case may well be relevant, or the test case minimizer would indeed have removed them.

He also points out another repro of the same call stack - https://clusterfuzz.com/testcase-detail/5137295091826688. The regression range here is different! - and doesn't have any smoking guns related to GC at all.

So I think we do need keishi@ or somebody to speculate about how that DEFINE_STATIC_LOCAL structure could possibly have been GCed, or how we can investigate more.

### ha...@chromium.org (2019-10-04)

bikineev@: Can you reproduce the issue locally? If yes, you can disable the concurrent sweeping and see whether the issue is gone.


### ml...@chromium.org (2019-10-04)

Folks, we have a reproducer since August 13, that's for 1.5 months (!)

Why do we think concurrent sweeping is related? It's is not the first time it is reverted because it flushed out an unrelated issue.

bikineev@ is OOO and I only have access to a machine to debug this on Monday.

### hp...@chromium.org (2019-10-04)

We need a Blink person to own the issue and look into it. haraken@, do you have somebody who has time and knows how to debug this?

### ml...@chromium.org (2019-10-04)

After discussing this offline: omerkatz@ will take a look today and I can join on Monday. Thanks!

[Monorail components: -Infra>Client>Oilpan Blink>MemoryAllocator>GarbageCollection]

### ha...@chromium.org (2019-10-04)

keishi@ has been looking into this and not yet succeeded in reproducing.


### om...@chromium.org (2019-10-04)

[Comment Deleted]

### om...@chromium.org (2019-10-04)

Successfully reproduced by checking out revision 686342 and building with gn args from clusterfuzz:
enable_ipc_fuzzer = true
enable_nacl = false
is_asan = true
is_component_build = false
is_debug = false
strip_absolute_paths_from_debug_symbols = true
target_cpu = "x86"
use_goma = true
v8_enable_verify_heap = true
v8_target_cpu = "arm"

Running the minimized test case on the produced chrome binary reproduces the asan error.

Note that these gn args produce a 32bit binary that requires x86 libraries.

### om...@chromium.org (2019-10-04)

[Comment Deleted]

### cl...@chromium.org (2019-10-04)

ClusterFuzz testcase 6219506298257408 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_v8_arm&range=696357:696387

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### bu...@chromium.org (2019-10-04)

[Auto-generated comment by a script] We noticed that this issue is targeted for M-78; it appears the fix may have landed after branch point, meaning a merge might be required. The owner of this bug should confirm if a merge is required here. If so, add Merge-Request-78 label and indicate which commits/CLs are to be merged. Otherwise, remove Merge-TBD label. Thanks.

### om...@chromium.org (2019-10-04)

This issue is not fixed.
It was hidden, not fixed, by revision 696359 (which I submitted and am now reverting).
The crash is still reproducible on tip-of-tree as of today.

It is also not due to concurrent sweeping.
The range reported by clusterfuzz (684580-684590) is wrong.
This issue is reproducible at least from revision 684000.

### om...@chromium.org (2019-10-04)

[Empty comment from Monorail migration]

### ha...@chromium.org (2019-10-04)

Nice detective work! Sorry for suspecting the concurrent sweeping...


### sr...@google.com (2019-10-04)

omerkatz@ currently it is marked as RBS for M78, Does this issue seem critical enough for that? if so can you pls remove the RBS label .

### ad...@chromium.org (2019-10-04)

omerkatz@ haraken@ and mlippautz@ thanks a lot for jumping on this.

In particular omerkatz@ thanks for getting to the point of being able to reproduce this. You inspired me to succeed in reproducing it too. A few more hints on how:
How to install 32-bit libraries:
sudo apt-get install libcups2:i386 libatk1.0-0:i386 libatk-bridge2.0-0:i386 libgtk-3-0:i386
How to launch Chrome:
./out/repro/chrome --js-flags='--expose_gc'


### om...@chromium.org (2019-10-04)

Thanks adetaylor@ for filling the gap I left in my repro instructions.
I'm close to narrowing down which CL introduced this crash.
Will update when I get there.

### ad...@chromium.org (2019-10-04)

OK cool. In order to answer srinivassista's question, just checked out 0cdcc6158160790658d1f033d3db873603250124, which is the base revision for the M77 branch, and it still appears to repro for me. So I'm going to mark this as Security_Impact-Stable and remove the RBS label. Obviously we still need to figure out the fix, so I'm really glad you're on the case. Thanks again!

### om...@chromium.org (2019-10-04)

This crash was introduced by r679175 and is still reproducible on tip-of-tree today.
Unfortunately the culprit CL is "Update V8 to version 7.7.281" which doesn't tell me anything useful. (time well wasted...)
mlippautz@ and hpayer@, since you're more familiar with V8 versions/code, does this give you any clue as to why we're seeing this crash?

### om...@chromium.org (2019-10-04)

[Empty comment from Monorail migration]

### ml...@chromium.org (2019-10-04)

That V8 roll has only two changes and the likely one is 
  heap: Add GC trigger when overshooting global limit

This CL changes GC timing. That's not a functional change for most parts. It merely triggers GC immediately if we report to V8 and overshot the limit by a large margin.

We've discovered today that we were doing GC's in a GCForbidden scope in https://crbug.com/chromium/993415. 

We could try next week to patch in and see if it fixes it
  https://chromium-review.googlesource.com/c/chromium/src/+/1841336


### [Deleted User] (2019-10-04)

On https://crbug.com/chromium/993415#c39, I'm guessing you meant to point to https://crbug.com/1005723

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-10-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/45d6949ff04ba7591d93c07f34ed7c62ec79bfcb

commit 45d6949ff04ba7591d93c07f34ed7c62ec79bfcb
Author: Omer Katz <omerkatz@chromium.org>
Date: Wed Oct 09 12:42:20 2019

Fix Null dereference in Node.cc

The Node class uses an ephemeron map to record EvenTargetData.
Each node holds a flag stating whether or not it has an entry in
the map. The map itself is only allocated when it is first
accessed and that setting the flag is always accompanied by
adding a corresponding entry to the map.
During tracing, if the flag is set, the map emtry is also traced.

This crash was due to the order of setting the flag and allocating
the map.
Existing implementation first set the flag, then allocated the map
and added an entry to it. However, since the map is GCed, allocating
it can trigger a GC (before performing the actual allocation). If
that happens, while tracing the node we will see that the flag set
try to access the map which was not yet allocated (resuling in the
Null dereference).

This CL fixes the issue by only setting the flag after adding an entry
to the map.

The following two WIP changes are also relevant to this issue:
1) Do not trace the entry when tracing the node. The entries are held in
a persistent map which is traced as a root so tracing the entries when
tracing the node is not required (this change is still WIP as it affects
DevTools heap snapshot).
2) Prohibiting Allocation during atomic phase. This crash manifested
because the map was allocated during the atomic phase. Prohibiting
allocations wouldn't directly solve the issue but, if similar issues
arise in the future, it would make it much easier to debug and resolve
them.

Bug: 993415
Change-Id: I878ee8639ea3ddbc1834ece9a9cae96a27349fea
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1849672
Reviewed-by: Michael Lippautz <mlippautz@chromium.org>
Reviewed-by: Kentaro Hara <haraken@chromium.org>
Commit-Queue: Omer Katz <omerkatz@chromium.org>
Cr-Commit-Position: refs/heads/master@{#704155}

[modify] https://crrev.com/45d6949ff04ba7591d93c07f34ed7c62ec79bfcb/third_party/blink/renderer/core/dom/node.cc


### om...@chromium.org (2019-10-09)

[Empty comment from Monorail migration]

### om...@chromium.org (2019-10-09)

Requesting merge to M78 because this is was a high-severity security bug and the fix is trivial

### sh...@chromium.org (2019-10-09)

This bug requires manual review: We are only 12 days from stable.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://goto.google.com/chrome-release-branch-merge-guidelines
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: govind@(Android), kariahda@(iOS), geohsu@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### om...@chromium.org (2019-10-09)

1. yes
2. https://chromium-review.googlesource.com/c/chromium/src/+/1849672
3. We should merge back after checking one Canary.
4. Long-standing memory corruption
5. No
6. n/a

### sh...@chromium.org (2019-10-09)

[Empty comment from Monorail migration]

### sr...@google.com (2019-10-09)

merge approved for M78, branch:3904 ( pls merge the change to the branch post verification on canary tomorrow)

### sr...@google.com (2019-10-10)

Please help complete the merge to M78 branch by End of day Friday Oct 11, 2019, PST time zone.  Stable RC build will be triggered early next week

### om...@chromium.org (2019-10-10)

I believe it was merged already (https://chromium-review.googlesource.com/c/chromium/src/+/1853364)

### ml...@chromium.org (2019-10-10)

Not sure why the bot didn't pick it up. Manually setting labels.

### ad...@chromium.org (2019-10-10)

[Empty comment from Monorail migration]

### ad...@google.com (2019-10-17)

Assuming this affects all the normal platforms so it gets onto the right release TPM lists.

### na...@google.com (2019-10-18)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### pa...@chromium.org (2019-10-18)

Congrats! The Panel decided to reward $2,000 for this report + a $1,000 fuzzing bonus! 

### na...@google.com (2019-10-18)

[Empty comment from Monorail migration]

### ad...@google.com (2019-10-18)

[Empty comment from Monorail migration]

### sh...@chromium.org (2020-01-15)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### va...@chromium.org (2021-09-16)

[Empty comment from Monorail migration]

[Monorail components: -Blink>MemoryAllocator>GarbageCollection Blink>GarbageCollection]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/993415?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>DOM, Blink>GarbageCollection, Blink>JavaScript>GarbageCollection]
[Monorail mergedwith: crbug.com/chromium/1012902]
[Monorail components added to Component Tags custom field.]

### ti...@chromium.org (2024-06-27)

Adding `ClusterFuzz-Ignore` hotlist to all `ClusterFuzz-Wrong` issues per crbug.com/40285975.

### ti...@chromium.org (2024-06-27)

Adding `ClusterFuzz-Ignore` hotlist to all `ClusterFuzz-Wrong` issues per crbug.com/40285975.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095978)*
