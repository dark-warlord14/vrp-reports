# SEGV in v8::internal::Scavenger::Process

| Field | Value |
|-------|-------|
| **Issue ID** | [358485426](https://issues.chromium.org/issues/358485426) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>GarbageCollection |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | em...@gmail.com |
| **Assignee** | bi...@chromium.org |
| **Created** | 2024-08-09 |
| **Bounty** | $7,000.00 |

## Description

tested os:ubuntu 22.04 and MacOS
tested chromimum version:
Chromium 129.0.6647.0(gs://chromium-browser-asan/linux-release/asan-linux-release-1339466.zip)
Chromium 128.0.6601.2

The issue occurs during garbage collection within the V8 engine, specifically within the v8::internal::Scavenger::Process function. The SEGV is caused by an invalid memory write operation. The problem appears to be related to the handling of external pointers during heap scavenging.


repro steps:
./chrome --incognito --user-data-dir=/tmp/xx2 http://localhost:8880/crash.html --headless  --disable-gpu --disable-in-process-stack-traces

Note:
The issue is intermittently reproducible, with a 50% chance of triggering a segmentation fault (SEGV) or encountering a failed assertion (Check failed: IsValidHandle(old_handle).).


==1==ERROR: AddressSanitizer: SEGV on unknown address 0x79bcb5ec0000 (pc 0x579608a9b3dd bp 0x7ffcf0153a80 sp 0x7ffcf0153a50 T0)
==1==The signal is caused by a WRITE memory access.
    #0 0x579608a9b3dd in __cxx_atomic_store<v8::internal::TaggedPayload<v8::internal::ExternalPointerTableEntry::ExternalPointerTaggingScheme> > ../../third_party/libc++/src/include/__atomic/cxx_atomic_impl.h:304:3
    ,,,
    #2 0x579608a9b3dd in Evacuate ../../v8/src/sandbox/external-pointer-table-inl.h:144:17
    ,,,
    #4 0x579608a9b3dd in VisitExternalPointer ../../v8/src/heap/scavenger.cc:106:11
    ,,,
    #9 0x579608a754e0 in v8::internal::Scavenger::IterateAndScavengePromotedObject ../../v8/src/heap/scavenger.cc:728:11
    #10 0x579608a634d2 in v8::internal::Scavenger::Process ../../v8/src/heap/scavenger.cc:847:7
    ,,,
    #22 0x5796088dab40 in v8::internal::Heap::Scavenge ../../v8/src/heap/heap.cc:2804:25
    ,,,
    #29 0x5796088ac92e in v8::internal::HeapAllocator::AllocateRawWithLightRetrySlowPath ../../v8/src/heap/heap-allocator.cc:120:5
    ,,,
    #50 0x57960875c1f9 in v8::internal::MicrotaskQueue::PerformCheckpointInternal ../../v8/src/execution/microtask-queue.cc:129:3
SUMMARY: AddressSanitizer: SEGV (BuildId: b8ec94666b85371f)


## Attachments

- [crash.html](attachments/crash.html) (text/html, 190 B)
- [asan.log](attachments/asan.log) (text/plain, 40.3 KB)

## Timeline

### ma...@chromium.org (2024-08-10)

Based on the stack trace it seems like this may be the same as crash report [issue 348680350](https://issues.chromium.org/issues/348680350) but here there is a repro case.

I was able to repro on 128 and 129 but that crash bug indicates it may be happening on earlier versions as well, so provisionally marking with foundin for extended stable version. Provisionaly marking high severity.

### pe...@google.com (2024-08-10)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2024-08-10)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### cl...@appspot.gserviceaccount.com (2024-08-12)

Detailed Report: https://clusterfuzz.com/testcase?key=5174216338898944

Fuzzer: None
Job Type: windows_asan_chrome
Platform Id: windows

Crash Type: CHECK failure
Crash Address: 
Crash State:
  IsValidHandle(old_handle)
  gin::PrintStackTrace
  v8::internal::ExternalPointerTable::EvacuateAndSweepAndCompact
  
Sanitizer: address (ASAN)

Crash Revision: https://clusterfuzz.com/revisions?job=windows_asan_chrome&revision=1340342

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5174216338898944

Additional requirements: Requires HTTP



### sa...@google.com (2024-08-12)

Great thanks! This indeed looks like the same issue as [issue 348680350](https://issues.chromium.org/issues/348680350), so that'd be really nice! It reproduces fairly reliably locally but only flakily on CF. I've tried bisecting it locally, and it leads to <https://chromium.googlesource.com/chromium/src/+/03aef6340e3201112cd1b79bd9b002cd862e4b79> "heap: Remove MinorMS from fieldtrial and update perf configs". I'm guessing that's not what actually introduced the bug, but maybe it "unhid" the bug or something like that. In any case, it's probably a good starting point. Omer, could you take a look?

In terms of security impact, the two symptoms observed above are just stability issues (segfault on unmapped memory and CHECK failure otherwise), but I'm not sure if anything else can happen here, so I think we can just leave this as Type-Vulnerability out of precaution.

### om...@chromium.org (2024-08-13)

I tried looking into this one but didn't get very far.
The culprit CL likely only means that this is a Scavenger specific bug.
saelo reuploaded the testcase to CF with `--js-flags=--no-minor-ms` to hopefully get a better bisect (see https://clusterfuzz.com/testcase-detail/5278329936478208).
Asking current memory sheriff to take over since I'm OOO.

### bi...@chromium.org (2024-08-21)

Reproduced now. gdb suggests that the handle contains a zapped value. rr suggests that it was zapped in the epilogue of the previous Scavenger phase (here: https://source.chromium.org/chromium/chromium/src/+/main:v8/src/heap/heap.cc;l=1247). This branch runs only for Scavenger, however, with MinorMS we should still zap memory in the sweeper, so I'm not sure what is different semantically.

### bi...@chromium.org (2024-08-22)

What happens is as follows:
 - incremental marking runs,
 - the full GC marker marks the external pointer, creates an evacuation entry pointing to original handle,
 - we have an interleaved Scavenger. The object containing the external pointer handle survives and get copied onto another semispace (not promoted).
 - EPT::EvacuateAndSweepAndCompact() during MarkCompact will run into this stale evacuationentry pointing to the zapped handle and fail in the DCHECK(IsValidHandle(old_handle)).

What we could do is:
 1) update the evacuation entries at the end of the Scavenger (similar to how we update the marking worklist). This is not trivial though:
      - separate phase,
      - we need to get to the object start (e.g. through the marking bitmap) to get the forwarding pointer, compute the handle offset, etc..
 2) we could just abort compaction for interleaved GCs.

The second option sounds appealing, since it'll avoid introducity another layer of complexity to already complicated logic of GC interleaving. Samuel, do you have any thoughts?

### om...@chromium.org (2024-08-22)

Thanks for investigating Anton!

Based on your description, I assume the evacuating the object during Scavenger is creating a new handle for the "new" object, which is why the old one os getting zapped. Could we instead just reuse the old handle? Just copy it as is? IIUC the old handle would still be valid and this will also fix the issue.

With Scavenger, I believe most full GCs have interleaved scavenges, so I suspect option 2 would mean that we almost always abort compaction, and thus regress memory.

### bi...@chromium.org (2024-08-22)

> I assume the evacuating the object during Scavenger is creating a new handle for the "new" object, which is why the old one os getting zapped.

No, actually evacuating the object during Scavenger neither creates a new handle nor updates the current one. It bails out, assuming the full GC will take care of it: https://source.chromium.org/chromium/chromium/src/+/main:v8/src/heap/scavenger-inl.h;l=554

The new evacuation-entry is created when the full GC marker marks the external pointer entry and iiuc is needed to update the handle itself (i.e. the slot) during EPT compaction. The issue is that this evacuation entry is not updated if the object was semi-space copied.


### sa...@google.com (2024-08-23)

In general I would vote for reducing complexity if possible, so to avoid interleaving GCs. Wrt. to security, less complexity is usually better :)

### ml...@chromium.org (2024-08-23)

> In general I would vote for reducing complexity if possible, so to avoid interleaving GCs. Wrt. to security, less complexity is usually better :)

I think that is the longer term plan. We need something short-term as well.

Would aborting compactiong for the segment just work out of the box?

### sa...@google.com (2024-08-23)

Hm so we can indeed [abort EPT compaction](https://source.chromium.org/chromium/chromium/src/+/main:v8/src/sandbox/compactible-external-entity-table-inl.h;l=130;drc=82dff63dbf9db05e9274e11d9128af7b9f51ceaa), but I think in that case we would still try to [resolve any evacuation entry we find during sweeping](https://source.chromium.org/chromium/chromium/src/+/main:v8/src/sandbox/external-pointer-table.cc;l=169;drc=11b2f0446216ef5c52f423dbb883831db8646911). So I think that wouldn't actually solve the problem here because the evacuation entry may already exist? I guess we could add another state though to indicate that compaction is aborted and that any evacuation entry must be ignored (or really, clobbered) during sweeping though. I think that could work.

### ap...@google.com (2024-08-27)

Project: v8/v8
Branch: main

commit 1a2b08edbec1a8ebcf3d4adc91da4f2569fb744a
Author: Anton Bikineev <bikineev@chromium.org>
Date:   Tue Aug 27 11:24:48 2024

    heap,sandbox: Update EPT's evacuation entries in Scavenger.
    
    If Scavenger interleaves MarkCompact that performs compaction on EPT,
    there may be some evacuation entries allocated in the young EPT that
    would back-point to the Scavenger's from-space. Add a new phase that
    updates all the evacuation entries in the young EPT up until
    `start_of_evacation_area`.
    
    Bug: 358485426
    Change-Id: Ic23e57ff38279d4e93964cf21ee62eb01ebe8e61
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5805957
    Reviewed-by: Samuel Groß <saelo@chromium.org>
    Reviewed-by: Michael Lippautz <mlippautz@chromium.org>
    Commit-Queue: Anton Bikineev <bikineev@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#95827}

M       src/heap/incremental-marking.cc
M       src/heap/incremental-marking.h
M       src/heap/scavenger.cc
M       src/sandbox/compactible-external-entity-table.h
M       src/sandbox/external-pointer-table.cc
M       src/sandbox/external-pointer-table.h

https://chromium-review.googlesource.com/5805957


### 24...@project.gserviceaccount.com (2024-08-28)

ClusterFuzz testcase 5174216338898944 is verified as fixed in https://clusterfuzz.com/revisions?job=windows_asan_chrome&range=1347411:1347433

If this is incorrect, please add the hotlistid:5433040 and re-open the issue.

### pe...@google.com (2024-08-28)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M128. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M129. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request - Manual Review: Merge review required: M128 is already shipping to stable.

Security Merge Request - Manual Review: Merge review required: M129 is already shipping to beta.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [128, 129].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### pe...@google.com (2024-08-29)

Security Merge Request Consideration: Not requesting merge to stable (M128) because latest trunk commit (95827) appears to be prior to stable branch point (1331488). If this is incorrect please remove NA-128 from the 'Merge' field and add 128 to the 'Merge-Request' field If other changes are required to fix this bug completely please request a merge if necessary.
Security Merge Request Consideration: Not requesting merge to beta (M129) because latest trunk commit (95827) appears to be prior to beta branch point (1343869). If this is incorrect please remove NA-129 from the 'Merge' field and add 129 to the 'Merge-Request' field If other changes are required to fix this bug completely please request a merge if necessary.
Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### am...@chromium.org (2024-08-29)

There have been a full 48 hours of bake time since this fix <https://crrev.com/c/5805957> landed on canary; I'm not seeing any issues with a potential backmerge; so I am tentatively approving backmerge. This is a textually large change, so please ensure there are no risks or concerns with this fix before backmerging.

If there are no risks or other concerns, please backmerge to 12.9 and 12.8 by EOD Friday (tomorrow, 30 August) so this fix can be included in next week's updates. Thank you!

### pb...@google.com (2024-08-30)

Thank you deepti, the cherry pick to M128 branch is in CQ now https://chromium-review.googlesource.com/c/v8/v8/+/5827960

### ap...@google.com (2024-08-30)

Project: v8/v8
Branch: refs/branch-heads/12.8

commit e75055b000b8c2455c60bfddda92ac4e57fcb0ab
Author: Anton Bikineev <bikineev@chromium.org>
Date:   Tue Aug 27 11:24:48 2024

    Merged: heap,sandbox: Update EPT's evacuation entries in Scavenger.
    
    If Scavenger interleaves MarkCompact that performs compaction on EPT,
    there may be some evacuation entries allocated in the young EPT that
    would back-point to the Scavenger's from-space. Add a new phase that
    updates all the evacuation entries in the young EPT up until
    `start_of_evacation_area`.
    
    Bug: 358485426
    
    (cherry picked from commit 1a2b08edbec1a8ebcf3d4adc91da4f2569fb744a)
    
    Change-Id: Iadabe3ded39b32d8908e5d4e8fbff593b977940c
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5827960
    Auto-Submit: Deepti Gandluri <gdeepti@chromium.org>
    Reviewed-by: Matthias Liedtke <mliedtke@chromium.org>
    Commit-Queue: Deepti Gandluri <gdeepti@chromium.org>
    Cr-Commit-Position: refs/branch-heads/12.8@{#50}
    Cr-Branched-From: 70cbb397b153166027e34c75adf8e7993858222e-refs/heads/12.8.374@{#1}
    Cr-Branched-From: 451b63ed4251c2b21c56144d8428f8be3331539b-refs/heads/main@{#95151}

M       src/heap/incremental-marking.cc
M       src/heap/incremental-marking.h
M       src/heap/scavenger.cc
M       src/sandbox/compactible-external-entity-table.h
M       src/sandbox/external-pointer-table.cc
M       src/sandbox/external-pointer-table.h

https://chromium-review.googlesource.com/5827960


### pe...@google.com (2024-08-30)

LTS Milestone M126

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### pb...@google.com (2024-08-30)

The Cl has been merged to M128 branch as comment#21, hence dropping Approved-128

### pe...@google.com (2024-09-02)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### go...@google.com (2024-09-03)

Please merge your change to M129 by 3:00 PM PT today so we can take it in for this week's M129 beta release.

M129 Branch Details: https://chromiumdash.appspot.com/branches

### pe...@google.com (2024-09-04)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### rz...@google.com (2024-09-04)

1. Just <https://crrev.com/c/5834610>
2. Low, no conflicts
3. 128, 129
4. Yes

### sp...@google.com (2024-09-04)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $7000.00 for this report.

Rationale for this decision:
baseline report of memory corruption in a sandboxed process / renderer


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-09-04)

Congratulations Cassidy Kim! Thank you for your efforts and reporting this issue to us.

### pe...@google.com (2024-09-06)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### qk...@google.com (2024-09-07)

https://crrev.com/c/5805957 is not applicable to LTS M120 branch because M120 LTS branch doesn't support the young generation external pointer space so we're not sure if the LTS version was affected by this bug. So I add "LTS-NonApplicable-120" label to this bug.

### ap...@google.com (2024-09-08)

Project: v8/v8
Branch: refs/branch-heads/12.9

commit 5476a6f9e4d485ffe3eb1a70de4e1bb4c74f8738
Author: Anton Bikineev <bikineev@chromium.org>
Date:   Tue Aug 27 11:24:48 2024

    [M129]: heap,sandbox: Update EPT's evacuation entries in Scavenger.
    
    If Scavenger interleaves MarkCompact that performs compaction on EPT,
    there may be some evacuation entries allocated in the young EPT that
    would back-point to the Scavenger's from-space. Add a new phase that
    updates all the evacuation entries in the young EPT up until
    `start_of_evacation_area`.
    
    (cherry picked from commit 1a2b08edbec1a8ebcf3d4adc91da4f2569fb744a)
    
    Bug: 358485426
    Change-Id: Ic23e57ff38279d4e93964cf21ee62eb01ebe8e61
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5805957
    Reviewed-by: Samuel Groß <saelo@chromium.org>
    Reviewed-by: Michael Lippautz <mlippautz@chromium.org>
    Commit-Queue: Anton Bikineev <bikineev@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#95827}
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5839896
    Cr-Commit-Position: refs/branch-heads/12.9@{#27}
    Cr-Branched-From: 64a21d7ad7fca1ddc73a9264132f703f35000b69-refs/heads/12.9.202@{#1}
    Cr-Branched-From: da4200b2cfe6eb1ad73c457ed27cf5b7ff32614f-refs/heads/main@{#95679}

M       src/heap/incremental-marking.cc
M       src/heap/incremental-marking.h
M       src/heap/scavenger.cc
M       src/sandbox/compactible-external-entity-table.h
M       src/sandbox/external-pointer-table.cc
M       src/sandbox/external-pointer-table.h

https://chromium-review.googlesource.com/5839896


### go...@google.com (2024-09-09)

Please merge your change to M129 latest by 10:00 AM PT tomorrow, Sept 10th so we can take it in for this week's M129 Early Stable release on Wednesday, Sept 11th.

M129 branch Details: https://chromiumdash.appspot.com/branches

### ap...@google.com (2024-10-18)

Project: v8/v8  

Branch: refs/branch-heads/12.6  

Author: Anton Bikineev <[bikineev@chromium.org](mailto:bikineev@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/5834610>

[M126-LTS] heap,sandbox: Update EPT's evacuation entries in Scavenger.

---


Expand for full commit details
```
[M126-LTS] heap,sandbox: Update EPT's evacuation entries in Scavenger.

If Scavenger interleaves MarkCompact that performs compaction on EPT,
there may be some evacuation entries allocated in the young EPT that
would back-point to the Scavenger's from-space. Add a new phase that
updates all the evacuation entries in the young EPT up until
`start_of_evacation_area`.

(cherry picked from commit 1a2b08edbec1a8ebcf3d4adc91da4f2569fb744a)

Bug: 358485426
Change-Id: Ic23e57ff38279d4e93964cf21ee62eb01ebe8e61
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5834610
Commit-Queue: Toon Verwaest <verwaest@chromium.org>
Reviewed-by: Igor Sheludko <ishell@chromium.org>
Reviewed-by: Anton Bikineev <bikineev@chromium.org>
Reviewed-by: Toon Verwaest <verwaest@chromium.org>
Cr-Commit-Position: refs/branch-heads/12.6@{#72}
Cr-Branched-From: 3c9fa12db3183a6f4ea53d2675adb66ea1194529-refs/heads/12.6.228@{#2}
Cr-Branched-From: 981bb15ba4dbf9e2381dfc94ec2c4af0b9c6a0b6-refs/heads/main@{#93835}

```

---

Files:

- M `src/heap/incremental-marking.cc`
- M `src/heap/incremental-marking.h`
- M `src/heap/scavenger.cc`
- M `src/sandbox/compactible-external-entity-table.h`
- M `src/sandbox/external-pointer-table.cc`
- M `src/sandbox/external-pointer-table.h`

---

Hash: 31c7633a888e238c481138249377b4049ff87560  

Date:  Tue Aug 27 11:24:48 2024


---

### pe...@google.com (2024-12-05)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/358485426)*
