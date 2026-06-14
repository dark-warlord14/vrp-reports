# Oilpan reintroduced inline meta-data

| Field | Value |
|-------|-------|
| **Issue ID** | [40084983](https://issues.chromium.org/issues/40084983) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>GarbageCollection |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | pa...@chromium.org |
| **Created** | 2016-08-01 |
| **Bounty** | $2,000.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2813.0 Safari/537.36

Steps to reproduce the problem:
The Oilpan GC heap has replaced PartitionAlloc as the backing store for Blink objects that inherit from Node. While this design maintains some the security properties of PartitionAlloc (e.g. these objects are separated from other objects such as strings, arrays etc) it reintroduced inline meta data in the form of a HeapObjectHeader.

The HeapObjectHeader class is defined in HeapPage.h and contains two member variables m_encoded and m_padding. The padding bits are only present in 64-bit builds. The m_encoded member has a number of bits that can be toggled to indicate the state of the chunk. These are defined on line ~146 of HeapPage.h in my checkout of the code. Some of these fields such as headerFreedBitMask and headerSizeMask indicate the state (free/used) and the size of the object.

This meta data appears to be stored inline with Blink Node objects. So while the Oilpan implementation makes exploitation of use-after-free harder it has reintroduced a prime overwrite target that may result in similar double-free or dangling pointers. A pointer to this header is typically retrieved using HeapObjectHeader::fromPayload function which just performs a simple subtraction of the size of the HeapObjectHeader from the start address of the chunk. Search through the code for calls to this function to get an idea of where this meta-data is used by the garbage collector.

Mitigating this could be done by storing the m_encoded value in a different segment of memory protected by guard pages the way PartitionAlloc does it. XORing m_encoded with a secret value likely won't work because some of these fields are a single bit. Placing a canary before m_encoded or using the padding bits and reversing their position could help prevent a linear overwrite. There are likely negative performance implications by doing this.

Note: I have not exploited this behavior. Its just something I noticed when reading through the code.

What is the expected behavior?
Maintain the security properties provided by PartitionAlloc

What went wrong?
Oilpan introduced inline meta data when it became the default allocator for Blink objects that inherit from Node

Did this work before? Yes PartitionAlloc

Chrome version: 54.0.2813.0  Channel: dev
OS Version: OS X 10.11.6
Flash Version: Shockwave Flash 22.0 r0

## Timeline

### ra...@chromium.org (2016-08-01)

Marking low severity as there is no PoC. 

haraken: could you please help triage this? Thanks.

[Monorail components: Infra>Client>Oilpan]

### ch...@gmail.com (2016-08-26)

Further inspection of the Oilpan GC heap shows a couple of things. If you can control the value of HeapObjectHeader::m_encoded via linear overwrite then one potential exploit technique may be to use the NormalPageArena::coalesce function which will use the untrusted size to adjust the startOfGap pointer. The resulting address will be passed to FreeList::addToFreeList.

I also noticed there are inline FreeListEntry structures with an m_next pointer which inherits from HeapObjectHeader. The FreeListEntry::unlink function looks easily abused if the m_next pointer can be controlled via linear overwrite as well.

There seems to be no basic hardening in the Oilpan GC heap.

### ha...@chromium.org (2016-08-26)

Thanks for reporting the issue!

> Mitigating this could be done by storing the m_encoded value in a different segment of memory protected by guard pages the way PartitionAlloc does it.

Yeah, this will mitigate the security concern but introduce some performance regression. So I want to understand how risky the current implementation is.

Concretely, what kind of exploit do you have in mind? It looks like that you're assuming a scenario where you've already got the beginning address of the Node object. However, when can you get the beginning address of the Node object in the first place?


### js...@chromium.org (2016-08-26)

Bumping the severity because this makes life far too easy for exploit writers. The solution here is that the allocator metadata either needs to be moved out-of-line or we need to reorder/guard it such that inconsistency will induce a crash before any damage can be done.

### js...@chromium.org (2016-08-26)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-08-28)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-08-28)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-09-09)

haraken: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@chromium.org (2016-09-09)

I'm not sure about the severity of this bug. Also, in practice I don't think we can fix the bug in short term anyway.


### ha...@chromium.org (2016-09-09)

Regarding #4, we tried to move the meta data to out-of-line before (for collecting all marking bits in one place and thus improving cache locality), but it significantly reduced runtime performance. The overhead to look up the header from an object body really matters.

> we need to reorder/guard it such that inconsistency will induce a crash before any damage can be done.

Would you elaborate a bit more?


### js...@chromium.org (2016-09-09)

If we can place a random canary around the metadata, and check it before we manipulate memory structures, then that might be sufficient protection. However, I was planning on waiting for palmer@ to get back and let him tackle this.

### sh...@chromium.org (2016-09-24)

haraken: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-13)

[Empty comment from Monorail migration]

### ch...@gmail.com (2016-10-18)

Its been roughly 75 days since I reported this. I realize this is more design flaw than it is an implementation flaw and thus will take longer to fix. However unprotected heap meta data provides a well understood mechanism for exploit developers. Is there a plan to harden oilpan against this?

### ha...@chromium.org (2016-10-19)

Per the comment in #11, assigning to palmer@.


### pa...@chromium.org (2016-10-24)

This isn't going to make it into M54, alas. I am officially back in action on 2 Nov 2016. Let's try for M56?

Also, does this bug really affect Chrome on iOS? Seems like it applies to every platform except iOS, give our dependence on the platform's WebKit there. Right?

### ra...@chromium.org (2016-11-28)

palmer: Friendly ping from security sheriff just checking you're still planning to work on this? 

### pa...@chromium.org (2016-11-28)

Yep, I'm hustlin' on it and related things.

### pa...@chromium.org (2016-12-15)

[Empty comment from Monorail migration]

### be...@chromium.org (2017-01-18)

Ping - please provide an update to your high priority bug. This bug is stale. Is it really P-1?

### do...@chromium.org (2017-01-31)

Hey palmer, just checking in on how this is going. Should the priority be reduced?

### pa...@chromium.org (2017-01-31)

I'm working on it, but performance is proving exciting.

### bu...@chromium.org (2017-02-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/40cd3c13c54f9aa73fc0b47e59a7d962037e2f94

commit 40cd3c13c54f9aa73fc0b47e59a7d962037e2f94
Author: palmer <palmer@chromium.org>
Date: Wed Feb 15 06:37:05 2017

Protect heap metadata in Oilpan.

Rather than checking a static 16-bit magic value to check a HeapObjectHeader's
integrity when DCHECK_IS_ON, use a random 32-bit canary value in all builds.
Place it before the HeapObjectHeader value, rather than after, so that linear
overwrites (e.g. from OOB writes starting from lower addresses) are more likely
to corrupt it.

This is not a complete fix for 633030; more work on other heap metadata is
coming next. This is the simplest possible start. In particular, in future work
we may xor the |m_encoded| field with the canary as well, to obfuscate its
meaning to attackers using an infoleak to learn about the Oilpan heap.

BUG=633030

Review-Url: https://codereview.chromium.org/2683823004
Cr-Commit-Position: refs/heads/master@{#450598}

[modify] https://crrev.com/40cd3c13c54f9aa73fc0b47e59a7d962037e2f94/third_party/WebKit/Source/platform/heap/HeapPage.h


### pa...@chromium.org (2017-02-16)

I'm kind of thinking of passing on xoring |m_encoded| — an attacker who can read it can probably read the preceding word, and hence could de-obfuscate the value.

That might be a somewhat tricky thing to achieve in what is supposed to be the infoleak stage of the exploit (i.e. relatively easy), but maybe it isn't really difficult enough, hence the security value of the obfuscation would not outweigh its cost. Chris R., any thoughts on that?

Doing the xor would have a small cost; I'd have to:

* de-obfuscate in getters
* de-obfuscate in setters
* re-obfuscate in setters

Obviously, xor is an extremely cheap machine instruction and the 'key' is the adjacent word, so these operations are just about as cheap as anything can be. And the xor instruction is small, but not 0 bytes. Just wanted to raise the issue.

### ch...@gmail.com (2017-02-20)

I don't see a big benefit in obfuscating the value of m_encoded by xoring it with the secret value. With the exception of the 14 size bits, m_encoded is likely only ever to be in a limited number of states. So leaking an obfuscated m_encoded value may reveal 18 bits of information about the secret canary value. Doesn't seem worth the cost.

If you have to pay a performance penalty somewhere a randomized free list seems like a stronger protection.

### dc...@chromium.org (2017-02-27)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-03-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/e3d585cce44455344c067ab7a5ebb359fae854f7

commit e3d585cce44455344c067ab7a5ebb359fae854f7
Author: palmer <palmer@chromium.org>
Date: Wed Mar 01 02:55:21 2017

Use the Oilpan heap canary only on 64-bit.

On 64-bit machines, the canary is free, space-wise. But on 32-bit, it doubles
the size of |HeapObjectHeader|, which has incurred a large run-time memory size
increase.

Turn off the canary for now, on 32-bit. Ultimately we may solve the original bug
(633030) by moving the metadata out of line instead of guarding it with a
canary.

BUG=692931,692624,633030

Review-Url: https://codereview.chromium.org/2723743003
Cr-Commit-Position: refs/heads/master@{#453802}

[modify] https://crrev.com/e3d585cce44455344c067ab7a5ebb359fae854f7/third_party/WebKit/Source/platform/heap/HeapPage.cpp
[modify] https://crrev.com/e3d585cce44455344c067ab7a5ebb359fae854f7/third_party/WebKit/Source/platform/heap/HeapPage.h


### bu...@chromium.org (2017-03-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/66e64785b1bfcaf2504e62f063b1c3ecf352605c

commit 66e64785b1bfcaf2504e62f063b1c3ecf352605c
Author: palmer <palmer@chromium.org>
Date: Wed Mar 01 23:08:07 2017

Better distribute the randomness of the Oilpan metadata canary.

Use a circular shift.

BUG=633030

Review-Url: https://codereview.chromium.org/2716383003
Cr-Commit-Position: refs/heads/master@{#454085}

[modify] https://crrev.com/66e64785b1bfcaf2504e62f063b1c3ecf352605c/third_party/WebKit/Source/platform/heap/HeapPage.h


### ch...@gmail.com (2017-03-02)

Any timeline for when this will land in a stable build? Any plans to randomize the freelist?

### pa...@chromium.org (2017-03-15)

Unfortunately, we are not yet in the happy place of enforcing canary checking in Release builds. That's pending https://codereview.chromium.org/2698673003 and then a trivial 1-line patch after that. Hopefully, Real Soon Now (TM).

### pa...@chromium.org (2017-03-29)

The bot doesn't seem to have added it to this CL, but, this landed: Call HeapObjectHeader::checkHeader solely for its side-effect (https://codereview.chromium.org/2698673003/).

### aw...@google.com (2017-03-31)

palmer@- are you expecting to make any more changes after #31, or can this be marked as fixed? Thanks!

### pa...@chromium.org (2017-03-31)

1 more change coming up.

### bu...@chromium.org (2017-03-31)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/a459a6e71008ba58aaec1a9a95ac20b5864d5e82

commit a459a6e71008ba58aaec1a9a95ac20b5864d5e82
Author: palmer <palmer@chromium.org>
Date: Fri Mar 31 20:53:08 2017

Make HeapObjectHeader::checkHeader private.

The function is properly private; callers should not have to 'know' when it's
necessary and when it isn't. It's the object's job to enforce its own internal
invariants.

BUG=633030

Review-Url: https://codereview.chromium.org/2786843002
Cr-Commit-Position: refs/heads/master@{#461220}

[modify] https://crrev.com/a459a6e71008ba58aaec1a9a95ac20b5864d5e82/third_party/WebKit/Source/bindings/core/v8/TraceWrapperMember.h
[modify] https://crrev.com/a459a6e71008ba58aaec1a9a95ac20b5864d5e82/third_party/WebKit/Source/platform/heap/GCInfo.cpp
[modify] https://crrev.com/a459a6e71008ba58aaec1a9a95ac20b5864d5e82/third_party/WebKit/Source/platform/heap/HeapAllocator.cpp
[modify] https://crrev.com/a459a6e71008ba58aaec1a9a95ac20b5864d5e82/third_party/WebKit/Source/platform/heap/HeapAllocator.h
[modify] https://crrev.com/a459a6e71008ba58aaec1a9a95ac20b5864d5e82/third_party/WebKit/Source/platform/heap/HeapPage.cpp
[modify] https://crrev.com/a459a6e71008ba58aaec1a9a95ac20b5864d5e82/third_party/WebKit/Source/platform/heap/HeapPage.h
[modify] https://crrev.com/a459a6e71008ba58aaec1a9a95ac20b5864d5e82/third_party/WebKit/Source/platform/heap/Member.h
[modify] https://crrev.com/a459a6e71008ba58aaec1a9a95ac20b5864d5e82/third_party/WebKit/Source/platform/heap/TraceTraits.h


### sh...@chromium.org (2017-04-20)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-04-24)

palmer@ - how 'bout now? :-)

### pa...@chromium.org (2017-04-26)

No, it's not fully fixed yet. However, I don't think we should delay considering rewarding for it, nor making it public. The further work will likely take a while. (I gotta spin a few other plates before getting back to performance on this. The next tactic I try will likely be moving the metadata out of line, which will be more complicated.)

### es...@chromium.org (2017-05-03)

Hello, palmer. It's security fix-it week and I got assigned this bug, so I am here to bother you -- sorry.

Should we close this bug and move it to the panel, and file follow-up bug(s) for the remaining work? Or would it make sense to just leave this bug open for the time being?

### pa...@chromium.org (2017-05-03)

Unfortunately, it needs to stay open. CHECKing on canary mismatch has too much performance impact, so I am going to try a new tack with out-of-line metadata. (That will have its own performance impact, both good and bad, and we'll no doubt have a lively debate once I have an implementation in hand.)

That said, this bug is older than our deadline, so I think we can remove the view restrictions? And +awhalley, can we consider it for the panel even though it's not fully Fixed yet? I don't think the reporter should have to wait on our internal architectural deliberations...

### aw...@google.com (2017-05-03)

If we've landed a fix that we feel is a good mitigation then I'm with putting it in front of the panel, even without a full fix. But if we don't feel that any of the changes landed so far have made much of a difference security wise we should wait.

### sh...@chromium.org (2017-06-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-07-26)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-09-06)

[Empty comment from Monorail migration]

### ra...@chromium.org (2017-09-20)

palmer: friendly ping :) Could you clarify how much of this issue is currently mitigated by CLs that have landed (as per #40)? 

### pa...@chromium.org (2017-09-20)

#44: In production, not mitigated at all. Solving this without performance regression is still an open problem, and I've been side-tracked by a 2-quarter long project that is finally finished. Here's hoping for Q4...

### pa...@chromium.org (2017-09-25)

[Empty comment from Monorail migration]

[Monorail components: -Infra>Client>Oilpan Blink>MemoryAllocator>GarbageCollection]

### sh...@chromium.org (2017-10-18)

[Empty comment from Monorail migration]

### mm...@chromium.org (2017-11-15)

We are in the middle of Q4, friendly ping from security sheriff, since the last activity here was 1 month ago.

### pa...@chromium.org (2017-11-16)

I'm currently chewing on this but a wild emergency has appeared. This is next on my agenda, though.

### pa...@chromium.org (2017-12-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-12-07)

[Empty comment from Monorail migration]

### pa...@chromium.org (2017-12-27)

[Empty comment from Monorail migration]

### pa...@chromium.org (2018-01-22)

I believe we should land https://chromium-review.googlesource.com/c/chromium/src/+/846356. If we later also move metadata out of line, that'd be great; but until then I think that CL is an affordable mechanism to thwart the most obvious attack.

### pa...@chromium.org (2018-01-22)

Re-assigning to mlippautz as discussed in email, for longer-term OOL work.

### sh...@chromium.org (2018-01-25)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-01-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/129fac28f2fc2e9003222a0be60997f299841a9a

commit 129fac28f2fc2e9003222a0be60997f299841a9a
Author: Chris Palmer <palmer@chromium.org>
Date: Fri Jan 26 23:13:26 2018

Enable the Oilpan metadata canary in production builds.

BUG=633030

Change-Id: Iaa27af5e6d3b4b55d11e044dc57e23dcf0682b39
Reviewed-on: https://chromium-review.googlesource.com/846356
Reviewed-by: Kentaro Hara <haraken@chromium.org>
Commit-Queue: Chris Palmer <palmer@chromium.org>
Cr-Commit-Position: refs/heads/master@{#532084}
[modify] https://crrev.com/129fac28f2fc2e9003222a0be60997f299841a9a/third_party/WebKit/Source/platform/heap/HeapPage.h


### pa...@chromium.org (2018-01-26)

Question (primarily for awhalley): Should we open a new bug (Security, Type=Feature) for out-of-line metadata work, and close this one as Fixed, so that it can become public and be considered for reward as usual? (Thanks Chris R!)

Or does it make more sense to keep the OOL metadata stuff on this bug? (If the latter, should we make this bug public and consider it for reward even while keeping it open?)

### aw...@google.com (2018-01-26)

The former!

### pa...@chromium.org (2018-01-26)

https://bugs.chromium.org/p/chromium/issues/detail?id=806407

### bu...@chromium.org (2018-01-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/f9a22f3e9d081a64e311116662fbdcab90cc4aac

commit f9a22f3e9d081a64e311116662fbdcab90cc4aac
Author: Hannes Payer <hpayer@chromium.org>
Date: Mon Jan 29 18:46:01 2018

Oilpan: Immediatelly promptly free objects.

This CL brings the following changes to promptly freeing and coalescing:
1) Promptly freed objects on already swept pages are immediately added to the free list.
2) For promptly freed objects on not already swept pages we only clear the mark bit.
3) The promptly_freed_size_ counter is explicitly set to 0 before sweeping because sweeping will take care of coalescing as well.
4) The dead bit is removed.
Note that coalescing before sweeping completed can not happen.

Future outlook: As a next step we will evaluate if we need coalescing and if we need it we have to make it jank friendly.

Bug: chromium:804279, chromium:633030
Change-Id: I35dfae80ae0e7ed6cfbc91877d97d0b5fc26498e
Reviewed-on: https://chromium-review.googlesource.com/873974
Commit-Queue: Hannes Payer <hpayer@chromium.org>
Reviewed-by: Kentaro Hara <haraken@chromium.org>
Reviewed-by: Michael Lippautz <mlippautz@chromium.org>
Cr-Commit-Position: refs/heads/master@{#532509}
[modify] https://crrev.com/f9a22f3e9d081a64e311116662fbdcab90cc4aac/third_party/WebKit/Source/platform/heap/HeapPage.cpp
[modify] https://crrev.com/f9a22f3e9d081a64e311116662fbdcab90cc4aac/third_party/WebKit/Source/platform/heap/HeapPage.h


### bu...@chromium.org (2018-01-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/e12ed52e5988fca99f50a5560a84beab39e51a39

commit e12ed52e5988fca99f50a5560a84beab39e51a39
Author: Samuel Huang <huangs@chromium.org>
Date: Mon Jan 29 19:14:13 2018

Revert "Oilpan: Immediatelly promptly free objects."

This reverts commit f9a22f3e9d081a64e311116662fbdcab90cc4aac.

Reason for revert: <INSERT REASONING HERE>

Original change's description:
> Oilpan: Immediatelly promptly free objects.
> 
> This CL brings the following changes to promptly freeing and coalescing:
> 1) Promptly freed objects on already swept pages are immediately added to the free list.
> 2) For promptly freed objects on not already swept pages we only clear the mark bit.
> 3) The promptly_freed_size_ counter is explicitly set to 0 before sweeping because sweeping will take care of coalescing as well.
> 4) The dead bit is removed.
> Note that coalescing before sweeping completed can not happen.
> 
> Future outlook: As a next step we will evaluate if we need coalescing and if we need it we have to make it jank friendly.
> 
> Bug: chromium:804279, chromium:633030
> Change-Id: I35dfae80ae0e7ed6cfbc91877d97d0b5fc26498e
> Reviewed-on: https://chromium-review.googlesource.com/873974
> Commit-Queue: Hannes Payer <hpayer@chromium.org>
> Reviewed-by: Kentaro Hara <haraken@chromium.org>
> Reviewed-by: Michael Lippautz <mlippautz@chromium.org>
> Cr-Commit-Position: refs/heads/master@{#532509}

TBR=haraken@chromium.org,hpayer@chromium.org,mlippautz@chromium.org

Change-Id: I868bc9b51c18a546994de93a3a8ef80362b0ba19
No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Bug: chromium:804279, chromium:633030
Reviewed-on: https://chromium-review.googlesource.com/891640
Reviewed-by: Samuel Huang <huangs@chromium.org>
Commit-Queue: Samuel Huang <huangs@chromium.org>
Cr-Commit-Position: refs/heads/master@{#532528}
[modify] https://crrev.com/e12ed52e5988fca99f50a5560a84beab39e51a39/third_party/WebKit/Source/platform/heap/HeapPage.cpp
[modify] https://crrev.com/e12ed52e5988fca99f50a5560a84beab39e51a39/third_party/WebKit/Source/platform/heap/HeapPage.h


### bu...@chromium.org (2018-01-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/efc102559ad670f9d8d6cf2bf5af3113603fc240

commit efc102559ad670f9d8d6cf2bf5af3113603fc240
Author: Hannes Payer <hpayer@chromium.org>
Date: Tue Jan 30 16:35:55 2018

Reland: Oilpan: Immediatelly promptly free objects.

Bug: chromium:804279, chromium:633030
Change-Id: I47f3b5ae087971105e64262cfe2e65495f99f3ca
Reviewed-on: https://chromium-review.googlesource.com/893181
Reviewed-by: Kentaro Hara <haraken@chromium.org>
Commit-Queue: Hannes Payer <hpayer@chromium.org>
Cr-Commit-Position: refs/heads/master@{#532909}
[modify] https://crrev.com/efc102559ad670f9d8d6cf2bf5af3113603fc240/third_party/WebKit/Source/platform/heap/HeapPage.cpp
[modify] https://crrev.com/efc102559ad670f9d8d6cf2bf5af3113603fc240/third_party/WebKit/Source/platform/heap/HeapPage.h


### aw...@chromium.org (2018-02-05)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-02-06)

Hi chris.rohlf@ - I'm very happy report that this bug has gone before the Chrome VRP panel, who decided to award $2,000!

A member of our finance team will be in touch to arrange for payment. Cheers!

### aw...@chromium.org (2018-02-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-02-08)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-02-08)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-02-09)

This bug requires manual review: Reverts referenced in bugdroid comments after merge request.
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), bhthompson@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2018-02-09)

[Bulk Edit]

+awhalley@ (Security TPM) for M65 merge review

### aw...@google.com (2018-02-09)

[Comment Deleted]

### aw...@google.com (2018-02-09)

[Empty comment from Monorail migration]

### go...@chromium.org (2018-02-09)

awhalley@, there are multiple CLs are listed here. Which one we need to merge to M65? Can this wait until M66 if not critical enough?

### ml...@chromium.org (2018-02-09)

I would neither back merge the commit in #56 or any later commits.

### go...@chromium.org (2018-02-09)

Rejecting merge to M65 based on https://crbug.com/chromium/633030#c73. 
awhalley@, pls let me know if there is any concern here. Thank you.

### aw...@google.com (2018-04-17)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-05-05)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-12-04)

[Empty comment from Monorail migration]

### va...@chromium.org (2021-09-16)

[Empty comment from Monorail migration]

[Monorail components: -Blink>MemoryAllocator>GarbageCollection Blink>GarbageCollection]

### yu...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-06)

This issue was migrated from crbug.com/chromium/633030?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084983)*
