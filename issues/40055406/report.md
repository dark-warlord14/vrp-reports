# BigInt toLocaleString free invalid pointer

| Field | Value |
|-------|-------|
| **Issue ID** | [40055406](https://issues.chromium.org/issues/40055406) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>JavaScript |
| **Platforms** | Linux, Mac, Windows |
| **Reporter** | wx...@gmail.com |
| **Assignee** | ft...@chromium.org |
| **Created** | 2021-04-01 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

The following testcase crashes the latest debug build of d8.

**VERSION**  

V8: V8 version 9.1.0 (candidate)  

Operating System: Linux 64bit

**REPRODUCTION CASE**  

v1 = 'MZ-65537RUZ-65537RQZ-65537RvZ-65537RTZ-65537RdZ-65537RMZ-65537RJZ-65537ReZ-65537RpZ-65537R-Z-65537R2Z-65537R5Z-65537R6Z-65537R-2Z-65537RnZ-65537RuZ-65537RmZ';  

v2 = BigInt(1);  

v2.toLocaleString(v1);

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**

Crash State:

free(): invalid pointer  

Received signal 6

#0 \_\_GI\_raise (sig=sig@entry=6) at ../sysdeps/unix/sysv/linux/raise.c:51  

#1 0x00007f9abbc31921 in \_\_GI\_abort () at abort.c:79  

#2 0x00007f9abbc7a967 in \_\_libc\_message (action=action@entry=do\_abort, fmt=fmt@entry=0x7f9abbda7b0d "%s\n") at ../sysdeps/posix/libc\_fatal.c:181  

#3 0x00007f9abbc819da in malloc\_printerr (str=str@entry=0x7f9abbda5d08 "free(): invalid pointer") at malloc.c:5342  

#4 0x00007f9abbc88f0c in \_int\_free (have\_lock=0, p=0x7ffe8b59e198, av=0x7f9abbfdcc40 <main\_arena>) at malloc.c:4167  

#5 \_\_GI\_\_\_libc\_free (mem=0x7ffe8b59e1a8) at malloc.c:3134  

#6 0x00007f9abc82fd2d in uprv\_free\_68 (buffer=0x7ffe8b59e1a8) at ../../third\_party/icu/source/common/cmemory.cpp:99  

#7 0x00007f9abc85058b in icu\_68::Locale::init (this=0x7ffe8b59e628, localeID=0x5618e37c5550 "mz\_\_65537R\_65537RDZ\_65537REZ\_65537RJZ\_65537RMZ\_65537RPZ\_65537RQZ\_65537RTZ\_65537RUZ\_65537RVZ@z=65537r2z-65537r5z-65537r6z-65537r-2z-65537rnz-65537ruz-65537rmz", canonicalize=1 '\001') at ../../third\_party/icu/source/common/locid.cpp:1841  

#8 0x00007f9abc8523d1 in icu\_68::Locale::canonicalize (this=0x7ffe8b59e628, status=@0x7ffe8b59e464: U\_ZERO\_ERROR) at ../../third\_party/icu/source/common/locid.cpp:2132  

#9 0x00007f9abf4698fe in v8::internal::(anonymous namespace)::CanonicalizeLanguageTag (isolate=0x5618e370af30, locale\_in=...) at ../../src/objects/intl-objects.cc:794  

#10 0x00007f9abf462a7c in v8::internal::(anonymous namespace)::CanonicalizeLanguageTag (isolate=0x5618e370af30, locale\_in=...) at ../../src/objects/intl-objects.cc:844  

#11 0x00007f9abf462000 in v8::internal::Intl::CanonicalizeLocaleList (isolate=0x5618e370af30, locales=..., only\_return\_one\_result=false) at ../../src/objects/intl-objects.cc:872  

#12 0x00007f9abf4c9321 in v8::internal::JSNumberFormat::New (isolate=0x5618e370af30, map=..., locales=..., options\_obj=..., service=0x7f9abdaeb9b0 "BigInt.prototype.toLocaleString") at ../../src/objects/js-number-format.cc:827  

#13 0x00007f9abf4642bb in v8::internal::(anonymous namespace)::New[v8::internal::JSNumberFormat](javascript:void(0);) (isolate=0x5618e370af30, constructor=..., locales=..., options=..., method=0x7f9abdaeb9b0 "BigInt.prototype.toLocaleString") at ../../src/objects/intl-objects.cc:188  

#14 0x00007f9abf463ff3 in v8::internal::Intl::NumberToLocaleString (isolate=0x5618e370af30, num=..., locales=..., options=..., method=0x7f9abdaeb9b0 "BigInt.prototype.toLocaleString") at ../../src/objects/intl-objects.cc:1105  

#15 0x00007f9abecaa74e in v8::internal::Builtin\_Impl\_BigIntPrototypeToLocaleString (args=..., isolate=0x5618e370af30) at ../../src/builtins/builtins-bigint.cc:135  

#16 0x00007f9abecaa31b in v8::internal::Builtin\_BigIntPrototypeToLocaleString (args\_length=6, args\_object=0x7ffe8b5a16a0, isolate=0x5618e370af30) at ../../src/builtins/builtins-bigint.cc:126  

#17 0x00007f9abe6a3120 in Builtins\_CEntry\_Return1\_DontSaveFPRegs\_ArgvOnStack\_BuiltinExit () from /data/v8/out/Debug/libv8.so  

#18 0x00007f9abe3fd16b in Builtins\_InterpreterEntryTrampoline () from /data/v8/out/Debug/libv8.so  

#19 0x000023c775a81599 in ?? ()  

#20 0x00002ef586d46f01 in ?? ()  

#21 0x0000000600000000 in ?? ()  

#22 0x000023c775a81669 in ?? ()  

#23 0x00000f16ea38c9c9 in ?? ()  

#24 0x00002ef586d60861 in ?? ()  

#25 0x00002ef586d60861 in ?? ()  

#26 0x00000f16ea38c9c9 in ?? ()  

#27 0x00002ef586d46f01 in ?? ()  

#28 0x000023c775a81599 in ?? ()  

#29 0x0000005500000000 in ?? ()  

#30 0x00002ef586d60a09 in ?? ()  

#31 0x0000000000000000 in ?? ()

## Timeline

### [Deleted User] (2021-04-01)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-04-01)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5123019547410432.

### cl...@chromium.org (2021-04-01)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-04-02)

Detailed Report: https://clusterfuzz.com/testcase?key=5123019547410432

Fuzzer: None
Job Type: linux_asan_d8
Platform Id: linux

Crash Type: Invalid-free
Crash Address: 0x7f11d7abe930
Crash State:
  icu_68::Locale::init
  icu_68::Locale::canonicalize
  v8::internal::CanonicalizeLanguageTag
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8&range=71299:71300

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5123019547410432

The reproduce tool requires a ClusterFuzz source checkout. To prepare one, run:

git clone https://github.com/google/clusterfuzz && cd clusterfuzz && git checkout tags/reproduce-tool-stable

To reproduce this issue, run:

./reproduce.sh -t https://clusterfuzz.com/testcase-detail/5123019547410432 -b /path/to/build

Please use the GN arguments provided in this report when building the binary. If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### cl...@chromium.org (2021-04-02)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Blink>JavaScript]

### cl...@chromium.org (2021-04-02)

Automatically assigning owner based on suspected regression changelist https://chromium.googlesource.com/v8/v8/+/fbfbc5c28b02b07b0679816f1a1f1cd701048014 ([intl] Validate locale by LocaleBuilder).

If this is incorrect, please let us know why and apply the Test-Predator-Wrong-CLs label. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### cl...@chromium.org (2021-04-07)

[Empty comment from Monorail migration]

### ad...@google.com (2021-04-14)

Please could you temporarily avoid including any .js test code in the CLs for this - speak to hablich@ with questions.

### ft...@chromium.org (2021-04-20)

[Empty comment from Monorail migration]

### ft...@chromium.org (2021-04-21)

can be reproduce after 69-1 landing. Could be caused by https://unicode-org.atlassian.net/browse/ICU-21587
trying https://github.com/unicode-org/icu/pull/1698 next

### ft...@chromium.org (2021-04-21)

[Empty comment from Monorail migration]

### ft...@chromium.org (2021-04-21)

yes, it is fixed by https://github.com/unicode-org/icu/pull/1698 

### ft...@chromium.org (2021-04-21)

[Empty comment from Monorail migration]

### ft...@chromium.org (2021-04-21)

Google internal fuzzer found ICU problem for https://unicode-org.atlassian.net/browse/ICU-21587 in March 27 2021 which trigger our work to fix it in https://github.com/unicode-org/icu/pull/1698

### ft...@chromium.org (2021-04-21)

related google internal bugs are 182675373 182960178 183794356 183861617 183887128
which were filed March 13, March 16, March 26, March 27 and March 28 . 


### [Deleted User] (2021-04-21)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2021-04-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/deps/icu/+/d25bdc013cb0d0d9b1b7c53beb1ab2a30323341c

commit d25bdc013cb0d0d9b1b7c53beb1ab2a30323341c
Author: Frank Tang <ftang@chromium.org>
Date: Wed Apr 21 01:31:40 2021

Fix crash caused by locale assign/move operators

https://unicode-org.atlassian.net/browse/ICU-21587
https://bugs.chromium.org/p/chromium/issues/detail?id=1194899

Bug: chromium:1194899
Change-Id: I39edcf04f43c52f6937365e50f521fab3679568b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/deps/icu/+/2842864
Reviewed-by: Jungshik Shin <jshin@chromium.org>

[modify] https://crrev.com/d25bdc013cb0d0d9b1b7c53beb1ab2a30323341c/README.chromium
[add] https://crrev.com/d25bdc013cb0d0d9b1b7c53beb1ab2a30323341c/patches/locid_operators.patch
[modify] https://crrev.com/d25bdc013cb0d0d9b1b7c53beb1ab2a30323341c/source/common/locid.cpp


### gi...@appspot.gserviceaccount.com (2021-04-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/deps/icu/+/7e128ffcd0919c956962366c7347cf4633785339

commit 7e128ffcd0919c956962366c7347cf4633785339
Author: Frank Tang <ftang@chromium.org>
Date: Wed Apr 21 01:31:40 2021

[m90] Fix crash caused by locale assign/move operators

https://unicode-org.atlassian.net/browse/ICU-21587
https://bugs.chromium.org/p/chromium/issues/detail?id=1194899

Bug: chromium:1194899
Change-Id: I39edcf04f43c52f6937365e50f521fab3679568b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/deps/icu/+/2842864
Reviewed-by: Jungshik Shin <jshin@chromium.org>
(cherry picked from commit d25bdc013cb0d0d9b1b7c53beb1ab2a30323341c)
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/deps/icu/+/2847140
Reviewed-by: Frank Tang <ftang@chromium.org>

[modify] https://crrev.com/7e128ffcd0919c956962366c7347cf4633785339/README.chromium
[add] https://crrev.com/7e128ffcd0919c956962366c7347cf4633785339/patches/locid_operators.patch
[modify] https://crrev.com/7e128ffcd0919c956962366c7347cf4633785339/source/common/locid.cpp


### gi...@appspot.gserviceaccount.com (2021-04-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/5846c2ac22f397073eeb818bf43a9c14756e5445

commit 5846c2ac22f397073eeb818bf43a9c14756e5445
Author: Frank Tang <ftang@chromium.org>
Date: Thu Apr 22 19:22:07 2021

Roll ICU to fix crash

Upstream bug: https://unicode-org.atlassian.net/browse/ICU-21587
Upstream PR: https://bugs.chromium.org/p/chromium/issues/detail?id=1194899

https://chromium.googlesource.com/chromium/deps/icu.git/+log/7e7574bd..d25bdc01

Security team request NOT to include test in the CL.

Bug: chromium:1194899
Change-Id: I961e995a56fdb8181249558a536acc85f8980f60
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2846020
Reviewed-by: Jungshik Shin <jshin@chromium.org>
Commit-Queue: Frank Tang <ftang@chromium.org>
Cr-Commit-Position: refs/heads/master@{#875299}

[modify] https://crrev.com/5846c2ac22f397073eeb818bf43a9c14756e5445/DEPS


### gi...@appspot.gserviceaccount.com (2021-04-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/deps/icu/+/690d11b7d9856ef8cb712f93e65a2f11125511f1

commit 690d11b7d9856ef8cb712f93e65a2f11125511f1
Author: Frank Tang <ftang@chromium.org>
Date: Wed Apr 21 01:31:40 2021

[m91] Fix crash caused by locale assign/move operators

https://unicode-org.atlassian.net/browse/ICU-21587
https://bugs.chromium.org/p/chromium/issues/detail?id=1194899

Bug: chromium:1194899
Change-Id: I39edcf04f43c52f6937365e50f521fab3679568b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/deps/icu/+/2842864
Reviewed-by: Jungshik Shin <jshin@chromium.org>
(cherry picked from commit d25bdc013cb0d0d9b1b7c53beb1ab2a30323341c)
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/deps/icu/+/2845799
Reviewed-by: Frank Tang <ftang@chromium.org>

[modify] https://crrev.com/690d11b7d9856ef8cb712f93e65a2f11125511f1/README.chromium
[add] https://crrev.com/690d11b7d9856ef8cb712f93e65a2f11125511f1/patches/locid_operators.patch
[modify] https://crrev.com/690d11b7d9856ef8cb712f93e65a2f11125511f1/source/common/locid.cpp


### ft...@chromium.org (2021-04-22)

Took out incorrect merged-merge labels. Nothing merge into m90 or m91 branch yet. These two are landed into branch prepare for m90 and m91 in the ICU branch. These were not yet merged into m90 or m91 yet

The real CLs to merge for m90 and m91 are
For m90 on refs/branch-heads/4430
https://chromium-review.googlesource.com/c/chromium/src/+/2847033

For m91 on refs/branch-heads/4472
https://chromium-review.googlesource.com/c/chromium/src/+/2846077  

We are waiting for the trunk and daily get out and verify that before put up merge request labels

### ft...@chromium.org (2021-04-23)

Fix verified in 92.0.4486.0

### ft...@chromium.org (2021-04-23)

[Empty comment from Monorail migration]

### ft...@chromium.org (2021-04-23)

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines

YES

2. Links to the CLs you are requesting to merge.
For m90 on refs/branch-heads/4430
https://chromium-review.googlesource.com/c/chromium/src/+/2847033

For m91 on refs/branch-heads/4472
https://chromium-review.googlesource.com/c/chromium/src/+/2846077  

3. Has the change landed and been verified on ToT?
YES Land on  Thu, Apr 22, 2021, 12:23 PM PDT as
https://chromium-review.googlesource.com/c/chromium/src/+/2846020

https://chromium.googlesource.com/chromium/src/+/5846c2ac22f397073eeb818bf43a9c14756e5445

Security team request NOT to include test in the CL.

The test is 
`
v1 = 'MZ-65537RUZ-65537RQZ-65537RvZ-65537RTZ-65537RdZ-65537RMZ-65537RJZ-65537ReZ-65537RpZ-65537R-Z-65537R2Z-65537R5Z-65537R6Z-65537R-2Z-65537RnZ-65537RuZ-65537RmZ';
v2 = BigInt(1);
v2.toLocaleString(v1);
`
Copy and paste above and m90 and m91 will crash

Verify the fix in 92.0.4486.0 Won't crash

4. Does this change need to be merged into other active release branches (M-1, M+1)?

Both m91 and m90

5. Why are these changes required in this milestone after branch?

Security issue

6. Is this a new feature?

NO

7. If it is a new feature, is it behind a flag using finch?
N/A

### sr...@google.com (2021-04-23)

+adetaylor@ to review 

### ad...@google.com (2021-04-23)

Approving merge to M91, branch 4472. We should wait for more bake time before merging to M90.

Please mark as fixed: https://chromium.googlesource.com/chromium/src/+/master/docs/security/security-labels.md#TOC-Merge-labels

### ft...@chromium.org (2021-04-23)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-04-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/3d9c4b0096b88097e16576f8d8b7617ea9e8219f

commit 3d9c4b0096b88097e16576f8d8b7617ea9e8219f
Author: Frank Tang <ftang@chromium.org>
Date: Fri Apr 23 21:41:12 2021

[m91] Roll ICU to Fix crash caused by locale assign/move operators

https://unicode-org.atlassian.net/browse/ICU-21587
https://bugs.chromium.org/p/chromium/issues/detail?id=1194899

https://chromium.googlesource.com/chromium/deps/icu.git/+log/81d6568..690d11b7

Bug: chromium:1194899
Change-Id: I670b1f69d6777776beef74e54d1931f7543b08a7
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2846077
Reviewed-by: Jungshik Shin <jshin@chromium.org>
Commit-Queue: Frank Tang <ftang@chromium.org>
Cr-Commit-Position: refs/branch-heads/4472@{#370}
Cr-Branched-From: 3d60439cfb36485e76a1c5bb7f513d3721b20da1-refs/heads/master@{#870763}

[modify] https://crrev.com/3d9c4b0096b88097e16576f8d8b7617ea9e8219f/DEPS


### [Deleted User] (2021-04-24)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-24)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-04-27)

ClusterFuzz testcase 5123019547410432 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8&range=74190:74191

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### am...@google.com (2021-04-28)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ft...@chromium.org (2021-04-28)

Somehow the test case is still crashed in 91.0.4472.27
Could be caused by some other bug fixed in icu 69-1 (m91 is on 68-1)

### am...@google.com (2021-04-30)

[Empty comment from Monorail migration]

### ad...@google.com (2021-05-03)

ftang@ please could you look into https://crbug.com/chromium/1194899#c33?

### ad...@google.com (2021-05-03)

(I realize now, of course, that you actually _made_ https://crbug.com/chromium/1194899#c33! But either way, it seems the bug should be Assigned not Verified. Thanks!)

### ft...@chromium.org (2021-05-05)

It is fixed and verify in m92, which is based on ICU 69.
After I apply the PR to m91, which is based on ICU 68, the cp PR is not enough to fix the crash.


### ad...@chromium.org (2021-05-05)

OK. Do you think it would be easy to identify what fixed this in ICU 69? If so, please do that, so we can consider merging the fix back to M91 and maybe M90. However, if it's hard to identify the specific fix, then maybe this can wait to be fixed in M92.

### ft...@chromium.org (2021-05-05)

The root cause is somehow we didn't cp https://github.com/unicode-org/icu/pull/1656/files into m90 or m91.



### ft...@chromium.org (2021-05-05)

fix for m91 in https://chromium-review.googlesource.com/c/chromium/src/+/2874872

### [Deleted User] (2021-05-05)

This bug requires manual review: DEPS changes referenced in bugdroid comments.
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
Owners: benmason@(Android), bindusuvarna@(iOS), marinakz@(ChromeOS), pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ft...@chromium.org (2021-05-05)

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines

YES

2. Links to the CLs you are requesting to merge.

For m91 on refs/branch-heads/4472
https://chromium-review.googlesource.com/c/chromium/src/+/2874872

3. Has the change landed and been verified on ToT?
It was already part of trunk for a while. Came with ICU69-1

Security team request NOT to include test in the CL.

The test is 
`
v1 = 'MZ-65537RUZ-65537RQZ-65537RvZ-65537RTZ-65537RdZ-65537RMZ-65537RJZ-65537ReZ-65537RpZ-65537R-Z-65537R2Z-65537R5Z-65537R6Z-65537R-2Z-65537RnZ-65537RuZ-65537RmZ';
v2 = BigInt(1);
v2.toLocaleString(v1);
`
Copy and paste above and m90 and m91 will crash

Verify the fix in 92.0.4486.0 Won't crash

4. Does this change need to be merged into other active release branches (M-1, M+1)?

Both m91 and m90

5. Why are these changes required in this milestone after branch?

Security issue

6. Is this a new feature?

NO

7. If it is a new feature, is it behind a flag using finch?
N/A

### ad...@google.com (2021-05-06)

Discussed with ftang yesterday - approving merge of the other half of the fix to M91, branch 4472.

### gi...@appspot.gserviceaccount.com (2021-05-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b3e7d3bc1c8850e1fab5adb5f095a1c163870579

commit b3e7d3bc1c8850e1fab5adb5f095a1c163870579
Author: Frank Tang <ftang@chromium.org>
Date: Fri May 07 01:15:35 2021

[m91] Roll ICU w/ fix of invalid free by long locale name

https://chromium.googlesource.com/chromium/deps/icu.git/+log/690d11b7..6266caed

Bug: 1194899
Change-Id: Ic929c7ea72c9cde45c240dd1913a0963be44468f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2874872
Reviewed-by: Frank Tang <ftang@chromium.org>
Reviewed-by: Jungshik Shin <jshin@chromium.org>
Commit-Queue: Frank Tang <ftang@chromium.org>
Cr-Commit-Position: refs/branch-heads/4472@{#816}
Cr-Branched-From: 3d60439cfb36485e76a1c5bb7f513d3721b20da1-refs/heads/master@{#870763}

[modify] https://crrev.com/b3e7d3bc1c8850e1fab5adb5f095a1c163870579/DEPS


### ft...@chromium.org (2021-05-07)

[Empty comment from Monorail migration]

### ft...@chromium.org (2021-05-12)

Verified on Version 91.0.4472.57 (Official Build) beta (x86_64)


### ad...@google.com (2021-05-21)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-05-24)

[Empty comment from Monorail migration]

### am...@google.com (2021-05-24)

[Empty comment from Monorail migration]

### wx...@gmail.com (2021-05-25)

Thanks! Please credit to leogan, nocma, cheneyxu of WeChat Open Platform Security Team.

### ja...@google.com (2021-05-26)

[Empty comment from Monorail migration]

### ja...@google.com (2021-05-27)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-27)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-05-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/deps/icu/+/95e145fcc72edac4cb1f31c7d1816b2e46eeeb6f

commit 95e145fcc72edac4cb1f31c7d1816b2e46eeeb6f
Author: Frank Tang <ftang@chromium.org>
Date: Wed Apr 21 01:31:40 2021

[86-LTS] Fix crash caused by locale assign/move operators

https://unicode-org.atlassian.net/browse/ICU-21587
https://bugs.chromium.org/p/chromium/issues/detail?id=1194899

Bug: chromium:1194899
Change-Id: I39edcf04f43c52f6937365e50f521fab3679568b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/deps/icu/+/2842864
Reviewed-by: Jungshik Shin <jshin@chromium.org>
(cherry picked from commit d25bdc013cb0d0d9b1b7c53beb1ab2a30323341c)
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/deps/icu/+/2919701
Reviewed-by: Victor-Gabriel Savu <vsavu@google.com>
Reviewed-by: Frank Tang <ftang@chromium.org>

[modify] https://crrev.com/95e145fcc72edac4cb1f31c7d1816b2e46eeeb6f/README.chromium
[add] https://crrev.com/95e145fcc72edac4cb1f31c7d1816b2e46eeeb6f/patches/locid_operators.patch
[modify] https://crrev.com/95e145fcc72edac4cb1f31c7d1816b2e46eeeb6f/source/common/locid.cpp


### gi...@appspot.gserviceaccount.com (2021-05-31)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/4174427c03fbbea4191306641d8786f9344806e3

commit 4174427c03fbbea4191306641d8786f9344806e3
Author: Jana Grill <janagrill@google.com>
Date: Mon May 31 15:37:23 2021

[86-LTS] Roll ICU to fix crash

Upstream bug: https://unicode-org.atlassian.net/browse/ICU-21587
Upstream PR: https://bugs.chromium.org/p/chromium/issues/detail?id=1194899

https://chromium.googlesource.com/chromium/deps/icu.git/+/95e145fcc72edac4cb1f31c7d1816b2e46eeeb6f

Bug: chromium:1194899
Change-Id: Ie8429bdf8b68e2ec92fdfccfa06e161db707ccb2
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2925595
Reviewed-by: Victor-Gabriel Savu <vsavu@google.com>
Commit-Queue: Jana Grill <janagrill@google.com>
Cr-Commit-Position: refs/branch-heads/4240@{#1653}
Cr-Branched-From: f297677702651916bbf65e59c0d4bbd4ce57d1ee-refs/heads/master@{#800218}

[modify] https://crrev.com/4174427c03fbbea4191306641d8786f9344806e3/DEPS


### gi...@appspot.gserviceaccount.com (2021-06-01)

The following revision refers to this bug:
  https://webrtc.googlesource.com/src/+/6b79468a0cb1d99d0e684e590053b57441145d75

commit 6b79468a0cb1d99d0e684e590053b57441145d75
Author: Mirko Bonadei <mbonadei@webrtc.org>
Date: Mon May 31 14:47:46 2021

[Merge M86] Roll ICU to fix crash

Upstream bug: https://unicode-org.atlassian.net/browse/ICU-21587
Upstream PR: https://bugs.chromium.org/p/chromium/issues/detail?id=1194899

https://chromium.googlesource.com/chromium/deps/icu.git/+/95e145fcc72edac4cb1f31c7d1816b2e46eeeb6f

TBR=titovartem@webrtc.org

No-Try: True
No-Presubmit: True
Bug: chromium:1194899
Change-Id: I1258a4c90fd7e6a7dee18459fa91b0e2ce258c16
Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/220924
Reviewed-by: Mirko Bonadei <mbonadei@webrtc.org>
Reviewed-by: Artem Titov <titovartem@webrtc.org>
Commit-Queue: Mirko Bonadei <mbonadei@webrtc.org>
Cr-Commit-Position: refs/branch-heads/4240@{#20}
Cr-Branched-From: 93a9d19d4eb53b3f4fb4d22e6c54f2e2824437eb-refs/heads/master@{#31969}

[modify] https://crrev.com/6b79468a0cb1d99d0e684e590053b57441145d75/DEPS


### gi...@appspot.gserviceaccount.com (2021-06-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/391e5a0a0c0bc1cbde7aa886c553210605e8d7e6

commit 391e5a0a0c0bc1cbde7aa886c553210605e8d7e6
Author: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
Date: Tue Jun 01 07:37:04 2021

Roll WebRTC from 1627015c8408 to 6b79468a0cb1 (1 revision)

https://webrtc.googlesource.com/src.git/+log/1627015c8408..6b79468a0cb1

2021-06-01 mbonadei@webrtc.org [Merge M86] Roll ICU to fix crash

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/webrtc-chromium-lts
Please CC cros-lts-team@google.com on the revert to ensure that a human
is aware of the problem.

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/master/autoroll/README.md

Bug: chromium:1194899
Tbr: cros-lts-team@google.com
Change-Id: Ic498aa26d25e6e3930f92f8508c5f9fbdadbc5ce
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2929896
Commit-Queue: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/4240@{#1654}
Cr-Branched-From: f297677702651916bbf65e59c0d4bbd4ce57d1ee-refs/heads/master@{#800218}

[modify] https://crrev.com/391e5a0a0c0bc1cbde7aa886c553210605e8d7e6/DEPS


### ja...@google.com (2021-06-01)

[Empty comment from Monorail migration]

### su...@google.com (2021-06-01)

[Empty comment from Monorail migration]

### am...@google.com (2021-06-07)

[Empty comment from Monorail migration]

### vs...@google.com (2021-06-14)

[Empty comment from Monorail migration]

### gi...@google.com (2021-06-15)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-06-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b0fa78c8430045c8126c7552c4d0bc9559a5ed66

commit b0fa78c8430045c8126c7552c4d0bc9559a5ed66
Author: Frank Tang <ftang@chromium.org>
Date: Tue Jun 15 16:40:25 2021

[m90] Roll ICU to Fix crash caused by locale assign/move operators

https://unicode-org.atlassian.net/browse/ICU-21587
https://bugs.chromium.org/p/chromium/issues/detail?id=1194899

https://chromium.googlesource.com/chromium/deps/icu.git/+log/e05b663d..7e128ffc

Bug: chromium:1194899
Change-Id: I15f0bea5be7161c97832ba45de6b513351c5be3d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2847033
Owners-Override: Victor-Gabriel Savu <vsavu@google.com>
Reviewed-by: Victor-Gabriel Savu <vsavu@google.com>
Reviewed-by: Achuith Bhandarkar <achuith@chromium.org>
Commit-Queue: Frank Tang <ftang@chromium.org>
Cr-Commit-Position: refs/branch-heads/4430@{#1524}
Cr-Branched-From: e5ce7dc4f7518237b3d9bb93cccca35d25216cbe-refs/heads/master@{#857950}

[modify] https://crrev.com/b0fa78c8430045c8126c7552c4d0bc9559a5ed66/DEPS


### ja...@google.com (2021-07-28)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-21)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1194899?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40055406)*
