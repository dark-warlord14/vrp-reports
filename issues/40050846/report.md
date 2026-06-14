# sqlite3_shadow_table_fuzzer: ASSERT: nDoclist>0

| Field | Value |
|-------|-------|
| **Issue ID** | [40050846](https://issues.chromium.org/issues/40050846) |
| **Status** | Accepted |
| **Severity** | S4-Minimal |
| **Priority** | P3 |
| **Component** | Internals>Storage |
| **Platforms** | Linux |
| **Reporter** | cl...@chromium.org |
| **Assignee** | hu...@chromium.org |
| **Created** | 2019-11-30 |
| **Bounty** | $3,000.00 |

## Description

Detailed Report: https://clusterfuzz.com/testcase?key=5201388652855296

Fuzzing Engine: libFuzzer
Fuzz Target: sqlite3_shadow_table_fuzzer
Job Type: libfuzzer_chrome_asan_debug
Platform Id: linux

Crash Type: ASSERT
Crash Address: 
Crash State:
  nDoclist>0
  fts3SegWriterAdd
  fts3SegmentMerge
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=libfuzzer_chrome_asan_debug&range=719098:719109

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5201388652855296

Issue filed automatically.

See https://chromium.googlesource.com/chromium/src/+/master/testing/libfuzzer/reproducing.md for instructions on reproducing this bug locally.

## Timeline

### cl...@chromium.org (2019-11-30)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Internals>Storage]

### cl...@chromium.org (2019-11-30)

Automatically adding ccs based on OWNERS file / target commit history.

If this is incorrect, please add the ClusterFuzz-Wrong label.

### le...@gmail.com (2019-12-01)

Hi I have a question, will the same corpus run on release build too or is it needed to add security restrict tag? 

assert in sqlite is more like DCHECK() and this might be a security problem in release chrome build. 

(I did't have the permission to clusterfuzz.com yet so I am not sure about it, I will try to send a request to the email you've mentioned on clusterfuzz.com)

### mm...@chromium.org (2019-12-02)

> will the same corpus run on release build too or is it needed to add security restrict tag? 


Yes, it will. Let me mark it as security issue just to be extra safe.

### mm...@chromium.org (2019-12-02)

Adding appropriate labels for the external fuzzer contribution.

### sh...@chromium.org (2019-12-03)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aj...@google.com (2020-04-15)

huangdarwin@ could you suggest an owner for this issue, or clarify if it should be a security bug?

### hu...@chromium.org (2020-04-16)

Thanks, I'll take this.

### hu...@chromium.org (2020-04-16)

Dr. Hipp and Daniel, please take a look? Test case and stack trace below.

Test Case:

CREATE VIRTUAL TABLE f USING fts3(a,b);
INSERT INTO f_segdir VALUES (28,0,0,0,'0 0',x'00');
INSERT INTO f_segdir VALUES (0,241,0,0,'0 0',x'0001000030310000f1');
INSERT INTO f VALUES (0,x'00');

Stack Trace:

sqlite3_shadow_table_fuzzer: ../../third_party/sqlite/src/amalgamation/sqlite3.c:176951: int fts3SegWriterAdd(Fts3Table *, SegmentWriter **, int, const char *, int, const char *, int): Assertion `nDoclist>0' failed.
AddressSanitizer:DEADLYSIGNAL
=================================================================
==3323121==ERROR: AddressSanitizer: ABRT on unknown address 0x05390032b4f1 (pc 0x7f6d14a7a428 bp 0x7f6d15fc5960 sp 0x7ffc4968afa8 T0)
    #0 0x7f6d14a7a428 in gsignal /build/glibc-LK5gWL/glibc-2.23/signal/../sysdeps/unix/sysv/linux/raise.c:54
    #1 0x7f6d14a7c029 in abort /build/glibc-LK5gWL/glibc-2.23/stdlib/abort.c:89
    #2 0x7f6d14a72bd6 in __assert_fail_base /build/glibc-LK5gWL/glibc-2.23/assert/assert.c:92
    #3 0x7f6d14a72c81 in __assert_fail /build/glibc-LK5gWL/glibc-2.23/assert/assert.c:101
    #4 0x7f6d1647acb7 in fts3SegWriterAdd third_party/sqlite/src/amalgamation/sqlite3.c:176951:3
    #5 0x7f6d1647834f in fts3SegmentMerge third_party/sqlite/src/amalgamation/sqlite3.c:177877:10
    #6 0x7f6d1647966b in fts3AllocateSegdirIdx third_party/sqlite/src/amalgamation/sqlite3.c:175771:12
    #7 0x7f6d16477c5b in fts3SegmentMerge third_party/sqlite/src/amalgamation/sqlite3.c:177858:10
    #8 0x7f6d16476c93 in sqlite3Fts3PendingTermsFlush third_party/sqlite/src/amalgamation/sqlite3.c:177913:10
    #9 0x7f6d16439204 in fts3SyncMethod third_party/sqlite/src/amalgamation/sqlite3.c:167950:8
    #10 0x7f6d1610fc17 in sqlite3VtabSync third_party/sqlite/src/amalgamation/sqlite3.c:138770:12
    #11 0x7f6d16109791 in vdbeCommit third_party/sqlite/src/amalgamation/sqlite3.c:79920:8
    #12 0x7f6d161060a6 in sqlite3VdbeHalt third_party/sqlite/src/amalgamation/sqlite3.c:80385:16
    #13 0x7f6d16126251 in sqlite3VdbeExec third_party/sqlite/src/amalgamation/sqlite3.c:85959:8
    #14 0x7f6d1602b0e1 in sqlite3Step third_party/sqlite/src/amalgamation/sqlite3.c:83200:10
    #15 0x7f6d1600ed43 in sqlite3_step third_party/sqlite/src/amalgamation/sqlite3.c:83265:16
    #16 0x7f6d16040337 in sqlite3_exec third_party/sqlite/src/amalgamation/sqlite3.c:122070:12
    #17 0x55c2f28d7750 in RunSqlQuery(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> >&, int*) third_party/sqlite/fuzz/shadow_table_fuzzer.cc:106:3

### da...@gmail.com (2020-04-18)

Thanks for this report. Now fixed here:

  https://sqlite.org/src/info/cb772b7a8fb53694

Dan.

### hu...@chromium.org (2020-04-27)

Note that I’ll be cherry-picking [1] instead of [2], as [1] is the original change on top of trunk, whereas [2] was a merge. 

[1]: https://sqlite.org/src/info/a9ec8c8f80a59bad
[2]: https://sqlite.org/src/info/cb772b7a8fb53694 

### hu...@chromium.org (2020-04-27)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-04-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/deps/sqlite/+/91efabc6ae8e66b6614d8d0e3f9574bd4cf6f5c3

commit 91efabc6ae8e66b6614d8d0e3f9574bd4cf6f5c3
Author: Darwin Huang <huangdarwin@chromium.org>
Date: Sat Apr 25 09:26:31 2020

Improve corruption detection in fts3 shadow tables earlier in order to prevent an assert() from failing.

Backports https://sqlite.org/src/info/a9ec8c8f80a59bad

FossilOrigin-Name: a9ec8c8f80a59badabb0afdb4189f0fd2934f936530d4151de395b3a7e7c1f1f
(cherry picked from commit 7576a68c8c9281288ab6ddc25f202d0f3c0ee05e)
Bug: 1029569
Change-Id: Ib00411451a3db609af81b27694d34ea33238f50e
[modify] https://crrev.com/91efabc6ae8e66b6614d8d0e3f9574bd4cf6f5c3/test/fts4aa.test
[modify] https://crrev.com/91efabc6ae8e66b6614d8d0e3f9574bd4cf6f5c3/amalgamation_dev/sqlite3.h
[modify] https://crrev.com/91efabc6ae8e66b6614d8d0e3f9574bd4cf6f5c3/test/fts3corrupt4.test
[modify] https://crrev.com/91efabc6ae8e66b6614d8d0e3f9574bd4cf6f5c3/amalgamation_dev/sqlite3.c
[modify] https://crrev.com/91efabc6ae8e66b6614d8d0e3f9574bd4cf6f5c3/manifest
[modify] https://crrev.com/91efabc6ae8e66b6614d8d0e3f9574bd4cf6f5c3/amalgamation/sqlite3.c
[modify] https://crrev.com/91efabc6ae8e66b6614d8d0e3f9574bd4cf6f5c3/amalgamation/sqlite3.h
[modify] https://crrev.com/91efabc6ae8e66b6614d8d0e3f9574bd4cf6f5c3/ext/fts3/fts3_write.c


### [Deleted User] (2020-04-28)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-04-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/efc16ba16aba1227558a800ec4edd7049ab4c232

commit efc16ba16aba1227558a800ec4edd7049ab4c232
Author: Darwin Huang <huangdarwin@chromium.org>
Date: Wed Apr 29 02:19:40 2020

Roll src/third_party/sqlite/src/ 15401f78a..3478eafd0 (2 commits)

https://chromium.googlesource.com/chromium/deps/sqlite.git/+log/15401f78a107..3478eafd05e3

$ git log 15401f78a..3478eafd0 --date=short --no-merges --format='%ad %ae %s'
2020-04-25 huangdarwin Fix an integer overflow in fts3 causing a usan error.
2020-04-25 huangdarwin Improve corruption detection in fts3 shadow tables earlier in order to prevent an assert() from failing.

Created with:
  roll-dep src/third_party/sqlite/src

Bug: 1029569, 1072736
Change-Id: I9b71b4dccefae08e4de98514ca31d2a8901f05ab
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2171677
Reviewed-by: Chris Mumford <cmumford@google.com>
Commit-Queue: Darwin Huang <huangdarwin@chromium.org>
Cr-Commit-Position: refs/heads/master@{#763676}

[modify] https://crrev.com/efc16ba16aba1227558a800ec4edd7049ab4c232/DEPS


### cl...@chromium.org (2020-04-29)

ClusterFuzz testcase 5201388652855296 is verified as fixed in https://clusterfuzz.com/revisions?job=libfuzzer_chrome_asan_debug&range=763664:763682

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### [Deleted User] (2020-04-30)

[Empty comment from Monorail migration]

### na...@google.com (2020-05-14)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-05-14)

Congrats! The Panel decided to award $2,000 + $1,000 fuzzing bonus for this report. 


### ad...@google.com (2020-07-13)

[Empty comment from Monorail migration]

### [Deleted User] (2020-08-05)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2020-09-03)

[Empty comment from Monorail migration]

### is...@google.com (2020-09-03)

This issue was migrated from crbug.com/chromium/1029569?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40050846)*
