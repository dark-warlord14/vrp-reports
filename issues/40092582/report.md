# heap buffer overflow in skia::SkTDPQueue::insert

| Field | Value |
|-------|-------|
| **Issue ID** | [40092582](https://issues.chromium.org/issues/40092582) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Canvas, Internals>Skia |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | cd...@gmail.com |
| **Assignee** | fs...@chromium.org |
| **Created** | 2018-09-29 |
| **Bounty** | $3,000.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36

Steps to reproduce the problem:
1. download and unzip the release asan chromium :asan-linux-release-593799
2. Run ./chrome crash.html

What is the expected behavior?

What went wrong?
heap buffer overflow in skia::SkTDPQueue::insert

1. download and unzip the release asan chromium :asan-linux-release-593799
2. Run ./chrome poc/crash.html

Could get 3 kinds of crash:oom ,UAF and double free.

The skia's SkTDPQueue seems not to be thread safe.

in src/third_party/skia/src/core/SkTDPQueue.h:
    void insert(T entry) {                       <----if two threads call into here together
        this->validate();
        int index = fArray.count();
        *fArray.append() = entry;                <----A
        this->setIndex(fArray.count() - 1);
        this->percolateUpIfNecessary(index);
        this->validate();
    }
The append() is not protected.So when two threads came into here ,could cause series of problems.One of the problems could be like this(code line marked A and B) :

in third_party/skia/include/private/SkTDArray.h:
    void resizeStorageToAtLeast(int count) {
        SkASSERT(count > fReserve);
        ...
        fReserve = SkTo<int>(reserve);
        fArray = (T*)sk_realloc_throw(fArray, fReserve * sizeof(T));  <----B                                                                                                                              
    }

1: If one thread comes to code line B while another thread is writing some data using old fArray pointer(see code line A),out of bounds write(or heap buffer overflow) happened.Stacktrace of this situation sees in log/oom.log
2: If two threads both come code line B,double free happened.Stacktrace of this situation sees log/double_free.log

To trigger this bug,i tried to let a worker connect with main thread using api about WebGraphicsContext3D.Sees in poc/crash.html

I also got situation 3 in this way.Perhaps they all cause by the unsafe operation through different threads?Or they should belong to two different issue?

3: in src/third_party/skia/src/gpu/GrResourceCache.cpp:
    while(fNonpurgeableResources.count()) {
        GrGpuResource* back = *(fNonpurgeableResources.end() - 1);
        SkASSERT(!back->wasDestroyed());
        back->cacheAccess().release();     <----C
    }
If other unsafe operation makes the SkTDArray holds two same pointer,the "back" pointer could be used after deleted at code line C.Stacktrace of this situation sees in log/UAF.log.

I tried a mitigation patch.Situation 1 and 2 sees in patch/patch1.diff situation 3 sees in patch/patch2.diff.Hope my work helps.

Did this work before? N/A 

Chrome version: 71.0.3561.0  Channel: n/a
OS Version: 16.04
Flash Version:

## Attachments

- deleted (application/octet-stream, 0 B)

## Timeline

### cd...@gmail.com (2018-09-29)

If can not repro,please change the timeout at crash.html:52 to make it more stable to repro and get different kind of crash.

### do...@chromium.org (2018-09-30)

Thanks for the report. +skia folks for triage.

[Monorail components: Internals>Skia]

### [Deleted User] (2018-10-01)

I don't think any of these data structures are meant to be thread safe.  This seems like Chromium's somehow breaking Skia's expectations about using Ganesh in multiple threads.

### bs...@google.com (2018-10-01)

From looking over mtklein@'s shoulder it seems offscreen canvas causes a texture-backed SkImage created by GrContext on one thread to be unreffed on another thread. This is not currently allowed. The destructor accesses manipulates non-atomic ref cnts and accesses GrResourceCache which is designed to be thread safe.

### do...@chromium.org (2018-10-01)

Thanks for investigating - canvas folks, can you follow up on this non-thread-safe use of SkImage?

[Monorail components: Blink>Canvas]

### fs...@chromium.org (2018-10-02)

[Empty comment from Monorail migration]

### me...@chromium.org (2018-10-03)

Adjusting labels.

### sh...@chromium.org (2018-10-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-10-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-10-14)

davidqu: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### fs...@chromium.org (2018-10-15)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-10-17)

[Empty comment from Monorail migration]

### fs...@chromium.org (2018-10-30)

Ahn! Found the fix! :)
Patch on its way.

### fs...@chromium.org (2018-10-30)

https://chromium-review.googlesource.com/c/chromium/src/+/1307775

### pa...@chromium.org (2018-10-30)

Security team thanks you, fserb! :)

### fs...@chromium.org (2018-10-31)

cc'ing folks on my CL so they can have context.

### bu...@chromium.org (2018-10-31)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/78d89fe556cb5dabbc47b4967cdf55e607e29580

commit 78d89fe556cb5dabbc47b4967cdf55e607e29580
Author: Fernando Serboncini <fserb@chromium.org>
Date: Wed Oct 31 22:25:41 2018

Fix *StaticBitmapImage ThreadChecker and unaccelerated SkImage destroy

- AcceleratedStaticBitmapImage was misusing ThreadChecker by having its
own detach logic. Using proper DetachThread is simpler, cleaner and
correct.
- UnacceleratedStaticBitmapImage didn't destroy the SkImage in the
proper thread, leading to GrContext/SkSp problems.

Bug: 890576
Change-Id: Ic71e7f7322b0b851774628247aa5256664bc0723
Reviewed-on: https://chromium-review.googlesource.com/c/1307775
Reviewed-by: Gabriel Charette <gab@chromium.org>
Reviewed-by: Jeremy Roman <jbroman@chromium.org>
Commit-Queue: Fernando Serboncini <fserb@chromium.org>
Cr-Commit-Position: refs/heads/master@{#604427}
[modify] https://crrev.com/78d89fe556cb5dabbc47b4967cdf55e607e29580/third_party/blink/renderer/platform/graphics/accelerated_static_bitmap_image.cc
[modify] https://crrev.com/78d89fe556cb5dabbc47b4967cdf55e607e29580/third_party/blink/renderer/platform/graphics/accelerated_static_bitmap_image.h
[modify] https://crrev.com/78d89fe556cb5dabbc47b4967cdf55e607e29580/third_party/blink/renderer/platform/graphics/unaccelerated_static_bitmap_image.cc
[modify] https://crrev.com/78d89fe556cb5dabbc47b4967cdf55e607e29580/third_party/blink/renderer/platform/graphics/unaccelerated_static_bitmap_image.h


### fs...@chromium.org (2018-11-01)

We did it, folks! :)
(does restrict-view get automatically dropped after a while?)

### jb...@chromium.org (2018-11-01)

Yes, sheriffbot will come by and make it public in 14 weeks.

### sh...@chromium.org (2018-11-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-11-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-11-04)

This bug requires manual review: M71 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: benmason@(Android), kariahda@(iOS), kbleicher@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2018-11-05)

+ awhalley@ (Security TPM) for M71 merge review. Thank you.

### aw...@chromium.org (2018-11-05)

[Empty comment from Monorail migration]

### aw...@google.com (2018-11-05)

govind@ - good for M71

### go...@chromium.org (2018-11-05)

Approving merge to M71 branch 3578 based on https://crbug.com/chromium/890576#c25. Pls merge ASAP. Thank you.

### fs...@chromium.org (2018-11-05)

Done.

### bu...@chromium.org (2018-11-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/1d98e2c78a40847353dffb23b765e83620e9c51a

commit 1d98e2c78a40847353dffb23b765e83620e9c51a
Author: Fernando Serboncini <fserb@chromium.org>
Date: Mon Nov 05 17:40:12 2018

Fix *StaticBitmapImage ThreadChecker and unaccelerated SkImage destroy

- AcceleratedStaticBitmapImage was misusing ThreadChecker by having its
own detach logic. Using proper DetachThread is simpler, cleaner and
correct.
- UnacceleratedStaticBitmapImage didn't destroy the SkImage in the
proper thread, leading to GrContext/SkSp problems.

Bug: 890576
Change-Id: Ic71e7f7322b0b851774628247aa5256664bc0723
Reviewed-on: https://chromium-review.googlesource.com/c/1307775
Reviewed-by: Gabriel Charette <gab@chromium.org>
Reviewed-by: Jeremy Roman <jbroman@chromium.org>
Commit-Queue: Fernando Serboncini <fserb@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#604427}(cherry picked from commit 78d89fe556cb5dabbc47b4967cdf55e607e29580)
Reviewed-on: https://chromium-review.googlesource.com/c/1318175
Reviewed-by: Fernando Serboncini <fserb@chromium.org>
Cr-Commit-Position: refs/branch-heads/3578@{#500}
Cr-Branched-From: 4226ddf99103e493d7afb23a4c7902ee496108b6-refs/heads/master@{#599034}
[modify] https://crrev.com/1d98e2c78a40847353dffb23b765e83620e9c51a/third_party/blink/renderer/platform/graphics/accelerated_static_bitmap_image.cc
[modify] https://crrev.com/1d98e2c78a40847353dffb23b765e83620e9c51a/third_party/blink/renderer/platform/graphics/accelerated_static_bitmap_image.h
[modify] https://crrev.com/1d98e2c78a40847353dffb23b765e83620e9c51a/third_party/blink/renderer/platform/graphics/unaccelerated_static_bitmap_image.cc
[modify] https://crrev.com/1d98e2c78a40847353dffb23b765e83620e9c51a/third_party/blink/renderer/platform/graphics/unaccelerated_static_bitmap_image.h


### cr...@appspot.gserviceaccount.com (2018-11-05)

The following revision refers to this bug: 
https://chromium.googlesource.com/chromium/src.git/+/1d98e2c78a40847353dffb23b765e83620e9c51a

Commit: 1d98e2c78a40847353dffb23b765e83620e9c51a
Author: fserb@chromium.org
Commiter: fserb@chromium.org
Date: 2018-11-05 17:40:12 +0000 UTC

Fix *StaticBitmapImage ThreadChecker and unaccelerated SkImage destroy

- AcceleratedStaticBitmapImage was misusing ThreadChecker by having its
own detach logic. Using proper DetachThread is simpler, cleaner and
correct.
- UnacceleratedStaticBitmapImage didn't destroy the SkImage in the
proper thread, leading to GrContext/SkSp problems.

Bug: 890576
Change-Id: Ic71e7f7322b0b851774628247aa5256664bc0723
Reviewed-on: https://chromium-review.googlesource.com/c/1307775
Reviewed-by: Gabriel Charette <gab@chromium.org>
Reviewed-by: Jeremy Roman <jbroman@chromium.org>
Commit-Queue: Fernando Serboncini <fserb@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#604427}(cherry picked from commit 78d89fe556cb5dabbc47b4967cdf55e607e29580)
Reviewed-on: https://chromium-review.googlesource.com/c/1318175
Reviewed-by: Fernando Serboncini <fserb@chromium.org>
Cr-Commit-Position: refs/branch-heads/3578@{#500}
Cr-Branched-From: 4226ddf99103e493d7afb23a4c7902ee496108b6-refs/heads/master@{#599034}

### aw...@chromium.org (2018-11-12)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-11-12)

Hi cdsrc2016@, $3,000 for this report from the Chrome VRP panel, thanks!

### aw...@google.com (2018-11-12)

[Empty comment from Monorail migration]

### cd...@gmail.com (2018-11-12)

Thanks very much for the reward :)

### aw...@google.com (2018-12-03)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-12-11)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-12-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-02-08)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/890576?no_tracker_redirect=1

[Multiple monorail components: Blink>Canvas, Internals>Skia]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092582)*
