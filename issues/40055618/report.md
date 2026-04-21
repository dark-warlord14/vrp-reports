# Security: use-of-uninitialized-value in libavif when decode the crafted avif file

| Field | Value |
|-------|-------|
| **Issue ID** | [40055618](https://issues.chromium.org/issues/40055618) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Media |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ha...@gmail.com |
| **Assignee** | wt...@google.com |
| **Created** | 2021-04-21 |
| **Bounty** | $7,500.00 |

## Description

**VULNERABILITY DETAILS**  

use-of-uninitialized-value in libavif when decode the crafted avif file

**VERSION**  

latest libavif version

Since the chromium adopt the libavif as the codec to the avif format, this crash may also happened on the chrome when decode the avif file.

**REPRODUCTION CASE**  

Build thee libavif library with memory sanitizer:

1. (Note that since the chromium reuse the source libavif of the github, I use the source of the github instead.)
2. git clone <https://github.com/AOMediaCodec/av1-avif.git>
3. build the dav1d with msan:

modify the ext/dav1d.cmd file in the root source, change the

meson --default-library=static --buildtype release ..

to

meson --default-library=static --buildtype release .. -Db\_sanitize=memory

Then compile it running ./ext/dav1d.cmd

4. build the libavif avif\_example\_decode\_file (example apps) with msan:

mkdir build  

cd build  

cmake -DBUILD\_SHARED\_LIBS=0 -DAVIF\_CODEC\_DAV1D=1 -DAVIF\_LOCAL\_DAV1D=1 -DAVIF\_BUILD\_EXAMPLES=1 ..  

make avif\_example\_decode\_file

5. run the avif\_example\_decode\_file with the uploaded crash file:  
   
   ./avif\_example\_decode\_file avif-reformat-use-of-uninitialized-value.avif

Then the lib crash with the use-of-uninitialized.

Type of crash: Use-of-uninitialized-value  

Crash State:

==115154==WARNING: MemorySanitizer: use-of-uninitialized-value  

#0 0x4c91b8 in avifImageYUVAnyToRGBAnySlow /libavif/src/reformat.c:584:84  

#1 0x4c91b8 in avifImageYUVToRGB /libavif/src/reformat.c:1212:29  

#2 0x494d37 in LLVMFuzzerTestOneInput /libavif/examples/decode\_fuzzer.c:45:52  

#3 0x495acf in main /libavif/examples/decode\_fuzzer.c:123:5  

#4 0x7faf61fa8bf6 in \_\_libc\_start\_main /build/glibc-S9d2JN/glibc-2.27/csu/../csu/libc-start.c:310  

#5 0x41b8e9 in \_start (/libavif/memory\_build/decode\_fuzzer+0x41b8e9)

SUMMARY: MemorySanitizer: use-of-uninitialized-value /libavif/src/reformat.c:584:84 in avifImageYUVAnyToRGBAnySlow  

Exiting

**CREDIT INFORMATION**  

Reporter credit: Chaoyuan Peng

## Attachments

- [avif-reformat-use-of-uninitialized-value.avif](attachments/avif-reformat-use-of-uninitialized-value.avif) (application/octet-stream, 322 B)

## Timeline

### [Deleted User] (2021-04-21)

[Empty comment from Monorail migration]

### ca...@chromium.org (2021-04-22)

Triaging as medium severity since libavif is used in the renderer. wtc: Passing to you since you are listed as a libavif owner. Can you help further triage this one (and reassign as appropriate)? Thanks.

[Monorail components: Blink>Media]

### ca...@chromium.org (2021-04-22)

[Empty comment from Monorail migration]

### wt...@google.com (2021-04-23)

happyercat: Thank you very much for the bug report. I will take a look.

### [Deleted User] (2021-04-23)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-04-23)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### wt...@google.com (2021-04-28)

I tracked down the bug. The uninitialized memory error is in dav1d. I wrote a fix at https://code.videolan.org/videolan/dav1d/-/merge_requests/1194.

The bug occurs when the frame uses film grain synthesis (it may require certain film grain parameters, I did not look closely), has an odd number of rows, and chroma is subsampled vertically (i.e., YUV 4:2:0). Under these conditions, the last row of the chroma planes contains uninitialized values for column indexes >= half of the stride.

Notes:

1. The steps to reproduce the bug in the original description have some errors. Fortunately I can build dav1d and libavif with msan in Google's internal source repository.

2. I cannot reproduce the error using avif_example_decode_file, but I can reproduce it using avifenc and avif_decode_fuzzer. Note that the stack trace in the original description is a stack trace from  avif_decode_fuzzer, not avif_example_decode_file.

### wt...@google.com (2021-04-28)

I believe this bug also affects AV1 videos, even though the reproducer test case is an AVIF image.

### wt...@google.com (2021-04-28)

It turns out that this bug was independently discovered by Google's internal ClusterFuzz on Feb 27, 2021 (b/181396790). Regrettably I failed to track down that bug quickly, and then ClusterFuzz closed that bug later because some change to libavif made the reproducer testcase fail the avifDecoderParse() call in avif_decoder_fuzzer.cc.

### ha...@gmail.com (2021-04-30)

[Comment Deleted]

### wt...@google.com (2021-04-30)

Hi happyercat,

My fix for dav1d has not been merged: https://code.videolan.org/videolan/dav1d/-/merge_requests/1194.

A poc of AV1 video would be helpful but is not necessary. (I believe we can create one by extracting the AV1 bitstream out of avif-reformat-use-of-uninitialized-value.avif and putting it in an IVF file.)

### ca...@chromium.org (2021-04-30)

Re #10: cc-ing adetaylor for the VRP and CVE questions, because I'm not sure about eligibility since the internal fuzzer had also discovered the bug.

### gi...@appspot.gserviceaccount.com (2021-05-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/7dca464eca4c9f062b8b6532b51ab92211634bf6

commit 7dca464eca4c9f062b8b6532b51ab92211634bf6
Author: Wan-Teh Chang <wtc@google.com>
Date: Sat May 01 01:27:07 2021

Roll src/third_party/dav1d/libdav1d/ f06148e7c..136585101 (20 commits)

https://chromium.googlesource.com/external/github.com/videolan/dav1d.git/+log/f06148e7c755..136585101bd5

$ git log f06148e7c..136585101 --date=short --no-merges --format='%ad %ae %s'
2021-04-28 wtc Subsample out->p.h correctly in dav1d_apply_grain
2021-03-22 martin arm64: filmgrain: Add NEON implementation of the generate_grain_y function
2021-03-26 martin checkasm: Implement printing of grain lut entries
2021-04-26 martin arm64: filmgrain: Add the missing HIGHBD_DECL_SUFFIX for the fguv functions
2021-04-27 martin Remove a variable that is set but not used
2021-03-16 martin checkasm: filmgrain: Add a padded check for fgy and fguv
2021-03-16 martin checkasm: Extend the padding checker to allow for some amount of overwrite
2021-02-19 martin checkasm: ipred: Use the padded pixel checking function
2021-02-19 martin checkasm: Add macros for allocating and checking padded pixel buffers
2021-04-22 martin x86: Fix writes past the intended area in AVX2 fguv
2021-04-14 jamrial dav1d: add event flags to the decoding process
2021-03-22 martin arm64: filmgrain: Share the prologue of the fgy function
2021-03-15 martin arm64: filmgrain: Add NEON implementation of the fguv function
2021-03-24 martin attributes: Add a CHECK_OFFSET macro for verifying struct offsets
2021-03-21 martin checkasm: filmgrain: Check all overlap combinations in each run
2021-03-20 martin filmgrain: Use the BITDEPTH_MAX macro and round2 helper function
2021-04-02 code CI: Fix asm checks
2021-03-16 martin checkasm: Drop one layer of macro expansion for concatenation
2021-03-12 martin arm64: Add NEON implementation of fgy_32x32xn
2021-03-07 code CI: Add check for illegal instructions

Created with:
  roll-dep src/third_party/dav1d/libdav1d
R=dalecurtis@chromium.org

Bug: 1201074
Change-Id: I67be894a4c4a9ef41fa653fd6a3b27f252299531
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2863934
Reviewed-by: Dale Curtis <dalecurtis@chromium.org>
Commit-Queue: Wan-Teh Chang <wtc@google.com>
Cr-Commit-Position: refs/heads/master@{#878146}

[modify] https://crrev.com/7dca464eca4c9f062b8b6532b51ab92211634bf6/DEPS
[modify] https://crrev.com/7dca464eca4c9f062b8b6532b51ab92211634bf6/third_party/dav1d/dav1d_generated.gni


### wt...@google.com (2021-05-05)

Hi Adrian (adetaylor),

This bug was assigned the target milestone M-91 by sheriffbot  in https://crbug.com/chromium/1201074#c5. I think it is sufficient to fix this bug in M-92. May I change the milestone and target to M-92 and Target-92?

This bug affects AV1 videos and AVIF images only under the following conditions:

The bug occurs when the frame uses film grain synthesis (it may require certain film grain parameters, I did not look closely), has an odd frame height, and chroma is subsampled vertically (i.e., YUV 4:2:0). Under these conditions, the last row of the chroma planes contains uninitialized values for column indexes >= half of the stride.

Since frame height is usually an even number and film grain synthesis is not a commonly used feature, this combination is rare in practice.

Thank you.

### ad...@chromium.org (2021-05-05)

Hi wtc, thanks for the thorough explanation!

First, could you mark this bug as Fixed if it's fixed? https://chromium.googlesource.com/chromium/src/+/master/docs/security/security-labels.md#TOC-Merge-labels - then Sheriffbot can add appropriate merge labels, this can go to the VRP panel, etc.

> Since frame height is usually an even number and film grain synthesis is not a commonly used feature, this combination is rare in practice.

I don't think that's relevant: An attacker can presumably craft such a file using whatever features they require to exploit this bug. Or, does Chrome reject such types of file before attempting to decode them?

This is medium severity, so we'd be pretty keen to merge this back to M91. Is your concern about the stability risk from a big roll of dav1d?

### wt...@google.com (2021-05-05)

Hi Adrian,

Thank you for your reply. Yes, I am worried about the stability risk from a big roll of dav1d.

### [Deleted User] (2021-05-06)

[Empty comment from Monorail migration]

### ad...@google.com (2021-05-06)

OK. Let's keep this for M92 then. Thanks.

### wt...@google.com (2021-05-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-06)

[Empty comment from Monorail migration]

### am...@google.com (2021-05-20)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-05-20)

[Comment Deleted]

### am...@chromium.org (2021-05-20)

Congratulations, Chaoyuan Peng! The VRP Panel has decided to award you $7500 for this report. A member of our finance team will be in touch in the coming days to arrange payment. Nice work!

### am...@google.com (2021-05-21)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-07-19)

[Empty comment from Monorail migration]

### am...@google.com (2021-07-19)

[Empty comment from Monorail migration]

### am...@google.com (2021-08-03)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-12)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ja...@google.com (2021-09-08)

Skipping for LTS due to https://crbug.com/chromium/1201074#c16.

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1201074?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40055618)*
