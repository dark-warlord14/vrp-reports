# Security: heap-use-after-free in libavif when decode the crafted avif file.

| Field | Value |
|-------|-------|
| **Issue ID** | [40942082](https://issues.chromium.org/issues/40942082) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Images>Codecs |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | me...@gmail.com |
| **Assignee** | vi...@chromium.org |
| **Created** | 2023-11-13 |
| **Bounty** | $7,000.00 |

## Description

**VULNERABILITY DETAILS**

heap-use-after-free in libavif when decode the crafted avif file. cause out-of-bounds reading bug.

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

./avifdec poc1 test.jpg

Then :  

READ of size 4 at 0x624000002124 thread T0  

#0 0x7f69449ddb6e in avifMetaFindAlphaItem libavif/src/read.c:4303  

#1 0x7f69449e03e0 in avifDecoderReset libavif/src/read.c:4687  

#2 0x7f69449dc42c in avifDecoderParse libavif/src/read.c:4107  

#3 0x55ae55fa3b09 in main libavif/apps/avifdec.c:335  

#4 0x7f69445c4082 in \_\_libc\_start\_main (/lib/x86\_64-linux-gnu/libc.so.6+0x24082)  

#5 0x55ae55fa1acd in \_start ( libavif/build/avifdec+0xaacd)

0x624000002124 is located 36 bytes inside of 7168-byte region [0x624000002100,0x624000003d00)  

freed by thread T0 here:  

#0 0x7f6944b1f5b8 in \_\_interceptor\_free (/lib/x86\_64-linux-gnu/libasan.so.4+0xdf5b8)  

#1 0x7f69449bdbeb in avifFree libavif/src/mem.c:17  

#2 0x7f6944a00f3f in avifArrayPush libavif/src/utils.c:115  

#3 0x7f69449c2470 in avifMetaFindOrCreateItem libavif/src/read.c:796  

#4 0x7f69449dda8d in avifMetaFindAlphaItem libavif/src/read.c:4296  

#5 0x7f69449e03e0 in avifDecoderReset libavif/src/read.c:4687  

#6 0x7f69449dc42c in avifDecoderParse libavif/src/read.c:4107  

#7 0x55ae55fa3b09 in main libavif/apps/avifdec.c:335  

#8 0x7f69445c4082 in \_\_libc\_start\_main (/lib/x86\_64-linux-gnu/libc.so.6+0x24082)

previously allocated by thread T0 here:  

#0 0x7f6944b1f950 in \_\_interceptor\_malloc (/lib/x86\_64-linux-gnu/libasan.so.4+0xdf950)  

#1 0x7f69449bdbd1 in avifAlloc libavif/src/mem.c:12  

#2 0x7f6944a00e50 in avifArrayPush libavif/src/utils.c:108  

#3 0x7f69449c2470 in avifMetaFindOrCreateItem libavif/src/read.c:796  

#4 0x7f69449c96c2 in avifParseItemLocationBox libavif/src/read.c:1722  

#5 0x7f69449d2a3b in avifParseMetaBox libavif/src/read.c:2742  

#6 0x7f69449d9b2a in avifParse libavif/src/read.c:3744  

#7 0x7f69449dbc4f in avifDecoderParse libavif/src/read.c:4060  

#8 0x55ae55fa3b09 in main libavif/apps/avifdec.c:335  

#9 0x7f69445c4082 in \_\_libc\_start\_main (/lib/x86\_64-linux-gnu/libc.so.6+0x24082)

SUMMARY: AddressSanitizer: heap-use-after-free libavif/src/read.c:4303 in avifMetaFindAlphaItem

**CREDIT INFORMATION**  

Reporter credit: Fudan University

## Attachments

- [poc1](attachments/poc1) (text/plain, 1.8 KB)
- [bug-1501770-tentative.txt](attachments/bug-1501770-tentative.txt) (text/plain, 2.7 KB)

## Timeline

### [Deleted User] (2023-11-13)

[Empty comment from Monorail migration]

### dr...@chromium.org (2023-11-13)

I was able to trigger a renderer crash in M119 just by opening this test file, so it seems like this does impact Chromium. Memory corruption in the renderer is High severity.

Triaging to //third_party/libavif OWNERS. sandersd@, liberato@ - I'm assuming this is an upstream bug. Can you work with upstream to get this fixed?



[Monorail components: Internals>Media>Codecs]

### [Deleted User] (2023-11-13)

[Empty comment from Monorail migration]

### dr...@chromium.org (2023-11-13)

[Empty comment from Monorail migration]

[Monorail components: -Internals>Media>Codecs Internals>Images>Codecs]

### [Deleted User] (2023-11-13)

[Empty comment from Monorail migration]

### sa...@chromium.org (2023-11-13)

[Empty comment from Monorail migration]

### wt...@google.com (2023-11-13)

[Empty comment from Monorail migration]

### wt...@google.com (2023-11-13)

Hi me3h0n,

Thank you for the bug report.

Vignesh: I think this bug was also introduced in "Allow alpha to be specified as an auxl of color tiles", like https://crbug.com/chromium/1501766:
https://github.com/AOMediaCodec/libavif/pull/1396

The code was later modified in https://github.com/AOMediaCodec/libavif/pull/1401.

I attached a tentative patch from my initial investigation, mainly to pinpoint the location of the bug.

This bug is caused by avifMetaFindOrCreateItem() reallocating the meta->items array to a larger size, invalidating any existing pointers to meta->items array elements.

Note that avifMetaFindItem() was renamed avifMetaFindOrCreateItem() in https://github.com/AOMediaCodec/libavif/pull/1694.

### vi...@chromium.org (2023-11-14)

[Empty comment from Monorail migration]

### vi...@chromium.org (2023-11-14)

@wtc, thanks for the analysis and finding the root cause. it made it easy for me to fix it.

Upstream fix in flight: https://github.com/AOMediaCodec/libavif/pull/1757

### wt...@google.com (2023-11-14)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-14)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2023-11-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/cb352715778d8efbcd2ba2d47ed2733d41ebd9cf

commit cb352715778d8efbcd2ba2d47ed2733d41ebd9cf
Author: Vignesh Venkatasubramanian <vigneshv@google.com>
Date: Wed Nov 15 17:15:53 2023

Roll src/third_party/libavif/src/ 026096beb..6d62963f7 (7 commits)

https://chromium.googlesource.com/external/github.com/AOMediaCodec/libavif.git/+log/026096bebdbe..6d62963f74aa

$ git log 026096beb..6d62963f7 --date=short --no-merges --format='%ad %ae %s'
2023-11-13 vigneshv Remove potential out of bound access to alphaItemIndices
2023-11-13 vigneshv Do not store item pointers until all items are created
2023-11-14 maryla Format avifgainmaputil. (#1759)
2023-11-13 fdintino fix: avif_android jni build.gradle config ndkVersion and target (#1751)
2023-11-13 fdintino ci: Fix a typo in the ci-unix-static-av2 workflow so AV1+AV2 tests run (#1748)
2023-11-13 maryla Add 'combine' command to avifgainmaputil. (#1747)
2023-11-13 yguyon Return DECODE_FAILED on tile/choice codec mismatch (#1753)

Created with:
  roll-dep src/third_party/libavif/src

Bug: 1501766, 1501770
Change-Id: I6f4e229379103b0f2fad8b340d12c4336f18d36e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5032655
Reviewed-by: Dale Curtis <dalecurtis@chromium.org>
Reviewed-by: Wan-Teh Chang <wtc@google.com>
Commit-Queue: Wan-Teh Chang <wtc@google.com>
Cr-Commit-Position: refs/heads/main@{#1224997}

[modify] https://crrev.com/cb352715778d8efbcd2ba2d47ed2733d41ebd9cf/third_party/libavif/src
[modify] https://crrev.com/cb352715778d8efbcd2ba2d47ed2733d41ebd9cf/DEPS


### vi...@chromium.org (2023-11-16)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-16)

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

### [Deleted User] (2023-11-16)

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

### [Deleted User] (2023-11-16)

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

### vi...@chromium.org (2023-11-16)

[Empty comment from Monorail migration]

### vi...@chromium.org (2023-11-16)

re merge request:

1. Why does your merge fit within the merge criteria for these milestones?

It is fixing a high severity security issue.

2. What changes specifically would you like to merge? Please link to Gerrit.

The fixes are in the libavif third party library. I am working on creating chromium CLs to for 118, 119 and 120 to include just the fix necessary for this bug from the upstream repository.

3. Have the changes been released and tested on canary?

Yes.

6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

No.

### [Deleted User] (2023-11-17)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-17)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-11-20)

Similar to https://crbug.com/chromium/1501766, the roll of libavif with the security fixes for that issue and this one seems to have not impact stability on Canary since it landed five days ago. 
Approving CP of https://github.com/AOMediaCodec/libavif/pull/1757/files to be backmerged to 120, 119, and 118 accordingly. 
Please backmerge the CPs of this fix to 120 Beta / branch 6099, 119 Stable / branch 6045, and 118 Extended Stable / branch 5993 at your earliest convenience, but before EOD Friday, 24 November so this fix can be included in the next security updates for each (since we are in release freeze this week). 

### vi...@chromium.org (2023-11-20)

Thank you Amy, i will do the cherry-picks for 118, 119 and 120 shortly.

### vi...@chromium.org (2023-11-20)

The cherry-pick CLs are here:
M118: https://chromium-review.googlesource.com/c/chromium/src/+/5046038
M119: https://chromium-review.googlesource.com/c/chromium/src/+/5046654
M120: https://chromium-review.googlesource.com/c/chromium/src/+/5046224

### gi...@appspot.gserviceaccount.com (2023-11-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/bf106c953ef13ef0efd3057bd4d22b96a624a968

commit bf106c953ef13ef0efd3057bd4d22b96a624a968
Author: Vignesh Venkatasubramanian <vigneshv@google.com>
Date: Tue Nov 21 00:07:24 2023

[M119] Roll src/third_party/libavif/src/ 0d4747a..1f2ccf0 (2 commits)

https://chromium.googlesource.com/external/github.com/AOMediaCodec/libavif.git/+log/0d4747a..1f2ccf0

$ git log 0d4747a..1f2ccf0 --date=short --no-merges --format='%ad %ae %s'
2023-11-15 vigneshv@google.com Remove potential out of bound access to alphaItemIndices
2023-11-15 vigneshv@google.com Do not store potentially invalid pointers

Bug: 1501766, 1501770
Test: blink_platform_unittests
Change-Id: I0c976d474b0ec9635249094a9cd0df4f58e50869
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5046654
Commit-Queue: Vignesh Venkat <vigneshv@google.com>
Reviewed-by: Wan-Teh Chang <wtc@google.com>
Reviewed-by: Dale Curtis <dalecurtis@chromium.org>
Cr-Commit-Position: refs/branch-heads/6045@{#1422}
Cr-Branched-From: 905e8bdd32d891451d94d1ec71682e989da2b0a1-refs/heads/main@{#1204232}

[modify] https://crrev.com/bf106c953ef13ef0efd3057bd4d22b96a624a968/third_party/libavif/src
[modify] https://crrev.com/bf106c953ef13ef0efd3057bd4d22b96a624a968/DEPS


### gi...@appspot.gserviceaccount.com (2023-11-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/d4647c411960c46228bea0acf957c949ab868a43

commit d4647c411960c46228bea0acf957c949ab868a43
Author: Vignesh Venkatasubramanian <vigneshv@google.com>
Date: Tue Nov 21 00:09:05 2023

[M120] Roll src/third_party/libavif/src/ 622336e..466d5e5 (2 commits)

https://chromium.googlesource.com/external/github.com/AOMediaCodec/libavif.git/+log/622336e..466d5e5

$ git log 622336e..466d5e5 --date=short --no-merges --format='%ad %ae %s'
2023-11-13 vigneshv@google.com Remove potential out of bound access to alphaItemIndices
2023-11-16 vigneshv@google.com Do not store item pointers until all items are created

Bug: 1501766, 1501770
Test: blink_platform_unittests
Change-Id: I79c2fac1fe21b9c9f5cf303dd16ccc0918ae2984
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5046224
Reviewed-by: Dale Curtis <dalecurtis@chromium.org>
Reviewed-by: Wan-Teh Chang <wtc@google.com>
Commit-Queue: Vignesh Venkat <vigneshv@google.com>
Cr-Commit-Position: refs/branch-heads/6099@{#906}
Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}

[modify] https://crrev.com/d4647c411960c46228bea0acf957c949ab868a43/third_party/libavif/src
[modify] https://crrev.com/d4647c411960c46228bea0acf957c949ab868a43/DEPS


### [Deleted User] (2023-11-21)

LTS Milestone M114

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2023-11-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/6cc0d9aa5b3fb3dec1ec0e1e24253b3c10110b88

commit 6cc0d9aa5b3fb3dec1ec0e1e24253b3c10110b88
Author: Vignesh Venkatasubramanian <vigneshv@google.com>
Date: Tue Nov 21 00:14:19 2023

[M118] Roll src/third_party/libavif/src/ d1c26fa..b2d36b1 (2 commits)

https://chromium.googlesource.com/external/github.com/AOMediaCodec/libavif.git/+log/d1c26fa..b2d36b1

$ git log d1c26fa..b2d36b1 --date=short --no-merges --format='%ad %ae %s'
2023-11-15 vigneshv@google.com Remove potential out of bound access to alphaItemIndices
2023-11-15 vigneshv@google.com Do not store potentially invalid pointers

Bug: 1501766, 1501770
Test: blink_platform_unittests
Change-Id: I72915b1187ca651e6f47f8d44e946644ebe9fce4
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5046038
Reviewed-by: Dale Curtis <dalecurtis@chromium.org>
Commit-Queue: Vignesh Venkat <vigneshv@google.com>
Reviewed-by: Wan-Teh Chang <wtc@google.com>
Cr-Commit-Position: refs/branch-heads/5993@{#1630}
Cr-Branched-From: 511350718e646be62331ae9d7213d10ec320d514-refs/heads/main@{#1192594}

[modify] https://crrev.com/6cc0d9aa5b3fb3dec1ec0e1e24253b3c10110b88/third_party/libavif/src
[modify] https://crrev.com/6cc0d9aa5b3fb3dec1ec0e1e24253b3c10110b88/DEPS


### rz...@google.com (2023-11-21)

[Empty comment from Monorail migration]

### vi...@chromium.org (2023-11-21)

I just checked the version of libavif in M114. The git hash is `1af8cea3d1b3a05ecbcb0e39d99a7f0183e6ce13` and that version of libavif is not susceptible to this bug. So no action is necessary for M114.

### rz...@google.com (2023-11-22)

Thanks vigneshv@, labelling as not applicable for 114.

### am...@google.com (2023-11-22)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-11-22)

Congratulations! The Chrome VRP Panel has decided to award you $7,000 for this report of a bug that allows for memory corruption in a sandboxed process. A member of our finance team will be in touch with you soon to arrange payment. Thank you for your efforts and reporting this issue to us -- nice work! 

### am...@google.com (2023-11-27)

[Empty comment from Monorail migration]

### pg...@google.com (2023-11-28)

[Empty comment from Monorail migration]

### pg...@google.com (2023-11-29)

[Empty comment from Monorail migration]

### pg...@google.com (2023-11-29)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### am...@chromium.org (2024-02-02)

[Empty comment from Monorail migration]

### is...@google.com (2024-02-02)

This issue was migrated from crbug.com/chromium/1501770?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-02-23)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40942082)*
