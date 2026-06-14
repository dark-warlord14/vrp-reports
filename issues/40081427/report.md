# Use-of-uninitialized-value in v8::internal::compiler::Schedule::block

| Field | Value |
|-------|-------|
| **Issue ID** | [40081427](https://issues.chromium.org/issues/40081427) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Unknown |
| **Reporter** | cl...@chromium.org |
| **Assignee** | ti...@chromium.org |
| **Created** | 2015-02-15 |
| **Bounty** | $1,000.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5112265213214720

Fuzzer: Decoder_langfuzz
Job Type: Linux_msan_d8

Crash Type: Use-of-uninitialized-value
Crash Address: 
Crash State:
  v8::internal::compiler::Schedule::block
  v8::internal::compiler::CFGBuilder::BuildBlockForNode
  v8::internal::compiler::CFGBuilder::BuildBlocksForSuccessors
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_msan_d8&range=315550:315577

Minimized Testcase (6.37 Kb): https://cluster-fuzz.appspot.com/download/AMIfv953eLwl9wUEG33UR7Y1XLl-DW0kNPHiwo5mpgN3iKLd8-0bUbKKSUqRO3aznR8Yl97tbasr-zWcRA452uk4bjDGrrio3FAhTL24QzFyX17bp-ZR2B6bc2QN6HNzWV0ra4tHeOjFE5448BwBrVan5vHGEw_EaA

Filer: inferno

## Timeline

### in...@chromium.org (2015-02-15)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-02-16)

[Empty comment from Monorail migration]

### ja...@chromium.org (2015-02-16)

The repro does not need msan, minimized test case is below.

function module(stdlib, foreign, heap) {
    "use asm";
    function foo(i) {
      var j = 0, i = -1;
      do  ; while (foo ? 0 : 2) ;      
      if (i > 0) {
        j = i;
      }
      return j;
    }
    return foo;
}

var foo = module(this, {}, new ArrayBuffer((1)*1024));
foo(0);

### bu...@chromium.org (2015-02-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/c5f7d2bb822f1cec021f590cf241bba5318d3ece

commit c5f7d2bb822f1cec021f590cf241bba5318d3ece
Author: titzer <titzer@chromium.org>
Date: Mon Feb 16 14:56:00 2015

[turbofan] Fix control reducer with re-reducing branches.

R=jarin@chromium.org
LOG=Y
BUG=chromium:458876

Review URL: https://codereview.chromium.org/917383004

Cr-Commit-Position: refs/heads/master@{#26666}

[modify] http://crrev.com/c5f7d2bb822f1cec021f590cf241bba5318d3ece/src/compiler/control-reducer.cc
[modify] http://crrev.com/c5f7d2bb822f1cec021f590cf241bba5318d3ece/src/compiler/graph-visualizer.cc
[add] http://crrev.com/c5f7d2bb822f1cec021f590cf241bba5318d3ece/test/mjsunit/regress/regress-458876.js


### in...@chromium.org (2015-02-16)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-02-16)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

Your fix is very close to the branch point. After the branch happens, please make sure to check if your fix is in.

- Your friendly ClusterFuzz

### cl...@chromium.org (2015-02-18)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5526326736322560

Fuzzer: Mbarbella_js_mutation
Job Type: Windows_asan_d8

Crash Type: UNKNOWN
Crash Address: 0x00000010
Crash State:
  v8::internal::compiler::Schedule::block
  v8::internal::compiler::CFGBuilder::BuildBlockForNode
  v8::internal::compiler::CFGBuilder::BuildBlocksForSuccessors
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=windows_asan_d8&range=316488:316499

Minimized Testcase (0.18 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv952VFwvDuALFTWiOIvo1E7T-Tq5B1Pv78E0ZOznnHpSQ8cCqOCWpqGFpERocPHRqhWasXk88gz30dcUT8G0tLbGgt3boZEtpgrGwA0_d75b9eQKIWDpgTz1kHh2oByBZ9qqdNADqla88Mu0aUh2aFfGu2deMw
function module() {
    "use asm";
    function __f_3() {
      do ; while (__f_3 ? 0 : 1) ;
      return -1 > 0 ? -1 : 0;
    }
    return __f_3;
}
var __f_3 = module();
 __f_3();


Filer: mbollu

### cl...@chromium.org (2015-02-18)

ClusterFuzz has detected this issue as fixed in range 316543:316580.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5112265213214720

Fuzzer: Decoder_langfuzz
Job Type: Linux_msan_d8

Crash Type: Use-of-uninitialized-value
Crash Address: 
Crash State:
  v8::internal::compiler::Schedule::block
  v8::internal::compiler::CFGBuilder::BuildBlockForNode
  v8::internal::compiler::CFGBuilder::BuildBlocksForSuccessors
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_msan_d8&range=315550:315577
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_msan_d8&range=316543:316580

Minimized Testcase (6.37 Kb): https://cluster-fuzz.appspot.com/download/AMIfv953eLwl9wUEG33UR7Y1XLl-DW0kNPHiwo5mpgN3iKLd8-0bUbKKSUqRO3aznR8Yl97tbasr-zWcRA452uk4bjDGrrio3FAhTL24QzFyX17bp-ZR2B6bc2QN6HNzWV0ra4tHeOjFE5448BwBrVan5vHGEw_EaA

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### ti...@google.com (2015-02-20)

Note to self: check back in on this to see what rev M42 ends up branching at and whether a merge is required.

### ti...@google.com (2015-02-25)

Regressed and fixed while still on trunk before M42 branch.

### cl...@chromium.org (2015-05-25)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2015-06-12)

$500 for the bug + $500 ClusterFuzz bonus.

Reward panel notes: Internal fuzzer caught this ~50 hours after found by decoder, and we pay out when not found within 48 hours.

We'll start payment via our new process, which should take 1-2 weeks. That 1-2 week period payment timeframe starts from when you see the "reward-inprocess" label on this bug.

### ti...@google.com (2015-06-25)

[Empty comment from Monorail migration]

### ti...@google.com (2015-07-24)

Processing via our e-payment system can take up to two weeks, but the reward should be on its way to you. Thanks again for your help!

(Note: sorry for the delay here - it turns out in the new payment system, these payments were waiting for a second approval from me).

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/458876?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081427)*
