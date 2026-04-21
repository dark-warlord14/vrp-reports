# Security:  heap-use-after-free in libavif when decode the crafted avif file.

| Field | Value |
|-------|-------|
| **Issue ID** | [40945359](https://issues.chromium.org/issues/40945359) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Internals>Images>Codecs |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | me...@gmail.com |
| **Assignee** | vi...@google.com |
| **Created** | 2023-11-23 |
| **Bounty** | $7,000.00 |

## Description

**VULNERABILITY DETAILS**

heap-use-after-free in libavif when decode the crafted avif file.

I just open it in 121.0.6144.0 chromium build with asan, and can make a crash. you can see the crash in the image attached.

**VERSION**

latest libavif version

Since the chromium adopt the libavif as the codec to the avif format, this crash or infomation leak may also happened on the chrome when decode the avif file.

**REPRODUCTION CASE**

Step 1: build libavif

```
git clone https://chromium.googlesource.com/external/github.com/AOMediaCodec/libavif  
cd libavif  
mkdir build && cd build  
CC="gcc -fsanitize=address" CXX="g++ -fsanitize=address" cmake -DCMAKE_BUILD_TYPE=Debug -DAVIF_BUILD_APPS=ON ..  
make -j  

```

Step 2: test poc  

./avifdec poc test.jpg

Then :

==2251562==ERROR: AddressSanitizer: heap-use-after-free on address 0x61c0000000fc at pc 0x7fc37cacbcbc bp 0x7fffc40ee0b0 sp 0x7fffc40ee0a0  

READ of size 4 at 0x61c0000000fc thread T0  

#0 0x7fc37cacbcbb in avifDecoderReset libavif/src/read.c:4904  

#1 0x7fc37cac5b37 in avifDecoderParse libavif/src/read.c:4125  

#2 0x555d1a7f7680 in main libavif/apps/avifdec.c:339  

#3 0x7fc37b829d8f in \_\_libc\_start\_call\_main ../sysdeps/nptl/libc\_start\_call\_main.h:58  

#4 0x7fc37b829e3f in \_\_libc\_start\_main\_impl ../csu/libc-start.c:392  

#5 0x555d1a7f5554 in \_start (libavif/build/avifdec+0xb554)

0x61c0000000fc is located 124 bytes inside of 1792-byte region [0x61c000000080,0x61c000000780)  

freed by thread T0 here:  

#0 0x7fc37c0b4537 in \_\_interceptor\_free ../../../../src/libsanitizer/asan/asan\_malloc\_linux.cpp:127  

#1 0x7fc37caa73ae in avifFree libavif/src/mem.c:17  

#2 0x7fc37caeb8bd in avifArrayPush libavif/src/utils.c:115  

#3 0x7fc37caabd20 in avifMetaFindOrCreateItem libavif/src/read.c:798  

#4 0x7fc37cac7689 in avifMetaFindAlphaItem libavif/src/read.c:4343  

#5 0x7fc37caca1dc in avifDecoderReset libavif/src/read.c:4747  

#6 0x7fc37cac5b37 in avifDecoderParse libavif/src/read.c:4125  

#7 0x555d1a7f7680 in main libavif/apps/avifdec.c:339  

#8 0x7fc37b829d8f in \_\_libc\_start\_call\_main ../sysdeps/nptl/libc\_start\_call\_main.h:58

previously allocated by thread T0 here:  

#0 0x7fc37c0b4887 in \_\_interceptor\_malloc ../../../../src/libsanitizer/asan/asan\_malloc\_linux.cpp:145  

#1 0x7fc37caa7390 in avifAlloc libavif/src/mem.c:12  

#2 0x7fc37caeb5f3 in avifArrayCreate libavif/src/utils.c:93  

#3 0x7fc37caab9a1 in avifMetaCreate libavif/src/read.c:752  

#4 0x7fc37caabf27 in avifDecoderDataCreate libavif/src/read.c:864  

#5 0x7fc37cac528a in avifDecoderParse libavif/src/read.c:4074  

#6 0x555d1a7f7680 in main libavif/apps/avifdec.c:339  

#7 0x7fc37b829d8f in \_\_libc\_start\_call\_main ../sysdeps/nptl/libc\_start\_call\_main.h:58

SUMMARY: AddressSanitizer: heap-use-after-free libavif/src/read.c:4904 in avifDecoderReset

**CREDIT INFORMATION**  

Reporter credit: [Fudan University](https://secsys.fudan.edu.cn/)

## Attachments

- [poc3.avif](attachments/poc3.avif) (application/octet-stream, 635 B)
- [crash.jpg](attachments/crash.jpg) (image/jpeg, 112.7 KB)

## Timeline

### [Deleted User] (2023-11-23)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-11-24)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6644769468383232.

### cl...@chromium.org (2023-11-25)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-11-25)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Internals>Images>Codecs]

### dc...@chromium.org (2023-11-25)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-11-26)

Detailed Report: https://clusterfuzz.com/testcase?key=6644769468383232

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x51c0000030fc
Crash State:
  avifDecoderReset
  avifDecoderParse
  blink::AVIFImageDecoder::UpdateDemuxer
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1147980:1148001

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6644769468383232

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### [Deleted User] (2023-11-26)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### wt...@google.com (2023-11-27)

[Empty comment from Monorail migration]

### wt...@google.com (2023-11-27)

[Empty comment from Monorail migration]

### vi...@google.com (2023-11-27)

I can reproduce this locally. Unfortunately this bug is very similar to crbug.com/1501770.

Upstream fix is here: https://github.com/AOMediaCodec/libavif/pull/1808.

Once that is merged, i will prepare the chromium DEPS update and cherry-picks to all the necessary branches.

### wt...@google.com (2023-11-27)

[Empty comment from Monorail migration]

### vi...@google.com (2023-11-28)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-11-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/d4c56a954852f77959ba6426e3b37f0865abd4c6

commit d4c56a954852f77959ba6426e3b37f0865abd4c6
Author: Vignesh Venkatasubramanian <vigneshv@google.com>
Date: Wed Nov 29 00:53:44 2023

Roll src/third_party/libavif/src/ f55cdaa90..784515364 (5 commits)

https://chromium.googlesource.com/external/github.com/AOMediaCodec/libavif.git/+log/f55cdaa902bf..7845153645cf

$ git log f55cdaa90..784515364 --date=short --no-merges --format='%ad %ae %s'
2023-11-27 vigneshv Do not store colorproperties until alpha item is found
2023-11-28 maryla Add metadata about the alternate image to the gainMap struct. (#1812)
2023-11-27 wtc Allocate the threadData array directly
2023-11-24 vrabaud Fix backward compatibility of AVIF_LOCAL_RAV1E (#1807)
2023-11-23 wtc README.md: Change "AOM" (libaom) to "AV1"

Created with:
  roll-dep src/third_party/libavif/src

Bug: 1504792
Change-Id: I3f0a76e94178f38ae648d96c8902452c97221570
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5067055
Reviewed-by: Dale Curtis <dalecurtis@chromium.org>
Commit-Queue: Vignesh Venkat <vigneshv@google.com>
Reviewed-by: Wan-Teh Chang <wtc@google.com>
Cr-Commit-Position: refs/heads/main@{#1230349}

[modify] https://crrev.com/d4c56a954852f77959ba6426e3b37f0865abd4c6/third_party/libavif/src
[modify] https://crrev.com/d4c56a954852f77959ba6426e3b37f0865abd4c6/DEPS


### vi...@google.com (2023-11-29)

[Empty comment from Monorail migration]

### vi...@google.com (2023-11-29)

The fix has to be merged to 118, 119 and 120. The CLs are here:
M118: crrev.com/c/5066687
M119: crrev.com/c/5069378
M120: crrev.com/c/5069673

### [Deleted User] (2023-11-29)

Merge review required: a commit with DEPS changes was detected.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: harrysouders (Android), harrysouders (iOS), obenedict (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-11-29)

Merge review required: a commit with DEPS changes was detected.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: eakpobaro (Android), eakpobaro (iOS), dgagnon (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-11-29)

Merge review required: a commit with DEPS changes was detected.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), govind (iOS), ceb (ChromeOS), danielyip (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### vi...@google.com (2023-11-29)

> 1. Why does your merge fit within the merge criteria for these milestones?

Fixes a high severity security bug.

> 2. What changes specifically would you like to merge? Please link to Gerrit.

M118: crrev.com/c/5066687
M119: crrev.com/c/5069378
M120: crrev.com/c/5069673


> 3. Have the changes been released and tested on canary?

Yes.

> 4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?

N/A.


### cl...@chromium.org (2023-11-29)

ClusterFuzz testcase 6644769468383232 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1230316:1230351

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### [Deleted User] (2023-11-29)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-29)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-11-29)

Last planned updates of M119 Stable and M118 Extended Stable shipped yesterday, so merges to M119 and M118 are not needed. Since the roll with this fix just landed on Canary < 24 hours ago, let's let it get a bit more bake time for M120. M120 Stable RC was just cut yesterday, so there's plenty of time for bake and review for this fix to be included in the first refresh of M120 Stable. 

### vi...@google.com (2023-11-29)

Amy, thanks for the update. The plan sounds good to me.

Please mark the bug as merge approved for 120 when it's appropriate and i will submit the merge. Thank you!

### am...@google.com (2023-11-30)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-11-30)

Congratulations! The Chrome VRP Panel has decided to award you $7,000 for this report of memory corruption in a sandboxed process. Thank you for your efforts and reporting this issue to us -- nice work! 

### am...@google.com (2023-11-30)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-12-04)

120 merge approved, please merge this fix (CP for 120 listed in c#19) to branch 6099 at your earliest convenience (before EOD Thursday, 7 December) so this fix can be included in the first update of M120 Stable -- thank you! 

### vi...@google.com (2023-12-05)

The merge CL is here: https://chromium-review.googlesource.com/c/chromium/src/+/5069673

I will submit it by EOD today (5th of December).

### gi...@appspot.gserviceaccount.com (2023-12-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/00fa4c3ca7340c767dccc4c55ca6f5261d630d1d

commit 00fa4c3ca7340c767dccc4c55ca6f5261d630d1d
Author: Vignesh Venkatasubramanian <vigneshv@google.com>
Date: Tue Dec 05 22:44:34 2023

[M120] Roll src/third_party/libavif/src/ 466d5e5..1a78d97 (1 commits)

https://chromium.googlesource.com/external/github.com/AOMediaCodec/libavif.git/+log/466d5e5..1a78d97

$ git log 466d5e5..1a78d97 --date=short --no-merges --format='%ad %ae %s'
2023-11-28 vigneshv@google.com Do not store colorproperties until alpha item is found

Bug: 1504792
Test: blink_platform_unittests
Change-Id: Ifbe26da53eba8e4b3fd9e9b0cafb01e35934dd72
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5069673
Reviewed-by: Wan-Teh Chang <wtc@google.com>
Commit-Queue: Vignesh Venkat <vigneshv@google.com>
Reviewed-by: Dale Curtis <dalecurtis@chromium.org>
Cr-Commit-Position: refs/branch-heads/6099@{#1411}
Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}

[modify] https://crrev.com/00fa4c3ca7340c767dccc4c55ca6f5261d630d1d/third_party/libavif/src
[modify] https://crrev.com/00fa4c3ca7340c767dccc4c55ca6f5261d630d1d/DEPS


### am...@chromium.org (2023-12-11)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-12-11)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-11)

LTS Milestone M114

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### vo...@google.com (2023-12-12)

[Empty comment from Monorail migration]

### vi...@google.com (2023-12-12)

This issue is not present in M114. It was a regression introduced later.

### vo...@google.com (2023-12-13)

[Empty comment from Monorail migration]

### am...@google.com (2023-12-14)

[Empty comment from Monorail migration]

### am...@google.com (2023-12-14)

[Comment Deleted]

### ha...@tencent.com (2023-12-28)

Is M115/M116/M117 affected ?

### wt...@google.com (2024-01-03)

M115, M116, and M117 are all affected.

M117 uses libavif revision 397f74c8e289386eb7d309b2f8041d8a190db29a.

M116 uses libavif revision 781d6a6467d82d8ba36256f31b6593a33c03345d.

M115 uses libavif revision 094e6166339bc317d54b42460232c28193ea4daf.

These libavif revisions all contain libavif commit c17d24ad2281fee383700e0710e019758a1969ad, which introduced the bug:
https://github.com/AOMediaCodec/libavif/commit/c17d24ad2281fee383700e0710e019758a1969ad

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1504792?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-03-07)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40945359)*
