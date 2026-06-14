# Security: v8 compactor may operate on undefined slots

| Field | Value |
|-------|-------|
| **Issue ID** | [40092092](https://issues.chromium.org/issues/40092092) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>GarbageCollection |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ma...@gmail.com |
| **Assignee** | ul...@chromium.org |
| **Created** | 2018-08-02 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

While in the following specified conditions, the compactor will operate on a undefined slot:

1. Incremental marking is in the compacting stage.
2. the victim object is a fast object, usually created by object literal or "new Object()" expression.
3. the old-to-old remember set of the page containing the victim records a slot inside the victim. When crashes, this slot may reset an object in the new space.
4. The victim object then MigrateFastToSlow, shrinking itself to 3 \* kPointerSize bytes.But the filler object to fill that space left out is created without cleaning the content of its space.
5. The space left out at 4 is not allocated out.

Because 4 does not clean the content, when the compactor tries to update pointers, it will access the undefined content.

**VERSION**  

V8 Version: 6.3.298.0  

Operating System: Various Android version.

**REPRODUCTION CASE**  

I can't reproduce it simply.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: v8  

Crash State: see the attached crash log.

The log file UpdateUntypedPointer.txt records the whole procedure I debug using gdb.

The $13 is the page contains the problematic slot. And the page's invalidated\_slots\_ set contains the invalidated\_object which has been shrinked when MigrateFastToSlow. The victim (invalidated) object original has size 136, but now 12.

To address my point more clear, the patch that confirmed fixing is also attached.

## Attachments

- deleted (application/octet-stream, 0 B)
- [UpdateUntypePointer.txt](attachments/UpdateUntypePointer.txt) (text/plain, 10.8 KB)
- [patch_base_on_ca41e2de07e62e22d4d6b77003d9b87926a9112e](attachments/patch_base_on_ca41e2de07e62e22d4d6b77003d9b87926a9112e) (text/plain, 2.7 KB)

## Timeline

### mm...@chromium.org (2018-08-02)

Thanks for your report.

Adding Blink>JavaScript label to put this into V8 Sheriff's queue.

[Monorail components: Blink>JavaScript]

### ha...@chromium.org (2018-08-02)

[Empty comment from Monorail migration]

### ml...@chromium.org (2018-08-03)

Currently looking into this. Without too much digging: MigrateFastToSlow [1] is supposed to clear the recorded slot with ClearRecordedSlots::kYes in the area which should prevent compaction from finding it.

Checking now whether we have other paths that maybe iterate the page.

[1] https://cs.chromium.org/chromium/src/v8/src/objects.cc?q=MigrateFastToSlow&sq=package:chromium&g=0&l=4393

### ml...@chromium.org (2018-08-03)

[Empty comment from Monorail migration]

[Monorail components: -Blink>JavaScript Blink>JavaScript>GC]

### ml...@chromium.org (2018-08-03)

V8 version 6.3.298 already contains the code for clearing out the slots.

This should have been fixed from 6.2 on [1].

Searching how this slot can survive.

[1] https://chromium.googlesource.com/v8/v8.git/+/1e182fd4463621877f080f2d8f79964b6679b5e6

### ml...@chromium.org (2018-08-03)

Since this has been caught in gdb. Is there any chance for a repro that we can run locally?

### ml...@chromium.org (2018-08-03)

The attached path also suggests that this would be a problem with external strings. However, their slot clearing logic is right on the next line and only executed in the case we know that the string did contain data pointers.

### ma...@gmail.com (2018-08-03)

To ensure this problem is fix I add the cleaning code to every present of NotifyObjectLayoutChange. Maybe add This to the String object is unnecessary. Also please note 6.2 only try to clean the store buffer, not the content of the object. That is what ClearRecordedSlot::kYes means.

### ma...@gmail.com (2018-08-03)

The procedure to repro is very complicated. The fix is release to UCBrowser and proven.

### ma...@gmail.com (2018-08-03)

As the fix suggested,= ClearFreedMemoryMode::kClearFreedMemory is needed to clean up the content.

### ml...@chromium.org (2018-08-04)

We would require a repro to investigate this.

ClearRecordedSlot::kYes means clearing the remembered set. Only slots that are part of the remembered set are processed for compaction. There's no need to clear the actual object's contents.

### ma...@gmail.com (2018-08-05)

Okay. I will try to wrtie a js to reproduce this, but certainly needs to add some runtime function to help.
"ClearRecordedSlot::kYes means clearing the remembered set." Yes, but it's implementation only clear the store buffer. If the incremental marking is started, then it also need to clear the old to old remember set.

### ul...@chromium.org (2018-08-06)

This is probably uncovering a bug in invalidated slots filtering.

I'll try to write a cctest with MigrateFastToSlow and see if I can reproduce this.

The expected behavior:
1) MigrateFastToSlow(obj) calls NotifyObjectLayoutChange(obj, 136)
2) NotifyObjectLayoutChange adds <obj, 136> into the invalidated_slots of obj's page.
3) The old-to-old pointer updater skips all slots in range [obj, obj + 136) because the InvalidatedSlotsFilter.IsValid(slot) returns false.

### ma...@gmail.com (2018-08-06)

[Comment Deleted]

### ul...@chromium.org (2018-08-06)

Michael and I found the bug in InvalidatedSlotsFilter::IsValid(). I'll upload a fix soon.

### ma...@gmail.com (2018-08-06)

What about my fix? Is That wrong?

### ul...@chromium.org (2018-08-06)

Your fix works. It can be improved by not clearing freed memory for the ClearRecordedSlots::kNo case.

I am concerned about performance overhead of clearing slots. I want to first try another fix that makes InvalidatedSlotsFilter work as expected.

After that, I'll try to land your fix with modifications and see if there are regressions in perf bots.



### ma...@gmail.com (2018-08-06)

another way to fix is to clear the old to old remember set if the increamental marking is started.

### ul...@chromium.org (2018-08-06)

The fix is here: https://chromium-review.googlesource.com/c/v8/v8/+/1163784

Simply clearing the old to old slots would not work because it would race with the concurrent marker inserting old to old slots.

### ma...@gmail.com (2018-08-06)

that's a better solution than mine, thanks for the sharing. I never have thought the invalidate slot algorithm had a problem, its comment on "return true” showed a strong signal "I am right".

### bu...@chromium.org (2018-08-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/719d23c032a5d92998505fb642a7afd361f3e3ea

commit 719d23c032a5d92998505fb642a7afd361f3e3ea
Author: Ulan Degenbaev <ulan@chromium.org>
Date: Tue Aug 07 18:19:58 2018

Fix invalidation of old-to-old slots after object trimming.

A recorded old-to-old slot may be overwritten with a pointer to a new
space object. If the object containing the slot is trimmed later on,
then the mark-compactor may crash on a stale pointer to new space.

This patch ensures that:
1) On trimming of an object we add it to the invalidated_slots sets.
2) The InvalidatedSlotsFilter::IsValid returns false for slots outside
   the invalidated object unless the page was already swept.

Array left-trimming is handled as a special case because object start
moves and cannot be added to the invalidated set. Instead, we clear
the freed memory so that the recorded slots contain Smi values.

Bug: chromium:870226,chromium:816426
Change-Id: Iffc05a58fcf52ece45fdb085b5d1fd4b3acb5d53
Reviewed-on: https://chromium-review.googlesource.com/1163784
Commit-Queue: Ulan Degenbaev <ulan@chromium.org>
Reviewed-by: Hannes Payer <hpayer@chromium.org>
Reviewed-by: Michael Lippautz <mlippautz@chromium.org>
Cr-Commit-Position: refs/heads/master@{#54953}
[modify] https://crrev.com/719d23c032a5d92998505fb642a7afd361f3e3ea/src/heap/heap.cc
[modify] https://crrev.com/719d23c032a5d92998505fb642a7afd361f3e3ea/src/heap/invalidated-slots-inl.h
[modify] https://crrev.com/719d23c032a5d92998505fb642a7afd361f3e3ea/src/heap/invalidated-slots.cc
[modify] https://crrev.com/719d23c032a5d92998505fb642a7afd361f3e3ea/src/heap/invalidated-slots.h
[modify] https://crrev.com/719d23c032a5d92998505fb642a7afd361f3e3ea/src/heap/mark-compact.cc
[modify] https://crrev.com/719d23c032a5d92998505fb642a7afd361f3e3ea/src/heap/spaces.cc
[modify] https://crrev.com/719d23c032a5d92998505fb642a7afd361f3e3ea/src/heap/spaces.h
[modify] https://crrev.com/719d23c032a5d92998505fb642a7afd361f3e3ea/test/cctest/heap/heap-tester.h
[modify] https://crrev.com/719d23c032a5d92998505fb642a7afd361f3e3ea/test/cctest/heap/test-invalidated-slots.cc


### bu...@chromium.org (2018-08-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/5b434929a34f846f0002857765a3f505e0a2d736

commit 5b434929a34f846f0002857765a3f505e0a2d736
Author: Ulan Degenbaev <ulan@chromium.org>
Date: Tue Aug 07 19:15:58 2018

Revert "Fix invalidation of old-to-old slots after object trimming."

This reverts commit 719d23c032a5d92998505fb642a7afd361f3e3ea.

Reason for revert: TSAN failures

Original change's description:
> Fix invalidation of old-to-old slots after object trimming.
> 
> A recorded old-to-old slot may be overwritten with a pointer to a new
> space object. If the object containing the slot is trimmed later on,
> then the mark-compactor may crash on a stale pointer to new space.
> 
> This patch ensures that:
> 1) On trimming of an object we add it to the invalidated_slots sets.
> 2) The InvalidatedSlotsFilter::IsValid returns false for slots outside
>    the invalidated object unless the page was already swept.
> 
> Array left-trimming is handled as a special case because object start
> moves and cannot be added to the invalidated set. Instead, we clear
> the freed memory so that the recorded slots contain Smi values.
> 
> Bug: chromium:870226,chromium:816426
> Change-Id: Iffc05a58fcf52ece45fdb085b5d1fd4b3acb5d53
> Reviewed-on: https://chromium-review.googlesource.com/1163784
> Commit-Queue: Ulan Degenbaev <ulan@chromium.org>
> Reviewed-by: Hannes Payer <hpayer@chromium.org>
> Reviewed-by: Michael Lippautz <mlippautz@chromium.org>
> Cr-Commit-Position: refs/heads/master@{#54953}

TBR=ulan@chromium.org,hpayer@chromium.org,mlippautz@chromium.org

Change-Id: I2e1ff83c2db7902488951a8f597d38133aeb3b04
No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Bug: chromium:870226, chromium:816426
Reviewed-on: https://chromium-review.googlesource.com/1165862
Reviewed-by: Ulan Degenbaev <ulan@chromium.org>
Commit-Queue: Ulan Degenbaev <ulan@chromium.org>
Cr-Commit-Position: refs/heads/master@{#54954}
[modify] https://crrev.com/5b434929a34f846f0002857765a3f505e0a2d736/src/heap/heap.cc
[modify] https://crrev.com/5b434929a34f846f0002857765a3f505e0a2d736/src/heap/invalidated-slots-inl.h
[modify] https://crrev.com/5b434929a34f846f0002857765a3f505e0a2d736/src/heap/invalidated-slots.cc
[modify] https://crrev.com/5b434929a34f846f0002857765a3f505e0a2d736/src/heap/invalidated-slots.h
[modify] https://crrev.com/5b434929a34f846f0002857765a3f505e0a2d736/src/heap/mark-compact.cc
[modify] https://crrev.com/5b434929a34f846f0002857765a3f505e0a2d736/src/heap/spaces.cc
[modify] https://crrev.com/5b434929a34f846f0002857765a3f505e0a2d736/src/heap/spaces.h
[modify] https://crrev.com/5b434929a34f846f0002857765a3f505e0a2d736/test/cctest/heap/heap-tester.h
[modify] https://crrev.com/5b434929a34f846f0002857765a3f505e0a2d736/test/cctest/heap/test-invalidated-slots.cc


### ma...@gmail.com (2018-08-08)

Strange. Why your solution can pass asan? Can you explan That to me? I can't find any flaws.

### bu...@chromium.org (2018-08-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/51e6ecb9dfae93894863a9e21f14258b6b7909f7

commit 51e6ecb9dfae93894863a9e21f14258b6b7909f7
Author: Ulan Degenbaev <ulan@chromium.org>
Date: Sat Aug 11 08:35:39 2018

Reland "Fix invalidation of old-to-old slots after object trimming."

This reverts commit 5b434929a34f846f0002857765a3f505e0a2d736.

Changes after the original CL:
- Right-trimming registers the array as an object with invalidated
  slots.
- Left-trimming moves the array start in the invalidated slots map.

Original change's description:
> Fix invalidation of old-to-old slots after object trimming.
>
> A recorded old-to-old slot may be overwritten with a pointer to a new
> space object. If the object containing the slot is trimmed later on,
> then the mark-compactor may crash on a stale pointer to new space.
>
> This patch ensures that:
> 1) On trimming of an object we add it to the invalidated_slots sets.
> 2) The InvalidatedSlotsFilter::IsValid returns false for slots outside
>    the invalidated object unless the page was already swept.
>
> Array left-trimming is handled as a special case because object start
> moves and cannot be added to the invalidated set. Instead, we clear
> the freed memory so that the recorded slots contain Smi values.
>
> Bug: chromium:870226,chromium:816426
> Change-Id: Iffc05a58fcf52ece45fdb085b5d1fd4b3acb5d53
> Reviewed-on: https://chromium-review.googlesource.com/1163784
> Commit-Queue: Ulan Degenbaev <ulan@chromium.org>
> Reviewed-by: Hannes Payer <hpayer@chromium.org>
> Reviewed-by: Michael Lippautz <mlippautz@chromium.org>
> Cr-Commit-Position: refs/heads/master@{#54953}

Change-Id: I1f1080f680196c581f62aef8d3a00a595f9bb9b0
Reviewed-on: https://chromium-review.googlesource.com/1165555
Commit-Queue: Ulan Degenbaev <ulan@chromium.org>
Reviewed-by: Michael Lippautz <mlippautz@chromium.org>
Reviewed-by: Hannes Payer <hpayer@chromium.org>
Cr-Commit-Position: refs/heads/master@{#55066}
[modify] https://crrev.com/51e6ecb9dfae93894863a9e21f14258b6b7909f7/src/heap/heap.cc
[modify] https://crrev.com/51e6ecb9dfae93894863a9e21f14258b6b7909f7/src/heap/incremental-marking.cc
[modify] https://crrev.com/51e6ecb9dfae93894863a9e21f14258b6b7909f7/src/heap/invalidated-slots-inl.h
[modify] https://crrev.com/51e6ecb9dfae93894863a9e21f14258b6b7909f7/src/heap/invalidated-slots.cc
[modify] https://crrev.com/51e6ecb9dfae93894863a9e21f14258b6b7909f7/src/heap/invalidated-slots.h
[modify] https://crrev.com/51e6ecb9dfae93894863a9e21f14258b6b7909f7/src/heap/mark-compact.cc
[modify] https://crrev.com/51e6ecb9dfae93894863a9e21f14258b6b7909f7/src/heap/spaces.cc
[modify] https://crrev.com/51e6ecb9dfae93894863a9e21f14258b6b7909f7/src/heap/spaces.h
[modify] https://crrev.com/51e6ecb9dfae93894863a9e21f14258b6b7909f7/test/cctest/heap/heap-tester.h
[modify] https://crrev.com/51e6ecb9dfae93894863a9e21f14258b6b7909f7/test/cctest/heap/test-invalidated-slots.cc


### ul...@chromium.org (2018-08-11)

> Strange. Why your solution can pass asan? Can you explan That to me? I can't find any flaws.
Sorry, I missed your comment. The reason the original CL fails was because of data race in clearing: memset writes value on byte granularity and that was racing with the concurrent marker reading the values.



### ma...@gmail.com (2018-08-11)

Oh, tsan should not let my patch pass. But it seems not a big deal. Just make concurrent marking conservative.

### ul...@chromium.org (2018-08-21)

[Empty comment from Monorail migration]

### ul...@chromium.org (2018-08-21)

Merge request of the fix to M69 was rejected in chromium:816426 because the fix is complex and risky.

### sh...@chromium.org (2018-08-21)

[Empty comment from Monorail migration]

### ts...@chromium.org (2018-08-30)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-09-05)

[Empty comment from Monorail migration]

### aw...@google.com (2018-09-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-09-06)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-09-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-09-11)

Hi manjian2006@! Thanks for the report! The VRP panel decided to award $3,000 - a member of our finance team will be in touch to arrange payment.

### aw...@chromium.org (2018-09-11)

[Empty comment from Monorail migration]

### ul...@chromium.org (2018-09-12)

I just saw that the security severity got bumped to high in commented #32.

I am requesting merge to M69 of the fix in https://crbug.com/chromium/870226#c24. Note that my first merge request was rejected in crbug.com/816426 due to being high risk.

By now the fix has a lot of Canary/Dev coverage and should be safe.



### sh...@chromium.org (2018-09-12)

This bug requires manual review: Request affecting a post-stable build
Please contact the milestone owner if you have questions.
Owners: amineer@(Android), kariahda@(iOS), cindyb@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ul...@chromium.org (2018-09-12)

[Empty comment from Monorail migration]

### go...@chromium.org (2018-09-12)

+awhalley@ (Security TPM) for M69 & M70 merge review.

### aw...@google.com (2018-09-12)

Setting next action date to Friday to review then, as that will give the change a chance to bake on Beta

### aw...@chromium.org (2018-09-13)

[Comment Deleted]

### aw...@chromium.org (2018-09-13)

Given the number of changes going into the next respin, let's merge to 69 on Tuesday to both get some more beta coverage and hit any subsequent respin.


### ul...@chromium.org (2018-09-14)

Thanks, awhalley@!

I did a dry-run merge to see if there are any conflicts. There were two conflicts (easy to resolve):
https://chromium-review.googlesource.com/c/v8/v8/+/1225706

I will do the actual merge on Tuesday if it gets approved.

### aw...@chromium.org (2018-09-14)

Thanks for the prep work! Have a great weekend ulan@!

### aw...@chromium.org (2018-09-17)

govind@ - good for 69

### go...@chromium.org (2018-09-17)

hablich@ for M69 merge review and approval.

### ha...@google.com (2018-09-18)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-09-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/b352ee2896699c00c8191f3b7ed1daa8cfa63459

commit b352ee2896699c00c8191f3b7ed1daa8cfa63459
Author: Ulan Degenbaev <ulan@chromium.org>
Date: Tue Sep 18 09:44:41 2018

Merged: Reland "Fix invalidation of old-to-old slots after object trimming."

Revision: 51e6ecb9dfae93894863a9e21f14258b6b7909f7

NOTRY=true
NOPRESUBMIT=true
NOTREECHECKS=true
R=mlippautz@chromium.org

Bug: chromium:870226
Change-Id: I71a9a3ed8370d6e05e33442e278ef2cd1fb1562f
Reviewed-on: https://chromium-review.googlesource.com/1230093
Reviewed-by: Michael Lippautz <mlippautz@chromium.org>
Cr-Commit-Position: refs/branch-heads/6.9@{#49}
Cr-Branched-From: d7b61abe7b48928aed739f02bf7695732d359e7e-refs/heads/6.9.427@{#1}
Cr-Branched-From: b7e108d6016bf6b7de3a34e6d61cb522f5193460-refs/heads/master@{#54504}
[modify] https://crrev.com/b352ee2896699c00c8191f3b7ed1daa8cfa63459/src/heap/heap.cc
[modify] https://crrev.com/b352ee2896699c00c8191f3b7ed1daa8cfa63459/src/heap/incremental-marking.cc
[modify] https://crrev.com/b352ee2896699c00c8191f3b7ed1daa8cfa63459/src/heap/invalidated-slots-inl.h
[modify] https://crrev.com/b352ee2896699c00c8191f3b7ed1daa8cfa63459/src/heap/invalidated-slots.cc
[modify] https://crrev.com/b352ee2896699c00c8191f3b7ed1daa8cfa63459/src/heap/invalidated-slots.h
[modify] https://crrev.com/b352ee2896699c00c8191f3b7ed1daa8cfa63459/src/heap/mark-compact.cc
[modify] https://crrev.com/b352ee2896699c00c8191f3b7ed1daa8cfa63459/src/heap/spaces.cc
[modify] https://crrev.com/b352ee2896699c00c8191f3b7ed1daa8cfa63459/src/heap/spaces.h
[modify] https://crrev.com/b352ee2896699c00c8191f3b7ed1daa8cfa63459/test/cctest/heap/heap-tester.h
[modify] https://crrev.com/b352ee2896699c00c8191f3b7ed1daa8cfa63459/test/cctest/heap/test-invalidated-slots.cc


### go...@chromium.org (2018-09-18)

Seems like this is merged to M69 at #50. So removing "Merge-Approved-69" label.

This doesn't need merge to M70, correct?

### ha...@chromium.org (2018-09-19)

51e6ecb9dfae93894863a9e21f14258b6b7909f7 is already on 70.

### ma...@gmail.com (2018-09-21)

I have read the patch, and have a question. What about the situation that the invalidated gap being reallocated to a object whose fields contain integral constant? Like a SharedFunctionInfo object, its length field is typed uint16_t instead of smi. The slots like these should be filter out.

### ul...@chromium.org (2018-09-21)

manjian2006@, do you mean what happens if SharedFunctionInfo is evacuated into a new page and happens to overlap with an existing invalidate slots range?

In that case, the new page must have been swept. The sweeper removes all entries from old-to-old remembered set in the free space. So there will be no recorded slot corresponding to the length field of the SharedFunctionInfo and invalidated slots range will not queried for that slot address.

### ma...@gmail.com (2018-09-21)

Okay. I forgot the sweeper will remove the entries of old to old remembered set. Thank you.

### ma...@gmail.com (2018-09-21)

I still have another question. Dependency on a probable racing variable, the concurrent sweeping state, is it reliable? Say the moment chunk->SweepingDone() reports false, the next nanosecond it may report true. That's the way background parallel sweeper works as I understand.

### aw...@google.com (2018-10-15)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-10-16)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-11-12)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-11-27)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2018-11-27)

This issue was migrated from crbug.com/chromium/870226?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092092)*
