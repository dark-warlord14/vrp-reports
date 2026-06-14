# Heap-use-after-free in blink::DeferredTaskHandler::handleDirtyAudioNodeOutputs

| Field | Value |
|-------|-------|
| **Issue ID** | [40084274](https://issues.chromium.org/issues/40084274) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebAudio |
| **Platforms** | Linux |
| **Reporter** | at...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2016-05-10 |
| **Bounty** | $3,500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5175218980519936

Fuzzer: attekett_webaudio_fuzzer
Job Type: linux_asan_chrome_chromeos
Platform Id: linux

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x6020001aa8b8
Crash State:
  blink::DeferredTaskHandler::handleDirtyAudioNodeOutputs
  blink::DeferredTaskHandler::handleDeferredTasks
  blink::AbstractAudioContext::handlePreRenderTasks
  
Recommended Security Severity: High

Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_chromeos&range=391820:391867

Unminimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv95hZ_K_ZPZvxdu9-Eh0dmP_zllTNZPedVF969DKfXyd4U4RNa4AMabXP2u4fFl3uzv4yL_grkbc7COjlv55DxZOkIwlW0PKN4eFYleQ5FqvHWYqi_GwwI3vj09Udt3R8SWt3ET3MOH77HZjfVWLKe3UcOwAY26jNOzxrzqGpbhqwIxt4ug


Filer: mmoroz

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

## Timeline

### mm...@chromium.org (2016-05-10)

[Empty comment from Monorail migration]

### tk...@chromium.org (2016-05-10)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-05-10)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-05-10)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-05-10)

This issue is a security regression. If you are not able to fix this quickly, please revert the change that introduced it.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2016-05-10)

[Empty comment from Monorail migration]

### mb...@chromium.org (2016-05-10)

[Empty comment from Monorail migration]

[Monorail components: Blink>WebAudio]

### bu...@chromium.org (2016-05-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/ac763683bafd8fe61ef1fe3285152b37d2bdab24

commit ac763683bafd8fe61ef1fe3285152b37d2bdab24
Author: sigbjornf <sigbjornf@opera.com>
Date: Tue May 10 21:14:00 2016

Prevent audio thread access to finished, non-active AudioNodes.

Follow up r392110 and have the audio thread skip over m_activeSourceNodes
nodes it has already deemed to be finished & removable by the main thread.
Accessing these cannot be safely done.

R=
BUG=610643

Review-Url: https://codereview.chromium.org/1958333006
Cr-Commit-Position: refs/heads/master@{#392720}

[modify] https://crrev.com/ac763683bafd8fe61ef1fe3285152b37d2bdab24/third_party/WebKit/Source/modules/webaudio/AbstractAudioContext.cpp
[modify] https://crrev.com/ac763683bafd8fe61ef1fe3285152b37d2bdab24/third_party/WebKit/Source/modules/webaudio/AbstractAudioContext.h


### [Deleted User] (2016-05-10)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-05-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-05-11)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-05-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/7b953ca0869bb4f2910b0f834b0ce7ad89166445

commit 7b953ca0869bb4f2910b0f834b0ce7ad89166445
Author: sigbjornf <sigbjornf@opera.com>
Date: Tue May 24 18:27:25 2016

Gracefully handle dirtying of audio nodes while processing current set.

When processing the set of dirty output nodes, nodes further down the
chain may be marked as dirty as a result. Take that into account
when iterating over the current set.

R=hoch
BUG=610643, 613902

Review-Url: https://codereview.chromium.org/2006883002
Cr-Commit-Position: refs/heads/master@{#395643}

[modify] https://crrev.com/7b953ca0869bb4f2910b0f834b0ce7ad89166445/third_party/WebKit/Source/modules/webaudio/DeferredTaskHandler.cpp


### [Deleted User] (2016-05-24)

Hopefully #12 takes care of it, let's wait & see.

### bu...@chromium.org (2016-06-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/d0b96fee6dfd3887573769b147952633720cc36c

commit d0b96fee6dfd3887573769b147952633720cc36c
Author: Alex Mineer <amineer@chromium.org>
Date: Wed Jun 29 15:43:58 2016

Gracefully handle dirtying of audio nodes while processing current set.

When processing the set of dirty output nodes, nodes further down the
chain may be marked as dirty as a result. Take that into account
when iterating over the current set.

R=hoch
BUG=610643, 613902

Review-Url: https://codereview.chromium.org/2006883002
Cr-Commit-Position: refs/heads/master@{#395643}
(cherry picked from commit 7b953ca0869bb4f2910b0f834b0ce7ad89166445)

Drop unique audio thread ID requirement.

r391848 introduced the requirement that, once set, the audio thread ID
could not be changed. This is proving too burdensome a constraint to
keep, in case audio device threads do end up being stopped and new
ones created.

While r395182 took care of some cases where audio threads end up
stopping, carefully resetting the recordeed audio thread ID, other
cases remain (see associated bug.) While those could be similarly
handled, precisely tracking the current audio thread ID is proving
to not be worth the overhead. Hence, retire the constraint and let
the audio thread processing a render quantum set its thread ID as
part of executing, irrespective of what audio thread executed
the previous quantum.

This effectively reverts r395182.

R=
BUG=613902

(cherry picked from commit 94a98a7b9932aafbb3baeabfec458fcdeea16707)

Review-Url: https://codereview.chromium.org/2008903002
Cr-Original-Commit-Position: refs/heads/master@{#395682}
Cr-Commit-Position: refs/branch-heads/2743@{#520}
Cr-Branched-From: 2b3ae3b8090361f8af5a611712fc1a5ab2de53cb-refs/heads/master@{#394939}

[modify] https://crrev.com/d0b96fee6dfd3887573769b147952633720cc36c/third_party/WebKit/Source/modules/webaudio/DeferredTaskHandler.cpp


### aw...@chromium.org (2016-07-20)

Nice - $3,500 for this one.

### aw...@chromium.org (2016-08-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-08-17)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-10)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-10)

This issue was migrated from crbug.com/chromium/610643?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/613902]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084274)*
