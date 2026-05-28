# MiraclePtr bypass due to PtrCount overflow

| Field | Value |
|-------|-------|
| **Issue ID** | [377803496](https://issues.chromium.org/issues/377803496) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Unknown |
| **Platforms** | Android, Linux, Mac, Windows, iOS, ChromeOS |
| **Chrome Version** | 124.0.0.0 |
| **Reporter** | ha...@gmail.com |
| **Assignee** | gl...@google.com |
| **Created** | 2024-11-07 |
| **Bounty** | $100,115.00 |

## Description

# PROBLEM DETAILS

## Root Cause Analysis

PartitionAlloc supports multi-threaded allocations. When BRP is enabled, each slot contains a metadata field to store information such as refcount, which also supports read/write in parallel.

In the function `PartitionRoot::FreeNoHooksImmediate`:

```
    auto* ref_count = InSlotMetadataPointerFromSlotStartAndSize(
        slot_start, slot_span->bucket->slot_size);
    // ...
    if (!ref_count->IsAliveWithNoKnownRefs()) [[unlikely]] {  // [0]
      QuarantineForBrp(slot_span, object);
    }

    if (!(ref_count->ReleaseFromAllocator())) [[unlikely]] {  // [1]

```

The `ref_count` is read at both lines [0] and [1], i.e., the metadata field. Specifically, at [0], it checks whether `ref_count` has only the `kMemoryHeldByAllocatorBit` set. At [1], the `kMemoryHeldByAllocatorBit` of `ref_count` is cleared, and the value of `ref_count` is **re-read**.

The issue arises from this memory double fetch. Between the two reads, `ref_count` may be modified, leading to inconsistent logic.

[0] <https://source.chromium.org/chromium/chromium/src/+/main:base/allocator/partition_allocator/src/partition_alloc/partition_root.h;drc=a45502c46d75f210c783e07384138379ea1e46e4;l=1596>

## Impact Analysis

There are two potential destructive effects:

**First Destructive Effect**: The first fetch determines that the pointer needs to be quarantined, while the second check concludes that it does not, falling through to the normal free process. This error results in inaccurate statistics in the second `if`, which is not a big deal.

**Second Destructive Effect**: The first fetch determines that the pointer does not need to be quarantined, while the second check concludes that it does. This would result in the slot not being freed, and the original retained data is not destroyed by the `QuarantineForBrp` function!

## Exploit Analysis

To trigger this issue, it is necessary to ensure that the first `if` checks `ref_count` as 0, while the second check sees `ref_count` as non-zero. This means that there must be a raw pointer's Acquire operation between the two fetches, incrementing `ref_count`.

Assuming the UaF (Use-after-Free) object is `target`, the exploitation process is as follows:

1. Create `target`, ensuring it has no raw\_ptr `ref_count`.
2. Trigger the delete operation for `target`.
3. At a certain moment during the delete execution, specifically after the first `if` fetch and before the second `if` fetch, trigger the raw pointer operation to increase `ref_count`.
4. Trigger the UaF. At this point, the UaF will not trigger any exceptions.

# REPRODUCTION CASE

Thanks to [issue 340122160](https://issues.chromium.org/issues/340122160) for providing the PoC. This PoC is modified based on that version.

To obtain the ASAN version of the crash log:

1. After `git apply patch1.diff`, build the ASAN version of Chromium.
2. Run `python3 copy_mojo_js_bindings.py path/to/out/asan/gen`.
3. Start HTTP server: `python -m http.server`.
4. Start Chrome to visit `miracle.html`:
   
   ```
   ./chrome --enable-blink-features=MojoJS 'http://localhost:8000/miracle.html'
   
   ```

You will then see the ASAN crash.

To reproduce in the Release version:

1. After applying `patch1.diff`, apply `patch2.diff`, and then build the Release version of Chromium.
2. Repeat the steps above for the ASAN version to access `miracle.html`. If you see the message `If this is printed, that means attack is successful`, it indicates that the raw\_ptr check has been bypassed. Example log:
   
   ```
   [NewObject] enter
   owned ptr: 0x69c01837e00
   [AsyncTask] enter
   [ThreadPoolTask] enter
   [ResetObject] enter
   [TriggerInUI] enter
   If this is printed, that means attack is successful
   
   ```

# SUGGESTED FIX

In fact, the conditions under which `IsAliveWithNoKnownRefs` and `ReleaseFromAllocator` return true are consistent. Both check whether `ref_count` is 0, the difference is that `ReleaseFromAllocator` clears the `kMemoryHeldByAllocatorBit` and checks for double free. The check of `IsAliveWithNoKnownRefs` is effectively weaker than that of `ReleaseFromAllocator`, so we can retain only the latter.

For details, see `fix.diff`.

# CRASH INFORMATION

Type of crash: MiraclePtr Bypass

Crash log: see asan.txt

# CREDIT INFORMATION

Reporter credit: DARKNAVY(@DarkNavyOrg)

## Attachments

- [patch1.diff](attachments/patch1.diff) (text/x-diff, 6.0 KB)
- [patch2.diff](attachments/patch2.diff) (text/x-diff, 2.7 KB)
- [copy_mojo_js_bindings.py](attachments/copy_mojo_js_bindings.py) (text/x-python, 653 B)
- [miracle.html](attachments/miracle.html) (text/html, 888 B)
- [asan.txt](attachments/asan.txt) (text/plain, 18.2 KB)
- [fix.diff](attachments/fix.diff) (text/x-diff, 1.0 KB)

## Timeline

### me...@google.com (2024-11-07)

Thanks for the report. Setting initial labels and owner based on [bug 340122160](https://issues.chromium.org/issues/340122160).

### me...@google.com (2024-11-08)

I can't repro on stable due to a patch being required in the repro steps, but the problematic code has been there for some time. Assuming this affects stable.

### ap...@google.com (2024-11-08)

Project: chromium/src  

Branch: main  

Author: Sergei Glazunov <[glazunov@google.com](mailto:glazunov@google.com)>  

Link:      <https://chromium-review.googlesource.com/6000544>

[BRP] Make sure all quarantined allocations are zapped

---


Expand for full commit details
```
[BRP] Make sure all quarantined allocations are zapped 
 
Bug: 377803496 
Change-Id: Ifb0c7fdd7fb5537178cde6220b99eb8a9ecc74b2 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6000544 
Reviewed-by: Kentaro Hara <haraken@chromium.org> 
Commit-Queue: Sergei Glazunov <glazunov@google.com> 
Cr-Commit-Position: refs/heads/main@{#1380330}

```

---

Files:

- M `base/allocator/partition_allocator/src/partition_alloc/partition_root.h`

---

Hash: bca210b2ebf688c23bfd0274fe6329280c4f7683  

Date:  Fri Nov 08 13:48:26 2024


---

### gl...@google.com (2024-11-15)

Thank you for the report!

The report describes a valid issue in the MiraclePtr implementation. This issue leads to protection degradation – a situation where a problematic allocation is quarantined but its contents are not “zapped.” As a result, the contents may still contain addresses of valid memory blocks. It has been previously demonstrated that, in many cases, quarantining without zapping can be exploited.

However, in practice, only a tiny proportion of use-after-free issues satisfy the conditions required for this attack. To recap:

1. Thread 1 holds an owning reference/pointer to a target allocation.
2. Thread 2 has a reference to a non-owning non-raw\_ptr pointer to the same allocation.
3. No raw\_ptr's point to the allocation.
4. Thread 1 calls `free()`, which passes the `IsAliveWithNoKnownRefs` check without zapping.
5. Thread 2 creates a new raw\_ptr to the allocation from a non-raw\_ptr.
6. Thread 1 reaches `ReleaseFromAllocator` and quarantines the allocation.
7. Thread 2 passes the raw\_ptr to Thread 1.
8. Thread 1 dereferences the raw\_ptr.

The combination of 3, 5, and 7 makes this scenario extremely unlikely.

In some of the steps above, a far more common alternative is a simple race condition issue. For example, in (7), Thread 2 is more likely to dereference the pointer on its own. However, this creates a memory safety issue before a use-after-free can happen – a race between the destructor in Thread 1 and use in Thread 2. BRP-ASan should correctly report such a case as “not protected.”

Unfortunately, we cannot apply the proposed fix. After returning from `IsAliveWithNoKnownRefs`, nothing prevents another thread from releasing the last remaining `raw_ptr` referencing the allocation. This would cause the allocation to be “finally freed” via a `RawFreeWithThreadCache` call, which could race with `QuarantineForBrp` (essentially, `memset`) and lead to a more serious issue than protection degradation – actual memory corruption in the allocator.

Luckily, since the attack scenario is so complex, it seems to never happen “organically” in Chrome. Therefore, we were able to add a defensive `PA_CHECK` to ensure that if the `ReleaseFromAllocator` branch is taken, `IsAliveWithNoKnownRefs` must also be taken.

### vu...@darknavy.com (2024-11-19)

Thank you for your explanation. The fix I suggested would indeed lead to other race issues. I think your fix is great :)

### gl...@google.com (2024-11-28)

After further consideration, we have concluded that the described technique does not bypass MiraclePtr protection.

The report describes a scenario where "the first fetch determines that the pointer does not need to be quarantined, while the second check concludes that it does. This would result in the slot not being freed, and the original retained data is not destroyed by the QuarantineForBrp function."

However, this scenario requires a native C++ pointer to be assigned to a MiraclePtr object in a second thread while the first thread is in the middle of FreeNoHooksImmediate() for the same allocation. Because the threads are not synchronized, the assignment could also happen slightly later – specifically, just after the first thread returns from FreeNoHooksImmediate(). In this situation, which we refer to as "pointer laundering," the MiraclePtr object may end up pointing to a freed memory block. If dereferenced later, as the report also requires, a regular use-after-free may occur.

We consider individual "pointer laundering" cases to be high-severity security issues. Because the technique described in the report requires a condition that can always be turned into pointer laundering, we consider the bypass invalid.

We're happy to reconsider our position if you can provide a realistic scenario or an example of an issue (historical or new) where the technique makes a bug exploitable that is not exploitable through pointer laundering.

### vu...@darknavy.com (2024-11-29)

Thank you for your analysis!
﻿

I indeed cannot find a realistic code scenario that satisfies the attack conditions, but I also don't think that the previous valid bypass was particularly "realistic" (it requires precisely overflowing a 31-bit unsigned int refcount).
﻿

However, I still have some questions about the explanation here. I don't know if PartitionAlloc has some mechanism (memory synchronization or something else?) preventing this scenario.
﻿

Regarding this scenario, I have some supplementary points:
﻿

The race only occurs in one place: thread 2 performing an increment operation on the refcount. More accurately: the instruction `lock xadd [rcx], eax` (on Windows). This instruction needs to be executed between two `if` statements. After this instruction is executed, whether or not `FreeNoHooksImmediate()` continues to finish its execution is no longer important. In the PoC, we wait for it to finish executing because we need ASAN to catch this use-after-free.
﻿

So I'm still unclear on how "pointer laundering" works. Could you explain it in more detail?

### am...@chromium.org (2024-12-05)

Thank you for this report and your efforts against MiraclePtr protection. Since this was determined to not be a successful bypass, this report is unfortunately not eligible for a Chrome VRP reward.

### ch...@google.com (2025-02-22)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/377803496)*
