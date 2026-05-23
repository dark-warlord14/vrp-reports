# Use-of-uninitialized-value in SkOpAngle::insert

| Field | Value |
|-------|-------|
| **Issue ID** | [40086594](https://issues.chromium.org/issues/40086594) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Internals>Skia |
| **Platforms** | Linux |
| **Reporter** | cl...@chromium.org |
| **Assignee** | ca...@google.com |
| **Created** | 2017-01-21 |
| **Bounty** | $1,000.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5433787745042432

Fuzzer: attekett_surku_fuzzer
Job Type: linux_msan_chrome
Platform Id: linux

Crash Type: Use-of-uninitialized-value
Crash Address: 
Crash State:
  SkOpAngle::insert
  SkOpSegment::sortAngles
  HandleCoincidence
  
Sanitizer: memory (MSAN)

Recommended Security Severity: Medium

Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_msan_chrome&range=445274:445281

Minimized Testcase (202.80 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95k15Yz9tjTTyKM7syRsK6Er9mzSfhBx1-5a4zxrSDHFxwOhz2BBtXo3OT-VW0JYOtGGm2yoSZCYNh1LB6K1rwrTtbvikZ58W2ZBnvaaQGeUpN3vIKseF5m7L57y7JQuQrHC3k3gDNc9a6dmVpOb_G3_P6sN0yWaogy84mXj__BeeKfYwXHRB5yYcBDnk78RBmmMPyWNbtabXhOfuL0VJbe9n_ypzUjKtz4OsOGbBW7GxXQQymv8U66sUW2GIqT6KvrW61d-nd_icvPywbc8s8QNzofxC73jaaGAZ8J6O8Tv0WbHVe3zjyOiWwF80OA4CGgYCc0EON7aG5RQoK_-JbVqTtGQr_Nswwj9pjfAxXUMcOjI9Q?testcase_id=5433787745042432

Issue filed automatically.

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

## Timeline

### sh...@chromium.org (2017-01-22)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-01-22)

This issue is a security regression. If you are not able to fix this quickly, please revert the change that introduced it.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2017-01-22)

[Empty comment from Monorail migration]

### go...@chromium.org (2017-01-23)


A friendly reminder that M57 Beta launch is coming soon on February 2nd! Your bug is labelled as Beta ReleaseBlock, pls make sure to land the fix and get it merged into the release branch (2987) ASAP so it gets enough baking time in Dev (before Beta promotion). Thank you!

### es...@chromium.org (2017-01-24)

reed, could you please help find an owner for this security bug? Thanks!

[Monorail components: Internals>Skia]

### hc...@chromium.org (2017-01-24)

[Empty comment from Monorail migration]

### hc...@chromium.org (2017-01-24)

over to Cary...

### cl...@chromium.org (2017-01-24)

ClusterFuzz has detected this issue as fixed in range 445391:445491.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5433787745042432

Fuzzer: attekett_surku_fuzzer
Job Type: linux_msan_chrome
Platform Id: linux

Crash Type: Use-of-uninitialized-value
Crash Address: 
Crash State:
  SkOpAngle::insert
  SkOpSegment::sortAngles
  HandleCoincidence
  
Sanitizer: memory (MSAN)

Recommended Security Severity: Medium

Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_msan_chrome&range=445274:445281
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_msan_chrome&range=445391:445491

Minimized Testcase (202.80 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95k15Yz9tjTTyKM7syRsK6Er9mzSfhBx1-5a4zxrSDHFxwOhz2BBtXo3OT-VW0JYOtGGm2yoSZCYNh1LB6K1rwrTtbvikZ58W2ZBnvaaQGeUpN3vIKseF5m7L57y7JQuQrHC3k3gDNc9a6dmVpOb_G3_P6sN0yWaogy84mXj__BeeKfYwXHRB5yYcBDnk78RBmmMPyWNbtabXhOfuL0VJbe9n_ypzUjKtz4OsOGbBW7GxXQQymv8U66sUW2GIqT6KvrW61d-nd_icvPywbc8s8QNzofxC73jaaGAZ8J6O8Tv0WbHVe3zjyOiWwF80OA4CGgYCc0EON7aG5RQoK_-JbVqTtGQr_Nswwj9pjfAxXUMcOjI9Q?testcase_id=5433787745042432

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2017-01-24)

ClusterFuzz testcase 5433787745042432 is verified as fixed, so closing issue.

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### sh...@chromium.org (2017-01-24)

[Empty comment from Monorail migration]

### ca...@google.com (2017-01-24)

This should repro the uninitialized value at src/pathops/SkOpAngle.cpp:834:13 in SkOpAngle::insert(SkOpAngle*)

static void release_8(skiatest::Reporter* reporter, const char* filename) {
    SkPath path;
    path.setFillType((SkPath::FillType) 0);
path.setFillType(SkPath::kWinding_FillType);
path.moveTo(SkBits2Float(0x410c0000), SkBits2Float(0x41880000));  // 8.75f, 17
path.cubicTo(SkBits2Float(0x41000000), SkBits2Float(0x41880000), SkBits2Float(0x40e40000), SkBits2Float(0x41840000), SkBits2Float(0x40d80000), SkBits2Float(0x41780000));  // 8, 17, 7.125f, 16.5f, 6.75f, 15.5f
path.lineTo(SkBits2Float(0x3f800000), SkBits2Float(0x40400000));  // 1, 3
path.cubicTo(SkBits2Float(0x3f000000), SkBits2Float(0x3ff00000), SkBits2Float(0x3fc00000), SkBits2Float(0x00000000), SkBits2Float(0x40000000), SkBits2Float(0x00000000));  // 0.5f, 1.875f, 1.5f, 0, 2, 0
path.lineTo(SkBits2Float(0x41da0000), SkBits2Float(0x00000000));  // 27.25f, 0
path.cubicTo(SkBits2Float(0x41e00000), SkBits2Float(0x00000000), SkBits2Float(0x41e70000), SkBits2Float(0x3f000000), SkBits2Float(0x41ea0000), SkBits2Float(0x3fc00000));  // 28, 0, 28.875f, 0.5f, 29.25f, 1.5f
path.lineTo(SkBits2Float(0x420c0000), SkBits2Float(0x41600000));  // 35, 14
path.cubicTo(SkBits2Float(0x420e0000), SkBits2Float(0x41720000), SkBits2Float(0x420a0000), SkBits2Float(0x41880000), SkBits2Float(0x42080000), SkBits2Float(0x41880000));  // 35.5f, 15.125f, 34.5f, 17, 34, 17
path.lineTo(SkBits2Float(0x410c0000), SkBits2Float(0x41880000));  // 8.75f, 17
path.close();

    SkPath path1(path);
    path.reset();
    path.setFillType((SkPath::FillType) 0);
path.setFillType(SkPath::kWinding_FillType);
path.moveTo(SkBits2Float(0x411c0000), SkBits2Float(0x41800000));  // 9.75f, 16
path.cubicTo(SkBits2Float(0x41100000), SkBits2Float(0x41800000), SkBits2Float(0x41020000), SkBits2Float(0x41780000), SkBits2Float(0x40f80000), SkBits2Float(0x41680000));  // 9, 16, 8.125f, 15.5f, 7.75f, 14.5f
path.lineTo(SkBits2Float(0x40000000), SkBits2Float(0x40000000));  // 2, 2
path.cubicTo(SkBits2Float(0x40000000), SkBits2Float(0x3fc00000), SkBits2Float(0x40100000), SkBits2Float(0x3f800000), SkBits2Float(0x40400000), SkBits2Float(0x3f800000));  // 2, 1.5f, 2.25f, 1, 3, 1
path.lineTo(SkBits2Float(0x41d20000), SkBits2Float(0x3f800000));  // 26.25f, 1
path.cubicTo(SkBits2Float(0x41d80000), SkBits2Float(0x3f800000), SkBits2Float(0x41df0000), SkBits2Float(0x3fc00000), SkBits2Float(0x41e20000), SkBits2Float(0x40200000));  // 27, 1, 27.875f, 1.5f, 28.25f, 2.5f
path.lineTo(SkBits2Float(0x42080000), SkBits2Float(0x41700000));  // 34, 15
path.cubicTo(SkBits2Float(0x42080000), SkBits2Float(0x41780000), SkBits2Float(0x42070000), SkBits2Float(0x41800000), SkBits2Float(0x42040000), SkBits2Float(0x41800000));  // 34, 15.5f, 33.75f, 16, 33, 16
path.lineTo(SkBits2Float(0x411c0000), SkBits2Float(0x41800000));  // 9.75f, 16
path.close();

    SkPath path2(path);
    testPathOp(reporter, path1, path2, (SkPathOp) 0, filename);
}


### aw...@chromium.org (2017-01-27)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-02-06)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-02-06)

Congratulations! $1,000 for this find.

### aw...@chromium.org (2017-02-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-05-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2017-05-02)

This issue was migrated from crbug.com/chromium/683533?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40086594)*
