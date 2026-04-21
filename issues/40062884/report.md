# Security: Type confusion in v8 value serializer

| Field | Value |
|-------|-------|
| **Issue ID** | [40062884](https://issues.chromium.org/issues/40062884) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Runtime |
| **Platforms** | Linux, Windows |
| **Reporter** | m-...@github.com |
| **Assignee** | ma...@chromium.org |
| **Created** | 2023-02-02 |
| **Bounty** | $10,000.00 |

## Description

Vulnerability Details

When deserializing Javascript objects, the function `ReadJSObjectProperties`[1] will try to create a map using existing transitions:

```
Maybe<uint32_t> ValueDeserializer::ReadJSObjectProperties(  
    Handle<JSObject> object, SerializationTag end_tag,  
    bool can_use_transitions) {  
  ...  
  // Fast path (following map transitions).  
  if (can_use_transitions) {  
    ...  
    while (transitioning) {  
      ...  
      } else {  
        ...  
        if (key->IsString(isolate_)) {  
          key =  
              isolate_->factory()->InternalizeString(Handle<String>::cast(key));  
          // Don't reuse |transitions| because it could be stale.  
          transitioning = TransitionsAccessor(isolate_, \*map)  
                              .FindTransitionToField(Handle<String>::cast(key))  
                              .ToHandle(&target);                                  //<------ 1.  
        } else {  
          transitioning = false;  
        }  
      }  
  
      // Read the value that corresponds to it.  
      Handle<Object> value;  
      if (!ReadObject().ToHandle(&value)) return Nothing<uint32_t>();             //<------- 2.  
  
      // If still transitioning and the value fits the field representation  
      // (though generalization may be required), store the property value so  
      // that we can copy them all at once. Otherwise, stop transitioning.  
      if (transitioning) {  
        // Deserializaton of |value| might have deprecated current |target|,  
        // ensure we are working with the up-to-date version.  
        target = Map::Update(isolate_, target);                                  //<-------- 3.  
        ...  
  
      CommitProperties(object, map, properties);                                 //<-------- 4.  
      num_properties = static_cast<uint32_t>(properties.size());  

```

At (1), a the transitiion tree is searched to find suitable transition as the new object map. Then at (2), the value of the property is read, which may involve new object creation. This, in particular, may deprecate the `target` map and change the structure of the transition tree. To take this potential change into account, the `target` map is updated in (3), as the comment suggests.

The problem is that, updating a deprecated map may result in it being normalized into a dictionary map, while the subsequence code in (4) assumes the map has fast properties. By crafting an object such that:

1. At (2), the target map becomes deprecated after the value of the property is serialized
2. At (3), the migration causes `target` to become a dictionary map

A type confusion between fast properties and dictionary properties will be created. This, for example, can be done as follows:

1. Create two objects with the following structure:

```
obj = {a : 1};  
obj.a1 = 2;  
obj.c = {};  

```

This object, when deserialized, creates the following transitions in the target context:

```
{a : SMI} -> {a: SMI, a1 : SMI} -> {a: SMI, a1: SMI, c: Tagged}  

```

Next create an array of objects as follows. The first element of the array is:

```
arr0 = {a : 1};  
arr0.a1 = 1.1;  

```

and the rest of the elements are of the following structures:

```
arr_i = {a : 1};  
arr_i.a1 = 1;  
arr_i['b' + i] = 2;  

```

Then create a message object as an array:

```
[obj0, obj1]   

```

where `obj1` is:

```
obj1 = {a : 1};  
obj1.a1 = 2;  
obj1.c = arr;  

```

and `arr` contains the elements `arr0,...,arr_i`.

When this object is deserialized, `obj0` will be deserialized first, which will create the transitions:

```
{a : SMI} -> {a: SMI, a1 : SMI} -> {a: SMI, a1: SMI, c: Tagged}  

```

in the target context. Then, when `obj1` is deserialized, all of its maps will be found via these transitions. So when the last field, `c` is deserialized in `obj1`, `transitioning`[2] will be set to true. After this, `ReadObject` is called to deserialize the value of `c`, which is the array `arr`. When the first element in `arr`, `arr0` is deserialized, the `target` map becomes deprecated due to the incompatible representation in `a1` (from SMI to double). This removes the transition to `c` from the transition tree. After this, the objects `arr_i` are deserialized, which will insert new transitions from `a1` to `bi` in the new map. By controlling the number of these new transitions, it is possible to create a situation such that, when the `target` map is updated and `ConstructNewMap`[3] is called, the `split_map`, which is the new map containing `a`, `a1` and all the transitions to the `bi`, cannot have anymore transition inserted. This then cause the updated map to become normalized and turned into a dictionary map:

```
MapUpdater::State MapUpdater::ConstructNewMap() {  
  ...  
  if (maybe_transition.is_null() &&  
      !TransitionsAccessor::CanHaveMoreTransitions(isolate_, split_map)) {  
    return Normalize("Normalize_CantHaveMoreTransitions");                 
  }  
  

```

Thank you very much for your help and please let me know if there is anything I can help.

Man Yue Mo of GitHub Security Lab

1. <https://source.chromium.org/chromium/chromium/src/+/ed7dcb0b9e64a3e72beff2bd0d358398f959e5d2:v8/src/objects/value-serializer.cc;drc=2a7fa9b6065bba9cbe273ddc4f5e5a4a51bb450d;l=2407>
2. <https://source.chromium.org/chromium/chromium/src/+/ed7dcb0b9e64a3e72beff2bd0d358398f959e5d2:v8/src/objects/value-serializer.cc;l=2455;drc=2a7fa9b6065bba9cbe273ddc4f5e5a4a51bb450d>
3. <https://source.chromium.org/chromium/chromium/src/+/ed7dcb0b9e64a3e72beff2bd0d358398f959e5d2:v8/src/objects/map-updater.cc;l=275>

Reproduction Case

To reproduce the issue, run the attached `test_ser.js` with `d8`:

```
./d8 test_ser.js  

```

The attached `test_ser.html` is also tested on the official build of Chrome version 109.0.5414.119. (latest release)

This should cause a crash.

**VERSION**  

Chrome version: d8 main branch commit de4e492 and Chrome 109.0.5414.119  

Operating System: Ubuntu 22.04

**CREDIT INFORMATION**  

Reporter credit: Man Yue Mo of GitHub Security Lab

## Attachments

- [test_ser.js](attachments/test_ser.js) (text/plain, 478 B)
- [test_ser.html](attachments/test_ser.html) (text/plain, 666 B)

## Timeline

### [Deleted User] (2023-02-02)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-02-03)

Detailed Report: https://clusterfuzz.com/testcase?key=6184247906992128

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: UNKNOWN WRITE
Crash Address: 0x7d8c00004088
Crash State:
  v8::internal::JSObject::WriteToField
  v8::internal::CommitProperties
  v8::internal::ValueDeserializer::ReadJSObjectProperties
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Crash Revision: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&revision=1100700

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6184247906992128

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### cl...@chromium.org (2023-02-03)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-02-03)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Blink>JavaScript>Runtime]

### cl...@chromium.org (2023-02-03)

Automatically assigning owner based on suspected regression changelist https://chromium.googlesource.com/v8/v8/+/633cc57f8d98260315f657f9ebafa1c171d96402 ([runtime] Update transitioning target when deserializing values).

If this is incorrect, please let us know why and apply the Test-Predator-Wrong-CLs label. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### fl...@google.com (2023-02-03)

Hey  m-y-mo@!  Sorry for the comment spam/noise; I took your testcase and ran it into Clusterfuzz, so it could automagically do the regression analysis and such.  (Thanks so much for the testcase + the clear writeup and explanation; this does indeed look like a real bug.)

Setting Security_Severity-High and FoundIn-108 accordingly.

ishell@, if you're not the right owner for this bug, please reassign it to whoever is.  Thanks!

### [Deleted User] (2023-02-03)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-04)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-02-08)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-17)

ishell: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@chromium.org (2023-02-17)

[Empty comment from Monorail migration]

### is...@chromium.org (2023-02-21)

[Empty comment from Monorail migration]

### ma...@chromium.org (2023-02-21)

OP: thanks for the bug report and a very detailed analysis! I also really appreciate the d8-only repro which allowed me to jumpstart debugging this :)

### gi...@appspot.gserviceaccount.com (2023-02-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/b0db6637936a88807b5512a4de68145d0a9d6f02

commit b0db6637936a88807b5512a4de68145d0a9d6f02
Author: Marja Hölttä <marja@chromium.org>
Date: Tue Feb 21 12:38:34 2023

[valueserializer] Fix map transition chain following w/ dictionary maps

Map::Update might return a dictionary map, and the calling code didn't
take it into account.

Bug: chromium:1412487
Change-Id: I80cfc92e9a60c6118218a07cf9b1f7ad1080db91
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4274626
Commit-Queue: Marja Hölttä <marja@chromium.org>
Reviewed-by: Igor Sheludko <ishell@chromium.org>
Cr-Commit-Position: refs/heads/main@{#85954}

[modify] https://crrev.com/b0db6637936a88807b5512a4de68145d0a9d6f02/src/objects/value-serializer.cc


### ma...@chromium.org (2023-02-21)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-21)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-21)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-21)

This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M110. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M111. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-02-22)

This high+ V8 security issue with stable impact requires a lightweight post mortem. Please take some time to answer questions asked in this form [1] to help us improve V8 security. [1] https://docs.google.com/forms/d/e/1FAIpQLSdSMCiEpIFLLFkMbgtulK1sf1B-idQmkFaA4XP2Rz5mN1cqWg/viewform?usp=pp_url&entry.307501673=1412487&entry.364066060=External&entry.958145677=Linux&entry.958145677=Windows&entry.763880440=Extended&entry.1678852700=High&entry.763402679=Blink>JavaScript>Runtime&entry.975983575=marja@chromium.org Please ensure to copy the full link, as otherwise some issue meta data might not be populated automatically. 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-02-22)

Merge review required: M111 is already shipping to beta.

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
Owners: harrysouders (Android), harrysouders (iOS), dgagnon (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-02-22)

Merge review required: M110 is already shipping to stable.

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
Owners: govind (Android), harrysouders (iOS), ceb (ChromeOS), danielyip (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ma...@chromium.org (2023-02-22)

Questionnaire 1:

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)

https://chromium-review.googlesource.com/c/v8/v8/+/4274626

2. Has this fix been tested on Canary?

Yes, Canary 112.0.5611.0

3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?

Low stability risk. We haven't heard of any stability regressions.

4. Does this fix pose any known compatibility risks?

No

5. Does it require manual verification by the test team? If so, please describe required testing.

No

-----------------------


1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines

Security bug fix

2. What changes specifically would you like to merge? Please link to Gerrit.

https://chromium-review.googlesource.com/c/v8/v8/+/4274626

3. Have the changes been released and tested on canary?

Yes, Canary 112.0.5611.0

4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?

No

5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents

No; but this is not a ChromeOS specific fix.

6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

No

### cl...@chromium.org (2023-02-22)

ClusterFuzz testcase 6184247906992128 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1107915:1107920

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### ma...@chromium.org (2023-02-23)

The regression test was omitted from the fix, and will be added when the bug goes public. Here's what will be added:

const arr = [];
const obj0 = {a : 1};
obj0.a1 = 2;
obj0.c = {};

const obj = {a : 1};
obj.a1 = 2;
obj.c = arr;

const f1 = {a : 1};
f1.a1 = 1.1;
arr.push(f1);

for (i = 0; i < 1600; i++) {
  const tmp = {a : 1};
  tmp.a1 = 1;
  tmp['b' + i] = 2;
  arr.push(tmp);
}

function workerCode() {
  onmessage = function(data) {
    postMessage('done');
  }
}

worker = new Worker(workerCode, {type: 'function', arguments: []});
worker.postMessage([obj0, obj]);

assertEquals('done', worker.getMessage());



### va...@chromium.org (2023-02-24)

@desktop owners: Can you please review the merge request? Thanks!

### am...@chromium.org (2023-02-24)

since this is a security issue, this is actually in our security merge review queue and is not on the desktop team to review; since the fix landed on Tuesday, I was giving it appropriate bake time since this would go into Stable RC for M111

### am...@chromium.org (2023-02-24)

canary performance looks okay, merge approved for M111 and M110
please merge this fix to 11.1-lkgr and 11.0-lkgr by end of day Monday, 27 February so this fix can be included in M111/Stable cut and M110/Extended 
Thank you! 

### gi...@appspot.gserviceaccount.com (2023-02-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/aeceeb2187a68f273b54159e4181ab7005923495

commit aeceeb2187a68f273b54159e4181ab7005923495
Author: Marja Hölttä <marja@chromium.org>
Date: Tue Feb 21 12:38:34 2023

Merged [valueserializer] Fix map transition chain following w/ dictionary maps

Map::Update might return a dictionary map, and the calling code didn't
take it into account.

Bug: chromium:1412487
(cherry picked from commit b0db6637936a88807b5512a4de68145d0a9d6f02)

Change-Id: Ib5e55aa60719e4ac2f14d993a3fc3e908cd43d2e
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4290145
Reviewed-by: Marja Hölttä <marja@chromium.org>
Reviewed-by: Lutz Vahl <vahl@chromium.org>
Commit-Queue: Lutz Vahl <vahl@chromium.org>
Cr-Commit-Position: refs/branch-heads/11.0@{#35}
Cr-Branched-From: 06097c6f0c5af54fd5d6965d37027efb72decd4f-refs/heads/11.0.226@{#1}
Cr-Branched-From: 6bf3344f5d9940de1ab253f1817dcb99c641c9d3-refs/heads/main@{#84857}

[modify] https://crrev.com/aeceeb2187a68f273b54159e4181ab7005923495/src/objects/value-serializer.cc


### gi...@appspot.gserviceaccount.com (2023-02-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/28a1dab5713bd9c5f2cf0fc1dc32fc8fcb5ada21

commit 28a1dab5713bd9c5f2cf0fc1dc32fc8fcb5ada21
Author: Marja Hölttä <marja@chromium.org>
Date: Tue Feb 21 12:38:34 2023

Merged: [valueserializer] Fix map transition chain following w/ dictionary maps

Map::Update might return a dictionary map, and the calling code didn't
take it into account.

Bug: chromium:1412487
(cherry picked from commit b0db6637936a88807b5512a4de68145d0a9d6f02)

Change-Id: I01995340856b5e21d1cda51915e8a2543428cfc4
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4290144
Reviewed-by: Lutz Vahl <vahl@chromium.org>
Commit-Queue: Lutz Vahl <vahl@chromium.org>
Reviewed-by: Marja Hölttä <marja@chromium.org>
Cr-Commit-Position: refs/branch-heads/11.1@{#18}
Cr-Branched-From: c77793a2ee5bfa7c5226dd8f622bf331b97a5a25-refs/heads/11.1.277@{#1}
Cr-Branched-From: 95b79bf04ba3f9de87f7bad77bc2d7552e5dc4d7-refs/heads/main@{#85479}

[modify] https://crrev.com/28a1dab5713bd9c5f2cf0fc1dc32fc8fcb5ada21/src/objects/value-serializer.cc


### gi...@appspot.gserviceaccount.com (2023-02-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/788e4f28e4e08c08d03e63f07ff5caec1bdf98c0

commit 788e4f28e4e08c08d03e63f07ff5caec1bdf98c0
Author: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
Date: Mon Feb 27 13:11:36 2023

Roll v8 11.1 from 3e5cb8693c29 to 9f67568f6710 (4 revisions)

https://chromium.googlesource.com/v8/v8.git/+log/3e5cb8693c29..9f67568f6710

2023-02-27 v8-ci-autoroll-builder@chops-service-accounts.iam.gserviceaccount.com Version 11.1.277.11
2023-02-27 mliedtke@chromium.org Merged: [wasm-gc] Liftoff: Fix 'br_on_cast_fail null <x> none' stack handling
2023-02-27 v8-ci-autoroll-builder@chops-service-accounts.iam.gserviceaccount.com Version 11.1.277.10
2023-02-27 marja@chromium.org Merged: [valueserializer] Fix map transition chain following w/ dictionary maps

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/v8-chromium-release-1
Please CC liviurau@google.com,v8-waterfall-sheriff@grotations.appspotmail.com,vahl@google.com on the revert to ensure that a human
is aware of the problem.

To file a bug in v8 11.1: https://bugs.chromium.org/p/v8/issues/entry
To file a bug in Chromium m111: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Bug: chromium:1412487
Tbr: v8-waterfall-sheriff@grotations.appspotmail.com
Change-Id: I32f460cf01340054493619db802408dd365d0331
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4293778
Commit-Queue: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/5563@{#853}
Cr-Branched-From: 3ac59a6729cdb287a7ee629a0004c907ec1b06dc-refs/heads/main@{#1097615}

[modify] https://crrev.com/788e4f28e4e08c08d03e63f07ff5caec1bdf98c0/DEPS


### gi...@appspot.gserviceaccount.com (2023-02-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/14c9e7a53a4e61a7deb03bb707ec2584c2982272

commit 14c9e7a53a4e61a7deb03bb707ec2584c2982272
Author: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
Date: Mon Feb 27 13:13:23 2023

Roll v8 11.0 from 299afaf4dec0 to e3829fc4daf7 (2 revisions)

https://chromium.googlesource.com/v8/v8.git/+log/299afaf4dec0..e3829fc4daf7

2023-02-27 v8-ci-autoroll-builder@chops-service-accounts.iam.gserviceaccount.com Version 11.0.226.18
2023-02-27 marja@chromium.org Merged [valueserializer] Fix map transition chain following w/ dictionary maps

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/v8-chromium-release-2
Please CC liviurau@google.com,v8-waterfall-sheriff@grotations.appspotmail.com,vahl@google.com on the revert to ensure that a human
is aware of the problem.

To file a bug in v8 11.0: https://bugs.chromium.org/p/v8/issues/entry
To file a bug in Chromium m110: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Bug: chromium:1412487
Tbr: v8-waterfall-sheriff@grotations.appspotmail.com
Change-Id: I168625b75d60310499ac976de37f242e2f1cf61d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4293501
Commit-Queue: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/5481@{#1294}
Cr-Branched-From: 130f3e4d850f4bc7387cfb8d08aa993d288a67a9-refs/heads/main@{#1084008}

[modify] https://crrev.com/14c9e7a53a4e61a7deb03bb707ec2584c2982272/DEPS


### am...@google.com (2023-03-02)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-03-02)

Congratulations, Man Yue Mo! The VRP Panel has decided to award you $10,000 for this report. Thank you for your high quality report and the efforts of discovering and reporting this issue to us -- great work! 

### am...@google.com (2023-03-03)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-03-06)

[Empty comment from Monorail migration]

### am...@google.com (2023-03-07)

[Empty comment from Monorail migration]

### pg...@google.com (2023-03-07)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-30)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2023-05-31)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/b8d6e262613c4bce6aef606242120d68b193d869

commit b8d6e262613c4bce6aef606242120d68b193d869
Author: Marja Hölttä <marja@chromium.org>
Date: Wed May 31 08:15:43 2023

[valueserializer] Add a regression test for a now-public bug

Bug: chromium:1412487
Change-Id: Ib2f78d23bedcf3517ee2ae3bcec3b7289bd72f5e
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4570890
Commit-Queue: Marja Hölttä <marja@chromium.org>
Reviewed-by: Igor Sheludko <ishell@chromium.org>
Cr-Commit-Position: refs/heads/main@{#87958}

[add] https://crrev.com/b8d6e262613c4bce6aef606242120d68b193d869/test/mjsunit/regress/regress-crbug-1412487.js


### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1412487?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062884)*
