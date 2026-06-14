# Security: use-of-uninitialized-value in SkPathMeasure::distanceToSegment

| Field | Value |
|-------|-------|
| **Issue ID** | [40088273](https://issues.chromium.org/issues/40088273) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Internals>Skia |
| **Platforms** | Linux, Windows |
| **Reporter** | tk...@googlemail.com |
| **Assignee** | ca...@google.com |
| **Created** | 2017-07-04 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**

The use of an uninitialized value in SkPathMeasure::distanceToSegment may lead to an out-of-bounds array access in SkPathMeasure::getSegment. This may result in bogus SkPoint structures being provided to SkPathMeasure\_segTo, possibly leading to an exploitable state.

1. The testcase (testcase.html) crashes the latest MSAN build of Chrome on Linux as follows (the complete stack trace can be found in msan.txt):

==2735==WARNING: MemorySanitizer: use-of-uninitialized-value  

#0 0x5576a9356da9 in SkPathMeasure::distanceToSegment(float, float\*) third\_party/skia/src/core/SkPathMeasure.cpp:568:13  

#1 0x5576a935850e in SkPathMeasure::getSegment(float, float, SkPath\*, bool) third\_party/skia/src/core/SkPathMeasure.cpp:655:36  

#2 0x5576a9f573c7 in SkDashPath::InternalFilter(SkPath\*, SkPath const&, SkStrokeRec\*, SkRect const\*, float const\*, int, float, int, float, SkDashPath::StrokeRecApplication) third\_party/skia/src/utils/SkDashPath.cpp:304:18  

..

2. The testcase (testcase.html) crashes the latest ASAN build of Chrome on Windows 10 as follows (the complete stack trace can be found in asan.txt):

=================================================================  

==5200==ERROR: AddressSanitizer: access-violation on unknown address 0xfd0af1c0 (pc 0x132e50e3 bp 0x04daa36c sp 0x04daa35c T0)  

==5200==The signal is caused by a READ memory access.  

==5200==\*\*\* WARNING: Failed to initialize DbgHelp! \*\*\*  

==5200==\*\*\* Most likely this means that the app is already \*\*\*  

==5200==\*\*\* using DbgHelp, possibly with incompatible flags. \*\*\*  

==5200==\*\*\* Due to technical reasons, symbolization might crash \*\*\*  

==5200==\*\*\* or produce wrong results. \*\*\*  

#0 0x132e50e2 in SkChopCubicAt(struct SkPoint const \* const,struct SkPoint \* const,float) C:\b\c\b\win\_asan\_release\src\third\_party\skia\src\core\SkGeometry.cpp:356  

#1 0x134a3500 in SkPathMeasure\_segTo(struct SkPoint const \* const,unsigned int,float,float,class SkPath \*) C:\b\c\b\win\_asan\_release\src\third\_party\skia\src\core\SkPathMeasure.cpp:110:21  

#2 0x134a8a03 in SkPathMeasure::getSegment(float,float,class SkPath \*,bool) C:\b\c\b\win\_asan\_release\src\third\_party\skia\src\core\SkPathMeasure.cpp:671:9  

..

3. Further debugging information for Chrome Stable on Windows 10 can be found in WinDbg\_Chrome\_Stable.txt.

**VERSION**

Tested on:

- Chrome Stable Version 59.0.3071.115 (64-Bit, Windows 10)
- msan-chained-origins-linux-release-483947
- asan-win32-release-483942

**REPRODUCTION CASE**

Provided files:

- testcase.html -- Testcase to trigger the issue.
- msan.txt -- Detailed MSAN output (Linux).
- asan.txt -- Detailed ASAN output (Windows 10).
- WinDbg\_Chrome\_Stable.txt -- Further debugging information (Chrome Stable on Windows 10).

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**

Type of crash: tab

## Attachments

- [testcase.html](attachments/testcase.html) (text/plain, 709 B)
- [msan.txt](attachments/msan.txt) (text/plain, 15.0 KB)
- [asan.txt](attachments/asan.txt) (text/plain, 12.2 KB)
- [WinDbg_Chrome_Stable.txt](attachments/WinDbg_Chrome_Stable.txt) (text/plain, 11.1 KB)

## Timeline

### cl...@chromium.org (2017-07-04)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6579450547535872.

### cl...@chromium.org (2017-07-05)

Detailed report: https://clusterfuzz.com/testcase?key=6579450547535872

Job Type: linux_asan_chrome_mp
Crash Type: UNKNOWN READ
Crash Address: 0x60adf60d5040
Crash State:
  SkChopCubicAt
  SkPathMeasure_segTo
  SkPathMeasure::getSegment
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=484002:484005

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6579450547535872


See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

A recommended severity was added to this bug. Please change the severity if it is inaccurate.


### cl...@chromium.org (2017-07-05)

Detailed report: https://clusterfuzz.com/testcase?key=6579450547535872

Job Type: linux_asan_chrome_mp
Crash Type: UNKNOWN READ
Crash Address: 0x60adf60d5040
Crash State:
  SkChopCubicAt
  SkPathMeasure_segTo
  SkPathMeasure::getSegment
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=484002:484005

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6579450547535872


See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

### ji...@chromium.org (2017-07-05)

caryclark@, could you help triage this issue?
Please feel free to re-assign if you see fit.

Thanks!

[Monorail components: Internals>Skia]

### sh...@chromium.org (2017-07-05)

[Empty comment from Monorail migration]

### ca...@chromium.org (2017-07-05)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-07-06)

The following revision refers to this bug:
  https://skia.googlesource.com/skia/+/ae68a399cdf3d94aff28e497d5360bc288f2131d

commit ae68a399cdf3d94aff28e497d5360bc288f2131d
Author: Cary Clark <caryclark@google.com>
Date: Thu Jul 06 12:35:14 2017

protect against fuzzer

Fuzzer data may generate path without a computable
length.

R=reed@google.com
Bug: 739190
Change-Id: I052540932937f24951ce66699080b8b959fb1a46
Reviewed-on: https://skia-review.googlesource.com/21500
Reviewed-by: Mike Reed <reed@google.com>
Commit-Queue: Cary Clark <caryclark@google.com>

[modify] https://crrev.com/ae68a399cdf3d94aff28e497d5360bc288f2131d/src/core/SkPathMeasure.cpp


### cl...@chromium.org (2017-07-07)

ClusterFuzz has detected this issue as fixed in range 484582:484617.

Detailed report: https://clusterfuzz.com/testcase?key=6579450547535872

Job Type: linux_asan_chrome_mp
Crash Type: UNKNOWN READ
Crash Address: 0x60adf60d5040
Crash State:
  SkChopCubicAt
  SkPathMeasure_segTo
  SkPathMeasure::getSegment
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=484002:484005
Fixed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=484582:484617

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6579450547535872


See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2017-07-07)

ClusterFuzz testcase 6579450547535872 is verified as fixed, so closing issue.

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### sh...@chromium.org (2017-07-07)

[Empty comment from Monorail migration]

### aw...@google.com (2017-07-10)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-07-24)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-07-24)

[Empty comment from Monorail migration]

### aw...@google.com (2017-07-24)

Nice one! The VRP Panel decided to award $1,000 for this bug. A member of our finance team will be in touch to arrange payment.

### aw...@chromium.org (2017-07-24)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-08-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-08-05)

This bug requires manual review: M61 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: amineer@(Android), cmasso@(iOS), ketakid@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2017-08-06)

+ awhalley@ (Security TPM) for M61 merge review.

### aw...@chromium.org (2017-08-07)

govind@ - good for 61

### go...@chromium.org (2017-08-07)

Approving merge to M61 branch 3163 based on https://crbug.com/chromium/739190#c19. Please merge ASAP. Thank you.

### go...@chromium.org (2017-08-07)

[Empty comment from Monorail migration]

### go...@chromium.org (2017-08-08)

I don't think M61 merge is needed here. CL listed at #7 landed on July 6th and we branched M61 on July 20th. So CL is already in M61 branch.

### aw...@google.com (2017-08-08)

[Empty comment from Monorail migration]

### tk...@googlemail.com (2017-08-09)

Thanks for the award! Please credit me as "Tobias Klein (www.trapkit.de)".

### aw...@google.com (2017-09-05)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-09-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-10-13)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/739190?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40088273)*
