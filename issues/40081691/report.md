# NO STACK

| Field | Value |
|-------|-------|
| **Issue ID** | [40081691](https://issues.chromium.org/issues/40081691) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript |
| **Reporter** | cl...@chromium.org |
| **Assignee** | ya...@chromium.org |
| **Created** | 2015-03-22 |
| **Bounty** | $3,500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5612329790603264

Fuzzer: Mbarbella_js_mutation
Job Type: Linux_asan_d8_dbg

Crash Type: UNKNOWN
Crash Address: 0x7fb88e60ce80
Crash State:
  NULL
Regressed: V8: r27257:27344

Minimized Testcase (2.48 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95GEWUreg8sG5f5bEuSnkPyUQyBsUoFOX0T36fiEs0W2Gz9ybPFZuqbm74uHV876PD3x18HwGY3XRWSuQn1SMelZhZpYAB6mw0viWxyu6-qBkKROKb0eCJ1VrbtrBm7jHM4izDfL0BGGeDyGq2re7KapoFwnA

Filer: machenbach

## Timeline

### ma...@chromium.org (2015-03-22)

PTAL

### cl...@chromium.org (2015-03-22)

[Empty comment from Monorail migration]

### ja...@chromium.org (2015-03-23)

[Empty comment from Monorail migration]

### ms...@chromium.org (2015-03-23)

Hmm, unable to repro so far. I tried ia32/x64, ASAN on/off, ASAN options set/unset and clang/gcc. So far no joy.

### ms...@chromium.org (2015-03-23)

I can repro it with commit fd51f615ebaf9a02c125f78a34d3243cc85a0b24, but the call-stack is completely messed up and the only return-address I could make out anywhere on the stack is in non-V8 code for which I don't have any symbols. This is a hard one. Not sure yet whether it points to a real issue or whether it's a red herring.

### ms...@chromium.org (2015-03-23)

This appears to go awry somewhere in generated RegExp code, the last sensible call I could trace was through the RegExpExec stub.

### ms...@chromium.org (2015-03-23)

[Empty comment from Monorail migration]

### ya...@chromium.org (2015-03-23)

What arch/mode/asan options did you use to reproduce?

### cl...@chromium.org (2015-03-24)

ClusterFuzz has detected this issue as fixed in range 27348:27352.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5612329790603264

Fuzzer: Mbarbella_js_mutation
Job Type: Linux_asan_d8_dbg

Crash Type: UNKNOWN
Crash Address: 0x7fb88e60ce80
Crash State:
  NULL
Regressed: V8: r27257:27344
Fixed: V8: r27348:27352

Minimized Testcase (2.48 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95GEWUreg8sG5f5bEuSnkPyUQyBsUoFOX0T36fiEs0W2Gz9ybPFZuqbm74uHV876PD3x18HwGY3XRWSuQn1SMelZhZpYAB6mw0viWxyu6-qBkKROKb0eCJ1VrbtrBm7jHM4izDfL0BGGeDyGq2re7KapoFwnA

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### ts...@chromium.org (2015-03-25)

Clicked "redo fixed" on CF.

### cl...@chromium.org (2015-03-26)

ClusterFuzz has detected this issue as fixed in range 27348:27352.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5612329790603264

Fuzzer: Mbarbella_js_mutation
Job Type: Linux_asan_d8_dbg

Crash Type: UNKNOWN
Crash Address: 0x7fb88e60ce80
Crash State:
  NULL
Regressed: V8: r27257:27344
Fixed: V8: r27348:27352

Minimized Testcase (2.48 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95GEWUreg8sG5f5bEuSnkPyUQyBsUoFOX0T36fiEs0W2Gz9ybPFZuqbm74uHV876PD3x18HwGY3XRWSuQn1SMelZhZpYAB6mw0viWxyu6-qBkKROKb0eCJ1VrbtrBm7jHM4izDfL0BGGeDyGq2re7KapoFwnA

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### ms...@chromium.org (2015-03-26)

Maeh, ClusterFuzz, I don't believe you, you are lying to me. Please keep this issue open.

### ms...@chromium.org (2015-03-26)

Re #8 just for posterity:

$ git checkout fd51f615ebaf9a02c125f78a34d3243cc85a0b24
$ make -j100 x64.debug asan=on
$ ./out/x64.debug/d8 --expose-gc --allow-natives-syntax --es-staging --verify-heap --gc-interval=173 --stress-compaction --stack-size=100 --random-seed=2092088013 ~/Downloads/fuzz-00509.js

### ms...@chromium.org (2015-03-26)

This happens when we have a GC that does code compaction while allocating the message for a stack-overflow exception from a RegExp (sic!). This one is crazily complex, I briefed Yang (our resident RegExp guy) and he graciously agreed to take cook up a fix. Thanks!

### ts...@chromium.org (2015-03-26)

mstarzinger@ - Do you know offhand how far this go back?  I'd like to set some labels on the bug, but I'm not trusting the CF regression range, either.

### ms...@chromium.org (2015-03-26)

Re #15: This is probably going back until forever, but I didn't verify, maybe Yang knows. The following is a link to the fix that Yang has in flight.

https://codereview.chromium.org/1034173002/

### in...@chromium.org (2015-03-26)

[Empty comment from Monorail migration]

### ya...@chromium.org (2015-03-27)

We've had this bug for at least the past four years, if not longer.

### cl...@chromium.org (2015-03-27)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-04-03)

[Empty comment from Monorail migration]

### bu...@chromium.org (2015-04-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/c67cb287a901ddf03d4ae4dafcf431d09fd3e22c

commit c67cb287a901ddf03d4ae4dafcf431d09fd3e22c
Author: yangguo <yangguo@chromium.org>
Date: Tue Apr 07 09:44:47 2015

Always update raw pointers when handling interrupts inside RegExp code.

R=mstarzinger@chromium.org
BUG=chromium:469480
LOG=N

Review URL: https://codereview.chromium.org/1034173002

Cr-Commit-Position: refs/heads/master@{#27615}

[modify] http://crrev.com/c67cb287a901ddf03d4ae4dafcf431d09fd3e22c/src/arm/regexp-macro-assembler-arm.cc
[modify] http://crrev.com/c67cb287a901ddf03d4ae4dafcf431d09fd3e22c/src/arm64/regexp-macro-assembler-arm64.cc
[modify] http://crrev.com/c67cb287a901ddf03d4ae4dafcf431d09fd3e22c/src/ia32/regexp-macro-assembler-ia32.cc
[modify] http://crrev.com/c67cb287a901ddf03d4ae4dafcf431d09fd3e22c/src/isolate.cc
[modify] http://crrev.com/c67cb287a901ddf03d4ae4dafcf431d09fd3e22c/src/mips/regexp-macro-assembler-mips.cc
[modify] http://crrev.com/c67cb287a901ddf03d4ae4dafcf431d09fd3e22c/src/mips64/regexp-macro-assembler-mips64.cc
[modify] http://crrev.com/c67cb287a901ddf03d4ae4dafcf431d09fd3e22c/src/ppc/regexp-macro-assembler-ppc.cc
[modify] http://crrev.com/c67cb287a901ddf03d4ae4dafcf431d09fd3e22c/src/regexp-macro-assembler.cc
[modify] http://crrev.com/c67cb287a901ddf03d4ae4dafcf431d09fd3e22c/src/regexp-macro-assembler.h
[modify] http://crrev.com/c67cb287a901ddf03d4ae4dafcf431d09fd3e22c/src/x64/regexp-macro-assembler-x64.cc
[modify] http://crrev.com/c67cb287a901ddf03d4ae4dafcf431d09fd3e22c/src/x87/regexp-macro-assembler-x87.cc
[add] http://crrev.com/c67cb287a901ddf03d4ae4dafcf431d09fd3e22c/test/mjsunit/regress/regress-crbug-469480.js


### ya...@chromium.org (2015-04-07)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-04-07)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### ya...@chromium.org (2015-04-07)

I don't think it makes sense to merge this.

### ti...@google.com (2015-04-09)

If you don't want to merge it (understandable in the circumstances), but this wont roll out till late July in M44.

If someone wants this in M43, please re-add Merge-Triage as we only missed the branch point by a few days.

### cl...@chromium.org (2015-07-14)

Bulk update: removing view restriction from closed bugs.

### mb...@chromium.org (2016-05-06)

Adding reward-topanel to consider https://crbug.com/chromium/463425 for a reward (duped into here).

### ti...@google.com (2016-05-12)

Congrats - $3,500 for this report.

I'll add it to next week's payment run. Woohoo!

### aw...@chromium.org (2016-06-08)

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

This issue was migrated from crbug.com/chromium/469480?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/463425]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081691)*
