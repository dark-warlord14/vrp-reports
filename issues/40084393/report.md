# Security: sfntly font parsing heap-buffer-overflow 

| Field | Value |
|-------|-------|
| **Issue ID** | [40084393](https://issues.chromium.org/issues/40084393) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Fonts, Internals>Skia>PDF |
| **Reporter** | ch...@topsec.com.cn |
| **Assignee** | th...@chromium.org |
| **Created** | 2016-05-26 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

sfntly fonts parsing heap-buffer-overflow or heap-use-after-free

two cases are index overflow.  

date used by memcpy later.

**VERSION**  

latest=git-repo

**REPRODUCTION CASE**

sources:

chromium/src/third\_party/sfntly/src/cpp/src/sfntly/data/growable\_memory\_byte\_array.cc:63  

chromium/src/third\_party/sfntly/src/cpp/src/sfntly/data/memory\_byte\_array.cc:46

two cases are index overflow.  

date used by memcpy later.

can be reproduced with processes like this:  

1.compile.

2.run.  

./bin/subsetter GrowableMemoryByteArray\_InternalGet\_heap\_overflow 1.bin  

./bin/subsetter MemoryByteArray\_InternalGet\_heap\_over\_flow 1.bin

==========================================================================  

<https://code.google.com/p/chromium/codesearch#chromium/src/third_party/sfntly/>

## Attachments

- [GrowableMemoryByteArray_InternalGet_heap_overflow](attachments/GrowableMemoryByteArray_InternalGet_heap_overflow) (text/plain, 72.0 KB)
- [MemoryByteArray_InternalGet_heap_over_flow](attachments/MemoryByteArray_InternalGet_heap_over_flow) (text/plain, 36.5 KB)
- [uaf](attachments/uaf) (text/plain, 72.0 KB)

## Timeline

### me...@chromium.org (2016-05-26)

arthurhsu: Can you please take a look and reassign as appropriate? Thanks.

### ar...@chromium.org (2016-05-26)

Lei can you help?

growable_memory_byte_array are more like C-style things. I did not use STL initially because STL at that time throws exceptions. I don't know if it's okay to use STL now.

If so these shall be handled nicely by STL.



### th...@chromium.org (2016-05-31)

Let me try to figure out how to build the subsetter test binary and take a look.

### cl...@chromium.org (2016-05-31)

[Empty comment from Monorail migration]

### th...@chromium.org (2016-05-31)

GrowableMemoryByteArray_InternalGet_heap_overflow repro'd. ByteVector in third_party/sfntly/src/cpp/src/sfntly/port/type.h is typedef'd to std::vector, so in a Linux debug build, there is bounds checking and the program aborts.

MemoryByteArray_InternalGet_heap_over_flow repro'd with Valgrind and ASAN.

Similarly, uaf repo'd with Valgrind and ASAN.

### me...@chromium.org (2016-05-31)

Adding labels based on https://crbug.com/chromium/614934#c5 (I'm assuming this reproes on stable).

### th...@chromium.org (2016-05-31)

It looks like if we just do the bounds check in ByteArray::Get() and return -1 on error, then all 3 errors stop occurring. Basically:

------
diff --git a/cpp/src/sfntly/data/byte_array.cc b/cpp/src/sfntly/data/byte_array.cc
index 915a40c..57f9eed 100644
--- a/cpp/src/sfntly/data/byte_array.cc
+++ b/cpp/src/sfntly/data/byte_array.cc
@@ -35,6 +35,8 @@ int32_t ByteArray::SetFilledLength(int32_t filled_length) {
 }
 
 int32_t ByteArray::Get(int32_t index) {
+  if (index < 0 || index >= Length())
+    return -1;
   return InternalGet(index) & 0xff;
 }
------

I'll put together a pull request with my GitHub account later today.

### sh...@chromium.org (2016-06-01)

[Empty comment from Monorail migration]

### fe...@chromium.org (2016-06-02)

[Empty comment from Monorail migration]

[Monorail components: Blink>Fonts]

### th...@chromium.org (2016-06-10)

behdad: https://github.com/googlei18n/sfntly/pull/56

### th...@chromium.org (2016-06-11)

Github pull request merged, Chromium DEPS roll is next: https://codereview.chromium.org/2060023003/

I'm not 100% sure if this affects mobile platforms. Just going to mark it OS-All anyway.

meacer: Can you help decide how far back we should merge this? Definitely M-52. How about M-51? This bug has been around for a long time.

### bu...@chromium.org (2016-06-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/e40502b71c9bd4f548118550952afd5d6a158bc4

commit e40502b71c9bd4f548118550952afd5d6a158bc4
Author: thestig <thestig@chromium.org>
Date: Sat Jun 11 04:11:08 2016

Roll DEPS for sfntly to 468cad5.

TBR=behdad@chromium.org
BUG=614934

Review-Url: https://codereview.chromium.org/2060023003
Cr-Commit-Position: refs/heads/master@{#399363}

[modify] https://crrev.com/e40502b71c9bd4f548118550952afd5d6a158bc4/DEPS


### bu...@chromium.org (2016-06-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/e40502b71c9bd4f548118550952afd5d6a158bc4

commit e40502b71c9bd4f548118550952afd5d6a158bc4
Author: thestig <thestig@chromium.org>
Date: Sat Jun 11 04:11:08 2016

Roll DEPS for sfntly to 468cad5.

TBR=behdad@chromium.org
BUG=614934

Review-Url: https://codereview.chromium.org/2060023003
Cr-Commit-Position: refs/heads/master@{#399363}

[modify] https://crrev.com/e40502b71c9bd4f548118550952afd5d6a158bc4/DEPS


### me...@chromium.org (2016-06-15)

thestig: Sorry I missed your comment. Not sure about the merge policy for DEPS rolls to stable channel.

mbarbella: Can you please advise?

### th...@chromium.org (2016-06-15)

FWIW, we use sfntly in Skia when generating PDFs for printing. I don't know if Skia is ever used in the browser process, but if it is, sfntly is at least not in the normal execution path.

### mb...@chromium.org (2016-06-15)

At a glance it looks like there's not much in the roll so I think it would probably be safe in this case. In general we're usually reluctant to merge a roll to a stable branch, though.

+timwillis in case he disagrees, but I think this is probably reasonable for M51. M52 definitely seems fine.

### th...@chromium.org (2016-06-15)

Ya, it's not much of a roll. The other commits in the roll are Java and does not affect us.

### ti...@google.com (2016-06-15)

[Automated comment] DEPS changes referenced in bugdroid comments, needs manual review.

### cl...@chromium.org (2016-06-16)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges.

- Your friendly ClusterFuzz

### sh...@chromium.org (2016-06-16)

[Empty comment from Monorail migration]

### go...@chromium.org (2016-06-17)

Before we approve merge to M52, Could you please confirm whether this change is baked/verified in Canary and safe to merge?


### th...@chromium.org (2016-06-17)

It's a very small change and there hasn't been any reports of printing failures.

### go...@chromium.org (2016-06-20)

Approving merge to M52 branch 2743 based on https://crbug.com/chromium/614934#c22. Please merge ASAP possibly before 5:00 PM PST today so we can take it for this week Beta release. Thank you.

### bu...@chromium.org (2016-06-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/a5694a5ba90056b8323afaab9c4b6b1032f54a72

commit a5694a5ba90056b8323afaab9c4b6b1032f54a72
Author: Lei Zhang <thestig@chromium.org>
Date: Mon Jun 20 17:41:39 2016

M52: Roll DEPS for sfntly to 468cad5.

TBR=behdad@chromium.org
BUG=614934

Review-Url: https://codereview.chromium.org/2060023003
Cr-Commit-Position: refs/heads/master@{#399363}
(cherry picked from commit e40502b71c9bd4f548118550952afd5d6a158bc4)

Review URL: https://codereview.chromium.org/2082643003 .

Cr-Commit-Position: refs/branch-heads/2743@{#405}
Cr-Branched-From: 2b3ae3b8090361f8af5a611712fc1a5ab2de53cb-refs/heads/master@{#394939}

[modify] https://crrev.com/a5694a5ba90056b8323afaab9c4b6b1032f54a72/DEPS


### aw...@chromium.org (2016-07-14)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-07-19)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-07-25)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-07-25)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-07-25)

Congratulations! The panel has awarded $500 for this bug.  A member of our finance team will be in touch in the next few weeks.

### aw...@chromium.org (2016-07-25)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-08-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-09-22)

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

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### th...@chromium.org (2018-09-05)

[Empty comment from Monorail migration]

[Monorail components: Internals>Skia>PDF]

### is...@google.com (2018-09-05)

This issue was migrated from crbug.com/chromium/614934?no_tracker_redirect=1

[Multiple monorail components: Blink>Fonts, Internals>Skia>PDF]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084393)*
