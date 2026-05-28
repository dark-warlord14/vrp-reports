# Crash in v8::internal::EvacuationVerifier::VerifyEvacuation

| Field | Value |
|-------|-------|
| **Issue ID** | [40073846](https://issues.chromium.org/issues/40073846) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Blink>JavaScript>GarbageCollection |
| **Platforms** | Linux |
| **Reporter** | m....@gmail.com |
| **Assignee** | ml...@chromium.org |
| **Created** | 2023-10-01 |
| **Bounty** | $9,000.00 |

## Description

Detailed Report: https://clusterfuzz.com/testcase?key=5037012981317632

Fuzzer: b0ring_webidl_fuzzer
Job Type: linux_asan_chrome_media
Platform Id: linux

Crash Type: UNKNOWN READ
Crash Address: 0x7938beadbef6
Crash State:
  v8::internal::EvacuationVerifier::VerifyEvacuation
  v8::internal::EvacuationVerifier::Run
  v8::internal::Heap::EnsureSweepingCompleted
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_media&range=1196594:1196604

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5037012981317632

Issue filed automatically.

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


## Timeline

### [Deleted User] (2023-10-01)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-10-01)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Blink>JavaScript>GarbageCollection]

### cl...@chromium.org (2023-10-01)

Automatically assigning owner based on suspected regression changelist https://chromium.googlesource.com/v8/v8/+/05d2ea11094eeddfd25ba8638722c72057c49f20 ([heap] Remove PageRange with addresses).

If this is incorrect, please let us know why and apply the Test-Predator-Wrong-CLs label. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### [Deleted User] (2023-10-01)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-10-01)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### va...@chromium.org (2023-10-02)

We've a public holiday in GER therefore adding the MTV sheriffs to PTAL.

### di...@chromium.org (2023-10-02)

I already started looking into this. I believe this is not a release-blocker since this happens with minor-mc which we don't use in production yet, see this line on the the stack trace: https://chromium.googlesource.com/v8/v8/+/ac29617dc7cd9f9a5e4c6f132c26277c4852c6c6/src/heap/evacuation-verifier.cc#91

### be...@google.com (2023-10-02)

Adding Hotlist-RBS-Removed for tracking purposes.

### di...@chromium.org (2023-10-04)

Looks like the evacuation verifier fails because we have new space allocations after the GC. This is because of cppgc sweeping, which may allocate. Reassigning to mlippautz@ to not finish sweeping in the safepoint GC pause. 

### gi...@appspot.gserviceaccount.com (2023-10-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/517ab248723851bfe2a390d4ceb70c648b72b621

commit 517ab248723851bfe2a390d4ceb70c648b72b621
Author: Michael Lippautz <mlippautz@chromium.org>
Date: Fri Oct 06 09:45:04 2023

cppgc: Rewire atomic sweeping

Instead of finishing atomic sweeping when sweeping starts delay the
actual sweeping phase till after leaving the V8 safepoint. This
prevents Oilpan and V8 allocations from interfering with heap layouts
and verifiers.

The concrete case is that heap verification runs at the end of the
safepoint and assumes no LABs are present. Atomic Oilpan sweeping may
call back into V8 in finalizers which may create a LAB via an
allocation. This is undefined behavior as V8 is still in a safepoint
and should thus be worked around.

Bug: chromium:1488263
Change-Id: Id9fc696909c42c75cf7de0001205d6870aa939ed
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4905775
Reviewed-by: Anton Bikineev <bikineev@chromium.org>
Reviewed-by: Dominik Inführ <dinfuehr@chromium.org>
Commit-Queue: Michael Lippautz <mlippautz@chromium.org>
Cr-Commit-Position: refs/heads/main@{#90275}

[modify] https://crrev.com/517ab248723851bfe2a390d4ceb70c648b72b621/src/heap/cppgc/heap.cc
[modify] https://crrev.com/517ab248723851bfe2a390d4ceb70c648b72b621/src/heap/cppgc/sweeper.h
[modify] https://crrev.com/517ab248723851bfe2a390d4ceb70c648b72b621/src/heap/heap.cc
[modify] https://crrev.com/517ab248723851bfe2a390d4ceb70c648b72b621/src/heap/cppgc-js/cpp-heap.cc
[modify] https://crrev.com/517ab248723851bfe2a390d4ceb70c648b72b621/src/heap/cppgc/heap-base.cc
[modify] https://crrev.com/517ab248723851bfe2a390d4ceb70c648b72b621/src/heap/cppgc-js/cpp-heap.h
[modify] https://crrev.com/517ab248723851bfe2a390d4ceb70c648b72b621/src/heap/cppgc/sweeper.cc
[modify] https://crrev.com/517ab248723851bfe2a390d4ceb70c648b72b621/test/unittests/heap/cppgc/compactor-unittest.cc


### ml...@chromium.org (2023-10-06)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-06)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-10-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/65dfc43ea42889e682e597118b683ae12accd669

commit 65dfc43ea42889e682e597118b683ae12accd669
Author: Omer Katz <omerkatz@chromium.org>
Date: Sat Oct 07 07:54:54 2023

Revert "cppgc: Rewire atomic sweeping"

This reverts commit 517ab248723851bfe2a390d4ceb70c648b72b621.

Reason for revert: Break debug chromium builds because heap verification finalizes sweeping before `FinishAtomicSweepingIfNeeded` is called, making a DCHECK that sweeping is in progress fail.

Original change's description:
> cppgc: Rewire atomic sweeping
>
> Instead of finishing atomic sweeping when sweeping starts delay the
> actual sweeping phase till after leaving the V8 safepoint. This
> prevents Oilpan and V8 allocations from interfering with heap layouts
> and verifiers.
>
> The concrete case is that heap verification runs at the end of the
> safepoint and assumes no LABs are present. Atomic Oilpan sweeping may
> call back into V8 in finalizers which may create a LAB via an
> allocation. This is undefined behavior as V8 is still in a safepoint
> and should thus be worked around.
>
> Bug: chromium:1488263
> Change-Id: Id9fc696909c42c75cf7de0001205d6870aa939ed
> Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4905775
> Reviewed-by: Anton Bikineev <bikineev@chromium.org>
> Reviewed-by: Dominik Inführ <dinfuehr@chromium.org>
> Commit-Queue: Michael Lippautz <mlippautz@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#90275}

Bug: chromium:1488263
Change-Id: If9d91bf9d231a01c154cb3e225d847b74f020642
No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4916665
Auto-Submit: Omer Katz <omerkatz@chromium.org>
Commit-Queue: Omer Katz <omerkatz@chromium.org>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#90285}

[modify] https://crrev.com/65dfc43ea42889e682e597118b683ae12accd669/src/heap/cppgc/heap.cc
[modify] https://crrev.com/65dfc43ea42889e682e597118b683ae12accd669/src/heap/cppgc/sweeper.h
[modify] https://crrev.com/65dfc43ea42889e682e597118b683ae12accd669/src/heap/heap.cc
[modify] https://crrev.com/65dfc43ea42889e682e597118b683ae12accd669/src/heap/cppgc-js/cpp-heap.cc
[modify] https://crrev.com/65dfc43ea42889e682e597118b683ae12accd669/src/heap/cppgc/heap-base.cc
[modify] https://crrev.com/65dfc43ea42889e682e597118b683ae12accd669/src/heap/cppgc-js/cpp-heap.h
[modify] https://crrev.com/65dfc43ea42889e682e597118b683ae12accd669/src/heap/cppgc/sweeper.cc
[modify] https://crrev.com/65dfc43ea42889e682e597118b683ae12accd669/test/unittests/heap/cppgc/compactor-unittest.cc


### gi...@appspot.gserviceaccount.com (2023-10-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/51dc737a0cf838bad4032f54356809bf60d03032

commit 51dc737a0cf838bad4032f54356809bf60d03032
Author: Michael Lippautz <mlippautz@chromium.org>
Date: Mon Oct 09 13:33:26 2023

Reland "cppgc: Rewire atomic sweeping"

This is a reland of commit 517ab248723851bfe2a390d4ceb70c648b72b621

Original change's description:
> cppgc: Rewire atomic sweeping
>
> Instead of finishing atomic sweeping when sweeping starts delay the
> actual sweeping phase till after leaving the V8 safepoint. This
> prevents Oilpan and V8 allocations from interfering with heap layouts
> and verifiers.
>
> The concrete case is that heap verification runs at the end of the
> safepoint and assumes no LABs are present. Atomic Oilpan sweeping may
> call back into V8 in finalizers which may create a LAB via an
> allocation. This is undefined behavior as V8 is still in a safepoint
> and should thus be worked around.
>
> Bug: chromium:1488263
> Change-Id: Id9fc696909c42c75cf7de0001205d6870aa939ed
> Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4905775
> Reviewed-by: Anton Bikineev <bikineev@chromium.org>
> Reviewed-by: Dominik Inführ <dinfuehr@chromium.org>
> Commit-Queue: Michael Lippautz <mlippautz@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#90275}

Bug: chromium:1488263
Change-Id: Idf12fe0c7661dbd9454d7eb60637a345ac1db343
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4921730
Reviewed-by: Anton Bikineev <bikineev@chromium.org>
Reviewed-by: Dominik Inführ <dinfuehr@chromium.org>
Commit-Queue: Michael Lippautz <mlippautz@chromium.org>
Cr-Commit-Position: refs/heads/main@{#90322}

[modify] https://crrev.com/51dc737a0cf838bad4032f54356809bf60d03032/src/heap/cppgc/heap.cc
[modify] https://crrev.com/51dc737a0cf838bad4032f54356809bf60d03032/src/heap/cppgc/sweeper.h
[modify] https://crrev.com/51dc737a0cf838bad4032f54356809bf60d03032/src/heap/heap.cc
[modify] https://crrev.com/51dc737a0cf838bad4032f54356809bf60d03032/src/heap/cppgc-js/cpp-heap.cc
[modify] https://crrev.com/51dc737a0cf838bad4032f54356809bf60d03032/src/heap/cppgc/heap-base.cc
[modify] https://crrev.com/51dc737a0cf838bad4032f54356809bf60d03032/src/heap/cppgc-js/cpp-heap.h
[modify] https://crrev.com/51dc737a0cf838bad4032f54356809bf60d03032/src/heap/cppgc/sweeper.cc
[modify] https://crrev.com/51dc737a0cf838bad4032f54356809bf60d03032/test/unittests/heap/cppgc/compactor-unittest.cc


### cl...@chromium.org (2023-10-11)

ClusterFuzz testcase 5037012981317632 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_media&range=1207567:1207575

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### am...@google.com (2023-10-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-10-11)

Congratulations! The Chrome VRP Panel has decided to award you $7,000 for this report + $2,000 fuzzer bonus. Thank you for your efforts toward Chrome Fuzzing that resulted in this report -- nice work! 

### am...@chromium.org (2023-10-13)

[Empty comment from Monorail migration]

### am...@google.com (2023-10-13)

[Empty comment from Monorail migration]

### ml...@chromium.org (2023-10-16)

For posterity: https://crbug.com/chromium/1488263#c9 was not super clear here but this was merely a verification issue. We don't see how this can cause issues with release builds.

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-12)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2024-01-12)

This issue was migrated from crbug.com/chromium/1488263?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40073846)*
