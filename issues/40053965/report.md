# Security: Uninitialised memory read with BigInt right-shift

| Field | Value |
|-------|-------|
| **Issue ID** | [40053965](https://issues.chromium.org/issues/40053965) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>JavaScript |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | an...@googlemail.com |
| **Assignee** | jk...@chromium.org |
| **Created** | 2020-11-23 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**

Right-shifts with BigInts may not initialise the most significant digit, which can be used to read a pointer-sized word of uninitialised memory.

**VERSION**

V8, commit 203a72833cc83ee3afda0a310ebf971be9a586dc  

Operating System: Any

**REPRODUCTION CASE**

Run in d8:

```
for (let i = 0, j = 0; i < 1_000_000; ++i) {  
  let x = (-0xffffffffffffffff_ffffffffffffffffn >> 0x40n);  
  if (x != -0x10000000000000000n) {  
    print(x.toString(16));  
    if (++j == 10) break;  
  }  
}  
  

```

Prints "-bfbfbfbfbfbfbfc00000000000000000" ten times in debug builds, where `0xbf` is the uninitialised memory marker for BigInts <https://github.com/v8/v8/blob/db5ede7ff8f34503fd7e99de5ded35309ac8fe64/src/objects/bigint.cc#L269-L271>. The last byte is 0xc0 because +1 is added to 0xbf. In non-debug builds, uninitialised memory can be observed.

The fix is relatively simple, in the `if (bits_shift == 0) {` block in <https://github.com/v8/v8/blob/db5ede7ff8f34503fd7e99de5ded35309ac8fe64/src/objects/bigint.cc#L1876>, add:

```
if (bits_shift == 0) {  
  // We must manually initialize the overflow space, if it was allocated.  
  result->set_digit(result_length - 1, 0);  
  ...  

```

NOTE:

The same BigInt implementation is also used in JSC and SpiderMonkey, so the bug can be reproduced there, too, which makes this a cross-browser issue. That means for example, releasing a regression test could easily be used to discover the same issue in the other browsers.

**CREDIT INFORMATION**

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: André Bargull

## Timeline

### an...@googlemail.com (2020-11-23)

JSC: https://bugs.webkit.org/show_bug.cgi?id=219253
SM: https://bugzilla.mozilla.org/show_bug.cgi?id=1679003

### [Deleted User] (2020-11-23)

[Empty comment from Monorail migration]

### cl...@chromium.org (2020-11-23)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5641451058036736.

### cl...@chromium.org (2020-11-23)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5706420491452416.

### mb...@chromium.org (2020-11-23)

[Empty comment from Monorail migration]

[Monorail components: Blink>JavaScript]

### cl...@chromium.org (2020-11-23)

[Empty comment from Monorail migration]

### [Deleted User] (2020-11-23)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cl...@chromium.org (2020-11-23)

Automatically assigning owner based on suspected regression changelist https://chromium.googlesource.com/v8/v8/+/dcd2032bb7c645bb26caa257c8ca8d78623655dd ([ESNext] Ship numeric separators).

If this is incorrect, please let us know why and apply the Test-Predator-Wrong-CLs label. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### cl...@chromium.org (2020-11-23)

Detailed Report: https://clusterfuzz.com/testcase?key=5706420491452416

Fuzzer: None
Job Type: linux_msan_d8
Platform Id: linux

Crash Type: Use-of-uninitialized-value
Crash Address: 
Crash State:
  v8::internal::MutableBigInt::AbsoluteAddOne
  v8::internal::MutableBigInt::RightShiftByAbsolute
  v8::internal::BigInt::SignedRightShift
  
Sanitizer: memory (MSAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=linux_msan_d8&range=60579:60580

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5706420491452416

See https://www.chromium.org/developers/testing/memorysanitizer#TOC-Reproducing-ClusterFuzz-Bugs for instructions on reproducing this bug locally.

### [Deleted User] (2020-11-24)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jk...@chromium.org (2020-11-25)

I'll take this one.

### jk...@chromium.org (2020-11-25)

Thanks for the report, and the fix suggestion!

CL in flight: https://chromium-review.googlesource.com/c/v8/v8/+/2561618

Security analysis: OOB read as a primitive value, i.e. one can read a (somewhat hard to control) internal pointer value as a numeric value. I don't think it's possible to craft a pointer from it, or to turn it into an OOB write (which in particular is possible when a pointer is read OOB, which isn't the case here). But this could be helpful when some other attack requires knowledge of a valid pointer value.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-11-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/e82a3b4d47a93ab64f07d8c03e3cd17b6b961c3f

commit e82a3b4d47a93ab64f07d8c03e3cd17b6b961c3f
Author: Jakob Kummerow <jkummerow@chromium.org>
Date: Thu Nov 26 09:24:15 2020

[bigint] Fix possibly-uninitialized leading digit on right shift

Fixed: chromium:1151890
Change-Id: I26f5c76494a9ff3f5a141f381e1c9a543e368571
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2561618
Auto-Submit: Jakob Kummerow <jkummerow@chromium.org>
Commit-Queue: Georg Neis <neis@chromium.org>
Reviewed-by: Georg Neis <neis@chromium.org>
Cr-Commit-Position: refs/heads/master@{#71422}

[modify] https://crrev.com/e82a3b4d47a93ab64f07d8c03e3cd17b6b961c3f/src/objects/bigint.cc
[add] https://crrev.com/e82a3b4d47a93ab64f07d8c03e3cd17b6b961c3f/test/mjsunit/regress/regress-crbug-1151890.js


### cl...@chromium.org (2020-11-26)

ClusterFuzz testcase 5706420491452416 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_msan_d8&range=71421:71422

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### [Deleted User] (2020-11-26)

[Empty comment from Monorail migration]

### [Deleted User] (2020-11-26)

[Empty comment from Monorail migration]

### [Deleted User] (2020-11-26)

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M87. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-11-26)

This bug requires manual review: Request affecting a post-stable build
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on ToT?
4. Does this change need to be merged into other active release branches (M-1, M+1)?
5. Why are these changes required in this milestone after branch?
6. Is this a new feature?
7. If it is a new feature, is it behind a flag using finch?

Chrome OS Only:
8. Was the change reviewed and approved by the Eng Prod Representative? See Eng Prod ownership by component: http://go/cros-engprodcomponents

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), bindusuvarna @(iOS), cindyb@(ChromeOS), lakpamarthy@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jk...@chromium.org (2020-11-27)

#17: If it gets merged to 87 then it should be merged to 88 too.

#18:
1.) Yes. Security issue, very low complexity fix.
2.) https://chromium.googlesource.com/v8/v8.git/+/e82a3b4d47a93ab64f07d8c03e3cd17b6b961c3f (see #13 above)
3.) Yes
4.) Yes, M88
5.) Old bug discovered now (has been around for ~2 years I think)
6.) No
7.) n/a

### [Deleted User] (2020-11-28)

Your change meets the bar and is auto-approved for M88. Please go ahead and merge the CL to branch 4324 (refs/branch-heads/4324) manually. Please contact milestone owner if you have questions.
Merge instructions: https://www.chromium.org/developers/how-tos/drover
Owners: govind@(Android), bindusuvarna@(iOS), dgagnon@(ChromeOS), srinivassista @(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-11-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/dfdf793b6bc0fc98178e493b94b65a1b0ba54c63

commit dfdf793b6bc0fc98178e493b94b65a1b0ba54c63
Author: Jakob Kummerow <jkummerow@chromium.org>
Date: Mon Nov 30 16:04:16 2020

[bigint] Fix possibly-uninitialized leading digit on right shift

(cherry picked from commit e82a3b4d47a93ab64f07d8c03e3cd17b6b961c3f)

Fixed: chromium:1151890
Change-Id: I26f5c76494a9ff3f5a141f381e1c9a543e368571
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2561618
Auto-Submit: Jakob Kummerow <jkummerow@chromium.org>
Commit-Queue: Georg Neis <neis@chromium.org>
Reviewed-by: Georg Neis <neis@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#71422}
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2565132
Reviewed-by: Jakob Kummerow <jkummerow@chromium.org>
Cr-Commit-Position: refs/branch-heads/8.8@{#13}
Cr-Branched-From: 2dbcdc105b963ee2501c82139eef7e0603977ff0-refs/heads/8.8.278@{#1}
Cr-Branched-From: 366d30c99049b3f1c673f8a93deb9f879d0fa9f0-refs/heads/master@{#71094}

[modify] https://crrev.com/dfdf793b6bc0fc98178e493b94b65a1b0ba54c63/src/objects/bigint.cc
[add] https://crrev.com/dfdf793b6bc0fc98178e493b94b65a1b0ba54c63/test/mjsunit/regress/regress-crbug-1151890.js


### la...@google.com (2020-11-30)

+adetaylor@ to review the M87 merge request

### ad...@chromium.org (2020-11-30)

Approving merge to M87 as well.

### sr...@google.com (2020-11-30)

Please complete the merges to M88 branch asap. We are cutting dev release build today ( Nov 30, 2020) around 3pm PST. so please help complete the merges asap so they can be part of the release build 

### sr...@google.com (2020-11-30)

per https://crbug.com/chromium/1151890#c21

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-11-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/1162c460dee4218abd798b51b88926aef5c8bd61

commit 1162c460dee4218abd798b51b88926aef5c8bd61
Author: Jakob Kummerow <jkummerow@chromium.org>
Date: Mon Nov 30 21:06:56 2020

[bigint] Fix possibly-uninitialized leading digit on right shift

(cherry picked from commit e82a3b4d47a93ab64f07d8c03e3cd17b6b961c3f)

Fixed: chromium:1151890
Change-Id: I26f5c76494a9ff3f5a141f381e1c9a543e368571
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2561618
Auto-Submit: Jakob Kummerow <jkummerow@chromium.org>
Commit-Queue: Georg Neis <neis@chromium.org>
Reviewed-by: Georg Neis <neis@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#71422}
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2565245
Reviewed-by: Jakob Kummerow <jkummerow@chromium.org>
Cr-Commit-Position: refs/branch-heads/8.7@{#57}
Cr-Branched-From: 0d81cd72688512abcbe1601015baee390c484a6a-refs/heads/8.7.220@{#1}
Cr-Branched-From: 942c2ef85caef00fcf02517d049f05e9a3d4b440-refs/heads/master@{#70196}

[modify] https://crrev.com/1162c460dee4218abd798b51b88926aef5c8bd61/src/objects/bigint.cc
[add] https://crrev.com/1162c460dee4218abd798b51b88926aef5c8bd61/test/mjsunit/regress/regress-crbug-1151890.js


### jk...@chromium.org (2020-11-30)

[Empty comment from Monorail migration]

### ad...@google.com (2020-12-02)

[Empty comment from Monorail migration]

### ad...@google.com (2020-12-02)

[Empty comment from Monorail migration]

### ad...@google.com (2020-12-02)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-12-03)

Congratulations! The VRP panel has decided to award $3000 for this bug.

(Incidentally feel free to cc the relevant WebKit/Mozilla folks on here if that's helpful to them).

### ad...@google.com (2020-12-04)

[Empty comment from Monorail migration]

### ad...@google.com (2020-12-07)

[Empty comment from Monorail migration]

### vs...@google.com (2020-12-10)

[Empty comment from Monorail migration]

### vs...@google.com (2020-12-10)

[Empty comment from Monorail migration]

### ke...@google.com (2020-12-11)

[Empty comment from Monorail migration]

### [Deleted User] (2020-12-14)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-12-18)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2021-01-07)

[Empty comment from Monorail migration]

### ja...@google.com (2021-01-15)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-15)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-01-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/412ac52d82466fc6a097bb398d799f9a708beadf

commit 412ac52d82466fc6a097bb398d799f9a708beadf
Author: Jakob Kummerow <jkummerow@chromium.org>
Date: Tue Jan 19 17:59:52 2021

[bigint] Fix possibly-uninitialized leading digit on right shift

(cherry picked from commit e82a3b4d47a93ab64f07d8c03e3cd17b6b961c3f)

(cherry picked from commit 1162c460dee4218abd798b51b88926aef5c8bd61)

No-Try: true
No-Presubmit: true
No-Tree-Checks: true
Fixed: chromium:1151890
Change-Id: I26f5c76494a9ff3f5a141f381e1c9a543e368571
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2561618
Auto-Submit: Jakob Kummerow <jkummerow@chromium.org>
Commit-Queue: Georg Neis <neis@chromium.org>
Reviewed-by: Georg Neis <neis@chromium.org>
Cr-Original-Original-Commit-Position: refs/heads/master@{#71422}
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2565245
Reviewed-by: Jakob Kummerow <jkummerow@chromium.org>
Cr-Original-Commit-Position: refs/branch-heads/8.7@{#57}
Cr-Original-Branched-From: 0d81cd72688512abcbe1601015baee390c484a6a-refs/heads/8.7.220@{#1}
Cr-Original-Branched-From: 942c2ef85caef00fcf02517d049f05e9a3d4b440-refs/heads/master@{#70196}
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2624611
Commit-Queue: Victor-Gabriel Savu <vsavu@google.com>
Cr-Commit-Position: refs/branch-heads/8.6@{#54}
Cr-Branched-From: a64aed2333abf49e494d2a5ce24bbd14fff19f60-refs/heads/8.6.395@{#1}
Cr-Branched-From: a626bc036236c9bf92ac7b87dc40c9e538b087e3-refs/heads/master@{#69472}

[modify] https://crrev.com/412ac52d82466fc6a097bb398d799f9a708beadf/src/objects/bigint.cc
[add] https://crrev.com/412ac52d82466fc6a097bb398d799f9a708beadf/test/mjsunit/regress/regress-crbug-1151890.js


### ja...@google.com (2021-01-19)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-21)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-04)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1151890?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40053965)*
