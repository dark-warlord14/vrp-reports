# heap-use-after-free in BlinkGC

| Field | Value |
|-------|-------|
| **Issue ID** | [40091344](https://issues.chromium.org/issues/40091344) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>GarbageCollection |
| **Platforms** | Linux |
| **Reporter** | cd...@gmail.com |
| **Assignee** | ml...@chromium.org |
| **Created** | 2018-05-09 |
| **Bounty** | $2,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36

Steps to reproduce the problem:
1. Build source code 
    config args.gn file as below:
		use_sanitizer_coverage = true
		is_asan = true
		is_debug = false
		enable_nacl = false
		treat_warnings_as_errors = false
	ninja -j4 -C out/chrome_asan chrome
2. Build a mini web server.
	I used python twisted module to build the webserver.
	1) cp 1.ogg(OR any other normal ogg file) to webserver/res/
	2) python webserver/web.py
3. ./chrome http://127.0.0.1:8605/poc.html

What is the expected behavior?
no process crash

What went wrong?
could stably get crash and received signal 11 SEGV_MAPERR,or occasionally get "use-after-free" .
and the two log files of stack trace are different.see signal11.txt and uaf.txt.

Did this work before? N/A 

Chrome version: 68.0.3419.0  Channel: dev
OS Version: 16.04
Flash Version:

## Attachments

- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)

## Timeline

### cd...@gmail.com (2018-05-09)

two logs came from two different vitrul host and the OS version are both ubuntu 16.04.
The chrome version of signal11.log is  68.0.3419.0 (64-bit) (dev) ,another is  68.0.3404.0  (64-bit)  (dev).

### rs...@chromium.org (2018-05-09)

vmiura: Can you take a look at this (or help route)?

I tried throwing this to Clusterfuzz (https://clusterfuzz.com/v2/testcase-detail/6582282991960064) but I think the webserver interaction may be difficult.

[Monorail components: Internals>GPU]

### vm...@chromium.org (2018-05-09)

I think there are two unrelated issues here, and we should split them.

1) There is a heap-use-after-free triggered in the Blink-GC, as per signal11.log.  Let's keep this under this issue.

2) There's a crash in the GPU process while calling into glQueryCounter().  We likely need to blacklist GPU timers on this driver.  I'm going to fork this into a separate issue.

hpayer@ could you help route the Blink-GC issue?

[Monorail components: -Internals>GPU Blink>JavaScript>GC]

### vm...@chromium.org (2018-05-09)

> 1) There is a heap-use-after-free triggered in the Blink-GC, as per signal11.log.  Let's keep this under this issue.

This should have said "as per uaf.log".

### vm...@chromium.org (2018-05-09)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-05-10)

[Empty comment from Monorail migration]

### hp...@chromium.org (2018-05-15)

Kentaro, can you find an owner in TOK for this?

Interesting, we ASAN unpoison the dead memory area before checking for finalizer: https://cs.chromium.org/chromium/src/third_party/blink/renderer/platform/heap/heap_page.cc?type=cs&q=heap_page&sq=package:chromium&l=1443 It looks like GCInfo touches protected memory. Maybe a compaction issue?

We need to reproduce this.

### ha...@chromium.org (2018-05-15)

[Empty comment from Monorail migration]

### ml...@chromium.org (2018-05-15)

[Empty comment from Monorail migration]

[Monorail components: -Blink>JavaScript>GC Blink>MemoryAllocator>GarbageCollection]

### ml...@chromium.org (2018-05-15)

From looking at the stack traces in uaf.log I get the impression that this is a data race on 'g_gc_info_table'. The race results in a UAF of non-Oilpan memory, i.e., regular C++ memory that is used for book-keeping and not the managed heap.

This is a global table that is accessed from multiple threads. GCInfoTable::EnsureGCInfoIndex is concurrency safe when acquiring a new index for a newly visible type. GCInfoTable::Resize is guarded by the same lock.

However, ThreadHeap::GcInfo [1] is left unguarded. Unless I am missing something, the scenario below should yield in the UAF observed.

Scenario:
- Multiple threads (e.g. workers) allocate different objects at the same time.
- Worker 1: GC happens and it uses ThreadHeap::GcInfo() for some access.
- Worker 1: g_gc_info_table is already dereferenced.
- Worker 1: Descheduled by the OS
- Worker 2: Allocates a new type.
- Worker 2: Resizes 'g_gc_info_table' by getting a new memory chunk (as growing doesn't work). The old chunk is invalid.
- Worker 1: Gets scheduled by the OS again and access the old memory chunk which is invalid.

Essentially, all you need is two threads with Oilpan heaps in the same process with lots of different types involved. This likely results in memory corruption and will surely crash when we try to cast to HeapObjectHeader (because of the canary field in release builds).

There are multiple things we can do:
- Use the same mutex for access (maybe costlybut we could try).
- Try to make it thread-local.
- ... (lock-free ds, refcounting, other synchronization protocols)

Also, ThreadHeap::GcInfo should just move to the GcInfo infrastructure, which would make this race obvious.

[1] https://cs.chromium.org/chromium/src/third_party/blink/renderer/platform/heap/heap.h?q=ThreadHeap::GcInfo&g=0&l=372

### hp...@chromium.org (2018-05-15)

Nice mlippautz!

How about reservng the virtual memory for the table upfront. Growing would just add physical pages to the table and it would not move.

### ml...@chromium.org (2018-05-15)

Since the maximum number of types we expect is 1<<14 (16k), we could also just virtually reserve that block and lazily commit the physical memory.

That would allow us to get away without lock during concurrent access.

We could leave the growing logic in place with the difference that it just commits on top of an already reserved virtual block.

### ha...@chromium.org (2018-05-15)

Nice detective work!

+1 to Michael's proposal.


### ml...@chromium.org (2018-05-15)

Will take this one.

### bu...@chromium.org (2018-05-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/20b65d00ca3d8696430e22efad7485366f8c3a21

commit 20b65d00ca3d8696430e22efad7485366f8c3a21
Author: Michael Lippautz <mlippautz@chromium.org>
Date: Tue May 22 00:46:52 2018

[oilpan] Fix GCInfoTable for multiple threads

Previously, grow and access from different threads could lead to a race
on the table backing; see bug.

- Rework the table to work on an existing reservation.
- Commit upon growing, avoiding any copies.

Drive-by: Fix over-allocation of table.

Bug: chromium:841280
Change-Id: I329cb6f40091e14e8c05334ba1104a9440c31d43
Reviewed-on: https://chromium-review.googlesource.com/1061525
Commit-Queue: Michael Lippautz <mlippautz@chromium.org>
Reviewed-by: Kentaro Hara <haraken@chromium.org>
Cr-Commit-Position: refs/heads/master@{#560434}
[modify] https://crrev.com/20b65d00ca3d8696430e22efad7485366f8c3a21/third_party/blink/renderer/platform/heap/BUILD.gn
[modify] https://crrev.com/20b65d00ca3d8696430e22efad7485366f8c3a21/third_party/blink/renderer/platform/heap/gc_info.cc
[modify] https://crrev.com/20b65d00ca3d8696430e22efad7485366f8c3a21/third_party/blink/renderer/platform/heap/gc_info.h
[add] https://crrev.com/20b65d00ca3d8696430e22efad7485366f8c3a21/third_party/blink/renderer/platform/heap/gc_info_test.cc
[modify] https://crrev.com/20b65d00ca3d8696430e22efad7485366f8c3a21/third_party/blink/renderer/platform/heap/heap.cc
[modify] https://crrev.com/20b65d00ca3d8696430e22efad7485366f8c3a21/third_party/blink/renderer/platform/heap/heap.h
[modify] https://crrev.com/20b65d00ca3d8696430e22efad7485366f8c3a21/third_party/blink/renderer/platform/heap/heap_page.cc
[modify] https://crrev.com/20b65d00ca3d8696430e22efad7485366f8c3a21/third_party/blink/renderer/platform/heap/incremental_marking_test.cc
[modify] https://crrev.com/20b65d00ca3d8696430e22efad7485366f8c3a21/third_party/blink/renderer/platform/heap/marking_verifier.h
[modify] https://crrev.com/20b65d00ca3d8696430e22efad7485366f8c3a21/third_party/blink/renderer/platform/heap/marking_visitor.cc
[modify] https://crrev.com/20b65d00ca3d8696430e22efad7485366f8c3a21/third_party/blink/renderer/platform/heap/marking_visitor.h
[modify] https://crrev.com/20b65d00ca3d8696430e22efad7485366f8c3a21/third_party/blink/renderer/platform/heap/process_heap.cc


### ml...@chromium.org (2018-05-22)

IIUC, then depending on timings this could also yield in stability improvements in sweeping and compaction.

### ml...@chromium.org (2018-05-22)

+awhalley for potential bounty: This is a UAF that usually leads to memory corruption. The memory is used as descriptor for GC interaction and an attacker could craft it in a way that the GC executes arbitrary code as a finalizer.

### aw...@google.com (2018-05-22)

Thanks! It'll get picked up once it's marked as fixed. Btw, does this affect stable?

### ml...@chromium.org (2018-05-22)

Yes, this affects stable. Afaics, this should affect everything since Oilpan launch that also involves multiple managed Oilpan heaps, which I think is pretty much anything :/

I will set the status accordingly after some baking time on bots.

### aw...@google.com (2018-05-22)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-05-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/4e481c2a6ff1d20fe135155559301c489316de4f

commit 4e481c2a6ff1d20fe135155559301c489316de4f
Author: Michael Lippautz <mlippautz@chromium.org>
Date: Tue May 22 03:46:19 2018

Revert "[oilpan] Fix GCInfoTable for multiple threads"

This reverts commit 20b65d00ca3d8696430e22efad7485366f8c3a21.

Reason for revert: Crashers, e.g., https://ci.chromium.org/buildbot/chromium.webkit/WebKit%20Mac10.11%20%28dbg%29/16072

Bug: chromium:845380

Original change's description:
> [oilpan] Fix GCInfoTable for multiple threads
> 
> Previously, grow and access from different threads could lead to a race
> on the table backing; see bug.
> 
> - Rework the table to work on an existing reservation.
> - Commit upon growing, avoiding any copies.
> 
> Drive-by: Fix over-allocation of table.
> 
> Bug: chromium:841280
> Change-Id: I329cb6f40091e14e8c05334ba1104a9440c31d43
> Reviewed-on: https://chromium-review.googlesource.com/1061525
> Commit-Queue: Michael Lippautz <mlippautz@chromium.org>
> Reviewed-by: Kentaro Hara <haraken@chromium.org>
> Cr-Commit-Position: refs/heads/master@{#560434}

TBR=ajwong@chromium.org,haraken@chromium.org,hpayer@chromium.org,mlippautz@chromium.org

Change-Id: Idb8b40c02d35810c00ed5a5a9064884b9c154f83
No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Bug: chromium:841280
Reviewed-on: https://chromium-review.googlesource.com/1068568
Reviewed-by: Michael Lippautz <mlippautz@chromium.org>
Commit-Queue: Michael Lippautz <mlippautz@chromium.org>
Cr-Commit-Position: refs/heads/master@{#560476}
[modify] https://crrev.com/4e481c2a6ff1d20fe135155559301c489316de4f/third_party/blink/renderer/platform/heap/BUILD.gn
[modify] https://crrev.com/4e481c2a6ff1d20fe135155559301c489316de4f/third_party/blink/renderer/platform/heap/gc_info.cc
[modify] https://crrev.com/4e481c2a6ff1d20fe135155559301c489316de4f/third_party/blink/renderer/platform/heap/gc_info.h
[delete] https://crrev.com/f10d746929edc6c5afb0d513f5340bf50e1cce4f/third_party/blink/renderer/platform/heap/gc_info_test.cc
[modify] https://crrev.com/4e481c2a6ff1d20fe135155559301c489316de4f/third_party/blink/renderer/platform/heap/heap.cc
[modify] https://crrev.com/4e481c2a6ff1d20fe135155559301c489316de4f/third_party/blink/renderer/platform/heap/heap.h
[modify] https://crrev.com/4e481c2a6ff1d20fe135155559301c489316de4f/third_party/blink/renderer/platform/heap/heap_page.cc
[modify] https://crrev.com/4e481c2a6ff1d20fe135155559301c489316de4f/third_party/blink/renderer/platform/heap/incremental_marking_test.cc
[modify] https://crrev.com/4e481c2a6ff1d20fe135155559301c489316de4f/third_party/blink/renderer/platform/heap/marking_verifier.h
[modify] https://crrev.com/4e481c2a6ff1d20fe135155559301c489316de4f/third_party/blink/renderer/platform/heap/marking_visitor.cc
[modify] https://crrev.com/4e481c2a6ff1d20fe135155559301c489316de4f/third_party/blink/renderer/platform/heap/marking_visitor.h
[modify] https://crrev.com/4e481c2a6ff1d20fe135155559301c489316de4f/third_party/blink/renderer/platform/heap/process_heap.cc


### bu...@chromium.org (2018-05-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/725650ab7df0855c8bc82bfd9b3e27536f943a27

commit 725650ab7df0855c8bc82bfd9b3e27536f943a27
Author: Michael Lippautz <mlippautz@chromium.org>
Date: Tue May 22 09:00:48 2018

Reland "[oilpan] Fix GCInfoTable for multiple threads"

Previously, grow and access from different threads could lead to a race
on the table backing; see bug.

- Rework the table to work on an existing reservation.
- Commit upon growing, avoiding any copies.

Reland:
- Fix an issue for component builds were the singleton was instantiated
  multiple times.

Drive-by: Fix over-allocation of table.
This reverts commit 4e481c2a6ff1d20fe135155559301c489316de4f.

Bug: chromium:841280
Change-Id: Ia89f135b3936162c6f938cb3aef3cfa73f964dd2
Reviewed-on: https://chromium-review.googlesource.com/1068636
Reviewed-by: Kentaro Hara <haraken@chromium.org>
Commit-Queue: Michael Lippautz <mlippautz@chromium.org>
Cr-Commit-Position: refs/heads/master@{#560517}
[modify] https://crrev.com/725650ab7df0855c8bc82bfd9b3e27536f943a27/third_party/blink/renderer/platform/heap/BUILD.gn
[modify] https://crrev.com/725650ab7df0855c8bc82bfd9b3e27536f943a27/third_party/blink/renderer/platform/heap/gc_info.cc
[modify] https://crrev.com/725650ab7df0855c8bc82bfd9b3e27536f943a27/third_party/blink/renderer/platform/heap/gc_info.h
[add] https://crrev.com/725650ab7df0855c8bc82bfd9b3e27536f943a27/third_party/blink/renderer/platform/heap/gc_info_test.cc
[modify] https://crrev.com/725650ab7df0855c8bc82bfd9b3e27536f943a27/third_party/blink/renderer/platform/heap/heap.cc
[modify] https://crrev.com/725650ab7df0855c8bc82bfd9b3e27536f943a27/third_party/blink/renderer/platform/heap/heap.h
[modify] https://crrev.com/725650ab7df0855c8bc82bfd9b3e27536f943a27/third_party/blink/renderer/platform/heap/heap_page.cc
[modify] https://crrev.com/725650ab7df0855c8bc82bfd9b3e27536f943a27/third_party/blink/renderer/platform/heap/incremental_marking_test.cc
[modify] https://crrev.com/725650ab7df0855c8bc82bfd9b3e27536f943a27/third_party/blink/renderer/platform/heap/marking_verifier.h
[modify] https://crrev.com/725650ab7df0855c8bc82bfd9b3e27536f943a27/third_party/blink/renderer/platform/heap/marking_visitor.cc
[modify] https://crrev.com/725650ab7df0855c8bc82bfd9b3e27536f943a27/third_party/blink/renderer/platform/heap/marking_visitor.h
[modify] https://crrev.com/725650ab7df0855c8bc82bfd9b3e27536f943a27/third_party/blink/renderer/platform/heap/process_heap.cc


### sh...@chromium.org (2018-05-22)

[Empty comment from Monorail migration]

### ml...@chromium.org (2018-05-28)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-05-28)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-05-29)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-05-29)

[Empty comment from Monorail migration]

### aw...@google.com (2018-05-30)

+palmer@, interesting bug :-)

### aw...@chromium.org (2018-06-04)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@chromium.org (2018-06-04)

Nice one cdsrc2016@! The VRP panel decided to award $2,000 for this report. Btw, how would you like to be credited in the Chrome release notes?

### aw...@chromium.org (2018-06-04)

[Empty comment from Monorail migration]

### cd...@gmail.com (2018-06-05)

Thanks for the award! Please credit us as
"Zhe Jin（金哲），Luyao Liu(刘路遥) from Chengdu Security Response Center of Qihoo 360 Technology Co. Ltd."

### sh...@chromium.org (2018-06-08)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-06-08)

This bug requires manual review: Reverts referenced in bugdroid comments after merge request.
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), kariahda@(iOS), bhthompson@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ab...@google.com (2018-06-08)

This should already be in branch. Code landed May 22nd, and 68 was branched on May 24th. 

### aw...@google.com (2018-07-23)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-08-28)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-09-03)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2019-01-04)

[Empty comment from Monorail migration]

### va...@chromium.org (2021-09-16)

[Empty comment from Monorail migration]

[Monorail components: -Blink>MemoryAllocator>GarbageCollection Blink>GarbageCollection]

### is...@google.com (2021-09-16)

This issue was migrated from crbug.com/chromium/841280?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091344)*
