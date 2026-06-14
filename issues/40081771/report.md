# Heap-buffer-overflow in blink::UTF16TextIterator::consumeSlowCase

| Field | Value |
|-------|-------|
| **Issue ID** | [40081771](https://issues.chromium.org/issues/40081771) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Unknown |
| **Reporter** | cl...@chromium.org |
| **Assignee** | ea...@chromium.org |
| **Created** | 2015-04-01 |
| **Bounty** | $500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6379654651314176

Fuzzer: Miaubiz_svg_fuzzer
Job Type: Windows_asan_chrome

Crash Type: Heap-buffer-overflow READ 2
Crash Address: 0x0ce04c34
Crash State:
  blink::UTF16TextIterator::consumeSlowCase
  blink::SimpleShaper::advanceInternal<blink::UTF16TextIterator>
  blink::SimpleShaper::advance
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=windows_asan_chrome&range=323147:323171

Minimized Testcase (2.23 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96hCJDbV2XZxXQR3vqcpntLV3qY6dm8_hP-8vz9ae9zOtE2PK99jAkLF3Ho--K4FLJ3Gnr1bizFsw8hLPwHiWqTK9qqCcYoCTjp8LCzmPPKRP_fv1cpkxbl6FBBQhwaMwwGC1mxEjF_fAQpKC709Xb0mbVb6g

Filer: inferno

## Timeline

### in...@chromium.org (2015-04-01)

Author: eae@chromium.org 
Component: blink
Changelist: https://chromium.googlesource.com/chromium/blink.git/+/ae0ad1bfbf55d1c922f84ab75c82923210b38664
Time: Tue Mar 31 21:44:15 2015
Lines 213 of file SimpleShaper.cpp which potentially caused crash are changed in this cl (frame #2, "blink::SimpleShaper::advance").

File UTF16TextIterator.cpp is changed in this cl (and is part of stack frame #0, "blink::UTF16TextIterator::consumeSlowCase")
Minimum distance from crash line to modified line: 0. (file: SimpleShaper.cpp, crashed on: 213, modified: 213).

### ea...@chromium.org (2015-04-01)

[Empty comment from Monorail migration]

### js...@chromium.org (2015-04-01)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-04-01)

This medium+ severity security issue is a regression on trunk.

Please fix this asap. If you are unable to look into this soon, please revert your change.

- Your friendly ClusterFuzz

### ea...@chromium.org (2015-04-01)

Working on it and should have a fix by tomorrow.

### in...@chromium.org (2015-04-02)

[Empty comment from Monorail migration]

### bu...@chromium.org (2015-04-03)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=193061

------------------------------------------------------------------
r193061 | eae@chromium.org | 2015-04-03T01:21:08.429936Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/text/international-iteration-simple-text.html?r1=193061&r2=193060&pathrev=193061
   M http://src.chromium.org/viewvc/blink/trunk/Source/platform/fonts/UTF16TextIterator.cpp?r1=193061&r2=193060&pathrev=193061
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/text/international-iteration-simple-text-expected.txt?r1=193061&r2=193060&pathrev=193061

Fix incorrect end offset bug in UTF16TextIterator from r192854

Fix bug in UTF16TextIterator where the end of the m_characters array was
computed incorrectly resulting in the possibility of reading one element
beyond the end of the array when looking for the surrogate pair low bit.

R=pdr@chromium.org
BUG=472613
TEST=fast/text/international-iteration-simple-text.html

Review URL: https://codereview.chromium.org/1058953004
-----------------------------------------------------------------

### in...@chromium.org (2015-04-03)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-04-03)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### ti...@google.com (2015-04-08)

Merge Requested to M43 (branch 2357)

### la...@google.com (2015-04-08)

[Automated comment] Commit may have occurred before M43 branch point (4/3/2015), needs manual review.

### dx...@google.com (2015-04-08)

this is already in m43.

### ti...@google.com (2015-05-16)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-05-16)

This bug is a regression and does not impact stable. Removing incorrectly added Release-0-M43 label.

- Your friendly ClusterFuzz

### ti...@google.com (2015-05-16)

Thanks CF - you're the best.

### ti...@google.com (2015-06-14)

Congrats - $500 for this report.

We'll start payment via our new process, which should take 1-2 weeks. That 1-2 week period payment time frame starts from when you see the "reward-inprocess" label on this bug.

### ti...@google.com (2015-06-25)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-07-10)

Bulk update: removing view restriction from closed bugs.

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

This issue was migrated from crbug.com/chromium/472613?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/473049]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081771)*
