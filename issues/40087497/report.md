# Container-overflow in SkSL::Compiler::addDefinitions

| Field | Value |
|-------|-------|
| **Issue ID** | [40087497](https://issues.chromium.org/issues/40087497) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Skia |
| **Platforms** | Linux |
| **Reporter** | cl...@chromium.org |
| **Assignee** | et...@chromium.org |
| **Created** | 2017-04-29 |
| **Bounty** | $1,500.00 |

## Description

Detailed report: https://clusterfuzz.com/testcase?key=5143412983726080

Fuzzer: attekett_dom_fuzzer
Job Type: linux_asan_chrome_media
Platform Id: linux

Crash Type: Container-overflow READ 4
Crash Address: 0x61000006be40
Crash State:
  SkSL::Compiler::addDefinitions
  SkSL::Compiler::scanCFG
  SkSL::Compiler::internalConvertProgram
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_media&range=468030:468089

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5143412983726080


Issue filed automatically.

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

## Timeline

### sh...@chromium.org (2017-04-29)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-04-29)

This issue is a security regression. If you are not able to fix this quickly, please revert the change that introduced it.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2017-04-29)

[Empty comment from Monorail migration]

### me...@chromium.org (2017-05-01)

Suspecting https://chromium.googlesource.com/skia/+/fe53e5828fd31326cdc4594ca06435eb0af50afe%5E%21/#F0

ethannicholas@: Can you please take a look or reassign as appropriate? Thanks.

[Monorail components: Internals>Skia]

### me...@chromium.org (2017-05-03)

ethannicholas: Friendly ping as part of the security fixit week.

### et...@chromium.org (2017-05-05)

I believe this will be fixed by https://skia-review.googlesource.com/c/15383/.

### cl...@chromium.org (2017-05-06)

ClusterFuzz has detected this issue as fixed in range 469656:469727.

Detailed report: https://clusterfuzz.com/testcase?key=5143412983726080

Fuzzer: attekett_dom_fuzzer
Job Type: linux_asan_chrome_media
Platform Id: linux

Crash Type: Container-overflow READ 4
Crash Address: 0x61000006be40
Crash State:
  SkSL::Compiler::addDefinitions
  SkSL::Compiler::scanCFG
  SkSL::Compiler::internalConvertProgram
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_media&range=468030:468089
Fixed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_media&range=469656:469727

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5143412983726080


See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### sh...@chromium.org (2017-05-06)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-05-15)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-05-15)

Nice one attekett! The panel decided to award $1,000 for this, plus the $500 clusterfuzz bonus.

However, they would consider raising the reward if you could demonstrate how it could be used.


### aw...@chromium.org (2017-05-15)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-05-18)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-08-12)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2017-08-12)

This issue was migrated from crbug.com/chromium/716713?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40087497)*
