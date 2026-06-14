# Use-of-uninitialized-value in v8::internal::Decoder<v8::internal::Simulator>::DecodeBranchSystemException

| Field | Value |
|-------|-------|
| **Issue ID** | [40080690](https://issues.chromium.org/issues/40080690) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript |
| **Reporter** | cl...@chromium.org |
| **Assignee** | ul...@chromium.org |
| **Created** | 2014-10-21 |
| **Bounty** | $2,500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6390149838536704

Fuzzer: Decoder_langfuzz
Job Type: Linux_msan_d8

Crash Type: Use-of-uninitialized-value
Crash Address: 
Crash State:
  v8::internal::Decoder<v8::internal::Simulator>::DecodeBranchSystemException
  v8::internal::Simulator::CallVoid
  v8::internal::Simulator::CallJS
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_msan_d8&range=299683:299847

Minimized Testcase (13.00 Kb): https://cluster-fuzz.appspot.com/download/AMIfv97k79ae8xp5fUEsxRVTVs1KlYXtiQRWFPndPgwQofvBm-insjPZX5lO9zTNBCndceM-iD_jW0dKCD6cmNRzer2yf5DO9f058EC4Je73SKNnTUW77CKvkk1kfu6Xx_IJO8yzpmun70toi05u8-YB96cMaeQcVg

Filer: aarya

## Timeline

### in...@chromium.org (2014-10-21)

Is this security related, can you please take a look.

### cl...@chromium.org (2014-10-21)

[Empty comment from Monorail migration]

### mb...@chromium.org (2014-10-21)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-10-22)

This medium+ severity security issue is a regression on trunk.

Please fix this asap. If you are unable to look into this soon, please revert your change.

- Your friendly ClusterFuzz

### da...@chromium.org (2014-10-22)

Giving to Ulan since Jakob is out the rest of the week.

### jk...@chromium.org (2014-10-22)

AFAICT it's an arm64-specific bug in Builtins::Generate_StringConstructCode. While it should index into the stack (in positive direction), it uses "__ Claim(argc, kXRegSize);" to subtract |argc| words from the stack pointer, then proceeds to read uninitialized memory from the stack.
I'm not sure about exploitability; since the bug is in string construction, it does not allow reading uninitialized stack memory directly; however it also messes up the stack pointer, which easily leads to crashes and probably makes it possible to do rather nasty things.
The code dates back to the initial import of the ARM64 port.

Reduced repro:
----------------------
var correct_result = "This is the correct result.";

function foo(recursion_depth) {
  if (recursion_depth > 0) return foo(recursion_depth - 1);
  return new String(correct_result, 1, 2, 3, 4, 5, 6);
}

// Roll our own non-strict assertEquals replacement.
function test(i) {
  var actual = foo(i);
  if (correct_result != actual) {
    var msg = "Expected \"" + correct_result + "\", found " + actual;
    throw new MjsUnitAssertionError(msg);
  }
}
test(1);
test(1);
test(10);
test(100);
----------------------

I could cook up a patch, but I'm not experienced with arm64, so if one of you lovely folks on CC could beat me to it, that would be awesome.
(Rodolph, as this is marked as a security issue, you'll have to explicitly CC anyone who needs to be able to see it.)

### in...@chromium.org (2014-10-22)

Based on "it also messes up the stack pointer, which easily leads to crashes and probably makes it possible to do rather nasty things.", updating severity.

### bu...@chromium.org (2014-10-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/ecbfc43f37ad5849c2f8c52c1d6b00a92a688a27

commit ecbfc43f37ad5849c2f8c52c1d6b00a92a688a27
Author: rodolph.perfetta@arm.com <rodolph.perfetta@arm.com>
Date: Wed Oct 22 18:24:20 2014

ARM64: Fix stack manipulation.

Builtins::Generate_StringConstructCode was claiming stack space instead of
giving it back.

BUG=chromium:425585
LOG=Y
R=jkummerow@chromium.org

Review URL: https://codereview.chromium.org/672623003

git-svn-id: https://v8.googlecode.com/svn/branches/bleeding_edge@24815 ce2b1a6d-e550-0410-aec6-3dcde31c8c00

[modify] https://chromium.googlesource.com/v8/v8.git/+/ecbfc43f37ad5849c2f8c52c1d6b00a92a688a27/src/arm64/builtins-arm64.cc
[add] https://chromium.googlesource.com/v8/v8.git/+/ecbfc43f37ad5849c2f8c52c1d6b00a92a688a27/test/mjsunit/regress/regress-crbug-425585.js


### bu...@chromium.org (2014-10-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/ecbfc43f37ad5849c2f8c52c1d6b00a92a688a27

commit ecbfc43f37ad5849c2f8c52c1d6b00a92a688a27
Author: rodolph.perfetta@arm.com <rodolph.perfetta@arm.com>
Date: Wed Oct 22 18:24:20 2014

ARM64: Fix stack manipulation.

Builtins::Generate_StringConstructCode was claiming stack space instead of
giving it back.

BUG=chromium:425585
LOG=Y
R=jkummerow@chromium.org

Review URL: https://codereview.chromium.org/672623003

git-svn-id: https://v8.googlecode.com/svn/branches/bleeding_edge@24815 ce2b1a6d-e550-0410-aec6-3dcde31c8c00

[modify] https://chromium.googlesource.com/v8/v8.git/+/ecbfc43f37ad5849c2f8c52c1d6b00a92a688a27/src/arm64/builtins-arm64.cc
[add] https://chromium.googlesource.com/v8/v8.git/+/ecbfc43f37ad5849c2f8c52c1d6b00a92a688a27/test/mjsunit/regress/regress-crbug-425585.js


### in...@chromium.org (2014-10-22)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-10-22)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-10-24)

ClusterFuzz has detected this issue as fixed in range 300874:300885.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6390149838536704

Fuzzer: Decoder_langfuzz
Job Type: Linux_msan_d8

Crash Type: Use-of-uninitialized-value
Crash Address: 
Crash State:
  v8::internal::Decoder<v8::internal::Simulator>::DecodeBranchSystemException
  v8::internal::Simulator::CallVoid
  v8::internal::Simulator::CallJS
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_msan_d8&range=299683:299847
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_msan_d8&range=300874:300885

Minimized Testcase (13.00 Kb): https://cluster-fuzz.appspot.com/download/AMIfv97k79ae8xp5fUEsxRVTVs1KlYXtiQRWFPndPgwQofvBm-insjPZX5lO9zTNBCndceM-iD_jW0dKCD6cmNRzer2yf5DO9f058EC4Je73SKNnTUW77CKvkk1kfu6Xx_IJO8yzpmun70toi05u8-YB96cMaeQcVg

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### ti...@google.com (2015-01-22)

Money time. $2000 for this report +$500 bonus for ClusterFuzz.

### cl...@chromium.org (2015-01-28)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2015-03-09)

[Empty comment from Monorail migration]

### ti...@google.com (2015-04-06)

Processing via our e-payment system can take up to six weeks, but the reward should be on its way to you. Thanks again for your help!

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/425585?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080690)*
