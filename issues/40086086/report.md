# Heap-buffer-overflow in table_r

| Field | Value |
|-------|-------|
| **Issue ID** | [40086086](https://issues.chromium.org/issues/40086086) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Internals>Skia |
| **Platforms** | Linux |
| **Reporter** | cl...@chromium.org |
| **Assignee** | ms...@chromium.org |
| **Created** | 2016-11-26 |
| **Bounty** | $1,500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5259923043909632

Fuzzer: attekett_surku_fuzzer
Job Type: linux_asan_chrome_chromeos
Platform Id: linux

Crash Type: Heap-buffer-overflow READ 4
Crash Address: 0x6190000405c8
Crash State:
  table_r
  color_lookup_table
  std::_Function_handler<void
  
Recommended Security Severity: Medium

Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_chromeos&range=434178:434216

Minimized Testcase (50.66 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95ChVwsDW6th6r3HE4-UkG9f02Diw8dwYkrD-CX1wCzb7pXJoWcJoZngFDprQW_N2dtIWSXwdLwD529gYVzl9euufrVyShuqVEJTxfh3GCu8XgXm3C_jE3MF27_fSoVp8WmDyHeai0ItYP-3o6M4glOOi3CsSAgWL6baK_KvpXzQpDmmkk?testcase_id=5259923043909632

Issue filed automatically.

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

## Timeline

### sh...@chromium.org (2016-11-26)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-11-26)

This issue is a security regression. If you are not able to fix this quickly, please revert the change that introduced it.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-11-26)

[Empty comment from Monorail migration]

### do...@chromium.org (2016-11-26)

Howdy folks, this is another overflow that ClusterFuzz found in Skia. Do you mind taking a look?

[Monorail components: Internals>Skia]

### bu...@chromium.org (2016-11-28)

The following revision refers to this bug:
  https://skia.googlesource.com/skia.git/+/264431d9e2c4021baa2a5357b0c8c7773384d614

commit 264431d9e2c4021baa2a5357b0c8c7773384d614
Author: raftias <raftias@google.com>
Date: Mon Nov 28 16:30:18 2016

Fuzzer fix for overflow in some Lut8 profiles.

Bug(?) in the tetrahedral interpolation causes output values to go out
of range a bit (1.035/1.0) in the upper range. We will just clamp for
now as a temporary fix.

BUG=668784

Change-Id: I78dd90da7174133e647b1c6c6e914dbde5de123c
Reviewed-on: https://skia-review.googlesource.com/5228
Reviewed-by: Matt Sarett <msarett@google.com>
Commit-Queue: Robert Aftias <raftias@google.com>

[modify] https://crrev.com/264431d9e2c4021baa2a5357b0c8c7773384d614/src/core/SkColorLookUpTable.cpp


### bu...@chromium.org (2016-11-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/b4ee4bffa0c144adfb16968ca3645bc624e938db

commit b4ee4bffa0c144adfb16968ca3645bc624e938db
Author: skia-deps-roller <skia-deps-roller@chromium.org>
Date: Tue Nov 29 04:21:16 2016

Roll src/third_party/skia/ d5de01364..99ab92b59 (22 commits).

https://skia.googlesource.com/skia.git/+log/d5de01364378..99ab92b5958a

$ git log d5de01364..99ab92b59 --date=short --no-merges --format='%ad %ae %s'
2016-11-28 raftias Moved A2B0 profile parsing before XYZ
2016-11-28 mtklein Consistent naming.
2016-11-28 reed use raster-pipeline in readPixels
2016-11-28 ethannicholas added support for layout(offset=...) to skslc
2016-11-28 benjaminwagner Merge changes from internal cl/140385880.
2016-11-28 mtklein simplify
2016-11-28 liyuqian Revert "Add the missing shift to the dy"
2016-11-28 mtklein Convert blitter over to new style from_srgb, to_srgb.
2016-11-28 lsalzman use __BYTE_ORDER__ macro to detect endianness when available
2016-11-28 brianosman Narrow the SkImageGenerator interface
2016-11-28 bsalomon Remove old driver bug workaround for glTexStorage.
2016-11-28 borenet Roll recipe DEPS
2016-11-28 ethannicholas unified ASTLayout/Layout and ASTModifiers/Modifiers
2016-11-28 ethannicholas removed textureProj() and legacy texture functions from sksl
2016-11-28 reed simplify SkConfig8888 logic: just fall-through if memcpy case isn't supported
2016-11-28 mtklein Split srgb out of accum stages.
2016-11-28 raftias Fuzzer fix for overflow in some Lut8 profiles.
2016-11-28 mtklein Fix unpremul stage.
2016-11-28 liyuqian Add the missing shift to the dy
2016-11-28 brianosman GrTextureProducer cleanup, phase two: Producer, Adjuster, Maker
2016-11-22 mtklein Guard against buggy ucrt\math.h.
2016-11-22 ethannicholas baked in a few more precision modifiers

BUG=668784,668907,666707

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, see:
http://www.chromium.org/developers/tree-sheriffs/sheriff-details-chromium#TOC-Failures-due-to-DEPS-rolls

CQ_INCLUDE_TRYBOTS=master.tryserver.blink:linux_trusty_blink_rel
TBR=brianosman@google.com

Review-Url: https://codereview.chromium.org/2532083003
Cr-Commit-Position: refs/heads/master@{#434889}

[modify] https://crrev.com/b4ee4bffa0c144adfb16968ca3645bc624e938db/DEPS


### ms...@chromium.org (2016-11-29)

Did Rob's fix make it into M56 or does it need to be cherry-picked?

### bu...@chromium.org (2016-11-29)

The following revision refers to this bug:
  https://skia.googlesource.com/skia.git/+/82589494dacdc3eb562a328daa28dd2655edb787

commit 82589494dacdc3eb562a328daa28dd2655edb787
Author: msarett <msarett@google.com>
Date: Tue Nov 29 21:22:01 2016

Fuzzer fix for overflow in some Lut8 profiles.

Bug(?) in the tetrahedral interpolation causes output values to go out
of range a bit (1.035/1.0) in the upper range. We will just clamp for
now as a temporary fix.

BUG=668784

Change-Id: I78dd90da7174133e647b1c6c6e914dbde5de123c
Reviewed-on: https://skia-review.googlesource.com/5228
Reviewed-by: Matt Sarett <msarett@google.com>
Commit-Queue: Robert Aftias <raftias@google.com>
GOLD_TRYBOT_URL= https://gold.skia.org/search?issue=2535383002
NOTREECHECKS=true
NOTRY=true
NOPRESUBMIT=true

Review-Url: https://codereview.chromium.org/2535383002

[modify] https://crrev.com/82589494dacdc3eb562a328daa28dd2655edb787/src/core/SkColorLookUpTable.cpp


### ms...@chromium.org (2016-11-29)

Cherry-picked the fix into M56.  Expecting the fuzzer to detect the fix.

### bu...@chromium.org (2016-11-29)

The following revision refers to this bug:
  https://skia.googlesource.com/skia.git/+/922e5be6e2494e46656ab3614c5395c6ff035a73

commit 922e5be6e2494e46656ab3614c5395c6ff035a73
Author: Matt Sarett <msarett@google.com>
Date: Tue Nov 29 15:14:03 2016

Fixes for SkColorLookUpTable::interp3D

(1) Fix subtle comparison bug so we interpolate the proper tetrahedral.
(2) Add new comments - the clamp is necessary.
(3) SkCSXformPrintf requires an extra friend class to compile.

BUG:668784

Change-Id: Id1a5c561f23ccfe25e141b8490cddee4c2482326
Reviewed-on: https://skia-review.googlesource.com/5238
Reviewed-by: Robert Aftias <raftias@google.com>
Commit-Queue: Matt Sarett <msarett@google.com>

[modify] https://crrev.com/922e5be6e2494e46656ab3614c5395c6ff035a73/infra/bots/assets/skimage/VERSION
[modify] https://crrev.com/922e5be6e2494e46656ab3614c5395c6ff035a73/infra/bots/tasks.json
[modify] https://crrev.com/922e5be6e2494e46656ab3614c5395c6ff035a73/src/core/SkColorLookUpTable.cpp
[modify] https://crrev.com/922e5be6e2494e46656ab3614c5395c6ff035a73/src/core/SkColorLookUpTable.h


### cl...@chromium.org (2016-11-30)

ClusterFuzz has detected this issue as fixed in range 434840:434922.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5259923043909632

Fuzzer: attekett_surku_fuzzer
Job Type: linux_asan_chrome_chromeos
Platform Id: linux

Crash Type: Heap-buffer-overflow READ 4
Crash Address: 0x6190000405c8
Crash State:
  table_r
  color_lookup_table
  std::_Function_handler<void
  
Recommended Security Severity: Medium

Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_chromeos&range=434178:434216
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_chromeos&range=434840:434922

Minimized Testcase (50.66 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95ChVwsDW6th6r3HE4-UkG9f02Diw8dwYkrD-CX1wCzb7pXJoWcJoZngFDprQW_N2dtIWSXwdLwD529gYVzl9euufrVyShuqVEJTxfh3GCu8XgXm3C_jE3MF27_fSoVp8WmDyHeai0ItYP-3o6M4glOOi3CsSAgWL6baK_KvpXzQpDmmkk?testcase_id=5259923043909632

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2016-11-30)

ClusterFuzz testcase is verified as fixed, closing issue.

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### sh...@chromium.org (2016-11-30)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-12-12)

[Empty comment from Monorail migration]

### aw...@google.com (2016-12-12)

Nice one!  The Panel awarded $1,500 for this report.  Thanks!

### aw...@chromium.org (2016-12-12)

[Empty comment from Monorail migration]

### aw...@google.com (2016-12-15)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-03-08)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2017-03-08)

This issue was migrated from crbug.com/chromium/668784?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40086086)*
