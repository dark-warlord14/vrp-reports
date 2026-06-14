# Use-of-uninitialized-value in S32A_Opaque_BlitRow32_SSE4

| Field | Value |
|-------|-------|
| **Issue ID** | [40083487](https://issues.chromium.org/issues/40083487) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Skia |
| **Platforms** | Linux |
| **Reporter** | at...@gmail.com |
| **Assignee** | re...@google.com |
| **Created** | 2016-01-04 |
| **Bounty** | $1,000.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6133678582792192

Fuzzer: attekett_surku_fuzzer
Job Type: linux_msan_chrome
Platform Id: linux

Crash Type: Use-of-uninitialized-value
Crash Address: 
Crash State:
  S32A_Opaque_BlitRow32_SSE4
  SkARGB32_Shader_Blitter::blitAntiH
  SkRectClipBlitter::blitAntiH
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_msan_chrome&range=361453:361496

Minimized Testcase (0.47 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94T_y64Qvmz3NHGlcuSMhdvuoWcSTVt3goM9V3Jzn1exeJuDYj9GdxE6QnWebnSVMYO4nT_N2lAjPEnv2r1cWadaqt9smAb-v5T6k8cmy9o9mVZWo-JTAY_mDFN9TsZtaQ1wKAqFNbngWbZzka9WBf4bq6ElA

Filer: aarya

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

## Timeline

### in...@chromium.org (2016-01-04)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-01-04)

[Empty comment from Monorail migration]

### mb...@chromium.org (2016-01-04)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-01-04)

This medium+ severity security issue is a regression on trunk.

Please fix this asap. If you are unable to look into this soon, please revert your change.

- Your friendly ClusterFuzz

### cl...@chromium.org (2016-01-15)

[Empty comment from Monorail migration]

### go...@chromium.org (2016-01-25)

Any update on this bug? 
FYI:
We're having M9 Beta candidate cut on Wednesday @ 5:00 PM PST and release on Thursday [01/28].

### cl...@chromium.org (2016-01-26)

reed@: Uh oh! This issue is still open and hasn't been updated in the last 21 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### [Deleted User] (2016-01-26)

mike, any insights into *what* might be uninitialized in this SSE code?

### cl...@chromium.org (2016-01-26)

[Empty comment from Monorail migration]

### [Deleted User] (2016-01-26)

Yes, the source bitmap, or at least its alpha components.

The use-of-uninitialized-value is triggering when we call _mm_testz_si128 (ptest) on the alphas of 16 source pixels.  We use ptest to branch this function 3 ways for each 16-pixel chunk, all based on source alpha:
  - all 0x00 ---> no-op  (i.e. degrade to Dst)
  - all 0xFF ---> copy 16 src pixels directly to dst  (i.e. degrade to Src)
  - else ---> really do the full-power SrcOver math for 16 pixel pairs

Usually it is a bug to SrcOver an uninitialized source.  (In contrast, it may not be a bug to have an unintialized dst.)  But that bug is logical bug, much higher-level than anything to do with this code.

This warning is a false positive as far as correctness and security go.  There's certainly no risk of crash or any misbehavior.  This function behaves completely sensibly with uninitialized inputs.  We'd see this sort of thing more often, but this is the only blit where we've found it profitable to branch based on pixel values inside its tight loop.  The other blits are just branch-free garbage-in, garbage-out.

We could "fix" this by writing a slower version of the code that just replaces the if (_mm_test...) lines with if (false), forcing the code to always go through the branch-free general case.

(The SSE2 version of this code is analogous, using movemask instead of ptest.)

### ss...@google.com (2016-01-27)

Thanks mtklein@ for the explanation. It sounds from the comment like this shouldn't impact beta release. Could you guys please remove the ReleaseBlock-Beta label if you agree?

### [Deleted User] (2016-01-27)

[Empty comment from Monorail migration]

### kc...@chromium.org (2016-01-27)

>> false positive as far as correctness and security go
Is there a chance that uninitialized bits will show up on a screen? 
If yes, here is a fun reading: 
http://googleprojectzero.blogspot.com/2014/08/what-does-pointer-look-like-anyway.html

### [Deleted User] (2016-01-27)

Yes, of course the uninitialized bits will show up on a screen.

But the bug is not here.  It's where the source bitmap was not initialized before calling this method.

### cl...@chromium.org (2016-01-30)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5651772514762752

Fuzzer: inferno_twister
Job Type: linux_msan_chrome
Platform Id: linux

Crash Type: Use-of-uninitialized-value
Crash Address: 
Crash State:
  S32A_Opaque_BlitRow32_SSE4
  SkARGB32_Shader_Blitter::blitAntiH
  SkRgnClipBlitter::blitAntiH
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_msan_chrome&range=361453:361496

Minimized Testcase (20.08 Kb): https://cluster-fuzz.appspot.com/download/AMIfv948wlBgN1GrRnxcSMkSdQ2OQUgEO8joOArbduMED0hvbyUQsLvRKqypXwVxUwRU3C_R9hkim8D-gGXjpwlcl1H8MZ1BPCJcgZ3BEBNIlkRuOmMsFjifYrUYsIVjpvI6Q7JSVZ3odPW18tgg3NswcmmgN5JRJxrj8GLErrFNOzf2EnmcqIU

Filer: inferno

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

### [Deleted User] (2016-02-01)

Is there a way to mark this function (and S32A_Opaque_BlitRow32_SSE2) to be ignored by MSAN?

### in...@chromium.org (2016-02-01)

You can use this http://clang.llvm.org/docs/MemorySanitizer.html#attribute-no-sanitize-memory to mark the function.

### kc...@chromium.org (2016-02-01)

[Empty comment from Monorail migration]

### eu...@google.com (2016-02-02)

If you ignore this function, we will miss all future bugs when an uninitialized image is passed to the blitter. Better fix this bug at the source.


### [Deleted User] (2016-02-02)

That sounds fine to me, but note we'll also miss future bugs when an uninitialized image is passed to any other blitter (they are many and varied), or if we find a faster way to implement this function that doesn't involve branching.  I'm not sure I'd keep this code branchy just to root out bugs somewhere else in Chrome.

What do we do about this bug?  Close it and keep closing it while a bot keeps reopening it?

### eu...@google.com (2016-02-02)

We should figure out why the input bitmap is uninitialized and fix that.

If there is no branching, MSan will propagate uninitialized values, marking some of the output bytes as uninitialized. The problem will be reported when these are eventually used.

If it's OK to require that the source bitmap is always initialized in this function, we can add an assert for that:
#ifdef MEMORY_SANITIZER
__msan_check_mem_is_initialized(ptr, size);
#endif
it's in <sanitizer/msan_interface.h>
This will produce a very similar report, but it would be clear that the bug is not in this function.



### [Deleted User] (2016-02-02)

Oooh, lovely.  It's definitely a bug to call this function with an uninitialized source.  __msan_check_mem_is_intialized() sounds like the right answer.  

### bu...@chromium.org (2016-02-03)

The following revision refers to this bug:
  https://skia.googlesource.com/skia.git/+/1059b1fc9f8711592a81836512850d123d75146d

commit 1059b1fc9f8711592a81836512850d123d75146d
Author: mtklein <mtklein@chromium.org>
Date: Wed Feb 03 15:25:02 2016

Add SkMSAN.h

This lets us tag up pieces of code as requiring initialized inputs.

Almost all code requires initialized inputs, of course.  This is for
code that works correctly with uninitialized data but triggers false
positive warnings in MSAN.  E.g., imagine MSAN's found use of uninitialized
data in this max function:

  static uint8_t max(uint8_t x, uint8_t y) { return x > y ? x : y; }

There's no bug in here... if there's uninitialized data being branched upon
here for the first time, it's sure not max's fault, it's its caller's fault.

So we might do this:
  static uint8_t max(uint8_t x, uint8_t y) {
      // This function uses branching, so if MSAN finds a problem here,
      // we can assert x and y are initialized.  This will remind us the
      // problem somewhere in the caller or above, not here.
      sk_msan_assert_initialized(&x, &x+1);
      sk_masn_assert_initialized(&y, &y+1);
      return x > y ? x : y;
  }

By allowing code to assert its inputs must be initialized,
we can make the blame for use of uninitialized data more clear.

(Sometimes we have another option, to rewrite the code to avoid branching:
  static uint8_t max(uint8_t x, uint8_t y) {
      // This function is branchfree, so MSAN won't complain here.
      // No real need to assert anything as requiring initialization.
      int diff = x - y;
      int negative = diff >> (sizeof(int)*8 - 1);
      return (y & negative) | (x & ~negative);
  }
These approaches to fixing MSAN false positives are orthogonal.)

BUG=chromium:574114
GOLD_TRYBOT_URL= https://gold.skia.org/search2?unt=true&query=source_type%3Dgm&master=false&issue=1658913005
CQ_EXTRA_TRYBOTS=client.skia:Test-Ubuntu-GCC-GCE-CPU-AVX2-x86_64-Release-SKNX_NO_SIMD-Trybot

Review URL: https://codereview.chromium.org/1658913005

[add] http://crrev.com/1059b1fc9f8711592a81836512850d123d75146d/src/core/SkMSAN.h
[modify] http://crrev.com/1059b1fc9f8711592a81836512850d123d75146d/src/opts/SkBlitRow_opts_SSE2.cpp
[modify] http://crrev.com/1059b1fc9f8711592a81836512850d123d75146d/src/opts/SkBlitRow_opts_SSE4.cpp


### cl...@chromium.org (2016-02-13)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4855540695433216

Fuzzer: noel-image-surku
Job Type: linux_msan_chrome
Platform Id: linux

Crash Type: Use-of-uninitialized-value
Crash Address: 
Crash State:
  S32A_Opaque_BlitRow32_SSE4
  SkARGB32_Shader_Blitter::blitRect
  antifilldot8
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_msan_chrome&range=370165:370712

Minimized Testcase (0.83 Kb): https://cluster-fuzz.appspot.com/download/AMIfv97BiweXVUQsSA5bjUvXGy2nGdztNsK7p90malX5LaqhH0w8fIJQpxRxePO8SZQBLCGojvw8VZW_04SZkl9XhQcNuE4kAewbtMwXlaHisP7Rqi705nHOs270_9RL_rsDio5xnutNjy1gpv9--QMbEtBkNIz2bA

Filer: inferno

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

### cl...@chromium.org (2016-02-13)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4855540695433216

Fuzzer: noel-image-surku
Job Type: linux_msan_chrome
Platform Id: linux

Crash Type: Use-of-uninitialized-value
Crash Address: 
Crash State:
  S32A_Opaque_BlitRow32_SSE4
  SkARGB32_Shader_Blitter::blitRect
  antifilldot8
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_msan_chrome&range=370165:370712

Minimized Testcase (0.83 Kb): https://cluster-fuzz.appspot.com/download/AMIfv97BiweXVUQsSA5bjUvXGy2nGdztNsK7p90malX5LaqhH0w8fIJQpxRxePO8SZQBLCGojvw8VZW_04SZkl9XhQcNuE4kAewbtMwXlaHisP7Rqi705nHOs270_9RL_rsDio5xnutNjy1gpv9--QMbEtBkNIz2bA

Filer: inferno

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

### cl...@chromium.org (2016-02-13)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4855540695433216

Fuzzer: noel-image-surku
Job Type: linux_msan_chrome
Platform Id: linux

Crash Type: Use-of-uninitialized-value
Crash Address: 
Crash State:
  S32A_Opaque_BlitRow32_SSE4
  SkARGB32_Shader_Blitter::blitRect
  antifilldot8
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_msan_chrome&range=370165:370712

Minimized Testcase (0.83 Kb): https://cluster-fuzz.appspot.com/download/AMIfv97BiweXVUQsSA5bjUvXGy2nGdztNsK7p90malX5LaqhH0w8fIJQpxRxePO8SZQBLCGojvw8VZW_04SZkl9XhQcNuE4kAewbtMwXlaHisP7Rqi705nHOs270_9RL_rsDio5xnutNjy1gpv9--QMbEtBkNIz2bA

Filer: inferno

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

### cl...@chromium.org (2016-02-17)

ClusterFuzz has detected this issue as fixed in range 372730:375259.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4855540695433216

Fuzzer: noel-image-surku
Job Type: linux_msan_chrome
Platform Id: linux

Crash Type: Use-of-uninitialized-value
Crash Address: 
Crash State:
  S32A_Opaque_BlitRow32_SSE4
  SkARGB32_Shader_Blitter::blitRect
  antifilldot8
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_msan_chrome&range=370165:370712
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_msan_chrome&range=372730:375259

Minimized Testcase (0.83 Kb): https://cluster-fuzz.appspot.com/download/AMIfv97BiweXVUQsSA5bjUvXGy2nGdztNsK7p90malX5LaqhH0w8fIJQpxRxePO8SZQBLCGojvw8VZW_04SZkl9XhQcNuE4kAewbtMwXlaHisP7Rqi705nHOs270_9RL_rsDio5xnutNjy1gpv9--QMbEtBkNIz2bA

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### ra...@chromium.org (2016-02-18)

mtklein: can this be marked as fixed now, based on the CL in #23 or is there more to do? Thanks!

### [Deleted User] (2016-02-18)

Sure!  

(Nothing to backport here.)

### cl...@chromium.org (2016-02-18)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### [Deleted User] (2016-02-18)

Nothing to merge here.

### sh...@chromium.org (2016-05-27)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cl...@chromium.org (2016-06-09)

ClusterFuzz has detected this issue as fixed in range 396253:396347.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5651772514762752

Fuzzer: inferno_twister
Job Type: linux_msan_chrome
Platform Id: linux

Crash Type: Use-of-uninitialized-value
Crash Address: 
Crash State:
  S32A_Opaque_BlitRow32_SSE4
  SkARGB32_Shader_Blitter::blitAntiH
  SkRgnClipBlitter::blitAntiH
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_msan_chrome&range=361453:361496
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_msan_chrome&range=396253:396347

Minimized Testcase (20.08 Kb): https://cluster-fuzz.appspot.com/download/AMIfv97dUTIRWloCZOYpWe15qoq9cwgk5bL4uBV46LggOrK2TO80DDxNPe96WRZz-vKDg6Qs7OW1ZwjtpgICARNxDnVTCUcaP7f1nE_V8g8GNXftWttibo0BfZNjrjoF7ksVqm5Wzxza1PhUSRAI4KDNZhF4-GPoqwthnf9iWPqIi7L_vVnj5yQ

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### ti...@google.com (2016-06-30)

Atte - $1,500 for this report ($1,000 for the report, $500 for the fuzzer). w00t.

### aw...@chromium.org (2016-06-30)

[Comment Deleted]

### aw...@chromium.org (2016-06-30)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-07-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/574114?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083487)*
